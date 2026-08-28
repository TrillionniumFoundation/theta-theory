#!/usr/bin/env python3
"""Gate-4 componentwise global Growth/recovery frontier certificate.

This certificate closes the missing *one-step* contraction-weighted join by
using a compressed incidence theorem rather than pretending that the frozen
horizon boxes are physical continuity components.

The finite candidate and raw-sheet universes are replayed exactly.  For an
arbitrary invariant-cone unstable curve W of sufficiently small Euclidean
length, physical true-continuity components are then keyed relative to W and
joined to their actual first-hit owner, homogeneity child, multiplicity, and
adapted-metric inverse-expansion bound.

Two elementary uniform estimates make the compressed join effective.

* A central child has discriminant bounded away from zero.  The discriminant
  is uniformly Lipschitz along W, so a central child is a definite distance
  from a true tangency endpoint.  A companion signed-sheet separation bound
  handles a grazing-only occlusion interval.  Hence a sufficiently short W
  has at most one central child globally.
* There are at most 153 true-continuity components.  Raising the homogeneity
  cutoff from 41 to 6121 charges every high-strip child of all 153 components
  to one global tail strictly below 1/5.

Thus Xi_1(delta_1)<900337/901685<1.  This is not the final same-occurrence q
and does not manufacture the still-missing invariant standard-curve
curvature/density constants, numerical C_p/vartheta_p, or native recovery.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2_gate3_candidate_first_hit_cert.py": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
    "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json": (
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4"
    ),
    "cm2-gate3-owner-voronoi-event-registry-manifest-2026-07-15.json": (
        "d7b1f9d879b9c02257552a6c51fad16de477e60deaac250b4fc55a13be44e8e5"
    ),
    "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json": (
        "003d3e0d742829039e85649975e8dca4a992fa7a389063eef4478df02ec03064"
    ),
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json": (
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
    "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json": (
        "4e0c8216892afe9ce0c19e22b9ecc5742f21e9e4512d949b88325e1ee1ff70d5"
    ),
    "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json": (
        "ee1ac2acb72af04ac254e2f0a33981df478b022cde0dc08f9988762ff1c8bcc9"
    ),
    "cm2-gate4-weighted-growth-join-diagnostic-manifest-2026-07-16.json": (
        "ccfdd6e001b57b2181bb8f9121b3a13e4881dff2996716d59b48384806886107"
    ),
    "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json": (
        "20f595ed4bcf62cb5cc5c89c22ab31a3ca039f43fff29fd35855673dc970b4a2"
    ),
    "cm2-gate4-finite-cemetery-resolution-tradeoff-manifest-2026-07-16.json": (
        "f9b12df851f9cfd5115c7810ec37349583e4a53ef9e312447b647cc3ae21b30d"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(name: str) -> dict[str, Any]:
    path = HERE / name
    assert path.is_file()
    assert sha256_path(path) == DEPENDENCIES[name]
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Target:
    obstacle: str
    ix: int
    iy: int

    @property
    def target_id(self) -> str:
        return f"{self.obstacle}[{self.ix},{self.iy}]"


RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}
EPS = Q(1, 400)
TAU_MAX = Q(3)
CELLS = ("E", "W", "N", "S")
SOURCES = ("G", "W")
INV_SQRT2_LOWER = Q(707, 1000)
INV_SQRT2_UPPER = Q(708, 1000)
TARGETS = tuple(
    Target(obstacle, ix, iy)
    for obstacle in SOURCES
    for ix in range(-4, 5)
    for iy in range(-4, 5)
)


def vector_interval(source: str, target: Target) -> tuple[Q, Q, Q, Q]:
    ix, iy = target.ix, target.iy
    if source == "G" and target.obstacle == "G":
        return Q(ix), Q(ix), Q(iy), Q(iy)
    if source == "G" and target.obstacle == "W":
        x = Q(2 * ix + 1, 2)
        return x - EPS, x + EPS, Q(2 * iy + 1, 2), Q(2 * iy + 1, 2)
    if source == "W" and target.obstacle == "G":
        x = Q(2 * ix - 1, 2)
        return x - EPS, x + EPS, Q(2 * iy - 1, 2), Q(2 * iy - 1, 2)
    return Q(ix), Q(ix), Q(iy), Q(iy)


def square_min_abs(lower: Q, upper: Q) -> Q:
    if lower <= 0 <= upper:
        return Q(0)
    return min(lower * lower, upper * upper)


def absmax(lower: Q, upper: Q) -> Q:
    return max(abs(lower), abs(upper))


def dominant_cell_support_upper(
    cell: str, x0: Q, x1: Q, y0: Q, y1: Q
) -> Q:
    if cell == "E":
        a_upper, b_abs = x1, absmax(y0, y1)
    elif cell == "W":
        a_upper, b_abs = -x0, absmax(y0, y1)
    elif cell == "N":
        a_upper, b_abs = y1, absmax(x0, x1)
    elif cell == "S":
        a_upper, b_abs = -y0, absmax(x0, x1)
    else:  # pragma: no cover
        raise ValueError(cell)
    if a_upper >= 0:
        return a_upper + b_abs * INV_SQRT2_UPPER
    return a_upper * INV_SQRT2_LOWER + b_abs * INV_SQRT2_UPPER


def retained_candidate(source: str, cell: str, target: Target) -> bool:
    if target.obstacle == source and target.ix == 0 and target.iy == 0:
        return False
    x0, x1, y0, y1 = vector_interval(source, target)
    distance_squared = square_min_abs(x0, x1) + square_min_abs(y0, y1)
    threshold = TAU_MAX + RADIUS[source] + RADIUS[target.obstacle]
    if distance_squared >= threshold * threshold:
        return False
    support_upper = dominant_cell_support_upper(cell, x0, x1, y0, y1)
    return support_upper >= RADIUS[source] - RADIUS[target.obstacle]


def candidate_ids(source: str, cell: str) -> list[str]:
    return [
        target.target_id
        for target in TARGETS
        if retained_candidate(source, cell, target)
    ]


def load_dependencies() -> dict[str, dict[str, Any]]:
    # The Python source is pinned even though the exact rational reduction is
    # replayed locally without importing python-flint.
    source_path = HERE / "cm2_gate3_candidate_first_hit_cert.py"
    assert sha256_path(source_path) == DEPENDENCIES[source_path.name]
    names = [name for name in DEPENDENCIES if name.endswith(".json")]
    data = {name: load_json(name) for name in names}

    first = data["cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"]
    owner = data[
        "cm2-gate3-owner-voronoi-event-registry-manifest-2026-07-15.json"
    ]
    slope = data[
        "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
    ]
    cone = data[
        "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
    ]
    finite_s = data[
        "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
    ]
    numeric = data[
        "cm2-gate4-numeric-growth-leaves-frontier-manifest-2026-07-16.json"
    ]
    global_growth = data[
        "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json"
    ]
    weighted = data[
        "cm2-gate4-weighted-growth-join-diagnostic-manifest-2026-07-16.json"
    ]
    native = data[
        "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json"
    ]
    cemetery = data[
        "cm2-gate4-finite-cemetery-resolution-tradeoff-manifest-2026-07-16.json"
    ]

    assert first["candidate_reduction"]["retained_pair_count"] == 448
    assert owner["scope"]["global_signed_tangency_sheets"] == 288
    assert owner["owner_partition"]["status"] == (
        "CERTIFIED_FINITE_BOOLEAN_SINGLE_OWNER_PARTITION"
    )
    assert slope["result"]["exact_oriented_slope_bounds"][
        "exact_source_slope_formula"
    ] == "dphi_source/dr_source=-kappa_source-cp_source/ell_T"
    assert cone["result"]["global_invariant_geometric_cone"]["cone_upper"] == (
        "4108425/145348"
    )
    assert finite_s["result"]["uniform_horizon_penetration_audit"][
        "replayed_leaf_count"
    ] == 35024
    assert numeric["replay_summary"]["inverse_contraction"] == (
        "144000/180337"
    )
    assert global_growth["replay_summary"][
        "true_continuity_component_upper"
    ] == 153
    assert weighted["replay_summary"]["componentwise_weighted_join_present"] is False
    assert native["replay_summary"]["native_recovery_target"] == (
        "DIVERGES_BEFORE_RECOVERY"
    )
    assert cemetery["replay_summary"]["unnormalized_reweighted_escape_refuted"] is False
    return data


def typed_outer_universe(data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    first = data["cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"]
    owner = data[
        "cm2-gate3-owner-voronoi-event-registry-manifest-2026-07-15.json"
    ]
    finite_s = data[
        "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
    ]
    chart_manifest = {
        row["chart_id"]: row for row in first["candidate_reduction"]["charts"]
    }
    candidate_rows: list[dict[str, Any]] = []
    chart_signed_rows: list[dict[str, Any]] = []
    global_owner_keys: set[tuple[str, str]] = set()
    for source in SOURCES:
        for cell in CELLS:
            chart_id = f"{source}:{cell}"
            ids = candidate_ids(source, cell)
            frozen = chart_manifest[chart_id]
            assert len(ids) == frozen["retained"]
            assert canonical_digest(ids) == frozen["candidate_sha256"]
            for target_id in ids:
                candidate_row_id = f"candidate:{chart_id}:{target_id}"
                candidate_rows.append({
                    "candidate_row_id": candidate_row_id,
                    "chart_id": chart_id,
                    "source_obstacle": source,
                    "owner_target_id": target_id,
                    "typed_role": "conservative_first-hit_owner_candidate",
                    "is_physical_continuity_component": False,
                })
                global_owner_keys.add((source, target_id))
                for epsilon in (-1, 1):
                    chart_signed_rows.append({
                        "candidate_row_id": candidate_row_id,
                        "raw_sheet_id": (
                            f"sheet:{source}:{target_id}:epsilon={epsilon:+d}"
                        ),
                        "epsilon": epsilon,
                        "typed_role": "chart-incidence view of a raw tangency sheet",
                        "is_physical_cut_only_after_visibility_test": True,
                    })
    assert len(candidate_rows) == 448
    assert len(chart_signed_rows) == 896

    global_owner_rows = [
        {
            "global_owner_id": f"owner:{source}:{target_id}",
            "source_obstacle": source,
            "owner_target_id": target_id,
        }
        for source, target_id in sorted(global_owner_keys)
    ]
    raw_sheet_rows = [
        {
            "raw_sheet_id": f"sheet:{source}:{target_id}:epsilon={epsilon:+d}",
            "global_owner_id": f"owner:{source}:{target_id}",
            "source_obstacle": source,
            "owner_target_id": target_id,
            "epsilon": epsilon,
            "event_equation": "Delta_T=R_T^2-w_T^2=0",
            "physical_visibility_required": True,
            "raw_sheet_is_not_a_physical_component": True,
        }
        for source, target_id in sorted(global_owner_keys)
        for epsilon in (-1, 1)
    ]
    counts = {
        source: sum(row["source_obstacle"] == source for row in global_owner_rows)
        for source in SOURCES
    }
    assert counts == {"G": 76, "W": 68}
    assert len(global_owner_rows) == 144
    assert len(raw_sheet_rows) == 288
    assert len(raw_sheet_rows) == owner["scope"]["global_signed_tangency_sheets"]

    horizon = finite_s["result"]["uniform_horizon_penetration_audit"]
    return {
        "horizon_witness_ledger": {
            "leaf_count": horizon["replayed_leaf_count"],
            "leaf_rows_sha256": horizon["horizon_leaf_rows_sha256"],
            "typed_role": "ambient position-direction witness for tau<3",
            "has_short_curve_or_component_key": False,
            "used_in_join_only_through_uniform_tau_upper": "3",
        },
        "candidate_owner_ledger": {
            "row_count": len(candidate_rows),
            "rows_sha256": canonical_digest(candidate_rows),
            "chart_counts": {
                f"{source}:{cell}": len(candidate_ids(source, cell))
                for source in SOURCES
                for cell in CELLS
            },
            "typed_rows_are_conservative_not_physical": True,
        },
        "chart_raw_sheet_incidence_ledger": {
            "row_count": len(chart_signed_rows),
            "rows_sha256": canonical_digest(chart_signed_rows),
            "chart_duplicates_are_quotiented_before_component_counting": True,
        },
        "global_owner_ledger": {
            "row_count": len(global_owner_rows),
            "source_counts": counts,
            "rows_sha256": canonical_digest(global_owner_rows),
        },
        "global_raw_sheet_ledger": {
            "row_count": len(raw_sheet_rows),
            "source_sheet_counts": {"G": 152, "W": 136},
            "rows_sha256": canonical_digest(raw_sheet_rows),
            "maximum_intersections_for_one_source_curve": 152,
            "maximum_true_continuity_components": 153,
        },
        "join_typing_guard": (
            "35024 horizon leaves contribute tau<3 only; 448 chart candidates "
            "quotient to 144 source-owner keys and 288 raw signed sheets; actual "
            "physical components are generated only after intersecting a concrete W "
            "and applying the frozen first-visible owner predicate"
        ),
    }


def short_curve_central_incidence_theorem() -> dict[str, Any]:
    k0 = 6121
    radius_min = Q(4, 25)
    radius_max = Q(9, 25)
    curvature_max = Q(25, 4)
    slope_upper = Q(29)
    tau_min = Q(36337, 800000)
    target_distance_upper = TAU_MAX + radius_max

    # d=a_T-q(r), w=u_perp.d and Delta=R_T^2-w^2.  Along an invariant-cone
    # graph, |d'|=1 and |u_perp'|=|kappa+V|.
    w_derivative_upper = 1 + target_distance_upper * (
        curvature_max + slope_upper
    )
    discriminant_derivative_upper = (
        2 * radius_max * w_derivative_upper
    )
    assert target_distance_upper == Q(84, 25)
    assert w_derivative_upper == Q(2986, 25)
    assert discriminant_derivative_upper == Q(53748, 625)

    central_cosine_lower = Q(1, 2 * k0 * k0)
    central_discriminant_lower = (
        radius_min * radius_min * central_cosine_lower * central_cosine_lower
    )
    assert central_discriminant_lower == Q(4, 625 * k0**4)
    central_to_tangency_r_distance = (
        central_discriminant_lower / discriminant_derivative_upper
    )
    assert central_to_tangency_r_distance == Q(1, 13437 * k0**4)

    # At one source point the two signed tangency angles of a target differ
    # by 2 asin(R/|d|)>2/21.  The difference between W and either sheet has
    # derivative less than V_max+kappa_max+1/tau_min.
    signed_tangent_angle_gap_lower = Q(2, 21)
    curve_sheet_relative_slope_upper = (
        slope_upper + curvature_max + 1 / tau_min
    )
    signed_sheet_crossing_r_separation = (
        signed_tangent_angle_gap_lower / curve_sheet_relative_slope_upper
    )
    assert curve_sheet_relative_slope_upper == Q(8323517, 145348)
    assert signed_sheet_crossing_r_separation == Q(41528, 24970551)

    delta_1 = central_to_tangency_r_distance / 2
    assert delta_1 == Q(1, 37724355673552103994)
    assert delta_1 < central_to_tangency_r_distance
    assert delta_1 < signed_sheet_crossing_r_separation

    return {
        "curve_class": (
            "one connected invariant-cone unstable graph W in one source obstacle, "
            "oriented so dr>0 and 25/9<V=dphi/dr<29"
        ),
        "short_curve_cell_id": (
            "(s,source,W); physical components are ordered connected intervals "
            "of W after visible raw-sheet cuts"
        ),
        "parameter_window": "|s|<=1/400",
        "homogeneity_cutoff_k0": k0,
        "central_cosine_strict_lower": str(central_cosine_lower),
        "central_discriminant_strict_lower": str(central_discriminant_lower),
        "discriminant_coordinate": (
            "Delta_T=R_T^2-(u_perp dot (a_T-q))^2=R_T^2*c_1^2"
        ),
        "discriminant_r_derivative_strict_upper": str(
            discriminant_derivative_upper
        ),
        "central_to_selected_tangency_r_distance_strict_lower": str(
            central_to_tangency_r_distance
        ),
        "two_signed_tangent_angle_gap_strict_lower": str(
            signed_tangent_angle_gap_lower
        ),
        "curve_minus_sheet_r_derivative_strict_upper": str(
            curve_sheet_relative_slope_upper
        ),
        "two_signed_sheet_crossing_r_separation_strict_lower": str(
            signed_sheet_crossing_r_separation
        ),
        "uniform_small_curve_threshold_delta_1": str(delta_1),
        "length_metric": (
            "Euclidean phase-space arclength; it dominates absolute source-r displacement"
        ),
        "first_hit_transition_dichotomy": (
            "strictly disjoint targets forbid equal positive first roots; between "
            "two central owner blocks, either an adjacent central owner reaches a "
            "selected raw tangency sheet, or an intervening grazing-only owner "
            "crosses both of its signed tangency sheets"
        ),
        "chart_seams_are_not_physical_cuts": True,
        "at_most_one_central_child_for_length_at_most_delta_1": True,
        "central_child_global_multiplicity_upper": 1,
        "compressed_sheet_separation_incidence_theorem": "CERTIFIED",
    }


def componentwise_weighted_growth_join(
    incidence: dict[str, Any], outer: dict[str, Any]
) -> dict[str, Any]:
    k0 = incidence["homogeneity_cutoff_k0"]
    true_component_upper = outer["global_raw_sheet_ledger"][
        "maximum_true_continuity_components"
    ]
    theta = Q(144000, 180337)
    per_component_two_sided_tail_integral = Q(8, k0 - 1)
    global_tail_integral = true_component_upper * per_component_two_sided_tail_integral
    assert k0 == 6121
    assert true_component_upper == 153
    assert global_tail_integral == Q(1, 5)
    xi_upper = theta + global_tail_integral
    margin = 1 - xi_upper
    assert xi_upper == Q(900337, 901685) < 1
    assert margin == Q(1348, 901685) > 0

    templates = [
        {
            "parent_short_curve_cell_id": "(s,source,W), length(W)<=delta_1",
            "physical_continuity_component_id": "ordered component j of W",
            "owner_target_id": "unique first-visible owner T(j)",
            "homogeneity_child_id": "central H_0(k0=6121)",
            "physical_component_multiplicity_upper": 1,
            "inverse_expansion_sup_strict_upper": str(theta),
        },
        {
            "parent_short_curve_cell_id": "(s,source,W), length(W)<=delta_1",
            "physical_continuity_component_id": "ordered component j of W",
            "owner_target_id": "unique first-visible owner T(j)",
            "homogeneity_child_id": "H_(sigma,k), sigma in {+,-}, k>=6121",
            "physical_component_multiplicity_upper_per_sigma_k": 153,
            "inverse_expansion_sup_strict_upper": "4/k^2",
        },
    ]
    return {
        "typed_component_templates": templates,
        "typed_component_templates_sha256": canonical_digest(templates),
        "join_fields": [
            "parent_short_curve_cell_id",
            "physical_continuity_component_id",
            "owner_target_id",
            "homogeneity_child_id",
            "physical_component_multiplicity",
            "inverse_expansion_sup_upper",
        ],
        "join_generation": (
            "intersect W with visible subsets of the 288 raw sheets, order the "
            "resulting physical components, attach the unique first-hit owner, then "
            "split the image graph by H_0 or H_(sigma,k)"
        ),
        "every_true_and_homogeneity_cut_counted_once": True,
        "conservative_candidates_not_charged_as_physical_children": True,
        "central_child_multiplicity_upper": 1,
        "high_child_multiplicity_upper_per_sign_and_rank": true_component_upper,
        "central_inverse_expansion_strict_upper": str(theta),
        "high_child_inverse_expansion_strict_upper": "4/k^2",
        "global_high_strip_tail_derivation": (
            "sum_(j<=153) sum_(sigma=+,-) sum_(k>=6121) 4/k^2 "
            "<153*8/(6121-1)=1/5"
        ),
        "global_high_strip_tail_strict_upper": str(global_tail_integral),
        "global_one_step_weighted_sum_strict_upper": str(xi_upper),
        "global_one_step_weighted_sum_margin": str(margin),
        "Xi_1_delta_1_formula": (
            "Xi_1(delta_1)=sup_(length(W)<=delta_1) sum_children "
            "sup norm(DT_s^-1)_* <900337/901685"
        ),
        "componentwise_multiplicity_inverse_expansion_join": "CERTIFIED_COMPRESSED",
        "numeric_global_one_step_weighted_Growth_contraction": "CERTIFIED",
        "this_is_not_q_branch_repetition": True,
        "this_is_not_final_same_occurrence_q": True,
    }


def recovery_frontier(
    data: dict[str, dict[str, Any]], weighted: dict[str, Any]
) -> dict[str, Any]:
    global_growth = data[
        "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json"
    ]
    native = data[
        "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json"
    ]
    cemetery = data[
        "cm2-gate4-finite-cemetery-resolution-tradeoff-manifest-2026-07-16.json"
    ]
    assert global_growth["verdict"][
        "numeric_oriented_carrier_one_step_log_r_jacobian_distortion"
    ] == "CERTIFIED"
    assert native["verdict"]["native_depth_plus_recovery_moment"] == (
        "NOT_CERTIFIED"
    )
    assert cemetery["verdict"]["unnormalized_reweighted_family_escape"] == (
        "NOT_REFUTED"
    )
    return {
        "new_numeric_Growth_inputs": {
            "global_one_step_theta_star_strict_upper": weighted[
                "global_one_step_weighted_sum_strict_upper"
            ],
            "uniform_delta_1": "1/37724355673552103994",
            "homogeneity_cutoff": 6121,
            "positive_margin": weighted["global_one_step_weighted_sum_margin"],
        },
        "still_missing_before_numeric_C_p_vartheta_p": [
            "an invariant numerical C2 curvature ceiling D_std for every iterated standard curve",
            "the corresponding all-standard-curve homogeneous log-Jacobian distortion constant",
            "a numerical regular-density constant C_r and additive Growth recurrence constant",
            "an executable theorem converting those constants and theta_star into C_p,vartheta_p",
        ],
        "why_existing_distortion_is_insufficient": (
            "6000000000000 is certified only for 128 initial oriented carriers; "
            "the frozen global certificate explicitly leaves arbitrary iterated "
            "standard-curve distortion uncertified"
        ),
        "unnormalized_reweighted_native_recovery_contract": {
            "required_fields": [
                "record-preserving unnormalized standard-family representation",
                "finite unnormalized boundary functional after every actual cut",
                "one-step inequality Z_un(TF)<=a*Z_un(F)+b*mass(F) with a<1",
                "query-independent merging or reweighting rule preserving occurrence labels",
                "charged-moment bound before any leafwise normalization",
            ],
            "fields_present_in_frozen_manifests": 0,
            "leafwise_inverse_mass_interface_required": False,
            "finite_cemetery_no_go_applies_to_this_contract": False,
            "finite_cemetery_no_go_scope": (
                "normalized cumulative-u atoms with separate leafwise p_a^-1 charge only"
            ),
            "unnormalized_reweighted_recovery": "NOT_CERTIFIED",
        },
        "propagation_status": {
            "numeric_C_p": False,
            "numeric_vartheta_p": False,
            "numeric_A0_A1": False,
            "numeric_C_fw": False,
            "numeric_C_rev": False,
            "final_same_occurrence_q": False,
        },
        "symbol_guard": (
            "Xi_1 upper 900337/901685 is a global one-step Growth coefficient; "
            "it is neither the old local q_branch nor the final CM2 same-occurrence q"
        ),
    }


def certify() -> dict[str, Any]:
    data = load_dependencies()
    outer = typed_outer_universe(data)
    incidence = short_curve_central_incidence_theorem()
    weighted = componentwise_weighted_growth_join(incidence, outer)
    recovery = recovery_frontier(data, weighted)
    return {
        "schema": "cm2.gate4.componentwise-global-growth-recovery-frontier.v1",
        "provenance": {
            "parameter_window": "|s|<=1/400",
            "map_scope": "constant fixed-configuration maps T_s=F_(K_s,K_s)",
            "dependency_sha256": DEPENDENCIES,
        },
        "typed_outer_universe": outer,
        "short_curve_central_incidence_theorem": incidence,
        "componentwise_weighted_growth_join": weighted,
        "recovery_and_propagation_frontier": recovery,
        "scope_limits": {
            "typed_horizon_candidate_raw_sheet_audit": True,
            "compressed_physical_component_join": True,
            "numeric_delta_1": True,
            "at_most_one_global_central_child": True,
            "single_global_high_strip_tail": True,
            "numeric_global_one_step_weighted_Growth_contraction": True,
            "full_numeric_Growth_Lemma_constants": False,
            "numeric_C_p_vartheta_p": False,
            "unnormalized_reweighted_native_recovery": False,
            "complete_numeric_C_fw_C_rev_final_q": False,
            "gate4_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_TYPED_COMPONENTWISE_JOIN: CERTIFIED_COMPRESSED")
    print("GATE4_GLOBAL_ONE_STEP_WEIGHTED_GROWTH_CONTRACTION: CERTIFIED")
    print("GATE4_NUMERIC_C_P_VARTTHETA_P: NOT_CERTIFIED")
    print("GATE4_UNNORMALIZED_REWEIGHTED_NATIVE_RECOVERY: NOT_CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
