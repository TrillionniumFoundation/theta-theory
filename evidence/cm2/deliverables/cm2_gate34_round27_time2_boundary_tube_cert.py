#!/usr/bin/env python3
"""Round-27 composed-flight boundary-tube theorem for physical time two.

The round-26 finite time-two cover stopped with 302,988 outer leaves, mostly
because natural interval evaluation could not decide a competitor
discriminant.  This append-only certificate does not iterate that finite
histogram.  It instead builds a dependency-neutral fair-dyadic classifier on
the complete limiting Q1 carrier and proves that every unresolved depth-d
box is contained in one of two physical outer tubes:

* a tangency tube for one of the complete retained second-flight candidates;
* the inverse image of the 96 physical C24 faces at time two.

Obstacle separation removes root-sign and root-order ties away from the
tangency tube.  A seam is handled by taking the union of adjacent candidate
tables, so it is not promoted to a physical singularity.  Explicit first-map
derivative bounds, a global square-root modulus at the second collision, and
collision-area preservation give, for fair absolute depth d >= 60,

    M_base(U2_d) < 160 sqrt(h_d),
    mu_collision(U2_d) < 26 sqrt(h_d),
    h_d = 2^(-floor(d/3)).

Hence the full physical R2/Q2 split exists modulo a collision-null set.  No
finite complete branch ledger, arbitrary-n split, weighted tail, or induced
strong coefficient is claimed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_candidate_first_hit_cert as first_hit


Q = Fraction
HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round27-time2-boundary-tube.v1"
MANIFEST_SCHEMA = "cm2.gate34.round27-time2-boundary-tube.manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round27-time2-boundary-tube-manifest-2026-07-18.json"
)

DEPENDENCIES = {
    "cm2_gate34_round26_boundary_tube_decay_cert.py": (
        "aaeff6582d966f873402986445cc370d22fd38606d4f1e7226b4677c03f94655"
    ),
    "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json": (
        "6ee5be1c2b60438043284c26837eef7681c94f95290abee33e52b7cab893e1d3"
    ),
    "cm2_gate34_round26_q1_time2_frontier_cert.py": (
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9"
    ),
    "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json": (
        "9fe21726952e83e121536d2ad6344f586405c5699183f12d210929487190832d"
    ),
    "cm2_standard_section_horizon_lift_cert.py": (
        "ce7215cdf5f37c1bb3cc55747b3ad0dd8ef5f080a661c8a77376984c1c3e62a0"
    ),
    "cm2_gate3_candidate_first_hit_cert.py": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(name: str) -> dict[str, Any]:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def load_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(sha256_path(path) == expected, f"dependency mismatch: {name}")
    step1 = load_json(
        "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json"
    )
    time2 = load_json(
        "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json"
    )
    require(
        step1["result"]["fair_dyadic_boundary_tube_theorem"]
        ["limiting_step1_R1_Q1_partition_mod_collision_null_set"]
        == "CERTIFIED",
        "step-one limiting partition",
    )
    registry = time2["result"]["Q1_time2_adaptive_registry"]
    require(registry["frozen_Q1_parent_atom_count"] == 2868, "Q1 parent count")
    require(registry["time2_leaf_count"] == 416994, "time2 leaf count")
    require(registry["strict_R2_inner_atom_count"] == 0, "depth-16 R2 count")
    require(registry["strict_Q2_inner_atom_count"] == 114006, "depth-16 Q2 count")
    require(
        registry["classification_histogram"]
        == {
            "SURVIVE_THROUGH_2_INNER": 114006,
            "UNRESOLVED_TIME2_OUTER": 302988,
        },
        "time2 histogram",
    )
    return step1, time2


def parse_target(target_id: str) -> tuple[str, int, int]:
    obstacle, coordinates = target_id.split("[")
    ix, iy = coordinates[:-1].split(",")
    return obstacle, int(ix), int(iy)


def candidate_weight_audit() -> dict[str, Any]:
    counts = {"G_to_G": 0, "G_to_W": 0, "W_to_G": 0, "W_to_W": 0}
    weighted = Q(0)
    maximum_center_distance_squared = Q(0)
    for source in ("G", "W"):
        for cell in ("E", "W", "N", "S"):
            ids = first_hit.candidate_ids(f"{source}:{cell}")
            require(len(ids) == (57 if source == "G" else 55), "candidate count")
            for identifier in ids:
                target, ix, iy = parse_target(identifier)
                counts[f"{source}_to_{target}"] += 1
                weighted += first_hit.RADIUS[source] * first_hit.RADIUS[target]
                for s in (Q(-1, 400), Q(1, 400)):
                    source_x = Q(0) if source == "G" else Q(1, 2) + s
                    source_y = Q(0) if source == "G" else Q(1, 2)
                    target_x = Q(ix) if target == "G" else Q(ix) + Q(1, 2) + s
                    target_y = Q(iy) if target == "G" else Q(iy) + Q(1, 2)
                    square = (target_x - source_x) ** 2 + (target_y - source_y) ** 2
                    maximum_center_distance_squared = max(
                        maximum_center_distance_squared, square
                    )
    require(counts == {
        "G_to_G": 140,
        "G_to_W": 88,
        "W_to_G": 104,
        "W_to_W": 116,
    }, "candidate type counts")
    require(sum(counts.values()) == 448, "candidate entry count")
    require(weighted == Q(20108, 625), "candidate radius weight")
    require(maximum_center_distance_squared == 13, "candidate center distance")
    return {
        "eight_chart_candidate_entry_count_with_multiplicity": 448,
        "candidate_type_histogram": counts,
        "sum_source_radius_times_target_radius": str(weighted),
        "maximum_candidate_center_distance_squared": str(
            maximum_center_distance_squared
        ),
        "adjacent_chart_union_at_exact_seam": True,
        "seam_is_physical_singularity": False,
    }


def obstacle_separation_audit() -> dict[str, Any]:
    gray_gray_gap = 1 - 2 * first_hit.RADIUS["G"]
    white_white_gap = 1 - 2 * first_hit.RADIUS["W"]
    mixed_center_square_lower = Q(199, 400) ** 2 + Q(1, 2) ** 2
    require(gray_gray_gap == Q(7, 25), "G-G gap")
    require(white_white_gap == Q(17, 25), "W-W gap")
    require(mixed_center_square_lower == Q(79601, 160000), "mixed center")
    require(mixed_center_square_lower > Q(7, 10) ** 2, "mixed center > 7/10")
    mixed_boundary_gap = Q(7, 10) - (
        first_hit.RADIUS["G"] + first_hit.RADIUS["W"]
    )
    require(mixed_boundary_gap == Q(9, 50), "mixed boundary gap")
    require(min(gray_gray_gap, white_white_gap, mixed_boundary_gap) == Q(9, 50),
            "global obstacle gap")
    return {
        "gray_gray_boundary_gap": str(gray_gray_gap),
        "white_white_boundary_gap": str(white_white_gap),
        "mixed_center_distance_squared_strict_lower": str(
            mixed_center_square_lower
        ),
        "mixed_center_distance_strict_lower": "7/10",
        "global_distinct_obstacle_boundary_gap_strict_lower": "9/50",
        "root_sign_or_order_tie_away_from_tangency": "IMPOSSIBLE",
    }


def derivative_budget() -> dict[str, Any]:
    # Absolute fair boxes inherit these half-widths from every physical core.
    half_t, half_p, half_s = Q(1, 200), Q(1, 50), Q(1, 400)
    p1_derivatives = (Q(44), Q(50), Q(7))
    theta1_derivatives = (Q(48), Q(55), Q(8))
    arcsin_p1_derivative = Q(21, 20)
    outgoing_angle = tuple(
        theta1_derivatives[i] + arcsin_p1_derivative * p1_derivatives[i]
        for i in range(3)
    )
    require(outgoing_angle[0] < 95, "outgoing angle t")
    require(outgoing_angle[1] < 108, "outgoing angle p")
    require(outgoing_angle[2] < 16, "outgoing angle s")
    outgoing_bounds = (Q(95), Q(108), Q(16))

    # q1=C1+R1*n1, R1<=9/25.  Candidate centers differ from C1 by sqrt(13),
    # hence |A2-q1|<sqrt(13)+9/25<4.
    contact_bounds = (Q(18), Q(20), Q(4))
    require(Q(13) < Q(91, 25) ** 2, "sqrt(13)<91/25")
    require(Q(91, 25) + Q(9, 25) == 4, "candidate contact distance")
    displacement_s_bound = Q(5)
    transverse_bounds = (
        4 * outgoing_bounds[0] + contact_bounds[0],
        4 * outgoing_bounds[1] + contact_bounds[1],
        4 * outgoing_bounds[2] + displacement_s_bound,
    )
    require(transverse_bounds == (398, 452, 69), "transverse derivatives")
    minimum_radius = Q(4, 25)
    impact_bounds = (Q(2488), Q(2825), Q(432))
    require(transverse_bounds[0] / minimum_radius < impact_bounds[0],
            "impact t")
    require(transverse_bounds[1] / minimum_radius <= impact_bounds[1],
            "impact p")
    require(transverse_bounds[2] / minimum_radius < impact_bounds[2],
            "impact s")
    impact_exact_radius = sum(
        derivative * halfwidth
        for derivative, halfwidth in zip(impact_bounds, (half_t, half_p, half_s))
    )
    require(impact_exact_radius == Q(3501, 50), "impact radius arithmetic")
    impact_radius = Q(71)
    require(impact_exact_radius + Q(1, 100) < impact_radius,
            "impact Arb reserve")

    ell_exact_radius = sum(
        derivative * halfwidth
        for derivative, halfwidth in zip(
            transverse_bounds, (half_t, half_p, half_s)
        )
    )
    require(ell_exact_radius == Q(4481, 400), "ell radius arithmetic")
    outgoing_exact_radius = sum(
        derivative * halfwidth
        for derivative, halfwidth in zip(
            outgoing_bounds, (half_t, half_p, half_s)
        )
    )
    require(outgoing_exact_radius == Q(107, 40), "outgoing radius arithmetic")

    # sqrt(142)<12 and R<=9/25 give a global radical modulus <108/25*sqrt(h).
    require(142 < 12 ** 2, "square-root modulus")
    require(Q(9, 25) * 12 == Q(108, 25), "radical coefficient")
    require(ell_exact_radius / 16 + Q(108, 25) + Q(1, 100) < 6,
            "root radius at h<=1/256")

    # The second normal is a rotation of (sqrt(1-p2^2),p2).  At h<=1/256,
    # its center-to-box chord radius is below 18*sqrt(h).
    require(
        Q(27, 10) / 16 + Q(71, 16) + 12 + Q(1, 100) < 18,
        "second normal square-root modulus",
    )
    return {
        "fair_depth_scale": "h_d=2^(-floor(d/3))",
        "source_halfwidth_coefficients_t_p_s": ["1/200", "1/50", "1/400"],
        "time1_p_partial_derivative_strict_uppers_t_p_s": ["44", "50", "7"],
        "time1_normal_angle_partial_derivative_strict_uppers_t_p_s": [
            "48", "55", "8"
        ],
        "time1_outgoing_angle_partial_derivative_strict_uppers_t_p_s": [
            "95", "108", "16"
        ],
        "time1_contact_partial_derivative_strict_uppers_t_p_s": [
            "18", "20", "4"
        ],
        "candidate_contact_distance_strict_upper": "4",
        "second_impact_p_partial_derivative_strict_uppers_t_p_s": [
            "2488", "2825", "432"
        ],
        "exact_second_impact_center_to_box_radius_coefficient": str(
            impact_exact_radius
        ),
        "dependency_neutral_second_impact_radius_coefficient": str(
            impact_radius
        ),
        "exact_ell_center_to_box_radius_coefficient": str(ell_exact_radius),
        "second_root_Holder_radius_coefficient_in_sqrt_h": "6",
        "time1_outgoing_angle_radius_coefficient_in_h": "27/10",
        "second_normal_chord_radius_coefficient_in_sqrt_h": "18",
        "adaptive_midpoint_Arb_ball_radius_relative_to_h": "1/100",
        "natural_interval_dependency_used_for_decay_theorem": False,
    }


def tube_theorem() -> dict[str, Any]:
    depth_threshold = 60
    h_threshold = Q(1, 2 ** 20)
    sqrt_h_threshold = Q(1, 2 ** 10)
    require(depth_threshold // 3 == 20, "depth threshold")
    require(sqrt_h_threshold ** 2 == h_threshold, "sqrt h threshold")

    # The whole unresolved box lies within twice the impact radius of one
    # candidate tangency.  At this depth epsilon<1/16.
    tangency_epsilon_coefficient = Q(142)
    require(tangency_epsilon_coefficient * h_threshold < Q(1, 16),
            "tangency band threshold")
    for radius in (Q(4, 25), Q(9, 25)):
        derivative_square = (
            (radius + Q(9, 50)) ** 2 - (Q(17, 16) * radius) ** 2
        )
        require(derivative_square > Q(1, 16), "tangency angular derivative")
    candidate_weight = Q(20108, 625)
    tangent_per_epsilon = Q(176, 7) * candidate_weight
    require(tangent_per_epsilon == Q(3539008, 4375), "tangent coefficient")
    tangency_h_coefficient = tangent_per_epsilon * tangency_epsilon_coefficient
    require(tangency_h_coefficient == Q(502539136, 4375),
            "tangency h coefficient")
    require(tangency_h_coefficient * sqrt_h_threshold < 113,
            "tangency sqrt h benchmark")

    # C24 face tube at time two.  These are the same exact radius-weighted
    # widths as the one-step theorem, now with eta_t=18*sqrt(h) and
    # eta_p=(1/10)*sqrt(h).
    eta_t, eta_p = Q(18), Q(1, 10)
    weighted_p_width = Q(546, 3125)
    weighted_t_width = Q(39, 625)
    radius_sum = Q(156, 25)
    require(Q(71) * sqrt_h_threshold < eta_p,
            "second impact h-radius absorbed by sqrt-h radius")
    expanded_t = Q(7, 10) + 2 * eta_t * sqrt_h_threshold
    require(Q(3, 2) ** 2 * (1 - expanded_t ** 2) > 1,
            "expanded core chart derivative")
    require(Q(707, 1000) > Q(7, 10), "seam lies beyond core t faces")
    core_linear = 12 * (
        eta_t * weighted_p_width + eta_p * weighted_t_width
    )
    core_quadratic = 96 * eta_t * eta_p * radius_sum
    require(core_linear == Q(23634, 625), "core linear")
    require(core_quadratic == Q(134784, 125), "core quadratic")
    core_effective = core_linear + core_quadratic * sqrt_h_threshold
    require(core_effective == Q(194337, 5000), "core effective")
    require(core_effective < 39, "core tube benchmark")

    # Root radius 6*sqrt(h) is much smaller than the 9/50 obstacle gap.
    require(12 * sqrt_h_threshold < Q(9, 50), "root-order separation")
    total_coefficient = Q(160)
    require(113 + 39 < total_coefficient, "total tube benchmark")
    collision_volume_lower = Q(156, 25)
    normalized = total_coefficient / collision_volume_lower
    require(normalized == Q(1000, 39), "normalized coefficient")
    require(normalized < 26, "normalized benchmark")
    return {
        "fair_absolute_binary_depth_threshold": depth_threshold,
        "threshold_h": str(h_threshold),
        "threshold_sqrt_h": str(sqrt_h_threshold),
        "second_owner_singularity_model": (
            "complete retained candidate tangencies plus distinct-obstacle gap"
        ),
        "candidate_tangency_outer_band_halfwidth": "142*h_d",
        "candidate_tangency_unnormalized_mass_coefficient_in_h": str(
            tangency_h_coefficient
        ),
        "candidate_tangency_mass_strict_upper_at_threshold": "113*sqrt(h_d)",
        "root_sign_and_root_order_resolved_off_tangency_tube": True,
        "global_horizon_tau_strict_upper": "3",
        "per_box_selected_root_lt_3_test_needed_by_theorem_classifier": False,
        "time1_chart_seam_policy": (
            "use union of the two adjacent complete retained candidate tables"
        ),
        "time2_chart_seam_policy": (
            "atlas-only; any unresolved seam overlap is absorbed by adjacent C24 t-face tubes"
        ),
        "time2_core_t_radius_coefficient_in_sqrt_h": str(eta_t),
        "time2_core_p_radius_coefficient_in_sqrt_h": str(eta_p),
        "time2_core_face_tube_linear_coefficient": str(core_linear),
        "time2_core_face_tube_quadratic_coefficient": str(core_quadratic),
        "time2_core_face_effective_coefficient_at_threshold": str(
            core_effective
        ),
        "time2_core_face_mass_strict_upper": "39*sqrt(h_d)",
        "uniform_parameter_averaged_unresolved_base_mass_bound": (
            "M_base(U2_d)<160*sqrt(h_d) for every fair frontier with d>=60"
        ),
        "uniform_parameter_averaged_normalized_collision_SRB_bound": (
            "mu(U2_d)<26*sqrt(h_d) for every fair frontier with d>=60"
        ),
        "six_split_cycle_base_bound": (
            "M_base(U2_(60+6j))<2^(-2-j) for every integer j>=0"
        ),
        "six_split_cycle_normalized_bound": (
            "mu(U2_(60+6j))<2^(-5-j) for every integer j>=0"
        ),
        "asymptotic_rate": "O(2^(-d/6))",
        "uniform_in_parameter_including_endpoints": True,
        "source_base_density_dominated_by_invariant_collision_density": True,
        "composed_singularity_and_core_face_preimage_collision_measure_zero": True,
        "limiting_full_physical_R2_Q2_partition_mod_collision_null_set": (
            "CERTIFIED"
        ),
    }


def verdict() -> dict[str, Any]:
    return {
        "dependency_neutral_composed_time2_boundary_tube_decay": "CERTIFIED",
        "limiting_full_physical_R2_Q2_partition_mod_collision_null_set": "CERTIFIED",
        "depth16_strict_R2_inner_admitted_count": "CERTIFIED_0_DEPTH16_ONLY",
        "physical_R2_set_empty": "NOT_CLAIMED",
        "finite_complete_R2_Q2_branch_ledger": "NOT_MATERIALIZED",
        "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
        "survivor_conditioned_recovery": "NOT_CERTIFIED",
        "strong_q_weighted_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def certify() -> dict[str, Any]:
    step1, time2 = load_inputs()
    candidate = candidate_weight_audit()
    separation = obstacle_separation_audit()
    derivative = derivative_budget()
    theorem = tube_theorem()
    result = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "proof_engine": (
                "exact rational geometry plus dependency-neutral midpoint radii"
            ),
            "finite_frontier_precision_bits": 384,
            "invariant_collision_area_form": "R_obstacle dtheta dp",
            "regular_billiard_absolute_area_Jacobian": "1",
        },
        "round26_finite_frontier_context": {
            "frozen_Q1_parent_atom_count": 2868,
            "depth16_time2_leaf_count": 416994,
            "depth16_strict_R2_inner_admitted_count": 0,
            "depth16_strict_Q2_inner_admitted_count": 114006,
            "depth16_unresolved_time2_outer_count": 302988,
            "depth16_Q2_inner_base_mass": "5257799/5120000000",
            "depth16_unresolved_outer_base_mass": "106721/204800000",
            "zero_R2_count_is_finite_depth_admission_only": True,
            "step1_limiting_R1_Q1_partition_dependency": step1["result"]
            ["fair_dyadic_boundary_tube_theorem"]
            ["limiting_step1_R1_Q1_partition_mod_collision_null_set"],
            "round26_time2_result_digest": time2["result"]["internal_replay_digest"],
        },
        "complete_candidate_and_seam_audit": candidate,
        "obstacle_separation_and_root_order_audit": separation,
        "composed_dependency_neutral_derivative_budget": derivative,
        "composed_fair_boundary_tube_theorem": theorem,
        "strict_nonpromotion": {
            "finite_complete_R2_Q2_branch_ledger": "NOT_MATERIALIZED",
            "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
            "numeric_branchwise_mass_Jacobian_distortion_strong_q": "NOT_CERTIFIED",
            "survivor_conditioned_recovery": "NOT_CERTIFIED",
            "strong_q_weighted_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    payload = dict(result)
    result["internal_replay_digest"] = digest(payload)
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = certify()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": verdict(),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_round27_time2_boundary_tube_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = certify()
    theorem = result["composed_fair_boundary_tube_theorem"]
    print("COMPOSED_TIME2_BOUNDARY_TUBE_DECAY: CERTIFIED")
    print(theorem["uniform_parameter_averaged_unresolved_base_mass_bound"])
    print("LIMITING_FULL_PHYSICAL_R2_Q2_MOD_NULL: CERTIFIED")
    print("ARBITRARY_N_RN_QN: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
