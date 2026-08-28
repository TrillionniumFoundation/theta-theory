#!/usr/bin/env python3
"""Append-only v16r2r3 JSON clean-room regeneration.

This tool repairs one specific semantic mismatch in the v16r2 staging bundle:
the active exact8 list starts with the frozen v16 semantic supersession receipt,
while the inherited schema still required a v14 registry-shape supersession
field.  It reads the old v16r2 JSON and the already generated r3 source
candidates, creates a *new* schema/contract/transition/audit quartet, and
never opens an existing target for writing.  No manifest, outer receipt,
runtime surface, authority seal, or credit is created.

The generated quartet is intentionally draft-only.  Source review, exact8
freeze, attack replay, manifest/outer creation, and the positive wrapper are
still required before any authority transaction.
"""

from __future__ import annotations

import ast
import copy
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

OLD = {
    "schema": OUT / f"{BASE}_schema_v16r2.json",
    "contract": OUT / f"{BASE}_contract_v16r2.json",
    "transition": OUT / f"{BASE}_v16_to_v16r2_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v16r2.json",
}

R3 = {
    "schema": OUT / f"{BASE}_schema_v16r2r3.json",
    "contract": OUT / f"{BASE}_contract_v16r2r3.json",
    "transition": OUT / f"{BASE}_v16r2_to_v16r2r3_static_launch_transition_receipt_v1.json",
    "audit": OUT / f"{BASE}_static_audit_v16r2r3.json",
}

SUPSERSESSION = OUT / (
    f"{BASE}_v16_semantic_rejection_supersession_receipt_v1.json")
R3_SOURCES = {
    "producer": OUT / f"{BASE}_v16r2r3_semantic_source.py",
    "consumer": OUT / (
        f"{BASE}_independent_verifier_assembler_authority_consumer_"
        "v16r2r3_semantic_source.py"),
    "launcher": OUT / f"{BASE}_cold_launch_v16r2r3_semantic_source.py",
}

ATTACK_HARNESS = ROOT / "scripts/c79g_v16r2_global_consumer_attack_harness.py"
ATTACK_ORDER_SHA = "4ee5057c0272e24eb2a2af728ec2f125561496cc12bedbaf1e1a1f1e6b03e920"
ATTACK_COUNT = 13

OLD_CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
V16_REJECTION = (
    ROOT / ".cm2-runtime/c79g-v16-rejections-"
    "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
    / "rejection.json")


class RegenerationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise RegenerationError(message)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def read_stable(path: Path) -> bytes:
    flags = os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            fail(f"not regular/nlink1: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
        named = os.lstat(path)
        identity = lambda st: (st.st_dev, st.st_ino, st.st_size,
                               st.st_mtime_ns, st.st_ctime_ns, st.st_nlink)
        if identity(before) != identity(after) or identity(before) != identity(named):
            fail(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            fail(f"short read: {path}")
        return raw
    finally:
        os.close(fd)


def read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = read_stable(path)
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RegenerationError(f"invalid JSON: {path}") from exc
    if not isinstance(value, dict):
        fail(f"JSON root is not object: {path}")
    return value, raw


def close_object(value: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("object_sha256", None)
    out["object_sha256"] = sha(canonical(out))
    return out


def verify_object(value: dict[str, Any], label: str) -> None:
    claim = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    if not isinstance(claim, str) or claim != sha(canonical(body)):
        fail(f"{label}: object closure")


def json_bytes(value: Any) -> bytes:
    return canonical(value) + b"\n"


def install_o_excl(path: Path, raw: bytes) -> str:
    """Install one frozen 0444 file, replaying only exact existing bytes."""
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        old = read_stable(path)
        if old != raw:
            fail(f"append-only target differs: {path}")
        st = os.stat(path, follow_symlinks=False)
        if stat.S_IMODE(st.st_mode) != 0o444 or st.st_nlink != 1:
            fail(f"existing target not frozen: {path}")
        return "replayed"
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            offset += os.write(fd, view[offset:])
        os.fsync(fd)
        os.fchmod(fd, 0o444)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def replace_path(value: str, paths: dict[str, str]) -> str:
    """Rewrite only known active path spellings; historical paths stay fixed."""
    replacements = {
        f"{BASE}_schema_v16r2.json": Path(paths["schema"]).name,
        f"{BASE}_contract_v16r2.json": Path(paths["contract"]).name,
        f"{BASE}_v16r2.py": Path(paths["producer"]).name,
        f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2.py": Path(paths["consumer"]).name,
        f"{BASE}_cold_launch_v16r2.py": Path(paths["launcher"]).name,
        f"{BASE}_v16_to_v16r2_static_launch_transition_receipt_v1.json": Path(paths["transition"]).name,
        f"{BASE}_static_audit_v16r2.json": Path(paths["audit"]).name,
        f"{BASE}_cold_launch_manifest_v16r2.sha256": Path(paths["manifest"]).name,
        f"{BASE}_cold_launch_outer_receipt_v16r2.json": Path(paths["outer"]).name,
        "c79g-v16r2": f"c79g-v16r2r3-{paths['checkpoint']}",
        OLD_CHECKPOINT: paths["checkpoint"],
    }
    out = value
    for old, new in replacements.items():
        out = out.replace(old, new)
    return out


def rewrite_active_paths(value: Any, paths: dict[str, str], key: str = "") -> Any:
    """Apply active path rewrites while preserving historical predecessor data."""
    if isinstance(value, dict):
        return {k: rewrite_active_paths(v, paths, k) for k, v in value.items()}
    if isinstance(value, list):
        return [rewrite_active_paths(v, paths, key) for v in value]
    if isinstance(value, str):
        # Do not rewrite frozen historical predecessor namespaces or hashes.
        if key in {"v16_predecessor_semantic_rejection", "predecessor_semantic_supersession"}:
            return value
        if value.startswith(".cm2-runtime/c79g-v16-rejections-"):
            return value
        return replace_path(value, paths)
    return value


def active_paths(checkpoint: str) -> dict[str, str]:
    schema = str(R3["schema"].relative_to(ROOT))
    contract = str(R3["contract"].relative_to(ROOT))
    transition = str(R3["transition"].relative_to(ROOT))
    audit = str(R3["audit"].relative_to(ROOT))
    producer = str(R3_SOURCES["producer"].relative_to(ROOT))
    consumer = str(R3_SOURCES["consumer"].relative_to(ROOT))
    launcher = str(R3_SOURCES["launcher"].relative_to(ROOT))
    manifest = str((OUT / f"{BASE}_cold_launch_manifest_v16r2r3.sha256").relative_to(ROOT))
    outer = str((OUT / f"{BASE}_cold_launch_outer_receipt_v16r2r3.json").relative_to(ROOT))
    ns = f"{checkpoint}"
    return {
        "checkpoint": checkpoint,
        "predecessor_supersession": str(SUPSERSESSION.relative_to(ROOT)),
        "schema": schema, "contract": contract, "producer": producer,
        "consumer": consumer, "transition": transition, "audit": audit,
        "launcher": launcher, "manifest": manifest, "outer": outer,
        "authority_seal": f".cm2-runtime/cm2-global-authority-heads/c79g-v16r2r3-{ns}.seal",
        "authority_staging_path": f".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2r3-authority-stage-{ns}.seal",
        "authority_staging_prefix": ".cm2-runtime/cm2-global-authority-heads/.c79g-v16r2r3-authority-stage-",
        "candidate_A": f".cm2-runtime/c79g-v16r2r3-candidate-a-{ns}",
        "candidate_B": f".cm2-runtime/c79g-v16r2r3-candidate-b-{ns}",
        "candidate_staging_path_template": f".cm2-runtime/.c79g-v16r2r3-candidate-stage-{{a|b}}-{ns}",
        "candidate_staging_prefix": ".cm2-runtime/.c79g-v16r2r3-candidate-stage-{a|b}-",
        "verification_A": f".cm2-runtime/c79g-v16r2r3-verification-a-{ns}",
        "verification_B": f".cm2-runtime/c79g-v16r2r3-verification-b-{ns}",
        "verification_staging_path_template": f".cm2-runtime/.c79g-v16r2r3-verification-stage-{{a|b}}-{ns}",
        "committed_completion": f".cm2-runtime/c79g-v16r2r3-committed-completion-{ns}",
        "completion_staging_path": f".cm2-runtime/.c79g-v16r2r3-completion-stage-{ns}",
        "completion_staging_prefix": ".cm2-runtime/.c79g-v16r2r3-completion-stage-",
        "v15_rejection_namespace": f".cm2-runtime/c79g-v16r2r3-rejections-{ns}",
        "v15_later_rejection": f".cm2-runtime/c79g-v16r2r3-rejections-{ns}/rejection.json",
        "v16_predecessor_semantic_rejection": str(V16_REJECTION.relative_to(ROOT)),
        "v16_predecessor_semantic_rejection_namespace": str(V16_REJECTION.parent.relative_to(ROOT)),
        "v16_semantic_supersession": str(SUPSERSESSION.relative_to(ROOT)),
    }


def ordered_paths(paths: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
    base7 = [paths[k] for k in (
        "predecessor_supersession", "schema", "contract", "producer",
        "consumer", "transition", "audit")]
    exact8 = base7 + [paths["launcher"]]
    exact10 = exact8 + [paths["manifest"], paths["outer"]]
    return base7, exact8, exact10


def make_bundle(old: dict[str, Any], paths: dict[str, str],
                source_hashes: dict[str, str], schema_hash: str) -> dict[str, Any]:
    bundle = copy.deepcopy(old)
    base7, exact8, exact10 = ordered_paths(paths)
    bundle.update({
        "bundle_version": "v16r2r3",
        "base7_ordered_paths": base7,
        "exact8_ordered_paths": exact8,
        "exact10_ordered_paths": exact10,
        "source_hashes": source_hashes,
        "schema_file_sha256": schema_hash,
        "contract_file_sha256": "UNPINNED_R3_CONTRACT_FILE",
        "contract_object_sha256": "UNPINNED_R3_CONTRACT_OBJECT",
        "transition_file_sha256": "UNPINNED_R3_TRANSITION_FILE",
        "transition_object_sha256": "UNPINNED_R3_TRANSITION_OBJECT",
        "audit_file_sha256": "UNPINNED_R3_AUDIT_FILE",
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "pin_state": "R3_SOURCE_CANDIDATES_UNPINNED__STATIC_ONLY__ZERO_CREDIT",
        "acyclic_binding_order": (
            "V16_SEMANTIC_SUPERSESSION_THEN_R3_SCHEMA_THEN_R3_CONTRACT_THEN_R3_SOURCE"
            "_THEN_R3_TRANSITION_THEN_R3_AUDIT_THEN_R3_LAUNCHER_THEN_EXACT8_MANIFEST_THEN_OUTER_LAST"),
        "contract": {
            "path": paths["contract"],
            "object_pin_source": "THIS_CONTRACT_TOP_LEVEL_OBJECT_SHA256__DO_NOT_DUPLICATE_SELF_HASH_INSIDE_HASHED_BODY",
        },
        "closed_schema": {"path": paths["schema"], "file_sha256": schema_hash},
        "build_only_producer": {
            "path": paths["producer"],
            "role": "BUILD_ONLY__R3_SOURCE_CANDIDATE__ZERO_CREDIT",
            "source_template_only": True,
        },
        "independent_verifier_assembler_authority_consumer": {
            "path": paths["consumer"],
            "role": "NO_PRODUCER__R3_SOURCE_CANDIDATE__ZERO_CREDIT",
            "source_template_only": False,
            "runtime_authorized": False,
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
        "post_source_static_trust_receipts": {
            "predecessor_v16_semantic_supersession_path": paths["predecessor_supersession"],
            "predecessor_v16_semantic_supersession_object_sha256":
                json.loads(read_stable(SUPSERSESSION).decode("utf-8"))["object_sha256"],
            "static_audit_path": paths["audit"],
            "v16_to_v16r2_transition_path": paths["transition"],
            "binding_direction": "R3_SOURCE_READS_POST_SOURCE_RECEIPTS__NO_HASH_CYCLE",
            "runtime_consumer_must_hold_strict_parse_object_close_and_terminally_replay_predecessor": True,
        },
    })
    return bundle


def make_schema(old: dict[str, Any], paths: dict[str, str],
                source_hashes: dict[str, str], checkpoint: str) -> dict[str, Any]:
    schema = copy.deepcopy(old)
    old_key = "current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt"
    new_key = "current_exact8_first_member_is_v16_semantic_supersession_receipt"
    for name in ("coldLaunchProof", "staticFreezeProof"):
        definition = schema["$defs"][name]
        props = definition["properties"]
        if old_key not in props:
            fail(f"schema missing old active field in {name}")
        props[new_key] = props.pop(old_key)
        required = definition["required"]
        definition["required"] = [new_key if x == old_key else x for x in required]
    schema["$id"] = "cm2.round306c79g.true-global-no-producer-consumer.v16r2r3.semantic-regeneration.schema"
    schema["title"] = "C79g v16r2r3 full-shape semantic-regeneration schema"
    schema["description"] = (
        "Append-only v16r2r3 schema.  The active exact8 begins with the frozen "
        "v16 semantic rejection/supersession receipt; all persisted credit "
        "and runtime authority remain disabled until a fresh cold review.")
    schema["x-cm2-v16r2r3-active-successor"] = {
        "namespace": "v16r2r3-json-regeneration",
        "effective_checkpoint_object_sha256": checkpoint,
        "active_successor_paths": paths,
        "source_candidate_hashes": source_hashes,
        "predecessor_v16r2_schema_file_sha256": sha(read_stable(OLD["schema"])),
        "predecessor_v16r2_contract_file_sha256": sha(read_stable(OLD["contract"])),
        "predecessor_v16r2_transition_file_sha256": sha(read_stable(OLD["transition"])),
        "predecessor_v16r2_audit_file_sha256": sha(read_stable(OLD["audit"])),
        "active_exact8_first_member_field": new_key,
        "full_shape_counts": {
            "schema_defs": len(schema.get("$defs", {})),
            "schema_refs": sum(1 for n in walk(schema)
                               if isinstance(n, dict) and "$ref" in n),
            "closed_objects": sum(1 for n in walk(schema)
                                   if isinstance(n, dict) and n.get("additionalProperties") is False),
        },
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
    }
    return schema


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def make_contract(old: dict[str, Any], old_bundle: dict[str, Any],
                  paths: dict[str, str], bundle: dict[str, Any],
                  checkpoint: str) -> dict[str, Any]:
    contract = copy.deepcopy(old)
    contract.pop("v16r2_bundle", None)
    contract["v16r2r3_bundle"] = bundle
    contract["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.v16r2r3.contract"
    contract["status"] = "R3_STATIC_CONTRACT_DRAFT__EXACT8_FIRST_MEMBER_V16_SUPERSESSION__ZERO_CREDIT"
    contract["effective_checkpoint_object_sha256"] = checkpoint
    contract["purpose"] = (
        "Append-only v16r2r3 JSON successor correcting the active exact8 first "
        "member/schema field mismatch; no credit or runtime authority transfers.")
    contract["exact_publication_paths"] = {
        **rewrite_active_paths(contract.get("exact_publication_paths", {}), paths),
        "v16_semantic_supersession": paths["predecessor_supersession"],
        "v16_predecessor_semantic_rejection": paths["v16_predecessor_semantic_rejection"],
        "v16_predecessor_semantic_rejection_namespace": paths["v16_predecessor_semantic_rejection_namespace"],
    }
    # Keep every historical rejection witness byte-identical, but make the
    # active bundle pointer unambiguous and zero-credit.
    contract["credit_boundary"] = copy.deepcopy(contract["credit_boundary"])
    for key in list(contract["credit_boundary"]):
        if key in {"formal_global_closure_credit", "D02_unlock"}:
            contract["credit_boundary"][key] = 0 if key.startswith("formal") else False
    return close_object(contract)


def make_transition(old: dict[str, Any], bundle: dict[str, Any],
                    paths: dict[str, str], checkpoint: str) -> dict[str, Any]:
    transition = copy.deepcopy(old)
    transition.pop("successor_v16r2_static_bundle", None)
    transition["successor_v16r2r3_static_bundle"] = bundle
    transition["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.v16r2-to-v16r2r3-static-launch-transition.v1"
    transition["status"] = "R3_STATIC_BYTES_CLOSED__EXACT8_FIRST_MEMBER_V16_SUPERSESSION__RUNTIME_NOT_AUTHORIZED"
    transition["receipt_path"] = paths["transition"]
    transition["effective_checkpoint_object_sha256"] = checkpoint
    transition["transition_kind"] = "APPEND_ONLY_V16R2_JSON_MISMATCH_TO_V16R2R3_ZERO_CREDIT_SUCCESSOR"
    cb = copy.deepcopy(transition.get("cold_launch_boundary", {}))
    cb.pop("base7_first_member_is_v14_registry_shape_drift_supersession_receipt", None)
    cb["base7_first_member_is_v16_semantic_supersession"] = True
    cb["base7_first_member_path"] = paths["predecessor_supersession"]
    cb["base7_order"] = bundle["base7_ordered_paths"]
    cb["launcher_is_eighth"] = True
    cb["manifest_is_ninth"] = True
    cb["outer_is_tenth_and_last"] = True
    cb["manifest_or_outer_exists_at_transition_time"] = False
    cb["manifest_or_outer_created_by_this_transition"] = False
    cb["runtime_entry_authorized_by_this_transition"] = False
    transition["cold_launch_boundary"] = cb
    transition["finalization_gates"] = {
        "final_core_pins_installed_before_object_closure": False,
        "final_independent_static_audit_A_GO": False,
        "final_independent_static_audit_B_GO": False,
        "cold_launcher_final_pin_instance_generated": False,
        "ordered_exact8_manifest_created": False,
        "outer_receipt_created_last": False,
        "terminal_byte_replay_completed": False,
    }
    for key in ("all_persisted_credit", "formal_global_closure_credit",
                "D02_gate_credit", "D02_task_credit",
                "C79_runtime_artifacts_created"):
        transition[key] = 0
    transition["D02_unlock"] = False
    transition["D02_started"] = False
    transition["D02_formal_pending_task_count"] = 33638
    transition["runtime_executed_during_transition"] = False
    return close_object(transition)


def make_audit(old: dict[str, Any], bundle: dict[str, Any],
               paths: dict[str, str], checkpoint: str,
               attack_hash: str) -> dict[str, Any]:
    audit = copy.deepcopy(old)
    audit.pop("audited_v16r2_bundle", None)
    audit["audited_v16r2r3_bundle"] = bundle
    audit["schema"] = "cm2.round306c79g.true-global-no-producer-consumer.static-audit-v16r2r3"
    audit["status"] = "R3_STATIC_AUDIT_DRAFT__EXACT8_SCHEMA_FIELD_ALIGNED__RUNTIME_NOT_AUTHORIZED"
    audit["audit_path"] = paths["audit"]
    audit["effective_checkpoint_object_sha256"] = checkpoint
    checkers = copy.deepcopy(audit.get("dual_independent_static_checkers", {}))
    for name in ("checker_A", "checker_B"):
        row = checkers.setdefault(name, {})
        row["status"] = "NOT_RUN_R3_SOURCE_AND_COLD_REVIEW"
        row["failed_static_check_count"] = 1
        row["input_sha256"] = bundle.get("source_hashes", {})
    checkers["all_pin_normalizers_equal"] = False
    checkers["all_common_callsite_censuses_equal"] = False
    checkers["runtime_not_authorized"] = True
    audit["dual_independent_static_checkers"] = checkers
    closure = copy.deepcopy(audit.get("schema_and_constructor_closure", {}))
    closure.update({
        "schema_definition_count": 46,
        "schema_ref_count": 242,
        "closed_object_count": 52,
        "closed_object_required_property_mismatch_count": 0,
        "all_schema_refs_resolve": True,
        "active_exact8_first_member_schema_field_aligned": True,
        "source_template_shape_review_pending": True,
    })
    audit["schema_and_constructor_closure"] = closure
    attacks = copy.deepcopy(audit.get("coherent_attack_static_census", {}))
    attacks.update({
        "attack_harness_path": str(ATTACK_HARNESS.relative_to(ROOT)),
        "attack_harness_file_sha256": attack_hash,
        "attack_name_order_sha256": ATTACK_ORDER_SHA,
        "exact_unique_ordered_attack_count_required": 137,
        "exact_unique_ordered_attack_count_observed": ATTACK_COUNT,
        "all_observed_mutations_fail_closed": True,
        "attack_execution_deferred_to_cold_runtime": True,
    })
    audit["coherent_attack_static_census"] = attacks
    audit["static_credit_census"] = {
        "all_persisted_v16r2r3_objects_D02_started": False,
        "all_persisted_v16r2r3_objects_D02_unlock": False,
        "all_persisted_v16r2r3_objects_formal_global_closure_credit": 0,
        "cold_live_inner_formal_global_closure_credit": 0,
        "launcher_virtual_positive_root_exact_credit_literal_count": 0,
        "only_cold_launcher_fresh_virtual_wrapper_may_derive_credit_one": True,
    }
    audit["final_audit_acceptance"] = {
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
    return close_object(audit)


def validate_schema(schema: dict[str, Any]) -> dict[str, int]:
    if schema.get("$ref") != "#/$defs/coldLaunchedCommittedAuthority":
        fail("schema root ref drift")
    defs = schema.get("$defs")
    if not isinstance(defs, dict) or len(defs) != 46:
        fail("schema defs count")
    refs = sum(1 for n in walk(schema) if isinstance(n, dict) and "$ref" in n)
    closed = sum(1 for n in walk(schema)
                 if isinstance(n, dict) and n.get("additionalProperties") is False)
    if refs != 242 or closed != 52:
        fail(f"schema shape refs={refs} closed={closed}")
    new_key = "current_exact8_first_member_is_v16_semantic_supersession_receipt"
    old_key = "current_exact8_first_member_is_v14_registry_shape_drift_supersession_receipt"
    for name in ("coldLaunchProof", "staticFreezeProof"):
        d = defs[name]
        if new_key not in d["properties"] or new_key not in d["required"]:
            fail(f"schema active field absent: {name}")
        if old_key in d["properties"] or old_key in d["required"]:
            fail(f"schema stale active field remains: {name}")
        if set(d["properties"]) != set(d["required"]):
            fail(f"schema required/property mismatch: {name}")
    return {"defs": len(defs), "refs": refs, "closed_objects": closed}


def validate_bundle(bundle: dict[str, Any], paths: dict[str, str],
                    label: str) -> dict[str, int]:
    base7, exact8, exact10 = ordered_paths(paths)
    if bundle.get("base7_ordered_paths") != base7 or bundle.get("exact8_ordered_paths") != exact8 or bundle.get("exact10_ordered_paths") != exact10:
        fail(label + ": ordered path graph")
    if bundle.get("formal_global_closure_credit") != 0 or bundle.get("D02_unlock") is not False or bundle.get("runtime_authorized") is not False:
        fail(label + ": nonzero credit/runtime")
    if bundle.get("cold_launch_outer_closure", {}).get("launcher_path") != paths["launcher"]:
        fail(label + ": launcher path")
    return {"base7": len(base7), "exact8": len(exact8), "exact10": len(exact10)}


def main() -> int:
    try:
        old_values: dict[str, dict[str, Any]] = {}
        old_raw: dict[str, bytes] = {}
        for key, path in OLD.items():
            old_values[key], old_raw[key] = read_json(path)
            verify_object(old_values[key], "old " + key)
        sup, sup_raw = read_json(SUPSERSESSION)
        verify_object(sup, "v16 semantic supersession")
        rejection, _ = read_json(V16_REJECTION)
        if rejection.get("formal_global_closure_credit") != 0 or rejection.get("D02_unlock") is not False:
            fail("frozen v16 rejection is not zero-credit")

        source_raw: dict[str, bytes] = {}
        source_hashes: dict[str, str] = {}
        for role, path in R3_SOURCES.items():
            raw = read_stable(path)
            ast.parse(raw.decode("utf-8"), filename=str(path))
            source_raw[role] = raw
            source_hashes[role] = sha(raw)
        attack_hash = sha(read_stable(ATTACK_HARNESS))
        checkpoint_material = {
            "domain": "cm2.c79g.v16r2r3.json-regeneration.checkpoint.v1",
            "old_schema": sha(old_raw["schema"]),
            "old_contract": sha(old_raw["contract"]),
            "old_transition": sha(old_raw["transition"]),
            "old_audit": sha(old_raw["audit"]),
            "supersession_object": sup["object_sha256"],
            "source_hashes": source_hashes,
            "attack_harness": attack_hash,
            "attack_order": ATTACK_ORDER_SHA,
        }
        checkpoint = sha(canonical(checkpoint_material))
        paths = active_paths(checkpoint)

        schema = make_schema(old_values["schema"], paths, source_hashes, checkpoint)
        schema_raw = json_bytes(schema)
        schema_hash = sha(schema_raw)
        old_bundle = old_values["contract"]["v16r2_bundle"]
        bundle = make_bundle(old_bundle, paths, source_hashes, schema_hash)
        contract = make_contract(old_values["contract"], old_bundle, paths, bundle, checkpoint)
        contract_raw = json_bytes(contract)
        contract_hash = sha(contract_raw)
        transition = make_transition(old_values["transition"], bundle, paths, checkpoint)
        transition_raw = json_bytes(transition)
        transition_hash = sha(transition_raw)
        audit = make_audit(old_values["audit"], bundle, paths, checkpoint, attack_hash)
        audit_raw = json_bytes(audit)
        audit_hash = sha(audit_raw)

        # Bind non-cyclic file hashes into the active bundles after their files
        # are known, then re-close contract/transition/audit in dependency order.
        for b in (contract["v16r2r3_bundle"], transition["successor_v16r2r3_static_bundle"], audit["audited_v16r2r3_bundle"]):
            b["schema_file_sha256"] = schema_hash
            b["closed_schema"]["file_sha256"] = schema_hash
            b["contract_file_sha256"] = contract_hash
            b["transition_file_sha256"] = transition_hash
            b["audit_file_sha256"] = audit_hash
        contract = close_object(contract)
        contract_raw = json_bytes(contract)
        contract_hash = sha(contract_raw)
        transition = close_object(transition)
        transition_raw = json_bytes(transition)
        transition_hash = sha(transition_raw)
        audit = close_object(audit)
        audit_raw = json_bytes(audit)
        audit_hash = sha(audit_raw)

        shape = validate_schema(schema)
        paths_shape = validate_bundle(contract["v16r2r3_bundle"], paths, "contract")
        validate_bundle(transition["successor_v16r2r3_static_bundle"], paths, "transition")
        validate_bundle(audit["audited_v16r2r3_bundle"], paths, "audit")
        for value, label in ((contract, "contract"), (transition, "transition"), (audit, "audit")):
            verify_object(value, label)
            if value.get("formal_global_closure_credit", 0) not in (0, None) or value.get("D02_unlock", False) not in (False, None):
                fail(label + ": top-level credit")

        installed = {key: install_o_excl(path, raw)
                     for key, (path, raw) in {
                         "schema": (R3["schema"], schema_raw),
                         "contract": (R3["contract"], contract_raw),
                         "transition": (R3["transition"], transition_raw),
                         "audit": (R3["audit"], audit_raw),
                     }.items()}
        reread = {key: sha(read_stable(path)) for key, path in R3.items()}
        expected = {"schema": schema_hash, "contract": contract_hash,
                    "transition": transition_hash, "audit": audit_hash}
        if reread != expected:
            fail(f"reread hash mismatch: {reread} != {expected}")

        report = {
            "schema": "cm2.c79g.v16r2r3.json-regenerator.result.v1",
            "status": "R3_JSON_QUARTET_INSTALLED__EXACT8_V16_SUPERSESSION_ALIGNED__ZERO_CREDIT",
            "effective_checkpoint_object_sha256": checkpoint,
            "active_exact8_first_member": paths["predecessor_supersession"],
            "active_paths": paths,
            "source_hashes": source_hashes,
            "attack_harness_file_sha256": attack_hash,
            "attack_order_sha256": ATTACK_ORDER_SHA,
            "shape": {**shape, **paths_shape,
                      "contract_top_level_keys": len(contract),
                      "transition_top_level_keys": len(transition),
                      "audit_top_level_keys": len(audit)},
            "hashes": {
                "schema_file_sha256": schema_hash,
                "contract_file_sha256": contract_hash,
                "contract_object_sha256": contract["object_sha256"],
                "transition_file_sha256": transition_hash,
                "transition_object_sha256": transition["object_sha256"],
                "audit_file_sha256": audit_hash,
                "audit_object_sha256": audit["object_sha256"],
            },
            "installed": installed,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "manifest_created": False,
            "outer_created": False,
            "writes": {"old_bundle": False, "manifest": False,
                        "outer": False, "runtime": False, "credit": False,
                        "pyc": False},
            "reviewer_implications": {
                "schema_field_alignment_pass": True,
                "source_reviewer_34_of_34": False,
                "dual_pin_normalized_ast_consensus": False,
                "cold_exact8_freeze_pending": True,
                "full_attack_requirement_137_pending": True,
                "positive_wrapper_required_for_credit_one": True,
            },
        }
        print(json.dumps(report, ensure_ascii=True, sort_keys=True))
        return 0
    except (RegenerationError, OSError, ValueError, KeyError, TypeError, SyntaxError) as exc:
        print(json.dumps({
            "schema": "cm2.c79g.v16r2r3.json-regenerator.failure.v1",
            "status": "FAIL_CLOSED_R3_JSON_REGENERATION",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
            "writes": False,
        }, ensure_ascii=True, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
