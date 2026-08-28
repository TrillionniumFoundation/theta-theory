#!/usr/bin/env python3
"""Clean-room append-only r29 static successor.

The r28 namespace is already sealed as a zero-credit rejection chain.  r29
uses the immutable r23 source/JSON template plus the r28 active anchor, while
rebinding the active edge to r28->r29.  A pre-install AST/literal census fixes
the runtime path bugs found in r24--r28: stale namespace/BASE, unsuffixed SELF
assertions, launcher configure globals, historical v3--v14 checkpoint paths,
and the dd9/b58 effective-checkpoint split.  No protocol or candidate source
is executed and no manifest/outer/runtime/credit surface is produced.
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
TEMPLATE = "v16r2r23"
TEMPLATE_PREV = "v16r2r22"
PREV = "v16r2r28"
TAG = "v16r2r29"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"


def load_generic():
    path = ROOT / "scripts/c79g_v16r2r19_candidate_builder.py"
    spec = importlib.util.spec_from_file_location("_r29_generic_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("generic builder import")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


b = load_generic()
b.R16 = TEMPLATE
b.PREV = PREV
b.TAG = TAG
# During build, CHECKPOINT is the effective C53 pin.  The anchor chain is
# sealed first while it is temporarily set to SUCCESSOR_PIN below.
b.CHECKPOINT = UPSTREAM
b.UPSTREAM = UPSTREAM
b.SRC_IN = {
    "producer": OUT / f"{BASE_PREFIX}_{TEMPLATE}_semantic_source.py",
    "consumer": OUT / f"{BASE_PREFIX}_independent_verifier_assembler_authority_consumer_{TEMPLATE}_semantic_source.py",
    "launcher": OUT / f"{BASE_PREFIX}_cold_launch_{TEMPLATE}_semantic_source.py",
}
b.JSON_IN = {
    "schema": OUT / f"{BASE_PREFIX}_schema_{TEMPLATE}.json",
    "contract": OUT / f"{BASE_PREFIX}_contract_{TEMPLATE}.json",
    "transition": OUT / f"{BASE_PREFIX}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE_PREFIX}_static_audit_{TEMPLATE}.json",
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

EDGE = f"{BASE_PREFIX}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
ANCHOR = f"{BASE_PREFIX}_{TAG}_active_predecessor_supersession_receipt_v1.json"
EDGE_RE = re.compile(rf"{re.escape(BASE_PREFIX)}_v16r2r\d+_to_v16r2r\d+_static_launch_transition_receipt_v1\.json")
ANCHOR_RE = re.compile(rf"{re.escape(BASE_PREFIX)}_v16r2r\d+_active_predecessor_supersession_receipt_v1\.json")
LEGACY_RE = re.compile(r"c79g-v(?:3|4|5|6|7|8|9|10|11|12|14)(?:-|\b)")


def retag(value: Any) -> Any:
    if isinstance(value, dict):
        out = {retag(k): retag(v) for k, v in value.items()}
        # Effective checkpoint fields are authority-domain labels, not the
        # successor namespace pin.  Normalize them before generic builder
        # hash closure so every downstream source pin sees the same b58 value.
        for key in tuple(out):
            if (isinstance(key, str) and
                    (key == "effective_checkpoint_object_sha256" or
                     key == "post_seal_effective_checkpoint_object_sha256")):
                out[key] = UPSTREAM
        return out
    if isinstance(value, list):
        return [retag(v) for v in value]
    if not isinstance(value, str):
        return value
    text = value.replace(
        f"{BASE_PREFIX}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json",
        "__R29_EDGE__",
    ).replace(
        f"{BASE_PREFIX}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json",
        "__R29_ANCHOR__",
    )
    text = (text.replace("V16R2R22", "__R29_PREV__")
                .replace("V16R2R23", "__R29_OLD__")
                .replace("v16r2r22", "__r29_prev__")
                .replace("v16r2r23", "__r29_old__"))
    return (text.replace("__R29_EDGE__", EDGE)
                .replace("__R29_ANCHOR__", ANCHOR)
                .replace("__R29_PREV__", "V16R2R28")
                .replace("__R29_OLD__", "V16R2R29")
                .replace("__r29_prev__", "v16r2r28")
                .replace("__r29_old__", "v16r2r29"))


def _parents(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    return {child: node for node in ast.walk(tree)
            for child in ast.iter_child_nodes(node)}


def _offsets(text: str) -> list[int]:
    out: list[int] = []
    n = 0
    # ast col_offset/end_col_offset are UTF-8 byte offsets, not Python
    # code-point offsets.  Use encoded line lengths so replacements remain
    # correct after the non-ASCII audit comments in these sources.
    for line in text.splitlines(keepends=True):
        out.append(n); n += len(line.encode("utf-8"))
    return out


def _replace_names_by_context(text: str, name: str, context: re.Pattern[str],
                              replacement: str) -> tuple[str, int]:
    tree = ast.parse(text, mode="exec")
    parents = _parents(tree)
    offs = _offsets(text)
    spans: list[tuple[int, int]] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Name) and node.id == name and
                isinstance(node.ctx, ast.Load)):
            continue
        cur: ast.AST | None = node
        hit = False
        for _ in range(14):
            par = parents.get(cur)
            if par is None:
                break
            seg = ast.get_source_segment(text, par) or ""
            if context.search(seg):
                hit = True; break
            cur = par
        if hit:
            spans.append((offs[node.lineno - 1] + node.col_offset,
                          offs[node.end_lineno - 1] + node.end_col_offset))
    raw = text.encode("utf-8")
    for start, end in sorted(spans, reverse=True):
        raw = raw[:start] + replacement.encode("utf-8") + raw[end:]
    return raw.decode("utf-8"), len(spans)


def _legacy_paths(text: str, role: str) -> tuple[str, int]:
    # Launcher path expressions occur before its later UPSTREAM_* assignment
    # at module import, so use the already-defined CHECKPOINT (same b58 value)
    # there.  Producer/consumer define UPSTREAM_* before their path tables.
    symbol = "CHECKPOINT" if role == "launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"
    return _replace_names_by_context(text, "CHECKPOINT_OBJECT_PIN", LEGACY_RE,
                                     symbol)


def _effective_paths(text: str) -> tuple[str, int]:
    # Every current effective-checkpoint field is the upstream C53 pin.  The
    # successor dd9 pin remains available for namespace/anchor path names and
    # CHECKPOINT_CHAIN_OBJECT_PINS, but never labels an active effective value.
    context = re.compile(r"(?:post_seal_)?effective_checkpoint_object_sha256")
    return _replace_names_by_context(text, "CHECKPOINT_OBJECT_PIN", context,
                                     "UPSTREAM_CHECKPOINT_OBJECT_PIN")


def _pin(text: str, role: str, name: str, value: str) -> str:
    pat = rf'(?m)^({re.escape(name)}\s*=\s*)"[0-9a-f]{{64}}"\s*$'
    text, n = re.subn(pat, rf'\1"{value}"', text)
    if n != 1:
        raise RuntimeError(f"{role}:{name}:pin replacement count {n}")
    return text


def _launcher_globals(text: str) -> str:
    """Split historical BASE from semantic BASE and repair configure rebinding."""
    semantic = f'{BASE_PREFIX}_{TAG}_semantic_source'
    old = f'BASE = "{semantic}"'
    if text.count(old) != 1:
        raise RuntimeError("launcher semantic BASE assignment shape")
    text = text.replace(old, f'HISTORICAL_BASE = "{BASE_PREFIX}"\n{old}', 1)
    # All remaining BASE+filename expressions in this launcher are historical
    # v2--v14 paths; active r28/r29 paths are explicit and the unsuffixed
    # assertion is normalized before this function runs.
    text = re.sub(r'\bBASE(\s*\+\s*")_',
                  r'HISTORICAL_BASE\1_', text)
    marker = '    global ROOT, OUT, RUNTIME, SELF, V3_OFFICIAL_REJECTION\n'
    if marker not in text:
        raise RuntimeError("launcher configure global marker absent")
    text = text.replace(marker, marker +
        '    global ACTIVE_PREDECESSOR_SUPERSESSION, ACTIVE_REJECTED_RETRY_SUPERSESSION\n'
        '    global ACTIVE_EXACT8_FIRST_MEMBER\n', 1)
    needle = '    OUT = ROOT / "deliverables"\n'
    if text.count(needle) != 1:
        raise RuntimeError("launcher configure OUT assignment shape")
    anchor_expr = (f'    ACTIVE_PREDECESSOR_SUPERSESSION = OUT / '
                   f'"{BASE_PREFIX}_{TAG}_active_predecessor_supersession_receipt_v1.json"\n'
                   '    ACTIVE_REJECTED_RETRY_SUPERSESSION = ACTIVE_PREDECESSOR_SUPERSESSION\n'
                   '    ACTIVE_EXACT8_FIRST_MEMBER = ACTIVE_PREDECESSOR_SUPERSESSION\n')
    text = text.replace(needle, needle + anchor_expr, 1)
    if re.search(r'\bBASE\s*\+\s*"_', text):
        raise RuntimeError("launcher historical BASE contamination remains")
    return text


def _source_paths(text: str, role: str) -> str:
    prod = f"{BASE_PREFIX}_{TAG}_semantic_source.py"
    cons = f"{BASE_PREFIX}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"
    launch = f"{BASE_PREFIX}_cold_launch_{TAG}_semantic_source.py"
    text = (text.replace(f"{BASE_PREFIX}_v16r2.py", prod)
                .replace(f"{BASE_PREFIX}_independent_verifier_assembler_authority_consumer_v16r2.py", cons)
                .replace("independent_verifier_assembler_authority_consumer_v16r2.py",
                         f"independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"))
    text, n = re.subn(r'SELF\s*==\s*OUT\s*/\s*\(BASE\s*\+\s*"_cold_launch_v16r2\.py"\)',
                      f'SELF == OUT / "{launch}"', text)
    if role == "launcher" and n != 1:
        raise RuntimeError(f"launcher unsuffixed SELF assertion count={n}")
    if role != "launcher" and n != 0:
        raise RuntimeError(f"non-launcher unexpected launch SELF assertion count={n}")
    return text


def _census(text: str, role: str) -> dict[str, int]:
    ast.parse(text, mode="exec"); compile(text, f"<r29-{role}>", "exec")
    ns = re.findall(r'(?m)^ACTIVE_SUCCESSOR_NAMESPACE\s*=\s*"([^"]+)"\s*$', text)
    nst = re.findall(r'(?m)^ACTIVE_SUCCESSOR_NAMESPACE_TAG\s*=\s*"([^"]+)"\s*$', text)
    if ns != [f"{TAG}_semantic_source"] or nst != [f"{TAG}-semantic-regeneration"]:
        raise RuntimeError(f"{role}:namespace census {ns}/{nst}")
    edges = EDGE_RE.findall(text)
    expected_edges = {"producer": 2, "consumer": 1, "launcher": 2}[role]
    if len(edges) != expected_edges or any(x != EDGE for x in edges):
        raise RuntimeError(f"{role}:edge census {len(edges)} {edges}")
    anchors = ANCHOR_RE.findall(text)
    if not anchors or any(x != ANCHOR for x in anchors):
        raise RuntimeError(f"{role}:anchor census {anchors}")
    if "v16r2r23" in text or "v16r2r22" in text:
        raise RuntimeError(f"{role}:old active token")
    if re.search(r'v16r2\.py|independent_verifier_assembler_authority_consumer_v16r2\.py', text):
        raise RuntimeError(f"{role}:unsuffixed current path")
    # Legacy path nodes must no longer use successor dd9.
    tree = ast.parse(text, mode="exec"); parents = _parents(tree)
    bad = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "CHECKPOINT_OBJECT_PIN" and isinstance(node.ctx, ast.Load):
            cur: ast.AST | None = node
            for _ in range(14):
                par = parents.get(cur)
                if par is None: break
                seg = ast.get_source_segment(text, par) or ""
                if LEGACY_RE.search(seg): bad += 1; break
                cur = par
    if bad:
        raise RuntimeError(f"{role}:legacy dd9 path nodes {bad}")
    return {"namespace": 1, "namespace_tag": 1, "active_edges": len(edges),
            "active_anchors": len(anchors), "legacy_paths_rebound": 1}


def _semantic_import_smoke(text: str, role: str) -> None:
    """Execute only module definitions, then inspect configured path globals.

    This is not protocol execution: the synthetic module name prevents any
    ``__main__`` entry point, and no child/process/authority function is
    called.  It catches NameError/order defects that AST compilation cannot.
    """
    ns: dict[str, Any] = {
        "__name__": f"_r29_static_{role}",
        "__file__": str(b.SRC_OUT[role]),
        "__package__": None,
    }
    exec(compile(text, str(b.SRC_OUT[role]), "exec"), ns, ns)
    root = Path("/tmp/cm2-r29-static-census")
    if role == "launcher":
        ns["configure_workspace_paths"](root)
        expected_anchor = root / "deliverables" / ANCHOR
        if ns["ACTIVE_PREDECESSOR_SUPERSESSION"] != expected_anchor:
            raise RuntimeError("launcher configured active anchor identity")
        if ns["ACTIVE_EXACT8_FIRST_MEMBER"] != expected_anchor:
            raise RuntimeError("launcher configured exact8 anchor identity")
        exact8 = tuple(ns["EXACT8"])
        if len(ns["BASE7_PINS"]) != 7 or tuple(ns["BASE7_PINS"]) != exact8[:7]:
            raise RuntimeError("launcher BASE7 keys/exact8 order mismatch")
        if ns["SELF"] != root / "deliverables" / f"{BASE_PREFIX}_cold_launch_{TAG}_semantic_source.py":
            raise RuntimeError("launcher configured SELF identity")
    else:
        out = ns["OUT"]
        expected = out / (f"{BASE_PREFIX}_{TAG}_semantic_source.py" if role == "producer"
                          else f"{BASE_PREFIX}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py")
        if ns["SELF"] != expected:
            raise RuntimeError(f"{role} SELF identity")
        if ns["ACTIVE_PREDECESSOR_SUPERSESSION"] != out / ANCHOR:
            raise RuntimeError(f"{role} active anchor identity")


def source_patch(raw: bytes, role: str, paths: dict[str, str], anchor_file: str,
                 anchor_object: str, schema_hash: str, contract_hash: str,
                 contract_object: str, producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = retag(raw.decode("utf-8"))
    text, _ = EDGE_RE.subn(EDGE, text)
    text = _source_paths(text, role)
    if role == "launcher":
        text = _launcher_globals(text)
    text, legacy_count = _legacy_paths(text, role)
    if legacy_count == 0:
        raise RuntimeError(f"{role}:no legacy paths found")
    text, effective_count = _effective_paths(text)
    if effective_count == 0 and role != "launcher":
        raise RuntimeError(f"{role}:no effective checkpoint fields found")
    text = _pin(text, role, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", anchor_file)
    text = _pin(text, role, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", anchor_object)
    if role != "launcher":
        text = _pin(text, role, "CONTRACT_FILE_PIN", contract_hash)
        text = _pin(text, role, "CONTRACT_OBJECT_PIN", contract_object)
        text = _pin(text, role, "CLOSED_SCHEMA_FILE_PIN", schema_hash)
    if role == "consumer":
        text = _pin(text, role, "PRODUCER_SOURCE_PIN", producer_hash or "")
    if role == "launcher":
        if base7 is None: raise RuntimeError("launcher BASE7 missing")
        names = [("ACTIVE_PREDECESSOR_SUPERSESSION", "anchor"),
                 ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                 ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                 ("TRANSITION", "transition"), ("AUDIT", "audit")]
        entries = "    BASE7_PINS.update({\n" + "".join(
            f"        {var}: (\"{base7[key][0]}\", {base7[key][1]!r}),\n"
            for var, key in names) + "    })"
        pat = r"(?s)    BASE7_PINS\.update\(\{.*?\n    \}\)\n    EXACT8"
        text, n = re.subn(pat, entries + "\n    EXACT8", text, count=1)
        if n != 1: raise RuntimeError(f"launcher BASE7 replacement count {n}")
    _census(text, role)
    _semantic_import_smoke(text, role)
    return (text if text.endswith("\n") else text + "\n").encode()


b.retag = retag
b.source_patch = source_patch


def _json_effective_census(generated: dict[str, bytes]) -> dict[str, int]:
    counts = {"effective_fields": 0, "non_upstream": 0}
    for name in ("contract", "transition", "audit"):
        value = json.loads(generated[name].decode())
        def walk(x: Any):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k == "effective_checkpoint_object_sha256":
                        counts["effective_fields"] += 1
                        if v != UPSTREAM: counts["non_upstream"] += 1
                    walk(v)
            elif isinstance(x, list):
                for v in x: walk(v)
        walk(value)
    if counts["non_upstream"]:
        raise RuntimeError(f"active JSON effective checkpoint not b58:{counts}")
    return counts


def main() -> int:
    inputs = [*b.SRC_IN.values(), *b.JSON_IN.values(), b.ANCHOR_IN]
    if any(not p.is_file() for p in inputs): raise RuntimeError("missing immutable r23/r28 input")
    targets = [*b.SRC_OUT.values(), *b.JSON_OUT.values(), b.MANIFEST, b.OUTER]
    if any(p.exists() for p in targets): raise RuntimeError("r29 target exists")
    if not b.REJ.exists():
        rej = b.close({"schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
                       "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_STATIC_BUILD__ZERO_CREDIT",
                       "failed_namespace": PREV,
                       "rejection_reason": "R28_NAMESPACE_RESERVED_AFTER_R27_CHAIN_ONLY_NO_STATIC_RUNTIME",
                       "detail": {"runtime_protocol_executed": False},
                       "append_only": True, "overwrite_delete_or_reuse_allowed": False,
                       "runtime_authorized": False, "formal_global_closure_credit": 0,
                       "D02_unlock": False, "manifest_created": False,
                       "outer_created": False, "runtime_surface_created": False})
        b.install(b.REJ, b.canon(rej) + b"\n")
    else:
        v, _ = b.load(b.REJ)
        if v.get("failed_namespace") != PREV or v.get("formal_global_closure_credit") != 0:
            raise RuntimeError("r28 rejection replay mismatch")
    # Preserve dd9 as the successor object pin in the r29 chain; switch to b58
    # only after anchor sealing so build effective fields are uniformly b58.
    b.CHECKPOINT = SUCCESSOR_PIN
    chain = b.ensure_successor_anchor()
    b.CHECKPOINT = UPSTREAM
    generated, meta = b.build()
    effective = _json_effective_census(generated)
    actions = {}
    for n in ("schema", "contract", "transition", "audit"):
        actions[n] = b.install(b.JSON_OUT[n], generated[n])
    for n in ("producer", "consumer", "launcher"):
        actions[n] = b.install(b.SRC_OUT[n], generated[n], 0o664)
    if b.MANIFEST.exists() or b.OUTER.exists(): raise RuntimeError("manifest/outer appeared")
    pyc = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*.pyc") if TAG in str(p)]
    if pyc: raise RuntimeError(f"candidate pyc:{pyc}")
    print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
                      "status": "V16R2R29_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
                      "template_namespace": TEMPLATE, "active_predecessor": PREV,
                      "chain": chain, "actions": actions, "meta": meta,
                      "effective_checkpoint_census": effective,
                      "candidate_install": True, "manifest_created": False,
                      "outer_created": False, "runtime_authorized": False,
                      "formal_global_closure_credit": 0, "D02_unlock": False,
                      "pyc_created": False}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__": raise SystemExit(main())
