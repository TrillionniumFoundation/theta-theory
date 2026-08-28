#!/usr/bin/env python3
"""Generalized interval-Newton continuation of the 32 physical R2 faces."""
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
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round26_q1_time2_frontier_cert as time2
from cm2_round72_r1_positive_component_monotonicity_generator import Jet


HERE = Path(__file__).resolve().parent
WITNESSES = HERE / "cm2-round74-s0-r2-pair-witnesses-2026-07-21.json"
SCHEMA = "cm2.round75.r2-physical-curves.v1"
mp.dps = 90


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def aq(value: Q) -> arb:
    return step1.arbq(value)


def interval(lower: Q, upper: Q) -> arb:
    return core_cert.first_hit.arb_interval(lower, upper)


def t2_output(core: Any, destination: Any, t0: Q, t1: Q, p0: Q, p1: Q) -> dict[str, Jet]:
    t = Jet(interval(t0, t1), arb(1), arb(0))
    p = Jet(interval(p0, p1), arb(0), arb(1))
    one = arb(1)
    normal_radial = (one - t * t).sqrt()
    velocity_radial = (one - p * p).sqrt()
    cell = core.chart_id.split(":")[1]
    if cell == "E":
        normal_x, normal_y = normal_radial, t
    elif cell == "W":
        normal_x, normal_y = -normal_radial, t
    elif cell == "N":
        normal_x, normal_y = t, normal_radial
    else:
        normal_x, normal_y = t, -normal_radial
    velocity_x = velocity_radial * normal_x - p * normal_y
    velocity_y = velocity_radial * normal_y + p * normal_x
    source_radius = aq(Q(4, 25))
    source_center = aq(Q(1, 2))
    point_x = source_center + source_radius * normal_x
    point_y = source_center + source_radius * normal_y
    first_ix, first_iy = map(int, core.target_id[2:-1].split(","))
    first_radius = aq(Q(9, 25))
    dx, dy = arb(first_ix) - point_x, arb(first_iy) - point_y
    ell = velocity_x * dx + velocity_y * dy
    transverse = -velocity_y * dx + velocity_x * dy
    radical = (first_radius * first_radius - transverse * transverse).sqrt()
    flight = ell - radical
    hit_x, hit_y = point_x + flight * velocity_x, point_y + flight * velocity_y
    first_normal_x = (hit_x - arb(first_ix)) / first_radius
    first_normal_y = (hit_y - arb(first_iy)) / first_radius
    first_p = transverse / first_radius
    outgoing_radial = (one - first_p * first_p).sqrt()
    outgoing_x = outgoing_radial * first_normal_x - first_p * first_normal_y
    outgoing_y = outgoing_radial * first_normal_y + first_p * first_normal_x
    second_radius = aq(Q(4, 25))
    dx2, dy2 = source_center - hit_x, source_center - hit_y
    ell2 = outgoing_x * dx2 + outgoing_y * dy2
    transverse2 = -outgoing_y * dx2 + outgoing_x * dy2
    radical2 = (second_radius * second_radius - transverse2 * transverse2).sqrt()
    flight2 = ell2 - radical2
    second_x, second_y = hit_x + flight2 * outgoing_x, hit_y + flight2 * outgoing_y
    second_normal_x = (second_x - source_center) / second_radius
    second_normal_y = (second_y - source_center) / second_radius
    target_p = transverse2 / second_radius
    destination_cell = destination.chart_id.split(":")[1]
    target_t = second_normal_y if destination_cell in ("E", "W") else second_normal_x
    return {
        "target_t": target_t, "target_p": target_p,
        "normal_x": second_normal_x, "normal_y": second_normal_y,
        "first_hit_x": hit_x, "first_hit_y": hit_y,
        "first_outgoing_x": outgoing_x, "first_outgoing_y": outgoing_y,
    }


def mpq(value: Q) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator


def scalar_output(core: Any, destination: Any, t: mp.mpf, p: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    rn, rp = mp.sqrt(1 - t * t), mp.sqrt(1 - p * p)
    cell = core.chart_id.split(":")[1]
    if cell == "E": nx, ny = rn, t
    elif cell == "W": nx, ny = -rn, t
    elif cell == "N": nx, ny = t, rn
    else: nx, ny = t, -rn
    ux, uy = rp * nx - p * ny, rp * ny + p * nx
    qx, qy = mp.mpf("0.5") + mp.mpf(4) / 25 * nx, mp.mpf("0.5") + mp.mpf(4) / 25 * ny
    ix, iy = map(int, core.target_id[2:-1].split(","))
    radius = mp.mpf(9) / 25
    dx, dy = mp.mpf(ix) - qx, mp.mpf(iy) - qy
    ell, transverse = ux * dx + uy * dy, -uy * dx + ux * dy
    flight = ell - mp.sqrt(radius * radius - transverse * transverse)
    hx, hy = qx + flight * ux, qy + flight * uy
    nx1, ny1 = (hx - ix) / radius, (hy - iy) / radius
    p1 = transverse / radius
    radial = mp.sqrt(1 - p1 * p1)
    vx, vy = radial * nx1 - p1 * ny1, radial * ny1 + p1 * nx1
    radius = mp.mpf(4) / 25
    dx, dy = mp.mpf("0.5") - hx, mp.mpf("0.5") - hy
    ell, transverse = vx * dx + vy * dy, -vy * dx + vx * dy
    flight = ell - mp.sqrt(radius * radius - transverse * transverse)
    x2, y2 = hx + flight * vx, hy + flight * vy
    nx2, ny2 = (x2 - mp.mpf("0.5")) / radius, (y2 - mp.mpf("0.5")) / radius
    p2 = transverse / radius
    dcell = destination.chart_id.split(":")[1]
    target_t = ny2 if dcell in ("E", "W") else nx2
    return target_t, p2, nx2, ny2


def sign(value: arb) -> int:
    if bool(value > 0): return 1
    if bool(value < 0): return -1
    return 0


def bracket(function: Any, lower: Q, upper: Q, reference: Q) -> tuple[Q, Q]:
    cells = 4096
    points = [lower + (upper - lower) * Q(index, cells) for index in range(cells + 1)]
    candidates = []
    previous = function(mpq(points[0]))
    for index in range(cells):
        current = function(mpq(points[index + 1]))
        if previous == 0 or current == 0 or previous * current < 0:
            candidates.append((points[index], points[index + 1]))
        previous = current
    if not candidates:
        raise RuntimeError("no endpoint root bracket")
    left, right = min(candidates, key=lambda pair: abs((pair[0] + pair[1]) / 2 - reference))
    left_sign = -1 if function(mpq(left)) < 0 else 1
    for _ in range(90):
        middle = (left + right) / 2
        middle_sign = -1 if function(mpq(middle)) < 0 else 1
        if middle_sign == left_sign: left = middle
        else: right = middle
    return left, right


def root_at_p(source: Any, destination: Any, coordinate: str, level: Q, p: mp.mpf, reference: mp.mpf) -> mp.mpf:
    cells = 512
    lower, upper = source.t0, source.t1
    candidates: list[tuple[Q, Q]] = []
    left = lower
    left_value = scalar_output(source, destination, mpq(left), p)[0 if coordinate == "target_t" else 1] - mpq(level)
    for index in range(cells):
        right = lower + (upper - lower) * Q(index + 1, cells)
        right_value = scalar_output(source, destination, mpq(right), p)[0 if coordinate == "target_t" else 1] - mpq(level)
        if left_value == 0 or right_value == 0 or left_value * right_value < 0:
            candidates.append((left, right))
        left, left_value = right, right_value
    if not candidates:
        raise RuntimeError("no curve root at parameter midpoint")
    left, right = min(candidates, key=lambda pair: abs(mpq((pair[0] + pair[1]) / 2) - reference))
    left_value = scalar_output(source, destination, mpq(left), p)[0 if coordinate == "target_t" else 1] - mpq(level)
    left_sign = -1 if left_value < 0 else 1
    for _ in range(90):
        middle = (left + right) / 2
        value = scalar_output(source, destination, mpq(middle), p)[0 if coordinate == "target_t" else 1] - mpq(level)
        if (-1 if value < 0 else 1) == left_sign: left = middle
        else: right = middle
    return mpq((left + right) / 2)


def chart_strict(destination: Any, values: dict[str, Jet]) -> bool:
    cell = destination.chart_id.split(":")[1]
    nx, ny = values["normal_x"].value, values["normal_y"].value
    if cell == "E": return bool(nx > 0) and bool(abs(nx) > abs(ny))
    if cell == "W": return bool(nx < 0) and bool(abs(nx) > abs(ny))
    if cell == "N": return bool(ny > 0) and bool(abs(ny) > abs(nx))
    return bool(ny < 0) and bool(abs(ny) > abs(nx))


def chart_free_second_owner_strict(source: Any, values: dict[str, Jet]) -> bool:
    candidate_ids = sorted({
        candidate
        for cell in ("E", "W", "N", "S")
        for candidate in time2.translated_candidate_ids(source.target_id, cell)
    })
    qx, qy = values["first_hit_x"].value, values["first_hit_y"].value
    ux, uy = values["first_outgoing_x"].value, values["first_outgoing_y"].value
    rows = {}
    for candidate in candidate_ids:
        row = time2.candidate_root(qx, qy, ux, uy, arb(0), candidate)
        kind = row["classification"]
        if kind in ("unresolved_discriminant", "unresolved_root_sign"):
            return False
        if kind == "strict_future_near_root":
            rows[candidate] = row["near"]
    if "W[0,0]" not in rows:
        return False
    winner = rows["W[0,0]"]
    return all(candidate == "W[0,0]" or bool(winner < root) for candidate, root in rows.items())


def active_sides(destination: Any, target_t: mp.mpf, target_p: mp.mpf) -> tuple[str, str]:
    t_side = "t_lower" if abs(target_t - mpq(destination.t0)) < abs(target_t - mpq(destination.t1)) else "t_upper"
    p_side = "p_lower" if abs(target_p - mpq(destination.p0)) < abs(target_p - mpq(destination.p1)) else "p_upper"
    return t_side, p_side


def side_level(destination: Any, side: str) -> Q:
    return destination.t0 if side == "t_lower" else destination.t1 if side == "t_upper" else destination.p0 if side == "p_lower" else destination.p1


def build() -> dict[str, Any]:
    witness_rows = json.loads(WITNESSES.read_text())["result"]["rows"]
    cores = core_cert.physical_cores()
    curve_rows = []
    component_rows = []
    for witness in witness_rows:
        source = cores[witness["source_core_index"]]
        destination = cores[witness["destination_core_index"]]
        t_center = (Q(witness["t_interval"][0]) + Q(witness["t_interval"][1])) / 2
        p_center = (Q(witness["p_interval"][0]) + Q(witness["p_interval"][1])) / 2
        scalar = scalar_output(source, destination, mpq(t_center), mpq(p_center))
        sides = active_sides(destination, scalar[0], scalar[1])
        source_t = source.t0 if t_center < 0 else source.t1
        source_p = source.p0 if p_center < 0 else source.p1
        component_curve_ids = []
        for active_side in sides:
            coordinate = "target_t" if active_side.startswith("t_") else "target_p"
            level = side_level(destination, active_side)
            function_on_t_side = lambda p, st=source_t, coord=coordinate, lev=level: scalar_output(source, destination, mpq(st), p)[0 if coord == "target_t" else 1] - mpq(lev)
            function_on_p_side = lambda t, sp=source_p, coord=coordinate, lev=level: scalar_output(source, destination, t, mpq(sp))[0 if coord == "target_t" else 1] - mpq(lev)
            p_bracket = bracket(function_on_t_side, source.p0, source.p1, p_center)
            t_bracket = bracket(function_on_p_side, source.t0, source.t1, t_center)
            endpoint_signs = []
            for t0, t1, p0, p1 in ((source_t, source_t, *p_bracket), (*t_bracket, source_p, source_p)):
                value0 = t2_output(source, destination, t0, t0, p0, p0)[coordinate].value - aq(level)
                value1 = t2_output(source, destination, t1, t1, p1, p1)[coordinate].value - aq(level)
                endpoint_signs.append([sign(value0), sign(value1)])
            p_midpoint = (p_bracket[0] + p_bracket[1]) / 2
            p_end = source_p
            p_start = p_bracket[0] if p_end < p_midpoint else p_bracket[1]
            slab_count = 128
            slab_rows = []
            endpoint_seam_typed = False
            previous_t = mpq(source_t)
            for slab_index in range(slab_count):
                pa = p_start + (p_end - p_start) * Q(slab_index, slab_count)
                pb = p_start + (p_end - p_start) * Q(slab_index + 1, slab_count)
                pl, pu = min(pa, pb), max(pa, pb)
                pmid = (mpq(pl) + mpq(pu)) / 2
                try:
                    root = mp.findroot(
                        lambda t, coord=coordinate, lev=level: scalar_output(source, destination, t, pmid)[0 if coord == "target_t" else 1] - mpq(lev),
                        previous_t,
                        tol=mp.mpf("1e-50"),
                        maxsteps=30,
                    )
                    if abs(mp.im(root)) > mp.mpf("1e-60"):
                        raise ValueError("non-real/outside continuation")
                    root = mp.re(root)
                    if not (mpq(source.t0) <= root <= mpq(source.t1)):
                        raise ValueError("non-real/outside continuation")
                    root_method = "continued_newton"
                except Exception:
                    root = root_at_p(source, destination, coordinate, level, pmid, previous_t)
                    root_method = "scan_bisection_fallback"
                previous_t = root
                denominator = 1 << 100
                tc = Q(int(mp.floor(root * denominator)), denominator)
                radius = Q(1, 1 << 28)
                for _ in range(36):
                    tl, tu = tc - radius, tc + radius
                    point = t2_output(source, destination, tc, tc, pl, pu)[coordinate]
                    box = t2_output(source, destination, tl, tu, pl, pu)
                    derivative = box[coordinate].dt
                    if sign(derivative) != 0:
                        newton = aq(tc) - (point.value - aq(level)) / derivative
                        if bool(newton > aq(tl)) and bool(newton < aq(tu)):
                            break
                    radius *= 2
                else:
                    raise RuntimeError(f"parametric interval Newton failure {witness['source_core_index']}:{witness['destination_core_index']}:{witness['branch']}:{active_side}:{slab_index}")
                physical_tl, physical_tu = max(source.t0, tl), min(source.t1, tu)
                check_tl, check_tu = physical_tl, physical_tu
                physical_box = t2_output(source, destination, check_tl, check_tu, pl, pu)
                atom = step1.Atom(witness["source_core_index"], source, check_tl, check_tu, pl, pu, Q(0), Q(0), "round75")
                first = step1.classify_atom(atom, cores)
                owner, owner_status = time2.strict_second_owner(atom)
                slab_endpoint_type = "ordinary"
                if slab_index == 0 and owner is None and owner_status == "unresolved_time1_outgoing_chart_or_geometry":
                    trim = (physical_tu - physical_tl) / 16
                    if source_t == source.t0: check_tl += trim
                    else: check_tu -= trim
                    physical_box = t2_output(source, destination, check_tl, check_tu, pl, pu)
                    atom = step1.Atom(witness["source_core_index"], source, check_tl, check_tu, pl, pu, Q(0), Q(0), "round75")
                    first = step1.classify_atom(atom, cores)
                    owner, owner_status = time2.strict_second_owner(atom)
                    slab_endpoint_type = "stationary_x_outgoing_chart_seam"
                    endpoint_seam_typed = True
                chart_free_owner = False
                if owner is None and owner_status == "unresolved_time1_outgoing_chart_or_geometry":
                    chart_free_owner = chart_free_second_owner_strict(source, physical_box)
                owner_ok = (
                    owner is not None and owner_status == "strict_unique_second_collision_owner"
                    and owner["selected_target_id"] == "W[0,0]"
                ) or chart_free_owner
                if first["classification"] != "SURVIVE_THROUGH_1_INNER" or not owner_ok:
                    raise RuntimeError(f"curve chart/owner not strict {witness['source_core_index']}:{witness['destination_core_index']}:{witness['branch']}:{active_side}:{slab_index}:{first['classification']}:{owner_status}:{None if owner is None else owner['selected_target_id']}")
                if not chart_strict(destination, physical_box):
                    raise RuntimeError(f"destination chart not strict {witness['source_core_index']}:{witness['destination_core_index']}:{witness['branch']}:{active_side}:{slab_index}")
                other = physical_box["target_p" if coordinate == "target_t" else "target_t"].value
                other_lower = destination.p0 if coordinate == "target_t" else destination.t0
                other_upper = destination.p1 if coordinate == "target_t" else destination.t1
                if not bool(other > aq(other_lower)) or not bool(other < aq(other_upper)):
                    raise RuntimeError(f"other destination coordinate not strict {witness['source_core_index']}:{witness['destination_core_index']}:{witness['branch']}:{active_side}:{slab_index}")
                slab_rows.append({"index": slab_index, "p_interval": [str(pl), str(pu)], "interval_newton_t_interval": [str(tl), str(tu)], "physical_clipped_t_interval": [str(physical_tl), str(physical_tu)], "strict_check_t_interval": [str(check_tl), str(check_tu)], "interval_newton_strict_interior": True, "dt_level_sign": sign(derivative), "source_t_endpoint_type": slab_endpoint_type, "chart_free_owner_union_used": chart_free_owner, "root_location_method": root_method})
            curve_payload = {"source_core_index": witness["source_core_index"], "destination_core_index": witness["destination_core_index"], "branch": witness["branch"], "active_side": active_side}
            curve_id = "physical-s0-r2-face:" + digest(curve_payload)
            component_curve_ids.append(curve_id)
            curve_rows.append({
                **curve_payload,
                "curve_id": curve_id,
                "level": str(level),
                "source_stationary_sides": ["t_lower" if source_t == source.t0 else "t_upper", "p_lower" if source_p == source.p0 else "p_upper"],
                "endpoint_on_source_t_side": {"t": str(source_t), "p_interval": [str(x) for x in p_bracket], "signs": endpoint_signs[0]},
                "endpoint_on_source_p_side": {"p": str(source_p), "t_interval": [str(x) for x in t_bracket], "signs": endpoint_signs[1]},
                "parametric_interval_newton_slab_count": slab_count,
                "slabs": slab_rows,
                "slabs_sha256": digest(slab_rows),
                "strict_Q1_owner_chart_other_coordinate": True,
                "source_t_endpoint_is_typed_outgoing_chart_seam": endpoint_seam_typed,
            })
        component_rows.append({
            "source_core_index": witness["source_core_index"],
            "destination_core_index": witness["destination_core_index"],
            "branch": witness["branch"],
            "active_sides": list(sides),
            "physical_curve_ids": sorted(component_curve_ids),
            "combinatorial_type": "boundary-attached band between two nonintersecting source-side crosscuts",
        })
    curve_rows.sort(key=canonical)
    component_rows.sort(key=canonical)
    result = {
        "physical_R2_component_count": len(component_rows),
        "physical_R2_curve_count": len(curve_rows),
        "endpoint_vertex_count": 2 * len(curve_rows),
        "parametric_interval_newton_slab_count": sum(row["parametric_interval_newton_slab_count"] for row in curve_rows),
        "chart_free_owner_curve_count": sum(any(slab["chart_free_owner_union_used"] for slab in row["slabs"]) for row in curve_rows),
        "fully_chart_free_owner_curve_count": sum(all(slab["chart_free_owner_union_used"] for slab in row["slabs"]) for row in curve_rows),
        "chart_free_owner_slab_count": sum(sum(slab["chart_free_owner_union_used"] for slab in row["slabs"]) for row in curve_rows),
        "scan_bisection_fallback_slab_count": sum(sum(slab["root_location_method"] == "scan_bisection_fallback" for slab in row["slabs"]) for row in curve_rows),
        "all_curves_have_strict_Q1_owner_chart_other_coordinate": all(row["strict_Q1_owner_chart_other_coordinate"] for row in curve_rows),
        "component_rows": component_rows,
        "component_rows_sha256": digest(component_rows),
        "curve_rows": curve_rows,
        "curve_rows_sha256": digest(curve_rows),
    }
    return {"schema": SCHEMA, "construction": {"arithmetic": "384-bit Arb + parametric interval Newton", "slabs_per_curve": 128}, "result": result}


if __name__ == "__main__":
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
