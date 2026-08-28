#!/usr/bin/env python3
"""Re-audit every Round87 registered port with an immutable candidate table."""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
from cm2_round79_tangency_intersection_generator import aq, digest, strict_sign


HERE = Path(__file__).resolve().parent
ROUND87 = HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json"
ROUND87_SOURCE = HERE / "cm2_round87_rank3_port_event_continuation_cert.py"
PINS = {
    ROUND87.name: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    ROUND87_SOURCE.name: "71f10cde22ea191c7710090e2e7474fdbc2925ded94fe60071159b2c262dc834",
}
SCHEMA = "cm2.round99.rank3-registered-port-candidate-audit.v1"
PRECISION_BITS = 512
WORK_CORES: tuple[Any, ...] = ()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def init_worker(precision_bits: int) -> None:
    global WORK_CORES
    ctx.prec = precision_bits
    WORK_CORES = core_cert.physical_cores()


def immutable_competitor_rows(
    state2: dict[str, Any], current_target: str, tangent_target: str, tangent_flight: Any,
) -> tuple[list[dict[str, Any]], str | None, int, int]:
    candidates = tuple(time3.time2_cert.translated_candidate_ids(current_target, state2["chart"]))
    if tangent_target not in candidates:
        raise RuntimeError("tangent candidate absent from immutable translated table")
    generator = time3.time2_cert.translated_candidate_ids(current_target, state2["chart"])
    if tangent_target not in generator:
        raise RuntimeError("tangent candidate absent from historical generator")
    historical_suffix = tuple(generator)
    rows: list[dict[str, Any]] = []
    future: list[tuple[str, Any]] = []
    for candidate_id in candidates:
        if candidate_id == tangent_target:
            continue
        candidate = time3.time2_cert.candidate_root(
            state2["contact_x"], state2["contact_y"],
            state2["outgoing_x"], state2["outgoing_y"],
            state2["s"], candidate_id,
        )
        classification = candidate["classification"]
        if classification == "no_real_intersection":
            relation = "NO_REAL_INTERSECTION"
        elif classification == "intersection_strictly_behind":
            relation = "INTERSECTION_STRICTLY_BEHIND"
        elif classification == "strict_future_near_root":
            near = candidate["near"]
            if bool(near < tangent_flight):
                relation = "STRICTLY_BEFORE_TANGENT_TARGET"
            elif bool(tangent_flight < near):
                relation = "STRICTLY_AFTER_TANGENT_TARGET"
            else:
                raise RuntimeError("unresolved competitor/tangent flight order")
            future.append((candidate_id, near))
        else:
            raise RuntimeError(f"unresolved competitor event equation: {classification}")
        rows.append({
            "candidate_id": candidate_id,
            "candidate_root_classification": classification,
            "relation_to_tangent_target_flight": relation,
        })
    rows.sort(key=lambda item: item["candidate_id"])
    winner = None
    for candidate_id, near in future:
        if all(candidate_id == other_id or bool(near < other_near) for other_id, other_near in future):
            if winner is not None:
                raise RuntimeError("nonunique strict future competitor winner")
            winner = candidate_id
    if future and winner is None:
        raise RuntimeError("unresolved strict future competitor winner")
    return rows, winner, len(candidates), len(candidates) - len(historical_suffix)


def audit_row(task: tuple[int, dict[str, Any], int]) -> tuple[int, dict[str, Any]]:
    index, row, precision_bits = task
    ctx.prec = precision_bits
    source = WORK_CORES[row["source_core_index"]]
    box = tuple(Q(value) for value in row["continuation_slab"]["source_coordinate_box"])
    atom = step1.Atom(
        row["source_core_index"], source, *box, Q(0), Q(0),
        f"round99-port-audit:{row['registered_port_id']}",
    )
    classification, _, destination, state1, owner2 = time3.homogeneity_cert.classify_with_geometry(
        atom, WORK_CORES
    )
    if classification != "SURVIVE_THROUGH_2_INNER" or destination is not None or owner2 is None:
        raise RuntimeError("frozen continuation slab no longer survives through second owner")
    if owner2["selected_target_id"] != row["second_selected_target_id"]:
        raise RuntimeError("frozen continuation slab second owner changed")
    state2 = time3.second_outgoing_state(atom, state1, owner2)
    if state2 is None:
        raise RuntimeError("missing second outgoing state")
    tangent_target = row["third_candidate_id"]
    candidate_x, candidate_y = time3.time2_cert.target_center(tangent_target, state2["s"])
    dx = candidate_x - state2["contact_x"]
    dy = candidate_y - state2["contact_y"]
    tangent_flight = state2["outgoing_x"] * dx + state2["outgoing_y"] * dy
    tangent_sign = strict_sign(tangent_flight)
    if tangent_sign == 0:
        raise RuntimeError("unresolved tangent flight sign")
    rows, winner, full_count, consumed_prefix = immutable_competitor_rows(
        state2, row["second_selected_target_id"], tangent_target, tangent_flight
    )
    tau_max = aq(time3.time2_cert.step1.first_hit.TAU_MAX)
    if tangent_sign < 0:
        corrected = "ALGEBRAIC_TANGENCY_STRICTLY_BEHIND_SECOND__LOCAL_CONTINUATION"
    elif bool(tangent_flight > tau_max):
        corrected = "ALGEBRAIC_TANGENCY_STRICTLY_AFTER_TAU_MAX__LOCAL_CONTINUATION"
    elif bool(tangent_flight < tau_max):
        before = [
            item["candidate_id"] for item in rows
            if item["relation_to_tangent_target_flight"] == "STRICTLY_BEFORE_TANGENT_TARGET"
        ]
        corrected = (
            "ALGEBRAIC_TANGENCY_OCCLUDED_BY_EARLIER_THIRD_OWNER__LOCAL_CONTINUATION"
            if before else "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
        )
        if before and winner not in before:
            raise RuntimeError("corrected winner does not precede tangent target")
    else:
        raise RuntimeError("unresolved tangent flight / tau-max relation")
    historical_rows = row["event_equation_evidence"]["competitor_rows"]
    omitted = sorted(set(item["candidate_id"] for item in rows) - set(item["candidate_id"] for item in historical_rows))
    return index, {
        "registered_port_id": row["registered_port_id"],
        "source_core_index": row["source_core_index"],
        "second_selected_target_id": row["second_selected_target_id"],
        "third_candidate_id": tangent_target,
        "historical_local_event_classification": row["local_event_classification"],
        "corrected_local_event_classification": corrected,
        "classification_changed": corrected != row["local_event_classification"],
        "full_candidate_count": full_count,
        "historically_consumed_prefix_count": consumed_prefix,
        "historically_omitted_candidate_ids": omitted,
        "corrected_unique_strict_future_competitor_winner": winner,
        "corrected_competitor_rows": rows,
        "corrected_competitor_rows_sha256": digest(rows),
    }


def build(precision_bits: int = PRECISION_BITS, workers: int = 16) -> dict[str, Any]:
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    frozen = json.loads(ROUND87.read_text())["result"]
    input_rows = frozen["port_event_rows"]
    tasks = [(index, row, precision_bits) for index, row in enumerate(input_rows)]
    if workers == 1:
        init_worker(precision_bits)
        raw = [audit_row(task) for task in tasks]
    else:
        context = mp.get_context("fork")
        with context.Pool(
            min(workers, os.cpu_count() or 1), initializer=init_worker, initargs=(precision_bits,)
        ) as pool:
            raw = list(pool.imap_unordered(audit_row, tasks))
    raw.sort(key=lambda item: item[0])
    rows = [row for _, row in raw]
    corrected_histogram = Counter(row["corrected_local_event_classification"] for row in rows)
    transition_histogram = Counter(
        row["historical_local_event_classification"] + " -> " + row["corrected_local_event_classification"]
        for row in rows
    )
    changed = [row for row in rows if row["classification_changed"]]
    corrected_physical = [
        row for row in rows
        if row["corrected_local_event_classification"] == "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION"
    ]
    winner_histogram = Counter(
        row["corrected_unique_strict_future_competitor_winner"] for row in changed
        if row["corrected_unique_strict_future_competitor_winner"] is not None
    )
    result = {
        "precision_bits": precision_bits,
        "audited_registered_port_count": len(rows),
        "historical_locally_physical_port_count": frozen["locally_physical_next_tangency_port_count"],
        "corrected_locally_physical_port_count": len(corrected_physical),
        "corrected_locally_nonphysical_port_count": len(rows) - len(corrected_physical),
        "classification_changed_port_count": len(changed),
        "corrected_event_classification_histogram": dict(sorted(corrected_histogram.items())),
        "classification_transition_histogram": dict(sorted(transition_histogram.items())),
        "corrected_earliest_winner_histogram_on_changed_ports": dict(sorted(winner_histogram.items())),
        "minimum_historically_consumed_prefix_count": min(row["historically_consumed_prefix_count"] for row in rows),
        "maximum_historically_consumed_prefix_count": max(row["historically_consumed_prefix_count"] for row in rows),
        "corrected_locally_physical_registered_port_ids": sorted(
            row["registered_port_id"] for row in corrected_physical
        ),
        "audit_rows": rows,
        "audit_rows_sha256": digest(rows),
        "strict_conclusion": "Round87 consumed translated_candidate_ids during membership testing; immutable full-table replay is required for every registered-port physicality label",
        "invalidated_downstream_inputs": [
            "Round87 locally physical registered-port set",
            "Round89 projective gap closure based on Round87 physical ports",
            "Round90 tracked residual closure based on Round89 physical branches",
        ],
        "strict_nonclaims": [
            "no corrected global branch continuation is asserted",
            "no rank-3 face quotient is promoted",
            "global gate vector remains unchanged",
        ],
        "upstream_pins": PINS,
    }
    result = json.loads(json.dumps(result, sort_keys=True))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()
    print(json.dumps(build(args.precision_bits, args.workers), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
