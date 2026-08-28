#!/usr/bin/env python3
"""Build a fail-closed zero-credit receipt for the cross-implementation match."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
COMPARATOR = ROOT / "cm2_c27_same_chart_witness_cross_implementation_comparator.py"
ATTACKER = ROOT / "cm2_c27_same_chart_witness_cross_implementation_attack_harness.py"
SELF = Path(__file__).resolve()


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
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def load_comparator() -> Any:
    spec = importlib.util.spec_from_file_location("cm2_same_chart_cross_comparator_receipt", COMPARATOR)
    need(spec is not None and spec.loader is not None, "comparator import spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def expected_from_result(result: dict[str, Any]) -> dict[str, Any]:
    comparison = result["cross_implementation_exact_comparison"]
    fields = (
        "witness_group_count",
        "witness_projection_count",
        "group_ids_sha256",
        "flattened_projection_sha256",
        "comparison_row_hashes_sha256",
        "unique_component_edge_count",
        "affected_component_vertex_count",
        "DSU_rank_reduction",
        "connected_component_count_on_affected_vertices",
        "unique_component_edges_sha256",
        "affected_component_vertices_sha256",
    )
    return {field: comparison[field] for field in fields}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--comparator-result", required=True)
    parser.add_argument("--comparison-ledger", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated -I -B runtime")
    module = load_comparator()
    result_path = Path(args.comparator_result).resolve(strict=True)
    ledger_path = Path(args.comparison_ledger).resolve(strict=True)
    attack_path = Path(args.attacks).resolve(strict=True)
    result = module.closed_object(result_path)
    attack = module.closed_object(attack_path)
    groups = list(module.closed_gzip_rows(ledger_path, "comparison_row_sha256"))
    expected = expected_from_result(result)
    observed = module.validate_comparison_groups(groups, expected)

    need(
        result.get("status") == "PASS_ZERO_CREDIT__PYTHON_EXTERNAL_SORT_AND_SQLITE_IMPLEMENTATIONS_EXACTLY_MATCH_228_GROUPS_456_PROJECTIONS__C27_C28_C29_REBUILD_REQUIRED"
        and result.get("formal_credit") == 0
        and result.get("legal_cross_component_witness_found") is True
        and result.get("C27_C28_C29") == "REJECT_AND_REBUILD_REQUIRED"
        and result.get("CM2") == "NO-GO_FOR_CLAIM",
        "truthful comparator result",
    )
    need(
        observed["witness_group_count"] == 228
        and observed["witness_projection_count"] == 456
        and observed["unique_component_edge_count"] == 192
        and observed["affected_component_vertex_count"] == 312
        and observed["DSU_rank_reduction"] == 192
        and observed["connected_component_count_on_affected_vertices"] == 120,
        "228/456/192/312/rank192 exact structure",
    )
    ledger = result.get("comparison_ledger")
    need(
        type(ledger) is dict
        and ledger.get("row_count") == 228
        and ledger.get("sha256") == file_hash(ledger_path)
        and ledger.get("size") == ledger_path.stat().st_size,
        "comparison ledger commitment",
    )
    need(
        result.get("implementation_B_cross_seed", {}).get("seeds") == [30_629_101, 30_629_901]
        and result["implementation_B_cross_seed"].get("seed_bearing_result_files_distinct") is True
        and result["implementation_B_cross_seed"].get("semantic_projection_exact_identical") is True
        and result["implementation_B_cross_seed"].get("ledger_byte_identical") is True,
        "implementation B real double-seed evidence",
    )
    pins = result.get("input_pins")
    need(type(pins) is dict and len(pins) == 7, "seven input pins")
    for name, pin in pins.items():
        path = Path(pin["path"]).resolve(strict=True)
        stat_value = path.stat()
        need(
            file_hash(path) == pin["sha256"]
            and stat_value.st_size == pin["size"]
            and stat_value.st_dev == pin["device"]
            and stat_value.st_ino == pin["inode"]
            and stat_value.st_mtime_ns == pin["mtime_ns"],
            f"receipt input pin still exact:{name}",
        )
    need(
        Path(pins["seed_A_ledger"]["path"]).read_bytes()
        == Path(pins["seed_B_ledger"]["path"]).read_bytes(),
        "receipt rechecks double-seed ledger byte identity",
    )
    need(
        attack.get("status") == "PASS_20_OF_20_COHERENT_CROSS_IMPLEMENTATION_COMPARATOR_ATTACKS_REJECTED__ZERO_CREDIT"
        and attack.get("attack_count") == attack.get("rejected_count") == 20
        and len(attack.get("rejected_attacks", [])) == 20
        and attack.get("baseline_result_sha256") == result["result_sha256"]
        and attack.get("baseline_result_file_sha256") == file_hash(result_path)
        and attack.get("baseline_ledger_sha256") == file_hash(ledger_path)
        and attack.get("formal_credit") == 0,
        "20 coherent attacks bound to comparator",
    )
    limitations = result.get("limitations")
    need(
        limitations == {
            "C26_absence_negative_theorem_proved": False,
            "half_open_endpoint_ownership_gap_resolved": False,
            "same_chart_relative_cells_totality_proved": False,
            "scope": "EXACT_EQUAL_POSITIVE_VOLUME_SAME_CHART_GROUP_CROSS_IMPLEMENTATION_COMPARISON_ONLY",
            "twenty_family_totality_proved": False,
        },
        "no totality overclaim",
    )

    body = {
        "schema": "cm2.c27.same-chart-witness-cross-implementation-comparator.zero-credit-receipt.v1",
        "status": "PASS_FINAL_ZERO_CREDIT__TWO_INDEPENDENT_IMPLEMENTATIONS_EXACTLY_MATCH_228_GROUPS_AND_456_PROJECTIONS__192_COMPONENT_EDGES_FORCE_DSU_RANK_192__C27_C28_C29_REBUILD_REQUIRED",
        "implementation_A": result["implementation_A"],
        "implementation_B": result["implementation_B"],
        "cross_implementation_exact_match": {
            "group_count": 228,
            "projection_count": 456,
            "group_ids_sha256": observed["group_ids_sha256"],
            "flattened_projection_sha256": observed["flattened_projection_sha256"],
            "unique_component_edge_count": 192,
            "affected_component_vertex_count": 312,
            "DSU_rank_reduction": 192,
            "connected_component_count_on_affected_vertices": 120,
            "unique_component_edges_sha256": observed["unique_component_edges_sha256"],
        },
        "implementation_B_double_seed": result["implementation_B_cross_seed"],
        "canonical_row_closures_validated": result["canonical_row_closures_validated"],
        "comparator_result_sha256": result["result_sha256"],
        "comparator_result_file_sha256": file_hash(result_path),
        "comparison_ledger_sha256": file_hash(ledger_path),
        "attack_result_sha256": attack["result_sha256"],
        "attack_file_sha256": file_hash(attack_path),
        "attack_count": 20,
        "comparator_script_sha256": file_hash(COMPARATOR),
        "attack_script_sha256": file_hash(ATTACKER),
        "receipt_builder_script_sha256": file_hash(SELF),
        "input_pins": pins,
        "forbidden_reuse": result["forbidden_reuse"],
        "legal_cross_component_witness_found": True,
        "required_governance_action": "REBUILD_C27_THROUGH_C29__PATCHING_OR_PRESERVING_C29_UNCONDITIONAL_AUTHORITY_IS_FORBIDDEN",
        "limitations": limitations,
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
    except (Failure, ModuleNotFoundError, OSError, TypeError, ValueError, KeyError, json.JSONDecodeError) as error:
        print("REJECT_SAME_CHART_CROSS_IMPLEMENTATION_RECEIPT:" + str(error), file=sys.stderr)
        raise SystemExit(2)
