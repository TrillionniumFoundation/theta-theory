#!/usr/bin/env python3
"""Append-only C78s singleton final candidate consumer.

The only terminal-evidence inputs are the exact sealed, independently verified
dual C77s and C77d stage bundles named below.  A narrowly pinned C55A
ledger/result/verification/manifest quartet supplies overlay identity only and
is forbidden from supplying or modifying a terminal disposition.  In
particular, this program never opens, reads, parses, decodes, imports, compiles,
or executes either upstream producer source.  It preserves C77s blocker
terminals and consumes every C77s decision residual exactly once through the
matching sealed C77d decision row.

The resulting 24-row global enumeration is a projection only.  Nothing here
installs it in the public global consumer, changes public unresolved=1148, or
earns formal, global, D02, CM2, or whole-parent credit.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import stat
import zlib
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "cm2.round306c78s.singleton-final-no-producer-consumer.v1"
BASE = "cm2_round306c78s_singleton_final_no_producer_consumer_v1"

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
C55A_OVERLAY_ROW_HASH_SEQUENCE_PIN = "3c6dbfc7f3cba144c99e87b3886954b996a18aff3822f248a351c03d4558a939"

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

C77D_LOCK = "ZERO_CREDIT_STAGED_C77D_DECISION_ROUTE_STRICT_EXCLUSION_ONLY.lock"
C77D_ROWS = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_rows.jsonl.gz"
C77D_INCIDENCE = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_root_incidence.jsonl.gz"
C77D_RESULT = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_result.json"
C77D_REPORT = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_report.md"
C77D_MANIFEST = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_candidate_manifest.sha256"
C77D_VERIFY = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_independent_verification_v1.json"
C77D_FINAL_MANIFEST = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_final_manifest_v1.sha256"
C77D_FINAL_OUTER = "cm2_round306c77d_decision_child_exact_route_strict_exclusion_v1_final_outer_receipt_v1.json"

# These are exact file-byte pins, not merely object hashes.  The three explicit
# C77d placeholders must be replaced only after the append-only finalizer has
# published the corresponding members.  The program rejects before reading any
# stage or creating an output directory while a placeholder remains.
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

C77S_BASE_ORDER = (
    C77S_LOCK, C77S_CHILD, C77S_SOURCE, C77S_PAIR, C77S_CELL,
    C77S_INCIDENCE, C77S_RESULT, C77S_REPORT,
)
C77S_FINAL_ORDER = C77S_BASE_ORDER + (C77S_MANIFEST, C77S_BASE_OUTER, C77S_VERIFY)
C77D_BASE_ORDER = (C77D_LOCK, C77D_ROWS, C77D_INCIDENCE, C77D_RESULT, C77D_REPORT)
C77D_FINAL_ORDER = C77D_BASE_ORDER + (C77D_MANIFEST, C77D_VERIFY)

PAIR_IDS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)
CREDIT_KEYS = (
    "formal_credit", "D02_gate_credit", "CM2_credit",
    "whole_parent_credit", "global_installed_credit",
)

OUT_LOCK = "ZERO_CREDIT_CANDIDATE_SINGLETON_FINAL_NO_PRODUCER_CONSUMER_ONLY.lock"
OUT_CHILD = BASE + "_child_dispositions.jsonl.gz"
OUT_SOURCE = BASE + "_source_rollups.jsonl.gz"
OUT_PAIR = BASE + "_reflection_pair_rollups.jsonl.gz"
OUT_CELL = BASE + "_singleton_cell_rollups.jsonl.gz"
OUT_PROJECTION = BASE + "_global_enum_projection.jsonl.gz"
OUT_RESULT = BASE + "_result.json"
OUT_REPORT = BASE + "_report.md"
OUT_MANIFEST = BASE + "_manifest.sha256"
OUT_OUTER = BASE + "_outer_receipt.json"
OUT_MEMBER_ORDER = (
    OUT_LOCK, OUT_CHILD, OUT_SOURCE, OUT_PAIR, OUT_CELL, OUT_PROJECTION,
    OUT_RESULT, OUT_REPORT,
)
OUT_UNIVERSE = OUT_MEMBER_ORDER + (OUT_MANIFEST, OUT_OUTER)


class Reject(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def raw_digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def object_digest(value: dict[str, Any]) -> str:
    body = dict(value)
    body.pop("object_sha256", None)
    return raw_digest(canonical(body))


def parse_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in items:
            need(key not in value, f"duplicate JSON key:{label}:{key}")
            value[key] = item
        return value

    try:
        value = json.loads(
            raw, object_pairs_hook=pairs,
            parse_constant=lambda item: (_ for _ in ()).throw(Reject(item)),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(f"invalid JSON:{label}:{exc}") from exc
    need(raw in (canonical(value), canonical(value) + b"\n"),
         f"noncanonical JSON:{label}")
    if isinstance(value, dict) and "object_sha256" in value:
        need(value["object_sha256"] == object_digest(value),
             f"object hash mismatch:{label}")
    return value


def add_row_hash(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "output row already hashed")
    return {**body, "row_sha256": raw_digest(canonical(body))}


def add_object_hash(body: dict[str, Any]) -> dict[str, Any]:
    need("object_sha256" not in body, "output object already hashed")
    return {**body, "object_sha256": raw_digest(canonical(body))}


def no_credit(value: dict[str, Any], label: str, *, require: Iterable[str] = ()) -> None:
    for key in require:
        need(key in value, f"missing zero-credit field:{label}:{key}")
    for key in CREDIT_KEYS:
        if key in value:
            need(value[key] == 0, f"credit inflation:{label}:{key}")


def ensure_no_placeholders() -> None:
    unresolved = [f"{name}={pin}" for name, pin in C77D_PINS.items()
                  if pin.startswith("__PIN_REQUIRED_")]
    need(not unresolved, "UNFILLED_C77D_FINAL_PINS:" + ",".join(unresolved))


def exact_stage_names(stage: Path) -> set[str]:
    need(stage.is_dir() and not stage.is_symlink(), f"stage missing/unsafe:{stage}")
    names: set[str] = set()
    with os.scandir(stage) as entries:
        for entry in entries:
            need(entry.name not in names, f"duplicate stage member:{stage}:{entry.name}")
            info = entry.stat(follow_symlinks=False)
            need(not entry.is_symlink() and stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                 f"unsafe stage member:{stage}:{entry.name}")
            names.add(entry.name)
    return names


def stable_member(stage: Path, name: str, expected: str) -> tuple[bytes, tuple[int, int]]:
    need(stage in (C77S_A, C77S_B, C77D_A, C77D_B), "unapproved input stage")
    need(Path(name).name == name and "/" not in name and Path(name).suffix != ".py",
         f"unsafe or forbidden member name:{name}")
    path = stage / name
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             f"unsafe input member:{path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    identity = (before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
                before.st_size, before.st_mtime_ns)
    need(identity == (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                      after.st_size, after.st_mtime_ns), f"input fd drift:{path}")
    need(identity == (current.st_dev, current.st_ino, current.st_mode,
                      current.st_nlink, current.st_size, current.st_mtime_ns),
         f"input path drift:{path}")
    raw = b"".join(chunks)
    need(raw_digest(raw) == expected, f"input pin mismatch:{path}")
    return raw, (before.st_dev, before.st_ino)


def stable_local(rel: str, expected: str) -> bytes:
    approved = set(C55A_PINS) | {CONTRACT_REL}
    # The closed allow-list is the authority boundary.  Reject executable
    # inputs by type; do not reject the contract merely because its schema
    # name contains the policy phrase ``no_producer``.
    need(rel in approved and Path(rel).suffix != ".py",
         f"unapproved or executable local input:{rel}")
    path = ROOT / rel
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             f"unsafe local input:{rel}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    identity = (before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
                before.st_size, before.st_mtime_ns)
    need(identity == (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                      after.st_size, after.st_mtime_ns), f"local input fd drift:{rel}")
    need(identity == (current.st_dev, current.st_ino, current.st_mode,
                      current.st_nlink, current.st_size, current.st_mtime_ns),
         f"local input path drift:{rel}")
    raw = b"".join(chunks)
    need(raw_digest(raw) == expected, f"local input pin mismatch:{rel}")
    return raw


def manifest_entries(
    raw: bytes, label: str, *, allow_relative_paths: bool = False,
) -> tuple[list[str], dict[str, str]]:
    need(raw.endswith(b"\n"), f"manifest missing final newline:{label}")
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise Reject(f"non-ASCII manifest:{label}") from exc
    order: list[str] = []
    values: dict[str, str] = {}
    for line in lines:
        pieces = line.split("  ")
        need(len(pieces) == 2, f"manifest syntax:{label}")
        pin, name = pieces
        need(len(pin) == 64 and all(ch in "0123456789abcdef" for ch in pin),
             f"manifest digest:{label}:{name}")
        member = Path(name)
        if allow_relative_paths:
            need(not member.is_absolute() and ".." not in member.parts and name not in ("", "."),
                 f"manifest relative member path:{label}:{name}")
        else:
            need(member.name == name, f"manifest basename member:{label}:{name}")
        need(name not in values, f"manifest duplicate member:{label}:{name}")
        order.append(name)
        values[name] = pin
    return order, values


def load_dual_bundle(
    label: str, stage_a: Path, stage_b: Path, pins: dict[str, str],
    base_manifest: str, base_order: tuple[str, ...],
    final_manifest: str, final_outer: str, final_order: tuple[str, ...],
) -> dict[str, bytes]:
    expected_names = set(pins)
    need(exact_stage_names(stage_a) == expected_names,
         f"{label} stage-A exact member universe")
    need(exact_stage_names(stage_b) == expected_names,
         f"{label} stage-B exact member universe")
    captured: dict[str, bytes] = {}
    for name, pin in pins.items():
        left, left_inode = stable_member(stage_a, name, pin)
        right, right_inode = stable_member(stage_b, name, pin)
        need(left == right, f"{label} dual byte mismatch:{name}")
        need(left_inode != right_inode, f"{label} dual inode alias:{name}")
        captured[name] = left

    base_names, base_values = manifest_entries(captured[base_manifest], label + ":base")
    need(tuple(base_names) == base_order, f"{label} base manifest order")
    need(base_values == {name: pins[name] for name in base_order},
         f"{label} base manifest closure")

    final_names, final_values = manifest_entries(captured[final_manifest], label + ":final")
    need(tuple(final_names) == final_order, f"{label} final manifest order")
    need(final_values == {name: pins[name] for name in final_order},
         f"{label} final manifest closure")

    outer = parse_json(captured[final_outer], label + ":final-outer")
    need(isinstance(outer, dict), f"{label} final outer object")
    if label == "C77d":
        need(outer.get("object_sha256") == C77D_FINAL_OUTER_OBJECT_PIN,
             "C77d final outer object pin")
    need(outer.get("candidate_is_authority") is False,
         f"{label} outer authority boundary")
    need(outer.get("final_manifest_filename") == final_manifest and
         outer.get("final_manifest_file_sha256") == pins[final_manifest],
         f"{label} outer/final-manifest link")
    need(outer.get("final_manifest_member_count") == len(final_order) and
         outer.get("final_manifest_order") == list(final_order),
         f"{label} outer final universe")
    need(outer.get("final_outer_receipt_published_last_in_each_stage") is True and
         outer.get("all_final_members_terminal_byte_replayed_in_both_stages") is True and
         outer.get("all_final_stage_bytes_identical") is True and
         outer.get("terminal_byte_replay_member_count_per_stage") == len(pins),
         f"{label} outer-last terminal replay")
    need(outer.get("candidate_public_unresolved_decrement") == 0,
         f"{label} outer unresolved inflation")
    no_credit(outer, label + ":final-outer")
    return captured


def one_gzip_member(raw: bytes, label: str) -> None:
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    for offset in range(0, len(raw), 1 << 20):
        decoder.decompress(raw[offset:offset + (1 << 20)])
        need(not decoder.unused_data, f"multiple gzip members/trailing bytes:{label}")
    decoder.flush()
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
         f"invalid single-member gzip:{label}")


def iter_rows(raw: bytes, label: str) -> Iterator[dict[str, Any]]:
    one_gzip_member(raw, label)
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
        for ordinal, line in enumerate(stream, 1):
            need(line.endswith(b"\n"), f"row missing newline:{label}:{ordinal}")
            row = parse_json(line[:-1], f"{label}:{ordinal}")
            need(isinstance(row, dict) and isinstance(row.get("row_sha256"), str),
                 f"row object/hash missing:{label}:{ordinal}")
            body = dict(row)
            row_hash = body.pop("row_sha256")
            need(row_hash == raw_digest(canonical(body)), f"row hash mismatch:{label}:{ordinal}")
            yield row


def scan_descriptor(raw: bytes, rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    sequence = hashlib.sha256()
    count = 0
    for row in rows:
        count += 1
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    return {
        "row_count": count,
        "row_hash_line_sequence_sha256": sequence.hexdigest(),
        "sha256": raw_digest(raw),
        "size": len(raw),
    }


def check_descriptor(
    published: dict[str, Any], actual: dict[str, Any], filename: str, label: str,
) -> None:
    need(published.get("filename") == filename, f"descriptor filename:{label}")
    for key in ("row_count", "row_hash_line_sequence_sha256", "sha256", "size"):
        need(published.get(key) == actual[key], f"descriptor mismatch:{label}:{key}")


def validate_input_objects(c77s: dict[str, bytes], c77d: dict[str, bytes]) -> tuple[dict[str, Any], dict[str, Any]]:
    s_result = parse_json(c77s[C77S_RESULT], "C77s result")
    s_incidence = parse_json(c77s[C77S_INCIDENCE], "C77s incidence")
    s_base_outer = parse_json(c77s[C77S_BASE_OUTER], "C77s base outer")
    s_verify = parse_json(c77s[C77S_VERIFY], "C77s verification")
    need(all(isinstance(x, dict) for x in (s_result, s_incidence, s_base_outer, s_verify)),
         "C77s JSON object universe")
    need(s_result.get("schema") == "cm2.round306c77s.singleton-parent-no-producer-consumer.v1.result",
         "C77s result schema")
    need(s_result.get("partition") == {
        "total_collision2_handoff_children": 167255,
        "decision_source_children": 33100,
        "blocker_source_children": 134155,
        "identity": "167255=33100+134155",
    }, "C77s exact partition")
    need(s_result.get("blocker_terminal_census") == {
        "whole_child_strict_exclusion": 110904,
        "cemetery_tangency_terminal": 23251,
        "sealed_collision3_handoff": 0,
        "residual": 0,
        "identity": "134155=110904+23251",
    }, "C77s blocker census")
    need(s_result.get("decision_source_disposition", {}).get("residual") == 33100 and
         s_result.get("candidate_is_authority") is False and
         s_result.get("candidate_public_unresolved_decrement") == 0 and
         s_result.get("candidate_public_unresolved_after") == 1148 and
         s_result.get("public_global_unresolved_before") == 1148 and
         s_result.get("canonical_pointer_or_seal_written") is False,
         "C77s fail-closed global boundary")
    need(s_result.get("credit_boundary") == {
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "global_installed_credit": 0, "whole_parent_credit": 0,
    }, "C77s result zero credit")
    need(s_verify.get("producer_source_policy") == {
        "compiled": False, "decoded": False, "executed": False,
        "imported": False, "opened": False, "parsed": False, "read": False,
    }, "C77s independent no-producer policy")
    need(s_verify.get("coherent_attacks", {}).get("attack_count") == 66 and
         s_verify.get("coherent_attacks", {}).get("rejected") == 66,
         "C77s 66/66 attacks")
    need(s_verify.get("reconstruction", {}).get("children") == 167255 and
         s_verify.get("reconstruction", {}).get("decision_residual") == 33100 and
         s_verify.get("reconstruction", {}).get("blocker_terminal") == 134155,
         "C77s verification census")
    need(s_base_outer.get("manifest_filename") == C77S_MANIFEST and
         s_base_outer.get("manifest_file_sha256") == C77S_PINS[C77S_MANIFEST] and
         s_base_outer.get("manifest_member_count") == len(C77S_BASE_ORDER) and
         s_base_outer.get("outer_receipt_published_last") is True and
         s_base_outer.get("all_members_terminal_byte_replayed") is True,
         "C77s base outer closure")
    no_credit(s_base_outer, "C77s base outer")

    d_result = parse_json(c77d[C77D_RESULT], "C77d result")
    d_verify = parse_json(c77d[C77D_VERIFY], "C77d verification")
    need(isinstance(d_result, dict) and isinstance(d_verify, dict), "C77d JSON objects")
    need(d_verify.get("object_sha256") == C77D_VERIFY_OBJECT_PIN,
         "C77d verification object pin")
    need(d_result.get("schema") == "cm2.round306c77d.decision-child-exact-route-strict-exclusion.v1.result",
         "C77d result schema")
    need(d_result.get("scope") == {
        "additional_dyadic_depth": 0, "pair_count": 8, "target_child_count": 33100,
    }, "C77d scope")
    need(d_result.get("whole_child_strict_exclusion_count") == 33100 and
         d_result.get("sealed_collision3_handoff_count") == 0 and
         d_result.get("explicit_residual_child_count") == 0 and
         d_result.get("expected_owner_match_count") == 0 and
         d_result.get("candidate_is_authority") is False and
         d_result.get("global_consumption_ready") is False and
         d_result.get("runtime_canonical_pointer_or_seal_writes") is False,
         "C77d exact zero-credit closure")
    no_credit(d_result, "C77d result", require=CREDIT_KEYS)
    policy = d_verify.get("producer_source_policy", {})
    need(policy == {
        "opened": False, "read": False, "parsed": False, "decoded": False,
        "imported": False, "compiled": False, "executed": False,
    }, "C77d independent no-producer policy")
    coverage = d_verify.get("coverage", {})
    need(coverage.get("target_child_count") == 33100 and
         coverage.get("whole_child_strict_exclusion_count") == 33100 and
         coverage.get("sealed_collision3_handoff_count") == 0 and
         coverage.get("explicit_residual_child_count") == 0,
         "C77d verification coverage")
    attacks = d_verify.get("coherent_attacks", {})
    need(attacks.get("attack_count") == 135 and attacks.get("rejected") == 135,
         "C77d 135/135 coherent attacks")
    need(d_verify.get("candidate_is_authority") is False and
         d_verify.get("global_consumption_ready") is False and
         d_verify.get("runtime_canonical_pointer_or_seal_writes") is False,
         "C77d verification global boundary")
    no_credit(d_verify, "C77d verification", require=CREDIT_KEYS)
    return s_result, d_result


def validate_c77d_rows(raw: bytes, result: dict[str, Any]) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[str, Any]]:
    evidence: dict[tuple[str, str], dict[str, Any]] = {}
    route_census: Counter[str] = Counter()
    input_census: Counter[str] = Counter()
    fresh_census: Counter[str] = Counter()
    sequence = hashlib.sha256()
    count = 0
    for count, row in enumerate(iter_rows(raw, "C77d decision rows"), 1):
        need(row.get("schema") == "cm2.round306c77d.decision-child-exact-route-strict-exclusion.v1.decision-row" and
             row.get("ordinal") == count, "C77d row schema/order")
        no_credit(row, f"C77d decision row:{count}", require=CREDIT_KEYS)
        need(row.get("candidate_is_authority") is False and
             row.get("global_consumption_ready") is False and
             row.get("additional_dyadic_depth") == 0 and
             row.get("whole_child_strict_exclusion_closed") is True and
             row.get("physical_chart_glue_closed") is True and
             row.get("allowed_exit_closed_for_every_stratum") is True and
             row.get("explicit_residual_strata") == 0 and
             row.get("sealed_collision3_handoff_count") == 0 and
             row.get("collision3_handoff") is None and
             row.get("current_disposition") == "STAGED_ZERO_CREDIT_WHOLE_CHILD_STRICT_EXCLUSION",
             f"C77d row closure:{count}")
        exits = row.get("stratum_exits")
        need(isinstance(exits, list) and exits and
             all(item.get("exit_class") == "STRICT_EXCLUSION" for item in exits),
             f"C77d strict exits:{count}")
        c65 = row.get("C65_aggregate_child_row_sha256")
        c71 = row.get("C71b_arrangement_row_sha256")
        key = (c65, c71)
        need(all(isinstance(item, str) and len(item) == 64 for item in key) and key not in evidence,
             f"C77d duplicate/bad join key:{count}")
        evidence[key] = {
            "row_sha256": row["row_sha256"],
            "C61_source_row_sha256": row["C61_aggregate_leaf_row_sha256"],
            "pair_index": row["pair_index"],
            "source_path": row["source_path"],
            "child_path": row["child_path"],
            "route_outcome": row["route_outcome"],
            "fresh_geometry_kind": row["fresh_geometry_kind"],
            "physical_chart_glue_kind": row["physical_chart_glue_kind"],
        }
        route_census[row["route_outcome"]] += 1
        input_census[row["input_arrangement_disposition"]] += 1
        fresh_census[row["fresh_geometry_kind"]] += 1
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    actual = {
        "row_count": count,
        "row_hash_line_sequence_sha256": sequence.hexdigest(),
        "sha256": raw_digest(raw), "size": len(raw),
    }
    need(count == 33100 and len(evidence) == 33100, "C77d exact decision-row count")
    need(dict(sorted(route_census.items())) == result.get("route_census"), "C77d route census")
    need(dict(sorted(input_census.items())) == result.get("input_arrangement_disposition_census"),
         "C77d input disposition census")
    need(dict(sorted(fresh_census.items())) == result.get("fresh_geometry_census"),
         "C77d fresh geometry census")
    check_descriptor(result["ledgers"]["decision_rows"], actual, C77D_ROWS, "C77d rows")
    return evidence, actual


def validate_c77d_incidence(raw: bytes, result: dict[str, Any]) -> dict[str, Any]:
    sequence = hashlib.sha256()
    degrees: Counter[int] = Counter()
    count = 0
    endpoint_sum = 0
    previous_root = ""
    for count, row in enumerate(iter_rows(raw, "C77d root incidence"), 1):
        need(row.get("schema") == "cm2.round306c77d.decision-child-exact-route-strict-exclusion.v1.root-incidence-row",
             f"C77d incidence schema:{count}")
        no_credit(row, f"C77d incidence:{count}", require=CREDIT_KEYS)
        degree = row.get("incidence_count")
        root_id = row.get("root_id")
        need(degree in (1, 2) and isinstance(root_id, str) and root_id > previous_root,
             f"C77d incidence order/degree:{count}")
        need(len(row.get("target_graph_endpoint_occurrences", [])) == degree and
             row.get("incidence_closed") is True and
             row.get("unique_half_open_dyadic_face_owner") and
             row.get("root_is_graph_endpoint_not_physical_terminal") is True and
             row.get("same_physical_trace_duplicate_identified_not_added") is True and
             row.get("paired_N_or_S_representation_is_shadow_only") is True and
             row.get("full_dimensional_Kraft_weight") == "0",
             f"C77d incidence closure:{count}")
        previous_root = root_id
        degrees[degree] += 1
        endpoint_sum += degree
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    actual = {
        "row_count": count,
        "row_hash_line_sequence_sha256": sequence.hexdigest(),
        "sha256": raw_digest(raw), "size": len(raw),
    }
    need(count == 27630 and endpoint_sum == 51494 and
         {str(k): v for k, v in sorted(degrees.items())} == result.get("target_graph_root_degree_census"),
         "C77d incidence census")
    check_descriptor(result["ledgers"]["root_incidence"], actual, C77D_INCIDENCE, "C77d incidence")
    return {**actual, "endpoint_occurrence_count": endpoint_sum,
            "degree_census": {str(k): v for k, v in sorted(degrees.items())}}


def derive_terminal_enum(cemetery_child_count: int) -> str:
    need(isinstance(cemetery_child_count, int) and cemetery_child_count >= 0,
         "invalid cemetery count for enum")
    return ("STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY"
            if cemetery_child_count else "STRICT_EXCLUSION_ONLY")


def validate_c77s_children(
    raw: bytes, result: dict[str, Any], evidence: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    source_stats: dict[str, Counter[str]] = defaultdict(Counter)
    pair_stats: dict[int, Counter[str]] = defaultdict(Counter)
    source_identity: dict[str, tuple[int, str]] = {}
    used: set[tuple[str, str]] = set()
    seen_c65: set[str] = set()
    sequence = hashlib.sha256()
    census: Counter[str] = Counter()
    count = 0
    for count, row in enumerate(iter_rows(raw, "C77s child dispositions"), 1):
        need(row.get("schema") == "cm2.round306c77s.singleton-parent-no-producer-consumer.v1.child-disposition-row" and
             row.get("ordinal") == count, "C77s child schema/order")
        no_credit(row, f"C77s child:{count}", require=("formal_credit", "D02_gate_credit", "whole_parent_credit"))
        need(row.get("global_unresolved_decrement") == 0, f"C77s child global decrement:{count}")
        c65 = row.get("C65_child_row_sha256")
        c71 = row.get("C71b_H1_row_sha256")
        source = row.get("C61_source_row_sha256")
        pair = row.get("pair_index")
        source_path = row.get("source_path")
        need(isinstance(c65, str) and len(c65) == 64 and c65 not in seen_c65,
             f"C77s child identity:{count}")
        seen_c65.add(c65)
        need(pair in PAIR_IDS and isinstance(source, str) and len(source) == 64 and
             isinstance(source_path, str) and row.get("child_path", "").startswith(source_path),
             f"C77s child lineage:{count}")
        identity = (pair, source_path)
        need(source not in source_identity or source_identity[source] == identity,
             f"C77s source identity drift:{count}")
        source_identity[source] = identity
        kind = row.get("C69c_source_kind")
        disposition = row.get("disposition")
        if kind == "BLOCKER":
            need(disposition in ("STRICT_EXCLUSION", "CEMETERY_TANGENCY_TERMINAL") and
                 row.get("terminal_predicate_present") is True and
                 row.get("consuming_oracle") not in (None, "NONE_C71_H1_ONLY") and
                 isinstance(row.get("consuming_oracle_row_sha256"), str),
                 f"C77s blocker terminal:{count}")
            final_disposition = disposition
            source_stats[source]["blocker"] += 1
        else:
            need(kind == "DECISION" and
                 disposition == "RESIDUAL_SEALED_NEXT_DECIDER_REQUIRED" and
                 row.get("terminal_predicate_present") is False and
                 row.get("consuming_oracle") == "NONE_C71_H1_ONLY" and
                 row.get("consuming_oracle_row_sha256") is None and
                 row.get("C72_atlas_row_sha256") is None,
                 f"C77s decision residual:{count}")
            key = (c65, c71)
            need(key in evidence and key not in used, f"C77s/C77d one-to-one join:{count}")
            proof = evidence[key]
            need(proof["C61_source_row_sha256"] == source and
                 proof["pair_index"] == pair and
                 proof["source_path"] == source_path and
                 proof["child_path"] == row.get("child_path"),
                 f"C77s/C77d full lineage join:{count}")
            used.add(key)
            final_disposition = "STRICT_EXCLUSION"
            source_stats[source]["decision"] += 1
        source_stats[source]["total"] += 1
        source_stats[source]["selected_kraft_numerator"] += Fraction(row["parent_volume_fraction"])
        source_stats[source]["strict"] += int(final_disposition == "STRICT_EXCLUSION")
        source_stats[source]["cemetery"] += int(final_disposition == "CEMETERY_TANGENCY_TERMINAL")
        pair_stats[pair]["total"] += 1
        pair_stats[pair]["blocker"] += int(kind == "BLOCKER")
        pair_stats[pair]["decision"] += int(kind == "DECISION")
        pair_stats[pair]["strict"] += int(final_disposition == "STRICT_EXCLUSION")
        pair_stats[pair]["cemetery"] += int(final_disposition == "CEMETERY_TANGENCY_TERMINAL")
        census[(kind + "|" + final_disposition)] += 1
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    actual = {
        "row_count": count,
        "row_hash_line_sequence_sha256": sequence.hexdigest(),
        "sha256": raw_digest(raw), "size": len(raw),
    }
    check_descriptor(result["ledgers"]["child_dispositions"], actual, C77S_CHILD, "C77s children")
    need(count == 167255 and len(seen_c65) == 167255 and len(used) == len(evidence) == 33100,
         "C77s/C77d exhaustive child consumption")
    need(census == {
        "BLOCKER|STRICT_EXCLUSION": 110904,
        "BLOCKER|CEMETERY_TANGENCY_TERMINAL": 23251,
        "DECISION|STRICT_EXCLUSION": 33100,
    }, f"C78s final child census:{census}")
    return {
        "source_stats": source_stats, "pair_stats": pair_stats,
        "source_identity": source_identity, "evidence": evidence,
        "descriptor": actual, "census": census,
    }


def validate_c77s_sources(raw: bytes, result: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    source_stats = state["source_stats"]
    source_identity = state["source_identity"]
    seen: set[str] = set()
    sequence = hashlib.sha256()
    kind_census: Counter[str] = Counter()
    count = 0
    for count, row in enumerate(iter_rows(raw, "C77s source rollups"), 1):
        need(row.get("schema") == "cm2.round306c77s.singleton-parent-no-producer-consumer.v1.source-rollup-row" and
             row.get("ordinal") == count, "C77s source schema/order")
        no_credit(row, f"C77s source:{count}", require=("formal_credit", "D02_gate_credit", "whole_parent_credit"))
        key = row.get("C61_source_row_sha256")
        need(isinstance(key, str) and key not in seen, f"C77s source duplicate:{count}")
        seen.add(key)
        stats = source_stats[key]
        need((row["pair_index"], row["source_path"]) == source_identity.get(key, (row["pair_index"], row["source_path"])),
             f"C77s source/child identity:{count}")
        need(row.get("selected_collision2_child_count") == stats["total"] and
             row.get("selected_blocker_terminal_child_count") == stats["blocker"] and
             row.get("selected_decision_residual_child_count") == stats["decision"] and
             Fraction(row["selected_child_Kraft"]) == stats["selected_kraft_numerator"] and
             Fraction(row["C65_strict_terminal_carry_Kraft"]) + Fraction(row["selected_child_Kraft"]) == Fraction(row["full_source_Kraft"]) and
             row.get("source_prefix_free_and_Kraft_closed") is True,
             f"C77s source rollup certificate:{count}")
        kind = row.get("C69c_source_kind")
        need(kind in ("BLOCKER", "DECISION"), f"C77s source kind:{count}")
        need((kind == "BLOCKER") == (stats["decision"] == 0) and
             row.get("whole_source_terminal") is (kind == "BLOCKER") and
             (row.get("residual_reason") is None) is (kind == "BLOCKER"),
             f"C77s source prior terminal state:{count}")
        kind_census[kind] += 1
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    actual = {
        "row_count": count,
        "row_hash_line_sequence_sha256": sequence.hexdigest(),
        "sha256": raw_digest(raw), "size": len(raw),
    }
    check_descriptor(result["ledgers"]["source_rollups"], actual, C77S_SOURCE, "C77s sources")
    need(count == 20879 and kind_census == {"BLOCKER": 18523, "DECISION": 2356} and
         set(source_stats).issubset(seen), "C77s exact source scope")
    return {"descriptor": actual, "kind_census": kind_census, "seen": seen}


def validate_c77s_pairs(raw: bytes, result: dict[str, Any], state: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    pair_stats = state["pair_stats"]
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    enum_census: Counter[str] = Counter()
    for ordinal, row in enumerate(iter_rows(raw, "C77s pair rollups"), 1):
        need(row.get("schema") == "cm2.round306c77s.singleton-parent-no-producer-consumer.v1.pair-rollup-row" and
             row.get("pair_index") == PAIR_IDS[ordinal - 1], "C77s pair schema/order")
        no_credit(row, f"C77s pair:{ordinal}", require=("formal_credit", "D02_gate_credit", "whole_parent_credit"))
        pair = row["pair_index"]
        stats = pair_stats[pair]
        need(row.get("reflection_cell_count") == 2 and
             row.get("parent_prefix_free") is True and row.get("parent_Kraft") == "1" and
             row.get("blocker_terminal_child_count") == stats["blocker"] and
             row.get("cemetery_graph_child_count") == stats["cemetery"] and
             row.get("decision_residual_child_count") == stats["decision"] and
             row.get("whole_reflection_pair_terminal") is (stats["decision"] == 0),
             f"C77s pair terminal certificate:{pair}")
        need(sum(Fraction(row[name]) for name in (
            "C57_strict_terminal_carry_Kraft", "C58_strict_terminal_carry_Kraft",
            "C61_strict_terminal_carry_Kraft", "C65_replacement_Kraft",
        )) == 1, f"C77s pair four-layer Kraft:{pair}")
        need(sum(row[name] for name in (
            "C57_strict_terminal_carry_leaf_count", "C58_strict_terminal_carry_leaf_count",
            "C61_strict_terminal_carry_leaf_count", "C65_replacement_leaf_count",
        )) == row["final_prefix_leaf_count"], f"C77s pair four-layer count:{pair}")
        terminal_enum = derive_terminal_enum(stats["cemetery"])
        enum_census[terminal_enum] += 1
        rows.append(row)
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    actual = {
        "row_count": len(rows),
        "row_hash_line_sequence_sha256": sequence.hexdigest(),
        "sha256": raw_digest(raw), "size": len(raw),
    }
    check_descriptor(result["ledgers"]["reflection_pair_rollups"], actual, C77S_PAIR, "C77s pairs")
    need(len(rows) == 12 and enum_census == {
        "STRICT_EXCLUSION_ONLY": 7,
        "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": 5,
    }, f"derived pair enum census:{enum_census}")
    return rows, dict(sorted(enum_census.items()))


def validate_c77s_cells(raw: bytes, result: dict[str, Any], state: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    pair_stats = state["pair_stats"]
    rows: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    by_pair: Counter[int] = Counter()
    component_indexes: set[int] = set()
    enum_census: Counter[str] = Counter()
    sequence = hashlib.sha256()
    for ordinal, row in enumerate(iter_rows(raw, "C77s cell rollups"), 1):
        need(row.get("schema") == "cm2.round306c77s.singleton-parent-no-producer-consumer.v1.singleton-cell-rollup-row",
             f"C77s cell schema:{ordinal}")
        no_credit(row, f"C77s cell:{ordinal}", require=("formal_credit", "D02_gate_credit", "whole_parent_credit"))
        need(row.get("candidate_public_unresolved_decrement") == 0,
             f"C77s cell global decrement:{ordinal}")
        pair = row.get("pair_index")
        stats = pair_stats[pair]
        need(pair in PAIR_IDS and row.get("blocker_terminal_child_count_on_reflection_pair") == stats["blocker"] and
             row.get("decision_residual_child_count_on_reflection_pair") == stats["decision"] and
             row.get("candidate_whole_cell_terminal") is (stats["decision"] == 0),
             f"C77s cell prior rollup:{ordinal}")
        cell_id = row.get("cell_id")
        component_index = row.get("component_index")
        need(isinstance(cell_id, str) and cell_id not in by_id and
             isinstance(component_index, int) and component_index not in component_indexes,
             f"C77s cell identity:{ordinal}")
        by_id[cell_id] = row
        component_indexes.add(component_index)
        by_pair[pair] += 1
        enum_census[derive_terminal_enum(stats["cemetery"])] += 1
        rows.append(row)
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    actual = {
        "row_count": len(rows),
        "row_hash_line_sequence_sha256": sequence.hexdigest(),
        "sha256": raw_digest(raw), "size": len(raw),
    }
    check_descriptor(result["ledgers"]["singleton_cell_rollups"], actual, C77S_CELL, "C77s cells")
    need(len(rows) == 24 and set(component_indexes) == set(range(2, 26)) and
         by_pair == {pair: 2 for pair in PAIR_IDS}, "C77s 24 cells/12 pairs/global indexes")
    for row in rows:
        partner = by_id.get(row["reflection_partner_cell_id"])
        need(partner is not None and partner["reflection_partner_cell_id"] == row["cell_id"] and
             partner["pair_index"] == row["pair_index"], "C77s reflection bijection")
    need(enum_census == {
        "STRICT_EXCLUSION_ONLY": 14,
        "STRICT_EXCLUSION_PLUS_CEMETERY_TANGENCY": 10,
    }, f"derived cell enum census:{enum_census}")
    return rows, dict(sorted(enum_census.items()))


def validate_contract() -> dict[str, Any]:
    contract = parse_json(stable_local(CONTRACT_REL, CONTRACT_FILE_PIN), "C78s contract")
    need(isinstance(contract, dict) and contract.get("object_sha256") == CONTRACT_OBJECT_PIN,
         "C78s contract object pin")
    roles = contract.get("authority_roles", {})
    terminal = roles.get("terminal_disposition_authority", {})
    overlay = roles.get("overlay_identity_authority", {})
    need(terminal.get("exclusive_sources") == [
        "INDEPENDENTLY_VERIFIED_SEALED_C77S_DUAL_BUNDLE",
        "INDEPENDENTLY_VERIFIED_SEALED_C77D_DUAL_BUNDLE",
    ] and terminal.get("C55A_may_supply_terminal_evidence") is False,
         "contract terminal authority separation")
    need(overlay.get("exclusive_source") == "PINNED_AND_INDEPENDENTLY_VERIFIED_C55A_LEAF_LEDGER" and
         overlay.get("permitted_fields") == [
             "leaf_ordinal", "cell_id", "row_sha256", "pair_index",
             "component_index", "component_ref", "reflection_partner_cell_id",
         ] and overlay.get("may_modify_or_supply_terminal_disposition") is False,
         "contract C55A identity-only role")
    need(contract.get("projection_policy", {}).get("row_order") == "C55A_LEAF_ORDINAL_ASCENDING" and
         contract.get("projection_policy", {}).get("terminal_enum_is_derived_only_from_actual_C77s_C77d_cemetery_child_count") is True and
         contract.get("projection_policy", {}).get("candidate_public_unresolved_decrement") == 0 and
         contract.get("projection_policy", {}).get("conditional_projection_installed") is False,
         "contract projection boundary")
    need(contract.get("branch_projection_semantics") == {
        "singleton_branch_unresolved": 0,
        "public_global_unresolved_before": 1148,
        "public_global_unresolved_after_branch": 1124,
        "public_global_unresolved_zero": False,
        "projection_target": "C79G_ATOMIC_MERGE",
        "installed_canonical_state": False,
        "global_zero_claim_forbidden": True,
    }, "contract branch projection/global-zero boundary")
    need(contract.get("credit_boundary") == {
        "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
        "whole_parent_credit": 0, "global_installed_credit": 0,
    } and contract.get("canonical_write_policy") == {
        "canonical_pointer_or_seal_writes": False,
        "append_only_candidate_output_only": True,
    }, "contract zero-credit/canonical-write boundary")
    need(contract.get("required_independent_verifier_attacks") == [
        "C55A_IDENTITY_SUBSTITUTION_MUST_FAIL_CLOSED",
        "C55A_AS_TERMINAL_AUTHORITY_PROMOTION_MUST_FAIL_CLOSED",
        "PUBLIC_GLOBAL_UNRESOLVED_ZERO_INFLATION_MUST_FAIL_CLOSED",
    ], "contract required C55A verifier attacks")
    return contract


def load_c55a_overlay_identity(cell_rows: list[dict[str, Any]]) -> dict[str, Any]:
    raw = {rel: stable_local(rel, pin) for rel, pin in C55A_PINS.items()}
    manifest_order, manifest = manifest_entries(
        raw[C55A_MANIFEST_REL], "C55A manifest", allow_relative_paths=True
    )
    required_manifest_members = {
        C55A_LEDGER_REL: C55A_PINS[C55A_LEDGER_REL],
        C55A_RESULT_REL: C55A_PINS[C55A_RESULT_REL],
        C55A_VERIFY_REL: C55A_PINS[C55A_VERIFY_REL],
    }
    need(all(manifest.get(name) == pin for name, pin in required_manifest_members.items()),
         "C55A manifest pins identity inputs")
    need(len(manifest_order) == len(manifest) and
         "deliverables/cm2_round306c55a_four_chart_fundamental_domain_bnb_v1.py" in manifest and
         "deliverables/cm2_round306c55a_four_chart_fundamental_domain_bnb_independent_verifier_v1.py" in manifest,
         "C55A full publication manifest syntax")

    result = parse_json(raw[C55A_RESULT_REL], "C55A result")
    verification = parse_json(raw[C55A_VERIFY_REL], "C55A independent verification")
    ledger = parse_json(raw[C55A_LEDGER_REL], "C55A leaf ledger")
    need(all(isinstance(value, dict) for value in (result, verification, ledger)),
         "C55A identity object universe")
    need(result.get("object_sha256") == C55A_RESULT_OBJECT_PIN and
         verification.get("object_sha256") == C55A_VERIFY_OBJECT_PIN and
         ledger.get("object_sha256") == C55A_LEDGER_OBJECT_PIN,
         "C55A exact object pins")
    need(result.get("schema") == "cm2.round306c55a.four-chart-fundamental-domain-bnb.v1.result" and
         result.get("bnb", {}).get("leaf_count") == 76832 and
         result.get("bnb", {}).get("remaining_unresolved_leaf_count") == 1148 and
         result.get("bnb", {}).get("unresolved_zero") is False and
         result.get("bnb", {}).get("leaf_ledger_file_sha256") == C55A_PINS[C55A_LEDGER_REL] and
         result.get("bnb", {}).get("leaf_ledger_object_sha256") == ledger.get("object_sha256"),
         "C55A result/ledger identity closure")
    need(result.get("formal_credit") == {
        "D02_gate_credit": 0, "formal_credit": 0,
        "source_grazing_or_cemetery_new_credit": 0,
    }, "C55A result zero credit")
    need(verification.get("schema") == "cm2.round306c55a.four-chart-fundamental-domain-bnb.independent-verification.v1" and
         verification.get("attacks") == {"executed": 8, "rejected": 8} and
         verification.get("census", {}).get("total") == 76832 and
         verification.get("census", {}).get("UNRESOLVED_R1648_CONTINUATION") == 1148 and
         verification.get("census", {}).get("unresolved_zero") is False and
         verification.get("independence", {}).get("C55A_producer_executed") is False and
         verification.get("independence", {}).get("C55A_producer_imported") is False,
         "C55A independent verification closure")
    need(ledger.get("schema") == "cm2.round306c55a.four-chart-fundamental-domain-bnb.v1.leaf-ledger" and
         ledger.get("leaf_order") == "C32_LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY" and
         ledger.get("proof_policy", {}).get("null_disposition_rule") ==
             "terminal_disposition_is_null_iff_unresolved_reason_is_nonempty",
         "C55A leaf-ledger policy")

    target_by_cell = {row["cell_id"]: row for row in cell_rows}
    need(len(target_by_cell) == 24, "C55A target cell identity set")
    selected: dict[str, dict[str, Any]] = {}
    exact_filter_cells: set[str] = set()
    full_sequence = hashlib.sha256()
    census: Counter[str] = Counter()
    leaves = ledger.get("leaves")
    need(isinstance(leaves, list) and len(leaves) == 76832, "C55A 76832 leaf array")
    for ordinal, leaf in enumerate(leaves):
        need(isinstance(leaf, dict) and
             leaf.get("schema") == "cm2.round306c55a.four-chart-fundamental-domain-bnb.v1.leaf" and
             leaf.get("leaf_ordinal") == ordinal and isinstance(leaf.get("row_sha256"), str),
             f"C55A leaf schema/order:{ordinal}")
        body = dict(leaf)
        row_hash = body.pop("row_sha256")
        need(row_hash == raw_digest(canonical(body)), f"C55A leaf row hash:{ordinal}")
        full_sequence.update((row_hash + "\n").encode("ascii"))
        terminal_disposition = leaf.get("terminal_disposition")
        unresolved_reason = leaf.get("unresolved_reason")
        need((terminal_disposition is None) == bool(unresolved_reason),
             f"C55A null disposition rule:{ordinal}")
        census[terminal_disposition or "UNRESOLVED_R1648_CONTINUATION"] += 1
        cell_id = leaf.get("cell_id")
        candidate_component = leaf.get("component_ref")
        exact_overlay_filter = (
            terminal_disposition is None and isinstance(candidate_component, dict) and
            isinstance(candidate_component.get("component_index"), int) and
            candidate_component["component_index"] >= 2
        )
        if cell_id in target_by_cell:
            need(exact_overlay_filter, f"C55A target misses exact overlay filter:{cell_id}")
        if not exact_overlay_filter:
            continue
        need(cell_id in target_by_cell and cell_id not in exact_filter_cells,
             f"C55A exact overlay filter scope:{cell_id}")
        exact_filter_cells.add(cell_id)
        need(cell_id not in selected, f"C55A duplicate singleton identity:{cell_id}")
        cell = target_by_cell[cell_id]
        component_ref = leaf.get("component_ref")
        reflection_ref = leaf.get("reflection_pair_ref")
        need(isinstance(component_ref, dict) and set(component_ref) == {
            "cell_role", "component_id", "component_index", "component_row_sha256",
        } and isinstance(reflection_ref, dict), f"C55A singleton identity objects:{cell_id}")
        identity = {
            "leaf_ordinal": leaf["leaf_ordinal"],
            "cell_id": cell_id,
            "row_sha256": row_hash,
            "pair_index": reflection_ref.get("pair_index"),
            "component_index": component_ref.get("component_index"),
            "component_ref": component_ref,
            "reflection_partner_cell_id": reflection_ref.get("partner_cell_id"),
            "previous_terminal_disposition": terminal_disposition,
            "previous_unresolved_reason": unresolved_reason,
        }
        need(identity["pair_index"] == cell["pair_index"] and
             identity["component_index"] == cell["component_index"] and
             component_ref.get("component_id") == cell["component_id"] and
             identity["reflection_partner_cell_id"] == cell["reflection_partner_cell_id"] and
             leaf.get("origin_key") == cell["origin_key"],
             f"C55A/C77s exact singleton identity join:{cell_id}")
        need(terminal_disposition is None and isinstance(unresolved_reason, str) and
             unresolved_reason.startswith("C55A_GLOBAL_DECIDER_BLOCKED:"),
             f"C55A selected row is exact old unresolved row:{cell_id}")
        selected[cell_id] = identity
    expected_census = dict(ledger["census"])
    expected_census.pop("total")
    expected_census.pop("unresolved_zero")
    need(all(census[key] == value for key, value in expected_census.items()) and
         set(census).issubset(expected_census), "C55A full leaf disposition census")
    need(exact_filter_cells == set(target_by_cell) == set(selected) and len(selected) == 24,
         "C55A exact null-disposition/component-index>=2 filter and C77s one-to-one join")
    ordered = sorted(selected.values(), key=lambda item: item["leaf_ordinal"])
    selected_sequence = raw_digest("".join(
        item["row_sha256"] + "\n" for item in ordered
    ).encode("ascii"))
    need(selected_sequence == C55A_OVERLAY_ROW_HASH_SEQUENCE_PIN,
         "C55A exact 24-row leaf-order hash sequence")
    return {
        "by_cell": selected,
        "file_sha256": C55A_PINS[C55A_LEDGER_REL],
        "object_sha256": ledger["object_sha256"],
        "full_leaf_count": len(leaves),
        "full_leaf_row_hash_line_sequence_sha256": full_sequence.hexdigest(),
        "selected_row_count": len(selected),
        "selected_leaf_ordinal_order": [item["leaf_ordinal"] for item in ordered],
        "selected_row_hash_line_sequence_sha256": selected_sequence,
        "terminal_authority": False,
        "role": "OVERLAY_IDENTITY_ONLY",
    }


def output_child_rows(raw: bytes, state: dict[str, Any]) -> Iterator[dict[str, Any]]:
    evidence = state["evidence"]
    for row in iter_rows(raw, "C77s child dispositions replay"):
        kind = row["C69c_source_kind"]
        if kind == "DECISION":
            proof = evidence[(row["C65_child_row_sha256"], row["C71b_H1_row_sha256"])]
            disposition = "STRICT_EXCLUSION"
            consumer = "C77D_EXACT_ROUTE_STRICT_EXCLUSION"
            consumer_row = proof["row_sha256"]
            route_outcome = proof["route_outcome"]
            geometry_kind = proof["fresh_geometry_kind"]
            glue_kind = proof["physical_chart_glue_kind"]
            decision_consumed = True
        else:
            disposition = row["disposition"]
            consumer = row["consuming_oracle"]
            consumer_row = row["consuming_oracle_row_sha256"]
            route_outcome = None
            geometry_kind = None
            glue_kind = None
            decision_consumed = False
        yield add_row_hash({
            "schema": SCHEMA + ".child-disposition-row",
            "ordinal": row["ordinal"],
            "pair_index": row["pair_index"],
            "source_path": row["source_path"],
            "child_path": row["child_path"],
            "parent_volume_fraction": row["parent_volume_fraction"],
            "C61_source_row_sha256": row["C61_source_row_sha256"],
            "C65_child_row_sha256": row["C65_child_row_sha256"],
            "C71b_H1_row_sha256": row["C71b_H1_row_sha256"],
            "C77s_child_disposition_row_sha256": row["row_sha256"],
            "C69c_source_kind": kind,
            "C72_atlas_row_sha256": row["C72_atlas_row_sha256"],
            "previous_C77s_disposition": row["disposition"],
            "consuming_oracle": consumer,
            "consuming_oracle_row_sha256": consumer_row,
            "C77d_decision_route_row_sha256": consumer_row if kind == "DECISION" else None,
            "C77d_route_outcome": route_outcome,
            "C77d_fresh_geometry_kind": geometry_kind,
            "C77d_physical_chart_glue_kind": glue_kind,
            "decision_residual_consumed_exactly_once": decision_consumed,
            "disposition": disposition,
            "terminal_predicate_present": True,
            "sealed_collision3_handoff_count": 0,
            "explicit_residual_count": 0,
            "candidate_is_authority": False,
            "candidate_public_unresolved_decrement": 0,
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "CM2_credit": 0,
            "whole_parent_credit": 0,
            "global_installed_credit": 0,
        })


def output_source_rows(raw: bytes, state: dict[str, Any]) -> Iterator[dict[str, Any]]:
    stats_by_source = state["source_stats"]
    for row in iter_rows(raw, "C77s source rollups replay"):
        stats = stats_by_source[row["C61_source_row_sha256"]]
        yield add_row_hash({
            "schema": SCHEMA + ".source-rollup-row",
            "ordinal": row["ordinal"],
            "pair_index": row["pair_index"],
            "source_path": row["source_path"],
            "C61_source_row_sha256": row["C61_source_row_sha256"],
            "C65_source_summary_row_sha256": row["C65_source_summary_row_sha256"],
            "C69c_source_row_sha256": row["C69c_source_row_sha256"],
            "C77s_source_rollup_row_sha256": row["row_sha256"],
            "C69c_source_kind": row["C69c_source_kind"],
            "C65_strict_terminal_carry_leaf_count": row["C65_strict_terminal_carry_leaf_count"],
            "selected_collision2_child_count": stats["total"],
            "selected_blocker_terminal_child_count": stats["blocker"],
            "selected_decision_strict_exclusion_child_count": stats["decision"],
            "selected_strict_exclusion_child_count": stats["strict"],
            "selected_cemetery_tangency_terminal_child_count": stats["cemetery"],
            "selected_residual_child_count": 0,
            "selected_collision3_handoff_child_count": 0,
            "selected_child_Kraft": row["selected_child_Kraft"],
            "C65_strict_terminal_carry_Kraft": row["C65_strict_terminal_carry_Kraft"],
            "full_source_Kraft": row["full_source_Kraft"],
            "source_prefix_free_and_Kraft_closed": True,
            "whole_source_terminal": True,
            "terminal_enum": derive_terminal_enum(stats["cemetery"]),
            "candidate_is_authority": False,
            "candidate_public_unresolved_decrement": 0,
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "CM2_credit": 0,
            "whole_parent_credit": 0,
            "global_installed_credit": 0,
        })


def output_pair_rows(rows: list[dict[str, Any]], state: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for ordinal, row in enumerate(rows, 1):
        stats = state["pair_stats"][row["pair_index"]]
        body = {
            "schema": SCHEMA + ".pair-rollup-row",
            "ordinal": ordinal,
            "pair_index": row["pair_index"],
            "reflection_cell_count": 2,
            "C77s_pair_rollup_row_sha256": row["row_sha256"],
        }
        for key in (
            "C69c_source_task_count", "final_prefix_leaf_count",
            "C57_strict_terminal_carry_leaf_count", "C58_strict_terminal_carry_leaf_count",
            "C61_strict_terminal_carry_leaf_count", "C65_replacement_leaf_count",
            "C57_strict_terminal_carry_Kraft", "C58_strict_terminal_carry_Kraft",
            "C61_strict_terminal_carry_Kraft", "C65_replacement_Kraft",
            "frozen_parent_row_sha256",
        ):
            body[key] = row[key]
        body.update({
            "blocker_terminal_child_count": stats["blocker"],
            "decision_strict_exclusion_child_count": stats["decision"],
            "strict_exclusion_child_count": stats["strict"],
            "cemetery_tangency_terminal_child_count": stats["cemetery"],
            "residual_child_count": 0,
            "sealed_collision3_handoff_child_count": 0,
            "parent_prefix_free": True,
            "parent_Kraft": "1",
            "prefix_free_and_exact_Kraft_one_certificate_carried_from_C77s": True,
            "whole_reflection_pair_terminal": True,
            "terminal_enum": derive_terminal_enum(stats["cemetery"]),
            "candidate_is_authority": False,
            "candidate_public_unresolved_decrement": 0,
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "CM2_credit": 0,
            "whole_parent_credit": 0,
            "global_installed_credit": 0,
        })
        yield add_row_hash(body)


def output_cell_rows(rows: list[dict[str, Any]], state: dict[str, Any]) -> Iterator[dict[str, Any]]:
    for ordinal, row in enumerate(rows, 1):
        stats = state["pair_stats"][row["pair_index"]]
        yield add_row_hash({
            "schema": SCHEMA + ".singleton-cell-rollup-row",
            "ordinal": ordinal,
            "component_index": row["component_index"],
            "component_id": row["component_id"],
            "cell_id": row["cell_id"],
            "reflection_partner_cell_id": row["reflection_partner_cell_id"],
            "pair_index": row["pair_index"],
            "origin_key": row["origin_key"],
            "C77s_singleton_cell_rollup_row_sha256": row["row_sha256"],
            "blocker_terminal_child_count_on_reflection_pair": stats["blocker"],
            "decision_strict_exclusion_child_count_on_reflection_pair": stats["decision"],
            "strict_exclusion_child_count_on_reflection_pair": stats["strict"],
            "cemetery_tangency_terminal_child_count_on_reflection_pair": stats["cemetery"],
            "residual_child_count_on_reflection_pair": 0,
            "sealed_collision3_handoff_child_count_on_reflection_pair": 0,
            "whole_cell_terminal": True,
            "terminal_enum": derive_terminal_enum(stats["cemetery"]),
            "candidate_is_authority": False,
            "candidate_public_unresolved_decrement": 0,
            "conditional_future_global_unresolved_decrement_if_atomically_installed": 1,
            "global_projection_installed": False,
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "CM2_credit": 0,
            "whole_parent_credit": 0,
            "global_installed_credit": 0,
        })


def output_projection_rows(
    rows: list[dict[str, Any]], state: dict[str, Any], c55a: dict[str, Any],
) -> Iterator[dict[str, Any]]:
    identities = c55a["by_cell"]
    ordered = sorted(rows, key=lambda item: identities[item["cell_id"]]["leaf_ordinal"])
    for ordinal, row in enumerate(ordered, 1):
        stats = state["pair_stats"][row["pair_index"]]
        identity = identities[row["cell_id"]]
        need(identity["pair_index"] == row["pair_index"] and
             identity["component_index"] == row["component_index"] and
             identity["component_ref"]["component_id"] == row["component_id"] and
             identity["reflection_partner_cell_id"] == row["reflection_partner_cell_id"],
             "C55A identity replay before projection")
        terminal_enum = derive_terminal_enum(stats["cemetery"])
        yield add_row_hash({
            "schema": SCHEMA + ".global-enum-projection-row",
            "ordinal": ordinal,
            "leaf_ordinal": identity["leaf_ordinal"],
            "cell_id": identity["cell_id"],
            "C55A_leaf_row_sha256": identity["row_sha256"],
            "pair_index": identity["pair_index"],
            "component_index": identity["component_index"],
            "component_ref": identity["component_ref"],
            "reflection_partner_cell_id": identity["reflection_partner_cell_id"],
            "C55A_identity": {
                "leaf_ordinal": identity["leaf_ordinal"],
                "cell_id": identity["cell_id"],
                "row_sha256": identity["row_sha256"],
                "pair_index": identity["pair_index"],
                "component_index": identity["component_index"],
                "component_ref": identity["component_ref"],
                "reflection_partner_cell_id": identity["reflection_partner_cell_id"],
            },
            "C77s_cell_rollup_row_sha256": row["row_sha256"],
            "origin_key": row["origin_key"],
            "previous_C55A_terminal_disposition": identity["previous_terminal_disposition"],
            "previous_C55A_unresolved_reason": identity["previous_unresolved_reason"],
            "new_candidate_disposition": "WHOLE_SINGLETON_CELL_TERMINAL",
            "new_terminal_enum": terminal_enum,
            "terminal_enum": terminal_enum,
            "terminal_enum_derived_from_actual_cemetery_child_count": stats["cemetery"],
            "terminal_disposition_authority": [
                "INDEPENDENTLY_VERIFIED_SEALED_C77S_DUAL_BUNDLE",
                "INDEPENDENTLY_VERIFIED_SEALED_C77D_DUAL_BUNDLE",
            ],
            "C55A_role": "OVERLAY_IDENTITY_ONLY_NEVER_TERMINAL_AUTHORITY",
            "whole_singleton_cell_terminal_candidate": True,
            "projection_role": "INPUT_ONLY_FOR_FUTURE_INDEPENDENT_NO_PRODUCER_GLOBAL_CONSUMER",
            "conditional_installation_requirement": "ALL_24_ROWS_MUST_BE_REVALIDATED_AND_ATOMICALLY_INSTALLED_BY_A_FUTURE_GLOBAL_CONSUMER",
            "current_public_global_unresolved_before": 1148,
            "current_candidate_public_unresolved_decrement": 0,
            "current_public_global_unresolved_after": 1148,
            "singleton_branch_unresolved": 0,
            "public_global_unresolved_before": 1148,
            "public_global_unresolved_after_branch": 1124,
            "public_global_unresolved_zero": False,
            "branch_projection_target": "C79G_ATOMIC_MERGE",
            "conditional_future_per_component_decrement_if_atomically_installed": 1,
            "conditional_projected_public_global_unresolved_after_all_24_if_atomically_installed": 1124,
            "global_projection_installed": False,
            "candidate_is_authority": False,
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "CM2_credit": 0,
            "whole_parent_credit": 0,
            "global_installed_credit": 0,
        })


def write_exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o444,
    )
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, f"exclusive write progress:{path.name}")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def stable_output(path: Path, expected: str | None = None) -> bytes:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             f"unsafe output member:{path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
         f"output fd drift:{path}")
    raw = b"".join(chunks)
    if expected is not None:
        need(raw_digest(raw) == expected, f"output terminal replay:{path.name}")
    return raw


def write_gzip_rows(path: Path, rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o444,
    )
    count = 0
    sequence = hashlib.sha256()
    base = os.fdopen(descriptor, "wb", closefd=True)
    try:
        stream = gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=base, mtime=0)
        try:
            for count, row in enumerate(rows, 1):
                need(isinstance(row.get("row_sha256"), str), f"output row hash:{path.name}:{count}")
                body = dict(row)
                row_hash = body.pop("row_sha256")
                need(row_hash == raw_digest(canonical(body)), f"output row closure:{path.name}:{count}")
                stream.write(canonical(row) + b"\n")
                sequence.update((row_hash + "\n").encode("ascii"))
        finally:
            stream.close()
        base.flush()
        os.fsync(base.fileno())
    finally:
        base.close()
    raw = stable_output(path)
    one_gzip_member(raw, "output:" + path.name)
    return {
        "filename": path.name,
        "row_count": count,
        "row_hash_line_sequence_sha256": sequence.hexdigest(),
        "sha256": raw_digest(raw),
        "size": len(raw),
    }


def manifest_raw(pins: dict[str, str], order: Iterable[str]) -> bytes:
    return b"".join(f"{pins[name]}  {name}\n".encode("ascii") for name in order)


def build_report(result: dict[str, Any]) -> bytes:
    lines = [
        "# C78s singleton final no-producer consumer v1",
        "",
        "Status: PASS candidate reconstruction; zero installed credit.",
        "",
        "- Exact sealed inputs: C77s 13-member dual bundle and C77d 9-member dual bundle.",
        "- C55A is pinned identity-only input for the 24-row overlay; it is never terminal authority.",
        "- Every projected row carries its exact C55A leaf ordinal/hash/component/reflection identity and C77s cell-row hash.",
        "- Upstream producer sources opened/read/imported/compiled/executed: no.",
        "- Children: 167,255 = 144,004 strict exclusions + 23,251 cemetery tangencies.",
        "- Decision residuals consumed exactly once: 33,100; residual/C3 handoff: 0/0.",
        "- Sources/pairs/cells terminal: 20,879 / 12 / 24.",
        "- Pair enum census: 7 strict-only, 5 strict-plus-cemetery.",
        "- Cell enum census: 14 strict-only, 10 strict-plus-cemetery.",
        "- Current public unresolved remains 1,148; candidate decrement is 0.",
        "- Singleton-branch unresolved is 0; its C79g branch projection is 1,148 -> 1,124.",
        "- The branch projection is not canonical state, and public-global unresolved-zero is false.",
        "- 1,124 becomes installed only if a future independent global consumer atomically accepts all 24 projection rows.",
        "- Formal/global/D02/CM2/whole-parent credit: all zero.",
        "",
        f"Result object SHA-256: `{result['object_sha256']}`",
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def publish(
    outdir: Path, c77s: dict[str, bytes], c77d: dict[str, bytes],
    state: dict[str, Any], pair_rows: list[dict[str, Any]], cell_rows: list[dict[str, Any]],
    pair_enum_census: dict[str, int], cell_enum_census: dict[str, int],
    s_result: dict[str, Any], d_result: dict[str, Any], incidence: dict[str, Any],
    contract: dict[str, Any], c55a: dict[str, Any],
) -> dict[str, Any]:
    need(not outdir.exists() and outdir.parent.is_dir(), "exclusive new output directory required")
    os.mkdir(outdir, 0o755)
    pins: dict[str, str] = {}

    lock = (
        "C78s candidate only; no public/global/formal/D02/CM2/whole-parent credit.\n"
        "The 24-row global enumeration projection is not installed.\n"
    ).encode("ascii")
    write_exclusive(outdir / OUT_LOCK, lock)
    pins[OUT_LOCK] = raw_digest(lock)

    ledgers = {
        "child_dispositions": write_gzip_rows(outdir / OUT_CHILD, output_child_rows(c77s[C77S_CHILD], state)),
        "source_rollups": write_gzip_rows(outdir / OUT_SOURCE, output_source_rows(c77s[C77S_SOURCE], state)),
        "reflection_pair_rollups": write_gzip_rows(outdir / OUT_PAIR, output_pair_rows(pair_rows, state)),
        "singleton_cell_rollups": write_gzip_rows(outdir / OUT_CELL, output_cell_rows(cell_rows, state)),
        "global_enum_projection": write_gzip_rows(
            outdir / OUT_PROJECTION, output_projection_rows(cell_rows, state, c55a)
        ),
    }
    for descriptor in ledgers.values():
        pins[descriptor["filename"]] = descriptor["sha256"]
    need(ledgers["child_dispositions"]["row_count"] == 167255 and
         ledgers["source_rollups"]["row_count"] == 20879 and
         ledgers["reflection_pair_rollups"]["row_count"] == 12 and
         ledgers["singleton_cell_rollups"]["row_count"] == 24 and
         ledgers["global_enum_projection"]["row_count"] == 24,
         "output ledger census")

    result_body = {
        "schema": SCHEMA + ".result",
        "status": "PASS_EXACT_SEALED_13_PLUS_9_INPUTS__167255_TERMINAL_CHILDREN__33100_DECISION_RESIDUALS_CONSUMED_EXACTLY_ONCE__20879_SOURCES__12_PAIRS__24_CELLS__GLOBAL_PROJECTION_NOT_INSTALLED__ZERO_CREDIT",
        "candidate_is_authority": False,
        "singleton_branch_unresolved": 0,
        "public_global_unresolved_before": 1148,
        "public_global_unresolved_after_branch": 1124,
        "public_global_unresolved_zero": False,
        "branch_projection_target": "C79G_ATOMIC_MERGE",
        "branch_projection_installed_as_canonical_state": False,
        "contract": {
            "file_sha256": CONTRACT_FILE_PIN,
            "object_sha256": contract["object_sha256"],
            "authority_role_separation_closed": True,
        },
        "authority_role_separation": {
            "terminal_disposition_authority_exclusive": [
                "INDEPENDENTLY_VERIFIED_SEALED_C77S_DUAL_BUNDLE",
                "INDEPENDENTLY_VERIFIED_SEALED_C77D_DUAL_BUNDLE",
            ],
            "C55A_role": "OVERLAY_IDENTITY_ONLY",
            "C55A_may_supply_or_modify_terminal_disposition": False,
            "C55A_identity_fields": [
                "leaf_ordinal", "cell_id", "row_sha256", "pair_index",
                "component_index", "component_ref", "reflection_partner_cell_id",
            ],
        },
        "upstream_producer_policy": {
            "C77s_producer": {"opened": False, "read": False, "parsed": False, "decoded": False, "imported": False, "compiled": False, "executed": False},
            "C77d_producer": {"opened": False, "read": False, "parsed": False, "decoded": False, "imported": False, "compiled": False, "executed": False},
        },
        "sealed_dual_inputs": {
            "C77s": {
                "stage_a": str(C77S_A.relative_to(ROOT)),
                "stage_b": str(C77S_B.relative_to(ROOT)),
                "exact_member_count_per_stage": 13,
                "final_manifest_file_sha256": C77S_PINS[C77S_FINAL_MANIFEST],
                "final_outer_receipt_file_sha256": C77S_PINS[C77S_FINAL_OUTER],
                "result_object_sha256": s_result["object_sha256"],
            },
            "C77d": {
                "stage_a": str(C77D_A.relative_to(ROOT)),
                "stage_b": str(C77D_B.relative_to(ROOT)),
                "exact_member_count_per_stage": 9,
                "final_manifest_file_sha256": C77D_PINS[C77D_FINAL_MANIFEST],
                "final_outer_receipt_file_sha256": C77D_PINS[C77D_FINAL_OUTER],
                "result_object_sha256": d_result["object_sha256"],
            },
            "all_22_stage_members_byte_identical_across_duals": True,
            "all_manifests_receipts_objects_rows_and_single_member_gzips_closed": True,
        },
        "C55A_overlay_identity_input": {
            "role": "OVERLAY_IDENTITY_ONLY_NEVER_TERMINAL_AUTHORITY",
            "leaf_ledger_file_sha256": c55a["file_sha256"],
            "leaf_ledger_object_sha256": c55a["object_sha256"],
            "full_leaf_count": c55a["full_leaf_count"],
            "full_leaf_row_hash_line_sequence_sha256": c55a["full_leaf_row_hash_line_sequence_sha256"],
            "matched_singleton_row_count": c55a["selected_row_count"],
            "matched_singleton_leaf_ordinal_order": c55a["selected_leaf_ordinal_order"],
            "matched_singleton_row_hash_line_sequence_sha256": c55a["selected_row_hash_line_sequence_sha256"],
            "result_file_sha256": C55A_PINS[C55A_RESULT_REL],
            "independent_verification_file_sha256": C55A_PINS[C55A_VERIFY_REL],
            "manifest_file_sha256": C55A_PINS[C55A_MANIFEST_REL],
            "one_to_one_old_C55A_row_to_new_projection_disposition": True,
            "terminal_authority": False,
        },
        "partition": {
            "total_children": 167255,
            "blocker_children_preserved": 134155,
            "decision_children_consumed": 33100,
            "identity": "167255=134155+33100",
        },
        "terminal_child_census": {
            "whole_child_strict_exclusion": 144004,
            "cemetery_tangency_terminal": 23251,
            "sealed_collision3_handoff": 0,
            "explicit_residual": 0,
            "identity": "167255=144004+23251",
        },
        "C77d_consumption": {
            "available_decision_rows": 33100,
            "consumed_exactly_once": 33100,
            "unconsumed": 0,
            "duplicate_consumption": 0,
            "join_key": ["C65_child_row_sha256", "C71b_H1_row_sha256"],
            "additional_exact_matches": ["C61_source_row_sha256", "pair_index", "source_path", "child_path"],
        },
        "sources": {"total": 20879, "whole_terminal": 20879, "residual": 0},
        "reflection_pairs": {
            "total": 12, "whole_terminal": 12, "residual": 0,
            "prefix_free_and_exact_Kraft_one_certificates_carried": 12,
            "terminal_enum_census": pair_enum_census,
        },
        "singleton_cells": {
            "total": 24, "whole_terminal": 24, "residual": 0,
            "terminal_enum_census": cell_enum_census,
        },
        "global_enum_projection": {
            "row_count": 24,
            "row_order": "C55A_LEAF_ORDINAL_ASCENDING",
            "row_hash_line_sequence_sha256": ledgers["global_enum_projection"]["row_hash_line_sequence_sha256"],
            "role": "CANDIDATE_INPUT_ONLY_FOR_FUTURE_INDEPENDENT_NO_PRODUCER_GLOBAL_CONSUMER",
            "installed": False,
            "atomic_installation_required": "24_OF_24",
        },
        "public_global_unresolved": {
            "current_before": 1148,
            "current_candidate_decrement": 0,
            "current_after": 1148,
            "conditional_projection": {
                "condition": "ONLY_IF_A_FUTURE_INDEPENDENT_NO_PRODUCER_GLOBAL_CONSUMER_REVALIDATES_AND_ATOMICALLY_INSTALLS_ALL_24_PROJECTION_ROWS",
                "projected_decrement": 24,
                "projected_after": 1124,
                "installed": False,
            },
        },
        "C77d_root_incidence_validated": {
            "unique_root_count": incidence["row_count"],
            "endpoint_occurrence_count": incidence["endpoint_occurrence_count"],
            "degree_census": incidence["degree_census"],
        },
        "ledgers": ledgers,
        "canonical_pointer_or_seal_written": False,
        "runtime_canonical_pointer_or_seal_writes": False,
        "credit_boundary": {
            "formal_credit": 0, "D02_gate_credit": 0, "CM2_credit": 0,
            "whole_parent_credit": 0, "global_installed_credit": 0,
        },
        "producer_file_sha256": raw_digest(Path(__file__).read_bytes()),
    }
    result = add_object_hash(result_body)
    result_raw = canonical(result) + b"\n"
    write_exclusive(outdir / OUT_RESULT, result_raw)
    pins[OUT_RESULT] = raw_digest(result_raw)

    report_raw = build_report(result)
    write_exclusive(outdir / OUT_REPORT, report_raw)
    pins[OUT_REPORT] = raw_digest(report_raw)

    need(tuple(pins) == OUT_MEMBER_ORDER, "output base member construction order")
    manifest = manifest_raw(pins, OUT_MEMBER_ORDER)
    write_exclusive(outdir / OUT_MANIFEST, manifest)
    pins[OUT_MANIFEST] = raw_digest(manifest)

    outer_body = {
        "schema": SCHEMA + ".outer-receipt",
        "status": "PASS_APPEND_ONLY_EXACT_SEALED_INPUT_CONSUMER__OUTER_LAST__TERMINAL_BYTE_REPLAY__GLOBAL_PROJECTION_NOT_INSTALLED__ZERO_CREDIT",
        "candidate_is_authority": False,
        "manifest_filename": OUT_MANIFEST,
        "manifest_file_sha256": pins[OUT_MANIFEST],
        "manifest_member_count": len(OUT_MEMBER_ORDER),
        "manifest_member_order": list(OUT_MEMBER_ORDER),
        "result_object_sha256": result["object_sha256"],
        "outer_receipt_published_last": True,
        "terminal_byte_replay_member_count": len(OUT_UNIVERSE),
        "all_members_terminal_byte_replayed": True,
        "current_public_global_unresolved": 1148,
        "candidate_public_unresolved_decrement": 0,
        "singleton_branch_unresolved": 0,
        "public_global_unresolved_before": 1148,
        "public_global_unresolved_after_branch": 1124,
        "public_global_unresolved_zero": False,
        "branch_projection_target": "C79G_ATOMIC_MERGE",
        "conditional_projected_future_public_global_unresolved": 1124,
        "conditional_projection_installed": False,
        "canonical_pointer_or_seal_written": False,
        "formal_credit": 0,
        "D02_gate_credit": 0,
        "CM2_credit": 0,
        "whole_parent_credit": 0,
        "global_installed_credit": 0,
    }
    outer = add_object_hash(outer_body)
    outer_raw = canonical(outer) + b"\n"
    # This is intentionally the final creation in the candidate directory.
    write_exclusive(outdir / OUT_OUTER, outer_raw)
    pins[OUT_OUTER] = raw_digest(outer_raw)

    need(set(os.listdir(outdir)) == set(OUT_UNIVERSE), "output exact 10-member universe")
    need(tuple(pins) == OUT_UNIVERSE, "output creation order")
    for name in OUT_UNIVERSE:
        stable_output(outdir / name, pins[name])
    os.chmod(outdir, 0o555)
    return {
        "status": "PASS",
        "output_dir": str(outdir),
        "result_file_sha256": pins[OUT_RESULT],
        "result_object_sha256": result["object_sha256"],
        "manifest_file_sha256": pins[OUT_MANIFEST],
        "outer_file_sha256": pins[OUT_OUTER],
        "outer_object_sha256": outer["object_sha256"],
        "member_count": len(OUT_UNIVERSE),
        "candidate_public_unresolved_decrement": 0,
        "current_public_global_unresolved": 1148,
        "conditional_projected_future_public_global_unresolved": 1124,
        "conditional_projection_installed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--outdir")
    mode.add_argument("--preflight-only", action="store_true")
    arguments = parser.parse_args()
    outdir: Path | None = None
    if arguments.outdir is not None:
        outdir = Path(arguments.outdir)
        if not outdir.is_absolute():
            outdir = ROOT / outdir

    # Placeholder rejection precedes every stage read and every output write.
    ensure_no_placeholders()
    contract = validate_contract()
    c77s = load_dual_bundle(
        "C77s", C77S_A, C77S_B, C77S_PINS,
        C77S_MANIFEST, C77S_BASE_ORDER,
        C77S_FINAL_MANIFEST, C77S_FINAL_OUTER, C77S_FINAL_ORDER,
    )
    c77d = load_dual_bundle(
        "C77d", C77D_A, C77D_B, C77D_PINS,
        C77D_MANIFEST, C77D_BASE_ORDER,
        C77D_FINAL_MANIFEST, C77D_FINAL_OUTER, C77D_FINAL_ORDER,
    )
    s_result, d_result = validate_input_objects(c77s, c77d)
    evidence, _ = validate_c77d_rows(c77d[C77D_ROWS], d_result)
    incidence = validate_c77d_incidence(c77d[C77D_INCIDENCE], d_result)
    state = validate_c77s_children(c77s[C77S_CHILD], s_result, evidence)
    source_validation = validate_c77s_sources(c77s[C77S_SOURCE], s_result, state)
    pair_rows, pair_enum_census = validate_c77s_pairs(c77s[C77S_PAIR], s_result, state)
    cell_rows, cell_enum_census = validate_c77s_cells(c77s[C77S_CELL], s_result, state)
    c55a = load_c55a_overlay_identity(cell_rows)
    if arguments.preflight_only:
        print(canonical({
            "schema": SCHEMA + ".preflight-only.v1",
            "status": "PASS_FULL_NO_WRITE_PREFLIGHT__33100_EXACT_JOIN__167255_TERMINAL_CHILDREN__20879_SOURCES__12_PAIRS__24_CELLS__24_C55A_IDENTITIES__ZERO_CREDIT",
            "output_created": False,
            "contract_file_sha256": CONTRACT_FILE_PIN,
            "contract_object_sha256": contract["object_sha256"],
            "C77s_exact_dual_member_count": 13,
            "C77d_exact_dual_member_count": 9,
            "C77d_decision_rows_joined_exactly_once": 33100,
            "terminal_child_census": {
                "STRICT_EXCLUSION": 144004,
                "CEMETERY_TANGENCY_TERMINAL": 23251,
                "RESIDUAL": 0,
                "SEALED_COLLISION3_HANDOFF": 0,
            },
            "source_count": len(source_validation["seen"]),
            "whole_terminal_source_count": 20879,
            "pair_count": len(pair_rows),
            "whole_terminal_pair_count": 12,
            "pair_terminal_enum_census": pair_enum_census,
            "cell_count": len(cell_rows),
            "whole_terminal_cell_count": 24,
            "cell_terminal_enum_census": cell_enum_census,
            "C55A_overlay_identity_row_count": c55a["selected_row_count"],
            "C55A_selected_row_hash_line_sequence_sha256": c55a["selected_row_hash_line_sequence_sha256"],
            "singleton_branch_unresolved": 0,
            "public_global_unresolved_before": 1148,
            "public_global_unresolved_after_branch": 1124,
            "public_global_unresolved_zero": False,
            "branch_projection_target": "C79G_ATOMIC_MERGE",
            "branch_projection_installed_as_canonical_state": False,
            "candidate_public_unresolved_decrement": 0,
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "CM2_credit": 0,
            "whole_parent_credit": 0,
            "global_installed_credit": 0,
        }).decode("utf-8"))
        return
    need(outdir is not None, "build mode requires --outdir")
    completion = publish(
        outdir, c77s, c77d, state, pair_rows, cell_rows,
        pair_enum_census, cell_enum_census, s_result, d_result, incidence,
        contract, c55a,
    )
    print(canonical(completion).decode("utf-8"))


if __name__ == "__main__":
    main()
