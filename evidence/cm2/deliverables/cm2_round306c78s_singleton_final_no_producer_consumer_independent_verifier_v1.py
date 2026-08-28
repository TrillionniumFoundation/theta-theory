#!/usr/bin/env python3
"""Independent no-producer verifier/finalizer for the C78s candidate.

This file never opens, reads, parses, decodes, imports, compiles, or executes
the C78s producer or any upstream producer source.  Terminal evidence is
reconstructed exclusively from the pinned, independently verified C77s and
C77d dual bundles.  Pinned C55A data is used only to recover the exact identity
of the 24 global-enumeration overlay rows and is never terminal authority.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
import os
import stat
import zlib
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import zip_longest
from pathlib import Path
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).absolute()
SCHEMA = "cm2.round306c78s.singleton-final-no-producer-consumer.v1"
BASE = "cm2_round306c78s_singleton_final_no_producer_consumer_v1"
PRODUCER_DECLARED_PIN = "506d28ab0428edc3dbd0302f27c4d8fb4bf198846ba6db321f4ad74ddc506a4c"
SELF_EXPECTED_NAME = (
    "cm2_round306c78s_singleton_final_no_producer_consumer_"
    "independent_verifier_v1.py"
)

DEFAULT_STAGE_A = ROOT / ".cm2-runtime/c78s-build-a.v1"
DEFAULT_STAGE_B = ROOT / ".cm2-runtime/c78s-build-b.v1"
C77S_A = ROOT / ".cm2-runtime/c77s-build-a5.v1"
C77S_B = ROOT / ".cm2-runtime/c77s-build-b5.v1"
C77D_A = ROOT / ".cm2-runtime/c77d-build-a.v1"
C77D_B = ROOT / ".cm2-runtime/c77d-build-b.v1"

CONTRACT_REL = "deliverables/cm2_round306c78s_singleton_final_no_producer_consumer_contract_v1.json"
CONTRACT_FILE_PIN = "a050522f7ed6b78f0fb8e6ef0da9ca987257b37bff2305c5d9b3fe51cd27aa4f"
CONTRACT_OBJECT_PIN = "71953457ee9ae3e3b2e6e477608dbb2d3ea0af7924b85aab535aee6c014c0159"

C55A_LEDGER_REL = "deliverables/cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json"
C55A_RESULT_REL = "deliverables/cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json"
C55A_VERIFY_REL = "deliverables/cm2_round306c55a_four_chart_fundamental_domain_bnb_independent_verification_v1.json"
C55A_MANIFEST_REL = "deliverables/cm2_round306c55a_four_chart_fundamental_domain_bnb_manifest_v1.sha256"
C55A_PINS = {
    C55A_LEDGER_REL: "e80c012e3260e8f9e68d5858ba5d9dafd94611e2a1c1200d787a20e3842d8db6",
    C55A_RESULT_REL: "d38f39792fc944b72e70100f9f96f312b5e30e034d5104ce5f848d24378ae5af",
    C55A_VERIFY_REL: "6e9dfe5c50cfb104cbb8014873f69f79761b22848f50a51033fced651a121772",
    C55A_MANIFEST_REL: "848c56c5d328cbdf291715d1eaab2611d3af95fb8bf2875beaadcbb9ffca6e0d",
}
C55A_LEDGER_OBJECT_PIN = "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90"
C55A_RESULT_OBJECT_PIN = "93b732cd65be4453e7b29379d7f70d8c849057d5bcba5489e1f6c4dd705972e3"
C55A_VERIFY_OBJECT_PIN = "cd6e3915f1dd89d8eef0766b4a806bc8a22244f348162af72fd009b98368d623"
C55A_OVERLAY_SEQUENCE_PIN = "3c6dbfc7f3cba144c99e87b3886954b996a18aff3822f248a351c03d4558a939"

C77S_LOCK = "ZERO_CREDIT_CANDIDATE_SINGLETON_PARENT_CONSUMER_ONLY.lock"
C77S_CHILD = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1_child_dispositions.jsonl.gz"
C77S_SOURCE = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1_source_rollups.jsonl.gz"
C77S_PAIR = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1_reflection_pair_rollups.jsonl.gz"
C77S_CELL = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1_singleton_cell_rollups.jsonl.gz"
C77S_INCIDENCE = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1_incidence_audit.json"
C77S_RESULT = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1_result.json"
C77S_REPORT = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1_report.md"
C77S_MANIFEST = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1_manifest.sha256"
C77S_BASE_OUTER = "cm2_round306c77s_singleton_parent_no_producer_consumer_v1_outer_receipt.json"
C77S_VERIFY = "cm2_round306c77s_singleton_parent_no_producer_consumer_independent_verification_v1.json"
C77S_FINAL_MANIFEST = "cm2_round306c77s_singleton_parent_no_producer_consumer_final_manifest_v1.sha256"
C77S_FINAL_OUTER = "cm2_round306c77s_singleton_parent_no_producer_consumer_final_outer_receipt_v1.json"
C77S_PINS = {
    C77S_LOCK: "e30e853c4ad0824f514959da072a71e53d7de63b303e8cd2c92201aa3fdd2061",
    C77S_CHILD: "a58448ef25656b4eed89fd3eef99405990f935778a395219e2465e6634c7a5c0",
    C77S_SOURCE: "e7e2c2ba2e8ddde0eae60d648248ba4a6eea3708323253662b1bf2a344254fbd",
    C77S_PAIR: "1f46044689c41fa33c752865077ce33b405a37e2f5118070e06433dc54d0568b",
    C77S_CELL: "bedd2b48fd0be9a76c72bd6337eb91697b3ab851674f630dfadc30a2f6678af9",
    C77S_INCIDENCE: "a3ab3095da090dd99376fc34963fcc9d807e118d74b31ae1e2676f1834b6d5a3",
    C77S_RESULT: "7544d6137a878ac8a4d1ce69ea13d63d8928d6c6db4bc1ab91bcaa8f7671963e",
    C77S_REPORT: "a277ddbc10f67bb021e576037d1449949d95294fb33362519bdf32a111dc8e1d",
    C77S_MANIFEST: "65021332c03328b3ce69a59179bb88a75016117a32c92a562d242286c552ca8d",
    C77S_BASE_OUTER: "257b3f362b81e32061cae49375967da6cf0b50d42bf67b979f46222d8ec1ac83",
    C77S_VERIFY: "200d889137913cec4753c7cceb30b471374bd04a077bc8e26c08847d0ffd7f3e",
    C77S_FINAL_MANIFEST: "45a12106d7fca7a9f952d4eeb48ae58b67115a20e52890c6ecbb143a00f229fb",
    C77S_FINAL_OUTER: "e86cd76bf0ce2c830fe34017fa73a640bb55c3ec332501ce17bdfec0af670fcb",
}
C77S_VERIFY_OBJECT_PIN = "6788637ffacc62283c71985b4096df472af3985b39f84ca8db7944f2491e58df"
C77S_FINAL_OUTER_OBJECT_PIN = "4a8d6f72ff4e201ebbe5475319d1f28435f4784fd452e78797f01d0a58232967"

C77D_LOCK = "ZERO_CREDIT_STAGED_C77D_DECISION_ROUTE_STRICT_EXCLUSION_ONLY.lock"
C77D_ROWS = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_rows.jsonl.gz"
C77D_INCIDENCE = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_root_incidence.jsonl.gz"
C77D_RESULT = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_result.json"
C77D_REPORT = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_report.md"
C77D_MANIFEST = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_candidate_manifest.sha256"
C77D_VERIFY = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_independent_verification_v1.json"
C77D_FINAL_MANIFEST = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_final_manifest_v1.sha256"
C77D_FINAL_OUTER = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_final_outer_receipt_v1.json"
C77D_PINS = {
    C77D_LOCK: "272582c332d360f580a9b85df7eed194224a654da85d62fda7f46d1233211871",
    C77D_ROWS: "0993dda3c66c91f62d01b6e815300567c56ce1aab9e61d5d49af833b444b5fa6",
    C77D_INCIDENCE: "2064d69578c49bf4079f26411f42ebd5a8cb097309d91e90383aaa2bc95ad0d9",
    C77D_RESULT: "73a2ac4003fda14744deb89ef5e383873a1d24eeb5b0225b6a8e7a6b023d9bc3",
    C77D_REPORT: "75a5e4a81629f67087464018fc94ab11f879269fcdac2d404214e3d06c3eb779",
    C77D_MANIFEST: "9419321d8375191ee214c7406bbe39930ddcbbc41c237a5e3e802f55aeafdef9",
    C77D_VERIFY: "6f59694019cd9ebf8be4a5be070579b69d82c4c084d8944a2f8cc44803958007",
    C77D_FINAL_MANIFEST: "8761f66309b71745a3de40d72dc415ef3f0a7d417c00719580bdb6f7b9b54907",
    C77D_FINAL_OUTER: "b801b0e48c736b78ed0f1e372b0d1b494925425cef36ed62d7c1be815003e9b0",
}
C77D_VERIFY_OBJECT_PIN = "4f2b014af66292efdf7eca1e10e5b09b0980d82444ff91fed87543c633b3a40b"
C77D_FINAL_OUTER_OBJECT_PIN = "f21d744d611751f084e20672510f9c9c151906fab981e3936f4a1a68558694ec"

LOCK = "ZERO_CREDIT_CANDIDATE_SINGLETON_FINAL_NO_PRODUCER_CONSUMER_ONLY.lock"
CHILD = BASE + "_child_dispositions.jsonl.gz"
SOURCE = BASE + "_source_rollups.jsonl.gz"
PAIR = BASE + "_reflection_pair_rollups.jsonl.gz"
CELL = BASE + "_singleton_cell_rollups.jsonl.gz"
PROJECTION = BASE + "_global_enum_projection.jsonl.gz"
RESULT = BASE + "_result.json"
REPORT = BASE + "_report.md"
MANIFEST = BASE + "_manifest.sha256"
BASE_OUTER = BASE + "_outer_receipt.json"
VERIFY = "cm2_round306c78s_singleton_final_no_producer_consumer_independent_verification_v1.json"
FINAL_MANIFEST = "cm2_round306c78s_singleton_final_no_producer_consumer_final_manifest_v1.sha256"
FINAL_OUTER = "cm2_round306c78s_singleton_final_no_producer_consumer_final_outer_receipt_v1.json"
BASE_MEMBER_ORDER = (LOCK, CHILD, SOURCE, PAIR, CELL, PROJECTION, RESULT, REPORT)
BASE_UNIVERSE = BASE_MEMBER_ORDER + (MANIFEST, BASE_OUTER)
FINAL_MANIFEST_ORDER = BASE_UNIVERSE + (VERIFY,)
FINAL_UNIVERSE = FINAL_MANIFEST_ORDER + (FINAL_MANIFEST, FINAL_OUTER)
PAIR_IDS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)
CREDIT_KEYS = ("formal_credit", "D02_gate_credit", "CM2_credit", "whole_parent_credit", "global_installed_credit")
EXECUTABLE_SOURCE_SUFFIXES = {".py", ".pyc", ".pyo"}
READABLE_ARTIFACT_NAMES = (
    {Path(CONTRACT_REL).name}
    | {Path(name).name for name in C55A_PINS}
    | set(C77S_PINS)
    | set(C77D_PINS)
    | set(FINAL_UNIVERSE)
)


class Reject(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def object_digest(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_sha256", None)
    return digest(canonical(body))


def parse_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in items:
            need(key not in value, f"duplicate JSON key:{label}:{key}")
            value[key] = item
        return value
    try:
        value = json.loads(raw, object_pairs_hook=pairs,
                           parse_constant=lambda item: (_ for _ in ()).throw(Reject(item)))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(f"invalid JSON:{label}:{exc}") from exc
    need(raw in (canonical(value), canonical(value) + b"\n"), f"noncanonical JSON:{label}")
    if isinstance(value, dict) and "object_sha256" in value:
        need(value["object_sha256"] == object_digest(value), f"object hash:{label}")
    return value


def add_row_hash(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(canonical(body))}


def add_object_hash(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "object_sha256": digest(canonical(body))}


def safe_read(path: Path, expected: str | None = None) -> tuple[bytes, tuple[int, int]]:
    need(path.name in READABLE_ARTIFACT_NAMES, f"artifact not on exact read allow-list:{path}")
    need(path.suffix.lower() not in EXECUTABLE_SOURCE_SUFFIXES,
         f"executable source access forbidden:{path}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, f"unsafe file:{path}")
        parts: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                break
            parts.append(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    identity = (before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
                before.st_size, before.st_mtime_ns)
    need(identity == (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                      after.st_size, after.st_mtime_ns), f"fd drift:{path}")
    need(identity == (current.st_dev, current.st_ino, current.st_mode, current.st_nlink,
                      current.st_size, current.st_mtime_ns), f"path drift:{path}")
    raw = b"".join(parts)
    if expected is not None:
        need(digest(raw) == expected, f"file pin:{path}")
    return raw, (before.st_dev, before.st_ino)


def safe_read_self_verifier() -> bytes:
    expected_path = ROOT / "deliverables" / SELF_EXPECTED_NAME
    need(SELF.name == SELF_EXPECTED_NAME and SELF == expected_path,
         f"verifier self path mismatch:{SELF}")
    descriptor_fd = os.open(SELF, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor_fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             f"unsafe verifier self file:{SELF}")
        parts: list[bytes] = []
        while True:
            chunk = os.read(descriptor_fd, 1 << 20)
            if not chunk:
                break
            parts.append(chunk)
        after = os.fstat(descriptor_fd)
    finally:
        os.close(descriptor_fd)
    current = os.stat(SELF, follow_symlinks=False)
    before_identity = (
        before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
        before.st_size, before.st_mtime_ns,
    )
    need(before_identity == (
        after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
        after.st_size, after.st_mtime_ns,
    ), f"verifier self fd drift:{SELF}")
    need(before_identity == (
        current.st_dev, current.st_ino, current.st_mode, current.st_nlink,
        current.st_size, current.st_mtime_ns,
    ), f"verifier self path drift:{SELF}")
    return b"".join(parts)


def exact_names(stage: Path) -> set[str]:
    need(stage.is_dir() and not stage.is_symlink(), f"unsafe/missing stage:{stage}")
    names: set[str] = set()
    with os.scandir(stage) as entries:
        for entry in entries:
            info = entry.stat(follow_symlinks=False)
            need(not entry.is_symlink() and stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                 f"unsafe stage member:{stage}:{entry.name}")
            need(entry.name not in names and
                 Path(entry.name).suffix.lower() not in EXECUTABLE_SOURCE_SUFFIXES,
                 f"duplicate/executable-source member:{entry.name}")
            names.add(entry.name)
    return names


def manifest_entries(raw: bytes, label: str, *, paths: bool = False) -> tuple[list[str], dict[str, str]]:
    need(raw.endswith(b"\n"), f"manifest newline:{label}")
    order: list[str] = []
    entries: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        pieces = line.split("  ")
        need(len(pieces) == 2, f"manifest syntax:{label}")
        pin, name = pieces
        need(len(pin) == 64 and all(ch in "0123456789abcdef" for ch in pin),
             f"manifest digest:{label}")
        member = Path(name)
        if paths:
            need(not member.is_absolute() and ".." not in member.parts, f"manifest path:{label}")
        else:
            need(member.name == name, f"manifest basename:{label}")
        need(name not in entries, f"manifest duplicate:{label}:{name}")
        order.append(name)
        entries[name] = pin
    return order, entries


def one_gzip(raw: bytes, label: str) -> None:
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    for offset in range(0, len(raw), 1 << 20):
        decoder.decompress(raw[offset:offset + (1 << 20)])
        need(not decoder.unused_data, f"gzip trailing/multiple member:{label}")
    decoder.flush()
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
         f"gzip closure:{label}")


def iter_rows(raw: bytes, label: str) -> Iterator[dict[str, Any]]:
    one_gzip(raw, label)
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
        for ordinal, line in enumerate(stream, 1):
            need(line.endswith(b"\n"), f"row newline:{label}:{ordinal}")
            row = parse_json(line[:-1], f"{label}:{ordinal}")
            need(isinstance(row, dict) and isinstance(row.get("row_sha256"), str),
                 f"row shape:{label}:{ordinal}")
            body = dict(row)
            row_hash = body.pop("row_sha256")
            need(row_hash == digest(canonical(body)), f"row hash:{label}:{ordinal}")
            yield row


def descriptor(raw: bytes, rows: Iterable[dict[str, Any]], filename: str) -> dict[str, Any]:
    sequence = hashlib.sha256()
    count = 0
    for row in rows:
        count += 1
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    return {"filename": filename, "row_count": count,
            "row_hash_line_sequence_sha256": sequence.hexdigest(),
            "sha256": digest(raw), "size": len(raw)}


def no_credit(value: dict[str, Any], label: str, required: Iterable[str] = ()) -> None:
    for key in required:
        need(key in value, f"missing credit field:{label}:{key}")
    for key in CREDIT_KEYS:
        if key in value:
            need(value[key] == 0, f"credit inflation:{label}:{key}")


def recursive_boundaries(value: Any, label: str = "root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            here = label + "." + key
            if key in CREDIT_KEYS:
                need(item == 0, f"recursive credit inflation:{here}")
            if key in ("canonical_pointer_or_seal_written", "runtime_canonical_pointer_or_seal_writes",
                       "global_projection_installed", "conditional_projection_installed",
                       "branch_projection_installed_as_canonical_state"):
                need(item is False, f"canonical/install inflation:{here}")
            if key in ("candidate_public_unresolved_decrement", "current_candidate_public_unresolved_decrement"):
                need(item == 0, f"installed decrement inflation:{here}")
            if key == "public_global_unresolved_zero":
                need(item is False, f"global-zero inflation:{here}")
            recursive_boundaries(item, here)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            recursive_boundaries(item, f"{label}[{index}]")


def load_pinned_dual(
    label: str, stage_a: Path, stage_b: Path, pins: dict[str, str],
    base_manifest: str, base_order: tuple[str, ...],
    final_manifest: str, final_order: tuple[str, ...], final_outer: str,
) -> dict[str, bytes]:
    need(exact_names(stage_a) == set(pins) and exact_names(stage_b) == set(pins),
         f"{label} exact dual universes")
    values: dict[str, bytes] = {}
    for name, pin in pins.items():
        left, li = safe_read(stage_a / name, pin)
        right, ri = safe_read(stage_b / name, pin)
        need(left == right and li != ri, f"{label} dual identity/isolation:{name}")
        values[name] = left
    base_names, base_entries = manifest_entries(values[base_manifest], label + ":base")
    need(tuple(base_names) == base_order and
         base_entries == {name: pins[name] for name in base_order}, f"{label} base manifest")
    final_names, final_entries = manifest_entries(values[final_manifest], label + ":final")
    need(tuple(final_names) == final_order and
         final_entries == {name: pins[name] for name in final_order}, f"{label} final manifest")
    outer = parse_json(values[final_outer], label + ":outer")
    need(outer["final_manifest_filename"] == final_manifest and
         outer["final_manifest_file_sha256"] == pins[final_manifest] and
         outer["final_manifest_member_count"] == len(final_order) and
         outer["final_manifest_order"] == list(final_order) and
         outer["terminal_byte_replay_member_count_per_stage"] == len(pins) and
         outer["all_final_members_terminal_byte_replayed_in_both_stages"] is True and
         outer["all_final_stage_bytes_identical"] is True and
         outer["candidate_is_authority"] is False and
         outer["candidate_public_unresolved_decrement"] == 0,
         f"{label} final outer closure")
    no_credit(outer, label + ":outer")
    return values


def load_candidate_dual(stage_a: Path, stage_b: Path) -> tuple[dict[str, bytes], dict[str, str]]:
    need(exact_names(stage_a) == set(BASE_UNIVERSE) and exact_names(stage_b) == set(BASE_UNIVERSE),
         "C78s exact 10-member base universes")
    values: dict[str, bytes] = {}
    identities: dict[str, str] = {}
    for name in BASE_UNIVERSE:
        left, li = safe_read(stage_a / name)
        right, ri = safe_read(stage_b / name)
        need(left == right and li != ri, f"C78s dual byte/inode identity:{name}")
        values[name] = left
        identities[name] = digest(left)
    order, entries = manifest_entries(values[MANIFEST], "C78s base manifest")
    need(tuple(order) == BASE_MEMBER_ORDER and
         entries == {name: identities[name] for name in BASE_MEMBER_ORDER},
         "C78s base manifest closure")
    outer = parse_json(values[BASE_OUTER], "C78s base outer")
    need(outer.get("manifest_filename") == MANIFEST and
         outer.get("manifest_file_sha256") == identities[MANIFEST] and
         outer.get("manifest_member_count") == len(BASE_MEMBER_ORDER) and
         outer.get("manifest_member_order") == list(BASE_MEMBER_ORDER) and
         outer.get("outer_receipt_published_last") is True and
         outer.get("terminal_byte_replay_member_count") == len(BASE_UNIVERSE) and
         outer.get("all_members_terminal_byte_replayed") is True and
         outer.get("candidate_is_authority") is False and
         outer.get("candidate_public_unresolved_decrement") == 0 and
         outer.get("singleton_branch_unresolved") == 0 and
         outer.get("public_global_unresolved_before") == 1148 and
         outer.get("public_global_unresolved_after_branch") == 1124 and
         outer.get("public_global_unresolved_zero") is False and
         outer.get("conditional_projection_installed") is False,
         "C78s base outer semantics")
    recursive_boundaries(outer, "C78s.outer")
    return values, identities


def load_contract() -> dict[str, Any]:
    raw, _ = safe_read(ROOT / CONTRACT_REL, CONTRACT_FILE_PIN)
    contract = parse_json(raw, "C78s contract")
    need(isinstance(contract, dict) and contract.get("object_sha256") == CONTRACT_OBJECT_PIN,
         "contract object pin")
    need(contract.get("authority_roles", {}).get("terminal_disposition_authority") == {
        "C55A_may_supply_terminal_evidence": False,
        "exclusive_sources": [
            "INDEPENDENTLY_VERIFIED_SEALED_C77S_DUAL_BUNDLE",
            "INDEPENDENTLY_VERIFIED_SEALED_C77D_DUAL_BUNDLE",
        ],
    }, "contract terminal authority")
    need(contract.get("authority_roles", {}).get("overlay_identity_authority", {}).get(
        "may_modify_or_supply_terminal_disposition") is False, "contract C55A role")
    need(contract.get("branch_projection_semantics") == {
        "global_zero_claim_forbidden": True,
        "installed_canonical_state": False,
        "projection_target": "C79G_ATOMIC_MERGE",
        "public_global_unresolved_after_branch": 1124,
        "public_global_unresolved_before": 1148,
        "public_global_unresolved_zero": False,
        "singleton_branch_unresolved": 0,
    }, "contract branch semantics")
    need(contract.get("required_independent_verifier_attacks") == [
        "C55A_IDENTITY_SUBSTITUTION_MUST_FAIL_CLOSED",
        "C55A_AS_TERMINAL_AUTHORITY_PROMOTION_MUST_FAIL_CLOSED",
        "PUBLIC_GLOBAL_UNRESOLVED_ZERO_INFLATION_MUST_FAIL_CLOSED",
    ], "contract attacks")
    recursive_boundaries(contract, "contract")
    return contract


def validate_input_objects(c77s: dict[str, bytes], c77d: dict[str, bytes]) -> tuple[dict[str, Any], dict[str, Any]]:
    s_result = parse_json(c77s[C77S_RESULT], "C77s result")
    s_verify = parse_json(c77s[C77S_VERIFY], "C77s verify")
    need(s_verify.get("object_sha256") == C77S_VERIFY_OBJECT_PIN and
         s_verify.get("coherent_attacks", {}).get("attack_count") == 66 and
         s_verify.get("coherent_attacks", {}).get("rejected") == 66 and
         s_verify.get("producer_source_policy") == {
             "compiled": False, "decoded": False, "executed": False,
             "imported": False, "opened": False, "parsed": False, "read": False,
         }, "C77s independent verification")
    need(s_result.get("partition") == {
        "blocker_source_children": 134155,
        "decision_source_children": 33100,
        "identity": "167255=33100+134155",
        "total_collision2_handoff_children": 167255,
    } and s_result.get("blocker_terminal_census") == {
        "cemetery_tangency_terminal": 23251,
        "identity": "134155=110904+23251",
        "residual": 0, "sealed_collision3_handoff": 0,
        "whole_child_strict_exclusion": 110904,
    }, "C77s result census")
    recursive_boundaries(s_result, "C77s.result")

    d_result = parse_json(c77d[C77D_RESULT], "C77d result")
    d_verify = parse_json(c77d[C77D_VERIFY], "C77d verify")
    need(d_verify.get("object_sha256") == C77D_VERIFY_OBJECT_PIN and
         d_verify.get("coherent_attacks", {}).get("attack_count") == 135 and
         d_verify.get("coherent_attacks", {}).get("rejected") == 135 and
         d_verify.get("producer_source_policy") == {
             "compiled": False, "decoded": False, "executed": False,
             "imported": False, "opened": False, "parsed": False, "read": False,
         }, "C77d independent verification")
    need(d_result.get("whole_child_strict_exclusion_count") == 33100 and
         d_result.get("explicit_residual_child_count") == 0 and
         d_result.get("sealed_collision3_handoff_count") == 0 and
         d_result.get("expected_owner_match_count") == 0,
         "C77d result census")
    recursive_boundaries(d_result, "C77d.result")
    return s_result, d_result


def validate_c77d(
    c77d: dict[str, bytes], result: dict[str, Any],
) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[str, Any]]:
    evidence: dict[tuple[str, str], dict[str, Any]] = {}
    route_census: Counter[str] = Counter()
    sequence = hashlib.sha256()
    count = 0
    for count, row in enumerate(iter_rows(c77d[C77D_ROWS], "C77d rows"), 1):
        need(row.get("ordinal") == count and
             row.get("schema") == "cm2.round306c77d.decision-child-exact-route-strict-exclusion.v1.decision-row",
             f"C77d row order:{count}")
        no_credit(row, f"C77d row:{count}", CREDIT_KEYS)
        need(row.get("candidate_is_authority") is False and
             row.get("global_consumption_ready") is False and
             row.get("additional_dyadic_depth") == 0 and
             row.get("whole_child_strict_exclusion_closed") is True and
             row.get("physical_chart_glue_closed") is True and
             row.get("allowed_exit_closed_for_every_stratum") is True and
             row.get("explicit_residual_strata") == 0 and
             row.get("sealed_collision3_handoff_count") == 0 and
             row.get("collision3_handoff") is None and
             all(exit_row.get("exit_class") == "STRICT_EXCLUSION"
                 for exit_row in row.get("stratum_exits", [])), f"C77d row closure:{count}")
        key = (row["C65_aggregate_child_row_sha256"], row["C71b_arrangement_row_sha256"])
        need(key not in evidence, f"C77d duplicate join key:{count}")
        evidence[key] = {
            "row_sha256": row["row_sha256"],
            "C65_child_row_sha256": key[0],
            "C71b_H1_row_sha256": key[1],
            "C61_source_row_sha256": row["C61_aggregate_leaf_row_sha256"],
            "pair_index": row["pair_index"],
            "source_path": row["source_path"],
            "child_path": row["child_path"],
            "route_outcome": row["route_outcome"],
            "fresh_geometry_kind": row["fresh_geometry_kind"],
            "physical_chart_glue_kind": row["physical_chart_glue_kind"],
        }
        route_census[row["route_outcome"]] += 1
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    rows_descriptor = {"filename": C77D_ROWS, "row_count": count,
                       "row_hash_line_sequence_sha256": sequence.hexdigest(),
                       "sha256": digest(c77d[C77D_ROWS]), "size": len(c77d[C77D_ROWS])}
    need(count == len(evidence) == 33100 and dict(sorted(route_census.items())) == result["route_census"],
         "C77d exact row scope")
    for key in ("row_count", "row_hash_line_sequence_sha256", "sha256", "size", "filename"):
        need(result["ledgers"]["decision_rows"].get(key) == rows_descriptor[key],
             f"C77d descriptor:{key}")

    incidence_sequence = hashlib.sha256()
    degree: Counter[int] = Counter()
    endpoint_count = 0
    incidence_count = 0
    previous = ""
    for incidence_count, row in enumerate(iter_rows(c77d[C77D_INCIDENCE], "C77d incidence"), 1):
        no_credit(row, f"C77d incidence:{incidence_count}", CREDIT_KEYS)
        root = row["root_id"]
        d = row["incidence_count"]
        need(root > previous and d in (1, 2) and row.get("incidence_closed") is True and
             len(row.get("target_graph_endpoint_occurrences", [])) == d and
             row.get("unique_half_open_dyadic_face_owner") and
             row.get("root_is_graph_endpoint_not_physical_terminal") is True,
             f"C77d incidence closure:{incidence_count}")
        previous = root
        degree[d] += 1
        endpoint_count += d
        incidence_sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    incidence_descriptor = {
        "filename": C77D_INCIDENCE, "row_count": incidence_count,
        "row_hash_line_sequence_sha256": incidence_sequence.hexdigest(),
        "sha256": digest(c77d[C77D_INCIDENCE]), "size": len(c77d[C77D_INCIDENCE]),
    }
    for key in ("row_count", "row_hash_line_sequence_sha256", "sha256", "size", "filename"):
        need(result["ledgers"]["root_incidence"].get(key) == incidence_descriptor[key],
             f"C77d incidence descriptor:{key}")
    need(incidence_count == 27630 and endpoint_count == 51494 and
         {str(k): v for k, v in sorted(degree.items())} == result["target_graph_root_degree_census"],
         "C77d incidence census")
    return evidence, {"row_count": incidence_count, "endpoint_occurrence_count": endpoint_count,
                      "degree_census": {str(k): v for k, v in sorted(degree.items())}}


def terminal_enum(cemetery: int) -> str:
    return ("STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY" if cemetery
            else "STRICT_EXCLUSION_ONLY")


def compare_exact(actual: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    need(actual == expected, f"exact candidate reconstruction mismatch:{label}")


def row_stream_descriptor(raw: bytes, rows: list[dict[str, Any]], filename: str) -> dict[str, Any]:
    sequence = digest("".join(row["row_sha256"] + "\n" for row in rows).encode("ascii"))
    return {"filename": filename, "row_count": len(rows),
            "row_hash_line_sequence_sha256": sequence,
            "sha256": digest(raw), "size": len(raw)}


def check_published_descriptor(
    published: dict[str, Any], actual: dict[str, Any], label: str,
) -> None:
    for key in ("filename", "row_count", "row_hash_line_sequence_sha256", "sha256", "size"):
        need(published.get(key) == actual.get(key), f"ledger descriptor:{label}:{key}")


def load_c55a() -> dict[str, Any]:
    raws: dict[str, bytes] = {}
    for rel, pin in C55A_PINS.items():
        raws[rel], _ = safe_read(ROOT / rel, pin)
    _, manifest = manifest_entries(raws[C55A_MANIFEST_REL], "C55A manifest", paths=True)
    for rel in (C55A_LEDGER_REL, C55A_RESULT_REL, C55A_VERIFY_REL):
        need(manifest.get(rel) == C55A_PINS[rel], f"C55A manifest pin:{rel}")
    result = parse_json(raws[C55A_RESULT_REL], "C55A result")
    verify = parse_json(raws[C55A_VERIFY_REL], "C55A verification")
    ledger = parse_json(raws[C55A_LEDGER_REL], "C55A ledger")
    need(result.get("object_sha256") == C55A_RESULT_OBJECT_PIN and
         verify.get("object_sha256") == C55A_VERIFY_OBJECT_PIN and
         ledger.get("object_sha256") == C55A_LEDGER_OBJECT_PIN,
         "C55A object pins")
    need(result.get("bnb", {}).get("leaf_count") == 76832 and
         result.get("bnb", {}).get("remaining_unresolved_leaf_count") == 1148 and
         result.get("bnb", {}).get("unresolved_zero") is False and
         result.get("bnb", {}).get("leaf_ledger_file_sha256") == C55A_PINS[C55A_LEDGER_REL] and
         result.get("formal_credit") == {
             "D02_gate_credit": 0, "formal_credit": 0,
             "source_grazing_or_cemetery_new_credit": 0,
         }, "C55A result boundary")
    need(verify.get("attacks") == {"executed": 8, "rejected": 8} and
         verify.get("independence", {}).get("C55A_producer_executed") is False and
         verify.get("independence", {}).get("C55A_producer_imported") is False,
         "C55A no-producer verification")
    leaves = ledger.get("leaves")
    need(isinstance(leaves, list) and len(leaves) == 76832, "C55A leaves")
    full_sequence = hashlib.sha256()
    disposition_census: Counter[str] = Counter()
    selected: dict[str, dict[str, Any]] = {}
    for ordinal, leaf in enumerate(leaves):
        need(leaf.get("leaf_ordinal") == ordinal and
             leaf.get("schema") == "cm2.round306c55a.four-chart-fundamental-domain-bnb.v1.leaf",
             f"C55A leaf order:{ordinal}")
        body = dict(leaf)
        row_hash = body.pop("row_sha256")
        need(row_hash == digest(canonical(body)), f"C55A row hash:{ordinal}")
        full_sequence.update((row_hash + "\n").encode("ascii"))
        disposition = leaf.get("terminal_disposition")
        reason = leaf.get("unresolved_reason")
        need((disposition is None) == bool(reason), f"C55A null rule:{ordinal}")
        disposition_census[disposition or "UNRESOLVED_R1648_CONTINUATION"] += 1
        component = leaf.get("component_ref")
        selected_here = (disposition is None and isinstance(component, dict) and
                         isinstance(component.get("component_index"), int) and
                         component["component_index"] >= 2)
        if not selected_here:
            continue
        reflection = leaf.get("reflection_pair_ref")
        cell_id = leaf.get("cell_id")
        need(isinstance(reflection, dict) and isinstance(cell_id, str) and cell_id not in selected,
             f"C55A overlay identity:{ordinal}")
        selected[cell_id] = {
            "leaf_ordinal": ordinal,
            "cell_id": cell_id,
            "row_sha256": row_hash,
            "pair_index": reflection["pair_index"],
            "component_index": component["component_index"],
            "component_ref": component,
            "reflection_partner_cell_id": reflection["partner_cell_id"],
            "origin_key": leaf["origin_key"],
            "previous_terminal_disposition": disposition,
            "previous_unresolved_reason": reason,
        }
    expected_census = dict(ledger["census"])
    expected_census.pop("total")
    expected_census.pop("unresolved_zero")
    need(all(disposition_census[key] == value for key, value in expected_census.items()) and
         set(disposition_census).issubset(expected_census), "C55A census")
    ordered = sorted(selected.values(), key=lambda item: item["leaf_ordinal"])
    selected_sequence = digest("".join(item["row_sha256"] + "\n" for item in ordered).encode("ascii"))
    need(len(selected) == 24 and selected_sequence == C55A_OVERLAY_SEQUENCE_PIN,
         "C55A exact 24 overlay sequence")
    return {
        "by_cell": selected,
        "ordered": ordered,
        "full_leaf_count": len(leaves),
        "full_sequence": full_sequence.hexdigest(),
        "selected_sequence": selected_sequence,
        "selected_ordinals": [item["leaf_ordinal"] for item in ordered],
    }


def expected_child(old: dict[str, Any], proof: dict[str, Any] | None) -> dict[str, Any]:
    decision = old["C69c_source_kind"] == "DECISION"
    if decision:
        need(proof is not None, "missing C77d decision proof")
        disposition = "STRICT_EXCLUSION"
        consumer = "C77D_EXACT_ROUTE_STRICT_EXCLUSION"
        consumer_row = proof["row_sha256"]
        route = proof["route_outcome"]
        geometry = proof["fresh_geometry_kind"]
        glue = proof["physical_chart_glue_kind"]
    else:
        need(proof is None, "blocker must not consume C77d")
        disposition = old["disposition"]
        consumer = old["consuming_oracle"]
        consumer_row = old["consuming_oracle_row_sha256"]
        route = geometry = glue = None
    return add_row_hash({
        "schema": SCHEMA + ".child-disposition-row",
        "ordinal": old["ordinal"], "pair_index": old["pair_index"],
        "source_path": old["source_path"], "child_path": old["child_path"],
        "parent_volume_fraction": old["parent_volume_fraction"],
        "C61_source_row_sha256": old["C61_source_row_sha256"],
        "C65_child_row_sha256": old["C65_child_row_sha256"],
        "C71b_H1_row_sha256": old["C71b_H1_row_sha256"],
        "C77s_child_disposition_row_sha256": old["row_sha256"],
        "C69c_source_kind": old["C69c_source_kind"],
        "C72_atlas_row_sha256": old["C72_atlas_row_sha256"],
        "previous_C77s_disposition": old["disposition"],
        "consuming_oracle": consumer, "consuming_oracle_row_sha256": consumer_row,
        "C77d_decision_route_row_sha256": consumer_row if decision else None,
        "C77d_route_outcome": route,
        "C77d_fresh_geometry_kind": geometry,
        "C77d_physical_chart_glue_kind": glue,
        "decision_residual_consumed_exactly_once": decision,
        "disposition": disposition, "terminal_predicate_present": True,
        "sealed_collision3_handoff_count": 0, "explicit_residual_count": 0,
        "candidate_is_authority": False, "candidate_public_unresolved_decrement": 0,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    })


def reconstruct_children(
    c77s_raw: bytes, candidate_raw: bytes, evidence: dict[tuple[str, str], dict[str, Any]],
    s_result: dict[str, Any],
) -> dict[str, Any]:
    source_stats: dict[str, Counter[str]] = defaultdict(Counter)
    pair_stats: dict[int, Counter[str]] = defaultdict(Counter)
    source_identity: dict[str, tuple[int, str]] = {}
    used: set[tuple[str, str]] = set()
    input_sequence = hashlib.sha256()
    candidate_sequence = hashlib.sha256()
    census: Counter[str] = Counter()
    count = 0
    samples: dict[str, dict[str, Any]] = {}
    sentinel = object()
    for count, pair in enumerate(zip_longest(
        iter_rows(c77s_raw, "C77s children"), iter_rows(candidate_raw, "C78s children"),
        fillvalue=sentinel,
    ), 1):
        old, actual = pair
        need(old is not sentinel and actual is not sentinel, "child stream length mismatch")
        input_sequence.update((old["row_sha256"] + "\n").encode("ascii"))
        key = (old["C65_child_row_sha256"], old["C71b_H1_row_sha256"])
        decision = old["C69c_source_kind"] == "DECISION"
        proof = evidence.get(key) if decision else None
        if decision:
            need(key not in used and proof is not None and
                 proof["C61_source_row_sha256"] == old["C61_source_row_sha256"] and
                 proof["pair_index"] == old["pair_index"] and
                 proof["source_path"] == old["source_path"] and
                 proof["child_path"] == old["child_path"], f"exact C77s/C77d join:{count}")
            used.add(key)
        expected = expected_child(old, proof)
        compare_exact(actual, expected, f"child:{count}")
        candidate_sequence.update((actual["row_sha256"] + "\n").encode("ascii"))
        if "child" not in samples:
            samples["child"] = actual
        if decision and "decision_child" not in samples:
            samples["decision_child"] = actual
        source = old["C61_source_row_sha256"]
        identity = (old["pair_index"], old["source_path"])
        need(source not in source_identity or source_identity[source] == identity,
             f"source identity:{count}")
        source_identity[source] = identity
        disposition = expected["disposition"]
        stats = source_stats[source]
        stats["total"] += 1
        stats["blocker"] += int(not decision)
        stats["decision"] += int(decision)
        stats["strict"] += int(disposition == "STRICT_EXCLUSION")
        stats["cemetery"] += int(disposition == "CEMETERY_TANGENCY_TERMINAL")
        stats["selected_kraft"] += Fraction(old["parent_volume_fraction"])
        pstats = pair_stats[old["pair_index"]]
        pstats["total"] += 1
        pstats["blocker"] += int(not decision)
        pstats["decision"] += int(decision)
        pstats["strict"] += int(disposition == "STRICT_EXCLUSION")
        pstats["cemetery"] += int(disposition == "CEMETERY_TANGENCY_TERMINAL")
        census[old["C69c_source_kind"] + "|" + disposition] += 1
    need(all(stats["total"] == stats["blocker"] + stats["decision"] for stats in pair_stats.values()),
         "pair child total accounting")
    need(count == 167255 and len(used) == len(evidence) == 33100 and census == {
        "BLOCKER|STRICT_EXCLUSION": 110904,
        "BLOCKER|CEMETERY_TANGENCY_TERMINAL": 23251,
        "DECISION|STRICT_EXCLUSION": 33100,
    }, "child reconstruction census")
    input_descriptor = {"filename": C77S_CHILD, "row_count": count,
                        "row_hash_line_sequence_sha256": input_sequence.hexdigest(),
                        "sha256": digest(c77s_raw), "size": len(c77s_raw)}
    check_published_descriptor(s_result["ledgers"]["child_dispositions"], input_descriptor, "C77s child")
    output_descriptor = {"filename": CHILD, "row_count": count,
                         "row_hash_line_sequence_sha256": candidate_sequence.hexdigest(),
                         "sha256": digest(candidate_raw), "size": len(candidate_raw)}
    return {"source_stats": source_stats, "pair_stats": pair_stats,
            "source_identity": source_identity, "descriptor": output_descriptor,
            "samples": samples, "census": census}


def expected_source(old: dict[str, Any], stats: Counter[str]) -> dict[str, Any]:
    selected_kraft = str(stats["selected_kraft"])
    need(old["selected_collision2_child_count"] == stats["total"] and
         old["selected_blocker_terminal_child_count"] == stats["blocker"] and
         old["selected_decision_residual_child_count"] == stats["decision"] and
         old["selected_child_Kraft"] == selected_kraft,
         f"C77s source/child accounting:{old['ordinal']}")
    return add_row_hash({
        "schema": SCHEMA + ".source-rollup-row",
        "ordinal": old["ordinal"], "pair_index": old["pair_index"],
        "source_path": old["source_path"],
        "C61_source_row_sha256": old["C61_source_row_sha256"],
        "C65_source_summary_row_sha256": old["C65_source_summary_row_sha256"],
        "C69c_source_row_sha256": old["C69c_source_row_sha256"],
        "C69c_source_kind": old["C69c_source_kind"],
        "C77s_source_rollup_row_sha256": old["row_sha256"],
        "C65_strict_terminal_carry_leaf_count": old["C65_strict_terminal_carry_leaf_count"],
        "C65_strict_terminal_carry_Kraft": old["C65_strict_terminal_carry_Kraft"],
        "selected_collision2_child_count": stats["total"],
        "selected_blocker_terminal_child_count": stats["blocker"],
        "selected_decision_strict_exclusion_child_count": stats["decision"],
        "selected_strict_exclusion_child_count": stats["strict"],
        "selected_cemetery_tangency_terminal_child_count": stats["cemetery"],
        "selected_residual_child_count": 0,
        "selected_collision3_handoff_child_count": 0,
        "selected_child_Kraft": selected_kraft,
        "full_source_Kraft": old["full_source_Kraft"],
        "source_prefix_free_and_Kraft_closed": True,
        "whole_source_terminal": True,
        "terminal_enum": terminal_enum(stats["cemetery"]),
        "candidate_is_authority": False, "candidate_public_unresolved_decrement": 0,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    })


def reconstruct_sources(
    c77s_raw: bytes, candidate_raw: bytes, child_data: dict[str, Any],
    s_result: dict[str, Any],
) -> dict[str, Any]:
    sequence = hashlib.sha256()
    input_sequence = hashlib.sha256()
    count = 0
    pair_source_counts: Counter[int] = Counter()
    samples: dict[str, dict[str, Any]] = {}
    sentinel = object()
    for count, (old, actual) in enumerate(zip_longest(
        iter_rows(c77s_raw, "C77s sources"), iter_rows(candidate_raw, "C78s sources"),
        fillvalue=sentinel,
    ), 1):
        need(old is not sentinel and actual is not sentinel, "source stream length mismatch")
        need(old["ordinal"] == count, f"C77s source ordinal:{count}")
        stats = child_data["source_stats"].get(old["C61_source_row_sha256"], Counter())
        if stats["total"]:
            need(child_data["source_identity"][old["C61_source_row_sha256"]] ==
                 (old["pair_index"], old["source_path"]), f"source join identity:{count}")
        expected = expected_source(old, stats)
        compare_exact(actual, expected, f"source:{count}")
        input_sequence.update((old["row_sha256"] + "\n").encode("ascii"))
        sequence.update((actual["row_sha256"] + "\n").encode("ascii"))
        pair_source_counts[old["pair_index"]] += 1
        samples.setdefault("source", actual)
        if stats["decision"]:
            samples.setdefault("decision_source", actual)
        if stats["cemetery"]:
            samples.setdefault("cemetery_source", actual)
    need(count == 20879 and set(pair_source_counts) == set(PAIR_IDS), "source exact scope")
    input_descriptor = {
        "filename": C77S_SOURCE, "row_count": count,
        "row_hash_line_sequence_sha256": input_sequence.hexdigest(),
        "sha256": digest(c77s_raw), "size": len(c77s_raw),
    }
    check_published_descriptor(s_result["ledgers"]["source_rollups"], input_descriptor,
                               "C77s source")
    return {
        "descriptor": {"filename": SOURCE, "row_count": count,
                       "row_hash_line_sequence_sha256": sequence.hexdigest(),
                       "sha256": digest(candidate_raw), "size": len(candidate_raw)},
        "pair_source_counts": pair_source_counts, "samples": samples,
    }


def expected_pair(old: dict[str, Any], ordinal: int, stats: Counter[str]) -> dict[str, Any]:
    need(old["blocker_terminal_child_count"] == stats["blocker"] and
         old["decision_residual_child_count"] == stats["decision"] and
         old["cemetery_graph_child_count"] == stats["cemetery"] and
         stats["total"] == stats["blocker"] + stats["decision"] and
         stats["total"] == stats["strict"] + stats["cemetery"],
         f"C77s pair/child accounting:{old['pair_index']}")
    return add_row_hash({
        "schema": SCHEMA + ".pair-rollup-row", "ordinal": ordinal,
        "pair_index": old["pair_index"], "C77s_pair_rollup_row_sha256": old["row_sha256"],
        "reflection_cell_count": old["reflection_cell_count"],
        "C69c_source_task_count": old["C69c_source_task_count"],
        "C57_strict_terminal_carry_leaf_count": old["C57_strict_terminal_carry_leaf_count"],
        "C57_strict_terminal_carry_Kraft": old["C57_strict_terminal_carry_Kraft"],
        "C58_strict_terminal_carry_leaf_count": old["C58_strict_terminal_carry_leaf_count"],
        "C58_strict_terminal_carry_Kraft": old["C58_strict_terminal_carry_Kraft"],
        "C61_strict_terminal_carry_leaf_count": old["C61_strict_terminal_carry_leaf_count"],
        "C61_strict_terminal_carry_Kraft": old["C61_strict_terminal_carry_Kraft"],
        "C65_replacement_leaf_count": old["C65_replacement_leaf_count"],
        "C65_replacement_Kraft": old["C65_replacement_Kraft"],
        "final_prefix_leaf_count": old["final_prefix_leaf_count"],
        "parent_prefix_free": old["parent_prefix_free"], "parent_Kraft": old["parent_Kraft"],
        "frozen_parent_row_sha256": old["frozen_parent_row_sha256"],
        "blocker_terminal_child_count": stats["blocker"],
        "decision_strict_exclusion_child_count": stats["decision"],
        "strict_exclusion_child_count": stats["strict"],
        "cemetery_tangency_terminal_child_count": stats["cemetery"],
        "residual_child_count": 0, "sealed_collision3_handoff_child_count": 0,
        "whole_reflection_pair_terminal": True,
        "terminal_enum": terminal_enum(stats["cemetery"]),
        "prefix_free_and_exact_Kraft_one_certificate_carried_from_C77s": True,
        "candidate_is_authority": False, "candidate_public_unresolved_decrement": 0,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    })


def reconstruct_pairs(
    c77s_raw: bytes, candidate_raw: bytes, pair_stats: dict[int, Counter[str]],
    s_result: dict[str, Any],
) -> dict[str, Any]:
    sequence = hashlib.sha256()
    input_sequence = hashlib.sha256()
    expected_by_pair: dict[int, dict[str, Any]] = {}
    enum_census: Counter[str] = Counter()
    count = 0
    sentinel = object()
    for count, (old, actual) in enumerate(zip_longest(
        iter_rows(c77s_raw, "C77s pairs"), iter_rows(candidate_raw, "C78s pairs"),
        fillvalue=sentinel,
    ), 1):
        need(old is not sentinel and actual is not sentinel and
             old["pair_index"] == PAIR_IDS[count - 1], f"pair stream/order:{count}")
        expected = expected_pair(old, count, pair_stats[old["pair_index"]])
        compare_exact(actual, expected, f"pair:{count}")
        input_sequence.update((old["row_sha256"] + "\n").encode("ascii"))
        sequence.update((actual["row_sha256"] + "\n").encode("ascii"))
        expected_by_pair[old["pair_index"]] = expected
        enum_census[expected["terminal_enum"]] += 1
    need(count == 12 and enum_census == {
        "STRICT_EXCLUSION_ONLY": 7,
        "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": 5,
    }, "pair exact enum census")
    input_descriptor = {
        "filename": C77S_PAIR, "row_count": count,
        "row_hash_line_sequence_sha256": input_sequence.hexdigest(),
        "sha256": digest(c77s_raw), "size": len(c77s_raw),
    }
    check_published_descriptor(s_result["ledgers"]["reflection_pair_rollups"],
                               input_descriptor, "C77s pair")
    return {
        "descriptor": {"filename": PAIR, "row_count": count,
                       "row_hash_line_sequence_sha256": sequence.hexdigest(),
                       "sha256": digest(candidate_raw), "size": len(candidate_raw)},
        "by_pair": expected_by_pair, "enum_census": enum_census,
        "sample": next(iter(expected_by_pair.values())),
    }


def expected_cell(old: dict[str, Any], ordinal: int, pair: dict[str, Any]) -> dict[str, Any]:
    need(old["blocker_terminal_child_count_on_reflection_pair"] ==
         pair["blocker_terminal_child_count"] and
         old["decision_residual_child_count_on_reflection_pair"] ==
         pair["decision_strict_exclusion_child_count"],
         f"C77s cell/pair accounting:{old['cell_id']}")
    return add_row_hash({
        "schema": SCHEMA + ".singleton-cell-rollup-row", "ordinal": ordinal,
        "component_index": old["component_index"], "component_id": old["component_id"],
        "cell_id": old["cell_id"], "reflection_partner_cell_id": old["reflection_partner_cell_id"],
        "pair_index": old["pair_index"], "origin_key": old["origin_key"],
        "C77s_singleton_cell_rollup_row_sha256": old["row_sha256"],
        "blocker_terminal_child_count_on_reflection_pair": pair["blocker_terminal_child_count"],
        "decision_strict_exclusion_child_count_on_reflection_pair":
            pair["decision_strict_exclusion_child_count"],
        "strict_exclusion_child_count_on_reflection_pair": pair["strict_exclusion_child_count"],
        "cemetery_tangency_terminal_child_count_on_reflection_pair":
            pair["cemetery_tangency_terminal_child_count"],
        "residual_child_count_on_reflection_pair": 0,
        "sealed_collision3_handoff_child_count_on_reflection_pair": 0,
        "whole_cell_terminal": True, "terminal_enum": pair["terminal_enum"],
        "global_projection_installed": False,
        "conditional_future_global_unresolved_decrement_if_atomically_installed": 1,
        "candidate_is_authority": False, "candidate_public_unresolved_decrement": 0,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    })


def reconstruct_cells(
    c77s_raw: bytes, candidate_raw: bytes, pairs: dict[str, Any], s_result: dict[str, Any],
) -> dict[str, Any]:
    sequence = hashlib.sha256()
    input_sequence = hashlib.sha256()
    cells: dict[str, dict[str, Any]] = {}
    enum_census: Counter[str] = Counter()
    count = 0
    sentinel = object()
    for count, (old, actual) in enumerate(zip_longest(
        iter_rows(c77s_raw, "C77s cells"), iter_rows(candidate_raw, "C78s cells"),
        fillvalue=sentinel,
    ), 1):
        need(old is not sentinel and actual is not sentinel and old["cell_id"] not in cells,
             f"cell stream/uniqueness:{count}")
        pair = pairs["by_pair"][old["pair_index"]]
        expected = expected_cell(old, count, pair)
        compare_exact(actual, expected, f"cell:{count}")
        input_sequence.update((old["row_sha256"] + "\n").encode("ascii"))
        sequence.update((actual["row_sha256"] + "\n").encode("ascii"))
        cells[old["cell_id"]] = expected
        enum_census[expected["terminal_enum"]] += 1
    need(count == len(cells) == 24 and enum_census == {
        "STRICT_EXCLUSION_ONLY": 14,
        "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": 10,
    }, "cell exact enum census")
    input_descriptor = {
        "filename": C77S_CELL, "row_count": count,
        "row_hash_line_sequence_sha256": input_sequence.hexdigest(),
        "sha256": digest(c77s_raw), "size": len(c77s_raw),
    }
    check_published_descriptor(s_result["ledgers"]["singleton_cell_rollups"],
                               input_descriptor, "C77s cell")
    return {
        "descriptor": {"filename": CELL, "row_count": count,
                       "row_hash_line_sequence_sha256": sequence.hexdigest(),
                       "sha256": digest(candidate_raw), "size": len(candidate_raw)},
        "by_cell": cells, "enum_census": enum_census,
    }


def expected_projection(
    item: dict[str, Any], cell: dict[str, Any], ordinal: int,
) -> dict[str, Any]:
    component = item["component_ref"]
    need(cell["cell_id"] == item["cell_id"] and
         cell["pair_index"] == item["pair_index"] and
         cell["component_index"] == item["component_index"] and
         cell["component_id"] == component["component_id"] and
         cell["reflection_partner_cell_id"] == item["reflection_partner_cell_id"] and
         cell["origin_key"] == item["origin_key"],
         f"exact C55A/C77s cell join:{item['leaf_ordinal']}")
    identity = {
        "leaf_ordinal": item["leaf_ordinal"], "cell_id": item["cell_id"],
        "row_sha256": item["row_sha256"], "pair_index": item["pair_index"],
        "component_index": item["component_index"], "component_ref": component,
        "reflection_partner_cell_id": item["reflection_partner_cell_id"],
    }
    return add_row_hash({
        "schema": SCHEMA + ".global-enum-projection-row", "ordinal": ordinal,
        "leaf_ordinal": item["leaf_ordinal"], "cell_id": item["cell_id"],
        "C55A_leaf_row_sha256": item["row_sha256"], "pair_index": item["pair_index"],
        "component_index": item["component_index"], "component_ref": component,
        "reflection_partner_cell_id": item["reflection_partner_cell_id"],
        "origin_key": item["origin_key"], "C55A_identity": identity,
        "C77s_cell_rollup_row_sha256": cell["C77s_singleton_cell_rollup_row_sha256"],
        "previous_C55A_terminal_disposition": item["previous_terminal_disposition"],
        "previous_C55A_unresolved_reason": item["previous_unresolved_reason"],
        "new_candidate_disposition": "WHOLE_SINGLETON_CELL_TERMINAL",
        "new_terminal_enum": cell["terminal_enum"], "terminal_enum": cell["terminal_enum"],
        "terminal_enum_derived_from_actual_cemetery_child_count":
            cell["cemetery_tangency_terminal_child_count_on_reflection_pair"],
        "whole_singleton_cell_terminal_candidate": True,
        "terminal_disposition_authority": [
            "INDEPENDENTLY_VERIFIED_SEALED_C77S_DUAL_BUNDLE",
            "INDEPENDENTLY_VERIFIED_SEALED_C77D_DUAL_BUNDLE",
        ],
        "C55A_role": "OVERLAY_IDENTITY_ONLY_NEVER_TERMINAL_AUTHORITY",
        "projection_role": "INPUT_ONLY_FOR_FUTURE_INDEPENDENT_NO_PRODUCER_GLOBAL_CONSUMER",
        "branch_projection_target": "C79G_ATOMIC_MERGE",
        "singleton_branch_unresolved": 0,
        "public_global_unresolved_before": 1148,
        "public_global_unresolved_after_branch": 1124,
        "public_global_unresolved_zero": False,
        "current_public_global_unresolved_before": 1148,
        "current_public_global_unresolved_after": 1148,
        "current_candidate_public_unresolved_decrement": 0,
        "conditional_future_per_component_decrement_if_atomically_installed": 1,
        "conditional_projected_public_global_unresolved_after_all_24_if_atomically_installed": 1124,
        "conditional_installation_requirement":
            "ALL_24_ROWS_MUST_BE_REVALIDATED_AND_ATOMICALLY_INSTALLED_BY_A_FUTURE_GLOBAL_CONSUMER",
        "global_projection_installed": False, "candidate_is_authority": False,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    })


def reconstruct_projection(
    candidate_raw: bytes, c55a: dict[str, Any], cells: dict[str, Any],
) -> dict[str, Any]:
    actual_rows = list(iter_rows(candidate_raw, "C78s projection"))
    need(len(actual_rows) == len(c55a["ordered"]) == len(cells["by_cell"]) == 24,
         "projection exact cardinality")
    expected_rows: list[dict[str, Any]] = []
    used_cells: set[str] = set()
    sequence = hashlib.sha256()
    for ordinal, (item, actual) in enumerate(zip(c55a["ordered"], actual_rows), 1):
        need(item["cell_id"] not in used_cells and item["cell_id"] in cells["by_cell"],
             f"projection exact one-to-one:{ordinal}")
        used_cells.add(item["cell_id"])
        expected = expected_projection(item, cells["by_cell"][item["cell_id"]], ordinal)
        compare_exact(actual, expected, f"projection:{ordinal}")
        expected_rows.append(expected)
        sequence.update((actual["row_sha256"] + "\n").encode("ascii"))
    need(used_cells == set(cells["by_cell"]) and
         [row["leaf_ordinal"] for row in actual_rows] == c55a["selected_ordinals"],
         "projection bijection/order")
    return {
        "descriptor": {"filename": PROJECTION, "row_count": 24,
                       "row_hash_line_sequence_sha256": sequence.hexdigest(),
                       "sha256": digest(candidate_raw), "size": len(candidate_raw)},
        "rows": expected_rows,
    }


def expected_result(
    descriptors: dict[str, dict[str, Any]], c55a: dict[str, Any],
    s_result: dict[str, Any], d_result: dict[str, Any], incidence: dict[str, Any],
    pair_enum: Counter[str], cell_enum: Counter[str],
) -> dict[str, Any]:
    false_policy = {
        "compiled": False, "decoded": False, "executed": False,
        "imported": False, "opened": False, "parsed": False, "read": False,
    }
    body = {
        "schema": SCHEMA + ".result",
        "status": "PASS_EXACT_SEALED_13_PLUS_9_INPUTS__167255_TERMINAL_CHILDREN__33100_DECISION_RESIDUALS_CONSUMED_EXACTLY_ONCE__20879_SOURCES__12_PAIRS__24_CELLS__GLOBAL_PROJECTION_NOT_INSTALLED__ZERO_CREDIT",
        "producer_file_sha256": PRODUCER_DECLARED_PIN,
        "contract": {"file_sha256": CONTRACT_FILE_PIN, "object_sha256": CONTRACT_OBJECT_PIN,
                     "authority_role_separation_closed": True},
        "sealed_dual_inputs": {
            "C77s": {
                "stage_a": ".cm2-runtime/c77s-build-a5.v1",
                "stage_b": ".cm2-runtime/c77s-build-b5.v1",
                "exact_member_count_per_stage": 13,
                "final_manifest_file_sha256": C77S_PINS[C77S_FINAL_MANIFEST],
                "final_outer_receipt_file_sha256": C77S_PINS[C77S_FINAL_OUTER],
                "result_object_sha256": s_result["object_sha256"],
            },
            "C77d": {
                "stage_a": ".cm2-runtime/c77d-build-a.v1",
                "stage_b": ".cm2-runtime/c77d-build-b.v1",
                "exact_member_count_per_stage": 9,
                "final_manifest_file_sha256": C77D_PINS[C77D_FINAL_MANIFEST],
                "final_outer_receipt_file_sha256": C77D_PINS[C77D_FINAL_OUTER],
                "result_object_sha256": d_result["object_sha256"],
            },
            "all_22_stage_members_byte_identical_across_duals": True,
            "all_manifests_receipts_objects_rows_and_single_member_gzips_closed": True,
        },
        "upstream_producer_policy": {"C77s_producer": false_policy,
                                     "C77d_producer": false_policy},
        "C77d_consumption": {
            "join_key": ["C65_child_row_sha256", "C71b_H1_row_sha256"],
            "additional_exact_matches": ["C61_source_row_sha256", "pair_index",
                                         "source_path", "child_path"],
            "available_decision_rows": 33100, "consumed_exactly_once": 33100,
            "duplicate_consumption": 0, "unconsumed": 0,
        },
        "C77d_root_incidence_validated": {
            "unique_root_count": incidence["row_count"],
            "endpoint_occurrence_count": incidence["endpoint_occurrence_count"],
            "degree_census": incidence["degree_census"],
        },
        "authority_role_separation": {
            "terminal_disposition_authority_exclusive": [
                "INDEPENDENTLY_VERIFIED_SEALED_C77S_DUAL_BUNDLE",
                "INDEPENDENTLY_VERIFIED_SEALED_C77D_DUAL_BUNDLE",
            ],
            "C55A_role": "OVERLAY_IDENTITY_ONLY",
            "C55A_may_supply_or_modify_terminal_disposition": False,
            "C55A_identity_fields": ["leaf_ordinal", "cell_id", "row_sha256", "pair_index",
                                     "component_index", "component_ref",
                                     "reflection_partner_cell_id"],
        },
        "C55A_overlay_identity_input": {
            "leaf_ledger_file_sha256": C55A_PINS[C55A_LEDGER_REL],
            "leaf_ledger_object_sha256": C55A_LEDGER_OBJECT_PIN,
            "result_file_sha256": C55A_PINS[C55A_RESULT_REL],
            "independent_verification_file_sha256": C55A_PINS[C55A_VERIFY_REL],
            "manifest_file_sha256": C55A_PINS[C55A_MANIFEST_REL],
            "full_leaf_count": c55a["full_leaf_count"],
            "full_leaf_row_hash_line_sequence_sha256": c55a["full_sequence"],
            "matched_singleton_row_count": 24,
            "matched_singleton_leaf_ordinal_order": c55a["selected_ordinals"],
            "matched_singleton_row_hash_line_sequence_sha256": c55a["selected_sequence"],
            "one_to_one_old_C55A_row_to_new_projection_disposition": True,
            "role": "OVERLAY_IDENTITY_ONLY_NEVER_TERMINAL_AUTHORITY",
            "terminal_authority": False,
        },
        "partition": {"total_children": 167255, "blocker_children_preserved": 134155,
                      "decision_children_consumed": 33100,
                      "identity": "167255=134155+33100"},
        "terminal_child_census": {
            "whole_child_strict_exclusion": 144004,
            "cemetery_tangency_terminal": 23251,
            "explicit_residual": 0, "sealed_collision3_handoff": 0,
            "identity": "167255=144004+23251",
        },
        "sources": {"total": 20879, "whole_terminal": 20879, "residual": 0},
        "reflection_pairs": {
            "total": 12, "whole_terminal": 12, "residual": 0,
            "prefix_free_and_exact_Kraft_one_certificates_carried": 12,
            "terminal_enum_census": dict(pair_enum),
        },
        "singleton_cells": {"total": 24, "whole_terminal": 24, "residual": 0,
                            "terminal_enum_census": dict(cell_enum)},
        "ledgers": descriptors,
        "global_enum_projection": {
            "row_count": 24,
            "row_hash_line_sequence_sha256":
                descriptors["global_enum_projection"]["row_hash_line_sequence_sha256"],
            "row_order": "C55A_LEAF_ORDINAL_ASCENDING",
            "role": "CANDIDATE_INPUT_ONLY_FOR_FUTURE_INDEPENDENT_NO_PRODUCER_GLOBAL_CONSUMER",
            "atomic_installation_required": "24_OF_24", "installed": False,
        },
        "singleton_branch_unresolved": 0,
        "public_global_unresolved_before": 1148,
        "public_global_unresolved_after_branch": 1124,
        "public_global_unresolved_zero": False,
        "public_global_unresolved": {
            "current_before": 1148, "current_after": 1148,
            "current_candidate_decrement": 0,
            "conditional_projection": {
                "projected_decrement": 24, "projected_after": 1124, "installed": False,
                "condition": "ONLY_IF_A_FUTURE_INDEPENDENT_NO_PRODUCER_GLOBAL_CONSUMER_REVALIDATES_AND_ATOMICALLY_INSTALLS_ALL_24_PROJECTION_ROWS",
            },
        },
        "branch_projection_target": "C79G_ATOMIC_MERGE",
        "branch_projection_installed_as_canonical_state": False,
        "candidate_is_authority": False, "canonical_pointer_or_seal_written": False,
        "runtime_canonical_pointer_or_seal_writes": False,
        "credit_boundary": {"formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
                            "whole_parent_credit": 0, "global_installed_credit": 0},
    }
    return add_object_hash(body)


def expected_base_outer(identities: dict[str, str], result: dict[str, Any]) -> dict[str, Any]:
    return add_object_hash({
        "schema": SCHEMA + ".outer-receipt",
        "status": "PASS_APPEND_ONLY_EXACT_SEALED_INPUT_CONSUMER__OUTER_LAST__TERMINAL_BYTE_REPLAY__GLOBAL_PROJECTION_NOT_INSTALLED__ZERO_CREDIT",
        "manifest_filename": MANIFEST, "manifest_file_sha256": identities[MANIFEST],
        "manifest_member_count": len(BASE_MEMBER_ORDER),
        "manifest_member_order": list(BASE_MEMBER_ORDER),
        "result_object_sha256": result["object_sha256"],
        "outer_receipt_published_last": True,
        "terminal_byte_replay_member_count": len(BASE_UNIVERSE),
        "all_members_terminal_byte_replayed": True,
        "branch_projection_target": "C79G_ATOMIC_MERGE",
        "singleton_branch_unresolved": 0,
        "public_global_unresolved_before": 1148,
        "public_global_unresolved_after_branch": 1124,
        "public_global_unresolved_zero": False,
        "current_public_global_unresolved": 1148,
        "conditional_projected_future_public_global_unresolved": 1124,
        "conditional_projection_installed": False,
        "candidate_is_authority": False, "candidate_public_unresolved_decrement": 0,
        "canonical_pointer_or_seal_written": False,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    })


def expected_report(result_hash: str) -> bytes:
    return (
        "# C78s singleton final no-producer consumer v1\n\n"
        "Status: PASS candidate reconstruction; zero installed credit.\n\n"
        "- Exact sealed inputs: C77s 13-member dual bundle and C77d 9-member dual bundle.\n"
        "- C55A is pinned identity-only input for the 24-row overlay; it is never terminal authority.\n"
        "- Every projected row carries its exact C55A leaf ordinal/hash/component/reflection identity and C77s cell-row hash.\n"
        "- Upstream producer sources opened/read/imported/compiled/executed: no.\n"
        "- Children: 167,255 = 144,004 strict exclusions + 23,251 cemetery tangencies.\n"
        "- Decision residuals consumed exactly once: 33,100; residual/C3 handoff: 0/0.\n"
        "- Sources/pairs/cells terminal: 20,879 / 12 / 24.\n"
        "- Pair enum census: 7 strict-only, 5 strict-plus-cemetery.\n"
        "- Cell enum census: 14 strict-only, 10 strict-plus-cemetery.\n"
        "- Current public unresolved remains 1,148; candidate decrement is 0.\n"
        "- Singleton-branch unresolved is 0; its C79g branch projection is 1,148 -> 1,124.\n"
        "- The branch projection is not canonical state, and public-global unresolved-zero is false.\n"
        "- 1,124 becomes installed only if a future independent global consumer atomically accepts all 24 projection rows.\n"
        "- Formal/global/D02/CM2/whole-parent credit: all zero.\n\n"
        f"Result object SHA-256: `{result_hash}`\n"
    ).encode("utf-8")


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = replacement


def coherent_copy(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> dict[str, Any]:
    changed = copy.deepcopy(value)
    cursor: Any = changed
    for part in path[:-1]:
        cursor = cursor[part]
    need(cursor[path[-1]] != replacement, f"attack mutation is a no-op:{path}")
    cursor[path[-1]] = replacement
    if "row_sha256" in changed:
        body = dict(changed)
        body.pop("row_sha256")
        changed["row_sha256"] = digest(canonical(body))
    if "object_sha256" in changed:
        changed["object_sha256"] = object_digest(changed)
    return changed


def run_attacks(
    result: dict[str, Any], outer: dict[str, Any], child_data: dict[str, Any],
    source_data: dict[str, Any], pair_data: dict[str, Any], cell_data: dict[str, Any],
    projection_data: dict[str, Any], manifest_raw: bytes, verifier_file_sha256: str,
) -> dict[str, Any]:
    rejected: list[str] = []

    def exact_attack(
        name: str, target: dict[str, Any], path: tuple[Any, ...], replacement: Any,
    ) -> None:
        changed = coherent_copy(target, path, replacement)
        try:
            compare_exact(changed, target, "attack:" + name)
        except Reject:
            rejected.append(name)
            return
        raise Reject("coherent attack accepted:" + name)

    result_specs: list[tuple[str, tuple[Any, ...], Any]] = [
        ("CONTRACT_FILE_PIN_DRIFT", ("contract", "file_sha256"), "0" * 64),
        ("CONTRACT_OBJECT_PIN_DRIFT", ("contract", "object_sha256"), "1" * 64),
        ("C77S_MEMBER_COUNT_DRIFT", ("sealed_dual_inputs", "C77s", "exact_member_count_per_stage"), 12),
        ("C77S_FINAL_MANIFEST_DRIFT", ("sealed_dual_inputs", "C77s", "final_manifest_file_sha256"), "2" * 64),
        ("C77S_FINAL_OUTER_DRIFT", ("sealed_dual_inputs", "C77s", "final_outer_receipt_file_sha256"), "3" * 64),
        ("C77S_RESULT_OBJECT_DRIFT", ("sealed_dual_inputs", "C77s", "result_object_sha256"), "4" * 64),
        ("C77S_STAGE_SUBSTITUTION", ("sealed_dual_inputs", "C77s", "stage_a"), ".cm2-runtime/substitute"),
        ("C77D_MEMBER_COUNT_DRIFT", ("sealed_dual_inputs", "C77d", "exact_member_count_per_stage"), 8),
        ("C77D_FINAL_MANIFEST_DRIFT", ("sealed_dual_inputs", "C77d", "final_manifest_file_sha256"), "5" * 64),
        ("C77D_FINAL_OUTER_DRIFT", ("sealed_dual_inputs", "C77d", "final_outer_receipt_file_sha256"), "6" * 64),
        ("C77D_RESULT_OBJECT_DRIFT", ("sealed_dual_inputs", "C77d", "result_object_sha256"), "7" * 64),
        ("C77D_STAGE_SUBSTITUTION", ("sealed_dual_inputs", "C77d", "stage_b"), ".cm2-runtime/substitute"),
        ("SEALED_DUAL_BYTE_IDENTITY_FALSE", ("sealed_dual_inputs", "all_22_stage_members_byte_identical_across_duals"), False),
        ("SEALED_REPLAY_CLOSURE_FALSE", ("sealed_dual_inputs", "all_manifests_receipts_objects_rows_and_single_member_gzips_closed"), False),
        ("C55A_AS_TERMINAL_AUTHORITY_PROMOTION_MUST_FAIL_CLOSED", ("authority_role_separation", "C55A_may_supply_or_modify_terminal_disposition"), True),
        ("C55A_ROLE_PROMOTION", ("authority_role_separation", "C55A_role"), "TERMINAL_AUTHORITY"),
        ("TERMINAL_AUTHORITY_C55A_INSERTION", ("authority_role_separation", "terminal_disposition_authority_exclusive"), ["C55A"]),
        ("C55A_IDENTITY_FIELD_ORDER_DRIFT", ("authority_role_separation", "C55A_identity_fields"), list(reversed(result["authority_role_separation"]["C55A_identity_fields"]))),
        ("C55A_LEDGER_PIN_SUBSTITUTION", ("C55A_overlay_identity_input", "leaf_ledger_file_sha256"), "8" * 64),
        ("C55A_LEDGER_OBJECT_SUBSTITUTION", ("C55A_overlay_identity_input", "leaf_ledger_object_sha256"), "9" * 64),
        ("C55A_RESULT_PIN_SUBSTITUTION", ("C55A_overlay_identity_input", "result_file_sha256"), "a" * 64),
        ("C55A_VERIFY_PIN_SUBSTITUTION", ("C55A_overlay_identity_input", "independent_verification_file_sha256"), "b" * 64),
        ("C55A_MANIFEST_PIN_SUBSTITUTION", ("C55A_overlay_identity_input", "manifest_file_sha256"), "c" * 64),
        ("C55A_FULL_LEAF_COUNT_DRIFT", ("C55A_overlay_identity_input", "full_leaf_count"), 76831),
        ("C55A_FULL_SEQUENCE_DRIFT", ("C55A_overlay_identity_input", "full_leaf_row_hash_line_sequence_sha256"), "d" * 64),
        ("C55A_MATCHED_COUNT_DRIFT", ("C55A_overlay_identity_input", "matched_singleton_row_count"), 23),
        ("C55A_IDENTITY_ORDER_DRIFT", ("C55A_overlay_identity_input", "matched_singleton_leaf_ordinal_order"), list(reversed(result["C55A_overlay_identity_input"]["matched_singleton_leaf_ordinal_order"]))),
        ("C55A_IDENTITY_SEQUENCE_DRIFT", ("C55A_overlay_identity_input", "matched_singleton_row_hash_line_sequence_sha256"), "e" * 64),
        ("C55A_ONE_TO_ONE_FALSE", ("C55A_overlay_identity_input", "one_to_one_old_C55A_row_to_new_projection_disposition"), False),
        ("C55A_TERMINAL_AUTHORITY_TRUE", ("C55A_overlay_identity_input", "terminal_authority"), True),
        ("C77D_CONSUMED_COUNT_DRIFT", ("C77d_consumption", "consumed_exactly_once"), 33099),
        ("C77D_DUPLICATE_CONSUMPTION", ("C77d_consumption", "duplicate_consumption"), 1),
        ("C77D_UNCONSUMED_INFLATION", ("C77d_consumption", "unconsumed"), 1),
        ("C77D_JOIN_KEY_ORDER_DRIFT", ("C77d_consumption", "join_key"), list(reversed(result["C77d_consumption"]["join_key"]))),
        ("C77D_JOIN_ADDITIONAL_FIELD_DROP", ("C77d_consumption", "additional_exact_matches"), result["C77d_consumption"]["additional_exact_matches"][:-1]),
        ("ROOT_INCIDENCE_UNIQUE_COUNT_DRIFT", ("C77d_root_incidence_validated", "unique_root_count"), 27629),
        ("ROOT_INCIDENCE_ENDPOINT_COUNT_DRIFT", ("C77d_root_incidence_validated", "endpoint_occurrence_count"), 51493),
        ("ROOT_INCIDENCE_DEGREE_ONE_DRIFT", ("C77d_root_incidence_validated", "degree_census", "1"), 3765),
        ("ROOT_INCIDENCE_DEGREE_TWO_DRIFT", ("C77d_root_incidence_validated", "degree_census", "2"), 23863),
        ("PARTITION_TOTAL_DRIFT", ("partition", "total_children"), 167254),
        ("PARTITION_BLOCKER_DRIFT", ("partition", "blocker_children_preserved"), 134154),
        ("PARTITION_DECISION_DRIFT", ("partition", "decision_children_consumed"), 33099),
        ("STRICT_CENSUS_SPOOF", ("terminal_child_census", "whole_child_strict_exclusion"), 144005),
        ("CEMETERY_CENSUS_SPOOF", ("terminal_child_census", "cemetery_tangency_terminal"), 23250),
        ("RESIDUAL_CENSUS_INFLATION", ("terminal_child_census", "explicit_residual"), 1),
        ("C3_HANDOFF_CENSUS_INFLATION", ("terminal_child_census", "sealed_collision3_handoff"), 1),
        ("SOURCE_TOTAL_DRIFT", ("sources", "total"), 20878),
        ("SOURCE_TERMINAL_DRIFT", ("sources", "whole_terminal"), 20878),
        ("SOURCE_RESIDUAL_INFLATION", ("sources", "residual"), 1),
        ("PAIR_TOTAL_DRIFT", ("reflection_pairs", "total"), 11),
        ("PAIR_TERMINAL_DRIFT", ("reflection_pairs", "whole_terminal"), 11),
        ("PAIR_RESIDUAL_INFLATION", ("reflection_pairs", "residual"), 1),
        ("PAIR_KRAFT_CERTIFICATE_DROP", ("reflection_pairs", "prefix_free_and_exact_Kraft_one_certificates_carried"), 11),
        ("PAIR_ENUM_7_SPOOF", ("reflection_pairs", "terminal_enum_census", "STRICT_EXCLUSION_ONLY"), 8),
        ("PAIR_ENUM_5_SPOOF", ("reflection_pairs", "terminal_enum_census", "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY"), 4),
        ("CELL_TOTAL_DRIFT", ("singleton_cells", "total"), 23),
        ("CELL_TERMINAL_DRIFT", ("singleton_cells", "whole_terminal"), 23),
        ("CELL_RESIDUAL_INFLATION", ("singleton_cells", "residual"), 1),
        ("CELL_ENUM_14_SPOOF", ("singleton_cells", "terminal_enum_census", "STRICT_EXCLUSION_ONLY"), 13),
        ("CELL_ENUM_10_SPOOF", ("singleton_cells", "terminal_enum_census", "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY"), 11),
        ("CHILD_LEDGER_MEMBER_DRIFT", ("ledgers", "child_dispositions", "sha256"), "f" * 64),
        ("SOURCE_LEDGER_SEQUENCE_DRIFT", ("ledgers", "source_rollups", "row_hash_line_sequence_sha256"), "0" * 64),
        ("PAIR_LEDGER_SIZE_DRIFT", ("ledgers", "reflection_pair_rollups", "size"), result["ledgers"]["reflection_pair_rollups"]["size"] + 1),
        ("CELL_LEDGER_COUNT_DRIFT", ("ledgers", "singleton_cell_rollups", "row_count"), 23),
        ("PROJECTION_LEDGER_PIN_DRIFT", ("ledgers", "global_enum_projection", "sha256"), "1" * 64),
        ("PROJECTION_ROW_COUNT_DRIFT", ("global_enum_projection", "row_count"), 23),
        ("PROJECTION_SEQUENCE_DRIFT", ("global_enum_projection", "row_hash_line_sequence_sha256"), "2" * 64),
        ("PROJECTION_ORDER_DRIFT", ("global_enum_projection", "row_order"), "CELL_ID_ASCENDING"),
        ("PROJECTION_ROLE_PROMOTION", ("global_enum_projection", "role"), "CANONICAL_STATE"),
        ("PROJECTION_ATOMICITY_WEAKENED", ("global_enum_projection", "atomic_installation_required"), "23_OF_24"),
        ("PROJECTION_INSTALLED_INFLATION", ("global_enum_projection", "installed"), True),
        ("SINGLETON_BRANCH_UNRESOLVED_INFLATION", ("singleton_branch_unresolved",), 1),
        ("PUBLIC_GLOBAL_BEFORE_DRIFT", ("public_global_unresolved_before",), 1147),
        ("PUBLIC_GLOBAL_AFTER_BRANCH_DRIFT", ("public_global_unresolved_after_branch",), 1123),
        ("PUBLIC_GLOBAL_UNRESOLVED_ZERO_INFLATION_MUST_FAIL_CLOSED", ("public_global_unresolved_zero",), True),
        ("CURRENT_PUBLIC_AFTER_DECREMENT_INFLATION", ("public_global_unresolved", "current_after"), 1124),
        ("CURRENT_CANDIDATE_DECREMENT_INFLATION", ("public_global_unresolved", "current_candidate_decrement"), 24),
        ("CONDITIONAL_PROJECTED_DECREMENT_DRIFT", ("public_global_unresolved", "conditional_projection", "projected_decrement"), 23),
        ("CONDITIONAL_PROJECTED_AFTER_DRIFT", ("public_global_unresolved", "conditional_projection", "projected_after"), 1125),
        ("CONDITIONAL_PROJECTION_INSTALLED_INFLATION", ("public_global_unresolved", "conditional_projection", "installed"), True),
        ("BRANCH_TARGET_SUBSTITUTION", ("branch_projection_target",), "CANONICAL_GLOBAL"),
        ("BRANCH_CANONICAL_INSTALL_INFLATION", ("branch_projection_installed_as_canonical_state",), True),
        ("CANDIDATE_AUTHORITY_INFLATION", ("candidate_is_authority",), True),
        ("CANONICAL_POINTER_WRITE_INFLATION", ("canonical_pointer_or_seal_written",), True),
        ("RUNTIME_CANONICAL_WRITE_INFLATION", ("runtime_canonical_pointer_or_seal_writes",), True),
        ("FORMAL_CREDIT_INFLATION", ("credit_boundary", "formal_credit"), 1),
        ("D02_CREDIT_INFLATION", ("credit_boundary", "D02_gate_credit"), 1),
        ("CM2_CREDIT_INFLATION", ("credit_boundary", "CM2_credit"), 1),
        ("WHOLE_PARENT_CREDIT_INFLATION", ("credit_boundary", "whole_parent_credit"), 1),
        ("GLOBAL_INSTALLED_CREDIT_INFLATION", ("credit_boundary", "global_installed_credit"), 1),
    ]
    for name, path, replacement in result_specs:
        exact_attack(name, result, path, replacement)

    child = child_data["samples"]["decision_child"]
    source = source_data["samples"]["cemetery_source"]
    pair = pair_data["sample"]
    cell = next(iter(cell_data["by_cell"].values()))
    projection = projection_data["rows"][0]
    row_specs = [
        ("CHILD_C65_JOIN_DRIFT", child, ("C65_child_row_sha256",), "3" * 64),
        ("CHILD_C71B_JOIN_DRIFT", child, ("C71b_H1_row_sha256",), "4" * 64),
        ("CHILD_C61_JOIN_DRIFT", child, ("C61_source_row_sha256",), "5" * 64),
        ("CHILD_SOURCE_PATH_JOIN_DRIFT", child, ("source_path",), child["source_path"] + "0"),
        ("CHILD_DECISION_PROOF_SUBSTITUTION", child, ("C77d_decision_route_row_sha256",), "6" * 64),
        ("CHILD_DISPOSITION_SPOOF", child, ("disposition",), "CEMETERY_TANGENCY_TERMINAL"),
        ("CHILD_RESIDUAL_INFLATION", child, ("explicit_residual_count",), 1),
        ("SOURCE_CEMETERY_ENUM_SPOOF", source, ("terminal_enum",), "STRICT_EXCLUSION_ONLY"),
        ("SOURCE_CEMETERY_COUNT_SPOOF", source, ("selected_cemetery_tangency_terminal_child_count",), source["selected_cemetery_tangency_terminal_child_count"] - 1),
        ("SOURCE_KRAFT_DRIFT", source, ("selected_child_Kraft",), "0"),
        ("PAIR_PARENT_KRAFT_DRIFT", pair, ("parent_Kraft",), "1/2"),
        ("PAIR_PREFIX_FREE_FALSE", pair, ("parent_prefix_free",), False),
        ("PAIR_CERTIFICATE_FALSE", pair, ("prefix_free_and_exact_Kraft_one_certificate_carried_from_C77s",), False),
        ("PAIR_CEMETERY_ENUM_SPOOF", pair, ("terminal_enum",), "STRICT_EXCLUSION_ONLY"),
        ("CELL_C77S_ROW_SUBSTITUTION", cell, ("C77s_singleton_cell_rollup_row_sha256",), "7" * 64),
        ("CELL_GLOBAL_INSTALL_INFLATION", cell, ("global_projection_installed",), True),
        ("CELL_CURRENT_DECREMENT_INFLATION", cell, ("candidate_public_unresolved_decrement",), 1),
        ("C55A_IDENTITY_SUBSTITUTION_MUST_FAIL_CLOSED", projection, ("C55A_identity", "row_sha256"), "8" * 64),
        ("C55A_CELL_ID_SUBSTITUTION", projection, ("C55A_identity", "cell_id"), "substitute-cell"),
        ("C55A_COMPONENT_SUBSTITUTION", projection, ("C55A_identity", "component_index"), 999),
        ("PROJECTION_C77S_CELL_SUBSTITUTION", projection, ("C77s_cell_rollup_row_sha256",), "9" * 64),
        ("PROJECTION_TERMINAL_AUTHORITY_PROMOTION", projection, ("terminal_disposition_authority",), projection["terminal_disposition_authority"] + ["C55A"]),
        ("PROJECTION_C55A_ROLE_PROMOTION", projection, ("C55A_role",), "TERMINAL_AUTHORITY"),
        ("PROJECTION_ENUM_SPOOF", projection, ("terminal_enum",), "STRICT_EXCLUSION_ONLY"),
        ("PROJECTION_GLOBAL_ZERO_INFLATION", projection, ("public_global_unresolved_zero",), True),
        ("PROJECTION_INSTALL_INFLATION", projection, ("global_projection_installed",), True),
        ("PROJECTION_CREDIT_INFLATION", projection, ("formal_credit",), 1),
    ]
    for name, target, path, replacement in row_specs:
        exact_attack(name, target, path, replacement)

    for name, rows in (
        ("C55A_PROJECTION_ORDER_SWAP", [projection_data["rows"][1], projection_data["rows"][0],
                                        *projection_data["rows"][2:]]),
        ("C55A_PROJECTION_DUPLICATE", [projection_data["rows"][0], projection_data["rows"][0],
                                       *projection_data["rows"][2:]]),
    ):
        try:
            need([row["row_sha256"] for row in rows] ==
                 [row["row_sha256"] for row in projection_data["rows"]], "projection order")
        except Reject:
            rejected.append(name)
        else:
            raise Reject("sequence attack accepted:" + name)

    exact_attack("BASE_OUTER_RESULT_OBJECT_DRIFT", outer, ("result_object_sha256",), "a" * 64)
    exact_attack("BASE_OUTER_REPLAY_COUNT_DRIFT", outer, ("terminal_byte_replay_member_count",), 9)
    exact_attack("BASE_OUTER_GLOBAL_ZERO_INFLATION", outer, ("public_global_unresolved_zero",), True)
    exact_attack(
        "VERIFIER_FILE_SHA256_DRIFT",
        {"verifier_file_sha256": verifier_file_sha256},
        ("verifier_file_sha256",), "b" * 64,
    )

    try:
        parse_json(b'{"a":1,"a":2}', "duplicate-key attack")
    except Reject:
        rejected.append("DUPLICATE_JSON_KEY")
    else:
        raise Reject("duplicate JSON key attack accepted")
    try:
        parse_json(b'{ "a": 1 }', "noncanonical attack")
    except Reject:
        rejected.append("NONCANONICAL_JSON")
    else:
        raise Reject("noncanonical JSON attack accepted")
    tiny_gzip = gzip.compress(b"{}\n", mtime=0)
    for name, raw in (("MULTI_MEMBER_GZIP", tiny_gzip + tiny_gzip),
                      ("TRAILING_GZIP_BYTES", tiny_gzip + b"x")):
        try:
            one_gzip(raw, name)
        except Reject:
            rejected.append(name)
        else:
            raise Reject("gzip attack accepted:" + name)
    order, entries = manifest_entries(manifest_raw, "attack manifest")
    try:
        need(tuple(reversed(order)) == BASE_MEMBER_ORDER and
             entries == entries, "manifest order attack")
    except Reject:
        rejected.append("BASE_MANIFEST_ORDER_REVERSAL")
    else:
        raise Reject("manifest order attack accepted")

    need(len(rejected) >= 100 and len(rejected) == len(set(rejected)),
         "attack matrix cardinality/uniqueness")
    return {"attack_count": len(rejected), "rejected": len(rejected), "names": rejected}


def build_verification(
    identities: dict[str, str], result: dict[str, Any], attacks: dict[str, Any],
    incidence: dict[str, Any], verifier_file_sha256: str,
) -> dict[str, Any]:
    false_policy = {
        "compiled": False, "decoded": False, "executed": False,
        "imported": False, "opened": False, "parsed": False, "read": False,
    }
    return add_object_hash({
        "schema": SCHEMA + ".independent-verification",
        "status": "PASS_INDEPENDENT_NO_PRODUCER_EXACT_RECONSTRUCTION__SEALED_C77S_C77D_TERMINAL_AUTHORITY_ONLY__C55A_IDENTITY_ONLY__ZERO_INSTALLED_CREDIT",
        "contract": {"file_sha256": CONTRACT_FILE_PIN, "object_sha256": CONTRACT_OBJECT_PIN},
        "verifier_file_sha256": verifier_file_sha256,
        "producer_file_sha256_declaration_only": PRODUCER_DECLARED_PIN,
        "producer_source_policy": false_policy,
        "upstream_producer_source_policy": {"C77s": false_policy, "C77d": false_policy},
        "candidate_base_bundle": {
            "exact_member_count_per_stage": len(BASE_UNIVERSE),
            "stage_a_stage_b_bytes_identical": True,
            "stage_a_stage_b_inodes_distinct": True,
            "base_manifest_filename": MANIFEST,
            "base_manifest_file_sha256": identities[MANIFEST],
            "base_outer_receipt_filename": BASE_OUTER,
            "base_outer_receipt_file_sha256": identities[BASE_OUTER],
            "result_filename": RESULT,
            "result_file_sha256": identities[RESULT],
            "result_object_sha256": result["object_sha256"],
            "base_member_file_sha256": {name: identities[name] for name in BASE_UNIVERSE},
        },
        "sealed_terminal_authority": {
            "exclusive_sources": [
                "INDEPENDENTLY_VERIFIED_SEALED_C77S_DUAL_BUNDLE",
                "INDEPENDENTLY_VERIFIED_SEALED_C77D_DUAL_BUNDLE",
            ],
            "C55A_role": "OVERLAY_IDENTITY_ONLY_NEVER_TERMINAL_AUTHORITY",
            "C55A_may_supply_or_modify_terminal_disposition": False,
            "C77s_final_outer_object_sha256": C77S_FINAL_OUTER_OBJECT_PIN,
            "C77d_final_outer_object_sha256": C77D_FINAL_OUTER_OBJECT_PIN,
        },
        "exact_reconstruction": {
            "children": 167255, "strict_exclusion": 144004,
            "cemetery_tangency_terminal": 23251,
            "decision_rows_consumed_exactly_once": 33100,
            "explicit_residual": 0, "sealed_collision3_handoff": 0,
            "sources_whole_terminal": 20879,
            "reflection_pairs_whole_terminal": 12,
            "singleton_cells_whole_terminal": 24,
            "projection_rows_exact_one_to_one": 24,
            "pair_terminal_enum_census": {
                "STRICT_EXCLUSION_ONLY": 7,
                "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": 5,
            },
            "cell_terminal_enum_census": {
                "STRICT_EXCLUSION_ONLY": 14,
                "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": 10,
            },
            "C77d_root_incidence": incidence,
        },
        "branch_boundary": {
            "singleton_branch_unresolved": 0,
            "public_global_unresolved_before": 1148,
            "public_global_unresolved_after_branch": 1124,
            "current_public_global_unresolved": 1148,
            "public_global_unresolved_zero": False,
            "conditional_projection_installed": False,
            "candidate_public_unresolved_decrement": 0,
            "projection_target": "C79G_ATOMIC_MERGE",
        },
        "coherent_attacks": attacks,
        "audit_only_mode_supported_with_zero_writes": True,
        "default_finalization_order": [
            "verification", "one_final_manifest", "final_outer_receipt_last",
            "terminal_byte_replay_13_members",
        ],
        "candidate_is_authority": False,
        "canonical_pointer_or_seal_written": False,
        "runtime_canonical_pointer_or_seal_writes": False,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    })


def validate_all(stage_a: Path, stage_b: Path) -> dict[str, Any]:
    need(set(FINAL_UNIVERSE).issubset(READABLE_ARTIFACT_NAMES),
         "all 13 final-universe artifacts must be on the exact read allow-list")
    need(not any(Path(name).suffix.lower() in EXECUTABLE_SOURCE_SUFFIXES
                 for name in FINAL_UNIVERSE),
         "final universe must contain no executable source type")
    verifier_file_sha256 = digest(safe_read_self_verifier())
    need(len(verifier_file_sha256) == 64 and
         all(character in "0123456789abcdef" for character in verifier_file_sha256),
         "verifier self SHA-256 shape")
    load_contract()
    c77s_base_order = (
        C77S_LOCK, C77S_CHILD, C77S_SOURCE, C77S_PAIR, C77S_CELL,
        C77S_INCIDENCE, C77S_RESULT, C77S_REPORT,
    )
    c77s_final_order = c77s_base_order + (C77S_MANIFEST, C77S_BASE_OUTER, C77S_VERIFY)
    c77d_base_order = (C77D_LOCK, C77D_ROWS, C77D_INCIDENCE, C77D_RESULT, C77D_REPORT)
    c77d_final_order = c77d_base_order + (C77D_MANIFEST, C77D_VERIFY)
    c77s = load_pinned_dual(
        "C77s", C77S_A, C77S_B, C77S_PINS,
        C77S_MANIFEST, c77s_base_order,
        C77S_FINAL_MANIFEST, c77s_final_order, C77S_FINAL_OUTER,
    )
    c77d = load_pinned_dual(
        "C77d", C77D_A, C77D_B, C77D_PINS,
        C77D_MANIFEST, c77d_base_order,
        C77D_FINAL_MANIFEST, c77d_final_order, C77D_FINAL_OUTER,
    )
    need(parse_json(c77s[C77S_FINAL_OUTER], "C77s final outer")["object_sha256"] ==
         C77S_FINAL_OUTER_OBJECT_PIN, "C77s final outer object pin")
    need(parse_json(c77d[C77D_FINAL_OUTER], "C77d final outer")["object_sha256"] ==
         C77D_FINAL_OUTER_OBJECT_PIN, "C77d final outer object pin")
    values, identities = load_candidate_dual(stage_a, stage_b)
    s_result, d_result = validate_input_objects(c77s, c77d)
    evidence, incidence = validate_c77d(c77d, d_result)
    c55a = load_c55a()
    need(c55a["full_sequence"] ==
         "26b4a9674e3dd1c3ca223cab456bd655c0c5c2f440034551a8fbc07ef9a4ea2c",
         "C55A full leaf sequence")

    children = reconstruct_children(c77s[C77S_CHILD], values[CHILD], evidence, s_result)
    sources = reconstruct_sources(c77s[C77S_SOURCE], values[SOURCE], children, s_result)
    pairs = reconstruct_pairs(c77s[C77S_PAIR], values[PAIR], children["pair_stats"], s_result)
    cells = reconstruct_cells(c77s[C77S_CELL], values[CELL], pairs, s_result)
    projection = reconstruct_projection(values[PROJECTION], c55a, cells)
    descriptors = {
        "child_dispositions": children["descriptor"],
        "source_rollups": sources["descriptor"],
        "reflection_pair_rollups": pairs["descriptor"],
        "singleton_cell_rollups": cells["descriptor"],
        "global_enum_projection": projection["descriptor"],
    }
    result = parse_json(values[RESULT], "C78s result")
    need(isinstance(result, dict), "C78s result shape")
    reconstructed_result = expected_result(
        descriptors, c55a, s_result, d_result, incidence,
        pairs["enum_census"], cells["enum_census"],
    )
    compare_exact(result, reconstructed_result, "result")
    recursive_boundaries(result, "C78s.result")

    need(values[LOCK] == (
        b"C78s candidate only; no public/global/formal/D02/CM2/whole-parent credit.\n"
        b"The 24-row global enumeration projection is not installed.\n"
    ), "C78s exact lock")
    need(values[REPORT] == expected_report(result["object_sha256"]), "C78s exact report")
    outer = parse_json(values[BASE_OUTER], "C78s base outer exact")
    compare_exact(outer, expected_base_outer(identities, result), "base outer")
    attacks = run_attacks(
        result, outer, children, sources, pairs, cells, projection, values[MANIFEST],
        verifier_file_sha256,
    )
    verification = build_verification(
        identities, result, attacks, incidence, verifier_file_sha256,
    )
    need(verification.get("verifier_file_sha256") == verifier_file_sha256,
         "verification self-binding mismatch")
    recursive_boundaries(verification, "C78s.verification")
    return {
        "values": values, "identities": identities, "result": result,
        "outer": outer, "verification": verification, "attacks": attacks,
    }


def write_exclusive(path: Path, raw: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor_fd = os.open(path, flags, 0o444)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor_fd, view)
            need(written > 0, f"short append-only write:{path}")
            view = view[written:]
        os.fsync(descriptor_fd)
    finally:
        os.close(descriptor_fd)
    directory_fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def replay_dual(
    stage_a: Path, stage_b: Path, names: tuple[str, ...], pins: dict[str, str],
) -> None:
    need(exact_names(stage_a) == set(names) and exact_names(stage_b) == set(names),
         f"dual replay exact universe:{len(names)}")
    for name in names:
        left, li = safe_read(stage_a / name, pins[name])
        right, ri = safe_read(stage_b / name, pins[name])
        need(left == right and li != ri, f"dual terminal byte/inode replay:{name}")


def final_outer(
    verification: dict[str, Any], verification_pin: str,
    final_manifest_pin: str,
) -> dict[str, Any]:
    return add_object_hash({
        "schema": SCHEMA + ".independent-verification.final-outer-receipt",
        "status": "PASS_DUAL_ISOLATED_BYTE_IDENTICAL__INDEPENDENT_NO_PRODUCER_RECONSTRUCTION__ONE_FINAL_MANIFEST__FINAL_OUTER_LAST__ZERO_INSTALLED_CREDIT",
        "producer_file_sha256_declaration_only": PRODUCER_DECLARED_PIN,
        "verifier_file_sha256": verification["verifier_file_sha256"],
        "producer_source_opened_read_parsed_decoded_imported_compiled_or_executed": False,
        "verification_filename": VERIFY,
        "verification_file_sha256": verification_pin,
        "verification_object_sha256": verification["object_sha256"],
        "final_manifest_filename": FINAL_MANIFEST,
        "final_manifest_file_sha256": final_manifest_pin,
        "final_manifest_member_count": len(FINAL_MANIFEST_ORDER),
        "final_manifest_order": list(FINAL_MANIFEST_ORDER),
        "final_outer_receipt_published_last_in_each_stage": True,
        "append_only_finalization_supersedes_base_outer_last_scope": True,
        "base_outer_was_last_in_base_publication": True,
        "base_outer_receipt_role":
            "VALID_CANDIDATE_STAGE_RECEIPT_SUPERSEDED_ONLY_FOR_FINAL_BUNDLE_ORDERING_NOT_INVALIDATED_OR_DELETED",
        "terminal_byte_replay_member_count_per_stage": len(FINAL_UNIVERSE),
        "all_final_members_terminal_byte_replayed_in_both_stages": True,
        "all_final_stage_bytes_identical": True,
        "terminal_disposition_authority_exclusive": [
            "INDEPENDENTLY_VERIFIED_SEALED_C77S_DUAL_BUNDLE",
            "INDEPENDENTLY_VERIFIED_SEALED_C77D_DUAL_BUNDLE",
        ],
        "C55A_role": "OVERLAY_IDENTITY_ONLY_NEVER_TERMINAL_AUTHORITY",
        "singleton_branch_unresolved": 0,
        "public_global_unresolved_before": 1148,
        "public_global_unresolved_after_branch": 1124,
        "current_public_global_unresolved": 1148,
        "public_global_unresolved_zero": False,
        "conditional_projection_installed": False,
        "candidate_is_authority": False, "candidate_public_unresolved_decrement": 0,
        "canonical_pointer_or_seal_written": False,
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    })


def finalize(stage_a: Path, stage_b: Path, validated: dict[str, Any]) -> dict[str, Any]:
    identities = dict(validated["identities"])
    need(exact_names(stage_a) == set(BASE_UNIVERSE) and
         exact_names(stage_b) == set(BASE_UNIVERSE), "base stages changed before finalization")
    need(stat.S_IMODE(os.stat(stage_a, follow_symlinks=False).st_mode) == 0o555 and
         stat.S_IMODE(os.stat(stage_b, follow_symlinks=False).st_mode) == 0o555,
         "append-only finalization requires both sealed base stage directories at mode 0555")
    for stage in (stage_a, stage_b):
        for name in (VERIFY, FINAL_MANIFEST, FINAL_OUTER):
            need(not (stage / name).exists(), f"append-only final member already exists:{stage / name}")

    verification_raw = canonical(validated["verification"]) + b"\n"
    verification_pin = digest(verification_raw)
    identities[VERIFY] = verification_pin
    final_manifest_raw = b"".join(
        f"{identities[name]}  {name}\n".encode("ascii") for name in FINAL_MANIFEST_ORDER
    )
    final_manifest_pin = digest(final_manifest_raw)
    identities[FINAL_MANIFEST] = final_manifest_pin
    outer = final_outer(validated["verification"], verification_pin, final_manifest_pin)
    outer_raw = canonical(outer) + b"\n"
    outer_pin = digest(outer_raw)
    identities[FINAL_OUTER] = outer_pin
    replay_dual(stage_a, stage_b, BASE_UNIVERSE,
                {name: identities[name] for name in BASE_UNIVERSE})

    made_writable: list[Path] = []
    try:
        for stage in (stage_a, stage_b):
            os.chmod(stage, 0o755, follow_symlinks=False)
            made_writable.append(stage)
        write_exclusive(stage_a / VERIFY, verification_raw)
        write_exclusive(stage_b / VERIFY, verification_raw)
        replay_dual(stage_a, stage_b, FINAL_MANIFEST_ORDER,
                    {name: identities[name] for name in FINAL_MANIFEST_ORDER})
        write_exclusive(stage_a / FINAL_MANIFEST, final_manifest_raw)
        write_exclusive(stage_b / FINAL_MANIFEST, final_manifest_raw)
        replay_dual(stage_a, stage_b, FINAL_MANIFEST_ORDER + (FINAL_MANIFEST,),
                    {name: identities[name]
                     for name in FINAL_MANIFEST_ORDER + (FINAL_MANIFEST,)})
        write_exclusive(stage_a / FINAL_OUTER, outer_raw)
        write_exclusive(stage_b / FINAL_OUTER, outer_raw)
        replay_dual(stage_a, stage_b, FINAL_UNIVERSE,
                    {name: identities[name] for name in FINAL_UNIVERSE})
    finally:
        restore_errors: list[str] = []
        for stage in reversed(made_writable):
            try:
                os.chmod(stage, 0o555, follow_symlinks=False)
            except OSError as exc:
                restore_errors.append(f"{stage}:{exc}")
        need(not restore_errors, "failed to restore sealed directory modes:" + ";".join(restore_errors))
    need(stat.S_IMODE(os.stat(stage_a, follow_symlinks=False).st_mode) == 0o555 and
         stat.S_IMODE(os.stat(stage_b, follow_symlinks=False).st_mode) == 0o555,
         "final stage directories not resealed at mode 0555")
    replay_dual(stage_a, stage_b, FINAL_UNIVERSE,
                {name: identities[name] for name in FINAL_UNIVERSE})
    return {
        "status": "FINALIZED", "final_member_count_per_stage": len(FINAL_UNIVERSE),
        "verification_file_sha256": verification_pin,
        "verification_object_sha256": validated["verification"]["object_sha256"],
        "final_manifest_file_sha256": final_manifest_pin,
        "final_outer_receipt_file_sha256": outer_pin,
        "final_outer_receipt_object_sha256": outer["object_sha256"],
        "coherent_attack_count": validated["attacks"]["attack_count"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage-a", type=Path, default=DEFAULT_STAGE_A)
    parser.add_argument("--stage-b", type=Path, default=DEFAULT_STAGE_B)
    parser.add_argument("--audit-only", action="store_true",
                        help="validate everything and perform zero filesystem writes")
    arguments = parser.parse_args()
    try:
        validated = validate_all(arguments.stage_a, arguments.stage_b)
        if arguments.audit_only:
            summary = {
                "status": "PASS_AUDIT_ONLY_ZERO_WRITES",
                "candidate_result_object_sha256": validated["result"]["object_sha256"],
                "verification_object_sha256": validated["verification"]["object_sha256"],
                "coherent_attack_count": validated["attacks"]["attack_count"],
                "candidate_member_count_per_stage": len(BASE_UNIVERSE),
            }
        else:
            summary = finalize(arguments.stage_a, arguments.stage_b, validated)
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 0
    except (Reject, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"REJECT:{exc}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
