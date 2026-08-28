#!/usr/bin/env python3
"""Read-only 34-check reviewer for the r15 static candidate.

The reviewer never imports or executes a candidate source.  In addition to
the structural checks inherited from the r13 gate, its final check compares
the live generic v16r2 protocol literals in all three sources with the JSON
roots, active bundle keys, trust receipts, and closed-schema root.
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
SUFFIX = os.environ.get("CM2_SUCCESSOR_SUFFIX", "v16r2r15")
PREV = os.environ.get("CM2_PREDECESSOR_SUFFIX", "v16r2r14")
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

SOURCES = {
    "producer": OUT / f"{BASE}_{SUFFIX}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{SUFFIX}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{SUFFIX}_semantic_source.py",
}
JSONS = {
    "schema": OUT / f"{BASE}_schema_{SUFFIX}.json",
    "contract": OUT / f"{BASE}_contract_{SUFFIX}.json",
    "transition": OUT / f"{BASE}_{PREV}_to_{SUFFIX}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{SUFFIX}.json",
}
REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
SUPERSESSION = OUT / f"{BASE}_{PREV}_to_{SUFFIX}_static_bundle_rejection_supersession_receipt_v1.json"
ANCHOR = OUT / f"{BASE}_{SUFFIX}_active_predecessor_supersession_receipt_v1.json"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{SUFFIX}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{SUFFIX}.json"

V14_REJECTION = ".cm2-runtime/c79g-v14-rejections-" + CHECKPOINT + "/rejection.json"
V14_SUPERSESSION = (
    f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json")
STRICT_REPLAY = (
    "runtime_consumer_must_hold_strict_parse_object_close_and_"
    "terminally_replay_inherited_v14_exact12")
TRANSITION_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer."
    "v16-to-v16r2-static-launch-transition.v1")
TRANSITION_KIND = (
    "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_"
    "ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR")

CHECK_NAMES = (
    "source_files_present", "source_regular_nlink1", "source_draft_modes",
    "ast_parse", "compile_in_memory", "utf8", "no_v15_tokens",
    "successor_tokens", "active_graph_consensus", "nearest_predecessor_closed",
    "checkpoint_derivation", "no_old_active_transition", "runtime_disabled",
    "final_flags_false", "no_pyc", "no_runtime_surfaces", "manifest_absent",
    "outer_absent", "source_hashes_distinct", "source_hashes_stable",
    "no_starred_calls", "no_double_star_calls", "no_duplicate_literal_keys",
    "no_dangerous_calls", "symtable", "json_closed_utf8", "schema_full_shape",
    "schema_root_ref", "instance_shapes_closed", "zero_credit_and_public_closure",
    "exact8_order", "source_pin_consistency", "predecessor_chain_closed",
    "runtime_contract_crosscheck",
)


class DuplicateKey(ValueError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


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
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise ValueError(f"unstable/non-regular: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after, named_after = os.fstat(fd), os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (after.st_dev, after.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise ValueError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise ValueError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(stable(path).decode("utf-8"),
                       object_pairs_hook=strict_pairs)
    if not isinstance(value, dict):
        raise ValueError(f"not an object: {path}")
    return value


def closed(value: dict[str, Any]) -> bool:
    claim = value.get("object_sha256")
    if not isinstance(claim, str) or len(claim) != 64:
        return False
    body = dict(value)
    body.pop("object_sha256", None)
    return sha(canonical(body)) == claim


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def add(rows: list[dict[str, Any]], name: str, passed: bool,
        detail: Any = None) -> None:
    row: dict[str, Any] = {"name": name, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    rows.append(row)


def source_edge_ok(text: dict[str, str]) -> bool:
    edge = JSONS["transition"].name
    anchor = ANCHOR.name
    for value in text.values():
        if edge not in value or anchor not in value:
            return False
        if any(bad in value for bad in (
                f"{BASE}_{SUFFIX}_to_{SUFFIX}", "v16r2r8", "v16r2r9")):
            return False
    return True


def predecessor_closed() -> tuple[bool, dict[str, Any]]:
    try:
        anchor = read_json(ANCHOR)
        supersession = read_json(ROOT / anchor["predecessor_supersession_path"])
        rejection = read_json(ROOT / supersession["predecessor_rejection_path"])
        ok = (closed(anchor) and closed(supersession) and closed(rejection) and
              anchor.get("predecessor_namespace") == PREV and
              anchor.get("successor_namespace") == f"{SUFFIX}_semantic_source" and
              supersession.get("predecessor_namespace") == PREV and
              supersession.get("successor_namespace") == SUFFIX and
              rejection.get("failed_namespace") == PREV and
              supersession.get("formal_global_closure_credit") == 0 and
              rejection.get("formal_global_closure_credit") == 0 and
              supersession.get("D02_unlock") is False and
              rejection.get("D02_unlock") is False)
        return ok, {"supersession": str((ROOT / anchor[
            "predecessor_supersession_path"]).relative_to(ROOT)),
                    "rejection": str((ROOT / supersession[
                        "predecessor_rejection_path"]).relative_to(ROOT))}
    except Exception as exc:
        return False, {"error": f"{type(exc).__name__}: {exc}"}


def call_census(tree: ast.AST) -> tuple[int, int, int, int]:
    starred = double = danger = duplicate = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            starred += sum(isinstance(arg, ast.Starred) for arg in node.args)
            double += sum(keyword.arg is None for keyword in node.keywords)
            danger += int(isinstance(node.func, ast.Name) and
                          node.func.id in {"eval", "exec", "__import__"})
        elif isinstance(node, ast.Dict):
            keys = [key.value for key in node.keys
                    if isinstance(key, ast.Constant) and
                    isinstance(key.value, str)]
            duplicate += len(keys) - len(set(keys))
    return starred, double, danger, duplicate


def final_transition_region(value: str, marker: str) -> str:
    index = value.rfind(marker)
    return value[index:index + 900] if index >= 0 else ""


def runtime_contract_ok(values: dict[str, dict[str, Any]],
                        text: dict[str, str], hashes: dict[str, str]) -> tuple[bool, dict[str, Any]]:
    contract, transition, audit, schema = (values["contract"], values["transition"],
                                           values["audit"], values["schema"])
    root_ok = (
        contract.get("schema") ==
        "cm2.round306c79g.true-global-no-producer-consumer.v16r2.contract" and
        contract.get("status") ==
        "STATIC_CONTRACT_BYTES_FINAL__COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
        transition.get("schema") == TRANSITION_SCHEMA and
        transition.get("status") ==
        "STATIC_BYTES_CLOSED_V16_TO_V16R2__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED" and
        transition.get("transition_kind") == TRANSITION_KIND and
        audit.get("schema") ==
        "cm2.round306c79g.true-global-no-producer-consumer.static-audit.v16r2" and
        audit.get("status") ==
        "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V16R2__PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED")
    key_ok = (
        isinstance(contract.get("v16r2_bundle"), dict) and
        isinstance(transition.get("successor_v16r2_static_bundle"), dict) and
        isinstance(audit.get("audited_v16r2_bundle"), dict) and
        not any(key.endswith("_bundle") for key in contract if key != "v16r2_bundle") and
        not any(key.endswith("_bundle") for key in transition
                if key != "successor_v16r2_static_bundle") and
        not any(key.endswith("_bundle") for key in audit
                if key != "audited_v16r2_bundle"))
    live = contract["v16r2_bundle"]
    expected_transition = str(JSONS["transition"].relative_to(ROOT))
    expected_audit = str(JSONS["audit"].relative_to(ROOT))
    trust = live.get("post_source_static_trust_receipts", {})
    trust_ok = (isinstance(trust, dict) and
                trust.get("v16_to_v16r2_transition_path") == expected_transition and
                trust.get("static_audit_path") == expected_audit and
                trust.get("v14_official_rejection_path") == V14_REJECTION and
                trust.get("v14_registry_shape_drift_supersession_receipt_path") == V14_SUPERSESSION and
                trust.get(STRICT_REPLAY) is True)
    exact = live.get("exact8_ordered_paths")
    expected8 = [str(ANCHOR.relative_to(ROOT)),
                 str(JSONS["schema"].relative_to(ROOT)),
                 str(JSONS["contract"].relative_to(ROOT)),
                 str(SOURCES["producer"].relative_to(ROOT)),
                 str(SOURCES["consumer"].relative_to(ROOT)),
                 expected_transition, expected_audit,
                 str(SOURCES["launcher"].relative_to(ROOT))]
    path_ok = (exact == expected8 and
               live.get("exact10_ordered_paths") == expected8 + [
                   str(MANIFEST.relative_to(ROOT)), str(OUTER.relative_to(ROOT))] and
               live.get("source_hashes") == hashes)
    schema_ok = (set(schema) <= {"$schema", "$id", "$comment", "title",
                                 "description", "$defs", "$ref"} and
                 "object_sha256" not in schema and
                 not any(key.startswith("x-cm2-") for key in schema) and
                 schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority")
    schema_hash = sha(stable(JSONS["schema"]))
    closed_value = live.get("closed_schema", {}).get("file_sha256")
    # Static draft phase permits an explicit unpinned sentinel; a concrete
    # stale predecessor hash is rejected.  The bundle's one-way
    # schema_file_sha256 must still equal the actual current schema bytes.
    closed_pin = ((closed_value == schema_hash or
                   (isinstance(closed_value, str) and
                    closed_value.startswith("UNPINNED_") and
                    "PINS_UNINSTALLED" in str(live.get("pin_state", "")))) and
                  live.get("schema_file_sha256") == schema_hash)
    source_keys = all("v16r2_bundle" in value and
                      "successor_v16r2_static_bundle" in value and
                      "audited_v16r2_bundle" in value for value in text.values())
    producer_region = final_transition_region(
        text["producer"], 'transition.get("schema")')
    consumer_region = final_transition_region(
        text["consumer"], 'transition.get("schema")')
    launcher_region = final_transition_region(
        text["launcher"], 'self.base_objects[TRANSITION].get("schema")')
    schema_fragments = (
        "cm2.round306c79g.true-global-no-producer-consumer.",
        "v16-to-v16r2-static-launch-transition.v1")
    kind_fragments = (
        "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_",
        "ZERO_CREDIT_V16R2_CLEAN_ROOM_SUCCESSOR")
    source_protocol = (source_keys and
                       all(fragment in region for fragment in schema_fragments
                           for region in (producer_region, consumer_region,
                                          launcher_region)) and
                       all(fragment in producer_region for fragment in kind_fragments) and
                       all(fragment in launcher_region for fragment in kind_fragments) and
                       all(fragment in text["consumer"] for fragment in kind_fragments))
    ok = root_ok and key_ok and trust_ok and path_ok and schema_ok and closed_pin and source_protocol
    return ok, {"root": root_ok, "keys": key_ok, "trust": trust_ok,
                "paths": path_ok, "schema_root": schema_ok,
                "closed_schema_pin": closed_pin,
                "source_protocol": source_protocol}


def main() -> int:
    rows: list[dict[str, Any]] = []
    raw: dict[str, bytes] = {}
    text: dict[str, str] = {}
    trees: dict[str, ast.Module] = {}
    errors: dict[str, str] = {}
    present = all(path.is_file() for path in (*SOURCES.values(), *JSONS.values(), ANCHOR))
    add(rows, "source_files_present", present)
    regular = modes = utf8 = True
    for role, path in SOURCES.items():
        try:
            data = stable(path)
            raw[role] = data
            state = path.stat()
            regular &= stat.S_ISREG(state.st_mode) and state.st_nlink == 1
            modes &= stat.S_IMODE(state.st_mode) in {0o644, 0o664}
            text[role] = data.decode("utf-8")
            trees[role] = ast.parse(text[role], filename=str(path))
        except Exception as exc:
            regular = modes = utf8 = False
            errors[role] = f"{type(exc).__name__}: {exc}"
    add(rows, "source_regular_nlink1", regular)
    add(rows, "source_draft_modes", modes)
    add(rows, "ast_parse", len(trees) == 3, errors)
    compile_ok = len(trees) == 3
    for role, tree in trees.items():
        try:
            compile(tree, str(SOURCES[role]), "exec")
        except Exception as exc:
            compile_ok = False
            errors[role] = str(exc)
    add(rows, "compile_in_memory", compile_ok)
    add(rows, "utf8", utf8 and len(raw) == 3)
    joined = b"\n".join(raw.values())
    add(rows, "no_v15_tokens", b"v15" not in joined and b"V15" not in joined)
    add(rows, "successor_tokens", all(SUFFIX.encode() in value for value in raw.values()))
    pred_lines: list[str] = []
    ns_lines: list[str] = []
    for value in text.values():
        for line in value.splitlines():
            if line.startswith("ACTIVE_PREDECESSOR_SUPERSESSION =") and '"' in line:
                pred_lines.append(line.split('"', 2)[1])
            if line.startswith("ACTIVE_SUCCESSOR_NAMESPACE =") and '"' in line:
                ns_lines.append(line.split('"', 2)[1])
    graph = (len(set(pred_lines)) == 1 and pred_lines and
             ANCHOR.name in pred_lines[0] and len(set(ns_lines)) == 1 and
             ns_lines[0] == f"{SUFFIX}_semantic_source")
    add(rows, "active_graph_consensus", graph,
        {"predecessor": pred_lines, "namespace": ns_lines})
    pred, pred_detail = predecessor_closed()
    add(rows, "nearest_predecessor_closed", pred, pred_detail)
    try:
        anchor_blob = json.dumps(read_json(ANCHOR), sort_keys=True)
        derivation = UPSTREAM in anchor_blob and CHECKPOINT in anchor_blob
    except Exception:
        derivation = False
    add(rows, "checkpoint_derivation", derivation,
        {"upstream": UPSTREAM, "successor": CHECKPOINT})
    add(rows, "no_old_active_transition", source_edge_ok(text))
    add(rows, "runtime_disabled", all(
        "RUNTIME_AUTHORIZED = False" in value and
        "FORMAL_GLOBAL_CLOSURE_CREDIT = 0" in value and
        "D02_UNLOCK = False" in value for value in text.values()))
    add(rows, "final_flags_false", all(
        re.search(r"FINAL_[A-Z0-9_]*PINS_INSTALLED\s*=\s*False", value)
        for value in text.values()))
    pycs = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc")
            if SUFFIX in path.name]
    add(rows, "no_pyc", not pycs, pycs)
    runtime_prefix = RUNTIME / f"c79g-{SUFFIX}-"
    runtime_hits = [str(path.relative_to(ROOT)) for path in RUNTIME.glob(
        f"c79g-{SUFFIX}-*")] if RUNTIME.exists() else []
    add(rows, "no_runtime_surfaces", not runtime_hits, runtime_hits)
    add(rows, "manifest_absent", not MANIFEST.exists())
    add(rows, "outer_absent", not OUTER.exists())
    hashes = {role: sha(value) for role, value in raw.items()}
    add(rows, "source_hashes_distinct", len(set(hashes.values())) == 3, hashes)
    add(rows, "source_hashes_stable",
        all(stable(path) == raw[role] for role, path in SOURCES.items()))
    counts = [call_census(tree) for tree in trees.values()]
    sums = [sum(row[index] for row in counts) for index in range(4)] if counts else [1] * 4
    add(rows, "no_starred_calls", sums[0] == 0, sums[0])
    add(rows, "no_double_star_calls", sums[1] == 0, sums[1])
    add(rows, "no_duplicate_literal_keys", sums[3] == 0, sums[3])
    add(rows, "no_dangerous_calls", sums[2] == 0, sums[2])
    add(rows, "symtable", all(
        _symtable_ok(value, SOURCES[role]) for role, value in text.items()))

    values: dict[str, dict[str, Any]] = {}
    json_ok = True
    for name, path in JSONS.items():
        try:
            values[name] = read_json(path)
        except Exception as exc:
            json_ok = False
            errors[name] = f"{type(exc).__name__}: {exc}"
    add(rows, "json_closed_utf8", json_ok and len(values) == 4 and
        all(closed(value) for name, value in values.items() if name != "schema"))
    schema = values.get("schema", {})
    refs = sum(1 for node in walk(schema)
               if isinstance(node, dict) and "$ref" in node)
    closed_count = sum(1 for node in walk(schema)
                       if isinstance(node, dict) and
                       node.get("additionalProperties") is False)
    add(rows, "schema_full_shape", len(schema.get("$defs", {})) == 46 and
        refs == 242 and closed_count == 52,
        {"defs": len(schema.get("$defs", {})), "refs": refs,
         "closed": closed_count})
    add(rows, "schema_root_ref",
        schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority" and
        "coldLaunchedCommittedAuthority" in schema.get("$defs", {}))
    add(rows, "instance_shapes_closed",
        len(values.get("contract", {})) == 30 and
        len(values.get("transition", {})) == 31 and
        len(values.get("audit", {})) == 30 and all(
            closed(values[name]) for name in ("contract", "transition", "audit")))
    baseline = values.get("audit", {}).get("schema_and_constructor_closure", {}).get(
        "global_consumer_baseline", {})
    credit_ok = all(
        not (isinstance(node, dict) and
             (("formal_global_closure_credit" in node and
               node["formal_global_closure_credit"] not in (0, False, None)) or
              ("all_persisted_credit" in node and
               node["all_persisted_credit"] not in (0, False, None)) or
              node.get("D02_unlock") is True))
        for name, value in values.items()
        for node in walk(({key: item for key, item in value.items()
                           if key != "$defs"} if name == "schema" else value)))
    # 1,148 is the held predecessor overlay census; the normative schema
    # closure is public-unresolved=0.  Keep those meanings distinct.
    public_ok = (baseline.get("input_rows") == 76832 and
                 baseline.get("current_public_unresolved") == 1148 and
                 any(isinstance(node, dict) and
                     node.get("public_global_unresolved") == {"const": 0}
                     for node in walk(schema)))
    add(rows, "zero_credit_and_public_closure", credit_ok and public_ok,
        {"credit_ok": credit_ok, "baseline": baseline})
    expected8 = [str(ANCHOR.relative_to(ROOT)),
                 str(JSONS["schema"].relative_to(ROOT)),
                 str(JSONS["contract"].relative_to(ROOT)),
                 str(SOURCES["producer"].relative_to(ROOT)),
                 str(SOURCES["consumer"].relative_to(ROOT)),
                 str(JSONS["transition"].relative_to(ROOT)),
                 str(JSONS["audit"].relative_to(ROOT)),
                 str(SOURCES["launcher"].relative_to(ROOT))]
    bundle = values.get("contract", {}).get("v16r2_bundle", {})
    add(rows, "exact8_order", bundle.get("exact8_ordered_paths") == expected8,
        {"actual": bundle.get("exact8_ordered_paths"), "expected": expected8})
    nested_hashes = [
        values.get("contract", {}).get("v16r2_bundle", {}).get("source_hashes"),
        values.get("transition", {}).get("successor_v16r2_static_bundle", {}).get("source_hashes"),
        values.get("audit", {}).get("audited_v16r2_bundle", {}).get("source_hashes"),
    ]
    add(rows, "source_pin_consistency",
        all(item == hashes for item in nested_hashes), nested_hashes)
    add(rows, "predecessor_chain_closed", pred and
        bundle.get("exact8_ordered_paths", [None])[0] == expected8[0])
    runtime_ok, runtime_detail = runtime_contract_ok(values, text, hashes)
    add(rows, "runtime_contract_crosscheck", runtime_ok, runtime_detail)

    if len(rows) != len(CHECK_NAMES) or tuple(row["name"] for row in rows) != CHECK_NAMES:
        raise RuntimeError("reviewer check list drift")
    failed = [row["name"] for row in rows if not row["passed"]]
    report: dict[str, Any] = {
        "schema": f"cm2.c79g.successor.{SUFFIX}-independent-read-only-review.v1",
        "successor_suffix": SUFFIX,
        "predecessor_suffix": PREV,
        "status": "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED" if not failed else "FAIL_CLOSED_SUCCESSOR_REVIEW__RUNTIME_NOT_AUTHORIZED",
        "read_only": True,
        "check_count": len(rows),
        "failed_check_count": len(failed),
        "failed_checks": failed,
        "checks": rows,
        "source_hashes": hashes,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    }
    report["object_sha256"] = sha(canonical(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if not failed else 1


def _symtable_ok(source: str, path: Path) -> bool:
    try:
        symtable.symtable(source, str(path), "exec")
        return True
    except Exception:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
