#!/usr/bin/env python3
"""Fresh append-only r40 static successor for the C79g v16r2 chain.

The r39 publication stopped after the manifest (the outer receipt was never
written).  That state is not replayable or promotable, so this builder first
seals it as a zero-credit publication-incomplete rejection and creates a new
r40 supersession/active-anchor chain with ``O_EXCL``.  Only then are immutable
r39 source/JSON bytes read and retagged in memory to form the r40 candidate.

This program is static-only: it performs AST/compile and closure checks, writes
the seven r40 candidate members, and deliberately does *not* create a
manifest, outer receipt, runtime surface, authority, or credit.  Every failed
attempt is fail-closed; an already sealed r40 chain is never replayed as a new
candidate namespace.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import os
import re
import stat
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TEMPLATE = "v16r2r39"
TEMPLATE_PREV = "v16r2r38"
PREV = "v16r2r39"
TAG = "v16r2r40"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

R39 = {
    f"deliverables/{BASE}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json":
        "9c599ef16d7be444e07ba2ae93d4c74dd71781eb859d0cb590098ed1fb03378e",
    f"deliverables/{BASE}_schema_{TEMPLATE}.json":
        "d547ed583867e817f25d0306057e27b9e781892d6728936da6298b9e40778a61",
    f"deliverables/{BASE}_contract_{TEMPLATE}.json":
        "5886242005f4eaad6ca373f9656f2e82f76ddbbd0e4ff5f1618c12b676daa542",
    f"deliverables/{BASE}_{TEMPLATE}_semantic_source.py":
        "f38b4cefa449102dd1992f1c454f0b55956de405c69253a208d8f55f3dca3961",
    f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{TEMPLATE}_semantic_source.py":
        "d899eb16506171d67265b8a3f57359a33e7a8dfdc2aea9498d9ace2ae4fedc9c",
    f"deliverables/{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json":
        "3ee3f9c4c8f595925de135d099a6612366b6bba64404ae4e82e582d2667a96b7",
    f"deliverables/{BASE}_static_audit_{TEMPLATE}.json":
        "2a1d24187e3e513347f05c163a38b11f3bea2d9de43afeca077a67aa7cae8b31",
    f"deliverables/{BASE}_cold_launch_{TEMPLATE}_semantic_source.py":
        "40196dbcc2a40c956f42ab385b610a302952bcca1fb272b7ce640bb3a5b45543",
    f"deliverables/{BASE}_cold_launch_manifest_{TEMPLATE}.sha256":
        "f4be58e68811566a554f7505d142646a1dc2be029913833fb42b9bd4589b96eb",
}

SCHEMA_NODE_DEFS = (
    "authoritySeal", "coldLaunchedCommittedAuthority", "innerComposite",
    "laterRejection", "presealCommittedSurface", "standaloneOuter",
    "v3OfficialLaterRejectionProof", "v4RejectionSupersessionProof",
    "v7_publication_lock_continuity_incident",
)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"bad immutable input:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after, named = os.fstat(fd), os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino)):
            raise RuntimeError(f"immutable input drift:{path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"immutable input short read:{path}")
        return raw
    finally:
        os.close(fd)


def pyc_inventory() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in ROOT.rglob("*.pyc"):
        if path.is_symlink() or not path.is_file():
            continue
        result[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    return result


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def close(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("object_sha256", None)
    out["object_sha256"] = sha(canon(out))
    return out


def assert_r39_partial() -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, expected in R39.items():
        path = ROOT / relative
        raw = stable(path)
        actual = sha(raw)
        if actual != expected:
            raise RuntimeError(f"r39 immutable pin mismatch:{relative}")
        st = path.stat()
        if st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != 0o444:
            raise RuntimeError(f"r39 frozen identity/mode:{relative}")
        observed[relative] = actual
    outer = OUT / f"{BASE}_cold_launch_outer_receipt_{TEMPLATE}.json"
    if outer.exists():
        raise RuntimeError("r39 outer unexpectedly exists")
    manifest = OUT / f"{BASE}_cold_launch_manifest_{TEMPLATE}.sha256"
    if not manifest.read_text(encoding="utf-8").strip():
        raise RuntimeError("r39 manifest empty")
    return observed


def load_r34_module() -> ModuleType:
    """Load the reviewed r34 constructor without importing its file path."""
    path = ROOT / "scripts/c79g_v16r2r34_candidate_builder.py"
    raw = stable(path)
    name = "_c79g_r40_r34_constructor"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None:
        raise RuntimeError("r34 constructor spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw.decode("utf-8"), str(path), "exec"), module.__dict__, module.__dict__)
    return module


def dynamic_runtime() -> dict[str, str]:
    return {
        "candidate_A": f".cm2-runtime/c79g-v16r2-candidate-a-{UPSTREAM}",
        "candidate_B": f".cm2-runtime/c79g-v16r2-candidate-b-{UPSTREAM}",
        "verification_A": f".cm2-runtime/c79g-v16r2-verification-a-{UPSTREAM}",
        "verification_B": f".cm2-runtime/c79g-v16r2-verification-b-{UPSTREAM}",
        "committed_completion": f".cm2-runtime/c79g-v16r2-committed-completion-{UPSTREAM}",
        "authority_seal": f".cm2-runtime/cm2-global-authority-heads/c79g-v16r2-{UPSTREAM}.seal",
        "v16r2_rejection_namespace": f".cm2-runtime/c79g-v16r2-rejections-{UPSTREAM}",
        "v16r2_later_rejection": f".cm2-runtime/c79g-v16r2-rejections-{UPSTREAM}/rejection.json",
        "candidate_staging_path_template": f".cm2-runtime/.c79g-v16r2-candidate-stage-{{a|b}}-{UPSTREAM}",
        "verification_staging_path_template": f".cm2-runtime/.c79g-v16r2-verification-stage-{{a|b}}-{UPSTREAM}",
        "completion_staging_path": f".cm2-runtime/.c79g-v16r2-completion-stage-{UPSTREAM}",
        "authority_staging_path": f".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2-authority-stage-{UPSTREAM}.seal",
        "cold_launcher": f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py",
        "cold_launch_exact8_manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
        "cold_launch_outer_last": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json",
    }


def offsets(text: str) -> list[int]:
    out: list[int] = []
    total = 0
    for line in text.splitlines(keepends=True):
        out.append(total)
        total += len(line.encode("utf-8"))
    return out


def retag_source(text: str) -> str:
    old_edge = f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json"
    new_edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    old_anchor = f"{BASE}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json"
    new_anchor = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    # Protect the newly formed edge/anchor while replacing the predecessor
    # suffix.  Here ``PREV == TEMPLATE`` (both are r39), so a naïve chained
    # ``.replace(TEMPLATE, TAG)`` would turn the desired r39→r40 edge into
    # r40→r40.
    edge_marker = "__CM2_R40_EDGE_MARKER__"
    anchor_marker = "__CM2_R40_ANCHOR_MARKER__"
    text = text.replace(old_edge, edge_marker).replace(old_anchor, anchor_marker)
    text = (text.replace(TEMPLATE.upper(), TAG.upper())
                .replace(TEMPLATE_PREV.upper(), PREV.upper())
                .replace(TEMPLATE, TAG).replace(TEMPLATE_PREV, PREV))
    text = text.replace(edge_marker, new_edge).replace(anchor_marker, new_anchor)
    text = text.replace("c79g-v16r2-semantic-source-candidate-",
                        "c79g-v16r2-candidate-")
    text = text.replace("c79g-v16r2-semantic-source-rejections-",
                        "c79g-v16r2-rejections-")
    return text


def repair_schema(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    defs = value.get("$defs")
    if not isinstance(defs, dict):
        return value
    for name in SCHEMA_NODE_DEFS:
        node = defs.get(name)
        if not isinstance(node, dict) or not isinstance(node.get("properties"), dict):
            raise RuntimeError(f"schema definition missing:{name}")
        current = node["properties"].get("effective_checkpoint_object_sha256")
        if current == UPSTREAM:
            node["properties"]["effective_checkpoint_object_sha256"] = {"const": UPSTREAM}
        elif current != {"const": UPSTREAM}:
            raise RuntimeError(f"schema checkpoint node drift:{name}:{current!r}")
    return value


def retag_value(value: Any) -> Any:
    """Safe r39→r40 JSON retag with a non-colliding edge substitution."""
    old_edge = f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json"
    new_edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    old_anchor = f"{BASE}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json"
    new_anchor = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"

    def string(text: str) -> str:
        em, am = "__CM2_R40_EDGE_MARKER__", "__CM2_R40_ANCHOR_MARKER__"
        text = text.replace(old_edge, em).replace(old_anchor, am)
        text = (text.replace(TEMPLATE.upper(), TAG.upper())
                    .replace(TEMPLATE_PREV.upper(), PREV.upper())
                    .replace(TEMPLATE, TAG).replace(TEMPLATE_PREV, PREV))
        text = text.replace(em, new_edge).replace(am, new_anchor)
        # Runtime path aliases must remain on the canonical upstream C53
        # namespace; the successor pin is evidence only, never a path.
        text = text.replace(f"c79g-v14-rejections-{SUCCESSOR_PIN}",
                            f"c79g-v14-rejections-{UPSTREAM}")
        if "c79g-v16r2" in text:
            text = text.replace(SUCCESSOR_PIN, UPSTREAM)
        return text

    if isinstance(value, dict):
        out = {retag_value(k): retag_value(v) for k, v in value.items()}
        for key in ("effective_checkpoint_object_sha256",
                    "post_seal_effective_checkpoint_object_sha256"):
            if key in out:
                out[key] = UPSTREAM
        if isinstance(out.get("exact_publication_paths"), dict):
            out["exact_publication_paths"].update({
                "cold_launcher": f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py",
                "cold_launch_exact8_manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
                "cold_launch_outer_last": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json",
            })
        for bundle_key in ("v16r2_bundle", "audited_v16r2_bundle"):
            bundle = out.get(bundle_key)
            if isinstance(bundle, dict):
                bundle["successor_checkpoint_object_sha256"] = SUCCESSOR_PIN
                closure = bundle.get("cold_launch_outer_closure")
                if isinstance(closure, dict):
                    closure.update({
                        "launcher_path": f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py",
                        "exact8_manifest_path": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
                        "outer_last_path": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json",
                    })
        if isinstance(out.get("cold_launch_boundary"), dict) and \
           isinstance(out.get("successor_v16r2_static_bundle"), dict):
            out["cold_launch_boundary"]["successor_checkpoint_object_sha256"] = SUCCESSOR_PIN
        if "$defs" in out:
            out = repair_schema(out)
        return out
    if isinstance(value, list):
        return [retag_value(item) for item in value]
    if isinstance(value, str):
        return string(value)
    return value


def schema_walk(value: Any) -> list[str]:
    """Ensure every recursive JSON-schema node is an object/bool, never a pin string."""
    bad: list[str] = []
    def walk(node: Any, path: str) -> None:
        if isinstance(node, bool):
            return
        if not isinstance(node, dict):
            bad.append(path)
            return
        for key in ("$defs", "properties"):
            child_map = node.get(key, {})
            if not isinstance(child_map, dict):
                bad.append(path + "." + key)
            else:
                for name, child in child_map.items():
                    walk(child, path + "." + key + "." + str(name))
        for key in ("items", "additionalProperties"):
            if key in node and node[key] is not None:
                walk(node[key], path + "." + key)
        prefix = node.get("prefixItems", [])
        if not isinstance(prefix, list):
            bad.append(path + ".prefixItems")
        else:
            for i, child in enumerate(prefix):
                walk(child, f"{path}.prefixItems[{i}]")
    walk(value, "closed-schema")
    return bad


def assign_pin(text: str, name: str, value: str, required: bool = True) -> str:
    pattern = rf'(?m)^(\s*{re.escape(name)}\s*=\s*)"[0-9a-f]{{64}}"(\s*)$'
    text, count = re.subn(pattern, rf'\1"{value}"\2', text)
    if required and count < 1:
        raise RuntimeError(f"{name}:pin assignment count {count}")
    return text


def fixed_loads(text: str, role: str) -> tuple[str, int]:
    tree = ast.parse(text, mode="exec")
    symbol = "CHECKPOINT" if role == "launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"
    starts = offsets(text)
    spans = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == symbol and isinstance(node.ctx, ast.Load):
            spans.append((starts[node.lineno - 1] + node.col_offset,
                          starts[node.end_lineno - 1] + node.end_col_offset))
    raw = text.encode("utf-8")
    for start, end in sorted(spans, reverse=True):
        raw = raw[:start] + symbol.encode("ascii") + raw[end:]
    return raw.decode("utf-8"), len(spans)


def launcher_globals(text: str, af: str, ao: str,
                     base7: dict[str, tuple[str, str | None]]) -> str:
    # Normalize duplicated historical-base declarations inherited by r39.
    text = re.sub(r'(?m)^(HISTORICAL_BASE\s*=\s*"[^"]+"\n)(?:^HISTORICAL_BASE\s*=.*\n)+', r'\1', text)
    # The r39 source has both module and configure-scope active assignments.
    text = assign_pin(text, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", af)
    text = assign_pin(text, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", ao)
    for name, value in (("ACTIVE_SUCCESSOR_NAMESPACE", f"{TAG}_semantic_source"),
                        ("ACTIVE_SUCCESSOR_NAMESPACE_TAG", f"{TAG}-semantic-regeneration")):
        text, count = re.subn(rf'(?m)^(\s*{name}\s*=\s*)"[^"]*"(\s*)$',
                              rf'\1"{value}"\2', text)
        if count < 1:
            raise RuntimeError(f"launcher {name} assignment count {count}")
    # Retagging already changed path suffixes; enforce all executable active
    # path assignments in case an inherited literal used string concatenation.
    active_anchor = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    text = re.sub(r'(?m)^(\s*ACTIVE_PREDECESSOR_SUPERSESSION\s*=\s*OUT\s*/\s*)"[^"]+"',
                  rf'\1"{active_anchor}"', text)
    text = re.sub(r'(?m)^(\s*ACTIVE_REJECTED_RETRY_SUPERSESSION\s*=\s*OUT\s*/\s*)"[^"]+"',
                  rf'\1"{active_anchor}"', text)
    # Replace the executable BASE7 map exactly once; this is the only place
    # where source hashes for downstream members are materialized.
    entries = "    BASE7_PINS.update({\n" + "".join(
        f"        {var}: (\"{base7[key][0]}\", {base7[key][1]!r}),\n"
        for var, key in (("ACTIVE_PREDECESSOR_SUPERSESSION", "anchor"),
                         ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                         ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                         ("TRANSITION", "transition"), ("AUDIT", "audit")))
    entries += "    })"
    text, count = re.subn(r'(?ms)^    BASE7_PINS\.update\(\{.*?^    \}\)(?=\n\s*EXACT8)',
                          entries, text, count=1)
    if count != 1:
        raise RuntimeError(f"launcher BASE7 block count {count}")
    # The inherited source has FINAL_BASE7 true; if a future template changes
    # it, normalize the one module assignment without touching history text.
    text = re.sub(r'(?m)^(FINAL_BASE7_PINS_INSTALLED\s*=\s*)False\s*$', r'\1True', text)
    return text


def source_patch(raw: bytes, role: str, paths: dict[str, str], af: str,
                 ao: str, sh: str, ch: str, co: str,
                 producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = retag_source(raw.decode("utf-8"))
    text, count = fixed_loads(text, role)
    if count == 0:
        raise RuntimeError(f"{role}:no checkpoint loads")
    text = assign_pin(text, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", af)
    text = assign_pin(text, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", ao)
    if role != "launcher":
        text = assign_pin(text, "CONTRACT_FILE_PIN", ch)
        text = assign_pin(text, "CONTRACT_OBJECT_PIN", co)
        text = assign_pin(text, "CLOSED_SCHEMA_FILE_PIN", sh)
        if role == "consumer" and producer_hash is not None:
            text = assign_pin(text, "PRODUCER_SOURCE_PIN", producer_hash)
        text = re.sub(r'(?m)^(FINAL_(?:V16R2_CORE|CURRENT_V16R2)_PINS_INSTALLED\s*=\s*)False\s*$', r'\1True', text)
    else:
        if base7 is None:
            raise RuntimeError("launcher BASE7 missing")
        text = launcher_globals(text, af, ao, base7)
    tree = ast.parse(text, filename=str(paths[role]))
    compile(tree, str(paths[role]), "exec")
    if any(isinstance(n, ast.Name) and n.id == "CHECKPOINT_OBJECT_PIN" and
           isinstance(n.ctx, ast.Load) for n in ast.walk(tree)):
        raise RuntimeError(f"{role}:successor checkpoint load")
    edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    anchor = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    if edge not in text or anchor not in text:
        raise RuntimeError(f"{role}:active edge/anchor absent")
    if f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json" in text:
        raise RuntimeError(f"{role}:stale active edge")
    return (text if text.endswith("\n") else text + "\n").encode()


def seal_r39_rejection(b: ModuleType) -> dict[str, str]:
    path = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
    if path.exists():
        value, raw = b.load(path)
        if value.get("failed_namespace") != PREV or value.get("formal_global_closure_credit") != 0:
            raise RuntimeError("r39 rejection replay mismatch")
        return {"action": "replayed", "file_sha256": b.sha(raw),
                "object_sha256": value["object_sha256"]}
    manifest = OUT / f"{BASE}_cold_launch_manifest_{TEMPLATE}.sha256"
    outer = OUT / f"{BASE}_cold_launch_outer_receipt_{TEMPLATE}.json"
    mf = sha(stable(manifest))
    value = close({
        "schema": f"cm2.c79g.{PREV}.publication-incomplete-rejection.v1",
        "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_PUBLICATION_INCOMPLETE__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "R39_MANIFEST_PRESENT_OUTER_ABSENT_PUBLICATION_INCOMPLETE",
        "detail": {"candidate_install": True, "manifest_present": True,
                   "manifest_path": str(manifest.relative_to(ROOT)),
                   "manifest_file_sha256": mf,
                   "outer_path": str(outer.relative_to(ROOT)),
                   "outer_present": False,
                   "runtime_protocol_executed": False,
                   "required_successor_fix": "fresh r40 exact8_manifest_outer_last"},
        "append_only": True, "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "manifest_created": True, "outer_created": False,
        "runtime_surface_created": False,
    })
    raw = canon(value) + b"\n"
    action = b.install(path, raw)
    installed, installed_raw = b.load(path)
    return {"action": action, "file_sha256": b.sha(installed_raw),
            "object_sha256": installed["object_sha256"]}


def configure(module: ModuleType, b: ModuleType) -> None:
    module.TEMPLATE = TEMPLATE
    module.TEMPLATE_PREV = TEMPLATE_PREV
    module.PREV = PREV
    module.TAG = TAG
    module.UPSTREAM = UPSTREAM
    module.SUCCESSOR_PIN = SUCCESSOR_PIN
    module.CANONICAL_RUNTIME = dynamic_runtime()
    b.BASE = BASE; b.R16 = TEMPLATE; b.PREV = PREV; b.TAG = TAG
    b.UPSTREAM = UPSTREAM; b.CHECKPOINT = UPSTREAM
    b.SRC_IN = {
        "producer": OUT / f"{BASE}_{TEMPLATE}_semantic_source.py",
        "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TEMPLATE}_semantic_source.py",
        "launcher": OUT / f"{BASE}_cold_launch_{TEMPLATE}_semantic_source.py",
    }
    b.JSON_IN = {
        "schema": OUT / f"{BASE}_schema_{TEMPLATE}.json",
        "contract": OUT / f"{BASE}_contract_{TEMPLATE}.json",
        "transition": OUT / f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{TEMPLATE}.json",
    }
    b.ANCHOR_IN = OUT / f"{BASE}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json"
    b.SRC_OUT = {
        "producer": OUT / f"{BASE}_{TAG}_semantic_source.py",
        "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        "launcher": OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
    }
    b.JSON_OUT = {
        "schema": OUT / f"{BASE}_schema_{TAG}.json",
        "contract": OUT / f"{BASE}_contract_{TAG}.json",
        "transition": OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{TAG}.json",
    }
    b.MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
    b.OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
    b.REJ = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
    b.SUP = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
    b.ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    # Use the collision-safe retagger above rather than r34's chained
    # replacement (r40's predecessor and template are both r39).
    b.retag = retag_value
    b.source_patch = source_patch


def main() -> int:
    before = pyc_inventory()
    chain_ready = False
    try:
        prior = assert_r39_partial()
        if any(TAG in p for p in before):
            raise RuntimeError("r40 pyc preexists")
        module = load_r34_module()
        b = module.load_generic()
        configure(module, b)
        rejection = seal_r39_rejection(b)
        b.CHECKPOINT = SUCCESSOR_PIN
        chain = b.ensure_successor_anchor()
        chain_ready = True
        b.CHECKPOINT = UPSTREAM
        inputs = [*b.SRC_IN.values(), *b.JSON_IN.values(), b.ANCHOR_IN, b.REJ]
        targets = [*b.SRC_OUT.values(), *b.JSON_OUT.values(), b.MANIFEST, b.OUTER]
        if any(not p.is_file() for p in inputs):
            raise RuntimeError("immutable r39/r40 chain input missing")
        if any(p.exists() for p in targets):
            raise RuntimeError("r40 target exists")
        generated, meta = b.build()
        schema = json.loads(generated["schema"].decode("utf-8"))
        bad = schema_walk(schema)
        if bad:
            raise RuntimeError("r40 schema node walk:" + ",".join(bad[:10]))
        # Reuse the reviewed cross-file closure checker with dynamic r40
        # globals; it performs source definition smoke and V14/path checks.
        module.b = b
        cross = module.path_crosscheck(generated)
        if pyc_inventory() != before:
            raise RuntimeError("pyc inventory changed before install")
        actions = {}
        for name in ("schema", "contract", "transition", "audit"):
            actions[name] = b.install(b.JSON_OUT[name], generated[name])
        for name in ("producer", "consumer", "launcher"):
            actions[name] = b.install(b.SRC_OUT[name], generated[name], 0o664)
        if b.MANIFEST.exists() or b.OUTER.exists():
            raise RuntimeError("r40 manifest/outer unexpectedly created")
        if pyc_inventory() != before:
            raise RuntimeError("pyc inventory changed after install")
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
                          "status": f"{TAG.upper()}_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
                          "r39_partial_exact9": prior, "predecessor_rejection": rejection,
                          "chain": chain, "actions": actions, "meta": meta,
                          "cross_file": cross, "candidate_install": True,
                          "manifest_created": False, "outer_created": False,
                          "runtime_authorized": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "pyc_created": False}, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
                          "status": f"FAIL_CLOSED_{TAG.upper()}_REJECTION_CHAIN_ONLY" if chain_ready else f"FAIL_CLOSED_{TAG.upper()}_CLEAN_ROOM",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "candidate_install": False, "manifest_created": False,
                          "outer_created": False, "runtime_authorized": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "anchor_presealed": chain_ready}, ensure_ascii=False,
                     sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
