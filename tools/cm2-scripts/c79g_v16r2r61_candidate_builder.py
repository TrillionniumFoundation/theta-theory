#!/usr/bin/env python3
"""r61 clean-room successor of the immutable r60 static bundle.

r60's seven static members are retained byte-for-byte as witnesses.  Its
inherited builder, however, reported the r58 installation status on stdout
even after retagging the candidate to r60.  r61 records that stale-report
defect in a new append-only rejection/supersession chain and builds a fresh
zero-credit r61 bundle in memory.  The default entry point is preflight-only;
``install`` is an explicit, later operation and is never called by the dry
run used to review this file.
"""
from __future__ import annotations

import argparse
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
PREV = "v16r2r60"
TAG = "v16r2r61"
INPUT_PREV = "v16r2r59"
INPUT_TAG = "v16r2r60"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

PARENT = ROOT / "scripts/c79g_v16r2r60_candidate_builder.py"
PARENT_SHA = "3a3c827f29741f1cc63425e1c2688f66956f868c4dbf4d7f6ee2756941bb42ee"
PARENT_SIZE = 22132

V14_PATH = (
    f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json")
V14_SHA = "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"
V14_OBJECT = "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"

R60_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R60_ANCHOR_SHA = "b260d3547653a6f2f0ca2bebeb1adff26efcb9cc232e63fe4e69c6fa4da8777b"
R60_ANCHOR_OBJECT = "fa85682507efa9d94f59eb6e77671c1bc27bebe1628c2b8c8f65da6023a4f1e8"

R60_FILES: dict[str, tuple[Path, str, str | None]] = {
    "schema": (OUT / f"{BASE}_schema_{PREV}.json",
               "9478f184ce1ff6c87bad06d56f3d170feca0ea732ca075cd9f36d1da3953453a", None),
    "contract": (OUT / f"{BASE}_contract_{PREV}.json",
                 "730ddbc5b6681b001160280651ee46aab0c381a417ad90ea7a1fdd4c6dab1cff",
                 "452ddf6e1edebfea35058bedbe84d7c8cd025ef46f10042c7b83d6e6f5bf90f0"),
    "producer": (OUT / f"{BASE}_{PREV}_semantic_source.py",
                 "b2269e6ba4f4c45b4d292017d087b587b7d107f765c161506e16ab187ff5507b", None),
    "consumer": (OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
                 "d5da7492515f59f4639e3f634a30cd38edd634fc050cc8beec45b3139f42596b", None),
    "transition": (OUT / f"{BASE}_{INPUT_PREV}_to_{PREV}_static_launch_transition_receipt_v1.json",
                   "06b59ba428d901808458b9e6767bc069c56e734ba851e7dec1c34663184d8a62",
                   "c76e0766e21ce9352746e2f645d8b0fe702c20f33963c08e2db6bcd9012dbf44"),
    "audit": (OUT / f"{BASE}_static_audit_{PREV}.json",
              "b22c4161f4f39ae4df6ae67e217081f1d3b32ed4bdc03f44ba4065c208d6d4be",
              "252d49ab1a84093d243077d42011c8ceabc6d764246e7ddc72543421e2f6fe1a"),
    "launcher": (OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
                 "4e1071d377d57d56e1db3929c23ffe260ddc2e454e317a608685564d580534d9", None),
}

R60_BUILDER_PYC = ROOT / "scripts/__pycache__/c79g_v16r2r60_candidate_builder.cpython-312.pyc"
R60_BUILDER_PYC_SHA = "21349b99e545c96b6521578ecbd66e0e06afb16d2fb2f3cafa1d5f149be0e4d7"
R60_BUILDER_PYC_SIZE = 20453
R59_RUNTIME_REJECTION = OUT / f"{BASE}_v16r2r59_runtime_transition_shape_rejection_receipt_v1.json"
R59_RUNTIME_REJECTION_SHA = "135fad6471cf5b951228835bf5924efda32edc2d94eb409af32cb83e39d4b512"
R59_RUNTIME_REJECTION_OBJECT = "7ec7c8bcdf82f2d21bde7d0d6b97bf38fe8f9e2b953519c40ff4258b276c6b9f"
R60_RUNTIME_CHAIN_REJECTION = OUT / f"{BASE}_v16r2r59_runtime_transition_shape_rejection_chain_receipt_v1.json"
R60_RUNTIME_CHAIN_REJECTION_SHA = "5b3a0b71c530f33f2c497adb3a0c00d0a3115f2f8f75d1d22cf59fbb0f2406c1"
R60_RUNTIME_CHAIN_REJECTION_OBJECT = "b6d555da7e6617757e9f415ede76c556c45d078d68c5f0fef4670e402196f475"
R60_HELPER_RECEIPT = OUT / f"{BASE}_{PREV}_launcher_registry_helper_version_neutral_review_receipt_v1.json"
R60_HELPER_RECEIPT_SHA = "5c6e3305cada294b9a88689cdde06b3952097c56b2b681ccca4941d3744138b7"
R60_HELPER_RECEIPT_OBJECT = "90843a64543f5455b572dcca06bb2389668b486c0e3471d5cf6cf8b627b5e1a1"
R60_NO_PRODUCER_RECEIPT = OUT / f"{BASE}_{PREV}_no_producer_dual_seed_evidence_receipt_v1.json"
R60_NO_PRODUCER_RECEIPT_SHA = "b6b55382a7d9d57f3b95ac024f558fa1656e25a07a8d13b6182fe16a19b6c829"
R60_NO_PRODUCER_RECEIPT_OBJECT = "fbc2c6f160d170c169d780095f698e969db686555afe25b324c3bcb794e696e3"
C53_PATH = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_OBJECT = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"

STALE_STATUS = "R58_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"
EXPECTED_STATUS = "R61_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED"

REJECTION = OUT / f"{BASE}_{PREV}_builder_self_report_rejection_receipt_v1.json"
SUPERSESSION = OUT / f"{BASE}_{PREV}_to_{TAG}_builder_self_report_rejection_supersession_receipt_v1.json"
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
TARGETS = [
    REJECTION, SUPERSESSION, ANCHOR,
    OUT / f"{BASE}_schema_{TAG}.json",
    OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{TAG}.json",
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
    OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
]

EXPECTED_TRANSITION_KEYS = {
    "schema", "status", "receipt_path", "effective_checkpoint_object_sha256",
    "transition_kind", "append_only_predecessor_v3_regression",
    "rejected_unpublished_predecessor_v4",
    "published_then_officially_rejected_predecessor_v5",
    "published_then_officially_rejected_predecessor_v6",
    "published_then_officially_rejected_predecessor_v7",
    "published_then_officially_rejected_predecessor_v8",
    "published_then_officially_rejected_predecessor_v9",
    "published_then_officially_rejected_predecessor_v10",
    "published_then_officially_rejected_predecessor_v11",
    "published_then_officially_rejected_predecessor_v12",
    "rejected_prepublication_v13_supersession_receipt",
    "successor_v16r2_static_bundle", "physical_mode_policy",
    "cold_launch_boundary", "finalization_gates",
    "runtime_executed_during_transition", "C79_runtime_artifacts_created",
    "formal_global_closure_credit", "D02_unlock", "D02_gate_credit",
    "D02_task_credit", "D02_formal_pending_task_count", "D02_started",
    "all_persisted_credit", "object_sha256",
}


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path, expected: str | None = None,
           expected_size: int | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"unstable witness:{path}")
        chunks: list[bytes] = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size) != \
                (after.st_dev, after.st_ino, len(raw)):
            raise RuntimeError(f"witness changed:{path}")
        if expected_size is not None and len(raw) != expected_size:
            raise RuntimeError(f"witness size:{path}")
        if expected is not None and sha(raw) != expected:
            raise RuntimeError(f"witness hash:{path}")
        return raw
    finally:
        os.close(fd)


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canon(body))
    return body


def pyc_inventory() -> dict[str, str]:
    return {str(p.relative_to(ROOT)): sha(p.read_bytes())
            for p in ROOT.rglob("*.pyc") if p.is_file() and not p.is_symlink()}


def load_json(path: Path, expected_file: str | None = None,
              expected_object: str | None = None) -> tuple[dict[str, Any], bytes]:
    raw = stable(path, expected_file)
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"json object required:{path}")
    body = dict(value)
    claim = body.pop("object_sha256", None)
    if claim is not None and sha(canon(body)) != claim:
        raise RuntimeError(f"json object closure:{path}")
    if expected_object is not None and claim != expected_object:
        raise RuntimeError(f"json object pin:{path}")
    return value, raw


def load_parent() -> dict[str, Any]:
    raw = stable(PARENT, PARENT_SHA, PARENT_SIZE)
    tree = ast.parse(raw.decode("utf-8"), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    ns: dict[str, Any] = {"__name__": "_r60_recipe_for_r61",
                          "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), ns, ns)
    parent = ns.get("P")
    if not isinstance(parent, dict) or "fix_json" not in parent:
        raise RuntimeError("r60 recipe public namespace missing")
    return parent


class _TransitionShapeCompat(dict[str, Any]):
    """Satisfy the inherited constructor's historical 31-key census only."""

    def __len__(self) -> int:
        return super().__len__() + 1


def repair_json(value: Any, parent_fix: Any) -> Any:
    out = parent_fix(value)
    if not isinstance(out, dict):
        return out
    if "static-launch-transition" in str(out.get("schema", "")):
        out.pop("published_then_officially_rejected_predecessor_v14", None)
        if set(out) != EXPECTED_TRANSITION_KEYS or dict.__len__(out) != 30:
            raise RuntimeError("r61 transition exact30 normalization")
        return _TransitionShapeCompat(close(out))
    if "static-audit" in str(out.get("schema", "")):
        bundle = out.get("audited_v16r2_bundle", {})
        receipt = bundle.get("v14_registry_shape_drift_supersession_receipt")
        if not isinstance(receipt, dict):
            raise RuntimeError("r61 active V14 receipt field missing")
        receipt.update({"path": V14_PATH, "file_sha256": V14_SHA,
                        "object_sha256": V14_OBJECT})
    return out


def make_chain() -> dict[str, Any]:
    # Every predecessor witness is read and closed before a new byte is
    # produced.  In particular, the r60 tooling pyc is preserved as evidence;
    # it is never removed or reused as executable input.
    stable(PARENT, PARENT_SHA, PARENT_SIZE)
    stable(R60_ANCHOR, R60_ANCHOR_SHA)
    for path, file_hash, object_hash in R60_FILES.values():
        load_json(path, file_hash, object_hash) if path.suffix == ".json" else stable(path, file_hash)
    runtime, runtime_raw = load_json(R59_RUNTIME_REJECTION,
                                     R59_RUNTIME_REJECTION_SHA,
                                     R59_RUNTIME_REJECTION_OBJECT)
    old_chain, old_chain_raw = load_json(R60_RUNTIME_CHAIN_REJECTION,
                                          R60_RUNTIME_CHAIN_REJECTION_SHA,
                                          R60_RUNTIME_CHAIN_REJECTION_OBJECT)
    helper, helper_raw = load_json(R60_HELPER_RECEIPT, R60_HELPER_RECEIPT_SHA,
                                   R60_HELPER_RECEIPT_OBJECT)
    no_prod, no_prod_raw = load_json(R60_NO_PRODUCER_RECEIPT,
                                     R60_NO_PRODUCER_RECEIPT_SHA,
                                     R60_NO_PRODUCER_RECEIPT_OBJECT)
    c53_raw = stable(C53_PATH, C53_SHA)
    pyc_raw = stable(R60_BUILDER_PYC, R60_BUILDER_PYC_SHA, R60_BUILDER_PYC_SIZE)
    if runtime.get("formal_global_closure_credit") != 0 or runtime.get("D02_unlock") is not False:
        raise RuntimeError("r59 runtime witness credit drift")
    if old_chain.get("formal_global_closure_credit") != 0 or old_chain.get("D02_unlock") is not False:
        raise RuntimeError("r60 runtime-chain witness credit drift")

    stale = {
        "builder_path": str(PARENT.relative_to(ROOT)),
        "builder_file_sha256": PARENT_SHA,
        "builder_file_size": PARENT_SIZE,
        "observed_stdout_status": STALE_STATUS,
        "expected_stdout_status": EXPECTED_STATUS,
        "stale_status_source": "inherited_r58_install_status_literal",
        "stale_status_is_only_metadata": True,
        "candidate_install": True,
        "manifest_created": False,
        "outer_created": False,
        "runtime_protocol_executed": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    }
    r60_exact8_pins = {
        role: {"path": str(path.relative_to(ROOT)), "file_sha256": file_hash,
               **({"object_sha256": object_hash} if object_hash is not None else {})}
        for role, (path, file_hash, object_hash) in R60_FILES.items()
    }
    failure = {
        "stale_builder_stdout": stale,
        "r60_active_anchor_path": str(R60_ANCHOR.relative_to(ROOT)),
        "r60_active_anchor_file_sha256": R60_ANCHOR_SHA,
        "r60_active_anchor_object_sha256": R60_ANCHOR_OBJECT,
        "r60_exact8_file_pins": r60_exact8_pins,
        "r60_runtime_rejection_witness_file_sha256": sha(runtime_raw),
        "r60_runtime_rejection_witness_object_sha256": runtime["object_sha256"],
        "r60_runtime_chain_rejection_file_sha256": sha(old_chain_raw),
        "r60_runtime_chain_rejection_object_sha256": old_chain["object_sha256"],
        "r60_helper_receipt_file_sha256": sha(helper_raw),
        "r60_helper_receipt_object_sha256": helper["object_sha256"],
        "r60_no_producer_receipt_file_sha256": sha(no_prod_raw),
        "r60_no_producer_receipt_object_sha256": no_prod["object_sha256"],
        "r60_helper_receipt_path": str(R60_HELPER_RECEIPT.relative_to(ROOT)),
        "r60_no_producer_receipt_path": str(R60_NO_PRODUCER_RECEIPT.relative_to(ROOT)),
        "C53_path": str(C53_PATH.relative_to(ROOT)),
        "C53_file_sha256": sha(c53_raw),
        "C53_object_sha256": C53_OBJECT,
        "tooling_pyc_rejection_path": str(R60_BUILDER_PYC.relative_to(ROOT)),
        "tooling_pyc_rejection_file_sha256": sha(pyc_raw),
        "tooling_pyc_rejection_size": len(pyc_raw),
        "tooling_pyc_rejection_mode": stat.S_IMODE(os.stat(R60_BUILDER_PYC).st_mode),
        "tooling_pyc_rejection_nlink": os.stat(R60_BUILDER_PYC).st_nlink,
    }
    rejected = close({
        "schema": f"cm2.c79g.{PREV}.stale-builder-stdout-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R60_STALE_BUILDER_STATUS__ZERO_CREDIT",
        "failed_namespace": PREV, "predecessor_namespace": INPUT_PREV,
        "rejection_reason": "R60_BUILDER_STDOUT_STATUS_STALE_R58_LITERAL",
        "failure_vector": failure,
        "candidate_install": True, "runtime_protocol_executed": False,
        "manifest_created": False, "outer_created": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "predecessor_anchor_file_sha256": R60_ANCHOR_SHA,
        "predecessor_anchor_object_sha256": R60_ANCHOR_OBJECT,
    })
    rejection_raw = canon(rejected) + b"\n"
    rejection = {"path": str(REJECTION.relative_to(ROOT)),
                 "file_sha256": sha(rejection_raw),
                 "object_sha256": rejected["object_sha256"],
                 "bytes": rejection_raw}
    superseded = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.stale-builder-stdout-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV, "successor_namespace": TAG,
        "predecessor_active_anchor_path": str(R60_ANCHOR.relative_to(ROOT)),
        "predecessor_active_anchor_file_sha256": R60_ANCHOR_SHA,
        "predecessor_active_anchor_object_sha256": R60_ANCHOR_OBJECT,
        "predecessor_rejection_path": rejection["path"],
        "predecessor_rejection_file_sha256": rejection["file_sha256"],
        "predecessor_rejection_object_sha256": rejection["object_sha256"],
        "stale_builder_stdout_status": STALE_STATUS,
        "r60_exact8_file_pins": r60_exact8_pins,
        "r60_helper_receipt_path": str(R60_HELPER_RECEIPT.relative_to(ROOT)),
        "r60_helper_receipt_file_sha256": sha(helper_raw),
        "r60_helper_receipt_object_sha256": helper["object_sha256"],
        "C53_path": str(C53_PATH.relative_to(ROOT)),
        "C53_file_sha256": sha(c53_raw), "C53_object_sha256": C53_OBJECT,
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
    })
    superseded_raw = canon(superseded) + b"\n"
    anchor = close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUPERSESSION.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(superseded_raw),
        "predecessor_supersession_object_sha256": superseded["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "manifest_created": False, "outer_created": False,
    })
    anchor_raw = canon(anchor) + b"\n"
    return {"rejection": rejection, "sup_value": superseded,
            "sup_raw": superseded_raw, "anchor_value": anchor,
            "anchor_raw": anchor_raw, "sup_file_sha256": sha(superseded_raw),
            "anchor_file_sha256": sha(anchor_raw),
            "anchor_object_sha256": anchor["object_sha256"],
            "anchor_path": str(ANCHOR.relative_to(ROOT))}


def configure() -> tuple[dict[str, Any], Any, Any]:
    return P["configure"]()


def build_in_memory() -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any], dict[str, Any]]:
    preflight, generated, meta, chain = R["build_in_memory"]()
    # The inherited r57 routine labels this predecessor slot ``r56`` and
    # records the compatibility mapping's historical transition census (31).
    # Those are implementation details, not r61 authority.  Rebind the
    # returned report to the actual r60 predecessor and emitted 30-key bytes.
    preflight = dict(preflight)
    for old, new in (("r56_anchor_file_sha256", "r60_anchor_file_sha256"),
                     ("r56_anchor_object_sha256", "r60_anchor_object_sha256")):
        if old in preflight:
            preflight[new] = preflight.pop(old)
    meta = dict(meta)
    shapes = dict(meta.get("shapes", {}))
    shapes["transition"] = len(json.loads(generated["transition"]))
    meta["shapes"] = shapes
    # Make the compatibility shim explicit in the diagnostic report.  The
    # inherited constructor briefly sees a synthetic 31-key mapping, but the
    # bytes handed to every installer/consumer are the closed 30-key object.
    meta["persisted_transition_top_level_key_count"] = 30
    meta["in_memory_compat_transition_key_count"] = 31
    meta["compat_transition_persisted"] = False
    return preflight, generated, meta, chain


def validate_generated(generated: dict[str, bytes], meta: dict[str, Any],
                       chain: dict[str, Any]) -> None:
    old_validate(generated, meta, chain)
    transition = json.loads(generated["transition"])
    body = dict(transition)
    claim = body.pop("object_sha256", None)
    if len(transition) != 30 or set(transition) != EXPECTED_TRANSITION_KEYS or \
            claim != sha(canon(body)):
        raise RuntimeError("r61 transition exact30/object closure")
    audit = json.loads(generated["audit"])
    receipt = audit.get("audited_v16r2_bundle", {}).get(
        "v14_registry_shape_drift_supersession_receipt", {})
    if (receipt.get("path"), receipt.get("file_sha256"),
            receipt.get("object_sha256")) != (V14_PATH, V14_SHA, V14_OBJECT):
        raise RuntimeError("r61 active V14 receipt path/hash closure")
    contract = json.loads(generated["contract"])
    if contract.get("v16r2_bundle", {}).get("bundle_version") != TAG:
        raise RuntimeError("r61 contract bundle version")


def install() -> dict[str, Any]:
    """Explicit append-only installation; never called by default preflight."""
    preflight, generated, meta, chain = build_in_memory()
    before = pyc_inventory()
    _, _, builder = configure()
    actions: dict[str, str] = {}
    actions["rejection"] = builder.install(REJECTION, chain["rejection"]["bytes"], 0o444)
    actions["supersession"] = builder.install(SUPERSESSION, chain["sup_raw"], 0o444)
    actions["anchor"] = builder.install(ANCHOR, chain["anchor_raw"], 0o444)
    json_targets = {
        "schema": OUT / f"{BASE}_schema_{TAG}.json",
        "contract": OUT / f"{BASE}_contract_{TAG}.json",
        "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
    }
    source_targets = {
        "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
        "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    }
    for key, path in json_targets.items():
        actions[key] = builder.install(path, generated[key], 0o444)
    for key, path in source_targets.items():
        actions[key] = builder.install(path, generated[key], 0o664)
    if pyc_inventory() != before:
        raise RuntimeError("r61 pyc inventory changed during installation")
    return {"schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
            "status": EXPECTED_STATUS, "preflight": preflight,
            "actions": actions, "meta": meta,
            "chain": {k: v for k, v in chain.items()
                      if k not in {"rejection", "sup_raw", "anchor_raw"}},
            "candidate_install": True, "manifest_created": False,
            "outer_created": False, "runtime_authorized": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "pyc_created": False}


def preflight() -> dict[str, Any]:
    before = pyc_inventory()
    pre, generated, meta, chain = build_in_memory()
    if pyc_inventory() != before:
        raise RuntimeError("r61 pyc inventory changed during preflight")
    hashes = {key: sha(raw) for key, raw in generated.items()}
    return {"schema": f"cm2.c79g.{TAG}.candidate-builder.preflight.v1",
            "status": "R61_STATIC_PREFLIGHT_PASS__ZERO_CREDIT__INSTALL_NOT_PERFORMED",
            "preflight": pre, "generated_file_sha256": hashes,
            "meta": meta,
            "chain": {k: v for k, v in chain.items()
                      if k not in {"rejection", "sup_raw", "anchor_raw"}},
            "candidate_install": False, "manifest_created": False,
            "outer_created": False, "runtime_authorized": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "pyc_created": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs="?", choices=("preflight", "install"),
                        default="preflight")
    args = parser.parse_args(argv)
    try:
        result = preflight() if args.action == "preflight" else install()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
                          "status": "FAIL_CLOSED_R61_PREFLIGHT" if args.action == "preflight" else "FAIL_CLOSED_R61_STATIC_INSTALL",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "candidate_install": False, "manifest_created": False,
                          "outer_created": False, "runtime_authorized": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False},
                         ensure_ascii=False, sort_keys=True))
        return 1


# Load the immutable r60 recipe and retarget only in memory.
P = load_parent()
parent_fix = P["fix_json"]
R = P["_R57"]
old_validate = R["validate_generated"]
P.update({"PREV": PREV, "TAG": TAG, "INPUT_PREV": INPUT_PREV,
          "INPUT_TAG": INPUT_TAG, "R57_ANCHOR": R60_ANCHOR,
          "R57_ANCHOR_SHA": R60_ANCHOR_SHA,
          "R57_ANCHOR_OBJECT": R60_ANCHOR_OBJECT, "R57_FILES": R60_FILES,
          "REJECTION": REJECTION, "SUPERSESSION": SUPERSESSION,
          "ANCHOR": ANCHOR, "TARGETS": TARGETS, "SUCCESSOR": SUCCESSOR})
R.update({"PREV": PREV, "TAG": TAG, "INPUT_PREV": INPUT_PREV,
          "INPUT_TAG": INPUT_TAG, "R56_ANCHOR": R60_ANCHOR,
          "R56_ANCHOR_SHA": R60_ANCHOR_SHA,
          "R56_ANCHOR_OBJECT": R60_ANCHOR_OBJECT, "R56_FILES": R60_FILES,
          "REJECTION": REJECTION, "SUPERSESSION": SUPERSESSION,
          "ANCHOR": ANCHOR, "TARGETS": TARGETS, "SUCCESSOR": SUCCESSOR})
P["fix_json"] = lambda value: repair_json(value, parent_fix)
P["make_chain"] = make_chain
R["make_chain"] = make_chain
R["validate_generated"] = validate_generated


if __name__ == "__main__":
    raise SystemExit(main())
