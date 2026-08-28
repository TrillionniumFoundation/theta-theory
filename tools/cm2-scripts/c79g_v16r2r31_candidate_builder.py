#!/usr/bin/env python3
"""Append-only r31 static retry after the r30 path/pyc rejection.

This file deliberately does not import the r30 bytecode.  At runtime it reads
the r30 *source* as text and evaluates its helper definitions in a synthetic
module after the initial whole-tree pyc inventory has completed.  The actual
candidate inputs remain the immutable r23 source/JSON quartet.  r29's path
rejection and the r30 rejection (including the recorded r30 builder pyc) are
sealed with O_EXCL; r30 -> r31 supersession and the r31 active anchor are also
O_EXCL.  No protocol/runtime/manifest/outer/credit surface is created.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TEMPLATE = "v16r2r23"
TEMPLATE_PREV = "v16r2r22"
R29 = "v16r2r29"
R30 = "v16r2r30"
TAG = "v16r2r31"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
R30_PYC = "scripts/__pycache__/c79g_v16r2r30_candidate_builder.cpython-312.pyc"
R30_PYC_SHA256 = "bcbf9b180adabc9ebef37f8bd74bb64749afa2ce915a70f18e98afc83133fe17"
R30_PYC_SIZE = 30591


def pyc_inventory() -> dict[str, tuple[int, str]]:
    result: dict[str, tuple[int, str]] = {}
    for path in ROOT.rglob("*.pyc"):
        if path.is_symlink() or not path.is_file():
            continue
        raw = path.read_bytes()
        result[str(path.relative_to(ROOT))] = (len(raw), hashlib.sha256(raw).hexdigest())
    return result


def load_r30_source() -> ModuleType:
    """Load definitions from r30 source without invoking its ``main``."""
    path = ROOT / "scripts/c79g_v16r2r30_candidate_builder.py"
    source = path.read_text(encoding="utf-8")
    module = ModuleType("_r30_source_helpers_only")
    module.__file__ = str(path)
    module.__package__ = None
    exec(compile(source, str(path), "exec"), module.__dict__, module.__dict__)
    # r30's draft omitted this import; injecting it is append-only and keeps
    # the rejected source bytes untouched.
    module.re = re
    return module


def configure(m: ModuleType, prev: str, tag: str, anchor_in: Path) -> None:
    """Retarget the generic builder and helper module to one append-only hop."""
    b = m.b
    m.PREV, m.TAG = prev, tag
    m.EDGE = f"{BASE}_{prev}_to_{tag}_static_launch_transition_receipt_v1.json"
    m.ANCHOR = f"{BASE}_{tag}_active_predecessor_supersession_receipt_v1.json"
    m.OLD_EDGE = f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json"
    m.OLD_ANCHOR = f"{BASE}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json"
    b.BASE = BASE
    b.R16 = TEMPLATE
    b.PREV = prev
    b.TAG = tag
    b.UPSTREAM = UPSTREAM
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
    b.ANCHOR_IN = anchor_in
    b.SRC_OUT = {
        "producer": OUT / f"{BASE}_{tag}_semantic_source.py",
        "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{tag}_semantic_source.py",
        "launcher": OUT / f"{BASE}_cold_launch_{tag}_semantic_source.py",
    }
    b.JSON_OUT = {
        "schema": OUT / f"{BASE}_schema_{tag}.json",
        "contract": OUT / f"{BASE}_contract_{tag}.json",
        "transition": OUT / f"{BASE}_{prev}_to_{tag}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{tag}.json",
    }
    b.MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{tag}.sha256"
    b.OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{tag}.json"
    b.REJ = OUT / f"{BASE}_{prev}_static_bundle_rejection_receipt_v1.json"
    b.SUP = OUT / f"{BASE}_{prev}_to_{tag}_static_bundle_rejection_supersession_receipt_v1.json"
    b.ANCHOR = OUT / f"{BASE}_{tag}_active_predecessor_supersession_receipt_v1.json"
    b.CHECKPOINT = UPSTREAM


def install_rejection(m: ModuleType, path: Path, namespace: str,
                      reason: str, detail: dict[str, Any]) -> dict[str, str]:
    b = m.b
    if path.exists():
        value, raw = b.load(path)
        if value.get("failed_namespace") != namespace or value.get("formal_global_closure_credit") != 0:
            raise RuntimeError(f"rejection replay mismatch:{path}")
        return {"action": "replayed", "file_sha256": b.sha(raw),
                "object_sha256": value["object_sha256"]}
    value = b.close({
        "schema": f"cm2.c79g.{namespace}.static-bundle-rejection.v1",
        "status": f"PERMANENT_FAIL_CLOSED_{namespace.upper()}_STATIC_BUILD__ZERO_CREDIT",
        "failed_namespace": namespace,
        "rejection_reason": reason,
        "detail": detail,
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "manifest_created": False,
        "outer_created": False,
        "runtime_surface_created": False,
    })
    raw = b.canon(value) + b"\n"
    action = b.install(path, raw)
    installed, installed_raw = b.load(path)
    return {"action": action, "file_sha256": b.sha(installed_raw),
            "object_sha256": installed["object_sha256"]}


def create_chain(m: ModuleType, prev: str, tag: str, rejection: Path,
                 anchor_in: Path) -> dict[str, str]:
    configure(m, prev, tag, anchor_in)
    m.b.REJ = rejection
    m.b.CHECKPOINT = SUCCESSOR_PIN
    result = m.b.ensure_successor_anchor()
    m.b.CHECKPOINT = UPSTREAM
    return result


def replace_loads(text: str, symbol: str) -> tuple[str, int]:
    tree = ast.parse(text, mode="exec")
    offsets: list[int] = []
    total = 0
    for line in text.splitlines(keepends=True):
        offsets.append(total)
        total += len(line.encode("utf-8"))
    spans: list[tuple[int, int]] = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Name) and node.id == "CHECKPOINT_OBJECT_PIN"
                and isinstance(node.ctx, ast.Load)):
            spans.append((offsets[node.lineno - 1] + node.col_offset,
                          offsets[node.end_lineno - 1] + node.end_col_offset))
    raw = text.encode("utf-8")
    for start, end in sorted(spans, reverse=True):
        raw = raw[:start] + symbol.encode("ascii") + raw[end:]
    return raw.decode("utf-8"), len(spans)


def role_aware_checkpoint_loads(text: str, role: str | None = None) -> tuple[str, int]:
    # Launcher V14 constants occur before UPSTREAM_CHECKPOINT_OBJECT_PIN is
    # assigned at module level.  CHECKPOINT is the already-defined b58 value.
    if role is None:
        # Only the launcher has a module-level CHECKPOINT assignment before
        # its V14 witness table; producer/consumer also carry that witness but
        # must use their earlier UPSTREAM_CHECKPOINT_OBJECT_PIN symbol.
        role = ("launcher" if re.search(
            r'(?m)^CHECKPOINT\s*=\s*"[0-9a-f]{64}"\s*$', text)
                else "source")
    symbol = "CHECKPOINT" if role == "launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"
    return replace_loads(text, symbol)


def canonical_json_patch(m: ModuleType) -> None:
    original = m.canonical_runtime_string

    def patched(value: str) -> str:
        value = original(value)
        value = value.replace(
            f"c79g-v14-rejections-{SUCCESSOR_PIN}",
            f"c79g-v14-rejections-{UPSTREAM}")
        return value

    m.canonical_runtime_string = patched


def v14_trust_crosscheck(m: ModuleType, generated: dict[str, bytes]) -> dict[str, str]:
    """Bind executable V14 path constants to both active JSON trust receipts."""
    expected = f".cm2-runtime/c79g-v14-rejections-{UPSTREAM}/rejection.json"
    consumer_ns: dict[str, Any] = {
        "__name__": "_r31_v14_path_consumer",
        "__file__": str(m.b.SRC_OUT["consumer"]),
        "__package__": None,
    }
    raw = generated["consumer"].decode("utf-8")
    exec(compile(raw, str(m.b.SRC_OUT["consumer"]), "exec"), consumer_ns, consumer_ns)
    launcher_ns: dict[str, Any] = {
        "__name__": "_r31_v14_path_launcher",
        "__file__": str(m.b.SRC_OUT["launcher"]),
        "__package__": None,
    }
    launch_raw = generated["launcher"].decode("utf-8")
    exec(compile(launch_raw, str(m.b.SRC_OUT["launcher"]), "exec"), launcher_ns, launcher_ns)
    if consumer_ns.get("V14_OFFICIAL_REJECTION_RELATIVE_PATH") != expected:
        raise RuntimeError("consumer V14 path is not canonical b58")
    # The launcher uses the same historical witness and must agree too.
    if launcher_ns.get("V14_OFFICIAL_REJECTION_RELATIVE_PATH") != expected:
        raise RuntimeError("launcher V14 path is not canonical b58")
    found: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "v14_official_rejection_path":
                    found.append(child)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for name in ("contract", "audit"):
        value = json.loads(generated[name].decode("utf-8"))
        found.clear()
        walk(value)
        if not found or any(item != expected for item in found):
            raise RuntimeError(f"{name} V14 trust path mismatch:{found!r}")
    return {"source_v14_official_rejection_path": expected,
            "contract_audit_v14_trust_paths": "一致(b58)"}


def launcher_rebind_census(text: str, anchor_file: str, anchor_object: str) -> None:
    """Require configured active namespace/tag and anchor-pin stores."""
    tree = ast.parse(text, mode="exec")
    funcs = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and
             node.name == "configure_workspace_paths"]
    if len(funcs) != 1:
        raise RuntimeError("launcher configurator count")
    fn = funcs[0]
    globals_seen = {name for node in fn.body if isinstance(node, ast.Global)
                    for name in node.names}
    required = {"ACTIVE_SUCCESSOR_NAMESPACE",
                "ACTIVE_SUCCESSOR_NAMESPACE_TAG",
                "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN",
                "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN"}
    if not required <= globals_seen:
        raise RuntimeError("launcher active rebind globals missing")
    stores = {node.id for node in ast.walk(fn)
              if isinstance(node, ast.Name) and
              isinstance(node.ctx, ast.Store)}
    if not required <= stores:
        raise RuntimeError("launcher active rebind stores missing")
    literals = {node.targets[0].id: node.value.value
                for node in ast.walk(fn)
                if isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)}
    if literals.get("ACTIVE_SUCCESSOR_NAMESPACE") != f"{TAG}_semantic_source":
        raise RuntimeError("launcher active namespace store value")
    if literals.get("ACTIVE_SUCCESSOR_NAMESPACE_TAG") != f"{TAG}-semantic-regeneration":
        raise RuntimeError("launcher active namespace tag store value")
    if literals.get("ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN") != anchor_file:
        raise RuntimeError("launcher active file-pin store value")
    if literals.get("ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN") != anchor_object:
        raise RuntimeError("launcher active object-pin store value")
    if "__R31_ANCHOR_FILE_PIN__" in text or "__R31_ANCHOR_OBJECT_PIN__" in text:
        raise RuntimeError("launcher anchor pin placeholder remains")


def patch_module_for_r31(m: ModuleType) -> None:
    m.re = re
    def retag_string(value: str) -> str:
        value = (value.replace(m.OLD_EDGE, m.EDGE)
                      .replace(m.OLD_ANCHOR, m.ANCHOR)
                      .replace("V16R2R23", m.TAG.upper())
                      .replace("V16R2R22", m.PREV.upper())
                      .replace("v16r2r23", m.TAG)
                      .replace("v16r2r22", m.PREV)
                      .replace("c79g-v16r2-semantic-source-candidate-",
                               "c79g-v16r2-candidate-")
                      .replace("c79g-v16r2-semantic-source-rejections-",
                               "c79g-v16r2-rejections-"))
        return m.canonical_runtime_string(value)

    def dynamic_retag(value: Any) -> Any:
        if isinstance(value, dict):
            out = {dynamic_retag(k): dynamic_retag(v)
                   for k, v in value.items()}
            for key in ("effective_checkpoint_object_sha256",
                        "post_seal_effective_checkpoint_object_sha256"):
                if key in out:
                    out[key] = UPSTREAM
            if isinstance(out.get("exact_publication_paths"), dict):
                out["exact_publication_paths"] = m.canonical_exact_paths(
                    out["exact_publication_paths"])
            return out
        if isinstance(value, list):
            return [dynamic_retag(item) for item in value]
        if isinstance(value, str):
            return retag_string(value)
        return value

    def dynamic_retag_source(text: str) -> str:
        # Source text keeps the successor literal intact.  Do *not* call
        # ``retag_string`` here: that helper intentionally canonicalizes JSON
        # runtime strings and would see the entire source as one string,
        # replacing the dd9 successor literal in
        # SUCCESSOR_CHECKPOINT_OBJECT_PIN/CHECKPOINT_OBJECT_PIN definitions.
        # Only retag namespace/filename literals; executable checkpoint loads
        # are normalized separately by role_aware_checkpoint_loads().
        return (text.replace(m.OLD_EDGE, m.EDGE)
                    .replace(m.OLD_ANCHOR, m.ANCHOR)
                    .replace("V16R2R23", m.TAG.upper())
                    .replace("V16R2R22", m.PREV.upper())
                    .replace("v16r2r23", m.TAG)
                    .replace("v16r2r22", m.PREV)
                    .replace("c79g-v16r2-semantic-source-candidate-",
                             "c79g-v16r2-candidate-")
                    .replace("c79g-v16r2-semantic-source-rejections-",
                             "c79g-v16r2-rejections-"))

    m.retag = dynamic_retag
    m.retag_source = dynamic_retag_source
    m.b.retag = dynamic_retag
    m.upstream_checkpoint_loads = role_aware_checkpoint_loads
    canonical_json_patch(m)
    original = m.launcher_globals

    def launcher_globals_with_active_rebinds(text: str) -> str:
        text = original(text)
        global_marker = '    global ACTIVE_EXACT8_FIRST_MEMBER\n'
        if text.count(global_marker) != 1:
            raise RuntimeError("launcher active-global insertion marker")
        text = text.replace(global_marker, global_marker +
            '    global ACTIVE_SUCCESSOR_NAMESPACE, ACTIVE_SUCCESSOR_NAMESPACE_TAG\n'
            '    global ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\n'
            '    global ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\n', 1)
        assignment_marker = (
            '    ACTIVE_EXACT8_FIRST_MEMBER = ACTIVE_PREDECESSOR_SUPERSESSION\n')
        if text.count(assignment_marker) != 1:
            raise RuntimeError("launcher active-store insertion marker")
        text = text.replace(assignment_marker, assignment_marker +
            f'    ACTIVE_SUCCESSOR_NAMESPACE = "{TAG}_semantic_source"\n'
            f'    ACTIVE_SUCCESSOR_NAMESPACE_TAG = "{TAG}-semantic-regeneration"\n'
            '    ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "__R31_ANCHOR_FILE_PIN__"\n'
            '    ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "__R31_ANCHOR_OBJECT_PIN__"\n', 1)
        return text

    m.launcher_globals = launcher_globals_with_active_rebinds
    original_source_patch = m.source_patch

    def source_patch_with_rebind(raw: bytes, role: str, paths: dict[str, str],
                                 anchor_file: str, anchor_object: str,
                                 schema_hash: str, contract_hash: str,
                                 contract_object: str,
                                 producer_hash: str | None = None,
                                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
        blob = original_source_patch(raw, role, paths, anchor_file, anchor_object,
                                     schema_hash, contract_hash, contract_object,
                                     producer_hash, base7)
        if role != "launcher":
            return blob
        text = blob.decode("utf-8")
        text = text.replace('"__R31_ANCHOR_FILE_PIN__"', f'"{anchor_file}"')
        text = text.replace('"__R31_ANCHOR_OBJECT_PIN__"', f'"{anchor_object}"')
        launcher_rebind_census(text, anchor_file, anchor_object)
        m.source_census(text, role)
        m.definition_smoke(text.encode("utf-8"), role)
        return (text if text.endswith("\n") else text + "\n").encode("utf-8")

    m.source_patch = source_patch_with_rebind
    m.b.source_patch = source_patch_with_rebind


def main() -> int:
    # Hard first operation: inventory the entire tree before loading helpers or
    # deriving any candidate bytes.  Existing r30 pyc is a recorded witness;
    # any r31-tagged bytecode is an immediate fail-closed stop.
    before_pyc = pyc_inventory()
    if any(TAG in path for path in before_pyc):
        print(json.dumps({"status": "FAIL_CLOSED_R31_PYC_PREEXISTS",
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False}, sort_keys=True))
        return 1
    if R30_PYC not in before_pyc or before_pyc[R30_PYC] != (R30_PYC_SIZE, R30_PYC_SHA256):
        print(json.dumps({"status": "FAIL_CLOSED_R30_PYC_WITNESS_MISMATCH",
                          "observed": before_pyc.get(R30_PYC),
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False}, sort_keys=True))
        return 1
    try:
        m = load_r30_source()
        patch_module_for_r31(m)
        if pyc_inventory() != before_pyc:
            raise RuntimeError("helper load changed whole-tree pyc inventory")
        r29_anchor = OUT / f"{BASE}_{R29}_active_predecessor_supersession_receipt_v1.json"
        r29_rejection = OUT / f"{BASE}_{R29}_static_bundle_rejection_receipt_v1.json"
        r30_anchor = OUT / f"{BASE}_{R30}_active_predecessor_supersession_receipt_v1.json"
        r30_rejection = OUT / f"{BASE}_{R30}_static_bundle_rejection_receipt_v1.json"
        if not r29_anchor.is_file():
            raise RuntimeError("missing immutable r29 anchor")
        # Preserve the failed r29 semantic-path attempt and close its chain.
        r29_rej = install_rejection(
            m, r29_rejection, R29,
            "R29_CURRENT_RUNTIME_PATHS_USED_SUCCESSOR_DD9_AND_SEMANTIC_SOURCE_NAMESPACE",
            {"runtime_protocol_executed": False,
             "required_successor_fix": "canonical b58 current paths"})
        chain30 = create_chain(m, R29, R30, r29_rejection, r29_anchor)
        # r30 is rejected for both the path split and the immutable builder-pyc
        # contamination.  This receipt is created before the r31 supersession.
        r30_rej = install_rejection(
            m, r30_rejection, R30,
            "R30_CANONICAL_PATH_SPLIT_AND_BUILDER_PYC_CONTAMINATION",
            {"path_split": "current executable runtime paths dd9/semantic-source versus canonical contract b58",
             "builder_pyc_path": R30_PYC,
             "builder_pyc_size": R30_PYC_SIZE,
             "builder_pyc_sha256": R30_PYC_SHA256,
             "runtime_protocol_executed": False})
        chain31 = create_chain(m, R30, TAG, r30_rejection, r30_anchor)
        configure(m, R30, TAG, r30_anchor)
        m.b.REJ = r30_rejection
        m.b.ANCHOR_IN = r30_anchor
        m.b.CHECKPOINT = UPSTREAM
        inputs = [*m.b.SRC_IN.values(), *m.b.JSON_IN.values(), r30_anchor, r30_rejection]
        targets = [*m.b.SRC_OUT.values(), *m.b.JSON_OUT.values(), m.b.MANIFEST, m.b.OUTER]
        if any(not path.is_file() for path in inputs):
            raise RuntimeError("r31 immutable input missing")
        if any(path.exists() for path in targets):
            raise RuntimeError("r31 candidate target already exists")
        generated, meta = m.b.build()
        path_audit = m.preinstall_path_crosscheck(generated)
        v14_audit = v14_trust_crosscheck(m, generated)
        if pyc_inventory() != before_pyc:
            raise RuntimeError("pyc inventory changed before candidate install")
        actions: dict[str, str] = {}
        for name in ("schema", "contract", "transition", "audit"):
            actions[name] = m.b.install(m.b.JSON_OUT[name], generated[name])
        for name in ("producer", "consumer", "launcher"):
            actions[name] = m.b.install(m.b.SRC_OUT[name], generated[name], 0o664)
        if m.b.MANIFEST.exists() or m.b.OUTER.exists():
            raise RuntimeError("r31 manifest/outer appeared")
        if pyc_inventory() != before_pyc:
            raise RuntimeError("pyc inventory changed after candidate install")
        result = {
            "schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
            "status": "V16R2R31_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "template_namespace": TEMPLATE,
            "active_predecessor": R30,
            "r29_rejection": r29_rej,
            "r30_chain": chain30,
            "r30_rejection": r30_rej,
            "r31_chain": chain31,
            "actions": actions,
            "meta": meta,
            "preinstall_path_crosscheck": path_audit,
            "v14_path_crosscheck": v14_audit,
            "pyc_inventory_sha256": hashlib.sha256(
                json.dumps(before_pyc, sort_keys=True).encode()).hexdigest(),
            "candidate_install": True,
            "manifest_created": False,
            "outer_created": False,
            "runtime_authorized": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "pyc_created": False,
        }
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
            "status": f"FAIL_CLOSED_{TAG.upper()}_STATIC_BUILD",
            "error": {"type": type(exc).__name__, "message": str(exc)},
            "candidate_install": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
