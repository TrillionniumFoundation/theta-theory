#!/usr/bin/env python3
"""Independent verifier for the Round113 endpoint-sheet owner certificate.

The verifier does not import either Round113 producer module.  It rebuilds
the blown-up flight geometry, all three translated candidate tables, strict
next-owner gaps, collision charts, transparent-wall order, and official word
keys at higher Arb precision.  It also checks the dyadic cover and the
separate natural-boundary ledger, then runs re-signed semantic attacks and
strict-JSON attacks.
"""
from __future__ import annotations

import argparse
import copy
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
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval, normal
from cm2_round79_tangency_intersection_generator import strict_sign


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
ROUND112 = HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json"
PRODUCER = HERE / "cm2_round113_rank3_endpoint_sheet_owner_ordering.py"
ENGINE = HERE / "cm2_round113_rank3_root_sheet_owner_ordering_spike.py"
SCHEMA = "cm2.round113.rank3-endpoint-sheet-owner-ordering.v1"
VERIFICATION_SCHEMA = "cm2.round113.rank3-endpoint-sheet-owner-ordering.verification.v1"
PRECISION_BITS = 640
CERTIFICATE_SHA256 = "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181"
PRODUCER_SHA256 = "249e30c6410bf77e2c81aec346461fd4c0d4d4c8448e74894f73f0b8ccd0bfd3"
ENGINE_SHA256 = "2263d213bad42163da326c892662f500f29a3c5f6cf4b8ba28cc2bb57990b11e"
ROUND112_SHA256 = "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5"
REGISTRY_ROWS_SHA256 = "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"

EXPECTED_UPSTREAM_PINS = {
    "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json": ROUND112_SHA256,
    "cm2-round112-rank3-double-grazing-two-sided-root-sheet-manifest-2026-07-23.sha256": "2bacd33db96ae0aa6ea0857f0326243067c1abc87cfe58fd36356b0c417b7290",
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

RESULT_KEYS = {
    "precision_bits", "maximum_dyadic_depth", "stored_numeric_evidence_outward_padding",
    "implicit_root_t_face_outward_padding",
    "input_root_sheet_count", "closed_root_sheet_count", "residual_root_sheet_count",
    "certified_parameter_cell_count", "residual_parameter_cell_count", "hit_sheet_count",
    "bypass_sheet_count", "third_leg_complete_candidate_count",
    "first_leg_complete_candidate_count", "second_leg_complete_candidate_count",
    "candidate_source", "candidate_and_official_word_source_audit",
    "rank3_official_word_grammar", "official_registry_candidate_key_count",
    "official_registry_rows_sha256",
    "regular_relative_interior_third_owner_histogram_by_certified_cell",
    "sheet_rows", "sheet_rows_sha256", "natural_boundary_trace_row_count",
    "natural_boundary_trace_rows", "natural_boundary_trace_rows_sha256",
    "whole_sheet_regular_relative_interior_unique_owner_ordering_installed",
    "complete_candidate_strict_classification_on_every_regular_relative_interior",
    "closed_proof_box_all_candidates_strictly_classified_without_boundary_labels",
    "unique_next_owner_strictly_earlier_than_every_other_future_candidate_on_every_regular_relative_interior",
    "full_pairwise_total_order_of_all_candidates_installed",
    "official_gate5_paths_installed_on_every_certified_relative_interior_cell",
    "whole_trace_collar_installed", "homogeneity_tail_or_canonical_child_installed",
    "gate5_actual_child_field_count", "strict_scope", "strict_nonclaims",
    "upstream_pins", "candidate_table_pattern_digests",
}
SHEET_KEYS = {
    "sheet_id", "sheet_kind", "corner_index", "exterior_port_id", "branch_key",
    "source_chart", "coordinate_domain", "certified_cell_count", "residual_cell_count",
    "maximum_certified_depth", "failure_histogram_all_attempts",
    "regular_relative_interior_third_owner_histogram",
    "unique_regular_relative_interior_third_owner_count",
    "unique_official_relative_interior_path_count", "official_relative_interior_path_ids",
    "coordinate_square_exact_rational_area", "certified_leaf_union_exact_rational_area",
    "residual_leaf_union_exact_rational_area", "recursive_dyadic_leaf_cover_exact",
    "artificial_boundary_half_open_ownership_convention", "certified_cells",
    "certified_cells_sha256", "residual_cells", "residual_cells_sha256",
    "whole_sheet_regular_relative_interior_closed",
}
CELL_KEYS = {
    "parameter_box", "implicit_t_root_enclosure", "implicit_t_root_enclosure_width",
    "strict_root_face_signs", "uniform_dt_sign", "source_chart",
    "source_chart_dominance_margin", "ordered_regular_relative_interior_owner_ids",
    "official_word_key_ids", "official_path_id",
    "official_path_regular_on_parameter_relative_interior_only",
    "source_and_third_grazing_edges_owned_by_singularity_ledger", "leg_audits",
    "all_three_legs_complete_candidate_first_owner_strict_on_regular_relative_interior",
    "all_three_legs_clean_wall_corner_chart_and_flight_cap_strict_on_regular_relative_interior",
    "dyadic_depth", "cell_id",
}
REGULAR_LEG_KEYS = {
    "candidate_count", "candidate_ids_sha256", "candidate_table_source_digest",
    "selected_owner_id", "selected_root_enclosure", "selected_collision_chart",
    "selected_collision_chart_component_margin", "selected_collision_chart_dominance_margin",
    "classification_histogram", "strict_future_competitor_gap_count",
    "minimum_owner_gap_enclosure", "ordered_clean_wall_record",
    "clean_wall_event_evidence", "no_wall_endpoint_or_corner_tie_on_closed_cell",
    "official_relative_target_id", "official_word_key",
    "selected_target_regular_interior_status", "selected_target_natural_boundary_status",
}
BYPASS_LEG_KEYS = {
    "candidate_count", "candidate_ids_sha256", "candidate_table_source_digest",
    "designated_target_id", "designated_target_status", "actual_selected_owner_id",
    "actual_selected_root_enclosure",
    "designated_tangent_boundary_minus_bypass_winner_sign",
    "designated_tangent_boundary_minus_bypass_winner_enclosure",
    "b3_zero_designated_tangency_owned_by_trace_not_bypass_stratum",
    "selected_collision_chart", "selected_collision_chart_component_margin",
    "selected_collision_chart_dominance_margin", "classification_histogram",
    "strict_future_competitor_gap_count", "minimum_owner_gap_enclosure",
    "ordered_clean_wall_record",
    "clean_wall_event_evidence", "no_wall_endpoint_or_corner_tie_on_closed_cell",
    "official_relative_target_id", "official_word_key",
}
WORD_KEYS = {"ordinal_zero_based", "word_key_id", "row", "row_sha256"}
EVENT_KEYS = {"token", "wall", "alpha_enclosure"}
BOUNDARY_KEYS = {
    "corner_index", "trace_id", "exterior_port_id", "branch_key",
    "designated_third_target_id", "incident_hit_sheet_id", "incident_bypass_sheet_id",
    "source_grazing_edge", "shared_third_grazing_edge", "double_grazing_corner",
    "regular_relative_interior_strata",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def strict_load_text(text: str) -> dict[str, Any]:
    value = json.loads(text, object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
    require(isinstance(value, dict), "top-level JSON object")
    return value


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_text(path.read_text(encoding="utf-8"))


def radius(target: str) -> Q:
    return Q(9, 25) if target[0] == "G" else Q(4, 25)


def stored_contains(pair: Any, value: arb, label: str) -> int:
    require(isinstance(pair, list) and len(pair) == 2, f"{label} enclosure shape")
    lower, upper = arb(pair[0]).upper(), arb(pair[1]).lower()
    require(bool(value > lower) and bool(value < upper), f"{label} stored enclosure")
    return 1


def strict_chart(nx: Jet, ny: Jet) -> tuple[str, arb, arb] | None:
    x, y = nx.value, ny.value
    ax, ay = abs(x), abs(y)
    if bool(ax > ay):
        if bool(x > 0):
            return "E", x, ax - ay
        if bool(x < 0):
            return "W", -x, ax - ay
    if bool(ay > ax):
        if bool(y > 0):
            return "N", y, ay - ax
        if bool(y < 0):
            return "S", -y, ay - ax
    return None


def collision(
    qx: Jet, qy: Jet, ux: Jet, uy: Jet, ax: Jet, ay: Jet, target_radius: Q,
) -> dict[str, Jet]:
    rr = aq(target_radius)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    discriminant = rr * rr - transverse * transverse
    radical = discriminant.sqrt()
    flight = ell - radical
    hx, hy = qx + flight * ux, qy + flight * uy
    nx, ny = (hx - ax) / rr, (hy - ay) / rr
    momentum = transverse / rr
    return {
        "hit_x": hx, "hit_y": hy, "normal_x": nx, "normal_y": ny,
        "momentum": momentum, "flight": flight, "discriminant": discriminant,
    }


def geometry(
    source: Any, branch: tuple[int, str, str, int], source_sign: int,
    sheet_kind: str, t0: Q, t1: Q, c00: Q, c01: Q, z0: Q, z1: Q,
) -> dict[str, Any]:
    t = Jet.variable(interval(t0, t1), 0)
    c0 = Jet.variable(interval(c00, c01), 1)
    z3 = Jet.variable(interval(z0, z1), 2)
    zero = Jet(arb(0))
    source_nx, source_ny = normal(source.chart_id.split(":")[1], t)
    p0 = source_sign * (arb(1) - c0 * c0).sqrt()
    u0x = c0 * source_nx - p0 * source_ny
    u0y = c0 * source_ny + p0 * source_nx
    sx, sy = center(f"{source.source}[0,0]", zero)
    q0x = sx + aq(radius(source.source)) * source_nx
    q0y = sy + aq(radius(source.source)) * source_ny
    ax1, ay1 = center(source.target_id, zero)
    one = collision(q0x, q0y, u0x, u0y, ax1, ay1, radius(source.target_id))
    c1 = (arb(1) - one["momentum"] * one["momentum"]).sqrt()
    u1x = c1 * one["normal_x"] - one["momentum"] * one["normal_y"]
    u1y = c1 * one["normal_y"] + one["momentum"] * one["normal_x"]
    ax2, ay2 = center(branch[1], zero)
    two = collision(one["hit_x"], one["hit_y"], u1x, u1y, ax2, ay2, radius(branch[1]))
    c2 = (arb(1) - two["momentum"] * two["momentum"]).sqrt()
    u2x = c2 * two["normal_x"] - two["momentum"] * two["normal_y"]
    u2y = c2 * two["normal_y"] + two["momentum"] * two["normal_x"]
    ax3, ay3 = center(branch[2], zero)
    dx, dy = ax3 - two["hit_x"], ay3 - two["hit_y"]
    ell3 = u2x * dx + u2y * dy
    transverse3 = -u2y * dx + u2x * dy
    r3 = aq(radius(branch[2]))
    delta3 = r3 * r3 - transverse3 * transverse3
    equation = delta3 - r3 * r3 * z3 * z3 if sheet_kind == "HIT" else delta3 + r3 * r3 * z3 * z3
    return {
        "source_normal": (source_nx, source_ny),
        "states": (
            (q0x, q0y, u0x, u0y),
            (one["hit_x"], one["hit_y"], u1x, u1y),
            (two["hit_x"], two["hit_y"], u2x, u2y),
        ),
        "equation": equation,
        "third_ell": ell3,
        "third_transverse": transverse3,
        "third_radical": r3 * z3,
        "third_near": ell3 - r3 * z3,
    }


def candidate(state: tuple[Jet, Jet, Jet, Jet], candidate_id: str) -> dict[str, Any]:
    qx, qy, ux, uy = state
    ax, ay = center(candidate_id, Jet(arb(0)))
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    rr = aq(radius(candidate_id))
    discriminant = rr * rr - transverse * transverse
    if bool(discriminant.value < 0):
        return {"candidate_id": candidate_id, "classification": "STRICT_WHOLE_LINE_MISS"}
    if not bool(discriminant.value > 0):
        raise RuntimeError(f"unresolved discriminant:{candidate_id}")
    radical = discriminant.sqrt()
    near, far = ell - radical, ell + radical
    if bool(far.value < 0):
        return {"candidate_id": candidate_id, "classification": "STRICT_INTERSECTION_BEHIND"}
    require(bool(near.value > 0), f"unresolved root sign:{candidate_id}")
    nx = (-radical * ux + transverse * uy) / rr
    ny = (-radical * uy - transverse * ux) / rr
    return {
        "candidate_id": candidate_id, "classification": "STRICT_FUTURE_NEAR_ROOT",
        "near": near, "normal_x": nx, "normal_y": ny,
    }


def hit_designated(g: dict[str, Any], candidate_id: str) -> dict[str, Any]:
    _qx, _qy, ux, uy = g["states"][2]
    rr = aq(radius(candidate_id))
    radical, transverse = g["third_radical"], g["third_transverse"]
    return {
        "candidate_id": candidate_id,
        "classification": "REGULAR_INTERIOR_FUTURE_HIT__c3_ZERO_TANGENCY_BOUNDARY",
        "near": g["third_near"],
        "normal_x": (-radical * ux + transverse * uy) / rr,
        "normal_y": (-radical * uy - transverse * ux) / rr,
    }


def axis_events(q: arb, h: arb, axis: str) -> list[tuple[arb, str, int]]:
    require(bool(q > -7) and bool(q < 7) and bool(h > -7) and bool(h < 7), "wall audit range")
    result = []
    for wall in range(-6, 7):
        w = arb(wall)
        plus = bool(q < w) and bool(h > w)
        minus = bool(q > w) and bool(h < w)
        same_lower = bool(q < w) and bool(h < w)
        same_upper = bool(q > w) and bool(h > w)
        if plus or minus:
            alpha = (w - q) / (h - q)
            require(bool(alpha > 0) and bool(alpha < 1), "wall crossing time")
            result.append((alpha, axis + ("+" if plus else "-"), wall))
        else:
            require(same_lower or same_upper, "wall endpoint")
    require(len(result) <= 4, "wall count")
    return result


def ordered_events(events: list[tuple[arb, str, int]]) -> tuple[str, ...]:
    remaining = list(events)
    result = []
    while remaining:
        minima = [
            i for i, (alpha, _token, _wall) in enumerate(remaining)
            if all(i == j or bool(alpha < beta) for j, (beta, _t, _w) in enumerate(remaining))
        ]
        require(len(minima) == 1, "wall corner tie")
        _alpha, token, _wall = remaining.pop(minima[0])
        result.append(token)
    return tuple(result)


def wall_audit(
    stored: dict[str, Any], state: tuple[Jet, Jet, Jet, Jet], root: Jet,
) -> tuple[tuple[str, ...], int]:
    qx, qy, ux, uy = state
    hx, hy = qx + root * ux, qy + root * uy
    events = axis_events(qx.value, hx.value, "X") + axis_events(qy.value, hy.value, "Y")
    crossings = ordered_events(events)
    require(stored["ordered_clean_wall_record"] == list(crossings), "stored wall record")
    evidence = stored["clean_wall_event_evidence"]
    require(len(evidence) == len(events), "wall evidence count")
    checks = 0
    for saved, (alpha, token, wall) in zip(evidence, events):
        require(set(saved) == EVENT_KEYS and saved["token"] == token and saved["wall"] == wall, "wall event row")
        checks += stored_contains(saved["alpha_enclosure"], alpha, "wall alpha")
    return crossings, checks


def verify_leg(
    saved: dict[str, Any], state: tuple[Jet, Jet, Jet, Jet], current_target: str,
    chart: str, selected_target: str, kind: str, g: dict[str, Any],
    pair_index: dict[tuple[str, str], int], pattern_index: dict[tuple[str, ...], int],
) -> tuple[str, str, int, int]:
    expected_keys = BYPASS_LEG_KEYS if kind == "BYPASS" else REGULAR_LEG_KEYS
    require(set(saved) == expected_keys, f"{kind} leg closed schema")
    ids = tuple(time2.translated_candidate_ids(current_target, chart))
    require(len(ids) == len(set(ids)) and selected_target in ids, "candidate universe")
    require(saved["candidate_count"] == len(ids), "candidate count")
    require(saved["candidate_ids_sha256"] == digest(list(ids)), "candidate id digest")
    source_digest = digest(list(time2.relative_candidate_ids(current_target[0], chart)))
    require(saved["candidate_table_source_digest"] == source_digest, "candidate source digest")
    rows = []
    for target in ids:
        if target == selected_target and kind == "HIT":
            row = hit_designated(g, target)
        elif target == selected_target and kind == "BYPASS":
            row = {
                "candidate_id": target,
                "classification": "BYPASS_INTERIOR_MISS__TANGENT_BOUNDARY",
                "tangent": g["third_ell"],
            }
        else:
            row = candidate(state, target)
        rows.append(row)
    histogram = Counter(row["classification"] for row in rows)
    require(saved["classification_histogram"] == dict(sorted(histogram.items())), "classification histogram")
    future = [row for row in rows if row["classification"] in {
        "STRICT_FUTURE_NEAR_ROOT",
        "REGULAR_INTERIOR_FUTURE_HIT__c3_ZERO_TANGENCY_BOUNDARY",
    }]
    evidence_checks = 0
    if kind == "BYPASS":
        winners = [
            row for row in future
            if all(row is other or bool(row["near"].value < other["near"].value) for other in future)
        ]
        require(len(winners) == 1, "bypass unique winner")
        selected = winners[0]
        require(saved["designated_target_id"] == selected_target, "bypass designated target")
        require(saved["designated_target_status"] == "BYPASS_INTERIOR_MISS__TANGENT_BOUNDARY", "bypass mixed boundary status")
        require(saved["actual_selected_owner_id"] == selected["candidate_id"], "bypass owner")
        require(saved["b3_zero_designated_tangency_owned_by_trace_not_bypass_stratum"] is True, "bypass trace boundary")
        evidence_checks += stored_contains(saved["actual_selected_root_enclosure"], selected["near"].value, "bypass root")
        tangent_gap = g["third_ell"] - selected["near"]
        require(strict_sign(tangent_gap.value) == saved["designated_tangent_boundary_minus_bypass_winner_sign"] != 0, "bypass boundary order")
        evidence_checks += stored_contains(saved["designated_tangent_boundary_minus_bypass_winner_enclosure"], tangent_gap.value, "bypass boundary gap")
    else:
        selected = next(row for row in rows if row["candidate_id"] == selected_target)
        require(saved["selected_owner_id"] == selected_target, "selected owner")
        require(saved["selected_target_regular_interior_status"] == "STRICT_FUTURE_NEAR_ROOT", "regular selected status")
        expected_boundary = "THIRD_GRAZING_TANGENCY" if kind == "HIT" else "TRANSVERSE_COLLISION_ON_THIRD_GRAZING_BOUNDARY_NOT_APPLICABLE"
        require(saved["selected_target_natural_boundary_status"] == expected_boundary, "selected boundary status")
        evidence_checks += stored_contains(saved["selected_root_enclosure"], selected["near"].value, "selected root")
    root = selected["near"]
    require(bool(root.value > 0) and bool(root.value < aq(Q(3))), "flight cap")
    gaps = [row["near"] - root for row in future if row is not selected]
    require(all(strict_sign(gap.value) == 1 for gap in gaps), "strict next-owner gaps")
    require(saved["strict_future_competitor_gap_count"] == len(gaps), "gap count")
    if gaps:
        minimum = min(gaps, key=lambda value: value.value.lower())
        evidence_checks += stored_contains(saved["minimum_owner_gap_enclosure"], minimum.value, "minimum owner gap")
    else:
        require(saved["minimum_owner_gap_enclosure"] is None, "empty gap evidence")
    selected_chart = strict_chart(selected["normal_x"], selected["normal_y"])
    require(selected_chart is not None and saved["selected_collision_chart"] == selected_chart[0], "selected chart")
    assert selected_chart is not None
    evidence_checks += stored_contains(saved["selected_collision_chart_component_margin"], selected_chart[1], "chart component")
    evidence_checks += stored_contains(saved["selected_collision_chart_dominance_margin"], selected_chart[2], "chart dominance")
    crossings, wall_checks = wall_audit(saved, state, root)
    evidence_checks += wall_checks
    relative = component.relative_target(current_target, selected["candidate_id"])
    require(saved["official_relative_target_id"] == relative, "official relative target")
    key = component.word_key(f"{current_target[0]}:{chart}", relative, crossings, pair_index, pattern_index)
    require(set(saved["official_word_key"]) == WORD_KEYS and saved["official_word_key"] == key, "official word key")
    require(saved["no_wall_endpoint_or_corner_tie_on_closed_cell"] is True, "wall/corner flag")
    return selected["candidate_id"], key["word_key_id"], len(ids), evidence_checks


def half_open_owns(x: Q, lower: Q, upper: Q, outer: Q) -> bool:
    return lower <= x < upper or (upper == outer and x == outer)


def verify_cover(sheet: dict[str, Any], upstream: dict[str, Any]) -> None:
    coordinate = "c3" if sheet["sheet_kind"] == "HIT" else "b3"
    domain = upstream["enclosing_parameter_box"]
    c0a, c0b = map(Q, domain["c0"])
    za, zb = map(Q, domain[coordinate])
    rectangles = []
    for cell in sheet["certified_cells"]:
        a, b = map(Q, cell["parameter_box"]["c0"])
        c, d = map(Q, cell["parameter_box"][coordinate])
        require(c0a <= a < b <= c0b and za <= c < d <= zb, "leaf in domain")
        rectangles.append((a, b, c, d))
    xs = sorted({c0a, c0b, *(x for rect in rectangles for x in rect[:2])})
    zs = sorted({za, zb, *(x for rect in rectangles for x in rect[2:])})
    xprobes = sorted(set(xs + [(a + b) / 2 for a, b in zip(xs, xs[1:])]))
    zprobes = sorted(set(zs + [(a + b) / 2 for a, b in zip(zs, zs[1:])]))
    for x in xprobes:
        for z in zprobes:
            owners = sum(
                half_open_owns(x, a, b, c0b) and half_open_owns(z, c, d, zb)
                for a, b, c, d in rectangles
            )
            require(owners == 1, "half-open exact cover")
    area = sum((b - a) * (d - c) for a, b, c, d in rectangles)
    require(area == (c0b - c0a) * (zb - za), "exact cover area")
    require(sheet["coordinate_square_exact_rational_area"] == str(area), "stored domain area")
    require(sheet["certified_leaf_union_exact_rational_area"] == str(area), "stored certified area")
    require(sheet["residual_leaf_union_exact_rational_area"] == "0", "stored residual area")


def verify_boundary_rows(result: dict[str, Any], upstream_sheets: list[dict[str, Any]]) -> None:
    rows = result["natural_boundary_trace_rows"]
    require(len(rows) == result["natural_boundary_trace_row_count"] == 8, "boundary row count")
    require(result["natural_boundary_trace_rows_sha256"] == digest(rows), "boundary row digest")
    input_by_corner: dict[int, dict[str, dict[str, Any]]] = {}
    audit_by_corner: dict[int, dict[str, dict[str, Any]]] = {}
    for row in upstream_sheets:
        input_by_corner.setdefault(row["corner_index"], {})[row["sheet_kind"]] = row
    for row in result["sheet_rows"]:
        audit_by_corner.setdefault(row["corner_index"], {})[row["sheet_kind"]] = row
    for index, row in enumerate(rows):
        require(set(row) == BOUNDARY_KEYS and row["corner_index"] == index, "boundary closed row")
        hit, bypass = input_by_corner[index]["HIT"], input_by_corner[index]["BYPASS"]
        hit_a, bypass_a = audit_by_corner[index]["HIT"], audit_by_corner[index]["BYPASS"]
        require(row["trace_id"] == "round113-natural-trace:" + digest([hit["exterior_port_id"], hit["branch_key"], index]), "trace id")
        require(row["branch_key"] == hit["branch_key"] == bypass["branch_key"], "trace branch")
        require(row["designated_third_target_id"] == hit["branch_key"][2], "trace target")
        require(row["incident_hit_sheet_id"] == hit["sheet_id"] and row["incident_bypass_sheet_id"] == bypass["sheet_id"], "trace incidence")
        source_edge = row["source_grazing_edge"]
        require(set(source_edge) == {"hit_condition", "bypass_condition", "status", "regular_owner_and_official_path_apply"}, "source edge schema")
        require(source_edge["status"] == "NATURAL_SOURCE_GRAZING_SINGULARITY" and source_edge["regular_owner_and_official_path_apply"] is False, "source edge semantics")
        third_edge = row["shared_third_grazing_edge"]
        require(set(third_edge) == {"hit_condition", "bypass_condition", "designated_candidate_status", "bypass_regular_owner_id_does_not_apply_on_boundary", "hit_regular_owner_limits_to_designated_tangent", "regular_official_third_word_applies"}, "third edge schema")
        require(third_edge["designated_candidate_status"] == "FUTURE_TANGENCY_NOT_TRANSVERSE_COLLISION" and third_edge["regular_official_third_word_applies"] is False, "third edge semantics")
        require(third_edge["bypass_regular_owner_id_does_not_apply_on_boundary"] in bypass_a["regular_relative_interior_third_owner_histogram"], "bypass boundary exclusion")
        require(third_edge["hit_regular_owner_limits_to_designated_tangent"] == hit["branch_key"][2], "hit tangent owner")
        corner = row["double_grazing_corner"]
        require(corner == {"condition": "c0=0 and c3=b3=0", "status": "SOURCE_AND_DESIGNATED_THIRD_DOUBLE_GRAZING", "regular_owner_and_official_path_apply": False}, "double corner")
        strata = row["regular_relative_interior_strata"]
        require(set(strata) == {"hit_condition", "hit_third_owner_id", "hit_official_path_ids", "bypass_condition", "bypass_third_owner_id", "bypass_official_path_ids"}, "regular strata schema")
        require(strata["hit_third_owner_id"] in hit_a["regular_relative_interior_third_owner_histogram"], "hit stratum owner")
        require(strata["bypass_third_owner_id"] in bypass_a["regular_relative_interior_third_owner_histogram"], "bypass stratum owner")
        require(strata["hit_official_path_ids"] == hit_a["official_relative_interior_path_ids"] and strata["bypass_official_path_ids"] == bypass_a["official_relative_interior_path_ids"], "stratum paths")


def structural_contract(document: dict[str, Any]) -> None:
    require(set(document) == {"schema", "result", "result_sha256"}, "top-level schema")
    require(document["schema"] == SCHEMA and document["result_sha256"] == digest(document["result"]), "document digest/schema")
    result = document["result"]
    require(isinstance(result, dict) and set(result) == RESULT_KEYS, "closed result schema")
    required_scalars = {
        "precision_bits": 512, "maximum_dyadic_depth": 4,
        "stored_numeric_evidence_outward_padding": "1/1000000",
        "implicit_root_t_face_outward_padding": "1/1000000000",
        "input_root_sheet_count": 16, "closed_root_sheet_count": 16,
        "residual_root_sheet_count": 0, "certified_parameter_cell_count": 72,
        "residual_parameter_cell_count": 0, "hit_sheet_count": 8,
        "bypass_sheet_count": 8, "first_leg_complete_candidate_count": 57,
        "second_leg_complete_candidate_count": 55, "third_leg_complete_candidate_count": 57,
        "official_registry_candidate_key_count": 441280,
        "official_registry_rows_sha256": REGISTRY_ROWS_SHA256,
        "natural_boundary_trace_row_count": 8,
        "whole_sheet_regular_relative_interior_unique_owner_ordering_installed": True,
        "complete_candidate_strict_classification_on_every_regular_relative_interior": True,
        "closed_proof_box_all_candidates_strictly_classified_without_boundary_labels": False,
        "unique_next_owner_strictly_earlier_than_every_other_future_candidate_on_every_regular_relative_interior": True,
        "full_pairwise_total_order_of_all_candidates_installed": False,
        "official_gate5_paths_installed_on_every_certified_relative_interior_cell": True,
        "whole_trace_collar_installed": False,
        "homogeneity_tail_or_canonical_child_installed": False,
        "gate5_actual_child_field_count": 0,
    }
    for key, expected in required_scalars.items():
        require(result[key] == expected, f"result scalar:{key}")
    require(result["upstream_pins"] == EXPECTED_UPSTREAM_PINS, "upstream pins payload")
    require(result["sheet_rows_sha256"] == digest(result["sheet_rows"]), "sheet digest")
    require(len(result["sheet_rows"]) == 16, "sheet rows")
    for sheet in result["sheet_rows"]:
        require(set(sheet) == SHEET_KEYS, "closed sheet schema")
        require(sheet["residual_cell_count"] == 0 and sheet["residual_cells"] == [], "sheet residual")
        require(sheet["residual_cells_sha256"] == digest([]), "residual digest")
        require(sheet["whole_sheet_regular_relative_interior_closed"] is True, "sheet closed")
        require(sheet["certified_cells_sha256"] == digest(sheet["certified_cells"]), "cell digest")
        require(sheet["certified_cell_count"] == len(sheet["certified_cells"]), "cell count")
        expected_count = 1 if sheet["sheet_kind"] == "HIT" else 8
        expected_depth = 0 if sheet["sheet_kind"] == "HIT" else 3
        require(sheet["certified_cell_count"] == expected_count and sheet["maximum_certified_depth"] == expected_depth, "sheet subdivision")
        require(sheet["unique_regular_relative_interior_third_owner_count"] == 1 and sheet["unique_official_relative_interior_path_count"] == 1, "sheet owner/path constancy")
        for cell in sheet["certified_cells"]:
            require(set(cell) == CELL_KEYS and len(cell["leg_audits"]) == 3, "closed cell schema")
            require(set(cell["leg_audits"][0]) == REGULAR_LEG_KEYS and set(cell["leg_audits"][1]) == REGULAR_LEG_KEYS, "prefix leg schema")
            require(set(cell["leg_audits"][2]) == (REGULAR_LEG_KEYS if sheet["sheet_kind"] == "HIT" else BYPASS_LEG_KEYS), "third leg schema")
            require([leg["candidate_count"] for leg in cell["leg_audits"]] == [57, 55, 57], "57/55/57 cell counts")
            for leg in cell["leg_audits"]:
                require(set(leg["official_word_key"]) == WORD_KEYS, "word key schema")
                require(all(set(event) == EVENT_KEYS for event in leg["clean_wall_event_evidence"]), "event schema")
            require(cell["source_and_third_grazing_edges_owned_by_singularity_ledger"] is True, "cell boundary ledger flag")
            require(cell["official_path_regular_on_parameter_relative_interior_only"] is True, "cell path scope")
        if sheet["sheet_kind"] == "BYPASS":
            require(all(cell["leg_audits"][2]["designated_target_status"] == "BYPASS_INTERIOR_MISS__TANGENT_BOUNDARY" for cell in sheet["certified_cells"]), "bypass mixed boundary label")
        else:
            require(all(cell["leg_audits"][2]["selected_target_natural_boundary_status"] == "THIRD_GRAZING_TANGENCY" for cell in sheet["certified_cells"]), "hit tangent boundary label")


def verify_document(document: dict[str, Any], precision_bits: int) -> dict[str, Any]:
    structural_contract(document)
    result = document["result"]
    ctx.prec = precision_bits
    upstream = strict_load(ROUND112)
    require(set(upstream) == {"schema", "result", "result_sha256"} and upstream["result_sha256"] == digest(upstream["result"]), "Round112 contract")
    upstream_sheets = upstream["result"]["sheet_rows"]
    upstream_by_id = {row["sheet_id"]: row for row in upstream_sheets}
    require(len(upstream_by_id) == 16, "Round112 sheet identity")
    cores = core_cert.physical_cores()
    pair_index, pattern_index, registry_sha = component.key_index_tables()
    require(registry_sha == REGISTRY_ROWS_SHA256, "official registry replay")
    candidate_comparisons = 0
    official_legs = 0
    evidence_checks = 0
    owner_histogram = Counter()
    for sheet in result["sheet_rows"]:
        upstream_sheet = upstream_by_id.get(sheet["sheet_id"])
        require(upstream_sheet is not None, "upstream sheet binding")
        require(sheet["coordinate_domain"] == upstream_sheet["enclosing_parameter_box"], "sheet domain binding")
        require(sheet["branch_key"] == upstream_sheet["branch_key"] and sheet["source_chart"] == upstream_sheet["source_chart"], "sheet geometry binding")
        verify_cover(sheet, upstream_sheet)
        branch = tuple(sheet["branch_key"])
        source = replace(cores[branch[0]], chart_id=sheet["source_chart"])
        coordinate = "c3" if sheet["sheet_kind"] == "HIT" else "b3"
        saved_owners = Counter()
        saved_paths = set()
        for cell in sheet["certified_cells"]:
            c00, c01 = map(Q, cell["parameter_box"]["c0"])
            z0, z1 = map(Q, cell["parameter_box"][coordinate])
            t0, t1 = map(Q, cell["implicit_t_root_enclosure"])
            require(Q(cell["implicit_t_root_enclosure_width"]) == t1 - t0 > 0, "implicit root width")
            g = geometry(source, branch, upstream_sheet["source_grazing_sign_sigma0"], sheet["sheet_kind"], t0, t1, c00, c01, z0, z1)
            left = geometry(source, branch, upstream_sheet["source_grazing_sign_sigma0"], sheet["sheet_kind"], t0, t0, c00, c01, z0, z1)["equation"].value
            right = geometry(source, branch, upstream_sheet["source_grazing_sign_sigma0"], sheet["sheet_kind"], t1, t1, c00, c01, z0, z1)["equation"].value
            signs = [strict_sign(left), strict_sign(right)]
            dt_sign = strict_sign(g["equation"].gradient[0])
            require(signs == cell["strict_root_face_signs"] and dt_sign == cell["uniform_dt_sign"] != 0, "implicit root signs")
            require(signs == [-dt_sign, dt_sign], "implicit monotone existence")
            source_chart = strict_chart(*g["source_normal"])
            require(source_chart is not None and source_chart[0] == cell["source_chart"] == sheet["source_chart"].split(":")[1], "source chart")
            assert source_chart is not None
            evidence_checks += stored_contains(cell["source_chart_dominance_margin"], source_chart[2], "source chart dominance")
            owner1, key1, n1, e1 = verify_leg(
                cell["leg_audits"][0], g["states"][0], f"{source.source}[0,0]",
                sheet["source_chart"].split(":")[1], source.target_id, "REGULAR", g,
                pair_index, pattern_index,
            )
            owner2, key2, n2, e2 = verify_leg(
                cell["leg_audits"][1], g["states"][1], source.target_id,
                upstream_sheet["first_outgoing_chart"], branch[1], "REGULAR", g,
                pair_index, pattern_index,
            )
            owner3, key3, n3, e3 = verify_leg(
                cell["leg_audits"][2], g["states"][2], branch[1],
                upstream_sheet["second_outgoing_chart"], branch[2], sheet["sheet_kind"], g,
                pair_index, pattern_index,
            )
            require(cell["ordered_regular_relative_interior_owner_ids"] == [owner1, owner2, owner3], "cell owner chain")
            keys = [key1, key2, key3]
            require(cell["official_word_key_ids"] == keys, "cell official keys")
            require(cell["official_path_id"] == "gate5-rank3-endpoint-sheet-path:" + digest(keys), "official path id")
            require(cell["cell_id"] == "round113-cell:" + digest([sheet["sheet_id"], cell["dyadic_depth"], [str(c00), str(c01), str(z0), str(z1)]]), "cell id")
            candidate_comparisons += n1 + n2 + n3
            official_legs += 3
            evidence_checks += e1 + e2 + e3
            saved_owners[owner3] += 1
            saved_paths.add(cell["official_path_id"])
            require(cell["all_three_legs_complete_candidate_first_owner_strict_on_regular_relative_interior"] is True, "owner flag")
            require(cell["all_three_legs_clean_wall_corner_chart_and_flight_cap_strict_on_regular_relative_interior"] is True, "path strict flag")
        require(sheet["regular_relative_interior_third_owner_histogram"] == dict(sorted(saved_owners.items())), "sheet owner histogram")
        require(sheet["official_relative_interior_path_ids"] == sorted(saved_paths), "sheet paths")
        owner_histogram.update(saved_owners)
    require(result["regular_relative_interior_third_owner_histogram_by_certified_cell"] == dict(sorted(owner_histogram.items())), "global owner histogram")
    verify_boundary_rows(result, upstream_sheets)
    return {
        "independently_recomputed_root_sheet_count": 16,
        "independently_recomputed_parameter_cell_count": 72,
        "independently_recomputed_candidate_row_count": candidate_comparisons,
        "independently_recomputed_official_leg_count": official_legs,
        "stored_numeric_evidence_containment_check_count": evidence_checks,
        "natural_boundary_trace_row_count": 8,
        "relative_interior_owner_ordering_status": "PASS",
        "full_pairwise_total_order_status": "EXPLICITLY_NOT_CLAIMED",
        "whole_trace_collar_status": "NOT_INSTALLED",
    }


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def attack_tests(document: dict[str, Any]) -> tuple[int, list[str]]:
    attacks: list[tuple[str, Any]] = []
    def add(name: str, mutation: Any) -> None:
        attacks.append((name, mutation))
    add("promote_total_order", lambda d: d["result"].__setitem__("full_pairwise_total_order_of_all_candidates_installed", True))
    add("promote_whole_trace", lambda d: d["result"].__setitem__("whole_trace_collar_installed", True))
    add("change_second_candidate_count", lambda d: d["result"].__setitem__("second_leg_complete_candidate_count", 57))
    add("invent_residual", lambda d: d["result"].__setitem__("residual_parameter_cell_count", 1))
    add("erase_boundary_label", lambda d: d["result"]["sheet_rows"][0]["certified_cells"][0]["leg_audits"][2].__setitem__("designated_target_status", "STRICT_WHOLE_LINE_MISS"))
    add("apply_word_on_boundary", lambda d: d["result"]["natural_boundary_trace_rows"][0]["shared_third_grazing_edge"].__setitem__("regular_official_third_word_applies", True))
    add("change_owner", lambda d: d["result"]["sheet_rows"][0]["certified_cells"][0]["leg_audits"][2].__setitem__("actual_selected_owner_id", "G[0,0]"))
    add("change_official_key", lambda d: d["result"]["sheet_rows"][0]["certified_cells"][0]["leg_audits"][2]["official_word_key"].__setitem__("word_key_id", "gate5-word:forged"))
    add("change_cell_candidate_count", lambda d: d["result"]["sheet_rows"][0]["certified_cells"][0]["leg_audits"][0].__setitem__("candidate_count", 58))
    add("remove_leg_field", lambda d: d["result"]["sheet_rows"][0]["certified_cells"][0]["leg_audits"][0].pop("classification_histogram"))
    add("unknown_result_key", lambda d: d["result"].__setitem__("forged", True))
    add("flip_boundary_gap_sign", lambda d: d["result"]["sheet_rows"][0]["certified_cells"][0]["leg_audits"][2].__setitem__("designated_tangent_boundary_minus_bypass_winner_sign", 1))
    rejected = []
    for name, mutation in attacks:
        trial = copy.deepcopy(document)
        mutation(trial)
        resign(trial)
        try:
            structural_contract(trial)
        except (AssertionError, KeyError, TypeError, ValueError, RuntimeError):
            rejected.append(name)
        else:
            # Deep semantic rows not fixed by the scalar contract must still
            # fail the independent replay; run it only for those few cases.
            try:
                verify_document(trial, PRECISION_BITS)
            except (AssertionError, KeyError, TypeError, ValueError, RuntimeError):
                rejected.append(name)
            else:
                raise RuntimeError(f"semantic attack accepted: {name}")
    return len(rejected), rejected


def json_attack_tests(text: str) -> tuple[int, list[str]]:
    attacks = [
        ("duplicate_key", '{"schema":"x","schema":"y","result":{},"result_sha256":"z"}'),
        ("nan", text.replace('"precision_bits": 512', '"precision_bits": NaN', 1)),
        ("infinity", text.replace('"precision_bits": 512', '"precision_bits": Infinity', 1)),
    ]
    rejected = []
    for name, payload in attacks:
        try:
            strict_load_text(payload)
        except (TypeError, ValueError, RuntimeError):
            rejected.append(name)
        else:
            raise RuntimeError(f"strict JSON attack accepted: {name}")
    return len(rejected), rejected


def verify_pins() -> None:
    require(CERTIFICATE_SHA256 != "TO_BE_FILLED", "verifier certificate pin not frozen")
    require(PRODUCER_SHA256 != "TO_BE_FILLED" and ENGINE_SHA256 != "TO_BE_FILLED", "verifier producer pins not frozen")
    require(sha256(CERTIFICATE) == CERTIFICATE_SHA256, "certificate byte pin")
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer byte pin")
    require(sha256(ENGINE) == ENGINE_SHA256, "engine byte pin")
    require(sha256(ROUND112) == ROUND112_SHA256, "Round112 byte pin")
    for name, expected in EXPECTED_UPSTREAM_PINS.items():
        require(sha256(HERE / name) == expected, f"upstream byte pin:{name}")


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    require(precision_bits >= 640, "verification precision")
    verify_pins()
    text = CERTIFICATE.read_text(encoding="utf-8")
    document = strict_load_text(text)
    replay = verify_document(document, precision_bits)
    attack_count, attack_names = attack_tests(document)
    json_count, json_names = json_attack_tests(text)
    result = {
        "verification_precision_bits": precision_bits,
        **replay,
        "semantic_resigning_attack_count": attack_count,
        "semantic_resigning_attacks_rejected": attack_names,
        "strict_json_attack_count": json_count,
        "strict_json_attacks_rejected": json_names,
        "certificate_sha256": CERTIFICATE_SHA256,
        "producer_sha256": PRODUCER_SHA256,
        "engine_sha256": ENGINE_SHA256,
        "independent_verifier_does_not_import_round113_producer_or_engine": True,
        "verification_status": "PASS",
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": VERIFICATION_SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    args = parser.parse_args()
    print(json.dumps(build(args.precision_bits), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
