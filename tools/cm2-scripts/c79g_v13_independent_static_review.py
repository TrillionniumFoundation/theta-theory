#!/usr/bin/env python3
"""Read-only, fail-closed static review for the C79g v13 successor.

The protocol sources are read as inert bytes and are never imported or
executed.  Python validation is limited to AST parsing, symtable analysis and
in-memory ``compile``.  JSON surfaces are decoded with duplicate-key tracking.

This reviewer deliberately distinguishes a safe draft state from a final
static bundle.  A draft may pass the absence/disabled checks, but the overall
result remains FAIL_CLOSED until all four v13 JSON surfaces exist, close, and
all three final pin flags are true.  Publication and runtime are never
authorized by this program.
"""

from __future__ import annotations

import ast
import builtins
import copy
import hashlib
import json
import os
import re
import stat
import symtable
from pathlib import Path
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
CHECKPOINT = (
    "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab")

V13_PYTHON = {
    "producer": OUT / f"{BASE}_v13.py",
    "consumer": OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_v13.py"),
    "launcher": OUT / f"{BASE}_cold_launch_v13.py",
}
V13_PYC_DIRECTORY = OUT / "__pycache__"
V13_JSON = {
    "schema": OUT / f"{BASE}_schema_v13.json",
    "contract": OUT / f"{BASE}_contract_v13.json",
    "transition": OUT / f"{BASE}_v12_to_v13_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v13.json",
}
V13_MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v13.sha256"
V13_OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v13.json"
V13_JSON_BUILDER = ROOT / "scripts" / "c79g_v13_json_draft_builder.py"
V5_REJECTION = RUNTIME / f"c79g-v5-rejections-{CHECKPOINT}" / "rejection.json"
V12_REJECTION = RUNTIME / f"c79g-v12-rejections-{CHECKPOINT}" / "rejection.json"

EXPECTED_V12_REJECTION_FILE_SHA256 = (
    "b6b087a3e31b25f0bbe0ffe6caa40f3c181b2f77c5c8b6169ce3af27439762b5")
EXPECTED_V12_REJECTION_OBJECT_SHA256 = (
    "18951895ea97f455bc3294e8ef9cdaa937f3b16e9831275b047e88142e9b91f6")
EXPECTED_V5_REJECTION_FILE_SHA256 = (
    "c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5")
EXPECTED_V5_REJECTION_OBJECT_SHA256 = (
    "9a94bf8b580f6145c4977dd335d9a63c69057d18d62678ab47c7916c764f8e4c")
EXPECTED_EXACT39_KEYSET_SHA256 = (
    "3b74017677a537d23cacbfbf95f1cc78e3b33fc4839be24e02e848bdd7410460")
EXPECTED_EXACT56_KEYSET_SHA256 = (
    "9c272f16d92497a7c5ced499e9e42c514b81cbfddcdb3f79c4f33837836e057e")
EXPECTED_V12_INCIDENT_HELPER_AST_SHA256 = (
    "fa4cf4f0bdb9e9f1b2a3bdeed7d7271830833395a2f58d32457f363e596fb5e9")

HISTORICAL_REJECTION_PINS = {
    "v3": (
        "57ce7a4361555c4ff403f725f17ef9cef50446a2e76d7086635c30a0f17bc62f",
        "c946e0d8170a75e32aa7031b42cf0dd5b7b585ba463b7b1ce0010cb65bb3b421",
        37, "21ba021c649349266d95670e63136fef1772b5d8dbb79334907c9df400620a18"),
    "v5": (
        "c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5",
        "9a94bf8b580f6145c4977dd335d9a63c69057d18d62678ab47c7916c764f8e4c",
        39, "3b74017677a537d23cacbfbf95f1cc78e3b33fc4839be24e02e848bdd7410460"),
    "v6": (
        "3559dcfd9e6d0ebb0e093226d6d3ae8d09d67eaeb186d4ec956241af87fcbd06",
        "87c0cd17ae6ca3885a01da82b47b66e96419eb778594b51423eb04cf3c68f48c",
        41, "5881a652aabef3e7e65917689487f13b99bfa60fff0ebb7c144bc02b26897638"),
    "v7": (
        "63d4bbc4f50ef674b6b90f6fde625ac4705d5272f500fd495111d445274ebf6b",
        "29c43ad51082bd56c2291dea88b619731c2853969b79ea008abea1cca3c83ecd",
        43, "02b54c94602de1f5af8e545692f44815b9ac3ba334369dd96ee4e9b677bf1308"),
    "v8": (
        "3b00a60c6c30cc10171d82e8262f880d67aa975e9f040888a29d7bdb4014ef95",
        "9fbc65609f33a62751b9fc60aa4def316a499dae9e3f64e1d4ae8a3be58894d5",
        46, "a1da14307b813345ee0f8877550412b40951f7857e5972570ab41f97e2fe31bf"),
    "v9": (
        "bca8f1042a1f3ee5b82d85a2e10c6ed2bf35d486116870bf50387f9ee9dcd302",
        "682ead5d02c386b992c15e1e845e5e35a3147e0c1387d440c604f431c7a8b1b4",
        48, "d0617183e15fd4c5bfd3495d7dca56cb9aea7035bedf35a1bdf6efd166a70308"),
    "v10": (
        "1b5bbd9ec04f07e7d7d433685aa693b73bf2315a91e4813960bd5a81e8112828",
        "efdb614e870e70c20202834d3c6ec1a7513a3e98ba5cb4e1b32f87976a529d76",
        50, "01274ec0c36bd85423d385bdb22cdff7fe6ccfe2d114864994fc2ead2153eddb"),
    "v11": (
        "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8",
        "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a",
        52, "75ca9378fbff7a6956686e7390556fffa3d6ff939630ed47e8c8c185872e97f8"),
    "v12": (
        EXPECTED_V12_REJECTION_FILE_SHA256,
        EXPECTED_V12_REJECTION_OBJECT_SHA256,
        54, "271055dec2aa42fb77c14bbd9b5c19e6bd4281428a71dc5db55c7d0db168b985"),
}
HISTORICAL_REJECTION_VERSION_ORDER = tuple(HISTORICAL_REJECTION_PINS)

INCIDENT_FD_ENV_NAMES = (
    "V10_PRODUCER_FD_ENV", "V9_LAUNCHER_FD_ENV",
    "V11_PRODUCER_FD_ENV", "V11_LAUNCHER_FD_ENV",
    "V11_REJECTION_FD_ENV", "V12_PRODUCER_FD_ENV",
    "V12_CONSUMER_FD_ENV", "V12_LAUNCHER_FD_ENV",
    "V5_REJECTION_FD_ENV", "V12_REJECTION_FD_ENV",
)
EXPECTED_INCIDENT_HELPER_CALLSITES = {
    "producer": [
        ("HeldSelf", "__init__", 5),
        ("HeldSelf", "terminal_replay", 5),
    ],
    "consumer": [
        ("HeldInheritedIncidentAuthorityExact10", "__init__", 5),
        ("HeldInheritedIncidentAuthorityExact10", "terminal_replay", 5),
    ],
    "launcher": [
        ("HeldV12PredecessorExact10", "bind_history", 5),
        ("HeldV12PredecessorExact10", "terminal_replay", 5),
    ],
}

# The v12 published exact10 is immutable predecessor evidence.  The v12
# official rejection is intentionally separate and strictly later.
V12_EXACT10 = (
    (f".cm2-runtime/c79g-v11-rejections-{CHECKPOINT}/rejection.json",
     "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8",
     "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a"),
    (f"deliverables/{BASE}_schema_v12.json",
     "5ed911a55e8f90e750fdcaf6ab4fb6c9683bebaf66a4d6250329dff98acb2e28", None),
    (f"deliverables/{BASE}_contract_v12.json",
     "72246725b15891f92cbc6e3fa1c07ab4a76cdaa19f1b366a736f47f51989b343",
     "f5c1710817dc8e3aa7fe2bbf4b88e6e39baaa1b17bbeb0f8bf37c8c4575ae5d7"),
    (f"deliverables/{BASE}_v12.py",
     "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d", None),
    (f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_v12.py",
     "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed", None),
    (f"deliverables/{BASE}_v11_to_v12_static_launch_transition_receipt_v1.json",
     "45dabc1ef60eb2f8ba34aa7daa69f9d2b3bedccd4168d9c472bd4bbb696b5400",
     "0673ecafaa9991cd78e905e144e7c8c1b91717a3d753befa13e82552d44a4072"),
    (f"deliverables/{BASE}_static_audit_v12.json",
     "ac29b1e31e0d1b51e8610b7699d1aaf55c80fa6f13f00b20b209c2889e121d37",
     "c1473ae0f5a08d8772227f61a55bd32c479a7b5c7d40da17b37e796abf4d9783"),
    (f"deliverables/{BASE}_cold_launch_v12.py",
     "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba", None),
    (f"deliverables/{BASE}_cold_launch_manifest_v12.sha256",
     "297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6", None),
    (f"deliverables/{BASE}_cold_launch_outer_receipt_v12.json",
     "27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0",
     "bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d"),
)

EXACT39_KEYS = frozenset({
    "D02_formal_pending_task_count", "D02_gate_credit", "D02_started",
    "D02_task_credit", "D02_unlock", "closed_schema_file_sha256",
    "cold_launcher_file_sha256", "cold_manifest_file_sha256",
    "cold_outer_file_sha256", "cold_outer_object_sha256",
    "commit_operation", "consumer_file_sha256", "contract_file_sha256",
    "contract_object_sha256", "effective_checkpoint_object_sha256",
    "file_fsync_required", "formal_global_closure_credit",
    "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent",
    "namespace_at_rest_mode", "namespace_exact_path",
    "namespace_fsync_required_after_file_and_after_reseal",
    "namespace_lock_held_write_window_mode", "object_sha256",
    "official_writer_coordination_lock_held_for_entire_reject_command",
    "official_writer_coordination_lock_policy",
    "overwrite_delete_or_reuse_allowed",
    "partial_malformed_or_extra_namespace_entry_revokes_authority",
    "producer_file_sha256", "rejection_file_mode", "rejection_file_nlink",
    "rejection_reason", "runtime_parent_fsync_required_after_namespace_creation",
    "schema", "standalone_authority", "status", "target_exact_path",
    "target_is_protocol_and_checkpoint_deterministic",
    "v4_rejection_supersession_file_sha256",
    "v4_rejection_supersession_object_sha256",
})

V12_REJECTION_KEYS = frozenset(
    set(EXACT39_KEYS) |
    {f"v{version}_official_rejection_{kind}_sha256"
     for version in range(5, 12) for kind in ("file", "object")} |
    {"v7_publication_lock_continuity_incident_object_sha256"})
EXACT56_KEYS = frozenset(
    set(V12_REJECTION_KEYS) |
    {"v12_official_rejection_file_sha256",
     "v12_official_rejection_object_sha256"})

EXPECTED_PREPUBLICATION_IDENTITY_COUNT = 106
EXPECTED_TERMINAL_IDENTITY_COUNT = 108
EXPECTED_RUNTIME_GROUP_VECTOR = [10] * 10 + [7, 1]
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MISSING = object()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode("utf-8")


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def read_stable(path: Path) -> tuple[bytes, tuple[int, ...]]:
    flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"not a regular file: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        raw = b"".join(chunks)
        if identity(before) != identity(after) or len(raw) != before.st_size:
            raise ValueError(f"identity changed during held read: {path}")
        return raw, identity(before)
    finally:
        os.close(descriptor)


def decode_json(raw: bytes, label: str) -> tuple[Any, list[str]]:
    duplicates: list[str] = []

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                duplicates.append(key)
            result[key] = value
        return result

    value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs)
    return value, duplicates


def object_closure(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or not isinstance(value.get("object_sha256"), str):
        return {"declared": None, "computed": None, "matches": False}
    work = copy.deepcopy(value)
    declared = work.pop("object_sha256")
    computed = sha_bytes(canonical(work))
    return {"declared": declared, "computed": computed,
            "matches": declared == computed}


class Report:
    def __init__(self) -> None:
        self.checks: list[dict[str, Any]] = []

    def add(self, name: str, passed: bool, **details: Any) -> None:
        row: dict[str, Any] = {"name": name, "passed": bool(passed)}
        if details:
            row["details"] = details
        self.checks.append(row)

    def finish(self, sections: Mapping[str, Any]) -> dict[str, Any]:
        failures = [row["name"] for row in self.checks if not row["passed"]]
        return {
            "schema": "cm2.c79g.v13.independent-read-only-static-review.v1",
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
            "sections": dict(sections),
        }


def module_assignments(tree: ast.Module) -> dict[str, list[ast.AST]]:
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
    if isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Add, ast.Mult, ast.BitOr, ast.Sub)):
        left, right = safe_literal(node.left, env), safe_literal(node.right, env)
        if left is MISSING or right is MISSING:
            return MISSING
        try:
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Sub):
                return left - right
            return left | right
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
            key, value = safe_literal(key_node, env), safe_literal(value_node, env)
            if key is MISSING or value is MISSING:
                return MISSING
            try:
                result[key] = value
            except TypeError:
                return MISSING
        return result
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id in {"tuple", "list", "set", "frozenset"} and
            len(node.args) in {0, 1} and not node.keywords):
        value = safe_literal(node.args[0], env) if node.args else ()
        if value is MISSING:
            return MISSING
        try:
            return {"tuple": tuple, "list": list, "set": set,
                    "frozenset": frozenset}[node.func.id](value)
        except (TypeError, ValueError):
            return MISSING
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "sorted" and len(node.args) == 1 and
            not node.keywords):
        value = safe_literal(node.args[0], env)
        if value is MISSING:
            return MISSING
        try:
            return sorted(value)
        except (TypeError, ValueError):
            return MISSING
    return MISSING


def literal_environment(tree: ast.Module) -> dict[str, Any]:
    assignments = module_assignments(tree)
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


def dict_literal_stats(tree: ast.Module, label: str) -> dict[str, Any]:
    duplicate_rows: list[dict[str, Any]] = []
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        count += 1
        seen: dict[Any, int] = {}
        for index, key_node in enumerate(node.keys):
            if key_node is None:
                continue
            try:
                key = ast.literal_eval(key_node)
                if key in seen:
                    duplicate_rows.append({
                        "source": label, "line": node.lineno,
                        "key": repr(key), "first_index": seen[key],
                        "second_index": index,
                    })
                else:
                    seen[key] = index
            except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                continue
    return {"dict_literal_count": count,
            "duplicate_count": len(duplicate_rows),
            "duplicates": duplicate_rows}


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


def literal_strings(tree: ast.Module) -> set[str]:
    return {
        node.value for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)}


def comparison_has_name_and_set_gate(node: ast.Compare, name: str) -> bool:
    parts = [node.left, *node.comparators]
    has_name = any(
        isinstance(item, ast.Name) and item.id == name
        for part in parts for item in ast.walk(part))
    has_set = any(
        isinstance(item, ast.Call) and isinstance(item.func, ast.Name) and
        item.func.id == "set" and len(item.args) == 1
        for part in parts for item in ast.walk(part))
    return has_name and has_set


def is_len_equals(node: ast.Compare, expected: int) -> ast.AST | None:
    parts = [node.left, *node.comparators]
    for left, right in zip(parts, parts[1:]):
        pairs = ((left, right), (right, left))
        for call, constant in pairs:
            if (isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and
                    call.func.id == "len" and len(call.args) == 1 and
                    not call.keywords and isinstance(constant, ast.Constant) and
                    type(constant.value) is int and constant.value == expected):
                return call.args[0]
    return None


def parent_map(tree: ast.Module) -> dict[ast.AST, ast.AST]:
    result: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            result[child] = node
    return result


def owner_chain(node: ast.AST, parents: Mapping[ast.AST, ast.AST]) -> list[str]:
    names: list[str] = []
    current = node
    while current in parents:
        current = parents[current]
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(current.name)
    return names


def stale_v5_len52_rows(tree: ast.Module, role: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    parents = parent_map(tree)
    all_rows: list[dict[str, Any]] = []
    stale: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        argument = is_len_equals(node, 52)
        if argument is None:
            continue
        owners = owner_chain(node, parents)
        expression = ast.unparse(argument)
        row = {"role": role, "line": node.lineno,
               "len_argument": expression, "owner_chain": owners}
        all_rows.append(row)
        haystack = " ".join([expression, *owners]).lower()
        if "v5" in haystack:
            stale.append(row)
    return all_rows, stale


def exact39_gate_counts(tree: ast.Module) -> dict[str, int]:
    set_gates = sum(
        comparison_has_name_and_set_gate(node, "V5_OFFICIAL_REJECTION_EXACT39_KEYS")
        for node in ast.walk(tree) if isinstance(node, ast.Compare))
    len39 = sum(
        is_len_equals(node, 39) is not None and
        any(isinstance(item, ast.Name) and
            item.id == "V5_OFFICIAL_REJECTION_EXACT39_KEYS"
            for item in ast.walk(node))
        for node in ast.walk(tree) if isinstance(node, ast.Compare))
    return {"set_equality_gate_count": set_gates,
            "derived_len39_gate_count": len39}


def largest_string_key_dict(function: ast.FunctionDef) -> set[str]:
    candidates: list[set[str]] = []
    for node in ast.walk(function):
        if not isinstance(node, ast.Dict) or any(key is None for key in node.keys):
            continue
        keys: set[str] = set()
        valid = True
        for key in node.keys:
            if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
                valid = False
                break
            keys.add(key.value)
        if valid:
            candidates.append(keys)
    return max(candidates, key=len, default=set())


def output_shape_values(tree: ast.Module, env: Mapping[str, Any]) -> list[dict[str, int]]:
    expected_names = {
        "selfIdentity", "independentConsumerProof", "staticFreezeProof",
        "coldLaunchProof", "laterRejection", "producerSourceRegistry",
        "liveRequest", "liveACK", "liveACKCensus",
    }
    rows: list[dict[str, int]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        value = safe_literal(node, env)
        if (isinstance(value, dict) and set(value) == expected_names and
                all(type(item) is int for item in value.values())):
            normalized = dict(value)
            if normalized not in rows:
                rows.append(normalized)
    return rows


def history_census_values(tree: ast.Module) -> dict[str, Any]:
    dictionary_values: list[int] = []
    comparisons: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if (isinstance(key, ast.Constant) and
                        key.value == "append_only_history_unique_file_identity_count" and
                        isinstance(value, ast.Constant) and type(value.value) is int):
                    dictionary_values.append(value.value)
        elif isinstance(node, ast.Compare):
            for number in (98, 106, 108):
                argument = is_len_equals(node, number)
                if argument is not None and "history" in ast.unparse(argument).lower():
                    comparisons.append({"line": node.lineno,
                                        "expression": ast.unparse(argument),
                                        "expected": number})
    return {"dictionary_values": dictionary_values,
            "history_len_comparisons": comparisons}


def launcher_exact10_pins(tree: ast.Module, env: Mapping[str, Any]) -> list[tuple[str, str | None]]:
    candidates: list[ast.Tuple] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if (any(isinstance(target, ast.Name) and target.id == "V12_EXACT10_PINS"
                    for target in targets) and isinstance(node.value, ast.Tuple) and
                    len(node.value.elts) == 10):
                candidates.append(node.value)
    if len(candidates) != 1:
        return []
    rows: list[tuple[str, str | None]] = []
    for row in candidates[0].elts:
        if not isinstance(row, ast.Tuple) or len(row.elts) != 3:
            return []
        file_pin = safe_literal(row.elts[1], env)
        object_pin = safe_literal(row.elts[2], env)
        if not (isinstance(file_pin, str) and HEX64.fullmatch(file_pin)):
            return []
        if object_pin is not None and not (
                isinstance(object_pin, str) and HEX64.fullmatch(object_pin)):
            return []
        rows.append((file_pin, object_pin))
    return rows


def producer_exact10_pins(tree: ast.Module) -> list[tuple[str, str | None]]:
    nodes = module_assignments(tree).get("V12_PUBLISHED_EXACT10_WITNESS", [])
    if len(nodes) != 1 or not isinstance(nodes[0], ast.Tuple) or len(nodes[0].elts) != 10:
        return []
    rows: list[tuple[str, str | None]] = []
    for row in nodes[0].elts:
        if not isinstance(row, ast.Tuple):
            return []
        hashes = [
            item.value for item in ast.walk(row)
            if isinstance(item, ast.Constant) and isinstance(item.value, str) and
            HEX64.fullmatch(item.value)]
        if not hashes:
            return []
        rows.append((hashes[0], hashes[1] if len(hashes) > 1 else None))
    return rows


def consumer_exact10_files(tree: ast.Module, env: Mapping[str, Any]) -> list[str]:
    value = env.get("V12_PUBLISHED_EXACT10_FILE_SHA256_ORDER")
    if not (isinstance(value, tuple) and len(value) == 10 and
            all(isinstance(item, str) and HEX64.fullmatch(item) for item in value)):
        return []
    return list(value)


def path_exists(path: Path) -> bool:
    try:
        os.lstat(path)
    except FileNotFoundError:
        return False
    return True


def target_v13_pyc_paths() -> list[Path]:
    """Return only cache files whose source stem is one of the three targets."""
    if not V13_PYC_DIRECTORY.is_dir():
        return []
    stems = {path.stem for path in V13_PYTHON.values()}
    result: list[Path] = []
    for path in V13_PYC_DIRECTORY.iterdir():
        if not path.name.endswith(".pyc"):
            continue
        if any(path.name == stem + ".pyc" or
               path.name.startswith(stem + ".") for stem in stems):
            result.append(path)
    return sorted(result, key=lambda path: path.name)


def target_v13_pyc_role(path: Path) -> str | None:
    for role, source in V13_PYTHON.items():
        if (path.name == source.stem + ".pyc" or
                path.name.startswith(source.stem + ".")):
            return role
    return None


def decode_pyc_header(raw: bytes) -> dict[str, Any]:
    """Decode the fixed PEP 552 header without loading the code object."""
    if len(raw) < 16:
        return {
            "header_size_required": 16, "observed_file_size": len(raw),
            "header_complete": False,
        }
    flags = int.from_bytes(raw[4:8], "little", signed=False)
    hash_based = bool(flags & 0x01)
    result: dict[str, Any] = {
        "header_size_required": 16,
        "header_complete": True,
        "magic_number_hex": raw[:4].hex(),
        "flags_uint32_le": flags,
        "hash_based": hash_based,
        "checked_hash": bool(flags & 0x02) if hash_based else None,
        "payload_bytes_8_15_hex": raw[8:16].hex(),
    }
    if hash_based:
        result["source_hash_8_hex"] = raw[8:16].hex()
        result["source_timestamp_uint32_le"] = None
        result["source_size_uint32_le"] = None
    else:
        result["source_hash_8_hex"] = None
        result["source_timestamp_uint32_le"] = int.from_bytes(
            raw[8:12], "little", signed=False)
        result["source_size_uint32_le"] = int.from_bytes(
            raw[12:16], "little", signed=False)
    return result


def v13_runtime_surfaces() -> list[Path]:
    explicit_names = [
        f"c79g-v13-candidate-a-{CHECKPOINT}",
        f"c79g-v13-candidate-b-{CHECKPOINT}",
        f"c79g-v13-verification-a-{CHECKPOINT}",
        f"c79g-v13-verification-b-{CHECKPOINT}",
        f"c79g-v13-committed-completion-{CHECKPOINT}",
        f"c79g-v13-rejections-{CHECKPOINT}",
        f".c79g-v13-candidate-stage-a-{CHECKPOINT}",
        f".c79g-v13-candidate-stage-b-{CHECKPOINT}",
        f".c79g-v13-verification-stage-a-{CHECKPOINT}",
        f".c79g-v13-verification-stage-b-{CHECKPOINT}",
        f".c79g-v13-completion-stage-{CHECKPOINT}",
    ]
    result = [RUNTIME / name for name in explicit_names]
    heads = RUNTIME / "cm2-global-authority-heads"
    result.extend([
        heads / f"c79g-v13-{CHECKPOINT}.seal",
        heads / f".c79g-v13-authority-stage-{CHECKPOINT}.seal",
    ])
    if RUNTIME.is_dir():
        result.extend(path for path in RUNTIME.iterdir()
                      if "c79g-v13" in path.name.lower())
    if heads.is_dir():
        result.extend(path for path in heads.iterdir()
                      if "c79g-v13" in path.name.lower())
    return sorted(set(result), key=str)


def incident_helper_review(tree: ast.Module, role: str) -> dict[str, Any]:
    helper_name = "derive_v12_v5_rejection_shape_incident"
    definitions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        node.name == helper_name]
    if len(definitions) != 1:
        return {
            "definition_count": len(definitions), "normalized_ast_sha256": None,
            "direct_callsites": [], "non_direct_loads": ["definition_missing"],
            "matches_expected_callsites": False,
        }
    normalized = ast.dump(
        definitions[0], annotate_fields=True,
        include_attributes=False).encode("utf-8")
    parents = parent_map(tree)
    rows: list[tuple[str | None, str | None, int]] = []
    non_direct: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and
                node.id == helper_name):
            continue
        parent = parents.get(node)
        if not (isinstance(parent, ast.Call) and parent.func is node and
                len(parent.args) == 5 and not parent.keywords):
            non_direct.append({"line": node.lineno,
                               "parent": type(parent).__name__ if parent else None})
            continue
        chain = owner_chain(parent, parents)
        function = next((name for name in chain if name not in {
            "HeldSelf", "HeldInheritedIncidentAuthorityExact10",
            "HeldV12PredecessorExact10"}), None)
        class_name = next((name for name in chain if name in {
            "HeldSelf", "HeldInheritedIncidentAuthorityExact10",
            "HeldV12PredecessorExact10"}), None)
        rows.append((class_name, function, len(parent.args)))
    expected = EXPECTED_INCIDENT_HELPER_CALLSITES[role]
    return {
        "definition_count": 1,
        "normalized_ast_sha256": sha_bytes(normalized),
        "normalized_ast_size": len(normalized),
        "direct_callsites": [list(row) for row in rows],
        "expected_callsites": [list(row) for row in expected],
        "non_direct_loads": non_direct,
        "matches_expected_callsites": rows == expected and not non_direct,
    }


def incident_fd_environment_review(
        tree: ast.Module, env: Mapping[str, Any], role: str,
) -> dict[str, Any]:
    coordination_name = (
        "COLD_COORDINATION_PARENT_FD_ENV" if role == "producer"
        else "COORDINATION_PARENT_FD_ENV")
    control_names = (
        "COLD_EXEC_FD_ENV", "COLD_SOURCE_FD_ENV",
        "COLD_WORKSPACE_ROOT_FD_ENV", coordination_name,
    )
    expected_names = set(control_names) | set(INCIDENT_FD_ENV_NAMES)
    expected_values = {
        name: "CM2_C79G_V13_" + name.removesuffix("_ENV")
        for name in expected_names}
    expected_values[coordination_name] = "CM2_C79G_V13_COORDINATION_PARENT_FD"
    assignments = {
        name: value for name, value in env.items()
        if name.endswith("_FD_ENV") and isinstance(value, str) and
        value.startswith("CM2_C79G_V13_")}
    load_counts = {
        name: sum(
            isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and
            node.id == name for node in ast.walk(tree))
        for name in INCIDENT_FD_ENV_NAMES}
    return {
        "expected_total_fd_env_count": 14,
        "observed_total_fd_env_count": len(assignments),
        "expected_incident_fd_env_count": 10,
        "observed_incident_fd_env_count": sum(
            name in assignments for name in INCIDENT_FD_ENV_NAMES),
        "missing_names": sorted(expected_names - set(assignments)),
        "extra_names": sorted(set(assignments) - expected_names),
        "value_mismatches": {
            name: {"observed": assignments.get(name), "expected": expected}
            for name, expected in expected_values.items()
            if assignments.get(name) != expected},
        "unique_observed_value_count": len(set(assignments.values())),
        "incident_role_load_counts": load_counts,
        "matches": (
            set(assignments) == expected_names and
            assignments == expected_values and len(set(assignments.values())) == 14 and
            all(count >= 1 for count in load_counts.values())),
    }


def launcher_v12_first_review(
        tree: ast.Module, env: Mapping[str, Any],
) -> dict[str, Any]:
    configure = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and
        node.name == "configure_workspace_paths"]
    base7_order: list[str | None] = []
    exact8_order: list[str | None] = []
    if len(configure) == 1:
        for node in configure[0].body:
            if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                    isinstance(node.targets[0], ast.Name)):
                if node.targets[0].id == "BASE7_PINS" and isinstance(node.value, ast.Dict):
                    base7_order = [
                        key.id if isinstance(key, ast.Name) else None
                        for key in node.value.keys]
                if node.targets[0].id == "EXACT8" and isinstance(node.value, ast.Tuple):
                    exact8_order = [
                        item.id if isinstance(item, ast.Name) else None
                        for item in node.value.elts]

    normalizers = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and
        node.name == "pin_normalized_launcher_ast_sha256"]
    normalizer_v11_names = normalizer_v12_names = -1
    normalizer_v11_strings: list[str] = []
    normalizer_v12_strings: list[str] = []
    if len(normalizers) == 1:
        normalizer_v11_names = sum(
            isinstance(node, ast.Name) and node.id == "V11_OFFICIAL_REJECTION"
            for node in ast.walk(normalizers[0]))
        normalizer_v12_names = sum(
            isinstance(node, ast.Name) and node.id == "V12_OFFICIAL_REJECTION"
            for node in ast.walk(normalizers[0]))
        normalizer_v11_strings = [
            node.value for node in ast.walk(normalizers[0])
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and
            "v11" in node.value.lower()]
        normalizer_v12_strings = [
            node.value for node in ast.walk(normalizers[0])
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and
            "v12" in node.value.lower()]

    base_object_orders: list[list[str | None]] = []
    classes = [
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "HeldBundle"]
    if len(classes) == 1:
        initializers = [
            node for node in classes[0].body
            if isinstance(node, ast.FunctionDef) and node.name == "_initialize"]
        if len(initializers) == 1:
            for node in ast.walk(initializers[0]):
                if (isinstance(node, ast.For) and isinstance(node.target, ast.Name) and
                        node.target.id == "path" and isinstance(node.iter, ast.Tuple)):
                    names = [
                        item.id if isinstance(item, ast.Name) else None
                        for item in node.iter.elts]
                    if {"CONTRACT", "TRANSITION", "AUDIT"}.issubset(set(names)):
                        base_object_orders.append(names)

    expected_base7 = [
        "V12_OFFICIAL_REJECTION", "SCHEMA", "CONTRACT", "PRODUCER",
        "CONSUMER", "TRANSITION", "AUDIT"]
    expected_exact8 = [*expected_base7, "SELF"]
    expected_base_objects = [
        "V12_OFFICIAL_REJECTION", "CONTRACT", "TRANSITION", "AUDIT"]
    algorithm = env.get("PIN_NORMALIZED_AST_ALGORITHM")
    matches = (
        base7_order == expected_base7 and exact8_order == expected_exact8 and
        len(normalizers) == 1 and normalizer_v11_names == 0 and
        not normalizer_v11_strings and
        "V12_OFFICIAL_REJECTION" in normalizer_v12_strings and
        isinstance(algorithm, str) and "PRESERVE_V12_REJECTION" in algorithm and
        "V11_REJECTION" not in algorithm and
        base_object_orders == [expected_base_objects])
    return {
        "configured_base7_key_order": base7_order,
        "configured_exact8_order": exact8_order,
        "pin_normalizer_definition_count": len(normalizers),
        "pin_normalizer_v12_symbol_count": normalizer_v12_names,
        "pin_normalizer_v11_symbol_count": normalizer_v11_names,
        "pin_normalizer_v11_string_residuals": normalizer_v11_strings,
        "pin_normalizer_v12_strings": normalizer_v12_strings,
        "pin_normalized_ast_algorithm": algorithm,
        "base_objects_loop_orders": base_object_orders,
        "expected_base_objects_loop_order": expected_base_objects,
        "matches": matches,
    }


def normalized_historical_witness(value: Any) -> list[dict[str, Any]] | None:
    if not isinstance(value, (tuple, list)):
        return None
    exact_keys = {
        "version", "path", "file_sha256", "object_sha256", "key_count",
        "sorted_keys", "sorted_key_array_sha256", "canonical_object_closed",
    }
    rows: list[dict[str, Any]] = []
    for value_row in value:
        if not isinstance(value_row, dict) or set(value_row) != exact_keys:
            return None
        row = dict(value_row)
        if isinstance(row["sorted_keys"], tuple):
            row["sorted_keys"] = list(row["sorted_keys"])
        rows.append(row)
    return rows


def _module_assignment_node(tree: ast.Module, name: str) -> ast.AST | None:
    nodes = module_assignments(tree).get(name, [])
    return nodes[0] if len(nodes) == 1 else None


def historical_witness_builder_review(
        tree: ast.Module, env: Mapping[str, Any], role: str,
        expected_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Rebuild the nine historical rows without invoking source code.

    The source-level witness is deliberately initialized with a function call,
    so it cannot be accepted from ``literal_environment``.  Authority here is
    the literal BASE/STEP graph plus the AST shape of the sole builder.
    """
    base = env.get("HISTORICAL_REJECTION_BASE_EXACT37_KEYS")
    steps = env.get("HISTORICAL_REJECTION_KEYSET_STEPS")
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    expected_versions = [3, 5, 6, 7, 8, 9, 10, 11, 12]
    expected_counts = [37, 39, 41, 43, 46, 48, 50, 52, 54]
    if not isinstance(base, (set, frozenset)):
        errors.append("BASE_NOT_STATIC_SET")
        keys: set[str] = set()
    else:
        keys = set(base)
        if len(keys) != 37 or not all(isinstance(item, str) for item in keys):
            errors.append("BASE_NOT_EXACT37_STRING_KEYS")
    if not isinstance(steps, tuple) or len(steps) != 9:
        errors.append("STEPS_NOT_EXACT9_STATIC_TUPLE")
        step_values: tuple[Any, ...] = ()
    else:
        step_values = steps
    for index, step in enumerate(step_values):
        if not isinstance(step, tuple) or len(step) != 5:
            errors.append(f"STEP_{index}_NOT_EXACT5")
            continue
        version, additions, file_pin, object_pin, keyset_digest = step
        if version != expected_versions[index]:
            errors.append(f"STEP_{index}_VERSION")
        if not isinstance(additions, (set, frozenset)) or not all(
                isinstance(item, str) for item in additions):
            errors.append(f"STEP_{index}_ADDITIONS")
            additions = frozenset()
        if not (isinstance(file_pin, str) and HEX64.fullmatch(file_pin)):
            errors.append(f"STEP_{index}_FILE_PIN")
        if not (isinstance(object_pin, str) and HEX64.fullmatch(object_pin)):
            errors.append(f"STEP_{index}_OBJECT_PIN")
        if not (isinstance(keyset_digest, str) and HEX64.fullmatch(keyset_digest)):
            errors.append(f"STEP_{index}_KEYSET_DIGEST")
        keys |= set(additions)
        sorted_keys = sorted(keys)
        computed_digest = sha_bytes(canonical(sorted_keys))
        if len(sorted_keys) != expected_counts[index]:
            errors.append(f"STEP_{index}_COUNT")
        if computed_digest != keyset_digest:
            errors.append(f"STEP_{index}_DIGEST")
        version_label = f"v{version}"
        rows.append({
            "version": version_label,
            "path": (
                f".cm2-runtime/c79g-{version_label}-rejections-{CHECKPOINT}/"
                "rejection.json"),
            "file_sha256": file_pin,
            "object_sha256": object_pin,
            "key_count": len(sorted_keys),
            "sorted_keys": sorted_keys,
            "sorted_key_array_sha256": keyset_digest,
            "canonical_object_closed": True,
        })

    definitions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and
        node.name == "_build_historical_rejection_exact_keyset_witness"]
    structure: dict[str, Any] = {"definition_count": len(definitions)}
    structure_ok = len(definitions) == 1
    if len(definitions) == 1:
        function = definitions[0]
        normalized = ast.dump(
            function, annotate_fields=True,
            include_attributes=False).encode("utf-8")
        for_nodes = [node for node in ast.walk(function) if isinstance(node, ast.For)]
        exact_for = [
            node for node in for_nodes
            if isinstance(node.target, ast.Tuple) and
            [item.id if isinstance(item, ast.Name) else None
             for item in node.target.elts] == [
                 "version", "additions", "file_pin", "object_pin",
                 "keyset_digest"] and
            isinstance(node.iter, ast.Name) and
            node.iter.id == "HISTORICAL_REJECTION_KEYSET_STEPS"]
        union_updates = [
            node for node in ast.walk(function)
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name) and
            node.targets[0].id == "keys" and
            isinstance(node.value, ast.BinOp) and
            isinstance(node.value.op, ast.BitOr) and
            isinstance(node.value.left, ast.Name) and node.value.left.id == "keys" and
            isinstance(node.value.right, ast.Name) and
            node.value.right.id == "additions"]
        sorted_updates = [
            node for node in ast.walk(function)
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name) and
            node.targets[0].id == "sorted_keys" and
            isinstance(node.value, ast.Call) and
            isinstance(node.value.func, ast.Name) and
            node.value.func.id == "sorted" and len(node.value.args) == 1 and
            isinstance(node.value.args[0], ast.Name) and
            node.value.args[0].id == "keys"]
        append_dicts = [
            node.args[0] for node in ast.walk(function)
            if isinstance(node, ast.Call) and
            isinstance(node.func, ast.Attribute) and
            isinstance(node.func.value, ast.Name) and
            node.func.value.id == "rows" and node.func.attr == "append" and
            len(node.args) == 1 and isinstance(node.args[0], ast.Dict)]
        expected_row_keys = {
            "version", "path", "file_sha256", "object_sha256", "key_count",
            "sorted_keys", "sorted_key_array_sha256",
            "canonical_object_closed"}
        append_keysets = [
            {key.value for key in node.keys
             if isinstance(key, ast.Constant) and isinstance(key.value, str)}
            for node in append_dicts]
        returns = [node for node in ast.walk(function) if isinstance(node, ast.Return)]
        return_tuple_rows = (
            len(returns) == 1 and isinstance(returns[0].value, ast.Call) and
            isinstance(returns[0].value.func, ast.Name) and
            returns[0].value.func.id == "tuple" and
            len(returns[0].value.args) == 1 and
            isinstance(returns[0].value.args[0], ast.Name) and
            returns[0].value.args[0].id == "rows")
        structure.update({
            "normalized_ast_sha256": sha_bytes(normalized),
            "for_step_loop_count": len(exact_for),
            "key_union_update_count": len(union_updates),
            "sorted_key_update_count": len(sorted_updates),
            "row_append_keysets": [sorted(value) for value in append_keysets],
            "returns_tuple_rows": return_tuple_rows,
        })
        structure_ok &= (
            len(exact_for) == 1 and len(union_updates) == 1 and
            len(sorted_updates) == 1 and append_keysets == [expected_row_keys] and
            return_tuple_rows)
    witness_assignment = _module_assignment_node(
        tree, "HISTORICAL_REJECTION_EXACT_KEYSET_WITNESS")
    assignment_is_builder_call = (
        isinstance(witness_assignment, ast.Call) and
        isinstance(witness_assignment.func, ast.Name) and
        witness_assignment.func.id ==
            "_build_historical_rejection_exact_keyset_witness" and
        not witness_assignment.args and not witness_assignment.keywords)
    materialized_assignment = normalized_historical_witness(
        safe_literal(witness_assignment, env))
    assignment_is_exact_materialization = materialized_assignment == rows
    structure["module_assignment_is_exact_zero_argument_builder_call"] = \
        assignment_is_builder_call
    structure["module_assignment_is_exact_static_materialization"] = \
        assignment_is_exact_materialization
    structure["module_assignment_mode"] = (
        "BUILDER_CALL" if assignment_is_builder_call else
        "STATIC_MATERIALIZATION" if assignment_is_exact_materialization else
        "INVALID")
    structure_ok &= assignment_is_builder_call or assignment_is_exact_materialization
    return {
        "role": role,
        "base_key_count": len(base) if isinstance(base, (set, frozenset)) else None,
        "step_count": len(steps) if isinstance(steps, tuple) else None,
        "reconstructed_rows": rows,
        "errors": errors,
        "builder_structure": structure,
        "matches_external_expected_rows": rows == expected_rows,
        "matches": not errors and structure_ok and rows == expected_rows,
    }


def _statement_successors(tree: ast.Module) -> dict[ast.stmt, ast.stmt]:
    successors: dict[ast.stmt, ast.stmt] = {}
    for owner in ast.walk(tree):
        for _, value in ast.iter_fields(owner):
            if not isinstance(value, list):
                continue
            statements = [item for item in value if isinstance(item, ast.stmt)]
            for left, right in zip(statements, statements[1:]):
                successors[left] = right
    return successors


def _containing_statement(
        node: ast.AST, parents: Mapping[ast.AST, ast.AST],
) -> ast.stmt | None:
    current = node
    while current in parents:
        current = parents[current]
        if isinstance(current, ast.stmt):
            return current
    return None


def published_v11_v12_adjacency_review(
        tree: ast.Module, role: str,
) -> dict[str, Any]:
    """Require every exact v11 proof surface to be immediately extended by v12."""
    v11 = "published_then_officially_rejected_predecessor_v11"
    v12 = "published_then_officially_rejected_predecessor_v12"
    parents = parent_map(tree)
    successors = _statement_successors(tree)
    occurrences = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and node.value == v11]
    v12_occurrences = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and node.value == v12]
    rows: list[dict[str, Any]] = []
    for occurrence in sorted(occurrences, key=lambda item: (item.lineno, item.col_offset)):
        direct_dict: ast.Dict | None = None
        parent = parents.get(occurrence)
        if isinstance(parent, ast.Dict) and occurrence in parent.keys:
            direct_dict = parent
        passed = False
        context = "statement"
        next_value: str | None = None
        if direct_dict is not None:
            context = "dict-key"
            index = direct_dict.keys.index(occurrence)
            if index + 1 < len(direct_dict.keys):
                next_key = direct_dict.keys[index + 1]
                if isinstance(next_key, ast.Constant) and isinstance(next_key.value, str):
                    next_value = next_key.value
            passed = next_value == v12
        else:
            statement = _containing_statement(occurrence, parents)
            relevant: list[ast.Constant] = []
            if statement is not None:
                relevant = sorted([
                    item for item in ast.walk(statement)
                    if isinstance(item, ast.Constant) and item.value in {v11, v12}
                ], key=lambda item: (item.lineno, item.col_offset))
            try:
                index = relevant.index(occurrence)
            except ValueError:
                index = -1
            if index >= 0 and index + 1 < len(relevant):
                next_value = relevant[index + 1].value
            elif statement is not None and statement in successors:
                following = sorted([
                    item for item in ast.walk(successors[statement])
                    if isinstance(item, ast.Constant) and item.value in {v11, v12}
                ], key=lambda item: (item.lineno, item.col_offset))
                if following:
                    next_value = following[0].value
                    context = "next-statement"
            passed = next_value == v12
        rows.append({
            "role": role, "line": occurrence.lineno, "context": context,
            "next_published_predecessor_key": next_value, "passes": passed,
        })
    return {
        "v11_occurrence_count": len(occurrences),
        "v12_occurrence_count": len(v12_occurrences),
        "occurrence_rows": rows,
        "failed_rows": [row for row in rows if not row["passes"]],
        "matches": bool(occurrences) and bool(v12_occurrences) and
            all(row["passes"] for row in rows),
    }


def _functions_named(tree: ast.Module, name: str) -> list[ast.FunctionDef]:
    return [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name]


def _literal_string_keyset(node: ast.AST) -> set[str] | None:
    if not isinstance(node, (ast.Set, ast.Tuple, ast.List)):
        return None
    values: set[str] = set()
    for item in node.elts:
        if not (isinstance(item, ast.Constant) and isinstance(item.value, str)):
            return None
        values.add(item.value)
    return values


def consumer_static_freeze_v12_review(tree: ast.Module) -> dict[str, Any]:
    functions = _functions_named(tree, "static_freeze_proof")
    if len(functions) != 1:
        return {"definition_count": len(functions), "matches": False}
    function = functions[0]
    required_transition_key = \
        "published_then_officially_rejected_predecessor_v12"
    transition_keysets: list[dict[str, Any]] = []
    for node in ast.walk(function):
        keyset = _literal_string_keyset(node)
        if keyset is None or "transition_kind" not in keyset or \
                "successor_v13_static_bundle" not in keyset:
            continue
        transition_keysets.append({
            "line": node.lineno, "key_count": len(keyset),
            "has_v11": "published_then_officially_rejected_predecessor_v11" in keyset,
            "has_v12": required_transition_key in keyset,
        })
    desired_kind = (
        "APPEND_ONLY_PUBLISHED_THEN_OFFICIALLY_REJECTED_V12_TO_"
        "ZERO_CREDIT_V13_STATIC_SUCCESSOR")
    stale_kind = (
        "APPEND_ONLY_PUBLISHED_THEN_OFFICIALLY_REJECTED_V11_TO_"
        "ZERO_CREDIT_V13_STATIC_SUCCESSOR")
    function_strings = literal_strings(function)  # type: ignore[arg-type]
    exact8_first_expressions: list[str] = []
    for node in ast.walk(function):
        if not isinstance(node, ast.Assign) or not any(
                isinstance(target, ast.Name) and target.id == "exact8_stats"
                for target in node.targets):
            continue
        if isinstance(node.value, (ast.List, ast.Tuple)) and node.value.elts:
            exact8_first_expressions.append(ast.unparse(node.value.elts[0]))
    policy_functions = _functions_named(tree, "_static_policy_guards")
    policy_rows: list[dict[str, Any]] = []
    for policy in policy_functions:
        names = {
            node.id for node in ast.walk(policy) if isinstance(node, ast.Name)}
        policy_rows.append({
            "line": policy.lineno,
            "has_v12_official_rejection": "V12_OFFICIAL_REJECTION" in names,
            "has_v12_to_v13_transition": "V12_TO_V13_TRANSITION" in names,
        })
    transition_shape_ok = (
        len(transition_keysets) == 1 and transition_keysets[0]["has_v11"] and
        transition_keysets[0]["has_v12"])
    exact8_first_ok = (
        exact8_first_expressions and
        all("V12_OFFICIAL_REJECTION" in value and
            "V11_OFFICIAL_REJECTION" not in value
            for value in exact8_first_expressions))
    policy_ok = (
        len(policy_rows) == 1 and
        policy_rows[0]["has_v12_official_rejection"] and
        policy_rows[0]["has_v12_to_v13_transition"])
    return {
        "definition_count": 1,
        "transition_top_level_keysets": transition_keysets,
        "desired_transition_kind_present": desired_kind in function_strings,
        "stale_v11_transition_kind_present": stale_kind in function_strings,
        "exact8_first_expressions": exact8_first_expressions,
        "static_policy_guard_rows": policy_rows,
        "matches": (
            transition_shape_ok and desired_kind in function_strings and
            stale_kind not in function_strings and exact8_first_ok and policy_ok),
    }


def _terminal_call_version(node: ast.Call, role: str) -> int | None:
    if role == "consumer" and isinstance(node.func, ast.Name):
        if node.func.id == "terminal_replay_v11_published_exact10":
            return 11
        if node.func.id == "terminal_replay_v12_published_exact10":
            return 12
    if role == "launcher" and isinstance(node.func, ast.Attribute) and \
            node.func.attr == "terminal_replay":
        value = node.func.value
        if (isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name) and
                value.value.id == "self"):
            if value.attr == "predecessor_v11":
                return 11
            if value.attr == "predecessor_v12":
                return 12
    return None


def terminal_replay_v11_then_v12_review(
        trees: Mapping[str, ast.Module],
) -> dict[str, Any]:
    role_rows: dict[str, Any] = {}
    all_pairs_ok = True
    for role in ("consumer", "launcher"):
        tree = trees.get(role)
        if tree is None:
            role_rows[role] = {"source_missing": True, "matches": False}
            all_pairs_ok = False
            continue
        parents = parent_map(tree)
        calls_by_function: dict[ast.FunctionDef, list[tuple[int, ast.Call]]] = {}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            version = _terminal_call_version(node, role)
            if version is None:
                continue
            current: ast.AST = node
            owner: ast.FunctionDef | None = None
            while current in parents:
                current = parents[current]
                if isinstance(current, ast.FunctionDef):
                    owner = current
                    break
            if owner is not None:
                calls_by_function.setdefault(owner, []).append((version, node))
        pairs: list[dict[str, Any]] = []
        for function, calls in calls_by_function.items():
            ordered = sorted(calls, key=lambda row: (row[1].lineno, row[1].col_offset))
            for index, (version, call) in enumerate(ordered):
                if version != 11:
                    continue
                next_version = ordered[index + 1][0] if index + 1 < len(ordered) else None
                next_line = ordered[index + 1][1].lineno if index + 1 < len(ordered) else None
                row = {
                    "function": function.name, "v11_line": call.lineno,
                    "next_historical_replay_version": next_version,
                    "next_historical_replay_line": next_line,
                    "passes": next_version == 12,
                }
                pairs.append(row)
        v11_count = sum(len([1 for version, _ in calls if version == 11])
                        for calls in calls_by_function.values())
        v12_count = sum(len([1 for version, _ in calls if version == 12])
                        for calls in calls_by_function.values())
        definition_ok = True
        if role == "consumer":
            definition_ok = (
                len(_functions_named(tree, "terminal_replay_v11_published_exact10")) == 1 and
                len(_functions_named(tree, "terminal_replay_v12_published_exact10")) == 1)
        role_ok = bool(pairs) and definition_ok and all(row["passes"] for row in pairs)
        role_rows[role] = {
            "v11_call_count": v11_count, "v12_call_count": v12_count,
            "consumer_both_replay_definitions_exist": definition_ok,
            "pair_rows": pairs, "matches": role_ok,
        }
        all_pairs_ok &= role_ok

    authorize_rows: list[dict[str, Any]] = []
    launcher = trees.get("launcher")
    if launcher is not None:
        launcher_parents = parent_map(launcher)
        for function in _functions_named(launcher, "run_authorize_child"):
            replay_lines: list[int] = []
            for node in ast.walk(function):
                if not (isinstance(node, ast.Call) and
                        isinstance(node.func, ast.Attribute) and
                        isinstance(node.func.value, ast.Name) and
                        node.func.value.id == "bundle" and
                        node.func.attr == "terminal_replay"):
                    continue
                current: ast.AST = node
                nearest: ast.FunctionDef | None = None
                while current in launcher_parents:
                    current = launcher_parents[current]
                    if isinstance(current, ast.FunctionDef):
                        nearest = current
                        break
                if nearest is function:
                    replay_lines.append(node.lineno)
            request_lines = [
                node.lineno for node in ast.walk(function)
                if isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == "request"
                    for target in node.targets)]
            authorize_rows.append({
                "function": function.name, "bundle_terminal_replay_lines": replay_lines,
                "live_request_assignment_lines": request_lines,
                "passes": bool(replay_lines) and len(request_lines) == 1 and
                    max(replay_lines) < request_lines[0],
            })
    authorize_ok = len(authorize_rows) == 1 and authorize_rows[0]["passes"]
    return {
        "roles": role_rows,
        "authorize_request_order": authorize_rows,
        "matches": all_pairs_ok and authorize_ok,
    }


def _expression_keyset(
        node: ast.AST, known: Mapping[str, set[str]],
        attribute_known: Mapping[str, set[str]] | None = None,
) -> tuple[set[str], list[str]]:
    attribute_known = attribute_known or {}
    rendered = ast.unparse(node)
    if rendered in attribute_known:
        return set(attribute_known[rendered]), []
    if isinstance(node, ast.Dict):
        keys: set[str] = set()
        unresolved: list[str] = []
        for key, value in zip(node.keys, node.values):
            if key is None:
                unpacked, missing = _expression_keyset(value, known, attribute_known)
                keys |= unpacked
                unresolved.extend(missing)
            elif isinstance(key, ast.Constant) and isinstance(key.value, str):
                keys.add(key.value)
            else:
                unresolved.append("DYNAMIC_KEY:" + ast.unparse(key))
        return keys, unresolved
    if isinstance(node, ast.Name):
        if node.id in known:
            return set(known[node.id]), []
        return set(), ["UNKNOWN_NAME:" + node.id]
    if isinstance(node, ast.Attribute):
        name = ast.unparse(node)
        if name in attribute_known:
            return set(attribute_known[name]), []
        return set(), ["UNKNOWN_ATTRIBUTE:" + name]
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "dict" and len(node.args) == 1 and not node.keywords):
        return _expression_keyset(node.args[0], known, attribute_known)
    return set(), ["UNSUPPORTED_UNPACK:" + ast.unparse(node)]


def _unwrap_close_object(node: ast.AST) -> tuple[ast.AST, bool]:
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
            node.func.id == "close_object" and len(node.args) == 1 and
            not node.keywords):
        return node.args[0], True
    return node, False


def _function_keyset(
        tree: ast.Module, function_name: str, *, target_name: str | None = None,
        attribute_known: Mapping[str, set[str]] | None = None,
) -> dict[str, Any]:
    functions = _functions_named(tree, function_name)
    if len(functions) != 1:
        return {"definition_count": len(functions), "keys": [],
                "unresolved": ["FUNCTION_COUNT"], "closed": False}
    function = functions[0]
    known: dict[str, set[str]] = {}
    assignments: list[tuple[str, ast.AST]] = []
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and \
                isinstance(node.targets[0], ast.Name):
            assignments.append((node.targets[0].id, node.value))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assignments.append((node.target.id, node.value))
    for _ in range(max(2, len(assignments))):
        changed = False
        for name, value in assignments:
            if name in known:
                continue
            rendered = ast.unparse(value)
            if attribute_known and rendered in attribute_known:
                known[name] = set(attribute_known[rendered])
                changed = True
                continue
            if (attribute_known and isinstance(value, ast.Call) and
                    isinstance(value.func, ast.Name) and
                    "CALL:" + value.func.id in attribute_known):
                known[name] = set(attribute_known["CALL:" + value.func.id])
                changed = True
                continue
            body, closed = _unwrap_close_object(value)
            if not isinstance(body, ast.Dict):
                continue
            keys, unresolved = _expression_keyset(body, known, attribute_known)
            if unresolved:
                continue
            if closed:
                keys.add("object_sha256")
            known[name] = keys
            changed = True
        if not changed:
            break

    candidates: list[tuple[int, ast.AST]] = []
    if target_name is not None:
        for node in ast.walk(function):
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if any(isinstance(target, ast.Name) and target.id == target_name
                       for target in targets):
                    candidates.append((node.lineno, node.value))
    else:
        candidates = [
            (node.lineno, node.value) for node in ast.walk(function)
            if isinstance(node, ast.Return) and node.value is not None]
    rows: list[dict[str, Any]] = []
    for line, value in candidates:
        body, closed = _unwrap_close_object(value)
        keys, unresolved = _expression_keyset(body, known, attribute_known)
        if closed:
            keys.add("object_sha256")
        rows.append({
            "line": line, "key_count": len(keys), "keys": sorted(keys),
            "unresolved": unresolved, "closed_by_close_object": closed,
        })
    usable = [row for row in rows if not row["unresolved"]]
    selected = max(usable, key=lambda row: row["key_count"], default=None)
    return {
        "definition_count": 1, "candidate_rows": rows,
        "line": selected["line"] if selected else None,
        "key_count": selected["key_count"] if selected else None,
        "keys": selected["keys"] if selected else [],
        "unresolved": selected["unresolved"] if selected else ["NO_USABLE_CANDIDATE"],
        "closed": selected["closed_by_close_object"] if selected else False,
    }


def registry_v12_authority_review(
        trees: Mapping[str, ast.Module],
) -> dict[str, Any]:
    required_registry = {
        "published_then_officially_rejected_predecessor_v12",
        "v12_official_rejection_file_sha256",
        "v12_official_rejection_object_sha256",
        "v12_v5_rejection_shape_incident",
    }
    rows: dict[str, Any] = {}
    producer = trees.get("producer")
    if producer is not None:
        execution_keys = set(_function_keyset(
            producer, "execution_proof").get("keys", []))
        row = _function_keyset(
            producer, "input_registry",
            attribute_known={"self_guard.execution_proof()": execution_keys})
        keys = set(row.get("keys", []))
        row["required_v12_authority_keys"] = sorted(required_registry)
        row["missing_v12_authority_keys"] = sorted(required_registry - keys)
        row["matches"] = not row["missing_v12_authority_keys"]
        rows["producer_input_registry"] = row
    consumer = trees.get("consumer")
    if consumer is not None:
        candidates: list[dict[str, Any]] = []
        for node in ast.walk(consumer):
            keyset = _literal_string_keyset(node)
            if keyset is None or "producer_file_sha256" not in keyset or \
                    "published_then_officially_rejected_predecessor_v11" not in keyset:
                continue
            candidates.append({"line": node.lineno, "keys": sorted(keyset),
                               "key_count": len(keyset)})
        candidate = max(candidates, key=lambda row: row["key_count"], default=None)
        keys = set(candidate["keys"]) if candidate else set()
        rows["consumer_registry_exact_set_gate"] = {
            "candidate_count": len(candidates), "selected": candidate,
            "required_v12_authority_keys": sorted(required_registry),
            "missing_v12_authority_keys": sorted(required_registry - keys),
            "matches": candidate is not None and not (required_registry - keys),
        }
    launcher = trees.get("launcher")
    if launcher is not None:
        chronology = _function_keyset(
            launcher, "cold_publication_chronology").get("keys", [])
        proof = _function_keyset(
            launcher, "cold_root", target_name="proof",
            attribute_known={"bundle.chronology": set(chronology)})
        proof_keys = set(proof.get("keys", []))
        proof["required_v12_authority_keys"] = sorted(required_registry)
        proof["missing_v12_authority_keys"] = sorted(required_registry - proof_keys)
        proof["matches"] = not proof["unresolved"] and not \
            proof["missing_v12_authority_keys"]
        rows["launcher_cold_launch_proof"] = proof
        authority_required = {
            "v12_official_rejection_file_sha256",
            "v12_official_rejection_object_sha256",
            "trusted_v12_v5_rejection_shape_incident_digest",
        }
        authority_candidates: list[dict[str, Any]] = []
        for node in ast.walk(next(iter(_functions_named(launcher, "cold_root")), launcher)):
            if not isinstance(node, ast.Dict):
                continue
            keys, unresolved = _expression_keyset(node, {}, {})
            if "authority_root_sha256" in ast.unparse(
                    parent_map(launcher).get(node, node)) or \
                    "trusted_v11_dual_validator_divergence_incident_digest" in keys:
                authority_candidates.append({
                    "line": node.lineno, "keys": sorted(keys),
                    "unresolved": unresolved, "key_count": len(keys)})
        authority = max(
            authority_candidates, key=lambda row: row["key_count"], default=None)
        authority_keys = set(authority["keys"]) if authority else set()
        rows["launcher_authority_root_domain"] = {
            "candidate_count": len(authority_candidates), "selected": authority,
            "required_v12_authority_keys": sorted(authority_required),
            "missing_v12_authority_keys": sorted(authority_required - authority_keys),
            "matches": authority is not None and not (authority_required - authority_keys),
        }
    return {"roles": rows,
            "matches": len(rows) == 4 and all(row.get("matches") for row in rows.values())}


STATIC_AUDIT_V11_BASE_INPUT_ORDER = (
    "schema", "contract_file", "contract_object", "producer", "consumer",
    "transition_file", "transition_object", "launcher_template",
    "v4_supersession_file", "v4_supersession_object",
    "v5_rejection_file", "v5_rejection_object",
    "v6_rejection_file", "v6_rejection_object",
    "v7_rejection_file", "v7_rejection_object",
    "v7_lock_continuity_incident_object",
    "v8_rejection_file", "v8_rejection_object", "v8_launcher_file",
    "v8_launcher_regression_defect_sha256",
    "trusted_v8_rollout_control_flow_incident_digest",
    "v9_rejection_file", "v9_rejection_object", "v9_launcher_file",
    "v9_persisted_v6_proof_sha256", "v9_expanded_v6_proof_sha256",
    "trusted_v9_proof_shape_drift_incident_digest",
    "v10_rejection_file", "v10_rejection_object", "v10_producer_file",
    "trusted_v10_regression_label_prefix_incident_digest",
    "v11_rejection_file", "v11_rejection_object", "v11_producer_file",
    "v11_launcher_file",
    "trusted_v11_dual_validator_divergence_incident_digest",
)
STATIC_AUDIT_V12_INPUT_SUFFIX = (
    "v12_rejection_file", "v12_rejection_object", "v12_producer_file",
    "v12_consumer_file", "v12_launcher_file",
    "trusted_v12_v5_rejection_shape_incident_digest",
)
EXPECTED_STATIC_AUDIT_V13_INPUT_ORDER = (
    *STATIC_AUDIT_V11_BASE_INPUT_ORDER, *STATIC_AUDIT_V12_INPUT_SUFFIX)


def static_audit_input_v12_extension_review(
        source_envs: Mapping[str, Mapping[str, Any]],
        builder_env: Mapping[str, Any],
) -> dict[str, Any]:
    names = {
        "producer": "STATIC_AUDIT_INPUT_KEY_ORDER",
        "consumer": "STATIC_AUDIT_INPUT_EXACT37",
        "launcher": "FINAL_STATIC_AUDIT_INPUT_KEY_ORDER",
        "builder": "STATIC_AUDIT_INPUT_KEY_ORDER",
    }
    environments: dict[str, Mapping[str, Any]] = dict(source_envs)
    environments["builder"] = builder_env
    expected_digest = sha_bytes(canonical(list(EXPECTED_STATIC_AUDIT_V13_INPUT_ORDER)))
    rows: dict[str, Any] = {}
    for role, name in names.items():
        value = environments.get(role, {}).get(name)
        observed = list(value) if isinstance(value, tuple) else None
        digest_names = [
            key for key in environments.get(role, {})
            if "STATIC_AUDIT_INPUT" in key and "SHA256" in key]
        declared_digests = {
            key: environments[role].get(key) for key in digest_names}
        rows[role] = {
            "assignment_name": name,
            "observed_count": len(value) if isinstance(value, tuple) else None,
            "observed_order": observed,
            "observed_suffix": observed[-len(STATIC_AUDIT_V12_INPUT_SUFFIX):]
                if observed is not None and len(observed) >= len(STATIC_AUDIT_V12_INPUT_SUFFIX)
                else None,
            "declared_digest_values": declared_digests,
            "computed_order_sha256": sha_bytes(canonical(observed))
                if observed is not None else None,
            "matches": (
                value == EXPECTED_STATIC_AUDIT_V13_INPUT_ORDER and
                (not declared_digests or
                 set(declared_digests.values()) == {expected_digest})),
        }
    return {
        "expected_count": len(EXPECTED_STATIC_AUDIT_V13_INPUT_ORDER),
        "expected_v12_suffix": list(STATIC_AUDIT_V12_INPUT_SUFFIX),
        "expected_order_sha256": expected_digest,
        "roles": rows,
        "matches": len(rows) == 4 and all(row["matches"] for row in rows.values()),
    }


def history_identity_semantics_review(
        trees: Mapping[str, ast.Module],
) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for role, tree in trees.items():
        number_rows = [
            {"line": node.lineno, "value": node.value,
             "owners": owner_chain(node, parent_map(tree))}
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and type(node.value) is int and
            node.value in {98, 106, 108}]
        rows[role] = {"identity_number_literals": number_rows}

    launcher = trees.get("launcher")
    vector_rows: list[dict[str, Any]] = []
    terminal108_rows: list[dict[str, Any]] = []
    if launcher is not None:
        for node in ast.walk(launcher):
            if isinstance(node, ast.Compare):
                argument = is_len_equals(node, 108)
                if argument is not None and "identit" in ast.unparse(argument).lower():
                    terminal108_rows.append({
                        "line": node.lineno, "expression": ast.unparse(argument)})
                for expression in [node.left, *node.comparators]:
                    value = safe_literal(expression, {})
                    if value == EXPECTED_RUNTIME_GROUP_VECTOR:
                        vector_rows.append({
                            "line": node.lineno,
                            "expression": ast.unparse(expression),
                            "vector": value,
                        })
    consumer = trees.get("consumer")
    predecessor98_rows: list[dict[str, Any]] = []
    terminal_union108_rows: list[dict[str, Any]] = []
    if consumer is not None:
        for node in ast.walk(consumer):
            if not isinstance(node, ast.Compare):
                continue
            argument98 = is_len_equals(node, 98)
            if argument98 is not None and "predecessor" in ast.unparse(argument98).lower():
                predecessor98_rows.append({
                    "line": node.lineno, "expression": ast.unparse(argument98)})
            argument108 = is_len_equals(node, 108)
            if argument108 is not None and "identit" in ast.unparse(argument108).lower():
                terminal_union108_rows.append({
                    "line": node.lineno, "expression": ast.unparse(argument108)})
    producer = trees.get("producer")
    producer108_rows: list[dict[str, Any]] = []
    if producer is not None:
        for node in ast.walk(producer):
            if not isinstance(node, ast.Compare):
                continue
            argument = is_len_equals(node, 108)
            if argument is not None and "guard" in ast.unparse(argument).lower():
                producer108_rows.append({
                    "line": node.lineno, "expression": ast.unparse(argument)})

    vector = vector_rows[0]["vector"] if len(vector_rows) == 1 else []
    derived = {
        "predecessor_identity_count": sum(vector[1:]) if vector else None,
        "prepublication_identity_count": sum(vector) - 2 if vector else None,
        "terminal_identity_count": sum(vector) if vector else None,
    }
    matches = (
        len(vector_rows) == 1 and vector == EXPECTED_RUNTIME_GROUP_VECTOR and
        derived == {
            "predecessor_identity_count": 98,
            "prepublication_identity_count": EXPECTED_PREPUBLICATION_IDENTITY_COUNT,
            "terminal_identity_count": EXPECTED_TERMINAL_IDENTITY_COUNT,
        } and
        bool(predecessor98_rows) and bool(terminal_union108_rows) and
        bool(producer108_rows) and bool(terminal108_rows))
    return {
        "source_number_occurrences": rows,
        "launcher_runtime_group_vector_rows": vector_rows,
        "launcher_terminal108_rows": terminal108_rows,
        "consumer_predecessor98_rows": predecessor98_rows,
        "consumer_terminal_union108_rows": terminal_union108_rows,
        "producer_terminal108_rows": producer108_rows,
        "mechanically_derived_from_runtime_group_vector": derived,
        "matches": matches,
    }


EXPECTED_OUTPUT_SHAPES = {
    "selfIdentity": 33,
    "independentConsumerProof": 59,
    "staticFreezeProof": 75,
    "coldLaunchProof": 108,
    "laterRejection": 56,
    "producerSourceRegistry": 70,
    "liveRequest": 15,
    "liveACK": 32,
    "liveACKCensus": 42,
}


def output_shape_constructor_review(
        trees: Mapping[str, ast.Module],
        envs: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    consumer = trees.get("consumer")
    producer = trees.get("producer")
    launcher = trees.get("launcher")
    constructor_rows: dict[str, Any] = {}
    if consumer is not None:
        consumer_chronology_keys = set(_function_keyset(
            consumer, "cold_publication_chronology").get("keys", []))
        constructor_rows["selfIdentity"] = _function_keyset(
            consumer, "_self_identity")
        constructor_rows["independentConsumerProof"] = _function_keyset(
            consumer, "independent_consumer_proof")
        constructor_rows["staticFreezeProof"] = _function_keyset(
            consumer, "static_freeze_proof",
            attribute_known={
                "CALL:cold_publication_chronology": consumer_chronology_keys})
        constructor_rows["liveACK"] = _function_keyset(
            consumer, "cold_authorize_live_protocol", target_name="ack")
        census_candidates: list[dict[str, Any]] = []
        protocol_functions = _functions_named(consumer, "cold_authorize_live_protocol")
        if len(protocol_functions) == 1:
            for node in ast.walk(protocol_functions[0]):
                if not isinstance(node, ast.Dict):
                    continue
                for key, value in zip(node.keys, node.values):
                    if (isinstance(key, ast.Constant) and
                            key.value == "final_dynamic_replay_census" and
                            isinstance(value, ast.Dict)):
                        keys, unresolved = _expression_keyset(value, {}, {})
                        census_candidates.append({
                            "line": value.lineno, "key_count": len(keys),
                            "keys": sorted(keys), "unresolved": unresolved,
                            "closed_by_close_object": False,
                        })
        census_selected = max(
            [row for row in census_candidates if not row["unresolved"]],
            key=lambda row: row["key_count"], default=None)
        constructor_rows["liveACKCensus"] = {
            "definition_count": len(protocol_functions),
            "candidate_rows": census_candidates,
            "line": census_selected["line"] if census_selected else None,
            "key_count": census_selected["key_count"] if census_selected else None,
            "keys": census_selected["keys"] if census_selected else [],
            "unresolved": census_selected["unresolved"] if census_selected
                else ["NO_USABLE_CANDIDATE"],
            "closed": False,
        }
    if producer is not None:
        execution_keys = set(_function_keyset(
            producer, "execution_proof").get("keys", []))
        constructor_rows["producerSourceRegistry"] = _function_keyset(
            producer, "input_registry",
            attribute_known={"self_guard.execution_proof()": execution_keys})
    if launcher is not None:
        chronology_keys = set(_function_keyset(
            launcher, "cold_publication_chronology").get("keys", []))
        constructor_rows["coldLaunchProof"] = _function_keyset(
            launcher, "cold_root", target_name="proof",
            attribute_known={"bundle.chronology": chronology_keys})
        constructor_rows["laterRejection"] = _function_keyset(
            launcher, "construct_launcher_native_rejection")
        constructor_rows["liveRequest"] = _function_keyset(
            launcher, "run_authorize_child", target_name="request")
    for name, row in constructor_rows.items():
        row["expected_key_count"] = EXPECTED_OUTPUT_SHAPES[name]
        row["matches_expected_key_count"] = (
            not row.get("unresolved") and
            row.get("key_count") == EXPECTED_OUTPUT_SHAPES[name])

    declaration_rows = {
        role: output_shape_values(tree, envs[role])
        for role, tree in trees.items()}
    declarations_ok = (
        len(declaration_rows) == 3 and
        all(rows == [EXPECTED_OUTPUT_SHAPES] for rows in declaration_rows.values()))
    constructors_ok = (
        set(constructor_rows) == set(EXPECTED_OUTPUT_SHAPES) and
        all(row["matches_expected_key_count"] for row in constructor_rows.values()))
    return {
        "expected_shapes": EXPECTED_OUTPUT_SHAPES,
        "constructor_keyset_reconstruction": constructor_rows,
        "three_source_declared_shapes": declaration_rows,
        "declarations_match": declarations_ok,
        "constructors_match": constructors_ok,
        "matches": declarations_ok and constructors_ok,
    }


def v12_incident_semantics(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    expected_source_files = {
        "v12_producer_source_file_sha256": V12_EXACT10[3][1],
        "v12_consumer_source_file_sha256": V12_EXACT10[4][1],
        "v12_launcher_source_file_sha256": V12_EXACT10[7][1],
        "v12_manifest_file_sha256": V12_EXACT10[8][1],
        "v12_outer_file_sha256": V12_EXACT10[9][1],
        "v12_outer_object_sha256": V12_EXACT10[9][2],
        "v12_official_rejection_file_sha256":
            EXPECTED_V12_REJECTION_FILE_SHA256,
        "v12_official_rejection_object_sha256":
            EXPECTED_V12_REJECTION_OBJECT_SHA256,
        "v5_rejection_exact39_keyset_sha256": EXPECTED_EXACT39_KEYSET_SHA256,
    }
    return (
        all(value.get(key) == expected for key, expected in expected_source_files.items()) and
        value.get("schema") == (
            "cm2.round306c79g.true-global-no-producer-consumer."
            "v12-v5-rejection-shape-incident.v1") and
        value.get("incident_id") == (
            "V12_LAUNCHER_V5_REJECTION_WRONG_EXPECTED_KEY_COUNT_52_FOR_"
            "CANONICAL_EXACT39") and
        value.get("failed_phase") ==
            "LAUNCHER_PRECHILD_HELD_HISTORY_CONSTRUCTOR" and
        value.get("actual_v5_rejection_key_count") == 39 and
        value.get("wrong_v12_launcher_expected_key_count") == 52 and
        value.get("v5_rejection_exact39_sorted_keys") == sorted(EXACT39_KEYS) and
        value.get("producer_v12_validator_uses_exact39_keyset") is True and
        value.get("consumer_v12_validator_uses_exact39_keyset") is True and
        value.get("launcher_v12_validator_used_bare_wrong_length_52") is True and
        value.get("bare_length_only_is_authority") is False and
        value.get("producer_child_spawned") is False and
        value.get("consumer_child_spawned") is False and
        value.get("candidate_write_started") is False and
        value.get("stage_write_started") is False and
        value.get("positive_runtime_surface_count") == 0 and
        value.get("formal_global_closure_credit") == 0 and
        value.get("D02_unlock") is False and
        value.get("D02_gate_credit") == 0 and
        value.get("D02_task_credit") == 0 and
        value.get("D02_formal_pending_task_count") == 33_638 and
        value.get("D02_started") is False)


def review() -> dict[str, Any]:
    report = Report()
    sections: dict[str, Any] = {}
    held: dict[Path, tuple[bytes, tuple[int, ...]]] = {}

    def snapshot(path: Path) -> bytes:
        if path not in held:
            held[path] = read_stable(path)
        return held[path][0]

    source_raw: dict[str, bytes] = {}
    source_trees: dict[str, ast.Module] = {}
    source_envs: dict[str, dict[str, Any]] = {}
    python_section: dict[str, Any] = {}
    total_duplicates = 0
    all_undefined: dict[str, list[str]] = {}
    for role, path in V13_PYTHON.items():
        raw = snapshot(path)
        source_raw[role] = raw
        label = path.name
        try:
            source = raw.decode("utf-8")
            tree = ast.parse(source, filename=label, mode="exec")
            compile(tree, label, "exec", dont_inherit=True)
            stats = dict_literal_stats(tree, label)
            undefined = undefined_globals(source, label)
            source_trees[role] = tree
            source_envs[role] = literal_environment(tree)
            total_duplicates += stats["duplicate_count"]
            all_undefined[role] = undefined
            python_section[role] = {
                "path": str(path.relative_to(ROOT)),
                "file_sha256": sha_bytes(raw),
                "size": len(raw),
                "ast_parse_and_in_memory_compile": True,
                "dict_literals": stats,
                "undefined_globals": undefined,
            }
        except Exception as exc:  # fail closed but retain the other source reports
            all_undefined[role] = [f"STATIC_PARSE_ERROR:{type(exc).__name__}"]
            python_section[role] = {
                "path": str(path.relative_to(ROOT)),
                "file_sha256": sha_bytes(raw),
                "size": len(raw),
                "ast_parse_and_in_memory_compile": False,
                "error": f"{type(exc).__name__}: {exc}",
            }
    sections["python_static"] = python_section
    report.add("three_python_ast_parse_and_in_memory_compile", len(source_trees) == 3)
    report.add("python_literal_dict_duplicate_key_count_zero",
               len(source_trees) == 3 and total_duplicates == 0,
               duplicate_count=total_duplicates)
    report.add("python_undefined_global_count_zero",
               len(source_trees) == 3 and not any(all_undefined.values()),
               undefined_globals=all_undefined)

    target_pyc_initial = target_v13_pyc_paths()
    pyc_directory_row: dict[str, Any]
    try:
        pyc_directory_stat = os.lstat(V13_PYC_DIRECTORY)
        pyc_directory_row = {
            "path": str(V13_PYC_DIRECTORY.relative_to(ROOT)),
            "present": True,
            "is_directory": stat.S_ISDIR(pyc_directory_stat.st_mode),
            "is_symlink": stat.S_ISLNK(pyc_directory_stat.st_mode),
            "mode": oct(stat.S_IMODE(pyc_directory_stat.st_mode)),
            "st_dev": pyc_directory_stat.st_dev,
            "st_ino": pyc_directory_stat.st_ino,
            "st_nlink": pyc_directory_stat.st_nlink,
            "st_mtime_ns": pyc_directory_stat.st_mtime_ns,
            "st_ctime_ns": pyc_directory_stat.st_ctime_ns,
        }
    except FileNotFoundError:
        pyc_directory_row = {
            "path": str(V13_PYC_DIRECTORY.relative_to(ROOT)),
            "present": False,
        }
    target_pyc_rows: list[dict[str, Any]] = []
    for path in target_pyc_initial:
        role = target_v13_pyc_role(path)
        raw = snapshot(path)
        pyc_identity = held[path][1]
        source_path = V13_PYTHON[role] if role is not None else None
        source_identity = held[source_path][1] if source_path in held else None
        header = decode_pyc_header(raw)
        header_timestamp = header.get("source_timestamp_uint32_le")
        header_size = header.get("source_size_uint32_le")
        source_mtime_seconds = (
            source_identity[5] // 1_000_000_000
            if source_identity is not None else None)
        source_size = source_identity[4] if source_identity is not None else None
        target_pyc_rows.append({
            "role": role,
            "path": str(path.relative_to(ROOT)),
            "file_sha256": sha_bytes(raw),
            "stat": {
                "st_dev": pyc_identity[0], "st_ino": pyc_identity[1],
                "mode": oct(stat.S_IMODE(pyc_identity[2])),
                "st_nlink": pyc_identity[3], "st_size": pyc_identity[4],
                "st_mtime_ns": pyc_identity[5], "st_ctime_ns": pyc_identity[6],
            },
            "header": header,
            "source": {
                "path": str(source_path.relative_to(ROOT))
                    if source_path is not None else None,
                "current_file_sha256": sha_bytes(source_raw[role])
                    if role in source_raw else None,
                "current_st_size": source_size,
                "current_st_mtime_ns": source_identity[5]
                    if source_identity is not None else None,
                "current_st_mtime_epoch_seconds": source_mtime_seconds,
                "current_st_ctime_ns": source_identity[6]
                    if source_identity is not None else None,
            },
            "timestamp_header_matches_current_source_mtime_seconds": (
                header_timestamp == source_mtime_seconds
                if header_timestamp is not None and source_mtime_seconds is not None
                else None),
            "timestamp_header_size_matches_current_source_size": (
                header_size == source_size
                if header_size is not None and source_size is not None else None),
        })
    target_pyc_present = bool(target_pyc_rows)
    role_counts = {
        role: sum(row["role"] == role for row in target_pyc_rows)
        for role in V13_PYTHON}
    sections["target_v13_pyc_incident"] = {
        "pyc_or___pycache___created": target_pyc_present,
        "target_pyc_created_or_present": target_pyc_present,
        "target___pycache___directory": pyc_directory_row,
        "target_pyc_count": len(target_pyc_rows),
        "target_pyc_role_counts": role_counts,
        "target_pyc_files": target_pyc_rows,
        "pyc_code_objects_unmarshalled_or_executed": False,
        "files_deleted_moved_or_modified_by_reviewer": False,
    }
    report.add(
        "target_v13_pyc_or___pycache___created_or_present_false",
        not target_pyc_present,
        target_pyc_created_or_present=target_pyc_present,
        target_pyc_count=len(target_pyc_rows),
        target_pyc_paths=[row["path"] for row in target_pyc_rows])

    builder_tree: ast.Module | None = None
    builder_env: dict[str, Any] = {}
    builder_section: dict[str, Any]
    try:
        builder_raw = snapshot(V13_JSON_BUILDER)
        builder_source = builder_raw.decode("utf-8")
        builder_tree = ast.parse(
            builder_source, filename=V13_JSON_BUILDER.name, mode="exec")
        compile(builder_tree, V13_JSON_BUILDER.name, "exec", dont_inherit=True)
        builder_env = literal_environment(builder_tree)
        builder_duplicates = dict_literal_stats(
            builder_tree, V13_JSON_BUILDER.name)
        builder_undefined = undefined_globals(
            builder_source, V13_JSON_BUILDER.name)
        builder_section = {
            "path": str(V13_JSON_BUILDER.relative_to(ROOT)),
            "file_sha256": sha_bytes(builder_raw),
            "ast_parse_and_in_memory_compile": True,
            "dict_literals": builder_duplicates,
            "undefined_globals": builder_undefined,
        }
        builder_static_ok = (
            builder_duplicates["duplicate_count"] == 0 and not builder_undefined)
    except Exception as exc:
        builder_static_ok = False
        builder_section = {"path": str(V13_JSON_BUILDER.relative_to(ROOT)),
                           "error": f"{type(exc).__name__}: {exc}"}
    sections["json_builder_static"] = builder_section
    report.add("v13_json_builder_ast_compile_duplicates_and_undefined_close",
               builder_static_ok, details=builder_section)

    helper_rows = {
        role: incident_helper_review(tree, role)
        for role, tree in source_trees.items()}
    helper_ast_digests = {
        row["normalized_ast_sha256"] for row in helper_rows.values()
        if row["normalized_ast_sha256"] is not None}
    incident_helper_ok = (
        len(helper_rows) == 3 and
        helper_ast_digests == {EXPECTED_V12_INCIDENT_HELPER_AST_SHA256} and
        all(row["matches_expected_callsites"] for row in helper_rows.values()))
    sections["v12_incident_helper_and_callsites"] = {
        "expected_normalized_ast_sha256":
            EXPECTED_V12_INCIDENT_HELPER_AST_SHA256,
        "roles": helper_rows,
    }
    report.add("v12_incident_helper_normalized_ast_and_exact_callsites_close_P_C_L",
               incident_helper_ok)

    incident_values = {
        role: env.get("V12_V5_REJECTION_SHAPE_INCIDENT")
        for role, env in source_envs.items()}
    incident_declared_digests = {
        role: env.get("V12_V5_REJECTION_SHAPE_INCIDENT_SHA256")
        for role, env in source_envs.items()}
    incident_computed_digests = {
        role: sha_bytes(canonical(value)) if isinstance(value, dict) else None
        for role, value in incident_values.items()}
    distinct_incident_objects = {
        canonical(value) for value in incident_values.values()
        if isinstance(value, dict)}
    common_incident_digest = next(iter(incident_computed_digests.values()), None)
    builder_incident_value = builder_env.get("V12_V5_REJECTION_SHAPE_INCIDENT")
    builder_declared_incident_digest = builder_env.get(
        "V12_V5_REJECTION_SHAPE_INCIDENT_SHA256")
    incident_object_ok = (
        len(incident_values) == 3 and len(distinct_incident_objects) == 1 and
        all(v12_incident_semantics(value) for value in incident_values.values()) and
        common_incident_digest is not None and
        set(incident_computed_digests.values()) == {common_incident_digest} and
        set(incident_declared_digests.values()) == {common_incident_digest} and
        builder_declared_incident_digest == common_incident_digest and
        (builder_incident_value is None or
         (isinstance(builder_incident_value, dict) and
          canonical(builder_incident_value) in distinct_incident_objects)))
    sections["v12_incident_object_digest_consensus"] = {
        "source_declared_digests": incident_declared_digests,
        "source_computed_digests": incident_computed_digests,
        "source_object_byte_identity_count": len(distinct_incident_objects),
        "source_semantics_match": {
            role: v12_incident_semantics(value)
            for role, value in incident_values.items()},
        "builder_declared_digest": builder_declared_incident_digest,
        "builder_embeds_incident_object": isinstance(builder_incident_value, dict),
        "builder_object_matches_sources": (
            isinstance(builder_incident_value, dict) and
            canonical(builder_incident_value) in distinct_incident_objects),
    }
    report.add("v12_incident_object_canonical_digest_consensus_P_C_L_builder",
               incident_object_ok)

    fd_environment_rows = {
        role: incident_fd_environment_review(
            source_trees[role], source_envs[role], role)
        for role in ("producer", "consumer") if role in source_trees}
    incident_fd_environment_ok = (
        set(fd_environment_rows) == {"producer", "consumer"} and
        all(row["matches"] for row in fd_environment_rows.values()))
    sections["P_C_incident_inherited_fd_environment"] = fd_environment_rows
    report.add("producer_consumer_incident_env_roles_exact10_total_fd14",
               incident_fd_environment_ok)

    launcher_v12_first = (
        launcher_v12_first_review(
            source_trees["launcher"], source_envs["launcher"])
        if "launcher" in source_trees else {"matches": False})
    launcher_v12_first_ok = bool(launcher_v12_first.get("matches"))
    sections["launcher_v12_first_pin_graph"] = launcher_v12_first
    report.add("launcher_pin_normalizer_and_base_objects_are_v12_first_without_v11_residual",
               launcher_v12_first_ok)

    flags: dict[str, Any] = {}
    final_names = {
        "producer": "FINAL_V13_CORE_PINS_INSTALLED",
        "consumer": "FINAL_CURRENT_V13_PINS_INSTALLED",
        "launcher": "FINAL_BASE7_PINS_INSTALLED",
    }
    for role in V13_PYTHON:
        env = source_envs.get(role, {})
        flags[role] = {
            "V13_DRAFT_RUNTIME_DISABLED": env.get("V13_DRAFT_RUNTIME_DISABLED"),
            "final_flag_name": final_names[role],
            "final_flag_value": env.get(final_names[role]),
        }
    sections["draft_and_final_flags"] = flags
    report.add("draft_execution_disabled_in_all_three_sources",
               all(row["V13_DRAFT_RUNTIME_DISABLED"] is True for row in flags.values()),
               flags=flags)

    json_initial_presence = {name: path_exists(path) for name, path in V13_JSON.items()}
    draft_json_absent = not any(json_initial_presence.values())
    report.add("final_pin_flags_false_while_all_v13_json_surfaces_absent",
               (not draft_json_absent or
                all(row["final_flag_value"] is False for row in flags.values())),
               all_json_absent=draft_json_absent, flags=flags)

    expected_pin_rows = [(file_pin, object_pin) for _, file_pin, object_pin in V12_EXACT10]
    exact10_filesystem: list[dict[str, Any]] = []
    exact10_fs_ok = True
    for relative, file_pin, object_pin in V12_EXACT10:
        path = ROOT / relative
        raw = snapshot(path)
        closure: dict[str, Any] | None = None
        if object_pin is not None:
            try:
                value, duplicates = decode_json(raw, str(path))
                closure = object_closure(value)
                closure["duplicate_keys"] = duplicates
                object_ok = (not duplicates and closure["matches"] and
                             closure["declared"] == object_pin)
            except Exception as exc:
                closure = {"matches": False, "error": f"{type(exc).__name__}: {exc}"}
                object_ok = False
        else:
            object_ok = True
        row_ok = sha_bytes(raw) == file_pin and object_ok
        exact10_fs_ok &= row_ok
        exact10_filesystem.append({
            "path": relative, "observed_file_sha256": sha_bytes(raw),
            "expected_file_sha256": file_pin,
            "expected_object_sha256": object_pin,
            "object_closure": closure, "matches": row_ok,
        })
    sections["v12_published_exact10_filesystem"] = exact10_filesystem
    report.add("v12_published_exact10_files_and_objects_match", exact10_fs_ok,
               exact10_count=len(exact10_filesystem))

    v12_rejection_raw = snapshot(V12_REJECTION)
    v12_rejection, v12_duplicates = decode_json(v12_rejection_raw, str(V12_REJECTION))
    v12_closure = object_closure(v12_rejection)
    v12_rejection_ok = (
        isinstance(v12_rejection, dict) and not v12_duplicates and
        sha_bytes(v12_rejection_raw) == EXPECTED_V12_REJECTION_FILE_SHA256 and
        v12_closure["matches"] and
        v12_closure["declared"] == EXPECTED_V12_REJECTION_OBJECT_SHA256 and
        set(v12_rejection) == V12_REJECTION_KEYS)
    sections["v12_official_rejection"] = {
        "path": str(V12_REJECTION.relative_to(ROOT)),
        "file_sha256": sha_bytes(v12_rejection_raw),
        "object_closure": v12_closure,
        "key_count": len(v12_rejection) if isinstance(v12_rejection, dict) else None,
        "keyset_sha256": sha_bytes(canonical(sorted(v12_rejection)))
            if isinstance(v12_rejection, dict) else None,
        "duplicate_keys": v12_duplicates,
    }
    report.add("v12_official_rejection_exact54_file_object_and_keyset_match",
               v12_rejection_ok)

    source_pin_rows: dict[str, Any] = {}
    if len(source_trees) == 3:
        producer_rows = producer_exact10_pins(source_trees["producer"])
        consumer_files = consumer_exact10_files(
            source_trees["consumer"], source_envs["consumer"])
        launcher_rows = launcher_exact10_pins(
            source_trees["launcher"], source_envs["launcher"])
        source_pin_rows = {
            "producer": producer_rows,
            "consumer_file_order": consumer_files,
            "launcher": launcher_rows,
        }
        exact10_source_ok = (
            producer_rows == expected_pin_rows and
            consumer_files == [row[0] for row in expected_pin_rows] and
            launcher_rows == expected_pin_rows)
    else:
        exact10_source_ok = False
    sections["v12_exact10_source_pins"] = source_pin_rows
    report.add("v12_exact10_pins_close_across_producer_consumer_launcher",
               exact10_source_ok)

    rejection_pin_state: dict[str, Any] = {}
    for role, env in source_envs.items():
        file_name = (
            "V12_REJECTION_FILE_PIN" if role == "launcher"
            else "V12_OFFICIAL_REJECTION_FILE_PIN")
        object_name = (
            "V12_REJECTION_OBJECT_PIN" if role == "launcher"
            else "V12_OFFICIAL_REJECTION_OBJECT_PIN")
        strings = literal_strings(source_trees[role])
        rejection_pin_state[role] = {
            "file_pin": env.get(file_name), "object_pin": env.get(object_name),
            "all_exact10_file_pins_present_somewhere": all(
                pin in strings or pin in env.values()
                for _, pin, _ in V12_EXACT10),
            "all_exact10_object_pins_present_somewhere": all(
                object_pin is None or object_pin in strings or object_pin in env.values()
                for _, _, object_pin in V12_EXACT10),
            # The no-producer consumer intentionally carries the ordered ten
            # file pins; producer and launcher carry the canonical object
            # pins used for historical object closure.
            "exact10_object_pin_presence_required_for_role":
                role in {"producer", "launcher"},
        }
    rejection_pin_sources_ok = all(
        row["file_pin"] == EXPECTED_V12_REJECTION_FILE_SHA256 and
        row["object_pin"] == EXPECTED_V12_REJECTION_OBJECT_SHA256 and
        row["all_exact10_file_pins_present_somewhere"] and
        (not row["exact10_object_pin_presence_required_for_role"] or
         row["all_exact10_object_pins_present_somewhere"])
        for row in rejection_pin_state.values())
    sections["v12_rejection_and_exact10_pin_presence"] = rejection_pin_state
    report.add("v12_exact10_plus_official_rejection_pins_present_in_all_three_sources",
               len(rejection_pin_state) == 3 and rejection_pin_sources_ok)

    v5_raw = snapshot(V5_REJECTION)
    v5_value, v5_duplicates = decode_json(v5_raw, str(V5_REJECTION))
    v5_closure = object_closure(v5_value)
    exact39_authority_ok = (
        isinstance(v5_value, dict) and not v5_duplicates and
        sha_bytes(v5_raw) == EXPECTED_V5_REJECTION_FILE_SHA256 and
        v5_closure["matches"] and
        v5_closure["declared"] == EXPECTED_V5_REJECTION_OBJECT_SHA256 and
        set(v5_value) == EXACT39_KEYS and len(EXACT39_KEYS) == 39 and
        sha_bytes(canonical(sorted(EXACT39_KEYS))) == EXPECTED_EXACT39_KEYSET_SHA256)
    exact39_sources: dict[str, Any] = {}
    exact39_source_ok = len(source_trees) == 3
    all_len52: list[dict[str, Any]] = []
    stale_len52: list[dict[str, Any]] = []
    for role, tree in source_trees.items():
        env = source_envs[role]
        gates = exact39_gate_counts(tree)
        all_rows, stale_rows = stale_v5_len52_rows(tree, role)
        all_len52.extend(all_rows)
        stale_len52.extend(stale_rows)
        row = {
            "declared_key_count": len(env.get("V5_OFFICIAL_REJECTION_EXACT39_KEYS", ()))
                if isinstance(env.get("V5_OFFICIAL_REJECTION_EXACT39_KEYS"),
                              (set, frozenset, tuple, list)) else None,
            "declared_keys_match": env.get("V5_OFFICIAL_REJECTION_EXACT39_KEYS") == EXACT39_KEYS,
            "declared_keyset_sha256": env.get(
                "V5_OFFICIAL_REJECTION_EXACT39_KEYSET_SHA256"),
            **gates,
        }
        exact39_sources[role] = row
        exact39_source_ok &= (
            row["declared_keys_match"] and
            row["declared_keyset_sha256"] == EXPECTED_EXACT39_KEYSET_SHA256 and
            row["set_equality_gate_count"] >= 1 and
            row["derived_len39_gate_count"] >= 1)
    sections["v5_exact39_authority"] = {
        "file_sha256": sha_bytes(v5_raw), "object_closure": v5_closure,
        "key_count": len(v5_value) if isinstance(v5_value, dict) else None,
        "keyset_sha256": sha_bytes(canonical(sorted(v5_value)))
            if isinstance(v5_value, dict) else None,
        "source_gates": exact39_sources,
        "all_len52_rows": all_len52,
        "stale_v5_len52_rows": stale_len52,
    }
    report.add("v5_rejection_exact39_external_authority_matches", exact39_authority_ok)
    report.add("v5_exact39_keyset_and_set_equality_gate_close_in_all_three_sources",
               exact39_source_ok)
    report.add("old_v5_len52_magic_number_gate_absent", not stale_len52,
               stale_rows=stale_len52, allowed_non_v5_len52_rows=all_len52)

    historical_actual: dict[str, Any] = {}
    expected_historical_witness: list[dict[str, Any]] = []
    historical_external_ok = True
    for version in HISTORICAL_REJECTION_VERSION_ORDER:
        file_pin, object_pin, key_count, keyset_digest = (
            HISTORICAL_REJECTION_PINS[version])
        path = (RUNTIME / f"c79g-{version}-rejections-{CHECKPOINT}" /
                "rejection.json")
        raw = snapshot(path)
        value, duplicates = decode_json(raw, str(path))
        closure = object_closure(value)
        observed_keys = sorted(value) if isinstance(value, dict) else []
        observed_keyset_digest = sha_bytes(canonical(observed_keys))
        held_identity = held[path][1]
        matches = (
            isinstance(value, dict) and not duplicates and
            sha_bytes(raw) == file_pin and closure["matches"] and
            closure["declared"] == object_pin and len(value) == key_count and
            observed_keyset_digest == keyset_digest and
            raw == canonical(value) + b"\n" and
            stat.S_IMODE(held_identity[2]) == 0o444 and held_identity[3] == 1)
        historical_external_ok &= matches
        relative = str(path.relative_to(ROOT))
        historical_actual[version] = {
            "path": relative, "file_sha256": sha_bytes(raw),
            "object_closure": closure, "key_count": len(observed_keys),
            "sorted_key_array_sha256": observed_keyset_digest,
            "mode": oct(stat.S_IMODE(held_identity[2])),
            "nlink": held_identity[3], "duplicate_keys": duplicates,
            "matches": matches,
        }
        expected_historical_witness.append({
            "version": version, "path": relative,
            "file_sha256": file_pin, "object_sha256": object_pin,
            "key_count": key_count, "sorted_keys": observed_keys,
            "sorted_key_array_sha256": keyset_digest,
            "canonical_object_closed": True,
        })
    historical_witness_reviews = {
        role: historical_witness_builder_review(
            source_trees[role], source_envs[role], role,
            expected_historical_witness)
        for role in source_trees}
    historical_witness_rows = {
        role: row["reconstructed_rows"]
        for role, row in historical_witness_reviews.items()}
    historical_witness_ok = (
        historical_external_ok and len(historical_witness_reviews) == 3 and
        all(row["matches"] for row in historical_witness_reviews.values()))
    sections["historical_rejection_exact_keyset_witness"] = {
        "required_version_order": list(HISTORICAL_REJECTION_VERSION_ORDER),
        "external_rejections": historical_actual,
        "source_witness_rows": historical_witness_rows,
        "source_AST_builder_reviews": historical_witness_reviews,
        "expected_witness_rows": expected_historical_witness,
    }
    report.add("historical_rejection_v3_v5_through_v12_external_keysets_close",
               historical_external_ok)
    report.add("historical_rejection_exact_keyset_witness_closes_in_P_C_L",
               historical_witness_ok)

    published_adjacency = {
        role: published_v11_v12_adjacency_review(tree, role)
        for role, tree in source_trees.items()}
    published_adjacency_ok = (
        len(published_adjacency) == 3 and
        all(row["matches"] for row in published_adjacency.values()))
    sections["published_v11_then_v12_all_surface_adjacency"] = published_adjacency
    report.add(
        "published_then_officially_rejected_predecessor_v12_adjacent_after_every_v11_surface_P_C_L",
        published_adjacency_ok,
        failed_row_count=sum(
            len(row["failed_rows"]) for row in published_adjacency.values()))

    consumer_static_v12 = (
        consumer_static_freeze_v12_review(source_trees["consumer"])
        if "consumer" in source_trees else {"matches": False})
    consumer_static_v12_ok = bool(consumer_static_v12.get("matches"))
    sections["consumer_static_freeze_current_v12_transition"] = consumer_static_v12
    report.add(
        "consumer_static_freeze_uses_current_v12_rejection_v12_transition_kind_and_v12_exact8_first",
        consumer_static_v12_ok)

    replay_v12 = terminal_replay_v11_then_v12_review(source_trees)
    replay_v12_ok = bool(replay_v12.get("matches"))
    sections["v11_then_v12_terminal_replay_before_authorize_request"] = replay_v12
    report.add(
        "every_existing_v11_exact10_terminal_replay_is_followed_by_v12_before_authorize_request",
        replay_v12_ok)

    registry_v12 = registry_v12_authority_review(source_trees)
    registry_v12_ok = bool(registry_v12.get("matches"))
    sections["registry_and_cold_authority_v12"] = registry_v12
    report.add(
        "producer_registry_consumer_registry_and_launcher_cold_authority_include_v12_authority",
        registry_v12_ok)

    static_audit_inputs = static_audit_input_v12_extension_review(
        source_envs, builder_env)
    static_audit_inputs_ok = bool(static_audit_inputs.get("matches"))
    sections["static_audit_input_v12_extension"] = static_audit_inputs
    report.add(
        "static_audit_input_order_extends_v11_exact37_with_exact_v12_authority_suffix_P_C_L_builder",
        static_audit_inputs_ok)

    exact56_digest_ok = (
        len(EXACT56_KEYS) == 56 and
        sha_bytes(canonical(sorted(EXACT56_KEYS))) == EXPECTED_EXACT56_KEYSET_SHA256)
    launcher_constructed_keys: set[str] = set()
    launcher_digest = None
    if "launcher" in source_trees:
        functions = [
            node for node in source_trees["launcher"].body
            if isinstance(node, ast.FunctionDef) and
            node.name == "construct_launcher_native_rejection"]
        if len(functions) == 1:
            launcher_constructed_keys = largest_string_key_dict(functions[0])
        launcher_digest = source_envs["launcher"].get(
            "V13_LATER_REJECTION_EXACT56_KEYSET_SHA256")
    output_shape_review = output_shape_constructor_review(
        source_trees, source_envs)
    output_shapes_ok = bool(output_shape_review.get("matches"))
    shape_rows = output_shape_review["three_source_declared_shapes"]
    shapes_ok = (
        output_shape_review.get("declarations_match") is True and
        output_shape_review.get("constructor_keyset_reconstruction", {}).get(
            "laterRejection", {}).get("matches_expected_key_count") is True)
    # ``construct_launcher_native_rejection`` passes a 55-key body to
    # close_object(); object_sha256 is deterministically appended there.
    launcher_closed_keys = launcher_constructed_keys | {"object_sha256"}
    exact56_source_ok = (
        exact56_digest_ok and launcher_closed_keys == EXACT56_KEYS and
        launcher_digest == EXPECTED_EXACT56_KEYSET_SHA256 and shapes_ok)
    sections["v13_exact56_keyset"] = {
        "expected_key_count": len(EXACT56_KEYS),
        "expected_sorted_key_array_sha256": sha_bytes(canonical(sorted(EXACT56_KEYS))),
        "launcher_declared_digest": launcher_digest,
        "launcher_body_key_count_before_close_object": len(launcher_constructed_keys),
        "launcher_closed_key_count": len(launcher_closed_keys),
        "launcher_closed_keyset_sha256": sha_bytes(
            canonical(sorted(launcher_closed_keys))),
        "missing_launcher_closed_keys": sorted(EXACT56_KEYS - launcher_closed_keys),
        "extra_launcher_closed_keys": sorted(launcher_closed_keys - EXACT56_KEYS),
        "output_shape_rows": shape_rows,
    }
    report.add("v13_launcher_exact56_and_three_source_shape_declarations_match",
               exact56_source_ok)
    sections["output_shape_constructor_reconstruction"] = output_shape_review
    report.add(
        "all_nine_output_shapes_mechanically_recompute_from_AST_constructors",
        output_shapes_ok)

    json_section: dict[str, Any] = {}
    json_all_present = all(json_initial_presence.values())
    json_all_close = json_all_present
    schema_exact56 = False
    for name, path in V13_JSON.items():
        if not json_initial_presence[name]:
            json_section[name] = {"present": False}
            continue
        try:
            raw = snapshot(path)
            value, duplicates = decode_json(raw, str(path))
            closure = object_closure(value) if name != "schema" else None
            row_ok = not duplicates and isinstance(value, dict)
            if name != "schema":
                row_ok &= bool(closure and closure["matches"])
            if name == "schema" and isinstance(value, dict):
                definition = value.get("$defs", {}).get("laterRejection", {})
                schema_keys = set(definition.get("properties", {}))
                required = set(definition.get("required", []))
                schema_exact56 = (
                    definition.get("type") == "object" and
                    definition.get("additionalProperties") is False and
                    schema_keys == required == EXACT56_KEYS)
                row_ok &= schema_exact56
            json_all_close &= row_ok
            json_section[name] = {
                "present": True, "file_sha256": sha_bytes(raw),
                "duplicate_keys": duplicates, "object_closure": closure,
                "matches_current_static_requirements": row_ok,
            }
        except Exception as exc:
            json_all_close = False
            json_section[name] = {"present": True,
                                  "error": f"{type(exc).__name__}: {exc}"}
    sections["v13_json_surfaces"] = json_section
    report.add("v13_json_surfaces_all_absent_in_safe_prebuilder_draft",
               draft_json_absent, presence=json_initial_presence)
    report.add("v13_json_surfaces_present_closed_and_schema_laterRejection_exact56",
               json_all_present and json_all_close and schema_exact56,
               presence=json_initial_presence, schema_exact56=schema_exact56)

    history_semantics = history_identity_semantics_review(source_trees)
    history_semantics_ok = bool(history_semantics.get("matches"))
    sections["history_identity_census"] = {
        "expected_predecessor_unique_identity_count": 98,
        "expected_prepublication_unique_identity_count":
            EXPECTED_PREPUBLICATION_IDENTITY_COUNT,
        "expected_terminal_unique_identity_count": EXPECTED_TERMINAL_IDENTITY_COUNT,
        "expected_runtime_group_vector": EXPECTED_RUNTIME_GROUP_VECTOR,
        **history_semantics,
    }
    report.add(
        "v13_history_identity_semantics_predecessor98_prepublication106_terminal108_vector_close",
        history_semantics_ok)

    runtime_initial = [path for path in v13_runtime_surfaces() if path_exists(path)]
    manifest_outer_initial = {
        "manifest": path_exists(V13_MANIFEST), "outer": path_exists(V13_OUTER)}
    sections["publication_and_runtime_absence"] = {
        "manifest_outer_presence": manifest_outer_initial,
        "runtime_surface_count": len(runtime_initial),
        "runtime_surfaces": [str(path.relative_to(ROOT)) for path in runtime_initial],
    }
    report.add("v13_manifest_and_outer_absent_before_publication",
               not any(manifest_outer_initial.values()),
               presence=manifest_outer_initial)
    report.add("v13_runtime_candidate_verification_completion_authority_rejection_and_stages_absent",
               not runtime_initial,
               present=[str(path.relative_to(ROOT)) for path in runtime_initial])

    finals_true = all(row["final_flag_value"] is True for row in flags.values())
    report.add("v13_final_static_bundle_gate",
               builder_static_ok and incident_helper_ok and incident_object_ok and
               incident_fd_environment_ok and launcher_v12_first_ok and
               historical_external_ok and historical_witness_ok and
               finals_true and json_all_present and json_all_close and
               schema_exact56 and exact10_fs_ok and v12_rejection_ok and
               exact10_source_ok and rejection_pin_sources_ok and
               exact39_authority_ok and exact39_source_ok and not stale_len52 and
               exact56_source_ok and output_shapes_ok and
               published_adjacency_ok and consumer_static_v12_ok and
               replay_v12_ok and registry_v12_ok and static_audit_inputs_ok and
               history_semantics_ok and
               not target_pyc_present and
               not any(manifest_outer_initial.values()) and not runtime_initial,
               final_flags_true=finals_true,
               incident_helper_ok=incident_helper_ok,
               incident_object_ok=incident_object_ok,
               incident_fd_environment_ok=incident_fd_environment_ok,
               launcher_v12_first_ok=launcher_v12_first_ok,
               historical_witness_ok=historical_witness_ok,
               published_adjacency_ok=published_adjacency_ok,
               consumer_static_v12_ok=consumer_static_v12_ok,
               replay_v12_ok=replay_v12_ok,
               registry_v12_ok=registry_v12_ok,
               static_audit_inputs_ok=static_audit_inputs_ok,
               output_shapes_ok=output_shapes_ok,
               history_semantics_ok=history_semantics_ok,
               target_pyc_created_or_present=target_pyc_present,
               json_all_present=json_all_present,
               json_all_close=json_all_close,
               publication_and_runtime_absent=(
                   not any(manifest_outer_initial.values()) and not runtime_initial))

    # Terminal snapshot: reopening is read-only and detects both metadata and
    # byte drift.  No intermediate hash can yield GO if any held source moved.
    changed: list[dict[str, Any]] = []
    for path, (before_raw, before_identity) in sorted(held.items(), key=lambda item: str(item[0])):
        try:
            after_raw, after_identity = read_stable(path)
            if before_identity != after_identity or before_raw != after_raw:
                changed.append({
                    "path": str(path.relative_to(ROOT)),
                    "before_identity": before_identity,
                    "after_identity": after_identity,
                    "before_sha256": sha_bytes(before_raw),
                    "after_sha256": sha_bytes(after_raw),
                })
        except Exception as exc:
            changed.append({"path": str(path.relative_to(ROOT)),
                            "terminal_error": f"{type(exc).__name__}: {exc}"})
    json_terminal_presence = {name: path_exists(path) for name, path in V13_JSON.items()}
    runtime_terminal = [path for path in v13_runtime_surfaces() if path_exists(path)]
    target_pyc_terminal = target_v13_pyc_paths()
    manifest_outer_terminal = {
        "manifest": path_exists(V13_MANIFEST), "outer": path_exists(V13_OUTER)}
    initial_target_pyc_names = {str(path) for path in target_pyc_initial}
    terminal_target_pyc_names = {str(path) for path in target_pyc_terminal}
    target_pyc_set_changed = initial_target_pyc_names != terminal_target_pyc_names
    sections["target_v13_pyc_incident"].update({
        "terminal_target_pyc_count": len(target_pyc_terminal),
        "terminal_target_pyc_paths": [
            str(path.relative_to(ROOT)) for path in target_pyc_terminal],
        "target_pyc_set_changed_during_review": target_pyc_set_changed,
    })
    if target_pyc_set_changed:
        changed.append({
            "surface": "target_v13_pyc_presence",
            "before": sorted(initial_target_pyc_names),
            "after": sorted(terminal_target_pyc_names),
        })
    if json_initial_presence != json_terminal_presence:
        changed.append({"surface": "v13_json_presence",
                        "before": json_initial_presence,
                        "after": json_terminal_presence})
    if manifest_outer_initial != manifest_outer_terminal:
        changed.append({"surface": "v13_manifest_outer_presence",
                        "before": manifest_outer_initial,
                        "after": manifest_outer_terminal})
    if {str(path) for path in runtime_initial} != {str(path) for path in runtime_terminal}:
        changed.append({"surface": "v13_runtime_presence",
                        "before": [str(path) for path in runtime_initial],
                        "after": [str(path) for path in runtime_terminal]})
    sections["terminal_snapshot"] = {
        "held_file_count": len(held), "changed_file_count": len(changed),
        "changed_files_or_surfaces": changed,
    }
    report.add("terminal_snapshot_changed_file_count_zero", not changed,
               changed_file_count=len(changed), changes=changed)
    return report.finish(sections)


def main() -> None:
    try:
        result = review()
    except Exception as exc:
        result = {
            "schema": "cm2.c79g.v13.independent-read-only-static-review.v1",
            "status": "FAIL_CLOSED_STATIC_REVIEW__RUNTIME_NOT_AUTHORIZED",
            "read_only": True,
            "protocol_python_imported_or_executed": False,
            "protocol_or_runtime_files_written": False,
            "fatal_error": f"{type(exc).__name__}: {exc}",
            "failed_check_count": 1,
            "failed_checks": ["review_completed_without_fatal_error"],
        }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
