#!/usr/bin/env python3
"""Coherent mutation attacks for the SINGLE_GRAPHS physical-totality subgate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
VERIFIER = ROOT / "cm2_c27_single_graphs_physical_totality_sqlite_verifier.py"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load_verifier():
    spec = importlib.util.spec_from_file_location("single_sqlite_verifier", VERIFIER)
    need(spec is not None and spec.loader is not None, "verifier import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reclose_row(row: dict[str, Any]) -> None:
    body = dict(row)
    body.pop("candidate_digest", None)
    row["candidate_digest"] = digest(body)


def reclose_result(result: dict[str, Any]) -> None:
    body = dict(result)
    body.pop("result_sha256", None)
    result["result_sha256"] = digest(body)


def first_with(rows: list[dict[str, Any]], predicate: Callable[[dict[str, Any]], bool]) -> dict[str, Any]:
    return next(row for row in rows if predicate(row))


RowMutation = Callable[[list[dict[str, Any]], dict[str, Any]], None]


def field_mutation(path: tuple[Any, ...], value: Any, predicate: Callable[[dict[str, Any]], bool] | None = None) -> RowMutation:
    def apply(rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
        del result
        row = rows[0] if predicate is None else first_with(rows, predicate)
        target: Any = row
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        reclose_row(row)
    return apply


def attacks() -> list[tuple[str, RowMutation]]:
    has_empty = lambda row: any(item.get("role") == "G2B_EXACT_EMPTY_SIDE" for item in row["dispositions"])
    exact_face = lambda row: row.get("graph_class") == "R235_SOURCE_EXACT_FACE_FULL_BASE"

    def drop_root(rows, result):
        del result
        rows.pop(0)

    def duplicate_root(rows, result):
        del result
        rows.insert(1, copy.deepcopy(rows[0]))

    def reorder_roots(rows, result):
        del result
        rows[0], rows[1] = rows[1], rows[0]

    def drop_role(role: str, predicate=None):
        def apply(rows, result):
            del result
            row = rows[0] if predicate is None else first_with(rows, predicate)
            index = next(i for i, item in enumerate(row["dispositions"]) if item["role"] == role)
            row["dispositions"].pop(index)
            reclose_row(row)
        return apply

    def duplicate_role(role: str, predicate=None):
        def apply(rows, result):
            del result
            row = rows[0] if predicate is None else first_with(rows, predicate)
            item = next(item for item in row["dispositions"] if item["role"] == role)
            row["dispositions"].append(copy.deepcopy(item))
            reclose_row(row)
        return apply

    def mutate_disposition(role: str, field: str, value: Any, predicate=None):
        def apply(rows, result):
            del result
            row = rows[0] if predicate is None else first_with(rows, predicate)
            item = next(item for item in row["dispositions"] if item["role"] == role)
            item[field] = value
            reclose_row(row)
        return apply

    def inject_empty(rows, result):
        del result
        row = first_with(rows, lambda item: item["graph_class"] == "R235_TARGET_POSITIVE_PARTIAL_BASE")
        item = copy.deepcopy(next(item for item in row["dispositions"] if item["role"] == "G2B_POSITIVE_SIDE"))
        item["role"] = "G2B_EXACT_EMPTY_SIDE"
        item["support_kernel"] = "C24B"
        row["dispositions"].append(item)
        reclose_row(row)

    def mutate_result(field: str, value: Any):
        def apply(rows, result):
            del rows
            result[field] = value
            reclose_result(result)
        return apply

    return [
        ("drop_single_root", drop_root),
        ("duplicate_single_root", duplicate_root),
        ("reorder_single_roots", reorder_roots),
        ("flip_graph_id", field_mutation(("graph_id",), "round235-single-endpoint:" + "0" * 64)),
        ("flip_graph_class", field_mutation(("graph_class",), "R242_UNIQUE_GRAPH_FULL_PATCH")),
        ("flip_terminal", field_mutation(("terminal",), "OUTGOING_GRAPHS")),
        ("flip_geometry_root", field_mutation(("geometry_root_sha256",), "1" * 64)),
        ("flip_base_ast", field_mutation(("base_domain_ast_sha256",), "2" * 64)),
        ("flip_carrier_ast", field_mutation(("carrier_domain_ast_sha256",), "3" * 64)),
        ("flip_equation_ast", field_mutation(("equation_ast_sha256",), "4" * 64)),
        ("flip_exact_support_ast", field_mutation(("exact_support_ast_sha256",), "5" * 64)),
        ("flip_C10_binding", field_mutation(("C10_row_sha256",), "6" * 64)),
        ("flip_C26_G1_binding", field_mutation(("C26_G1_row_sha256",), "7" * 64)),
        ("drop_G2A_sheet", drop_role("G2A_SHEET")),
        ("duplicate_G2A_sheet", duplicate_role("G2A_SHEET")),
        ("drop_positive_side", drop_role("G2B_POSITIVE_SIDE")),
        ("duplicate_positive_side", duplicate_role("G2B_POSITIVE_SIDE")),
        ("drop_exact_empty_side", drop_role("G2B_EXACT_EMPTY_SIDE", has_empty)),
        ("duplicate_exact_empty_side", duplicate_role("G2B_EXACT_EMPTY_SIDE", has_empty)),
        ("inject_empty_into_partial", inject_empty),
        ("flip_sheet_role", mutate_disposition("G2A_SHEET", "role", "G2B_POSITIVE_SIDE")),
        ("flip_positive_role", mutate_disposition("G2B_POSITIVE_SIDE", "role", "G2B_EXACT_EMPTY_SIDE")),
        ("flip_empty_role", mutate_disposition("G2B_EXACT_EMPTY_SIDE", "role", "G2B_POSITIVE_SIDE", has_empty)),
        ("flip_positive_kernel", mutate_disposition("G2B_POSITIVE_SIDE", "support_kernel", "C24B")),
        ("flip_empty_kernel", mutate_disposition("G2B_EXACT_EMPTY_SIDE", "support_kernel", "C24A", has_empty)),
        ("flip_member_id", mutate_disposition("G2A_SHEET", "member_id", "round306c14-exact-partial-sheet:" + "8" * 64)),
        ("flip_component", mutate_disposition("G2A_SHEET", "fresh_component_id", "round306c15-source-g-component:" + "9" * 64)),
        ("flip_base_root", mutate_disposition("G2A_SHEET", "base_root_id", "round306c14c-exact-partial-sheet-self-root:" + "a" * 64)),
        ("flip_official_key", mutate_disposition("G2A_SHEET", "official_key_id", "gate5-word:000000:" + "b" * 64)),
        ("flip_support_sha", mutate_disposition("G2A_SHEET", "normalized_support_ast_sha256", "c" * 64)),
        ("flip_theorem_sha", mutate_disposition("G2A_SHEET", "semantic_theorem_ast_sha256", "d" * 64)),
        ("flip_C15_binding", mutate_disposition("G2A_SHEET", "C15_row_sha256", "e" * 64)),
        ("flip_C24_binding", mutate_disposition("G2A_SHEET", "C24_row_sha256", "f" * 64)),
        ("flip_C25_binding", mutate_disposition("G2A_SHEET", "C25_row_sha256", "0" * 64)),
        ("flip_C26_binding", mutate_disposition("G2A_SHEET", "C26_row_sha256", "1" * 64)),
        ("flip_exact_face_member", mutate_disposition("G2A_SHEET", "member_id", "round248-wall-sheet:" + "2" * 64, exact_face)),
        ("flip_root_classification_certificate", field_mutation(("physical_totality_certificate", "root_classified_from_C10_before_relation_join"), False)),
        ("flip_one_sheet_certificate", field_mutation(("physical_totality_certificate", "exactly_one_G2A_sheet"), False)),
        ("flip_kernel_exhaustion_certificate", field_mutation(("physical_totality_certificate", "positive_and_exact_empty_registered_G2B_rows_exhaust_C24A_C24B_for_root"), False)),
        ("flip_material_join_certificate", field_mutation(("physical_totality_certificate", "all_dispositions_materially_join_C15_C24_C25_C26"), False)),
        ("flip_unique_assignment_certificate", field_mutation(("physical_totality_certificate", "terminal_assignment_unique_in_full_C10_C24_partition"), False)),
        ("flip_positive_count", field_mutation(("physical_totality_certificate", "G2B_positive_count"), 99)),
        ("inject_unresolved", field_mutation(("physical_totality_certificate", "unresolved"), 1)),
        ("inject_candidate_credit", field_mutation(("formal_credit",), 1)),
        ("mutate_result_root_count", mutate_result("single_root_count", 4983)),
        ("mutate_result_C24_allocation", mutate_result("C24_full_terminal_allocation", {})),
        ("inject_result_unresolved", mutate_result("unresolved_count", 1)),
        ("inject_result_credit", mutate_result("formal_credit", 1)),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output-tag", required=True)
    args = parser.parse_args()
    module = load_verifier()
    reference_rows, reference_result = module.reconstruct_sqlite()
    supplied_rows, supplied_result = module.read_candidate(Path(args.candidate_dir).resolve())
    module.validate_candidate_rows(supplied_rows, reference_rows)
    need(canonical(supplied_result) == canonical(reference_result), "baseline exact result")
    rejected: list[str] = []
    unexpected: list[str] = []
    for name, mutation in attacks():
        candidate_rows = copy.deepcopy(supplied_rows)
        candidate_result = copy.deepcopy(supplied_result)
        mutation(candidate_rows, candidate_result)
        try:
            module.validate_candidate_rows(candidate_rows, reference_rows)
            if canonical(candidate_result) != canonical(reference_result):
                raise module.Failure("candidate result differs from independent reference")
        except module.Failure:
            rejected.append(name)
        else:
            unexpected.append(name)
    need(not unexpected and len(rejected) == len(attacks()) and len(rejected) >= 30, "all coherent attacks rejected")
    body = {
        "schema": "cm2.c27.single-graphs-physical-totality-zero-credit.v1.attack-harness.v1",
        "status": "PASS_48_COHERENT_SINGLE_GRAPH_ATTACKS_REJECTED__ZERO_CREDIT_FAIL_CLOSE",
        "attack_count": len(attacks()),
        "rejected_count": len(rejected),
        "unexpected_accept_count": 0,
        "rejected_attacks": rejected,
        "baseline_candidate_count": 4984,
        "baseline_materialized_disposition_count": 14552,
        "baseline_result_sha256": supplied_result["result_sha256"],
        "reference_result_sha256": reference_result["result_sha256"],
        "formal_credit": 0,
        "unconditional_C27_C28_C29": "REJECT_REMAINS_PENDING_FULL_TWENTY_TERMINAL_GATE",
    }
    need(len(attacks()) == 48, "declared attack denominator")
    result = {**body, "result_sha256": digest(body)}
    target = AUDIT / args.output_tag
    need(not target.exists() and target.parent.resolve() == AUDIT.resolve(), "new direct-child output")
    target.mkdir(mode=0o700)
    (target / "attack_result.json").write_bytes(canonical(result))
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
