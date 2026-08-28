#!/usr/bin/env python3
"""Fail-closed owner-ordering engine on the Round112 endpoint root sheets.

This append-only spike deliberately distinguishes the two analytic sheets

    HIT:    Delta_3 - R_3^2 c_3^2 = 0,
    BYPASS: Delta_3 + R_3^2 b_3^2 = 0.

For a dyadic parameter rectangle it first encloses the unique implicit root
``t=t(c0,z3)`` by strict signs on two constant-t faces.  It then replays the
complete translated candidate tables for all three collision legs.  Every
candidate must be a strict miss, a strict behind intersection, or a strict
future near root, and the selected owner must be strictly earlier than every
other future root.  Transparent-wall event order, collision charts, and the
flight cap are checked on the same closed rectangle.  Indeterminate boxes are
bisected and retained as residuals at the requested depth; no physical collar
or whole-sheet word is inferred from a residual box.

The exploratory spike closed every sheet and is retained as the implementation
engine behind the small Round113 certificate entry point.  Natural grazing
edges remain separate singular strata and never inherit a regular word.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as component
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval, normal
from cm2_round79_tangency_intersection_generator import digest, strict_sign


HERE = Path(__file__).resolve().parent
ROUND112_JSON = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
ROUND112_MANIFEST = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-manifest-2026-07-23.sha256"
SCHEMA = "cm2.round113.rank3-endpoint-sheet-owner-ordering.v1"
PRECISION_BITS = 512
ROOT_FACE_BISECTIONS = 96
DEFAULT_MAX_DEPTH = 4
EVIDENCE_PADDING = Q(1, 10**6)
ROOT_T_FACE_OUTWARD_PADDING = Q(1, 10**9)
PINS = {
    ROUND112_JSON.name: "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5",
    ROUND112_MANIFEST.name: "2bacd33db96ae0aa6ea0857f0326243067c1abc87cfe58fd36356b0c417b7290",
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate3_candidate_first_hit_cert.py": "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate34_round26_q1_time2_frontier_cert.py": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "cm2_gate5_return_word_three_norm_frontier_cert.py": "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    "cm2-round79-time3-carrier-seeds-2026-07-21.json": "00a8af0ed6e59789dbaa746f2dff51479e6004f9d3d855a9ee4a1a6283f42755",
    "cm2-round79-tangency-intersections-2026-07-21.json": "c7a3f0c5c680154d4ef9870d8a5891b283af2fe2ce2ede92c868db433e94177e",
    "cm2-round87-rank3-port-event-continuation-2026-07-22.json": "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    "cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json": "915f7c18d896d92116ab3f4346a5853c09fef2d3226a1f5429a7c19bca948ee3",
    "cm2-round98-rank3-full-candidate-generator-audit-2026-07-22.json": "219e9f0d4c0935e41482fb05f675a5dc21f76eebdaf1474fd43dfa41487b3e4b",
    "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json": "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json": "097849bf3da9d34a83ce9693ca68093ed2de7460cc51dcb26ce484c589f278d6",
    "cm2-round107-rank3-adjacent-smooth-cell-atlas-2026-07-22.json": "bb6aeaa821174a1e1994eff2eb10046811b66dd7cf41c4e2d1c898b74d9dea74",
    "cm2-round108-rank3-official-word-crosswalk-2026-07-22.json": "96bf22d97f517d53cb360c4aae64a2d5a5a0bbfb7125610dc69b519629bd78ea",
}
TARGET_PATTERN_DIGEST = {
    f"{source}:{chart}": digest(list(time2.relative_candidate_ids(source, chart)))
    for source in ("G", "W") for chart in ("E", "N", "W", "S")
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def strict_load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=reject_nonfinite,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"non-object JSON dependency: {path.name}")
    return value


def validate_pins() -> None:
    for name, expected in PINS.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or sha256(path) != expected:
            raise RuntimeError(f"direct dependency byte pin mismatch: {name}")


def qstr(value: Q) -> str:
    return str(value)


def arb_bounds(value: arb) -> list[str]:
    padding = aq(EVIDENCE_PADDING)
    return [str(value.lower() - padding), str(value.upper() + padding)]


def parse_box(payload: dict[str, list[str]], coordinate: str) -> tuple[Q, Q, Q, Q, Q, Q]:
    t0, t1 = map(Q, payload["t"])
    c00, c01 = map(Q, payload["c0"])
    z0, z1 = map(Q, payload[coordinate])
    return t0, t1, c00, c01, z0, z1


def strict_chart(normal_x: Jet, normal_y: Jet) -> tuple[str, arb, arb] | None:
    nx, ny = normal_x.value, normal_y.value
    ax, ay = abs(nx), abs(ny)
    if bool(ax > ay):
        if bool(nx > 0):
            return "E", nx, ax - ay
        if bool(nx < 0):
            return "W", -nx, ax - ay
    if bool(ay > ax):
        if bool(ny > 0):
            return "N", ny, ay - ax
        if bool(ny < 0):
            return "S", -ny, ay - ax
    return None


def path_geometry(
    source: Any,
    branch: tuple[int, str, str, int],
    source_sign: int,
    sheet_kind: str,
    t0: Q,
    t1: Q,
    c00: Q,
    c01: Q,
    z0: Q,
    z1: Q,
) -> dict[str, Any]:
    """Three selected-collision states, retaining all three derivatives."""
    t = Jet.variable(interval(t0, t1), 0)
    c0 = Jet.variable(interval(c00, c01), 1)
    z3 = Jet.variable(interval(z0, z1), 2)
    zero = Jet(arb(0))
    source_nx, source_ny = normal(source.chart_id.split(":")[1], t)
    source_p = source_sign * (arb(1) - c0 * c0).sqrt()
    u0x = c0 * source_nx - source_p * source_ny
    u0y = c0 * source_ny + source_p * source_nx
    source_x, source_y = center(f"{source.source}[0,0]", zero)
    q0x = source_x + aq(round112.radius(source.source)) * source_nx
    q0y = source_y + aq(round112.radius(source.source)) * source_ny

    first_x, first_y = center(source.target_id, zero)
    first = round112.collision_diagnostic(
        q0x, q0y, u0x, u0y, first_x, first_y,
        round112.radius(source.target_id),
    )
    c1_square = arb(1) - first["momentum"] * first["momentum"]
    c1 = c1_square.sqrt()
    u1x = c1 * first["normal_x"] - first["momentum"] * first["normal_y"]
    u1y = c1 * first["normal_y"] + first["momentum"] * first["normal_x"]

    second_x, second_y = center(branch[1], zero)
    second = round112.collision_diagnostic(
        first["hit_x"], first["hit_y"], u1x, u1y,
        second_x, second_y, round112.radius(branch[1]),
    )
    c2_square = arb(1) - second["momentum"] * second["momentum"]
    c2 = c2_square.sqrt()
    u2x = c2 * second["normal_x"] - second["momentum"] * second["normal_y"]
    u2y = c2 * second["normal_y"] + second["momentum"] * second["normal_x"]

    third_x, third_y = center(branch[2], zero)
    dx, dy = third_x - second["hit_x"], third_y - second["hit_y"]
    ell3 = u2x * dx + u2y * dy
    transverse3 = -u2y * dx + u2x * dy
    r3 = aq(round112.radius(branch[2]))
    delta3 = r3 * r3 - transverse3 * transverse3
    square_term = r3 * r3 * z3 * z3
    equation = delta3 - square_term if sheet_kind == "HIT" else delta3 + square_term
    return {
        "source_normal": (source_nx, source_ny),
        "states": (
            (q0x, q0y, u0x, u0y),
            (first["hit_x"], first["hit_y"], u1x, u1y),
            (second["hit_x"], second["hit_y"], u2x, u2y),
        ),
        "selected": (first, second),
        "selected_third_ell": ell3,
        "selected_third_transverse": transverse3,
        "selected_third_root": ell3 - r3 * z3,
        "selected_third_radical": r3 * z3,
        "z3": z3,
        "equation": equation,
    }


def equation_value(
    source: Any, branch: tuple[int, str, str, int], source_sign: int,
    sheet_kind: str, t: Q, c00: Q, c01: Q, z0: Q, z1: Q,
) -> arb:
    return path_geometry(
        source, branch, source_sign, sheet_kind,
        t, t, c00, c01, z0, z1,
    )["equation"].value


def implicit_root_enclosure(
    source: Any, branch: tuple[int, str, str, int], source_sign: int,
    sheet_kind: str, global_t0: Q, global_t1: Q,
    c00: Q, c01: Q, z0: Q, z1: Q,
) -> tuple[Q, Q, int, int]:
    """Enclose every root over one parameter rectangle by strict face signs."""
    lower_sign = strict_sign(equation_value(
        source, branch, source_sign, sheet_kind, global_t0, c00, c01, z0, z1,
    ))
    upper_sign = strict_sign(equation_value(
        source, branch, source_sign, sheet_kind, global_t1, c00, c01, z0, z1,
    ))
    if lower_sign * upper_sign != -1:
        raise RuntimeError("root_global_face_sign")

    # Largest strict lower-sign face.
    good, bad = global_t0, global_t1
    for _ in range(ROOT_FACE_BISECTIONS):
        middle = (good + bad) / 2
        sign = strict_sign(equation_value(
            source, branch, source_sign, sheet_kind, middle, c00, c01, z0, z1,
        ))
        if sign == lower_sign:
            good = middle
        else:
            bad = middle
    root_t0 = good - ROOT_T_FACE_OUTWARD_PADDING

    # Smallest strict upper-sign face.
    bad, good = global_t0, global_t1
    for _ in range(ROOT_FACE_BISECTIONS):
        middle = (bad + good) / 2
        sign = strict_sign(equation_value(
            source, branch, source_sign, sheet_kind, middle, c00, c01, z0, z1,
        ))
        if sign == upper_sign:
            good = middle
        else:
            bad = middle
    root_t1 = good + ROOT_T_FACE_OUTWARD_PADDING
    actual_lower_sign = strict_sign(equation_value(
        source, branch, source_sign, sheet_kind, root_t0, c00, c01, z0, z1,
    ))
    actual_upper_sign = strict_sign(equation_value(
        source, branch, source_sign, sheet_kind, root_t1, c00, c01, z0, z1,
    ))
    if (
        root_t0 < global_t0 or root_t1 > global_t1 or root_t0 >= root_t1
        or actual_lower_sign != lower_sign or actual_upper_sign != upper_sign
    ):
        raise RuntimeError("root_enclosure_order")
    return root_t0, root_t1, actual_lower_sign, actual_upper_sign


def candidate_geometry(state: tuple[Jet, Jet, Jet, Jet], candidate_id: str) -> dict[str, Any]:
    qx, qy, ux, uy = state
    zero = Jet(arb(0))
    ax, ay = center(candidate_id, zero)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = aq(round112.radius(candidate_id))
    discriminant = radius * radius - transverse * transverse
    if bool(discriminant.value < 0):
        return {
            "candidate_id": candidate_id,
            "classification": "STRICT_WHOLE_LINE_MISS",
            "discriminant": discriminant,
        }
    if not bool(discriminant.value > 0):
        return {
            "candidate_id": candidate_id,
            "classification": "UNRESOLVED_DISCRIMINANT",
            "discriminant": discriminant,
        }
    radical = discriminant.sqrt()
    near, far = ell - radical, ell + radical
    if bool(far.value < 0):
        return {
            "candidate_id": candidate_id,
            "classification": "STRICT_INTERSECTION_BEHIND",
            "discriminant": discriminant,
            "far": far,
        }
    if not bool(near.value > 0):
        return {
            "candidate_id": candidate_id,
            "classification": "UNRESOLVED_ROOT_SIGN",
            "discriminant": discriminant,
            "near": near,
        }
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    return {
        "candidate_id": candidate_id,
        "classification": "STRICT_FUTURE_NEAR_ROOT",
        "discriminant": discriminant,
        "near": near,
        "radical": radical,
        "transverse": transverse,
        "normal_x": normal_x,
        "normal_y": normal_y,
    }


def selected_third_geometry(
    geometry: dict[str, Any], candidate_id: str, sheet_kind: str,
) -> dict[str, Any]:
    state = geometry["states"][2]
    _qx, _qy, ux, uy = state
    radius = aq(round112.radius(candidate_id))
    transverse = geometry["selected_third_transverse"]
    radical = geometry["selected_third_radical"]
    near = geometry["selected_third_root"]
    if sheet_kind == "BYPASS":
        return {
            "candidate_id": candidate_id,
            "classification": "BYPASS_INTERIOR_MISS__TANGENT_BOUNDARY",
            "tangent_boundary_flight": geometry["selected_third_ell"],
        }
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    return {
        "candidate_id": candidate_id,
        "classification": "REGULAR_INTERIOR_FUTURE_HIT__c3_ZERO_TANGENCY_BOUNDARY",
        "near": near,
        "radical": radical,
        "transverse": transverse,
        "normal_x": normal_x,
        "normal_y": normal_y,
    }


def wall_record(
    state: tuple[Jet, Jet, Jet, Jet], root: Jet,
) -> tuple[tuple[str, ...], list[dict[str, Any]]]:
    qx, qy, ux, uy = state
    hx, hy = qx + root * ux, qy + root * uy
    x_events, reason = component.ordered_axis_events(qx.value, hx.value, "X")
    if x_events is None:
        raise RuntimeError(f"clean_wall:{reason}")
    y_events, reason = component.ordered_axis_events(qy.value, hy.value, "Y")
    if y_events is None:
        raise RuntimeError(f"clean_wall:{reason}")
    events = x_events + y_events
    crossings, reason = component.strict_event_order(events)
    if crossings is None:
        raise RuntimeError(f"clean_wall:{reason}")
    evidence = [
        {"token": token, "wall": wall, "alpha_enclosure": arb_bounds(alpha)}
        for alpha, token, wall in events
    ]
    return crossings, evidence


def leg_audit(
    state: tuple[Jet, Jet, Jet, Jet], current_target: str, chart: str,
    selected_target: str,
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
    selected_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidates = tuple(time2.translated_candidate_ids(current_target, chart))
    if len(candidates) != len(set(candidates)) or selected_target not in candidates:
        raise RuntimeError("candidate_universe")
    rows: list[dict[str, Any]] = []
    for candidate_id in candidates:
        row = (
            selected_override
            if candidate_id == selected_target and selected_override is not None
            else candidate_geometry(state, candidate_id)
        )
        rows.append(row)
    unresolved = [row for row in rows if row["classification"].startswith("UNRESOLVED")]
    if unresolved:
        raise RuntimeError("candidate:" + ",".join(
            f"{row['candidate_id']}:{row['classification']}" for row in unresolved
        ))
    future_kinds = {
        "STRICT_FUTURE_NEAR_ROOT",
        "REGULAR_INTERIOR_FUTURE_HIT__c3_ZERO_TANGENCY_BOUNDARY",
    }
    future = [row for row in rows if row["classification"] in future_kinds]
    selected = next(row for row in rows if row["candidate_id"] == selected_target)
    if selected["classification"] not in future_kinds:
        raise RuntimeError("selected_not_future")
    selected_root = selected["near"]
    if not bool(selected_root.value > 0) or not bool(selected_root.value < aq(Q(3))):
        raise RuntimeError("selected_flight_cap")
    gaps: list[dict[str, Any]] = []
    for other in future:
        if other["candidate_id"] == selected_target:
            continue
        gap = other["near"] - selected_root
        if strict_sign(gap.value) != 1:
            raise RuntimeError(f"owner_gap:{other['candidate_id']}")
        gaps.append({
            "competitor_id": other["candidate_id"],
            "competitor_minus_selected_near_root": arb_bounds(gap.value),
        })
    selected_chart = strict_chart(selected["normal_x"], selected["normal_y"])
    if selected_chart is None:
        raise RuntimeError("selected_collision_chart_seam")
    crossings, wall_evidence = wall_record(state, selected_root)
    official_chart = f"{current_target[0]}:{chart}"
    relative_target = component.relative_target(current_target, selected_target)
    official_key = component.word_key(
        official_chart, relative_target, crossings, pair_index, pattern_index,
    )
    histogram = Counter(row["classification"] for row in rows)
    return {
        "candidate_count": len(candidates),
        "candidate_ids_sha256": digest(list(candidates)),
        "candidate_table_source_digest": TARGET_PATTERN_DIGEST[f"{current_target[0]}:{chart}"],
        "selected_owner_id": selected_target,
        "selected_root_enclosure": arb_bounds(selected_root.value),
        "selected_target_regular_interior_status": "STRICT_FUTURE_NEAR_ROOT",
        "selected_target_natural_boundary_status": (
            "THIRD_GRAZING_TANGENCY" if selected["classification"].startswith("REGULAR_INTERIOR_")
            else "TRANSVERSE_COLLISION_ON_THIRD_GRAZING_BOUNDARY_NOT_APPLICABLE"
        ),
        "selected_collision_chart": selected_chart[0],
        "selected_collision_chart_component_margin": arb_bounds(selected_chart[1]),
        "selected_collision_chart_dominance_margin": arb_bounds(selected_chart[2]),
        "classification_histogram": dict(sorted(histogram.items())),
        "strict_future_competitor_gap_count": len(gaps),
        "minimum_owner_gap_enclosure": min(
            (row["competitor_minus_selected_near_root"] for row in gaps),
            key=lambda pair: Q(pair[0].split(" ")[0].lstrip("[")),
            default=None,
        ),
        "ordered_clean_wall_record": list(crossings),
        "clean_wall_event_evidence": wall_evidence,
        "no_wall_endpoint_or_corner_tie_on_closed_cell": True,
        "official_relative_target_id": relative_target,
        "official_word_key": official_key,
    }


def bypass_third_audit(
    state: tuple[Jet, Jet, Jet, Jet], current_target: str, chart: str,
    designated_target: str, designated: dict[str, Any],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    candidates = tuple(time2.translated_candidate_ids(current_target, chart))
    if len(candidates) != len(set(candidates)) or designated_target not in candidates:
        raise RuntimeError("candidate_universe")
    rows = [
        designated if candidate_id == designated_target else candidate_geometry(state, candidate_id)
        for candidate_id in candidates
    ]
    unresolved = [row for row in rows if row["classification"].startswith("UNRESOLVED")]
    if unresolved:
        raise RuntimeError("candidate:" + ",".join(
            f"{row['candidate_id']}:{row['classification']}" for row in unresolved
        ))
    future = [row for row in rows if row["classification"] == "STRICT_FUTURE_NEAR_ROOT"]
    winners = [
        row for row in future
        if all(
            row is other or bool(row["near"].value < other["near"].value)
            for other in future
        )
    ]
    if len(winners) != 1:
        raise RuntimeError("bypass_unique_owner")
    winner = winners[0]
    tangent_gap = designated["tangent_boundary_flight"] - winner["near"]
    tangent_gap_sign = strict_sign(tangent_gap.value)
    if tangent_gap_sign == 0:
        raise RuntimeError("bypass_winner_vs_designated_tangent_boundary_tie")
    if not bool(winner["near"].value > 0) or not bool(winner["near"].value < aq(Q(3))):
        raise RuntimeError("selected_flight_cap")
    winner_chart = strict_chart(winner["normal_x"], winner["normal_y"])
    if winner_chart is None:
        raise RuntimeError("selected_collision_chart_seam")
    crossings, wall_evidence = wall_record(state, winner["near"])
    official_chart = f"{current_target[0]}:{chart}"
    relative_target = component.relative_target(current_target, winner["candidate_id"])
    official_key = component.word_key(
        official_chart, relative_target, crossings, pair_index, pattern_index,
    )
    gaps: list[Jet] = []
    for other in future:
        if other is winner:
            continue
        gap = other["near"] - winner["near"]
        if strict_sign(gap.value) != 1:
            raise RuntimeError(f"owner_gap:{other['candidate_id']}")
        gaps.append(gap)
    histogram = Counter(row["classification"] for row in rows)
    return {
        "candidate_count": len(candidates),
        "candidate_ids_sha256": digest(list(candidates)),
        "candidate_table_source_digest": TARGET_PATTERN_DIGEST[f"{current_target[0]}:{chart}"],
        "designated_target_id": designated_target,
        "designated_target_status": designated["classification"],
        "actual_selected_owner_id": winner["candidate_id"],
        "actual_selected_root_enclosure": arb_bounds(winner["near"].value),
        "designated_tangent_boundary_minus_bypass_winner_sign": tangent_gap_sign,
        "designated_tangent_boundary_minus_bypass_winner_enclosure": arb_bounds(tangent_gap.value),
        "b3_zero_designated_tangency_owned_by_trace_not_bypass_stratum": True,
        "selected_collision_chart": winner_chart[0],
        "selected_collision_chart_component_margin": arb_bounds(winner_chart[1]),
        "selected_collision_chart_dominance_margin": arb_bounds(winner_chart[2]),
        "classification_histogram": dict(sorted(histogram.items())),
        "strict_future_competitor_gap_count": len(gaps),
        "minimum_owner_gap_enclosure": (
            arb_bounds(min(gaps, key=lambda value: value.value.lower()).value)
            if gaps else None
        ),
        "ordered_clean_wall_record": list(crossings),
        "clean_wall_event_evidence": wall_evidence,
        "no_wall_endpoint_or_corner_tie_on_closed_cell": True,
        "official_relative_target_id": relative_target,
        "official_word_key": official_key,
    }


def audit_cell(
    sheet: dict[str, Any], source: Any, branch: tuple[int, str, str, int],
    c00: Q, c01: Q, z0: Q, z1: Q,
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    coordinate = "c3" if sheet["sheet_kind"] == "HIT" else "b3"
    global_t0, global_t1, *_ = parse_box(sheet["enclosing_parameter_box"], coordinate)
    t0, t1, lower_sign, upper_sign = implicit_root_enclosure(
        source, branch, sheet["source_grazing_sign_sigma0"], sheet["sheet_kind"],
        global_t0, global_t1, c00, c01, z0, z1,
    )
    geometry = path_geometry(
        source, branch, sheet["source_grazing_sign_sigma0"], sheet["sheet_kind"],
        t0, t1, c00, c01, z0, z1,
    )
    dt_sign = strict_sign(geometry["equation"].gradient[0])
    if dt_sign == 0 or lower_sign != -dt_sign or upper_sign != dt_sign:
        raise RuntimeError("implicit_root_monotonicity")
    source_chart = strict_chart(*geometry["source_normal"])
    if source_chart is None or source_chart[0] != sheet["source_chart"].split(":")[1]:
        raise RuntimeError("source_chart_seam")
    first_selected = candidate_geometry(geometry["states"][0], source.target_id)
    second_selected = candidate_geometry(geometry["states"][1], branch[1])
    leg1 = leg_audit(
        geometry["states"][0], f"{source.source}[0,0]",
        sheet["source_chart"].split(":")[1], source.target_id,
        pair_index, pattern_index, first_selected,
    )
    leg2 = leg_audit(
        geometry["states"][1], source.target_id,
        sheet["first_outgoing_chart"], branch[1],
        pair_index, pattern_index, second_selected,
    )
    if (
        leg1["selected_collision_chart"] != sheet["first_outgoing_chart"]
        or leg2["selected_collision_chart"] != sheet["second_outgoing_chart"]
    ):
        raise RuntimeError("selected_first_second_chart_mismatch")
    designated = selected_third_geometry(geometry, branch[2], sheet["sheet_kind"])
    if sheet["sheet_kind"] == "HIT":
        leg3 = leg_audit(
            geometry["states"][2], branch[1],
            sheet["second_outgoing_chart"], branch[2],
            pair_index, pattern_index, designated,
        )
        actual_third = branch[2]
    else:
        leg3 = bypass_third_audit(
            geometry["states"][2], branch[1],
            sheet["second_outgoing_chart"], branch[2], designated,
            pair_index, pattern_index,
        )
        actual_third = leg3["actual_selected_owner_id"]
    return {
        "parameter_box": {
            "c0": [qstr(c00), qstr(c01)],
            coordinate: [qstr(z0), qstr(z1)],
        },
        "implicit_t_root_enclosure": [qstr(t0), qstr(t1)],
        "implicit_t_root_enclosure_width": qstr(t1 - t0),
        "strict_root_face_signs": [lower_sign, upper_sign],
        "uniform_dt_sign": dt_sign,
        "source_chart": source_chart[0],
        "source_chart_dominance_margin": arb_bounds(source_chart[2]),
        "ordered_regular_relative_interior_owner_ids": [
            source.target_id, branch[1], actual_third,
        ],
        "official_word_key_ids": [
            leg1["official_word_key"]["word_key_id"],
            leg2["official_word_key"]["word_key_id"],
            leg3["official_word_key"]["word_key_id"],
        ],
        "official_path_id": "gate5-rank3-endpoint-sheet-path:" + digest([
            leg1["official_word_key"]["word_key_id"],
            leg2["official_word_key"]["word_key_id"],
            leg3["official_word_key"]["word_key_id"],
        ]),
        "official_path_regular_on_parameter_relative_interior_only": True,
        "source_and_third_grazing_edges_owned_by_singularity_ledger": True,
        "leg_audits": [leg1, leg2, leg3],
        "all_three_legs_complete_candidate_first_owner_strict_on_regular_relative_interior": True,
        "all_three_legs_clean_wall_corner_chart_and_flight_cap_strict_on_regular_relative_interior": True,
    }


def split_box(box: tuple[Q, Q, Q, Q]) -> tuple[tuple[Q, Q, Q, Q], tuple[Q, Q, Q, Q]]:
    c00, c01, z0, z1 = box
    # Prefer c0: the root graph has a first-order c0 slope but only z3^2.
    if c01 - c00 >= z1 - z0:
        middle = (c00 + c01) / 2
        return (c00, middle, z0, z1), (middle, c01, z0, z1)
    middle = (z0 + z1) / 2
    return (c00, c01, z0, middle), (c00, c01, middle, z1)


def audit_sheet(
    sheet: dict[str, Any], source: Any, branch: tuple[int, str, str, int],
    max_depth: int,
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    coordinate = "c3" if sheet["sheet_kind"] == "HIT" else "b3"
    _t0, _t1, c00, c01, z0, z1 = parse_box(sheet["enclosing_parameter_box"], coordinate)
    stack: list[tuple[int, tuple[Q, Q, Q, Q]]] = [(0, (c00, c01, z0, z1))]
    certified: list[dict[str, Any]] = []
    residuals: list[dict[str, Any]] = []
    failures = Counter()
    while stack:
        depth, box = stack.pop()
        try:
            row = audit_cell(
                sheet, source, branch, *box, pair_index, pattern_index,
            )
            row["dyadic_depth"] = depth
            row["cell_id"] = "round113-cell:" + digest([
                sheet["sheet_id"], depth, [qstr(value) for value in box]
            ])
            certified.append(row)
        except (AssertionError, ValueError, ZeroDivisionError, RuntimeError) as exc:
            reason = f"{type(exc).__name__}:{exc}"
            failures[reason] += 1
            if depth < max_depth:
                left, right = split_box(box)
                stack.append((depth + 1, right))
                stack.append((depth + 1, left))
            else:
                residuals.append({
                    "parameter_box": {
                        "c0": [qstr(box[0]), qstr(box[1])],
                        coordinate: [qstr(box[2]), qstr(box[3])],
                    },
                    "dyadic_depth": depth,
                    "first_failure": reason,
                })
    certified.sort(key=lambda row: row["cell_id"])
    residuals.sort(key=lambda row: (row["parameter_box"]["c0"], row["parameter_box"][coordinate]))
    domain_area = (c01 - c00) * (z1 - z0)
    certified_area = sum(
        (Q(row["parameter_box"]["c0"][1]) - Q(row["parameter_box"]["c0"][0]))
        * (Q(row["parameter_box"][coordinate][1]) - Q(row["parameter_box"][coordinate][0]))
        for row in certified
    )
    residual_area = sum(
        (Q(row["parameter_box"]["c0"][1]) - Q(row["parameter_box"]["c0"][0]))
        * (Q(row["parameter_box"][coordinate][1]) - Q(row["parameter_box"][coordinate][0]))
        for row in residuals
    )
    if certified_area + residual_area != domain_area:
        raise RuntimeError("recursive dyadic cover area mismatch")
    owner_histogram = Counter(
        row["ordered_regular_relative_interior_owner_ids"][2] for row in certified
    )
    official_paths = sorted({row["official_path_id"] for row in certified})
    return {
        "sheet_id": sheet["sheet_id"],
        "sheet_kind": sheet["sheet_kind"],
        "corner_index": sheet["corner_index"],
        "exterior_port_id": sheet["exterior_port_id"],
        "branch_key": sheet["branch_key"],
        "source_chart": sheet["source_chart"],
        "coordinate_domain": sheet["enclosing_parameter_box"],
        "certified_cell_count": len(certified),
        "residual_cell_count": len(residuals),
        "maximum_certified_depth": max((row["dyadic_depth"] for row in certified), default=None),
        "failure_histogram_all_attempts": dict(sorted(failures.items())),
        "regular_relative_interior_third_owner_histogram": dict(sorted(owner_histogram.items())),
        "unique_regular_relative_interior_third_owner_count": len(owner_histogram),
        "unique_official_relative_interior_path_count": len(official_paths),
        "official_relative_interior_path_ids": official_paths,
        "coordinate_square_exact_rational_area": qstr(domain_area),
        "certified_leaf_union_exact_rational_area": qstr(certified_area),
        "residual_leaf_union_exact_rational_area": qstr(residual_area),
        "recursive_dyadic_leaf_cover_exact": True,
        "artificial_boundary_half_open_ownership_convention": (
            "[lower,upper) on each coordinate, except an interval ending at the "
            "outer domain endpoint owns that endpoint"
        ),
        "certified_cells": certified,
        "certified_cells_sha256": digest(certified),
        "residual_cells": residuals,
        "residual_cells_sha256": digest(residuals),
        "whole_sheet_regular_relative_interior_closed": len(residuals) == 0,
    }


def natural_boundary_trace_rows(
    input_sheets: list[dict[str, Any]], audited_sheets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    input_by_corner: dict[int, dict[str, dict[str, Any]]] = {}
    audited_by_corner: dict[int, dict[str, dict[str, Any]]] = {}
    for row in input_sheets:
        input_by_corner.setdefault(row["corner_index"], {})[row["sheet_kind"]] = row
    for row in audited_sheets:
        audited_by_corner.setdefault(row["corner_index"], {})[row["sheet_kind"]] = row
    rows = []
    for corner_index in range(8):
        pair = input_by_corner.get(corner_index, {})
        audited = audited_by_corner.get(corner_index, {})
        if set(pair) != {"HIT", "BYPASS"} or set(audited) != {"HIT", "BYPASS"}:
            raise RuntimeError("two-sided corner incidence")
        hit, bypass = pair["HIT"], pair["BYPASS"]
        hit_audit, bypass_audit = audited["HIT"], audited["BYPASS"]
        if (
            hit["branch_key"] != bypass["branch_key"]
            or hit["exterior_port_id"] != bypass["exterior_port_id"]
        ):
            raise RuntimeError("two-sided trace identity")
        hit_owner = list(hit_audit["regular_relative_interior_third_owner_histogram"])
        bypass_owner = list(bypass_audit["regular_relative_interior_third_owner_histogram"])
        if len(hit_owner) != 1 or len(bypass_owner) != 1:
            raise RuntimeError("nonconstant regular owner at a corner")
        c0_outer = hit["enclosing_parameter_box"]["c0"][1]
        c3_outer = hit["enclosing_parameter_box"]["c3"][1]
        b3_outer = bypass["enclosing_parameter_box"]["b3"][1]
        rows.append({
            "corner_index": corner_index,
            "trace_id": "round113-natural-trace:" + digest([
                hit["exterior_port_id"], hit["branch_key"], corner_index,
            ]),
            "exterior_port_id": hit["exterior_port_id"],
            "branch_key": hit["branch_key"],
            "designated_third_target_id": hit["branch_key"][2],
            "incident_hit_sheet_id": hit["sheet_id"],
            "incident_bypass_sheet_id": bypass["sheet_id"],
            "source_grazing_edge": {
                "hit_condition": f"c0=0, 0<=c3<={c3_outer}",
                "bypass_condition": f"c0=0, 0<=b3<={b3_outer}",
                "status": "NATURAL_SOURCE_GRAZING_SINGULARITY",
                "regular_owner_and_official_path_apply": False,
            },
            "shared_third_grazing_edge": {
                "hit_condition": f"0<=c0<={c0_outer}, c3=0",
                "bypass_condition": f"0<=c0<={c0_outer}, b3=0",
                "designated_candidate_status": "FUTURE_TANGENCY_NOT_TRANSVERSE_COLLISION",
                "bypass_regular_owner_id_does_not_apply_on_boundary": bypass_owner[0],
                "hit_regular_owner_limits_to_designated_tangent": hit_owner[0],
                "regular_official_third_word_applies": False,
            },
            "double_grazing_corner": {
                "condition": "c0=0 and c3=b3=0",
                "status": "SOURCE_AND_DESIGNATED_THIRD_DOUBLE_GRAZING",
                "regular_owner_and_official_path_apply": False,
            },
            "regular_relative_interior_strata": {
                "hit_condition": f"0<c0<={c0_outer}, 0<c3<={c3_outer}",
                "hit_third_owner_id": hit_owner[0],
                "hit_official_path_ids": hit_audit["official_relative_interior_path_ids"],
                "bypass_condition": f"0<c0<={c0_outer}, 0<b3<={b3_outer}",
                "bypass_third_owner_id": bypass_owner[0],
                "bypass_official_path_ids": bypass_audit["official_relative_interior_path_ids"],
            },
        })
    return rows


def build(precision_bits: int = PRECISION_BITS, max_depth: int = DEFAULT_MAX_DEPTH) -> dict[str, Any]:
    if precision_bits < 256 or max_depth < 0:
        raise RuntimeError("invalid runtime configuration")
    ctx.prec = precision_bits
    validate_pins()
    document = strict_load(ROUND112_JSON)
    if (
        set(document) != {"schema", "result", "result_sha256"}
        or document.get("schema") != round112.SCHEMA
        or document.get("result_sha256") != digest(document.get("result"))
    ):
        raise RuntimeError("Round112 document contract")
    upstream = document["result"]
    if (
        upstream.get("precision_bits") != 512
        or upstream.get("certified_hit_root_sheet_count") != 8
        or upstream.get("certified_bypass_root_sheet_count") != 8
        or upstream.get("certified_two_sided_sheet_row_count") != 16
        or upstream.get("whole_57_candidate_order_installed") is not False
        or upstream.get("first_second_owner_ordering_installed") is not False
        or upstream.get("official_word_or_canonical_child_installed") is not False
        or upstream.get("sheet_rows_sha256") != digest(upstream.get("sheet_rows"))
    ):
        raise RuntimeError("Round112 semantic handoff")
    sheets = upstream["sheet_rows"]
    if len(sheets) != 16:
        raise RuntimeError("Round112 sheet count")
    cores = core_cert.physical_cores()
    pair_index, pattern_index, registry_rows_sha256 = component.key_index_tables()
    sheet_rows = []
    for sheet in sheets:
        branch = tuple(sheet["branch_key"])
        base_source = cores[branch[0]]
        source = replace(base_source, chart_id=sheet["source_chart"])
        sheet_rows.append(audit_sheet(
            sheet, source, branch, max_depth, pair_index, pattern_index,
        ))
    sheet_rows.sort(key=lambda row: (row["corner_index"], row["sheet_kind"]))
    boundary_rows = natural_boundary_trace_rows(sheets, sheet_rows)
    residual_count = sum(row["residual_cell_count"] for row in sheet_rows)
    closed_count = sum(row["whole_sheet_regular_relative_interior_closed"] for row in sheet_rows)
    actual_histogram = Counter(
        owner for row in sheet_rows
        for owner, count in row["regular_relative_interior_third_owner_histogram"].items()
        for _ in range(count)
    )
    result = {
        "precision_bits": precision_bits,
        "maximum_dyadic_depth": max_depth,
        "stored_numeric_evidence_outward_padding": qstr(EVIDENCE_PADDING),
        "implicit_root_t_face_outward_padding": qstr(ROOT_T_FACE_OUTWARD_PADDING),
        "input_root_sheet_count": len(sheet_rows),
        "closed_root_sheet_count": closed_count,
        "residual_root_sheet_count": len(sheet_rows) - closed_count,
        "certified_parameter_cell_count": sum(row["certified_cell_count"] for row in sheet_rows),
        "residual_parameter_cell_count": residual_count,
        "hit_sheet_count": sum(row["sheet_kind"] == "HIT" for row in sheet_rows),
        "bypass_sheet_count": sum(row["sheet_kind"] == "BYPASS" for row in sheet_rows),
        "third_leg_complete_candidate_count": 57,
        "first_leg_complete_candidate_count": 57,
        "second_leg_complete_candidate_count": 55,
        "candidate_source": "frozen Gate3 retained target lifts translated by Round26 after tuple materialization",
        "candidate_and_official_word_source_audit": {
            "round79_role": "algebraic tangency/carrier seeds only; not a whole-sheet owner order",
            "round87_role": "registered local port continuation input",
            "round94_role": "adjacent source-chart transfer and tight grazing seed input",
            "round98_consumed_generator_bug_respected": True,
            "round98_audited_probe_count": 10112,
            "round98_corrected_occluded_probe_count": 8576,
            "round99_full_immutable_table_replay_required": True,
            "round99_audited_registered_port_count": 3212,
            "round99_corrected_locally_physical_port_count": 120,
            "round100_role": "source-cap incidence filter only",
            "round107_local_complete_candidate_germ_count": 24,
            "round107_whole_sheet_inheritance_rejected": True,
            "round108_fixed_s0_local_official_path_count": 24,
            "round108_whole_sheet_inheritance_rejected": True,
            "official_word_unit": "one straight flight, so rank three is three official keys",
        },
        "rank3_official_word_grammar": "one official Gate5 key per straight flight; a rank-three path requires three keys",
        "official_registry_candidate_key_count": 441280,
        "official_registry_rows_sha256": registry_rows_sha256,
        "regular_relative_interior_third_owner_histogram_by_certified_cell": dict(sorted(actual_histogram.items())),
        "sheet_rows": sheet_rows,
        "sheet_rows_sha256": digest(sheet_rows),
        "natural_boundary_trace_row_count": len(boundary_rows),
        "natural_boundary_trace_rows": boundary_rows,
        "natural_boundary_trace_rows_sha256": digest(boundary_rows),
        "whole_sheet_regular_relative_interior_unique_owner_ordering_installed": residual_count == 0,
        "complete_candidate_strict_classification_on_every_regular_relative_interior": residual_count == 0,
        "closed_proof_box_all_candidates_strictly_classified_without_boundary_labels": False,
        "unique_next_owner_strictly_earlier_than_every_other_future_candidate_on_every_regular_relative_interior": residual_count == 0,
        "full_pairwise_total_order_of_all_candidates_installed": False,
        "official_gate5_paths_installed_on_every_certified_relative_interior_cell": True,
        "whole_trace_collar_installed": False,
        "homogeneity_tail_or_canonical_child_installed": False,
        "gate5_actual_child_field_count": 0,
        "strict_scope": (
            "dyadic closed-cell owner-ordering certificate on the sixteen local Round112 root sheets; "
            "complete candidate first-owner comparisons, official three-key paths, and "
            "wall/corner/chart/flight-cap checks on the regular relative interiors of cells "
            "listed as certified; natural grazing edges are separate singular strata"
        ),
        "strict_nonclaims": [
            "a complete next-owner order is not a pairwise total order of all future candidates",
            "a selected-collision algebraic root sheet is not called a physical collar unless every parameter cell closes",
            "the Round108 fixed-box official paths are not inherited by these endpoint sheets",
            "official Gate5 paths are regular only on c0>0 and c3>0 or b3>0; grazing edges remain in the singularity ledger",
            "no whole-trace coverage, countable homogeneity tail, canonical curve recut, or Gate5 child field is installed",
            "residual boxes are explicit failures and contribute no physical-owner claim",
        ],
        "upstream_pins": PINS,
        "candidate_table_pattern_digests": TARGET_PATTERN_DIGEST,
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH)
    args = parser.parse_args()
    print(json.dumps(build(args.precision_bits, args.max_depth), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
