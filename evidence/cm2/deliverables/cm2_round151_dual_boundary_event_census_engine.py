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
import cm2_round150_connected_2d_corridor_engine as r150


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
    "cm2_round150_connected_2d_corridor_engine.py":
        "4d80a8e3cef5e3e754e1b10221716239bc123aa228c6ab27a30b9fc76af336fc",
    "cm2-round150-connected-2d-corridor-atlas-2026-07-24.json":
        "6bb182760205190ad635ef34c21eca6221d2224e2dcdb585f70c157fad76321c",
    "cm2-round150-connected-2d-corridor-atlas-verification-2026-07-24.json":
        "686e236dbe998c111a0307e3edfd34d0b26185b6f52ec54fa33e340725655ee5",
}
POWER = 4296
PRECISION = 8192
RETURN_DEPTH = 1648


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
    verification = json.loads(
        (
            HERE
            / "cm2-round150-connected-2d-corridor-atlas-verification-2026-07-24.json"
        ).read_text(encoding="utf-8")
    )
    require(verification["result"]["status"] == "PASS", "Round150 verification")


def fixed_outer(value: arb, bits: int = 256) -> list[str]:
    return [
        r139.qstr(bound)
        for bound in base.fixed_padded_outer(value, bits)
    ]


def scaled_outer(value: arb, scale: Q, bits: int = 256) -> list[str]:
    return fixed_outer(value * r139.lower.aq(scale), bits)


def qspec(spec: dict[str, str]) -> tuple[Q, Q, Q, Q]:
    return (
        Q(spec["abs_x_lower_h"]),
        Q(spec["abs_x_upper_h"]),
        Q(spec["beta_lower_h"]),
        Q(spec["beta_upper_h"]),
    )


def model_for_spec(
    root: tuple[Q, Q],
    spec: dict[str, str],
) -> base.Model:
    abs_lower, abs_upper, beta_lower, beta_upper = qspec(spec)
    h = Q(1, 2**POWER)
    return r150.arbitrary_initial_model(
        root,
        -Q(abs_lower + abs_upper, 2) * h,
        Q(abs_upper - abs_lower, 2) * h,
        Q(beta_lower + beta_upper, 2) * h,
        Q(beta_upper - beta_lower, 2) * h,
    )


def c24_frontier(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    ctx.prec = PRECISION
    owners, root = r150.load_seed()
    abs_lower, abs_upper, beta_lower, beta_upper = qspec(spec)
    h_q = Q(1, 2**POWER)
    h = r139.lower.aq(h_q)
    x_center_q = -Q(abs_lower + abs_upper, 2) * h_q
    x_radius_q = Q(abs_upper - abs_lower, 2) * h_q
    beta_center_q = Q(beta_lower + beta_upper, 2) * h_q
    beta_radius_q = Q(beta_upper - beta_lower, 2) * h_q
    whole_model, target, derivative = (
        r150.propagate_model_and_jacobian(
            root,
            owners,
            x_center_q,
            x_radius_q,
            beta_center_q,
            beta_radius_q,
        )
    )
    _chart, whole_phase = r150.r146.phase_at_contact(
        whole_model,
        target,
    )
    whole_event = whole_phase["p"] + r139.lower.aq(Q(1, 50))
    require(
        not bool(whole_event > 0) and not bool(whole_event < 0),
        "C24 whole event",
    )
    require(
        bool(derivative[0] > 0) and bool(derivative[1] > 0),
        "C24 derivative signs",
    )
    lower_model, lower_target = r150.propagate_model(
        root,
        owners,
        x_center_q,
        x_radius_q,
        beta_lower * h_q,
        Q(0),
    )
    upper_model, upper_target = r150.propagate_model(
        root,
        owners,
        x_center_q,
        x_radius_q,
        beta_upper * h_q,
        Q(0),
    )
    require(
        lower_target == target == upper_target,
        "C24 target identity",
    )
    _chart, lower_phase = r150.r146.phase_at_contact(
        lower_model,
        lower_target,
    )
    _chart, upper_phase = r150.r146.phase_at_contact(
        upper_model,
        upper_target,
    )
    lower_event = lower_phase["p"] + r139.lower.aq(Q(1, 50))
    upper_event = upper_phase["p"] + r139.lower.aq(Q(1, 50))
    require(
        bool(lower_event < 0) and bool(upper_event > 0),
        "C24 beta edge signs",
    )
    middle_model, middle_target = r150.propagate_model(
        root,
        owners,
        x_center_q,
        x_radius_q,
        beta_center_q,
        Q(0),
    )
    _chart, middle_phase = r150.r146.phase_at_contact(
        middle_model,
        middle_target,
    )
    middle_event = middle_phase["p"] + r139.lower.aq(Q(1, 50))
    interval_newton = (
        r139.lower.aq(beta_center_q)
        - middle_event / derivative[1]
    )
    require(
        bool(interval_newton > r139.lower.aq(beta_lower * h_q))
        and bool(interval_newton < r139.lower.aq(beta_upper * h_q)),
        "C24 interval Newton",
    )
    slope_beta_per_abs_x = derivative[0] / derivative[1]
    require(bool(slope_beta_per_abs_x > 0), "C24 graph slope")
    ledger = base.AuditLedger()
    event_core = r150.terminal_event_core_audit(
        {
            **whole_phase,
            "selected_target_id": target,
            "selected_root": None,
        },
        tuple(r139.lower.core_cert.physical_cores()),
        ledger,
    )
    return {
        "event_kind": "COLLISION1648_TERMINAL_C24_P0_ZERO",
        "event_function": "terminal_p(delta_x,delta_beta)+1/50",
        "abs_delta_x_in_h_units": [
            r139.qstr(abs_lower),
            r139.qstr(abs_upper),
        ],
        "delta_beta_event_box_in_h_units": [
            r139.qstr(beta_lower),
            r139.qstr(beta_upper),
        ],
        "event_function_outer": fixed_outer(whole_event),
        "lower_beta_edge_event_strict_negative": True,
        "upper_beta_edge_event_strict_positive": True,
        "partial_event_partial_delta_x_times_h_outer":
            scaled_outer(derivative[0], h_q),
        "partial_event_partial_delta_beta_times_h_outer":
            scaled_outer(derivative[1], h_q),
        "both_partial_derivatives_strict_positive": True,
        "parametric_interval_newton_beta_in_h_units_outer":
            scaled_outer(interval_newton, Q(1, 1) / h_q),
        "parametric_interval_newton_strictly_inside_event_box": True,
        "unique_beta_root_for_every_fixed_delta_x": True,
        "transverse_to_beta_fibres": True,
        "implicit_beta_per_abs_delta_x_slope_outer":
            fixed_outer(slope_beta_per_abs_x, 128),
        "implicit_beta_per_abs_delta_x_slope_strict_positive": True,
        "sole_unresolved_terminal_core":
            event_core["sole_unresolved_core"],
        "all_other_terminal_core_constraints_strict": True,
        "event_box_id": "round151-c24-event-box:" + digest(spec),
    }


def d3_frontier(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    ctx.prec = PRECISION
    _owners, root = r150.load_seed()
    abs_lower, abs_upper, beta_lower, beta_upper = qspec(spec)
    h_q = Q(1, 2**POWER)
    h = r139.lower.aq(h_q)
    x_center = -r139.lower.aq(Q(abs_lower + abs_upper, 2) * h_q)
    x_radius = r139.lower.aq(Q(abs_upper - abs_lower, 2) * h_q)
    beta_center = r139.lower.aq(Q(beta_lower + beta_upper, 2) * h_q)
    beta_radius = r139.lower.aq(Q(beta_upper - beta_lower, 2) * h_q)
    root_lower, root_upper = map(r139.lower.aq, root)
    t_star = (
        (root_lower + root_upper) / 2
        + r150.r146.symmetric((root_upper - root_lower) / 2)
    )
    whole = r150.r146.anchor_discriminant(
        x_center + r150.r146.symmetric(x_radius),
        beta_center + r150.r146.symmetric(beta_radius),
        t_star,
    )
    require(
        bool(whole.derivative[0] > 0)
        and bool(whole.derivative[1] > 0),
        "D3 derivative signs",
    )
    lower_corner = r150.r146.anchor_discriminant(
        -r139.lower.aq(abs_lower * h_q),
        r139.lower.aq(beta_lower * h_q),
        t_star,
    )
    upper_corner = r150.r146.anchor_discriminant(
        -r139.lower.aq(abs_upper * h_q),
        r139.lower.aq(beta_upper * h_q),
        t_star,
    )
    require(
        bool(lower_corner.value < 0)
        and bool(upper_corner.value > 0),
        "D3 edge signs",
    )
    center = r150.r146.anchor_discriminant(
        x_center,
        beta_center,
        t_star,
    )
    mean_value = (
        center.value
        + whole.derivative[0] * r150.r146.symmetric(x_radius)
    )
    interval_newton = beta_center - mean_value / whole.derivative[1]
    require(
        bool(interval_newton > r139.lower.aq(beta_lower * h_q))
        and bool(interval_newton < r139.lower.aq(beta_upper * h_q)),
        "D3 interval Newton",
    )
    slope_beta_per_abs_x = whole.derivative[0] / whole.derivative[1]
    require(bool(slope_beta_per_abs_x > 0), "D3 graph slope")
    return {
        "event_kind": "COLLISION3_D0_TANGENCY_D3_ZERO",
        "event_function": "D3(delta_x,delta_beta)",
        "anchor_candidate": r139.ANCHOR,
        "abs_delta_x_in_h_units": [
            r139.qstr(abs_lower),
            r139.qstr(abs_upper),
        ],
        "delta_beta_event_box_in_h_units": [
            r139.qstr(beta_lower),
            r139.qstr(beta_upper),
        ],
        "D3_strictly_increasing_in_delta_x": True,
        "D3_strictly_increasing_in_delta_beta": True,
        "lower_beta_corner_D3_strict_negative": True,
        "upper_beta_corner_D3_strict_positive": True,
        "parametric_interval_newton_beta_in_h_units_outer":
            fixed_outer(interval_newton / h, 256),
        "parametric_interval_newton_strictly_inside_event_box": True,
        "unique_beta_root_for_every_fixed_delta_x": True,
        "transverse_to_beta_fibres": True,
        "implicit_beta_per_abs_delta_x_slope_outer":
            fixed_outer(slope_beta_per_abs_x, 128),
        "implicit_beta_per_abs_delta_x_slope_strict_positive": True,
        "Jacobian_outer": {
            "partial_D3_partial_delta_x":
                fixed_outer(whole.derivative[0], 128),
            "partial_D3_partial_delta_beta":
                fixed_outer(whole.derivative[1], 128),
        },
        "event_box_id": "round151-d3-event-box:" + digest(spec),
    }


def audit_c24_event_box(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    ctx.prec = PRECISION
    owners, root = r150.load_seed()
    model = model_for_spec(root, spec)
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
        "official registry",
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
            f"C24 owner:{collision_index}",
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
            f"C24 word:{collision_index}:{word_error}",
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
        current_chart, phase = r150.r146.phase_at_contact(
            model,
            current_target,
        )
        require(bool(phase["cosine"] > 0), f"C24 cosine:{collision_index}")
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
                f"C24 preterminal core:{collision_index}:{classification}",
            )
            r139.lower.round136.core_margin(
                certified_owner,
                classification,
                destination,
                cores,
                ledger,
            )
        else:
            terminal_event = r150.terminal_event_core_audit(
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
        official_id = r139.lower.round136.compact_key(
            word["key"]
        )["official_word_key_id"]
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
    require(terminal_event is not None, "C24 terminal event")
    return {
        "status": "PASS",
        "event_box_id": "round151-c24-event-box:" + digest(spec),
        "collision_count": RETURN_DEPTH,
        "full_radius4_candidate_test_count": 161 * RETURN_DEPTH,
        "official_sequence_sha256": digest(official_ids),
        "compact_rows_sha256": digest(compact_rows),
        "homogeneity_histogram": dict(Counter(homogeneity_labels)),
        "incidence_histogram": dict(Counter(incidence_ranks)),
        "preterminal_strict_nonreturn_count": RETURN_DEPTH - 1,
        "terminal_event": terminal_event,
        "strict_margin_ledger_sha256": digest({
            name: [ledger.depths[name], ledger.counts[name]]
            for name in sorted(ledger.depths)
        }),
        "ledger_worst_depth": max(ledger.depths.values()),
    }


def event_candidate_universe(
    candidate_ids: tuple[str, ...],
    state: dict[str, arb],
    expected_owner: str,
    ledger: base.AuditLedger,
    prefix: str,
) -> dict[str, Any]:
    qx, qy, ux, uy = (
        state["contact_x"],
        state["contact_y"],
        state["outgoing_x"],
        state["outgoing_y"],
    )
    future = {}
    histogram: Counter[str] = Counter()
    anchor_ell = None
    for candidate_id in candidate_ids:
        center_x, center_y = (
            r139.lower.time3.time2_cert.target_center(
                candidate_id,
                arb(0),
            )
        )
        dx, dy = center_x - qx, center_y - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = r139.lower.aq(
            r139.lower.time3.time2_cert.first_hit.RADIUS[candidate_id[0]]
        )
        discriminant = radius * radius - transverse * transverse
        witness = {"collision_index": 3, "candidate_id": candidate_id}
        if candidate_id == r139.ANCHOR:
            require(
                not bool(discriminant > 0)
                and not bool(discriminant < 0),
                f"{prefix} anchor event",
            )
            require(bool(ell > 0), f"{prefix} anchor flight")
            anchor_ell = ell
            histogram["sole_unresolved_anchor_discriminant"] += 1
            continue
        if bool(discriminant < 0):
            ledger.observe(
                prefix + "_candidate_miss_discriminant",
                -discriminant,
                witness,
            )
            histogram["no_real_intersection"] += 1
            continue
        require(bool(discriminant > 0), f"{prefix} other discriminant")
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            ledger.observe(
                prefix + "_candidate_behind_far_root",
                -far,
                witness,
            )
            histogram["intersection_strictly_behind"] += 1
            continue
        require(bool(near > 0), f"{prefix} future root")
        ledger.observe(
            prefix + "_candidate_future_root_positive",
            near,
            witness,
        )
        future[candidate_id] = near
        histogram["strict_future_near_root"] += 1
    require(anchor_ell is not None, f"{prefix} anchor census")
    require(expected_owner in future, f"{prefix} expected future owner")
    selected = future[expected_owner]
    for candidate_id, near in future.items():
        if candidate_id == expected_owner:
            continue
        ledger.observe(
            prefix + "_winner_pairwise_root_gap",
            near - selected,
            {
                "collision_index": 3,
                "winner_id": expected_owner,
                "competitor_id": candidate_id,
            },
        )
    preemption = selected - anchor_ell
    require(bool(preemption > 0), f"{prefix} anchor preemption")
    preemption_depth = ledger.observe(
        prefix + "_anchor_double_root_preempts_frozen_winner",
        preemption,
        {
            "collision_index": 3,
            "anchor_id": r139.ANCHOR,
            "frozen_winner_id": expected_owner,
        },
    )
    require(
        sum(histogram.values()) == len(candidate_ids),
        f"{prefix} candidate census",
    )
    return {
        "candidate_count": len(candidate_ids),
        "candidate_classification_histogram": dict(sorted(histogram.items())),
        "sole_unresolved_candidate": r139.ANCHOR,
        "sole_unresolved_event": "D3=0",
        "frozen_winner_excluding_anchor": expected_owner,
        "anchor_double_root_strictly_preempts_frozen_winner": True,
        "anchor_preemption_margin_dyadic_depth": preemption_depth,
        "all_other_candidate_decisions_strict": True,
        "all_other_winner_gaps_strict": True,
    }


def audit_d3_event_box(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    ctx.prec = PRECISION
    owners, root = r150.load_seed()
    model = model_for_spec(root, spec)
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    current_chart = "E"
    ledger = base.AuditLedger()
    for collision_index, expected_owner in enumerate(owners[:2], start=1):
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
            f"D3 prefix owner:{collision_index}",
        )
        model, _ = base.step_model_with_audit(model, expected_owner)
        current_target = expected_owner
        current_chart, phase = r150.r146.phase_at_contact(
            model,
            current_target,
        )
        require(bool(phase["cosine"] > 0), f"D3 prefix cosine:{collision_index}")
    boxes = model.boxes()
    state = {
        "contact_x": boxes[0],
        "contact_y": boxes[1],
        "outgoing_x": boxes[2],
        "outgoing_y": boxes[3],
    }
    retained_ids = tuple(
        r139.lower.time3.time2_cert.translated_candidate_ids(
            current_target,
            current_chart,
        )
    )
    full_ids = tuple(r139.lower.charge.candidate_ids_around(current_target))
    require(len(full_ids) == 161, "D3 full radius4 universe")
    retained = event_candidate_universe(
        retained_ids,
        state,
        owners[2],
        ledger,
        "retained",
    )
    full = event_candidate_universe(
        full_ids,
        state,
        owners[2],
        ledger,
        "full_radius4",
    )
    require(
        retained["frozen_winner_excluding_anchor"]
        == full["frozen_winner_excluding_anchor"]
        == owners[2],
        "D3 retained/full winner",
    )
    return {
        "status": "PASS",
        "event_box_id": "round151-d3-event-box:" + digest(spec),
        "fully_audited_prefix_collision_count": 2,
        "fully_audited_prefix_radius4_candidate_test_count": 2 * 161,
        "collision3_retained_candidate_event_census": retained,
        "collision3_full_radius4_candidate_event_census": full,
        "collision3_full_radius4_candidate_test_count": 161,
        "collision3_anchor_is_immediate_owner_switch": True,
        "strict_margin_ledger_sha256": digest({
            name: [ledger.depths[name], ledger.counts[name]]
            for name in sorted(ledger.depths)
        }),
        "ledger_worst_depth": max(ledger.depths.values()),
    }


if __name__ == "__main__":
    raise SystemExit("library module")
