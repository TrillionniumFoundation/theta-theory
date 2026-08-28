#!/usr/bin/env python3
"""Numeric F8/F9/F10/F13/F16 rows on all Round-75 physical R2 faces."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1


HERE = Path(__file__).resolve().parent
CURVES = HERE / "cm2-round75-r2-physical-curves-2026-07-21.json"
ROUND72 = HERE / "cm2-round72-r1-full-atlas-f10-f13-f16-manifest-2026-07-21.json"
ROUND71 = HERE / "cm2-round71-r1-nonempty-face-germs-manifest-2026-07-21.json"
SCHEMA = "cm2.round76.r2-numeric-fields.v1"


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def aq(value: Q | int) -> arb:
    return step1.arbq(Q(value))


def interval(lower: Q, upper: Q) -> arb:
    return core_cert.first_hit.arb_interval(lower, upper)


class Jet:
    def __init__(self, value: arb, gradient: list[arb] | None = None, hessian: list[list[arb]] | None = None):
        self.value = value
        self.gradient = gradient or [arb(0) for _ in range(3)]
        self.hessian = hessian or [[arb(0) for _ in range(3)] for _ in range(3)]

    @staticmethod
    def variable(value: arb, index: int) -> "Jet":
        gradient = [arb(0) for _ in range(3)]
        gradient[index] = arb(1)
        return Jet(value, gradient)

    def __add__(self, other: Any) -> "Jet":
        other = other if isinstance(other, Jet) else Jet(other)
        return Jet(
            self.value + other.value,
            [self.gradient[i] + other.gradient[i] for i in range(3)],
            [[self.hessian[i][j] + other.hessian[i][j] for j in range(3)] for i in range(3)],
        )

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet(-self.value, [-value for value in self.gradient], [[-value for value in row] for row in self.hessian])

    def __sub__(self, other: Any) -> "Jet":
        return self + (-other if isinstance(other, Jet) else -other)

    def __rsub__(self, other: Any) -> "Jet":
        return Jet(other) - self

    def __mul__(self, other: Any) -> "Jet":
        other = other if isinstance(other, Jet) else Jet(other)
        gradient = [self.gradient[i] * other.value + self.value * other.gradient[i] for i in range(3)]
        hessian = [
            [
                self.hessian[i][j] * other.value
                + self.value * other.hessian[i][j]
                + self.gradient[i] * other.gradient[j]
                + other.gradient[i] * self.gradient[j]
                for j in range(3)
            ]
            for i in range(3)
        ]
        return Jet(self.value * other.value, gradient, hessian)

    __rmul__ = __mul__

    def unary(self, value: arb, first: arb, second: arb) -> "Jet":
        return Jet(
            value,
            [first * entry for entry in self.gradient],
            [[first * self.hessian[i][j] + second * self.gradient[i] * self.gradient[j] for j in range(3)] for i in range(3)],
        )

    def inverse(self) -> "Jet":
        return self.unary(1 / self.value, -1 / (self.value * self.value), 2 / (self.value * self.value * self.value))

    def __truediv__(self, other: Any) -> "Jet":
        return self * (other.inverse() if isinstance(other, Jet) else 1 / other)

    def __rtruediv__(self, other: Any) -> "Jet":
        return Jet(other) * self.inverse()

    def sqrt(self) -> "Jet":
        root = self.value.sqrt()
        return self.unary(root, 1 / (2 * root), -1 / (4 * root * root * root))


def normal(cell: str, coordinate: Jet) -> tuple[Jet, Jet]:
    radial = (arb(1) - coordinate * coordinate).sqrt()
    if cell == "E":
        return radial, coordinate
    if cell == "W":
        return -radial, coordinate
    if cell == "N":
        return coordinate, radial
    return coordinate, -radial


def center(target: str, parameter: Jet) -> tuple[Jet, Jet]:
    obstacle = target[0]
    ix, iy = map(int, target[2:-1].split(","))
    if obstacle == "G":
        return Jet(arb(ix)), Jet(arb(iy))
    return Jet(arb(ix) + aq(Q(1, 2))) + parameter, Jet(arb(iy) + aq(Q(1, 2)))


def collision(point_x: Jet, point_y: Jet, velocity_x: Jet, velocity_y: Jet, target_x: Jet, target_y: Jet, radius: Q) -> tuple[Jet, Jet, Jet, Jet, Jet]:
    radius_ball = aq(radius)
    dx, dy = target_x - point_x, target_y - point_y
    longitudinal = velocity_x * dx + velocity_y * dy
    transverse = -velocity_y * dx + velocity_x * dy
    radical = (radius_ball * radius_ball - transverse * transverse).sqrt()
    flight = longitudinal - radical
    hit_x, hit_y = point_x + flight * velocity_x, point_y + flight * velocity_y
    normal_x, normal_y = (hit_x - target_x) / radius_ball, (hit_y - target_y) / radius_ball
    momentum = transverse / radius_ball
    return hit_x, hit_y, normal_x, normal_y, momentum


def t2_jet(source: Any, destination: Any, t0: Q, t1: Q, p0: Q, p1: Q) -> tuple[Jet, Jet]:
    t = Jet.variable(interval(t0, t1), 0)
    p = Jet.variable(interval(p0, p1), 1)
    parameter = Jet.variable(arb(0), 2)
    normal_x, normal_y = normal(source.chart_id.split(":")[1], t)
    velocity_radial = (arb(1) - p * p).sqrt()
    velocity_x = velocity_radial * normal_x - p * normal_y
    velocity_y = velocity_radial * normal_y + p * normal_x
    source_x, source_y = center(f"{source.source}[0,0]", parameter)
    source_radius = Q(9, 25) if source.source == "G" else Q(4, 25)
    point_x = source_x + aq(source_radius) * normal_x
    point_y = source_y + aq(source_radius) * normal_y
    first_x, first_y = center(source.target_id, parameter)
    first_radius = Q(9, 25) if source.target_id[0] == "G" else Q(4, 25)
    hit_x, hit_y, first_normal_x, first_normal_y, first_p = collision(point_x, point_y, velocity_x, velocity_y, first_x, first_y, first_radius)
    outgoing_radial = (arb(1) - first_p * first_p).sqrt()
    outgoing_x = outgoing_radial * first_normal_x - first_p * first_normal_y
    outgoing_y = outgoing_radial * first_normal_y + first_p * first_normal_x
    second_x, second_y = center("W[0,0]", parameter)
    _hit2_x, _hit2_y, normal2_x, normal2_y, target_p = collision(hit_x, hit_y, outgoing_x, outgoing_y, second_x, second_y, Q(4, 25))
    destination_cell = destination.chart_id.split(":")[1]
    target_t = normal2_y if destination_cell in ("E", "W") else normal2_x
    return target_t, target_p


def ceil_arb(value: arb) -> int:
    candidate = max(1, math.ceil(float(value)) + 2)
    while not bool(arb(candidate) > value):
        candidate += 1
    while candidate > 1 and bool(arb(candidate - 1) > value):
        candidate -= 1
    return candidate


def rational_upper(value: arb, denominator: int = 10**12) -> Q:
    candidate = max(1, math.ceil(float(value) * denominator) + 8)
    while not bool(aq(Q(candidate, denominator)) > value):
        candidate += 1
    while candidate > 1 and bool(aq(Q(candidate - 1, denominator)) > value):
        candidate -= 1
    return Q(candidate, denominator)


def normalized_transversality_lower(derivative_t: arb, derivative_p: arb) -> Q:
    denominator = abs(derivative_t) + abs(derivative_p)
    for exponent in range(1, 257):
        candidate = Q(1, 1 << exponent)
        if bool(abs(derivative_t) > aq(candidate) * denominator):
            return candidate
    raise RuntimeError("no positive normalized transversality lower bound")


def build() -> dict[str, Any]:
    curve_document = json.loads(CURVES.read_text())["result"]
    round72 = json.loads(ROUND72.read_text())["result"]["numeric_local_field_registry"]
    round71 = json.loads(ROUND71.read_text())["result"]["actual_local_field_attachment"]
    cores = core_cert.physical_cores()
    output_rows = []
    for curve in curve_document["curve_rows"]:
        source = cores[curve["source_core_index"]]
        destination = cores[curve["destination_core_index"]]
        coordinate_index = 0 if curve["active_side"].startswith("t_") else 1
        level = Q(curve["level"])
        f8_lower = Q(1)
        f9_upper = 1
        f10_upper = 1
        variation = arb(0)
        slab_rows = []
        for slab in curve["slabs"]:
            t0, t1 = map(Q, slab["physical_clipped_t_interval"])
            p0, p1 = map(Q, slab["p_interval"])
            function = t2_jet(source, destination, t0, t1, p0, p1)[coordinate_index]
            function.value -= aq(level)
            ft, fp, fs = function.gradient
            if not (bool(ft > 0) or bool(ft < 0)):
                raise RuntimeError(f"F_t unresolved on {curve['curve_id']} slab {slab['index']}")
            t_p = -fp / ft
            t_s = -fs / ft
            ftt, ftp, fts = function.hessian[0]
            fpp, fps = function.hessian[1][1], function.hessian[1][2]
            fss = function.hessian[2][2]
            t_pp = -(fpp + 2 * ftp * t_p + ftt * t_p * t_p) / ft
            t_ps = -(fps + ftp * t_s + fts * t_p + ftt * t_p * t_s) / ft
            t_ss = -(fss + 2 * fts * t_s + ftt * t_s * t_s) / ft
            slab_f8 = normalized_transversality_lower(ft, fp)
            slab_f9 = ceil_arb(t_pp.abs_upper())
            t_ball = interval(t0, t1)
            radius = aq(Q(4, 25))
            radial = (arb(1) - t_ball * t_ball).sqrt()
            weight = radius / radial
            weight_t = radius * t_ball / (radial * radial * radial)
            rho = weight * t_s
            rho_p = weight_t * t_p * t_s + weight * t_ps
            rho_s = weight_t * t_s * t_s + weight * t_ss
            slab_f10 = ceil_arb(rho.abs_upper() + rho_p.abs_upper() + rho_s.abs_upper())
            variation += aq(p1 - p0) * rho.abs_upper()
            f8_lower = min(f8_lower, slab_f8)
            f9_upper = max(f9_upper, slab_f9)
            f10_upper = max(f10_upper, slab_f10)
            slab_rows.append({"index": slab["index"], "F8_normalized_transversality_dyadic_lower": str(slab_f8), "F9_unit_speed_C2_integer_upper": slab_f9, "F10_density_C1_integer_upper": slab_f10})
        face_variation = rational_upper(variation)
        output_rows.append({
            "curve_id": curve["curve_id"],
            "source_core_index": curve["source_core_index"],
            "destination_core_index": curve["destination_core_index"],
            "branch": curve["branch"],
            "active_side": curve["active_side"],
            "F8_normalized_transversality_dyadic_lower": str(f8_lower),
            "F9_unit_speed_C2_integer_upper": f9_upper,
            "F10_density_C1_integer_upper": f10_upper,
            "F13_full_face_current_variation_strict_upper": str(face_variation),
            "F16_full_face_Piola_flux_cost_strict_upper": str(face_variation),
            "slab_rows_sha256": digest(slab_rows),
        })
    output_rows.sort(key=lambda row: row["curve_id"])
    r2_f13 = sum((Q(row["F13_full_face_current_variation_strict_upper"]) for row in output_rows), Q(0))
    r2_f16 = sum((Q(row["F16_full_face_Piola_flux_cost_strict_upper"]) for row in output_rows), Q(0))
    r1_f13 = Q(round72["F13_32_face_current_variation_strict_upper"])
    r1_f16 = Q(round72["F16_32_face_flux_cost_strict_upper"])
    r1_f9 = Q(round71["F9_32_face_finite_sum_upper"])
    r2_f9 = Q(sum(row["F9_unit_speed_C2_integer_upper"] for row in output_rows))
    r1_f10 = Q(round72["F10_integer_sum"])
    r2_f10 = Q(sum(row["F10_density_C1_integer_upper"] for row in output_rows))
    result = {
        "physical_R2_face_count": len(output_rows),
        "F8_common_normalized_transversality_dyadic_lower": str(min(Q(row["F8_normalized_transversality_dyadic_lower"]) for row in output_rows)),
        "F9_integer_minimum": min(row["F9_unit_speed_C2_integer_upper"] for row in output_rows),
        "F9_integer_maximum": max(row["F9_unit_speed_C2_integer_upper"] for row in output_rows),
        "F9_32_face_integer_sum": sum(row["F9_unit_speed_C2_integer_upper"] for row in output_rows),
        "F10_integer_minimum": min(row["F10_density_C1_integer_upper"] for row in output_rows),
        "F10_integer_maximum": max(row["F10_density_C1_integer_upper"] for row in output_rows),
        "F10_32_face_integer_sum": sum(row["F10_density_C1_integer_upper"] for row in output_rows),
        "F13_32_face_current_variation_strict_upper": str(r2_f13),
        "F16_32_face_Piola_flux_cost_strict_upper": str(r2_f16),
        "finite_cross_rank_counting_sum": {
            "R1_face_count": 32,
            "R2_face_count": 32,
            "F10_64_face_integer_sum": round72["F10_integer_sum"] + sum(row["F10_density_C1_integer_upper"] for row in output_rows),
            "F13_64_face_current_variation_strict_upper": str(r1_f13 + r2_f13),
            "F16_64_face_Piola_flux_cost_strict_upper": str(r1_f16 + r2_f16),
            "scope": "finite counting measure on the certified 32 R1 plus 32 R2 physical faces; not a limiting path-law weighted sum",
        },
        "finite_cross_rank_geometric_depth_weight_sum": {
            "weight_rule": "face at time_j receives 2^(-time_j)",
            "R1_time_and_weight": [1, "1/2"],
            "R2_time_and_weight": [2, "1/4"],
            "F8_common_normalized_transversality_lower": str(min(Q(round71["F8_common_normalized_strict_lower"]), min(Q(row["F8_normalized_transversality_dyadic_lower"]) for row in output_rows))),
            "F9_weighted_sum_upper": str(r1_f9 / 2 + r2_f9 / 4),
            "F10_weighted_sum_upper": str(r1_f10 / 2 + r2_f10 / 4),
            "F13_weighted_sum_strict_upper": str(r1_f13 / 2 + r2_f13 / 4),
            "F16_weighted_sum_strict_upper": str(r1_f16 / 2 + r2_f16 / 4),
            "scope": "certified finite two-rank geometric-depth weight demonstration; not the official limiting physical path law",
        },
        "rows": output_rows,
        "rows_sha256": digest(output_rows),
    }
    return {
        "schema": SCHEMA,
        "construction": {
            "arithmetic": "384-bit Arb second-order Jet in source t, source p, and moving parameter s",
            "graph": "source t = T(source p,s)",
            "signed_current_density": "rho=(4/25)/sqrt(1-t^2) * partial_s T",
            "F10_integrand": "abs(rho)+abs(partial_p rho)+abs(partial_s rho)",
            "F16_source": "exact area-preserving Piola flux identity",
        },
        "result": result,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(build(), sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
