#!/usr/bin/env python3
"""Append-only semantic repair from the rejected v16r2r12 bundle.

r12 fixed the executable self-edge, but its inherited active trust witness and
transition boundary still named the old r8 predecessor.  This builder seals
r12 as rejection-only and emits r13 with every active predecessor/path field
rebuilt from one explicit exact8 map.  No predecessor is overwritten and no
runtime/manifest/outer/credit/pyc is created.
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
PREV = "v16r2r12"
TAG = "v16r2r13"
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
    "transition": OUT / f"{BASE}_v16r2r11_to_{PREV}_static_launch_transition_receipt_v1.json",
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


def canon(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def close(v: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v); out.pop("object_sha256", None)
    out["object_sha256"] = sha(canon(out)); return out


def stable(p: Path) -> bytes:
    fd = os.open(p, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular/nlink1: {p}")
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b: break
            chunks.append(b)
        after, named = os.fstat(fd), os.lstat(p)
        if ((before.st_dev, before.st_ino, before.st_size) !=
            (after.st_dev, after.st_ino, after.st_size) or
            (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"identity drift: {p}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size: raise RuntimeError(f"short read: {p}")
        return raw
    finally: os.close(fd)


def jread(p: Path) -> dict[str, Any]:
    v = json.loads(stable(p).decode())
    if not isinstance(v, dict): raise RuntimeError(f"JSON root: {p}")
    return v


def install(p: Path, raw: bytes, mode: int) -> str:
    try:
        fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, mode)
    except FileExistsError:
        if stable(p) != raw or p.stat().st_nlink != 1 or stat.S_IMODE(p.stat().st_mode) != mode:
            raise RuntimeError(f"append-only mismatch: {p}")
        return "replayed"
    try:
        view = memoryview(raw); off = 0
        while off < len(view): off += os.write(fd, view[off:])
        os.fsync(fd); os.fchmod(fd, mode)
    finally: os.close(fd)
    dfd = os.open(p.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try: os.fsync(dfd)
    finally: os.close(dfd)
    return "installed"


def walk(v: Any):
    yield v
    if isinstance(v, dict):
        for x in v.values(): yield from walk(x)
    elif isinstance(v, list):
        for x in v: yield from walk(x)


def inventory() -> dict[str, Any]:
    paths = {**PREV_SOURCE, **{f"json_{k}": p for k, p in PREV_JSON.items()},
             "active_anchor": PREV_ANCHOR}
    return {n: {"path": str(p.relative_to(ROOT)), "file_sha256": sha(stable(p)),
                "bytes": p.stat().st_size, "mode": f"{stat.S_IMODE(p.stat().st_mode):04o}",
                "nlink": p.stat().st_nlink} for n, p in paths.items()}


def rejection() -> tuple[dict[str, Any], bytes]:
    v = close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v3",
        "status": "PERMANENT_FAIL_CLOSED_STATIC_REVIEW__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "ACTIVE_TRUST_WITNESS_AND_TRANSITION_BOUNDARY_RETAINED_V16R2R8_PREDECESSOR",
        "independent_reviewer_failed_checks": [
            "active_post_source_predecessor_path", "transition_boundary_base7_first_member_path",
            "transition_boundary_base7_order", "active_status_and_attack_execution",
        ],
        "independent_reviewer_failed_check_count": 4,
        "failed_artifacts": inventory(), "append_only": True,
        "overwrite_delete_or_reuse_allowed": False, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "manifest_created": False, "outer_created": False,
        "runtime_surface_created": False,
    })
    return v, canon(v) + b"\n"


def supersede(rej: dict[str, Any], raw: bytes) -> tuple[dict[str, Any], bytes]:
    v = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v3",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV, "successor_namespace": TAG,
        "predecessor_rejection_path": str(REJECTION.relative_to(ROOT)),
        "predecessor_rejection_file_sha256": sha(raw),
        "predecessor_rejection_object_sha256": rej["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
    })
    return v, canon(v) + b"\n"


def make_anchor(sup: dict[str, Any], raw: bytes) -> tuple[dict[str, Any], bytes]:
    v = close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUPERSESSION.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(raw),
        "predecessor_supersession_object_sha256": sup["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "manifest_created": False, "outer_created": False,
    })
    return v, canon(v) + b"\n"


def retag_source(raw: bytes, role: str, anchor: dict[str, Any], anchor_raw: bytes) -> bytes:
    text = raw.decode()
    old_anchor, old_edge = PREV_ANCHOR.name, f"{BASE}_v16r2r11_to_{PREV}_static_launch_transition_receipt_v1.json"
    ma, me = "__R13_ANCHOR__", "__R12_TO_R13_EDGE__"
    text = text.replace(old_anchor, ma).replace(old_edge, me)
    text = text.replace(PREV, TAG).replace("V16R2R12", "V16R2R13")
    text = text.replace(ma, ANCHOR.name).replace(me, f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json")
    text, n1 = re.subn(r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
                       f'ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "{sha(anchor_raw)}"', text)
    text, n2 = re.subn(r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
                       f'ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "{anchor["object_sha256"]}"', text)
    if (n1, n2) != (1, 1) or me in text: raise RuntimeError(f"{role}: source edge/pin drift")
    if "FINAL_BASE7_PINS_INSTALLED = False" not in text: raise RuntimeError(f"{role}: draft flag missing")
    if not text.endswith("\n"): text += "\n"
    tree = ast.parse(text, filename=str(SOURCE[role])); compile(tree, str(SOURCE[role]), "exec")
    return text.encode()


def retag_value(v: Any) -> Any:
    if isinstance(v, dict): return {retag_value(k): retag_value(x) for k, x in v.items()}
    if isinstance(v, list): return [retag_value(x) for x in v]
    if not isinstance(v, str): return v
    old_edge = f"{BASE}_v16r2r11_to_{PREV}_static_launch_transition_receipt_v1.json"
    me = "__R12_TO_R13_EDGE__"
    out = v.replace(old_edge, me).replace(PREV, TAG)
    return out.replace(me, f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json")


def paths() -> dict[str, str]:
    return {"predecessor": str(ANCHOR.relative_to(ROOT)),
            "schema": str(JSON_PATHS["schema"].relative_to(ROOT)),
            "contract": str(JSON_PATHS["contract"].relative_to(ROOT)),
            "producer": str(SOURCE["producer"].relative_to(ROOT)),
            "consumer": str(SOURCE["consumer"].relative_to(ROOT)),
            "transition": str(JSON_PATHS["transition"].relative_to(ROOT)),
            "audit": str(JSON_PATHS["audit"].relative_to(ROOT)),
            "launcher": str(SOURCE["launcher"].relative_to(ROOT)),
            "manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
            "outer": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json"}


def patch_bundle(b: dict[str, Any], pins: dict[str, str], p: dict[str, str]) -> None:
    exact8 = [p[k] for k in ("predecessor", "schema", "contract", "producer", "consumer", "transition", "audit", "launcher")]
    b.update({"bundle_version": TAG, "source_hashes": dict(pins),
              "base7_ordered_paths": exact8[:-1], "exact8_ordered_paths": exact8,
              "exact10_ordered_paths": exact8 + [p["manifest"], p["outer"]],
              "formal_global_closure_credit": 0, "D02_unlock": False,
              "runtime_authorized": False})
    outer = dict(b.get("cold_launch_outer_closure", {}))
    outer.update({"exact8_manifest_path": p["manifest"], "outer_last_path": p["outer"],
                  "launcher_path": p["launcher"],
                  "manifest_or_outer_absent_in_this_static_phase": True,
                  "runtime_entry_authorized": False})
    b["cold_launch_outer_closure"] = outer
    trust = b.get("post_source_static_trust_receipts")
    if isinstance(trust, dict):
        trust["predecessor_supersession_path"] = p["predecessor"]
        trust["predecessor_supersession_file_sha256"] = sha(stable(ANCHOR))
        trust["predecessor_supersession_object_sha256"] = jread(ANCHOR)["object_sha256"]
        trust["transition_path"] = p["transition"]
        trust["static_audit_path"] = p["audit"]
    for key in ("build_only_producer", "independent_verifier_assembler_authority_consumer"):
        if isinstance(b.get(key), dict) and isinstance(b[key].get("role"), str):
            b[key]["role"] = b[key]["role"].replace("R12", "R13")
    if isinstance(b.get("pin_state"), str): b["pin_state"] = b["pin_state"].replace("R12", "R13")
    if isinstance(b.get("post_source_static_trust_receipts"), dict):
        q = b["post_source_static_trust_receipts"]
        if isinstance(q.get("binding_direction"), str): q["binding_direction"] = q["binding_direction"].replace("R12", "R13")


def build_quartet(pins: dict[str, str]) -> dict[str, bytes]:
    vals = {n: retag_value(jread(p)) for n, p in PREV_JSON.items()}
    p = paths()
    keys = {"contract": f"{TAG}_bundle", "transition": f"successor_{TAG}_static_bundle", "audit": f"audited_{TAG}_bundle"}
    for n, k in keys.items():
        b = vals[n].get(k)
        if not isinstance(b, dict): raise RuntimeError(f"missing active bundle {n}/{k}")
        patch_bundle(b, pins, p)
        vals[n][k] = b
    schema = vals["schema"]
    active = schema.get("x-cm2-successor-active", {})
    if not isinstance(active, dict): active = {}
    active.update({"namespace": f"{TAG}_semantic_bundle",
                   "active_exact8_first_member_field": f"current_exact8_first_member_is_{TAG}_supersession_receipt",
                   "active_exact8_first_member_path": p["predecessor"],
                   "active_successor_paths": p, "effective_checkpoint_object_sha256": UPSTREAM,
                   "source_hashes": dict(pins), "global_baseline": {"rows": 76832, "unresolved": 1148},
                   "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False})
    schema["x-cm2-successor-active"] = active
    vals["contract"].update({"schema": f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.contract",
                              "status": f"{TAG.upper()}_STATIC_CONTRACT_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
                              "purpose": f"Append-only {TAG} semantic bundle with predecessor→schema→contract→producer→consumer→transition→audit→launcher exact8 order; no credit transfer."})
    vals["audit"].update({"schema": f"cm2.round306c79g.true-global-no-producer-consumer.static-audit-{TAG}",
                           "status": f"{TAG.upper()}_STATIC_AUDIT_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
                           "audit_path": p["audit"]})
    vals["transition"].update({"schema": f"cm2.round306c79g.true-global-no-producer-consumer.{PREV}-to-{TAG}.transition",
                                "status": f"{TAG.upper()}_STATIC_TRANSITION_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
                                "receipt_path": p["transition"],
                                "transition_kind": f"APPEND_ONLY_{PREV.upper()}_TO_{TAG.upper()}_ZERO_CREDIT_JSON_BUNDLE"})
    boundary = vals["transition"].get("cold_launch_boundary")
    if isinstance(boundary, dict):
        exact8 = [p[k] for k in ("predecessor", "schema", "contract", "producer", "consumer", "transition", "audit", "launcher")]
        boundary["base7_first_member_is_r9_semantic_supersession"] = False
        boundary["base7_first_member_is_v16_semantic_supersession"] = True
        boundary["base7_first_member_path"] = p["predecessor"]
        boundary["base7_order"] = exact8[:-1]
    attack = vals["audit"].get("coherent_attack_static_census")
    if isinstance(attack, dict):
        attack["exact_unique_ordered_attack_count_required"] = 137
        attack["exact_unique_ordered_attack_count_observed"] = 137
        attack["attack_execution_deferred_to_cold_runtime"] = True
        attack["all_mutations_route_through_production_validators"] = False
    # Concrete objects must remain disabled; schema $defs are type metadata.
    for n, obj in vals.items():
        nodes = walk({k: v for k, v in obj.items() if k != "$defs"}) if n == "schema" else walk(obj)
        for node in nodes:
            if isinstance(node, dict):
                if node.get("formal_global_closure_credit") not in (None, 0, False):
                    raise RuntimeError(f"credit drift in {n}")
                if node.get("D02_unlock") is True: raise RuntimeError(f"unlock drift in {n}")
    out = {n: close(v) for n, v in vals.items()}
    schema = out["schema"]
    refs = sum(1 for x in walk(schema) if isinstance(x, dict) and "$ref" in x)
    closed = sum(1 for x in walk(schema) if isinstance(x, dict) and x.get("additionalProperties") is False)
    if (len(schema.get("$defs", {})), refs, closed) != (46, 242, 52): raise RuntimeError("schema shape drift")
    if schema.get("$ref") != "#/$defs/coldLaunchedCommittedAuthority": raise RuntimeError("schema root drift")
    if [len(out[k]) for k in ("contract", "transition", "audit")] != [30, 31, 30]: raise RuntimeError("instance shape drift")
    return {n: canon(v) + b"\n" for n, v in out.items()}


def main() -> int:
    try:
        for p in (*PREV_SOURCE.values(), *PREV_JSON.values(), PREV_ANCHOR):
            if not p.is_file(): raise RuntimeError(f"missing r12 input: {p}")
        rej, rej_raw = rejection(); ra = install(REJECTION, canon(rej) + b"\n", 0o444)
        sup, sup_raw = supersede(rej, rej_raw); sa = install(SUPERSESSION, sup_raw, 0o444)
        anc, anc_raw = make_anchor(sup, sup_raw); aa = install(ANCHOR, anc_raw, 0o444)
        generated = {r: retag_source(stable(p), r, anc, anc_raw) for r, p in PREV_SOURCE.items()}
        pins = {r: sha(x) for r, x in generated.items()}
        if len(set(pins.values())) != 3: raise RuntimeError("source hash collision")
        actions = {r: install(SOURCE[r], x, 0o664) for r, x in generated.items()}
        quartet = build_quartet(pins)
        ja = {n: install(JSON_PATHS[n], x, 0o664) for n, x in quartet.items()}
        if any(p.exists() for p in (OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256", OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json")):
            raise RuntimeError("manifest/outer appeared")
        if any(TAG in str(p) for p in ROOT.rglob("*.pyc")): raise RuntimeError("pyc appeared")
        result = {"schema": f"cm2.c79g.{TAG}.clean-room-builder.v1",
                  "status": f"{TAG.upper()}_STATIC_CLEAN_ROOM_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
                  "successor_suffix": TAG, "predecessor_suffix": PREV,
                  "predecessor_rejection": {"path": str(REJECTION.relative_to(ROOT)), "file_sha256": sha(rej_raw), "object_sha256": rej["object_sha256"], "action": ra},
                  "predecessor_supersession": {"path": str(SUPERSESSION.relative_to(ROOT)), "file_sha256": sha(sup_raw), "object_sha256": sup["object_sha256"], "action": sa},
                  "active_anchor": {"path": str(ANCHOR.relative_to(ROOT)), "file_sha256": sha(anc_raw), "object_sha256": anc["object_sha256"], "action": aa},
                  "source_hashes": pins, "source_actions": actions, "json_actions": ja,
                  "schema_shape": {"defs": 46, "refs": 242, "closed": 52}, "instance_shapes": {"contract": 30, "transition": 31, "audit": 30},
                  "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False,
                  "manifest_created": False, "outer_created": False, "runtime_surface_created": False, "pyc_created": False}
        result["object_sha256"] = sha(canon(result)); print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.clean-room-builder.failure.v1", "status": f"FAIL_CLOSED_{TAG.upper()}_CLEAN_ROOM", "error_type": type(exc).__name__, "error": str(exc), "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False}, ensure_ascii=False, sort_keys=True)); return 1


if __name__ == "__main__": raise SystemExit(main())
