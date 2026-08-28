#!/usr/bin/env python3
"""Physical two-generator centered-jet engine for Round146.

The two affine generators are genuine source coordinates

    delta_x = x - x_star,       x = sqrt(17) r,
    delta_beta = (asin(p) - 4 r) - b_star.

The certified numerical enclosure of ``t_star`` is *not* a parameter
generator.  It is evaluated as an interval constant and charged to the
initial componentwise remainder.

This module is an append-only computational engine.  The Round146 producer
pins it and turns selected runs into a closed certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable, Sequence

from flint import arb, ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
import cm2_round141_centered_affine_d0_collar_spike as base


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
R139_CERTIFICATE = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
RETURN_DEPTH = 1648
DEFAULT_X_POWER = 4296
DEFAULT_X_CELL_INDEX = 1
DEFAULT_BETA_POWER = 5888


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def point(value: arb) -> arb:
    return arb(value.mid())


def symmetric(radius: arb) -> arb:
    return arb(0, radius.upper())


def dual_asin(value: base.Dual) -> base.Dual:
    denominator = (1 - value.value * value.value).sqrt()
    return base.Dual(
        value.value.asin(),
        [entry / denominator for entry in value.derivative],
    )


def physical_initial(
    delta_x: base.Dual,
    delta_beta: base.Dual,
    t_star: arb,
) -> list[base.Dual]:
    """Map physical centered coordinates to the source contact state."""

    require(delta_x.dimension == 2, "two physical generators")
    require(delta_beta.dimension == 2, "two physical generators")
    sqrt17 = arb(17).sqrt()
    t_star_dual = base.Dual(t_star, dimension=2)
    contact_angle = (
        dual_asin(t_star_dual)
        + delta_x / (r139.lower.aq(r139.lower.R_W) * sqrt17)
    )
    t = base.dsin(contact_angle)
    p_phase = (
        base.Dual(
            r139.lower.aq(r139.lower.SOURCE_P_STAR).asin(),
            dimension=2,
        )
        + 4 * delta_x / sqrt17
        + delta_beta
    )
    p = base.dsin(p_phase)
    normal_x, normal_y = base.dcos(contact_angle), t
    radial = base.dsqrt(base.Dual(1, dimension=2) - p * p)
    velocity = (
        radial * normal_x - p * normal_y,
        radial * normal_y + p * normal_x,
    )
    center, radius = base.target_geometry(
        r139.lower.SOURCE_ABSOLUTE_OWNER
    )
    position = (
        base.Dual(center[0], dimension=2) + radius * normal_x,
        base.Dual(center[1], dimension=2) + radius * normal_y,
    )
    return list(position + velocity)


def parameter_cell(
    x_power: int,
    x_cell_index: int,
    beta_power: int,
    beta_cell_index: int,
) -> tuple[arb, arb, arb, arb]:
    """Return centers and radii for translated x and beta cells.

    The x cells are the Round141 left-translated cells
    ``[-(i+1)2^-k, -i 2^-k]``.  The beta cells have halfwidth
    ``2^-m`` and center ``2 j 2^-m``.
    """

    require(
        type(x_power) is int
        and type(beta_power) is int
        and x_power > 0
        and beta_power > 0,
        "positive cell powers",
    )
    require(
        type(x_cell_index) is int and x_cell_index >= 1,
        "interior x cell index",
    )
    require(type(beta_cell_index) is int, "integer beta cell index")
    x_width = r139.lower.aq(Q(1, 2**x_power))
    x_center = -(2 * x_cell_index + 1) * x_width / 2
    x_radius = x_width / 2
    beta_radius = r139.lower.aq(Q(1, 2**beta_power))
    beta_center = 2 * beta_cell_index * beta_radius
    return x_center, x_radius, beta_center, beta_radius


def initial_model(
    root: tuple[Q, Q],
    x_power: int,
    x_cell_index: int,
    beta_power: int,
    beta_cell_index: int,
) -> base.Model:
    """Build a rigorous two-physical-generator affine initial state."""

    x_center, x_radius, beta_center, beta_radius = parameter_cell(
        x_power,
        x_cell_index,
        beta_power,
        beta_cell_index,
    )
    root_lower, root_upper = map(r139.lower.aq, root)
    root_center = point((root_lower + root_upper) / 2)
    root_ball = root_center + symmetric((root_upper - root_lower) / 2)
    center_values = physical_initial(
        base.Dual(x_center, [arb(1), arb(0)]),
        base.Dual(beta_center, [arb(0), arb(1)]),
        root_center,
    )
    interval_values = physical_initial(
        base.Dual(
            x_center + symmetric(x_radius),
            [arb(1), arb(0)],
        ),
        base.Dual(
            beta_center + symmetric(beta_radius),
            [arb(0), arb(1)],
        ),
        root_ball,
    )
    root_only_values = physical_initial(
        base.Dual(x_center, [arb(1), arb(0)]),
        base.Dual(beta_center, [arb(0), arb(1)]),
        root_ball,
    )
    raw_affine = base.rows(center_values)
    affine = [[point(entry) for entry in row] for row in raw_affine]
    interval_derivatives = base.rows(interval_values)
    domain_radii = (x_radius, beta_radius)
    centers = [point(value.value) for value in center_values]
    remainders = [
        (center_values[row].value - centers[row]).abs_upper()
        + (root_only_values[row].value - center_values[row].value).abs_upper()
        + sum(
            (
                raw_affine[row][column] - affine[row][column]
            ).abs_upper()
            * domain_radii[column]
            for column in range(2)
        )
        + sum(
            (
                interval_derivatives[row][column]
                - raw_affine[row][column]
            ).abs_upper()
            * domain_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]
    return base.Model(centers, affine, remainders, domain_radii)


def anchor_discriminant(
    delta_x: arb,
    delta_beta: arb,
    t_star: arb,
) -> base.Dual:
    """Collision-three W[0,0] discriminant with physical derivatives."""

    state = physical_initial(
        base.Dual(delta_x, [arb(1), arb(0)]),
        base.Dual(delta_beta, [arb(0), arb(1)]),
        t_star,
    )
    document = json.loads(R139_CERTIFICATE.read_text(encoding="utf-8"))
    owners = [
        row["selected_absolute_owner_id"]
        for row in document["result"]["collision_rows"]
    ]
    for owner in owners[:2]:
        center, radius = base.target_geometry(owner)
        state, _metrics = base.collision(state, center, radius)
    center, radius = base.target_geometry(r139.ANCHOR)
    position, velocity = state[:2], state[2:]
    displacement = (
        position[0] - center[0],
        position[1] - center[1],
    )
    linear = base.dot(displacement, velocity)
    offset = base.dot(displacement, displacement) - radius * radius
    return linear * linear - offset


def fixed_outer(value: arb, bits: int) -> list[str]:
    return [
        r139.qstr(entry)
        for entry in base.fixed_padded_outer(value, bits)
    ]


def physical_anchor_exclusion(
    root: tuple[Q, Q],
    x_power: int,
    x_cell_index: int,
    beta_power: int,
    beta_cell_index: int,
) -> dict[str, Any]:
    """Prove D3<0 on one physical cell by monotonic corner evaluation."""

    x_center, x_radius, beta_center, beta_radius = parameter_cell(
        x_power,
        x_cell_index,
        beta_power,
        beta_cell_index,
    )
    root_lower, root_upper = map(r139.lower.aq, root)
    t_star = (
        (root_lower + root_upper) / 2
        + symmetric((root_upper - root_lower) / 2)
    )
    whole = anchor_discriminant(
        x_center + symmetric(x_radius),
        beta_center + symmetric(beta_radius),
        t_star,
    )
    require(
        bool(whole.derivative[0] > 0)
        and bool(whole.derivative[1] > 0),
        "D3 physical coordinate monotonicity",
    )
    right_upper = anchor_discriminant(
        x_center + x_radius,
        beta_center + beta_radius,
        t_star,
    )
    require(
        bool(right_upper.value < 0),
        "D3 negative at monotone maximum corner",
    )
    return {
        "method":
            "full-cell derivative signs plus exact upper-right corner",
        "anchor_candidate": r139.ANCHOR,
        "collision_index": r139.ANCHOR_COLLISION_INDEX,
        "D3_strictly_increasing_in_delta_x": True,
        "D3_strictly_increasing_in_delta_beta": True,
        "D3_maximum_corner": [
            "delta_x upper",
            "delta_beta upper",
        ],
        "D3_maximum_strict_negative": True,
        "D3_miss_margin_dyadic_depth":
            r139.lower.round136.strict_dyadic_depth(-right_upper.value),
        "D3_delta_x_derivative_outer": fixed_outer(
            whole.derivative[0],
            128,
        ),
        "D3_delta_beta_derivative_outer": fixed_outer(
            whole.derivative[1],
            128,
        ),
        "t_star_numerical_enclosure_charged_not_parameterized": True,
    }


def transverse_D3_event_frontier(
    root: tuple[Q, Q],
    x_power: int = DEFAULT_X_POWER,
    x_cell_index: int = DEFAULT_X_CELL_INDEX,
) -> dict[str, Any]:
    """Certify a local parametric interval-Newton D3 event graph."""

    require(
        x_power == DEFAULT_X_POWER
        and x_cell_index == DEFAULT_X_CELL_INDEX,
        "frozen Round146 event x cell",
    )
    h_q = Q(1, 2**x_power)
    h = r139.lower.aq(h_q)
    x_center = -r139.lower.aq(Q(3, 2)) * h
    x_radius = h / 2
    beta_lower = 2 * h
    beta_upper = 6 * h
    beta_center = 4 * h
    beta_radius = 2 * h
    root_lower, root_upper = map(r139.lower.aq, root)
    t_star = (
        (root_lower + root_upper) / 2
        + symmetric((root_upper - root_lower) / 2)
    )
    whole = anchor_discriminant(
        x_center + symmetric(x_radius),
        beta_center + symmetric(beta_radius),
        t_star,
    )
    require(
        bool(whole.derivative[0] > 0)
        and bool(whole.derivative[1] > 0),
        "event Jacobian transverse signs",
    )
    bottom_maximum = anchor_discriminant(
        -h,
        beta_lower,
        t_star,
    )
    top_minimum = anchor_discriminant(
        -2 * h,
        beta_upper,
        t_star,
    )
    shared_face_maximum = anchor_discriminant(
        -h,
        h,
        t_star,
    )
    positive_neighbor_top_right = anchor_discriminant(
        -h,
        3 * h,
        t_star,
    )
    require(
        bool(bottom_maximum.value < 0)
        and bool(top_minimum.value > 0)
        and bool(shared_face_maximum.value < 0)
        and bool(positive_neighbor_top_right.value > 0),
        "event edge sign pattern",
    )
    center_value = anchor_discriminant(
        x_center,
        beta_center,
        t_star,
    )
    mean_value_at_beta_center = (
        center_value.value
        + whole.derivative[0] * symmetric(x_radius)
    )
    interval_newton = (
        beta_center
        - mean_value_at_beta_center / whole.derivative[1]
    )
    require(
        bool(interval_newton > beta_lower)
        and bool(interval_newton < beta_upper),
        "parametric interval Newton strict inclusion",
    )
    slope = -whole.derivative[0] / whole.derivative[1]
    require(bool(slope < 0), "event graph negative slope")
    return {
        "event_kind": "COLLISION3_D0_TANGENCY_D3_ZERO",
        "anchor_candidate": r139.ANCHOR,
        "physical_parameter_box": {
            "delta_x": [
                r139.qstr(-2 * h_q),
                r139.qstr(-h_q),
            ],
            "delta_beta": [
                r139.qstr(2 * h_q),
                r139.qstr(6 * h_q),
            ],
        },
        "event_function": "D3(delta_x,delta_beta)",
        "D3_strictly_increasing_in_delta_x": True,
        "D3_strictly_increasing_in_delta_beta": True,
        "bottom_edge_D3_strict_negative": True,
        "top_edge_D3_strict_positive": True,
        "unique_beta_root_for_every_fixed_delta_x": True,
        "parametric_interval_Newton_center_beta":
            r139.qstr(4 * h_q),
        "parametric_interval_Newton_image_in_h_units":
            fixed_outer(interval_newton / h, 256),
        "parametric_interval_Newton_strictly_inside_event_beta_box":
            True,
        "Jacobian_outer": {
            "partial_D3_partial_delta_x":
                fixed_outer(whole.derivative[0], 128),
            "partial_D3_partial_delta_beta":
                fixed_outer(whole.derivative[1], 128),
        },
        "transverse_to_beta_fibres": True,
        "implicit_graph_slope_outer":
            fixed_outer(slope, 128),
        "implicit_graph_slope_strict_negative": True,
        "central_x_root_beta_in_h_units":
            fixed_outer(
                (
                    beta_center
                    - center_value.value / center_value.derivative[1]
                )
                / h,
                256,
            ),
        "certified_cell_upper_shared_face_beta":
            r139.qstr(h_q),
        "D3_negative_on_whole_shared_face": True,
        "positive_transverse_neighbor": {
            "delta_beta": [
                r139.qstr(h_q),
                r139.qstr(3 * h_q),
            ],
            "shares_exact_artificial_face": True,
            "D3_event_enters_neighbor": True,
            "whole_neighbor_has_frozen_owner_path": False,
        },
        "negative_transverse_neighbor": {
            "delta_beta": [
                r139.qstr(-3 * h_q),
                r139.qstr(-h_q),
            ],
            "shares_exact_artificial_face": True,
            "D3_event_enters_neighbor": False,
            "complete_path_audit_in_this_result": False,
        },
        "event_curve_is_local_not_exhaustive_global_frontier": True,
    }


def candidates_owner_excluding_physical_anchor(
    state: dict[str, Any],
    current_target: str,
    candidates: Iterable[str],
    ledger: Any,
    collision_index: int,
    full_radius4: bool,
    anchor_proof: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Audit candidates after an independent physical-cell D3<0 proof."""

    require(
        collision_index == r139.ANCHOR_COLLISION_INDEX,
        "physical anchor exclusion only at collision three",
    )
    require(
        anchor_proof["D3_maximum_strict_negative"] is True,
        "closed physical anchor exclusion proof",
    )
    candidate_ids = tuple(candidates)
    require(r139.ANCHOR in candidate_ids, "anchor in candidate universe")
    prefix = "full_radius4_" if full_radius4 else ""
    qx, qy, ux, uy, s = (
        state["contact_x"],
        state["contact_y"],
        state["outgoing_x"],
        state["outgoing_y"],
        state["s"],
    )
    future: list[tuple[str, dict[str, arb]]] = []
    histogram: Counter[str] = Counter()
    decision_depths: list[int] = []
    ambiguous_nonanchor: list[str] = []
    for candidate_id in candidate_ids:
        if candidate_id == r139.ANCHOR:
            continue
        center_x, center_y = (
            r139.lower.time3.time2_cert.target_center(candidate_id, s)
        )
        dx, dy = center_x - qx, center_y - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = r139.lower.aq(
            r139.lower.time3.time2_cert.first_hit.RADIUS[
                candidate_id[0]
            ]
        )
        discriminant = radius * radius - transverse * transverse
        witness = {
            "collision_index": collision_index,
            "candidate_id": candidate_id,
        }
        if bool(discriminant < 0):
            histogram["no_real_intersection"] += 1
            decision_depths.append(ledger.observe(
                prefix + "candidate_miss_discriminant",
                -discriminant,
                witness,
            ))
            continue
        if not bool(discriminant > 0):
            ambiguous_nonanchor.append(candidate_id)
            continue
        if not full_radius4:
            decision_depths.append(ledger.observe(
                "candidate_positive_discriminant",
                discriminant,
                witness,
            ))
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            histogram["intersection_strictly_behind"] += 1
            decision_depths.append(ledger.observe(
                prefix + "candidate_behind_far_root",
                -far,
                witness,
            ))
            continue
        require(bool(near > 0), "nonanchor future root strict")
        histogram["strict_future_near_root"] += 1
        decision_depths.append(ledger.observe(
            prefix + "candidate_future_root_positive",
            near,
            witness,
        ))
        future.append((
            candidate_id,
            {
                "near": near,
                "radical": radical,
                "transverse": transverse,
                "radius": radius,
                "discriminant": discriminant,
            },
        ))
    require(
        not ambiguous_nonanchor,
        f"only physical anchor excluded:{ambiguous_nonanchor}",
    )
    winners = [
        (candidate_id, row)
        for candidate_id, row in future
        if all(
            candidate_id == other_id or bool(row["near"] < other["near"])
            for other_id, other in future
        )
    ]
    require(
        len(winners) == 1
        and winners[0][0] == r139.EXPECTED_MINUS_OWNER,
        "unique collision-three physical-cell winner",
    )
    selected_id, selected = winners[0]
    gap_depths = [
        ledger.observe(
            prefix + "winner_pairwise_root_gap",
            row["near"] - selected["near"],
            {
                "collision_index": collision_index,
                "winner_id": selected_id,
                "competitor_id": candidate_id,
            },
        )
        for candidate_id, row in future
        if candidate_id != selected_id
    ]
    root = selected["near"]
    if not full_radius4:
        tau_margin = (
            r139.lower.aq(
                r139.lower.time3.time2_cert.first_hit.TAU_MAX
            )
            - root
        )
        require(bool(tau_margin > 0), "collision-three winner cap")
        ledger.observe(
            "selected_root_positive",
            root,
            {"collision_index": collision_index},
        )
        ledger.observe(
            "selected_discriminant_positive",
            selected["discriminant"],
            {
                "collision_index": collision_index,
                "candidate_id": selected_id,
            },
        )
        ledger.observe(
            "selected_root_below_tau_max",
            tau_margin,
            {"collision_index": collision_index},
        )
    radical = selected["radical"]
    transverse = selected["transverse"]
    radius = selected["radius"]
    owner = {
        "selected_target_id": selected_id,
        "selected_root": root,
        "normal_x": (-radical * ux + transverse * uy) / radius,
        "normal_y": (-radical * uy - transverse * ux) / radius,
        "p": transverse / radius,
        "cosine": radical / radius,
    }
    require(
        sum(histogram.values()) == len(candidate_ids) - 1,
        "physical nonanchor candidate census",
    )
    return owner, {
        "candidate_universe":
            "full-radius-four" if full_radius4 else "retained-chart",
        "candidate_count": len(candidate_ids),
        "nonanchor_candidate_count": len(candidate_ids) - 1,
        "anchor_candidate_count": 1,
        "ambiguous_nonanchor_candidate_count": 0,
        "candidate_classification_histogram":
            dict(sorted(histogram.items())),
        "minimum_candidate_decision_margin_dyadic_depth":
            max(decision_depths),
        "minimum_winner_gap_dyadic_depth":
            max(gap_depths) if gap_depths else None,
        "selected_target_id": selected_id,
        "selected_target_matches_minus_branch": True,
        "anchor": anchor_proof,
    }


def phase_at_contact(
    model: base.Model,
    current_target: str,
) -> tuple[str, dict[str, arb]]:
    return base.chart_and_owner_state(model, current_target)


def probe_owner_cell(
    x_power: int,
    x_cell_index: int,
    beta_power: int,
    beta_cell_index: int,
    precision: int,
) -> dict[str, Any]:
    """Fast retained-owner probe; this is never a complete-audit claim."""

    ctx.prec = precision
    document = json.loads(R139_CERTIFICATE.read_text(encoding="utf-8"))
    result = document["result"]
    owners = [
        row["selected_absolute_owner_id"]
        for row in result["collision_rows"]
    ]
    root = tuple(
        Q(value)
        for value in result["deep_same_D0_root_and_b_star"][
            "deep_D0_root_bracket"
        ]
    )
    model = initial_model(
        root,
        x_power,
        x_cell_index,
        beta_power,
        beta_cell_index,
    )
    anchor_proof = physical_anchor_exclusion(
        root,
        x_power,
        x_cell_index,
        beta_power,
        beta_cell_index,
    )
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    current_chart = "E"
    ledger = base.NoLedger()
    maximum_radius = arb(0)
    for collision_index, expected_owner in enumerate(owners, start=1):
        for radius in model.radii():
            if bool(radius > maximum_radius):
                maximum_radius = radius.abs_upper()
        boxes = model.boxes()
        state = {
            "contact_x": boxes[0],
            "contact_y": boxes[1],
            "outgoing_x": boxes[2],
            "outgoing_y": boxes[3],
            "s": arb(0),
            "chart": current_chart,
        }
        try:
            if collision_index == r139.ANCHOR_COLLISION_INDEX:
                candidates = tuple(
                    r139.lower.time3.time2_cert.translated_candidate_ids(
                        current_target,
                        current_chart,
                    )
                )
                owner, _audit = (
                    candidates_owner_excluding_physical_anchor(
                        state,
                        current_target,
                        candidates,
                        ledger,
                        collision_index,
                        False,
                        anchor_proof,
                    )
                )
            else:
                owner, _audit = r139.lower.round136.complete_owner(
                    state,
                    current_target,
                    ledger,
                    collision_index,
                )
            require(
                owner["selected_target_id"] == expected_owner,
                f"owner mismatch:{collision_index}:"
                f"{owner['selected_target_id']}:{expected_owner}",
            )
            model, _step = base.step_model_with_audit(
                model,
                expected_owner,
            )
            current_target = expected_owner
            current_chart, phase = phase_at_contact(
                model,
                current_target,
            )
            require(
                bool(phase["cosine"] > 0),
                f"positive contact cosine:{collision_index}",
            )
        except Exception as exc:
            return {
                "status": "BLOCKED",
                "complete_audit": False,
                "first_failure_collision": collision_index,
                "first_failure_expected_owner": expected_owner,
                "first_failure": str(exc),
            }
    return {
        "status": "FEASIBLE_RETAINED_OWNER_PROBE",
        "complete_audit": False,
        "collision_count": RETURN_DEPTH,
        "maximum_state_radius_strict_upper_power_of_two_exponent":
            base.strict_upper_power_of_two_exponent(maximum_radius),
    }


def run_cell(
    x_power: int,
    x_cell_index: int,
    beta_power: int,
    beta_cell_index: int,
    precision: int,
    audit_all: bool,
) -> dict[str, Any]:
    """Propagate and optionally fully audit one physical 2D cell."""

    require(precision >= 8192, "Round146 minimum cell precision")
    require(audit_all is True, "Round146 complete cell audit required")
    ctx.prec = precision
    document = json.loads(R139_CERTIFICATE.read_text(encoding="utf-8"))
    result = document["result"]
    owners = [
        row["selected_absolute_owner_id"]
        for row in result["collision_rows"]
    ]
    root = tuple(
        Q(value)
        for value in result["deep_same_D0_root_and_b_star"][
            "deep_D0_root_bracket"
        ]
    )
    model = initial_model(
        root,
        x_power,
        x_cell_index,
        beta_power,
        beta_cell_index,
    )
    anchor_proof = physical_anchor_exclusion(
        root,
        x_power,
        x_cell_index,
        beta_power,
        beta_cell_index,
    )
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    current_chart = "E"
    ledger: base.NoLedger = (
        base.AuditLedger() if audit_all else base.NoLedger()
    )
    maximum_radius = arb(0)
    maximum_radius_witness: list[Any] | None = None
    radius_rows: list[list[Any]] = []
    official_ids: list[str] = []
    compact_rows: list[list[Any]] = []
    homogeneity_labels: list[str] = []
    incidence_ranks: list[int] = []
    cores = tuple(r139.lower.core_cert.physical_cores())
    pair_index, pattern_index, registry_sha = (
        r139.lower.component_cert.key_index_tables()
    )
    require(
        registry_sha == r139.OFFICIAL_REGISTRY_SHA256,
        "official registry digest",
    )
    initial_boxes = model.boxes()
    source_center, source_radius = base.target_geometry(current_target)
    initial_nx = (initial_boxes[0] - source_center[0]) / source_radius
    initial_ny = (initial_boxes[1] - source_center[1]) / source_radius
    initial_p = -initial_boxes[2] * initial_ny + initial_boxes[3] * initial_nx
    previous_cosine = (1 - initial_p * initial_p).sqrt()
    for collision_index, expected_owner in enumerate(owners, start=1):
        incoming_target = current_target
        state_boxes = model.boxes()
        for component, radius in enumerate(model.radii()):
            if bool(radius > maximum_radius):
                maximum_radius = radius.abs_upper()
                maximum_radius_witness = [
                    collision_index - 1,
                    component,
                    base.strict_upper_power_of_two_exponent(radius),
                ]
        state = {
            "contact_x": state_boxes[0],
            "contact_y": state_boxes[1],
            "outgoing_x": state_boxes[2],
            "outgoing_y": state_boxes[3],
            "s": arb(0),
            "chart": current_chart,
        }
        owner, _audit = r139.lower.round136.complete_owner(
            state,
            current_target,
            ledger,
            collision_index,
        )
        r139.lower.full_radius4_candidate_audit(
            state,
            current_target,
            owner,
            ledger,
            collision_index,
        )
        require(
            owner["selected_target_id"] == expected_owner,
            f"owner mismatch:{collision_index}:"
            f"{owner['selected_target_id']}:{expected_owner}",
        )
        word, word_error = (
            r139.lower.round136.translation_normalized_official_word(
                state,
                current_target,
                owner,
                pair_index,
                pattern_index,
            )
        )
        require(
            word is not None and word_error is None,
            f"official word:{collision_index}:{word_error}",
        )
        r139.official_wall_margin_audit(
            state,
            current_target,
            owner,
            ledger,
            collision_index,
        )
        model, step_audit = base.step_model_with_audit(
            model,
            expected_owner,
        )
        for component, radius in enumerate(
            step_audit["output_state_radii"]
        ):
            if bool(radius > maximum_radius):
                maximum_radius = radius.abs_upper()
                maximum_radius_witness = [
                    collision_index,
                    component,
                    base.strict_upper_power_of_two_exponent(radius),
                ]
        radius_rows.append([
            collision_index,
            base.vector_upper_exponents(
                step_audit["input_affine_radii"]
            ),
            base.vector_upper_exponents(step_audit["input_remainders"]),
            base.vector_upper_exponents(step_audit["input_state_radii"]),
            base.vector_upper_exponents(
                step_audit["raw_propagated_remainders"]
            ),
            base.vector_upper_exponents(
                step_audit["center_recenter_losses"]
            ),
            base.vector_upper_exponents(
                step_audit["coefficient_recenter_losses"]
            ),
            base.vector_upper_exponents(
                step_audit["output_affine_radii"]
            ),
            base.vector_upper_exponents(step_audit["output_remainders"]),
            base.vector_upper_exponents(step_audit["output_state_radii"]),
        ])
        current_target = expected_owner
        current_chart, phase = phase_at_contact(model, current_target)
        require(
            bool(phase["cosine"] > 0),
            f"positive contact cosine:{collision_index}",
        )
        certified_owner = {
            **phase,
            "selected_target_id": expected_owner,
            "selected_root": owner["selected_root"],
        }
        classification, destination, _witnesses = (
            r139.lower.time3.core_classification(
                certified_owner,
                cores,
            )
        )
        if collision_index < RETURN_DEPTH:
            require(
                classification == "SURVIVE_THROUGH_3_INNER"
                and destination is None,
                f"preterminal C24:{collision_index}:"
                f"{classification}:{destination}",
            )
        else:
            require(
                classification == "RETURN_AT_3_INNER"
                and destination == r139.EXPECTED_DESTINATION_CORE_ID,
                f"terminal C24:{classification}:{destination}",
            )
        r139.lower.round136.core_margin(
            certified_owner,
            classification,
            destination,
            cores,
            ledger,
        )
        homogeneity, _homogeneity_audit = (
            r139.lower.generic_homogeneity_label(
                collision_index,
                phase["cosine"],
                ledger,
            )
        )
        source_rank = (
            r139.lower.round136.capped_reciprocal_cosine_rank(
                previous_cosine,
                ledger,
                collision_index,
                "source",
            )
        )
        target_rank = (
            r139.lower.round136.capped_reciprocal_cosine_rank(
                phase["cosine"],
                ledger,
                collision_index,
                "target",
            )
        )
        incidence = max(14, source_rank, target_rank)
        r139.lower.round136.chart_margin(
            {
                "chart": current_chart,
                "normal_x": phase["normal_x"],
                "normal_y": phase["normal_y"],
            },
            ledger,
        )
        compact_key = r139.lower.round136.compact_key(word["key"])
        official_id = compact_key["official_word_key_id"]
        official_ids.append(official_id)
        homogeneity_labels.append(homogeneity)
        incidence_ranks.append(incidence)
        compact_rows.append([
            collision_index,
            incoming_target,
            expected_owner,
            official_id,
            homogeneity,
            incidence,
            classification,
            destination,
        ])
        previous_cosine = phase["cosine"]
    x_width_q = Q(1, 2**x_power)
    x_center_q = -Q(2 * x_cell_index + 1, 2) * x_width_q
    x_radius_q = x_width_q / 2
    beta_radius_q = Q(1, 2**beta_power)
    beta_center_q = 2 * beta_cell_index * beta_radius_q
    assert isinstance(ledger, base.AuditLedger)
    return {
        "status": "PASS",
        "minimum_certified_precision_bits": 8192,
        "runtime_precision_not_serialized": True,
        "audit_all": audit_all,
        "physical_parameter_generator_count": 2,
        "parameter_generators": ["delta_x", "delta_beta"],
        "t_star_numerical_isolation_is_parameter": False,
        "collision3_physical_anchor_exclusion": anchor_proof,
        "x_power": x_power,
        "x_cell_index": x_cell_index,
        "beta_power": beta_power,
        "beta_cell_index": beta_cell_index,
        "x_center": r139.qstr(x_center_q),
        "x_radius": r139.qstr(x_radius_q),
        "beta_center": r139.qstr(beta_center_q),
        "beta_radius": r139.qstr(beta_radius_q),
        "collision_count": RETURN_DEPTH,
        "full_radius4_candidate_test_count": 161 * RETURN_DEPTH,
        "official_sequence_sha256": digest(official_ids),
        "compact_rows_sha256": digest(compact_rows),
        "homogeneity_histogram": dict(Counter(homogeneity_labels)),
        "incidence_histogram": dict(Counter(incidence_ranks)),
        "preterminal_strict_nonreturn_count": RETURN_DEPTH - 1,
        "terminal_strict_return_count": 1,
        "terminal_owner": r139.EXPECTED_TERMINAL_OWNER,
        "terminal_destination_core": r139.EXPECTED_DESTINATION_CORE_ID,
        "model_radius_ledger_row_count": len(radius_rows),
        "model_radius_ledger_sha256": digest(radius_rows),
        "maximum_state_radius_strict_upper_power_of_two_exponent":
            base.strict_upper_power_of_two_exponent(maximum_radius),
        "maximum_state_radius_witness": maximum_radius_witness,
        "terminal_state_radius_strict_upper_power_of_two_exponents":
            base.vector_upper_exponents(model.radii()),
        "strict_margin_ledger": {
            name: {
                "dyadic_depth": ledger.depths[name],
                "observation_count": ledger.counts[name],
                "one_worst_depth_witness": ledger.witnesses[name],
            }
            for name in sorted(ledger.depths)
        },
        "ledger_worst_depth": max(ledger.depths.values()),
        "ledger_worst_names": sorted(
            name
            for name, depth in ledger.depths.items()
            if depth == max(ledger.depths.values())
        ),
        "terminal_phase_fixed_dyadic_outer_bits": 128,
        "terminal_normal_x_fixed_dyadic_outer": [
            r139.qstr(value)
            for value in base.fixed_padded_outer(phase["normal_x"], 128)
        ],
        "terminal_normal_y_fixed_dyadic_outer": [
            r139.qstr(value)
            for value in base.fixed_padded_outer(phase["normal_y"], 128)
        ],
        "terminal_p_fixed_dyadic_outer": [
            r139.qstr(value)
            for value in base.fixed_padded_outer(phase["p"], 128)
        ],
        "terminal_cosine_fixed_dyadic_outer": [
            r139.qstr(value)
            for value in base.fixed_padded_outer(phase["cosine"], 128)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x-power", type=int, default=DEFAULT_X_POWER)
    parser.add_argument(
        "--x-cell-index",
        type=int,
        default=DEFAULT_X_CELL_INDEX,
    )
    parser.add_argument(
        "--beta-power",
        type=int,
        default=DEFAULT_BETA_POWER,
    )
    parser.add_argument("--beta-cell-index", type=int, default=0)
    parser.add_argument("--precision", type=int, default=8192)
    parser.add_argument("--audit-all", action="store_true")
    parser.add_argument("--probe-only", action="store_true")
    args = parser.parse_args()
    summary = (
        probe_owner_cell(
            args.x_power,
            args.x_cell_index,
            args.beta_power,
            args.beta_cell_index,
            args.precision,
        )
        if args.probe_only
        else run_cell(
            args.x_power,
            args.x_cell_index,
            args.beta_power,
            args.beta_cell_index,
            args.precision,
            args.audit_all,
        )
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
