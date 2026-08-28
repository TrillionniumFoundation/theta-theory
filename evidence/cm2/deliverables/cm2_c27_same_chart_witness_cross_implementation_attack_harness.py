#!/usr/bin/env python3
"""Coherent mutation attacks for the SAME_CHART cross-implementation comparator."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
COMPARATOR_PATH = ROOT / "cm2_c27_same_chart_witness_cross_implementation_comparator.py"


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


def load_comparator() -> Any:
    spec = importlib.util.spec_from_file_location("cm2_same_chart_cross_comparator", COMPARATOR_PATH)
    need(spec is not None and spec.loader is not None, "comparator import spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_result(module: Any, path: Path) -> dict[str, Any]:
    return module.closed_object(path)


def load_groups(module: Any, path: Path) -> list[dict[str, Any]]:
    output = list(module.closed_gzip_rows(path, "comparison_row_sha256"))
    need(len(output) == 228, "baseline 228 comparison rows")
    return output


def expected_from_result(result: dict[str, Any]) -> dict[str, Any]:
    source = result["cross_implementation_exact_comparison"]
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
    return {field: source[field] for field in fields}


def reclose(module: Any, row: dict[str, Any]) -> dict[str, Any]:
    body = dict(row)
    body.pop("comparison_row_sha256", None)
    return module.close_comparison_row(body)


def renumber_and_reclose(module: Any, groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for ordinal, row in enumerate(groups):
        body = dict(row)
        body.pop("comparison_row_sha256", None)
        body["ordinal"] = ordinal
        output.append(module.close_comparison_row(body))
    return output


def first_mutation(
    module: Any,
    groups: list[dict[str, Any]],
    callback: Callable[[dict[str, Any]], None],
) -> list[dict[str, Any]]:
    output = copy.deepcopy(groups)
    callback(output[0])
    output[0] = reclose(module, output[0])
    return output


def mutate_drop_group(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    return renumber_and_reclose(module, copy.deepcopy(groups[:-1])), copy.deepcopy(expected)


def mutate_duplicate_group(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    output = copy.deepcopy(groups)
    output.append(copy.deepcopy(output[-1]))
    return renumber_and_reclose(module, output), copy.deepcopy(expected)


def mutate_drop_member(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    def change(row: dict[str, Any]) -> None:
        row["projections"] = row["projections"][:1]
        row["projection_count"] = 1
    return first_mutation(module, groups, change), copy.deepcopy(expected)


def mutate_duplicate_member(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    def change(row: dict[str, Any]) -> None:
        row["projections"].append(copy.deepcopy(row["projections"][-1]))
        row["projections"].sort(key=module.projection_sort_key)
        row["projection_count"] = 3
    return first_mutation(module, groups, change), copy.deepcopy(expected)


def mutate_owner(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    def change(row: dict[str, Any]) -> None:
        row["projections"][0]["owner_member_id"] = "coherent-mutated-owner:" + "0" * 64
        row["projections"].sort(key=module.projection_sort_key)
    return first_mutation(module, groups, change), copy.deepcopy(expected)


def mutate_component(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    def change(row: dict[str, Any]) -> None:
        row["projections"][0]["fresh_component_id"] = "round306c15-source-g-component:" + "0" * 64
        row["projections"].sort(key=module.projection_sort_key)
        row["component_edge"] = sorted(
            {value["fresh_component_id"] for value in row["projections"]},
            key=lambda value: value.encode("ascii"),
        )
    return first_mutation(module, groups, change), copy.deepcopy(expected)


def mutate_bounds_rekey(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    def change(row: dict[str, Any]) -> None:
        row["physical_bounds"][0] = {"kind": "Q", "value": "-999999/1000000"}
        row["group_id"] = "same-chart-exact-equal-positive-volume:" + module.digest([row["chart"], row["physical_bounds"]])
    return first_mutation(module, groups, change), copy.deepcopy(expected)


def mutate_group_id(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    def change(row: dict[str, Any]) -> None:
        row["group_id"] = "same-chart-exact-equal-positive-volume:" + "f" * 64
    return first_mutation(module, groups, change), copy.deepcopy(expected)


def mutate_source_row_sha(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    def change(row: dict[str, Any]) -> None:
        row["projections"][0]["source_row_sha256"] = "e" * 64
        row["projections"].sort(key=module.projection_sort_key)
    return first_mutation(module, groups, change), copy.deepcopy(expected)


def mutate_support_kind(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    def change(row: dict[str, Any]) -> None:
        row["projections"][0]["support_kind"] = "HALF_OPEN_RATIONAL_BOX"
        row["projections"].sort(key=module.projection_sort_key)
    return first_mutation(module, groups, change), copy.deepcopy(expected)


def mutate_stale_row_closure(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    output = copy.deepcopy(groups)
    output[0]["formal_credit"] = 1
    return output, copy.deepcopy(expected)


def mutate_ordinal(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    def change(row: dict[str, Any]) -> None:
        row["ordinal"] = 999
    return first_mutation(module, groups, change), copy.deepcopy(expected)


def mutate_pin(field: str, replacement: Any) -> Callable[[Any, list[dict[str, Any]], dict[str, Any]], tuple[list[dict[str, Any]], dict[str, Any]]]:
    def apply(module: Any, groups: list[dict[str, Any]], expected: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        pins = copy.deepcopy(expected)
        pins[field] = replacement(pins[field]) if callable(replacement) else replacement
        return copy.deepcopy(groups), pins
    return apply


ATTACKS = [
    ("DROP_GROUP_AND_RENUMBER_RECLOSE", mutate_drop_group),
    ("DUPLICATE_GROUP_AND_RENUMBER_RECLOSE", mutate_duplicate_group),
    ("DROP_MEMBER_AND_RECOUNT_RECLOSE", mutate_drop_member),
    ("DUPLICATE_MEMBER_AND_RECOUNT_RECLOSE", mutate_duplicate_member),
    ("MUTATE_MEMBER_OWNER_AND_RESORT_RECLOSE", mutate_owner),
    ("MUTATE_COMPONENT_AND_EDGE_RESORT_RECLOSE", mutate_component),
    ("MUTATE_BOUNDS_AND_COHERENTLY_REKEY_RECLOSE", mutate_bounds_rekey),
    ("MUTATE_GROUP_ID_RECLOSE", mutate_group_id),
    ("MUTATE_SOURCE_ROW_SHA_AND_RESORT_RECLOSE", mutate_source_row_sha),
    ("MUTATE_SUPPORT_KIND_AND_RESORT_RECLOSE", mutate_support_kind),
    ("MUTATE_ROW_WITH_STALE_CLOSURE", mutate_stale_row_closure),
    ("MUTATE_ORDINAL_RECLOSE", mutate_ordinal),
    ("MUTATE_GROUP_COUNT_PIN", mutate_pin("witness_group_count", lambda value: value + 1)),
    ("MUTATE_PROJECTION_COUNT_PIN", mutate_pin("witness_projection_count", lambda value: value + 1)),
    ("MUTATE_GROUP_IDS_HASH_PIN", mutate_pin("group_ids_sha256", "0" * 64)),
    ("MUTATE_FLATTENED_PROJECTION_HASH_PIN", mutate_pin("flattened_projection_sha256", "1" * 64)),
    ("MUTATE_UNIQUE_EDGE_COUNT_PIN", mutate_pin("unique_component_edge_count", lambda value: value + 1)),
    ("MUTATE_AFFECTED_VERTEX_COUNT_PIN", mutate_pin("affected_component_vertex_count", lambda value: value + 1)),
    ("MUTATE_DSU_RANK_PIN", mutate_pin("DSU_rank_reduction", lambda value: value - 1)),
    ("MUTATE_UNIQUE_EDGE_HASH_PIN", mutate_pin("unique_component_edges_sha256", "2" * 64)),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--comparator-result", required=True)
    parser.add_argument("--comparison-ledger", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated -I -B runtime")
    module = load_comparator()
    result_path = Path(args.comparator_result).resolve(strict=True)
    ledger_path = Path(args.comparison_ledger).resolve(strict=True)
    result = load_result(module, result_path)
    groups = load_groups(module, ledger_path)
    expected = expected_from_result(result)
    baseline = module.validate_comparison_groups(groups, expected)
    need(baseline["witness_group_count"] == 228 and baseline["witness_projection_count"] == 456, "baseline exact comparison")

    rejected: list[dict[str, str]] = []
    for name, attack in ATTACKS:
        mutated_groups, mutated_expected = attack(module, groups, expected)
        try:
            module.validate_comparison_groups(mutated_groups, mutated_expected)
        except module.Failure as error:
            rejected.append({"attack": name, "exact_rejection_reason": str(error)})
        else:
            raise Failure("mutation accepted:" + name)
    need(len(rejected) == len(ATTACKS), "all coherent mutations rejected")
    body = {
        "schema": "cm2.c27.same-chart-witness-cross-implementation-comparator.attacks.v1",
        "status": f"PASS_{len(ATTACKS)}_OF_{len(ATTACKS)}_COHERENT_CROSS_IMPLEMENTATION_COMPARATOR_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_count": len(ATTACKS),
        "rejected_count": len(rejected),
        "rejected_attacks": rejected,
        "baseline_result_sha256": result["result_sha256"],
        "baseline_result_file_sha256": file_hash(result_path),
        "baseline_ledger_sha256": file_hash(ledger_path),
        "baseline_group_ids_sha256": expected["group_ids_sha256"],
        "baseline_flattened_projection_sha256": expected["flattened_projection_sha256"],
        "baseline_unique_component_edges_sha256": expected["unique_component_edges_sha256"],
        "tested_mutation_classes": [name for name, _ in ATTACKS],
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    output = {**body, "result_sha256": digest(body)}
    output_path = Path(args.output).resolve()
    output_path.write_bytes(canonical(output) + b"\n")
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, TypeError, ValueError, KeyError, json.JSONDecodeError) as error:
        print("REJECT_SAME_CHART_CROSS_IMPLEMENTATION_ATTACK_HARNESS:" + str(error), file=sys.stderr)
        raise SystemExit(2)
