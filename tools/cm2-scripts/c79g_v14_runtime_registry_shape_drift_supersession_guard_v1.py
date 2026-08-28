#!/usr/bin/env python3
"""Append-only v14 runtime registry-shape incident supersession guard.

``PREFLIGHT`` is read-only.  ``FREEZE_REJECT`` publishes one canonical,
object-closed receipt from an anonymous ``O_TMPFILE`` inode with a no-replace
``linkat`` operation.  The guard never imports, compiles, or executes any C79g
protocol source; the v14 defect is reconstructed from frozen ASTs only.
"""

from __future__ import annotations

import ast
import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any


FINAL_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_GUARD_PINS_INSTALLED = True
ROOT_EXPECTED = Path(
    "/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
RECEIPT_REL = (
    f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_"
    "supersession_receipt_v1.json")
REJECTION_REL = f".cm2-runtime/c79g-v14-rejections-{CHECKPOINT}/rejection.json"
REJECTION_NAMESPACE_REL = f".cm2-runtime/c79g-v14-rejections-{CHECKPOINT}"


V14_EXACT10: tuple[dict[str, Any], ...] = (
    {
        "name": "v13_prepublication_supersession_receipt",
        "path": f"deliverables/{BASE}_v13_prepublication_pyc_contamination_"
                "rejection_supersession_receipt_v1.json",
        "file_sha256": "098296d9807a89f58250f4fd404bdd45b1cf343e3e2e1c7a51a24d67225d016f",
        "object_sha256": "3c9c44500465c6b416cc0ee6689ea82cdd9096a79687b94f94c409ca5a78c677",
    },
    {
        "name": "closed_schema_v14",
        "path": f"deliverables/{BASE}_schema_v14.json",
        "file_sha256": "3d07ccda67cb71d0e5c64d37c0d8e1fcf425de4fbfefddf03bf43934ffdaaa4d",
    },
    {
        "name": "contract_v14",
        "path": f"deliverables/{BASE}_contract_v14.json",
        "file_sha256": "479a0b3f6b4f0ad7e25d22c9f32eec046758a9a7d40509a6bda200e8e41e0ece",
        "object_sha256": "11fd8966ed631f3bcc0eb6b1881f0536c814b7a7c093eca8289680e38a7d7b8b",
    },
    {
        "name": "build_only_producer_v14",
        "path": f"deliverables/{BASE}_v14.py",
        "file_sha256": "9fa2f2e20cdf15ed37d7f3ff904197fa7bc46a4eec243cab0ae8fb477e2e1ff0",
    },
    {
        "name": "independent_consumer_v14",
        "path": f"deliverables/{BASE}_independent_verifier_assembler_"
                "authority_consumer_v14.py",
        "file_sha256": "83c58e792b922ad57a7c031b4aca60fe4d5868679e6f7a70b513e3cc4b7dc24c",
    },
    {
        "name": "transition_v13_to_v14",
        "path": f"deliverables/{BASE}_v13_to_v14_static_launch_"
                "transition_receipt_v1.json",
        "file_sha256": "e8c810f85b511cbc3637321f872f96c996a854454ab7ae1fbb3f5bdf19d7fd95",
        "object_sha256": "78912a8f23f7a2e229795aae0e609ca58232dbe36c52ad50bddad727f259413f",
    },
    {
        "name": "static_audit_v14",
        "path": f"deliverables/{BASE}_static_audit_v14.json",
        "file_sha256": "dbf5e6bf0f13524ee847d01482f9ad34f715368deb2df40207bd2eb436f293e9",
        "object_sha256": "16a8bc6e274a9e4e5a8fe4b2a39b80136cbbb117bfdf2e0ed89ee90fdc71944a",
    },
    {
        "name": "cold_launcher_v14",
        "path": f"deliverables/{BASE}_cold_launch_v14.py",
        "file_sha256": "1236f53865d69d69d27091758a66b21ddc2ea33ed7f422bc8d56adb69a23f5b5",
    },
    {
        "name": "cold_manifest_v14",
        "path": f"deliverables/{BASE}_cold_launch_manifest_v14.sha256",
        "file_sha256": "aae2b3735ca9d5469d4228189ff0127e85aca934c6e56dfa3650a4d4d46a5937",
    },
    {
        "name": "cold_outer_v14",
        "path": f"deliverables/{BASE}_cold_launch_outer_receipt_v14.json",
        "file_sha256": "fa6d10673d96a36aaf0163c44e014162ffb7811b12b1efa9068d78c8aa5b2040",
        "object_sha256": "786f9be9142ae0aafd31a6d86b08f815d5d4f7ca09fd67506f499635fdddc256",
    },
)

V14_OFFICIAL_REJECTION = {
    "name": "official_v14_later_rejection",
    "path": REJECTION_REL,
    "file_sha256": "1cc1b5836457f219ce26aa8e463ebebe8d48a26d2145806d24f7cbfea6c7e567",
    "object_sha256": "0856353a2390c46b4f4bdefe9f13f6eb6e0e94aa352174cdc8d2f672ace4a41d",
}

EXECUTION_PROOF_EXACT7 = [
    "producer_exec_fd_is_fresh_sealed_memfd",
    "producer_exec_fd_distinct_from_installed_source_fd",
    "producer_exec_memfd_required_seals_valid",
    "producer_exec_bytes_equal_installed_source_bytes",
    "producer_exec_and_installed_source_terminal_replayed",
    "seventeen_incident_authority_inputs_inherited_as_held_fds",
    "seventeen_incident_held_fds_path_identity_mount_and_hash_revalidated",
]
LAUNCHER_HELPER_AST_SHA256 = (
    "f1077fb8a0b14aaeb2d76e5880e9297ef48a35d7a6e338d931df5a2f9c4dedea")
V14_LATER_REJECTION_EXACT56_KEYSET_SHA256 = (
    "9c272f16d92497a7c5ced499e9e42c514b81cbfddcdb3f79c4f33837836e057e")

V14_FORBIDDEN_POSITIVE_AND_STAGE_EXACT12 = (
    f".cm2-runtime/c79g-v14-candidate-a-{CHECKPOINT}",
    f".cm2-runtime/c79g-v14-candidate-b-{CHECKPOINT}",
    f".cm2-runtime/c79g-v14-verification-a-{CHECKPOINT}",
    f".cm2-runtime/c79g-v14-verification-b-{CHECKPOINT}",
    f".cm2-runtime/c79g-v14-committed-completion-{CHECKPOINT}",
    f".cm2-runtime/cm2-global-authority-heads/c79g-v14-{CHECKPOINT}.seal",
    f".cm2-runtime/.c79g-v14-candidate-stage-a-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v14-candidate-stage-b-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v14-verification-stage-a-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v14-verification-stage-b-{CHECKPOINT}",
    f".cm2-runtime/.c79g-v14-completion-stage-{CHECKPOINT}",
    f".cm2-runtime/cm2-global-authority-heads/"
    f".c79g-v14-authority-stage-{CHECKPOINT}.seal",
)


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        assert key not in result, f"duplicate JSON key: {key}"
        result[key] = value
    return result


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    assert "object_sha256" not in body
    result = dict(body)
    result["object_sha256"] = sha256(canonical(body))
    return result


def verify_object(raw: bytes, expected: str) -> dict[str, Any]:
    value = json.loads(raw, object_pairs_hook=strict_pairs)
    assert isinstance(value, dict) and value.get("object_sha256") == expected
    body = dict(value)
    del body["object_sha256"]
    assert sha256(canonical(body)) == expected
    return value


def read_all(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    blocks: list[bytes] = []
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            return b"".join(blocks)
        blocks.append(block)


def write_all(fd: int, raw: bytes) -> None:
    offset = 0
    while offset < len(raw):
        count = os.write(fd, raw[offset:])
        assert count > 0
        offset += count


class Held:
    def __init__(self, root: Path, pin: dict[str, Any]):
        self.root = root
        self.pin = pin
        rel = pin["path"]
        assert rel and not rel.startswith("/") and ".." not in Path(rel).parts
        flags = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW
        if hasattr(os, "O_NOATIME"):
            flags |= os.O_NOATIME
        self.fd = os.open(root / rel, flags)
        try:
            self.initial = os.fstat(self.fd)
            assert stat.S_ISREG(self.initial.st_mode)
            assert stat.S_IMODE(self.initial.st_mode) == 0o444
            assert self.initial.st_nlink == 1
            path_state = os.lstat(root / rel)
            assert (path_state.st_dev, path_state.st_ino) == (
                self.initial.st_dev, self.initial.st_ino)
            self.raw = read_all(self.fd)
            assert sha256(self.raw) == pin["file_sha256"]
            if pin.get("object_sha256") is not None:
                verify_object(self.raw, pin["object_sha256"])
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def replay(self) -> os.stat_result:
        state = os.fstat(self.fd)
        assert stat.S_ISREG(state.st_mode)
        assert stat.S_IMODE(state.st_mode) == 0o444 and state.st_nlink == 1
        assert (state.st_dev, state.st_ino, state.st_size) == (
            self.initial.st_dev, self.initial.st_ino, self.initial.st_size)
        path_state = os.lstat(self.root / self.pin["path"])
        assert (path_state.st_dev, path_state.st_ino) == (
            state.st_dev, state.st_ino)
        actual = read_all(self.fd)
        assert actual == self.raw and sha256(actual) == self.pin["file_sha256"]
        if self.pin.get("object_sha256") is not None:
            verify_object(actual, self.pin["object_sha256"])
        return state

    def close(self) -> None:
        os.close(self.fd)


def one_top_level_function(tree: ast.Module, name: str) -> ast.FunctionDef:
    rows = [node for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == name]
    assert len(rows) == 1
    return rows[0]


def producer_registry_shape(raw: bytes) -> dict[str, Any]:
    tree = ast.parse(raw.decode("utf-8"), filename="producer_v14", mode="exec")
    registry = one_top_level_function(tree, "input_registry")
    held_self_rows = [node for node in tree.body
                      if isinstance(node, ast.ClassDef) and node.name == "HeldSelf"]
    assert len(held_self_rows) == 1
    proof_rows = [node for node in held_self_rows[0].body
                  if isinstance(node, ast.FunctionDef) and
                  node.name == "execution_proof"]
    assert len(proof_rows) == 1
    registry_returns = [
        node for node in ast.walk(registry)
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Call) and
        isinstance(node.value.func, ast.Name) and node.value.func.id == "close_object" and
        len(node.value.args) == 1 and isinstance(node.value.args[0], ast.Dict)]
    proof_returns = [node for node in ast.walk(proof_rows[0])
                     if isinstance(node, ast.Return) and
                     isinstance(node.value, ast.Dict)]
    assert len(registry_returns) == len(proof_returns) == 1
    registry_dict = registry_returns[0].value.args[0]
    proof_dict = proof_returns[0].value
    assert all(key is None or (
        isinstance(key, ast.Constant) and isinstance(key.value, str))
        for key in registry_dict.keys)
    assert all(isinstance(key, ast.Constant) and isinstance(key.value, str)
               for key in proof_dict.keys)
    explicit = [key.value for key in registry_dict.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, str)]
    expansions = [value for key, value in zip(
        registry_dict.keys, registry_dict.values) if key is None]
    proof = [key.value for key in proof_dict.keys
             if isinstance(key, ast.Constant) and isinstance(key.value, str)]
    assert len(explicit) == len(set(explicit)) == 67
    assert len(expansions) == 1
    expansion = expansions[0]
    assert isinstance(expansion, ast.Call)
    assert isinstance(expansion.func, ast.Attribute)
    assert isinstance(expansion.func.value, ast.Name)
    assert expansion.func.value.id == "self_guard"
    assert expansion.func.attr == "execution_proof"
    assert not expansion.args and not expansion.keywords
    assert proof == EXECUTION_PROOF_EXACT7
    return {
        "producer_explicit_registry_key_count": len(explicit),
        "producer_execution_proof_key_count": len(proof),
        "canonical_object_closure_key_count": 1,
        "actual_total_registry_shape": len(explicit) + len(proof) + 1,
        "ordered_execution_proof_exact7": proof,
        "ordered_explicit_registry_keys_sha256": sha256(canonical(explicit)),
    }


def launcher_stale_helper_shape(raw: bytes) -> dict[str, Any]:
    tree = ast.parse(raw.decode("utf-8"), filename="launcher_v14", mode="exec")
    helper = one_top_level_function(tree, "producer_source_registry_shape_from_ast")
    helper_ast_sha = sha256(ast.dump(
        helper, annotate_fields=True, include_attributes=False).encode("utf-8"))
    assert helper_ast_sha == LAUNCHER_HELPER_AST_SHA256
    constants = [node.value for node in ast.walk(helper)
                 if isinstance(node, ast.Constant)]
    assert constants.count(62) == 1
    assert "Derive explicit62 + execution-proof7 + object closure1 structurally." in constants
    assert "current v14 registry explicit62 plus exact execution-proof7" in constants
    assignments = [node for node in tree.body if isinstance(node, ast.Assign) and
                   any(isinstance(target, ast.Name) and
                       target.id == "FINAL_STATIC_AUDIT_OUTPUT_SHAPES"
                       for target in node.targets)]
    assert len(assignments) == 1
    shapes = ast.literal_eval(assignments[0].value)
    assert isinstance(shapes, dict) and shapes.get("producerSourceRegistry") == 75
    return {
        "launcher_helper_ast_sha256": helper_ast_sha,
        "launcher_stale_expected_explicit_registry_key_count": 62,
        "launcher_expected_execution_proof_key_count": 7,
        "launcher_expected_object_closure_key_count": 1,
        "launcher_stale_total_registry_shape": 70,
        "launcher_declared_static_output_shape": 75,
        "launcher_reject_message":
            "current v14 registry explicit62 plus exact execution-proof7",
    }


def stable_output_snapshot(root: Path) -> tuple[Any, ...]:
    output = root / "deliverables"
    state = os.stat(output, follow_symlinks=False)
    return (
        state.st_dev, state.st_ino, stat.S_IMODE(state.st_mode),
        state.st_nlink, state.st_mtime_ns, state.st_ctime_ns,
        tuple(sorted(item.name for item in output.iterdir())),
    )


def validate_runtime_census(root: Path) -> dict[str, Any]:
    runtime = root / ".cm2-runtime"
    names = sorted(item.name for item in runtime.iterdir()
                   if "c79g-v14" in item.name)
    expected = [Path(REJECTION_NAMESPACE_REL).name]
    assert names == expected
    namespace = root / REJECTION_NAMESPACE_REL
    state = os.lstat(namespace)
    assert stat.S_ISDIR(state.st_mode) and stat.S_IMODE(state.st_mode) == 0o555
    assert state.st_nlink == 2
    assert sorted(item.name for item in namespace.iterdir()) == ["rejection.json"]
    forbidden_states = {
        rel: os.path.lexists(root / rel)
        for rel in V14_FORBIDDEN_POSITIVE_AND_STAGE_EXACT12}
    assert len(forbidden_states) == 12 and not any(forbidden_states.values())
    heads = runtime / "cm2-global-authority-heads"
    head_names = (sorted(item.name for item in heads.iterdir()
                         if "c79g-v14" in item.name)
                  if heads.exists() else [])
    assert head_names == []
    return {
        "exact_top_level_c79g_v14_runtime_entry_names": names,
        "exact_authority_heads_c79g_v14_entry_names": head_names,
        "forbidden_positive_and_stage_exact12_paths":
            list(V14_FORBIDDEN_POSITIVE_AND_STAGE_EXACT12),
        "forbidden_positive_and_stage_exact12_all_absent": True,
        "positive_surface_count": 0,
        "deterministic_stage_surface_count": 0,
        "official_rejection_namespace_mode": "0555",
        "official_rejection_namespace_nlink": 2,
        "official_rejection_namespace_exact_member_universe": ["rejection.json"],
    }


def validate_rejection(value: dict[str, Any]) -> None:
    sorted_keys = sorted(value)
    assert len(sorted_keys) == 56
    assert sha256(canonical(sorted_keys)) == \
        V14_LATER_REJECTION_EXACT56_KEYSET_SHA256
    assert value["schema"] == (
        "cm2.round306c79g.true-global-no-producer-consumer.v14.later-rejection")
    assert value["status"] == "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT"
    assert value["rejection_reason"] == "ORPHANED_OR_INCOMPLETE_C79G_V14_SURFACE"
    assert value["formal_global_closure_credit"] == 0
    assert value["D02_unlock"] is False
    assert value["D02_started"] is False
    assert value["D02_gate_credit"] == value["D02_task_credit"] == 0
    assert value["D02_formal_pending_task_count"] == 33638
    assert value["overwrite_delete_or_reuse_allowed"] is False
    assert value["effective_checkpoint_object_sha256"] == CHECKPOINT
    assert value["closed_schema_file_sha256"] == \
        V14_EXACT10[1]["file_sha256"]
    assert value["contract_file_sha256"] == V14_EXACT10[2]["file_sha256"]
    assert value["contract_object_sha256"] == V14_EXACT10[2]["object_sha256"]
    assert value["producer_file_sha256"] == V14_EXACT10[3]["file_sha256"]
    assert value["consumer_file_sha256"] == V14_EXACT10[4]["file_sha256"]
    assert value["cold_launcher_file_sha256"] == V14_EXACT10[7]["file_sha256"]
    assert value["cold_manifest_file_sha256"] == V14_EXACT10[8]["file_sha256"]
    assert value["cold_outer_file_sha256"] == V14_EXACT10[9]["file_sha256"]
    assert value["cold_outer_object_sha256"] == V14_EXACT10[9]["object_sha256"]
    assert value["namespace_exact_path"] == REJECTION_NAMESPACE_REL
    assert value["target_exact_path"] == REJECTION_REL
    assert value["namespace_at_rest_mode"] == "0555"
    assert value["rejection_file_mode"] == "0444"
    assert value["rejection_file_nlink"] == 1


def build_receipt(
        exact10: list[Held], rejection: Held,
        registry: dict[str, Any], launcher: dict[str, Any],
        census: dict[str, Any]) -> dict[str, Any]:
    exact10_rows = []
    for item in exact10:
        row = {
            "name": item.pin["name"], "path": item.pin["path"],
            "file_sha256": item.pin["file_sha256"],
            "mode": "0444", "nlink": 1,
        }
        if item.pin.get("object_sha256") is not None:
            row["object_sha256"] = item.pin["object_sha256"]
        exact10_rows.append(row)
    rejection_row = {
        "path": rejection.pin["path"],
        "file_sha256": rejection.pin["file_sha256"],
        "object_sha256": rejection.pin["object_sha256"],
        "mode": "0444", "nlink": 1,
        "status": "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT",
        "reason": "ORPHANED_OR_INCOMPLETE_C79G_V14_SURFACE",
    }
    return close_object({
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer."
            "v14-runtime-registry-shape-drift-rejection-supersession-receipt.v1"),
        "status": (
            "FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_REJECTION__"
            "ZERO_CREDIT__V15_SUCCESSOR_ONLY"),
        "receipt_path": RECEIPT_REL,
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "transition_kind": (
            "APPEND_ONLY_PUBLISHED_V14_RUNTIME_FAIL_CLOSED_REJECTION_TO_"
            "ZERO_CREDIT_V15_CLEAN_ROOM_SUCCESSOR"),
        "frozen_v14_publication_authority": {
            "ordered_exact10": exact10_rows,
            "ordered_member_count": 10,
            "exact8_then_manifest_then_outer_order_validated": True,
            "all_regular_0444_nlink1_hash_and_object_pins_match": True,
            "joint_same_fd_terminal_replay_before_this_receipt": True,
            "official_later_rejection": rejection_row,
            "outer_strictly_precedes_official_rejection": True,
        },
        "runtime_registry_shape_drift_incident": {
            "incident_id": "V14_LAUNCHER_STALE_EXPLICIT62_VS_PRODUCER_EXPLICIT67",
            "mechanically_reconstructed_from_frozen_source_asts": True,
            "producer_registry_shape": registry,
            "cold_launcher_stale_helper_shape": launcher,
            "shape_delta": registry["actual_total_registry_shape"] -
                           launcher["launcher_stale_total_registry_shape"],
            "runtime_effect": (
                "FAIL_CLOSED_IN_LAUNCHER_SOURCE_REGISTRY_SHAPE_CHECK_BEFORE_"
                "CANDIDATE_OR_STAGE_MATERIALIZATION"),
            "operator_reported_first_cold_attempt": {
                "bootstrap": "scripts/c79g_v14_external_held_fd_bootstrap.py",
                "action": "build",
                "candidate_label": "a",
                "PYTHONHASHSEED": "101",
                "process_return_code": 2,
                "stderr": (
                    "REJECT: current v14 registry explicit62 plus exact "
                    "execution-proof7"),
                "operator_report_is_bound_as_attestation_not_as_standalone_authority": True,
            },
            "post_attempt_runtime_surface_census": census,
        },
        "credit": {
            "formal_global_closure_credit": 0,
            "D02_gate_credit": 0,
            "D02_task_credit": 0,
            "D02_unlock": False,
            "D02_started": False,
            "D02_formal_pending_task_count": 33638,
        },
        "permanent_v14_rejection_policy": {
            "v14_execution_allowed": False,
            "v14_exact10_or_rejection_overwrite_delete_or_reuse_allowed": False,
            "v14_runtime_namespace_reuse_allowed": False,
            "v14_may_be_patched_or_republished": False,
            "v14_may_contribute_formal_credit": False,
            "successor_version": 15,
        },
        "v15_successor_contract": {
            "v15_current_exact8_first_member_must_be_this_receipt": True,
            "v15_must_pin_this_receipt_file_and_object_sha256": True,
            "v15_must_directly_hold_and_terminally_replay_v14_exact10_plus_"
            "official_rejection_plus_this_receipt": True,
            "v15_inherited_published_incident_authority_exact12_count": 12,
            "v15_launcher_registry_helper_must_require_explicit67_plus_"
            "execution_proof7_plus_object_closure1_equals75": True,
            "v15_independent_reviewer_must_execute_the_actual_launcher_helper_"
            "against_actual_producer_bytes": True,
            "v15_independent_reviewer_must_reject_in_memory_explicit62_tamper": True,
            "this_receipt_does_not_pin_any_v15_successor_byte": True,
            "one_way_binding_avoids_hash_cycle": True,
        },
        "publication_mechanics": {
            "official_runtime_writer_lock_held_for_entire_validation_and_commit": True,
            "v14_exact10_and_rejection_fds_held_through_terminal_exact12_replay": True,
            "receipt_commit_operation": (
                "O_TMPFILE_COMPLETE_FCHMOD0444_FSYNC_VERIFY__PROC_SELF_FD_"
                "LINKAT_AT_SYMLINK_FOLLOW_ATOMIC_NO_REPLACE"),
            "receipt_file_mode": "0444",
            "receipt_nlink": 1,
            "receipt_created_strictly_after_official_rejection": True,
            "file_and_parent_fsync_required": True,
            "overwrite_delete_or_reuse_allowed": False,
        },
    })


AT_FDCWD = -100
AT_SYMLINK_FOLLOW = 0x400


def link_anonymous_no_replace(fd: int, output_fd: int, name: str) -> None:
    assert name and "/" not in name
    old = f"/proc/self/fd/{fd}"
    library = ctypes.CDLL(None, use_errno=True)
    result = library.linkat(
        ctypes.c_int(AT_FDCWD), ctypes.c_char_p(os.fsencode(old)),
        ctypes.c_int(output_fd), ctypes.c_char_p(os.fsencode(name)),
        ctypes.c_int(AT_SYMLINK_FOLLOW))
    assert result == 0, ("linkat", ctypes.get_errno())


def publish_receipt(root: Path, raw: bytes, rejection_state: os.stat_result) -> int:
    output_fd = os.open(root / "deliverables",
                        os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    fd = -1
    try:
        assert not (root / RECEIPT_REL).exists()
        fd = os.open(".", os.O_RDWR | os.O_TMPFILE | os.O_CLOEXEC, 0o600,
                     dir_fd=output_fd)
        write_all(fd, raw)
        os.fchmod(fd, 0o444)
        os.fsync(fd)
        anonymous = os.fstat(fd)
        assert stat.S_ISREG(anonymous.st_mode)
        assert stat.S_IMODE(anonymous.st_mode) == 0o444
        assert anonymous.st_nlink == 0 and anonymous.st_size == len(raw)
        assert max(rejection_state.st_mtime_ns, rejection_state.st_ctime_ns) < min(
            anonymous.st_mtime_ns, anonymous.st_ctime_ns)
        assert read_all(fd) == raw
        link_anonymous_no_replace(fd, output_fd, Path(RECEIPT_REL).name)
        os.fsync(output_fd)
        linked = os.fstat(fd)
        assert linked.st_nlink == 1 and stat.S_IMODE(linked.st_mode) == 0o444
        return fd
    except BaseException:
        if fd >= 0:
            os.close(fd)
        raise
    finally:
        os.close(output_fd)


def main() -> int:
    if not __debug__:
        raise RuntimeError("python -O is forbidden")
    assert FINAL_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_GUARD_PINS_INSTALLED is True
    assert len(sys.argv) == 3
    root = Path(sys.argv[1]).resolve(strict=True)
    command = sys.argv[2]
    assert root == ROOT_EXPECTED
    assert command in {"PREFLIGHT", "FREEZE_REJECT"}
    assert len(V14_EXACT10) == 10
    runtime_fd = os.open(root / ".cm2-runtime",
                         os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    held: list[Held] = []
    receipt_fd = -1
    try:
        fcntl.flock(runtime_fd, fcntl.LOCK_EX)
        before = stable_output_snapshot(root) if command == "PREFLIGHT" else None
        receipt_exists = (root / RECEIPT_REL).exists()
        if command == "PREFLIGHT":
            assert not receipt_exists
        for pin in V14_EXACT10:
            held.append(Held(root, pin))
        rejection = Held(root, V14_OFFICIAL_REJECTION)
        held.append(rejection)
        assert len({(item.initial.st_dev, item.initial.st_ino)
                    for item in held}) == 11
        assert len({item.initial.st_dev for item in held}) == 1
        manifest_expected = b"".join(
            f"{pin['file_sha256']}  {pin['path']}\n".encode("ascii")
            for pin in V14_EXACT10[:8])
        assert held[8].raw == manifest_expected
        first8_max = max(max(item.initial.st_mtime_ns, item.initial.st_ctime_ns)
                         for item in held[:8])
        manifest_min = min(held[8].initial.st_mtime_ns,
                           held[8].initial.st_ctime_ns)
        manifest_max = max(held[8].initial.st_mtime_ns,
                           held[8].initial.st_ctime_ns)
        outer_min = min(held[9].initial.st_mtime_ns,
                        held[9].initial.st_ctime_ns)
        outer_max = max(held[9].initial.st_mtime_ns,
                        held[9].initial.st_ctime_ns)
        rejection_min = min(rejection.initial.st_mtime_ns,
                            rejection.initial.st_ctime_ns)
        assert first8_max < manifest_min and manifest_max < outer_min
        assert outer_max < rejection_min
        rejection_value = verify_object(rejection.raw,
                                        V14_OFFICIAL_REJECTION["object_sha256"])
        validate_rejection(rejection_value)
        census = validate_runtime_census(root)
        registry = producer_registry_shape(held[3].raw)
        launcher = launcher_stale_helper_shape(held[7].raw)
        assert registry["actual_total_registry_shape"] == 75
        assert launcher["launcher_stale_total_registry_shape"] == 70
        receipt_value = build_receipt(
            held[:10], rejection, registry, launcher, census)
        raw = canonical(receipt_value) + b"\n"
        object_sha = receipt_value["object_sha256"]
        assert sha256(canonical({key: value for key, value in receipt_value.items()
                                 if key != "object_sha256"})) == object_sha
        if command == "PREFLIGHT":
            for item in held:
                item.replay()
            assert not (root / RECEIPT_REL).exists()
            assert stable_output_snapshot(root) == before
            result = {
                "status": (
                    "PREFLIGHT_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_EXACT11_"
                    "READ_ONLY_PASS_UNDER_OFFICIAL_LOCK"),
                "v14_exact10_terminal_replayed": True,
                "official_v14_rejection_terminal_replayed": True,
                "actual_producer_registry_shape": 75,
                "stale_launcher_registry_shape": 70,
                "shape_delta": 5,
                "candidate_and_stage_namespace_count": 0,
                "prospective_receipt_object_sha256": object_sha,
                "no_write_chmod_import_compile_execution_or_py_compile_performed": True,
            }
        else:
            # The frozen exact10 plus official rejection must be replayed
            # before the receipt directory entry can exist.  Publication is
            # followed by a second, terminal exact12 replay below.
            for item in held:
                item.replay()
            if receipt_exists:
                receipt_pin = {
                    "path": RECEIPT_REL,
                    "file_sha256": sha256(raw),
                    "object_sha256": object_sha,
                }
                existing = Held(root, receipt_pin)
                held.append(existing)
                receipt_fd = existing.fd
            else:
                receipt_fd = publish_receipt(root, raw, rejection.initial)
                receipt_state = os.fstat(receipt_fd)
                assert receipt_state.st_nlink == 1
                assert read_all(receipt_fd) == raw
                verify_object(raw, object_sha)
            for item in held:
                item.replay()
            receipt_path_state = os.lstat(root / RECEIPT_REL)
            receipt_fd_state = os.fstat(receipt_fd)
            assert (receipt_path_state.st_dev, receipt_path_state.st_ino) == (
                receipt_fd_state.st_dev, receipt_fd_state.st_ino)
            assert stat.S_IMODE(receipt_fd_state.st_mode) == 0o444
            assert receipt_fd_state.st_nlink == 1
            assert read_all(receipt_fd) == raw
            assert max(rejection.initial.st_mtime_ns,
                       rejection.initial.st_ctime_ns) < min(
                receipt_fd_state.st_mtime_ns, receipt_fd_state.st_ctime_ns)
            os.fsync(receipt_fd)
            output_fd = os.open(root / "deliverables",
                                os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
            try:
                os.fsync(output_fd)
            finally:
                os.close(output_fd)
            os.fsync(runtime_fd)
            result = {
                "status": (
                    "FROZEN_APPEND_ONLY_V14_RUNTIME_REGISTRY_SHAPE_DRIFT_"
                    "REJECTION__ZERO_CREDIT__V15_SUCCESSOR_ONLY"),
                "receipt_path": RECEIPT_REL,
                "receipt_file_sha256": sha256(raw),
                "receipt_object_sha256": object_sha,
                "terminal_exact12_same_fd_replay": True,
                "formal_global_closure_credit": 0,
                "D02_unlock": False,
                "D02_formal_pending_task_count": 33638,
            }
        print(canonical(result).decode("ascii"))
        return 0
    finally:
        if receipt_fd >= 0 and all(item.fd != receipt_fd for item in held):
            os.close(receipt_fd)
        for item in reversed(held):
            item.close()
        try:
            fcntl.flock(runtime_fd, fcntl.LOCK_UN)
        finally:
            os.close(runtime_fd)


if __name__ == "__main__":
    raise SystemExit(main())
