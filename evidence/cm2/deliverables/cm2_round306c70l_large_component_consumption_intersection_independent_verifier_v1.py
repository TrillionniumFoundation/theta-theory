#!/usr/bin/env python3
"""Cold no-producer verifier for the C70-L large-component intersection.

The candidate producer is read only as opaque bytes for its SHA-256 binding.
It is never decoded as Python, imported, compiled, or executed.  This verifier
independently consumes the frozen C63/C66/C67/C68 byte ledgers, reconstructs
all 1,042 edge and 1,044 corridor decisions, and binds the actual gzip bytes,
sizes, row counts, row hashes, and row-hash sequences recorded by C70-L.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import io
import json
import os
import shutil
import stat
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Iterable

sys.dont_write_bytecode = True

SELF = Path(__file__).resolve()
ROOT = SELF.parents[1]
OUT = ROOT / "deliverables"
SCHEMA = "cm2.round306c70l.large-component-consumption-intersection.independent-verification.v1"

PRODUCER = OUT / "cm2_round306c70l_large_component_consumption_intersection_v1.py"
CANDIDATE_RESULT = OUT / "cm2_round306c70l_large_component_consumption_intersection_result_v1.json"
CANDIDATE_EDGE = OUT / "cm2_round306c70l_large_component_consumption_intersection_edge_ledger_v1.jsonl.gz"
CANDIDATE_CORRIDOR = OUT / "cm2_round306c70l_large_component_consumption_intersection_corridor_ledger_v1.jsonl.gz"
REJECTION = OUT / "cm2_round306c70l_large_component_consumption_intersection_rejection_v1.json"

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
    "PRODUCER": "12757adc50c13b38cf8d0971bfbc4a97edc336bad0c8e1a802c7b188fabd6da2",
    "CANDIDATE_RESULT": "6f981c2dced0c5dc97357d43660d9b40c733ada4c964a7322c7cb15fe4e413d8",
    "CANDIDATE_OBJECT": "86fb7b4d203e567e16e1b308456758ccd3a645382379bca4f656034af86febfd",
    "CANDIDATE_EDGE": "d440cbefccb0c3c49c6e35b2f42b73a0cef6ad7a83797a1d712e1c5dfeba0d78",
    "CANDIDATE_CORRIDOR": "dd9bad188879d1e63b2a7d7cd0d4abef91e8d975c84476619e69fa2057b9a693",
    "REJECTION": "6fd0cd001d2c9bfb2f9352626201aa6807965de0fd74c0cb48328b15a13a1318",
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
    "PRODUCER": PRODUCER, "CANDIDATE_RESULT": CANDIDATE_RESULT,
    "CANDIDATE_EDGE": CANDIDATE_EDGE, "CANDIDATE_CORRIDOR": CANDIDATE_CORRIDOR, "REJECTION": REJECTION,
    "C63_RESULT": C63_RESULT, "C63_EDGE": C63_EDGE, "C63_VERIFY": C63_VERIFY,
    "C66_RESULT": C66_RESULT, "C66_EDGE": C66_EDGE, "C66_VERIFY": C66_VERIFY,
    "C67_RESULT": C67_RESULT, "C67_EDGE": C67_EDGE, "C67_CORRIDOR": C67_CORRIDOR, "C67_VERIFY": C67_VERIFY,
    "C68_RESULT": C68_RESULT, "C68_EDGE": C68_EDGE, "C68_CORRIDOR": C68_CORRIDOR, "C68_VERIFY": C68_VERIFY,
    "C53": C53, "CANON": CANON,
}

RESULT_KEYS = {
    "schema", "status", "input_byte_bindings", "semantic_contract", "summary",
    "edge_boolean_intersection_census", "edge_blocker_intersection_census", "edge_component_census",
    "corridor_boolean_intersection_census", "corridor_blocker_intersection_census",
    "corridor_component_census", "corridor_incident_degree_census", "ledgers",
    "producer_self_test", "strict_boundary", "required_next", "object_sha256",
}
EDGE_KEYS = {
    "schema", "C63_edge_replay_row_sha256", "C66_edge_owner_decision_row_sha256",
    "C67_edge_coverage_row_sha256", "C68_edge_blocker_row_sha256", "component_index",
    "source_cell_id", "target_cell_id", "face_or_corner_id", "glue_kind", "source_seam",
    "owner_pass", "semantic_history_pass", "full_named_margin_pass",
    "source_direct_C41_local_pass", "target_direct_C41_local_pass",
    "five_way_consumption_intersection_pass", "decision", "remaining_blocker_codes",
    "formal_credit", "handoff_credit", "whole_cell_credit", "D02_gate_credit", "row_sha256",
}
CORRIDOR_KEYS = {
    "schema", "C67_corridor_coverage_row_sha256", "C68_corridor_blocker_row_sha256",
    "component_index", "cell_id", "pair_index", "incident_edge_count",
    "incident_edge_C70_row_hash_sequence_sha256", "incident_edge_pass_count",
    "all_immediate_incident_edges_consumption_intersection_pass",
    "direct_C41_current_cell_local_pass", "direct_C41_whole_rooted_corridor_local_pass",
    "corridor_consumption_intersection_ready", "decision", "remaining_blocker_codes",
    "formal_credit", "handoff_credit", "whole_cell_credit", "D02_gate_credit", "row_sha256",
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
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular-single-link:" + path.name)
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(identity(opened) == identity(before), "path-fd-identity:" + path.name)
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
    need(identity(before) == identity(after_fd) == identity(after_path), "TOCTOU:" + path.name)
    blob = b"".join(chunks)
    need(len(blob) == before.st_size and digest(blob) == expected, "file-hash:" + path.name)
    return blob, identity(before)


def json_object(blob: bytes) -> dict[str, Any]:
    value = json.loads(blob)
    need(type(value) is dict, "json-object")
    return value


def rows(blob: bytes, descriptor: dict[str, Any], label: str, expected_keys: set[str] | None = None) -> list[dict[str, Any]]:
    need(descriptor["sha256"] == digest(blob), label + "-actual-gzip-sha")
    need(descriptor["size"] == len(blob), label + "-actual-gzip-size")
    with gzip.GzipFile(fileobj=io.BytesIO(blob), mode="rb") as stream:
        lines = stream.read().splitlines()
    output: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for line in lines:
        row = json.loads(line)
        need(type(row) is dict and type(row.get("row_sha256")) is str, label + "-row-shape")
        if expected_keys is not None:
            need(set(row) == expected_keys, label + "-closed-row-schema")
        body = dict(row); claimed = body.pop("row_sha256")
        need(digest(body) == claimed, label + "-row-hash")
        sequence.update((claimed + "\n").encode())
        output.append(row)
    need(len(output) == descriptor["row_count"], label + "-row-count")
    need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], label + "-row-sequence")
    return output


def sequence_hash(values: Iterable[str]) -> str:
    h = hashlib.sha256()
    for value in values:
        h.update((value + "\n").encode())
    return h.hexdigest()


def expected_edge(c63: dict[str, Any], c66: dict[str, Any], c67: dict[str, Any], c68: dict[str, Any]) -> dict[str, Any]:
    need(c66["C63_edge_replay_row_sha256"] == c63["row_sha256"], "edge-C66-C63")
    need(c68["C63_history_edge_row_sha256"] == c63["row_sha256"], "edge-C68-C63")
    need(c68["C66_owner_edge_row_sha256"] == c66["row_sha256"], "edge-C68-C66")
    need(c67["C57_edge_row_sha256"] == c68["C57_edge_obligation_row_sha256"], "edge-C67-C68-C57")
    for key in ("face_or_corner_id", "glue_kind"):
        need(c63[key] == c66[key] == c67[key] == c68[key], "edge-common-" + key)
    for key in ("component_index", "source_cell_id", "target_cell_id"):
        need(c67[key] == c68[key], "edge-common-" + key)
    owner = c66["closed_schema"] is True and c66["all_atom_owners_unique"] is True and c66["decision"] == "STRICT_FULL_DOMAIN_OWNER_VECTOR_AVAILABLE"
    # This is intentionally the C63 semantic-history predicate.  The old
    # overall_owner_history_mapping_pass includes C63-era owner ties and must
    # not be reused after C66 independently supplies the owner decision.
    history = c63["all_atom_semantic_mappings_complete"] is True and c63["all_atoms_in_complete_overlay_scope"] is True
    need(c68["owner_decision_pass"] is owner and c68["semantic_history_map_pass"] is history, "C68-exact-owner-history-flags")
    margin = c67["all_atoms_and_both_endpoint_occurrences_recomputed"] is True and c67["all_applicable_C36_named_margins_strict_whole_edge"] is True
    source_local = c68["source_direct_C41_local_frontier_beyond_collision1"] is True
    target_local = c68["target_direct_C41_local_frontier_beyond_collision1"] is True
    ready = owner and history and margin and source_local and target_local
    blockers: list[str] = []
    if not owner: blockers.append("C66_FULL_DOMAIN_OWNER_VECTOR_NOT_AVAILABLE")
    if not history: blockers.append("C63_SEMANTIC_HISTORY_MAPPING_INCOMPLETE")
    if not margin: blockers.append("C67_FULL_NAMED_MARGIN_NOT_STRICT_WHOLE_EDGE")
    if not source_local: blockers.append("C68_SOURCE_DIRECT_C41_LOCAL_FRONTIER_NOT_BEYOND_COLLISION1")
    if not target_local: blockers.append("C68_TARGET_DIRECT_C41_LOCAL_FRONTIER_NOT_BEYOND_COLLISION1")
    body = {
        "schema": "cm2.round306c70l.large-component-consumption-intersection.v1.edge-row",
        "C63_edge_replay_row_sha256": c63["row_sha256"], "C66_edge_owner_decision_row_sha256": c66["row_sha256"],
        "C67_edge_coverage_row_sha256": c67["row_sha256"], "C68_edge_blocker_row_sha256": c68["row_sha256"],
        "component_index": c67["component_index"], "source_cell_id": c67["source_cell_id"],
        "target_cell_id": c67["target_cell_id"], "face_or_corner_id": c67["face_or_corner_id"],
        "glue_kind": c67["glue_kind"], "source_seam": c67["glue_kind"] == "SOURCE_CHART_TRANSITION",
        "owner_pass": owner, "semantic_history_pass": history, "full_named_margin_pass": margin,
        "source_direct_C41_local_pass": source_local, "target_direct_C41_local_pass": target_local,
        "five_way_consumption_intersection_pass": ready,
        "decision": "READY_ZERO_CREDIT_CONSUMPTION_INTERSECTION" if ready else "BLOCKED_FAIL_CLOSED_CONSUMPTION_INTERSECTION",
        "remaining_blocker_codes": blockers, "formal_credit": 0, "handoff_credit": 0,
        "whole_cell_credit": 0, "D02_gate_credit": 0,
    }
    return body | {"row_sha256": digest(body)}


def expected_corridor(c67: dict[str, Any], c68: dict[str, Any], incident: list[dict[str, Any]]) -> dict[str, Any]:
    need(c67["C57_corridor_row_sha256"] == c68["C57_corridor_transport_row_sha256"], "corridor-C57")
    need(c67["component_index"] == c68["component_index"] and c67["cell_id"] == c68["cell_id"], "corridor-common")
    need(len(incident) > 0 and len(incident) == c67["incident_edge_count"], "corridor-incident-count")
    need(c67["all_incident_edges_strict"] is all(row["full_named_margin_pass"] for row in incident), "corridor-C67-margin")
    all_incident = all(row["five_way_consumption_intersection_pass"] for row in incident)
    local = c68["direct_C41_all_current_pending_tasks_beyond_collision1"] is True
    whole = c68["direct_C41_all_corridor_nodes_beyond_collision1"] is True
    need((not whole) or local, "corridor-whole-implies-local")
    ready = all_incident and whole
    blockers: list[str] = []
    if not all_incident: blockers.append("IMMEDIATE_INCIDENT_EDGE_CONSUMPTION_INTERSECTION_NOT_ALL_PASS")
    if not local: blockers.append("DIRECT_C41_CURRENT_CELL_LOCAL_FRONTIER_NOT_BEYOND_COLLISION1")
    if not whole: blockers.append("DIRECT_C41_WHOLE_ROOTED_CORRIDOR_NOT_BEYOND_COLLISION1")
    body = {
        "schema": "cm2.round306c70l.large-component-consumption-intersection.v1.corridor-row",
        "C67_corridor_coverage_row_sha256": c67["row_sha256"], "C68_corridor_blocker_row_sha256": c68["row_sha256"],
        "component_index": c68["component_index"], "cell_id": c68["cell_id"], "pair_index": c68["pair_index"],
        "incident_edge_count": len(incident),
        "incident_edge_C70_row_hash_sequence_sha256": sequence_hash(sorted(row["row_sha256"] for row in incident)),
        "incident_edge_pass_count": sum(row["five_way_consumption_intersection_pass"] for row in incident),
        "all_immediate_incident_edges_consumption_intersection_pass": all_incident,
        "direct_C41_current_cell_local_pass": local,
        "direct_C41_whole_rooted_corridor_local_pass": whole,
        "corridor_consumption_intersection_ready": ready,
        "decision": "READY_ZERO_CREDIT_CORRIDOR_INTERSECTION" if ready else "BLOCKED_FAIL_CLOSED_CORRIDOR_INTERSECTION",
        "remaining_blocker_codes": blockers, "formal_credit": 0, "handoff_credit": 0,
        "whole_cell_credit": 0, "D02_gate_credit": 0,
    }
    return body | {"row_sha256": digest(body)}


def census(edge_rows: list[dict[str, Any]], corridor_rows: list[dict[str, Any]]) -> dict[str, Any]:
    edge_boolean: Counter[str] = Counter(); edge_blockers: Counter[str] = Counter(); edge_component: Counter[str] = Counter()
    for row in edge_rows:
        bits = "|".join(f"{key}={int(row[key])}" for key in ("owner_pass", "semantic_history_pass", "full_named_margin_pass", "source_direct_C41_local_pass", "target_direct_C41_local_pass"))
        edge_boolean[bits] += 1
        edge_blockers["NONE" if not row["remaining_blocker_codes"] else "|".join(row["remaining_blocker_codes"])] += 1
        edge_component[f"component_{row['component_index']}__{'ready' if row['five_way_consumption_intersection_pass'] else 'blocked'}"] += 1
    corridor_boolean: Counter[str] = Counter(); corridor_blockers: Counter[str] = Counter(); corridor_component: Counter[str] = Counter(); degree: Counter[str] = Counter()
    for row in corridor_rows:
        bits = "|".join(f"{key}={int(row[key])}" for key in ("all_immediate_incident_edges_consumption_intersection_pass", "direct_C41_whole_rooted_corridor_local_pass", "direct_C41_current_cell_local_pass"))
        corridor_boolean[bits] += 1
        corridor_blockers["NONE" if not row["remaining_blocker_codes"] else "|".join(row["remaining_blocker_codes"])] += 1
        corridor_component[f"component_{row['component_index']}__{'ready' if row['corridor_consumption_intersection_ready'] else 'blocked'}"] += 1
        degree[str(row["incident_edge_count"])] += 1
    summary = {
        "edge_count": len(edge_rows), "edge_owner_pass_count": sum(r["owner_pass"] for r in edge_rows),
        "edge_semantic_history_pass_count": sum(r["semantic_history_pass"] for r in edge_rows),
        "edge_full_named_margin_pass_count": sum(r["full_named_margin_pass"] for r in edge_rows),
        "edge_source_local_pass_count": sum(r["source_direct_C41_local_pass"] for r in edge_rows),
        "edge_target_local_pass_count": sum(r["target_direct_C41_local_pass"] for r in edge_rows),
        "edge_both_local_pass_count": sum(r["source_direct_C41_local_pass"] and r["target_direct_C41_local_pass"] for r in edge_rows),
        "edge_ready_count": sum(r["five_way_consumption_intersection_pass"] for r in edge_rows),
        "edge_blocked_count": sum(not r["five_way_consumption_intersection_pass"] for r in edge_rows),
        "source_seam_count": sum(r["source_seam"] for r in edge_rows),
        "source_seam_margin_pass_count": sum(r["source_seam"] and r["full_named_margin_pass"] for r in edge_rows),
        "source_seam_both_local_pass_count": sum(r["source_seam"] and r["source_direct_C41_local_pass"] and r["target_direct_C41_local_pass"] for r in edge_rows),
        "source_seam_ready_count": sum(r["source_seam"] and r["five_way_consumption_intersection_pass"] for r in edge_rows),
        "corridor_count": len(corridor_rows),
        "corridor_all_incident_edge_pass_count": sum(r["all_immediate_incident_edges_consumption_intersection_pass"] for r in corridor_rows),
        "corridor_current_local_pass_count": sum(r["direct_C41_current_cell_local_pass"] for r in corridor_rows),
        "corridor_whole_rooted_local_pass_count": sum(r["direct_C41_whole_rooted_corridor_local_pass"] for r in corridor_rows),
        "corridor_ready_count": sum(r["corridor_consumption_intersection_ready"] for r in corridor_rows),
        "corridor_blocked_count": sum(not r["corridor_consumption_intersection_ready"] for r in corridor_rows),
        "formal_credit": 0, "handoff_credit": 0, "whole_cell_credit": 0, "D02_gate_credit": 0,
    }
    return {
        "summary": summary, "edge_boolean_intersection_census": dict(sorted(edge_boolean.items())),
        "edge_blocker_intersection_census": dict(sorted(edge_blockers.items())),
        "edge_component_census": dict(sorted(edge_component.items())),
        "corridor_boolean_intersection_census": dict(sorted(corridor_boolean.items())),
        "corridor_blocker_intersection_census": dict(sorted(corridor_blockers.items())),
        "corridor_component_census": dict(sorted(corridor_component.items())),
        "corridor_incident_degree_census": dict(sorted(degree.items(), key=lambda x: int(x[0]))),
    }


def expect_rejected(label: str, action: Callable[[], None], checks: dict[str, str]) -> None:
    try:
        action()
    except (FailClosed, OSError, ValueError, KeyError, TypeError, IndexError, json.JSONDecodeError):
        checks[label] = "FAIL_CLOSED"
    else:
        raise FailClosed("attack-escaped:" + label)


def attacks(candidate: dict[str, Any], edge_rows: list[dict[str, Any]], corridor_rows: list[dict[str, Any]], projection: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, str] = {}
    def reject_equal(label: str, value: Any, expected: Any) -> None:
        expect_rejected(label, lambda: need(value == expected, label), checks)

    for index, key in enumerate(("edge_ready_count", "corridor_ready_count", "source_seam_ready_count", "formal_credit", "handoff_credit", "whole_cell_credit", "D02_gate_credit")):
        mutated = copy.deepcopy(projection["summary"]); mutated[key] += 1
        reject_equal(f"coherent_summary_{index:02d}_{key}", mutated, projection["summary"])
    for index, key in enumerate(("sha256", "size", "row_count", "row_hash_line_sequence_sha256")):
        mutated = copy.deepcopy(candidate["ledgers"]["edge_consumption_intersection"])
        mutated[key] = (mutated[key] + "x") if type(mutated[key]) is str else mutated[key] + 1
        reject_equal(f"edge_descriptor_{index:02d}_{key}", mutated, candidate["ledgers"]["edge_consumption_intersection"])
    mutated_result = copy.deepcopy(candidate); mutated_result["extra_field"] = "reclosed"; mutated_result["object_sha256"] = digest({k: v for k, v in mutated_result.items() if k != "object_sha256"})
    expect_rejected("closed_result_schema", lambda: need(set(mutated_result) == RESULT_KEYS, "closed-result"), checks)
    base_edge = copy.deepcopy(next(row for row in edge_rows if row["five_way_consumption_intersection_pass"]))
    for index, key in enumerate(("semantic_history_pass", "full_named_margin_pass", "source_direct_C41_local_pass", "target_direct_C41_local_pass")):
        mutated = copy.deepcopy(base_edge); mutated[key] = False; mutated["five_way_consumption_intersection_pass"] = False
        mutated["decision"] = "BLOCKED_FAIL_CLOSED_CONSUMPTION_INTERSECTION"; mutated["remaining_blocker_codes"] = ["COHERENT_ATTACK"]
        body = dict(mutated); body.pop("row_sha256"); mutated["row_sha256"] = digest(body)
        reject_equal(f"coherent_edge_{index:02d}_{key}", mutated, base_edge)
    base_corridor = copy.deepcopy(next(row for row in corridor_rows if row["corridor_consumption_intersection_ready"]))
    for index, key in enumerate(("all_immediate_incident_edges_consumption_intersection_pass", "direct_C41_whole_rooted_corridor_local_pass", "corridor_consumption_intersection_ready")):
        mutated = copy.deepcopy(base_corridor); mutated[key] = False; mutated["corridor_consumption_intersection_ready"] = False
        mutated["decision"] = "BLOCKED_FAIL_CLOSED_CORRIDOR_INTERSECTION"; mutated["remaining_blocker_codes"] = ["COHERENT_ATTACK"]
        body = dict(mutated); body.pop("row_sha256"); mutated["row_sha256"] = digest(body)
        reject_equal(f"coherent_corridor_{index:02d}_{key}", mutated, base_corridor)
    seam = next(row for row in edge_rows if row["source_seam"])
    mutated_seam = copy.deepcopy(seam); mutated_seam["five_way_consumption_intersection_pass"] = True
    body = dict(mutated_seam); body.pop("row_sha256"); mutated_seam["row_sha256"] = digest(body)
    reject_equal("coherent_source_seam_false_ready", mutated_seam, seam)
    old_history = 911
    reject_equal("C63_legacy_owner_history_not_semantic_history", old_history, 1042)

    stage = Path(tempfile.mkdtemp(prefix="cm2-c70l-verifier-attacks."))
    try:
        regular = stage / "regular"; regular.write_bytes(b"exact")
        symlink = stage / "symlink"; symlink.symlink_to(regular)
        expect_rejected("nofollow_symlink", lambda: secure_bytes(symlink, digest(b"exact")), checks)
        hardlink = stage / "hardlink"; os.link(regular, hardlink)
        expect_rejected("single_link", lambda: secure_bytes(regular, digest(b"exact")), checks)
        other = stage / "other"; other.write_bytes(b"wrong")
        expect_rejected("file_hash_substitution", lambda: secure_bytes(other, digest(b"exact")), checks)
    finally:
        shutil.rmtree(stage)
    need(len(checks) == 24, "exact-24-attacks")
    return {"status": "PASS_24_OF_24_COHERENT_AND_FILE_ATTACKS_FAIL_CLOSED", "attack_count": 24, "attacks": checks}


def verify(output: Path) -> dict[str, Any]:
    raw: dict[str, bytes] = {}; initial: dict[str, tuple[int, int, int, int, int, int]] = {}
    for key, path in PATHS.items():
        raw[key], initial[key] = secure_bytes(path, PINS[key])

    # PRODUCER remains opaque bytes.  No decode, AST parse, compile, import, or execution occurs.
    candidate = json_object(raw["CANDIDATE_RESULT"])
    need(set(candidate) == RESULT_KEYS, "candidate-closed-result-schema")
    close_object(candidate, PINS["CANDIDATE_OBJECT"], "candidate")
    rejection = json_object(raw["REJECTION"])
    need(rejection["status"] == "TERMINAL_REJECTED_ZERO_CREDIT_NEVER_CONSUME", "rejection-terminal")
    need(rejection["accepted_successor"]["producer_file_sha256"] == PINS["PRODUCER"], "rejection-current-source-binding")
    need(rejection["rejected_tuple"]["result_object_sha256"] == "5266c9404fddabcf78d8b64a0ec9f48b18c9f9b841425093dc2b19c05f44941d", "rejection-old-object")
    need(set(rejection["credit"].values()) == {0}, "rejection-zero-credit")

    objects: dict[str, dict[str, Any]] = {}
    for round_name in ("C63", "C66", "C67", "C68"):
        result = json_object(raw[round_name + "_RESULT"]); close_object(result, PINS[round_name + "_OBJECT"], round_name)
        verification = json_object(raw[round_name + "_VERIFY"]); close_object(verification, PINS[round_name + "_VERIFY_OBJECT"], round_name + "-verify")
        need("PASS" in verification["status"], round_name + "-verify-pass")
        objects[round_name] = result

    input_bindings = {key: PINS[key] for key in ("C63_RESULT", "C63_EDGE", "C63_VERIFY", "C66_RESULT", "C66_EDGE", "C66_VERIFY", "C67_RESULT", "C67_EDGE", "C67_CORRIDOR", "C67_VERIFY", "C68_RESULT", "C68_EDGE", "C68_CORRIDOR", "C68_VERIFY", "C53", "CANON")}
    need(candidate["input_byte_bindings"] == dict(sorted(input_bindings.items())), "candidate-input-bindings")

    c63 = rows(raw["C63_EDGE"], objects["C63"]["ledgers"]["edge_replay"], "C63-edge")
    c66 = rows(raw["C66_EDGE"], objects["C66"]["ledgers"]["edge_owner_decisions"], "C66-edge")
    c67 = rows(raw["C67_EDGE"], objects["C67"]["ledgers"]["edge_coverage"], "C67-edge")
    c67c = rows(raw["C67_CORRIDOR"], objects["C67"]["ledgers"]["corridor_coverage"], "C67-corridor")
    c68 = rows(raw["C68_EDGE"], objects["C68"]["ledgers"]["large_edge_blockers"], "C68-edge")
    c68c = rows(raw["C68_CORRIDOR"], objects["C68"]["ledgers"]["large_corridor_cell_blockers"], "C68-corridor")
    candidate_edges = rows(raw["CANDIDATE_EDGE"], candidate["ledgers"]["edge_consumption_intersection"], "candidate-edge", EDGE_KEYS)
    candidate_corridors = rows(raw["CANDIDATE_CORRIDOR"], candidate["ledgers"]["corridor_consumption_intersection"], "candidate-corridor", CORRIDOR_KEYS)

    by63 = {r["face_or_corner_id"]: r for r in c63}; by66 = {r["face_or_corner_id"]: r for r in c66}; by68 = {r["face_or_corner_id"]: r for r in c68}
    faces = {r["face_or_corner_id"] for r in c67}
    need(len(by63) == len(by66) == len(by68) == len(faces) == 1042 and set(by63) == set(by66) == set(by68) == faces, "edge-domain")
    expected_edges = [expected_edge(by63[r["face_or_corner_id"]], by66[r["face_or_corner_id"]], r, by68[r["face_or_corner_id"]]) for r in c67]
    need(candidate_edges == expected_edges, "all-1042-candidate-edge-rows-exact")
    semantic_count = sum(r["all_atom_semantic_mappings_complete"] is True and r["all_atoms_in_complete_overlay_scope"] is True for r in c63)
    legacy_overall_count = sum(r["overall_owner_history_mapping_pass"] is True for r in c63)
    need(semantic_count == 1042 and legacy_overall_count == 911, "C63-semantic-vs-legacy-owner-history-census")

    incident: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in expected_edges:
        incident[row["source_cell_id"]].append(row); incident[row["target_cell_id"]].append(row)
    by67c = {r["cell_id"]: r for r in c67c}; by68c = {r["cell_id"]: r for r in c68c}
    need(len(by67c) == len(by68c) == len(incident) == 1044 and set(by67c) == set(by68c) == set(incident), "corridor-domain")
    expected_corridors = [expected_corridor(by67c[r["cell_id"]], r, incident[r["cell_id"]]) for r in c68c]
    need(candidate_corridors == expected_corridors, "all-1044-candidate-corridor-rows-exact")

    projection = census(expected_edges, expected_corridors)
    for key, value in projection.items():
        need(candidate[key] == value, "candidate-census:" + key)
    summary = projection["summary"]
    expected_summary = {
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
    need(summary == expected_summary, "exact-summary")
    for row in expected_edges + expected_corridors:
        need(row["formal_credit"] == row["handoff_credit"] == row["whole_cell_credit"] == row["D02_gate_credit"] == 0, "all-row-credit-zero")
    need(candidate["strict_boundary"]["formal_credit"] == candidate["strict_boundary"]["handoff_credit"] == candidate["strict_boundary"]["whole_cell_credit"] == candidate["strict_boundary"]["D02_gate_credit"] == 0, "result-credit-zero")
    need(candidate["strict_boundary"]["runtime_or_canonical_written"] is False, "result-no-runtime-canonical-write")

    attack_result = attacks(candidate, expected_edges, expected_corridors, projection)
    for key, path in PATHS.items():
        _again, final = secure_bytes(path, PINS[key]); need(final == initial[key], "final-input-identity:" + key)

    verification: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PASS_COLD_NO_PRODUCER_EXACT_REBUILD__1042_EDGES_298_READY__1044_CORRIDORS_73_READY__SOURCE_SEAM_0_READY__24_OF_24_ATTACKS__ZERO_CREDIT",
        "candidate_producer_file_sha256": PINS["PRODUCER"],
        "candidate_result_file_sha256": PINS["CANDIDATE_RESULT"],
        "candidate_result_object_sha256": PINS["CANDIDATE_OBJECT"],
        "candidate_edge_actual_gzip_descriptor": candidate["ledgers"]["edge_consumption_intersection"],
        "candidate_corridor_actual_gzip_descriptor": candidate["ledgers"]["corridor_consumption_intersection"],
        "rejection_marker_file_sha256": PINS["REJECTION"],
        "semantic_history_audit": {
            "predicate": "C63.all_atom_semantic_mappings_complete AND C63.all_atoms_in_complete_overlay_scope",
            "semantic_history_pass_count": semantic_count,
            "legacy_overall_owner_history_pass_count_not_reused": legacy_overall_count,
            "C66_owner_is_separate_predicate": True,
        },
        "independent_rebuild": projection,
        "attacks": attack_result,
        "producer_source_imported_decoded_compiled_or_executed": False,
        "TOCTOU_and_single_link_checks_passed": True,
        "runtime_or_canonical_written": False,
        "C53_head_file_sha256": PINS["C53"],
        "canonical_file_sha256": PINS["CANON"],
        "formal_credit": 0,
        "handoff_credit": 0,
        "whole_cell_credit": 0,
        "D02_gate_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    verification["object_sha256"] = digest(verification)
    blob = canonical(verification) + b"\n"
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        offset = 0
        while offset < len(blob): offset += os.write(fd, blob[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT / "cm2_round306c70l_large_component_consumption_intersection_independent_verification_v1.json")
    args = parser.parse_args()
    result = verify(args.output)
    print(json.dumps({"status": result["status"], "object_sha256": result["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, TypeError, IndexError, json.JSONDecodeError) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
