#!/usr/bin/env python3
"""Round123 producer skeleton: stage-3 properization and F14 frontier.

The producer materializes the actual-third output recut for the single
Round121 exact-b seed.  It also constructs the 120 immutable full-key F14
slot identities and the regular-density arithmetic that a later theorem
would use.  Those F14 rows are deliberately fail-closed:

* no Round122 artifact is read or pinned;
* no F14 slot is installed;
* an independent Round123 verifier is still required.

Thus this file is an executable producer skeleton, not an F14 promotion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_round123_rank3_exact_seed_stage3_output_properization_common as stage3


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round123.rank3-stage3-output-properization-f14-frontier.v1"
DEFAULT_OUTPUT = (
    HERE
    / "cm2-round123-rank3-stage3-output-properization-f14-frontier-2026-07-23.json"
)

Q_REGULARITY = Q(93, 100)
THETA_INVERSE = Q(144000, 180337)
DISTORTION_CJ = 15000000000000000000000000
REGULAR_DENSITY_CONE_K = 500000000000000000000000000
DISTORTION_ONLY_FRONTIER_CONSTANT = 13950000000000000000000001
F14_ONE_STEP_FRONTIER_VALUE = 34
F14_THREE_LEG_FRONTIER_PRODUCT = 39304


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def qstr(value: Q) -> str:
    return str(Q(value))


def f14_slot_id(immutable_key: list[Any]) -> str:
    payload = ["round123-gate5-f14-frontier-slot-v1", immutable_key]
    return "round123-gate5-f14-frontier-slot:" + digest(payload)


def regular_density_frontier_theorem() -> dict[str, Any]:
    q = Q_REGULARITY
    theta = THETA_INVERSE
    cj = DISTORTION_CJ
    cone = REGULAR_DENSITY_CONE_K
    one_step = q * cone + cj
    three_step = q**3 * cone + cj * (1 + q + q**2)
    distortion_only = DISTORTION_ONLY_FRONTIER_CONSTANT
    delta = Q(1, 10**90)
    cj_delta = cj * delta
    f14_margin = (
        Q(F14_ONE_STEP_FRONTIER_VALUE)
        - Q(100, 3)
        - (1 + cj) * delta
    )
    direct_three_leg_distortion = cj * (1 + q + q**2)
    require(
        direct_three_leg_distortion
        == 41923500000000000000000000,
        "direct three-leg distortion",
    )
    direct_three_leg_margin = (
        Q(F14_ONE_STEP_FRONTIER_VALUE)
        - Q(100, 3)
        - (1 + direct_three_leg_distortion) * delta
    )

    require(theta < q**3, "theta must be strictly below q^3")
    require(one_step < cone, "one-step regular-density cone margin")
    require(three_step < cone, "three-step regular-density cone margin")
    require(
        distortion_only == 1 + q * cj,
        "distortion-only frontier arithmetic",
    )
    theta_cross_margin = (
        93**3 * 180337 - 144000 * 100**3
    )
    require(theta_cross_margin == 1055328309, "theta exact cross-margin")
    require(
        F14_ONE_STEP_FRONTIER_VALUE >= 1
        and Q(F14_ONE_STEP_FRONTIER_VALUE) >= q,
        "F14 unit and regularity coefficients",
    )
    require(f14_margin > 0, "F14 inverse-length and distortion margin")
    require(
        direct_three_leg_margin > 0,
        "direct three-leg accepted-norm margin",
    )
    require(
        F14_ONE_STEP_FRONTIER_VALUE**3
        == F14_THREE_LEG_FRONTIER_PRODUCT,
        "three-leg F14 product",
    )

    return {
        "status": "COMPLETE_F14_THEOREM_INTERFACE__FAIL_CLOSED_NOT_INSTALLED",
        "accepted_regular_density_norm": "N=M*(1+Reg+1/L)",
        "input_scope": (
            "every positive normalized density rho on each of the"
            " 24 exact-seed common children"
        ),
        "authoritative_one_step_recurrence": (
            "Reg_out <= (93/100)*Reg_in + C_J"
        ),
        "warning": "C_J is additive and is not multiplied by 93/100",
        "q": qstr(q),
        "theta_inverse": qstr(theta),
        "theta_strictly_less_than_q_cubed": True,
        "theta_q_cubed_integer_cross_margin": theta_cross_margin,
        "C_J": str(cj),
        "regular_density_cone_K": str(cone),
        "one_step_cone_image_upper": str(one_step),
        "one_step_cone_margin": str(cone - one_step),
        "three_step_cone_image_upper": str(three_step),
        "three_step_cone_margin": str(cone - three_step),
        "distortion_only_frontier_constant": str(distortion_only),
        "distortion_only_constant_identity": "1+(93/100)*C_J",
        "distortion_only_constant_is_an_accepted_F14_cost": False,
        "every_leg_input_length_less_or_equal": "delta=10^-90",
        "rejected_fragmentwise_bound": (
            "C14*M_fragment does not control the accepted"
            " M_fragment/ell_fragment norm term"
        ),
        "leg_output_length_strict_lowers": {
            "stage1": "(3/100)*delta",
            "stage2": "(17/200)*delta",
            "stage3": "(4/125)*delta",
            "uniform": "(3/100)*delta",
        },
        "certified_family_level_mass_weighted_bound": (
            "sum_fragment M_fragment/ell_fragment"
            " < (100/(3*delta))*M_input_child"
        ),
        "one_leg_accepted_norm_bound": (
            "N_out < M*(1+(93/100)*Reg_in+C_J"
            "+100/(3*delta))"
        ),
        "C_J_times_delta": qstr(cj_delta),
        "F14_one_step_frontier_value": F14_ONE_STEP_FRONTIER_VALUE,
        "F14_one_step_exact_margin": qstr(f14_margin),
        "F14_three_leg_conservative_product": (
            F14_THREE_LEG_FRONTIER_PRODUCT
        ),
        "direct_three_leg_distortion_B": str(
            direct_three_leg_distortion
        ),
        "direct_three_leg_F14_frontier_value": (
            F14_ONE_STEP_FRONTIER_VALUE
        ),
        "direct_three_leg_exact_margin": qstr(
            direct_three_leg_margin
        ),
        "direct_three_leg_value_is_not_a_one_step_slot_value": True,
        "slot_value_is_one_step_not_three_step": True,
        "physical_collision_factor_count": 3,
        "roof_level_slot_count_per_subbranch": 5,
        "generic_composition_is_34_cubed_not_34_to_the_fifth": True,
        "restriction_and_conditional_normalization_do_not_increase_Reg": True,
        "zero_mass_output_members_are_omitted": True,
        "mass_conservation": "sum_output_member_masses=M_input_child",
        "signed_Jordan_extension": (
            "apply the positive theorem separately to positive and negative"
            " Jordan parts and add the two accepted norms"
        ),
        "fragment_number_does_not_multiply_the_mass_weighted_bound": True,
        "arbitrary_fragment_masses_are_symbolic_and_not_assumed_equal": True,
        "source_full_key_F14_frontier_slot_count": 120,
        "output_fragment_F14_slot_count": 0,
        "transparent_wall_roof_split_adds_no_operator_factor": True,
        "round122_final_F10_F13_F16_bridge_pin": "PENDING",
        "independent_round123_replay": "PENDING",
        "F14_theorem_installed": False,
    }


def build_f14_frontier_slots(
    round121: dict[str, Any],
    partitions: list[dict[str, Any]],
    leg_output_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    partition_by_child = {
        row["input_common_child_id"]: row for row in partitions
    }
    require(len(partition_by_child) == 24, "24 input-child partitions")
    leg_by_child_and_index = {
        (row["common_child_id"], row["leg_index"]): row
        for row in leg_output_rows
    }
    require(len(leg_by_child_and_index) == 72, "72 leg-output rows")

    # F1 has exactly one row for every full-key roof coordinate.  Reusing
    # those coordinates avoids collapsing roof=2 into a collision index.
    coordinates = [
        row
        for row in round121["gate5_F1_F6_slot_rows"]
        if row["field_index"] == 1
    ]
    require(len(coordinates) == 120, "120 full-key roof coordinates")
    coordinates.sort(
        key=lambda row: canonical(
            [
                row["official_word_key_id"],
                row["refined_homogeneous_subbranch_id"],
                row["roof_level_j"],
            ]
        )
    )

    rows: list[dict[str, Any]] = []
    keys: set[str] = set()
    ids: set[str] = set()
    for coordinate in coordinates:
        child_id = coordinate["common_child_id"]
        partition = partition_by_child[child_id]
        leg_index = coordinate["stage"]
        leg_row = leg_by_child_and_index[(child_id, leg_index)]
        immutable_key = [
            coordinate["official_word_key_id"],
            coordinate["refined_homogeneous_subbranch_id"],
            coordinate["roof_level_j"],
            "regular_density_operator_cost",
        ]
        key_text = canonical(immutable_key)
        require(key_text not in keys, "unique F14 immutable key")
        keys.add(key_text)
        slot_id = f14_slot_id(immutable_key)
        require(slot_id not in ids, "unique F14 slot ID")
        ids.add(slot_id)
        row = {
            "slot_id": slot_id,
            "immutable_slot_key": immutable_key,
            "official_word_key_id": coordinate["official_word_key_id"],
            "refined_homogeneous_subbranch_id": coordinate[
                "refined_homogeneous_subbranch_id"
            ],
            "roof_level_j": coordinate["roof_level_j"],
            "field_index": 14,
            "field_name": "regular_density_operator_cost",
            "common_child_id": child_id,
            "input_common_rank": partition["input_common_rank"],
            "leg_index": leg_index,
            "accepted_norm_leg_output_row_id": leg_row[
                "leg_output_row_id"
            ],
            "output_member_count": leg_row["output_member_count"],
            "output_member_ids": leg_row["output_member_ids"],
            "field_value": "NOT_INSTALLED",
            "F14_one_step_frontier_value": F14_ONE_STEP_FRONTIER_VALUE,
            "F14_three_leg_frontier_product": (
                F14_THREE_LEG_FRONTIER_PRODUCT
            ),
            "slot_value_is_one_step_not_three_step": True,
            "transparent_wall_roof_split_adds_no_operator_factor": True,
            "distortion_only_frontier_constant": str(
                DISTORTION_ONLY_FRONTIER_CONSTANT
            ),
            "distortion_only_constant_is_an_accepted_F14_cost": False,
            "certified_mass_weighted_inverse_length_assembly": (
                "sum_fragment M_fragment/ell_fragment"
                "<(100/(3*delta))*M_input_child"
            ),
            "slot_status": "FRONTIER_ONLY__FAIL_CLOSED__NOT_INSTALLED",
            "blocking_dependencies": [
                "FINAL_ROUND122_F10_F13_F16_BRIDGE_PIN",
                "INDEPENDENT_ROUND123_STAGE3_AND_F14_VERIFIER",
            ],
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    require(len(rows) == 120, "F14 frontier slot count")
    return rows


def build(bits: int, bisections: int) -> dict[str, Any]:
    stage3_document = stage3.build(bits, bisections)
    stage3_result = dict(stage3_document["result"])
    stage3_result.pop("status")
    round121 = stage3.load_round121()

    f14_rows = build_f14_frontier_slots(
        round121,
        stage3_result["input_child_output_partition_rows"],
        stage3_result["accepted_norm_leg_output_rows"],
    )
    gate_status = dict(round121["gate5_actual_child_field_status"])
    require(
        gate_status["F14"]
        == "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
        "Round121 F14 remains uninstalled",
    )

    strict_nonclaims = list(stage3_result["strict_nonclaims"])
    strict_nonclaims.extend(
        [
            "the pending Round122 bridge is not read or pinned",
            "the 120 F14 rows are frontier identities, not installed slots",
            "the distortion-only constant is not an accepted F14 cost",
            "child-local maturity remains 6/18 in this standalone chain",
            "the hypothetical post-Round122 F14 maturity 15/18 is not claimed",
        ]
    )
    stage3_result["strict_nonclaims"] = strict_nonclaims
    stage3_result.update(
        {
            "status": (
                "PRODUCER_SKELETON__STAGE3_OUTPUT_MATERIALIZED"
                "__F14_FAIL_CLOSED"
            ),
            "regular_density_frontier_theorem": (
                regular_density_frontier_theorem()
            ),
            "gate5_F14_frontier_slot_rows": f14_rows,
            "gate5_F14_frontier_slot_rows_sha256": digest(f14_rows),
            "F14_frontier_slot_count": len(f14_rows),
            "F14_installed_slot_count": 0,
            "F14_installation_gate": {
                "stage3_output_properization_materialized_by_producer": True,
                "all_72_leg_outputs_independently_verified": False,
                "final_round122_bridge_pinned": False,
                "independent_round123_verifier_passed": False,
                "all_required_conditions_met": False,
                "fail_closed": True,
            },
            "gate5_actual_child_field_status": gate_status,
            "rank3_seed_child_field_maturity": "6/18",
            "candidate_maturity_after_future_R122_and_F14": (
                "15/18__FRONTIER_ONLY__NOT_INSTALLED"
            ),
            "gate5_global_maturity": "10/18",
            "complete_18_field_block_count": 0,
            "cm2_verdict": "NO-GO_FOR_CLAIM",
        }
    )
    result = stage3_result
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", type=int, default=stage3.DEFAULT_BITS)
    parser.add_argument(
        "--bisections", type=int, default=stage3.DEFAULT_BISECTIONS
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    document = build(args.bits, args.bisections)
    text = json.dumps(document, sort_keys=True, indent=2, allow_nan=False) + "\n"
    args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
