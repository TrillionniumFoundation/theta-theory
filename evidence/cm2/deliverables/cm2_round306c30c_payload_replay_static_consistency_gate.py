#!/usr/bin/env python3
"""Static exact-tree/consumer consistency gate for the C30c payload replay.

The gate reads the pinned outer verifier as inert AST.  It proves that the
literal ``PAYLOAD_REPLAY_FILES`` exact-tree contract is identical to every
literal ``small[...]`` and ``captures[...]`` file consumed by
``validate_payload_replay``.  It grants no formal credit and writes nothing.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parent.parent
OUTER = (
    WORKSPACE / "deliverables"
    / "cm2_round306c30c_source_w_full_delta_whole_origin_disposition_"
      "formal_handoff_outer_verifier.py"
)
OUTER_SHA256 = "0e3d7922c5d47134500b2e1dd337a947669dac724166ed2fbd6d9ef0959e1e68"
EXPECTED = frozenset({
    "exit.txt", "manifest_post.raw", "manifest_pre.raw", "provenance.json",
    "sealed_post.sha256.raw", "sealed_pre.sha256.raw", "stderr.raw",
    "stdout.raw", "time.raw", "trace.raw", "trace_audit.json",
})


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def capture(path: Path) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical outer path")
    descriptor = os.open(
        absolute, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 < before.st_size <= 4 << 20,
            "bounded regular outer verifier",
        )
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            need(bool(block), "complete outer read")
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "stable outer EOF")
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    fields = lambda value: (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )
    need(fields(before) == fields(after), "stable outer capture")
    return b"".join(chunks)


def literal_file_set(node: ast.AST) -> set[str]:
    if isinstance(node, ast.Constant) and type(node.value) is str:
        return {node.value}
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        output: set[str] = set()
        for element in node.elts:
            output.update(literal_file_set(element))
        return output
    if (
        isinstance(node, ast.Call) and len(node.args) == 1 and not node.keywords
        and isinstance(node.func, ast.Name) and node.func.id in {"tuple", "sorted"}
    ):
        return literal_file_set(node.args[0])
    raise Reject("PAYLOAD_REPLAY_FILES is not a closed literal tuple(sorted(...))")


def analyze(raw: bytes) -> dict[str, Any]:
    need(hashlib.sha256(raw).hexdigest() == OUTER_SHA256, "pinned outer verifier hash")
    try:
        tree = ast.parse(raw, filename=os.fspath(OUTER))
    except SyntaxError as error:
        raise Reject("outer verifier parses") from error

    assignments = [
        node.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "PAYLOAD_REPLAY_FILES"
            for target in node.targets
        )
    ]
    need(len(assignments) == 1, "single PAYLOAD_REPLAY_FILES assignment")
    declared = literal_file_set(assignments[0])

    functions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "validate_payload_replay"
    ]
    need(len(functions) == 1, "single validate_payload_replay function")
    consumed: set[str] = set()
    dynamic_subscripts: list[str] = []
    for node in ast.walk(functions[0]):
        if not (
            isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name)
            and node.value.id in {"small", "captures"}
        ):
            continue
        index = node.slice
        if isinstance(index, ast.Constant) and type(index.value) is str:
            consumed.add(index.value)
        else:
            dynamic_subscripts.append(ast.dump(index, include_attributes=False))
    need(not dynamic_subscripts, "no dynamic payload replay file subscripts")
    need(declared == consumed == set(EXPECTED),
         "declared exact tree equals all consumed replay files")
    return {
        "schema": "cm2.round306c30c.payload-replay-static-consistency.v1",
        "status": "PASS_EXACT_TREE_EQUALS_CONSUMED_KEYS__ZERO_FORMAL_CREDIT",
        "outer_verifier_sha256": OUTER_SHA256,
        "declared_files": sorted(declared),
        "consumed_files": sorted(consumed),
        "file_count": len(declared),
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }


def main() -> int:
    try:
        output = analyze(capture(OUTER))
    except (Reject, OSError, ValueError, TypeError) as error:
        print(canonical({
            "schema": "cm2.round306c30c.payload-replay-static-consistency.v1",
            "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error),
            "formal_credit": 0,
            "source_W_transition_authorized": False,
        }).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
