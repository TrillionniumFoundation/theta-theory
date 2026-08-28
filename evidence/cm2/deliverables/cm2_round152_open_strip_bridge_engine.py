#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_round151_dual_boundary_event_census_engine as r151


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
    "cm2_round151_dual_boundary_event_census_engine.py":
        "dca8a2bc670411074703d4a87a5557649fa3506fbcb4e62a144cb81e01a22085",
    "cm2-round151-dual-boundary-event-census-2026-07-24.json":
        "593188b5e9996cfa8151cd15c318a7a6136c108dba123cc91e421c83f7aea821",
    "cm2-round151-dual-boundary-event-census-verification-2026-07-24.json":
        "61e053ca782cd030bb6d3a182e7ff4f032e4d6bb2fadf1fa82682789908ae1cd",
}
r139 = r151.r139
base = r151.base
r150 = r151.r150
r146 = r150.r146
POWER = r151.POWER
PRECISION = r151.PRECISION
RETURN_DEPTH = r151.RETURN_DEPTH


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
            / "cm2-round151-dual-boundary-event-census-verification-2026-07-24.json"
        ).read_text(encoding="utf-8")
    )
    require(verification["result"]["status"] == "PASS", "Round151 verification")


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


def collision3_anchor_exclusion(
    spec: dict[str, str],
    root: tuple[Q, Q],
) -> dict[str, Any]:
    ctx.prec = PRECISION
    abs_lower, abs_upper, beta_lower, beta_upper = qspec(spec)
    h_q = Q(1, 2**POWER)
    x_center = -r139.lower.aq(Q(abs_lower + abs_upper, 2) * h_q)
    x_radius = r139.lower.aq(Q(abs_upper - abs_lower, 2) * h_q)
    beta_center = r139.lower.aq(Q(beta_lower + beta_upper, 2) * h_q)
    beta_radius = r139.lower.aq(Q(beta_upper - beta_lower, 2) * h_q)
    root_lower, root_upper = map(r139.lower.aq, root)
    t_star = (
        (root_lower + root_upper) / 2
        + r146.symmetric((root_upper - root_lower) / 2)
    )
    whole = r146.anchor_discriminant(
        x_center + r146.symmetric(x_radius),
        beta_center + r146.symmetric(beta_radius),
        t_star,
    )
    require(
        bool(whole.derivative[0] > 0)
        and bool(whole.derivative[1] > 0),
        "bridge D3 coordinate monotonicity",
    )
    maximum_corner = r146.anchor_discriminant(
        -r139.lower.aq(abs_lower * h_q),
        r139.lower.aq(beta_upper * h_q),
        t_star,
    )
    require(
        bool(maximum_corner.value < 0),
        "bridge D3 maximum strict negative",
    )
    return {
        "method":
            "full-bridge derivative signs plus exact upper-right corner",
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
            r139.lower.round136.strict_dyadic_depth(-maximum_corner.value),
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


def terminal_return_monotonicity(
    spec: dict[str, str],
    owners: list[str],
    root: tuple[Q, Q],
) -> dict[str, Any]:
    ctx.prec = PRECISION
    abs_lower, abs_upper, beta_lower, beta_upper = qspec(spec)
    h_q = Q(1, 2**POWER)
    x_center_q = -Q(abs_lower + abs_upper, 2) * h_q
    x_radius_q = Q(abs_upper - abs_lower, 2) * h_q
    beta_center_q = Q(beta_lower + beta_upper, 2) * h_q
    beta_radius_q = Q(beta_upper - beta_lower, 2) * h_q
    _whole_model, target, derivative = (
        r150.propagate_model_and_jacobian(
            root,
            owners,
            x_center_q,
            x_radius_q,
            beta_center_q,
            beta_radius_q,
        )
    )
    require(
        bool(derivative[1] > 0),
        "terminal event beta derivative positive on bridge",
    )
    lower_model, lower_target = r150.propagate_model(
        root,
        owners,
        x_center_q,
        x_radius_q,
        beta_lower * h_q,
        Q(0),
    )
    require(lower_target == target, "terminal target identity")
    _chart, lower_phase = r146.phase_at_contact(
        lower_model,
        lower_target,
    )
    lower_event = lower_phase["p"] + r139.lower.aq(Q(1, 50))
    require(
        bool(lower_event > 0),
        "terminal event positive on bridge lower edge",
    )
    return {
        "event_function": "terminal_p(delta_x,delta_beta)+1/50",
        "beta_lower_edge_event_outer": fixed_outer(lower_event),
        "beta_lower_edge_event_strict_positive": True,
        "partial_event_partial_delta_beta_times_h_outer":
            scaled_outer(derivative[1], h_q),
        "partial_event_partial_delta_beta_strict_positive_on_full_bridge":
            True,
        "terminal_event_strict_positive_on_entire_bridge": True,
        "forced_terminal_classification": "RETURN_AT_3_INNER",
        "forced_terminal_destination_core":
            r139.EXPECTED_DESTINATION_CORE_ID,
    }


def audit_bridge_cell(spec: dict[str, str]) -> dict[str, Any]:
    check_pins()
    ctx.prec = PRECISION
    owners, root = r150.load_seed()
    anchor_proof = collision3_anchor_exclusion(spec, root)
    terminal_proof = terminal_return_monotonicity(spec, owners, root)
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
    terminal_event_audit = None
    collision3_retained_audit = None
    collision3_full_audit = None
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
        if collision_index == r139.ANCHOR_COLLISION_INDEX:
            retained_ids = tuple(
                r139.lower.time3.time2_cert.translated_candidate_ids(
                    current_target,
                    current_chart,
                )
            )
            full_ids = tuple(
                r139.lower.charge.candidate_ids_around(current_target)
            )
            owner, collision3_retained_audit = (
                r146.candidates_owner_excluding_physical_anchor(
                    state,
                    current_target,
                    retained_ids,
                    ledger,
                    collision_index,
                    False,
                    anchor_proof,
                )
            )
            full_owner, collision3_full_audit = (
                r146.candidates_owner_excluding_physical_anchor(
                    state,
                    current_target,
                    full_ids,
                    ledger,
                    collision_index,
                    True,
                    anchor_proof,
                )
            )
            require(
                owner["selected_target_id"]
                == full_owner["selected_target_id"]
                == expected_owner,
                "collision3 retained/full owner",
            )
        else:
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
            f"bridge owner:{collision_index}",
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
            f"bridge word:{collision_index}:{word_error}",
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
            f"bridge cosine:{collision_index}",
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
                f"bridge preterminal core:{collision_index}:{classification}",
            )
            r139.lower.round136.core_margin(
                certified_owner,
                classification,
                destination,
                cores,
                ledger,
            )
            recorded_classification = classification
            recorded_destination = destination
        else:
            terminal_event_audit = r150.terminal_event_core_audit(
                certified_owner,
                cores,
                ledger,
            )
            require(
                terminal_proof[
                    "terminal_event_strict_positive_on_entire_bridge"
                ] is True,
                "terminal return forcing",
            )
            recorded_classification = "RETURN_AT_3_INNER"
            recorded_destination = r139.EXPECTED_DESTINATION_CORE_ID
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
            recorded_classification,
            recorded_destination,
        ])
        previous_cosine = phase["cosine"]
    require(
        terminal_event_audit is not None
        and collision3_retained_audit is not None
        and collision3_full_audit is not None,
        "bridge special audits",
    )
    require(
        terminal_event_audit["sole_unresolved_core"]
        == r139.EXPECTED_DESTINATION_CORE_ID,
        "bridge terminal core",
    )
    return {
        "status": "PASS",
        "bridge_cell_id": "round152-open-strip-bridge:" + digest(spec),
        "abs_delta_x_in_h_units": [
            r139.qstr(value)
            for value in qspec(spec)[:2]
        ],
        "delta_beta_in_h_units": [
            r139.qstr(value)
            for value in qspec(spec)[2:]
        ],
        "collision_count": RETURN_DEPTH,
        "full_radius4_candidate_test_count": 161 * RETURN_DEPTH,
        "collision3_physical_anchor_exclusion": anchor_proof,
        "collision3_retained_candidate_audit": collision3_retained_audit,
        "collision3_full_radius4_candidate_audit": collision3_full_audit,
        "terminal_event_non_event_core_audit": terminal_event_audit,
        "terminal_return_monotonicity": terminal_proof,
        "terminal_classification": "RETURN_AT_3_INNER",
        "terminal_destination_core": r139.EXPECTED_DESTINATION_CORE_ID,
        "official_sequence_sha256": digest(official_ids),
        "compact_rows_sha256": digest(compact_rows),
        "homogeneity_histogram": dict(Counter(homogeneity_labels)),
        "incidence_histogram": dict(Counter(incidence_ranks)),
        "preterminal_strict_nonreturn_count": RETURN_DEPTH - 1,
        "strict_margin_ledger_sha256": digest({
            name: [ledger.depths[name], ledger.counts[name]]
            for name in sorted(ledger.depths)
        }),
        "ledger_worst_depth": max(ledger.depths.values()),
    }


if __name__ == "__main__":
    raise SystemExit("library module")
