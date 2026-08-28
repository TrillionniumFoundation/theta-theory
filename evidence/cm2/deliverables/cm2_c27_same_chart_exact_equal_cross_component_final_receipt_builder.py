#!/usr/bin/env python3
"""Build the zero-credit final receipt for the independent 228-group audit."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
PRODUCER = "cm2_c27_same_chart_exact_equal_cross_component_sqlite_probe.py"
ATTACKER = "cm2_c27_same_chart_exact_equal_cross_component_attack_harness.py"
LEDGER = "cm2_c27_same_chart_exact_equal_cross_component_witness_groups.jsonl.gz"
RESULT = "cm2_c27_same_chart_exact_equal_cross_component_sqlite_result.json"


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def closed_object(path: Path, field: str = "result_sha256") -> dict[str, Any]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and b"\n" not in raw[:-1], f"single object:{path}")
    value = json.loads(raw[:-1])
    need(canonical(value) + b"\n" == raw, f"canonical object:{path}")
    body = dict(value)
    need(body.pop(field, None) == digest(body), f"object closure:{path}")
    return value


def validate_groups(path: Path) -> dict[str, Any]:
    group_count = 0
    member_count = 0
    component_count = 0
    group_ids = []
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), "group newline")
            row = json.loads(line[:-1])
            need(canonical(row) + b"\n" == line, "canonical group")
            body = dict(row)
            claimed = body.pop("group_row_sha256", None)
            need(claimed == digest(body) and row["ordinal"] == ordinal, "group closure and ordinal")
            components = {member["fresh_component_id"] for member in row["members"]}
            need(
                len(components) == row["component_count"] == 2
                and row["member_count"] == len(row["members"]) == 2
                and row["cross_component_member_pair_count"] == 1
                and row["legal_cross_component_physical_witness"] is True
                and row["strict_positive_volume_proof"]["common_open_interior_nonempty"] is True,
                "exact two-member two-component positive-volume witness",
            )
            for member in row["members"]:
                member_body = dict(member)
                member_claimed = member_body.pop("member_row_sha256", None)
                need(member_claimed == digest(member_body), "member closure")
                need(
                    member["source_kernel"] == "C22A"
                    and member["support_kind"] == "OPEN_RATIONAL_BOX"
                    and member["chart"] == row["chart"]
                    and member["physical_bounds"] == row["physical_bounds"],
                    "observed C22A open-box witness member",
                )
            group_count += 1
            member_count += len(row["members"])
            component_count += len(components)
            group_ids.append(row["group_id"])
    need(group_count == 228 and member_count == component_count == 456, "228/456 exact witness census")
    return {
        "group_count": group_count,
        "member_count": member_count,
        "component_occurrence_count": component_count,
        "group_ids_sha256": digest(group_ids),
    }


def validate_run_evidence(
    directory: Path, result_path: Path, result: dict[str, Any], seed: int,
) -> dict[str, Any]:
    exit_path = directory / "exit_code.txt"
    stderr_path = directory / "stderr.txt"
    stdout_path = directory / "stdout.json"
    time_path = directory / "time.txt"
    need(exit_path.read_bytes() == b"0\n", "numeric exit zero")
    need(stderr_path.read_bytes() == b"", "stderr empty")
    need(stdout_path.read_bytes() == result_path.read_bytes(), "same invocation stdout/result identity")
    time_raw = time_path.read_text(encoding="utf-8")
    need(
        "Exit status: 0" in time_raw
        and f"--seed {seed}" in time_raw
        and f"--output-dir {directory}" in time_raw,
        "time receipt command and exit",
    )
    expected_command = [
        sys.executable, "-I", "-B", str((ROOT / PRODUCER).resolve()),
        "--output-dir", str(directory), "--seed", str(seed),
    ]
    need(
        result["declared_seed"] == seed
        and result["declared_seed_used_for_pre_sort_sqlite_insertion_order"] is True
        and result["invocation"] == {
            "command_argv": expected_command,
            "isolated_runtime": True,
            "dont_write_bytecode": True,
        },
        "actual seed and normalized command authority",
    )
    return {
        "declared_seed": seed,
        "normalized_command_argv": expected_command,
        "exit_code_file_sha256": file_hash(exit_path),
        "stderr_file_sha256": file_hash(stderr_path),
        "stdout_file_sha256": file_hash(stdout_path),
        "time_file_sha256": file_hash(time_path),
        "numeric_exit": 0,
        "stderr_empty": True,
        "stdout_equals_result_file": True,
        "time_exit_status": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-a-dir", required=True)
    parser.add_argument("--seed-b-dir", required=True)
    parser.add_argument("--seed-a", required=True, type=int)
    parser.add_argument("--seed-b", required=True, type=int)
    parser.add_argument("--attacks-json", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated -I -B runtime")
    need(args.seed_a != args.seed_b, "distinct real seeds")
    a, b = Path(args.seed_a_dir).resolve(), Path(args.seed_b_dir).resolve()
    result_a, result_b = a / RESULT, b / RESULT
    ledger_a, ledger_b = a / LEDGER, b / LEDGER
    need(result_a.read_bytes() != result_b.read_bytes(), "seed-bearing results must differ")
    need(ledger_a.read_bytes() == ledger_b.read_bytes(), "double-seed ledger byte identity")
    result = closed_object(result_a)
    result_b_value = closed_object(result_b)
    need(
        result["semantic_projection_sha256"] == result_b_value["semantic_projection_sha256"]
        and result["group_ids_sha256"] == result_b_value["group_ids_sha256"]
        and result["group_rows_sha256"] == result_b_value["group_rows_sha256"]
        and result["ledger_semantic_commitments"] == result_b_value["ledger_semantic_commitments"]
        and result["input_sha256"] == result_b_value["input_sha256"]
        and result["witness_census"] == result_b_value["witness_census"],
        "cross-seed exact semantic equality",
    )
    run_a = validate_run_evidence(a, result_a, result, args.seed_a)
    run_b = validate_run_evidence(b, result_b, result_b_value, args.seed_b)
    need(
        result["status"] == "PASS_ZERO_CREDIT__228_SAME_CHART_EXACT_EQUAL_POSITIVE_VOLUME_CROSS_C15_COMPONENT_WITNESS_GROUPS"
        and result["primitive_atom_count"] == 483_232
        and result["witness_census"] == {
            "cross_component_member_pair_count": 228,
            "duplicate_exact_box_group_count": 134_968,
            "witness_component_occurrence_count": 456,
            "witness_group_count": 228,
            "witness_member_count": 456,
        }
        and result["forbidden_inputs"] == {
            "C27_source_or_FAMILIES_imported_or_read": False,
            "old_edge_ledger_used_as_candidate_universe": False,
            "same_chart_census_atom_ledger_opened_or_used": False,
        }
        and result["legal_cross_component_witness_found"] is True
        and result["endpoint_bits_needed_for_these_witnesses"] is False
        and result["formal_credit"] == 0
        and result["C27_C28_C29"] == "REJECT_AND_REBUILD_REQUIRED"
        and result["CM2"] == "NO-GO_FOR_CLAIM",
        "truthful independent witness result",
    )
    group_census = validate_groups(ledger_a)
    need(group_census["group_ids_sha256"] == result["group_ids_sha256"], "group id commitment")
    attack = closed_object(Path(args.attacks_json).resolve())
    need(
        attack["status"] == "PASS_27_OF_27_COHERENT_SAME_CHART_WITNESS_ATTACKS_REJECTED__ZERO_CREDIT"
        and attack["attack_count"] == attack["rejected_count"] == 27
        and len(attack["rejected_attacks"]) == 27
        and attack["baseline_result_sha256"] == result["result_sha256"]
        and attack["baseline_group_ids_sha256"] == result["group_ids_sha256"]
        and attack["baseline_declared_seed"] == args.seed_a
        and attack["baseline_semantic_projection_sha256"] == result["semantic_projection_sha256"]
        and attack["formal_credit"] == 0
        and attack["C27_C28_C29"] == "REJECT_AND_REBUILD_REQUIRED",
        "24 coherent attacks",
    )
    body = {
        "schema": "cm2.c27.same-chart-exact-equal-cross-component.final-zero-credit-receipt.v1",
        "status": "PASS_FINAL_ZERO_CREDIT__INDEPENDENT_228_GROUP_SAME_CHART_POSITIVE_VOLUME_CROSS_COMPONENT_WITNESSES__C27_C28_C29_REBUILD_REQUIRED",
        "candidate_universe": result["candidate_universe"],
        "implementation": result["implementation"],
        "seeds": [args.seed_a, args.seed_b],
        "run_receipts": [run_a, run_b],
        "seed_bearing_result_files_intentionally_distinct": True,
        "cross_seed_semantic_projection_identical": True,
        "double_seed_ledger_byte_identical": True,
        "primitive_atom_count": 483_232,
        "witness_census": result["witness_census"],
        "observed_witness_structure": {
            "source_pair": "C22A+C22A",
            "support_kind_pair": "OPEN_RATIONAL_BOX+OPEN_RATIONAL_BOX",
            "members_per_group": 2,
            "distinct_C15_components_per_group": 2,
            "strict_positive_volume_groups": 228,
            "C23_signed_sqrt_groups_in_witness_set": 0,
            "C23_signed_sqrt_branches_in_candidate_universe_and_normalized_exactly": True,
        },
        "group_ids_sha256": result["group_ids_sha256"],
        "group_rows_sha256": result["group_rows_sha256"],
        "semantic_projection_sha256": result["semantic_projection_sha256"],
        "result_object_sha256": result["result_sha256"],
        "result_B_object_sha256": result_b_value["result_sha256"],
        "result_file_sha256": file_hash(result_a),
        "result_B_file_sha256": file_hash(result_b),
        "ledger_sha256": file_hash(ledger_a),
        "ledger_group_row_sequence_sha256": result["ledger"]["group_row_sequence_sha256"],
        "ledger_flattened_member_row_sequence_sha256": result["ledger"]["flattened_member_row_sequence_sha256"],
        "attack_result_sha256": attack["result_sha256"],
        "attack_file_sha256": file_hash(Path(args.attacks_json).resolve()),
        "attack_count": 27,
        "producer_script_sha256": file_hash(ROOT / PRODUCER),
        "attack_script_sha256": file_hash(ROOT / ATTACKER),
        "input_sha256": result["input_sha256"],
        "forbidden_inputs": result["forbidden_inputs"],
        "legal_cross_component_witness_found": True,
        "endpoint_bits_needed_for_these_witnesses": False,
        "required_governance_action": "REBUILD_C27_THROUGH_C29__PATCHING_OR_PRESERVING_C29_UNCONDITIONAL_AUTHORITY_IS_FORBIDDEN",
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = {**body, "receipt_sha256": digest(body)}
    output = Path(args.output).resolve()
    output.write_bytes(canonical(receipt) + b"\n")
    print(canonical(receipt).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print("REJECT_SAME_CHART_WITNESS_FINAL_RECEIPT:" + str(error), file=sys.stderr)
        raise SystemExit(2)
