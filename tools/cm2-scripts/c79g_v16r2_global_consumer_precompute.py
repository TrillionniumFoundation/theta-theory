#!/usr/bin/env python3
"""Read-only C79g v16r2 global-consumer precomputation.

This helper is deliberately *not* a protocol consumer.  It does not import,
compile, execute, or inspect any producer/consumer/launcher source.  It reads
only the already frozen C55A/C55B, C42/C53, C78L and C78S evidence, verifies
their bytes and filesystem identities, and reconstructs the three prospective
row streams in memory.  No candidate, manifest, outer receipt, authority
head, credit, or runtime file is written.  The only output is a JSON report on
stdout.

The reconstruction is intentionally independent of the v15 consumer module;
the row schemas and closure operations are reproduced here so this check can
serve as a no-producer preflight for v16r2.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from collections import Counter, defaultdict
from typing import Any, Iterable, Mapping

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

# Immutable, already published input pins.  These are copied from the frozen
# evidence descriptors; they are data, not executable protocol code.
UNIVERSE = 76_832
BASELINE = 75_684
OVERLAY_COUNT = 1_148
LARGE_COUNT = 1_124
SINGLETON_COUNT = 24
PAIR_COUNT = 862
BASELINE_PAIRS = 288
LARGE_PAIRS = 562
SINGLETON_PAIRS = 12

TERMINALS = {
    "CONNECTED_TO_KNOWN",
    "EARLIEST_PREFIX_EXCLUDED",
    "SOURCE_GRAZING_OR_CEMETERY",
    "TYPED_EVENT_GRAPH",
}
LARGE_MAP = {
    "WHOLE_PUBLIC_CELL_STRICT_EXCLUSION": (
        "EARLIEST_PREFIX_EXCLUDED",
        "C78L_WHOLE_STRICT_TO_EARLIEST_PREFIX_EXCLUDED",
    ),
    "EXHAUSTIVE_PUBLIC_CELL_TYPED_EVENT_C3_PARTITION": (
        "TYPED_EVENT_GRAPH",
        "C78L_TYPED_PARTITION_TO_TYPED_EVENT_GRAPH",
    ),
}
SINGLETON_MAP = {
    "STRICT_EXCLUSION_ONLY": (
        "EARLIEST_PREFIX_EXCLUDED",
        "C78S_STRICT_ONLY_TO_EARLIEST_PREFIX_EXCLUDED",
    ),
    "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": (
        "SOURCE_GRAZING_OR_CEMETERY",
        "C78S_STRICT_PLUS_CEMETERY_TO_SOURCE_GRAZING_OR_CEMETERY",
    ),
}
CLOSURE = {
    "owner": True,
    "history": True,
    "glue": True,
    "two_sides": True,
    "incidence": True,
    "prefix_Kraft": True,
}

C55A_LEAF = OUT / "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json"
C55A_LEAF_SHA = "e80c012e3260e8f9e68d5858ba5d9dafd94611e2a1c1200d787a20e3842d8db6"
C55A_LEAF_OBJECT = "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90"

C55B_CELLS = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz"
C55B_CELLS_SHA = "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce"

C78L_PREFIX = "cm2_round306c78l_large_component_final_no_producer_consumer_v1"
C78L_NAMES = {
    "lock": "ZERO_CREDIT_STAGED_C78L_FINAL_CONSUMER_ONLY.lock",
    "tasks": C78L_PREFIX + "_task_consumption.jsonl.gz",
    "sides": C78L_PREFIX + "_task_side_occurrences.jsonl.gz",
    "cells": C78L_PREFIX + "_public_cell_rollup.jsonl.gz",
    "pairs": C78L_PREFIX + "_reflection_pair_rollup.jsonl.gz",
    "registry": C78L_PREFIX + "_source_registry.json",
    "result": C78L_PREFIX + "_result.json",
    "report": C78L_PREFIX + "_report.md",
    "manifest": C78L_PREFIX + "_manifest.sha256",
    "outer": C78L_PREFIX + "_outer_receipt.json",
}
C78L_PINS = {
    "lock": "3eaaa094987dce2545148d6e66c7fb241f2e7429b2988547eff064d05b0f8b19",
    "tasks": "e439be9ae8bc56ab00479baab6d23c029bc6274e7fda72d986153e97fed8c6c9",
    "sides": "7b2f7b57e1d7eeab6fbd1075f23e4d837e9521cb3c17a9d5ab6ef82de4dbea52",
    "cells": "a602f62b5c1c54253256887feac37359cdbb408ce2cad6678c853551e4a1c115",
    "pairs": "47b0c22dc66139964b1a93060ecae30b3fe4786ade5d842ca3e193c63becbbfa",
    "registry": "bf7aa990854950430effb0bc8a05c8e77051f25e3eca8b043cef9a91a237a893",
    "result": "0ab8e3dc9c379dbc14a276b05a394ef96e1cbe93392c940edb0cfe4f246cbb1d",
    "report": "42b6041bf25e94faec45dadf5c013d0d83f995a4e1f9c9e39d81e7c74a294be8",
    "manifest": "09c8a466d3906e01ea38d504f4dcb81b812e591ae7d515551674f7232982bd19",
    "outer": "e343c21c4c5ba1273d370e10eca5aba82e34c6b7f05609b7cb3c25878af0d044",
}
C78L_A = RUNTIME / "c78l-build-a3.9cdedea3"
C78L_B = RUNTIME / "c78l-build-b3.9cdedea3"
C78L_VERIFY_A = RUNTIME / "c78l-independent-v1-a3.a384bba4.json"
C78L_VERIFY_B = RUNTIME / "c78l-independent-v1-b3.a384bba4.json"
C78L_VERIFY_SHA = "22223e2aca6eaa069cfda7ab95da5f31b6adb36773544f9f2034bd01c6d1f0c1"
C78L_VERIFY_OBJECT = "850eba67fb2d343e8b607394469c8d2febf47229b26d86c6894249fd060c1419"
C78L_COMPLETION = RUNTIME / "c78l-completion-a3.a384bba4"
C78L_COMPLETION_NAMES = {
    "receipt": C78L_PREFIX + "_dual_completion_receipt.json",
    "manifest": C78L_PREFIX + "_dual_completion_manifest.sha256",
    "outer": C78L_PREFIX + "_dual_completion_outer_receipt.json",
}
C78L_COMPLETION_PINS = {
    "receipt": "235e876e53f1ee390ce0f89715fe465376de6b82e07ef6258068e26f35b8a3fd",
    "manifest": "c2ff451ad50cbe5f9b226569351e255b441f7ae500b81867c539b12a8656b1ff",
    "outer": "aa6da7b659af57e7eb5f45ea6e88fc67acdb2e6cbc51953e18e01f265a4e70e4",
}

C78S_PREFIX = "cm2_round306c78s_singleton_final_no_producer_consumer_v1"
C78S_NAMES = {
    "lock": "ZERO_CREDIT_CANDIDATE_SINGLETON_FINAL_NO_PRODUCER_CONSUMER_ONLY.lock",
    "children": C78S_PREFIX + "_child_dispositions.jsonl.gz",
    "sources": C78S_PREFIX + "_source_rollups.jsonl.gz",
    "pairs": C78S_PREFIX + "_reflection_pair_rollups.jsonl.gz",
    "cells": C78S_PREFIX + "_singleton_cell_rollups.jsonl.gz",
    "projection": C78S_PREFIX + "_global_enum_projection.jsonl.gz",
    "result": C78S_PREFIX + "_result.json",
    "report": C78S_PREFIX + "_report.md",
    "manifest": C78S_PREFIX + "_manifest.sha256",
    "outer": C78S_PREFIX + "_outer_receipt.json",
}
C78S_PINS = {
    "lock": "29e545e9b6fe75f95215a80bbbefee2a56668153f29a5afd42ea2afeddeb523e",
    "children": "cdb5606dd4561846e46bb484a3e4b34f11b6e89c8867c25acf4c43982dfc4783",
    "sources": "efad60b5cff0193033c92577d7c3b2e6c8788b47c8d7e45e0c474f59a491cc25",
    "pairs": "68493c4c1ef530c14b74cdac03a6e7cc632a0f788db05c15b69a58625b9bc614",
    "cells": "89d04fdb79cf5b6af95e6abc85978e684c6fcce86e221b28cf756b5e6afaaa7a",
    "projection": "2bb4e3c2885ed2d87b34ea7a79f2f850452eb402673d5cdfae8fdfdada0f27da",
    "result": "8256d10eb8f81db49ec33782f510e18ed61f3b8bfe8f9406adc457c152083ac4",
    "report": "c9ae55aff5ff8897023f0d8d9500cac2a7fedc1f14798d4e0db195d1597c839d",
    "manifest": "73aa1f256fcdc585b5c824ba5d0c48fd9d37de80054f2d4411df413880b982f4",
    "outer": "dd2ec68ec46fb8e6cf50032e575fe0429344c83d8e8979ca9a2f414f7522cabd",
}
C78S_A = RUNTIME / "c78s-build-a.v1"
C78S_B = RUNTIME / "c78s-build-b.v1"
C78S_VERIFY_NAME = C78S_PREFIX.replace("_v1", "") + "_independent_verification_v1.json"
# The frozen file uses the historical basename without the ``_v1`` segment.
C78S_VERIFY_NAME = "cm2_round306c78s_singleton_final_no_producer_consumer_independent_verification_v1.json"
C78S_VERIFY_SHA = "b9fe78455672fa873a23d6bd2d8c803dfa26ab38986275cd35aefc5cd51690c6"
C78S_VERIFY_OBJECT = "dff4cc4af2f1348a110c0010c58444607eb49707a63fb30380d405911f319d82"
C78S_FINAL_MANIFEST_NAME = C78S_PREFIX.replace("_v1", "") + "_final_manifest_v1.sha256"
C78S_FINAL_OUTER_NAME = C78S_PREFIX.replace("_v1", "") + "_final_outer_receipt_v1.json"
C78S_FINAL_MANIFEST_SHA = "568e60d5d67703a9fc9cf8fa4082865c3cd78474ba5bfac6f6fc435e38290642"
C78S_FINAL_OUTER_SHA = "6c682ee6e22340fe0a329f834e675198a541244a79b1577189e940bd488a9145"
C78S_FINAL_OUTER_OBJECT = "500efc48360a239817cce40106850d96dce257f15d57e7711ca3c8bb7bf57242"

C42_PARENT = RUNTIME / "candidates/c42-p391-formal-producer-20260811T044500Z-f1/parent_conservation.jsonl.gz"
C42_PARENT_SHA = "9e414b2fea9de614e73fd72f604fb857fb332dbfef49f11c33ae3929f68c8323"
C53_AUDIT = OUT / "cm2_round306c53_d02a_pair1_pair_level_successor_independent_audit_v1.json"
C53_AUDIT_SHA = "b58a6ba170e43be02ca414208e7197e746183dd335a49982b9ae28dab919497b"
C53_AUDIT_OBJECT = "a7bee7e57b6527c7bf9ea7f17966379c62a722fe9ce2ce2009f19f85a5afaa7c"
C53_HEAD = RUNTIME / "cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_HEAD_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_HEAD_OBJECT = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"
C53_CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
C42_C42_SEQUENCE = "00d8e4a88766a2bba46f9a06f528795773c0606d66cd71e87fa26700e2fa4807"
C53_C53_SEQUENCE = "eb1f66adc4f6a54819555a36bbeb108091614135761743cd4ec9fea0b51cba0e"


class AuditError(RuntimeError):
    """A fail-closed input or reconstruction error."""


def fail(message: str) -> None:
    raise AuditError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    ).encode("ascii")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    return sha_bytes(canonical(value))


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    if "row_sha256" in body:
        fail("row already closed")
    return {**body, "row_sha256": digest(body)}


def verify_row(row: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(row))
    claim = body.pop("row_sha256", None)
    if not isinstance(claim, str) or claim != digest(body):
        fail(label + ":row_sha256")


def verify_object(value: Mapping[str, Any], label: str,
                  expected: str | None = None) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    if not isinstance(claim, str) or claim != digest(body):
        fail(label + ":object_sha256")
    if expected is not None and claim != expected:
        fail(label + ":object pin")


def _identity(st: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        st.st_dev, st.st_ino, st.st_mode, st.st_size,
        st.st_mtime_ns, st.st_ctime_ns, st.st_nlink,
    )


def read_stable(path: Path, expected_sha: str | None = None,
                expected_mode: int | None = None) -> tuple[bytes, os.stat_result]:
    """Read one regular file with O_NOFOLLOW and identity stability checks."""
    flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            fail("not regular/nlink1: " + str(path))
        if expected_mode is not None and stat.S_IMODE(before.st_mode) != expected_mode:
            fail("mode mismatch: " + str(path))
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
        named = os.lstat(path)
        if _identity(before) != _identity(after) or _identity(before) != _identity(named):
            fail("identity drift: " + str(path))
        raw = b"".join(chunks)
    finally:
        os.close(fd)
    if expected_sha is not None and sha_bytes(raw) != expected_sha:
        fail("sha256 mismatch: " + str(path))
    return raw, before


def read_json(path: Path, expected_sha: str | None = None,
              expected_mode: int | None = None) -> tuple[Any, bytes, os.stat_result]:
    raw, st = read_stable(path, expected_sha, expected_mode)
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditError("invalid JSON: " + str(path)) from exc
    return value, raw, st


def read_gzip_rows(path: Path, expected_sha: str,
                   expected_mode: int, label: str) -> tuple[list[dict[str, Any]], bytes, os.stat_result]:
    raw, st = read_stable(path, expected_sha, expected_mode)
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
            plain = stream.read()
    except (OSError, EOFError) as exc:
        raise AuditError(label + ":gzip") from exc
    if not plain.endswith(b"\n"):
        fail(label + ":missing newline")
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(plain.splitlines(), 1):
        if not line:
            fail(label + ":blank line")
        try:
            row = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise AuditError(f"{label}:{index}:JSON") from exc
        if not isinstance(row, dict):
            fail(f"{label}:{index}:not object")
        verify_row(row, f"{label}:{index}")
        rows.append(row)
    return rows, raw, st


def directory_snapshot(path: Path, expected_names: set[str],
                       expected_mode: int) -> tuple[os.stat_result, dict[str, tuple[bytes, os.stat_result]]]:
    flags = os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISDIR(before.st_mode) or stat.S_IMODE(before.st_mode) != expected_mode:
            fail("directory mode/type: " + str(path))
        names = set(os.listdir(fd))
        if names != expected_names:
            fail("directory member set: " + str(path))
    finally:
        os.close(fd)
    members: dict[str, tuple[bytes, os.stat_result]] = {}
    for name in sorted(expected_names):
        members[name] = read_stable(path / name, expected_mode=0o444)
    after = os.stat(path, follow_symlinks=False)
    if _identity(before) != _identity(after):
        fail("directory identity drift: " + str(path))
    return before, members


def dual_surface(
        directory_a: Path, directory_b: Path, names: Mapping[str, str],
        pins: Mapping[str, str], expected_mode: int,
        label: str) -> tuple[dict[str, bytes], dict[str, bytes], dict[str, Any]]:
    expected_names = set(names.values())
    stat_a, files_a = directory_snapshot(directory_a, expected_names, expected_mode)
    stat_b, files_b = directory_snapshot(directory_b, expected_names, expected_mode)
    if (stat_a.st_dev, stat_a.st_ino) == (stat_b.st_dev, stat_b.st_ino):
        fail(label + ":A/B directory identity collision")
    a: dict[str, bytes] = {}
    b: dict[str, bytes] = {}
    identity_distinct = True
    for key, name in names.items():
        if sha_bytes(files_a[name][0]) != pins[key] or sha_bytes(files_b[name][0]) != pins[key]:
            fail(label + ":member pin:" + key)
        a[key], b[key] = files_a[name][0], files_b[name][0]
        if a[key] != b[key]:
            fail(label + ":A/B bytes:" + key)
        if (files_a[name][1].st_dev, files_a[name][1].st_ino) == (files_b[name][1].st_dev, files_b[name][1].st_ino):
            identity_distinct = False
    if not identity_distinct:
        fail(label + ":A/B member inode collision")
    return a, b, {"directory_identity_distinct": True, "member_identity_distinct": True}


def parse_manifest(raw: bytes, label: str) -> list[tuple[str, str]]:
    if not raw.endswith(b"\n"):
        fail(label + ":newline")
    result: list[tuple[str, str]] = []
    seen: set[str] = set()
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ", 1)
        if len(parts) != 2 or len(parts[0]) != 64 or parts[1] in seen:
            fail(label + ":entry")
        seen.add(parts[1])
        result.append((parts[0], parts[1]))
    return result


def line_sequence_sha(values: Iterable[str]) -> str:
    return sha_bytes(b"".join((value + "\n").encode("ascii") for value in values))


def validate_c78_metadata() -> dict[str, Any]:
    """Validate non-ledger frozen members without trusting their contents."""
    # C78L independent verification and completion are held outside the A/B
    # directories; their bytes and object closures are still checked.
    va, va_raw, va_st = read_json(C78L_VERIFY_A, C78L_VERIFY_SHA, 0o444)
    vb, vb_raw, vb_st = read_json(C78L_VERIFY_B, C78L_VERIFY_SHA, 0o444)
    if va_raw != vb_raw or (va_st.st_dev, va_st.st_ino) == (vb_st.st_dev, vb_st.st_ino):
        fail("C78L verification dual bytes/inodes")
    verify_object(va, "C78L verification", C78L_VERIFY_OBJECT)
    verify_object(vb, "C78L verification", C78L_VERIFY_OBJECT)
    completion_stat, completion = directory_snapshot(
        C78L_COMPLETION, set(C78L_COMPLETION_NAMES.values()), 0o755)
    completion_objects: dict[str, Any] = {}
    for key, name in C78L_COMPLETION_NAMES.items():
        raw, st = completion[name]
        if sha_bytes(raw) != C78L_COMPLETION_PINS[key]:
            fail("C78L completion pin:" + key)
        if key in {"receipt", "outer"}:
            try:
                obj = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise AuditError("C78L completion JSON:" + key) from exc
            completion_objects[key] = obj
    if "receipt" in completion_objects:
        verify_object(completion_objects["receipt"], "C78L completion receipt",
                      "4b627b9e05d4552ce1a5c55c31a2e9dc11e3e5067657691e0b3fdfdf53562cfe")
    if "outer" in completion_objects:
        verify_object(completion_objects["outer"], "C78L completion outer",
                      "d67abd63ffabefddcb7829cb781dc038a00498686726e54d806db10f3c2fc4a9")
    # C78S A/B directories contain exactly the ten base members plus the three
    # final verification members.
    s_names = dict(C78S_NAMES)
    s_names.update({
        "verification": C78S_VERIFY_NAME,
        "final_manifest": C78S_FINAL_MANIFEST_NAME,
        "final_outer": C78S_FINAL_OUTER_NAME,
    })
    s_pins = dict(C78S_PINS)
    s_pins.update({
        "verification": C78S_VERIFY_SHA,
        "final_manifest": C78S_FINAL_MANIFEST_SHA,
        "final_outer": C78S_FINAL_OUTER_SHA,
    })
    sa, sb, s_identity = dual_surface(
        C78S_A, C78S_B, s_names, s_pins, 0o555, "C78S")
    sv = json.loads(sa["verification"].decode("utf-8"))
    so = json.loads(sa["final_outer"].decode("utf-8"))
    verify_object(sv, "C78S verification", C78S_VERIFY_OBJECT)
    verify_object(so, "C78S final outer", C78S_FINAL_OUTER_OBJECT)
    expected_manifest = [
        (C78S_PINS[key], C78S_NAMES[key]) for key in C78S_NAMES
    ] + [(C78S_VERIFY_SHA, C78S_VERIFY_NAME)]
    if parse_manifest(sa["final_manifest"], "C78S final manifest") != expected_manifest:
        fail("C78S final manifest order")
    return {
        "C78L_verification_object": C78L_VERIFY_OBJECT,
        # C78L's historical verifier keeps these boundary fields at top level;
        # normalize them into a small private map for the caller.
        "C78L_verification_branch_boundary": {
            "branch_unresolved": va.get("branch_unresolved"),
            "public_global_unresolved_after_branch": va.get("public_global_unresolved_after_branch"),
            "public_global_unresolved_zero": va.get("public_global_unresolved_zero"),
        },
        "C78L_completion_member_count": len(completion),
        "C78S_final_member_count": len(s_names),
        "C78S_dual_identity": s_identity,
        "C78S_verification_object": C78S_VERIFY_OBJECT,
        "C78S_verification_branch_boundary": sv.get("branch_boundary", {}),
        "C78S_final_outer_object": C78S_FINAL_OUTER_OBJECT,
    }


def validate_c53() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    parent_rows, _, _ = read_gzip_rows(C42_PARENT, C42_PARENT_SHA, 0o664, "C42 parent")
    if len(parent_rows) != PAIR_COUNT:
        fail("C42 parent count")
    by_pair: dict[int, dict[str, Any]] = {}
    for row in parent_rows:
        pair = row.get("pair_index")
        if type(pair) is not int or pair in by_pair:
            fail("C42 pair index")
        by_pair[pair] = row
        if row.get("parent_Kraft_conservation") != "1" or row.get("D02_gate_credit") != 0 or row.get("terminal_reflection_transport_materialized") is not True:
            fail("C42 zero-credit/Kraft row")
    if set(by_pair) != set(range(PAIR_COUNT)):
        fail("C42 dense pair index")
    c42_sequence = [by_pair[i]["row_sha256"] for i in range(PAIR_COUNT)]
    if line_sequence_sha(c42_sequence) != C42_C42_SEQUENCE:
        fail("C42 row sequence")

    head, head_raw, _ = read_json(C53_HEAD, C53_HEAD_SHA, 0o444)
    # The global-head seal intentionally uses a field-specific closure name,
    # ``authority_seal_object_sha256``.  It is not an ordinary object with an
    # ``object_sha256`` member, so verify the exact seal convention here.
    head_body = copy.deepcopy(head)
    head_claim = head_body.pop("authority_seal_object_sha256", None)
    if head_claim != C53_HEAD_OBJECT or digest(head_body) != head_claim:
        fail("C53 global head:authority seal closure")
    if head.get("post_seal_effective_checkpoint_object_sha256") != C53_CHECKPOINT:
        fail("C53 checkpoint binding")

    audit, _, _ = read_json(C53_AUDIT, C53_AUDIT_SHA, 0o664)
    verify_object(audit, "C53 audit", C53_AUDIT_OBJECT)
    if audit.get("D02_gate_credit") != 0 or audit.get("formal_credit") != 0:
        fail("C53 nonzero credit")
    derivation = audit.get("post_seal_promotion_derivation")
    if not isinstance(derivation, dict):
        fail("C53 derivation missing")
    body = copy.deepcopy(derivation)
    claim = body.pop("promotion_derivation_object_sha256", None)
    if claim != digest(body) or derivation.get("parent_projection_count") != PAIR_COUNT:
        fail("C53 derivation closure")
    projections = derivation.get("parent_projections")
    if not isinstance(projections, list) or len(projections) != PAIR_COUNT:
        fail("C53 projection count")
    by_projection: dict[int, dict[str, Any]] = {}
    for projection in projections:
        pair = projection.get("pair_index")
        if type(pair) is not int or pair in by_projection:
            fail("C53 projection index")
        pbody = copy.deepcopy(projection)
        pclaim = pbody.pop("projection_object_sha256", None)
        if pclaim != digest(pbody) or projection.get("C42_parent_row_sha256") != by_pair[pair]["row_sha256"] or projection.get("D02_gate_credit") != 0:
            fail("C53 projection join")
        by_projection[pair] = projection
    if set(by_projection) != set(range(PAIR_COUNT)):
        fail("C53 dense projections")
    projection_sequence = [by_projection[i]["projection_object_sha256"] for i in range(PAIR_COUNT)]
    if line_sequence_sha(projection_sequence) != C53_C53_SEQUENCE:
        fail("C53 projection sequence")
    return parent_rows, projections, {
        "C42_parent_rows": len(parent_rows),
        "C42_kraft_one_rows": len(parent_rows),
        "C53_projection_rows": len(projections),
        "C53_head_object_sha256": C53_HEAD_OBJECT,
        "C53_audit_object_sha256": C53_AUDIT_OBJECT,
        "effective_checkpoint_object_sha256": C53_CHECKPOINT,
    }


def reconstruct(
        leaf_raw: bytes, c55b_cells: list[dict[str, Any]],
        c78l_cells: list[dict[str, Any]], c78l_pairs: list[dict[str, Any]],
        c78s_projection: list[dict[str, Any]], c78s_pairs: list[dict[str, Any]],
        c42_rows: list[dict[str, Any]], c53_projections: list[dict[str, Any]],
        ) -> tuple[dict[str, Any], dict[str, str]]:
    leaf_object = json.loads(leaf_raw.decode("utf-8"))
    verify_object(leaf_object, "C55A leaf", C55A_LEAF_OBJECT)
    leaves = leaf_object.get("leaves")
    if not isinstance(leaves, list) or len(leaves) != UNIVERSE:
        fail("C55A leaf count")
    leaf_by_cell: dict[str, dict[str, Any]] = {}
    unresolved: set[str] = set()
    baseline: set[str] = set()
    for ordinal, leaf in enumerate(leaves):
        verify_row(leaf, "C55A leaf")
        if leaf.get("leaf_ordinal") != ordinal or leaf.get("cell_id") in leaf_by_cell:
            fail("C55A leaf order/identity")
        terminal = leaf.get("terminal_disposition")
        reason = leaf.get("unresolved_reason")
        if not ((terminal in TERMINALS and reason is None) or
                (terminal is None and isinstance(reason, str) and bool(reason))):
            fail("C55A leaf XOR")
        leaf_by_cell[leaf["cell_id"]] = leaf
        (unresolved if terminal is None else baseline).add(leaf["cell_id"])
    if len(baseline) != BASELINE or len(unresolved) != OVERLAY_COUNT:
        fail("C55A baseline/overlay census")

    if len(c55b_cells) != 1_724:
        fail("C55B cell count")
    c55b: dict[str, dict[str, Any]] = {}
    pairs: dict[int, list[dict[str, Any]]] = defaultdict(list)
    c55b_unresolved: set[str] = set()
    for row in c55b_cells:
        if row.get("cell_id") in c55b or row.get("cell_id") not in leaf_by_cell:
            fail("C55B cell identity")
        c55b[row["cell_id"]] = row
        pair = row.get("pair_index")
        pairs[pair].append(row)
        if row.get("current_effective_disposition") == "UNRESOLVED_R1648_CONTINUATION":
            c55b_unresolved.add(row["cell_id"])
        if row.get("current_effective_disposition") not in {"EARLIEST_PREFIX_EXCLUDED", "UNRESOLVED_R1648_CONTINUATION"}:
            fail("C55B disposition")
    if c55b_unresolved != unresolved or set(pairs) != set(range(PAIR_COUNT)) or not all(len(v) == 2 for v in pairs.values()):
        fail("C55B unresolved/pairs")
    for rows in pairs.values():
        if rows[0].get("reflection_partner_cell_id") != rows[1].get("cell_id") or rows[1].get("reflection_partner_cell_id") != rows[0].get("cell_id"):
            fail("C55B reflection reciprocity")

    large = {row["cell_id"]: row for row in c78l_cells}
    singleton = {row["cell_id"]: row for row in c78s_projection}
    large_pair = {row["pair_index"]: row for row in c78l_pairs}
    singleton_pair = {row["pair_index"]: row for row in c78s_pairs}
    large_set, singleton_set = set(large), set(singleton)
    if (len(large_set) != LARGE_COUNT or len(singleton_set) != SINGLETON_COUNT or
            large_set & singleton_set or large_set | singleton_set != unresolved or
            len(large_pair) != LARGE_PAIRS or len(singleton_pair) != SINGLETON_PAIRS):
        fail("C78 overlay partition")
    for row in c78l_cells:
        if row.get("unresolved_count") != 0 or row.get("public_cell_disposition") not in LARGE_MAP:
            fail("C78L semantic row")
    for row in c78l_pairs:
        if not isinstance(row.get("prefix_Kraft"), dict) or row["prefix_Kraft"].get("prefix_free") is not True or row.get("unresolved_count") != 0:
            fail("C78L pair semantic row")
    for row in c78s_projection:
        if row.get("terminal_enum") not in SINGLETON_MAP or row.get("global_projection_installed") is not False or row.get("candidate_is_authority") is not False:
            fail("C78S semantic row")
    for row in c78s_pairs:
        if row.get("parent_Kraft") != "1" or row.get("parent_prefix_free") is not True:
            fail("C78S pair semantic row")

    overlay_rows: list[dict[str, Any]] = []
    overlay_by_cell: dict[str, dict[str, Any]] = {}
    for cell_id in sorted(unresolved, key=lambda item: leaf_by_cell[item]["leaf_ordinal"]):
        leaf = leaf_by_cell[cell_id]
        structure = c55b[cell_id]
        if cell_id in large:
            authority_row = large[cell_id]
            enum = authority_row["public_cell_disposition"]
            terminal, rule = LARGE_MAP[enum]
            if authority_row.get("owner_history_glue_two_sides_incidence_closed") is not True or authority_row.get("prefix_Kraft", {}).get("prefix_free") is not True:
                fail("C78L closure row")
            authority = "C78L_VERIFIED_FINAL_SURFACE"
        else:
            authority_row = singleton[cell_id]
            enum = authority_row["terminal_enum"]
            terminal, rule = SINGLETON_MAP[enum]
            pair = singleton_pair[structure["pair_index"]]
            if pair.get("parent_prefix_free") is not True or pair.get("parent_Kraft") != "1":
                fail("C78S Kraft row")
            authority = "C78S_VERIFIED_FINAL_SURFACE"
        row = close_row({
            "schema": "cm2.round306c79g.true-global-no-producer-consumer.v15.overlay-row",
            "overlay_ordinal": len(overlay_rows),
            "leaf_ordinal": leaf["leaf_ordinal"],
            "cell_id": cell_id,
            "C55A_leaf_row_sha256": leaf["row_sha256"],
            "C55B_cell_row_sha256": structure["row_sha256"],
            "pair_index": structure["pair_index"],
            "component_index": structure["component_index"],
            "component_id": structure["component_id"],
            "reflection_partner_cell_id": structure["reflection_partner_cell_id"],
            "previous_terminal_disposition": None,
            "previous_unresolved_reason": leaf["unresolved_reason"],
            "terminal_authority": authority,
            "terminal_authority_row_sha256": authority_row["row_sha256"],
            "authority_input_enum": enum,
            "mapping_rule": rule,
            "terminal_disposition": terminal,
            "overlay_sets_disjoint_and_exact": True,
            "installed_atomically_only_by_C79g_completion": True,
            "row_is_individually_creditable": False,
            "closure": dict(CLOSURE),
        })
        overlay_rows.append(row)
        overlay_by_cell[cell_id] = row

    successor_rows: list[dict[str, Any]] = []
    successor_by_cell: dict[str, dict[str, Any]] = {}
    census: Counter[str] = Counter()
    retained = 0
    for leaf in leaves:
        overlay = overlay_by_cell.get(leaf["cell_id"])
        if overlay is None:
            terminal = leaf["terminal_disposition"]
            mode = "C72G_BASELINE_RETAINED"
            authority = "C55A_PREEXISTING_TERMINAL_RETAINED_UNDER_C72G_STRUCTURAL_CLOSURE"
            authority_row_sha = leaf["row_sha256"]
            overlay_sha = None
            preserved = True
            retained += 1
        else:
            terminal = overlay["terminal_disposition"]
            mode = "C79G_OVERLAY_REPLACEMENT"
            authority = overlay["terminal_authority"]
            authority_row_sha = overlay["terminal_authority_row_sha256"]
            overlay_sha = overlay["row_sha256"]
            preserved = False
        if terminal not in TERMINALS:
            fail("successor terminal")
        row = close_row({
            "schema": "cm2.round306c79g.true-global-no-producer-consumer.v15.full-successor-row",
            "leaf_ordinal": leaf["leaf_ordinal"],
            "cell_id": leaf["cell_id"],
            "C55A_leaf_row_sha256": leaf["row_sha256"],
            "origin_key": leaf["origin_key"],
            "physical_chart": leaf["physical_chart"],
            "exact_box": leaf["exact_box"],
            "source_cell_row_sha256": leaf["source_cell_row_sha256"],
            "component_ref": leaf["component_ref"],
            "reflection_pair_ref": leaf["reflection_pair_ref"],
            "previous_terminal_disposition": leaf["terminal_disposition"],
            "previous_unresolved_reason": leaf["unresolved_reason"],
            "successor_terminal_disposition": terminal,
            "successor_unresolved_reason": None,
            "lineage_mode": mode,
            "terminal_authority": authority,
            "terminal_authority_row_sha256": authority_row_sha,
            "overlay_row_sha256": overlay_sha,
            "baseline_terminal_preserved_exactly": preserved,
            "candidate_atomic_install_only": True,
        })
        successor_rows.append(row)
        successor_by_cell[leaf["cell_id"]] = row
        census[terminal] += 1
    if retained != BASELINE or len(successor_rows) != UNIVERSE:
        fail("successor census")

    c42_by_pair = {row["pair_index"]: row for row in c42_rows}
    c53_by_pair = {row["pair_index"]: row for row in c53_projections}
    parent_rows: list[dict[str, Any]] = []
    modes: Counter[str] = Counter()
    for pair_index in sorted(pairs):
        structural = pairs[pair_index]
        roles = {leaf_by_cell[row["cell_id"]]["component_ref"]["cell_role"]: row for row in structural}
        if set(roles) != {"REPRESENTATIVE", "REFLECTED"}:
            fail("parent roles")
        representative, reflected = roles["REPRESENTATIVE"], roles["REFLECTED"]
        ids = {representative["cell_id"], reflected["cell_id"]}
        evidence_authority = "C42_INSTALLED_PARENT_CONSERVATION_VIA_C53_C55B_JOIN"
        if ids <= baseline:
            mode = "C72G_BASELINE_RETAINED"
            authority = "C55A_PREEXISTING_TERMINALS_WITH_C72G_STRUCTURAL_CLOSURE"
            authority_sha = leaf_by_cell[representative["cell_id"]]["row_sha256"]
            if not all(row.get("whole_pair_terminal_after_C53") is True for row in structural):
                fail("baseline pair terminal")
        elif ids <= large_set:
            mode = "C78L_OVERLAY"
            authority = "C78L_VERIFIED_FINAL_SURFACE"
            pair = large_pair[pair_index]
            authority_sha = pair["row_sha256"]
            if pair.get("prefix_Kraft", {}).get("prefix_free") is not True or pair.get("unresolved_count") != 0:
                fail("large pair closure")
        else:
            if not ids <= singleton_set:
                fail("mixed pair")
            mode = "C78S_OVERLAY"
            authority = "C78S_VERIFIED_FINAL_SURFACE"
            pair = singleton_pair[pair_index]
            authority_sha = pair["row_sha256"]
            if pair.get("parent_prefix_free") is not True or pair.get("parent_Kraft") != "1":
                fail("singleton pair closure")
        components = sorted({row["component_index"] for row in structural})
        if len(components) != 2:
            fail("cross-component reflection")
        dispositions = Counter(successor_by_cell[cell]["successor_terminal_disposition"] for cell in ids)
        parent_rows.append(close_row({
            "schema": "cm2.round306c79g.true-global-no-producer-consumer.v15.reflection-parent-closure-row",
            "parent_ordinal": len(parent_rows),
            "pair_index": pair_index,
            "representative_cell_id": representative["cell_id"],
            "reflected_cell_id": reflected["cell_id"],
            "representative_C55B_row_sha256": representative["row_sha256"],
            "reflected_C55B_row_sha256": reflected["row_sha256"],
            "representative_successor_row_sha256": successor_by_cell[representative["cell_id"]]["row_sha256"],
            "reflected_successor_row_sha256": successor_by_cell[reflected["cell_id"]]["row_sha256"],
            "component_indices": components,
            "parent_lineage_mode": mode,
            "terminal_authority": authority,
            "parent_authority_row_sha256": authority_sha,
            "terminal_disposition_census": dict(sorted(dispositions.items())),
            "reciprocal_reflection_partner_identity_closed": True,
            "owner_history_glue_two_sides_incidence_closed": True,
            "prefix_Kraft": {
                "evidence_authority": evidence_authority,
                "C42_parent_row_sha256": c42_by_pair[pair_index]["row_sha256"],
                "C53_parent_projection_object_sha256": c53_by_pair[pair_index]["projection_object_sha256"],
                "C55B_crosswalk_two_side_row_sha256s": sorted(row["row_sha256"] for row in structural),
                "C42_parent_Kraft_conservation": "1",
                "C72_boolean_used_as_authority": False,
                "prefix_free": True,
                "exact_parent_closure": True,
                "physical_reflection_duplicate_credit": 0,
            },
            "unresolved_count": 0,
        }))
        modes[mode] += 1
    if modes != Counter({"C72G_BASELINE_RETAINED": BASELINE_PAIRS, "C78L_OVERLAY": LARGE_PAIRS, "C78S_OVERLAY": SINGLETON_PAIRS}):
        fail("parent mode census")
    return {
        "overlay": overlay_rows,
        "successor": successor_rows,
        "parents": parent_rows,
        "census": {key: census.get(key, 0) for key in sorted(TERMINALS)},
        "modes": dict(sorted(modes.items())),
    }, {
        "overlay": sha_bytes(b"".join(canonical(x) + b"\n" for x in overlay_rows)),
        "successor": sha_bytes(b"".join(canonical(x) + b"\n" for x in successor_rows)),
        "parents": sha_bytes(b"".join(canonical(x) + b"\n" for x in parent_rows)),
    }


def run_precompute() -> dict[str, Any]:
    # Fixed geometry / crosswalk inputs.
    leaf_obj, leaf_raw, _ = read_json(C55A_LEAF, C55A_LEAF_SHA, 0o444)
    verify_object(leaf_obj, "C55A leaf", C55A_LEAF_OBJECT)
    c55b_cells, _, _ = read_gzip_rows(C55B_CELLS, C55B_CELLS_SHA, 0o664, "C55B cells")
    # Full dual surfaces are validated before using their two semantic ledgers.
    l_a, l_b, l_identity = dual_surface(C78L_A, C78L_B, C78L_NAMES, C78L_PINS, 0o755, "C78L")
    s_meta = validate_c78_metadata()
    # The C78L verifier is external to the A/B directory; its status is checked
    # here only as a data assertion, never used as an authority/credit signal.
    lv_boundary = s_meta["C78L_verification_branch_boundary"]
    if lv_boundary.get("branch_unresolved") != 0 or lv_boundary.get("public_global_unresolved_after_branch") != 24 or lv_boundary.get("public_global_unresolved_zero") is not False:
        fail("C78L branch boundary")
    # C78S verification was parsed only after secure O_NOFOLLOW/hash checks in
    # validate_c78_metadata; reuse that immutable parsed boundary rather than
    # reopening the path through an unchecked read_text() call.
    sv_boundary = s_meta["C78S_verification_branch_boundary"]
    if sv_boundary.get("current_public_global_unresolved") != 1_148 or sv_boundary.get("public_global_unresolved_after_branch") != 1_124:
        fail("C78S branch boundary")
    # Extract only the semantic ledgers after the complete surfaces have been
    # hash/inode checked.
    l_cells, _, _ = read_gzip_rows(C78L_A / C78L_NAMES["cells"], C78L_PINS["cells"], 0o444, "C78L cells")
    l_pairs, _, _ = read_gzip_rows(C78L_A / C78L_NAMES["pairs"], C78L_PINS["pairs"], 0o444, "C78L pairs")
    s_projection, _, _ = read_gzip_rows(C78S_A / C78S_NAMES["projection"], C78S_PINS["projection"], 0o444, "C78S projection")
    s_pairs, _, _ = read_gzip_rows(C78S_A / C78S_NAMES["pairs"], C78S_PINS["pairs"], 0o444, "C78S pairs")
    c42_rows, c53_rows, c53_meta = validate_c53()
    state, digests = reconstruct(leaf_raw, c55b_cells, l_cells, l_pairs, s_projection, s_pairs, c42_rows, c53_rows)
    return {
        "schema": "cm2.c79g.v16r2.global-consumer-precompute.v1",
        "status": "PASS_READ_ONLY_IN_MEMORY_RECONSTRUCTION__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
        "input_validation": {
            "O_NOFOLLOW": True,
            "stable_fd_hash_and_identity": True,
            "C55A_leaf_sha256": C55A_LEAF_SHA,
            "C55B_cells_sha256": C55B_CELLS_SHA,
            "C78L_dual_bytes_and_distinct_inodes": l_identity,
            "C78S_dual_bytes_and_distinct_inodes": s_meta["C78S_dual_identity"],
            "C53_checkpoint": c53_meta,
        },
        "reconstruction": {
            "overlay_rows": len(state["overlay"]),
            "successor_rows": len(state["successor"]),
            "parent_rows": len(state["parents"]),
            "public_unresolved_after_reconstruction": 0,
            "all_parent_unresolved_count_zero": all(row["unresolved_count"] == 0 for row in state["parents"]),
            "census": state["census"],
            "modes": state["modes"],
        },
        "canonical_line_sequence_sha256": digests,
        "credit": {
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "D02_started": False,
            "runtime_authorized": False,
            "canonical_pointer_written": False,
        },
        "writes": {
            "deliverables": False,
            "runtime": False,
            "manifest": False,
            "outer": False,
            "credit": False,
        },
    }


def run_seed_child(seed: int) -> dict[str, Any]:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = str(seed)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, "-I", "-B", "-S", str(Path(__file__).resolve()), "--digest-only"]
    completed = subprocess.run(command, cwd=str(ROOT), env=env, text=True,
                               capture_output=True, check=False)
    if completed.returncode != 0:
        fail("seed child failed:" + completed.stderr[-400:])
    try:
        value = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise AuditError("seed child did not return JSON") from exc
    if value.get("status") != "PASS_READ_ONLY_DIGEST_ONLY":
        fail("seed child status")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digest-only", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        report = run_precompute()
        if args.digest_only:
            print(json.dumps({
                "status": "PASS_READ_ONLY_DIGEST_ONLY",
                "counts": report["reconstruction"],
                "digests": report["canonical_line_sequence_sha256"],
            }, sort_keys=True, ensure_ascii=True))
            return 0
        child_a = run_seed_child(1)
        child_b = run_seed_child(99991)
        expected = report["canonical_line_sequence_sha256"]
        seed_invariant = (
            child_a.get("digests") == expected and
            child_b.get("digests") == expected and
            child_a.get("counts", {}).get("overlay_rows") == OVERLAY_COUNT and
            child_a.get("counts", {}).get("successor_rows") == UNIVERSE and
            child_a.get("counts", {}).get("parent_rows") == PAIR_COUNT and
            child_b.get("counts", {}).get("overlay_rows") == OVERLAY_COUNT and
            child_b.get("counts", {}).get("successor_rows") == UNIVERSE and
            child_b.get("counts", {}).get("parent_rows") == PAIR_COUNT
        )
        if not seed_invariant:
            fail("PYTHONHASHSEED invariance")
        report["seed_invariance"] = {
            "seeds": [1, 99991],
            "pass": True,
            "child_digests": {"1": child_a["digests"], "99991": child_b["digests"]},
        }
        print(json.dumps(report, sort_keys=True, ensure_ascii=True))
        return 0
    except (AuditError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({
            "schema": "cm2.c79g.v16r2.global-consumer-precompute.v1",
            "status": "FAIL_CLOSED_READ_ONLY_PRECOMPUTE",
            "error": type(exc).__name__ + ": " + str(exc),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "writes": False,
        }, sort_keys=True, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
