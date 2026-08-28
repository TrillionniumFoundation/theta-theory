#!/usr/bin/env python3
"""Frozen no-producer global consumer successor for the C65/C69c/C70 bundle.

Every direct input is an inert, byte-pinned non-Python artifact.  This verifier
never reads, decodes, imports, compiles, or executes any producer source.  It
requires owner, semantic history, exact glue, both full sides, incidence, and
prefix/Kraft closure, but grants formal credit only when the public 76,832-row
global census has unresolved=0 and every successor-branch blocker is empty.

The currently frozen bundle has public unresolved=1,148.  C65 local terminals,
C69c source decisions, and C70 ready intersections therefore remain zero-credit
evidence only.  This verifier never installs authority or writes runtime or
canonical state.  With --emit it publishes only new append-only evidence files,
with the outer receipt written last.
"""

from __future__ import annotations

import argparse
import ast
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
from typing import Any, Callable, Iterable


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
OUT = SELF.parent

SCHEMA = "cm2.round306c72g.no-producer-global-consumer-successor.v1"
CONTRACT_SCHEMA = SCHEMA + ".contract"
VERIFICATION_SCHEMA = SCHEMA + ".verification"
SELF_TEST_SCHEMA = SCHEMA + ".self-test"
OUTER_SCHEMA = SCHEMA + ".outer-publication-receipt"

CONTRACT_NAME = "cm2_round306c72g_no_producer_global_consumer_successor_contract_v1.json"
VERIFICATION_NAME = "cm2_round306c72g_no_producer_global_consumer_successor_verification_v1.json"
SELF_TEST_NAME = "cm2_round306c72g_no_producer_global_consumer_successor_self_test_v1.json"
REPORT_NAME = "cm2_round306c72g_no_producer_global_consumer_successor_report_v1.md"
MANIFEST_NAME = "cm2_round306c72g_no_producer_global_consumer_successor_manifest_v1.sha256"
OUTER_NAME = "cm2_round306c72g_no_producer_global_consumer_successor_outer_receipt_v1.json"

CONTRACT_PATH = OUT / CONTRACT_NAME
CONTRACT_FILE_SHA256 = "6de59a039600f75d0b0d5722f9735fb2456f3b25b8a777df3fffef1f27e1749a"
CONTRACT_FILE_SIZE = 8708
CONTRACT_OBJECT_SHA256 = "5b2784b7f033ba4dde0a3d7f30af05ba4a71fb64bd6bf9fe34b64c48cc976b51"
EFFECTIVE_CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
UNIVERSE = 76_832
PUBLIC_CENSUS = {
    "CONNECTED_TO_KNOWN": 0,
    "EARLIEST_PREFIX_EXCLUDED": 75_388,
    "SOURCE_GRAZING_OR_CEMETERY": 0,
    "TYPED_EVENT_GRAPH": 296,
    "UNRESOLVED_R1648_CONTINUATION": 1_148,
    "total": UNIVERSE,
}
REQUIRED_CLOSURES = ("owner", "history", "glue", "two_sides", "incidence", "prefix_Kraft")
EXPECTED_INPUT_NAMES = frozenset({
    "C53_HEAD", "CANONICAL_STATUS", "C55C_VERIFY", "C55C_MANIFEST",
    "C55C_MANIFEST_SEAL", "C56_RESULT", "C56_VERIFY", "C56_MANIFEST",
    "C56_MANIFEST_SEAL", "C63_RESULT", "C63_VERIFY", "C63_MANIFEST",
    "C66_RESULT", "C66_VERIFY", "C66_MANIFEST", "C65_RESULT", "C65_VERIFY",
    "C65_POST_REPLAY", "C65_MANIFEST", "C65_OUTER", "C69_RESULT", "C69_VERIFY",
    "C69_MANIFEST", "C69_OUTER", "C70_RESULT", "C70_VERIFY", "C70_EDGE",
    "C70_CORRIDOR", "C70_MANIFEST", "C70_MANIFEST_SEAL", "C70_REJECTION",
})

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
MANIFEST_LINE = re.compile(r"([0-9a-f]{64})  ([^\r\n]+)\Z")

EDGE_KEYS = frozenset({
    "schema", "C63_edge_replay_row_sha256", "C66_edge_owner_decision_row_sha256",
    "C67_edge_coverage_row_sha256", "C68_edge_blocker_row_sha256", "component_index",
    "source_cell_id", "target_cell_id", "face_or_corner_id", "glue_kind", "source_seam",
    "owner_pass", "semantic_history_pass", "full_named_margin_pass",
    "source_direct_C41_local_pass", "target_direct_C41_local_pass",
    "five_way_consumption_intersection_pass", "decision", "remaining_blocker_codes",
    "formal_credit", "handoff_credit", "whole_cell_credit", "D02_gate_credit", "row_sha256",
})
CORRIDOR_KEYS = frozenset({
    "schema", "C67_corridor_coverage_row_sha256", "C68_corridor_blocker_row_sha256",
    "component_index", "cell_id", "pair_index", "incident_edge_count",
    "incident_edge_C70_row_hash_sequence_sha256", "incident_edge_pass_count",
    "all_immediate_incident_edges_consumption_intersection_pass",
    "direct_C41_current_cell_local_pass", "direct_C41_whole_rooted_corridor_local_pass",
    "corridor_consumption_intersection_ready", "decision", "remaining_blocker_codes",
    "formal_credit", "handoff_credit", "whole_cell_credit", "D02_gate_credit", "row_sha256",
})

ALLOWED_IMPORT_ROOTS = frozenset({
    "__future__", "argparse", "ast", "copy", "gzip", "hashlib", "io", "json", "os",
    "pathlib", "re", "shutil", "stat", "sys", "tempfile", "typing",
})
FORBIDDEN_CALL_NAMES = frozenset({"compile", "eval", "exec", "__import__"})
FORBIDDEN_ATTRIBUTE_ROOTS = frozenset({"importlib", "marshal", "pickle", "runpy", "subprocess"})


class Rejected(RuntimeError):
    """Fail-closed structural, semantic, or publication rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False,
    ).encode("ascii")


def bytes_sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def object_sha(value: Any) -> str:
    return bytes_sha(canonical(value))


def close_object(body: dict[str, Any], hash_key: str = "object_sha256") -> dict[str, Any]:
    value = copy.deepcopy(body)
    need(hash_key not in value, "close-hash-key-absent:" + hash_key)
    value[hash_key] = object_sha(value)
    return value


def verify_closed(value: Any, label: str, hash_key: str = "object_sha256") -> None:
    need(type(value) is dict, label + ":object")
    claimed = value.get(hash_key)
    need(type(claimed) is str and HEX64.fullmatch(claimed) is not None, label + ":hash-shape")
    body = copy.deepcopy(value)
    body.pop(hash_key)
    need(object_sha(body) == claimed, label + ":self-hash")


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise Rejected("duplicate-json-key:" + key)
        result[key] = value
    return result


def parse_json(raw: bytes, label: str, require_canonical: bool = True) -> Any:
    need(0 < len(raw) <= 8 << 20, label + ":bounded-nonempty")
    need(not raw.startswith(b"\xef\xbb\xbf"), label + ":no-bom")
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=reject_duplicate_pairs,
            parse_constant=lambda token: (_ for _ in ()).throw(
                Rejected(label + ":non-finite:" + token)
            ),
        )
    except Rejected:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Rejected(label + ":strict-json:" + str(exc)) from exc
    if require_canonical:
        need(raw == canonical(value) + b"\n", label + ":canonical-ascii-bytes")
    return value


def _identity(item: os.stat_result) -> tuple[int, ...]:
    return (
        item.st_dev, item.st_ino, item.st_mode, item.st_nlink, item.st_uid,
        item.st_gid, item.st_size, item.st_mtime_ns, item.st_ctime_ns,
    )


def secure_file(path: Path, expected_sha: str, expected_size: int) -> tuple[bytes, tuple[int, ...]]:
    before = path.lstat()
    need(
        stat.S_ISREG(before.st_mode) and before.st_nlink == 1
        and before.st_uid == os.getuid() and before.st_size == expected_size
        and before.st_mode & stat.S_IWOTH == 0,
        "secure-file-shape:" + path.name,
    )
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        need(_identity(opened) == _identity(before), "secure-file-path-fd:" + path.name)
        chunks: list[bytes] = []
        remaining = expected_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            need(bool(block), "secure-file-no-short-read:" + path.name)
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "secure-file-no-extra-byte:" + path.name)
        after_fd = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    after_path = path.lstat()
    need(_identity(before) == _identity(after_fd) == _identity(after_path), "secure-file-toctou:" + path.name)
    raw = b"".join(chunks)
    need(bytes_sha(raw) == expected_sha, "secure-file-sha:" + path.name)
    return raw, _identity(before)


def safe_workspace_path(relative: str) -> Path:
    need(type(relative) is str and relative != "" and "\x00" not in relative, "input-path-string")
    item = Path(relative)
    need(not item.is_absolute() and all(part not in ("", ".", "..") for part in item.parts), "input-path-relative-beneath")
    path = ROOT.joinpath(*item.parts)
    need(path.parent.resolve() == path.parent.absolute(), "input-parent-no-symlink")
    return path


def policy_scan_source(source: str, label: str) -> None:
    try:
        tree = ast.parse(source, filename=label)
    except SyntaxError as exc:
        raise Rejected(label + ":syntax") from exc
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                need(alias.name.split(".", 1)[0] in ALLOWED_IMPORT_ROOTS, label + ":import:" + alias.name)
        elif isinstance(node, ast.ImportFrom):
            need(node.level == 0 and node.module is not None, label + ":relative-import")
            need(node.module.split(".", 1)[0] in ALLOWED_IMPORT_ROOTS, label + ":from-import:" + str(node.module))
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                need(node.func.id not in FORBIDDEN_CALL_NAMES, label + ":dynamic-call:" + node.func.id)
            elif isinstance(node.func, ast.Attribute):
                root: ast.AST = node.func
                while isinstance(root, ast.Attribute):
                    root = root.value
                if isinstance(root, ast.Name):
                    need(root.id not in FORBIDDEN_ATTRIBUTE_ROOTS, label + ":dynamic-root:" + root.id)


def verify_contract_blob(raw: bytes) -> dict[str, Any]:
    need(len(raw) == CONTRACT_FILE_SIZE and bytes_sha(raw) == CONTRACT_FILE_SHA256, "contract-file-pin")
    value = parse_json(raw, "contract", require_canonical=False)
    verify_closed(value, "contract")
    need(value["object_sha256"] == CONTRACT_OBJECT_SHA256, "contract-object-pin")
    need(value["schema"] == CONTRACT_SCHEMA, "contract-schema")
    need(value["effective_checkpoint_object_sha256"] == EFFECTIVE_CHECKPOINT, "contract-checkpoint")
    need(value["exact_universe_size"] == UNIVERSE and value["public_global_census"] == PUBLIC_CENSUS, "contract-public-census")
    gate = value["positive_credit_gate"]
    need(gate["required_closures"] == list(REQUIRED_CLOSURES), "contract-closure-order")
    need(gate["public_global_unresolved_must_equal"] == 0, "contract-zero-unresolved-gate")
    need(all(gate[key] is True for key in (
        "all_required_closures_must_be_true", "formal_credit_iff_entire_conjunction_true",
        "local_terminal_decision_or_ready_projection_is_never_formal_credit",
        "successor_branch_blockers_must_be_empty",
    )), "contract-positive-gate")
    need(set(value["zero_credit_nonpromotion"].values()) == {0}, "contract-zero-credit")
    policy = value["producer_policy"]
    need(policy == {
        "direct_python_input_count": 0,
        "dynamic_execution_allowed": False,
        "producer_decode_compile_import_or_execution_allowed": False,
        "producer_files_are_manifest_text_only_transitive_names": True,
        "runtime_or_canonical_write_allowed": False,
    }, "contract-producer-policy")
    inputs = value["inputs"]
    need(type(inputs) is dict and frozenset(inputs) == EXPECTED_INPUT_NAMES, "contract-exact-input-domain")
    seen_paths: set[str] = set()
    for name, descriptor in inputs.items():
        need(type(descriptor) is dict and set(descriptor) == {"kind", "path", "sha256", "size"}, "input-descriptor:" + name)
        need(type(descriptor["kind"]) is str and descriptor["kind"] != "", "input-kind:" + name)
        need(type(descriptor["path"]) is str and descriptor["path"] not in seen_paths, "input-unique-path:" + name)
        seen_paths.add(descriptor["path"])
        safe_workspace_path(descriptor["path"])
        need(not descriptor["path"].endswith(".py"), "no-direct-python-input:" + name)
        need(type(descriptor["sha256"]) is str and HEX64.fullmatch(descriptor["sha256"]) is not None, "input-sha:" + name)
        need(type(descriptor["size"]) is int and 0 < descriptor["size"] <= 8 << 20, "input-size:" + name)
    return value


def read_input_bundle(contract: dict[str, Any]) -> tuple[dict[str, bytes], dict[str, tuple[int, ...]]]:
    raw: dict[str, bytes] = {}
    identities: dict[str, tuple[int, ...]] = {}
    for name in sorted(contract["inputs"]):
        descriptor = contract["inputs"][name]
        raw[name], identities[name] = secure_file(
            safe_workspace_path(descriptor["path"]), descriptor["sha256"], descriptor["size"],
        )
    return raw, identities


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise Rejected(label + ":ascii") from exc
    need(text.endswith("\n") and "\r" not in text, label + ":terminal-newline")
    result: dict[str, str] = {}
    for line in text.splitlines():
        match = MANIFEST_LINE.fullmatch(line)
        need(match is not None, label + ":line-shape")
        digest, path = match.groups()
        need(path not in result and path not in (".", "..") and "\x00" not in path, label + ":unique-path")
        result[path] = digest
    need(bool(result), label + ":nonempty")
    return result


def require_manifest_member(entries: dict[str, str], path: str, digest: str, label: str) -> None:
    need(entries.get(path) == digest, label + ":member:" + path)


def require_manifest_seal(raw: bytes, manifest_name: str, manifest_sha: str, label: str) -> None:
    entries = parse_manifest(raw, label)
    need(entries == {manifest_name: manifest_sha}, label + ":exact-seal")


def parse_objects(contract: dict[str, Any], raw: dict[str, bytes]) -> dict[str, dict[str, Any]]:
    objects: dict[str, dict[str, Any]] = {}
    for name, descriptor in contract["inputs"].items():
        if descriptor["kind"] in {"json", "json-seal"}:
            value = parse_json(raw[name], name)
            need(type(value) is dict, name + ":json-object")
            if name == "C53_HEAD":
                verify_closed(value, name, "authority_seal_object_sha256")
            elif name != "C70_REJECTION":
                verify_closed(value, name)
            objects[name] = value
    return objects


def parse_gzip_rows(
    raw: bytes, descriptor: dict[str, Any], expected_keys: frozenset[str], label: str,
) -> list[dict[str, Any]]:
    need(descriptor["sha256"] == bytes_sha(raw), label + ":descriptor-sha")
    need(descriptor["size"] == len(raw), label + ":descriptor-size")
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
            decompressed = stream.read(64 << 20)
            need(stream.read(1) == b"", label + ":bounded-decompression")
    except (OSError, EOFError) as exc:
        raise Rejected(label + ":gzip") from exc
    need(decompressed.endswith(b"\n"), label + ":terminal-newline")
    lines = decompressed.splitlines()
    result: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for index, line in enumerate(lines):
        row = parse_json(line + b"\n", f"{label}-row-{index}")
        need(type(row) is dict and frozenset(row) == expected_keys, label + ":closed-row-schema")
        verify_closed(row, label + ":row", "row_sha256")
        sequence.update((row["row_sha256"] + "\n").encode("ascii"))
        result.append(row)
    need(len(result) == descriptor["row_count"], label + ":row-count")
    need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], label + ":row-sequence")
    return result


def line_sequence_sha(values: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update((value + "\n").encode("ascii"))
    return digest.hexdigest()


def zero_credit(value: dict[str, Any], keys: Iterable[str], label: str) -> None:
    for key in keys:
        need(value[key] == 0, label + ":zero:" + key)


def validate_c70_rows(
    edges: list[dict[str, Any]], corridors: list[dict[str, Any]],
) -> dict[str, int]:
    need(len(edges) == 1_042 and len(corridors) == 1_044, "C70-row-domain-count")
    need(len({row["face_or_corner_id"] for row in edges}) == len(edges), "C70-unique-edge-domain")
    need(len({row["cell_id"] for row in corridors}) == len(corridors), "C70-unique-corridor-domain")

    incident: dict[str, list[dict[str, Any]]] = {}
    for row in edges:
        for key in (
            "owner_pass", "semantic_history_pass", "full_named_margin_pass",
            "source_direct_C41_local_pass", "target_direct_C41_local_pass",
            "five_way_consumption_intersection_pass", "source_seam",
        ):
            need(type(row[key]) is bool, "C70-edge-bool:" + key)
        need(row["owner_pass"] is True and row["semantic_history_pass"] is True, "C70-full-owner-history")
        ready = all(row[key] for key in (
            "owner_pass", "semantic_history_pass", "full_named_margin_pass",
            "source_direct_C41_local_pass", "target_direct_C41_local_pass",
        ))
        need(row["five_way_consumption_intersection_pass"] is ready, "C70-edge-ready-conjunction")
        need(type(row["remaining_blocker_codes"]) is list, "C70-edge-blocker-list")
        need(bool(row["remaining_blocker_codes"]) is (not ready), "C70-edge-blocker-iff")
        need(row["decision"] == (
            "READY_ZERO_CREDIT_CONSUMPTION_INTERSECTION" if ready
            else "BLOCKED_FAIL_CLOSED_CONSUMPTION_INTERSECTION"
        ), "C70-edge-decision")
        zero_credit(row, ("formal_credit", "handoff_credit", "whole_cell_credit", "D02_gate_credit"), "C70-edge")
        for cell_id in (row["source_cell_id"], row["target_cell_id"]):
            incident.setdefault(cell_id, []).append(row)

    need(len(incident) == 1_044, "C70-incidence-cell-domain")
    by_cell = {row["cell_id"]: row for row in corridors}
    need(set(by_cell) == set(incident), "C70-incidence-domain-equality")
    for cell_id, row in by_cell.items():
        for key in (
            "all_immediate_incident_edges_consumption_intersection_pass",
            "direct_C41_current_cell_local_pass", "direct_C41_whole_rooted_corridor_local_pass",
            "corridor_consumption_intersection_ready",
        ):
            need(type(row[key]) is bool, "C70-corridor-bool:" + key)
        attached = incident[cell_id]
        attached_ready = sum(item["five_way_consumption_intersection_pass"] for item in attached)
        all_attached = attached_ready == len(attached)
        need(row["incident_edge_count"] == len(attached), "C70-corridor-incident-count")
        need(row["incident_edge_pass_count"] == attached_ready, "C70-corridor-incident-pass-count")
        need(
            row["incident_edge_C70_row_hash_sequence_sha256"]
            == line_sequence_sha(sorted(item["row_sha256"] for item in attached)),
            "C70-corridor-incident-sequence",
        )
        need(row["all_immediate_incident_edges_consumption_intersection_pass"] is all_attached, "C70-corridor-all-incident")
        need((not row["direct_C41_whole_rooted_corridor_local_pass"]) or row["direct_C41_current_cell_local_pass"], "C70-whole-implies-current")
        ready = all_attached and row["direct_C41_whole_rooted_corridor_local_pass"]
        need(row["corridor_consumption_intersection_ready"] is ready, "C70-corridor-ready-conjunction")
        need(type(row["remaining_blocker_codes"]) is list, "C70-corridor-blocker-list")
        need(bool(row["remaining_blocker_codes"]) is (not ready), "C70-corridor-blocker-iff")
        need(row["decision"] == (
            "READY_ZERO_CREDIT_CORRIDOR_INTERSECTION" if ready
            else "BLOCKED_FAIL_CLOSED_CORRIDOR_INTERSECTION"
        ), "C70-corridor-decision")
        zero_credit(row, ("formal_credit", "handoff_credit", "whole_cell_credit", "D02_gate_credit"), "C70-corridor")

    summary = {
        "edge_count": len(edges),
        "edge_owner_pass_count": sum(row["owner_pass"] for row in edges),
        "edge_semantic_history_pass_count": sum(row["semantic_history_pass"] for row in edges),
        "edge_full_named_margin_pass_count": sum(row["full_named_margin_pass"] for row in edges),
        "edge_source_local_pass_count": sum(row["source_direct_C41_local_pass"] for row in edges),
        "edge_target_local_pass_count": sum(row["target_direct_C41_local_pass"] for row in edges),
        "edge_both_local_pass_count": sum(row["source_direct_C41_local_pass"] and row["target_direct_C41_local_pass"] for row in edges),
        "edge_ready_count": sum(row["five_way_consumption_intersection_pass"] for row in edges),
        "edge_blocked_count": sum(not row["five_way_consumption_intersection_pass"] for row in edges),
        "source_seam_count": sum(row["source_seam"] for row in edges),
        "source_seam_margin_pass_count": sum(row["source_seam"] and row["full_named_margin_pass"] for row in edges),
        "source_seam_both_local_pass_count": sum(row["source_seam"] and row["source_direct_C41_local_pass"] and row["target_direct_C41_local_pass"] for row in edges),
        "source_seam_ready_count": sum(row["source_seam"] and row["five_way_consumption_intersection_pass"] for row in edges),
        "corridor_count": len(corridors),
        "corridor_all_incident_edge_pass_count": sum(row["all_immediate_incident_edges_consumption_intersection_pass"] for row in corridors),
        "corridor_current_local_pass_count": sum(row["direct_C41_current_cell_local_pass"] for row in corridors),
        "corridor_whole_rooted_local_pass_count": sum(row["direct_C41_whole_rooted_corridor_local_pass"] for row in corridors),
        "corridor_ready_count": sum(row["corridor_consumption_intersection_ready"] for row in corridors),
        "corridor_blocked_count": sum(not row["corridor_consumption_intersection_ready"] for row in corridors),
        "formal_credit": 0,
        "handoff_credit": 0,
        "whole_cell_credit": 0,
        "D02_gate_credit": 0,
    }
    need(summary == {
        "edge_count": 1_042, "edge_owner_pass_count": 1_042,
        "edge_semantic_history_pass_count": 1_042, "edge_full_named_margin_pass_count": 491,
        "edge_source_local_pass_count": 348, "edge_target_local_pass_count": 379,
        "edge_both_local_pass_count": 300, "edge_ready_count": 298, "edge_blocked_count": 744,
        "source_seam_count": 16, "source_seam_margin_pass_count": 13,
        "source_seam_both_local_pass_count": 0, "source_seam_ready_count": 0,
        "corridor_count": 1_044, "corridor_all_incident_edge_pass_count": 248,
        "corridor_current_local_pass_count": 350, "corridor_whole_rooted_local_pass_count": 89,
        "corridor_ready_count": 73, "corridor_blocked_count": 971,
        "formal_credit": 0, "handoff_credit": 0, "whole_cell_credit": 0, "D02_gate_credit": 0,
    }, "C70-exact-row-summary")
    return summary


def validate_semantics(
    contract: dict[str, Any], objects: dict[str, dict[str, Any]], raw: dict[str, bytes],
    edges: list[dict[str, Any]], corridors: list[dict[str, Any]],
) -> dict[str, Any]:
    head = objects["C53_HEAD"]
    need(head["authority_role"] == "GLOBAL_COMPOSITE", "C53-global-role")
    need(head["post_seal_effective_checkpoint_object_sha256"] == EFFECTIVE_CHECKPOINT, "C53-checkpoint")
    need(head["formal_scope"]["D02_four_class_after"] == contract["public_global_census"] == PUBLIC_CENSUS, "C53-public-census")
    need(head["formal_scope"]["D02_gate_credit"] == 0, "C53-zero-D02")
    need(head["formal_scope"]["after"]["logical_pending_task_count"] == 33_638, "C53-D02-pending-tasks")
    need(head["semantic_commit"]["this_predecessor_keyed_global_head_is_only_semantic_commit"] is True, "C53-semantic-head")

    c55 = objects["C55C_VERIFY"]
    need(c55["schema"].endswith(".verification"), "C55c-schema")
    need(c55["status"] == "FAIL_CLOSED_GLOBAL_STRICT_DECIDER_NOT_ENABLED", "C55c-fail-closed")
    zero_credit(c55, ("formal_credit", "D02_credit", "terminal_credit"), "C55c")
    need(c55["positive_terminal_enabled"] is False and c55["result_is_authority"] is False, "C55c-no-positive-authority")
    need(c55["input_state"]["independent_A_census"] == PUBLIC_CENSUS, "C55c-A-census")
    cross = c55["input_state"]["A_B_cross_reconstruction"]
    need(all(cross[key] is True for key in (
        "component_row_crosswalk_agrees", "exact_physical_box_crosswalk_agrees", "full_census_agrees",
    )), "C55c-glue-cross-reconstruction")
    need(cross["ordinary_cell_crosswalk_count"] == 1_724, "C55c-ordinary-crosswalk")
    need(c55["producer_independence"] == {
        "A_or_B_producer_executed": False,
        "A_or_B_producer_imported": False,
        "dynamic_execution_primitives": [],
    }, "C55c-no-producer")

    c56r, c56v = objects["C56_RESULT"], objects["C56_VERIFY"]
    for value, label in ((c56r, "C56-result"), (c56v, "C56-verify")):
        need(value["census"] == PUBLIC_CENSUS, label + ":census")
        zero_credit(value, ("formal_credit", "D02_credit"), label)
        need(value["positive_terminal_enabled"] is False, label + ":positive-disabled")
    need(c56r["unresolved_zero"] is False and c56r["strict_decider_eligible"] is False, "C56-unresolved")
    need(c56v["projection_row_count"] == UNIVERSE and c56v["every_row_byte_for_byte_independently_reconstructed"] is True, "C56-full-B-side")
    need(c56v["independence"]["upstream_producer_imported"] is False and c56v["independence"]["upstream_producer_executed"] is False, "C56-no-producer")

    c63r, c63v = objects["C63_RESULT"], objects["C63_VERIFY"]
    need(c63v["status"].startswith("PASS_NO_PRODUCER_EXACT_15009_SCOPE_EXTENSION_REPLAY"), "C63-pass")
    need(c63v["independence"]["producer_imported_or_executed"] is False, "C63-no-producer")
    need(c63v["verified"] == c63r["scope"], "C63-result-verify-scope")
    need(c63v["verified"]["atom_replay_count"] == c63v["verified"]["atom_semantic_mapping_complete_count"] == 13_103, "C63-atom-history")
    need(c63v["verified"]["edge_replay_count"] == c63v["verified"]["edge_semantic_mapping_complete_count"] == 1_042, "C63-edge-history")
    need(c63v["verified"]["overlay_incidence_count"] == 26_206, "C63-overlay-incidence")
    zero_credit(c63v["strict_boundary"], ("formal_credit", "D02_gate_credit"), "C63")

    c66r, c66v = objects["C66_RESULT"], objects["C66_VERIFY"]
    need(c66v["status"].startswith("PASS_COLD_NO_PRODUCER_FULL_REPLAY"), "C66-pass")
    need(c66v["independence"]["producer_imported_or_executed"] is False, "C66-no-producer")
    need(c66v["verified"]["query_domain_edge_count"] == c66v["verified"]["full_unique_owner_edge_count"] == 1_042, "C66-edge-owner")
    need(c66v["verified"]["atom_domain_count"] == c66v["verified"]["full_unique_owner_atom_count"] == 13_103, "C66-atom-owner")
    need(c66v["verified"]["query_partition_overlap_count"] == c66v["verified"]["atom_partition_overlap_count"] == 0, "C66-owner-partition")
    need(c66v["strict_boundary"]["consumption_ready"] is True and c66v["strict_boundary"]["installed_authority"] is False, "C66-consumption-only")
    zero_credit(c66v["strict_boundary"], ("formal_credit", "D02_gate_credit"), "C66")
    need(c66r["authority_status"] == "CANDIDATE_NOT_INSTALLED", "C66-not-installed")

    c65r, c65v = objects["C65_RESULT"], objects["C65_VERIFY"]
    c65p, c65o = objects["C65_POST_REPLAY"], objects["C65_OUTER"]
    zero_credit(c65r, ("formal_credit", "D02_gate_credit", "whole_parent_credit"), "C65-result")
    zero_credit(c65v, ("formal_credit", "D02_gate_credit"), "C65-verify")
    zero_credit(c65p, ("formal_credit", "D02_gate_credit", "whole_parent_credit"), "C65-post")
    zero_credit(c65o, ("formal_credit", "D02_gate_credit", "whole_parent_credit"), "C65-outer")
    need(c65r["candidate_is_authority"] is False and c65v["candidate_is_authority"] is False, "C65-not-authority")
    need(c65r["runtime_canonical_pointer_or_seal_writes"] is False and c65o["runtime_canonical_pointer_or_seal_writes"] is False, "C65-no-runtime-write")
    need(c65r["invariants"]["all_20879_source_partitions_prefix_free_and_Kraft_conserved"] is True, "C65-prefix-Kraft")
    need(c65r["invariants"]["all_12_replacement_parents_preserve_prefix_Kraft_via_C61_base_certificate_and_exact_source_partitions"] is True, "C65-parent-prefix-Kraft")
    need(c65r["invariants"]["C69b_or_C69c_capability_injected"] is False, "C65-no-C69-injection")
    need(c65v["invariants"]["C69b_or_C69c_consumed"] is False, "C65-no-C69-consumption")
    need(c65v["coverage"]["whole_pairs_terminal"] == 0 and c65r["coverage"]["whole_sources_terminal"] == 2_943, "C65-local-terminal-only")
    need(c65r["coverage"]["complete_parent_disposition_census"] == {
        "COLLISION2_HANDOFF": 167_255, "COLLISION3_READY": 0, "STRICT_TERMINAL": 219_072,
    }, "C65-parent-census")
    need(c65v["independence"]["C65_programs_imported_or_executed"] is False, "C65-no-program-exec")
    need(c65p["verification_file_sha256"] == contract["inputs"]["C65_VERIFY"]["sha256"], "C65-post-verification-pin")
    need(c65p["verification_object_sha256"] == c65v["object_sha256"], "C65-post-object-pin")
    need(c65o["manifest_file_sha256"] == contract["inputs"]["C65_MANIFEST"]["sha256"], "C65-outer-manifest-pin")
    need(c65o["outer_receipt_published_last"] is True and c65o["manifest_members_recaptured_after_publication"] is True, "C65-publication-closure")

    c69r, c69v, c69o = objects["C69_RESULT"], objects["C69_VERIFY"], objects["C69_OUTER"]
    zero_credit(c69r["strict_boundary"], ("formal_credit", "D02_gate_credit", "whole_parent_credit"), "C69-result")
    zero_credit(c69v, ("formal_credit", "D02_gate_credit", "whole_parent_credit"), "C69-verify")
    zero_credit(c69o, ("formal_credit", "D02_gate_credit", "whole_parent_credit"), "C69-outer")
    need(c69r["strict_boundary"]["decisions_are_terminal_dispositions"] is False, "C69-decisions-nonterminal")
    need(c69r["strict_boundary"]["candidate_is_installed_authority"] is False, "C69-not-authority")
    need(c69r["scope"] == {
        "D02_gate_credit": 0, "decision_count": 2_356, "eligible_full_face_count": 2_356,
        "formal_credit": 0, "full_face_numeric_blocker_count": 0, "input_task_count": 20_879,
        "layer_A_count": 2_355, "layer_B_count": 1, "layer_C_count": 0,
        "parametric_cover_row_count": 2, "total_blocker_count": 18_523,
    }, "C69-exact-scope")
    need(c69r["global_invariants"]["additional_dyadic_source_disposition_depth_used"] is False, "C69-no-extra-dyadic-depth")
    need(all(
        value is True for key, value in c69r["global_invariants"].items()
        if key != "additional_dyadic_source_disposition_depth_used"
    ), "C69-all-positive-global-invariants")
    need(c69v["producer_executed"] is False and c69v["producer_imported"] is False, "C69-no-producer-exec")
    need(c69v["producer_or_wrapper_source_read_or_decoded"] is False and c69v["self_source_policy_scan_pass"] is True, "C69-no-producer-read")
    need(c69v["actual_descriptors"]["decisions"]["row_count"] == 2_356 and c69v["actual_descriptors"]["blockers"]["row_count"] == 18_523, "C69-descriptor-counts")
    need(c69o["published_artifact_captures"]["cm2_round306c69c_descriptor_repair_supersession_independent_manifest_v1.sha256"]["sha256"] == contract["inputs"]["C69_MANIFEST"]["sha256"], "C69-outer-manifest-pin")
    need(c69o["publication_O_EXCL_no_replace"] is True, "C69-no-replace-publication")

    c70r, c70v, c70x = objects["C70_RESULT"], objects["C70_VERIFY"], objects["C70_REJECTION"]
    zero_credit(c70r["strict_boundary"], ("formal_credit", "handoff_credit", "whole_cell_credit", "D02_gate_credit"), "C70-result")
    zero_credit(c70v, ("formal_credit", "handoff_credit", "whole_cell_credit", "D02_gate_credit"), "C70-verify")
    need(c70r["strict_boundary"]["C66_candidate_installed_as_authority"] is False, "C70-owner-not-promoted")
    need(c70r["strict_boundary"]["consumption_ready_means_only_this_frozen_projection"] is True, "C70-ready-projection-only")
    need(c70v["producer_source_imported_decoded_compiled_or_executed"] is False, "C70-no-producer")
    need(c70v["attacks"]["attack_count"] == 24 and c70v["attacks"]["status"].startswith("PASS_24_OF_24"), "C70-upstream-attacks")
    need(c70x["status"] == "TERMINAL_REJECTED_ZERO_CREDIT_NEVER_CONSUME", "C70-old-tuple-rejected")
    need(set(c70x["credit"].values()) == {0}, "C70-rejection-zero-credit")
    summary = validate_c70_rows(edges, corridors)
    need(c70r["summary"] == summary and c70v["independent_rebuild"]["summary"] == summary, "C70-row-summary-bindings")
    need(c70r["semantic_contract"]["partial_edge_or_corridor_coverage_is_not_credit"] is True, "C70-partial-not-credit")

    manifests = {
        name: parse_manifest(raw[name], name)
        for name in ("C55C_MANIFEST", "C56_MANIFEST", "C63_MANIFEST", "C66_MANIFEST", "C65_MANIFEST", "C69_MANIFEST", "C70_MANIFEST")
    }
    require_manifest_member(manifests["C55C_MANIFEST"], Path(contract["inputs"]["C55C_VERIFY"]["path"]).name, contract["inputs"]["C55C_VERIFY"]["sha256"], "C55c-manifest")
    require_manifest_member(manifests["C56_MANIFEST"], Path(contract["inputs"]["C56_RESULT"]["path"]).name, contract["inputs"]["C56_RESULT"]["sha256"], "C56-manifest")
    require_manifest_member(manifests["C56_MANIFEST"], Path(contract["inputs"]["C56_VERIFY"]["path"]).name, contract["inputs"]["C56_VERIFY"]["sha256"], "C56-manifest")
    require_manifest_member(manifests["C63_MANIFEST"], Path(contract["inputs"]["C63_RESULT"]["path"]).name, contract["inputs"]["C63_RESULT"]["sha256"], "C63-manifest")
    require_manifest_member(manifests["C63_MANIFEST"], Path(contract["inputs"]["C63_VERIFY"]["path"]).name, contract["inputs"]["C63_VERIFY"]["sha256"], "C63-manifest")
    require_manifest_member(manifests["C66_MANIFEST"], Path(contract["inputs"]["C66_RESULT"]["path"]).name, contract["inputs"]["C66_RESULT"]["sha256"], "C66-manifest")
    require_manifest_member(manifests["C66_MANIFEST"], Path(contract["inputs"]["C66_VERIFY"]["path"]).name, contract["inputs"]["C66_VERIFY"]["sha256"], "C66-manifest")
    for name in ("C65_RESULT", "C65_VERIFY", "C65_POST_REPLAY"):
        alias = contract["inputs"][name]["path"].replace("/", "__")
        require_manifest_member(manifests["C65_MANIFEST"], alias, contract["inputs"][name]["sha256"], "C65-manifest")
    for name in ("C69_RESULT", "C69_VERIFY"):
        require_manifest_member(manifests["C69_MANIFEST"], contract["inputs"][name]["path"], contract["inputs"][name]["sha256"], "C69-manifest")
    for name in ("C70_RESULT", "C70_VERIFY", "C70_EDGE", "C70_CORRIDOR", "C70_REJECTION"):
        require_manifest_member(manifests["C70_MANIFEST"], Path(contract["inputs"][name]["path"]).name, contract["inputs"][name]["sha256"], "C70-manifest")
    require_manifest_seal(raw["C55C_MANIFEST_SEAL"], Path(contract["inputs"]["C55C_MANIFEST"]["path"]).name, contract["inputs"]["C55C_MANIFEST"]["sha256"], "C55c-manifest-seal")
    require_manifest_seal(raw["C56_MANIFEST_SEAL"], Path(contract["inputs"]["C56_MANIFEST"]["path"]).name, contract["inputs"]["C56_MANIFEST"]["sha256"], "C56-manifest-seal")
    require_manifest_seal(raw["C70_MANIFEST_SEAL"], Path(contract["inputs"]["C70_MANIFEST"]["path"]).name, contract["inputs"]["C70_MANIFEST"]["sha256"], "C70-manifest-seal")

    closures = {
        "owner": c66v["verified"]["full_unique_owner_edge_count"] == 1_042 and summary["edge_owner_pass_count"] == 1_042,
        "history": c63v["verified"]["edge_semantic_mapping_complete_count"] == 1_042 and summary["edge_semantic_history_pass_count"] == 1_042,
        "glue": all(cross[key] is True for key in ("component_row_crosswalk_agrees", "exact_physical_box_crosswalk_agrees", "full_census_agrees")),
        "two_sides": c56v["projection_row_count"] == UNIVERSE and c55["input_state"]["independent_A_census"]["total"] == UNIVERSE,
        "incidence": summary["edge_count"] == 1_042 and summary["corridor_count"] == 1_044 and len({row["cell_id"] for row in corridors}) == 1_044,
        "prefix_Kraft": c65r["invariants"]["all_20879_source_partitions_prefix_free_and_Kraft_conserved"] is True and c69r["global_invariants"]["all_decision_source_paths_prefix_free"] is True and c69r["global_invariants"]["all_decision_source_volume_and_Kraft_preserved"] is True,
    }
    need(tuple(closures) == REQUIRED_CLOSURES and all(closures.values()), "all-six-structural-closures")

    blockers = {
        "public_global_unresolved": PUBLIC_CENSUS["UNRESOLVED_R1648_CONTINUATION"],
        "C65_collision2_handoff_leaves": c65r["coverage"]["complete_parent_disposition_census"]["COLLISION2_HANDOFF"],
        "C65_whole_pairs_terminal": c65v["coverage"]["whole_pairs_terminal"],
        "C69c_nonterminal_decisions": c69r["scope"]["decision_count"],
        "C69c_remaining_blockers": c69r["scope"]["total_blocker_count"],
        "C70_blocked_edges": summary["edge_blocked_count"],
        "C70_blocked_corridors": summary["corridor_blocked_count"],
        "C70_unready_source_seams": summary["source_seam_count"] - summary["source_seam_ready_count"],
    }
    public_zero = blockers["public_global_unresolved"] == 0
    branch_clear = all(blockers[key] == 0 for key in (
        "C65_collision2_handoff_leaves", "C69c_nonterminal_decisions", "C69c_remaining_blockers",
        "C70_blocked_edges", "C70_blocked_corridors", "C70_unready_source_seams",
    ))
    formal_eligible = all(closures.values()) and public_zero and branch_clear
    need(formal_eligible is False, "current-bundle-must-remain-zero-credit")

    return {
        "closures": closures,
        "public_global_census": copy.deepcopy(PUBLIC_CENSUS),
        "public_global_unresolved_zero": public_zero,
        "successor_branch_blockers": blockers,
        "successor_branch_blockers_empty": branch_clear,
        "formal_credit_eligible": formal_eligible,
        "formal_credit": 0,
        "D02_gate_credit": 0,
        "D02_formal_pending_task_count": 33_638,
        "D02_unlock_capability": False,
        "nonpromotion": {
            "C65_local_terminal": "ZERO_CREDIT_ONLY",
            "C69c_source_decision": "ZERO_CREDIT_ONLY",
            "C70_ready_intersection": "ZERO_CREDIT_ONLY",
        },
        "C70_summary": summary,
    }


def expect_rejected(label: str, action: Callable[[], None], results: dict[str, str]) -> None:
    try:
        action()
    except (Rejected, OSError, ValueError, KeyError, TypeError, IndexError, json.JSONDecodeError, gzip.BadGzipFile):
        results[label] = "FAIL_CLOSED"
    else:
        raise Rejected("attack-escaped:" + label)


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def run_attacks(
    contract: dict[str, Any], objects: dict[str, dict[str, Any]], raw: dict[str, bytes],
    edges: list[dict[str, Any]], corridors: list[dict[str, Any]],
) -> dict[str, Any]:
    results: dict[str, str] = {}

    def object_attack(label: str, changes: list[tuple[str, tuple[str, ...], Any]]) -> None:
        mutated = copy.deepcopy(objects)
        for name, path, replacement in changes:
            set_path(mutated[name], path, replacement)
        expect_rejected(label, lambda: validate_semantics(contract, mutated, raw, edges, corridors), results)

    object_attack("coherent_00_public_unresolved_forged_zero", [
        ("C53_HEAD", ("formal_scope", "D02_four_class_after", "UNRESOLVED_R1648_CONTINUATION"), 0),
        ("C55C_VERIFY", ("input_state", "independent_A_census", "UNRESOLVED_R1648_CONTINUATION"), 0),
        ("C56_RESULT", ("census", "UNRESOLVED_R1648_CONTINUATION"), 0),
        ("C56_VERIFY", ("census", "UNRESOLVED_R1648_CONTINUATION"), 0),
    ])
    changed_contract = copy.deepcopy(contract)
    changed_contract["public_global_census"]["UNRESOLVED_R1648_CONTINUATION"] = 0
    changed_contract["object_sha256"] = object_sha({key: value for key, value in changed_contract.items() if key != "object_sha256"})
    changed_contract_raw = canonical(changed_contract) + b"\n"
    expect_rejected("coherent_01_contract_reclosed_unresolved_zero", lambda: verify_contract_blob(changed_contract_raw), results)
    object_attack("coherent_02_owner_domain_truncated", [("C66_VERIFY", ("verified", "full_unique_owner_edge_count"), 1_041)])
    object_attack("coherent_03_owner_false_installation", [
        ("C66_VERIFY", ("strict_boundary", "installed_authority"), True),
        ("C66_RESULT", ("authority_status",), "INSTALLED"),
    ])
    object_attack("coherent_04_history_domain_truncated", [("C63_VERIFY", ("verified", "edge_semantic_mapping_complete_count"), 1_041)])
    object_attack("coherent_05_glue_crosswalk_false", [("C55C_VERIFY", ("input_state", "A_B_cross_reconstruction", "component_row_crosswalk_agrees"), False)])
    object_attack("coherent_06_second_side_truncated", [("C56_VERIFY", ("projection_row_count",), 76_831)])
    object_attack("coherent_07_incidence_summary_retarget", [
        ("C70_RESULT", ("summary", "edge_ready_count"), 299),
        ("C70_VERIFY", ("independent_rebuild", "summary", "edge_ready_count"), 299),
    ])
    object_attack("coherent_08_C65_prefix_Kraft_false", [("C65_RESULT", ("invariants", "all_20879_source_partitions_prefix_free_and_Kraft_conserved"), False)])
    object_attack("coherent_09_C69_prefix_Kraft_false", [("C69_RESULT", ("global_invariants", "all_decision_source_volume_and_Kraft_preserved"), False)])
    object_attack("coherent_10_C65_formal_credit_promotion", [
        ("C65_RESULT", ("formal_credit",), 1), ("C65_VERIFY", ("formal_credit",), 1),
        ("C65_POST_REPLAY", ("formal_credit",), 1), ("C65_OUTER", ("formal_credit",), 1),
    ])
    object_attack("coherent_11_C65_D02_credit_promotion", [
        ("C65_RESULT", ("D02_gate_credit",), 1), ("C65_VERIFY", ("D02_gate_credit",), 1),
        ("C65_POST_REPLAY", ("D02_gate_credit",), 1), ("C65_OUTER", ("D02_gate_credit",), 1),
    ])
    object_attack("coherent_12_C65_whole_parent_promotion", [
        ("C65_RESULT", ("whole_parent_credit",), 1), ("C65_POST_REPLAY", ("whole_parent_credit",), 1),
        ("C65_OUTER", ("whole_parent_credit",), 1),
    ])
    object_attack("coherent_13_C65_C69_injection_claim", [("C65_RESULT", ("invariants", "C69b_or_C69c_capability_injected"), True)])
    object_attack("coherent_14_C65_whole_pair_terminal_claim", [("C65_VERIFY", ("coverage", "whole_pairs_terminal"), 1)])
    object_attack("coherent_15_C69_decision_terminal_claim", [("C69_RESULT", ("strict_boundary", "decisions_are_terminal_dispositions"), True)])
    object_attack("coherent_16_C69_formal_credit_promotion", [
        ("C69_RESULT", ("strict_boundary", "formal_credit"), 1),
        ("C69_RESULT", ("scope", "formal_credit"), 1),
        ("C69_VERIFY", ("formal_credit",), 1), ("C69_OUTER", ("formal_credit",), 1),
    ])
    object_attack("coherent_17_C69_blocker_retarget", [("C69_RESULT", ("scope", "total_blocker_count"), 18_522)])
    object_attack("coherent_18_C69_producer_execution", [("C69_VERIFY", ("producer_executed",), True)])
    object_attack("coherent_19_C70_formal_credit_promotion", [("C70_RESULT", ("strict_boundary", "formal_credit"), 1), ("C70_VERIFY", ("formal_credit",), 1)])
    object_attack("coherent_20_C70_handoff_credit_promotion", [("C70_RESULT", ("strict_boundary", "handoff_credit"), 1), ("C70_VERIFY", ("handoff_credit",), 1)])
    object_attack("coherent_21_C70_whole_cell_credit_promotion", [("C70_RESULT", ("strict_boundary", "whole_cell_credit"), 1), ("C70_VERIFY", ("whole_cell_credit",), 1)])
    object_attack("coherent_22_C70_D02_credit_promotion", [("C70_RESULT", ("strict_boundary", "D02_gate_credit"), 1), ("C70_VERIFY", ("D02_gate_credit",), 1)])

    seam_rows = copy.deepcopy(edges)
    seam = next(row for row in seam_rows if row["source_seam"])
    for key in ("owner_pass", "semantic_history_pass", "full_named_margin_pass", "source_direct_C41_local_pass", "target_direct_C41_local_pass", "five_way_consumption_intersection_pass"):
        seam[key] = True
    seam["decision"] = "READY_ZERO_CREDIT_CONSUMPTION_INTERSECTION"
    seam["remaining_blocker_codes"] = []
    seam["row_sha256"] = object_sha({key: value for key, value in seam.items() if key != "row_sha256"})
    expect_rejected("coherent_23_C70_source_seam_false_ready", lambda: validate_semantics(contract, objects, raw, seam_rows, corridors), results)

    corridor_rows = copy.deepcopy(corridors)
    corridor_rows[0]["incident_edge_count"] += 1
    corridor_rows[0]["row_sha256"] = object_sha({key: value for key, value in corridor_rows[0].items() if key != "row_sha256"})
    expect_rejected("coherent_24_C70_incident_count_retarget", lambda: validate_semantics(contract, objects, raw, edges, corridor_rows), results)
    object_attack("coherent_25_C70_owner_authority_promotion", [("C70_RESULT", ("strict_boundary", "C66_candidate_installed_as_authority"), True)])
    object_attack("coherent_26_C55_producer_import", [("C55C_VERIFY", ("producer_independence", "A_or_B_producer_imported"), True)])
    object_attack("coherent_27_C56_producer_execution", [("C56_VERIFY", ("independence", "upstream_producer_executed"), True)])
    object_attack("coherent_28_runtime_write_claim", [("C65_RESULT", ("runtime_canonical_pointer_or_seal_writes",), True)])
    object_attack("coherent_29_head_D02_credit_promotion", [("C53_HEAD", ("formal_scope", "D02_gate_credit"), 1)])
    object_attack("coherent_30_rejected_C70_tuple_revival", [("C70_REJECTION", ("status",), "ACCEPTED")])

    dropped_manifest = b"\n".join(raw["C70_MANIFEST"].splitlines()[1:]) + b"\n"
    expect_rejected("negative_31_manifest_member_drop", lambda: require_manifest_member(parse_manifest(dropped_manifest, "attack-manifest"), Path(contract["inputs"]["C70_CORRIDOR"]["path"]).name, contract["inputs"]["C70_CORRIDOR"]["sha256"], "attack-manifest"), results)
    retargeted_seal = ("0" * 64 + "  " + Path(contract["inputs"]["C70_MANIFEST"]["path"]).name + "\n").encode("ascii")
    expect_rejected("negative_32_manifest_seal_retarget", lambda: require_manifest_seal(retargeted_seal, Path(contract["inputs"]["C70_MANIFEST"]["path"]).name, contract["inputs"]["C70_MANIFEST"]["sha256"], "attack-seal"), results)
    changed_pin_contract = copy.deepcopy(contract)
    changed_pin_contract["inputs"]["C70_EDGE"]["sha256"] = "0" * 64
    changed_pin_contract["object_sha256"] = object_sha({key: value for key, value in changed_pin_contract.items() if key != "object_sha256"})
    expect_rejected("negative_33_contract_input_pin_retarget", lambda: verify_contract_blob(canonical(changed_pin_contract) + b"\n"), results)

    stage = Path(tempfile.mkdtemp(prefix="cm2-c72g-attacks."))
    try:
        regular = stage / "regular"
        regular.write_bytes(b"exact")
        symlink = stage / "symlink"
        symlink.symlink_to(regular)
        expect_rejected("negative_34_symlink", lambda: secure_file(symlink, bytes_sha(b"exact"), 5), results)
        hardlink = stage / "hardlink"
        os.link(regular, hardlink)
        expect_rejected("negative_35_hardlink", lambda: secure_file(regular, bytes_sha(b"exact"), 5), results)
        wrong = stage / "wrong"
        wrong.write_bytes(b"wrong")
        expect_rejected("negative_36_byte_substitution", lambda: secure_file(wrong, bytes_sha(b"exact"), 5), results)
    finally:
        shutil.rmtree(stage)

    expect_rejected("negative_37_importlib_policy", lambda: policy_scan_source("import importlib\n", "attack-importlib"), results)
    expect_rejected("negative_38_dynamic_exec_policy", lambda: policy_scan_source("exec('x')\n", "attack-exec"), results)
    need(len(results) == 39 and set(results.values()) == {"FAIL_CLOSED"}, "exact-39-attacks")
    return {
        "schema": SELF_TEST_SCHEMA,
        "status": "PASS_39_OF_39_COHERENT_SEMANTIC_FILE_AND_POLICY_ATTACKS_FAIL_CLOSED",
        "attack_count": 39,
        "attacks": dict(sorted(results.items())),
        "producer_source_read_decoded_compiled_imported_or_executed": False,
        "runtime_or_canonical_written": False,
        "formal_credit": 0,
        "D02_gate_credit": 0,
    }


def build_evidence() -> tuple[dict[str, Any], dict[str, Any], dict[str, bytes], dict[str, tuple[int, ...]], dict[str, Any]]:
    policy_scan_source(SELF.read_text(encoding="utf-8"), "self")
    contract_raw, contract_identity = secure_file(CONTRACT_PATH, CONTRACT_FILE_SHA256, CONTRACT_FILE_SIZE)
    contract = verify_contract_blob(contract_raw)
    raw, identities = read_input_bundle(contract)
    objects = parse_objects(contract, raw)
    c70r, c70v = objects["C70_RESULT"], objects["C70_VERIFY"]
    edge_descriptor = c70r["ledgers"]["edge_consumption_intersection"]
    corridor_descriptor = c70r["ledgers"]["corridor_consumption_intersection"]
    need(edge_descriptor == c70v["candidate_edge_actual_gzip_descriptor"], "C70-edge-descriptor-cross-pin")
    need(corridor_descriptor == c70v["candidate_corridor_actual_gzip_descriptor"], "C70-corridor-descriptor-cross-pin")
    edges = parse_gzip_rows(raw["C70_EDGE"], edge_descriptor, EDGE_KEYS, "C70-edge")
    corridors = parse_gzip_rows(raw["C70_CORRIDOR"], corridor_descriptor, CORRIDOR_KEYS, "C70-corridor")
    projection = validate_semantics(contract, objects, raw, edges, corridors)
    self_test = close_object(run_attacks(contract, objects, raw, edges, corridors))

    recaptured_contract, recaptured_contract_identity = secure_file(CONTRACT_PATH, CONTRACT_FILE_SHA256, CONTRACT_FILE_SIZE)
    need(recaptured_contract == contract_raw and recaptured_contract_identity == contract_identity, "contract-terminal-byte-replay")
    recaptured, recaptured_identities = read_input_bundle(contract)
    need(recaptured == raw and recaptured_identities == identities, "input-terminal-byte-replay")

    verification = close_object({
        "schema": VERIFICATION_SCHEMA,
        "status": "PASS_FROZEN_NO_PRODUCER_GLOBAL_CONSUMER__6_OF_6_STRUCTURAL_CLOSURES__PUBLIC_UNRESOLVED_1148__ZERO_CREDIT",
        "contract_file_sha256": CONTRACT_FILE_SHA256,
        "contract_object_sha256": CONTRACT_OBJECT_SHA256,
        "verifier_file_sha256": bytes_sha(SELF.read_bytes()),
        "effective_checkpoint_object_sha256": EFFECTIVE_CHECKPOINT,
        "direct_input_count": len(contract["inputs"]),
        "direct_input_pin_map_object_sha256": object_sha(contract["inputs"]),
        "all_direct_inputs_non_python": True,
        "all_direct_inputs_terminal_byte_replayed": True,
        "producer_source_read_decoded_compiled_imported_or_executed": False,
        "dynamic_execution_primitives": [],
        "runtime_or_canonical_written": False,
        "structural_closure": projection["closures"],
        "public_global_census": projection["public_global_census"],
        "public_global_unresolved_zero": projection["public_global_unresolved_zero"],
        "successor_branch_blockers": projection["successor_branch_blockers"],
        "successor_branch_blockers_empty": projection["successor_branch_blockers_empty"],
        "formal_credit_eligible": projection["formal_credit_eligible"],
        "formal_credit": 0,
        "D02_gate_credit": 0,
        "D02_formal_pending_task_count": projection["D02_formal_pending_task_count"],
        "D02_unlock_capability": False,
        "nonpromotion": projection["nonpromotion"],
        "C70_row_level_rebuild": projection["C70_summary"],
        "self_test_object_sha256": self_test["object_sha256"],
        "CM2": "NO-GO_FOR_CLAIM",
    })
    return verification, self_test, raw, identities, contract


def write_no_replace(path: Path, raw: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        0o644,
    )
    try:
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            need(written > 0, "publication-short-write:" + path.name)
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def report_bytes(verification: dict[str, Any], self_test: dict[str, Any]) -> bytes:
    blockers = verification["successor_branch_blockers"]
    text = f"""# Round 306c72g no-producer global consumer successor v1

Status: **frozen, fail-closed, zero credit**.

- All six structural inputs are closed: owner, history, glue, both sides, incidence, and prefix/Kraft.
- Public global census remains `{blockers['public_global_unresolved']}` unresolved out of `76,832`; therefore `formal_credit=0` and `D02_gate_credit=0`.
- C65 local terminals, C69c source decisions, and C70 ready intersections are evidence only and were not promoted.
- Remaining incomparable branch blockers: C65 collision-2 handoff leaves `{blockers['C65_collision2_handoff_leaves']}`, C69c blockers `{blockers['C69c_remaining_blockers']}` plus `{blockers['C69c_nonterminal_decisions']}` nonterminal decisions, C70 blocked edges/corridors `{blockers['C70_blocked_edges']}/{blockers['C70_blocked_corridors']}`, and `{blockers['C70_unready_source_seams']}` unready source seams.
- D02 remains locked with `{verification['D02_formal_pending_task_count']}` formal tasks; this consumer cannot unlock D02.
- Direct inputs: `{verification['direct_input_count']}` byte/size/path pins, all non-Python and terminal-byte replayed.
- Negative testing: `{self_test['attack_count']}` of `{self_test['attack_count']}` coherent semantic, file, and execution-policy attacks failed closed.
"""
    return text.encode("utf-8")


def manifest_bytes(entries: list[tuple[str, bytes]]) -> bytes:
    seen: set[str] = set()
    lines: list[str] = []
    for path, raw in entries:
        need(path not in seen and "\n" not in path and "\r" not in path, "publication-manifest-path")
        seen.add(path)
        lines.append(bytes_sha(raw) + "  " + path)
    return ("\n".join(lines) + "\n").encode("ascii")


def emit() -> dict[str, Any]:
    verification, self_test, upstream_raw, _identities, contract = build_evidence()
    verification_raw = canonical(verification) + b"\n"
    self_test_raw = canonical(self_test) + b"\n"
    report_raw = report_bytes(verification, self_test)
    source_raw = SELF.read_bytes()
    contract_raw = CONTRACT_PATH.read_bytes()

    artifact_entries: list[tuple[str, bytes]] = [
        ("deliverables/" + CONTRACT_NAME, contract_raw),
        ("deliverables/" + SELF.name, source_raw),
    ]
    artifact_entries.extend(
        (contract["inputs"][name]["path"], upstream_raw[name]) for name in sorted(contract["inputs"])
    )
    artifact_entries.extend([
        ("deliverables/" + VERIFICATION_NAME, verification_raw),
        ("deliverables/" + SELF_TEST_NAME, self_test_raw),
        ("deliverables/" + REPORT_NAME, report_raw),
    ])
    manifest_raw = manifest_bytes(artifact_entries)

    write_no_replace(OUT / VERIFICATION_NAME, verification_raw)
    write_no_replace(OUT / SELF_TEST_NAME, self_test_raw)
    write_no_replace(OUT / REPORT_NAME, report_raw)
    write_no_replace(OUT / MANIFEST_NAME, manifest_raw)

    captures: dict[str, Any] = {}
    for name, expected_raw in (
        (VERIFICATION_NAME, verification_raw), (SELF_TEST_NAME, self_test_raw),
        (REPORT_NAME, report_raw), (MANIFEST_NAME, manifest_raw),
    ):
        actual_raw, identity = secure_file(OUT / name, bytes_sha(expected_raw), len(expected_raw))
        need(actual_raw == expected_raw, "postpublication-artifact-byte-replay:" + name)
        captures[name] = {"sha256": bytes_sha(actual_raw), "size": len(actual_raw), "identity": list(identity)}

    recaptured_upstream, recaptured_identities = read_input_bundle(contract)
    need(recaptured_upstream == upstream_raw, "postpublication-upstream-byte-replay")
    outer = close_object({
        "schema": OUTER_SCHEMA,
        "status": "PASS_OUTER_RECEIPT_PUBLISHED_LAST__FULL_INPUT_AND_ARTIFACT_BYTE_REPLAY__ZERO_CREDIT",
        "manifest_filename": MANIFEST_NAME,
        "manifest_file_sha256": bytes_sha(manifest_raw),
        "manifest_entry_count": len(artifact_entries),
        "manifest_entry_path_sequence_sha256": line_sequence_sha(path for path, _raw in artifact_entries),
        "published_artifact_captures": captures,
        "direct_input_count": len(contract["inputs"]),
        "direct_input_identity_count": len(recaptured_identities),
        "direct_inputs_recaptured_after_publication": True,
        "outer_receipt_published_last": True,
        "publication_O_EXCL_no_replace": True,
        "producer_source_read_decoded_compiled_imported_or_executed": False,
        "runtime_or_canonical_written": False,
        "formal_credit": 0,
        "D02_gate_credit": 0,
        "D02_unlock_capability": False,
    })
    write_no_replace(OUT / OUTER_NAME, canonical(outer) + b"\n")
    return outer


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="publish new evidence files with O_EXCL; outer receipt last")
    args = parser.parse_args()
    if args.emit:
        result = emit()
        print(json.dumps({"status": result["status"], "object_sha256": result["object_sha256"]}, sort_keys=True))
    else:
        verification, self_test, _raw, _identities, _contract = build_evidence()
        print(json.dumps({
            "status": verification["status"],
            "object_sha256": verification["object_sha256"],
            "attack_count": self_test["attack_count"],
            "formal_credit": 0,
            "D02_gate_credit": 0,
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Rejected, OSError, ValueError, KeyError, TypeError, IndexError, json.JSONDecodeError, gzip.BadGzipFile) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
