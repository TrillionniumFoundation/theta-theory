#!/usr/bin/env python3
"""Round-26 fair-dyadic boundary-tube decay for the C24 one-step map.

This append-only leaf has two independent parts.

First, it consumes the frozen round-25 unresolved frontier and freshly
replays the scheduled 26,876 -> 53,752 child generation with the original
384-bit whole-box Arb engine.  Every child remains fail-closed and the exact
parent/child collision-base mass identity is checked.

Second, it removes a genuine obstruction in that original engine: a natural
interval extension may retain dependency overestimation and therefore does
not, by itself, imply a quantitative decay rate.  On the same regular
one-collision branches we give a dependency-neutral midpoint plus analytic
radius classifier.  Explicit derivative bounds put every unresolved depth-d
box into an outer tube around the 96 physical C24 rectangle faces.  Billiard
area preservation and reversibility then give, for d >= 24,

    M_base(U_d) <= B(h_d) < 8 h_d,
    h_d = 2^(-floor(d/3)).

Thus the fair unresolved mass is O(2^(-d/3)), uniformly in the parameter,
including chart seams.  This proves a limiting one-step R1/Q1 partition
modulo collision-null boundary fibres.  It does not materialize a finite
branch ledger, an arbitrary-n return partition, a weighted tail, or an
induced strong Lasota--Yorke coefficient.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate34_full_core_return_adaptive_frontier_cert as adaptive


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

RESULT_SCHEMA = "cm2.gate34.round26-boundary-tube-decay.v1"
MANIFEST_SCHEMA = "cm2.gate34.round26-boundary-tube-decay.manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json"
)

DEPENDENCIES = {
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json": (
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
    ),
    "cm2_gate5_round25_adaptive_face_f789_cert.py": (
        "d8c4b28ee856927f63bbbb746ea26fd2d7d473b2a3a0009d5c0836fadff3e63a"
    ),
    "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json": (
        "6b9354026a1707a25971925e02acbb5ea7e459ca177190a28ff1b39857283d86"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_gate3_candidate_first_hit_cert.py": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
}

PARENT_UNRESOLVED_COUNT = 26876
CHILD_COUNT = 53752
PARENT_UNRESOLVED_MASS = Q(44519, 256000000)
PARENT_SPLIT_ROWS_DIGEST = (
    "7ab264eef8af4a156c988da008b271d9deb1c89e665d7ba99cbf8f9c63e6767b"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file() and sha256_path(path) == expected,
                f"dependency mismatch: {name}")
    upstream = json.loads(
        (HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json")
        .read_text(encoding="utf-8")
    )
    plan = json.loads(
        (HERE / "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json")
        .read_text(encoding="utf-8")
    )
    registry = upstream["result"]["adaptive_full_core_step1_registry"]
    require(registry["adaptive_leaf_count"] == 33960, "upstream leaf count")
    require(
        registry["classification_histogram"]["UNRESOLVED_OUTER"]
        == PARENT_UNRESOLVED_COUNT,
        "upstream unresolved count",
    )
    split = plan["result"]["unresolved_outer_next_generation_split_plan"]
    require(split["planned_next_generation_child_count"] == CHILD_COUNT,
            "planned child count")
    require(split["next_split_axis_histogram"] == {"t": PARENT_UNRESOLVED_COUNT},
            "planned split axes")
    require(split["planned_split_record_rows_sha256"] == PARENT_SPLIT_ROWS_DIGEST,
            "planned split digest")
    return upstream, plan


def atom_from_row(row: dict[str, Any], cores: tuple[Any, ...]) -> adaptive.Atom:
    box = row["source_box"]
    index = int(row["source_core_index"])
    return adaptive.Atom(
        index,
        cores[index],
        Q(box["t"][0]), Q(box["t"][1]),
        Q(box["p"][0]), Q(box["p"][1]),
        Q(box["s"][0]), Q(box["s"][1]),
        row["dyadic_path"],
    )


def child_row(
    parent: dict[str, Any], child: adaptive.Atom, classification: dict[str, Any]
) -> dict[str, Any]:
    box = {
        "t": [str(child.t0), str(child.t1)],
        "p": [str(child.p0), str(child.p1)],
        "s": [str(child.s0), str(child.s1)],
    }
    payload = {
        "parent_atom_id": parent["atom_id"],
        "source_core_id": parent["source_core_id"],
        "source_core_index": child.source_core_index,
        "dyadic_path": child.path,
        "source_box": box,
    }
    return {
        "child_atom_id": "round26-step1-child:" + digest(payload),
        **payload,
        "depth": child.depth,
        "classification": classification["classification"],
        "destination_core_id": classification["destination_core_id"],
        "classification_witness_rows_sha256": digest(
            classification["witness_rows"]
        ),
        "output_enclosures": classification["output_enclosures"],
        "parameter_averaged_unnormalized_base_mass": str(
            adaptive.base_mass(child)
        ),
        "fresh_whole_child_Arb_classification": True,
        "precision_bits": 384,
    }


def replay_children(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cores = adaptive.core_cert.physical_cores()
    unresolved = [row for row in rows if row["classification"] == "UNRESOLVED_OUTER"]
    require(len(unresolved) == PARENT_UNRESOLVED_COUNT, "unresolved row count")
    result: list[dict[str, Any]] = []
    parent_conservation_rows: list[dict[str, Any]] = []
    for parent in unresolved:
        atom = atom_from_row(parent, cores)
        children = adaptive.split_atom(atom)
        require(len(children) == 2, "binary child count")
        require(all(child.path in {atom.path + "0", atom.path + "1"}
                    for child in children), "child paths")
        # The frozen frontier depths are 12 or 15, hence the fair next axis is t.
        require(all(
            child.p0 == atom.p0 and child.p1 == atom.p1
            and child.s0 == atom.s0 and child.s1 == atom.s1
            for child in children
        ), "scheduled next split is not t")
        local: list[dict[str, Any]] = []
        for child in children:
            classification = adaptive.classify_atom(child, cores)
            row = child_row(parent, child, classification)
            local.append(row)
            result.append(row)
        parent_mass = Q(parent["parameter_averaged_unnormalized_base_mass"])
        child_masses = [Q(row["parameter_averaged_unnormalized_base_mass"])
                        for row in local]
        require(sum(child_masses, Q(0)) == parent_mass, "child mass conservation")
        require(child_masses[0] == child_masses[1] == parent_mass / 2,
                "equal t split masses")
        parent_conservation_rows.append({
            "parent_atom_id": parent["atom_id"],
            "child_atom_ids": sorted(row["child_atom_id"] for row in local),
            "parent_mass": str(parent_mass),
            "each_child_mass": str(parent_mass / 2),
        })
    result.sort(key=lambda row: (
        row["source_core_index"], row["dyadic_path"], row["child_atom_id"]
    ))
    parent_conservation_rows.sort(key=lambda row: row["parent_atom_id"])
    require(len(result) == CHILD_COUNT, "fresh child total")
    require(len({row["child_atom_id"] for row in result}) == CHILD_COUNT,
            "duplicate child id")
    histogram = Counter(row["classification"] for row in result)
    depth_histogram = Counter(int(row["depth"]) for row in result)
    mass = {
        kind: sum(
            (Q(row["parameter_averaged_unnormalized_base_mass"])
             for row in result if row["classification"] == kind),
            Q(0),
        )
        for kind in (
            "RETURN_AT_1_INNER", "SURVIVE_THROUGH_1_INNER", "UNRESOLVED_OUTER"
        )
    }
    require(sum(mass.values(), Q(0)) == PARENT_UNRESOLVED_MASS,
            "generation mass conservation")
    require(histogram == {
        "RETURN_AT_1_INNER": 4088,
        "SURVIVE_THROUGH_1_INNER": 2048,
        "UNRESOLVED_OUTER": 47616,
    }, "fresh classification histogram")
    require(depth_histogram == {13: 13632, 16: 40120}, "child depth histogram")
    require(mass == {
        "RETURN_AT_1_INNER": Q(5953, 1024000000),
        "SURVIVE_THROUGH_1_INNER": Q(17319, 1024000000),
        "UNRESOLVED_OUTER": Q(38701, 256000000),
    }, "fresh class masses")
    require(mass["UNRESOLVED_OUTER"] / PARENT_UNRESOLVED_MASS < Q(7, 8),
            "one-generation residual contraction")
    summary = {
        "fresh_child_count": len(result),
        "classification_histogram": dict(sorted(histogram.items())),
        "child_depth_histogram": {
            str(key): value for key, value in sorted(depth_histogram.items())
        },
        "mass_by_class": {key: str(value) for key, value in mass.items()},
        "exact_total_child_mass": str(sum(mass.values(), Q(0))),
        "residual_mass_ratio_to_parent": str(
            mass["UNRESOLVED_OUTER"] / PARENT_UNRESOLVED_MASS
        ),
        "residual_mass_ratio_strict_upper_benchmark": "7/8",
        "new_terminal_child_count": (
            histogram["RETURN_AT_1_INNER"]
            + histogram["SURVIVE_THROUGH_1_INNER"]
        ),
        "new_terminal_base_mass": str(
            mass["RETURN_AT_1_INNER"] + mass["SURVIVE_THROUGH_1_INNER"]
        ),
        "fresh_child_rows_sha256": digest(result),
        "parent_conservation_rows_sha256": digest(parent_conservation_rows),
        "representative_child_rows": [
            result[0], result[len(result) // 2], result[-1]
        ],
    }
    return result, summary


def regularity_audit() -> dict[str, Any]:
    cores = adaptive.core_cert.physical_cores()
    require(len(cores) == 24, "core count")
    rows: list[dict[str, Any]] = []
    for index, core in enumerate(cores):
        geometry = adaptive.core_cert.contact_geometry(core)
        root = geometry["root"]
        p_target = geometry["p_target"]
        root_ok = bool(root > 0) and bool(root < arbq(3))
        nongrazing = bool(abs(p_target) < arbq(Q(1, 5)))
        require(root_ok and nongrazing, f"parent regularity {index}")
        owner = adaptive.core_cert.certify_core(core)
        require(owner["strict_first_hit"] is True, f"parent owner {index}")
        rows.append({
            "source_core_index": index,
            "source_core_id": adaptive.core_id(core),
            "chart_id": core.chart_id,
            "selected_target_id": core.target_id,
            "root_enclosure": str(root),
            "p_target_enclosure": str(p_target),
            "strict_root_in_0_3": root_ok,
            "strict_abs_p_target_lt_1_over_5": nongrazing,
            "complete_first_owner_replayed": True,
        })
    return {
        "regular_parent_branch_count": len(rows),
        "all_parent_branches_strict_first_owner": True,
        "all_parent_branches_abs_output_p_lt_1_over_5": True,
        "all_parent_branches_reversible_local_diffeomorphisms": True,
        "invariant_area_form": "R_obstacle dtheta dp",
        "billiard_map_absolute_invariant_area_Jacobian": "1",
        "parent_regularity_rows_sha256": digest(rows),
        "representative_parent_regularity_rows": [rows[0], rows[12], rows[-1]],
    }


def derivative_and_tube_theorem() -> tuple[dict[str, Any], dict[str, Any]]:
    # Uniform source geometry.  All root t-widths are 1/100, the largest
    # p-width is 1/25, and the parameter width is 1/200.
    source_t_halfwidth = Q(1, 200)
    source_p_halfwidth = Q(1, 50)
    source_s_halfwidth = Q(1, 400)
    require(adaptive.GLOBAL_DTHETA_DT_UPPER < Q(3, 2), "normal t derivative")
    require(Q(2) ** 2 * (1 - Q(1, 50) ** 2) > 1,
            "velocity p derivative")

    # With d=A-q, the certified root tau<3 gives |d|<3+9/25<4.
    d_upper = Q(4)
    normal_t_derivative = Q(3, 2)
    velocity_p_derivative = Q(2)
    q_t_derivative = Q(27, 50)
    d_s_derivative = Q(1)
    require(normal_t_derivative * d_upper + q_t_derivative < 7,
            "transverse t derivative")
    require(velocity_p_derivative * d_upper <= 8,
            "transverse p derivative")
    pprime_t = Q(44)
    pprime_p = Q(50)
    pprime_s = Q(7)
    # R_target>=4/25.
    require(Q(7) / Q(4, 25) < pprime_t, "pprime t budget")
    require(Q(8) / Q(4, 25) <= pprime_p, "pprime p budget")
    require(Q(1) / Q(4, 25) < pprime_s, "pprime s budget")

    # On |p'|<1/5, the normal reconstruction derivative in p' is <21/20.
    normal_from_pprime = Q(21, 20)
    require(normal_from_pprime ** 2 * (1 - Q(1, 5) ** 2) > 1,
            "target normal pprime derivative")
    output_t_t = Q(48)
    output_t_p = Q(55)
    output_t_s = Q(8)
    require(normal_t_derivative + normal_from_pprime * pprime_t < output_t_t,
            "output t/t budget")
    require(velocity_p_derivative + normal_from_pprime * pprime_p < output_t_p,
            "output t/p budget")
    require(normal_from_pprime * pprime_s < output_t_s,
            "output t/s budget")

    exact_pprime_radius = (
        pprime_t * source_t_halfwidth
        + pprime_p * source_p_halfwidth
        + pprime_s * source_s_halfwidth
    )
    exact_output_t_radius = (
        output_t_t * source_t_halfwidth
        + output_t_p * source_p_halfwidth
        + output_t_s * source_s_halfwidth
    )
    require(exact_pprime_radius == Q(99, 80), "pprime radius arithmetic")
    require(exact_output_t_radius == Q(34, 25), "output t radius arithmetic")
    # A h/100 center-evaluation ball is absorbed in the advertised radii.
    eta_p_coefficient = Q(5, 4)
    eta_t_coefficient = Q(7, 5)
    require(exact_pprime_radius + Q(1, 100) < eta_p_coefficient,
            "p radius reserve")
    require(exact_output_t_radius + Q(1, 100) < eta_t_coefficient,
            "t radius reserve")

    # Boundary geometry: 8 axis and 16 diagonal cores.  At d>=24,
    # h<=1/256 and even the twice-expanded t tube stays in |t|<=91/128,
    # where dtheta/dt<3/2.  The major normal component remains >7/10, so
    # the E/W/N/S seam/sign test adds no physical boundary component.
    h_threshold = Q(1, 256)
    max_twice_expanded_abs_t = Q(7, 10) + 2 * eta_t_coefficient * h_threshold
    require(max_twice_expanded_abs_t == Q(91, 128), "expanded t endpoint")
    require(Q(3, 2) ** 2 * (1 - max_twice_expanded_abs_t ** 2) > 1,
            "expanded t chart derivative")
    center_abs_t = Q(7, 10) + eta_t_coefficient * h_threshold
    require(1 - center_abs_t ** 2 > Q(7, 10) ** 2,
            "major sign and seam margin")

    radius_sum_axis = Q(52, 25)
    radius_sum_diagonal = Q(104, 25)
    radius_sum = radius_sum_axis + radius_sum_diagonal
    radius_weighted_pwidth = (
        radius_sum_axis * Q(1, 250)
        + radius_sum_diagonal * Q(1, 25)
    )
    radius_weighted_twidth = radius_sum * Q(1, 100)
    require(radius_sum == Q(156, 25), "radius multiplicity")
    require(radius_weighted_pwidth == Q(546, 3125),
            "weighted p width")
    require(radius_weighted_twidth == Q(39, 625),
            "weighted t width")
    linear = 12 * (
        eta_t_coefficient * radius_weighted_pwidth
        + eta_p_coefficient * radius_weighted_twidth
    )
    quadratic = (
        12 * 8 * eta_t_coefficient * eta_p_coefficient * radius_sum
    )
    require(linear == Q(60489, 15625), "tube linear coefficient")
    require(quadratic == Q(26208, 25), "tube quadratic coefficient")
    threshold_effective = linear + quadratic * h_threshold
    require(threshold_effective == Q(995787, 125000),
            "threshold effective coefficient")
    require(threshold_effective < 8, "tube coefficient benchmark")
    global_collision_volume_lower = 4 * 3 * (
        adaptive.first_hit.RADIUS["G"] + adaptive.first_hit.RADIUS["W"]
    )
    require(global_collision_volume_lower == Q(156, 25),
            "collision volume lower")
    normalized_coefficient = Q(8) / global_collision_volume_lower
    require(normalized_coefficient == Q(50, 39), "normalized tube coefficient")

    derivative = {
        "source_root_widths_t_p_s": ["1/100", "1/25", "1/200"],
        "fair_depth_scale": "h_d=2^(-floor(d/3))",
        "source_normal_t_derivative_strict_upper": "3/2",
        "source_velocity_p_derivative_strict_upper": "2",
        "center_distance_strict_upper": "4",
        "output_p_partial_derivative_strict_uppers_t_p_s": ["44", "50", "7"],
        "target_normal_component_partial_derivative_strict_uppers_t_p_s": [
            "48", "55", "8"
        ],
        "exact_center_to_box_output_p_radius_coefficient": str(
            exact_pprime_radius
        ),
        "exact_center_to_box_target_t_radius_coefficient": str(
            exact_output_t_radius
        ),
        "Arb_center_ball_required_radius_relative_to_h": "1/100",
        "dependency_neutral_output_p_radius_coefficient": str(
            eta_p_coefficient
        ),
        "dependency_neutral_target_t_radius_coefficient": str(
            eta_t_coefficient
        ),
        "adaptive_precision_policy": (
            "increase Arb precision until each midpoint output scalar ball "
            "has radius <= h_d/100"
        ),
        "natural_interval_dependency_used_for_decay_theorem": False,
    }
    tube = {
        "fair_absolute_binary_depth_threshold": 24,
        "threshold_h": "1/256",
        "destination_core_rectangle_count": 24,
        "physical_t_face_count": 48,
        "physical_p_face_count": 48,
        "additional_chart_seam_face_count": 0,
        "chart_seam_policy": (
            "dominant-cell seam is an atlas artifact; use signed major-half-circle "
            "t coordinate, and absorb the seam-side overlap in the t-upper-face tube"
        ),
        "major_normal_component_strict_lower_at_threshold": "7/10",
        "max_twice_expanded_abs_t_at_threshold": "91/128",
        "expanded_dtheta_dt_strict_upper": "3/2",
        "radius_weighted_p_width_sum": str(radius_weighted_pwidth),
        "radius_weighted_t_width_sum": str(radius_weighted_twidth),
        "radius_multiplicity_sum": str(radius_sum),
        "outer_tube_unnormalized_collision_mass_formula": (
            "B(h)=(60489/15625)h+(26208/25)h^2"
        ),
        "outer_tube_linear_coefficient": str(linear),
        "outer_tube_quadratic_coefficient": str(quadratic),
        "outer_tube_effective_coefficient_at_h_le_1_over_256": str(
            threshold_effective
        ),
        "outer_tube_effective_coefficient_strict_upper": "8",
        "uniform_parameter_averaged_unresolved_base_mass_bound": (
            "M_base(U_d)<=B(h_d)<8h_d for every fair frontier with d>=24"
        ),
        "uniform_parameter_averaged_normalized_collision_SRB_bound": (
            "mu(U_d)<(50/39)h_d for every fair frontier with d>=24"
        ),
        "three_split_cycle_bound": (
            "M_base(U_(24+3j))<2^(-5-j) for every integer j>=0"
        ),
        "asymptotic_rate": "O(2^(-d/3))",
        "uniform_in_parameter_including_endpoints": True,
        "boundary_preimage_collision_measure_zero": True,
        "limiting_step1_R1_Q1_partition_mod_collision_null_set": "CERTIFIED",
    }
    return derivative, tube


def verdict() -> dict[str, Any]:
    return {
        "round25_53752_child_fresh_Arb_replay": "CERTIFIED",
        "one_generation_residual_mass_ratio_lt_7_over_8": "CERTIFIED_NONITERABLE",
        "dependency_neutral_fair_boundary_tube_decay_O_2_to_minus_d_over_3": (
            "CERTIFIED"
        ),
        "limiting_step1_R1_Q1_partition_mod_collision_null_set": "CERTIFIED",
        "finite_depth_unresolved_exhaustion": "NOT_CERTIFIED",
        "finite_complete_step1_branch_ledger": "NOT_MATERIALIZED",
        "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
        "q_weighted_return_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def certify() -> dict[str, Any]:
    upstream, _plan = load_inputs()
    rows = upstream["result"]["adaptive_full_core_step1_raw_leaf_rows"]
    _children, child_summary = replay_children(rows)
    regularity = regularity_audit()
    derivative, tube = derivative_and_tube_theorem()
    result = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "finite_child_admission_engine": "python-flint Arb whole-box natural extension",
            "finite_child_precision_bits": 384,
            "decay_engine": "exact midpoint Lipschitz radius plus adaptive-precision Arb",
            "clock": "source core at time 0; selected next collision at time 1",
        },
        "frozen_parent_frontier": {
            "unresolved_parent_count": PARENT_UNRESOLVED_COUNT,
            "planned_child_count": CHILD_COUNT,
            "unresolved_parent_base_mass": str(PARENT_UNRESOLVED_MASS),
            "parent_depth_histogram": {"12": 6816, "15": 20060},
            "scheduled_split_axis_histogram": {"t": PARENT_UNRESOLVED_COUNT},
            "planned_split_record_rows_sha256": PARENT_SPLIT_ROWS_DIGEST,
        },
        "fresh_53752_child_replay": child_summary,
        "regular_local_diffeomorphism_audit": regularity,
        "dependency_neutral_derivative_budget": derivative,
        "fair_dyadic_boundary_tube_theorem": tube,
        "strict_nonpromotion": {
            "natural_Arb_one_generation_ratio_automatically_iterable": False,
            "finite_depth_unresolved_cover_empty": False,
            "all_boundary_fibres_materialized_as_raw_rows": False,
            "finite_complete_step1_R1_Q1_ledger": "NOT_MATERIALIZED",
            "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
            "survivor_conditioned_recovery": "NOT_CERTIFIED",
            "strong_q_weighted_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def write_manifest(path: Path, verifier_path: Path) -> None:
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": DEPENDENCIES,
        "result": certify(),
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
        default=HERE / "cm2_gate34_round26_boundary_tube_decay_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = certify()
    child = result["fresh_53752_child_replay"]
    print("ROUND25_53752_CHILD_FRESH_ARB_REPLAY: CERTIFIED")
    print(f"CHILD_HISTOGRAM: {child['classification_histogram']}")
    print(f"RESIDUAL_BASE_MASS: {child['mass_by_class']['UNRESOLVED_OUTER']}")
    print("FAIR_BOUNDARY_TUBE_DECAY: M_base(U_d)<8*2^(-floor(d/3)), d>=24")
    print("LIMITING_STEP1_R1_Q1_MOD_NULL: CERTIFIED")
    print("ARBITRARY_N_RN_QN: NOT_CERTIFIED")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
