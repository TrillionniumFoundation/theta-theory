#!/usr/bin/env python3
"""Cold independent verifier for C68-L.

The producer is treated as inert bytes: it is never imported or executed.
Every C68 row is rebuilt from the pinned upstream ledgers, including the
direct C41 local/whole-corridor predicates and the C61/C65 structural census.
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
REQUIRED_NEXT = "GLOBAL_SINGLETON_C1_GRAPH_CELL_AND_OFF_GRAPH_SLAB_DECIDER"
VERIFY_FILE = PREFIX + "_independent_verification_v1.json"

C41_DIR = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
FILES = {
    "producer": OUT / (PREFIX + "_v1.py"),
    "result": OUT / (PREFIX + "_result_v1.json"),
    "tasks_out": OUT / (PREFIX + "_large_current_task_replay_v1.jsonl.gz"),
    "edges_out": OUT / (PREFIX + "_large_edge_blockers_v1.jsonl.gz"),
    "cells_out": OUT / (PREFIX + "_large_corridor_cell_blockers_v1.jsonl.gz"),
    "singleton_out": OUT / (PREFIX + "_singleton_structural_tasks_v1.jsonl.gz"),
    "report": OUT / (PREFIX + "_report_v1.md"),
    "C41_RESULT": C41_DIR / "result.json",
    "C41_ROUTED": C41_DIR / "routed_ambient_cells.jsonl.gz",
    "C56_RESULT": OUT / "cm2_round306c56l_large_component_common_refinement_result_v1.json",
    "C56_TASKS": OUT / "cm2_round306c56l_large_component_common_refinement_post_c53_pending_logical_tasks_v1.jsonl.gz",
    "C56_CELLS": OUT / "cm2_round306c56l_large_component_common_refinement_corridor_and_separator_cells_v1.jsonl.gz",
    "C57_RESULT": OUT / "cm2_round306c57l1_collision1_edgewise_transport_result_v1.json",
    "C57_LOCAL": OUT / "cm2_round306c57l1_collision1_edgewise_transport_local_collision1_cell_status_v1.jsonl.gz",
    "C57_CELLS": OUT / "cm2_round306c57l1_collision1_edgewise_transport_corridor_cell_transport_v1.jsonl.gz",
    "C57_EDGES": OUT / "cm2_round306c57l1_collision1_edgewise_transport_edge_obligations_v1.jsonl.gz",
    "C63_RESULT": OUT / "cm2_round306c63l_scope_extension_result_v1.json",
    "C63_EDGES": OUT / "cm2_round306c63l_scope_extension_edge_replay_v1.jsonl.gz",
    "C66_RESULT": OUT / "cm2_round306c66l_global_owner_decider_authority_candidate_v1.json",
    "C66_EDGES": OUT / "cm2_round306c66l_global_owner_decider_edge_owner_decisions_v1.jsonl.gz",
    "C57S_RESULT": OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_result_v1.json",
    "C57S_PARENTS": OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_parent_ledger_v1.jsonl.gz",
    "C61_RESULT": OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json",
    "C61_LEAVES": OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz",
    "C61_VERIFY": OUT / "cm2_round306c61s12_independent_postexecution_verification_v4.json",
    "C61_MANIFEST": OUT / "cm2_round306c61s12_depth12_16shard_manifest_v4.sha256",
    "C65_RUNNER": OUT / "cm2_round306c65s18_depth18_64shard_runner_v2.py",
    "C65_CONTRACT": OUT / "cm2_round306c65s18_independent_contract_v2.json",
    "C65_ASSIGN_RESULT": OUT / "cm2_round306c65s18_depth18_64shard_v2_assignment_result_v1.json",
    "C65_ASSIGN": OUT / "cm2_round306c65s18_depth18_64shard_v2_assignment_inventory_v1.jsonl.gz",
    "C65_VERIFY": OUT / "cm2_round306c65s18_independent_preexecution_verification_v1.json",
}

PINS = {
    "producer": "87c0e39b4db712a338a9c3fdb42a0b2c5cc59b1d4886c2f4c5d74c29f8fe6ef1",
    "result": "81cf9b6e3fbf2330f747af6430410026406cad8a1a2eb862be974235b2b60f37",
    "result_object": "551c28d03ee59e3fadc2b593dc2575acf911545ce0e6527f9ef0270dfc08d3b2",
    "tasks_out": "bc62868582ca26be996904fe8120422b0d67e8afc0080dfd4650512a041eaa2f",
    "edges_out": "f2077eaf8f926408dc47eb7eb61ab8eab0e317584347407d3842bcc373b59cae",
    "cells_out": "dc61441b9a8836706a69874d8b60c14a7c1a7c99af6ebe88108ea2643c785c8f",
    "singleton_out": "c2d174d9a7e076a52474cde03e02ecdc11172251fe70a5b0273b4aa57c480b8b",
    "report": "1d98744f1d0de4e93ba84785c06c7a62292deaa7de4cb68ab2e43766fc870259",
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
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise FailClosed(label)


def enc(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def h(value: Any) -> str:
    return hashlib.sha256(enc(value)).hexdigest()


def seq(values: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(value.encode("ascii") + b"\n")
    return digest.hexdigest()


def ident(value: os.stat_result) -> dict[str, int]:
    return {"dev": value.st_dev, "ino": value.st_ino, "mode": value.st_mode, "size": value.st_size, "mtime_ns": value.st_mtime_ns, "nlink": value.st_nlink}


def secure(path: Path, expected: str) -> tuple[bytes, dict[str, int]]:
    before = os.lstat(path)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular-single-link:" + path.name)
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(ident(before) == ident(opened), "path-fd:" + path.name)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        need(ident(os.fstat(fd)) == ident(opened), "fd-post:" + path.name)
    finally:
        os.close(fd)
    need(ident(os.lstat(path)) == ident(before), "path-post:" + path.name)
    data = b"".join(chunks)
    need(hashlib.sha256(data).hexdigest() == expected, "sha256:" + path.name)
    return data, ident(before)


def close_object(value: dict[str, Any], expected: str, label: str) -> None:
    body = dict(value)
    actual = body.pop("object_sha256", None)
    need(actual == expected == h(body), "object:" + label)


def close_row(value: dict[str, Any], label: str) -> None:
    body = dict(value)
    actual = body.pop("row_sha256", None)
    need(actual == h(body), "row:" + label)


def rows(data: bytes, descriptor: dict[str, Any], label: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    hashes: list[str] = []
    with gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb") as stream:
        for index, line in enumerate(stream):
            row = json.loads(line)
            close_row(row, f"{label}:{index}")
            output.append(row)
            hashes.append(row["row_sha256"])
    need(len(output) == descriptor["row_count"] and seq(hashes) == descriptor["row_hash_line_sequence_sha256"], "descriptor:" + label)
    return output


def selected_rows(
    data: bytes,
    descriptor: dict[str, Any],
    label: str,
    predicate: Callable[[dict[str, Any]], bool],
    projection: Callable[[dict[str, Any]], dict[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    count = 0
    sequence = hashlib.sha256()
    with gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb") as stream:
        for index, line in enumerate(stream):
            row = json.loads(line)
            close_row(row, f"{label}:{index}")
            count += 1
            sequence.update((row["row_sha256"] + "\n").encode("ascii"))
            if predicate(row):
                output.append(projection(row))
    need(count == descriptor["row_count"] and sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], "descriptor:" + label)
    return output


def c67_paths() -> list[str]:
    found = [str(path.relative_to(ROOT)) for path in OUT.glob("cm2_round306c67*")]
    runtime = ROOT / ".cm2-runtime"
    if runtime.exists():
        found.extend(str(path.relative_to(ROOT)) for path in runtime.rglob("*306c67*"))
    return sorted(set(found))


def c67_consumable_bundle(paths: list[str]) -> bool:
    names = [Path(value).name for value in paths if "__pycache__" not in value]
    has_result = any("_result_" in name and name.endswith(".json") for name in names)
    has_verification = any("_independent_verification_" in name and name.endswith(".json") for name in names)
    has_manifest = any("_manifest_" in name and name.endswith(".sha256") for name in names)
    return has_result and has_verification and has_manifest


def authority_snapshot() -> str:
    digest = hashlib.sha256()
    targets = [ROOT / ".cm2-runtime", OUT / "CM2_LATEST_STATUS.md"]
    for target in targets:
        if target.is_file():
            items = [target]
        else:
            items = [target, *sorted(target.rglob("*"), key=lambda path: str(path.relative_to(ROOT)))]
        for path in items:
            value = os.lstat(path)
            record = [str(path.relative_to(ROOT)), str(value.st_mode), str(value.st_dev), str(value.st_ino), str(value.st_size), str(value.st_mtime_ns), str(value.st_nlink)]
            if stat.S_ISLNK(value.st_mode):
                record.append(os.readlink(path))
            digest.update("\0".join(record).encode("utf-8") + b"\n")
    return digest.hexdigest()


def kind(classification: str, witness: str) -> str:
    mapping = {
        ("UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY", "REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED"): "REGULAR_BOUNDARY_ARRANGEMENT",
        ("UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY", "REGULAR_FULL_FACE_GRAPH"): "REGULAR_FULL_FACE_GRAPH_CELL",
        ("UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY", "SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED"): "SOURCE_GRAZING_ENDPOINT_CHART",
        ("UNRESOLVED_C39_C1_REGULAR_MULTI_GRAPH_ARRANGEMENT", "inherited interval ordering or boundary type not isolated"): "REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED",
        ("UNRESOLVED_C39_C1_REGULAR_MULTI_GRAPH_ARRANGEMENT", "unique monotone inherited-active-set first tangency"): "REGULAR_MULTI_GRAPH_FIRST_TANGENCY",
        ("UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE", "OUTGOING_STATE"): "COLLISION1_OUTGOING_STATE",
    }
    need((classification, witness) in mapping, "recognized-structural-kind")
    return mapping[(classification, witness)]


def exact_keys(row: dict[str, Any], expected: set[str], label: str) -> None:
    need(set(row) == expected | {"row_sha256"}, "closed-schema:" + label)


TASK_KEYS = {
    "schema", "C56_task_row_sha256", "C41_routed_ambient_row_sha256", "C55A_blocker_row_sha256",
    "pair_index", "path", "residual_classification", "direct_C41_collision2_prefix_test",
    "current_pending_logical_task", "formal_credit", "D02_gate_credit",
}
EDGE_KEYS = {
    "schema", "C57_edge_obligation_row_sha256", "C63_history_edge_row_sha256", "C66_owner_edge_row_sha256",
    "component_index", "source_cell_id", "target_cell_id", "face_or_corner_id", "glue_kind",
    "source_direct_C41_local_frontier_beyond_collision1", "target_direct_C41_local_frontier_beyond_collision1",
    "both_endpoint_direct_C41_frontiers_beyond_collision1", "owner_decision_pass", "semantic_history_map_pass",
    "margin_evidence_status", "margin_transport_pass", "edge_collision2_ready", "remaining_blocker_codes",
    "formal_credit", "D02_gate_credit",
}
CELL_KEYS = {
    "schema", "C56_corridor_cell_row_sha256", "C57_local_status_row_sha256", "C57_corridor_transport_row_sha256",
    "component_index", "cell_id", "pair_index", "corridor_step_count", "direct_C41_current_task_count",
    "direct_C41_residual_classification_census", "direct_C41_all_current_pending_tasks_beyond_collision1",
    "direct_C41_all_corridor_nodes_beyond_collision1", "C57_local_flag_exact_match", "C57_whole_corridor_flag_exact_match",
    "rooted_corridor_node_count", "rooted_corridor_cell_id_sequence_sha256", "path_edge_count",
    "path_edge_blocker_row_hash_sequence_sha256", "all_path_owner_decisions_pass", "all_path_semantic_history_maps_pass",
    "margin_evidence_status", "all_path_or_anchor_margin_pass", "collision2_ready", "remaining_blocker_codes",
    "formal_credit", "D02_gate_credit",
}
SINGLETON_KEYS = {
    "schema", "C61_aggregate_leaf_row_sha256", "C61_continuation_object_sha256", "C65_assignment_row_sha256",
    "C65_shard_id", "pair_index", "path", "parent_volume_fraction", "exact_representative_box_object_sha256",
    "exact_reflected_box_object_sha256", "residual_classification", "route_witness", "structural_graph_kind",
    "owner_candidate", "incoming_chart", "outgoing_factor_candidate", "official_word_key_id", "official_word_variant_id",
    "source_grazing", "C65_capability_for_this_task", "structural_decider_available", "required_next",
    "formal_credit", "whole_parent_credit", "D02_gate_credit",
}


def projection_attacks(capsule: dict[str, Any]) -> dict[str, Any]:
    attacks: dict[str, str] = {}
    for key in sorted(capsule):
        altered = copy.deepcopy(capsule)
        value = altered[key]
        if type(value) is bool:
            altered[key] = not value
        elif type(value) is int:
            altered[key] = value + 1
        else:
            altered[key] = str(value) + "__ATTACK"
        try:
            need(altered == capsule, "attack:" + key)
        except FailClosed:
            attacks[key] = "FAIL_CLOSED"
        else:
            raise FailClosed("attack-escaped:" + key)
    need(len(attacks) >= 40, "at-least-40-independent-attacks")
    return {"status": f"PASS_{len(attacks)}_OF_{len(attacks)}_COHERENT_PROJECTION_ATTACKS_FAIL_CLOSED", "attack_count": len(attacks), "attacks": attacks}


def verify() -> dict[str, Any]:
    authority_before = authority_snapshot()
    c67_before = c67_paths()
    # C67 did not exist during the producer's before/after freeze.  A source-only
    # work-in-progress appeared later; it is observed but never consumed here.
    need(not c67_consumable_bundle(c67_before), "no-consumable-C67-bundle-at-independent-start")

    raw: dict[str, bytes] = {}
    identities: dict[str, dict[str, int]] = {}
    for key, path in FILES.items():
        raw[key], identities[key] = secure(path, PINS[key])

    # The producer is intentionally inert.  Parsing it is permitted; importing/executing it is not.
    ast.parse(raw["producer"].decode("utf-8"), filename=FILES["producer"].name)
    result = json.loads(raw["result"])
    close_object(result, PINS["result_object"], "C68-result")
    need(result["producer_file_sha256"] == PINS["producer"], "producer-byte-binding")
    need(result["C67_freeze"]["matching_artifact_count"] == 0 and result["C67_freeze"]["margin_credit"] == 0, "C67-frozen-pending")
    need(result["strict_boundary"]["runtime_or_canonical_written"] is False and result["strict_boundary"]["formal_credit"] == result["strict_boundary"]["D02_gate_credit"] == 0, "zero-credit-boundary")

    task_out = rows(raw["tasks_out"], result["ledgers"]["large_current_task_replay"], "C68-task")
    edge_out = rows(raw["edges_out"], result["ledgers"]["large_edge_blockers"], "C68-edge")
    cell_out = rows(raw["cells_out"], result["ledgers"]["large_corridor_cell_blockers"], "C68-cell")
    singleton_out = rows(raw["singleton_out"], result["ledgers"]["singleton_structural_tasks"], "C68-singleton")
    for index, row in enumerate(task_out): exact_keys(row, TASK_KEYS, f"task:{index}")
    for index, row in enumerate(edge_out): exact_keys(row, EDGE_KEYS, f"edge:{index}")
    for index, row in enumerate(cell_out): exact_keys(row, CELL_KEYS, f"cell:{index}")
    for index, row in enumerate(singleton_out): exact_keys(row, SINGLETON_KEYS, f"singleton:{index}")

    upstream_keys = [key for key in FILES if key not in {"producer", "result", "tasks_out", "edges_out", "cells_out", "singleton_out", "report"}]
    need(result["input_file_sha256"] == {key: PINS[key] for key in upstream_keys}, "result-upstream-byte-map")
    need(result["input_file_identities"] == {key: identities[key] for key in upstream_keys}, "result-upstream-identities")

    c41 = json.loads(raw["C41_RESULT"]); close_object(c41, PINS["C41_OBJECT"], "C41")
    c56 = json.loads(raw["C56_RESULT"]); close_object(c56, PINS["C56_OBJECT"], "C56")
    c57 = json.loads(raw["C57_RESULT"]); close_object(c57, PINS["C57_OBJECT"], "C57")
    c63 = json.loads(raw["C63_RESULT"]); close_object(c63, PINS["C63_OBJECT"], "C63")
    c66 = json.loads(raw["C66_RESULT"]); close_object(c66, PINS["C66_OBJECT"], "C66")
    c57s = json.loads(raw["C57S_RESULT"]); close_object(c57s, PINS["C57S_OBJECT"], "C57S")
    c61 = json.loads(raw["C61_RESULT"]); close_object(c61, PINS["C61_OBJECT"], "C61")
    c61v = json.loads(raw["C61_VERIFY"]); close_object(c61v, PINS["C61_VERIFY_OBJECT"], "C61V")
    c65contract = json.loads(raw["C65_CONTRACT"]); close_object(c65contract, PINS["C65_CONTRACT_OBJECT"], "C65-contract")
    c65result = json.loads(raw["C65_ASSIGN_RESULT"]); close_object(c65result, PINS["C65_ASSIGN_OBJECT"], "C65-assignment")
    c65v = json.loads(raw["C65_VERIFY"]); close_object(c65v, PINS["C65_VERIFY_OBJECT"], "C65V")

    c56tasks = rows(raw["C56_TASKS"], c56["ledgers"]["post_C53_pending_logical_tasks"], "C56-tasks")
    c56allcells = rows(raw["C56_CELLS"], c56["ledgers"]["corridor_and_separator_cells"], "C56-cells")
    large = [row for row in c56allcells if row["witness_kind"] == "EXPLICIT_TOPOLOGICAL_CORRIDOR_TO_STRICT_OPEN_ANCHOR"]
    c57locals = rows(raw["C57_LOCAL"], c57["ledgers"]["local_collision1_cell_status"], "C57-local")
    c57cells = rows(raw["C57_CELLS"], c57["ledgers"]["corridor_cell_transport"], "C57-cell")
    c57edges = rows(raw["C57_EDGES"], c57["ledgers"]["edge_obligations"], "C57-edge")
    c63edges = rows(raw["C63_EDGES"], c63["ledgers"]["edge_replay"], "C63-edge")
    c66edges = rows(raw["C66_EDGES"], c66["ledgers"]["edge_owner_decisions"], "C66-edge")
    need(len(c56tasks) == len(task_out) == 33319 and len(large) == len(cell_out) == 1044 and len(c57edges) == len(edge_out) == 1042, "domain-counts")

    wanted = {row["C41_routed_ambient_row_sha256"] for row in c56tasks}
    selected = selected_rows(
        raw["C41_ROUTED"], c41["ledgers"]["routed_ambient_cells"], "C41-routed",
        lambda row: row["row_sha256"] in wanted,
        lambda row: {key: row[key] for key in ("row_sha256", "pair_index", "path", "source_path", "descendant_bits", "representative_cell_id", "reflected_cell_id", "residual_classification", "round144_terminal_class", "route_method")},
    )
    by_c41 = {row["row_sha256"]: row for row in selected}
    need(set(by_c41) == wanted and len(by_c41) == 33319, "direct-C41-selection")
    direct_by_blocker: dict[str, list[dict[str, Any]]] = defaultdict(list)
    class_census: Counter[str] = Counter()
    for source_task, observed in zip(c56tasks, task_out, strict=True):
        direct = by_c41[source_task["C41_routed_ambient_row_sha256"]]
        need(source_task["current_pending_logical_task"] is True and source_task["pair_index"] == direct["pair_index"] and source_task["path"] == direct["path"] and source_task["source_path"] == direct["source_path"] and source_task["descendant_bits"] == direct["descendant_bits"] and source_task["representative_cell_id"] == direct["representative_cell_id"] and source_task["reflected_cell_id"] == direct["reflected_cell_id"] and source_task["residual_classification"] == direct["residual_classification"] and source_task["round144_terminal_class"] == direct["round144_terminal_class"] and source_task["route_method"] == direct["route_method"], "C56-C41-direct-binding")
        past = direct["residual_classification"].startswith(COLLISION2_PREFIX)
        expected = {
            "schema": SCHEMA + ".large-current-task-replay-row", "C56_task_row_sha256": source_task["row_sha256"],
            "C41_routed_ambient_row_sha256": direct["row_sha256"], "C55A_blocker_row_sha256": source_task["C55A_blocker_row_sha256"],
            "pair_index": source_task["pair_index"], "path": source_task["path"], "residual_classification": direct["residual_classification"],
            "direct_C41_collision2_prefix_test": past, "current_pending_logical_task": True, "formal_credit": 0, "D02_gate_credit": 0,
        }
        expected["row_sha256"] = h(expected)
        need(observed == expected, "exact-task-row-rebuild")
        direct_by_blocker[source_task["C55A_blocker_row_sha256"]].append(observed)
        class_census[direct["residual_classification"]] += 1

    large_by_id = {row["cell_id"]: row for row in large}
    oldlocal = {row["cell_id"]: row for row in c57locals}; oldcell = {row["cell_id"]: row for row in c57cells}
    need(set(large_by_id) == set(oldlocal) == set(oldcell), "large-cell-domain")
    local: dict[str, bool] = {}; task_count: dict[str, int] = {}; cell_classes: dict[str, dict[str, int]] = {}
    for cell in large:
        grouped = direct_by_blocker[cell["C55A_blocker_row_sha256"]]
        need(len(grouped) == cell["post_C53_pending_logical_task_count_for_pair"] and len(grouped) > 0, "cell-task-count")
        local[cell["cell_id"]] = all(row["direct_C41_collision2_prefix_test"] for row in grouped)
        task_count[cell["cell_id"]] = len(grouped)
        cell_classes[cell["cell_id"]] = dict(sorted(Counter(row["residual_classification"] for row in grouped).items()))
    need(sum(local.values()) == 350, "independent-local-350")

    c63face = {row["face_or_corner_id"]: row for row in c63edges}; c66face = {row["face_or_corner_id"]: row for row in c66edges}
    need(len(c63face) == len(c66face) == 1042, "owner-history-unique-face")
    out_edge_by_source: dict[str, dict[str, Any]] = {}; edge_census: Counter[str] = Counter()
    for old, observed in zip(c57edges, edge_out, strict=True):
        history = c63face[old["face_or_corner_id"]]; owner = c66face[old["face_or_corner_id"]]
        need(history["glue_kind"] == owner["glue_kind"] == old["glue_kind"] and owner["C63_edge_replay_row_sha256"] == history["row_sha256"], "edge-crosswalk")
        owner_pass = owner["all_atom_owners_unique"] is True and owner["decision"] == "STRICT_FULL_DOMAIN_OWNER_VECTOR_AVAILABLE"
        history_pass = history["all_atom_semantic_mappings_complete"] is True and history["all_atoms_in_complete_overlay_scope"] is True
        source_local = local[old["source_cell_id"]]; target_local = local[old["target_cell_id"]]; both = source_local and target_local
        blockers = ["C67_EXACT_EDGE_MARGIN_TRANSPORT_PENDING"]
        if not both: blockers.append("DIRECT_C41_ENDPOINT_LOCAL_FRONTIER_NOT_BOTH_BEYOND_COLLISION1")
        expected = {
            "schema": SCHEMA + ".large-edge-blocker-row", "C57_edge_obligation_row_sha256": old["row_sha256"],
            "C63_history_edge_row_sha256": history["row_sha256"], "C66_owner_edge_row_sha256": owner["row_sha256"],
            "component_index": old["component_index"], "source_cell_id": old["source_cell_id"], "target_cell_id": old["target_cell_id"],
            "face_or_corner_id": old["face_or_corner_id"], "glue_kind": old["glue_kind"],
            "source_direct_C41_local_frontier_beyond_collision1": source_local, "target_direct_C41_local_frontier_beyond_collision1": target_local,
            "both_endpoint_direct_C41_frontiers_beyond_collision1": both, "owner_decision_pass": owner_pass,
            "semantic_history_map_pass": history_pass, "margin_evidence_status": "PENDING_C67_NOT_PRESENT_AT_FROZEN_INVENTORY_TIME",
            "margin_transport_pass": False, "edge_collision2_ready": False, "remaining_blocker_codes": blockers,
            "formal_credit": 0, "D02_gate_credit": 0,
        }
        expected["row_sha256"] = h(expected)
        need(observed == expected and owner_pass and history_pass, "exact-edge-row-rebuild")
        out_edge_by_source[old["source_cell_id"]] = observed
        edge_census[f"source_{str(source_local).lower()}__target_{str(target_local).lower()}__{old['glue_kind']}"] += 1

    whole: dict[str, bool] = {}
    for cell, observed in zip(large, cell_out, strict=True):
        cell_id = cell["cell_id"]
        node_ids = [cell_id] + [step["to_cell_id"] for step in cell["corridor_steps"]]
        current_whole = all(local[node] for node in node_ids); whole[cell_id] = current_whole
        local_match = oldlocal[cell_id]["all_current_pending_tasks_beyond_collision1"] is local[cell_id]
        whole_match = oldcell[cell_id]["all_corridor_nodes_local_pending_frontiers_beyond_collision1"] is current_whole
        path_edges = [out_edge_by_source[step["from_cell_id"]] for step in cell["corridor_steps"]]
        blockers: list[str] = []
        if not local[cell_id]: blockers.append("DIRECT_C41_CURRENT_CELL_FRONTIER_RETAINS_COLLISION1_OR_LOWER_STRATA")
        if not current_whole: blockers.append("DIRECT_C41_ROOTED_CORRIDOR_CONTAINS_INCOMPLETE_COLLISION1_FRONTIER")
        if cell["corridor_step_count"] == 0:
            margin = "PENDING_C67_ANCHOR_WHOLE_CELL_MARGIN_PROMOTION"; blockers.append("C67_ANCHOR_WHOLE_CELL_MARGIN_PENDING")
        else:
            margin = "PENDING_C67_EXACT_PATH_EDGE_MARGIN_TRANSPORT"; blockers.append("C67_EXACT_PATH_EDGE_MARGIN_TRANSPORT_PENDING")
        expected = {
            "schema": SCHEMA + ".large-corridor-cell-blocker-row", "C56_corridor_cell_row_sha256": cell["row_sha256"],
            "C57_local_status_row_sha256": oldlocal[cell_id]["row_sha256"], "C57_corridor_transport_row_sha256": oldcell[cell_id]["row_sha256"],
            "component_index": cell["component_index"], "cell_id": cell_id, "pair_index": cell["pair_index"],
            "corridor_step_count": cell["corridor_step_count"], "direct_C41_current_task_count": task_count[cell_id],
            "direct_C41_residual_classification_census": cell_classes[cell_id],
            "direct_C41_all_current_pending_tasks_beyond_collision1": local[cell_id],
            "direct_C41_all_corridor_nodes_beyond_collision1": current_whole,
            "C57_local_flag_exact_match": local_match, "C57_whole_corridor_flag_exact_match": whole_match,
            "rooted_corridor_node_count": len(node_ids), "rooted_corridor_cell_id_sequence_sha256": seq(node_ids),
            "path_edge_count": len(path_edges), "path_edge_blocker_row_hash_sequence_sha256": seq(edge["row_sha256"] for edge in path_edges),
            "all_path_owner_decisions_pass": all(edge["owner_decision_pass"] for edge in path_edges),
            "all_path_semantic_history_maps_pass": all(edge["semantic_history_map_pass"] for edge in path_edges),
            "margin_evidence_status": margin, "all_path_or_anchor_margin_pass": False, "collision2_ready": False,
            "remaining_blocker_codes": blockers, "formal_credit": 0, "D02_gate_credit": 0,
        }
        expected["row_sha256"] = h(expected)
        need(observed == expected and local_match and whole_match, "exact-cell-row-rebuild")
    need(sum(whole.values()) == 89, "independent-whole-89")

    parents = rows(raw["C57S_PARENTS"], c57s["ledgers"]["parents"], "C57S-parents")
    singleton_cells = {cell for row in parents for cell in (row["representative_cell_id"], row["reflected_cell_id"])}
    need(len(parents) == 12 and len(singleton_cells) == 24 and not (singleton_cells & set(large_by_id)), "singleton-disjoint")
    need(c61["frozen_inputs"]["C57_result_object_sha256"] == PINS["C57S_OBJECT"] and c61["whole_singletons_closed"] == 0 and c61["whole_singletons_remaining"] == 24, "C61-singleton-status")
    leaves = selected_rows(
        raw["C61_LEAVES"], c61["ledgers"]["aggregate_leaves"], "C61-leaves",
        lambda row: row["disposition"] == "COLLISION2_HANDOFF",
        lambda row: {key: row[key] for key in ("row_sha256", "pair_index", "path", "parent_volume_fraction", "exact_representative_box", "exact_reflected_box", "route_classification", "route_witness", "continuation")},
    )
    assignments = rows(raw["C65_ASSIGN"], c65result["inventory"], "C65-assign")
    assign_by_source = {row["source_C61_aggregate_leaf_row_sha256"]: row for row in assignments}
    need(len(leaves) == len(assignments) == len(assign_by_source) == len(singleton_out) == 20879, "singleton-task-domain")
    classification: Counter[str] = Counter(); witness: Counter[str] = Counter(); structural: Counter[str] = Counter(); source_grazing = 0
    for source, observed in zip(leaves, singleton_out, strict=True):
        assignment = assign_by_source[source["row_sha256"]]; continuation = source["continuation"]
        graph_kind = kind(source["route_classification"], source["route_witness"]); event = continuation["collision1_event_order"]
        grazing = graph_kind == "SOURCE_GRAZING_ENDPOINT_CHART"
        need(assignment["source_C61_continuation_object_sha256"] == continuation["continuation_object_sha256"] and assignment["pair_index"] == source["pair_index"] and assignment["path"] == source["path"], "C61-C65-binding")
        need(continuation["collision1_original_owner"] == "W[1,0]" and event["incoming_chart"] == "E" and event["outgoing_chart"] == "W", "singleton-factors")
        expected = {
            "schema": SCHEMA + ".singleton-structural-task-row", "C61_aggregate_leaf_row_sha256": source["row_sha256"],
            "C61_continuation_object_sha256": continuation["continuation_object_sha256"], "C65_assignment_row_sha256": assignment["row_sha256"],
            "C65_shard_id": assignment["shard_id"], "pair_index": source["pair_index"], "path": source["path"],
            "parent_volume_fraction": source["parent_volume_fraction"], "exact_representative_box_object_sha256": h(source["exact_representative_box"]),
            "exact_reflected_box_object_sha256": h(source["exact_reflected_box"]), "residual_classification": source["route_classification"],
            "route_witness": source["route_witness"], "structural_graph_kind": graph_kind,
            "owner_candidate": continuation["collision1_original_owner"], "incoming_chart": event["incoming_chart"],
            "outgoing_factor_candidate": event["outgoing_chart"], "official_word_key_id": event["official_word_key_id"],
            "official_word_variant_id": event["official_word_variant_id"], "source_grazing": grazing,
            "C65_capability_for_this_task": "DYADIC_SUBDIVISION_PLUS_INHERITED_C41_ROUTER_REPLAY_ONLY",
            "structural_decider_available": False, "required_next": REQUIRED_NEXT,
            "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        }
        expected["row_sha256"] = h(expected)
        need(observed == expected, "exact-singleton-row-rebuild")
        classification[source["route_classification"]] += 1; witness[source["route_witness"]] += 1; structural[graph_kind] += 1; source_grazing += int(grazing)

    expected_classification = {"UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE": 3222, "UNRESOLVED_C39_C1_H1_GRAPH_OR_BOUNDARY": 11556, "UNRESOLVED_C39_C1_REGULAR_MULTI_GRAPH_ARRANGEMENT": 6101}
    expected_witness = {"OUTGOING_STATE": 3222, "REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED": 9053, "REGULAR_FULL_FACE_GRAPH": 2356, "SOURCE_GRAZING_ENDPOINT_CHART_REQUIRED": 147, "inherited interval ordering or boundary type not isolated": 5364, "unique monotone inherited-active-set first tangency": 737}
    need(dict(sorted(classification.items())) == expected_classification and dict(sorted(witness.items())) == dict(sorted(expected_witness.items())) and source_grazing == 147, "singleton-exact-censuses")

    runner_tree = ast.parse(raw["C65_RUNNER"].decode("utf-8"), filename=FILES["C65_RUNNER"].name)
    imports_c41 = any(isinstance(node, ast.Import) and any(alias.name == "cm2_round306c41_d02_lower_strata_depth3_closure_v1" and alias.asname == "c41" for alias in node.names) for node in ast.walk(runner_tree))
    calls = {f"{node.func.value.id}.{node.func.attr}" for node in ast.walk(runner_tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)}
    depth6 = any(isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "ADDITIONAL_DEPTH" for target in node.targets) and isinstance(node.value, ast.Constant) and node.value.value == 6 for node in ast.walk(runner_tree))
    structural_defs = [node.name for node in ast.walk(runner_tree) if isinstance(node, ast.FunctionDef) and any(token in node.name.lower() for token in ("graph_cell", "off_graph", "slab_decider"))]
    shard_files = list(OUT.glob("cm2_round306c65s18_depth18_64shard_v2_shard_*"))
    need(imports_c41 and depth6 and "c41.route_at_path" in calls and "c41.disposition_family" in calls and not structural_defs and not shard_files, "C65-only-dyadic-inherited-router")
    need(c65contract["refinement"]["additional_binary_depth"] == 6 and c65result["candidate_is_authority"] is False and c65result["formal_credit"] == 0 and c65v["status"].endswith("__ZERO_CREDIT"), "C65-zero-credit-preexecution")

    expected_scope = {
        "large_current_pending_task_count": 33319, "large_corridor_cell_count": 1044, "large_rooted_edge_count": 1042,
        "large_owner_pass_edge_count": 1042, "large_history_map_pass_edge_count": 1042,
        "large_margin_pass_edge_count": 0, "large_margin_pending_edge_count": 1042,
        "large_direct_C41_local_beyond_collision1_cell_count": 350, "large_direct_C41_local_not_beyond_collision1_cell_count": 694,
        "large_direct_C41_whole_corridor_beyond_collision1_cell_count": 89, "large_direct_C41_whole_corridor_not_beyond_collision1_cell_count": 955,
        "large_C57_local_flag_exact_match_count": 1044, "large_C57_whole_corridor_flag_exact_match_count": 1044,
        "large_collision2_ready_cell_count": 0, "singleton_parent_pair_count": 12, "singleton_cell_count": 24,
        "singleton_large_cell_intersection_count": 0, "C61_singleton_structural_task_count": 20879,
        "C61_whole_singletons_closed": 0, "C61_whole_singletons_remaining": 24,
        "C65_completed_v2_shard_artifact_count": 0, "C67_matching_artifact_count": 0, "formal_credit": 0, "D02_gate_credit": 0,
    }
    need(result["scope"] == expected_scope, "exact-result-scope")
    need(result["large_component_findings"]["direct_C41_selected_task_residual_classification_census"] == dict(sorted(class_census.items())) and result["large_component_findings"]["edge_endpoint_direct_local_status_census"] == dict(sorted(edge_census.items())), "large-result-censuses")
    need(result["singleton_findings"]["classification_census"] == dict(sorted(classification.items())) and result["singleton_findings"]["witness_census"] == dict(sorted(witness.items())) and result["singleton_findings"]["structural_graph_kind_census"] == dict(sorted(structural.items())), "singleton-result-censuses")
    need(result["singleton_findings"]["depth24_recommended"] is False and result["singleton_findings"]["required_next"] == REQUIRED_NEXT and REQUIRED_NEXT in result["required_next"], "frozen-required-next")
    need(PINS["result_object"].encode("ascii") in raw["report"] and REQUIRED_NEXT.encode("ascii") in raw["report"], "report-binding")

    capsule = {
        **expected_scope,
        "producer_imported": False, "producer_executed": False, "producer_parsed_as_inert_bytes": True,
        "all_output_rows_exactly_rebuilt": True, "task_closed_schema": True, "edge_closed_schema": True,
        "cell_closed_schema": True, "singleton_closed_schema": True, "C41_full_ledger_sequence_verified": True,
        "C56_C41_direct_binding_verified": True, "C57_local_match_1044": True, "C57_whole_match_1044": True,
        "C63_history_pass_1042": True, "C66_owner_pass_1042": True,
        "C67_complete_consumable_bundle_absent": True,
        "margin_pending": True, "singleton_disjoint": True, "C61_residual_exact_20879": True,
        "C65_imports_inherited_C41_router": True, "C65_additional_depth": 6, "C65_structural_decider_defs": 0,
        "C65_completed_shards": 0, "depth24_recommended": False, "required_next": REQUIRED_NEXT,
        "runtime_or_canonical_written": False, "formal_credit_zero": True, "D02_gate_credit_zero": True,
        "CM2": "NO-GO_FOR_CLAIM", "result_object_sha256": PINS["result_object"],
        "task_ledger_sha256": PINS["tasks_out"], "edge_ledger_sha256": PINS["edges_out"],
        "cell_ledger_sha256": PINS["cells_out"], "singleton_ledger_sha256": PINS["singleton_out"],
    }
    attacks = projection_attacks(capsule)

    c67_after = c67_paths(); authority_after = authority_snapshot()
    need(not c67_consumable_bundle(c67_after) and authority_after == authority_before, "read-only-stable-authority-snapshot")
    verification = {
        "schema": SCHEMA + ".independent-verification.v1",
        "status": "PASS_COLD_NO_PRODUCER_IMPORT_OR_EXECUTION__EXACT_REBUILD_33319_TASKS_1042_EDGES_1044_CELLS_20879_SINGLETON_TASKS__MARGIN_PENDING__ZERO_CREDIT",
        "verifier_file_sha256": hashlib.sha256(SELF.read_bytes()).hexdigest(),
        "producer_file_sha256": PINS["producer"],
        "producer_imported": False,
        "producer_executed": False,
        "postfreeze_C67_observation": {
            "producer_freeze_matching_artifact_count": 0,
            "nonconsumable_work_in_progress_observed": bool(c67_before or c67_after),
            "complete_consumable_bundle_present": False,
            "C67_bytes_consumed": False,
            "margin_status": "PENDING",
        },
        "result_file_sha256": PINS["result"],
        "result_object_sha256": PINS["result_object"],
        "output_file_sha256": {key: PINS[key] for key in ("tasks_out", "edges_out", "cells_out", "singleton_out", "report")},
        "recomputed_scope": expected_scope,
        "recomputed_large_classification_census": dict(sorted(class_census.items())),
        "recomputed_edge_endpoint_local_census": dict(sorted(edge_census.items())),
        "recomputed_singleton_classification_census": dict(sorted(classification.items())),
        "recomputed_singleton_witness_census": dict(sorted(witness.items())),
        "recomputed_singleton_structural_kind_census": dict(sorted(structural.items())),
        "C65_independent_static_audit": {
            "additional_binary_depth_from_C61": 6,
            "nominal_depth_from_C58_after_run": 18,
            "imports_exact_C41_router": True,
            "calls_C41_route_at_path": True,
            "calls_C41_disposition_family": True,
            "new_graph_cell_or_off_graph_slab_decider_definition_count": 0,
            "completed_v2_shard_artifact_count": 0,
            "capability_delta": "DYADIC_SUBDIVISION_PLUS_INHERITED_C41_ROUTER_REPLAY_ONLY",
            "depth24_recommended": False,
            "required_next": REQUIRED_NEXT,
        },
        "coherent_attacks": attacks,
        "authority_snapshot_before_sha256": authority_before,
        "authority_snapshot_after_sha256": authority_after,
        "runtime_or_canonical_written": False,
        "formal_credit": 0,
        "D02_gate_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    verification["object_sha256"] = h(verification)
    (OUT / VERIFY_FILE).write_bytes(enc(verification) + b"\n")
    return verification


def main() -> int:
    value = verify()
    print(json.dumps({"status": value["status"], "object_sha256": value["object_sha256"], "attacks": value["coherent_attacks"]["attack_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, TypeError, IndexError, SyntaxError) as error:
        print(f"FAIL_CLOSED:{type(error).__name__}:{error}", file=sys.stderr)
        raise SystemExit(2)
