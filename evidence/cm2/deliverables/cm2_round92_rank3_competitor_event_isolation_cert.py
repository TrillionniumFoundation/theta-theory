#!/usr/bin/env python3
"""Isolate the four Round91 exterior competitor-discriminant events."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round87_rank3_port_event_continuation_cert as round87
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round91_rank3_exterior_source_exit_cert as round91
from cm2_round79_tangency_intersection_generator import aq, digest, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet

HERE = Path(__file__).resolve().parent
ROUND91 = HERE / "cm2-round91-rank3-exterior-source-exit-2026-07-22.json"
SCHEMA = "cm2.round92.rank3-competitor-event-isolation.v1"
PRECISION_BITS = 512
PINS = {
    ROUND91.name: "c82c516edb4254116421e878ea470b3febfe9dfce506b94ff6346359dbdc16b0",
    "cm2_round91_rank3_exterior_source_exit_cert.py": "d75eb3a9a6aeca2c45b5b9eaa487c32481d4a9cf7e3da04c5d45d6f9a79414da",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def point_state2(branch, q: Q, cores):
    box = round91.inverse_box(branch, q, q, cores)
    core = cores[branch[0]]
    atom = step1.Atom(branch[0], core, *box, Q(0), Q(0), f"round92:{q}")
    classification, _, destination, state1, owner2 = (
        time3.homogeneity_cert.classify_with_geometry(atom, cores)
    )
    if (
        classification != "SURVIVE_THROUGH_2_INNER"
        or destination is not None
        or owner2 is None
        or owner2["selected_target_id"] != branch[1]
    ):
        raise RuntimeError("point two-collision owner")
    state2 = time3.second_outgoing_state(atom, state1, owner2)
    if state2 is None:
        raise RuntimeError("point second state")
    return box, state2


def discriminant(state2, candidate: str) -> arb:
    cx, cy = time3.time2_cert.target_center(candidate, state2["s"])
    dx, dy = cx - state2["contact_x"], cy - state2["contact_y"]
    transverse = -state2["outgoing_y"] * dx + state2["outgoing_x"] * dy
    radius = aq(Q(9, 25) if candidate[0] == "G" else Q(4, 25))
    return radius * radius - transverse * transverse


def centered_discriminant(source, second: str, candidate: str, box):
    t0, t1, p0, p1 = box
    tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
    point = third_tangency_jet(source, second, candidate, tc, tc, pc, pc)
    full = third_tangency_jet(source, second, candidate, *box)
    tr, pr = (t1 - t0) / 2, (p1 - p0) / 2
    return (
        point.value
        + full.gradient[0] * arb(0, aq(tr).upper())
        + full.gradient[1] * arb(0, aq(pr).upper())
    )


def centered_competitor_rows(state2, source, second, tangent_target, tangent_flight, box):
    candidate_ids = time3.time2_cert.translated_candidate_ids(second, state2["chart"])
    if tangent_target not in candidate_ids:
        raise RuntimeError("tangent candidate absent")
    rows = []
    future = []
    centered_repairs = []
    for candidate_id in candidate_ids:
        if candidate_id == tangent_target:
            continue
        candidate = time3.time2_cert.candidate_root(
            state2["contact_x"], state2["contact_y"],
            state2["outgoing_x"], state2["outgoing_y"],
            state2["s"], candidate_id,
        )
        classification = candidate["classification"]
        if classification == "unresolved_discriminant":
            tight = centered_discriminant(source, second, candidate_id, box)
            tight_sign = strict_sign(tight)
            if tight_sign < 0:
                classification = "no_real_intersection"
            elif tight_sign > 0:
                cx, cy = time3.time2_cert.target_center(candidate_id, state2["s"])
                dx, dy = cx - state2["contact_x"], cy - state2["contact_y"]
                ell = state2["outgoing_x"] * dx + state2["outgoing_y"] * dy
                radical = tight.sqrt()
                near, far = ell - radical, ell + radical
                if bool(far < 0):
                    classification = "intersection_strictly_behind"
                elif bool(near > 0):
                    classification = "strict_future_near_root"
                    candidate = {"classification": classification, "near": near}
                else:
                    raise RuntimeError("centered unresolved root sign")
            else:
                raise RuntimeError(f"centered unresolved discriminant:{candidate_id}:{tight}")
            centered_repairs.append((candidate_id, tight_sign, str(tight)))
        if classification == "no_real_intersection":
            relation = "NO_REAL_INTERSECTION"
        elif classification == "intersection_strictly_behind":
            relation = "INTERSECTION_STRICTLY_BEHIND"
        elif classification == "strict_future_near_root":
            near = candidate["near"]
            if bool(near < tangent_flight):
                relation = "STRICTLY_BEFORE_TANGENT_TARGET"
            elif bool(tangent_flight < near):
                relation = "STRICTLY_AFTER_TANGENT_TARGET"
            else:
                raise RuntimeError("centered unresolved competitor order")
            future.append((candidate_id, near))
        else:
            raise RuntimeError(f"centered unresolved candidate: {classification}")
        rows.append((candidate_id, classification, relation))
    winner = None
    for candidate_id, near in future:
        if all(candidate_id == other or bool(near < other_near) for other, other_near in future):
            if winner is not None:
                raise RuntimeError("centered nonunique winner")
            winner = candidate_id
    if future and winner is None:
        raise RuntimeError("centered unresolved winner")
    return rows, winner, centered_repairs


def centered_physical_type(state2, source, second, tangent_target, box):
    cx, cy = time3.time2_cert.target_center(tangent_target, state2["s"])
    dx, dy = cx - state2["contact_x"], cy - state2["contact_y"]
    ux, uy = state2["outgoing_x"], state2["outgoing_y"]
    tangent_flight = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    flight_sign, transverse_sign = strict_sign(tangent_flight), strict_sign(transverse)
    if flight_sign == 0 or transverse_sign == 0:
        raise RuntimeError("target tangent signs")
    rows, winner, repairs = centered_competitor_rows(
        state2, source, second, tangent_target, tangent_flight, box
    )
    tau_max = aq(time3.time2_cert.step1.first_hit.TAU_MAX)
    if flight_sign < 0:
        status = "ALGEBRAIC_TANGENCY_STRICTLY_BEHIND_SECOND__LOCAL_CONTINUATION"
    elif bool(tangent_flight > tau_max):
        status = "ALGEBRAIC_TANGENCY_STRICTLY_AFTER_TAU_MAX__LOCAL_CONTINUATION"
    elif bool(tangent_flight < tau_max):
        before = [candidate for candidate, _, relation in rows if relation == "STRICTLY_BEFORE_TANGENT_TARGET"]
        if before:
            if winner not in before:
                raise RuntimeError("centered occluding winner")
            status = "ALGEBRAIC_TANGENCY_OCCLUDED_BY_EARLIER_THIRD_OWNER__LOCAL_CONTINUATION"
        else:
            status = "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
    else:
        raise RuntimeError("target tau event")
    return status, transverse_sign, rows, repairs


def ray_geometry(branch, side, port_id, physical, cores):
    q0 = round91.q_mid(physical[port_id])
    direction = -1 if side == "LEFT_PROJECTIVE_END" else 1
    start = round91.margins(branch, q0, cores)
    if any(strict_sign(value) != 1 for value in start):
        raise RuntimeError("ray start")
    outside_step = None
    outside = None
    for exponent in range(-12, 3):
        step = Q(10) ** exponent
        candidate = round91.margins(branch, q0 + direction * step, cores)
        if any(strict_sign(value) == -1 for value in candidate):
            outside_step, outside = step, candidate
            break
    if outside_step is None:
        raise RuntimeError("source exit search")
    roots = []
    for index, value in enumerate(outside):
        if strict_sign(value) != -1:
            continue
        lower, upper = Q(0), outside_step
        for _ in range(112):
            middle = (lower + upper) / 2
            sign = strict_sign(
                round91.margins(branch, q0 + direction * middle, cores)[index]
            )
            if sign == 0:
                raise RuntimeError("source root bisection")
            if sign == 1:
                lower = middle
            else:
                upper = middle
        roots.append((lower, upper, index))
    roots.sort(key=lambda row: row[0])
    return q0, direction, roots[0][0]


def event_probe(branch, side, port_id, physical, cores):
    q0, direction, exit_lower = ray_geometry(
        branch, side, port_id, physical, cores
    )
    _, initial_state = point_state2(branch, q0, cores)
    candidates = [
        candidate
        for candidate in time3.time2_cert.translated_candidate_ids(
            branch[1], initial_state["chart"]
        )
        if candidate != branch[2]
    ]
    transitions = []
    minima = {}
    subdivisions = 512
    previous = {}
    for index in range(subdivisions + 1):
        x = exit_lower * Q(index, subdivisions)
        q = q0 + direction * x
        _, state2 = point_state2(branch, q, cores)
        for candidate in candidates:
            value = discriminant(state2, candidate)
            sign = strict_sign(value)
            magnitude = abs(float(value.mid()))
            if candidate not in minima or magnitude < minima[candidate][0]:
                minima[candidate] = (magnitude, x, str(value), sign)
            if sign == 0:
                continue
            if candidate in previous and previous[candidate][1] != sign:
                transitions.append(
                    (previous[candidate][0], x, candidate, previous[candidate][1], sign)
                )
            previous[candidate] = (x, sign)
    if not transitions:
        candidate, minimum = min(minima.items(), key=lambda item: item[1][0])
        return {
            "exterior_port_id": port_id,
            "branch_key": list(branch),
            "projective_end": side,
            "probe_status": "NO_POINT_SIGN_TRANSITION",
            "closest_competitor_candidate_id": candidate,
            "closest_parameter": str(minimum[1]),
            "closest_discriminant_enclosure": minimum[2],
            "closest_discriminant_sign": minimum[3],
        }
    transitions.sort(key=lambda row: row[0])
    lower, upper, competitor, lower_sign, upper_sign = transitions[0]
    for _ in range(112):
        middle = (lower + upper) / 2
        _, state2 = point_state2(branch, q0 + direction * middle, cores)
        sign = strict_sign(discriminant(state2, competitor))
        if sign == 0:
            raise RuntimeError("event root bisection indeterminate")
        if sign == lower_sign:
            lower = middle
        else:
            upper = middle
    qa, qb = q0 + direction * lower, q0 + direction * upper
    event_box = round91.inverse_box(branch, min(qa, qb), max(qa, qb), cores)
    target_jet = third_tangency_jet(
        cores[branch[0]], branch[1], branch[2], *event_box
    )
    competitor_jet = third_tangency_jet(
        cores[branch[0]], branch[1], competitor, *event_box
    )
    determinant = (
        target_jet.gradient[0] * competitor_jet.gradient[1]
        - target_jet.gradient[1] * competitor_jet.gradient[0]
    )
    determinant_sign = strict_sign(determinant)
    return {
        "exterior_port_id": port_id,
        "branch_key": list(branch),
        "projective_end": side,
        "competitor_candidate_id": competitor,
        "discriminant_sign_before_event": lower_sign,
        "discriminant_sign_after_event": upper_sign,
        "event_parameter_bracket": [str(lower), str(upper)],
        "event_source_box": [str(value) for value in event_box],
        "event_root_bisection_depth": 112,
        "two_curve_jacobian_determinant_sign": determinant_sign,
        "probe_status": "STRICT_POINT_SIGN_TRANSITION",
        "event_box_target_function_enclosure": str(target_jet.value),
        "event_box_competitor_function_enclosure": str(competitor_jet.value),
    }


def certify_centered_ray(branch, side, port_id, physical, cores):
    q0, direction, exit_lower = ray_geometry(branch, side, port_id, physical, cores)
    source = cores[branch[0]]
    last = "NO_ATTEMPT"
    strip_options = (65536,) if branch[0] == 14 else (32768,)
    for strips in strip_options:
        boxes = []
        repair_rows = []
        competitor_rows = []
        ok = True
        for index in range(strips):
            xa, xb = exit_lower * Q(index, strips), exit_lower * Q(index + 1, strips)
            qa, qb = q0 + direction * xa, q0 + direction * xb
            try:
                box = round91.inverse_box(branch, min(qa, qb), max(qa, qb), cores)
                box = (
                    max(box[0], source.t0), min(box[1], source.t1),
                    max(box[2], source.p0), min(box[3], source.p1),
                )
                atom = step1.Atom(branch[0], source, *box, Q(0), Q(0), f"round92:{strips}:{index}")
                classification, _, destination, state1, owner2 = time3.homogeneity_cert.classify_with_geometry(atom, cores)
                if classification != "SURVIVE_THROUGH_2_INNER" or destination is not None or owner2 is None or owner2["selected_target_id"] != branch[1]:
                    raise RuntimeError("two-collision owner")
                state2 = time3.second_outgoing_state(atom, state1, owner2)
                if state2 is None:
                    raise RuntimeError("second state")
                status, sign, rows, repairs = centered_physical_type(
                    state2, source, branch[1], branch[2], box
                )
                if status != "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION" or sign != branch[3]:
                    raise RuntimeError(status)
            except (RuntimeError, ValueError, ZeroDivisionError) as exc:
                last = f"strip={strips}:index={index}:" + str(exc)
                ok = False
                break
            boxes.append(list(map(str, box)))
            repair_rows.extend((index, *row) for row in repairs)
            competitor_rows.append(rows)
        if ok:
            return {
                "exterior_port_id": port_id,
                "branch_key": list(branch),
                "projective_end": side,
                "centered_chain_strip_count": strips,
                "centered_discriminant_repair_count": len(repair_rows),
                "centered_discriminant_repair_rows_sha256": digest(repair_rows),
                "competitor_rows_sha256": digest(competitor_rows),
                "chain_boxes_sha256": digest(boxes),
                "whole_open_ray_status": "PHYSICAL_NEXT_TANGENCY_UNTIL_SOURCE_CORE_EXIT__CENTERED_TAYLOR_REPAIRED",
            }
    raise RuntimeError(f"centered ray unresolved: {last}")


def build(precision_bits: int = PRECISION_BITS):
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    frozen = json.loads(ROUND91.read_text())["result"]
    events, _ = round89.load()
    physical = {
        row["registered_port_id"]: row
        for row in events
        if row["port_is_locally_physical_third_tangency"]
    }
    cores = core_cert.physical_cores()
    round87.WORK_CORES = cores
    diagnostic_rows = []
    closure_rows = []
    for residual in frozen["unresolved_ray_rows"]:
        branch = tuple(residual["branch_key"])
        diagnostic_rows.append(
            event_probe(
                branch,
                residual["projective_end"],
                residual["exterior_port_id"],
                physical,
                cores,
            )
        )
        closure_rows.append(
            certify_centered_ray(
                branch,
                residual["projective_end"],
                residual["exterior_port_id"],
                physical,
                cores,
            )
        )
    result = {
        "precision_bits": precision_bits,
        "input_round91_residual_ray_count": 4,
        "strict_discriminant_transition_count": sum(row["probe_status"] == "STRICT_POINT_SIGN_TRANSITION" for row in diagnostic_rows),
        "no_point_discriminant_sign_transition_count": sum(row["probe_status"] == "NO_POINT_SIGN_TRANSITION" for row in diagnostic_rows),
        "nonzero_two_curve_jacobian_count": sum(
            row.get("two_curve_jacobian_determinant_sign", 0) != 0 for row in diagnostic_rows
        ),
        "diagnostic_rows": diagnostic_rows,
        "diagnostic_rows_sha256": digest(diagnostic_rows),
        "centered_taylor_closed_residual_ray_count": len(closure_rows),
        "combined_round91_round92_source_exit_ray_count": 61 + len(closure_rows),
        "remaining_exterior_ray_within_frozen_source_cores_count": 4 - len(closure_rows),
        "closure_rows": closure_rows,
        "closure_rows_sha256": digest(closure_rows),
        "strict_scope": "centered-Taylor repair of the four Round91 interval-dependency residual rays through their first frozen source-core boundary",
        "strict_nonclaims": [
            "source-core boundaries remain frozen-domain boundaries rather than global physical-face endpoints",
            "no continuation beyond the source-core registry or RN/Gate5 installation is asserted",
        ],
        "upstream_pins": PINS,
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main():
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
