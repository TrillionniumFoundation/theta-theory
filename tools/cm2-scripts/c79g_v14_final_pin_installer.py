#!/usr/bin/env python3
"""Fail-closed, source-only final-pin installer for the C79g v14 DAG.

This program never imports or executes a v14 protocol source.  Every command
holds the official ``.cm2-runtime`` directory flock through terminal replay and
unlock.  PREFLIGHT modes are read-only.  INSTALL modes are disabled by default
and require either the corresponding one-shot source flag below or a complete
CLI prehash contract.

The non-crash CORE transaction is deliberately ordered producer then consumer.
It is not crash-atomic across the two inodes.  A process-local failure restores
both held inodes and fsyncs them; a host crash between the two writes leaves a
fail-closed producer-final/consumer-draft state which a later exact-prehash run
may finish.  No persisted receipt is written: the only receipt is stdout JSON.
"""

from __future__ import annotations

import argparse
import ast
import builtins
import copy
import fcntl
import hashlib
import json
import os
import stat
import symtable
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ONE_SHOT_CORE_WRITE_ENABLED = False
ONE_SHOT_LAUNCHER_WRITE_ENABLED = False

BASE = "cm2_round306c79g_true_global_no_producer_consumer"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = OUT / f"{BASE}_schema_v14.json"
CONTRACT = OUT / f"{BASE}_contract_v14.json"
PRODUCER = OUT / f"{BASE}_v14.py"
CONSUMER = OUT / (
    f"{BASE}_independent_verifier_assembler_authority_consumer_v14.py")
TRANSITION = OUT / f"{BASE}_v13_to_v14_static_launch_transition_receipt_v1.json"
AUDIT = OUT / f"{BASE}_static_audit_v14.json"
LAUNCHER = OUT / f"{BASE}_cold_launch_v14.py"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_v14.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_v14.json"
V13_RECEIPT = OUT / (
    f"{BASE}_v13_prepublication_pyc_contamination_rejection_"
    "supersession_receipt_v1.json")

V13_RECEIPT_FILE_SHA256 = (
    "098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f")
V13_RECEIPT_OBJECT_SHA256 = (
    "3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677")

CURRENT_BASE7_KEYS = (
    "SCHEMA", "CONTRACT", "PRODUCER", "CONSUMER", "TRANSITION", "AUDIT")
OBJECT_BASE7_KEYS = frozenset({"CONTRACT", "TRANSITION", "AUDIT"})

CORE_CRASH_BOUNDARY = (
    "NOT_CRASH_ATOMIC_ACROSS_PRODUCER_AND_CONSUMER__PRODUCER_WRITES_FIRST__"
    "A_CRASH_MAY_LEAVE_FINAL_PRODUCER_AND_DRAFT_CONSUMER__THIS_STATE_IS_"
    "FAIL_CLOSED_AND_EXACT_PREHASH_RECOVERABLE")


class Refuse(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def is_sha256(value: Any) -> bool:
    return (isinstance(value, str) and len(value) == 64 and
            all(ch in "0123456789abcdef" for ch in value))


def strict_json(
        raw: bytes, label: str, *, canonical_bytes: bool = False,
) -> dict[str, Any]:
    duplicates: list[str] = []

    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                duplicates.append(key)
            result[key] = value
        return result

    try:
        value = json.loads(raw, object_pairs_hook=hook)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Refuse(label + ": strict JSON parse failed") from exc
    if duplicates:
        raise Refuse(label + ": duplicate JSON keys: " + repr(duplicates))
    if not isinstance(value, dict):
        raise Refuse(label + ": top level is not an object")
    if canonical_bytes and raw != canonical(value) + b"\n":
        raise Refuse(label + ": bytes are not canonical object plus newline")
    if not raw.endswith(b"\n"):
        raise Refuse(label + ": JSON bytes lack terminal newline")
    return value


def object_sha256(value: dict[str, Any], label: str) -> str:
    declared = value.get("object_sha256")
    if not is_sha256(declared):
        raise Refuse(label + ": missing/noncanonical object_sha256")
    body = copy.deepcopy(value)
    del body["object_sha256"]
    actual = sha256(canonical(body))
    if actual != declared:
        raise Refuse(label + ": object_sha256 closure mismatch")
    return actual


def fd_mount_id(fd: int) -> int:
    try:
        text = Path(f"/proc/self/fdinfo/{fd}").read_text()
    except OSError as exc:
        raise Refuse("cannot read held-fd mount identity") from exc
    for line in text.splitlines():
        if line.startswith("mnt_id:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError as exc:
                raise Refuse("invalid held-fd mount identity") from exc
    raise Refuse("held-fd mount identity absent")


def pread_all(fd: int) -> bytes:
    blocks: list[bytes] = []
    offset = 0
    while True:
        block = os.pread(fd, 1 << 20, offset)
        if not block:
            return b"".join(blocks)
        blocks.append(block)
        offset += len(block)


@dataclass
class Held:
    path: Path
    fd: int
    parent_fd: int
    before: os.stat_result
    parent_before: os.stat_result
    mount_id: int
    parent_mount_id: int
    raw: bytes
    writable: bool
    expected_mode: int

    @classmethod
    def open(cls, path: Path, *, writable: bool, expected_mode: int) -> "Held":
        parent_fd = -1
        fd = -1
        try:
            parent_fd = os.open(
                path.parent,
                os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
            flags = os.O_CLOEXEC | os.O_NOFOLLOW | (
                os.O_RDWR if writable else os.O_RDONLY)
            fd = os.open(path.name, flags, dir_fd=parent_fd)
            before = os.fstat(fd)
            parent_before = os.fstat(parent_fd)
            if (not stat.S_ISREG(before.st_mode) or
                    stat.S_IMODE(before.st_mode) != expected_mode or
                    before.st_nlink != 1):
                raise Refuse(
                    f"{path.relative_to(ROOT)}: expected regular "
                    f"{expected_mode:04o}/nlink1")
            if not stat.S_ISDIR(parent_before.st_mode):
                raise Refuse(str(path.parent) + ": held parent is not directory")
            mount_id = fd_mount_id(fd)
            parent_mount_id = fd_mount_id(parent_fd)
            if mount_id != parent_mount_id:
                raise Refuse(str(path) + ": file and parent mount differ")
            raw = pread_all(fd)
            result = cls(
                path, fd, parent_fd, before, parent_before, mount_id,
                parent_mount_id, raw, writable, expected_mode)
            result.revalidate_path_identity()
            return result
        except Exception:
            if fd >= 0:
                os.close(fd)
            if parent_fd >= 0:
                os.close(parent_fd)
            raise

    def revalidate_path_identity(self) -> None:
        try:
            named_parent = os.stat(self.path.parent, follow_symlinks=False)
            current = os.stat(
                self.path.name, dir_fd=self.parent_fd, follow_symlinks=False)
            held = os.fstat(self.fd)
            parent = os.fstat(self.parent_fd)
        except OSError as exc:
            raise Refuse(str(self.path) + ": held/path identity unavailable") from exc
        if ((current.st_dev, current.st_ino) !=
                (held.st_dev, held.st_ino) or
                (named_parent.st_dev, named_parent.st_ino) !=
                (parent.st_dev, parent.st_ino) or
                (parent.st_dev, parent.st_ino) !=
                (self.parent_before.st_dev, self.parent_before.st_ino) or
                not stat.S_ISDIR(named_parent.st_mode) or
                not stat.S_ISDIR(parent.st_mode) or
                not stat.S_ISREG(current.st_mode) or
                not stat.S_ISREG(held.st_mode) or
                stat.S_IMODE(current.st_mode) != self.expected_mode or
                stat.S_IMODE(held.st_mode) != self.expected_mode or
                current.st_nlink != 1 or held.st_nlink != 1 or
                fd_mount_id(self.fd) != self.mount_id or
                fd_mount_id(self.parent_fd) != self.parent_mount_id):
            raise Refuse(str(self.path) + ": held/path identity drift")

    def terminal_replay(self, expected: bytes | None = None) -> bytes:
        self.revalidate_path_identity()
        raw = pread_all(self.fd)
        if expected is not None and raw != expected:
            raise Refuse(str(self.path) + ": held bytes drift")
        return raw

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1
        if self.parent_fd >= 0:
            os.close(self.parent_fd)
            self.parent_fd = -1


def close_all(held: Iterable[Held]) -> None:
    for item in reversed(list(held)):
        item.close()


def same_mount(held: Iterable[Held]) -> None:
    values = list(held)
    if not values or len({item.mount_id for item in values}) != 1:
        raise Refuse("all held DAG inputs must share one mount")


def path_lexists(path: Path) -> bool:
    try:
        os.lstat(path)
        return True
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise Refuse(str(path) + ": cannot establish path absence") from exc


def require_absent(path: Path, label: str) -> None:
    if path_lexists(path):
        raise Refuse(label + " already present (including symlink)")


@dataclass
class OfficialWriterLock:
    fd: int
    before: os.stat_result
    mount_id: int
    owned: bool = False

    @classmethod
    def acquire(cls) -> "OfficialWriterLock":
        try:
            named = os.lstat(RUNTIME)
        except OSError as exc:
            raise Refuse("official runtime directory unavailable") from exc
        if not stat.S_ISDIR(named.st_mode) or stat.S_ISLNK(named.st_mode):
            raise Refuse("official runtime path is not a no-follow directory")
        fd = -1
        try:
            fd = os.open(
                RUNTIME,
                os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
            before = os.fstat(fd)
            if ((named.st_dev, named.st_ino) != (before.st_dev, before.st_ino) or
                    not stat.S_ISDIR(before.st_mode)):
                raise Refuse("official runtime held/path identity mismatch")
            result = cls(fd=fd, before=before, mount_id=fd_mount_id(fd))
            fcntl.flock(fd, fcntl.LOCK_EX)
            result.owned = True
            result.revalidate()
            return result
        except Exception:
            if fd >= 0:
                os.close(fd)
            raise

    def revalidate(self) -> None:
        if not self.owned or self.fd < 0:
            raise Refuse("official writer lock is not owned")
        try:
            named = os.lstat(RUNTIME)
            held = os.fstat(self.fd)
        except OSError as exc:
            raise Refuse("official runtime lock identity unavailable") from exc
        if ((named.st_dev, named.st_ino) != (held.st_dev, held.st_ino) or
                (held.st_dev, held.st_ino) !=
                (self.before.st_dev, self.before.st_ino) or
                not stat.S_ISDIR(named.st_mode) or
                not stat.S_ISDIR(held.st_mode) or
                fd_mount_id(self.fd) != self.mount_id):
            raise Refuse("official runtime lock held/path identity drift")

    def release(self) -> None:
        if self.fd < 0:
            return
        try:
            if self.owned:
                self.revalidate()
                fcntl.flock(self.fd, fcntl.LOCK_UN)
                self.owned = False
        finally:
            os.close(self.fd)
            self.fd = -1


def find_v14_pyc() -> list[str]:
    rows: list[str] = []
    for base in (OUT, ROOT / "scripts"):
        if base.is_dir():
            rows.extend(str(path.relative_to(ROOT)) for path in base.rglob("*.pyc")
                        if "v14" in path.name)
    return sorted(rows)


def runtime_surfaces() -> list[str]:
    if not RUNTIME.is_dir():
        return []
    return sorted(str(path.relative_to(ROOT)) for path in RUNTIME.rglob("*")
                  if "c79g-v14" in path.name.lower())


def require_static_absence() -> None:
    pycs = find_v14_pyc()
    if pycs:
        raise Refuse("v14 pyc present: " + repr(pycs))
    surfaces = runtime_surfaces()
    if surfaces:
        raise Refuse("v14 runtime surface present: " + repr(surfaces))
    require_absent(MANIFEST, "v14 manifest")
    require_absent(OUTER, "v14 outer receipt")


def require_core_phase_absence() -> None:
    require_absent(TRANSITION, "v14 transition")
    require_absent(AUDIT, "v14 audit")


def replay_snapshot(
        held: Iterable[Held],
        replacements: dict[Path, bytes] | None = None,
) -> None:
    replacements = replacements or {}
    for item in held:
        item.terminal_replay(replacements.get(item.path, item.raw))


def iter_symbol_tables(table: symtable.SymbolTable) -> Iterable[symtable.SymbolTable]:
    yield table
    for child in table.get_children():
        yield from iter_symbol_tables(child)


def python_static(raw: bytes, label: str) -> dict[str, Any]:
    try:
        source = raw.decode("utf-8")
        tree = ast.parse(source, filename=label)
        compile(tree, label, "exec")
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Refuse(label + ": AST parse/in-memory compile failed") from exc

    duplicates: list[dict[str, Any]] = []
    dict_count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        dict_count += 1
        seen: dict[tuple[str, str], int] = {}
        for key in node.keys:
            if key is None:
                continue
            try:
                value = ast.literal_eval(key)
            except Exception:
                continue
            token = (type(value).__name__, repr(value))
            if token in seen:
                duplicates.append({
                    "dict_line": node.lineno, "key": repr(value),
                    "first_line": seen[token], "duplicate_line": key.lineno})
            else:
                seen[token] = key.lineno
    if duplicates:
        raise Refuse(label + ": duplicate Python literal dict keys")

    table = symtable.symtable(source, label, "exec")
    module_defined = {
        symbol.get_name() for symbol in table.get_symbols()
        if (symbol.is_assigned() or symbol.is_imported() or
            symbol.is_namespace() or symbol.is_parameter())}
    allowed = module_defined | set(dir(builtins)) | {
        "__file__", "__name__", "__package__", "__spec__", "__loader__",
        "__cached__", "__builtins__", "__doc__", "__annotations__"}
    undefined = sorted({
        symbol.get_name()
        for child in iter_symbol_tables(table)
        for symbol in child.get_symbols()
        if (symbol.is_referenced() and symbol.is_global() and
            symbol.get_name() not in allowed)})
    if undefined:
        raise Refuse(label + ": undefined globals: " + repr(undefined))
    return {"dict_literal_count": dict_count, "duplicate_key_count": 0,
            "undefined_global_count": 0}


def module_assignment(tree: ast.Module, name: str) -> ast.Assign | ast.AnnAssign:
    rows: list[ast.Assign | ast.AnnAssign] = []
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and
                isinstance(node.targets[0], ast.Name) and
                node.targets[0].id == name):
            rows.append(node)
        elif (isinstance(node, ast.AnnAssign) and
              isinstance(node.target, ast.Name) and node.target.id == name):
            rows.append(node)
    if len(rows) != 1:
        raise Refuse(f"expected one module assignment for {name}")
    return rows[0]


def assignment_value(node: ast.Assign | ast.AnnAssign) -> ast.expr:
    if node.value is None:
        raise Refuse("assignment has no value")
    return node.value


def small_eval(node: ast.AST, names: dict[str, Any] | None = None) -> Any:
    names = names or {}
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name) and node.id in names:
        return names[node.id]
    if isinstance(node, ast.Tuple):
        return tuple(small_eval(item, names) for item in node.elts)
    if isinstance(node, ast.List):
        return [small_eval(item, names) for item in node.elts]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        return small_eval(node.left, names) * small_eval(node.right, names)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return small_eval(node.left, names) + small_eval(node.right, names)
    raise Refuse("unsupported static expression: " + ast.dump(node))


def is_exact_repeat(node: ast.AST, unit: str, count: int) -> bool:
    return (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult) and
            isinstance(node.left, ast.Constant) and node.left.value == unit and
            isinstance(node.right, ast.Constant) and node.right.value == count)


def require_exact_constant_tuple(
        node: ast.AST, expected: tuple[str, ...], label: str,
) -> None:
    if (not isinstance(node, ast.Tuple) or len(node.elts) != len(expected) or
            any(not isinstance(item, ast.Constant) or item.value != value
                for item, value in zip(node.elts, expected))):
        raise Refuse(label + ": forbidden sentinel literal tuple changed")


def source_tree(raw: bytes, label: str) -> ast.Module:
    python_static(raw, label)
    return ast.parse(raw.decode("utf-8"), filename=label)


def span(raw: bytes, node: ast.AST) -> tuple[int, int]:
    if not all(hasattr(node, attr) for attr in
               ("lineno", "col_offset", "end_lineno", "end_col_offset")):
        raise Refuse("AST node lacks exact source span")
    lines = raw.splitlines(keepends=True)
    start = sum(len(line) for line in lines[:node.lineno - 1]) + node.col_offset
    end = (sum(len(line) for line in lines[:node.end_lineno - 1]) +
           node.end_col_offset)
    return start, end


def apply_replacements(
        raw: bytes, replacements: list[tuple[ast.AST, bytes]]) -> bytes:
    edits = [(span(raw, node)[0], span(raw, node)[1], value)
             for node, value in replacements]
    edits.sort(reverse=True)
    result = raw
    last_start = len(raw) + 1
    for start, end, value in edits:
        if end > last_start or not (0 <= start < end <= len(raw)):
            raise Refuse("overlapping or invalid AST byte replacement")
        result = result[:start] + value + result[end:]
        last_start = start
    return result


def core_source_state(
        raw: bytes, role: str, pins: dict[str, str]) -> tuple[str, bytes, str]:
    tree = source_tree(raw, role)
    if role == "producer":
        flag_name = "FINAL_V14_CORE_PINS_INSTALLED"
        pin_names = (
            "CONTRACT_FILE_PIN", "CONTRACT_OBJECT_PIN", "CLOSED_SCHEMA_FILE_PIN")
        expected = (
            pins["contract_file"], pins["contract_object"], pins["schema_file"])
        draft = ("d0" * 32, "e0" * 32, "f0" * 32)
        sentinel_name = "V14_DRAFT_CORE_PIN_SENTINELS"
    elif role == "consumer":
        flag_name = "FINAL_CURRENT_V14_PINS_INSTALLED"
        pin_names = (
            "CONTRACT_FILE_PIN", "CONTRACT_OBJECT_PIN", "CLOSED_SCHEMA_FILE_PIN",
            "PRODUCER_SOURCE_PIN")
        expected = (
            pins["contract_file"], pins["contract_object"], pins["schema_file"],
            pins["producer_file"])
        draft = ("d9" * 32, "e9" * 32, "f9" * 32, "a9" * 32)
        sentinel_name = "V14_DRAFT_CURRENT_CORE_PINS"
    else:
        raise Refuse("unknown core role")

    flag_node = module_assignment(tree, flag_name)
    flag_value_node = assignment_value(flag_node)
    flag = small_eval(flag_value_node)
    if (not isinstance(flag_value_node, ast.Constant) or
            type(flag_value_node.value) is not bool):
        raise Refuse(role + ": final flag is not an exact bool literal")
    pin_value_nodes = tuple(
        assignment_value(module_assignment(tree, name)) for name in pin_names)
    values = tuple(small_eval(node) for node in pin_value_nodes)
    sentinel_value_node = assignment_value(
        module_assignment(tree, sentinel_name))
    require_exact_constant_tuple(
        sentinel_value_node, draft, role + " sentinel declaration")
    if any(value in draft for value in expected):
        raise Refuse(role + ": final DAG pin collides with a draft sentinel")
    if flag is False and values == draft:
        if any(not is_exact_repeat(node, value[:2], 32)
               for node, value in zip(pin_value_nodes, draft)):
            raise Refuse(role + ": draft pin expression is not exact")
        state = "DRAFT"
    elif flag is True and values == expected:
        if any(not isinstance(node, ast.Constant) or node.value != value
               for node, value in zip(pin_value_nodes, expected)):
            raise Refuse(role + ": final pin is not an exact string literal")
        state = "FINAL"
    else:
        raise Refuse(role + ": mixed, stale, or unrecognized pin state")
    if state == "FINAL":
        proposed = raw
    else:
        replacements: list[tuple[ast.AST, bytes]] = [
            (assignment_value(flag_node), b"True")]
        replacements.extend(
            (assignment_value(module_assignment(tree, name)),
             json.dumps(value).encode("ascii"))
            for name, value in zip(pin_names, expected))
        proposed = apply_replacements(raw, replacements)
    post_tree = source_tree(proposed, role + " proposed")
    post_flag = assignment_value(module_assignment(post_tree, flag_name))
    if (not isinstance(post_flag, ast.Constant) or post_flag.value is not True):
        raise Refuse(role + ": proposed final flag did not close")
    post_nodes = tuple(assignment_value(module_assignment(post_tree, name))
                       for name in pin_names)
    post_values = tuple(small_eval(node) for node in post_nodes)
    if post_values != expected:
        raise Refuse(role + ": proposed pins do not equal DAG inputs")
    if any(not isinstance(node, ast.Constant) or node.value != value
           for node, value in zip(post_nodes, expected)):
        raise Refuse(role + ": proposed pins are not exact string literals")
    require_exact_constant_tuple(
        assignment_value(module_assignment(post_tree, sentinel_name)),
        draft, role + " proposed sentinel declaration")
    return state, proposed, sha256(proposed)


def validate_launcher_receipt_first_pin(
        tree: ast.Module, mapping: ast.Dict, label: str,
) -> None:
    file_node = assignment_value(module_assignment(
        tree, "V13_SUPERSESSION_RECEIPT_FILE_PIN"))
    object_node = assignment_value(module_assignment(
        tree, "V13_SUPERSESSION_RECEIPT_OBJECT_PIN"))
    if (not isinstance(file_node, ast.Constant) or
            not isinstance(object_node, ast.Constant) or
            file_node.value != V13_RECEIPT_FILE_SHA256 or
            object_node.value != V13_RECEIPT_OBJECT_SHA256):
        raise Refuse(label + ": v13 receipt constant literal pins mismatch")
    first = mapping.values[0]
    if (not isinstance(first, ast.Tuple) or len(first.elts) != 2 or
            not isinstance(first.elts[0], ast.Name) or
            first.elts[0].id != "V13_SUPERSESSION_RECEIPT_FILE_PIN" or
            not isinstance(first.elts[1], ast.Name) or
            first.elts[1].id != "V13_SUPERSESSION_RECEIPT_OBJECT_PIN"):
        raise Refuse(label + ": receipt-first tuple is not the exact fixed pin pair")


def require_launcher_current_pin_ast(
        mapping: ast.Dict, names: list[str | None],
        base7: dict[str, tuple[str, str | None]], state: str, label: str,
) -> None:
    for index, name in enumerate(names[1:], start=1):
        if name is None:
            raise Refuse(label + ": non-name BASE7 key")
        node = mapping.values[index]
        if not isinstance(node, ast.Tuple) or len(node.elts) != 2:
            raise Refuse(label + ": BASE7 pin row is not an exact pair")
        if state == "DRAFT":
            expected_object_name = (
                "_DRAFT_OBJECT_PIN" if name in OBJECT_BASE7_KEYS else None)
            if (not isinstance(node.elts[0], ast.Name) or
                    node.elts[0].id != "_DRAFT_FILE_PIN" or
                    (expected_object_name is None and not (
                        isinstance(node.elts[1], ast.Constant) and
                        node.elts[1].value is None)) or
                    (expected_object_name is not None and not (
                        isinstance(node.elts[1], ast.Name) and
                        node.elts[1].id == expected_object_name))):
                raise Refuse(label + ": draft BASE7 pin expression changed")
        else:
            expected = base7[name]
            if any(not isinstance(item, ast.Constant) or item.value != value
                   for item, value in zip(node.elts, expected)):
                raise Refuse(label + ": final BASE7 pin literals mismatch")


def pin_normalized_launcher_ast(raw: bytes, label: str) -> str:
    tree = source_tree(raw, label)
    flag = module_assignment(tree, "FINAL_BASE7_PINS_INSTALLED")
    flag.value = ast.Constant(value=False)
    funcs = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
             node.name == "configure_workspace_paths"]
    if len(funcs) != 1:
        raise Refuse(label + ": configure_workspace_paths not unique")
    rows = [node for node in funcs[0].body
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and
            isinstance(node.targets[0], ast.Name) and
            node.targets[0].id == "BASE7_PINS"]
    if len(rows) != 1 or not isinstance(rows[0].value, ast.Dict):
        raise Refuse(label + ": BASE7_PINS direct dict not unique")
    value = rows[0].value
    key_names = [key.id if isinstance(key, ast.Name) else None
                 for key in value.keys]
    expected_keys = ["V13_SUPERSESSION_RECEIPT", *CURRENT_BASE7_KEYS]
    if key_names != expected_keys or len(value.values) != 7:
        raise Refuse(label + ": receipt-first BASE7 order mismatch")
    validate_launcher_receipt_first_pin(tree, value, label)
    receipt_before = ast.dump(value.values[0], include_attributes=False)
    for index, key in enumerate(key_names[1:], start=1):
        value.values[index] = ast.Tuple(elts=[
            ast.Constant(value="f" * 64),
            ast.Constant(value="e" * 64 if key in OBJECT_BASE7_KEYS else None),
        ], ctx=ast.Load())
    if ast.dump(value.values[0], include_attributes=False) != receipt_before:
        raise Refuse(label + ": normalizer changed v13 receipt pin")
    return sha256(ast.dump(
        tree, annotate_fields=True, include_attributes=False).encode("utf-8"))


def launcher_state(
        raw: bytes,
        base7: dict[str, tuple[str, str | None]],
) -> tuple[str, bytes, str, str]:
    tree = source_tree(raw, "launcher")
    draft_file_node = assignment_value(
        module_assignment(tree, "_DRAFT_FILE_PIN"))
    draft_object_node = assignment_value(
        module_assignment(tree, "_DRAFT_OBJECT_PIN"))
    draft_file = small_eval(draft_file_node)
    draft_object = small_eval(draft_object_node)
    if draft_file != "f" * 64 or draft_object != "e" * 64:
        raise Refuse("launcher forbidden draft sentinel values changed")
    if (not is_exact_repeat(draft_file_node, "f", 64) or
            not is_exact_repeat(draft_object_node, "e", 64)):
        raise Refuse("launcher forbidden draft sentinel expressions changed")
    flag_node = module_assignment(tree, "FINAL_BASE7_PINS_INSTALLED")
    flag_value_node = assignment_value(flag_node)
    flag = small_eval(flag_value_node)
    if (not isinstance(flag_value_node, ast.Constant) or
            type(flag_value_node.value) is not bool):
        raise Refuse("launcher final flag is not an exact bool literal")
    funcs = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
             node.name == "configure_workspace_paths"]
    if len(funcs) != 1:
        raise Refuse("launcher configure_workspace_paths not unique")
    assignments = [node for node in funcs[0].body
                   if isinstance(node, ast.Assign) and len(node.targets) == 1 and
                   isinstance(node.targets[0], ast.Name) and
                   node.targets[0].id == "BASE7_PINS"]
    if len(assignments) != 1 or not isinstance(assignments[0].value, ast.Dict):
        raise Refuse("launcher BASE7_PINS direct dict not unique")
    mapping = assignments[0].value
    names = [key.id if isinstance(key, ast.Name) else None for key in mapping.keys]
    if names != ["V13_SUPERSESSION_RECEIPT", *CURRENT_BASE7_KEYS]:
        raise Refuse("launcher BASE7 is not receipt-first exact7")
    validate_launcher_receipt_first_pin(tree, mapping, "launcher")
    constants = {"_DRAFT_FILE_PIN": draft_file, "_DRAFT_OBJECT_PIN": draft_object}
    current = {
        name: small_eval(mapping.values[index], constants)
        for index, name in enumerate(names[1:], start=1)}
    expected_draft = {
        name: (draft_file, draft_object if name in OBJECT_BASE7_KEYS else None)
        for name in CURRENT_BASE7_KEYS}
    if flag is False and current == expected_draft:
        state = "DRAFT"
    elif flag is True and current == base7:
        state = "FINAL"
    else:
        raise Refuse("launcher mixed, stale, or unrecognized BASE7 state")
    require_launcher_current_pin_ast(
        mapping, names, base7, state, "launcher " + state.lower())
    normalized_before = pin_normalized_launcher_ast(raw, "launcher pre")
    if state == "FINAL":
        proposed = raw
    else:
        replacements: list[tuple[ast.AST, bytes]] = [
            (assignment_value(flag_node), b"True")]
        for index, name in enumerate(names[1:], start=1):
            replacements.append((
                mapping.values[index],
                repr(base7[name]).encode("ascii")))
        proposed = apply_replacements(raw, replacements)
    post_tree = source_tree(proposed, "launcher proposed")
    post_draft_file = assignment_value(
        module_assignment(post_tree, "_DRAFT_FILE_PIN"))
    post_draft_object = assignment_value(
        module_assignment(post_tree, "_DRAFT_OBJECT_PIN"))
    if (not is_exact_repeat(post_draft_file, "f", 64) or
            not is_exact_repeat(post_draft_object, "e", 64)):
        raise Refuse("launcher proposal modified forbidden sentinels")
    post_flag = assignment_value(module_assignment(
        post_tree, "FINAL_BASE7_PINS_INSTALLED"))
    if not isinstance(post_flag, ast.Constant) or post_flag.value is not True:
        raise Refuse("launcher proposed final flag is not exact True literal")
    post_funcs = [node for node in post_tree.body
                  if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and
                  node.name == "configure_workspace_paths"]
    post_assignments = [node for node in post_funcs[0].body
                        if isinstance(node, ast.Assign) and
                        len(node.targets) == 1 and
                        isinstance(node.targets[0], ast.Name) and
                        node.targets[0].id == "BASE7_PINS"]
    if len(post_assignments) != 1 or not isinstance(
            post_assignments[0].value, ast.Dict):
        raise Refuse("launcher proposed BASE7 direct dict not unique")
    post_mapping = post_assignments[0].value
    validate_launcher_receipt_first_pin(
        post_tree, post_mapping, "launcher proposed")
    require_launcher_current_pin_ast(
        post_mapping, names, base7, "FINAL", "launcher proposed")
    normalized_after = pin_normalized_launcher_ast(proposed, "launcher proposed")
    if normalized_before != normalized_after:
        raise Refuse("PIN_NORMALIZED launcher AST changed across injection")
    return state, proposed, sha256(proposed), normalized_before


def read_json_held(path: Path, label: str) -> tuple[Held, dict[str, Any], str, str | None]:
    held = Held.open(path, writable=False, expected_mode=0o664)
    try:
        value = strict_json(held.raw, label)
        obj = object_sha256(value, label) if "object_sha256" in value else None
        return held, value, sha256(held.raw), obj
    except Exception:
        held.close()
        raise


def validate_schema_contract(
        schema: dict[str, Any], schema_hash: str,
        contract: dict[str, Any], contract_hash: str,
        contract_object: str) -> None:
    if not isinstance(schema.get("$defs"), dict):
        raise Refuse("schema: closed $defs mapping absent")
    bundle = contract.get("v14_bundle")
    if not isinstance(bundle, dict):
        raise Refuse("contract: v14_bundle absent")
    closed = bundle.get("closed_schema")
    if not isinstance(closed, dict) or closed.get("file_sha256") != schema_hash:
        raise Refuse("contract does not bind current schema bytes")
    if not is_sha256(contract_hash) or not is_sha256(contract_object):
        raise Refuse("contract pins are not canonical sha256")


def open_core(*, writable: bool) -> tuple[list[Held], dict[str, Any]]:
    held: list[Held] = []
    try:
        schema_h, schema, schema_file, _ = read_json_held(SCHEMA, "v14 schema")
        held.append(schema_h)
        contract_h, contract, contract_file, contract_object = read_json_held(
            CONTRACT, "v14 contract")
        held.append(contract_h)
        if contract_object is None:
            raise Refuse("v14 contract lacks object closure")
        validate_schema_contract(
            schema, schema_file, contract, contract_file, contract_object)
        require_core_phase_absence()
        producer = Held.open(PRODUCER, writable=writable, expected_mode=0o664)
        consumer = Held.open(CONSUMER, writable=writable, expected_mode=0o664)
        held.extend((producer, consumer))
        same_mount(held)
        pins = {"schema_file": schema_file, "contract_file": contract_file,
                "contract_object": contract_object}
        p_state, p_new, p_new_hash = core_source_state(
            producer.raw, "producer", pins)
        pins["producer_file"] = p_new_hash
        c_state, c_new, c_new_hash = core_source_state(
            consumer.raw, "consumer", pins)
        return held, {
            "pins": pins,
            "producer_state": p_state,
            "consumer_state": c_state,
            "producer_pre_sha256": sha256(producer.raw),
            "consumer_pre_sha256": sha256(consumer.raw),
            "producer_post_sha256": p_new_hash,
            "consumer_post_sha256": c_new_hash,
            "producer_new": p_new,
            "consumer_new": c_new,
        }
    except Exception:
        close_all(held)
        raise


def validate_transition_audit_bindings(
        transition: dict[str, Any], audit: dict[str, Any],
        hashes: dict[str, str]) -> None:
    successor = transition.get("successor_v14_static_bundle")
    audited = audit.get("audited_v14_bundle")
    if not isinstance(successor, dict) or not isinstance(audited, dict):
        raise Refuse("transition/audit current bundle binding absent")

    expected = {
        "closed_schema": (SCHEMA, hashes["SCHEMA"], None),
        "contract": (CONTRACT, hashes["CONTRACT"], hashes["CONTRACT_OBJECT"]),
        "build_only_producer": (PRODUCER, hashes["PRODUCER"], None),
        "independent_verifier_assembler_authority_consumer": (
            CONSUMER, hashes["CONSUMER"], None),
    }
    for key, (path, file_pin, object_pin) in expected.items():
        row = successor.get(key)
        if not isinstance(row, dict) or row.get("path") != str(path.relative_to(ROOT)) \
                or row.get("file_sha256") != file_pin:
            raise Refuse("transition stale binding: " + key)
        if object_pin is not None and row.get("object_sha256") != object_pin:
            raise Refuse("transition stale object binding: " + key)
        audit_row = audited.get(key)
        if not isinstance(audit_row, dict) or audit_row.get("path") != \
                str(path.relative_to(ROOT)) or audit_row.get("file_sha256") != file_pin:
            raise Refuse("audit stale binding: " + key)
        if object_pin is not None and audit_row.get("object_sha256") != object_pin:
            raise Refuse("audit stale object binding: " + key)

    transition_row = audited.get("v13_to_v14_transition_receipt")
    if (not isinstance(transition_row, dict) or
            transition_row.get("path") != str(TRANSITION.relative_to(ROOT)) or
            transition_row.get("file_sha256") != hashes["TRANSITION"] or
            transition_row.get("object_sha256") != hashes["TRANSITION_OBJECT"]):
        raise Refuse("audit does not bind current transition")

    dual = audit.get("dual_independent_static_checkers")
    if not isinstance(dual, dict):
        raise Refuse("audit dual checker proof absent")
    expected_normalized = hashes["LAUNCHER_PIN_NORMALIZED"]
    found = []
    for value in dual.values():
        if isinstance(value, dict) and "pin_normalized_launcher_ast_sha256" in value:
            found.append(value["pin_normalized_launcher_ast_sha256"])
    if not found or any(value != expected_normalized for value in found):
        raise Refuse("audit launcher PIN_NORMALIZED binding mismatch")


def open_launcher(*, writable: bool) -> tuple[list[Held], dict[str, Any]]:
    held: list[Held] = []
    try:
        for path, label in ((SCHEMA, "v14 schema"), (CONTRACT, "v14 contract"),
                            (TRANSITION, "v14 transition"), (AUDIT, "v14 audit")):
            item, value, file_hash, obj_hash = read_json_held(path, label)
            held.append(item)
            if path in (CONTRACT, TRANSITION, AUDIT) and obj_hash is None:
                raise Refuse(label + ": object closure absent")
            if path == SCHEMA:
                schema, schema_file = value, file_hash
            elif path == CONTRACT:
                contract, contract_file, contract_object = value, file_hash, obj_hash
            elif path == TRANSITION:
                transition, transition_file, transition_object = value, file_hash, obj_hash
            else:
                audit, audit_file, audit_object = value, file_hash, obj_hash
        validate_schema_contract(
            schema, schema_file, contract, contract_file, str(contract_object))

        producer = Held.open(PRODUCER, writable=False, expected_mode=0o664)
        consumer = Held.open(CONSUMER, writable=False, expected_mode=0o664)
        launcher = Held.open(LAUNCHER, writable=writable, expected_mode=0o664)
        receipt = Held.open(V13_RECEIPT, writable=False, expected_mode=0o444)
        held.extend((producer, consumer, launcher, receipt))
        same_mount(held)
        receipt_value = strict_json(
            receipt.raw, "v13 supersession receipt", canonical_bytes=True)
        if (sha256(receipt.raw) != V13_RECEIPT_FILE_SHA256 or
                object_sha256(receipt_value, "v13 supersession receipt") !=
                V13_RECEIPT_OBJECT_SHA256):
            raise Refuse("v13 supersession receipt pin mismatch")

        core_pins = {"schema_file": schema_file, "contract_file": contract_file,
                     "contract_object": str(contract_object)}
        p_state, p_same, p_hash = core_source_state(
            producer.raw, "producer", core_pins)
        if p_state != "FINAL" or p_same != producer.raw:
            raise Refuse("launcher stage requires final producer")
        core_pins["producer_file"] = p_hash
        c_state, c_same, c_hash = core_source_state(
            consumer.raw, "consumer", core_pins)
        if c_state != "FINAL" or c_same != consumer.raw:
            raise Refuse("launcher stage requires final consumer")

        hashes = {
            "SCHEMA": schema_file,
            "CONTRACT": contract_file,
            "CONTRACT_OBJECT": str(contract_object),
            "PRODUCER": p_hash,
            "CONSUMER": c_hash,
            "TRANSITION": transition_file,
            "TRANSITION_OBJECT": str(transition_object),
            "AUDIT": audit_file,
            "AUDIT_OBJECT": str(audit_object),
            "LAUNCHER_PIN_NORMALIZED": pin_normalized_launcher_ast(
                launcher.raw, "launcher held"),
        }
        validate_transition_audit_bindings(transition, audit, hashes)
        base7 = {
            "SCHEMA": (schema_file, None),
            "CONTRACT": (contract_file, str(contract_object)),
            "PRODUCER": (p_hash, None),
            "CONSUMER": (c_hash, None),
            "TRANSITION": (transition_file, str(transition_object)),
            "AUDIT": (audit_file, str(audit_object)),
        }
        state, proposed, post_hash, normalized = launcher_state(launcher.raw, base7)
        if normalized != hashes["LAUNCHER_PIN_NORMALIZED"]:
            raise Refuse("launcher normalized hash drift during proposal")
        return held, {
            "hashes": hashes,
            "base7": base7,
            "launcher_state": state,
            "launcher_pre_sha256": sha256(launcher.raw),
            "launcher_post_sha256": post_hash,
            "launcher_pin_normalized_ast_sha256": normalized,
            "launcher_new": proposed,
        }
    except Exception:
        close_all(held)
        raise


def write_held(
        item: Held, raw: bytes, *, expected_before: bytes | None = None,
) -> None:
    if not item.writable:
        raise Refuse(str(item.path) + ": held fd is read-only")
    if expected_before is None:
        item.revalidate_path_identity()
    else:
        item.terminal_replay(expected_before)
    offset = 0
    while offset < len(raw):
        written = os.pwrite(item.fd, raw[offset:offset + (1 << 20)], offset)
        if written <= 0:
            raise OSError("short/zero pwrite")
        offset += written
    os.ftruncate(item.fd, len(raw))
    os.fsync(item.fd)
    item.revalidate_path_identity()
    if pread_all(item.fd) != raw:
        raise Refuse(str(item.path) + ": post-write replay mismatch")


def fsync_parents(items: Iterable[Held]) -> None:
    seen: set[tuple[int, int]] = set()
    for item in items:
        info = os.fstat(item.parent_fd)
        identity = (info.st_dev, info.st_ino)
        if identity not in seen:
            os.fsync(item.parent_fd)
            seen.add(identity)


def contract_value(args: argparse.Namespace, name: str) -> str | None:
    return getattr(args, name, None)


def require_exact_contract(
        args: argparse.Namespace, expected: dict[str, str], enabled: bool) -> str:
    supplied = {name: contract_value(args, name) for name in expected}
    present = [value is not None for value in supplied.values()]
    if enabled and not any(present):
        return "SOURCE_ONE_SHOT_ENABLE_FLAG"
    if not all(present):
        raise Refuse(
            "write disabled: provide the complete exact expected-prehash contract")
    mismatches = {
        name: {"expected": expected[name], "supplied": supplied[name]}
        for name in expected if supplied[name] != expected[name]}
    if mismatches:
        raise Refuse("exact expected-prehash contract mismatch: " +
                     canonical(mismatches).decode("utf-8"))
    return "EXPLICIT_EXACT_EXPECTED_PREHASH_CONTRACT"


def core_result(info: dict[str, Any], status: str) -> dict[str, Any]:
    return {
        "schema": "cm2.c79g.v14.final-pin-installer.core-result.v1",
        "status": status,
        "stage": "CORE__S_TO_C_TO_P_TO_CONSUMER",
        "write_performed": False,
        "producer_state": info["producer_state"],
        "consumer_state": info["consumer_state"],
        "pre_sha256": {
            "schema": info["pins"]["schema_file"],
            "contract_file": info["pins"]["contract_file"],
            "contract_object": info["pins"]["contract_object"],
            "producer": info["producer_pre_sha256"],
            "consumer": info["consumer_pre_sha256"],
        },
        "proposed_post_sha256": {
            "producer": info["producer_post_sha256"],
            "consumer": info["consumer_post_sha256"],
        },
        "transition_and_audit_absent": True,
        "v14_pyc_count": 0,
        "runtime_surface_count": 0,
        "core_noncrash_atomicity_boundary": CORE_CRASH_BOUNDARY,
    }


def launcher_result(info: dict[str, Any], status: str) -> dict[str, Any]:
    return {
        "schema": "cm2.c79g.v14.final-pin-installer.launcher-result.v1",
        "status": status,
        "stage": "LAUNCHER__T_TO_A_TO_L",
        "write_performed": False,
        "launcher_state": info["launcher_state"],
        "base7": {
            key: {"file_sha256": value[0], "object_sha256": value[1]}
            for key, value in info["base7"].items()},
        "launcher_pre_sha256": info["launcher_pre_sha256"],
        "launcher_proposed_post_sha256": info["launcher_post_sha256"],
        "pin_normalized_launcher_ast_sha256":
            info["launcher_pin_normalized_ast_sha256"],
        "pin_normalized_pre_post_identical": True,
        "v13_receipt_is_immutable_first_base7_member": True,
        "v14_pyc_count": 0,
        "runtime_surface_count": 0,
    }


def preflight_core() -> dict[str, Any]:
    require_static_absence()
    require_core_phase_absence()
    held, info = open_core(writable=False)
    try:
        replay_snapshot(held)
        require_core_phase_absence()
        require_static_absence()
        status = ("PREFLIGHT_CORE_ALREADY_INSTALLED" if
                  info["producer_state"] == info["consumer_state"] == "FINAL"
                  else "PREFLIGHT_CORE_PASS__INSTALL_NOT_EXECUTED")
        return core_result(info, status)
    finally:
        close_all(held)


def install_core(args: argparse.Namespace) -> dict[str, Any]:
    require_static_absence()
    require_core_phase_absence()
    held, info = open_core(writable=True)
    targets = held[-2:]
    originals = [item.raw for item in targets]
    commit_started = False
    try:
        expected_contract = {
            "expect_schema_file_sha256": info["pins"]["schema_file"],
            "expect_contract_file_sha256": info["pins"]["contract_file"],
            "expect_contract_object_sha256": info["pins"]["contract_object"],
            "expect_producer_pre_sha256": info["producer_pre_sha256"],
            "expect_consumer_pre_sha256": info["consumer_pre_sha256"],
        }
        authority = require_exact_contract(
            args, expected_contract, ONE_SHOT_CORE_WRITE_ENABLED)
        replay_snapshot(held)
        require_core_phase_absence()
        require_static_absence()
        if info["producer_state"] == info["consumer_state"] == "FINAL":
            result = core_result(info, "INSTALL_CORE_IDEMPOTENT_ALREADY_INSTALLED")
            result["authorization"] = authority
            return result
        if info["consumer_state"] == "FINAL" and info["producer_state"] != "FINAL":
            raise Refuse("invalid reverse partial state: consumer final before producer")
        commit_started = True
        write_held(
            targets[0], info["producer_new"], expected_before=targets[0].raw)
        replay_snapshot(held, {PRODUCER: info["producer_new"]})
        require_core_phase_absence()
        require_static_absence()
        write_held(
            targets[1], info["consumer_new"], expected_before=targets[1].raw)
        replay_snapshot(held, {
            PRODUCER: info["producer_new"],
            CONSUMER: info["consumer_new"],
        })
        require_core_phase_absence()
        require_static_absence()
        fsync_parents(targets)
        replay_snapshot(held, {
            PRODUCER: info["producer_new"],
            CONSUMER: info["consumer_new"],
        })
        require_core_phase_absence()
        require_static_absence()
        result = core_result(info, "INSTALL_CORE_PASS__STDOUT_RECEIPT_ONLY")
        result["write_performed"] = True
        result["authorization"] = authority
        result["post_sha256"] = {
            "producer": sha256(targets[0].terminal_replay(info["producer_new"])),
            "consumer": sha256(targets[1].terminal_replay(info["consumer_new"])),
        }
        result["rollback_required"] = False
        return result
    except Exception as exc:
        rollback = {"attempted": commit_started, "restored": False,
                    "error": None}
        if commit_started:
            try:
                for item, original in zip(targets, originals):
                    write_held(item, original)
                fsync_parents(targets)
                replay_snapshot(held)
                require_core_phase_absence()
                require_static_absence()
                rollback["restored"] = True
            except Exception as restore_exc:
                rollback["error"] = type(restore_exc).__name__ + ":" + str(restore_exc)
        raise Refuse(str(exc) + " | rollback=" +
                     canonical(rollback).decode("utf-8")) from exc
    finally:
        close_all(held)


def preflight_launcher() -> dict[str, Any]:
    require_static_absence()
    held, info = open_launcher(writable=False)
    try:
        replay_snapshot(held)
        require_static_absence()
        status = ("PREFLIGHT_LAUNCHER_ALREADY_INSTALLED" if
                  info["launcher_state"] == "FINAL" else
                  "PREFLIGHT_LAUNCHER_PASS__INSTALL_NOT_EXECUTED")
        return launcher_result(info, status)
    finally:
        close_all(held)


def install_launcher(args: argparse.Namespace) -> dict[str, Any]:
    require_static_absence()
    held, info = open_launcher(writable=True)
    target = next(item for item in held if item.path == LAUNCHER)
    original = target.raw
    commit_started = False
    try:
        hashes = info["hashes"]
        expected_contract = {
            "expect_schema_file_sha256": hashes["SCHEMA"],
            "expect_contract_file_sha256": hashes["CONTRACT"],
            "expect_contract_object_sha256": hashes["CONTRACT_OBJECT"],
            "expect_producer_pre_sha256": hashes["PRODUCER"],
            "expect_consumer_pre_sha256": hashes["CONSUMER"],
            "expect_transition_file_sha256": hashes["TRANSITION"],
            "expect_transition_object_sha256": hashes["TRANSITION_OBJECT"],
            "expect_audit_file_sha256": hashes["AUDIT"],
            "expect_audit_object_sha256": hashes["AUDIT_OBJECT"],
            "expect_launcher_pre_sha256": info["launcher_pre_sha256"],
            "expect_launcher_pin_normalized_sha256":
                info["launcher_pin_normalized_ast_sha256"],
        }
        authority = require_exact_contract(
            args, expected_contract, ONE_SHOT_LAUNCHER_WRITE_ENABLED)
        replay_snapshot(held)
        require_static_absence()
        if info["launcher_state"] == "FINAL":
            result = launcher_result(
                info, "INSTALL_LAUNCHER_IDEMPOTENT_ALREADY_INSTALLED")
            result["authorization"] = authority
            return result
        commit_started = True
        write_held(
            target, info["launcher_new"], expected_before=target.raw)
        replay_snapshot(held, {LAUNCHER: info["launcher_new"]})
        require_static_absence()
        fsync_parents([target])
        replay_snapshot(held, {LAUNCHER: info["launcher_new"]})
        require_static_absence()
        if pin_normalized_launcher_ast(
                target.terminal_replay(), "launcher installed") != \
                info["launcher_pin_normalized_ast_sha256"]:
            raise Refuse("installed launcher PIN_NORMALIZED replay mismatch")
        require_static_absence()
        result = launcher_result(
            info, "INSTALL_LAUNCHER_PASS__STDOUT_RECEIPT_ONLY")
        result["write_performed"] = True
        result["authorization"] = authority
        result["launcher_post_sha256"] = sha256(
            target.terminal_replay(info["launcher_new"]))
        result["rollback_required"] = False
        return result
    except Exception as exc:
        rollback = {"attempted": commit_started, "restored": False,
                    "error": None}
        if commit_started:
            try:
                write_held(target, original)
                fsync_parents([target])
                replay_snapshot(held)
                require_static_absence()
                rollback["restored"] = True
            except Exception as restore_exc:
                rollback["error"] = type(restore_exc).__name__ + ":" + str(restore_exc)
        raise Refuse(str(exc) + " | rollback=" +
                     canonical(rollback).decode("utf-8")) from exc
    finally:
        close_all(held)


def add_contract_args(parser: argparse.ArgumentParser) -> None:
    for name in (
            "schema-file-sha256", "contract-file-sha256",
            "contract-object-sha256", "producer-pre-sha256",
            "consumer-pre-sha256", "transition-file-sha256",
            "transition-object-sha256", "audit-file-sha256",
            "audit-object-sha256", "launcher-pre-sha256",
            "launcher-pin-normalized-sha256"):
        parser.add_argument("--expect-" + name, default=None)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="C79g v14 fail-closed final-pin installer")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("PREFLIGHT_CORE")
    core = sub.add_parser("INSTALL_CORE")
    add_contract_args(core)
    sub.add_parser("PREFLIGHT_LAUNCHER")
    launcher = sub.add_parser("INSTALL_LAUNCHER")
    add_contract_args(launcher)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    official_lock: OfficialWriterLock | None = None
    try:
        official_lock = OfficialWriterLock.acquire()
        if args.command == "PREFLIGHT_CORE":
            result = preflight_core()
        elif args.command == "INSTALL_CORE":
            result = install_core(args)
        elif args.command == "PREFLIGHT_LAUNCHER":
            result = preflight_launcher()
        elif args.command == "INSTALL_LAUNCHER":
            result = install_launcher(args)
        else:
            raise Refuse("unknown command")
        official_lock.revalidate()
        result["official_writer_coordination_lock"] = {
            "api": "fcntl.flock(LOCK_EX)",
            "held_for_entire_command": True,
            "runtime_directory_st_dev": official_lock.before.st_dev,
            "runtime_directory_st_ino": official_lock.before.st_ino,
            "runtime_directory_mount_id": official_lock.mount_id,
            "held_path_identity_terminally_revalidated_before_unlock": True,
        }
        official_lock.release()
        official_lock = None
        result["installer_file_sha256"] = sha256(Path(__file__).read_bytes())
        result["success"] = True
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 0
    except Exception as exc:
        cleanup_error: str | None = None
        if official_lock is not None and official_lock.fd >= 0:
            try:
                official_lock.release()
            except Exception as cleanup_exc:
                cleanup_error = type(cleanup_exc).__name__ + ":" + str(cleanup_exc)
        failure = {
            "schema": "cm2.c79g.v14.final-pin-installer.failure.v1",
            "status": "FAIL_CLOSED__NO_RUNTIME_AUTHORIZATION",
            "command": args.command,
            "success": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "write_enable_flags": {
                "core": ONE_SHOT_CORE_WRITE_ENABLED,
                "launcher": ONE_SHOT_LAUNCHER_WRITE_ENABLED,
            },
            "core_noncrash_atomicity_boundary": CORE_CRASH_BOUNDARY,
            "installer_file_sha256": sha256(Path(__file__).read_bytes()),
        }
        if cleanup_error is not None:
            failure["official_lock_cleanup_error"] = cleanup_error
        sys.stdout.buffer.write(canonical(failure) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
