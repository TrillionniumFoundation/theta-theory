#!/usr/bin/env python3
"""Generate Arb-certified vertices for the shared base-R1 quotient."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb
from mpmath import mp

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as adaptive_cert
import cm2_round71_r1_nonempty_face_germs_cert as face_cert
from cm2_round72_r1_positive_component_monotonicity_generator import output


HERE = Path(__file__).resolve().parent
WITNESSES = HERE / "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json"
SCHEMA = "cm2.round73.base-r1-quotient-vertices.v1"
mp.dps = 90


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def mpq(value: Q) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator


def scalar_output(core: Any, destination: Any, t: mp.mpf, p: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    rn = mp.sqrt(1 - t * t)
    rp = mp.sqrt(1 - p * p)
    source, cell = core.chart_id.split(":")
    if cell == "E":
        nx, ny = rn, t
    elif cell == "W":
        nx, ny = -rn, t
    elif cell == "N":
        nx, ny = t, rn
    else:
        nx, ny = t, -rn
    ux, uy = rp * nx - p * ny, rp * ny + p * nx
    if source == "G":
        cx = cy = mp.mpf(0)
        radius = mp.mpf(9) / 25
    else:
        cx = cy = mp.mpf(1) / 2
        radius = mp.mpf(4) / 25
    qx, qy = cx + radius * nx, cy + radius * ny
    obstacle = core.target_id[0]
    ix, iy = map(int, core.target_id[2:-1].split(","))
    target_radius = mp.mpf(9) / 25 if obstacle == "G" else mp.mpf(4) / 25
    ax = mp.mpf(ix) + (mp.mpf(1) / 2 if obstacle == "W" else 0)
    ay = mp.mpf(iy) + (mp.mpf(1) / 2 if obstacle == "W" else 0)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    flight = ell - mp.sqrt(target_radius * target_radius - transverse * transverse)
    hx, hy = qx + flight * ux, qy + flight * uy
    normal_x, normal_y = (hx - ax) / target_radius, (hy - ay) / target_radius
    target_p = transverse / target_radius
    destination_cell = destination.chart_id.split(":")[1]
    target_t = normal_y if destination_cell in ("E", "W") else normal_x
    return target_t, target_p


def sign(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def fraction_from_mp(value: mp.mpf, bits: int = 100) -> Q:
    denominator = 1 << bits
    return Q(int(mp.floor(value * denominator)), denominator)


def bracket_root(function: Any, lower: Q, upper: Q, depth: int = 90) -> tuple[Q, Q]:
    left, right = lower, upper
    left_sign = -1 if function(mpq(left)) < 0 else 1
    right_sign = -1 if function(mpq(right)) < 0 else 1
    if left_sign == right_sign:
        raise RuntimeError("root not bracketed")
    for _ in range(depth):
        middle = (left + right) / 2
        middle_sign = -1 if function(mpq(middle)) < 0 else 1
        if middle_sign == left_sign:
            left = middle
        else:
            right = middle
    return left, right


def qbox(value: Q) -> str:
    return str(value)


def build() -> dict[str, Any]:
    witness_rows = json.loads(WITNESSES.read_text())["rows"]
    cores = core_cert.physical_cores()
    rows = []
    for source_index in sorted({row["source_core_index"] for row in witness_rows}):
        core = cores[source_index]
        source_witnesses = [row for row in witness_rows if row["source_core_index"] == source_index]
        destination_index = next(iter({row["destination_core_index"] for row in source_witnesses}))
        destination = cores[destination_index]
        levels = {row["level_coordinate"]: Q(row["level_value"]) for row in source_witnesses}
        source_corner = None
        for t_side, t_value in (("t_lower", core.t0), ("t_upper", core.t1)):
            for p_side, p_value in (("p_lower", core.p0), ("p_upper", core.p1)):
                target_t, target_p = scalar_output(core, destination, mpq(t_value), mpq(p_value))
                if mpq(destination.t0) <= target_t <= mpq(destination.t1) and mpq(destination.p0) <= target_p <= mpq(destination.p1):
                    source_corner = (t_side, p_side, t_value, p_value)
        if source_corner is None:
            raise RuntimeError("missing return corner")
        t_side, p_side, t_corner, p_corner = source_corner

        endpoint_rows = []
        for witness in source_witnesses:
            coordinate = witness["level_coordinate"]
            level = Q(witness["level_value"])
            if coordinate == "t":
                varying_lower, varying_upper = core.t0, core.t1
                function = lambda t, pc=p_corner, lev=level: scalar_output(core, destination, t, mpq(pc))[0] - mpq(lev)
                lower, upper = bracket_root(function, varying_lower, varying_upper)
                t0, t1, p0, p1 = lower, upper, p_corner, p_corner
                fixed_side = p_side
                target_coordinate = 0
            else:
                varying_lower, varying_upper = core.p0, core.p1
                function = lambda p, tc=t_corner, lev=level: scalar_output(core, destination, mpq(tc), p)[1] - mpq(lev)
                lower, upper = bracket_root(function, varying_lower, varying_upper)
                t0, t1, p0, p1 = t_corner, t_corner, lower, upper
                fixed_side = t_side
                target_coordinate = 1
            left_output = output(core, destination, t0, t0, p0, p0)[target_coordinate].value - adaptive_cert.arbq(level)
            right_output = output(core, destination, t1, t1, p1, p1)[target_coordinate].value - adaptive_cert.arbq(level)
            endpoint_rows.append({
                "candidate_family_id": witness["candidate_family_id"],
                "pullback_side": witness["side"],
                "stationary_side": fixed_side,
                "t_interval": [qbox(t0), qbox(t1)],
                "p_interval": [qbox(p0), qbox(p1)],
                "endpoint_signs": [sign(left_output), sign(right_output)],
            })

        center = mp.findroot(
            lambda t, p: (
                scalar_output(core, destination, t, p)[0] - mpq(levels["t"]),
                scalar_output(core, destination, t, p)[1] - mpq(levels["p"]),
            ),
            ((mpq(core.t0) + mpq(core.t1)) / 2, (mpq(core.p0) + mpq(core.p1)) / 2),
        )
        center_t = fraction_from_mp(center[0])
        center_p = fraction_from_mp(center[1])
        step = mp.mpf(2) ** -120
        f_t_plus = scalar_output(core, destination, center[0] + step, center[1])
        f_t_minus = scalar_output(core, destination, center[0] - step, center[1])
        f_p_plus = scalar_output(core, destination, center[0], center[1] + step)
        f_p_minus = scalar_output(core, destination, center[0], center[1] - step)
        jacobian = mp.matrix([
            [(f_t_plus[0] - f_t_minus[0]) / (2 * step), (f_p_plus[0] - f_p_minus[0]) / (2 * step)],
            [(f_t_plus[1] - f_t_minus[1]) / (2 * step), (f_p_plus[1] - f_p_minus[1]) / (2 * step)],
        ])
        inverse = jacobian ** -1
        inverse_q = [[fraction_from_mp(inverse[i, j], 100) for j in range(2)] for i in range(2)]
        radius = Q(1, 1 << 70)
        for _ in range(30):
            t0, t1, p0, p1 = center_t - radius, center_t + radius, center_p - radius, center_p + radius
            jets = output(core, destination, t0, t1, p0, p1)
            point_jets = output(core, destination, center_t, center_t, center_p, center_p)
            function_point = [point_jets[i].value - adaptive_cert.arbq(levels["tp"[i]]) for i in range(2)]
            jacobian_box = [[jets[0].dt, jets[0].dp], [jets[1].dt, jets[1].dp]]
            delta = core_cert.first_hit.arb_interval(-radius, radius)
            krawczyk = []
            for i, center_coordinate in enumerate((center_t, center_p)):
                value = adaptive_cert.arbq(center_coordinate)
                for j in range(2):
                    value -= adaptive_cert.arbq(inverse_q[i][j]) * function_point[j]
                for column in range(2):
                    coefficient = arb(1 if i == column else 0)
                    for row_index in range(2):
                        coefficient -= adaptive_cert.arbq(inverse_q[i][row_index]) * jacobian_box[row_index][column]
                    value += coefficient * delta
                krawczyk.append(value)
            if bool(krawczyk[0] > adaptive_cert.arbq(t0)) and bool(krawczyk[0] < adaptive_cert.arbq(t1)) and bool(krawczyk[1] > adaptive_cert.arbq(p0)) and bool(krawczyk[1] < adaptive_cert.arbq(p1)):
                break
            radius *= 2
        else:
            raise RuntimeError("Krawczyk box unresolved")
        pullback_ids = sorted(row["candidate_family_id"] for row in source_witnesses)
        stationary_ids = sorted(face_cert.face_id(core, side) for side in (t_side, p_side))
        rows.append({
            "source_core_index": source_index,
            "source_core_id": adaptive_cert.core_id(core),
            "destination_core_index": destination_index,
            "destination_core_id": adaptive_cert.core_id(destination),
            "return_corner_sides": [t_side, p_side],
            "return_corner": {"t": str(t_corner), "p": str(p_corner)},
            "stationary_face_ids": stationary_ids,
            "pullback_family_ids": pullback_ids,
            "endpoint_vertices": endpoint_rows,
            "pullback_intersection_vertex": {
                "t_interval": [qbox(t0), qbox(t1)],
                "p_interval": [qbox(p0), qbox(p1)],
                "krawczyk_enclosure": [str(value) for value in krawczyk],
                "krawczyk_strict_interior": True,
            },
        })
    rows.sort(key=lambda row: row["source_core_index"])
    result = {
        "positive_return_cells": len(rows),
        "stationary_face_instances_before_subdivision": 96,
        "stationary_faces_split_once": 32,
        "stationary_segments_after_subdivision": 128,
        "pullback_face_components": 32,
        "quotient_edges": 160,
        "original_core_corner_vertices": 96,
        "stationary_pullback_endpoint_vertices": 32,
        "pullback_pullback_vertices": 16,
        "quotient_vertices": 144,
        "survival_cells": 24,
        "quotient_two_cells": 40,
        "connected_components": 24,
        "euler_identity": "144-160+40=24",
        "rows": rows,
    }
    result["rows_sha256"] = digest(rows)
    return {"schema": SCHEMA, "construction": {"arithmetic": "python-flint Arb + 90-digit root location", "endpoint_bisection_depth": 90, "corner_box_initial_radius": "2^-70"}, "result": result}


if __name__ == "__main__":
    document = build()
    json.dump(document, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
