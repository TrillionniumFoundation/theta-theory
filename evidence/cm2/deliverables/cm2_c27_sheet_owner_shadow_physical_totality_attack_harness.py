#!/usr/bin/env python3
"""Coherent mutations against the independent sheet physical-totality gate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
VERIFIER = ROOT / "cm2_c27_sheet_owner_shadow_physical_totality_sqlite_verifier.py"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load_verifier() -> Any:
    spec = importlib.util.spec_from_file_location("sheet_physical_sqlite", VERIFIER)
    need(spec is not None and spec.loader is not None, "verifier module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reclose_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = digest(row)


def reclose_result(result: dict[str, Any]) -> None:
    result.pop("result_sha256", None)
    result["result_sha256"] = digest(result)


def reordinal(rows: list[dict[str, Any]]) -> None:
    for ordinal, row in enumerate(rows):
        row["ordinal"] = ordinal
        reclose_row(row)


State = tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]
Mutation = Callable[[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]], None]


def first_pair(roles: list[dict[str, Any]], source_class: str = "R204") -> tuple[int, int]:
    for index, row in enumerate(roles):
        if row["source_class"] == source_class and row["role"] == "OWNER":
            need(index + 1 < len(roles) and roles[index + 1]["role"] == "SHADOW", "adjacent role pair")
            return index, index + 1
    raise Failure("source-class role pair")


def companion_index(companions: list[dict[str, Any]], sheet_id: str) -> int:
    for index, row in enumerate(companions):
        if row["physical_sheet_id"] == sheet_id:
            return index
    raise Failure("companion lookup")


def role_field(name: str, value: Any, source_class: str = "R204", both: bool = False) -> Mutation:
    def mutate(roles, companions, result):
        owner, shadow = first_pair(roles, source_class)
        targets = (owner, shadow) if both else (owner,)
        for index in targets:
            roles[index][name] = copy.deepcopy(value)
            reclose_row(roles[index])
    return mutate


def companion_field(name: str, value: Any) -> Mutation:
    def mutate(roles, companions, result):
        owner, _ = first_pair(roles)
        index = companion_index(companions, roles[owner]["physical_sheet_id"])
        companions[index][name] = copy.deepcopy(value)
        reclose_row(companions[index])
    return mutate


def result_field(name: str, value: Any) -> Mutation:
    def mutate(roles, companions, result):
        result[name] = copy.deepcopy(value)
        reclose_result(result)
    return mutate


def attacks() -> list[tuple[str, Mutation]]:
    def drop_complete_sheet(roles, companions, result):
        sheet = roles[0]["physical_sheet_id"]
        roles[:] = [row for row in roles if row["physical_sheet_id"] != sheet]
        companions[:] = [row for row in companions if row["physical_sheet_id"] != sheet]
        reordinal(roles)
        reordinal(companions)

    def duplicate_complete_sheet(roles, companions, result):
        roles.insert(2, copy.deepcopy(roles[0]))
        roles.insert(3, copy.deepcopy(roles[1]))
        companions.insert(1, copy.deepcopy(companions[0]))
        reordinal(roles)
        reordinal(companions)

    def swap_role_order(roles, companions, result):
        roles[0], roles[1] = roles[1], roles[0]
        reordinal(roles)

    def coherent_owner_shadow_swap(roles, companions, result):
        owner_index, shadow_index = first_pair(roles)
        owner, shadow = roles[owner_index], roles[shadow_index]
        for row in (owner, shadow):
            row["owner_member_id"], row["shadow_member_id"] = row["shadow_member_id"], row["owner_member_id"]
            row["owner_C15_row_sha256"], row["shadow_C15_row_sha256"] = row["shadow_C15_row_sha256"], row["owner_C15_row_sha256"]
            row["owner_C25_row_sha256"], row["shadow_C25_row_sha256"] = row["shadow_C25_row_sha256"], row["owner_C25_row_sha256"]
        owner["assigned_member_id"] = owner["owner_member_id"]
        shadow["assigned_member_id"] = shadow["shadow_member_id"]
        index = companion_index(companions, owner["physical_sheet_id"])
        companion = companions[index]
        companion["owner_member_id"], companion["shadow_member_id"] = companion["shadow_member_id"], companion["owner_member_id"]
        reclose_row(owner); reclose_row(shadow); reclose_row(companion)

    def coherent_component_forgery(roles, companions, result):
        owner, shadow = first_pair(roles)
        forged = "round306c15-source-g-component:" + "a" * 64
        for index in (owner, shadow):
            roles[index]["fresh_component_id"] = forged
            reclose_row(roles[index])
        companion = companions[companion_index(companions, roles[owner]["physical_sheet_id"])]
        companion["fresh_component_id"] = forged
        reclose_row(companion)

    def coherent_shadow_node_rekey(roles, companions, result):
        owner, shadow = first_pair(roles)
        companion = companions[companion_index(companions, roles[owner]["physical_sheet_id"])]
        new_id = "cm2-c27-independent-shadow-companion:" + "b" * 64
        companion["materialized_shadow_node_id"] = new_id
        preordinal = {key: value for key, value in companion.items() if key not in {"ordinal", "row_sha256"}}
        preordinal_sha = digest(preordinal)
        reclose_row(companion)
        for index in (owner, shadow):
            roles[index]["materialized_shadow_node_id"] = new_id
            roles[index]["materialized_shadow_node_row_sha256"] = preordinal_sha
            reclose_row(roles[index])

    def coherent_mechanism_relabel(roles, companions, result):
        owner, shadow = first_pair(roles)
        for index in (owner, shadow):
            roles[index]["mechanism"] = "R211_ACTIVE_FACTOR_ZERO_SHEET"
            reclose_row(roles[index])
        companion = companions[companion_index(companions, roles[owner]["physical_sheet_id"])]
        companion["mechanism"] = "R211_ACTIVE_FACTOR_ZERO_SHEET"
        reclose_row(companion)

    def coherent_primitive_sha_forgery(roles, companions, result):
        owner, shadow = first_pair(roles)
        forged = "c" * 64
        for index in (owner, shadow):
            roles[index]["primitive_sheet_row_sha256"] = forged
            reclose_row(roles[index])
        companion = companions[companion_index(companions, roles[owner]["physical_sheet_id"])]
        companion["primitive_sheet_row_sha256"] = forged
        reclose_row(companion)

    def coherent_c26_forgery(roles, companions, result):
        owner, shadow = first_pair(roles)
        forged = "d" * 64
        for index in (owner, shadow):
            roles[index]["C26_owner_root_row_sha256"] = forged
            reclose_row(roles[index])
        companion = companions[companion_index(companions, roles[owner]["physical_sheet_id"])]
        companion["C26_owner_root_row_sha256"] = forged
        reclose_row(companion)

    def flip_owner_and_shadow_inclusion(roles, companions, result):
        owner, shadow = first_pair(roles)
        roles[owner]["equality_sheet_included"] = False
        roles[owner]["terminal_disposition"] = "UNIQUE_ADJACENT_SHADOW_EXCLUDED_FROM_EQUALITY_SHEET"
        roles[shadow]["equality_sheet_included"] = True
        roles[shadow]["terminal_disposition"] = "UNIQUE_HALF_OPEN_SHEET_OWNER"
        reclose_row(roles[owner]); reclose_row(roles[shadow])

    def orphan_shadow_companion(roles, companions, result):
        fake = copy.deepcopy(companions[0])
        fake["physical_sheet_id"] += ":ORPHAN"
        companions.append(fake)
        companions.sort(key=lambda row: row["physical_sheet_id"])
        reordinal(companions)

    def result_nested(field: str, child: str, value: Any) -> Mutation:
        def mutate(roles, companions, result):
            result[field][child] = copy.deepcopy(value)
            reclose_result(result)
        return mutate

    return [
        ("A01_DROP_COMPLETE_PHYSICAL_SHEET_CHAIN", drop_complete_sheet),
        ("A02_DUPLICATE_COMPLETE_PHYSICAL_SHEET_CHAIN", duplicate_complete_sheet),
        ("A03_SWAP_CANONICAL_OWNER_SHADOW_ROW_ORDER", swap_role_order),
        ("A04_COHERENT_OWNER_SHADOW_SWAP", coherent_owner_shadow_swap),
        ("A05_COHERENT_COMPONENT_FORGERY", coherent_component_forgery),
        ("A06_COHERENT_SHADOW_NODE_REKEY", coherent_shadow_node_rekey),
        ("A07_COHERENT_MECHANISM_RELABEL", coherent_mechanism_relabel),
        ("A08_COHERENT_PRIMITIVE_SHEET_SHA_FORGERY", coherent_primitive_sha_forgery),
        ("A09_COHERENT_C26_BINDING_FORGERY", coherent_c26_forgery),
        ("A10_REVERSE_HALF_OPEN_INCLUSION", flip_owner_and_shadow_inclusion),
        ("A11_ORPHAN_SHADOW_COMPANION", orphan_shadow_companion),
        ("A12_R204_PHYSICAL_SHEET_ID", role_field("physical_sheet_id", "round204-target-graph-sheet-cell:" + "0" * 64, both=True)),
        ("A13_R204_COORDINATE_CHART", role_field("coordinate_chart", "G:E", both=True)),
        ("A14_R204_AMBIENT_BOX", role_field("exact_ambient_box", ["0", "1", "0", "1", "0", "1"], both=True)),
        ("A15_R204_EQUATION_KIND", role_field("equation_kind", "ACTIVE_FACTOR_EQUALS_ZERO", both=True)),
        ("A16_R204_EQUATION_PARAMETER", role_field("equation_parameter", {"target": "ATTACK", "wall_axis": "X", "integer_wall": 7}, both=True)),
        ("A17_R204_INCLUSION_RULE", role_field("sheet_inclusion_rule", "NEGATIVE_SIDE_OWNS", both=True)),
        ("A18_OWNER_OPEN_SIDE", role_field("open_side_predicate", "TARGET_FACTOR_STRICT_NEGATIVE")),
        ("A19_OWNER_ASSIGNED_MEMBER", role_field("assigned_member_id", "round204-wall-open-region:" + "1" * 64)),
        ("A20_OWNER_TERMINAL_RELABEL", role_field("terminal", "SHEET_SHADOW")),
        ("A21_OWNER_ROLE_RELABEL", role_field("role", "SHADOW")),
        ("A22_OWNER_DISPOSITION_RELABEL", role_field("terminal_disposition", "ATTACK_DISPOSITION")),
        ("A23_OWNER_C15_BINDING", role_field("owner_C15_row_sha256", "2" * 64, both=True)),
        ("A24_SHADOW_C15_BINDING", role_field("shadow_C15_row_sha256", "3" * 64, both=True)),
        ("A25_OWNER_C25_BINDING", role_field("owner_C25_row_sha256", "4" * 64, both=True)),
        ("A26_SHADOW_C25_BINDING", role_field("shadow_C25_row_sha256", "5" * 64, both=True)),
        ("A27_A1_THEOREM_ROW_BINDING", role_field("A1_theorem_row_sha256", "6" * 64, both=True)),
        ("A28_A1_THEOREM_AST_BINDING", role_field("A1_theorem_ast_sha256", "7" * 64, both=True)),
        ("A29_ROLE_FORMAL_CREDIT", role_field("formal_credit", 1)),
        ("A30_R211_ACTIVE_FACTOR", role_field("equation_parameter", {"active_factor": "HPLUS", "inactive_factor": "HMINUS", "inactive_factor_strict_sign": "STRICT_NEGATIVE", "factor_identity_on_sheet": "ATTACK"}, source_class="R211", both=True)),
        ("A31_R211_OWNER_OPEN_CELL", role_field("open_side_predicate", "OUTGOING_CELL_IN_N_OR_S", source_class="R211")),
        ("A32_COMPANION_EQUALITY_INCLUDED", companion_field("equality_sheet_included", True)),
        ("A33_COMPANION_EXCLUSION_REASON", companion_field("exclusion_reason", "ATTACK_REASON")),
        ("A34_COMPANION_SHADOW_OPEN_SIDE", companion_field("shadow_open_side", "TARGET_FACTOR_STRICT_POSITIVE")),
        ("A35_COMPANION_PRIMITIVE_SHADOW_SHA", companion_field("primitive_shadow_region_row_sha256", "8" * 64)),
        ("A36_COMPANION_C15_BINDING", companion_field("shadow_C15_row_sha256", "9" * 64)),
        ("A37_COMPANION_C25_BINDING", companion_field("shadow_C25_row_sha256", "a" * 64)),
        ("A38_COMPANION_SHADOW_AUTHORITY_FLIP", companion_field("C26_shadow_node_was_absent_and_not_used_as_authority", False)),
        ("A39_COMPANION_FORMAL_CREDIT", companion_field("formal_credit", 1)),
        ("A40_RESULT_R204_DENOMINATOR", result_nested("primitive_candidate_generation", "R204_target_factor_sign_partition", 223)),
        ("A41_RESULT_R211_DENOMINATOR", result_nested("primitive_candidate_generation", "R211_factor_sign_and_outgoing_chart_partition", 17_715)),
        ("A42_RESULT_PROJECTION_COMMITMENT", result_field("candidate_projection_sha256", "b" * 64)),
        ("A43_RESULT_UNRESOLVED", result_field("unresolved", 1)),
        ("A44_RESULT_CROSS_COMPONENT_WITNESS", result_field("legal_cross_component_witness", 1)),
        ("A45_RESULT_PHYSICAL_TOTALITY_REJECT", result_field("terminal_physical_totality", "REJECT")),
        ("A46_RESULT_C27_PROMOTION", result_field("C27_C28_C29", "PASS")),
        ("A47_RESULT_CM2_PROMOTION", result_field("CM2", "GO_FOR_CLAIM")),
        ("A48_RESULT_FORMAL_CREDIT", result_field("formal_credit", 1)),
        ("A49_RESULT_DECLARED_SEED", result_field("declared_seed", 0)),
        ("A50_RESULT_INVOCATION_SEED", result_nested("invocation", "command_argv", [])),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output-tag", required=True)
    arguments = parser.parse_args()
    module = load_verifier()
    reference_roles, reference_companions, reference = module.reconstruct_sqlite(arguments.seed)
    supplied_roles, supplied_companions, supplied_result = module.read_candidate(Path(arguments.candidate_dir).resolve())
    module.validate_supplied(
        supplied_roles, supplied_companions, supplied_result,
        reference_roles, reference_companions, reference, arguments.seed,
    )
    rows = []
    for ordinal, (attack_id, mutation) in enumerate(attacks()):
        roles = copy.deepcopy(supplied_roles)
        companions = copy.deepcopy(supplied_companions)
        result = copy.deepcopy(supplied_result)
        mutation(roles, companions, result)
        rejected = False
        boundary = ""
        try:
            module.validate_supplied(
                roles, companions, result, reference_roles,
                reference_companions, reference, arguments.seed,
            )
        except (module.Failure, KeyError, TypeError, ValueError) as error:
            rejected = True
            boundary = type(error).__name__ + ":" + str(error)
        need(rejected, "attack escaped:" + attack_id)
        body = {"ordinal": ordinal, "attack_id": attack_id, "rejected": True, "rejection_boundary": boundary}
        rows.append({**body, "row_sha256": digest(body)})
    need(len(rows) == len(attacks()) == 50, "attack denominator")
    body = {
        "schema": "cm2.c27.sheet-owner-shadow-physical-totality.zero-credit.v1.attack-harness.v1",
        "status": "PASS_50_COHERENT_SHEET_OWNER_SHADOW_PHYSICAL_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_count": 50, "rejected_count": 50, "unexpected_accept_count": 0,
        "attack_rows": rows, "attacks_sha256": digest(rows),
        "baseline_primitive_sheet_count": 17_940, "baseline_role_row_count": 35_880,
        "baseline_shadow_companion_count": 17_940,
        "baseline_candidate_projection_sha256": reference["candidate_projection_sha256"],
        "formal_credit": 0, "C27_C28_C29": "REJECT_PENDING_ALL_20_TERMINAL_GATE", "CM2": "NO-GO_FOR_CLAIM",
    }
    output = {**body, "result_sha256": digest(body)}
    target = AUDIT / arguments.output_tag
    need(not target.exists() and target.parent.resolve() == AUDIT.resolve(), "new direct-child output")
    target.mkdir(mode=0o700)
    (target / "attack_result.json").write_bytes(canonical(output))
    print(canonical({"status": output["status"], "result_sha256": output["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print("REJECT_SHEET_OWNER_SHADOW_PHYSICAL_ATTACKS:" + str(error), file=sys.stderr)
        raise SystemExit(2)
