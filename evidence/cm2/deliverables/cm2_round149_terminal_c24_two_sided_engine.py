#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

from flint import arb, ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
import cm2_round141_centered_affine_d0_collar_spike as base
import cm2_round146_physical_centered_jet_2d_engine as r146


HERE = Path(__file__).resolve().parent
PINS = {
    "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py": "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json": "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    "cm2_round141_centered_affine_d0_collar_spike.py": "5656f33a4974b63124bda19c56716dccb7c52ad7840741668512795560007ef1",
    "cm2_round146_physical_centered_jet_2d_engine.py": "ac332c1cc99c96a56251a53b2432caaba951f028de810045d840b8991bdf27eb",
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def check_pins():
    for name, expected in PINS.items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"pin mismatch:{name}")


def audit_cell(spec):
    check_pins()
    x_power = spec["x_power"]
    x_cell_index = spec["x_cell_index"]
    beta_power = spec["beta_power"]
    beta_cell_index = spec["beta_cell_index"]
    expected_terminal = spec["expected_terminal_classification"]
    precision = spec.get("precision", 8192)
    if expected_terminal not in {"RETURN_AT_3_INNER", "SURVIVE_THROUGH_3_INNER"}:
        raise RuntimeError("terminal expectation")
    ctx.prec = precision
    document = json.loads(r146.R139_CERTIFICATE.read_text(encoding="utf-8"))
    result = document["result"]
    owners = [row["selected_absolute_owner_id"] for row in result["collision_rows"]]
    root = tuple(Q(value) for value in result["deep_same_D0_root_and_b_star"]["deep_D0_root_bracket"])
    model = r146.initial_model(root, x_power, x_cell_index, beta_power, beta_cell_index)
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    current_chart = "E"
    ledger = base.AuditLedger()
    official_ids = []
    compact_rows = []
    homogeneity_labels = []
    incidence_ranks = []
    cores = tuple(r139.lower.core_cert.physical_cores())
    pair_index, pattern_index, registry_sha = r139.lower.component_cert.key_index_tables()
    if registry_sha != r139.OFFICIAL_REGISTRY_SHA256:
        raise RuntimeError("official registry")
    initial_boxes = model.boxes()
    source_center, source_radius = base.target_geometry(current_target)
    initial_nx = (initial_boxes[0] - source_center[0]) / source_radius
    initial_ny = (initial_boxes[1] - source_center[1]) / source_radius
    initial_p = -initial_boxes[2] * initial_ny + initial_boxes[3] * initial_nx
    previous_cosine = (1 - initial_p * initial_p).sqrt()
    terminal_classification = None
    terminal_destination = None
    terminal_phase = None
    for collision_index, expected_owner in enumerate(owners, start=1):
        incoming_target = current_target
        boxes = model.boxes()
        state = {
            "contact_x": boxes[0], "contact_y": boxes[1],
            "outgoing_x": boxes[2], "outgoing_y": boxes[3],
            "s": arb(0), "chart": current_chart,
        }
        owner, _ = r139.lower.round136.complete_owner(state, current_target, ledger, collision_index)
        r139.lower.full_radius4_candidate_audit(state, current_target, owner, ledger, collision_index)
        if owner["selected_target_id"] != expected_owner:
            raise RuntimeError(f"owner mismatch:{collision_index}")
        word, word_error = r139.lower.round136.translation_normalized_official_word(
            state, current_target, owner, pair_index, pattern_index
        )
        if word is None or word_error is not None:
            raise RuntimeError(f"official word:{collision_index}:{word_error}")
        r139.official_wall_margin_audit(state, current_target, owner, ledger, collision_index)
        model, _ = base.step_model_with_audit(model, expected_owner)
        current_target = expected_owner
        current_chart, phase = r146.phase_at_contact(model, current_target)
        if not bool(phase["cosine"] > 0):
            raise RuntimeError(f"positive cosine:{collision_index}")
        certified_owner = {**phase, "selected_target_id": expected_owner, "selected_root": owner["selected_root"]}
        classification, destination, _ = r139.lower.time3.core_classification(certified_owner, cores)
        if collision_index < r146.RETURN_DEPTH:
            if classification != "SURVIVE_THROUGH_3_INNER" or destination is not None:
                raise RuntimeError(f"preterminal C24:{collision_index}:{classification}")
        else:
            if classification != expected_terminal:
                raise RuntimeError(f"terminal C24:{classification}:{expected_terminal}")
            if expected_terminal == "RETURN_AT_3_INNER" and destination != r139.EXPECTED_DESTINATION_CORE_ID:
                raise RuntimeError("terminal destination")
            if expected_terminal == "SURVIVE_THROUGH_3_INNER" and destination is not None:
                raise RuntimeError("survive destination")
            terminal_classification = classification
            terminal_destination = destination
            terminal_phase = phase
        r139.lower.round136.core_margin(certified_owner, classification, destination, cores, ledger)
        homogeneity, _ = r139.lower.generic_homogeneity_label(collision_index, phase["cosine"], ledger)
        source_rank = r139.lower.round136.capped_reciprocal_cosine_rank(previous_cosine, ledger, collision_index, "source")
        target_rank = r139.lower.round136.capped_reciprocal_cosine_rank(phase["cosine"], ledger, collision_index, "target")
        incidence = max(14, source_rank, target_rank)
        r139.lower.round136.chart_margin({"chart": current_chart, "normal_x": phase["normal_x"], "normal_y": phase["normal_y"]}, ledger)
        compact_key = r139.lower.round136.compact_key(word["key"])
        official_id = compact_key["official_word_key_id"]
        official_ids.append(official_id)
        homogeneity_labels.append(homogeneity)
        incidence_ranks.append(incidence)
        compact_rows.append([
            collision_index, incoming_target, expected_owner, official_id,
            homogeneity, incidence, classification, destination,
        ])
        previous_cosine = phase["cosine"]
    if terminal_phase is None:
        raise RuntimeError("terminal phase")
    x_width = Q(1, 2**x_power)
    beta_radius = Q(1, 2**beta_power)
    x_lower = -Q(x_cell_index + 1) * x_width
    x_upper = -Q(x_cell_index) * x_width
    beta_center = 2 * beta_cell_index * beta_radius
    return {
        "status": "PASS",
        "x_power": x_power,
        "x_cell_index": x_cell_index,
        "beta_power": beta_power,
        "beta_cell_index": beta_cell_index,
        "delta_x_interval": [r139.qstr(x_lower), r139.qstr(x_upper)],
        "delta_beta_interval": [r139.qstr(beta_center - beta_radius), r139.qstr(beta_center + beta_radius)],
        "collision_count": r146.RETURN_DEPTH,
        "full_radius4_candidate_test_count": 161 * r146.RETURN_DEPTH,
        "official_sequence_sha256": digest(official_ids),
        "compact_rows_sha256": digest(compact_rows),
        "homogeneity_histogram": dict(Counter(homogeneity_labels)),
        "incidence_histogram": dict(Counter(incidence_ranks)),
        "terminal_classification": terminal_classification,
        "terminal_destination_core": terminal_destination,
        "terminal_p_fixed_dyadic_outer": [
            r139.qstr(value) for value in base.fixed_padded_outer(terminal_phase["p"], 128)
        ],
        "strict_margin_ledger_names": sorted(ledger.depths),
        "strict_margin_ledger_sha256": digest({
            name: [ledger.depths[name], ledger.counts[name]] for name in sorted(ledger.depths)
        }),
        "ledger_worst_depth": max(ledger.depths.values()),
    }


if __name__ == "__main__":
    raise SystemExit("library module")
