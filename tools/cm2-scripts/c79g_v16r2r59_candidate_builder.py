#!/usr/bin/env python3
"""r59 append-only successor of the immutable r58 static candidate.

r58 closed the executable/schema shapes, but its active audit bundle carried
one stale V14 receipt path.  This wrapper loads the reviewed r58 builder only
as an inert in-memory recipe, repairs that path to the immutable V14
supersession receipt, and installs a fresh r59 chain with O_EXCL.  It never
modifies r58, creates manifest/outer/runtime surfaces, or grants credit.
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
PREV = "v16r2r58"
TAG = "v16r2r59"
INPUT_PREV = "v16r2r57"
INPUT_TAG = "v16r2r58"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

PARENT = ROOT / "scripts/c79g_v16r2r58_candidate_builder.py"
V14_PATH = (
    f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json")
V14_SHA = "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"
V14_OBJECT = "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"

R58_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R58_ANCHOR_SHA = "75ed65910e2aeffeb588ddc553dafc91116a9a6d6bee23074b58d0be34f78ed9"
R58_ANCHOR_OBJECT = "66b599ff985334ec95ea24367b5dee8ddfe5509c2322f5c3d09c18c217914d69"
R58_FILES: dict[str, tuple[Path, str, str | None]] = {
    "schema": (OUT / f"{BASE}_schema_{PREV}.json",
               "82a7ff395ec10fa3b2916808fb5c6dd979e59b62f239983caf580e6a91d38ccc", None),
    "contract": (OUT / f"{BASE}_contract_{PREV}.json",
                 "6e4829dcf14cf6c7420da81702a3e10db4b4a251a251dc9e0899746d9179d7e8",
                 "30e87fd03e72385eb9fb9da1465e81dca5d9f15117352e80b52ae31e59c9a92a"),
    "producer": (OUT / f"{BASE}_{PREV}_semantic_source.py",
                 "0c1789d05cbb1d99c5c56707ab2bfd2bb7def9560d032062617beb2d0b015f39", None),
    "consumer": (OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
                 "fcfddc117c8ac7c3b0e747a47e31fe9d073617452b7fd87edf6790fca65b4b05", None),
    "transition": (OUT / f"{BASE}_{INPUT_PREV}_to_{PREV}_static_launch_transition_receipt_v1.json",
                   "7760bc0ffbe050cfaa426273d9f2085848cf5c32c17cae035399026f7037eec6",
                   "17e3b395ac5e2cb18ac65518f551eeb53334c71dea83bf14bdf260b19190e03c"),
    "audit": (OUT / f"{BASE}_static_audit_{PREV}.json",
              "5f8d101d5d8375f234a47abff61ebfd2674466053a579844f5a4c55412f921e9",
              "9ae8389270ec47019595067eb8f1477fd6553adc4ad3a43b14c1ae263daf9752"),
    "launcher": (OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
                 "26a2af91bea70b7d8d1603fcc90d74c29ef387ae7060a6fa4447fb85f39a3a97", None),
}

REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
SUPERSESSION = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
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


def load_parent() -> dict[str, Any]:
    raw = PARENT.read_bytes()
    tree = ast.parse(raw.decode("utf-8"), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    ns: dict[str, Any] = {"__name__": "_r58_recipe_for_r59",
                          "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), ns, ns)
    return ns


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canon(body))
    return body


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pyc_inventory() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in ROOT.rglob("*.pyc"):
        if path.is_file() and not path.is_symlink():
            result[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    return result


def repair_audit(value: Any, parent_fix: Any) -> Any:
    out = parent_fix(value)
    if not isinstance(out, dict) or "static-audit" not in str(out.get("schema", "")):
        return out
    bundle = out.get("audited_v16r2_bundle", {})
    receipt = bundle.get("v14_registry_shape_drift_supersession_receipt")
    if not isinstance(receipt, dict):
        raise RuntimeError("r59 active V14 receipt field missing")
    receipt.update({"path": V14_PATH, "file_sha256": V14_SHA,
                    "object_sha256": V14_OBJECT})
    return out


def idempotent_registry_canonicalizer(text: str, parent_canon: Any) -> str:
    """Permit already-normalized r58 input, while retaining r58's patch gate."""
    tree = ast.parse(text, "r59_launcher_registry", mode="exec")
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and
               n.name == "producer_source_registry_shape_from_ast"), None)
    if fn is None:
        raise RuntimeError("r59 launcher registry helper missing")
    segment = ast.get_source_segment(text, fn) or ""
    old = segment.count("producer_v15") == 1 and segment.count("current v15") == 5
    current = segment.count("producer_v16r2") == 1 and segment.count("current v16r2") == 5
    if current:
        return text
    if old:
        return parent_canon(text)
    raise RuntimeError("r59 launcher registry diagnostic census")


def make_chain(parent: dict[str, Any]) -> dict[str, Any]:
    failure = {
        "r58_candidate_install": True,
        "active_audit_v14_alias_path": True,
        "active_audit_v14_alias_file_sha256":
            "74c82c804993a6b00196ba5c0b78a3c5067d3242452d61044229f3f04eaf4a7a",
        "active_audit_v14_alias_object_sha256":
            "3ead78915247f1a43eaa301d2ebd77d05f790f36530c59deeba677d747bae431",
        "r58_registry_expected_template_sha256":
            "f27a5e8df3308e5b022519929e8f0f64257dcbc35b355fa1537b0169d5604a8c",
        "r58_registry_current_sha256":
            "2acf6424fe5ca8c58bc19d28ff9fcf3b9326b7c62e59741adda17e5f8e84392d",
        "manifest_created": False, "outer_created": False,
        "runtime_protocol_executed": False,
    }
    for role, (_, file_hash, object_hash) in R58_FILES.items():
        failure[f"r58_{role}_file_sha256"] = file_hash
        if object_hash is not None:
            failure[f"r58_{role}_object_sha256"] = object_hash
    rejected = close({
        "schema": f"cm2.c79g.{PREV}.active-audit-v14-path-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R58_ACTIVE_AUDIT_V14_PATH_RESIDUE__ZERO_CREDIT",
        "failed_namespace": PREV, "predecessor_namespace": INPUT_PREV,
        "rejection_reason": "ACTIVE_AUDIT_V14_ALIAS_PATH_NOT_CANONICAL",
        "failure_vector": failure, "candidate_install": True,
        "runtime_protocol_executed": False, "manifest_created": False,
        "outer_created": False, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "append_only": True, "overwrite_delete_or_reuse_allowed": False,
        "predecessor_anchor_file_sha256": R58_ANCHOR_SHA,
        "predecessor_anchor_object_sha256": R58_ANCHOR_OBJECT,
    })
    rejected_raw = canon(rejected) + b"\n"
    rejection = {"path": str(REJECTION.relative_to(ROOT)),
                 "file_sha256": sha(rejected_raw),
                 "object_sha256": rejected["object_sha256"],
                 "bytes": rejected_raw}
    superseded = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.static-bundle-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV, "successor_namespace": TAG,
        "predecessor_active_anchor_path": str(R58_ANCHOR.relative_to(ROOT)),
        "predecessor_active_anchor_file_sha256": R58_ANCHOR_SHA,
        "predecessor_active_anchor_object_sha256": R58_ANCHOR_OBJECT,
        "predecessor_rejection_path": rejection["path"],
        "predecessor_rejection_file_sha256": rejection["file_sha256"],
        "predecessor_rejection_object_sha256": rejection["object_sha256"],
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


def main() -> int:
    try:
        print(json.dumps(P["install"](), ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
                          "status": "FAIL_CLOSED_R59_STATIC_INSTALL",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "candidate_install": False, "manifest_created": False,
                          "outer_created": False, "runtime_authorized": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False},
                         ensure_ascii=False, sort_keys=True))
        return 1


# Load and retarget the immutable r58 recipe before exposing the entry point.
P = load_parent()
parent_fix = P["fix_json"]
parent_canon = P["launcher_registry_canonicalizer"]

P.update({"PREV": PREV, "TAG": TAG, "INPUT_PREV": INPUT_PREV,
          "INPUT_TAG": INPUT_TAG, "R57_ANCHOR": R58_ANCHOR,
          "R57_ANCHOR_SHA": R58_ANCHOR_SHA,
          "R57_ANCHOR_OBJECT": R58_ANCHOR_OBJECT, "R57_FILES": R58_FILES,
          "REJECTION": REJECTION, "SUPERSESSION": SUPERSESSION,
          "ANCHOR": ANCHOR, "TARGETS": TARGETS})
R = P["_R57"]
R.update({"PREV": PREV, "TAG": TAG, "INPUT_PREV": INPUT_PREV,
          "INPUT_TAG": INPUT_TAG, "R56_ANCHOR": R58_ANCHOR,
          "R56_ANCHOR_SHA": R58_ANCHOR_SHA,
          "R56_ANCHOR_OBJECT": R58_ANCHOR_OBJECT, "R56_FILES": R58_FILES,
          "REJECTION": REJECTION, "SUPERSESSION": SUPERSESSION,
          "ANCHOR": ANCHOR, "TARGETS": TARGETS})

P["fix_json"] = lambda value: repair_audit(value, parent_fix)
P["launcher_registry_canonicalizer"] = lambda text: \
    idempotent_registry_canonicalizer(text, parent_canon)
R["make_chain"] = lambda: make_chain(P)

parent_validate = P["validate_generated"]
def validate_generated(generated: dict[str, bytes], meta: dict[str, Any],
                       chain: dict[str, Any]) -> None:
    parent_validate(generated, meta, chain)
    audit = json.loads(generated["audit"])
    receipt = audit.get("audited_v16r2_bundle", {}).get(
        "v14_registry_shape_drift_supersession_receipt", {})
    if (receipt.get("path"), receipt.get("file_sha256"),
            receipt.get("object_sha256")) != (V14_PATH, V14_SHA, V14_OBJECT):
        raise RuntimeError("r59 active V14 receipt path/hash closure")
R["validate_generated"] = validate_generated

if __name__ == "__main__":
    raise SystemExit(main())
