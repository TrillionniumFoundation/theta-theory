#!/usr/bin/env python3
"""Bind both seeds, both semantics and attacks for OUTGOING_GRAPHS."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
SOURCES = (
    "cm2_c27_outgoing_graphs_physical_totality_stream_probe.py",
    "cm2_c27_outgoing_graphs_physical_totality_sqlite_verifier.py",
    "cm2_c27_outgoing_graphs_physical_totality_attack_harness.py",
)


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def closed(path: Path, closure_field: str) -> dict[str, Any]:
    raw = path.read_bytes()
    obj = json.loads(raw)
    need(canonical(obj) == raw, "canonical:" + path.name)
    body = dict(obj)
    claimed = body.pop(closure_field, None)
    need(isinstance(claimed, str) and claimed == digest(body), "closure:" + path.name)
    return obj


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream-a", required=True)
    parser.add_argument("--stream-b", required=True)
    parser.add_argument("--sqlite-a", required=True)
    parser.add_argument("--sqlite-b", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--output-tag", required=True)
    args = parser.parse_args()
    sa, sb = Path(args.stream_a).resolve(), Path(args.stream_b).resolve()
    qa, qb = Path(args.sqlite_a).resolve(), Path(args.sqlite_b).resolve()
    attack_dir = Path(args.attacks).resolve()
    for name in ("ledger.jsonl.gz", "result.json", "manifest.json"):
        need((sa / name).read_bytes() == (sb / name).read_bytes(), "stream double-seed bytes:" + name)
    need((qa / "verification.json").read_bytes() == (qb / "verification.json").read_bytes(), "SQLite double-seed bytes")
    stream = closed(sa / "result.json", "result_sha256")
    verification = closed(qa / "verification.json", "verification_sha256")
    attacks = closed(attack_dir / "attack_result.json", "result_sha256")
    need(stream["status"].startswith("PASS_ZERO_CREDIT__OUTGOING_GRAPHS_264_ROOTS"), "stream status")
    need(stream["C10_actual_G1_partition"] == {"OUTGOING": 264, "SINGLE": 4984, "DOUBLE": 16}, "fresh class partition")
    need(stream["outgoing_root_count"] == stream["G2A_sheet_disposition_count"] == 264, "root/G2A census")
    need(stream["G2B_side_disposition_count"] == 528 and stream["unresolved_count"] == 0, "G2B/unresolved census")
    need(verification["status"].startswith("PASS_SQLITE_INDEPENDENT_REBUILD"), "SQLite status")
    need(verification["per_candidate_digest_mismatch_count"] == 0, "per-candidate digest identity")
    need(verification["ordered_candidate_digests_sha256"] == stream["ordered_candidate_digests_sha256"], "ordered digest identity")
    need(attacks["attack_count"] == attacks["rejected_count"] == 31 and attacks["unexpected_accept_count"] == 0, "attack census")
    evidence = {
        "stream_seed_A": {name: file_sha(sa / name) for name in ("ledger.jsonl.gz", "result.json", "manifest.json")},
        "stream_seed_B": {name: file_sha(sb / name) for name in ("ledger.jsonl.gz", "result.json", "manifest.json")},
        "sqlite_seed_A": {"verification.json": file_sha(qa / "verification.json")},
        "sqlite_seed_B": {"verification.json": file_sha(qb / "verification.json")},
        "attacks": {"attack_result.json": file_sha(attack_dir / "attack_result.json")},
    }
    body = {
        "schema": "cm2.c27.outgoing-graphs-physical-totality-zero-credit.v1.final-receipt.v1",
        "status": "PASS_OUTGOING_GRAPHS_DUAL_SEMANTICS_DOUBLE_SEED_31_ATTACKS__ZERO_CREDIT",
        "fresh_G1_partition": stream["C10_actual_G1_partition"],
        "outgoing_roots": 264,
        "G2A_sheet_dispositions": 264,
        "G2B_side_dispositions": 528,
        "unresolved": 0,
        "stream_double_seed_byte_identical": True,
        "sqlite_double_seed_byte_identical": True,
        "cross_implementation_per_candidate_digest_mismatch": 0,
        "coherent_attacks_rejected": 31,
        "C27_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "source_files": [{"filename": name, "sha256": file_sha(ROOT / name)} for name in SOURCES],
        "evidence": evidence,
        "formal_credit": 0,
        "strict_nonpromotion": {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result = {**body, "receipt_sha256": digest(body)}
    target = AUDIT / args.output_tag
    need(not target.exists() and target.parent.resolve() == AUDIT.resolve(), "new direct-child output")
    target.mkdir(mode=0o700)
    (target / "receipt.json").write_bytes(canonical(result))
    print(canonical({"status": result["status"], "receipt_sha256": result["receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
