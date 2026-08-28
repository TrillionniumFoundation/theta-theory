#!/usr/bin/env python3
"""Transfer all Round93 chart seams and continue them to source grazing."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round91_rank3_exterior_source_exit_cert as round91
import cm2_round92_rank3_competitor_event_isolation_cert as round92
import cm2_round93_rank3_full_source_chart_exit_cert as round93
from cm2_round79_tangency_intersection_generator import digest, strict_sign


HERE = Path(__file__).resolve().parent
ROUND93 = HERE / "cm2-round93-rank3-full-source-chart-exit-2026-07-22.json"
PINS = {
    ROUND93.name: "8a69487f962afe850eb15cc0a0d0b3faebe3c5cc50d6c93662e7a52b4285ccb3",
    "cm2_round93_rank3_full_source_chart_exit_cert.py": "cec3bc83ae2a9df015441ce72397c2d553a74baf2cab89946a220ee4debb1023",
}
SCHEMA = "cm2.round94.rank3-adjacent-chart-transfer.v1"
PRECISION_BITS = 512
ROOT_DEPTH = 96
PROBE_COUNT = 64
EVENT_SCAN_COUNT = 128


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def adjacent_chart(old_chart: str, seam_coordinate) -> str:
    positive = strict_sign(seam_coordinate) > 0
    if old_chart in ("E", "W"):
        return "N" if positive else "S"
    return "E" if positive else "W"


def inverse_state(source, branch, q_value):
    status, rows, _ = round91.reverse.reverse_target(
        source, branch[1], round91.tangent_target(branch, q_value, q_value)
    )
    if status != "INVERSE_PRESENT" or len(rows) != 1:
        return "SOURCE_GRAZING", status, None, None
    t_value, p_value = rows[0]
    chart_margin = 1 - 2 * t_value * t_value
    grazing_margin = 1 - p_value * p_value
    if strict_sign(chart_margin) < 0:
        return "SOURCE_CHART_SEAM", status, t_value, p_value
    if strict_sign(grazing_margin) < 0:
        return "SOURCE_GRAZING", status, t_value, p_value
    if strict_sign(chart_margin) == 0 or strict_sign(grazing_margin) == 0:
        return "UNRESOLVED_BOUNDARY", status, t_value, p_value
    return "INTERIOR", status, t_value, p_value


def isolate_next_event(source, branch, q0, direction, start):
    lower = start
    if inverse_state(source, branch, q0 + direction * lower)[0] != "INTERIOR":
        raise RuntimeError("transferred chart start")
    step = max(Q(1, 10**8), start / 16)
    upper = lower + step
    while upper < 2 and inverse_state(source, branch, q0 + direction * upper)[0] == "INTERIOR":
        lower, step = upper, 2 * step
        upper = lower + step
    if upper >= 2:
        raise RuntimeError("no transferred event")
    event = inverse_state(source, branch, q0 + direction * upper)[0]
    for _ in range(ROOT_DEPTH):
        middle = (lower + upper) / 2
        if inverse_state(source, branch, q0 + direction * middle)[0] == "INTERIOR":
            lower = middle
        else:
            upper = middle
    return lower, upper, event, inverse_state(source, branch, q0 + direction * lower), inverse_state(source, branch, q0 + direction * upper)


def physical_point(source, source_index, branch, q_value, cores):
    status, rows, _ = round91.reverse.reverse_target(
        source, branch[1], round91.tangent_target(branch, q_value, q_value)
    )
    if status != "INVERSE_PRESENT" or len(rows) != 1:
        raise RuntimeError("point inverse")
    t_value, p_value = rows[0]
    t_lower, t_upper = round91.arb_bounds(t_value)
    p_lower, p_upper = round91.arb_bounds(p_value)
    atom = step1.Atom(source_index, source, t_lower, t_upper, p_lower, p_upper, Q(0), Q(0), "round94")
    first_hit.certify_first_hit_patch(atom.phase_box, source.target_id)
    _, _, _, state1, owner2 = time3.homogeneity_cert.classify_with_geometry(atom, cores)
    if state1 is None or owner2 is None or owner2["selected_target_id"] != branch[1]:
        raise RuntimeError("second owner")
    state2 = time3.second_outgoing_state(atom, state1, owner2)
    if state2 is None:
        raise RuntimeError("second state")
    box = (t_lower, t_upper, p_lower, p_upper)
    physical_status, transverse_sign, competitor_rows, repairs = round92.centered_physical_type(
        state2, source, branch[1], branch[2], box
    )
    if transverse_sign != branch[3]:
        raise RuntimeError("transverse branch sign")
    return {
        "status": physical_status,
        "t": str(t_value),
        "p": str(p_value),
        "strictly_earlier_competitor_ids": sorted(row[0] for row in competitor_rows if row[2] == "STRICTLY_BEFORE_TANGENT_TARGET"),
        "competitor_rows_sha256": digest(competitor_rows),
        "repair_rows_sha256": digest(repairs),
    }


def build(precision_bits: int = PRECISION_BITS):
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    frozen = json.loads(ROUND93.read_text())["result"]
    frozen_by_port = {row["exterior_port_id"]: row for row in frozen["ray_rows"]}
    events, _ = round89.load()
    physical = {row["registered_port_id"]: row for row in events if row["port_is_locally_physical_third_tangency"]}
    cores = core_cert.physical_cores()
    round91.round87.WORK_CORES = cores
    rows = []
    for branch, side, port_id in round93.rays(physical):
        if frozen_by_port[port_id]["terminal_event_type"] != "SOURCE_CHART_SEAM":
            continue
        q0, direction, _, _, seam_outer, _, old_inner, _ = round93.isolate_event(branch, side, port_id, physical, cores)
        source = cores[branch[0]]
        old_chart = source.chart_id.split(":")[1]
        new_chart = adjacent_chart(old_chart, old_inner[2])
        transferred_source = replace(source, chart_id=f"{source.source}:{new_chart}")
        transferred_state = inverse_state(transferred_source, branch, q0 + direction * seam_outer)
        if transferred_state[0] != "INTERIOR":
            raise RuntimeError("adjacent chart transfer")
        grazing_inner, grazing_outer, event, inner_state, outer_state = isolate_next_event(
            transferred_source, branch, q0, direction, seam_outer
        )
        if event != "SOURCE_GRAZING" or outer_state[0] == "INTERIOR":
            raise RuntimeError("transferred terminal event")
        physical_status = "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
        event_lower = seam_outer
        event_upper = grazing_inner
        post_event_status = "SOURCE_GRAZING"
        previous = seam_outer
        for index in range(1, EVENT_SCAN_COUNT + 1):
            parameter = seam_outer + (grazing_inner - seam_outer) * Q(index, EVENT_SCAN_COUNT + 1)
            point = physical_point(transferred_source, branch[0], branch, q0 + direction * parameter, cores)
            if point["status"] != physical_status:
                event_lower, event_upper = previous, parameter
                post_event_status = point["status"]
                break
            previous = parameter
        if post_event_status != "SOURCE_GRAZING":
            for _ in range(ROOT_DEPTH):
                middle = (event_lower + event_upper) / 2
                point = physical_point(transferred_source, branch[0], branch, q0 + direction * middle, cores)
                if point["status"] == physical_status:
                    event_lower = middle
                else:
                    event_upper = middle
                    post_event_status = point["status"]
        post_event_point = None if post_event_status == "SOURCE_GRAZING" else physical_point(
            transferred_source, branch[0], branch, q0 + direction * event_upper, cores
        )
        probes = []
        for index in range(1, PROBE_COUNT + 1):
            parameter = seam_outer + (event_lower - seam_outer) * Q(index, PROBE_COUNT + 1)
            point = physical_point(transferred_source, branch[0], branch, q0 + direction * parameter, cores)
            if point["status"] != physical_status:
                raise RuntimeError("physical transferred prefix probe")
            probes.append(point)
        rows.append({
            "exterior_port_id": port_id,
            "branch_key": list(branch),
            "projective_end": side,
            "old_source_chart": old_chart,
            "adjacent_source_chart": new_chart,
            "seam_transfer_status": "INVERSE_PRESENT_IN_UNIQUE_ADJACENT_CHART",
            "algebraic_transferred_terminal_event_type": event,
            "transferred_grazing_parameter_bracket": [str(grazing_inner), str(grazing_outer)],
            "transferred_inner_t_enclosure": str(inner_state[2]),
            "transferred_inner_p_enclosure": str(inner_state[3]),
            "transferred_outer_reverse_status": outer_state[1],
            "first_physical_terminal_event_type": post_event_status,
            "first_physical_terminal_event_parameter_bracket": [str(event_lower), str(event_upper)],
            "occluding_competitor_ids": [] if post_event_point is None else post_event_point["strictly_earlier_competitor_ids"],
            "strict_transferred_physical_prefix_probe_count": len(probes),
            "transferred_point_probe_rows_sha256": digest(probes),
        })
    histogram = Counter((row["old_source_chart"], row["adjacent_source_chart"]) for row in rows)
    result = {
        "precision_bits": precision_bits,
        "input_round93_chart_seam_count": 28,
        "certified_unique_adjacent_chart_transfer_count": len(rows),
        "algebraic_transferred_source_grazing_count": sum(row["algebraic_transferred_terminal_event_type"] == "SOURCE_GRAZING" for row in rows),
        "second_chart_seam_count": sum(row["algebraic_transferred_terminal_event_type"] == "SOURCE_CHART_SEAM" for row in rows),
        "strict_transferred_physical_prefix_probe_total": sum(row["strict_transferred_physical_prefix_probe_count"] for row in rows),
        "physical_terminal_event_histogram": dict(sorted(Counter(row["first_physical_terminal_event_type"] for row in rows).items())),
        "chart_transfer_histogram": {f"{old}->{new}": count for (old, new), count in sorted(histogram.items())},
        "transfer_rows": rows,
        "transfer_rows_sha256": digest(rows),
        "strict_scope": "unique adjacent-chart transfer of all Round93 seam rays and strict continuation diagnostics to source grazing",
        "strict_nonclaims": ["whole open intervals between strict probes still require centered-Taylor coverage", "no complete physical-face quotient or gate field is installed"],
        "upstream_pins": PINS,
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2))
