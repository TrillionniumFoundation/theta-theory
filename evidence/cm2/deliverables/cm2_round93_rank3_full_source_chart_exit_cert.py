#!/usr/bin/env python3
"""Isolate the first full source-chart event on all Round92 exterior rays."""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round91_rank3_exterior_source_exit_cert as round91
import cm2_round92_rank3_competitor_event_isolation_cert as round92
from cm2_round79_tangency_intersection_generator import digest, strict_sign


HERE = Path(__file__).resolve().parent
ROUND90 = HERE / "cm2-round90-rank3-tracked-residual-gap-closure-2026-07-22.json"
PINS = {
    "cm2_round91_rank3_exterior_source_exit_cert.py": "d75eb3a9a6aeca2c45b5b9eaa487c32481d4a9cf7e3da04c5d45d6f9a79414da",
    "cm2_round92_rank3_competitor_event_isolation_cert.py": "90527519cc66c1a5fa3a2c8336f97c29994ed893c4508ad370247fd542ccdd50",
    ROUND90.name: "7a121a5348e71136e82981fb9d5fed165faf3a3cab23d35a1b2b434536fa5323",
}
SCHEMA = "cm2.round93.rank3-full-source-chart-exit.v1"
PRECISION_BITS = 512
ROOT_DEPTH = 112
PROBE_COUNT = 128


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rays(physical: dict[str, Any]) -> list[tuple[tuple[int, str, str, int], str, str]]:
    frozen = json.loads(ROUND90.read_text())["result"]
    capped = {(tuple(row["branch_key"]), row["projective_end"]) for row in frozen["source_cap_rows"]}
    grouped: defaultdict[tuple[int, str, str, int], list[str]] = defaultdict(list)
    for port_id, row in physical.items():
        grouped[round89.key(row)].append(port_id)
    result = []
    for branch, port_ids in sorted(grouped.items()):
        port_ids.sort(key=lambda port_id: float(round89.qball(physical[port_id]).mid()))
        for side, port_id in (("LEFT_PROJECTIVE_END", port_ids[0]), ("RIGHT_PROJECTIVE_END", port_ids[-1])):
            if (branch, side) not in capped:
                result.append((branch, side, port_id))
    if len(result) != 65:
        raise RuntimeError("exterior ray accounting")
    return result


def inverse_point(branch, q, cores):
    status, rows, _ = round91.reverse.reverse_target(
        cores[branch[0]], branch[1], round91.tangent_target(branch, q, q)
    )
    if status != "INVERSE_PRESENT" or len(rows) != 1:
        return status, None, None
    return status, rows[0][0], rows[0][1]


def full_chart_state(branch, q, cores):
    status, t_value, p_value = inverse_point(branch, q, cores)
    if status != "INVERSE_PRESENT":
        return "SOURCE_GRAZING", status, t_value, p_value
    chart_margin = 1 - 2 * t_value * t_value
    grazing_margin = 1 - p_value * p_value
    if strict_sign(chart_margin) < 0:
        return "SOURCE_CHART_SEAM", status, t_value, p_value
    if strict_sign(grazing_margin) < 0:
        return "SOURCE_GRAZING", status, t_value, p_value
    if strict_sign(chart_margin) == 0 or strict_sign(grazing_margin) == 0:
        return "UNRESOLVED_BOUNDARY", status, t_value, p_value
    return "INTERIOR", status, t_value, p_value


def isolate_event(branch, side, port_id, physical, cores):
    q0, direction, core_exit = round92.ray_geometry(branch, side, port_id, physical, cores)
    lower = core_exit
    if full_chart_state(branch, q0 + direction * lower, cores)[0] != "INTERIOR":
        raise RuntimeError("core exit is not full-chart interior")
    step = max(Q(1, 10**8), core_exit / 16)
    upper = lower + step
    while upper < 2 and full_chart_state(branch, q0 + direction * upper, cores)[0] == "INTERIOR":
        lower, step = upper, 2 * step
        upper = lower + step
    if upper >= 2:
        raise RuntimeError("no full-chart event")
    event_kind = full_chart_state(branch, q0 + direction * upper, cores)[0]
    if event_kind not in {"SOURCE_CHART_SEAM", "SOURCE_GRAZING"}:
        raise RuntimeError(f"untyped full-chart event: {event_kind}")
    for _ in range(ROOT_DEPTH):
        middle = (lower + upper) / 2
        state = full_chart_state(branch, q0 + direction * middle, cores)[0]
        if state == "INTERIOR":
            lower = middle
        else:
            upper = middle
    inner = full_chart_state(branch, q0 + direction * lower, cores)
    outer = full_chart_state(branch, q0 + direction * upper, cores)
    if inner[0] != "INTERIOR" or outer[0] == "INTERIOR":
        raise RuntimeError("event bracket")
    return q0, direction, core_exit, lower, upper, event_kind, inner, outer


def certify_box(branch, qa, qb, cores):
    box = round91.inverse_box(branch, min(qa, qb), max(qa, qb), cores)
    source = cores[branch[0]]
    atom = step1.Atom(branch[0], source, *box, Q(0), Q(0), "round93")
    first_hit.certify_first_hit_patch(atom.phase_box, source.target_id)
    classification, _, destination, state1, owner2 = time3.homogeneity_cert.classify_with_geometry(atom, cores)
    if classification != "SURVIVE_THROUGH_2_INNER" or destination is not None:
        raise RuntimeError("unexpected frozen-core return")
    if state1 is None or owner2 is None or owner2["selected_target_id"] != branch[1]:
        raise RuntimeError("second owner")
    state2 = time3.second_outgoing_state(atom, state1, owner2)
    if state2 is None:
        raise RuntimeError("second outgoing state")
    status, transverse_sign, rows, repairs = round92.centered_physical_type(
        state2, source, branch[1], branch[2], box
    )
    if status != "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION" or transverse_sign != branch[3]:
        raise RuntimeError(status)
    return box, rows, repairs


def certify_ray(branch, side, port_id, physical, cores):
    q0, direction, core_exit, inner, outer, event_kind, inner_state, outer_state = isolate_event(
        branch, side, port_id, physical, cores
    )
    probes = []
    for index in range(1, PROBE_COUNT + 1):
        parameter = core_exit + (inner - core_exit) * Q(index, PROBE_COUNT + 1)
        q_value = q0 + direction * parameter
        box, rows, repairs = certify_box(branch, q_value, q_value, cores)
        probes.append((index, list(map(str, box)), digest(rows), digest(repairs)))
    return {
        "exterior_port_id": port_id,
        "branch_key": list(branch),
        "projective_end": side,
        "terminal_event_type": event_kind,
        "event_parameter_bracket": [str(inner), str(outer)],
        "event_root_bisection_depth": ROOT_DEPTH,
        "inner_t_enclosure": str(inner_state[2]),
        "inner_p_enclosure": str(inner_state[3]),
        "outer_reverse_status": outer_state[1],
        "strict_point_probe_count": len(probes),
        "point_probe_rows_sha256": digest(probes),
        "whole_open_ray_status": "ENDPOINT_ISOLATED__DENSE_POINT_PROBES_PHYSICAL__INTERVAL_BRIDGE_OPEN",
    }


def build(precision_bits: int = PRECISION_BITS):
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    events, _ = round89.load()
    physical = {
        row["registered_port_id"]: row
        for row in events
        if row["port_is_locally_physical_third_tangency"]
    }
    cores = core_cert.physical_cores()
    round91.round87.WORK_CORES = cores
    rows = [certify_ray(branch, side, port_id, physical, cores) for branch, side, port_id in rays(physical)]
    histogram = Counter(row["terminal_event_type"] for row in rows)
    result = {
        "precision_bits": precision_bits,
        "input_round92_frozen_core_exit_ray_count": 65,
        "certified_first_full_source_chart_event_count": len(rows),
        "terminal_event_type_histogram": dict(sorted(histogram.items())),
        "remaining_untyped_full_source_chart_ray_count": 65 - len(rows),
        "ray_rows": rows,
        "ray_rows_sha256": digest(rows),
        "strict_scope": "first source-chart event isolation plus 128 strict physical point probes on each of all 65 exterior rank-three rays",
        "strict_nonclaims": [
            "the open intervals between point probes are not yet covered by one interval/Taylor chain",
            "chart-seam continuations in adjacent charts are not yet glued",
            "no complete physical-face quotient, RN row, or Gate5 field is installed",
        ],
        "upstream_pins": PINS,
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main():
    json.dump(build(), __import__("sys").stdout, sort_keys=True, indent=2)
    print()


if __name__ == "__main__":
    main()
