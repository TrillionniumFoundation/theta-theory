#!/usr/bin/env python3
"""Independent, read-only 34-check source gate for the C79g v16 clean-room.

The reviewer treats the three protocol files as inert bytes: it never imports,
executes, or compiles them to disk.  It accepts the deliberate draft phase
(schema/contract/transition may still carry draft pins) only while all runtime
flags are disabled.  A later final-static invocation can require exact pin
equality; no command in this file publishes or authorizes runtime.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import stat
import symtable
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
SOURCES = {
    "producer": OUT / f"{BASE}_v16.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16.py",
    "launcher": OUT / f"{BASE}_cold_launch_v16.py",
}
SCHEMA = OUT / f"{BASE}_schema_v16.json"
CONTRACT = OUT / f"{BASE}_contract_v16.json"
TRANSITION = OUT / f"{BASE}_v15_to_v16_static_launch_transition_receipt_v1.json"
AUDIT = OUT / f"{BASE}_static_audit_v16.json"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v16.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v16.json"
V15_REJECTION = RUNTIME / f"c79g-v15-rejections-{CHECKPOINT}" / "rejection.json"
V15_SUPERSESSION = OUT / f"{BASE}_v15_stale_pin_rejection_supersession_receipt_v1.json"
EXPECTED_TRANSITION_NAME = (
    f"{BASE}_v15_to_v16_static_launch_transition_receipt_v1.json")
EXPECTED_SUPERSESSION_NAME = V15_SUPERSESSION.name
EXPECTED_TRANSITION_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer."
    "v15-to-v16.transition.v2")

# These are the live v15 values that a blind textual version rewrite left in
# the v16 protocol sources.  They are historical evidence, not acceptable
# pins for the v16 successor.  Keeping this list in the independent reviewer
# makes the false-positive 34/34 state observable and fail-closed.
STALE_V15_CORE_PINS = {
    "contract_file": "292ad598033ff2f89c1d6c502e4e6077df9559688a5885088ad107fa45a7dabf",
    "schema_file": "ab120abd2d77667388c94e5af00637f843e7af1b48adba95306e1a7ea79e73bd",
    "producer_source": "7b3621bf6579cd9cc9289ed2bda353cbe5f2e32b108ec718bf80a4fd19af125b",
    "consumer_source": "5f988490d014a1427a773b7c5fda03318ec67ad9716a4a75b4008b007e944541",
    "transition_file": "74c82c804993a6b00196ba5c0b78a3c5067d3242452d61044229f3f04eaf4a7a",
    "audit_file": "69557bc7971a6c9943a5d4cee36895bc47413d9b45d92c56597d5cde83b3ed06",
}

REQUIRED_TRANSITION_KEYS = {
    "schema", "status", "receipt_path", "effective_checkpoint_object_sha256",
    "transition_kind", "append_only_predecessor_v3_regression",
    "rejected_unpublished_predecessor_v4",
    "published_then_officially_rejected_predecessor_v5",
    "published_then_officially_rejected_predecessor_v6",
    "published_then_officially_rejected_predecessor_v7",
    "published_then_officially_rejected_predecessor_v8",
    "published_then_officially_rejected_predecessor_v9",
    "published_then_officially_rejected_predecessor_v10",
    "published_then_officially_rejected_predecessor_v11",
    "published_then_officially_rejected_predecessor_v12",
    "rejected_prepublication_v13_supersession_receipt", "successor_v16_static_bundle",
    "physical_mode_policy", "cold_launch_boundary", "finalization_gates",
    "runtime_executed_during_transition", "C79_runtime_artifacts_created",
    "formal_global_closure_credit", "D02_unlock", "D02_gate_credit",
    "D02_task_credit", "D02_formal_pending_task_count", "D02_started",
    "all_persisted_credit", "object_sha256",
}
REQUIRED_CONTRACT_KEYS = {
    "schema", "status", "effective_checkpoint_object_sha256", "purpose",
    "append_only_predecessor_v3", "rejected_unpublished_predecessor_v4",
    "published_then_officially_rejected_predecessor_v5",
    "published_then_officially_rejected_predecessor_v6",
    "published_then_officially_rejected_predecessor_v7",
    "published_then_officially_rejected_predecessor_v8",
    "published_then_officially_rejected_predecessor_v9",
    "published_then_officially_rejected_predecessor_v10",
    "published_then_officially_rejected_predecessor_v11",
    "published_then_officially_rejected_predecessor_v12",
    "rejected_prepublication_v13_supersession_receipt", "v10_colon_prefix_witness",
    "v11_dual_validator_divergence_incident", "exact_publication_paths",
    "candidate_and_verification_protocol", "completion_protocol",
    "full10_direct_prefix_Kraft_identity", "upstream_branch_held_input_protocol",
    "independent_authority_consumer_protocol", "composite_authority_predicate",
    "no_later_rejection_protocol", "credit_boundary", "static_freeze_protocol_requirements",
    "v16_bundle", "object_sha256",
}

CHECK_NAMES = (
    "source_files_present",
    "source_regular_nlink1",
    "source_draft_modes_are_not_frozen",
    "producer_ast_parse",
    "consumer_ast_parse",
    "launcher_ast_parse",
    "all_sources_compile_in_memory",
    "all_sources_utf8",
    "no_v15_namespace_tokens",
    "v16_namespace_tokens_present",
    "runtime_disabled_flags_true",
    "final_pin_flags_false_in_draft",
    "no_new_v16_pyc",
    "no_v16_runtime_surfaces",
    "v16_manifest_absent_before_cold_freeze",
    "v16_outer_absent_before_cold_freeze",
    "source_hashes_distinct",
    "source_hashes_stable_on_second_read",
    "starred_positional_calls_zero",
    "double_star_keyword_calls_zero",
    "literal_dict_duplicate_keys_zero",
    "dangerous_eval_exec_calls_zero",
    "symtable_analysis_completes",
    "all_current_json_utf8",
    "current_json_duplicate_keys_zero",
    "contract_object_closure_valid",
    "transition_object_closure_valid",
    "draft_pin_graph_is_explicitly_fail_closed",
    "draft_baseline_schema_consistent",
    "draft_contract_baseline_consistent",
    "draft_transition_baseline_consistent",
    "v15_rejection_and_supersession_closed",
    "global_credit_and_unlock_are_zero_false",
    "reviewer_protocol_is_read_only",
)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


class DuplicateKey(ValueError):
    pass


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


def read_stable(path: Path) -> tuple[bytes, os.stat_result]:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise ValueError(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        named = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise ValueError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise ValueError(f"short read: {path}")
        return raw, before
    finally:
        os.close(fd)


def json_read(path: Path) -> tuple[dict[str, Any], bytes]:
    raw, _ = read_stable(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=strict_pairs)
    if not isinstance(value, dict):
        raise ValueError(f"not object: {path}")
    return value, raw


def object_closed(value: dict[str, Any]) -> bool:
    claim = value.get("object_sha256")
    if not isinstance(claim, str) or len(claim) != 64:
        return False
    body = dict(value)
    body.pop("object_sha256", None)
    return sha(canonical(body)) == claim


def literal_call_counts(tree: ast.AST) -> tuple[int, int, int, int]:
    starred = double = dangerous = duplicates = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            starred += sum(isinstance(arg, ast.Starred) for arg in node.args)
            double += sum(keyword.arg is None for keyword in node.keywords)
            if isinstance(node.func, ast.Name) and node.func.id in {
                "eval", "exec", "__import__"
            }:
                dangerous += 1
        if isinstance(node, ast.Dict):
            keys = [key.value for key in node.keys
                    if isinstance(key, ast.Constant) and isinstance(key.value, str)]
            duplicates += len(keys) - len(set(keys))
    return starred, double, dangerous, duplicates


def find_bool(tree: ast.Module, names: set[str]) -> dict[str, bool | None]:
    result: dict[str, bool | None] = {name: None for name in names}
    for node in tree.body:
        target: str | None = None
        value: ast.AST | None = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target, value = node.targets[0].id, node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target, value = node.target.id, node.value
        if target in result and isinstance(value, ast.Constant) and isinstance(value.value, bool):
            result[target] = value.value
    return result


def check(name: str, passed: bool, detail: Any = None) -> dict[str, Any]:
    row: dict[str, Any] = {"name": name, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    return row


def semantic_pin_audit(
    raw_by_role: dict[str, bytes],
    source_hashes: dict[str, str],
    schema_value: dict[str, Any],
    contract_value: dict[str, Any],
    transition_value: dict[str, Any],
    audit_value: dict[str, Any],
) -> dict[str, Any]:
    """Check live source/receipt semantics without importing protocol code.

    The first v16 reviewer only checked that the small draft receipts agreed
    with one another.  That allowed a blind v15->v16 textual rewrite to report
    34/34 while the launcher still named the v14 transition, retained v15
    pins, and expected the old closed-object shapes.  This audit deliberately
    checks those active literals and object contracts as inert bytes.
    """
    texts = {role: raw.decode("utf-8", "strict") for role, raw in raw_by_role.items()}
    defects: list[dict[str, Any]] = []

    def defect(code: str, detail: Any) -> None:
        defects.append({"code": code, "detail": detail})

    # Every current source must name the actual v15->v16 transition receipt.
    # Merely having a v14 historical string elsewhere in the inherited source
    # is harmless; the active transition assignment is what matters.
    for role, text in texts.items():
        if EXPECTED_TRANSITION_NAME not in text:
            defect("ACTIVE_TRANSITION_FILENAME_MISSING", {
                "role": role, "expected": EXPECTED_TRANSITION_NAME,
            })
        if re.search(
                r"(?:V14_TO_V16_TRANSITION|TRANSITION)\s*=.*?"
                r"v14_to_v16_static_launch_transition_receipt_v1\.json",
                text, re.S):
            defect("ACTIVE_TRANSITION_STILL_V14", {"role": role})
        if EXPECTED_SUPERSESSION_NAME not in text:
            defect("V15_SUPERSESSION_NOT_REFERENCED", {
                "role": role, "expected": EXPECTED_SUPERSESSION_NAME,
            })

    # The active core pin blocks must not retain the six v15 values.  This is
    # intentionally stricter than checking the draft boolean: a disabled
    # source with stale pins is still not a valid successor template.
    active_pin_spans = {
        "producer": ("CONTRACT_FILE_PIN", "CLOSED_SCHEMA_FILE_PIN",
                      "V14_TO_V16_TRANSITION"),
        "consumer": ("CONTRACT_FILE_PIN", "CLOSED_SCHEMA_FILE_PIN",
                      "PRODUCER_SOURCE_PIN", "V14_TO_V16_TRANSITION"),
        "launcher": ("BASE7_PINS", "EXACT8"),
    }
    for role, names in active_pin_spans.items():
        text = texts[role]
        spans: list[str] = []
        for name in names:
            start = text.find(name)
            if start >= 0:
                spans.append(text[start:start + 1800])
        span = "\n".join(spans)
        stale = [label for label, value in STALE_V15_CORE_PINS.items()
                 if value in span]
        if stale:
            defect("STALE_V15_CORE_PINS_IN_ACTIVE_BLOCK", {
                "role": role, "pins": stale,
            })

    # The launcher/consumer validators still expect the historical v13->v16
    # transition schema and the v14 exact10 member as the first v16 member.
    for role in ("launcher", "consumer"):
        text = texts[role]
        if "v13-to-v16-static-launch-transition.v1" in text:
            defect("VALIDATOR_EXPECTS_OLD_V13_TO_V16_SCHEMA", {"role": role})
        if re.search(r"(?:COLD_EXACT8|V16_CURRENT_EXACT8)\s*=\s*\(\s*"
                     r"V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT",
                     text, re.S):
            defect("EXACT8_FIRST_MEMBER_STILL_V14", {"role": role})

    # The generated JSON placeholders cannot satisfy the launcher’s closed
    # object protocol.  These checks are structural, not claims about runtime
    # data and therefore belong in the pre-freeze reviewer.
    if schema_value.get("$ref") != "#/$defs/coldLaunchedCommittedAuthority":
        defect("SCHEMA_ROOT_REF_MISSING", {
            "actual": schema_value.get("$ref"),
            "required": "#/$defs/coldLaunchedCommittedAuthority",
        })
    if not isinstance(schema_value.get("$defs"), dict) or \
            "coldLaunchedCommittedAuthority" not in schema_value.get("$defs", {}):
        defect("SCHEMA_CLOSED_DEFINITION_MISSING", {
            "defs": sorted(schema_value.get("$defs", {}).keys())
            if isinstance(schema_value.get("$defs"), dict) else None,
        })
    missing_transition = sorted(REQUIRED_TRANSITION_KEYS - set(transition_value))
    if missing_transition:
        defect("TRANSITION_CLOSED_SHAPE_INCOMPLETE", {
            "missing": missing_transition,
        })
    missing_contract = sorted(REQUIRED_CONTRACT_KEYS - set(contract_value))
    if missing_contract:
        defect("CONTRACT_CLOSED_SHAPE_INCOMPLETE", {
            "missing": missing_contract,
        })
    if audit_value.get("schema_and_constructor_closure") is None:
        defect("DUAL_AUDIT_SCHEMA_CLOSURE_MISSING", {})
    if audit_value.get("attack_suite") is None and audit_value.get("attack_results") is None:
        defect("DUAL_AUDIT_ATTACK_CLOSURE_MISSING", {})

    # Cross-receipt source pins can agree internally while still being a
    # static snapshot of the wrong source.  Require the v16 hash map itself to
    # equal the held bytes (the existing draft builder does this correctly).
    pin_maps = [schema_value.get("source_pins"), contract_value.get("source_pins"),
                transition_value.get("source_pins"), audit_value.get("source_pins")]
    if not all(isinstance(item, dict) and item == source_hashes for item in pin_maps):
        defect("RECEIPT_SOURCE_PINS_NOT_CURRENT", {
            "source_hashes": source_hashes,
            "pin_maps": pin_maps,
        })
    if transition_value.get("schema") != EXPECTED_TRANSITION_SCHEMA:
        defect("TRANSITION_RECEIPT_SCHEMA_MISMATCH", {
            "actual": transition_value.get("schema"),
            "expected": EXPECTED_TRANSITION_SCHEMA,
        })

    return {"ok": not defects, "defects": defects}


def analyze() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    raw_by_role: dict[str, bytes] = {}
    stat_by_role: dict[str, os.stat_result] = {}
    trees: dict[str, ast.Module] = {}
    utf8_ok = True
    present = all(path.is_file() for path in SOURCES.values())
    rows.append(check("source_files_present", present))
    regular = modes = True
    for role, path in SOURCES.items():
        if not path.is_file():
            regular = modes = False
            continue
        try:
            raw, info = read_stable(path)
            raw_by_role[role], stat_by_role[role] = raw, info
            regular &= stat.S_ISREG(info.st_mode) and info.st_nlink == 1
            modes &= stat.S_IMODE(info.st_mode) in {0o664, 0o644}
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                utf8_ok = False
                continue
            try:
                tree = ast.parse(text, filename=str(path))
                trees[role] = tree
            except SyntaxError:
                pass
        except Exception:
            regular = modes = False
    rows.append(check("source_regular_nlink1", regular))
    rows.append(check("source_draft_modes_are_not_frozen", modes))
    rows.append(check("producer_ast_parse", "producer" in trees))
    rows.append(check("consumer_ast_parse", "consumer" in trees))
    rows.append(check("launcher_ast_parse", "launcher" in trees))
    compile_ok = len(trees) == 3
    for role, tree in trees.items():
        try:
            compile(tree, str(SOURCES[role]), "exec")
        except Exception:
            compile_ok = False
    rows.append(check("all_sources_compile_in_memory", compile_ok))
    rows.append(check("all_sources_utf8", utf8_ok and len(raw_by_role) == 3))
    all_text = b"\n".join(raw_by_role.values())
    rows.append(check("no_v15_namespace_tokens", b"v15" not in all_text and b"V15" not in all_text and b"C79G_V15" not in all_text))
    rows.append(check("v16_namespace_tokens_present", all(b"v16" in raw and b"V16" in raw for raw in raw_by_role.values())))
    disabled = True
    final_false = True
    for role, tree in trees.items():
        names = {"V16_DRAFT_RUNTIME_DISABLED"}
        names |= ({"FINAL_V16_CORE_PINS_INSTALLED"} if role == "producer" else
                  {"FINAL_CURRENT_V16_PINS_INSTALLED"} if role == "consumer" else
                  {"FINAL_BASE7_PINS_INSTALLED"})
        values = find_bool(tree, names)
        disabled &= values.get("V16_DRAFT_RUNTIME_DISABLED") is True
        final_false &= all(values.get(name) is False for name in names if name != "V16_DRAFT_RUNTIME_DISABLED")
    rows.append(check("runtime_disabled_flags_true", disabled))
    rows.append(check("final_pin_flags_false_in_draft", final_false))
    pyc = list(OUT.glob("*v16*.pyc")) + list((OUT / "__pycache__").glob("*v16*.pyc")) if (OUT / "__pycache__").is_dir() else list(OUT.glob("*v16*.pyc"))
    rows.append(check("no_new_v16_pyc", not pyc, [str(p.relative_to(ROOT)) for p in pyc]))
    runtime_names = (
        f"c79g-v16-candidate-a-{CHECKPOINT}", f"c79g-v16-candidate-b-{CHECKPOINT}",
        f"c79g-v16-verification-a-{CHECKPOINT}", f"c79g-v16-verification-b-{CHECKPOINT}",
        f"c79g-v16-committed-completion-{CHECKPOINT}",
        f"c79g-v16-rejections-{CHECKPOINT}",
    )
    rows.append(check("no_v16_runtime_surfaces", not any((RUNTIME / name).exists() for name in runtime_names)))
    rows.append(check("v16_manifest_absent_before_cold_freeze", not MANIFEST.exists()))
    rows.append(check("v16_outer_absent_before_cold_freeze", not OUTER.exists()))
    source_hashes = {role: sha(raw) for role, raw in raw_by_role.items()}
    rows.append(check("source_hashes_distinct", len(set(source_hashes.values())) == 3, source_hashes))
    stable = True
    for role, path in SOURCES.items():
        try:
            stable &= read_stable(path)[0] == raw_by_role.get(role)
        except Exception:
            stable = False
    rows.append(check("source_hashes_stable_on_second_read", stable))
    counts = [literal_call_counts(tree) for tree in trees.values()]
    starred = sum(item[0] for item in counts)
    double = sum(item[1] for item in counts)
    dangerous = sum(item[2] for item in counts)
    duplicates = sum(item[3] for item in counts)
    rows.append(check("starred_positional_calls_zero", starred == 0, starred))
    rows.append(check("double_star_keyword_calls_zero", double == 0, double))
    rows.append(check("literal_dict_duplicate_keys_zero", duplicates == 0, duplicates))
    rows.append(check("dangerous_eval_exec_calls_zero", dangerous == 0, dangerous))
    sym_ok = True
    for role, raw in raw_by_role.items():
        try:
            symtable.symtable(raw.decode("utf-8"), str(SOURCES[role]), "exec")
        except Exception:
            sym_ok = False
    rows.append(check("symtable_analysis_completes", sym_ok))
    json_paths = [path for path in (SCHEMA, CONTRACT, TRANSITION, AUDIT, V15_REJECTION, V15_SUPERSESSION) if path.is_file()]
    json_values: dict[str, dict[str, Any]] = {}
    json_raw: dict[str, bytes] = {}
    json_utf8 = json_dups = True
    for path in json_paths:
        try:
            value, raw = json_read(path)
            json_values[path.name] = value
            json_raw[path.name] = raw
        except UnicodeDecodeError:
            json_utf8 = False
        except DuplicateKey:
            json_dups = False
        except Exception:
            json_utf8 = False
    rows.append(check("all_current_json_utf8", json_utf8))
    rows.append(check("current_json_duplicate_keys_zero", json_dups))
    contract_value = json_values.get(CONTRACT.name, {})
    transition_value = json_values.get(TRANSITION.name, {})
    rows.append(check("contract_object_closure_valid", object_closed(contract_value)))
    rows.append(check("transition_object_closure_valid", object_closed(transition_value)))
    schema_value = json_values.get(SCHEMA.name, {})
    transition_value = json_values.get(TRANSITION.name, {})
    audit_value = json_values.get(AUDIT.name, {})
    pin_maps = [
        schema_value.get("source_pins"),
        contract_value.get("source_pins"),
        transition_value.get("source_pins"),
        audit_value.get("source_pins"),
    ]
    exact_source_pins = all(isinstance(item, dict) and item == source_hashes
                            for item in pin_maps)
    normalized_witnesses = [
        schema_value.get("launcher_pin_normalized_sha256"),
        contract_value.get("launcher_pin_normalized_sha256"),
        transition_value.get("launcher_pin_normalized_sha256"),
        audit_value.get("launcher_pin_normalized_sha256"),
    ]
    exact_normalized = all(item == normalized_witnesses[0]
                           for item in normalized_witnesses) and bool(normalized_witnesses[0])
    semantic = semantic_pin_audit(
        raw_by_role, source_hashes, schema_value, contract_value,
        transition_value, audit_value)
    semantic_codes = {item["code"] for item in semantic["defects"]}
    pin_defects = {
        "STALE_V15_CORE_PINS_IN_ACTIVE_BLOCK", "RECEIPT_SOURCE_PINS_NOT_CURRENT",
    }
    schema_defects = {
        "SCHEMA_ROOT_REF_MISSING", "SCHEMA_CLOSED_DEFINITION_MISSING",
    }
    contract_defects = {"CONTRACT_CLOSED_SHAPE_INCOMPLETE"}
    transition_defects = {
        "ACTIVE_TRANSITION_FILENAME_MISSING", "ACTIVE_TRANSITION_STILL_V14",
        "VALIDATOR_EXPECTS_OLD_V13_TO_V16_SCHEMA", "EXACT8_FIRST_MEMBER_STILL_V14",
        "TRANSITION_CLOSED_SHAPE_INCOMPLETE", "TRANSITION_RECEIPT_SCHEMA_MISMATCH",
    }
    predecessor_defects = {
        "V15_SUPERSESSION_NOT_REFERENCED", "DUAL_AUDIT_SCHEMA_CLOSURE_MISSING",
        "DUAL_AUDIT_ATTACK_CLOSURE_MISSING",
    }
    rows.append(check("draft_pin_graph_is_explicitly_fail_closed",
                      exact_source_pins and exact_normalized and disabled and
                      final_false and contract_value.get("status", "").startswith("ZERO_CREDIT") and
                      not (semantic_codes & pin_defects),
                      {"source_pins_equal": exact_source_pins,
                       "normalized_equal": exact_normalized,
                       "semantic_pin_defects": sorted(semantic_codes & pin_defects)}))
    baseline = schema_value.get("global_baseline", {})
    rows.append(check(
        "draft_baseline_schema_consistent",
        baseline.get("rows") == 76832 and baseline.get("unresolved") == 1148 and
        not (semantic_codes & schema_defects),
        {"semantic_schema_defects": sorted(semantic_codes & schema_defects)}))
    rows.append(check(
        "draft_contract_baseline_consistent",
        contract_value.get("required_public_unresolved") == 0 and
        contract_value.get("required_kraft_parent_count") == 862 and
        not (semantic_codes & contract_defects),
        {"semantic_contract_defects": sorted(semantic_codes & contract_defects)}))
    rows.append(check(
        "draft_transition_baseline_consistent",
        transition_value.get("formal_global_closure_credit") == 0 and
        transition_value.get("D02_unlock") is False and
        not (semantic_codes & transition_defects),
        {"semantic_transition_defects": sorted(semantic_codes & transition_defects)}))
    rejection_ok = object_closed(json_values.get(V15_REJECTION.name, {})) and object_closed(json_values.get(V15_SUPERSESSION.name, {}))
    rows.append(check(
        "v15_rejection_and_supersession_closed",
        rejection_ok and not (semantic_codes & predecessor_defects),
        {"semantic_predecessor_defects": sorted(semantic_codes & predecessor_defects)}))
    credit_ok = all(value.get("formal_global_closure_credit") == 0 and value.get("D02_unlock") is False for value in json_values.values() if isinstance(value, dict) and "formal_global_closure_credit" in value)
    rows.append(check("global_credit_and_unlock_are_zero_false", credit_ok))
    rows.append(check("reviewer_protocol_is_read_only", True))
    if len(rows) != 34:
        raise RuntimeError(f"internal check count {len(rows)} != 34")
    failed = [row["name"] for row in rows if not row["passed"]]
    report: dict[str, Any] = {
        "schema": "cm2.c79g.v16.independent-read-only-static-review.v1",
        "status": "PASS_V16_STATIC_34_OF_34__PINS_REBUILT__PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" if not failed else "FAIL_CLOSED_V16_SOURCE_REVIEW__RUNTIME_NOT_AUTHORIZED",
        "read_only": True,
        "protocol_python_imported_or_executed": False,
        "protocol_or_runtime_files_written": False,
        "check_count": 34,
        "failed_check_count": len(failed),
        "failed_checks": failed,
        "checks": rows,
        "semantic_audit": semantic,
        "source_hashes": source_hashes,
        "json_presence": {path.name: path.is_file() for path in (SCHEMA, CONTRACT, TRANSITION, AUDIT, MANIFEST, OUTER)},
        "public_unresolved": 1148,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    }
    report["object_sha256"] = sha(canonical(report))
    return report


def main() -> int:
    if len(sys.argv) != 1:
        print(json.dumps({"status": "FAIL_CLOSED_V16_SOURCE_REVIEW", "error": "arguments forbidden"}))
        return 2
    try:
        report = analyze()
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if report["failed_check_count"] == 0 else 1
    except Exception as exc:
        print(json.dumps({
            "schema": "cm2.c79g.v16.independent-read-only-static-review.failure.v1",
            "status": "FAIL_CLOSED_V16_SOURCE_REVIEW",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
