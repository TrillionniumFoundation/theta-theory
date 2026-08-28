#!/usr/bin/env python3
"""Append-only r26 successor; repairs the r25 malformed self-edge retag."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
OLD, PREV, OLD_PREV, TAG = "v16r2r25", "v16r2r25", "v16r2r24", "v16r2r26"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"


def load_parent():
    path = ROOT / "scripts/c79g_v16r2r25_candidate_builder.py"
    spec = importlib.util.spec_from_file_location("_r25_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("r25 builder import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


r = load_parent()
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
    edge_old = f"{BASE}_{OLD_PREV}_to_{OLD}_static_launch_transition_receipt_v1.json"
    edge_bad = f"{BASE}_{OLD}_to_{OLD}_static_launch_transition_receipt_v1.json"
    edge_new = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    anchor_old = f"{BASE}_{OLD}_active_predecessor_supersession_receipt_v1.json"
    anchor_new = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    # Protect both the correctly formed predecessor edge and the malformed
    # r25 self-edge before applying version token substitutions.
    text = (value.replace(edge_old, "__R26_EDGE__")
                 .replace(edge_bad, "__R26_EDGE__")
                 .replace(anchor_old, "__R26_ANCHOR__")
                 .replace("V16R2R24", "__R26_PREV__")
                 .replace("V16R2R25", "__R26_OLD__")
                 .replace("v16r2r24", "__r26_prev__")
                 .replace("v16r2r25", "__r26_old__"))
    return (text.replace("__R26_EDGE__", edge_new)
                .replace("__R26_ANCHOR__", anchor_new)
                .replace("__R26_PREV__", "V16R2R25")
                .replace("__R26_OLD__", "V16R2R26")
                .replace("__r26_prev__", "v16r2r25")
                .replace("__r26_old__", "v16r2r26"))


r.retag = retag
b.retag = retag


def make_rejection() -> dict[str, Any]:
    return b.close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
        "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_STATIC_BUILD__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "R25_ACTIVE_TRANSITION_LITERAL_COLLAPSED_TO_SELF_EDGE",
        "detail": {"failed_check": "successor_tokens_and_active_namespace",
                    "malformed_literal": f"{BASE}_{OLD}_to_{OLD}_static_launch_transition_receipt_v1.json",
                    "required_successor_literal": f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
                    "runtime_protocol_executed": False},
        "append_only": True, "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "manifest_created": False,
        "outer_created": False, "runtime_surface_created": False,
    })


def main() -> int:
    if any(not p.is_file() for p in [*b.SRC_IN.values(), *b.JSON_IN.values(), b.ANCHOR_IN]):
        raise RuntimeError("missing immutable r25 input")
    if not b.REJ.exists():
        b.install(b.REJ, b.canon(make_rejection()) + b"\n")
    else:
        old_rej, _ = b.load(b.REJ)
        if old_rej.get("failed_namespace") != PREV or old_rej.get("formal_global_closure_credit") != 0:
            raise RuntimeError("r25 rejection replay mismatch")
    chain = b.ensure_successor_anchor()
    generated, meta = b.build()
    actions = {}
    for name in ("schema", "contract", "transition", "audit"):
        actions[name] = b.install(b.JSON_OUT[name], generated[name])
    for name in ("producer", "consumer", "launcher"):
        actions[name] = b.install(b.SRC_OUT[name], generated[name], 0o664)
    if b.MANIFEST.exists() or b.OUTER.exists():
        raise RuntimeError("manifest/outer appeared")
    print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
                      "status": "V16R2R26_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
                      "chain": chain, "actions": actions, "meta": meta,
                      "candidate_install": True, "manifest_created": False,
                      "outer_created": False, "runtime_authorized": False,
                      "formal_global_closure_credit": 0, "D02_unlock": False,
                      "pyc_created": False}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
