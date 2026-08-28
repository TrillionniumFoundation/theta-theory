#!/usr/bin/env python3
"""Create and hold the audited one-shot lock, then exec the formal v8 runner.

This launcher is append-only and mints no authority.  Its launch plan closes
over every non-lock runner argument and four explicit lock placeholders before
the lock exists.  The lock then closes over the plan, so no digest cycle is
introduced.  The inherited exclusive descriptor remains held across execve
for the runner's whole publication window.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).absolute().parent.parent
AUDIT = ROOT / ".cm2-runtime/audit"
SELF = Path(__file__).absolute()
PYTHON = Path("/usr/bin/python3.12")
RUNNER = ROOT / (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_integrity_fixture_runner_v8.py")
VALIDATOR = ROOT / (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_repair_boundary_independent_validator_v8.py")
CASE_WRAPPER = ROOT / (
    "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
    "rebuild_v2_release_integrity_case_transaction_wrapper_v2.py")

PYTHON_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
RUNNER_SHA256 = "530b060e5f0221b3a9cd4a05545a37d62e53217b4148344c35e387e969a24e80"
VALIDATOR_SHA256 = "9c24ec0f3c226db94bc6fc6d72e0d9fd627f822b82b90df684f038d420cf7464"
CASE_WRAPPER_SHA256 = "90f2fbf9f07eda2006829cd895dd3aee982fa81b3c30b9c4d8b2d48f777ea784"

PYTHON_HASH_SEED = "30662790"
EXACT_ENVIRONMENT = {
    "PATH": "/usr/bin:/bin",
    "LANG": "C",
    "LC_ALL": "C",
    "PYTHONHASHSEED": PYTHON_HASH_SEED,
}

PREFIX = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2.")
PLAN_SCHEMA = PREFIX + "release-integrity-v8-one-shot-launch-plan.v1"
PLAN_STATUS = (
    "FROZEN_C27R2_RELEASE_INTEGRITY_V8_73_PLUS_8_ONE_SHOT_LAUNCH_PLAN__"
    "ZERO_CREDIT")
PUBLICATION_LOCK_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-repair."
    "publication-lock.v1")
PUBLICATION_LOCK_STATUS = "FROZEN_ONE_SHOT_PUBLICATION_LOCK__NO_AUTHORITY"
PUBLICATION_LOCK_PROTOCOL = "FLOCK_EXCLUSIVE_WHOLE_PUBLICATION_WINDOW_V1"
SELF_TEST_SCHEMA = PLAN_SCHEMA + ".self-test"
SELF_TEST_STATUS = (
    "PASS_CLOSED_PLAN_EXACT10_LOCK_FULL_V8_ARGV_AND_73_PLUS_8_INVENTORY_"
    "TEMP_ONLY__ZERO_CREDIT")

VALIDATOR_NEGATIVE_INVENTORY_SHA256 = (
    "2e6cfa731d4423f99e7a2d4b886987df7522fd66a70a60b9e7d931db8d04c57c")
PUBLICATION_LOCK_PREFLIGHT_INVENTORY_SHA256 = (
    "92add6db3116e10fe54cda24ce5d61288bb47622e6956f1353898ba707811c5d")

CASE_NAMES = [
    "wrong-core-unit",
    "wrong-core-invocation",
    "actual-terminal-directory-swap",
    "actual-base-directory-swap",
    "actual-terminal-receipt-file-pin",
    "actual-terminal-receipt-object-pin",
    "actual-terminal-root-pin",
    "actual-terminal-PASS-drift",
    "actual-payload-manifest-drift",
    "post-actual-gate-execution-receipt-drift",
    "post-actual-gate-PASS-drift",
    "seed1-identical-bytes-new-inode",
    "seed2-edge-drift",
    "frozen-C15-drift",
    "core-transaction-receipt-coherent-reclosure",
    "core-pinset-actual-pin-lie",
    "producer-command-spec-lie",
    "verifier-command-spec-seed-and-pin-lie",
    "attack-command-spec-lie",
    "candidate-result-census-coherent-reclosure",
    "candidate-truncated-gzip",
    "candidate-missing-member",
    "candidate-extra-member",
    "candidate-symlink",
    "candidate-hardlink",
    "independent-verification-coherent-reclosure",
    "core-attacks-coherent-reclosure",
    "producer-nonzero-exit",
    "verifier-signal",
    "attack-nonempty-stderr",
    "process-input-post-drift",
    "process-output-validation-drift",
    "cold-historical-verification-drift",
    "cold-receipt-coherent-reclosure",
    "evidence-inventory-member-drift",
    "wrong-PYTHONHASHSEED",
    "missing-isolated-python-flag",
    "atomic-replace-same-bytes-new-inode",
    "post-hash-content-TOCTOU",
    "payload-manifest-reorder",
    "manifest-duplicate",
    "manifest-traversal",
    "root-member-substitution",
    "outer-fake-release-count-coherent-reclosure",
    "future-seal-fake-authority",
    "terminal-byte-mismatch",
    "core-PASS-drift",
    "core-control-extra-member",
    "core-control-runner-stdout-drift",
    "gate-extra-member",
    "gate-stage-stdout-drift",
    "producer-run-extra-member",
    "producer-run-PASS-drift",
    "producer-run-stdout-drift",
    "producer-run-timing-drift",
    "producer-run-runner-start-drift",
    "cold-control-PASS-drift",
    "cold-control-runner-stdout-drift",
    "cold-run-extra-member",
    "cold-run-PASS-drift",
    "cold-run-stdout-drift",
    "cold-run-timing-drift",
    "cold-run-runner-start-drift",
    "producer-command-spec-extra-argv",
    "core-spec-extra-input",
    "cold-spec-extra-input",
    "attestation-extra-path",
    "attestation-omitted-path",
    "service-query-missing-bus-route",
    "service-query-wrong-bus-route",
    "cold-authority-missing-key",
    "cold-authority-extra-key",
    "cold-authority-service-projection-mismatch",
]

LOCK_PREFLIGHT_CASE_NAMES = [
    "missing-lock-arguments",
    "bad-inherited-fd",
    "wrong-inode-path-substitution",
    "unlocked-inherited-fd",
    "shared-only-inherited-lock",
    "symlink-or-nonsingleton-lock-path",
    "lock-pin-or-stat-drift",
    "early-close-or-unlock",
]

VALIDATOR_COMMON = (
    "python", "expect_python_sha256", "expect_validator_sha256",
    "expected_python_hash_seed", "actual_terminal_relative",
    "actual_base_relative", "expect_actual_terminal_root_sha256",
    "expect_actual_terminal_receipt_file_sha256",
    "expect_actual_terminal_receipt_object_sha256", "seed1_edge_relative",
    "expect_seed1_edge_sha256", "seed2_edge_relative",
    "expect_seed2_edge_sha256", "frozen_c15_relative",
    "expect_frozen_c15_sha256", "gate_relative",
    "expect_gate_receipt_file_sha256", "expect_gate_receipt_object_sha256",
    "expect_gate_root_file_sha256", "expect_gate_root_object_sha256",
    "core_control_relative", "candidate_relative", "verifier_output_relative",
    "attack_work_relative", "producer_run_relative", "verifier_run_relative",
    "attack_run_relative", "expect_core_receipt_file_sha256",
    "expect_core_receipt_object_sha256", "core_unit", "core_invocation_id",
    "core_exec_start_property_sha256", "core_fragment_path",
    "core_fragment_file_sha256", "core_fragment_stat9_json",
    "service_query_fixture", "cold_control_relative",
    "cold_output_relative", "cold_run_relative",
    "expect_cold_receipt_file_sha256", "expect_cold_receipt_object_sha256",
    "cold_helper_relative", "expect_cold_helper_sha256",
    "cold_python_hash_seed", "evidence_relative", "evidence_builder_relative",
    "expect_evidence_builder_sha256", "expect_evidence_file_sha256",
    "expect_evidence_object_sha256", "future_outer_relative",
    "future_seal_relative", "future_terminal_relative",
)

LOCK_PLACEHOLDERS = [
    {"option": "--publication-lock-file-sha256",
     "placeholder": "<PUBLICATION_LOCK_FILE_SHA256>"},
    {"option": "--publication-lock-object-sha256",
     "placeholder": "<PUBLICATION_LOCK_OBJECT_SHA256>"},
    {"option": "--publication-lock-stat9-json",
     "placeholder": "<PUBLICATION_LOCK_STAT9_JSON>"},
    {"option": "--publication-lock-fd",
     "placeholder": "<PUBLICATION_LOCK_FD>"},
]


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


def fingerprint(value: os.stat_result) -> list[int]:
    return [value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_uid, value.st_gid]


def capture_file(path: Path, maximum: int = 1 << 30) \
        -> tuple[bytes, dict[str, Any]]:
    path = path.absolute()
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 <= before.st_size <= maximum,
             "captured path exact regular singleton")
        state = hashlib.sha256()
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            state.update(block)
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    need(fingerprint(before) == fingerprint(after) == fingerprint(current),
         "captured path stable full9stat")
    payload = b"".join(chunks)
    need(len(payload) == before.st_size, "captured path exact size")
    return payload, {"path": str(path), "sha256": state.hexdigest(),
                     "size": before.st_size,
                     "stat_fingerprint": fingerprint(before)}


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                         | getattr(os, "O_CLOEXEC", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_once(path: Path, payload: bytes, mode: int) -> dict[str, Any]:
    need(path.parent.is_dir() and not path.exists() and not path.is_symlink(),
         "fresh one-shot output path")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), mode)
    try:
        os.fchmod(descriptor, mode)
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            need(written > 0, "one-shot write progress")
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    fsync_directory(path.parent)
    record = capture_file(path, 1 << 20)[1]
    need(stat.S_IMODE(record["stat_fingerprint"][2]) == mode,
         "one-shot exact mode")
    return record


def strict_closed_document(path: Path, closure: str) -> dict[str, Any]:
    payload = capture_file(path, 1 << 20)[0]
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "canonical one-newline document")
    value = json.loads(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical exact JSON document")
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body), "document object closure")
    return value


def verify_exact_runtime() -> None:
    need(Path(sys.executable).absolute() == PYTHON
         and sys.flags.isolated == 1 and sys.dont_write_bytecode,
         "launcher exact /usr/bin/python3.12 -I -B runtime")
    need(dict(os.environ) == EXACT_ENVIRONMENT,
         "launcher exact four-variable environment")


def verify_inventories() -> None:
    need(len(CASE_NAMES) == 73 and len(set(CASE_NAMES)) == 73,
         "exact unique 73-case inventory")
    need(len(LOCK_PREFLIGHT_CASE_NAMES) == 8
         and len(set(LOCK_PREFLIGHT_CASE_NAMES)) == 8,
         "exact unique 8-lock inventory")
    need(digest({"validator_negative_case_count": 73,
                 "ordered_validator_negative_case_names": CASE_NAMES})
             == VALIDATOR_NEGATIVE_INVENTORY_SHA256,
         "exact ordered validator inventory digest")
    need(digest({"publication_lock_preflight_case_count": 8,
                 "ordered_publication_lock_preflight_case_names":
                     LOCK_PREFLIGHT_CASE_NAMES})
             == PUBLICATION_LOCK_PREFLIGHT_INVENTORY_SHA256,
         "exact ordered lock inventory digest")
    need(CASE_NAMES[-3:] == ["cold-authority-missing-key",
                            "cold-authority-extra-key",
                            "cold-authority-service-projection-mismatch"],
         "three production cold-authority negatives appended")


def validate_launch_id(value: Any) -> str:
    need(type(value) is str
         and re.fullmatch(
             r"c27r2-release-repair-integrity-v8-[A-Za-z0-9][A-Za-z0-9._-]{7,70}",
             value) is not None,
         "exact formal one-shot launch-id syntax")
    return value


def launch_paths(audit: Path, launch_id: str) -> dict[str, Path]:
    validate_launch_id(launch_id)
    paths = {
        "work": audit / launch_id,
        "publication_control": audit / (launch_id + "-control"),
        "future_outer": audit / (launch_id + "-outer"),
        "future_seal": audit / (launch_id + "-seal"),
        "future_terminal": audit / (launch_id + "-terminal"),
    }
    need(len(set(paths.values())) == 5
         and all(path.parent == audit for path in paths.values()),
         "five distinct direct audit siblings")
    return paths


def assert_fresh_paths(paths: dict[str, Path]) -> None:
    need(set(paths) == {"work", "publication_control", "future_outer",
                        "future_seal", "future_terminal"},
         "exact fresh-path roles")
    for role, path in paths.items():
        need(not path.exists() and not path.is_symlink(),
             "fresh absent direct audit sibling:" + role)


def source_pin_records(expect_self_sha256: str) -> dict[str, dict[str, Any]]:
    expected = {
        "launcher": (SELF, expect_self_sha256),
        "python": (PYTHON, PYTHON_SHA256),
        "runner": (RUNNER, RUNNER_SHA256),
        "validator": (VALIDATOR, VALIDATOR_SHA256),
        "case_wrapper": (CASE_WRAPPER, CASE_WRAPPER_SHA256),
    }
    result: dict[str, dict[str, Any]] = {}
    for role, (path, expected_sha) in expected.items():
        need(valid_sha(expected_sha), "source lowercase SHA pin:" + role)
        record = capture_file(path)[1]
        need(record["sha256"] == expected_sha, "frozen source SHA:" + role)
        frozen = record["stat_fingerprint"]
        if role == "python":
            need(stat.S_IMODE(frozen[2]) == 0o755
                 and frozen[3] == 1 and frozen[7:] == [0, 0],
                 "frozen Python exact root:root 0755 singleton")
        else:
            need(stat.S_IMODE(frozen[2]) == 0o444
                 and frozen[3] == 1 and frozen[7:] == [1000, 1000],
                 "frozen source exact uid/gid 1000 mode 0444 singleton:" + role)
        result[role] = record
    return result


def source_pin_projection(records: dict[str, dict[str, Any]]) \
        -> dict[str, dict[str, str]]:
    need(set(records) == {"launcher", "python", "runner", "validator",
                          "case_wrapper"}, "exact source pin roles")
    return {role: {"path": value["path"], "sha256": value["sha256"]}
            for role, value in sorted(records.items())}


def validator_common_values(paths: dict[str, Path],
                            authority_root: Path = ROOT) -> dict[str, str]:
    relative = lambda path: str(path.relative_to(authority_root))
    values = {
        "python": str(PYTHON),
        "expect_python_sha256": PYTHON_SHA256,
        "expect_validator_sha256": VALIDATOR_SHA256,
        "expected_python_hash_seed": PYTHON_HASH_SEED,
        "actual_terminal_relative": (
            ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-"
            "dual-seed-zero-credit-seal-v2-20260808T1544-terminal-replay"),
        "actual_base_relative": (
            ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-"
            "dual-seed-zero-credit-seal-v2-20260808T1544"),
        "expect_actual_terminal_root_sha256":
            "c46609c00ede1308d160aa724c3ee7c9387d0329c82be7d01d09d12a3ddaadae",
        "expect_actual_terminal_receipt_file_sha256":
            "8fc365cc487d8f74695a858afd5ee26efc514547631960a9e0bc6dc8cf597cb1",
        "expect_actual_terminal_receipt_object_sha256":
            "2a6d3b70667742cd5dbeacead0ec8a5a11429a2c7817d2809fd65e597b394222",
        "seed1_edge_relative": (
            ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-"
            "seed30660101-p0r2-20260808T1432/full_component_edge_union.jsonl.gz"),
        "expect_seed1_edge_sha256":
            "5bc29ef85bc57f467bee5ba94cd12e31950c2c940928cb57498421200c95bec0",
        "seed2_edge_relative": (
            ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-"
            "seed30660991-p0r2-20260808T1432/full_component_edge_union.jsonl.gz"),
        "expect_seed2_edge_sha256":
            "5bc29ef85bc57f467bee5ba94cd12e31950c2c940928cb57498421200c95bec0",
        "frozen_c15_relative": (
            "deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_"
            "freeze_member_component_ledger.jsonl.gz"),
        "expect_frozen_c15_sha256":
            "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
        "gate_relative": (
            ".cm2-runtime/audit/c27r2-post-actual-v2-rebuild-gate-v3-r2-"
            "zero-credit-20260808T164429"),
        "expect_gate_receipt_file_sha256":
            "fb1feeeee61246aedd8aeb78c4c0a29a6a0ceb93084895cd84c951279d2cc5d4",
        "expect_gate_receipt_object_sha256":
            "4afaff6f0dd51b5119fa7de7689abb7e35865c382b643a12a8eb82fdff5e1b71",
        "expect_gate_root_file_sha256":
            "1269dd8dfa7b070efcd755d7c2b76f17a3647b16d7e75304a157837cb2ffc9a9",
        "expect_gate_root_object_sha256":
            "0c6c81aa6fdb58855c16f074cbb161df211a34d1e760c00dbf6fc8cd6a55fbcd",
        "core_control_relative": (
            ".cm2-runtime/audit/c27r2-source-g-authority-v2-v6-formal-r2-"
            "20260808T180523-control"),
        "candidate_relative": (
            ".cm2-runtime/audit/c27r2-source-g-authority-v2-v6-formal-r2-"
            "20260808T180523-candidate"),
        "verifier_output_relative": (
            ".cm2-runtime/audit/c27r2-source-g-authority-v2-v6-formal-r2-"
            "20260808T180523-verifier-output"),
        "attack_work_relative": (
            ".cm2-runtime/audit/c27r2-source-g-authority-v2-v6-formal-r2-"
            "20260808T180523-attack-work"),
        "producer_run_relative": (
            ".cm2-runtime/audit/c27r2-source-g-authority-v2-v6-formal-r2-"
            "20260808T180523-producer-run"),
        "verifier_run_relative": (
            ".cm2-runtime/audit/c27r2-source-g-authority-v2-v6-formal-r2-"
            "20260808T180523-verifier-run"),
        "attack_run_relative": (
            ".cm2-runtime/audit/c27r2-source-g-authority-v2-v6-formal-r2-"
            "20260808T180523-attack-run"),
        "expect_core_receipt_file_sha256":
            "4104edc46bb130bae530a990609d5053bc9d7f675e4e3587e88b8327394c5796",
        "expect_core_receipt_object_sha256":
            "783d05cb9c01a2049a03112f9412bab787b5fad2c81fba1855d9cca4dabcb016",
        "core_unit": (
            "cm2-c27r2-source-g-authority-v2-v6-formal-r2-"
            "20260808T180523.service"),
        "core_invocation_id": "aa82e1c6611f4910ae80b94307fb9ca9",
        "core_exec_start_property_sha256":
            "1333b53bd5ee08623d90f42dd847c141eaedf889d2b906ea0cc1493cf2ebc509",
        "core_fragment_path": (
            "/run/user/1000/systemd/transient/cm2-c27r2-source-g-authority-v2-"
            "v6-formal-r2-20260808T180523.service"),
        "core_fragment_file_sha256":
            "51fb8cc7ada292e0e656c41d2e11a7d2c78610750d3af73453bff08840af05b5",
        "core_fragment_stat9_json":
            "[68,15456,33188,1,3363,1786183593722628652,"
            "1786183593722628652,1000,1000]",
        "service_query_fixture": "fixed",
        "cold_control_relative": (
            ".cm2-runtime/audit/c27r2-release-cold-v4-r1-"
            "20260808T191556Z-control"),
        "cold_output_relative": (
            ".cm2-runtime/audit/c27r2-release-cold-v4-r1-"
            "20260808T191556Z-output"),
        "cold_run_relative": (
            ".cm2-runtime/audit/c27r2-release-cold-v4-r1-"
            "20260808T191556Z-run"),
        "expect_cold_receipt_file_sha256":
            "2b43a4be6285f04ad4f6a94dd005079477d1c4819135b9b44af6d791ffe94502",
        "expect_cold_receipt_object_sha256":
            "66df67907f836947b9633644a697682aebdf1b313b7691ff241f4687b69c6ac6",
        "cold_helper_relative": (
            "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
            "rebuild_v2_release_cold_replay_runner_v4.py"),
        "expect_cold_helper_sha256":
            "3d44ebbc37449192f975e3687284c6e74285f7d7f564e40ef12e37232f0ec838",
        "cold_python_hash_seed": "30662727",
        "evidence_relative": (
            ".cm2-runtime/audit/c27r2-release-chain-v1-formal-r1-"
            "20260808T183910-evidence"),
        "evidence_builder_relative": (
            "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
            "rebuild_v2_release_evidence_bundle_builder_v1.py"),
        "expect_evidence_builder_sha256":
            "beb339c6fd8ab0b5b3b4effde8563c8b8a30eec2733e5a3bdf4b85038cec8fe3",
        "expect_evidence_file_sha256":
            "8efd9e85ff5d9d9718fc39aa2c09b4cf1cc48146502081f4639ca49695288396",
        "expect_evidence_object_sha256":
            "2639eaace81b3fff15a433680d41457f492c48c73e6309b724b174c6102751f6",
        "future_outer_relative": relative(paths["future_outer"]),
        "future_seal_relative": relative(paths["future_seal"]),
        "future_terminal_relative": relative(paths["future_terminal"]),
    }
    need(tuple(values) == VALIDATOR_COMMON,
         "full historical VALIDATOR_COMMON order and values")
    need(values["service_query_fixture"] == "fixed",
         "fixed service-query fixture")
    need(all(type(value) is str and value != "" for value in values.values()),
         "all validator common values exact strings")
    return values


def runner_nonlock_argv(paths: dict[str, Path],
                        authority_root: Path = ROOT) -> list[str]:
    lock_path = paths["publication_control"] / "publication_lock.json"
    command = [
        str(PYTHON), "-I", "-B", str(RUNNER),
        "--validator", str(VALIDATOR),
        "--case-wrapper", str(CASE_WRAPPER),
        "--expect-case-wrapper-sha256", CASE_WRAPPER_SHA256,
        "--expect-runner-sha256", RUNNER_SHA256,
        "--work-dir", str(paths["work"]),
        "--out-file", str(paths["work"] / "fixture_receipt.json"),
        "--control-timeout-seconds", "21600",
        "--case-timeout-seconds", "21600",
        "--publication-lock-path", str(lock_path),
    ]
    values = validator_common_values(paths, authority_root)
    for name in VALIDATOR_COMMON:
        command.extend(["--" + name.replace("_", "-"), values[name]])
    dynamic_options = {item["option"] for item in LOCK_PLACEHOLDERS}
    need(not dynamic_options.intersection(command),
         "nonlock argv excludes four dynamic lock options")
    need(all(type(item) is str and item != "" for item in command)
         and command[:4] == [str(PYTHON), "-I", "-B", str(RUNNER)],
         "exact isolated runner argv prefix")
    for name in VALIDATOR_COMMON:
        need(command.count("--" + name.replace("_", "-")) == 1,
             "validator common option exactly once:" + name)
    need(command.count("--control-timeout-seconds") == 1
         and command[command.index("--control-timeout-seconds") + 1] == "21600"
         and command.count("--case-timeout-seconds") == 1
         and command[command.index("--case-timeout-seconds") + 1] == "21600",
         "exact 21600-second timeouts")
    return command


def build_plan(launch_id: str, paths: dict[str, Path],
               source_pins: dict[str, dict[str, str]],
               authority_root: Path = ROOT) -> dict[str, Any]:
    nonlock = runner_nonlock_argv(paths, authority_root)
    body = {
        "schema": PLAN_SCHEMA,
        "status": PLAN_STATUS,
        "one_shot_launch_id": launch_id,
        "launcher": source_pins["launcher"],
        "source_pins": source_pins,
        "work_dir": str(paths["work"]),
        "out_file": str(paths["work"] / "fixture_receipt.json"),
        "publication_control_dir": str(paths["publication_control"]),
        "publication_lock_path": str(
            paths["publication_control"] / "publication_lock.json"),
        "future_authority_paths": [str(paths["future_outer"]),
                                   str(paths["future_seal"]),
                                   str(paths["future_terminal"])],
        "runner_argv_nonlock": nonlock,
        "publication_lock_argv_placeholders": LOCK_PLACEHOLDERS,
        "publication_lock_argument_position": "append-after-nonlock-argv",
        "publication_lock_digest_cycle": False,
        "exact_environment": EXACT_ENVIRONMENT,
        "validator_common_argument_order": list(VALIDATOR_COMMON),
        "control_timeout_seconds": 21_600,
        "case_timeout_seconds": 21_600,
        "validator_negative_case_count": 73,
        "ordered_validator_negative_case_names": CASE_NAMES,
        "ordered_validator_negative_inventory_sha256":
            VALIDATOR_NEGATIVE_INVENTORY_SHA256,
        "publication_lock_preflight_case_count": 8,
        "ordered_publication_lock_preflight_case_names":
            LOCK_PREFLIGHT_CASE_NAMES,
        "ordered_publication_lock_preflight_inventory_sha256":
            PUBLICATION_LOCK_PREFLIGHT_INVENTORY_SHA256,
        "total_integrity_check_count": 81,
        "formal_credit": 0,
        "manifest_authorized": False,
        "authority_minted": False,
    }
    value = dict(body)
    value["plan_sha256"] = digest(body)
    validate_plan(value, launch_id, paths, source_pins, authority_root)
    return value


def validate_plan(value: dict[str, Any], launch_id: str,
                  paths: dict[str, Path],
                  source_pins: dict[str, dict[str, str]],
                  authority_root: Path = ROOT) -> None:
    expected_keys = {
        "schema", "status", "one_shot_launch_id", "launcher", "source_pins",
        "work_dir", "out_file", "publication_control_dir",
        "publication_lock_path", "future_authority_paths",
        "runner_argv_nonlock", "publication_lock_argv_placeholders",
        "publication_lock_argument_position", "publication_lock_digest_cycle",
        "exact_environment", "validator_common_argument_order",
        "control_timeout_seconds", "case_timeout_seconds",
        "validator_negative_case_count", "ordered_validator_negative_case_names",
        "ordered_validator_negative_inventory_sha256",
        "publication_lock_preflight_case_count",
        "ordered_publication_lock_preflight_case_names",
        "ordered_publication_lock_preflight_inventory_sha256",
        "total_integrity_check_count", "formal_credit", "manifest_authorized",
        "authority_minted", "plan_sha256",
    }
    need(type(value) is dict and set(value) == expected_keys,
         "launch plan exact closed keyset")
    body = dict(value)
    claim = body.pop("plan_sha256")
    need(valid_sha(claim) and claim == digest(body), "launch plan object closure")
    need(value["schema"] == PLAN_SCHEMA and value["status"] == PLAN_STATUS
         and value["one_shot_launch_id"] == launch_id,
         "launch plan exact identity")
    need(value["launcher"] == source_pins["launcher"]
         and value["source_pins"] == source_pins,
         "launch plan exact current source pins")
    need(value["work_dir"] == str(paths["work"])
         and value["out_file"] == str(paths["work"] / "fixture_receipt.json")
         and value["publication_control_dir"]
             == str(paths["publication_control"])
         and value["publication_lock_path"]
             == str(paths["publication_control"] / "publication_lock.json")
         and value["future_authority_paths"]
             == [str(paths["future_outer"]), str(paths["future_seal"]),
                 str(paths["future_terminal"])],
         "launch plan exact fresh path model")
    need(value["runner_argv_nonlock"]
             == runner_nonlock_argv(paths, authority_root)
         and value["publication_lock_argv_placeholders"] == LOCK_PLACEHOLDERS
         and value["publication_lock_argument_position"]
             == "append-after-nonlock-argv"
         and value["publication_lock_digest_cycle"] is False,
         "launch plan nonlock argv and four no-cycle placeholders")
    need(value["exact_environment"] == EXACT_ENVIRONMENT
         and value["validator_common_argument_order"] == list(VALIDATOR_COMMON)
         and value["control_timeout_seconds"] == 21_600
         and value["case_timeout_seconds"] == 21_600,
         "launch plan exact runtime and full validator option order")
    need(value["validator_negative_case_count"] == 73
         and value["ordered_validator_negative_case_names"] == CASE_NAMES
         and value["ordered_validator_negative_inventory_sha256"]
             == VALIDATOR_NEGATIVE_INVENTORY_SHA256
         and value["publication_lock_preflight_case_count"] == 8
         and value["ordered_publication_lock_preflight_case_names"]
             == LOCK_PREFLIGHT_CASE_NAMES
         and value["ordered_publication_lock_preflight_inventory_sha256"]
             == PUBLICATION_LOCK_PREFLIGHT_INVENTORY_SHA256
         and value["total_integrity_check_count"] == 81,
         "launch plan exact 73 plus 8 inventories")
    need(value["formal_credit"] == 0
         and value["manifest_authorized"] is False
         and value["authority_minted"] is False,
         "launch plan zero-credit policy")


def build_lock(launch_id: str, plan_record: dict[str, Any],
               plan: dict[str, Any]) -> dict[str, Any]:
    body = {
        "schema": PUBLICATION_LOCK_SCHEMA,
        "status": PUBLICATION_LOCK_STATUS,
        "protocol": PUBLICATION_LOCK_PROTOCOL,
        "one_shot_launch_id": launch_id,
        "plan_file_sha256": plan_record["sha256"],
        "plan_object_sha256": plan["plan_sha256"],
        "formal_credit": 0,
        "manifest_authorized": False,
        "authority_minted": False,
    }
    value = dict(body)
    value["publication_lock_sha256"] = digest(body)
    validate_lock(value, launch_id, plan_record, plan)
    return value


def validate_lock(value: dict[str, Any], launch_id: str,
                  plan_record: dict[str, Any], plan: dict[str, Any]) -> None:
    need(type(value) is dict and set(value) == {
        "schema", "status", "protocol", "one_shot_launch_id",
        "plan_file_sha256", "plan_object_sha256", "formal_credit",
        "manifest_authorized", "authority_minted", "publication_lock_sha256",
    }, "publication lock exact10 keyset")
    body = dict(value)
    claim = body.pop("publication_lock_sha256")
    need(valid_sha(claim) and claim == digest(body),
         "publication lock object closure")
    need(value["schema"] == PUBLICATION_LOCK_SCHEMA
         and value["status"] == PUBLICATION_LOCK_STATUS
         and value["protocol"] == PUBLICATION_LOCK_PROTOCOL
         and value["one_shot_launch_id"] == launch_id
         and value["plan_file_sha256"] == plan_record["sha256"]
         and value["plan_object_sha256"] == plan["plan_sha256"]
         and value["formal_credit"] == 0
         and value["manifest_authorized"] is False
         and value["authority_minted"] is False,
         "publication lock exact plan pins and zero-credit policy")


def inherited_fd_at_least_three(
        descriptor: int, duplicate: Any = fcntl.fcntl,
        close: Any = os.close) -> int:
    need(type(descriptor) is int and descriptor >= 0,
         "publication lock open descriptor syntax")
    if descriptor >= 3:
        return descriptor
    operation = getattr(fcntl, "F_DUPFD_CLOEXEC", fcntl.F_DUPFD)
    promoted = duplicate(descriptor, operation, 3)
    need(type(promoted) is int and promoted >= 3,
         "publication lock promoted inherited fd >=3")
    close(descriptor)
    return promoted


def open_and_lock(path: Path, expected: dict[str, Any]) \
        -> tuple[int, dict[str, Any]]:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        descriptor = inherited_fd_at_least_three(descriptor)
        current = os.fstat(descriptor)
        path_stat = os.stat(path, follow_symlinks=False)
        need(stat.S_ISREG(current.st_mode) and current.st_nlink == 1
             and fingerprint(current) == fingerprint(path_stat)
             and (current.st_dev, current.st_ino)
                 == tuple(expected["stat_fingerprint"][:2]),
             "publication lock inherited fd/path exact singleton inode")
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        os.set_inheritable(descriptor, True)
        need(os.get_inheritable(descriptor),
             "publication lock descriptor inheritable")
        for operation in (fcntl.LOCK_EX, fcntl.LOCK_SH):
            probe = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                            | getattr(os, "O_NOFOLLOW", 0))
            try:
                try:
                    fcntl.flock(probe, operation | fcntl.LOCK_NB)
                except BlockingIOError:
                    pass
                else:
                    fcntl.flock(probe, fcntl.LOCK_UN)
                    raise Rejected("separate publication lock probe acquired")
            finally:
                os.close(probe)
        final = os.fstat(descriptor)
        need(fingerprint(final) == expected["stat_fingerprint"],
             "publication lock unchanged after exclusive acquisition")
        return descriptor, {"path": str(path),
                            "file_sha256": expected["sha256"],
                            "stat_fingerprint": fingerprint(final)}
    except BaseException:
        os.close(descriptor)
        raise


def final_runner_argv(nonlock: list[str], lock: dict[str, Any],
                      lock_record: dict[str, Any], descriptor: int) -> list[str]:
    values = {
        "--publication-lock-file-sha256": lock_record["sha256"],
        "--publication-lock-object-sha256": lock["publication_lock_sha256"],
        "--publication-lock-stat9-json": canonical(
            lock_record["stat_fingerprint"]).decode("ascii"),
        "--publication-lock-fd": str(descriptor),
    }
    need(list(values) == [item["option"] for item in LOCK_PLACEHOLDERS]
         and all(item["placeholder"].startswith("<PUBLICATION_LOCK_")
                 for item in LOCK_PLACEHOLDERS),
         "exact ordered four dynamic lock values")
    command = list(nonlock)
    for option in (item["option"] for item in LOCK_PLACEHOLDERS):
        command.extend([option, values[option]])
    need(len(command) == len(nonlock) + 8
         and all(command.count(option) == 1 for option in values),
         "four lock arguments appended exactly once")
    return command


def self_test(expect_self_sha256: str) -> dict[str, Any]:
    verify_inventories()
    duplicate_calls: list[tuple[int, int, int]] = []
    closed_fds: list[int] = []
    def fake_duplicate(descriptor: int, operation: int, minimum: int) -> int:
        duplicate_calls.append((descriptor, operation, minimum))
        return 7
    need(inherited_fd_at_least_three(
            1, fake_duplicate, lambda descriptor: closed_fds.append(descriptor))
             == 7
         and duplicate_calls == [(1, getattr(
             fcntl, "F_DUPFD_CLOEXEC", fcntl.F_DUPFD), 3)]
         and closed_fds == [1],
         "self-test low inherited fd promoted without touching stdio")
    duplicate_calls.clear()
    closed_fds.clear()
    need(inherited_fd_at_least_three(
            5, fake_duplicate, lambda descriptor: closed_fds.append(descriptor))
             == 5
         and duplicate_calls == [] and closed_fds == [],
         "self-test existing inherited fd >=3 unchanged")
    self_before = capture_file(SELF)[1]
    need(self_before["sha256"] == expect_self_sha256,
         "self-test launcher current SHA pin")
    static_pins = {
        "launcher": {"path": str(SELF), "sha256": expect_self_sha256},
        "python": {"path": str(PYTHON), "sha256": PYTHON_SHA256},
        "runner": {"path": str(RUNNER), "sha256": RUNNER_SHA256},
        "validator": {"path": str(VALIDATOR), "sha256": VALIDATOR_SHA256},
        "case_wrapper": {"path": str(CASE_WRAPPER),
                         "sha256": CASE_WRAPPER_SHA256},
    }
    with tempfile.TemporaryDirectory(prefix="c27r2-v8-launcher-selftest-") as raw:
        temp = Path(raw)
        temp_root = temp / "workspace"
        audit = temp_root / ".cm2-runtime/audit"
        audit.mkdir(mode=0o700, parents=True)
        launch_id = "c27r2-release-repair-integrity-v8-selftest01"
        paths = launch_paths(audit, launch_id)
        assert_fresh_paths(paths)
        paths["publication_control"].mkdir(mode=0o700)
        need(stat.S_IMODE(os.stat(paths["publication_control"]).st_mode) == 0o700,
             "self-test publication control mode")
        plan = build_plan(launch_id, paths, static_pins, temp_root)
        plan_path = paths["publication_control"] / "launch_plan.json"
        plan_record = write_once(plan_path, canonical(plan) + b"\n", 0o400)
        need(strict_closed_document(plan_path, "plan_sha256") == plan,
             "self-test plan replay")
        lock = build_lock(launch_id, plan_record, plan)
        lock_path = paths["publication_control"] / "publication_lock.json"
        lock_record = write_once(lock_path, canonical(lock) + b"\n", 0o400)
        need(strict_closed_document(lock_path, "publication_lock_sha256")
                 == lock,
             "self-test lock replay")
        descriptor, _ = open_and_lock(lock_path, lock_record)
        try:
            command = final_runner_argv(
                plan["runner_argv_nonlock"], lock, lock_record, descriptor)
            need(command[:4] == [str(PYTHON), "-I", "-B", str(RUNNER)]
                 and command[-2] == "--publication-lock-fd"
                 and command[-1] == str(descriptor)
                 and command.count("--service-query-fixture") == 1
                 and command[command.index("--service-query-fixture") + 1]
                     == "fixed",
                 "self-test final exact runner argv")
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)
    need(capture_file(SELF)[1] == self_before,
         "self-test launcher pre/post full9stat replay")
    return {"schema": SELF_TEST_SCHEMA, "status": SELF_TEST_STATUS,
            "formal_reads": 0, "formal_outputs": 0, "formal_credit": 0,
            "manifest_authorized": False, "authority_minted": False,
            "CM2": "NO-GO_FOR_CLAIM"}


def execute(launch_id: str, expect_self_sha256: str) -> None:
    verify_inventories()
    validate_launch_id(launch_id)
    need(AUDIT.is_dir() and not AUDIT.is_symlink(),
         "current direct audit parent")
    paths = launch_paths(AUDIT, launch_id)
    assert_fresh_paths(paths)
    source_before = source_pin_records(expect_self_sha256)
    source_pins = source_pin_projection(source_before)

    os.mkdir(paths["publication_control"], mode=0o700)
    fsync_directory(AUDIT)
    control_stat = os.stat(paths["publication_control"], follow_symlinks=False)
    need(stat.S_ISDIR(control_stat.st_mode)
         and stat.S_IMODE(control_stat.st_mode) == 0o700,
         "publication control exact 0700 directory")
    for role in ("work", "future_outer", "future_seal", "future_terminal"):
        need(not paths[role].exists() and not paths[role].is_symlink(),
             "fresh sibling after control publication:" + role)

    plan = build_plan(launch_id, paths, source_pins)
    plan_path = paths["publication_control"] / "launch_plan.json"
    plan_record = write_once(plan_path, canonical(plan) + b"\n", 0o400)
    need(strict_closed_document(plan_path, "plan_sha256") == plan,
         "formal launch plan exact byte replay")

    lock = build_lock(launch_id, plan_record, plan)
    lock_path = paths["publication_control"] / "publication_lock.json"
    lock_record = write_once(lock_path, canonical(lock) + b"\n", 0o400)
    need(strict_closed_document(lock_path, "publication_lock_sha256") == lock,
         "formal exact10 publication lock byte replay")
    need(sorted(path.name for path in paths["publication_control"].iterdir())
             == ["launch_plan.json", "publication_lock.json"],
         "publication control exact two-file inventory")

    descriptor, _ = open_and_lock(lock_path, lock_record)
    try:
        command = final_runner_argv(
            plan["runner_argv_nonlock"], lock, lock_record, descriptor)
        need(source_pin_records(expect_self_sha256) == source_before,
             "launcher and frozen sources pre-exec full9stat replay")
        need(strict_closed_document(plan_path, "plan_sha256") == plan
             and strict_closed_document(lock_path, "publication_lock_sha256")
                 == lock,
             "plan and lock final byte replay")
        for role in ("work", "future_outer", "future_seal", "future_terminal"):
            need(not paths[role].exists() and not paths[role].is_symlink(),
                 "final fresh sibling before execve:" + role)
        os.execve(str(PYTHON), command, EXACT_ENVIRONMENT)
    except BaseException:
        os.close(descriptor)
        raise


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--launch-id")
    value.add_argument("--expect-self-sha256", required=True)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        verify_exact_runtime()
        need(valid_sha(args.expect_self_sha256),
             "launcher expected self lowercase SHA")
        if args.self_test:
            need(args.launch_id is None, "self-test takes no formal launch-id")
            result = self_test(args.expect_self_sha256)
            sys.stdout.buffer.write(canonical(result) + b"\n")
            return 0
        need(args.launch_id is not None, "formal launcher requires launch-id")
        execute(args.launch_id, args.expect_self_sha256)
        raise Rejected("execve unexpectedly returned")
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            json.JSONDecodeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
