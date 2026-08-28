#!/usr/bin/env python3
"""Bind both seeds, both semantics and attacks for SINGLE_GRAPHS."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
SOURCES = (
    "cm2_c27_single_graphs_physical_totality_stream_probe.py",
    "cm2_c27_single_graphs_physical_totality_sqlite_verifier.py",
    "cm2_c27_single_graphs_physical_totality_attack_harness.py",
    "cm2_c27_single_graphs_physical_totality_final_receipt_builder.py",
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
    stream_a, stream_b = Path(args.stream_a).resolve(), Path(args.stream_b).resolve()
    sqlite_a, sqlite_b = Path(args.sqlite_a).resolve(), Path(args.sqlite_b).resolve()
    attack_dir = Path(args.attacks).resolve()
    for name in ("ledger.jsonl.gz", "result.json", "manifest.json"):
        need((stream_a / name).read_bytes() == (stream_b / name).read_bytes(), "stream double-seed bytes:" + name)
    need((sqlite_a / "verification.json").read_bytes() == (sqlite_b / "verification.json").read_bytes(), "SQLite double-seed bytes")
    stream = closed(stream_a / "result.json", "result_sha256")
    verification = closed(sqlite_a / "verification.json", "verification_sha256")
    attacks = closed(attack_dir / "attack_result.json", "result_sha256")
    need(stream["status"].startswith("PASS_ZERO_CREDIT__SINGLE_GRAPHS_4984_ROOTS"), "stream status")
    need(stream["C10_terminal_partition"] == {"DOUBLE_GRAPHS": 16, "OUTGOING_GRAPHS": 264, "SINGLE_GRAPHS": 4984}, "C10 terminal partition")
    need(stream["single_graph_class_partition"] == {"R235_SOURCE_EXACT_FACE_FULL_BASE": 552, "R235_TARGET_POSITIVE_PARTIAL_BASE": 4432}, "single class partition")
    need(stream["C24_full_terminal_allocation"] == {
        "C24A": {
            "DOUBLE_GRAPHS": {"G2A": 16, "G2B": 16},
            "OUTGOING_GRAPHS": {"G2A": 264, "G2B": 528},
            "SINGLE_GRAPHS": {"G2A": 4984, "G2B": 9416},
        },
        "C24B": {"DOUBLE_GRAPHS": {"G2B": 16}, "OUTGOING_GRAPHS": {}, "SINGLE_GRAPHS": {"G2B": 152}},
    }, "full C24 terminal allocation")
    need(stream["single_root_count"] == stream["G2A_sheet_count"] == 4984, "single root/sheet census")
    need(stream["G2B_positive_side_count"] == 9416 and stream["G2B_exact_empty_side_count"] == 152, "single side census")
    need(stream["selected_member_count"] == 14552 and stream["unresolved_count"] == 0, "single member/unresolved census")
    need(verification["status"].startswith("PASS_SQLITE_INDEPENDENT_REBUILD"), "SQLite status")
    need(verification["per_candidate_digest_mismatch_count"] == 0, "per-candidate exact identity")
    need(verification["ordered_candidate_digests_sha256"] == stream["ordered_candidate_digests_sha256"], "ordered digest identity")
    need(attacks["attack_count"] == attacks["rejected_count"] == 48 and attacks["unexpected_accept_count"] == 0, "attack census")
    evidence = {
        "stream_seed_A": {name: file_sha(stream_a / name) for name in ("ledger.jsonl.gz", "result.json", "manifest.json")},
        "stream_seed_B": {name: file_sha(stream_b / name) for name in ("ledger.jsonl.gz", "result.json", "manifest.json")},
        "sqlite_seed_A": {"verification.json": file_sha(sqlite_a / "verification.json")},
        "sqlite_seed_B": {"verification.json": file_sha(sqlite_b / "verification.json")},
        "attacks": {"attack_result.json": file_sha(attack_dir / "attack_result.json")},
    }
    body = {
        "schema": "cm2.c27.single-graphs-physical-totality-zero-credit.v1.final-receipt.v1",
        "status": "PASS_SINGLE_GRAPHS_DUAL_SEMANTICS_DOUBLE_SEED_48_ATTACKS__ZERO_CREDIT",
        "C10_terminal_partition": stream["C10_terminal_partition"],
        "single_graph_class_partition": stream["single_graph_class_partition"],
        "C24_full_terminal_allocation": stream["C24_full_terminal_allocation"],
        "single_roots": 4984,
        "G2A_sheet_dispositions": 4984,
        "G2B_positive_side_dispositions": 9416,
        "G2B_exact_empty_side_dispositions": 152,
        "materialized_C15_C24_C25_C26_proof_rows": 14552,
        "unresolved": 0,
        "stream_double_seed_byte_identical": True,
        "sqlite_double_seed_byte_identical": True,
        "cross_implementation_per_candidate_digest_mismatch": 0,
        "coherent_attacks_rejected": 48,
        "legacy_transition_family_table_used": False,
        "historical_edge_ledger_used_as_candidate_universe": False,
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
