#!/usr/bin/env python3
"""Clean-room r34 static successor with parameterized retagging.

The predecessor r33 namespace is sealed as a zero-credit static candidate.
This builder creates the r33 -> r34 rejection supersession and active anchor
with O_EXCL, then derives a fresh quartet from immutable r23
source/JSON bytes.  All active runtime paths use the canonical upstream C53
object pin (b58); the successor pin (dd9) is retained only in explicit chain
evidence and the successor constant.  The retag functions are parameterized by
PREV/TAG and contain no fixed r30/r31 rewrite branch.

Only AST parse/compile and definition-only synthetic smoke execution are used;
there is no protocol execution, manifest/outer publication, runtime write, or
credit operation.  Bytecode is disabled before any helper is loaded, and the
    whole-tree pyc inventory is checked before and after the in-memory build.
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
TEMPLATE = os.environ.get("CM2_TEMPLATE_SUFFIX", "v16r2r23")
TEMPLATE_PREV = os.environ.get("CM2_TEMPLATE_PREV_SUFFIX", "v16r2r22")
PREV = os.environ.get("CM2_PREDECESSOR_SUFFIX", "v16r2r33")
TAG = os.environ.get("CM2_SUCCESSOR_SUFFIX", "v16r2r34")
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

CANONICAL_RUNTIME = {
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
    # These three publication aliases are namespace-specific.  Keeping the
    # inherited unsuffixed v16r2 aliases would split exact8/manifest/outer
    # identity from the actual successor launcher and leave a path bypass.
    "cold_launcher": f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py",
    "cold_launch_exact8_manifest": f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256",
    "cold_launch_outer_last": f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json",
}


def load_generic() -> ModuleType:
    path = ROOT / "scripts/c79g_v16r2r19_candidate_builder.py"
    source = path.read_text(encoding="utf-8")
    module = ModuleType("_r34_generic_builder")
    module.__file__ = str(path)
    module.__package__ = None
    exec(compile(source, str(path), "exec"), module.__dict__, module.__dict__)
    return module


b: ModuleType | None = None


def configure_builder(anchor_in: Path) -> None:
    b.BASE = BASE
    b.R16 = TEMPLATE
    b.PREV = PREV
    b.TAG = TAG
    b.UPSTREAM = UPSTREAM
    b.CHECKPOINT = UPSTREAM
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


def pyc_inventory() -> dict[str, tuple[int, str]]:
    result: dict[str, tuple[int, str]] = {}
    for path in ROOT.rglob("*.pyc"):
        if path.is_symlink() or not path.is_file():
            continue
        raw = path.read_bytes()
        result[str(path.relative_to(ROOT))] = (len(raw), hashlib.sha256(raw).hexdigest())
    return result


def canonical_runtime_string(value: str) -> str:
    value = value.replace("c79g-v16r2-semantic-source-candidate-",
                          "c79g-v16r2-candidate-")
    value = value.replace("c79g-v16r2-semantic-source-rejections-",
                          "c79g-v16r2-rejections-")
    value = value.replace(f"c79g-v14-rejections-{SUCCESSOR_PIN}",
                          f"c79g-v14-rejections-{UPSTREAM}")
    if "c79g-v16r2" in value:
        value = value.replace(SUCCESSOR_PIN, UPSTREAM)
    return value


def canonical_exact_paths(value: dict[str, Any]) -> dict[str, Any]:
    out = dict(value)
    out.update(CANONICAL_RUNTIME)
    return out


def retag_string(value: str) -> str:
    old_edge = f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json"
    old_anchor = f"{BASE}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json"
    new_edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    new_anchor = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    return canonical_runtime_string(
        value.replace(old_edge, new_edge).replace(old_anchor, new_anchor)
        .replace(TEMPLATE.upper(), TAG.upper())
        .replace(TEMPLATE_PREV.upper(), PREV.upper())
        .replace(TEMPLATE, TAG).replace(TEMPLATE_PREV, PREV)
        .replace("c79g-v16r2-semantic-source-candidate-", "c79g-v16r2-candidate-")
        .replace("c79g-v16r2-semantic-source-rejections-", "c79g-v16r2-rejections-"))


def retag(value: Any) -> Any:
    if isinstance(value, dict):
        out = {retag(k): retag(v) for k, v in value.items()}
        for key in ("effective_checkpoint_object_sha256",
                    "post_seal_effective_checkpoint_object_sha256"):
            if key in out:
                out[key] = UPSTREAM
        if isinstance(out.get("exact_publication_paths"), dict):
            out["exact_publication_paths"] = canonical_exact_paths(
                out["exact_publication_paths"])
        # Keep the top-level contract/transition/audit shapes unchanged while
        # making the active successor checkpoint explicit.  The transition's
        # successor bundle has a strict historical 11-key shape, so its
        # successor pin belongs in the existing cold-launch boundary map.
        if isinstance(out.get("v16r2_bundle"), dict):
            active = out["v16r2_bundle"]
            active["successor_checkpoint_object_sha256"] = SUCCESSOR_PIN
            closure = active.get("cold_launch_outer_closure")
            if isinstance(closure, dict):
                closure.update({
                    "launcher_path": CANONICAL_RUNTIME["cold_launcher"],
                    "exact8_manifest_path": CANONICAL_RUNTIME["cold_launch_exact8_manifest"],
                    "outer_last_path": CANONICAL_RUNTIME["cold_launch_outer_last"],
                })
        if isinstance(out.get("audited_v16r2_bundle"), dict):
            active = out["audited_v16r2_bundle"]
            active["successor_checkpoint_object_sha256"] = SUCCESSOR_PIN
            closure = active.get("cold_launch_outer_closure")
            if isinstance(closure, dict):
                closure.update({
                    "launcher_path": CANONICAL_RUNTIME["cold_launcher"],
                    "exact8_manifest_path": CANONICAL_RUNTIME["cold_launch_exact8_manifest"],
                    "outer_last_path": CANONICAL_RUNTIME["cold_launch_outer_last"],
                })
        if isinstance(out.get("cold_launch_boundary"), dict) and \
           isinstance(out.get("successor_v16r2_static_bundle"), dict):
            out["cold_launch_boundary"]["successor_checkpoint_object_sha256"] = SUCCESSOR_PIN
        return out
    if isinstance(value, list):
        return [retag(item) for item in value]
    if isinstance(value, str):
        return retag_string(value)
    return value


def retag_source(text: str) -> str:
    # Keep the dd9 literal untouched; role-aware AST rewriting below changes
    # executable loads while preserving SUCCESSOR_CHECKPOINT_OBJECT_PIN.
    old_edge = f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json"
    old_anchor = f"{BASE}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json"
    return (text.replace(old_edge,
                         f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json")
                .replace(old_anchor,
                         f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json")
                .replace(TEMPLATE.upper(), TAG.upper())
                .replace(TEMPLATE_PREV.upper(), PREV.upper())
                .replace(TEMPLATE, TAG).replace(TEMPLATE_PREV, PREV)
                .replace("c79g-v16r2-semantic-source-candidate-",
                         "c79g-v16r2-candidate-")
                .replace("c79g-v16r2-semantic-source-rejections-",
                         "c79g-v16r2-rejections-"))


def offsets(text: str) -> list[int]:
    result: list[int] = []
    total = 0
    for line in text.splitlines(keepends=True):
        result.append(total)
        total += len(line.encode("utf-8"))
    return result


def replace_checkpoint_loads(text: str, role: str) -> tuple[str, int]:
    tree = ast.parse(text, mode="exec")
    symbol = "CHECKPOINT" if role == "launcher" else "UPSTREAM_CHECKPOINT_OBJECT_PIN"
    starts = offsets(text)
    spans: list[tuple[int, int]] = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Name) and node.id == "CHECKPOINT_OBJECT_PIN"
                and isinstance(node.ctx, ast.Load)):
            spans.append((starts[node.lineno - 1] + node.col_offset,
                          starts[node.end_lineno - 1] + node.end_col_offset))
    raw = text.encode("utf-8")
    for start, end in sorted(spans, reverse=True):
        raw = raw[:start] + symbol.encode("ascii") + raw[end:]
    return raw.decode("utf-8"), len(spans)


def source_paths(text: str, role: str) -> str:
    producer = f"{BASE}_{TAG}_semantic_source.py"
    consumer = f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"
    launcher = f"{BASE}_cold_launch_{TAG}_semantic_source.py"
    text = (text.replace(f"{BASE}_v16r2.py", producer)
                .replace(f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2.py", consumer)
                .replace("independent_verifier_assembler_authority_consumer_v16r2.py",
                         f"independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"))
    text, count = re.subn(r'SELF\s*==\s*OUT\s*/\s*\(BASE\s*\+\s*"_cold_launch_v16r2\.py"\)',
                          f'SELF == OUT / "{launcher}"', text)
    if (role == "launcher" and count != 1) or (role != "launcher" and count):
        raise RuntimeError(f"{role}:unsuffixed SELF assertion")
    return text


def replace_pin(text: str, role: str, name: str, value: str) -> str:
    text, count = re.subn(rf'(?m)^({re.escape(name)}\s*=\s*)"[0-9a-f]{{64}}"\s*$',
                          rf'\1"{value}"', text)
    if count != 1:
        raise RuntimeError(f"{role}:{name}:pin count {count}")
    return text


def launcher_globals(text: str, anchor_file: str, anchor_object: str) -> str:
    semantic = f"{BASE}_{TAG}_semantic_source"
    assignment = f'BASE = "{semantic}"'
    if text.count(assignment) != 1:
        raise RuntimeError("launcher BASE assignment")
    text = text.replace(assignment, f'HISTORICAL_BASE = "{BASE}"\n{assignment}', 1)
    text = re.sub(r'\bBASE(\s*\+\s*")_', r'HISTORICAL_BASE\1_', text)
    marker = '    global ROOT, OUT, RUNTIME, SELF, V3_OFFICIAL_REJECTION\n'
    if marker not in text:
        raise RuntimeError("launcher global marker")
    text = text.replace(marker, marker +
        '    global ACTIVE_PREDECESSOR_SUPERSESSION, ACTIVE_REJECTED_RETRY_SUPERSESSION\n'
        '    global ACTIVE_EXACT8_FIRST_MEMBER\n'
        '    global ACTIVE_SUCCESSOR_NAMESPACE, ACTIVE_SUCCESSOR_NAMESPACE_TAG\n'
        '    global ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN\n'
        '    global ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN\n', 1)
    needle = '    OUT = ROOT / "deliverables"\n'
    if text.count(needle) != 1:
        raise RuntimeError("launcher OUT assignment")
    anchor = (f'    ACTIVE_PREDECESSOR_SUPERSESSION = OUT / "{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"\n'
              '    ACTIVE_REJECTED_RETRY_SUPERSESSION = ACTIVE_PREDECESSOR_SUPERSESSION\n'
              '    ACTIVE_EXACT8_FIRST_MEMBER = ACTIVE_PREDECESSOR_SUPERSESSION\n'
              f'    ACTIVE_SUCCESSOR_NAMESPACE = "{TAG}_semantic_source"\n'
              f'    ACTIVE_SUCCESSOR_NAMESPACE_TAG = "{TAG}-semantic-regeneration"\n'
              f'    ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = "{anchor_file}"\n'
              f'    ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN = "{anchor_object}"\n')
    text = text.replace(needle, needle + anchor, 1)
    if re.search(r'\bBASE\s*\+\s*"_', text):
        raise RuntimeError("launcher historical BASE contamination")
    return text


def source_census(text: str, role: str) -> None:
    tree = ast.parse(text, mode="exec")
    compile(tree, f"<r34-{role}>", "exec")
    old_edge = f"{BASE}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json"
    old_anchor = f"{BASE}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json"
    edge = f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
    anchor = f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    if old_edge in text or old_anchor in text:
        raise RuntimeError(f"{role}:old active edge/anchor")
    if "c79g-v16r2-semantic-source-candidate-" in text or "c79g-v16r2-semantic-source-rejections-" in text:
        raise RuntimeError(f"{role}:semantic-source runtime path")
    if any(isinstance(node, ast.Name) and node.id == "CHECKPOINT_OBJECT_PIN" and
           isinstance(node.ctx, ast.Load) for node in ast.walk(tree)):
        raise RuntimeError(f"{role}:successor pin load")
    edges = re.findall(rf'{re.escape(BASE)}_v16r2r\d+_to_v16r2r\d+_static_launch_transition_receipt_v1\.json', text)
    anchors = re.findall(rf'{re.escape(BASE)}_v16r2r\d+_active_predecessor_supersession_receipt_v1\.json', text)
    if not edges or any(item != edge for item in edges):
        raise RuntimeError(f"{role}:edge census {edges}")
    if not anchors or any(item != anchor for item in anchors):
        raise RuntimeError(f"{role}:anchor census {anchors}")
    expected_ns = f"{TAG}_semantic_source"
    expected_nst = f"{TAG}-semantic-regeneration"
    if role != "launcher":
        # Producer/consumer keep the active namespace declarations at module
        # scope; require exactly one literal assignment for each.
        ns = re.findall(r'(?m)^ACTIVE_SUCCESSOR_NAMESPACE\s*=\s*"([^"]+)"\s*$', text)
        nst = re.findall(r'(?m)^ACTIVE_SUCCESSOR_NAMESPACE_TAG\s*=\s*"([^"]+)"\s*$', text)
        if ns != [expected_ns] or nst != [expected_nst]:
            raise RuntimeError(f"{role}:namespace/tag census {ns}/{nst}")
    else:
        # launcher_globals deliberately binds the active namespace inside the
        # root configurator.  Audit that executable scope directly instead of
        # counting only module-level declarations.
        configure_functions = [
            node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == "configure_workspace_paths"
        ]
        if len(configure_functions) != 1:
            raise RuntimeError(f"launcher:configure_workspace_paths definitions {len(configure_functions)}")
        observed: dict[str, list[str]] = {
            "ACTIVE_SUCCESSOR_NAMESPACE": [],
            "ACTIVE_SUCCESSOR_NAMESPACE_TAG": [],
        }
        for node in ast.walk(configure_functions[0]):
            if not (isinstance(node, ast.Assign)
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in observed:
                    observed[target.id].append(node.value.value)
        if observed["ACTIVE_SUCCESSOR_NAMESPACE"] != [expected_ns] or \
           observed["ACTIVE_SUCCESSOR_NAMESPACE_TAG"] != [expected_nst]:
            raise RuntimeError(f"launcher:namespace/tag census {observed}")


def definition_smoke(raw: bytes, role: str, anchor_file: str,
                     anchor_object: str) -> dict[str, str]:
    ns: dict[str, Any] = {"__name__": f"_r34_static_{role}",
                          "__file__": str(b.SRC_OUT[role]),
                          "__package__": None}
    text = raw.decode("utf-8")
    exec(compile(text, str(b.SRC_OUT[role]), "exec"), ns, ns)
    root = ROOT if role != "launcher" else Path("/tmp/cm2-r34-path-crosscheck")
    if role == "launcher":
        ns["configure_workspace_paths"](root)
    expected_names = (("CANDIDATE_A", "candidate_A"),
                      ("CANDIDATE_B", "candidate_B"))
    if role == "consumer":
        expected_names += (("VERIFICATION_A", "verification_A"),
                           ("VERIFICATION_B", "verification_B"),
                           ("COMMITTED_COMPLETION", "committed_completion"),
                           ("AUTHORITY_SEAL", "authority_seal"),
                           ("REJECTION_NAMESPACE", "v16r2_rejection_namespace"),
                           ("LATER_REJECTION", "v16r2_later_rejection"))
    if role == "launcher":
        expected_names = (("V16R2_REJECTION_NAMESPACE", "v16r2_rejection_namespace"),
                          ("V16R2_LATER_REJECTION", "v16r2_later_rejection"))
    observed: dict[str, str] = {}
    for name, key in expected_names:
        expected = root / CANONICAL_RUNTIME[key]
        if ns.get(name) != expected:
            raise RuntimeError(f"{role}:{name}:{ns.get(name)!r}!={expected!r}")
        observed[name] = str(ns[name])
    if ns.get("UPSTREAM_CHECKPOINT_OBJECT_PIN") != UPSTREAM or ns.get("SUCCESSOR_CHECKPOINT_OBJECT_PIN") != SUCCESSOR_PIN:
        raise RuntimeError(f"{role}:checkpoint role")
    if ns.get("CHECKPOINT", UPSTREAM) != UPSTREAM:
        raise RuntimeError(f"{role}:effective CHECKPOINT")
    if role == "launcher":
        for name, value in (("ACTIVE_SUCCESSOR_NAMESPACE", f"{TAG}_semantic_source"),
                            ("ACTIVE_SUCCESSOR_NAMESPACE_TAG", f"{TAG}-semantic-regeneration"),
                            ("ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", anchor_file),
                            ("ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", anchor_object)):
            if ns.get(name) != value:
                raise RuntimeError(f"launcher:{name} rebind")
    return observed


def source_patch(raw: bytes, role: str, paths: dict[str, str], anchor_file: str,
                 anchor_object: str, schema_hash: str, contract_hash: str,
                 contract_object: str, producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = retag_source(raw.decode("utf-8"))
    text = source_paths(text, role)
    text, count = replace_checkpoint_loads(text, role)
    if count == 0:
        raise RuntimeError(f"{role}:no checkpoint loads")
    text = replace_pin(text, role, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", anchor_file)
    text = replace_pin(text, role, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", anchor_object)
    if role != "launcher":
        text = replace_pin(text, role, "CONTRACT_FILE_PIN", contract_hash)
        text = replace_pin(text, role, "CONTRACT_OBJECT_PIN", contract_object)
        text = replace_pin(text, role, "CLOSED_SCHEMA_FILE_PIN", schema_hash)
    if role == "consumer":
        text = replace_pin(text, role, "PRODUCER_SOURCE_PIN", producer_hash or "")
    if role == "launcher":
        text = launcher_globals(text, anchor_file, anchor_object)
        if base7 is None:
            raise RuntimeError("launcher BASE7 missing")
        names = [("ACTIVE_PREDECESSOR_SUPERSESSION", "anchor"),
                 ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                 ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                 ("TRANSITION", "transition"), ("AUDIT", "audit")]
        entries = "    BASE7_PINS.update({\n" + "".join(
            f"        {var}: (\"{base7[key][0]}\", {base7[key][1]!r}),\n"
            for var, key in names) + "    })"
        text, n = re.subn(r"(?s)    BASE7_PINS\.update\(\{.*?\n    \}\)\n    EXACT8",
                          entries + "\n    EXACT8", text, count=1)
        if n != 1:
            raise RuntimeError("launcher BASE7 replacement")
    source_census(text, role)
    blob = (text if text.endswith("\n") else text + "\n").encode("utf-8")
    definition_smoke(blob, role, anchor_file, anchor_object)
    return blob


def bind_builder() -> None:
    global b
    if b is None:
        raise RuntimeError("generic builder not loaded")
    b.retag = retag
    b.source_patch = source_patch


def path_crosscheck(generated: dict[str, bytes]) -> dict[str, Any]:
    contract = json.loads(generated["contract"].decode("utf-8"))
    paths = contract.get("exact_publication_paths")
    if not isinstance(paths, dict):
        raise RuntimeError("contract exact_publication_paths")
    for key, expected in CANONICAL_RUNTIME.items():
        if paths.get(key) != expected:
            raise RuntimeError(f"contract path {key}")
        if "semantic-source" in str(paths[key]) or SUCCESSOR_PIN in str(paths[key]):
            raise RuntimeError(f"contract noncanonical path {key}")
    expected_aliases = {
        "cold_launcher": str(b.SRC_OUT["launcher"].relative_to(ROOT)),
        "cold_launch_exact8_manifest": str(b.MANIFEST.relative_to(ROOT)),
        "cold_launch_outer_last": str(b.OUTER.relative_to(ROOT)),
    }
    if {key: paths.get(key) for key in expected_aliases} != expected_aliases:
        raise RuntimeError(f"contract cold-launch aliases {paths}")
    active_contract = contract.get("v16r2_bundle")
    if not isinstance(active_contract, dict) or \
       active_contract.get("successor_checkpoint_object_sha256") != SUCCESSOR_PIN:
        raise RuntimeError("contract active successor checkpoint")
    closure = active_contract.get("cold_launch_outer_closure")
    # The closure uses launcher_path/exact8_manifest_path/outer_last_path
    # names rather than the contract alias keys.
    if not isinstance(closure, dict) or {
        "launcher_path": closure.get("launcher_path"),
        "exact8_manifest_path": closure.get("exact8_manifest_path"),
        "outer_last_path": closure.get("outer_last_path"),
    } != {
        "launcher_path": expected_aliases["cold_launcher"],
        "exact8_manifest_path": expected_aliases["cold_launch_exact8_manifest"],
        "outer_last_path": expected_aliases["cold_launch_outer_last"],
    }:
        raise RuntimeError("contract cold-launch closure aliases")
    transition = json.loads(generated["transition"].decode("utf-8"))
    boundary = transition.get("cold_launch_boundary")
    if not isinstance(boundary, dict) or boundary.get("successor_checkpoint_object_sha256") != SUCCESSOR_PIN:
        raise RuntimeError("transition boundary successor checkpoint")
    successor = transition.get("successor_v16r2_static_bundle")
    if not isinstance(successor, dict) or len(successor) != 11:
        raise RuntimeError("transition successor exact 11-key shape")
    audit = json.loads(generated["audit"].decode("utf-8"))
    active_audit = audit.get("audited_v16r2_bundle")
    if not isinstance(active_audit, dict) or \
       active_audit.get("successor_checkpoint_object_sha256") != SUCCESSOR_PIN:
        raise RuntimeError("audit active successor checkpoint")
    audit_closure = active_audit.get("cold_launch_outer_closure")
    if not isinstance(audit_closure, dict) or {
        "launcher_path": audit_closure.get("launcher_path"),
        "exact8_manifest_path": audit_closure.get("exact8_manifest_path"),
        "outer_last_path": audit_closure.get("outer_last_path"),
    } != {
        "launcher_path": expected_aliases["cold_launcher"],
        "exact8_manifest_path": expected_aliases["cold_launch_exact8_manifest"],
        "outer_last_path": expected_aliases["cold_launch_outer_last"],
    }:
        raise RuntimeError("audit cold-launch closure aliases")
    if [len(contract), len(transition), len(audit)] != [30, 31, 30]:
        raise RuntimeError("active JSON top-level shape")
    # Pin the immutable anchor itself, not the nested predecessor-supersession
    # witness it points to.  The source pins and generic DAG builder both use
    # this top-level anchor file SHA plus its closed object SHA.
    anchor_path = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
    anchor_raw = b.stable(anchor_path)
    anchor = json.loads(anchor_raw.decode("utf-8"))
    af = b.sha(anchor_raw)
    ao = anchor["object_sha256"]
    observed = {role: definition_smoke(generated[role], role, af, ao)
                for role in ("producer", "consumer", "launcher")}
    expected_v14 = f".cm2-runtime/c79g-v14-rejections-{UPSTREAM}/rejection.json"
    for role in ("consumer", "launcher"):
        ns: dict[str, Any] = {"__name__": f"_r34_v14_{role}",
                              "__file__": str(b.SRC_OUT[role]), "__package__": None}
        text = generated[role].decode("utf-8")
        exec(compile(text, str(b.SRC_OUT[role]), "exec"), ns, ns)
        if role == "launcher":
            ns["configure_workspace_paths"](Path("/tmp/cm2-r34-path-crosscheck"))
        if ns.get("V14_OFFICIAL_REJECTION_RELATIVE_PATH") != expected_v14:
            raise RuntimeError(f"{role}:V14 path")
    for name in ("contract", "audit"):
        value = json.loads(generated[name].decode("utf-8"))
        found: list[str] = []
        def walk(x: Any) -> None:
            if isinstance(x, dict):
                for key, child in x.items():
                    if key == "v14_official_rejection_path":
                        found.append(child)
                    walk(child)
            elif isinstance(x, list):
                for child in x:
                    walk(child)
        walk(value)
        if not found or any(item != expected_v14 for item in found):
            raise RuntimeError(f"{name}:V14 trust path {found}")
    return {"contract_exact_paths": paths, "source_path_globals": observed,
            "v14_source_and_json_b58": True}


def predecessor_rejection() -> dict[str, str]:
    path = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
    if path.exists():
        value, raw = b.load(path)
        if value.get("failed_namespace") != PREV or value.get("formal_global_closure_credit") != 0:
            raise RuntimeError("predecessor rejection replay")
        return {"action": "replayed", "file_sha256": b.sha(raw),
                "object_sha256": value["object_sha256"]}
    value = b.close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
        "status": f"PERMANENT_FAIL_CLOSED_{PREV.upper()}_STATIC_BUILD__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": f"{PREV.upper()}_NAMESPACE_TAG_CENSUS_FAILED_BEFORE_CANDIDATE_INSTALL",
        "detail": {"candidate_install": False, "runtime_protocol_executed": False,
                    "required_successor_fix": f"parameterized dynamic {TAG} retag"},
        "append_only": True, "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "manifest_created": False, "outer_created": False,
        "runtime_surface_created": False,
    })
    raw = b.canon(value) + b"\n"
    action = b.install(path, raw)
    installed, installed_raw = b.load(path)
    return {"action": action, "file_sha256": b.sha(installed_raw),
            "object_sha256": installed["object_sha256"]}


def main() -> int:
    before_pyc = pyc_inventory()
    if any(TAG in path for path in before_pyc):
        print(json.dumps({"status": f"FAIL_CLOSED_{TAG.upper()}_PYC_PREEXISTS",
                          "formal_global_closure_credit": 0, "D02_unlock": False}, sort_keys=True))
        return 1
    try:
        if pyc_inventory() != before_pyc:
            raise RuntimeError("initial pyc inventory drift")
        global b
        b = load_generic()
        bind_builder()
        anchor_in = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
        if not anchor_in.is_file():
            raise RuntimeError("missing immutable predecessor anchor")
        configure_builder(anchor_in)
        rej = predecessor_rejection()
        b.CHECKPOINT = SUCCESSOR_PIN
        chain = b.ensure_successor_anchor()
        b.CHECKPOINT = UPSTREAM
        inputs = [*b.SRC_IN.values(), *b.JSON_IN.values(), b.ANCHOR_IN, b.REJ]
        targets = [*b.SRC_OUT.values(), *b.JSON_OUT.values(), b.MANIFEST, b.OUTER]
        if any(not path.is_file() for path in inputs):
            raise RuntimeError(f"immutable r23/{PREV} input missing")
        if any(path.exists() for path in targets):
            raise RuntimeError(f"{TAG} target exists")
        generated, meta = b.build()
        audit = path_crosscheck(generated)
        if pyc_inventory() != before_pyc:
            raise RuntimeError("pyc inventory changed before install")
        actions: dict[str, str] = {}
        for name in ("schema", "contract", "transition", "audit"):
            actions[name] = b.install(b.JSON_OUT[name], generated[name])
        for name in ("producer", "consumer", "launcher"):
            actions[name] = b.install(b.SRC_OUT[name], generated[name], 0o664)
        if b.MANIFEST.exists() or b.OUTER.exists():
            raise RuntimeError("manifest/outer appeared")
        if pyc_inventory() != before_pyc:
            raise RuntimeError("pyc inventory changed after install")
        result = {"schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
                  "status": f"{TAG.upper()}_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
                  "template_namespace": TEMPLATE, "active_predecessor": PREV,
                  "predecessor_rejection": rej, "chain": chain, "actions": actions,
                  "meta": meta, "preinstall_path_crosscheck": audit,
                  "candidate_install": True, "manifest_created": False,
                  "outer_created": False, "runtime_authorized": False,
                  "formal_global_closure_credit": 0, "D02_unlock": False,
                  "pyc_created": False}
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
                          "status": f"FAIL_CLOSED_{TAG.upper()}_STATIC_BUILD",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "candidate_install": False, "formal_global_closure_credit": 0,
                          "D02_unlock": False, "runtime_authorized": False},
                         ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
