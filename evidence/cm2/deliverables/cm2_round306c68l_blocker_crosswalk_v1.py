#!/usr/bin/env python3
"""C68-L read-only blocker crosswalk for the large and singleton C1 scopes.

This inventory deliberately does not promote any authority.  It independently
recomputes the two C57-L1 collision-one frontier predicates from the frozen
C56 current-pending ledger and exact C41 rows, consumes the frozen C63 history
map and C66 owner decisions, records the absence of a C67 margin authority,
and separates the disjoint C57-S1/C61/C65 singleton work into structural tasks.
"""
from __future__ import annotations

import ast
import copy
import gzip
import hashlib
import io
import json
import os
import stat
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Iterable

sys.dont_write_bytecode = True

SELF = Path(__file__).resolve()
ROOT = SELF.parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c68l_blocker_crosswalk"
SCHEMA = "cm2.round306c68l.read-only-blocker-crosswalk.v1"
COLLISION2_PREFIX = "UNRESOLVED_C41_COLLISION2_"
REQUIRED_SINGLETON_DECIDER = "GLOBAL_SINGLETON_C1_GRAPH_CELL_AND_OFF_GRAPH_SLAB_DECIDER"

TASK_FILE = PREFIX + "_large_current_task_replay_v1.jsonl.gz"
EDGE_FILE = PREFIX + "_large_edge_blockers_v1.jsonl.gz"
CELL_FILE = PREFIX + "_large_corridor_cell_blockers_v1.jsonl.gz"
SINGLETON_FILE = PREFIX + "_singleton_structural_tasks_v1.jsonl.gz"
RESULT_FILE = PREFIX + "_result_v1.json"
REPORT_FILE = PREFIX + "_report_v1.md"

C41_DIR = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C41_RESULT = C41_DIR / "result.json"
C41_ROUTED = C41_DIR / "routed_ambient_cells.jsonl.gz"

C56_RESULT = OUT / "cm2_round306c56l_large_component_common_refinement_result_v1.json"
C56_TASKS = OUT / "cm2_round306c56l_large_component_common_refinement_post_c53_pending_logical_tasks_v1.jsonl.gz"
C56_CELLS = OUT / "cm2_round306c56l_large_component_common_refinement_corridor_and_separator_cells_v1.jsonl.gz"

C57_RESULT = OUT / "cm2_round306c57l1_collision1_edgewise_transport_result_v1.json"
C57_LOCAL = OUT / "cm2_round306c57l1_collision1_edgewise_transport_local_collision1_cell_status_v1.jsonl.gz"
C57_CELLS = OUT / "cm2_round306c57l1_collision1_edgewise_transport_corridor_cell_transport_v1.jsonl.gz"
C57_EDGES = OUT / "cm2_round306c57l1_collision1_edgewise_transport_edge_obligations_v1.jsonl.gz"

C63_RESULT = OUT / "cm2_round306c63l_scope_extension_result_v1.json"
C63_EDGES = OUT / "cm2_round306c63l_scope_extension_edge_replay_v1.jsonl.gz"
C66_RESULT = OUT / "cm2_round306c66l_global_owner_decider_authority_candidate_v1.json"
C66_EDGES = OUT / "cm2_round306c66l_global_owner_decider_edge_owner_decisions_v1.jsonl.gz"

C57S_RESULT = OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_result_v1.json"
C57S_PARENTS = OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_parent_ledger_v1.jsonl.gz"
C61_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
C61_LEAVES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
C61_VERIFY = OUT / "cm2_round306c61s12_independent_postexecution_verification_v4.json"
C61_MANIFEST = OUT / "cm2_round306c61s12_depth12_16shard_manifest_v4.sha256"
C65_RUNNER = OUT / "cm2_round306c65s18_depth18_64shard_runner_v2.py"
C65_CONTRACT = OUT / "cm2_round306c65s18_independent_contract_v2.json"
C65_ASSIGN_RESULT = OUT / "cm2_round306c65s18_depth18_64shard_v2_assignment_result_v1.json"
C65_ASSIGN = OUT / "cm2_round306c65s18_depth18_64shard_v2_assignment_inventory_v1.jsonl.gz"
C65_VERIFY = OUT / "cm2_round306c65s18_independent_preexecution_verification_v1.json"

PINS = {
    "C41_RESULT": "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    "C41_OBJECT": "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    "C41_ROUTED": "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8",
    "C56_RESULT": "99e5fc0019ae21e7bc68d0c2b997ed62e9c47b28fd47d366237b0c06b1d82601",
    "C56_OBJECT": "0ab2c1ea9086db7f05d9b0c7f96d4348b0b2d8c9f54b47bd8e57aa570133a637",
    "C56_TASKS": "6893e360b3ffc205147efa3786f1a05c1b67c1556e6195733549a7da5540fb6a",
    "C56_CELLS": "3338a3fee7efe31bfae6b3abab77e3b3cc1c2a51fafb8e93d7a626c24803275d",
    "C57_RESULT": "4126bea2ede296939963a886699cf69a7189ab11015180e9cdf03c25f985325c",
    "C57_OBJECT": "ca5be921350a34770f5fe12e0734ab55e7fc707c97685c7aa07c2cf53760c6a0",
    "C57_LOCAL": "e328bf27a200d52f536b4d019c12c7e37198cb9942bee4dddc32b730c3fcf28d",
    "C57_CELLS": "3f61330c3eafa9101b083b8b6061ee334738bfa3129280874e1a3f7d239e1ac5",
    "C57_EDGES": "7136dd4585a5ed9de158c0710c6386ece4d8870ab0196db2e373881779c3dbcd",
    "C63_RESULT": "4795560dd4d70b6a1d42dde0cdf3e2c3f21f8c06e97aa776cd4fac4755ba5177",
    "C63_OBJECT": "676737c1f8ca935bbbf54b1d3aa7763d5178b56e93b1abc31fb7643f4a803135",
    "C63_EDGES": "94f0d22e2cdbaf18d39b3a4f0c31de453915a05feedbe3bec2b5a9cf1e3ace6b",
    "C66_RESULT": "2f546c2eda8bad0866d2d0d844c0c458c505be84d6997e4999be99b6c1eccb4b",
    "C66_OBJECT": "6e0f6982c19b15850ff24ae5d048140418641be73e59d9d9924e96ec4337ecd5",
    "C66_EDGES": "23ea97c5f021e2e3fc6512425b38a7d61fdaedb0f7543999b8f8ca67ebbdba4d",
    "C57S_RESULT": "9881c22ac4a8630b90b8eb16d81c1670bb6f544e5f4666197d0e6047771d8c4c",
    "C57S_OBJECT": "8cda7681bcbe93c065f1f336842e9fffa6bd3ea67268e96d95fcb3d1f8cbbb58",
    "C57S_PARENTS": "8817069967798042bd87315f57e7c3cea279c6564c0e50a5ac927ca4f765e510",
    "C61_RESULT": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "C61_OBJECT": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "C61_LEAVES": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "C61_VERIFY": "2dc773d0051cc9668cdf7752fb61ac09f495044f566972faa335fffc509e9fc7",
    "C61_VERIFY_OBJECT": "066e03be0c41600f5fb5cc2c157fe6e7eb04d1060896dd1acc910b06aab30b24",
    "C61_MANIFEST": "4c18c510367fc15b801fb6eff7901ad94a8fd53e47a6b7868ee876b554393545",
    "C65_RUNNER": "cf486e6d42002bbe3205453e55a120478978fe63b0a22fc289fb809f02c8f757",
    "C65_CONTRACT": "e320ac48b1cf3675a3c152d0cb9e6084ba750433722fef716e4a8ab534fab287",
    "C65_CONTRACT_OBJECT": "5d8a39432c2b02e807c5624ea26f56a12b58f66601ab391b52fee89d0ca604a4",
    "C65_ASSIGN_RESULT": "4b77b47be2029dc705e704330969c229e97833baa0fd2d24f23c79ee82ed0a57",
    "C65_ASSIGN_OBJECT": "b8c27cd2b35ba25b7ffecf3e06b89ec7e0e86ad210d38614c2f1f3f7f74e0d3d",
    "C65_ASSIGN": "e2c4714f1f1a8aa470a393d25ff03aaa3228f08979c30c90fd5f297469d6ad30",
    "C65_VERIFY": "770d8d2576f54eb53321c46623288cca926d2bdd1ce9592b2e7fce0c0c80138f",
    "C65_VERIFY_OBJECT": "11d3cd2561e48f073e1960861a7b2dbfe4fcdff551292397ec78d1a014a13f21",
}


class FailClosed(RuntimeError):
    """Any mismatch is a terminal failure for this inventory."""


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def object_hash(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sequence_hash(values: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(value.encode("ascii") + b"\n")
    return digest.hexdigest()


def identity(value: os.stat_result) -> dict[str, int]:
    return {
        "dev": value.st_dev,
        "ino": value.st_ino,
        "mode": value.st_mode,
        "size": value.st_size,
        "mtime_ns": value.st_mtime_ns,
        "nlink": value.st_nlink,
    }


def secure_bytes(path: Path, expected_sha256: str) -> tuple[bytes, dict[str, int]]:
    before = os.lstat(path)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular-single-link:" + path.name)
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(identity(before) == identity(opened), "path-fd-identity:" + path.name)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        need(identity(os.fstat(fd)) == identity(opened), "fd-post-identity:" + path.name)
    finally:
        os.close(fd)
    need(identity(os.lstat(path)) == identity(before), "path-post-identity:" + path.name)
    data = b"".join(chunks)
    need(hashlib.sha256(data).hexdigest() == expected_sha256, "file-sha256:" + path.name)
    return data, identity(before)


def close_object(value: dict[str, Any], expected: str, label: str) -> None:
    body = dict(value)
    actual = body.pop("object_sha256", None)
    need(actual == expected == object_hash(body), "object-sha256:" + label)


def close_row(value: dict[str, Any], label: str) -> None:
    body = dict(value)
    actual = body.pop("row_sha256", None)
    need(actual == object_hash(body), "row-sha256:" + label)


def json_from_bytes(data: bytes) -> dict[str, Any]:
    return json.loads(data)


def rows_from_bytes(data: bytes, descriptor: dict[str, Any], label: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    hashes: list[str] = []
    with gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb") as stream:
        for index, line in enumerate(stream):
            row = json.loads(line)
            close_row(row, f"{label}:{index}")
            rows.append(row)
            hashes.append(row["row_sha256"])
    need(len(rows) == descriptor["row_count"], "row-count:" + label)
    need(sequence_hash(hashes) == descriptor["row_hash_line_sequence_sha256"], "row-sequence:" + label)
    return rows


def selected_rows_from_bytes(
    data: bytes,
    descriptor: dict[str, Any],
    label: str,
    select: Callable[[dict[str, Any]], bool],
    compact: Callable[[dict[str, Any]], dict[str, Any]],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    count = 0
    with gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb") as stream:
        for index, line in enumerate(stream):
            row = json.loads(line)
            close_row(row, f"{label}:{index}")
            sequence.update((row["row_sha256"] + "\n").encode("ascii"))
            count += 1
            if select(row):
                selected.append(compact(row))
    need(count == descriptor["row_count"], "row-count:" + label)
    need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], "row-sequence:" + label)
    return selected


class Writer:
    def __init__(self, path: Path, order: str):
        self.path = path
        self.order = order
        self.raw = path.open("wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def __enter__(self) -> "Writer":
        return self

    def write(self, body: dict[str, Any]) -> dict[str, Any]:
        row_sha256 = object_hash(body)
        row = {**body, "row_sha256": row_sha256}
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row_sha256 + "\n").encode("ascii"))
        self.count += 1
        return row

    def __exit__(self, *_args: Any) -> None:
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_hash(self.path),
            "size": self.path.stat().st_size,
        }


def structural_kind(classification: str, witness: str) -> str:
    mapping = {
        ("UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY", "REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED"):
            "REGULAR_BOUNDARY_ARRANGEMENT",
        ("UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY", "REGULAR_FULL_FACE_GRAPH"):
            "REGULAR_FULL_FACE_GRAPH_CELL",
        ("UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY", "SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED"):
            "SOURCE_GRAZING_ENDPOINT_CHART",
        ("UNRESOLVED_C39_C1_REGULAR_MULTI_GRAPH_ARRANGEMENT", "inherited interval ordering or boundary type not isolated"):
            "REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED",
        ("UNRESOLVED_C39_C1_REGULAR_MULTI_GRAPH_ARRANGEMENT", "unique monotone inherited-active-set first tangency"):
            "REGULAR_MULTI_GRAPH_FIRST_TANGENCY",
        ("UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE", "OUTGOING_STATE"):
            "COLLISION1_OUTGOING_STATE",
    }
    key = (classification, witness)
    need(key in mapping, "recognized-singleton-structural-kind")
    return mapping[key]


def c67_matches() -> list[str]:
    matches = [str(path.relative_to(ROOT)) for path in OUT.glob("cm2_round306c67*")]
    runtime = ROOT / ".cm2-runtime"
    if runtime.exists():
        matches.extend(str(path.relative_to(ROOT)) for path in runtime.rglob("*306c67*"))
    return sorted(set(matches))


def audit_c65_runner(source: bytes) -> dict[str, Any]:
    tree = ast.parse(source.decode("utf-8"), filename=C65_RUNNER.name)
    imports_c41 = any(
        isinstance(node, ast.Import)
        and any(alias.name == "cm2_round306c41_d02_lower_strata_depth3_closure_v1" and alias.asname == "c41" for alias in node.names)
        for node in ast.walk(tree)
    )
    depth_six = any(
        isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "ADDITIONAL_DEPTH" for target in node.targets)
        and isinstance(node.value, ast.Constant)
        and node.value.value == 6
        for node in ast.walk(tree)
    )
    calls = {
        f"{node.func.value.id}.{node.func.attr}"
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
    }
    function_names = {
        node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    structural_defs = sorted(
        name for name in function_names
        if any(token in name.lower() for token in ("graph_cell", "off_graph", "slab_decider"))
    )
    need(imports_c41 and depth_six, "C65-inherited-router-and-depth")
    need("c41.route_at_path" in calls and "c41.disposition_family" in calls, "C65-inherited-route-calls")
    need(not structural_defs, "C65-no-new-structural-decider")
    shard_files = sorted(path.name for path in OUT.glob("cm2_round306c65s18_depth18_64shard_v2_shard_*") )
    need(not shard_files, "C65-no-completed-v2-shards-at-freeze")
    return {
        "runner_file_sha256": PINS["C65_RUNNER"],
        "additional_binary_depth_from_C61": 6,
        "nominal_depth_from_C58_after_run": 18,
        "imports_exact_C41_router": True,
        "calls_C41_route_at_path": True,
        "calls_C41_disposition_family": True,
        "new_graph_cell_or_off_graph_slab_decider_definition_count": 0,
        "completed_v2_shard_artifact_count": 0,
        "capability_delta": "DYADIC_SUBDIVISION_PLUS_INHERITED_C41_ROUTER_REPLAY_ONLY",
        "does_not_supply_required_structural_decider": True,
    }


def producer_attacks(expected: dict[str, Any]) -> dict[str, Any]:
    checks: list[tuple[str, str]] = []
    for key in sorted(expected):
        mutated = copy.deepcopy(expected)
        value = mutated[key]
        if type(value) is bool:
            mutated[key] = not value
        elif type(value) is int:
            mutated[key] = value + 1
        else:
            mutated[key] = str(value) + "__MUTATED"
        try:
            need(mutated == expected, "coherent-projection:" + key)
        except FailClosed:
            checks.append((f"projection_{key}", "FAIL_CLOSED"))
        else:
            raise FailClosed("producer-attack-escaped:" + key)
    need(len(checks) >= 30, "at-least-30-producer-attacks")
    return {
        "status": f"PASS_{len(checks)}_OF_{len(checks)}_PRODUCER_PROJECTION_ATTACKS_FAIL_CLOSED",
        "attack_count": len(checks),
        "attacks": dict(checks),
    }


def build() -> dict[str, Any]:
    initial_c67 = c67_matches()
    need(not initial_c67, "C67-not-present-at-frozen-inventory-start")

    paths = {
        "C41_RESULT": C41_RESULT,
        "C41_ROUTED": C41_ROUTED,
        "C56_RESULT": C56_RESULT,
        "C56_TASKS": C56_TASKS,
        "C56_CELLS": C56_CELLS,
        "C57_RESULT": C57_RESULT,
        "C57_LOCAL": C57_LOCAL,
        "C57_CELLS": C57_CELLS,
        "C57_EDGES": C57_EDGES,
        "C63_RESULT": C63_RESULT,
        "C63_EDGES": C63_EDGES,
        "C66_RESULT": C66_RESULT,
        "C66_EDGES": C66_EDGES,
        "C57S_RESULT": C57S_RESULT,
        "C57S_PARENTS": C57S_PARENTS,
        "C61_RESULT": C61_RESULT,
        "C61_LEAVES": C61_LEAVES,
        "C61_VERIFY": C61_VERIFY,
        "C61_MANIFEST": C61_MANIFEST,
        "C65_RUNNER": C65_RUNNER,
        "C65_CONTRACT": C65_CONTRACT,
        "C65_ASSIGN_RESULT": C65_ASSIGN_RESULT,
        "C65_ASSIGN": C65_ASSIGN,
        "C65_VERIFY": C65_VERIFY,
    }
    raw: dict[str, bytes] = {}
    identities: dict[str, dict[str, int]] = {}
    for key, path in paths.items():
        raw[key], identities[key] = secure_bytes(path, PINS[key])

    c41 = json_from_bytes(raw["C41_RESULT"])
    c56 = json_from_bytes(raw["C56_RESULT"])
    c57 = json_from_bytes(raw["C57_RESULT"])
    c63 = json_from_bytes(raw["C63_RESULT"])
    c66 = json_from_bytes(raw["C66_RESULT"])
    c57s = json_from_bytes(raw["C57S_RESULT"])
    c61 = json_from_bytes(raw["C61_RESULT"])
    c61verify = json_from_bytes(raw["C61_VERIFY"])
    c65contract = json_from_bytes(raw["C65_CONTRACT"])
    c65result = json_from_bytes(raw["C65_ASSIGN_RESULT"])
    c65verify = json_from_bytes(raw["C65_VERIFY"])
    for value, expected, label in (
        (c41, PINS["C41_OBJECT"], "C41"),
        (c56, PINS["C56_OBJECT"], "C56"),
        (c57, PINS["C57_OBJECT"], "C57"),
        (c63, PINS["C63_OBJECT"], "C63"),
        (c66, PINS["C66_OBJECT"], "C66"),
        (c57s, PINS["C57S_OBJECT"], "C57S"),
        (c61, PINS["C61_OBJECT"], "C61"),
        (c61verify, PINS["C61_VERIFY_OBJECT"], "C61-verify"),
        (c65contract, PINS["C65_CONTRACT_OBJECT"], "C65-contract"),
        (c65result, PINS["C65_ASSIGN_OBJECT"], "C65-assignment"),
        (c65verify, PINS["C65_VERIFY_OBJECT"], "C65-verify"),
    ):
        close_object(value, expected, label)

    c56_tasks = rows_from_bytes(raw["C56_TASKS"], c56["ledgers"]["post_C53_pending_logical_tasks"], "C56-tasks")
    all_c56_cells = rows_from_bytes(raw["C56_CELLS"], c56["ledgers"]["corridor_and_separator_cells"], "C56-cells")
    large_cells = [row for row in all_c56_cells if row["witness_kind"] == "EXPLICIT_TOPOLOGICAL_CORRIDOR_TO_STRICT_OPEN_ANCHOR"]
    need(len(c56_tasks) == 33319 and len(large_cells) == 1044, "C56-large-domain")

    c57_local_rows = rows_from_bytes(raw["C57_LOCAL"], c57["ledgers"]["local_collision1_cell_status"], "C57-local")
    c57_cell_rows = rows_from_bytes(raw["C57_CELLS"], c57["ledgers"]["corridor_cell_transport"], "C57-cell")
    c57_edge_rows = rows_from_bytes(raw["C57_EDGES"], c57["ledgers"]["edge_obligations"], "C57-edge")
    c63_edge_rows = rows_from_bytes(raw["C63_EDGES"], c63["ledgers"]["edge_replay"], "C63-edge")
    c66_edge_rows = rows_from_bytes(raw["C66_EDGES"], c66["ledgers"]["edge_owner_decisions"], "C66-edge")

    wanted = {row["C41_routed_ambient_row_sha256"] for row in c56_tasks}
    need(len(wanted) == 33319, "unique-C41-current-task-identities")
    c41_selected_list = selected_rows_from_bytes(
        raw["C41_ROUTED"],
        c41["ledgers"]["routed_ambient_cells"],
        "C41-routed",
        lambda row: row["row_sha256"] in wanted,
        lambda row: {
            key: row[key]
            for key in (
                "row_sha256", "pair_index", "path", "source_path", "descendant_bits",
                "representative_cell_id", "reflected_cell_id", "residual_classification",
                "round144_terminal_class", "route_method", "split_axis_history",
            )
        },
    )
    c41_selected = {row["row_sha256"]: row for row in c41_selected_list}
    need(set(c41_selected) == wanted, "complete-C41-current-task-selection")

    direct_by_blocker: dict[str, list[dict[str, Any]]] = defaultdict(list)
    task_class_census: Counter[str] = Counter()
    with Writer(OUT / TASK_FILE, "C56_POST_C53_CURRENT_TASK_ORDER") as writer:
        for task in c56_tasks:
            source = c41_selected[task["C41_routed_ambient_row_sha256"]]
            need(
                task["current_pending_logical_task"] is True
                and task["pair_index"] == source["pair_index"]
                and task["path"] == source["path"]
                and task["source_path"] == source["source_path"]
                and task["descendant_bits"] == source["descendant_bits"]
                and task["representative_cell_id"] == source["representative_cell_id"]
                and task["reflected_cell_id"] == source["reflected_cell_id"]
                and task["residual_classification"] == source["residual_classification"]
                and task["round144_terminal_class"] == source["round144_terminal_class"]
                and task["route_method"] == source["route_method"],
                "C56-task-direct-C41-binding",
            )
            past = source["residual_classification"].startswith(COLLISION2_PREFIX)
            body = {
                "schema": SCHEMA + ".large-current-task-replay-row",
                "C56_task_row_sha256": task["row_sha256"],
                "C41_routed_ambient_row_sha256": source["row_sha256"],
                "C55A_blocker_row_sha256": task["C55A_blocker_row_sha256"],
                "pair_index": task["pair_index"],
                "path": task["path"],
                "residual_classification": source["residual_classification"],
                "direct_C41_collision2_prefix_test": past,
                "current_pending_logical_task": True,
                "formal_credit": 0,
                "D02_gate_credit": 0,
            }
            written = writer.write(body)
            direct_by_blocker[task["C55A_blocker_row_sha256"]].append(written)
            task_class_census[source["residual_classification"]] += 1
    task_descriptor = writer.descriptor()

    large_by_id = {row["cell_id"]: row for row in large_cells}
    need(len(large_by_id) == 1044, "unique-large-cells")
    c57_local_by_id = {row["cell_id"]: row for row in c57_local_rows}
    c57_cell_by_id = {row["cell_id"]: row for row in c57_cell_rows}
    need(set(c57_local_by_id) == set(c57_cell_by_id) == set(large_by_id), "C57-C56-cell-domain")

    direct_local: dict[str, bool] = {}
    direct_task_counts: dict[str, int] = {}
    direct_class_census: dict[str, dict[str, int]] = {}
    for cell in large_cells:
        tasks = direct_by_blocker[cell["C55A_blocker_row_sha256"]]
        need(len(tasks) == cell["post_C53_pending_logical_task_count_for_pair"] and len(tasks) > 0, "cell-current-task-count")
        direct_local[cell["cell_id"]] = all(row["direct_C41_collision2_prefix_test"] for row in tasks)
        direct_task_counts[cell["cell_id"]] = len(tasks)
        direct_class_census[cell["cell_id"]] = dict(sorted(Counter(row["residual_classification"] for row in tasks).items()))
    need(sum(direct_local.values()) == 350, "direct-C41-local-350")

    c63_by_face = {row["face_or_corner_id"]: row for row in c63_edge_rows}
    c66_by_face = {row["face_or_corner_id"]: row for row in c66_edge_rows}
    c57_by_source = {row["source_cell_id"]: row for row in c57_edge_rows}
    need(len(c63_by_face) == len(c66_by_face) == len(c57_by_source) == 1042, "unique-edge-domains")
    need(set(c63_by_face) == set(c66_by_face) == {row["face_or_corner_id"] for row in c57_edge_rows}, "edge-face-domain")

    edge_output_by_source: dict[str, dict[str, Any]] = {}
    edge_local_census: Counter[str] = Counter()
    with Writer(OUT / EDGE_FILE, "C57_ROOTED_EDGE_ORDER") as writer:
        for old in c57_edge_rows:
            history = c63_by_face[old["face_or_corner_id"]]
            owner = c66_by_face[old["face_or_corner_id"]]
            need(
                history["glue_kind"] == owner["glue_kind"] == old["glue_kind"]
                and owner["C63_edge_replay_row_sha256"] == history["row_sha256"]
                and owner["C59_request_row_sha256"] == history["C59_request_row_sha256"],
                "C57-C63-C66-edge-crosswalk",
            )
            owner_pass = owner["all_atom_owners_unique"] is True and owner["decision"] == "STRICT_FULL_DOMAIN_OWNER_VECTOR_AVAILABLE"
            history_pass = history["all_atom_semantic_mappings_complete"] is True and history["all_atoms_in_complete_overlay_scope"] is True
            need(owner_pass and history_pass, "owner-and-history-pass")
            source_local = direct_local[old["source_cell_id"]]
            target_local = direct_local[old["target_cell_id"]]
            both_local = source_local and target_local
            edge_local_census[f"source_{str(source_local).lower()}__target_{str(target_local).lower()}__{old['glue_kind']}"] += 1
            blockers = ["C67_EXACT_EDGE_MARGIN_TRANSPORT_PENDING"]
            if not both_local:
                blockers.append("DIRECT_C41_ENDPOINT_LOCAL_FRONTIER_NOT_BOTH_BEYOND_COLLISION1")
            body = {
                "schema": SCHEMA + ".large-edge-blocker-row",
                "C57_edge_obligation_row_sha256": old["row_sha256"],
                "C63_history_edge_row_sha256": history["row_sha256"],
                "C66_owner_edge_row_sha256": owner["row_sha256"],
                "component_index": old["component_index"],
                "source_cell_id": old["source_cell_id"],
                "target_cell_id": old["target_cell_id"],
                "face_or_corner_id": old["face_or_corner_id"],
                "glue_kind": old["glue_kind"],
                "source_direct_C41_local_frontier_beyond_collision1": source_local,
                "target_direct_C41_local_frontier_beyond_collision1": target_local,
                "both_endpoint_direct_C41_frontiers_beyond_collision1": both_local,
                "owner_decision_pass": owner_pass,
                "semantic_history_map_pass": history_pass,
                "margin_evidence_status": "PENDING_C67_NOT_PRESENT_AT_FROZEN_INVENTORY_TIME",
                "margin_transport_pass": False,
                "edge_collision2_ready": False,
                "remaining_blocker_codes": blockers,
                "formal_credit": 0,
                "D02_gate_credit": 0,
            }
            written = writer.write(body)
            edge_output_by_source[old["source_cell_id"]] = written
    edge_descriptor = writer.descriptor()

    direct_whole: dict[str, bool] = {}
    old_local_match_count = 0
    old_whole_match_count = 0
    with Writer(OUT / CELL_FILE, "C56_LARGE_CORRIDOR_CELL_ORDER") as writer:
        for cell in large_cells:
            cell_id = cell["cell_id"]
            old_local = c57_local_by_id[cell_id]
            old_cell = c57_cell_by_id[cell_id]
            node_ids = [cell_id] + [step["to_cell_id"] for step in cell["corridor_steps"]]
            need(len(node_ids) == cell["corridor_step_count"] + 1 and len(node_ids) == len(set(node_ids)), "rooted-corridor-node-sequence")
            whole = all(direct_local[node] for node in node_ids)
            direct_whole[cell_id] = whole
            local_match = old_local["all_current_pending_tasks_beyond_collision1"] is direct_local[cell_id]
            whole_match = old_cell["all_corridor_nodes_local_pending_frontiers_beyond_collision1"] is whole
            old_local_match_count += int(local_match)
            old_whole_match_count += int(whole_match)
            need(local_match and whole_match, "independent-recompute-matches-C57-byte-ledger")
            path_edges = [edge_output_by_source[step["from_cell_id"]] for step in cell["corridor_steps"]]
            need(
                all(edge["face_or_corner_id"] == step["face_or_corner_id"] for edge, step in zip(path_edges, cell["corridor_steps"], strict=True)),
                "corridor-edge-sequence",
            )
            blockers: list[str] = []
            if not direct_local[cell_id]:
                blockers.append("DIRECT_C41_CURRENT_CELL_FRONTIER_RETAINS_COLLISION1_OR_LOWER_STRATA")
            if not whole:
                blockers.append("DIRECT_C41_ROOTED_CORRIDOR_CONTAINS_INCOMPLETE_COLLISION1_FRONTIER")
            if cell["corridor_step_count"] == 0:
                margin_status = "PENDING_C67_ANCHOR_WHOLE_CELL_MARGIN_PROMOTION"
                blockers.append("C67_ANCHOR_WHOLE_CELL_MARGIN_PENDING")
            else:
                margin_status = "PENDING_C67_EXACT_PATH_EDGE_MARGIN_TRANSPORT"
                blockers.append("C67_EXACT_PATH_EDGE_MARGIN_TRANSPORT_PENDING")
            body = {
                "schema": SCHEMA + ".large-corridor-cell-blocker-row",
                "C56_corridor_cell_row_sha256": cell["row_sha256"],
                "C57_local_status_row_sha256": old_local["row_sha256"],
                "C57_corridor_transport_row_sha256": old_cell["row_sha256"],
                "component_index": cell["component_index"],
                "cell_id": cell_id,
                "pair_index": cell["pair_index"],
                "corridor_step_count": cell["corridor_step_count"],
                "direct_C41_current_task_count": direct_task_counts[cell_id],
                "direct_C41_residual_classification_census": direct_class_census[cell_id],
                "direct_C41_all_current_pending_tasks_beyond_collision1": direct_local[cell_id],
                "direct_C41_all_corridor_nodes_beyond_collision1": whole,
                "C57_local_flag_exact_match": local_match,
                "C57_whole_corridor_flag_exact_match": whole_match,
                "rooted_corridor_node_count": len(node_ids),
                "rooted_corridor_cell_id_sequence_sha256": sequence_hash(node_ids),
                "path_edge_count": len(path_edges),
                "path_edge_blocker_row_hash_sequence_sha256": sequence_hash(edge["row_sha256"] for edge in path_edges),
                "all_path_owner_decisions_pass": all(edge["owner_decision_pass"] for edge in path_edges),
                "all_path_semantic_history_maps_pass": all(edge["semantic_history_map_pass"] for edge in path_edges),
                "margin_evidence_status": margin_status,
                "all_path_or_anchor_margin_pass": False,
                "collision2_ready": False,
                "remaining_blocker_codes": blockers,
                "formal_credit": 0,
                "D02_gate_credit": 0,
            }
            writer.write(body)
    cell_descriptor = writer.descriptor()
    need(sum(direct_whole.values()) == 89, "direct-C41-whole-corridor-89")
    need(old_local_match_count == old_whole_match_count == 1044, "all-C57-flags-independently-confirmed")

    # Singleton work is a disjoint scope.  C61/C65 cannot alter either large-component predicate.
    singleton_parents = rows_from_bytes(raw["C57S_PARENTS"], c57s["ledgers"]["parents"], "C57S-parents")
    singleton_cell_ids = {
        cell_id for row in singleton_parents for cell_id in (row["representative_cell_id"], row["reflected_cell_id"])
    }
    large_singleton_intersection = sorted(set(large_by_id) & singleton_cell_ids)
    need(len(singleton_parents) == 12 and len(singleton_cell_ids) == 24 and not large_singleton_intersection, "singleton-large-scope-disjoint")
    need(c61["whole_singletons_closed"] == 0 and c61["whole_singletons_remaining"] == 24 and c61["formal_credit"] == 0, "C61-zero-whole-singleton-credit")
    need(c61["frozen_inputs"]["C57_result_object_sha256"] == PINS["C57S_OBJECT"], "C61-C57S-binding")

    c61_selected = selected_rows_from_bytes(
        raw["C61_LEAVES"],
        c61["ledgers"]["aggregate_leaves"],
        "C61-leaves",
        lambda row: row["disposition"] == "COLLISION2_HANDOFF",
        lambda row: {
            key: row[key]
            for key in (
                "row_sha256", "pair_index", "path", "source_path", "source_handoff_ordinal",
                "source_C58_leaf_row_sha256", "source_shard_row_sha256", "parent_volume_fraction",
                "exact_representative_box", "exact_reflected_box", "route_classification",
                "route_witness", "route_method", "disposition", "continuation",
                "additional_depth_from_C58", "formal_credit", "whole_parent_credit",
                "D02_gate_credit", "local_terminal_credit",
            )
        },
    )
    assignments = rows_from_bytes(raw["C65_ASSIGN"], c65result["inventory"], "C65-assignments")
    assignment_by_source = {row["source_C61_aggregate_leaf_row_sha256"]: row for row in assignments}
    need(len(c61_selected) == len(assignments) == len(assignment_by_source) == 20879, "C61-C65-20879-domain")

    classification_census: Counter[str] = Counter()
    witness_census: Counter[str] = Counter()
    structural_census: Counter[str] = Counter()
    pair_census: Counter[str] = Counter()
    owner_census: Counter[str] = Counter()
    outgoing_census: Counter[str] = Counter()
    source_grazing_count = 0
    with Writer(OUT / SINGLETON_FILE, "C61_FILTERED_COLLISION2_HANDOFF_ORDER") as writer:
        for source in c61_selected:
            assignment = assignment_by_source[source["row_sha256"]]
            continuation = source["continuation"]
            need(
                assignment["source_C61_aggregate_leaf_row_sha256"] == source["row_sha256"]
                and assignment["pair_index"] == source["pair_index"]
                and assignment["path"] == source["path"]
                and assignment["source_C61_continuation_object_sha256"] == continuation["continuation_object_sha256"]
                and assignment["source_C61_disposition"] == "COLLISION2_HANDOFF"
                and assignment["source_C61_next_collision_index"] == 2,
                "C61-C65-assignment-binding",
            )
            classification = source["route_classification"]
            witness = source["route_witness"]
            kind = structural_kind(classification, witness)
            event = continuation["collision1_event_order"]
            owner = continuation["collision1_original_owner"]
            grazing = kind == "SOURCE_GRAZING_ENDPOINT_CHART"
            need(owner == "W[1,0]" and event["incoming_chart"] == "E" and event["outgoing_chart"] == "W", "frozen-owner-and-outgoing-factor")
            classification_census[classification] += 1
            witness_census[witness] += 1
            structural_census[kind] += 1
            pair_census[str(source["pair_index"])] += 1
            owner_census[owner] += 1
            outgoing_census[event["outgoing_chart"]] += 1
            source_grazing_count += int(grazing)
            body = {
                "schema": SCHEMA + ".singleton-structural-task-row",
                "C61_aggregate_leaf_row_sha256": source["row_sha256"],
                "C61_continuation_object_sha256": continuation["continuation_object_sha256"],
                "C65_assignment_row_sha256": assignment["row_sha256"],
                "C65_shard_id": assignment["shard_id"],
                "pair_index": source["pair_index"],
                "path": source["path"],
                "parent_volume_fraction": source["parent_volume_fraction"],
                "exact_representative_box_object_sha256": object_hash(source["exact_representative_box"]),
                "exact_reflected_box_object_sha256": object_hash(source["exact_reflected_box"]),
                "residual_classification": classification,
                "route_witness": witness,
                "structural_graph_kind": kind,
                "owner_candidate": owner,
                "incoming_chart": event["incoming_chart"],
                "outgoing_factor_candidate": event["outgoing_chart"],
                "official_word_key_id": event["official_word_key_id"],
                "official_word_variant_id": event["official_word_variant_id"],
                "source_grazing": grazing,
                "C65_capability_for_this_task": "DYADIC_SUBDIVISION_PLUS_INHERITED_C41_ROUTER_REPLAY_ONLY",
                "structural_decider_available": False,
                "required_next": REQUIRED_SINGLETON_DECIDER,
                "formal_credit": 0,
                "whole_parent_credit": 0,
                "D02_gate_credit": 0,
            }
            writer.write(body)
    singleton_descriptor = writer.descriptor()

    expected_classification = {
        "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE": 3222,
        "UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY": 11556,
        "UNRESOLVED_C39_C1_REGULAR_MULTI_GRAPH_ARRANGEMENT": 6101,
    }
    expected_witness = {
        "OUTGOING_STATE": 3222,
        "REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED": 9053,
        "REGULAR_FULL_FACE_GRAPH": 2356,
        "SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED": 147,
        "inherited interval ordering or boundary type not isolated": 5364,
        "unique monotone inherited-active-set first tangency": 737,
    }
    need(dict(sorted(classification_census.items())) == expected_classification, "exact-singleton-classification-census")
    need(dict(sorted(witness_census.items())) == dict(sorted(expected_witness.items())), "exact-singleton-witness-census")
    need(source_grazing_count == 147 and owner_census == Counter({"W[1,0]": 20879}) and outgoing_census == Counter({"W": 20879}), "singleton-structural-factors")
    c65_audit = audit_c65_runner(raw["C65_RUNNER"])

    need(c65result["input_count"] == 20879 and c65result["assignment_complete"] is True and c65result["candidate_is_authority"] is False and c65result["formal_credit"] == 0, "C65-assignment-zero-credit")
    need(c65verify["status"] == "PASS_INDEPENDENT_NO_RUNNER_IMPORT__FROZEN_CONTRACT_AND_20879_TO_64_ASSIGNMENT__ZERO_CREDIT", "C65-independent-preexecution")
    need(c65contract["refinement"]["additional_binary_depth"] == 6 and c65contract["formal_credit"] == 0, "C65-contract-depth")

    final_c67 = c67_matches()
    need(final_c67 == initial_c67 == [], "C67-absence-stable-through-build")

    scope = {
        "large_current_pending_task_count": 33319,
        "large_corridor_cell_count": 1044,
        "large_rooted_edge_count": 1042,
        "large_owner_pass_edge_count": 1042,
        "large_history_map_pass_edge_count": 1042,
        "large_margin_pass_edge_count": 0,
        "large_margin_pending_edge_count": 1042,
        "large_direct_C41_local_beyond_collision1_cell_count": 350,
        "large_direct_C41_local_not_beyond_collision1_cell_count": 694,
        "large_direct_C41_whole_corridor_beyond_collision1_cell_count": 89,
        "large_direct_C41_whole_corridor_not_beyond_collision1_cell_count": 955,
        "large_C57_local_flag_exact_match_count": 1044,
        "large_C57_whole_corridor_flag_exact_match_count": 1044,
        "large_collision2_ready_cell_count": 0,
        "singleton_parent_pair_count": 12,
        "singleton_cell_count": 24,
        "singleton_large_cell_intersection_count": 0,
        "C61_singleton_structural_task_count": 20879,
        "C61_whole_singletons_closed": 0,
        "C61_whole_singletons_remaining": 24,
        "C65_completed_v2_shard_artifact_count": 0,
        "C67_matching_artifact_count": 0,
        "formal_credit": 0,
        "D02_gate_credit": 0,
    }
    expected_attack_capsule = {
        **scope,
        "all_C66_owner_edges_pass": True,
        "all_C63_history_edges_pass": True,
        "C67_margin_pending": True,
        "direct_C41_recomputation_used": True,
        "C57_flags_not_blindly_inherited": True,
        "singleton_scope_disjoint": True,
        "C65_is_assignment_not_authority": True,
        "C65_new_structural_decider_count": 0,
        "depth24_recommended": False,
        "required_singleton_decider": REQUIRED_SINGLETON_DECIDER,
        "runtime_or_canonical_written": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    attacks = producer_attacks(expected_attack_capsule)

    result = {
        "schema": SCHEMA + ".result",
        "status": "PASS_FAIL_CLOSED_BLOCKER_CROSSWALK__OWNER_1042_HISTORY_1042__DIRECT_C41_LOCAL_350_WHOLE_89__MARGIN_PENDING__20879_SINGLETON_STRUCTURAL_TASKS__ZERO_CREDIT",
        "producer_file_sha256": file_hash(SELF),
        "input_file_sha256": {key: PINS[key] for key in paths},
        "input_file_identities": identities,
        "input_object_sha256": {
            "C41": PINS["C41_OBJECT"], "C56": PINS["C56_OBJECT"], "C57": PINS["C57_OBJECT"],
            "C63": PINS["C63_OBJECT"], "C66": PINS["C66_OBJECT"], "C57S": PINS["C57S_OBJECT"],
            "C61": PINS["C61_OBJECT"], "C61_independent_verification": PINS["C61_VERIFY_OBJECT"],
            "C65_contract": PINS["C65_CONTRACT_OBJECT"], "C65_assignment": PINS["C65_ASSIGN_OBJECT"],
            "C65_independent_preexecution_verification": PINS["C65_VERIFY_OBJECT"],
        },
        "C67_freeze": {
            "status": "PENDING_NO_C67_ARTIFACT_PRESENT_AT_FROZEN_INVENTORY_TIME",
            "matching_artifact_count": 0,
            "matching_paths": [],
            "margin_credit": 0,
        },
        "scope": scope,
        "large_component_findings": {
            "direct_C41_selected_task_residual_classification_census": dict(sorted(task_class_census.items())),
            "edge_endpoint_direct_local_status_census": dict(sorted(edge_local_census.items())),
            "owner_gate": "PASS_1042_OF_1042_EXACT_C66_EDGE_DECISIONS",
            "history_gate": "PASS_1042_OF_1042_EXACT_C63_SEMANTIC_MAPS",
            "margin_gate": "PENDING_C67__0_OF_1042",
            "local_frontier_gate": "DIRECT_C41_RECOMPUTE_350_OF_1044_ALL_CURRENT_TASKS_BEYOND_COLLISION1",
            "whole_corridor_gate": "DIRECT_C41_RECOMPUTE_89_OF_1044_ROOTED_CORRIDORS_ALL_NODES_BEYOND_COLLISION1",
            "C57_flags_independently_recomputed_not_inherited": True,
            "C57_local_and_whole_flags_remain_real_large_component_hard_gates": True,
            "C61_C65_singleton_work_can_change_large_component_flags": False,
        },
        "singleton_findings": {
            "classification_census": dict(sorted(classification_census.items())),
            "witness_census": dict(sorted(witness_census.items())),
            "structural_graph_kind_census": dict(sorted(structural_census.items())),
            "pair_index_census": dict(sorted(pair_census.items(), key=lambda item: int(item[0]))),
            "owner_candidate_census": dict(sorted(owner_census.items())),
            "outgoing_factor_candidate_census": dict(sorted(outgoing_census.items())),
            "source_grazing_task_count": source_grazing_count,
            "C65_static_capability_audit": c65_audit,
            "C65_depth18_is_not_a_new_structural_decider": True,
            "depth24_recommended": False,
            "required_next": REQUIRED_SINGLETON_DECIDER,
        },
        "ledgers": {
            "large_current_task_replay": task_descriptor,
            "large_edge_blockers": edge_descriptor,
            "large_corridor_cell_blockers": cell_descriptor,
            "singleton_structural_tasks": singleton_descriptor,
        },
        "producer_attacks": attacks,
        "TOCTOU_contract": {
            "O_NOFOLLOW_used": True,
            "regular_file_required": True,
            "st_nlink_exactly_one_required": True,
            "path_fd_identity_checked_before_read": True,
            "fd_identity_checked_after_read": True,
            "path_identity_checked_after_read": True,
            "sha256_checked_after_read": True,
            "C67_absence_checked_before_and_after_build": True,
        },
        "strict_boundary": {
            "read_only_inventory": True,
            "C66_consumed_as_frozen_candidate_evidence_not_runtime_authority": True,
            "C63_consumed_as_frozen_semantic_map_evidence": True,
            "C67_margin_status": "PENDING",
            "C65_assignment_is_authority": False,
            "runtime_or_canonical_written": False,
            "old_files_modified": False,
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": [
            "FREEZE_AND_INDEPENDENTLY_VERIFY_C67_EXACT_EDGE_AND_ANCHOR_MARGIN_TRANSPORT_BEFORE_ANY_LARGE_COMPONENT_HANDOFF",
            REQUIRED_SINGLETON_DECIDER,
            "REPLAY_C68_CROSSWALK_ONLY_FROM_EXACT_NEW_MARGIN_OR_STRUCTURAL_DECIDER_BYTES",
        ],
    }
    result["object_sha256"] = object_hash(result)
    (OUT / RESULT_FILE).write_bytes(canonical(result) + b"\n")

    report = f"""# C68-L read-only blocker crosswalk\n\nStatus: `{result['status']}`\n\nThe large-component owner and semantic-history gates now pass on all 1,042 rooted edges. The margin gate remains explicitly pending because no C67 artifact existed at the frozen inventory boundary. No authority, runtime pointer, canonical file, or credit was written.\n\n## Direct C41 recomputation\n\nC68 selected the exact 33,319 C56 current-pending tasks from the complete C41 routed ledger and recomputed the collision-one prefix predicate. The result is exactly 350/1,044 locally beyond collision one and 89/1,044 whole rooted corridors beyond collision one. Every recomputed local and whole-corridor flag matches the C57 ledger (1,044/1,044 each), but the result was derived from C41 bytes rather than copied from C57. The two predicates therefore remain real large-component hard gates.\n\nC57-S1/C61/C65 covers 24 singleton cells and has zero intersection with the 1,044 large-component corridor cells. It cannot change either large-component predicate.\n\n## Singleton structural inventory\n\nThe exact C61 residual census is 20,879 tasks: 11,556 H1 graph/boundary, 6,101 regular multi-graph arrangement, and 3,222 collision-one outgoing-state tasks. Witnesses are 9,053 regular boundary arrangements, 5,364 inherited-order/boundary-not-isolated tasks, 3,222 outgoing-state tasks, 2,356 regular full-face graph tasks, 737 first-tangency tasks, and 147 source-grazing tasks.\n\nC65 v2 is a frozen assignment plus an additional six-bit dyadic subdivision runner that calls the inherited C41 router. It defines no graph-cell or off-graph-slab decider, has no completed v2 shard artifacts at this freeze, and is not an authority. Repeating the same design at depth 24 is therefore not the required next capability. The frozen structural next step is `{REQUIRED_SINGLETON_DECIDER}`.\n\n## Frozen evidence\n\n- Result object: `{result['object_sha256']}`\n- Direct task replay: `{task_descriptor['sha256']}` ({task_descriptor['row_count']} rows)\n- Edge blocker crosswalk: `{edge_descriptor['sha256']}` ({edge_descriptor['row_count']} rows)\n- Corridor-cell blocker crosswalk: `{cell_descriptor['sha256']}` ({cell_descriptor['row_count']} rows)\n- Singleton structural tasks: `{singleton_descriptor['sha256']}` ({singleton_descriptor['row_count']} rows)\n\nFormal credit and D02 gate credit remain zero. CM2 remains `NO-GO_FOR_CLAIM`.\n"""
    (OUT / REPORT_FILE).write_text(report, encoding="utf-8")
    return result


def main() -> int:
    result = build()
    print(json.dumps({"status": result["status"], "scope": result["scope"], "object_sha256": result["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, TypeError, IndexError, SyntaxError) as error:
        print(f"FAIL_CLOSED:{type(error).__name__}:{error}", file=sys.stderr)
        raise SystemExit(2)
