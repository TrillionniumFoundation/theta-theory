#!/usr/bin/env python3
"""Independent static review of the C79g v12 draft/final bytes.

The three protocol Python files are never imported or executed.  This program
reads each byte snapshot once, parses it with ``ast``/``symtable``, and performs
the requested in-memory compile.  JSON is decoded with duplicate-key tracking.
By default it writes no files and creates no protocol or runtime surface.  The
explicit ``--write-checker-census-report`` option may create exactly one
canonically closed, immutable checker report below this workspace's
``scripts/`` directory.  That opt-in report is not a protocol/runtime surface.

A successful result is only a static-byte result.  It does not authorize a
runtime entry, publication, D02 credit, or D02 start.
"""

from __future__ import annotations

import argparse
import ast
import builtins
import copy
import hashlib
import json
import os
import stat
import symtable
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
CHECKPOINT = (
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")

V12_PYTHON = (
    ("producer", OUT / f"{BASE}_v12.py"),
    ("consumer", OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v12.py"),
    ("launcher", OUT / f"{BASE}_cold_launch_v12.py"),
)
V11_PYTHON = (
    ("producer", OUT / f"{BASE}_v11.py"),
    ("consumer", OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v11.py"),
    ("launcher", OUT / f"{BASE}_cold_launch_v11.py"),
)
V12_JSON = {
    "schema": OUT / f"{BASE}_schema_v12.json",
    "contract": OUT / f"{BASE}_contract_v12.json",
    "transition": OUT / f"{BASE}_v11_to_v12_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v12.json",
}
V11_AUDIT = OUT / f"{BASE}_static_audit_v11.json"
V11_REJECTION = (
    RUNTIME / f"c79g-v11-rejections-{CHECKPOINT}" / "rejection.json")
V12_MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v12.sha256"
V12_OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v12.json"
V12_JSON_BUILDER = ROOT / "scripts" / "c79g_v12_json_draft_builder.py"

EXPECTED_V11_CALLSITE_COUNT = 2964
EXPECTED_V11_CALLSITE_SHA256 = (
    "d6d1ffa7a47968ff691fac8e720c9c6770549ae0892e64241204dfe2cd41d6cf")
HELPER_NAME = "derive_v10_colon_prefix_witness"
EXPECTED_HELPER_CALLSITES = [
    {"source_role": "producer", "enclosing_function": "hold_static_freeze_trust",
     "direct_call_count": 1},
    {"source_role": "consumer", "enclosing_function": "__init__",
     "direct_call_count": 1},
    {"source_role": "launcher", "enclosing_function": "bind_predecessors",
     "direct_call_count": 1},
    {"source_role": "launcher", "enclosing_function": "terminal_replay",
     "direct_call_count": 1},
]
EXPECTED_HELPER_CALLSITE_SHA256 = (
    "69979c91172f95d179e5af986d4f8d2d5406ffcfdc14abaef1f1578766c1963d")
EXPECTED_AUDIT_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer.static-audit.v12")
EXPECTED_AUDIT_STATUS = (
    "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V12__"
    "PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED")
CALLSITE_KINDS = (
    "module_function", "module_constructor", "self_instance_method",
    "cls_class_method", "localclass_static_method",
    "localclass_class_method", "localclass_instance_method",
)
SHAPE_KEYS = {
    "selfIdentity", "independentConsumerProof", "staticFreezeProof",
    "coldLaunchProof", "laterRejection", "producerSourceRegistry",
    "liveRequest", "liveACK", "liveACKCensus",
}
SCHEMA_KEYWORDS = {
    "$comment", "$defs", "$id", "$ref", "$schema", "additionalProperties",
    "const", "description", "items", "maxItems", "minItems", "minLength",
    "minimum", "oneOf", "pattern", "prefixItems", "properties", "required",
    "title", "type", "uniqueItems",
}
SUPPORTED_SCHEMA_KEYWORDS = {
    "$comment", "$defs", "$id", "$ref", "$schema", "additionalProperties",
    "const", "description", "items", "maxItems", "minItems", "minLength",
    "minimum", "pattern", "prefixItems", "properties", "required", "title",
    "type", "uniqueItems",
}
MISSING = object()

CHECKER_CENSUS_REPORT_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer."
    "v12-static-checker-census.v1")
CHECKER_REPORT_ZERO_KEYS = (
    "arity_failure_count", "starred_positional_total",
    "double_star_keyword_total", "undefined_global_count",
    "JSON_duplicate_key_count", "python_literal_dict_duplicate_key_count",
    "object_closure_failure_count", "pin_failure_count",
    "failed_static_check_count",
)
# This is intentionally an exact local mirror of the consumer builder's
# CHECKER_REPORT_KEYS.  The writer verifies equality again immediately before
# O_EXCL creation; no extra diagnostic or timestamp key may enter the object.
CHECKER_REPORT_KEYS = frozenset({
    "schema", "producer_file_sha256", "consumer_file_sha256",
    "launcher_file_sha256", "wider_local_callsite_census_row_count",
    "wider_local_callsite_census_sha256",
    "common_ordered_callsite_row_count",
    "common_ordered_callsite_census_sha256", "common_callsite_kind_census",
    "python_literal_dict_count",
    "python_AST_and_compile_in_memory_file_count", *CHECKER_REPORT_ZERO_KEYS,
    "object_sha256",
})


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode("utf-8")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_sha256(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def stat_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def read_stable_regular_file(path: Path) -> tuple[bytes, tuple[int, ...]]:
    flags = os.O_RDONLY | os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"{path}: not a regular file")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if stat_identity(before) != stat_identity(after):
            raise ValueError(f"{path}: identity changed during read")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise ValueError(f"{path}: short or extended read")
        return raw, stat_identity(before)
    finally:
        os.close(descriptor)


class Report:
    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []

    def add(self, name: str, passed: bool, **details: Any) -> None:
        row: dict[str, Any] = {"name": name, "passed": bool(passed)}
        if details:
            row["details"] = details
        self.checks.append(row)

    def finish(self, sections: dict[str, Any]) -> dict[str, Any]:
        failures = [row["name"] for row in self.checks if not row["passed"]]
        return {
            "schema": "cm2.c79g.v12.independent-read-only-static-review.v1",
            "status": (
                "PASS_STATIC_BYTES__RUNTIME_NOT_AUTHORIZED"
                if not failures else
                "FAIL_CLOSED_STATIC_REVIEW__RUNTIME_NOT_AUTHORIZED"),
            "read_only": True,
            "protocol_python_imported_or_executed": False,
            "protocol_or_runtime_files_written": False,
            "root": str(ROOT),
            "check_count": len(self.checks),
            "failed_check_count": len(failures),
            "failed_checks": failures,
            "checks": self.checks,
            "sections": sections,
        }


def decode_json_with_duplicates(raw: bytes, label: str) -> tuple[Any, list[str]]:
    duplicates: list[str] = []

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                duplicates.append(key)
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label}: JSON decode failed: {exc}") from exc
    return value, duplicates


def object_hash_details(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or "object_sha256" not in value:
        return {"declared": None, "computed": None, "matches": False}
    work = copy.deepcopy(value)
    declared = work.pop("object_sha256")
    computed = sha_bytes(canonical(work))
    return {
        "declared": declared,
        "computed": computed,
        "matches": isinstance(declared, str) and declared == computed,
    }


def module_assignment_nodes(tree: ast.Module) -> dict[str, list[ast.AST]]:
    result: dict[str, list[ast.AST]] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    result.setdefault(target.id, []).append(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            result.setdefault(node.target.id, []).append(node.value)
    return result


def safe_literal(node: ast.AST | None, env: Mapping[str, Any]) -> Any:
    if node is None:
        return MISSING
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        pass
    if isinstance(node, ast.Name):
        return env.get(node.id, MISSING)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = safe_literal(node.operand, env)
        if type(value) in {int, float, complex}:
            return value if isinstance(node.op, ast.UAdd) else -value
        return MISSING
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Mult)):
        left = safe_literal(node.left, env)
        right = safe_literal(node.right, env)
        if left is MISSING or right is MISSING:
            return MISSING
        allowed = (str, bytes, list, tuple, int)
        if not isinstance(left, allowed) or not isinstance(right, allowed):
            return MISSING
        try:
            return left + right if isinstance(node.op, ast.Add) else left * right
        except (TypeError, ValueError, OverflowError):
            return MISSING
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        values = [safe_literal(item, env) for item in node.elts]
        if any(value is MISSING for value in values):
            return MISSING
        if isinstance(node, ast.Tuple):
            return tuple(values)
        if isinstance(node, ast.List):
            return values
        try:
            return set(values)
        except TypeError:
            return MISSING
    if isinstance(node, ast.Dict):
        result: dict[Any, Any] = {}
        for key_node, value_node in zip(node.keys, node.values):
            if key_node is None:
                return MISSING
            key = safe_literal(key_node, env)
            value = safe_literal(value_node, env)
            if key is MISSING or value is MISSING:
                return MISSING
            try:
                result[key] = value
            except TypeError:
                return MISSING
        return result
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id in {"tuple", "list", "set", "frozenset"} and
            len(node.args) == 1 and not node.keywords):
        value = safe_literal(node.args[0], env)
        if value is MISSING:
            return MISSING
        try:
            return {"tuple": tuple, "list": list, "set": set,
                    "frozenset": frozenset}[node.func.id](value)
        except (TypeError, ValueError):
            return MISSING
    return MISSING


def module_literal_environment(tree: ast.Module) -> dict[str, Any]:
    assignments = module_assignment_nodes(tree)
    env: dict[str, Any] = {}
    for _ in range(max(2, len(assignments))):
        changed = False
        for name, nodes in assignments.items():
            if len(nodes) != 1 or name in env:
                continue
            value = safe_literal(nodes[0], env)
            if value is not MISSING:
                env[name] = value
                changed = True
        if not changed:
            break
    return env


def python_dict_literal_stats(tree: ast.Module, label: str) -> dict[str, Any]:
    duplicate_rows: list[dict[str, Any]] = []
    unhashable_rows: list[dict[str, Any]] = []
    literal_key_count = 0
    dict_count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        dict_count += 1
        seen: dict[Any, int] = {}
        for key_node in node.keys:
            if key_node is None:
                continue
            try:
                key = ast.literal_eval(key_node)
            except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                continue
            literal_key_count += 1
            try:
                if key in seen:
                    duplicate_rows.append({
                        "source": label, "line": node.lineno,
                        "key": repr(key), "first_key_index": seen[key],
                    })
                else:
                    seen[key] = literal_key_count
            except TypeError:
                unhashable_rows.append({
                    "source": label, "line": node.lineno, "key": repr(key)})
    return {
        "dict_literal_count": dict_count,
        "literal_key_count": literal_key_count,
        "duplicate_count": len(duplicate_rows),
        "duplicates": duplicate_rows,
        "unhashable_literal_key_count": len(unhashable_rows),
        "unhashable_literal_keys": unhashable_rows,
    }


def undefined_globals(source: str, label: str) -> list[str]:
    table = symtable.symtable(source, label, "exec")
    definitions = {
        symbol.get_name() for symbol in table.get_symbols()
        if (symbol.is_assigned() or symbol.is_imported() or
            symbol.is_namespace() or symbol.is_parameter())
    }
    allowed = set(dir(builtins)) | {
        "__file__", "__name__", "__package__", "__spec__", "__loader__",
        "__builtins__", "__annotations__", "__cached__",
    }
    bad: set[str] = set()

    def walk(scope: symtable.SymbolTable) -> None:
        for symbol in scope.get_symbols():
            if (symbol.is_referenced() and symbol.is_global() and
                    symbol.get_name() not in definitions | allowed):
                bad.add(symbol.get_name())
        for child in scope.get_children():
            walk(child)

    walk(table)
    return sorted(bad)


def decorators(function: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    return {ast.unparse(item) for item in function.decorator_list}


def excluded_constructor(node: ast.ClassDef) -> bool:
    bases = {ast.unparse(base) for base in node.bases}
    return bool(bases & {
        "Exception", "BaseException", "RuntimeError", "ValueError", "OSError",
    }) or any(base.endswith(".Structure") for base in bases)


def call_target(
        call: ast.Call,
        module_functions: Mapping[str, ast.FunctionDef | ast.AsyncFunctionDef],
        module_classes: Mapping[str, ast.ClassDef],
        current_class: ast.ClassDef | None,
) -> tuple[str, ast.FunctionDef | ast.AsyncFunctionDef | None, int] | None:
    function = call.func
    if isinstance(function, ast.Name) and function.id in module_functions:
        return "module_function", module_functions[function.id], 0
    if (isinstance(function, ast.Name) and function.id in module_classes and
            not excluded_constructor(module_classes[function.id])):
        initializer = next((
            item for item in module_classes[function.id].body
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            item.name == "__init__"), None)
        return "module_constructor", initializer, 1
    if (isinstance(function, ast.Attribute) and
            isinstance(function.value, ast.Name) and
            function.value.id in {"self", "cls"} and current_class is not None):
        method = next((
            item for item in current_class.body
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            item.name == function.attr), None)
        if method is not None:
            bound = 0 if "staticmethod" in decorators(method) else 1
            kind = (
                "self_instance_method" if function.value.id == "self" else
                "cls_class_method")
            return kind, method, bound
    if (isinstance(function, ast.Attribute) and
            isinstance(function.value, ast.Name) and
            function.value.id in module_classes):
        method = next((
            item for item in module_classes[function.value.id].body
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            item.name == function.attr), None)
        if method is not None:
            method_decorators = decorators(method)
            kind = (
                "localclass_static_method"
                if "staticmethod" in method_decorators else
                "localclass_class_method"
                if "classmethod" in method_decorators else
                "localclass_instance_method")
            bound = (
                0 if "staticmethod" in method_decorators else
                1 if "classmethod" in method_decorators else 0)
            return kind, method, bound
    return None


def arity_failure(
        call: ast.Call,
        target: ast.FunctionDef | ast.AsyncFunctionDef | None,
        bound: int,
) -> bool:
    if target is None:
        return bool(call.args or call.keywords)
    arguments = target.args
    positional = list(arguments.posonlyargs) + list(arguments.args)
    default_start = len(positional) - len(arguments.defaults)
    required = [
        item.arg for index, item in enumerate(positional)
        if index < default_start][bound:]
    maximum = None if arguments.vararg else len(positional) - bound
    if maximum is not None and len(call.args) > maximum:
        return True
    keyword_names = [item.arg for item in call.keywords]
    legal = ([item.arg for item in positional[bound:]] +
             [item.arg for item in arguments.kwonlyargs])
    if arguments.kwarg is None and any(name not in legal for name in keyword_names):
        return True
    provided = {name for name in keyword_names if name is not None}
    provided.update(
        item.arg for item in positional[bound:bound + len(call.args)])
    missing = [name for name in required if name not in provided]
    missing.extend(
        item.arg for item, default in
        zip(arguments.kwonlyargs, arguments.kw_defaults)
        if default is None and item.arg not in provided)
    return bool(missing)


def callsite_row(label: str, call: ast.Call, kind: str) -> list[Any]:
    return [
        label, call.lineno, call.col_offset, call.end_lineno,
        call.end_col_offset, kind,
        ast.dump(call.func, annotate_fields=True, include_attributes=False),
        len(call.args), [item.arg for item in call.keywords],
    ]


def callsite_census_parent_map(
        sources: Sequence[tuple[str, bytes]],
) -> tuple[list[list[Any]], Counter[str], int]:
    rows: list[list[Any]] = []
    kinds: Counter[str] = Counter()
    failures = 0
    for label, raw in sources:
        tree = ast.parse(raw, filename=label, mode="exec")
        parents: dict[ast.AST, ast.AST] = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent
        functions = {
            node.name: node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        classes = {
            node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
        for call in (node for node in ast.walk(tree) if isinstance(node, ast.Call)):
            parent = parents.get(call)
            current_class = None
            while parent is not None:
                if isinstance(parent, ast.ClassDef):
                    current_class = parent
                    break
                parent = parents.get(parent)
            resolved = call_target(call, functions, classes, current_class)
            if resolved is None:
                continue
            kind, target, bound = resolved
            kinds[kind] += 1
            rows.append(callsite_row(label, call, kind))
            failures += int(arity_failure(call, target, bound))
    return sorted(rows), kinds, failures


def callsite_census_visitor(
        sources: Sequence[tuple[str, bytes]],
) -> tuple[list[list[Any]], Counter[str], int]:
    rows: list[list[Any]] = []
    kinds: Counter[str] = Counter()
    failures = 0
    for label, raw in sources:
        tree = ast.parse(raw, filename=label, mode="exec")
        functions = {
            node.name: node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        classes = {
            node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}

        class Visitor(ast.NodeVisitor):
            def __init__(self) -> None:
                self.stack: list[ast.ClassDef] = []

            def visit_ClassDef(self, node: ast.ClassDef) -> None:
                self.stack.append(node)
                self.generic_visit(node)
                self.stack.pop()

            def visit_Call(self, node: ast.Call) -> None:
                nonlocal failures
                resolved = call_target(
                    node, functions, classes,
                    self.stack[-1] if self.stack else None)
                if resolved is not None:
                    kind, target, bound = resolved
                    kinds[kind] += 1
                    rows.append(callsite_row(label, node, kind))
                    failures += int(arity_failure(node, target, bound))
                self.generic_visit(node)

        Visitor().visit(tree)
    return sorted(rows), kinds, failures


def callsite_summary(sources: Sequence[tuple[str, bytes]]) -> dict[str, Any]:
    rows_a, kinds_a, arity_a = callsite_census_parent_map(sources)
    rows_b, kinds_b, arity_b = callsite_census_visitor(sources)
    implementation_a = {
        "row_count": len(rows_a),
        "census_sha256": sha_bytes(canonical(rows_a)),
        "kind_census": {
            kind: kinds_a.get(kind, 0) for kind in CALLSITE_KINDS},
        "arity_failure_count": arity_a,
    }
    implementation_b = {
        "row_count": len(rows_b),
        "census_sha256": sha_bytes(canonical(rows_b)),
        "kind_census": {
            kind: kinds_b.get(kind, 0) for kind in CALLSITE_KINDS},
        "arity_failure_count": arity_b,
    }
    return {
        "implementation_A_B_rows_equal": rows_a == rows_b,
        "implementation_A_B_kind_census_equal": kinds_a == kinds_b,
        "implementation_A_B_arity_equal": arity_a == arity_b,
        "implementation_A": implementation_a,
        "implementation_B": implementation_b,
        "row_count": implementation_a["row_count"],
        "census_sha256": implementation_a["census_sha256"],
        "kind_census": implementation_a["kind_census"],
        "arity_failure_count": arity_a,
    }


def exact_helper_review(
        ordered_trees: Sequence[tuple[str, ast.Module]],
        environments: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    digests: dict[str, str] = {}
    return_key_orders: dict[str, list[str]] = {}
    calls: list[dict[str, Any]] = []
    declared_digests: dict[str, Any] = {}
    declared_key_orders: dict[str, list[str]] = {}
    object_pins: dict[str, Any] = {}
    digest_names = {
        "producer": "V10_COLON_PREFIX_HELPER_NORMALIZED_AST_SHA256",
        "consumer": "V10_COLON_PREFIX_WITNESS_HELPER_AST_SHA256",
        "launcher": "V10_COLON_PREFIX_HELPER_NORMALIZED_AST_SHA256",
    }
    for role, tree in ordered_trees:
        helpers = [
            node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == HELPER_NAME]
        if len(helpers) != 1:
            raise ValueError(f"{role}: expected one module-level {HELPER_NAME}")
        helper = helpers[0]
        digests[role] = sha_bytes(ast.dump(
            helper, annotate_fields=True,
            include_attributes=False).encode("utf-8"))
        dictionaries = [
            node for node in ast.walk(helper)
            if isinstance(node, ast.Dict) and len(node.keys) >= 35 and
            all(isinstance(key, ast.Constant) and isinstance(key.value, str)
                for key in node.keys if key is not None)]
        if len(dictionaries) != 1:
            raise ValueError(f"{role}: expected one helper witness dictionary")
        return_key_orders[role] = [
            key.value for key in dictionaries[0].keys
            if isinstance(key, ast.Constant)] + ["object_sha256"]

        parent: dict[ast.AST, ast.AST] = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parent[child] = node
        loaded = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and
            node.id == HELPER_NAME]
        owned_calls: list[tuple[ast.Call, ast.FunctionDef | ast.AsyncFunctionDef]] = []
        for name in loaded:
            call = parent.get(name)
            if not (isinstance(call, ast.Call) and call.func is name and
                    len(call.args) == 2 and not call.keywords):
                raise ValueError(f"{role}: helper has a non-direct/non-exact callsite")
            cursor: ast.AST = call
            owner: ast.FunctionDef | ast.AsyncFunctionDef | None = None
            while cursor in parent:
                cursor = parent[cursor]
                if isinstance(cursor, ast.Lambda):
                    raise ValueError(f"{role}: helper call is nested in lambda")
                if isinstance(cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    owner = cursor
                    break
            if owner is None:
                raise ValueError(f"{role}: helper call lacks enclosing function")
            owned_calls.append((call, owner))
        owners: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
        counts: Counter[int] = Counter()
        for call, owner in sorted(
                owned_calls, key=lambda pair: (pair[0].lineno, pair[0].col_offset)):
            if id(owner) not in counts:
                owners.append(owner)
            counts[id(owner)] += 1
        for owner in sorted(owners, key=lambda item: (item.lineno, item.col_offset)):
            calls.append({
                "source_role": role,
                "enclosing_function": owner.name,
                "direct_call_count": counts[id(owner)],
            })

        env = environments[role]
        declared_digests[role] = env.get(digest_names[role])
        assignments = module_assignment_nodes(tree)
        if role in {"producer", "launcher"}:
            order_node = assignments.get("V10_COLON_PREFIX_WITNESS_KEY_ORDER", [])
            value = safe_literal(order_node[0], env) if len(order_node) == 1 else MISSING
            declared_key_orders[role] = list(value) if isinstance(value, tuple) else []
            object_pins[role] = env.get("V10_COLON_PREFIX_WITNESS_OBJECT_PIN")
        else:
            witness_nodes = assignments.get("V10_COLON_PREFIX_WITNESS", [])
            if len(witness_nodes) != 1 or not isinstance(witness_nodes[0], ast.Dict):
                raise ValueError("consumer: missing direct V10 witness dictionary")
            witness = witness_nodes[0]
            declared_key_orders[role] = [
                key.value for key in witness.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, str)]
            object_value = next((
                value for key, value in zip(witness.keys, witness.values)
                if isinstance(key, ast.Constant) and key.value == "object_sha256"), None)
            object_pins[role] = safe_literal(object_value, env)
    return {
        "normalized_function_ast_sha256": digests,
        "all_three_function_asts_equal": len(set(digests.values())) == 1,
        "declared_helper_ast_sha256": declared_digests,
        "all_declared_helper_digests_match_ast": all(
            declared_digests[role] == digests[role] for role in digests),
        "helper_return_exact40_key_orders": return_key_orders,
        "declared_exact40_key_orders": declared_key_orders,
        "all_exact40_key_orders_equal": (
            len({tuple(value) for value in return_key_orders.values()}) == 1 and
            len({tuple(value) for value in declared_key_orders.values()}) == 1 and
            next(iter(return_key_orders.values())) ==
            next(iter(declared_key_orders.values())) and
            len(next(iter(declared_key_orders.values()))) == 40),
        "witness_object_pins": object_pins,
        "all_witness_object_pins_equal": len(set(object_pins.values())) == 1,
        "ordered_callsite_census": calls,
        "ordered_callsite_census_sha256": sha_bytes(canonical(calls)),
        "exact_expected_callsites": calls == EXPECTED_HELPER_CALLSITES,
    }


def string_collection(
        node: ast.AST, module_env: Mapping[str, Any],
        local_env: Mapping[str, set[str]],
) -> set[str] | None:
    if isinstance(node, ast.Name):
        if node.id in local_env:
            return local_env[node.id]
        value = module_env.get(node.id, MISSING)
        if isinstance(value, (tuple, list, set, frozenset)) and all(
                isinstance(item, str) for item in value):
            return set(value)
        return None
    if isinstance(node, (ast.Set, ast.Tuple, ast.List)):
        values = [safe_literal(item, module_env) for item in node.elts]
        if all(isinstance(value, str) for value in values):
            return set(values)
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id in {"set", "tuple", "list", "frozenset"} and
            len(node.args) == 1 and not node.keywords):
        return string_collection(node.args[0], module_env, local_env)
    return None


def static_audit_keyset_closures(
        tree: ast.Module, function_name: str, module_env: Mapping[str, Any],
) -> dict[str, list[str]]:
    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == function_name]
    if len(functions) != 1:
        raise ValueError(f"expected one {function_name}")
    function = functions[0]
    local_env: dict[str, set[str]] = {}
    for node in ast.walk(function):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name)):
            value = string_collection(node.value, module_env, local_env)
            if value is not None:
                local_env[node.targets[0].id] = value
    result: dict[str, set[str]] = {}
    for comparison in (node for node in ast.walk(function)
                       if isinstance(node, ast.Compare)):
        pairs = zip(
            [comparison.left] + list(comparison.comparators[:-1]),
            comparison.comparators)
        for left, right in pairs:
            for set_call, other in ((left, right), (right, left)):
                if not (isinstance(set_call, ast.Call) and
                        isinstance(set_call.func, ast.Name) and
                        set_call.func.id == "set" and len(set_call.args) == 1 and
                        not set_call.keywords and
                        isinstance(set_call.args[0], ast.Name)):
                    continue
                keys = string_collection(other, module_env, local_env)
                if keys is not None:
                    result.setdefault(set_call.args[0].id, set()).update(keys)
    return {name: sorted(keys) for name, keys in result.items()}


def find_output_shapes(tree: ast.Module, env: Mapping[str, Any]) -> list[dict[str, int]]:
    shapes: list[dict[str, int]] = []
    seen: set[tuple[tuple[str, int], ...]] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        value = safe_literal(node, env)
        if not (isinstance(value, dict) and set(value) == SHAPE_KEYS and
                all(type(item) is int for item in value.values())):
            continue
        identity = tuple(sorted(value.items()))
        if identity not in seen:
            seen.add(identity)
            shapes.append(value)
    return shapes


def resolve_json_pointer(root: Any, reference: str) -> bool:
    if reference == "#":
        return True
    if not reference.startswith("#/"):
        return False
    current = root
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return False
    return True


def schema_summary(schema: Mapping[str, Any]) -> dict[str, Any]:
    stack: list[Any] = [schema]
    object_nodes: list[dict[str, Any]] = []
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            object_nodes.append(value)
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
    references = [node["$ref"] for node in object_nodes if "$ref" in node]
    unresolved = [
        reference for reference in references
        if not isinstance(reference, str) or
        not resolve_json_pointer(schema, reference)]
    closed = [
        node for node in object_nodes
        if node.get("type") == "object" and
        node.get("additionalProperties") is False]
    mismatches = [
        node for node in closed
        if set(node.get("required", [])) != set(node.get("properties", {}))]
    actual_keywords = sorted({
        key for node in object_nodes for key in node if key in SCHEMA_KEYWORDS})
    definitions = schema.get("$defs", {})
    shape_counts = {
        name: len(definitions[name].get("properties", {}))
        for name in SHAPE_KEYS
        if isinstance(definitions, dict) and
        isinstance(definitions.get(name), dict)}
    return {
        "definition_count": len(definitions) if isinstance(definitions, dict) else -1,
        "ref_count": len(references),
        "unresolved_ref_count": len(unresolved),
        "unresolved_refs": unresolved,
        "closed_object_count": len(closed),
        "closed_object_required_property_mismatch_count": len(mismatches),
        "actual_schema_keyword_universe": actual_keywords,
        "actual_schema_keyword_universe_sha256": sha_bytes(canonical(actual_keywords)),
        "unsupported_schema_keywords": sorted(
            set(actual_keywords) - SUPPORTED_SCHEMA_KEYWORDS),
        "output_shape_key_counts": shape_counts,
    }


def pin_normalized_launcher_ast(tree: ast.Module) -> dict[str, Any]:
    work = copy.deepcopy(tree)
    flag_owners = [
        node for node in work.body
        if ((isinstance(node, ast.Assign) and len(node.targets) == 1 and
             isinstance(node.targets[0], ast.Name) and
             node.targets[0].id == "FINAL_BASE7_PINS_INSTALLED") or
            (isinstance(node, ast.AnnAssign) and
             isinstance(node.target, ast.Name) and
             node.target.id == "FINAL_BASE7_PINS_INSTALLED"))]
    if len(flag_owners) != 1:
        raise ValueError("launcher: expected one final BASE7 flag")
    flag_owners[0].value = ast.Constant(False)
    functions = [
        node for node in work.body
        if isinstance(node, ast.FunctionDef) and
        node.name == "configure_workspace_paths"]
    if len(functions) != 1:
        raise ValueError("launcher: expected one workspace configurator")
    tables = [
        node for node in functions[0].body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "BASE7_PINS"]
    if len(tables) != 1 or not isinstance(tables[0].value, ast.Dict):
        raise ValueError("launcher: expected one direct BASE7 dict")
    table = tables[0].value
    names = [key.id if isinstance(key, ast.Name) else None for key in table.keys]
    expected = [
        "V11_OFFICIAL_REJECTION", "SCHEMA", "CONTRACT", "PRODUCER",
        "CONSUMER", "TRANSITION", "AUDIT"]
    if names != expected:
        raise ValueError(f"launcher: BASE7 order mismatch: {names!r}")
    predecessor_before = ast.dump(table.values[0], include_attributes=False)
    for index, name in enumerate(names[1:], 1):
        table.values[index] = ast.Tuple(elts=[
            ast.Constant("f" * 64),
            ast.Constant(
                "e" * 64 if name in {"CONTRACT", "TRANSITION", "AUDIT"}
                else None),
        ], ctx=ast.Load())
    predecessor_after = ast.dump(table.values[0], include_attributes=False)
    digest = sha_bytes(ast.dump(
        work, annotate_fields=True,
        include_attributes=False).encode("utf-8"))
    return {
        "algorithm": (
            "PYTHON_AST_DUMP_NO_ATTRIBUTES__FORCE_FINAL_BASE7_FALSE__"
            "CURRENT_V12_SIX_BASE7_FILE_F64_OBJECT_E64_OR_NONE__"
            "PRESERVE_V11_REJECTION_AND_ALL_HISTORICAL_PINS_V1"),
        "base7_key_order": names,
        "predecessor_pin_preserved": predecessor_before == predecessor_after,
        "sha256": digest,
    }


def launcher_base7_state(
        tree: ast.Module, env: Mapping[str, Any],
) -> dict[str, Any]:
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and
        node.name == "configure_workspace_paths"]
    if len(functions) != 1:
        raise ValueError("launcher: expected one workspace configurator")
    tables = [
        node.value for node in functions[0].body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "BASE7_PINS" and isinstance(node.value, ast.Dict)]
    if len(tables) != 1:
        raise ValueError("launcher: expected one BASE7 dict")
    table = tables[0]
    values: dict[str, Any] = {}
    draft_references: list[str] = []
    for key, value in zip(table.keys, table.values):
        if not isinstance(key, ast.Name):
            continue
        evaluated = safe_literal(value, env)
        values[key.id] = None if evaluated is MISSING else evaluated
        draft_references.extend(sorted({
            node.id for node in ast.walk(value)
            if isinstance(node, ast.Name) and node.id.startswith("_DRAFT_")}))
    return {
        "flag": env.get("FINAL_BASE7_PINS_INSTALLED"),
        "pins": values,
        "draft_references": sorted(set(draft_references)),
    }


def lstat_exists(path: Path) -> bool:
    try:
        os.lstat(path)
    except FileNotFoundError:
        return False
    return True


def runtime_surface_summary() -> dict[str, Any]:
    names = [
        f"c79g-v12-candidate-a-{CHECKPOINT}",
        f"c79g-v12-candidate-b-{CHECKPOINT}",
        f"c79g-v12-verification-a-{CHECKPOINT}",
        f"c79g-v12-verification-b-{CHECKPOINT}",
        f"c79g-v12-committed-completion-{CHECKPOINT}",
        f"c79g-v12-rejections-{CHECKPOINT}",
        f".c79g-v12-candidate-stage-a-{CHECKPOINT}",
        f".c79g-v12-candidate-stage-b-{CHECKPOINT}",
        f".c79g-v12-verification-stage-a-{CHECKPOINT}",
        f".c79g-v12-verification-stage-b-{CHECKPOINT}",
        f".c79g-v12-completion-stage-{CHECKPOINT}",
    ]
    authority = RUNTIME / "cm2-global-authority-heads"
    explicit = [RUNTIME / name for name in names] + [
        authority / f"c79g-v12-{CHECKPOINT}.seal",
        authority / f".c79g-v12-authority-stage-{CHECKPOINT}.seal",
    ]
    present = {str(path.relative_to(ROOT)) for path in explicit if lstat_exists(path)}
    if RUNTIME.is_dir():
        present.update(
            str(path.relative_to(ROOT)) for path in RUNTIME.iterdir()
            if "c79g-v12" in path.name.lower())
    if authority.is_dir():
        present.update(
            str(path.relative_to(ROOT)) for path in authority.iterdir()
            if "c79g-v12" in path.name.lower())
    return {
        "enumerated_surface_count": len(explicit),
        "present_surface_count": len(present),
        "present_surfaces": sorted(present),
    }


def actual_audit_keysets(audit: Mapping[str, Any]) -> dict[str, list[str]]:
    dual = audit.get("dual_independent_static_checkers", {})
    if not isinstance(dual, dict):
        dual = {}
    mapping: dict[str, Any] = {
        "audit": audit,
        "dual": dual,
        "checker_a": dual.get("checker_A", {}),
        "checker_b": dual.get("checker_B", {}),
        "checker_c": dual.get(
            "checker_C_common_census_and_pin_normalized_ast_reproduction", {}),
        "helper_consensus": dual.get("v10_colon_prefix_helper_consensus", {}),
    }
    return {
        name: sorted(value) if isinstance(value, dict) else []
        for name, value in mapping.items()}


def pin_mismatch_rows(
        pins: Mapping[str, Any], expected: Mapping[str, tuple[str, str | None]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, expected_value in expected.items():
        observed = pins.get(name)
        normalized = tuple(observed) if isinstance(observed, (tuple, list)) else observed
        if normalized != expected_value:
            rows.append({"name": name, "observed": normalized,
                         "expected": expected_value})
    return rows


def review() -> dict[str, Any]:
    report = Report()
    sections: dict[str, Any] = {}
    snapshots: dict[Path, tuple[int, ...]] = {}

    def snapshot(path: Path) -> bytes:
        raw, identity = read_stable_regular_file(path)
        previous = snapshots.setdefault(path, identity)
        if previous != identity:
            raise ValueError(f"{path}: identity differs across review reads")
        return raw

    json_values: dict[str, Any] = {}
    json_duplicates: dict[str, list[str]] = {}
    json_file_hashes: dict[str, str] = {}
    for name, path in V12_JSON.items():
        raw = snapshot(path)
        value, duplicates = decode_json_with_duplicates(raw, str(path))
        json_values[name] = value
        json_duplicates[name] = duplicates
        json_file_hashes[name] = sha_bytes(raw)
    v11_audit_raw = snapshot(V11_AUDIT)
    v11_audit, v11_audit_duplicates = decode_json_with_duplicates(
        v11_audit_raw, str(V11_AUDIT))
    json_duplicates["v11_audit_calibration"] = v11_audit_duplicates
    sections["json_duplicate_keys"] = json_duplicates
    report.add(
        "strict_json_duplicate_key_count_zero",
        sum(len(items) for items in json_duplicates.values()) == 0,
        duplicate_keys=json_duplicates)
    report.add(
        "v12_json_roots_are_objects",
        all(isinstance(value, dict) for value in json_values.values()),
        root_types={name: type(value).__name__ for name, value in json_values.items()})
    schema = json_values["schema"]
    contract = json_values["contract"]
    transition = json_values["transition"]
    audit = json_values["audit"]
    if not all(isinstance(value, dict) for value in (schema, contract, transition, audit)):
        raise ValueError("one or more required v12 JSON roots is not an object")

    object_closures = {
        name: object_hash_details(value)
        for name, value in {
            "contract": contract, "transition": transition, "audit": audit,
        }.items()}
    sections["json_object_closures"] = object_closures
    report.add(
        "contract_transition_audit_object_hashes_close",
        all(item["matches"] for item in object_closures.values()),
        closures=object_closures)

    raw_v12 = [(role, path.name, snapshot(path)) for role, path in V12_PYTHON]
    trees: dict[str, ast.Module] = {}
    environments: dict[str, dict[str, Any]] = {}
    python_stats: dict[str, Any] = {}
    total_python_duplicates = 0
    total_literal_dicts = 0
    total_starred = 0
    total_double_star = 0
    all_undefined: dict[str, list[str]] = {}
    for role, label, raw in raw_v12:
        source = raw.decode("utf-8")
        tree = ast.parse(source, filename=label, mode="exec")
        compile(tree, label, "exec", dont_inherit=True)
        trees[role] = tree
        environments[role] = module_literal_environment(tree)
        dict_stats = python_dict_literal_stats(tree, label)
        undefined = undefined_globals(source, label)
        starred = sum(
            isinstance(argument, ast.Starred)
            for node in ast.walk(tree) if isinstance(node, ast.Call)
            for argument in node.args)
        double_star = sum(
            keyword.arg is None
            for node in ast.walk(tree) if isinstance(node, ast.Call)
            for keyword in node.keywords)
        python_stats[role] = {
            "path": label,
            "file_sha256": sha_bytes(raw),
            "ast_parse_and_in_memory_compile": True,
            "dict_literals": dict_stats,
            "undefined_globals": undefined,
            "starred_positional_total": starred,
            "double_star_keyword_total": double_star,
        }
        total_python_duplicates += dict_stats["duplicate_count"]
        total_literal_dicts += dict_stats["dict_literal_count"]
        total_starred += starred
        total_double_star += double_star
        all_undefined[role] = undefined
    sections["python_static"] = python_stats
    report.add("three_python_ast_parse_and_in_memory_compile", len(trees) == 3)
    report.add(
        "python_literal_dict_duplicate_key_count_zero",
        total_python_duplicates == 0,
        duplicate_count=total_python_duplicates)
    report.add(
        "python_undefined_global_count_zero",
        not any(all_undefined.values()), undefined_globals=all_undefined)
    report.add(
        "python_star_and_double_star_calls_absent",
        total_starred == 0 and total_double_star == 0,
        starred_positional_total=total_starred,
        double_star_keyword_total=total_double_star)

    v11_sources = [(path.name, snapshot(path)) for _, path in V11_PYTHON]
    v11_census = callsite_summary(v11_sources)
    v11_dual = (
        v11_audit.get("dual_independent_static_checkers", {})
        if isinstance(v11_audit, dict) else {})
    v11_checker_b = v11_dual.get("checker_B", {}) if isinstance(v11_dual, dict) else {}
    declared_v11_count = (
        v11_checker_b.get("common_ordered_callsite_row_count")
        if isinstance(v11_checker_b, dict) else None)
    declared_v11_digest = (
        v11_checker_b.get("common_ordered_callsite_census_sha256")
        if isinstance(v11_checker_b, dict) else None)
    calibration_passed = (
        v11_census["implementation_A_B_rows_equal"] and
        v11_census["implementation_A_B_kind_census_equal"] and
        v11_census["implementation_A_B_arity_equal"] and
        v11_census["arity_failure_count"] == 0 and
        v11_census["row_count"] == EXPECTED_V11_CALLSITE_COUNT == declared_v11_count and
        v11_census["census_sha256"] ==
            EXPECTED_V11_CALLSITE_SHA256 == declared_v11_digest)
    sections["v11_callsite_calibration"] = {
        **v11_census,
        "known_row_count": EXPECTED_V11_CALLSITE_COUNT,
        "known_sha256": EXPECTED_V11_CALLSITE_SHA256,
        "v11_audit_declared_row_count": declared_v11_count,
        "v11_audit_declared_sha256": declared_v11_digest,
        "calibrated": calibration_passed,
    }
    report.add(
        "general_callsite_census_calibrates_to_v11_2964_d6d1",
        calibration_passed,
        observed_count=v11_census["row_count"],
        observed_sha256=v11_census["census_sha256"],
        expected_count=EXPECTED_V11_CALLSITE_COUNT,
        expected_sha256=EXPECTED_V11_CALLSITE_SHA256)

    v12_sources = [(label, raw) for _, label, raw in raw_v12]
    v12_census = callsite_summary(v12_sources)
    v12_census["authoritative_only_if_v11_calibrated"] = calibration_passed
    sections["v12_callsite_census"] = v12_census
    dual = audit.get("dual_independent_static_checkers", {})
    if not isinstance(dual, dict):
        dual = {}
    checker_a = dual.get("checker_A", {})
    checker_b = dual.get("checker_B", {})
    checker_c = dual.get(
        "checker_C_common_census_and_pin_normalized_ast_reproduction", {})
    declared_census_values = {
        "checker_A_count": checker_a.get("wider_local_callsite_census_row_count")
            if isinstance(checker_a, dict) else None,
        "checker_A_sha256": checker_a.get("wider_local_callsite_census_sha256")
            if isinstance(checker_a, dict) else None,
        "checker_B_count": checker_b.get("common_ordered_callsite_row_count")
            if isinstance(checker_b, dict) else None,
        "checker_B_sha256": checker_b.get("common_ordered_callsite_census_sha256")
            if isinstance(checker_b, dict) else None,
        "checker_C_count": checker_c.get("common_ordered_callsite_row_count")
            if isinstance(checker_c, dict) else None,
        "checker_C_sha256": checker_c.get("common_ordered_callsite_census_sha256")
            if isinstance(checker_c, dict) else None,
        "checker_C_kind_census": checker_c.get("common_callsite_kind_census")
            if isinstance(checker_c, dict) else None,
    }
    census_declared_match = (
        calibration_passed and
        v12_census["implementation_A_B_rows_equal"] and
        v12_census["implementation_A_B_kind_census_equal"] and
        v12_census["implementation_A_B_arity_equal"] and
        v12_census["arity_failure_count"] == 0 and
        all(declared_census_values[key] == v12_census["row_count"]
            for key in ("checker_A_count", "checker_B_count", "checker_C_count")) and
        all(declared_census_values[key] == v12_census["census_sha256"]
            for key in ("checker_A_sha256", "checker_B_sha256", "checker_C_sha256")) and
        declared_census_values["checker_C_kind_census"] ==
            v12_census["kind_census"])
    report.add(
        "v12_common_callsite_census_reproduces_all_audit_claims",
        census_declared_match,
        observed=v12_census, declared=declared_census_values)
    report.add(
        "audit_python_literal_dict_and_undefined_counts_match",
        isinstance(checker_a, dict) and
        checker_a.get("python_literal_dict_count") == total_literal_dicts and
        checker_a.get("python_literal_dict_duplicate_key_count") ==
            total_python_duplicates and
        checker_a.get("undefined_global_count") == sum(
            len(items) for items in all_undefined.values()) and
        checker_a.get("python_AST_and_compile_in_memory_file_count") == 3,
        observed_literal_dict_count=total_literal_dicts,
        audit_literal_dict_count=(checker_a.get("python_literal_dict_count")
                                  if isinstance(checker_a, dict) else None))

    helper = exact_helper_review(
        [(role, trees[role]) for role, _ in V12_PYTHON], environments)
    sections["exact40_helper"] = helper
    helper_passed = (
        helper["all_three_function_asts_equal"] and
        helper["all_declared_helper_digests_match_ast"] and
        helper["all_exact40_key_orders_equal"] and
        helper["all_witness_object_pins_equal"] and
        helper["exact_expected_callsites"] and
        helper["ordered_callsite_census_sha256"] ==
            EXPECTED_HELPER_CALLSITE_SHA256)
    report.add(
        "exact40_three_helper_ast_key_order_and_callsites_close",
        helper_passed, helper=helper)
    helper_consensus = dual.get("v10_colon_prefix_helper_consensus", {})
    helper_audit_match = (
        isinstance(helper_consensus, dict) and
        helper_consensus.get("normalized_helper_ast_sha256") ==
            next(iter(helper["normalized_function_ast_sha256"].values())) and
        helper_consensus.get("witness_exact_key_order") ==
            next(iter(helper["declared_exact40_key_orders"].values())) and
        helper_consensus.get("witness_exact_key_count") == 40 and
        helper_consensus.get("witness_object_sha256") ==
            next(iter(helper["witness_object_pins"].values())) and
        helper_consensus.get("ordered_callsite_census") ==
            helper["ordered_callsite_census"] and
        helper_consensus.get("ordered_callsite_census_sha256") ==
            helper["ordered_callsite_census_sha256"] and
        helper_consensus.get("all_three_helpers_equal") is True and
        helper_consensus.get("all_callsites_exact") is True)
    report.add(
        "audit_exact40_helper_consensus_matches_independent_derivation",
        helper_audit_match,
        audit_helper_consensus_present=isinstance(helper_consensus, dict) and
            bool(helper_consensus))

    closure_functions = {
        "producer": "_validate_final_static_audit",
        "consumer": "_validate_final_static_audit",
        "launcher": "validate_final_static_audit",
    }
    closures = {
        role: static_audit_keyset_closures(
            trees[role], closure_functions[role], environments[role])
        for role in closures_function_order(closure_functions)}
    sections["three_source_audit_keysets"] = closures
    closure_names = {
        "audit", "dual", "checker_a", "checker_b", "checker_c",
        "helper_consensus"}
    three_way_keysets_equal = all(
        name in closures[role]
        for role in closures for name in closure_names) and all(
        closures["producer"][name] == closures["consumer"][name] ==
        closures["launcher"][name] for name in closure_names)
    report.add(
        "producer_consumer_launcher_audit_keysets_equal",
        three_way_keysets_equal, closures=closures)
    actual_keysets = actual_audit_keysets(audit)
    expected_keysets = closures.get("producer", {})
    keyset_mismatches = {
        name: {
            "missing": sorted(set(expected_keysets.get(name, [])) -
                              set(actual_keysets.get(name, []))),
            "extra": sorted(set(actual_keysets.get(name, [])) -
                            set(expected_keysets.get(name, []))),
        }
        for name in closure_names
        if expected_keysets.get(name, []) != actual_keysets.get(name, [])}
    sections["audit_json_keyset_mismatches"] = keyset_mismatches
    report.add(
        "audit_json_matches_three_source_exact_keysets",
        three_way_keysets_equal and not keyset_mismatches,
        mismatches=keyset_mismatches)

    input_orders = {
        "producer": environments["producer"].get("STATIC_AUDIT_INPUT_KEY_ORDER"),
        "consumer": environments["consumer"].get("STATIC_AUDIT_INPUT_EXACT37"),
        "launcher": environments["launcher"].get(
            "FINAL_STATIC_AUDIT_INPUT_KEY_ORDER"),
    }
    input_order_equal = (
        all(isinstance(value, tuple) for value in input_orders.values()) and
        len({value for value in input_orders.values()}) == 1 and
        len(input_orders["producer"]) == 37)
    input_order_digest = (
        sha_bytes(canonical(list(input_orders["producer"])))
        if isinstance(input_orders["producer"], tuple) else None)
    input_digest_claims = {
        "producer": environments["producer"].get(
            "STATIC_AUDIT_INPUT_KEY_ORDER_SHA256"),
        "consumer": environments["consumer"].get(
            "STATIC_AUDIT_INPUT_EXACT37_ORDER_SHA256"),
    }
    source_input_constants_passed = (
        input_order_equal and
        all(value == input_order_digest
            for value in input_digest_claims.values()))
    audit_inputs_a = checker_a.get("input_sha256", {}) if isinstance(checker_a, dict) else {}
    audit_inputs_b = checker_b.get("input_sha256", {}) if isinstance(checker_b, dict) else {}
    input_constants_passed = (
        input_order_equal and
        all(value == input_order_digest for value in input_digest_claims.values()) and
        isinstance(audit_inputs_a, dict) and isinstance(audit_inputs_b, dict) and
        list(audit_inputs_a) == list(input_orders["producer"]) and
        list(audit_inputs_b) == list(input_orders["producer"]) and
        audit_inputs_a == audit_inputs_b)
    sections["static_audit_input_constants"] = {
        "orders": input_orders,
        "derived_order_sha256": input_order_digest,
        "declared_order_sha256": input_digest_claims,
        "audit_checker_A_input_keys": list(audit_inputs_a),
        "audit_checker_B_input_keys": list(audit_inputs_b),
    }
    report.add(
        "three_source_exact37_audit_input_constants_and_audit_match",
        input_constants_passed)

    checkpoint_values = {
        "producer": environments["producer"].get("CHECKPOINT_OBJECT_PIN"),
        "consumer": environments["consumer"].get("CHECKPOINT_OBJECT_PIN"),
        "launcher": environments["launcher"].get("CHECKPOINT"),
    }
    status_present = {
        role: any(
            isinstance(node, ast.Constant) and node.value == EXPECTED_AUDIT_STATUS
            for node in ast.walk(trees[role]))
        for role in trees}
    schema_present = {
        role: any(
            isinstance(node, ast.Constant) and node.value == EXPECTED_AUDIT_SCHEMA
            for node in ast.walk(trees[role]))
        for role in trees}
    source_protocol_constants_passed = (
        all(value == CHECKPOINT for value in checkpoint_values.values()) and
        all(status_present.values()) and all(schema_present.values()))
    report.add(
        "three_source_checkpoint_audit_schema_and_status_constants_equal",
        source_protocol_constants_passed and
        audit.get("schema") == EXPECTED_AUDIT_SCHEMA and
        audit.get("status") == EXPECTED_AUDIT_STATUS,
        checkpoints=checkpoint_values,
        source_status_literal_present=status_present,
        source_schema_literal_present=schema_present,
        audit_schema=audit.get("schema"), audit_status=audit.get("status"))

    output_shapes = {
        role: find_output_shapes(trees[role], environments[role])
        for role in trees}
    unique_shapes = {
        role: values[0] if len(values) == 1 else None
        for role, values in output_shapes.items()}
    shapes_equal = (
        all(value is not None for value in unique_shapes.values()) and
        unique_shapes["producer"] == unique_shapes["consumer"] ==
        unique_shapes["launcher"])
    sections["three_source_output_shapes"] = output_shapes

    schema_details = schema_summary(schema)
    sections["schema"] = schema_details
    claimed_schema = audit.get("schema_and_constructor_closure", {})
    if not isinstance(claimed_schema, dict):
        claimed_schema = {}
    schema_claims_match = (
        claimed_schema.get("schema_definition_count") ==
            schema_details["definition_count"] and
        claimed_schema.get("schema_ref_count") == schema_details["ref_count"] and
        claimed_schema.get("unresolved_schema_ref_count") ==
            schema_details["unresolved_ref_count"] and
        claimed_schema.get("closed_object_count") ==
            schema_details["closed_object_count"] and
        claimed_schema.get("closed_object_required_property_mismatch_count") ==
            schema_details["closed_object_required_property_mismatch_count"] and
        claimed_schema.get("actual_schema_keyword_universe") ==
            schema_details["actual_schema_keyword_universe"] and
        claimed_schema.get("actual_schema_keyword_universe_sha256") ==
            schema_details["actual_schema_keyword_universe_sha256"] and
        isinstance(claimed_schema.get("output_shape_key_counts"), dict) and
        all(claimed_schema["output_shape_key_counts"].get(key) == value
            for key, value in
            schema_details["output_shape_key_counts"].items()))
    report.add(
        "schema_defs_refs_closed_objects_resolve_and_match_audit",
        schema_details["unresolved_ref_count"] == 0 and
        schema_details["closed_object_required_property_mismatch_count"] == 0 and
        not schema_details["unsupported_schema_keywords"] and
        schema_claims_match,
        observed=schema_details,
        claimed={
            key: claimed_schema.get(key) for key in (
                "schema_definition_count", "schema_ref_count",
                "unresolved_schema_ref_count", "closed_object_count",
                "closed_object_required_property_mismatch_count")})
    full_source_shapes = unique_shapes["producer"] if shapes_equal else None
    schema_shape_subset_matches = (
        isinstance(full_source_shapes, dict) and
        all(full_source_shapes.get(key) == value
            for key, value in schema_details["output_shape_key_counts"].items()))
    report.add(
        "three_source_schema_and_output_shape_constants_equal",
        shapes_equal and schema_shape_subset_matches and
        claimed_schema.get("output_shape_key_counts") == full_source_shapes,
        source_shapes=unique_shapes,
        schema_shapes=schema_details["output_shape_key_counts"],
        audit_shapes=claimed_schema.get("output_shape_key_counts"))

    normalized_launcher = pin_normalized_launcher_ast(trees["launcher"])
    sections["pin_normalized_launcher_ast"] = normalized_launcher
    normalized_claims = {
        "checker_A": checker_a.get("pin_normalized_launcher_ast_sha256")
            if isinstance(checker_a, dict) else None,
        "checker_B": checker_b.get("pin_normalized_launcher_ast_sha256")
            if isinstance(checker_b, dict) else None,
        "checker_C": checker_c.get("pin_normalized_launcher_ast_sha256")
            if isinstance(checker_c, dict) else None,
        "dual_held": dual.get("held_launcher_pin_normalized_ast_sha256"),
        "input_launcher_template": audit_inputs_a.get("launcher_template")
            if isinstance(audit_inputs_a, dict) else None,
    }
    algorithm_literal_present = {
        role: any(
            isinstance(node, ast.Constant) and
            node.value == normalized_launcher["algorithm"]
            for node in ast.walk(trees[role]))
        for role in trees}
    report.add(
        "pin_normalized_launcher_ast_and_three_source_algorithm_match_audit",
        normalized_launcher["predecessor_pin_preserved"] and
        all(value == normalized_launcher["sha256"]
            for value in normalized_claims.values()) and
        all(algorithm_literal_present.values()),
        observed_sha256=normalized_launcher["sha256"],
        audit_claims=normalized_claims,
        algorithm_literal_present=algorithm_literal_present)

    producer_env = environments["producer"]
    consumer_env = environments["consumer"]
    launcher_state = launcher_base7_state(
        trees["launcher"], environments["launcher"])
    producer_pins = {
        "CONTRACT_FILE_PIN": producer_env.get("CONTRACT_FILE_PIN"),
        "CONTRACT_OBJECT_PIN": producer_env.get("CONTRACT_OBJECT_PIN"),
        "CLOSED_SCHEMA_FILE_PIN": producer_env.get("CLOSED_SCHEMA_FILE_PIN"),
    }
    consumer_pins = {
        "CONTRACT_FILE_PIN": consumer_env.get("CONTRACT_FILE_PIN"),
        "CONTRACT_OBJECT_PIN": consumer_env.get("CONTRACT_OBJECT_PIN"),
        "CLOSED_SCHEMA_FILE_PIN": consumer_env.get("CLOSED_SCHEMA_FILE_PIN"),
        "PRODUCER_SOURCE_PIN": consumer_env.get("PRODUCER_SOURCE_PIN"),
    }
    computed_core = {
        "schema": json_file_hashes["schema"],
        "contract_file": json_file_hashes["contract"],
        "contract_object": object_closures["contract"]["computed"],
        "producer": python_stats["producer"]["file_sha256"],
        "consumer": python_stats["consumer"]["file_sha256"],
        "transition_file": json_file_hashes["transition"],
        "transition_object": object_closures["transition"]["computed"],
        "audit_file": json_file_hashes["audit"],
        "audit_object": object_closures["audit"]["computed"],
    }
    producer_pin_matches = (
        producer_pins["CONTRACT_FILE_PIN"] == computed_core["contract_file"] and
        producer_pins["CONTRACT_OBJECT_PIN"] == computed_core["contract_object"] and
        producer_pins["CLOSED_SCHEMA_FILE_PIN"] == computed_core["schema"])
    consumer_pin_matches = (
        consumer_pins["CONTRACT_FILE_PIN"] == computed_core["contract_file"] and
        consumer_pins["CONTRACT_OBJECT_PIN"] == computed_core["contract_object"] and
        consumer_pins["CLOSED_SCHEMA_FILE_PIN"] == computed_core["schema"] and
        consumer_pins["PRODUCER_SOURCE_PIN"] == computed_core["producer"])

    v11_rejection_raw = snapshot(V11_REJECTION)
    v11_rejection, v11_rejection_duplicates = decode_json_with_duplicates(
        v11_rejection_raw, str(V11_REJECTION))
    v11_rejection_object = object_hash_details(v11_rejection)
    sections["v11_rejection_static_input"] = {
        "file_sha256": sha_bytes(v11_rejection_raw),
        "duplicate_key_count": len(v11_rejection_duplicates),
        "object_closure": v11_rejection_object,
    }
    report.add(
        "v11_rejection_json_duplicate_free_and_object_closed",
        not v11_rejection_duplicates and v11_rejection_object["matches"],
        duplicate_keys=v11_rejection_duplicates,
        object_closure=v11_rejection_object)
    expected_base7 = {
        "V11_OFFICIAL_REJECTION": (
            sha_bytes(v11_rejection_raw), v11_rejection_object["computed"]),
        "SCHEMA": (computed_core["schema"], None),
        "CONTRACT": (
            computed_core["contract_file"], computed_core["contract_object"]),
        "PRODUCER": (computed_core["producer"], None),
        "CONSUMER": (computed_core["consumer"], None),
        "TRANSITION": (
            computed_core["transition_file"], computed_core["transition_object"]),
        "AUDIT": (computed_core["audit_file"], computed_core["audit_object"]),
    }
    predecessor_pin = launcher_state["pins"].get("V11_OFFICIAL_REJECTION")
    if isinstance(predecessor_pin, list):
        predecessor_pin = tuple(predecessor_pin)
    pre_audit_pin_failures: list[str] = []
    if producer_env.get("FINAL_V12_CORE_PINS_INSTALLED") is not True:
        pre_audit_pin_failures.append("producer_final_core_flag_not_true")
    if not producer_pin_matches:
        pre_audit_pin_failures.append("producer_core_pins_do_not_match_bytes")
    if consumer_env.get("FINAL_CURRENT_V12_PINS_INSTALLED") is not True:
        pre_audit_pin_failures.append("consumer_final_current_flag_not_true")
    if not consumer_pin_matches:
        pre_audit_pin_failures.append("consumer_current_pins_do_not_match_bytes")
    if launcher_state["flag"] is not False:
        pre_audit_pin_failures.append(
            "launcher_template_flag_must_remain_false_before_audit")
    if predecessor_pin != expected_base7["V11_OFFICIAL_REJECTION"]:
        pre_audit_pin_failures.append("launcher_v11_rejection_pin_mismatch")
    if not helper_passed:
        pre_audit_pin_failures.append("exact40_helper_pin_consensus_failure")
    if not normalized_launcher["predecessor_pin_preserved"]:
        pre_audit_pin_failures.append(
            "pin_normalizer_does_not_preserve_predecessor")
    sections["pre_audit_pin_eligibility"] = {
        "failure_count": len(pre_audit_pin_failures),
        "failures": pre_audit_pin_failures,
        "scope": (
            "producer/consumer final core pins, frozen predecessor pin, "
            "exact40 pin consensus, and pin-normalizer predecessor "
            "preservation; current transition/audit launcher pins are "
            "post-report outputs and intentionally excluded"),
    }
    base7_mismatches = pin_mismatch_rows(launcher_state["pins"], expected_base7)
    sentinel_values: set[Any] = set()
    for role, name in (
            ("producer", "V12_DRAFT_CORE_PIN_SENTINELS"),
            ("consumer", "V12_DRAFT_CURRENT_CORE_PINS")):
        value = environments[role].get(name, ())
        if isinstance(value, tuple):
            sentinel_values.update(value)
    installed_values = set(producer_pins.values()) | set(consumer_pins.values())
    installed_values.update(
        item for pair in launcher_state["pins"].values()
        if isinstance(pair, (tuple, list)) for item in pair if item is not None)
    surviving_sentinels = sorted(
        str(value) for value in installed_values if value in sentinel_values)
    pin_state = {
        "flags": {
            "producer_FINAL_V12_CORE_PINS_INSTALLED": producer_env.get(
                "FINAL_V12_CORE_PINS_INSTALLED"),
            "consumer_FINAL_CURRENT_V12_PINS_INSTALLED": consumer_env.get(
                "FINAL_CURRENT_V12_PINS_INSTALLED"),
            "launcher_FINAL_BASE7_PINS_INSTALLED": launcher_state["flag"],
        },
        "producer_pins": producer_pins,
        "consumer_pins": consumer_pins,
        "launcher_base7": launcher_state,
        "computed_current_core": computed_core,
        "launcher_base7_mismatches": base7_mismatches,
        "surviving_current_pin_sentinels": surviving_sentinels,
    }
    sections["final_pin_state"] = pin_state
    report.add(
        "three_final_pin_flags_true_no_sentinels_and_all_pins_match_bytes",
        all(value is True for value in pin_state["flags"].values()) and
        producer_pin_matches and consumer_pin_matches and
        not launcher_state["draft_references"] and
        not base7_mismatches and not surviving_sentinels,
        flags=pin_state["flags"],
        producer_pins_match=producer_pin_matches,
        consumer_pins_match=consumer_pin_matches,
        launcher_draft_references=launcher_state["draft_references"],
        launcher_base7_mismatches=base7_mismatches,
        surviving_sentinels=surviving_sentinels)

    bundle = audit.get("audited_v12_bundle", {})
    if not isinstance(bundle, dict):
        bundle = {}
    bundle_expected = {
        "build_only_producer": computed_core["producer"],
        "closed_schema": computed_core["schema"],
        "contract": computed_core["contract_file"],
        "independent_verifier_assembler_authority_consumer":
            computed_core["consumer"],
        "v11_to_v12_transition_receipt": computed_core["transition_file"],
    }
    bundle_mismatches = {
        key: {"observed": (
            bundle.get(key, {}).get("file_sha256")
            if isinstance(bundle.get(key), dict) else None),
              "expected": value}
        for key, value in bundle_expected.items()
        if not isinstance(bundle.get(key), dict) or
        bundle[key].get("file_sha256") != value}
    report.add(
        "audit_bundle_file_hashes_match_current_v12_bytes",
        not bundle_mismatches, mismatches=bundle_mismatches)

    current_input_expected = {
        "schema": computed_core["schema"],
        "contract_file": computed_core["contract_file"],
        "contract_object": computed_core["contract_object"],
        "producer": computed_core["producer"],
        "consumer": computed_core["consumer"],
        "transition_file": computed_core["transition_file"],
        "transition_object": computed_core["transition_object"],
        "launcher_template": normalized_launcher["sha256"],
    }
    current_input_mismatches = {
        key: {"observed": audit_inputs_a.get(key), "expected": value}
        for key, value in current_input_expected.items()
        if not isinstance(audit_inputs_a, dict) or audit_inputs_a.get(key) != value}
    report.add(
        "audit_current_core_input_hashes_match_current_v12_bytes",
        not current_input_mismatches,
        mismatches=current_input_mismatches)

    runtime_summary = runtime_surface_summary()
    sections["runtime_surfaces"] = runtime_summary
    report.add(
        "v12_runtime_surfaces_absent",
        runtime_summary["present_surface_count"] == 0,
        present_surfaces=runtime_summary["present_surfaces"])
    prepublication_present = [
        str(path.relative_to(ROOT)) for path in (V12_MANIFEST, V12_OUTER)
        if lstat_exists(path)]
    sections["prepublication_surfaces"] = {
        "present": prepublication_present,
        "manifest_absent": not lstat_exists(V12_MANIFEST),
        "outer_absent": not lstat_exists(V12_OUTER),
    }
    report.add(
        "v12_manifest_and_outer_absent_before_static_freeze",
        not prepublication_present, present=prepublication_present)

    changed_snapshots: list[dict[str, Any]] = []
    for path, expected_identity in snapshots.items():
        try:
            observed_identity = stat_identity(os.stat(path, follow_symlinks=False))
        except FileNotFoundError:
            observed_identity = None
        if observed_identity != expected_identity:
            changed_snapshots.append({
                "path": str(path.relative_to(ROOT)),
                "initial_identity": expected_identity,
                "terminal_identity": observed_identity,
            })
    sections["terminal_snapshot_stability"] = {
        "held_file_count": len(snapshots),
        "changed_file_count": len(changed_snapshots),
        "changed_files": changed_snapshots,
    }
    report.add(
        "all_read_source_and_json_snapshots_stable_through_terminal_check",
        not changed_snapshots, changed_files=changed_snapshots)

    # The external census report is an input to rebuilding transition/audit,
    # so its eligibility deliberately excludes claims that can only become
    # true after those two outputs are rebuilt.  It does require the complete
    # current P/C core-pin chain and the launcher template/predecessor pin.
    json_duplicate_count = (
        sum(len(items) for items in json_duplicates.values()) +
        len(v11_rejection_duplicates))
    undefined_global_count = sum(
        len(items) for items in all_undefined.values())
    object_closure_failure_count = sum((
        int(not object_closures["contract"]["matches"]),
        int(not v11_rejection_object["matches"]),
    ))
    zero_observations = {
        "arity_failure_count": v12_census["arity_failure_count"],
        "starred_positional_total": total_starred,
        "double_star_keyword_total": total_double_star,
        "undefined_global_count": undefined_global_count,
        "JSON_duplicate_key_count": json_duplicate_count,
        "python_literal_dict_duplicate_key_count": total_python_duplicates,
        "object_closure_failure_count": object_closure_failure_count,
        "pin_failure_count": len(pre_audit_pin_failures),
    }
    schema_source_passed = (
        schema_details["unresolved_ref_count"] == 0 and
        schema_details["closed_object_required_property_mismatch_count"] == 0 and
        not schema_details["unsupported_schema_keywords"] and
        shapes_equal and schema_shape_subset_matches)
    source_pin_normalizer_passed = (
        normalized_launcher["predecessor_pin_preserved"] and
        all(algorithm_literal_present.values()))
    checker_export_predicates = (
        ("three_python_ast_compile", len(trees) == 3),
        ("json_duplicate_free", json_duplicate_count == 0),
        ("python_literal_dict_duplicate_free", total_python_duplicates == 0),
        ("undefined_globals_absent", undefined_global_count == 0),
        ("star_and_double_star_absent",
         total_starred == 0 and total_double_star == 0),
        ("contract_and_v11_rejection_objects_close",
         object_closure_failure_count == 0),
        ("v11_common_census_calibrated", calibration_passed),
        ("v12_independent_census_rows_equal",
         v12_census["implementation_A_B_rows_equal"]),
        ("v12_independent_census_kinds_equal",
         v12_census["implementation_A_B_kind_census_equal"]),
        ("v12_independent_census_arity_equal",
         v12_census["implementation_A_B_arity_equal"]),
        ("v12_arity_failure_count_zero",
         v12_census["arity_failure_count"] == 0),
        ("exact40_helper_static_closure", helper_passed),
        ("three_source_audit_keysets_equal", three_way_keysets_equal),
        ("three_source_exact37_input_constants",
         source_input_constants_passed),
        ("three_source_protocol_constants",
         source_protocol_constants_passed),
        ("schema_and_three_source_shapes_close", schema_source_passed),
        ("source_pin_normalizer_closes", source_pin_normalizer_passed),
        ("pre_audit_pin_chain_closes", not pre_audit_pin_failures),
        ("v12_runtime_surfaces_absent",
         runtime_summary["present_surface_count"] == 0),
        ("manifest_and_outer_absent", not prepublication_present),
        ("all_input_snapshots_stable", not changed_snapshots),
    )
    checker_export_blockers = [
        name for name, passed in checker_export_predicates if not passed]
    zero_observations["failed_static_check_count"] = len(
        checker_export_blockers)
    sections["checker_census_report_export"] = {
        "eligible": (
            not checker_export_blockers and
            all(zero_observations[key] == 0
                for key in CHECKER_REPORT_ZERO_KEYS)),
        "blockers": checker_export_blockers,
        "zero_key_observations": zero_observations,
        "python_literal_dict_count": total_literal_dicts,
        "python_AST_and_compile_in_memory_file_count": len(trees),
        "wider_implementation": "independent parent-map implementation A",
        "common_implementation": "independent NodeVisitor implementation B",
        "object_closure_scope": ["current_v12_contract", "v11_rejection"],
        "post_report_outputs_excluded": [
            "current_v12_transition", "current_v12_static_audit",
            "current_transition/audit_launcher_pins"],
    }

    return report.finish(sections)


def closures_function_order(mapping: Mapping[str, str]) -> Iterable[str]:
    """Keep the protocol source role order explicit and deterministic."""
    for role in ("producer", "consumer", "launcher"):
        if role in mapping:
            yield role


def is_sha256_text(value: Any) -> bool:
    return (
        isinstance(value, str) and len(value) == 64 and
        all(character in "0123456789abcdef" for character in value))


def builder_checker_report_key_contract() -> tuple[tuple[str, ...], frozenset[str]]:
    """Parse, but never import/execute, the builder's declared report keys."""
    raw, _ = read_stable_regular_file(V12_JSON_BUILDER)
    tree = ast.parse(raw, filename=V12_JSON_BUILDER.name, mode="exec")
    assignments = module_assignment_nodes(tree)
    zero_nodes = assignments.get("CHECKER_REPORT_ZERO_KEYS", [])
    key_nodes = assignments.get("CHECKER_REPORT_KEYS", [])
    if len(zero_nodes) != 1 or len(key_nodes) != 1:
        raise ValueError("builder checker-report key declarations are not unique")
    zero_value = safe_literal(zero_nodes[0], {})
    if not (isinstance(zero_value, tuple) and
            all(isinstance(item, str) for item in zero_value)):
        raise ValueError("builder zero-key declaration is not a literal tuple")
    key_node = key_nodes[0]
    if not isinstance(key_node, ast.Set):
        raise ValueError("builder report-key declaration is not a literal set")
    keys: list[str] = []
    for item in key_node.elts:
        if (isinstance(item, ast.Starred) and
                isinstance(item.value, ast.Name) and
                item.value.id == "CHECKER_REPORT_ZERO_KEYS"):
            keys.extend(zero_value)
            continue
        value = safe_literal(item, {})
        if not isinstance(value, str):
            raise ValueError("builder report-key set contains a nonliteral key")
        keys.append(value)
    return zero_value, frozenset(keys)


def build_checker_census_report(review_result: Mapping[str, Any]) -> dict[str, Any]:
    """Derive the builder's exact external report from one stable review.

    This does not write anything.  It refuses to synthesize zero failure
    fields unless every pre-audit eligibility predicate observed an actual
    zero/pass.  Implementation A supplies the wider census and independent
    implementation B supplies the common census.
    """
    builder_zero_keys, builder_keys = builder_checker_report_key_contract()
    if (builder_zero_keys != CHECKER_REPORT_ZERO_KEYS or
            builder_keys != CHECKER_REPORT_KEYS):
        raise ValueError("local report contract diverges from current builder")

    sections = review_result.get("sections")
    if not isinstance(sections, dict):
        raise ValueError("static review has no structured sections")
    eligibility = sections.get("checker_census_report_export")
    if not isinstance(eligibility, dict):
        raise ValueError("static review lacks checker-report eligibility")
    if eligibility.get("eligible") is not True:
        blockers = eligibility.get("blockers", [])
        raise ValueError(
            "checker census report is not eligible: " +
            ", ".join(str(item) for item in blockers))

    python_static = sections.get("python_static")
    census = sections.get("v12_callsite_census")
    zero = eligibility.get("zero_key_observations")
    if not isinstance(python_static, dict) or not isinstance(census, dict):
        raise ValueError("missing current source/census observations")
    if not isinstance(zero, dict) or set(zero) != set(CHECKER_REPORT_ZERO_KEYS):
        raise ValueError("zero-key observation closure mismatch")
    if any(type(zero[key]) is not int or zero[key] != 0
           for key in CHECKER_REPORT_ZERO_KEYS):
        raise ValueError("one or more checker failure fields is not exact zero")

    wider = census.get("implementation_A")
    common = census.get("implementation_B")
    if not isinstance(wider, dict) or not isinstance(common, dict):
        raise ValueError("independent wider/common census details missing")
    if not (
            census.get("implementation_A_B_rows_equal") is True and
            census.get("implementation_A_B_kind_census_equal") is True and
            census.get("implementation_A_B_arity_equal") is True):
        raise ValueError("independent wider/common censuses diverge")

    source_hashes: dict[str, str] = {}
    for role in ("producer", "consumer", "launcher"):
        details = python_static.get(role)
        value = details.get("file_sha256") if isinstance(details, dict) else None
        if not is_sha256_text(value):
            raise ValueError(f"invalid held {role} source hash")
        source_hashes[role] = value

    kind_census = common.get("kind_census")
    if not (
            isinstance(kind_census, dict) and
            set(kind_census) == set(CALLSITE_KINDS) and
            all(type(value) is int and value >= 0
                for value in kind_census.values()) and
            sum(kind_census.values()) == common.get("row_count")):
        raise ValueError("common callsite kind census does not close")
    for label, details in (("wider", wider), ("common", common)):
        if type(details.get("row_count")) is not int or details["row_count"] <= 0:
            raise ValueError(f"{label} callsite row count is not positive")
        if not is_sha256_text(details.get("census_sha256")):
            raise ValueError(f"{label} callsite digest is invalid")
        if (details["row_count"] == EXPECTED_V11_CALLSITE_COUNT and
                details["census_sha256"] == EXPECTED_V11_CALLSITE_SHA256):
            raise ValueError(f"refuse stale v11 {label} census")

    literal_dict_count = eligibility.get("python_literal_dict_count")
    compile_count = eligibility.get(
        "python_AST_and_compile_in_memory_file_count")
    if type(literal_dict_count) is not int or literal_dict_count <= 0:
        raise ValueError("python literal dict count is not positive")
    if compile_count != 3:
        raise ValueError("expected exactly three in-memory compiled sources")

    body: dict[str, Any] = {
        "schema": CHECKER_CENSUS_REPORT_SCHEMA,
        "producer_file_sha256": source_hashes["producer"],
        "consumer_file_sha256": source_hashes["consumer"],
        "launcher_file_sha256": source_hashes["launcher"],
        "wider_local_callsite_census_row_count": wider["row_count"],
        "wider_local_callsite_census_sha256": wider["census_sha256"],
        "common_ordered_callsite_row_count": common["row_count"],
        "common_ordered_callsite_census_sha256": common["census_sha256"],
        "common_callsite_kind_census": {
            key: kind_census[key] for key in CALLSITE_KINDS},
        "python_literal_dict_count": literal_dict_count,
        "python_AST_and_compile_in_memory_file_count": compile_count,
        **{key: zero[key] for key in CHECKER_REPORT_ZERO_KEYS},
    }
    body["object_sha256"] = sha_bytes(canonical(body))
    if set(body) != set(CHECKER_REPORT_KEYS):
        raise ValueError("checker report exact key closure mismatch")
    if not object_hash_details(body)["matches"]:
        raise ValueError("checker report object closure failed")
    return body


def resolve_checker_report_target(requested: Path) -> Path:
    """Resolve an existing parent and constrain the target below scripts/."""
    scripts_root = (ROOT / "scripts").resolve(strict=True)
    candidate = requested if requested.is_absolute() else Path.cwd() / requested
    if candidate.name in {"", ".", ".."}:
        raise ValueError("checker report target must name one file")
    parent = candidate.parent.resolve(strict=True)
    if parent != scripts_root and scripts_root not in parent.parents:
        raise ValueError(
            "checker report target must be below workspace scripts/")
    return parent / candidate.name


def _read_open_descriptor(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        try:
            chunk = os.read(descriptor, 1024 * 1024)
        except InterruptedError:
            continue
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _open_held_current_sources(
        expected_hashes: Mapping[str, str],
) -> list[tuple[str, Path, int, tuple[int, ...]]]:
    held: list[tuple[str, Path, int, tuple[int, ...]]] = []
    flags = os.O_RDONLY | os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        for role, path in V12_PYTHON:
            descriptor = os.open(path, flags)
            try:
                before = os.fstat(descriptor)
                if not stat.S_ISREG(before.st_mode):
                    raise ValueError(f"{role}: current source is not regular")
                raw = _read_open_descriptor(descriptor)
                after = os.fstat(descriptor)
                identity = stat_identity(before)
                if identity != stat_identity(after) or len(raw) != before.st_size:
                    raise ValueError(f"{role}: source changed during held read")
                if sha_bytes(raw) != expected_hashes.get(role):
                    raise ValueError(
                        f"{role}: current bytes differ from reviewed held hash")
                path_identity = stat_identity(
                    os.stat(path, follow_symlinks=False))
                if path_identity != identity:
                    raise ValueError(
                        f"{role}: source pathname/FD identity diverges")
            except Exception:
                os.close(descriptor)
                raise
            held.append((role, path, descriptor, identity))
    except Exception:
        for _, _, descriptor, _ in held:
            os.close(descriptor)
        raise
    return held


def _assert_held_sources_unchanged(
        held: Sequence[tuple[str, Path, int, tuple[int, ...]]],
) -> None:
    for role, path, descriptor, expected_identity in held:
        if stat_identity(os.fstat(descriptor)) != expected_identity:
            raise ValueError(f"{role}: held source FD identity drifted")
        observed = stat_identity(os.stat(path, follow_symlinks=False))
        if observed != expected_identity:
            raise ValueError(f"{role}: source pathname identity drifted")


def _write_all(descriptor: int, raw: bytes) -> None:
    offset = 0
    while offset < len(raw):
        try:
            written = os.write(descriptor, raw[offset:])
        except InterruptedError:
            continue
        if written <= 0:
            raise OSError("short checker-report write")
        offset += written


def write_checker_census_report(
        requested: Path, report_object: Mapping[str, Any],
) -> dict[str, Any]:
    """O_EXCL-create, fsync, freeze, and replay one scripts/ report."""
    target = resolve_checker_report_target(requested)
    if set(report_object) != set(CHECKER_REPORT_KEYS):
        raise ValueError("refuse non-exact checker report key set")
    payload = dict(report_object)
    if not object_hash_details(payload)["matches"]:
        raise ValueError("refuse non-closed checker report object")
    raw = canonical(payload) + b"\n"
    if raw != canonical(json.loads(raw.decode("utf-8"))) + b"\n":
        raise ValueError("checker report canonical-byte reproduction failed")

    expected_hashes = {
        role: payload[role + "_file_sha256"]
        for role in ("producer", "consumer", "launcher")}
    held = _open_held_current_sources(expected_hashes)
    parent_flags = os.O_RDONLY | os.O_CLOEXEC
    if hasattr(os, "O_DIRECTORY"):
        parent_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        parent_flags |= os.O_NOFOLLOW
    parent_descriptor: int | None = None
    descriptor: int | None = None
    committed = False

    def cleanup_owned_uncommitted() -> None:
        if descriptor is None:
            return
        try:
            held_stat = os.fstat(descriptor)
            path_stat = os.stat(
                target.name, dir_fd=parent_descriptor,
                follow_symlinks=False)
            if ((held_stat.st_dev, held_stat.st_ino) ==
                    (path_stat.st_dev, path_stat.st_ino)):
                os.unlink(target.name, dir_fd=parent_descriptor)
                os.fsync(parent_descriptor)
        except (FileNotFoundError, OSError):
            pass

    try:
        parent_descriptor = os.open(target.parent, parent_flags)
        _assert_held_sources_unchanged(held)
        create_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC
        if hasattr(os, "O_NOFOLLOW"):
            create_flags |= os.O_NOFOLLOW
        descriptor = os.open(
            target.name, create_flags, 0o600, dir_fd=parent_descriptor)
        os.fchmod(descriptor, 0o600)
        initial = os.fstat(descriptor)
        if (not stat.S_ISREG(initial.st_mode) or initial.st_nlink != 1 or
                stat.S_IMODE(initial.st_mode) != 0o600 or initial.st_size != 0):
            raise ValueError("new checker report lacks exact 0600 singleton state")
        _write_all(descriptor, raw)
        os.fsync(descriptor)
        written = os.fstat(descriptor)
        if (stat.S_IMODE(written.st_mode) != 0o600 or
                written.st_size != len(raw)):
            raise ValueError("checker report 0600 write/fsync replay failed")
        _assert_held_sources_unchanged(held)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        frozen = os.fstat(descriptor)
        if (stat.S_IMODE(frozen.st_mode) != 0o444 or frozen.st_nlink != 1 or
                frozen.st_size != len(raw)):
            raise ValueError("checker report exact 0444 freeze failed")
        _assert_held_sources_unchanged(held)
        path_stat = os.stat(
            target.name, dir_fd=parent_descriptor, follow_symlinks=False)
        if ((path_stat.st_dev, path_stat.st_ino) !=
                (frozen.st_dev, frozen.st_ino)):
            raise ValueError("checker report pathname/held inode diverges")
        os.fsync(parent_descriptor)
        _assert_held_sources_unchanged(held)
        committed = True
        return {
            "status": (
                "WROTE_EXCLUSIVE_FROZEN_CHECKER_CENSUS_REPORT__"
                "RUNTIME_NOT_AUTHORIZED"),
            "path": str(target.relative_to(ROOT)),
            "file_sha256": sha_bytes(raw),
            "object_sha256": payload["object_sha256"],
            "byte_count": len(raw),
            "mode": "0444",
            "nlink": frozen.st_nlink,
            "held_source_file_sha256": expected_hashes,
        }
    except Exception:
        if not committed:
            cleanup_owned_uncommitted()
        raise
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if parent_descriptor is not None:
            os.close(parent_descriptor)
        for _, _, held_descriptor, _ in held:
            os.close(held_descriptor)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pretty", action="store_true",
        help="pretty-print the read-only JSON report")
    parser.add_argument(
        "--write-checker-census-report", metavar="PATH", type=Path,
        help=(
            "opt in to O_CREAT|O_EXCL publication of one canonical, "
            "self-closed checker census report; PATH must resolve below this "
            "workspace's scripts/ directory (default: no writes)"))
    args = parser.parse_args()
    write_succeeded = False
    try:
        result = review()
    except Exception as exc:  # fail closed while retaining a machine report
        result = {
            "schema": "cm2.c79g.v12.independent-read-only-static-review.v1",
            "status": "FAIL_CLOSED_STATIC_REVIEW__RUNTIME_NOT_AUTHORIZED",
            "read_only": True,
            "protocol_python_imported_or_executed": False,
            "protocol_or_runtime_files_written": False,
            "fatal_error": f"{type(exc).__name__}: {exc}",
        }
    if args.write_checker_census_report is not None:
        try:
            checker_report = build_checker_census_report(result)
            write_details = write_checker_census_report(
                args.write_checker_census_report, checker_report)
            result["read_only"] = False
            result["nonprotocol_scripts_file_written"] = True
            result["checker_census_report_write"] = write_details
            write_succeeded = True
        except Exception as exc:
            result["checker_census_report_write"] = {
                "status": (
                    "FAIL_CLOSED_CHECKER_CENSUS_REPORT_NOT_WRITTEN__"
                    "RUNTIME_NOT_AUTHORIZED"),
                "error": f"{type(exc).__name__}: {exc}",
            }
    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")))
    exit_success = (
        write_succeeded if args.write_checker_census_report is not None else
        result.get("status", "").startswith("PASS_"))
    raise SystemExit(0 if exit_success else 1)


if __name__ == "__main__":
    main()
