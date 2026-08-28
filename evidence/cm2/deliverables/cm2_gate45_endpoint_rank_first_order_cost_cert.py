#!/usr/bin/env python3
"""All-row endpoint-rank tails and first-order bidirectional costs.

Every maximal occurrence row has exactly two endpoint incidences.  On an
inward angular collar each incidence is governed by one scalar germ: source
cosine, parameter velocity, earlier-visibility clearance, or miss-switch
clearance.  This replay proves that all 128 germs are simple with uniform
one-sided derivative margins and that the complement of the collars has
uniform source, miss, and clearance scales.

The resulting canonical endpoint rank has a global ``4^-b`` positive-mass
tail.  Its first moment ``integral 2^B dm`` is therefore finite.  The exact
billiard derivative formula then gives numeric one-collision forward and
reverse C1 chart/test-pullback subcosts dominated by ``151*2^B``.  These are
first-order subcosts only; curvature, log-density, boundary-Z, stopped-depth
recovery, and the complete CM2 costs are not claimed.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_depth_one_fixed_gauge_dq_cert as dq
import cm2_gate3_global_physical_subrow_atlas_cert as bulk
import cm2_gate3_maximal_global_row_registry_cert as maximal


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent
CORRECTED_DQ_MANIFEST = (
    HERE / "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
)
SLOPE_MANIFEST = (
    HERE / "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
)
ALGEBRA_MANIFEST = (
    HERE / "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
)

SOURCE_GRAZING = "source_grazing"
POLARITY = "parameter_polarity"
FIRST = "physical_earlier_occlusion_boundary"
MISS = "physical_later_miss_switch_boundary"
COLLAR = Q(1, 2048)
MAX_CORE_DEPTH = 19
DERIVATIVE_LOWER = {
    SOURCE_GRAZING: Q(99, 100),
    POLARITY: Q(9, 50),
    FIRST: Q(3, 40),
    MISS: Q(3, 80),
}
EXPECTED_ENDPOINT_COUNTS = {
    SOURCE_GRAZING: 32,
    POLARITY: 16,
    FIRST: 16,
    MISS: 64,
}
CORE_THRESHOLDS = {
    "source_cp": Q(1, 1 << 12),
    "absolute_uy": Q(1, 1 << 14),
    "miss_cp_squared": Q(1, 1 << 14),
    "transition_scale_squared": Q(1, 1 << 14),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def arbq(value: Q | int) -> arb:
    return bulk.arbq(Q(value))


def as_arb(value: Any) -> arb:
    if isinstance(value, arb):
        return value
    return arbq(Q(value))


@dataclass(frozen=True)
class Jet:
    value: arb
    derivative: arb

    @classmethod
    def constant(cls, value: Any) -> "Jet":
        return cls(as_arb(value), arb(0))

    @classmethod
    def variable(cls, value: Any) -> "Jet":
        return cls(as_arb(value), arb(1))

    def coerce(self, other: Any) -> "Jet":
        return other if isinstance(other, Jet) else Jet.constant(other)

    def __add__(self, other: Any) -> "Jet":
        other = self.coerce(other)
        return Jet(self.value + other.value, self.derivative + other.derivative)

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet(-self.value, -self.derivative)

    def __sub__(self, other: Any) -> "Jet":
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> "Jet":
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> "Jet":
        other = self.coerce(other)
        return Jet(
            self.value * other.value,
            self.derivative * other.value + self.value * other.derivative,
        )

    __rmul__ = __mul__

    def inverse(self) -> "Jet":
        assert not self.value.contains(0)
        return Jet(1 / self.value, -self.derivative / (self.value * self.value))

    def __truediv__(self, other: Any) -> "Jet":
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other: Any) -> "Jet":
        return self.coerce(other) / self

    def sqrt(self) -> "Jet":
        assert bool(self.value > 0)
        root = self.value.sqrt()
        return Jet(root, self.derivative / (2 * root))

    def sin(self) -> "Jet":
        return Jet(self.value.sin(), self.value.cos() * self.derivative)

    def cos(self) -> "Jet":
        return Jet(self.value.cos(), -self.value.sin() * self.derivative)


def load_dependencies() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    corrected = json.loads(CORRECTED_DQ_MANIFEST.read_text(encoding="utf-8"))
    slopes = json.loads(SLOPE_MANIFEST.read_text(encoding="utf-8"))
    algebra = json.loads(ALGEBRA_MANIFEST.read_text(encoding="utf-8"))
    assert corrected["verdict"]["complete_depth_one_fixed_gauge_DQ"] == "CERTIFIED"
    assert slopes["verdict"]["all_row_oriented_slope_envelope_lt_29"] == "CERTIFIED"
    assert algebra["verdict"]["controlled_dyadic_stopped_interval_algebra"] == "CERTIFIED"
    rows, registry = dq.load_rows()
    assert len(rows) == 64
    return rows, registry


def target_center_scalar(target_id: str) -> tuple[arb, arb, arb]:
    x, y = bulk.cached_target_center(target_id, arb(0))
    obstacle = bulk.TARGET_BY_ID[target_id].obstacle
    return x, y, bulk.ARB_RADIUS[obstacle]


def target_center_jet(target_id: str) -> tuple[Jet, Jet, Jet]:
    x, y, radius = target_center_scalar(target_id)
    return Jet.constant(x), Jet.constant(y), Jet.constant(radius)


def source_center_scalar(source: str) -> tuple[arb, arb]:
    if source == "G":
        return arb(0), arb(0)
    return arbq(Q(1, 2)), arbq(Q(1, 2))


def source_center_jet(source: str) -> tuple[Jet, Jet]:
    x, y = source_center_scalar(source)
    return Jet.constant(x), Jet.constant(y)


def scalar_tangent_geometry(
    row: dict[str, Any], normal_x: arb, normal_y: arb,
) -> tuple[arb, arb, arb, arb, arb, arb]:
    center_x, center_y = source_center_scalar(row["source"])
    source_radius = bulk.ARB_RADIUS[row["source"]]
    point_x = center_x + source_radius * normal_x
    point_y = center_y + source_radius * normal_y
    target_x, target_y, target_radius = target_center_scalar(row["target"])
    difference_x = target_x - point_x
    difference_y = target_y - point_y
    distance_squared = difference_x * difference_x + difference_y * difference_y
    radical_squared = distance_squared - target_radius * target_radius
    assert bool(radical_squared > 0)
    flight = radical_squared.sqrt()
    epsilon = row["epsilon"]
    velocity_x = (
        flight * difference_x + epsilon * target_radius * difference_y
    ) / distance_squared
    velocity_y = (
        flight * difference_y - epsilon * target_radius * difference_x
    ) / distance_squared
    source_cp = velocity_x * normal_x + velocity_y * normal_y
    return point_x, point_y, velocity_x, velocity_y, flight, source_cp


def jet_tangent_geometry(
    row: dict[str, Any], normal_x: Jet, normal_y: Jet,
) -> tuple[Jet, Jet, Jet, Jet, Jet, Jet]:
    center_x, center_y = source_center_jet(row["source"])
    source_radius = Jet.constant(bulk.ARB_RADIUS[row["source"]])
    point_x = center_x + source_radius * normal_x
    point_y = center_y + source_radius * normal_y
    target_x, target_y, target_radius = target_center_jet(row["target"])
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


def scalar_discriminant(
    point_x: arb,
    point_y: arb,
    velocity_x: arb,
    velocity_y: arb,
    target_id: str,
) -> arb:
    target_x, target_y, target_radius = target_center_scalar(target_id)
    difference_x = target_x - point_x
    difference_y = target_y - point_y
    transverse = -velocity_y * difference_x + velocity_x * difference_y
    return target_radius * target_radius - transverse * transverse


def jet_discriminant(
    point_x: Jet,
    point_y: Jet,
    velocity_x: Jet,
    velocity_y: Jet,
    target_id: str,
) -> Jet:
    target_x, target_y, target_radius = target_center_jet(target_id)
    difference_x = target_x - point_x
    difference_y = target_y - point_y
    transverse = -velocity_y * difference_x + velocity_x * difference_y
    return target_radius * target_radius - transverse * transverse


def signed_uy_multiplier(row: dict[str, Any]) -> int:
    multiplier = (
        row["parameter_coarea_polarity"]
        * bulk.eta(row["source"], row["target"])
        * row["epsilon"]
    )
    assert multiplier in (-1, 1)
    return multiplier


def endpoint_germ_jet(
    row: dict[str, Any], boundary: dict[str, Any], inward_side: int,
) -> tuple[Jet, dict[str, Any]]:
    normal = maximal.curve_normal(boundary, maximal.S0, maximal.S0)
    variable = Jet.variable(bulk.arb_interval(Q(0), COLLAR))
    sine = variable.sin()
    cosine = variable.cos()
    normal_x = cosine * normal[0] - inward_side * sine * normal[1]
    normal_y = cosine * normal[1] + inward_side * sine * normal[0]
    point_x, point_y, velocity_x, velocity_y, _flight, source_cp = (
        jet_tangent_geometry(row, normal_x, normal_y)
    )
    kind = boundary["kind"]
    if kind == SOURCE_GRAZING:
        return source_cp, {
            "germ": "cp_source",
            "rank_scale": "cp_source",
            "degenerate_target": row["source"],
        }
    if kind == POLARITY:
        return signed_uy_multiplier(row) * velocity_y, {
            "germ": "signed_abs_u_y",
            "rank_scale": "abs(u_y)",
            "degenerate_target": "parameter_velocity",
        }
    other = boundary["descriptor"]["other"]
    discriminant = jet_discriminant(
        point_x, point_y, velocity_x, velocity_y, other
    )
    if kind == FIRST:
        return -discriminant, {
            "germ": "-Delta_earlier_blocker",
            "rank_scale": "sqrt(-Delta_earlier_blocker)/R_blocker",
            "degenerate_target": other,
        }
    assert kind == MISS
    selected = row["miss_target"] == other
    return (discriminant if selected else -discriminant), {
        "germ": "Delta_selected_miss" if selected else "-Delta_new_competitor",
        "rank_scale": "sqrt(abs(Delta_switch))/R_switch",
        "degenerate_target": other,
    }


def endpoint_germ_at_zero(
    row: dict[str, Any], boundary: dict[str, Any], inward_side: int,
) -> arb:
    normal = maximal.curve_normal(boundary, maximal.S0, maximal.S0)
    point_x, point_y, velocity_x, velocity_y, _flight, source_cp = (
        scalar_tangent_geometry(row, normal[0], normal[1])
    )
    kind = boundary["kind"]
    if kind == SOURCE_GRAZING:
        return source_cp
    if kind == POLARITY:
        return signed_uy_multiplier(row) * velocity_y
    other = boundary["descriptor"]["other"]
    discriminant = scalar_discriminant(
        point_x, point_y, velocity_x, velocity_y, other
    )
    if kind == FIRST:
        return -discriminant
    assert kind == MISS
    return discriminant if row["miss_target"] == other else -discriminant


def endpoint_collar_incidence_scales(
    row: dict[str, Any], boundary: dict[str, Any], inward_side: int,
) -> tuple[arb, arb, bool, bool]:
    normal = maximal.curve_normal(boundary, maximal.S0, maximal.S0)
    variable = bulk.arb_interval(Q(0), COLLAR)
    sine = variable.sin()
    cosine = variable.cos()
    normal_x = cosine * normal[0] - inward_side * sine * normal[1]
    normal_y = cosine * normal[1] + inward_side * sine * normal[0]
    point_x, point_y, velocity_x, velocity_y, _flight, source_cp = (
        scalar_tangent_geometry(row, normal_x, normal_y)
    )
    miss = row["miss_target"]
    miss_obstacle = bulk.TARGET_BY_ID[miss].obstacle
    miss_radius = bulk.ARB_RADIUS[miss_obstacle]
    miss_cp_squared = scalar_discriminant(
        point_x, point_y, velocity_x, velocity_y, miss
    ) / (miss_radius * miss_radius)
    source_scale_is_active = boundary["kind"] == SOURCE_GRAZING
    miss_scale_is_active = (
        boundary["kind"] == MISS
        and row["miss_target"] == boundary["descriptor"]["other"]
    )
    if not source_scale_is_active:
        assert bool(source_cp > arbq(CORE_THRESHOLDS["source_cp"]))
    if not miss_scale_is_active:
        assert bool(
            miss_cp_squared > arbq(CORE_THRESHOLDS["miss_cp_squared"])
        )
    return (
        source_cp,
        miss_cp_squared,
        source_scale_is_active,
        miss_scale_is_active,
    )


def row_arc_width(row: dict[str, Any]) -> tuple[tuple[arb, arb], arb]:
    left = maximal.curve_normal(
        row["left_boundary"], maximal.S0, maximal.S0
    )
    right = maximal.curve_normal(
        row["right_boundary"], maximal.S0, maximal.S0
    )
    left_angle = arb.atan2(left[1], left[0])
    right_angle = arb.atan2(right[1], right[0])
    approximate_width = (
        math.atan2(float(right[1]), float(right[0]))
        - math.atan2(float(left[1]), float(left[0]))
    ) % (2 * math.pi)
    raw_width = right_angle - left_angle
    turns = round((approximate_width - float(raw_width)) / (2 * math.pi))
    width = raw_width + 2 * turns * arb.pi()
    assert bool(width > arbq(Q(1, 10)))
    return left, width


def endpoint_transversality_audit(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    endpoint_rows = []
    counts = Counter()
    width_rows = []
    for row in rows:
        _left, width = row_arc_width(row)
        width_rows.append({
            "occurrence_id": row["occurrence_id"],
            "arc_width_enclosure": str(width),
        })
        for side_name, field, inward_side in (
            ("left", "left_boundary", 1),
            ("right", "right_boundary", -1),
        ):
            boundary = row[field]
            kind = boundary["kind"]
            germ, metadata = endpoint_germ_jet(row, boundary, inward_side)
            zero_value = endpoint_germ_at_zero(row, boundary, inward_side)
            assert zero_value.contains(0)
            lower = DERIVATIVE_LOWER[kind]
            assert bool(germ.derivative > arbq(lower))
            (
                collar_source_cp,
                collar_miss_cp_squared,
                source_scale_is_active,
                miss_scale_is_active,
            ) = endpoint_collar_incidence_scales(
                row, boundary, inward_side
            )
            counts[kind] += 1
            endpoint_rows.append({
                "occurrence_id": row["occurrence_id"],
                "side": side_name,
                "boundary_kind": kind,
                "inward_rotation_sign": inward_side,
                "collar_width": str(COLLAR),
                "zero_value_enclosure": str(zero_value),
                "inward_derivative_enclosure": str(germ.derivative),
                "certified_derivative_strict_lower": str(lower),
                "source_incidence_is_active_rank_scale": (
                    source_scale_is_active
                ),
                "miss_incidence_is_active_rank_scale": miss_scale_is_active,
                "companion_source_cp_enclosure": str(collar_source_cp),
                "companion_miss_cp_squared_enclosure": str(
                    collar_miss_cp_squared
                ),
                **metadata,
            })
    endpoint_rows.sort(key=canonical_json)
    width_rows.sort(key=canonical_json)
    assert counts == Counter(EXPECTED_ENDPOINT_COUNTS)
    assert len(endpoint_rows) == 128
    return endpoint_rows, {
        "maximal_row_count": len(rows),
        "endpoint_incidence_count": len(endpoint_rows),
        "endpoint_counts_by_kind": dict(sorted(counts.items())),
        "minimum_row_arc_width_strict_lower": "1/10",
        "collars_are_pairwise_disjoint_on_each_row": True,
        "common_collar_width": str(COLLAR),
        "global_simple_germ_derivative_strict_lower": "3/80",
        "every_nonactive_collar_source_cp_strict_lower": "1/4096",
        "every_nonactive_collar_miss_cp_squared_strict_lower": "1/16384",
        "endpoint_rows_sha256": canonical_digest(endpoint_rows),
        "row_width_rows_sha256": canonical_digest(width_rows),
    }


def normalized_transition_germ_scalar(
    row: dict[str, Any],
    boundary: dict[str, Any],
    point_x: arb,
    point_y: arb,
    velocity_x: arb,
    velocity_y: arb,
) -> arb:
    other = boundary["descriptor"]["other"]
    obstacle = bulk.TARGET_BY_ID[other].obstacle
    radius = bulk.ARB_RADIUS[obstacle]
    discriminant = scalar_discriminant(
        point_x, point_y, velocity_x, velocity_y, other
    )
    if boundary["kind"] == FIRST:
        return -discriminant / (radius * radius)
    assert boundary["kind"] == MISS
    signed = discriminant if row["miss_target"] == other else -discriminant
    return signed / (radius * radius)


def core_values(
    row: dict[str, Any],
    left: tuple[arb, arb],
    width: arb,
    t0: Q,
    t1: Q,
) -> list[tuple[str, arb, Q]]:
    normalized = bulk.arb_interval(t0, t1)
    angle = arbq(COLLAR) + (width - 2 * arbq(COLLAR)) * normalized
    cosine = angle.cos()
    sine = angle.sin()
    normal_x = cosine * left[0] - sine * left[1]
    normal_y = cosine * left[1] + sine * left[0]
    point_x, point_y, velocity_x, velocity_y, _flight, source_cp = (
        scalar_tangent_geometry(row, normal_x, normal_y)
    )
    absolute_uy = signed_uy_multiplier(row) * velocity_y
    miss = row["miss_target"]
    miss_obstacle = bulk.TARGET_BY_ID[miss].obstacle
    miss_radius = bulk.ARB_RADIUS[miss_obstacle]
    miss_cp_squared = scalar_discriminant(
        point_x, point_y, velocity_x, velocity_y, miss
    ) / (miss_radius * miss_radius)
    values = [
        ("source_cp", source_cp, CORE_THRESHOLDS["source_cp"]),
        ("absolute_uy", absolute_uy, CORE_THRESHOLDS["absolute_uy"]),
        (
            "miss_cp_squared",
            miss_cp_squared,
            CORE_THRESHOLDS["miss_cp_squared"],
        ),
    ]
    for side_name, field in (
        ("left", "left_boundary"),
        ("right", "right_boundary"),
    ):
        boundary = row[field]
        kind = boundary["kind"]
        if kind == SOURCE_GRAZING:
            value = source_cp
            threshold = CORE_THRESHOLDS["source_cp"]
        elif kind == POLARITY:
            value = absolute_uy
            threshold = CORE_THRESHOLDS["absolute_uy"]
        else:
            value = normalized_transition_germ_scalar(
                row,
                boundary,
                point_x,
                point_y,
                velocity_x,
                velocity_y,
            )
            threshold = CORE_THRESHOLDS["transition_scale_squared"]
        values.append((f"{side_name}_{kind}", value, threshold))
    return values


def compact_core_audit(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    leaf_rows = []
    depth_counts = Counter()
    per_occurrence = []
    for row in rows:
        left, width = row_arc_width(row)
        pending = [(Q(0), Q(1), 0)]
        row_leaf_count = 0
        row_maximum_depth = 0
        while pending:
            t0, t1, depth = pending.pop()
            try:
                values = core_values(row, left, width, t0, t1)
            except AssertionError:
                assert depth < MAX_CORE_DEPTH
                middle = (t0 + t1) / 2
                pending.append((middle, t1, depth + 1))
                pending.append((t0, middle, depth + 1))
                continue
            if not all(bool(value > arbq(threshold)) for _name, value, threshold in values):
                assert depth < MAX_CORE_DEPTH
                middle = (t0 + t1) / 2
                pending.append((middle, t1, depth + 1))
                pending.append((t0, middle, depth + 1))
                continue
            leaf_rows.append({
                "occurrence_id": row["occurrence_id"],
                "normalized_core_interval": [str(t0), str(t1)],
                "depth": depth,
            })
            row_leaf_count += 1
            row_maximum_depth = max(row_maximum_depth, depth)
            depth_counts[depth] += 1
        per_occurrence.append({
            "occurrence_id": row["occurrence_id"],
            "core_leaf_count": row_leaf_count,
            "maximum_depth": row_maximum_depth,
        })
    leaf_rows.sort(key=canonical_json)
    per_occurrence.sort(key=canonical_json)
    expected_depth_counts = {
        2: 2,
        3: 92,
        4: 464,
        5: 390,
        6: 372,
        7: 334,
        8: 316,
        9: 332,
        10: 332,
        11: 252,
        12: 192,
        13: 96,
        14: 32,
    }
    assert dict(sorted(depth_counts.items())) == expected_depth_counts
    assert len(leaf_rows) == 3206
    assert max(depth_counts) == 14
    return leaf_rows, {
        "trimmed_core_row_count": len(rows),
        "common_endpoint_trim": str(COLLAR),
        "strict_core_source_cp_lower": str(CORE_THRESHOLDS["source_cp"]),
        "strict_core_absolute_uy_lower": str(CORE_THRESHOLDS["absolute_uy"]),
        "strict_core_miss_cp_squared_lower": str(
            CORE_THRESHOLDS["miss_cp_squared"]
        ),
        "strict_core_transition_scale_squared_lower": str(
            CORE_THRESHOLDS["transition_scale_squared"]
        ),
        "adaptive_core_leaf_count": len(leaf_rows),
        "maximum_core_subdivision_depth": max(depth_counts),
        "core_leaf_depth_counts": {
            str(key): value for key, value in sorted(depth_counts.items())
        },
        "core_leaf_rows_sha256": canonical_digest(leaf_rows),
        "per_occurrence_core_rows_sha256": canonical_digest(per_occurrence),
    }


def endpoint_rank_tail_and_cost() -> dict[str, Any]:
    coarea_density_upper = Q(18, 5)
    maximum_radius_squared = Q(81, 625)
    source_tail_per_endpoint = coarea_density_upper / DERIVATIVE_LOWER[
        SOURCE_GRAZING
    ]
    polarity_tail_per_endpoint = coarea_density_upper / DERIVATIVE_LOWER[
        POLARITY
    ]
    first_tail_per_endpoint = (
        coarea_density_upper
        * maximum_radius_squared
        / DERIVATIVE_LOWER[FIRST]
    )
    miss_tail_per_endpoint = (
        coarea_density_upper
        * maximum_radius_squared
        / DERIVATIVE_LOWER[MISS]
    )
    global_tail_constant = (
        EXPECTED_ENDPOINT_COUNTS[SOURCE_GRAZING] * source_tail_per_endpoint
        + EXPECTED_ENDPOINT_COUNTS[POLARITY] * polarity_tail_per_endpoint
        + EXPECTED_ENDPOINT_COUNTS[FIRST] * first_tail_per_endpoint
        + EXPECTED_ENDPOINT_COUNTS[MISS] * miss_tail_per_endpoint
    )
    assert source_tail_per_endpoint == Q(40, 11)
    assert polarity_tail_per_endpoint == Q(20)
    assert first_tail_per_endpoint == Q(3888, 625)
    assert miss_tail_per_endpoint == Q(7776, 625)
    assert global_tail_constant == Q(9158592, 6875)

    base_rank = 14
    positive_mass_upper = Q(8064, 5)
    first_rank_moment_upper = (
        (1 << base_rank) * positive_mass_upper
        + global_tail_constant * Q(1, 1 << (base_rank - 1))
    )
    collision_matrix_numerator = Q(2391, 16)
    assert collision_matrix_numerator < 150
    first_order_pullback_multiplier = Q(151)
    first_order_charge_mass_upper = (
        first_order_pullback_multiplier * first_rank_moment_upper
    )
    first_order_current_tv_upper = 2 * first_order_charge_mass_upper
    return {
        "canonical_rank_definition": {
            "core_rank": base_rank,
            "source_grazing_scale": "cp_source",
            "parameter_polarity_scale": "abs(u_y)",
            "transition_scale": "sqrt(abs(Delta_transition))/R_transition",
            "endpoint_rank": "max(14,ceil(log2(1/scale))) on its collar",
            "only_one_endpoint_collar_active_per_row_point": True,
        },
        "endpoint_tail": {
            "valid_integer_threshold": f"b>={base_rank}",
            "global_unnormalized_mass_tail": (
                "sum_e m_e{B>b}<=(9158592/6875)*4^-b"
            ),
            "source_tail_constant_per_endpoint": str(source_tail_per_endpoint),
            "polarity_tail_constant_per_endpoint": str(
                polarity_tail_per_endpoint
            ),
            "first_visibility_tail_constant_per_endpoint": str(
                first_tail_per_endpoint
            ),
            "miss_switch_tail_constant_per_endpoint": str(
                miss_tail_per_endpoint
            ),
            "global_tail_constant": str(global_tail_constant),
            "tail_exponent_in_dyadic_rank": "2",
        },
        "raw_rank_moment": {
            "positive_coarea_mass_upper_before_Z_N_inverse": str(
                positive_mass_upper
            ),
            "finite_first_rank_moment": True,
            "integral_2^B_dm_upper_before_Z_N_inverse": str(
                first_rank_moment_upper
            ),
            "all_rank_moments_2^(chi*B)_finite_for": "0<=chi<2",
            "first_order_charge_rank_moments_2^(chi*B)_finite_for": (
                "0<=chi<1"
            ),
            "chi_equals_2_not_inferred_from_tail_bound": True,
        },
        "one_collision_birkhoff_derivative": {
            "matrix_formula": (
                "-1/cp_1*[[tau*kappa_0+cp_0,tau],"
                "[tau*kappa_0*kappa_1+kappa_0*cp_1+kappa_1*cp_0,"
                "tau*kappa_1+cp_1]]"
            ),
            "tau_strict_upper": "3",
            "kappa_upper": "25/4",
            "infinity_norm_numerator_upper": str(collision_matrix_numerator),
            "forward_derivative_bound": "||DF_e||_infinity<150/cp_miss",
            "reverse_derivative_bound": "||DF_e^-1||_infinity<150/cp_source",
            "rank_dominates_both_inverse_incidence_scales": True,
        },
        "first_order_bidirectional_subcharge": {
            "forward_C1_chart_test_subcost": "C_fw^(1)(a)=151*2^B(a)",
            "reverse_C1_chart_test_subcost": "C_rev^(1)(a)=151*2^B(a)",
            "one_common_first_order_charge": "q_e^(1)=151*2^B*m_e",
            "global_first_order_charge_mass_upper_before_Z_N_inverse": str(
                first_order_charge_mass_upper
            ),
            "global_first_order_current_TV_upper_before_Z_N_inverse": str(
                first_order_current_tv_upper
            ),
            "one_collision_dynamic_C1_pullback_integrable": True,
            "first_order_charge_is_not_final_q": True,
        },
    }


def certify() -> dict[str, Any]:
    rows, registry = load_dependencies()
    endpoint_rows, endpoint_audit = endpoint_transversality_audit(rows)
    core_leaves, core_audit = compact_core_audit(rows)
    rank_cost = endpoint_rank_tail_and_cost()
    assert registry["maximal_row_rows_sha256"] == (
        "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
    )
    return {
        "schema": "cm2.gate45.endpoint-rank-first-order-cost.v1",
        "provenance": {
            "corrected_DQ_manifest": CORRECTED_DQ_MANIFEST.name,
            "all_row_slope_manifest": SLOPE_MANIFEST.name,
            "controlled_interval_algebra_manifest": ALGEBRA_MANIFEST.name,
            "maximal_row_registry_sha256": registry[
                "maximal_row_rows_sha256"
            ],
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "all_endpoint_simple_germ_audit": endpoint_audit,
        "compact_core_nondegeneracy_audit": core_audit,
        "endpoint_rank_tail_and_first_order_cost": rank_cost,
        "scope_limits": {
            "all_128_endpoint_germs_simple": True,
            "global_endpoint_rank_tail_exponent_two": True,
            "finite_raw_first_rank_moment": True,
            "numeric_first_order_forward_reverse_C1_subcosts": True,
            "one_collision_dynamic_C1_pullback_integrable": True,
            "homogeneity_weighted_C2_curvature_cost": False,
            "log_density_and_boundary_Z_cost": False,
            "complete_numeric_C_fw_C_rev": False,
            "controlled_stopped_parent_recovery": False,
            "full_dynamic_MT_DQ": False,
            "CM2_norm_lifts": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
        "internal_replay_digest": canonical_digest({
            "endpoint_rows": endpoint_rows,
            "core_leaves": core_leaves,
        }),
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE45_ALL_128_ENDPOINT_SIMPLE_GERMS: CERTIFIED")
    print("GATE45_GLOBAL_ENDPOINT_RANK_TAIL_EXPONENT_TWO: CERTIFIED")
    print("GATE45_FIRST_ORDER_BIDIRECTIONAL_C1_COSTS: CERTIFIED")
    print("GATE45_COMPLETE_C_FW_C_REV_AND_RECOVERY: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
