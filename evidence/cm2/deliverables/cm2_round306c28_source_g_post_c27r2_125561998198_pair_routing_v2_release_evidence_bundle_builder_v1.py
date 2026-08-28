#!/usr/bin/env python3
"""Build the zero-credit C28-v2 release evidence bundle.

The builder requires a clean, terminal-pending core service, exact core and
cold receipts, and 32/32 release-only attack rejection.  It opens every
declared authority member with O_NOFOLLOW, records SHA256 plus a nine-field
stat fingerprint, and requires path/fd identity before emitting a sorted
inventory and closed evidence document.  It cannot create manifests, seals,
terminal receipts, or authority.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
PREFIX = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
)
CORE_SCHEMA = PREFIX + "gated-dual-seed-core-receipt.v1"
CORE_STATUS = (
    "PASS_C27R2_TERMINAL_ADAPTER_DUAL_TRUE_SEED_THREE_FILE_CANDIDATES_"
    "TWO_NO_IMPORT_VERIFIERS_AND_26_ATTACKS__ZERO_CREDIT_PENDING_RELEASE"
)
CORE_PASS = b"PASS_C28_PAIR_ROUTING_V2_DUAL_SEED_CORE__ZERO_CREDIT\n"
COLD_SCHEMA = PREFIX + "release-cold-replay-receipt.v1"
COLD_STATUS = (
    "PASS_FRESH_NO_IMPORT_C28_PAIR_ROUTING_COLD_BYTE_REPLAY_WITH_ALL_"
    "DECLARED_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT"
)
ATTACK_SCHEMA = PREFIX + "release-only-attack-harness.v1"
ATTACK_STATUS = (
    "PASS_BASELINE_AND_32_OF_32_RELEASE_ONLY_ATTACKS_REJECTED_FAIL_"
    "CLOSED__ZERO_CREDIT_PENDING_EVIDENCE_MANIFEST_OUTER_AND_TERMINAL"
)
EVIDENCE_SCHEMA = PREFIX + "release-evidence-bundle.v1"
EVIDENCE_STATUS = (
    "PASS_C28_CORE_COLD_32_RELEASE_ATTACKS_AND_ALL_AUTHORITY_INPUT_"
    "SHA_STAT_EVIDENCE__ZERO_CREDIT"
)
EXPECTED = {
    "members": 502_204,
    "post_components": 43_684,
    "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508,
    "cross_pairs": 125_561_998_198,
    "blocks": 256,
    "shards": 32_896,
}


class Blocked(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (type(value) is str and len(value) == 64
            and all(character in "0123456789abcdef" for character in value))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result,
                 "unique JSON key:" + str(key))
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


class Capture:
    def __init__(self, path: Path):
        self.path = path.absolute()
        need(self.path.resolve(strict=True) == self.path,
             "canonical path:" + str(path))
        self.fd = os.open(self.path, os.O_RDONLY
                          | getattr(os, "O_CLOEXEC", 0)
                          | getattr(os, "O_NOFOLLOW", 0))
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1,
             "regular singleton:" + str(path))
        self.sha256 = self._hash()

    def _hash(self) -> str:
        os.lseek(self.fd, 0, os.SEEK_SET)
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             "stable fd hash:" + str(self.path))
        return state.hexdigest()

    def bytes(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             "stable fd read:" + str(self.path))
        return b"".join(chunks)

    def document(self, closure: str) -> dict[str, Any]:
        payload = self.bytes()
        need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
             "JSON newline:" + str(self.path))
        value = strict_load(payload[:-1])
        need(type(value) is dict and canonical(value) == payload[:-1],
             "canonical JSON:" + str(self.path))
        body = dict(value)
        claim = body.pop(closure, None)
        need(valid_sha(claim) and claim == digest(body),
             "object closure:" + str(self.path))
        return value

    def attest(self) -> dict[str, Any]:
        current_fd = os.fstat(self.fd)
        current_path = os.stat(self.path, follow_symlinks=False)
        need(fingerprint(current_fd) == fingerprint(self.before)
             and fingerprint(current_path) == fingerprint(self.before)
             and self._hash() == self.sha256,
             "pre/post SHA/stat/path identity:" + str(self.path))
        return {
            "path": str(self.path.relative_to(ROOT)),
            "sha256": self.sha256, "size": self.before.st_size,
            "stat_fingerprint": list(fingerprint(self.before)),
            "O_NOFOLLOW": True, "single_link": True,
            "fd_and_path_pre_post_identity": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def file_sha(path: Path) -> str:
    capture = Capture(path)
    try:
        return capture.sha256
    finally:
        capture.close()


def document(path: Path, closure: str) -> dict[str, Any]:
    capture = Capture(path)
    try:
        return capture.document(closure)
    finally:
        capture.close()


def write_once(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(fd, payload[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)


def audit_dir(raw: str) -> Path:
    path = Path(raw).absolute()
    need(path.parent == AUDIT and path.is_dir() and not path.is_symlink(),
         "existing direct audit directory:" + str(path))
    return path


def service_success(unit: str, invocation: str) -> None:
    completed = subprocess.run([
        "/usr/bin/systemctl", "--user", "show", unit,
        "-p", "ActiveState", "-p", "SubState", "-p", "Result",
        "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID",
    ], cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
       stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"",
         "query core service")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == invocation,
         "exact core service clean success")


def recursive_paths(directories: list[Path]) -> list[Path]:
    result: list[Path] = []
    for directory in directories:
        for current, directory_names, file_names in os.walk(directory):
            base = Path(current)
            for name in directory_names:
                need(not (base / name).is_symlink(), "no symlink directory")
            for name in sorted(file_names):
                path = base / name
                need(path.is_file() and not path.is_symlink(),
                     "regular evidence input:" + str(path))
                result.append(path)
    need(result and len(result) == len(set(result)),
         "nonempty disjoint evidence roots")
    return sorted(result)


def validate_boundaries(args: argparse.Namespace) -> dict[str, Any]:
    control = audit_dir(args.core_control_dir)
    cold_control = audit_dir(args.cold_control_dir)
    attacks_dir = audit_dir(args.release_attack_dir)
    core_path = control / "core_receipt.json"
    core = document(core_path, "core_receipt_sha256")
    need(file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA
         and core.get("status") == CORE_STATUS
         and core.get("exact_math") == EXPECTED
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and (control / "PASS.lock").read_bytes() == CORE_PASS
         and file_sha(control / "PASS.lock") == args.expect_core_pass_sha256,
         "exact core receipt/PASS boundary")
    cold_path = cold_control / "cold_replay_receipt.json"
    cold = document(cold_path, "cold_replay_receipt_sha256")
    need(file_sha(cold_path) == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and cold.get("schema") == COLD_SCHEMA
         and cold.get("status") == COLD_STATUS
         and cold.get("cold_replay_byte_identical") is True
         and cold.get("all_declared_core_inputs_pre_post_sha_stat_identical")
             is True
         and cold.get("formal_credit") == 0
         and cold.get("manifest_authorized") is False,
         "exact cold replay boundary")
    attacks_path = attacks_dir / "release_attacks.json"
    attacks = document(attacks_path, "release_attack_receipt_sha256")
    need(file_sha(attacks_path) == args.expect_release_attack_file_sha256
         and attacks["release_attack_receipt_sha256"]
             == args.expect_release_attack_object_sha256
         and attacks.get("schema") == ATTACK_SCHEMA
         and attacks.get("status") == ATTACK_STATUS
         and attacks.get("attack_census") == {
             "planned": 32, "executed": 32,
             "rejected_fail_closed": 32, "accepted": 0,
         }
         and attacks.get("authoritative_inputs_pre_post_sha_stat_identical")
             is True
         and attacks.get("formal_credit") == 0
         and attacks.get("manifest_authorized") is False,
         "exact release attack boundary")
    return {"core": core, "cold": cold, "attacks": attacks}


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_builder_sha256,
            args.expect_core_receipt_file_sha256,
            args.expect_core_receipt_object_sha256,
            args.expect_core_pass_sha256,
            args.expect_cold_receipt_file_sha256,
            args.expect_cold_receipt_object_sha256,
            args.expect_release_attack_file_sha256,
            args.expect_release_attack_object_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_builder_sha256,
         "evidence builder self/all boundary pins")
    need(type(args.core_unit) is str and args.core_unit.endswith(".service")
         and type(args.expect_core_invocation_id) is str
         and len(args.expect_core_invocation_id) == 32
         and all(character in "0123456789abcdef"
                 for character in args.expect_core_invocation_id),
         "unit/invocation syntax")
    output = Path(args.output_dir).absolute()
    need(output.parent == AUDIT and not output.exists()
         and not output.is_symlink(), "fresh evidence output")
    service_success(args.core_unit, args.expect_core_invocation_id)
    validated = validate_boundaries(args)
    roots = [audit_dir(raw) for raw in args.evidence_root]
    required = {audit_dir(args.core_control_dir),
                audit_dir(args.cold_control_dir),
                audit_dir(args.release_attack_dir)}
    need(required.issubset(set(roots)) and len(roots) >= 12,
         "declared evidence roots cover core/cold/attacks")
    captures = [Capture(path) for path in recursive_paths(roots)]
    captures.append(Capture(SELF))
    try:
        if args.preflight_only:
            for capture in captures:
                capture.attest()
            return {"status":
                    "PASS_C28_RELEASE_EVIDENCE_PREFLIGHT__NO_OUTPUT_CREATED_ZERO_CREDIT"}
        attestations: dict[str, dict[str, Any]] = {}
        for capture in captures:
            value = capture.attest()
            need(value["path"] not in attestations,
                 "unique evidence member:" + value["path"])
            attestations[value["path"]] = value
        attestations = dict(sorted(attestations.items()))
        inventory_raw = ("\n".join(
            f"{value['sha256']}  {path}"
            for path, value in attestations.items()) + "\n").encode("ascii")
        body = {
            "schema": EVIDENCE_SCHEMA, "status": EVIDENCE_STATUS,
            "built_at_utc": utc_now(),
            "core_unit": args.core_unit,
            "core_invocation_id": args.expect_core_invocation_id,
            "core_receipt_file_sha256":
                args.expect_core_receipt_file_sha256,
            "core_receipt_object_sha256":
                args.expect_core_receipt_object_sha256,
            "cold_receipt_file_sha256":
                args.expect_cold_receipt_file_sha256,
            "cold_receipt_object_sha256":
                args.expect_cold_receipt_object_sha256,
            "release_attack_file_sha256":
                args.expect_release_attack_file_sha256,
            "release_attack_object_sha256":
                args.expect_release_attack_object_sha256,
            "authority_member_count": len(attestations),
            "authority_inventory_sha256":
                hashlib.sha256(inventory_raw).hexdigest(),
            "attestations": attestations,
            "validated_projection": {
                "exact_math": EXPECTED,
                "dual_seed_candidate_byte_identity": True,
                "two_no_import_verifiers": True,
                "core_attacks_rejected": 26,
                "cold_replay_byte_identical":
                    validated["cold"]["cold_replay_byte_identical"],
                "release_attacks_rejected": 32,
                "all_authority_inputs_pre_post_sha_stat_identical": True,
                "core_receipt_object_sha256":
                    validated["core"]["core_receipt_sha256"],
                "cold_receipt_object_sha256":
                    validated["cold"]["cold_replay_receipt_sha256"],
                "release_attack_object_sha256":
                    validated["attacks"]["release_attack_receipt_sha256"],
            },
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
            "C28": "UNAUTHORIZED_PENDING_MANIFEST_OUTER_AND_TERMINAL_REPLAY",
            "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        result = {**body, "evidence_bundle_sha256": digest(body)}
        output.mkdir(mode=0o700)
        write_once(output / "authority_inventory.sha256", inventory_raw)
        write_once(output / "evidence_bundle.json", canonical(result) + b"\n")
        return result
    finally:
        for capture in captures:
            capture.close()


def self_test() -> dict[str, Any]:
    body = {"schema": EVIDENCE_SCHEMA, "status": EVIDENCE_STATUS,
            "exact_math": EXPECTED, "formal_credit": 0}
    need(digest(body) == hashlib.sha256(canonical(body)).hexdigest(),
         "evidence closure fixture")
    return {"status": "PASS_C28_RELEASE_EVIDENCE_CLOSURE_FIXTURE"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "core-unit", "expect-core-invocation-id", "core-control-dir",
        "cold-control-dir", "release-attack-dir", "output-dir",
        "expect-builder-sha256", "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-core-pass-sha256",
        "expect-cold-receipt-file-sha256",
        "expect-cold-receipt-object-sha256",
        "expect-release-attack-file-sha256",
        "expect-release-attack-object-sha256",
    ):
        value.add_argument("--" + name)
    value.add_argument("--evidence-root", action="append")
    return value


def main() -> int:
    args = parser().parse_args()
    fields = (
        "core_unit", "expect_core_invocation_id", "core_control_dir",
        "cold_control_dir", "release_attack_dir", "output_dir",
        "expect_builder_sha256", "expect_core_receipt_file_sha256",
        "expect_core_receipt_object_sha256", "expect_core_pass_sha256",
        "expect_cold_receipt_file_sha256",
        "expect_cold_receipt_object_sha256",
        "expect_release_attack_file_sha256",
        "expect_release_attack_object_sha256",
    )
    try:
        if args.self_test:
            need(not args.preflight_only and args.evidence_root is None
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(args.evidence_root is not None
                 and all(getattr(args, field) is not None for field in fields),
                 "all run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "status": result["status"],
        }) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
