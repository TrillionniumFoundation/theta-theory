#!/usr/bin/env python3
"""Build the v16r9 zero-credit JSON quartet against the r9 source bytes.

This wrapper reuses the fail-closed input/identity logic from the r6 builder,
but gives the successor a single coherent tag: r9 sources point at r9 JSON
paths, and the generated JSON pins those exact source bytes.  It never edits
the v16r2/r6 files and is dry-run by default.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r9"
PREDECESSOR_TAG = "v16r8"

R9_SOURCE_DEFAULTS = {
    "producer": OUT / f"{BASE}_v16r2r9_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r9_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_v16r2r9_semantic_source.py",
    "supersession": OUT / f"{BASE}_v16r2r8_active_predecessor_supersession_receipt_v1.json",
}


def load_base():
    path = Path(__file__).with_name("c79g_r6_json_bundle_builder.py")
    spec = importlib.util.spec_from_file_location("c79g_r6_json_bundle_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load base builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def recursive_retag(value, old: str = "v16r6", new: str = TAG):
    """Retag only fields introduced by the r6 wrapper, preserving old history."""
    if isinstance(value, dict):
        return {recursive_retag(k, old, new): recursive_retag(v, old, new)
                for k, v in value.items()}
    if isinstance(value, list):
        return [recursive_retag(v, old, new) for v in value]
    if isinstance(value, str):
        return (value.replace("v16r2-to-v16r6", f"{PREDECESSOR_TAG}-to-{TAG}")
                     .replace("v16r2_to_v16r6", f"{PREDECESSOR_TAG}_to_{TAG}")
                     .replace("_is_r6_semantic_", "_is_r9_semantic_")
                     .replace("_r6_semantic_", "_r9_semantic_")
                     .replace(old, new))
    return value


def reclose(module, value: dict):
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    return module.close_object(body)


def target_outputs():
    return {
        "schema": OUT / f"{BASE}_schema_{TAG}.json",
        "contract": OUT / f"{BASE}_contract_{TAG}.json",
        "transition": OUT / f"{BASE}_{PREDECESSOR_TAG}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
    }


def target_paths(outputs, source_cfg, predecessor):
    rel = lambda p: str(Path(p).relative_to(ROOT))
    return {
        "checkpoint": "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
        "predecessor_supersession": rel(predecessor),
        "schema": rel(outputs["schema"]), "contract": rel(outputs["contract"]),
        "transition": rel(outputs["transition"]), "audit": rel(outputs["audit"]),
        "producer": rel(source_cfg["producer"]), "consumer": rel(source_cfg["consumer"]),
        "launcher": rel(source_cfg["launcher"]),
        "manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
        "outer": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json",
        "candidate_A": ".cm2-runtime/c79g-v16r9-candidate-a-b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
        "candidate_B": ".cm2-runtime/c79g-v16r9-candidate-b-b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
        "verification_A": ".cm2-runtime/c79g-v16r9-verification-a-b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
        "verification_B": ".cm2-runtime/c79g-v16r9-verification-b-b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
        "committed_completion": ".cm2-runtime/c79g-v16r9-committed-completion-b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
        "rejection_namespace": ".cm2-runtime/c79g-v16r9-rejections-b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
        "later_rejection": ".cm2-runtime/c79g-v16r9-rejections-b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab/rejection.json",
        "authority_seal": ".cm2-runtime/cm2-global-authority-heads/c79g-v16r9-b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab.seal",
    }


def validate_shapes(module, schema, contract, transition, audit, paths):
    defs = schema.get("$defs", {})
    refs = sum(1 for n in module.walk(schema) if isinstance(n, dict) and "$ref" in n)
    closed = sum(1 for n in module.walk(schema)
                 if isinstance(n, dict) and n.get("additionalProperties") is False)
    if (len(defs), refs, closed) != (46, 242, 52):
        raise module.BuildError(f"r9 schema shape {(len(defs), refs, closed)}")
    if (len(contract), len(transition), len(audit)) != (30, 31, 30):
        raise module.BuildError("r9 top-level shape must be 30/31/30")
    active_field = "current_exact8_first_member_is_r9_semantic_supersession_receipt"
    for name in ("coldLaunchProof", "staticFreezeProof"):
        d = defs[name]
        if active_field not in d.get("properties", {}) or active_field not in d.get("required", []):
            raise module.BuildError(f"r9 active field missing: {name}")
    for value, label in ((contract, "contract"), (transition, "transition"), (audit, "audit")):
        module.verify_object(value, label)
        module.ensure_zero_credit(value, label)
    expected_keys = (f"{TAG}_bundle", f"successor_{TAG}_static_bundle",
                     f"audited_{TAG}_bundle")
    for key in expected_keys:
        found = [value for value in (contract, transition, audit) if key in value]
        if found and found[0][key].get("exact8_ordered_paths", [None])[0] != paths["predecessor_supersession"]:
            raise module.BuildError(key + ": predecessor path mismatch")
    return {"schema_defs": len(defs), "schema_refs": refs,
            "closed_objects": closed, "contract_keys": len(contract),
            "transition_keys": len(transition), "audit_keys": len(audit)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    for role in ("producer", "consumer", "launcher", "supersession"):
        parser.add_argument("--" + role)
    args = parser.parse_args(argv)
    module = None
    try:
        module = load_base()
        source_cfg = dict(R9_SOURCE_DEFAULTS)
        for role in source_cfg:
            value = getattr(args, role)
            if value:
                source_cfg[role] = Path(value) if Path(value).is_absolute() else ROOT / value
            if not source_cfg[role].is_file():
                raise module.BuildError(f"missing r9 {role}: {source_cfg[role]}")
        outputs = target_outputs()
        # Point the imported helper at this target without touching its files.
        module.R6_TAG = TAG
        module.R6_OUT = outputs
        old_values, old_raws, old_shape = module.validate_old_inputs()
        c53 = module.validate_c53(module.C53_CHECKPOINT)
        predecessor, predecessor_raw = module.read_json(source_cfg["supersession"])
        predecessor_report = module.validate_predecessor_anchor(
            predecessor, predecessor_raw, module.C53_CHECKPOINT)
        source = module.source_hashes(source_cfg)
        paths = target_paths(outputs, source_cfg, source_cfg["supersession"])
        module.validate_source_path_graph(source_cfg, paths)
        schema = module.make_schema(old_values["schema"], paths, source,
                                    module.C53_CHECKPOINT,
                                    predecessor["object_sha256"])
        # Retag wrapper-introduced names before computing bytes/hashes.
        schema = recursive_retag(schema)
        schema_raw = module.json_bytes(schema)
        schema_hash = module.sha(schema_raw)
        old_bundle = old_values["contract"].get("v16r2_bundle")
        if not isinstance(old_bundle, dict):
            raise module.BuildError("v16r2 contract bundle missing")
        bundle = module.make_bundle(old_bundle, paths, source, schema_hash,
                                    module.C53_CHECKPOINT, c53,
                                    predecessor["object_sha256"])
        contract = recursive_retag(module.make_contract(old_values["contract"], bundle,
                                                         module.C53_CHECKPOINT))
        transition = recursive_retag(module.make_transition(old_values["transition"], bundle,
                                                             paths, module.C53_CHECKPOINT))
        audit = recursive_retag(module.make_audit(old_values["audit"], bundle,
                                                  paths, module.C53_CHECKPOINT, c53))
        # Retagging changed the hashed body; close each top-level receipt again.
        contract = reclose(module, contract)
        transition = reclose(module, transition)
        audit = reclose(module, audit)
        shape = validate_shapes(module, schema, contract, transition, audit, paths)
        outputs_raw = {
            "schema": (outputs["schema"], schema_raw),
            "contract": (outputs["contract"], module.json_bytes(contract)),
            "transition": (outputs["transition"], module.json_bytes(transition)),
            "audit": (outputs["audit"], module.json_bytes(audit)),
        }
        if args.dry_run or not args.dry_run:
            installed = {key: "dry-run" for key in outputs_raw}
            if not args.dry_run:
                installed = {key: module.install_o_excl(path, raw)
                             for key, (path, raw) in outputs_raw.items()}
        hashes = {key: module.sha(raw) for key, (_, raw) in outputs_raw.items()}
        report = {
            "schema": "cm2.c79g.v16r9.json-bundle-builder.result.v1",
            "status": "R9_JSON_BUNDLE_DRY_RUN_PASS__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED" if args.dry_run else
                      "R9_JSON_BUNDLE_DRAFT_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "effective_checkpoint_object_sha256": module.C53_CHECKPOINT,
            "c53": c53,
            "predecessor_supersession": {"path": paths["predecessor_supersession"], **predecessor_report},
            "active_paths": paths, "source_hashes": source,
            "shape": {**shape, "old_v16r2_shape": old_shape,
                      "baseline_rows": module.UNIVERSE_ROWS,
                      "baseline_public_unresolved": module.BASELINE_PUBLIC_UNRESOLVED},
            "file_hashes": hashes, "installed": installed,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "D02_started": False, "D02_formal_pending_task_count": module.D02_PENDING,
            "manifest_created": False, "outer_created": False,
            "runtime_authorized": False,
            "writes": {"r9_outputs": not args.dry_run, "old_outputs": False,
                        "manifest": False, "outer": False, "runtime": False,
                        "credit": False, "pyc": False},
        }
        print(json.dumps(report, ensure_ascii=True, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": "cm2.c79g.v16r9.json-bundle-builder.failure.v1",
                          "status": "FAIL_CLOSED_R9_JSON_BUILDER",
                          "error_type": type(exc).__name__, "error": str(exc),
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "runtime_authorized": False, "writes": False}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
