#!/usr/bin/env python3
"""Append-only export and typing audit for the last 164 Gate-3 graphs."""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate3_critical_graph_owner_typing_frontier_cert as critical_frozen


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent
CRITICAL_MANIFEST = (
    HERE / "cm2-gate3-critical-graph-owner-typing-frontier-manifest-2026-07-16.json"
)
ENDPOINT_MANIFEST = (
    HERE / "cm2-gate3-endpoint-scaled-resultant-frontier-manifest-2026-07-16.json"
)
frozen = critical_frozen.frozen
outer = critical_frozen.outer
deep = critical_frozen.deep

TARGET_ROWS = (8, 15, 36, 51)
SELECTIVE_T = 6
SELECTIVE_V = 4
MAX_OWNER_ADDITIONAL_T = 8
MAX_OWNER_ADDITIONAL_V = 8
EXPECTED_NONZERO_ROWS = {
    8: {
        "audit_call_count": 39648,
        "untyped_graph_count": 41,
        "untyped_graph_failure_counts": {
            "additional_ambiguous_candidate_may_precede": 15,
            "untyped_candidate_graph_cover": 26,
        },
        "untyped_graph_ledger_sha256": (
            "ea14c3d45d1321d8fe74660aae21e54d9092ae6c9e66fca1cfe91370c8f0f115"
        ),
    },
    15: {
        "audit_call_count": 39648,
        "untyped_graph_count": 41,
        "untyped_graph_failure_counts": {
            "additional_ambiguous_candidate_may_precede": 15,
            "untyped_candidate_graph_cover": 26,
        },
        "untyped_graph_ledger_sha256": (
            "ce1e15b1c1478ba0f72f64d67a0499b0200f6931c5f9f9cc6983a448111cc1ad"
        ),
    },
    36: {
        "audit_call_count": 39648,
        "untyped_graph_count": 41,
        "untyped_graph_failure_counts": {
            "additional_ambiguous_candidate_may_precede": 15,
            "untyped_candidate_graph_cover": 26,
        },
        "untyped_graph_ledger_sha256": (
            "2ae8af19087d89c323a15d97fa8c15167ddf69305f73b100fa8b3acabb6b0877"
        ),
    },
    51: {
        "audit_call_count": 39648,
        "untyped_graph_count": 41,
        "untyped_graph_failure_counts": {
            "additional_ambiguous_candidate_may_precede": 15,
            "untyped_candidate_graph_cover": 26,
        },
        "untyped_graph_ledger_sha256": (
            "f90b5efc94370fa6c01b2662d850c288231249f987ce31e3e1a50052fe666e2b"
        ),
    },
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def base_record(
    row_index: int, row: dict[str, Any], box: outer.FutureBox,
) -> dict[str, Any]:
    return {
        "row_index": row_index,
        "occurrence_id": row["occurrence_id"],
        "t": [str(box.t0), str(box.t1)],
        "v": [str(box.v0), str(box.v1)],
        "s": [str(box.s0), str(box.s1)],
        "t_depth": box.t_depth,
        "v_depth": box.v_depth,
    }


def export_untyped_one_row(
    task: tuple[int, dict[str, Any], list[outer.FutureBox]],
) -> dict[str, Any]:
    """Replay independent initial cells of one depth-(6,4) row."""

    row_index, row, initial_boxes = task
    pending = list(initial_boxes)
    untyped = []
    calls = 0
    while pending:
        box = pending.pop()
        calls += 1
        status, witness = outer.audit_box(row, box)
        if status == "refine_t" and box.t_depth < frozen.MAX_T_DEPTH:
            pending.extend(reversed(box.split_t()))
            continue
        if status == "refine_t" and box.v_depth < frozen.MAX_V_DEPTH:
            pending.extend(reversed(box.split_v()))
            continue
        if status == "refine_v" and box.v_depth < frozen.MAX_V_DEPTH:
            pending.extend(reversed(box.split_v()))
            continue
        if status == "refine_v" and box.t_depth < frozen.MAX_T_DEPTH:
            pending.extend(reversed(box.split_t()))
            continue
        if status in {
            "analytic_unresolved", "owner_unresolved",
            "multi_or_tangent_unresolved",
        }:
            if box.t_depth < frozen.MAX_T_DEPTH:
                pending.extend(reversed(box.split_t()))
                continue
            if box.v_depth < frozen.MAX_V_DEPTH:
                pending.extend(reversed(box.split_v()))
                continue

        base = base_record(row_index, row, box)
        if status == "transverse_root_strip":
            candidate = witness["candidate_relative_to_miss_source"]
            ok, typed = frozen.physical_first_witness(row, box, candidate)
            if ok:
                continue
            if box.t_depth < SELECTIVE_T:
                pending.extend(reversed(box.split_t()))
                continue
            if box.v_depth < SELECTIVE_V:
                pending.extend(reversed(box.split_v()))
                continue
            # Preserve the predecessor record byte-for-byte so its compact
            # per-row ledger digest can be checked, rather than merely
            # reproducing the aggregate count.
            untyped.append({
                **base, **witness, **typed,
                "root_registry_kind": "full_slab_bracketed_transverse_graph",
            })
            continue
        if status == "immutable":
            continue

        reason = witness.get("reason", status)
        if reason == "transverse_candidate_not_bracketed_on_full_s_slab":
            candidate = witness.get("candidate_relative_to_miss_source")
            if isinstance(candidate, str):
                ok, typed = frozen.physical_first_witness(row, box, candidate)
                if ok:
                    continue
                if box.t_depth < SELECTIVE_T:
                    pending.extend(reversed(box.split_t()))
                    continue
                if box.v_depth < SELECTIVE_V:
                    pending.extend(reversed(box.split_v()))
                    continue
                witness = {**witness, **typed}
                reason = typed.get("physical_first_failure", reason)
        if box.t_depth < SELECTIVE_T:
            pending.extend(reversed(box.split_t()))
            continue
        if box.v_depth < SELECTIVE_V:
            pending.extend(reversed(box.split_v()))
            continue
        covered, graph_rows, summary = frozen.candidate_graph_cover(row, box)
        if covered:
            for graph in graph_rows:
                untyped.append({
                    **base, **graph,
                    "t_interval_ownership": (
                        "[t0,t1), except the final t1=1 endpoint is closed"
                    ),
                    "v_interval_ownership": (
                        "[v0,v1), except the final v1=1 endpoint is closed"
                    ),
                    "empty_graph_chart_contributes_zero_current": True,
                })
            continue
        # Positive-width terminal classes are deliberately irrelevant here.

    return {
        "row_index": row_index,
        "audit_call_count": calls,
        "records": untyped,
    }


def _type_task(
    task: tuple[list[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    return critical_frozen.type_one_graph(*task)


def strict_preempting_collision(
    rows: list[dict[str, Any]], record: dict[str, Any],
) -> dict[str, Any]:
    """Exclude a candidate zero if another strict positive root is earlier.

    Uniqueness of the earlier root is unnecessary: the existence of any
    certified collision strictly before the candidate tangent time already
    proves that the candidate cannot be a physical first future face.
    """

    row_index = int(record["row_index"])
    row = rows[row_index]
    candidate = record["candidate"]
    box = critical_frozen.box_from_graph(record)
    t_radius = (box.t1 - box.t0) / 2
    s_radius = (box.s1 - box.s0) / 2
    try:
        centre, interval = outer.geometry_on_box(
            row, box.t0, box.t1, box.s0, box.s1
        )
        boundary_projection = frozen.enclosure(
            centre["candidates"][candidate]["projection"],
            interval["candidates"][candidate]["projection"],
            t_radius, s_radius,
        )
        preemptors = []
        for relative_id in sorted(interval["candidates"]):
            if relative_id == candidate:
                continue
            root = frozen.positive_root_enclosure(
                centre["candidates"][relative_id],
                interval["candidates"][relative_id],
                t_radius, s_radius,
            )
            if root is not None and bool(root < boundary_projection):
                preemptors.append({
                    "relative_id": relative_id,
                    "positive_root_enclosure": str(root),
                })
        if preemptors:
            return {
                "classification": "strictly_preempted_nonphysical_tangency",
                "record": {
                    **record,
                    "classification": "strictly_preempted_nonphysical_tangency",
                    "candidate_tangent_time_enclosure": str(
                        boundary_projection
                    ),
                    "strict_preemption_inequality": (
                        "upper(other_positive_near_root)<"
                        "lower(candidate_tangent_projection)"
                    ),
                    "strict_preemptor_count": len(preemptors),
                    "strict_preemptor_ledger_sha256": canonical_digest(
                        preemptors
                    ),
                },
            }
    except (AssertionError, KeyError, ValueError, ZeroDivisionError) as exc:
        exception = type(exc).__name__
    else:
        exception = None
    return {
        "classification": "untyped_after_strict_preemption_audit",
        "record": {
            **record,
            "strict_preemption_failure": (
                f"interval_exception:{exception}"
                if exception else "no_strict_positive_root_before_candidate"
            ),
        },
    }


def _preempt_task(
    task: tuple[list[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    return strict_preempting_collision(*task)


def build_result() -> dict[str, Any]:
    wrapper = json.loads(CRITICAL_MANIFEST.read_text(encoding="utf-8"))
    assert wrapper["verdict"]["critical_graph_physical_future_exclusion"] == "CERTIFIED"
    assert wrapper["verdict"]["gate3"] == "NOT_CERTIFIED"
    endpoint_wrapper = json.loads(ENDPOINT_MANIFEST.read_text(encoding="utf-8"))
    endpoint = endpoint_wrapper["result"]["deeper_selective_frontier"]
    assert endpoint["untyped_candidate_graph_chart_count"] == 164
    assert endpoint["untyped_graph_failure_counts"] == {
        "additional_ambiguous_candidate_may_precede": 60,
        "untyped_candidate_graph_cover": 104,
    }
    critical_frontier = wrapper["result"]["remaining_frontier"]
    assert critical_frontier["frozen_unexported_untyped_graph_count"] == 164
    assert critical_frontier[
        "safe_maximum_candidate_graph_charts_on_one_fixed_s_slice"
    ] == 592
    assert critical_frontier[
        "safe_maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice"
    ] == 51404
    rows, provenance = frozen.load_dependencies()
    workers = min(
        int(os.environ.get("CM2_WORKERS", "32")), os.cpu_count() or 1, 64
    )
    cell_tasks = [
        (index, rows[index], [box])
        for index in TARGET_ROWS
        for box in outer.initial_boxes_for_row(index)
    ]
    assert len(cell_tasks) == 1024
    with multiprocessing.get_context("fork").Pool(workers) as pool:
        cell_parts = list(pool.imap_unordered(
            export_untyped_one_row,
            cell_tasks,
            chunksize=1,
        ))
    parts = []
    for index in TARGET_ROWS:
        selected = [part for part in cell_parts if part["row_index"] == index]
        row_records = [
            record for part in selected for record in part["records"]
        ]
        row_records.sort(key=canonical_json)
        parts.append({
            "row_index": index,
            "initial_cell_task_count": len(selected),
            "audit_call_count": sum(
                part["audit_call_count"] for part in selected
            ),
            "untyped_graph_count": len(row_records),
            "untyped_graph_failure_counts": dict(sorted(Counter(
                record.get(
                    "physical_first_failure",
                    "untyped_candidate_graph_cover",
                )
                for record in row_records
            ).items())),
            "untyped_graph_ledger_sha256": canonical_digest(row_records),
            "records": row_records,
        })
    observed_nonzero = {
        part["row_index"]: {
            key: part[key]
            for key in (
                "audit_call_count", "untyped_graph_count",
                "untyped_graph_failure_counts",
                "untyped_graph_ledger_sha256",
            )
        }
        for part in parts if part["untyped_graph_count"]
    }
    assert observed_nonzero == EXPECTED_NONZERO_ROWS
    records = [record for part in parts for record in part.pop("records")]
    records.sort(key=canonical_json)
    assert len(records) == 164, [
        {
            "row_index": part["row_index"],
            "untyped_graph_count": part["untyped_graph_count"],
            "untyped_graph_failure_counts": part[
                "untyped_graph_failure_counts"
            ],
        }
        for part in parts
    ]
    assert len({canonical_json(record) for record in records}) == 164

    typing_records = [
        {
            **record,
            "candidate": record["candidate_relative_to_miss_source"],
        }
        for record in records
    ]
    tasks = [(rows, record) for record in typing_records]
    old_owner_t = critical_frozen.MAX_TYPING_ADDITIONAL_T
    old_owner_v = critical_frozen.MAX_TYPING_ADDITIONAL_V
    try:
        critical_frozen.MAX_TYPING_ADDITIONAL_T = MAX_OWNER_ADDITIONAL_T
        critical_frozen.MAX_TYPING_ADDITIONAL_V = MAX_OWNER_ADDITIONAL_V
        with multiprocessing.get_context("fork").Pool(workers) as pool:
            typed_parts = list(pool.imap_unordered(
                _type_task, tasks, chunksize=1
            ))
    finally:
        critical_frozen.MAX_TYPING_ADDITIONAL_T = old_owner_t
        critical_frozen.MAX_TYPING_ADDITIONAL_V = old_owner_v
    typed = [leaf for part in typed_parts for leaf in part["typed"]]
    delta_excluded = [leaf for part in typed_parts for leaf in part["excluded"]]
    nonphysical = [leaf for part in typed_parts for leaf in part["nonphysical"]]
    direct_nonphysical_time = list(nonphysical)
    untyped = [leaf for part in typed_parts for leaf in part["untyped"]]
    preemption_input_count = len(untyped)
    if untyped:
        with multiprocessing.get_context("fork").Pool(workers) as pool:
            preemption_parts = list(pool.imap_unordered(
                _preempt_task,
                [(rows, record) for record in untyped],
                chunksize=1,
            ))
        strictly_preempted = [
            part["record"] for part in preemption_parts
            if part["classification"]
            == "strictly_preempted_nonphysical_tangency"
        ]
        untyped = [
            part["record"] for part in preemption_parts
            if part["classification"]
            == "untyped_after_strict_preemption_audit"
        ]
        nonphysical.extend(strictly_preempted)
    else:
        strictly_preempted = []
    for ledger in (typed, delta_excluded, nonphysical, untyped):
        ledger.sort(key=canonical_json)
    failures: Counter[str] = Counter()
    for part in typed_parts:
        failures.update(part["encountered_failure_counts"])

    complete = not untyped
    result = {
        "schema": "cm2.gate3.remaining-graph-complete-current-frontier.v1",
        "provenance": {
            "frozen_critical_manifest_sha256": file_sha256(CRITICAL_MANIFEST),
            "frozen_critical_certificate_sha256": file_sha256(
                Path(critical_frozen.__file__).resolve()
            ),
            "frozen_endpoint_manifest_sha256": file_sha256(
                ENDPOINT_MANIFEST
            ),
            "frozen_critical_internal_replay_digest": wrapper["result"][
                "internal_replay_digest"
            ],
            "maximal_row_registry_sha256": provenance[
                "maximal_row_registry_sha256"
            ],
            "arithmetic_precision_bits": 384,
            "owner_typing_maximum_additional_t_depth": (
                MAX_OWNER_ADDITIONAL_T
            ),
            "owner_typing_maximum_additional_parameter_depth": (
                MAX_OWNER_ADDITIONAL_V
            ),
        },
        "last_164_coordinate_export": {
            "target_row_indices": list(TARGET_ROWS),
            "target_row_count": len(TARGET_ROWS),
            "exported_untyped_graph_count": len(records),
            "equals_frozen_aggregate_and_therefore_exhausts_it": True,
            "coordinate_ledger_sha256": canonical_digest(records),
            "per_row_summaries": parts,
            "per_row_summary_ledger_sha256": canonical_digest(parts),
        },
        "last_164_owner_typing": {
            "input_graph_count": len(records),
            "typing_audit_call_count": sum(
                part["audit_call_count"] for part in typed_parts
            ),
            "strict_preemption_audit_input_count": preemption_input_count,
            "strict_preemption_root_branch_requirements": (
                "full-box discriminant>0, positive near root, near root<3"
            ),
            "strict_preemption_inequality": (
                "upper(other_positive_near_root)<"
                "lower(candidate_tangent_projection)"
            ),
            "one_strict_preemptor_suffices_without_unique_owner": True,
            "strictly_preempted_nonphysical_descendant_count": len(
                strictly_preempted
            ),
            "strictly_preempted_nonphysical_ledger_sha256": canonical_digest(
                sorted(strictly_preempted, key=canonical_json)
            ),
            "typed_graph_leaf_count": len(typed),
            "Delta_strict_excluded_descendant_count": len(delta_excluded),
            "strict_nonphysical_time_descendant_count": len(
                direct_nonphysical_time
            ),
            "total_nonphysical_descendant_count": len(nonphysical),
            "untyped_graph_leaf_count": len(untyped),
            "encountered_failure_counts": dict(sorted(failures.items())),
            "typed_graph_ledger_sha256": canonical_digest(typed),
            "Delta_excluded_ledger_sha256": canonical_digest(delta_excluded),
            "strict_nonphysical_time_ledger_sha256": canonical_digest(
                sorted(direct_nonphysical_time, key=canonical_json)
            ),
            "total_nonphysical_ledger_sha256": canonical_digest(nonphysical),
            "untyped_graph_ledger_sha256": canonical_digest(untyped),
        },
        "complete_current_frontier": {
            "all_1052_predecessor_untyped_graphs_resolved": complete,
            "remaining_untyped_graph_count": len(untyped),
            "complete_conditionally_physical_first_graph_chart_count": (
                41344 + len(typed) if complete else None
            ),
            "complete_marked_current_TV_upper": (
                "518152320" if complete else None
            ),
            "predecessor_candidate_graph_fixed_s_count_upper": (
                592 if complete else None
            ),
            "predecessor_candidate_graph_fixed_s_normalized_slope_sum_upper": (
                51404 if complete else None
            ),
            "refining_or_excluding_old_candidate_charts_cannot_increase_these_outers": (
                complete
            ),
            "TV_outer_was_frozen_on_complete_physical_plus_1052_candidate_graph_atlas": (
                complete
            ),
            "complete_side_owner_current": complete,
            "strong_DQ_MT_DQ_FACE": False,
            "gate3": False,
        },
        "exact_remaining_blockers": [
            "resolve every retained untyped descendant" if untyped else "none: graph typing/current layer complete",
            "prove common branch-record strong DQ/MT_DQ and physical FACE_2CUT/FACE_TIME",
        ],
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


if __name__ == "__main__":
    print(json.dumps(build_result(), sort_keys=True, indent=2))
