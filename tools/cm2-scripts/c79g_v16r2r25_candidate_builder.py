#!/usr/bin/env python3
"""Append-only r25 successor of the rejected r24 static bundle.

The only semantic correction is the active predecessor/current transition
retag order: edge and anchor tokens are protected before version substitution,
so source literals retain ``r23_to_r25`` rather than collapsing to ``r25_to_r25``.
The r24 runtime-path fix is inherited; no manifest/outer/runtime/credit action
is permitted.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
OLD = "v16r2r24"
PREV = "v16r2r24"
OLD_PREV = "v16r2r23"
TAG = "v16r2r25"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"


def load_r24():
    path = ROOT / "scripts/c79g_v16r2r24_candidate_builder.py"
    spec = importlib.util.spec_from_file_location("_r24_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("r24 builder import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


r = load_r24()
b = r.b
r.OLD, r.PREV, r.OLD_PREV, r.TAG = OLD, PREV, OLD_PREV, TAG
r.UPSTREAM, r.CHECKPOINT = UPSTREAM, CHECKPOINT
b.R16, b.PREV, b.TAG = OLD, PREV, TAG
b.UPSTREAM, b.CHECKPOINT = UPSTREAM, CHECKPOINT
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
    # Protect edge/anchor first; otherwise the current token in a newly formed
    # edge would be retagged a second time.
    text = (value.replace(old_edge, "__R25_EDGE__")
                 .replace(old_anchor, "__R25_ANCHOR__")
                 .replace("V16R2R23", "__R25_PREV__")
                 .replace("V16R2R24", "__R25_OLD__")
                 .replace("v16r2r23", "__r25_prev__")
                 .replace("v16r2r24", "__r25_old__"))
    return (text.replace("__R25_EDGE__", new_edge)
                .replace("__R25_ANCHOR__", new_anchor)
                .replace("__R25_PREV__", "V16R2R24")
                .replace("__R25_OLD__", "V16R2R25")
                .replace("__r25_prev__", "v16r2r24")
                .replace("__r25_old__", "v16r2r25"))


r.retag = retag
b.retag = retag


def make_rejection() -> dict[str, Any]:
    return b.close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
        "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_STATIC_BUILD__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "R24_ACTIVE_TRANSITION_LITERAL_COLLAPSED_TO_SELF_EDGE",
        "detail": {
            "failed_check": "successor_tokens_and_active_namespace",
            "malformed_literal": f"{BASE}_{OLD_PREV}_to_{OLD}_static_launch_transition_receipt_v1.json",
            "required_successor_literal": f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
            "runtime_protocol_executed": False,
        },
        "append_only": True, "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "manifest_created": False,
        "outer_created": False, "runtime_surface_created": False,
    })


def main() -> int:
    inputs = [*b.SRC_IN.values(), *b.JSON_IN.values(), b.ANCHOR_IN]
    if any(not p.is_file() for p in inputs):
        raise RuntimeError("missing immutable r24 input")
    if not b.REJ.exists():
        rejection = make_rejection()
        b.install(b.REJ, b.canon(rejection) + b"\n")
    else:
        old_rej, _ = b.load(b.REJ)
        if old_rej.get("failed_namespace") != PREV or old_rej.get("formal_global_closure_credit") != 0:
            raise RuntimeError("r24 rejection replay mismatch")
    chain = b.ensure_successor_anchor()
    generated, meta = b.build()
    actions = {}
    for name in ("schema", "contract", "transition", "audit"):
        actions[name] = b.install(b.JSON_OUT[name], generated[name])
    for name in ("producer", "consumer", "launcher"):
        actions[name] = b.install(b.SRC_OUT[name], generated[name], 0o664)
    if b.MANIFEST.exists() or b.OUTER.exists():
        raise RuntimeError("manifest/outer appeared")
    print(json.dumps({
        "schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
        "status": "V16R2R25_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
        "chain": chain, "actions": actions, "meta": meta,
        "candidate_install": True, "manifest_created": False,
        "outer_created": False, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "pyc_created": False,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
