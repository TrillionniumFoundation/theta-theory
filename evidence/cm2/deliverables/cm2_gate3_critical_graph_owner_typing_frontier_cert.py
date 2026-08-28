#!/usr/bin/env python3
"""Append-only Gate-3 typing audit for the 888 critical graph leaves.

The cancellation-free interval-frontier stack is treated as frozen input.
This layer replays the fifteenth critical refinement solely to export the
coordinates that the old compact manifest retained only by hash, then tries
conditional physical-first owner typing on every actual zero subset.
"""

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

import cm2_gate3_cancellation_free_current_frontier_cert as interval_frozen


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent
INTERVAL_MANIFEST = (
    HERE / "cm2-gate3-cancellation-free-current-frontier-manifest-2026-07-16.json"
)
deep = interval_frozen.previous
frozen = deep.frozen
outer = deep.outer

MAX_TYPING_ADDITIONAL_T = 3
MAX_TYPING_ADDITIONAL_V = 3


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export_one_candidate(
    row_index: int, row: dict[str, Any], initial: outer.FutureBox,
    candidate: str, *, additional_t: int = 5, additional_v: int = 5,
) -> dict[str, Any]:
    """Exact replay of the frozen refinement, now exporting graph leaves."""

    queue = [initial]
    delta_excluded = []
    graphs = []
    regular = []
    unresolved = []
    calls = 0
    while queue:
        box = queue.pop()
        calls += 1
        try:
            delta, delta_t, second = deep.critical_system_enclosure(
                row, box, candidate
            )
            if not delta.contains(0):
                delta_excluded.append({
                    **deep.box_record(row_index, row, box),
                    "candidate": candidate,
                    "exclusion": "Delta_strict_sign",
                    "Delta": str(delta),
                })
                continue
            if not delta_t.contains(0):
                dt_lower = min(abs(delta_t.lower()), abs(delta_t.upper()))
                ds_upper = max(abs(second.ds.lower()), abs(second.ds.upper()))
                slope_ball = (ds_upper / dt_lower / 200).upper().ceil()
                slope = slope_ball.unique_fmpz()
                assert slope is not None
                graphs.append({
                    **deep.box_record(row_index, row, box),
                    "candidate": candidate,
                    "Delta": str(delta),
                    "Delta_t": str(delta_t),
                    "Delta_s": str(second.ds),
                    "normalized_dt_dv_absolute_slope_integer_upper": int(slope),
                    "possibly_empty_transverse_zero_graph": True,
                })
                continue
            determinant = -(second.ds * second.dtt)
            if not determinant.contains(0):
                regular.append({
                    **deep.box_record(row_index, row, box),
                    "candidate": candidate,
                    "minus_Delta_s_Delta_tt": str(determinant),
                })
                continue
        except (AssertionError, KeyError, ValueError, ZeroDivisionError) as exc:
            exception = type(exc).__name__
        else:
            exception = None

        can_t = box.t_depth < initial.t_depth + additional_t
        can_v = box.v_depth < initial.v_depth + additional_v
        if can_t or can_v:
            added_t = box.t_depth - initial.t_depth
            added_v = box.v_depth - initial.v_depth
            if can_t and (not can_v or added_t <= added_v):
                queue.extend(reversed(box.split_t()))
            else:
                queue.extend(reversed(box.split_v()))
            continue
        unresolved.append({
            **deep.box_record(row_index, row, box),
            "candidate": candidate,
            "exception": exception,
        })

    for ledger in (delta_excluded, graphs, regular, unresolved):
        ledger.sort(key=canonical_json)
    return {
        "audit_call_count": calls,
        "delta_excluded": delta_excluded,
        "graphs": graphs,
        "regular": regular,
        "unresolved": unresolved,
    }


def export_critical_graphs(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tasks = []
    for spec in deep.critical_terminal_box_specs():
        row_index = int(spec["row_index"])
        row = rows[row_index]
        box = deep.critical_box_from_spec(spec)
        candidates = deep.critical_candidates(row, box)
        tasks.extend((row_index, row, box, candidate) for candidate in candidates)
    assert len(tasks) == 444
    workers = min(
        int(os.environ.get("CM2_WORKERS", "32")), os.cpu_count() or 1, 64
    )
    with multiprocessing.get_context("fork").Pool(workers) as pool:
        parts = list(pool.starmap(export_one_candidate, tasks, chunksize=1))
    delta_excluded = [leaf for part in parts for leaf in part["delta_excluded"]]
    graphs = [leaf for part in parts for leaf in part["graphs"]]
    regular = [leaf for part in parts for leaf in part["regular"]]
    unresolved = [leaf for part in parts for leaf in part["unresolved"]]
    for ledger in (delta_excluded, graphs, regular, unresolved):
        ledger.sort(key=canonical_json)
    assert sum(part["audit_call_count"] for part in parts) == 3196
    assert len(delta_excluded) == 932
    assert len(graphs) == 888
    assert not regular and not unresolved
    return {
        "coarse_candidate_task_count": len(tasks),
        "audit_call_count": sum(part["audit_call_count"] for part in parts),
        "Delta_strict_excluded_leaf_count": len(delta_excluded),
        "transverse_graph_leaf_count": len(graphs),
        "regular_fold_leaf_count": len(regular),
        "unresolved_leaf_count": len(unresolved),
        "Delta_excluded_coordinate_ledger_sha256": canonical_digest(delta_excluded),
        "transverse_graph_coordinate_ledger_sha256": canonical_digest(graphs),
        "graphs": graphs,
    }


def box_from_graph(record: dict[str, Any]) -> outer.FutureBox:
    return outer.FutureBox(
        int(record["row_index"]), Q(record["t"][0]), Q(record["t"][1]),
        Q(record["v"][0]), Q(record["v"][1]),
        int(record["t_depth"]), int(record["v_depth"]),
    )


def graph_delta_enclosure(
    row: dict[str, Any], box: outer.FutureBox, candidate: str,
) -> tuple[Any, Any, Any]:
    t_radius = (box.t1 - box.t0) / 2
    s_radius = (box.s1 - box.s0) / 2
    centre, interval = outer.geometry_on_box(
        row, box.t0, box.t1, box.s0, box.s1
    )
    centre_delta = centre["candidates"][candidate]["discriminant"]
    interval_delta = interval["candidates"][candidate]["discriminant"]
    centre_projection = centre["candidates"][candidate]["projection"]
    interval_projection = interval["candidates"][candidate]["projection"]
    delta = frozen.enclosure(
        centre_delta, interval_delta, t_radius, s_radius
    )
    projection = frozen.enclosure(
        centre_projection, interval_projection, t_radius, s_radius
    )
    return delta, interval_delta, projection


def type_one_graph(
    rows: list[dict[str, Any]], record: dict[str, Any],
) -> dict[str, Any]:
    row_index = int(record["row_index"])
    row = rows[row_index]
    candidate = record["candidate"]
    initial = box_from_graph(record)
    pending = [initial]
    typed = []
    excluded = []
    nonphysical = []
    untyped = []
    calls = 0
    failures: Counter[str] = Counter()
    while pending:
        box = pending.pop()
        calls += 1
        try:
            delta, interval_delta, projection = graph_delta_enclosure(
                row, box, candidate
            )
            if not delta.contains(0):
                excluded.append({
                    **deep.box_record(row_index, row, box),
                    "candidate": candidate,
                    "classification": "Delta_strict_exclusion",
                })
                continue
            if bool(projection < 0):
                nonphysical.append({
                    **deep.box_record(row_index, row, box),
                    "candidate": candidate,
                    "classification": "strictly_behind_nonphysical_tangency",
                    "candidate_tangent_time_enclosure": str(projection),
                })
                continue
            if bool(projection > outer.arbq(outer.TAU_MAX)):
                nonphysical.append({
                    **deep.box_record(row_index, row, box),
                    "candidate": candidate,
                    "classification": "strictly_after_tau3_nonphysical_tangency",
                    "candidate_tangent_time_enclosure": str(projection),
                })
                continue
            if interval_delta.dt.contains(0):
                failure = "candidate_dt_not_strict_after_refinement"
                witness = {"physical_first_failure": failure}
            else:
                ok, witness = frozen.physical_first_witness(row, box, candidate)
                if ok:
                    typed.append({
                        **deep.box_record(row_index, row, box),
                        "candidate": candidate,
                        "classification": "conditionally_physical_first_graph",
                        "miss_side_alternative_owner": witness[
                            "miss_side_alternative_owner"
                        ],
                        "dt_sign": witness["dt_discriminant_strict_sign"],
                        "normalized_slope_upper": witness[
                            "normalized_dt_dv_absolute_slope_integer_upper"
                        ],
                        "typing_witness_sha256": canonical_digest(witness),
                    })
                    continue
                failure = witness.get(
                    "physical_first_failure", "unclassified_physical_first_failure"
                )
        except (AssertionError, KeyError, ValueError, ZeroDivisionError) as exc:
            failure = f"interval_exception:{type(exc).__name__}"
            witness = {"physical_first_failure": failure}
        failures[failure] += 1
        added_t = box.t_depth - initial.t_depth
        added_v = box.v_depth - initial.v_depth
        can_t = added_t < MAX_TYPING_ADDITIONAL_T
        can_v = added_v < MAX_TYPING_ADDITIONAL_V
        if can_t or can_v:
            if can_t and (not can_v or added_t <= added_v):
                pending.extend(reversed(box.split_t()))
            else:
                pending.extend(reversed(box.split_v()))
            continue
        untyped.append({
            **deep.box_record(row_index, row, box),
            "candidate": candidate,
            "classification": "untyped_graph_retained",
            "physical_first_failure": failure,
            "failure_witness_sha256": canonical_digest(witness),
        })

    for ledger in (typed, excluded, nonphysical, untyped):
        ledger.sort(key=canonical_json)
    return {
        "audit_call_count": calls,
        "typed": typed,
        "excluded": excluded,
        "nonphysical": nonphysical,
        "untyped": untyped,
        "encountered_failure_counts": dict(sorted(failures.items())),
    }


def _type_graph_task(
    task: tuple[list[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    return type_one_graph(*task)


def build_result() -> dict[str, Any]:
    interval_wrapper = json.loads(INTERVAL_MANIFEST.read_text(encoding="utf-8"))
    assert interval_wrapper["verdict"]["cancellation_free_interval_frontier"] == "CERTIFIED"
    assert interval_wrapper["verdict"]["gate3"] == "NOT_CERTIFIED"
    rows, provenance = frozen.load_dependencies()
    exported = export_critical_graphs(rows)
    graphs = exported.pop("graphs")
    workers = min(
        int(os.environ.get("CM2_WORKERS", "32")), os.cpu_count() or 1, 64
    )
    tasks = [(rows, graph) for graph in graphs]
    with multiprocessing.get_context("fork").Pool(workers) as pool:
        parts = list(pool.imap_unordered(_type_graph_task, tasks, chunksize=1))
    typed = [leaf for part in parts for leaf in part["typed"]]
    excluded = [leaf for part in parts for leaf in part["excluded"]]
    nonphysical = [leaf for part in parts for leaf in part["nonphysical"]]
    untyped = [leaf for part in parts for leaf in part["untyped"]]
    for ledger in (typed, excluded, nonphysical, untyped):
        ledger.sort(key=canonical_json)
    failure_counts: Counter[str] = Counter()
    for part in parts:
        failure_counts.update(part["encountered_failure_counts"])
    assert len(typed) == 0
    assert len(excluded) == 840
    assert len(nonphysical) == 48
    assert len(untyped) == 0
    assert sum(part["audit_call_count"] for part in parts) == 888

    result = {
        "schema": "cm2.gate3.critical-graph-owner-typing-frontier.v1",
        "provenance": {
            "frozen_interval_manifest_sha256": file_sha256(INTERVAL_MANIFEST),
            "frozen_interval_certificate_sha256": file_sha256(
                Path(interval_frozen.__file__).resolve()
            ),
            "frozen_interval_internal_replay_digest": interval_wrapper["result"][
                "internal_replay_digest"
            ],
            "maximal_row_registry_sha256": provenance[
                "maximal_row_registry_sha256"
            ],
            "arithmetic_precision_bits": 384,
        },
        "critical_coordinate_export": exported,
        "critical_graph_owner_typing": {
            "input_graph_leaf_count": len(graphs),
            "typing_audit_call_count": sum(
                part["audit_call_count"] for part in parts
            ),
            "typed_graph_leaf_count": len(typed),
            "Delta_strict_excluded_descendant_count": len(excluded),
            "strict_nonphysical_time_graph_descendant_count": len(nonphysical),
            "untyped_graph_leaf_count": len(untyped),
            "encountered_failure_counts": dict(sorted(failure_counts.items())),
            "typed_graph_ledger_sha256": canonical_digest(typed),
            "Delta_excluded_ledger_sha256": canonical_digest(excluded),
            "strict_nonphysical_time_ledger_sha256": canonical_digest(nonphysical),
            "untyped_graph_ledger_sha256": canonical_digest(untyped),
            "all_888_conservative_graph_leaves_resolved_without_physical_future_face": True,
            "marked_current_TV_contribution_from_critical_graph_class": "0",
            "physical_FACE_2CUT_contribution_from_critical_graph_class": "0",
            "physical_FACE_TIME_contribution_from_critical_graph_class": "0",
        },
        "remaining_frontier": {
            "frozen_unexported_untyped_graph_count": 164,
            "critical_untyped_graph_count_after_this_audit": len(untyped),
            "combined_untyped_graph_count_upper": 164 + len(untyped),
            "safe_maximum_candidate_graph_charts_on_one_fixed_s_slice": 592,
            "safe_maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice": 51404,
            "safe_uniform_fixed_s_candidate_zero_set_Leb_Z_linear_coefficient": "1184",
            "safe_uniform_fixed_s_candidate_zero_set_row_law_Z_linear_coefficient": "149184/5",
            "partial_genuine_physical_marked_current_TV_upper_unchanged": "518152320",
            "complete_side_owner_current": False,
            "strong_DQ_MT_DQ_FACE": False,
            "gate3": False,
        },
        "exact_remaining_blockers": [
            "replay/export and type the 164 frozen untyped graph coordinates whose predecessor retained only SHA summaries",
            "assemble the complete current after the remaining 164 charts have unique physical-first owners or strict nonphysical exclusions",
            "prove common strong DQ/MT_DQ/FACE on the completed branch record",
        ],
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


if __name__ == "__main__":
    print(json.dumps(build_result(), sort_keys=True, indent=2))
