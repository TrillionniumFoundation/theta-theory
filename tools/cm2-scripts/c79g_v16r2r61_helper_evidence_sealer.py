#!/usr/bin/env python3
"""Seal r61's version-neutral launcher-helper evidence.

The default command is a read-only dual-seed preflight.  ``--seal`` performs
one append-only O_EXCL install of the 0444 receipt after the same checks pass.
No candidate, manifest, outer, runtime, authority, or credit surface is
created or modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r61"
UPSTREAM = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
ANCHOR_FILE_SHA = "a6e7ebe51eed1a877f0440d2bf90827e17ca955912d449a4eaca6fc17f383838"
ANCHOR_OBJECT = "fc63955e5c40352413245ca0e8a2a4a098a4b3f596f534838a9442190dd98be2"
LAUNCHER = OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py"
RECEIPT = OUT / f"{BASE}_{TAG}_launcher_registry_helper_version_neutral_review_receipt_v1.json"
REVIEW_A = ROOT / "scripts/c79g_v16r2r61_role_aware_reviewer.py"
REVIEW_B = ROOT / "scripts/c79g_v16r2r61_helper_reviewer_b.py"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
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
            b = os.read(fd, 1 << 20)
            if not b: break
            chunks.append(b)
        raw = b"".join(chunks); after = os.fstat(fd); named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(raw) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        return raw
    finally:
        os.close(fd)


def closed(value: dict[str, Any]) -> bool:
    claim = value.get("object_sha256")
    body = dict(value); body.pop("object_sha256", None)
    return isinstance(claim, str) and len(claim) == 64 and sha(canon(body)) == claim


def run_reviewer(path: Path, seed: str) -> tuple[dict[str, Any], bytes]:
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "PYTHONHASHSEED": seed})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", "-S", str(path)],
                          cwd=str(ROOT), env=env, capture_output=True,
                          check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"reviewer {path.name} rc={proc.returncode}:" +
                           proc.stderr.decode(errors="replace")[-500:])
    raw = proc.stdout
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict) or not closed(value):
        raise RuntimeError(f"reviewer {path.name} report not closed")
    return value, raw


def preflight() -> tuple[dict[str, Any], bytes]:
    if not all(p.is_file() for p in (ANCHOR, LAUNCHER, REVIEW_A, REVIEW_B, C53)):
        raise RuntimeError("required input missing")
    if sha(stable(ANCHOR)) != ANCHOR_FILE_SHA or json.loads(stable(ANCHOR).decode())["object_sha256"] != ANCHOR_OBJECT:
        raise RuntimeError("r61 anchor pin mismatch")
    if sha(stable(C53)) != C53_SHA:
        raise RuntimeError("C53 drift")
    if MANIFEST.exists() or OUTER.exists():
        raise RuntimeError("cold positive surfaces already exist")
    before = {"launcher": sha(stable(LAUNCHER)),
              "anchor": sha(stable(ANCHOR)),
              "c53": sha(stable(C53))}
    reports: dict[str, dict[str, Any]] = {}
    raws: dict[str, dict[str, bytes]] = {"A": {}, "B": {}}
    for label, path in (("A", REVIEW_A), ("B", REVIEW_B)):
        for seed in ("1", "99991"):
            reports[f"{label}:{seed}"], raws[label][seed] = run_reviewer(path, seed)
        if raws[label]["1"] != raws[label]["99991"]:
            raise RuntimeError(f"{label} dual-seed report drift")
    a = reports["A:1"]; b = reports["B:1"]
    if not a.get("status", "").startswith("PASS_DUAL_STATIC_CANDIDATE_34_OF_34") or a.get("failed_check_count") != 0:
        raise RuntimeError("reviewer A failed")
    if not b.get("status", "").startswith("PASS_VERSION_NEUTRAL_HELPER_REVIEW_B") or b.get("failed_checks"):
        raise RuntimeError("reviewer B failed")
    if a.get("version_neutral_helper_ast_sha256") != "5f82214b873d270ea5d01ac43132c0bf1463b12c3289362a001a7c870952bada" or \
       b.get("version_neutral_normalized_helper_ast_sha256") != "5f82214b873d270ea5d01ac43132c0bf1463b12c3289362a001a7c870952bada":
        raise RuntimeError("neutral helper digest mismatch")
    if a.get("helper_raw_ast_sha256") != "2acf6424fe5ca8c58bc19d28ff9fcf3b9326b7c62e59741adda17e5f8e84392d" or \
       b.get("historical_template_raw_ast_sha256") != "f27a5e8df3308e5b022519929e8f0f64257dcbc35b355fa1537b0169d5604a8c":
        raise RuntimeError("raw helper digest witness mismatch")
    after = {"launcher": sha(stable(LAUNCHER)),
             "anchor": sha(stable(ANCHOR)), "c53": sha(stable(C53))}
    if before != after:
        raise RuntimeError("input bytes changed during review")
    if any(TAG in p.name and p.name !=
           "c79g_v16r2r60_candidate_builder.cpython-312.pyc"
           for p in ROOT.rglob("*.pyc")):
        raise RuntimeError("r61 unexpected pyc appeared")
    body: dict[str, Any] = {
        "schema": f"cm2.c79g.{TAG}.launcher-registry-helper-version-neutral-review.v1",
        "status": "PASS_R61_DUAL_INDEPENDENT_VERSION_NEUTRAL_HELPER_REVIEW__ZERO_CREDIT",
        "candidate_namespace": TAG,
        "candidate_launcher_path": str(LAUNCHER.relative_to(ROOT)),
        "candidate_launcher_file_sha256": before["launcher"],
        "helper_function": "producer_source_registry_shape_from_ast",
        "helper_raw_ast_sha256": a["helper_raw_ast_sha256"],
        "historical_template_raw_ast_sha256": b["historical_template_raw_ast_sha256"],
        "version_neutral_normalization_algorithm": "AST_DUMP_NO_ATTRIBUTES_V1__AND_LEXICAL_FUNCTION_SEGMENT_REGEX_THEN_AST_DUMP_V1",
        "normalization_rules": [
            {"scope": "helper FunctionDef only", "match": "producer_(v15|v16r2)", "replace": "producer_CURRENT"},
            {"scope": "helper FunctionDef only", "match": "current v(15|16r2)", "replace": "current CURRENT"},
        ],
        "version_neutral_normalized_helper_ast_sha256": "5f82214b873d270ea5d01ac43132c0bf1463b12c3289362a001a7c870952bada",
        "current_label_census": {"producer_v16r2": 1, "current_v16r2": 5, "producer_v15": 0, "current_v15": 0},
        "guard_vector": {"explicit_key_guard": [67], "proof7": 1, "expansion1": 1,
                          "shape75": 1, "stale62": 0, "nested_scopes": 0,
                          "raw_param": True, "formula": True, "direct_return": True,
                          "live_call_owner": "validate_final_static_audit", "live_call_count": 1,
                          "live_held_producer_raw": True, "live_expected_shapes_75_gate": True,
                          "producer_shape": 75},
        "mutation_results": {"stale62_rejected": True, "dead_callsite_rejected": True},
        "reviewers": {
            "A": {"source_path": str(REVIEW_A.relative_to(ROOT)), "source_sha256": sha(stable(REVIEW_A)),
                  "report_object_sha256": a["object_sha256"], "report_sha256": sha(raws["A"]["1"])},
            "B": {"source_path": str(REVIEW_B.relative_to(ROOT)), "source_sha256": sha(stable(REVIEW_B)),
                  "report_object_sha256": b["object_sha256"], "report_sha256": sha(raws["B"]["1"])},
        },
        "dual_seed_replays": {"A": True, "B": True, "seeds": ["1", "99991"]},
        "active_anchor_file_sha256": ANCHOR_FILE_SHA,
        "active_anchor_object_sha256": ANCHOR_OBJECT,
        "upstream_checkpoint_object_sha256": UPSTREAM,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False, "manifest_created": False,
        "outer_created": False, "runtime_protocol_executed": False,
    }
    body["object_sha256"] = sha(canon(body))
    return body, canon(body) + b"\n"


def install(raw: bytes) -> str:
    try:
        fd = os.open(RECEIPT, os.O_RDWR | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if (stable(RECEIPT) != raw or RECEIPT.stat().st_nlink != 1 or
                stat.S_IMODE(RECEIPT.stat().st_mode) != 0o444):
            raise RuntimeError("existing receipt differs")
        return "replayed"
    try:
        view = memoryview(raw); offset = 0
        while offset < len(view):
            n = os.write(fd, view[offset:])
            if n <= 0: raise RuntimeError("short receipt write")
            offset += n
        os.fsync(fd); os.fchmod(fd, 0o444)
        os.lseek(fd, 0, os.SEEK_SET)
        reread = b""
        while True:
            b = os.read(fd, 1 << 20)
            if not b: break
            reread += b
        if reread != raw: raise RuntimeError("same-fd terminal reread mismatch")
    finally:
        os.close(fd)
    dfd = os.open(RECEIPT.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try: os.fsync(dfd)
    finally: os.close(dfd)
    return "installed"


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--seal", action="store_true")
    args = parser.parse_args()
    try:
        body, raw = preflight()
        if args.seal:
            body["install_result"] = install(raw)
            # The receipt bytes are already closed; install_result is only a
            # local stdout diagnostic and is deliberately not folded into it.
        print(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{TAG}.helper-evidence-sealer.failure.v1",
                          "status": "FAIL_CLOSED_R61_HELPER_EVIDENCE", "error": f"{type(exc).__name__}:{exc}",
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "runtime_authorized": False}, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
