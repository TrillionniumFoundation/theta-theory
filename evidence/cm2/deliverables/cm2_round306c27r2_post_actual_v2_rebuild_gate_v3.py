#!/usr/bin/env python3
"""Append-only zero-credit launch gate for a fresh post-actual-v2 C27R2 rebuild.

This program does not build C27R2 and cannot mint C27R2, C28, or C29.  It
validates the exact completed actual-v2 dual-seed terminal transaction, all
base/terminal manifest payloads, the durable finalizer execution record, and
the pinned implementation files.  Its sole positive conclusion is permission
to *begin* a separate fresh C27R2 rebuild.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SERVICE_UNIT = "cm2-c27-source-g-actual-v2-p1-finalizer-v2-20260808T1544.service"
FINALIZER_RUN = ROOT / ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-dual-seed-finalizer-p1v2-20260808T1544-run"
BASE_SEAL = ROOT / ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-dual-seed-zero-credit-seal-v2-20260808T1544"
TERMINAL = ROOT / ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-v2-dual-seed-zero-credit-seal-v2-20260808T1544-terminal-replay"

EXPECTED_FILES = {
    "base_receipt": (BASE_SEAL / "receipt.json", "cf5e381c29e31a2b3b9107fc8e53109b15cee86d498bd11deed0558c4d85f614"),
    "base_payload_manifest": (BASE_SEAL / "payload_manifest.sha256", "99165cc3e0e7be219c8187158b68d822802a1c9f5451c210a5e76a5ecacb4020"),
    "base_root_manifest": (BASE_SEAL / "root_manifest.sha256", "51472919ec2b51fb53ec5c078ac4e1b1e4c57526c7a79ce135511cf21016449b"),
    "terminal_receipt": (TERMINAL / "terminal_receipt.json", "8fc365cc487d8f74695a858afd5ee26efc514547631960a9e0bc6dc8cf597cb1"),
    "terminal_replay": (TERMINAL / "terminal_replay.json", "aa0bcf639c416c5b2deaccd58070c561ab6f6607b33c94143f9358f4585f13b8"),
    "terminal_payload_manifest": (TERMINAL / "payload_manifest.sha256", "9cf2a36f207152a34b58e95500d84cf145d1950970c55e30ec52d509f578f79a"),
    "terminal_root_manifest": (TERMINAL / "root_manifest.sha256", "c46609c00ede1308d160aa724c3ee7c9387d0329c82be7d01d09d12a3ddaadae"),
    "final_result": (FINALIZER_RUN / "final_result.json", "8fc365cc487d8f74695a858afd5ee26efc514547631960a9e0bc6dc8cf597cb1"),
}

SOURCE_FILES = {
    "runner": ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_runner.py",
    "assembler": ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2.py",
    "seed2_handoff_watcher": ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_seed2_gated_handoff.py",
    "independent_verifier": ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_independent_verifier_v2.py",
    "coherent_attack_harness": ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_coherent_attack_harness_v2.py",
    "terminal_replay": ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_terminal_replay_v1.py",
    "finalizer_watcher": ROOT / "deliverables/cm2_c27_primitive_twenty_family_gate_v5_actual_v2_dual_seed_finalizer_watcher_v2.py",
    "frozen_C15": ROOT / "deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz",
    "python": Path("/usr/bin/python3.12"),
}

SOURCE_PINS = {
    "runner": "c0f2c29d03aad122762ba0b3dad5885418c17872dab3da665eb764dad9cab245",
    "assembler": "038c6a661438f9253fb00a29b9f41941bea33a3a8769a258d8dfa5763880b561",
    "seed2_handoff_watcher": "3e5f874230c9faf809975808a2bd7284acf32c6e2b771e36a86d532a1a22c386",
    "independent_verifier": "fa85d391ec62a4e0026bd6895f2adb76df052c10426b0317466e0238ccc31268",
    "coherent_attack_harness": "883992243b9aabbcb948ca76484e2f77994a874d9a9034190084ebe987af34ae",
    "terminal_replay": "bce8f616c139823300f14fe7c16eeec60d4a4455216926fc1cff09d47d87bcab",
    "finalizer_watcher": "b34b41bb070d83312ff3687439d0f0afa88633ec50b5321a061e5b6a8ee5e4e0",
    "frozen_C15": "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
}

TERMINALS = (
    "SAME_CHART_RELATIVE_CELLS", "RETAINED_CONTINUATION", "OUTGOING_GRAPHS",
    "SINGLE_GRAPHS", "DOUBLE_GRAPHS", "SHEET_OWNER", "SHEET_SHADOW",
    "SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS", "INCLUDED_STRATUM_ATTACHMENTS",
    "REVERSE_RECHART", "TRUE_CYCLIC_SEAM_E_TO_N",
    "TRUE_CYCLIC_SEAM_N_TO_W", "TRUE_CYCLIC_SEAM_W_TO_S",
    "TRUE_CYCLIC_SEAM_S_TO_E", "Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL", "REPRESENTATION_ALIASES",
)
EXPECTED_CANDIDATES = (
    5_970_840, 276, 264, 4_984, 1_362_088, 17_940, 17_940,
    25_452, 10_688, 64_940, 10_660, 0, 1, 1, 1, 1, 0, 0, 0, 0,
)
EXPECTED_PROOFS = (
    32_240, 0, 0, 216, 0, 0, 0, 0, 0, 32_608,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
)
EXPECTED_CENSUS = {
    "atom_pair_incidence_terminal_census": {
        "COMPLETE_BOUNDARY_FACES": 30_624,
        "POSITIVE_VOLUME_CARRIERS": 120_472,
        "SIGNED_BOUNDARY_FACES": 55_536,
    },
    "atom_pair_incidence_total": 206_632,
    "candidate_component_disposition_census": {
        "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 65_064,
        "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 7_156_856,
        "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 264_156,
    },
    "candidate_total": 7_486_076,
    "exact_complement_atoms": 420_464,
    "fresh_DSU_cycle_edges": 668,
    "fresh_DSU_final_component_total": 43_684,
    "fresh_DSU_successful_merges": 14_192,
    "frozen_C15_component_total": 57_876,
    "frozen_C15_member_total": 502_204,
    "full_component_edge_union_total": 14_860,
    "incident_atoms": 62_768,
    "materialized_physical_proof_total": 65_064,
    "multi_terminal_atoms": 3_896,
    "primitive_atom_denominator": 483_232,
    "terminal_candidate_census": dict(zip(TERMINALS, EXPECTED_CANDIDATES)),
    "terminal_materialized_physical_proof_census": dict(zip(TERMINALS, EXPECTED_PROOFS)),
}

BASE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-seed-zero-credit-seal.v1"
BASE_STATUS = "PASS_SEALED_TWO_REAL_SEEDS_NATIVE_AND_INDEPENDENT_REPLAY_PLUS_24_ATTACKS__PENDING_COLD_REPLAY__ZERO_CREDIT"
TERMINAL_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-seed-terminal-receipt.v1"
TERMINAL_STATUS = "PASS_ACTUAL_V2_TWO_REAL_SEEDS_INDEPENDENT_REPLAY_24_ATTACKS_COLD_REPLAY_TERMINAL_SEAL__ZERO_CREDIT"
REPLAY_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-seed-terminal-replay.v1"
REPLAY_STATUS = "PASS_COLD_ROOT_PAYLOAD_CURRENT_SHA_STAT_NATIVE_DUAL_SEED_INDEPENDENT_REPLAY_AND_24_ATTACKS__ZERO_CREDIT"


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            info.st_uid, info.st_gid)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


class Capture:
    def __init__(self, path: Path, label: str, expected: str | None = None):
        self.path = path.resolve()
        self.label = label
        if path != Path("/usr/bin/python3.12"):
            need(self.path == ROOT or ROOT in self.path.parents,
                 label + ":inside-workspace")
        need(not path.is_symlink(), label + ":no-symlink")
        self.fd = os.open(self.path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                          | getattr(os, "O_NOFOLLOW", 0))
        before = os.fstat(self.fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             label + ":regular-single-link")
        self.initial = fingerprint(before)
        state = hashlib.sha256()
        parts = []
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
            parts.append(block)
        self.raw = b"".join(parts)
        self.sha256 = state.hexdigest()
        need(fingerprint(os.fstat(self.fd)) == self.initial,
             label + ":stable-hash-fstat")
        if expected is not None:
            need(self.sha256 == expected, label + ":expected-sha256")

    def document(self, closure: str | None = None) -> Any:
        value = json.loads(
            self.raw, object_pairs_hook=unique_object,
            parse_constant=lambda item: (_ for _ in ()).throw(
                Reject(self.label + ":nonfinite:" + item)))
        need(self.raw == canonical(value) + b"\n", self.label + ":canonical-json")
        if closure is not None:
            need(type(value) is dict, self.label + ":closed-object")
            body = dict(value)
            claimed = body.pop(closure, None)
            need(type(claimed) is str and claimed == digest(body),
                 self.label + ":object-closure")
        return value

    def attest(self) -> dict[str, Any]:
        need(fingerprint(os.fstat(self.fd)) == self.initial,
             self.label + ":terminal-fstat")
        try:
            relative = str(self.path.relative_to(ROOT))
        except ValueError:
            relative = str(self.path)
        return {
            "path": relative, "sha256": self.sha256,
            "size": self.initial[4], "stat_fingerprint": list(self.initial),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def write_new(path: Path, value: dict[str, Any]) -> None:
    need(path.parent.is_dir(), "output-parent-exists")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, canonical(value) + b"\n")
        os.fsync(fd)
    finally:
        os.close(fd)


def manifest_rows(capture: Capture, expected_count: int | None = None) -> list[tuple[str, str]]:
    need(capture.raw.endswith(b"\n"), capture.label + ":manifest-newline")
    try:
        lines = capture.raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Reject(capture.label + ":manifest-ascii") from error
    rows: list[tuple[str, str]] = []
    paths: set[str] = set()
    for ordinal, line in enumerate(lines):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64
             and pieces[0] == pieces[0].lower()
             and all(char in "0123456789abcdef" for char in pieces[0]),
             f"{capture.label}:manifest-line:{ordinal}")
        need(pieces[1] not in paths, capture.label + ":manifest-duplicate-path")
        paths.add(pieces[1])
        rows.append((pieces[1], pieces[0]))
    if expected_count is not None:
        need(len(rows) == expected_count, capture.label + ":manifest-count")
    return rows


def workspace_payload(path_text: str) -> Path:
    pure = PurePosixPath(path_text)
    need(not pure.is_absolute() and ".." not in pure.parts
         and "." not in pure.parts and str(pure) == path_text,
         "payload-canonical-relative-path:" + path_text)
    path = (ROOT / path_text).resolve()
    need(path == ROOT or ROOT in path.parents, "payload-inside-workspace:" + path_text)
    return path


def exact_root(capture: Capture, payload_sha: str, receipt_name: str,
               receipt_sha: str) -> None:
    expected = (f"{payload_sha}  payload_manifest.sha256\n"
                f"{receipt_sha}  {receipt_name}\n").encode("ascii")
    need(capture.raw == expected, capture.label + ":exact-two-entry-root")


def source_pin_gate(captures: list[Capture]) -> dict[str, dict[str, Any]]:
    output = {}
    for label, path in SOURCE_FILES.items():
        cap = Capture(path, "source:" + label, SOURCE_PINS[label])
        captures.append(cap)
        output[label] = cap.attest()
    return output


def service_gate(terminal_object_sha256: str) -> dict[str, Any]:
    show = subprocess.run([
        "/usr/bin/systemctl", "--user", "show", SERVICE_UNIT,
        "--property=Id", "--property=LoadState", "--property=ActiveState",
        "--property=SubState", "--property=Result", "--property=ExecMainCode",
        "--property=ExecMainStatus", "--no-pager",
    ], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(show.returncode == 0 and show.stderr == b"", "finalizer-service-show")
    values = {}
    for line in show.stdout.decode("ascii", "strict").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    need(values.get("Id") == SERVICE_UNIT
         and values.get("ActiveState") == "inactive"
         and values.get("SubState") == "dead"
         and values.get("ExecMainStatus") == "0",
         "finalizer-service-terminal-state")
    if values.get("LoadState") == "loaded":
        need(values.get("Result") == "success"
             and values.get("ExecMainCode") in {"1", "exited"},
             "loaded-finalizer-service-success")
        return {"mode": "LOADED_INACTIVE_DEAD_SUCCESS_EXIT0",
                "unit": SERVICE_UNIT, "show": values,
                "show_sha256": hashlib.sha256(show.stdout).hexdigest()}

    need(values.get("LoadState") == "not-found",
         "finalizer-service-loaded-or-collected")
    journal = subprocess.run([
        "/usr/bin/journalctl", "--user", "-u", SERVICE_UNIT,
        "--no-pager", "-o", "cat",
    ], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(journal.returncode == 0 and journal.stderr == b"",
         "collected-finalizer-journal")
    lines = journal.stdout.decode("utf-8", "strict").splitlines()
    expected_summary = canonical({
        "C27R2_C28_C29": "AUTHORIZED_TO_BEGIN_FRESH_REBUILD_ONLY__NOT_REBUILT_NOT_CREDITED",
        "CM2": "NO-GO_FOR_CLAIM", "status": TERMINAL_STATUS,
        "terminal_receipt_sha256": terminal_object_sha256,
    }).decode("ascii")
    need(lines.count(expected_summary) == 1
         and any(line.startswith("Starting " + SERVICE_UNIT) for line in lines)
         and any(line.startswith("Started " + SERVICE_UNIT) for line in lines)
         and not any("Failed with result" in line or line.startswith("FAIL:")
                     for line in lines),
         "collected-finalizer-durable-journal-success")
    return {
        "mode": "TRANSIENT_UNIT_COLLECTED_AFTER_DURABLE_TERMINAL_SUCCESS",
        "unit": SERVICE_UNIT, "show": values,
        "show_sha256": hashlib.sha256(show.stdout).hexdigest(),
        "journal_sha256": hashlib.sha256(journal.stdout).hexdigest(),
        "terminal_summary_line_sha256": hashlib.sha256(
            expected_summary.encode("ascii")).hexdigest(),
    }


def validate_positive() -> dict[str, Any]:
    captures: list[Capture] = []
    try:
        fixed: dict[str, Capture] = {}
        for label, (path, expected) in EXPECTED_FILES.items():
            fixed[label] = Capture(path, label, expected)
            captures.append(fixed[label])

        need((FINALIZER_RUN / "PASS.lock").read_bytes()
             == b"PASS_ACTUAL_V2_DUAL_SEED_FINALIZER_TERMINAL_ZERO_CREDIT\n",
             "finalizer-exact-PASS-lock")
        need((TERMINAL / "PASS.lock").read_bytes()
             == b"PASS_ACTUAL_V2_DUAL_SEED_TERMINAL_ZERO_CREDIT_SEAL\n",
             "terminal-exact-PASS-lock")
        need(not (FINALIZER_RUN / "FAILED.lock").exists()
             and not (FINALIZER_RUN / "failure.json").exists()
             and not (TERMINAL / "FAILED.lock").exists(),
             "exclusive-PASS-no-failure")

        base = fixed["base_receipt"].document("receipt_sha256")
        terminal = fixed["terminal_receipt"].document("terminal_receipt_sha256")
        replay = fixed["terminal_replay"].document("result_sha256")
        final_result = fixed["final_result"].document("terminal_receipt_sha256")
        need(base["schema"] == BASE_SCHEMA and base["status"] == BASE_STATUS
             and base["execution_seeds"] == [30660101, 30660991]
             and base["source_pins"] == SOURCE_PINS
             and base["exact_census"] == EXPECTED_CENSUS
             and base["actual_v2_terminal_gate"] == "PENDING_COLD_REPLAY"
             and base["formal_credit"] == 0
             and base["manifest_authorized"] is False
             and base["C27R2_C28_C29"]
                 == "UNAUTHORIZED_PENDING_ACTUAL_V2_COLD_REPLAY"
             and base["CM2"] == "NO-GO_FOR_CLAIM",
             "base-seal-exact-state")
        need(terminal["schema"] == TERMINAL_SCHEMA
             and terminal["status"] == TERMINAL_STATUS
             and terminal["execution_seeds"] == [30660101, 30660991]
             and terminal["source_pins"] == SOURCE_PINS
             and terminal["exact_census"] == EXPECTED_CENSUS
             and terminal["actual_v2_terminal_seal_passed"] is True
             and terminal["formal_credit"] == 0
             and terminal["manifest_authorized"] is False
             and terminal["C27R2_C28_C29"]
                 == "AUTHORIZED_TO_BEGIN_FRESH_REBUILD_ONLY__NOT_REBUILT_NOT_CREDITED"
             and terminal["Source_G"]
                 == "ACTUAL_V2_TERMINAL_ZERO_CREDIT_AUTHORITY_RESTORED_FOR_FRESH_DOWNSTREAM_REBUILD"
             and terminal["CM2"] == "NO-GO_FOR_CLAIM",
             "terminal-receipt-exact-state")
        need(replay["schema"] == REPLAY_SCHEMA
             and replay["status"] == REPLAY_STATUS
             and replay["execution_seeds"] == [30660101, 30660991]
             and replay["exact_census"] == EXPECTED_CENSUS
             and replay["actual_v2_terminal_gate"]
                 == "PASS_COLD_REPLAY_READY_FOR_TERMINAL_RECEIPT"
             and replay["formal_credit"] == 0
             and replay["manifest_authorized"] is False
             and replay["C27R2_C28_C29"]
                 == "UNAUTHORIZED_PENDING_TERMINAL_RECEIPT"
             and replay["CM2"] == "NO-GO_FOR_CLAIM",
             "terminal-replay-exact-state")
        need(final_result == terminal
             and fixed["final_result"].raw == fixed["terminal_receipt"].raw,
             "final-result-terminal-byte-identity")

        exact_root(fixed["base_root_manifest"],
                   fixed["base_payload_manifest"].sha256, "receipt.json",
                   fixed["base_receipt"].sha256)
        exact_root(fixed["terminal_root_manifest"],
                   fixed["terminal_payload_manifest"].sha256,
                   "terminal_receipt.json", fixed["terminal_receipt"].sha256)
        need(terminal["base_seal"] == {
            "receipt_file_sha256": fixed["base_receipt"].sha256,
            "receipt_object_sha256": base["receipt_sha256"],
            "payload_manifest_file_sha256": fixed["base_payload_manifest"].sha256,
            "root_manifest_file_sha256": fixed["base_root_manifest"].sha256,
        }, "terminal-base-seal-binding")
        need(terminal["cold_replay"]["file_sha256"]
             == fixed["terminal_replay"].sha256
             and terminal["cold_replay"]["object_sha256"] == replay["result_sha256"],
             "terminal-replay-binding")

        payload_attestations: dict[str, dict[str, Any]] = {}
        for namespace, manifest_cap, count in (
            ("base", fixed["base_payload_manifest"], 56),
            ("terminal", fixed["terminal_payload_manifest"], 12),
        ):
            rows = manifest_rows(manifest_cap, count)
            for relative, expected in rows:
                cap = Capture(workspace_payload(relative),
                              namespace + ":payload:" + relative, expected)
                captures.append(cap)
                payload_attestations[namespace + ":" + relative] = cap.attest()
        need(terminal["terminal_payload_manifest"] == {
            "entry_count": 12,
            "file_sha256": fixed["terminal_payload_manifest"].sha256,
        }, "terminal-payload-descriptor")
        need(base["payload_manifest"]["entry_count"] == 56
             and base["payload_manifest"]["file_sha256"]
                 == fixed["base_payload_manifest"].sha256,
             "base-payload-descriptor")

        watcher = Capture(FINALIZER_RUN / "watcher_start.json", "watcher-start")
        captures.append(watcher)
        watcher_value = watcher.document()
        need(watcher_value["schema"]
             == "cm2.c27-actual-v2-dual-seed-finalizer-preflight.v2"
             and watcher_value["source_pins"] == SOURCE_PINS
             and watcher_value["formal_credit"] == 0
             and watcher_value["manifest_authorized"] is False,
             "watcher-start-pins-and-governance")
        for label in ("independent_verifier", "coherent_attacks", "terminal_replay"):
            need((FINALIZER_RUN / (label + ".exit_code.txt")).read_bytes() == b"0\n"
                 and (FINALIZER_RUN / (label + ".stderr.log")).read_bytes() == b"",
                 "finalizer-stage-exit0-empty-stderr:" + label)

        source_attestations = source_pin_gate(captures)
        service = service_gate(terminal["terminal_receipt_sha256"])
        for cap in captures:
            cap.attest()
        return {
            "terminal_receipt": fixed["terminal_receipt"].attest(),
            "terminal_receipt_object_sha256": terminal["terminal_receipt_sha256"],
            "terminal_replay": fixed["terminal_replay"].attest(),
            "terminal_replay_object_sha256": replay["result_sha256"],
            "base_root_manifest": fixed["base_root_manifest"].attest(),
            "base_payload_manifest": fixed["base_payload_manifest"].attest(),
            "terminal_root_manifest": fixed["terminal_root_manifest"].attest(),
            "terminal_payload_manifest": fixed["terminal_payload_manifest"].attest(),
            "base_payload_entries_verified": 56,
            "terminal_payload_entries_verified": 12,
            "all_payload_hashes_and_pre_post_stats_verified": True,
            "service": service,
            "source_attestations": source_attestations,
            "exact_census": EXPECTED_CENSUS,
        }
    finally:
        for cap in captures:
            try:
                cap.close()
            except OSError:
                pass


def negative_self_test(path: Path) -> dict[str, Any]:
    need(path.is_absolute() and not path.exists()
         and not (path == ROOT or ROOT in path.parents),
         "negative-self-test-path-must-be-absent-and-outside-workspace")
    return {
        "schema": "cm2.round306c27r2.post-actual-v2-rebuild-gate.v3",
        "status": "REJECT_STATIC_SELF_TEST_ACTUAL_V2_TERMINAL_RECEIPT_MISSING__ZERO_CREDIT",
        "decision": "REJECT", "intended_process_exit_code": 2,
        "self_test_mode": "NEGATIVE_MISSING_TERMINAL_ONLY",
        "missing_required_paths": [str(path)],
        "actual_v2_terminal_gate_validated": False,
        "fresh_C27R2_rebuild_may_start": False,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED", "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--negative-missing-self-test", type=Path)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    try:
        if args.negative_missing_self_test is not None:
            body = negative_self_test(args.negative_missing_self_test.resolve())
            exit_code = 2
        else:
            evidence = validate_positive()
            body = {
                "schema": "cm2.round306c27r2.post-actual-v2-rebuild-gate.v3",
                "status": "PASS_EXACT_ACTUAL_V2_DUAL_SEED_TERMINAL_SERVICE_RECEIPT_ROOT_PAYLOAD_AND_PASS_LOCK__FRESH_C27R2_REBUILD_MAY_BEGIN__ZERO_CREDIT",
                "decision": "PASS", "intended_process_exit_code": 0,
                "self_test_mode": None,
                "actual_v2_terminal_evidence": evidence,
                "derived_post_rebuild_contract": {
                    "initial_frozen_C15_components": 57_876,
                    "proof_derived_component_edges": 14_860,
                    "successful_DSU_merges": 14_192,
                    "cycle_edges": 668,
                    "post_C27R2_components": 43_684,
                    "member_denominator": 502_204,
                    "total_unordered_member_pairs": 126_104_177_706,
                    "post_C27R2_within_component_pairs": 542_179_508,
                    "post_C27R2_cross_component_pair_denominator": 125_561_998_198,
                    "counts_are_launch_contract_not_formal_C27R2_authority": True,
                },
                "actual_v2_terminal_gate_validated": True,
                "fresh_C27R2_rebuild_may_start": True,
                "formal_credit": 0, "manifest_authorized": False,
                "C27R2": "PREFLIGHT_GATE_PASS_ONLY__NOT_REBUILT_NOT_CREDITED",
                "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED",
                "CM2": "NO-GO_FOR_CLAIM",
            }
            exit_code = 0
        result = dict(body)
        result["gate_receipt_sha256"] = digest(result)
        write_new(output, result)
        print(canonical({"status": result["status"],
                         "gate_receipt_sha256": result["gate_receipt_sha256"],
                         "fresh_C27R2_rebuild_may_start":
                             result["fresh_C27R2_rebuild_may_start"]}).decode("ascii"))
        return exit_code
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError, subprocess.SubprocessError) as error:
        print("REJECT:" + str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
