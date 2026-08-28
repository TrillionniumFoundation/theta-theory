#!/usr/bin/env python3
"""Append-only r18 redesign preflight; design evidence only.

This checker reads immutable r16/r17 evidence, describes the acyclic byte-pin
layout required by a fresh successor, and freezes one r18 design receipt with
O_EXCL.  It never creates source, schema, contract, transition, audit,
manifest, outer, runtime, authority, or credit artifacts.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
SOURCE = "v16r2r16"
PREDECESSOR = "v16r2r17"
TAG = "v16r2r18"

R16_SOURCES = {
    "producer": OUT / f"{BASE}_{SOURCE}_semantic_source.py",
    "consumer": OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_"
        f"{SOURCE}_semantic_source.py"),
    "launcher": OUT / f"{BASE}_cold_launch_{SOURCE}_semantic_source.py",
}
R16_JSON = {
    "schema": OUT / f"{BASE}_schema_{SOURCE}.json",
    "contract": OUT / f"{BASE}_contract_{SOURCE}.json",
    "transition": OUT / (
        f"{BASE}_v16r2r15_to_{SOURCE}_static_launch_transition_receipt_v1.json"),
    "audit": OUT / f"{BASE}_static_audit_{SOURCE}.json",
}
R17 = {
    "rejection": OUT / f"{BASE}_{SOURCE}_static_bundle_rejection_receipt_v1.json",
    "supersession": OUT / (
        f"{BASE}_{SOURCE}_to_{PREDECESSOR}_static_bundle_rejection_"
        "supersession_receipt_v1.json"),
    "anchor": OUT / f"{BASE}_{PREDECESSOR}_active_predecessor_supersession_receipt_v1.json",
}
REPORT = OUT / f"{BASE}_{TAG}_redesign_preflight_design_receipt_v1.json"


class DuplicateKey(ValueError):
    pass


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def close(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result.pop("object_sha256", None)
    result["object_sha256"] = sha(canonical(result))
    return result


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
        named = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named.st_dev, named.st_ino)):
            raise RuntimeError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def strict_json(path: Path, *, require_object: bool = False) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON object required: {path}")
    claimed = value.get("object_sha256")
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    if claimed is None and not require_object:
        return value, raw
    if claimed != sha(canonical(body)):
        raise RuntimeError(f"object closure mismatch: {path}")
    return value, raw


def install(path: Path, raw: bytes) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if (stable(path) != raw or path.stat().st_nlink != 1 or
                stat.S_IMODE(path.stat().st_mode) != 0o444):
            raise RuntimeError(f"append-only mismatch: {path}")
        return "replayed"
    try:
        offset = 0
        view = memoryview(raw)
        while offset < len(view):
            offset += os.write(fd, view[offset:])
        os.fsync(fd)
        os.fchmod(fd, 0o444)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def evidence(path: Path) -> dict[str, Any]:
    raw = stable(path)
    info: dict[str, Any] = {
        "path": str(path.relative_to(ROOT)),
        "file_sha256": sha(raw),
        "bytes": len(raw),
        "mode": f"{stat.S_IMODE(path.stat().st_mode):04o}",
        "nlink": path.stat().st_nlink,
    }
    if path.suffix == ".json":
        value, _ = strict_json(path)
        if "object_sha256" in value:
            info["object_sha256"] = value["object_sha256"]
    return info


def candidate_paths() -> list[Path]:
    return [
        OUT / f"{BASE}_{TAG}_semantic_source.py",
        OUT / (f"{BASE}_independent_verifier_assembler_authority_consumer_"
               f"{TAG}_semantic_source.py"),
        OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
        OUT / f"{BASE}_schema_{TAG}.json",
        OUT / f"{BASE}_contract_{TAG}.json",
        OUT / f"{BASE}_{PREDECESSOR}_to_{TAG}_static_launch_transition_receipt_v1.json",
        OUT / f"{BASE}_static_audit_{TAG}.json",
        OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
        OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
        OUT / f"{BASE}_{TAG}_runtime.json",
        OUT / f"{BASE}_{TAG}_formal_global_closure_credit.json",
    ]


def verify_r17_chain() -> dict[str, Any]:
    rejection, rejection_raw = strict_json(R17["rejection"], require_object=True)
    supersession, supersession_raw = strict_json(R17["supersession"], require_object=True)
    anchor, _ = strict_json(R17["anchor"], require_object=True)
    checks = {
        "supersession_rejection_file_pin":
            supersession.get("predecessor_rejection_file_sha256") == sha(rejection_raw),
        "supersession_rejection_object_pin":
            supersession.get("predecessor_rejection_object_sha256") ==
            rejection.get("object_sha256"),
        "anchor_supersession_file_pin":
            anchor.get("predecessor_supersession_file_sha256") == sha(supersession_raw),
        "anchor_supersession_object_pin":
            anchor.get("predecessor_supersession_object_sha256") ==
            supersession.get("object_sha256"),
        "anchor_successor_namespace":
            anchor.get("successor_namespace") == f"{PREDECESSOR}_semantic_source",
        "chain_zero_credit": all(value.get("formal_global_closure_credit") == 0
                                 for value in (rejection, supersession, anchor)),
        "chain_D02_locked": all(value.get("D02_unlock") is False
                                for value in (rejection, supersession, anchor)),
    }
    if not all(checks.values()):
        raise RuntimeError(f"r17 chain failed: {checks}")
    return checks


def current_transition_shape() -> dict[str, Any]:
    transition, _ = strict_json(R16_JSON["transition"], require_object=True)
    successor = transition.get("successor_v16r2_static_bundle")
    if not isinstance(successor, dict):
        raise RuntimeError("r16 successor_v16r2_static_bundle missing")
    expected_keys = {
        "all_four_core_file_pins_final", "build_only_producer",
        "closed_schema", "cold_launcher_v16r2_path", "contract",
        "draft_pin_sentinels_remain_present", "final_consumer_pin_installed",
        "independent_verifier_assembler_authority_consumer",
        "static_audit_v16r2_path",
        "transition_receipt_bytes_are_closed_around_final_core_pins",
        "transition_receipt_physical_freeze_completed",
    }
    return {
        "actual_key_count": len(successor),
        "actual_keys": sorted(successor),
        "missing_required_keys": sorted(expected_keys - set(successor)),
        "extra_generic_draft_keys": sorted(set(successor) - expected_keys),
        "matches_exact_11_key_design": set(successor) == expected_keys,
    }


def cycle_break_requirements() -> dict[str, Any]:
    reverse_edges = []
    for artifact in ("contract", "transition", "audit"):
        for role in ("producer", "consumer", "launcher"):
            reverse_edges.append({
                "remove_from_hashed_body": f"{artifact}.active.source_hashes.{role}",
                "edge": f"{artifact}_bytes -> {role}_source_bytes",
                "reason": (
                    f"{role} source is downstream of, or pins, {artifact}; "
                    "retaining this reverse file-hash commitment prevents a DAG"),
                "replacement": (
                    "post-source binding evidence not read or pinned by any "
                    "source byte sequence"),
            })
    return {
        "required_topological_order": [
            "active_predecessor_anchor", "closed_schema", "contract",
            "producer_source", "consumer_source", "transition", "audit",
            "launcher_source",
        ],
        "pin_edge_rule": (
            "a hashed node may commit only to nodes strictly earlier in the "
            "required_topological_order"),
        "must_remove_reverse_source_hash_edges": reverse_edges,
        "must_remove_generic_members": [
            "contract.active.source_hashes",
            "transition.successor_v16r2_static_bundle.source_hashes",
            "audit.audited_v16r2_bundle.source_hashes",
        ],
        "allowed_forward_closure": {
            "contract": ["active_predecessor_anchor", "closed_schema"],
            "producer_source": ["active_predecessor_anchor", "closed_schema", "contract"],
            "consumer_source": [
                "active_predecessor_anchor", "closed_schema", "contract",
                "producer_source"],
            "transition": [
                "active_predecessor_anchor", "closed_schema", "contract",
                "producer_source", "consumer_source"],
            "audit": [
                "active_predecessor_anchor", "closed_schema", "contract",
                "producer_source", "consumer_source", "transition"],
            "launcher_source": [
                "active_predecessor_anchor", "closed_schema", "contract",
                "producer_source", "consumer_source", "transition", "audit"],
        },
        "forbidden_self_cycles": [
            ["producer_source", "contract", "producer_source"],
            ["consumer_source", "contract", "consumer_source"],
            ["launcher_source", "contract", "launcher_source"],
            ["launcher_source", "transition", "launcher_source"],
            ["launcher_source", "audit", "launcher_source"],
        ],
        "source_hash_binding_policy": (
            "source hash claims may be emitted only in a later external binding "
            "receipt that no source embeds or pins; they must not be duplicated "
            "inside contract/transition/audit hashed bodies"),
    }


def successor_design() -> dict[str, Any]:
    keys = [
        "all_four_core_file_pins_final", "build_only_producer",
        "closed_schema", "cold_launcher_v16r2_path", "contract",
        "draft_pin_sentinels_remain_present", "final_consumer_pin_installed",
        "independent_verifier_assembler_authority_consumer",
        "static_audit_v16r2_path",
        "transition_receipt_bytes_are_closed_around_final_core_pins",
        "transition_receipt_physical_freeze_completed",
    ]
    return {
        "member_name": "successor_v16r2_static_bundle",
        "exact_key_count": 11,
        "exact_keyset_sorted": sorted(keys),
        "additional_properties": False,
        "required_boolean_values": {
            "all_four_core_file_pins_final": True,
            "draft_pin_sentinels_remain_present": False,
            "final_consumer_pin_installed": True,
            "transition_receipt_bytes_are_closed_around_final_core_pins": True,
            "transition_receipt_physical_freeze_completed": False,
        },
        "required_nested_objects": {
            "closed_schema": {
                "exact_keyset_sorted": ["file_sha256", "path"],
                "file_sha256": "actual_lower_hex_sha256",
            },
            "contract": {
                "exact_keyset_sorted": ["file_sha256", "object_sha256", "path"],
                "file_sha256": "actual_lower_hex_sha256",
                "object_sha256": "actual_closed_object_sha256",
            },
            "build_only_producer": {
                "exact_keyset_sorted": ["file_sha256", "path"],
                "file_sha256": "actual_lower_hex_sha256",
            },
            "independent_verifier_assembler_authority_consumer": {
                "exact_keyset_sorted": ["file_sha256", "path"],
                "file_sha256": "actual_lower_hex_sha256",
            },
        },
        "required_path_strings": {
            "static_audit_v16r2_path": "fresh_r18_audit_path",
            "cold_launcher_v16r2_path": "fresh_r18_launcher_path",
        },
        "forbidden_members": [
            "source_hashes", "pin_state", "exact8_ordered_paths",
            "exact10_ordered_paths", "post_source_static_trust_receipts",
            "cold_launch_outer_closure", "formal_global_closure_credit",
            "D02_unlock", "runtime_authorized",
        ],
        "phase_note": (
            "transition_receipt_physical_freeze_completed remains false in the "
            "pre-freeze transition bytes and is proven true only by later "
            "physical freeze evidence"),
    }


def acceptance_predicates() -> list[dict[str, Any]]:
    return [
        {"id": "A01_fresh_namespace", "predicate":
         "every r18 candidate target absent before O_EXCL; no r16/r17 write target"},
        {"id": "A02_pin_graph_dag", "predicate":
         "all byte-hash edges follow the declared 8-node topological order"},
        {"id": "A03_no_reverse_source_hashes", "predicate":
         "no contract/transition/audit hashed body contains generic source_hashes"},
        {"id": "A04_actual_core_pins", "predicate":
         "all file/object pins are actual 64-lower-hex hashes; no c/d/e/f or UNPINNED sentinel"},
        {"id": "A05_final_source_flags", "predicate":
         "producer/consumer/launcher final pin flags true; draft runtime remains disabled"},
        {"id": "A06_source_syntax", "predicate":
         "three sources UTF-8, AST parse and in-memory compile under -I -B; no pyc"},
        {"id": "A07_strict_json_closure", "predicate":
         "schema/contract/transition/audit duplicate-free strict JSON; every receipt object hash closes"},
        {"id": "A08_schema_shape", "predicate":
         "closed schema is 46 defs / 242 refs / 52 additionalProperties=false"},
        {"id": "A09_instance_shapes", "predicate":
         "contract/transition/audit top-level shapes are exactly 30/31/30"},
        {"id": "A10_successor_exact11", "predicate":
         "transition successor equals the exact 11-key design and boolean values in this receipt"},
        {"id": "A11_independent_static_gates", "predicate":
         "independent reviewer A and structurally independent checker B both 34/34; CI uses jq -e"},
        {"id": "A12_zero_credit_static_phase", "predicate":
         "formal_global_closure_credit=0, D02_unlock=false, runtime_authorized=false"},
        {"id": "A13_cold_order", "predicate":
         "after static GO only: exact8 freeze then manifest ninth then outer tenth/last"},
        {"id": "A14_independent_runtime_evidence", "predicate":
         "dual PYTHONHASHSEED, no-producer, attack set, byte equality and terminal replay all pass"},
        {"id": "A15_public_reconstruction", "predicate":
         "independent consumer reconstructs 76832 successors and 862 Kraft parents with unresolved=0"},
        {"id": "A16_positive_wrapper_only", "predicate":
         "credit=1 and D02_unlock=true appear only in a later independent positive wrapper"},
    ]


def build_report() -> tuple[dict[str, Any], bytes]:
    for path in (*R16_SOURCES.values(), *R16_JSON.values(), *R17.values()):
        if not path.is_file():
            raise RuntimeError(f"required immutable input missing: {path}")
    existing = [str(path.relative_to(ROOT)) for path in candidate_paths()
                if path.exists()]
    if existing:
        raise RuntimeError(f"r18 candidate already exists: {existing}")
    chain_checks = verify_r17_chain()
    inputs = {
        **{f"r16_source_{name}": evidence(path)
           for name, path in R16_SOURCES.items()},
        **{f"r16_json_{name}": evidence(path)
           for name, path in R16_JSON.items()},
        **{f"r17_{name}": evidence(path) for name, path in R17.items()},
    }
    value = close({
        "schema": f"cm2.c79g.{TAG}.redesign-preflight-design-receipt.v1",
        "status": "PASS_R18_REDESIGN_PREFLIGHT__DESIGN_ONLY__NO_CANDIDATE",
        "source_namespace": SOURCE,
        "predecessor_namespace": PREDECESSOR,
        "proposed_successor_namespace": TAG,
        "design_evidence_only": True,
        "candidate_acceptance_evaluated": False,
        "candidate_install": False,
        "candidate_artifacts_installed": False,
        "immutable_input_evidence": inputs,
        "r17_chain_checks": chain_checks,
        "observed_r16_transition_successor": current_transition_shape(),
        "pin_graph_cycle_break_requirements": cycle_break_requirements(),
        "transition_successor_exact_final_core_design": successor_design(),
        "fresh_candidate_acceptance_predicates": acceptance_predicates(),
        "fresh_candidate_acceptance_predicate_count": 16,
        "append_only": True,
        "overwrite_delete_or_authority_write_allowed": False,
        "manifest_created": False,
        "outer_created": False,
        "runtime_surface_created": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    })
    raw = canonical(value) + b"\n"
    return value, raw


def main() -> int:
    try:
        value, raw = build_report()
        action = install(REPORT, raw)
        after_candidates = [str(path.relative_to(ROOT)) for path in candidate_paths()
                            if path.exists()]
        pyc = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc")
               if TAG in str(path)]
        if after_candidates or pyc:
            raise RuntimeError(
                f"forbidden output appeared: candidates={after_candidates}, pyc={pyc}")
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.redesign-preflight-checker.result.v1",
            "status": value["status"],
            "report": {
                "path": str(REPORT.relative_to(ROOT)),
                "file_sha256": sha(raw),
                "object_sha256": value["object_sha256"],
                "mode": "0444",
                "nlink": REPORT.stat().st_nlink,
                "action": action,
            },
            "pin_graph_cycle_break_requirement_count": 9,
            "transition_successor_exact_key_count": 11,
            "fresh_candidate_acceptance_predicate_count": 16,
            "candidate_install": False,
            "candidate_artifacts_installed": False,
            "manifest_created": False,
            "outer_created": False,
            "runtime_surface_created": False,
            "pyc_created": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.redesign-preflight-checker.failure.v1",
            "status": "FAIL_CLOSED_R18_REDESIGN_PREFLIGHT",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "candidate_install": False,
            "candidate_artifacts_installed": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
