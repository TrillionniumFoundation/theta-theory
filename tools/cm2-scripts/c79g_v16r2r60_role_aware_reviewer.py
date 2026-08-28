#!/usr/bin/env python3
"""Read-only r60 role-aware static reviewer.

This is deliberately independent of the historical v15 checker census.  It
checks the active r60 bytes, then compares the launcher registry helper after
version-neutral AST label normalization.  It never imports candidate code and
never writes a file.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import stat
import symtable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r60"
PREV = "v16r2r59"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
ANCHOR_FILE = "b260d3547653a6f2f0ca2bebeb1adff26efcb9cc232e63fe4e69c6fa4da8777b"
ANCHOR_OBJECT = "fa85682507efa9d94f59eb6e77671c1bc27bebe1628c2b8c8f65da6023a4f1e8"
V14_PATH = f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json"
V14_SHA = "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"
V14_OBJECT = "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
NEUTRAL = "5f82214b873d270ea5d01ac43132c0bf1463b12c3289362a001a7c870952bada"
V15_HELPER = OUT / f"{BASE}_cold_launch_v15.py"
SOURCES = {
    "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
}
JSONS = {
    "schema": OUT / f"{BASE}_schema_{TAG}.json",
    "contract": OUT / f"{BASE}_contract_{TAG}.json",
    "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
}
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
SUP = OUT / f"{BASE}_{PREV}_to_{TAG}_runtime_transition_shape_rejection_supersession_receipt_v1.json"
REJ = OUT / f"{BASE}_{PREV}_runtime_transition_shape_rejection_chain_receipt_v1.json"
V14 = OUT / f"{BASE}_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"


class DuplicateKey(ValueError):
    pass


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in items:
        if key in out:
            raise DuplicateKey(key)
        out[key] = value
    return out


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        raw = b"".join(chunks)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(raw) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        return raw
    finally:
        os.close(fd)


def read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=strict_pairs)
    if not isinstance(value, dict):
        raise ValueError(f"not object:{path}")
    return value, raw


def closed(value: Any) -> bool:
    if not isinstance(value, dict) or not isinstance(value.get("object_sha256"), str):
        return False
    claim = value["object_sha256"]
    body = dict(value)
    body.pop("object_sha256", None)
    return len(claim) == 64 and sha(canon(body)) == claim


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for item in value.values():
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def add(rows: list[dict[str, Any]], name: str, passed: bool,
        detail: Any = None) -> None:
    row: dict[str, Any] = {"name": name, "passed": bool(passed)}
    if detail is not None:
        row["detail"] = detail
    rows.append(row)


def top_function(tree: ast.AST, name: str) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    return next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                 and n.name == name), None)


def helper_node(tree: ast.Module) -> ast.FunctionDef:
    fn = top_function(tree, "producer_source_registry_shape_from_ast")
    if not isinstance(fn, ast.FunctionDef):
        raise ValueError("registry helper missing")
    return fn


def helper_digest(fn: ast.FunctionDef) -> str:
    return sha(ast.dump(fn, annotate_fields=True,
                        include_attributes=False).encode())


def neutralize(fn: ast.FunctionDef, mode: str) -> ast.FunctionDef:
    tree = ast.fix_missing_locations(ast.parse(ast.unparse(fn), mode="exec"))
    out = tree.body[0]
    assert isinstance(out, ast.FunctionDef)
    if mode == "ast":
        for node in ast.walk(out):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                node.value = re.sub(r"producer_(?:v15|v16r2)", "producer_CURRENT", node.value)
                node.value = re.sub(r"current v(?:15|16r2)", "current CURRENT", node.value)
    else:
        text = ast.get_source_segment(ast.unparse(fn), out) or ast.unparse(out)
        text = re.sub(r"producer_(?:v15|v16r2)", "producer_CURRENT", text)
        text = re.sub(r"current v(?:15|16r2)", "current CURRENT", text)
        parsed = ast.parse(text, mode="exec")
        out = parsed.body[0]
        assert isinstance(out, ast.FunctionDef)
    return out


def source_call_stats(tree: ast.AST) -> tuple[int, int, int, int]:
    star = double = danger = duplicate = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            star += sum(isinstance(a, ast.Starred) for a in node.args)
            double += sum(k.arg is None for k in node.keywords)
            danger += int(isinstance(node.func, ast.Name) and
                          node.func.id in {"eval", "exec", "__import__"})
        elif isinstance(node, ast.Dict):
            keys = [k.value for k in node.keys if isinstance(k, ast.Constant)
                    and isinstance(k.value, str)]
            duplicate += len(keys) - len(set(keys))
    return star, double, danger, duplicate


def _len_name(node: ast.AST, name: str) -> bool:
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "len" and len(node.args) == 1
            and not node.keywords and isinstance(node.args[0], ast.Name)
            and node.args[0].id == name)


def _len_set_name(node: ast.AST, name: str) -> bool:
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "len" and len(node.args) == 1
            and not node.keywords and isinstance(node.args[0], ast.Call)
            and isinstance(node.args[0].func, ast.Name)
            and node.args[0].func.id == "set" and len(node.args[0].args) == 1
            and not node.args[0].keywords and isinstance(node.args[0].args[0], ast.Name)
            and node.args[0].args[0].id == name)


def _len_attr(node: ast.AST, name: str, attr: str) -> bool:
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "len" and len(node.args) == 1
            and not node.keywords and isinstance(node.args[0], ast.Attribute)
            and isinstance(node.args[0].value, ast.Name)
            and node.args[0].value.id == name and node.args[0].attr == attr)


def _direct_need(fn: ast.AST, node: ast.AST) -> bool:
    parents = {child: parent for parent in ast.walk(fn)
               for child in ast.iter_child_nodes(parent)}
    cur = node
    while cur in parents:
        parent = parents[cur]
        if isinstance(parent, ast.Expr) and isinstance(parent.value, ast.Call):
            return (isinstance(parent.value.func, ast.Name)
                    and parent.value.func.id == "need" and bool(parent.value.args))
        if isinstance(parent, ast.Call) and isinstance(parent.func, ast.Name) and parent.func.id == "need":
            return bool(parent.args) and cur is parent.args[0]
        if not isinstance(parent, ast.BoolOp) or not isinstance(parent.op, ast.And):
            return False
        cur = parent
    return False


def helper_structural(tree: ast.Module, producer_tree: ast.Module) -> dict[str, Any]:
    fn = helper_node(tree)
    nodes = list(ast.walk(fn))
    nested = sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef,
                                ast.Lambda, ast.ClassDef)) and n is not fn
                 for n in nodes)
    args = [*fn.args.posonlyargs, *fn.args.args]
    explicit_guards = []
    proof_guards = []
    expansion_guards = []
    shape_guards = 0
    stale62 = sum(isinstance(n, ast.Constant) and n.value == 62 for n in nodes)
    for n in nodes:
        if isinstance(n, ast.Compare) and _direct_need(fn, n):
            if (len(n.ops) == 2 and all(isinstance(op, ast.Eq) for op in n.ops)
                    and _len_name(n.left, "explicit_keys")
                    and _len_set_name(n.comparators[0], "explicit_keys")
                    and isinstance(n.comparators[1], ast.Constant)
                    and n.comparators[1].value == 67):
                explicit_guards.append(n)
            if (len(n.ops) == 1 and isinstance(n.ops[0], ast.Eq)
                    and _len_attr(n.left, "proof_dict", "keys")
                    and len(n.comparators) == 1
                    and isinstance(n.comparators[0], ast.Constant)
                    and n.comparators[0].value == 7):
                proof_guards.append(n)
            if (len(n.ops) == 1 and isinstance(n.ops[0], ast.Eq)
                    and _len_name(n.left, "expansions")
                    and len(n.comparators) == 1
                    and isinstance(n.comparators[0], ast.Constant)
                    and n.comparators[0].value == 1):
                expansion_guards.append(n)
            if (len(n.ops) == 1 and isinstance(n.ops[0], ast.Eq)
                    and isinstance(n.left, ast.Name) and n.left.id == "shape"
                    and len(n.comparators) == 1
                    and isinstance(n.comparators[0], ast.Constant)
                    and n.comparators[0].value == 75):
                shape_guards += 1
    source = ast.unparse(fn)
    labels = {
        "producer_v16r2": source.count("producer_v16r2"),
        "current_v16r2": source.count("current v16r2"),
        "producer_v15": source.count("producer_v15"),
        "current_v15": source.count("current v15"),
    }
    producer_shape = 0
    registry = top_function(producer_tree, "input_registry")
    held = next((n for n in producer_tree.body if isinstance(n, ast.ClassDef)
                 and n.name == "HeldSelf"), None)
    proof = next((n for n in held.body if isinstance(n, ast.FunctionDef)
                  and n.name == "execution_proof"), None) if held else None
    if registry and proof:
        returns = [n for n in ast.walk(registry) if isinstance(n, ast.Return)
                   and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
                   and n.value.func.id == "close_object" and n.value.args
                   and isinstance(n.value.args[0], ast.Dict)]
        proofs = [n for n in ast.walk(proof) if isinstance(n, ast.Return)
                  and isinstance(n.value, ast.Dict)]
        if len(returns) == 1 and len(proofs) == 1:
            keys = [k for k in returns[0].value.args[0].keys
                    if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            pkeys = [k for k in proofs[0].value.keys
                     if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            producer_shape = len(keys) + len(pkeys) + 1
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name)
             and n.func.id == "producer_source_registry_shape_from_ast"]
    owner = None
    direct = held_raw = expected_gate = False
    parents = {child: parent for parent in ast.walk(tree)
               for child in ast.iter_child_nodes(parent)}
    if len(calls) == 1:
        call = calls[0]
        cur: ast.AST = call
        while cur in parents:
            par = parents[cur]
            if isinstance(par, ast.FunctionDef):
                owner = par.name
                break
            cur = par
        assignment = parents.get(call)
        direct = (isinstance(assignment, ast.Assign) and
                  isinstance(assignment.targets[0], ast.Name) and
                  assignment.targets[0].id == "computed_registry_shape")
        if direct:
            cursor = assignment
            while cursor in parents:
                owner_node = parents[cursor]
                if isinstance(owner_node, (ast.If, ast.For, ast.While, ast.Try,
                                            ast.With, ast.Match, ast.ExceptHandler)):
                    direct = False
                    break
                if isinstance(owner_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    break
                cursor = owner_node
        held_raw = ast.dump(call.args[0], include_attributes=False) == ast.dump(
            ast.parse("held_by_path[PRODUCER].raw", mode="eval").body,
            include_attributes=False) if call.args and not call.keywords else False
        expected_gate = any(isinstance(n, ast.Compare) and
                            isinstance(n.left, ast.Name) and
                            n.left.id == "computed_registry_shape" and
                            any(isinstance(c, ast.Constant) and c.value == 75
                                for c in n.comparators)
                            for n in ast.walk(next((x for x in ast.walk(tree)
                                                    if isinstance(x, ast.FunctionDef)
                                                    and x.name == "validate_final_static_audit"), fn)))
    return {
        "explicit_key_guard": [67] if explicit_guards else [],
        "proof7": len(proof_guards),
        "expansion1": len(expansion_guards),
        "shape75": shape_guards,
        "stale62": stale62,
        "nested_scopes": nested,
        "raw_param": len(args) == 1 and args[0].arg == "raw" and not fn.args.vararg
                      and not fn.args.kwarg and not fn.args.kwonlyargs,
        "formula": "len(explicit_keys) + len(proof_dict.keys) + 1" in source,
        "direct_return": bool(fn.body and isinstance(fn.body[-1], ast.Return)
                               and isinstance(fn.body[-1].value, ast.Name)
                               and fn.body[-1].value.id == "shape"),
        "live_call_owner": owner,
        "live_call_count": len(calls),
        "live_direct_assignment": direct,
        "live_held_producer_raw": held_raw,
        "live_expected_shapes_75_gate": expected_gate,
        "producer_shape": producer_shape,
        "labels": labels,
    }


def mutation_replay(tree: ast.Module, producer_tree: ast.Module) -> dict[str, bool]:
    # Independent structural predicates: changing 67 to 62 or hiding the live
    # call must make the same guard vector fail.
    fn = helper_node(tree)
    tampered = ast.parse(ast.unparse(tree))
    tf = helper_node(tampered)
    changed = 0
    for n in ast.walk(tf):
        if isinstance(n, ast.Constant) and n.value == 67:
            n.value = 62; changed += 1
    stale = helper_structural(tampered, producer_tree)
    stale_rejected = changed == 1 and not (stale["explicit_key_guard"] == [67])
    dead = ast.parse(ast.unparse(tree))
    moved = 0
    class HideLiveCall(ast.NodeTransformer):
        def visit_Assign(self, node: ast.Assign):
            nonlocal moved
            if (len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id == "computed_registry_shape"):
                moved += 1
                return ast.If(test=ast.Constant(False), body=[node], orelse=[])
            return self.generic_visit(node)
    HideLiveCall().visit(dead)
    deadv = helper_structural(dead, producer_tree)
    return {"stale62_rejected": stale_rejected,
            "dead_callsite_rejected": moved == 1 and not deadv["live_direct_assignment"]}


def main() -> int:
    rows: list[dict[str, Any]] = []
    failed: list[str] = []
    raw: dict[str, bytes] = {}
    texts: dict[str, str] = {}
    trees: dict[str, ast.Module] = {}
    values: dict[str, dict[str, Any]] = {}
    raws: dict[str, bytes] = {}

    paths = [*SOURCES.values(), *JSONS.values(), ANCHOR, SUP, REJ, V14]
    present = all(p.is_file() for p in paths)
    add(rows, "candidate_files_present", present)
    regular = mode_ok = stable_ok = utf8_ok = True
    for role, path in SOURCES.items():
        try:
            raw[role] = stable(path); texts[role] = raw[role].decode("utf-8")
            st = path.stat(); regular &= stat.S_ISREG(st.st_mode) and st.st_nlink == 1
            mode_ok &= stat.S_IMODE(st.st_mode) == 0o664
            stable_ok &= sha(raw[role]) == sha(stable(path)); ast.parse(texts[role], str(path))
        except Exception:
            regular = mode_ok = stable_ok = utf8_ok = False
    add(rows, "source_regular_nlink1", regular)
    add(rows, "source_modes_0664_pre_freeze", mode_ok)
    add(rows, "source_stable_identity_replay", stable_ok)
    add(rows, "source_utf8_ast_parse", utf8_ok and len(texts) == 3)
    compile_ok = True
    for role, text in texts.items():
        try:
            trees[role] = ast.parse(text, str(SOURCES[role]), mode="exec")
            compile(trees[role], str(SOURCES[role]), "exec")
        except Exception:
            compile_ok = False
    add(rows, "source_compile_in_memory", compile_ok and len(trees) == 3)
    sym_ok = True
    try:
        for role, text in texts.items(): symtable.symtable(text, str(SOURCES[role]), "exec")
    except Exception: sym_ok = False
    add(rows, "source_symtable", sym_ok)
    stats = [source_call_stats(t) for t in trees.values()]
    add(rows, "no_starred_calls", all(x[0] == 0 for x in stats))
    add(rows, "no_double_star_calls", all(x[1] == 0 for x in stats))
    add(rows, "no_dangerous_calls", all(x[2] == 0 for x in stats))
    add(rows, "no_duplicate_literal_dict_keys", all(x[3] == 0 for x in stats))

    json_ok = json_closed = True
    try:
        for role, path in JSONS.items(): values[role], raws[role] = read_json(path)
    except Exception:
        json_ok = False
    json_closed = json_ok and all(closed(values[r]) for r in ("contract", "transition", "audit"))
    add(rows, "strict_json_unique_keys", json_ok)
    add(rows, "top_level_json_object_closures", json_closed)
    schema, contract = values.get("schema", {}), values.get("contract", {})
    transition, audit = values.get("transition", {}), values.get("audit", {})
    refs = sum(isinstance(n, dict) and "$ref" in n for n in walk(schema))
    closed_nodes = [n for n in walk(schema) if isinstance(n, dict) and n.get("additionalProperties") is False]
    mismatch = [n for n in closed_nodes if set(n.get("required", [])) != set(n.get("properties", {}))]
    add(rows, "schema_46_defs_242_refs_52_closed", len(schema.get("$defs", {})) == 46 and refs == 242 and len(closed_nodes) == 52)
    add(rows, "schema_root_and_id", schema.get("$ref") == "#/$defs/coldLaunchedCommittedAuthority" and schema.get("$id", "").endswith(f".{TAG}.schema"))
    add(rows, "schema_required_property_sets", not mismatch)
    checkpoint_nodes = [d.get("properties", {}).get("effective_checkpoint_object_sha256")
                        for d in schema.get("$defs", {}).values() if isinstance(d, dict)
                        and "effective_checkpoint_object_sha256" in d.get("properties", {})]
    add(rows, "schema_checkpoint_const_nodes", len(checkpoint_nodes) == 9 and all(x == {"const": UPSTREAM} for x in checkpoint_nodes))
    add(rows, "instance_top_level_shapes", len(contract) == 30 and len(transition) == 30 and len(audit) == 30)
    credit_values = []
    for role in ("contract", "transition", "audit"):
        for n in walk(values.get(role, {})):
            if isinstance(n, dict):
                for key in ("formal_global_closure_credit", "D02_unlock", "runtime_authorized"):
                    if key in n:
                        credit_values.append((key, n[key]))
    add(rows, "zero_credit_runtime_baseline",
        all((key == "formal_global_closure_credit" and value == 0) or
            (key in {"D02_unlock", "runtime_authorized"} and value is False)
            for key, value in credit_values))

    # Active source constants and pins.
    succ = []; pred = []; pred_file = []; pred_obj = []
    for tree in trees.values():
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                names = [x.id for x in node.targets if isinstance(x, ast.Name)]
                if "ACTIVE_SUCCESSOR_NAMESPACE" in names:
                    try: succ.append(ast.literal_eval(node.value))
                    except Exception: pass
                if "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN" in names:
                    try: pred_file.append(ast.literal_eval(node.value))
                    except Exception: pass
                if "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN" in names:
                    try: pred_obj.append(ast.literal_eval(node.value))
                    except Exception: pass
                if "ACTIVE_PREDECESSOR_SUPERSESSION" in names:
                    pred.append(ast.unparse(node.value))
    add(rows, "active_namespace_consensus", len(succ) >= 3 and
        set(succ) == {f"{TAG}_semantic_source"} and
        all(TAG in x for x in pred))
    add(rows, "active_anchor_pin_consensus", len(pred_file) >= 3 and set(pred_file) == {ANCHOR_FILE} and len(pred_obj) >= 3 and set(pred_obj) == {ANCHOR_OBJECT})
    bundle = contract.get("v16r2_bundle", {})
    expected8 = [V14_PATH, str(JSONS["schema"].relative_to(ROOT)), str(JSONS["contract"].relative_to(ROOT)),
                 str(SOURCES["producer"].relative_to(ROOT)), str(SOURCES["consumer"].relative_to(ROOT)),
                 str(JSONS["transition"].relative_to(ROOT)), str(JSONS["audit"].relative_to(ROOT)),
                 str(SOURCES["launcher"].relative_to(ROOT))]
    add(rows, "exact8_base7_exact10_order", bundle.get("exact8_ordered_paths") == expected8 and
        bundle.get("base7_ordered_paths") == expected8[:-1] and
        bundle.get("exact10_ordered_paths") == expected8 + [str(MANIFEST.relative_to(ROOT)), str(OUTER.relative_to(ROOT))])
    source_hashes = {role: sha(data) for role, data in raw.items()}
    nested_hashes = [bundle.get("build_only_producer", {}).get("file_sha256"),
                     transition.get("successor_v16r2_static_bundle", {}).get("build_only_producer", {}).get("file_sha256"),
                     audit.get("audited_v16r2_bundle", {}).get("build_only_producer", {}).get("file_sha256")]
    consumer_pin = transition.get("successor_v16r2_static_bundle", {}).get("independent_verifier_assembler_authority_consumer", {}).get("file_sha256")
    add(rows, "source_hash_pin_consistency", all(x in (None, source_hashes["producer"]) for x in nested_hashes) and
        consumer_pin == source_hashes["consumer"] and
        audit.get("audited_v16r2_bundle", {}).get("independent_verifier_assembler_authority_consumer", {}).get("file_sha256") == source_hashes["consumer"])
    checker = audit.get("dual_independent_static_checkers", {})
    checker_inputs_ok = all(
        checker.get(name, {}).get("input_sha256", {}).get(role) == source_hashes[role]
        for name in ("checker_A", "checker_B") for role in ("producer", "consumer")
    ) and checker.get("all_common_callsite_censuses_equal") is True
    add(rows, "independent_checker_input_pin_replay", checker_inputs_ok)

    try:
        av, _ = read_json(ANCHOR); sv, _ = read_json(SUP); rv, _ = read_json(REJ)
        prev_anchor = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
        chain = (closed(av) and closed(sv) and closed(rv) and av.get("object_sha256") == ANCHOR_OBJECT and
                 av.get("predecessor_namespace") == PREV and av.get("successor_namespace") == f"{TAG}_semantic_source" and
                 sv.get("predecessor_namespace") == PREV and sv.get("successor_namespace") == TAG and
                 sv.get("predecessor_active_anchor_file_sha256") == sha(stable(prev_anchor)) and
                 sv.get("predecessor_active_anchor_object_sha256") == json.loads(stable(prev_anchor).decode())["object_sha256"] and
                 rv.get("formal_global_closure_credit") == 0)
    except Exception:
        chain = False
    add(rows, "predecessor_chain_closure", chain)
    try:
        av, _ = read_json(V14); active = audit.get("audited_v16r2_bundle", {}).get("v14_registry_shape_drift_supersession_receipt", {})
        v14ok = (sha(stable(V14)) == V14_SHA and av.get("object_sha256") == V14_OBJECT and
                 active == {"path": V14_PATH, "file_sha256": V14_SHA, "object_sha256": V14_OBJECT})
    except Exception:
        v14ok = False
    add(rows, "active_v14_receipt_pin", v14ok)

    tb = transition.get("successor_v16r2_static_bundle", {})
    boundary = transition.get("cold_launch_boundary", {})
    sem = (tb.get("all_four_core_file_pins_final") is True and tb.get("final_consumer_pin_installed") is True and
           tb.get("transition_receipt_physical_freeze_completed") is False and
           boundary.get("base7_order") == ["v14_registry_shape_drift_supersession_receipt", "closed_schema_v16r2", "contract_v16r2", "producer_v16r2", "consumer_v16r2", "transition_v16_to_v16r2", "static_audit_v16r2"])
    add(rows, "transition_boundary_semantics", sem)
    add(rows, "audit_static_semantics", audit.get("status", "").startswith("PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO") and
        audit.get("final_audit_acceptance", {}).get("final_failed_static_check_count_required") == 0)

    hfn = helper_node(trees["launcher"])
    hs = helper_structural(trees["launcher"], trees["producer"])
    add(rows, "launcher_current_label_census", hs["labels"] == {"producer_v16r2": 1, "current_v16r2": 5, "producer_v15": 0, "current_v15": 0})
    oldfn = helper_node(ast.parse(stable(V15_HELPER).decode("utf-8")))
    neutral_a = helper_digest(neutralize(hfn, "ast"))
    neutral_b = helper_digest(neutralize(oldfn, "ast"))
    add(rows, "launcher_version_neutral_template_equivalence", neutral_a == NEUTRAL and neutral_b == NEUTRAL)
    guard_ok = (hs["explicit_key_guard"] == [67] and hs["proof7"] == 1 and hs["expansion1"] == 1 and
                hs["shape75"] == 1 and hs["stale62"] == 0 and hs["nested_scopes"] == 0 and hs["raw_param"] and
                hs["formula"] and hs["direct_return"] and hs["live_call_owner"] == "validate_final_static_audit" and
                hs["live_call_count"] == 1 and hs["live_held_producer_raw"] and hs["live_expected_shapes_75_gate"] and hs["producer_shape"] == 75)
    add(rows, "launcher_registry_guard_vector", guard_ok, hs)
    muts = mutation_replay(trees["launcher"], trees["producer"])
    add(rows, "launcher_registry_mutation_fail_closed", muts["stale62_rejected"] and muts["dead_callsite_rejected"], muts)
    runtime_hits = [str(p) for p in ROOT.rglob("*.pyc")
                    if TAG in p.name and p.name != "c79g_v16r2r60_candidate_builder.cpython-312.pyc"]
    add(rows, "no_r60_pyc_manifest_outer_runtime", not MANIFEST.exists() and not OUTER.exists() and not runtime_hits)
    add(rows, "c53_authority_unchanged", C53.is_file() and sha(stable(C53)) == C53_SHA)

    if len(rows) != 34:
        raise RuntimeError(f"review check census {len(rows)} != 34")
    failed = [r["name"] for r in rows if not r["passed"]]
    report = {"schema": f"cm2.c79g.{TAG}.role-aware-independent-review.v1",
              "candidate_namespace": TAG,
              "status": "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__VERSION_NEUTRAL_HELPER_GO__RUNTIME_NOT_AUTHORIZED" if not failed else "FAIL_CLOSED_ROLE_AWARE_REVIEW__RUNTIME_NOT_AUTHORIZED",
              "check_count": len(rows), "failed_check_count": len(failed),
              "failed_checks": failed, "checks": rows,
              "helper_raw_ast_sha256": helper_digest(hfn),
              "historical_helper_raw_ast_sha256": helper_digest(oldfn),
              "version_neutral_helper_ast_sha256": neutral_a,
              "formal_global_closure_credit": 0, "D02_unlock": False,
              "runtime_authorized": False, "manifest_created": False,
              "outer_created": False, "runtime_protocol_executed": False,
              "source_hashes": source_hashes}
    report["object_sha256"] = sha(canon(report))
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
