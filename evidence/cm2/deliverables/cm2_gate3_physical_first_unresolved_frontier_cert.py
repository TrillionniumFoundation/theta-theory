#!/usr/bin/env python3
"""Reason-resolved Gate-3 future atlas and physical-first root frontier.

This certificate is a strict extension of, and never a replacement for, the
frozen twelfth-pass finite-s future-candidate outer atlas.  It replays the
same 64 labelled ``(t,v)`` carriers and the same 4,704 discriminants, but
keeps terminal-reason ledgers and tests a stronger statement on every
transverse candidate root: at the tangency the candidate must be the first
physical collision, and the first collision on the miss side must be a
single uniformly typed alternative owner.

The normalized coordinate ``v`` is only a parameter coordinate.  It is not a
probability variable.  Every two-dimensional area in this file is therefore
nonphysical parameter bookkeeping.  Physical bounds use a supremum over
fixed-s slices only.  The artificial rectangular t-boundary is also kept
separate from the analytic future-collision boundary.
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

import cm2_gate3_finite_s_future_singularity_outer_atlas_cert as outer


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

OUTER_MANIFEST = (
    HERE / "cm2-gate3-finite-s-future-singularity-outer-atlas-manifest-2026-07-16.json"
)

# The first pass deliberately uses the frozen resolution.  The point of this
# stack is to distinguish analytic/prerequisite failures, positive-root order
# dependency, unbracketed transverse roots, and genuine multiple/critical
# blockers before any selective refinement is claimed.
MAX_T_DEPTH = outer.MAX_T_DEPTH
MAX_V_DEPTH = outer.MAX_V_DEPTH
SELECTIVE_MAX_T_DEPTH = 5
SELECTIVE_MAX_V_DEPTH = 3


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nearest_endpoint_trimmed_row_normal(
    row: dict[str, Any], t: outer.Jet2, s: outer.Jet2,
) -> tuple[outer.Jet2, outer.Jet2]:
    """Pointwise-identical two-anchor version of the frozen row formula.

    The frozen outer atlas deliberately used one left anchor.  Near t=1 the
    natural interval expression ``left+width`` repeats the same moving
    endpoint data and creates many false prerequisite failures.  Every
    initial and descendant t-cell lies in one closed half, so we anchor it at
    its nearest analytic endpoint exactly as in the already frozen finite-s
    common-core audit.
    """

    left_x, left_y = outer.curve_normal(row["left_boundary"], s)
    right_x, right_y = outer.curve_normal(row["right_boundary"], s)
    cross = left_x * right_y - left_y * right_x
    dot = left_x * right_x + left_y * right_y
    width = outer.atan2_jet(cross, dot)
    half = outer.arbq(Q(1, 2))
    if bool(t.value.mid() <= half):
        distance = outer.ENDPOINT_TRIM + (width - 2 * outer.ENDPOINT_TRIM) * t
        cosine, sine = distance.cos(), distance.sin()
        return (
            cosine * left_x - sine * left_y,
            cosine * left_y + sine * left_x,
        )
    if bool(t.value.mid() >= half):
        distance = (
            outer.ENDPOINT_TRIM
            + (width - 2 * outer.ENDPOINT_TRIM) * (1 - t)
        )
        cosine, sine = distance.cos(), distance.sin()
        return (
            cosine * right_x + sine * right_y,
            cosine * right_y - sine * right_x,
        )
    raise AssertionError("a t-cell crossed the exact half-row anchor seam")


# This is a process-local runtime binding only.  The frozen twelfth-pass file
# and manifest remain byte-for-byte unchanged.
outer.trimmed_row_normal = nearest_endpoint_trimmed_row_normal


def enclosure(
    centre: outer.Jet2, box: outer.Jet2, t_radius: Q, s_radius: Q,
) -> arb:
    return outer.field_enclosure(centre, box, t_radius, s_radius)


def positive_root_enclosure(
    centre_fields: dict[str, outer.Jet2],
    box_fields: dict[str, outer.Jet2],
    t_radius: Q,
    s_radius: Q,
) -> arb | None:
    discriminant = enclosure(
        centre_fields["discriminant"], box_fields["discriminant"],
        t_radius, s_radius,
    )
    projection = enclosure(
        centre_fields["projection"], box_fields["projection"],
        t_radius, s_radius,
    )
    if not bool(discriminant > 0):
        return None
    root = projection - discriminant.sqrt()
    far = projection + discriminant.sqrt()
    if bool(far < 0) or not bool(root > 0) or not bool(root < outer.arbq(outer.TAU_MAX)):
        return None
    return root


def physical_first_witness(
    row: dict[str, Any], box: outer.FutureBox, candidate: str,
) -> tuple[bool, dict[str, Any]]:
    """Certify that one transverse candidate root is a physical first face.

    At the graph ``Delta_candidate=0`` its collision time is exactly the
    projection.  We certify it lies strictly before one unique alternative
    owner, and that the latter lies before every remaining possible root.
    This types the two traces as grazing-hit versus first miss-side owner.
    """

    t_radius = (box.t1 - box.t0) / 2
    s_radius = (box.s1 - box.s0) / 2
    try:
        centre, interval = outer.geometry_on_box(
            row, box.t0, box.t1, box.s0, box.s1
        )
        boundary_projection = enclosure(
            centre["candidates"][candidate]["projection"],
            interval["candidates"][candidate]["projection"],
            t_radius, s_radius,
        )
        if not (
            bool(boundary_projection > 0)
            and bool(boundary_projection < outer.arbq(outer.TAU_MAX))
        ):
            return False, {"physical_first_failure": "candidate_tangent_time_not_forward"}

        roots: dict[str, arb] = {}
        nonblocking: dict[str, str] = {}
        possible_root_lowers: dict[str, arb] = {}
        for relative_id in sorted(interval["candidates"]):
            if relative_id == candidate:
                continue
            centre_fields = centre["candidates"][relative_id]
            box_fields = interval["candidates"][relative_id]
            discriminant = enclosure(
                centre_fields["discriminant"], box_fields["discriminant"],
                t_radius, s_radius,
            )
            projection = enclosure(
                centre_fields["projection"], box_fields["projection"],
                t_radius, s_radius,
            )
            if bool(discriminant < 0):
                nonblocking[relative_id] = "strict_miss"
                continue
            upper = discriminant.upper()
            if bool(upper < 0):
                nonblocking[relative_id] = "strict_miss"
                continue
            radical_upper = upper.sqrt()
            possible_near_lower = projection.lower() - radical_upper
            possible_far_upper = projection.upper() + radical_upper
            if bool(possible_far_upper < 0):
                nonblocking[relative_id] = "strict_behind"
                continue
            if bool(possible_near_lower > outer.arbq(outer.TAU_MAX)):
                nonblocking[relative_id] = "strict_after_tau3"
                continue
            root = positive_root_enclosure(
                centre_fields, box_fields, t_radius, s_radius
            )
            if root is not None:
                roots[relative_id] = root
            else:
                # A strictly positive discriminant whose near-root interval
                # crosses zero is still a possible forward competitor.  It
                # is retained by the same dependency-free lower bound used
                # for a discriminant that straddles tangency.
                possible_root_lowers[relative_id] = possible_near_lower

        alternative_owners = [
            relative_id for relative_id, root in roots.items()
            if all(
                other_id == relative_id or bool(root < other_root)
                for other_id, other_root in roots.items()
            )
        ]
        if len(alternative_owners) != 1:
            return False, {
                "physical_first_failure": "alternative_owner_not_uniformly_unique",
                "uniform_positive_root_count": len(roots),
                "alternative_owner_count": len(alternative_owners),
            }
        alternative = alternative_owners[0]
        alternative_root = roots[alternative]
        if not bool(boundary_projection < alternative_root):
            return False, {
                "physical_first_failure": "candidate_tangent_not_before_alternative_owner",
                "alternative_owner": alternative,
            }

        # Any discriminant straddling zero other than the selected candidate
        # is not silently discarded.  It must be uniformly later than the
        # certified alternative root by its dependency-free possible lower
        # root, or the physical-first typing fails closed.
        ambiguous_later = [
            relative_id
            for relative_id, possible_near_lower in possible_root_lowers.items()
            if relative_id != alternative
            and not bool(alternative_root < possible_near_lower)
        ]
        if ambiguous_later:
            return False, {
                "physical_first_failure": "additional_ambiguous_candidate_may_precede",
                "ambiguous_candidate_count": len(ambiguous_later),
                "ambiguous_candidates_sha256": canonical_digest(ambiguous_later),
            }

        d = interval["candidates"][candidate]["discriminant"]
        if d.dt.contains(0):
            return False, {"physical_first_failure": "candidate_dt_not_strict"}
        if bool(d.dt > 0):
            dt_sign = 1
            hit_t_side = "increasing_t"
        elif bool(d.dt < 0):
            dt_sign = -1
            hit_t_side = "decreasing_t"
        else:
            return False, {"physical_first_failure": "candidate_dt_sign_not_strict"}
        dt_lower = min(abs(d.dt.lower()), abs(d.dt.upper()))
        ds_upper = max(abs(d.ds.lower()), abs(d.ds.upper()))
        if dt_lower == 0:
            return False, {"physical_first_failure": "candidate_dt_not_strict"}
        normalized_slope = ds_upper / dt_lower / 200
        slope_ceiling_ball = normalized_slope.upper().ceil()
        slope_ceiling_fmpz = slope_ceiling_ball.unique_fmpz()
        assert slope_ceiling_fmpz is not None
        normalized_slope_ceiling = int(slope_ceiling_fmpz)
        return True, {
            "candidate_relative_to_miss_source": candidate,
            "miss_side_alternative_owner": alternative,
            "candidate_tangent_time_enclosure": str(boundary_projection),
            "alternative_owner_root_enclosure": str(alternative_root),
            "candidate_is_strictly_first_at_tangency": True,
            "miss_side_owner_uniformly_typed": True,
            "physical_mark": ["grazing-hit", "first-miss-side-owner"],
            "dt_discriminant_strict_sign": dt_sign,
            "candidate_hit_t_side": hit_t_side,
            "graph_velocity_to_hit_minus_miss_current_sign": -dt_sign,
            "signed_current_coefficient_formula": (
                "partial_s_Delta/abs(partial_t_Delta)"
            ),
            "normalized_dt_dv_absolute_slope_integer_upper": normalized_slope_ceiling,
            "physical_dt_ds_absolute_upper": 200 * normalized_slope_ceiling,
            "other_candidate_ledger_sha256": canonical_digest(nonblocking),
        }
    except (AssertionError, KeyError, ValueError, ZeroDivisionError) as exc:
        return False, {
            "physical_first_failure": "interval_geometry_exception",
            "exception_type": type(exc).__name__,
        }


def implicit_root_arc_witness(
    row: dict[str, Any], box: outer.FutureBox, candidate: str,
) -> tuple[bool, dict[str, Any]]:
    """Prove a nonempty transverse zero arc without rectangular bracketing.

    A slanted root normally enters a dyadic rectangle through a horizontal
    edge, so opposite signs on both *vertical* edges for the entire v slab
    are unnecessarily strong.  We use one interval-Newton inclusion on the
    fixed middle parameter slice.  Strict dDelta/dt on the full rectangle
    then makes the entire zero set in the rectangle a (possibly shorter)
    analytic graph arc.  Its actual v-domain is not enlarged to the full
    rectangular slab; using that slab later is only an upper bound.
    """

    tm = (box.t0 + box.t1) / 2
    try:
        interval = outer.second_geometry(
            row,
            outer.Jet2.t_variable(outer.arb_interval(box.t0, box.t1)),
            outer.Jet2.s_variable(outer.arb_interval(box.s0, box.s1)),
            candidate_only=candidate,
        )["candidates"][candidate]["discriminant"]
        derivative = interval.dt
        if derivative.contains(0):
            return False, {"implicit_arc_failure": "dt_discriminant_contains_zero"}
        newton = None
        witness_parameter = None
        witness_kind = None
        # A slanted graph segment may occupy only a small part of the
        # rectangle's v range.  Seventeen exact parameter samples are used
        # only to prove nonemptiness; the derivative enclosure remains the
        # full rectangle enclosure.
        for index in range(17):
            v = box.v0 + (box.v1 - box.v0) * Q(index, 16)
            s = outer.S_LOWER + (outer.S_UPPER - outer.S_LOWER) * v
            point = outer.second_geometry(
                row,
                outer.Jet2.t_variable(outer.arbq(tm)),
                outer.Jet2.s_variable(outer.arbq(s)),
                candidate_only=candidate,
            )["candidates"][candidate]["discriminant"].value
            trial = outer.arbq(tm) - point / derivative
            if (
                bool(trial > outer.arbq(box.t0))
                and bool(trial < outer.arbq(box.t1))
            ):
                newton = trial
                witness_parameter = v
                witness_kind = "fixed_v_t_interval_newton"
                break
        if newton is None:
            # If the graph crosses a horizontal t-edge, it can miss every
            # sampled v slice.  Solve Delta(tm,s)=0 instead.  A strict ds on
            # the full rectangle and an interval-Newton inclusion in the
            # parameter interval certifies a boundary-crossing graph point.
            ds_derivative = interval.ds
            if not ds_derivative.contains(0):
                sm = (box.s0 + box.s1) / 2
                point = outer.second_geometry(
                    row,
                    outer.Jet2.t_variable(outer.arbq(tm)),
                    outer.Jet2.s_variable(outer.arbq(sm)),
                    candidate_only=candidate,
                )["candidates"][candidate]["discriminant"].value
                parameter_newton = outer.arbq(sm) - point / ds_derivative
                if (
                    bool(parameter_newton > outer.arbq(box.s0))
                    and bool(parameter_newton < outer.arbq(box.s1))
                ):
                    newton = parameter_newton
                    witness_parameter = (
                        Q(400) * sm + 1
                    ) / 2
                    witness_kind = "fixed_t_s_interval_newton"
            if newton is None:
                return False, {
                    "implicit_arc_failure": "two_axis_interval_newton_not_interior",
                    "sampled_parameter_count": 17,
                    "ds_discriminant_enclosure": str(ds_derivative),
                }
        physical_ok, physical = physical_first_witness(row, box, candidate)
        if not physical_ok:
            return False, {
                "implicit_arc_failure": "physical_first_typing_failed",
                **physical,
            }
        return True, {
            **physical,
            "root_registry_kind": "nonempty_transverse_implicit_graph_arc",
            "interval_newton_witness_v": str(witness_parameter),
            "interval_newton_enclosure": str(newton),
            "interval_newton_witness_kind": witness_kind,
            "interval_newton_parameter_sample_count_upper": 17,
            "strict_dt_on_full_rectangle": True,
            "actual_root_arc_v_domain_is_not_promoted_to_full_slab": True,
            "full_v_slab_used_only_for_fixed_s_count_and_TV_upper_bounds": True,
        }
    except (AssertionError, KeyError, ValueError, ZeroDivisionError) as exc:
        return False, {
            "implicit_arc_failure": "interval_geometry_exception",
            "exception_type": type(exc).__name__,
        }


def candidate_graph_cover(
    row: dict[str, Any], box: outer.FutureBox,
) -> tuple[bool, list[dict[str, Any]], dict[str, Any]]:
    """Cover every possible owner-change set by strict-dt candidate graphs.

    On a connected regular billiard branch, distinct disjoint target disks
    cannot exchange the first positive root without one root being born or
    dying at a tangency.  Hence after the three prerequisite inequalities
    are strict, the physical future boundary is contained in the union of
    candidate discriminant zero sets.  If each candidate whose enclosure
    meets zero has strict dDelta/dt, those sets are (possibly empty) graphs
    and have zero t-width on every fixed-s slice.  No physical-first label is
    asserted by this fallback.
    """

    t_radius = (box.t1 - box.t0) / 2
    s_radius = (box.s1 - box.s0) / 2
    try:
        centre, interval = outer.geometry_on_box(
            row, box.t0, box.t1, box.s0, box.s1
        )
        for key in ("source_cp", "miss_delta", "miss_root_gap"):
            value = enclosure(centre[key], interval[key], t_radius, s_radius)
            if not bool(value > 0):
                return False, [], {
                    "graph_cover_failure": f"{key}_not_strict"
                }
        graphs = []
        critical = []
        for candidate in sorted(interval["candidates"]):
            centre_d = centre["candidates"][candidate]["discriminant"]
            interval_d = interval["candidates"][candidate]["discriminant"]
            d = enclosure(centre_d, interval_d, t_radius, s_radius)
            if not d.contains(0):
                continue
            if interval_d.dt.contains(0):
                critical.append(candidate)
                continue
            dt_lower = min(
                abs(interval_d.dt.lower()), abs(interval_d.dt.upper())
            )
            ds_upper = max(
                abs(interval_d.ds.lower()), abs(interval_d.ds.upper())
            )
            slope_ball = (ds_upper / dt_lower / 200).upper().ceil()
            slope_fmpz = slope_ball.unique_fmpz()
            assert slope_fmpz is not None
            graphs.append({
                "candidate_relative_to_miss_source": candidate,
                "root_registry_kind": (
                    "possibly_empty_untyped_transverse_candidate_graph_cover"
                ),
                "dt_discriminant_enclosure": str(interval_d.dt),
                "normalized_dt_dv_absolute_slope_integer_upper": int(slope_fmpz),
                "physical_dt_ds_absolute_upper": 200 * int(slope_fmpz),
                "actual_zero_subset_only_not_the_rectangular_cell": True,
                "nonemptiness_not_asserted": True,
                "physical_first_not_asserted": True,
            })
        if critical:
            return False, graphs, {
                "graph_cover_failure": "candidate_zero_with_dt_containing_zero",
                "critical_candidate_count": len(critical),
                "critical_candidates_sha256": canonical_digest(critical),
            }
        return True, graphs, {
            "candidate_zero_graph_count": len(graphs),
            "owner_change_subset_of_candidate_tangency_union": True,
            "no_candidate_zero_implies_topologically_immutable": not graphs,
        }
    except (AssertionError, KeyError, ValueError, ZeroDivisionError) as exc:
        return False, [], {
            "graph_cover_failure": "interval_geometry_exception",
            "exception_type": type(exc).__name__,
        }


def initial_boxes_for_row(row_index: int) -> list[outer.FutureBox]:
    return outer.initial_boxes_for_row(row_index)


def audit_one_row(task: tuple[int, dict[str, Any]]) -> dict[str, Any]:
    row_index, row = task
    pending = initial_boxes_for_row(row_index)
    terminal_counts: Counter[str] = Counter()
    terminal_reason_counts: Counter[str] = Counter()
    terminal_reason_area: Counter[str] = Counter()
    terminal_reason_records: list[dict[str, Any]] = []
    physical_rows: list[dict[str, Any]] = []
    nonphysical_rows: list[dict[str, Any]] = []
    event_map: dict[Q, Counter[str]] = {}
    calls = 0

    while pending:
        box = pending.pop()
        calls += 1
        status, witness = outer.audit_box(row, box)
        if status == "refine_t" and box.t_depth < MAX_T_DEPTH:
            pending.extend(reversed(box.split_t()))
            continue
        if status == "refine_t" and box.v_depth < MAX_V_DEPTH:
            pending.extend(reversed(box.split_v()))
            continue
        if status == "refine_v" and box.v_depth < MAX_V_DEPTH:
            pending.extend(reversed(box.split_v()))
            continue
        if status == "refine_v" and box.t_depth < MAX_T_DEPTH:
            pending.extend(reversed(box.split_t()))
            continue
        if status in {
            "analytic_unresolved", "owner_unresolved",
            "multi_or_tangent_unresolved",
        }:
            if box.t_depth < MAX_T_DEPTH:
                pending.extend(reversed(box.split_t()))
                continue
            if box.v_depth < MAX_V_DEPTH:
                pending.extend(reversed(box.split_v()))
                continue

        base = {
            "row_index": row_index,
            "occurrence_id": row["occurrence_id"],
            "t": [str(box.t0), str(box.t1)],
            "v": [str(box.v0), str(box.v1)],
            "s": [str(box.s0), str(box.s1)],
            "t_depth": box.t_depth,
            "v_depth": box.v_depth,
        }
        if status == "transverse_root_strip":
            candidate = witness["candidate_relative_to_miss_source"]
            ok, typed = physical_first_witness(row, box, candidate)
            record = {
                **base, **witness, **typed,
                "root_registry_kind": "full_slab_bracketed_transverse_graph",
            }
            if ok:
                physical_rows.append(record)
            else:
                if box.t_depth < SELECTIVE_MAX_T_DEPTH:
                    pending.extend(reversed(box.split_t()))
                    continue
                if box.v_depth < SELECTIVE_MAX_V_DEPTH:
                    pending.extend(reversed(box.split_v()))
                    continue
                nonphysical_rows.append(record)
            continue
        if status == "immutable":
            continue

        reason = witness.get("reason", status)
        if reason == "transverse_candidate_not_bracketed_on_full_s_slab":
            candidate = witness.get("candidate_relative_to_miss_source")
            if isinstance(candidate, str):
                # Nonemptiness is not needed to register the *actual* zero
                # subset.  The frozen witness already has strict dDelta/dt
                # on the whole box.  Conditional physical-first typing then
                # proves that the possibly empty set {Delta=0} is one graph
                # and every point on it has the declared physical traces.
                # Half-open (t,v) ownership prevents duplicates at dyadic
                # chart boundaries.  Empty charts contribute no current.
                physical_ok, conditional = physical_first_witness(
                    row, box, candidate
                )
                if physical_ok:
                    physical_rows.append({
                        **base,
                        **witness,
                        **conditional,
                        "root_registry_kind": (
                            "possibly_empty_conditionally_physical_transverse_graph"
                        ),
                        "actual_zero_subset_only_not_the_rectangular_cell": True,
                        "t_interval_ownership": (
                            "[t0,t1), except the final t1=1 endpoint is closed"
                        ),
                        "v_interval_ownership": (
                            "[v0,v1), except the final v1=1 endpoint is closed"
                        ),
                        "nonemptiness_not_asserted": True,
                        "empty_graph_chart_contributes_zero_current": True,
                    })
                    continue
                if box.t_depth < SELECTIVE_MAX_T_DEPTH:
                    pending.extend(reversed(box.split_t()))
                    continue
                if box.v_depth < SELECTIVE_MAX_V_DEPTH:
                    pending.extend(reversed(box.split_v()))
                    continue
                witness = {**witness, **conditional}
                reason = conditional.get("physical_first_failure", reason)
        if box.t_depth < SELECTIVE_MAX_T_DEPTH:
            pending.extend(reversed(box.split_t()))
            continue
        if box.v_depth < SELECTIVE_MAX_V_DEPTH:
            pending.extend(reversed(box.split_v()))
            continue
        covered, graph_rows, graph_summary = candidate_graph_cover(
            row, box
        )
        if covered:
            for graph in graph_rows:
                nonphysical_rows.append({
                    **base,
                    **graph,
                    "t_interval_ownership": (
                        "[t0,t1), except the final t1=1 endpoint is closed"
                    ),
                    "v_interval_ownership": (
                        "[v0,v1), except the final v1=1 endpoint is closed"
                    ),
                    "empty_graph_chart_contributes_zero_current": True,
                })
            continue
        witness = {**witness, **graph_summary}
        reason = graph_summary.get("graph_cover_failure", reason)
        terminal_counts[status] += 1
        terminal_reason_counts[reason] += 1
        terminal_reason_area[reason] += box.area
        terminal_reason_records.append({
            **base,
            "terminal_status": status,
            "terminal_reason": reason,
            "witness_digest": canonical_digest(witness),
        })
        for endpoint, sign in ((box.v0, 1), (box.v1, -1)):
            event = event_map.setdefault(endpoint, Counter())
            event["terminal:count"] += sign
            event["terminal:width"] += sign * (box.t1 - box.t0)
            event[f"reason:{reason}:count"] += sign
            event[f"reason:{reason}:width"] += sign * (box.t1 - box.t0)

    terminal_reason_records.sort(key=canonical_json)
    physical_rows.sort(key=canonical_json)
    nonphysical_rows.sort(key=canonical_json)
    nonempty_physical_rows = [
        record for record in physical_rows
        if record.get("nonemptiness_not_asserted") is not True
    ]
    physical_dt_sign_counts = Counter(
        str(record["dt_discriminant_strict_sign"])
        for record in physical_rows
    )
    physical_event_map: dict[Q, Counter[str]] = {}
    for record in physical_rows:
        v0, v1 = Q(record["v"][0]), Q(record["v"][1])
        slope = record["normalized_dt_dv_absolute_slope_integer_upper"]
        for endpoint, sign in ((v0, 1), (v1, -1)):
            event = physical_event_map.setdefault(endpoint, Counter())
            event["count"] += sign
            event["normalized_slope_sum"] += sign * slope
    graph_event_map: dict[Q, Counter[str]] = {}
    for record in physical_rows + nonphysical_rows:
        v0, v1 = Q(record["v"][0]), Q(record["v"][1])
        slope = record["normalized_dt_dv_absolute_slope_integer_upper"]
        for endpoint, sign in ((v0, 1), (v1, -1)):
            event = graph_event_map.setdefault(endpoint, Counter())
            event["count"] += sign
            event["normalized_slope_sum"] += sign * slope
    nonempty_physical_event_map: dict[Q, Counter[str]] = {}
    for record in nonempty_physical_rows:
        v0, v1 = Q(record["v"][0]), Q(record["v"][1])
        for endpoint, sign in ((v0, 1), (v1, -1)):
            nonempty_physical_event_map.setdefault(endpoint, Counter())[
                "count"
            ] += sign

    return {
        "row_index": row_index,
        "audit_call_count": calls,
        "terminal_counts": dict(terminal_counts),
        "terminal_reason_counts": dict(terminal_reason_counts),
        "terminal_reason_areas": {
            key: str(value) for key, value in terminal_reason_area.items()
        },
        "terminal_reason_records_sha256": canonical_digest(terminal_reason_records),
        "conditionally_physical_first_graph_chart_count": len(physical_rows),
        "conditionally_physical_first_dt_sign_counts": dict(
            sorted(physical_dt_sign_counts.items())
        ),
        "nonempty_physical_first_root_arc_count": len(nonempty_physical_rows),
        "conditionally_physical_first_graph_records_sha256": canonical_digest(
            physical_rows
        ),
        "untyped_candidate_graph_chart_count": len(nonphysical_rows),
        "untyped_candidate_graph_records_sha256": canonical_digest(
            nonphysical_rows
        ),
        "untyped_graph_failure_counts": dict(Counter(
            record.get(
                "physical_first_failure",
                "untyped_candidate_graph_cover",
            )
            for record in nonphysical_rows
        )),
        "terminal_event_map": {
            str(key): {
                field: (str(amount) if field.endswith(":width") else int(amount))
                for field, amount in value.items()
            }
            for key, value in sorted(event_map.items())
        },
        "physical_event_map": {
            str(key): dict(value)
            for key, value in sorted(physical_event_map.items())
        },
        "candidate_graph_event_map": {
            str(key): dict(value)
            for key, value in sorted(graph_event_map.items())
        },
        "nonempty_physical_event_map": {
            str(key): dict(value)
            for key, value in sorted(nonempty_physical_event_map.items())
        },
    }


def sweep_maxima(
    events: dict[Q, Counter[str]],
) -> tuple[dict[str, Q | int], dict[str, Q | int]]:
    active: Counter[str] = Counter()
    maxima: dict[str, Q | int] = {}
    endpoints = sorted(events)
    if not endpoints:
        return maxima, {}
    for index, endpoint in enumerate(endpoints[:-1]):
        active.update(events[endpoint])
        if endpoints[index + 1] == endpoint:
            continue
        for key, value in active.items():
            maxima[key] = max(maxima.get(key, 0), value)
    # The parameter window is closed.  The active ledger immediately before
    # the final closing events is exactly the value at v=1, because no
    # positive-width half-open chart can start at that terminal endpoint.
    # Include and freeze it explicitly rather than relying on the preceding
    # open interval to have the same value implicitly.
    closed_final_endpoint = {
        key: value for key, value in active.items() if value
    }
    for key, value in closed_final_endpoint.items():
        maxima[key] = max(maxima.get(key, 0), value)
    active.update(events[endpoints[-1]])
    assert not any(active.values())
    return maxima, closed_final_endpoint


def build_frontier(rows: list[dict[str, Any]]) -> dict[str, Any]:
    workers = min(int(os.environ.get("CM2_WORKERS", "32")), os.cpu_count() or 1, 64)
    assert 1 <= workers <= 64
    with multiprocessing.get_context("fork").Pool(workers) as pool:
        partials = list(pool.imap_unordered(
            audit_one_row, list(enumerate(rows)), chunksize=1
        ))
    partials.sort(key=lambda item: item["row_index"])
    assert [item["row_index"] for item in partials] == list(range(64))

    terminal_counts: Counter[str] = Counter()
    terminal_reason_counts: Counter[str] = Counter()
    terminal_reason_areas: Counter[str] = Counter()
    untyped_failures: Counter[str] = Counter()
    physical_dt_sign_counts: Counter[str] = Counter()
    terminal_events: dict[Q, Counter[str]] = {}
    physical_events: dict[Q, Counter[str]] = {}
    graph_events: dict[Q, Counter[str]] = {}
    nonempty_physical_events: dict[Q, Counter[str]] = {}
    for part in partials:
        terminal_counts.update(part["terminal_counts"])
        terminal_reason_counts.update(part["terminal_reason_counts"])
        terminal_reason_areas.update({
            key: Q(value) for key, value in part["terminal_reason_areas"].items()
        })
        untyped_failures.update(part["untyped_graph_failure_counts"])
        physical_dt_sign_counts.update(
            part["conditionally_physical_first_dt_sign_counts"]
        )
        for endpoint_text, event in part["terminal_event_map"].items():
            converted = {
                key: (Q(value) if key.endswith(":width") else int(value))
                for key, value in event.items()
            }
            terminal_events.setdefault(Q(endpoint_text), Counter()).update(converted)
        for endpoint_text, event in part["physical_event_map"].items():
            physical_events.setdefault(Q(endpoint_text), Counter()).update(event)
        for endpoint_text, event in part["candidate_graph_event_map"].items():
            graph_events.setdefault(Q(endpoint_text), Counter()).update(event)
        for endpoint_text, event in part["nonempty_physical_event_map"].items():
            nonempty_physical_events.setdefault(
                Q(endpoint_text), Counter()
            ).update(event)

    terminal_maxima, terminal_v1 = sweep_maxima(terminal_events)
    physical_maxima, physical_v1 = sweep_maxima(physical_events)
    graph_maxima, graph_v1 = sweep_maxima(graph_events)
    nonempty_physical_maxima, nonempty_physical_v1 = sweep_maxima(
        nonempty_physical_events
    )
    reason_slice_widths = {
        key.split(":")[1]: str(value)
        for key, value in terminal_maxima.items()
        if key.startswith("reason:") and key.endswith(":width")
    }
    max_terminal_count = int(terminal_maxima.get("terminal:count", 0))
    max_terminal_width = Q(terminal_maxima.get("terminal:width", 0))
    max_physical_roots = int(physical_maxima.get("count", 0))
    max_normalized_slope_sum = int(
        physical_maxima.get("normalized_slope_sum", 0)
    )
    max_candidate_graphs = int(graph_maxima.get("count", 0))
    max_candidate_slope_sum = int(
        graph_maxima.get("normalized_slope_sum", 0)
    )
    # dm/dt <=126/5.  The parameter derivative is
    # |dt/ds|=200|dt/dv|, and the two physical traces give the factor 2.
    physical_current_tv_upper = (
        Q(2) * Q(126, 5) * 200 * max_normalized_slope_sum
    )
    public_partials = []
    for part in partials:
        public = {
            key: value for key, value in part.items()
            if key not in {
                "terminal_event_map", "physical_event_map",
                "candidate_graph_event_map", "nonempty_physical_event_map",
            }
        }
        public["terminal_event_map_sha256"] = canonical_digest(
            part["terminal_event_map"]
        )
        public["physical_event_map_sha256"] = canonical_digest(
            part["physical_event_map"]
        )
        public["candidate_graph_event_map_sha256"] = canonical_digest(
            part["candidate_graph_event_map"]
        )
        public["nonempty_physical_event_map_sha256"] = canonical_digest(
            part["nonempty_physical_event_map"]
        )
        public_partials.append(public)
    return {
        "frozen_resolution": {
            "maximum_additional_t_depth": MAX_T_DEPTH,
            "maximum_additional_parameter_depth": MAX_V_DEPTH,
            "resolution_is_reason_audit_not_complete_root_isolation": True,
            "selective_terminal_t_depth": SELECTIVE_MAX_T_DEPTH,
            "selective_terminal_parameter_depth": SELECTIVE_MAX_V_DEPTH,
        },
        "terminal_status_counts": dict(sorted(terminal_counts.items())),
        "terminal_reason_counts": dict(sorted(terminal_reason_counts.items())),
        "terminal_reason_nonphysical_parameter_areas": {
            key: str(value) for key, value in sorted(terminal_reason_areas.items())
        },
        "uniform_fixed_s_terminal_reason_t_width_outers": dict(
            sorted(reason_slice_widths.items())
        ),
        "maximum_terminal_boxes_on_one_fixed_s_slice": max_terminal_count,
        "uniform_fixed_s_terminal_positive_t_width_outer": str(
            max_terminal_width
        ),
        "uniform_fixed_s_future_candidate_zero_intercept_Z": (
            max_terminal_width == 0
        ),
        "conditionally_physical_first_graph_chart_count": sum(
            part["conditionally_physical_first_graph_chart_count"]
            for part in partials
        ),
        "conditionally_physical_first_dt_sign_counts": dict(
            sorted(physical_dt_sign_counts.items())
        ),
        "nonempty_physical_first_root_arc_count": sum(
            part["nonempty_physical_first_root_arc_count"]
            for part in partials
        ),
        "untyped_candidate_graph_chart_count": sum(
            part["untyped_candidate_graph_chart_count"] for part in partials
        ),
        "untyped_graph_failure_counts": dict(sorted(untyped_failures.items())),
        "maximum_conditionally_physical_first_graph_charts_on_one_fixed_s_slice": (
            max_physical_roots
        ),
        "maximum_nonempty_physical_first_root_arcs_on_one_fixed_s_slice": int(
            nonempty_physical_maxima.get("count", 0)
        ),
        "maximum_normalized_absolute_root_slope_sum_on_one_fixed_s_slice": (
            max_normalized_slope_sum
        ),
        "maximum_candidate_graph_charts_on_one_fixed_s_slice": (
            max_candidate_graphs
        ),
        "maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice": (
            max_candidate_slope_sum
        ),
        "uniform_fixed_s_actual_candidate_zero_set_Leb_Z_linear_coefficient": str(
            2 * max_candidate_graphs
        ),
        "uniform_fixed_s_actual_candidate_zero_set_row_law_Z_linear_coefficient": str(
            Q(252, 5) * max_candidate_graphs
        ),
        "partial_genuine_physical_marked_current_TV_upper": str(
            physical_current_tv_upper
        ),
        "partial_current_definition": (
            "sum_i (partial_s_Delta_i/abs(partial_t_Delta_i)) "
            "rho_e(t_i,s) "
            "[delta_grazing_hit_i-delta_first_miss_side_owner_i]"
        ),
        "graph_velocity_current_orientation_identity": (
            "partial_s_Delta/abs(partial_t_Delta)="
            "-sign(partial_t_Delta)*dt_graph/ds"
        ),
        "closed_final_v_endpoint_explicitly_included_in_all_sweeps": True,
        "closed_v1_endpoint_sweep_values": {
            "terminal": {
                key: (str(value) if isinstance(value, Q) else value)
                for key, value in sorted(terminal_v1.items())
            },
            "conditionally_physical": dict(sorted(physical_v1.items())),
            "candidate_graph": dict(sorted(graph_v1.items())),
            "nonempty_physical": dict(sorted(nonempty_physical_v1.items())),
        },
        "partial_current_is_on_actual_zero_subsets_of_conditionally_physical_first_charts": True,
        "possibly_empty_chart_contributes_zero_current": True,
        "half_open_t_v_chart_ownership_is_unique": True,
        "partial_current_is_not_complete_future_current": True,
        "v_is_not_probability_coordinate": True,
        "two_dimensional_areas_are_nonphysical_parameter_bookkeeping": True,
        "artificial_rectangular_t_boundary_is_not_future_physical_current": True,
        "ordered_row_summary_ledger": public_partials,
        "ordered_row_summary_ledger_sha256": canonical_digest(public_partials),
        "total_audit_call_count": sum(part["audit_call_count"] for part in partials),
    }


def load_dependencies() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    frozen = json.loads(OUTER_MANIFEST.read_text(encoding="utf-8"))
    assert frozen["verdict"]["finite_s_future_candidate_outer_atlas"] == "CERTIFIED"
    assert frozen["verdict"]["physical_future_face_or_current"] == "NOT_CERTIFIED"
    rows, provenance = outer.load_dependencies()
    return rows, {
        "frozen_outer_manifest_sha256": file_sha256(OUTER_MANIFEST),
        "frozen_outer_certificate_sha256": file_sha256(Path(outer.__file__).resolve()),
        "maximal_row_registry_sha256": provenance["maximal_row_registry_sha256"],
    }


def build_manifest() -> dict[str, Any]:
    rows, provenance = load_dependencies()
    frontier = build_frontier(rows)
    if frontier["uniform_fixed_s_future_candidate_zero_intercept_Z"]:
        first_blocker = (
            "assemble root-isolated side-owner components across the half-open "
            "candidate graph charts; no terminal positive-width interval remains"
        )
    else:
        first_blocker = (
            "eliminate or analytically dominate every reason-resolved terminal "
            "fixed-s positive-width interval"
        )
    if frontier["untyped_candidate_graph_chart_count"]:
        second_blocker = (
            "type every remaining untyped/critical candidate graph chart by "
            "physical-first owner and complete the marked current"
        )
    else:
        second_blocker = (
            "prove global owner-component assembly and promote the conservative "
            "chartwise marked current to a complete future current"
        )
    result = {
        "schema": "cm2.gate3.physical-first-unresolved-frontier.v1",
        "provenance": provenance,
        "reason_resolved_frontier": frontier,
        "scope_limits": {
            "terminal_unresolved_reason_decomposition": True,
            "certified_nonempty_physical_first_root_arc_subfamily": (
                frontier["nonempty_physical_first_root_arc_count"] > 0
            ),
            "conditionally_physical_first_graph_chart_family": (
                frontier["conditionally_physical_first_graph_chart_count"] > 0
            ),
            "partial_genuine_marked_current_on_certified_subfamily": (
                frontier["conditionally_physical_first_graph_chart_count"] > 0
            ),
            "all_candidate_graph_charts_typed_physical_first": (
                frontier["untyped_candidate_graph_chart_count"] == 0
            ),
            "zero_intercept_complete_future_candidate_boundary_Z": (
                frontier["uniform_fixed_s_future_candidate_zero_intercept_Z"]
            ),
            "complete_root_isolated_owner_atlas": False,
            "complete_physical_future_current": False,
            "strong_source_invariance": False,
            "operator_norm_depth_two_DQ": False,
            "fixed_time_branch_record_MT_DQ": False,
            "physical_FACE_2CUT": False,
            "physical_FACE_TIME": False,
            "gate3_certified": False,
        },
        "exact_remaining_blockers": [
            first_blocker,
            second_blocker,
            "prove strong-space invariance for immutable and root-restricted sources",
            "prove operator-norm one-step/depth-two DQ and dynamic-test convergence",
            "close branch-record MT_DQ, FACE_2CUT, and FACE_TIME",
        ],
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


if __name__ == "__main__":
    print(json.dumps(build_manifest(), sort_keys=True, indent=2))
