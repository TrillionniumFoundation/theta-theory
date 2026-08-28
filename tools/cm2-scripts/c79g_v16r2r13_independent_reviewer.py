#!/usr/bin/env python3
"""Independent 34-check, read-only reviewer for the r13 static bundle.

This checker intentionally validates the executable source path constants and
the nested exact10/boundary witnesses, checks that the 137-name attack census
is present (execution is still deferred), and never imports or executes a
candidate.  A nonzero exit status is reserved for a failed check.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import symtable
import sys
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
SUFFIX = "v16r2r13"
PREV = "v16r2r12"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"

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
ANCHOR = OUT / f"{BASE}_{SUFFIX}_active_predecessor_supersession_receipt_v1.json"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{SUFFIX}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{SUFFIX}.json"

CHECKS = (
    "source_files_present", "source_regular_nlink1", "source_draft_modes",
    "ast_parse", "compile_in_memory", "utf8", "no_v15_tokens",
    "successor_tokens", "active_graph_consensus", "nearest_predecessor_closed",
    "checkpoint_derivation", "no_old_active_transition", "runtime_disabled",
    "final_flags_false", "no_pyc", "no_runtime_surfaces", "manifest_absent",
    "outer_absent", "source_hashes_distinct", "source_hashes_stable",
    "no_starred_calls", "no_double_star_calls", "no_duplicate_literal_keys",
    "no_dangerous_calls", "symtable", "json_closed_utf8", "schema_full_shape",
    "schema_root_ref", "instance_shapes_closed", "zero_credit_baseline",
    "exact8_order", "source_pin_consistency", "predecessor_chain_closed",
    "semantic_transition_paths",
)


class DuplicateKey(ValueError):
    pass


def canonical(v: Any) -> bytes:
    return json.dumps(v, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out: raise DuplicateKey(k)
        out[k] = v
    return out


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise ValueError(f"not regular/nlink1: {path}")
        chunks = []
        while True:
            b = os.read(fd, 1 << 20)
            if not b: break
            chunks.append(b)
        after, named = os.fstat(fd), os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
            (after.st_dev, after.st_ino, after.st_size) or
            (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise ValueError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size: raise ValueError(f"short read: {path}")
        return raw
    finally: os.close(fd)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(stable(path).decode("utf-8"), object_pairs_hook=strict_pairs)
    if not isinstance(value, dict): raise ValueError(f"not object: {path}")
    return value


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for x in value.values(): yield from walk(x)
    elif isinstance(value, list):
        for x in value: yield from walk(x)


def closed(value: Any) -> bool:
    if not isinstance(value, dict) or not isinstance(value.get("object_sha256"), str): return False
    body = dict(value); claim = body.pop("object_sha256")
    return len(claim) == 64 and sha(canonical(body)) == claim


def call_counts(tree: ast.AST) -> tuple[int, int, int, int]:
    star = double = danger = duplicate = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            star += sum(isinstance(a, ast.Starred) for a in node.args)
            double += sum(k.arg is None for k in node.keywords)
            danger += isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__"}
        elif isinstance(node, ast.Dict):
            keys = [k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            duplicate += len(keys) - len(set(keys))
    return star, double, danger, duplicate


def add(rows: list[dict[str, Any]], name: str, passed: bool, detail: Any = None) -> None:
    row = {"name": name, "passed": bool(passed)}
    if detail is not None: row["detail"] = detail
    rows.append(row)


def resolve(path: str | None) -> Path | None:
    if not isinstance(path, str): return None
    return ROOT / path if "/" in path else OUT / path


def predecessor_ok(anchor: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    try:
        p = resolve(anchor.get("predecessor_supersession_path"))
        if p is None: return False, {"reason": "missing path"}
        sup = read_json(p)
        r = resolve(sup.get("predecessor_rejection_path"))
        if r is None: return False, {"reason": "missing rejection"}
        rej = read_json(r)
        ok = (closed(anchor) and closed(sup) and closed(rej) and
              anchor.get("predecessor_namespace") == PREV and
              sup.get("predecessor_namespace") == PREV and sup.get("successor_namespace") == SUFFIX and
              rej.get("failed_namespace") == PREV and
              sup.get("formal_global_closure_credit") == 0 and sup.get("D02_unlock") is False and
              rej.get("formal_global_closure_credit") == 0 and rej.get("D02_unlock") is False)
        return ok, {"supersession": str(p.relative_to(ROOT)), "rejection": str(r.relative_to(ROOT))}
    except Exception as exc:
        return False, {"error": f"{type(exc).__name__}: {exc}"}


def source_edge_ok(texts: dict[str, str], expected_transition: str, expected_anchor: str) -> bool:
    for text in texts.values():
        if expected_transition not in text or expected_anchor not in text:
            return False
        if any(bad in text for bad in ("v16r2r8", "v16r2r9", f"{BASE}_{SUFFIX}_to_{SUFFIX}", "R9_STATIC")):
            return False
    # The launcher exact8 tuple must enumerate the active first eight names
    # in order; checking ordered textual positions catches path swaps without
    # executing the launcher.
    launcher = texts["launcher"]
    names = [ANCHOR.name, JSONS["schema"].name, JSONS["contract"].name,
             SOURCES["producer"].name, SOURCES["consumer"].name,
             JSONS["transition"].name, JSONS["audit"].name,
             SOURCES["launcher"].name]
    # Restrict the order test to the literal COLD_EXACT8 tuple.  The same
    # filenames occur in earlier configuration constants (SELF/SCHEMA/etc.),
    # so a whole-file first-occurrence comparison would be a false failure.
    start = launcher.find("COLD_EXACT8")
    if start < 0:
        start = launcher.find("EXACT8")
    excerpt = launcher[start:] if start >= 0 else launcher
    # The tuple uses the local ``SELF`` symbol for its eighth member rather
    # than repeating the launcher basename.  Check the seven literal members
    # and require SELF after the audit member.
    positions = [excerpt.find(n) for n in names[:-1]]
    self_pos = excerpt.find("SELF", positions[-1] if positions else 0)
    return (all(x >= 0 for x in positions) and positions == sorted(positions)
            and self_pos > positions[-1])


def main() -> int:
    rows: list[dict[str, Any]] = []
    raw: dict[str, bytes] = {}
    text: dict[str, str] = {}
    trees: dict[str, ast.Module] = {}
    errors: dict[str, str] = {}
    present = all(p.is_file() for p in SOURCES.values())
    add(rows, "source_files_present", present)
    regular = modes = utf8 = True
    for role, path in SOURCES.items():
        try:
            data = stable(path); raw[role] = data; st = path.stat()
            regular &= stat.S_ISREG(st.st_mode) and st.st_nlink == 1
            modes &= stat.S_IMODE(st.st_mode) in {0o644, 0o664}
            text[role] = data.decode("utf-8")
            trees[role] = ast.parse(text[role], filename=str(path))
        except UnicodeDecodeError as exc:
            utf8 = False; errors[role] = str(exc)
        except Exception as exc:
            regular = modes = utf8 = False; errors[role] = f"{type(exc).__name__}: {exc}"
    add(rows, "source_regular_nlink1", regular)
    add(rows, "source_draft_modes", modes)
    add(rows, "ast_parse", len(trees) == 3, errors)
    compile_ok = len(trees) == 3
    for role, tree in trees.items():
        try: compile(tree, str(SOURCES[role]), "exec")
        except Exception as exc: compile_ok = False; errors[role] = str(exc)
    add(rows, "compile_in_memory", compile_ok)
    add(rows, "utf8", utf8 and len(raw) == 3)
    joined = b"\n".join(raw.values())
    add(rows, "no_v15_tokens", b"v15" not in joined and b"V15" not in joined)
    add(rows, "successor_tokens", all(SUFFIX.encode() in x for x in raw.values()))
    pred_lines = []
    ns_lines = []
    for value in text.values():
        for line in value.splitlines():
            if line.startswith("ACTIVE_PREDECESSOR_SUPERSESSION =") and '"' in line: pred_lines.append(line.split('"', 2)[1])
            if line.startswith("ACTIVE_SUCCESSOR_NAMESPACE =") and '"' in line: ns_lines.append(line.split('"', 2)[1])
    graph = (len(set(pred_lines)) == 1 and pred_lines and ANCHOR.name in pred_lines[0] and
             len(set(ns_lines)) == 1 and ns_lines[0] == f"{SUFFIX}_semantic_source")
    add(rows, "active_graph_consensus", graph, {"predecessor": pred_lines, "namespace": ns_lines})
    try: anchor = read_json(ANCHOR); pred, pred_detail = predecessor_ok(anchor)
    except Exception as exc: anchor = {}; pred = False; pred_detail = {"error": str(exc)}
    add(rows, "nearest_predecessor_closed", pred, pred_detail)
    blob = json.dumps(anchor, sort_keys=True)
    add(rows, "checkpoint_derivation", UPSTREAM in blob and CHECKPOINT in blob,
        {"upstream": UPSTREAM, "successor": CHECKPOINT})
    add(rows, "no_old_active_transition", source_edge_ok(text, JSONS["transition"].name, ANCHOR.name))
    add(rows, "runtime_disabled", all("RUNTIME_AUTHORIZED = False" in x and "FORMAL_GLOBAL_CLOSURE_CREDIT = 0" in x and "D02_UNLOCK = False" in x for x in text.values()))
    add(rows, "final_flags_false", all("FINAL_BASE7_PINS_INSTALLED = False" in x for x in text.values()))
    pycs = [str(p.relative_to(ROOT)) for p in OUT.rglob("*.pyc") if SUFFIX in p.name]
    add(rows, "no_pyc", not pycs, pycs)
    forbidden = [RUNTIME / f"c79g-{SUFFIX}-candidate-a-{CHECKPOINT}", RUNTIME / f"c79g-{SUFFIX}-candidate-b-{CHECKPOINT}", RUNTIME / f"c79g-{SUFFIX}-verification-a-{CHECKPOINT}", RUNTIME / f"c79g-{SUFFIX}-verification-b-{CHECKPOINT}"]
    add(rows, "no_runtime_surfaces", not any(p.exists() for p in forbidden))
    add(rows, "manifest_absent", not MANIFEST.exists())
    add(rows, "outer_absent", not OUTER.exists())
    hashes = {r: sha(x) for r, x in raw.items()}
    add(rows, "source_hashes_distinct", len(set(hashes.values())) == 3, hashes)
    add(rows, "source_hashes_stable", all(stable(p) == raw[r] for r, p in SOURCES.items()))
    counts = [call_counts(t) for t in trees.values()]
    sums = [sum(c[i] for c in counts) for i in range(4)] if counts else [1, 1, 1, 1]
    add(rows, "no_starred_calls", sums[0] == 0, sums[0]); add(rows, "no_double_star_calls", sums[1] == 0, sums[1]); add(rows, "no_duplicate_literal_keys", sums[3] == 0, sums[3]); add(rows, "no_dangerous_calls", sums[2] == 0, sums[2])
    sym_ok = True
    for role, data in raw.items():
        try: symtable.symtable(data.decode(), str(SOURCES[role]), "exec")
        except Exception: sym_ok = False
    add(rows, "symtable", sym_ok)
    values: dict[str, dict[str, Any]] = {}; json_ok = duplicate_ok = True
    for name, path in JSONS.items():
        try: values[name] = read_json(path)
        except DuplicateKey: duplicate_ok = False
        except Exception: json_ok = False
    add(rows, "json_closed_utf8", json_ok and len(values) == 4 and all(closed(x) for x in values.values()))
    schema, contract = values.get("schema", {}), values.get("contract", {})
    transition, audit = values.get("transition", {}), values.get("audit", {})
    refs = sum(1 for x in walk(schema) if isinstance(x, dict) and "$ref" in x)
    closed_count = sum(1 for x in walk(schema) if isinstance(x, dict) and x.get("additionalProperties") is False)
    add(rows, "schema_full_shape", len(schema.get("$defs", {})) == 46 and refs == 242 and closed_count == 52, {"defs": len(schema.get("$defs", {})), "refs": refs, "closed": closed_count})
    add(rows, "schema_root_ref", schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority" and "coldLaunchedCommittedAuthority" in schema.get("$defs", {}))
    add(rows, "instance_shapes_closed", len(contract) == 30 and len(transition) == 31 and len(audit) == 30 and all(closed(x) for x in (contract, transition, audit)))
    active = schema.get("x-cm2-successor-active", {})
    baseline = active.get("global_baseline", {}) if isinstance(active, dict) else {}
    credit_ok = True
    for name, value in values.items():
        nodes = walk({k: v for k, v in value.items() if k != "$defs"}) if name == "schema" else walk(value)
        for node in nodes:
            if isinstance(node, dict):
                for key in ("formal_global_closure_credit", "all_persisted_credit"):
                    if key in node and node[key] not in (0, False, None): credit_ok = False
    add(rows, "zero_credit_baseline", baseline.get("rows") == 76832 and baseline.get("unresolved") == 1148 and credit_ok)
    bundle = contract.get(f"{SUFFIX}_bundle", {})
    expected = [str(ANCHOR.relative_to(ROOT)), str(JSONS["schema"].relative_to(ROOT)), str(JSONS["contract"].relative_to(ROOT)), str(SOURCES["producer"].relative_to(ROOT)), str(SOURCES["consumer"].relative_to(ROOT)), str(JSONS["transition"].relative_to(ROOT)), str(JSONS["audit"].relative_to(ROOT)), str(SOURCES["launcher"].relative_to(ROOT))]
    add(rows, "exact8_order", isinstance(bundle, dict) and bundle.get("exact8_ordered_paths") == expected, {"actual": bundle.get("exact8_ordered_paths"), "expected": expected})
    nested = [active.get("source_hashes") if isinstance(active, dict) else None, bundle.get("source_hashes") if isinstance(bundle, dict) else None, transition.get(f"successor_{SUFFIX}_static_bundle", {}).get("source_hashes"), audit.get(f"audited_{SUFFIX}_bundle", {}).get("source_hashes")]
    add(rows, "source_pin_consistency", all(x == hashes for x in nested), nested)
    add(rows, "predecessor_chain_closed", pred and isinstance(bundle, dict) and bundle.get("exact8_ordered_paths", [None])[0] == expected[0])
    semantic = False
    try:
        tb = transition.get(f"successor_{SUFFIX}_static_bundle", {})
        boundary = transition.get("cold_launch_boundary", {})
        trust = bundle.get("post_source_static_trust_receipts", {})
        attack = audit.get("coherent_attack_static_census", {})
        semantic = (transition.get("receipt_path") == expected[5] and
                    transition.get("schema") == f"cm2.round306c79g.true-global-no-producer-consumer.{PREV}-to-{SUFFIX}.transition" and
                    transition.get("transition_kind") == f"APPEND_ONLY_{PREV.upper()}_TO_{SUFFIX.upper()}_ZERO_CREDIT_JSON_BUNDLE" and
                    tb.get("exact10_ordered_paths") == expected + [f"deliverables/{BASE}_cold_launch_manifest_{SUFFIX}.sha256", f"deliverables/{BASE}_cold_launch_outer_receipt_{SUFFIX}.json"] and
                    boundary.get("base7_first_member_path") == expected[0] and boundary.get("base7_order") == expected[:-1] and
                    trust.get("predecessor_supersession_path") == expected[0] and
                    attack.get("exact_unique_ordered_attack_count_required") == 137 and attack.get("exact_unique_ordered_attack_count_observed") == 137 and
                    attack.get("attack_execution_deferred_to_cold_runtime") is True and
                    all(JSONS["transition"].name in x for x in text.values()))
    except Exception: semantic = False
    add(rows, "semantic_transition_paths", semantic)
    if not duplicate_ok: rows[25]["passed"] = False
    if len(rows) != 34: raise RuntimeError(f"check count {len(rows)}")
    failed = [x["name"] for x in rows if not x["passed"]]
    report = {"schema": f"cm2.c79g.successor.{SUFFIX}-independent-read-only-review.v1", "successor_suffix": SUFFIX, "predecessor_suffix": PREV, "status": "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED" if not failed else "FAIL_CLOSED_SUCCESSOR_REVIEW__RUNTIME_NOT_AUTHORIZED", "read_only": True, "check_count": 34, "failed_check_count": len(failed), "failed_checks": failed, "checks": rows, "source_hashes": hashes, "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False}
    report["object_sha256"] = sha(canonical(report)); print(json.dumps(report, ensure_ascii=False, sort_keys=True)); return 0 if not failed else 1


if __name__ == "__main__": raise SystemExit(main())
