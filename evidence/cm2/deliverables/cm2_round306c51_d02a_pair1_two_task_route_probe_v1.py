#!/usr/bin/env python3
"""Read-only dual-side adaptive route probe for the two pair-1 D02-A tasks.

This is a zero-credit feasibility object.  It reconstructs the frozen C46
queue, selects the complete two-row ``DIRECT_WHOLE_PAIR`` group for pair 1,
and uses the frozen C41 route/split primitives.  A leaf is marked locally
closed only when the C48 two-side routine independently routes both physical
sides and reproduces every strict terminal margin.  No codimension-owner
claim, checkpoint successor, pointer, seal, canonical update, or D02 credit is
created here.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction as Q
import hashlib
import importlib
import json
from pathlib import Path
import sys
from typing import Any


SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
sys.dont_write_bytecode = True

SCHEMA = "cm2.round306c51.d02-a-pair1-two-task-route-probe.v1"
C41_TOKEN = "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C41_OBJECT_SHA256 = "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
C46_PLAN_OBJECT_SHA256 = "7d004f59282dee21a28db0cd0b727a9045f4befce207c96be4efb07d1399c9bf"
C47_SOURCE_SHA256 = "28c7eb805729f4ab8d5adaf5fac211394616877b5e08c39bd9f288c1f7640a1f"
C48_SOURCE_SHA256 = "a16d8802288c021d6d153942df15c7e7f0078628f5fb2c29eb927c6e9b94a7b8"
PAIR = 1
EXPECTED_TASKS = (
    (
        "daada4d9fd48677629cbfa9872b073d5fdf1552b115bf94438e7357f9a5dd95b",
        "111111110",
        "c41-ambient:1610ea6d1bc40ef5eed6614db0e25e77ba374850efaec77964a50520b77c1b09",
        "c41-c2-outer:d3762e8c71c9bbb8bd9863d3d47c2a92b380ba5f3ca776509d7cdb2da820ca54",
    ),
    (
        "e37b527423ad1aabba7485faacd03f7bb95ba9d79caebd614fb63d38ccd8dac6",
        "111111111",
        "c41-ambient:bb566b646775f7e2599e0277e84cdfe1e2222371d9c6ccfc5d50a42ec9c663db",
        "c41-c2-outer:f74b3ca3b825776480ebc1ed9f210bcd710ca29dd59c7e7700590c8092d4aaf7",
    ),
)


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def prefix_free(paths: list[str]) -> bool:
    return len(paths) == len(set(paths)) and not any(
        right.startswith(left)
        for left in paths for right in paths if left != right
    )


def load_modules() -> tuple[Any, Any, Any, Any]:
    c47_path = DELIVERABLES / (
        "cm2_round306c47_d02a_pair668_exact_route_adaptive_feasibility_spike_v1.py"
    )
    c48_path = DELIVERABLES / (
        "cm2_round306c48_d02a_pair668_two_side_owner_closure_v1.py"
    )
    need(file_sha(c47_path) == C47_SOURCE_SHA256, "frozen C47 source")
    need(file_sha(c48_path) == C48_SOURCE_SHA256, "frozen C48 source")
    sys.path.insert(0, str(DELIVERABLES))
    try:
        c47 = importlib.import_module(c47_path.stem)
        c48 = importlib.import_module(c48_path.stem)
        c46, c41 = c47.load_frozen_modules()
    finally:
        if sys.path and sys.path[0] == str(DELIVERABLES):
            sys.path.pop(0)
    return c46, c41, c47, c48


def frozen_pair_inputs(c46: Any, c41: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    plan, tasks, _shards = c46.build_read_only_plan(64)
    need(plan["plan_object_sha256"] == C46_PLAN_OBJECT_SHA256, "C46 plan pin")
    selected = sorted(
        [row for row in tasks if row["pair_index"] == PAIR
         and row["queue"]["priority_class"] == "DIRECT_WHOLE_PAIR"],
        key=lambda row: (row["descendant_path"], row["primary_outer_id"]),
    )
    observed = tuple((
        row["task_binding_sha256"], row["descendant_path"],
        row["ambient_cell_id"], row["primary_outer_id"],
    ) for row in selected)
    need(observed == EXPECTED_TASKS, "exact frozen pair-1 two-task group")

    c41_dir = RUNTIME / "candidates" / C41_TOKEN
    result = c41.strict_json(c41_dir / "result.json")
    c41.validate_object(result, C41_OBJECT_SHA256, "C41 candidate")
    wanted = {row["ambient_cell_id"] for row in selected}
    ambient_by_id: dict[str, dict[str, Any]] = {}
    for row in c41.iter_ledger(c41_dir, result["ledgers"]["routed_ambient_cells"]):
        if row["c41_ambient_cell_id"] in wanted:
            need(row["c41_ambient_cell_id"] not in ambient_by_id,
                 "selected ambient uniqueness")
            ambient_by_id[row["c41_ambient_cell_id"]] = row
    need(set(ambient_by_id) == wanted, "both selected ambient rows present")

    c40_dir = ROOT / result["C40_authority"]["path"]
    c40_audit = ROOT / result["C40_authority"]["independent_audit_path"]
    c40_result = c41.strict_json(c40_dir / "result.json")
    wanted_sources = {
        ambient_by_id[row["ambient_cell_id"]]["c40_source_leaf_id"]
        for row in selected
    }
    source_by_id: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(c41.iter_ledger(
            c40_dir, c40_result["ledgers"]["routed_leaf_cells"])):
        if row["c40_leaf_id"] in wanted_sources:
            need(row["c40_leaf_id"] not in source_by_id,
                 "selected C40 source uniqueness")
            source_by_id[row["c40_leaf_id"]] = (ordinal, row)
    need(set(source_by_id) == wanted_sources, "both C40 source rows present")
    context = c41.load_context(c40_dir, c40_audit, formal=True)
    config = c41.decode_worker_config(context["config"])

    frozen_rows = []
    for selected_row in selected:
        ambient = ambient_by_id[selected_row["ambient_cell_id"]]
        need(
            ambient["row_sha256"] == selected_row["ambient_row_sha256"]
            and ambient["pair_index"] == PAIR
            and ambient["path"] == selected_row["descendant_path"],
            "task/ambient binding",
        )
        ordinal, source = source_by_id[ambient["c40_source_leaf_id"]]
        task = c41.task_for_row(ordinal, source, context)
        frozen_rows.append({
            "plan": plan, "selected": selected_row, "ambient": ambient,
            "source": source, "source_ordinal": ordinal,
            "context": context, "config": config, "task": task,
        })
    return plan, frozen_rows


def compact_leaf(leaf: dict[str, Any]) -> dict[str, Any]:
    margin = leaf["terminal_margin_certificate"]
    return {
        "side": leaf["side"],
        "relative_path": leaf["relative_path"],
        "physical_route_path": leaf["physical_route_path"],
        "physical_cell_id": leaf["physical_cell_id"],
        "exact_closed_box": leaf["exact_closed_box"],
        "terminal_classification": leaf["terminal_classification"],
        "selected_absolute_owner": margin["collision2"]["selected_absolute_owner"],
        "unscreened_active_competitor_count": margin["collision2"]
        ["unscreened_active_competitor_count"],
        "all_required_strict_margins_complete": margin[
            "all_required_strict_margins_complete"
        ],
        "physical_leaf_id": leaf["physical_leaf_id"],
        "leaf_object_sha256": digest(leaf),
        "formal_credit": 0,
    }


def strict_physical_leaf(
    c41: Any, c48: Any, frozen: dict[str, Any], side: str, relative: str,
) -> dict[str, Any]:
    """Recompute either C40-C2 or C39-downstream C2 strict exclusion.

    C48's narrow helper accepts only leaves that first reach C2 through the
    C40 ``collision2_safe`` branch.  Pair 1 also has leaves whose C39 W-side
    downstream route already returns an exclusion.  For those leaves this
    probe deliberately reruns the same exact dynamic C2 classifier and then
    applies C48's complete margin reconstruction; an upstream exclusion label
    alone is never accepted.
    """
    try:
        return c48.route_leaf(c41, frozen, side, relative)[0]
    except c48.Rejected as original_error:
        semantic_path = c48.ROOT_PATH + relative
        task, cell, origin, physical_path = c48.physical_task(
            c41, frozen, side, semantic_path
        )
        route = c41.c39.route_c1_task(task, frozen["config"])
        need(
            route["classification"]
            == "EXCLUDED_C39_C1_ENHANCED_W_SIDE_COLLISION2_OWNER_MISMATCH",
            "fallback is exact C39 W-side collision2 owner mismatch:"
            + str(original_error),
        )
        box, _active = c41.c39.reconstruct_box(cell, physical_path)
        c2_status, c2_detail, c2_evidence, c2_baseline = (
            c41.round185.resolve_dynamic_box(
                origin, box, frozen["config"]["pair_index"],
                frozen["config"]["pattern_index"],
            )
        )
        need(c2_status.startswith("LOCAL_EXACT_KEY"),
             "fallback exact C2 local key; observed=" + str(c2_status))
        exact_classification, exact_witness = c41.c40.expected_collision2(
            c2_detail, frozen["config"]
        )
        need(exact_classification == "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH",
             "fallback exact C2 owner mismatch")
        expected_owners = sorted({
            frozen["config"]["original_path"][1]["selected_absolute_owner_id"],
            frozen["config"]["reflected_path"][1]["selected_absolute_owner_id"],
        })
        margin = c48.terminal_margin(
            c41, cell, origin, box, route, c2_detail, expected_owners
        )
        need(margin["all_required_strict_margins_complete"],
             "fallback C39/C2 strict terminal margin complete")
        body = {
            "schema": SCHEMA + ".physical-leaf",
            "side": side,
            "pair_index": PAIR,
            "task_binding_sha256": frozen["selected"]["task_binding_sha256"],
            "relative_path": relative,
            "semantic_path": semantic_path,
            "physical_route_path": physical_path,
            "physical_cell_id": cell["cell_id"],
            "physical_origin_key": origin,
            "exact_closed_box": c48.payload_box(
                c41, c48.compact_chart(cell), box
            ),
            "relative_parent_fraction": str(Q(1, 2 ** len(relative))),
            "C1_route_result": route,
            "C1_route_result_sha256": digest(route),
            "C2_status": c2_status,
            "C2_baseline": c2_baseline,
            "C2_detail": c2_detail,
            "C2_detail_sha256": digest(c2_detail),
            "C2_evidence": c2_evidence,
            "terminal_classification": exact_classification,
            "upstream_terminal_classification": route["classification"],
            "terminal_witness": exact_witness,
            "terminal_margin_certificate": margin,
            "terminal_candidate_closed": True,
            "formal_credit": 0,
        }
        return {**body, "physical_leaf_id": "c51-leaf:" + digest(body)}


def probe_task(c41: Any, c48: Any, frozen: dict[str, Any], budget: int) -> dict[str, Any]:
    selected = frozen["selected"]
    root = selected["descendant_path"]
    source_path = frozen["source"]["path"]
    c48.PAIR = PAIR
    c48.TASK_BINDING = selected["task_binding_sha256"]
    c48.ROOT_PATH = root
    c48.AMBIENT_ID = selected["ambient_cell_id"]

    frontier = [""]
    terminal: dict[str, list[dict[str, Any]]] = {}
    observations: dict[str, dict[str, Any]] = {}
    splits: list[dict[str, Any]] = []
    while len(splits) < budget:
        split_path = None
        split_route = None
        for relative in sorted(frontier):
            if relative in terminal:
                continue
            absolute = root + relative
            route = c41.route_at_path(frozen["task"], absolute, frozen["config"])
            observation = {
                "relative_path": relative,
                "absolute_path": absolute,
                "classification": route["classification"],
                "disposition_family": c41.disposition_family(route["classification"]),
                "route_method": route["route_method"],
                "C2_status": route["c2_status"],
                "C2_detail_sha256": (
                    digest(route["c2_detail"]) if route["c2_detail"] is not None
                    else None
                ),
            }
            try:
                leaves = [strict_physical_leaf(
                    c41, c48, frozen, side, relative
                ) for side in ("REPRESENTATIVE", "REFLECTED")]
                terminal[relative] = [compact_leaf(row) for row in leaves]
                observation["dual_side_strict_terminal"] = True
                observation["strict_terminal_failure"] = None
            except (Exception,) as exc:
                observation["dual_side_strict_terminal"] = False
                observation["strict_terminal_failure"] = (
                    type(exc).__name__ + ":" + str(exc)
                )
            observations[relative] = observation
            if relative not in terminal:
                split_path, split_route = relative, route
                break
        if split_path is None:
            break
        absolute = root + split_path
        bits = absolute[len(source_path):]
        history = c41.exact_axis_history(frozen["task"], bits)
        adjacency, children, axis = c41.split_row(
            frozen["task"], split_route["box"], bits, len(bits), history
        )
        for bit in ("0", "1"):
            child = c41.route_at_path(
                frozen["task"], absolute + bit, frozen["config"]
            )
            need(
                c41.box_payload(child["box"])
                == c41.box_payload(children[int(bit)]),
                "fresh child equals exact split child",
            )
        split_body = {
            "relative_path": split_path,
            "absolute_path": absolute,
            "split_axis": ("t", "p", "s")[axis],
            "C41_split_face_adjacency_sha256": digest(adjacency),
            "formal_credit": 0,
        }
        splits.append({**split_body, "split_object_sha256": digest(split_body)})
        frontier.remove(split_path)
        frontier.extend([split_path + "0", split_path + "1"])
        frontier.sort()

    for relative in sorted(frontier):
        if relative in observations:
            continue
        absolute = root + relative
        route = c41.route_at_path(frozen["task"], absolute, frozen["config"])
        observations[relative] = {
            "relative_path": relative,
            "absolute_path": absolute,
            "classification": route["classification"],
            "disposition_family": c41.disposition_family(route["classification"]),
            "route_method": route["route_method"],
            "C2_status": route["c2_status"],
            "C2_detail_sha256": (
                digest(route["c2_detail"]) if route["c2_detail"] is not None
                else None
            ),
            "dual_side_strict_terminal": False,
            "strict_terminal_failure": "NOT_EVALUATED_AFTER_RESOURCE_BUDGET",
        }

    paths = sorted(frontier)
    kraft = sum((Q(1, 2 ** len(path)) for path in paths), Q(0))
    need(prefix_free(paths) and kraft == 1, "prefix-free exact Kraft frontier")
    all_closed = set(paths) == set(terminal)
    body = {
        "schema": SCHEMA + ".task-probe",
        "task_id": selected["task_id"],
        "task_binding_sha256": selected["task_binding_sha256"],
        "pair_index": PAIR,
        "root_path": root,
        "ambient_cell_id": selected["ambient_cell_id"],
        "primary_outer_id": selected["primary_outer_id"],
        "event_budget": budget,
        "split_count": len(splits),
        "split_events": splits,
        "frontier_paths": paths,
        "frontier_leaf_count": len(paths),
        "relative_Kraft_sum": str(kraft),
        "prefix_free": True,
        "dual_side_strict_terminal_paths": sorted(terminal),
        "dual_side_strict_terminal_count": len(terminal),
        "dual_side_terminal_rows": [
            {"relative_path": path, "physical_sides": terminal[path]}
            for path in sorted(terminal)
        ],
        "observations": [observations[path] for path in sorted(
            observations, key=lambda value: (len(value), value)
        )],
        "all_frontier_leaves_dual_side_strict_terminal": all_closed,
        "candidate_route_closure_only": all_closed,
        "global_codimension_owner_oracle_applied": False,
        "candidate_or_authority_created": False,
        "formal_credit": 0,
        "D02_gate_credit": 0,
    }
    return {**body, "task_probe_object_sha256": digest(body)}


def run_probe(budget: int) -> dict[str, Any]:
    need(type(budget) is int and 1 <= budget <= 256, "event budget in [1,256]")
    c46, c41, _c47, c48 = load_modules()
    plan, frozen_rows = frozen_pair_inputs(c46, c41)
    probes = [probe_task(c41, c48, frozen, budget) for frozen in frozen_rows]
    all_closed = all(row["all_frontier_leaves_dual_side_strict_terminal"]
                     for row in probes)
    body = {
        "schema": SCHEMA,
        "status": (
            "PASS_PAIR1_TWO_TASK_DUAL_SIDE_STRICT_ROUTE_FRONTIERS_ZERO_CREDIT"
            if all_closed else
            "PASS_PAIR1_PROBE_INCOMPLETE_FRONTIERS_REMAIN_ZERO_CREDIT"
        ),
        "source_sha256": file_sha(SELF),
        "C46_plan_object_sha256": plan["plan_object_sha256"],
        "pair_index": PAIR,
        "task_count": len(probes),
        "task_probes": probes,
        "both_tasks_route_closed": all_closed,
        "prefix_free_and_Kraft_one_for_both_tasks": all(
            row["prefix_free"] and row["relative_Kraft_sum"] == "1"
            for row in probes
        ),
        "full_global_codimension_owner_ledger_pending": True,
        "independent_no_producer_import_verifier_pending": True,
        "no_replace_seal_pending": True,
        "coarse_formal_authority_unchanged": {
            "paired_coarse_cells": 574,
            "unresolved_coarse_cells": 1150,
            "representative_parents_remaining": 575,
        },
        "runtime_writes_performed": False,
        "formal_credit": 0,
        "D02_gate_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**body, "object_sha256": digest(body)}


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", action="store_true", required=True)
    parser.add_argument("--event-budget", type=int, default=16)
    args = parser.parse_args()
    try:
        emit(run_probe(args.event_budget))
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            RuntimeError, AssertionError) as exc:
        body = {
            "schema": SCHEMA + ".rejection",
            "status": "REJECTED_FAIL_CLOSED",
            "reason": type(exc).__name__ + ":" + str(exc),
            "runtime_writes_performed": False,
            "formal_credit": 0,
            "D02_gate_credit": 0,
        }
        emit({**body, "object_sha256": digest(body)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
