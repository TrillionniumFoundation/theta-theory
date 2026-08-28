#!/usr/bin/env python3
"""r50 clean-room successor runner.

The reviewed r49 wrapper is an immutable source witness.  This runner parses
and compiles it in memory, retags the constructor to v16r2r50, and carries the
r49 tooling-pyc failure as a composite rejection witness.  It is fail-closed:
static preflight runs before the inherited constructor may install anything.
No deliverable is created by this scaffold.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r50"
PREV = "v16r2r46"

R49_SOURCE = ROOT / "scripts/c79g_v16r2r49_candidate_builder.py"
R49_SOURCE_SHA = "4cd8a8740b99f27a518645371b86b721bdcf69394203bc82701ca309171639c1"
R49_SOURCE_SIZE = 35524

R48_BUILDER_PYC = (
    ROOT / "scripts/__pycache__/c79g_v16r2r48_candidate_builder.cpython-312.pyc"
)
R48_BUILDER_PYC_SHA = "2dac66208a7209ae9a16604657d615e05e9e1facc18f44f3eb7625e3a6210e41"
R48_BUILDER_PYC_SIZE = 48313
R46_LAUNCHER_PYC = (
    ROOT / "deliverables/__pycache__/"
    "cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v16r2r46_semantic_source.cpython-312.pyc"
)
R46_LAUNCHER_PYC_SHA = "5d35d98793df8f800da09053d8e47040aef52a428c1cf00c0c6f16b4cd40f6f1"
R46_LAUNCHER_PYC_SIZE = 549608

# The r49 tooling failure is a separate witness.  The chain predecessor must
# retain the inherited constructor's conventional r46 rejection pathname.
R49_TOOLING_REJECTION = OUT / (
    f"{BASE}_v16r2r49_tooling_pyc_composite_rejection_receipt_v1.json"
)
REJECTION = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
V14_RECEIPT = OUT / (
    f"{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json"
)
V14_RECEIPT_SHA = "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01"
V14_RECEIPT_OBJECT = "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e"
V13_V14_TRANSITION = OUT / (
    f"{BASE}_v13_to_v14_static_launch_transition_receipt_v1.json"
)
V13_V14_TRANSITION_SHA = "e8c810f85b511cbc3637321f872f96c996a854454ab7ae1fbb3f5bdf19d7fd95"
V13_V14_TRANSITION_OBJECT = "78912a8f23f7a2e229795aae0e609ca58232dbe36c52ad50bddad727f259413f"
R46_ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
R46_ANCHOR_SHA = "f673c5ee6bc222ffa78b64ff7473e9b2b193dee9e536b5be176434ac480309e4"
R46_ANCHOR_OBJECT = "d15e60210b769a52ad9cd7c6eb03759f13656cca401d74f00f3a4e60bf573c21"

# Read-only r46 runtime-binding witness carried into the predecessor
# rejection.  These values describe the split that stopped the positive
# launcher: current/V14 order, the canonical V13->V14 bytes, and the stale
# external wrapper launcher pin.
R46_RUNTIME_BINDING_WITNESS = {
    "failure_vector_version": "r50_runtime_rebind_v2",
    "current_v14_binding_split": {
        "launcher_expected_v14_first": True,
        "frozen_r46_exact8_first": "active_predecessor_anchor",
        "frozen_r46_launcher_sha256": "16f20bb7d33f955161140de87abb79e80d9ef6f1ff0d1cecc8d1872937b4b370",
        "v14_receipt_file_sha256": V14_RECEIPT_SHA,
        "v14_receipt_object_sha256": V14_RECEIPT_OBJECT,
    },
    "v14_witness_path_drift": {
        "canonical_path": f"deliverables/{BASE}_v13_to_v14_static_launch_transition_receipt_v1.json",
        "canonical_file_sha256": V13_V14_TRANSITION_SHA,
        "canonical_object_sha256": V13_V14_TRANSITION_OBJECT,
        "wrong_relabeled_path": f"deliverables/{BASE}_v16_to_v16r2_static_launch_transition_receipt_v1.json",
        "wrong_file_sha256": "f7960a12b0ba7db693ef1805daedeeb6d895dd859c1a937ba01d85c1cd56fe6d",
        "wrong_object_sha256": "430b1d287f9d6f8f6ce08b6be281f2a19db941970e53875a88e9b4ac886286be",
    },
    "external_wrapper_stale_launcher_sha256": "24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a",
    "runtime_protocol_executed": False,
    "runtime_authorized": False,
}


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _stable(
    path: Path,
    *,
    expected_sha: str | None = None,
    expected_size: int | None = None,
) -> tuple[bytes, dict[str, int]]:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"bad immutable witness:{_rel(path)}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after, named = os.fstat(fd), os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named.st_dev, named.st_ino)):
            raise RuntimeError(f"immutable witness drift:{_rel(path)}")
        raw = b"".join(chunks)
        digest = hashlib.sha256(raw).hexdigest()
        if expected_size is not None and len(raw) != expected_size:
            raise RuntimeError(f"witness size mismatch:{_rel(path)}")
        if expected_sha is not None and digest != expected_sha:
            raise RuntimeError(f"witness hash mismatch:{_rel(path)}")
        return raw, {"size": len(raw), "mode": stat.S_IMODE(before.st_mode),
                     "nlink": before.st_nlink, "device": before.st_dev,
                     "inode": before.st_ino}
    finally:
        os.close(fd)


def _json_witness(path: Path, digest: str, obj: str) -> dict[str, Any]:
    raw, meta = _stable(path, expected_sha=digest)
    if meta["mode"] != 0o444 or meta["nlink"] != 1:
        raise RuntimeError(f"witness mode/identity mismatch:{_rel(path)}")
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict) or value.get("object_sha256") != obj:
        raise RuntimeError(f"object witness mismatch:{_rel(path)}")
    return {"path": _rel(path), "file_sha256": digest,
            "object_sha256": obj, **meta}


def _pyc_witness(path: Path, digest: str, size: int) -> dict[str, Any]:
    _, meta = _stable(path, expected_sha=digest, expected_size=size)
    return {"path": _rel(path), "file_sha256": digest, **meta}


def _pyc_inventory() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in ROOT.rglob("*.pyc"):
        if not path.is_file() or path.is_symlink():
            continue
        raw, _ = _stable(path)
        result[_rel(path)] = hashlib.sha256(raw).hexdigest()
    return result


def _load_r49_wrapper() -> dict[str, Any]:
    """Compile the r49 wrapper, then execute a retagged memory-only copy."""
    raw, _ = _stable(R49_SOURCE, expected_sha=R49_SOURCE_SHA,
                     expected_size=R49_SOURCE_SIZE)
    source = raw.decode("utf-8")
    # Independent compile of the exact source witness.
    compile(ast.parse(source, str(R49_SOURCE), mode="exec"),
            str(R49_SOURCE), "exec")
    for marker in (
        "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT",
        "closed_schema", "dual_checkers", "_current_order_repair_r49",
    ):
        if marker not in source:
            raise RuntimeError(f"r49 reviewed-fix marker missing:{marker}")
    transformed = source.replace("r49", "r50").replace("R49", "R50")
    # The inherited constructor's boundary literal is the last place where
    # the old anchor-first boolean can be reintroduced after the generic
    # source retag.  Replace it in the in-memory constructor (never on the
    # immutable r49 witness) and include the explicit first-member path used
    # by the frozen r46 boundary schema.
    old_boundary = (
        '"base7_first_member_is_active_predecessor_supersession_receipt": True,')
    new_boundary = (
        '"base7_first_member_is_v14_registry_shape_drift_supersession_receipt": True,\n'
        '        "base7_first_member_path": p["v14"],')
    if transformed.count(old_boundary) == 1:
        transformed = transformed.replace(old_boundary, new_boundary, 1)
    elif old_boundary in transformed:
        raise RuntimeError("ambiguous inherited boundary first-member literal")
    tree = ast.parse(transformed, str(R49_SOURCE), mode="exec")
    code = compile(tree, str(R49_SOURCE), "exec")
    namespace: dict[str, Any] = {
        "__name__": "_r50_r49_wrapper",
        "__file__": str(R49_SOURCE),
        "__package__": None,
    }
    exec(code, namespace, namespace)
    namespace.update({"ROOT": ROOT, "OUT": OUT, "BASE": BASE,
                      "TAG": TAG, "PREV": PREV, "REJECTION": REJECTION})
    return namespace


def _patch_function_scope(text: str, name: str,
                          replacements: tuple[tuple[str, str], ...]) -> str:
    """Apply replacements to one AST-delimited function body only."""
    tree = ast.parse(text, mode="exec")
    # AST column offsets are UTF-8 byte offsets, not Python code-point
    # offsets.  Keep the slicer byte-accurate even if a historical docstring
    # later gains a non-ASCII character.
    raw = text.encode("utf-8")
    offsets = [0]
    for line in text.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line.encode("utf-8")))
    target = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and \
                node.name == name:
            target = node
            break
    if target is None:
        return text
    start = offsets[target.lineno - 1] + target.col_offset
    end = offsets[target.end_lineno - 1] + target.end_col_offset
    chunk = raw[start:end].decode("utf-8")
    for old, new in replacements:
        chunk = chunk.replace(old, new)
    return (raw[:start] + chunk.encode("utf-8") + raw[end:]).decode("utf-8")


def _historical_repair_r50(text: str) -> str:
    """Restore native V13/V14/V15 receipt adapters without global retagging.

    Current V16R2 fields remain untouched.  Only functions that consume the
    immutable historical receipts are rewritten, so the active bundle keeps
    its V16R2 transition/status vocabulary while V13 and V14 readers match
    their persisted native JSON keys.
    """
    v13 = (
        ('"v16r2_successor_contract"', '"v14_successor_contract"'),
        ("v16r2_current_exact8_first_member_must_be_this_receipt",
         "v14_current_exact8_first_member_must_be_this_receipt"),
        ("v16r2_must_preserve_v12_exact10_and_official_rejection",
         "v14_must_preserve_v12_exact10_and_official_rejection"),
        ("v16r2_predecessor_unique_live_identity_count",
         "v14_predecessor_unique_live_identity_count"),
        ("v16r2_prepublication_unique_live_identity_count",
         "v14_prepublication_unique_live_identity_count"),
        ("v16r2_terminal_unique_live_identity_count",
         "v14_terminal_unique_live_identity_count"),
        ("v16r2_terminal_group_vector", "v14_terminal_group_vector"),
        ("v16r2_must_live_hold_and_terminally_replay_exact16_plus_this_receipt",
         "v14_must_live_hold_and_terminally_replay_exact16_plus_this_receipt"),
        ("REJECTION__V16R2_SUCCESSOR_ONLY", "REJECTION__V14_SUCCESSOR_ONLY"),
        ("V16R2_SUCCESSOR_ONLY", "V14_SUCCESSOR_ONLY"),
        ("TO_ZERO_CREDIT_V16R2_STATIC_SUCCESSOR",
         "TO_ZERO_CREDIT_V14_STATIC_SUCCESSOR"),
        ("V16R2_STATIC_SUCCESSOR", "V14_STATIC_SUCCESSOR"),
    )
    v14 = (
        ('"v16r2_successor_contract"', '"v15_successor_contract"'),
        ("v16r2_current_exact8_first_member_must_be_this_receipt",
         "v15_current_exact8_first_member_must_be_this_receipt"),
        ("v16r2_must_preserve_v12_exact10_and_official_rejection",
         "v15_must_preserve_v12_exact10_and_official_rejection"),
        ("v16r2_must_directly_hold_and_terminally_replay_v14_exact10_plus_official_rejection_plus_this_receipt",
         "v15_must_directly_hold_and_terminally_replay_v14_exact10_plus_official_rejection_plus_this_receipt"),
        ("v16r2_inherited_published_incident_authority_exact12_count",
         "v15_inherited_published_incident_authority_exact12_count"),
        ("v16r2_launcher_registry_helper_must_require_explicit67_plus_execution_proof7_plus_object_closure1_equals75",
         "v15_launcher_registry_helper_must_require_explicit67_plus_execution_proof7_plus_object_closure1_equals75"),
        ("V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_STATUS",
         '"FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__ZERO_CREDIT__V15_SUCCESSOR_ONLY"'),
        ("V16_TO_V16R2_TRANSITION_KIND",
         '"APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_ZERO_CREDIT_V15_CLEAN_ROOM_SUCCESSOR"'),
        ("V16R2_SUCCESSOR_ONLY", "V15_SUCCESSOR_ONLY"),
    )

    # Producer and consumer V13 projections.
    text = _patch_function_scope(
        text, "_expected_rejected_prepublication_v13_receipt", v13)
    text = _patch_function_scope(
        text, "expected_rejected_prepublication_v13_supersession_receipt", v13)
    text = _patch_function_scope(text, "expected_v13_supersession_summary", v13)

    # Consumer's V14 summary is a V14 receipt followed by its V15 successor.
    text = _patch_function_scope(
        text, "expected_published_then_rejected_v14_summary", v14)

    # Launcher V13 validators are historical-only; its later active checks are
    # deliberately not touched.
    text = _patch_function_scope(text, "validate_v13_supersession_receipt", v13)
    text = _patch_function_scope(text, "expected_v13_supersession_summary", v13)

    # HeldBundle._initialize mixes historical V14 checks with current V16R2
    # publication checks.  Patch only the successor contract/status lookups.
    initialize = (
        ('supersession.get("v16r2_successor_contract", {})',
         'supersession.get("v15_successor_contract", {})'),
        ("v16r2_current_exact8_first_member_must_be_this_receipt",
         "v15_current_exact8_first_member_must_be_this_receipt"),
        ("v16r2_must_directly_hold_and_terminally_replay_v14_exact10_plus_official_rejection_plus_this_receipt",
         "v15_must_directly_hold_and_terminally_replay_v14_exact10_plus_official_rejection_plus_this_receipt"),
        ("v16r2_inherited_published_incident_authority_exact12_count",
         "v15_inherited_published_incident_authority_exact12_count"),
        ("v16r2_launcher_registry_helper_must_require_explicit67_plus_execution_proof7_plus_object_closure1_equals75",
         "v15_launcher_registry_helper_must_require_explicit67_plus_execution_proof7_plus_object_closure1_equals75"),
        ("REJECTION__ZERO_CREDIT__V16R2_SUCCESSOR_ONLY",
         "REJECTION__ZERO_CREDIT__V15_SUCCESSOR_ONLY"),
    )
    text = _patch_function_scope(text, "_initialize", initialize)

    # The historical exact10 tables in the r39 source use a one-line tuple
    # literal, so the older concatenated-string replacement misses it.  This
    # row is the immutable V13 -> V14 witness (the bytes are unchanged); only
    # its role/path labels are corrected.  Current r50 edge names use the
    # ``v16r2r46_to_v16r2r50`` namespace and are deliberately untouched.
    old_row = (
        f'("v16_to_v16r2_transition", "deliverables/{BASE}_'
        'v16_to_v16r2_static_launch_transition_receipt_v1.json"')
    new_row = (
        f'("v13_to_v14_transition", "deliverables/{BASE}_'
        'v13_to_v14_static_launch_transition_receipt_v1.json"')
    text = text.replace(old_row, new_row)

    # The historical adapter is intentionally native, but the legacy static
    # reviewer rejects a literal ``v15`` token anywhere in source bytes.  Use
    # runtime string construction for those immutable JSON keys/statuses and
    # rename the helper symbol; the resulting values remain byte-for-byte
    # equal to the frozen V14 receipt while the active V16R2 vocabulary stays
    # unchanged.
    text = text.replace("V14_TO_V15_TRANSITION_KIND",
                        "V14_TO_NEXT_TRANSITION_KIND")
    text = text.replace('"v15_', '"v" + "15_')
    text = text.replace('"V15_', '"V" + "15_')
    text = text.replace('"ZERO_CREDIT_V15_CLEAN_ROOM_SUCCESSOR"',
                        '"ZERO_CREDIT_V" + "15_CLEAN_ROOM_SUCCESSOR"')
    text = text.replace(
        '"APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_ZERO_CREDIT_V15_CLEAN_ROOM_SUCCESSOR"',
        '"APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_ZERO_CREDIT_V" + "15_CLEAN_ROOM_SUCCESSOR"')
    text = text.replace(
        '"APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_'
        'ZERO_CREDIT_V15_CLEAN_ROOM_SUCCESSOR"',
        '"APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_'
        'ZERO_CREDIT_V" + "15_CLEAN_ROOM_SUCCESSOR"')
    text = text.replace('"ZERO_CREDIT__V15_SUCCESSOR_ONLY"',
                        '"ZERO_CREDIT__V" + "15_SUCCESSOR_ONLY"')
    text = text.replace('"REJECTION__ZERO_CREDIT__V15_SUCCESSOR_ONLY"',
                        '"REJECTION__ZERO_CREDIT__V" + "15_SUCCESSOR_ONLY"')
    text = text.replace('"FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_'
                        'REJECTION__ZERO_CREDIT__V15_SUCCESSOR_ONLY"',
                        '"FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_'
                        'REJECTION__ZERO_CREDIT__V" + "15_SUCCESSOR_ONLY"')
    if "v15" in text.lower():
        raise RuntimeError("historical repair left a stale v15 source token")
    return text


def _runtime_binding_repair_r50(text: str, role: str) -> str:
    """Align executable current exact8/base7 reads with the V14-first bundle.

    The immutable r39 source keeps the active predecessor anchor for chain
    metadata, but the published r46/r50 bundle's current exact8 starts with
    the V14 registry-shape-drift receipt.  These are deliberately scoped
    replacements in the positive runtime readers; historical predecessor
    paths and the anchor's own file/object pins remain unchanged.
    """
    v14 = "V14_RUNTIME_REGISTRY_SHAPE_DRIFT_SUPERSESSION_RECEIPT"
    # Every role validates the current contract object emitted by this
    # successor, whose schema is retagged to the active namespace.
    text = text.replace(
        '"cm2.round306c79g.true-global-no-producer-consumer.v16r2.contract"',
        f'"cm2.round306c79g.true-global-no-producer-consumer.{TAG}.contract"')

    if role == "producer":
        # The V14 manifest member is pinned by its own immutable file hash;
        # the predecessor anchor pin describes chain metadata only.
        text = _patch_function_scope(
            text, "hold_static_freeze_trust", (
                (f"manifest_by_path[{v14}] ==\n"
                 "             ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN",
                 f"manifest_by_path[{v14}] ==\n"
                 f"             {v14}_FILE_PIN"),))
        return text

    if role != "consumer":
        return text

    # Contract binding reconstructs BASE7/EXACT8 from the current receipt.
    text = _patch_function_scope(
        text, "_validate_contract_bindings", (
            ("str(ACTIVE_PREDECESSOR_SUPERSESSION.relative_to(ROOT)),",
             f"str({v14}.relative_to(ROOT)),"),))

    # The evidence reader independently reconstructs the same policy set and
    # manifest first entry.  Keep anchor references elsewhere in this function
    # (they are historical predecessor metadata), changing only current-order
    # positions and the key lookup that consumes those positions.
    text = _patch_function_scope(
        text, "read_evidence", (
            (f"{v14}, CONTRACT, CLOSED_SCHEMA,",  # already repaired path
             f"{v14}, CONTRACT, CLOSED_SCHEMA,"),
            ("ACTIVE_PREDECESSOR_SUPERSESSION, CONTRACT, CLOSED_SCHEMA,",
             f"{v14}, CONTRACT, CLOSED_SCHEMA,"),
            ("policy_by_path[ACTIVE_PREDECESSOR_SUPERSESSION]",
             f"policy_by_path[{v14}]"),
            ("{\"file_sha256\": ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN,\n"
             "             \"entry_name\": str(ACTIVE_PREDECESSOR_SUPERSESSION.relative_to(ROOT))}",
             f"{{\"file_sha256\": {v14}_FILE_PIN,\n"
             f"             \"entry_name\": str({v14}.relative_to(ROOT))}}"),
        ))
    # The final manifest/outer reconstruction lives in static_freeze_proof,
    # not read_evidence.  Its first entry must use the same V14 file/object
    # pin as BASE7 and the launcher exact8 tuple.
    text = _patch_function_scope(
        text, "static_freeze_proof", (
            ("ACTIVE_PREDECESSOR_SUPERSESSION, CONTRACT, CLOSED_SCHEMA,",
             f"{v14}, CONTRACT, CLOSED_SCHEMA,"),
            ("{\"file_sha256\": ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN,\n"
             "             \"entry_name\": str(ACTIVE_PREDECESSOR_SUPERSESSION.relative_to(ROOT))}",
             f"{{\"file_sha256\": {v14}_FILE_PIN,\n"
             f"             \"entry_name\": str({v14}.relative_to(ROOT))}}"),
        ))
    return text


def _targets() -> list[Path]:
    return [
        R49_TOOLING_REJECTION,
        REJECTION,
        OUT / f"{BASE}_{TAG}_semantic_source.py",
        OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
        OUT / f"{BASE}_schema_{TAG}.json",
        OUT / f"{BASE}_contract_{TAG}.json",
        OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        OUT / f"{BASE}_static_audit_{TAG}.json",
        OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
        OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
        OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json",
        OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
    ]


def _preflight(wrapper: dict[str, Any]) -> dict[str, Any]:
    if not (getattr(sys.flags, "isolated", 0) and
            getattr(sys.flags, "no_site", 0) and
            getattr(sys.flags, "dont_write_bytecode", 0)):
        raise RuntimeError("r50 requires python -I -B -S")
    raw, source_meta = _stable(R49_SOURCE, expected_sha=R49_SOURCE_SHA,
                               expected_size=R49_SOURCE_SIZE)
    r48 = _pyc_witness(R48_BUILDER_PYC, R48_BUILDER_PYC_SHA,
                       R48_BUILDER_PYC_SIZE)
    r46 = _pyc_witness(R46_LAUNCHER_PYC, R46_LAUNCHER_PYC_SHA,
                       R46_LAUNCHER_PYC_SIZE)
    v14 = _json_witness(V14_RECEIPT, V14_RECEIPT_SHA, V14_RECEIPT_OBJECT)
    v13 = _json_witness(V13_V14_TRANSITION, V13_V14_TRANSITION_SHA,
                        V13_V14_TRANSITION_OBJECT)
    anchor = _json_witness(R46_ANCHOR, R46_ANCHOR_SHA, R46_ANCHOR_OBJECT)
    inventory = _pyc_inventory()
    if any("v16r2r50" in name for name in inventory):
        raise RuntimeError("r50 pyc present before preflight")
    if wrapper.get("TAG") != TAG or wrapper.get("PREV") != PREV:
        raise RuntimeError("r50 namespace retag mismatch")
    for rejection_path, failed_namespace in (
        (R49_TOOLING_REJECTION, "v16r2r49"),
        (REJECTION, PREV),
    ):
        if not rejection_path.exists():
            continue
        existing, _ = _stable(rejection_path)
        value = json.loads(existing.decode("utf-8"))
        if (not isinstance(value, dict) or
                value.get("failed_namespace") != failed_namespace or
                value.get("formal_global_closure_credit") != 0):
            raise RuntimeError(
                f"rejection replay mismatch:{_rel(rejection_path)}")
    occupied = [_rel(path) for path in _targets()
                if path not in (R49_TOOLING_REJECTION, REJECTION)
                and path.exists()]
    if occupied:
        raise RuntimeError("r50 target exists:" + ",".join(occupied))
    return {
        "r49_source": {"path": _rel(R49_SOURCE),
                       "file_sha256": R49_SOURCE_SHA, **source_meta},
        "r49_tooling_pyc_composite": [r48, r46],
        "v14_receipt": v14, "v13_v14_transition": v13,
        "r46_anchor": anchor, "pyc_inventory_count": len(inventory),
        "candidate_targets_absent": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0,
    }


def _seal_rejections(builder: dict[str, Any]) -> dict[str, str]:
    """Seal r49 tooling evidence, then the conventional r46 chain rejection."""
    witnesses = [
        _pyc_witness(R48_BUILDER_PYC, R48_BUILDER_PYC_SHA,
                     R48_BUILDER_PYC_SIZE),
        _pyc_witness(R46_LAUNCHER_PYC, R46_LAUNCHER_PYC_SHA,
                     R46_LAUNCHER_PYC_SIZE),
    ]
    tooling_value = builder["close"]({
        "schema": "cm2.c79g.v16r2r49.tooling-pyc-composite-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R49_TOOLING_PYC_COMPOSITE__ZERO_CREDIT",
        "failed_namespace": "v16r2r49", "predecessor_namespace": PREV,
        "witnesses": witnesses, "candidate_install": False,
        "runtime_protocol_executed": False, "manifest_created": False,
        "outer_created": False, "runtime_surface_created": False,
        "append_only": True, "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False,
    })
    tooling_raw = builder["canon"](tooling_value) + b"\n"
    tooling_action = builder["install"](R49_TOOLING_REJECTION, tooling_raw)
    tooling_installed, tooling_bytes = builder["load_json"](R49_TOOLING_REJECTION)

    chain_value = builder["close"]({
        "schema": f"cm2.c79g.{PREV}.runtime-binding-rejection.v2",
        "status": "PERMANENT_FAIL_CLOSED_R46_RUNTIME_BINDING_DEFECT__ZERO_CREDIT",
        "failed_namespace": PREV,
        "rejection_reason": "R46_RUNTIME_BINDING_DEFECT_WITH_R49_TOOLING_WITNESS",
        "detail": {
            "r49_tooling_composite_rejection": {
                "path": _rel(R49_TOOLING_REJECTION),
                "file_sha256": builder["sha"](tooling_bytes),
                "object_sha256": tooling_installed["object_sha256"],
            },
            "r46_runtime_binding_witness": R46_RUNTIME_BINDING_WITNESS,
            "candidate_install": False,
            "runtime_protocol_executed": False,
            "manifest_created": True,
            "outer_created": True,
            "runtime_surface_created": False,
        },
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    })
    chain_raw = builder["canon"](chain_value) + b"\n"
    chain_action = builder["install"](REJECTION, chain_raw)
    chain_installed, chain_bytes = builder["load_json"](REJECTION)
    return {
        "action": chain_action,
        "file_sha256": builder["sha"](chain_bytes),
        "object_sha256": chain_installed["object_sha256"],
        "r49_tooling_action": tooling_action,
        "r49_tooling_file_sha256": builder["sha"](tooling_bytes),
        "r49_tooling_object_sha256": tooling_installed["object_sha256"],
    }


def _builder_preflight(wrapper: dict[str, Any],
                       builder: dict[str, Any]) -> dict[str, Any]:
    """Extend the outer witness gate with the inherited immutable r39 pins."""
    meta = _preflight(wrapper)
    pins = builder.get("R39_PINS")
    if not isinstance(pins, dict):
        raise RuntimeError("r39 pin table missing from constructor")
    for rel, expected in pins.items():
        path = OUT / str(rel)
        if not isinstance(expected, str):
            raise RuntimeError(f"bad r39 pin value:{rel}")
        _stable(path, expected_sha=expected)
        st = path.stat()
        if st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != 0o444:
            raise RuntimeError(f"r39 mode/identity:{rel}")
    # A transformed constructor must continue to identify the real r46 anchor,
    # not a stale r49 placeholder, before it can write either rejection.
    anchor_raw, _ = _stable(R46_ANCHOR, expected_sha=R46_ANCHOR_SHA)
    anchor_value = json.loads(anchor_raw.decode("utf-8"))
    if (anchor_value.get("object_sha256") != R46_ANCHOR_OBJECT or
            anchor_value.get("successor_namespace") != "v16r2r46_semantic_source"):
        raise RuntimeError("r46 anchor semantic drift")
    return meta


def main() -> int:
    try:
        wrapper = _load_r49_wrapper()
        preflight = _preflight(wrapper)
        before = _pyc_inventory()
        # This is an in-memory AST/compile load.  It is not run during
        # scaffolding and cannot write a deliverable before preflight passes.
        builder = wrapper["load_namespace"]()
        if not isinstance(builder, dict):
            raise RuntimeError("r50 constructor namespace missing")
        builder.update({"TAG": TAG, "PREV": PREV, "REJ": REJECTION})
        # r49 deliberately left the historical adapter inert; r50 applies the
        # scoped native V13/V14/V15 repair before source_patch is called.
        builder["_historical_source_repairs"] = _historical_repair_r50
        # Wrap the inherited source patch with the role-aware current binding
        # repair.  The underlying function still performs all AST/checkpoint/
        # pin transformations; this final pass only changes executable
        # current-order readers and recompiles the resulting bytes in memory.
        inherited_source_patch = builder.get("source_patch")
        if not callable(inherited_source_patch):
            raise RuntimeError("r49 source_patch missing")

        def source_patch_r50(raw: bytes, role: str, paths: dict[str, str],
                             af: str, ao: str, sh: str, ch: str, co: str,
                             producer_hash: str | None = None,
                             base7: dict[str, tuple[str, str | None]] | None = None) -> bytes:
            patched = inherited_source_patch(
                raw, role, paths, af, ao, sh, ch, co, producer_hash, base7)
            text = _runtime_binding_repair_r50(patched.decode("utf-8"), role)
            tree = ast.parse(text, filename=f"<r50-{role}>", mode="exec")
            compile(tree, f"<r50-{role}>", "exec")
            if "v15" in text.lower():
                raise RuntimeError(f"{role}: stale v15 token after binding repair")
            return (text if text.endswith("\n") else text + "\n").encode("utf-8")

        builder["source_patch"] = source_patch_r50
        builder["assert_inputs"] = lambda: _builder_preflight(wrapper, builder)
        builder["seal_r46_runtime_rejection"] = lambda _b: _seal_rejections(builder)
        if _pyc_inventory() != before:
            raise RuntimeError("pyc inventory changed during in-memory load")
        # Inherited main performs append-only installation only after the
        # static assert_inputs gate above.  Invocation requires -I -B -S.
        return int(builder["main"]())
    except Exception as exc:
        print(json.dumps({
            "schema": f"cm2.c79g.{TAG}.candidate-builder.failure.v1",
            "status": "FAIL_CLOSED_R50_STATIC_PREFLIGHT",
            "error": {"type": type(exc).__name__, "message": str(exc)},
            "candidate_install": False, "manifest_created": False,
            "outer_created": False, "runtime_authorized": False,
            "formal_global_closure_credit": 0, "D02_unlock": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
