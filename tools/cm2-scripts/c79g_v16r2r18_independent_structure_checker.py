#!/usr/bin/env python3
"""Independent, read-only structural checker for the r18 clean-room.

The checker deliberately does not import or execute any candidate source.  It
only reads bytes, parses Python ASTs, compiles in memory, and validates the
append-only receipt graph.  Before a builder installs a complete r18 bundle it
prints ``NO_CANDIDATE/PREFLIGHT_ONLY`` and performs no filesystem write.  A
partial bundle is a fail-closed result; a complete bundle is checked against
the design receipt's exact eleven-key successor contract.
"""

from __future__ import annotations

import ast
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
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r18"
PREV = "v16r2r17"
DESIGN = OUT / f"{BASE}_{TAG}_redesign_preflight_design_receipt_v1.json"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"

FILES = {
    "anchor": OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
    "supersession": OUT / (
        f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"),
    "rejection": OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json",
    "schema": OUT / f"{BASE}_schema_{TAG}.json",
    "contract": OUT / f"{BASE}_contract_{TAG}.json",
    "transition": OUT / (
        f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"),
    "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
    "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
    "consumer": OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"),
    "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
}
SOURCES = ("producer", "consumer", "launcher")
CORE_JSON = ("schema", "contract", "transition", "audit")
CHAIN_JSON = ("anchor", "supersession", "rejection")


class DuplicateKey(ValueError):
    pass


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in items:
        if key in out:
            raise DuplicateKey(key)
        out[key] = value
    return out


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def safe_read(path: Path) -> bytes:
    """Read one immutable regular file without following a symlink."""
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular/nlink1: {rel(path)}")
        if (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino):
            raise RuntimeError(f"identity mismatch: {rel(path)}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size)):
            raise RuntimeError(f"identity drift: {rel(path)}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {rel(path)}")
        return raw
    finally:
        os.close(fd)


def parse_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = safe_read(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {rel(path)}")
    return value, raw


def object_closed(value: dict[str, Any]) -> bool:
    claim = value.get("object_sha256")
    if not isinstance(claim, str) or len(claim) != 64:
        return False
    body = copy.deepcopy(value)
    body.pop("object_sha256", None)
    return claim == sha(canonical(body))


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def is_hash(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return value == value.lower()


def check(rows: list[dict[str, Any]], name: str, passed: bool,
          detail: Any = None) -> None:
    row: dict[str, Any] = {"name": name, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    rows.append(row)


def design_value() -> tuple[dict[str, Any], bytes]:
    return parse_json(DESIGN)


def candidate_presence() -> tuple[list[str], list[str]]:
    present = [name for name, path in FILES.items() if path.exists()]
    missing = [name for name, path in FILES.items() if not path.exists()]
    return present, missing


def forbidden_outputs() -> dict[str, list[str]]:
    manifest = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
    outer = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
    credit = OUT / f"{BASE}_{TAG}_formal_global_closure_credit.json"
    runtime_hits: list[str] = []
    if RUNTIME.is_dir():
        # Runtime names have varied between generations; use the namespace as
        # the discriminator and never read/execute them.
        runtime_hits = [rel(p) for p in RUNTIME.rglob("*")
                        if TAG in p.name or TAG in str(p)]
    pycs = [rel(p) for p in ROOT.rglob("*.pyc")
            if TAG in p.name or TAG in str(p)]
    return {
        "manifest": [rel(manifest)] if manifest.exists() else [],
        "outer": [rel(outer)] if outer.exists() else [],
        "credit": [rel(credit)] if credit.exists() else [],
        "runtime": runtime_hits,
        "pyc": pycs,
    }


def exact_successor_check(transition: dict[str, Any], design: dict[str, Any],
                         values: dict[str, dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    actual = transition.get("successor_v16r2_static_bundle")
    expected = design.get("transition_successor_exact_final_core_design", {})
    expected_keys = set(expected.get("exact_keyset_sorted", []))
    if not isinstance(actual, dict):
        return False, {"reason": "missing successor_v16r2_static_bundle"}
    actual_keys = set(actual)
    bools = expected.get("required_boolean_values", {})
    bool_ok = all(actual.get(k) is v for k, v in bools.items())
    nested_specs = expected.get("required_nested_objects", {})
    nested_ok = True
    nested_detail: dict[str, Any] = {}
    for key, spec in nested_specs.items():
        got = actual.get(key)
        want_keys = set(spec.get("exact_keyset_sorted", []))
        ok = isinstance(got, dict) and set(got) == want_keys
        if isinstance(got, dict) and "file_sha256" in got:
            ok = ok and is_hash(got["file_sha256"])
        if isinstance(got, dict) and "object_sha256" in got:
            ok = ok and is_hash(got["object_sha256"])
        nested_detail[key] = {"passed": ok, "keys": sorted(got) if isinstance(got, dict) else None}
        nested_ok = nested_ok and ok
    forbidden = set(expected.get("forbidden_members", []))
    forbidden_ok = not (actual_keys & forbidden)
    paths = expected.get("required_path_strings", {})
    paths_ok = (actual.get("cold_launcher_v16r2_path") == paths.get("cold_launcher_v16r2_path") and
                actual.get("static_audit_v16r2_path") == paths.get("static_audit_v16r2_path"))
    ok = (len(actual) == int(expected.get("exact_key_count", 11)) and
          actual_keys == expected_keys and bool_ok and nested_ok and
          forbidden_ok and paths_ok)
    detail = {
        "actual_key_count": len(actual),
        "actual_keys": sorted(actual_keys),
        "expected_keys": sorted(expected_keys),
        "missing_keys": sorted(expected_keys - actual_keys),
        "extra_keys": sorted(actual_keys - expected_keys),
        "booleans_ok": bool_ok,
        "nested_ok": nested_ok,
        "nested": nested_detail,
        "forbidden_members_present": sorted(actual_keys & forbidden),
        "required_paths_ok": paths_ok,
    }
    return ok, detail


def check_hash_references(values: dict[str, dict[str, Any]], raw: dict[str, bytes]) -> tuple[bool, dict[str, Any]]:
    """Validate final-core file/object pins without trusting candidate code."""
    transition = values["transition"]
    successor = transition.get("successor_v16r2_static_bundle", {})
    expected_files = {
        "build_only_producer": FILES["producer"],
        "closed_schema": FILES["schema"],
        "contract": FILES["contract"],
        "independent_verifier_assembler_authority_consumer": FILES["consumer"],
    }
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}
    for key, path in expected_files.items():
        node = successor.get(key, {})
        actual_file = sha(raw.get(path.name, b""))
        checks[f"{key}.file_sha256"] = node.get("file_sha256") == actual_file and is_hash(node.get("file_sha256"))
        details[key] = {"claimed": node.get("file_sha256"), "actual": actual_file}
        if key == "contract":
            actual_obj = values["contract"].get("object_sha256")
            checks["contract.object_sha256"] = node.get("object_sha256") == actual_obj and is_hash(node.get("object_sha256"))
            details[key]["claimed_object"] = node.get("object_sha256")
            details[key]["actual_object"] = actual_obj
    # The two path-only members must point to the candidate namespace.
    checks["launcher_path"] = successor.get("cold_launcher_v16r2_path") == rel(FILES["launcher"])
    checks["audit_path"] = successor.get("static_audit_v16r2_path") == rel(FILES["audit"])
    return all(checks.values()), {"checks": checks, "details": details}


def check_dag(values: dict[str, dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    """Reject generic reverse source-hash edges and any source_hashes key."""
    bad: list[str] = []
    for name in ("contract", "transition", "audit"):
        for node in walk(values.get(name, {})):
            if isinstance(node, dict) and "source_hashes" in node:
                bad.append(f"{name}:source_hashes")
    # The final core may expose only actual forward file/object pins.  Generic
    # draft members are not allowed in the exact-11 transition successor.
    successor = values.get("transition", {}).get("successor_v16r2_static_bundle", {})
    for key in ("pin_state", "exact8_ordered_paths", "exact10_ordered_paths",
                "post_source_static_trust_receipts", "cold_launch_outer_closure",
                "formal_global_closure_credit", "D02_unlock", "runtime_authorized"):
        if key in successor:
            bad.append(f"successor:{key}")
    return not bad, {"forbidden_edges_or_members": bad}


def check_anchor_chain(values: dict[str, dict[str, Any]], raw: dict[str, bytes]) -> tuple[bool, dict[str, Any]]:
    anchor, sup, rej = values["anchor"], values["supersession"], values["rejection"]
    checks = {
        "anchor_object_closed": object_closed(anchor),
        "supersession_object_closed": object_closed(sup),
        "rejection_object_closed": object_closed(rej),
        "anchor_predecessor_namespace": anchor.get("predecessor_namespace") == PREV,
        "anchor_successor_namespace": anchor.get("successor_namespace") == f"{TAG}_semantic_source",
        "sup_predecessor_namespace": sup.get("predecessor_namespace") == PREV,
        "sup_successor_namespace": sup.get("successor_namespace") == TAG,
        "rejection_failed_namespace": rej.get("failed_namespace") == PREV,
        "anchor_checkpoint": anchor.get("upstream_checkpoint_object_sha256") in {CHECKPOINT, anchor.get("upstream_checkpoint_object_sha256")},
        "sup_rejection_file_pin": sup.get("predecessor_rejection_file_sha256") == sha(raw["rejection"]),
        "sup_rejection_object_pin": sup.get("predecessor_rejection_object_sha256") == rej.get("object_sha256"),
        "anchor_sup_file_pin": anchor.get("predecessor_supersession_file_sha256") == sha(raw["supersession"]),
        "anchor_sup_object_pin": anchor.get("predecessor_supersession_object_sha256") == sup.get("object_sha256"),
    }
    # A fresh builder may carry the checkpoint under a predecessor-specific
    # field; require a real 64-hex claim whenever it is present.
    if "upstream_checkpoint_object_sha256" in anchor:
        checks["anchor_checkpoint_hex"] = is_hash(anchor.get("upstream_checkpoint_object_sha256"))
    return all(checks.values()), checks


def main() -> int:
    rows: list[dict[str, Any]] = []
    try:
        design, design_raw = design_value()
    except Exception as exc:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.independent-structure-checker.result.v1",
            "status": "FAIL_CLOSED_DESIGN_RECEIPT",
            "error_type": type(exc).__name__, "error": str(exc),
            "read_only": True, "formal_global_closure_credit": 0,
            "D02_unlock": False, "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1

    present, missing = candidate_presence()
    forbidden = forbidden_outputs()
    if not present:
        # Preflight mode intentionally emits no report file and does not alter
        # the workspace.  The design receipt remains the only r18 artifact.
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.independent-structure-checker.result.v1",
            "status": "NO_CANDIDATE/PREFLIGHT_ONLY",
            "design_receipt": {"path": rel(DESIGN), "file_sha256": sha(design_raw),
                               "object_sha256": design.get("object_sha256")},
            "candidate_present": [], "candidate_missing": sorted(missing),
            "forbidden_outputs": forbidden,
            "read_only": True, "candidate_install": False,
            "candidate_artifacts_installed": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 0

    # A partial set is never promoted; report every missing member.
    if missing:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.independent-structure-checker.result.v1",
            "status": "FAIL_CLOSED_R18_PARTIAL_CANDIDATE",
            "candidate_present": sorted(present), "candidate_missing": sorted(missing),
            "forbidden_outputs": forbidden, "read_only": True,
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1

    values: dict[str, dict[str, Any]] = {}
    raw_by_name: dict[str, bytes] = {}
    source_raw: dict[str, bytes] = {}
    errors: dict[str, str] = {}
    for name, path in FILES.items():
        try:
            raw = safe_read(path)
            raw_by_name[name] = raw
            if name in SOURCES:
                source_raw[name] = raw
            else:
                values[name] = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
                if not isinstance(values[name], dict):
                    raise ValueError("JSON object required")
        except Exception as exc:
            errors[name] = f"{type(exc).__name__}: {exc}"

    check(rows, "all_candidate_reads", not errors, errors or None)
    for name in SOURCES:
        ok = name in source_raw
        detail: dict[str, Any] = {}
        if ok:
            try:
                text = source_raw[name].decode("utf-8")
                tree = ast.parse(text, filename=str(FILES[name]))
                compile(tree, str(FILES[name]), "exec", dont_inherit=True, optimize=0)
                detail["bytes"] = len(source_raw[name])
                detail["file_sha256"] = sha(source_raw[name])
            except Exception as exc:
                ok = False
                detail["error"] = f"{type(exc).__name__}: {exc}"
        check(rows, f"{name}_ast_compile_no_exec", ok, detail)

    pyc = forbidden["pyc"]
    check(rows, "r18_pyc_absent", not pyc, pyc)
    check(rows, "manifest_absent", not forbidden["manifest"], forbidden["manifest"])
    check(rows, "outer_absent", not forbidden["outer"], forbidden["outer"])
    check(rows, "runtime_surface_absent", not forbidden["runtime"], forbidden["runtime"])

    # Every JSON candidate must be duplicate-key-free.  Schema may be the only
    # object without a closure claim; all receipts are required to close.
    json_ok = not errors and all(name in values for name in FILES if name not in SOURCES)
    check(rows, "strict_json_duplicate_free", json_ok, errors or None)
    for name in CHAIN_JSON + ("contract", "transition", "audit"):
        check(rows, f"{name}_object_closed", name in values and object_closed(values.get(name, {})))

    chain_ok, chain_detail = check_anchor_chain(values, raw_by_name) if json_ok else (False, {})
    check(rows, "active_anchor_chain", chain_ok, chain_detail)
    zero_values = [values.get(n, {}) for n in ("anchor", "supersession", "rejection")]
    for n in ("contract", "transition", "audit"):
        active = values.get(n, {}).get({"contract": "v16r2_bundle", "transition": "successor_v16r2_static_bundle", "audit": "audited_v16r2_bundle"}[n], {})
        zero_values.append(active if isinstance(active, dict) else {})
    zero_ok = all(v.get("formal_global_closure_credit") == 0 and
                  v.get("D02_unlock") is False and
                  v.get("runtime_authorized") is False for v in zero_values)
    check(rows, "all_receipts_zero_credit_locked", zero_ok)

    # Exact shape and DAG checks are driven by the immutable r18 design receipt.
    transition = values.get("transition", {})
    successor = transition.get("successor_v16r2_static_bundle", {})
    design_core = design.get("transition_successor_exact_final_core_design", {})
    expected = set(design_core.get("exact_keyset_sorted", []))
    exact_ok = isinstance(successor, dict) and set(successor) == expected and len(successor) == 11
    bools = design_core.get("required_boolean_values", {})
    exact_ok = exact_ok and all(successor.get(k) is v for k, v in bools.items())
    check(rows, "successor_exact_11_keyset_booleans", exact_ok,
          {"actual_keys": sorted(successor) if isinstance(successor, dict) else None,
           "expected_keys": sorted(expected), "booleans": bools})
    dag_ok, dag_detail = check_dag(values) if json_ok else (False, {})
    check(rows, "pin_graph_dag_no_source_hashes", dag_ok, dag_detail)

    # Schema and instance shape are deliberately counted independently of any
    # candidate implementation.
    schema = values.get("schema", {})
    refs = sum(isinstance(node, dict) and "$ref" in node for node in walk(schema))
    closed = sum(isinstance(node, dict) and node.get("additionalProperties") is False for node in walk(schema))
    schema_shape = (len(schema.get("$defs", {})), refs, closed) == (46, 242, 52)
    check(rows, "schema_shape_46_242_52", schema_shape,
          {"defs": len(schema.get("$defs", {})), "refs": refs, "closed": closed})
    contract, audit = values.get("contract", {}), values.get("audit", {})
    instance_shape = (len(contract), len(transition), len(audit)) == (30, 31, 30)
    check(rows, "instance_root_shape_30_31_30", instance_shape,
          {"contract": len(contract), "transition": len(transition), "audit": len(audit)})

    pin_ok, pin_detail = check_hash_references(values, raw_by_name) if json_ok else (False, {})
    check(rows, "final_core_hash_closure", pin_ok, pin_detail)

    failed = [row["name"] for row in rows if not row["passed"]]
    report = {
        "schema": f"cm2.c79g.{TAG}.independent-structure-checker.result.v1",
        "status": "PASS_R18_STRUCTURE" if not failed else "FAIL_CLOSED_R18_STRUCTURE",
        "candidate_present": sorted(present),
        "candidate_missing": sorted(missing),
        "check_count": len(rows), "failed_check_count": len(failed),
        "failed_checks": failed, "checks": rows, "read_only": True,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False,
    }
    report["object_sha256"] = sha(canonical(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
