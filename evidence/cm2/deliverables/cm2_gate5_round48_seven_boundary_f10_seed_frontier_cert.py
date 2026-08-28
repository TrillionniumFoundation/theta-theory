#!/usr/bin/env python3
"""Round-48 seven-boundary-kind F10 base-seed frontier.

This append-only layer audits the seven frozen one-collision boundary kinds.
Five kinds have identically zero parameter normal velocity in the fixed
horizontal-translation gauge.  The two moving kinds admit explicit regular
noncorner C1 coarea seeds:

* cross-colour candidate tangencies; and
* integer-corner rays whose source obstacle is W.

The resulting finite candidate-slot arithmetic is useful, but it does not
identify the endpoint-coarea, collision-SRB and C24 trace measures on one
arbitrary-R_n disintegration kernel.  The displayed all-face D1 ratio is
therefore a conditional arithmetic target, not a physical path-charge
theorem.  Complete F10 and Gate-5 field credit remain fail-closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round48-seven-boundary-f10-seed-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round48-seven-boundary-f10-seed-frontier-manifest-2026-07-19.json"
)

DEPENDENCIES = {
    "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json": (
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4"
    ),
    "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json": (
        "58a8b27517a55fabd5776e9299802bb656f60733ae86c25941b640be2dfb4e91"
    ),
    "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json": (
        "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8"
    ),
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json": (
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788"
    ),
    "cm2-gate5-round41-physical-parameter-jet-envelopes-manifest-2026-07-19.json": (
        "dd19fd73a01c3aa9868fb9e3c89a039a5e8c97d807b6f57048fddc35c744c2cc"
    ),
    "cm2-gate5-round47-regular-c1dual-f13-manifest-2026-07-19.json": (
        "3415f8533865e9ed907df823c1453ee981f3f1f1d5e04333fc14a90ddb2884d0"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
}

RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}
EPSILON = Q(1, 400)
TAU_MAX = Q(3)
INV_SQRT2_LOWER = Q(707, 1000)
INV_SQRT2_UPPER = Q(708, 1000)

DISK_GAP = Q(36337, 800000)
RADIUS_MAX = Q(9, 25)
MINIMUM_RANK = 14
D1_COEFFICIENT = 151
TANGENCY_C1 = 30 / DISK_GAP + 5 / DISK_GAP**2 + 2 * RADIUS_MAX / DISK_GAP**3
CORNER_C1 = Q(40)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=strict_object
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def vector_interval(
    source: str, obstacle: str, ix: int, iy: int
) -> tuple[Q, Q, Q, Q]:
    if source == "G" and obstacle == "G":
        return Q(ix), Q(ix), Q(iy), Q(iy)
    if source == "G" and obstacle == "W":
        x = Q(2 * ix + 1, 2)
        y = Q(2 * iy + 1, 2)
        return x - EPSILON, x + EPSILON, y, y
    if source == "W" and obstacle == "G":
        x = Q(2 * ix - 1, 2)
        y = Q(2 * iy - 1, 2)
        return x - EPSILON, x + EPSILON, y, y
    return Q(ix), Q(ix), Q(iy), Q(iy)


def square_min_abs(lower: Q, upper: Q) -> Q:
    return Q(0) if lower <= 0 <= upper else min(lower * lower, upper * upper)


def retained_candidate(
    source: str, cell: str, obstacle: str, ix: int, iy: int
) -> bool:
    if obstacle == source and ix == 0 and iy == 0:
        return False
    x0, x1, y0, y1 = vector_interval(source, obstacle, ix, iy)
    distance_squared = square_min_abs(x0, x1) + square_min_abs(y0, y1)
    threshold = TAU_MAX + RADIUS[source] + RADIUS[obstacle]
    if distance_squared >= threshold * threshold:
        return False
    if cell == "E":
        a_upper, b_abs = x1, max(abs(y0), abs(y1))
    elif cell == "W":
        a_upper, b_abs = -x0, max(abs(y0), abs(y1))
    elif cell == "N":
        a_upper, b_abs = y1, max(abs(x0), abs(x1))
    elif cell == "S":
        a_upper, b_abs = -y0, max(abs(x0), abs(x1))
    else:
        raise ValueError("cell")
    if a_upper >= 0:
        support = a_upper + b_abs * INV_SQRT2_UPPER
    else:
        support = a_upper * INV_SQRT2_LOWER + b_abs * INV_SQRT2_UPPER
    return support >= RADIUS[source] - RADIUS[obstacle]


def candidate_chart_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in ("G", "W"):
        for cell in ("E", "W", "N", "S"):
            retained = [
                (obstacle, ix, iy)
                for obstacle in ("G", "W")
                for ix in range(-4, 5)
                for iy in range(-4, 5)
                if retained_candidate(source, cell, obstacle, ix, iy)
            ]
            same = sum(obstacle == source for obstacle, _ix, _iy in retained)
            cross = len(retained) - same
            rows.append(
                {
                    "chart_id": f"{source}:{cell}",
                    "source_obstacle": source,
                    "retained_candidate_count": len(retained),
                    "same_colour_candidate_count": same,
                    "cross_colour_candidate_count": cross,
                    "moving_signed_tangency_sheet_count": 2 * cross,
                    "stationary_signed_tangency_sheet_count": 2 * same,
                }
            )
    return rows


def validate_dependencies() -> None:
    first = load("cm2-gate3-first-hit-atlas-manifest-2026-07-15.json")
    if first["schema"] != "cm2.gate3.first-hit-atlas.v1":
        raise RuntimeError("first-hit schema")
    charts = first["candidate_reduction"]["charts"]
    if [row["retained"] for row in charts] != [57] * 4 + [55] * 4:
        raise RuntimeError("first-hit retained counts")

    roots = load(
        "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json"
    )["result"]
    grammar = roots["physical_branch_slope_and_root_grammar"]
    if grammar["branch_type_count"] != 7:
        raise RuntimeError("seven branch kinds")
    records = roots["positive_seeded_component_boundary_reduction"][
        "source_class_records"
    ]
    if [row["source_obstacle"] for row in records] != ["G", "W"]:
        raise RuntimeError("source classes")
    if [row["seeded_component_count"] for row in records] != [12, 12]:
        raise RuntimeError("source component counts")
    if [
        row["common_physical_reduction"]["physical_signed_tangency_branch_upper"]
        for row in records
    ] != [114, 110]:
        raise RuntimeError("tangency slot counts")
    word = records[0]["common_physical_reduction"][
        "frozen_word_chart_homogeneity_grammar"
    ]
    if word != {
        "coordinate_velocity_zero": 2,
        "endpoint_on_integer_wall": 44,
        "roof_two_oriented_wall_chart_in_word_grammar": True,
        "source_chart_seams": 2,
        "source_target_central_homogeneity_faces": 4,
        "target_chart_seams": 2,
        "transparent_word_total": 167,
        "vertical_horizontal_wall_time_tie": 121,
    }:
        raise RuntimeError("word grammar")

    shell = load(
        "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json"
    )["result"]["exact_parameter_angle_jacobian"]
    if shell["collision_flux_coordinate"] != "dr*dp":
        raise RuntimeError("area coordinate")
    if shell["corrected_positive_face_law"] != (
        "R_source*cp*abs(u_y)/ell_T*dtheta"
    ):
        raise RuntimeError("tangency coarea law")

    f9 = load(
        "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
    )["result"]
    geometry = f9["base_physical_face_geometry"]
    if geometry["global_distinct_disk_boundary_gap_strict_lower"] != qstr(
        DISK_GAP
    ):
        raise RuntimeError("disk gap")
    if geometry["global_circle_tangency_face"][
        "absolute_graph_slope_strict_upper"
    ] != "29":
        raise RuntimeError("tangency slope")
    if geometry["forward_integer_corner_face"][
        "uniform_corner_ray_length_strict_lower"
    ] != "1/2":
        raise RuntimeError("corner ray length")
    if geometry["forward_integer_corner_face"][
        "absolute_graph_slope_strict_upper"
    ] != "9":
        raise RuntimeError("corner slope")

    jets = load(
        "cm2-gate5-round41-physical-parameter-jet-envelopes-manifest-2026-07-19.json"
    )["result"]["all_face_base_parameter_jets"]["seven_boundary_kind_rows"]
    if [row["type"] for row in jets] != [row["type"] for row in grammar["branch_types"]]:
        raise RuntimeError("jet/type join")
    if sum(row["G_s_upper"] == "0" for row in jets) != 5:
        raise RuntimeError("five zero-speed kinds")

    round47 = load(
        "cm2-gate5-round47-regular-c1dual-f13-manifest-2026-07-19.json"
    )["result"]
    target = round47["rank_zero_C24_core_edge_F10_seed"][
        "full_face_join_target_not_a_theorem"
    ]
    if target["formula"] != (
        "103/151+(192*55)/(151*2^14)=26533/38656<1"
    ):
        raise RuntimeError("round47 target")
    if target["same_measure_arbitrary_Rn_join"] != "NOT_CERTIFIED":
        raise RuntimeError("round47 measure frontier")

    d1 = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]["arbitrary_Rn_additive_rank_sum_charge"]
    if d1["pointwise_density"] != "c_D1,n(x)=151*sum_{i=1}^n 2^B_i(x)":
        raise RuntimeError("D1 charge")


def slot_inventory() -> dict[str, Any]:
    charts = candidate_chart_rows()
    expected = {
        "G": (57, 35, 22, 44, 70),
        "W": (55, 29, 26, 52, 58),
    }
    for source, values in expected.items():
        source_rows = [row for row in charts if row["source_obstacle"] == source]
        for row in source_rows:
            observed = (
                row["retained_candidate_count"],
                row["same_colour_candidate_count"],
                row["cross_colour_candidate_count"],
                row["moving_signed_tangency_sheet_count"],
                row["stationary_signed_tangency_sheet_count"],
            )
            if observed != values:
                raise RuntimeError("candidate colour count")

    tangency_total = 12 * 114 + 12 * 110
    tangency_moving = 12 * 44 + 12 * 52
    corner_total = 24 * 121
    corner_moving = 12 * 121
    zero_rows = [
        {
            "type": "target_endpoint_on_wall_or_target_chart_seam",
            "candidate_slot_count": 24 * (44 + 2),
        },
        {
            "type": "target_momentum_homogeneity_face",
            "candidate_slot_count": 24 * 2,
        },
        {
            "type": "coordinate_velocity_zero",
            "candidate_slot_count": 24 * 2,
        },
        {
            "type": "source_endpoint_on_wall_or_source_chart_seam",
            "candidate_slot_count": 24 * 2,
        },
        {
            "type": "source_momentum_homogeneity_face",
            "candidate_slot_count": 24 * 2,
        },
    ]
    zero_total = sum(row["candidate_slot_count"] for row in zero_rows)
    if (tangency_total, tangency_moving, corner_total, corner_moving, zero_total) != (
        2688,
        1152,
        2904,
        1452,
        1296,
    ):
        raise RuntimeError("slot arithmetic")
    return {
        "candidate_chart_rows": charts,
        "candidate_chart_rows_sha256": digest(charts),
        "seeded_component_count": 24,
        "source_component_histogram": {"G": 12, "W": 12},
        "candidate_signed_tangency_slots": tangency_total,
        "moving_cross_colour_signed_tangency_slots": tangency_moving,
        "stationary_same_colour_signed_tangency_slots": (
            tangency_total - tangency_moving
        ),
        "forward_integer_corner_slots": corner_total,
        "moving_W_source_corner_slots": corner_moving,
        "stationary_G_source_corner_slots": corner_total - corner_moving,
        "five_zero_speed_kind_rows": zero_rows,
        "five_zero_speed_candidate_slot_count": zero_total,
        "seven_kind_candidate_slot_count": tangency_total + corner_total + zero_total,
        "moving_nonzero_base_seed_candidate_slot_count": (
            tangency_moving + corner_moving
        ),
        "candidate_slot_is_not_claimed_as_nonempty_face_component": True,
    }


def tangency_seed() -> dict[str, Any]:
    if TANGENCY_C1 != Q(516607461656000000, 47978559724753):
        raise RuntimeError("tangency C1 arithmetic")
    return {
        "scope": "regular noncorner cross-colour candidate tangency germ",
        "collision_area_coordinates": "(r,p=sin(phi)), dr*dp",
        "relative_translation_label": "eta in {-1,1}",
        "signed_density_relative_to_dr": "a_tan=eta*c*u_y/ell",
        "geometric_inputs": {
            "ell_strict_lower": qstr(DISK_GAP),
            "target_radius_upper": qstr(RADIUS_MAX),
            "absolute_tangency_graph_slope_strict_upper": "29",
        },
        "differentiated_bounds": [
            "abs(h_s)<=1/g",
            "abs(ell_r),abs(ell_s)<=1+Rmax/g",
            "abs((u_y)_r),abs((u_y)_s)<=1/g",
            "abs(c_r)<29 and abs(c_s)<=1/g",
            "abs(a_r)<29/g+2/g^2+Rmax/g^3",
            "abs(a_s)<=3/g^2+Rmax/g^3",
        ],
        "unit_tangent_derivative_rule": "abs(partial_tau a)<=abs(partial_r a)",
        "C1_cost_formula": "30/g+5/g^2+2*Rmax/g^3",
        "C1_cost_exact_strict_upper": qstr(TANGENCY_C1),
        "integer_relaxation_strict_upper": "10768",
        "same_colour_eta_zero_current": True,
        "status": "CERTIFIED_REGULAR_BASE_SEED",
    }


def corner_seed() -> dict[str, Any]:
    return {
        "scope": "regular noncorner forward integer-corner ray germ",
        "signed_density_relative_to_dr": "a_corner=c*h_s",
        "geometric_inputs": [
            "corner ray length lambda>1/2",
            "absolute point-caustic graph slope<9",
        ],
        "moving_source_rule": "only W-source charts move relative to the fixed integer lattice",
        "differentiated_bounds": {
            "abs_h_s": "<2",
            "abs_h_rs": "<8",
            "abs_h_ss": "<8",
            "abs_a": "<2",
            "abs_partial_tau_a": "<26",
            "abs_partial_s_a": "<12",
        },
        "C1_cost_strict_upper": qstr(CORNER_C1),
        "G_source_corner_current": "0",
        "status": "CERTIFIED_REGULAR_BASE_SEED",
    }


def zero_speed_seeds(inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        "rows": inventory["five_zero_speed_kind_rows"],
        "row_count": 5,
        "candidate_slot_count": inventory["five_zero_speed_candidate_slot_count"],
        "base_parameter_jets": "G_s=G_xs=G_ss=0",
        "coarea_density_and_derivatives": "rho=partial_tau rho=partial_s rho=0",
        "same_colour_tangencies_are_additional_zero_current_slots": 1536,
        "G_source_integer_corners_are_additional_zero_current_slots": 1452,
        "zero_collision_trace_measure_claimed": False,
        "status": "CERTIFIED_ZERO_PARAMETER_CURRENT",
    }


def conditional_charge_ledger() -> dict[str, Any]:
    boundary_cost = 52 * TANGENCY_C1 + 121 * CORNER_C1
    minimum_d1 = D1_COEFFICIENT * (1 << MINIMUM_RANK)
    boundary_ratio = boundary_cost / minimum_d1
    occurrence_ratio = Q(103, 151)
    core_ratio = Q(192 * 55, 151 * (1 << MINIMUM_RANK))
    formal_total = boundary_ratio + occurrence_ratio + core_ratio
    if boundary_cost != Q(27095804235179804520, 47978559724753):
        raise RuntimeError("boundary cost")
    if boundary_ratio != Q(
        3386975529397475565, 14837273637760415744
    ):
        raise RuntimeError("boundary ratio")
    if core_ratio != Q(165, 38656):
        raise RuntimeError("core ratio")
    if formal_total != Q(
        13571096530812446357, 14837273637760415744
    ):
        raise RuntimeError("formal total")
    if not formal_total < 1:
        raise RuntimeError("formal subunit ratio")
    return {
        "worst_source_class": "W",
        "per_insertion_collision_boundary_seed_cost_strict_upper": qstr(
            boundary_cost
        ),
        "minimum_D1_insertion_charge": str(minimum_d1),
        "collision_boundary_formal_D1_ratio": qstr(boundary_ratio),
        "round47_occurrence_formal_ratio": qstr(occurrence_ratio),
        "round47_C24_core_formal_ratio": qstr(core_ratio),
        "formal_all_face_ratio": qstr(formal_total),
        "formal_all_face_ratio_strictly_below_one": True,
        "strict_subunit_slack": qstr(1 - formal_total),
        "formal_formula": (
            "(52*A_tan+121*40)/(151*2^14)+103/151+"
            "(192*55)/(151*2^14)"
        ),
        "same_measure_warning": (
            "the occurrence term is on the raw endpoint-coarea law, D1 is on collision-SRB, and the core term is a boundary trace"
        ),
        "arbitrary_Rn_common_restriction_disintegration_kernel": "NOT_CERTIFIED",
        "return_depth_weighted_coarea_integrability": "NOT_CERTIFIED",
        "physical_D1_dominated_all_face_F10_path_charge": "NOT_CERTIFIED",
        "status": "CERTIFIED_ARITHMETIC_TARGET_NOT_A_THEOREM",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    inventory = slot_inventory()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "base derivative at s=0 in the fixed horizontal-translation gauge",
            "face_scope": "seven frozen one-step boundary kinds on regular noncorner germs",
            "claim_type": "base F10 seed bounds and conditional all-face charge arithmetic only",
        },
        "seven_boundary_kind_candidate_slot_inventory": inventory,
        "cross_colour_tangency_F10_base_seed": tangency_seed(),
        "W_source_integer_corner_F10_base_seed": corner_seed(),
        "five_zero_speed_F10_base_seeds": zero_speed_seeds(inventory),
        "conditional_all_face_charge_ledger": conditional_charge_ledger(),
        "arbitrary_Rn_installation_frontier": {
            "candidate_instance_token": (
                "(common-Rn-restriction-id,time_j,boundary-kind,primitive-key,connected-rank,F10)"
            ),
            "regular_restriction_preserves_each_base_seed_bound": True,
            "corner_simultaneous_root_face_intersection_policy": "cemetery",
            "artificial_chart_or_homogeneity_cuts_are_physical_F10_faces": False,
            "all_seven_one_step_base_seed_types_have_numeric_values": "CERTIFIED",
            "same_measure_arbitrary_Rn_join": "NOT_CERTIFIED",
            "complete_all_five_face_F10_field": "NOT_CERTIFIED",
        },
        "F17_bulk_frontier": {
            "source_bulk_ratio": "25/151 of c_D1 before suffix propagation",
            "nonempty_suffix_safe_bound": (
                "D_suffix*c_X+c_F13, D_suffix=product_i(150*2^B_i)"
            ),
            "Piola_cancels_bulk_or_tangential_C1_growth": False,
            "F17_dynamic_test_or_joint_rank_tail": "NOT_CERTIFIED",
        },
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayer": "seven one-step boundary-kind regular F10 base seeds",
            "reason_no_new_field_credit": (
                "the common arbitrary-Rn coarea/collision-SRB/core-trace disintegration and weighted return-depth join remain missing"
            ),
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
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
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=(
            HERE / "cm2_gate5_round48_seven_boundary_f10_seed_frontier_verifier.py"
        ),
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(
        "SEVEN_BOUNDARY_KIND_F10_BASE_SEEDS:",
        result["strict_nonpromotion"][
            "seven_boundary_kind_regular_F10_base_seed_join"
        ],
    )
    print("SAME_MEASURE_ARBITRARY_RN_F10: NOT_CERTIFIED")
    print("GATE5_MATURITY: 10/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
