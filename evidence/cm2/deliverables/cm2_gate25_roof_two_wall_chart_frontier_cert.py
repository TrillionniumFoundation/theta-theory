#!/usr/bin/env python3
"""Physical transparent-wall charts on the four certified roof-two cores.

This certificate is deliberately local.  It binds the missing intermediate
transparent-wall section on the four positive physical roof-two cores from
the frozen Gate-2/5 registry.  It does not enlarge those compact cores to
maximal word domains and does not populate any complete 18-field operator
block.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as base
import cm2_gate3_candidate_first_hit_cert as first_hit


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = (
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json",
    "cm2_gate25_physical_return_core_registry_cert.py",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json",
    "cm2_gate5_return_word_three_norm_frontier_cert.py",
)


def aq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Dual2:
    value: arb
    dt: arb
    dp: arb

    @staticmethod
    def constant(value: arb | Q | int) -> "Dual2":
        if not isinstance(value, arb):
            value = aq(value)
        return Dual2(value, arb(0), arb(0))

    def __add__(self, other: "Dual2 | arb | Q | int") -> "Dual2":
        if not isinstance(other, Dual2):
            other = Dual2.constant(other)
        return Dual2(
            self.value + other.value,
            self.dt + other.dt,
            self.dp + other.dp,
        )

    __radd__ = __add__

    def __neg__(self) -> "Dual2":
        return Dual2(-self.value, -self.dt, -self.dp)

    def __sub__(self, other: "Dual2 | arb | Q | int") -> "Dual2":
        if not isinstance(other, Dual2):
            other = Dual2.constant(other)
        return self + (-other)

    def __rsub__(self, other: "Dual2 | arb | Q | int") -> "Dual2":
        return Dual2.constant(other) - self

    def __mul__(self, other: "Dual2 | arb | Q | int") -> "Dual2":
        if not isinstance(other, Dual2):
            other = Dual2.constant(other)
        return Dual2(
            self.value * other.value,
            self.dt * other.value + self.value * other.dt,
            self.dp * other.value + self.value * other.dp,
        )

    __rmul__ = __mul__

    def reciprocal(self) -> "Dual2":
        square = self.value * self.value
        return Dual2(
            1 / self.value,
            -self.dt / square,
            -self.dp / square,
        )

    def __truediv__(self, other: "Dual2 | arb | Q | int") -> "Dual2":
        if not isinstance(other, Dual2):
            other = Dual2.constant(other)
        return self * other.reciprocal()

    def __rtruediv__(self, other: "Dual2 | arb | Q | int") -> "Dual2":
        return Dual2.constant(other) / self

    def sqrt(self) -> "Dual2":
        root = self.value.sqrt()
        return Dual2(root, self.dt / (2 * root), self.dp / (2 * root))


def dependency_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name in DEPENDENCIES:
        path = HERE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        hashes[name] = sha256_path(path)
    return hashes


def matrix_inverse(
    matrix: tuple[arb, arb, arb, arb]
) -> tuple[tuple[arb, arb, arb, arb], arb]:
    a, b, c, d = matrix
    determinant = a * d - b * c
    return (d / determinant, -b / determinant,
            -c / determinant, a / determinant), determinant


def matrix_multiply(
    left: tuple[arb, arb, arb, arb],
    right: tuple[arb, arb, arb, arb],
) -> tuple[arb, arb, arb, arb]:
    a, b, c, d = left
    e, f, g, h = right
    return (
        a * e + b * g,
        a * f + b * h,
        c * e + d * g,
        c * f + d * h,
    )


def assert_infinity_norm_strict_upper(
    matrix: tuple[arb, arb, arb, arb], upper: Q | int
) -> None:
    a, b, c, d = matrix
    assert bool(abs(a) + abs(b) < aq(upper))
    assert bool(abs(c) + abs(d) < aq(upper))


def suffix_cell_audit(
    core: base.Core,
    t0: Q,
    t1: Q,
    p0: Q,
    p1: Q,
    s0: Q,
    s1: Q,
    cell_index: tuple[int, int, int],
) -> dict[str, Any]:
    t = Dual2(first_hit.arb_interval(t0, t1), arb(1), arb(0))
    p = Dual2(first_hit.arb_interval(p0, p1), arb(0), arb(1))
    s = first_hit.arb_interval(s0, s1)
    radical_t = (Dual2.constant(1) - t * t).sqrt()
    radical_p = (Dual2.constant(1) - p * p).sqrt()
    source_cell = core.chart_id.split(":")[1]
    if source_cell == "E":
        nx, ny = radical_t, t
    elif source_cell == "W":
        nx, ny = -radical_t, t
    elif source_cell == "N":
        nx, ny = t, radical_t
    elif source_cell == "S":
        nx, ny = t, -radical_t
    else:  # pragma: no cover
        raise AssertionError(source_cell)

    ux = radical_p * nx - p * ny
    uy = radical_p * ny + p * nx
    qx = Dual2.constant(aq(Q(1, 2)) + s) + aq(Q(4, 25)) * nx
    qy = Dual2.constant(Q(1, 2)) + aq(Q(4, 25)) * ny
    token = core.crossings[0]
    wall_index = 1 if token[1] == "+" else 0
    if token[0] == "X":
        tau = (wall_index - qx) / ux
        z = qy + tau * uy
        eta = uy
    else:
        tau = (wall_index - qy) / uy
        z = qx + tau * ux
        eta = ux

    target = first_hit.target_by_id(core.target_id)
    assert target.obstacle == "W"
    ax = Dual2.constant(target.ix + Q(1, 2)) + Dual2.constant(s)
    ay = Dual2.constant(target.iy + Q(1, 2))
    dx, dy = ax - qx, ay - qy
    transverse = -uy * dx + ux * dy
    radius = Dual2.constant(Q(4, 25))
    radical = (radius * radius - transverse * transverse).sqrt()
    target_nx = (-radical * ux + transverse * uy) / radius
    target_ny = (-radical * uy - transverse * ux) / radius
    target_p = transverse / radius

    target_cells = {"E": "W", "W": "E", "N": "S", "S": "N"}
    target_cell = target_cells[source_cell]
    if target_cell == "E":
        assert bool(target_nx.value > 0)
        target_t = target_ny
    elif target_cell == "W":
        assert bool(target_nx.value < 0)
        target_t = target_ny
    elif target_cell == "N":
        assert bool(target_ny.value > 0)
        target_t = target_nx
    else:
        assert bool(target_ny.value < 0)
        target_t = target_nx
    assert bool(abs(target_t.value) < aq(Q(1, 4)))
    assert bool(abs(target_p.value) < aq(Q(1, 4)))

    wall_matrix = (z.dt, z.dp, eta.dt, eta.dp)
    target_matrix = (
        target_t.dt, target_t.dp, target_p.dt, target_p.dp
    )
    inverse_wall, wall_determinant = matrix_inverse(wall_matrix)
    inverse_target, target_determinant = matrix_inverse(target_matrix)
    assert bool(abs(wall_determinant) > aq(Q(3, 20)))
    assert bool(abs(target_determinant) > aq(Q(1, 10)))
    suffix_matrix = matrix_multiply(target_matrix, inverse_wall)
    inverse_suffix = matrix_multiply(wall_matrix, inverse_target)
    assert_infinity_norm_strict_upper(suffix_matrix, 20)
    assert_infinity_norm_strict_upper(inverse_suffix, 20)
    return {
        "cell_index_t_p_s": list(cell_index),
        "source_subbox": {
            "t": [str(t0), str(t1)],
            "p": [str(p0), str(p1)],
            "s": [str(s0), str(s1)],
        },
        "target_collision_chart": f"W:{target_cell}",
        "target_abs_t_and_p_strict_upper": "1/4",
        "absolute_target_map_Jacobian_determinant_strict_lower": "1/10",
        "wall_to_target_D_infinity_strict_upper": "20",
        "target_to_wall_D_infinity_strict_upper": "20",
    }


def wall_core_data(core: base.Core) -> dict[str, Any]:
    assert core.source == "W"
    assert len(core.crossings) == 1
    token = core.crossings[0]
    assert token in {"X+", "X-", "Y+", "Y-"}

    t = Dual2(
        first_hit.arb_interval(core.t0, core.t1), arb(1), arb(0)
    )
    p = Dual2(
        first_hit.arb_interval(core.p0, core.p1), arb(0), arb(1)
    )
    s = first_hit.arb_interval(base.S_LOWER, base.S_UPPER)
    radical_t = (Dual2.constant(1) - t * t).sqrt()
    radical_p = (Dual2.constant(1) - p * p).sqrt()
    cell = core.chart_id.split(":")[1]
    if cell == "E":
        nx, ny = radical_t, t
    elif cell == "W":
        nx, ny = -radical_t, t
    elif cell == "N":
        nx, ny = t, radical_t
    elif cell == "S":
        nx, ny = t, -radical_t
    else:  # pragma: no cover - frozen registry has only four cells
        raise AssertionError(cell)

    ux = radical_p * nx - p * ny
    uy = radical_p * ny + p * nx
    qx = Dual2.constant(aq(Q(1, 2)) + s) + aq(Q(4, 25)) * nx
    qy = Dual2.constant(Q(1, 2)) + aq(Q(4, 25)) * ny

    wall_index = 1 if token[1] == "+" else 0
    if token[0] == "X":
        tau = (wall_index - qx) / ux
        z = qy + tau * uy
        eta = uy
        normal_velocity = ux
        chart_coordinates = "(z=y, eta=u_y)"
        wall_equation = f"x={wall_index}"
    else:
        tau = (wall_index - qy) / uy
        z = qx + tau * ux
        eta = ux
        normal_velocity = uy
        chart_coordinates = "(z=x, eta=u_x)"
        wall_equation = f"y={wall_index}"

    contact = base.contact_geometry(core)
    remaining = contact["root"] - tau.value

    assert bool(tau.value > aq(Q(1, 3)))
    assert bool(tau.value < aq(Q(7, 20)))
    assert bool(remaining > aq(Q(33, 100)))
    assert bool(remaining < aq(Q(7, 20)))
    assert bool(contact["root"] > aq(Q(2, 3)))
    assert bool(contact["root"] < aq(Q(7, 10)))
    assert bool(z.value > aq(Q(1, 2)))
    assert bool(z.value < aq(Q(53, 100)))
    assert bool(abs(eta.value) < aq(Q(1, 40)))
    if token[1] == "+":
        assert bool(normal_velocity.value > aq(Q(99, 100)))
    else:
        assert bool(normal_velocity.value < -aq(Q(99, 100)))

    determinant = z.dt * eta.dp - z.dp * eta.dt
    forward_row_1 = abs(z.dt) + abs(z.dp)
    forward_row_2 = abs(eta.dt) + abs(eta.dp)
    assert bool(abs(determinant) > aq(Q(3, 20)))
    assert bool(forward_row_1 < aq(3))
    assert bool(forward_row_2 < aq(3))

    inverse_00 = eta.dp / determinant
    inverse_01 = -z.dp / determinant
    inverse_10 = -eta.dt / determinant
    inverse_11 = z.dt / determinant
    inverse_row_1 = abs(inverse_00) + abs(inverse_01)
    inverse_row_2 = abs(inverse_10) + abs(inverse_11)
    assert bool(inverse_row_1 < aq(10))
    assert bool(inverse_row_2 < aq(10))

    suffix_ledger: list[dict[str, Any]] = []
    subdivisions = 2
    for i in range(subdivisions):
        t0 = core.t0 + (core.t1 - core.t0) * i / subdivisions
        t1 = core.t0 + (core.t1 - core.t0) * (i + 1) / subdivisions
        for j in range(subdivisions):
            p0 = core.p0 + (core.p1 - core.p0) * j / subdivisions
            p1 = core.p0 + (core.p1 - core.p0) * (j + 1) / subdivisions
            for k in range(subdivisions):
                s0 = base.S_LOWER + (
                    base.S_UPPER - base.S_LOWER
                ) * k / subdivisions
                s1 = base.S_LOWER + (
                    base.S_UPPER - base.S_LOWER
                ) * (k + 1) / subdivisions
                suffix_ledger.append(suffix_cell_audit(
                    core, t0, t1, p0, p1, s0, s1, (i, j, k)
                ))
    assert len(suffix_ledger) == 8
    return {
        "physical_key": [
            core.chart_id,
            core.target_id,
            list(core.crossings),
            len(core.crossings) + 1,
        ],
        "wall_token": token,
        "wall_equation": wall_equation,
        "oriented_transparent_wall_chart": chart_coordinates,
        "wall_time_strict_bounds": ["1/3", "7/20"],
        "wall_to_target_time_strict_bounds": ["33/100", "7/20"],
        "full_flight_time_strict_bounds": ["2/3", "7/10"],
        "wall_coordinate_strict_bounds": ["1/2", "53/100"],
        "distance_from_either_integer_corner_strict_lower": "47/100",
        "absolute_normal_velocity_strict_lower": "99/100",
        "absolute_tangential_velocity_strict_upper": "1/40",
        "source_core_to_wall_chart_D_infinity_strict_upper": "3",
        "wall_chart_to_source_core_D_infinity_strict_upper": "10",
        "absolute_chart_Jacobian_determinant_strict_lower_in_t_p": "3/20",
        "suffix_subdivision_t_p_s": [2, 2, 2],
        "suffix_subdivision_cell_count": 8,
        "all_suffix_cells_target_abs_t_and_p_strict_upper": "1/4",
        "all_suffix_cells_target_map_determinant_strict_lower": "1/10",
        "wall_to_target_local_collision_chart_D_infinity_strict_upper": "20",
        "target_local_collision_chart_to_wall_D_infinity_strict_upper": "20",
        "suffix_subdivision_ledger_sha256": canonical_digest(suffix_ledger),
    }


def build_result() -> dict[str, Any]:
    frozen = base.certify()
    frozen_registry = frozen["physical_return_core_registry"]
    assert frozen_registry["roof_histogram"] == {"1": 20, "2": 4}
    assert frozen_registry["registered_roof_level_prefix_suffix_pairs"] == 28
    assert frozen_registry["registered_endpoint_boundary_splits"] == 52

    roof_two = [core for core in base.physical_cores() if core.crossings]
    assert len(roof_two) == 4
    wall_rows = [wall_core_data(core) for core in roof_two]
    wall_rows.sort(key=lambda row: canonical_json(row["physical_key"]))
    assert sum(row["suffix_subdivision_cell_count"] for row in wall_rows) == 32
    suffix_digest_ledger = [
        {
            "physical_key": row["physical_key"],
            "suffix_subdivision_ledger_sha256": (
                row["suffix_subdivision_ledger_sha256"]
            ),
        }
        for row in wall_rows
    ]

    result: dict[str, Any] = {
        "schema": "cm2.gate25.roof-two-wall-chart-frontier.v1",
        "provenance": {
            "frozen_dependency_sha256": dependency_hashes(),
            "arithmetic": "384-bit Arb first-order automatic differentiation",
            "parameter_window": ["-1/400", "1/400"],
        },
        "roof_two_wall_chart_registry": {
            "roof_one_physical_core_count": 20,
            "roof_two_physical_core_count": 4,
            "intermediate_transparent_wall_chart_count": 4,
            "all_four_wall_crossings_unique_and_away_from_corners": True,
            "all_four_wall_charts_uniform_on_full_parameter_window": True,
            "all_four_wall_chart_maps_local_diffeomorphisms": True,
            "all_four_suffix_maps_certified_by_2x2x2_subdivision": True,
            "total_suffix_subdivision_cell_count": 32,
            "all_28_core_local_roof_level_prefix_suffix_pairs_have_charts": True,
            "all_52_core_local_split_slots_have_charts": True,
            "roof_two_wall_adjacent_local_chart_D_infinity_upper": "20",
            "wall_rows": wall_rows,
            "wall_rows_sha256": canonical_digest(wall_rows),
            "suffix_subdivision_digest_ledger": suffix_digest_ledger,
            "suffix_subdivision_digest_ledger_sha256": canonical_digest(
                suffix_digest_ledger
            ),
        },
        "typing_limits": {
            "transparent_wall_is_not_a_collision_or_singularity": True,
            "wall_chart_cost_is_in_local_t_p_and_z_eta_coordinates": True,
            "wall_chart_cost_is_not_a_CM2_strong_operator_cost": True,
            "compact_cores_are_not_maximal_word_domains": True,
            "complete_full_key_18_field_block_count": 0,
            "completed_full_key_schema_field_count_on_each_of_24_keys": 1,
            "stable_saturated_Young_base": False,
            "stable_quotient_rho_reverse_kernel_PPE": False,
            "gate2": False,
            "gate5": False,
        },
        "exact_remaining_blockers": [
            "maximal homogeneous word domains and complete subbranch table",
            "full-key inverse-Jacobian, distortion, cut-growth and face fields",
            "three CM2 strong operator lifts, Kac output and operator phase",
            "stable-saturated quotient, rho, reverse weights, stopping and PPE",
        ],
    }
    payload = json.loads(canonical_json(result))
    result["internal_replay_digest"] = canonical_digest(payload)
    return result


if __name__ == "__main__":
    print(json.dumps(build_result(), indent=2, sort_keys=True))
