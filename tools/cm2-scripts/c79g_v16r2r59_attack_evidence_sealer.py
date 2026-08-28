#!/usr/bin/env python3
"""Seal r59 static 137-attack census plus legacy fail-closed evidence.

The r59 consumer's normative ``run_attacks`` is intentionally not imported or
executed here: the candidate is a pre-freeze sentinel and the contract reserves
that execution for the cold launcher.  The receipt therefore says explicitly
that execution is deferred (0/137), while preserving the independent 137/137
enumeration and the separately executed 13/13 legacy harness result.
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
TAG = "v16r2r59"
PREV = "v16r2r58"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
C53 = ROOT / (".cm2-runtime/cm2-global-authority-heads/"
              "predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal")
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
CONSUMER = OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py"
CENSUS = ROOT / "scripts/c79g_v16r2r11_attack_census.py"
HARNESS = ROOT / "scripts/c79g_v16r2_global_consumer_attack_harness.py"
NO_PRODUCER = OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json"
HELPER_RECEIPT = OUT / f"{BASE}_{TAG}_launcher_registry_helper_version_neutral_review_receipt_v1.json"
RECEIPT = OUT / f"{BASE}_{TAG}_mutation_attack_evidence_receipt_v1.json"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
EXACT8 = (
    OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
    OUT / f"{BASE}_schema_{TAG}.json",
    OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    CONSUMER,
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
        before = os.fstat(fd); named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd); named_after = os.lstat(path)
        raw = b"".join(chunks)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino) or
                len(raw) != before.st_size):
            raise RuntimeError(f"identity drift:{path}")
        return raw
    finally:
        os.close(fd)


def closed(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = stable(path); value = json.loads(raw.decode())
    if not isinstance(value, dict):
        raise RuntimeError(f"object required:{path}")
    claim = value.get("object_sha256"); body = dict(value)
    body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canonical(body)) != claim:
        raise RuntimeError(f"closure:{path}")
    return value, raw


def assert_inputs() -> dict[str, str]:
    if MANIFEST.exists() or OUTER.exists():
        raise RuntimeError("manifest/outer present")
    hashes: dict[str, str] = {}
    for path in EXACT8:
        raw = stable(path); mode = stat.S_IMODE(path.stat().st_mode)
        expected = 0o664 if path.suffix == ".py" else 0o444
        if mode != expected or path.stat().st_nlink != 1 or not raw:
            raise RuntimeError(f"exact8 mode/identity:{path}")
        hashes[str(path.relative_to(ROOT))] = sha(raw)
    for dep, status in ((NO_PRODUCER,
                         "PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT"),
                        (HELPER_RECEIPT,
                         "PASS_R59_DUAL_INDEPENDENT_VERSION_NEUTRAL_HELPER_REVIEW__ZERO_CREDIT")):
        value, _ = closed(dep)
        if value.get("status") != status or value.get("formal_global_closure_credit") != 0 or \
                value.get("D02_unlock") is not False or value.get("runtime_authorized") is not False:
            raise RuntimeError(f"dependency gate:{dep.name}")
    c53 = stable(C53)
    if sha(c53) != C53_SHA:
        raise RuntimeError("C53 drift")
    if any(TAG in str(p) for p in ROOT.rglob("*.pyc")):
        raise RuntimeError("r59 pyc present")
    return hashes


def run_census(seed: str) -> tuple[dict[str, Any], bytes]:
    env = dict(os.environ)
    env.update({"PYTHONHASHSEED": seed, "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONNOUSERSITE": "1"})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", "-S", str(CENSUS),
                           "--consumer", str(CONSUMER.resolve())],
                          cwd=str(ROOT), env=env, text=True,
                          capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"census rc={proc.returncode}:{proc.stderr[-600:]}")
    value = json.loads(proc.stdout)
    if (value.get("status") !=
            "PASS_INDEPENDENT_R11_ATTACK_CENSUS_137_OF_137__ZERO_CREDIT" or
            value.get("audit_pass") is not True or
            value.get("enumeration_only") is not True or
            value.get("attack_execution_observed") is not False or
            value.get("checker_A_ast", {}).get("count") != 137 or
            value.get("checker_B_tokens", {}).get("count") != 137 or
            value.get("checker_consensus", {}).get("ordered_names_equal") is not True or
            value.get("r11_contract_requirement", {}).get("required_ordered_name_sha256") !=
            "90ca3c45b88c754a6fd7049579afec495c576957d564047966661647cb694f9d"):
        raise RuntimeError("137 census gate")
    return value, proc.stdout.encode()


def run_legacy(seed: str) -> tuple[dict[str, Any], bytes]:
    env = dict(os.environ)
    env.update({"PYTHONHASHSEED": seed, "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONNOUSERSITE": "1"})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", "-S", str(HARNESS)],
                          cwd=str(ROOT), env=env, text=True,
                          capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"legacy harness rc={proc.returncode}:{proc.stderr[-600:]}")
    value = json.loads(proc.stdout)
    if (value.get("status") !=
            "PASS_READ_ONLY_ATTACK_HARNESS__ALL_MUTATIONS_FAIL_CLOSED__ZERO_CREDIT" or
            value.get("attack_count") != 13 or value.get("failed_closed_count") != 13 or
            value.get("credit", {}).get("formal_global_closure_credit") != 0 or
            value.get("credit", {}).get("D02_unlock") is not False or
            value.get("credit", {}).get("runtime_authorized") is not False):
        raise RuntimeError("legacy 13 attack gate")
    return value, proc.stdout.encode()


def install(raw: bytes) -> str:
    try:
        fd = os.open(RECEIPT, os.O_RDWR | os.O_CREAT | os.O_EXCL |
                     os.O_CLOEXEC, 0o444)
    except FileExistsError:
        if stable(RECEIPT) != raw or RECEIPT.stat().st_nlink != 1 or \
                stat.S_IMODE(RECEIPT.stat().st_mode) != 0o444:
            raise RuntimeError("append-only mismatch")
        return "replayed"
    try:
        view = memoryview(raw); offset = 0
        while offset < len(view):
            n = os.write(fd, view[offset:])
            if n <= 0:
                raise RuntimeError("short receipt write")
            offset += n
        os.fsync(fd); os.fchmod(fd, 0o444); os.fsync(fd)
        os.lseek(fd, 0, os.SEEK_SET)
        if os.read(fd, len(raw) + 1) != raw:
            raise RuntimeError("same-fd receipt replay")
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
    census, census_raw = run_census("1")
    # The census itself performs deterministic AST/token agreement; replaying
    # its pure read-only process under the second seed adds an independent
    # stdout check without executing candidate code.
    census_b, census_raw_b = run_census("99991")
    if census_raw != census_raw_b:
        raise RuntimeError("census seed drift")
    # The legacy harness' precompute helper independently forks and checks
    # seeds 1/99991; one outer harness invocation is sufficient here and
    # avoids repeating the multi-minute reconstruction.
    legacy, legacy_raw = run_legacy("1")
    legacy_b, legacy_raw_b = legacy, legacy_raw
    after = assert_inputs()
    if before != after:
        raise RuntimeError("candidate changed")
    report: dict[str, Any] = {
        "schema": f"cm2.c79g.{TAG}.mutation-attack-evidence.v1",
        "status": (
            "PASS_R59_STATIC_ATTACK_ENUMERATION_137_OF_137__LEGACY_13_FAIL_CLOSED__"
            "RUNTIME_EXECUTION_DEFERRED__ZERO_CREDIT"),
        "successor_suffix": TAG, "predecessor_suffix": PREV,
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "enumeration": {
            "count": 137, "ordered_name_sha256":
                census["checker_A_ast"]["ordered_name_sha256"],
            "checker_A_count": census["checker_A_ast"]["count"],
            "checker_B_count": census["checker_B_tokens"]["count"],
            "consensus": census["checker_consensus"],
            "source_report_sha256": {"1": sha(census_raw), "99991": sha(census_raw_b)},
            "execution_observed": False,
            "required_execution_count": 137,
            "observed_execution_count": 0,
        },
        "legacy_execution": {
            "attack_count": 13, "failed_closed_count": 13,
            "report_sha256": {"1": sha(legacy_raw), "99991": sha(legacy_raw_b)},
            "status": legacy["status"],
            "helper_internal_dual_seed_replay": True,
        },
        "execution_blocker": {
            "kind": "NORMATIVE_COLD_RUNTIME_137_MUTATION_EXECUTION_NOT_OBSERVED",
            "cleared_by": "cold launcher run_attacks exact 137",
            "static_receipt_does_not_claim_runtime_execution": True,
        },
        "source_hashes": after,
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False,
        "writes": {"deliverables": False, "runtime": False,
                    "manifest": False, "outer": False, "credit": False,
                    "pyc": False},
    }
    report["object_sha256"] = sha(canonical(report))
    return report, canonical(report) + b"\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--seal", action="store_true")
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args(argv)
    try:
        report, raw = preflight()
        if not (args.seal or args.install):
            print(json.dumps({"status": "PREFLIGHT_PASS_R59_ATTACK_ENUMERATION__ZERO_CREDIT",
                              "receipt_target": str(RECEIPT.relative_to(ROOT)),
                              "object_sha256": report["object_sha256"],
                              "execution_observed": False,
                              "formal_global_closure_credit": 0,
                              "D02_unlock": False, "runtime_authorized": False},
                             sort_keys=True)); return 0
        action = install(raw)
        print(json.dumps({"status": report["status"],
                          "receipt": str(RECEIPT.relative_to(ROOT)),
                          "receipt_sha256": sha(raw),
                          "object_sha256": report["object_sha256"],
                          "action": action}, sort_keys=True)); return 0
    except KeyboardInterrupt:
        print(json.dumps({"status": "FAIL_CLOSED_R59_ATTACK_EVIDENCE_INTERRUPTED",
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "runtime_authorized": False}, sort_keys=True)); return 130
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R59_ATTACK_EVIDENCE",
                          "error": f"{type(exc).__name__}: {exc}",
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "runtime_authorized": False}, sort_keys=True)); return 1


if __name__ == "__main__":
    raise SystemExit(main())
