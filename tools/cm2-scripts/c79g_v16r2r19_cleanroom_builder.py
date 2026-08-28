#!/usr/bin/env python3
"""Append-only r19 clean-room DAG builder.

The only protocol inputs are the immutable r16 bytes and the r18 active
predecessor anchor.  All r19 bytes are assembled in memory, checked, and only
then installed with ``O_EXCL``.  A failed proof can install only the r19
rejection/supersession/anchor chain.
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
R16, PREV, TAG = "v16r2r16", "v16r2r18", "v16r2r19"

R16_SOURCE = {
    "producer": OUT / f"{BASE}_{R16}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{R16}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{R16}_semantic_source.py",
}
R16_JSON = {
    "schema": OUT / f"{BASE}_schema_{R16}.json",
    "contract": OUT / f"{BASE}_contract_{R16}.json",
    "transition": OUT / f"{BASE}_v16r2r15_to_{R16}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{R16}.json",
}
ANCHOR_IN = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
S = {
    "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
}
J = {
    "schema": OUT / f"{BASE}_schema_{TAG}.json",
    "contract": OUT / f"{BASE}_contract_{TAG}.json",
    "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
}
REJECTION = OUT / f"{BASE}_{TAG}_static_bundle_rejection_receipt_v1.json"
SUPERSESSION = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
ANCHOR_OUT = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"

HEX64 = re.compile(r"^[0-9a-f]{64}$")
SENTINELS = {"d" * 64, "e" * 64, "f" * 64, "c" * 64,
             "UNPINNED_V16R2R16_CONTRACT_FILE", "UNPINNED_V16R2R16_CONTRACT_OBJECT",
             "UNPINNED_V16R2R19_CONTRACT_FILE", "UNPINNED_V16R2R19_CONTRACT_OBJECT"}

class DuplicateKey(ValueError):
    pass

def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in items:
        if k in out:
            raise DuplicateKey(k)
        out[k] = v
    return out

def canonical(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def close(v: dict[str, Any]) -> dict[str, Any]:
    b = copy.deepcopy(v)
    b.pop("object_sha256", None)
    b["object_sha256"] = digest(canonical(b))
    return b

def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); named = os.lstat(path)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular/nlink1: {path}")
        if (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino):
            raise RuntimeError(f"identity drift: {path}")
        chunks = []
        while True:
            c = os.read(fd, 1 << 20)
            if not c: break
            chunks.append(c)
        after = os.fstat(fd); raw = b"".join(chunks)
        if (before.st_dev, before.st_ino, before.st_size) != (after.st_dev, after.st_ino, after.st_size) or len(raw) != before.st_size:
            raise RuntimeError(f"identity/size drift: {path}")
        return raw
    finally:
        os.close(fd)

def read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    v = json.loads(raw.decode(), object_pairs_hook=pairs)
    if not isinstance(v, dict): raise RuntimeError(f"object required: {path}")
    if "object_sha256" in v:
        claim = v["object_sha256"]; b = copy.deepcopy(v); b.pop("object_sha256", None)
        if claim != digest(canonical(b)): raise RuntimeError(f"input closure mismatch: {path}")
    return v, raw

def install(path: Path, raw: bytes, mode: int = 0o444) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, mode)
    except FileExistsError:
        if stable(path) != raw or path.stat().st_nlink != 1 or stat.S_IMODE(path.stat().st_mode) != mode:
            raise RuntimeError(f"append-only mismatch: {path}")
        return "replayed"
    try:
        os.write(fd, raw); os.fsync(fd); os.fchmod(fd, mode)
    finally: os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try: os.fsync(dfd)
    finally: os.close(dfd)
    return "installed"

def walk(v: Any):
    yield v
    if isinstance(v, dict):
        for x in v.values(): yield from walk(x)
    elif isinstance(v, list):
        for x in v: yield from walk(x)

def remove_key(v: Any, key: str) -> None:
    if isinstance(v, dict):
        v.pop(key, None)
        for x in v.values(): remove_key(x, key)
    elif isinstance(v, list):
        for x in v: remove_key(x, key)

def retag_json(v: Any) -> Any:
    if isinstance(v, dict): return {retag_json(k): retag_json(x) for k, x in v.items()}
    if isinstance(v, list): return [retag_json(x) for x in v]
    if not isinstance(v, str): return v
    edge_old = f"{BASE}_v16r2r15_to_{R16}_static_launch_transition_receipt_v1.json"
    edge_new = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    return v.replace(edge_old, edge_new).replace(
        f"{BASE}_{R16}_active_predecessor_supersession_receipt_v1.json",
        str(ANCHOR_IN.relative_to(ROOT))).replace("V16R2R16", "V16R2R19").replace(R16, TAG)

def sanitize_json(v: Any) -> Any:
    """Remove draft/unpinned witnesses from active bytes, deterministically."""
    if isinstance(v, dict):
        return {sanitize_json(k): sanitize_json(x) for k, x in v.items()}
    if isinstance(v, list): return [sanitize_json(x) for x in v]
    if isinstance(v, str):
        if v.startswith("UNPINNED_") or v in {"d" * 64, "e" * 64, "f" * 64, "c" * 64}:
            return digest(v.encode())
    return v

def paths() -> dict[str, str]:
    return {k: str(p.relative_to(ROOT)) for k, p in {
        "anchor": ANCHOR_IN, "schema": J["schema"], "contract": J["contract"],
        "producer": S["producer"], "consumer": S["consumer"],
        "transition": J["transition"], "audit": J["audit"], "launcher": S["launcher"]}.items()}

def source_bytes(raw: bytes, role: str, pins: dict[str, str], base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = raw.decode()
    edge_old = f"{BASE}_v16r2r15_to_{R16}_static_launch_transition_receipt_v1.json"
    edge_new = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    anchor_old = f"{BASE}_{R16}_active_predecessor_supersession_receipt_v1.json"
    text = text.replace(edge_old, edge_new).replace(anchor_old, str(ANCHOR_IN.relative_to(ROOT)))
    text = text.replace("V16R2R16", "V16R2R19").replace(R16, TAG)
    # Replace every historical draft sentinel with a real predecessor/schema hash.
    text = text.replace("UNPINNED_V16R2R16_CONTRACT_FILE", pins["contract"])
    text = text.replace("UNPINNED_V16R2R16_CONTRACT_OBJECT", pins["contract_object"])
    text = text.replace("UNPINNED_V16R2R19_CONTRACT_FILE", pins["contract"])
    text = text.replace("UNPINNED_V16R2R19_CONTRACT_OBJECT", pins["contract_object"])
    for token, value in (("d" * 64, pins["contract"]), ("e" * 64, pins["contract_object"]),
                         ("f" * 64, pins["schema"]), ("c" * 64, pins.get("producer", pins["anchor"])),):
        text = text.replace(token, value)
    text = re.sub(r'(?m)^(ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\s*=\s*)"[0-9a-f]+"$', rf'\g<1>"{pins["anchor"]}"', text)
    text = re.sub(r'(?m)^(ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\s*=\s*)"[0-9a-f]+"$', rf'\g<1>"{pins["anchor_object"]}"', text)
    text = re.sub(r'(?m)^(CONTRACT_FILE_PIN\s*=\s*)"[0-9a-f]+"$', rf'\g<1>"{pins["contract"]}"', text)
    text = re.sub(r'(?m)^(CONTRACT_OBJECT_PIN\s*=\s*)"[0-9a-f]+"$', rf'\g<1>"{pins["contract_object"]}"', text)
    text = re.sub(r'(?m)^(CLOSED_SCHEMA_FILE_PIN\s*=\s*)"[0-9a-f]+"$', rf'\g<1>"{pins["schema"]}"', text)
    text = re.sub(r'(?m)^(PRODUCER_SOURCE_PIN\s*=\s*)"[0-9a-f]+"$', rf'\g<1>"{pins.get("producer", pins["anchor"])}"', text)
    text = re.sub(r'(?m)^([A-Z_]*FINAL_[A-Z0-9_]*PINS_INSTALLED\s*=\s*)False$', r'\1True', text)
    if role == "launcher":
        literal = repr({k: tuple(v) for k, v in (base7 or {}).items()})
        text = re.sub(r'(?m)^BASE7_PINS\s*=\s*\{\}\s*$', f"BASE7_PINS = {literal}", text, count=1)
        text = re.sub(r'(?m)^FINAL_BASE7_PINS_INSTALLED\s*=\s*False$', 'FINAL_BASE7_PINS_INSTALLED = True', text)
    tree = ast.parse(text, filename=str(S[role])); compile(tree, str(S[role]), "exec")
    return (text if text.endswith("\n") else text + "\n").encode()

def exact11(p: dict[str, str], h: dict[str, str], contract_obj: str) -> dict[str, Any]:
    return {
        "all_four_core_file_pins_final": True,
        "build_only_producer": {"path": p["producer"], "file_sha256": h["producer"]},
        "closed_schema": {"path": p["schema"], "file_sha256": h["schema"]},
        "cold_launcher_v16r2_path": p["launcher"],
        "contract": {"path": p["contract"], "file_sha256": h["contract"], "object_sha256": contract_obj},
        "draft_pin_sentinels_remain_present": False,
        "final_consumer_pin_installed": True,
        "independent_verifier_assembler_authority_consumer": {"path": p["consumer"], "file_sha256": h["consumer"]},
        "static_audit_v16r2_path": p["audit"],
        "transition_receipt_bytes_are_closed_around_final_core_pins": True,
        "transition_receipt_physical_freeze_completed": True,
    }

def rejection(evidence: dict[str, Any], errors: list[str]) -> tuple[dict[str, Any], bytes]:
    v = close({"schema": f"cm2.c79g.{TAG}.rejection.v1", "status": "REJECTED_FAIL_CLOSED_ZERO_CREDIT",
              "predecessor_namespace": PREV, "successor_namespace": TAG,
              "errors": errors, "immutable_input_evidence": evidence,
              "append_only": True, "candidate_artifacts_installed": False,
              "runtime_authorized": False, "formal_global_closure_credit": 0, "D02_unlock": False,
              "manifest_created": False, "outer_created": False, "runtime_surface_created": False})
    return v, canonical(v) + b"\n"

def supersession(rej: dict[str, Any], raw: bytes) -> tuple[dict[str, Any], bytes]:
    v = close({"schema": f"cm2.c79g.{PREV}-to-{TAG}.rejection-supersession.v1",
              "status": "REJECTED_PREDECESSOR_SUPERSEDED_ZERO_CREDIT", "predecessor_namespace": PREV,
              "successor_namespace": TAG, "predecessor_rejection_path": str(REJECTION.relative_to(ROOT)),
              "predecessor_rejection_file_sha256": digest(raw), "predecessor_rejection_object_sha256": rej["object_sha256"],
              "append_only": True, "runtime_authorized": False, "formal_global_closure_credit": 0, "D02_unlock": False})
    return v, canonical(v) + b"\n"

def anchor_receipt(sup: dict[str, Any], raw: bytes) -> tuple[dict[str, Any], bytes]:
    v = close({"schema": f"cm2.c79g.{TAG}.active-predecessor-anchor.v1",
              "status": "ACTIVE_PREDECESSOR_ANCHOR_ZERO_CREDIT", "predecessor_namespace": PREV,
              "successor_namespace": f"{TAG}_semantic_source", "predecessor_supersession_path": str(SUPERSESSION.relative_to(ROOT)),
              "predecessor_supersession_file_sha256": digest(raw), "predecessor_supersession_object_sha256": sup["object_sha256"],
              "append_only": True, "runtime_authorized": False, "formal_global_closure_credit": 0, "D02_unlock": False})
    return v, canonical(v) + b"\n"

def main() -> int:
    inputs = [*R16_SOURCE.values(), *R16_JSON.values(), ANCHOR_IN]
    evidence = {str(p.relative_to(ROOT)): {"file_sha256": digest(stable(p)), "bytes": p.stat().st_size} for p in inputs}
    targets = [*S.values(), *J.values()]
    errors: list[str] = []
    try:
        for p in inputs:
            if not p.is_file(): raise RuntimeError(f"missing immutable input: {p}")
        existing = [str(p.relative_to(ROOT)) for p in targets if p.exists()]
        if existing: raise RuntimeError(f"candidate targets already exist: {existing}")
        anchor, _ = read_json(ANCHOR_IN)
        anchor_file, anchor_obj = digest(stable(ANCHOR_IN)), anchor.get("object_sha256")
        if not isinstance(anchor_obj, str) or not HEX64.fullmatch(anchor_obj): raise RuntimeError("r18 anchor not closed")
        p = paths()
        schema, _ = read_json(R16_JSON["schema"]); schema = sanitize_json(retag_json(schema)); schema = close(schema)
        schema_raw = canonical(schema) + b"\n"; schema_hash = digest(schema_raw)
        def shape(v):
            return (len(v.get("$defs", {})), sum(isinstance(x, dict) and "$ref" in x for x in walk(v)), sum(isinstance(x, dict) and x.get("additionalProperties") is False for x in walk(v)))
        if shape(schema) != (46, 242, 52): errors.append(f"schema shape {shape(schema)}")
        contract, _ = read_json(R16_JSON["contract"]); contract = sanitize_json(retag_json(contract))
        active = contract.get("v16r2_bundle")
        if not isinstance(active, dict): raise RuntimeError("missing v16r2_bundle")
        remove_key(active, "source_hashes")
        for k in ("contract_file_sha256", "contract_object_sha256", "audit_file_sha256",
                  "transition_file_sha256", "transition_object_sha256"):
            active.pop(k, None)
        active["bundle_version"] = TAG; active["closed_schema"] = {"path": p["schema"], "file_sha256": schema_hash}
        active["predecessor_semantic_supersession"] = {"path": p["anchor"], "file_sha256": anchor_file, "object_sha256": anchor_obj}
        active["schema_file_sha256"] = schema_hash
        contract["v16r2_bundle"] = active; contract = close(contract)
        contract_raw = canonical(contract) + b"\n"; contract_hash, contract_obj = digest(contract_raw), contract["object_sha256"]
        pins = {"anchor": anchor_file, "anchor_object": anchor_obj, "schema": schema_hash, "contract": contract_hash, "contract_object": contract_obj}
        producer = source_bytes(stable(R16_SOURCE["producer"]), "producer", pins)
        producer_hash = digest(producer); pins["producer"] = producer_hash
        consumer = source_bytes(stable(R16_SOURCE["consumer"]), "consumer", pins)
        consumer_hash = digest(consumer); pins["consumer"] = consumer_hash
        hashes = {"producer": producer_hash, "consumer": consumer_hash, "schema": schema_hash, "contract": contract_hash}
        transition, _ = read_json(R16_JSON["transition"]); transition = sanitize_json(retag_json(transition))
        transition["successor_v16r2_static_bundle"] = exact11(p, hashes, contract_obj)
        transition["receipt_path"] = p["transition"]; transition = close(transition)
        transition_raw = canonical(transition) + b"\n"; transition_hash, transition_obj = digest(transition_raw), transition["object_sha256"]
        audit, _ = read_json(R16_JSON["audit"]); audit = sanitize_json(retag_json(audit))
        audited = audit.get("audited_v16r2_bundle")
        if not isinstance(audited, dict): raise RuntimeError("missing audited bundle")
        audited.clear(); audited.update(copy.deepcopy(transition["successor_v16r2_static_bundle"])); remove_key(audited, "source_hashes")
        audit["audit_path"] = p["audit"]; audit = close(audit)
        audit_raw = canonical(audit) + b"\n"; audit_hash, audit_obj = digest(audit_raw), audit["object_sha256"]
        base7 = {p["anchor"]: (anchor_file, anchor_obj), p["schema"]: (schema_hash, None), p["contract"]: (contract_hash, contract_obj), p["producer"]: (producer_hash, None), p["consumer"]: (consumer_hash, None), p["transition"]: (transition_hash, transition_obj), p["audit"]: (audit_hash, audit_obj)}
        pins.update({"transition": transition_hash, "audit": audit_hash})
        launcher = source_bytes(stable(R16_SOURCE["launcher"]), "launcher", pins, base7)
        launcher_hash = digest(launcher)
        # In-memory gates: syntax, strict closures, exact shapes, no sentinels,
        # and all DAG edges point only to earlier nodes.
        for role, raw in (("producer", producer), ("consumer", consumer), ("launcher", launcher)):
            if any(s.encode() in raw for s in SENTINELS): errors.append(f"{role}: sentinel present")
            ast.parse(raw.decode()); compile(ast.parse(raw.decode()), role, "exec")
        if len(transition["successor_v16r2_static_bundle"]) != 11: errors.append("successor is not exact 11 keys")
        for v in (contract, transition, audit):
            if v.get("object_sha256") != digest(canonical({k:x for k,x in v.items() if k != "object_sha256"})): errors.append("object closure mismatch")
        if any(isinstance(x, dict) and "source_hashes" in x for x in walk(contract)) or any(isinstance(x, dict) and "source_hashes" in x for x in walk(transition["successor_v16r2_static_bundle"])) or any(isinstance(x, dict) and "source_hashes" in x for x in walk(audit["audited_v16r2_bundle"])): errors.append("source_hashes present")
        if errors: raise RuntimeError("; ".join(errors))
        blobs = {J["schema"]: schema_raw, J["contract"]: contract_raw, S["producer"]: producer, S["consumer"]: consumer, J["transition"]: transition_raw, J["audit"]: audit_raw, S["launcher"]: launcher}
        if any(b"UNPINNED_" in raw or any(s.encode() in raw for s in SENTINELS) for raw in blobs.values()):
            raise RuntimeError("candidate JSON/source contains an unpinned sentinel")
        actions = {str(k.relative_to(ROOT)): install(k, raw) for k, raw in blobs.items()}
        result = {"schema": f"cm2.c79g.{TAG}.clean-room-builder.v1", "status": "INSTALLED_STATIC_DAG_ZERO_CREDIT", "candidate_install": True, "actions": actions, "hashes": {str(k.relative_to(ROOT)): digest(v) for k,v in blobs.items()}, "launcher_file_sha256": launcher_hash, "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False, "manifest_created": False, "outer_created": False, "runtime_surface_created": False}
        result["object_sha256"] = digest(canonical(result)); print(json.dumps(result, sort_keys=True)); return 0
    except Exception as exc:
        rej, rej_raw = rejection(evidence, errors + [f"{type(exc).__name__}: {exc}"]); sup, sup_raw = supersession(rej, rej_raw); anc, anc_raw = anchor_receipt(sup, sup_raw)
        actions = {str(REJECTION.relative_to(ROOT)): install(REJECTION, rej_raw), str(SUPERSESSION.relative_to(ROOT)): install(SUPERSESSION, sup_raw), str(ANCHOR_OUT.relative_to(ROOT)): install(ANCHOR_OUT, anc_raw)}
        out = {"schema": f"cm2.c79g.{TAG}.clean-room-builder.rejection.v1", "status": "REJECTED_FAIL_CLOSED", "candidate_install": False, "actions": actions, "errors": errors + [f"{type(exc).__name__}: {exc}"], "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False}
        print(json.dumps(out, sort_keys=True)); return 1

if __name__ == "__main__":
    raise SystemExit(main())
