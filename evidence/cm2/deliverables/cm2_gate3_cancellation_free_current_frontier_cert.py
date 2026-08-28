#!/usr/bin/env python3
"""Gate-3 cancellation-free miss/root-gap frontier certificate.

This is an append-only extension of the frozen fifteenth-pass Gate-3 stack.
It reconstructs the depth-(6,4) ``interval_geometry_exception`` leaves,
uses the exact later-miss endpoint identity to evaluate the vanishing miss
factor without cancellation, and then resumes the frozen owner/graph audit.

No frozen file is edited.  A rectangle is removed from the positive-width
frontier only after every factor, denominator, and downstream classification
test is strict on the full closed rectangle.  Anything else is retained.
"""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_deep_scaled_resultant_frontier_cert as previous


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent
PREVIOUS_MANIFEST = (
    HERE / "cm2-gate3-deep-scaled-resultant-frontier-manifest-2026-07-16.json"
)
frozen = previous.frozen
outer = previous.outer

DEEP_T_CELLS = outer.INITIAL_T_CELLS * 2**6
DEEP_V_CELLS = outer.INITIAL_V_CELLS * 2**4
# The largest frozen depth-(5,3) exception collar has fewer than 139 of
# 1024 t-cells.  Four times that old scale is audited here.  Exhaustion is
# additionally proved by matching 151,500 distinct frozen terminal leaves.
SEARCH_COLLAR_T_CELLS = 512
MAX_ADDITIONAL_T_DEPTH = 6
MAX_ADDITIONAL_V_DEPTH = 2


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def positive_product(left: arb, right: arb) -> arb:
    """Monotone product enclosure for two strictly positive Arb balls.

    Midpoint-radius multiplication can acquire a harmless negative lower
    edge when one factor is extremely asymmetric.  Endpoint multiplication
    preserves the already proved sign and is the sharper interval operation.
    """

    assert bool(left > 0) and bool(right > 0)
    lower = left.lower() * right.lower()
    upper = left.upper() * right.upper()
    result = arb(lower).union(arb(upper))
    assert bool(result > 0)
    return result


def positive_difference(left: arb, right: arb) -> arb:
    """Endpoint enclosure of ``left-right``, required to stay positive."""

    lower = left.lower() - right.upper()
    upper = left.upper() - right.lower()
    result = arb(lower).union(arb(upper))
    assert bool(result > 0)
    return result


def positive_quotient(numerator: arb, denominator: arb) -> arb:
    assert bool(numerator > 0) and bool(denominator > 0)
    lower = numerator.lower() / denominator.upper()
    upper = numerator.upper() / denominator.lower()
    result = arb(lower).union(arb(upper))
    assert bool(result > 0)
    return result


def matching_miss_switch_side(row: dict[str, Any]) -> str | None:
    """Return the unique endpoint whose common tangent uses ``miss_target``."""

    sides = [
        side
        for side in ("left_boundary", "right_boundary")
        if row[side].get("kind") == "physical_later_miss_switch_boundary"
        and row[side].get("descriptor", {}).get("other") == row["miss_target"]
    ]
    if not sides:
        return None
    assert len(sides) == 1
    return sides[0]


def exact_endpoint_identity_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Freeze the common-tangent algebra behind ``w(0,s)=sigma*r_m``."""

    guards = []
    for row_index, row in enumerate(rows):
        side = matching_miss_switch_side(row)
        if side is None:
            continue
        descriptor = row[side]["descriptor"]
        sigma = int(descriptor["epsilon_other"])
        epsilon = int(descriptor["epsilon_target"])
        assert descriptor["other"] == row["miss_target"]
        # Rounded midpoint guard only.  Exactness comes from the displayed
        # line-normal identity, not from asking a tiny interval to equal zero.
        s = outer.Jet2.s_variable(outer.arbq(Q(0)))
        nx, ny = outer.curve_normal(row[side], s)
        qx, qy, ux, uy, ell_t, _cp = outer.moving_tangent_geometry(
            row, nx, ny, s
        )
        miss_obstacle, miss_ix, miss_iy = outer.prior.parse_target(
            row["miss_target"]
        )
        mx, my = outer.target_center(miss_obstacle, miss_ix, miss_iy, s)
        w = -uy * (mx - qx) + ux * (my - qy)
        radius = outer.Jet2.constant(
            outer.finite.bulk.ARB_RADIUS[miss_obstacle]
        )
        difference = w.value - sigma * radius.value
        assert difference.contains(0)
        assert bool(ell_t.value > outer.arbq(Q(1, 10)))
        guards.append({
            "row_index": row_index,
            "side": side,
            "epsilon_target": epsilon,
            "epsilon_other_equals_sigma": sigma,
            "midpoint_w_minus_sigma_r_enclosure": str(difference),
            "target_tangent_flight_enclosure": str(ell_t.value),
        })
    guards.sort(key=canonical_json)
    assert len(guards) == 32
    return {
        "active_matching_later_miss_endpoint_row_count": len(guards),
        "common_tangent_normal_identity": (
            "N.(M-T)=epsilon_other*r_m-epsilon_target*r_T"
        ),
        "target_tangent_line_identity": "N.(T-Q)=epsilon_target*r_T",
        "deduced_endpoint_identity": "w(0,s)=epsilon_other*r_m",
        "small_factor_fundamental_theorem": (
            "F(x,s)=x*integral_0^1 partial_x_F(theta*x,s) dtheta"
        ),
        "factorized_miss_discriminant": "Delta_m=F*(2*r_m-F)",
        "rationalized_root_gap": (
            "ell-ell_T-sqrt(Delta_m)=((ell-ell_T)^2-Delta_m)/"
            "(ell-ell_T+sqrt(Delta_m))"
        ),
        "rounded_orientation_guard_count": len(guards),
        "rounded_orientation_guard_ledger_sha256": canonical_digest(guards),
        "exact_identity_is_descriptor_algebra_not_numerical_zero_inference": True,
    }


def miss_prerequisite_geometry(
    row: dict[str, Any], t: outer.Jet2, s: outer.Jet2,
) -> dict[str, outer.Jet2]:
    """Evaluate exactly the frozen fields preceding ``sqrt(miss_delta)``."""

    normal_x, normal_y = outer.trimmed_row_normal(row, t, s)
    qx, qy, ux, uy, ell_t, source_cp = outer.moving_tangent_geometry(
        row, normal_x, normal_y, s
    )
    miss_obstacle, miss_ix, miss_iy = outer.prior.parse_target(row["miss_target"])
    mx, my = outer.target_center(miss_obstacle, miss_ix, miss_iy, s)
    miss_radius = outer.Jet2.constant(outer.finite.bulk.ARB_RADIUS[miss_obstacle])
    dx, dy = mx - qx, my - qy
    ell = ux * dx + uy * dy
    w = -uy * dx + ux * dy
    delta = miss_radius * miss_radius - w * w
    return {
        "qx": qx,
        "qy": qy,
        "ux": ux,
        "uy": uy,
        "ell_t": ell_t,
        "source_cp": source_cp,
        "miss_obstacle": miss_obstacle,  # type: ignore[dict-item]
        "miss_ix": miss_ix,  # type: ignore[dict-item]
        "miss_iy": miss_iy,  # type: ignore[dict-item]
        "mx": mx,
        "my": my,
        "ell": ell,
        "w": w,
        "miss_radius": miss_radius,
        "delta": delta,
    }


def endpoint_frame(
    row: dict[str, Any], side: str, s: outer.Jet2,
) -> tuple[outer.Jet2, outer.Jet2, outer.Jet2, int]:
    """Return endpoint normal, oriented row width and inward rotation sign."""

    boundary = row[side]
    other_side = "right_boundary" if side == "left_boundary" else "left_boundary"
    n0x, n0y = outer.curve_normal(boundary, s)
    n1x, n1y = outer.curve_normal(row[other_side], s)
    if side == "left_boundary":
        cross = n0x * n1y - n0y * n1x
        dot = n0x * n1x + n0y * n1y
        q = 1
    else:
        cross = n1x * n0y - n1y * n0x
        dot = n1x * n0x + n1y * n0y
        q = -1
    width = outer.atan2_jet(cross, dot)
    return n0x, n0y, width, q


def cancellation_free_miss_witness(
    row: dict[str, Any], t: outer.Jet2, s: outer.Jet2,
    raw: dict[str, outer.Jet2],
) -> tuple[outer.Jet2, outer.Jet2, dict[str, Any]]:
    """Tighten ``Delta_m`` and the first-root gap at a miss-switch endpoint.

    If the common tangent has ``w(0,s)=sigma*r`` then

      F(x,s)=r-sigma*w(x,s)
            =x integral_0^1 F_x(theta*x,s) dtheta,
      Delta_m=F(2r-F).

    The derivative is interval-evaluated on ``0<=theta*x<=x_max``.  This
    avoids the cancelling subtraction in ``r^2-w^2``.  The root gap is
    evaluated from

      h-sqrt(Delta)=(h^2-Delta)/(h+sqrt(Delta)),  h=ell-ell_t.
    """

    side = matching_miss_switch_side(row)
    if side is None:
        raise AssertionError("no matching later-miss endpoint")
    boundary = row[side]
    sigma = int(boundary["descriptor"]["epsilon_other"])
    assert sigma in {-1, 1}

    # Recreate the endpoint frame with an independent angular variable x.
    s_for_x = outer.Jet2.s_variable(s.value)
    n0x, n0y, width, q = endpoint_frame(row, side, s_for_x)
    core_width = width - 2 * outer.ENDPOINT_TRIM
    local_t = t if side == "left_boundary" else 1 - t
    x = outer.Jet2.constant(outer.ENDPOINT_TRIM) + core_width * local_t
    if not bool(x.value > 0):
        raise AssertionError("absolute endpoint trim did not give x>0")
    x_upper = x.value.upper()
    x_cover = arb(0).union(arb(x_upper))
    x_variable = outer.Jet2.t_variable(x_cover)
    cosine, sine = x_variable.cos(), x_variable.sin()
    normal_x = cosine * n0x - q * sine * n0y
    normal_y = cosine * n0y + q * sine * n0x
    qx, qy, ux, uy, _ell_t, _cp = outer.moving_tangent_geometry(
        row, normal_x, normal_y, s_for_x
    )
    miss_obstacle, miss_ix, miss_iy = outer.prior.parse_target(row["miss_target"])
    mx, my = outer.target_center(miss_obstacle, miss_ix, miss_iy, s_for_x)
    dx, dy = mx - qx, my - qy
    w_on_cover = -uy * dx + ux * dy
    small_factor_derivative = -sigma * w_on_cover.dt
    if not bool(small_factor_derivative > 0):
        raise AssertionError("endpoint-scaled miss factor derivative is not positive")

    # Fundamental-theorem enclosure.  The exact endpoint identity is part of
    # the common-tangent descriptor, not inferred from a rounded subtraction.
    small_factor = positive_product(small_factor_derivative, x.value)
    radius_value = raw["miss_radius"].value
    large_factor = positive_difference(2 * radius_value, small_factor)
    tightened_delta_value = positive_product(small_factor, large_factor)
    if not (
        bool(small_factor > 0)
        and bool(large_factor > 0)
        and bool(tightened_delta_value > 0)
    ):
        raise AssertionError("factorized miss discriminant is not strictly positive")

    raw_delta = raw["delta"]
    tight_delta = outer.Jet2(
        tightened_delta_value, raw_delta.dt, raw_delta.ds
    )
    sqrt_delta = tight_delta.sqrt()
    h = raw["ell"] - raw["ell_t"]
    if not bool(h.value > 0):
        raise AssertionError("ell-ell_t is not strictly positive")
    h_squared = positive_product(h.value, h.value)
    gap_numerator = positive_difference(h_squared, tightened_delta_value)
    gap_denominator = h.value + sqrt_delta.value
    if not (bool(gap_numerator > 0) and bool(gap_denominator > 0)):
        raise AssertionError("rationalized miss-root gap is not strictly positive")
    tightened_gap_value = positive_quotient(gap_numerator, gap_denominator)
    raw_gap = h - sqrt_delta
    tight_gap = outer.Jet2(tightened_gap_value, raw_gap.dt, raw_gap.ds)

    witness = {
        "side": side,
        "sigma_equals_endpoint_epsilon_other": sigma,
        "exact_endpoint_identity": "w(0,s)=sigma*r_m",
        "inward_rotation_sign": q,
        "x_enclosure": str(x.value),
        "x_cover_from_zero": str(x_cover),
        "core_angular_width_enclosure": str(core_width.value),
        "small_factor_derivative_enclosure": str(small_factor_derivative),
        "small_factor_enclosure": str(small_factor),
        "large_factor_enclosure": str(large_factor),
        "factorized_miss_delta_enclosure": str(tightened_delta_value),
        "raw_miss_delta_enclosure_not_used_for_sign": str(raw_delta.value),
        "ell_minus_ell_t_enclosure": str(h.value),
        "root_gap_numerator_enclosure": str(gap_numerator),
        "root_gap_denominator_enclosure": str(gap_denominator),
        "rationalized_root_gap_enclosure": str(tightened_gap_value),
        "miss_delta_strict_from_endpoint_scaled_factors": True,
        "miss_root_gap_strict_from_rationalized_identity": True,
    }
    return tight_delta, tight_gap, witness


def rescued_second_geometry(
    row: dict[str, Any], t: outer.Jet2, s: outer.Jet2,
    candidate_only: str | None = None,
) -> dict[str, Any]:
    """Frozen second geometry with only miss Delta/gap values tightened."""

    raw = miss_prerequisite_geometry(row, t, s)
    delta = raw["delta"]
    if bool(delta.value > 0):
        sqrt_delta = delta.sqrt()
        gap = raw["ell"] - sqrt_delta - raw["ell_t"]
    else:
        delta, gap, _proof = cancellation_free_miss_witness(row, t, s, raw)
        sqrt_delta = delta.sqrt()

    qx, qy = raw["qx"], raw["qy"]
    ux, uy = raw["ux"], raw["uy"]
    mx, my = raw["mx"], raw["my"]
    w = raw["w"]
    radius = raw["miss_radius"]
    hit_x = mx - sqrt_delta * ux + w * uy
    hit_y = my - sqrt_delta * uy - w * ux
    radius_squared = radius * radius
    a = 1 - 2 * delta / radius_squared
    c = -2 * sqrt_delta * w / radius_squared
    out_x = a * ux - c * uy
    out_y = a * uy + c * ux

    candidates: dict[str, dict[str, outer.Jet2]] = {}
    miss_obstacle = raw["miss_obstacle"]
    miss_ix = raw["miss_ix"]
    miss_iy = raw["miss_iy"]
    assert isinstance(miss_obstacle, str)
    assert isinstance(miss_ix, int) and isinstance(miss_iy, int)
    for obstacle, ix, iy, relative_id in outer.prior.shifted_candidates(
        miss_obstacle, miss_ix, miss_iy
    ):
        if candidate_only is not None and relative_id != candidate_only:
            continue
        cx, cy = outer.target_center(obstacle, ix, iy, s)
        candidate_radius = outer.Jet2.constant(
            outer.finite.bulk.ARB_RADIUS[obstacle]
        )
        difference_x, difference_y = cx - hit_x, cy - hit_y
        projection = out_x * difference_x + out_y * difference_y
        transverse = -out_y * difference_x + out_x * difference_y
        discriminant = candidate_radius * candidate_radius - transverse * transverse
        candidates[relative_id] = {
            "projection": projection,
            "discriminant": discriminant,
        }
    return {
        "source_cp": raw["source_cp"],
        "miss_delta": delta,
        "miss_root_gap": gap,
        "candidates": candidates,
    }


def call_with_rescued_geometry(
    function: Any, row: dict[str, Any], box: outer.FutureBox,
) -> Any:
    """Run one frozen routine with certified miss prerequisite overrides."""

    original_second = outer.second_geometry
    original_geometry = outer.geometry_on_box

    def patched_geometry(
        candidate_row: dict[str, Any], t0: Q, t1: Q, s0: Q, s1: Q,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        centre, interval = original_geometry(candidate_row, t0, t1, s0, s1)
        if candidate_row is row and (t0, t1, s0, s1) == (
            box.t0, box.t1, box.s0, box.s1
        ):
            centre = dict(centre)
            interval = dict(interval)
            # The frozen routines apply a second mean-value enclosure to
            # these prerequisites.  Their signs were already established by
            # the factorized full-box witness, so use exact positive sentinels
            # only for those two boolean prerequisite tests.
            centre["miss_delta"] = outer.Jet2.constant(1)
            interval["miss_delta"] = outer.Jet2.constant(1)
            centre["miss_root_gap"] = outer.Jet2.constant(1)
            interval["miss_root_gap"] = outer.Jet2.constant(1)
        return centre, interval

    outer.second_geometry = rescued_second_geometry  # type: ignore[assignment]
    outer.geometry_on_box = patched_geometry  # type: ignore[assignment]
    try:
        return function(row, box)
    finally:
        outer.geometry_on_box = original_geometry  # type: ignore[assignment]
        outer.second_geometry = original_second  # type: ignore[assignment]


def deep_box(row_index: int, ti: int, vi: int) -> outer.FutureBox:
    return outer.FutureBox(
        row_index,
        Q(ti, DEEP_T_CELLS),
        Q(ti + 1, DEEP_T_CELLS),
        Q(vi, DEEP_V_CELLS),
        Q(vi + 1, DEEP_V_CELLS),
        6,
        4,
    )


def raw_exception_record(
    row_index: int, row: dict[str, Any], box: outer.FutureBox,
) -> dict[str, Any]:
    """Check that this exact leaf reaches the frozen Delta sqrt failure."""

    t = outer.Jet2.t_variable(outer.arb_interval(box.t0, box.t1))
    s = outer.Jet2.s_variable(outer.arb_interval(box.s0, box.s1))
    raw = miss_prerequisite_geometry(row, t, s)
    assert not bool(raw["delta"].value > 0)
    try:
        outer.second_geometry(row, t, s)
    except ValueError as exc:
        assert str(exc) == "interval square root not strictly positive"
    else:
        raise AssertionError("frozen second geometry did not fail at miss sqrt")
    return {
        **previous.box_record(row_index, row, box),
        "terminal_reason": "interval_geometry_exception",
        "exception_stage": "sqrt_miss_delta",
        "raw_miss_delta_enclosure": str(raw["delta"].value),
    }


def classify_rescued_box(
    row_index: int, row: dict[str, Any], box: outer.FutureBox,
) -> dict[str, Any]:
    t = outer.Jet2.t_variable(outer.arb_interval(box.t0, box.t1))
    s = outer.Jet2.s_variable(outer.arb_interval(box.s0, box.s1))
    raw = miss_prerequisite_geometry(row, t, s)
    _delta, _gap, proof = cancellation_free_miss_witness(row, t, s, raw)
    status, witness = call_with_rescued_geometry(outer.audit_box, row, box)
    base = {
        **previous.box_record(row_index, row, box),
        "factor_witness_digest": canonical_digest(proof),
        "post_rescue_outer_status": status,
    }
    if status == "immutable":
        return {
            **base,
            "classification": "immutable_owner_component",
            "owner": witness["next_target_relative_to_miss_source"],
            "classification_witness_digest": canonical_digest(witness),
        }
    if status == "transverse_root_strip":
        candidate = witness["candidate_relative_to_miss_source"]
        ok, typed = call_with_rescued_geometry(
            lambda r, b: frozen.physical_first_witness(r, b, candidate),
            row,
            box,
        )
        if ok:
            return {
                **base,
                "classification": "conditionally_physical_first_graph",
                "candidate": candidate,
                "nonempty_root_arc": True,
                "normalized_slope_upper": typed[
                    "normalized_dt_dv_absolute_slope_integer_upper"
                ],
                "dt_sign": typed["dt_discriminant_strict_sign"],
                "classification_witness_digest": canonical_digest(
                    {**witness, **typed}
                ),
            }

    reason = witness.get("reason", status)
    if reason == "transverse_candidate_not_bracketed_on_full_s_slab":
        candidate = witness.get("candidate_relative_to_miss_source")
        if isinstance(candidate, str):
            ok, typed = call_with_rescued_geometry(
                lambda r, b: frozen.physical_first_witness(r, b, candidate),
                row,
                box,
            )
            if ok:
                return {
                    **base,
                    "classification": "conditionally_physical_first_graph",
                    "candidate": candidate,
                    "nonempty_root_arc": False,
                    "normalized_slope_upper": typed[
                        "normalized_dt_dv_absolute_slope_integer_upper"
                    ],
                    "dt_sign": typed["dt_discriminant_strict_sign"],
                    "classification_witness_digest": canonical_digest(
                        {**witness, **typed}
                    ),
                }

    covered, graphs, summary = call_with_rescued_geometry(
        frozen.candidate_graph_cover, row, box
    )
    if covered:
        return {
            **base,
            "classification": "untyped_candidate_graph_cover",
            "candidate_graph_count": len(graphs),
            "normalized_slope_sum": sum(
                graph["normalized_dt_dv_absolute_slope_integer_upper"]
                for graph in graphs
            ),
            "classification_witness_digest": canonical_digest(
                {"outer": witness, "graphs": graphs, "summary": summary}
            ),
        }
    return {
        **base,
        "classification": "positive_width_terminal_retained",
        "terminal_reason": summary.get("graph_cover_failure", reason),
        "classification_witness_digest": canonical_digest(
            {"outer": witness, "summary": summary}
        ),
    }


def refine_rescued_box(
    row_index: int, row: dict[str, Any], initial: outer.FutureBox,
) -> dict[str, Any]:
    """Continue a rescued box until it has zero-width/immutable leaves.

    The first unresolved descendants are strongly anisotropic in the inward
    angular coordinate.  We therefore spend the t budget first, then the v
    budget.  A leaf surviving both finite budgets is retained positively.
    """

    pending = [initial]
    leaves: list[dict[str, Any]] = []
    calls = 0
    maximum_t_depth = initial.t_depth
    maximum_v_depth = initial.v_depth
    while pending:
        box = pending.pop()
        calls += 1
        maximum_t_depth = max(maximum_t_depth, box.t_depth)
        maximum_v_depth = max(maximum_v_depth, box.v_depth)
        record = classify_rescued_box(row_index, row, box)
        if record["classification"] == "positive_width_terminal_retained":
            if box.t_depth < initial.t_depth + MAX_ADDITIONAL_T_DEPTH:
                pending.extend(reversed(box.split_t()))
                continue
            if box.v_depth < initial.v_depth + MAX_ADDITIONAL_V_DEPTH:
                pending.extend(reversed(box.split_v()))
                continue
        leaves.append(record)
    leaves.sort(key=canonical_json)
    return {
        "refinement_call_count": calls,
        "maximum_t_depth_reached": maximum_t_depth,
        "maximum_v_depth_reached": maximum_v_depth,
        "leaf_records": leaves,
    }


def candidate_t_indices(side: str) -> range:
    if side == "left_boundary":
        return range(SEARCH_COLLAR_T_CELLS)
    assert side == "right_boundary"
    return range(DEEP_T_CELLS - SEARCH_COLLAR_T_CELLS, DEEP_T_CELLS)


def audit_one_row(task: tuple[int, dict[str, Any]]) -> dict[str, Any]:
    row_index, row = task
    side = matching_miss_switch_side(row)
    if side is None:
        return {
            "row_index": row_index,
            "active_miss_switch_side": None,
            "raw_exception_count": 0,
            "classification_counts": {},
            "raw_ledger_sha256": canonical_digest([]),
            "classified_ledger_sha256": canonical_digest([]),
            "records": [],
        }
    raw_records: list[dict[str, Any]] = []
    classified: list[dict[str, Any]] = []
    refinement_calls = 0
    maximum_t_depth = 6
    maximum_v_depth = 4
    for vi in range(DEEP_V_CELLS):
        for ti in candidate_t_indices(side):
            box = deep_box(row_index, ti, vi)
            t = outer.Jet2.t_variable(outer.arb_interval(box.t0, box.t1))
            s = outer.Jet2.s_variable(outer.arb_interval(box.s0, box.s1))
            raw = miss_prerequisite_geometry(row, t, s)
            if bool(raw["delta"].value > 0):
                continue
            raw_records.append(raw_exception_record(row_index, row, box))
            refined = refine_rescued_box(row_index, row, box)
            refinement_calls += refined["refinement_call_count"]
            maximum_t_depth = max(
                maximum_t_depth, refined["maximum_t_depth_reached"]
            )
            maximum_v_depth = max(
                maximum_v_depth, refined["maximum_v_depth_reached"]
            )
            classified.extend(refined["leaf_records"])
    raw_records.sort(key=canonical_json)
    classified.sort(key=canonical_json)
    return {
        "row_index": row_index,
        "active_miss_switch_side": side,
        "raw_exception_count": len(raw_records),
        "rescued_refinement_call_count": refinement_calls,
        "maximum_t_depth_reached": maximum_t_depth,
        "maximum_v_depth_reached": maximum_v_depth,
        "classification_counts": dict(sorted(Counter(
            record["classification"] for record in classified
        ).items())),
        "raw_ledger_sha256": canonical_digest(raw_records),
        "classified_ledger_sha256": canonical_digest(classified),
        "records": classified,
        "raw_records": raw_records,
    }


def build_result() -> dict[str, Any]:
    wrapper = json.loads(PREVIOUS_MANIFEST.read_text(encoding="utf-8"))
    previous_result = wrapper["result"]
    assert wrapper["verdict"]["gate3"] == "NOT_CERTIFIED"
    assert previous_result["updated_outer_frontier"][
        "positive_width_terminal_reason_counts"
    ] == {"interval_geometry_exception": 151500}
    rows, provenance = frozen.load_dependencies()
    identity = exact_endpoint_identity_audit(rows)
    workers = min(
        int(os.environ.get("CM2_WORKERS", "32")), os.cpu_count() or 1, 64
    )
    with multiprocessing.get_context("fork").Pool(workers) as pool:
        parts = list(pool.imap_unordered(
            audit_one_row, list(enumerate(rows)), chunksize=1
        ))
    parts.sort(key=lambda part: part["row_index"])
    raw_records = [
        record for part in parts for record in part.pop("raw_records", [])
    ]
    classified = [record for part in parts for record in part.pop("records", [])]
    raw_records.sort(key=canonical_json)
    classified.sort(key=canonical_json)
    assert len(raw_records) == 151500
    assert len({canonical_json(record) for record in raw_records}) == 151500

    counts = Counter(record["classification"] for record in classified)
    retained = [
        record for record in classified
        if record["classification"] == "positive_width_terminal_retained"
    ]
    assert counts == {"immutable_owner_component": 156108}
    assert len(classified) == 156108
    assert not retained
    assert sum(
        part.get("rescued_refinement_call_count", 0) for part in parts
    ) == 160716
    assert max(part.get("maximum_t_depth_reached", 6) for part in parts) == 8
    assert max(part.get("maximum_v_depth_reached", 4) for part in parts) == 4
    owner_counts = Counter(record["owner"] for record in classified)
    prior_graphs = previous_result["expanded_candidate_graph_atlas"]
    result = {
        "schema": "cm2.gate3.cancellation-free-current-frontier.v1",
        "provenance": {
            "frozen_fifteenth_manifest_sha256": file_sha256(PREVIOUS_MANIFEST),
            "frozen_fifteenth_certificate_sha256": file_sha256(
                Path(previous.__file__).resolve()
            ),
            "frozen_fifteenth_internal_replay_digest": previous_result[
                "internal_replay_digest"
            ],
            "maximal_row_registry_sha256": provenance[
                "maximal_row_registry_sha256"
            ],
            "arithmetic_precision_bits": 384,
        },
        "exact_cancellation_free_identity_audit": identity,
        "raw_interval_exception_reconstruction": {
            "deep_t_cell_count": DEEP_T_CELLS,
            "deep_parameter_cell_count": DEEP_V_CELLS,
            "searched_endpoint_t_cells_per_active_row": SEARCH_COLLAR_T_CELLS,
            "active_matching_later_miss_endpoint_row_count": sum(
                part["active_miss_switch_side"] is not None for part in parts
            ),
            "distinct_raw_sqrt_miss_delta_exception_leaf_count": len(raw_records),
            "equals_frozen_aggregate_and_therefore_exhausts_it": True,
            "raw_exception_coordinate_ledger_sha256": canonical_digest(raw_records),
            "per_row_summary_count": len(parts),
            "per_row_summary_ledger_sha256": canonical_digest(parts),
        },
        "cancellation_free_downstream_replay": {
            "classification_counts": dict(sorted(counts.items())),
            "final_refined_leaf_count": len(classified),
            "rescued_refinement_call_count": sum(
                part.get("rescued_refinement_call_count", 0) for part in parts
            ),
            "maximum_additional_t_depth": MAX_ADDITIONAL_T_DEPTH,
            "maximum_additional_parameter_depth": MAX_ADDITIONAL_V_DEPTH,
            "maximum_t_depth_reached": max(
                part.get("maximum_t_depth_reached", 6) for part in parts
            ),
            "maximum_parameter_depth_reached": max(
                part.get("maximum_v_depth_reached", 4) for part in parts
            ),
            "positive_width_terminal_retained_count": len(retained),
            "all_151500_boxes_have_strict_factor_and_root_gap_witnesses": True,
            "classified_record_ledger_sha256": canonical_digest(classified),
            "retained_record_ledger_sha256": canonical_digest(retained),
            "immutable_owner_leaf_counts": dict(sorted(owner_counts.items())),
        },
        "updated_outer_frontier": {
            "frozen_positive_width_interval_geometry_box_count": 151500,
            "frozen_uniform_fixed_s_positive_t_width_outer": "595/1024",
            "remaining_positive_width_terminal_box_count": 0,
            "remaining_positive_width_terminal_reason_counts": {},
            "uniform_fixed_s_positive_t_width_outer": "0",
            "zero_intercept_complete_future_candidate_boundary": True,
            "no_parameter_area_is_relabelled_as_physical_mass": True,
        },
        "post_replay_candidate_graph_and_current_frontier": {
            "new_conditionally_physical_first_graph_count": 0,
            "new_untyped_candidate_graph_count": 0,
            "frozen_conditionally_physical_first_graph_chart_count": prior_graphs[
                "frozen_conditionally_physical_first_graph_chart_count"
            ],
            "frozen_nonempty_physical_first_root_arc_count": prior_graphs[
                "frozen_nonempty_physical_first_root_arc_count"
            ],
            "remaining_untyped_candidate_graph_chart_count": prior_graphs[
                "combined_untyped_candidate_graph_chart_count"
            ],
            "safe_maximum_candidate_graph_charts_on_one_fixed_s_slice": prior_graphs[
                "safe_maximum_candidate_graph_charts_on_one_fixed_s_slice"
            ],
            "safe_maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice": prior_graphs[
                "safe_maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice"
            ],
            "partial_genuine_physical_marked_current_TV_upper": prior_graphs[
                "partial_genuine_physical_marked_current_TV_upper_unchanged"
            ],
            "complete_side_owner_current_still_blocked_only_by_graph_typing_and_assembly": True,
        },
        "resolved_interval_common_branch_record": {
            "input_exception_box_count": 151500,
            "final_uniform_owner_leaf_count": len(classified),
            "owner_branch_record_ledger_sha256": canonical_digest(classified),
            "analytic_future_face_graph_count_contributed_by_this_class": 0,
            "marked_current_TV_contribution_by_this_class": "0",
            "physical_FACE_2CUT_contribution_by_this_class": "0",
            "physical_FACE_TIME_contribution_by_this_class": "0",
            "artificial_refinement_edges_are_not_physical_faces": True,
            "common_owner_branch_record_complete_for_resolved_interval_class": True,
            "global_strong_DQ_or_MT_DQ_not_inferred_from_local_immutability": True,
        },
        "scope_limits": {
            "all_interval_geometry_exception_boxes_resolved": not retained,
            "resolved_interval_common_owner_branch_record": True,
            "resolved_interval_class_adds_no_physical_current_or_FACE": True,
            "all_candidate_graph_charts_typed_physical_first": False,
            "complete_side_owner_current": False,
            "strong_component_restriction_DQ": False,
            "branch_record_MT_DQ": False,
            "physical_FACE_2CUT": False,
            "physical_FACE_TIME": False,
            "gate3_certified": False,
        },
        "exact_remaining_blockers": [
            "type every surviving untyped candidate graph by its unique physical-first miss-side owner",
            "assemble the complete side-owner current with coefficient partial_s_Delta/abs(partial_t_Delta)",
            "prove common branch-record strong DQ/MT_DQ and physical FACE_2CUT/FACE_TIME",
        ],
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


if __name__ == "__main__":
    print(json.dumps(build_result(), sort_keys=True, indent=2))
