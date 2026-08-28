#!/usr/bin/env python3
"""Adapt the frozen C51 pair-1 probe data to a C50a owner request.

The adapter derives every reflected split child map from exact leaf geometry
and physical paths, checks it against the C51 representative split-axis
sequence, and emits two hash-chained replacement transactions.  It creates no
authority, seal, pointer, or D02 credit.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
from pathlib import Path
import sys
from typing import Any


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
DELIVERABLES = ROOT / "deliverables"

SCHEMA = "cm2.round306c50a.pair1-probe-to-owner-request-adapter.v1"
PRODUCER_NAME = "cm2_round306c50a_global_codimension_owner_oracle_v1"
C51_SOURCE = DELIVERABLES / "cm2_round306c51_d02a_pair1_two_task_route_probe_v1.py"
C51_REPORT = DELIVERABLES / "cm2_round306c51_d02a_pair1_two_task_route_probe_report_v1.md"
C51_SOURCE_SHA256 = "caf043d2a475f8c25e92785587db971a0d33242b8560dd096f09a1e5c6e72069"
C51_REPORT_SHA256 = "d2330ac69da6cdb0e3fa092c9b697c836a21026ebb52b9b3655f9487a88f6330"
C51_OBJECT_SHA256 = "187344a3c524dce1898151bf64f507c181dde137a3710eb9bc5cd1b895a81f6e"
TASK_BINDINGS = (
    "daada4d9fd48677629cbfa9872b073d5fdf1552b115bf94438e7357f9a5dd95b",
    "e37b527423ad1aabba7485faacd03f7bb95ba9d79caebd614fb63d38ccd8dac6",
)


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def load_producer() -> Any:
    sys.path.insert(0, str(DELIVERABLES))
    try:
        module = importlib.import_module(PRODUCER_NAME)
    finally:
        if sys.path and sys.path[0] == str(DELIVERABLES):
            sys.path.pop(0)
    need(Path(module.__file__).absolute() == DELIVERABLES / (PRODUCER_NAME + ".py"),
         "C50a producer import path")
    return module


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def common_prefix(values: list[str]) -> str:
    need(bool(values), "nonempty physical path group")
    prefix = values[0]
    for value in values[1:]:
        while not value.startswith(prefix):
            prefix = prefix[:-1]
    return prefix


def box_bound(p: Any, rows: list[dict[str, Any]]) -> tuple[Any, Any, Any, Any]:
    parsed = [p.exact_box(row["exact_closed_box"], "pair1 leaf box") for row in rows]
    return (min(row[0] for row in parsed), max(row[1] for row in parsed),
            min(row[2] for row in parsed), max(row[3] for row in parsed))


def inferred_decisions(p: Any, task_probe: dict[str, Any],
                       replacements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    frontier = task_probe["frontier_paths"]
    internal = p.prefixes(frontier)
    upstream = {row["relative_path"]: row for row in task_probe["split_events"]}
    need(set(upstream) == internal, "C51 split-prefix exhaustion")
    output = []
    for side in ("REPRESENTATIVE", "REFLECTED"):
        side_rows = [row for row in replacements if row["side"] == side]
        for parent in sorted(internal, key=lambda value: (len(value), value)):
            parent_rows = [row for row in side_rows if row["relative_path"].startswith(parent)]
            zero_rows = [row for row in parent_rows
                         if row["relative_path"].startswith(parent + "0")]
            one_rows = [row for row in parent_rows
                        if row["relative_path"].startswith(parent + "1")]
            need(bool(zero_rows) and bool(one_rows), "full pair1 split children")
            parent_physical = common_prefix([row["physical_route_path"] for row in parent_rows])
            zero_physical = common_prefix([row["physical_route_path"] for row in zero_rows])
            one_physical = common_prefix([row["physical_route_path"] for row in one_rows])
            need({zero_physical, one_physical} == {parent_physical + "0", parent_physical + "1"},
                 "pair1 physical binary children")
            zero_box, one_box = box_bound(p, zero_rows), box_bound(p, one_rows)
            axis = upstream[parent]["split_axis"]
            if axis == "t":
                need(zero_box[2:] == one_box[2:], "pair1 t transverse interval")
                if zero_box[1] == one_box[0]:
                    lower_logical, upper_logical = parent + "0", parent + "1"
                    lower_physical, upper_physical = zero_physical, one_physical
                    coordinate = zero_box[1]
                else:
                    need(one_box[1] == zero_box[0], "pair1 t adjacency")
                    lower_logical, upper_logical = parent + "1", parent + "0"
                    lower_physical, upper_physical = one_physical, zero_physical
                    coordinate = one_box[1]
            elif axis == "p":
                need(zero_box[:2] == one_box[:2], "pair1 p transverse interval")
                if zero_box[3] == one_box[2]:
                    lower_logical, upper_logical = parent + "0", parent + "1"
                    lower_physical, upper_physical = zero_physical, one_physical
                    coordinate = zero_box[3]
                else:
                    need(one_box[3] == zero_box[2], "pair1 p adjacency")
                    lower_logical, upper_logical = parent + "1", parent + "0"
                    lower_physical, upper_physical = one_physical, zero_physical
                    coordinate = one_box[3]
            else:
                raise Reject("pair1 in-slice split axis")
            output.append(p.split_decision(
                side, parent, parent_physical, axis, str(coordinate),
                lower_logical, lower_physical, upper_logical, upper_physical,
            ))
    output.sort(key=lambda row: (row["side"], row["logical_parent_prefix"]))
    return output


def transaction(p: Any, task_probe: dict[str, Any], ambient: dict[str, Any],
                index: int, parent_head: str) -> dict[str, Any]:
    frontier = task_probe["frontier_paths"]
    split_evidence_sequence = p.sequence_digest(
        row["split_object_sha256"] for row in task_probe["split_events"])
    replacements = []
    for logical in task_probe["dual_side_terminal_rows"]:
        need(logical["relative_path"] in frontier, "terminal row frontier key")
        for leaf in logical["physical_sides"]:
            need(leaf["relative_path"] == logical["relative_path"]
                 and leaf["formal_credit"] == 0, "pair1 leaf key/credit")
            evidence = {
                "source_schema": task_probe["schema"],
                "source_task_probe_object_sha256": task_probe["task_probe_object_sha256"],
                "source_split_event_sequence_sha256": split_evidence_sequence,
                "source_physical_leaf_id": leaf["physical_leaf_id"],
                "source_leaf_object_sha256": leaf["leaf_object_sha256"],
                "source_compact_leaf_row_sha256": p.digest(leaf),
                "terminal_classification": leaf["terminal_classification"],
                "all_required_strict_margins_complete": leaf[
                    "all_required_strict_margins_complete"],
                "formal_credit": 0,
            }
            replacements.append({
                "side": leaf["side"], "relative_path": leaf["relative_path"],
                "semantic_path": task_probe["root_path"] + leaf["relative_path"],
                "physical_route_path": leaf["physical_route_path"],
                "physical_cell_id": leaf["physical_cell_id"],
                "exact_closed_box": leaf["exact_closed_box"],
                "relative_parent_fraction": str(p.F(1, 2 ** len(leaf["relative_path"]))),
                "source_evidence": evidence,
            })
    replacements.sort(key=lambda row: (row["side"], row["relative_path"]))
    decisions = inferred_decisions(p, task_probe, replacements)
    task_body = {
        "task_id": task_probe["task_id"],
        "upstream_task_binding_sha256": task_probe["task_binding_sha256"],
        "pair_index": 1, "root_semantic_path": task_probe["root_path"],
        "predecessors": [{
            "side": side, "locator_kind": "C41_AMBIENT_SIDE",
            "upstream_ambient_cell_id": task_probe["ambient_cell_id"],
            "upstream_ambient_row_sha256": ambient["row_sha256"],
        } for side in ("REPRESENTATIVE", "REFLECTED")],
    }
    task = {**task_body, "oracle_task_binding_sha256": p.digest(task_body)}
    body = {
        "transaction_index": index, "parent_history_sha256": parent_head,
        "task": task, "relative_frontier": frontier,
        "split_decisions": decisions, "replacements": replacements,
    }
    return {**body, "transaction_binding_sha256": p.digest(body)}


def request_body(p: Any, transactions: list[dict[str, Any]]) -> dict[str, Any]:
    body = {
        "schema": p.REQUEST_SCHEMA, "protocol_versions": p.PROTOCOLS,
        "active_universe": p.ACTIVE_UNIVERSE,
        "active_universe_binding_sha256": p.ACTIVE_UNIVERSE_SHA256,
        "history_genesis": p.GENESIS_BODY,
        "history_genesis_sha256": p.GENESIS_SHA256,
        "transactions": transactions,
        "target_mode": "ALL_ACTIVE_HISTORY_REPLACEMENTS",
        "target_transaction_indices": [],
        "request_purpose": "PAIR1_TWO_TASK_NINE_LOGICAL_EIGHTEEN_PHYSICAL_OWNER_REPLAY__ZERO_CREDIT",
        "formal_credit": 0,
    }
    return {**body, "request_object_sha256": p.digest(body)}


def build(probe_path: Path) -> dict[str, Any]:
    p = load_producer()
    need(file_hash(C51_SOURCE) == C51_SOURCE_SHA256, "C51 source pin")
    need(file_hash(C51_REPORT) == C51_REPORT_SHA256, "C51 report pin")
    raw = p.stable_read(probe_path.absolute(), "C51 pair1 probe result")
    probe = p.json_value(raw, "C51 pair1 probe result", canonical_line=True)
    p.closed(probe, "object_sha256", "C51 pair1 probe result")
    need(probe["object_sha256"] == C51_OBJECT_SHA256
         and probe["status"] == "PASS_PAIR1_TWO_TASK_DUAL_SIDE_STRICT_ROUTE_FRONTIERS_ZERO_CREDIT",
         "C51 pair1 probe object/status pin")
    tasks = probe["task_probes"]
    need(tuple(row["task_binding_sha256"] for row in tasks) == TASK_BINDINGS,
         "exact pair1 task ordering")
    need(sum(row["frontier_leaf_count"] for row in tasks) == 9
         and sum(2 * row["frontier_leaf_count"] for row in tasks) == 18,
         "pair1 nine-logical/eighteen-physical census")
    baseline, ambient_index, _replay = p.load_active_universe()
    tx0 = transaction(p, tasks[0], ambient_index[tasks[0]["ambient_cell_id"]],
                      0, p.GENESIS_SHA256)
    provisional = request_body(p, [tx0])
    provisional["target_mode"] = "TRANSACTION_INSERTIONS_STILL_ACTIVE"
    provisional["target_transaction_indices"] = [0]
    provisional_body = {key: value for key, value in provisional.items()
                        if key != "request_object_sha256"}
    provisional["request_object_sha256"] = p.digest(provisional_body)
    p.request_check(provisional)
    _overlay, _nodes, _targets, head0 = p.apply_history(provisional, baseline)
    tx1 = transaction(p, tasks[1], ambient_index[tasks[1]["ambient_cell_id"]],
                      1, head0)
    request = request_body(p, [tx0, tx1])
    p.request_check(request)
    return request


def emit(p: Any, value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(p.canonical(value) + b"\n")
    sys.stdout.buffer.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe-result", type=Path, required=True)
    args = parser.parse_args(argv)
    p = load_producer()
    try:
        emit(p, build(args.probe_result))
        return 0
    except (Reject, p.Reject, OSError, ValueError, KeyError, TypeError,
            StopIteration) as error:
        body = {"schema": SCHEMA + ".fail-closed", "status": "REJECTED",
                "error_class": type(error).__name__, "reason": str(error),
                "runtime_writes_performed": False, "formal_credit": 0}
        emit(p, {**body, "object_sha256": p.digest(body)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
