#!/usr/bin/env python3
"""Append-only r44 clean-room builder (static self-check by default).

The r43 candidate is rejected because its predecessor rejection witness kept
only truncated (four-character) guard/report digests.  This entry point does
not repair or re-use any r43 candidate bytes.  It loads the reviewed r40
constructor in memory, retags the immutable r39 source/JSON inputs to a fresh
r43 -> r44 edge, and carries the full immutable guard digests into the new
rejection witness.  The r43 active anchor and r43 supersession are the only
predecessor-chain inputs.

Running this file performs no installation.  ``--static-self-check`` (the
default) only reads immutable inputs and exercises AST/in-memory retag checks.
The explicit ``--install`` path is retained for the owner, and is the only
path that can create the r43 rejection, r43->r44 chain, or r44 candidate
members.  It never creates a manifest, outer receipt, runtime surface,
authority, or credit.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"

# Candidate inputs are deliberately pinned to the immutable r39 exact9.  The
# predecessor chain for this attempt is r43, not the mutable r43 candidate
# surface rejected by the caller.
TEMPLATE = "v16r2r39"
TEMPLATE_PREV = "v16r2r38"
PREV = "v16r2r43"
TAG = "v16r2r44"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

R43_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R43_SUP = OUT / f"{BASE}_v16r2r42_to_v16r2r43_static_bundle_rejection_supersession_receipt_v1.json"
R43_TRANSITION = OUT / f"{BASE}_v16r2r42_to_v16r2r43_static_launch_transition_receipt_v1.json"
R43_SCHEMA = OUT / f"{BASE}_schema_v16r2r43.json"
R43_COLD_MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v16r2r43.sha256"
R43_COLD_OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v16r2r43.json"
R43_SIDE_RECEIPTS = (
    OUT / f"{BASE}_v16r2r43_no_producer_dual_seed_evidence_receipt_v1.json",
    OUT / f"{BASE}_v16r2r43_mutation_attack_evidence_receipt_v1.json",
    OUT / f"{BASE}_v16r2r43_dual_checker_terminal_replay_receipt_v1.json",
)

R43_ANCHOR_SHA256 = "91494dd8813aabd3464e9ab320ed364d183a5cb5d39da4b797c914283ccee637"
R43_ANCHOR_OBJECT_SHA256 = "aad9ca9041a8a8cba3c36767c7657058d531fb93da0f1fb405f91b9a1b0545d2"
R43_SUP_SHA256 = "480abeed4907b463f5bb00291bc9efa8a4f92d3deb7c495371a36760e4efd57f"
R43_SUP_OBJECT_SHA256 = "ccf8bc2c322057c253a2e72ae51630178db15719478548d40bf69957b66f3050"
R43_TRANSITION_SHA256 = "4aeb9d54205b1b485fafde968c456462587ea209938b5f7740d49994e2091d71"
R43_SCHEMA_SHA256 = "2a4141edab5acad8bcd3a63d87c59e0f7e09382492553b5826bacf72da303d44"
R43_SCHEMA_OBJECT_SHA256 = "f902b444464c26935f5a6822eef6da1add2e5f5a91e94fdf3a73daed4597eb12"
R43_SCHEMA_DESCRIPTION = (
    "Append-only v16r2r43 schema.  The active exact8 starts with the configured "
    "recent predecessor supersession receipt; all persisted credit and "
    "runtime authority remain disabled."
)
R42_REJECTION = OUT / f"{BASE}_v16r2r42_static_bundle_rejection_receipt_v1.json"
R42_REJECTION_SHA256 = "6e9b666a365b9df87ec3c1cd61c4a54bc67da2e01a8e2942fd2a1f1df3d288ae"
R42_FAILURE_OBJECT_SHA256 = "19ed0012556cd3db6f04183ebdd0bd542aef1fe62d6a4ab13cda0dc909e38452"
R42_FAILURE_REPORT_SHA256 = "1d0ab79ad8edbd549f020baafa8671f6d4cca573ff2b944736a84b7a8937bd50"

SCHEMA_DESCRIPTION = (
    "Append-only v16r2r44 schema.  The active exact8 starts with the "
    "configured recent predecessor supersession receipt; all persisted "
    "credit and runtime authority remain disabled."
)

# r43's closed-schema metadata retained an obsolete active-proof field name
# from the r9 template.  The executable launcher/source already emits and
# validates the fresh active-predecessor name.  Rename only the two active
# proof definitions; incident/history payloads elsewhere in the schema are
# immutable historical witnesses and must not be rewritten.
STALE_ACTIVE_PROOF_KEY = (
    "current_exact8_first_member_is_r9_semantic_supersession_receipt"
)
FRESH_ACTIVE_PROOF_KEY = (
    "current_exact8_first_member_is_active_predecessor_supersession_receipt"
)
ACTIVE_PROOF_DEFS = ("coldLaunchProof", "staticFreezeProof")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    """Read one regular immutable file while checking held identity."""
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable predecessor input:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise RuntimeError(f"predecessor identity drift:{path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short predecessor read:{path}")
        return raw
    finally:
        os.close(fd)


def load_r40_constructor() -> dict[str, Any]:
    """Compile the reviewed r40 constructor in memory, retagged to r44."""
    path = ROOT / "scripts/c79g_v16r2r40_candidate_builder.py"
    raw = stable(path).decode("utf-8")
    old_prev = 'PREV = "v16r2r39"'
    old_tag = 'TAG = "v16r2r40"'
    if raw.count(old_prev) != 1 or raw.count(old_tag) != 1:
        raise RuntimeError("r40 constructor assignment census")
    raw = raw.replace(old_prev, f'PREV = "{PREV}"', 1)
    raw = raw.replace(old_tag, f'TAG = "{TAG}"', 1)
    tree = ast.parse(raw, filename=str(path))
    compile(tree, str(path), "exec")
    ns: dict[str, Any] = {"__name__": "_c79g_r44_constructor",
                           "__file__": str(path), "__package__": None}
    exec(compile(tree, str(path), "exec"), ns, ns)
    return ns


def _assert_frozen(path: Path, expected_file: str,
                   expected_object: str | None = None) -> dict[str, Any]:
    if not path.is_file() or path.stat().st_nlink != 1 or \
       stat.S_IMODE(path.stat().st_mode) != 0o444:
        raise RuntimeError(f"predecessor chain member mutable/missing:{path}")
    raw = stable(path)
    actual = sha(raw)
    if actual != expected_file:
        raise RuntimeError(f"predecessor file hash drift:{path}:{actual}")
    value = json.loads(raw.decode("utf-8"))
    if expected_object is not None and value.get("object_sha256") != expected_object:
        raise RuntimeError(f"predecessor object hash drift:{path}")
    if value.get("formal_global_closure_credit") != 0 or \
       value.get("D02_unlock") is not False or \
       value.get("runtime_authorized") is not False:
        raise RuntimeError(f"predecessor credit/authority drift:{path}")
    return value


def _schema_residue_fix(value: Any, ns: dict[str, Any]) -> Any:
    """Apply r44 metadata only to the active closed-schema root."""
    value = ns["retag_value"](value)
    if not isinstance(value, dict):
        return value
    # The r39 schema called this active predicate an ``r9`` member, while the
    # executable launcher/consumer emit and require the role-aware name.  The
    # rename is limited to the two active schema definitions; historical
    # incident payloads elsewhere in the document remain byte-for-byte data.
    defs = value.get("$defs")
    if isinstance(defs, dict):
        old_key = "current_exact8_first_member_is_r9_semantic_supersession_receipt"
        new_key = "current_exact8_first_member_is_active_predecessor_supersession_receipt"
        for node_name in ("coldLaunchProof", "staticFreezeProof"):
            node = defs.get(node_name)
            if not isinstance(node, dict):
                raise RuntimeError(f"schema active definition missing:{node_name}")
            props = node.get("properties")
            required = node.get("required")
            if not isinstance(props, dict) or not isinstance(required, list):
                raise RuntimeError(f"schema active key shape:{node_name}")
            if old_key in props:
                if new_key in props:
                    raise RuntimeError(f"schema active key collision:{node_name}")
                props[new_key] = props.pop(old_key)
            if old_key in required:
                required[required.index(old_key)] = new_key
            if new_key not in props or new_key not in required or old_key in props or old_key in required:
                raise RuntimeError(f"schema active key not normalized:{node_name}")
    # Contract purpose and audit template-review state are active metadata,
    # not historical incident witnesses.  Normalize them in the same in-
    # memory pass so the downstream hashes are computed over the corrected
    # bytes and no hash cycle is introduced.
    if "v16r2_bundle" in value and "purpose" in value:
        value["purpose"] = (
            f"Append-only {TAG} semantic bundle with the active predecessor "
            "chain and canonical C53 runtime root; no credit transfer."
        )
    closure = value.get("schema_and_constructor_closure")
    if isinstance(closure, dict) and "source_template_shape_review_pending" in closure:
        closure["source_template_shape_review_pending"] = False
    if "$defs" not in value or "$schema" not in value:
        return value
    value["$id"] = f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.schema"
    value["$comment"] = f"CM2_{TAG.upper()}_DAG_STATIC_ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
    value["description"] = SCHEMA_DESCRIPTION
    value["title"] = f"C79g {TAG} full-shape zero-credit schema"
    defs = value.get("$defs")
    if not isinstance(defs, dict):
        raise RuntimeError("closed schema definitions missing")
    for def_name in ACTIVE_PROOF_DEFS:
        node = defs.get(def_name)
        if not isinstance(node, dict) or not isinstance(node.get("properties"), dict):
            raise RuntimeError(f"active proof definition missing:{def_name}")
        props = node["properties"]
        if STALE_ACTIVE_PROOF_KEY in props:
            if FRESH_ACTIVE_PROOF_KEY in props:
                raise RuntimeError(f"active proof key collision:{def_name}")
            props[FRESH_ACTIVE_PROOF_KEY] = props.pop(STALE_ACTIVE_PROOF_KEY)
        required = node.get("required")
        if not isinstance(required, list):
            raise RuntimeError(f"active proof required list missing:{def_name}")
        replaced = [FRESH_ACTIVE_PROOF_KEY if item == STALE_ACTIVE_PROOF_KEY
                    else item for item in required]
        if replaced.count(FRESH_ACTIVE_PROOF_KEY) != 1:
            raise RuntimeError(f"active proof required key mismatch:{def_name}")
        node["required"] = replaced
    if "r9 schema" in str(value.get("description", "")).lower():
        raise RuntimeError("schema description residue survived r44 retag")
    return value


def _assert_r43_schema_residue() -> dict[str, Any]:
    """Pin the rejected r43 schema and its immutable predecessor metadata."""
    raw = stable(R43_SCHEMA)
    if sha(raw) != R43_SCHEMA_SHA256:
        raise RuntimeError("r43 schema file hash drift")
    value = json.loads(raw.decode("utf-8"))
    body = dict(value)
    body.pop("object_sha256", None)
    canonical = json.dumps(body, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":"), allow_nan=False).encode()
    if sha(canonical) != R43_SCHEMA_OBJECT_SHA256:
        raise RuntimeError("r43 schema object hash drift")
    if value.get("description") != R43_SCHEMA_DESCRIPTION or \
       "r9 schema" in str(value.get("description", "")).lower():
        raise RuntimeError("r43 schema metadata drift")
    if value.get("$id") != f"cm2.round306c79g.true-global-no-producer-consumer.{PREV}.schema":
        raise RuntimeError("r43 schema id drift")
    return {"path": str(R43_SCHEMA.relative_to(ROOT)),
            "file_sha256": R43_SCHEMA_SHA256,
            "object_sha256": R43_SCHEMA_OBJECT_SHA256,
            "description": value["description"],
            "rejection_reason": "R43_R42_REJECTION_WITNESS_PREFIX_ONLY_FAIL_CLOSED"}


def _assert_r42_rejection_witness() -> dict[str, Any]:
    """Prove the exact r42 rejection bytes and upgrade its truncated witnesses."""
    raw = stable(R42_REJECTION)
    if sha(raw) != R42_REJECTION_SHA256:
        raise RuntimeError("r42 rejection file hash drift")
    value = json.loads(raw.decode("utf-8"))
    if value.get("rejection_reason") != "R42_COLD_FREEZE_GUARD_PYC_FAIL_CLOSED":
        raise RuntimeError("r42 rejection reason drift")
    detail = value.get("detail")
    if not isinstance(detail, dict) or \
       detail.get("guard_failure_object_sha256_prefix") != "19ed" or \
       detail.get("guard_failure_report_sha256_prefix") != "1d0":
        raise RuntimeError("r42 truncated witness shape drift")
    claimed_object = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    if not isinstance(claimed_object, str) or sha(
            json.dumps(body, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False).encode()
    ) != claimed_object:
        raise RuntimeError("r42 rejection object closure drift")
    if not R42_FAILURE_OBJECT_SHA256.startswith(detail["guard_failure_object_sha256_prefix"]) or \
       not R42_FAILURE_REPORT_SHA256.startswith(detail["guard_failure_report_sha256_prefix"]):
        raise RuntimeError("r42 full witness does not match truncated prefix")
    return {
        "path": str(R42_REJECTION.relative_to(ROOT)),
        "file_sha256": R42_REJECTION_SHA256,
        "object_sha256": claimed_object,
        "rejection_reason": value["rejection_reason"],
        "guard_failure_object_sha256": R42_FAILURE_OBJECT_SHA256,
        "guard_failure_report_sha256": R42_FAILURE_REPORT_SHA256,
        "source_fields_were_prefix_only": True,
    }


def _configure_r44(ns: dict[str, Any], b: Any) -> None:
    """Bind the generic constructor to immutable r39 inputs and r43 anchor."""
    # The caller invokes the reviewed configure on the actual generic module
    # first.  This helper only replaces every path/chain value that matters;
    # calling ``ns["configure"]`` here would recurse once the install hook
    # wraps that function.
    b.BASE = BASE
    b.R16 = TEMPLATE
    b.PREV = PREV
    b.TAG = TAG
    b.UPSTREAM = UPSTREAM
    b.CHECKPOINT = UPSTREAM
    b.SRC_IN = {
        "producer": OUT / f"{BASE}_{TEMPLATE}_semantic_source.py",
        "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TEMPLATE}_semantic_source.py",
        "launcher": OUT / f"{BASE}_cold_launch_{TEMPLATE}_semantic_source.py",
    }
    b.JSON_IN = {
        "schema": OUT / f"{BASE}_schema_{TEMPLATE}.json",
        "contract": OUT / f"{BASE}_contract_{TEMPLATE}.json",
        "transition": OUT / f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{TEMPLATE}.json",
    }
    b.ANCHOR_IN = R43_ANCHOR
    b.SRC_OUT = {
        "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
        "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    }
    b.JSON_OUT = {
        "schema": OUT / f"{BASE}_schema_{TAG}.json",
        "contract": OUT / f"{BASE}_contract_{TAG}.json",
        "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
    }
    b.MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
    b.OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
    b.REJ = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
    b.SUP = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
    b.ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    b.retag = lambda value: _schema_residue_fix(value, ns)
    b.source_patch = ns["source_patch"]


def _seal_r43_rejection(b: Any) -> dict[str, str]:
    """Explicit-install hook; default self-check never calls this."""
    path = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
    if path.exists():
        value, raw = b.load(path)
        if value.get("failed_namespace") != PREV or \
           value.get("formal_global_closure_credit") != 0 or \
           value.get("rejection_reason") != \
           "R43_R42_REJECTION_WITNESS_PREFIX_ONLY_FAIL_CLOSED":
            raise RuntimeError("r43 rejection replay mismatch")
        return {"action": "replayed", "file_sha256": b.sha(raw),
                "object_sha256": value["object_sha256"]}
    anchor_raw = stable(R43_ANCHOR)
    anchor = json.loads(anchor_raw.decode("utf-8"))
    value = b.close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
        "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_STATIC_BUILD__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "R43_R42_REJECTION_WITNESS_PREFIX_ONLY_FAIL_CLOSED",
        "detail": {
            "candidate_install": True,
            "runtime_protocol_executed": False,
            "anchor_path": str(R43_ANCHOR.relative_to(ROOT)),
            "anchor_file_sha256": sha(anchor_raw),
            "anchor_object_sha256": anchor.get("object_sha256"),
            "schema_path": str(R43_SCHEMA.relative_to(ROOT)),
            "schema_file_sha256": R43_SCHEMA_SHA256,
            "schema_object_sha256": R43_SCHEMA_OBJECT_SHA256,
            "schema_description": R43_SCHEMA_DESCRIPTION,
            "r42_rejection_path": str(R42_REJECTION.relative_to(ROOT)),
            "r42_rejection_file_sha256": R42_REJECTION_SHA256,
            "guard_failure_object_sha256": R42_FAILURE_OBJECT_SHA256,
            "guard_failure_report_sha256": R42_FAILURE_REPORT_SHA256,
            "required_successor_fix": "r44 clean-room full-hash witness and no-pyc static build from immutable r39 bytes",
        },
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
        "runtime_surface_created": False,
    })
    raw = b.canon(value) + b"\n"
    b.install(path, raw)
    installed, installed_raw = b.load(path)
    return {"action": "installed", "file_sha256": b.sha(installed_raw),
            "object_sha256": installed["object_sha256"]}


def static_self_check() -> dict[str, Any]:
    """Read-only r44 chain, AST, and in-memory schema-retag verification."""
    if R43_COLD_MANIFEST.exists() or R43_COLD_OUTER.exists() or \
       any(path.exists() for path in R43_SIDE_RECEIPTS):
        raise RuntimeError("r43 positive/evidence surface unexpectedly exists")
    if any("v16r2r43" in str(path) for path in
           (ROOT / ".cm2-runtime").rglob("*") if path.exists()):
        raise RuntimeError("r43 runtime surface unexpectedly exists")
    r42_rejection_witness = _assert_r42_rejection_witness()
    schema_witness = _assert_r43_schema_residue()
    anchor = _assert_frozen(R43_ANCHOR, R43_ANCHOR_SHA256,
                            R43_ANCHOR_OBJECT_SHA256)
    if anchor.get("successor_namespace") != f"{PREV}_semantic_source" or \
       anchor.get("predecessor_namespace") != "v16r2r42":
        raise RuntimeError("r43 active anchor semantics")
    sup = _assert_frozen(R43_SUP, R43_SUP_SHA256, R43_SUP_OBJECT_SHA256)
    if sup.get("predecessor_namespace") != "v16r2r42" or \
       sup.get("successor_namespace") != PREV:
        raise RuntimeError("r43 supersession semantics")
    if not R43_TRANSITION.is_file() or sha(stable(R43_TRANSITION)) != R43_TRANSITION_SHA256:
        raise RuntimeError("r40->r43 transition drift")
    ns = load_r40_constructor()
    ns["PREV"] = PREV
    ns["TAG"] = TAG
    schema_path = OUT / f"{BASE}_schema_{TEMPLATE}.json"
    schema = json.loads(stable(schema_path).decode("utf-8"))
    fixed = _schema_residue_fix(schema, ns)
    if fixed.get("$id") != f"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.schema":
        raise RuntimeError("r44 schema id")
    if fixed.get("$comment") != f"CM2_{TAG.upper()}_DAG_STATIC_ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED":
        raise RuntimeError("r44 schema comment")
    if fixed.get("description") != SCHEMA_DESCRIPTION or "r9 schema" in fixed.get("description", "").lower():
        raise RuntimeError("r44 schema description")
    for def_name in ACTIVE_PROOF_DEFS:
        node = fixed["$defs"][def_name]
        if STALE_ACTIVE_PROOF_KEY in node.get("properties", {}) or \
           STALE_ACTIVE_PROOF_KEY in node.get("required", []) or \
           FRESH_ACTIVE_PROOF_KEY not in node.get("properties", {}) or \
           FRESH_ACTIVE_PROOF_KEY not in node.get("required", []):
            raise RuntimeError(f"r44 active proof key closure:{def_name}")
    bad = ns["schema_walk"](fixed)
    if bad:
        raise RuntimeError("r44 schema recursive node walk:" + ",".join(bad[:8]))
    contract_input = json.loads(stable(
        OUT / f"{BASE}_contract_{TEMPLATE}.json").decode("utf-8"))
    contract_fixed = _schema_residue_fix(contract_input, ns)
    if not str(contract_fixed.get("purpose", "")).startswith(
            f"Append-only {TAG} semantic bundle"):
        raise RuntimeError("r44 contract purpose residue")
    audit_input = json.loads(stable(
        OUT / f"{BASE}_static_audit_{TEMPLATE}.json").decode("utf-8"))
    audit_fixed = _schema_residue_fix(audit_input, ns)
    if audit_fixed.get("schema_and_constructor_closure", {}).get(
            "source_template_shape_review_pending") is not False:
        raise RuntimeError("r44 audit template-review residue")
    for name in ("retag_source", "retag_value", "source_patch", "schema_walk"):
        if not callable(ns.get(name)):
            raise RuntimeError(f"r40 constructor missing {name}")
    for role, rel in (
        ("producer", f"{BASE}_{TEMPLATE}_semantic_source.py"),
        ("consumer", f"{BASE}_independent_verifier_assembler_authority_consumer_{TEMPLATE}_semantic_source.py"),
        ("launcher", f"{BASE}_cold_launch_{TEMPLATE}_semantic_source.py"),
    ):
        retagged = ns["retag_source"](stable(OUT / rel).decode("utf-8"))
        edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
        anchor_name = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
        old_edge = f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json"
        if edge not in retagged or anchor_name not in retagged or old_edge in retagged:
            raise RuntimeError(f"{role}:r44 active edge/anchor retag")
    ast.parse(Path(__file__).read_text(encoding="utf-8"), filename=str(__file__))
    target_files = [
        OUT / f"{BASE}_{TAG}_semantic_source.py",
        OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
        OUT / f"{BASE}_schema_{TAG}.json",
        OUT / f"{BASE}_contract_{TAG}.json",
        OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        OUT / f"{BASE}_static_audit_{TAG}.json",
    ]
    if any(p.exists() for p in target_files):
        raise RuntimeError("r44 candidate target already exists")
    if any(TAG in str(p) for p in ROOT.rglob("*.pyc")):
        raise RuntimeError("r44 tagged pyc preexists")
    ns["assert_r39_partial"]()
    return {
        "status": "PASS_R44_CLEAN_ROOM_AST_SCHEMA_ACTIVE_PATH_STATIC_ONLY",
        "template_inputs": "immutable_r39_source_json_bytes",
        "predecessor_anchor": str(R43_ANCHOR.relative_to(ROOT)),
        "predecessor_anchor_file_sha256": R43_ANCHOR_SHA256,
        "predecessor_anchor_object_sha256": R43_ANCHOR_OBJECT_SHA256,
        "predecessor_namespace": PREV,
        "target_namespace": TAG,
        "schema_description_fixed": True,
        "r42_rejection_witness": r42_rejection_witness,
        "rejected_predecessor_schema_witness": schema_witness,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "installation_performed": False,
    }


def _install_r44() -> int:
    ns = load_r40_constructor()
    original_configure = ns["configure"]

    def configure_r44(module: Any, builder: Any) -> None:
        original_configure(module, builder)
        _configure_r44(ns, builder)

    ns["configure"] = configure_r44
    ns["seal_r39_rejection"] = _seal_r43_rejection
    return int(ns["main"]())


def main() -> int:
    try:
        result = static_self_check()
        if "--install" in sys.argv[1:]:
            return _install_r44()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "status": "FAIL_CLOSED_R44_CLEAN_ROOM_STATIC_ONLY",
            "error": {"type": type(exc).__name__, "message": str(exc)},
            "installation_performed": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
