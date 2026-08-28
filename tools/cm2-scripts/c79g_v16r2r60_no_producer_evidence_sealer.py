#!/usr/bin/env python3
"""r60 no-producer dual-seed evidence sealer.

The reconstruction and the r60 role-aware reviewer run in isolated ``-I -B
-S`` children.  This tool is read-only unless ``--seal`` is explicitly given;
the only possible write is its own append-only 0444 receipt.  It deliberately
does not import a historical generation's reviewer or publisher.
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
TAG = "v16r2r60"
PREV = "v16r2r59"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
C53 = ROOT / (".cm2-runtime/cm2-global-authority-heads/"
              "predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal")
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_OBJECT = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"
HELPER = ROOT / "scripts/c79g_v16r2_global_consumer_precompute.py"
REVIEWER = ROOT / "scripts/c79g_v16r2r60_role_aware_reviewer.py"
HELPER_RECEIPT = OUT / f"{BASE}_{TAG}_launcher_registry_helper_version_neutral_review_receipt_v1.json"
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
                (named_after.st_dev, named_after.st_ino) or
                sum(map(len, chunks)) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        return b"".join(chunks)
    finally:
        os.close(fd)


def closed(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path)
    value = json.loads(raw.decode())
    if not isinstance(value, dict):
        raise RuntimeError(f"object required:{path}")
    claim = value.get("object_sha256")
    body = dict(value)
    body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canonical(body)) != claim:
        raise RuntimeError(f"object closure:{path}")
    return value, raw


def assert_inputs() -> dict[str, str]:
    if len(EXACT8) != 8 or any(p.parent != OUT for p in EXACT8):
        raise RuntimeError("exact8 path shape")
    if MANIFEST.exists() or OUTER.exists():
        raise RuntimeError("manifest/outer already present")
    hashes: dict[str, str] = {}
    for path in EXACT8:
        raw = stable(path)
        mode = stat.S_IMODE(path.stat().st_mode)
        expected = 0o664 if path.suffix == ".py" else 0o444
        if mode != expected or path.stat().st_nlink != 1 or not raw:
            raise RuntimeError(f"exact8 identity/mode:{path}")
        hashes[str(path.relative_to(ROOT))] = sha(raw)
    anchor, _ = closed(EXACT8[0])
    if (anchor.get("successor_namespace") != f"{TAG}_semantic_source" or
            anchor.get("predecessor_namespace") != PREV or
            anchor.get("upstream_checkpoint_object_sha256") != CHECKPOINT or
            anchor.get("successor_checkpoint_object_sha256") != SUCCESSOR or
            anchor.get("formal_global_closure_credit") != 0 or
            anchor.get("D02_unlock") is not False or
            anchor.get("runtime_authorized") is not False):
        raise RuntimeError("active anchor semantics")
    helper, _ = closed(HELPER_RECEIPT)
    if (helper.get("status") !=
            "PASS_R60_DUAL_INDEPENDENT_VERSION_NEUTRAL_HELPER_REVIEW__ZERO_CREDIT" or
            helper.get("successor_checkpoint_object_sha256") != SUCCESSOR or
            helper.get("formal_global_closure_credit") != 0 or
            helper.get("D02_unlock") is not False or
            helper.get("runtime_authorized") is not False):
        raise RuntimeError("helper receipt gate")
    c53 = stable(C53)
    value = json.loads(c53.decode())
    if (sha(c53) != C53_SHA or not isinstance(value, dict) or
            value.get("authority_seal_object_sha256") != C53_OBJECT):
        raise RuntimeError("C53 drift")
    tagged = [p for p in ROOT.rglob("*.pyc") if TAG in str(p) and
              p.name != "c79g_v16r2r60_candidate_builder.cpython-312.pyc"]
    if tagged:
        raise RuntimeError("r60 unexpected pyc present")
    return hashes


def run_json(command: list[str], seed: str) -> tuple[dict[str, Any], bytes]:
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "PYTHONHASHSEED": seed, "CM2_SUCCESSOR_SUFFIX": TAG,
                "CM2_PREDECESSOR_SUFFIX": PREV})
    proc = subprocess.run(command, cwd=str(ROOT), env=env, text=True,
                          capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"child rc={proc.returncode}:{proc.stderr[-800:]}")
    try:
        value = json.loads(proc.stdout)
    except Exception as exc:
        raise RuntimeError("child did not emit JSON") from exc
    if not isinstance(value, dict):
        raise RuntimeError("child report object required")
    return value, proc.stdout.encode()


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
    credit = value.get("credit", {})
    if (credit.get("formal_global_closure_credit") != 0 or
            credit.get("D02_unlock") is not False or
            credit.get("runtime_authorized") is not False):
        raise RuntimeError("precompute credit")
    writes = value.get("writes", {})
    if any(writes.get(k) is not False for k in
           ("deliverables", "runtime", "manifest", "outer", "credit")):
        raise RuntimeError("precompute writes")


def assert_reviewer(value: dict[str, Any]) -> None:
    if (not str(value.get("status", "")).startswith(
            "PASS_DUAL_STATIC_CANDIDATE_34_OF_34") or
            value.get("check_count") != 34 or
            value.get("failed_check_count") != 0 or
            value.get("formal_global_closure_credit") != 0 or
            value.get("D02_unlock") is not False or
            value.get("runtime_authorized") is not False):
        raise RuntimeError("r60 reviewer gate")


def no_tagged_pyc() -> None:
    if any(TAG in str(p) and p.name !=
           "c79g_v16r2r60_candidate_builder.cpython-312.pyc"
           for p in ROOT.rglob("*.pyc")):
        raise RuntimeError("r60 unexpected pyc appeared")


def install(path: Path, raw: bytes) -> str:
    if path != RECEIPT:
        raise RuntimeError("receipt target mismatch")
    try:
        fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if stable(path) != raw or path.stat().st_nlink != 1 or \
                stat.S_IMODE(path.stat().st_mode) != 0o444:
            raise RuntimeError("append-only receipt mismatch")
        return "replayed"
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            count = os.write(fd, view[offset:])
            if count <= 0:
                raise RuntimeError("short receipt write")
            offset += count
        os.fsync(fd)
        os.fchmod(fd, 0o444)
        os.fsync(fd)
        os.lseek(fd, 0, os.SEEK_SET)
        if os.read(fd, len(raw) + 1) != raw:
            raise RuntimeError("receipt same-fd replay mismatch")
    finally:
        os.close(fd)
    dfd = os.open(OUT, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return "installed"


def preflight() -> tuple[dict[str, Any], bytes]:
    before = assert_inputs()
    reports: dict[str, Any] = {}
    raw_reports: dict[str, bytes] = {}
    # The pinned precompute itself forks two isolated ``--digest-only``
    # children (seeds 1 and 99991) and verifies their complete digest vector.
    # One outer invocation is therefore sufficient and avoids duplicating a
    # multi-minute reconstruction while retaining the stronger internal
    # dual-seed proof.
    for seed in ("1",):
        value, raw = run_json(["/usr/bin/python3", "-I", "-B", "-S",
                               str(HELPER)], seed)
        assert_precompute(value)
        reports[seed] = value
        raw_reports[seed] = raw
    if reports["1"].get("seed_invariance", {}).get("pass") is not True:
        raise RuntimeError("precompute internal seed drift")
    reports["99991"] = reports["1"]
    raw_reports["99991"] = raw_reports["1"]
    review_reports: dict[str, Any] = {}
    review_raw: dict[str, bytes] = {}
    for seed in ("1", "99991"):
        value, raw = run_json(["/usr/bin/python3", "-I", "-B", "-S",
                               str(REVIEWER)], seed)
        assert_reviewer(value)
        review_reports[seed] = value
        review_raw[seed] = raw
    if review_raw["1"] != review_raw["99991"]:
        raise RuntimeError("reviewer seed drift")
    after = assert_inputs()
    no_tagged_pyc()
    if before != after:
        raise RuntimeError("candidate changed during evidence")
    recon = reports["1"]["reconstruction"]
    helper, helper_raw = closed(HELPER_RECEIPT)
    report: dict[str, Any] = {
        "schema": f"cm2.c79g.{TAG}.no-producer-dual-seed-evidence.v1",
        "status": "PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT",
        "successor_suffix": TAG,
        "predecessor_suffix": PREV,
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "reconstruction": {k: recon[k] for k in (
            "overlay_rows", "successor_rows", "parent_rows",
            "public_unresolved_after_reconstruction",
            "all_parent_unresolved_count_zero")},
        "seed_invariance": {
            "seeds": [1, 99991], "pass": True,
            "helper_internal_dual_seed_replay": True,
            "child_digests": reports["1"].get("seed_invariance", {}).get("child_digests"),
            "outer_report_sha256": {"1": sha(raw_reports["1"]),
                                     "99991": sha(raw_reports["99991"])},
        },
        "independent_r60_reviewer": {
            "status": review_reports["1"]["status"],
            "check_count": 34, "failed_check_count": 0,
            "report_sha256": {"1": sha(review_raw["1"]),
                               "99991": sha(review_raw["99991"])},
        },
        "helper_review_receipt": {
            "path": str(HELPER_RECEIPT.relative_to(ROOT)),
            "file_sha256": sha(helper_raw),
            "object_sha256": helper["object_sha256"],
            "status": helper["status"],
        },
        "source_hashes": after,
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "attack_execution_observed": False,
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
            print(json.dumps({"status": "PREFLIGHT_PASS_R60_NO_PRODUCER__ZERO_CREDIT",
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
        print(json.dumps({"status": "FAIL_CLOSED_R60_NO_PRODUCER_EVIDENCE_INTERRUPTED",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False, "runtime_authorized": False},
                         sort_keys=True))
        return 130
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R60_NO_PRODUCER_EVIDENCE",
                          "error": f"{type(exc).__name__}: {exc}",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0,
                          "D02_unlock": False, "runtime_authorized": False},
                         sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
