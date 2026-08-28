#!/usr/bin/env python3
"""Append-only r41 successor after the permanently rejected r40 attempt.

The r40 namespace contains only its immutable rejection/supersession/anchor
chain; it has no candidate bytes to repair.  This clean-room adapter reuses
the reviewed collision-safe r40 *constructor code* in memory, keeps r39's
source/JSON bytes as the only candidate inputs, and changes only the active
chain to r40→r41.  It is intentionally a builder-only entry point: use
``--static-self-check`` (the default) for AST checks; no installation is done
by this file until its explicit ``--install`` option is supplied by the owner.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TEMPLATE = "v16r2r39"
TEMPLATE_PREV = "v16r2r38"
PREV = "v16r2r40"
TAG = "v16r2r41"

R40_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R40_SUP = OUT / f"{BASE}_{TEMPLATE}_to_{PREV}_static_bundle_rejection_supersession_receipt_v1.json"
R40_ANCHOR_SHA256 = "799901b142218de7b1a33a6e16847ad66ce5d90d71fbe70209267d53cbf95c43"
R40_ANCHOR_OBJECT_SHA256 = "05369f3d6ba90b0e737c7f20daf203b116443142c1814ed82ee40ca7c9b09221"
R40_SUP_SHA256 = "785b335c68e813c388c841a74969999b7fccf0548dcd3ef885ebf0ad6aa45dc1"
R40_SUP_OBJECT_SHA256 = "69fafaaafc971cf5b03a54f2340d08008f6c3b80944313281e6a51261469a2b2"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_r40_constructor():
    """Load corrected r40 implementation in memory, retagged only to r41."""
    path = ROOT / "scripts/c79g_v16r2r40_candidate_builder.py"
    raw = path.read_text(encoding="utf-8")
    old_prev = 'PREV = "v16r2r39"'
    old_tag = 'TAG = "v16r2r40"'
    if raw.count(old_prev) != 1 or raw.count(old_tag) != 1:
        raise RuntimeError("r40 constructor assignment census")
    raw = raw.replace(old_prev, 'PREV = "v16r2r40"', 1)
    raw = raw.replace(old_tag, 'TAG = "v16r2r41"', 1)
    ns = {"__name__": "_c79g_r41_constructor", "__file__": str(path),
          "__package__": None}
    exec(compile(raw, str(path), "exec"), ns, ns)
    return ns


def static_self_check() -> dict[str, object]:
    """Check the r41 adapter and immutable r40 anchor without writing files."""
    if not R40_ANCHOR.is_file() or R40_ANCHOR.stat().st_nlink != 1 or \
       stat.S_IMODE(R40_ANCHOR.stat().st_mode) != 0o444:
        raise RuntimeError("r40 active anchor missing or mutable")
    raw = R40_ANCHOR.read_bytes()
    actual_file = hashlib.sha256(raw).hexdigest()
    value = json.loads(raw.decode("utf-8"))
    actual_obj = value.get("object_sha256")
    if actual_file != R40_ANCHOR_SHA256:
        raise RuntimeError(f"r40 anchor file hash drift:{actual_file}")
    # The object hash is intentionally checked against the live JSON value;
    # the file and object hashes differ in a normal closed receipt.
    if actual_obj != R40_ANCHOR_OBJECT_SHA256:
        raise RuntimeError(f"r40 anchor object drift:{actual_obj}")
    if value.get("successor_namespace") != "v16r2r40_semantic_source" or \
       value.get("formal_global_closure_credit") != 0:
        raise RuntimeError("r40 anchor semantic drift")
    if not R40_SUP.is_file() or R40_SUP.stat().st_nlink != 1 or \
       stat.S_IMODE(R40_SUP.stat().st_mode) != 0o444:
        raise RuntimeError("r40 supersession missing or mutable")
    sup_raw = R40_SUP.read_bytes()
    if hashlib.sha256(sup_raw).hexdigest() != R40_SUP_SHA256:
        raise RuntimeError("r40 supersession file hash drift")
    sup = json.loads(sup_raw.decode("utf-8"))
    if sup.get("object_sha256") != R40_SUP_OBJECT_SHA256 or \
       sup.get("successor_namespace") != "v16r2r40":
        raise RuntimeError("r40 supersession semantic drift")
    ns = load_r40_constructor()
    # Re-run the constructor's immutable r39 input census read-only.  This
    # proves the adapter has not silently pivoted to any r40 candidate bytes.
    ns["assert_r39_partial"]()
    # Compile the adapter source and all dynamically loaded constructor code;
    # this does not import/execute any producer, consumer, or launcher source.
    ast.parse(Path(__file__).read_text(encoding="utf-8"), filename=str(__file__))
    for name in ("retag_source", "retag_value", "source_patch", "schema_walk"):
        if not callable(ns.get(name)):
            raise RuntimeError(f"r40 constructor missing {name}")
    return {"status": "PASS_R41_ADAPTER_AST_STATIC_ONLY",
            "template_inputs": "immutable_r39_source_json_bytes",
            "predecessor_anchor": str(R40_ANCHOR.relative_to(ROOT)),
            "predecessor_anchor_file_sha256": actual_file,
            "predecessor_anchor_object_sha256": actual_obj,
            "target_namespace": TAG,
            "runtime_authorized": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "installation_performed": False}


def _install_r41() -> int:
    """Run the adapted constructor only when the caller explicitly opts in."""
    ns = load_r40_constructor()
    original_configure = ns["configure"]

    def configure_r41(module, builder):
        original_configure(module, builder)
        # r40 has no source/JSON candidate, but its active anchor is the
        # immutable predecessor edge for this attempt.  Keep r39 bytes as the
        # actual template inputs while binding the new chain to r40.
        builder.ANCHOR_IN = R40_ANCHOR

    def seal_r40_rejection(builder):
        path = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
        if path.exists():
            value, raw = builder.load(path)
            if value.get("failed_namespace") != PREV or \
               value.get("formal_global_closure_credit") != 0 or \
               value.get("rejection_reason") != "R40_STATIC_CANDIDATE_REJECTED_AFTER_ANCHOR":
                raise RuntimeError("r40 rejection replay mismatch")
            return {"action": "replayed", "file_sha256": builder.sha(raw),
                    "object_sha256": value["object_sha256"]}
        anchor_raw = R40_ANCHOR.read_bytes()
        anchor = json.loads(anchor_raw.decode("utf-8"))
        value = builder.close({
            "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
            "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_STATIC_BUILD__ZERO_CREDIT",
            "failed_namespace": PREV,
            "rejection_reason": "R40_STATIC_CANDIDATE_REJECTED_AFTER_ANCHOR",
            "detail": {"candidate_install": False,
                       "runtime_protocol_executed": False,
                       "anchor_path": str(R40_ANCHOR.relative_to(ROOT)),
                       "anchor_file_sha256": hashlib.sha256(anchor_raw).hexdigest(),
                       "anchor_object_sha256": anchor.get("object_sha256"),
                       "required_successor_fix": "fresh r41 collision_safe_retag_from_r39"},
            "append_only": True, "overwrite_delete_or_reuse_allowed": False,
            "runtime_authorized": False, "formal_global_closure_credit": 0,
            "D02_unlock": False, "manifest_created": False,
            "outer_created": False, "runtime_surface_created": False,
        })
        raw = builder.canon(value) + b"\n"
        builder.install(path, raw)
        installed, installed_raw = builder.load(path)
        return {"action": "installed", "file_sha256": builder.sha(installed_raw),
                "object_sha256": installed["object_sha256"]}

    ns["configure"] = configure_r41
    ns["seal_r39_rejection"] = seal_r40_rejection
    return int(ns["main"]())


def main() -> int:
    try:
        result = static_self_check()
        if "--install" in sys.argv[1:]:
            return _install_r41()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R41_ADAPTER_STATIC_ONLY",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "installation_performed": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False}, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
