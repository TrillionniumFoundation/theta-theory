#!/usr/bin/env python3
"""Manifest-first zero-credit seal for the truthful-REJECT rebuild preflight."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parent.parent
ACTUAL = (WORKSPACE / ".cm2-runtime/audit/"
          "c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v2/receipt.json")


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def closed(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    need(type(value) is dict, path.name + ":object")
    body = dict(value)
    claim = body.pop(field, None)
    need(type(claim) is str and claim == digest(body), path.name + ":closure")
    return value


def write_new(path: Path, payload: bytes) -> None:
    path = path.resolve()
    need(path.is_relative_to(WORKSPACE), "output:workspace")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def rel(path: Path) -> str:
    path = path.resolve()
    need(path.is_relative_to(WORKSPACE), "payload:workspace")
    return str(path.relative_to(WORKSPACE))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--seal-dir", required=True)
    parser.add_argument("--producer", required=True)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--builder", required=True)
    parser.add_argument("--terminal-replay", required=True)
    args = parser.parse_args()
    try:
        run = Path(args.run_dir).resolve()
        seal = Path(args.seal_dir).resolve()
        need(run.is_relative_to(WORKSPACE) and run.is_dir(), "run-dir")
        need(seal.is_relative_to(WORKSPACE) and not seal.exists(), "seal-dir:fresh")
        receipt_path = run / "preflight.json"
        execution_path = run / "execution.json"
        verification_path = run / "independent_verification.json"
        attacks_path = run / "coherent_attacks.json"
        preflight = closed(receipt_path, "preflight_sha256")
        execution = closed(execution_path, "execution_sha256")
        verification = closed(verification_path, "verification_sha256")
        attacks = closed(attacks_path, "attacks_sha256")
        need(preflight["decision"] == "REJECT"
             and preflight["fresh_C27R2_C28_C29_producer_may_start"] is False,
             "preflight:reject")
        need(execution["numeric_exit_code"] == 2 and execution["signal"] is None
             and execution["stdout_empty"] is True and execution["stderr_empty"] is True,
             "execution:truthful-reject")
        need(execution["preflight_file_sha256"] == fsha(receipt_path),
             "execution:receipt-pin")
        need(verification["decision"] == "PASS"
             and verification["details"]["actual_gate_missing"] is True,
             "verification:pass")
        need(attacks["attacks"] == attacks["rejected"] == 42
             and attacks["accepted"] == 0, "attacks:42")
        need(not ACTUAL.exists(), "actual:still-missing")

        payload_paths = [
            receipt_path, execution_path, verification_path, attacks_path,
            run / "stdout.log", run / "stderr.log",
            Path(args.producer), Path(args.runner), Path(args.verifier),
            Path(args.attacks), Path(args.builder), Path(args.terminal_replay),
            WORKSPACE / ".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json",
        ]
        for item in preflight["sealed_subauthorities_consumed"]:
            payload_paths.append(WORKSPACE / item["receipt"]["path"])
            payload_paths.append(WORKSPACE / item["cold_replay"]["path"])
        need(len(payload_paths) == 21 and len({p.resolve() for p in payload_paths}) == 21,
             "payload:21-unique")
        entries = sorted((rel(path), fsha(path)) for path in payload_paths)
        manifest_payload = b"".join(
            sha.encode("ascii") + b"  " + path.encode("utf-8") + b"\n"
            for path, sha in entries)
        seal.mkdir(parents=True, mode=0o700)
        manifest_path = seal / "payload_manifest.sha256"
        write_new(manifest_path, manifest_payload)
        body = {
            "schema": "cm2.round306c27r2-c28-c29.post-actual-v5-rebuild-preflight-zero-credit-seal.v1",
            "status": "PASS_SEALED_TRUTHFUL_REJECT_ACTUAL_V5_V2_MISSING__NO_IMPORT_VERIFIER__42_ATTACKS__ZERO_CREDIT",
            "preflight": {
                "file_sha256": fsha(receipt_path),
                "object_sha256": preflight["preflight_sha256"],
                "numeric_exit_code": execution["numeric_exit_code"],
                "signal": execution["signal"], "stdout_empty": True, "stderr_empty": True,
            },
            "independent_verification": {
                "file_sha256": fsha(verification_path),
                "object_sha256": verification["verification_sha256"],
                "producer_module_imported": False,
            },
            "coherent_resigned_attacks": {
                "file_sha256": fsha(attacks_path),
                "object_sha256": attacks["attacks_sha256"],
                "attacks": 42, "rejected": 42, "accepted": 0,
            },
            "exact_eventual_contract": preflight["eventual_exact_global_conservation"],
            "diagnostics_never_authority": {
                "component_edge_expectation": 14_860,
                "fresh_DSU_component_expectation": 43_684,
                "historical_14772_or_14724_used": False,
            },
            "actual_gate_v2_receipt_present": False,
            "fresh_C27R2_C28_C29_producer_may_start": False,
            "payload_manifest": {
                "path": rel(manifest_path), "entry_count": len(entries),
                "file_sha256": hashlib.sha256(manifest_payload).hexdigest(),
            },
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED", "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "Source_W_transition_authorized": False, "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        body["receipt_sha256"] = digest(body)
        seal_receipt = seal / "receipt.json"
        write_new(seal_receipt, canonical(body) + b"\n")
        root_payload = (
            hashlib.sha256(manifest_payload).hexdigest().encode("ascii")
            + b"  payload_manifest.sha256\n"
            + fsha(seal_receipt).encode("ascii") + b"  receipt.json\n"
        )
        write_new(seal / "root_manifest.sha256", root_payload)
        return 0
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as exc:
        print("REJECT:" + str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
