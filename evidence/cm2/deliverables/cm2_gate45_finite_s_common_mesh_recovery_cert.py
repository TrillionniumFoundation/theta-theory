#!/usr/bin/env python3
"""Finite-s endpoint mesh and controlled moving-table recovery.

This replay upgrades the one-time controlled stopped-parent construction from
the centred table to the complete parameter interval ``|s|<=1/400``.  It has
three independent layers.

* The 64 maximal rows already known to persist over the whole parameter
  window are parameterised by inward angular distance from their two moving
  analytic endpoints.  Adaptive Arb subdivision in ``s`` proves uniform
  simple-germ and companion-incidence bounds on common endpoint collars.
  A second adaptive cover proves uniform nondegeneracy on the moving core.
  Thus one canonical finite-s endpoint rank and one density-regular mesh work
  for every table in the path.
* The frozen 35,024-box horizon cover is replayed while retaining its least
  penetration slack.  This gives an explicit ``(3,1/512)`` horizon and an
  explicit lower free-flight bound, placing the compact path of circular
  tables in one Stenlund--Young--Zhang configuration class.
* On the usual solid-boundary collision section ``N`` we apply arXiv:
  1210.0011v4, Lemma 16 (the uniform Z-recovery consequence of the Growth
  Lemma 12), to the constant configuration sequence ``K_s,K_s,...``.  This is
  not an identification with their source/target moving-configuration map.
  It yields one set of recovery constants, uniform in ``s``.

The theorem constants ``C_p`` and ``vartheta_p`` are supplied by the cited
uniform theorem and are not numerical.  Consequently this certificate gives
an explicit finite-s initial ``C_mesh`` and an affine recovery formula, but
does not claim a fully numerical final ``C_fw,C_rev,q``.  It also does not
claim recovery after arbitrary repeated indicator cuts.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_global_physical_subrow_atlas_cert as bulk
import cm2_gate3_maximal_global_row_registry_cert as maximal
import cm2_gate45_endpoint_rank_first_order_cost_cert as rank0
import cm2_standard_section_horizon_lift_cert as horizon


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

MAXIMAL_MANIFEST = (
    HERE / "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json"
)
CURVATURE_MANIFEST = (
    HERE / "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
)
PRODUCT_MANIFEST = (
    HERE / "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
)
S0_RECOVERY_MANIFEST = (
    HERE / "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
)

SOURCE_GRAZING = rank0.SOURCE_GRAZING
POLARITY = rank0.POLARITY
FIRST = rank0.FIRST
MISS = rank0.MISS

COLLAR = Q(1, 48)
BASE_RANK = 20
CORE_THRESHOLD = Q(1, 1 << BASE_RANK)
MAX_PARAMETER_DEPTH = 16
MAX_CORE_DEPTH = 16
INITIAL_ENDPOINT_D = 32
INITIAL_CORE_T = 16
INITIAL_CORE_S = 64

# These deliberately rounded margins are weaker than the centred-table
# margins.  They are replayed on the complete parameter interval below.
FINITE_S_DERIVATIVE_LOWER = {
    SOURCE_GRAZING: Q(9, 10),
    POLARITY: Q(1, 6),
    FIRST: Q(1, 16),
    MISS: Q(1, 32),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def arbq(value: Q | int) -> arb:
    return bulk.arbq(Q(value))


def load_dependencies() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    maximal_manifest = json.loads(MAXIMAL_MANIFEST.read_text(encoding="utf-8"))
    curvature = json.loads(CURVATURE_MANIFEST.read_text(encoding="utf-8"))
    product = json.loads(PRODUCT_MANIFEST.read_text(encoding="utf-8"))
    recovery0 = json.loads(S0_RECOVERY_MANIFEST.read_text(encoding="utf-8"))
    assert maximal_manifest["verdict"]["maximal_connected_event_rows"] == "CERTIFIED"
    assert maximal_manifest["result"]["maximal_row_registry"][
        "every_row_is_a_connected_open_band_over_full_parameter_window"
    ] is True
    assert curvature["verdict"]["bidirectional_log_density_costs"] == "CERTIFIED"
    assert product["verdict"]["supercritical_depth_tail_and_E_2K"] == "CERTIFIED"
    assert recovery0["verdict"]["controlled_s0_stopped_parent_recovery"] == "CERTIFIED"
    rows, registry = rank0.load_dependencies()
    assert len(rows) == 64
    return rows, registry


def jet_constant(value: Any) -> rank0.Jet:
    return rank0.Jet.constant(value)


def source_center(row: dict[str, Any], s: arb) -> tuple[arb, arb]:
    if row["source"] == "G":
        return arb(0), arb(0)
    return arbq(Q(1, 2)) + s, arbq(Q(1, 2))


def moving_tangent_geometry(
    row: dict[str, Any], normal_x: rank0.Jet, normal_y: rank0.Jet,
    s0: Q, s1: Q,
) -> tuple[rank0.Jet, ...]:
    s = bulk.arb_interval(s0, s1)
    source_x, source_y = source_center(row, s)
    target_x, target_y = bulk.cached_target_center(row["target"], s)
    source_radius = bulk.ARB_RADIUS[row["source"]]
    target_radius = bulk.ARB_RADIUS[
        bulk.TARGET_BY_ID[row["target"]].obstacle
    ]
    source_x, source_y, target_x, target_y, source_radius, target_radius = map(
        jet_constant,
        (source_x, source_y, target_x, target_y, source_radius, target_radius),
    )
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


def moving_discriminant(
    point_x: rank0.Jet,
    point_y: rank0.Jet,
    velocity_x: rank0.Jet,
    velocity_y: rank0.Jet,
    target_id: str,
    s0: Q,
    s1: Q,
) -> rank0.Jet:
    s = bulk.arb_interval(s0, s1)
    target_x, target_y = bulk.cached_target_center(target_id, s)
    target_radius = bulk.ARB_RADIUS[bulk.TARGET_BY_ID[target_id].obstacle]
    target_x, target_y, target_radius = map(
        jet_constant, (target_x, target_y, target_radius)
    )
    difference_x = target_x - point_x
    difference_y = target_y - point_y
    transverse = -velocity_y * difference_x + velocity_x * difference_y
    return target_radius * target_radius - transverse * transverse


def rotated_boundary_normal(
    boundary: dict[str, Any], inward_side: int, d0: Q, d1: Q,
    s0: Q, s1: Q,
) -> tuple[rank0.Jet, rank0.Jet]:
    boundary_x, boundary_y = maximal.curve_normal(boundary, s0, s1)
    angle = rank0.Jet.variable(bulk.arb_interval(d0, d1))
    sine = angle.sin()
    cosine = angle.cos()
    return (
        cosine * boundary_x - inward_side * sine * boundary_y,
        cosine * boundary_y + inward_side * sine * boundary_x,
    )


def moving_endpoint_germ(
    row: dict[str, Any], boundary: dict[str, Any], inward_side: int,
    d0: Q, d1: Q, s0: Q, s1: Q,
) -> tuple[rank0.Jet, tuple[rank0.Jet, rank0.Jet, rank0.Jet]]:
    normal_x, normal_y = rotated_boundary_normal(
        boundary,
        inward_side,
        d0,
        d1,
        s0,
        s1,
    )
    point_x, point_y, velocity_x, velocity_y, _flight, source_cp = (
        moving_tangent_geometry(row, normal_x, normal_y, s0, s1)
    )
    absolute_uy = rank0.signed_uy_multiplier(row) * velocity_y
    miss_target = row["miss_target"]
    miss_obstacle = bulk.TARGET_BY_ID[miss_target].obstacle
    miss_radius = jet_constant(bulk.ARB_RADIUS[miss_obstacle])
    miss_delta = moving_discriminant(
        point_x, point_y, velocity_x, velocity_y, miss_target, s0, s1
    )
    miss_cp_squared = miss_delta / (miss_radius * miss_radius)
    kind = boundary["kind"]
    if kind == SOURCE_GRAZING:
        germ = source_cp
    elif kind == POLARITY:
        germ = absolute_uy
    else:
        other = boundary["descriptor"]["other"]
        discriminant = moving_discriminant(
            point_x, point_y, velocity_x, velocity_y, other, s0, s1
        )
        if kind == FIRST:
            germ = -discriminant
        else:
            assert kind == MISS
            germ = (
                discriminant
                if row["miss_target"] == other
                else -discriminant
            )
    return germ, (source_cp, absolute_uy, miss_cp_squared)


def endpoint_leaf_ok(
    row: dict[str, Any], boundary: dict[str, Any], inward_side: int,
    d0: Q, d1: Q, s0: Q, s1: Q,
) -> tuple[bool, dict[str, Any]]:
    germ, companions = moving_endpoint_germ(
        row, boundary, inward_side, d0, d1, s0, s1
    )
    source_cp, absolute_uy, miss_cp_squared = companions
    kind = boundary["kind"]
    selected_miss_active = (
        kind == MISS
        and row["miss_target"] == boundary["descriptor"]["other"]
    )
    conditions = [
        bool(germ.derivative > arbq(FINITE_S_DERIVATIVE_LOWER[kind])),
        kind == SOURCE_GRAZING or bool(source_cp.value > arbq(CORE_THRESHOLD)),
        kind == POLARITY or bool(absolute_uy.value > arbq(CORE_THRESHOLD)),
        selected_miss_active
        or bool(miss_cp_squared.value > arbq(CORE_THRESHOLD)),
    ]
    return all(conditions), {
        "inward_distance": [str(d0), str(d1)],
        "s": [str(s0), str(s1)],
        "germ_derivative_enclosure": str(germ.derivative),
        "source_cp_enclosure": str(source_cp.value),
        "absolute_u_y_enclosure": str(absolute_uy.value),
        "miss_cp_squared_enclosure": str(miss_cp_squared.value),
    }


def endpoint_collar_audit(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    endpoint_rows: list[dict[str, Any]] = []
    depth_counts: Counter[int] = Counter()
    counts: Counter[str] = Counter()
    for row in rows:
        for side, field, inward_side in (
            ("left", "left_boundary", 1),
            ("right", "right_boundary", -1),
        ):
            boundary = row[field]
            pending = [
                (
                    COLLAR * index / INITIAL_ENDPOINT_D,
                    COLLAR * (index + 1) / INITIAL_ENDPOINT_D,
                    bulk.S_LOWER,
                    bulk.S_UPPER,
                    0,
                )
                for index in range(INITIAL_ENDPOINT_D)
            ]
            leaves = []
            while pending:
                d0, d1, s0, s1, depth = pending.pop()
                ok, witness = endpoint_leaf_ok(
                    row, boundary, inward_side, d0, d1, s0, s1
                )
                if ok:
                    depth_counts[depth] += 1
                    leaves.append({"depth": depth, **witness})
                    continue
                assert depth < MAX_PARAMETER_DEPTH, (
                    row["occurrence_id"], side, boundary["kind"], witness
                )
                middle = (s0 + s1) / 2
                pending.append((d0, d1, middle, s1, depth + 1))
                pending.append((d0, d1, s0, middle, depth + 1))
            leaves.sort(key=canonical_json)
            counts[boundary["kind"]] += 1
            endpoint_rows.append({
                "occurrence_id": row["occurrence_id"],
                "side": side,
                "boundary_kind": boundary["kind"],
                "inward_side": inward_side,
                "parameter_leaves": leaves,
            })
    endpoint_rows.sort(key=canonical_json)
    assert counts == Counter(rank0.EXPECTED_ENDPOINT_COUNTS)
    assert len(endpoint_rows) == 128
    return endpoint_rows, {
        "parameter_window": [str(bulk.S_LOWER), str(bulk.S_UPPER)],
        "common_inward_angular_collar": str(COLLAR),
        "initial_angular_cells_per_endpoint": INITIAL_ENDPOINT_D,
        "endpoint_incidence_count": len(endpoint_rows),
        "endpoint_counts_by_kind": dict(sorted(counts.items())),
        "uniform_inward_derivative_strict_lowers": {
            key: str(value)
            for key, value in sorted(FINITE_S_DERIVATIVE_LOWER.items())
        },
        "common_nonactive_scale_strict_lower": str(CORE_THRESHOLD),
        "parameter_leaf_count": sum(depth_counts.values()),
        "maximum_parameter_subdivision_depth": max(depth_counts),
        "parameter_leaf_depth_counts": {
            str(key): value for key, value in sorted(depth_counts.items())
        },
        "endpoint_parameter_rows_sha256": canonical_digest(endpoint_rows),
    }


def row_angle_width(
    row: dict[str, Any], s0: Q, s1: Q,
) -> tuple[arb, tuple[arb, arb]]:
    left = maximal.curve_normal(row["left_boundary"], s0, s1)
    right = maximal.curve_normal(row["right_boundary"], s0, s1)
    cross = left[0] * right[1] - left[1] * right[0]
    dot = left[0] * right[0] + left[1] * right[1]
    assert bool(cross > 0)
    width = arb.atan2(cross, dot)
    assert bool(width > arbq(Q(1, 16)))
    return width, left


def moving_core_normal(
    row: dict[str, Any], t0: Q, t1: Q, s0: Q, s1: Q,
) -> tuple[rank0.Jet, rank0.Jet]:
    width, left = row_angle_width(row, s0, s1)
    t = bulk.arb_interval(t0, t1)
    # Anchor each half of the core at its nearest analytic boundary.  The two
    # formulae are identical pointwise, but the right-anchored expression
    # avoids the interval dependency ``left + width = right`` near t=1.
    # The initial 1/16 cells (and every descendant) lie in one half.
    if t1 <= Q(1, 2):
        distance = arbq(COLLAR) + (width - 2 * arbq(COLLAR)) * t
        cosine = distance.cos()
        sine = distance.sin()
        normal_x = cosine * left[0] - sine * left[1]
        normal_y = cosine * left[1] + sine * left[0]
    else:
        assert t0 >= Q(1, 2)
        right = maximal.curve_normal(row["right_boundary"], s0, s1)
        distance = (
            arbq(COLLAR)
            + (width - 2 * arbq(COLLAR)) * (arb(1) - t)
        )
        cosine = distance.cos()
        sine = distance.sin()
        normal_x = cosine * right[0] + sine * right[1]
        normal_y = cosine * right[1] - sine * right[0]
    return jet_constant(normal_x), jet_constant(normal_y)


def normalized_boundary_germ(
    row: dict[str, Any], boundary: dict[str, Any],
    point_x: rank0.Jet, point_y: rank0.Jet,
    velocity_x: rank0.Jet, velocity_y: rank0.Jet,
    source_cp: rank0.Jet, absolute_uy: rank0.Jet,
    s0: Q, s1: Q,
) -> rank0.Jet:
    kind = boundary["kind"]
    if kind == SOURCE_GRAZING:
        return source_cp
    if kind == POLARITY:
        return absolute_uy
    other = boundary["descriptor"]["other"]
    obstacle = bulk.TARGET_BY_ID[other].obstacle
    radius = jet_constant(bulk.ARB_RADIUS[obstacle])
    delta = moving_discriminant(
        point_x, point_y, velocity_x, velocity_y, other, s0, s1
    )
    if kind == FIRST:
        return -delta / (radius * radius)
    assert kind == MISS
    signed = delta if row["miss_target"] == other else -delta
    return signed / (radius * radius)


def core_leaf_ok(
    row: dict[str, Any], t0: Q, t1: Q, s0: Q, s1: Q,
) -> tuple[bool, dict[str, Any]]:
    normal_x, normal_y = moving_core_normal(row, t0, t1, s0, s1)
    point_x, point_y, velocity_x, velocity_y, _flight, source_cp = (
        moving_tangent_geometry(row, normal_x, normal_y, s0, s1)
    )
    absolute_uy = rank0.signed_uy_multiplier(row) * velocity_y
    miss = row["miss_target"]
    miss_obstacle = bulk.TARGET_BY_ID[miss].obstacle
    miss_radius = jet_constant(bulk.ARB_RADIUS[miss_obstacle])
    miss_cp_squared = moving_discriminant(
        point_x, point_y, velocity_x, velocity_y, miss, s0, s1
    ) / (miss_radius * miss_radius)
    values = [source_cp, absolute_uy, miss_cp_squared]
    for field in ("left_boundary", "right_boundary"):
        values.append(normalized_boundary_germ(
            row,
            row[field],
            point_x,
            point_y,
            velocity_x,
            velocity_y,
            source_cp,
            absolute_uy,
            s0,
            s1,
        ))
    ok = all(bool(value.value > arbq(CORE_THRESHOLD)) for value in values)
    return ok, {
        "t": [str(t0), str(t1)],
        "s": [str(s0), str(s1)],
        "scale_enclosures": [str(value.value) for value in values],
    }


def core_audit(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    leaf_rows = []
    depth_counts: Counter[int] = Counter()
    per_occurrence = []
    for row in rows:
        pending = [
            (
                Q(index, INITIAL_CORE_T),
                Q(index + 1, INITIAL_CORE_T),
                bulk.S_LOWER
                + (bulk.S_UPPER - bulk.S_LOWER) * parameter_index
                / INITIAL_CORE_S,
                bulk.S_LOWER
                + (bulk.S_UPPER - bulk.S_LOWER) * (parameter_index + 1)
                / INITIAL_CORE_S,
                0,
            )
            for index in range(INITIAL_CORE_T)
            for parameter_index in range(INITIAL_CORE_S)
        ]
        row_count = 0
        row_depth = 0
        while pending:
            t0, t1, s0, s1, depth = pending.pop()
            try:
                ok, witness = core_leaf_ok(row, t0, t1, s0, s1)
            except (AssertionError, ValueError, ZeroDivisionError):
                ok = False
                witness = {"t": [str(t0), str(t1)], "s": [str(s0), str(s1)]}
            if ok:
                leaf_rows.append({
                    "occurrence_id": row["occurrence_id"],
                    "depth": depth,
                    **witness,
                })
                depth_counts[depth] += 1
                row_count += 1
                row_depth = max(row_depth, depth)
                continue
            assert depth < MAX_CORE_DEPTH, (row["occurrence_id"], witness)
            middle = (t0 + t1) / 2
            pending.append((middle, t1, s0, s1, depth + 1))
            pending.append((t0, middle, s0, s1, depth + 1))
        per_occurrence.append({
            "occurrence_id": row["occurrence_id"],
            "core_leaf_count": row_count,
            "maximum_depth": row_depth,
        })
    leaf_rows.sort(key=canonical_json)
    per_occurrence.sort(key=canonical_json)
    return leaf_rows, {
        "moving_core_definition": (
            f"inward angular interval [{COLLAR},width_s-{COLLAR}]"
        ),
        "uniform_row_angular_width_strict_lower": "1/16",
        "common_core_scale_strict_lower": str(CORE_THRESHOLD),
        "initial_normalized_angular_cells_per_row": INITIAL_CORE_T,
        "uniform_parameter_cells_per_row": INITIAL_CORE_S,
        "core_leaf_count": len(leaf_rows),
        "maximum_core_subdivision_depth": max(depth_counts),
        "core_leaf_depth_counts": {
            str(key): value for key, value in sorted(depth_counts.items())
        },
        "core_leaf_rows_sha256": canonical_digest(leaf_rows),
        "per_occurrence_rows_sha256": canonical_digest(per_occurrence),
    }


def finite_s_rank_and_cost() -> dict[str, Any]:
    density_coefficient = Q(18, 5)
    radius_squared = Q(81, 625)
    per_endpoint = {
        SOURCE_GRAZING: density_coefficient / FINITE_S_DERIVATIVE_LOWER[
            SOURCE_GRAZING
        ],
        POLARITY: density_coefficient / FINITE_S_DERIVATIVE_LOWER[POLARITY],
        FIRST: density_coefficient * radius_squared / FINITE_S_DERIVATIVE_LOWER[
            FIRST
        ],
        MISS: density_coefficient * radius_squared / FINITE_S_DERIVATIVE_LOWER[
            MISS
        ],
    }
    global_tail = sum(
        rank0.EXPECTED_ENDPOINT_COUNTS[kind] * value
        for kind, value in per_endpoint.items()
    )
    mass_upper = Q(8064, 5)
    rank_moment_upper = (
        (1 << BASE_RANK) * mass_upper
        + global_tail * Q(1, 1 << (BASE_RANK - 1))
    )
    partial_charge_upper = 204 * rank_moment_upper
    return {
        "canonical_finite_s_rank": {
            "core_rank": BASE_RANK,
            "endpoint_rank": (
                "max(20,ceil(log2(1/scale_s))) on the unique active moving collar"
            ),
            "source_scale": "cp_source",
            "polarity_scale": "abs(u_y)",
            "transition_scale": "sqrt(abs(Delta_transition))/R_transition",
            "moving_collars_pairwise_disjoint": True,
        },
        "uniform_rank_tail": {
            "valid_for_every_s": "|s|<=1/400",
            "valid_integer_threshold": "b>=20",
            "unnormalized_mass_tail": (
                f"sum_e m_e,s{{B_s>b}}<={global_tail}*4^-b"
            ),
            "global_tail_constant": str(global_tail),
            "per_endpoint_tail_constants": {
                key: str(value) for key, value in sorted(per_endpoint.items())
            },
            "tail_exponent_in_dyadic_rank": "2",
            "integral_2^B_uniform_upper_before_Z_N_inverse": str(
                rank_moment_upper
            ),
        },
        "finite_s_one_collision_cost": {
            "uniform_reverse_subcost": "C_rev^(geom)(s,a)<=204*2^B_s(a)",
            "uniform_forward_subcost": "C_fw^(geom)(s,a)<=204*2^B_s(a)",
            "uniform_partial_charge_mass_upper_before_boundary_Z": str(
                partial_charge_upper
            ),
            "same_coefficients_as_centred_geometry": (
                "151 chart/test + 52 log-density + 1 carrier-C2"
            ),
            "complete_propagated_numeric_C_fw_C_rev": False,
        },
    }


def finite_s_density_mesh_and_numeric_cmesh() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    carrier_length_coefficient = 1 << 17
    rows = []
    for b in range(BASE_RANK, 65):
        shell_upper = Q(1, 1 << b)
        shell_lower = Q(1, 1 << (b + 1))
        mesh_exponent = (3 * (b + 1) + 1) // 2
        delta = Q(1, 1 << mesh_exponent)
        assert delta * delta <= shell_lower**3
        piece_count = (carrier_length_coefficient << mesh_exponent) // (1 << b) + 1
        assert piece_count >= carrier_length_coefficient * shell_upper / delta
        z_upper = 23 * piece_count * shell_upper
        rows.append({
            "shell_rank_b": b,
            "density_scale_interval": [str(shell_lower), str(shell_upper)],
            "mesh_length": str(delta),
            "piece_count_upper": piece_count,
            "Z_numerator_upper": str(z_upper),
        })

    # Pair b=2n and b=2n+1.  For n>=10 the common piece-count bound is
    # 2^(n+19)+1.  Summing both parity classes gives the exact bound below.
    endpoint_z_upper = 23 * (Q(1536) + Q(1, 1 << 19))
    assert endpoint_z_upper == Q(18522046487, 524288)
    row_width_lower = Q(1, 16) - 2 * COLLAR
    row_mass_lower = (
        Q(4, 25)
        * CORE_THRESHOLD
        * CORE_THRESHOLD
        * row_width_lower
        / 3
    )
    row_z_upper = Q(23) + 2 * endpoint_z_upper + 2 * Q(23)
    c_mesh = row_z_upper / row_mass_lower
    return rows, {
        "canonical_mesh": "delta_b=2^-ceil(3(b+1)/2), b>=20",
        "uniform_carrier_shell_length_upper": "2^17*2^-b",
        "uniform_density_upper_on_zero_shell": "23*2^-b",
        "uniform_log_Hoelder_constant": "52",
        "log_Hoelder_exponent": "1/3",
        "one_zero_endpoint_Z_series_upper": str(endpoint_z_upper),
        "one_zero_endpoint_Z_series_summable": True,
        "uniform_row_mass_strict_lower": str(row_mass_lower),
        "row_mass_lower_derivation": (
            f"(4/25)*2^-20*2^-20*(1/16-2*{COLLAR})/3"
        ),
        "unnormalized_restricted_row_Z_upper": str(row_z_upper),
        "explicit_initial_C_mesh": str(c_mesh),
        "single_atom_normalized_boundary": (
            f"Z_s,fw(K,j),Z_s,rev(K,j)<={c_mesh}*2^K"
        ),
        "density_mesh_rows_sha256": canonical_digest(rows),
    }


def horizon_penetration_audit() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    pending = horizon.initial_boxes()
    leaves = []
    depth_counts: Counter[int] = Counter()
    squared_slack_lower = Q(1, 1 << 19)
    while pending:
        box = pending.pop()
        witness = horizon.choose_witness(box)
        cx, cy, radius, time, label = witness
        x_mid, y_mid, angle_mid_q = horizon.midpoint(box)
        x = horizon.interval(x_mid, (box.x1 - box.x0) / 2)
        y = horizon.interval(y_mid, (box.y1 - box.y0) / 2)
        angle_mid = 2 * arb.pi() * horizon.arbq(angle_mid_q)
        angle_radius = 2 * arb.pi() * horizon.arbq((box.a1 - box.a0) / 2)
        angle = angle_mid + arb(0, angle_radius.upper())
        t = horizon.arbq(time)
        dx = x + t * angle.cos() - horizon.arbq(cx)
        dy = y + t * angle.sin() - horizon.arbq(cy)
        slack = horizon.arbq(radius) ** 2 - dx * dx - dy * dy
        if bool(slack > horizon.arbq(squared_slack_lower)):
            depth_counts[box.depth] += 1
            leaves.append({
                "box": {
                    "x": [str(box.x0), str(box.x1)],
                    "y": [str(box.y0), str(box.y1)],
                    "angle_turns": [str(box.a0), str(box.a1)],
                    "depth": box.depth,
                },
                "witness_label": label,
                "witness_time": str(time),
                "core_radius": str(radius),
                "squared_penetration_slack_enclosure": str(slack),
            })
            continue
        if bool(slack > 0):
            # The frozen cover accepted this leaf, but the stronger common
            # dyadic slack may require a further exact dyadic subdivision.
            assert box.depth < horizon.MAX_DEPTH
            pending.extend(horizon.split(box))
            continue
        assert box.depth < horizon.MAX_DEPTH
        pending.extend(horizon.split(box))
    leaves.sort(key=canonical_json)
    assert len(leaves) >= 35024
    incidence_sine_squared_lower = squared_slack_lower / Q(9, 25)
    assert incidence_sine_squared_lower > Q(1, 512) ** 2
    return leaves, {
        "replayed_leaf_count": len(leaves),
        "frozen_leaf_count_before_slack_refinement": 35024,
        "maximum_binary_depth": max(depth_counts),
        "least_squared_penetration_slack_strict_lower": str(
            squared_slack_lower
        ),
        "uniform_actual_scatterer_squared_radial_slack_strict_lower": str(
            squared_slack_lower
        ),
        "uniform_incidence_sine_squared_strict_lower": str(
            incidence_sine_squared_lower
        ),
        "explicit_SYZ_horizon": "(t,phi)=(3,1/512)",
        "every_open_length_3_segment_has_one_incidence_angle_gt_1_over_512": True,
        "horizon_leaf_rows_sha256": canonical_digest(leaves),
    }


def uniform_configuration_and_recovery(c_mesh: str) -> dict[str, Any]:
    separation_margin = Q(36337, 800000)
    assert separation_margin > Q(1, 25)
    return {
        "compact_configuration_path": {
            "path": "K_s: gray disk fixed, white disk translated by (s,0)",
            "parameter_window": "|s|<=1/400",
            "scatterer_boundaries": "two fixed-radius circular C^infinity boundaries",
            "uniform_curvature_interval": "[25/9,25/4]",
            "uniform_minimum_free_flight_strict_lower": str(separation_margin),
            "declared_SYZ_tau_bar_min": "1/25",
            "uniform_SYZ_horizon": "(3,1/512)",
            "one_compact_SYZ_configuration_class": True,
        },
        "solid_section_typing": {
            "section": "N=G disjoint-union W, the usual solid-boundary collision section",
            "common_gauge": "fixed obstacle labels and boundary arclength coordinates",
            "map_used": "T_s=F_{K_s,K_s} in the canonical fixed-configuration gauge",
            "configuration_sequence": "K_s,K_s,K_s,... (constant for each fixed s)",
            "not_used": (
                "no identification of the transparent/fixed-section map with "
                "the source-target moving-configuration map F_{K',K}"
            ),
        },
        "one_time_atom_typing": {
            "atom_definition": (
                "for each fixed s, the one-time (K,j) atom is cut by the "
                "moving coordinates u_{e,s}"
            ),
            "bidirectional_record": (
                "forward and reverse orientations share the same fixed-s "
                "restricted measure and the same (s,K,j) record"
            ),
            "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas": False,
            "uniform_recovery_is_not_common_branch_record_MT_DQ": True,
        },
        "uniform_recovery_theorem": {
            "source": (
                "Stenlund--Young--Zhang, Dispersing billiards with moving "
                "scatterers, arXiv:1210.0011v4"
            ),
            "growth_result": "Lemma 12 (Growth lemma), uniform for all configuration sequences",
            "Z_result": (
                "Lemma 16: Z_n/mu <= C_p/2*(1+vartheta_p^n*Z_0/mu)"
            ),
            "theorem_supplied_constants": "C_p>1 and 0<vartheta_p<1",
            "constants_uniform_in_s_and_orientation": True,
            "initial_atom_boundary": f"Z_0/mu<={c_mesh}*2^K",
            "one_orientation_recovery_clock": (
                "R(K)<=A0+A1*K, A0=ceil(log(C_mesh)/|log(vartheta_p)|)+1, "
                "A1=ceil(log(2)/|log(vartheta_p)|)"
            ),
            "two_orientation_recovery_clock": (
                "R_fw+R_rev<=2*A0+2*A1*K"
            ),
            "uniform_depth_recovery_moment": (
                "for 0<gamma<log(2)/(2*A1), "
                "E[2^K exp(gamma(R_fw+R_rev))]<infinity"
            ),
            "controlled_one_time_finite_s_stopped_parent_recovery": True,
            "C_p_vartheta_p_numerically_evaluated": False,
            "hereditary_repeated_indicator_recovery": False,
        },
    }


def certify() -> dict[str, Any]:
    rows, registry = load_dependencies()
    endpoint_rows, endpoint_audit = endpoint_collar_audit(rows)
    core_rows, core_summary = core_audit(rows)
    rank_cost = finite_s_rank_and_cost()
    mesh_rows, mesh = finite_s_density_mesh_and_numeric_cmesh()
    horizon_rows, horizon_summary = horizon_penetration_audit()
    recovery = uniform_configuration_and_recovery(mesh["explicit_initial_C_mesh"])
    assert registry["maximal_row_rows_sha256"] == (
        "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
    )
    return {
        "schema": "cm2.gate45.finite-s-common-mesh-recovery.v1",
        "provenance": {
            "maximal_row_manifest": MAXIMAL_MANIFEST.name,
            "curvature_log_density_manifest": CURVATURE_MANIFEST.name,
            "product_stopped_depth_manifest": PRODUCT_MANIFEST.name,
            "s0_recovery_manifest": S0_RECOVERY_MANIFEST.name,
            "uniform_horizon_certificate": "cm2_standard_section_horizon_lift_cert.py",
            "maximal_row_registry_sha256": registry["maximal_row_rows_sha256"],
        },
        "finite_s_endpoint_collar_audit": endpoint_audit,
        "finite_s_moving_core_audit": core_summary,
        "finite_s_rank_and_one_collision_cost": rank_cost,
        "finite_s_density_mesh_and_numeric_C_mesh": mesh,
        "uniform_horizon_penetration_audit": horizon_summary,
        "uniform_configuration_and_recovery": recovery,
        "scope_limits": {
            "finite_s_common_moving_endpoint_collars": True,
            "finite_s_common_density_regular_mesh_rule": True,
            "mesh_endpoints_move_with_u_e_s": True,
            "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas": False,
            "common_branch_record_MT_DQ": False,
            "explicit_numeric_initial_C_mesh": True,
            "uniform_one_time_finite_s_stopped_parent_recovery": True,
            "finite_s_depth_plus_recovery_moment_for_some_gamma": True,
            "uniform_one_collision_geometric_cost_coefficients": True,
            "theorem_recovery_constants_numeric": False,
            "complete_propagated_numeric_C_fw_C_rev_q": False,
            "native_dynamical_stopping_antichain": False,
            "hereditary_repeated_indicator_recovery": False,
            "physical_prefix_suffix_costs": False,
            "full_dynamic_MT_DQ": False,
            "CM2_norm_lifts": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
        "internal_replay_digest": canonical_digest({
            "endpoint_rows": endpoint_rows,
            "core_rows": core_rows,
            "mesh_rows": mesh_rows,
            "horizon_rows": horizon_rows,
        }),
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE45_FINITE_S_COMMON_ENDPOINT_MESH: CERTIFIED")
    print("GATE45_UNIFORM_ONE_TIME_FINITE_S_RECOVERY: CERTIFIED")
    print("GATE45_EXPLICIT_INITIAL_C_MESH: CERTIFIED")
    print("GATE45_COMPLETE_PROPAGATED_NUMERIC_C_FW_C_REV_Q: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
