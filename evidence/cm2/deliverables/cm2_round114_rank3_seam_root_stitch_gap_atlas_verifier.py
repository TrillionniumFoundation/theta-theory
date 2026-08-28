#!/usr/bin/env python3
"""Independent verifier for the Round114 seam/root stitch gap atlas.

The verifier never imports the Round114 producer.  It reconstructs the seam
candidate censuses and the two endpoint q images directly from frozen
geometry, first at the producer's 640-bit precision for exact evidence
comparison and again at 768 bits for an independent semantic replay.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from collections import Counter
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_round91_rank3_exterior_source_exit_cert as round91
import cm2_round93_rank3_full_source_chart_exit_cert as round93
import cm2_round95_rank3_centered_reverse_interval_cert as round95
import cm2_round96_rank3_correlated_owner_interval_cert as round96
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval, normal
from cm2_round79_tangency_intersection_generator import digest, strict_sign


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "cm2-round114-rank3-seam-root-stitch-gap-atlas-2026-07-23.json"
PRODUCER = HERE / "cm2_round114_rank3_seam_root_stitch_gap_atlas.py"
UPSTREAM = {
    "r87": HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json",
    "r94": HERE / "cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json",
    "r99": HERE / "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json",
    "r111": HERE / "cm2-round111-rank3-round101-zero-width-correction-impact-audit-2026-07-23.json",
    "r112": HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json",
}
CERTIFIED_PRODUCER_PINS = {
    UPSTREAM["r87"].name: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    UPSTREAM["r94"].name: "915f7c18d896d92116ab3f4346a5853c09fef2d3226a1f5429a7c19bca948ee3",
    UPSTREAM["r99"].name: "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    UPSTREAM["r111"].name: "e343a15d5ad4838c2b9a808d64f9724e564e850cbdb13168c5e31e8f059794f1",
    UPSTREAM["r112"].name: "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate3_candidate_first_hit_cert.py": "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate34_round26_q1_time2_frontier_cert.py": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2_round76_r2_numeric_fields_generator.py": "96facebedf899d98d274f8a8c036fa8f02d1c34512933a587f7e581df174aadf",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    "cm2_round89_rank3_projective_gap_closure_cert.py": "6b5706fe16bd9a9142e64fbd227b32b6a2cfdc13d90d362c76fd33eca6874daf",
    "cm2_round91_rank3_exterior_source_exit_cert.py": "d75eb3a9a6aeca2c45b5b9eaa487c32481d4a9cf7e3da04c5d45d6f9a79414da",
    "cm2_round93_rank3_full_source_chart_exit_cert.py": "cec3bc83ae2a9df015441ce72397c2d553a74baf2cab89946a220ee4debb1023",
    "cm2_round95_rank3_centered_reverse_interval_cert.py": "c7921f2e999df9f1fb9ac935f28093e830d036116dafaf18dc2b2090c5e7702b",
    "cm2_round96_rank3_correlated_owner_interval_cert.py": "5c0205e4756270d8f94ede4947c2b80f82ad655b37d81a6bc02aa8bade54c702",
    "cm2_round112_rank3_double_grazing_two_sided_root_sheet.py": "ccdfeebfa14fdaa466a67b79269145b2a36076b7027f2bac0a9c5daa030b5e3f",
}
PINS = {
    CANDIDATE.name: "945cbd96032544bdff449398715f173cabb9e034415a0ca5edb594715ce970d4",
    PRODUCER.name: "47a231e32df2121058185a0fd82cbfb6c6105ace0d268a257103bc005b46ed02",
    **CERTIFIED_PRODUCER_PINS,
}
SCHEMA = "cm2.round114.rank3-seam-root-stitch-gap-atlas.v1"
EDGE_WIDTH = Q(1, 16384)
EDGE_DEPTH = 192
RESULT_KEYS = {
    "certified_selected_lift_root_edge_stitch_count",
    "certified_source_chart_seam_bridge_count",
    "gap_atlas",
    "gap_atlas_sha256",
    "input_corrected_ray_count",
    "new_gate5_actual_child_field_count",
    "physical_owner_end_to_end_trace_closure_count",
    "precision_bits",
    "root_edge_stitch_rows",
    "root_edge_stitch_rows_sha256",
    "selected_lift_end_to_end_trace_coverage_count",
    "source_chart_seam_bridge_rows",
    "source_chart_seam_bridge_rows_sha256",
    "strict_nonclaims",
    "strict_scope",
    "strict_separator",
    "upstream_and_helper_pins",
    "whole_collar_complete_57_candidate_ordering_count",
    "whole_trace_no_fold_atlas_count",
    "whole_trace_positive_reach_certificate_count",
    "whole_trace_two_sided_physical_collar_count",
    "whole_trace_uniform_other_singularity_separation_count",
}
SEAM_KEYS = {
    "adjacent_source_chart", "branch_key", "bridge_mode", "evidence", "exterior_port_id",
    "old_source_chart", "parameter_interval", "physical_selected_owner_clearance_replayed",
    "projective_end", "q_interval", "ray_index", "strict_positive_parameter_width",
}
SEAM_EVIDENCE_KEYS = {
    "all_competitor_rows_sha256", "cartesian_master_chart", "clearance_status_histogram",
    "first_candidate_union_size", "first_competitor_row_count", "first_outgoing_chart",
    "reverse_path", "second_competitor_row_count", "second_outgoing_chart",
    "source_table_policy", "strict_selected_flight_and_competitor_margin_lower_bound",
    "third_competitor_row_count",
}
EDGE_KEYS = {
    "blown_up_graph_determinant_abs_lower_bound", "blown_up_graph_determinant_identity",
    "branch_key", "bypass_sheet_id", "continuous_edge_image_covers_tail_and_reaches_unique_corner",
    "corner_parameter_enclosure", "corner_projective_q_enclosure", "corner_root_face_signs",
    "corner_t_root_bracket", "coverage_theorem", "exterior_port_id", "hit_sheet_id",
    "outer_parameter_enclosure", "outer_projective_q_enclosure", "outer_root_face_signs",
    "outer_t_root_bracket", "physical_owner_order_on_edge_installed", "pre_root_tail_parameter_interval",
    "projective_end", "q_of_c0_injectivity_installed", "ray_index", "shared_edge",
    "source_root_coordinate_interval", "stereographic_q_denominator_lower_bound",
    "strict_corner_after_tight_lower_margin", "strict_corner_before_tight_upper_margin",
    "strict_overlap_before_tail_margin", "tight_root_parameter_bracket",
}
EXPECTED_NONCLAIMS = [
    "the IVT edge stitch proves coverage, not injectivity or a no-fold q parameterisation",
    "the tight grazing parameter bracket encloses one unknown endpoint; it is not a physical trace interval whose every parameter must be covered",
    "the root-edge selected collision lift is not a complete first/second/third owner ordering",
    "the four-table seam bridge does not supply a positive-width transverse collar",
    "no uniform normal reach, chart-overlap width, or distance to every other singularity is installed along the whole trace",
    "the valid determinant is partial_t_Delta3 in blown-up (c0,t) coordinates; no (g0,Delta3) C1 Jacobian is claimed",
    "HIT and BYPASS remain separate real sheets sharing only c3=b3=0",
    "no homogeneity child, official word, or Gate5 field is installed",
]
EXPECTED_SEPARATOR = {
    "CM2": "NO-GO_FOR_CLAIM",
    "physical_owner_trace_closure": "0/8",
    "selected_lift_algebraic_trace_coverage": "8/8",
    "whole_trace_two_sided_collar": "0/8",
}
EXPECTED_GAPS = [
    {"gate": "SOURCE_CHART_TRANSFER_SEAM", "paid_count": 8, "remaining_count": 0, "status": "CLOSED_BY_CARTESIAN_MASTER_AND_FOUR_TABLE_UNION"},
    {"gate": "SELECTED_LIFT_PRE_ROOT_TAIL_TO_UNIQUE_CORNER", "paid_count": 8, "remaining_count": 0, "status": "PRE_ROOT_TAIL_COVERED_AND_UNIQUE_CORNER_ENCLOSED_INSIDE_TIGHT_NUMERICAL_BRACKET"},
    {"gate": "ROOT_EDGE_PHYSICAL_OWNER_ORDER", "paid_count": 0, "remaining_count": 8, "status": "OPEN__REQUIRES_COMPLETE_CANDIDATE_REPLAY_ON_ROOT_SHEETS"},
    {"gate": "WHOLE_TRACE_NO_FOLD_AND_POSITIVE_REACH", "paid_count": 0, "remaining_count": 8, "status": "OPEN__Q_IMAGE_COVERAGE_DOES_NOT_PROVE_INJECTIVITY_OR_NORMAL_REACH"},
    {"gate": "WHOLE_TRACE_TWO_SIDED_COLLAR_SEPARATION", "paid_count": 0, "remaining_count": 8, "status": "OPEN__NO_UNIFORM_DISTANCE_TO_ALL_OTHER_SINGULARITIES_OR_SEAMS"},
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_constant(token: str) -> Any:
    raise ValueError(f"nonfinite: {token}")


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def strict_load(text: str) -> dict[str, Any]:
    return json.loads(text, object_pairs_hook=strict_object, parse_constant=reject_constant)


def directed_pair(value: arb) -> tuple[Q, Q]:
    lower, _ = round91.arb_bounds(value.lower())
    _, upper = round91.arb_bounds(value.upper())
    return lower, upper


def positive_lower(value: arb) -> Q:
    if strict_sign(value) != 1:
        raise RuntimeError("non-strict positive evidence")
    lower, _ = directed_pair(value)
    if lower <= 0:
        raise RuntimeError("nonpositive directed endpoint")
    return lower


def validate_structure(doc: dict[str, Any]) -> None:
    if set(doc) != {"schema", "result", "result_sha256"} or doc.get("schema") != SCHEMA:
        raise ValueError("top-level schema")
    result = doc["result"]
    if doc["result_sha256"] != digest(result) or set(result) != RESULT_KEYS:
        raise ValueError("result closure")
    exact = {
        "precision_bits": 640,
        "input_corrected_ray_count": 8,
        "certified_source_chart_seam_bridge_count": 8,
        "certified_selected_lift_root_edge_stitch_count": 8,
        "selected_lift_end_to_end_trace_coverage_count": 8,
        "physical_owner_end_to_end_trace_closure_count": 0,
        "whole_trace_no_fold_atlas_count": 0,
        "whole_trace_positive_reach_certificate_count": 0,
        "whole_trace_uniform_other_singularity_separation_count": 0,
        "whole_trace_two_sided_physical_collar_count": 0,
        "whole_collar_complete_57_candidate_ordering_count": 0,
        "new_gate5_actual_child_field_count": 0,
    }
    for key, value in exact.items():
        if result.get(key) != value:
            raise ValueError(f"exact field: {key}")
    if result["strict_nonclaims"] != EXPECTED_NONCLAIMS or result["strict_separator"] != EXPECTED_SEPARATOR:
        raise ValueError("nonclaim/separator")
    if result["upstream_and_helper_pins"] != CERTIFIED_PRODUCER_PINS:
        raise ValueError("producer pin-map closure")
    if result["gap_atlas"] != EXPECTED_GAPS or result["gap_atlas_sha256"] != digest(EXPECTED_GAPS):
        raise ValueError("gap atlas")
    if result["source_chart_seam_bridge_rows_sha256"] != digest(result["source_chart_seam_bridge_rows"]):
        raise ValueError("seam digest")
    if result["root_edge_stitch_rows_sha256"] != digest(result["root_edge_stitch_rows"]):
        raise ValueError("edge digest")
    if len(result["source_chart_seam_bridge_rows"]) != 8 or len(result["root_edge_stitch_rows"]) != 8:
        raise ValueError("row census")
    if [row["ray_index"] for row in result["source_chart_seam_bridge_rows"]] != list(range(8)):
        raise ValueError("seam indices")
    if [row["ray_index"] for row in result["root_edge_stitch_rows"]] != list(range(8)):
        raise ValueError("edge indices")
    for row in result["source_chart_seam_bridge_rows"]:
        if set(row) != SEAM_KEYS or set(row["evidence"]) != SEAM_EVIDENCE_KEYS:
            raise ValueError("seam row keys")
        if row["bridge_mode"] != "CARTESIAN_MASTER_WITH_FOUR_SOURCE_TABLE_UNION" or not row["physical_selected_owner_clearance_replayed"]:
            raise ValueError("seam semantics")
        if not row["evidence"]["cartesian_master_chart"] or row["evidence"]["source_table_policy"] != "UNION_OF_E_W_N_S_FIRST_HIT_TABLES":
            raise ValueError("seam atlas")
        if Q(row["strict_positive_parameter_width"]) <= 0 or Q(row["evidence"]["strict_selected_flight_and_competitor_margin_lower_bound"]) <= 0:
            raise ValueError("seam strictness")
    for row in result["root_edge_stitch_rows"]:
        if set(row) != EDGE_KEYS:
            raise ValueError("edge row keys")
        if row["shared_edge"] != "c3=b3=0" or row["source_root_coordinate_interval"] != ["0", "1/16384"]:
            raise ValueError("edge coordinates")
        if row["coverage_theorem"] != "IVT_ON_CONTINUOUS_q_OF_UNIQUE_t(c0)_GRAPH" or not row["continuous_edge_image_covers_tail_and_reaches_unique_corner"]:
            raise ValueError("edge coverage")
        if row["q_of_c0_injectivity_installed"] or row["physical_owner_order_on_edge_installed"]:
            raise ValueError("edge overclaim")
        if row["blown_up_graph_determinant_identity"] != "det D_(c0,t)(c0,Delta3)=partial_t_Delta3":
            raise ValueError("determinant identity")
        if any(Q(row[key]) <= 0 for key in (
            "strict_overlap_before_tail_margin", "strict_corner_after_tight_lower_margin",
            "strict_corner_before_tight_upper_margin", "blown_up_graph_determinant_abs_lower_bound",
            "stereographic_q_denominator_lower_bound",
        )):
            raise ValueError("edge strictness")


def centered_state(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q) -> tuple[tuple[int, int, int], dict[str, Any]]:
    lo, hi = min(qa, qb), max(qa, qb)
    middle, radius = (lo + hi) / 2, (hi - lo) / 2
    path = round95.discover_path(source, branch, middle)
    q = round95.Centered.variable(aq(middle), round91.qball(lo, hi), arb(0, aq(radius).upper()))
    tangent_normal, outgoing2, offset = round95.tangent(branch, q)
    hit2, normal2 = round95.line_hit(tangent_normal, outgoing2, offset, branch[1], path[0])
    incoming2 = round95.reflect(outgoing2, normal2)
    hit1, normal1, flight1 = round95.ray_hit(hit2, round95.scale(-1, incoming2), source.target_id, path[1])
    initial = round95.reflect(incoming2, normal1)
    hit0, normal0, flight0 = round95.ray_hit(hit1, round95.scale(-1, initial), f"{source.source}[0,0]", path[2])
    contact = round95.sub(round95.center(branch[2]), round95.scale(branch[3] * round95.radius(branch[2]), tangent_normal))
    tangent_flight = round95.dot(outgoing2, round95.sub(contact, hit2))
    return path, {
        "hit0": hit0, "normal0": normal0, "initial": initial, "flight0": flight0,
        "hit1": hit1, "normal1": normal1, "outgoing1": incoming2, "flight1": flight1,
        "hit2": hit2, "normal2": normal2, "outgoing2": outgoing2, "tangent_flight": tangent_flight,
    }


def classify_clearance(point: Any, velocity: Any, target: str, terminal: Any) -> tuple[str, Q]:
    delta = round95.sub(round95.center(target), point)
    longitudinal = round95.dot(velocity, delta)
    transverse = round95.cross(velocity, delta)
    radius = round95.radius(target)
    line_clear = transverse * transverse - radius * radius
    end_clear = (longitudinal - terminal) * (longitudinal - terminal) + transverse * transverse - radius * radius
    if strict_sign(line_clear.value) == 1:
        return "WHOLE_LINE_MISS", positive_lower(line_clear.value)
    if strict_sign(-longitudinal.value) == 1:
        return "CLOSEST_BEHIND_START", positive_lower(-longitudinal.value)
    after = longitudinal - terminal
    if strict_sign(after.value) == 1 and strict_sign(end_clear.value) == 1:
        return "CLOSEST_AFTER_TERMINAL__END_CLEAR", min(positive_lower(after.value), positive_lower(end_clear.value))
    raise RuntimeError(f"unresolved seam candidate: {target}")


def independent_seam_evidence(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q) -> dict[str, Any]:
    path, state = centered_state(source, branch, qa, qb)
    flight_margins: list[Q] = []
    for name in ("flight0", "flight1", "tangent_flight"):
        flight_margins.extend((positive_lower(state[name].value), positive_lower(aq(Q(3)) - state[name].value)))
    first_ids: set[str] = set()
    for chart in ("E", "W", "N", "S"):
        first_ids.update(first_hit.candidate_ids(f"{source.source}:{chart}"))
    first_rows = [(target, *classify_clearance(state["hit0"], state["initial"], target, state["flight0"])) for target in sorted(first_ids - {source.target_id, f"{source.source}[0,0]"})]
    chart1 = round96.chart(state["normal1"])
    second_rows = [(target, *classify_clearance(state["hit1"], state["outgoing1"], target, state["flight1"])) for target in sorted(set(time2.translated_candidate_ids(source.target_id, chart1)) - {branch[1], source.target_id})]
    chart2 = round96.chart(state["normal2"])
    third_rows = [(target, *classify_clearance(state["hit2"], state["outgoing2"], target, state["tangent_flight"])) for target in sorted(set(time2.translated_candidate_ids(branch[1], chart2)) - {branch[2], branch[1]})]
    rows = [*first_rows, *second_rows, *third_rows]
    margin = min([*flight_margins, *(row[2] for row in rows)])
    return {
        "reverse_path": list(path),
        "cartesian_master_chart": True,
        "source_table_policy": "UNION_OF_E_W_N_S_FIRST_HIT_TABLES",
        "first_candidate_union_size": len(first_ids),
        "first_competitor_row_count": len(first_rows),
        "second_competitor_row_count": len(second_rows),
        "third_competitor_row_count": len(third_rows),
        "first_outgoing_chart": chart1,
        "second_outgoing_chart": chart2,
        "clearance_status_histogram": dict(sorted(Counter(row[1] for row in rows).items())),
        "all_competitor_rows_sha256": digest([(row[0], row[1], str(row[2])) for row in rows]),
        "strict_selected_flight_and_competitor_margin_lower_bound": str(margin),
    }


def edge_geometry(source: Any, branch: tuple[Any, ...], source_sign: int, ta: Q, tb: Q, ca: Q, cb: Q) -> dict[str, Jet]:
    t = Jet.variable(interval(ta, tb), 0)
    c0 = Jet.variable(interval(ca, cb), 1)
    zero = Jet(arb(0))
    nx, ny = normal(source.chart_id.split(":")[1], t)
    momentum0 = source_sign * (arb(1) - c0 * c0).sqrt()
    vx, vy = c0 * nx - momentum0 * ny, c0 * ny + momentum0 * nx
    sx, sy = center(f"{source.source}[0,0]", zero)
    px, py = sx + aq(round112.radius(source.source)) * nx, sy + aq(round112.radius(source.source)) * ny
    tx, ty = center(source.target_id, zero)
    first = round112.collision_diagnostic(px, py, vx, vy, tx, ty, round112.radius(source.target_id))
    cosine1 = (arb(1) - first["momentum"] * first["momentum"]).sqrt()
    v1x = cosine1 * first["normal_x"] - first["momentum"] * first["normal_y"]
    v1y = cosine1 * first["normal_y"] + first["momentum"] * first["normal_x"]
    tx, ty = center(branch[1], zero)
    second = round112.collision_diagnostic(first["hit_x"], first["hit_y"], v1x, v1y, tx, ty, round112.radius(branch[1]))
    cosine2 = (arb(1) - second["momentum"] * second["momentum"]).sqrt()
    v2x = cosine2 * second["normal_x"] - second["momentum"] * second["normal_y"]
    v2y = cosine2 * second["normal_y"] + second["momentum"] * second["normal_x"]
    tx, ty = center(branch[2], zero)
    dx, dy = tx - second["hit_x"], ty - second["hit_y"]
    transverse = -v2y * dx + v2x * dy
    radius3 = aq(round112.radius(branch[2]))
    denominator = arb(1) + v2x
    return {
        "equation": radius3 * radius3 - transverse * transverse,
        "projective_q": v2y / denominator,
        "projective_q_denominator": denominator,
    }


def edge_root(source: Any, branch: tuple[Any, ...], source_sign: int, c0: Q, lower: Q, upper: Q) -> tuple[Q, Q, int, int]:
    left_sign = strict_sign(edge_geometry(source, branch, source_sign, lower, lower, c0, c0)["equation"].value)
    right_sign = strict_sign(edge_geometry(source, branch, source_sign, upper, upper, c0, c0)["equation"].value)
    if not left_sign or not right_sign or left_sign == right_sign:
        raise RuntimeError("root faces")
    for _ in range(EDGE_DEPTH):
        middle = (lower + upper) / 2
        sign = strict_sign(edge_geometry(source, branch, source_sign, middle, middle, c0, c0)["equation"].value)
        if not sign:
            raise RuntimeError("root midpoint")
        if sign == left_sign:
            lower = middle
        else:
            upper = middle
    return lower, upper, left_sign, right_sign


def edge_q(source: Any, branch: tuple[Any, ...], source_sign: int, c0: Q, root: tuple[Q, Q, int, int]) -> tuple[Q, Q]:
    return directed_pair(edge_geometry(source, branch, source_sign, root[0], root[1], c0, c0)["projective_q"].value)


def parameter_pair(q0: Q, direction: int, q: tuple[Q, Q]) -> tuple[Q, Q]:
    values = direction * (q[0] - q0), direction * (q[1] - q0)
    return min(values), max(values)


def load_upstream() -> dict[str, dict[str, Any]]:
    result = {}
    for alias, path in UPSTREAM.items():
        doc = strict_load(path.read_text())
        if doc["result_sha256"] != digest(doc["result"]):
            raise RuntimeError(f"upstream digest: {alias}")
        result[alias] = doc["result"]
    return result


def mathematical_replay(doc: dict[str, Any], precision: int, exact_evidence: bool) -> tuple[int, int]:
    ctx.prec = precision
    data = load_upstream()
    result = doc["result"]
    by_port = {row["registered_port_id"]: row for row in data["r87"]["port_event_rows"]}
    physical = {port_id: by_port[port_id] for port_id in data["r99"]["corrected_locally_physical_registered_port_ids"]}
    frozen = {row["exterior_port_id"]: row for row in data["r111"]["ray_correction_rows"]}
    sheets: dict[str, dict[str, dict[str, Any]]] = {}
    for row in data["r112"]["sheet_rows"]:
        sheets.setdefault(row["exterior_port_id"], {})[row["sheet_kind"]] = row
    cores = core_cert.physical_cores()
    round91.round87.WORK_CORES = cores
    seam_count = 0
    edge_count = 0
    for row in result["source_chart_seam_bridge_rows"]:
        f = frozen[row["exterior_port_id"]]
        branch = tuple(row["branch_key"])
        q0, direction, _cell, inner, outer, kind, _a, _b = round93.isolate_event(branch, row["projective_end"], row["exterior_port_id"], physical, cores)
        if kind != "SOURCE_CHART_SEAM" or row["parameter_interval"] != [str(inner), str(outer)]:
            raise RuntimeError("independent seam crosswalk")
        qa, qb = q0 + direction * inner, q0 + direction * outer
        if row["q_interval"] != [str(qa), str(qb)] or row["strict_positive_parameter_width"] != str(outer - inner):
            raise RuntimeError("independent seam endpoints")
        evidence = independent_seam_evidence(cores[branch[0]], branch, qa, qb)
        if exact_evidence:
            if evidence != row["evidence"]:
                raise RuntimeError("independent seam evidence")
        else:
            for key in ("reverse_path", "first_candidate_union_size", "first_competitor_row_count", "second_competitor_row_count", "third_competitor_row_count", "first_outgoing_chart", "second_outgoing_chart", "clearance_status_histogram"):
                if evidence[key] != row["evidence"][key]:
                    raise RuntimeError(f"high-precision seam semantic: {key}")
        if f["unbridged_source_chart_transfer_seam_bracket"] != row["parameter_interval"]:
            raise RuntimeError("frozen seam mismatch")
        seam_count += 1

    for row in result["root_edge_stitch_rows"]:
        f = frozen[row["exterior_port_id"]]
        branch = tuple(row["branch_key"])
        hit = sheets[row["exterior_port_id"]]["HIT"]
        bypass = sheets[row["exterior_port_id"]]["BYPASS"]
        if row["hit_sheet_id"] != hit["sheet_id"] or row["bypass_sheet_id"] != bypass["sheet_id"]:
            raise RuntimeError("sheet ids")
        source = replace(cores[branch[0]], chart_id=hit["source_chart"])
        sign = hit["source_grazing_sign_sigma0"]
        tbox = tuple(map(Q, hit["enclosing_parameter_box"]["t"]))
        corner = edge_root(source, branch, sign, Q(0), *tbox)
        outer = edge_root(source, branch, sign, EDGE_WIDTH, *tbox)
        cq, oq = edge_q(source, branch, sign, Q(0), corner), edge_q(source, branch, sign, EDGE_WIDTH, outer)
        r87row = by_port[row["exterior_port_id"]]
        q0 = round91.q_mid(r87row)
        direction = -1 if row["projective_end"] == "LEFT_PROJECTIVE_END" else 1
        cp, op = parameter_pair(q0, direction, cq), parameter_pair(q0, direction, oq)
        tail = tuple(map(Q, f["remaining_pre_root_bracket_interval_tail_parameter_interval"]))
        tight = tuple(map(Q, f["unresolved_tight_algebraic_source_grazing_root_bracket"]))
        if not (op[1] < tail[0] and tight[0] < cp[0] and cp[1] < tight[1]):
            raise RuntimeError("independent edge overlap")
        full = edge_geometry(source, branch, sign, tbox[0], tbox[1], Q(0), EDGE_WIDTH)
        denominator_lower = positive_lower(full["projective_q_denominator"].value)
        sheet = round112.root_sheet_jet(source, branch[1], branch[2], sign, "HIT", tbox[0], tbox[1], Q(0), EDGE_WIDTH, Q(0), Q(0))
        dt = sheet["equation"].gradient[0]
        dt_bounds = directed_pair(dt)
        dt_lower = min(abs(dt_bounds[0]), abs(dt_bounds[1]))
        if strict_sign(dt) == 0 or dt_lower <= 3:
            raise RuntimeError("independent determinant")
        if exact_evidence:
            expected = {
                "ray_index": row["ray_index"], "exterior_port_id": row["exterior_port_id"], "branch_key": list(branch),
                "projective_end": row["projective_end"], "shared_edge": "c3=b3=0", "hit_sheet_id": hit["sheet_id"],
                "bypass_sheet_id": bypass["sheet_id"], "source_root_coordinate_interval": ["0", "1/16384"],
                "corner_t_root_bracket": [str(corner[0]), str(corner[1])], "outer_t_root_bracket": [str(outer[0]), str(outer[1])],
                "corner_root_face_signs": [corner[2], corner[3]], "outer_root_face_signs": [outer[2], outer[3]],
                "corner_projective_q_enclosure": [str(cq[0]), str(cq[1])], "outer_projective_q_enclosure": [str(oq[0]), str(oq[1])],
                "corner_parameter_enclosure": [str(cp[0]), str(cp[1])], "outer_parameter_enclosure": [str(op[0]), str(op[1])],
                "pre_root_tail_parameter_interval": [str(tail[0]), str(tail[1])], "tight_root_parameter_bracket": [str(tight[0]), str(tight[1])],
                "strict_overlap_before_tail_margin": str(tail[0] - op[1]), "strict_corner_after_tight_lower_margin": str(cp[0] - tight[0]),
                "strict_corner_before_tight_upper_margin": str(tight[1] - cp[1]),
                "blown_up_graph_determinant_identity": "det D_(c0,t)(c0,Delta3)=partial_t_Delta3",
                "blown_up_graph_determinant_abs_lower_bound": str(dt_lower), "stereographic_q_denominator_lower_bound": str(denominator_lower),
                "continuous_edge_image_covers_tail_and_reaches_unique_corner": True,
                "coverage_theorem": "IVT_ON_CONTINUOUS_q_OF_UNIQUE_t(c0)_GRAPH",
                "q_of_c0_injectivity_installed": False, "physical_owner_order_on_edge_installed": False,
            }
            if expected != row:
                raise RuntimeError("independent exact edge evidence")
        edge_count += 1
    return seam_count, edge_count


def resign(doc: dict[str, Any]) -> dict[str, Any]:
    doc["result"]["source_chart_seam_bridge_rows_sha256"] = digest(doc["result"]["source_chart_seam_bridge_rows"])
    doc["result"]["root_edge_stitch_rows_sha256"] = digest(doc["result"]["root_edge_stitch_rows"])
    doc["result"]["gap_atlas_sha256"] = digest(doc["result"]["gap_atlas"])
    doc["result_sha256"] = digest(doc["result"])
    return doc


def hostile_tests(doc: dict[str, Any]) -> int:
    mutations = []
    for key, value in (
        ("certified_source_chart_seam_bridge_count", 7),
        ("certified_selected_lift_root_edge_stitch_count", 7),
        ("selected_lift_end_to_end_trace_coverage_count", 7),
        ("physical_owner_end_to_end_trace_closure_count", 1),
        ("whole_trace_two_sided_physical_collar_count", 1),
        ("whole_trace_no_fold_atlas_count", 1),
    ):
        altered = copy.deepcopy(doc); altered["result"][key] = value; mutations.append(resign(altered))
    altered = copy.deepcopy(doc); altered["result"]["source_chart_seam_bridge_rows"][0]["physical_selected_owner_clearance_replayed"] = False; mutations.append(resign(altered))
    altered = copy.deepcopy(doc); altered["result"]["root_edge_stitch_rows"][0]["continuous_edge_image_covers_tail_and_reaches_unique_corner"] = False; mutations.append(resign(altered))
    altered = copy.deepcopy(doc); altered["result"]["root_edge_stitch_rows"][0]["q_of_c0_injectivity_installed"] = True; mutations.append(resign(altered))
    altered = copy.deepcopy(doc); altered["result"]["root_edge_stitch_rows"][0]["physical_owner_order_on_edge_installed"] = True; mutations.append(resign(altered))
    altered = copy.deepcopy(doc); altered["result"]["root_edge_stitch_rows"][0]["blown_up_graph_determinant_identity"] = "det D(g0,Delta3)"; mutations.append(resign(altered))
    altered = copy.deepcopy(doc); altered["result"]["strict_separator"]["CM2"] = "GO"; mutations.append(resign(altered))
    altered = copy.deepcopy(doc); altered["result"]["upstream_and_helper_pins"]["cm2_round95_rank3_centered_reverse_interval_cert.py"] = "0" * 64; mutations.append(resign(altered))
    rejected = 0
    for altered in mutations:
        try:
            validate_structure(altered)
        except (ValueError, RuntimeError, KeyError):
            rejected += 1
    if rejected != len(mutations):
        raise RuntimeError("hostile semantic rejection")
    return rejected


def json_hostile_tests(doc: dict[str, Any]) -> int:
    attacks = [
        '{"schema":"x","schema":"y","result":{},"result_sha256":"z"}',
        json.dumps(doc).replace('"precision_bits": 640', '"precision_bits": NaN', 1),
        json.dumps({**doc, "unknown": 1}),
    ]
    rejected = 0
    for text in attacks:
        try:
            candidate = strict_load(text)
            validate_structure(candidate)
        except (ValueError, RuntimeError, KeyError):
            rejected += 1
    if rejected != 3:
        raise RuntimeError("hostile JSON rejection")
    return rejected


def main() -> int:
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    doc = strict_load(CANDIDATE.read_text())
    validate_structure(doc)
    exact_seams, exact_edges = mathematical_replay(doc, 640, True)
    high_seams, high_edges = mathematical_replay(doc, 768, False)
    semantic_rejected = hostile_tests(doc)
    json_rejected = json_hostile_tests(doc)
    result = {
        "verdict": "VERIFIED",
        "candidate_schema": SCHEMA,
        "candidate_file_sha256": PINS[CANDIDATE.name],
        "candidate_result_sha256": doc["result_sha256"],
        "producer_file_sha256": PINS[PRODUCER.name],
        "producer_imported_by_verifier": False,
        "exact_replay_precision_bits": 640,
        "independent_replay_precision_bits": 768,
        "exact_source_chart_seam_bridge_replay_count": exact_seams,
        "exact_root_edge_stitch_replay_count": exact_edges,
        "high_precision_source_chart_seam_bridge_replay_count": high_seams,
        "high_precision_root_edge_stitch_replay_count": high_edges,
        "hostile_semantic_mutations_rejected": semantic_rejected,
        "strict_json_attacks_rejected": json_rejected,
        "selected_lift_trace_coverage_verified": "8/8",
        "physical_owner_trace_closure_verified": "0/8",
        "whole_trace_two_sided_collar_verified": "0/8",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    output = {"schema": "cm2.round114.rank3-seam-root-stitch-gap-atlas-verification.v1", "result": result, "result_sha256": digest(result)}
    json.dump(output, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
