#!/usr/bin/env python3
"""r52 append-only successor driver.

The r51 candidate is retained as an immutable rejection witness after an
independent consumer check found stale active-bundle source paths.  This thin
driver reuses the pinned r51 constructor in memory, supplies a generalized
r51->r52 retagger, and performs the same no-pyc/O_EXCL gates in a fresh
namespace.  It never edits r51 or any earlier deliverable.
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
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
PREV = "v16r2r51"
TAG = "v16r2r52"
PARENT = ROOT / "scripts/c79g_v16r2r51_candidate_builder.py"
PARENT_SHA = "90fa64ba8354a1a3bb659615da8509cf21e930eb15a8e762586e5d326ae5ae97"
PARENT_SIZE = 63171
OUT = ROOT / "deliverables"

R50_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R50_ANCHOR_SHA = "3d56690089b7691fed7fbcfe18a639ea603afad2c7dcd3befa1b92e91d459d8e"
R50_ANCHOR_OBJECT = "356e2d17f9a8b8701c6aefc29f11792b1601475594972de2fc6d1a38316b087d"

R50_FILES = {
    "schema": (OUT / f"{BASE}_schema_{PREV}.json",
               "a1fdf6fb9156086ce60aaca72f6fb32db6afc17411ccc07f24da78cf1d15f78c", None),
    "contract": (OUT / f"{BASE}_contract_{PREV}.json",
                 "2aac1e71194edf7e2eb85b2c0cb07a52b17f4dbb72385c0481d625dcc75ab8a7",
                 "72c3addc70cf938a9f122eb3770784c203fcf393ef4330173eef35a12ad76643"),
    "producer": (OUT / f"{BASE}_{PREV}_semantic_source.py",
                 "03f2aed1f28dd446b1ff84356cc6eae2a65003462b46b7183ab3994f41765bd7", None),
    "consumer": (OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
                 "934c982dcb00b28d87b608b26bd11d3b6ed2381faef0ab4320dabbef25dff1c0", None),
    "transition": (OUT / f"{BASE}_v16r2r50_to_{PREV}_static_launch_transition_receipt_v1.json",
                   "ae7e207e44738f754fe755efba14a0a0995ca895de3f9ae9e7918ce852552de1",
                   "4cae80c590d7296a8385ab5cfe001b563e832bcc96bd80a9b63648e55887a48a"),
    "audit": (OUT / f"{BASE}_static_audit_{PREV}.json",
              "e467e73b6a8b023bf8f557e29ea07eb9ce697eb269949677e8fb46a7aee99f00",
              "79b1f0f1b485e644bc6f41bc37f67ec801511df9c049c631ea85aaacd4015100"),
    "launcher": (OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
                 "5952bf657ad96b03da318aa9557bd5ea7a2ebf8b6a24587015e6df0cfc7f26b7", None),
}

R51_REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
R52_SUP = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
R52_ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"


def _stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"unstable parent witness:{path}")
        chunks = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        raw = b"".join(chunks)
        named = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"parent witness changed:{path}")
        return raw
    finally:
        os.close(fd)


def _load_parent() -> dict[str, Any]:
    raw = _stable(PARENT)
    if len(raw) != PARENT_SIZE or hashlib.sha256(raw).hexdigest() != PARENT_SHA:
        raise RuntimeError("r51 constructor witness drift")
    tree = ast.parse(raw.decode(), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    ns: dict[str, Any] = {"__name__": "_r52_parent",
                          "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), ns, ns)
    ns.update({"ROOT": ROOT, "OUT": OUT, "BASE": BASE,
               "PREV": PREV, "TAG": TAG,
               "R50_BUILDER": PARENT, "R50_BUILDER_SHA": PARENT_SHA,
               "R50_BUILDER_SIZE": PARENT_SIZE,
               "R50_ANCHOR": R50_ANCHOR,
               "R50_ANCHOR_SHA": R50_ANCHOR_SHA,
               "R50_ANCHOR_OBJECT": R50_ANCHOR_OBJECT,
               "R50_FILES": R50_FILES,
               "R50_REJECTION": R51_REJECTION,
               "R51_REJECTION": R51_REJECTION,
               "R51_SUP": R52_SUP, "R51_ANCHOR": R52_ANCHOR})
    ns["R51_TARGETS"] = [
        R51_REJECTION, R52_SUP, R52_ANCHOR,
        OUT / f"{BASE}_{TAG}_semantic_source.py",
        OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
        OUT / f"{BASE}_schema_{TAG}.json", OUT / f"{BASE}_contract_{TAG}.json",
        OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        OUT / f"{BASE}_static_audit_{TAG}.json",
        OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
        OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
    ]

    # r51's launcher was serialized through ``ast.unparse`` and therefore
    # carries single-quoted top-level pin assignments.  The older helper only
    # accepted double quotes; keep its exact top-level-only census while
    # accepting either quote style.  Indented runtime rebinding statements
    # remain untouched and are deliberately not part of the static pin edit.
    def replace_hex_assignment(text: str, name: str, value: str) -> str:
        pattern = rf"(?m)^({re.escape(name)}\s*=\s*)(['\"])[0-9a-f]{{64}}\2\s*$"
        text, count = re.subn(pattern, rf'\1"{value}"', text)
        if count != 1:
            raise RuntimeError(f"r52 pin assignment {name}:{count}")
        return text
    ns["_replace_hex_assignment"] = replace_hex_assignment

    # The r51 retagger replaced the predecessor token globally.  For r52 we
    # replace only the old *successor* token, preserving r50 in the edge and
    # historical diagnostic paths.
    def direct_patch(raw_bytes: bytes, role: str, paths: dict[str, str],
                     af: str, ao: str, sh: str, ch: str, co: str,
                     producer_hash: str | None,
                     base7: dict[str, tuple[str, str | None]] | None) -> bytes:
        text = raw_bytes.decode("utf-8")
        old_edge = f"{BASE}_v16r2r50_to_v16r2r51_"
        text = text.replace(old_edge, "__R52_EDGE__")
        text = text.replace("v16r2r51", TAG).replace("V16R2R51", "V16R2R52")
        text = text.replace("__R52_EDGE__", f"{BASE}_{PREV}_to_{TAG}_")
        text = ns["_replace_hex_assignment"](
            text, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", af)
        text = ns["_replace_hex_assignment"](
            text, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", ao)
        if role != "launcher":
            text = ns["_replace_hex_assignment"](text, "CONTRACT_FILE_PIN", ch)
            text = ns["_replace_hex_assignment"](text, "CONTRACT_OBJECT_PIN", co)
            text = ns["_replace_hex_assignment"](text, "CLOSED_SCHEMA_FILE_PIN", sh)
            if role == "consumer" and producer_hash is not None:
                text = ns["_replace_hex_assignment"](text, "PRODUCER_SOURCE_PIN", producer_hash)
        else:
            if base7 is None:
                raise RuntimeError("r52 launcher base7 missing")
            base7 = dict(base7)
            base7.setdefault("v14", (ns["V14_SHA"], ns["V14_OBJECT"]))
            tree = ast.parse(text, "r52_launcher", mode="exec")
            funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and
                     n.name == "configure_workspace_paths"]
            assigns = [n for n in funcs[0].body if isinstance(n, ast.Assign) and
                       len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and
                       n.targets[0].id == "BASE7_PINS"] if len(funcs) == 1 else []
            if len(assigns) != 1:
                raise RuntimeError("r52 launcher BASE7 assignment")
            order = [("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT", "v14"),
                     ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                     ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                     ("TRANSITION", "transition"), ("AUDIT", "audit")]
            assigns[0].value = ast.Dict(
                keys=[ast.Name(id=name, ctx=ast.Load()) for name, _ in order],
                values=[ast.Tuple([ast.Constant(base7[key][0]),
                                    ast.Constant(base7[key][1])], ast.Load())
                        for _, key in order])
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and \
                        isinstance(node.targets[0], ast.Name) and \
                        node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED":
                    node.value = ast.Constant(True)
            text = ast.unparse(tree) + "\n"
        edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
        if edge not in text:
            raise RuntimeError(f"{role}: r52 edge absent")
        return text.encode()

    ns["_direct_source_patch_r50"] = direct_patch
    old_canon = ns["_canonicalize_registry_helper"]
    def canonicalize(text: str) -> str:
        try:
            return old_canon(text)
        except RuntimeError as exc:
            if ("literal not found" in str(exc) or
                    "literals not found" in str(exc) or
                    "patch incomplete" in str(exc)):
                return text
            raise
    ns["_canonicalize_registry_helper"] = canonicalize
    old_cross = ns["_patch_launcher_validator_cross_role"]
    def cross(text: str) -> str:
        if ("consumer_frozen_predecessor_incident_exact5_bytes_read_only_noncredit_allowed"
                not in text and
                "pin_normalization_preserves_v12_rejection_and_all_historical_pins"
                not in text and
                "actual_runtime_registry_shape_evidence" in text and
                "published_then_officially_rejected_predecessor_v14" in text):
            return text
        return old_cross(text)
    ns["_patch_launcher_validator_cross_role"] = cross

    def reject_previous(builder: Any) -> dict[str, str]:
        close = ns["_close"]
        value = close({
            "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
            "status": "PERMANENT_FAIL_CLOSED_R51_CONTRACT_ACTIVE_BUNDLE_PATH_DRIFT__ZERO_CREDIT",
            "failed_namespace": PREV, "predecessor_namespace": "v16r2r50",
            "rejection_reason": "CONTRACT_ACTIVE_BUNDLE_SOURCE_PATHS_RETAINED_R50",
            "failure_vector": {
                "contract_bundle_contract_path": f"deliverables/{BASE}_contract_v16r2r50.json",
                "contract_bundle_producer_path": f"deliverables/{BASE}_v16r2r50_semantic_source.py",
                "contract_bundle_consumer_path": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2r50_semantic_source.py",
                "required_namespace": PREV,
                "candidate_bytes_remain_immutable": True,
            },
            "candidate_install": True, "runtime_protocol_executed": False,
            "manifest_created": False, "outer_created": False,
            "runtime_authorized": False, "formal_global_closure_credit": 0,
            "D02_unlock": False, "append_only": True,
            "overwrite_delete_or_reuse_allowed": False,
            "candidate_schema_file_sha256": R50_FILES["schema"][1],
            "candidate_contract_file_sha256": R50_FILES["contract"][1],
            "candidate_contract_object_sha256": R50_FILES["contract"][2],
            "candidate_audit_file_sha256": R50_FILES["audit"][1],
            "candidate_audit_object_sha256": R50_FILES["audit"][2],
        })
        raw = ns["_canon"](value) + b"\n"
        return {"path": str(R51_REJECTION.relative_to(ROOT)),
                "file_sha256": hashlib.sha256(raw).hexdigest(),
                "object_sha256": value["object_sha256"], "bytes": raw}
    ns["seal_r50_rejection"] = reject_previous
    return ns


def main() -> int:
    ns = _load_parent()
    try:
        print(json.dumps(ns["install_r51_candidate"](),
                         ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
                          "status": "FAIL_CLOSED_R52_STATIC_INSTALL",
                          "error": {"type": type(exc).__name__,
                                    "message": str(exc)},
                          "candidate_install": False,
                          "manifest_created": False,
                          "outer_created": False,
                          "runtime_authorized": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False}, ensure_ascii=False,
                  sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
