#!/usr/bin/env python3
"""Bind dual seeds, dual physical semantics, and attacks into zero-credit receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
SOURCES = (
    "cm2_c27_sheet_owner_shadow_physical_totality_stream_probe.py",
    "cm2_c27_sheet_owner_shadow_physical_totality_sqlite_verifier.py",
    "cm2_c27_sheet_owner_shadow_physical_totality_attack_harness.py",
    "cm2_c27_sheet_owner_shadow_physical_totality_final_receipt_builder.py",
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


def closed(path: Path, field: str, newline: bool = False) -> dict[str, Any]:
    raw = path.read_bytes()
    if newline:
        need(raw.endswith(b"\n"), "newline:" + str(path))
        raw = raw[:-1]
    value = json.loads(raw)
    need(canonical(value) == raw, "canonical:" + str(path))
    body = dict(value)
    claimed = body.pop(field, None)
    need(isinstance(claimed, str) and claimed == digest(body), "closure:" + str(path))
    return value


def run_evidence(
    directory: Path, artifact: Path, expected_argv: list[str],
) -> dict[str, Any]:
    exit_path = directory / "exit_code.txt"
    stderr_path = directory / "stderr.txt"
    stdout_path = directory / "stdout.json"
    time_path = directory / "time.txt"
    need(exit_path.read_bytes() == b"0\n", "numeric exit zero:" + str(directory))
    need(stderr_path.read_bytes() == b"", "stderr empty:" + str(directory))
    need(stdout_path.read_bytes() == artifact.read_bytes(), "stdout/artifact same invocation identity:" + str(directory))
    time_text = time_path.read_text(encoding="utf-8")
    need("Exit status: 0" in time_text, "time exit status zero:" + str(directory))
    need(all(token in time_text for token in expected_argv[3:]), "time command argv binding:" + str(directory))
    return {
        "normalized_command_argv": expected_argv,
        "numeric_exit": 0,
        "stderr_empty": True,
        "stdout_equals_artifact": True,
        "time_exit_status": 0,
        "exit_code_file_sha256": file_sha(exit_path),
        "stderr_file_sha256": file_sha(stderr_path),
        "stdout_file_sha256": file_sha(stdout_path),
        "time_file_sha256": file_sha(time_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream-a", required=True)
    parser.add_argument("--stream-b", required=True)
    parser.add_argument("--sqlite-a", required=True)
    parser.add_argument("--sqlite-b", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--seed-a", type=int, required=True)
    parser.add_argument("--seed-b", type=int, required=True)
    parser.add_argument("--output-tag", required=True)
    parser.add_argument("--publish", default="cm2_c27_sheet_owner_shadow_physical_totality_subgate_receipt.json")
    arguments = parser.parse_args()
    need(arguments.seed_a >= 0 and arguments.seed_b >= 0 and arguments.seed_a != arguments.seed_b, "two distinct real seeds")
    stream_a, stream_b = Path(arguments.stream_a).resolve(), Path(arguments.stream_b).resolve()
    sqlite_a, sqlite_b = Path(arguments.sqlite_a).resolve(), Path(arguments.sqlite_b).resolve()
    attacks_dir = Path(arguments.attacks).resolve()
    for name in ("sheet_owner_shadow_terminal_ledger.jsonl.gz", "materialized_shadow_companion_ledger.jsonl.gz"):
        need((stream_a / name).read_bytes() == (stream_b / name).read_bytes(), "stream double-seed byte identity:" + name)
    need((stream_a / "result.json").read_bytes() != (stream_b / "result.json").read_bytes(), "stream seed-bearing results intentionally distinct")
    need((sqlite_a / "verification.json").read_bytes() != (sqlite_b / "verification.json").read_bytes(), "SQLite seed-bearing results intentionally distinct")
    stream = closed(stream_a / "result.json", "result_sha256", newline=True)
    stream_b_result = closed(stream_b / "result.json", "result_sha256", newline=True)
    verification = closed(sqlite_a / "verification.json", "verification_sha256", newline=True)
    verification_b = closed(sqlite_b / "verification.json", "verification_sha256", newline=True)
    attacks = closed(attacks_dir / "attack_result.json", "result_sha256")
    need(
        stream["declared_seed"] == arguments.seed_a
        and stream_b_result["declared_seed"] == arguments.seed_b
        and stream["semantic_projection_sha256"] == stream_b_result["semantic_projection_sha256"],
        "stream actual double-seed semantic identity",
    )
    need(
        verification["declared_seed"] == arguments.seed_a
        and verification_b["declared_seed"] == arguments.seed_b
        and verification["semantic_projection_sha256"] == verification_b["semantic_projection_sha256"],
        "SQLite actual double-seed semantic identity",
    )
    stream_script = str((ROOT / SOURCES[0]).resolve())
    sqlite_script = str((ROOT / SOURCES[1]).resolve())
    stream_argv_a = [sys.executable, "-I", "-B", stream_script, "--seed", str(arguments.seed_a), "--output-dir", str(stream_a)]
    stream_argv_b = [sys.executable, "-I", "-B", stream_script, "--seed", str(arguments.seed_b), "--output-dir", str(stream_b)]
    sqlite_argv_a = [sys.executable, "-I", "-B", sqlite_script, "--candidate-dir", str(stream_a), "--seed", str(arguments.seed_a), "--output-tag", sqlite_a.name]
    sqlite_argv_b = [sys.executable, "-I", "-B", sqlite_script, "--candidate-dir", str(stream_b), "--seed", str(arguments.seed_b), "--output-tag", sqlite_b.name]
    need(stream["invocation"]["command_argv"] == stream_argv_a and stream_b_result["invocation"]["command_argv"] == stream_argv_b, "stream normalized command authority")
    need(verification["invocation"]["command_argv"] == sqlite_argv_a and verification_b["invocation"]["command_argv"] == sqlite_argv_b, "SQLite normalized command authority")
    run_receipts = {
        "stream_seed_A": run_evidence(stream_a, stream_a / "result.json", stream_argv_a),
        "stream_seed_B": run_evidence(stream_b, stream_b / "result.json", stream_argv_b),
        "sqlite_seed_A": run_evidence(sqlite_a, sqlite_a / "verification.json", sqlite_argv_a),
        "sqlite_seed_B": run_evidence(sqlite_b, sqlite_b / "verification.json", sqlite_argv_b),
    }
    need(stream["primitive_candidate_generation"] == {"R204_target_factor_sign_partition": 224, "R211_factor_sign_and_outgoing_chart_partition": 17_716, "total_physical_sheets": 17_940}, "primitive candidate census")
    need(stream["terminal_census"] == {"SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940} and stream["candidate_role_row_count"] == 35_880, "terminal census")
    need(stream["unresolved"] == stream["orphan_or_duplicate"] == stream["legal_cross_component_witness"] == 0, "stream closed physical gate")
    need(stream["terminal_physical_totality"] == "PASS_LOCAL_ZERO_CREDIT" and stream["formal_credit"] == 0, "stream zero-credit status")
    need(verification["status"].startswith("PASS_SQLITE_INDEPENDENT_R173_R204_R208_REBUILD"), "SQLite status")
    need(verification["primitive_candidates_generated_before_C21_C25_C26_read"] is True, "binding order")
    need(verification["per_role_row_exact_mismatch_count"] == verification["per_shadow_row_exact_mismatch_count"] == 0, "cross-implementation exact rows")
    need(verification["candidate_projection_sha256"] == stream["candidate_projection_sha256"], "cross-implementation projection commitment")
    need(verification["role_ordered_row_hashes_sha256"] == stream["role_ledger"]["ordered_row_hashes_sha256"], "role commitment")
    need(verification["shadow_ordered_row_hashes_sha256"] == stream["shadow_companion_ledger"]["ordered_row_hashes_sha256"], "shadow commitment")
    need(attacks["attack_count"] == attacks["rejected_count"] == 50 and attacks["unexpected_accept_count"] == 0, "attack census")
    need(stream["C27_C28_C29"] == verification["C27_C28_C29"] == attacks["C27_C28_C29"] == "REJECT_PENDING_ALL_20_TERMINAL_GATE", "C27-29 nonpromotion")
    need(stream["CM2"] == verification["CM2"] == attacks["CM2"] == "NO-GO_FOR_CLAIM", "CM2 nonpromotion")
    evidence = {
        "stream_seed_A": {name: file_sha(stream_a / name) for name in ("sheet_owner_shadow_terminal_ledger.jsonl.gz", "materialized_shadow_companion_ledger.jsonl.gz", "result.json")},
        "stream_seed_B": {name: file_sha(stream_b / name) for name in ("sheet_owner_shadow_terminal_ledger.jsonl.gz", "materialized_shadow_companion_ledger.jsonl.gz", "result.json")},
        "sqlite_seed_A": {"verification.json": file_sha(sqlite_a / "verification.json")},
        "sqlite_seed_B": {"verification.json": file_sha(sqlite_b / "verification.json")},
        "attacks": {"attack_result.json": file_sha(attacks_dir / "attack_result.json")},
    }
    body = {
        "schema": "cm2.c27.sheet-owner-shadow-physical-totality.zero-credit.v1.final-receipt.v1",
        "status": "PASS_SHEET_OWNER_SHADOW_DUAL_PHYSICAL_SEMANTICS_DOUBLE_SEED_50_ATTACKS__ZERO_CREDIT",
        "declared_seeds": [arguments.seed_a, arguments.seed_b],
        "primitive_candidate_generation": {"R204": 224, "R211": 17_716, "total": 17_940},
        "terminal_census": {"SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940},
        "role_rows": 35_880, "materialized_shadow_companions": 17_940,
        "stream_double_seed_ledger_byte_identical": True,
        "stream_seed_bearing_results_intentionally_distinct": True,
        "sqlite_seed_bearing_results_intentionally_distinct": True,
        "stream_cross_seed_semantic_projection_identical": True,
        "sqlite_cross_seed_semantic_projection_identical": True,
        "cross_implementation_role_row_mismatch": 0, "cross_implementation_shadow_row_mismatch": 0,
        "candidate_projection_sha256": stream["candidate_projection_sha256"],
        "coherent_attacks_rejected": 50, "unresolved": 0, "legal_cross_component_witness": 0,
        "primitive_candidates_generated_before_C21_C25_C26_binding": True,
        "C27_FAMILIES_imported_or_read": False, "edge_ledger_used_as_candidate_universe": False,
        "source_files": [{"filename": name, "sha256": file_sha(ROOT / name)} for name in SOURCES],
        "evidence": evidence, "run_receipts": run_receipts, "formal_credit": 0,
        "strict_nonpromotion": {"C27_transition_totality": 0, "C28_pair_routing": 0, "C29_physical_maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
    }
    receipt = {**body, "receipt_sha256": digest(body)}
    target = AUDIT / arguments.output_tag
    need(not target.exists() and target.parent.resolve() == AUDIT.resolve(), "new direct-child output")
    target.mkdir(mode=0o700)
    (target / "receipt.json").write_bytes(canonical(receipt))
    publish = (ROOT / arguments.publish).resolve()
    need(publish.parent == ROOT.resolve() and not publish.exists(), "new direct-child published receipt")
    publish.write_bytes(canonical(receipt) + b"\n")
    print(canonical({"status": receipt["status"], "receipt_sha256": receipt["receipt_sha256"], "published": publish.name}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print("REJECT_SHEET_OWNER_SHADOW_PHYSICAL_FINAL_RECEIPT:" + str(error), file=sys.stderr)
        raise SystemExit(2)
