#!/usr/bin/env python3
"""Append-only r24 static successor builder.

This wrapper reuses only the generic, read-only DAG assembly helpers from the
previous builder.  It seals the r23 rejection/supersession/anchor chain first,
then derives a fresh r24 bundle.  It repairs the runtime-reachable SELF path
assertions inherited by r23; no protocol source is executed and no manifest,
outer receipt, runtime surface, credit, or D02 state is created here.
"""
from __future__ import annotations

import ast
import copy
import importlib.util
import json
import os
import re
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
OLD = "v16r2r23"
PREV = "v16r2r23"
OLD_PREV = "v16r2r22"
TAG = "v16r2r24"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"


def _load_generic():
    path = ROOT / "scripts/c79g_v16r2r19_candidate_builder.py"
    spec = importlib.util.spec_from_file_location("_r24_generic_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("generic builder import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


b = _load_generic()
b.R16 = OLD
b.PREV = PREV
b.TAG = TAG
b.UPSTREAM = UPSTREAM
b.CHECKPOINT = CHECKPOINT
b.SRC_IN = {
    "producer": OUT / f"{BASE}_{OLD}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{OLD}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{OLD}_semantic_source.py",
}
b.JSON_IN = {
    "schema": OUT / f"{BASE}_schema_{OLD}.json",
    "contract": OUT / f"{BASE}_contract_{OLD}.json",
    "transition": OUT / f"{BASE}_{OLD_PREV}_to_{OLD}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{OLD}.json",
}
b.ANCHOR_IN = OUT / f"{BASE}_{OLD}_active_predecessor_supersession_receipt_v1.json"
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


def retag(value: Any) -> Any:
    """Retag only active r23/r22 edge tokens; preserve historical evidence."""
    if isinstance(value, dict):
        return {retag(k): retag(v) for k, v in value.items()}
    if isinstance(value, list):
        return [retag(v) for v in value]
    if not isinstance(value, str):
        return value
    old_edge = f"{BASE}_{OLD_PREV}_to_{OLD}_static_launch_transition_receipt_v1.json"
    new_edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    old_anchor = f"{BASE}_{OLD}_active_predecessor_supersession_receipt_v1.json"
    new_anchor = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    text = value.replace(old_edge, new_edge).replace(old_anchor, new_anchor)
    # Placeholder substitution prevents predecessor/current cascades.
    text = text.replace("V16R2R22", "__R24_PREV__").replace("V16R2R23", "__R24_OLD__")
    text = text.replace("v16r2r22", "__r24_prev__").replace("v16r2r23", "__r24_old__")
    return (text.replace("__R24_PREV__", "V16R2R23")
                .replace("__R24_OLD__", "V16R2R24")
                .replace("__r24_prev__", "v16r2r23")
                .replace("__r24_old__", "v16r2r24"))


b.retag = retag


def _replace_pin(text: str, role: str, name: str, value: str,
                 required: bool = True) -> str:
    pattern = rf'(?m)^({re.escape(name)}\s*=\s*)"[0-9a-f]{{64}}"\s*$'
    text, count = re.subn(pattern, rf'\1"{value}"', text)
    if required and count != 1:
        raise RuntimeError(f"{role}:{name}:replacement_count={count}")
    return text


def source_patch(raw: bytes, role: str, paths: dict[str, str],
                 anchor_file: str, anchor_object: str, schema_hash: str,
                 contract_hash: str, contract_object: str,
                 producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = retag(raw.decode("utf-8"))
    # These inherited assertions were runtime-reachable and pointed to
    # nonexistent unsuffixed v16r2 files.  Bind them to this exact candidate.
    old_producer = f"{BASE}_v16r2.py"
    old_consumer = f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2.py"
    old_launcher = f"{BASE}_cold_launch_v16r2.py"
    text = (text.replace(old_producer, f"{BASE}_{TAG}_semantic_source.py")
                .replace(old_consumer,
                         f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py")
                .replace(old_launcher, f"{BASE}_cold_launch_{TAG}_semantic_source.py"))
    text = _replace_pin(text, role, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", anchor_file)
    text = _replace_pin(text, role, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", anchor_object)
    if role != "launcher":
        text = _replace_pin(text, role, "CONTRACT_FILE_PIN", contract_hash)
        text = _replace_pin(text, role, "CONTRACT_OBJECT_PIN", contract_object)
        text = _replace_pin(text, role, "CLOSED_SCHEMA_FILE_PIN", schema_hash)
    if role == "consumer":
        text = _replace_pin(text, role, "PRODUCER_SOURCE_PIN", producer_hash or "")
    if role == "launcher":
        if base7 is None:
            raise RuntimeError("launcher base7 missing")
        names = [("ACTIVE_PREDECESSOR_SUPERSESSION", "anchor"),
                 ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                 ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                 ("TRANSITION", "transition"), ("AUDIT", "audit")]
        entries = "    BASE7_PINS.update({\n" + "".join(
            f"        {var}: (\"{base7[key][0]}\", {base7[key][1]!r}),\n"
            for var, key in names) + "    })"
        pattern = r"(?s)    BASE7_PINS\.update\(\{.*?\n    \}\)\n    EXACT8"
        text, count = re.subn(pattern, entries + "\n    EXACT8", text, count=1)
        if count != 1:
            raise RuntimeError(f"launcher:BASE7 map replacement_count={count}")
    tree = ast.parse(text, filename=str(b.SRC_OUT[role]), mode="exec")
    compile(tree, str(b.SRC_OUT[role]), "exec")
    for stale in (old_producer, old_consumer, old_launcher):
        if stale in text:
            raise RuntimeError(f"{role}:stale_runtime_path:{stale}")
    return text.encode("utf-8") if text.endswith("\n") else (text + "\n").encode("utf-8")


b.source_patch = source_patch


def make_r23_rejection() -> tuple[dict[str, Any], bytes]:
    return b.close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
        "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_RUNTIME_PATH_AUDIT__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "RUNTIME_REACHABLE_SELF_PATH_ASSERTIONS_BIND_NONEXISTENT_V16R2_FILENAMES",
        "detail": {
            "producer_self_assertion_count": 2,
            "producer_contract_consumer_path_assertion_count": 1,
            "consumer_self_assertion_count": 1,
            "launcher_self_assertion_count": 1,
            "unsuffixed_paths": [
                f"deliverables/{BASE}_v16r2.py",
                f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v16r2.py",
                f"deliverables/{BASE}_cold_launch_v16r2.py",
            ],
            "actual_r23_paths": {
                "producer": f"deliverables/{BASE}_{OLD}_semantic_source.py",
                "consumer": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{OLD}_semantic_source.py",
                "launcher": f"deliverables/{BASE}_cold_launch_{OLD}_semantic_source.py",
            },
            "runtime_protocol_executed": False,
        },
        "append_only": True, "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "manifest_created": False,
        "outer_created": False, "runtime_surface_created": False,
    })


def main() -> int:
    inputs = [*b.SRC_IN.values(), *b.JSON_IN.values(), b.ANCHOR_IN]
    targets = [*b.SRC_OUT.values(), *b.JSON_OUT.values(), b.MANIFEST, b.OUTER,
               b.REJ, b.SUP, b.ANCHOR]
    if any(not path.is_file() for path in inputs):
        raise RuntimeError("missing immutable r23 input")
    # The predecessor rejection is the only new byte permitted before the
    # r24 supersession/anchor.  Replays must match exactly.
    rejection = make_r23_rejection()
    if b.REJ.exists():
        existing, existing_raw = b.load(b.REJ)
        if (existing.get("failed_namespace") != PREV or
                existing.get("formal_global_closure_credit") != 0 or
                existing.get("runtime_authorized") is not False):
            raise RuntimeError("existing r23 rejection is not a zero-credit replay")
    else:
        b.install(b.REJ, b.canon(rejection) + b"\n")
    chain = b.ensure_successor_anchor()
    generated, meta = b.build()
    actions: dict[str, str] = {}
    for name in ("schema", "contract", "transition", "audit"):
        actions[name] = b.install(b.JSON_OUT[name], generated[name])
    for name in ("producer", "consumer", "launcher"):
        actions[name] = b.install(b.SRC_OUT[name], generated[name], 0o664)
    if b.MANIFEST.exists() or b.OUTER.exists():
        raise RuntimeError("manifest/outer appeared")
    print(json.dumps({
        "schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
        "status": "V16R2R24_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
        "chain": chain, "actions": actions, "meta": meta,
        "candidate_install": True, "manifest_created": False,
        "outer_created": False, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "pyc_created": False,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
