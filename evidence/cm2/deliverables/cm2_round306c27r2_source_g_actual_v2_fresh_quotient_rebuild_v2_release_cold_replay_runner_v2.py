#!/usr/bin/env python3
"""Build and run one fresh, independently verified C27R2 cold replay.

This append-only v2 helper consumes the frozen C27R2 v6 core and the exact
actual-v2 terminal/base/gate authority.  It creates a fresh command spec and
delegates the only mathematical execution to the already frozen v4 process
transaction runner and the no-import seed-2 verifier.  Success remains zero
credit and cannot create a manifest, seal, terminal receipt, service, or any
downstream authority.

The cold child transaction has exactly eleven success files.  Its declared
input list is an exact canonical inventory (not a subset contract), and the
run attestation must contain exactly command-spec, pinset, and every declared
input in order.  Any failure after the control directory is created produces
an append-only failure receipt and FAILED.lock.
"""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / ".cm2-runtime/audit"
SELF = Path(__file__).resolve()
PYTHON = Path("/usr/bin/python3.12")

UNIT = "cm2-c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523.service"
INVOCATION_ID = "aa82e1c6611f4910ae80b94307fb9ca9"
STEM = "c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523"
CORE_RECEIPT_FILE_SHA = "4104edc46bb130bae530a990609d5053bc9d7f675e4e3587e88b8327394c5796"
CORE_RECEIPT_OBJECT_SHA = "783d05cb9c01a2049a03112f9412bab787b5fad2c81fba1855d9cca4dabcb016"

ACTUAL_BASE_REL = (
    ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-"
    "dual-seed-zero-credit-seal-v2-20260808T1544"
)
ACTUAL_TERMINAL_REL = ACTUAL_BASE_REL + "-terminal-replay"
GATE_REL = (
    ".cm2-runtime/audit/c27r2-post-actual-v2-rebuild-gate-v3-r2-zero-"
    "credit-20260808T164429"
)
SEED1_EDGE_REL = (
    ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-"
    "seed30660101-p0r2-20260808T1432/full_component_edge_union.jsonl.gz"
)
SEED2_EDGE_REL = (
    ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-"
    "seed30660991-p0r2-20260808T1432/full_component_edge_union.jsonl.gz"
)
C15_REL = (
    "deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_"
    "freeze_member_component_ledger.jsonl.gz"
)
CORE_CONTROL_REL = f".cm2-runtime/audit/{STEM}-control"
CORE_CANDIDATE_REL = f".cm2-runtime/audit/{STEM}-candidate"
CORE_VERIFICATION_REL = f".cm2-runtime/audit/{STEM}-verifier-output"

SOURCE_PATHS = {
    "producer": (
        "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
        "rebuild_v2_producer_v4.py"
    ),
    "independent_verifier": (
        "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
        "rebuild_v2_independent_verifier_v4.py"
    ),
    "coherent_attack_harness": (
        "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
        "rebuild_v2_coherent_attack_harness_v4.py"
    ),
    "transaction_runner": (
        "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
        "rebuild_v2_transaction_runner_v4.py"
    ),
    "gated_watcher": (
        "deliverables/cm2_round306c27r2_source_g_actual_v2_fresh_quotient_"
        "rebuild_v2_gated_dual_seed_watcher_v6.py"
    ),
}
SOURCE_PINS = {
    "producer": "578d0ce0d39d14dede9d9528be383abb3d4140c26bcac75917fe860a98bb158b",
    "independent_verifier": "acc66bbff3717e16bf56b15f9498070d97a4be1b0cd9253a79b7cae598b4082f",
    "coherent_attack_harness": "1d501ca968853712743524e7aba16d29dadd62b9d46458b53e0421aef2072007",
    "transaction_runner": "7ce75edac7e1aad904718e173cf6ed178f6d2631ba1f5cb4253bcf2c1e121d63",
    "gated_watcher": "68c1d70ca55e4d17f1b727a6b1eda8343c1a6eaecd61df43ed5449198a88331d",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}
GATE_SOURCE_PATHS = {
    "producer": "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3.py",
    "independent_verifier": (
        "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3_"
        "independent_verifier_r2.py"
    ),
    "coherent_attack_harness": (
        "deliverables/cm2_round306c27r2_post_actual_v2_rebuild_gate_v3_"
        "coherent_attack_harness_r2.py"
    ),
}
GATE_SOURCE_PINS = {
    "producer": "aab253ba102dc5f168ff96089145ea8a23a3f4ff8255dad92d668430c93c82f8",
    "independent_verifier": "3a1aac7d79ce095226f310fdca0ac2614ee7d3a90e17d3fe69638b56b06dfe81",
    "coherent_attack_harness": "4e6c1b3c1befd08d6ad64c9f84728df309424ded28406740b39f95f6575657fb",
}

TERMINAL_FILE_PINS = {
    "PASS.lock": "dda5588904c0ab42dae19acbb5edea7bddd856e411cce7dade9dc3f354e49bd1",
    "payload_manifest.sha256": "9cf2a36f207152a34b58e95500d84cf145d1950970c55e30ec52d509f578f79a",
    "root_manifest.sha256": "c46609c00ede1308d160aa724c3ee7c9387d0329c82be7d01d09d12a3ddaadae",
    "terminal_receipt.json": "8fc365cc487d8f74695a858afd5ee26efc514547631960a9e0bc6dc8cf597cb1",
    "terminal_replay.json": "aa0bcf639c416c5b2deaccd58070c561ab6f6607b33c94143f9358f4585f13b8",
}
BASE_FILE_PINS = {
    "payload_manifest.sha256": "99165cc3e0e7be219c8187158b68d822802a1c9f5451c210a5e76a5ecacb4020",
    "receipt.json": "cf5e381c29e31a2b3b9107fc8e53109b15cee86d498bd11deed0558c4d85f614",
    "root_manifest.sha256": "51472919ec2b51fb53ec5c078ac4e1b1e4c57526c7a79ce135511cf21016449b",
    "payload/coherent_attacks.json": "efa2d2a1d4a83263f4491f1f64e0d2232e0b5539bc38cf0f3c1048d87e1cbd87",
    "payload/independent_verification.json": "98a88bd9f027fe108eea525a2c86c899380fd79ea400f5f2930f4afc009d7c94",
    "payload/inventory.json": "3999c5560ea499cfbf79534f455b0c916f0a274322cf3c02688ebfd31ac07481",
}

GATE_RECEIPT_FILE_SHA = "fb1feeeee61246aedd8aeb78c4c0a29a6a0ceb93084895cd84c951279d2cc5d4"
GATE_RECEIPT_OBJECT_SHA = "4afaff6f0dd51b5119fa7de7689abb7e35865c382b643a12a8eb82fdff5e1b71"
GATE_ROOT_FILE_SHA = "1269dd8dfa7b070efcd755d7c2b76f17a3647b16d7e75304a157837cb2ffc9a9"
GATE_ROOT_OBJECT_SHA = "0c6c81aa6fdb58855c16f074cbb161df211a34d1e760c00dbf6fc8cd6a55fbcd"
EDGE_SHA = "5bc29ef85bc57f467bee5ba94cd12e31950c2c940928cb57498421200c95bec0"
C15_SHA = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
ACTUAL_TERMINAL_RECEIPT_OBJECT_SHA = (
    "2a6d3b70667742cd5dbeacead0ec8a5a11429a2c7817d2809fd65e597b394222"
)
ACTUAL_TERMINAL_REPLAY_OBJECT_SHA = (
    "5a81b6a94adb506cc53bb9e137da0fe1019367fb5bf96a158e27ed1f81121c02"
)
ACTUAL_BASE_RECEIPT_OBJECT_SHA = (
    "3a29d0d4a761a659001b1ed34c24502f5247658b6a34c2f6c42a7987225789d5"
)

PREFIX = "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
PINSET_SCHEMA = PREFIX + "gated-transaction-pinset.v4"
SPEC_SCHEMA = PREFIX + "process-command-spec.v4"
RUN_SCHEMA = PREFIX + "process-run-attestation.v4"
RUN_STATUS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
CORE_SCHEMA = PREFIX + "gated-dual-seed-transaction-receipt.v4"
CORE_STATUS = (
    "PASS_GATE_SEED1_FOUR_FILE_CANDIDATE_SEED2_NO_IMPORT_REPLAY_AND_21_"
    "ATTACKS__ZERO_CREDIT_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
)
VERIFICATION_SCHEMA = PREFIX + "independent-verification.v1"
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_ACTUAL_V2_SEED2_INDEPENDENT_QUOTIENT_AND_BYTE_EXACT_"
    "CANDIDATE_REPLAY__ZERO_CREDIT_PENDING_ATTACKS_COLD_REPLAY_AND_"
    "TERMINAL_SEAL"
)
COLD_SCHEMA = "cm2.round306c27r2.source-g-authority-v2.release-cold-replay-receipt.v1"
COLD_STATUS = (
    "PASS_FRESH_NO_IMPORT_SEED2_COLD_BYTE_REPLAY_WITH_ALL_CORE_INPUT_PRE_"
    "POST_SHA_STAT__ZERO_CREDIT"
)
FAILURE_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-cold-replay-failure.v2"
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

ACTUAL_PASS = b"PASS_ACTUAL_V2_DUAL_SEED_TERMINAL_ZERO_CREDIT_SEAL\n"
CORE_PASS = b"PASS_C27R2_AUTHORITY_V2_GATED_DUAL_SEED_CORE__ZERO_CREDIT\n"
COLD_PASS = b"PASS_C27R2_RELEASE_COLD_REPLAY__ZERO_CREDIT\n"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
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
CONTROL_FILES = {
    "PASS.lock", "attack_command_spec.json", "candidate_validation.json",
    "coherent_attacks_runner.exit_code.txt",
    "coherent_attacks_runner.stderr.log",
    "coherent_attacks_runner.stdout.log",
    "dual_seed_descriptor_agreement.json",
    "independent_verifier_runner.exit_code.txt",
    "independent_verifier_runner.stderr.log",
    "independent_verifier_runner.stdout.log", "pinset.json", "preflight.json",
    "producer_command_spec.json", "producer_runner.exit_code.txt",
    "producer_runner.stderr.log", "producer_runner.stdout.log",
    "transaction_receipt.json", "verifier_command_spec.json",
}
GATE_FILES = {
    "PASS.lock", "gate_receipt.json", "execution_receipt.json",
    "coherent_attacks.json", "independent_verification.json",
    "producer.exit_code.txt", "producer.stderr.log", "producer.stdout.log",
    "independent_verifier.exit_code.txt", "independent_verifier.stderr.log",
    "independent_verifier.stdout.log", "coherent_attacks.exit_code.txt",
    "coherent_attacks.stderr.log", "coherent_attacks.stdout.log",
}
TERMINAL_FILES = set(TERMINAL_FILE_PINS)
BASE_FILES = set(BASE_FILE_PINS)
EXPECTED_MATH = {
    "C15_sha256": C15_SHA,
    "candidate_result_object_sha256":
        "70afe7c796348a657c58feffa227f6cfd9f7b1714e5a3c0c0ae5baa5d2c51fed",
    "cross_pairs": 125_561_998_198,
    "cycles": 668,
    "edges": 14_860,
    "members": 502_204,
    "merges": 14_192,
    "old_components": 57_876,
    "post_components": 43_684,
    "seed1_edge_sha256": EDGE_SHA,
    "seed2_edge_sha256": EDGE_SHA,
    "terminal_receipt_object_sha256": ACTUAL_TERMINAL_RECEIPT_OBJECT_SHA,
    "within_pairs": 542_179_508,
}
EXPECTED_CHECKS = {
    "all_gzip_canonical_order_count_row_closures_pass": True,
    "all_three_candidate_ledgers_byte_semantically_exact": True,
    "canonical_post_IDs_rederived_from_sorted_old_component_sets": True,
    "fresh_DSU_rebuilt_without_producer_import": True,
    "pair_identity_126104177706_equals_542179508_plus_125561998198": True,
    "seed1_and_seed2_edge_ledgers_byte_identical": True,
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
    return type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z")


def strict(raw: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(type(key) is str and key not in result, "unique JSON key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          ValueError(token)))


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid)


def workspace_path(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (ROOT / supplied if not supplied.is_absolute() else supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Blocked("path outside workspace:" + str(raw)) from error
    need(all(part not in {"", ".", ".."} for part in relative.parts),
         "canonical workspace path:" + str(raw))
    current = ROOT
    for part in relative.parts:
        current = current / part
        if not current.exists():
            need(absent, "missing path component:" + str(current))
            break
        need(not current.is_symlink(), "symlink path component:" + str(current))
    return path


def capture(path: Path) -> tuple[bytes, dict[str, Any]]:
    target = workspace_path(path)
    descriptor = os.open(target, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link:" + str(target))
        state = hashlib.sha256()
        chunks: list[bytes] = []
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
            chunks.append(block)
        after = os.fstat(descriptor)
        path_after = os.stat(target, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after)
             == fingerprint(path_after), "stable full9stat:" + str(target))
        return b"".join(chunks), {
            "path": str(target.relative_to(ROOT)), "sha256": state.hexdigest(),
            "size": before.st_size, "stat_fingerprint": list(fingerprint(before)),
            "O_NOFOLLOW": True, "single_link": True,
        }
    finally:
        os.close(descriptor)


def external_sha(path: Path) -> str:
    """Hash one pinned non-workspace executable with the same FD discipline."""
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "external regular single-link:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        path_after = os.stat(path, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after)
             == fingerprint(path_after), "external stable full9stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def document(path: Path, closure: str) -> tuple[dict[str, Any], dict[str, Any]]:
    raw, record = capture(path)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
         "document newline:" + str(path))
    value = strict(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1],
         "canonical document:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "object closure:" + str(path))
    return value, record


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def exact_tree(root: Path, directories: set[str], files: set[str],
               label: str) -> list[str]:
    base = workspace_path(root)
    need(base.is_dir() and not base.is_symlink(), label + ":directory")
    observed_dirs: set[str] = set()
    observed_files: set[str] = set()
    for current, names, file_names in os.walk(base):
        here = Path(current)
        for name in names:
            child = here / name
            need(not child.is_symlink(), label + ":no symlink directory")
            observed_dirs.add(str(child.relative_to(base)))
        for name in file_names:
            child = here / name
            need(not child.is_symlink() and child.is_file(),
                 label + ":regular file")
            observed_files.add(str(child.relative_to(base)))
    need(observed_dirs == directories and observed_files == files,
         label + ":exact recursive inventory")
    return [str((base / name).relative_to(ROOT)) for name in sorted(files)]


def attack_inventory() -> tuple[set[str], set[str]]:
    files = {
        "baseline_verification.json", "candidate-clone/member_to_post_component.jsonl.gz",
        "candidate-clone/old_c15_component_to_post_component.jsonl.gz",
        "candidate-clone/post_component_census.jsonl.gz",
        "candidate-clone/result.json", "coherent_attacks.json",
    }
    stems = [
        "baseline",
        "attack-00-missing-result", "attack-01-extra-inventory",
        "attack-02-result-noncanonical", "attack-03-result-duplicate-key",
        "attack-04-result-stale-closure", "attack-05-coherent-formal-credit",
        "attack-06-coherent-manifest-authorized", "attack-07-coherent-status-lie",
        "attack-08-coherent-census-lie", "attack-09-coherent-dsu-root-id-formula",
        "attack-10-coherent-seed-label-swap", "attack-11-coherent-ledger-sha-lie",
        "attack-12-result-symlink", "attack-13-old-map-hardlink",
        "attack-14-old-map-truncated-gzip", "attack-15-member-map-bad-gzip",
        "attack-16-post-census-empty-gzip", "attack-17-wrong-terminal-root-pin",
        "attack-18-wrong-terminal-file-pin", "attack-19-wrong-terminal-object-pin",
        "attack-20-terminal-base-directory-swap",
    ]
    for stem in stems:
        for suffix in ("exit_code.txt", "stderr", "stdout"):
            files.add(f"transcripts/{stem}.{suffix}")
    return {"candidate-clone", "saved", "transcripts"}, files


def core_inventory() -> list[str]:
    result: list[str] = []
    descriptions = [
        ("control", set(), CONTROL_FILES),
        ("candidate", set(), CANDIDATE_FILES),
        ("producer-run", set(), RUN_FILES),
        ("verifier-output", set(), {"verification.json"}),
        ("verifier-run", set(), RUN_FILES),
        ("attack-work", *attack_inventory()),
        ("attack-run", set(), RUN_FILES),
    ]
    for suffix, directories, files in descriptions:
        result.extend(exact_tree(AUDIT / f"{STEM}-{suffix}", directories,
                                 files, "core-" + suffix))
    need(len(result) == 128 and len(result) == len(set(result)),
         "exact 128-file frozen core inventory")
    return sorted(result)


def exact_source_pins() -> list[str]:
    paths: list[str] = []
    for role, relative in SOURCE_PATHS.items():
        _, record = capture(ROOT / relative)
        need(record["sha256"] == SOURCE_PINS[role], "C27 source pin:" + role)
        paths.append(relative)
    for role, relative in GATE_SOURCE_PATHS.items():
        _, record = capture(ROOT / relative)
        need(record["sha256"] == GATE_SOURCE_PINS[role], "gate source pin:" + role)
        paths.append(relative)
    need(external_sha(PYTHON) == SOURCE_PINS["python"], "Python executable pin")
    return paths


def service_success() -> None:
    completed = subprocess.run([
        "/usr/bin/systemctl", "--user", "show", UNIT,
        "-p", "ActiveState", "-p", "SubState", "-p", "Result",
        "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID",
    ], cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
       stderr=subprocess.PIPE, check=False, timeout=30)
    need(completed.returncode == 0 and completed.stderr == b"",
         "query frozen core service")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == INVOCATION_ID,
         "unique frozen core service clean success")


def validate_authority() -> tuple[dict[str, Any], list[str], list[dict[str, Any]]]:
    service_success()
    core_files = core_inventory()
    source_files = exact_source_pins()
    control = ROOT / CORE_CONTROL_REL
    core, core_record = document(control / "transaction_receipt.json",
                                 "transaction_receipt_sha256")
    pinset, _ = document(control / "pinset.json", "pinset_sha256")
    need(core_record["sha256"] == CORE_RECEIPT_FILE_SHA
         and core["transaction_receipt_sha256"] == CORE_RECEIPT_OBJECT_SHA
         and core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and core.get("C27R2")
             == "UNAUTHORIZED_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
         and capture(control / "PASS.lock")[0] == CORE_PASS,
         "frozen core terminal boundary")
    need(pinset.get("schema") == PINSET_SCHEMA
         and pinset.get("source_pins") == SOURCE_PINS,
         "frozen core pinset source closure")
    authority = pinset.get("actual_v2_authority")
    need(type(authority) is dict
         and authority.get("actual_base_seal_dir") == ACTUAL_BASE_REL
         and authority.get("actual_terminal_dir") == ACTUAL_TERMINAL_REL
         and authority.get("actual_terminal_root_sha256")
             == TERMINAL_FILE_PINS["root_manifest.sha256"]
         and authority.get("actual_terminal_receipt_file_sha256")
             == TERMINAL_FILE_PINS["terminal_receipt.json"]
         and authority.get("actual_terminal_receipt_object_sha256")
             == ACTUAL_TERMINAL_RECEIPT_OBJECT_SHA
         and authority.get("seed1_edge_path") == SEED1_EDGE_REL
         and authority.get("seed2_edge_path") == SEED2_EDGE_REL
         and authority.get("seed1_edge_sha256") == EDGE_SHA
         and authority.get("seed2_edge_sha256") == EDGE_SHA
         and authority.get("frozen_C15_path") == C15_REL
         and authority.get("frozen_C15_sha256") == C15_SHA
         and authority.get("gate_execution_root_object_sha256")
             == GATE_ROOT_OBJECT_SHA,
         "frozen core exact actual-v2 authority")

    expected_core_authority_inputs = sorted({
        *{str(Path(ACTUAL_TERMINAL_REL) / name)
          for name in TERMINAL_FILES - {"terminal_replay.json"}},
        *{str(Path(ACTUAL_BASE_REL) / name)
          for name in {"payload_manifest.sha256", "receipt.json",
                       "root_manifest.sha256"}},
        *{str(Path(GATE_REL) / name) for name in GATE_FILES},
        SEED1_EDGE_REL, SEED2_EDGE_REL, C15_REL,
    })
    need(authority.get("authority_input_paths") == expected_core_authority_inputs
         and len(expected_core_authority_inputs) == 24,
         "core authority exact fixed 24-path cross-closure")

    terminal_files = exact_tree(ROOT / ACTUAL_TERMINAL_REL, set(), TERMINAL_FILES,
                                "actual-terminal")
    for name, expected in TERMINAL_FILE_PINS.items():
        need(capture(ROOT / ACTUAL_TERMINAL_REL / name)[1]["sha256"] == expected,
             "actual terminal file pin:" + name)
    terminal, _ = document(ROOT / ACTUAL_TERMINAL_REL / "terminal_receipt.json",
                           "terminal_receipt_sha256")
    replay, _ = document(ROOT / ACTUAL_TERMINAL_REL / "terminal_replay.json",
                         "result_sha256")
    need(terminal.get("schema") == ACTUAL_TERMINAL_SCHEMA
         and terminal.get("status") == ACTUAL_TERMINAL_STATUS
         and terminal["terminal_receipt_sha256"]
             == ACTUAL_TERMINAL_RECEIPT_OBJECT_SHA
         and replay.get("schema") == ACTUAL_REPLAY_SCHEMA
         and replay.get("status") == ACTUAL_REPLAY_STATUS
         and replay["result_sha256"] == ACTUAL_TERMINAL_REPLAY_OBJECT_SHA
         and terminal.get("formal_credit") == 0
         and terminal.get("manifest_authorized") is False
         and replay.get("formal_credit") == 0
         and replay.get("manifest_authorized") is False
         and capture(ROOT / ACTUAL_TERMINAL_REL / "PASS.lock")[0] == ACTUAL_PASS,
         "actual terminal receipt/replay/PASS closure")

    base_files = exact_tree(ROOT / ACTUAL_BASE_REL, {"payload"}, BASE_FILES,
                            "actual-base")
    for name, expected in BASE_FILE_PINS.items():
        need(capture(ROOT / ACTUAL_BASE_REL / name)[1]["sha256"] == expected,
             "actual base file pin:" + name)
    base, base_record = document(ROOT / ACTUAL_BASE_REL / "receipt.json",
                                 "receipt_sha256")
    base_seal = terminal.get("base_seal")
    need(type(base_seal) is dict
         and base_record["sha256"] == BASE_FILE_PINS["receipt.json"]
         and base["receipt_sha256"] == ACTUAL_BASE_RECEIPT_OBJECT_SHA
         and base_seal.get("receipt_file_sha256") == base_record["sha256"]
         and base_seal.get("receipt_object_sha256") == base["receipt_sha256"]
         and base_seal.get("payload_manifest_file_sha256")
             == BASE_FILE_PINS["payload_manifest.sha256"]
         and base_seal.get("root_manifest_file_sha256")
             == BASE_FILE_PINS["root_manifest.sha256"],
         "terminal to actual base closure")

    gate_files = exact_tree(ROOT / GATE_REL, set(), GATE_FILES, "post-actual-gate")
    gate, gate_record = document(ROOT / GATE_REL / "gate_receipt.json",
                                 "gate_receipt_sha256")
    gate_root, gate_root_record = document(ROOT / GATE_REL / "execution_receipt.json",
                                           "execution_receipt_sha256")
    need(gate_record["sha256"] == GATE_RECEIPT_FILE_SHA
         and gate["gate_receipt_sha256"] == GATE_RECEIPT_OBJECT_SHA
         and gate_root_record["sha256"] == GATE_ROOT_FILE_SHA
         and gate_root["execution_receipt_sha256"] == GATE_ROOT_OBJECT_SHA
         and gate.get("schema") == GATE_SCHEMA and gate.get("status") == GATE_STATUS
         and gate_root.get("schema") == GATE_ROOT_SCHEMA
         and gate_root.get("status") == GATE_ROOT_STATUS
         and gate.get("formal_credit") == 0
         and gate.get("manifest_authorized") is False
         and gate_root.get("formal_credit") == 0
         and gate_root.get("manifest_authorized") is False,
         "post-actual gate exact root closure")
    for role, expected in (("seed1-edge", EDGE_SHA), ("seed2-edge", EDGE_SHA),
                           ("frozen-C15", C15_SHA)):
        relative = {"seed1-edge": SEED1_EDGE_REL, "seed2-edge": SEED2_EDGE_REL,
                    "frozen-C15": C15_REL}[role]
        need(capture(ROOT / relative)[1]["sha256"] == expected,
             "authority data pin:" + role)

    verifier_source = (ROOT / SOURCE_PATHS["independent_verifier"]).read_text(
        encoding="utf-8")
    tree = ast.parse(verifier_source, filename=SOURCE_PATHS["independent_verifier"])
    forbidden = Path(SOURCE_PATHS["producer"]).stem
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            need(all(alias.name != forbidden for alias in node.names),
                 "no-import verifier AST")
        if isinstance(node, ast.ImportFrom):
            need(node.module != forbidden, "no-import verifier AST")

    core_sources = sorted(SOURCE_PATHS.values())
    gate_sources = sorted(GATE_SOURCE_PATHS.values())
    need(sorted(source_files) == sorted(core_sources + gate_sources),
         "source-role partition closure")
    role_map = [
        {"role": "core_v6_frozen_transaction", "paths": core_files},
        {"role": "actual_v2_terminal", "paths": terminal_files},
        {"role": "actual_v2_base", "paths": base_files},
        {"role": "post_actual_gate", "paths": gate_files},
        {"role": "authority_data", "paths": sorted([
            SEED1_EDGE_REL, SEED2_EDGE_REL, C15_REL])},
        {"role": "core_sources", "paths": core_sources},
        {"role": "gate_sources", "paths": gate_sources},
        {"role": "cold_helper", "paths": [str(SELF.relative_to(ROOT))]},
    ]
    need([row["role"] for row in role_map] == [
        "core_v6_frozen_transaction", "actual_v2_terminal", "actual_v2_base",
        "post_actual_gate", "authority_data", "core_sources", "gate_sources",
        "cold_helper",
    ] and all(row["paths"] == sorted(set(row["paths"])) for row in role_map),
         "fixed exact cold role-map contract")
    inputs = sorted({path for row in role_map for path in row["paths"]})
    need(len(inputs) == 165, "exact 165-file cold declared input inventory")
    summary = {
        "actual_terminal_root_sha256": TERMINAL_FILE_PINS["root_manifest.sha256"],
        "actual_terminal_receipt_file_sha256":
            TERMINAL_FILE_PINS["terminal_receipt.json"],
        "actual_terminal_receipt_object_sha256":
            ACTUAL_TERMINAL_RECEIPT_OBJECT_SHA,
        "actual_terminal_replay_object_sha256": ACTUAL_TERMINAL_REPLAY_OBJECT_SHA,
        "actual_base_receipt_object_sha256": ACTUAL_BASE_RECEIPT_OBJECT_SHA,
        "gate_receipt_object_sha256": GATE_RECEIPT_OBJECT_SHA,
        "gate_execution_root_object_sha256": GATE_ROOT_OBJECT_SHA,
        "seed1_edge_sha256": EDGE_SHA, "seed2_edge_sha256": EDGE_SHA,
        "frozen_C15_sha256": C15_SHA,
    }
    return summary, inputs, role_map


def record_paths(attestations: Any) -> list[str]:
    need(type(attestations) is dict, "attestation map")
    labels = ["command-spec", "pinset"] + [
        f"declared-input-{ordinal:03d}" for ordinal in
        range(len(attestations) - 2)]
    need(list(attestations) == labels, "exact ordered attestation labels")
    result: list[str] = []
    for label in labels:
        row = attestations[label]
        need(type(row) is dict
             and set(row) == {"path", "sha256", "size", "stat_fingerprint",
                              "O_NOFOLLOW",
                              "single_open_file_description_hash_child_fstat_and_path_identity"}
             and valid_sha(row.get("sha256"))
             and type(row.get("size")) is int and row["size"] >= 0
             and type(row.get("stat_fingerprint")) is list
             and len(row["stat_fingerprint"]) == 9
             and row.get("O_NOFOLLOW") is True
             and row.get("single_open_file_description_hash_child_fstat_and_path_identity")
                 is True,
             "full9stat attestation row:" + label)
        result.append(row["path"])
    return result


def validate_exact_attestation_paths(attestations: Any, spec_relative: str,
                                     pinset_relative: str,
                                     inputs: list[str]) -> list[str]:
    observed = record_paths(attestations)
    expected = [spec_relative, pinset_relative, *inputs]
    need(observed == expected and len(observed) == len(set(observed)),
         "exact attestation path sequence no extra/omission")
    return observed


def failure(control: Path, stage: str, error: BaseException) -> None:
    body = {
        "schema": FAILURE_SCHEMA,
        "status": "FAILED_CLOSED_C27R2_RELEASE_REPAIR_FRESH_COLD_V2__ZERO_CREDIT",
        "failed_at_utc": utc_now(), "stage": stage,
        "error": f"{type(error).__name__}:{error}",
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED", "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt = {**body, "failure_receipt_sha256": digest(body)}
    if not (control / "failure_receipt.json").exists():
        write_json(control / "failure_receipt.json", receipt)
    if not (control / "FAILED.lock").exists():
        write_once(control / "FAILED.lock",
                   b"FAILED_CLOSED_C27R2_RELEASE_REPAIR_FRESH_COLD_V2\n")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    need(valid_sha(args.expect_helper_sha256)
         and capture(SELF)[1]["sha256"] == args.expect_helper_sha256,
         "cold helper self pin")
    control = workspace_path(args.control_dir, absent=True)
    output = workspace_path(args.output_dir, absent=True)
    run = workspace_path(args.run_dir, absent=True)
    need(len({control, output, run}) == 3
         and all(path.parent == AUDIT for path in (control, output, run))
         and all(not path.exists() and not path.is_symlink()
                 for path in (control, output, run)),
         "fresh distinct cold paths under audit root")
    if args.preflight_only:
        authority, inputs, role_map = validate_authority()
        return {"status": "PASS_C27R2_RELEASE_REPAIR_FRESH_COLD_V2_PREFLIGHT_"
                "EXACT165_INPUTS__NO_PATHS_CREATED_ZERO_CREDIT",
                "authority": authority, "input_count": len(inputs),
                "role_map_sha256": digest(role_map)}

    control.mkdir(mode=0o700)
    stage = "authority_and_exact_inventory"
    try:
        authority, inputs, role_map = validate_authority()
        output.mkdir(mode=0o700)
        pinset_body = {
            "schema": PINSET_SCHEMA,
            "status": "PASS_C27R2_RELEASE_COLD_REPLAY_PINSET__ZERO_CREDIT",
            "predecessor_unit": UNIT,
            "predecessor_invocation_id": INVOCATION_ID,
            "core_receipt_file_sha256": CORE_RECEIPT_FILE_SHA,
            "core_receipt_object_sha256": CORE_RECEIPT_OBJECT_SHA,
            "actual_v2_authority": authority,
            "source_pins": {
                "cold_replay_helper": args.expect_helper_sha256,
                "independent_verifier": SOURCE_PINS["independent_verifier"],
                "python": SOURCE_PINS["python"],
                "transaction_runner": SOURCE_PINS["transaction_runner"],
            },
            "targets": {
                "control": str(control.relative_to(ROOT)),
                "output": str(output.relative_to(ROOT)),
                "run": str(run.relative_to(ROOT)),
            },
            "exact_declared_input_count": len(inputs),
            "exact_declared_input_paths_sha256": hashlib.sha256(
                b"".join(path.encode("ascii") + b"\n" for path in inputs)
            ).hexdigest(),
            "declared_input_role_map": role_map,
            "declared_input_role_map_sha256": digest(role_map),
            "cold_replay_only": True, "formal_credit": 0,
            "manifest_authorized": False, "C27R2": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        pinset = {**pinset_body, "pinset_sha256": digest(pinset_body)}
        pinset_path = control / "pinset.json"
        write_json(pinset_path, pinset)

        verifier = ROOT / SOURCE_PATHS["independent_verifier"]
        runner = ROOT / SOURCE_PATHS["transaction_runner"]
        verification_path = output / "verification.json"
        argv = [
            str(PYTHON), "-I", "-B", str(verifier),
            "--terminal-dir", str(ROOT / ACTUAL_TERMINAL_REL),
            "--base-seal-dir", str(ROOT / ACTUAL_BASE_REL),
            "--expect-terminal-root-sha256",
            TERMINAL_FILE_PINS["root_manifest.sha256"],
            "--expect-terminal-receipt-file-sha256",
            TERMINAL_FILE_PINS["terminal_receipt.json"],
            "--expect-terminal-receipt-object-sha256",
            ACTUAL_TERMINAL_RECEIPT_OBJECT_SHA,
            "--candidate-dir", str(ROOT / CORE_CANDIDATE_REL),
            "--out-file", str(verification_path),
        ]
        spec_body = {
            "schema": SPEC_SCHEMA, "stage": "independent_verifier",
            "source_path": str(verifier),
            "source_sha256": SOURCE_PINS["independent_verifier"],
            "argv": argv,
            "environment": {"PATH": "/usr/bin:/bin", "LANG": "C",
                            "LC_ALL": "C", "PYTHONHASHSEED": "30662727"},
            "python_hash_seed": "30662727",
            "timeout_seconds": args.timeout_seconds,
            "expected_stdout_status": VERIFICATION_STATUS,
            "input_paths": inputs,
            "exact_declared_input_count": len(inputs),
            "exact_declared_input_paths_sha256": pinset[
                "exact_declared_input_paths_sha256"],
            "declared_input_role_map_sha256": pinset[
                "declared_input_role_map_sha256"],
            "output_roots": [{
                "path": str(output), "kind": "directory",
                "precondition": "EXISTING_EMPTY_DIRECTORY",
                "exact_inventory": ["verification.json"],
                "required_relative_files": ["verification.json"],
            }],
            "pinset_file_sha256": capture(pinset_path)[1]["sha256"],
            "pinset_object_sha256": pinset["pinset_sha256"],
            "runner_source_sha256": SOURCE_PINS["transaction_runner"],
            "python_sha256": SOURCE_PINS["python"],
            "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM",
        }
        spec = {**spec_body, "command_spec_sha256": digest(spec_body)}
        spec_path = control / "cold_command_spec.json"
        write_json(spec_path, spec)

        stage = "fresh_no_import_seed2_process_transaction"
        completed = subprocess.run([
            str(PYTHON), "-I", "-B", str(runner),
            "--stage", "independent_verifier", "--command-spec", str(spec_path),
            "--pinset", str(pinset_path), "--run-dir", str(run),
            "--expect-runner-sha256", SOURCE_PINS["transaction_runner"],
            "--expect-python-sha256", SOURCE_PINS["python"],
        ], cwd=ROOT, env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
                          "PYTHONHASHSEED": "30662728"},
           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
           stderr=subprocess.PIPE, check=False, timeout=args.timeout_seconds + 120)
        write_once(control / "runner.stdout.log", completed.stdout)
        write_once(control / "runner.stderr.log", completed.stderr)
        write_once(control / "runner.exit_code.txt",
                   (str(completed.returncode) + "\n").encode("ascii"))
        expected_wrapper = canonical({
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
            "stage": "independent_verifier", "status": RUN_STATUS,
        }) + b"\n"
        need(completed.returncode == 0 and completed.stderr == b""
             and completed.stdout == expected_wrapper,
             "cold runner exact clean wrapper transaction")
        need(run.is_dir() and not run.is_symlink()
             and {path.name for path in run.iterdir()} == RUN_FILES,
             "cold exact eleven-file success transaction")

        attestation, attestation_record = document(run / "run_attestation.json",
                                                   "run_attestation_sha256")
        need(attestation.get("schema") == RUN_SCHEMA
             and attestation.get("status") == RUN_STATUS
             and attestation.get("stage") == "independent_verifier"
             and attestation.get("numeric_exit_code") == 0
             and attestation.get("signal") is None
             and attestation.get("timed_out") is False
             and attestation.get("stderr_empty") is True
             and attestation.get("stderr_sha256") == EMPTY_SHA
             and attestation.get("input_pre_post_sha_stat_identical") is True
             and attestation.get("runner_source_sha256")
                 == SOURCE_PINS["transaction_runner"]
             and attestation.get("stage_source_sha256")
                 == SOURCE_PINS["independent_verifier"]
             and attestation.get("python_sha256") == SOURCE_PINS["python"]
             and attestation.get("formal_credit") == 0
             and attestation.get("manifest_authorized") is False,
             "cold process attestation closure")
        pre_raw, _ = capture(run / "input_pre.json")
        post_raw, _ = capture(run / "input_post.json")
        need(pre_raw == post_raw, "cold input pre/post byte identity")
        pre = strict(pre_raw[:-1])
        need(pre == attestation["input_attestations"],
             "cold input sidecar/attestation identity")
        observed_paths = validate_exact_attestation_paths(
            pre, str(spec_path.relative_to(ROOT)), str(pinset_path.relative_to(ROOT)),
            inputs)
        need(len(observed_paths) == 167, "exact 167 captured process inputs")
        need(capture(run / "exit_code.txt")[0] == b"0\n"
             and capture(run / "signal.json")[0] == b"null\n"
             and capture(run / "stderr.log")[0] == b"",
             "cold numeric exit/signal/stderr sidecars")

        cold, cold_record = document(verification_path, "verification_sha256")
        formal_raw, formal_record = capture(
            ROOT / CORE_VERIFICATION_REL / "verification.json")
        cold_raw, _ = capture(verification_path)
        need(cold_raw == formal_raw and cold_record["sha256"] == formal_record["sha256"]
             and cold.get("schema") == VERIFICATION_SCHEMA
             and cold.get("status") == VERIFICATION_STATUS
             and cold.get("producer_imported_or_executed") is False
             and cold.get("actual_v2_seed_used") == "seed2"
             and cold.get("mathematical_projection") == EXPECTED_MATH
             and cold.get("exact_checks") == EXPECTED_CHECKS
             and cold.get("formal_credit") == 0
             and cold.get("manifest_authorized") is False
             and cold.get("CM2") == "NO-GO_FOR_CLAIM",
             "fresh no-import ledger/quotient/count and byte replay closure")

        stage = "write_zero_credit_cold_receipt"
        body = {
            "schema": COLD_SCHEMA, "status": COLD_STATUS,
            "completed_at_utc": utc_now(), "predecessor_unit": UNIT,
            "predecessor_invocation_id": INVOCATION_ID,
            "core_receipt_file_sha256": CORE_RECEIPT_FILE_SHA,
            "core_receipt_object_sha256": CORE_RECEIPT_OBJECT_SHA,
            "verification_file_sha256": cold_record["sha256"],
            "verification_object_sha256": cold["verification_sha256"],
            "formal_verification_byte_identical": True,
            "run_attestation_file_sha256": attestation_record["sha256"],
            "run_attestation_object_sha256": attestation["run_attestation_sha256"],
            "numeric_exit_code": 0, "signal": None, "stderr_empty": True,
            "all_core_inputs_pre_post_sha_stat_identical": True,
            "exact_process_success_file_count": 11,
            "exact_declared_input_count": len(inputs),
            "exact_process_capture_count": len(observed_paths),
            "exact_declared_input_paths_sha256": pinset[
                "exact_declared_input_paths_sha256"],
            "exact_attested_path_sequence_sha256": hashlib.sha256(
                b"".join(path.encode("ascii") + b"\n" for path in observed_paths)
            ).hexdigest(),
            "authority_closure": authority,
            "no_import_seed2_verifier": True,
            "ledger_quotient_count_closure": EXPECTED_MATH,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_RELEASE_ATTACKS_MANIFEST_OUTER_AND_TERMINAL_REPLAY",
            "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = {**body, "cold_replay_receipt_sha256": digest(body)}
        write_json(control / "cold_replay_receipt.json", receipt)
        write_once(control / "PASS.lock", COLD_PASS)
        need({path.name for path in control.iterdir()} == {
            "PASS.lock", "cold_command_spec.json", "cold_replay_receipt.json",
            "pinset.json", "runner.exit_code.txt", "runner.stderr.log",
            "runner.stdout.log",
        }, "cold exact seven-file control inventory")
        return receipt
    except BaseException as error:
        failure(control, stage, error)
        raise


def fixture_record(path: str) -> dict[str, Any]:
    return {
        "path": path, "sha256": "0" * 64, "size": 0,
        "stat_fingerprint": [1, 2, stat.S_IFREG | 0o600, 1, 0, 3, 4, 5, 6],
        "O_NOFOLLOW": True,
        "single_open_file_description_hash_child_fstat_and_path_identity": True,
    }


def self_test() -> dict[str, Any]:
    attack_dirs, attack_files = attack_inventory()
    need(attack_dirs == {"candidate-clone", "saved", "transcripts"}
         and len(attack_files) == 72 and len(RUN_FILES) == 11
         and len(CONTROL_FILES) == 18 and len(GATE_FILES) == 14,
         "exact frozen inventory fixture")
    inputs = ["fixture/a", "fixture/b"]
    labels = ["command-spec", "pinset", "declared-input-000",
              "declared-input-001"]
    paths = ["fixture/spec", "fixture/pinset", *inputs]
    valid = {label: fixture_record(path) for label, path in zip(labels, paths)}
    need(validate_exact_attestation_paths(
        valid, "fixture/spec", "fixture/pinset", inputs) == paths,
        "exact attestation positive fixture")
    extra = dict(valid)
    extra["declared-input-002"] = fixture_record("fixture/extra")
    omitted = dict(valid)
    omitted.pop("declared-input-001")
    rejected = 0
    for candidate in (extra, omitted):
        try:
            validate_exact_attestation_paths(
                candidate, "fixture/spec", "fixture/pinset", inputs)
        except Blocked:
            rejected += 1
    need(rejected == 2, "extra and omission negative fixtures")
    producer = Path(SOURCE_PATHS["producer"]).stem
    verifier_tree = ast.parse((ROOT / SOURCE_PATHS["independent_verifier"])
                              .read_text(encoding="utf-8"))
    need(all(not (isinstance(node, ast.Import)
                  and any(alias.name == producer for alias in node.names))
             and not (isinstance(node, ast.ImportFrom) and node.module == producer)
             for node in ast.walk(verifier_tree)),
         "no-import verifier static fixture")
    with tempfile.TemporaryDirectory(dir=ROOT / ".cm2-runtime",
            prefix="c27r2-fresh-cold-v2-selftest-") as raw:
        member = Path(raw) / "member"
        member.write_bytes(b"cold-fixture\n")
        first = capture(member)[1]
        second = capture(member)[1]
        need(first == second and len(first["stat_fingerprint"]) == 9
             and first["single_link"] is True,
             "real O_NOFOLLOW full9stat fixture")
    return {
        "status": "PASS_C27R2_RELEASE_REPAIR_FRESH_COLD_V2_EXACT_"
                  "INVENTORY_ATTESTATION_EXTRA_OMISSION_NO_IMPORT_FULL9STAT_FIXTURES",
        "formal_execution_started": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--control-dir")
    parser.add_argument("--output-dir")
    parser.add_argument("--run-dir")
    parser.add_argument("--expect-helper-sha256")
    parser.add_argument("--timeout-seconds", type=int, default=10_800)
    args = parser.parse_args()
    fields = ("control_dir", "output_dir", "run_dir", "expect_helper_sha256")
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no execution arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields)
                 and 60 <= args.timeout_seconds <= 86_400,
                 "all execution arguments and bounded timeout")
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
