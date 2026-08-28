#!/usr/bin/env python3
"""Create the append-only C79g v16r2r11 static clean-room.

This version closes the r9/r10 rejection chain explicitly and uses one
coherent tag for sources, JSON objects, and the predecessor-to-successor
transition path.  All writes use O_EXCL.  No predecessor is modified and no
manifest, outer receipt, runtime surface, authority, credit, or bytecode is
created.
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
PREV = "v16r2r10"
TAG = "v16r2r11"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"

R9_SOURCE = {
    "producer": OUT / f"{BASE}_v16r2r9_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r9_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_v16r2r9_semantic_source.py",
}
R9_JSON = {
    "schema": OUT / f"{BASE}_schema_v16r9.json",
    "contract": OUT / f"{BASE}_contract_v16r9.json",
    "transition": OUT / f"{BASE}_v16r8_to_v16r9_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v16r9.json",
}
R9_ANCHOR = OUT / f"{BASE}_v16r2r9_active_predecessor_supersession_receipt_v1.json"

PREV_SOURCE = {
    "producer": OUT / f"{BASE}_{PREV}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
}
PREV_JSON = {
    "schema": OUT / f"{BASE}_schema_{PREV}.json",
    "contract": OUT / f"{BASE}_contract_{PREV}.json",
    "transition": OUT / f"{BASE}_v16r2r9_to_{PREV}_static_launch_transition_receipt_v1.json",
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

R9_REJECTION = OUT / f"{BASE}_v16r2r9_static_bundle_rejection_receipt_v1.json"
R9_TO_R10 = OUT / f"{BASE}_v16r2r9_to_v16r2r10_static_bundle_rejection_supersession_receipt_v1.json"
R10_REJECTION = OUT / f"{BASE}_v16r2r10_static_bundle_rejection_receipt_v1.json"
R10_TO_R11 = OUT / f"{BASE}_v16r2r10_to_v16r2r11_static_bundle_rejection_supersession_receipt_v1.json"
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    claim = sha(canonical(body))
    body["object_sha256"] = claim
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


def file_inventory(paths: dict[str, Path], anchor: Path) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, path in {**paths, "active_anchor": anchor}.items():
        raw = read_stable(path)
        st = path.stat()
        result[name] = {
            "path": str(path.relative_to(ROOT)), "file_sha256": sha(raw),
            "bytes": len(raw), "mode": f"{stat.S_IMODE(st.st_mode):04o}",
            "nlink": st.st_nlink,
        }
    return result


def rejection_receipt(namespace: str, files: dict[str, Any],
                      failed_checks: list[str], reason: str,
                      predecessor_chain: dict[str, Any] | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": f"cm2.c79g.{namespace}.static-bundle-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_STATIC_REVIEW__ZERO_CREDIT",
        "failed_namespace": namespace,
        "rejection_reason": reason,
        "independent_reviewer_failed_checks": failed_checks,
        "independent_reviewer_failed_check_count": len(failed_checks),
        "failed_artifacts": files,
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
        "runtime_surface_created": False,
    }
    if predecessor_chain is not None:
        body["predecessor_chain_supersession"] = predecessor_chain
    return close_object(body)


def supersession_receipt(predecessor: str, successor: str,
                         rejection_path: Path, rejection: dict[str, Any],
                         rejection_raw: bytes,
                         predecessor_chain: dict[str, Any] | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": f"cm2.c79g.{predecessor}-to-{successor}.static-bundle-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": predecessor,
        "successor_namespace": successor,
        "predecessor_rejection_path": str(rejection_path.relative_to(ROOT)),
        "predecessor_rejection_file_sha256": sha(rejection_raw),
        "predecessor_rejection_object_sha256": rejection["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "append_only": True,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    }
    if predecessor_chain is not None:
        body["predecessor_chain_supersession"] = predecessor_chain
    return close_object(body)


def receipt_ref(path: Path, value: dict[str, Any], raw: bytes) -> dict[str, Any]:
    return {"path": str(path.relative_to(ROOT)), "file_sha256": sha(raw),
            "object_sha256": value["object_sha256"]}


def build_rejection_chain() -> tuple[dict[str, Any], dict[str, str]]:
    r9_files = file_inventory({**R9_SOURCE, **{f"json_{k}": v for k, v in R9_JSON.items()}}, R9_ANCHOR)
    r9_failed = [
        "final_flags_false", "json_closed_utf8", "schema_full_shape",
        "schema_root_ref", "instance_shapes_closed", "zero_credit_baseline",
        "exact8_order", "source_pin_consistency",
    ]
    r9_rej = rejection_receipt(
        "v16r2r9", r9_files, r9_failed,
        "EXECUTABLE_SOURCE_SUFFIX_AND_STATIC_JSON_SUFFIX_DIVERGED",
    )
    r9_rej_raw = canonical(r9_rej) + b"\n"
    r9_rej_action = install(R9_REJECTION, r9_rej_raw, 0o444)
    r9_to_r10 = supersession_receipt(
        "v16r2r9", "v16r2r10", R9_REJECTION, r9_rej, r9_rej_raw)
    r9_to_r10_raw = canonical(r9_to_r10) + b"\n"
    r9_to_r10_action = install(R9_TO_R10, r9_to_r10_raw, 0o444)
    r9_chain = receipt_ref(R9_TO_R10, r9_to_r10, r9_to_r10_raw)

    r10_files = file_inventory({**PREV_SOURCE, **{f"json_{k}": v for k, v in PREV_JSON.items()}}, PREV_ANCHOR)
    r10_failed = ["json_closed_utf8", "instance_shapes_closed",
                  "zero_credit_baseline", "exact8_order",
                  "source_pin_consistency"]
    r10_rej = rejection_receipt(
        "v16r2r10", r10_files, r10_failed,
        "GENERIC_REVIEWER_TRANSITION_PATH_EXPECTATION_DID_NOT_MATCH_PREDECESSOR_TO_SUCCESSOR_PATH",
        r9_chain,
    )
    r10_rej_raw = canonical(r10_rej) + b"\n"
    r10_rej_action = install(R10_REJECTION, r10_rej_raw, 0o444)
    r10_to_r11 = supersession_receipt(
        "v16r2r10", "v16r2r11", R10_REJECTION, r10_rej, r10_rej_raw,
        r9_chain,
    )
    r10_to_r11_raw = canonical(r10_to_r11) + b"\n"
    r10_to_r11_action = install(R10_TO_R11, r10_to_r11_raw, 0o444)
    actions = {
        "r9_rejection": r9_rej_action, "r9_to_r10": r9_to_r10_action,
        "r10_rejection": r10_rej_action, "r10_to_r11": r10_to_r11_action,
    }
    return r10_to_r11, actions


def make_anchor(immediate: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    immediate_raw = read_stable(R10_TO_R11)
    body = {
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(R10_TO_R11.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(immediate_raw),
        "predecessor_supersession_object_sha256": immediate["object_sha256"],
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


def recursive_retag(value: Any) -> Any:
    if isinstance(value, dict):
        return {recursive_retag(k): recursive_retag(v) for k, v in value.items()}
    if isinstance(value, list):
        return [recursive_retag(v) for v in value]
    if not isinstance(value, str):
        return value
    replacements = (
        (PREV_JSON["transition"].name, JSON_PATHS["transition"].name),
        (PREV_ANCHOR.name, ANCHOR.name),
        (PREV_SOURCE["consumer"].name, SOURCE["consumer"].name),
        (PREV_SOURCE["launcher"].name, SOURCE["launcher"].name),
        (PREV_SOURCE["producer"].name, SOURCE["producer"].name),
        (PREV_JSON["schema"].name, JSON_PATHS["schema"].name),
        (PREV_JSON["contract"].name, JSON_PATHS["contract"].name),
        (PREV_JSON["audit"].name, JSON_PATHS["audit"].name),
        (f"{BASE}_cold_launch_manifest_{PREV}.sha256",
         f"{BASE}_cold_launch_manifest_{TAG}.sha256"),
        (f"{BASE}_cold_launch_outer_receipt_{PREV}.json",
         f"{BASE}_cold_launch_outer_receipt_{TAG}.json"),
        (PREV, TAG),
        ("V16R2R10", "V16R2R11"),
    )
    result = value
    for old, new in replacements:
        result = result.replace(old, new)
    return result


def source_retag(raw: bytes, role: str, anchor: dict[str, Any],
                 anchor_raw: bytes) -> bytes:
    text = recursive_retag(raw.decode("utf-8"))
    text, file_count = re.subn(
        r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
        f'ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "{sha(anchor_raw)}"', text)
    text, object_count = re.subn(
        r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
        f'ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "{anchor["object_sha256"]}"', text)
    if (file_count, object_count) != (1, 1):
        raise RuntimeError(f"{role}: active anchor assignment count drift")
    if "FINAL_BASE7_PINS_INSTALLED = False" not in text:
        marker = "RUNTIME_AUTHORIZED = False\n"
        if marker not in text:
            raise RuntimeError(f"{role}: runtime marker absent")
        text = text.replace(marker, marker + "FINAL_BASE7_PINS_INSTALLED = False\n", 1)
    if not text.endswith("\n"):
        text += "\n"
    tree = ast.parse(text, filename=str(SOURCE[role]))
    compile(tree, str(SOURCE[role]), "exec")
    if TAG not in text or "SOURCE_TEMPLATE_ONLY" in text:
        raise RuntimeError(f"{role}: executable successor marker failure")
    return text.encode("utf-8")


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def patch_bundle(bundle: dict[str, Any], source_hashes: dict[str, str],
                 exact8: list[str], paths: dict[str, str]) -> None:
    bundle["bundle_version"] = TAG
    bundle["source_hashes"] = dict(source_hashes)
    bundle["exact8_ordered_paths"] = list(exact8)
    bundle["base7_ordered_paths"] = list(exact8[:-1])
    outer = dict(bundle.get("cold_launch_outer_closure", {}))
    outer.update({"launcher_path": paths["launcher"],
                  "exact8_manifest_path": paths["manifest"],
                  "outer_last_path": paths["outer"],
                  "manifest_or_outer_absent_in_this_static_phase": True,
                  "runtime_entry_authorized": False})
    bundle["cold_launch_outer_closure"] = outer
    bundle["formal_global_closure_credit"] = 0
    bundle["D02_unlock"] = False
    bundle["runtime_authorized"] = False


def make_quartet(source_hashes: dict[str, str]) -> dict[str, bytes]:
    values = {name: recursive_retag(read_json(path))
              for name, path in PREV_JSON.items()}
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
    schema = values["schema"]
    active = copy.deepcopy(schema.get("x-cm2-successor-active", {}))
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
    bundle_keys = {
        "contract": f"{TAG}_bundle",
        "transition": f"successor_{TAG}_static_bundle",
        "audit": f"audited_{TAG}_bundle",
    }
    for name, key in bundle_keys.items():
        bundle = values[name].get(key)
        if not isinstance(bundle, dict):
            raise RuntimeError(f"missing active bundle {name}/{key}")
        patch_bundle(bundle, source_hashes, exact8, paths)
    out = {name: close_object(value) for name, value in values.items()}
    refs = sum(1 for node in walk(out["schema"])
               if isinstance(node, dict) and "$ref" in node)
    closed = sum(1 for node in walk(out["schema"])
                 if isinstance(node, dict) and node.get("additionalProperties") is False)
    if (len(out["schema"].get("$defs", {})), refs, closed) != (46, 242, 52):
        raise RuntimeError("schema structural shape drift")
    if [len(out[k]) for k in ("contract", "transition", "audit")] != [30, 31, 30]:
        raise RuntimeError("instance structural shape drift")
    # Concrete instances must be zero-credit.  Schema definitions may model
    # the later positive authority state and are therefore deliberately not
    # interpreted as concrete persisted values here.
    for name in ("contract", "transition", "audit"):
        for node in walk(out[name]):
            if not isinstance(node, dict):
                continue
            for key in ("formal_global_closure_credit", "all_persisted_credit"):
                if key in node and node[key] not in (0, False, None):
                    raise RuntimeError(f"{name}: nonzero concrete {key}")
    return {name: canonical(value) + b"\n" for name, value in out.items()}


def main() -> int:
    try:
        all_inputs = (*R9_SOURCE.values(), *R9_JSON.values(), R9_ANCHOR,
                      *PREV_SOURCE.values(), *PREV_JSON.values(), PREV_ANCHOR)
        for path in all_inputs:
            if not path.is_file():
                raise RuntimeError(f"missing input: {path}")
        immediate, chain_actions = build_rejection_chain()
        anchor, anchor_raw = make_anchor(immediate)
        anchor_action = install(ANCHOR, anchor_raw, 0o444)
        generated = {role: source_retag(read_stable(path), role, anchor, anchor_raw)
                     for role, path in PREV_SOURCE.items()}
        source_hashes = {role: sha(raw) for role, raw in generated.items()}
        source_actions = {role: install(SOURCE[role], raw, 0o664)
                          for role, raw in generated.items()}
        quartet = make_quartet(source_hashes)
        json_actions = {name: install(JSON_PATHS[name], raw, 0o664)
                        for name, raw in quartet.items()}
        result = {
            "schema": "cm2.c79g.v16r2r11.clean-room-builder.v1",
            "status": "V16R2R11_STATIC_CLEAN_ROOM_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "successor_suffix": TAG, "predecessor_suffix": PREV,
            "rejection_chain_actions": chain_actions,
            "active_anchor": {"path": str(ANCHOR.relative_to(ROOT)),
                              "file_sha256": sha(anchor_raw),
                              "object_sha256": anchor["object_sha256"],
                              "action": anchor_action},
            "source_hashes": source_hashes,
            "source_actions": source_actions, "json_actions": json_actions,
            "schema_shape": {"defs": 46, "refs": 242, "closed": 52},
            "instance_shapes": {"contract": 30, "transition": 31, "audit": 30},
            "transition_path": str(JSON_PATHS["transition"].relative_to(ROOT)),
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
            "schema": "cm2.c79g.v16r2r11.clean-room-builder.failure.v1",
            "status": "FAIL_CLOSED_R11_CLEAN_ROOM",
            "error_type": type(exc).__name__, "error": str(exc),
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False,
        }, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
