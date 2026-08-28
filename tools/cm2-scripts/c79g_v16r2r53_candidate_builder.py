#!/usr/bin/env python3
"""r53 append-only clean-room successor driver.

This driver loads the reviewed r52 constructor only as an immutable in-memory
witness, retags the r52 bundle to r53, and lets the corrected r51 audit builder
emit the native ordered exact43 input map and V16R2 normalizer label.  It never
modifies r52 (or any earlier member) and performs one O_EXCL installation only
after all in-memory gates pass.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
PREV = "v16r2r52"
TAG = "v16r2r53"

R52_WRAPPER = ROOT / "scripts/c79g_v16r2r52_candidate_builder.py"
R52_WRAPPER_SHA = "5a684de6179f987f08f8af4ca84a3cf511c3f66c3b884e04701429c2f81f2ca3"
R52_WRAPPER_SIZE = 13530
PARENT = ROOT / "scripts/c79g_v16r2r51_candidate_builder.py"
PARENT_SHA = "861f64ae670fa0d75fcaacffd5538ce6ecd323f67543535e0799d03cd2950cf5"
PARENT_SIZE = 65180

R52_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R52_ANCHOR_SHA = "81fb3995bcf98b4a96dc1f71969700dfe743a6e9c42eb59e6c6fc4a6d5616559"
R52_ANCHOR_OBJECT = "e88744a79dd91f4e68bc133e23e3b2261d468bc21ce7c15890e1faaaf31c84dd"

R52_FILES: dict[str, tuple[Path, str, str | None]] = {
    "schema": (OUT / f"{BASE}_schema_{PREV}.json",
               "609b9268686271eb5cbe7d3859f57846db52a636da98ebe463afb2c7018ed140", None),
    "contract": (OUT / f"{BASE}_contract_{PREV}.json",
                 "c75fe2846af759ddc58929f3633d1d2c6f1e07f1c3abf6882da054b70f91b505",
                 "3fe2680b73a7af74091997f8dfd7982046e2ec372753b2eded9e14ae88429d6a"),
    "producer": (OUT / f"{BASE}_{PREV}_semantic_source.py",
                 "c7b3108b4692ba695c1a1a4c9b1e2224ad6c42684399242359e88e6b82251989", None),
    "consumer": (OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
                 "bbd08696ea7f9eee66456b703b05e1529bdf71f1f04fb800a66c087021020da1", None),
    "transition": (OUT / f"{BASE}_v16r2r51_to_{PREV}_static_launch_transition_receipt_v1.json",
                   "26959762048d9ada0be8558841d622e7a8c363c6eed1a6cbbb94d9a8ac69b741",
                   "7515311e3ad8f8a0072fd453141dce31a54ee544d3bacd2742322051ae95fe2e"),
    "audit": (OUT / f"{BASE}_static_audit_{PREV}.json",
              "52ff60ce514230ed87de6a61233cf8eeceae38bad372a518aff3cea4567dd000",
              "9e3dbcd141c62d7c1bc9271beacc2630de55467a00cfaa6e4e594b5712d1c50c"),
    "launcher": (OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
                 "dc8ee8a77dbcfb5cd24e8729dd283666f3949825b23dfedae9b91e93f3485d22", None),
}

R53_REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
R53_SUP = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
R53_ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
R53_TARGETS = [
    R53_REJECTION, R53_SUP, R53_ANCHOR,
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    OUT / f"{BASE}_schema_{TAG}.json", OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{TAG}.json",
    OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
    OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
]


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"unstable witness:{path}")
        chunks: list[bytes] = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        named = os.lstat(path)
        raw = b"".join(chunks)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"witness changed:{path}")
        return raw
    finally:
        os.close(fd)


def replace_hex(text: str, name: str, value: str) -> str:
    pattern = rf"(?m)^({re.escape(name)}\s*=\s*)(['\"])[0-9a-f]{{64}}\2\s*$"
    text, count = re.subn(pattern, rf'\1"{value}"', text)
    if count != 1:
        raise RuntimeError(f"r53 pin assignment {name}:{count}")
    return text


def load_wrapper_namespace() -> dict[str, Any]:
    raw = stable(R52_WRAPPER)
    if len(raw) != R52_WRAPPER_SIZE or hashlib.sha256(raw).hexdigest() != R52_WRAPPER_SHA:
        raise RuntimeError("r52 wrapper witness drift")
    tree = ast.parse(raw.decode(), str(R52_WRAPPER), mode="exec")
    compile(tree, str(R52_WRAPPER), "exec")
    w: dict[str, Any] = {"__name__": "_r52_wrapper_for_r53",
                         "__file__": str(R52_WRAPPER), "__package__": None}
    exec(compile(tree, str(R52_WRAPPER), "exec"), w, w)
    # Rebind the wrapper's module globals before asking it to load the pinned
    # r51 constructor.  Its loader is otherwise reused unchanged in memory.
    w.update({"ROOT": ROOT, "OUT": OUT, "BASE": BASE, "PREV": PREV, "TAG": TAG,
              "PARENT": PARENT, "PARENT_SHA": PARENT_SHA, "PARENT_SIZE": PARENT_SIZE,
              "R50_ANCHOR": R52_ANCHOR, "R50_ANCHOR_SHA": R52_ANCHOR_SHA,
              "R50_ANCHOR_OBJECT": R52_ANCHOR_OBJECT, "R50_FILES": R52_FILES,
              "R51_REJECTION": R53_REJECTION, "R52_SUP": R53_SUP,
              "R52_ANCHOR": R53_ANCHOR})
    return w


def configure_parent(w: dict[str, Any]) -> dict[str, Any]:
    ns = w["_load_parent"]()
    ns.update({"ROOT": ROOT, "OUT": OUT, "BASE": BASE, "PREV": PREV, "TAG": TAG,
               "R50_BUILDER": R52_WRAPPER, "R50_BUILDER_SHA": R52_WRAPPER_SHA,
               "R50_BUILDER_SIZE": R52_WRAPPER_SIZE,
               "R50_ANCHOR": R52_ANCHOR, "R50_ANCHOR_SHA": R52_ANCHOR_SHA,
               "R50_ANCHOR_OBJECT": R52_ANCHOR_OBJECT, "R50_FILES": R52_FILES,
               "R50_REJECTION": R53_REJECTION, "R51_REJECTION": R53_REJECTION,
               "R51_SUP": R53_SUP, "R51_ANCHOR": R53_ANCHOR,
               "R51_TARGETS": R53_TARGETS,
               "_replace_hex_assignment": replace_hex})

    def direct_patch(raw_bytes: bytes, role: str, paths: dict[str, str],
                     af: str, ao: str, sh: str, ch: str, co: str,
                     producer_hash: str | None,
                     base7: dict[str, tuple[str, str | None]] | None) -> bytes:
        text = raw_bytes.decode("utf-8")
        old_edge = f"{BASE}_v16r2r51_to_v16r2r52_"
        text = text.replace(old_edge, "__R53_EDGE__")
        text = text.replace("v16r2r52", TAG).replace("V16R2R52", "V16R2R53")
        text = text.replace("__R53_EDGE__", f"{BASE}_{PREV}_to_{TAG}_")
        text = replace_hex(text, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", af)
        text = replace_hex(text, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", ao)
        if role != "launcher":
            text = replace_hex(text, "CONTRACT_FILE_PIN", ch)
            text = replace_hex(text, "CONTRACT_OBJECT_PIN", co)
            text = replace_hex(text, "CLOSED_SCHEMA_FILE_PIN", sh)
            if role == "consumer" and producer_hash is not None:
                text = replace_hex(text, "PRODUCER_SOURCE_PIN", producer_hash)
        else:
            if base7 is None:
                raise RuntimeError("r53 launcher base7 missing")
            tree = ast.parse(text, "r53_launcher", mode="exec")
            funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and
                     n.name == "configure_workspace_paths"]
            if len(funcs) != 1:
                raise RuntimeError("r53 launcher configure function")
            assigns = [n for n in funcs[0].body if isinstance(n, ast.Assign) and
                       len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and
                       n.targets[0].id == "BASE7_PINS"]
            if len(assigns) != 1:
                raise RuntimeError("r53 launcher BASE7 assignment")
            pins = dict(base7)
            pins.setdefault("v14", (ns["V14_SHA"], ns["V14_OBJECT"]))
            order = [("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT", "v14"),
                     ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                     ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                     ("TRANSITION", "transition"), ("AUDIT", "audit")]
            assigns[0].value = ast.Dict(
                keys=[ast.Name(id=name, ctx=ast.Load()) for name, _ in order],
                values=[ast.Tuple([ast.Constant(pins[key][0]),
                                   ast.Constant(pins[key][1])], ast.Load())
                        for _, key in order])
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and \
                        isinstance(node.targets[0], ast.Name) and \
                        node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED":
                    node.value = ast.Constant(True)
            text = ast.unparse(tree) + "\n"
        edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
        if edge not in text:
            raise RuntimeError(f"{role}: r53 edge absent")
        return text.encode()

    ns["_direct_source_patch_r50"] = direct_patch
    old_canon = ns["_canonicalize_registry_helper"]
    def canonicalize(text: str) -> str:
        try:
            return old_canon(text)
        except RuntimeError as exc:
            if "literal" in str(exc) or "patch incomplete" in str(exc):
                return text
            raise
    ns["_canonicalize_registry_helper"] = canonicalize
    old_cross = ns["_patch_launcher_validator_cross_role"]
    def cross(text: str) -> str:
        if ("consumer_frozen_predecessor_incident_exact5_bytes_read_only_noncredit_allowed"
                not in text and
                "pin_normalization_preserves_v12_rejection_and_all_historical_pins"
                not in text and "actual_runtime_registry_shape_evidence" in text and
                "published_then_officially_rejected_predecessor_v14" in text):
            return text
        return old_cross(text)
    ns["_patch_launcher_validator_cross_role"] = cross

    def reject_previous(builder: Any) -> dict[str, str]:
        value = ns["_close"]({
            "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
            "status": "PERMANENT_FAIL_CLOSED_R52_AUDIT_ORDER_AND_NORMALIZER_LABEL__ZERO_CREDIT",
            "failed_namespace": PREV, "predecessor_namespace": "v16r2r51",
            "rejection_reason": "STATIC_AUDIT_INPUT_ORDER_AND_V16R2_NORMALIZER_LABEL_DRIFT",
            "failure_vector": {
                "checker_input_sha256_order_was_not_native_exact43": True,
                "pin_normalized_ast_algorithm_used_v15_label": True,
                "required_namespace": PREV, "candidate_bytes_remain_immutable": True,
            },
            "candidate_install": True, "runtime_protocol_executed": False,
            "manifest_created": False, "outer_created": False,
            "runtime_authorized": False, "formal_global_closure_credit": 0,
            "D02_unlock": False, "append_only": True,
            "overwrite_delete_or_reuse_allowed": False,
            "candidate_schema_file_sha256": R52_FILES["schema"][1],
            "candidate_contract_file_sha256": R52_FILES["contract"][1],
            "candidate_contract_object_sha256": R52_FILES["contract"][2],
            "candidate_audit_file_sha256": R52_FILES["audit"][1],
            "candidate_audit_object_sha256": R52_FILES["audit"][2],
        })
        raw = ns["_canon"](value) + b"\n"
        return {"path": str(R53_REJECTION.relative_to(ROOT)),
                "file_sha256": hashlib.sha256(raw).hexdigest(),
                "object_sha256": value["object_sha256"], "bytes": raw}
    ns["seal_r50_rejection"] = reject_previous
    return ns


def main() -> int:
    try:
        w = load_wrapper_namespace()
        ns = configure_parent(w)
        print(json.dumps(ns["install_r51_candidate"](), ensure_ascii=False,
                         sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
                          "status": "FAIL_CLOSED_R53_STATIC_INSTALL",
                          "error": {"type": type(exc).__name__,
                                    "message": str(exc)},
                          "candidate_install": False, "manifest_created": False,
                          "outer_created": False, "runtime_authorized": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False}, ensure_ascii=False,
                  sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
