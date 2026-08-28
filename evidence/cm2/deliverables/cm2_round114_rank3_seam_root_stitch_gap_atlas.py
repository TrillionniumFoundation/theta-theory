#!/usr/bin/env python3
"""Close the eight representation-seam gaps and stitch the algebraic trace edge.

This round deliberately separates three statements which older endpoint ledgers
conflated:

* a Cartesian, four-table-union replay can bridge each source-chart seam;
* the shared c3=b3=0 edge of the Round112 HIT/BYPASS sheets continuously
  overlaps the last certified q-rings and replaces the tight q root bracket by
  a unique blown-up corner;
* neither fact supplies a physical-owner collar, a no-fold parameterisation,
  positive reach, or separation from every other singularity.

The second item is only selected-lift algebraic coverage.  It uses the
intermediate-value theorem for the continuous stereographic q image of the
unique t(c0) root graph; no injectivity of q(c0) is claimed.
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
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round91_rank3_exterior_source_exit_cert as round91
import cm2_round93_rank3_full_source_chart_exit_cert as round93
import cm2_round95_rank3_centered_reverse_interval_cert as round95
import cm2_round96_rank3_correlated_owner_interval_cert as round96
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval, normal
from cm2_round79_tangency_intersection_generator import digest, strict_sign


HERE = Path(__file__).resolve().parent
FILES = {
    "r87": HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json",
    "r94": HERE / "cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json",
    "r99": HERE / "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json",
    "r111": HERE / "cm2-round111-rank3-round101-zero-width-correction-impact-audit-2026-07-23.json",
    "r112": HERE / "cm2-round112-rank3-double-grazing-two-sided-root-sheet-2026-07-23.json",
}
PINS = {
    FILES["r87"].name: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    FILES["r94"].name: "915f7c18d896d92116ab3f4346a5853c09fef2d3226a1f5429a7c19bca948ee3",
    FILES["r99"].name: "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    FILES["r111"].name: "e343a15d5ad4838c2b9a808d64f9724e564e850cbdb13168c5e31e8f059794f1",
    FILES["r112"].name: "94a54ddbf31518cfc2a93b105d66337111f2b950be894f126e7b9c042e6b02e5",
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
SCHEMAS = {
    "r87": "cm2.round87.rank3-port-event-continuation.v1",
    "r94": "cm2.round94.rank3-adjacent-chart-transfer.v1",
    "r99": "cm2.round99.rank3-registered-port-candidate-audit.v1",
    "r111": "cm2.round111.rank3-round101-zero-width-correction-impact-audit.v1",
    "r112": "cm2.round112.rank3-double-grazing-two-sided-root-sheet.v1",
}
SCHEMA = "cm2.round114.rank3-seam-root-stitch-gap-atlas.v1"
PRECISION_BITS = 640
EDGE_ROOT_DEPTH = 192
EDGE_WIDTH = Q(1, 16384)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_documents() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for alias, path in FILES.items():
        if sha256(path) != PINS[path.name]:
            raise RuntimeError(f"pin mismatch: {path.name}")
        doc = json.loads(path.read_text(), parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
        if set(doc) != {"schema", "result", "result_sha256"}:
            raise RuntimeError(f"open document: {path.name}")
        if doc["schema"] != SCHEMAS[alias] or doc["result_sha256"] != digest(doc["result"]):
            raise RuntimeError(f"closed document mismatch: {path.name}")
        result[alias] = doc["result"]
    for name, expected in PINS.items():
        if name in {path.name for path in FILES.values()}:
            continue
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"helper pin mismatch: {name}")
    return result


def arb_pair(value: arb) -> tuple[Q, Q]:
    # ``str(value)`` prints the radius with deliberately few digits.  Parsing
    # that presentation can erase a tiny strict margin by making centre-radius
    # round to zero.  The directed endpoint balls retain the rigorous side.
    lower, _ = round91.arb_bounds(value.lower())
    _, upper = round91.arb_bounds(value.upper())
    return lower, upper


def positive_lower(value: arb, label: str) -> Q:
    if strict_sign(value) != 1:
        raise RuntimeError(f"non-strict {label}")
    lower, _ = arb_pair(value)
    if lower <= 0:
        raise RuntimeError(f"nonpositive directed lower bound: {label}")
    return lower


def centered_seam_state(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q) -> tuple[tuple[int, int, int], dict[str, Any]]:
    lo, hi = min(qa, qb), max(qa, qb)
    middle, radius = (lo + hi) / 2, (hi - lo) / 2
    path = round95.discover_path(source, branch, middle)
    q_value = round95.Centered.variable(aq(middle), round91.qball(lo, hi), arb(0, aq(radius).upper()))
    tangent_normal, direction, offset = round95.tangent(branch, q_value)
    hit2, normal2 = round95.line_hit(tangent_normal, direction, offset, branch[1], path[0])
    incoming2 = round95.reflect(direction, normal2)
    hit1, normal1, flight1 = round95.ray_hit(hit2, round95.scale(-1, incoming2), source.target_id, path[1])
    initial = round95.reflect(incoming2, normal1)
    hit0, normal0, flight0 = round95.ray_hit(hit1, round95.scale(-1, initial), f"{source.source}[0,0]", path[2])
    contact = round95.sub(round95.center(branch[2]), round95.scale(branch[3] * round95.radius(branch[2]), tangent_normal))
    tangent_flight = round95.dot(direction, round95.sub(contact, hit2))
    values = {
        "hit0": hit0,
        "normal0": normal0,
        "initial": initial,
        "flight0": flight0,
        "hit1": hit1,
        "normal1": normal1,
        "outgoing1": incoming2,
        "flight1": flight1,
        "hit2": hit2,
        "normal2": normal2,
        "outgoing2": direction,
        "tangent_flight": tangent_flight,
    }
    return path, values


def clearance(point: Any, velocity: Any, target: str, terminal: Any) -> tuple[str, Q]:
    delta = round95.sub(round95.center(target), point)
    longitudinal = round95.dot(velocity, delta)
    transverse = round95.cross(velocity, delta)
    radius = round95.radius(target)
    line_clear = transverse * transverse - radius * radius
    end_clear = (longitudinal - terminal) * (longitudinal - terminal) + transverse * transverse - radius * radius
    if strict_sign(line_clear.value) == 1:
        return "WHOLE_LINE_MISS", positive_lower(line_clear.value, f"line clear {target}")
    if strict_sign(-longitudinal.value) == 1:
        return "CLOSEST_BEHIND_START", positive_lower(-longitudinal.value, f"behind {target}")
    after = longitudinal - terminal
    if strict_sign(after.value) == 1 and strict_sign(end_clear.value) == 1:
        return "CLOSEST_AFTER_TERMINAL__END_CLEAR", min(
            positive_lower(after.value, f"after {target}"),
            positive_lower(end_clear.value, f"end clear {target}"),
        )
    raise RuntimeError(f"seam competitor unresolved: {target}")


def seam_bridge_evidence(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q) -> dict[str, Any]:
    path, state = centered_seam_state(source, branch, qa, qb)
    flight_margins: list[Q] = []
    for name in ("flight0", "flight1", "tangent_flight"):
        value = state[name].value
        flight_margins.extend((positive_lower(value, name), positive_lower(aq(Q(3)) - value, f"3-{name}")))

    first_ids: set[str] = set()
    for chart in ("E", "W", "N", "S"):
        first_ids.update(first_hit.candidate_ids(f"{source.source}:{chart}"))
    first_rows = [
        (target, *clearance(state["hit0"], state["initial"], target, state["flight0"]))
        for target in sorted(first_ids - {source.target_id, f"{source.source}[0,0]"})
    ]
    chart1 = round96.chart(state["normal1"])
    second_rows = [
        (target, *clearance(state["hit1"], state["outgoing1"], target, state["flight1"]))
        for target in sorted(set(time2.translated_candidate_ids(source.target_id, chart1)) - {branch[1], source.target_id})
    ]
    chart2 = round96.chart(state["normal2"])
    third_rows = [
        (target, *clearance(state["hit2"], state["outgoing2"], target, state["tangent_flight"]))
        for target in sorted(set(time2.translated_candidate_ids(branch[1], chart2)) - {branch[2], branch[1]})
    ]
    if len(first_rows) != 75:
        raise RuntimeError("four-chart first census")
    all_rows = [*first_rows, *second_rows, *third_rows]
    margin = min([*flight_margins, *(row[2] for row in all_rows)])
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
        "clearance_status_histogram": dict(sorted(Counter(row[1] for row in all_rows).items())),
        "all_competitor_rows_sha256": digest([(row[0], row[1], str(row[2])) for row in all_rows]),
        "strict_selected_flight_and_competitor_margin_lower_bound": str(margin),
    }


def edge_jet(source: Any, branch: tuple[Any, ...], source_sign: int, t0: Q, t1: Q, c00: Q, c01: Q) -> dict[str, Jet]:
    t = Jet.variable(interval(t0, t1), 0)
    c0 = Jet.variable(interval(c00, c01), 1)
    zero = Jet(arb(0))
    source_normal_x, source_normal_y = normal(source.chart_id.split(":")[1], t)
    source_p = source_sign * (arb(1) - c0 * c0).sqrt()
    velocity_x = c0 * source_normal_x - source_p * source_normal_y
    velocity_y = c0 * source_normal_y + source_p * source_normal_x
    source_x, source_y = center(f"{source.source}[0,0]", zero)
    point_x = source_x + aq(round112.radius(source.source)) * source_normal_x
    point_y = source_y + aq(round112.radius(source.source)) * source_normal_y

    first_x, first_y = center(source.target_id, zero)
    first = round112.collision_diagnostic(point_x, point_y, velocity_x, velocity_y, first_x, first_y, round112.radius(source.target_id))
    first_c = (arb(1) - first["momentum"] * first["momentum"]).sqrt()
    outgoing1_x = first_c * first["normal_x"] - first["momentum"] * first["normal_y"]
    outgoing1_y = first_c * first["normal_y"] + first["momentum"] * first["normal_x"]

    second_x, second_y = center(branch[1], zero)
    second = round112.collision_diagnostic(first["hit_x"], first["hit_y"], outgoing1_x, outgoing1_y, second_x, second_y, round112.radius(branch[1]))
    second_c = (arb(1) - second["momentum"] * second["momentum"]).sqrt()
    outgoing2_x = second_c * second["normal_x"] - second["momentum"] * second["normal_y"]
    outgoing2_y = second_c * second["normal_y"] + second["momentum"] * second["normal_x"]

    candidate_x, candidate_y = center(branch[2], zero)
    dx, dy = candidate_x - second["hit_x"], candidate_y - second["hit_y"]
    transverse = -outgoing2_y * dx + outgoing2_x * dy
    radius3 = aq(round112.radius(branch[2]))
    equation = radius3 * radius3 - transverse * transverse
    denominator = arb(1) + outgoing2_x
    projective_q = outgoing2_y / denominator
    return {
        "equation": equation,
        "projective_q": projective_q,
        "projective_q_denominator": denominator,
        "third_transverse": transverse,
    }


def isolate_edge_root(source: Any, branch: tuple[Any, ...], source_sign: int, c0: Q, lower: Q, upper: Q) -> tuple[Q, Q, int, int]:
    left = edge_jet(source, branch, source_sign, lower, lower, c0, c0)["equation"].value
    right = edge_jet(source, branch, source_sign, upper, upper, c0, c0)["equation"].value
    left_sign, right_sign = strict_sign(left), strict_sign(right)
    if left_sign == 0 or right_sign == 0 or left_sign == right_sign:
        raise RuntimeError("edge root faces")
    for _ in range(EDGE_ROOT_DEPTH):
        middle = (lower + upper) / 2
        middle_sign = strict_sign(edge_jet(source, branch, source_sign, middle, middle, c0, c0)["equation"].value)
        if middle_sign == 0:
            raise RuntimeError("edge root bisection indeterminate")
        if middle_sign == left_sign:
            lower = middle
        else:
            upper = middle
    return lower, upper, left_sign, right_sign


def q_bounds_on_edge_root(source: Any, branch: tuple[Any, ...], source_sign: int, c0: Q, root: tuple[Q, Q, int, int]) -> tuple[Q, Q]:
    value = edge_jet(source, branch, source_sign, root[0], root[1], c0, c0)["projective_q"].value
    return arb_pair(value)


def parameter_bounds(q0: Q, direction: int, q_bounds: tuple[Q, Q]) -> tuple[Q, Q]:
    values = (direction * (q_bounds[0] - q0), direction * (q_bounds[1] - q0))
    return min(values), max(values)


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    if precision_bits < 512:
        raise RuntimeError("insufficient precision")
    ctx.prec = precision_bits
    docs = load_documents()
    by_port = {row["registered_port_id"]: row for row in docs["r87"]["port_event_rows"]}
    physical = {port_id: by_port[port_id] for port_id in docs["r99"]["corrected_locally_physical_registered_port_ids"]}
    transfers = {row["exterior_port_id"]: row for row in docs["r94"]["transfer_rows"]}
    r111_rows = {row["exterior_port_id"]: row for row in docs["r111"]["ray_correction_rows"]}
    sheet_groups: dict[str, dict[str, dict[str, Any]]] = {}
    for row in docs["r112"]["sheet_rows"]:
        sheet_groups.setdefault(row["exterior_port_id"], {})[row["sheet_kind"]] = row
    cores = core_cert.physical_cores()
    round91.round87.WORK_CORES = cores

    seam_rows: list[dict[str, Any]] = []
    edge_rows: list[dict[str, Any]] = []
    for frozen in sorted(docs["r111"]["ray_correction_rows"], key=lambda row: row["ray_index"]):
        ray_index = frozen["ray_index"]
        port_id = frozen["exterior_port_id"]
        branch = tuple(frozen["branch_key"])
        q0, direction, _cell_edge, inner, seam_outer, event_kind, _inner_state, _outer_state = round93.isolate_event(
            branch, frozen["projective_end"], port_id, physical, cores
        )
        if event_kind != "SOURCE_CHART_SEAM" or [str(inner), str(seam_outer)] != frozen["unbridged_source_chart_transfer_seam_bracket"]:
            raise RuntimeError("seam bracket crosswalk")
        qa, qb = q0 + direction * inner, q0 + direction * seam_outer
        source = cores[branch[0]]
        seam_evidence = seam_bridge_evidence(source, branch, qa, qb)
        seam_rows.append({
            "ray_index": ray_index,
            "exterior_port_id": port_id,
            "branch_key": list(branch),
            "projective_end": frozen["projective_end"],
            "parameter_interval": [str(inner), str(seam_outer)],
            "q_interval": [str(qa), str(qb)],
            "strict_positive_parameter_width": str(seam_outer - inner),
            "old_source_chart": frozen["old_source_chart"],
            "adjacent_source_chart": frozen["adjacent_source_chart"],
            "bridge_mode": "CARTESIAN_MASTER_WITH_FOUR_SOURCE_TABLE_UNION",
            "physical_selected_owner_clearance_replayed": True,
            "evidence": seam_evidence,
        })

        sheets = sheet_groups.get(port_id, {})
        if set(sheets) != {"HIT", "BYPASS"}:
            raise RuntimeError("two-sided sheet crosswalk")
        hit, bypass = sheets["HIT"], sheets["BYPASS"]
        for key in ("branch_key", "corner_root_t_bracket", "source_chart", "source_grazing_sign_sigma0", "tight_round94_grazing_parameter_bracket"):
            if hit[key] != bypass[key]:
                raise RuntimeError(f"shared edge mismatch: {key}")
        if hit["tight_round94_grazing_parameter_bracket"] != frozen["unresolved_tight_algebraic_source_grazing_root_bracket"]:
            raise RuntimeError("tight bracket crosswalk")
        edge_source = replace(cores[branch[0]], chart_id=hit["source_chart"])
        source_sign = hit["source_grazing_sign_sigma0"]
        t_box = tuple(map(Q, hit["enclosing_parameter_box"]["t"]))
        corner_root = isolate_edge_root(edge_source, branch, source_sign, Q(0), *t_box)
        outer_root = isolate_edge_root(edge_source, branch, source_sign, EDGE_WIDTH, *t_box)
        corner_q = q_bounds_on_edge_root(edge_source, branch, source_sign, Q(0), corner_root)
        outer_q = q_bounds_on_edge_root(edge_source, branch, source_sign, EDGE_WIDTH, outer_root)
        corner_parameter = parameter_bounds(q0, direction, corner_q)
        outer_parameter = parameter_bounds(q0, direction, outer_q)

        tight_lower, tight_upper = map(Q, frozen["unresolved_tight_algebraic_source_grazing_root_bracket"])
        tail_lower, tail_upper = map(Q, frozen["remaining_pre_root_bracket_interval_tail_parameter_interval"])
        if tail_upper != tight_lower:
            raise RuntimeError("tail/tight adjacency")
        if not (
            outer_parameter[1] < tail_lower
            and tight_lower < corner_parameter[0]
            and corner_parameter[1] < tight_upper
        ):
            raise RuntimeError("root-edge overlap/order")

        full_edge = edge_jet(edge_source, branch, source_sign, t_box[0], t_box[1], Q(0), EDGE_WIDTH)
        q_denominator_lower = positive_lower(full_edge["projective_q_denominator"].value, "stereographic q denominator")
        full_sheet = round112.root_sheet_jet(
            edge_source, branch[1], branch[2], source_sign, "HIT",
            t_box[0], t_box[1], Q(0), EDGE_WIDTH, Q(0), Q(0),
        )
        dt = full_sheet["equation"].gradient[0]
        dt_lower = min(abs(value) for value in arb_pair(dt))
        if strict_sign(dt) == 0 or dt_lower <= 3:
            raise RuntimeError("blown-up graph determinant")

        edge_rows.append({
            "ray_index": ray_index,
            "exterior_port_id": port_id,
            "branch_key": list(branch),
            "projective_end": frozen["projective_end"],
            "shared_edge": "c3=b3=0",
            "hit_sheet_id": hit["sheet_id"],
            "bypass_sheet_id": bypass["sheet_id"],
            "source_root_coordinate_interval": ["0", str(EDGE_WIDTH)],
            "corner_t_root_bracket": [str(corner_root[0]), str(corner_root[1])],
            "outer_t_root_bracket": [str(outer_root[0]), str(outer_root[1])],
            "corner_root_face_signs": [corner_root[2], corner_root[3]],
            "outer_root_face_signs": [outer_root[2], outer_root[3]],
            "corner_projective_q_enclosure": [str(corner_q[0]), str(corner_q[1])],
            "outer_projective_q_enclosure": [str(outer_q[0]), str(outer_q[1])],
            "corner_parameter_enclosure": [str(corner_parameter[0]), str(corner_parameter[1])],
            "outer_parameter_enclosure": [str(outer_parameter[0]), str(outer_parameter[1])],
            "pre_root_tail_parameter_interval": [str(tail_lower), str(tail_upper)],
            "tight_root_parameter_bracket": [str(tight_lower), str(tight_upper)],
            "strict_overlap_before_tail_margin": str(tail_lower - outer_parameter[1]),
            "strict_corner_after_tight_lower_margin": str(corner_parameter[0] - tight_lower),
            "strict_corner_before_tight_upper_margin": str(tight_upper - corner_parameter[1]),
            "blown_up_graph_determinant_identity": "det D_(c0,t)(c0,Delta3)=partial_t_Delta3",
            "blown_up_graph_determinant_abs_lower_bound": str(dt_lower),
            "stereographic_q_denominator_lower_bound": str(q_denominator_lower),
            "continuous_edge_image_covers_tail_and_reaches_unique_corner": True,
            "coverage_theorem": "IVT_ON_CONTINUOUS_q_OF_UNIQUE_t(c0)_GRAPH",
            "q_of_c0_injectivity_installed": False,
            "physical_owner_order_on_edge_installed": False,
        })

    if len(seam_rows) != 8 or len(edge_rows) != 8 or set(r111_rows) != {row["exterior_port_id"] for row in seam_rows}:
        raise RuntimeError("eight-ray accounting")

    gap_atlas = [
        {
            "gate": "SOURCE_CHART_TRANSFER_SEAM",
            "status": "CLOSED_BY_CARTESIAN_MASTER_AND_FOUR_TABLE_UNION",
            "paid_count": 8,
            "remaining_count": 0,
        },
        {
            "gate": "SELECTED_LIFT_PRE_ROOT_TAIL_TO_UNIQUE_CORNER",
            "status": "PRE_ROOT_TAIL_COVERED_AND_UNIQUE_CORNER_ENCLOSED_INSIDE_TIGHT_NUMERICAL_BRACKET",
            "paid_count": 8,
            "remaining_count": 0,
        },
        {
            "gate": "ROOT_EDGE_PHYSICAL_OWNER_ORDER",
            "status": "OPEN__REQUIRES_COMPLETE_CANDIDATE_REPLAY_ON_ROOT_SHEETS",
            "paid_count": 0,
            "remaining_count": 8,
        },
        {
            "gate": "WHOLE_TRACE_NO_FOLD_AND_POSITIVE_REACH",
            "status": "OPEN__Q_IMAGE_COVERAGE_DOES_NOT_PROVE_INJECTIVITY_OR_NORMAL_REACH",
            "paid_count": 0,
            "remaining_count": 8,
        },
        {
            "gate": "WHOLE_TRACE_TWO_SIDED_COLLAR_SEPARATION",
            "status": "OPEN__NO_UNIFORM_DISTANCE_TO_ALL_OTHER_SINGULARITIES_OR_SEAMS",
            "paid_count": 0,
            "remaining_count": 8,
        },
    ]
    result = {
        "precision_bits": precision_bits,
        "input_corrected_ray_count": 8,
        "certified_source_chart_seam_bridge_count": len(seam_rows),
        "source_chart_seam_bridge_rows": seam_rows,
        "source_chart_seam_bridge_rows_sha256": digest(seam_rows),
        "certified_selected_lift_root_edge_stitch_count": len(edge_rows),
        "root_edge_stitch_rows": edge_rows,
        "root_edge_stitch_rows_sha256": digest(edge_rows),
        "selected_lift_end_to_end_trace_coverage_count": 8,
        "physical_owner_end_to_end_trace_closure_count": 0,
        "whole_trace_no_fold_atlas_count": 0,
        "whole_trace_positive_reach_certificate_count": 0,
        "whole_trace_uniform_other_singularity_separation_count": 0,
        "whole_trace_two_sided_physical_collar_count": 0,
        "whole_collar_complete_57_candidate_ordering_count": 0,
        "new_gate5_actual_child_field_count": 0,
        "gap_atlas": gap_atlas,
        "gap_atlas_sha256": digest(gap_atlas),
        "strict_scope": "eight Cartesian source-chart seam bridges plus selected-lift algebraic q-coverage from the certified pre-root chains to the unique shared blown-up HIT/BYPASS corners",
        "strict_nonclaims": [
            "the IVT edge stitch proves coverage, not injectivity or a no-fold q parameterisation",
            "the tight grazing parameter bracket encloses one unknown endpoint; it is not a physical trace interval whose every parameter must be covered",
            "the root-edge selected collision lift is not a complete first/second/third owner ordering",
            "the four-table seam bridge does not supply a positive-width transverse collar",
            "no uniform normal reach, chart-overlap width, or distance to every other singularity is installed along the whole trace",
            "the valid determinant is partial_t_Delta3 in blown-up (c0,t) coordinates; no (g0,Delta3) C1 Jacobian is claimed",
            "HIT and BYPASS remain separate real sheets sharing only c3=b3=0",
            "no homogeneity child, official word, or Gate5 field is installed",
        ],
        "strict_separator": {
            "selected_lift_algebraic_trace_coverage": "8/8",
            "physical_owner_trace_closure": "0/8",
            "whole_trace_two_sided_collar": "0/8",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "upstream_and_helper_pins": PINS,
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", type=int, default=PRECISION_BITS)
    args = parser.parse_args()
    print(json.dumps(build(args.precision), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
