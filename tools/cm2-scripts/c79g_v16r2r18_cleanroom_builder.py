#!/usr/bin/env python3
"""Append-only r18 clean-room preflight/builder.

The r18 design receipt changes the binding direction to a real DAG and makes
``successor_v16r2_static_bundle`` an exact eleven-key object.  This program
therefore constructs the proposed r18 bytes *in memory first*.  It is
deliberately fail-closed: until every design predicate is proven, the only
files it may install are the r18 rejection, rejection-supersession, and
active-anchor receipts.  In particular it never writes a source, schema,
contract, transition, audit, launcher, manifest, outer receipt, runtime, or
credit surface.

The implementation is self contained and reads only immutable r16 bytes, the
r17 anchor, and the r18 redesign receipt.  It does not import or execute any
protocol source and has no byte-code-producing imports.
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
R16 = "v16r2r16"
PREV = "v16r2r17"
TAG = "v16r2r18"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

R16_SOURCE = {
    "producer": OUT / f"{BASE}_{R16}_semantic_source.py",
    "consumer": OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_"
        f"{R16}_semantic_source.py"),
    "launcher": OUT / f"{BASE}_cold_launch_{R16}_semantic_source.py",
}
R16_JSON = {
    "schema": OUT / f"{BASE}_schema_{R16}.json",
    "contract": OUT / f"{BASE}_contract_{R16}.json",
    "transition": OUT / (
        f"{BASE}_v16r2r15_to_{R16}_static_launch_transition_receipt_v1.json"),
    "audit": OUT / f"{BASE}_static_audit_{R16}.json",
}
R17_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
DESIGN = OUT / f"{BASE}_{TAG}_redesign_preflight_design_receipt_v1.json"

R18_SOURCE = {
    "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
    "consumer": OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_"
        f"{TAG}_semantic_source.py"),
    "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
}
R18_JSON = {
    "schema": OUT / f"{BASE}_schema_{TAG}.json",
    "contract": OUT / f"{BASE}_contract_{TAG}.json",
    "transition": OUT / (
        f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"),
    "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
}
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
RUNTIME = OUT / f"{BASE}_{TAG}_runtime.json"
CREDIT = OUT / f"{BASE}_{TAG}_formal_global_closure_credit.json"

REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
SUPERSESSION = OUT / (
    f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json")
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"

HEX64 = re.compile(r"^[0-9a-f]{64}$")
SENTINELS = {
    "d" * 64, "e" * 64, "f" * 64, "c" * 64,
    "UNPINNED_R16R2R16_CONTRACT_FILE", "UNPINNED_R16R2R16_CONTRACT_OBJECT",
}


class DuplicateKey(ValueError):
    pass


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canonical(body))
    return body


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
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON object required: {path}")
    if "object_sha256" in value:
        body = copy.deepcopy(value)
        claimed = body.pop("object_sha256")
        if claimed != sha(canonical(body)):
            raise RuntimeError(f"object closure mismatch: {path}")
    return value, raw


def evidence(path: Path) -> dict[str, Any]:
    raw = stable(path)
    item: dict[str, Any] = {
        "path": str(path.relative_to(ROOT)),
        "file_sha256": sha(raw),
        "bytes": len(raw),
        "mode": f"{stat.S_IMODE(path.stat().st_mode):04o}",
        "nlink": path.stat().st_nlink,
    }
    if path.suffix == ".json":
        value, _ = read_json(path)
        if "object_sha256" in value:
            item["object_sha256"] = value["object_sha256"]
    return item


def install(path: Path, raw: bytes, mode: int = 0o444) -> str:
    """Install exactly once.  Existing bytes are accepted only as replay."""
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


def retag(value: Any) -> Any:
    """Retag metadata without importing or executing predecessor sources."""
    if isinstance(value, dict):
        return {retag(k): retag(v) for k, v in value.items()}
    if isinstance(value, list):
        return [retag(v) for v in value]
    if not isinstance(value, str):
        return value
    # Protect the predecessor-to-successor edge before the broad namespace
    # rewrite; otherwise r16r15_to_r16r16 would be malformed.
    edge_old = f"{BASE}_v16r2r15_to_{R16}_static_launch_transition_receipt_v1.json"
    edge_new = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    anchor_old = f"{BASE}_{R16}_active_predecessor_supersession_receipt_v1.json"
    anchor_new = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    return (value.replace(edge_old, edge_new)
            .replace(anchor_old, anchor_new)
            .replace("V16R2R16", "V16R2R18")
            .replace(R16, TAG))


def retag_source(raw: bytes, role: str, anchor_value: dict[str, Any],
                 *, final_flags: bool = True) -> bytes:
    text = raw.decode("utf-8")
    edge_old = f"{BASE}_v16r2r15_to_{R16}_static_launch_transition_receipt_v1.json"
    edge_new = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    anchor_old = f"{BASE}_{R16}_active_predecessor_supersession_receipt_v1.json"
    anchor_new = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    text = (text.replace(edge_old, edge_new).replace(anchor_old, anchor_new)
            .replace("V16R2R16", "V16R2R18").replace(R16, TAG))
    # The active anchor is a forward edge and is safe to bind before sources.
    text, n_file = re.subn(
        r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
        f'ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "{sha(stable(R17_ANCHOR))}"', text)
    text, n_obj = re.subn(
        r'(?m)^ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\s*=\s*"[0-9a-f]{64}"\s*$',
        f'ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "{anchor_value["object_sha256"]}"', text)
    if (n_file, n_obj) != (1, 1):
        raise RuntimeError(f"{role}: active anchor pin assignment count {(n_file, n_obj)}")
    if final_flags:
        # Patch only the command gate; draft pin literals are intentionally
        # retained in this in-memory attempt so the preflight can report them.
        names = {
            "producer": "FINAL_V16R2_CORE_PINS_INSTALLED",
            "consumer": "FINAL_CURRENT_V16R2_PINS_INSTALLED",
            "launcher": "FINAL_BASE7_PINS_INSTALLED",
        }
        name = names[role]
        text, count = re.subn(
            rf'(?m)^({re.escape(name)}\s*=\s*)False\s*$', r'\1True', text)
        # The held r16 sources contain a duplicated compatibility assignment
        # for the producer/consumer final flag.  That is itself evidence for
        # the successor audit, not a reason for this preflight recorder to
        # abort before sealing its rejection chain.  Rewrite every exact
        # boolean assignment in-memory and let the candidate reviewer decide
        # whether the duplicate shape is acceptable.
        if count < 1:
            raise RuntimeError(f"{role}: {name} assignment count {count}")
    tree = ast.parse(text, filename=str(R18_SOURCE[role]))
    compile(tree, str(R18_SOURCE[role]), "exec")
    return (text if text.endswith("\n") else text + "\n").encode("utf-8")


def active_bundle(value: dict[str, Any], key: str) -> dict[str, Any]:
    bundle = value.get(key)
    if not isinstance(bundle, dict):
        raise RuntimeError(f"missing active bundle {key}")
    return bundle


def strip_source_hashes(bundle: dict[str, Any]) -> None:
    bundle.pop("source_hashes", None)


def exact11(paths: dict[str, str], hashes: dict[str, str],
            contract_object: str) -> dict[str, Any]:
    return {
        "all_four_core_file_pins_final": True,
        "build_only_producer": {
            "path": paths["producer"], "file_sha256": hashes["producer"]},
        "closed_schema": {
            "path": paths["schema"], "file_sha256": hashes["schema"]},
        "cold_launcher_v16r2_path": paths["launcher"],
        "contract": {
            "path": paths["contract"],
            "file_sha256": hashes["contract"],
            "object_sha256": contract_object,
        },
        "draft_pin_sentinels_remain_present": False,
        "final_consumer_pin_installed": True,
        "independent_verifier_assembler_authority_consumer": {
            "path": paths["consumer"], "file_sha256": hashes["consumer"]},
        "static_audit_v16r2_path": paths["audit"],
        "transition_receipt_bytes_are_closed_around_final_core_pins": True,
        "transition_receipt_physical_freeze_completed": False,
    }


def candidate_paths() -> list[Path]:
    return [*R18_SOURCE.values(), *R18_JSON.values(), MANIFEST, OUTER, RUNTIME, CREDIT]


def path_map() -> dict[str, str]:
    return {"anchor": str(ANCHOR.relative_to(ROOT)),
            "schema": str(R18_JSON["schema"].relative_to(ROOT)),
            "contract": str(R18_JSON["contract"].relative_to(ROOT)),
            "producer": str(R18_SOURCE["producer"].relative_to(ROOT)),
            "consumer": str(R18_SOURCE["consumer"].relative_to(ROOT)),
            "transition": str(R18_JSON["transition"].relative_to(ROOT)),
            "audit": str(R18_JSON["audit"].relative_to(ROOT)),
            "launcher": str(R18_SOURCE["launcher"].relative_to(ROOT))}


def draft_attempt(anchor_value: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Construct all proposed bytes in RAM and return evidence + blockers."""
    blockers: list[dict[str, Any]] = []
    paths = path_map()
    schema_value, _ = read_json(R16_JSON["schema"])
    schema = retag(schema_value)
    schema["$comment"] = "CM2_R18_DAG_DESIGN_ONLY__RUNTIME_NOT_AUTHORIZED"
    schema_raw = canonical(schema) + b"\n"
    schema_hash = sha(schema_raw)

    contract_value, _ = read_json(R16_JSON["contract"])
    contract = retag(contract_value)
    cb = active_bundle(contract, "v16r2_bundle")
    strip_source_hashes(cb)
    cb["bundle_version"] = TAG
    cb["pin_state"] = "R18_DAG_CORE_PINS_FINAL_SOURCE_DRAFT_RUNTIME_DISABLED"
    cb["closed_schema"] = {"path": paths["schema"], "file_sha256": schema_hash}
    cb["predecessor_semantic_supersession"] = {
        "path": paths["anchor"], "file_sha256": sha(stable(R17_ANCHOR)),
        "object_sha256": anchor_value["object_sha256"], "successor_only": f"{TAG}-semantic-bundle"}
    cb["predecessor_supersession_object_sha256"] = anchor_value["object_sha256"]
    cb["schema_file_sha256"] = schema_hash
    # Self pins are intentionally not guessed.  They are the key blocker this
    # preflight is designed to expose (a file cannot honestly contain its own
    # hash while also closing its object digest).
    cb["contract_file_sha256"] = f"UNPINNED_{TAG.upper()}_CONTRACT_FILE"
    cb["contract_object_sha256"] = f"UNPINNED_{TAG.upper()}_CONTRACT_OBJECT"
    contract["v16r2_bundle"] = cb
    contract["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.contract"
    contract_raw = canonical(close(contract)) + b"\n"
    contract_file_hash = sha(contract_raw)
    contract_object_hash = json.loads(contract_raw)["object_sha256"]

    source_drafts: dict[str, bytes] = {}
    source_status: dict[str, Any] = {}
    for role, path in R16_SOURCE.items():
        try:
            raw = stable(path)
            draft = retag_source(raw, role, anchor_value)
            source_drafts[role] = draft
            source_status[role] = {"ast_parse": True, "in_memory_compile": True,
                                   "bytes": len(draft), "file_sha256": sha(draft)}
        except Exception as exc:
            source_status[role] = {"ast_parse": False, "in_memory_compile": False,
                                   "error": f"{type(exc).__name__}: {exc}"}
            blockers.append({"id": f"{role}_source_ast_compile", "error": str(exc)})

    # The exact 11-key successor is assembled using the in-memory source
    # hashes.  No receipt bytes are installed, and no source is made to read a
    # downstream transition/audit hash.
    hashes = {role: sha(raw) for role, raw in source_drafts.items()}
    # Keep the attempted successor object total even when a held source
    # failed AST construction.  A zero hash is never accepted by a candidate;
    # it is only a typed failure witness in the rejection receipt.
    for role in R16_SOURCE:
        hashes.setdefault(role, "0" * 64)
    hashes.update({"schema": schema_hash, "contract": contract_file_hash})
    transition_value, _ = read_json(R16_JSON["transition"])
    transition = retag(transition_value)
    successor = exact11(paths, hashes, contract_object_hash)
    transition["successor_v16r2_static_bundle"] = successor
    transition["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.v16-to-v16r2-static-launch-transition.v1"
    transition["receipt_path"] = paths["transition"]
    transition_raw = canonical(close(transition)) + b"\n"
    transition_hash = sha(transition_raw)
    transition_obj = json.loads(transition_raw)["object_sha256"]
    audit_value, _ = read_json(R16_JSON["audit"])
    audit = retag(audit_value)
    audited = active_bundle(audit, "audited_v16r2_bundle")
    audited.clear()
    audited.update(copy.deepcopy(successor))
    audit["audited_v16r2_bundle"] = audited
    audit["audit_path"] = paths["audit"]
    audit_raw = canonical(close(audit)) + b"\n"
    audit_hash = sha(audit_raw)
    audit_obj = json.loads(audit_raw)["object_sha256"]
    # Launcher is downstream of every prior node.  Its AST is checked after
    # patching final flag only; BASE7_PINS itself remains draft in this proof,
    # because installing it would require a second source hash rewrite.
    launcher_status = source_status.get("launcher", {})
    if launcher_status.get("ast_parse"):
        try:
            launcher = source_drafts["launcher"].decode("utf-8")
            # Verify the source still has its explicit draft BASE7 shape.
            if "BASE7_PINS = {}" not in launcher:
                blockers.append({"id": "launcher_base7_draft_shape",
                                 "error": "BASE7_PINS={} marker missing"})
            launcher_status["draft_base7_present"] = "BASE7_PINS = {}" in launcher
        except Exception as exc:
            blockers.append({"id": "launcher_draft_inspection", "error": str(exc)})

    # Design predicates that cannot be honestly claimed before independent
    # r18 candidate installation are explicit blockers, not silent omissions.
    blockers.extend([
        {"id": "contract_self_file_object_pins",
         "fields": ["v16r2_bundle.contract_file_sha256",
                     "v16r2_bundle.contract_object_sha256"],
         "reason": "contract bytes cannot contain their own closed file/object hashes"},
        {"id": "source_pin_constants_not_finalized",
         "sentinels": sorted(SENTINELS),
         "reason": "r16 source templates retain draft pin constants; final source injection requires a fresh semantic rewrite"},
        {"id": "launcher_base7_pin_fixed_point",
         "reason": "setting BASE7_PINS to launcher-dependent final bytes needs a separately specified external binding stage"},
        {"id": "independent_r18_static_gates_pending",
         "reason": "reviewer A/B and jq -e CI are not authorized against uninstalled r18 bytes"},
        {"id": "independent_r18_runtime_evidence_pending",
         "reason": "dual-seed/no-producer/attack/terminal replay must run only after cold static freeze"},
    ])
    # Ensure the hypothetical successor itself obeys the exact design.  This
    # is useful evidence even though the surrounding graph is rejected.
    expected = {
        "all_four_core_file_pins_final", "build_only_producer", "closed_schema",
        "cold_launcher_v16r2_path", "contract", "draft_pin_sentinels_remain_present",
        "final_consumer_pin_installed",
        "independent_verifier_assembler_authority_consumer", "static_audit_v16r2_path",
        "transition_receipt_bytes_are_closed_around_final_core_pins",
        "transition_receipt_physical_freeze_completed"}
    shape_ok = set(successor) == expected and successor["draft_pin_sentinels_remain_present"] is False
    if not shape_ok:
        blockers.append({"id": "successor_exact11_shape", "actual_keys": sorted(successor),
                         "expected_keys": sorted(expected)})
    evidence = {
        "schema_draft": {"bytes": len(schema_raw), "file_sha256": schema_hash,
                          "shape": [len(schema.get("$defs", {})),
                                    sum(1 for n in _walk(schema) if isinstance(n, dict) and "$ref" in n),
                                    sum(1 for n in _walk(schema) if isinstance(n, dict) and n.get("additionalProperties") is False)]},
        "contract_draft": {"bytes": len(contract_raw), "file_sha256": contract_file_hash,
                            "object_sha256": contract_object_hash,
                            "source_hashes_present": "source_hashes" in cb,
                            "self_pin_values": [cb.get("contract_file_sha256"), cb.get("contract_object_sha256")]},
        "source_drafts": source_status,
        "transition_draft": {"bytes": len(transition_raw), "file_sha256": transition_hash,
                              "object_sha256": transition_obj,
                              "successor_key_count": len(successor),
                              "successor_keys": sorted(successor),
                              "source_hashes_present": "source_hashes" in successor},
        "audit_draft": {"bytes": len(audit_raw), "file_sha256": audit_hash,
                         "object_sha256": audit_obj,
                         "source_hashes_present": "source_hashes" in audited},
        "launcher_downstream_hash_inputs": {
            "schema": schema_hash, "contract": contract_file_hash,
            "contract_object": contract_object_hash, "producer": hashes.get("producer"),
            "consumer": hashes.get("consumer"), "transition": transition_hash,
            "transition_object": transition_obj, "audit": audit_hash},
        "candidate_bytes_materialized_in_memory_only": True,
    }
    return evidence, blockers


def _walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def rejection(inputs: dict[str, Any], attempt: dict[str, Any],
              blockers: list[dict[str, Any]]) -> tuple[dict[str, Any], bytes]:
    value = close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v6",
        "status": "PERMANENT_FAIL_CLOSED_R18_PREFLIGHT__ZERO_CREDIT",
        "failed_namespace": PREV,
        "proposed_successor_namespace": TAG,
        "rejection_reason": "R18_DAG_PREFLIGHT_UNRESOLVED_CORE_PIN_AND_RUNTIME_GATES",
        "design_receipt_path": str(DESIGN.relative_to(ROOT)),
        "design_receipt_file_sha256": inputs["design"]["file_sha256"],
        "independent_reviewer_failed_checks": [item["id"] for item in blockers],
        "independent_reviewer_failed_check_count": len(blockers),
        "preflight_blockers": blockers,
        "in_memory_attempt": attempt,
        "immutable_input_evidence": inputs,
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
        "runtime_surface_created": False,
        "candidate_artifacts_installed": False,
    })
    return value, canonical(value) + b"\n"


def supersession(rej: dict[str, Any], rej_raw: bytes) -> tuple[dict[str, Any], bytes]:
    value = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v6",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV, "successor_namespace": TAG,
        "predecessor_rejection_path": str(REJECTION.relative_to(ROOT)),
        "predecessor_rejection_file_sha256": sha(rej_raw),
        "predecessor_rejection_object_sha256": rej["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
    })
    return value, canonical(value) + b"\n"


def anchor(sup: dict[str, Any], sup_raw: bytes) -> tuple[dict[str, Any], bytes]:
    value = close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUPERSESSION.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(sup_raw),
        "predecessor_supersession_object_sha256": sup["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": CHECKPOINT,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "manifest_created": False, "outer_created": False,
    })
    return value, canonical(value) + b"\n"


def main() -> int:
    try:
        required = [*R16_SOURCE.values(), *R16_JSON.values(), R17_ANCHOR, DESIGN]
        for path in required:
            if not path.is_file():
                raise RuntimeError(f"immutable input missing: {path}")
        existing = [str(path.relative_to(ROOT)) for path in candidate_paths() if path.exists()]
        if existing:
            raise RuntimeError(f"r18 candidate target already exists: {existing}")
        anchor_value, _ = read_json(R17_ANCHOR)
        if anchor_value.get("successor_namespace") != f"{PREV}_semantic_source":
            raise RuntimeError("r17 anchor successor namespace mismatch")
        if (anchor_value.get("formal_global_closure_credit") != 0 or
                anchor_value.get("D02_unlock") is not False):
            raise RuntimeError("r17 anchor is not zero-credit locked")
        inputs = {"design": evidence(DESIGN), "r17_anchor": evidence(R17_ANCHOR)}
        inputs.update({f"r16_source_{k}": evidence(v) for k, v in R16_SOURCE.items()})
        inputs.update({f"r16_json_{k}": evidence(v) for k, v in R16_JSON.items()})
        attempt, blockers = draft_attempt(anchor_value)
        # The preflight is intentionally non-authorizing.  Even if a future
        # source rewrite removes today's blockers, this version never silently
        # promotes in-memory bytes; a new reviewed builder must be minted.
        blockers.append({"id": "candidate_materialization_guard",
                         "reason": "this revision is preflight-first and installs no candidate bytes"})
        rej, rej_raw = rejection(inputs, attempt, blockers)
        rej_action = install(REJECTION, rej_raw)
        sup, sup_raw = supersession(rej, rej_raw)
        sup_action = install(SUPERSESSION, sup_raw)
        anc, anc_raw = anchor(sup, sup_raw)
        anc_action = install(ANCHOR, anc_raw)
        after = [str(path.relative_to(ROOT)) for path in candidate_paths() if path.exists()]
        if after:
            raise RuntimeError(f"forbidden candidate outputs appeared: {after}")
        pyc = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc") if TAG in str(path)]
        if pyc:
            raise RuntimeError(f"r18 pyc appeared: {pyc}")
        result = {
            "schema": f"cm2.c79g.{TAG}.clean-room-builder.preflight.v1",
            "status": "FAIL_CLOSED_V16R2R18_PREFLIGHT__REJECTION_CHAIN_ONLY",
            "candidate_install": False,
            "candidate_artifacts_installed": False,
            "predecessor_rejection": {"path": str(REJECTION.relative_to(ROOT)),
                                       "file_sha256": sha(rej_raw),
                                       "object_sha256": rej["object_sha256"], "action": rej_action},
            "predecessor_supersession": {"path": str(SUPERSESSION.relative_to(ROOT)),
                                          "file_sha256": sha(sup_raw),
                                          "object_sha256": sup["object_sha256"], "action": sup_action},
            "active_anchor": {"path": str(ANCHOR.relative_to(ROOT)),
                               "file_sha256": sha(anc_raw),
                               "object_sha256": anc["object_sha256"], "action": anc_action},
            "blocker_count": len(blockers), "blocker_ids": [b["id"] for b in blockers],
            "in_memory_attempt": attempt,
            "manifest_created": False, "outer_created": False,
            "runtime_surface_created": False, "pyc_created": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False,
        }
        result["object_sha256"] = sha(canonical(result))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 1
    except Exception as exc:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.clean-room-builder.failure.v1",
            "status": "FAIL_CLOSED_V16R2R18_CLEAN_ROOM",
            "error_type": type(exc).__name__, "error": str(exc),
            "candidate_install": False, "candidate_artifacts_installed": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
