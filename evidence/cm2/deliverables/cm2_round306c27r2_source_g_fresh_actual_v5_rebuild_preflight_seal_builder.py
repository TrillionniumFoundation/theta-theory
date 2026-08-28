#!/usr/bin/env python3
"""Manifest-first zero-credit seal for the truthful actual-v5 preflight REJECT."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
DEFAULT_RUN = (WORKSPACE / ".cm2-runtime/audit/"
               "c27r2-fresh-actual-v5-rebuild-preflight-v1-missing-actual-seal-run")
ACTUAL = (WORKSPACE / ".cm2-runtime/audit/"
          "c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v1/receipt.json")

SOURCE_NAMES = [
    "cm2_round306c27r2_source_g_fresh_actual_v5_rebuild_preflight.py",
    "cm2_round306c27r2_source_g_fresh_actual_v5_rebuild_preflight_runner.py",
    "cm2_round306c27r2_source_g_fresh_actual_v5_rebuild_preflight_independent_verifier.py",
    "cm2_round306c27r2_source_g_fresh_actual_v5_rebuild_preflight_attack_harness.py",
    "cm2_round306c27r2_source_g_fresh_actual_v5_rebuild_preflight_seal_builder.py",
    "cm2_round306c27r2_source_g_fresh_actual_v5_rebuild_preflight_terminal_replay.py",
]


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
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def closed(path: Path, field: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and b"\n" not in raw[:-1], "single object:" + str(path))
    value = json.loads(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "canonical:" + str(path))
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body), "closure:" + str(path))
    return value


def write_new(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default=str(DEFAULT_RUN))
    parser.add_argument("--seal-dir", required=True)
    args = parser.parse_args()
    run = Path(args.run_dir).resolve()
    seal = Path(args.seal_dir).resolve()
    try:
        need(run.is_relative_to(WORKSPACE) and seal.is_relative_to(WORKSPACE),
             "workspace-bound")
        need(not ACTUAL.exists(), "actual receipt must still be absent for reject seal")
        preflight_path = run / "payload/preflight.json"
        execution_path = run / "execution.json"
        verification_path = run / "independent_verification.json"
        attacks_path = run / "coherent_attacks.json"
        preflight = closed(preflight_path, "preflight_sha256")
        execution = closed(execution_path, "execution_sha256")
        verification = closed(verification_path, "verification_sha256")
        attacks = closed(attacks_path, "attack_result_sha256")
        need(preflight.get("decision") == "REJECT"
             and preflight.get("intended_process_exit_code") == 2
             and preflight.get("formal_credit") == 0
             and preflight.get("fresh_C27R2_producer_may_start") is False,
             "preflight reject")
        need(execution.get("numeric_exit") == 2
             and execution.get("signal") is None
             and execution.get("stderr_empty") is True
             and execution.get("truthful_reject") is True
             and execution.get("producer_unchanged") is True
             and execution.get("preflight_file_sha256") == fsha(preflight_path),
             "execution receipt")
        producer_path = HERE / SOURCE_NAMES[0]
        need(execution.get("producer_post_sha256") == fsha(producer_path),
             "execution producer pin")
        need(verification.get("status") ==
             "PASS_INDEPENDENT_NO_IMPORT_TRUTHFUL_REJECT_AND_LOCKED_ACTUAL_INTERFACE__ZERO_CREDIT"
             and verification.get("producer_module_imported") is False
             and verification.get("formal_credit") == 0,
             "independent verification")
        need(attacks.get("status") ==
             "PASS_ALL_COHERENT_ACTUAL_INTERFACE_AND_NONPROMOTION_ATTACKS_REJECTED__ZERO_CREDIT"
             and attacks.get("attack_count") == 41
             and attacks.get("rejected_count") == 41
             and attacks.get("accepted_count") == 0,
             "41 attacks")

        payload_paths = [HERE / name for name in SOURCE_NAMES] + [
            preflight_path, execution_path, run / "stdout.log", run / "stderr.log",
            verification_path, attacks_path,
        ]
        for path in payload_paths:
            need(path.is_file() and path.resolve().is_relative_to(WORKSPACE),
                 "payload exists:" + str(path))
        entries = [(fsha(path), str(path.resolve().relative_to(WORKSPACE)))
                   for path in payload_paths]
        entries.sort(key=lambda item: item[1])
        manifest_bytes = b"".join(
            sha.encode("ascii") + b"  " + rel.encode("utf-8") + b"\n"
            for sha, rel in entries
        )
        seal.mkdir(parents=True, exist_ok=False)
        manifest_path = seal / "payload_manifest.sha256"
        write_new(manifest_path, manifest_bytes)

        body = {
            "schema": "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-preflight-truthful-reject-seal.v1",
            "status": "PASS_SEALED_TRUTHFUL_REJECT_LOCKED_ACTUAL_INTERFACE_VERIFIER_AND_41_ATTACKS__ZERO_CREDIT",
            "preflight_execution": {
                "numeric_exit": 2,
                "signal": None,
                "stderr_empty": True,
                "truthful_reject": True,
                "preflight_file_sha256": fsha(preflight_path),
                "preflight_object_sha256": preflight["preflight_sha256"],
                "execution_file_sha256": fsha(execution_path),
                "execution_object_sha256": execution["execution_sha256"],
            },
            "independent_verification": {
                "file_sha256": fsha(verification_path),
                "object_sha256": verification["verification_sha256"],
                "no_producer_import": True,
            },
            "coherent_attacks": {
                "file_sha256": fsha(attacks_path),
                "object_sha256": attacks["attack_result_sha256"],
                "attack_count": 41,
                "rejected": 41,
                "accepted": 0,
            },
            "actual_gate_contract": {
                "receipt_path": str(ACTUAL.relative_to(WORKSPACE)),
                "receipt_present_at_seal": False,
                "required_before_fresh_C27R2_producer": True,
                "machine_readable_interface": (
                    str(preflight_path.relative_to(WORKSPACE)) + "#/input_interface"
                ),
                "twenty_authority_slot_order_locked": True,
                "three_ledger_schemas_locked": True,
            },
            "payload_manifest": {
                "filename": "payload_manifest.sha256",
                "entry_count": len(entries),
                "file_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            },
            "edge_universe_governance": preflight["edge_universe_governance"],
            "formal_credit": 0,
            "manifest_authorized": False,
            "fresh_C27R2_producer_may_start": False,
            "C27_transition_totality": "UNAUTHORIZED",
            "C28_pair_routing": "UNAUTHORIZED",
            "C29_physical_maximality": "UNAUTHORIZED",
            "C29_patch_or_preservation_permitted": False,
            "Source_W_transition_authorized": False,
            "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        body["receipt_sha256"] = digest(body)
        receipt_path = seal / "receipt.json"
        write_new(receipt_path, canonical(body) + b"\n")
        root_bytes = (
            fsha(manifest_path).encode("ascii") + b"  payload_manifest.sha256\n" +
            fsha(receipt_path).encode("ascii") + b"  receipt.json\n"
        )
        write_new(seal / "root_manifest.sha256", root_bytes)
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": body["status"],
                     "receipt_sha256": body["receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
