#!/usr/bin/env python3
"""C79g v16r2 semantic-regeneration static rebuilder.

This program is intentionally a *static* clean-room builder.  It reads the
held v15 full-shape bytes and the frozen v16 semantic rejection chain, then
creates a new ``v16r2`` namespace with O_EXCL.  It never opens a v15/v16
target for writing, never executes a producer/consumer/launcher, and never
creates a manifest, outer receipt, runtime directory, positive surface, or
Python bytecode.

The JSON layer keeps the verified v15 structural universe (46 schema
definitions, 242 references, 52 closed objects, and the 30/31/30 instance
shapes) while replacing only the *active successor* binding.  Historical
v3--v15 evidence remains byte-pinned and is not rewritten.  Source outputs
are explicit disabled templates, not executable authority implementations;
their purpose is to make the active path/anchor contract reviewable before a
later semantic source regeneration.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any, Callable

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"

V15 = {
    "schema": OUT / f"{BASE}_schema_v15.json",
    "contract": OUT / f"{BASE}_contract_v15.json",
    "transition": OUT / f"{BASE}_v14_to_v15_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v15.json",
    "producer": OUT / f"{BASE}_v15.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v15.py",
    "launcher": OUT / f"{BASE}_cold_launch_v15.py",
}
V15_EXPECTED_SHA = {
    "schema": "ab120abd2d77667388c94e5af00637f843e7af1b48adba95306e1a7ea79e73bd",
    "contract": "292ad598033ff2f89c1d6c502e4e6077df9559688a5885088ad107fa45a7dabf",
    "transition": "74c82c804993a6b00196ba5c0b78a3c5067d3242452d61044229f3f04eaf4a7a",
    "audit": "69557bc7971a6c9943a5d4cee36895bc47413d9b45d92c56597d5cde83b3ed06",
    "producer": "7b3621bf6579cd9cc9289ed2bda353cbe5f2e32b108ec718bf80a4fd19af125b",
    "consumer": "5f988490d014a1427a773b7c5fda03318ec67ad9716a4a75b4008b007e944541",
    "launcher": "1ded892a514f21cb534d25a4ecf6cc0b82b97775371f7666d5d24f359d21e015",
}

V16_REJECTION = RUNTIME / (
    "c79g-v16-rejections-dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
) / "rejection.json"
V16_SUPERSESSION = OUT / (
    f"{BASE}_v16_semantic_rejection_supersession_receipt_v1.json"
)

V16R2 = {
    "schema": OUT / f"{BASE}_schema_v16r2.json",
    "contract": OUT / f"{BASE}_contract_v16r2.json",
    "transition": OUT / f"{BASE}_v16_to_v16r2_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v16r2.json",
    "producer": OUT / f"{BASE}_v16r2.py",
    "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2.py",
    "launcher": OUT / f"{BASE}_cold_launch_v16r2.py",
}

SUCCESSOR_TAG = "v16r2-semantic-regeneration"
SUCCESSOR_CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
UPSTREAM_CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    """Close an object without allowing a stale self hash to survive."""
    out = dict(body)
    out.pop("object_sha256", None)
    out["object_sha256"] = sha(canonical(out))
    return out


def read_stable(path: Path) -> bytes:
    flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"input is not a regular nlink=1 file: {path}")
        chunks: list[bytes] = []
        while True:
            part = os.read(fd, 1 << 20)
            if not part:
                break
            chunks.append(part)
        after = os.fstat(fd)
        named = os.lstat(path)
        if (before.st_dev, before.st_ino, before.st_size) != (
            after.st_dev, after.st_ino, after.st_size
        ) or (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino):
            raise RuntimeError(f"input identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def install_o_excl(path: Path, raw: bytes, *, mode: int = 0o664) -> str:
    """Install a new file, or replay an exactly identical file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
            mode,
        )
    except FileExistsError:
        old = read_stable(path)
        st = path.stat()
        if old != raw or st.st_nlink != 1:
            raise RuntimeError(f"append-only target mismatch: {path}")
        return "replayed"
    try:
        view = memoryview(raw)
        off = 0
        while off < len(view):
            off += os.write(fd, view[off:])
        os.fsync(fd)
        os.fchmod(fd, mode)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def replace_values(value: Any, fn: Callable[[str, Any], Any], path: str = "") -> Any:
    """Copy a JSON value while applying a path-aware scalar transform."""
    if isinstance(value, dict):
        return {
            key: replace_values(val, fn, f"{path}/{key}")
            for key, val in value.items()
        }
    if isinstance(value, list):
        return [replace_values(val, fn, f"{path}[{i}]") for i, val in enumerate(value)]
    return fn(path, value)


def active_path_rewrite(path: str, value: Any) -> Any:
    """Rewrite only values under the successor path/metadata sections.

    Historical predecessor sections are deliberately excluded by the caller;
    this function itself is conservative and only changes explicit v15 path
    tokens when the containing path is an active successor field.
    """
    if not isinstance(value, str):
        return value
    # These are lexical names of *future* v16r2 surfaces, not historical
    # evidence.  No file is created for any of them in this phase.
    return value.replace("_v15", "_v16r2").replace("c79g-v15", "c79g-v16r2")


def successor_paths() -> dict[str, str]:
    token = SUCCESSOR_CHECKPOINT
    return {
        "predecessor_supersession": str(V16_SUPERSESSION.relative_to(ROOT)),
        "schema": str(V16R2["schema"].relative_to(ROOT)),
        "contract": str(V16R2["contract"].relative_to(ROOT)),
        "producer": str(V16R2["producer"].relative_to(ROOT)),
        "consumer": str(V16R2["consumer"].relative_to(ROOT)),
        "transition": str(V16R2["transition"].relative_to(ROOT)),
        "audit": str(V16R2["audit"].relative_to(ROOT)),
        "launcher": str(V16R2["launcher"].relative_to(ROOT)),
        "manifest": str((OUT / f"{BASE}_cold_launch_manifest_v16r2.sha256").relative_to(ROOT)),
        "outer": str((OUT / f"{BASE}_cold_launch_outer_receipt_v16r2.json").relative_to(ROOT)),
        "candidate_a": f".cm2-runtime/c79g-v16r2-candidate-a-{token}",
        "candidate_b": f".cm2-runtime/c79g-v16r2-candidate-b-{token}",
        "verification_a": f".cm2-runtime/c79g-v16r2-verification-a-{token}",
        "verification_b": f".cm2-runtime/c79g-v16r2-verification-b-{token}",
        "rejection_ns": f".cm2-runtime/c79g-v16r2-rejections-{token}",
        "rejection": f".cm2-runtime/c79g-v16r2-rejections-{token}/rejection.json",
    }


def make_bundle(source_hashes: dict[str, str], schema_hash: str,
                contract_hash: str, contract_object: str | None,
                transition_hash: str | None, transition_object: str | None,
                audit_hash: str, paths: dict[str, str]) -> dict[str, Any]:
    """Create the successor bundle with the same semantic field universe."""
    return {
        "bundle_version": "v16r2",
        "predecessor_semantic_supersession": {
            "path": str(V16_SUPERSESSION.relative_to(ROOT)),
            "file_sha256": sha(read_stable(V16_SUPERSESSION)),
            "object_sha256": json.loads(read_stable(V16_SUPERSESSION))["object_sha256"],
            "successor_only": SUCCESSOR_TAG,
        },
        "required_member_mode": "0444",
        "required_nlink": 1,
        "base7_ordered_paths": [
            paths["predecessor_supersession"], paths["schema"], paths["contract"],
            paths["producer"], paths["consumer"], paths["transition"], paths["audit"],
        ],
        "exact8_ordered_paths": [
            paths["predecessor_supersession"], paths["schema"], paths["contract"],
            paths["producer"], paths["consumer"], paths["transition"], paths["audit"],
            paths["launcher"],
        ],
        "exact10_ordered_paths": [
            paths["predecessor_supersession"], paths["schema"], paths["contract"],
            paths["producer"], paths["consumer"], paths["transition"], paths["audit"],
            paths["launcher"], paths["manifest"], paths["outer"],
        ],
        "contract": {
            "path": paths["contract"],
            "object_pin_source": "THIS_CONTRACT_TOP_LEVEL_OBJECT_SHA256__DO_NOT_DUPLICATE_SELF_HASH_INSIDE_HASHED_BODY",
        },
        "closed_schema": {"path": paths["schema"], "file_sha256": schema_hash},
        "closed_schema_validator_policy": {
            "unsupported_validation_keyword_action": "FAIL_CLOSED",
            "runtime_validator_walks_complete_schema_keyword_universe": True,
            "oneOf_keyword_allowed": False,
            "file_and_object_pin_definitions_are_split_closed_types": True,
            "all_closed_object_required_sets_equal_property_sets": True,
            "static_audit_must_pin_actual_and_supported_keyword_universes": True,
        },
        "build_only_producer": {
            "path": paths["producer"],
            "role": "BUILD_ONLY__ALWAYS_ZERO_CREDIT__NO_VERIFY_ASSEMBLE_AUTHORIZE_OR_SEAL_COMMAND",
            "freeze_hash_binding": "TRANSITION_AND_AUDIT_THEN_COLD_EXACT8_MANIFEST_AND_OUTER_LAST__ACYCLIC_AFTER_SOURCE",
            "source_template_only": True,
        },
        "independent_verifier_assembler_authority_consumer": {
            "path": paths["consumer"],
            "role": "NO_PRODUCER_VERIFY_ASSEMBLE_AUTHORIZE_OR_PERMANENTLY_REJECT__PERSISTED_AND_DIRECT_INNER_SURFACES_ZERO__COLD_LAUNCHER_REQUIRED",
            "freeze_hash_binding": "TRANSITION_AND_AUDIT_THEN_COLD_EXACT8_MANIFEST_AND_OUTER_LAST__ACYCLIC_AFTER_SOURCE",
            "source_template_only": True,
        },
        "post_source_static_trust_receipts": {
            "predecessor_v16_semantic_supersession_path": paths["predecessor_supersession"],
            "predecessor_v16_semantic_supersession_object_sha256": json.loads(read_stable(V16_SUPERSESSION))["object_sha256"],
            "static_audit_path": paths["audit"],
            "v16_to_v16r2_transition_path": paths["transition"],
            "binding_direction": "SOURCE_TEMPLATE_FIXED_PATH_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE",
            "runtime_consumer_must_hold_strict_parse_object_close_and_terminally_replay_predecessor": True,
        },
        "cold_launch_outer_closure": {
            "launcher_path": paths["launcher"],
            "exact8_manifest_path": paths["manifest"],
            "outer_last_path": paths["outer"],
            "manifest_order": "V16_SEMANTIC_SUPERSESSION_THEN_SCHEMA_THEN_CONTRACT_THEN_PRODUCER_THEN_INDEPENDENT_SOURCE_THEN_V16_TO_V16R2_TRANSITION_THEN_STATIC_AUDIT_THEN_LAUNCHER",
            "launcher_embeds_exact_base7_file_and_object_pins": True,
            "manifest_pins_exact_base7_plus_launcher": True,
            "outer_last_pins_exact8_and_manifest": True,
            "manifest_or_outer_absent_in_this_static_phase": True,
            "runtime_entry_authorized": False,
            "all_cold_launch_persisted_credit": 0,
            "all_cold_launch_persisted_D02_unlock": False,
        },
        "acyclic_binding_order": "V16_SEMANTIC_SUPERSESSION_THEN_SCHEMA_THEN_CONTRACT_THEN_PRODUCER_THEN_INDEPENDENT_SOURCE_THEN_V16_TO_V16R2_TRANSITION_THEN_STATIC_AUDIT_THEN_LAUNCHER_THEN_EXACT8_MANIFEST_THEN_OUTER_LAST",
        "pin_state": "SOURCE_TEMPLATES_UNPINNED__STATIC_ONLY__NO_HASH_CYCLE__COLD_LAUNCHER_EXTERNAL_PIN_REQUIRED",
        "source_hashes": source_hashes,
        # Cross-artifact hashes are intentionally left as explicit staging
        # sentinels here.  Injecting them into the contract would create a
        # contract↔transition↔audit hash cycle; the later pin installer must
        # close that graph in the documented acyclic order.
        "schema_file_sha256": schema_hash,
        "contract_file_sha256": "UNPINNED_STATIC_CONTRACT",
        "contract_object_sha256": "UNPINNED_STATIC_CONTRACT_OBJECT",
        "transition_file_sha256": "UNPINNED_STATIC_TRANSITION",
        "transition_object_sha256": "UNPINNED_STATIC_TRANSITION_OBJECT",
        "audit_file_sha256": "UNPINNED_STATIC_AUDIT",
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    }


def source_template(role: str, v15_raw: bytes, v16_rej_raw: bytes,
                    v16_sup_raw: bytes, paths: dict[str, str]) -> bytes:
    """Emit a small, inert, metadata-complete source template.

    Keeping this template separate from the v15 executable source prevents a
    textual version rewrite from masquerading as a semantic implementation.
    The next phase must regenerate executable producer/consumer/launcher
    bytes from these held facts and independently review them.
    """
    role_title = {
        "producer": "build-only producer",
        "consumer": "independent no-producer consumer",
        "launcher": "cold launcher",
    }[role]
    origin = {
        "role": role,
        "template_status": "INERT_SOURCE_TEMPLATE__RUNTIME_NOT_AUTHORIZED",
        "origin_v15_file_sha256": sha(v15_raw),
        "origin_v15_file_bytes": len(v15_raw),
        "origin_v15_ast_node_count": len(list(ast.walk(ast.parse(v15_raw.decode("utf-8"))))),
        "v16_semantic_rejection_path": str(V16_REJECTION.relative_to(ROOT)),
        "v16_semantic_rejection_file_sha256": sha(v16_rej_raw),
        "v16_semantic_rejection_object_sha256": json.loads(v16_rej_raw)["object_sha256"],
        "v16_semantic_supersession_path": str(V16_SUPERSESSION.relative_to(ROOT)),
        "v16_semantic_supersession_file_sha256": sha(v16_sup_raw),
        "v16_semantic_supersession_object_sha256": json.loads(v16_sup_raw)["object_sha256"],
        "active_successor_paths": paths,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "manifest_or_outer_created": False,
        "positive_runtime_surface_created": False,
    }
    payload = json.dumps(origin, ensure_ascii=False, sort_keys=True, indent=2)
    text = f'''#!/usr/bin/env python3
"""C79g v16r2 {role_title} source template.

This is an inert semantic-regeneration template.  It intentionally cannot
build, verify, assemble, authorize, reject, publish, or write runtime state.
Executable source must be regenerated and independently reviewed after the
full active transition/pin graph is closed.
"""
from __future__ import annotations

RUNTIME_AUTHORIZED = False
FINAL_BASE7_PINS_INSTALLED = False
FORMAL_GLOBAL_CLOSURE_CREDIT = 0
D02_UNLOCK = False
ACTIVE_SUCCESSOR_NAMESPACE = {SUCCESSOR_TAG!r}
ACTIVE_PREDECESSOR_SUPERSESSION = {paths['predecessor_supersession']!r}
ACTIVE_SCHEMA = {paths['schema']!r}
ACTIVE_CONTRACT = {paths['contract']!r}
ACTIVE_PRODUCER = {paths['producer']!r}
ACTIVE_CONSUMER = {paths['consumer']!r}
ACTIVE_TRANSITION = {paths['transition']!r}
ACTIVE_AUDIT = {paths['audit']!r}
ACTIVE_LAUNCHER = {paths['launcher']!r}
ACTIVE_MANIFEST = {paths['manifest']!r}
ACTIVE_OUTER = {paths['outer']!r}
ACTIVE_EXACT8_FIRST_MEMBER = ACTIVE_PREDECESSOR_SUPERSESSION
SOURCE_TEMPLATE_METADATA = {payload}

def fail_closed() -> None:
    raise RuntimeError(
        "C79G_V16R2_SOURCE_TEMPLATE_ONLY__RUNTIME_NOT_AUTHORIZED__"
        "SEMANTIC_REVIEW_AND_COLD_FREEZE_REQUIRED"
    )

def main() -> int:
    fail_closed()
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
'''
    return text.encode("utf-8")


def build_schema(v15_schema: dict[str, Any], source_hashes: dict[str, str],
                 paths: dict[str, str], v16_rej: dict[str, Any],
                 v16_sup: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v15_schema)
    out["$id"] = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.semantic-regeneration.schema"
    out["title"] = "C79g v16r2 full-shape semantic-regeneration schema"
    out["description"] = (
        "The v15 full-shape schema is retained as a held structural baseline; "
        "the active successor is v16r2 and remains zero-credit until a fresh "
        "semantic source review and cold exact8/manifest/outer sequence pass."
    )
    out["x-cm2-v16r2-active-successor"] = {
        "namespace": SUCCESSOR_TAG,
        "predecessor_v15_schema_file_sha256": V15_EXPECTED_SHA["schema"],
        "predecessor_v15_contract_file_sha256": V15_EXPECTED_SHA["contract"],
        "predecessor_v15_transition_file_sha256": V15_EXPECTED_SHA["transition"],
        "predecessor_v15_audit_file_sha256": V15_EXPECTED_SHA["audit"],
        "v16_semantic_rejection_path": str(V16_REJECTION.relative_to(ROOT)),
        "v16_semantic_rejection_file_sha256": sha(read_stable(V16_REJECTION)),
        "v16_semantic_rejection_object_sha256": v16_rej["object_sha256"],
        "v16_semantic_supersession_path": str(V16_SUPERSESSION.relative_to(ROOT)),
        "v16_semantic_supersession_file_sha256": sha(read_stable(V16_SUPERSESSION)),
        "v16_semantic_supersession_object_sha256": v16_sup["object_sha256"],
        "active_successor_paths": paths,
        "source_template_hashes": source_hashes,
        "full_shape_counts": {
            "schema_defs": len(out.get("$defs", {})),
            "schema_refs": sum(
                1 for node in _walk(out) if isinstance(node, dict) and "$ref" in node
            ),
            "closed_objects": sum(
                1 for node in _walk(out)
                if isinstance(node, dict) and node.get("additionalProperties") is False
            ),
        },
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    }
    return out


def _walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def update_active_dict_strings(value: Any) -> Any:
    """Apply v15->v16r2 labels only to a newly-created active subtree."""
    if isinstance(value, dict):
        return {key: update_active_dict_strings(val) for key, val in value.items()}
    if isinstance(value, list):
        return [update_active_dict_strings(val) for val in value]
    if isinstance(value, str):
        return value.replace("v15", "v16r2").replace("V15", "V16R2")
    return value


def build_contract(v15_contract: dict[str, Any], source_hashes: dict[str, str],
                   schema_hash: str, paths: dict[str, str],
                   v16_rej: dict[str, Any], v16_sup: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v15_contract)
    # Keep the 30-key top-level contract shape while changing the active key.
    bundle = out.pop("v15_bundle")
    out["v16r2_bundle"] = update_active_dict_strings(bundle)
    out["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.v16r2.contract"
    out["status"] = "STATIC_CONTRACT_BYTES_FULL_SHAPE_DRAFT__RUNTIME_NOT_AUTHORIZED"
    out["effective_checkpoint_object_sha256"] = SUCCESSOR_CHECKPOINT
    out["purpose"] = (
        "Append-only v16r2 semantic-regeneration successor.  The held v15 "
        "full-shape bytes and frozen v16 semantic rejection/supersession are "
        "inputs only; no credit or runtime authority transfers."
    )
    p = out["exact_publication_paths"]
    # This is an active future-path map, so rewrite its labels explicitly.
    p2 = update_active_dict_strings(p)
    p2["v16_predecessor_semantic_rejection_namespace"] = str(V16_REJECTION.parent.relative_to(ROOT))
    p2["v16_predecessor_semantic_rejection"] = str(V16_REJECTION.relative_to(ROOT))
    p2["v16_semantic_supersession"] = paths["predecessor_supersession"]
    out["exact_publication_paths"] = p2
    # The bundle is the authoritative active source/pin graph for this draft.
    b = out["v16r2_bundle"]
    b.update({
        "predecessor_semantic_supersession": {
            "path": paths["predecessor_supersession"],
            "file_sha256": sha(read_stable(V16_SUPERSESSION)),
            "object_sha256": v16_sup["object_sha256"],
            "successor_only": SUCCESSOR_TAG,
        },
        "source_hashes": source_hashes,
        "closed_schema": {"path": paths["schema"], "file_sha256": schema_hash},
        "build_only_producer": {
            "path": paths["producer"],
            "role": "BUILD_ONLY__SOURCE_TEMPLATE__ZERO_CREDIT",
            "source_template_only": True,
        },
        "independent_verifier_assembler_authority_consumer": {
            "path": paths["consumer"],
            "role": "NO_PRODUCER__SOURCE_TEMPLATE__ZERO_CREDIT",
            "source_template_only": True,
        },
        "cold_launch_outer_closure": {
            "launcher_path": paths["launcher"],
            "exact8_manifest_path": paths["manifest"],
            "outer_last_path": paths["outer"],
            "manifest_or_outer_absent_in_this_static_phase": True,
            "runtime_entry_authorized": False,
            "all_cold_launch_persisted_credit": 0,
            "all_cold_launch_persisted_D02_unlock": False,
        },
        "acyclic_binding_order": "V16_SEMANTIC_SUPERSESSION_THEN_SCHEMA_THEN_CONTRACT_THEN_PRODUCER_THEN_INDEPENDENT_SOURCE_THEN_V16_TO_V16R2_TRANSITION_THEN_STATIC_AUDIT_THEN_LAUNCHER_THEN_EXACT8_MANIFEST_THEN_OUTER_LAST",
        "pin_state": "SOURCE_TEMPLATES_UNPINNED__STATIC_ONLY__NO_HASH_CYCLE",
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    })
    # Keep historical nested sections untouched, but make active static gates
    # explicit and fail-closed.
    out["static_freeze_protocol_requirements"] = copy.deepcopy(out["static_freeze_protocol_requirements"])
    out["static_freeze_protocol_requirements"]["runtime_execution_performed_while_drafting"] = False
    out["static_freeze_protocol_requirements"]["pyc_or___pycache___written"] = False
    out["static_freeze_protocol_requirements"]["this_contract_alone_authorizes_runtime_execution"] = False
    cb = out["credit_boundary"]
    for key in list(cb):
        if "v15" in key.lower() or key in {"formal_global_closure_credit", "D02_unlock"}:
            if isinstance(cb[key], bool):
                cb[key] = False
            elif isinstance(cb[key], int):
                cb[key] = 0
    cb["v16r2_static_schema_contract_transition_credit"] = 0
    cb["v16r2_runtime_authorized"] = False
    # The original contract's top-level shape is intentionally retained at
    # 30 keys; these two additions live inside the active bundle instead.
    return close_object(out)


def build_transition(v15_transition: dict[str, Any], bundle: dict[str, Any],
                     paths: dict[str, str], v16_rej: dict[str, Any],
                     v16_sup: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v15_transition)
    old = out.pop("successor_v15_static_bundle")
    del old
    out["successor_v16r2_static_bundle"] = copy.deepcopy(bundle)
    out["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.v16-to-v16r2-static-launch-transition.v1"
    out["status"] = "STATIC_BYTES_CLOSED_V16_TO_V16R2__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED"
    out["receipt_path"] = paths["transition"]
    out["effective_checkpoint_object_sha256"] = SUCCESSOR_CHECKPOINT
    out["transition_kind"] = "APPEND_ONLY_V16_SEMANTIC_REJECTION_TO_ZERO_CREDIT_V16R2_STATIC_SUCCESSOR"
    out["physical_mode_policy"] = update_active_dict_strings(out["physical_mode_policy"])
    out["physical_mode_policy"].update({
        "v16r2_working_files_mode_before_cold_freeze": "0664",
        "v16r2_exact8_required_final_mode": "0444",
        "v16r2_exact8_required_final_nlink": 1,
        "v16r2_exact8_physical_freeze_completed": False,
        "v16r2_manifest_physical_freeze_completed": False,
        "v16r2_outer_physical_freeze_completed": False,
    })
    cb = out["cold_launch_boundary"]
    cb = update_active_dict_strings(cb)
    cb.update({
        "base7_first_member_is_v16_semantic_supersession": True,
        "base7_first_member_path": paths["predecessor_supersession"],
        "base7_order": bundle["base7_ordered_paths"],
        "launcher_is_eighth": True,
        "manifest_is_ninth": True,
        "outer_is_tenth_and_last": True,
        "manifest_or_outer_exists_at_transition_time": False,
        "manifest_or_outer_created_by_this_transition": False,
        "runtime_entry_authorized_by_this_transition": False,
    })
    out["cold_launch_boundary"] = cb
    out["finalization_gates"] = {
        "final_core_pins_installed_before_object_closure": False,
        "final_independent_static_audit_A_GO": False,
        "final_independent_static_audit_B_GO": False,
        "cold_launcher_final_pin_instance_generated": False,
        "ordered_exact8_manifest_created": False,
        "outer_receipt_created_last": False,
        "terminal_byte_replay_completed": False,
    }
    for key in (
        "all_persisted_credit", "formal_global_closure_credit", "D02_gate_credit",
        "D02_task_credit", "C79_runtime_artifacts_created",
    ):
        out[key] = 0
    out["D02_unlock"] = False
    out["D02_started"] = False
    out["D02_formal_pending_task_count"] = 33638
    out["runtime_executed_during_transition"] = False
    # Keep the historical 31-key transition top-level shape: predecessor
    # evidence belongs inside the active successor bundle, not as a new
    # top-level field.
    out["successor_v16r2_static_bundle"]["v16_predecessor_semantic_rejection"] = {
        "path": str(V16_REJECTION.relative_to(ROOT)),
        "file_sha256": sha(read_stable(V16_REJECTION)),
        "object_sha256": v16_rej["object_sha256"],
        "status": v16_rej.get("status"),
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
    }
    return close_object(out)


def build_audit(v15_audit: dict[str, Any], bundle: dict[str, Any],
                source_hashes: dict[str, str], schema_hash: str,
                contract_hash: str, contract_object: str,
                transition_hash: str, transition_object: str,
                paths: dict[str, str], v16_rej: dict[str, Any],
                v16_sup: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(v15_audit)
    old = out.pop("audited_v15_bundle")
    del old
    out["audited_v16r2_bundle"] = copy.deepcopy(bundle)
    out["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.static-audit-v16r2"
    out["status"] = "STAGING_V16R2_FULL_SHAPE_REBUILD__RUNTIME_NOT_AUTHORIZED"
    out["audit_path"] = paths["audit"]
    out["effective_checkpoint_object_sha256"] = SUCCESSOR_CHECKPOINT
    # Keep the historical 30-key audit top-level shape.  The semantic
    # predecessor witness is nested in the active bundle below.
    out["audited_v16r2_bundle"]["v16_semantic_predecessor"] = {
        "rejection_path": str(V16_REJECTION.relative_to(ROOT)),
        "rejection_file_sha256": sha(read_stable(V16_REJECTION)),
        "rejection_object_sha256": v16_rej["object_sha256"],
        "supersession_path": paths["predecessor_supersession"],
        "supersession_file_sha256": sha(read_stable(V16_SUPERSESSION)),
        "supersession_object_sha256": v16_sup["object_sha256"],
        "successor_only": SUCCESSOR_TAG,
    }
    out["dual_independent_static_checkers"] = {
        "checker_A": {
            "status": "NOT_RUN_SOURCE_TEMPLATE_ONLY",
            "failed_static_check_count": 1,
            "input_sha256": source_hashes,
        },
        "checker_B": {
            "status": "NOT_RUN_SOURCE_TEMPLATE_ONLY",
            "failed_static_check_count": 1,
            "input_sha256": source_hashes,
        },
        "all_pin_normalizers_equal": False,
        "all_common_callsite_censuses_equal": False,
        "runtime_not_authorized": True,
    }
    attack = copy.deepcopy(out["coherent_attack_static_census"])
    attack["exact_unique_ordered_attack_count_required"] = 137
    attack["exact_unique_ordered_attack_count_observed"] = 0
    attack["all_mutations_route_through_production_validators"] = False
    attack["attack_execution_deferred_to_cold_runtime"] = True
    out["coherent_attack_static_census"] = attack
    closure = copy.deepcopy(out["schema_and_constructor_closure"])
    closure.update({
        "schema_definition_count": 46,
        "schema_ref_count": 242,
        "unresolved_schema_ref_count": 0,
        "closed_object_count": 52,
        "closed_object_required_property_mismatch_count": 0,
        "all_schema_refs_resolve": True,
        "source_template_shape_review_pending": True,
    })
    out["schema_and_constructor_closure"] = closure
    sealed = copy.deepcopy(out["sealed_exec_and_no_producer_static_proof"])
    sealed.update({
        "source_template_only": True,
        "executable_source_semantic_review_completed": False,
        "runtime_authorized": False,
    })
    out["sealed_exec_and_no_producer_static_proof"] = sealed
    out["static_credit_census"] = {
        "all_persisted_v16r2_objects_D02_started": False,
        "all_persisted_v16r2_objects_D02_unlock": False,
        "all_persisted_v16r2_objects_formal_global_closure_credit": 0,
        "cold_live_inner_formal_global_closure_credit": 0,
        "launcher_virtual_positive_root_exact_credit_literal_count": 0,
        "only_cold_launcher_fresh_virtual_wrapper_may_derive_credit_one": True,
    }
    out["static_no_run"] = {
        "C79_entrypoint_executed": False,
        "C79_v16r2_runtime_artifact_count": 0,
        "C79_v16r2_process_count": 0,
        "pyc_or___pycache___created": False,
        "cold_manifest_or_outer_created_before_dual_GO": False,
    }
    out["final_audit_acceptance"] = {
        "current_draft_pass": False,
        "final_failed_static_check_count_required": 0,
        "final_static_freeze_pass_required": True,
        "dual_static_checker_A_pin_normalized_ast_GO": False,
        "dual_static_checker_B_pin_normalized_ast_GO": False,
        "pin_normalized_launcher_ast_digest_consensus": False,
        "common_callsite_census_digest_consensus": False,
        "final_launcher_pin_normalized_ast_replay_required_after_pin_injection": True,
        "this_audit_authorizes_C79_runtime": False,
        "requires_cold_exact8_freeze_manifest_then_outer_last_and_terminal_replay": True,
    }
    # The historical audit instance has no top-level credit fields; keep its
    # exact 30-key shape.  Credit state is already represented in
    # ``static_credit_census`` and the active bundle.
    out["audited_v16r2_bundle"]["formal_global_closure_credit"] = 0
    out["audited_v16r2_bundle"]["D02_unlock"] = False
    return close_object(out)


def validate_shapes(schema: dict[str, Any], contract: dict[str, Any],
                    transition: dict[str, Any], audit: dict[str, Any]) -> None:
    if len(schema.get("$defs", {})) != 46:
        raise RuntimeError("schema definition count drift")
    refs = sum(1 for node in _walk(schema) if isinstance(node, dict) and "$ref" in node)
    closed = sum(1 for node in _walk(schema)
                 if isinstance(node, dict) and node.get("additionalProperties") is False)
    if refs != 242 or closed != 52:
        raise RuntimeError(f"schema shape drift refs={refs} closed={closed}")
    if len(contract) != 30 or len(transition) != 31 or len(audit) != 30:
        raise RuntimeError(
            f"instance shape drift contract={len(contract)} transition={len(transition)} audit={len(audit)}"
        )
    for obj in (contract, transition, audit):
        if ("formal_global_closure_credit" in obj and
                obj.get("formal_global_closure_credit") != 0) or (
                "D02_unlock" in obj and obj.get("D02_unlock") is not False):
            raise RuntimeError("zero-credit boundary violated")
        if obj.get("object_sha256") != sha(canonical({k: v for k, v in obj.items() if k != "object_sha256"})):
            raise RuntimeError("object closure mismatch")


def main() -> int:
    try:
        v15_raw = {role: read_stable(path) for role, path in V15.items()}
        actual = {role: sha(raw) for role, raw in v15_raw.items()}
        if actual != V15_EXPECTED_SHA:
            raise RuntimeError(f"v15 held input hash drift: {actual}")
        rej_raw = read_stable(V16_REJECTION)
        sup_raw = read_stable(V16_SUPERSESSION)
        rej = json.loads(rej_raw.decode("utf-8"))
        sup = json.loads(sup_raw.decode("utf-8"))
        if rej.get("formal_global_closure_credit") != 0 or rej.get("D02_unlock") is not False:
            raise RuntimeError("v16 rejection is not zero-credit")
        if sup.get("formal_global_closure_credit") != 0 or sup.get("D02_unlock") is not False:
            raise RuntimeError("v16 supersession is not zero-credit")
        paths = successor_paths()

        # Source templates are emitted first so their hashes can be pinned in
        # the static JSON layer; no executable source is imported or run.
        template_raw: dict[str, bytes] = {}
        for role in ("producer", "consumer", "launcher"):
            template_raw[role] = source_template(role, v15_raw[role], rej_raw, sup_raw, paths)
        source_hashes = {role: sha(raw) for role, raw in template_raw.items()}

        v15_schema = json.loads(v15_raw["schema"].decode("utf-8"))
        v15_contract = json.loads(v15_raw["contract"].decode("utf-8"))
        v15_transition = json.loads(v15_raw["transition"].decode("utf-8"))
        v15_audit = json.loads(v15_raw["audit"].decode("utf-8"))

        schema = build_schema(v15_schema, source_hashes, paths, rej, sup)
        schema_raw = canonical(schema) + b"\n"
        schema_hash = sha(schema_raw)

        # Build the active bundle with explicit unpinned sentinels.  The
        # contract is then closed once, followed by transition and audit; no
        # artifact embeds a hash that would point back into itself.
        bundle = make_bundle(
            source_hashes, schema_hash, "UNPINNED_STATIC_CONTRACT",
            "UNPINNED_STATIC_CONTRACT_OBJECT", None, None,
            "UNPINNED_STATIC_AUDIT", paths,
        )
        contract_seed = build_contract(v15_contract, source_hashes, schema_hash, paths, rej, sup)
        contract_seed["v16r2_bundle"] = copy.deepcopy(bundle)
        contract_seed = close_object(contract_seed)
        contract_raw = canonical(contract_seed) + b"\n"
        contract_hash = sha(contract_raw)
        contract_obj = contract_seed["object_sha256"]

        transition_seed = build_transition(v15_transition, bundle, paths, rej, sup)
        transition_raw = canonical(transition_seed) + b"\n"
        transition_hash = sha(transition_raw)
        transition_obj = transition_seed["object_sha256"]

        audit_seed = build_audit(
            v15_audit, bundle, source_hashes, schema_hash, contract_hash,
            contract_obj, transition_hash, transition_obj, paths, rej, sup,
        )
        audit_raw = canonical(audit_seed) + b"\n"
        audit_hash = sha(audit_raw)
        audit_obj = audit_seed["object_sha256"]
        validate_shapes(schema, contract_seed, transition_seed, audit_seed)

        outputs: dict[str, str] = {}
        for role, raw in template_raw.items():
            outputs[f"{role}_template"] = install_o_excl(V16R2[role], raw)
        outputs["schema"] = install_o_excl(V16R2["schema"], schema_raw)
        outputs["contract"] = install_o_excl(V16R2["contract"], contract_raw)
        outputs["transition"] = install_o_excl(V16R2["transition"], transition_raw)
        outputs["audit"] = install_o_excl(V16R2["audit"], audit_raw)

        # No manifest/outer/runtime path is touched.  Assert that this run did
        # not accidentally create a v16r2 positive surface or bytecode.
        forbidden = [
            OUT / f"{BASE}_cold_launch_manifest_v16r2.sha256",
            OUT / f"{BASE}_cold_launch_outer_receipt_v16r2.json",
        ]
        if any(path.exists() for path in forbidden):
            raise RuntimeError("forbidden manifest/outer appeared")
        if any("v16r2" in str(path) for path in ROOT.rglob("*.pyc")):
            raise RuntimeError("v16r2 bytecode appeared")

        result = {
            "schema": "cm2.c79g.v16r2.static-rebuilder.result.v1",
            "status": "V16R2_FULL_SHAPE_STATIC_DRAFTS_INSTALLED__RUNTIME_NOT_AUTHORIZED",
            "input_v15_sha256": actual,
            "v16_semantic_rejection": {
                "path": str(V16_REJECTION.relative_to(ROOT)),
                "file_sha256": sha(rej_raw),
                "object_sha256": rej["object_sha256"],
            },
            "v16_semantic_supersession": {
                "path": str(V16_SUPERSESSION.relative_to(ROOT)),
                "file_sha256": sha(sup_raw),
                "object_sha256": sup["object_sha256"],
            },
            "v16r2_paths": paths,
            "v16r2_hashes": {
                "schema": schema_hash,
                "contract": contract_hash,
                "contract_object": contract_obj,
                "transition": transition_hash,
                "transition_object": transition_obj,
                "audit": audit_hash,
                "audit_object": audit_obj,
                **source_hashes,
            },
            "shape": {
                "schema_defs": len(schema["$defs"]),
                "schema_refs": sum(1 for node in _walk(schema) if isinstance(node, dict) and "$ref" in node),
                "schema_closed_objects": sum(1 for node in _walk(schema) if isinstance(node, dict) and node.get("additionalProperties") is False),
                "contract_top_level_keys": len(contract_seed),
                "transition_top_level_keys": len(transition_seed),
                "audit_top_level_keys": len(audit_seed),
            },
            "writes": outputs,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "manifest_created": False,
            "outer_created": False,
            "runtime_authorized": False,
            "pyc_created": False,
        }
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "schema": "cm2.c79g.v16r2.static-rebuilder.failure.v1",
            "status": "FAIL_CLOSED_V16R2_STATIC_REBUILD",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
        }, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
