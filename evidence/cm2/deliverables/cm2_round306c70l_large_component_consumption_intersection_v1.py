#!/usr/bin/env python3
"""C70-L read-only consumption intersection over the frozen large component.

This is deliberately a projection, not a promotion.  It intersects the C66
owner decision, C63 semantic-history map, C67 full named-margin decision, and
C68 direct-C41 endpoint-local flags for every edge.  For each large corridor
cell it then intersects all immediate incident edge decisions with C68's
whole-rooted-local flag.  Every output credit remains zero.
"""
from __future__ import annotations

import argparse
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
from typing import Any, Iterable

sys.dont_write_bytecode = True

SELF = Path(__file__).resolve()
ROOT = SELF.parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c70l_large_component_consumption_intersection"
SCHEMA = "cm2.round306c70l.large-component-consumption-intersection.v1"
EDGE_FILE = PREFIX + "_edge_ledger_v1.jsonl.gz"
CORRIDOR_FILE = PREFIX + "_corridor_ledger_v1.jsonl.gz"
RESULT_FILE = PREFIX + "_result_v1.json"

C63_RESULT = OUT / "cm2_round306c63l_scope_extension_result_v1.json"
C63_EDGE = OUT / "cm2_round306c63l_scope_extension_edge_replay_v1.jsonl.gz"
C63_VERIFY = OUT / "cm2_round306c63l_scope_extension_independent_verification_v1.json"
C66_RESULT = OUT / "cm2_round306c66l_global_owner_decider_authority_candidate_v1.json"
C66_EDGE = OUT / "cm2_round306c66l_global_owner_decider_edge_owner_decisions_v1.jsonl.gz"
C66_VERIFY = OUT / "cm2_round306c66l_global_owner_decider_independent_verification_v1.json"
C67_RESULT = OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_result_v1.json"
C67_EDGE = OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_edge_coverage_v1.jsonl.gz"
C67_CORRIDOR = OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_corridor_coverage_v1.jsonl.gz"
C67_VERIFY = OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_independent_verification_v1.json"
C68_RESULT = OUT / "cm2_round306c68l_blocker_crosswalk_result_v1.json"
C68_EDGE = OUT / "cm2_round306c68l_blocker_crosswalk_large_edge_blockers_v1.jsonl.gz"
C68_CORRIDOR = OUT / "cm2_round306c68l_blocker_crosswalk_large_corridor_cell_blockers_v1.jsonl.gz"
C68_VERIFY = OUT / "cm2_round306c68l_blocker_crosswalk_independent_verification_v1.json"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
CANON = OUT / "CM2_LATEST_STATUS.md"

PINS = {
    "C63_RESULT": "4795560dd4d70b6a1d42dde0cdf3e2c3f21f8c06e97aa776cd4fac4755ba5177",
    "C63_OBJECT": "676737c1f8ca935bbbf54b1d3aa7763d5178b56e93b1abc31fb7643f4a803135",
    "C63_EDGE": "94f0d22e2cdbaf18d39b3a4f0c31de453915a05feedbe3bec2b5a9cf1e3ace6b",
    "C63_VERIFY": "e070b6ea4553de806861c9e95bceccc0aa758b7944a319a14225a8676e6cf996",
    "C63_VERIFY_OBJECT": "f8e3dce7c5d1b826cabb46f9cb629b8b9a06d26f84b885de83be9639f5fa602b",
    "C66_RESULT": "2f546c2eda8bad0866d2d0d844c0c458c505be84d6997e4999be99b6c1eccb4b",
    "C66_OBJECT": "6e0f6982c19b15850ff24ae5d048140418641be73e59d9d9924e96ec4337ecd5",
    "C66_EDGE": "23ea97c5f021e2e3fc6512425b38a7d61fdaedb0f7543999b8f8ca67ebbdba4d",
    "C66_VERIFY": "17b9de74d71c2126774081d5720b3fab706c8063ce22caadaf87f9978c94170c",
    "C66_VERIFY_OBJECT": "29dfabb69287fdfe8a0b5d15469adef298cd198ff56e22f24c6e051a22c85b03",
    "C67_RESULT": "5b43ecb647958185859e987e5985660c660fb6a5ee7e422ae2748f96a880b8ac",
    "C67_OBJECT": "0e5b88cd4978661fdfad6bc508029f714e78a760f7164f4114cf540334b73fe1",
    "C67_EDGE": "84298c8283ae26685f34e5de24638257edb541f8d609f2a62f1b60d8285fbab8",
    "C67_CORRIDOR": "d28fc4ff49e7243e38e55997113d98fb0694eb3ed81f14ecbf5a051f1890684e",
    "C67_VERIFY": "0b8648f6bae78c7f0b632c762173d76de47fc3b3da034402bf10e22d6c825669",
    "C67_VERIFY_OBJECT": "fd8b0ce7d5414367e4107b018bed009bddb0574c3422abc635b853fb7f7b1dcf",
    "C68_RESULT": "81cf9b6e3fbf2330f747af6430410026406cad8a1a2eb862be974235b2b60f37",
    "C68_OBJECT": "551c28d03ee59e3fadc2b593dc2575acf911545ce0e6527f9ef0270dfc08d3b2",
    "C68_EDGE": "f2077eaf8f926408dc47eb7eb61ab8eab0e317584347407d3842bcc373b59cae",
    "C68_CORRIDOR": "dc61441b9a8836706a69874d8b60c14a7c1a7c99af6ebe88108ea2643c785c8f",
    "C68_VERIFY": "037dae421cd04132fef64aee95ae47b1a159c8d133b2b050039669afd682f818",
    "C68_VERIFY_OBJECT": "214d7294637aaa9140997a1ec1a0e3f11932f3f169647ae1e78f993ea23c39cc",
    "C53": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "CANON": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
}

PATHS = {
    "C63_RESULT": C63_RESULT, "C63_EDGE": C63_EDGE, "C63_VERIFY": C63_VERIFY,
    "C66_RESULT": C66_RESULT, "C66_EDGE": C66_EDGE, "C66_VERIFY": C66_VERIFY,
    "C67_RESULT": C67_RESULT, "C67_EDGE": C67_EDGE, "C67_CORRIDOR": C67_CORRIDOR, "C67_VERIFY": C67_VERIFY,
    "C68_RESULT": C68_RESULT, "C68_EDGE": C68_EDGE, "C68_CORRIDOR": C68_CORRIDOR, "C68_VERIFY": C68_VERIFY,
    "C53": C53, "CANON": CANON,
}


class FailClosed(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: Any) -> str:
    blob = value if isinstance(value, bytes) else canonical(value)
    return hashlib.sha256(blob).hexdigest()


def close_object(value: dict[str, Any], expected: str, label: str) -> None:
    body = dict(value)
    claimed = body.pop("object_sha256", None)
    need(claimed == expected and digest(body) == expected, label + "-object")


def identity(st: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size, st.st_mtime_ns)


def secure_bytes(path: Path, expected: str) -> tuple[bytes, tuple[int, int, int, int, int, int]]:
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "input-regular-single-link:" + path.name)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        opened = os.fstat(fd)
        need(identity(opened) == identity(before), "input-path-fd-identity:" + path.name)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after_fd = os.fstat(fd)
    finally:
        os.close(fd)
    after_path = path.lstat()
    need(identity(before) == identity(after_fd) == identity(after_path), "input-stable:" + path.name)
    blob = b"".join(chunks)
    need(len(blob) == before.st_size and digest(blob) == expected, "input-hash:" + path.name)
    return blob, identity(before)


def json_object(blob: bytes) -> dict[str, Any]:
    value = json.loads(blob)
    need(type(value) is dict, "json-object")
    return value


def ledger_rows(blob: bytes, descriptor: dict[str, Any], label: str) -> list[dict[str, Any]]:
    need(digest(blob) == descriptor["sha256"], label + "-descriptor-file-hash")
    with gzip.GzipFile(fileobj=io.BytesIO(blob), mode="rb") as stream:
        lines = stream.read().splitlines()
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for line in lines:
        row = json.loads(line)
        need(type(row) is dict and type(row.get("row_sha256")) is str, label + "-row-shape")
        body = dict(row)
        claimed = body.pop("row_sha256")
        need(digest(body) == claimed, label + "-row-hash")
        sequence.update((claimed + "\n").encode())
        rows.append(row)
    need(len(rows) == descriptor["row_count"], label + "-row-count")
    need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], label + "-sequence")
    return rows


def sequence_hash(values: Iterable[str]) -> str:
    h = hashlib.sha256()
    for value in values:
        h.update((value + "\n").encode())
    return h.hexdigest()


class Writer:
    def __init__(self, path: Path, order: str):
        self.path = path
        self.order = order
        self.fd: int | None = None
        self.raw: Any = None
        self.gz: gzip.GzipFile | None = None
        self.count = 0
        self.sequence = hashlib.sha256()

    def __enter__(self) -> "Writer":
        self.fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        self.raw = os.fdopen(self.fd, "wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, body: dict[str, Any]) -> dict[str, Any]:
        need("row_sha256" not in body, "writer-unclosed-row")
        row = dict(body)
        row["row_sha256"] = digest(body)
        assert self.gz is not None
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row["row_sha256"] + "\n").encode())
        self.count += 1
        return row

    def __exit__(self, kind: Any, value: Any, traceback: Any) -> None:
        assert self.gz is not None and self.raw is not None
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": digest(self.path.read_bytes()),
            "size": self.path.stat().st_size,
        }


def write_new(path: Path, blob: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        offset = 0
        while offset < len(blob):
            offset += os.write(fd, blob[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)


def edge_body(c63: dict[str, Any], c66: dict[str, Any], c67: dict[str, Any], c68: dict[str, Any]) -> dict[str, Any]:
    need(c66["C63_edge_replay_row_sha256"] == c63["row_sha256"], "edge-C66-C63-binding")
    need(c68["C63_history_edge_row_sha256"] == c63["row_sha256"], "edge-C68-C63-binding")
    need(c68["C66_owner_edge_row_sha256"] == c66["row_sha256"], "edge-C68-C66-binding")
    need(c67["C57_edge_row_sha256"] == c68["C57_edge_obligation_row_sha256"], "edge-C67-C68-C57-binding")
    for key in ("face_or_corner_id", "glue_kind"):
        need(c63[key] == c66[key] == c67[key] == c68[key], "edge-common-" + key)
    for key in ("component_index", "source_cell_id", "target_cell_id"):
        need(c67[key] == c68[key], "edge-common-" + key)
    owner = c66["closed_schema"] is True and c66["all_atom_owners_unique"] is True and c66["decision"] == "STRICT_FULL_DOMAIN_OWNER_VECTOR_AVAILABLE"
    history = c63["all_atom_semantic_mappings_complete"] is True and c63["all_atoms_in_complete_overlay_scope"] is True
    need(c68["owner_decision_pass"] is owner and c68["semantic_history_map_pass"] is history, "edge-C68-pass-replay")
    margin = c67["all_atoms_and_both_endpoint_occurrences_recomputed"] is True and c67["all_applicable_C36_named_margins_strict_whole_edge"] is True
    source_local = c68["source_direct_C41_local_frontier_beyond_collision1"] is True
    target_local = c68["target_direct_C41_local_frontier_beyond_collision1"] is True
    ready = owner and history and margin and source_local and target_local
    blockers: list[str] = []
    if not owner:
        blockers.append("C66_FULL_DOMAIN_OWNER_VECTOR_NOT_AVAILABLE")
    if not history:
        blockers.append("C63_SEMANTIC_HISTORY_MAPPING_INCOMPLETE")
    if not margin:
        blockers.append("C67_FULL_NAMED_MARGIN_NOT_STRICT_WHOLE_EDGE")
    if not source_local:
        blockers.append("C68_SOURCE_DIRECT_C41_LOCAL_FRONTIER_NOT_BEYOND_COLLISION1")
    if not target_local:
        blockers.append("C68_TARGET_DIRECT_C41_LOCAL_FRONTIER_NOT_BEYOND_COLLISION1")
    return {
        "schema": SCHEMA + ".edge-row",
        "C63_edge_replay_row_sha256": c63["row_sha256"],
        "C66_edge_owner_decision_row_sha256": c66["row_sha256"],
        "C67_edge_coverage_row_sha256": c67["row_sha256"],
        "C68_edge_blocker_row_sha256": c68["row_sha256"],
        "component_index": c67["component_index"],
        "source_cell_id": c67["source_cell_id"],
        "target_cell_id": c67["target_cell_id"],
        "face_or_corner_id": c67["face_or_corner_id"],
        "glue_kind": c67["glue_kind"],
        "source_seam": c67["glue_kind"] == "SOURCE_CHART_TRANSITION",
        "owner_pass": owner,
        "semantic_history_pass": history,
        "full_named_margin_pass": margin,
        "source_direct_C41_local_pass": source_local,
        "target_direct_C41_local_pass": target_local,
        "five_way_consumption_intersection_pass": ready,
        "decision": "READY_ZERO_CREDIT_CONSUMPTION_INTERSECTION" if ready else "BLOCKED_FAIL_CLOSED_CONSUMPTION_INTERSECTION",
        "remaining_blocker_codes": blockers,
        "formal_credit": 0,
        "handoff_credit": 0,
        "whole_cell_credit": 0,
        "D02_gate_credit": 0,
    }


def corridor_body(c67: dict[str, Any], c68: dict[str, Any], incident: list[dict[str, Any]]) -> dict[str, Any]:
    need(c67["C57_corridor_row_sha256"] == c68["C57_corridor_transport_row_sha256"], "corridor-C57-binding")
    for key in ("component_index", "cell_id"):
        need(c67[key] == c68[key], "corridor-common-" + key)
    need(len(incident) > 0 and len(incident) == c67["incident_edge_count"], "corridor-incident-count")
    input_margin_pass = all(row["full_named_margin_pass"] for row in incident)
    need(c67["all_incident_edges_strict"] is input_margin_pass, "corridor-C67-margin-aggregate")
    all_incident = all(row["five_way_consumption_intersection_pass"] for row in incident)
    local = c68["direct_C41_all_current_pending_tasks_beyond_collision1"] is True
    whole = c68["direct_C41_all_corridor_nodes_beyond_collision1"] is True
    need((not whole) or local, "corridor-whole-implies-current-local")
    ready = all_incident and whole
    blockers: list[str] = []
    if not all_incident:
        blockers.append("IMMEDIATE_INCIDENT_EDGE_CONSUMPTION_INTERSECTION_NOT_ALL_PASS")
    if not local:
        blockers.append("DIRECT_C41_CURRENT_CELL_LOCAL_FRONTIER_NOT_BEYOND_COLLISION1")
    if not whole:
        blockers.append("DIRECT_C41_WHOLE_ROOTED_CORRIDOR_NOT_BEYOND_COLLISION1")
    return {
        "schema": SCHEMA + ".corridor-row",
        "C67_corridor_coverage_row_sha256": c67["row_sha256"],
        "C68_corridor_blocker_row_sha256": c68["row_sha256"],
        "component_index": c68["component_index"],
        "cell_id": c68["cell_id"],
        "pair_index": c68["pair_index"],
        "incident_edge_count": len(incident),
        "incident_edge_C70_row_hash_sequence_sha256": sequence_hash(sorted(row["row_sha256"] for row in incident)),
        "incident_edge_pass_count": sum(row["five_way_consumption_intersection_pass"] for row in incident),
        "all_immediate_incident_edges_consumption_intersection_pass": all_incident,
        "direct_C41_current_cell_local_pass": local,
        "direct_C41_whole_rooted_corridor_local_pass": whole,
        "corridor_consumption_intersection_ready": ready,
        "decision": "READY_ZERO_CREDIT_CORRIDOR_INTERSECTION" if ready else "BLOCKED_FAIL_CLOSED_CORRIDOR_INTERSECTION",
        "remaining_blocker_codes": blockers,
        "formal_credit": 0,
        "handoff_credit": 0,
        "whole_cell_credit": 0,
        "D02_gate_credit": 0,
    }


def attack_self_test(projection: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, str] = {}
    for index, key in enumerate(sorted(projection)):
        altered = copy.deepcopy(projection)
        value = altered[key]
        if type(value) is bool:
            altered[key] = not value
        elif type(value) is int:
            altered[key] = value + 1
        else:
            altered[key] = str(value) + "__MUTATED"
        try:
            need(altered == projection, "projection:" + key)
        except FailClosed:
            checks[f"projection_{index:02d}_{key}"] = "FAIL_CLOSED"
        else:
            raise FailClosed("self-test-escaped:" + key)
    need(len(checks) >= 20, "self-test-at-least-20")
    return {"status": f"PASS_{len(checks)}_OF_{len(checks)}_PROJECTION_ATTACKS_FAIL_CLOSED", "attack_count": len(checks), "attacks": checks}


def build(directory: Path) -> dict[str, Any]:
    raw: dict[str, bytes] = {}
    initial_identities: dict[str, tuple[int, int, int, int, int, int]] = {}
    for key, path in PATHS.items():
        raw[key], initial_identities[key] = secure_bytes(path, PINS[key])

    c63_result = json_object(raw["C63_RESULT"]); close_object(c63_result, PINS["C63_OBJECT"], "C63")
    c63_verify = json_object(raw["C63_VERIFY"]); close_object(c63_verify, PINS["C63_VERIFY_OBJECT"], "C63-verify")
    c66_result = json_object(raw["C66_RESULT"]); close_object(c66_result, PINS["C66_OBJECT"], "C66")
    c66_verify = json_object(raw["C66_VERIFY"]); close_object(c66_verify, PINS["C66_VERIFY_OBJECT"], "C66-verify")
    c67_result = json_object(raw["C67_RESULT"]); close_object(c67_result, PINS["C67_OBJECT"], "C67")
    c67_verify = json_object(raw["C67_VERIFY"]); close_object(c67_verify, PINS["C67_VERIFY_OBJECT"], "C67-verify")
    c68_result = json_object(raw["C68_RESULT"]); close_object(c68_result, PINS["C68_OBJECT"], "C68")
    c68_verify = json_object(raw["C68_VERIFY"]); close_object(c68_verify, PINS["C68_VERIFY_OBJECT"], "C68-verify")

    need("PASS" in c63_verify["status"] and c63_verify["strict_boundary"]["formal_credit"] == 0, "C63-verify-pass")
    need(c66_verify["strict_boundary"]["consumption_ready"] is True and c66_verify["strict_boundary"]["installed_authority"] is False, "C66-consumption-ready-not-installed")
    need(c67_verify["numeric_reconstruction"]["edge_full"] == 491 and c67_verify["numeric_reconstruction"]["seam_full"] == 13, "C67-verified-coverage")
    need(
        "PASS" in c68_verify["status"]
        and c68_result["large_component_findings"]["local_frontier_gate"]
        == "DIRECT_C41_RECOMPUTE_350_OF_1044_ALL_CURRENT_TASKS_BEYOND_COLLISION1",
        "C68-verified-local",
    )

    c63_edges = ledger_rows(raw["C63_EDGE"], c63_result["ledgers"]["edge_replay"], "C63-edge")
    c66_edges = ledger_rows(raw["C66_EDGE"], c66_result["ledgers"]["edge_owner_decisions"], "C66-edge")
    c67_edges = ledger_rows(raw["C67_EDGE"], c67_result["ledgers"]["edge_coverage"], "C67-edge")
    c67_corridors = ledger_rows(raw["C67_CORRIDOR"], c67_result["ledgers"]["corridor_coverage"], "C67-corridor")
    c68_edges = ledger_rows(raw["C68_EDGE"], c68_result["ledgers"]["large_edge_blockers"], "C68-edge")
    c68_corridors = ledger_rows(raw["C68_CORRIDOR"], c68_result["ledgers"]["large_corridor_cell_blockers"], "C68-corridor")

    by63 = {row["face_or_corner_id"]: row for row in c63_edges}
    by66 = {row["face_or_corner_id"]: row for row in c66_edges}
    by68 = {row["face_or_corner_id"]: row for row in c68_edges}
    faces = {row["face_or_corner_id"] for row in c67_edges}
    need(len(by63) == len(by66) == len(by68) == len(faces) == 1042, "edge-unique-domain")
    need(set(by63) == set(by66) == set(by68) == faces, "edge-equal-domain")

    edge_rows: list[dict[str, Any]] = []
    edge_combinations: Counter[str] = Counter()
    edge_blockers: Counter[str] = Counter()
    component_edges: Counter[str] = Counter()
    seam: Counter[str] = Counter()
    with Writer(directory / EDGE_FILE, "C67_EDGE_ORDER") as writer:
        for c67 in c67_edges:
            face = c67["face_or_corner_id"]
            body = edge_body(by63[face], by66[face], c67, by68[face])
            row = writer.write(body)
            edge_rows.append(row)
            bits = "|".join(f"{key}={int(body[key])}" for key in ("owner_pass", "semantic_history_pass", "full_named_margin_pass", "source_direct_C41_local_pass", "target_direct_C41_local_pass"))
            edge_combinations[bits] += 1
            blocker_key = "NONE" if not body["remaining_blocker_codes"] else "|".join(body["remaining_blocker_codes"])
            edge_blockers[blocker_key] += 1
            component_edges[f"component_{body['component_index']}__{'ready' if body['five_way_consumption_intersection_pass'] else 'blocked'}"] += 1
            if body["source_seam"]:
                seam["total"] += 1
                seam["margin_pass"] += body["full_named_margin_pass"]
                seam["both_local_pass"] += body["source_direct_C41_local_pass"] and body["target_direct_C41_local_pass"]
                seam["ready"] += body["five_way_consumption_intersection_pass"]
    edge_descriptor = writer.descriptor()

    incident: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in edge_rows:
        incident[row["source_cell_id"]].append(row)
        incident[row["target_cell_id"]].append(row)
    by67c = {row["cell_id"]: row for row in c67_corridors}
    by68c = {row["cell_id"]: row for row in c68_corridors}
    need(len(by67c) == len(by68c) == len(incident) == 1044 and set(by67c) == set(by68c) == set(incident), "corridor-equal-domain")

    corridor_combinations: Counter[str] = Counter()
    corridor_blockers: Counter[str] = Counter()
    component_corridors: Counter[str] = Counter()
    corridor_degree: Counter[str] = Counter()
    corridor_rows: list[dict[str, Any]] = []
    with Writer(directory / CORRIDOR_FILE, "C68_LARGE_CORRIDOR_CELL_ORDER") as writer:
        for c68 in c68_corridors:
            cell = c68["cell_id"]
            body = corridor_body(by67c[cell], c68, incident[cell])
            row = writer.write(body)
            corridor_rows.append(row)
            bits = "|".join(f"{key}={int(body[key])}" for key in ("all_immediate_incident_edges_consumption_intersection_pass", "direct_C41_whole_rooted_corridor_local_pass", "direct_C41_current_cell_local_pass"))
            corridor_combinations[bits] += 1
            blocker_key = "NONE" if not body["remaining_blocker_codes"] else "|".join(body["remaining_blocker_codes"])
            corridor_blockers[blocker_key] += 1
            component_corridors[f"component_{body['component_index']}__{'ready' if body['corridor_consumption_intersection_ready'] else 'blocked'}"] += 1
            corridor_degree[str(body["incident_edge_count"])] += 1
    corridor_descriptor = writer.descriptor()

    projection = {
        "edge_count": len(edge_rows),
        "edge_owner_pass_count": sum(row["owner_pass"] for row in edge_rows),
        "edge_semantic_history_pass_count": sum(row["semantic_history_pass"] for row in edge_rows),
        "edge_full_named_margin_pass_count": sum(row["full_named_margin_pass"] for row in edge_rows),
        "edge_source_local_pass_count": sum(row["source_direct_C41_local_pass"] for row in edge_rows),
        "edge_target_local_pass_count": sum(row["target_direct_C41_local_pass"] for row in edge_rows),
        "edge_both_local_pass_count": sum(row["source_direct_C41_local_pass"] and row["target_direct_C41_local_pass"] for row in edge_rows),
        "edge_ready_count": sum(row["five_way_consumption_intersection_pass"] for row in edge_rows),
        "edge_blocked_count": sum(not row["five_way_consumption_intersection_pass"] for row in edge_rows),
        "source_seam_count": seam["total"],
        "source_seam_margin_pass_count": seam["margin_pass"],
        "source_seam_both_local_pass_count": seam["both_local_pass"],
        "source_seam_ready_count": seam["ready"],
        "corridor_count": len(corridor_rows),
        "corridor_all_incident_edge_pass_count": sum(row["all_immediate_incident_edges_consumption_intersection_pass"] for row in corridor_rows),
        "corridor_current_local_pass_count": sum(row["direct_C41_current_cell_local_pass"] for row in corridor_rows),
        "corridor_whole_rooted_local_pass_count": sum(row["direct_C41_whole_rooted_corridor_local_pass"] for row in corridor_rows),
        "corridor_ready_count": sum(row["corridor_consumption_intersection_ready"] for row in corridor_rows),
        "corridor_blocked_count": sum(not row["corridor_consumption_intersection_ready"] for row in corridor_rows),
        "formal_credit": 0,
        "handoff_credit": 0,
        "whole_cell_credit": 0,
        "D02_gate_credit": 0,
    }
    expected = {
        "edge_count": 1042, "edge_owner_pass_count": 1042, "edge_semantic_history_pass_count": 1042,
        "edge_full_named_margin_pass_count": 491, "edge_source_local_pass_count": 348,
        "edge_target_local_pass_count": 379, "edge_both_local_pass_count": 300,
        "edge_ready_count": 298, "edge_blocked_count": 744,
        "source_seam_count": 16, "source_seam_margin_pass_count": 13,
        "source_seam_both_local_pass_count": 0, "source_seam_ready_count": 0,
        "corridor_count": 1044, "corridor_all_incident_edge_pass_count": 248,
        "corridor_current_local_pass_count": 350, "corridor_whole_rooted_local_pass_count": 89,
        "corridor_ready_count": 73, "corridor_blocked_count": 971,
        "formal_credit": 0, "handoff_credit": 0, "whole_cell_credit": 0, "D02_gate_credit": 0,
    }
    need(projection == expected, "exact-projection")
    tests = attack_self_test(projection)

    for key, path in PATHS.items():
        _blob, final_identity = secure_bytes(path, PINS[key])
        need(final_identity == initial_identities[key], "final-input-identity:" + key)

    result: dict[str, Any] = {
        "schema": SCHEMA + ".result",
        "status": "PASS_EXACT_READ_ONLY_CONSUMPTION_INTERSECTION__298_OF_1042_EDGES__73_OF_1044_CORRIDORS_READY__ZERO_CREDIT",
        "input_byte_bindings": {key: PINS[key] for key in sorted(PATHS)},
        "semantic_contract": {
            "C63_history_predicate": "all_atom_semantic_mappings_complete AND all_atoms_in_complete_overlay_scope",
            "C63_legacy_owner_tie_predicate_not_reused": True,
            "C66_owner_predicate": "closed_schema AND all_atom_owners_unique AND STRICT_FULL_DOMAIN_OWNER_VECTOR_AVAILABLE",
            "edge_ready_predicate": "C66_owner AND C63_history AND C67_full_named_margin AND C68_source_local AND C68_target_local",
            "corridor_ready_predicate": "all_immediate_incident_edges_edge_ready AND C68_whole_rooted_local",
            "partial_edge_or_corridor_coverage_is_not_credit": True,
        },
        "summary": projection,
        "edge_boolean_intersection_census": dict(sorted(edge_combinations.items())),
        "edge_blocker_intersection_census": dict(sorted(edge_blockers.items())),
        "edge_component_census": dict(sorted(component_edges.items())),
        "corridor_boolean_intersection_census": dict(sorted(corridor_combinations.items())),
        "corridor_blocker_intersection_census": dict(sorted(corridor_blockers.items())),
        "corridor_component_census": dict(sorted(component_corridors.items())),
        "corridor_incident_degree_census": dict(sorted(corridor_degree.items(), key=lambda item: int(item[0]))),
        "ledgers": {"edge_consumption_intersection": edge_descriptor, "corridor_consumption_intersection": corridor_descriptor},
        "producer_self_test": tests,
        "strict_boundary": {
            "C66_candidate_installed_as_authority": False,
            "consumption_ready_means_only_this_frozen_projection": True,
            "runtime_or_canonical_written": False,
            "old_files_modified": False,
            "formal_credit": 0,
            "handoff_credit": 0,
            "whole_cell_credit": 0,
            "D02_gate_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": [
            "INDEPENDENT_NO_PRODUCER_REBUILD_AND_COHERENT_ATTACK_AUDIT",
            "KEEP_744_BLOCKED_EDGES_AND_971_BLOCKED_CORRIDORS_FAIL_CLOSED",
            "DO_NOT_PROMOTE_PARTIAL_INTERSECTION_TO_HANDOFF_FORMAL_OR_D02_CREDIT",
        ],
    }
    result["object_sha256"] = digest(result)
    write_new(directory / RESULT_FILE, canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = build(args.output_dir)
    print(json.dumps({"status": result["status"], "summary": result["summary"], "object_sha256": result["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
