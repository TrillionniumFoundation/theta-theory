#!/usr/bin/env python3
"""Independent read-only structural checker for the frozen r16 candidate.

This checker does not import, execute, or rewrite any candidate source.  It
reads the r16 namespace with duplicate-key detection, recomputes receipt
object hashes, and emits exactly 34 fail-closed checks.  It is intentionally
separate from the r15 reviewer entrypoint so a wrapper cannot hide a stale
pin or a predecessor-chain defect.
"""

from __future__ import annotations

import ast
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
SUFFIX = "v16r2r16"
PREV = "v16r2r15"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"

FILES = {
    "anchor": OUT / f"{BASE}_{SUFFIX}_active_predecessor_supersession_receipt_v1.json",
    "supersession": OUT / f"{BASE}_{PREV}_to_{SUFFIX}_static_bundle_rejection_supersession_receipt_v1.json",
    "rejection": OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json",
    "schema": OUT / f"{BASE}_schema_{SUFFIX}.json",
    "contract": OUT / f"{BASE}_contract_{SUFFIX}.json",
    "transition": OUT / f"{BASE}_{PREV}_to_{SUFFIX}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{SUFFIX}.json",
    "producer": OUT / f"{BASE}_{SUFFIX}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{SUFFIX}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{SUFFIX}_semantic_source.py",
}
SOURCE_NAMES = ("producer", "consumer", "launcher")
RECEIPT_NAMES = ("anchor", "supersession", "rejection", "contract", "transition", "audit")
JSON_NAMES = (*RECEIPT_NAMES[:3], "schema", *RECEIPT_NAMES[3:])


class DuplicateKey(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


def read_json(name: str) -> dict[str, Any]:
    raw = FILES[name].read_bytes()
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    if not isinstance(value, dict):
        raise ValueError(name + ": non-object")
    return value


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def closed(name: str, value: dict[str, Any]) -> bool:
    claim = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    return isinstance(claim, str) and len(claim) == 64 and sha(canonical(body)) == claim


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def check(rows: list[dict[str, Any]], name: str, passed: bool,
          detail: Any = None) -> None:
    row: dict[str, Any] = {"name": name, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    rows.append(row)


def main() -> int:
    rows: list[dict[str, Any]] = []
    errors: dict[str, str] = {}
    values: dict[str, dict[str, Any]] = {}
    raw: dict[str, bytes] = {}
    text: dict[str, str] = {}

    present = all(path.is_file() for path in FILES.values())
    check(rows, "all_paths_present", present)

    source_regular = all(
        path.is_file() and stat.S_ISREG(path.stat().st_mode) and
        path.stat().st_nlink == 1 for name, path in FILES.items()
        if name in SOURCE_NAMES)
    json_regular = all(
        path.is_file() and stat.S_ISREG(path.stat().st_mode) and
        path.stat().st_nlink == 1 for name, path in FILES.items()
        if name not in SOURCE_NAMES)
    check(rows, "source_regular_nlink1", source_regular)
    check(rows, "json_regular_nlink1", json_regular)

    source_modes = all(stat.S_IMODE(FILES[name].stat().st_mode) in {0o644, 0o664}
                       for name in SOURCE_NAMES)
    json_modes = all(stat.S_IMODE(FILES[name].stat().st_mode) in {0o644, 0o664}
                     for name in ("schema", "contract", "transition", "audit"))
    frozen_modes = all(stat.S_IMODE(FILES[name].stat().st_mode) == 0o444 and
                       FILES[name].stat().st_nlink == 1
                       for name in ("anchor", "supersession", "rejection"))
    check(rows, "source_draft_modes", source_modes)
    check(rows, "json_draft_modes", json_modes)
    check(rows, "frozen_receipt_modes", frozen_modes)

    utf8 = True
    ast_ok = True
    for name in SOURCE_NAMES:
        try:
            raw[name] = FILES[name].read_bytes()
            text[name] = raw[name].decode("utf-8")
            ast.parse(text[name], filename=str(FILES[name]))
        except Exception as exc:
            utf8 = ast_ok = False
            errors[name] = f"{type(exc).__name__}: {exc}"
    check(rows, "source_utf8", utf8)
    check(rows, "source_ast_parse", ast_ok, errors or None)

    pycs = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc")
            if SUFFIX in path.name or SUFFIX in str(path)]
    check(rows, "r16_pyc_absent", not pycs, pycs)
    manifest = OUT / f"{BASE}_cold_launch_manifest_{SUFFIX}.sha256"
    outer = OUT / f"{BASE}_cold_launch_outer_receipt_{SUFFIX}.json"
    check(rows, "manifest_absent", not manifest.exists())
    check(rows, "outer_absent", not outer.exists())
    runtime_hits = []
    if RUNTIME.exists():
        runtime_hits = [str(p.relative_to(ROOT)) for p in RUNTIME.glob(
            f"c79g-{SUFFIX}-*")] + [str(p.relative_to(ROOT)) for p in RUNTIME.glob(
            f".{SUFFIX}-*")]
    check(rows, "r16_runtime_surfaces_absent", not runtime_hits, runtime_hits)

    json_ok = True
    for name in JSON_NAMES:
        try:
            values[name] = read_json(name)
        except Exception as exc:
            json_ok = False
            errors[name] = f"{type(exc).__name__}: {exc}"
    check(rows, "strict_json_receipts", json_ok and len(values) == len(JSON_NAMES), errors or None)

    check(rows, "anchor_object_closed", "anchor" in values and closed("anchor", values["anchor"]))
    check(rows, "supersession_object_closed", "supersession" in values and closed("supersession", values["supersession"]))
    check(rows, "rejection_object_closed", "rejection" in values and closed("rejection", values["rejection"]))

    anchor = values.get("anchor", {})
    sup = values.get("supersession", {})
    rejection = values.get("rejection", {})
    chain_ok = (
        anchor.get("predecessor_namespace") == PREV and
        anchor.get("successor_namespace") == f"{SUFFIX}_semantic_source" and
        anchor.get("predecessor_supersession_path") == rel(FILES["supersession"]) and
        sup.get("predecessor_namespace") == PREV and
        sup.get("successor_namespace") == SUFFIX and
        sup.get("predecessor_rejection_path") == rel(FILES["rejection"]) and
        rejection.get("failed_namespace") == PREV and
        anchor.get("upstream_checkpoint_object_sha256") == UPSTREAM and
        anchor.get("successor_checkpoint_object_sha256") == CHECKPOINT)
    check(rows, "active_anchor_chain", chain_ok)

    credit_zero = all(
        value.get("formal_global_closure_credit") == 0 and
        value.get("D02_unlock") is False and
        value.get("runtime_authorized") is False
        for value in (anchor, sup, rejection))
    check(rows, "predecessor_zero_credit", credit_zero)

    schema = values.get("schema", {})
    contract = values.get("contract", {})
    transition = values.get("transition", {})
    audit = values.get("audit", {})
    active_contract = contract.get("v16r2_bundle", {})
    active_transition = transition.get("successor_v16r2_static_bundle", {})
    active_audit = audit.get("audited_v16r2_bundle", {})
    successor_zero = all(
        value.get("formal_global_closure_credit") == 0 and
        value.get("D02_unlock") is False and
        value.get("runtime_authorized") is False
        for value in (active_contract, active_transition, active_audit))
    check(rows, "successor_zero_credit", successor_zero)

    allowed_root = {"$schema", "$id", "$comment", "title", "description", "$defs", "$ref"}
    schema_root = (set(schema) <= allowed_root and "object_sha256" not in schema and
                   not any(key.startswith("x-cm2-") for key in schema))
    check(rows, "schema_root_allowed", schema_root, sorted(set(schema) - allowed_root))
    check(rows, "schema_root_ref", schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority")
    refs = sum(isinstance(node, dict) and "$ref" in node for node in walk(schema))
    closed_count = sum(isinstance(node, dict) and
                       node.get("additionalProperties") is False for node in walk(schema))
    check(rows, "schema_full_shape", (len(schema.get("$defs", {})), refs, closed_count) == (46, 242, 52),
          {"defs": len(schema.get("$defs", {})), "refs": refs, "closed": closed_count})

    root_shapes = (len(contract), len(transition), len(audit)) == (30, 31, 30)
    check(rows, "instance_root_shapes", root_shapes,
          {"contract": len(contract), "transition": len(transition), "audit": len(audit)})
    active_keysets = (len(active_contract) == 28 and
                      set(active_contract) == set(active_transition) ==
                      set(active_audit))
    check(rows, "active_bundle_keysets", active_keysets,
          {"contract": len(active_contract), "transition": len(active_transition),
           "audit": len(active_audit)})
    check(rows, "contract_object_closed", closed("contract", contract))
    check(rows, "transition_object_closed", closed("transition", transition))
    check(rows, "audit_object_closed", closed("audit", audit))

    source_hashes = {name: sha(raw.get(name, b"")) for name in SOURCE_NAMES}
    source_pin_ok = all(active.get("source_hashes") == source_hashes
                        for active in (active_contract, active_transition, active_audit))
    check(rows, "three_source_hashes_match", source_pin_ok,
          {"actual": source_hashes, "contract": active_contract.get("source_hashes")})

    expected8 = [rel(FILES[name]) for name in
                 ("anchor", "schema", "contract", "producer", "consumer",
                  "transition", "audit", "launcher")]
    expected10 = expected8 + [rel(manifest), rel(outer)]
    check(rows, "exact8_order", active_contract.get("exact8_ordered_paths") == expected8,
          {"actual": active_contract.get("exact8_ordered_paths"), "expected": expected8})
    check(rows, "exact10_order", active_contract.get("exact10_ordered_paths") == expected10)

    schema_file_sha = sha(FILES["schema"].read_bytes())
    nested_schema = active_contract.get("closed_schema", {})
    nested_value = nested_schema.get("file_sha256")
    nested_pin_policy = (
        nested_value == schema_file_sha or
        (isinstance(nested_value, str) and nested_value.startswith("UNPINNED_") and
         "PINS_UNINSTALLED" in str(active_contract.get("pin_state", ""))))
    check(rows, "nested_closed_schema_pin_policy",
          nested_pin_policy and active_contract.get("schema_file_sha256") == schema_file_sha,
          {"actual": nested_value, "expected": schema_file_sha,
           "draft_sentinel_allowed": True})

    trust = active_contract.get("post_source_static_trust_receipts", {})
    trust_ok = (trust.get("predecessor_supersession_path") == rel(FILES["anchor"]) and
                trust.get("static_audit_path") == rel(FILES["audit"]) and
                trust.get("v16_to_v16r2_transition_path") == rel(FILES["transition"]) and
                trust.get("v14_official_rejection_path") ==
                ".cm2-runtime/c79g-v14-rejections-" + CHECKPOINT + "/rejection.json" and
                trust.get("runtime_consumer_must_hold_strict_parse_object_close_and_terminally_replay_inherited_v14_exact12") is True)
    check(rows, "trust_receipt_paths", trust_ok, trust)

    baseline = audit.get("schema_and_constructor_closure", {}).get("global_consumer_baseline", {})
    public_schema_zero = any(isinstance(node, dict) and
                             node.get("public_global_unresolved") == {"const": 0}
                             for node in walk(schema))
    public_ok = (baseline.get("input_rows") == 76832 and
                 baseline.get("current_public_unresolved") == 1148 and
                 public_schema_zero)
    check(rows, "public_baseline_and_schema_zero", public_ok, baseline)

    protocol_ok = (
        contract.get("schema") == "cm2.round306c79g.true-global-no-producer-consumer.v16r2.contract" and
        transition.get("schema") == "cm2.round306c79g.true-global-no-producer-consumer.v16-to-v16r2-static-launch-transition.v1" and
        transition.get("transition_kind") ==
        "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR" and
        audit.get("schema") == "cm2.round306c79g.true-global-no-producer-consumer.static-audit.v16r2" and
        all("v16-to-v16r2-static-launch-transition.v1" in text.get(name, "")
            for name in SOURCE_NAMES) and
        all(fragment in text.get(name, "") for name in SOURCE_NAMES
            for fragment in ("APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_",
                             "ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR")) and
        all(f"{SUFFIX}_to_{SUFFIX}" not in text.get(name, "") for name in SOURCE_NAMES))
    check(rows, "generic_runtime_protocol", protocol_ok)

    if len(rows) != 34:
        raise RuntimeError(f"checker row drift: {len(rows)}")
    failed = [row["name"] for row in rows if not row["passed"]]
    report = {
        "schema": f"cm2.c79g.{SUFFIX}.independent-structure-checker-b.v1",
        "successor_suffix": SUFFIX,
        "predecessor_suffix": PREV,
        "check_count": len(rows),
        "failed_check_count": len(failed),
        "failed_checks": failed,
        "status": "PASS_34_OF_34" if not failed else "FAIL_CLOSED_STRUCTURE_B",
        "read_only": True,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "checks": rows,
    }
    report["object_sha256"] = sha(canonical(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
