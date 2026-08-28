#!/usr/bin/env python3
"""Finite-parameter second-collision singularity outer atlas for CM2 Gate 3.

This certificate works on the fixed labelled carrier

    disjoint_union_(e=0)^63 ([0,1]_t x [0,1]_v),
    s=(2v-1)/400.

The row coordinate ``t`` is the inward-angle coordinate of the frozen
finite-s maximal-row registry (with the already charged absolute endpoint
trim ``2^-20``).  A first-order interval Taylor model in both ``t`` and ``s``
is used to enclose every one of the 4,704 possible next-collision tangency
discriminants.  Rectangles on which all discriminants have fixed sign have
an immutable next-collision owner.  Rectangles meeting a discriminant zero
are retained positively as finite root strips; whenever possible the strip
also carries a strict ``d/dt`` sign and opposite signs on its two vertical
edges, so it contains exactly one transverse root for every parameter in
that slab.

The resulting finite rectangular cover is a *future-singularity outer
atlas*.  It deliberately does not delete the root strips and does not call
their finite positive cover area the mass of the analytic singular set.
The ``v`` coordinate is a normalized parameter coordinate, not a probability
law.  Consequently two-dimensional ``(t,v)`` areas, perimeters and tubes are
reported only as nonphysical parameter-integrated bookkeeping.  Physical
row-law outer charges are stated only through a separate supremum over fixed
parameter slices.  Candidate root graphs are not assumed to be physical-first
collision boundaries, and a formal two-point mark is not called a physical
current.  Strong-space restriction estimates, operator-norm DQ and
branch-record MT_DQ remain open.
"""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_iterated_common_atlas_mt_dq_cert as prior
import cm2_gate45_finite_s_common_mesh_recovery_cert as finite


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

PRIOR_MANIFEST = (
    HERE / "cm2-gate3-iterated-common-atlas-mt-dq-manifest-2026-07-16.json"
)
FINITE_MANIFEST = (
    HERE / "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
)

S_LOWER = Q(-1, 400)
S_UPPER = Q(1, 400)
ENDPOINT_TRIM = Q(1, 1 << 20)
TAU_MAX = Q(3)

# The adaptive cover starts with 32*8=256 rectangles per occurrence row.
# Only boxes that cannot yet be typed are refined.  The terminal resolution
# is deliberately finite and fail-closed: larger unresolved outer covers are
# preferable to an impractically large replay or a hidden deletion.
INITIAL_T_CELLS = 32
INITIAL_V_CELLS = 8
MAX_T_DEPTH = 5
MAX_V_DEPTH = 3
ROOT_T_WIDTH = Q(1, 1 << 10)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def arb_interval(lower: Q, upper: Q) -> arb:
    return finite.bulk.arb_interval(lower, upper)


@dataclass(frozen=True)
class Jet2:
    """Natural interval value plus exact first-order AD in ``t`` and ``s``."""

    value: arb
    dt: arb
    ds: arb

    @classmethod
    def constant(cls, value: Any) -> "Jet2":
        if not isinstance(value, arb):
            value = arbq(Q(value))
        return cls(value, arb(0), arb(0))

    @classmethod
    def t_variable(cls, value: arb) -> "Jet2":
        return cls(value, arb(1), arb(0))

    @classmethod
    def s_variable(cls, value: arb) -> "Jet2":
        return cls(value, arb(0), arb(1))

    def coerce(self, other: Any) -> "Jet2":
        return other if isinstance(other, Jet2) else Jet2.constant(other)

    def __add__(self, other: Any) -> "Jet2":
        other = self.coerce(other)
        return Jet2(
            self.value + other.value,
            self.dt + other.dt,
            self.ds + other.ds,
        )

    __radd__ = __add__

    def __neg__(self) -> "Jet2":
        return Jet2(-self.value, -self.dt, -self.ds)

    def __sub__(self, other: Any) -> "Jet2":
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> "Jet2":
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> "Jet2":
        other = self.coerce(other)
        return Jet2(
            self.value * other.value,
            self.dt * other.value + self.value * other.dt,
            self.ds * other.value + self.value * other.ds,
        )

    __rmul__ = __mul__

    def inverse(self) -> "Jet2":
        if self.value.contains(0):
            raise ValueError("interval inverse crosses zero")
        square = self.value * self.value
        return Jet2(1 / self.value, -self.dt / square, -self.ds / square)

    def __truediv__(self, other: Any) -> "Jet2":
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other: Any) -> "Jet2":
        return self.coerce(other) / self

    def sqrt(self) -> "Jet2":
        if not bool(self.value > 0):
            raise ValueError("interval square root not strictly positive")
        root = self.value.sqrt()
        return Jet2(root, self.dt / (2 * root), self.ds / (2 * root))

    def sin(self) -> "Jet2":
        return Jet2(
            self.value.sin(),
            self.value.cos() * self.dt,
            self.value.cos() * self.ds,
        )

    def cos(self) -> "Jet2":
        return Jet2(
            self.value.cos(),
            -self.value.sin() * self.dt,
            -self.value.sin() * self.ds,
        )


def atan2_jet(y: Jet2, x: Jet2) -> Jet2:
    denominator = x.value * x.value + y.value * y.value
    if denominator.contains(0):
        raise ValueError("atan2 derivative denominator crosses zero")
    return Jet2(
        arb.atan2(y.value, x.value),
        (x.value * y.dt - y.value * x.dt) / denominator,
        (x.value * y.ds - y.value * x.ds) / denominator,
    )


def target_center(
    obstacle: str, ix: int, iy: int, s: Jet2,
) -> tuple[Jet2, Jet2]:
    if obstacle == "G":
        return Jet2.constant(ix), Jet2.constant(iy)
    return Jet2.constant(Q(2 * ix + 1, 2)) + s, Jet2.constant(Q(2 * iy + 1, 2))


def target_center_id(target_id: str, s: Jet2) -> tuple[Jet2, Jet2]:
    obstacle, ix, iy = prior.parse_target(target_id)
    return target_center(obstacle, ix, iy, s)


def source_center(source: str, s: Jet2) -> tuple[Jet2, Jet2]:
    if source == "G":
        return Jet2.constant(0), Jet2.constant(0)
    return Jet2.constant(Q(1, 2)) + s, Jet2.constant(Q(1, 2))


def curve_normal(curve: dict[str, Any], s: Jet2) -> tuple[Jet2, Jet2]:
    """Replay every moving maximal-row boundary in two-variable AD."""

    source = curve["source"]
    target = curve["target"]
    epsilon = curve["epsilon"]
    tx, ty = target_center_id(target, s)
    sx, sy = source_center(source, s)
    cx, cy = tx - sx, ty - sy
    source_radius = Jet2.constant(finite.bulk.ARB_RADIUS[source])
    target_obstacle = finite.bulk.TARGET_BY_ID[target].obstacle
    target_radius = Jet2.constant(finite.bulk.ARB_RADIUS[target_obstacle])
    kind = curve["kind"]

    if kind == finite.maximal.SOURCE_GRAZING:
        direction = curve["tangent_direction"]
        distance_squared = cx * cx + cy * cy
        offset = source_radius - direction * epsilon * target_radius
        radical = (distance_squared - offset * offset).sqrt()
        return (
            (offset * cx + direction * radical * cy) / distance_squared,
            (offset * cy - direction * radical * cx) / distance_squared,
        )

    if kind == finite.maximal.POLARITY:
        direction = curve["horizontal_direction"]
        normal_y = (cy - direction * epsilon * target_radius) / source_radius
        normal_x = direction * (1 - normal_y * normal_y).sqrt()
        return normal_x, normal_y

    descriptor = curve["descriptor"]
    other = descriptor["other"]
    epsilon_other = descriptor["epsilon_other"]
    line_branch = descriptor["line_branch"]
    ax, ay = target_center_id(target, s)
    bx, by = target_center_id(other, s)
    dx, dy = bx - ax, by - ay
    distance_squared = dx * dx + dy * dy
    other_obstacle = finite.bulk.TARGET_BY_ID[other].obstacle
    other_radius = Jet2.constant(finite.bulk.ARB_RADIUS[other_obstacle])
    h = epsilon_other * other_radius - epsilon * target_radius
    radical = (distance_squared - h * h).sqrt()
    nx = (h * dx - line_branch * radical * dy) / distance_squared
    ny = (h * dy + line_branch * radical * dx) / distance_squared
    ux, uy = ny, -nx
    source_x, source_y = source_center(source, s)
    line_offset = nx * (ax - source_x) + ny * (ay - source_y) - epsilon * target_radius
    z = line_offset / source_radius
    cp = (1 - z * z).sqrt()
    return cp * ux + z * nx, cp * uy + z * ny


def trimmed_row_normal(
    row: dict[str, Any], t: Jet2, s: Jet2,
) -> tuple[Jet2, Jet2]:
    left_x, left_y = curve_normal(row["left_boundary"], s)
    right_x, right_y = curve_normal(row["right_boundary"], s)
    cross = left_x * right_y - left_y * right_x
    dot = left_x * right_x + left_y * right_y
    width = atan2_jet(cross, dot)
    distance = ENDPOINT_TRIM + (width - 2 * ENDPOINT_TRIM) * t
    cosine, sine = distance.cos(), distance.sin()
    return (
        cosine * left_x - sine * left_y,
        cosine * left_y + sine * left_x,
    )


def moving_tangent_geometry(
    row: dict[str, Any], normal_x: Jet2, normal_y: Jet2, s: Jet2,
) -> tuple[Jet2, ...]:
    source_x, source_y = source_center(row["source"], s)
    target_x, target_y = target_center_id(row["target"], s)
    source_radius = Jet2.constant(finite.bulk.ARB_RADIUS[row["source"]])
    target_obstacle = finite.bulk.TARGET_BY_ID[row["target"]].obstacle
    target_radius = Jet2.constant(finite.bulk.ARB_RADIUS[target_obstacle])
    point_x = source_x + source_radius * normal_x
    point_y = source_y + source_radius * normal_y
    difference_x = target_x - point_x
    difference_y = target_y - point_y
    distance_squared = difference_x * difference_x + difference_y * difference_y
    flight = (distance_squared - target_radius * target_radius).sqrt()
    epsilon = row["epsilon"]
    velocity_x = (
        flight * difference_x + epsilon * target_radius * difference_y
    ) / distance_squared
    velocity_y = (
        flight * difference_y - epsilon * target_radius * difference_x
    ) / distance_squared
    source_cp = velocity_x * normal_x + velocity_y * normal_y
    return point_x, point_y, velocity_x, velocity_y, flight, source_cp


def second_geometry(
    row: dict[str, Any], t: Jet2, s: Jet2,
    candidate_only: str | None = None,
) -> dict[str, Any]:
    """Return analytic prerequisite and candidate fields before owner logic."""

    normal_x, normal_y = trimmed_row_normal(row, t, s)
    qx, qy, ux, uy, ell_t, source_cp = moving_tangent_geometry(
        row, normal_x, normal_y, s
    )
    miss_obstacle, miss_ix, miss_iy = prior.parse_target(row["miss_target"])
    mx, my = target_center(miss_obstacle, miss_ix, miss_iy, s)
    miss_radius = Jet2.constant(finite.bulk.ARB_RADIUS[miss_obstacle])
    dx, dy = mx - qx, my - qy
    ell = ux * dx + uy * dy
    w = -uy * dx + ux * dy
    delta = miss_radius * miss_radius - w * w
    sqrt_delta = delta.sqrt()
    miss_root_gap = ell - sqrt_delta - ell_t
    hit_x = mx - sqrt_delta * ux + w * uy
    hit_y = my - sqrt_delta * uy - w * ux
    radius_squared = miss_radius * miss_radius
    a = 1 - 2 * delta / radius_squared
    c = -2 * sqrt_delta * w / radius_squared
    out_x = a * ux - c * uy
    out_y = a * uy + c * ux

    candidates: dict[str, dict[str, Jet2]] = {}
    for obstacle, ix, iy, relative_id in prior.shifted_candidates(
        miss_obstacle, miss_ix, miss_iy
    ):
        if candidate_only is not None and relative_id != candidate_only:
            continue
        cx, cy = target_center(obstacle, ix, iy, s)
        radius = Jet2.constant(finite.bulk.ARB_RADIUS[obstacle])
        difference_x, difference_y = cx - hit_x, cy - hit_y
        projection = out_x * difference_x + out_y * difference_y
        transverse = -out_y * difference_x + out_x * difference_y
        discriminant = radius * radius - transverse * transverse
        candidates[relative_id] = {
            "projection": projection,
            "discriminant": discriminant,
        }
    return {
        "source_cp": source_cp,
        "miss_delta": delta,
        "miss_root_gap": miss_root_gap,
        "candidates": candidates,
    }


def candidate_universe_and_filter_audit(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Freeze the 4,704-function universe and the candidate-only fast path."""

    total = 0
    per_row_counts = []
    for row_index, row in enumerate(rows):
        miss_obstacle, miss_ix, miss_iy = prior.parse_target(row["miss_target"])
        count = len(prior.shifted_candidates(miss_obstacle, miss_ix, miss_iy))
        total += count
        per_row_counts.append({"row_index": row_index, "candidate_count": count})
    assert total == 4704

    samples = []
    sample_rows = (0, 9, 18, 27, 36, 45, 54, 63)
    sample_s = (S_LOWER, Q(0), S_UPPER)
    for sample_index, row_index in enumerate(sample_rows):
        row = rows[row_index]
        t_value = Q(2 * sample_index + 3, 20)
        s_value = sample_s[sample_index % len(sample_s)]
        miss_obstacle, miss_ix, miss_iy = prior.parse_target(row["miss_target"])
        relative_id = sorted(
            candidate[3]
            for candidate in prior.shifted_candidates(
                miss_obstacle, miss_ix, miss_iy
            )
        )[sample_index % per_row_counts[row_index]["candidate_count"]]
        t = Jet2.t_variable(arbq(t_value))
        s = Jet2.s_variable(arbq(s_value))
        full = second_geometry(row, t, s)["candidates"][relative_id]
        filtered = second_geometry(
            row, t, s, candidate_only=relative_id
        )["candidates"][relative_id]

        def ledger(fields: dict[str, Jet2]) -> dict[str, list[str]]:
            return {
                key: [str(value.value), str(value.dt), str(value.ds)]
                for key, value in sorted(fields.items())
            }

        full_ledger = ledger(full)
        filtered_ledger = ledger(filtered)
        assert full_ledger == filtered_ledger
        samples.append({
            "row_index": row_index,
            "t": str(t_value),
            "s": str(s_value),
            "candidate": relative_id,
            "field_ledger_sha256": canonical_digest(full_ledger),
        })

    return {
        "candidate_discriminant_function_count": total,
        "per_row_candidate_counts_sha256": canonical_digest(per_row_counts),
        "candidate_only_full_equivalence_sample_count": len(samples),
        "candidate_only_full_equivalence_samples_sha256": canonical_digest(samples),
        "candidate_only_full_equivalence": True,
    }


def mean_value_enclosure(
    centre: arb, dt: arb, ds: arb, t_radius: Q, s_radius: Q,
) -> arb:
    return (
        centre
        + dt * arb_interval(-t_radius, t_radius)
        + ds * arb_interval(-s_radius, s_radius)
    )


def field_enclosure(
    centre: Jet2, box: Jet2, t_radius: Q, s_radius: Q,
) -> arb:
    return mean_value_enclosure(centre.value, box.dt, box.ds, t_radius, s_radius)


def sign_of(value: arb) -> int:
    if bool(value > 0):
        return 1
    if bool(value < 0):
        return -1
    return 0


def centre_owner(geometry: dict[str, Any]) -> str | None:
    """Select the first strict next root at one point, if it is regular."""

    candidates = []
    for relative_id, fields in geometry["candidates"].items():
        projection = fields["projection"].value
        discriminant = fields["discriminant"].value
        if not bool(discriminant > 0):
            continue
        root = projection - discriminant.sqrt()
        far = projection + discriminant.sqrt()
        if bool(far < 0) or not bool(root > 0) or not bool(root < arbq(TAU_MAX)):
            continue
        candidates.append((relative_id, root))
    winners = [
        candidate
        for candidate in candidates
        if all(
            other is candidate or bool(candidate[1] < other[1])
            for other in candidates
        )
    ]
    return winners[0][0] if len(winners) == 1 else None


def geometry_on_box(
    row: dict[str, Any], t0: Q, t1: Q, s0: Q, s1: Q,
) -> tuple[dict[str, Any], dict[str, Any]]:
    tm, sm = (t0 + t1) / 2, (s0 + s1) / 2
    box = second_geometry(
        row,
        Jet2.t_variable(arb_interval(t0, t1)),
        Jet2.s_variable(arb_interval(s0, s1)),
    )
    centre = second_geometry(
        row,
        Jet2.t_variable(arbq(tm)),
        Jet2.s_variable(arbq(sm)),
    )
    return centre, box


def discriminant_on_edge(
    row: dict[str, Any], relative_id: str, t: Q, s0: Q, s1: Q,
) -> arb:
    sm = (s0 + s1) / 2
    s_radius = (s1 - s0) / 2
    box = second_geometry(
        row,
        Jet2.t_variable(arbq(t)),
        Jet2.s_variable(arb_interval(s0, s1)),
        candidate_only=relative_id,
    )["candidates"][relative_id]["discriminant"]
    centre = second_geometry(
        row,
        Jet2.t_variable(arbq(t)),
        Jet2.s_variable(arbq(sm)),
        candidate_only=relative_id,
    )["candidates"][relative_id]["discriminant"]
    return mean_value_enclosure(centre.value, box.dt, box.ds, Q(0), s_radius)


@dataclass(frozen=True)
class FutureBox:
    row_index: int
    t0: Q
    t1: Q
    v0: Q
    v1: Q
    t_depth: int
    v_depth: int

    @property
    def s0(self) -> Q:
        return S_LOWER + (S_UPPER - S_LOWER) * self.v0

    @property
    def s1(self) -> Q:
        return S_LOWER + (S_UPPER - S_LOWER) * self.v1

    @property
    def area(self) -> Q:
        return (self.t1 - self.t0) * (self.v1 - self.v0)

    def split_t(self) -> tuple["FutureBox", "FutureBox"]:
        middle = (self.t0 + self.t1) / 2
        return (
            FutureBox(self.row_index, self.t0, middle, self.v0, self.v1,
                      self.t_depth + 1, self.v_depth),
            FutureBox(self.row_index, middle, self.t1, self.v0, self.v1,
                      self.t_depth + 1, self.v_depth),
        )

    def split_v(self) -> tuple["FutureBox", "FutureBox"]:
        middle = (self.v0 + self.v1) / 2
        return (
            FutureBox(self.row_index, self.t0, self.t1, self.v0, middle,
                      self.t_depth, self.v_depth + 1),
            FutureBox(self.row_index, self.t0, self.t1, middle, self.v1,
                      self.t_depth, self.v_depth + 1),
        )


def audit_box(row: dict[str, Any], box: FutureBox) -> tuple[str, dict[str, Any]]:
    """Type a rectangle as immutable, one-root strip, or unresolved."""

    t_radius = (box.t1 - box.t0) / 2
    s_radius = (box.s1 - box.s0) / 2
    try:
        centre, interval = geometry_on_box(
            row, box.t0, box.t1, box.s0, box.s1
        )
        prerequisites = {}
        for key in ("source_cp", "miss_delta", "miss_root_gap"):
            value = field_enclosure(
                centre[key], interval[key], t_radius, s_radius
            )
            prerequisites[key] = str(value)
            if not bool(value > 0):
                return "analytic_unresolved", {
                    "reason": f"{key}_not_strict", **prerequisites
                }

        # It is neither necessary nor correct to cut at a tangency that lies
        # behind the already certified first next collision.  First certify
        # the centre owner, then compare its entire root enclosure against
        # every possible competitor (including a discriminant interval that
        # straddles zero).  This is the dependency-reduced version of the
        # frozen s=0 owner test.
        owner = centre_owner(centre)
        if owner is None:
            return "owner_unresolved", {"reason": "centre_owner_not_unique"}
        owner_centre = centre["candidates"][owner]
        owner_interval = interval["candidates"][owner]
        owner_d = field_enclosure(
            owner_centre["discriminant"], owner_interval["discriminant"],
            t_radius, s_radius,
        )
        owner_p = field_enclosure(
            owner_centre["projection"], owner_interval["projection"],
            t_radius, s_radius,
        )
        if not bool(owner_d > 0):
            blockers = [owner]
            owner_root = None
        else:
            owner_root = owner_p - owner_d.sqrt()
            if not (bool(owner_root > 0) and bool(owner_root < arbq(TAU_MAX))):
                return "owner_unresolved", {
                    "reason": "centre_owner_not_uniformly_forward"
                }
            blockers = []

        comparison_signs: dict[str, str] = {}
        if owner_root is not None:
            for relative_id in sorted(interval["candidates"]):
                if relative_id == owner:
                    continue
                centre_fields = centre["candidates"][relative_id]
                box_fields = interval["candidates"][relative_id]
                discriminant = field_enclosure(
                    centre_fields["discriminant"], box_fields["discriminant"],
                    t_radius, s_radius,
                )
                projection = field_enclosure(
                    centre_fields["projection"], box_fields["projection"],
                    t_radius, s_radius,
                )
                if bool(discriminant < 0):
                    comparison_signs[relative_id] = "strict_miss"
                    continue
                upper = discriminant.upper()
                if bool(upper < 0):
                    comparison_signs[relative_id] = "strict_miss"
                    continue
                radical_upper = upper.sqrt()
                possible_near_lower = projection.lower() - radical_upper
                possible_far_upper = projection.upper() + radical_upper
                if bool(possible_far_upper < 0):
                    comparison_signs[relative_id] = "strict_behind"
                    continue
                if bool(possible_near_lower > arbq(TAU_MAX)):
                    comparison_signs[relative_id] = "strict_after_tau3"
                    continue
                if bool(owner_root < possible_near_lower):
                    comparison_signs[relative_id] = "strictly_after_owner"
                    continue
                blockers.append(relative_id)

        if not blockers:
            return "immutable", {
                "next_target_relative_to_miss_source": owner,
                "owner_root_enclosure": str(owner_root),
                "competitor_comparison_digest": canonical_digest(comparison_signs),
                "strict_competitor_count": len(comparison_signs),
            }

        # A terminal transverse strip is allowed only when the sole blocker
        # is a discriminant zero.  Positive-root order uncertainty is merely
        # interval dependency and is refined rather than rebranded as a
        # physical singularity.
        zero_candidates = []
        for relative_id in blockers:
            centre_d = centre["candidates"][relative_id]["discriminant"]
            box_d = interval["candidates"][relative_id]["discriminant"]
            enclosure = field_enclosure(centre_d, box_d, t_radius, s_radius)
            if enclosure.contains(0):
                zero_candidates.append(relative_id)

        if len(blockers) == 1 and len(zero_candidates) == 1:
            relative_id = blockers[0]
            derivative = interval["candidates"][relative_id]["discriminant"].dt
            if not derivative.contains(0):
                left = discriminant_on_edge(
                    row, relative_id, box.t0, box.s0, box.s1
                )
                right = discriminant_on_edge(
                    row, relative_id, box.t1, box.s0, box.s1
                )
                if sign_of(left) * sign_of(right) == -1:
                    if box.t1 - box.t0 <= ROOT_T_WIDTH:
                        dt_lower = min(
                            abs(derivative.lower()), abs(derivative.upper())
                        )
                        ds_field = interval["candidates"][relative_id][
                            "discriminant"
                        ].ds
                        ds_upper = max(abs(ds_field.lower()), abs(ds_field.upper()))
                        # ds/dv=(ds/ds)/(dt/dt) * (1/200).  An integer
                        # ceiling is deliberately used so the later graph
                        # length and tubular-collar arithmetic is rational.
                        normalized_slope = ds_upper / dt_lower / 200
                        slope_ceiling_ball = normalized_slope.upper().ceil()
                        slope_ceiling_fmpz = slope_ceiling_ball.unique_fmpz()
                        assert slope_ceiling_fmpz is not None
                        normalized_slope_ceiling = int(slope_ceiling_fmpz)
                        return "transverse_root_strip", {
                            "candidate_relative_to_miss_source": relative_id,
                            "dt_discriminant_enclosure": str(derivative),
                            "left_edge_sign": sign_of(left),
                            "right_edge_sign": sign_of(right),
                            "unique_root_for_every_s_in_slab": True,
                            "normalized_dt_dv_absolute_slope_integer_upper": (
                                normalized_slope_ceiling
                            ),
                        }
                    return "refine_t", {
                        "reason": "root_strip_too_wide",
                        "candidate_relative_to_miss_source": relative_id,
                    }
                dt_lower = min(abs(derivative.lower()), abs(derivative.upper()))
                ds_upper = max(
                    abs(interval["candidates"][relative_id]["discriminant"].ds.lower()),
                    abs(interval["candidates"][relative_id]["discriminant"].ds.upper()),
                )
                root_drift = ds_upper * arbq(box.s1 - box.s0) / dt_lower
                preferred = "refine_v" if bool(root_drift > arbq(box.t1 - box.t0) / 2) else "refine_t"
                return preferred, {
                    "reason": "transverse_candidate_not_bracketed_on_full_s_slab",
                    "candidate_relative_to_miss_source": relative_id,
                    "dt_discriminant_enclosure": str(derivative),
                    "root_drift_upper": str(root_drift),
                }
            return "refine_t", {
                "reason": "single_zero_candidate_dt_requires_t_refinement",
                "candidate_relative_to_miss_source": relative_id,
                "dt_discriminant_enclosure": str(derivative),
            }
        return "multi_or_tangent_unresolved", {
            "reason": "multiple_blockers_positive_order_or_dt_zero",
            "blocker_count": len(blockers),
            "zero_candidate_count": len(zero_candidates),
            "blockers_digest": canonical_digest(blockers),
            "zero_candidates_digest": canonical_digest(zero_candidates),
        }
    except (AssertionError, ValueError, ZeroDivisionError) as exc:
        return "analytic_unresolved", {
            "reason": "interval_geometry_exception",
            "exception_type": type(exc).__name__,
        }


def initial_boxes_for_row(row_index: int) -> list[FutureBox]:
    return [
        FutureBox(
            row_index,
            Q(ti, INITIAL_T_CELLS),
            Q(ti + 1, INITIAL_T_CELLS),
            Q(vi, INITIAL_V_CELLS),
            Q(vi + 1, INITIAL_V_CELLS),
            0,
            0,
        )
        for vi in range(INITIAL_V_CELLS)
        for ti in range(INITIAL_T_CELLS)
    ]


def audit_one_row(
    task: tuple[int, dict[str, Any]],
) -> dict[str, Any]:
    """Worker-local adaptive replay for one disjoint occurrence square."""

    row_index, row = task
    pending = initial_boxes_for_row(row_index)
    immutable_rows: list[dict[str, Any]] = []
    root_rows: list[dict[str, Any]] = []
    unresolved_rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    owner_counts: Counter[str] = Counter()
    root_candidate_counts: Counter[str] = Counter()
    depth_counts: Counter[str] = Counter()
    immutable_area = Q(0)
    root_area = Q(0)
    unresolved_area = Q(0)
    audit_call_count = 0

    while pending:
        box = pending.pop()
        audit_call_count += 1
        status, witness = audit_box(row, box)

        # A bracketed root is narrowed in t.  A transverse but unbracketed
        # root is first narrowed in parameter, while natural-interval
        # failures are narrowed in the larger normalized coordinate.
        if status == "refine_t" and box.t_depth < MAX_T_DEPTH:
            pending.extend(reversed(box.split_t()))
            continue
        if status == "refine_t" and box.v_depth < MAX_V_DEPTH:
            pending.extend(reversed(box.split_v()))
            continue
        if status == "refine_v" and box.v_depth < MAX_V_DEPTH:
            pending.extend(reversed(box.split_v()))
            continue
        if status == "refine_v" and box.t_depth < MAX_T_DEPTH:
            pending.extend(reversed(box.split_t()))
            continue
        if status in {
            "analytic_unresolved", "owner_unresolved",
            "multi_or_tangent_unresolved",
        }:
            if box.t_depth < MAX_T_DEPTH:
                pending.extend(reversed(box.split_t()))
                continue
            if box.v_depth < MAX_V_DEPTH:
                pending.extend(reversed(box.split_v()))
                continue

        base = {
            "row_index": box.row_index,
            "occurrence_id": row["occurrence_id"],
            "t": [str(box.t0), str(box.t1)],
            "v": [str(box.v0), str(box.v1)],
            "v_interval_ownership": "[v0,v1), except the final v1=1 endpoint is closed",
            "s": [str(box.s0), str(box.s1)],
            "t_depth": box.t_depth,
            "v_depth": box.v_depth,
            "normalized_parameter_area": str(box.area),
        }
        depth_counts[f"{box.t_depth}:{box.v_depth}"] += 1
        status_counts[status] += 1
        if status == "immutable":
            record = {**base, **witness}
            record["component_index"] = (
                "fs2:" + canonical_digest(record)[:24]
            )
            immutable_rows.append(record)
            immutable_area += box.area
            owner_counts[witness["next_target_relative_to_miss_source"]] += 1
        elif status == "transverse_root_strip":
            root_rows.append({**base, **witness})
            root_area += box.area
            root_candidate_counts[
                witness["candidate_relative_to_miss_source"]
            ] += 1
        else:
            unresolved_rows.append({**base, "terminal_status": status, **witness})
            unresolved_area += box.area

    immutable_rows.sort(key=canonical_json)
    root_rows.sort(key=canonical_json)
    unresolved_rows.sort(key=canonical_json)
    all_rows = immutable_rows + root_rows + unresolved_rows
    event_map: dict[Q, Counter[str]] = {}
    for kind, records in (
        ("all", all_rows),
        ("root", root_rows),
        ("unresolved", unresolved_rows),
    ):
        for record in records:
            v0, v1 = Q(record["v"][0]), Q(record["v"][1])
            width = Q(record["t"][1]) - Q(record["t"][0])
            for endpoint, sign in ((v0, 1), (v1, -1)):
                event = event_map.setdefault(endpoint, Counter())
                event[f"{kind}_count"] += sign
                if kind == "unresolved":
                    event["unresolved_width"] += sign * width

    perimeter_sum = sum(
        2 * (
            Q(record["t"][1]) - Q(record["t"][0])
            + Q(record["v"][1]) - Q(record["v"][0])
        )
        for record in all_rows
    )
    unresolved_perimeter_sum = sum(
        2 * (
            Q(record["t"][1]) - Q(record["t"][0])
            + Q(record["v"][1]) - Q(record["v"][0])
        )
        for record in unresolved_rows
    )
    root_graph_length_upper = sum(
        (Q(record["v"][1]) - Q(record["v"][0]))
        * (1 + record["normalized_dt_dv_absolute_slope_integer_upper"])
        for record in root_rows
    )
    record_digest_ledger = {
        "row_index": row_index,
        "immutable_count": len(immutable_rows),
        "immutable_digest": canonical_digest(immutable_rows),
        "root_count": len(root_rows),
        "root_digest": canonical_digest(root_rows),
        "unresolved_count": len(unresolved_rows),
        "unresolved_digest": canonical_digest(unresolved_rows),
    }
    return {
        "row_index": row_index,
        "record_digest_ledger": record_digest_ledger,
        "immutable_count": len(immutable_rows),
        "root_count": len(root_rows),
        "unresolved_count": len(unresolved_rows),
        "status_counts": status_counts,
        "owner_counts": owner_counts,
        "root_candidate_counts": root_candidate_counts,
        "depth_counts": depth_counts,
        "immutable_area": immutable_area,
        "root_area": root_area,
        "unresolved_area": unresolved_area,
        "perimeter_sum": perimeter_sum,
        "unresolved_perimeter_sum": unresolved_perimeter_sum,
        "root_graph_length_upper": root_graph_length_upper,
        "all_root_strips_strict": all(
            record["unique_root_for_every_s_in_slab"] for record in root_rows
        ),
        "event_map": {
            str(endpoint): dict(event)
            for endpoint, event in sorted(event_map.items())
        },
        "audit_call_count": audit_call_count,
    }


def finite_s_future_outer_atlas(rows: list[dict[str, Any]]) -> dict[str, Any]:
    requested_workers = int(os.environ.get("CM2_WORKERS", "40"))
    assert 1 <= requested_workers <= 64
    worker_count = min(requested_workers, os.cpu_count() or 1, len(rows))
    context = multiprocessing.get_context("fork")
    with context.Pool(processes=worker_count) as pool:
        partials = list(pool.imap_unordered(
            audit_one_row, list(enumerate(rows)), chunksize=1
        ))
    partials.sort(key=lambda partial: partial["row_index"])
    assert [partial["row_index"] for partial in partials] == list(range(64))

    status_counts: Counter[str] = Counter()
    owner_counts: Counter[str] = Counter()
    root_candidate_counts: Counter[str] = Counter()
    depth_counts: Counter[str] = Counter()
    immutable_area = Q(0)
    root_area = Q(0)
    unresolved_area = Q(0)
    immutable_count = 0
    root_count = 0
    unresolved_count = 0
    perimeter_sum = Q(0)
    unresolved_perimeter_sum = Q(0)
    root_graph_length_upper = Q(0)
    all_root_strips_strict = True
    audit_call_count = 0
    slice_events: dict[Q, Counter[str]] = {}
    for partial in partials:
        status_counts.update(partial["status_counts"])
        owner_counts.update(partial["owner_counts"])
        root_candidate_counts.update(partial["root_candidate_counts"])
        depth_counts.update(partial["depth_counts"])
        immutable_area += partial["immutable_area"]
        root_area += partial["root_area"]
        unresolved_area += partial["unresolved_area"]
        immutable_count += partial["immutable_count"]
        root_count += partial["root_count"]
        unresolved_count += partial["unresolved_count"]
        perimeter_sum += partial["perimeter_sum"]
        unresolved_perimeter_sum += partial["unresolved_perimeter_sum"]
        root_graph_length_upper += partial["root_graph_length_upper"]
        all_root_strips_strict = (
            all_root_strips_strict and partial["all_root_strips_strict"]
        )
        audit_call_count += partial["audit_call_count"]
        for endpoint_text, event in partial["event_map"].items():
            endpoint = Q(endpoint_text)
            slice_events.setdefault(endpoint, Counter()).update(event)

    row_digest_ledger = [
        partial["record_digest_ledger"] for partial in partials
    ]
    row_work_ledger = [
        {
            "row_index": partial["row_index"],
            "audit_call_count": partial["audit_call_count"],
            "terminal_leaf_count": (
                partial["immutable_count"]
                + partial["root_count"]
                + partial["unresolved_count"]
            ),
        }
        for partial in partials
    ]
    assert immutable_area + root_area + unresolved_area == 64

    # This is normalized-parameter integrated bookkeeping only.  The v axis
    # is not a probability coordinate, so neither the two-dimensional area
    # nor the following weighted values are called physical mass/current.
    boundary_collar_coefficient = 2 * perimeter_sum
    parameter_integrated_density_weighted_outer = (
        Q(126, 5) * (root_area + unresolved_area)
    )
    parameter_integrated_formal_two_mark_outer = (
        2 * parameter_integrated_density_weighted_outer
    )
    parameter_integrated_density_weighted_boundary = (
        Q(126, 5) * boundary_collar_coefficient
    )
    parameter_integrated_formal_two_mark_boundary = (
        2 * parameter_integrated_density_weighted_boundary
    )

    # Every accepted root strip contains one C1 graph t=t(v).  Its stored
    # integer slope bound gives length <= Delta_v*(1+L).  The rho tube of N
    # such graph arcs has planar area <=2*length*rho+pi*N*rho^2; for rho<=1
    # and pi<4 this is bounded linearly by (2*length+4N)rho.  This is a
    # zero-intercept statement only in normalized two-dimensional parameter
    # geometry; it is not a physical face/current certificate.
    root_graph_collar_coefficient = (
        2 * root_graph_length_upper + 4 * root_count
    )
    parameter_integrated_root_density_weighted_Z = (
        Q(126, 5) * root_graph_collar_coefficient
    )
    parameter_integrated_root_formal_two_mark_Z = (
        2 * parameter_integrated_root_density_weighted_Z
    )
    unresolved_collar_linear = (
        2 * unresolved_perimeter_sum + 4 * unresolved_count
    )
    parameter_integrated_unresolved_density_intercept = (
        Q(126, 5) * unresolved_area
    )
    parameter_integrated_unresolved_density_linear = (
        Q(126, 5) * unresolved_collar_linear
    )

    # The fixed-s sweep is the only layer to which the physical row-density
    # bound may be applied.  Boxes are half-open in v, except that the final
    # v=1 endpoint is owned by the last slab.  We separately track (i) all
    # artificial rectangles, (ii) candidate root graphs, and (iii) terminal
    # unresolved boxes.  Candidate roots need not be physical-first owners.
    active = Counter()
    max_all_count = 0
    max_root_count = 0
    max_unresolved_count = 0
    max_unresolved_width = Q(0)
    max_full_slice_linear_count = 0
    event_rows = []
    endpoints = sorted(slice_events)
    assert endpoints[0] == 0 and endpoints[-1] == 1
    for index, endpoint in enumerate(endpoints[:-1]):
        active.update(slice_events[endpoint])
        next_endpoint = endpoints[index + 1]
        if next_endpoint == endpoint:
            continue
        all_count_on_slice = active["all_count"]
        root_count_on_slice = active["root_count"]
        unresolved_count_on_slice = active["unresolved_count"]
        unresolved_width = active["unresolved_width"]
        assert (
            all_count_on_slice >= 0
            and root_count_on_slice >= 0
            and unresolved_count_on_slice >= 0
            and unresolved_width >= 0
        )
        max_all_count = max(max_all_count, all_count_on_slice)
        max_root_count = max(max_root_count, root_count_on_slice)
        max_unresolved_count = max(
            max_unresolved_count, unresolved_count_on_slice
        )
        max_unresolved_width = max(max_unresolved_width, unresolved_width)
        max_full_slice_linear_count = max(
            max_full_slice_linear_count,
            root_count_on_slice + unresolved_count_on_slice,
        )
        event_rows.append({
            "v": [str(endpoint), str(next_endpoint)],
            "all_artificial_rectangle_count": all_count_on_slice,
            "candidate_root_graph_count": root_count_on_slice,
            "unresolved_box_count": unresolved_count_on_slice,
            "unresolved_t_width_sum": str(unresolved_width),
        })
    active.update(slice_events[endpoints[-1]])
    assert not any(active.values())
    uniform_artificial_t_boundary_Leb_Z = 4 * max_all_count
    uniform_root_slice_Leb_Z = 2 * max_root_count
    uniform_full_slice_linear = 2 * max_full_slice_linear_count
    uniform_artificial_t_boundary_row_density_Z = (
        Q(126, 5) * uniform_artificial_t_boundary_Leb_Z
    )
    uniform_artificial_t_boundary_formal_mark_Z = (
        2 * uniform_artificial_t_boundary_row_density_Z
    )
    uniform_root_row_density_Z = Q(126, 5) * uniform_root_slice_Leb_Z
    uniform_root_formal_mark_Z = 2 * uniform_root_row_density_Z
    uniform_full_row_density_intercept = Q(126, 5) * max_unresolved_width
    uniform_full_row_density_linear = Q(126, 5) * uniform_full_slice_linear
    uniform_full_formal_mark_intercept = 2 * uniform_full_row_density_intercept
    uniform_full_formal_mark_linear = 2 * uniform_full_row_density_linear

    return {
        "fixed_common_carrier": (
            "disjoint_union_e ([0,1]_t x [0,1]_v), "
            "s=(2v-1)/400"
        ),
        "row_count": 64,
        "candidate_discriminant_function_count": 4704,
        "initial_t_cells_per_row_parameter_slab": INITIAL_T_CELLS,
        "initial_parameter_slabs": INITIAL_V_CELLS,
        "maximum_additional_t_depth": MAX_T_DEPTH,
        "maximum_additional_parameter_depth": MAX_V_DEPTH,
        "accepted_root_strip_t_width_upper": str(ROOT_T_WIDTH),
        "immutable_component_count": immutable_count,
        "transverse_candidate_root_strip_count": root_count,
        "terminal_unresolved_box_count": unresolved_count,
        "immutable_normalized_parameter_area": str(immutable_area),
        "transverse_candidate_root_strip_normalized_parameter_area": str(root_area),
        "terminal_unresolved_normalized_parameter_area": str(unresolved_area),
        "total_bad_outer_cover_normalized_parameter_area": str(
            root_area + unresolved_area
        ),
        "bad_outer_cover_fraction_of_64_row_carrier": str(
            (root_area + unresolved_area) / 64
        ),
        "parameter_integrated_density_weighted_bad_outer_bookkeeping": str(
            parameter_integrated_density_weighted_outer
        ),
        "parameter_integrated_formal_two_mark_bad_outer_bookkeeping": str(
            parameter_integrated_formal_two_mark_outer
        ),
        "parameter_integrated_artificial_rectangle_perimeter_sum": str(
            perimeter_sum
        ),
        "parameter_integrated_artificial_boundary_Leb_collar": (
            "Leb([B]_rho)<=min(64,"
            f"{boundary_collar_coefficient}*rho)"
        ),
        "parameter_integrated_artificial_boundary_Leb_linear_coefficient": str(
            boundary_collar_coefficient
        ),
        "parameter_integrated_artificial_boundary_density_weighted_linear_bookkeeping": str(
            parameter_integrated_density_weighted_boundary
        ),
        "parameter_integrated_artificial_boundary_formal_two_mark_linear_bookkeeping": str(
            parameter_integrated_formal_two_mark_boundary
        ),
        "parameter_integrated_candidate_root_graph_length_upper": str(
            root_graph_length_upper
        ),
        "parameter_integrated_candidate_root_Leb_tube_linear_coefficient": str(
            root_graph_collar_coefficient
        ),
        "parameter_integrated_candidate_root_density_weighted_linear_bookkeeping": str(
            parameter_integrated_root_density_weighted_Z
        ),
        "parameter_integrated_candidate_root_formal_two_mark_linear_bookkeeping": str(
            parameter_integrated_root_formal_two_mark_Z
        ),
        "parameter_integrated_unresolved_rectangle_perimeter_sum": str(
            unresolved_perimeter_sum
        ),
        "parameter_integrated_unresolved_density_weighted_intercept_bookkeeping": str(
            parameter_integrated_unresolved_density_intercept
        ),
        "parameter_integrated_unresolved_density_weighted_linear_bookkeeping": str(
            parameter_integrated_unresolved_density_linear
        ),
        "ordered_row_record_digest_ledger": row_digest_ledger,
        "ordered_row_record_digest_ledger_sha256": canonical_digest(
            row_digest_ledger
        ),
        "row_work_ledger": row_work_ledger,
        "row_work_ledger_sha256": canonical_digest(row_work_ledger),
        "total_audit_call_count": audit_call_count,
        "maximum_audit_calls_on_one_row": max(
            row["audit_call_count"] for row in row_work_ledger
        ),
        "parameter_slice_ledger_sha256": canonical_digest(event_rows),
        "maximum_all_artificial_rectangles_on_one_parameter_slice": max_all_count,
        "maximum_candidate_root_graphs_on_one_parameter_slice": max_root_count,
        "maximum_unresolved_boxes_on_one_parameter_slice": max_unresolved_count,
        "uniform_parameter_slice_unresolved_t_width_outer": str(
            max_unresolved_width
        ),
        "uniform_fixed_s_artificial_rectangular_t_boundary_Leb_Z_linear_coefficient": str(
            uniform_artificial_t_boundary_Leb_Z
        ),
        "uniform_fixed_s_artificial_rectangular_t_boundary_row_law_density_Z_linear_coefficient": str(
            uniform_artificial_t_boundary_row_density_Z
        ),
        "uniform_fixed_s_artificial_rectangular_t_boundary_formal_two_mark_Z_linear_coefficient": str(
            uniform_artificial_t_boundary_formal_mark_Z
        ),
        "uniform_fixed_s_candidate_root_Leb_Z_linear_coefficient": str(
            uniform_root_slice_Leb_Z
        ),
        "uniform_fixed_s_candidate_root_row_law_density_Z_linear_coefficient": str(
            uniform_root_row_density_Z
        ),
        "uniform_fixed_s_candidate_root_formal_two_mark_Z_linear_coefficient": str(
            uniform_root_formal_mark_Z
        ),
        "uniform_fixed_s_future_candidate_row_law_density_outer_intercept": str(
            uniform_full_row_density_intercept
        ),
        "uniform_fixed_s_future_candidate_row_law_density_outer_linear_coefficient": str(
            uniform_full_row_density_linear
        ),
        "uniform_fixed_s_future_candidate_formal_two_mark_outer_intercept": str(
            uniform_full_formal_mark_intercept
        ),
        "uniform_fixed_s_future_candidate_formal_two_mark_outer_linear_coefficient": str(
            uniform_full_formal_mark_linear
        ),
        "uniform_fixed_s_full_future_zero_intercept_Z": (
            max_unresolved_width == 0
        ),
        "status_counts": dict(sorted(status_counts.items())),
        "owner_leaf_counts": dict(sorted(owner_counts.items())),
        "root_candidate_leaf_counts": dict(sorted(root_candidate_counts.items())),
        "terminal_depth_counts": dict(sorted(depth_counts.items())),
        "all_root_strips_have_strict_dt_and_opposite_vertical_edge_signs": (
            all_root_strips_strict
        ),
        "outer_cover_is_not_singularity_mass": True,
        "v_half_open_except_last_closed": True,
        "v_is_not_probability_coordinate": True,
        "two_dimensional_bookkeeping_is_nonphysical_parameter_integrated": True,
        "root_graphs_not_certified_physical_first": True,
        "formal_two_point_mark_not_physical_current": True,
        "fixed_s_row_law_bounds_are_outer_charges_not_face_current_certificates": True,
        "uniform_fixed_s_artificial_rectangular_t_boundary_Z": True,
        "finite_common_future_singularity_outer_atlas": True,
        "finite_common_root_isolated_complete_atlas": unresolved_count == 0,
        "scope": (
            "one future collision after the maximal-row miss trace, over "
            "the full finite-s window; candidate-root and unresolved strips "
            "are retained as an outer cover; only fixed-s slice row-law "
            "outer charges are physical, and no face/current/strong-space/DQ "
            "claim is made"
        ),
    }


def load_dependencies() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    prior_manifest = json.loads(PRIOR_MANIFEST.read_text(encoding="utf-8"))
    finite_manifest = json.loads(FINITE_MANIFEST.read_text(encoding="utf-8"))
    assert prior_manifest["verdict"]["genuine_s0_depth_two_full_measure_atlas"] == "CERTIFIED"
    assert prior_manifest["verdict"]["finite_s_depth_two_registry"] == "NOT_CERTIFIED"
    assert finite_manifest["verdict"]["finite_s_common_endpoint_mesh"] == "CERTIFIED"
    rows, provenance = prior.load_dependencies()
    assert len(rows) == 64
    return rows, {
        "prior_iterated_atlas_manifest_sha256": file_sha256(PRIOR_MANIFEST),
        "finite_s_common_mesh_manifest_sha256": file_sha256(FINITE_MANIFEST),
        "prior_iterated_atlas_cert_sha256": file_sha256(Path(prior.__file__).resolve()),
        "finite_s_common_mesh_cert_sha256": file_sha256(Path(finite.__file__).resolve()),
        "maximal_row_registry_sha256": provenance["maximal_row_registry_sha256"],
    }


def build_manifest() -> dict[str, Any]:
    rows, provenance = load_dependencies()
    candidate_audit = candidate_universe_and_filter_audit(rows)
    atlas = finite_s_future_outer_atlas(rows)
    result = {
        "schema": "cm2.gate3.finite-s-future-singularity-outer-atlas.v1",
        "provenance": provenance,
        "candidate_universe_and_filter_audit": candidate_audit,
        "future_outer_atlas": atlas,
        "scope_limits": {
            "full_finite_s_parameter_window": True,
            "fixed_finite_rectangular_common_carrier": True,
            "strictly_quantified_bad_parameter_outer_cover": True,
            "uniform_fixed_s_artificial_rectangular_t_boundary_Z": True,
            "uniform_fixed_s_candidate_root_outer_Z": True,
            "uniform_fixed_s_future_candidate_row_law_outer_charge": True,
            "two_dimensional_v_average_is_physical_mass_or_current": False,
            "candidate_root_graphs_are_certified_physical_first": False,
            "formal_two_point_mark_is_physical_current": False,
            "physical_face_or_current_on_future_atlas": False,
            "complete_root_isolated_future_atlas": atlas[
                "finite_common_root_isolated_complete_atlas"
            ],
            "strong_source_invariance": False,
            "operator_norm_depth_two_DQ": False,
            "fixed_time_branch_record_MT_DQ": False,
            "physical_FACE_2CUT": False,
            "physical_FACE_TIME": False,
            "gate3_certified": False,
        },
        "exact_remaining_blockers": [
            "eliminate or analytically dominate every fixed-s terminal unresolved outer interval",
            "type candidate root graphs by physical-first owner and construct the physical marked current",
            "prove strong-space invariance for every immutable/root-strip restriction",
            "prove operator-norm one-step DQ and common dynamic-test BL convergence",
            "propagate regular/face/product-current/response types on the physical subatlas",
            "close physical FACE_2CUT/FACE_TIME and the no-|s|^-1 per-depth estimate",
        ],
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


if __name__ == "__main__":
    print(json.dumps(build_manifest(), sort_keys=True, indent=2))
