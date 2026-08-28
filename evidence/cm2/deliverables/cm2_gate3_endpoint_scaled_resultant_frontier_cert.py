#!/usr/bin/env python3
"""Endpoint-scaled and critical-resultant Gate-3 frontier certificate.

This is a strict extension of the frozen thirteenth-pass physical-first
frontier.  It does not edit or reinterpret that artifact.  The first part
replays the source-grazing terminal collars in a cancellation-free angular
coordinate.  The second part freezes the exact algebraic reduction of a
candidate critical root to the two-variable system ``(Delta, Delta_t)``.

The numerical resultant/nonvanishing audit is deliberately kept separate:
the algebraic identity alone does not certify that the remaining critical
boxes contain no junction.  All unsupported Gate-3 conclusions therefore
remain fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_finite_s_future_singularity_outer_atlas_cert as outer
import cm2_gate3_physical_first_unresolved_frontier_cert as frozen


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent
FROZEN_MANIFEST = (
    HERE / "cm2-gate3-physical-first-unresolved-frontier-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_grazing_endpoint_scaled_cp(
    row: dict[str, Any], side: str, s0: Q, s1: Q,
    terminal_t_width: Q,
) -> dict[str, Any]:
    """Cancellation-free ``c_p`` on a source-grazing terminal strip.

    Put ``C=target-source`` and decompose it in the endpoint frame as
    ``C=a0*n0+B0*j0``.  The source-grazing construction gives the *exact*
    identity ``a0=R_source+sigma*R_target``.  At angular distance ``x`` from
    that endpoint,

      A-sigma R_t = (cos(x)-1)a0 + q sin(x) B0,

    where ``A=C*n-R_source`` and ``q`` is the inward rotation sign.  The
    usual formula for ``c_p`` loses this small factor by subtraction.  We
    instead use

      c_p = (A^2-R_t^2)/(ell*A-epsilon*R_t*B).

    The numerator is evaluated as the two factors
    ``(A-sigma R_t)(A+sigma R_t)``.  This is pointwise identical wherever
    the displayed denominator is nonzero.
    """

    assert side in {"left_boundary", "right_boundary"}
    boundary = row[side]
    assert boundary["kind"] == outer.finite.maximal.SOURCE_GRAZING
    s = outer.Jet2.s_variable(outer.arb_interval(s0, s1))
    n0x, n0y = outer.curve_normal(boundary, s)
    other_side = "right_boundary" if side == "left_boundary" else "left_boundary"
    n1x, n1y = outer.curve_normal(row[other_side], s)
    if side == "left_boundary":
        cross = n0x * n1y - n0y * n1x
        dot = n0x * n1x + n0y * n1y
        q = 1
    else:
        # Keep the oriented full-row width left-to-right, while the local
        # endpoint coordinate xi=1-t grows inward from the right endpoint.
        cross = n1x * n0y - n1y * n0x
        dot = n1x * n0x + n1y * n0y
        q = -1
    width = outer.atan2_jet(cross, dot)
    core_width = width - 2 * outer.ENDPOINT_TRIM
    assert bool(core_width.value > outer.arbq(Q(1, 40)))
    assert bool(width.value < outer.arbq(Q(9, 4)))
    # Multiplying two balls whose local coordinate starts at zero can lose a
    # tiny positive absolute trim through outward midpoint-radius rounding.
    # Monotonicity gives the sharp range directly: x is between the exact
    # trim and trim+sup(core_width)*terminal_t_width.
    x_lower = outer.arbq(outer.ENDPOINT_TRIM)
    x_upper = (
        x_lower
        + core_width.value.upper() * outer.arbq(terminal_t_width)
    )
    x = outer.Jet2.constant(arb(x_lower).union(arb(x_upper)))
    cosine, sine = x.cos(), x.sin()

    source_x, source_y = outer.source_center(row["source"], s)
    target_x, target_y = outer.target_center_id(row["target"], s)
    cx, cy = target_x - source_x, target_y - source_y
    b0 = -cx * n0y + cy * n0x
    source_radius = outer.Jet2.constant(
        outer.finite.bulk.ARB_RADIUS[row["source"]]
    )
    target_obstacle = outer.finite.bulk.TARGET_BY_ID[row["target"]].obstacle
    target_radius = outer.Jet2.constant(
        outer.finite.bulk.ARB_RADIUS[target_obstacle]
    )
    epsilon = int(row["epsilon"])
    direction = int(boundary["tangent_direction"])
    sigma = -direction * epsilon
    a0 = source_radius + sigma * target_radius

    # n=cos(x)n0+q sin(x)j0.  The exact endpoint identity replaces C*n0 by
    # a0, so no interval subtraction of two nearly equal quantities occurs.
    a_minus = (cosine - 1) * a0 + q * sine * b0
    a = sigma * target_radius + a_minus
    a_plus = a_minus + 2 * sigma * target_radius
    numerator = a_minus * a_plus
    b = cosine * b0 - q * sine * a0
    distance_squared = a * a + b * b
    ell = (distance_squared - target_radius * target_radius).sqrt()
    denominator = ell * a - epsilon * target_radius * b
    if denominator.value.contains(0):
        raise AssertionError("rationalized source-cp denominator crosses zero")
    cp = numerator / denominator
    # Use separately rounded factor signs.  Multiplying two very asymmetric
    # Arb balls can add a harmless outward radius larger than the tiny lower
    # endpoint factor; the individual strict signs are the sharper proof.
    if not bool(a_minus.value > 0):
        raise AssertionError("endpoint-scaled grazing factor is not positive")
    if sigma == -1 and not bool(a_plus.value < 0):
        raise AssertionError("opposite endpoint factor is not negative")
    if sigma == 1 and not bool(a_plus.value > 0):
        raise AssertionError("opposite endpoint factor is not positive")
    numerator_sign = -1 if sigma == -1 else 1
    denominator_sign = -1 if bool(denominator.value < 0) else 1
    if denominator_sign != numerator_sign:
        raise AssertionError("rationalized source-cp sign is not positive")

    # Direct pointwise identity at the midpoint is a guard against a sign or
    # frame convention error in the rationalization.
    sm = (s0 + s1) / 2
    if side == "left_boundary":
        tm = terminal_t_width / 2
    else:
        tm = 1 - terminal_t_width / 2
    direct_s = outer.Jet2.s_variable(outer.arbq(sm))
    direct_t = outer.Jet2.t_variable(outer.arbq(tm))
    nx, ny = frozen.nearest_endpoint_trimmed_row_normal(row, direct_t, direct_s)
    direct_cp = outer.moving_tangent_geometry(row, nx, ny, direct_s)[-1].value
    rational_midpoint = source_grazing_endpoint_scaled_cp_point(
        row, side, tm, sm
    )
    difference = direct_cp - rational_midpoint
    if not difference.contains(0):
        raise AssertionError("rationalized and direct source-cp formulas differ")

    return {
        "side": side,
        "sigma": sigma,
        "inward_rotation_sign": q,
        "parameter_interval": [str(s0), str(s1)],
        "terminal_t_width": str(terminal_t_width),
        "core_angular_width_enclosure": str(core_width.value),
        "source_cp_raw_ball_enclosure_not_used_for_sign": str(cp.value),
        "grazing_factor_enclosure": str(a_minus.value),
        "opposite_factor_enclosure": str(a_plus.value),
        "source_cp_strict_sign_from_separate_factors": 1,
        "rationalized_denominator_enclosure": str(denominator.value),
        "direct_midpoint_identity_enclosure": str(difference),
    }


def source_grazing_endpoint_scaled_cp_point(
    row: dict[str, Any], side: str, t: Q, s_value: Q,
) -> arb:
    """Point version of the factorized formula used only as an identity guard."""

    s = outer.Jet2.s_variable(outer.arbq(s_value))
    boundary = row[side]
    other_side = "right_boundary" if side == "left_boundary" else "left_boundary"
    n0x, n0y = outer.curve_normal(boundary, s)
    n1x, n1y = outer.curve_normal(row[other_side], s)
    if side == "left_boundary":
        cross = n0x * n1y - n0y * n1x
        dot = n0x * n1x + n0y * n1y
        q = 1
        xi = t
    else:
        cross = n1x * n0y - n1y * n0x
        dot = n1x * n0x + n1y * n0y
        q = -1
        xi = 1 - t
    width = outer.atan2_jet(cross, dot)
    x = outer.ENDPOINT_TRIM + (width - 2 * outer.ENDPOINT_TRIM) * xi
    cosine, sine = x.cos(), x.sin()
    sx, sy = outer.source_center(row["source"], s)
    tx, ty = outer.target_center_id(row["target"], s)
    cx, cy = tx - sx, ty - sy
    b0 = -cx * n0y + cy * n0x
    rs = outer.Jet2.constant(outer.finite.bulk.ARB_RADIUS[row["source"]])
    target_obstacle = outer.finite.bulk.TARGET_BY_ID[row["target"]].obstacle
    rt = outer.Jet2.constant(outer.finite.bulk.ARB_RADIUS[target_obstacle])
    epsilon = int(row["epsilon"])
    sigma = -int(boundary["tangent_direction"]) * epsilon
    a0 = rs + sigma * rt
    a_minus = (cosine - 1) * a0 + q * sine * b0
    a = sigma * rt + a_minus
    b = cosine * b0 - q * sine * a0
    ell = (a * a + b * b - rt * rt).sqrt()
    return ((a_minus * (a_minus + 2 * sigma * rt)) /
            (ell * a - epsilon * rt * b)).value


def endpoint_scaled_source_incidence_audit(
    rows: list[dict[str, Any]], frozen_frontier: dict[str, Any],
) -> dict[str, Any]:
    """Certify the canonical source-grazing endpoint bands.

    The frozen terminal-record ledger is hashed, not exported coordinate by
    coordinate.  Matching its aggregate 24x64 count does not by itself prove
    record-to-band containment.  This routine therefore certifies only the
    explicit canonical bands and keeps that containment claim false.
    """

    terminal_t_width = Q(1, outer.INITIAL_T_CELLS * 2 ** frozen.SELECTIVE_MAX_T_DEPTH)
    assert terminal_t_width == Q(1, 1024)
    parameter_cells = outer.INITIAL_V_CELLS * 2 ** frozen.SELECTIVE_MAX_V_DEPTH
    assert parameter_cells == 64
    records: list[dict[str, Any]] = []
    source_rows = []
    ledger = frozen_frontier["ordered_row_summary_ledger"]
    for row_index, (row, old) in enumerate(zip(rows, ledger, strict=True)):
        count = int(old["terminal_reason_counts"].get("source_cp_not_strict", 0))
        if not count:
            continue
        sides = [
            side for side in ("left_boundary", "right_boundary")
            if row[side]["kind"] == outer.finite.maximal.SOURCE_GRAZING
        ]
        assert len(sides) == 1
        assert count == parameter_cells
        side = sides[0]
        source_rows.append(row_index)
        for vi in range(parameter_cells):
            v0, v1 = Q(vi, parameter_cells), Q(vi + 1, parameter_cells)
            s0 = outer.S_LOWER + (outer.S_UPPER - outer.S_LOWER) * v0
            s1 = outer.S_LOWER + (outer.S_UPPER - outer.S_LOWER) * v1
            witness = source_grazing_endpoint_scaled_cp(
                row, side, s0, s1, terminal_t_width
            )
            records.append({"row_index": row_index, "v_cell": vi, **witness})

    old_count = int(frozen_frontier["terminal_reason_counts"]["source_cp_not_strict"])
    assert len(records) == old_count == 1536
    old_source_width = Q(
        frozen_frontier["uniform_fixed_s_terminal_reason_t_width_outers"][
            "source_cp_not_strict"
        ]
    )
    assert old_source_width == Q(3, 128)
    # Every certified source row contributes exactly one terminal-width cell
    # on every one of the 64 half-open parameter cells, including the closed
    # v=1 ledger.  Hence its fixed-s width is constant, not merely bounded.
    assert old_source_width == len(source_rows) * terminal_t_width
    return {
        "canonical_endpoint_band_parameter_cell_count": len(records),
        "frozen_source_tagged_terminal_count_for_comparison_only": old_count,
        "canonical_source_grazing_row_count": len(source_rows),
        "source_incidence_row_indices": source_rows,
        "parameter_cells_per_source_row": parameter_cells,
        "terminal_t_width_per_source_row": str(terminal_t_width),
        "canonical_endpoint_band_fixed_s_width": str(old_source_width),
        "closed_v1_endpoint_included": True,
        "endpoint_scaled_record_ledger_sha256": canonical_digest(records),
        "canonical_endpoint_bands_have_strictly_positive_source_cp": True,
        "frozen_terminal_record_to_endpoint_band_containment_certified": False,
        "frozen_terminal_boxes_removed_or_reclassified": False,
    }


def critical_resultant_identity() -> dict[str, Any]:
    """Freeze the exact critical-root Jacobian reduction.

    For ``Delta=r^2-w^2`` with constant target radius, a critical zero has
    ``w=sigma r`` and ``w_t=0``.  There

      det D_(t,s)(Delta,Delta_t) = -4 r^2 w_s w_tt.

    Nonvanishing of the last product is therefore the exact regular-value
    test.  This function certifies the coefficient algebra only; it does not
    claim interval nonvanishing on the frozen critical boxes.
    """

    # Coefficient check at a critical zero.  Store monomials as exponent
    # tuples (r, ws, wtt); both routes must yield -4*r^2*ws*wtt.
    delta_s = { (1, 1, 0): -2 }
    delta_tt = { (1, 0, 1): -2 }
    determinant: dict[tuple[int, int, int], int] = {}
    for (a1, b1, c1), v1 in delta_s.items():
        for (a2, b2, c2), v2 in delta_tt.items():
            key = (a1 + a2, b1 + b2, c1 + c2)
            determinant[key] = determinant.get(key, 0) - v1 * v2
    assert determinant == {(2, 1, 1): -4}
    return {
        "candidate_discriminant": "Delta=r^2-w^2",
        "critical_zero_equations": ["w=sigma*r", "w_t=0"],
        "critical_jacobian_determinant": "-4*r^2*w_s*w_tt",
        "coefficient_ledger": {"r^2*w_s*w_tt": -4},
        "algebraic_reduction_certified": True,
        "interval_nonvanishing_on_all_critical_boxes_certified": False,
        "absence_of_critical_junctions_certified": False,
    }


def deeper_selective_frontier(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Replay one additional level in each normalized coordinate.

    This is still a finite fail-closed outer atlas.  It is not extrapolated
    to zero mesh.  Only aggregate ledgers and a digest of the complete
    per-row result are exported, keeping the frozen artifact compact while
    the verifier recomputes the entire replay.
    """

    old_t = frozen.SELECTIVE_MAX_T_DEPTH
    old_v = frozen.SELECTIVE_MAX_V_DEPTH
    try:
        frozen.SELECTIVE_MAX_T_DEPTH = 6
        frozen.SELECTIVE_MAX_V_DEPTH = 4
        full = frozen.build_frontier(rows)
    finally:
        frozen.SELECTIVE_MAX_T_DEPTH = old_t
        frozen.SELECTIVE_MAX_V_DEPTH = old_v

    assert full["frozen_resolution"]["selective_terminal_t_depth"] == 6
    assert full["frozen_resolution"]["selective_terminal_parameter_depth"] == 4
    assert full["terminal_reason_counts"] == {
        "candidate_zero_with_dt_containing_zero": 12,
        "interval_geometry_exception": 151500,
        "source_cp_not_strict": 2048,
    }
    assert full["terminal_reason_nonphysical_parameter_areas"] == {
        "candidate_zero_with_dt_containing_zero": "3/65536",
        "interval_geometry_exception": "37875/65536",
        "source_cp_not_strict": "1/128",
    }
    assert full["uniform_fixed_s_terminal_reason_t_width_outers"] == {
        "candidate_zero_with_dt_containing_zero": "1/1024",
        "interval_geometry_exception": "595/1024",
        "source_cp_not_strict": "1/128",
    }
    assert full["uniform_fixed_s_terminal_positive_t_width_outer"] == "603/1024"
    assert full["conditionally_physical_first_graph_chart_count"] == 41344
    assert full["nonempty_physical_first_root_arc_count"] == 11678
    assert full["untyped_candidate_graph_chart_count"] == 164
    assert full["untyped_graph_failure_counts"] == {
        "additional_ambiguous_candidate_may_precede": 60,
        "untyped_candidate_graph_cover": 104,
    }
    assert full["total_audit_call_count"] == 1722936
    return {
        "selective_terminal_t_depth": 6,
        "selective_terminal_parameter_depth": 4,
        "terminal_reason_counts": full["terminal_reason_counts"],
        "terminal_reason_nonphysical_parameter_areas": full[
            "terminal_reason_nonphysical_parameter_areas"
        ],
        "uniform_fixed_s_terminal_reason_t_width_outers": full[
            "uniform_fixed_s_terminal_reason_t_width_outers"
        ],
        "maximum_terminal_boxes_on_one_fixed_s_slice": full[
            "maximum_terminal_boxes_on_one_fixed_s_slice"
        ],
        "uniform_fixed_s_terminal_positive_t_width_outer": full[
            "uniform_fixed_s_terminal_positive_t_width_outer"
        ],
        "conditionally_physical_first_graph_chart_count": full[
            "conditionally_physical_first_graph_chart_count"
        ],
        "conditionally_physical_first_dt_sign_counts": full[
            "conditionally_physical_first_dt_sign_counts"
        ],
        "nonempty_physical_first_root_arc_count": full[
            "nonempty_physical_first_root_arc_count"
        ],
        "untyped_candidate_graph_chart_count": full[
            "untyped_candidate_graph_chart_count"
        ],
        "untyped_graph_failure_counts": full["untyped_graph_failure_counts"],
        "maximum_conditionally_physical_first_graph_charts_on_one_fixed_s_slice": full[
            "maximum_conditionally_physical_first_graph_charts_on_one_fixed_s_slice"
        ],
        "maximum_nonempty_physical_first_root_arcs_on_one_fixed_s_slice": full[
            "maximum_nonempty_physical_first_root_arcs_on_one_fixed_s_slice"
        ],
        "maximum_normalized_absolute_root_slope_sum_on_one_fixed_s_slice": full[
            "maximum_normalized_absolute_root_slope_sum_on_one_fixed_s_slice"
        ],
        "maximum_candidate_graph_charts_on_one_fixed_s_slice": full[
            "maximum_candidate_graph_charts_on_one_fixed_s_slice"
        ],
        "maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice": full[
            "maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice"
        ],
        "partial_genuine_physical_marked_current_TV_upper": full[
            "partial_genuine_physical_marked_current_TV_upper"
        ],
        "partial_current_definition": full["partial_current_definition"],
        "graph_velocity_current_orientation_identity": full[
            "graph_velocity_current_orientation_identity"
        ],
        "closed_final_v_endpoint_explicitly_included_in_all_sweeps": full[
            "closed_final_v_endpoint_explicitly_included_in_all_sweeps"
        ],
        "closed_v1_endpoint_sweep_values": full[
            "closed_v1_endpoint_sweep_values"
        ],
        "ordered_row_summary_ledger_sha256": full[
            "ordered_row_summary_ledger_sha256"
        ],
        "total_audit_call_count": full["total_audit_call_count"],
        "complete_replay_sha256": canonical_digest(full),
    }


def build_result() -> dict[str, Any]:
    wrapper = json.loads(FROZEN_MANIFEST.read_text(encoding="utf-8"))
    frozen_result = wrapper["result"]
    frozen_frontier = frozen_result["reason_resolved_frontier"]
    assert wrapper["verdict"]["gate3"] == "NOT_CERTIFIED"
    rows, provenance = frozen.load_dependencies()
    endpoint = endpoint_scaled_source_incidence_audit(rows, frozen_frontier)
    resultant = critical_resultant_identity()
    deeper = deeper_selective_frontier(rows)

    old_width = Q(frozen_frontier["uniform_fixed_s_terminal_positive_t_width_outer"])
    canonical_band_width = Q(endpoint["canonical_endpoint_band_fixed_s_width"])
    assert old_width == Q(373, 256)
    assert canonical_band_width == Q(3, 128)
    deep_reasons = deeper["terminal_reason_counts"]
    deep_terminal_count = sum(deep_reasons.values())
    assert deep_terminal_count == 153560

    result = {
        "schema": "cm2.gate3.endpoint-scaled-resultant-frontier.v1",
        "provenance": {
            "frozen_physical_first_manifest_sha256": file_sha256(FROZEN_MANIFEST),
            "frozen_physical_first_certificate_sha256": file_sha256(Path(frozen.__file__).resolve()),
            "frozen_internal_replay_digest": frozen_result["internal_replay_digest"],
            "maximal_row_registry_sha256": provenance["maximal_row_registry_sha256"],
        },
        "endpoint_scaled_source_incidence": endpoint,
        "critical_resultant_reduction": resultant,
        "deeper_selective_frontier": deeper,
        "retained_fail_closed_terminal_frontier": {
            "frozen_thirteenth_terminal_box_count": sum(
                frozen_frontier["terminal_reason_counts"].values()
            ),
            "frozen_thirteenth_source_tagged_terminal_count_retained": endpoint[
                "frozen_source_tagged_terminal_count_for_comparison_only"
            ],
            "deep_replay_source_tagged_descendant_count_pending_downstream_reclassification": deep_reasons[
                "source_cp_not_strict"
            ],
            "deep_replay_terminal_box_count_retained_fail_closed": deep_terminal_count,
            "deep_replay_terminal_reason_counts_retained_fail_closed": deep_reasons,
            "frozen_uniform_fixed_s_positive_t_width_outer": str(old_width),
            "raw_deep_replay_uniform_fixed_s_positive_t_width_outer": deeper[
                "uniform_fixed_s_terminal_positive_t_width_outer"
            ],
            "deep_replay_uniform_fixed_s_positive_t_width_outer_retained_fail_closed": deeper[
                "uniform_fixed_s_terminal_positive_t_width_outer"
            ],
            "parent_to_deep_source_descendant_containment_ledger_certified": False,
            "deep_source_descendant_downstream_miss_root_owner_classification_certified": False,
            "zero_intercept": False,
        },
        "scope_limits": {
            "canonical_endpoint_band_source_cp_positivity": True,
            "all_frozen_source_incidence_terminal_boxes_resolved": False,
            "frozen_terminal_record_to_endpoint_band_containment_certified": False,
            "canonical_endpoint_band_coordinate_regular_on_full_parameter_window": True,
            "all_deeper_source_tagged_descendants_covered_and_reclassified": False,
            "critical_resultant_algebraic_reduction": True,
            "critical_resultant_interval_nonvanishing": False,
            "interval_geometry_exception_boxes_resolved": False,
            "critical_root_boxes_resolved": False,
            "all_candidate_graph_charts_typed": False,
            "complete_side_owner_current": False,
            "strong_component_restriction_DQ": False,
            "branch_record_MT_DQ": False,
            "physical_FACE_2CUT": False,
            "physical_FACE_TIME": False,
            "gate3_certified": False,
        },
        "exact_remaining_blockers": [
            "resolve the 151,500 deeper-replay interval-geometry boxes in analogous cancellation-free miss/root-gap coordinates",
            "interval-certify w_s*w_tt nonvanishing or isolate every zero of the critical resultant on the 12 remaining critical boxes",
            "type the 164 remaining candidate graph charts by a unique miss-side owner",
            "freeze coordinatewise containment for the 1,536 frozen source-tagged records and the 2,048 deeper descendants, then continue downstream miss-delta/root-gap/candidate/owner classification",
            "assemble the complete side-owner current with coefficient partial_s_Delta/abs(partial_t_Delta)",
            "prove strong component restriction DQ, branch-record MT_DQ, FACE_2CUT, and FACE_TIME",
        ],
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


if __name__ == "__main__":
    print(json.dumps(build_result(), sort_keys=True, indent=2))
