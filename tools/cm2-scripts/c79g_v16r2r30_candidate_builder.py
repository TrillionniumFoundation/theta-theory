#!/usr/bin/env python3
"""Append-only r30 static successor with canonical b58 runtime paths.

r29 passed the two independent byte reviewers, but its executable source still
constructed the current C79g runtime surfaces with the successor/rejection pin
(``dd9``) and with the ``semantic-source`` namespace.  r30 is a fresh static
candidate derived from the immutable r23 template.  It first seals r29 as a
zero-credit rejection, then creates a new r29 -> r30 supersession/anchor using
O_EXCL.  Current executable paths and the contract's exact-publication paths
are normalized to the upstream C53 pin (b58); dd9 is retained only as the
successor checkpoint constant and in the append-only rejection chain.

No candidate source is imported as a protocol, no manifest/outer/runtime
surface is created, and no credit/authority state is touched.  The only source
execution below is a synthetic definition-only smoke test in memory, followed
by an independent path cross-check before any candidate byte is installed.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import os
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE_PREFIX = "cm2_round306c79g_true_global_no_producer_consumer"
TEMPLATE = "v16r2r23"
TEMPLATE_PREV = "v16r2r22"
PREV = "v16r2r29"
TAG = "v16r2r30"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_PIN = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"


def load_generic():
    path = ROOT / "scripts/c79g_v16r2r19_candidate_builder.py"
    spec = importlib.util.spec_from_file_location("_r30_generic_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("generic builder import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


b = load_generic()
b.BASE = BASE_PREFIX
b.R16 = TEMPLATE
b.PREV = PREV
b.TAG = TAG
b.UPSTREAM = UPSTREAM
b.CHECKPOINT = UPSTREAM
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
OLD_EDGE = f"{BASE_PREFIX}_{TEMPLATE_PREV}_to_{TEMPLATE}_static_launch_transition_receipt_v1.json"
OLD_ANCHOR = f"{BASE_PREFIX}_{TEMPLATE}_active_predecessor_supersession_receipt_v1.json"

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
}


def canonical_runtime_string(value: str) -> str:
    """Normalize only current v16r2 runtime path strings in JSON values."""
    value = value.replace(
        "c79g-v16r2-semantic-source-candidate-", "c79g-v16r2-candidate-")
    value = value.replace(
        "c79g-v16r2-semantic-source-rejections-", "c79g-v16r2-rejections-")
    # A v16r2 runtime path is current authority-domain data.  The predecessor
    # v16 rejection path is ``c79g-v16-rejections-*`` and is intentionally not
    # matched by this guard.
    if "c79g-v16r2" in value:
        value = value.replace(SUCCESSOR_PIN, UPSTREAM)
    return value


def canonical_exact_paths(value: dict[str, Any]) -> dict[str, Any]:
    out = dict(value)
    for key, path in CANONICAL_RUNTIME.items():
        out[key] = path
    return out


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
        return out
    if isinstance(value, list):
        return [retag(item) for item in value]
    if isinstance(value, str):
        value = (value.replace(OLD_EDGE, EDGE).replace(OLD_ANCHOR, ANCHOR)
                      .replace("V16R2R23", "V16R2R30")
                      .replace("V16R2R22", "V16R2R29")
                      .replace("v16r2r23", "v16r2r30")
                      .replace("v16r2r22", "v16r2r29"))
        return canonical_runtime_string(value)
    return value


def retag_source(text: str) -> str:
    # Source text is not passed through canonical_runtime_string: changing a
    # literal dd9 there would erase SUCCESSOR_CHECKPOINT_OBJECT_PIN.  AST
    # replacement below changes only executable loads of that symbol.
    return (text.replace(OLD_EDGE, EDGE).replace(OLD_ANCHOR, ANCHOR)
            .replace("V16R2R23", "V16R2R30")
            .replace("V16R2R22", "V16R2R29")
            .replace("v16r2r23", "v16r2r30")
            .replace("v16r2r22", "v16r2r29")
            .replace("c79g-v16r2-semantic-source-candidate-",
                     "c79g-v16r2-candidate-")
            .replace("c79g-v16r2-semantic-source-rejections-",
                     "c79g-v16r2-rejections-"))


def _offsets(text: str) -> list[int]:
    offsets: list[int] = []
    total = 0
    for line in text.splitlines(keepends=True):
        offsets.append(total)
        total += len(line.encode("utf-8"))
    return offsets


def upstream_checkpoint_loads(text: str) -> tuple[str, int]:
    """Replace every executable load of CHECKPOINT_OBJECT_PIN with b58.

    The assignment itself (the successor dd9 literal) is deliberately left
    intact.  This makes the only remaining dd9 data in executable source the
    explicit successor constant; all path and preseal derivations use b58.
    """
    tree = ast.parse(text, mode="exec")
    offsets = _offsets(text)
    spans: list[tuple[int, int]] = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Name) and node.id == "CHECKPOINT_OBJECT_PIN"
                and isinstance(node.ctx, ast.Load)):
            spans.append((offsets[node.lineno - 1] + node.col_offset,
                          offsets[node.end_lineno - 1] + node.end_col_offset))
    raw = text.encode("utf-8")
    for start, end in sorted(spans, reverse=True):
        raw = raw[:start] + b"UPSTREAM_CHECKPOINT_OBJECT_PIN" + raw[end:]
    return raw.decode("utf-8"), len(spans)


def source_paths(text: str, role: str) -> str:
    producer = f"{BASE_PREFIX}_{TAG}_semantic_source.py"
    consumer = (f"{BASE_PREFIX}_independent_verifier_assembler_authority_consumer_"
                f"{TAG}_semantic_source.py")
    launcher = f"{BASE_PREFIX}_cold_launch_{TAG}_semantic_source.py"
    text = (text.replace(f"{BASE_PREFIX}_v16r2.py", producer)
                .replace(f"{BASE_PREFIX}_independent_verifier_assembler_authority_consumer_v16r2.py", consumer)
                .replace("independent_verifier_assembler_authority_consumer_v16r2.py",
                         f"independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"))
    old = re.compile(r'SELF\s*==\s*OUT\s*/\s*\(BASE\s*\+\s*"_cold_launch_v16r2\.py"\)')
    text, count = old.subn(f'SELF == OUT / "{launcher}"', text)
    if role == "launcher" and count != 1:
        raise RuntimeError(f"{role}:unsuffixed SELF assertion count={count}")
    if role != "launcher" and count:
        raise RuntimeError(f"{role}:unexpected launcher SELF assertion")
    return text


def launcher_globals(text: str) -> str:
    semantic = f"{BASE_PREFIX}_{TAG}_semantic_source"
    assignment = f'BASE = "{semantic}"'
    if text.count(assignment) != 1:
        raise RuntimeError("launcher semantic BASE assignment shape")
    text = text.replace(assignment,
                        f'HISTORICAL_BASE = "{BASE_PREFIX}"\n{assignment}', 1)
    text = re.sub(r'\bBASE(\s*\+\s*")_', r'HISTORICAL_BASE\1_', text)
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
        raise RuntimeError("launcher historical BASE contamination")
    return text


def replace_pin(text: str, role: str, name: str, value: str) -> str:
    pattern = rf'(?m)^({re.escape(name)}\s*=\s*)"[0-9a-f]{{64}}"\s*$'
    text, count = re.subn(pattern, rf'\1"{value}"', text)
    if count != 1:
        raise RuntimeError(f"{role}:{name}:replacement count {count}")
    return text


def source_census(text: str, role: str) -> None:
    tree = ast.parse(text, mode="exec")
    compile(tree, f"<r30-{role}>", "exec")
    if any(token in text for token in ("v16r2r23", "v16r2r22", "v16r2r28")):
        raise RuntimeError(f"{role}:stale active token")
    if "c79g-v16r2-semantic-source-candidate-" in text or \
            "c79g-v16r2-semantic-source-rejections-" in text:
        raise RuntimeError(f"{role}:semantic-source runtime path remains")
    loads = [node for node in ast.walk(tree)
             if isinstance(node, ast.Name) and
             node.id == "CHECKPOINT_OBJECT_PIN" and
             isinstance(node.ctx, ast.Load)]
    if loads:
        raise RuntimeError(f"{role}:successor pin still used by executable code")
    edges = re.findall(rf'{re.escape(BASE_PREFIX)}_v16r2r\d+_to_v16r2r\d+_static_launch_transition_receipt_v1\.json', text)
    if not edges or any(edge != EDGE for edge in edges):
        raise RuntimeError(f"{role}:active edge census")
    anchors = re.findall(rf'{re.escape(BASE_PREFIX)}_v16r2r\d+_active_predecessor_supersession_receipt_v1\.json', text)
    if not anchors or any(anchor != ANCHOR for anchor in anchors):
        raise RuntimeError(f"{role}:active anchor census")
    ns = re.findall(r'(?m)^ACTIVE_SUCCESSOR_NAMESPACE\s*=\s*"([^"]+)"\s*$', text)
    nst = re.findall(r'(?m)^ACTIVE_SUCCESSOR_NAMESPACE_TAG\s*=\s*"([^"]+)"\s*$', text)
    if ns != [f"{TAG}_semantic_source"] or nst != [f"{TAG}-semantic-regeneration"]:
        raise RuntimeError(f"{role}:namespace/tag census")


def definition_smoke(raw: bytes, role: str) -> dict[str, Any]:
    text = raw.decode("utf-8")
    ns: dict[str, Any] = {"__name__": f"_r30_static_{role}",
                          "__file__": str(b.SRC_OUT[role]),
                          "__package__": None}
    exec(compile(text, str(b.SRC_OUT[role]), "exec"), ns, ns)
    root = ROOT if role != "launcher" else Path("/tmp/cm2-r30-path-crosscheck")
    if role == "launcher":
        ns["configure_workspace_paths"](root)
    if role == "producer":
        expected = {
            "CANDIDATE_A": root / CANONICAL_RUNTIME["candidate_A"],
            "CANDIDATE_B": root / CANONICAL_RUNTIME["candidate_B"],
        }
    else:
        expected = {
            "CANDIDATE_A": root / CANONICAL_RUNTIME["candidate_A"],
            "CANDIDATE_B": root / CANONICAL_RUNTIME["candidate_B"],
            "VERIFICATION_A": root / CANONICAL_RUNTIME["verification_A"],
            "VERIFICATION_B": root / CANONICAL_RUNTIME["verification_B"],
            "COMMITTED_COMPLETION": root / CANONICAL_RUNTIME["committed_completion"],
            "AUTHORITY_SEAL": root / CANONICAL_RUNTIME["authority_seal"],
            "REJECTION_NAMESPACE": root / CANONICAL_RUNTIME["v16r2_rejection_namespace"],
            "LATER_REJECTION": root / CANONICAL_RUNTIME["v16r2_later_rejection"],
        }
    if role == "launcher":
        # The launcher exposes the rejection namespace under the V16R2 name.
        expected = {"V16R2_REJECTION_NAMESPACE": expected["REJECTION_NAMESPACE"],
                    "V16R2_LATER_REJECTION": expected["LATER_REJECTION"]}
    observed: dict[str, str] = {}
    for name, path in expected.items():
        value = ns.get(name)
        if value != path:
            raise RuntimeError(f"{role}:{name} path mismatch:{value!r}!={path!r}")
        observed[name] = str(value)
    if ns.get("UPSTREAM_CHECKPOINT_OBJECT_PIN") != UPSTREAM:
        raise RuntimeError(f"{role}:upstream checkpoint mismatch")
    if ns.get("SUCCESSOR_CHECKPOINT_OBJECT_PIN") != SUCCESSOR_PIN:
        raise RuntimeError(f"{role}:successor checkpoint mismatch")
    return observed


def source_patch(raw: bytes, role: str, paths: dict[str, str], anchor_file: str,
                 anchor_object: str, schema_hash: str, contract_hash: str,
                 contract_object: str, producer_hash: str | None = None,
                 base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
    text = retag_source(raw.decode("utf-8"))
    text = source_paths(text, role)
    text, replaced = upstream_checkpoint_loads(text)
    if replaced == 0:
        raise RuntimeError(f"{role}:no successor checkpoint loads to normalize")
    if role == "launcher":
        text = launcher_globals(text)
    text = replace_pin(text, role, "ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN", anchor_file)
    text = replace_pin(text, role, "ACTIVE_PREDECESSOR_SUPERSESSION_OBJECT_PIN", anchor_object)
    if role != "launcher":
        text = replace_pin(text, role, "CONTRACT_FILE_PIN", contract_hash)
        text = replace_pin(text, role, "CONTRACT_OBJECT_PIN", contract_object)
        text = replace_pin(text, role, "CLOSED_SCHEMA_FILE_PIN", schema_hash)
    if role == "consumer":
        text = replace_pin(text, role, "PRODUCER_SOURCE_PIN", producer_hash or "")
    if role == "launcher":
        if base7 is None:
            raise RuntimeError("launcher BASE7 missing")
        names = [("ACTIVE_PREDECESSOR_SUPERSESSION", "anchor"),
                 ("SCHEMA", "schema"), ("CONTRACT", "contract"),
                 ("PRODUCER", "producer"), ("CONSUMER", "consumer"),
                 ("TRANSITION", "transition"), ("AUDIT", "audit")]
        entries = "    BASE7_PINS.update({\n" + "".join(
            f"        {var}: (\"{base7[key][0]}\", {base7[key][1]!r}),\n"
            for var, key in names) + "    })"
        text, count = re.subn(r"(?s)    BASE7_PINS\.update\(\{.*?\n    \}\)\n    EXACT8",
                              entries + "\n    EXACT8", text, count=1)
        if count != 1:
            raise RuntimeError(f"launcher BASE7 replacement count {count}")
    source_census(text, role)
    blob = (text if text.endswith("\n") else text + "\n").encode("utf-8")
    definition_smoke(blob, role)
    return blob


b.retag = retag
b.source_patch = source_patch


def preinstall_path_crosscheck(generated: dict[str, bytes]) -> dict[str, Any]:
    """Evaluate source path globals against the canonical contract object."""
    contract = json.loads(generated["contract"].decode("utf-8"))
    paths = contract.get("exact_publication_paths")
    if not isinstance(paths, dict):
        raise RuntimeError("contract exact_publication_paths missing")
    for key, expected in CANONICAL_RUNTIME.items():
        if paths.get(key) != expected:
            raise RuntimeError(f"contract path {key}: {paths.get(key)!r}!={expected!r}")
    if any("semantic-source" in str(paths.get(key, ""))
           for key in CANONICAL_RUNTIME):
        raise RuntimeError("contract semantic-source runtime path")
    if any(SUCCESSOR_PIN in str(paths.get(key, ""))
           for key in CANONICAL_RUNTIME):
        raise RuntimeError("contract successor-pin current path")
    observed = {role: definition_smoke(generated[role], role)
                for role in ("producer", "consumer", "launcher")}
    expected_consumer = {
        name: str(ROOT / path) for name, path in {
            "CANDIDATE_A": CANONICAL_RUNTIME["candidate_A"],
            "CANDIDATE_B": CANONICAL_RUNTIME["candidate_B"],
            "VERIFICATION_A": CANONICAL_RUNTIME["verification_A"],
            "VERIFICATION_B": CANONICAL_RUNTIME["verification_B"],
            "COMMITTED_COMPLETION": CANONICAL_RUNTIME["committed_completion"],
            "AUTHORITY_SEAL": CANONICAL_RUNTIME["authority_seal"],
            "REJECTION_NAMESPACE": CANONICAL_RUNTIME["v16r2_rejection_namespace"],
            "LATER_REJECTION": CANONICAL_RUNTIME["v16r2_later_rejection"],
        }.items()
    }
    if observed["consumer"] != expected_consumer:
        raise RuntimeError("consumer/contract canonical path disagreement")
    launcher_root = Path("/tmp/cm2-r30-path-crosscheck")
    expected_launcher = {
        "V16R2_REJECTION_NAMESPACE": str(launcher_root / CANONICAL_RUNTIME["v16r2_rejection_namespace"]),
        "V16R2_LATER_REJECTION": str(launcher_root / CANONICAL_RUNTIME["v16r2_later_rejection"]),
    }
    if observed["launcher"] != expected_launcher:
        raise RuntimeError("launcher/contract canonical rejection path disagreement")
    return {"contract_exact_paths": paths, "source_path_globals": observed,
            "successor_pin_absent_from_current_paths": True,
            "semantic_source_absent_from_current_paths": True}


def seal_r29_rejection() -> dict[str, str]:
    if b.REJ.exists():
        value, raw = b.load(b.REJ)
        if value.get("failed_namespace") != PREV or value.get("formal_global_closure_credit") != 0:
            raise RuntimeError("r29 rejection replay mismatch")
        return {"file_sha256": b.sha(raw), "object_sha256": value["object_sha256"],
                "action": "replayed"}
    value = b.close({
        "schema": f"cm2.c79g.{PREV}.static-bundle-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_V16R2R29_STATIC_BUILD__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "R29_CURRENT_RUNTIME_PATHS_USED_SUCCESSOR_DD9_AND_SEMANTIC_SOURCE_NAMESPACE",
        "detail": {
            "semantic_audit": "current CANDIDATE_A/B, VERIFICATION_A/B, COMMITTED_COMPLETION, AUTHORITY_SEAL, REJECTION_NAMESPACE and stage paths were not canonical b58",
            "required_successor_fix": "r30 canonical b58 runtime path rewrite with semantic-source removed",
            "runtime_protocol_executed": False,
        },
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
    action = b.install(b.REJ, raw)
    installed, installed_raw = b.load(b.REJ)
    return {"file_sha256": b.sha(installed_raw),
            "object_sha256": installed["object_sha256"], "action": action}


def main() -> int:
    inputs = [*b.SRC_IN.values(), *b.JSON_IN.values(), b.ANCHOR_IN]
    targets = [*b.SRC_OUT.values(), *b.JSON_OUT.values(), b.MANIFEST, b.OUTER]
    try:
        if any(not path.is_file() for path in inputs):
            raise RuntimeError("missing immutable r23/r29 input")
        if any(path.exists() for path in targets):
            raise RuntimeError("r30 candidate target already exists")
        rejection = seal_r29_rejection()
        b.CHECKPOINT = SUCCESSOR_PIN
        chain = b.ensure_successor_anchor()
        b.CHECKPOINT = UPSTREAM
        generated, meta = b.build()
        path_audit = preinstall_path_crosscheck(generated)
        actions: dict[str, str] = {}
        for name in ("schema", "contract", "transition", "audit"):
            actions[name] = b.install(b.JSON_OUT[name], generated[name])
        for name in ("producer", "consumer", "launcher"):
            actions[name] = b.install(b.SRC_OUT[name], generated[name], 0o664)
        if b.MANIFEST.exists() or b.OUTER.exists():
            raise RuntimeError("manifest/outer appeared")
        pyc = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*.pyc")
               if TAG in str(path)]
        if pyc:
            raise RuntimeError(f"r30 pyc:{pyc}")
        result = {
            "schema": f"cm2.c79g.{TAG}.candidate-builder.v1",
            "status": "V16R2R30_STATIC_CANDIDATE_INSTALLED__ZERO_CREDIT__RUNTIME_NOT_AUTHORIZED",
            "template_namespace": TEMPLATE,
            "active_predecessor": PREV,
            "r29_rejection": rejection,
            "chain": chain,
            "actions": actions,
            "meta": meta,
            "preinstall_path_crosscheck": path_audit,
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
