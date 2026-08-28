#!/usr/bin/env python3
"""Append-only r28 static successor builder.

This candidate is deliberately derived from the immutable r23 source/JSON
bytes, never from the malformed r24--r27 source namespaces.  The predecessor
chain is nevertheless r27 -> r28: r27 is rejected and its active anchor is
held as the only predecessor authority input.  The source patch is a
clean-room lexical/AST operation.  It binds every current path, namespace,
active transition, and pin to r28, while preserving historical evidence and
binding legacy v3/v5--v14 rejection paths to the upstream b58 checkpoint.

Only static bytes and the rejection/supersession/anchor chain are in scope.
No producer, consumer, launcher, manifest, outer receipt, runtime surface,
formal credit, or D02 state is created or executed here.
"""
from __future__ import annotations

import ast
import copy
import importlib.util
import json
import os
import re
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE_PREFIX = "cm2_round306c79g_true_global_no_producer_consumer"
OLD = "v16r2r23"                 # immutable source/JSON template namespace
PREV = "v16r2r27"                # active predecessor anchor namespace
OLD_PREV = "v16r2r22"            # template transition predecessor
TAG = "v16r2r28"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"


def _load_generic():
    path = ROOT / "scripts/c79g_v16r2r19_candidate_builder.py"
    spec = importlib.util.spec_from_file_location("_r28_generic_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("generic builder import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


b = _load_generic()
# All generic-builder globals are rebound here, in one module, so no wrapper
# chain can leak an old PREV/TAG or source_patch function closure.
b.R16 = OLD
b.PREV = PREV
b.TAG = TAG
b.UPSTREAM = UPSTREAM
b.CHECKPOINT = CHECKPOINT
b.SRC_IN = {
    "producer": OUT / f"{BASE_PREFIX}_{OLD}_semantic_source.py",
    "consumer": OUT / f"{BASE_PREFIX}_independent_verifier_assembler_authority_consumer_{OLD}_semantic_source.py",
    "launcher": OUT / f"{BASE_PREFIX}_cold_launch_{OLD}_semantic_source.py",
}
b.JSON_IN = {
    "schema": OUT / f"{BASE_PREFIX}_schema_{OLD}.json",
    "contract": OUT / f"{BASE_PREFIX}_contract_{OLD}.json",
    "transition": OUT / f"{BASE_PREFIX}_{OLD_PREV}_to_{OLD}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE_PREFIX}_static_audit_{OLD}.json",
}
b.ANCHOR_IN = OUT / f"{BASE_PREFIX}_{PREV}_active_predecessor_supersession_receipt_v1.json"
b.SRC_OUT = {
    "producer": OUT / f"{BASE_PREFIX}_{TAG}_semantic_source.py",
    "consumer": OUT / f"{BASE_PREFIX}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    "launcher": OUT / f"{BASE_PREFIX}_cold_launch_{TAG}_semantic_source.py",
}
b.JSON_OUT = {
    "schema": OUT / f"{BASE_PREFIX}_schema_{TAG}.json",
    "contract": OUT / f"{BASE_PREFIX}_contract_{TAG}.json",
    "transition": OUT / f"{BASE_PREFIX}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE_PREFIX}_static_audit_{TAG}.json",
}
b.MANIFEST = OUT / f"{BASE_PREFIX}_cold_launch_manifest_{TAG}.sha256"
b.OUTER = OUT / f"{BASE_PREFIX}_cold_launch_outer_receipt_{TAG}.json"
b.REJ = OUT / f"{BASE_PREFIX}_{PREV}_static_bundle_rejection_receipt_v1.json"
b.SUP = OUT / f"{BASE_PREFIX}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
b.ANCHOR = OUT / f"{BASE_PREFIX}_{TAG}_active_predecessor_supersession_receipt_v1.json"

EDGE_NEW = f"{BASE_PREFIX}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
ANCHOR_NEW = f"{BASE_PREFIX}_{TAG}_active_predecessor_supersession_receipt_v1.json"
LEGACY_VERSION_RE = re.compile(r"c79g-v(?:3|4|5|6|7|8|9|10|11|12|14)(?:-|\b)")
ACTIVE_EDGE_RE = re.compile(
    rf"{re.escape(BASE_PREFIX)}_v16r2r\d+_to_v16r2r\d+_static_launch_transition_receipt_v1\.json"
)
ACTIVE_ANCHOR_RE = re.compile(
    rf"{re.escape(BASE_PREFIX)}_v16r2r\d+_active_predecessor_supersession_receipt_v1\.json"
)


def retag(value: Any) -> Any:
    """Retag only the active template edge/namespace; keep history opaque."""
    if isinstance(value, dict):
        return {retag(k): retag(v) for k, v in value.items()}
    if isinstance(value, list):
        return [retag(v) for v in value]
    if not isinstance(value, str):
        return value
    text = value.replace(
        f"{BASE_PREFIX}_{OLD_PREV}_to_{OLD}_static_launch_transition_receipt_v1.json",
        "__R28_EDGE__",
    ).replace(
        f"{BASE_PREFIX}_{OLD}_active_predecessor_supersession_receipt_v1.json",
        "__R28_ANCHOR__",
    )
    # Protect edge/anchor before replacing version tokens so a self-edge can
    # never be manufactured by a cascading replacement.
    text = (text.replace("V16R2R22", "__R28_PREV__")
                .replace("V16R2R23", "__R28_OLD__")
                .replace("v16r2r22", "__r28_prev__")
                .replace("v16r2r23", "__r28_old__"))
    return (text.replace("__R28_EDGE__", EDGE_NEW)
                .replace("__R28_ANCHOR__", ANCHOR_NEW)
                .replace("__R28_PREV__", "V16R2R27")
                .replace("__R28_OLD__", "V16R2R28")
                .replace("__r28_prev__", "v16r2r27")
                .replace("__r28_old__", "v16r2r28"))


def _rewrite_legacy_checkpoint_names(text: str) -> tuple[str, int]:
    """Use the b58 pin for every v3/v4/v5--v14 path expression.

    ``CHECKPOINT_OBJECT_PIN`` is the successor (dd9) object pin and remains
    correct for current v16r2 candidate surfaces and object comparisons.  The
    historical rejection directories on disk are keyed by the upstream C53
    pin (b58).  AST parent inspection limits this rewrite to path expressions;
    historical object-value comparisons are not changed.
    """
    tree = ast.parse(text, mode="exec")
    parents = {child: node for node in ast.walk(tree)
               for child in ast.iter_child_nodes(node)}
    replacements: list[tuple[int, int]] = []
    legacy = re.compile(r"c79g-v(?:3|4|5|6|7|8|9|10|11|12|14)(?:-|\\b)")
    lines = text.splitlines(keepends=True)
    offsets: list[int] = []
    total = 0
    for line in lines:
        offsets.append(total)
        total += len(line)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Name) and node.id == "CHECKPOINT_OBJECT_PIN"
                and isinstance(node.ctx, ast.Load)):
            continue
        cur: ast.AST | None = node
        found = False
        for _ in range(12):
            parent = parents.get(cur)
            if parent is None:
                break
            segment = ast.get_source_segment(text, parent) or ""
            if legacy.search(segment):
                found = True
                break
            cur = parent
        if found:
            start = offsets[node.lineno - 1] + node.col_offset
            end = offsets[node.end_lineno - 1] + node.end_col_offset
            replacements.append((start, end))
    for start, end in sorted(replacements, reverse=True):
        text = text[:start] + "UPSTREAM_CHECKPOINT_OBJECT_PIN" + text[end:]
    return text, len(replacements)


def _replace_pin(text: str, role: str, name: str, value: str,
                 required: bool = True) -> str:
    pattern = rf'(?m)^({re.escape(name)}\s*=\s*)"[0-9a-f]{{64}}"\s*$'
    text, count = re.subn(pattern, rf'\1"{value}"', text)
    if required and count != 1:
        raise RuntimeError(f"{role}:{name}:replacement_count={count}")
    return text


def _normalize_source_paths(text: str, role: str) -> str:
    """Bind every runtime-reachable current path to this candidate."""
    prod = f"{BASE_PREFIX}_{TAG}_semantic_source.py"
    cons = f"{BASE_PREFIX}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"
    launch = f"{BASE_PREFIX}_cold_launch_{TAG}_semantic_source.py"
    # The r23 template has four unsuffixed SELF assertions.  Replace the
    # literal basenames, including the launcher's BASE+ expression, before the
    # final census.  These are executable assertions, not historical records.
    text = (text.replace(f"{BASE_PREFIX}_v16r2.py", prod)
                .replace(f"{BASE_PREFIX}_independent_verifier_assembler_authority_consumer_v16r2.py", cons)
                # The producer's contract cross-check stores this basename
                # as two adjacent string literals, so the BASE_PREFIX form
                # above cannot match it.
                .replace("independent_verifier_assembler_authority_consumer_v16r2.py",
                         f"independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"))
    # The producer's contract-path assertion is split across adjacent source
    # string literals, so the full basename is not contiguous in the raw
    # template bytes.  Normalize the suffix independently as well.
    text = re.sub(
        r"independent_verifier_assembler_authority_consumer_v16r2\.py",
        f"independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        text,
    )
    text, n = re.subn(
        r'SELF\s*==\s*OUT\s*/\s*\(BASE\s*\+\s*"_cold_launch_v16r2\.py"\)',
        f'SELF == OUT / "{launch}"', text)
    if role == "launcher" and n != 1:
        raise RuntimeError(f"launcher:unsuffixed launcher assertion count={n}")
    return text


def _current_path_census(text: str, role: str) -> dict[str, int]:
    """Independent AST/literal census run before any filesystem install."""
    ast.parse(text, mode="exec")
    compile(text, f"<r28-{role}>", "exec")
    expected_ns = f"{TAG}_semantic_source"
    expected_tag = f"{TAG}-semantic-regeneration"
    expected_edge = EDGE_NEW
    # Exactly one active namespace and namespace-tag assignment are required;
    # historical nested records are not counted because these are anchored
    # module-level assignment lines.
    ns = re.findall(rf'(?m)^ACTIVE_SUCCESSOR_NAMESPACE\s*=\s*"([^"]+)"\s*$', text)
    nstag = re.findall(r'(?m)^ACTIVE_SUCCESSOR_NAMESPACE_TAG\s*=\s*"([^"]+)"\s*$', text)
    if ns != [expected_ns] or nstag != [expected_tag]:
        raise RuntimeError(f"{role}:active namespace census ns={ns} tag={nstag}")
    edge_matches = ACTIVE_EDGE_RE.findall(text)
    expected_edge_name = expected_edge
    # Producer carries the module transition constant and one COLD_EXACT8
    # witness; consumer has one module transition constant; launcher has its
    # root/configuration pair.
    expected_count = {"producer": 2, "consumer": 1, "launcher": 2}[role]
    if len(edge_matches) != expected_count or any(x != expected_edge_name for x in edge_matches):
        raise RuntimeError(f"{role}:active transition census count={len(edge_matches)} values={edge_matches}")
    # Current active anchor literals must all point to the r28 anchor.
    anchor_matches = ACTIVE_ANCHOR_RE.findall(text)
    if not anchor_matches or any(x != ANCHOR_NEW for x in anchor_matches):
        raise RuntimeError(f"{role}:active anchor census values={anchor_matches}")
    if re.search(r"v16r2\.py|independent_verifier_assembler_authority_consumer_v16r2\.py", text):
        raise RuntimeError(f"{role}:unsuffixed v16r2 runtime path remains")
    if "v16r2r23" in text or "v16r2r22" in text:
        raise RuntimeError(f"{role}:template active namespace remains")
    # Historical paths must use the upstream checkpoint symbol after the AST
    # rewrite; this catches the dd9/b58 mismatch without touching current v16.
    tree = ast.parse(text, mode="exec")
    parents = {child: node for node in ast.walk(tree)
               for child in ast.iter_child_nodes(node)}
    legacy_bad = 0
    legacy = re.compile(r"c79g-v(?:3|4|5|6|7|8|9|10|11|12|14)(?:-|\b)")
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Name) and node.id == "CHECKPOINT_OBJECT_PIN"
                and isinstance(node.ctx, ast.Load)):
            continue
        cur: ast.AST | None = node
        for _ in range(12):
            parent = parents.get(cur)
            if parent is None:
                break
            segment = ast.get_source_segment(text, parent) or ""
            if legacy.search(segment):
                legacy_bad += 1
                break
            cur = parent
    if legacy_bad:
        raise RuntimeError(f"{role}:legacy checkpoint path still uses successor pin:{legacy_bad}")
    return {"namespace": len(ns), "namespace_tag": len(nstag),
            "active_transition": len(edge_matches),
            "active_anchor": len(anchor_matches),
            "legacy_paths_rebound": 1}


def source_patch(raw: bytes, role: str, paths: dict[str, str],
                 anchor_file: str, anchor_object: str, schema_hash: str,
                 contract_hash: str, contract_object: str,
                 producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = retag(raw.decode("utf-8"))
    # Normalize all active transition assignments after retagging.  This also
    # repairs any self-edge inherited by a prior candidate, but only for the
    # v16r2 active edge pattern (historical v5/v6/etc edges are untouched).
    text, edge_count = ACTIVE_EDGE_RE.subn(EDGE_NEW, text)
    if edge_count < (2 if role == "launcher" else 1):
        raise RuntimeError(f"{role}:active transition literal absent after retag")
    text = _normalize_source_paths(text, role)
    text, legacy_count = _rewrite_legacy_checkpoint_names(text)
    if legacy_count == 0:
        raise RuntimeError(f"{role}:legacy checkpoint path census found no paths")
    text = _replace_pin(text, role, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", anchor_file)
    text = _replace_pin(text, role, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", anchor_object)
    if role != "launcher":
        text = _replace_pin(text, role, "CONTRACT_FILE_PIN", contract_hash)
        text = _replace_pin(text, role, "CONTRACT_OBJECT_PIN", contract_object)
        text = _replace_pin(text, role, "CLOSED_SCHEMA_FILE_PIN", schema_hash)
    if role == "consumer":
        text = _replace_pin(text, role, "PRODUCER_SOURCE_PIN", producer_hash or "")
    if role == "launcher":
        if base7 is None:
            raise RuntimeError("launcher base7 missing")
        names = [("ACTIVE_PREDECESSOR_SUPERSESSION", "anchor"),
                 ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                 ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                 ("TRANSITION", "transition"), ("AUDIT", "audit")]
        entries = "    BASE7_PINS.update({\n" + "".join(
            f"        {var}: (\"{base7[key][0]}\", {base7[key][1]!r}),\n"
            for var, key in names) + "    })"
        pattern = r"(?s)    BASE7_PINS\.update\(\{.*?\n    \}\)\n    EXACT8"
        text, count = re.subn(pattern, entries + "\n    EXACT8", text, count=1)
        if count != 1:
            raise RuntimeError(f"launcher:BASE7 map replacement_count={count}")
    census = _current_path_census(text, role)
    # Keep a machine-readable census marker in the builder report only; source
    # bytes remain untouched by diagnostics.  Reparse once more after all pin
    # substitutions so syntax failures cannot reach install().
    ast.parse(text, filename=str(b.SRC_OUT[role]), mode="exec")
    compile(text, str(b.SRC_OUT[role]), "exec")
    if census["active_transition"] != {"producer": 2, "consumer": 1, "launcher": 2}[role]:
        raise RuntimeError(f"{role}:post-pin transition census drift")
    return (text if text.endswith("\n") else text + "\n").encode("utf-8")


b.retag = retag
b.source_patch = source_patch


def _r27_rejection() -> dict[str, Any]:
    return b.close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
        "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_STATIC_BUILD__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "R27_ACTIVE_SOURCE_NAMESPACE_AND_GRAPH_STALE_AFTER_WRAPPER_RETAG",
        "detail": {
            "failed_checks": ["successor_tokens_and_active_namespace",
                              "active_graph_consensus"],
            "runtime_path_audit": {
                "unsuffixed_self_assertions": True,
                "historical_rejection_paths_used_successor_dd9_pin": True,
            },
            "runtime_protocol_executed": False,
        },
        "append_only": True, "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "manifest_created": False,
        "outer_created": False, "runtime_surface_created": False,
    })


def main() -> int:
    inputs = [*b.SRC_IN.values(), *b.JSON_IN.values(), b.ANCHOR_IN]
    if any(not path.is_file() for path in inputs):
        raise RuntimeError("missing immutable r23 source/JSON or r27 anchor input")
    # The rejection/supersession/anchor chain is itself append-only and may
    # already have been sealed by a pre-install failure.  `ensure_successor_anchor`
    # below replays and byte-validates those objects; only candidate members,
    # manifest, and outer are forbidden pre-existing targets here.
    targets = [*b.SRC_OUT.values(), *b.JSON_OUT.values(), b.MANIFEST, b.OUTER]
    if any(path.exists() for path in targets):
        raise RuntimeError("r28 target already exists")
    if not b.REJ.exists():
        b.install(b.REJ, b.canon(_r27_rejection()) + b"\n")
    else:
        rejection, _ = b.load(b.REJ)
        if rejection.get("failed_namespace") != PREV or rejection.get("formal_global_closure_credit") != 0:
            raise RuntimeError("r27 rejection replay mismatch")
    # Seal r27->r28 supersession and r28 active anchor before deriving bytes.
    chain = b.ensure_successor_anchor()
    generated, meta = b.build()
    actions: dict[str, str] = {}
    for name in ("schema", "contract", "transition", "audit"):
        actions[name] = b.install(b.JSON_OUT[name], generated[name])
    for name in ("producer", "consumer", "launcher"):
        actions[name] = b.install(b.SRC_OUT[name], generated[name], 0o664)
    if b.MANIFEST.exists() or b.OUTER.exists():
        raise RuntimeError("manifest/outer appeared")
    candidate_pyc = [str(x.relative_to(ROOT)) for x in ROOT.rglob("*.pyc") if TAG in str(x)]
    if candidate_pyc:
        raise RuntimeError(f"candidate pyc:{candidate_pyc}")
    print(json.dumps({
        "schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
        "status": "V16R2R28_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
        "template_namespace": OLD, "active_predecessor": PREV,
        "chain": chain, "actions": actions, "meta": meta,
        "candidate_install": True, "manifest_created": False,
        "outer_created": False, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "pyc_created": False,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
