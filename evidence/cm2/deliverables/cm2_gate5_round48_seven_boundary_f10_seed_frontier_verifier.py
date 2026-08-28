#!/usr/bin/env python3
"""Fail-closed verifier for the Round-48 seven-boundary F10 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round48_seven_boundary_f10_seed_frontier_cert as cert


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def read(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=strict_object
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def independent_arithmetic() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    gap = Q(36337, 800000)
    radius = Q(9, 25)
    tangency = 30 / gap + 5 / gap**2 + 2 * radius / gap**3
    if tangency != Q(516607461656000000, 47978559724753):
        errors.append("tangency exact arithmetic")
    if not tangency < 10768:
        errors.append("tangency integer relaxation")

    # Independent chart-colour totals from the exact candidate reduction:
    # G has 35 same + 22 cross; W has 29 same + 26 cross.
    moving_tangencies = 12 * (2 * 22) + 12 * (2 * 26)
    all_tangencies = 12 * (2 * 57) + 12 * (2 * 55)
    all_corners = 24 * 121
    moving_corners = 12 * 121
    five_zero = 24 * ((44 + 2) + 2 + 2 + 2 + 2)
    if (moving_tangencies, all_tangencies) != (1152, 2688):
        errors.append("tangency counts")
    if (all_corners, moving_corners, five_zero) != (2904, 1452, 1296):
        errors.append("corner/zero counts")
    if all_tangencies + all_corners + five_zero != 6888:
        errors.append("seven-kind count")

    boundary_cost = 52 * tangency + 121 * 40
    minimum_d1 = 151 * 2**14
    boundary_ratio = boundary_cost / minimum_d1
    core_ratio = Q(192 * 55, minimum_d1)
    total = boundary_ratio + Q(103, 151) + core_ratio
    if boundary_cost != Q(27095804235179804520, 47978559724753):
        errors.append("boundary cost")
    if boundary_ratio != Q(
        3386975529397475565, 14837273637760415744
    ):
        errors.append("boundary ratio")
    if core_ratio != Q(165, 38656):
        errors.append("core ratio")
    if total != Q(13571096530812446357, 14837273637760415744):
        errors.append("formal total")
    if not total < 1:
        errors.append("formal total not subunit")
    return {
        "tangency": tangency,
        "moving_tangencies": moving_tangencies,
        "all_tangencies": all_tangencies,
        "all_corners": all_corners,
        "moving_corners": moving_corners,
        "five_zero": five_zero,
        "boundary_cost": boundary_cost,
        "minimum_d1": minimum_d1,
        "boundary_ratio": boundary_ratio,
        "core_ratio": core_ratio,
        "total": total,
    }, errors


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        if not path.is_file() or path.is_symlink():
            return ["unsafe manifest"]
        source = read(path)
        if source.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("manifest schema")
        if source.get("certificate_sha256") != cert.sha(
            Path(cert.__file__).resolve()
        ):
            errors.append("certificate hash")
        if source.get("verifier_sha256") != cert.sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if source.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")

        replay = cert.build_result()
        if source.get("result") != replay:
            errors.append("result replay")
        if source.get("verdict") != replay["strict_nonpromotion"]:
            errors.append("verdict replay")

        arithmetic, arithmetic_errors = independent_arithmetic()
        errors.extend(arithmetic_errors)
        result = source.get("result", {})
        provenance = result.get("provenance", {})
        if provenance.get("parameter_scope") != (
            "base derivative at s=0 in the fixed horizontal-translation gauge"
        ):
            errors.append("parameter scope")
        if provenance.get("face_scope") != (
            "seven frozen one-step boundary kinds on regular noncorner germs"
        ):
            errors.append("face scope")

        inventory = result.get("seven_boundary_kind_candidate_slot_inventory", {})
        chart_rows = inventory.get("candidate_chart_rows", [])
        if len(chart_rows) != 8:
            errors.append("chart row count")
        if inventory.get("candidate_chart_rows_sha256") != cert.digest(chart_rows):
            errors.append("chart row digest")
        if [row.get("retained_candidate_count") for row in chart_rows] != (
            [57] * 4 + [55] * 4
        ):
            errors.append("retained chart counts")
        if [row.get("cross_colour_candidate_count") for row in chart_rows] != (
            [22] * 4 + [26] * 4
        ):
            errors.append("cross-colour chart counts")
        expected_inventory = {
            "candidate_signed_tangency_slots": arithmetic["all_tangencies"],
            "moving_cross_colour_signed_tangency_slots": arithmetic[
                "moving_tangencies"
            ],
            "stationary_same_colour_signed_tangency_slots": 1536,
            "forward_integer_corner_slots": arithmetic["all_corners"],
            "moving_W_source_corner_slots": arithmetic["moving_corners"],
            "stationary_G_source_corner_slots": 1452,
            "five_zero_speed_candidate_slot_count": arithmetic["five_zero"],
            "seven_kind_candidate_slot_count": 6888,
            "moving_nonzero_base_seed_candidate_slot_count": 2604,
        }
        for key, value in expected_inventory.items():
            if inventory.get(key) != value:
                errors.append(f"inventory {key}")
        if inventory.get(
            "candidate_slot_is_not_claimed_as_nonempty_face_component"
        ) is not True:
            errors.append("candidate/nonempty distinction")

        tangency = result.get("cross_colour_tangency_F10_base_seed", {})
        if tangency.get("signed_density_relative_to_dr") != (
            "a_tan=eta*c*u_y/ell"
        ):
            errors.append("tangency density")
        if tangency.get("C1_cost_exact_strict_upper") != qstr(
            arithmetic["tangency"]
        ):
            errors.append("tangency C1")
        if tangency.get("integer_relaxation_strict_upper") != "10768":
            errors.append("tangency relaxation")
        if tangency.get("same_colour_eta_zero_current") is not True:
            errors.append("same-colour current")
        if tangency.get("status") != "CERTIFIED_REGULAR_BASE_SEED":
            errors.append("tangency status")

        corner = result.get("W_source_integer_corner_F10_base_seed", {})
        if corner.get("C1_cost_strict_upper") != "40":
            errors.append("corner C1")
        if corner.get("G_source_corner_current") != "0":
            errors.append("G corner current")
        if corner.get("status") != "CERTIFIED_REGULAR_BASE_SEED":
            errors.append("corner status")

        zero = result.get("five_zero_speed_F10_base_seeds", {})
        if zero.get("row_count") != 5 or zero.get("candidate_slot_count") != 1296:
            errors.append("zero-speed inventory")
        if zero.get("coarea_density_and_derivatives") != (
            "rho=partial_tau rho=partial_s rho=0"
        ):
            errors.append("zero-speed density")
        if zero.get("zero_collision_trace_measure_claimed") is not False:
            errors.append("zero trace overclaim")

        ledger = result.get("conditional_all_face_charge_ledger", {})
        checks = {
            "per_insertion_collision_boundary_seed_cost_strict_upper": qstr(
                arithmetic["boundary_cost"]
            ),
            "minimum_D1_insertion_charge": str(arithmetic["minimum_d1"]),
            "collision_boundary_formal_D1_ratio": qstr(
                arithmetic["boundary_ratio"]
            ),
            "round47_occurrence_formal_ratio": "103/151",
            "round47_C24_core_formal_ratio": qstr(arithmetic["core_ratio"]),
            "formal_all_face_ratio": qstr(arithmetic["total"]),
            "physical_D1_dominated_all_face_F10_path_charge": "NOT_CERTIFIED",
            "status": "CERTIFIED_ARITHMETIC_TARGET_NOT_A_THEOREM",
        }
        for key, value in checks.items():
            if ledger.get(key) != value:
                errors.append(f"ledger {key}")
        if ledger.get("formal_all_face_ratio_strictly_below_one") is not True:
            errors.append("formal subunit flag")
        if ledger.get("arbitrary_Rn_common_restriction_disintegration_kernel") != (
            "NOT_CERTIFIED"
        ):
            errors.append("measure kernel overclaim")
        if ledger.get("return_depth_weighted_coarea_integrability") != (
            "NOT_CERTIFIED"
        ):
            errors.append("return-depth overclaim")

        install = result.get("arbitrary_Rn_installation_frontier", {})
        if install.get("all_seven_one_step_base_seed_types_have_numeric_values") != (
            "CERTIFIED"
        ):
            errors.append("seven-seed installation")
        if install.get("same_measure_arbitrary_Rn_join") != "NOT_CERTIFIED":
            errors.append("same-measure overclaim")
        if install.get("complete_all_five_face_F10_field") != "NOT_CERTIFIED":
            errors.append("full F10 overclaim")
        if install.get("corner_simultaneous_root_face_intersection_policy") != (
            "cemetery"
        ):
            errors.append("cemetery policy")

        f17 = result.get("F17_bulk_frontier", {})
        if f17.get("nonempty_suffix_safe_bound") != (
            "D_suffix*c_X+c_F13, D_suffix=product_i(150*2^B_i)"
        ):
            errors.append("bulk suffix")
        if f17.get("Piola_cancels_bulk_or_tangential_C1_growth") is not False:
            errors.append("Piola overclaim")
        if f17.get("F17_dynamic_test_or_joint_rank_tail") != "NOT_CERTIFIED":
            errors.append("F17 overclaim")

        maturity = result.get("Gate5_maturity_update", {})
        if maturity.get("previous_global_maturity") != "10/18":
            errors.append("prior maturity")
        if maturity.get("new_global_field_completed") is not None:
            errors.append("field credit overclaim")
        if maturity.get("current_global_maturity") != "10/18":
            errors.append("maturity")
        if maturity.get("complete_18_field_operator_block_count") != 0:
            errors.append("complete block overclaim")

        strict = result.get("strict_nonpromotion", {})
        expected_strict = {
            "seven_boundary_kind_regular_F10_base_seed_join": "CERTIFIED",
            "formal_subunit_all_face_ratio": "CERTIFIED_NOT_A_THEOREM",
            "same_measure_arbitrary_Rn_F10_join": "NOT_CERTIFIED",
            "physical_D1_dominated_all_face_F10_path_charge": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F17_bulk_dynamic_test": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if strict != expected_strict:
            errors.append("strict nonpromotion")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(path: Path) -> tuple[int, int]:
    source = read(path)
    changes: list[tuple[tuple[str, ...], Any]] = [
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "parameter_scope"), "all s"),
        (("result", "provenance", "face_scope"), "including corners"),
        (("result", "seven_boundary_kind_candidate_slot_inventory", "candidate_chart_rows_sha256"), "0" * 64),
        (("result", "seven_boundary_kind_candidate_slot_inventory", "candidate_signed_tangency_slots"), 1),
        (("result", "seven_boundary_kind_candidate_slot_inventory", "moving_cross_colour_signed_tangency_slots"), 1),
        (("result", "seven_boundary_kind_candidate_slot_inventory", "stationary_same_colour_signed_tangency_slots"), 1),
        (("result", "seven_boundary_kind_candidate_slot_inventory", "forward_integer_corner_slots"), 1),
        (("result", "seven_boundary_kind_candidate_slot_inventory", "moving_W_source_corner_slots"), 1),
        (("result", "seven_boundary_kind_candidate_slot_inventory", "five_zero_speed_candidate_slot_count"), 1),
        (("result", "seven_boundary_kind_candidate_slot_inventory", "seven_kind_candidate_slot_count"), 1),
        (("result", "seven_boundary_kind_candidate_slot_inventory", "moving_nonzero_base_seed_candidate_slot_count"), 1),
        (("result", "seven_boundary_kind_candidate_slot_inventory", "candidate_slot_is_not_claimed_as_nonempty_face_component"), False),
        (("result", "cross_colour_tangency_F10_base_seed", "signed_density_relative_to_dr"), "0"),
        (("result", "cross_colour_tangency_F10_base_seed", "C1_cost_exact_strict_upper"), "10768"),
        (("result", "cross_colour_tangency_F10_base_seed", "integer_relaxation_strict_upper"), "10767"),
        (("result", "cross_colour_tangency_F10_base_seed", "same_colour_eta_zero_current"), False),
        (("result", "cross_colour_tangency_F10_base_seed", "status"), "NOT_CERTIFIED"),
        (("result", "W_source_integer_corner_F10_base_seed", "C1_cost_strict_upper"), "39"),
        (("result", "W_source_integer_corner_F10_base_seed", "G_source_corner_current"), "moving"),
        (("result", "W_source_integer_corner_F10_base_seed", "status"), "NOT_CERTIFIED"),
        (("result", "five_zero_speed_F10_base_seeds", "row_count"), 4),
        (("result", "five_zero_speed_F10_base_seeds", "candidate_slot_count"), 0),
        (("result", "five_zero_speed_F10_base_seeds", "coarea_density_and_derivatives"), "unknown"),
        (("result", "five_zero_speed_F10_base_seeds", "zero_collision_trace_measure_claimed"), True),
        (("result", "conditional_all_face_charge_ledger", "per_insertion_collision_boundary_seed_cost_strict_upper"), "0"),
        (("result", "conditional_all_face_charge_ledger", "minimum_D1_insertion_charge"), "1"),
        (("result", "conditional_all_face_charge_ledger", "collision_boundary_formal_D1_ratio"), "1"),
        (("result", "conditional_all_face_charge_ledger", "round47_occurrence_formal_ratio"), "1"),
        (("result", "conditional_all_face_charge_ledger", "round47_C24_core_formal_ratio"), "1"),
        (("result", "conditional_all_face_charge_ledger", "formal_all_face_ratio"), "1"),
        (("result", "conditional_all_face_charge_ledger", "formal_all_face_ratio_strictly_below_one"), False),
        (("result", "conditional_all_face_charge_ledger", "arbitrary_Rn_common_restriction_disintegration_kernel"), "CERTIFIED"),
        (("result", "conditional_all_face_charge_ledger", "return_depth_weighted_coarea_integrability"), "CERTIFIED"),
        (("result", "conditional_all_face_charge_ledger", "physical_D1_dominated_all_face_F10_path_charge"), "CERTIFIED"),
        (("result", "conditional_all_face_charge_ledger", "status"), "CERTIFIED_THEOREM"),
        (("result", "arbitrary_Rn_installation_frontier", "all_seven_one_step_base_seed_types_have_numeric_values"), "NOT_CERTIFIED"),
        (("result", "arbitrary_Rn_installation_frontier", "same_measure_arbitrary_Rn_join"), "CERTIFIED"),
        (("result", "arbitrary_Rn_installation_frontier", "complete_all_five_face_F10_field"), "CERTIFIED"),
        (("result", "arbitrary_Rn_installation_frontier", "corner_simultaneous_root_face_intersection_policy"), "regular"),
        (("result", "F17_bulk_frontier", "nonempty_suffix_safe_bound"), "c_F13"),
        (("result", "F17_bulk_frontier", "Piola_cancels_bulk_or_tangential_C1_growth"), True),
        (("result", "F17_bulk_frontier", "F17_dynamic_test_or_joint_rank_tail"), "CERTIFIED"),
        (("result", "Gate5_maturity_update", "new_global_field_completed"), "F10"),
        (("result", "Gate5_maturity_update", "current_global_maturity"), "11/18"),
        (("result", "Gate5_maturity_update", "complete_18_field_operator_block_count"), 1),
        (("result", "strict_nonpromotion", "same_measure_arbitrary_Rn_F10_join"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_all_face_F10"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "F17_bulk_dynamic_test"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate5"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate5_maturity"), "18/18"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "Gate5_maturity"), "11/18"),
    ]
    mutations: list[tuple[str, str]] = []
    for index, (keys, replacement) in enumerate(changes):
        mutation = copy.deepcopy(source)
        set_path(mutation, keys, replacement)
        mutations.append((f"mutation-{index}.json", json.dumps(mutation)))
    for key, replacement in (
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
    ):
        mutation = copy.deepcopy(source)
        mutation[key] = replacement
        mutations.append((f"mutation-{len(mutations)}.json", json.dumps(mutation)))
    duplicate = path.read_text(encoding="utf-8").rstrip()
    duplicate = duplicate[:-1] + ',"schema":"duplicate"}'
    mutations.append((f"mutation-{len(mutations)}.json", duplicate))

    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for name, body in mutations:
            target = Path(directory) / name
            target.write_text(body, encoding="utf-8")
            rejected += bool(verify(target))
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST
    )
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("AUDIT_MODE: FAIL")
        for error in errors:
            print(error)
        return 1
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
        return 0 if rejected == total else 1
    if args.integrity_only or args.replay:
        print("AUDIT_MODE: PASS")
        return 0
    print("AUDIT_MODE: PASS")
    print("GATE5_MATURITY: 10/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
