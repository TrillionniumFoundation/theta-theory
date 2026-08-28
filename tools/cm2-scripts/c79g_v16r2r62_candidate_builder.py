#!/usr/bin/env python3
"""Clean-room r62 static candidate builder.

The installed r61 bundle and the three r61→r62 tooling-pyc chain receipts are
immutable inputs.  The r61 builder is loaded as an AST-only recipe and its
namespace is retargeted in memory to r62.  This program's default action is a
read-only preflight; ``install`` is explicit and writes only the seven new
static members (the three chain receipts are already sealed by their own
append-only sealer).
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
PREV = "v16r2r61"
TAG = "v16r2r62"
INPUT_PREV = "v16r2r60"
INPUT_TAG = "v16r2r61"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

PARENT = ROOT / "scripts/c79g_v16r2r61_candidate_builder.py"
PARENT_SHA = "89f27fd44388ee1e245327ef5cc44bbc3e5929d01a791509b6e61a9a87f2ac27"
PARENT_SIZE = 26528

V14_PATH = (
    f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json")
V14_SHA = "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"
V14_OBJECT = "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"

R61_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R61_ANCHOR_SHA = "a6e7ebe51eed1a877f0440d2bf90827e17ca955912d449a4eaca6fc17f383838"
R61_ANCHOR_OBJECT = "fc63955e5c40352413245ca0e8a2a4a098a4b3f596f534838a9442190dd98be2"

R61_FILES: dict[str, tuple[Path, str, str | None]] = {
    "schema": (OUT / f"{BASE}_schema_{PREV}.json",
               "fdccae1a4d2c59d712b6ca4c7924a0eac06b285c40da9b76449f9e2c6ea4498a", None),
    "contract": (OUT / f"{BASE}_contract_{PREV}.json",
                 "25c8b839f2919e7d41cc4735da5d3161f1bbe74320712396839be103d6979cb4",
                 "7b7ee6a90c1d0248178c6d774186a6bdcbdf506e4f83faff8598f61c9ccd6eb2"),
    "producer": (OUT / f"{BASE}_{PREV}_semantic_source.py",
                 "2cc329b416ddd903c0b9e3e8552f18a4f35039086445e5da76973e18798791d4", None),
    "consumer": (OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
                 "723fe15b9c28d776c9f3a9aaa77449a10e4f09323aaf23ec731ef062266161f0", None),
    # The immutable predecessor transition is r60→r61 (INPUT_PREV→PREV).
    "transition": (OUT / f"{BASE}_{INPUT_PREV}_to_{PREV}_static_launch_transition_receipt_v1.json",
                   "9fd292d9fb88917a63afbec02c5e95436655f6a9d5ec268cfb7f4bf7c80e8851",
                   "1d0d830e04bf768273c6bc6890cc65f638e926464e5dd0313be2f863cb3866cd"),
    "audit": (OUT / f"{BASE}_static_audit_{PREV}.json",
              "f8f2a40fdd55a8a71fd83666c2b165b23e8ecb85382a662898e34d60c0b675b2",
              "f2c07d5213d73f9b3e8e5caddf8454817be83d8ac8d463015b495aee030c1c8b"),
    "launcher": (OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
                 "54c62c7a969cc6d2af11776ab24cabeafb7c9463c3226ca47c3d4dfa5fb27fc5", None),
}

R61_HELPER_RECEIPT = OUT / f"{BASE}_{PREV}_launcher_registry_helper_version_neutral_review_receipt_v1.json"
R61_HELPER_RECEIPT_SHA = "4442057b6e3b67839dd0686e0fa1b108ba08350b68b02a206da738cdd88e3498"
R61_HELPER_RECEIPT_OBJECT = "8e73a17685940781d974e9df582e0016b6b7b5aa31418cce8b572285b3127350"

# The no-producer attempt was stopped before child spawn because this pyc was
# already present.  It is historical evidence, never an executable input.
R60_PYC = ROOT / "scripts/__pycache__/c79g_v16r2r60_candidate_builder.cpython-312.pyc"
R60_PYC_SHA = "21349b99e545c96b6521578ecbd66e0e06afb16d2fb2f3cafa1d5f149be0e4d7"
R60_PYC_SIZE = 20453
R61_PYC = ROOT / "scripts/__pycache__/c79g_v16r2r61_no_producer_evidence_sealer.cpython-312.pyc"
R61_PYC_SHA = "a25be0dadafa36751eff506d169f670776fb91f42ab4118596e5511a88a135a7"
R61_PYC_SIZE = 21748
R61_PYC_ALLOWLIST = {
    str(R60_PYC.relative_to(ROOT)): (R60_PYC_SHA, R60_PYC_SIZE),
    str(R61_PYC.relative_to(ROOT)): (R61_PYC_SHA, R61_PYC_SIZE),
}

C53_PATH = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_OBJECT = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"

# These three objects are sealed inputs, not r62 builder outputs.
CHAIN = {
    "rejection": (OUT / f"{BASE}_{PREV}_no_producer_tooling_pyc_rejection_receipt_v1.json",
                   "061e0fb3be64987f4b7c6c275a399b077e07660485e1e88c4f19f802fcb023a5",
                   "1b110cf25de1669612464dbe1d8528a2d5e4a541a87edc11c92627e4d769be4d"),
    "supersession": (OUT / f"{BASE}_{PREV}_to_{TAG}_no_producer_tooling_pyc_rejection_supersession_receipt_v1.json",
                     "8deec2d601f1e552a75af8f2d3e7248358c59e656c10852424ecd32631262132",
                     "64b52e09bb18e69dc2da9c64e22913786d5789c1cdfc1e67e3ade4307477d426"),
    "anchor": (OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
               "bf90b37c218c18d974793498816f6165807685e3f8e806bbf034468a7af66194",
               "0262a45dfb6812eaae673955934f6eb0ca5d6ace92f75b428f1cde33e777c9c6"),
}

STATIC_TARGETS = [
    OUT / f"{BASE}_schema_{TAG}.json",
    OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{TAG}.json",
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
]
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
TARGETS = STATIC_TARGETS + [MANIFEST, OUTER]

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
        before = os.fstat(fd); named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable witness:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        raw = b"".join(chunks); after = os.fstat(fd); named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(raw) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        if expected is not None and sha(raw) != expected:
            raise RuntimeError(f"witness hash:{path}")
        if expected_size is not None and len(raw) != expected_size:
            raise RuntimeError(f"witness size:{path}")
        return raw
    finally:
        os.close(fd)


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value); body.pop("object_sha256", None)
    body["object_sha256"] = sha(canon(body))
    return body


def load_json(path: Path, expected_file: str | None = None,
              expected_object: str | None = None) -> tuple[dict[str, Any], bytes]:
    raw = stable(path, expected_file)
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"json object required:{path}")
    body = dict(value); claim = body.pop("object_sha256", None)
    if claim is not None and sha(canon(body)) != claim:
        raise RuntimeError(f"json object closure:{path}")
    if expected_object is not None and claim != expected_object:
        raise RuntimeError(f"json object pin:{path}")
    return value, raw


def pyc_inventory() -> dict[str, str]:
    return {str(p.relative_to(ROOT)): sha(p.read_bytes())
            for p in ROOT.rglob("*.pyc") if p.is_file() and not p.is_symlink()}


def assert_pyc_policy() -> dict[str, Any]:
    witnesses: dict[str, dict[str, Any]] = {}
    for rel, (digest, size) in R61_PYC_ALLOWLIST.items():
        path = ROOT / rel
        raw = stable(path, digest, size)
        st = path.stat()
        if st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != 0o664:
            raise RuntimeError(f"tooling pyc identity:{path}")
        witnesses[rel] = {"file_sha256": sha(raw), "size": len(raw),
                          "mode": stat.S_IMODE(st.st_mode), "nlink": st.st_nlink}
    unexpected = []
    for path in ROOT.rglob("*.pyc"):
        if not path.is_file() or path.is_symlink():
            continue
        rel = str(path.relative_to(ROOT))
        if ("v16r2r61" in rel or "v16r2r62" in rel) and rel not in R61_PYC_ALLOWLIST:
            unexpected.append(rel)
    if unexpected:
        raise RuntimeError("unexpected r61/r62 tooling pyc:" + ",".join(sorted(unexpected)))
    return {"allowlist": witnesses, "unexpected_tagged_pyc": []}


def load_parent() -> dict[str, Any]:
    raw = stable(PARENT, PARENT_SHA, PARENT_SIZE)
    tree = ast.parse(raw.decode("utf-8"), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    ns: dict[str, Any] = {"__name__": "_r61_recipe_for_r62",
                          "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), ns, ns)
    if not isinstance(ns.get("P"), dict) or not isinstance(ns.get("R"), dict):
        raise RuntimeError("r61 recipe namespace missing")
    return ns


def chain_inputs() -> dict[str, Any]:
    anchor, anchor_raw = load_json(R61_ANCHOR, R61_ANCHOR_SHA, R61_ANCHOR_OBJECT)
    if (anchor.get("predecessor_namespace") != "v16r2r60" or
            anchor.get("successor_namespace") != f"{PREV}_semantic_source" or
            anchor.get("formal_global_closure_credit") != 0 or
            anchor.get("D02_unlock") is not False or
            anchor.get("runtime_authorized") is not False):
        raise RuntimeError("r61 anchor semantics")
    # Physical identity is part of the immutable predecessor contract.  JSON
    # receipts must be sealed 0444 and executable source witnesses remain
    # 0664 until the later cold-freeze publisher changes them to 0444.
    for role, (path, _file_hash, _object_hash) in R61_FILES.items():
        st = path.stat()
        expected_mode = 0o444 if path.suffix == ".json" else 0o664
        if st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != expected_mode:
            raise RuntimeError(
                f"r61 predecessor physical identity:{role}:"
                f"mode={stat.S_IMODE(st.st_mode):04o},nlink={st.st_nlink}")
    helper, helper_raw = load_json(R61_HELPER_RECEIPT, R61_HELPER_RECEIPT_SHA,
                                   R61_HELPER_RECEIPT_OBJECT)
    if helper.get("status") != "PASS_R61_DUAL_INDEPENDENT_VERSION_NEUTRAL_HELPER_REVIEW__ZERO_CREDIT":
        raise RuntimeError("r61 helper receipt status")
    chain_values: dict[str, dict[str, Any]] = {}
    chain_raws: dict[str, bytes] = {}
    for role, (path, file_hash, object_hash) in CHAIN.items():
        value, raw = load_json(path, file_hash, object_hash)
        if stat.S_IMODE(path.stat().st_mode) != 0o444 or path.stat().st_nlink != 1:
            raise RuntimeError(f"chain identity:{path}")
        chain_values[role] = value; chain_raws[role] = raw
    if chain_values["rejection"].get("tooling_pyc_rejection_file_sha256") != R61_PYC_SHA:
        raise RuntimeError("r61 rejection pyc pin")
    if chain_values["supersession"].get("successor_namespace") != TAG:
        raise RuntimeError("r61->r62 supersession successor")
    if chain_values["anchor"].get("predecessor_namespace") != PREV or \
       chain_values["anchor"].get("successor_namespace") != f"{TAG}_semantic_source":
        raise RuntimeError("r62 anchor semantics")
    c53_raw = stable(C53_PATH, C53_SHA)
    c53 = json.loads(c53_raw.decode("utf-8"))
    if c53.get("authority_seal_object_sha256") != C53_OBJECT:
        raise RuntimeError("C53 object drift")
    return {
        "rejection": {"value": chain_values["rejection"], "raw": chain_raws["rejection"]},
        "supersession": {"value": chain_values["supersession"], "raw": chain_raws["supersession"]},
        "anchor": {"value": chain_values["anchor"], "raw": chain_raws["anchor"]},
        "anchor_file_sha256": sha(chain_raws["anchor"]),
        "anchor_object_sha256": chain_values["anchor"]["object_sha256"],
        "anchor_path": str(CHAIN["anchor"][0].relative_to(ROOT)),
        "rejection_file_sha256": sha(chain_raws["rejection"]),
        "supersession_file_sha256": sha(chain_raws["supersession"]),
        "r61_anchor_file_sha256": R61_ANCHOR_SHA,
        "r61_anchor_object_sha256": R61_ANCHOR_OBJECT,
        "r61_helper_receipt_file_sha256": sha(helper_raw),
        "r61_helper_receipt_object_sha256": helper["object_sha256"],
        "C53_file_sha256": sha(c53_raw), "C53_object_sha256": C53_OBJECT,
    }


def repair_json(value: Any, parent_fix: Any) -> Any:
    out = parent_fix(value)
    if not isinstance(out, dict):
        return out
    if "static-launch-transition" in str(out.get("schema", "")):
        out.pop("published_then_officially_rejected_predecessor_v14", None)
        if set(out) != EXPECTED_TRANSITION_KEYS or dict.__len__(out) != 30:
            raise RuntimeError("r62 transition exact30 normalization")
    if "static-audit" in str(out.get("schema", "")):
        receipt = out.get("audited_v16r2_bundle", {}).get(
            "v14_registry_shape_drift_supersession_receipt")
        if not isinstance(receipt, dict):
            raise RuntimeError("r62 active V14 receipt field missing")
        receipt.update({"path": V14_PATH, "file_sha256": V14_SHA,
                        "object_sha256": V14_OBJECT})
    return out


def build_chain_for_recipe(chain: dict[str, Any]) -> dict[str, Any]:
    # The historical recipe expects these keys even though r62 treats the
    # chain as already sealed input.  Supplying the exact bytes keeps its
    # generated metadata honest without permitting another chain write.
    return {
        "rejection": {"path": str(CHAIN["rejection"][0].relative_to(ROOT)),
                      "file_sha256": chain["rejection_file_sha256"],
                      "object_sha256": chain["rejection"]["value"]["object_sha256"],
                      "bytes": chain["rejection"]["raw"]},
        "sup_value": chain["supersession"]["value"],
        "sup_raw": chain["supersession"]["raw"],
        "anchor_value": chain["anchor"]["value"],
        "anchor_raw": chain["anchor"]["raw"],
        "sup_file_sha256": chain["supersession_file_sha256"],
        "rejection_file_sha256": chain["rejection_file_sha256"],
        "supersession_file_sha256": chain["supersession_file_sha256"],
        "anchor_file_sha256": chain["anchor_file_sha256"],
        "anchor_object_sha256": chain["anchor_object_sha256"],
        "anchor_path": chain["anchor_path"],
    }


def configure_recipe() -> dict[str, Any]:
    global P, R, parent_fix, old_validate
    P = N["P"]; R = N["R"]
    parent_fix = P["fix_json"]
    old_validate = R["validate_generated"]
    retag = {"BASE": BASE, "PREV": PREV, "TAG": TAG,
             "INPUT_PREV": INPUT_PREV, "INPUT_TAG": INPUT_TAG,
             "SUCCESSOR": SUCCESSOR, "UPSTREAM": UPSTREAM,
             "R57_ANCHOR": R61_ANCHOR, "R57_ANCHOR_SHA": R61_ANCHOR_SHA,
             "R57_ANCHOR_OBJECT": R61_ANCHOR_OBJECT, "R57_FILES": R61_FILES,
             "R56_ANCHOR": R61_ANCHOR, "R56_ANCHOR_SHA": R61_ANCHOR_SHA,
             "R56_ANCHOR_OBJECT": R61_ANCHOR_OBJECT, "R56_FILES": R61_FILES,
             "REJECTION": CHAIN["rejection"][0],
             "SUPERSESSION": CHAIN["supersession"][0],
             "ANCHOR": CHAIN["anchor"][0], "TARGETS": TARGETS}
    for d in (P, R):
        d.update(retag)
    # The underlying constructor's occupancy check must ignore the three
    # already-sealed chain inputs; only fresh r62 static targets are writable.
    P["TARGETS"] = list(TARGETS); R["TARGETS"] = list(TARGETS)
    N.update(retag)
    # Keep the loaded r61 ``P["fix_json"]`` closure, but point its recipe
    # namespace at this wrapper's repair function.  A lambda here would
    # recurse through the same global name with two arguments.
    N["repair_json"] = repair_json
    # r61's top-level builder asks R for its chain and validator.
    R["make_chain"] = lambda: build_chain_for_recipe(chain_inputs())
    P["make_chain"] = R["make_chain"]
    # Replace the loaded r61 validator with this wrapper's r62 validator;
    # otherwise the recipe would silently validate against its predecessor's
    # namespace and skip the r62 contract/transition assertions.
    R["validate_generated"] = validate_generated
    P["validate_generated"] = validate_generated
    return P


def build_in_memory() -> tuple[dict[str, Any], dict[str, bytes], dict[str, Any], dict[str, Any]]:
    chain = chain_inputs()
    preflight, generated, meta, recipe_chain = R["build_in_memory"]()
    preflight = dict(preflight)
    for old, new in (("r56_anchor_file_sha256", "r61_anchor_file_sha256"),
                     ("r56_anchor_object_sha256", "r61_anchor_object_sha256"),
                     ("r60_anchor_file_sha256", "r61_anchor_file_sha256"),
                     ("r60_anchor_object_sha256", "r61_anchor_object_sha256")):
        if old in preflight:
            preflight[new] = preflight.pop(old)
    meta = dict(meta); shapes = dict(meta.get("shapes", {}))
    shapes["transition"] = len(json.loads(generated["transition"]))
    meta["shapes"] = shapes
    meta["persisted_transition_top_level_key_count"] = 30
    meta["in_memory_compat_transition_key_count"] = 31
    meta["compat_transition_persisted"] = False
    meta["chain_inputs"] = {"rejection_file_sha256": chain["rejection_file_sha256"],
                             "supersession_file_sha256": chain["supersession_file_sha256"],
                             "anchor_file_sha256": chain["anchor_file_sha256"],
                             "anchor_object_sha256": chain["anchor_object_sha256"]}
    return preflight, generated, meta, chain


def validate_generated(generated: dict[str, bytes], meta: dict[str, Any],
                       chain: dict[str, Any]) -> None:
    # ``R["build_in_memory"]`` hands back the recipe-shaped chain directly;
    # do not reinterpret its already-materialized rejection entry as the
    # richer preflight ``chain_inputs`` mapping.
    old_validate(generated, meta, chain)
    transition = json.loads(generated["transition"])
    body = dict(transition); claim = body.pop("object_sha256", None)
    if len(transition) != 30 or set(transition) != EXPECTED_TRANSITION_KEYS or \
            claim != sha(canon(body)):
        raise RuntimeError("r62 transition exact30/object closure")
    audit = json.loads(generated["audit"])
    receipt = audit.get("audited_v16r2_bundle", {}).get(
        "v14_registry_shape_drift_supersession_receipt", {})
    if (receipt.get("path"), receipt.get("file_sha256"),
            receipt.get("object_sha256")) != (V14_PATH, V14_SHA, V14_OBJECT):
        raise RuntimeError("r62 active V14 receipt path/hash closure")
    contract = json.loads(generated["contract"])
    if contract.get("v16r2_bundle", {}).get("bundle_version") != TAG:
        raise RuntimeError("r62 contract bundle version")


def preflight() -> dict[str, Any]:
    before = pyc_inventory()
    pre, generated, meta, chain = build_in_memory()
    if pyc_inventory() != before:
        raise RuntimeError("r62 pyc inventory changed during preflight")
    pyc = assert_pyc_policy()
    return {"schema": f"cm2.c79g.{TAG}.candidate-builder.preflight.v1",
            "status": "R62_STATIC_PREFLIGHT_PASS__ZERO_CREDIT__INSTALL_NOT_PERFORMED",
            "preflight": pre, "generated_file_sha256": {k: sha(v) for k, v in generated.items()},
            "meta": meta,
            "chain_inputs": {"rejection_file_sha256": chain["rejection_file_sha256"],
                             "supersession_file_sha256": chain["supersession_file_sha256"],
                             "anchor_file_sha256": chain["anchor_file_sha256"],
                             "anchor_object_sha256": chain["anchor_object_sha256"]},
            "pyc_policy": pyc, "candidate_install": False,
            "manifest_created": False, "outer_created": False,
            "runtime_authorized": False, "formal_global_closure_credit": 0,
            "D02_unlock": False, "pyc_created": False}


def install() -> dict[str, Any]:
    pre, generated, meta, chain = build_in_memory()
    before = pyc_inventory(); _, _, builder = N["configure"]()
    paths = {
        "schema": STATIC_TARGETS[0], "contract": STATIC_TARGETS[1],
        "transition": STATIC_TARGETS[2], "audit": STATIC_TARGETS[3],
        "producer": STATIC_TARGETS[4], "consumer": STATIC_TARGETS[5],
        "launcher": STATIC_TARGETS[6],
    }
    actions: dict[str, str] = {}
    for key in ("schema", "contract", "transition", "audit"):
        actions[key] = builder.install(paths[key], generated[key], 0o444)
    for key in ("producer", "consumer", "launcher"):
        actions[key] = builder.install(paths[key], generated[key], 0o664)
    if pyc_inventory() != before:
        raise RuntimeError("r62 pyc inventory changed during installation")
    assert_pyc_policy()
    return {"schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
            "status": "R62_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "preflight": pre, "actions": actions, "meta": meta,
            "chain_inputs": {"rejection_file_sha256": chain["rejection_file_sha256"],
                             "supersession_file_sha256": chain["supersession_file_sha256"],
                             "anchor_file_sha256": chain["anchor_file_sha256"],
                             "anchor_object_sha256": chain["anchor_object_sha256"]},
            "candidate_install": True, "manifest_created": False,
            "outer_created": False, "runtime_authorized": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "pyc_created": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("action", nargs="?",
        choices=("preflight", "install"), default="preflight")
    args = parser.parse_args(argv)
    try:
        result = preflight() if args.action == "preflight" else install()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
                          "status": "FAIL_CLOSED_R62_PREFLIGHT" if args.action == "preflight" else "FAIL_CLOSED_R62_STATIC_INSTALL",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "candidate_install": False, "manifest_created": False,
                          "outer_created": False, "runtime_authorized": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False},
                         ensure_ascii=False, sort_keys=True))
        return 1


N = load_parent()
configure_recipe()

if __name__ == "__main__":
    raise SystemExit(main())
