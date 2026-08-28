#!/usr/bin/env python3
"""Read-only external checker census for C79g v14 static bytes.

The three protocol sources are held and read as inert bytes.  They are never
imported or executed.  Successful stdout is exactly the canonically
object-closed report consumed by ``c79g_v14_json_draft_builder.py``.  Any
failed census, source check, object closure, or pre-audit pin check instead
emits a separately closed fail-closed diagnostic object which the builder
cannot mistake for a checker report.

This program never writes a file, creates a runtime surface, or authorizes a
protocol entry.  Run it with ``python3 -I -B``; it also refuses any arguments.
"""

from __future__ import annotations

import ast
import builtins
import hashlib
import json
import os
import stat
import symtable
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
CHECKPOINT = (
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")

SOURCES = (
    ("producer", OUT / f"{BASE}_v14.py"),
    ("consumer", OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_v14.py")),
    ("launcher", OUT / f"{BASE}_cold_launch_v14.py"),
)
SCHEMA = OUT / f"{BASE}_schema_v14.json"
CONTRACT = OUT / f"{BASE}_contract_v14.json"
TRANSITION = OUT / (
    f"{BASE}_v13_to_v14_static_launch_transition_receipt_v1.json")
AUDIT = OUT / f"{BASE}_static_audit_v14.json"
V12_REJECTION = (
    RUNTIME / f"c79g-v12-rejections-{CHECKPOINT}" / "rejection.json")
V13_SUPERSESSION_RECEIPT = OUT / (
    f"{BASE}_v13_prepublication_pyc_contamination_rejection_"
    "supersession_receipt_v1.json")

REPORT_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer."
    "v14-static-checker-census.v1")
FAILURE_SCHEMA = REPORT_SCHEMA + ".failure.v1"
STALE_V11_CALLSITE_COUNT = 2964
STALE_V11_CALLSITE_SHA256 = (
    "d6d1ffa7a47968ff691fac8e720c9c6770549ae0892e64241204dfe2cd41d6cf")
PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER = (
    "SCHEMA", "CONTRACT", "PRODUCER", "CONSUMER", "TRANSITION", "AUDIT",
)
PIN_NORMALIZED_OBJECT_BASE7_KEYS = frozenset({
    "CONTRACT", "TRANSITION", "AUDIT",
})
PIN_NORMALIZED_AST_ALGORITHM = (
    "PYTHON_AST_DUMP_NO_ATTRIBUTES__FORCE_FINAL_BASE7_FALSE__"
    "CURRENT_V14_SIX_BASE7_FILE_F64_OBJECT_E64_OR_NONE__"
    "PRESERVE_V13_SUPERSESSION_RECEIPT_AND_ALL_HISTORICAL_PINS_V1"
)
CALLSITE_KINDS = (
    "module_function", "module_constructor", "self_instance_method",
    "cls_class_method", "localclass_static_method",
    "localclass_class_method", "localclass_instance_method",
)
ZERO_KEYS = (
    "arity_failure_count", "starred_positional_total",
    "double_star_keyword_total", "undefined_global_count",
    "JSON_duplicate_key_count", "python_literal_dict_duplicate_key_count",
    "object_closure_failure_count", "pin_failure_count",
    "failed_static_check_count",
)
REPORT_KEYS = frozenset({
    "schema", "producer_file_sha256", "consumer_file_sha256",
    "launcher_file_sha256", "wider_local_callsite_census_row_count",
    "wider_local_callsite_census_sha256",
    "common_ordered_callsite_row_count",
    "common_ordered_callsite_census_sha256", "common_callsite_kind_census",
    "python_literal_dict_count",
    "python_AST_and_compile_in_memory_file_count", *ZERO_KEYS,
    "object_sha256",
})
MISSING = object()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str) and len(value) == 64 and
        value != "0" * 64 and
        all(character in "0123456789abcdef" for character in value))


def object_sha256(value: Mapping[str, Any]) -> str:
    return sha256_bytes(canonical({
        key: item for key, item in value.items() if key != "object_sha256"}))


def close_object(value: Mapping[str, Any]) -> dict[str, Any]:
    if "object_sha256" in value:
        raise ValueError("object already has an object_sha256")
    result = dict(value)
    result["object_sha256"] = sha256_bytes(canonical(value))
    return result


def stat_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def stable_read(path: Path) -> bytes:
    """Read one no-follow descriptor and reject pathname or inode drift."""
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        named_before = os.stat(path, follow_symlinks=False)
        if (not stat.S_ISREG(before.st_mode) or
                stat_identity(before) != stat_identity(named_before)):
            raise ValueError(path.name + ": non-regular or unstable input")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        raw = b"".join(chunks)
        after = os.fstat(descriptor)
        named_after = os.stat(path, follow_symlinks=False)
        if (stat_identity(before) != stat_identity(after) or
                stat_identity(after) != stat_identity(named_after) or
                len(raw) != after.st_size):
            raise ValueError(path.name + ": input changed during held read")
        return raw
    finally:
        os.close(descriptor)


def decode_json(raw: bytes, label: str) -> tuple[Any, int]:
    duplicate_count = 0

    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        nonlocal duplicate_count
        result: dict[str, Any] = {}
        for key, item in pairs:
            if key in result:
                duplicate_count += 1
            result[key] = item
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs_hook)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(label + ": invalid JSON") from exc
    return value, duplicate_count


def closed_json_failure(value: Any) -> int:
    if not isinstance(value, dict):
        return 1
    claim = value.get("object_sha256")
    return int(not is_sha256(claim) or object_sha256(value) != claim)


def module_assignment_nodes(tree: ast.Module) -> dict[str, list[ast.AST]]:
    result: dict[str, list[ast.AST]] = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name)):
            result.setdefault(node.targets[0].id, []).append(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            result.setdefault(node.target.id, []).append(node.value)
    return result


def safe_value(node: ast.AST | None, env: Mapping[str, Any]) -> Any:
    if node is None:
        return MISSING
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return env.get(node.id, MISSING)
    if isinstance(node, ast.UnaryOp):
        operand = safe_value(node.operand, env)
        if operand is MISSING:
            return MISSING
        if isinstance(node.op, ast.USub) and type(operand) in (int, float):
            return -operand
        if isinstance(node.op, ast.UAdd) and type(operand) in (int, float):
            return +operand
        if isinstance(node.op, ast.Not) and type(operand) is bool:
            return not operand
        return MISSING
    if isinstance(node, ast.BinOp):
        left = safe_value(node.left, env)
        right = safe_value(node.right, env)
        if left is MISSING or right is MISSING:
            return MISSING
        try:
            if isinstance(node.op, ast.Add) and isinstance(
                    left, (str, bytes, tuple, list)) and type(left) is type(right):
                return left + right
            if isinstance(node.op, ast.Mult):
                if isinstance(left, (str, bytes, tuple, list)) and type(right) is int:
                    return left * right
                if type(left) is int and isinstance(right, (str, bytes, tuple, list)):
                    return right * left
        except (OverflowError, MemoryError):
            return MISSING
        return MISSING
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        values = [safe_value(item, env) for item in node.elts]
        if any(item is MISSING for item in values):
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
            key = safe_value(key_node, env)
            value = safe_value(value_node, env)
            if key is MISSING or value is MISSING:
                return MISSING
            try:
                result[key] = value
            except TypeError:
                return MISSING
        return result
    return MISSING


def literal_environment(tree: ast.Module) -> dict[str, Any]:
    assignments = module_assignment_nodes(tree)
    result: dict[str, Any] = {}
    for _ in range(max(2, len(assignments))):
        changed = False
        for name, nodes in assignments.items():
            if name in result or len(nodes) != 1:
                continue
            value = safe_value(nodes[0], result)
            if value is not MISSING:
                result[name] = value
                changed = True
        if not changed:
            break
    return result


def dict_literal_stats(tree: ast.Module) -> tuple[int, int]:
    literal_count = 0
    duplicate_count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        literal_count += 1
        seen: set[Any] = set()
        for key_node in node.keys:
            if key_node is None:
                continue
            try:
                key = ast.literal_eval(key_node)
                if key in seen:
                    duplicate_count += 1
                else:
                    seen.add(key)
            except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                continue
    return literal_count, duplicate_count


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
    failures: set[str] = set()

    def walk(scope: symtable.SymbolTable) -> None:
        for symbol in scope.get_symbols():
            if (symbol.is_referenced() and symbol.is_global() and
                    symbol.get_name() not in definitions | allowed):
                failures.add(symbol.get_name())
        for child in scope.get_children():
            walk(child)

    walk(table)
    return sorted(failures)


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
    if arguments.kwarg is None and any(
            name not in legal for name in keyword_names):
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


def exact_main_gate(
        tree: ast.Module, runtime_name: str, final_name: str) -> bool:
    mains = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "main"]
    if len(mains) != 1:
        return False

    def exact(test: ast.AST) -> bool:
        if not isinstance(test, ast.BoolOp) or not isinstance(test.op, ast.And):
            return False
        terms = test.values
        return (
            len(terms) == 2 and
            isinstance(terms[0], ast.Name) and terms[0].id == runtime_name and
            isinstance(terms[1], ast.UnaryOp) and
            isinstance(terms[1].op, ast.Not) and
            isinstance(terms[1].operand, ast.Name) and
            terms[1].operand.id == final_name)

    return sum(
        exact(node.test) for node in ast.walk(mains[0])
        if isinstance(node, ast.If)) == 1


def function_assignment(
        tree: ast.Module, function_name: str, assignment_name: str,
) -> ast.AST | None:
    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == function_name]
    if len(functions) != 1:
        return None
    values: list[ast.AST] = []
    for node in ast.walk(functions[0]):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == assignment_name):
            values.append(node.value)
        elif (isinstance(node, ast.AnnAssign) and
              isinstance(node.target, ast.Name) and
              node.target.id == assignment_name):
            values.append(node.value)
    return values[0] if len(values) == 1 else None


def launcher_draft_base7(
        tree: ast.Module, env: Mapping[str, Any],
) -> tuple[dict[str, Any], tuple[str, ...] | None]:
    base7_node = function_assignment(
        tree, "configure_workspace_paths", "BASE7_PINS")
    exact8_node = function_assignment(
        tree, "configure_workspace_paths", "EXACT8")
    pins: dict[str, Any] = {}
    if isinstance(base7_node, ast.Dict):
        for key_node, value_node in zip(base7_node.keys, base7_node.values):
            if not isinstance(key_node, ast.Name):
                continue
            value = safe_value(value_node, env)
            if value is not MISSING:
                pins[key_node.id] = value
    exact8: tuple[str, ...] | None = None
    if (isinstance(exact8_node, ast.Tuple) and
            all(isinstance(item, ast.Name) for item in exact8_node.elts)):
        exact8 = tuple(item.id for item in exact8_node.elts)
    return pins, exact8


def exact_module_assignment(
        tree: ast.Module, name: str,
) -> ast.Assign | ast.AnnAssign:
    rows: list[ast.Assign | ast.AnnAssign] = []
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == name):
            rows.append(node)
        elif (isinstance(node, ast.AnnAssign) and
              isinstance(node.target, ast.Name) and node.target.id == name):
            rows.append(node)
    if len(rows) != 1 or rows[0].value is None:
        raise ValueError("launcher: expected one module assignment for " + name)
    return rows[0]


def exact_repeat(node: ast.AST, unit: str, count: int) -> bool:
    return (
        isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult) and
        isinstance(node.left, ast.Constant) and node.left.value == unit and
        isinstance(node.right, ast.Constant) and node.right.value == count)


def launcher_base7_nodes(
        tree: ast.Module,
) -> tuple[ast.Dict, tuple[str, ...], ast.AST]:
    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "configure_workspace_paths"]
    if len(functions) != 1:
        raise ValueError("launcher: configure_workspace_paths not unique")
    base7_rows = [
        node for node in functions[0].body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "BASE7_PINS"]
    exact8_rows = [
        node for node in functions[0].body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "EXACT8"]
    if (len(base7_rows) != 1 or
            not isinstance(base7_rows[0].value, ast.Dict)):
        raise ValueError("launcher: BASE7_PINS direct dictionary not unique")
    if len(exact8_rows) != 1:
        raise ValueError("launcher: EXACT8 direct assignment not unique")
    mapping = base7_rows[0].value
    names = tuple(
        key.id if isinstance(key, ast.Name) else "" for key in mapping.keys)
    expected = (
        "V13_SUPERSESSION_RECEIPT", *PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER)
    if names != expected or len(mapping.values) != len(expected):
        raise ValueError("launcher: BASE7 is not receipt-first exact7")
    return mapping, names, exact8_rows[0].value


def validate_receipt_first_ast(
        tree: ast.Module, mapping: ast.Dict,
        receipt_expected: tuple[str, str],
) -> None:
    file_node = exact_module_assignment(
        tree, "V13_SUPERSESSION_RECEIPT_FILE_PIN").value
    object_node = exact_module_assignment(
        tree, "V13_SUPERSESSION_RECEIPT_OBJECT_PIN").value
    if (not isinstance(file_node, ast.Constant) or
            not isinstance(object_node, ast.Constant) or
            file_node.value != receipt_expected[0] or
            object_node.value != receipt_expected[1]):
        raise ValueError("launcher: fixed v13 receipt literal pins mismatch")
    first = mapping.values[0]
    if (not isinstance(first, ast.Tuple) or len(first.elts) != 2 or
            not isinstance(first.elts[0], ast.Name) or
            first.elts[0].id != "V13_SUPERSESSION_RECEIPT_FILE_PIN" or
            not isinstance(first.elts[1], ast.Name) or
            first.elts[1].id != "V13_SUPERSESSION_RECEIPT_OBJECT_PIN"):
        raise ValueError("launcher: receipt-first tuple is not the fixed pair")


def pin_normalized_launcher_ast_sha256(
        raw: bytes, receipt_expected: tuple[str, str],
) -> str:
    """Reproduce the protocol's exact cycle-breaking launcher template."""
    try:
        tree = ast.parse(raw.decode("utf-8"), filename="launcher", mode="exec")
        compile(tree, "launcher", "exec", dont_inherit=True)
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise ValueError("launcher: PIN_NORMALIZED AST parse") from exc
    flag = exact_module_assignment(tree, "FINAL_BASE7_PINS_INSTALLED")
    flag.value = ast.Constant(value=False)
    mapping, names, _ = launcher_base7_nodes(tree)
    validate_receipt_first_ast(tree, mapping, receipt_expected)
    receipt_before = ast.dump(
        mapping.values[0], annotate_fields=True, include_attributes=False)
    for index, name in enumerate(names[1:], start=1):
        mapping.values[index] = ast.Tuple(
            elts=[
                ast.Constant(value="f" * 64),
                ast.Constant(value=(
                    "e" * 64
                    if name in PIN_NORMALIZED_OBJECT_BASE7_KEYS else None)),
            ],
            ctx=ast.Load())
    if ast.dump(
            mapping.values[0], annotate_fields=True,
            include_attributes=False) != receipt_before:
        raise ValueError("launcher: normalizer changed the v13 receipt pin")
    return sha256_bytes(ast.dump(
        tree, annotate_fields=True,
        include_attributes=False).encode("utf-8"))


def launcher_lifecycle_state(
        raw: bytes,
        final_expected: Mapping[str, tuple[str | None, str | None]],
        receipt_expected: tuple[str, str],
) -> tuple[str, str]:
    """Accept exactly one of the complete DRAFT or complete FINAL states."""
    tree = ast.parse(raw.decode("utf-8"), filename="launcher", mode="exec")
    env = literal_environment(tree)
    flag_node = exact_module_assignment(tree, "FINAL_BASE7_PINS_INSTALLED")
    if (not isinstance(flag_node.value, ast.Constant) or
            type(flag_node.value.value) is not bool):
        raise ValueError("launcher: final flag is not an exact bool literal")
    flag = flag_node.value.value
    draft_file_node = exact_module_assignment(tree, "_DRAFT_FILE_PIN").value
    draft_object_node = exact_module_assignment(tree, "_DRAFT_OBJECT_PIN").value
    if (not exact_repeat(draft_file_node, "f", 64) or
            not exact_repeat(draft_object_node, "e", 64) or
            env.get("_DRAFT_FILE_PIN") != "f" * 64 or
            env.get("_DRAFT_OBJECT_PIN") != "e" * 64):
        raise ValueError("launcher: exact draft sentinel declarations changed")

    mapping, names, exact8_node = launcher_base7_nodes(tree)
    validate_receipt_first_ast(tree, mapping, receipt_expected)
    if (not isinstance(exact8_node, ast.Tuple) or
            tuple(item.id if isinstance(item, ast.Name) else ""
                  for item in exact8_node.elts) != (
                      "V13_SUPERSESSION_RECEIPT", "SCHEMA", "CONTRACT",
                      "PRODUCER", "CONSUMER", "TRANSITION", "AUDIT", "SELF")):
        raise ValueError("launcher: EXACT8 order is not receipt-first exact8")

    current: dict[str, Any] = {}
    for index, name in enumerate(names[1:], start=1):
        node = mapping.values[index]
        value = safe_value(node, env)
        if value is MISSING:
            raise ValueError("launcher: unevaluable BASE7 row " + name)
        current[name] = value
    expected_draft = {
        name: ("f" * 64,
               "e" * 64 if name in PIN_NORMALIZED_OBJECT_BASE7_KEYS else None)
        for name in PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER}

    if flag is False and current == expected_draft:
        state = "DRAFT"
        for index, name in enumerate(names[1:], start=1):
            node = mapping.values[index]
            object_name = (
                "_DRAFT_OBJECT_PIN"
                if name in PIN_NORMALIZED_OBJECT_BASE7_KEYS else None)
            if (not isinstance(node, ast.Tuple) or len(node.elts) != 2 or
                    not isinstance(node.elts[0], ast.Name) or
                    node.elts[0].id != "_DRAFT_FILE_PIN" or
                    (object_name is None and not (
                        isinstance(node.elts[1], ast.Constant) and
                        node.elts[1].value is None)) or
                    (object_name is not None and not (
                        isinstance(node.elts[1], ast.Name) and
                        node.elts[1].id == object_name))):
                raise ValueError(
                    "launcher: draft BASE7 expression changed for " + name)
    elif flag is True:
        if (set(final_expected) != set(PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER) or
                any(not is_sha256(pair[0]) or
                    (name in PIN_NORMALIZED_OBJECT_BASE7_KEYS and
                     not is_sha256(pair[1])) or
                    (name not in PIN_NORMALIZED_OBJECT_BASE7_KEYS and
                     pair[1] is not None)
                    for name, pair in final_expected.items())):
            raise ValueError("launcher: final bundle is partial or unclosed")
        if current != dict(final_expected):
            raise ValueError("launcher: mixed or stale final BASE7 pins")
        state = "FINAL"
        for index, name in enumerate(names[1:], start=1):
            node = mapping.values[index]
            expected = final_expected[name]
            if (not isinstance(node, ast.Tuple) or len(node.elts) != 2 or
                    any(not isinstance(item, ast.Constant) or
                        item.value != value
                        for item, value in zip(node.elts, expected))):
                raise ValueError(
                    "launcher: final BASE7 literals mismatch for " + name)
    else:
        raise ValueError("launcher: mixed, stale, or partial BASE7 state")

    normalized = pin_normalized_launcher_ast_sha256(raw, receipt_expected)
    if not is_sha256(normalized):
        raise ValueError("launcher: invalid PIN_NORMALIZED AST digest")
    return state, normalized


def audit_bundle_and_template_match(
        audit: Mapping[str, Any],
        final_expected: Mapping[str, tuple[str | None, str | None]],
        normalized: str,
) -> bool:
    bundle = audit.get("audited_v14_bundle")
    dual = audit.get("dual_independent_static_checkers")
    if not isinstance(bundle, dict) or not isinstance(dual, dict):
        return False
    checker_a = dual.get("checker_A")
    checker_b = dual.get("checker_B")
    checker_c = dual.get(
        "checker_C_common_census_and_pin_normalized_ast_reproduction")
    if not all(isinstance(item, dict) for item in (
            checker_a, checker_b, checker_c)):
        return False
    producer = bundle.get("build_only_producer")
    consumer = bundle.get("independent_verifier_assembler_authority_consumer")
    schema = bundle.get("closed_schema")
    contract = bundle.get("contract")
    transition = bundle.get("v13_to_v14_transition_receipt")
    if not all(isinstance(item, dict) for item in (
            producer, consumer, schema, contract, transition)):
        return False
    expected_input = {
        "schema": final_expected["SCHEMA"][0],
        "contract_file": final_expected["CONTRACT"][0],
        "contract_object": final_expected["CONTRACT"][1],
        "producer": final_expected["PRODUCER"][0],
        "consumer": final_expected["CONSUMER"][0],
        "transition_file": final_expected["TRANSITION"][0],
        "transition_object": final_expected["TRANSITION"][1],
        "launcher_template": normalized,
    }
    return bool(
        audit.get("status") == (
            "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V14__"
            "PHYSICAL_COLD_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED") and
        schema.get("file_sha256") == final_expected["SCHEMA"][0] and
        contract.get("file_sha256") == final_expected["CONTRACT"][0] and
        contract.get("object_sha256") == final_expected["CONTRACT"][1] and
        producer.get("file_sha256") == final_expected["PRODUCER"][0] and
        consumer.get("file_sha256") == final_expected["CONSUMER"][0] and
        transition.get("file_sha256") == final_expected["TRANSITION"][0] and
        transition.get("object_sha256") == final_expected["TRANSITION"][1] and
        dual.get("pin_normalized_ast_algorithm") ==
            PIN_NORMALIZED_AST_ALGORITHM and
        dual.get("pin_normalized_current_base7_key_order") ==
            list(PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER) and
        dual.get("held_launcher_pin_normalized_ast_sha256") == normalized and
        checker_a.get("pin_normalized_launcher_ast_sha256") == normalized and
        checker_b.get("pin_normalized_launcher_ast_sha256") == normalized and
        checker_c.get("pin_normalized_launcher_ast_sha256") == normalized and
        all(isinstance(checker.get("input_sha256"), dict) and
            all(checker["input_sha256"].get(key) == value
                for key, value in expected_input.items())
            for checker in (checker_a, checker_b)))


def launcher_lifecycle_self_tests() -> bool:
    """Positive DRAFT/FINAL and negative mixed/stale/partial/tamper tests."""
    receipt = ("a" * 64, "b" * 64)
    final = {
        name: (str(index) * 64,
               "a" * 64
               if name in PIN_NORMALIZED_OBJECT_BASE7_KEYS else None)
        for index, name in enumerate(
            PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER, start=1)}
    draft_rows = {
        name: ("_DRAFT_FILE_PIN, _DRAFT_OBJECT_PIN"
               if name in PIN_NORMALIZED_OBJECT_BASE7_KEYS else
               "_DRAFT_FILE_PIN, None")
        for name in PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER}
    final_rows = {
        name: repr(final[name]) for name in PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER}

    def sample(flag: bool, rows: Mapping[str, str], receipt_file: str) -> bytes:
        mapping = "\n".join(
            "        " + name + ": (" + rows[name] + "),"
            for name in PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER)
        return (f'''FINAL_BASE7_PINS_INSTALLED = {flag!r}\n'''
                '''_DRAFT_FILE_PIN = "f" * 64\n'''
                '''_DRAFT_OBJECT_PIN = "e" * 64\n'''
                f'''V13_SUPERSESSION_RECEIPT_FILE_PIN = {receipt_file!r}\n'''
                f'''V13_SUPERSESSION_RECEIPT_OBJECT_PIN = {receipt[1]!r}\n'''
                '''def configure_workspace_paths(root):\n'''
                '''    BASE7_PINS = {\n'''
                '''        V13_SUPERSESSION_RECEIPT: (V13_SUPERSESSION_RECEIPT_FILE_PIN, V13_SUPERSESSION_RECEIPT_OBJECT_PIN),\n'''
                + mapping + '''\n    }\n'''
                '''    EXACT8 = (V13_SUPERSESSION_RECEIPT, SCHEMA, CONTRACT, PRODUCER, CONSUMER, TRANSITION, AUDIT, SELF)\n''').encode("utf-8")

    draft = sample(False, draft_rows, receipt[0])
    completed = sample(True, final_rows, receipt[0])
    draft_state, draft_normalized = launcher_lifecycle_state(
        draft, final, receipt)
    final_state, final_normalized = launcher_lifecycle_state(
        completed, final, receipt)
    if (draft_state != "DRAFT" or final_state != "FINAL" or
            draft_normalized != final_normalized):
        return False

    negative_cases = [
        sample(True, {**final_rows, "SCHEMA": draft_rows["SCHEMA"]}, receipt[0]),
        sample(True, {**final_rows, "SCHEMA": repr(("9" * 64, None))},
               receipt[0]),
        sample(True, final_rows, "c" * 64),
    ]
    partial = dict(final)
    partial["AUDIT"] = (None, None)
    failures = 0
    for raw in negative_cases:
        try:
            launcher_lifecycle_state(raw, final, receipt)
        except ValueError:
            failures += 1
    try:
        launcher_lifecycle_state(completed, partial, receipt)
    except ValueError:
        failures += 1
    return failures == len(negative_cases) + 1


def add_pin_failure(
        failures: list[str], condition: bool, label: str) -> None:
    if not condition:
        failures.append(label)


def analyze() -> tuple[dict[str, Any] | None, dict[str, Any]]:
    source_raw: dict[str, bytes] = {}
    source_hashes: dict[str, str] = {}
    trees: dict[str, ast.Module] = {}
    environments: dict[str, dict[str, Any]] = {}
    total_literal_dicts = 0
    literal_duplicate_count = 0
    undefined_count = 0
    starred_count = 0
    double_star_count = 0
    compile_count = 0

    for role, path in SOURCES:
        raw = stable_read(path)
        source_raw[role] = raw
        source_hashes[role] = sha256_bytes(raw)
        source = raw.decode("utf-8")
        tree = ast.parse(source, filename=path.name, mode="exec")
        compile(tree, path.name, "exec", dont_inherit=True)
        compile_count += 1
        trees[role] = tree
        environments[role] = literal_environment(tree)
        literal_count, duplicate_count = dict_literal_stats(tree)
        total_literal_dicts += literal_count
        literal_duplicate_count += duplicate_count
        undefined_count += len(undefined_globals(source, path.name))
        starred_count += sum(
            isinstance(argument, ast.Starred)
            for node in ast.walk(tree) if isinstance(node, ast.Call)
            for argument in node.args)
        double_star_count += sum(
            keyword.arg is None
            for node in ast.walk(tree) if isinstance(node, ast.Call)
            for keyword in node.keywords)

    ordered_sources = [
        (path.name, source_raw[role]) for role, path in SOURCES]
    rows_a, kinds_a, arity_a = callsite_census_parent_map(ordered_sources)
    rows_b, kinds_b, arity_b = callsite_census_visitor(ordered_sources)
    digest_a = sha256_bytes(canonical(rows_a))
    digest_b = sha256_bytes(canonical(rows_b))
    kind_census = {kind: kinds_b.get(kind, 0) for kind in CALLSITE_KINDS}

    json_duplicate_count = 0
    object_failures: list[str] = []
    json_values: dict[str, dict[str, Any]] = {}
    json_raw: dict[str, bytes] = {}
    for label, path, required, needs_closure in (
            ("schema", SCHEMA, False, False),
            ("contract", CONTRACT, False, True),
            ("transition", TRANSITION, False, True),
            ("audit", AUDIT, False, True),
            ("v12_rejection", V12_REJECTION, True, True),
            ("v13_supersession_receipt", V13_SUPERSESSION_RECEIPT, True, True)):
        if not path.is_file():
            if required:
                object_failures.append(label + "_missing")
            continue
        raw = stable_read(path)
        value, duplicates = decode_json(raw, label)
        json_duplicate_count += duplicates
        json_raw[label] = raw
        if not isinstance(value, dict):
            object_failures.append(label + "_root_not_object")
            continue
        json_values[label] = value
        if needs_closure and closed_json_failure(value):
            object_failures.append(label + "_object_closure")

    pin_failures: list[str] = []
    producer_env = environments["producer"]
    consumer_env = environments["consumer"]
    launcher_env = environments["launcher"]

    if "v12_rejection" in json_raw and "v12_rejection" in json_values:
        v12_file = sha256_bytes(json_raw["v12_rejection"])
        v12_object = object_sha256(json_values["v12_rejection"])
        for role, env in environments.items():
            add_pin_failure(
                pin_failures,
                env.get("V12_OFFICIAL_REJECTION_FILE_PIN") == v12_file,
                role + "_v12_rejection_file_pin")
            add_pin_failure(
                pin_failures,
                env.get("V12_OFFICIAL_REJECTION_OBJECT_PIN") == v12_object,
                role + "_v12_rejection_object_pin")

    receipt_expected: tuple[str, str] | None = None
    if ("v13_supersession_receipt" in json_raw and
            "v13_supersession_receipt" in json_values):
        receipt_expected = (
            sha256_bytes(json_raw["v13_supersession_receipt"]),
            object_sha256(json_values["v13_supersession_receipt"]),
        )
        for role, env in environments.items():
            add_pin_failure(
                pin_failures,
                env.get("V13_SUPERSESSION_RECEIPT_FILE_PIN") ==
                    receipt_expected[0],
                role + "_v13_receipt_file_pin")
            add_pin_failure(
                pin_failures,
                env.get("V13_SUPERSESSION_RECEIPT_OBJECT_PIN") ==
                    receipt_expected[1],
                role + "_v13_receipt_object_pin")

    schema_hash = sha256_bytes(json_raw["schema"]) if "schema" in json_raw else None
    contract_file_hash = (
        sha256_bytes(json_raw["contract"]) if "contract" in json_raw else None)
    contract_object_hash = (
        object_sha256(json_values["contract"])
        if "contract" in json_values else None)
    transition_file_hash = (
        sha256_bytes(json_raw["transition"])
        if "transition" in json_raw else None)
    transition_object_hash = (
        object_sha256(json_values["transition"])
        if "transition" in json_values else None)
    audit_file_hash = (
        sha256_bytes(json_raw["audit"]) if "audit" in json_raw else None)
    audit_object_hash = (
        object_sha256(json_values["audit"])
        if "audit" in json_values else None)

    add_pin_failure(
        pin_failures,
        producer_env.get("FINAL_V14_CORE_PINS_INSTALLED") is True,
        "producer_final_core_flag_not_true")
    add_pin_failure(
        pin_failures,
        schema_hash is not None and contract_file_hash is not None and
        contract_object_hash is not None and
        producer_env.get("CLOSED_SCHEMA_FILE_PIN") == schema_hash and
        producer_env.get("CONTRACT_FILE_PIN") == contract_file_hash and
        producer_env.get("CONTRACT_OBJECT_PIN") == contract_object_hash,
        "producer_core_pins_do_not_match_current_schema_contract")
    add_pin_failure(
        pin_failures,
        consumer_env.get("FINAL_CURRENT_V14_PINS_INSTALLED") is True,
        "consumer_final_current_flag_not_true")
    add_pin_failure(
        pin_failures,
        schema_hash is not None and contract_file_hash is not None and
        contract_object_hash is not None and
        consumer_env.get("CLOSED_SCHEMA_FILE_PIN") == schema_hash and
        consumer_env.get("CONTRACT_FILE_PIN") == contract_file_hash and
        consumer_env.get("CONTRACT_OBJECT_PIN") == contract_object_hash and
        consumer_env.get("PRODUCER_SOURCE_PIN") == source_hashes["producer"],
        "consumer_current_pins_do_not_match_current_bytes")

    final_base7_expected: dict[
        str, tuple[str | None, str | None]
    ] = {
        "SCHEMA": (schema_hash, None),
        "CONTRACT": (contract_file_hash, contract_object_hash),
        "PRODUCER": (source_hashes["producer"], None),
        "CONSUMER": (source_hashes["consumer"], None),
        "TRANSITION": (transition_file_hash, transition_object_hash),
        "AUDIT": (audit_file_hash, audit_object_hash),
    }
    launcher_state: str | None = None
    launcher_normalized: str | None = None
    if receipt_expected is None:
        pin_failures.append("launcher_v13_receipt_anchor_unavailable")
    else:
        try:
            launcher_state, launcher_normalized = launcher_lifecycle_state(
                source_raw["launcher"], final_base7_expected, receipt_expected)
        except (UnicodeDecodeError, SyntaxError, ValueError) as exc:
            pin_failures.append(
                "launcher_lifecycle_rejected:" + type(exc).__name__ + ":" +
                str(exc))
    if launcher_state == "FINAL":
        add_pin_failure(
            pin_failures,
            "audit" in json_values and launcher_normalized is not None and
            audit_bundle_and_template_match(
                json_values["audit"], final_base7_expected,
                launcher_normalized),
            "launcher_final_pin_normalized_template_or_audit_bundle_mismatch")
    elif launcher_state == "DRAFT" and "audit" in json_values:
        add_pin_failure(
            pin_failures,
            launcher_normalized is not None and
            audit_bundle_and_template_match(
                json_values["audit"], final_base7_expected,
                launcher_normalized),
            "launcher_draft_pin_normalized_template_or_audit_bundle_mismatch")

    static_failures: list[str] = []
    static_predicates = (
        ("exact_three_ast_parse_compile", compile_count == 3),
        ("positive_python_literal_dict_count", total_literal_dicts > 0),
        ("python_literal_dict_duplicates_zero", literal_duplicate_count == 0),
        ("undefined_globals_zero", undefined_count == 0),
        ("starred_positional_zero", starred_count == 0),
        ("double_star_keywords_zero", double_star_count == 0),
        ("dual_callsite_rows_equal", rows_a == rows_b),
        ("dual_callsite_kinds_equal", kinds_a == kinds_b),
        ("dual_callsite_arity_equal", arity_a == arity_b),
        ("callsite_arity_zero", arity_a == 0 and arity_b == 0),
        ("positive_callsite_rows", len(rows_a) > 0 and len(rows_b) > 0),
        ("callsite_digest_consensus", digest_a == digest_b),
        ("refuse_stale_v11_callsite_count",
         len(rows_a) != STALE_V11_CALLSITE_COUNT and
         len(rows_b) != STALE_V11_CALLSITE_COUNT),
        ("refuse_stale_v11_callsite_digest",
         digest_a != STALE_V11_CALLSITE_SHA256 and
         digest_b != STALE_V11_CALLSITE_SHA256),
        ("common_kind_key_and_sum_closure",
         set(kind_census) == set(CALLSITE_KINDS) and
         sum(kind_census.values()) == len(rows_b)),
        ("strict_json_duplicates_zero", json_duplicate_count == 0),
        ("required_object_closures_zero", not object_failures),
        ("pre_audit_pin_failures_zero", not pin_failures),
        ("launcher_lifecycle_positive_and_negative_self_tests",
         launcher_lifecycle_self_tests()),
        ("producer_exact_draft_and_not_final_main_gate", exact_main_gate(
            trees["producer"], "V14_DRAFT_RUNTIME_DISABLED",
            "FINAL_V14_CORE_PINS_INSTALLED")),
        ("consumer_exact_draft_and_not_final_main_gate", exact_main_gate(
            trees["consumer"], "V14_DRAFT_RUNTIME_DISABLED",
            "FINAL_CURRENT_V14_PINS_INSTALLED")),
        ("launcher_exact_draft_and_not_final_main_gate", exact_main_gate(
            trees["launcher"], "V14_DRAFT_RUNTIME_DISABLED",
            "FINAL_BASE7_PINS_INSTALLED")),
        ("three_runtime_disable_flags_true", all(
            env.get("V14_DRAFT_RUNTIME_DISABLED") is True
            for env in environments.values())),
        ("three_source_hashes_nonzero_and_distinct",
         len(set(source_hashes.values())) == 3 and
         all(is_sha256(value) for value in source_hashes.values())),
    )
    static_failures.extend(
        label for label, passed in static_predicates if not passed)

    pycache = OUT / "__pycache__"
    if pycache.is_dir():
        stems = tuple(path.stem for _, path in SOURCES)
        if any(
                any(path.name.startswith(stem + ".") for stem in stems)
                for path in pycache.glob("*.pyc")):
            static_failures.append("v14_protocol_pyc_present")

    zero = {
        "arity_failure_count": max(arity_a, arity_b),
        "starred_positional_total": starred_count,
        "double_star_keyword_total": double_star_count,
        "undefined_global_count": undefined_count,
        "JSON_duplicate_key_count": json_duplicate_count,
        "python_literal_dict_duplicate_key_count": literal_duplicate_count,
        "object_closure_failure_count": len(object_failures),
        "pin_failure_count": len(pin_failures),
        "failed_static_check_count": len(static_failures),
    }
    diagnostics = {
        "source_hashes": source_hashes,
        "zero_key_observations": zero,
        "static_failures": static_failures,
        "object_closure_failures": object_failures,
        "pin_failures": pin_failures,
        "wider_row_count": len(rows_a),
        "wider_sha256": digest_a,
        "common_row_count": len(rows_b),
        "common_sha256": digest_b,
        "common_kind_census": kind_census,
        "python_literal_dict_count": total_literal_dicts,
        "python_AST_and_compile_in_memory_file_count": compile_count,
    }

    if any(type(zero[key]) is not int or zero[key] != 0 for key in ZERO_KEYS):
        return None, diagnostics

    report: dict[str, Any] = {
        "schema": REPORT_SCHEMA,
        "producer_file_sha256": source_hashes["producer"],
        "consumer_file_sha256": source_hashes["consumer"],
        "launcher_file_sha256": source_hashes["launcher"],
        "wider_local_callsite_census_row_count": len(rows_a),
        "wider_local_callsite_census_sha256": digest_a,
        "common_ordered_callsite_row_count": len(rows_b),
        "common_ordered_callsite_census_sha256": digest_b,
        "common_callsite_kind_census": kind_census,
        "python_literal_dict_count": total_literal_dicts,
        "python_AST_and_compile_in_memory_file_count": compile_count,
        **zero,
    }
    report["object_sha256"] = object_sha256(report)
    if set(report) != set(REPORT_KEYS) or object_sha256(report) != report[
            "object_sha256"]:
        raise ValueError("internal checker report key/object closure failure")
    return report, diagnostics


def fail_closed(reason: str, details: Mapping[str, Any] | None = None) -> int:
    body: dict[str, Any] = {
        "schema": FAILURE_SCHEMA,
        "status": (
            "FAIL_CLOSED_V14_STATIC_CHECKER_CENSUS__"
            "NO_CHECKER_REPORT_EMITTED__RUNTIME_NOT_AUTHORIZED"),
        "reason": reason,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_started": False,
        "details": dict(details or {}),
    }
    sys.stdout.buffer.write(canonical(close_object(body)) + b"\n")
    return 1


def main() -> int:
    if len(sys.argv) != 1:
        return fail_closed("arguments_are_forbidden")
    try:
        report, diagnostics = analyze()
        if report is None:
            return fail_closed("one_or_more_static_export_gates_failed", diagnostics)
        sys.stdout.buffer.write(canonical(report) + b"\n")
        return 0
    except Exception as exc:
        return fail_closed(
            "checker_exception_fail_closed",
            {"exception_type": type(exc).__name__, "message": str(exc)})


if __name__ == "__main__":
    raise SystemExit(main())
