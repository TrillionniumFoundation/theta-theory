#!/usr/bin/env python3
"""Parameterized, read-only 34-check reviewer for a C79g static DAG.

The reviewer only reads installed bytes and performs AST/JSON checks in
memory.  It never imports or executes a candidate source and never creates a
manifest, outer receipt, runtime surface, credit, or ``.pyc`` file.  The
successor and predecessor namespaces are supplied by environment variables so
the same reviewer can be used for an append-only r20, r21, ... attempt.

The companion shell gate is intentionally responsible for the normative
``jq -e`` predicate.  This program still returns non-zero whenever one of the
34 checks fails, and it emits a report even when inputs are missing or
malformed.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import symtable
import sys
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
SUFFIX_RAW = os.environ.get("CM2_SUCCESSOR_SUFFIX", "v16r2r20")
PREV_RAW = os.environ.get("CM2_PREDECESSOR_SUFFIX", "v16r2r19")
# Do not allow an environment value to escape deliverables through ``..`` or
# a path separator.  Invalid values are mapped to an inert name and are still
# reported as a failed check below.
COMPONENT = re.compile(r"^[A-Za-z0-9_-]+$")
SUFFIX_OK = bool(COMPONENT.fullmatch(SUFFIX_RAW)) and SUFFIX_RAW not in {".", ".."}
PREV_OK = bool(COMPONENT.fullmatch(PREV_RAW)) and PREV_RAW not in {".", ".."}
SUFFIX = SUFFIX_RAW if SUFFIX_OK else "__invalid_successor__"
PREV = PREV_RAW if PREV_OK else "__invalid_predecessor__"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

SOURCE_PATHS = {
    "producer": OUT / f"{BASE}_{SUFFIX}_semantic_source.py",
    "consumer": OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_"
        f"{SUFFIX}_semantic_source.py"),
    "launcher": OUT / f"{BASE}_cold_launch_{SUFFIX}_semantic_source.py",
}
JSON_PATHS = {
    "schema": OUT / f"{BASE}_schema_{SUFFIX}.json",
    "contract": OUT / f"{BASE}_contract_{SUFFIX}.json",
    "transition": OUT / (
        f"{BASE}_{PREV}_to_{SUFFIX}_static_launch_transition_receipt_v1.json"),
    "audit": OUT / f"{BASE}_static_audit_{SUFFIX}.json",
}
CHAIN_PATHS = {
    "anchor": OUT / (
        f"{BASE}_{SUFFIX}_active_predecessor_supersession_receipt_v1.json"),
    "rejection": OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json",
    "supersession": OUT / (
        f"{BASE}_{PREV}_to_{SUFFIX}_static_bundle_rejection_"
        "supersession_receipt_v1.json"),
}
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{SUFFIX}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{SUFFIX}.json"

ALL_PATHS = {
    **CHAIN_PATHS,
    **JSON_PATHS,
    **SOURCE_PATHS,
}

# Keep this tuple immutable: CI and downstream consumers rely on exactly 34
# rows, in this order, regardless of which input is missing.
CHECK_NAMES = (
    "namespace_parameters_safe",
    "all_static_paths_present",
    "source_regular_nlink1",
    "source_modes",
    "ast_parse",
    "compile_in_memory",
    "utf8_and_no_stale_tokens",
    "successor_tokens_and_active_namespace",
    "active_graph_consensus",
    "nearest_predecessor_closed",
    "checkpoint_derivation",
    "no_old_active_transition",
    "runtime_disabled",
    "final_flags_consistent",
    "no_candidate_pyc",
    "no_runtime_surfaces",
    "manifest_absent",
    "outer_absent",
    "source_hashes_distinct",
    "source_hashes_stable",
    "no_starred_calls",
    "no_double_star_calls",
    "no_duplicate_literal_keys",
    "no_dangerous_calls",
    "symtable",
    "json_strict_and_closed",
    "schema_full_shape",
    "instance_shapes_closed",
    "zero_credit_baseline",
    "exact8_order",
    "exact11_transition_and_no_generic_edges",
    "source_pin_consistency",
    "predecessor_chain_closed",
    "final_pin_crosscheck",
)


class DuplicateKey(ValueError):
    """Raised when a JSON object repeats a key."""


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


def stable(path: Path) -> bytes:
    """Read one immutable regular file while checking identity before/after."""
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named_before = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named_before.st_dev, named_before.st_ino, named_before.st_size)):
            raise ValueError(f"not regular/nlink1 or identity drift: {path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise ValueError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise ValueError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def closed(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    claim = value.get("object_sha256")
    if not isinstance(claim, str) or not HEX64.fullmatch(claim):
        return False
    body = dict(value)
    body.pop("object_sha256", None)
    return sha(canonical(body)) == claim


def load_json(path: Path, require_object: bool = True) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    def reject_constant(token: str) -> None:
        raise ValueError(f"non-standard JSON constant: {token}")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=strict_pairs,
                       parse_constant=reject_constant)
    if require_object and not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value, raw


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def call_counts(tree: ast.AST) -> tuple[int, int, int, int]:
    starred = double = dangerous = duplicate = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            starred += sum(isinstance(arg, ast.Starred) for arg in node.args)
            double += sum(keyword.arg is None for keyword in node.keywords)
            if (isinstance(node.func, ast.Name) and
                    node.func.id in {"eval", "exec", "__import__"}):
                dangerous += 1
        elif isinstance(node, ast.Dict):
            keys = [key.value for key in node.keys
                    if isinstance(key, ast.Constant) and
                    isinstance(key.value, str)]
            duplicate += len(keys) - len(set(keys))
    return starred, double, dangerous, duplicate


def add(rows: list[dict[str, Any]], name: str, passed: bool,
        detail: Any = None) -> None:
    row: dict[str, Any] = {"name": name, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    rows.append(row)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def resolve_repo_path(value: Any) -> Path | None:
    """Resolve a receipt path, rejecting absolute paths and traversal."""
    if not isinstance(value, str) or not value or value.startswith("/"):
        return None
    candidate = (ROOT / value).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def all_zero_credit(values: list[Any]) -> bool:
    for value in values:
        for node in walk(value):
            if not isinstance(node, dict):
                continue
            if node.get("formal_global_closure_credit", 0) not in (0, False, None):
                return False
            if node.get("all_persisted_credit", 0) not in (0, False, None):
                return False
            if node.get("D02_unlock") is True:
                return False
    return True


def flag_values(text: str, name: str) -> list[str]:
    return re.findall(rf"(?m)^{re.escape(name)}\s*=\s*(True|False)\s*$",
                      text)


def literal_pin(text: str, name: str) -> list[str]:
    return re.findall(rf"(?m)^{re.escape(name)}\s*=\s*\"([0-9a-f]{{64}})\"\s*$",
                      text)


def child_dict(value: Any, key: str) -> dict[str, Any]:
    """Return a nested object or an inert empty object on malformed input."""
    if not isinstance(value, dict):
        return {}
    child = value.get(key, {})
    return child if isinstance(child, dict) else {}


def main() -> int:
    rows: list[dict[str, Any]] = []
    raw: dict[str, bytes] = {}
    values: dict[str, dict[str, Any]] = {}
    texts: dict[str, str] = {}
    trees: dict[str, ast.Module] = {}
    errors: dict[str, str] = {}

    # 1. Namespace safety is a check, not a process-level exception.
    add(rows, "namespace_parameters_safe", SUFFIX_OK and PREV_OK and
        SUFFIX != PREV, {"successor": SUFFIX_RAW, "predecessor": PREV_RAW})

    # 2. Read all expected bytes.  Missing/malformed inputs are represented in
    # later checks rather than aborting the report.
    add(rows, "all_static_paths_present", all(path.is_file()
        for path in ALL_PATHS.values()) and not MANIFEST.exists() and not OUTER.exists(),
        {name: str(path.relative_to(ROOT)) for name, path in ALL_PATHS.items()})
    for name, path in ALL_PATHS.items():
        try:
            if path.suffix == ".json":
                value, blob = load_json(path)
                values[name] = value
                raw[name] = blob
            else:
                raw[name] = stable(path)
        except Exception as exc:
            errors[name] = f"{type(exc).__name__}: {exc}"
    for role, path in SOURCE_PATHS.items():
        try:
            texts[role] = raw[role].decode("utf-8")
            trees[role] = ast.parse(texts[role], filename=str(path))
        except Exception as exc:
            errors[f"{role}_ast"] = f"{type(exc).__name__}: {exc}"

    # 3-4. Source identity and mode checks.
    regular = modes = True
    for role, path in SOURCE_PATHS.items():
        try:
            state = path.stat()
            regular &= stat.S_ISREG(state.st_mode) and state.st_nlink == 1
            # Source members are writable during the draft/static phase, then
            # become immutable 0444 members during the physical exact8
            # freeze.  Accept both phases while retaining the strict regular
            # file + nlink=1 identity gate.
            modes &= stat.S_IMODE(state.st_mode) in {0o444, 0o644, 0o664}
        except OSError:
            regular = modes = False
    add(rows, "source_regular_nlink1", regular)
    add(rows, "source_modes", modes)

    # 5-6. AST parse and in-memory compile only.
    add(rows, "ast_parse", len(trees) == 3, errors)
    compile_ok = len(trees) == 3
    for role, tree in trees.items():
        try:
            compile(tree, str(SOURCE_PATHS[role]), "exec")
        except Exception as exc:
            compile_ok = False
            errors[f"{role}_compile"] = f"{type(exc).__name__}: {exc}"
    add(rows, "compile_in_memory", compile_ok)

    # 7-8. Namespace/path literals are checked textually; source is never
    # imported.  Historical v16/r15 active paths are forbidden in a fresh DAG.
    utf8 = len(texts) == 3
    stale = any("v15" in text.lower() or "v16r2r15" in text.lower() or
                "v16r2r16" in text.lower() for text in texts.values())
    add(rows, "utf8_and_no_stale_tokens", utf8 and not stale,
        {"utf8": utf8, "stale": stale})
    expected_anchor_name = CHAIN_PATHS["anchor"].name
    expected_transition_name = JSON_PATHS["transition"].name
    token_ok = (len(texts) == 3 and all(SUFFIX in text and
                 expected_anchor_name in text and
                 expected_transition_name in text for text in texts.values()))
    ns_values: list[str] = []
    for text in texts.values():
        ns_values.extend(re.findall(r"(?m)^ACTIVE_SUCCESSOR_NAMESPACE\s*=\s*\"([^\"]+)\"\s*$", text))
    token_ok = token_ok and len(ns_values) == 3 and set(ns_values) == {f"{SUFFIX}_semantic_source"}
    add(rows, "successor_tokens_and_active_namespace", token_ok,
        {"namespaces": ns_values, "anchor": expected_anchor_name,
         "transition": expected_transition_name})

    # 9. Every source must agree on the same active anchor and successor.
    pred_literals: list[str] = []
    for text in texts.values():
        pred_literals.extend(re.findall(
            r"(?m)^ACTIVE_PREDECESSOR_SUPERSESSION\s*=\s*OUT\s*/\s*\"([^\"]+)\"\s*$",
            text))
    graph_ok = (len(pred_literals) == 3 and set(pred_literals) == {expected_anchor_name} and
                len(ns_values) == 3 and set(ns_values) == {f"{SUFFIX}_semantic_source"})
    add(rows, "active_graph_consensus", graph_ok,
        {"predecessor_literals": pred_literals, "namespaces": ns_values})

    anchor = values.get("anchor", {})
    rejection = values.get("rejection", {})
    supersession = values.get("supersession", {})

    # 10. Verify the entire immutable predecessor rejection -> supersession ->
    # anchor chain, including object/file hashes and namespace direction.
    chain_ok = False
    chain_detail: dict[str, Any] = {}
    try:
        if not all(closed(x) for x in (anchor, rejection, supersession)):
            raise ValueError("anchor/rejection/supersession object closure")
        expected_rej_path = rel(CHAIN_PATHS["rejection"])
        expected_sup_path = rel(CHAIN_PATHS["supersession"])
        chain_ok = (
            anchor.get("predecessor_namespace") == PREV and
            anchor.get("successor_namespace") == f"{SUFFIX}_semantic_source" and
            anchor.get("predecessor_supersession_path") == expected_sup_path and
            supersession.get("predecessor_namespace") == PREV and
            supersession.get("successor_namespace") == SUFFIX and
            supersession.get("predecessor_rejection_path") == expected_rej_path and
            rejection.get("failed_namespace") == PREV and
            rejection.get("formal_global_closure_credit") == 0 and
            rejection.get("D02_unlock") is False and
            rejection.get("runtime_authorized") is False and
            supersession.get("formal_global_closure_credit") == 0 and
            supersession.get("D02_unlock") is False and
            supersession.get("runtime_authorized") is False and
            anchor.get("formal_global_closure_credit") == 0 and
            anchor.get("D02_unlock") is False and
            anchor.get("runtime_authorized") is False and
            sha(raw.get("rejection", b"")) == supersession.get("predecessor_rejection_file_sha256") and
            rejection.get("object_sha256") == supersession.get("predecessor_rejection_object_sha256") and
            sha(raw.get("supersession", b"")) == anchor.get("predecessor_supersession_file_sha256") and
            supersession.get("object_sha256") == anchor.get("predecessor_supersession_object_sha256"))
        chain_detail = {"expected_rejection": expected_rej_path,
                        "expected_supersession": expected_sup_path}
    except Exception as exc:
        chain_detail = {"error": f"{type(exc).__name__}: {exc}"}
    add(rows, "nearest_predecessor_closed", chain_ok, chain_detail)

    # 11. Both pinned checkpoints must be present in the immutable chain.
    checkpoint_ok = (UPSTREAM in json.dumps(anchor, sort_keys=True) and
                     CHECKPOINT in json.dumps(anchor, sort_keys=True) and
                     UPSTREAM in json.dumps(supersession, sort_keys=True) and
                     CHECKPOINT in json.dumps(supersession, sort_keys=True))
    add(rows, "checkpoint_derivation", checkpoint_ok,
        {"upstream": UPSTREAM, "successor": CHECKPOINT})

    # 12. No source may retain the old active transition edge.
    old_edge = f"{BASE}_v16r2r15_to_v16r2r16_static_launch_transition_receipt_v1.json"
    add(rows, "no_old_active_transition", len(texts) == 3 and all(
        old_edge not in text and "v16r2r16_active_predecessor" not in text
        for text in texts.values()))

    # 13-14. Runtime/credit remain disabled and all role-specific final pins
    # are true (duplicate inherited assignments are accepted only if every
    # assignment is true, never a mixed true/false state).
    runtime_ok = len(texts) == 3 and all(
        "RUNTIME_AUTHORIZED = False" in text and
        "FORMAL_GLOBAL_CLOSURE_CREDIT = 0" in text and
        "D02_UNLOCK = False" in text and
        "RUNTIME_AUTHORIZED = True" not in text for text in texts.values())
    add(rows, "runtime_disabled", runtime_ok)
    role_flags = {
        "producer": "FINAL_V16R2_CORE_PINS_INSTALLED",
        "consumer": "FINAL_CURRENT_V16R2_PINS_INSTALLED",
        "launcher": "FINAL_BASE7_PINS_INSTALLED",
    }
    flag_detail: dict[str, list[str]] = {}
    flags_ok = True
    for role, flag in role_flags.items():
        vals = flag_values(texts.get(role, ""), flag)
        flag_detail[role] = vals
        flags_ok &= bool(vals) and all(value == "True" for value in vals)
    add(rows, "final_flags_consistent", flags_ok, flag_detail)

    # 15-18. No generated pyc/runtime/manifest/outer surfaces.
    pycs = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc")
            if SUFFIX_RAW in str(path)]
    add(rows, "no_candidate_pyc", not pycs, pycs)
    runtime_hits = []
    if RUNTIME.exists():
        runtime_hits = [str(path.relative_to(ROOT)) for path in RUNTIME.rglob("*")
                        if SUFFIX_RAW in str(path) and path.is_file()]
    add(rows, "no_runtime_surfaces", not runtime_hits, runtime_hits)
    add(rows, "manifest_absent", not MANIFEST.exists())
    add(rows, "outer_absent", not OUTER.exists())

    # 19-20. Source bytes are distinct and stable under a second descriptor
    # read.  Hashes are kept local; this reviewer never writes a pin.
    source_hashes = {role: sha(raw[role]) for role in SOURCE_PATHS if role in raw}
    add(rows, "source_hashes_distinct", len(source_hashes) == 3 and
        len(set(source_hashes.values())) == 3, source_hashes)
    stable_again = len(source_hashes) == 3
    for role, path in SOURCE_PATHS.items():
        try:
            stable_again &= stable(path) == raw.get(role, b"")
        except Exception:
            stable_again = False
    add(rows, "source_hashes_stable", stable_again)

    # 21-25. Pure AST census (never executes source).
    counts = [call_counts(tree) for tree in trees.values()]
    sums = [sum(item[index] for item in counts) for index in range(4)] if counts else [1, 1, 1, 1]
    add(rows, "no_starred_calls", sums[0] == 0, sums[0])
    add(rows, "no_double_star_calls", sums[1] == 0, sums[1])
    add(rows, "no_duplicate_literal_keys", sums[3] == 0, sums[3])
    add(rows, "no_dangerous_calls", sums[2] == 0, sums[2])
    sym_ok = len(texts) == 3
    for role, text in texts.items():
        try:
            symtable.symtable(text, str(SOURCE_PATHS[role]), "exec")
        except Exception:
            sym_ok = False
    add(rows, "symtable", sym_ok)

    # 26. Strict JSON parsing, duplicate-key rejection, and object closure for
    # every receipt.  The schema is deliberately a plain closed JSON document
    # without an object_sha256 field, matching the builder contract.
    required_receipts = ("anchor", "rejection", "supersession", "contract",
                         "transition", "audit")
    json_ok = (all(name in values for name in ("schema", *required_receipts)) and
               all(isinstance(values.get(name), dict) for name in ("schema", *required_receipts)) and
               all(closed(values[name]) for name in required_receipts))
    add(rows, "json_strict_and_closed", json_ok, errors)

    schema = values.get("schema", {})
    contract = values.get("contract", {})
    transition = values.get("transition", {})
    audit = values.get("audit", {})

    # 27-29. Schema/instance shapes and zero-credit baseline.
    refs = sum(1 for node in walk(schema)
               if isinstance(node, dict) and "$ref" in node)
    closed_count = sum(1 for node in walk(schema)
                       if isinstance(node, dict) and
                       node.get("additionalProperties") is False)
    schema_ok = (len(schema.get("$defs", {})) == 46 and refs == 242 and
                 closed_count == 52 and
                 schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority" and
                 "coldLaunchedCommittedAuthority" in schema.get("$defs", {}))
    add(rows, "schema_full_shape", schema_ok,
        {"defs": len(schema.get("$defs", {})), "refs": refs,
         "closed": closed_count})
    add(rows, "instance_shapes_closed",
        len(contract) == 30 and len(transition) == 31 and len(audit) == 30 and
        all(closed(values.get(name, {})) for name in ("contract", "transition", "audit")))
    closure = audit.get("schema_and_constructor_closure", {})
    closure = closure if isinstance(closure, dict) else {}
    baseline = closure.get("global_consumer_baseline", {})
    baseline = baseline if isinstance(baseline, dict) else {}
    if not baseline:
        baseline = child_dict(schema, "x-cm2-successor-active").get(
            "global_baseline", {})
        baseline = baseline if isinstance(baseline, dict) else {}
    if not baseline:
        baseline = child_dict(schema, "x-cm2-v16r2-active-successor").get(
            "global_baseline", {})
        baseline = baseline if isinstance(baseline, dict) else {}
    public_zero = any(
        isinstance(node, dict) and
        isinstance(node.get("public_global_unresolved"), dict) and
        node["public_global_unresolved"].get("const") == 0
        for node in walk(schema))
    parent_count = any(
        isinstance(node, dict) and
        (node.get("C42_parent_count") == 862 or
         node.get("validates_reflection_parent_rows") == 862)
        for node in walk(contract)) or any(
        isinstance(node, dict) and
        (node.get("C42_parent_count") == 862 or
         node.get("validates_reflection_parent_rows") == 862)
        for node in walk(audit))
    schema_instance = {key: value for key, value in schema.items()
                       if key != "$defs"}
    baseline_ok = (baseline.get("input_rows", baseline.get("rows")) == 76832 and
                   baseline.get("current_public_unresolved",
                                baseline.get("unresolved")) == 1148 and
                   public_zero and parent_count and
                   all_zero_credit([schema_instance, contract, transition, audit, anchor,
                                    rejection, supersession]))
    add(rows, "zero_credit_baseline", baseline_ok,
        {"baseline": baseline, "public_zero": public_zero,
         "parent_count_862": parent_count})

    # 30. Exact8 must begin at the newly sealed anchor and preserve the DAG
    # order; no manifest/outer member is permitted before cold freeze.
    expected8 = [rel(CHAIN_PATHS["anchor"]), rel(JSON_PATHS["schema"]),
                 rel(JSON_PATHS["contract"]), rel(SOURCE_PATHS["producer"]),
                 rel(SOURCE_PATHS["consumer"]), rel(JSON_PATHS["transition"]),
                 rel(JSON_PATHS["audit"]), rel(SOURCE_PATHS["launcher"])]
    bundle = contract.get("v16r2_bundle", {})
    exact8_ok = (isinstance(bundle, dict) and
                 bundle.get("exact8_ordered_paths") == expected8 and
                 bundle.get("base7_ordered_paths") == expected8[:-1])
    add(rows, "exact8_order", exact8_ok,
        {"actual": bundle.get("exact8_ordered_paths"), "expected": expected8})

    # 31. The transition successor must be exactly the fresh 11-key witness,
    # and no generic source_hashes edge may survive in active bundles.
    successor_value = transition.get("successor_v16r2_static_bundle", {})
    successor = successor_value if isinstance(successor_value, dict) else {}
    expected11 = {
        "all_four_core_file_pins_final", "build_only_producer", "closed_schema",
        "cold_launcher_v16r2_path", "contract", "draft_pin_sentinels_remain_present",
        "final_consumer_pin_installed",
        "independent_verifier_assembler_authority_consumer", "static_audit_v16r2_path",
        "transition_receipt_bytes_are_closed_around_final_core_pins",
        "transition_receipt_physical_freeze_completed",
    }
    no_generic = not any(isinstance(node, dict) and "source_hashes" in node
                         for value in (contract, transition, audit)
                         for node in walk(value))
    boundary = child_dict(transition, "cold_launch_boundary")
    boundary_order = boundary.get("base7_order")
    boundary_ok = (boundary.get("base7_first_member_path") == expected8[0] and
                   boundary_order == expected8[:-1] and
                   not any(isinstance(item, str) and
                           item.startswith("deliverables/deliverables/")
                           for item in (boundary_order if isinstance(boundary_order, list) else [])))
    exact11_ok = (isinstance(successor, dict) and set(successor) == expected11 and
                  successor.get("draft_pin_sentinels_remain_present") is False and
                  no_generic and boundary_ok)
    add(rows, "exact11_transition_and_no_generic_edges", exact11_ok,
        {"keys": sorted(successor) if isinstance(successor, dict) else None,
         "no_generic": no_generic, "boundary_ok": boundary_ok})

    # 32. Verify JSON hash/path pins against the bytes read above.
    json_hashes = {name: sha(raw[name]) for name in ALL_PATHS if name in raw}
    cb = bundle if isinstance(bundle, dict) else {}
    audited_value = audit.get("audited_v16r2_bundle", {})
    audited = audited_value if isinstance(audited_value, dict) else {}
    pin_json_ok = (
        cb.get("schema_file_sha256") == json_hashes.get("schema") and
        child_dict(cb, "closed_schema").get("file_sha256") == json_hashes.get("schema") and
        child_dict(cb, "predecessor_semantic_supersession").get("file_sha256") == json_hashes.get("anchor") and
        child_dict(cb, "predecessor_semantic_supersession").get("object_sha256") == anchor.get("object_sha256") and
        child_dict(successor, "build_only_producer").get("file_sha256") == source_hashes.get("producer") and
        child_dict(successor, "closed_schema").get("file_sha256") == json_hashes.get("schema") and
        child_dict(successor, "contract").get("file_sha256") == json_hashes.get("contract") and
        child_dict(successor, "contract").get("object_sha256") == contract.get("object_sha256") and
        child_dict(successor, "independent_verifier_assembler_authority_consumer").get("file_sha256") == source_hashes.get("consumer") and
        audited.get("transition_file_sha256") == json_hashes.get("transition") and
        audited.get("transition_object_sha256") == transition.get("object_sha256") and
        child_dict(audited, "build_only_producer").get("file_sha256") == source_hashes.get("producer") and
        child_dict(audited, "independent_verifier_assembler_authority_consumer").get("file_sha256") == source_hashes.get("consumer"))
    add(rows, "source_pin_consistency", pin_json_ok)

    # 33. The contract/audit paths must point at the same chain and the active
    # predecessor must be the first exact8 member.  This is intentionally
    # separate from the raw chain check to catch a stale-but-closed receipt.
    exact8_actual = cb.get("exact8_ordered_paths") if isinstance(cb, dict) else None
    exact8_first = (exact8_actual[0] if isinstance(exact8_actual, list) and
                    exact8_actual else None)
    chain_path_ok = (
        exact8_first == rel(CHAIN_PATHS["anchor"]) and
        child_dict(cb, "predecessor_semantic_supersession").get("path") == rel(CHAIN_PATHS["anchor"]) and
        child_dict(audited, "predecessor_semantic_supersession").get("path") == rel(CHAIN_PATHS["anchor"]) and
        transition.get("receipt_path") == rel(JSON_PATHS["transition"]) and
        audit.get("audit_path") == rel(JSON_PATHS["audit"]))
    add(rows, "predecessor_chain_closed", chain_ok)

    # 34. Textual source constants must close the DAG.  Launcher self-hash is
    # deliberately excluded: its seven upstream pins are acyclic, while its
    # own hash cannot be embedded without a self-referential fixed point.
    producer = texts.get("producer", "")
    consumer = texts.get("consumer", "")
    launcher = texts.get("launcher", "")
    contract_obj = contract.get("object_sha256")
    source_pin_ok = (
        literal_pin(producer, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN") == [json_hashes.get("anchor")] and
        literal_pin(producer, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN") == [anchor.get("object_sha256")] and
        literal_pin(producer, "CONTRACT_FILE_PIN") == [json_hashes.get("contract")] and
        literal_pin(producer, "CONTRACT_OBJECT_PIN") == [contract_obj] and
        literal_pin(producer, "CLOSED_SCHEMA_FILE_PIN") == [json_hashes.get("schema")] and
        literal_pin(consumer, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN") == [json_hashes.get("anchor")] and
        literal_pin(consumer, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN") == [anchor.get("object_sha256")] and
        literal_pin(consumer, "PRODUCER_SOURCE_PIN") == [source_hashes.get("producer")] and
        literal_pin(consumer, "CONTRACT_FILE_PIN") == [json_hashes.get("contract")] and
        literal_pin(consumer, "CONTRACT_OBJECT_PIN") == [contract_obj] and
        literal_pin(consumer, "CLOSED_SCHEMA_FILE_PIN") == [json_hashes.get("schema")])
    # The launcher gets the seven predecessor/base7 hashes.  It may contain
    # historical hashes in comments/receipts, so search for required values,
    # not for the impossible launcher self-hash.
    required_launcher_hashes = [
        json_hashes.get("anchor"), json_hashes.get("schema"),
        json_hashes.get("contract"), source_hashes.get("producer"),
        source_hashes.get("consumer"), json_hashes.get("transition"),
        json_hashes.get("audit"),
    ]
    source_pin_ok = source_pin_ok and all(
        isinstance(value, str) and value in launcher for value in required_launcher_hashes)
    cb_producer = child_dict(cb, "build_only_producer")
    cb_consumer = child_dict(cb, "independent_verifier_assembler_authority_consumer")
    cb_trust = child_dict(cb, "post_source_static_trust_receipts")
    audited_producer = child_dict(audited, "build_only_producer")
    audited_consumer = child_dict(audited, "independent_verifier_assembler_authority_consumer")
    audited_trust = child_dict(audited, "post_source_static_trust_receipts")
    metadata_ok = (
        schema.get("$comment") ==
        f"CM2_{SUFFIX.upper()}_DAG_STATIC_ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED" and
        cb.get("pin_state") ==
        f"{SUFFIX.upper()}_DAG_SOURCE_PINS_FINAL__RUNTIME_NOT_AUTHORIZED" and
        cb_producer.get("role") ==
        f"BUILD_ONLY__{SUFFIX.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT" and
        cb_producer.get("source_template_only") is False and
        cb_consumer.get("role") ==
        f"NO_PRODUCER__{SUFFIX.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT" and
        cb_consumer.get("source_template_only") is False and
        cb_trust.get("binding_direction") ==
        f"{SUFFIX.upper()}_SOURCE_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE" and
        cb_trust.get("predecessor_supersession_path") == rel(CHAIN_PATHS["anchor"]) and
        cb_trust.get("predecessor_supersession_file_sha256") == json_hashes.get("anchor") and
        cb_trust.get("predecessor_supersession_object_sha256") == anchor.get("object_sha256") and
        audited.get("pin_state") ==
        f"{SUFFIX.upper()}_SOURCE_AND_JSON_PINS_FINAL__STATIC_ZERO_CREDIT" and
        audited_producer.get("role") ==
        f"BUILD_ONLY__{SUFFIX.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT" and
        audited_producer.get("source_template_only") is False and
        audited_consumer.get("role") ==
        f"NO_PRODUCER__{SUFFIX.upper()}_EXECUTABLE_SOURCE__ZERO_CREDIT" and
        audited_consumer.get("source_template_only") is False and
        audited_trust.get("binding_direction") ==
        f"{SUFFIX.upper()}_SOURCE_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE" and
        audited_trust.get("predecessor_supersession_path") == rel(CHAIN_PATHS["anchor"]) and
        audited_trust.get("predecessor_supersession_file_sha256") == json_hashes.get("anchor") and
        audited_trust.get("predecessor_supersession_object_sha256") == anchor.get("object_sha256"))
    source_pin_ok = source_pin_ok and metadata_ok
    add(rows, "final_pin_crosscheck", source_pin_ok,
        {"producer": source_hashes.get("producer"),
         "consumer": source_hashes.get("consumer"),
         "launcher_self_hash_excluded": True, "metadata_ok": metadata_ok})

    # Guard against accidental check-list drift and always emit a fixed-shape
    # report.  This assertion is internal and cannot be triggered by input.
    if len(rows) != len(CHECK_NAMES) or tuple(row["name"] for row in rows) != CHECK_NAMES:
        raise RuntimeError("reviewer check list drift")
    failed = [row["name"] for row in rows if not row["passed"]]
    report: dict[str, Any] = {
        "schema": f"cm2.c79g.successor.{SUFFIX_RAW}-independent-read-only-review.v1",
        "successor_suffix": SUFFIX_RAW,
        "predecessor_suffix": PREV_RAW,
        "status": ("PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED"
                   if not failed else
                   "FAIL_CLOSED_SUCCESSOR_REVIEW__RUNTIME_NOT_AUTHORIZED"),
        "read_only": True,
        "protocol_python_imported_or_executed": False,
        "protocol_or_runtime_files_written": False,
        "check_count": 34,
        "failed_check_count": len(failed),
        "failed_checks": failed,
        "checks": rows,
        "source_hashes": source_hashes,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    }
    report["object_sha256"] = sha(canonical(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
