#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
import cm2_round141_centered_affine_d0_collar_spike as base
import cm2_round146_physical_centered_jet_2d_engine as r146
import cm2_round149_terminal_c24_two_sided_engine as r149


HERE = Path(__file__).resolve().parent
PINS = {
    "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py":
        "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json":
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    "cm2_round141_centered_affine_d0_collar_spike.py":
        "5656f33a4974b63124bda19c56716dccb7c52ad7840741668512795560007ef1",
    "cm2_round146_physical_centered_jet_2d_engine.py":
        "ac332c1cc99c96a56251a53b2432caaba951f028de810045d840b8991bdf27eb",
    "cm2_round149_terminal_c24_two_sided_engine.py":
        "ffa02ee24969f7b9b4cbd0d81690ba209411a5a00f869a2d935135d1d2376aa8",
}
POWER = 4296
BETA_POWER = 4304
PRECISION = 8192
RETURN_DEPTH = 1648
EVENT_ABS_X_LEFT_IN_H = Q(4675, 32)
EVENT_ABS_X_RIGHT_IN_H = Q(1169, 8)
EVENT_BETA_RADIUS_IN_H = Q(1, 256)


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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def check_pins() -> None:
    for name, expected in PINS.items():
        require(sha256(HERE / name) == expected, f"pin mismatch:{name}")


def load_seed() -> tuple[list[str], tuple[Q, Q]]:
    document = json.loads(r146.R139_CERTIFICATE.read_text(encoding="utf-8"))
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
    require(len(owners) == RETURN_DEPTH, "owner path depth")
    return owners, root


def arbitrary_initial_model(
    root: tuple[Q, Q],
    x_center_q: Q,
    x_radius_q: Q,
    beta_center_q: Q,
    beta_radius_q: Q,
) -> base.Model:
    x_center = r139.lower.aq(x_center_q)
    x_radius = r139.lower.aq(x_radius_q)
    beta_center = r139.lower.aq(beta_center_q)
    beta_radius = r139.lower.aq(beta_radius_q)
    root_lower, root_upper = map(r139.lower.aq, root)
    root_center = r146.point((root_lower + root_upper) / 2)
    root_ball = root_center + r146.symmetric((root_upper - root_lower) / 2)
    center_values = r146.physical_initial(
        base.Dual(x_center, [arb(1), arb(0)]),
        base.Dual(beta_center, [arb(0), arb(1)]),
        root_center,
    )
    interval_values = r146.physical_initial(
        base.Dual(
            x_center + r146.symmetric(x_radius),
            [arb(1), arb(0)],
        ),
        base.Dual(
            beta_center + r146.symmetric(beta_radius),
            [arb(0), arb(1)],
        ),
        root_ball,
    )
    root_only_values = r146.physical_initial(
        base.Dual(x_center, [arb(1), arb(0)]),
        base.Dual(beta_center, [arb(0), arb(1)]),
        root_ball,
    )
    raw_affine = base.rows(center_values)
    affine = [[r146.point(entry) for entry in row] for row in raw_affine]
    interval_derivatives = base.rows(interval_values)
    domain_radii = (x_radius, beta_radius)
    centers = [r146.point(value.value) for value in center_values]
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


def propagate_model(
    root: tuple[Q, Q],
    owners: list[str],
    x_center_q: Q,
    x_radius_q: Q,
    beta_center_q: Q,
    beta_radius_q: Q,
) -> tuple[base.Model, str]:
    model = arbitrary_initial_model(
        root,
        x_center_q,
        x_radius_q,
        beta_center_q,
        beta_radius_q,
    )
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    for expected_owner in owners:
        model, _ = base.step_model_with_audit(model, expected_owner)
        current_target = expected_owner
    return model, current_target


def propagate_model_and_jacobian(
    root: tuple[Q, Q],
    owners: list[str],
    x_center_q: Q,
    x_radius_q: Q,
    beta_center_q: Q,
    beta_radius_q: Q,
) -> tuple[base.Model, str, list[arb]]:
    model = arbitrary_initial_model(
        root,
        x_center_q,
        x_radius_q,
        beta_center_q,
        beta_radius_q,
    )
    x_center = r139.lower.aq(x_center_q)
    x_radius = r139.lower.aq(x_radius_q)
    beta_center = r139.lower.aq(beta_center_q)
    beta_radius = r139.lower.aq(beta_radius_q)
    root_lower, root_upper = map(r139.lower.aq, root)
    root_ball = (
        r146.point((root_lower + root_upper) / 2)
        + r146.symmetric((root_upper - root_lower) / 2)
    )
    initial_values = r146.physical_initial(
        base.Dual(
            x_center + r146.symmetric(x_radius),
            [arb(1), arb(0)],
        ),
        base.Dual(
            beta_center + r146.symmetric(beta_radius),
            [arb(0), arb(1)],
        ),
        root_ball,
    )
    parameter_jacobian = base.rows(initial_values)
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    for expected_owner in owners:
        boxes = model.boxes()
        state = [
            base.Dual(
                boxes[row],
                [arb(int(row == column)) for column in range(4)],
            )
            for row in range(4)
        ]
        center, radius = base.target_geometry(expected_owner)
        outputs, _ = base.collision(state, center, radius)
        local_jacobian = base.rows(outputs)
        parameter_jacobian = [
            [
                sum(
                    (
                        local_jacobian[row][inner]
                        * parameter_jacobian[inner][column]
                        for inner in range(4)
                    ),
                    arb(0),
                )
                for column in range(2)
            ]
            for row in range(4)
        ]
        model, _ = base.step_model_with_audit(model, expected_owner)
        current_target = expected_owner
    boxes = model.boxes()
    state = [
        base.Dual(
            boxes[row],
            [arb(int(row == column)) for column in range(4)],
        )
        for row in range(4)
    ]
    center, radius = base.target_geometry(current_target)
    normal_x = (state[0] - center[0]) / radius
    normal_y = (state[1] - center[1]) / radius
    momentum = -state[2] * normal_y + state[3] * normal_x
    derivative = [
        sum(
            (
                momentum.derivative[inner]
                * parameter_jacobian[inner][column]
                for inner in range(4)
            ),
            arb(0),
        )
        for column in range(2)
    ]
    return model, current_target, derivative


def fixed_outer(value: arb, bits: int = 256) -> list[str]:
    return [
        r139.qstr(bound)
        for bound in base.fixed_padded_outer(value, bits)
    ]


def scaled_outer(value: arb, scale: Q, bits: int = 256) -> list[str]:
    return fixed_outer(value * r139.lower.aq(scale), bits)


def core_margins(
    core: Any,
    normal_x: arb,
    normal_y: arb,
    momentum: arb,
) -> tuple[list[arb], list[arb]]:
    cell = core.chart_id.split(":")[1]
    t, _inside, _outside = (
        r139.lower.time3.time2_cert.step1.chart_tests(
            cell,
            normal_x,
            normal_y,
        )
    )
    if cell == "E":
        inside = [normal_x, abs(normal_x) - abs(normal_y)]
        outside = [-normal_x, abs(normal_y) - abs(normal_x)]
    elif cell == "W":
        inside = [-normal_x, abs(normal_x) - abs(normal_y)]
        outside = [normal_x, abs(normal_y) - abs(normal_x)]
    elif cell == "N":
        inside = [normal_y, abs(normal_y) - abs(normal_x)]
        outside = [-normal_y, abs(normal_x) - abs(normal_y)]
    else:
        inside = [-normal_y, abs(normal_y) - abs(normal_x)]
        outside = [normal_y, abs(normal_x) - abs(normal_y)]
    inside.extend([
        t - r139.lower.aq(core.t0),
        r139.lower.aq(core.t1) - t,
        momentum - r139.lower.aq(core.p0),
        r139.lower.aq(core.p1) - momentum,
    ])
    outside.extend([
        r139.lower.aq(core.t0) - t,
        t - r139.lower.aq(core.t1),
        r139.lower.aq(core.p0) - momentum,
        momentum - r139.lower.aq(core.p1),
    ])
    return inside, outside


def terminal_event_core_audit(
    certified_owner: dict[str, Any],
    cores: tuple[Any, ...],
    ledger: base.AuditLedger,
) -> dict[str, Any]:
    classification, destination, witnesses = (
        r139.lower.time3.core_classification(certified_owner, cores)
    )
    require(
        classification == "UNRESOLVED_TIME3_OUTER"
        and destination is None,
        "terminal event classification",
    )
    unresolved = [
        row["core_id"]
        for row in witnesses
        if row["kind"] == "unresolved"
    ]
    require(
        unresolved == [r139.EXPECTED_DESTINATION_CORE_ID],
        "sole terminal unresolved core",
    )
    relevant = [
        core
        for core in cores
        if core.source == certified_owner["selected_target_id"][0]
    ]
    event_outer = None
    non_event_depths = []
    for core in relevant:
        identifier = r139.lower.time3.time2_cert.step1.core_id(core)
        inside, outside = core_margins(
            core,
            certified_owner["normal_x"],
            certified_owner["normal_y"],
            certified_owner["p"],
        )
        if identifier == r139.EXPECTED_DESTINATION_CORE_ID:
            require(
                all(bool(value > 0) for index, value in enumerate(inside)
                    if index != 4),
                "terminal event non-event inside margins",
            )
            require(
                not bool(inside[4] > 0) and not bool(inside[4] < 0),
                "terminal event function crosses zero",
            )
            non_event_depths.extend(
                ledger.observe(
                    "terminal_event_nonzero_core_margin",
                    value,
                )
                for index, value in enumerate(inside)
                if index != 4
            )
            event_outer = fixed_outer(inside[4])
        else:
            positive = [value for value in outside if bool(value > 0)]
            require(positive, f"terminal competing core exclusion:{identifier}")
            non_event_depths.extend(
                ledger.observe(
                    "terminal_event_competing_core_exclusion_margin",
                    value,
                )
                for value in positive
            )
    require(event_outer is not None and non_event_depths, "terminal event census")
    return {
        "classification": classification,
        "destination_core": None,
        "sole_unresolved_core": r139.EXPECTED_DESTINATION_CORE_ID,
        "event_function": "terminal_p+1/50",
        "event_function_outer": event_outer,
        "all_other_core_constraints_strict": True,
        "competing_cores_strictly_excluded": True,
        "non_event_margin_worst_dyadic_depth": max(non_event_depths),
    }


def audit_terminal_event_box() -> dict[str, Any]:
    check_pins()
    ctx.prec = PRECISION
    owners, root = load_seed()
    h = Q(1, 2**POWER)
    x_lower = -EVENT_ABS_X_RIGHT_IN_H * h
    x_upper = -EVENT_ABS_X_LEFT_IN_H * h
    x_center = (x_lower + x_upper) / 2
    x_radius = (x_upper - x_lower) / 2
    beta_radius = EVENT_BETA_RADIUS_IN_H * h
    model = arbitrary_initial_model(
        root,
        x_center,
        x_radius,
        Q(0),
        beta_radius,
    )
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    current_chart = "E"
    ledger = base.AuditLedger()
    official_ids = []
    compact_rows = []
    homogeneity_labels = []
    incidence_ranks = []
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
    terminal_event = None
    for collision_index, expected_owner in enumerate(owners, start=1):
        incoming_target = current_target
        boxes = model.boxes()
        state = {
            "contact_x": boxes[0],
            "contact_y": boxes[1],
            "outgoing_x": boxes[2],
            "outgoing_y": boxes[3],
            "s": arb(0),
            "chart": current_chart,
        }
        owner, _ = r139.lower.round136.complete_owner(
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
            f"event owner mismatch:{collision_index}",
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
            f"event official word:{collision_index}:{word_error}",
        )
        r139.official_wall_margin_audit(
            state,
            current_target,
            owner,
            ledger,
            collision_index,
        )
        model, _ = base.step_model_with_audit(model, expected_owner)
        current_target = expected_owner
        current_chart, phase = r146.phase_at_contact(
            model,
            current_target,
        )
        require(
            bool(phase["cosine"] > 0),
            f"event positive cosine:{collision_index}",
        )
        certified_owner = {
            **phase,
            "selected_target_id": expected_owner,
            "selected_root": owner["selected_root"],
        }
        classification, destination, _ = (
            r139.lower.time3.core_classification(
                certified_owner,
                cores,
            )
        )
        if collision_index < RETURN_DEPTH:
            require(
                classification == "SURVIVE_THROUGH_3_INNER"
                and destination is None,
                f"event preterminal C24:{collision_index}:{classification}",
            )
            r139.lower.round136.core_margin(
                certified_owner,
                classification,
                destination,
                cores,
                ledger,
            )
        else:
            terminal_event = terminal_event_core_audit(
                certified_owner,
                cores,
                ledger,
            )
        homogeneity, _ = r139.lower.generic_homogeneity_label(
            collision_index,
            phase["cosine"],
            ledger,
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
    require(terminal_event is not None, "terminal event row")
    return {
        "status": "PASS",
        "role": "terminal_c24_event_box",
        "minimum_certified_precision_bits": PRECISION,
        "delta_x_interval": [r139.qstr(x_lower), r139.qstr(x_upper)],
        "abs_delta_x_in_h_units": [
            r139.qstr(EVENT_ABS_X_LEFT_IN_H),
            r139.qstr(EVENT_ABS_X_RIGHT_IN_H),
        ],
        "delta_beta_interval": [
            r139.qstr(-beta_radius),
            r139.qstr(beta_radius),
        ],
        "delta_beta_in_h_units": [
            r139.qstr(-EVENT_BETA_RADIUS_IN_H),
            r139.qstr(EVENT_BETA_RADIUS_IN_H),
        ],
        "collision_count": RETURN_DEPTH,
        "full_radius4_candidate_test_count": 161 * RETURN_DEPTH,
        "official_sequence_sha256": digest(official_ids),
        "compact_rows_sha256": digest(compact_rows),
        "homogeneity_histogram": dict(Counter(homogeneity_labels)),
        "incidence_histogram": dict(Counter(incidence_ranks)),
        "preterminal_strict_nonreturn_count": RETURN_DEPTH - 1,
        "terminal_event": terminal_event,
        "strict_margin_ledger_names": sorted(ledger.depths),
        "strict_margin_ledger_sha256": digest({
            name: [ledger.depths[name], ledger.counts[name]]
            for name in sorted(ledger.depths)
        }),
        "ledger_worst_depth": max(ledger.depths.values()),
    }


def terminal_event_frontier() -> dict[str, Any]:
    check_pins()
    ctx.prec = PRECISION
    owners, root = load_seed()
    h = Q(1, 2**POWER)
    x_lower = -EVENT_ABS_X_RIGHT_IN_H * h
    x_upper = -EVENT_ABS_X_LEFT_IN_H * h
    x_center = (x_lower + x_upper) / 2
    x_radius = (x_upper - x_lower) / 2
    beta_radius = EVENT_BETA_RADIUS_IN_H * h
    whole_model, current_target, derivative = (
        propagate_model_and_jacobian(
            root,
            owners,
            x_center,
            x_radius,
            Q(0),
            beta_radius,
        )
    )
    _chart, whole_phase = r146.phase_at_contact(
        whole_model,
        current_target,
    )
    event_whole = whole_phase["p"] + r139.lower.aq(Q(1, 50))
    require(
        not bool(event_whole > 0) and not bool(event_whole < 0),
        "whole event box crosses p0",
    )
    require(
        bool(derivative[0] > 0) and bool(derivative[1] > 0),
        "terminal event derivative signs",
    )
    left_model, left_target = propagate_model(
        root,
        owners,
        x_upper,
        Q(0),
        Q(0),
        beta_radius,
    )
    right_model, right_target = propagate_model(
        root,
        owners,
        x_lower,
        Q(0),
        Q(0),
        beta_radius,
    )
    require(
        left_target == current_target == right_target,
        "terminal target identity",
    )
    _chart, left_phase = r146.phase_at_contact(left_model, left_target)
    _chart, right_phase = r146.phase_at_contact(right_model, right_target)
    left_event = left_phase["p"] + r139.lower.aq(Q(1, 50))
    right_event = right_phase["p"] + r139.lower.aq(Q(1, 50))
    require(
        bool(left_event > 0) and bool(right_event < 0),
        "terminal event edge signs",
    )
    middle_model, middle_target = propagate_model(
        root,
        owners,
        x_center,
        Q(0),
        Q(0),
        beta_radius,
    )
    _chart, middle_phase = r146.phase_at_contact(
        middle_model,
        middle_target,
    )
    middle_event = middle_phase["p"] + r139.lower.aq(Q(1, 50))
    interval_newton = (
        r139.lower.aq(x_center)
        - middle_event / derivative[0]
    )
    require(
        bool(interval_newton > r139.lower.aq(x_lower))
        and bool(interval_newton < r139.lower.aq(x_upper)),
        "terminal parametric interval Newton inclusion",
    )
    delta_x_slope = -derivative[1] / derivative[0]
    abs_x_slope = derivative[1] / derivative[0]
    require(
        bool(delta_x_slope < 0) and bool(abs_x_slope > 0),
        "terminal event graph slope",
    )
    return {
        "event_kind": "COLLISION1648_TERMINAL_C24_P0_ZERO",
        "event_function": "terminal_p(delta_x,delta_beta)+1/50",
        "event_box": {
            "abs_delta_x_in_h_units": [
                r139.qstr(EVENT_ABS_X_LEFT_IN_H),
                r139.qstr(EVENT_ABS_X_RIGHT_IN_H),
            ],
            "delta_beta_in_h_units": [
                r139.qstr(-EVENT_BETA_RADIUS_IN_H),
                r139.qstr(EVENT_BETA_RADIUS_IN_H),
            ],
        },
        "whole_box_event_function_outer": fixed_outer(event_whole),
        "return_side_edge_event_function_outer": fixed_outer(left_event),
        "survive_side_edge_event_function_outer": fixed_outer(right_event),
        "return_side_edge_strict_positive": True,
        "survive_side_edge_strict_negative": True,
        "partial_event_partial_delta_x_times_h_outer":
            scaled_outer(derivative[0], h),
        "partial_event_partial_delta_beta_times_h_outer":
            scaled_outer(derivative[1], h),
        "partial_event_partial_delta_x_strict_positive": True,
        "partial_event_partial_delta_beta_strict_positive": True,
        "parametric_interval_newton_abs_delta_x_in_h_units_outer":
            scaled_outer(-interval_newton, Q(1, 1) / h),
        "parametric_interval_newton_strictly_inside_event_box": True,
        "unique_delta_x_root_for_every_fixed_delta_beta": True,
        "transverse_to_delta_x_fibres": True,
        "implicit_delta_x_per_delta_beta_slope_outer":
            fixed_outer(delta_x_slope, 128),
        "implicit_abs_delta_x_per_delta_beta_slope_outer":
            fixed_outer(abs_x_slope, 128),
        "implicit_delta_x_per_delta_beta_slope_strict_negative": True,
        "implicit_abs_delta_x_per_delta_beta_slope_strict_positive": True,
        "terminal_event_graph_id":
            "round150-terminal-c24-p0-event-graph:"
            + digest({
                "event": "terminal_p+1/50",
                "x": [
                    r139.qstr(EVENT_ABS_X_LEFT_IN_H),
                    r139.qstr(EVENT_ABS_X_RIGHT_IN_H),
                ],
                "beta": [
                    r139.qstr(-EVENT_BETA_RADIUS_IN_H),
                    r139.qstr(EVENT_BETA_RADIUS_IN_H),
                ],
            }),
    }


def audit_regular_cell(spec: dict[str, Any]) -> dict[str, Any]:
    check_pins()
    return r149.audit_cell(spec)


if __name__ == "__main__":
    raise SystemExit("library module")
