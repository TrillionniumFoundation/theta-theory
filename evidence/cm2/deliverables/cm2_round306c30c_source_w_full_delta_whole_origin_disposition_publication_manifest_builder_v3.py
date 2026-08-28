#!/usr/bin/env python3
"""Build the C30c v3 payload and root manifests before outer verification.

The root is deliberately non-self-referential: it pins the exact payload
manifest and the exact Round306C30b authority.  The later terminal seal pins
the independent outer verification.  This stage grants zero formal credit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT = WORKSPACE / ".cm2-runtime/audit"
RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260808T0635Z-receipt-v3"
BRIDGE_NAME = "c30c-postreceipt-v3-p1-bridge-v1-20260808T0655Z"
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
C30B_MANIFEST_REL = (
    "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_"
    "disposition_manifest.sha256"
)
C30B_MANIFEST_SHA256 = "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248"
EXPECTED_BUNDLE_STATUS = (
    "PASS_EXACT_V3_TRANSACTION_AND_BRIDGE_EVIDENCE_BUNDLED__ZERO_FORMAL_CREDIT"
)
SCRIPT_NAMES = (
    PREFIX + "_audit_evidence_bundle_builder_v3.py",
    PREFIX + "_publication_manifest_builder_v3.py",
    PREFIX + "_formal_handoff_outer_verifier_v3.py",
    PREFIX + "_terminal_seal_replay_v3.py",
    "cm2_round306c30c_publication_static_consistency_gate_v3.py",
    "cm2_round306c30c_postreceipt_v3_publication_chain_watch_v1.py",
)
CANDIDATE_FILES = (
    "cm2_round306c30b_python_flint_runtime_attestation.json",
    PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz",
    PREFIX + "_delta_h_cell_ledger.jsonl.gz",
    PREFIX + "_inherited_h_cell_ledger.jsonl.gz",
    PREFIX + "_result.json",
    PREFIX + "_whole_origin_ledger.jsonl.gz",
)


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def capture(path: Path, maximum: int = 64 << 30) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + os.fspath(path))
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
             0 <= before.st_size <= maximum, "bounded singleton:" + os.fspath(path))
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(4 << 20, remaining))
            need(bool(block), "complete read:" + os.fspath(path))
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "stable EOF:" + os.fspath(path))
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after), "stable capture:" + os.fspath(path))
    return b"".join(chunks)


def sha(path: Path) -> str:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical hash path:" + os.fspath(path))
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "hash singleton:" + os.fspath(path))
        state = hashlib.sha256()
        total = 0
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
            total += len(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after) and total == before.st_size,
         "stable hash:" + os.fspath(path))
    return state.hexdigest()


def strict_object(path: Path, label: str) -> dict[str, Any]:
    raw = capture(path, 16 << 20)
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(type(key) is str and key not in output, "unique key:" + label)
            output[key] = value
        return output
    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=unique,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Blocked("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical JSON:" + label)
    return value


def parse_manifest(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    try:
        lines = capture(path, 4 << 20).decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Blocked("ASCII manifest:" + path.name) from error
    for line in lines:
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64 and
             all(c in "0123456789abcdef" for c in pieces[0]) and pieces[1] and
             not Path(pieces[1]).is_absolute() and ".." not in Path(pieces[1]).parts and
             pieces[1] not in rows, "manifest syntax:" + path.name)
        rows[pieces[1]] = pieces[0]
    return rows


def exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o400)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(descriptor, view)
            need(count > 0, "complete write:" + path.name)
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def payload_paths(chain_dir: Path) -> dict[str, Path]:
    c30b_manifest = WORKSPACE / C30B_MANIFEST_REL
    need(sha(c30b_manifest) == C30B_MANIFEST_SHA256, "exact Round306C30b manifest")
    c30b_rows = parse_manifest(c30b_manifest)
    need(len(c30b_rows) == 14, "Round306C30b 14-member authority")
    paths = {C30B_MANIFEST_REL: c30b_manifest}
    for relative, expected in c30b_rows.items():
        path = DELIVERABLES / relative
        need(sha(path) == expected, "Round306C30b member:" + relative)
        paths["deliverables/" + relative] = path
    for script in SCRIPT_NAMES:
        paths["deliverables/" + script] = DELIVERABLES / script
    for name in (
        "cm2_round306c30c_62_attack_run_receipt_validator_v3.py",
        "cm2_round306c30c_postreceipt_v3_p1_bridge_watch_v1.py",
        PREFIX + "_independent_verifier.py",
        PREFIX + "_attack_harness.py",
        PREFIX + "_cold_trace_analyzer.py",
        "cm2_round306c30c_cold_trace_unfinished_pairing_attack_gate.py",
    ):
        paths["deliverables/" + name] = DELIVERABLES / name
    for seed in ("30630071", "30630929"):
        base = WORKSPACE / ".cm2-runtime/candidates" / ("c30c-v4-seed-" + seed)
        for name in CANDIDATE_FILES:
            relative = ".cm2-runtime/candidates/c30c-v4-seed-" + seed + "/" + name
            paths[relative] = base / name
    raw_roots = {
        ".cm2-runtime/receipts/" + RUN_NAME + "/receipt.json":
            WORKSPACE / ".cm2-runtime/receipts" / RUN_NAME / "receipt.json",
        ".cm2-runtime/audit/" + BRIDGE_NAME + "/terminal_status.json":
            AUDIT / BRIDGE_NAME / "terminal_status.json",
        ".cm2-runtime/audit/" + BRIDGE_NAME + "/receipt_gate.json":
            AUDIT / BRIDGE_NAME / "receipt_gate.json",
        ".cm2-runtime/audit/" + BRIDGE_NAME + "/dual_checker_receipt.json":
            AUDIT / BRIDGE_NAME / "dual_checker_receipt.json",
        ".cm2-runtime/audit/" + BRIDGE_NAME + "/cold_replay_receipt.json":
            AUDIT / BRIDGE_NAME / "cold_replay_receipt.json",
        ".cm2-runtime/control/" + BRIDGE_NAME + "/pins.sha256":
            WORKSPACE / ".cm2-runtime/control" / BRIDGE_NAME / "pins.sha256",
        ".cm2-runtime/control/" + RUN_NAME + "/pins.sha256":
            WORKSPACE / ".cm2-runtime/control" / RUN_NAME / "pins.sha256",
    }
    paths.update(raw_roots)
    chain_rel = chain_dir.relative_to(WORKSPACE).as_posix()
    paths[chain_rel + "/c30c_v3_audit_evidence.tar.gz"] = (
        chain_dir / "c30c_v3_audit_evidence.tar.gz"
    )
    paths[chain_rel + "/evidence_bundle_receipt.json"] = (
        chain_dir / "evidence_bundle_receipt.json"
    )
    return dict(sorted(paths.items()))


def build(chain_dir: Path) -> dict[str, Any]:
    need(chain_dir.is_dir() and not chain_dir.is_symlink(), "real chain directory")
    receipt = strict_object(chain_dir / "evidence_bundle_receipt.json", "bundle receipt")
    need(receipt.get("schema") == "cm2.round306c30c.v3-audit-evidence-bundle.v1"
         and receipt.get("status") == EXPECTED_BUNDLE_STATUS
         and receipt.get("formal_credit") == 0
         and receipt.get("source_W_formal_remainder") == 80
         and receipt.get("source_W_transition_authorized") is False,
         "zero-credit bundle predecessor")
    paths = payload_paths(chain_dir)
    need(receipt.get("bundle_sha256") == sha(chain_dir / "c30c_v3_audit_evidence.tar.gz"),
         "bundle receipt hash")
    payload_rows = {name: sha(path) for name, path in paths.items()}
    payload_raw = b"".join((payload_rows[name] + "  " + name + "\n").encode("ascii")
                            for name in sorted(payload_rows))
    payload_path = chain_dir / "payload_manifest.sha256"
    exclusive(payload_path, payload_raw)
    chain_rel = chain_dir.relative_to(WORKSPACE).as_posix()
    root_rows = {
        chain_rel + "/payload_manifest.sha256": hashlib.sha256(payload_raw).hexdigest(),
        C30B_MANIFEST_REL: C30B_MANIFEST_SHA256,
    }
    root_raw = b"".join((root_rows[name] + "  " + name + "\n").encode("ascii")
                        for name in sorted(root_rows))
    root_path = chain_dir / "root_manifest.sha256"
    exclusive(root_path, root_raw)
    output = {
        "schema": "cm2.round306c30c.v3-publication-manifests.v1",
        "status": "PASS_PAYLOAD_AND_ROOT_MANIFESTS__ZERO_FORMAL_CREDIT",
        "payload_manifest_sha256": hashlib.sha256(payload_raw).hexdigest(),
        "payload_member_count": len(payload_rows),
        "root_manifest_sha256": hashlib.sha256(root_raw).hexdigest(),
        "root_member_count": 2,
        "round306c30b_manifest_sha256": C30B_MANIFEST_SHA256,
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    exclusive(chain_dir / "manifest_receipt.json", canonical(output) + b"\n")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain-dir", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        result = build(arguments.chain_dir.resolve(strict=True))
    except (Blocked, OSError, ValueError, TypeError, KeyError) as error:
        print(canonical({"schema": "cm2.round306c30c.v3-publication-manifests.v1",
                         "status": "BLOCKED_FAIL_CLOSED", "error": str(error),
                         "formal_credit": 0, "source_W_formal_remainder": 80,
                         "source_W_transition_authorized": False,
                         "CM2": "NO-GO_FOR_CLAIM"}).decode("ascii"))
        return 1
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
