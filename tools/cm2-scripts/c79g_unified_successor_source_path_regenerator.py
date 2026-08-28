#!/usr/bin/env python3
"""Prepare a source namespace whose active paths match one fresh JSON tag.

The historical r2/r8 source retries were structurally valid but still pointed
at the frozen ``*_v16r2.json`` quartet.  This tool performs only complete AST
assignment-span replacements for the active path constants, producing a fresh
source namespace (default ``v16r8``) that can be paired with a same-tag JSON
builder.  It is append-only and dry-run by default; no protocol source is
imported or executed and no runtime/credit surface is created.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
DEFAULT_INPUT = {
    "producer": OUT / f"{BASE}_v16r2r8_semantic_source.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2r8_semantic_source.py",
    "launcher": OUT / f"{BASE}_cold_launch_v16r2r8_semantic_source.py",
}


class BuildError(RuntimeError):
    pass


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def read_stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise BuildError(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named = os.lstat(path)
        ident = lambda st: (st.st_dev, st.st_ino, st.st_size,
                            st.st_mtime_ns, st.st_ctime_ns, st.st_nlink)
        if ident(before) != ident(after) or ident(before) != ident(named):
            raise BuildError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise BuildError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def install_o_excl(path: Path, raw: bytes) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o664)
    except FileExistsError:
        old = read_stable(path)
        st = os.stat(path, follow_symlinks=False)
        if old != raw or stat.S_IMODE(st.st_mode) != 0o664 or st.st_nlink != 1:
            raise BuildError(f"existing target differs/not staging mode: {path}")
        return "replayed"
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            offset += os.write(fd, view[offset:])
        os.fsync(fd)
        os.fchmod(fd, 0o664)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def target_paths(tag: str, predecessor_tag: str, source_suffix: str,
                 predecessor_anchor: str) -> dict[str, str]:
    transition = f"deliverables/{BASE}_{predecessor_tag}_to_{tag}_static_launch_transition_receipt_v1.json"
    return {
        "predecessor": predecessor_anchor,
        "schema": f"deliverables/{BASE}_schema_{tag}.json",
        "contract": f"deliverables/{BASE}_contract_{tag}.json",
        "producer": f"deliverables/{BASE}_{tag}_semantic_source.py",
        "consumer": f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{tag}_semantic_source.py",
        "launcher": f"deliverables/{BASE}_cold_launch_{tag}_semantic_source.py",
        "transition": transition,
        "audit": f"deliverables/{BASE}_static_audit_{tag}.json",
        "manifest": f"deliverables/{BASE}_cold_launch_manifest_{tag}.sha256",
        "outer": f"deliverables/{BASE}_cold_launch_outer_receipt_{tag}.json",
    }


def names(node: ast.AST) -> set[str]:
    targets: list[ast.AST] = []
    if isinstance(node, ast.Assign):
        targets = list(node.targets)
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
    return {item.id for item in targets if isinstance(item, ast.Name)}


def line_offsets(text: str) -> list[int]:
    out = [0]
    for line in text.splitlines(True):
        out.append(out[-1] + len(line))
    return out


def apply_edits(text: str, edits: list[tuple[int, int, str]]) -> str:
    ordered = sorted(edits)
    for left, right in zip(ordered, ordered[1:]):
        if right[0] < left[1]:
            raise BuildError(f"overlapping AST edits: {left}/{right}")
    offsets = line_offsets(text)
    out = text
    for start_line, end_line, replacement in sorted(edits, reverse=True):
        start = offsets[start_line - 1]
        end = offsets[end_line - 1]
        newline = text.find("\n", end)
        end = len(text) if newline < 0 else newline + 1
        line_end = text.find("\n", start)
        if line_end < 0:
            line_end = len(text)
        original_line = text[start:line_end]
        indent = original_line[:len(original_line) - len(original_line.lstrip(" \t"))]
        replacement = "\n".join(
            (indent + line if line else line)
            for line in replacement.splitlines()
        )
        if not replacement.endswith("\n"):
            replacement += "\n"
        out = out[:start] + replacement + out[end:]
    return out


def expression_for(role: str, key: str, paths: dict[str, str], tag: str,
                   source_base: str) -> str | None:
    # Keep variable names inherited by the protocol; only their active values
    # change.  The caller supplies the original RHS to distinguish active
    # assignments from historical replay constants.
    if role in {"producer", "consumer"}:
        if key == "SCHEMA":
            return f'SCHEMA = "cm2.round306c79g.true-global-no-producer-consumer.{tag}"'
        if key == "BASE":
            return f'BASE = "{source_base}"'
        table = {
            "CONTRACT": paths["contract"], "CLOSED_SCHEMA": paths["schema"],
            "V16_TO_V16R2_TRANSITION": paths["transition"],
            "STATIC_AUDIT_V16R2": paths["audit"],
            "PRODUCER_SOURCE": paths["producer"],
            "COLD_LAUNCHER": paths["launcher"],
            "COLD_LAUNCH_MANIFEST": paths["manifest"],
            "COLD_LAUNCH_OUTER": paths["outer"],
            "COLD_MANIFEST": paths["manifest"],
            "COLD_OUTER": paths["outer"],
            "FINAL_OUTER": paths["outer"],
        }
        if key in table:
            return f'{key} = OUT / "{Path(table[key]).name}"'
    else:
        if key == "BASE":
            return f'BASE = "{source_base}"'
        if key == "LAUNCHER_RELATIVE":
            return f'LAUNCHER_RELATIVE = Path("deliverables") / "{Path(paths["launcher"]).name}"'
        table = {
            "SCHEMA": paths["schema"], "CONTRACT": paths["contract"],
            "PRODUCER": paths["producer"], "CONSUMER": paths["consumer"],
            "TRANSITION": paths["transition"], "AUDIT": paths["audit"],
            "MANIFEST": paths["manifest"], "OUTER": paths["outer"],
        }
        if key in table:
            # Launcher has both ROOT/deliverables and OUT assignments; use the
            # same relative filename in either context.
            return f'{key} = ROOT / "{table[key]}"'
    return None


def rewrite_source(text: str, role: str, paths: dict[str, str], tag: str,
                   predecessor_tag: str) -> tuple[str, list[str]]:
    tree = ast.parse(text, filename=f"held_{role}.py")
    source_base = f"{BASE}_{tag}_semantic_source"
    edits: list[tuple[int, int, str]] = []
    labels: list[str] = []
    path_needles = ("schema_v16r2", "contract_v16r2", "v16_to_v16r2",
                    "static_audit_v16r2", "manifest_v16r2",
                    "outer_receipt_v16r2", "v16r2r8_semantic_source")
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        target = names(node)
        if len(target) != 1:
            continue
        key = next(iter(target))
        segment = ast.get_source_segment(text, node) or ""
        replacement: str | None = None
        # Active successor anchor metadata is safe to retarget by exact name.
        if key == "ACTIVE_SUCCESSOR_NAMESPACE" and "v16r2r8" in segment:
            replacement = f'ACTIVE_SUCCESSOR_NAMESPACE = "{tag}_semantic_source"'
        elif key == "ACTIVE_SUCCESSOR_NAMESPACE_TAG" and "v16r2r8" in segment:
            replacement = f'ACTIVE_SUCCESSOR_NAMESPACE_TAG = "{tag}-semantic-regeneration"'
        elif key == "SELF" and "v16r2r8" in segment:
            replacement = (f'SELF = {"ROOT" if role == "launcher" else "OUT"} / '
                           f'"{Path(paths["launcher"] if role == "launcher" else paths[role]).name}"')
        elif key == "SOURCE_BASENAME" and "v16r2r8" in segment:
            replacement = f'SOURCE_BASENAME = "{Path(paths["consumer"]).name}"'
        elif key in {"SCHEMA", "BASE", "CONTRACT", "CLOSED_SCHEMA",
                     "PRODUCER_SOURCE", "COLD_LAUNCHER", "COLD_MANIFEST",
                     "COLD_OUTER", "COLD_LAUNCH_MANIFEST", "COLD_LAUNCH_OUTER",
                     "FINAL_OUTER", "V16_TO_V16R2_TRANSITION",
                     "STATIC_AUDIT_V16R2", "LAUNCHER_RELATIVE", "PRODUCER",
                     "CONSUMER", "TRANSITION", "AUDIT", "MANIFEST", "OUTER"}:
            # Only touch assignments that are visibly part of the active
            # successor path block; historical v3..v14 constants are retained.
            if key in {"BASE", "SCHEMA"} or any(needle in segment for needle in path_needles):
                replacement = expression_for(role, key, paths, tag, source_base)
        elif key in {"EXACT8", "COLD_EXACT8", "V16R2_CURRENT_EXACT8"}:
            if "active_predecessor_supersession" in segment:
                if role == "launcher":
                    vals = [f'ROOT / "{paths["predecessor"]}"'] + [
                        f'ROOT / "{paths[k]}"' for k in
                        ("schema", "contract", "producer", "consumer", "transition", "audit", "launcher")]
                elif role == "producer":
                    vals = [f'OUT / "{Path(paths["predecessor"]).name}"',
                            f'OUT / "{Path(paths["schema"]).name}"',
                            f'OUT / "{Path(paths["contract"]).name}"',
                            "SELF", f'OUT / "{Path(paths["consumer"]).name}"',
                            f'OUT / "{Path(paths["transition"]).name}"',
                            f'OUT / "{Path(paths["audit"]).name}"',
                            f'OUT / "{Path(paths["launcher"]).name}"']
                else:
                    vals = [f'OUT / "{Path(paths["predecessor"]).name}"',
                            "CLOSED_SCHEMA", "CONTRACT", "PRODUCER_SOURCE", "SELF",
                            "V16_TO_V16R2_TRANSITION", "STATIC_AUDIT_V16R2", "COLD_LAUNCHER"]
                annotation = "EXACT8: tuple[Path, ...] = " if isinstance(node, ast.AnnAssign) else f"{key} = "
                replacement = annotation + "(" + ",\n".join("    " + x for x in vals) + ",\n)"
        if replacement is not None:
            edits.append((int(node.lineno), int(node.end_lineno), replacement))
            labels.append(f"{role}:{node.lineno}:{key}")
    if not edits:
        raise BuildError(f"no active path edits for {role}")
    return apply_edits(text, edits), labels


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", default="v16r8")
    parser.add_argument("--predecessor-tag", default="v16r7")
    parser.add_argument(
        "--predecessor-anchor",
        default=f"deliverables/{BASE}_v16r2r8_active_predecessor_supersession_receipt_v1.json",
    )
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--producer")
    parser.add_argument("--consumer")
    parser.add_argument("--launcher")
    args = parser.parse_args(argv)
    try:
        if not args.tag.startswith("v") or not args.predecessor_tag.startswith("v"):
            raise BuildError("tags must start with v")
        suffix = f"{args.tag}_semantic_source"
        paths = target_paths(args.tag, args.predecessor_tag, suffix,
                             args.predecessor_anchor)
        cfg = dict(DEFAULT_INPUT)
        for role in cfg:
            value = getattr(args, role)
            if value:
                cfg[role] = Path(value) if Path(value).is_absolute() else ROOT / value
        generated: dict[str, bytes] = {}
        labels: dict[str, list[str]] = {}
        input_hashes: dict[str, str] = {}
        for role, path in cfg.items():
            raw = read_stable(path)
            input_hashes[role] = sha(raw)
            text = raw.decode("utf-8")
            patched, role_labels = rewrite_source(text, role, paths, args.tag, args.predecessor_tag)
            tree = ast.parse(patched, filename=str(path))
            compile(tree, str(path), "exec")
            generated[role] = (patched if patched.endswith("\n") else patched + "\n").encode()
            labels[role] = role_labels
        output_paths = {role: ROOT / paths[role] for role in generated}
        missing_graph = {
            role: [item for item in paths.values()
                   if item not in generated[role].decode("utf-8") and
                   Path(item).name not in generated[role].decode("utf-8")]
            for role in generated
        }
        missing_graph = {role: vals for role, vals in missing_graph.items() if vals}
        if missing_graph:
            raise BuildError("rewritten source path graph incomplete: " + json.dumps(missing_graph, sort_keys=True))
        actions: dict[str, str] = {}
        if args.install:
            for role, raw in generated.items():
                actions[role] = install_o_excl(output_paths[role], raw)
        report = {
            "schema": "cm2.c79g.unified-successor-source-path-regenerator.v1",
            "status": "UNIFIED_SOURCE_PATH_DRY_RUN_PASS__ZERO_CREDIT" if not args.install else
                      "UNIFIED_SOURCE_PATH_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "target_tag": args.tag,
            "predecessor_tag": args.predecessor_tag,
            "paths": paths,
            "input_hashes": input_hashes,
            "output_hashes": {role: sha(raw) for role, raw in generated.items()},
            "patch_labels": labels,
            "installed": actions,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "manifest_created": False,
            "outer_created": False,
            "writes": bool(args.install),
        }
        report["object_sha256"] = sha(canonical(report))
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0
    except (BuildError, OSError, UnicodeError, SyntaxError, ValueError) as exc:
        print(json.dumps({
            "schema": "cm2.c79g.unified-successor-source-path-regenerator.failure.v1",
            "status": "FAIL_CLOSED_UNIFIED_SOURCE_PATH_REGENERATOR",
            "error_type": type(exc).__name__, "error": str(exc),
            "formal_global_closure_credit": 0, "D02_unlock": False,
            "runtime_authorized": False, "writes": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
