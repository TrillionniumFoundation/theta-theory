#!/usr/bin/env python3
"""Append-only r17 static clean-room builder.

This builder consumes only the rejected r16 bytes and creates a new r17
namespace.  It repairs the three historical transition-validator dialects,
restores the generic live v16r2 root protocol, installs the complete trust
receipt key set, and removes staging-only schema-root extensions.  It never
imports or executes a protocol source and never creates a manifest, outer
receipt, runtime surface, credit, or authority artifact.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
PREV = "v16r2r16"
TAG = "v16r2r17"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

PS = {
    "producer": OUT / f"{BASE}_{PREV}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
}
PJ = {
    "schema": OUT / f"{BASE}_schema_{PREV}.json",
    "contract": OUT / f"{BASE}_contract_{PREV}.json",
    "transition": OUT / f"{BASE}_v16r2r15_to_{PREV}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{PREV}.json",
}
SA = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
S = {
    "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
}
J = {
    "schema": OUT / f"{BASE}_schema_{TAG}.json",
    "contract": OUT / f"{BASE}_contract_{TAG}.json",
    "transition": OUT / f"{BASE}_v16r2r16_to_{TAG}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
}
REJ = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
SUP = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"

V14_REJECTION = ".cm2-runtime/c79g-v14-rejections-" + CHECKPOINT + "/rejection.json"
V14_SUPERSESSION = (
    f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json"
)
V14_STRICT_REPLAY_KEY = (
    "runtime_consumer_must_hold_strict_parse_object_close_and_"
    "terminally_replay_inherited_v14_exact12"
)
CANONICAL_TRANSITION_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer."
    "v16-to-v16r2-static-launch-transition.v1"
)
CANONICAL_TRANSITION_KIND = (
    "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_"
    "ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR"
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canonical(body))
    return body


class DuplicateKey(ValueError):
    pass


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after, named = os.fstat(fd), os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named.st_dev, named.st_ino)):
            raise RuntimeError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(stable(path).decode("utf-8"), object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON object required: {path}")
    return value


def install(path: Path, raw: bytes, mode: int) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, mode)
    except FileExistsError:
        if (stable(path) != raw or path.stat().st_nlink != 1 or
                stat.S_IMODE(path.stat().st_mode) != mode):
            raise RuntimeError(f"append-only mismatch: {path}")
        return "replayed"
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            offset += os.write(fd, view[offset:])
        os.fsync(fd)
        os.fchmod(fd, mode)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def rejection() -> tuple[dict[str, Any], bytes]:
    inputs = {**PS, **{f"json_{k}": p for k, p in PJ.items()},
              "active_anchor": SA}
    evidence = {
        name: {
            "path": str(path.relative_to(ROOT)),
            "file_sha256": sha(stable(path)),
            "bytes": path.stat().st_size,
            "mode": f"{stat.S_IMODE(path.stat().st_mode):04o}",
            "nlink": path.stat().st_nlink,
        }
        for name, path in inputs.items()
    }
    value = close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v5",
        "status": "PERMANENT_FAIL_CLOSED_STATIC_REVIEW__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": (
            "R17_PREFLIGHT_PIN_NORMALIZATION_SELF_HASH_CYCLE_OR_"
            "RUNTIME_TRANSITION_SUCCESSOR_SHAPE_DRIFT"),
        "independent_reviewer_failed_checks": [
            "pin_dependency_graph_acyclicity",
            "source_contract_transition_audit_pin_closure",
            "consumer_required_final_core_successor_shape",
        ],
        "independent_reviewer_failed_check_count": 3,
        "failed_artifacts": evidence,
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
        "runtime_surface_created": False,
    })
    return value, canonical(value) + b"\n"


def supersession(rejected: dict[str, Any], rejected_raw: bytes,
                 rejection_raw: bytes) -> tuple[dict[str, Any], bytes]:
    value = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v5",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "successor_namespace": TAG,
        "predecessor_rejection_path": str(REJ.relative_to(ROOT)),
        "predecessor_rejection_file_sha256": sha(rejection_raw),
        "predecessor_rejection_object_sha256": rejected["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    })
    return value, canonical(value) + b"\n"


def anchor(sup: dict[str, Any], sup_raw: bytes) -> tuple[dict[str, Any], bytes]:
    value = close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUP.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(sup_raw),
        "predecessor_supersession_object_sha256": sup["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
    })
    return value, canonical(value) + b"\n"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, got {count}")
    return text.replace(old, new)


def normalize_transition_checks(text: str, role: str) -> str:
    """Normalize legacy transition literals while accepting an already
    canonical predecessor source. Historical witness literals remain intact."""
    canonical_schema = '"v16-to-v16r2-static-launch-transition.v1"'
    canonical_kind = (
        '"APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_"\\n'
        '             "ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR"')
    if role == "producer":
        old_schema = '"v12-to-v16r2-static-launch-transition.v1"'
        if old_schema in text:
            text = replace_once(text, old_schema, canonical_schema,
                                "producer final transition schema")
        elif canonical_schema not in text:
            raise RuntimeError("producer canonical transition schema missing")
        old_kind = (
            '"APPEND_ONLY_PUBLISHED_THEN_OFFICIALLY_REJECTED_V12_TO_"\\n'
            '             "ZERO_CREDIT_V16R2_STATIC_SUCCESSOR"')
        if old_kind in text:
            text = replace_once(text, old_kind, canonical_kind,
                                "producer final transition kind")
        elif not all(fragment in text for fragment in (
                "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_",
                "ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR")):
            raise RuntimeError("producer canonical transition kind missing")
    elif role == "launcher":
        old_kind = (
            '"APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_REJECTION_"\\n'
            '                 "TO_ZERO_CREDIT_V16R2_STATIC_SUCCESSOR"')
        if old_kind in text:
            text = replace_once(
                text, old_kind,
                '"APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_"\\n'
                '                 "ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR"',
                "launcher final transition kind")
        elif not all(fragment in text for fragment in (
                "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_",
                "ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR")):
            raise RuntimeError("launcher canonical transition kind missing")
    return text

def source_bytes(raw: bytes, role: str, anchor_value: dict[str, Any],
                 anchor_raw: bytes) -> bytes:
    text = raw.decode("utf-8")
    old_anchor = SA.name
    old_edge = f"{BASE}_v16r2r15_to_{PREV}_static_launch_transition_receipt_v1.json"
    anchor_marker, edge_marker = "__R17_ANCHOR__", "__R16_TO_R17_EDGE__"
    text = text.replace(old_anchor, anchor_marker)
    text = text.replace(old_edge, edge_marker)
    text = text.replace("V16R2R16", "V16R2R17")
    text = text.replace(PREV, TAG)
    text = text.replace(anchor_marker, ANCHOR.name)
    text = text.replace(edge_marker, J["transition"].name)
    text = normalize_transition_checks(text, role)
    text, n_file = re.subn(
        r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
        f'ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "{sha(anchor_raw)}"',
        text)
    text, n_object = re.subn(
        r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
        f'ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "{anchor_value["object_sha256"]}"',
        text)
    if (n_file, n_object) != (1, 1):
        raise RuntimeError(f"{role}: active anchor pin count")
    if f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json" in text:
        raise RuntimeError(f"{role}: stale active predecessor path")
    if "v16r2r16_to_v16r2r16" in text or "v16r2r17_to_v16r2r17" in text:
        raise RuntimeError(f"{role}: self transition edge")
    tree = ast.parse(text, filename=str(S[role]))
    compile(tree, str(S[role]), "exec")
    return (text if text.endswith("\n") else text + "\n").encode("utf-8")


def retag(value: Any) -> Any:
    if isinstance(value, dict):
        return {retag(key): retag(child) for key, child in value.items()}
    if isinstance(value, list):
        return [retag(child) for child in value]
    if not isinstance(value, str):
        return value
    old_edge = f"{BASE}_v16r2r15_to_{PREV}_static_launch_transition_receipt_v1.json"
    return (value.replace(old_edge, "__R16_TO_R17_EDGE__")
            .replace("V16R2R16", "V16R2R17")
            .replace(PREV, TAG)
            .replace("__R16_TO_R17_EDGE__", J["transition"].relative_to(ROOT).as_posix()))


def paths() -> dict[str, str]:
    return {
        "predecessor": str(ANCHOR.relative_to(ROOT)),
        "schema": str(J["schema"].relative_to(ROOT)),
        "contract": str(J["contract"].relative_to(ROOT)),
        "producer": str(S["producer"].relative_to(ROOT)),
        "consumer": str(S["consumer"].relative_to(ROOT)),
        "transition": str(J["transition"].relative_to(ROOT)),
        "audit": str(J["audit"].relative_to(ROOT)),
        "launcher": str(S["launcher"].relative_to(ROOT)),
        "manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
        "outer": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json",
    }


def patch_bundle(bundle: dict[str, Any], source_hashes: dict[str, str],
                 p: dict[str, str], schema_file_sha: str) -> None:
    exact8 = [p[name] for name in
              ("predecessor", "schema", "contract", "producer",
               "consumer", "transition", "audit", "launcher")]
    bundle.update({
        "bundle_version": TAG,
        "source_hashes": source_hashes,
        "base7_ordered_paths": exact8[:-1],
        "exact8_ordered_paths": exact8,
        "exact10_ordered_paths": exact8 + [p["manifest"], p["outer"]],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "pin_state": "R17_SOURCE_AND_JSON_PINS_UNINSTALLED__STATIC_ZERO_CREDIT",
        "schema_file_sha256": schema_file_sha,
        "predecessor_supersession_object_sha256": read_json(ANCHOR)["object_sha256"],
        "predecessor_semantic_supersession": {
            "path": p["predecessor"],
            "file_sha256": sha(stable(ANCHOR)),
            "object_sha256": read_json(ANCHOR)["object_sha256"],
            "successor_only": f"{TAG}-semantic-bundle",
        },
        "contract_file_sha256": f"UNPINNED_{TAG.upper()}_CONTRACT_FILE",
        "contract_object_sha256": f"UNPINNED_{TAG.upper()}_CONTRACT_OBJECT",
        "transition_file_sha256": f"UNPINNED_{TAG.upper()}_TRANSITION_FILE",
        "transition_object_sha256": f"UNPINNED_{TAG.upper()}_TRANSITION_OBJECT",
        "audit_file_sha256": f"UNPINNED_{TAG.upper()}_AUDIT_FILE",
    })
    # The runtime reads the nested closed-schema receipt as the authoritative
    # one-way file pin.  Keep its historical object sentinel untouched (the
    # live JSON Schema has no receipt object hash), but bind the actual bytes
    # and successor path before any downstream root is closed.
    closed_schema = bundle.get("closed_schema")
    if not isinstance(closed_schema, dict):
        raise RuntimeError("active closed_schema receipt missing")
    closed_schema["path"] = p["schema"]
    closed_schema["file_sha256"] = schema_file_sha
    outer = dict(bundle.get("cold_launch_outer_closure", {}))
    outer.update({
        "exact8_manifest_path": p["manifest"],
        "outer_last_path": p["outer"],
        "launcher_path": p["launcher"],
        "manifest_or_outer_absent_in_this_static_phase": True,
        "runtime_entry_authorized": False,
    })
    bundle["cold_launch_outer_closure"] = outer
    trust = bundle.get("post_source_static_trust_receipts")
    if not isinstance(trust, dict):
        raise RuntimeError("active trust receipt object missing")
    trust.update({
        "binding_direction": "R17_SOURCE_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE",
        "predecessor_supersession_path": p["predecessor"],
        "predecessor_supersession_file_sha256": sha(stable(ANCHOR)),
        "predecessor_supersession_object_sha256": read_json(ANCHOR)["object_sha256"],
        "static_audit_path": p["audit"],
        "transition_path": p["transition"],
        "v16_to_v16r2_transition_path": p["transition"],
        "v14_official_rejection_path": V14_REJECTION,
        "v14_registry_shape_drift_supersession_receipt_path": V14_SUPERSESSION,
        V14_STRICT_REPLAY_KEY: True,
    })


def build_quartet(source_hashes: dict[str, str]) -> dict[str, bytes]:
    values = {name: retag(read_json(path)) for name, path in PJ.items()}
    # The live runtime has one generic active key per root.  Versioned aliases
    # are staging metadata only and are deliberately removed.
    key_candidates = {
        "contract": ("v16r2_bundle", f"{PREV}_bundle"),
        "transition": ("successor_v16r2_static_bundle",
                       f"successor_{PREV}_static_bundle"),
        "audit": ("audited_v16r2_bundle", f"audited_{PREV}_bundle"),
    }
    active: dict[str, dict[str, Any]] = {}
    for name, candidates in key_candidates.items():
        found = None
        for key in candidates:
            if isinstance(values[name].get(key), dict):
                found = values[name].pop(key)
                break
        if found is None:
            raise RuntimeError(f"missing active {name} bundle")
        for key in list(values[name]):
            if key.endswith("_bundle") and key not in {
                    "v16r2_bundle", "successor_v16r2_static_bundle",
                    "audited_v16r2_bundle"}:
                values[name].pop(key, None)
        active[name] = found
    p = paths()

    # A live closed schema is a JSON Schema document, not a closed receipt:
    # runtime explicitly rejects object_sha256 and x-cm2 extension members at
    # its root.  Historical extension bytes remain immutable in r16 and are
    # represented by the r17 rejection evidence, never by this live schema.
    schema = values["schema"]
    schema.pop("object_sha256", None)
    for key in list(schema):
        if key.startswith("x-cm2-"):
            schema.pop(key, None)
    schema["$comment"] = (
        "CM2_R17_LIVE_SUCCESSOR__GENERIC_V16R2_ROOT_PROTOCOL__"
        "STATIC_ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED")
    schema_raw = canonical(schema) + b"\n"
    schema_file_sha = sha(schema_raw)

    for name, bundle in active.items():
        patch_bundle(bundle, source_hashes, p, schema_file_sha)
    values["contract"]["v16r2_bundle"] = active["contract"]
    values["transition"]["successor_v16r2_static_bundle"] = active["transition"]
    values["audit"]["audited_v16r2_bundle"] = active["audit"]

    values["contract"].update({
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.v16r2.contract",
        "status": "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
        "purpose": (
            "Append-only r17 semantic bundle with generic v16r2 runtime root "
            "protocol; no credit transfer."),
    })
    values["transition"].update({
        "schema": CANONICAL_TRANSITION_SCHEMA,
        "status": "STATIC_BYTES_CLOSED_V16_TO_V16R2__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED",
        "receipt_path": p["transition"],
        "transition_kind": CANONICAL_TRANSITION_KIND,
    })
    values["audit"].update({
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.static-audit.v16r2",
        "status": (
            "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V16R2__"
            "PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED"),
        "audit_path": p["audit"],
    })

    # Keep the exact historical schema/constructor closure shape untouched.
    if (len(schema.get("$defs", {})),
            sum(1 for node in walk(schema)
                if isinstance(node, dict) and "$ref" in node),
            sum(1 for node in walk(schema)
                if isinstance(node, dict) and
                node.get("additionalProperties") is False)) != (46, 242, 52):
        raise RuntimeError("schema shape drift")
    if [len(values[name]) for name in ("contract", "transition", "audit")] != [30, 31, 30]:
        raise RuntimeError("instance root shape drift")

    result = {
        "schema": schema_raw,
        "contract": canonical(close(values["contract"])) + b"\n",
        "transition": canonical(close(values["transition"])) + b"\n",
        "audit": canonical(close(values["audit"])) + b"\n",
    }
    return result


class PreflightBlocker(RuntimeError):
    """A deterministic blocker found before any r17 candidate is installed."""

    def __init__(self, blockers: list[dict[str, Any]]):
        self.blockers = blockers
        super().__init__("; ".join(item["id"] for item in blockers))


def preflight_pin_graph() -> dict[str, Any]:
    """Audit the dependency graph without constructing or writing candidates.

    r16 roots carry ``source_hashes`` while every final source is required to
    read the post-source contract/schema/transition/audit pins.  Once those
    sentinels are normalized, the two directions form a real hash cycle.  We
    report the concrete edges here instead of trying to guess a fixed point.
    """
    transition = read_json(PJ["transition"])
    successor = transition.get("successor_v16r2_static_bundle")
    if not isinstance(successor, dict):
        raise RuntimeError("r16 transition successor bundle missing")

    # These are the exact keys/values consumed by r16's static_freeze_proof.
    required = {
        "all_four_core_file_pins_final",
        "build_only_producer",
        "closed_schema",
        "cold_launcher_v16r2_path",
        "contract",
        "draft_pin_sentinels_remain_present",
        "final_consumer_pin_installed",
        "independent_verifier_assembler_authority_consumer",
        "static_audit_v16r2_path",
        "transition_receipt_bytes_are_closed_around_final_core_pins",
        "transition_receipt_physical_freeze_completed",
    }
    actual = set(successor)
    shape = {
        "required_key_count": len(required),
        "actual_key_count": len(actual),
        "missing_keys": sorted(required - actual),
        "extra_keys": sorted(actual - required),
        "value_failures": {},
    }
    expected_true = (
        "all_four_core_file_pins_final",
        "final_consumer_pin_installed",
        "transition_receipt_bytes_are_closed_around_final_core_pins",
    )
    for key in expected_true:
        if successor.get(key) is not True:
            shape["value_failures"][key] = successor.get(key)
    if successor.get("draft_pin_sentinels_remain_present") is not False:
        shape["value_failures"]["draft_pin_sentinels_remain_present"] = successor.get(
            "draft_pin_sentinels_remain_present")
    # The transition is still pre-physical-freeze at this phase; the consumer
    # contract explicitly requires this flag to remain False until exact8 /
    # manifest / outer-last are independently completed.
    if successor.get("transition_receipt_physical_freeze_completed") is not False:
        shape["value_failures"]["transition_receipt_physical_freeze_completed"] = successor.get(
            "transition_receipt_physical_freeze_completed")
    for key in ("closed_schema", "contract", "build_only_producer",
                "independent_verifier_assembler_authority_consumer"):
        if not isinstance(successor.get(key), dict):
            shape["value_failures"][key] = "object_required"
    shape_ok = not (shape["missing_keys"] or shape["extra_keys"] or
                    shape["value_failures"])

    # Pin graph nodes represent bytes whose SHA-256 is asserted elsewhere.
    # The labels are deliberately field-level so the rejection is actionable.
    graph_edges = [
        {"from": "producer_source_bytes", "to": "contract_json",
         "field": "CONTRACT_FILE_PIN/CONTRACT_OBJECT_PIN"},
        {"from": "producer_source_bytes", "to": "schema_json",
         "field": "CLOSED_SCHEMA_FILE_PIN"},
        {"from": "consumer_source_bytes", "to": "contract_json",
         "field": "CONTRACT_FILE_PIN/CONTRACT_OBJECT_PIN"},
        {"from": "consumer_source_bytes", "to": "schema_json",
         "field": "CLOSED_SCHEMA_FILE_PIN"},
        {"from": "consumer_source_bytes", "to": "producer_source_bytes",
         "field": "PRODUCER_SOURCE_PIN"},
        {"from": "launcher_source_bytes", "to": "schema_json",
         "field": "BASE7_PINS[SCHEMA]"},
        {"from": "launcher_source_bytes", "to": "contract_json",
         "field": "BASE7_PINS[CONTRACT]"},
        {"from": "launcher_source_bytes", "to": "producer_source_bytes",
         "field": "BASE7_PINS[PRODUCER]"},
        {"from": "launcher_source_bytes", "to": "consumer_source_bytes",
         "field": "BASE7_PINS[CONSUMER]"},
        {"from": "launcher_source_bytes", "to": "transition_json",
         "field": "BASE7_PINS[TRANSITION]"},
        {"from": "launcher_source_bytes", "to": "audit_json",
         "field": "BASE7_PINS[AUDIT]"},
    ]
    for artifact in ("contract_json", "transition_json", "audit_json"):
        for role in ("producer", "consumer", "launcher"):
            graph_edges.append({
                "from": artifact,
                "to": f"{role}_source_bytes",
                "field": f"{artifact}.source_hashes.{role}",
            })

    # A short, explicit cycle witness is enough to fail closed.  It is not a
    # claim about a runtime fixed point: changing either source changes the
    # asserted source hash in the contract/transition/audit bytes again.
    cycle = [
        "producer_source_bytes",
        "contract_json",
        "producer_source_bytes",
    ]
    blockers: list[dict[str, Any]] = [{
        "id": "pin_dependency_graph_cycle",
        "cycle": cycle,
        "edges": [
            {
                "from": "producer_source_bytes",
                "to": "contract_json",
                "field": "CONTRACT_FILE_PIN/CONTRACT_OBJECT_PIN",
            },
            {
                "from": "contract_json",
                "to": "producer_source_bytes",
                "field": "source_hashes.producer",
            },
        ],
        "explanation": (
            "normalizing the producer's actual contract pins changes the "
            "producer bytes; the contract source_hashes.producer then changes "
            "the contract bytes and therefore the pin again"),
    }]
    if not shape_ok:
        blockers.append({
            "id": "consumer_required_final_core_successor_shape",
            "required_key_count": len(required),
            "actual_key_count": len(actual),
            "missing_keys": shape["missing_keys"],
            "extra_keys": shape["extra_keys"],
            "value_failures": shape["value_failures"],
            "explanation": (
                "r16 consumer static_freeze_proof requires an exact 11-key "
                "final successor core; the predecessor is still a generic "
                "28-key draft bundle"),
        })
    return {
        "status": "FAIL_CLOSED_PREINSTALL",
        "shape": shape,
        "shape_ok": shape_ok,
        "graph_edges": graph_edges,
        "blockers": blockers,
        "candidate_install_allowed": False,
    }


def main() -> int:
    try:
        for path in (*PS.values(), *PJ.values(), SA):
            if not path.is_file():
                raise RuntimeError(f"missing r16 input: {path}")

        # Freeze only the rejection chain first.  No source or JSON candidate
        # is even constructed until the read-only dependency/shape preflight
        # has passed.
        rej, rej_raw = rejection()
        rejection_action = install(REJ, rej_raw, 0o444)
        sup, sup_raw = supersession(rej, rej_raw, rej_raw)
        supersession_action = install(SUP, sup_raw, 0o444)
        anc, anc_raw = anchor(sup, sup_raw)
        anchor_action = install(ANCHOR, anc_raw, 0o444)

        preflight = preflight_pin_graph()
        manifest = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
        outer = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
        if manifest.exists() or outer.exists():
            raise RuntimeError("manifest/outer appeared during preflight")
        pyc_paths = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc")
                     if TAG in str(path)]
        if pyc_paths:
            raise RuntimeError(f"r17 pyc appeared: {pyc_paths}")
        result = {
            "schema": f"cm2.c79g.{TAG}.clean-room-builder.preflight.v2",
            "status": f"FAIL_CLOSED_{TAG.upper()}_PIN_PREFLIGHT",
            "successor_suffix": TAG,
            "predecessor_suffix": PREV,
            "candidate_install": False,
            "candidate_artifacts_installed": False,
            "predecessor_rejection": {
                "path": str(REJ.relative_to(ROOT)),
                "file_sha256": sha(rej_raw),
                "object_sha256": rej["object_sha256"],
                "action": rejection_action,
            },
            "predecessor_supersession": {
                "path": str(SUP.relative_to(ROOT)),
                "file_sha256": sha(sup_raw),
                "object_sha256": sup["object_sha256"],
                "action": supersession_action,
            },
            "active_anchor": {
                "path": str(ANCHOR.relative_to(ROOT)),
                "file_sha256": sha(anc_raw),
                "object_sha256": anc["object_sha256"],
                "action": anchor_action,
            },
            "preflight": preflight,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "manifest_created": False,
            "outer_created": False,
            "runtime_surface_created": False,
            "pyc_created": False,
        }
        result["object_sha256"] = sha(canonical(result))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 1
    except Exception as exc:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.clean-room-builder.failure.v2",
            "status": f"FAIL_CLOSED_{TAG.upper()}_CLEAN_ROOM",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "candidate_install": False,
            "candidate_artifacts_installed": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
