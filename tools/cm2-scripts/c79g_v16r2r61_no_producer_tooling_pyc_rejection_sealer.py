#!/usr/bin/env python3
"""Seal the r61 no-producer tooling-pyc hard rejection and open r62.

This is a read-only audit until ``--seal``.  It never removes the pyc witness
or changes an r61 byte; the only writes are three new 0444 JSON objects made
with O_EXCL, in rejection -> supersession -> active-anchor order.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
PREV = "v16r2r61"
TAG = "v16r2r62"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_OBJECT = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"
PYCS = ROOT / "scripts/__pycache__/c79g_v16r2r61_no_producer_evidence_sealer.cpython-312.pyc"
PYC_SHA = "a25be0dadafa36751eff506d169f670776fb91f42ab4118596e5511a88a135a7"
PYC_SIZE = 21748
SEALER = ROOT / "scripts/c79g_v16r2r61_no_producer_evidence_sealer.py"
SEALER_SHA = None
ANCHOR = OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json"
ANCHOR_SHA = "a6e7ebe51eed1a877f0440d2bf90827e17ca955912d449a4eaca6fc17f383838"
ANCHOR_OBJECT = "fc63955e5c40352413245ca0e8a2a4a098a4b3f596f534838a9442190dd98be2"
HELPER_RECEIPT = OUT / f"{BASE}_{PREV}_launcher_registry_helper_version_neutral_review_receipt_v1.json"
HELPER_SHA = "4442057b6e3b67839dd0686e0fa1b108ba08350b68b02a206da738cdd88e3498"
HELPER_OBJECT = "8e73a17685940781d974e9df582e0016b6b7b5aa31418cce8b572285b3127350"
REJECTION = OUT / f"{BASE}_{PREV}_no_producer_tooling_pyc_rejection_receipt_v1.json"
SUPERSESSION = OUT / f"{BASE}_{PREV}_to_{TAG}_no_producer_tooling_pyc_rejection_supersession_receipt_v1.json"
NEXT_ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
TARGETS = (REJECTION, SUPERSESSION, NEXT_ANCHOR)

EXACT8 = (
    OUT / f"{BASE}_{PREV}_active_predecessor_supersession_receipt_v1.json",
    OUT / f"{BASE}_schema_{PREV}.json",
    OUT / f"{BASE}_contract_{PREV}.json",
    OUT / f"{BASE}_{PREV}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{PREV}_semantic_source.py",
    OUT / f"{BASE}_v16r2r60_to_{PREV}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{PREV}.json",
    OUT / f"{BASE}_cold_launch_{PREV}_semantic_source.py",
)


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path, expected: str | None = None,
           expected_size: int | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable:{path}")
        chunks = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        raw = b"".join(chunks); after = os.fstat(fd); named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(raw) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        if expected is not None and sha(raw) != expected:
            raise RuntimeError(f"hash drift:{path}")
        if expected_size is not None and len(raw) != expected_size:
            raise RuntimeError(f"size drift:{path}")
        return raw
    finally:
        os.close(fd)


def closed(path: Path, expected_file: str | None = None,
           expected_object: str | None = None) -> tuple[dict[str, Any], bytes]:
    raw = stable(path, expected_file)
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"object required:{path}")
    body = dict(value); claim = body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canon(body)) != claim:
        raise RuntimeError(f"object closure:{path}")
    if expected_object is not None and claim != expected_object:
        raise RuntimeError(f"object pin:{path}")
    return value, raw


def close(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value); body.pop("object_sha256", None)
    body["object_sha256"] = sha(canon(body))
    return body


def preflight() -> tuple[dict[str, Any], bytes, bytes, bytes]:
    if any(p.exists() for p in TARGETS):
        raise RuntimeError("r62 rejection/anchor target already exists")
    anchor, anchor_raw = closed(ANCHOR, ANCHOR_SHA, ANCHOR_OBJECT)
    if (anchor.get("predecessor_namespace") != "v16r2r60" or
            anchor.get("successor_namespace") != f"{PREV}_semantic_source" or
            anchor.get("formal_global_closure_credit") != 0 or
            anchor.get("D02_unlock") is not False or
            anchor.get("runtime_authorized") is not False):
        raise RuntimeError("r61 anchor semantics")
    helper, helper_raw = closed(HELPER_RECEIPT, HELPER_SHA, HELPER_OBJECT)
    if helper.get("status") != "PASS_R61_DUAL_INDEPENDENT_VERSION_NEUTRAL_HELPER_REVIEW__ZERO_CREDIT":
        raise RuntimeError("r61 helper status")
    for path in EXACT8[1:]:
        stable(path)
    c53_raw = stable(C53, C53_SHA)
    c53 = json.loads(c53_raw.decode())
    if c53.get("authority_seal_object_sha256") != C53_OBJECT:
        raise RuntimeError("C53 object drift")
    pyc_raw = stable(PYCS, PYC_SHA, PYC_SIZE)
    if stat.S_IMODE(PYCS.stat().st_mode) != 0o664 or PYCS.stat().st_nlink != 1:
        raise RuntimeError("tooling pyc identity")
    sealer_raw = stable(SEALER, SEALER_SHA)
    failure = {
        "phase": "r61_no_producer_preflight_before_child_spawn",
        "error": "FAIL_CLOSED_R61_NO_PRODUCER_EVIDENCE: r61 unexpected pyc present",
        "child_processes_spawned": False,
        "receipt_written": False, "manifest_created": False,
        "outer_created": False, "runtime_surface_created": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "tooling_pyc": {"path": str(PYCS.relative_to(ROOT)),
                        "file_sha256": sha(pyc_raw), "size": len(pyc_raw),
                        "mode": stat.S_IMODE(PYCS.stat().st_mode),
                        "nlink": PYCS.stat().st_nlink},
        "sealer_source": {"path": str(SEALER.relative_to(ROOT)),
                          "file_sha256": sha(sealer_raw)},
    }
    rejected = close({
        "schema": f"cm2.c79g.{PREV}.no-producer-tooling-pyc-rejection.v1",
        "status": "PERMANENT_FAIL_CLOSED_R61_NO_PRODUCER_TOOLING_PYC__ZERO_CREDIT",
        "failed_namespace": PREV, "predecessor_namespace": "v16r2r60",
        "rejection_reason": "R61_NO_PRODUCER_TAGGED_TOOLING_PYC_BEFORE_PREFLIGHT",
        "failure_vector": failure,
        "r61_anchor_file_sha256": ANCHOR_SHA,
        "r61_anchor_object_sha256": ANCHOR_OBJECT,
        "r61_helper_receipt_file_sha256": HELPER_SHA,
        "r61_helper_receipt_object_sha256": HELPER_OBJECT,
        "tooling_pyc_rejection_path": str(PYCS.relative_to(ROOT)),
        "tooling_pyc_rejection_file_sha256": sha(pyc_raw),
        "tooling_pyc_rejection_size": len(pyc_raw),
        "candidate_install": True, "runtime_protocol_executed": False,
        "manifest_created": False, "outer_created": False,
        "runtime_authorized": False, "formal_global_closure_credit": 0,
        "D02_unlock": False, "append_only": True,
        "overwrite_delete_or_reuse_allowed": False,
    })
    rejection_raw = canon(rejected) + b"\n"
    superseded = close({
        "schema": f"cm2.c79g.{PREV}-to-{TAG}.no-producer-tooling-pyc-rejection-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_REJECTED_PREDECESSOR_SUPERSEDED__ZERO_CREDIT",
        "predecessor_namespace": PREV, "successor_namespace": TAG,
        "predecessor_active_anchor_path": str(ANCHOR.relative_to(ROOT)),
        "predecessor_active_anchor_file_sha256": ANCHOR_SHA,
        "predecessor_active_anchor_object_sha256": ANCHOR_OBJECT,
        "predecessor_rejection_path": str(REJECTION.relative_to(ROOT)),
        "predecessor_rejection_file_sha256": sha(rejection_raw),
        "predecessor_rejection_object_sha256": rejected["object_sha256"],
        "tooling_pyc_rejection_path": str(PYCS.relative_to(ROOT)),
        "tooling_pyc_rejection_file_sha256": sha(pyc_raw),
        "tooling_pyc_rejection_size": len(pyc_raw),
        "r61_helper_receipt_file_sha256": HELPER_SHA,
        "r61_helper_receipt_object_sha256": HELPER_OBJECT,
        "C53_file_sha256": sha(c53_raw), "C53_object_sha256": C53_OBJECT,
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
    })
    superseded_raw = canon(superseded) + b"\n"
    next_anchor = close({
        "schema": f"cm2.c79g.{TAG}.active-predecessor-supersession.v1",
        "status": "FROZEN_APPEND_ONLY_ACTIVE_PREDECESSOR_ANCHOR__ZERO_CREDIT",
        "predecessor_namespace": PREV,
        "predecessor_supersession_path": str(SUPERSESSION.relative_to(ROOT)),
        "predecessor_supersession_file_sha256": sha(superseded_raw),
        "predecessor_supersession_object_sha256": superseded["object_sha256"],
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "successor_namespace": f"{TAG}_semantic_source",
        "append_only": True, "runtime_authorized": False,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "manifest_created": False, "outer_created": False,
    })
    next_raw = canon(next_anchor) + b"\n"
    report = {"schema": f"cm2.c79g.{PREV}.no-producer-tooling-pyc-rejection-sealer.v1",
              "status": "PREFLIGHT_PASS_R61_NO_PRODUCER_TOOLING_PYC_REJECTION__ZERO_CREDIT",
              "rejection_file_sha256": sha(rejection_raw),
              "rejection_object_sha256": rejected["object_sha256"],
              "supersession_file_sha256": sha(superseded_raw),
              "supersession_object_sha256": superseded["object_sha256"],
              "next_anchor_file_sha256": sha(next_raw),
              "next_anchor_object_sha256": next_anchor["object_sha256"],
              "tooling_pyc_file_sha256": sha(pyc_raw), "tooling_pyc_size": len(pyc_raw),
              "formal_global_closure_credit": 0, "D02_unlock": False,
              "runtime_authorized": False, "installation_performed": False}
    return report, rejection_raw, superseded_raw, next_raw


def install(path: Path, raw: bytes) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if stable(path) != raw or path.stat().st_nlink != 1 or stat.S_IMODE(path.stat().st_mode) != 0o444:
            raise RuntimeError(f"existing target differs:{path}")
        return "replayed"
    try:
        os.write(fd, raw); os.fsync(fd); os.fchmod(fd, 0o444)
    finally:
        os.close(fd)
    return "installed"


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--seal", action="store_true")
    args = ap.parse_args()
    try:
        report, rejection, supersession, anchor = preflight()
        if args.seal:
            report["actions"] = {
                "rejection": install(REJECTION, rejection),
                "supersession": install(SUPERSESSION, supersession),
                "anchor": install(NEXT_ANCHOR, anchor),
            }
            report["installation_performed"] = True
        print(json.dumps(report, sort_keys=True, separators=(",", ":")))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R61_TOOLING_PYC_REJECTION_SEALER",
                          "error": f"{type(exc).__name__}:{exc}",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
