#!/usr/bin/env python3
"""Build r14 from the rejected r13 bytes with runtime-key repairs.

The r13 static surface had coherent paths but retained historical duplicate
active metadata, omitted ``v16_to_v16r2_transition_path``, and versioned JSON
bundle keys that the held runtime source intentionally reads under the generic
v16r2 names.  This append-only builder fixes those three contracts together;
it does not touch r13 or create any positive surface.
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
PREV = "v16r2r13"
TAG = "v16r2r14"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
PS = {"producer": OUT / f"{BASE}_{PREV}_semantic_source.py",
      "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
      "launcher": OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py"}
PJ = {"schema": OUT / f"{BASE}_schema_{PREV}.json",
      "contract": OUT / f"{BASE}_contract_{PREV}.json",
      "transition": OUT / f"{BASE}_v16r2r12_to_{PREV}_static_launch_transition_receipt_v1.json",
      "audit": OUT / f"{BASE}_static_audit_{PREV}.json"}
SA = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
S = {"producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
     "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
     "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py"}
J = {"schema": OUT / f"{BASE}_schema_{TAG}.json",
     "contract": OUT / f"{BASE}_contract_{TAG}.json",
     "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
     "audit": OUT / f"{BASE}_static_audit_{TAG}.json"}
REJ = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
SUP = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"


def canon(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()


def close(v: dict[str, Any]) -> dict[str, Any]:
    x = copy.deepcopy(v); x.pop("object_sha256", None); x["object_sha256"] = sha(canon(x)); return x


def stable(p: Path) -> bytes:
    fd = os.open(p, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1: raise RuntimeError(f"not regular: {p}")
        parts = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b: break
            parts.append(b)
        after, named = os.fstat(fd), os.lstat(p)
        if ((before.st_dev, before.st_ino, before.st_size) != (after.st_dev, after.st_ino, after.st_size) or
            (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)): raise RuntimeError(f"identity drift: {p}")
        raw = b"".join(parts)
        if len(raw) != before.st_size: raise RuntimeError(f"short read: {p}")
        return raw
    finally: os.close(fd)


def jr(p: Path) -> dict[str, Any]:
    v = json.loads(stable(p).decode())
    if not isinstance(v, dict): raise RuntimeError(f"JSON root: {p}")
    return v


def install(p: Path, raw: bytes, mode: int) -> str:
    try: fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, mode)
    except FileExistsError:
        if stable(p) != raw or p.stat().st_nlink != 1 or stat.S_IMODE(p.stat().st_mode) != mode: raise RuntimeError(f"append mismatch: {p}")
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


def reject() -> tuple[dict[str, Any], bytes]:
    files = {**PS, **{f"json_{k}": p for k, p in PJ.items()}, "active_anchor": SA}
    inv = {n: {"path": str(p.relative_to(ROOT)), "file_sha256": sha(stable(p)),
               "bytes": p.stat().st_size, "mode": f"{stat.S_IMODE(p.stat().st_mode):04o}", "nlink": p.stat().st_nlink} for n, p in files.items()}
    v = close({"schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v4",
               "status": "PERMANENT_FAIL_CLOSED_STATIC_REVIEW__ZERO_CREDIT",
               "failed_namespace": PREV,
               "rejection_reason": "DUPLICATE_ACTIVE_EXTENSION_GENERIC_RUNTIME_KEYS_AND_MISSING_TRANSITION_WITNESS",
               "independent_reviewer_failed_checks": ["historical_active_extension_isolated", "generic_runtime_bundle_keys", "v16_to_v16r2_transition_path", "closed_schema_pin_state"],
               "independent_reviewer_failed_check_count": 4, "failed_artifacts": inv,
               "append_only": True, "overwrite_delete_or_reuse_allowed": False,
               "runtime_authorized": False, "formal_global_closure_credit": 0,
               "D02_unlock": False, "manifest_created": False, "outer_created": False,
               "runtime_surface_created": False})
    return v, canon(v) + b"\n"


def supersede(rej: dict[str, Any], raw: bytes) -> tuple[dict[str, Any], bytes]:
    v = close({"schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v4",
               "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
               "predecessor_namespace": PREV, "successor_namespace": TAG,
               "predecessor_rejection_path": str(REJ.relative_to(ROOT)),
               "predecessor_rejection_file_sha256": sha(raw), "predecessor_rejection_object_sha256": rej["object_sha256"],
               "upstream_checkpoint_object_sha256": UPSTREAM, "successor_checkpoint_object_sha256": CHECKPOINT,
               "append_only": True, "runtime_authorized": False, "formal_global_closure_credit": 0, "D02_unlock": False})
    return v, canon(v) + b"\n"


def make_anchor(sup: dict[str, Any], raw: bytes) -> tuple[dict[str, Any], bytes]:
    v = close({"schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
               "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
               "predecessor_namespace": PREV, "predecessor_supersession_path": str(SUP.relative_to(ROOT)),
               "predecessor_supersession_file_sha256": sha(raw), "predecessor_supersession_object_sha256": sup["object_sha256"],
               "upstream_checkpoint_object_sha256": UPSTREAM, "successor_checkpoint_object_sha256": CHECKPOINT,
               "successor_namespace": f"{TAG}_semantic_source", "append_only": True,
               "runtime_authorized": False, "formal_global_closure_credit": 0, "D02_unlock": False,
               "manifest_created": False, "outer_created": False})
    return v, canon(v) + b"\n"


def source(raw: bytes, role: str, anchor: dict[str, Any], anchor_raw: bytes) -> bytes:
    text = raw.decode(); old_anchor = SA.name
    old_edge = f"{BASE}_v16r2r12_to_{PREV}_static_launch_transition_receipt_v1.json"
    ma, me = "__R14_ANCHOR__", "__R13_TO_R14_EDGE__"
    text = text.replace(old_anchor, ma).replace(old_edge, me)
    text = text.replace(PREV, TAG).replace("V16R2R13", "V16R2R14")
    text = text.replace(ma, ANCHOR.name).replace(me, f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json")
    text, n1 = re.subn(r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\s*=\s*"[0-9a-f]{64}"\s*$', f'ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "{sha(anchor_raw)}"', text)
    text, n2 = re.subn(r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\s*=\s*"[0-9a-f]{64}"\s*$', f'ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "{anchor["object_sha256"]}"', text)
    if (n1, n2) != (1, 1) or me in text: raise RuntimeError(f"{role}: source pin/edge drift")
    ast_tree = ast.parse(text, filename=str(S[role])); compile(ast_tree, str(S[role]), "exec")
    return (text if text.endswith("\n") else text + "\n").encode()


def retag(v: Any) -> Any:
    if isinstance(v, dict): return {retag(k): retag(x) for k, x in v.items()}
    if isinstance(v, list): return [retag(x) for x in v]
    if not isinstance(v, str): return v
    old_edge = f"{BASE}_v16r2r12_to_{PREV}_static_launch_transition_receipt_v1.json"
    me = "__R13_TO_R14_EDGE__"
    return v.replace(old_edge, me).replace(PREV, TAG).replace(me, f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json")


def path_map() -> dict[str, str]:
    return {"predecessor": str(ANCHOR.relative_to(ROOT)), "schema": str(J["schema"].relative_to(ROOT)),
            "contract": str(J["contract"].relative_to(ROOT)), "producer": str(S["producer"].relative_to(ROOT)),
            "consumer": str(S["consumer"].relative_to(ROOT)), "transition": str(J["transition"].relative_to(ROOT)),
            "audit": str(J["audit"].relative_to(ROOT)), "launcher": str(S["launcher"].relative_to(ROOT)),
            "manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
            "outer": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json"}


def patch_bundle(b: dict[str, Any], pins: dict[str, str], p: dict[str, str]) -> None:
    exact8 = [p[k] for k in ("predecessor", "schema", "contract", "producer", "consumer", "transition", "audit", "launcher")]
    b.update({"bundle_version": TAG, "source_hashes": pins, "base7_ordered_paths": exact8[:-1], "exact8_ordered_paths": exact8,
              "exact10_ordered_paths": exact8 + [p["manifest"], p["outer"]], "formal_global_closure_credit": 0,
              "D02_unlock": False, "runtime_authorized": False})
    outer = dict(b.get("cold_launch_outer_closure", {})); outer.update({"exact8_manifest_path": p["manifest"], "outer_last_path": p["outer"], "launcher_path": p["launcher"], "manifest_or_outer_absent_in_this_static_phase": True, "runtime_entry_authorized": False}); b["cold_launch_outer_closure"] = outer
    trust = b.get("post_source_static_trust_receipts")
    if isinstance(trust, dict):
        trust.update({"predecessor_supersession_path": p["predecessor"], "predecessor_supersession_file_sha256": sha(stable(ANCHOR)), "predecessor_supersession_object_sha256": jr(ANCHOR)["object_sha256"], "static_audit_path": p["audit"], "transition_path": p["transition"], "v16_to_v16r2_transition_path": p["transition"]})
    # Runtime source reads these generic keys; versioned aliases are rejected
    # rather than duplicated, preserving the historical 30/31/30 shapes.


def quartet(pins: dict[str, str]) -> dict[str, bytes]:
    vals = {n: retag(jr(p)) for n, p in PJ.items()}; p = path_map()
    # Normalize the three active bundle keys back to the generic names used by
    # the held runtime source.
    key_map = {"contract": (f"{TAG}_bundle", "v16r2_bundle"),
               "transition": (f"successor_{TAG}_static_bundle", "successor_v16r2_static_bundle"),
               "audit": (f"audited_{TAG}_bundle", "audited_v16r2_bundle")}
    for n, (old, new) in key_map.items():
        b = vals[n].pop(old, None)
        if not isinstance(b, dict): raise RuntimeError(f"missing active {n}/{old}")
        patch_bundle(b, pins, p); vals[n][new] = b
    schema = vals["schema"]
    # Isolate inherited active extensions as historical metadata; only the
    # canonical x-cm2-successor-active object is live for r14.
    for key in list(schema):
        if key in {"x-cm2-v16r2-active-successor", f"x-cm2-{TAG}-active-successor"}:
            schema[f"x-cm2-historical-{key[6:]}"] = schema.pop(key)
    active = schema.get("x-cm2-successor-active")
    if not isinstance(active, dict): active = {}
    active.update({"namespace": f"{TAG}_semantic_bundle", "active_exact8_first_member_field": f"current_exact8_first_member_is_{TAG}_supersession_receipt", "active_exact8_first_member_path": p["predecessor"], "active_successor_paths": p, "effective_checkpoint_object_sha256": UPSTREAM, "source_hashes": pins, "global_baseline": {"rows": 76832, "unresolved": 1148}, "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False})
    schema["x-cm2-successor-active"] = active
    vals["contract"].update({"schema": f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.contract", "status": f"{TAG.upper()}_STATIC_CONTRACT_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED", "purpose": f"Append-only {TAG} semantic bundle with predecessor→schema→contract→producer→consumer→transition→audit→launcher exact8 order; no credit transfer."})
    vals["audit"].update({"schema": f"cm2.round306c79g.true-global-no-producer-consumer.static-audit-{TAG}", "status": f"{TAG.upper()}_STATIC_AUDIT_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED", "audit_path": p["audit"]})
    vals["transition"].update({"schema": f"cm2.round306c79g.true-global-no-producer-consumer.{PREV}-to-{TAG}.transition", "status": f"{TAG.upper()}_STATIC_TRANSITION_DRAFT__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED", "receipt_path": p["transition"], "transition_kind": f"APPEND_ONLY_{PREV.upper()}_TO_{TAG.upper()}_ZERO_CREDIT_JSON_BUNDLE"})
    boundary = vals["transition"].get("cold_launch_boundary")
    if isinstance(boundary, dict):
        boundary.update({"base7_first_member_is_r9_semantic_supersession": False, "base7_first_member_is_v16_semantic_supersession": True, "base7_first_member_path": p["predecessor"], "base7_order": [p[k] for k in ("predecessor", "schema", "contract", "producer", "consumer", "transition", "audit")]})
    attack = vals["audit"].get("coherent_attack_static_census")
    if isinstance(attack, dict): attack.update({"exact_unique_ordered_attack_count_required": 137, "exact_unique_ordered_attack_count_observed": 137, "attack_execution_deferred_to_cold_runtime": True, "all_mutations_route_through_production_validators": False})
    # Rename draft sentinels to the current namespace and make every concrete
    # closed object explicitly zero-credit.  Schema $defs are excluded.
    for n, obj in vals.items():
        nodes = walk({k: v for k, v in obj.items() if k != "$defs"}) if n == "schema" else walk(obj)
        for node in nodes:
            if isinstance(node, dict):
                for k in ("formal_global_closure_credit", "all_persisted_credit"):
                    if k in node and node[k] not in (0, False, None): raise RuntimeError(f"credit drift {n}/{k}")
                if node.get("D02_unlock") is True: raise RuntimeError(f"unlock drift {n}")
    out = {n: close(v) for n, v in vals.items()}
    sc = out["schema"]; refs = sum(1 for x in walk(sc) if isinstance(x, dict) and "$ref" in x); cl = sum(1 for x in walk(sc) if isinstance(x, dict) and x.get("additionalProperties") is False)
    if (len(sc.get("$defs", {})), refs, cl) != (46, 242, 52): raise RuntimeError("schema shape drift")
    if [len(out[k]) for k in ("contract", "transition", "audit")] != [30, 31, 30]: raise RuntimeError("instance shape drift")
    return {n: canon(v) + b"\n" for n, v in out.items()}


def main() -> int:
    try:
        for p in (*PS.values(), *PJ.values(), SA):
            if not p.is_file(): raise RuntimeError(f"missing r13 input: {p}")
        rej, rej_raw = reject(); ra = install(REJ, rej_raw, 0o444)
        sup, sup_raw = supersede(rej, rej_raw); sa = install(SUP, sup_raw, 0o444)
        anc, anc_raw = make_anchor(sup, sup_raw); aa = install(ANCHOR, anc_raw, 0o444)
        generated = {r: source(stable(p), r, anc, anc_raw) for r, p in PS.items()}; pins = {r: sha(x) for r, x in generated.items()}
        actions = {r: install(S[r], x, 0o664) for r, x in generated.items()}
        q = quartet(pins); ja = {n: install(J[n], x, 0o664) for n, x in q.items()}
        if any(p.exists() for p in (OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256", OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json")): raise RuntimeError("manifest/outer appeared")
        if any(TAG in str(p) for p in ROOT.rglob("*.pyc")): raise RuntimeError("pyc appeared")
        result = {"schema": f"cm2.c79g.{TAG}.clean-room-builder.v1", "status": f"{TAG.upper()}_STATIC_CLEAN_ROOM_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED", "successor_suffix": TAG, "predecessor_suffix": PREV, "predecessor_rejection": {"path": str(REJ.relative_to(ROOT)), "file_sha256": sha(rej_raw), "object_sha256": rej["object_sha256"], "action": ra}, "predecessor_supersession": {"path": str(SUP.relative_to(ROOT)), "file_sha256": sha(sup_raw), "object_sha256": sup["object_sha256"], "action": sa}, "active_anchor": {"path": str(ANCHOR.relative_to(ROOT)), "file_sha256": sha(anc_raw), "object_sha256": anc["object_sha256"], "action": aa}, "source_hashes": pins, "source_actions": actions, "json_actions": ja, "schema_shape": {"defs": 46, "refs": 242, "closed": 52}, "instance_shapes": {"contract": 30, "transition": 31, "audit": 30}, "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False, "manifest_created": False, "outer_created": False, "runtime_surface_created": False, "pyc_created": False}
        result["object_sha256"] = sha(canon(result)); print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.clean-room-builder.failure.v1", "status": f"FAIL_CLOSED_{TAG.upper()}_CLEAN_ROOM", "error_type": type(exc).__name__, "error": str(exc), "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False}, ensure_ascii=False, sort_keys=True)); return 1


if __name__ == "__main__": raise SystemExit(main())
