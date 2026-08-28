#!/usr/bin/env python3
"""r41 no-producer dual-seed evidence (read-only by default).

The helper and reviewer are executed in isolated ``-I -B`` subprocesses.  The
default invocation only performs the checks and prints a report.  ``--seal``
or ``--install`` is required before the single append-only 0444 receipt may
be installed.  No candidate, runtime, manifest, outer, authority, credit, or
historical r34/r39 receipt is ever written or rebound by this program.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r41"
PREV = "v16r2r40"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
HELPER = ROOT / "scripts/c79g_v16r2_global_consumer_precompute.py"
REVIEWER = ROOT / "scripts/c79g_v16r2r20_independent_reviewer.py"
RECEIPT = OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"

EXACT8 = (
    OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
    OUT / f"{BASE}_schema_{TAG}.json",
    OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{TAG}.json",
    OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
)
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable input:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise RuntimeError(f"identity drift:{path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"short read:{path}")
        return raw
    finally:
        os.close(fd)


def install(path: Path, raw: bytes) -> str:
    """Install only the requested receipt, never a candidate or runtime file."""
    if path != RECEIPT:
        raise RuntimeError("receipt target mismatch")
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if (stable(path) != raw or path.stat().st_nlink != 1 or
                stat.S_IMODE(path.stat().st_mode) != 0o444):
            raise RuntimeError("append-only receipt mismatch")
        return "replayed"
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            written = os.write(fd, view[offset:])
            if written <= 0:
                raise RuntimeError("short receipt write")
            offset += written
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


def run_json(command: list[str], env: dict[str, str]) -> tuple[dict[str, Any], bytes]:
    proc = subprocess.run(command, cwd=str(ROOT), env=env, text=True,
                          capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"subprocess rc={proc.returncode}:{proc.stderr[-600:]}")
    raw = proc.stdout.encode()
    value = json.loads(proc.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("subprocess report object required")
    return value, raw


def assert_namespace_and_chain() -> dict[str, str]:
    if len(EXACT8) != 8 or any(p.parent != OUT for p in EXACT8):
        raise RuntimeError("exact8 direct-path shape")
    if any("v16r2r34" in str(p) or "v16r2r39" in str(p) for p in EXACT8):
        raise RuntimeError("historical r34/r39 path rebound")
    for path in EXACT8:
        raw = stable(path)
        mode = stat.S_IMODE(path.stat().st_mode)
        expected_mode = 0o664 if path.suffix == ".py" else 0o444
        if path.stat().st_nlink != 1 or mode != expected_mode:
            raise RuntimeError(f"exact8 identity/mode:{path}:{oct(mode)}")
        if not raw:
            raise RuntimeError(f"empty exact8 member:{path}")
    if MANIFEST.exists() or OUTER.exists():
        raise RuntimeError("positive cold surfaces already exist")
    if not HELPER.is_file() or not REVIEWER.is_file():
        raise RuntimeError("independent helper/reviewer missing")
    anchor = json.loads(stable(EXACT8[0]).decode())
    if (anchor.get("successor_namespace") != f"{TAG}_semantic_source" or
            anchor.get("predecessor_namespace") != PREV or
            anchor.get("formal_global_closure_credit") != 0 or
            anchor.get("successor_checkpoint_object_sha256") != SUCCESSOR):
        raise RuntimeError("active r41 anchor semantics")
    prev_rej = OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json"
    prev_sup = OUT / f"{BASE}_{PREV}_to_{TAG}_static_bundle_rejection_supersession_receipt_v1.json"
    for path in (prev_rej, prev_sup):
        value = json.loads(stable(path).decode())
        if value.get("formal_global_closure_credit") != 0:
            raise RuntimeError(f"chain credit:{path}")
    c53 = stable(C53)
    if sha(c53) != C53_SHA:
        raise RuntimeError("C53 drift")
    return {str(p.relative_to(ROOT)): sha(stable(p)) for p in EXACT8}


def assert_precompute(value: dict[str, Any]) -> None:
    if value.get("status") != (
            "PASS_READ_ONLY_IN_MEMORY_RECONSTRUCTION__ZERO_CREDIT__"
            "RUNTIME_NOT_AUTHORIZED"):
        raise RuntimeError("precompute status")
    recon = value.get("reconstruction", {})
    if tuple(recon.get(k) for k in ("overlay_rows", "successor_rows",
                                    "parent_rows",
                                    "public_unresolved_after_reconstruction")) != \
            (1148, 76832, 862, 0):
        raise RuntimeError("reconstruction census")
    if recon.get("all_parent_unresolved_count_zero") is not True:
        raise RuntimeError("parent unresolved census")
    if value.get("credit", {}).get("formal_global_closure_credit") != 0 or \
            value.get("credit", {}).get("D02_unlock") is not False or \
            value.get("credit", {}).get("runtime_authorized") is not False:
        raise RuntimeError("precompute authorization")
    writes = value.get("writes", {})
    if any(writes.get(k) is not False for k in
           ("deliverables", "runtime", "manifest", "outer", "credit")):
        raise RuntimeError("precompute write claim")


def assert_reviewer(value: dict[str, Any]) -> None:
    if (value.get("status") !=
            "PASS_DUAL_STATIC_CANDIDATE_34_OF_34__RUNTIME_NOT_AUTHORIZED" or
            value.get("check_count") != 34 or
            value.get("failed_check_count") != 0 or
            value.get("read_only") is not True or
            value.get("successor_suffix") != TAG or
            value.get("predecessor_suffix") != PREV):
        raise RuntimeError("reviewer gate")


def no_tagged_pyc() -> None:
    found = [p for p in ROOT.rglob("*.pyc") if TAG in str(p)]
    if found:
        raise RuntimeError("tagged pyc:" + ",".join(map(str, found)))


def preflight() -> tuple[dict[str, Any], bytes]:
    hashes = assert_namespace_and_chain()
    no_tagged_pyc()
    common = dict(os.environ)
    common.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})
    precompute_reports: dict[str, Any] = {}
    precompute_raw: dict[str, bytes] = {}
    for seed in ("1", "99991"):
        env = dict(common, PYTHONHASHSEED=seed)
        value, raw = run_json(["/usr/bin/python3", "-I", "-B", str(HELPER)], env)
        assert_precompute(value)
        precompute_reports[seed] = value
        precompute_raw[seed] = raw
    if (precompute_reports["1"].get("reconstruction") !=
            precompute_reports["99991"].get("reconstruction") or
            precompute_reports["1"].get("canonical_line_sequence_sha256") !=
            precompute_reports["99991"].get("canonical_line_sequence_sha256")):
        raise RuntimeError("precompute dual-seed drift")
    review_reports: dict[str, Any] = {}
    review_raw: dict[str, bytes] = {}
    for seed in ("1", "99991"):
        env = dict(common, PYTHONHASHSEED=seed,
                   CM2_SUCCESSOR_SUFFIX=TAG, CM2_PREDECESSOR_SUFFIX=PREV)
        value, raw = run_json(["/usr/bin/python3", "-I", "-B", str(REVIEWER)], env)
        assert_reviewer(value)
        review_reports[seed] = value
        review_raw[seed] = raw
    if canonical(review_reports["1"]) != canonical(review_reports["99991"]):
        raise RuntimeError("reviewer dual-seed drift")
    no_tagged_pyc()
    if MANIFEST.exists() or OUTER.exists():
        raise RuntimeError("positive cold surfaces appeared")
    recon = precompute_reports["1"]["reconstruction"]
    report: dict[str, Any] = {
        "schema": f"cm2.c79g.{TAG}.no-producer-dual-seed-evidence.v1",
        "status": "PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT",
        "successor_suffix": TAG, "predecessor_suffix": PREV,
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "reconstruction": {k: recon[k] for k in (
            "overlay_rows", "successor_rows", "parent_rows",
            "public_unresolved_after_reconstruction",
            "all_parent_unresolved_count_zero")},
        "seed_invariance": {"seeds": [1, 99991], "pass": True,
            "outer_report_sha256": {"1": sha(precompute_raw["1"]),
                                     "99991": sha(precompute_raw["99991"])}},
        "independent_reviewer": {"status": review_reports["1"]["status"],
            "check_count": 34, "failed_check_count": 0,
            "report_sha256": {"1": sha(review_raw["1"]),
                               "99991": sha(review_raw["99991"])}},
        "source_hashes": hashes,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False,
        "writes": {"deliverables": False, "runtime": False,
                    "manifest": False, "outer": False, "credit": False,
                    "pyc": False},
    }
    report["object_sha256"] = sha(canonical(report))
    return report, canonical(report) + b"\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--seal", action="store_true")
    mode.add_argument("--install", action="store_true")
    args = parser.parse_args(argv)
    try:
        report, raw = preflight()
        if not (args.seal or args.install):
            print(json.dumps({"status": "PREFLIGHT_PASS_R41_NO_PRODUCER__ZERO_CREDIT",
                              "receipt_target": str(RECEIPT.relative_to(ROOT)),
                              "object_sha256": report["object_sha256"],
                              "installation_performed": False,
                              "formal_global_closure_credit": 0,
                              "D02_unlock": False, "runtime_authorized": False},
                             sort_keys=True))
            return 0
        action = install(RECEIPT, raw)
        print(json.dumps({"status": report["status"],
                          "receipt": str(RECEIPT.relative_to(ROOT)),
                          "receipt_sha256": sha(raw),
                          "object_sha256": report["object_sha256"],
                          "action": action}, sort_keys=True))
        return 0
    except KeyboardInterrupt:
        print(json.dumps({"status": "FAIL_CLOSED_R41_NO_PRODUCER_EVIDENCE_INTERRUPTED",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False, "runtime_authorized": False},
                         sort_keys=True))
        return 130
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R41_NO_PRODUCER_EVIDENCE",
                          "error": f"{type(exc).__name__}: {exc}",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False, "runtime_authorized": False},
                         sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
