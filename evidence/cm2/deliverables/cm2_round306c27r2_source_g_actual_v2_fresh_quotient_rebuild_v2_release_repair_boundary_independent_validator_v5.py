#!/usr/bin/env python3
"""Independent fail-closed C27R2 release-repair boundary validator.

This append-only validator consumes the already completed C27R2 core as a
read-only contract.  It does not import or execute the producer, verifier,
attack harness, cold helper, evidence builder, or any release/seal program.

Formal mode requires an exactly empty, file/object-pinned override map.
Private-fixture mode requires exactly one allowlisted logical path mapped to
``CASE_ROOT/override``.  Both modes traverse the same validation path.  Every
opened authority is O_NOFOLLOW, regular, single-link, current-byte hashed and
checked with a full nine-field stat fingerprint before and after use.
"""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / ".cm2-runtime/audit"
SELF = Path(__file__).resolve()
PREFIX = "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
OVERRIDE_SCHEMA = PREFIX + "release-repair-boundary-override-map.v5"
OUTPUT_SCHEMA = PREFIX + "release-boundary-validator.v5"
FORMAL_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_BOUNDARY_V5_FORMAL_EMPTY_OVERRIDE_EXACT_"
    "SPEC_ATTESTATION_INPUT_SET_FIXED_USER_BUS_SERVICE_QUERY_CURRENT_PROCESS_"
    "INVENTORY_AND_AUTHORITY_CLOSURE__ZERO_CREDIT"
)
PRIVATE_STATUS = (
    "PASS_C27R2_RELEASE_REPAIR_BOUNDARY_V5_PRIVATE_SINGLE_OVERRIDE_EXACT_"
    "SPEC_ATTESTATION_INPUT_SET_FIXED_USER_BUS_SERVICE_QUERY_CURRENT_PROCESS_"
    "INVENTORY_AND_AUTHORITY_CLOSURE__ZERO_CREDIT"
)

SYSTEMCTL = Path("/usr/bin/systemctl")
SYSTEMCTL_SHA256 = (
    "7ba82b5ba146759c710e1b80fadaa3fdbc0f9b85c8fb2c8c3196b7b1a0037ef8"
)
SERVICE_UID = 1000
SERVICE_RUNTIME = Path("/run/user/1000")
SERVICE_BUS = SERVICE_RUNTIME / "bus"
CONTROL_BUS_ENV = {
    "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
    "XDG_RUNTIME_DIR": "/run/user/1000",
    "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
}

CORE_SCHEMA = PREFIX + "gated-dual-seed-transaction-receipt.v4"
CORE_STATUS = (
    "PASS_GATE_SEED1_FOUR_FILE_CANDIDATE_SEED2_NO_IMPORT_REPLAY_AND_21_"
    "ATTACKS__ZERO_CREDIT_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
)
PINSET_SCHEMA = PREFIX + "gated-transaction-pinset.v4"
SPEC_SCHEMA = PREFIX + "process-command-spec.v4"
RUN_SCHEMA = PREFIX + "process-run-attestation.v4"
RUN_STATUS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
RESULT_SCHEMA = PREFIX + "producer-result.v1"
RESULT_STATUS = (
    "PASS_FRESH_ACTUAL_V2_SEED1_QUOTIENT_REBUILD_ZERO_CREDIT__PENDING_"
    "NO_IMPORT_SEED2_VERIFICATION_ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL"
)
VERIFICATION_SCHEMA = PREFIX + "independent-verification.v1"
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_ACTUAL_V2_SEED2_INDEPENDENT_QUOTIENT_AND_BYTE_EXACT_"
    "CANDIDATE_REPLAY__ZERO_CREDIT_PENDING_ATTACKS_COLD_REPLAY_AND_"
    "TERMINAL_SEAL"
)
ATTACK_SCHEMA = PREFIX + "coherent-attack-harness.v1"
ATTACK_STATUS = (
    "PASS_BASELINE_AND_21_OF_21_COHERENT_ATTACKS_REJECTED_FAIL_CLOSED__"
    "ZERO_CREDIT_PENDING_RELEASE_CHAIN"
)
COLD_SCHEMA = "cm2.round306c27r2.source-g-authority-v2.release-cold-replay-receipt.v4"
COLD_STATUS = (
    "PASS_FRESH_NO_IMPORT_SEED2_COLD_BYTE_REPLAY_WITH_FIXED_CONTROL_BUS_AND_"
    "ALL_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT"
)
COLD_HELPER_PATH = (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_cold_replay_runner_v4.py"
)
COLD_HELPER_SHA256 = (
    "3d44ebbc37449192f975e3687284c6e74285f7d7f564e40ef12e37232f0ec838"
)
COLD_INPUT_PATHS_SHA256 = (
    "fe01c7fd4eabdfd992f6528938e8d624578dc5618c6440c4aae082c828cbee2c"
)
COLD_ROLE_MAP_SHA256 = (
    "f4673ac89907f9fae4b90df5ffe77036235329b9a8d6317751fd37ca8d9d76ed"
)
COLD_ATTESTED_PATH_SEQUENCE_SHA256 = (
    "623cfb0a624152b2523948d86542d267b6e25ebdb185d1080b13de3468372bbf"
)
EVIDENCE_SCHEMA = "cm2.round306c27r2.source-g-authority-v2.release-evidence-bundle.v1"
EVIDENCE_STATUS = (
    "PASS_EXACT_V6_FORMAL_R2_CORE_SERVICE_RECEIPT_CANDIDATE_DUAL_VERIFIER_"
    "21_ATTACKS_AND_PROCESS_CLOSURE__ZERO_CREDIT"
)
ACTUAL_TERMINAL_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-"
    "seed-terminal-receipt.v1"
)
ACTUAL_TERMINAL_STATUS = (
    "PASS_ACTUAL_V2_TWO_REAL_SEEDS_INDEPENDENT_REPLAY_24_ATTACKS_COLD_"
    "REPLAY_TERMINAL_SEAL__ZERO_CREDIT"
)
ACTUAL_REPLAY_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-"
    "seed-terminal-replay.v1"
)
ACTUAL_REPLAY_STATUS = (
    "PASS_COLD_ROOT_PAYLOAD_CURRENT_SHA_STAT_NATIVE_DUAL_SEED_INDEPENDENT_"
    "REPLAY_AND_24_ATTACKS__ZERO_CREDIT"
)
ACTUAL_BASE_SCHEMA = (
    "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-"
    "seed-zero-credit-seal.v1"
)
GATE_SCHEMA = "cm2.round306c27r2.post-actual-v2-rebuild-gate.v3"
GATE_STATUS = (
    "PASS_EXACT_ACTUAL_V2_DUAL_SEED_TERMINAL_SERVICE_RECEIPT_ROOT_PAYLOAD_"
    "AND_PASS_LOCK__FRESH_C27R2_REBUILD_MAY_BEGIN__ZERO_CREDIT"
)
GATE_ROOT_SCHEMA = "cm2.round306c27r2.post-actual-v2-rebuild-gate-execution-r2.v3"
GATE_ROOT_STATUS = (
    "PASS_HARDENED_R2_GATE_PRODUCER_INDEPENDENT_VERIFIER_AND_16_COHERENT_"
    "ATTACKS__FRESH_C27R2_REBUILD_MAY_BEGIN__ZERO_CREDIT"
)

EMPTY_SHA = hashlib.sha256(b"").hexdigest()
ACTUAL_PASS = b"PASS_ACTUAL_V2_DUAL_SEED_TERMINAL_ZERO_CREDIT_SEAL\n"
CORE_PASS = b"PASS_C27R2_AUTHORITY_V2_GATED_DUAL_SEED_CORE__ZERO_CREDIT\n"
COLD_PASS = (
    b"PASS_C27R2_RELEASE_COLD_REPLAY_V4_FIXED_CONTROL_BUS__ZERO_CREDIT\n"
)
GATE_PASS = (
    b"PASS_HARDENED_R2_POST_ACTUAL_V2_C27R2_REBUILD_GATE_V3__FRESH_REBUILD_"
    b"MAY_BEGIN__ZERO_CREDIT\n"
)
EXPECTED_CENSUS = {
    "cross_post_component_member_pairs": 125_561_998_198,
    "cycle_edges": 668,
    "frozen_C15_components": 57_876,
    "frozen_C15_members": 502_204,
    "post_C27R2_components": 43_684,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
}
SOURCE_PINS = {
    "producer": "578d0ce0d39d14dede9d9528be383abb3d4140c26bcac75917fe860a98bb158b",
    "independent_verifier": "acc66bbff3717e16bf56b15f9498070d97a4be1b0cd9253a79b7cae598b4082f",
    "coherent_attack_harness": "1d501ca968853712743524e7aba16d29dadd62b9d46458b53e0421aef2072007",
    "transaction_runner": "7ce75edac7e1aad904718e173cf6ed178f6d2631ba1f5cb4253bcf2c1e121d63",
    "gated_watcher": "68c1d70ca55e4d17f1b727a6b1eda8343c1a6eaecd61df43ed5449198a88331d",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
SOURCE_PATHS = {
    "producer": "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_producer_v4.py",
    "independent_verifier": "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_independent_verifier_v4.py",
    "coherent_attack_harness": "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_coherent_attack_harness_v4.py",
    "transaction_runner": "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_transaction_runner_v4.py",
    "gated_watcher": "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_gated_dual_seed_watcher_v6.py",
}
GATE_SOURCE_PINS = {
    "producer": "aab253ba102dc5f168ff96089145ea8a23a3f4ff8255dad92d668430c93c82f8",
    "independent_verifier": "3a1aac7d79ce095226f310fdca0ac2614ee7d3a90e17d3fe69638b56b06dfe81",
    "coherent_attack_harness": "4e6c1b3c1befd08d6ad64c9f84728df309424ded28406740b39f95f6575657fb",
    "python": SOURCE_PINS["python"],
}
GATE_SOURCE_PATHS = {
    "producer": "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3.py",
    "independent_verifier": "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3_independent_verifier_r2.py",
    "coherent_attack_harness": "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3_coherent_attack_harness_r2.py",
}
CANDIDATE_FILES = {
    "member_to_post_component.jsonl.gz",
    "old_c15_component_to_post_component.jsonl.gz",
    "post_component_census.jsonl.gz",
    "result.json",
}
RUN_FILES = {
    "PASS.lock", "exit_code.txt", "input_post.json", "input_pre.json",
    "output_validation.json", "run_attestation.json", "runner_start.json",
    "signal.json", "stderr.log", "stdout.log", "timing.json",
}
CORE_CONTROL_FILES = {
    "PASS.lock", "attack_command_spec.json", "candidate_validation.json",
    "coherent_attacks_runner.exit_code.txt",
    "coherent_attacks_runner.stderr.log",
    "coherent_attacks_runner.stdout.log",
    "dual_seed_descriptor_agreement.json",
    "independent_verifier_runner.exit_code.txt",
    "independent_verifier_runner.stderr.log",
    "independent_verifier_runner.stdout.log", "pinset.json",
    "preflight.json", "producer_command_spec.json",
    "producer_runner.exit_code.txt", "producer_runner.stderr.log",
    "producer_runner.stdout.log", "transaction_receipt.json",
    "verifier_command_spec.json",
}
GATE_FILES = {
    "PASS.lock", "gate_receipt.json", "execution_receipt.json",
    "coherent_attacks.json", "independent_verification.json",
    "producer.exit_code.txt", "producer.stderr.log", "producer.stdout.log",
    "independent_verifier.exit_code.txt",
    "independent_verifier.stderr.log",
    "independent_verifier.stdout.log",
    "coherent_attacks.exit_code.txt", "coherent_attacks.stderr.log",
    "coherent_attacks.stdout.log",
}
COLD_CONTROL_FILES = {
    "PASS.lock", "cold_command_spec.json", "cold_replay_receipt.json",
    "pinset.json", "runner.exit_code.txt", "runner.stderr.log",
    "runner.stdout.log",
}
TERMINAL_FILES = {
    "PASS.lock", "payload_manifest.sha256", "root_manifest.sha256",
    "terminal_receipt.json", "terminal_replay.json",
}
BASE_FILES = {"payload", "payload_manifest.sha256", "receipt.json", "root_manifest.sha256"}
BASE_COLD_INPUT_FILES = {
    "payload_manifest.sha256", "receipt.json", "root_manifest.sha256",
    "payload/coherent_attacks.json", "payload/independent_verification.json",
    "payload/inventory.json",
}
CORE_ATTACK_NAMES = (
    "missing-result", "extra-inventory", "result-noncanonical",
    "result-duplicate-key", "result-stale-closure",
    "coherent-formal-credit", "coherent-manifest-authorized",
    "coherent-status-lie", "coherent-census-lie",
    "coherent-dsu-root-id-formula", "coherent-seed-label-swap",
    "coherent-ledger-sha-lie", "result-symlink", "old-map-hardlink",
    "old-map-truncated-gzip", "member-map-bad-gzip",
    "post-census-empty-gzip", "wrong-terminal-root-pin",
    "wrong-terminal-file-pin", "wrong-terminal-object-pin",
    "terminal-base-directory-swap",
)
ATTACK_WORK_FILES = sorted({
    "baseline_verification.json", "coherent_attacks.json",
    *{f"candidate-clone/{name}" for name in CANDIDATE_FILES},
    *{f"transcripts/attack-{index:02d}-{name}.{suffix}"
      for index, name in enumerate(CORE_ATTACK_NAMES)
      for suffix in ("exit_code.txt", "stderr", "stdout")},
    *{f"transcripts/baseline.{suffix}"
      for suffix in ("exit_code.txt", "stderr", "stdout")},
})
STAGES = {
    "producer": ("producer_command_spec.json", "producer_run", "producer", "30662721"),
    "independent_verifier": ("verifier_command_spec.json", "verifier_run", "independent_verifier", "30662722"),
    "coherent_attacks": ("attack_command_spec.json", "attack_run", "coherent_attack_harness", "30662723"),
}


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def strict(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          Rejected("non-finite JSON:" + token)))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid)


def logical_name(raw: str | Path) -> str:
    path = Path(raw)
    if path.is_absolute():
        try:
            path = path.relative_to(ROOT)
        except ValueError as error:
            raise Rejected("logical path outside workspace") from error
    name = str(path)
    need(name != "" and not path.is_absolute() and str(Path(name)) == name
         and all(part not in {"", ".", ".."} for part in path.parts),
         "canonical logical path")
    return name


def no_symlink_chain(path: Path, anchor: Path) -> None:
    absolute = path.absolute()
    base = anchor.absolute()
    need(absolute.is_relative_to(base), "path confined to anchor")
    need(base.exists() and base.is_dir() and not base.is_symlink(),
         "real anchor directory")
    current = base
    for part in absolute.relative_to(base).parts:
        current = current / part
        if current.exists() or current.is_symlink():
            need(not current.is_symlink(), "no symlink in path chain")


def capture_direct(path: Path, anchor: Path,
                   maximum: int = 16 << 30) -> tuple[bytes, dict[str, Any]]:
    path = path.absolute()
    no_symlink_chain(path, anchor)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 <= before.st_size <= maximum, "singleton regular file")
        state = hashlib.sha256()
        chunks: list[bytes] = []
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    need(fingerprint(before) == fingerprint(after) == fingerprint(current),
         "FD/path full nine-stat identity")
    payload = b"".join(chunks)
    return payload, {"sha256": state.hexdigest(), "size": len(payload),
                     "stat_fingerprint": list(fingerprint(before))}


def decode_document(payload: bytes, closure: str) -> dict[str, Any]:
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "canonical document newline")
    value = strict(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON document")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "JSON object closure")
    return value


class Resolver:
    def __init__(self, override_logical: str | None,
                 override_physical: Path | None, case_root: Path | None,
                 barrier: bool = False):
        self.override_logical = override_logical
        self.override_physical = override_physical
        self.case_root = case_root
        self.barrier = barrier
        self.barrier_used = False
        self.override_used = False
        self.records: dict[str, dict[str, Any]] = {}

    def resolve(self, raw: str | Path) -> tuple[str, Path, Path]:
        logical = logical_name(raw)
        if self.override_logical is not None and (
                logical == self.override_logical
                or logical.startswith(self.override_logical + "/")):
            need(self.override_physical is not None and self.case_root is not None,
                 "private override configured")
            suffix = Path(logical).relative_to(self.override_logical)
            self.override_used = True
            return logical, self.override_physical / suffix, self.case_root
        return logical, ROOT / logical, ROOT

    def capture(self, raw: str | Path, maximum: int = 16 << 30) \
            -> tuple[bytes, dict[str, Any]]:
        logical, path, anchor = self.resolve(raw)
        payload, record = capture_direct(path, anchor, maximum)
        if self.barrier and not self.barrier_used and logical == self.override_logical:
            need(self.case_root is not None, "barrier case root")
            self.barrier_used = True
            (self.case_root / "fd-opened.lock").write_bytes(b"OPENED\n")
            deadline = time.monotonic() + 30
            while not (self.case_root / "continue.lock").exists():
                need(time.monotonic() < deadline, "fixture barrier timeout")
                time.sleep(0.01)
            current = os.stat(path, follow_symlinks=False)
            need(list(fingerprint(current)) == record["stat_fingerprint"],
                 "barrier current full nine-stat identity")
        current_record = {"path": logical, **record}
        prior = self.records.setdefault(logical, current_record)
        need(prior == current_record, "repeated logical capture identity")
        return payload, current_record

    def document(self, raw: str | Path, closure: str) -> dict[str, Any]:
        return decode_document(self.capture(raw, 512 << 20)[0], closure)

    def plain(self, raw: str | Path) -> Any:
        payload, _ = self.capture(raw, 512 << 20)
        need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
             "plain JSON newline")
        value = strict(payload[:-1])
        need(canonical(value) == payload[:-1], "canonical plain JSON")
        return value

    def directory(self, raw: str | Path, expected: set[str] | None = None) \
            -> tuple[str, Path]:
        logical, path, anchor = self.resolve(raw)
        no_symlink_chain(path, anchor)
        need(path.is_dir() and not path.is_symlink(), "real directory")
        if expected is not None:
            need({entry.name for entry in path.iterdir()} == expected,
                 "exact directory inventory:" + logical)
        return logical, path

    def snapshot(self, raw: str | Path,
                 exact: list[str] | None = None) -> dict[str, Any]:
        logical, path = self.directory(raw)
        files: list[str] = []
        directories = 0
        for current, names, filenames in os.walk(path):
            base = Path(current)
            for name in names:
                need(not (base / name).is_symlink(), "no symlink directory")
                directories += 1
            for name in filenames:
                member = base / name
                need(member.is_file() and not member.is_symlink(),
                     "regular directory member")
                files.append(str(member.relative_to(path)))
        files.sort()
        if exact is not None:
            need(files == exact, "exact recursive inventory")
        records = [self.capture(str(Path(logical) / name))[1] for name in files]
        return {"kind": "directory", "directory_count": directories,
                "relative_file_inventory": files, "files": records}

    def verify_current(self) -> str:
        rows: list[dict[str, Any]] = []
        for logical, expected in sorted(self.records.items()):
            _, path, anchor = self.resolve(logical)
            _, current = capture_direct(path, anchor)
            need(current == {key: expected[key] for key in
                              ("sha256", "size", "stat_fingerprint")},
                 "authority post current SHA/full9stat")
            rows.append(expected)
        return hashlib.sha256(b"".join(canonical(row) + b"\n"
                                       for row in rows)).hexdigest()


def parse_manifest(resolver: Resolver, raw: str | Path,
                   members_relative_to_manifest: bool = False) -> dict[str, str]:
    payload, _ = resolver.capture(raw, 64 << 20)
    need(payload.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    claimed_names: list[str] = []
    manifest_parent = Path(logical_name(raw)).parent
    for line in payload.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None and match.group(2) not in result,
             "manifest row syntax/uniqueness")
        claimed = match.group(2)
        claimed_names.append(claimed)
        logical = logical_name(manifest_parent / claimed
            if members_relative_to_manifest else claimed)
        need((not members_relative_to_manifest and logical == claimed)
             or (members_relative_to_manifest
                 and str(Path(claimed)) == claimed
                 and all(part not in {"", ".", ".."}
                         for part in Path(claimed).parts)),
             "manifest canonical path")
        result[logical] = match.group(1)
    need(claimed_names == sorted(claimed_names), "manifest sorted")
    for logical, expected in result.items():
        need(resolver.capture(logical)[1]["sha256"] == expected,
             "manifest current member")
    return result


def sha_record_matches(value: Any, current: dict[str, Any]) -> bool:
    return (type(value) is dict and value.get("path") == current["path"]
            and value.get("sha256") == current["sha256"]
            and value.get("size") == current["size"]
            and value.get("stat_fingerprint") == current["stat_fingerprint"])


def state_zero(value: dict[str, Any], expected_c27: str | None = None) -> bool:
    return (value.get("formal_credit") == 0
            and value.get("manifest_authorized") is False
            and value.get("CM2") == "NO-GO_FOR_CLAIM"
            and (expected_c27 is None or value.get("C27R2") == expected_c27))


def validate_environment(args: argparse.Namespace) -> None:
    python = Path(args.python).absolute()
    need(Path(sys.executable).absolute() == python
         and sys.flags.isolated == 1 and sys.dont_write_bytecode,
         "workspace Python invoked with -I -B")
    need(valid_sha(args.expect_python_sha256)
         and capture_direct(python, python.parent)[1]["sha256"]
             == args.expect_python_sha256 == SOURCE_PINS["python"],
         "workspace Python current SHA pin")
    need(valid_sha(args.expect_validator_sha256)
         and capture_direct(SELF, ROOT)[1]["sha256"]
             == args.expect_validator_sha256,
         "validator self SHA pin")
    expected = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                "PYTHONHASHSEED": args.expected_python_hash_seed}
    observed = dict(os.environ)
    need(observed == expected, "exact process environment")
    need(args.service_query_fixture in {"fixed", "missing", "wrong"}
         and (args.mode == "private" or args.service_query_fixture == "fixed"),
         "formal fixed/private injected service-query route")


def allowed_overrides(args: argparse.Namespace) -> set[str]:
    top = {
        logical_name(args.actual_terminal_relative),
        logical_name(args.actual_base_relative),
        logical_name(args.gate_relative),
        logical_name(args.core_control_relative),
        logical_name(args.candidate_relative),
        logical_name(args.verifier_output_relative),
        logical_name(args.attack_work_relative),
        logical_name(args.producer_run_relative),
        logical_name(args.verifier_run_relative),
        logical_name(args.attack_run_relative),
        logical_name(args.cold_control_relative),
        logical_name(args.cold_output_relative),
        logical_name(args.cold_run_relative),
        logical_name(args.evidence_relative),
        logical_name(args.seed1_edge_relative),
        logical_name(args.seed2_edge_relative),
        logical_name(args.frozen_c15_relative),
        logical_name(args.future_outer_relative),
        logical_name(args.future_seal_relative),
        logical_name(args.future_terminal_relative),
    }
    children: set[str] = set()
    for directory, names in (
        (args.actual_terminal_relative, TERMINAL_FILES),
        (args.actual_base_relative, BASE_FILES),
        (args.candidate_relative, CANDIDATE_FILES),
        (args.verifier_output_relative, {"verification.json"}),
        (args.producer_run_relative, RUN_FILES),
        (args.verifier_run_relative, RUN_FILES),
        (args.attack_run_relative, RUN_FILES),
        (args.cold_run_relative, RUN_FILES),
        (args.cold_output_relative, {"verification.json"}),
        (args.evidence_relative, {"core_inventory.sha256", "evidence_bundle.json"}),
    ):
        base = Path(logical_name(directory))
        children |= {str(base / name) for name in names}
    control = Path(logical_name(args.core_control_relative))
    children |= {str(control / name) for name in CORE_CONTROL_FILES}
    gate = Path(logical_name(args.gate_relative))
    children |= {str(gate / name) for name in GATE_FILES}
    cold = Path(logical_name(args.cold_control_relative))
    children |= {str(cold / name) for name in COLD_CONTROL_FILES}
    return top | children


def load_override(args: argparse.Namespace) \
        -> tuple[str | None, Path | None, Path | None, dict[str, Any]]:
    path = Path(args.override_map).absolute()
    payload, record = capture_direct(path, path.parent, 4 << 20)
    need(record["sha256"] == args.expect_override_map_file_sha256,
         "override map file pin")
    value = decode_document(payload, "override_map_sha256")
    need(value.get("schema") == OVERRIDE_SCHEMA
         and value.get("mode") == args.mode
         and state_zero(value, "UNAUTHORIZED")
         and value.get("entries") is not None
         and value["override_map_sha256"] == args.expect_override_map_object_sha256,
         "override map schema/state/object pin")
    entries = value["entries"]
    need(type(entries) is list, "override entries list")
    if args.mode == "formal":
        need(entries == [] and args.case_root is None
             and not args.fixture_barrier, "formal exact empty override")
        return None, None, None, value
    need(len(entries) == 1 and args.case_root is not None,
         "private exact one override")
    case_root = Path(args.case_root).absolute()
    need(case_root.is_dir() and not case_root.is_symlink()
         and case_root.is_relative_to(AUDIT)
         and case_root.name.startswith("private-c27r2-release-fixture-"),
         "private allowlisted case root")
    entry = entries[0]
    need(type(entry) is dict and set(entry) == {"logical_path", "physical_path"},
         "exact override entry shape")
    logical = logical_name(entry["logical_path"])
    physical = Path(entry["physical_path"]).absolute()
    need(logical in allowed_overrides(args)
         and physical == case_root / "override",
         "one allowlisted logical to exact case-root override")
    return logical, physical, case_root, value


def validate_actual(resolver: Resolver, args: argparse.Namespace) \
        -> dict[str, Any]:
    terminal = logical_name(args.actual_terminal_relative)
    base = logical_name(args.actual_base_relative)
    resolver.directory(terminal, TERMINAL_FILES)
    resolver.directory(base, BASE_FILES)
    terminal_root_path = str(Path(terminal) / "root_manifest.sha256")
    terminal_receipt_path = str(Path(terminal) / "terminal_receipt.json")
    terminal_replay_path = str(Path(terminal) / "terminal_replay.json")
    terminal_root_record = resolver.capture(terminal_root_path)[1]
    terminal_receipt_record = resolver.capture(terminal_receipt_path)[1]
    terminal_receipt = resolver.document(terminal_receipt_path,
                                         "terminal_receipt_sha256")
    terminal_replay = resolver.document(terminal_replay_path, "result_sha256")
    need(terminal_root_record["sha256"] == args.expect_actual_terminal_root_sha256
         and terminal_receipt_record["sha256"]
             == args.expect_actual_terminal_receipt_file_sha256
         and terminal_receipt["terminal_receipt_sha256"]
             == args.expect_actual_terminal_receipt_object_sha256,
         "dynamic actual terminal CLI three-pin closure")
    need(terminal_receipt.get("schema") == ACTUAL_TERMINAL_SCHEMA
         and terminal_receipt.get("status") == ACTUAL_TERMINAL_STATUS
         and terminal_receipt.get("actual_v2_terminal_seal_passed") is True
         and terminal_receipt.get("execution_seeds") == [30660101, 30660991]
         and terminal_receipt.get("exact_census", {}).get(
             "fresh_DSU_final_component_total") == 43_684
         and terminal_receipt.get("exact_census", {}).get(
             "full_component_edge_union_total") == 14_860
         and terminal_receipt.get("formal_credit") == 0
         and terminal_receipt.get("manifest_authorized") is False
         and terminal_receipt.get("CM2") == "NO-GO_FOR_CLAIM",
         "actual terminal receipt semantics")
    need(terminal_replay.get("schema") == ACTUAL_REPLAY_SCHEMA
         and terminal_replay.get("status") == ACTUAL_REPLAY_STATUS
         and terminal_replay.get("execution_seeds") == [30660101, 30660991]
         and terminal_replay.get("formal_credit") == 0
         and terminal_replay.get("manifest_authorized") is False
         and terminal_replay.get("CM2") == "NO-GO_FOR_CLAIM"
         and resolver.capture(str(Path(terminal) / "PASS.lock"))[0]
             == ACTUAL_PASS,
         "actual terminal replay/PASS semantics")
    terminal_payload = parse_manifest(
        resolver, str(Path(terminal) / "payload_manifest.sha256"))
    terminal_root = parse_manifest(resolver, terminal_root_path, True)
    need(len(terminal_payload) == 12
         and terminal_receipt["terminal_payload_manifest"] == {
             "entry_count": 12,
             "file_sha256": resolver.capture(
                 str(Path(terminal) / "payload_manifest.sha256"))[1]["sha256"]}
         and terminal_root == {
             str(Path(terminal) / "payload_manifest.sha256"):
                 resolver.capture(str(Path(terminal) / "payload_manifest.sha256"))[1]["sha256"],
             str(Path(terminal) / "terminal_receipt.json"):
                 terminal_receipt_record["sha256"]},
         "actual terminal manifest closure")
    base_receipt_path = str(Path(base) / "receipt.json")
    base_receipt = resolver.document(base_receipt_path, "receipt_sha256")
    need(base_receipt.get("schema") == ACTUAL_BASE_SCHEMA
         and base_receipt.get("formal_credit") == 0
         and base_receipt.get("manifest_authorized") is False
         and base_receipt.get("CM2") == "NO-GO_FOR_CLAIM",
         "actual base receipt state")
    base_payload = parse_manifest(resolver, str(Path(base) / "payload_manifest.sha256"))
    base_root = parse_manifest(resolver,
                               str(Path(base) / "root_manifest.sha256"), True)
    need(len(base_payload) == 56 and base_root == {
        str(Path(base) / "payload_manifest.sha256"):
            resolver.capture(str(Path(base) / "payload_manifest.sha256"))[1]["sha256"],
        str(Path(base) / "receipt.json"):
            resolver.capture(base_receipt_path)[1]["sha256"]},
        "actual base manifest closure")
    claimed_base = terminal_receipt.get("base_seal")
    need(type(claimed_base) is dict
         and claimed_base.get("payload_manifest_file_sha256")
             == resolver.capture(str(Path(base) / "payload_manifest.sha256"))[1]["sha256"]
         and claimed_base.get("receipt_file_sha256")
             == resolver.capture(base_receipt_path)[1]["sha256"]
         and claimed_base.get("receipt_object_sha256") == base_receipt["receipt_sha256"]
         and claimed_base.get("root_manifest_file_sha256")
             == resolver.capture(str(Path(base) / "root_manifest.sha256"))[1]["sha256"],
         "terminal to base seal closure")
    return {"terminal_root": terminal_root_record["sha256"],
            "terminal_receipt_file": terminal_receipt_record["sha256"],
            "terminal_receipt_object": terminal_receipt["terminal_receipt_sha256"],
            "terminal_replay_object": terminal_replay["result_sha256"],
            "base_receipt_object": base_receipt["receipt_sha256"]}


def validate_gate(resolver: Resolver, args: argparse.Namespace) -> dict[str, Any]:
    gate = logical_name(args.gate_relative)
    resolver.directory(gate, GATE_FILES)
    receipt_path = str(Path(gate) / "gate_receipt.json")
    root_path = str(Path(gate) / "execution_receipt.json")
    receipt_record = resolver.capture(receipt_path)[1]
    root_record = resolver.capture(root_path)[1]
    receipt = resolver.document(receipt_path, "gate_receipt_sha256")
    root_receipt = resolver.document(root_path, "execution_receipt_sha256")
    need(receipt_record["sha256"] == args.expect_gate_receipt_file_sha256
         and receipt["gate_receipt_sha256"] == args.expect_gate_receipt_object_sha256
         and root_record["sha256"] == args.expect_gate_root_file_sha256
         and root_receipt["execution_receipt_sha256"]
             == args.expect_gate_root_object_sha256,
         "post-actual gate four pins")
    need(receipt.get("schema") == GATE_SCHEMA
         and receipt.get("status") == GATE_STATUS
         and receipt.get("fresh_C27R2_rebuild_may_start") is True
         and receipt.get("formal_credit") == 0
         and receipt.get("manifest_authorized") is False
         and receipt.get("C27R2")
             == "PREFLIGHT_GATE_PASS_ONLY__NOT_REBUILT_NOT_CREDITED"
         and receipt.get("C28") == "UNAUTHORIZED"
         and receipt.get("C29") == "UNAUTHORIZED"
         and receipt.get("CM2") == "NO-GO_FOR_CLAIM",
         "post-actual gate receipt semantics")
    need(root_receipt.get("schema") == GATE_ROOT_SCHEMA
         and root_receipt.get("status") == GATE_ROOT_STATUS
         and root_receipt.get("source_pins") == GATE_SOURCE_PINS
         and root_receipt.get("gate_receipt_file_sha256") == receipt_record["sha256"]
         and root_receipt.get("gate_receipt_object_sha256")
             == receipt["gate_receipt_sha256"]
         and root_receipt.get("stage_total") == 3
         and root_receipt.get("formal_credit") == 0
         and root_receipt.get("manifest_authorized") is False
         and root_receipt.get("C27R2")
             == "PREFLIGHT_GATE_PASS_ONLY__NOT_REBUILT_NOT_CREDITED"
         and root_receipt.get("CM2") == "NO-GO_FOR_CLAIM"
         and resolver.capture(str(Path(gate) / "PASS.lock"))[0] == GATE_PASS,
         "post-actual root/source/process/PASS closure")
    stages = root_receipt.get("stages")
    need(type(stages) is list
         and [row.get("name") for row in stages]
             == ["producer", "independent_verifier", "coherent_attacks"],
         "post-actual gate exact stage order")
    for row in stages:
        name = row["name"]
        stdout = resolver.capture(str(Path(gate) / f"{name}.stdout.log"))[0]
        stderr = resolver.capture(str(Path(gate) / f"{name}.stderr.log"))[0]
        exit_code = resolver.capture(
            str(Path(gate) / f"{name}.exit_code.txt"))[0]
        need(exit_code == b"0\n" and stderr == b""
             and stdout.endswith(b"\n") and not stdout.endswith(b"\n\n")
             and hashlib.sha256(stdout).hexdigest() == row.get("stdout_sha256")
             and hashlib.sha256(stderr).hexdigest() == row.get("stderr_sha256")
             and row.get("expected_exit_code") == 0
             and row.get("observed_exit_code") == 0
             and row.get("stderr_empty") is True
             and type(strict(stdout[:-1])) is dict
             and canonical(strict(stdout[:-1])) == stdout[:-1],
             "post-actual gate current exact transcript:" + name)
    need(all(resolver.capture(path)[1]["sha256"] == GATE_SOURCE_PINS[name]
             for name, path in GATE_SOURCE_PATHS.items()),
         "post-actual gate source pins current")
    return {"gate_receipt_file": receipt_record["sha256"],
            "gate_receipt_object": receipt["gate_receipt_sha256"],
            "gate_root_file": root_record["sha256"],
            "gate_root_object": root_receipt["execution_receipt_sha256"]}


def arg_after(argv: list[Any], name: str) -> str:
    need(all(type(item) is str for item in argv) and argv.count(name) == 1,
         "command exact argument:" + name)
    index = argv.index(name)
    need(index + 1 < len(argv), "command argument value:" + name)
    return argv[index + 1]


def validate_historical_current(resolver: Resolver, value: Any, label: str,
                                expected_inputs: list[str], spec_path: str,
                                pinset_path: str) -> None:
    expected_inputs = [logical_name(path) for path in expected_inputs]
    need(expected_inputs == sorted(set(expected_inputs)),
         label + ":canonical exact expected inputs")
    expected_labels = ({"command-spec", "pinset"}
        | {f"declared-input-{index:03d}"
           for index in range(len(expected_inputs))})
    need(type(value) is dict and set(value) == expected_labels,
         label + ":exact historical input labels")
    expected_paths = [logical_name(spec_path), logical_name(pinset_path),
                      *expected_inputs]
    observed_paths = [value["command-spec"].get("path"),
                      value["pinset"].get("path"),
                      *[value[f"declared-input-{index:03d}"].get("path")
                        for index in range(len(expected_inputs))]]
    need(observed_paths == expected_paths
         and len(observed_paths) == len(set(observed_paths)),
         label + ":attestation path multiset exact spec+pinset+declared inputs")
    for record in value.values():
        need(type(record) is dict and set(record) == {
                 "path", "sha256", "size", "stat_fingerprint",
                 "O_NOFOLLOW",
                 "single_open_file_description_hash_child_fstat_and_path_identity"}
             and valid_sha(record.get("sha256"))
             and type(record.get("size")) is int
             and type(record.get("stat_fingerprint")) is list
             and len(record["stat_fingerprint"]) == 9
             and record.get("O_NOFOLLOW") is True
             and record.get(
                 "single_open_file_description_hash_child_fstat_and_path_identity")
                 is True,
             label + ":historical record shape")
        _, current = resolver.capture(record["path"])
        need(sha_record_matches(record, current),
             label + ":historical current SHA/full9stat")


def core_authority_input_paths(args: argparse.Namespace) -> list[str]:
    """Derive the historical v6 core authority set from fixed roles.

    The old pinset's optional ``authority_input_paths`` is only a redundant
    cross-check.  It is never allowed to define or enlarge this set.
    """
    terminal = Path(logical_name(args.actual_terminal_relative))
    base = Path(logical_name(args.actual_base_relative))
    gate = Path(logical_name(args.gate_relative))
    paths = [
        *[str(terminal / name) for name in (
            "PASS.lock", "payload_manifest.sha256", "root_manifest.sha256",
            "terminal_receipt.json")],
        *[str(base / name) for name in (
            "payload_manifest.sha256", "receipt.json", "root_manifest.sha256")],
        *[str(gate / name) for name in GATE_FILES],
        logical_name(args.seed1_edge_relative),
        logical_name(args.seed2_edge_relative),
        logical_name(args.frozen_c15_relative),
    ]
    result = sorted(set(paths))
    need(len(result) == 24 and all(logical_name(path) == path for path in result),
         "fixed exact 24 historical core authority inputs")
    return result


def core_expected_input_paths(pinset: dict[str, Any], control: str,
                              stage: str, args: argparse.Namespace) \
        -> list[str]:
    authority_inputs = core_authority_input_paths(args)
    authority = pinset.get("actual_v2_authority")
    declared = authority.get("authority_input_paths") \
        if type(authority) is dict else None
    need(declared is None or declared == authority_inputs,
         stage + ":optional old pinset authority list equals fixed roles")
    common = [*authority_inputs, *SOURCE_PATHS.values(),
              str(Path(control) / "preflight.json")]
    if stage == "producer":
        expected = common
    else:
        expected = [*common,
            *[str(Path(logical_name(args.candidate_relative)) / name)
              for name in CANDIDATE_FILES],
            str(Path(control) / "candidate_validation.json")]
        if stage == "coherent_attacks":
            expected.extend([
                str(Path(logical_name(args.verifier_output_relative))
                    / "verification.json"),
                str(Path(control) / "dual_seed_descriptor_agreement.json")])
    return sorted(set(logical_name(path) for path in expected))


def fixed_core_file_paths(resolver: Resolver, args: argparse.Namespace) \
        -> list[str]:
    """Capture the exact seven-directory, 128-file frozen core surface."""
    inventories: list[tuple[str, list[str], set[str]]] = [
        (logical_name(args.core_control_relative),
         sorted(CORE_CONTROL_FILES), set()),
        (logical_name(args.candidate_relative), sorted(CANDIDATE_FILES), set()),
        (logical_name(args.verifier_output_relative), ["verification.json"], set()),
        (logical_name(args.attack_work_relative), ATTACK_WORK_FILES,
         {"candidate-clone", "saved", "transcripts"}),
        (logical_name(args.producer_run_relative), sorted(RUN_FILES), set()),
        (logical_name(args.verifier_run_relative), sorted(RUN_FILES), set()),
        (logical_name(args.attack_run_relative), sorted(RUN_FILES), set()),
    ]
    result: list[str] = []
    for root, inventory, expected_directories in inventories:
        _, physical = resolver.directory(root)
        observed_directories: set[str] = set()
        for current, names, _ in os.walk(physical):
            base = Path(current)
            for name in names:
                child = base / name
                need(not child.is_symlink(), "fixed core no symlink directory")
                observed_directories.add(str(child.relative_to(physical)))
        need(observed_directories == expected_directories,
             "fixed core exact recursive directories:" + root)
        snapshot = resolver.snapshot(root, inventory)
        need(snapshot["directory_count"] == len(expected_directories),
             "fixed core recursive directory count:" + root)
        result.extend(str(Path(root) / name) for name in inventory)
    result = sorted(set(result))
    need(len(result) == 128, "fixed exact 128 frozen core files")
    return result


def cold_expected_contract(resolver: Resolver, args: argparse.Namespace) \
        -> tuple[list[str], list[dict[str, Any]]]:
    """Derive the fresh-cold-v3 input set from immutable roles/inventories."""
    terminal = Path(logical_name(args.actual_terminal_relative))
    base = Path(logical_name(args.actual_base_relative))
    gate = Path(logical_name(args.gate_relative))
    need(logical_name(args.cold_helper_relative) == COLD_HELPER_PATH
         and args.expect_cold_helper_sha256 == COLD_HELPER_SHA256,
         "frozen append-only fresh cold v3 helper path/SHA")
    for root, expected_directories, expected_files in (
        (str(terminal), set(), set(TERMINAL_FILES)),
        (str(base), {"payload"}, set(BASE_COLD_INPUT_FILES)),
        (str(gate), set(), set(GATE_FILES)),
    ):
        _, physical = resolver.directory(root)
        observed_directories: set[str] = set()
        observed_files: set[str] = set()
        for current, names, filenames in os.walk(physical):
            here = Path(current)
            for name in names:
                child = here / name
                need(not child.is_symlink(), "cold authority no symlink directory")
                observed_directories.add(str(child.relative_to(physical)))
            for name in filenames:
                child = here / name
                need(child.is_file() and not child.is_symlink(),
                     "cold authority regular file")
                observed_files.add(str(child.relative_to(physical)))
        need(observed_directories == expected_directories
             and observed_files == expected_files,
             "fresh cold v3 exact recursive authority inventory:" + root)
    core_files = fixed_core_file_paths(resolver, args)
    terminal_files = sorted(str(terminal / name) for name in TERMINAL_FILES)
    base_files = sorted(str(base / name) for name in BASE_COLD_INPUT_FILES)
    gate_files = sorted(str(gate / name) for name in GATE_FILES)
    authority_data = sorted([
        logical_name(args.seed1_edge_relative),
        logical_name(args.seed2_edge_relative),
        logical_name(args.frozen_c15_relative),
    ])
    core_sources = sorted(SOURCE_PATHS.values())
    gate_sources = sorted(GATE_SOURCE_PATHS.values())
    role_map = [
        {"role": "core_v6_frozen_transaction", "paths": core_files},
        {"role": "actual_v2_terminal", "paths": terminal_files},
        {"role": "actual_v2_base", "paths": base_files},
        {"role": "post_actual_gate", "paths": gate_files},
        {"role": "authority_data", "paths": authority_data},
        {"role": "core_sources", "paths": core_sources},
        {"role": "gate_sources", "paths": gate_sources},
        {"role": "cold_helper", "paths": [COLD_HELPER_PATH]},
    ]
    result = sorted({path for row in role_map for path in row["paths"]})
    # transaction_runner is already one of the five frozen core sources.
    paths_digest = hashlib.sha256(b"".join(
        path.encode("ascii") + b"\n" for path in result)).hexdigest()
    need(len(result) == 165
         and [len(row["paths"]) for row in role_map]
             == [128, 5, 6, 14, 3, 5, 3, 1]
         and paths_digest == COLD_INPUT_PATHS_SHA256
         and digest(role_map) == COLD_ROLE_MAP_SHA256,
         "fixed exact 165 fresh cold v3 role/path contract")
    return result, role_map


def expected_stage_contract(args: argparse.Namespace, stage: str,
                            source_key: str) \
        -> tuple[list[str], list[dict[str, Any]], str]:
    authority = [
        "--terminal-dir", str((ROOT / args.actual_terminal_relative).absolute()),
        "--base-seal-dir", str((ROOT / args.actual_base_relative).absolute()),
        "--expect-terminal-root-sha256",
        args.expect_actual_terminal_root_sha256,
        "--expect-terminal-receipt-file-sha256",
        args.expect_actual_terminal_receipt_file_sha256,
        "--expect-terminal-receipt-object-sha256",
        args.expect_actual_terminal_receipt_object_sha256,
    ]
    prefix = [args.python, "-I", "-B",
              str((ROOT / SOURCE_PATHS[source_key]).absolute()), *authority]
    if stage == "producer":
        argv = [*prefix, "--out-dir",
                str((ROOT / args.candidate_relative).absolute())]
        roots = [{"path": str((ROOT / args.candidate_relative).absolute()),
            "kind": "directory", "precondition": "ABSENT",
            "exact_inventory": sorted(CANDIDATE_FILES),
            "required_relative_files": sorted(CANDIDATE_FILES)}]
        stdout_status = RESULT_STATUS
    elif stage == "independent_verifier":
        output_file = (ROOT / args.verifier_output_relative
                       / "verification.json").absolute()
        argv = [*prefix, "--candidate-dir",
                str((ROOT / args.candidate_relative).absolute()),
                "--out-file", str(output_file)]
        roots = [{"path": str((ROOT / args.verifier_output_relative).absolute()),
            "kind": "directory", "precondition": "EXISTING_EMPTY_DIRECTORY",
            "exact_inventory": ["verification.json"],
            "required_relative_files": ["verification.json"]}]
        stdout_status = VERIFICATION_STATUS
    else:
        output_file = (ROOT / args.attack_work_relative
                       / "coherent_attacks.json").absolute()
        argv = [*prefix, "--candidate-dir",
                str((ROOT / args.candidate_relative).absolute()),
                "--work-dir", str((ROOT / args.attack_work_relative).absolute()),
                "--out-file", str(output_file),
                "--expect-verifier-sha256", SOURCE_PINS["independent_verifier"],
                "--expect-python-sha256", SOURCE_PINS["python"],
                "--expect-harness-sha256",
                SOURCE_PINS["coherent_attack_harness"]]
        roots = [{"path": str((ROOT / args.attack_work_relative).absolute()),
            "kind": "directory", "precondition": "ABSENT",
            "exact_inventory": None,
            "required_relative_files": ["baseline_verification.json",
                                        "coherent_attacks.json"]}]
        stdout_status = ATTACK_STATUS
    return argv, roots, stdout_status


def validate_run(resolver: Resolver, args: argparse.Namespace,
                 control: str, pinset: dict[str, Any], core: dict[str, Any],
                 stage: str, spec_name: str, run_key: str,
                 source_key: str, seed: str, targets: dict[str, Any]) \
        -> dict[str, Any]:
    spec_path = str(Path(control) / spec_name)
    spec_record = resolver.capture(spec_path)[1]
    spec = resolver.document(spec_path, "command_spec_sha256")
    run = logical_name(targets[run_key])
    resolver.directory(run, RUN_FILES)
    attestation_path = str(Path(run) / "run_attestation.json")
    attestation_record = resolver.capture(attestation_path)[1]
    attestation = resolver.document(attestation_path, "run_attestation_sha256")
    expected_env = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                    "PYTHONHASHSEED": seed}
    argv = spec.get("argv")
    expected_argv, expected_outputs, expected_stdout = expected_stage_contract(
        args, stage, source_key)
    input_paths = spec.get("input_paths")
    need(type(input_paths) is list and input_paths == sorted(set(input_paths)),
         stage + ":sorted unique declared inputs")
    expected_inputs = core_expected_input_paths(pinset, control, stage, args)
    need(spec.get("schema") == SPEC_SCHEMA and spec.get("stage") == stage
         and spec.get("environment") == expected_env
         and spec.get("python_hash_seed") == seed
         and argv == expected_argv
         and spec.get("output_roots") == expected_outputs
         and spec.get("expected_stdout_status") == expected_stdout
         and type(spec.get("timeout_seconds")) is int
         and 60 <= spec["timeout_seconds"] <= 86_400
         and input_paths == expected_inputs
         and spec.get("source_path")
             == str((ROOT / SOURCE_PATHS[source_key]).absolute())
         and spec.get("source_sha256") == SOURCE_PINS[source_key]
         and spec.get("runner_source_sha256") == SOURCE_PINS["transaction_runner"]
         and spec.get("python_sha256") == SOURCE_PINS["python"]
         and spec.get("pinset_file_sha256")
             == resolver.capture(str(Path(control) / "pinset.json"))[1]["sha256"]
         and spec.get("pinset_object_sha256") == pinset["pinset_sha256"]
         and spec.get("formal_credit") == 0
         and spec.get("CM2") == "NO-GO_FOR_CLAIM",
         stage + ":full exact argv/input/output/source/env/seed closure")
    need(attestation.get("schema") == RUN_SCHEMA
         and attestation.get("status") == RUN_STATUS
         and attestation.get("stage") == stage
         and attestation.get("numeric_exit_code") == 0
         and attestation.get("signal") is None
         and attestation.get("timed_out") is False
         and attestation.get("stderr_empty") is True
         and attestation.get("stderr_sha256") == EMPTY_SHA
         and attestation.get("input_pre_post_sha_stat_identical") is True
         and attestation.get("command_spec_file_sha256") == spec_record["sha256"]
         and attestation.get("command_spec_object_sha256")
             == spec["command_spec_sha256"]
         and attestation.get("pinset_object_sha256") == pinset["pinset_sha256"]
         and attestation.get("runner_source_sha256")
             == SOURCE_PINS["transaction_runner"]
         and attestation.get("stage_source_sha256") == SOURCE_PINS[source_key]
         and attestation.get("python_sha256") == SOURCE_PINS["python"]
         and state_zero(attestation, "UNAUTHORIZED_PENDING_RELEASE_CHAIN"),
         stage + ":run attestation closure")
    validate_historical_current(resolver, attestation["input_attestations"],
                                stage, expected_inputs, spec_path,
                                str(Path(control) / "pinset.json"))
    claimed = ({"producer": core["seed1"]["run_attestation_object_sha256"],
                "independent_verifier": core["seed2"]["run_attestation_object_sha256"],
                "coherent_attacks": core["coherent_attacks"]["run_attestation_object_sha256"]}
               [stage])
    need(attestation["run_attestation_sha256"] == claimed,
         stage + ":core/run object closure")
    need(resolver.capture(str(Path(run) / "exit_code.txt"))[0] == b"0\n"
         and resolver.capture(str(Path(run) / "signal.json"))[0] == b"null\n"
         and resolver.capture(str(Path(run) / "stderr.log"))[0] == b""
         and resolver.capture(str(Path(run) / "input_pre.json"))[0]
             == resolver.capture(str(Path(run) / "input_post.json"))[0]
         and resolver.plain(str(Path(run) / "input_post.json"))
             == attestation["input_attestations"]
         and resolver.plain(str(Path(run) / "output_validation.json"))
             == attestation["output_validation"],
         stage + ":process sidecars")
    expected_pass = ("PASS_C27R2_AUTHORITY_V2_" + stage.upper()
                     + "_PROCESS_TRANSACTION__ZERO_CREDIT\n").encode("ascii")
    stdout_raw = resolver.capture(str(Path(run) / "stdout.log"))[0]
    need(stdout_raw.endswith(b"\n") and not stdout_raw.endswith(b"\n\n"),
         stage + ":stdout canonical newline")
    stdout_value = strict(stdout_raw[:-1])
    need(type(stdout_value) is dict and canonical(stdout_value) == stdout_raw[:-1]
         and stdout_value == attestation.get("stdout")
         and stdout_value.get("status") == spec.get("expected_stdout_status")
         and stdout_value.get("formal_credit") == 0
         and stdout_value.get("CM2") == "NO-GO_FOR_CLAIM"
         and hashlib.sha256(stdout_raw).hexdigest()
             == attestation.get("stdout_sha256")
         and resolver.capture(str(Path(run) / "PASS.lock"))[0] == expected_pass,
         stage + ":current stdout/attestation/PASS closure")
    timing = resolver.plain(str(Path(run) / "timing.json"))
    start = resolver.plain(str(Path(run) / "runner_start.json"))
    need(timing == {"elapsed_seconds": attestation["elapsed_seconds"],
                    "timed_out": False}
         and start == {"schema": RUN_SCHEMA + ".start", "stage": stage,
            "started_at_utc": attestation["started_at_utc"],
            "runner_source_sha256": SOURCE_PINS["transaction_runner"],
            "command_spec_file_sha256": spec_record["sha256"],
            "command_spec_object_sha256": spec["command_spec_sha256"],
            "pinset_file_sha256":
                resolver.capture(str(Path(control) / "pinset.json"))[1]["sha256"],
            "pinset_object_sha256": pinset["pinset_sha256"],
            "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM"},
         stage + ":start/timing closure")
    current_outputs: dict[str, Any] = {}
    for output in spec["output_roots"]:
        output_path = logical_name(output["path"])
        if output["kind"] == "file":
            current_outputs[output["path"]] = {
                "kind": "file", "files": [resolver.capture(output_path)[1]]}
        else:
            current_outputs[output["path"]] = resolver.snapshot(
                output_path, output.get("exact_inventory"))
    need(current_outputs == attestation["output_validation"],
         stage + ":current output equals historical")
    return attestation


def validate_gzip(payload: bytes, descriptor: dict[str, Any],
                  expected_rows: int) -> str:
    need(len(payload) >= 10 and payload[:3] == b"\x1f\x8b\x08"
         and int.from_bytes(payload[4:8], "little") == 0,
         "gzip header/mtime zero")
    rows = 0
    sequence = hashlib.sha256()
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
            for raw in stream:
                need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
                     "JSONL exact newline")
                value = strict(raw[:-1])
                need(type(value) is dict and canonical(value) == raw[:-1],
                     "canonical JSONL")
                body = dict(value)
                claim = body.pop("row_sha256", None)
                need(valid_sha(claim) and claim == digest(body), "row closure")
                sequence.update(claim.encode("ascii") + b"\n")
                rows += 1
    except (gzip.BadGzipFile, EOFError, OSError) as error:
        raise Rejected("valid complete gzip") from error
    need(rows == expected_rows == descriptor.get("row_count")
         and sequence.hexdigest() == descriptor.get("row_sequence_sha256")
         and descriptor.get("canonical_jsonl") is True
         and descriptor.get("gzip_mtime") == 0,
         "gzip row/count/sequence descriptor closure")
    return sequence.hexdigest()


def validate_candidate(resolver: Resolver, args: argparse.Namespace) \
        -> dict[str, Any]:
    candidate = logical_name(args.candidate_relative)
    resolver.directory(candidate, CANDIDATE_FILES)
    result_path = str(Path(candidate) / "result.json")
    result_record = resolver.capture(result_path)[1]
    result = resolver.document(result_path, "result_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("status") == RESULT_STATUS
         and result.get("exact_census") == EXPECTED_CENSUS
         and state_zero(result,
             "UNAUTHORIZED_PENDING_INDEPENDENT_VERIFICATION_AND_TERMINAL_SEAL")
         and result.get("C28_C29") == "UNAUTHORIZED"
         and result.get("Source_W")
             == "UNCHANGED_BY_SOURCE_G_REBUILD_CANDIDATE",
         "candidate result exact state/census")
    ledgers = result.get("ledgers")
    need(type(ledgers) is dict and set(ledgers) == {
        "member_to_post_component", "old_C15_component_to_post_component",
        "post_component_census"}, "exact ledger descriptor keys")
    files = {
        "member_to_post_component": ("member_to_post_component.jsonl.gz", 502_204),
        "old_C15_component_to_post_component": (
            "old_c15_component_to_post_component.jsonl.gz", 57_876),
        "post_component_census": ("post_component_census.jsonl.gz", 43_684),
    }
    for key, (name, count) in files.items():
        payload, record = resolver.capture(str(Path(candidate) / name), 1 << 30)
        descriptor = ledgers[key]
        need(descriptor.get("filename") == name
             and descriptor.get("sha256") == record["sha256"]
             and descriptor.get("size") == record["size"],
             "ledger file descriptor:" + key)
        validate_gzip(payload, descriptor, count)
    return {"result": result, "result_record": result_record}


def service_query_environment(fixture: str) -> dict[str, str]:
    need(fixture in {"fixed", "missing", "wrong"},
         "service query fixture mode")
    result = dict(CONTROL_BUS_ENV)
    if fixture == "missing":
        result.pop("XDG_RUNTIME_DIR")
        result.pop("DBUS_SESSION_BUS_ADDRESS")
    elif fixture == "wrong":
        result["XDG_RUNTIME_DIR"] = "/run/user/1000/c27r2-missing-runtime"
        result["DBUS_SESSION_BUS_ADDRESS"] = (
            "unix:path=/run/user/1000/c27r2-missing-bus")
    return result


def service_bus_stat() -> list[int]:
    need(os.getuid() == os.geteuid() == SERVICE_UID
         and SERVICE_RUNTIME.is_dir() and not SERVICE_RUNTIME.is_symlink(),
         "exact user-bus UID/runtime path")
    runtime = os.stat(SERVICE_RUNTIME, follow_symlinks=False)
    socket = os.stat(SERVICE_BUS, follow_symlinks=False)
    need(stat.S_ISDIR(runtime.st_mode) and runtime.st_uid == SERVICE_UID
         and stat.S_ISSOCK(socket.st_mode) and socket.st_uid == SERVICE_UID
         and socket.st_nlink == 1,
         "exact owned runtime directory and singleton Unix bus socket")
    return list(fingerprint(socket))


def validate_core_service(unit: str, invocation: str,
                          service_query_fixture: str) -> dict[str, str]:
    need(type(unit) is str and unit.endswith(".service")
         and re.fullmatch(r"[0-9a-f]{32}", invocation) is not None,
         "core unit/invocation syntax")
    need(capture_direct(SYSTEMCTL, SYSTEMCTL.parent)[1]["sha256"]
             == SYSTEMCTL_SHA256,
         "exact current systemctl binary pin")
    socket_before = service_bus_stat()
    completed = subprocess.run([
        str(SYSTEMCTL), "--user", "show", unit,
        "-p", "LoadState", "-p", "ActiveState", "-p", "SubState",
        "-p", "Result", "-p", "ExecMainCode", "-p", "ExecMainStatus",
        "-p", "InvocationID"], cwd=ROOT,
        env=service_query_environment(service_query_fixture),
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False, timeout=30)
    socket_after = service_bus_stat()
    need(socket_before == socket_after,
         "user bus socket full9stat unchanged across query")
    need(completed.returncode == 0 and completed.stderr == b"",
         "systemd query clean")
    lines = completed.stdout.decode("ascii").splitlines()
    need(len(lines) == 7 and all(line.count("=") == 1 for line in lines)
         and len({line.split("=", 1)[0] for line in lines}) == 7,
         "systemd query exactly seven unique key/value lines")
    fields = dict(line.split("=", 1) for line in lines)
    need(fields == {"Result": "success", "ExecMainCode": "1",
                    "ExecMainStatus": "0", "LoadState": "loaded",
                    "ActiveState": "active", "SubState": "exited",
                    "InvocationID": invocation},
         "exact loaded active/exited clean core service")
    return fields


def validate_core(resolver: Resolver, args: argparse.Namespace,
                  actual: dict[str, Any], gate: dict[str, Any]) \
        -> dict[str, Any]:
    control = logical_name(args.core_control_relative)
    resolver.directory(control, CORE_CONTROL_FILES)
    pinset_path = str(Path(control) / "pinset.json")
    receipt_path = str(Path(control) / "transaction_receipt.json")
    pinset_record = resolver.capture(pinset_path)[1]
    receipt_record = resolver.capture(receipt_path)[1]
    pinset = resolver.document(pinset_path, "pinset_sha256")
    core = resolver.document(receipt_path, "transaction_receipt_sha256")
    need(receipt_record["sha256"] == args.expect_core_receipt_file_sha256
         and core["transaction_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA
         and core.get("status") == CORE_STATUS
         and state_zero(core, "UNAUTHORIZED_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY")
         and core.get("C28_C29") == "UNAUTHORIZED",
         "core receipt dynamic pins/schema/state")
    need(resolver.capture(str(Path(control) / "PASS.lock"))[0] == CORE_PASS,
         "core exact PASS lock")
    need(pinset.get("schema") == PINSET_SCHEMA
         and pinset.get("status")
             == "PASS_DYNAMIC_GATE_SOURCE_ROLE_AND_FRESH_PATH_PINSET__ZERO_CREDIT"
         and pinset.get("source_pins") == SOURCE_PINS
         and state_zero(pinset, "UNAUTHORIZED_PENDING_RELEASE_CHAIN")
         and pinset_record["sha256"] == core["pinset_file_sha256"]
         and pinset["pinset_sha256"] == core["pinset_object_sha256"],
         "core pinset/source closure")
    need(all(resolver.capture(path)[1]["sha256"] == SOURCE_PINS[name]
             for name, path in SOURCE_PATHS.items()),
         "core source pins current")
    authority = pinset.get("actual_v2_authority")
    need(type(authority) is dict
         and authority.get("actual_terminal_dir")
             == logical_name(args.actual_terminal_relative)
         and authority.get("actual_base_seal_dir")
             == logical_name(args.actual_base_relative)
         and authority.get("actual_terminal_root_sha256")
             == actual["terminal_root"] == args.expect_actual_terminal_root_sha256
         and authority.get("actual_terminal_receipt_file_sha256")
             == actual["terminal_receipt_file"]
             == args.expect_actual_terminal_receipt_file_sha256
         and authority.get("actual_terminal_receipt_object_sha256")
             == actual["terminal_receipt_object"]
             == args.expect_actual_terminal_receipt_object_sha256
         and authority.get("gate_execution_root_object_sha256")
             == gate["gate_root_object"]
         and authority.get("seed1_edge_path")
             == logical_name(args.seed1_edge_relative)
         and authority.get("seed2_edge_path")
             == logical_name(args.seed2_edge_relative)
         and authority.get("frozen_C15_path")
             == logical_name(args.frozen_c15_relative)
         and authority.get("seed1_edge_sha256")
             == resolver.capture(args.seed1_edge_relative)[1]["sha256"]
             == args.expect_seed1_edge_sha256
         and authority.get("seed2_edge_sha256")
             == resolver.capture(args.seed2_edge_relative)[1]["sha256"]
             == args.expect_seed2_edge_sha256
         and authority.get("frozen_C15_sha256")
             == resolver.capture(args.frozen_c15_relative)[1]["sha256"]
             == args.expect_frozen_c15_sha256,
         "CLI/actual/pinset four-way authority closure")
    need(core.get("gate_receipt_file_sha256") == gate["gate_receipt_file"]
         and core.get("gate_receipt_object_sha256") == gate["gate_receipt_object"]
         and core.get("gate_execution_root_file_sha256") == gate["gate_root_file"]
         and core.get("gate_execution_root_object_sha256") == gate["gate_root_object"]
         and core.get("gate_PASS_lock_sha256")
             == resolver.capture(str(Path(args.gate_relative) / "PASS.lock"))[1]["sha256"],
         "core to post-actual gate closure")
    attestations = core.get("gate_pre_post_attestations")
    need(type(attestations) is dict and len(attestations) >= 18,
         "gate current attestation map")
    for record in attestations.values():
        need(type(record) is dict and record.get("O_NOFOLLOW") is True
             and record.get("single_open_file_description_hash_fstat_and_path_identity") is True
             and type(record.get("stat_fingerprint")) is list
             and len(record["stat_fingerprint"]) == 9,
             "gate full-nine attestation shape")
        _, current = resolver.capture(record["path"])
        need(sha_record_matches(record, current),
             "gate attestation current SHA/full9stat")
    targets = pinset.get("targets")
    expected_targets = {
        "control": logical_name(args.core_control_relative),
        "producer_candidate": logical_name(args.candidate_relative),
        "verifier_output": logical_name(args.verifier_output_relative),
        "attack_work": logical_name(args.attack_work_relative),
        "producer_run": logical_name(args.producer_run_relative),
        "verifier_run": logical_name(args.verifier_run_relative),
        "attack_run": logical_name(args.attack_run_relative),
    }
    need(targets == expected_targets, "core target topology")
    runs = {}
    for stage, (spec, run_key, source, seed) in STAGES.items():
        runs[stage] = validate_run(resolver, args, control, pinset, core,
                                   stage, spec, run_key, source, seed, targets)
        prefix = str(Path(control) / (stage + "_runner"))
        wrapper_stdout = resolver.capture(prefix + ".stdout.log")[0]
        wrapper_stderr = resolver.capture(prefix + ".stderr.log")[0]
        wrapper_exit = resolver.capture(prefix + ".exit_code.txt")[0]
        need(wrapper_exit == b"0\n" and wrapper_stderr == b""
             and wrapper_stdout.endswith(b"\n")
             and not wrapper_stdout.endswith(b"\n\n"),
             stage + ":core wrapper clean transcript")
        wrapper_value = strict(wrapper_stdout[:-1])
        need(type(wrapper_value) is dict
             and canonical(wrapper_value) == wrapper_stdout[:-1]
             and wrapper_value == {"CM2": "NO-GO_FOR_CLAIM",
                "formal_credit": 0, "stage": stage, "status": RUN_STATUS},
             stage + ":core wrapper exact stdout")
    candidate = validate_candidate(resolver, args)
    verification_path = str(Path(args.verifier_output_relative) / "verification.json")
    resolver.directory(args.verifier_output_relative, {"verification.json"})
    verification_record = resolver.capture(verification_path)[1]
    verification = resolver.document(verification_path, "verification_sha256")
    need(verification.get("schema") == VERIFICATION_SCHEMA
         and verification.get("status") == VERIFICATION_STATUS
         and state_zero(verification,
             "UNAUTHORIZED_PENDING_ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL")
         and verification.get("candidate_result_file_sha256")
             == candidate["result_record"]["sha256"]
         and verification.get("candidate_result_object_sha256")
             == candidate["result"]["result_sha256"]
         and verification_record["sha256"] == core["seed2"]["verification_file_sha256"]
         and verification["verification_sha256"]
             == core["seed2"]["verification_object_sha256"],
         "independent verification/core closure")
    attacks_path = str(Path(args.attack_work_relative) / "coherent_attacks.json")
    attacks_record = resolver.capture(attacks_path)[1]
    attacks = resolver.document(attacks_path, "attack_harness_sha256")
    need(attacks.get("schema") == ATTACK_SCHEMA
         and attacks.get("status") == ATTACK_STATUS
         and attacks.get("attack_count") == 21
         and attacks.get("accepted") == 0 and attacks.get("rejected") == 21
         and type(attacks.get("attacks")) is list and len(attacks["attacks"]) == 21
         and all(row.get("numeric_exit_code") == 2
                 and row.get("rejected_fail_closed") is True
                 and row.get("verification_output_created") is False
                 for row in attacks["attacks"])
         and attacks.get("formal_credit") == 0
         and attacks.get("manifest_authorized") is False
         and attacks.get("C27R2") == "UNAUTHORIZED_PENDING_RELEASE_CHAIN"
         and attacks_record["sha256"] == core["coherent_attacks"]["file_sha256"]
         and attacks.get("harness_source_sha256") == SOURCE_PINS["coherent_attack_harness"],
         "real 21 subprocess coherent attacks/core closure")
    need(attacks["attack_harness_sha256"]
             == core["coherent_attacks"]["object_sha256"],
         "coherent attack object/core pin")
    service = validate_core_service(args.core_unit, args.core_invocation_id,
                                    args.service_query_fixture)
    return {"receipt_file": receipt_record["sha256"],
            "receipt_object": core["transaction_receipt_sha256"],
            "pinset_object": pinset["pinset_sha256"],
            "verification_object": verification["verification_sha256"],
            "attacks_file": attacks_record["sha256"],
            "authority_input_paths": core_authority_input_paths(args),
            "service": service, "core": core, "runs": runs}


def validate_cold(resolver: Resolver, args: argparse.Namespace,
                  core: dict[str, Any], actual: dict[str, Any],
                  gate: dict[str, Any]) -> dict[str, Any]:
    control = logical_name(args.cold_control_relative)
    output = logical_name(args.cold_output_relative)
    run = logical_name(args.cold_run_relative)
    resolver.directory(control, COLD_CONTROL_FILES)
    resolver.directory(output, {"verification.json"})
    resolver.directory(run, RUN_FILES)
    pinset_path = str(Path(control) / "pinset.json")
    spec_path = str(Path(control) / "cold_command_spec.json")
    receipt_path = str(Path(control) / "cold_replay_receipt.json")
    pinset_record = resolver.capture(pinset_path)[1]
    spec_record = resolver.capture(spec_path)[1]
    receipt_record = resolver.capture(receipt_path)[1]
    pinset = resolver.document(pinset_path, "pinset_sha256")
    spec = resolver.document(spec_path, "command_spec_sha256")
    receipt = resolver.document(receipt_path, "cold_replay_receipt_sha256")
    attestation_path = str(Path(run) / "run_attestation.json")
    attestation_record = resolver.capture(attestation_path)[1]
    attestation = resolver.document(attestation_path, "run_attestation_sha256")
    expected_inputs, expected_role_map = cold_expected_contract(resolver, args)
    expected_input_digest = hashlib.sha256(b"".join(
        path.encode("ascii") + b"\n" for path in expected_inputs)).hexdigest()
    expected_authority_closure = {
        "actual_terminal_root_sha256": actual["terminal_root"],
        "actual_terminal_receipt_file_sha256":
            actual["terminal_receipt_file"],
        "actual_terminal_receipt_object_sha256":
            actual["terminal_receipt_object"],
        "actual_terminal_replay_object_sha256":
            actual["terminal_replay_object"],
        "actual_base_receipt_object_sha256": actual["base_receipt_object"],
        "gate_receipt_object_sha256": gate["gate_receipt_object"],
        "gate_execution_root_object_sha256": gate["gate_root_object"],
        "seed1_edge_sha256": args.expect_seed1_edge_sha256,
        "seed2_edge_sha256": args.expect_seed2_edge_sha256,
        "frozen_C15_sha256": args.expect_frozen_c15_sha256,
    }
    expected_cold_math = {
        "C15_sha256": args.expect_frozen_c15_sha256,
        "candidate_result_object_sha256":
            core["core"]["seed1"]["candidate_result_object_sha256"],
        "cross_pairs": 125_561_998_198, "cycles": 668,
        "edges": 14_860, "members": 502_204, "merges": 14_192,
        "old_components": 57_876, "post_components": 43_684,
        "seed1_edge_sha256": args.expect_seed1_edge_sha256,
        "seed2_edge_sha256": args.expect_seed2_edge_sha256,
        "terminal_receipt_object_sha256": actual["terminal_receipt_object"],
        "within_pairs": 542_179_508,
    }
    expected_cold_process_policy = {
        "control_plane": {
            "environment": CONTROL_BUS_ENV,
            "purpose": "read_only_user_service_discovery",
            "systemctl_path": str(SYSTEMCTL),
            "systemctl_sha256": SYSTEMCTL_SHA256,
            "uid": SERVICE_UID,
        },
        "environment_key_partition": {
            "control_plane_only": ["DBUS_SESSION_BUS_ADDRESS",
                                   "XDG_RUNTIME_DIR"],
            "mathematical_only": ["PYTHONHASHSEED"],
            "shared_locale_and_path": ["LANG", "LC_ALL", "PATH"],
        },
        "mathematical_stage_child": {
            "dont_write_bytecode": True,
            "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                "LC_ALL": "C", "PYTHONHASHSEED":
                    args.cold_python_hash_seed},
            "isolated_python": True,
            "purpose": "execute_no_import_seed2_verifier_only",
        },
        "mathematical_transaction_wrapper": {
            "dont_write_bytecode": True,
            "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                "LC_ALL": "C", "PYTHONHASHSEED": "30662728"},
            "isolated_python": True,
            "purpose": "execute_frozen_transaction_runner_only",
        },
    }
    receipt_keys = {
        "schema", "status", "completed_at_utc", "predecessor_unit",
        "predecessor_invocation_id", "core_receipt_file_sha256",
        "core_receipt_object_sha256", "verification_file_sha256",
        "verification_object_sha256", "formal_verification_byte_identical",
        "run_attestation_file_sha256", "run_attestation_object_sha256",
        "numeric_exit_code", "signal", "stderr_empty",
        "all_core_inputs_pre_post_sha_stat_identical",
        "exact_process_success_file_count", "exact_declared_input_count",
        "exact_process_capture_count", "exact_declared_input_paths_sha256",
        "exact_attested_path_sequence_sha256", "authority_closure",
        "process_policy",
        "no_import_seed2_verifier", "ledger_quotient_count_closure",
        "formal_credit", "manifest_authorized", "C27R2", "C28_C29", "CM2",
        "cold_replay_receipt_sha256",
    }
    need(receipt_record["sha256"] == args.expect_cold_receipt_file_sha256
         and receipt["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and set(receipt) == receipt_keys
         and receipt.get("schema") == COLD_SCHEMA
         and receipt.get("status") == COLD_STATUS
         and receipt.get("core_receipt_file_sha256") == core["receipt_file"]
         and receipt.get("core_receipt_object_sha256") == core["receipt_object"]
         and receipt.get("predecessor_unit") == args.core_unit
         and receipt.get("predecessor_invocation_id") == args.core_invocation_id
         and receipt.get("numeric_exit_code") == 0
         and receipt.get("signal") is None
         and receipt.get("stderr_empty") is True
         and receipt.get("formal_verification_byte_identical") is True
         and receipt.get("all_core_inputs_pre_post_sha_stat_identical") is True
         and receipt.get("exact_process_success_file_count") == 11
         and receipt.get("exact_declared_input_count") == 165
         and receipt.get("exact_process_capture_count") == 167
         and receipt.get("exact_declared_input_paths_sha256")
             == expected_input_digest == COLD_INPUT_PATHS_SHA256
         and receipt.get("authority_closure") == expected_authority_closure
         and receipt.get("no_import_seed2_verifier") is True
         and receipt.get("ledger_quotient_count_closure") == expected_cold_math
         and receipt.get("process_policy") == expected_cold_process_policy
         and receipt.get("run_attestation_file_sha256")
             == attestation_record["sha256"]
         and receipt.get("run_attestation_object_sha256")
             == attestation["run_attestation_sha256"]
         and receipt.get("C28_C29") == "UNAUTHORIZED"
         and state_zero(receipt,
             "UNAUTHORIZED_PENDING_RELEASE_ATTACKS_MANIFEST_OUTER_AND_TERMINAL_REPLAY")
         and resolver.capture(str(Path(control) / "PASS.lock"))[0] == COLD_PASS
         and resolver.capture(str(Path(control) / "runner.exit_code.txt"))[0] == b"0\n"
         and resolver.capture(str(Path(control) / "runner.stderr.log"))[0] == b"",
         "fresh cold receipt/process/core closure")
    control_stdout = resolver.capture(str(Path(control) / "runner.stdout.log"))[0]
    need(control_stdout.endswith(b"\n")
         and not control_stdout.endswith(b"\n\n"),
         "fresh cold control stdout newline")
    control_stdout_value = strict(control_stdout[:-1])
    need(type(control_stdout_value) is dict
         and canonical(control_stdout_value) == control_stdout[:-1]
         and control_stdout_value == {"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "stage": "independent_verifier",
            "status": RUN_STATUS},
         "fresh cold exact wrapper stdout")
    pinset_keys = {
        "schema", "status", "predecessor_unit", "predecessor_invocation_id",
        "core_receipt_file_sha256", "core_receipt_object_sha256",
        "actual_v2_authority", "source_pins", "targets",
        "exact_declared_input_count", "exact_declared_input_paths_sha256",
        "declared_input_role_map", "declared_input_role_map_sha256",
        "process_policy",
        "cold_replay_only", "formal_credit", "manifest_authorized", "C27R2",
        "CM2", "pinset_sha256",
    }
    need(set(pinset) == pinset_keys
         and pinset.get("schema") == PINSET_SCHEMA
         and pinset.get("status") == "PASS_C27R2_RELEASE_COLD_REPLAY_PINSET__ZERO_CREDIT"
         and pinset.get("source_pins") == {
             "cold_replay_helper": COLD_HELPER_SHA256,
             "independent_verifier": SOURCE_PINS["independent_verifier"],
             "python": SOURCE_PINS["python"],
             "transaction_runner": SOURCE_PINS["transaction_runner"]}
         and pinset.get("targets") == {"control": control, "output": output,
                                         "run": run}
         and pinset.get("core_receipt_file_sha256") == core["receipt_file"]
         and pinset.get("core_receipt_object_sha256") == core["receipt_object"]
         and pinset.get("predecessor_unit") == args.core_unit
         and pinset.get("predecessor_invocation_id") == args.core_invocation_id
         and pinset.get("actual_v2_authority") == expected_authority_closure
         and pinset.get("exact_declared_input_count") == 165
         and pinset.get("exact_declared_input_paths_sha256")
             == expected_input_digest == COLD_INPUT_PATHS_SHA256
         and pinset.get("declared_input_role_map") == expected_role_map
         and pinset.get("declared_input_role_map_sha256")
             == COLD_ROLE_MAP_SHA256 == digest(expected_role_map)
         and pinset.get("cold_replay_only") is True
         and pinset.get("process_policy") == expected_cold_process_policy
         and state_zero(pinset, "UNAUTHORIZED")
         and pinset_record["sha256"] == spec.get("pinset_file_sha256")
         and pinset["pinset_sha256"] == spec.get("pinset_object_sha256"),
         "fresh cold pinset topology/source/core closure")
    need(resolver.capture(args.cold_helper_relative)[1]["sha256"]
             == args.expect_cold_helper_sha256 == COLD_HELPER_SHA256,
         "fresh cold helper current source pin")
    argv = spec.get("argv")
    expected_argv = [
        args.python, "-I", "-B",
        str((ROOT / SOURCE_PATHS["independent_verifier"]).absolute()),
        "--terminal-dir", str((ROOT / args.actual_terminal_relative).absolute()),
        "--base-seal-dir", str((ROOT / args.actual_base_relative).absolute()),
        "--expect-terminal-root-sha256",
        args.expect_actual_terminal_root_sha256,
        "--expect-terminal-receipt-file-sha256",
        args.expect_actual_terminal_receipt_file_sha256,
        "--expect-terminal-receipt-object-sha256",
        args.expect_actual_terminal_receipt_object_sha256,
        "--candidate-dir", str((ROOT / args.candidate_relative).absolute()),
        "--out-file", str((ROOT / output / "verification.json").absolute()),
    ]
    expected_output_roots = [{
        "path": str((ROOT / output).absolute()), "kind": "directory",
        "precondition": "EXISTING_EMPTY_DIRECTORY",
        "exact_inventory": ["verification.json"],
        "required_relative_files": ["verification.json"]}]
    input_paths = spec.get("input_paths")
    need(type(input_paths) is list and input_paths == sorted(set(input_paths)),
         "fresh cold sorted unique declared inputs")
    spec_keys = {
        "schema", "stage", "source_path", "source_sha256", "argv",
        "environment", "python_hash_seed", "timeout_seconds",
        "expected_stdout_status", "input_paths", "exact_declared_input_count",
        "exact_declared_input_paths_sha256", "declared_input_role_map_sha256",
        "output_roots", "pinset_file_sha256", "pinset_object_sha256",
        "runner_source_sha256", "python_sha256", "formal_credit", "CM2",
        "command_spec_sha256",
    }
    need(set(spec) == spec_keys
         and args.cold_python_hash_seed == "30662727"
         and spec.get("schema") == SPEC_SCHEMA
         and spec.get("stage") == "independent_verifier"
         and spec.get("environment") == {"PATH": "/usr/bin:/bin", "LANG": "C",
             "LC_ALL": "C", "PYTHONHASHSEED": args.cold_python_hash_seed}
         and argv == expected_argv
         and spec.get("source_path")
             == str((ROOT / SOURCE_PATHS["independent_verifier"]).absolute())
         and spec.get("output_roots") == expected_output_roots
         and spec.get("expected_stdout_status") == VERIFICATION_STATUS
         and type(spec.get("timeout_seconds")) is int
         and 60 <= spec["timeout_seconds"] <= 86_400
         and input_paths == expected_inputs
         and spec.get("exact_declared_input_count") == 165
         and spec.get("exact_declared_input_paths_sha256")
             == COLD_INPUT_PATHS_SHA256 == expected_input_digest
         and spec.get("declared_input_role_map_sha256")
             == COLD_ROLE_MAP_SHA256
         and spec.get("source_sha256") == SOURCE_PINS["independent_verifier"]
         and spec.get("runner_source_sha256") == SOURCE_PINS["transaction_runner"]
         and spec.get("python_sha256") == SOURCE_PINS["python"]
         and spec.get("formal_credit") == 0
         and spec.get("CM2") == "NO-GO_FOR_CLAIM",
         "fresh cold full exact argv/input/output/source/env/seed closure")
    need(attestation.get("schema") == RUN_SCHEMA
         and attestation.get("status") == RUN_STATUS
         and attestation.get("stage") == "independent_verifier"
         and attestation.get("numeric_exit_code") == 0
         and attestation.get("signal") is None
         and attestation.get("timed_out") is False
         and attestation.get("stderr_empty") is True
         and attestation.get("stderr_sha256") == EMPTY_SHA
         and attestation.get("input_pre_post_sha_stat_identical") is True
         and attestation.get("command_spec_file_sha256") == spec_record["sha256"]
         and attestation.get("command_spec_object_sha256")
             == spec["command_spec_sha256"]
         and attestation.get("pinset_object_sha256") == pinset["pinset_sha256"]
         and attestation.get("runner_source_sha256")
             == SOURCE_PINS["transaction_runner"]
         and attestation.get("stage_source_sha256")
             == SOURCE_PINS["independent_verifier"]
         and attestation.get("python_sha256") == SOURCE_PINS["python"]
         and state_zero(attestation, "UNAUTHORIZED_PENDING_RELEASE_CHAIN")
         and attestation["run_attestation_sha256"]
             == receipt["run_attestation_object_sha256"],
         "fresh cold run attestation closure")
    need(resolver.capture(str(Path(run) / "exit_code.txt"))[0] == b"0\n"
         and resolver.capture(str(Path(run) / "signal.json"))[0] == b"null\n"
         and resolver.capture(str(Path(run) / "stderr.log"))[0] == b""
         and resolver.capture(str(Path(run) / "input_pre.json"))[0]
             == resolver.capture(str(Path(run) / "input_post.json"))[0]
         and resolver.plain(str(Path(run) / "input_post.json"))
             == attestation["input_attestations"]
         and resolver.plain(str(Path(run) / "output_validation.json"))
             == attestation["output_validation"],
         "fresh cold run sidecars")
    cold_stdout = resolver.capture(str(Path(run) / "stdout.log"))[0]
    need(cold_stdout.endswith(b"\n") and not cold_stdout.endswith(b"\n\n"),
         "fresh cold stdout newline")
    cold_stdout_value = strict(cold_stdout[:-1])
    expected_run_pass = (
        b"PASS_C27R2_AUTHORITY_V2_INDEPENDENT_VERIFIER_PROCESS_"
        b"TRANSACTION__ZERO_CREDIT\n")
    timing = resolver.plain(str(Path(run) / "timing.json"))
    start = resolver.plain(str(Path(run) / "runner_start.json"))
    need(type(cold_stdout_value) is dict
         and canonical(cold_stdout_value) == cold_stdout[:-1]
         and cold_stdout_value == attestation.get("stdout")
         and cold_stdout_value.get("status") == VERIFICATION_STATUS
         and cold_stdout_value.get("formal_credit") == 0
         and cold_stdout_value.get("CM2") == "NO-GO_FOR_CLAIM"
         and hashlib.sha256(cold_stdout).hexdigest()
             == attestation.get("stdout_sha256")
         and resolver.capture(str(Path(run) / "PASS.lock"))[0]
             == expected_run_pass
         and timing == {"elapsed_seconds": attestation["elapsed_seconds"],
                        "timed_out": False}
         and start == {"schema": RUN_SCHEMA + ".start",
            "stage": "independent_verifier",
            "started_at_utc": attestation["started_at_utc"],
            "runner_source_sha256": SOURCE_PINS["transaction_runner"],
            "command_spec_file_sha256": spec_record["sha256"],
            "command_spec_object_sha256": spec["command_spec_sha256"],
            "pinset_file_sha256": pinset_record["sha256"],
            "pinset_object_sha256": pinset["pinset_sha256"],
            "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM"},
         "fresh cold stdout/PASS/timing/start closure")
    validate_historical_current(resolver, attestation["input_attestations"],
                                "fresh cold", expected_inputs, spec_path,
                                pinset_path)
    expected_attested_paths = [spec_path, pinset_path, *expected_inputs]
    expected_attested_digest = hashlib.sha256(b"".join(
        path.encode("ascii") + b"\n" for path in expected_attested_paths)
    ).hexdigest()
    need(len(expected_attested_paths) == 167
         and expected_attested_digest == COLD_ATTESTED_PATH_SEQUENCE_SHA256
         and receipt.get("exact_attested_path_sequence_sha256")
             == expected_attested_digest,
         "fresh cold exact 167 attested path sequence digest")
    cold_verification = resolver.capture(str(Path(output) / "verification.json"))[0]
    formal_verification = resolver.capture(
        str(Path(args.verifier_output_relative) / "verification.json"))[0]
    need(cold_verification == formal_verification
         and hashlib.sha256(cold_verification).hexdigest()
             == receipt["verification_file_sha256"]
         and receipt.get("verification_object_sha256")
             == core["verification_object"],
         "fresh cold byte-identical independent verification")
    current_output = {spec["output_roots"][0]["path"]:
                      resolver.snapshot(output, ["verification.json"])}
    need(current_output == attestation["output_validation"],
         "fresh cold current output equals run historical closure")
    return {"receipt_file": receipt_record["sha256"],
            "receipt_object": receipt["cold_replay_receipt_sha256"],
            "run_object": attestation["run_attestation_sha256"]}


def validate_evidence(resolver: Resolver, args: argparse.Namespace,
                      core: dict[str, Any]) -> dict[str, Any]:
    evidence_dir = logical_name(args.evidence_relative)
    resolver.directory(evidence_dir,
                       {"core_inventory.sha256", "evidence_bundle.json"})
    path = str(Path(evidence_dir) / "evidence_bundle.json")
    record = resolver.capture(path)[1]
    value = resolver.document(path, "evidence_bundle_sha256")
    need(resolver.capture(args.evidence_builder_relative)[1]["sha256"]
             == args.expect_evidence_builder_sha256,
         "fresh evidence builder current source pin")
    need(record["sha256"] == args.expect_evidence_file_sha256
         and value["evidence_bundle_sha256"] == args.expect_evidence_object_sha256
         and value.get("schema") == EVIDENCE_SCHEMA
         and value.get("status") == EVIDENCE_STATUS
         and value.get("core_transaction_receipt_file_sha256")
             == core["receipt_file"]
         and value.get("core_transaction_receipt_object_sha256")
             == core["receipt_object"]
         and value.get("predecessor_unit") == args.core_unit
         and value.get("predecessor_invocation_id") == args.core_invocation_id
         and value.get("cold_replay_completed") is False
         and value.get("release_attacks_completed") is False
         and state_zero(value,
             "UNAUTHORIZED_PENDING_COLD_RELEASE_ATTACKS_MANIFEST_OUTER_AND_TERMINAL_REPLAY"),
         "fresh evidence receipt/core/state closure")
    attestations = value.get("attestations")
    need(type(attestations) is dict
         and len(attestations) == value.get("core_member_count") == 128,
         "evidence exact core member count")
    rows: list[str] = []
    for logical, historical in sorted(attestations.items()):
        need(logical_name(logical) == logical
             and type(historical) is dict
             and historical.get("O_NOFOLLOW") is True
             and historical.get("single_link") is True
             and len(historical.get("stat_fingerprint", [])) == 9,
             "evidence attestation shape")
        _, current = resolver.capture(logical)
        need(sha_record_matches(historical, current),
             "evidence current member SHA/full9stat")
        rows.append(f"{current['sha256']}  {logical}")
    inventory = ("\n".join(rows) + "\n").encode("ascii")
    need(resolver.capture(str(Path(evidence_dir) / "core_inventory.sha256"))[0]
             == inventory
         and hashlib.sha256(inventory).hexdigest()
             == value["core_inventory_sha256"],
         "evidence sorted inventory/current closure")
    return {"file": record["sha256"],
            "object": value["evidence_bundle_sha256"],
            "inventory": value["core_inventory_sha256"]}


def validate_future_absent(resolver: Resolver, args: argparse.Namespace) -> None:
    # The repair boundary is pre-release.  It must never consume, create, or
    # bless outer/seal/terminal output.  A private override of one of these
    # logical roots therefore remains a real negative fixture.
    for raw in (args.future_outer_relative, args.future_seal_relative,
                args.future_terminal_relative):
        logical, physical, _ = resolver.resolve(raw)
        need(not physical.exists() and not physical.is_symlink(),
             "future authority absent at repair boundary:" + logical)


def validate_no_import_exec(payload: bytes) -> None:
    tree = ast.parse(payload.decode("utf-8"), filename=str(SELF))
    forbidden = {Path(path).stem for path in SOURCE_PATHS.values()}
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {alias.name.split(".")[0] for alias in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    need(imported.isdisjoint(forbidden), "no producer/verifier/harness import")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    validate_environment(args)
    override_logical, override_physical, case_root, override = load_override(args)
    out_file = Path(args.out_file).absolute()
    need(out_file.is_relative_to(AUDIT) and out_file.parent.is_dir()
         and not out_file.parent.is_symlink()
         and not out_file.exists() and not out_file.is_symlink(),
         "fresh validator output confined to audit")
    if args.mode == "private":
        need(case_root is not None
             and out_file == case_root / "validator-output.json",
             "private output exact case-root path")
    resolver = Resolver(override_logical, override_physical, case_root,
                        args.fixture_barrier)
    self_payload = resolver.capture(logical_name(SELF), 16 << 20)[0]
    validate_no_import_exec(self_payload)
    validate_future_absent(resolver, args)
    actual = validate_actual(resolver, args)
    gate = validate_gate(resolver, args)
    core = validate_core(resolver, args, actual, gate)
    cold = validate_cold(resolver, args, core, actual, gate)
    evidence = validate_evidence(resolver, args, core)
    need((args.mode == "formal" and not resolver.override_used)
         or (args.mode == "private" and resolver.override_used),
         "override usage exactly matches mode")
    current_digest = resolver.verify_current()
    body = {
        "schema": OUTPUT_SCHEMA,
        "status": FORMAL_STATUS if args.mode == "formal" else PRIVATE_STATUS,
        "validated_at_utc": utc_now(),
        "mode": args.mode,
        "override_map_file_sha256": args.expect_override_map_file_sha256,
        "override_map_object_sha256": override["override_map_sha256"],
        "override_count": len(override["entries"]),
        "baseline_accepted": args.mode == "formal",
        "authority_pre_sha_stat_captured": True,
        "authority_pre_post_sha_stat_identical": True,
        "process_and_current_output_closure_verified": True,
        "authority_record_count": len(resolver.records),
        "authority_current_projection_sha256": current_digest,
        "actual_v2": actual,
        "post_actual_gate": gate,
        "core": {key: core[key] for key in (
            "receipt_file", "receipt_object", "pinset_object",
            "verification_object", "attacks_file")},
        "cold": cold,
        "evidence": evidence,
        "core_service": {"unit": args.core_unit,
                         "invocation_id": args.core_invocation_id,
                         "state": core["service"]},
        "service_query_policy": {
            "systemctl": str(SYSTEMCTL),
            "systemctl_sha256": SYSTEMCTL_SHA256,
            "uid": SERVICE_UID, "runtime": str(SERVICE_RUNTIME),
            "bus_socket": str(SERVICE_BUS), "environment": CONTROL_BUS_ENV,
            "fixture": args.service_query_fixture,
            "returned_field_count": 7,
        },
        "process_policy": {"python": args.python, "python_sha256":
            args.expect_python_sha256, "isolated": True,
            "dont_write_bytecode": True,
            "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                "LC_ALL": "C", "PYTHONHASHSEED":
                    args.expected_python_hash_seed}},
        "formal_credit": 0,
        "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_REPAIRED_RELEASE_CHAIN",
        "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["validation_sha256"] = digest(body)
    return result


def write_once(path: Path, payload: bytes) -> None:
    path = path.absolute()
    need(path.parent.is_dir() and not path.parent.is_symlink()
         and not path.exists() and not path.is_symlink(), "fresh output file")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        view = memoryview(payload)
        offset = 0
        while offset < len(view):
            written = os.write(descriptor, view[offset:])
            need(type(written) is int and written > 0,
                 "write-all made positive progress")
            offset += written
        need(offset == len(payload), "write-all exact payload length")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    reopened, record = capture_direct(path, path.parent,
                                      max(1, len(payload)))
    need(reopened == payload and record["size"] == len(payload),
         "reopened output exact bytes/current SHA/full9stat")
    parent_descriptor = os.open(path.parent, os.O_RDONLY
                                | getattr(os, "O_DIRECTORY", 0)
                                | getattr(os, "O_CLOEXEC", 0)
                                | getattr(os, "O_NOFOLLOW", 0))
    try:
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)


def self_test() -> dict[str, Any]:
    need(digest({"b": 2, "a": 1})
         == hashlib.sha256(b'{"a":1,"b":2}').hexdigest(),
         "canonical digest fixture")
    try:
        strict(b'{"a":1,"a":2}')
    except Rejected:
        pass
    else:
        raise Rejected("duplicate key fixture rejected")
    fixed_bus = service_query_environment("fixed")
    missing_bus = service_query_environment("missing")
    wrong_bus = service_query_environment("wrong")
    need(fixed_bus == CONTROL_BUS_ENV
         and set(fixed_bus) == {"PATH", "LANG", "LC_ALL",
                               "XDG_RUNTIME_DIR",
                               "DBUS_SESSION_BUS_ADDRESS"}
         and "XDG_RUNTIME_DIR" not in missing_bus
         and "DBUS_SESSION_BUS_ADDRESS" not in missing_bus
         and missing_bus == {"PATH": "/usr/bin:/bin", "LANG": "C",
                             "LC_ALL": "C"}
         and wrong_bus["XDG_RUNTIME_DIR"]
             == "/run/user/1000/c27r2-missing-runtime"
         and wrong_bus["DBUS_SESSION_BUS_ADDRESS"]
             == "unix:path=/run/user/1000/c27r2-missing-bus"
         and wrong_bus != fixed_bus,
         "fixed/missing/wrong user-bus query environment fixtures")
    with tempfile.TemporaryDirectory(prefix="c27r2-boundary-v5-") as raw:
        root = Path(raw)
        normal = root / "normal"
        normal.write_bytes(b"fixture\n")
        payload, record = capture_direct(normal, root)
        need(payload == b"fixture\n" and len(record["stat_fingerprint"]) == 9,
             "direct capture fixture")
        symlink = root / "symlink"
        symlink.symlink_to(normal)
        try:
            capture_direct(symlink, root)
        except (Rejected, OSError):
            pass
        else:
            raise Rejected("symlink fixture rejected")
        hard = root / "hard"
        os.link(normal, hard)
        try:
            capture_direct(normal, root)
        except Rejected:
            pass
        else:
            raise Rejected("hardlink fixture rejected")
        hard.unlink()
        row = {"ordinal": 0, "formal_credit": 0}
        row["row_sha256"] = digest(row)
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=0) as stream:
            stream.write(canonical(row) + b"\n")
        descriptor = {"row_count": 1,
            "row_sequence_sha256": hashlib.sha256(
                row["row_sha256"].encode("ascii") + b"\n").hexdigest(),
            "canonical_jsonl": True, "gzip_mtime": 0}
        validate_gzip(buffer.getvalue(), descriptor, 1)
        body = {"schema": OVERRIDE_SCHEMA, "mode": "formal", "entries": [],
                "formal_credit": 0, "manifest_authorized": False,
                "C27R2": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM"}
        closed = dict(body)
        closed["override_map_sha256"] = digest(body)
        need(decode_document(canonical(closed) + b"\n",
                             "override_map_sha256") == closed,
             "override object closure fixture")
    need(len(RUN_FILES) == 11 and len(CORE_CONTROL_FILES) == 18
         and len(GATE_FILES) == 14 and len(COLD_CONTROL_FILES) == 7,
         "exact run/core/gate/cold inventory fixtures")
    fixture_paths = ["fixture/spec", "fixture/pinset", "fixture/a", "fixture/b"]
    fixture_records = {
        path: {"path": path, "sha256": hashlib.sha256(path.encode()).hexdigest(),
               "size": len(path),
               "stat_fingerprint": [1, 2, stat.S_IFREG | 0o400, 1,
                                    len(path), 3, 4, 5, 6],
               "O_NOFOLLOW": True,
               "single_open_file_description_hash_child_fstat_and_path_identity":
                   True}
        for path in fixture_paths
    }
    class HistoricalFixtureResolver:
        def capture(self, raw: str) -> tuple[bytes, dict[str, Any]]:
            return b"", fixture_records[raw]
    fixture_attestations = {
        "command-spec": fixture_records["fixture/spec"],
        "pinset": fixture_records["fixture/pinset"],
        "declared-input-000": fixture_records["fixture/a"],
        "declared-input-001": fixture_records["fixture/b"],
    }
    validate_historical_current(HistoricalFixtureResolver(),
        fixture_attestations, "fixture", ["fixture/a", "fixture/b"],
        "fixture/spec", "fixture/pinset")
    for broken in (
        {**fixture_attestations,
         "declared-input-999": fixture_records["fixture/a"]},
        {key: value for key, value in fixture_attestations.items()
         if key != "declared-input-001"},
    ):
        try:
            validate_historical_current(HistoricalFixtureResolver(), broken,
                "fixture", ["fixture/a", "fixture/b"], "fixture/spec",
                "fixture/pinset")
        except Rejected:
            pass
        else:
            raise Rejected("attestation extra/omitted path fixture rejected")
    need(all(valid_sha(value) for value in (
            COLD_HELPER_SHA256, COLD_INPUT_PATHS_SHA256,
            COLD_ROLE_MAP_SHA256, COLD_ATTESTED_PATH_SEQUENCE_SHA256)),
         "frozen fresh cold v3 contract digest fixtures")
    dummy = argparse.Namespace(
        python="/usr/bin/python3.12",
        actual_terminal_relative="audit/terminal",
        actual_base_relative="audit/base",
        expect_actual_terminal_root_sha256="1" * 64,
        expect_actual_terminal_receipt_file_sha256="2" * 64,
        expect_actual_terminal_receipt_object_sha256="3" * 64,
        candidate_relative="audit/candidate",
        verifier_output_relative="audit/verifier",
        attack_work_relative="audit/attacks")
    contracts = [expected_stage_contract(dummy, stage, source) for
        stage, source in (("producer", "producer"),
                          ("independent_verifier", "independent_verifier"),
                          ("coherent_attacks", "coherent_attack_harness"))]
    need([contract[0][3] for contract in contracts]
             == [str((ROOT / SOURCE_PATHS[name]).absolute()) for name in
                 ("producer", "independent_verifier",
                  "coherent_attack_harness")]
         and [contract[2] for contract in contracts]
             == [RESULT_STATUS, VERIFICATION_STATUS, ATTACK_STATUS]
         and all(type(contract[1]) is list and len(contract[1]) == 1
                 for contract in contracts),
         "full exact stage argv/output/stdout contract fixtures")
    self_payload = capture_direct(SELF, ROOT, 16 << 20)[0]
    validate_no_import_exec(self_payload)
    return {"schema": OUTPUT_SCHEMA + ".self-test",
            "status": "PASS_TINY_CANONICAL_DUPLICATE_GZIP_OVERRIDE_O_NOFOLLOW_"
                      "NLINK_FULL9STAT_FIXED_MISSING_WRONG_USER_BUS_AND_NO_"
                      "IMPORT_FIXTURES",
            "formal_reads": 0, "formal_outputs": 0, "formal_credit": 0,
            "manifest_authorized": False, "C27R2": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


NORMAL_ARGUMENTS = [
    "mode", "override_map", "expect_override_map_file_sha256",
    "expect_override_map_object_sha256", "python", "expect_python_sha256",
    "expect_validator_sha256", "expected_python_hash_seed",
    "actual_terminal_relative", "actual_base_relative",
    "expect_actual_terminal_root_sha256",
    "expect_actual_terminal_receipt_file_sha256",
    "expect_actual_terminal_receipt_object_sha256", "gate_relative",
    "seed1_edge_relative", "expect_seed1_edge_sha256",
    "seed2_edge_relative", "expect_seed2_edge_sha256",
    "frozen_c15_relative", "expect_frozen_c15_sha256",
    "expect_gate_receipt_file_sha256", "expect_gate_receipt_object_sha256",
    "expect_gate_root_file_sha256", "expect_gate_root_object_sha256",
    "core_control_relative", "candidate_relative", "verifier_output_relative",
    "attack_work_relative", "producer_run_relative", "verifier_run_relative",
    "attack_run_relative", "expect_core_receipt_file_sha256",
    "expect_core_receipt_object_sha256", "core_unit", "core_invocation_id",
    "service_query_fixture",
    "cold_control_relative", "cold_output_relative", "cold_run_relative",
    "expect_cold_receipt_file_sha256", "expect_cold_receipt_object_sha256",
    "cold_helper_relative", "expect_cold_helper_sha256",
    "cold_python_hash_seed", "evidence_relative", "evidence_builder_relative",
    "expect_evidence_builder_sha256",
    "expect_evidence_file_sha256", "expect_evidence_object_sha256",
    "future_outer_relative", "future_seal_relative", "future_terminal_relative",
    "out_file",
]


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--mode", choices=("formal", "private"))
    value.add_argument("--override-map")
    value.add_argument("--expect-override-map-file-sha256")
    value.add_argument("--expect-override-map-object-sha256")
    value.add_argument("--case-root")
    value.add_argument("--fixture-barrier", action="store_true")
    value.add_argument("--python")
    value.add_argument("--expect-python-sha256")
    value.add_argument("--expect-validator-sha256")
    value.add_argument("--expected-python-hash-seed")
    value.add_argument("--actual-terminal-relative")
    value.add_argument("--actual-base-relative")
    value.add_argument("--expect-actual-terminal-root-sha256")
    value.add_argument("--expect-actual-terminal-receipt-file-sha256")
    value.add_argument("--expect-actual-terminal-receipt-object-sha256")
    value.add_argument("--seed1-edge-relative")
    value.add_argument("--expect-seed1-edge-sha256")
    value.add_argument("--seed2-edge-relative")
    value.add_argument("--expect-seed2-edge-sha256")
    value.add_argument("--frozen-c15-relative")
    value.add_argument("--expect-frozen-c15-sha256")
    value.add_argument("--gate-relative")
    value.add_argument("--expect-gate-receipt-file-sha256")
    value.add_argument("--expect-gate-receipt-object-sha256")
    value.add_argument("--expect-gate-root-file-sha256")
    value.add_argument("--expect-gate-root-object-sha256")
    value.add_argument("--core-control-relative")
    value.add_argument("--candidate-relative")
    value.add_argument("--verifier-output-relative")
    value.add_argument("--attack-work-relative")
    value.add_argument("--producer-run-relative")
    value.add_argument("--verifier-run-relative")
    value.add_argument("--attack-run-relative")
    value.add_argument("--expect-core-receipt-file-sha256")
    value.add_argument("--expect-core-receipt-object-sha256")
    value.add_argument("--core-unit")
    value.add_argument("--core-invocation-id")
    value.add_argument("--service-query-fixture",
                       choices=("fixed", "missing", "wrong"))
    value.add_argument("--cold-control-relative")
    value.add_argument("--cold-output-relative")
    value.add_argument("--cold-run-relative")
    value.add_argument("--expect-cold-receipt-file-sha256")
    value.add_argument("--expect-cold-receipt-object-sha256")
    value.add_argument("--expect-cold-helper-sha256")
    value.add_argument("--cold-helper-relative")
    value.add_argument("--cold-python-hash-seed", default="30662727")
    value.add_argument("--evidence-relative")
    value.add_argument("--evidence-builder-relative")
    value.add_argument("--expect-evidence-builder-sha256")
    value.add_argument("--expect-evidence-file-sha256")
    value.add_argument("--expect-evidence-object-sha256")
    value.add_argument("--future-outer-relative")
    value.add_argument("--future-seal-relative")
    value.add_argument("--future-terminal-relative")
    value.add_argument("--out-file")
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        if args.self_test:
            result = self_test()
        else:
            need(all(getattr(args, name) is not None for name in NORMAL_ARGUMENTS),
                 "all normal arguments required")
            need(all(valid_sha(getattr(args, name)) for name in (
                "expect_override_map_file_sha256",
                "expect_override_map_object_sha256", "expect_python_sha256",
                "expect_validator_sha256", "expect_actual_terminal_root_sha256",
                "expect_actual_terminal_receipt_file_sha256",
                "expect_actual_terminal_receipt_object_sha256",
                "expect_seed1_edge_sha256", "expect_seed2_edge_sha256",
                "expect_frozen_c15_sha256",
                "expect_gate_receipt_file_sha256", "expect_gate_receipt_object_sha256",
                "expect_gate_root_file_sha256", "expect_gate_root_object_sha256",
                "expect_core_receipt_file_sha256", "expect_core_receipt_object_sha256",
                "expect_cold_receipt_file_sha256", "expect_cold_receipt_object_sha256",
                "expect_cold_helper_sha256", "expect_evidence_file_sha256",
                "expect_evidence_object_sha256",
                "expect_evidence_builder_sha256")),
                "all SHA arguments lowercase exact")
            result = execute(args)
            output_path = Path(args.out_file)
            write_once(output_path, canonical(result) + b"\n")
            reopened = decode_document(
                capture_direct(output_path, output_path.parent,
                               64 << 20)[0], "validation_sha256")
            need(reopened == result,
                 "reopened canonical validator output object closure")
        sys.stdout.buffer.write(canonical({"schema": result["schema"],
            "status": result["status"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM"}) + b"\n")
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
