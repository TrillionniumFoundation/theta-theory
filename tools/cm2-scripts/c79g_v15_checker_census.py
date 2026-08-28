#!/usr/bin/env python3
"""Read-only external checker census for C79g v15 static bytes.

The three protocol sources are held and read as inert bytes.  They are never
imported or executed.  Successful stdout is exactly the canonically
object-closed report consumed by ``c79g_v15_json_draft_builder.py``.  Any
failed census, source check, object closure, or pre-audit pin check instead
emits a separately closed fail-closed diagnostic object which the builder
cannot mistake for a checker report.

This program never writes a file, creates a runtime surface, or authorizes a
protocol entry.  Run it with ``python3 -I -B``; it also refuses any arguments.
"""

from __future__ import annotations

import ast
import builtins
import copy
import hashlib
import json
import os
import stat
import symtable
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
CHECKPOINT = (
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")

SOURCES = (
    ("producer", OUT / f"{BASE}_v15.py"),
    ("consumer", OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_v15.py")),
    ("launcher", OUT / f"{BASE}_cold_launch_v15.py"),
)
SCHEMA = OUT / f"{BASE}_schema_v15.json"
CONTRACT = OUT / f"{BASE}_contract_v15.json"
TRANSITION = OUT / (
    f"{BASE}_v14_to_v15_static_launch_transition_receipt_v1.json")
AUDIT = OUT / f"{BASE}_static_audit_v15.json"
V14_REJECTION = (
    RUNTIME / f"c79g-v14-rejections-{CHECKPOINT}" / "rejection.json")
V14_SUPERSESSION_RECEIPT = OUT / (
    f"{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json")

V14_EXACT10 = (
    (f"deliverables/{BASE}_v13_prepublication_pyc_contamination_rejection_"
     "supersession_receipt_v1.json",
     "098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f",
     "3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677"),
    (f"deliverables/{BASE}_schema_v14.json",
     "3d07ccda67cb71d0e5c64d37c0d8e1fcf425de4fbfefddf03bf43934ffdaaa4d",
     None),
    (f"deliverables/{BASE}_contract_v14.json",
     "479a0b3f6b4f0ad7e25d22c9f32eec046758a9a7d40509a6bda200e8e41e0ece",
     "11fd8966ed631f3bcc0eb6b1881f0536c814b7a7c093eca8289680e38a7d7b8b"),
    (f"deliverables/{BASE}_v14.py",
     "9fa2f2e20cdf15ed37d7f3ff904197fa7bc46a4eec243cab0ae8fb477e2e1ff0",
     None),
    (f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v14.py",
     "83c58e792b922ad57a7c031b4aca60fe4d5868679e6f7a70b513e3cc4b7dc24c",
     None),
    (f"deliverables/{BASE}_v13_to_v14_static_launch_transition_receipt_v1.json",
     "e8c810f85b511cbc3637321f872f96c996a854454ab7ae1fbb3f5bdf19d7fd95",
     "78912a8f23f7a2e229795aae0e609ca58232dbe36c52ad50bddad727f259413f"),
    (f"deliverables/{BASE}_static_audit_v14.json",
     "dbf5e6bf0f13524ee847d01482f9ad34f715368deb2df40207bd2eb436f293e9",
     "16a8bc6e274a9e4e5a8fe4b2a39b80136cbbb117bfdf2e0ed89ee90fdc71944a"),
    (f"deliverables/{BASE}_cold_launch_v14.py",
     "1236f53865d69d69d27091758a66b21ddc2ea33ed7f422bc8d56adb69a23f5b5",
     None),
    (f"deliverables/{BASE}_cold_launch_manifest_v14.sha256",
     "aae2b3735ca9d5469d4228189ff0127e85aca934c6e56dfa3650a4d4d46a5937",
     None),
    (f"deliverables/{BASE}_cold_launch_outer_receipt_v14.json",
     "fa6d10673d96a36aaf0163c44e014162ffb7811b12b1efa9068d78c8aa5b2040",
     "786f9be9142ae0aafd31a6d86b08f815d5d4f7ca09fd67506f499635fdddc256"),
)
V14_REJECTION_PIN = (
    str(V14_REJECTION.relative_to(ROOT)),
    "1cc1b5836457f219ce26aa8e463ebebe8d48a26d2145806d24f7cbfea6c7e567",
    "0856353a2390c46b4f4bdefe9f13f6eb6e0e94aa352174cdc8d2f672ace4a41d",
)
V14_SUPERSESSION_PIN = (
    str(V14_SUPERSESSION_RECEIPT.relative_to(ROOT)),
    "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01",
    "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e",
)
V14_EXACT12 = V14_EXACT10 + (V14_REJECTION_PIN, V14_SUPERSESSION_PIN)
V14_EXACT12_ROLES = (
    "v13_supersession_receipt",
    "closed_schema",
    "contract",
    "build_only_producer",
    "independent_consumer",
    "v13_to_v14_transition",
    "static_audit",
    "cold_launcher",
    "cold_manifest",
    "cold_outer",
    "v14_official_rejection",
    "v14_registry_shape_drift_supersession_receipt",
)
V14_EXACT10_ROWS = tuple(
    (role, *pins)
    for role, pins in zip(V14_EXACT12_ROLES[:10], V14_EXACT10, strict=True))
V14_EXACT12_ROWS = V14_EXACT10_ROWS + (
    (V14_EXACT12_ROLES[10], *V14_REJECTION_PIN),
    (V14_EXACT12_ROLES[11], *V14_SUPERSESSION_PIN),
)
V14_EXACT12_FD_ENV_ORDER = tuple(
    (role, "CM2_C79G_V15_V14_" + role.upper() + "_FD")
    for role in V14_EXACT12_ROLES[:10]
) + (
    ("v14_official_rejection",
     "CM2_C79G_V15_V14_OFFICIAL_REJECTION_FD"),
    ("v14_registry_shape_drift_supersession_receipt",
     "CM2_C79G_V15_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_"
     "SUPERSESSION_RECEIPT_FD"),
)
SOURCE_REGISTRY_EXECUTION_PROOF_EXACT7 = (
    "producer_exec_fd_is_fresh_sealed_memfd",
    "producer_exec_fd_distinct_from_installed_source_fd",
    "producer_exec_memfd_required_seals_valid",
    "producer_exec_bytes_equal_installed_source_bytes",
    "producer_exec_and_installed_source_terminal_replayed",
    "twelve_v14_inherited_authority_inputs_inherited_as_held_fds",
    "twelve_v14_inherited_authority_held_fds_path_identity_mount_and_hash_revalidated",
)
V15_EXPECTED_LAUNCHER_REGISTRY_HELPER_AST_SHA256 = (
    "f27a5e8df3308e5b022519929e8f0f64257dcbc35b355fa1537b0169d5604a8c")
V15_EXPECTED_EXACT12_TERMINAL_REPLAY_AST_SHA256 = (
    "7f5ea7ac3f3f4fa81e49947fd718220b0660b5a02b1269f4c9a0d0a12482af69")
V15_EXPECTED_NEED_AST_SHA256 = {
    "producer": "99e6a9e40c339be77ac5270f4ec7471e1cecf9144a83600106bdd01a50f7b99e",
    "consumer": "01d9df10bef3fcbb124dd2e265e685173ab38efedee7a0a8a7fba37930c831d1",
    "launcher": "99e6a9e40c339be77ac5270f4ec7471e1cecf9144a83600106bdd01a50f7b99e",
}
V15_EXPECTED_RUNTIME_OWNER_AST_SHA256 = {
    "producer": {
        "module.canonical":
            "84624bc091a80868ff92af73f4a5c79f0ec48db530007a2f6455c625818a975e",
        "module.strict_json":
            "cd18a308d38da9644fe5ea25fa81fca5e86395f70c07c474dc91fb68e75046f0",
        "module.terminal_replay_v14_exact10_and_official_rejection":
            "dbc5419a5afec206f495e374aa1f735ff5d81a4225b10e0cc400b4a444c3f6df",
        "module.ensure_launch_configuration":
            "7dd5704be115a6e39e376c141f35c4b1d4194b03b03ce7bf11348e14be38f97b",
        "HeldSelf.__init__":
            "05b8b426ba611112a333b5be890138e4dd9b7cb44a1a1b35c9780a3ca5cd2683",
        "HeldSelf.terminal_replay":
            "4419a2aedb75672a993f5cb43155d357237e33ace8a8e509a46645419f9d1782",
    },
    "consumer": {
        "module.canonical":
            "84624bc091a80868ff92af73f4a5c79f0ec48db530007a2f6455c625818a975e",
        "module.strict_json":
            "82403d3bb73d516043d6b21d95da0fbad59ff580229585fe39b24022edc1bae6",
        "module.terminal_replay_v14_exact10_and_official_rejection":
            "dbc5419a5afec206f495e374aa1f735ff5d81a4225b10e0cc400b4a444c3f6df",
        "module.main":
            "098ad9319c7cefd50d0a985e3974d1bd90cbc51cd38f4e34190c56c499ca2284",
        "HeldInheritedV14AuthorityExact12.__init__":
            "a3ab1415e01a49985fe2094dbadfecb3bfe031fa324f570e6554a36794c42762",
        "HeldInheritedV14AuthorityExact12.terminal_replay":
            "f621ac8001abf146077158488fc1b591d7079db1b9797a879f2b2b3256fa7b2b",
    },
    "launcher": {
        "module.canonical":
            "84624bc091a80868ff92af73f4a5c79f0ec48db530007a2f6455c625818a975e",
        "module.strict_json":
            "4ac3d06e0a2f4f2c7b46a41cae69e8cff017130719c1d9ce5e0bbda2e17b2657",
        "module.terminal_replay_v14_exact10_and_official_rejection":
            "dbc5419a5afec206f495e374aa1f735ff5d81a4225b10e0cc400b4a444c3f6df",
        "module.main":
            "d9a040e4fe431bc9b05542f9a6163db91e5b47b52feeef8bc6f44e4e3ca6c4f5",
        "HeldBundle._hold_v14_inherited_authority_exact12":
            "c433d3f7c8f964f56171dd035a27093af2d8a175fcc2d97bdccc7bea9e77f1d3",
        "HeldBundle.terminal_replay":
            "7ca1602756dc317897dd9abb04fad298424f0557f7c08a91f0ed2485352d45ae",
        "module.child_environment":
            "898f1cc9e566a6a4447653e693bf6c5a060ec78a43a1e5b80ca7d992bf641bbe",
        "module.child_pass_fds":
            "33d705bbbc8255dd4f4faf3d0767258cc723e60882aab56e7620f6238fa139e8",
    },
}

REPORT_SCHEMA = (
    "cm2.round306c79g.true-global-no-producer-consumer."
    "v15-static-checker-census.v1")
FAILURE_SCHEMA = REPORT_SCHEMA + ".failure.v1"
STALE_CALLSITE_CENSUSES = frozenset({
    (2964, "d6d1ffa7a47968ff691fac8e720c9c6770549ae0892e64241204dfe2cd41d6cf"),
    (3659, "8045428c8276b6a26ab24604a4f888329848a701f4225fe529c74c3b9add3de2"),
})
PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER = (
    "SCHEMA", "CONTRACT", "PRODUCER", "CONSUMER", "TRANSITION", "AUDIT",
)
PIN_NORMALIZED_OBJECT_BASE7_KEYS = frozenset({
    "CONTRACT", "TRANSITION", "AUDIT",
})
PIN_NORMALIZED_AST_ALGORITHM = (
    "PYTHON_AST_DUMP_NO_ATTRIBUTES__FORCE_FINAL_BASE7_FALSE__"
    "CURRENT_V15_SIX_BASE7_FILE_F64_OBJECT_E64_OR_NONE__"
    "PRESERVE_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_"
    "AND_ALL_HISTORICAL_PINS_V1"
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
    "source_lifecycle_state",
    "v14_inherited_authority_exact12_member_count",
    "v14_inherited_authority_exact12_canonical_sha256",
    "v14_supersession_receipt_file_sha256",
    "v14_supersession_receipt_object_sha256",
    "producer_source_registry_census",
    "launcher_runtime_registry_helper_census",
    "runtime_registry_shape_consensus",
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
        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT",
        *PIN_NORMALIZED_CURRENT_BASE7_KEY_ORDER)
    if names != expected or len(mapping.values) != len(expected):
        raise ValueError("launcher: BASE7 is not receipt-first exact7")
    return mapping, names, exact8_rows[0].value


def validate_receipt_first_ast(
        tree: ast.Module, mapping: ast.Dict,
        receipt_expected: tuple[str, str],
) -> None:
    file_node = exact_module_assignment(
        tree,
        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN").value
    object_node = exact_module_assignment(
        tree,
        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN").value
    if (not isinstance(file_node, ast.Constant) or
            not isinstance(object_node, ast.Constant) or
            file_node.value != receipt_expected[0] or
            object_node.value != receipt_expected[1]):
        raise ValueError("launcher: fixed v14 receipt literal pins mismatch")
    first = mapping.values[0]
    if (not isinstance(first, ast.Tuple) or len(first.elts) != 2 or
            not isinstance(first.elts[0], ast.Name) or
            first.elts[0].id !=
                "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN" or
            not isinstance(first.elts[1], ast.Name) or
            first.elts[1].id !=
                "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN"):
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
        raise ValueError("launcher: normalizer changed the v14 receipt pin")
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
                      "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT",
                      "SCHEMA", "CONTRACT",
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
    bundle = audit.get("audited_v15_bundle")
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
    transition = bundle.get("v14_to_v15_transition_receipt")
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
            "PASS_DUAL_STATIC_PIN_NORMALIZED_AST_GO_V15__"
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
                f'''V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN = {receipt_file!r}\n'''
                f'''V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN = {receipt[1]!r}\n'''
                '''def configure_workspace_paths(root):\n'''
                '''    BASE7_PINS = {\n'''
                '''        V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT: (V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN, V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN),\n'''
                + mapping + '''\n    }\n'''
                '''    EXACT8 = (V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT, SCHEMA, CONTRACT, PRODUCER, CONSUMER, TRANSITION, AUDIT, SELF)\n''').encode("utf-8")

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


class FunctionScopeReturns(ast.NodeVisitor):
    """Collect returns without accepting nested-function decoys."""

    def __init__(self, root: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        self.root = root
        self.rows: list[ast.Return] = []

    def visit_Return(self, node: ast.Return) -> None:  # noqa: N802
        self.rows.append(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        if node is self.root:
            self.generic_visit(node)

    def visit_AsyncFunctionDef(  # noqa: N802
            self, node: ast.AsyncFunctionDef) -> None:
        if node is self.root:
            self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> None:  # noqa: N802
        return


def function_scope_returns(
        function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ast.Return]:
    visitor = FunctionScopeReturns(function)
    visitor.visit(function)
    return visitor.rows


def unique_module_function(
        tree: ast.Module, name: str,
) -> ast.FunctionDef | ast.AsyncFunctionDef:
    rows = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == name]
    if len(rows) != 1:
        raise ValueError(name + ": unique module function required")
    return rows[0]


def producer_close_object_census(tree: ast.Module) -> dict[str, Any]:
    """Prove the producer's close_object adds exactly one named hash field."""
    function = unique_module_function(tree, "close_object")
    positional = [*function.args.posonlyargs, *function.args.args]
    parameter = positional[0].arg if (
        len(positional) == 1 and not function.args.vararg and
        not function.args.kwonlyargs and not function.args.kwarg) else None
    nested_scope_count = sum(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                          ast.Lambda, ast.ClassDef)) and node is not function
        for node in ast.walk(function))
    returns = function_scope_returns(function)
    direct_return = function.body[-1] if function.body else None
    return_dict = returns[0].value if len(returns) == 1 else None
    expansion_ok = (
        isinstance(return_dict, ast.Dict) and len(return_dict.keys) == 2 and
        return_dict.keys[0] is None and
        isinstance(return_dict.values[0], ast.Name) and
        return_dict.values[0].id == parameter)
    closure_key_ok = (
        isinstance(return_dict, ast.Dict) and len(return_dict.keys) == 2 and
        isinstance(return_dict.keys[1], ast.Constant) and
        return_dict.keys[1].value == "object_sha256")
    closure_value = (
        return_dict.values[1] if isinstance(return_dict, ast.Dict) and
        len(return_dict.values) == 2 else None)
    digest_ok = (
        isinstance(closure_value, ast.Call) and
        isinstance(closure_value.func, ast.Name) and
        closure_value.func.id == "digest" and len(closure_value.args) == 1 and
        isinstance(closure_value.args[0], ast.Name) and
        closure_value.args[0].id == parameter and not closure_value.keywords)
    guard_count = 0
    for statement in function.body[:-1]:
        if not (isinstance(statement, ast.Expr) and
                isinstance(statement.value, ast.Call) and
                isinstance(statement.value.func, ast.Name) and
                statement.value.func.id == "need" and statement.value.args):
            continue
        condition = statement.value.args[0]
        if (isinstance(condition, ast.Compare) and
                isinstance(condition.left, ast.Constant) and
                condition.left.value == "object_sha256" and
                len(condition.ops) == len(condition.comparators) == 1 and
                isinstance(condition.ops[0], ast.NotIn) and
                isinstance(condition.comparators[0], ast.Name) and
                condition.comparators[0].id == parameter):
            guard_count += 1
    matches = (
        parameter is not None and nested_scope_count == 0 and
        len(function.body) == 2 and
        len(returns) == 1 and direct_return is returns[0] and
        expansion_ok and closure_key_ok and digest_ok and guard_count == 1)
    return {
        "normalized_close_object_ast_sha256": sha256_bytes(ast.dump(
            function, annotate_fields=True,
            include_attributes=False).encode("utf-8")),
        "single_positional_parameter": parameter is not None,
        "nested_scope_count": nested_scope_count,
        "exact_body_statement_count": len(function.body),
        "direct_terminal_return_count": int(
            len(returns) == 1 and direct_return is returns[0]),
        "input_expansion_exact_once": expansion_ok,
        "object_sha256_literal_field_exact_once": closure_key_ok,
        "object_sha256_is_digest_of_unclosed_input": digest_ok,
        "already_closed_rejection_guard_count": guard_count,
        "matches": matches,
    }


def _producer_source_registry_census_core(tree: ast.Module) -> dict[str, Any]:
    """Independently derive explicit67 + proof7 + close1 from held P AST."""
    registry = unique_module_function(tree, "input_registry")
    held_self_rows = [
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "HeldSelf"]
    if len(held_self_rows) != 1:
        raise ValueError("producer: unique HeldSelf required")
    proof_rows = [
        node for node in held_self_rows[0].body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == "execution_proof"]
    if len(proof_rows) != 1:
        raise ValueError("producer: unique HeldSelf.execution_proof required")
    registry_returns = function_scope_returns(registry)
    proof_returns = function_scope_returns(proof_rows[0])
    if len(registry_returns) != 1 or len(proof_returns) != 1:
        raise ValueError("producer: unique function-scope registry/proof return")
    registry_return = registry_returns[0].value
    proof_return = proof_returns[0].value
    if (not isinstance(registry_return, ast.Call) or
            not isinstance(registry_return.func, ast.Name) or
            registry_return.func.id != "close_object" or
            len(registry_return.args) != 1 or registry_return.keywords or
            not isinstance(registry_return.args[0], ast.Dict) or
            not isinstance(proof_return, ast.Dict)):
        raise ValueError("producer: registry close_object/proof literal shape")
    registry_dict = registry_return.args[0]
    explicit_keys = [
        key.value for key in registry_dict.keys
        if isinstance(key, ast.Constant) and isinstance(key.value, str)]
    unsupported_keys = sum(
        key is not None and not (
            isinstance(key, ast.Constant) and isinstance(key.value, str))
        for key in registry_dict.keys)
    expansions = [
        value for key, value in zip(registry_dict.keys, registry_dict.values)
        if key is None]
    expansion_ok = (
        len(expansions) == 1 and isinstance(expansions[0], ast.Call) and
        isinstance(expansions[0].func, ast.Attribute) and
        isinstance(expansions[0].func.value, ast.Name) and
        expansions[0].func.value.id == "self_guard" and
        expansions[0].func.attr == "execution_proof" and
        not expansions[0].args and not expansions[0].keywords)
    proof_keys = [
        key.value for key in proof_return.keys
        if isinstance(key, ast.Constant) and isinstance(key.value, str)]
    unsupported_proof_keys = sum(
        not (isinstance(key, ast.Constant) and isinstance(key.value, str))
        for key in proof_return.keys)
    proof_values_true = all(
        isinstance(value, ast.Constant) and value.value is True
        for value in proof_return.values)
    explicit_unique = len(set(explicit_keys))
    proof_unique = len(set(proof_keys))
    keysets_disjoint = set(explicit_keys).isdisjoint(proof_keys)
    object_sha_absent = "object_sha256" not in set(explicit_keys) | set(
        proof_keys)
    close_census = producer_close_object_census(tree)
    closure_field_count = int(
        close_census["matches"] is True and object_sha_absent)
    computed = len(set(explicit_keys) | set(proof_keys) | {"object_sha256"})
    matches = (
        bool(registry.body) and registry.body[-1] is registry_returns[0] and
        bool(proof_rows[0].body) and proof_rows[0].body[-1] is proof_returns[0] and
        unsupported_keys == 0 and len(explicit_keys) == explicit_unique == 67 and
        len(registry_dict.keys) == len(explicit_keys) + 1 and
        expansion_ok and tuple(proof_keys) ==
            SOURCE_REGISTRY_EXECUTION_PROOF_EXACT7 and
        len(proof_keys) == proof_unique == 7 and unsupported_proof_keys == 0 and
        proof_values_true and keysets_disjoint and object_sha_absent and
        close_census["matches"] is True and closure_field_count == 1 and
        computed == 75)
    return {
        "explicit_key_count": len(explicit_keys),
        "explicit_unique_key_count": explicit_unique,
        "explicit_sorted_key_array_sha256": sha256_bytes(
            canonical(sorted(explicit_keys))),
        "explicit_ordered_key_array_sha256": sha256_bytes(
            canonical(explicit_keys)),
        "unsupported_explicit_key_count": unsupported_keys,
        "execution_proof_key_count": len(proof_keys),
        "execution_proof_unique_key_count": proof_unique,
        "execution_proof_unsupported_key_count": unsupported_proof_keys,
        "execution_proof_keys": proof_keys,
        "execution_proof_values_all_literal_true": proof_values_true,
        "execution_proof_expansion_exact_once": expansion_ok,
        "registry_return_is_direct_terminal":
            bool(registry.body) and registry.body[-1] is registry_returns[0],
        "execution_proof_return_is_direct_terminal":
            bool(proof_rows[0].body) and
            proof_rows[0].body[-1] is proof_returns[0],
        "explicit_and_execution_proof_keysets_disjoint": keysets_disjoint,
        "object_sha256_absent_before_closure": object_sha_absent,
        "close_object_semantics": close_census,
        "object_closure_field_count": closure_field_count,
        "computed_closed_registry_key_count": computed,
        "matches": matches,
    }


def _producer_registry_dicts(
        tree: ast.Module,
) -> tuple[ast.Dict, ast.Dict]:
    registry = unique_module_function(tree, "input_registry")
    held_self = next(
        (node for node in tree.body
         if isinstance(node, ast.ClassDef) and node.name == "HeldSelf"), None)
    if held_self is None:
        raise ValueError("producer mutation: HeldSelf missing")
    proof = next(
        (node for node in held_self.body
         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
         node.name == "execution_proof"), None)
    if proof is None:
        raise ValueError("producer mutation: execution_proof missing")
    registry_returns = function_scope_returns(registry)
    proof_returns = function_scope_returns(proof)
    registry_call = registry_returns[0].value if len(registry_returns) == 1 else None
    registry_dict = (
        registry_call.args[0] if isinstance(registry_call, ast.Call) and
        registry_call.args and isinstance(registry_call.args[0], ast.Dict)
        else None)
    proof_dict = proof_returns[0].value if len(proof_returns) == 1 else None
    if not isinstance(registry_dict, ast.Dict) or not isinstance(
            proof_dict, ast.Dict):
        raise ValueError("producer mutation: registry/proof dict missing")
    return registry_dict, proof_dict


def producer_source_registry_census(tree: ast.Module) -> dict[str, Any]:
    current = _producer_source_registry_census_core(tree)
    registry_dict, _ = _producer_registry_dicts(tree)
    explicit = next(
        key.value for key in registry_dict.keys
        if isinstance(key, ast.Constant) and isinstance(key.value, str))

    overlap_tree = copy.deepcopy(tree)
    _, overlap_proof = _producer_registry_dicts(overlap_tree)
    overlap_proof.keys[0] = ast.Constant(value=explicit)
    overlap_rejected = (
        _producer_source_registry_census_core(overlap_tree)["matches"] is False)

    object_tree = copy.deepcopy(tree)
    _, object_proof = _producer_registry_dicts(object_tree)
    object_proof.keys[0] = ast.Constant(value="object_sha256")
    object_rejected = (
        _producer_source_registry_census_core(object_tree)["matches"] is False)

    nonstring_tree = copy.deepcopy(tree)
    _, nonstring_proof = _producer_registry_dicts(nonstring_tree)
    nonstring_proof.keys[0] = ast.Constant(value=7)
    nonstring_rejected = (
        _producer_source_registry_census_core(nonstring_tree)["matches"] is False)

    close_tree = copy.deepcopy(tree)
    close_function = unique_module_function(close_tree, "close_object")
    close_return = function_scope_returns(close_function)[0].value
    if not isinstance(close_return, ast.Dict) or len(close_return.keys) != 2:
        raise ValueError("producer mutation: close_object return dict missing")
    close_return.keys[1] = ast.Constant(value="row_sha256")
    close_rejected = (
        _producer_source_registry_census_core(close_tree)["matches"] is False)

    current.update({
        "in_memory_explicit_proof_overlap_rejected": overlap_rejected,
        "in_memory_preclosure_object_sha256_rejected": object_rejected,
        "in_memory_nonstring_proof_key_rejected": nonstring_rejected,
        "in_memory_close_object_field_tamper_rejected": close_rejected,
    })
    current["matches"] = bool(
        current["matches"] and overlap_rejected and object_rejected and
        nonstring_rejected and close_rejected)
    return current


def _len_name(node: ast.AST, name: str) -> bool:
    return (
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "len" and len(node.args) == 1 and not node.keywords and
        isinstance(node.args[0], ast.Name) and node.args[0].id == name)


def _len_set_name(node: ast.AST, name: str) -> bool:
    return (
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "len" and len(node.args) == 1 and not node.keywords and
        isinstance(node.args[0], ast.Call) and
        isinstance(node.args[0].func, ast.Name) and
        node.args[0].func.id == "set" and len(node.args[0].args) == 1 and
        not node.args[0].keywords and
        isinstance(node.args[0].args[0], ast.Name) and
        node.args[0].args[0].id == name)


def _len_attribute_name(node: ast.AST, name: str, attribute: str) -> bool:
    return (
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "len" and len(node.args) == 1 and not node.keywords and
        isinstance(node.args[0], ast.Attribute) and
        isinstance(node.args[0].value, ast.Name) and
        node.args[0].value.id == name and node.args[0].attr == attribute)


def _direct_statement(
        function: ast.FunctionDef | ast.AsyncFunctionDef, node: ast.AST,
) -> ast.stmt | None:
    parent = {
        child: item for item in ast.walk(function)
        for child in ast.iter_child_nodes(item)}
    cursor: ast.AST = node
    while cursor in parent:
        owner = parent[cursor]
        if owner is function:
            return cursor if isinstance(cursor, ast.stmt) else None
        cursor = owner
    return None


def _is_direct_need_condition(
        function: ast.FunctionDef | ast.AsyncFunctionDef, node: ast.AST,
) -> bool:
    statement = _direct_statement(function, node)
    if not (
            isinstance(statement, ast.Expr) and
            isinstance(statement.value, ast.Call) and
            isinstance(statement.value.func, ast.Name) and
            statement.value.func.id == "need" and statement.value.args):
        return False
    condition = statement.value.args[0]
    parent = {
        child: item for item in ast.walk(condition)
        for child in ast.iter_child_nodes(item)}
    cursor = node
    while cursor is not condition:
        owner = parent.get(cursor)
        if not isinstance(owner, ast.BoolOp) or not isinstance(owner.op, ast.And):
            return False
        cursor = owner
    return True


def _launcher_runtime_helper_core(
        tree: ast.Module, producer_shape: int) -> dict[str, Any]:
    helper = unique_module_function(
        tree, "producer_source_registry_shape_from_ast")
    helper_nodes = list(ast.walk(helper))
    explicit_guards = [
        node for node in helper_nodes
        if isinstance(node, ast.Compare) and len(node.ops) == 2 and
        all(isinstance(op, ast.Eq) for op in node.ops) and
        _len_name(node.left, "explicit_keys") and
        _len_set_name(node.comparators[0], "explicit_keys") and
        isinstance(node.comparators[1], ast.Constant) and
        type(node.comparators[1].value) is int and
        _is_direct_need_condition(helper, node)]
    expected_literals = [node.comparators[1].value for node in explicit_guards]
    stale_62_count = sum(
        isinstance(node, ast.Constant) and node.value == 62
        for node in helper_nodes)
    proof_7_guards = [
        node for node in helper_nodes
        if isinstance(node, ast.Compare) and len(node.ops) == 1 and
        isinstance(node.ops[0], ast.Eq) and
        _len_attribute_name(node.left, "proof_dict", "keys") and
        len(node.comparators) == 1 and
        isinstance(node.comparators[0], ast.Constant) and
        node.comparators[0].value == 7 and
        _is_direct_need_condition(helper, node)]
    expansion_exact_one_guards = [
        node for node in helper_nodes
        if isinstance(node, ast.Compare) and len(node.ops) == 1 and
        isinstance(node.ops[0], ast.Eq) and
        _len_name(node.left, "expansions") and
        len(node.comparators) == 1 and
        isinstance(node.comparators[0], ast.Constant) and
        node.comparators[0].value == 1 and
        _is_direct_need_condition(helper, node)]
    expansion_guard_literals = {
        node.value for node in helper_nodes
        if isinstance(node, ast.Constant) and
        node.value in {"self_guard", "execution_proof"}}
    shape_assignments = [
        node.value for node in helper.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "shape"]
    expected_shape_formula = ast.parse(
        "len(explicit_keys) + len(proof_dict.keys) + 1", mode="eval").body
    formula_ok = (
        len(shape_assignments) == 1 and
        ast.dump(shape_assignments[0], include_attributes=False) ==
            ast.dump(expected_shape_formula, include_attributes=False))
    returns = function_scope_returns(helper)
    return_shape_ok = (
        len(returns) == 1 and isinstance(returns[0].value, ast.Name) and
        returns[0].value.id == "shape" and bool(helper.body) and
        helper.body[-1] is returns[0])
    nested_scope_count = sum(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                          ast.Lambda, ast.ClassDef)) and node is not helper
        for node in helper_nodes)
    shape_75_guards = [
        node for node in helper_nodes
        if isinstance(node, ast.Compare) and len(node.ops) == 1 and
        isinstance(node.ops[0], ast.Eq) and
        isinstance(node.left, ast.Name) and node.left.id == "shape" and
        len(node.comparators) == 1 and
        isinstance(node.comparators[0], ast.Constant) and
        node.comparators[0].value == 75 and
        _is_direct_need_condition(helper, node)]

    parent: dict[ast.AST, ast.AST] = {
        child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "producer_source_registry_shape_from_ast"]
    live_call_ok = False
    live_result_consumed_ok = False
    live_call_direct_assignment_ok = False
    live_consumption_direct_need_ok = False
    call_owner = None
    if len(calls) == 1:
        call = calls[0]
        expected_argument = ast.parse(
            "held_by_path[PRODUCER].raw", mode="eval").body
        argument_ok = (
            len(call.args) == 1 and not call.keywords and
            ast.dump(call.args[0], include_attributes=False) ==
                ast.dump(expected_argument, include_attributes=False))
        cursor: ast.AST = call
        direct_statement: ast.stmt | None = None
        while cursor in parent:
            owner = parent[cursor]
            if isinstance(owner, (ast.FunctionDef, ast.AsyncFunctionDef)):
                call_owner = owner.name
                direct_statement = cursor if isinstance(cursor, ast.stmt) else None
                live_call_direct_assignment_ok = (
                    isinstance(direct_statement, ast.Assign) and
                    len(direct_statement.targets) == 1 and
                    isinstance(direct_statement.targets[0], ast.Name) and
                    direct_statement.targets[0].id ==
                        "computed_registry_shape" and
                    direct_statement.value is call)
                consumption = [
                    node for node in ast.walk(owner)
                    if isinstance(node, ast.Compare) and len(node.ops) == 2 and
                    all(isinstance(op, ast.Eq) for op in node.ops) and
                    isinstance(node.left, ast.Name) and
                    node.left.id == "computed_registry_shape" and
                    isinstance(node.comparators[0], ast.Subscript) and
                    isinstance(node.comparators[0].value, ast.Name) and
                    node.comparators[0].value.id == "expected_shapes" and
                    isinstance(node.comparators[0].slice, ast.Constant) and
                    node.comparators[0].slice.value ==
                        "producerSourceRegistry" and
                    isinstance(node.comparators[1], ast.Constant) and
                    node.comparators[1].value == 75]
                live_consumption_direct_need_ok = (
                    len(consumption) == 1 and
                    _is_direct_need_condition(owner, consumption[0]))
                live_result_consumed_ok = live_consumption_direct_need_ok
                break
            cursor = owner
        live_call_ok = (
            argument_ok and live_call_direct_assignment_ok and
            call_owner == "validate_final_static_audit" and
            live_result_consumed_ok)
    normalized = sha256_bytes(ast.dump(
        helper, annotate_fields=True, include_attributes=False).encode("utf-8"))
    parameters = [*helper.args.posonlyargs, *helper.args.args]
    exact_raw_parameter = (
        len(parameters) == 1 and parameters[0].arg == "raw" and
        not helper.args.vararg and not helper.args.kwonlyargs and
        not helper.args.kwarg and not helper.args.defaults)
    matches = (
        expected_literals == [67] and stale_62_count == 0 and
        len(proof_7_guards) == 1 and len(expansion_exact_one_guards) == 1 and
        expansion_guard_literals == {"self_guard", "execution_proof"} and
        normalized == V15_EXPECTED_LAUNCHER_REGISTRY_HELPER_AST_SHA256 and
        exact_raw_parameter and nested_scope_count == 0 and formula_ok and
        return_shape_ok and len(shape_75_guards) == 1 and live_call_ok and
        producer_shape == 75)
    return {
        "normalized_helper_ast_sha256": normalized,
        "expected_normalized_helper_ast_sha256":
            V15_EXPECTED_LAUNCHER_REGISTRY_HELPER_AST_SHA256,
        "exact_single_raw_parameter": exact_raw_parameter,
        "normalized_helper_semantics_match_reviewed_template":
            normalized == V15_EXPECTED_LAUNCHER_REGISTRY_HELPER_AST_SHA256,
        "explicit_key_guard_literals": expected_literals,
        "stale_literal_62_count": stale_62_count,
        "exact_execution_proof_7_guard_count": len(proof_7_guards),
        "exact_execution_proof_expansion_guard_count":
            len(expansion_exact_one_guards),
        "nested_helper_scope_count": nested_scope_count,
        "shape_formula_is_len_explicit_plus_len_proof_plus_one": formula_ok,
        "return_is_computed_shape": return_shape_ok,
        "exact_shape_75_guard_count": len(shape_75_guards),
        "live_callsite_count": len(calls),
        "live_callsite_owner": call_owner,
        "live_callsite_is_direct_assignment": live_call_direct_assignment_ok,
        "live_callsite_uses_held_producer_raw": live_call_ok,
        "live_computed_shape_consumed_by_expected_shapes_then_75_gate":
            live_result_consumed_ok,
        "live_consumption_is_direct_need_gate":
            live_consumption_direct_need_ok,
        "held_producer_independent_computed_shape": producer_shape,
        "matches": matches,
    }


def launcher_runtime_registry_helper_census(
        tree: ast.Module, producer_shape: int) -> dict[str, Any]:
    current = _launcher_runtime_helper_core(tree, producer_shape)
    tampered = copy.deepcopy(tree)
    helper = unique_module_function(
        tampered, "producer_source_registry_shape_from_ast")
    changed = 0
    for node in ast.walk(helper):
        if (isinstance(node, ast.Compare) and len(node.comparators) == 2 and
                isinstance(node.comparators[-1], ast.Constant) and
                node.comparators[-1].value == 67):
            node.comparators[-1].value = 62
            changed += 1
    stale_rejected = (
        changed == 1 and
        _launcher_runtime_helper_core(tampered, producer_shape)["matches"] is False)

    dead_callsite_tree = copy.deepcopy(tree)
    audit_function = unique_module_function(
        dead_callsite_tree, "validate_final_static_audit")
    moved = 0
    for index, statement in enumerate(audit_function.body):
        if (isinstance(statement, ast.Assign) and len(statement.targets) == 1 and
                isinstance(statement.targets[0], ast.Name) and
                statement.targets[0].id == "computed_registry_shape"):
            audit_function.body[index] = ast.If(
                test=ast.Constant(value=False), body=[statement], orelse=[])
            moved += 1
    dead_callsite_rejected = (
        moved == 1 and
        _launcher_runtime_helper_core(
            dead_callsite_tree, producer_shape)["matches"] is False)
    current["in_memory_stale_62_mutation_count"] = changed
    current["in_memory_stale_62_rejected"] = stale_rejected
    current["in_memory_dead_callsite_mutation_count"] = moved
    current["in_memory_dead_callsite_rejected"] = dead_callsite_rejected
    current["matches"] = bool(
        current["matches"] and stale_rejected and dead_callsite_rejected)
    return current


def shape_declarations(tree: ast.Module) -> list[int]:
    values: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        mapping: dict[str, Any] = {}
        valid = True
        for key, value in zip(node.keys, node.values):
            if not (isinstance(key, ast.Constant) and
                    isinstance(key.value, str)):
                valid = False
                break
            if isinstance(value, ast.Constant):
                mapping[key.value] = value.value
        if (valid and mapping.get("producerSourceRegistry") is not None and
                set(("selfIdentity", "independentConsumerProof",
                     "staticFreezeProof", "coldLaunchProof", "laterRejection",
                     "producerSourceRegistry", "liveRequest", "liveACK",
                     "liveACKCensus")).issubset(mapping)):
            value = mapping["producerSourceRegistry"]
            if type(value) is int:
                values.append(value)
    return values


class HeldExact12StaticInputSet:
    """Keep all twelve predecessor descriptors held through terminal replay."""

    def __init__(self) -> None:
        self.descriptors: dict[str, int] = {}
        self.before: dict[str, os.stat_result] = {}
        self.raw: dict[str, bytes] = {}
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            for relative, _, _ in V14_EXACT12:
                path = ROOT / relative
                descriptor = os.open(path, flags)
                self.descriptors[relative] = descriptor
                before = os.fstat(descriptor)
                named_before = os.stat(path, follow_symlinks=False)
                if (not stat.S_ISREG(before.st_mode) or
                        stat_identity(before) != stat_identity(named_before)):
                    raise ValueError(relative + ": held initial identity")
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
                    raise ValueError(relative + ": held initial read drift")
                self.before[relative] = before
                self.raw[relative] = raw
        except BaseException:
            self.close()
            raise

    def terminal_replay(self) -> bool:
        for relative, _, _ in V14_EXACT12:
            descriptor = self.descriptors[relative]
            path = ROOT / relative
            before = self.before[relative]
            pre = os.fstat(descriptor)
            named_pre = os.stat(path, follow_symlinks=False)
            if (stat_identity(before) != stat_identity(pre) or
                    stat_identity(pre) != stat_identity(named_pre)):
                return False
            os.lseek(descriptor, 0, os.SEEK_SET)
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            replay = b"".join(chunks)
            post = os.fstat(descriptor)
            named_post = os.stat(path, follow_symlinks=False)
            if (replay != self.raw[relative] or
                    stat_identity(pre) != stat_identity(post) or
                    stat_identity(post) != stat_identity(named_post)):
                return False
        return True

    def close(self) -> None:
        for descriptor in reversed(tuple(self.descriptors.values())):
            try:
                os.close(descriptor)
            except OSError:
                pass
        self.descriptors.clear()


def _held_v14_exact12_review_impl(
        held: HeldExact12StaticInputSet,
) -> tuple[dict[str, Any], list[str]]:
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    identities: set[tuple[int, int]] = set()
    devices: set[int] = set()
    for ordinal, (relative, file_pin, object_pin) in enumerate(
            V14_EXACT12, start=1):
        path = ROOT / relative
        try:
            raw = held.raw[relative]
            metadata = held.before[relative]
            identities.add((metadata.st_dev, metadata.st_ino))
            devices.add(metadata.st_dev)
            value: dict[str, Any] | None = None
            object_ok = object_pin is None
            duplicate_count = 0
            if object_pin is not None:
                parsed, duplicate_count = decode_json(raw, relative)
                value = parsed if isinstance(parsed, dict) else None
                object_ok = (
                    value is not None and duplicate_count == 0 and
                    object_sha256(value) == value.get("object_sha256") ==
                        object_pin)
            matches = (
                sha256_bytes(raw) == file_pin and object_ok and
                stat.S_ISREG(metadata.st_mode) and
                stat.S_IMODE(metadata.st_mode) == 0o444 and
                metadata.st_nlink == 1)
            if not matches:
                failures.append("v14_exact12_member_" + str(ordinal))
            rows.append({
                "ordinal": ordinal, "path": relative,
                "file_sha256": sha256_bytes(raw),
                "object_sha256": object_pin,
                "mode": f"{stat.S_IMODE(metadata.st_mode):04o}",
                "nlink": metadata.st_nlink, "matches": matches,
            })
        except Exception as exc:
            failures.append("v14_exact12_member_" + str(ordinal))
            rows.append({
                "ordinal": ordinal, "path": relative, "matches": False,
                "error": type(exc).__name__ + ":" + str(exc),
            })
    if len(identities) != 12:
        failures.append("v14_exact12_pairwise_unique_file_identities")
    if len(devices) != 1:
        failures.append("v14_exact12_one_st_dev")
    try:
        expected_manifest = b"".join(
            (file_pin + "  " + relative + "\n").encode("ascii")
            for relative, file_pin, _ in V14_EXACT10[:8])
        manifest_raw = held.raw[V14_EXACT10[8][0]]
        if manifest_raw != expected_manifest:
            failures.append("v14_manifest_exact_ordered8_bytes")
        outer_raw = held.raw[V14_EXACT10[9][0]]
        outer, outer_duplicates = decode_json(outer_raw, "v14 outer")
        outer_entries = [
            {"path": relative, "file_sha256": file_pin}
            for relative, file_pin, _ in V14_EXACT10[:8]]
        if not (
                outer_duplicates == 0 and isinstance(outer, dict) and
                outer.get("status") ==
                    "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED" and
                outer.get("exact8_ordered_entries") == outer_entries and
                outer.get("cold_launch_manifest", {}).get("file_sha256") ==
                    V14_EXACT10[8][1] and
                outer.get("formal_global_closure_credit") == 0 and
                outer.get("D02_unlock") is False):
            failures.append("v14_outer_exact8_zero_credit_closure")
        rejection_raw = held.raw[V14_REJECTION_PIN[0]]
        rejection, rejection_duplicates = decode_json(
            rejection_raw, "v14 rejection")
        if not (
                rejection_duplicates == 0 and isinstance(rejection, dict) and
                rejection.get("status") ==
                    "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT" and
                rejection.get("rejection_reason") ==
                    "ORPHANED_OR_INCOMPLETE_C79G_V14_SURFACE" and
                rejection.get("formal_global_closure_credit") == 0 and
                rejection.get("D02_unlock") is False and
                rejection.get("D02_started") is False):
            failures.append("v14_official_rejection_zero_credit_closure")
        receipt_raw = held.raw[V14_SUPERSESSION_PIN[0]]
        receipt, receipt_duplicates = decode_json(
            receipt_raw, "v14 supersession receipt")
        successor = receipt.get("v15_successor_contract", {}) \
            if isinstance(receipt, dict) else {}
        incident = receipt.get("runtime_registry_shape_drift_incident", {}) \
            if isinstance(receipt, dict) else {}
        if not (
                receipt_duplicates == 0 and isinstance(receipt, dict) and
                receipt.get("status") ==
                    "FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__ZERO_CREDIT__V15_SUCCESSOR_ONLY" and
                successor.get(
                    "v15_inherited_published_incident_authority_exact12_count") == 12 and
                successor.get(
                    "v15_current_exact8_first_member_must_be_this_receipt") is True and
                successor.get(
                    "v15_independent_reviewer_must_execute_the_actual_launcher_helper_against_actual_producer_bytes") is True and
                successor.get(
                    "v15_independent_reviewer_must_reject_in_memory_explicit62_tamper") is True and
                incident.get("producer_registry_shape", {}).get(
                    "producer_explicit_registry_key_count") == 67 and
                incident.get("producer_registry_shape", {}).get(
                    "producer_execution_proof_key_count") == 7 and
                incident.get("producer_registry_shape", {}).get(
                    "actual_total_registry_shape") == 75 and
                incident.get("cold_launcher_stale_helper_shape", {}).get(
                    "launcher_stale_expected_explicit_registry_key_count") == 62):
            failures.append("v14_supersession_receipt_exact12_incident_closure")
    except Exception as exc:
        failures.append(
            "v14_exact12_semantic_replay:" + type(exc).__name__ + ":" +
            str(exc))
    terminal_replay_matches = held.terminal_replay()
    if not terminal_replay_matches:
        failures.append("v14_exact12_simultaneous_held_terminal_replay")
    records = [
        {"path": path, "file_sha256": file_pin,
         "object_sha256": object_pin}
        for path, file_pin, object_pin in V14_EXACT12]
    return ({
        "ordered_member_count": len(rows),
        "ordered_members": rows,
        "ordered_exact12_canonical_sha256": sha256_bytes(canonical(records)),
        "pairwise_unique_file_identity_count": len(identities),
        "st_dev_count": len(devices),
        "simultaneously_held_descriptor_count": len(held.descriptors),
        "simultaneous_held_terminal_replay_unchanged":
            terminal_replay_matches,
        "all_regular_0444_nlink1_and_hash_object_closed": not failures,
    }, failures)


def held_v14_exact12_review() -> tuple[dict[str, Any], list[str]]:
    held = HeldExact12StaticInputSet()
    try:
        return _held_v14_exact12_review_impl(held)
    finally:
        held.close()


def source_exact12_pin_review(
        environments: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], list[str]]:
    rows: dict[str, Any] = {}
    failures: list[str] = []
    expected_triples = tuple(V14_EXACT12)
    for role, env in environments.items():
        witness = env.get("V14_PUBLISHED_EXACT10_WITNESS")
        exact12 = env.get("V14_INHERITED_AUTHORITY_EXACT12")
        witness_rows = tuple(witness) if (
            isinstance(witness, tuple) and all(
            isinstance(row, tuple) and len(row) == 4 for row in witness)) else ()
        exact12_rows = tuple(exact12) if (
            isinstance(exact12, tuple) and all(
            isinstance(row, tuple) and len(row) == 4 for row in exact12)) else ()
        exact12_triples = tuple(row[1:] for row in exact12_rows)
        sentinels = env.get(
            "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_DRAFT_SENTINELS")
        matches = (
            witness_rows == V14_EXACT10_ROWS and
            exact12_rows == V14_EXACT12_ROWS and
            exact12_triples == expected_triples and
            env.get("V14_OFFICIAL_REJECTION_RELATIVE_PATH") ==
                V14_REJECTION_PIN[0] and
            env.get("V14_OFFICIAL_REJECTION_FILE_PIN") == V14_REJECTION_PIN[1] and
            env.get("V14_OFFICIAL_REJECTION_OBJECT_PIN") == V14_REJECTION_PIN[2] and
            env.get(
                "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_RELATIVE_PATH") ==
                V14_SUPERSESSION_PIN[0] and
            env.get(
                "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_FILE_PIN") ==
                V14_SUPERSESSION_PIN[1] and
            env.get(
                "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT_OBJECT_PIN") ==
                V14_SUPERSESSION_PIN[2] and
            isinstance(sentinels, tuple) and
            V14_SUPERSESSION_PIN[1] not in sentinels and
            V14_SUPERSESSION_PIN[2] not in sentinels)
        rows[role] = {
            "published_exact10_count": len(witness_rows),
            "published_exact10_role_order_matches":
                witness_rows == V14_EXACT10_ROWS,
            "inherited_exact12_count": len(exact12_rows),
            "inherited_exact12_role_order_matches":
                exact12_rows == V14_EXACT12_ROWS,
            "receipt_pins_are_final_not_sentinel": (
                isinstance(sentinels, tuple) and
                V14_SUPERSESSION_PIN[1] not in sentinels and
                V14_SUPERSESSION_PIN[2] not in sentinels),
            "matches": matches,
        }
        if not matches:
            failures.append(role + "_v14_exact12_source_pin_graph")
    return rows, failures


def _unique_assignment_value(tree: ast.Module, name: str) -> ast.AST:
    rows = module_assignment_nodes(tree).get(name, [])
    if len(rows) != 1:
        raise ValueError(name + ": unique module assignment required")
    return rows[0]


def _fd_env_order_value(
        node: ast.AST, environment: Mapping[str, Any],
) -> tuple[tuple[str, str], ...] | None:
    """Evaluate only the closed tuple algebra permitted for exact12 FD order."""
    if isinstance(node, ast.Name):
        if node.id == "V14_EXACT10_FD_ENV_ORDER":
            return V14_EXACT12_FD_ENV_ORDER[:10]
        value = environment.get(node.id, MISSING)
        if isinstance(value, tuple) and all(
                isinstance(row, tuple) and len(row) == 2 and
                all(isinstance(item, str) for item in row)
                for row in value):
            return value
        return None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _fd_env_order_value(node.left, environment)
        right = _fd_env_order_value(node.right, environment)
        return None if left is None or right is None else left + right
    if isinstance(node, (ast.Tuple, ast.List)):
        rows: list[tuple[str, str]] = []
        for element in node.elts:
            if isinstance(element, ast.Starred):
                expanded = _fd_env_order_value(element.value, environment)
                if expanded is None:
                    return None
                rows.extend(expanded)
                continue
            if not isinstance(element, (ast.Tuple, ast.List)) or len(
                    element.elts) != 2:
                return None
            role = safe_value(element.elts[0], environment)
            env_name = safe_value(element.elts[1], environment)
            if not isinstance(role, str) or not isinstance(env_name, str):
                return None
            rows.append((role, env_name))
        return tuple(rows)
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "tuple" and len(node.args) == 1 and
            not node.keywords):
        return _fd_env_order_value(node.args[0], environment)
    return None


def _function_owner_names(tree: ast.Module, target: str) -> list[str]:
    parent = {
        child: node for node in ast.walk(tree)
        for child in ast.iter_child_nodes(node)}
    owners: list[str] = []
    for call in ast.walk(tree):
        if not (isinstance(call, ast.Call) and
                isinstance(call.func, ast.Name) and call.func.id == target):
            continue
        cursor: ast.AST = call
        function_name: str | None = None
        class_name: str | None = None
        forbidden_control = False
        while cursor in parent:
            cursor = parent[cursor]
            if isinstance(cursor, (ast.If, ast.IfExp, ast.For, ast.AsyncFor,
                                   ast.While, ast.Lambda,
                                   ast.ListComp, ast.SetComp, ast.DictComp,
                                   ast.GeneratorExp)):
                forbidden_control = True
            if function_name is None and isinstance(
                    cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_name = cursor.name
            elif isinstance(cursor, ast.ClassDef):
                class_name = cursor.name
                break
        if function_name is not None and not forbidden_control:
            owners.append(
                function_name if class_name is None else
                class_name + "." + function_name)
    return sorted(owners)


def _constructor_owner_names(tree: ast.Module, target: str) -> list[str]:
    parent = {
        child: node for node in ast.walk(tree)
        for child in ast.iter_child_nodes(node)}
    owners: list[str] = []
    for call in ast.walk(tree):
        if not (isinstance(call, ast.Call) and
                isinstance(call.func, ast.Name) and call.func.id == target):
            continue
        cursor: ast.AST = call
        function_name: str | None = None
        class_name: str | None = None
        forbidden_control = False
        while cursor in parent:
            cursor = parent[cursor]
            if isinstance(cursor, (ast.If, ast.IfExp, ast.For, ast.AsyncFor,
                                   ast.While, ast.Lambda,
                                   ast.ListComp, ast.SetComp, ast.DictComp,
                                   ast.GeneratorExp)):
                forbidden_control = True
            if function_name is None and isinstance(
                    cursor, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_name = cursor.name
            elif isinstance(cursor, ast.ClassDef):
                class_name = cursor.name
                break
        if function_name is not None and not forbidden_control:
            owners.append(
                function_name if class_name is None else
                class_name + "." + function_name)
    return sorted(owners)


def _method_calls(function: ast.AST, owner: str, method: str) -> list[ast.Call]:
    return [
        node for node in ast.walk(function)
        if isinstance(node, ast.Call) and
        isinstance(node.func, ast.Attribute) and
        isinstance(node.func.value, ast.Name) and
        node.func.value.id == owner and node.func.attr == method]


def _compare_has_len_gate(
        compare: ast.Compare, name: str, set_wrapped: bool, expected: int,
) -> bool:
    operands = [compare.left, *compare.comparators]
    target = _len_set_name if set_wrapped else _len_name
    return (
        bool(compare.ops) and all(isinstance(op, ast.Eq) for op in compare.ops) and
        any(target(node, name) for node in operands) and
        any(isinstance(node, ast.Constant) and
            type(node.value) is int and node.value == expected
            for node in operands))


def _name_write_count(function: ast.AST, name: str) -> int:
    return sum(
        isinstance(node, ast.Name) and node.id == name and
        isinstance(node.ctx, (ast.Store, ast.Del))
        for node in ast.walk(function))


def _owned_function(tree: ast.Module, owner: str) -> ast.AST:
    owner_name, function_name = owner.split(".", 1)
    body = tree.body
    if owner_name != "module":
        classes = [
            node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == owner_name]
        if len(classes) != 1:
            raise ValueError(owner + ": unique owner class required")
        body = classes[0].body
    functions = [
        node for node in body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == function_name]
    if len(functions) != 1:
        raise ValueError(owner + ": unique owned function required")
    return functions[0]


def _normalized_owned_function_sha256(tree: ast.Module, owner: str) -> str:
    return sha256_bytes(ast.dump(
        _owned_function(tree, owner), annotate_fields=True,
        include_attributes=False).encode("utf-8"))


class ModuleBindingVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.counts: Counter[str] = Counter()

    def visit_Name(self, node: ast.Name) -> None:  # noqa: N802
        if isinstance(node.ctx, (ast.Store, ast.Del)):
            self.counts[node.id] += 1

    def visit_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802
        if isinstance(node.ctx, (ast.Store, ast.Del)):
            self.counts["<dynamic-module-store>"] += 1
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:  # noqa: N802
        if isinstance(node.ctx, (ast.Store, ast.Del)):
            self.counts["<dynamic-module-store>"] += 1
        self.generic_visit(node)

    def _scope(self, node: ast.AST, name: str) -> None:
        self.counts[name] += 1
        for decorator in getattr(node, "decorator_list", []):
            self.visit(decorator)
        for default in [
                *getattr(getattr(node, "args", None), "defaults", []),
                *getattr(getattr(node, "args", None), "kw_defaults", [])]:
            if default is not None:
                self.visit(default)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        self._scope(node, node.name)

    def visit_AsyncFunctionDef(  # noqa: N802
            self, node: ast.AsyncFunctionDef) -> None:
        self._scope(node, node.name)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
        self.counts[node.name] += 1
        for base in node.bases:
            self.visit(base)
        for keyword in node.keywords:
            self.visit(keyword.value)
        for decorator in node.decorator_list:
            self.visit(decorator)

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        for alias in node.names:
            self.counts[alias.asname or alias.name.split(".")[0]] += 1

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        for alias in node.names:
            self.counts[alias.asname or alias.name] += 1


def _module_binding_counts(tree: ast.Module) -> Counter[str]:
    visitor = ModuleBindingVisitor()
    visitor.visit(tree)
    return visitor.counts


def _dynamic_namespace_violation_count(tree: ast.Module) -> int:
    forbidden_names = {
        "__builtins__", "__import__", "eval", "exec", "globals", "locals",
        "vars",
    }
    protected_modules = {
        "ast", "builtins", "copy", "hashlib", "json",
    }
    count = sum(
        isinstance(node, ast.Name) and node.id in forbidden_names
        for node in ast.walk(tree))
    count += sum(
        isinstance(node, ast.Attribute) and
        isinstance(node.ctx, (ast.Store, ast.Del)) and
        isinstance(node.value, ast.Name) and
        node.value.id in protected_modules
        for node in ast.walk(tree))
    count += sum(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id in {"setattr", "delattr"} and bool(node.args) and
        isinstance(node.args[0], ast.Name) and
        node.args[0].id in protected_modules | {"__builtins__"}
        for node in ast.walk(tree))
    return count


def _tuple_first_name(node: ast.AST, expected: str) -> bool:
    return (
        isinstance(node, ast.Tuple) and len(node.elts) == 8 and
        isinstance(node.elts[0], ast.Name) and node.elts[0].id == expected)


def _v14_exact12_runtime_wiring_census_core(
        trees: Mapping[str, ast.Module],
        environments: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Reject static-only exact12 decoys and the inherited exact17/21 path."""
    expected_exact10_expression = ast.parse(
        'tuple((role, "CM2_C79G_V15_V14_" + role.upper() + "_FD") '
        'for role, _, _, _ in V14_PUBLISHED_EXACT10_WITNESS)',
        mode="eval").body
    expected_exact10_dump = ast.dump(
        expected_exact10_expression, include_attributes=False)
    terminal_definitions: dict[str, int] = {}
    terminal_calls: dict[str, list[str]] = {}
    terminal_call_counts: dict[str, int] = {}
    terminal_ast_hashes: dict[str, str | None] = {}
    live_authority_constructor_owners: dict[str, list[str]] = {}
    authority_constructor_call_counts: dict[str, int] = {}
    fd_order_matches: dict[str, bool] = {}
    exact10_fd_order_matches: dict[str, bool] = {}
    exact12_role_order_matches: dict[str, bool] = {}
    runtime_owner_ast_hashes: dict[str, dict[str, str]] = {}
    need_ast_hashes: dict[str, str] = {}
    critical_binding_failures: dict[str, dict[str, int]] = {}
    dynamic_namespace_violations: dict[str, int] = {}
    stale_symbol_counts: dict[str, int] = {}
    stale_exact17_literal_counts: dict[str, int] = {}
    stale_proof_key_counts: dict[str, int] = {}
    current_exact8_first_matches: dict[str, bool] = {}
    expected_terminal_call_owners = {
        "producer": ["HeldSelf.__init__", "HeldSelf.terminal_replay"],
        "consumer": [
            "HeldInheritedV14AuthorityExact12.__init__",
            "HeldInheritedV14AuthorityExact12.terminal_replay",
        ],
        "launcher": [
            "HeldBundle._hold_v14_inherited_authority_exact12",
            "HeldBundle.terminal_replay",
        ],
    }
    expected_constructor_owners = {
        "producer": ["ensure_launch_configuration"],
        "consumer": ["main"],
        "launcher": ["main"],
    }
    constructor_names = {
        "producer": "HeldSelf",
        "consumer": "HeldInheritedV14AuthorityExact12",
        "launcher": "HeldBundle",
    }
    critical_builtins = {
        "all", "any", "bool", "bytes", "dict", "isinstance", "len", "list",
        "next", "set", "str", "tuple", "type", "zip",
    }
    expected_role_order_dump = ast.dump(ast.parse(
        "tuple(row[0] for row in V14_INHERITED_AUTHORITY_EXACT12)",
        mode="eval").body, include_attributes=False)
    stale_proof_keys = {
        "seventeen_incident_authority_inputs_inherited_as_held_fds",
        "seventeen_incident_held_fds_path_identity_mount_and_hash_revalidated",
    }
    stale_exact17_string_markers = stale_proof_keys | {
        "inherited_incident_authority_exact17_held_and_terminally_replayed",
        "INHERITED_INCIDENT_AUTHORITY_EXACT17",
    }

    for role, tree in trees.items():
        terminal_definitions[role] = sum(
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "terminal_replay_v14_inherited_authority_exact12"
            for node in tree.body)
        terminal_calls[role] = _function_owner_names(
            tree, "terminal_replay_v14_inherited_authority_exact12")
        terminal_call_counts[role] = sum(
            isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "terminal_replay_v14_inherited_authority_exact12"
            for node in ast.walk(tree))
        terminal_functions = [
            node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "terminal_replay_v14_inherited_authority_exact12"]
        terminal_ast_hashes[role] = (
            sha256_bytes(ast.dump(
                terminal_functions[0], annotate_fields=True,
                include_attributes=False).encode("utf-8"))
            if len(terminal_functions) == 1 else None)
        live_authority_constructor_owners[role] = _constructor_owner_names(
            tree, constructor_names[role])
        authority_constructor_call_counts[role] = sum(
            isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == constructor_names[role]
            for node in ast.walk(tree))
        runtime_owner_ast_hashes[role] = {
            owner: _normalized_owned_function_sha256(tree, owner)
            for owner in V15_EXPECTED_RUNTIME_OWNER_AST_SHA256[role]}
        need_ast_hashes[role] = _normalized_owned_function_sha256(
            tree, "module.need")
        bindings = _module_binding_counts(tree)
        critical_binding_failures[role] = {
            name: bindings[name]
            for name in sorted(critical_builtins)
            if bindings[name] != 0}
        for required_import in ("Mapping", "ast", "copy", "hashlib", "json"):
            if bindings[required_import] != 1:
                critical_binding_failures[role][required_import] = bindings[
                    required_import]
        if bindings["need"] != 1:
            critical_binding_failures[role]["need"] = bindings["need"]
        if bindings["<dynamic-module-store>"] != 0:
            critical_binding_failures[role]["<dynamic-module-store>"] = \
                bindings["<dynamic-module-store>"]
        forbidden_global_rebinds = sorted({
            name for node in ast.walk(tree) if isinstance(node, ast.Global)
            for name in node.names
            if name in critical_builtins | {
                "Mapping", "ast", "copy", "hashlib", "json", "need"}})
        for name in forbidden_global_rebinds:
            critical_binding_failures[role]["global:" + name] = 1
        dynamic_namespace_violations[role] = \
            _dynamic_namespace_violation_count(tree)
        try:
            exact10_node = _unique_assignment_value(
                tree, "V14_EXACT10_FD_ENV_ORDER")
            exact10_fd_order_matches[role] = ast.dump(
                exact10_node, include_attributes=False) == expected_exact10_dump
        except ValueError:
            exact10_fd_order_matches[role] = False
        try:
            exact12_node = _unique_assignment_value(
                tree, "V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER")
            fd_order_matches[role] = (
                _fd_env_order_value(exact12_node, environments[role]) ==
                V14_EXACT12_FD_ENV_ORDER)
        except ValueError:
            fd_order_matches[role] = False
        try:
            role_order_node = _unique_assignment_value(
                tree, "V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER")
            exact12_role_order_matches[role] = (
                ast.dump(role_order_node, include_attributes=False) ==
                expected_role_order_dump)
        except ValueError:
            exact12_role_order_matches[role] = False

        identifiers: list[str] = []
        literals: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                identifiers.append(node.id)
            elif isinstance(node, ast.Attribute):
                identifiers.append(node.attr)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                  ast.ClassDef)):
                identifiers.append(node.name)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                literals.append(node.value)
        stale_symbol_counts[role] = sum(
            value == "inherited_incident_evidence_fds" or
            value.startswith("INCIDENT_AUTHORITY_INHERITED_EXACT") or
            value.startswith("HeldInheritedIncidentAuthorityExact")
            for value in identifiers)
        stale_exact17_literal_counts[role] = sum(
            value in stale_exact17_string_markers for value in literals)
        stale_proof_key_counts[role] = sum(
            value in stale_proof_keys for value in literals)

    exact8_assignments = {
        "producer": _unique_assignment_value(trees["producer"], "COLD_EXACT8"),
        "consumer": _unique_assignment_value(
            trees["consumer"], "V15_CURRENT_EXACT8"),
        "launcher": function_assignment(
            trees["launcher"], "configure_workspace_paths", "EXACT8"),
    }
    current_exact8_first_matches = {
        role: _tuple_first_name(
            node, "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT")
        for role, node in exact8_assignments.items()}

    launcher = trees["launcher"]
    held_bundle_rows = [
        node for node in launcher.body
        if isinstance(node, ast.ClassDef) and node.name == "HeldBundle"]
    holder_method_count = 0
    holder_attribute_reference_count = 0
    holder_exact12_len_gate_count = 0
    holder_exact12_unique_gate_count = 0
    holder_returns_result = False
    holder_result_order_matches = False
    holder_result_assignment_count = 0
    holder_result_write_count = 0
    holder_exact_body_statement_count = 0
    if len(held_bundle_rows) == 1:
        held_bundle = held_bundle_rows[0]
        holder_attribute_reference_count = sum(
            isinstance(node, ast.Attribute) and
            node.attr == "v14_inherited_authority_exact12"
            for node in ast.walk(held_bundle))
        methods = [
            node for node in held_bundle.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
            node.name == "inherited_v14_authority_exact12_fds"]
        holder_method_count = len(methods)
        if len(methods) == 1:
            method = methods[0]
            holder_exact_body_statement_count = len(method.body)
            comparisons = [
                node for node in ast.walk(method)
                if isinstance(node, ast.Compare) and
                _is_direct_need_condition(method, node)]
            holder_exact12_len_gate_count = sum(
                _compare_has_len_gate(node, "result", False, 12)
                for node in comparisons)
            holder_exact12_unique_gate_count = sum(
                _compare_has_len_gate(node, "result", True, 12)
                for node in comparisons)
            returns = function_scope_returns(method)
            holder_returns_result = (
                len(returns) == 1 and isinstance(returns[0].value, ast.Name) and
                returns[0].value.id == "result" and bool(method.body) and
                method.body[-1] is returns[0])
            holder_result_assignments = [
                node.value for node in method.body
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == "result"]
            holder_result_assignment_count = sum(
                isinstance(node, (ast.Assign, ast.AnnAssign)) and
                ((isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == "result"
                    for target in node.targets)) or
                 (isinstance(node, ast.AnnAssign) and
                  isinstance(node.target, ast.Name) and
                  node.target.id == "result"))
                for node in ast.walk(method))
            holder_result_write_count = _name_write_count(method, "result")
            expected_holder_result = ast.parse(
                "tuple(self.v14_inherited_authority_by_role[role].fd "
                "for role in V14_INHERITED_AUTHORITY_EXACT12_ROLE_ORDER)",
                mode="eval").body
            holder_result_order_matches = (
                len(holder_result_assignments) ==
                    holder_result_assignment_count ==
                    holder_result_write_count == 1 and
                ast.dump(holder_result_assignments[0],
                         include_attributes=False) ==
                ast.dump(expected_holder_result, include_attributes=False))

    child_environment = unique_module_function(launcher, "child_environment")
    child_pass_fds = unique_module_function(launcher, "child_pass_fds")
    environment_exact12_calls = _method_calls(
        child_environment, "bundle", "inherited_v14_authority_exact12_fds")
    environment_fd_assignment_matches = False
    environment_authority_mapping_matches = False
    environment_returns_result = False
    environment_result_assignment_count = sum(
        isinstance(node, (ast.Assign, ast.AnnAssign)) and
        ((isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "result"
            for target in node.targets)) or
         (isinstance(node, ast.AnnAssign) and
          isinstance(node.target, ast.Name) and node.target.id == "result"))
        for node in ast.walk(child_environment))
    environment_authority_fds_write_count = _name_write_count(
        child_environment, "authority_fds")
    environment_authority_mapping_write_count = _name_write_count(
        child_environment, "authority_environment")
    environment_result_write_count = _name_write_count(
        child_environment, "result")
    environment_fd_assignments = [
        node for node in child_environment.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "authority_fds"]
    if len(environment_fd_assignments) == 1:
        expected_environment_call = ast.parse(
            "bundle.inherited_v14_authority_exact12_fds()",
            mode="eval").body
        environment_fd_assignment_matches = (
            ast.dump(environment_fd_assignments[0].value,
                     include_attributes=False) ==
            ast.dump(expected_environment_call, include_attributes=False))
    authority_mapping_assignments = [
        node.value for node in child_environment.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "authority_environment"]
    expected_authority_mapping = ast.parse(
        "{env_name: str(descriptor) "
        "for ((_, env_name), descriptor) in zip("
        "V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER, authority_fds, "
        "strict=True)}", mode="eval").body
    environment_authority_mapping_matches = (
        len(authority_mapping_assignments) == 1 and
        ast.dump(authority_mapping_assignments[0], include_attributes=False) ==
        ast.dump(expected_authority_mapping, include_attributes=False))
    environment_authority_update_count = sum(
        isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and
        isinstance(node.value.func, ast.Attribute) and
        isinstance(node.value.func.value, ast.Name) and
        node.value.func.value.id == "result" and
        node.value.func.attr == "update" and len(node.value.args) == 1 and
        isinstance(node.value.args[0], ast.Name) and
        node.value.args[0].id == "authority_environment" and
        not node.value.keywords
        for node in child_environment.body)
    environment_returns = function_scope_returns(child_environment)
    environment_returns_result = (
        len(environment_returns) == 1 and child_environment.body and
        child_environment.body[-1] is environment_returns[0] and
        isinstance(environment_returns[0].value, ast.Name) and
        environment_returns[0].value.id == "result")
    environment_order_reference_count = sum(
        isinstance(node, ast.Name) and
        node.id == "V14_INHERITED_AUTHORITY_EXACT12_FD_ENV_ORDER"
        for node in ast.walk(child_environment))
    pass_exact12_calls = _method_calls(
        child_pass_fds, "bundle", "inherited_v14_authority_exact12_fds")
    result_assignments = [
        node.value for node in child_pass_fds.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and
        node.targets[0].id == "result"]
    pass_result_assignment_count = sum(
        isinstance(node, (ast.Assign, ast.AnnAssign)) and
        ((isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "result"
            for target in node.targets)) or
         (isinstance(node, ast.AnnAssign) and
          isinstance(node.target, ast.Name) and node.target.id == "result"))
        for node in ast.walk(child_pass_fds))
    pass_result_write_count = _name_write_count(child_pass_fds, "result")
    expected_pass_tuple = ast.parse(
        "(child_exec.fd, source.fd, coordination.fd, "
        "bundle.bootstrap.root_fd, "
        "*bundle.inherited_v14_authority_exact12_fds())",
        mode="eval").body
    pass_tuple_order_matches = (
        len(result_assignments) == pass_result_assignment_count == 1 and
        ast.dump(result_assignments[0], include_attributes=False) ==
        ast.dump(expected_pass_tuple, include_attributes=False))
    pass_comparisons = [
        node for node in ast.walk(child_pass_fds)
        if isinstance(node, ast.Compare) and
        _is_direct_need_condition(child_pass_fds, node)]
    pass_len16_gate_count = sum(
        _compare_has_len_gate(node, "result", False, 16)
        for node in pass_comparisons)
    pass_unique16_gate_count = sum(
        _compare_has_len_gate(node, "result", True, 16)
        for node in pass_comparisons)
    pass_literal21_count = sum(
        isinstance(node, ast.Constant) and type(node.value) is int and
        node.value == 21 for node in ast.walk(child_pass_fds))
    pass_returns = function_scope_returns(child_pass_fds)
    pass_returns_result = (
        len(pass_returns) == 1 and child_pass_fds.body and
        child_pass_fds.body[-1] is pass_returns[0] and
        isinstance(pass_returns[0].value, ast.Name) and
        pass_returns[0].value.id == "result")

    source_closure = all(
        terminal_definitions.get(role) == 1 and
        terminal_call_counts.get(role) == 2 and
        terminal_calls.get(role) == expected_terminal_call_owners[role] and
        terminal_ast_hashes.get(role) ==
            V15_EXPECTED_EXACT12_TERMINAL_REPLAY_AST_SHA256 and
        runtime_owner_ast_hashes.get(role) ==
            V15_EXPECTED_RUNTIME_OWNER_AST_SHA256[role] and
        need_ast_hashes.get(role) == V15_EXPECTED_NEED_AST_SHA256[role] and
        not critical_binding_failures.get(role) and
        dynamic_namespace_violations.get(role) == 0 and
        authority_constructor_call_counts.get(role) == 1 and
        live_authority_constructor_owners.get(role) ==
            expected_constructor_owners[role] and
        exact10_fd_order_matches.get(role) is True and
        exact12_role_order_matches.get(role) is True and
        fd_order_matches.get(role) is True and
        stale_symbol_counts.get(role) == 0 and
        stale_exact17_literal_counts.get(role) == 0 and
        stale_proof_key_counts.get(role) == 0 and
        current_exact8_first_matches.get(role) is True
        for role in ("producer", "consumer", "launcher"))
    launcher_closure = (
        holder_method_count == 1 and holder_attribute_reference_count >= 1 and
        holder_exact12_len_gate_count == 1 and
        holder_exact12_unique_gate_count == 1 and holder_returns_result and
        holder_result_order_matches and holder_result_assignment_count == 1 and
        holder_exact_body_statement_count == 4 and
        len(environment_exact12_calls) == 1 and
        environment_fd_assignment_matches and
        environment_authority_mapping_matches and
        len(child_environment.body) == 7 and
        environment_authority_fds_write_count == 1 and
        environment_authority_mapping_write_count == 1 and
        environment_result_assignment_count ==
            environment_result_write_count == 1 and
        environment_authority_update_count == 1 and
        environment_returns_result and
        environment_order_reference_count >= 1 and
        len(pass_exact12_calls) == 1 and pass_tuple_order_matches and
        pass_len16_gate_count == 1 and pass_unique16_gate_count == 1 and
        len(child_pass_fds.body) == 3 and pass_literal21_count == 0 and
        pass_result_assignment_count == pass_result_write_count == 1 and
        pass_returns_result)
    return {
        "terminal_exact12_definition_count_by_source": terminal_definitions,
        "terminal_exact12_call_count_by_source": terminal_call_counts,
        "terminal_exact12_live_callsite_owners_by_source": terminal_calls,
        "terminal_exact12_normalized_ast_sha256_by_source":
            terminal_ast_hashes,
        "terminal_exact12_expected_normalized_ast_sha256":
            V15_EXPECTED_EXACT12_TERMINAL_REPLAY_AST_SHA256,
        "live_exact12_authority_constructor_call_count_by_source":
            authority_constructor_call_counts,
        "runtime_owner_normalized_ast_sha256_by_source":
            runtime_owner_ast_hashes,
        "runtime_owner_expected_normalized_ast_sha256_by_source":
            V15_EXPECTED_RUNTIME_OWNER_AST_SHA256,
        "need_normalized_ast_sha256_by_source": need_ast_hashes,
        "need_expected_normalized_ast_sha256_by_source":
            V15_EXPECTED_NEED_AST_SHA256,
        "critical_builtin_or_dependency_binding_failures_by_source":
            critical_binding_failures,
        "dynamic_namespace_mutation_violation_count_by_source":
            dynamic_namespace_violations,
        "dynamic_namespace_mutation_negative_self_test": all(
            _dynamic_namespace_violation_count(ast.parse(source)) > 0
            for source in (
                'globals().__setitem__("need", lambda condition, label: None)',
                'globals()["need"] = lambda condition, label: None',
                'vars()["need"] = lambda condition, label: None',
            )),
        "live_exact12_authority_constructor_owners_by_source":
            live_authority_constructor_owners,
        "exact10_fd_env_order_matches_by_source": exact10_fd_order_matches,
        "exact12_role_order_matches_by_source": exact12_role_order_matches,
        "exact12_fd_env_order_matches_by_source": fd_order_matches,
        "stale_exact17_symbol_count_by_source": stale_symbol_counts,
        "stale_exact17_literal_count_by_source": stale_exact17_literal_counts,
        "stale_execution_proof_key_count_by_source": stale_proof_key_counts,
        "current_exact8_first_is_v14_supersession_receipt_by_source":
            current_exact8_first_matches,
        "launcher_holder_method_count": holder_method_count,
        "launcher_holder_attribute_reference_count":
            holder_attribute_reference_count,
        "launcher_holder_exact12_len_gate_count":
            holder_exact12_len_gate_count,
        "launcher_holder_exact12_unique_gate_count":
            holder_exact12_unique_gate_count,
        "launcher_holder_returns_computed_result": holder_returns_result,
        "launcher_holder_result_exact_role_order_matches":
            holder_result_order_matches,
        "launcher_holder_result_assignment_count":
            holder_result_assignment_count,
        "launcher_holder_result_write_count": holder_result_write_count,
        "launcher_holder_exact_body_statement_count":
            holder_exact_body_statement_count,
        "child_environment_exact12_holder_call_count":
            len(environment_exact12_calls),
        "child_environment_holder_call_is_direct_assignment":
            environment_fd_assignment_matches,
        "child_environment_exact12_zip_mapping_matches":
            environment_authority_mapping_matches,
        "child_environment_result_assignment_count":
            environment_result_assignment_count,
        "child_environment_authority_fds_write_count":
            environment_authority_fds_write_count,
        "child_environment_authority_mapping_write_count":
            environment_authority_mapping_write_count,
        "child_environment_result_write_count":
            environment_result_write_count,
        "child_environment_exact_body_statement_count":
            len(child_environment.body),
        "child_environment_authority_update_count":
            environment_authority_update_count,
        "child_environment_returns_result": environment_returns_result,
        "child_environment_fd_env_order_reference_count":
            environment_order_reference_count,
        "child_pass_fds_exact12_holder_call_count": len(pass_exact12_calls),
        "child_pass_fds_prefix_then_exact12_order_matches":
            pass_tuple_order_matches,
        "child_pass_fds_exact16_len_gate_count": pass_len16_gate_count,
        "child_pass_fds_exact16_unique_gate_count": pass_unique16_gate_count,
        "child_pass_fds_stale_literal21_count": pass_literal21_count,
        "child_pass_fds_result_assignment_count":
            pass_result_assignment_count,
        "child_pass_fds_result_write_count": pass_result_write_count,
        "child_pass_fds_exact_body_statement_count":
            len(child_pass_fds.body),
        "child_pass_fds_returns_result": pass_returns_result,
        "matches": source_closure and launcher_closure and all(
            _dynamic_namespace_violation_count(ast.parse(source)) > 0
            for source in (
                'globals().__setitem__("need", lambda condition, label: None)',
                'globals()["need"] = lambda condition, label: None',
                'vars()["need"] = lambda condition, label: None',
            )),
    }


def v14_exact12_runtime_wiring_census(
        trees: Mapping[str, ast.Module],
        environments: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    current = _v14_exact12_runtime_wiring_census_core(trees, environments)

    stale_trees = {role: copy.deepcopy(tree) for role, tree in trees.items()}
    stale_pass = unique_module_function(stale_trees["launcher"], "child_pass_fds")
    stale_mutation_count = 0
    for node in ast.walk(stale_pass):
        if (isinstance(node, ast.Call) and
                isinstance(node.func, ast.Attribute) and
                node.func.attr == "inherited_v14_authority_exact12_fds"):
            node.func.attr = "renamed_legacy_seventeen_fds"
            stale_mutation_count += 1
    stale_rejected = (
        current.get("matches") is True and stale_mutation_count == 1 and
        _v14_exact12_runtime_wiring_census_core(
            stale_trees, environments)["matches"] is False)

    dead_trees = {role: copy.deepcopy(tree) for role, tree in trees.items()}
    consumer_class = next(
        (node for node in dead_trees["consumer"].body
         if isinstance(node, ast.ClassDef) and
         node.name == "HeldInheritedV14AuthorityExact12"), None)
    dead_mutation_count = 0
    if consumer_class is not None:
        terminal = next(
            (node for node in consumer_class.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
             node.name == "terminal_replay"), None)
        if terminal is not None:
            for index, statement in enumerate(terminal.body):
                if any(
                        isinstance(node, ast.Call) and
                        isinstance(node.func, ast.Name) and
                        node.func.id ==
                            "terminal_replay_v14_inherited_authority_exact12"
                        for node in ast.walk(statement)):
                    terminal.body[index] = ast.If(
                        test=ast.Constant(value=False),
                        body=[statement], orelse=[])
                    dead_mutation_count += 1
    dead_rejected = (
        current.get("matches") is True and dead_mutation_count == 1 and
        _v14_exact12_runtime_wiring_census_core(
            dead_trees, environments)["matches"] is False)

    current.update({
        "in_memory_renamed_legacy17_passfd_mutation_count":
            stale_mutation_count,
        "in_memory_renamed_legacy17_passfd_rejected": stale_rejected,
        "in_memory_dead_terminal_replay_mutation_count": dead_mutation_count,
        "in_memory_dead_terminal_replay_rejected": dead_rejected,
    })
    current["matches"] = bool(
        current.get("matches") and stale_rejected and dead_rejected)
    return current


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

    helper_failures: list[str] = []
    try:
        producer_registry = producer_source_registry_census(trees["producer"])
    except Exception as exc:
        producer_registry = {
            "matches": False,
            "error": type(exc).__name__ + ":" + str(exc),
        }
    if producer_registry.get("matches") is not True:
        helper_failures.append("producer_source_registry_exact67_plus7_plus1")

    producer_shape = producer_registry.get("computed_closed_registry_key_count")
    try:
        launcher_helper = launcher_runtime_registry_helper_census(
            trees["launcher"],
            producer_shape if type(producer_shape) is int else -1)
    except Exception as exc:
        launcher_helper = {
            "matches": False,
            "error": type(exc).__name__ + ":" + str(exc),
        }
    if launcher_helper.get("matches") is not True:
        helper_failures.append(
            "actual_launcher_runtime_registry_helper_held_producer_exact75")

    source_shape_declarations = {
        role: shape_declarations(tree) for role, tree in trees.items()}
    shape_sources_ok = (
        all(values and set(values) == {75}
            for values in source_shape_declarations.values()) and
        set(source_shape_declarations) == {"producer", "consumer", "launcher"})

    exact12_review, exact12_filesystem_failures = held_v14_exact12_review()
    source_exact12_rows, source_exact12_failures = source_exact12_pin_review(
        environments)
    try:
        exact12_runtime_wiring = v14_exact12_runtime_wiring_census(
            trees, environments)
    except Exception as exc:
        exact12_runtime_wiring = {
            "matches": False,
            "error": type(exc).__name__ + ":" + str(exc),
        }
    if exact12_runtime_wiring.get("matches") is not True:
        helper_failures.append(
            "v14_exact12_actual_runtime_wiring_rejects_exact17_and_passfd21")

    json_duplicate_count = 0
    object_failures: list[str] = []
    json_values: dict[str, dict[str, Any]] = {}
    json_raw: dict[str, bytes] = {}
    current_json = (
        ("schema", SCHEMA, False),
        ("contract", CONTRACT, True),
        ("transition", TRANSITION, True),
        ("audit", AUDIT, True),
    )
    current_presence = tuple(path.is_file() for _, path, _ in current_json)
    lifecycle_by_presence = {
        (False, False, False, False): "DRAFT",
        (True, True, False, False): "CORE_PINNED",
        (True, True, True, True): "FINAL_STATIC",
    }
    source_lifecycle_state = lifecycle_by_presence.get(
        current_presence, "INVALID_MIXED_JSON")
    if source_lifecycle_state == "INVALID_MIXED_JSON":
        object_failures.append("current_v15_json_lifecycle_mixed")

    for label, path, needs_closure in current_json:
        if not path.is_file():
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

    pin_failures = [
        *exact12_filesystem_failures,
        *source_exact12_failures,
    ]
    producer_env = environments["producer"]
    consumer_env = environments["consumer"]

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
    receipt_expected = (V14_SUPERSESSION_PIN[1], V14_SUPERSESSION_PIN[2])
    launcher_state: str | None = None
    launcher_normalized: str | None = None
    try:
        launcher_state, launcher_normalized = launcher_lifecycle_state(
            source_raw["launcher"], final_base7_expected, receipt_expected)
    except (UnicodeDecodeError, SyntaxError, ValueError) as exc:
        pin_failures.append(
            "launcher_lifecycle_rejected:" + type(exc).__name__ + ":" +
            str(exc))

    if source_lifecycle_state == "DRAFT":
        add_pin_failure(
            pin_failures,
            producer_env.get("FINAL_V15_CORE_PINS_INSTALLED") is False,
            "producer_draft_core_flag_not_false")
        add_pin_failure(
            pin_failures,
            consumer_env.get("FINAL_CURRENT_V15_PINS_INSTALLED") is False,
            "consumer_draft_current_flag_not_false")
        add_pin_failure(
            pin_failures, launcher_state == "DRAFT",
            "launcher_not_complete_draft_during_draft_state")
    elif source_lifecycle_state in {"CORE_PINNED", "FINAL_STATIC"}:
        add_pin_failure(
            pin_failures,
            producer_env.get("FINAL_V15_CORE_PINS_INSTALLED") is True,
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
            consumer_env.get("FINAL_CURRENT_V15_PINS_INSTALLED") is True,
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
        if source_lifecycle_state == "CORE_PINNED":
            add_pin_failure(
                pin_failures, launcher_state == "DRAFT",
                "launcher_not_draft_during_core_pinned_state")
        else:
            add_pin_failure(
                pin_failures, launcher_state == "FINAL",
                "launcher_not_final_during_final_static_state")
            add_pin_failure(
                pin_failures,
                "audit" in json_values and launcher_normalized is not None and
                audit_bundle_and_template_match(
                    json_values["audit"], final_base7_expected,
                    launcher_normalized),
                "launcher_final_pin_normalized_template_or_audit_bundle_mismatch")
    else:
        pin_failures.append("invalid_current_v15_json_lifecycle")

    audit_declared_shape: int | None = None
    if isinstance(json_values.get("audit"), dict):
        closure = json_values["audit"].get("schema_and_constructor_closure")
        if isinstance(closure, dict):
            shapes = closure.get("output_shape_key_counts")
            if isinstance(shapes, dict) and type(
                    shapes.get("producerSourceRegistry")) is int:
                audit_declared_shape = shapes["producerSourceRegistry"]
    shape_consensus_matches = (
        producer_registry.get("matches") is True and
        launcher_helper.get("matches") is True and shape_sources_ok and
        exact12_runtime_wiring.get("matches") is True and
        (source_lifecycle_state != "FINAL_STATIC" or audit_declared_shape == 75))
    shape_consensus = {
        "producer_independent_closed_key_count": producer_shape,
        "launcher_actual_runtime_helper_matches": launcher_helper.get("matches"),
        "source_declared_producerSourceRegistry_values":
            source_shape_declarations,
        "audit_declared_producerSourceRegistry":
            audit_declared_shape,
        "v14_inherited_authority_runtime_wiring_matches":
            exact12_runtime_wiring.get("matches"),
        "expected_closed_key_count": 75,
        "matches": shape_consensus_matches,
    }

    terminal_source_replay = {
        role: stable_read(path) == source_raw[role]
        for role, path in SOURCES}
    terminal_source_replay_matches = all(terminal_source_replay.values())

    static_failures: list[str] = []
    current_census = (len(rows_a), digest_a)
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
        ("refuse_stale_v11_or_v14_callsite_census",
         current_census not in STALE_CALLSITE_CENSUSES),
        ("common_kind_key_and_sum_closure",
         set(kind_census) == set(CALLSITE_KINDS) and
         sum(kind_census.values()) == len(rows_b)),
        ("strict_json_duplicates_zero", json_duplicate_count == 0),
        ("required_object_closures_zero", not object_failures),
        ("v14_exact12_filesystem_and_source_pin_graph_close",
         not exact12_filesystem_failures and not source_exact12_failures),
        ("v14_exact12_actual_runtime_wiring_closes_and_old_exact17_21_absent",
         exact12_runtime_wiring.get("matches") is True),
        ("producer_registry_exact67_plus_proof7_plus_close1_equals75",
         producer_registry.get("matches") is True),
        ("actual_launcher_runtime_helper_uses_held_producer_and_rejects62",
         launcher_helper.get("matches") is True),
        ("runtime_registry_shape_source_and_audit_consensus_exact75",
         shape_consensus_matches),
        ("three_source_terminal_byte_replay_unchanged",
         terminal_source_replay_matches),
        ("pre_audit_pin_failures_zero", not pin_failures),
        ("launcher_lifecycle_positive_and_negative_self_tests",
         launcher_lifecycle_self_tests()),
        ("producer_exact_draft_and_not_final_main_gate", exact_main_gate(
            trees["producer"], "V15_DRAFT_RUNTIME_DISABLED",
            "FINAL_V15_CORE_PINS_INSTALLED")),
        ("consumer_exact_draft_and_not_final_main_gate", exact_main_gate(
            trees["consumer"], "V15_DRAFT_RUNTIME_DISABLED",
            "FINAL_CURRENT_V15_PINS_INSTALLED")),
        ("launcher_exact_draft_and_not_final_main_gate", exact_main_gate(
            trees["launcher"], "V15_DRAFT_RUNTIME_DISABLED",
            "FINAL_BASE7_PINS_INSTALLED")),
        ("three_runtime_disable_flags_true", all(
            env.get("V15_DRAFT_RUNTIME_DISABLED") is True
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
            static_failures.append("v15_protocol_pyc_present")

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
        "source_lifecycle_state": source_lifecycle_state,
        "current_json_presence": {
            label: present
            for (label, _, _), present in zip(current_json, current_presence)},
        "zero_key_observations": zero,
        "static_failures": static_failures,
        "object_closure_failures": object_failures,
        "pin_failures": pin_failures,
        "helper_failures": helper_failures,
        "producer_source_registry_census": producer_registry,
        "launcher_runtime_registry_helper_census": launcher_helper,
        "runtime_registry_shape_consensus": shape_consensus,
        "v14_exact12_runtime_wiring_census": exact12_runtime_wiring,
        "terminal_source_byte_replay": terminal_source_replay,
        "v14_exact12_filesystem": exact12_review,
        "v14_exact12_source_pins": source_exact12_rows,
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
        "source_lifecycle_state": source_lifecycle_state,
        "v14_inherited_authority_exact12_member_count": 12,
        "v14_inherited_authority_exact12_canonical_sha256":
            exact12_review["ordered_exact12_canonical_sha256"],
        "v14_supersession_receipt_file_sha256": V14_SUPERSESSION_PIN[1],
        "v14_supersession_receipt_object_sha256": V14_SUPERSESSION_PIN[2],
        "producer_source_registry_census": producer_registry,
        "launcher_runtime_registry_helper_census": launcher_helper,
        "runtime_registry_shape_consensus": shape_consensus,
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
            "FAIL_CLOSED_V15_STATIC_CHECKER_CENSUS__"
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
