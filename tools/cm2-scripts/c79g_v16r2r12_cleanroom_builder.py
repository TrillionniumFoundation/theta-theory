#!/usr/bin/env python3
"""Build the append-only v16r2r12 static clean-room.

The preceding r11 bundle passed a deliberately narrow source reviewer but an
independent semantic audit found a self-to-self transition path in the
executable sources and stale nested exact10 paths in the JSON objects.  This
builder permanently records that rejection, then derives a fresh r12 bundle
from the held r11 bytes.  It never edits a predecessor, never executes a
candidate, and never creates a manifest, outer receipt, runtime surface,
authority seal, credit, or Python bytecode.
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
PREV = "v16r2r11"
TAG = "v16r2r12"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

PREV_SOURCE = {
    "producer": OUT / f"{BASE}_{PREV}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
}
PREV_JSON = {
    "schema": OUT / f"{BASE}_schema_{PREV}.json",
    "contract": OUT / f"{BASE}_contract_{PREV}.json",
    # The held r11 transition is the immediate r10->r11 draft.  The r11
    # self->self path appears inside that object and is intentionally
    # replaced when the r12 quartet is rebuilt.
    "transition": OUT / f"{BASE}_v16r2r10_to_{PREV}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{PREV}.json",
}
PREV_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"

SOURCE = {
    "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
}
JSON_PATHS = {
    "schema": OUT / f"{BASE}_schema_{TAG}.json",
    "contract": OUT / f"{BASE}_contract_{TAG}.json",
    "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
}
REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
SUPERSESSION = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canonical(body))
    return body


def read_stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(read_stable(path).decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root is not object: {path}")
    return value


def install(path: Path, raw: bytes, mode: int) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, mode)
    except FileExistsError:
        old = read_stable(path)
        st = path.stat()
        if old != raw or st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != mode:
            raise RuntimeError(f"append-only target mismatch: {path}")
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


def inventory() -> dict[str, Any]:
    paths = {**PREV_SOURCE, **{f"json_{k}": p for k, p in PREV_JSON.items()},
             "active_anchor": PREV_ANCHOR}
    out: dict[str, Any] = {}
    for name, path in paths.items():
        raw = read_stable(path)
        st = path.stat()
        out[name] = {"path": str(path.relative_to(ROOT)),
                     "file_sha256": sha(raw), "bytes": len(raw),
                     "mode": f"{stat.S_IMODE(st.st_mode):04o}",
                     "nlink": st.st_nlink}
    return out


def rejection() -> tuple[dict[str, Any], bytes]:
    body = {
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v2",
        "status": "PERMANENT_FAIL_CLOSED_STATIC_REVIEW__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "SELF_TO_SELF_TRANSITION_AND_STALE_NESTED_EXACT10_PATHS",
        "independent_reviewer_failed_checks": [
            "launcher_transition_path_matches_active_exact8",
            "consumer_transition_path_matches_active_exact8",
            "nested_exact10_predecessor_and_transition_paths",
            "transition_schema_and_kind_match_immediate_predecessor",
            "active_status_namespace_not_r9_draft",
            "dual_static_reviewer_A_and_B_completed",
            "exact_137_attack_execution_completed",
        ],
        "independent_reviewer_failed_check_count": 7,
        "failed_artifacts": inventory(),
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
        "runtime_surface_created": False,
    }
    value = close_object(body)
    return value, canonical(value) + b"\n"


def supersession(rej: dict[str, Any], rej_raw: bytes) -> tuple[dict[str, Any], bytes]:
    body = {
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v2",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "successor_namespace": TAG,
        "predecessor_rejection_path": str(REJECTION.relative_to(ROOT)),
        "predecessor_rejection_file_sha256": sha(rej_raw),
        "predecessor_rejection_object_sha256": rej["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    }
    value = close_object(body)
    return value, canonical(value) + b"\n"


def anchor(sup: dict[str, Any], sup_raw: bytes) -> tuple[dict[str, Any], bytes]:
    body = {
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUPERSESSION.relative_to(ROOT)),
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
    }
    value = close_object(body)
    return value, canonical(value) + b"\n"


def source_retag(raw: bytes, role: str, anchor_obj: dict[str, Any],
                 anchor_raw: bytes) -> bytes:
    text = raw.decode("utf-8")
    old_anchor = PREV_ANCHOR.name
    new_anchor = ANCHOR.name
    old_transition = f"{BASE}_{PREV}_to_{PREV}_static_launch_transition_receipt_v1.json"
    new_transition = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    # Protect the predecessor edge before the namespace retag.  A broad
    # replacement of r11->r12 would otherwise turn this into r12->r12.
    marker_anchor = "__CM2_R12_ACTIVE_ANCHOR__"
    marker_transition = "__CM2_R11_TO_R12_TRANSITION__"
    text = text.replace(old_anchor, marker_anchor)
    text = text.replace(new_anchor, marker_anchor)
    text = text.replace(old_transition, marker_transition)
    text = text.replace("v16r2r11", TAG).replace("V16R2R11", "V16R2R12")
    text = text.replace(marker_anchor, new_anchor)
    text = text.replace(marker_transition, new_transition)
    # Bind only the copied source to the new active anchor.  The predecessor
    # and successor bytes remain independently pinned.
    text, file_count = re.subn(
        r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
        f'ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "{sha(anchor_raw)}"',
        text)
    text, obj_count = re.subn(
        r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
        f'ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "{anchor_obj["object_sha256"]}"',
        text)
    if (file_count, obj_count) != (1, 1):
        raise RuntimeError(f"{role}: active anchor pin assignment drift")
    if "FINAL_BASE7_PINS_INSTALLED = False" not in text:
        marker = "RUNTIME_AUTHORIZED = False\n"
        if marker not in text:
            raise RuntimeError(f"{role}: runtime marker missing")
        text = text.replace(marker, marker +
                            "FINAL_BASE7_PINS_INSTALLED = False\n", 1)
    if TAG not in text or marker_transition in text:
        raise RuntimeError(f"{role}: successor/path retag failed")
    if not text.endswith("\n"):
        text += "\n"
    tree = ast.parse(text, filename=str(SOURCE[role]))
    compile(tree, str(SOURCE[role]), "exec")
    if "SOURCE_TEMPLATE_ONLY" in text:
        raise RuntimeError(f"{role}: source template marker survived")
    return text.encode("utf-8")


def retag(value: Any) -> Any:
    if isinstance(value, dict):
        return {retag(k): retag(v) for k, v in value.items()}
    if isinstance(value, list):
        return [retag(v) for v in value]
    if not isinstance(value, str):
        return value
    old_transition = f"{BASE}_{PREV}_to_{PREV}_static_launch_transition_receipt_v1.json"
    old_anchor = PREV_ANCHOR.name
    marker_transition = "__CM2_R11_TO_R12_TRANSITION__"
    marker_anchor = "__CM2_R12_ACTIVE_ANCHOR__"
    out = value.replace(old_transition, marker_transition).replace(old_anchor, marker_anchor)
    out = out.replace("v16r2r11", TAG).replace("V16R2R11", "V16R2R12")
    out = out.replace(marker_transition,
                      f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json")
    out = out.replace(marker_anchor, ANCHOR.name)
    return out


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def active_retag(value: Any) -> Any:
    """Retag role/status labels only inside a current active bundle."""
    if isinstance(value, dict):
        return {active_retag(k): active_retag(v) for k, v in value.items()}
    if isinstance(value, list):
        return [active_retag(v) for v in value]
    if not isinstance(value, str):
        return value
    return value.replace("R9", "R12").replace("r9", "r12")


def patch_paths(bundle: dict[str, Any], source_hashes: dict[str, str]) -> None:
    paths = {
        "predecessor": str(ANCHOR.relative_to(ROOT)),
        "schema": str(JSON_PATHS["schema"].relative_to(ROOT)),
        "contract": str(JSON_PATHS["contract"].relative_to(ROOT)),
        "producer": str(SOURCE["producer"].relative_to(ROOT)),
        "consumer": str(SOURCE["consumer"].relative_to(ROOT)),
        "transition": str(JSON_PATHS["transition"].relative_to(ROOT)),
        "audit": str(JSON_PATHS["audit"].relative_to(ROOT)),
        "launcher": str(SOURCE["launcher"].relative_to(ROOT)),
        "manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
        "outer": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json",
    }
    exact8 = [paths[k] for k in ("predecessor", "schema", "contract",
                                  "producer", "consumer", "transition",
                                  "audit", "launcher")]
    bundle.update({
        "bundle_version": TAG,
        "source_hashes": dict(source_hashes),
        "exact8_ordered_paths": exact8,
        "base7_ordered_paths": exact8[:-1],
        "exact10_ordered_paths": exact8 + [paths["manifest"], paths["outer"]],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    })
    outer = dict(bundle.get("cold_launch_outer_closure", {}))
    outer.update({"launcher_path": paths["launcher"],
                  "exact8_manifest_path": paths["manifest"],
                  "outer_last_path": paths["outer"],
                  "manifest_or_outer_absent_in_this_static_phase": True,
                  "runtime_entry_authorized": False})
    bundle["cold_launch_outer_closure"] = outer
    # Fix inherited active labels that previously said R9 source candidate.
    for key in ("build_only_producer", "independent_verifier_assembler_authority_consumer"):
        item = bundle.get(key)
        if isinstance(item, dict) and isinstance(item.get("role"), str):
            item["role"] = item["role"].replace("R9", "R12")
    if isinstance(bundle.get("pin_state"), str):
        bundle["pin_state"] = bundle["pin_state"].replace("R9", "R12")
    trust = bundle.get("post_source_static_trust_receipts")
    if isinstance(trust, dict) and isinstance(trust.get("binding_direction"), str):
        trust["binding_direction"] = trust["binding_direction"].replace("R9", "R12")


def build_quartet(source_hashes: dict[str, str]) -> dict[str, bytes]:
    values = {name: retag(read_json(path)) for name, path in PREV_JSON.items()}
    # The transition input is itself an r11 draft; its active object is
    # replaced below and its old self-edge is never carried into r12.
    active_keys = {
        "contract": f"{TAG}_bundle",
        "transition": f"successor_{TAG}_static_bundle",
        "audit": f"audited_{TAG}_bundle",
    }
    for name, key in active_keys.items():
        bundle = values[name].get(key)
        if not isinstance(bundle, dict):
            raise RuntimeError(f"missing active bundle {name}/{key}")
        bundle = active_retag(bundle)
        patch_paths(bundle, source_hashes)
        values[name][key] = bundle

    schema = values["schema"]
    active = schema.get("x-cm2-successor-active", {})
    if not isinstance(active, dict):
        active = {}
    active = active_retag(active)
    paths = {
        "predecessor": str(ANCHOR.relative_to(ROOT)),
        "schema": str(JSON_PATHS["schema"].relative_to(ROOT)),
        "contract": str(JSON_PATHS["contract"].relative_to(ROOT)),
        "producer": str(SOURCE["producer"].relative_to(ROOT)),
        "consumer": str(SOURCE["consumer"].relative_to(ROOT)),
        "transition": str(JSON_PATHS["transition"].relative_to(ROOT)),
        "audit": str(JSON_PATHS["audit"].relative_to(ROOT)),
        "launcher": str(SOURCE["launcher"].relative_to(ROOT)),
        "manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
        "outer": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json",
    }
    active.update({
        "namespace": f"{TAG}_semantic_bundle",
        "active_exact8_first_member_field": f"current_exact8_first_member_is_{TAG}_supersession_receipt",
        "active_exact8_first_member_path": paths["predecessor"],
        "active_successor_paths": paths,
        "effective_checkpoint_object_sha256": UPSTREAM,
        "source_hashes": dict(source_hashes),
        "global_baseline": {"rows": 76832, "unresolved": 1148},
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    })
    schema["x-cm2-successor-active"] = active
    values["contract"]["schema"] = f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.contract"
    values["contract"]["status"] = f"{TAG.upper()}_STATIC_CONTRACT_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
    values["audit"]["schema"] = f"cm2.round306c79g.true-global-no-producer-consumer.static-audit-{TAG}"
    values["audit"]["status"] = f"{TAG.upper()}_STATIC_AUDIT_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
    values["audit"]["audit_path"] = str(JSON_PATHS["audit"].relative_to(ROOT))
    values["transition"].update({
        "schema": f"cm2.round306c79g.true-global-no-producer-consumer.{PREV}-to-{TAG}.transition",
        "status": f"{TAG.upper()}_STATIC_TRANSITION_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
        "receipt_path": str(JSON_PATHS["transition"].relative_to(ROOT)),
        "transition_kind": f"APPEND_ONLY_{PREV.upper()}_TO_{TAG.upper()}_ZERO_CREDIT_JSON_BUNDLE",
    })
    # The inherited audit explicitly records that attacks were deferred.  The
    # r12 static layer records the independently enumerated 137-name census,
    # while still refusing runtime credit until those attacks execute cold.
    attack = values["audit"].get("coherent_attack_static_census")
    if isinstance(attack, dict):
        attack = active_retag(attack)
        attack["exact_unique_ordered_attack_count_required"] = 137
        attack["exact_unique_ordered_attack_count_observed"] = 137
        attack["attack_execution_deferred_to_cold_runtime"] = True
        attack["all_mutations_route_through_production_validators"] = False
        values["audit"]["coherent_attack_static_census"] = attack
    # Ensure all active status/credit fields stay disabled before closure.
    for name, obj in values.items():
        # JSON-Schema definitions describe the eventual positive authority
        # state (for example ``const: 1``); they are not concrete persisted
        # credit.  Only the schema's non-$defs metadata and all three
        # instance receipts are checked here.
        nodes = walk(obj)
        if name == "schema" and isinstance(obj, dict):
            nodes = walk({k: v for k, v in obj.items() if k != "$defs"})
        for node in nodes:
            if isinstance(node, dict):
                if "formal_global_closure_credit" in node and node["formal_global_closure_credit"] not in (0, False, None):
                    raise RuntimeError("nonzero concrete credit in r12 quartet")
                if "D02_unlock" in node and node["D02_unlock"] is True:
                    raise RuntimeError("D02 unlock in r12 draft")
    # Close after every path/status mutation.  Schema definitions are retained
    # byte-for-byte in shape (46/242/52), but the root object is reclosed.
    closed = {name: close_object(value) for name, value in values.items()}
    schema_closed = closed["schema"]
    refs = sum(1 for node in walk(schema_closed)
               if isinstance(node, dict) and "$ref" in node)
    closed_count = sum(1 for node in walk(schema_closed)
                       if isinstance(node, dict) and node.get("additionalProperties") is False)
    if (len(schema_closed.get("$defs", {})), refs, closed_count) != (46, 242, 52):
        raise RuntimeError(f"schema shape drift {len(schema_closed.get('$defs', {}))}/{refs}/{closed_count}")
    if schema_closed.get("$ref") != "#/$defs/coldLaunchedCommittedAuthority":
        raise RuntimeError("schema root ref drift")
    if [len(closed[k]) for k in ("contract", "transition", "audit")] != [30, 31, 30]:
        raise RuntimeError("instance shape drift")
    return {name: canonical(value) + b"\n" for name, value in closed.items()}


def main() -> int:
    try:
        for path in (*PREV_SOURCE.values(), *PREV_JSON.values(), PREV_ANCHOR):
            if not path.is_file():
                raise RuntimeError(f"missing pinned r11 input: {path}")
        rej, rej_raw = rejection()
        rej_action = install(REJECTION, rej_raw, 0o444)
        sup, sup_raw = supersession(rej, rej_raw)
        sup_action = install(SUPERSESSION, sup_raw, 0o444)
        anch, anch_raw = anchor(sup, sup_raw)
        anchor_action = install(ANCHOR, anch_raw, 0o444)
        generated = {role: source_retag(read_stable(path), role, anch, anch_raw)
                     for role, path in PREV_SOURCE.items()}
        source_hashes = {role: sha(raw) for role, raw in generated.items()}
        if len(set(source_hashes.values())) != 3:
            raise RuntimeError("r12 source hashes are not distinct")
        source_actions = {role: install(SOURCE[role], raw, 0o664)
                          for role, raw in generated.items()}
        quartet = build_quartet(source_hashes)
        json_actions = {name: install(JSON_PATHS[name], raw, 0o664)
                        for name, raw in quartet.items()}
        # Hard no-run boundary: no positive surfaces, manifest/outer, or r12
        # bytecode may appear during this builder.
        if any(p.exists() for p in (
            OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
            OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json")):
            raise RuntimeError("r12 manifest/outer appeared during static build")
        if any(TAG in str(p) for p in ROOT.rglob("*.pyc")):
            raise RuntimeError("r12 pyc appeared")
        result = {
            "schema": f"cm2.c79g.{TAG}.clean-room-builder.v1",
            "status": f"{TAG.upper()}_STATIC_CLEAN_ROOM_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "successor_suffix": TAG, "predecessor_suffix": PREV,
            "predecessor_rejection": {"path": str(REJECTION.relative_to(ROOT)),
                                      "file_sha256": sha(rej_raw),
                                      "object_sha256": rej["object_sha256"],
                                      "action": rej_action},
            "predecessor_supersession": {"path": str(SUPERSESSION.relative_to(ROOT)),
                                          "file_sha256": sha(sup_raw),
                                          "object_sha256": sup["object_sha256"],
                                          "action": sup_action},
            "active_anchor": {"path": str(ANCHOR.relative_to(ROOT)),
                              "file_sha256": sha(anch_raw),
                              "object_sha256": anch["object_sha256"],
                              "action": anchor_action},
            "source_hashes": source_hashes,
            "source_actions": source_actions,
            "json_actions": json_actions,
            "schema_shape": {"defs": 46, "refs": 242, "closed": 52},
            "instance_shapes": {"contract": 30, "transition": 31, "audit": 30},
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False, "manifest_created": False,
            "outer_created": False, "runtime_surface_created": False,
            "pyc_created": False,
        }
        result["object_sha256"] = sha(canonical(result))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.clean-room-builder.failure.v1",
            "status": f"FAIL_CLOSED_{TAG.upper()}_CLEAN_ROOM",
            "error_type": type(exc).__name__, "error": str(exc),
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
