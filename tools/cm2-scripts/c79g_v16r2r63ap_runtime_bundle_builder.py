#!/usr/bin/env python3
"""Construct the append-only r63ap static-freeze schema projection successor.

r63ao completed the physical candidate/verification/completion surface and
installed the two-phase authority input seal, but the second authorize was
correctly rejected because ``static_freeze_proof.v8_official_rejection`` was
serialized as the raw historical v8 receipt.  The frozen v16r2 schema places
that field under the current ``laterRejection`` definition.  This successor
keeps the raw v8 receipt and all of its pins untouched, and changes only the
schema-facing projection returned by ``static_freeze_proof``.  Every prior
recipe and every prior publication namespace remains hash-pinned and
append-only.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts/c79g_v16r2r63ao_runtime_bundle_builder.py"
TEMPLATE_SHA256 = "46b3dacc9a35ef2c33cfcc8bbc22a653e091e7525f9b3a303f9502f67e818a70"
R63AN_TEMPLATE = ROOT / "scripts/c79g_v16r2r63an_runtime_bundle_builder.py"
R63AN_TEMPLATE_SHA256 = "c60a91849ef31a119eab5923e96ba0d7e8501c56096a49509d9728eeae7a1de0"
MARKER = "_R63AP_STATIC_FREEZE_SCHEMA_PROJECTION_APPLIED_"


def _projection_patch_source() -> str:
    """Return source injected into the generated consumer module."""
    return r'''# _R63AP_STATIC_FREEZE_SCHEMA_PROJECTION_APPLIED_
def _r63ap_schema_later_rejection_projection(self_guard, freeze_proof):
    """Project the historical v8 evidence into the current frozen envelope."""
    body = {
        "schema": LATER_REJECTION_SCHEMA,
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "effective_checkpoint_object_sha256": UPSTREAM_CHECKPOINT_OBJECT_PIN,
        "namespace_exact_path": DECLARED_REJECTION_NAMESPACE,
        "target_exact_path": DECLARED_LATER_REJECTION,
        "rejection_reason": LATER_REJECTION_REASON,
        "consumer_file_sha256": self_guard.file_sha256,
        "producer_file_sha256": PRODUCER_SOURCE_PIN,
        "contract_file_sha256": CONTRACT_FILE_PIN,
        "contract_object_sha256": CONTRACT_OBJECT_PIN,
        "closed_schema_file_sha256": CLOSED_SCHEMA_FILE_PIN,
        "v4_rejection_supersession_file_sha256":
            V4_REJECTION_SUPERSESSION_FILE_PIN,
        "v4_rejection_supersession_object_sha256":
            V4_REJECTION_SUPERSESSION_OBJECT_PIN,
        "v5_official_rejection_file_sha256": V5_OFFICIAL_REJECTION_FILE_PIN,
        "v5_official_rejection_object_sha256": V5_OFFICIAL_REJECTION_OBJECT_PIN,
        "v6_official_rejection_file_sha256": V6_OFFICIAL_REJECTION_FILE_PIN,
        "v6_official_rejection_object_sha256": V6_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_official_rejection_file_sha256": V7_OFFICIAL_REJECTION_FILE_PIN,
        "v7_official_rejection_object_sha256": V7_OFFICIAL_REJECTION_OBJECT_PIN,
        "v8_official_rejection_file_sha256": V8_OFFICIAL_REJECTION_FILE_PIN,
        "v8_official_rejection_object_sha256": V8_OFFICIAL_REJECTION_OBJECT_PIN,
        "v9_official_rejection_file_sha256": V9_OFFICIAL_REJECTION_FILE_PIN,
        "v9_official_rejection_object_sha256": V9_OFFICIAL_REJECTION_OBJECT_PIN,
        "v10_official_rejection_file_sha256": V10_OFFICIAL_REJECTION_FILE_PIN,
        "v10_official_rejection_object_sha256": V10_OFFICIAL_REJECTION_OBJECT_PIN,
        "v11_official_rejection_file_sha256": V11_OFFICIAL_REJECTION_FILE_PIN,
        "v11_official_rejection_object_sha256": V11_OFFICIAL_REJECTION_OBJECT_PIN,
        "v12_official_rejection_file_sha256": V12_OFFICIAL_REJECTION_FILE_PIN,
        "v12_official_rejection_object_sha256": V12_OFFICIAL_REJECTION_OBJECT_PIN,
        "v7_publication_lock_continuity_incident_object_sha256":
            V7_PUBLICATION_LOCK_CONTINUITY_INCIDENT["object_sha256"],
        "cold_launcher_file_sha256":
            freeze_proof["cold_launcher_identity"]["file_sha256"],
        "cold_manifest_file_sha256":
            freeze_proof["cold_launch_manifest_identity"]["file_sha256"],
        "cold_outer_file_sha256":
            freeze_proof["cold_launch_outer_identity"]["file_sha256"],
        "cold_outer_object_sha256":
            freeze_proof["cold_launch_outer_object_sha256"],
        "official_writer_coordination_lock_policy": {
            "acquired_before_any_runtime_evidence_or_commit_surface_open_for_each_command": True,
            "child_calls_LOCK_UN": False,
            "child_must_duplicate_and_identity_mount_check_inherited_fd": True,
            "coordination_lock_is_not_claimed_as_a_security_boundary_against_noncooperating_same_uid_or_filesystem_administrator": True,
            "launcher_exclusive_lock_must_be_confirmed_by_independent_nonblocking_probe": True,
            "launcher_lock_owner_scope_requirement_includes_child_live_protocol": True,
            "launcher_owned_open_file_description_must_be_inherited_by_child": True,
            "live_st_dev_st_ino_and_stx_mnt_id_must_not_be_persisted": True,
            "lock_api": "launcher_owned_fcntl.flock(LOCK_EX)",
            "mandatory_for_all_official_runtime_writers": True,
            "path": ".cm2-runtime",
            "protocol_requires_launcher_RELEASE_before_normal_child_guard_close": True,
            "required_final_hold_scope": [
                "inner_canonical_stdout_flush",
                "launcher_commit_request",
                "absolute_last_dynamic_terminal_replay",
                "live_ACK_canonical_stdout_flush",
                "launcher_positive_wrapper_raw_fd1_final_newline_write",
                "launcher_RELEASE",
            ],
        },
        "official_writer_coordination_lock_held_for_entire_reject_command": True,
        "target_is_protocol_and_checkpoint_deterministic": True,
        "commit_operation": "O_CREAT_EXCL_FIXED_TARGET_NO_FALLBACK",
        "namespace_at_rest_mode": "0555",
        "namespace_lock_held_write_window_mode": "0755",
        "rejection_file_mode": "0444",
        "rejection_file_nlink": 1,
        "file_fsync_required": True,
        "namespace_fsync_required_after_file_and_after_reseal": True,
        "runtime_parent_fsync_required_after_namespace_creation": True,
        "idempotent_existing_recovery_re_fsyncs_rejection_file_namespace_and_runtime_parent": True,
        "overwrite_delete_or_reuse_allowed": False,
        "partial_malformed_or_extra_namespace_entry_revokes_authority": True,
        "standalone_authority": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": PENDING_D02,
        "D02_started": False,
    }
    return close_object(body)


_r63ap_raw_static_freeze_proof = static_freeze_proof


def static_freeze_proof(*args, **kwargs):
    proof = _r63ap_raw_static_freeze_proof(*args, **kwargs)
    self_guard = args[1] if len(args) > 1 else kwargs.get("self_guard")
    if self_guard is None:
        raise RuntimeError("r63ap static-freeze self guard missing")
    if not isinstance(proof, dict):
        raise RuntimeError("r63ap static-freeze proof is not an object")
    # The raw historical v8 object remains held and hashed by the identity and
    # predecessor fields.  Only this schema-facing member is projected.
    proof["v8_official_rejection"] = _r63ap_schema_later_rejection_projection(
        self_guard, proof)
    return proof
'''


def main(argv: list[str] | None = None) -> int:
    raw = TEMPLATE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != TEMPLATE_SHA256:
        raise RuntimeError("immutable r63ao builder template hash drift")
    base = R63AN_TEMPLATE.read_bytes()
    if hashlib.sha256(base).hexdigest() != R63AN_TEMPLATE_SHA256:
        raise RuntimeError("immutable r63an builder lineage hash drift")

    # Reproduce the r63ao retag exactly, then add one post-constructor source
    # transformation.  No earlier file is opened for mutation or reused as a
    # publication target.
    text = base.decode("utf-8").replace("r63an", "r63ap").replace("R63AN", "R63AP")
    anchor = "\ndef _patch_base_source(source_text: str) -> str:\n"
    if text.count(anchor) != 1:
        raise RuntimeError("r63ap base-source patch anchor drift")
    helper = _projection_patch_source()
    # This function is inserted into the r63an/r63am constructor patch.  It
    # runs at the only layer that owns the generated ``consumer_text`` bytes,
    # after all inherited path/key repairs and immediately before hashing.
    consumer_patch_code = (
        "    _r63ap_static_anchor = \"\\ndef _static_freeze_is_valid(\"\n"
        "    if _r63ap_static_anchor not in consumer_text:\n"
        "        raise RuntimeError(\"r63ap static-freeze source anchor missing\")\n"
        "    if consumer_text.count(_r63ap_static_anchor) != 1:\n"
        "        raise RuntimeError(\"r63ap static-freeze source anchor drift\")\n"
        "    if " + repr(MARKER) + " not in consumer_text:\n"
        "        _r63ap_static_block = " + repr(helper) + "\n"
        "        consumer_text = consumer_text.replace(\n"
        "            _r63ap_static_anchor, \"\\n\" + _r63ap_static_block + _r63ap_static_anchor, 1)\n"
    )
    consumer_patch_def = (
        "def _r63ap_consumer_patch() -> str:\n"
        "    return " + repr(consumer_patch_code) + "\n"
    )
    text = text.replace(anchor, "\n" + consumer_patch_def + anchor, 1)
    consumer_insert_anchor = (
        "    source_text = source_text.replace(consumer_anchor, _consumer_patch() + consumer_anchor, 1)\n")
    if text.count(consumer_insert_anchor) != 1:
        raise RuntimeError("r63ap consumer insertion anchor drift")
    text = text.replace(
        consumer_insert_anchor,
        "    source_text = source_text.replace(consumer_anchor, _consumer_patch() + _r63ap_consumer_patch() + consumer_anchor, 1)\n",
        1,
    )

    # The helper above is inserted into the generated consumer source by the
    # nested compile hook.  Keep a marker in the builder recipe so accidental
    # double application is rejected rather than silently changing bytes.
    if MARKER not in text:
        raise RuntimeError("r63ap projection marker missing")
    ns = {
        "__name__": "_c79g_r63ap_builder_template",
        "__file__": str(ROOT / "scripts/c79g_v16r2r63ap_runtime_bundle_builder.py"),
    }
    exec(compile(text, str(R63AN_TEMPLATE), "exec"), ns, ns)
    return int(ns["main"](sys.argv[1:] if argv is None else argv))


if __name__ == "__main__":
    raise SystemExit(main())
