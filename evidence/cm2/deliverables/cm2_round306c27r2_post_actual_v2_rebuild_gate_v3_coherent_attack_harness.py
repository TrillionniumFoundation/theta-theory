#!/usr/bin/env python3
"""Coherent fail-closed attacks for the zero-credit C27R2 rebuild gate v3.

The harness mutates and re-closes the gate receipt, then requires the pinned
independent verifier to reject every forged authority claim without producing
a verification artifact.  It does not import the producer or verifier and it
cannot start a C27R2 rebuild.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
from typing import Any, Callable


PYTHON = Path("/usr/bin/python3.12")
PYTHON_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
GATE_SCHEMA = "cm2.round306c27r2.post-actual-v2-rebuild-gate.v3"
VERIFICATION_SCHEMA = (
    "cm2.round306c27r2.post-actual-v2-rebuild-gate-independent-verification.v3"
)
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_INDEPENDENT_GATE_RECEIPT_SERVICE_ROOT_PAYLOAD_AND_GOVERNANCE_"
    "VERIFICATION__ZERO_CREDIT"
)


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def wire(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate-key:" + key)
        result[key] = value
    return result


def parse_closed(path: Path, closure: str, label: str) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    value = json.loads(
        raw, object_pairs_hook=unique,
        parse_constant=lambda item: (_ for _ in ()).throw(
            Reject(label + ":nonfinite:" + item)))
    need(type(value) is dict and raw == wire(value) + b"\n", label + ":canonical")
    body = dict(value)
    claim = body.pop(closure, None)
    need(type(claim) is str and claim == object_sha(body), label + ":closure")
    return value, raw


def file_sha(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular-single-link:" + str(path))
        identity = (before.st_dev, before.st_ino, before.st_mode,
                    before.st_nlink, before.st_size, before.st_mtime_ns,
                    before.st_ctime_ns, before.st_uid, before.st_gid)
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        need(identity == (after.st_dev, after.st_ino, after.st_mode,
                          after.st_nlink, after.st_size, after.st_mtime_ns,
                          after.st_ctime_ns, after.st_uid, after.st_gid),
             "stable-fstat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def write_new(path: Path, raw: bytes) -> None:
    need(path.parent.is_dir(), "output-parent")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(descriptor, raw)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def reclose(receipt: dict[str, Any]) -> bytes:
    body = copy.deepcopy(receipt)
    body.pop("gate_receipt_sha256", None)
    body["gate_receipt_sha256"] = object_sha(body)
    return wire(body) + b"\n"


def mutations(receipt: dict[str, Any]) -> list[tuple[str, Callable[[dict[str, Any]], None], bool]]:
    attacks: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = [
        ("schema_forgery", lambda x: x.__setitem__("schema", GATE_SCHEMA + ".forged"), True),
        ("status_forgery", lambda x: x.__setitem__("status", "PASS_FORGED_AUTHORITY"), True),
        ("decision_flip", lambda x: x.__setitem__("decision", "REJECT" if x["decision"] == "PASS" else "PASS"), True),
        ("exit_code_forgery", lambda x: x.__setitem__("intended_process_exit_code", 7), True),
        ("self_test_mode_forgery", lambda x: x.__setitem__("self_test_mode", "FORGED"), True),
        ("terminal_validation_flip", lambda x: x.__setitem__("actual_v2_terminal_gate_validated", not x["actual_v2_terminal_gate_validated"]), True),
        ("launch_permission_flip", lambda x: x.__setitem__("fresh_C27R2_rebuild_may_start", not x["fresh_C27R2_rebuild_may_start"]), True),
        ("formal_credit_mint", lambda x: x.__setitem__("formal_credit", 1), True),
        ("manifest_authorization_mint", lambda x: x.__setitem__("manifest_authorized", True), True),
        ("C27R2_authority_mint", lambda x: x.__setitem__("C27R2", "REBUILT_AND_CREDITED"), True),
        ("C28_authority_mint", lambda x: x.__setitem__("C28", "AUTHORIZED"), True),
        ("C29_authority_mint", lambda x: x.__setitem__("C29", "AUTHORIZED"), True),
        ("CM2_claim_mint", lambda x: x.__setitem__("CM2", "GO_FOR_CLAIM"), True),
        ("required_field_removal", lambda x: x.pop("decision"), True),
        ("stale_object_closure", lambda x: x.__setitem__("formal_credit", 1), False),
    ]
    if receipt["decision"] == "PASS":
        attacks.append((
            "derived_cross_pair_denominator_forgery",
            lambda x: x["derived_post_rebuild_contract"].__setitem__(
                "post_C27R2_cross_component_pair_denominator", 125_561_998_197),
            True,
        ))
    else:
        attacks.append((
            "negative_missing_path_forgery",
            lambda x: x.__setitem__("missing_required_paths", [str(Path.cwd())]),
            True,
        ))
    return attacks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--control-verification", required=True)
    parser.add_argument("--verifier-source", required=True)
    parser.add_argument("--producer-source", required=True)
    parser.add_argument("--expect-verifier-sha256", required=True)
    parser.add_argument("--expect-producer-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        receipt_path = Path(args.receipt).resolve()
        verification_path = Path(args.control_verification).resolve()
        verifier = Path(args.verifier_source).resolve()
        producer = Path(args.producer_source).resolve()
        need(file_sha(PYTHON) == PYTHON_SHA256, "python-pin")
        need(file_sha(verifier) == args.expect_verifier_sha256,
             "verifier-source-pin")
        need(file_sha(producer) == args.expect_producer_sha256,
             "producer-source-pin")
        receipt, receipt_raw = parse_closed(
            receipt_path, "gate_receipt_sha256", "gate-receipt")
        verification, _ = parse_closed(
            verification_path, "verification_sha256", "control-verification")
        need(receipt["schema"] == GATE_SCHEMA, "control-gate-schema")
        need(verification["schema"] == VERIFICATION_SCHEMA
             and verification["status"] == VERIFICATION_STATUS
             and verification["gate_receipt_file_sha256"]
                 == hashlib.sha256(receipt_raw).hexdigest()
             and verification["gate_receipt_object_sha256"]
                 == receipt["gate_receipt_sha256"]
             and verification["gate_decision"] == receipt["decision"]
             and verification["fresh_C27R2_rebuild_may_start"]
                 is receipt["fresh_C27R2_rebuild_may_start"]
             and verification["source_audit"]["sha256"]
                 == args.expect_producer_sha256
             and verification["formal_credit"] == 0
             and verification["manifest_authorized"] is False
             and verification["C27R2"] == "NOT_REBUILT_NOT_CREDITED"
             and verification["C28"] == verification["C29"] == "UNAUTHORIZED"
             and verification["CM2"] == "NO-GO_FOR_CLAIM",
             "control-verification-binding")

        results = []
        with tempfile.TemporaryDirectory(
                prefix="cm2-c27r2-gate-v3-coherent-attacks-") as temporary:
            temp = Path(temporary)
            for ordinal, (name, mutate, close) in enumerate(mutations(receipt)):
                forged = copy.deepcopy(receipt)
                mutate(forged)
                if close:
                    forged_raw = reclose(forged)
                else:
                    forged_raw = wire(forged) + b"\n"
                forged_path = temp / f"attack-{ordinal:02d}.json"
                forged_path.write_bytes(forged_raw)
                attempted_output = temp / f"attack-{ordinal:02d}-verification.json"
                process = subprocess.run([
                    str(PYTHON), str(verifier),
                    "--receipt", str(forged_path),
                    "--producer-source", str(producer),
                    "--expect-producer-sha256", args.expect_producer_sha256,
                    "--output", str(attempted_output),
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                need(process.returncode == 2 and process.stderr == b""
                     and process.stdout.startswith(b"REJECT:")
                     and not attempted_output.exists(),
                     "attack-not-rejected:" + name)
                results.append({
                    "attack": name,
                    "forged_receipt_sha256": hashlib.sha256(forged_raw).hexdigest(),
                    "verifier_exit_code": process.returncode,
                    "verification_artifact_created": False,
                    "rejected": True,
                })

        body = {
            "schema": "cm2.round306c27r2.post-actual-v2-rebuild-gate-coherent-attacks.v3",
            "status": "PASS_16_OF_16_COHERENT_GATE_AUTHORITY_FORGERIES_REJECTED__ZERO_CREDIT",
            "gate_receipt_file_sha256": hashlib.sha256(receipt_raw).hexdigest(),
            "gate_receipt_object_sha256": receipt["gate_receipt_sha256"],
            "control_verification_file_sha256": file_sha(verification_path),
            "control_verification_object_sha256": verification["verification_sha256"],
            "producer_source_sha256": args.expect_producer_sha256,
            "verifier_source_sha256": args.expect_verifier_sha256,
            "attack_total": len(results), "attack_passed": len(results),
            "all_forged_receipts_rejected_without_artifact": True,
            "attacks": results,
            "fresh_C27R2_rebuild_may_start": receipt["fresh_C27R2_rebuild_may_start"],
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "NOT_REBUILT_NOT_CREDITED",
            "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        need(len(results) == 16, "exactly-16-attacks")
        body["attack_result_sha256"] = object_sha(body)
        write_new(Path(args.output).resolve(), wire(body) + b"\n")
        print(wire({"status": body["status"],
                    "attack_result_sha256": body["attack_result_sha256"],
                    "attack_passed": body["attack_passed"]}).decode("ascii"))
        return 0
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError, subprocess.SubprocessError) as error:
        print("REJECT:" + str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
