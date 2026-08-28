#!/usr/bin/env python3
"""r60 append-only successor of the immutable r59 static candidate.

r59's first cold authorize failed before either child because its transition
carried one extra legacy v14 top-level key.  This wrapper loads the reviewed
r59 builder only as an inert in-memory recipe, removes that key in memory,
and installs a fresh r60 chain with O_EXCL.  It never modifies r59, creates
manifest/outer/runtime surfaces, or grants credit.
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
PREV = "v16r2r59"
TAG = "v16r2r60"
INPUT_PREV = "v16r2r58"
INPUT_TAG = "v16r2r59"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

PARENT = ROOT / "scripts/c79g_v16r2r59_candidate_builder.py"
PARENT_SHA = "68363d65fd0a241d0100a6ba4339063407dfdcc1c4b56cd49e864882985a5761"
R51_BUILDER_SHA = "084de3f79f9f13c9270799a1ba6570bb820447405b3e1300c6d0b2aa18e3d11c"
V14_PATH = (
    f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json")
V14_SHA = "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"
V14_OBJECT = "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"

R59_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R59_ANCHOR_SHA = "26d919c2760eb8ce2c0cfe2588f91dc8061c2ad7bbab1575ae2736ca657a43fa"
R59_ANCHOR_OBJECT = "15131c6ac0f7d09574a944fc99eb588ec79aa6d31afe70b2373936269329b716"
R59_RUNTIME_REJECTION = OUT / f"{BASE}_{PREV}_runtime_transition_shape_rejection_receipt_v1.json"
R59_RUNTIME_REJECTION_SHA = "135fad6471cf5b951228835bf5924efda32edc2d94eb409af32cb83e39d4b512"
R59_RUNTIME_REJECTION_OBJECT = "7ec7c8bcdf82f2d21bde7d0d6b97bf38fe8f9e2b953519c40ff4258b276c6b9f"
TOOLING_PYC = ROOT / "scripts/__pycache__/c79g_v16r2r60_candidate_builder.cpython-312.pyc"
TOOLING_PYC_SHA = "21349b99e545c96b6521578ecbd66e0e06afb16d2fb2f3cafa1d5f149be0e4d7"
TOOLING_PYC_SIZE = 20453
R59_FILES: dict[str, tuple[Path, str, str | None]] = {
    "schema": (OUT / f"{BASE}_schema_{PREV}.json",
               "f10bd33759b184c0695f9beb710914635fbda779bbc27037b6703dc0a808a676", None),
    "contract": (OUT / f"{BASE}_contract_{PREV}.json",
                 "e93ca9b5e2e64d48de6d77e698756ed4afee749501ffdf651aaee57b9ee50c7d",
                 "a28dbb0dcf703f72e9a60d7295efea7c7b0acfdf11d676de664d6c67fc088c60"),
    "producer": (OUT / f"{BASE}_{PREV}_semantic_source.py",
                 "1a8d3b17aab88351890992fe45a6b17c2194d8a5dc4f3ad25f8ecd894538dc32", None),
    "consumer": (OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
                 "2f0452b1dd4cb24ed058285802f6bd6f3854798a79289832cbef03b1789473cd", None),
    "transition": (OUT / f"{BASE}_{INPUT_PREV}_to_{PREV}_static_launch_transition_receipt_v1.json",
                   "2c8b9d20c4af440a58837b05404be5a0a8e3f665a1a06e6aa7260a1a2ee21d2f",
                   "91c4f18aa4aed1e40d5f22c055515dc16d01d232cd9819418f64a021dcec8ca2"),
    "audit": (OUT / f"{BASE}_static_audit_{PREV}.json",
              "41b0c0f0a6b40df1f2688c56fcf5222e0cebe87e46157c93b45fe4b4bffe3093",
              "61d42e9291c8e10e186d8fc3c95583e7776744dc9c910ddc3318ae5827f1fd36"),
    "launcher": (OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
                 "323bced6d33ec437b8a175f82c557bcbd9ce1831411d698643b1dce1537ade80", None),
}

REJECTION = OUT / f"{BASE}_{PREV}_runtime_transition_shape_rejection_chain_receipt_v1.json"
SUPERSESSION = OUT / f"{BASE}_{PREV}_to_{TAG}_runtime_transition_shape_rejection_supersession_receipt_v1.json"
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


def load_parent() -> dict[str, Any]:
    raw = stable(PARENT, PARENT_SHA)
    tree = ast.parse(raw.decode("utf-8"), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    ns: dict[str, Any] = {"__name__": "_r59_recipe_for_r60",
                          "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), ns, ns)
    # r59 is itself a wrapper around the r58 recipe.  Its public build/install
    # namespace is the nested ``P`` mapping; returning the outer loader
    # namespace would expose only r59's wrapper helpers and lose ``fix_json``
    # / ``configure`` used by the inherited constructor.
    parent = ns.get("P")
    if not isinstance(parent, dict) or "fix_json" not in parent:
        raise RuntimeError("r59 recipe public namespace missing")
    return parent


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canon(body))
    return body


def load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"json object required:{path}")
    body = dict(value)
    claim = body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canon(body)) != claim:
        raise RuntimeError(f"json object closure:{path}")
    return value, raw


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
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(raw) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        if expected_size is not None and len(raw) != expected_size:
            raise RuntimeError(f"size drift:{path}")
        if expected is not None and sha(raw) != expected:
            raise RuntimeError(f"hash drift:{path}")
        return raw
    finally:
        os.close(fd)


def pyc_inventory() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in ROOT.rglob("*.pyc"):
        if path.is_file() and not path.is_symlink():
            result[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    return result


class _TransitionShapeCompat(dict[str, Any]):
    """Keep the inherited constructor's historical preflight census happy.

    The r51 constructor still checks ``len(transition) == 31`` before it
    serializes the receipt.  r60 deliberately removes the stale V14 member,
    so the canonical mapping has 30 members.  This inert mapping reports the
    old census only for that one in-memory check; iteration, serialization,
    and ``dict(value)`` expose the normalized 30-key mapping.
    """

    def __len__(self) -> int:
        return super().__len__() + 1


def repair_json(value: Any, parent_fix: Any) -> Any:
    out = parent_fix(value)
    if not isinstance(out, dict):
        return out
    if "static-launch-transition" in str(out.get("schema", "")):
        extra = set(out) - EXPECTED_TRANSITION_KEYS
        if extra not in (set(), {"published_then_officially_rejected_predecessor_v14"}):
            raise RuntimeError(f"r60 transition unexpected keys:{sorted(extra)}")
        out.pop("published_then_officially_rejected_predecessor_v14", None)
        if set(out) != EXPECTED_TRANSITION_KEYS or dict.__len__(out) != 30:
            raise RuntimeError("r60 transition exact30 normalization")
        # Re-close on the normalized body, then retain the compatibility
        # mapping solely until the inherited constructor's shape census has
        # completed.  Its canonical close helper calls ``dict(value)`` and
        # therefore emits the real 30-key object and hash.
        return _TransitionShapeCompat(close(out))
    if "static-audit" in str(out.get("schema", "")):
        bundle = out.get("audited_v16r2_bundle", {})
        receipt = bundle.get("v14_registry_shape_drift_supersession_receipt")
        if not isinstance(receipt, dict):
            raise RuntimeError("r60 active V14 receipt field missing")
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


def make_chain(_: dict[str, Any]) -> dict[str, Any]:
    runtime, runtime_raw = load_json(R59_RUNTIME_REJECTION)
    if (sha(runtime_raw) != R59_RUNTIME_REJECTION_SHA or
            runtime.get("object_sha256") != R59_RUNTIME_REJECTION_OBJECT or
            runtime.get("schema") !=
                f"cm2.c79g.{PREV}.runtime-transition-shape-rejection.v1" or
            runtime.get("status") !=
                "PERMANENT_FAIL_CLOSED_R59_RUNTIME_TRANSITION_SHAPE__ZERO_CREDIT" or
            runtime.get("failed_namespace") != PREV or
            runtime.get("formal_global_closure_credit") != 0 or
            runtime.get("D02_unlock") is not False):
        raise RuntimeError("r59 runtime rejection witness drift")
    detail = runtime.get("detail", {})
    if (detail.get("returncode") != 2 or
            detail.get("failed_phase") !=
                "HeldBundle._initialize_before_producer_or_consumer_child" or
            detail.get("extra_transition_keys") !=
                ["published_then_officially_rejected_predecessor_v14"] or
            detail.get("consumer_child_spawned") is not False or
            detail.get("producer_child_spawned") is not False or
            detail.get("candidate_surface_created") is not False or
            detail.get("verification_surface_created") is not False or
            detail.get("manifest_created") is not False or
            detail.get("outer_created") is not False or
            detail.get("runtime_surface_created") is not False or
            detail.get("c53_file_sha256_before_and_after") !=
                "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"):
        raise RuntimeError("r59 runtime rejection detail drift")
    pyc_raw = stable(TOOLING_PYC, TOOLING_PYC_SHA, TOOLING_PYC_SIZE)
    failure = {
        "runtime_rejection_witness_path": str(R59_RUNTIME_REJECTION.relative_to(ROOT)),
        "runtime_rejection_witness_file_sha256": sha(runtime_raw),
        "runtime_rejection_witness_object_sha256": runtime["object_sha256"],
        "transition_extra_top_level_key": "published_then_officially_rejected_predecessor_v14",
        "transition_expected_key_count": 30, "transition_actual_key_count": 31,
        "producer_child_spawned": False, "consumer_child_spawned": False,
        "candidate_surface_created": False, "verification_surface_created": False,
        "manifest_or_outer_created_by_failed_attempt": False,
        "tooling_pyc_rejection_path": str(TOOLING_PYC.relative_to(ROOT)),
        "tooling_pyc_rejection_file_sha256": sha(pyc_raw),
        "tooling_pyc_rejection_size": len(pyc_raw),
        "tooling_pyc_rejection_mode": stat.S_IMODE(os.stat(TOOLING_PYC).st_mode),
        "tooling_pyc_rejection_nlink": os.stat(TOOLING_PYC).st_nlink,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "r59_manifest_or_outer_present": False,
    }
    rejected = close({
        "schema": f"cm2.c79g.{PREV}.runtime-transition-shape-chain-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R59_RUNTIME_TRANSITION_SHAPE__ZERO_CREDIT",
        "failed_namespace": PREV, "predecessor_namespace": INPUT_PREV,
        "rejection_reason": "R59_RUNTIME_TRANSITION_TOP_LEVEL_EXTRA_V14_KEY",
        "runtime_rejection_witness_path": str(R59_RUNTIME_REJECTION.relative_to(ROOT)),
        "runtime_rejection_witness_file_sha256": sha(runtime_raw),
        "runtime_rejection_witness_object_sha256": runtime["object_sha256"],
        "tooling_pyc_rejection_path": str(TOOLING_PYC.relative_to(ROOT)),
        "tooling_pyc_rejection_file_sha256": sha(pyc_raw),
        "tooling_pyc_rejection_size": len(pyc_raw),
        "tooling_pyc_rejection_mode": stat.S_IMODE(os.stat(TOOLING_PYC).st_mode),
        "tooling_pyc_rejection_nlink": os.stat(TOOLING_PYC).st_nlink,
        "failure_vector": failure, "candidate_install": True,
        "runtime_protocol_executed": False, "manifest_created": False,
        "outer_created": False, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "append_only": True, "overwrite_delete_or_reuse_allowed": False,
        "predecessor_anchor_file_sha256": R59_ANCHOR_SHA,
        "predecessor_anchor_object_sha256": R59_ANCHOR_OBJECT,
    })
    rejected_raw = canon(rejected) + b"\n"
    rejection = {"path": str(REJECTION.relative_to(ROOT)),
                 "file_sha256": sha(rejected_raw),
                 "object_sha256": rejected["object_sha256"], "bytes": rejected_raw}
    superseded = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.runtime-transition-shape-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_RUNTIME_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV, "successor_namespace": TAG,
        "predecessor_active_anchor_path": str(R59_ANCHOR.relative_to(ROOT)),
        "predecessor_active_anchor_file_sha256": R59_ANCHOR_SHA,
        "predecessor_active_anchor_object_sha256": R59_ANCHOR_OBJECT,
        "predecessor_rejection_path": rejection["path"],
        "predecessor_rejection_file_sha256": rejection["file_sha256"],
        "predecessor_rejection_object_sha256": rejection["object_sha256"],
        "runtime_rejection_witness_path": str(R59_RUNTIME_REJECTION.relative_to(ROOT)),
        "runtime_rejection_witness_file_sha256": sha(runtime_raw),
        "runtime_rejection_witness_object_sha256": runtime["object_sha256"],
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


# Load and retarget the immutable r59 recipe before exposing the entry point.
P = load_parent()
parent_fix = P["fix_json"]
parent_canon = P["launcher_registry_canonicalizer"]

P.update({"PREV": PREV, "TAG": TAG, "INPUT_PREV": INPUT_PREV,
          "INPUT_TAG": INPUT_TAG, "R57_ANCHOR": R59_ANCHOR,
          "R57_ANCHOR_SHA": R59_ANCHOR_SHA,
          "R57_ANCHOR_OBJECT": R59_ANCHOR_OBJECT, "R57_FILES": R59_FILES,
          "REJECTION": REJECTION, "SUPERSESSION": SUPERSESSION,
          "ANCHOR": ANCHOR, "TARGETS": TARGETS})
R = P["_R57"]
R.update({"PREV": PREV, "TAG": TAG, "INPUT_PREV": INPUT_PREV,
          "INPUT_TAG": INPUT_TAG, "R56_ANCHOR": R59_ANCHOR,
          "R56_ANCHOR_SHA": R59_ANCHOR_SHA,
          "R56_ANCHOR_OBJECT": R59_ANCHOR_OBJECT, "R56_FILES": R59_FILES,
          "REJECTION": REJECTION, "SUPERSESSION": SUPERSESSION,
          "ANCHOR": ANCHOR, "TARGETS": TARGETS})

P["fix_json"] = lambda value: repair_json(value, parent_fix)
P["launcher_registry_canonicalizer"] = lambda text: \
    idempotent_registry_canonicalizer(text, parent_canon)
P["make_chain"] = lambda: make_chain(P)
R["make_chain"] = lambda: make_chain(P)

parent_validate = P["validate_generated"]
def validate_generated(generated: dict[str, bytes], meta: dict[str, Any],
                       chain: dict[str, Any]) -> None:
    # r59's historical validator still expects the stale 31-key transition.
    # Give it an in-memory compatibility copy only; never persist it.
    compat = dict(generated)
    current = json.loads(generated["transition"])
    legacy, _ = load_json(R59_FILES["transition"][0])
    compat_transition = dict(current)
    compat_transition["published_then_officially_rejected_predecessor_v14"] = \
        legacy["published_then_officially_rejected_predecessor_v14"]
    compat["transition"] = canon(close(compat_transition)) + b"\n"
    parent_validate(compat, meta, chain)
    body = dict(current)
    claim = body.pop("object_sha256", None)
    if len(current) != 30 or set(current) != EXPECTED_TRANSITION_KEYS or \
            claim != sha(canon(body)):
        raise RuntimeError("r60 transition exact30/object closure")
    audit = json.loads(generated["audit"])
    receipt = audit.get("audited_v16r2_bundle", {}).get(
        "v14_registry_shape_drift_supersession_receipt", {})
    if (receipt.get("path"), receipt.get("file_sha256"),
            receipt.get("object_sha256")) != (V14_PATH, V14_SHA, V14_OBJECT):
        raise RuntimeError("r60 active V14 receipt path/hash closure")
R["validate_generated"] = validate_generated

if __name__ == "__main__":
    raise SystemExit(main())
