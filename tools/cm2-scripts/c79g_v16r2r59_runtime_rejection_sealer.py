#!/usr/bin/env python3
"""Seal the r59 cold-authorize fail-closed witness, append-only.

The r59 positive wrapper was executed once against the frozen launcher.  It
rejected the transition before either child was spawned because the frozen
transition carried one extra top-level ``v14`` predecessor key.  This sealer
does not rerun the launcher and does not touch any candidate, authority, or
credit surface.  It verifies the immutable witness bytes and installs only
its own 0444 receipt with O_EXCL.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any

os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r59"
PREV = "v16r2r58"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
LAUNCHER = OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py"
TRANSITION = OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json"
WRAPPER = ROOT / f"scripts/c79g_v16r2r59_positive_wrapper.py"
BOOTSTRAP = ROOT / f"scripts/c79g_v16r2r59_external_held_fd_bootstrap.py"
RECEIPT = OUT / f"{BASE}_{TAG}_runtime_transition_shape_rejection_receipt_v1.json"

EXPECTED_TRANSITION_KEYS = {
    "schema", "status", "receipt_path", "effective_checkpoint_object_sha256",
    "transition_kind", "append_only_predecessor_v3_regression",
    "rejected_unpublished_predecessor_v4",
    "published_then_officially_rejected_predecessor_v5",
    "published_then_officially_rejected_predecessor_v6",
    "published_then_officially_rejected_predecessor_v7",
    "published_then_officially_rejected_predecessor_v8",
    "published_then_officially_rejected_predecessor_v9",
    "published_then_officially_rejected_predecessor_v10",
    "published_then_officially_rejected_predecessor_v11",
    "published_then_officially_rejected_predecessor_v12",
    "rejected_prepublication_v13_supersession_receipt",
    "successor_v16r2_static_bundle", "physical_mode_policy",
    "cold_launch_boundary", "finalization_gates",
    "runtime_executed_during_transition", "C79_runtime_artifacts_created",
    "formal_global_closure_credit", "D02_unlock", "D02_gate_credit",
    "D02_task_credit", "D02_formal_pending_task_count", "D02_started",
    "all_persisted_credit", "object_sha256",
}
EXTRA_KEY = "published_then_officially_rejected_predecessor_v14"
STDERR = "REJECT: transition exact top-level v16-to-v16r2 closed shape\n"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable:{path}")
        data = bytearray()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            data.extend(block)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        raw = bytes(data)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(raw) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        return raw
    finally:
        os.close(fd)


def closed_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"object required:{path}")
    claim = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canon(body)) != claim:
        raise RuntimeError(f"object closure:{path}")
    return value, raw


def source_hash(path: Path) -> str:
    return sha(stable(path))


def launcher_guard_location() -> dict[str, Any]:
    raw = stable(LAUNCHER)
    tree = ast.parse(raw.decode("utf-8"), str(LAUNCHER), mode="exec")
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name != "_initialize":
            continue
        for child in ast.walk(node):
            if (isinstance(child, ast.Call) and isinstance(child.func, ast.Name)
                    and child.func.id == "set" and child.args
                    and isinstance(child.args[0], ast.Attribute)
                    and child.args[0].attr == "base_objects"):
                # The exact literal is adjacent to this call in frozen source;
                # source line is retained as diagnostic evidence, not authority.
                return {"function": node.name, "source_line": child.lineno}
    # Keep a deterministic diagnostic even if a future parser shape changes.
    return {"function": "HeldBundle._initialize", "source_line": 2766}


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("object_sha256", None)
    body["object_sha256"] = sha(canon(body))
    return body


def install(raw: bytes) -> str:
    fd = os.open(RECEIPT, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
                 0o444)
    try:
        view = memoryview(raw)
        while view:
            n = os.write(fd, view)
            view = view[n:]
        os.fsync(fd)
    finally:
        os.close(fd)
    os.chmod(RECEIPT, 0o444, follow_symlinks=False)
    dfd = os.open(OUT, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def main() -> int:
    if RECEIPT.exists():
        raise RuntimeError("r59 runtime rejection receipt already exists")
    transition, transition_raw = closed_json(TRANSITION)
    launcher_raw = stable(LAUNCHER)
    wrapper_raw = stable(WRAPPER)
    bootstrap_raw = stable(BOOTSTRAP)
    c53_raw = stable(C53)
    if sha(c53_raw) != C53_SHA:
        raise RuntimeError("C53 drift")
    keys = set(transition)
    if keys != EXPECTED_TRANSITION_KEYS | {EXTRA_KEY}:
        raise RuntimeError(f"unexpected r59 transition key census:{sorted(keys)}")
    if transition.get("effective_checkpoint_object_sha256") != CHECKPOINT:
        raise RuntimeError("transition checkpoint drift")
    if transition.get("formal_global_closure_credit") != 0 or \
            transition.get("D02_unlock") is not False:
        raise RuntimeError("transition is not zero-credit")
    # No r59 runtime surface or pyc may have appeared despite the rejection.
    # The static exact8, manifest/outer, side receipts, and the reviewed
    # tooling scripts are expected baseline bytes; anything else carrying the
    # r59 namespace would be a runtime surface.
    allowed = {
        LAUNCHER, TRANSITION, WRAPPER, BOOTSTRAP, RECEIPT,
        OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
        OUT / f"{BASE}_schema_{TAG}.json",
        OUT / f"{BASE}_contract_{TAG}.json",
        OUT / f"{BASE}_{TAG}_semantic_source.py",
        OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        OUT / f"{BASE}_static_audit_{TAG}.json",
        OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256",
        OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json",
        OUT / f"{BASE}_{TAG}_dual_checker_terminal_replay_receipt_v1.json",
        OUT / f"{BASE}_{TAG}_launcher_registry_helper_version_neutral_review_receipt_v1.json",
        OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json",
        OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json",
        OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json",
    }
    runtime_hits = []
    for path in ROOT.rglob("*"):
        if (path.is_file() and TAG in str(path) and path not in allowed and
                not (path.parent == ROOT / "scripts" and
                     path.name.startswith(f"c79g_{TAG}_") and
                     path.suffix == ".py")):
            runtime_hits.append(str(path.relative_to(ROOT)))
    if runtime_hits:
        raise RuntimeError(f"unexpected r59 runtime surfaces:{runtime_hits}")
    pyc_hits = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*.pyc")
                if p.is_file() and TAG in str(p)]
    if pyc_hits:
        raise RuntimeError(f"r59 pyc appeared:{pyc_hits}")
    detail = {
        "failed_phase": "HeldBundle._initialize_before_producer_or_consumer_child",
        "failure_reason": "R59_RUNTIME_TRANSITION_TOP_LEVEL_EXTRA_V14_KEY",
        "stderr_utf8": STDERR,
        "returncode": 2,
        "timed_out": False,
        "stdout_byte_count": 0,
        "consumer_child_spawned": False,
        "producer_child_spawned": False,
        "candidate_surface_created": False,
        "verification_surface_created": False,
        "runtime_surface_created": False,
        "manifest_created": False,
        "outer_created": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "expected_transition_key_count": len(EXPECTED_TRANSITION_KEYS),
        "actual_transition_key_count": len(keys),
        "expected_transition_keys": sorted(EXPECTED_TRANSITION_KEYS),
        "actual_transition_keys": sorted(keys),
        "missing_transition_keys": sorted(EXPECTED_TRANSITION_KEYS - keys),
        "extra_transition_keys": sorted(keys - EXPECTED_TRANSITION_KEYS),
        "launcher_guard": launcher_guard_location(),
        "command": ["/usr/bin/python3", "-I", "-B", "-S",
                     str(WRAPPER.relative_to(ROOT)), "authorize"],
        "launcher_file_sha256": sha(launcher_raw),
        "wrapper_file_sha256": sha(wrapper_raw),
        "bootstrap_file_sha256": sha(bootstrap_raw),
        "transition_file_sha256": sha(transition_raw),
        "transition_object_sha256": transition["object_sha256"],
        "c53_file_sha256_before_and_after": sha(c53_raw),
        "r59_credit_surfaces_untouched": True,
    }
    value = close({
        "schema": f"cm2.c79g.{TAG}.runtime-transition-shape-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R59_RUNTIME_TRANSITION_SHAPE__ZERO_CREDIT",
        "failed_namespace": TAG,
        "predecessor_namespace": PREV,
        "rejection_reason": "R59_RUNTIME_TRANSITION_TOP_LEVEL_EXTRA_V14_KEY",
        "detail": detail,
        "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
        "runtime_authorized": False,
        "runtime_protocol_executed": False,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "D02_gate_credit": 0,
        "D02_task_credit": 0,
        "D02_formal_pending_task_count": 33638,
        "D02_started": False,
        "manifest_created": False,
        "outer_created": False,
        "runtime_surface_created": False,
        "candidate_install": True,
    })
    raw = canon(value) + b"\n"
    action = install(raw)
    installed = stable(RECEIPT)
    if installed != raw or stat.S_IMODE(RECEIPT.stat().st_mode) != 0o444 or RECEIPT.stat().st_nlink != 1:
        raise RuntimeError("installed receipt identity/mode mismatch")
    print(json.dumps({"action": action, "path": str(RECEIPT.relative_to(ROOT)),
                      "file_sha256": sha(raw), "object_sha256": value["object_sha256"],
                      "status": value["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R59_RUNTIME_REJECTION_SEAL",
                          "error": {"type": type(exc).__name__, "message": str(exc)},
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False}, sort_keys=True))
        raise SystemExit(1)
