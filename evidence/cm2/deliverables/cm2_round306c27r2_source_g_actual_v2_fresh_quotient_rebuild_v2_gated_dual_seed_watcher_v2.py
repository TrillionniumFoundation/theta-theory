#!/usr/bin/env python3
"""Gate and run the first C27R2 authority-v2 release segment.

Roles are deliberately asymmetric and exact:

* seed1: the producer consumes the terminal-pinned actual-v2 seed1 edge ledger
  and writes one fresh four-file canonical quotient candidate;
* seed2: the no-import verifier consumes the independently terminal-pinned
  seed2 edge ledger, rebuilds the mathematics, and byte-semantically verifies
  the seed1 candidate.

The post-actual gate receipt, root manifest and PASS lock are dynamic launch
pins.  Their hashes are never embedded here.  No control, candidate, verifier,
attack or run directory is created until the exact gate chain passes.  This
watcher stops before evidence bundle, outer verifier, seal and terminal replay;
therefore every success remains zero-credit and C27R2 remains unauthorized.

The explicit producer-stage fixture mode is disposable and stops immediately
after the real seed1 producer has emitted and the runner has validated the
exact four-file candidate.  It never starts the verifier, attacks or a service.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
PYTHON = Path("/usr/bin/python3.12")
PRODUCER = ROOT / (
    "deliverables/"
    "cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_"
    "producer_v2.py"
)
VERIFIER = ROOT / (
    "deliverables/"
    "cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_"
    "independent_verifier_v2.py"
)
ATTACKS = ROOT / (
    "deliverables/"
    "cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_"
    "coherent_attack_harness_v2.py"
)
RUNNER = ROOT / (
    "deliverables/"
    "cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_"
    "transaction_runner_v2.py"
)
C15 = ROOT / (
    "deliverables/"
    "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_"
    "member_component_ledger.jsonl.gz"
)
C15_SHA256 = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
GATE_SCHEMA = "cm2.round306c27r2.post-actual-v2-rebuild-gate.v3"
GATE_STATUS = (
    "PASS_EXACT_ACTUAL_V2_DUAL_SEED_TERMINAL_SERVICE_RECEIPT_ROOT_"
    "PAYLOAD_AND_PASS_LOCK__FRESH_C27R2_REBUILD_MAY_BEGIN__ZERO_CREDIT"
)
GATE_PASS_BYTES = (
    b"PASS_HARDENED_R2_POST_ACTUAL_V2_C27R2_REBUILD_GATE_V3__FRESH_REBUILD_"
    b"MAY_BEGIN__ZERO_CREDIT\n"
)
GATE_ROOT_SCHEMA = (
    "cm2.round306c27r2.post-actual-v2-rebuild-gate-execution-r2.v3"
)
GATE_ROOT_STATUS = (
    "PASS_HARDENED_R2_GATE_PRODUCER_INDEPENDENT_VERIFIER_AND_16_COHERENT_"
    "ATTACKS__FRESH_C27R2_REBUILD_MAY_BEGIN__ZERO_CREDIT"
)
PINSET_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "gated-transaction-pinset.v2"
)
PREFLIGHT_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "gated-preflight.v2"
)
COMMAND_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "process-command-spec.v2"
)
RUN_ATTESTATION_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "process-run-attestation.v2"
)
RUNNER_PASS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
RESULT_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "producer-result.v1"
)
RESULT_STATUS = (
    "PASS_FRESH_ACTUAL_V2_SEED1_QUOTIENT_REBUILD_ZERO_CREDIT__PENDING_"
    "NO_IMPORT_SEED2_VERIFICATION_ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL"
)
VERIFICATION_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "independent-verification.v1"
)
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_ACTUAL_V2_SEED2_INDEPENDENT_QUOTIENT_AND_BYTE_EXACT_"
    "CANDIDATE_REPLAY__ZERO_CREDIT_PENDING_ATTACKS_COLD_REPLAY_AND_"
    "TERMINAL_SEAL"
)
ATTACK_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "coherent-attack-harness.v1"
)
ATTACK_STATUS = (
    "PASS_BASELINE_AND_21_OF_21_COHERENT_ATTACKS_REJECTED_FAIL_CLOSED__"
    "ZERO_CREDIT_PENDING_RELEASE_CHAIN"
)
TRANSACTION_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "gated-dual-seed-transaction-receipt.v2"
)
FAILURE_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "gated-dual-seed-failure-receipt.v2"
)
OUTPUT_FILES = {
    "old": "old_c15_component_to_post_component.jsonl.gz",
    "member": "member_to_post_component.jsonl.gz",
    "census": "post_component_census.jsonl.gz",
    "result": "result.json",
}
LEDGER_CONTRACTS = {
    "old_C15_component_to_post_component": {
        "filename": OUTPUT_FILES["old"],
        "row_count": 57_876,
        "row_schema": (
            "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild."
            "v2.old-c15-component-to-post-component-row.v1"
        ),
        "ordering_field": "old_C15_component_id",
    },
    "member_to_post_component": {
        "filename": OUTPUT_FILES["member"],
        "row_count": 502_204,
        "row_schema": (
            "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild."
            "v2.member-to-post-component-row.v1"
        ),
        "ordering_field": "member_ordinal",
    },
    "post_component_census": {
        "filename": OUTPUT_FILES["census"],
        "row_count": 43_684,
        "row_schema": (
            "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild."
            "v2.post-component-census-row.v1"
        ),
        "ordering_field": "post_C27R2_component_id",
    },
}
EXPECTED_MATH = {
    "frozen_C15_members": 502_204,
    "frozen_C15_components": 57_876,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192,
    "cycle_edges": 668,
    "post_C27R2_components": 43_684,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )


def strict_load(payload: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result

    def constant(value: str) -> None:
        raise Failure("non-finite JSON:" + value)

    return json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)


def inside(raw: str | Path, *, absent: bool = False) -> Path:
    supplied = Path(raw)
    path = (ROOT / supplied if not supplied.is_absolute()
            else supplied).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Failure("path outside workspace:" + str(raw)) from error
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


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid,
    )


class Capture:
    def __init__(self, path: Path, label: str):
        self.path = inside(path)
        self.label = label
        self.fd = os.open(
            self.path,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
        )
        self.before = os.fstat(self.fd)
        need(stat.S_ISREG(self.before.st_mode) and self.before.st_nlink == 1,
             label + ":regular-single-link")
        self.sha256 = self._hash()

    def _hash(self) -> str:
        os.lseek(self.fd, 0, os.SEEK_SET)
        state = hashlib.sha256()
        while block := os.read(self.fd, 4 << 20):
            state.update(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-fd-hash")
        return state.hexdigest()

    def bytes(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        os.lseek(self.fd, 0, os.SEEK_SET)
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":stable-fd-read")
        return b"".join(chunks)

    def document(self, closure: str) -> dict[str, Any]:
        payload = self.bytes()
        need(payload.endswith(b"\n"), self.label + ":JSON-newline")
        value = strict_load(payload[:-1])
        need(type(value) is dict and canonical(value) == payload[:-1],
             self.label + ":canonical-JSON")
        body = dict(value)
        claim = body.pop(closure, None)
        need(valid_sha(claim) and claim == digest(body),
             self.label + ":object-closure")
        return value

    def attest(self) -> dict[str, Any]:
        need(fingerprint(os.fstat(self.fd)) == fingerprint(self.before),
             self.label + ":fd-pre-post-stat")
        current_path = os.stat(self.path, follow_symlinks=False)
        need(fingerprint(current_path) == fingerprint(self.before),
             self.label + ":path-pre-post-identity")
        need(self._hash() == self.sha256, self.label + ":pre-post-sha")
        return {
            "path": str(self.path.relative_to(ROOT)),
            "sha256": self.sha256,
            "size": self.before.st_size,
            "stat_fingerprint": list(fingerprint(self.before)),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_fstat_and_path_identity": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def external_sha(path: Path) -> str:
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "external regular single-link:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        need(fingerprint(os.fstat(descriptor)) == fingerprint(before),
             "external stable hash:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def file_sha(path: Path) -> str:
    return external_sha(path)


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_json(path: Path, value: Any) -> None:
    write_once(path, canonical(value) + b"\n")


def parse_manifest(payload: bytes, label: str) -> dict[str, str]:
    need(payload.endswith(b"\n"), label + ":manifest-newline")
    result: dict[str, str] = {}
    for ordinal, line in enumerate(payload.decode("ascii", "strict").splitlines()):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and valid_sha(pieces[0])
             and type(pieces[1]) is str and pieces[1] != "",
             f"{label}:manifest-row:{ordinal}")
        need(pieces[1] not in result, label + ":manifest-unique")
        result[pieces[1]] = pieces[0]
    return result


def resolve_manifest_entry(manifest_path: Path, entry: str) -> Path:
    value = Path(entry)
    need(not value.is_absolute()
         and all(part not in {"", ".", ".."} for part in value.parts),
         "canonical relative manifest entry:" + entry)
    candidates: list[Path] = []
    for raw in (manifest_path.parent / value, ROOT / value):
        path = raw.absolute()
        try:
            path.relative_to(ROOT)
        except ValueError:
            continue
        if path.exists() and not path.is_symlink() and path not in candidates:
            candidates.append(path)
    need(len(candidates) == 1,
         "manifest entry resolves exactly once:" + entry)
    return candidates[0]


def validate_gate_root_receipt(
    root_capture: Capture,
    receipt_capture: Capture,
    expected_root_object_sha256: str,
) -> tuple[dict[str, Any], list[Capture], list[str]]:
    value = root_capture.document("execution_receipt_sha256")
    need(value["execution_receipt_sha256"] == expected_root_object_sha256,
         "gate execution-root dynamic object pin")
    need(
        value.get("schema") == GATE_ROOT_SCHEMA
        and value.get("status") == GATE_ROOT_STATUS
        and value.get("mode") == "POSITIVE"
        and value.get("gate_decision") == "PASS"
        and value.get("actual_v2_terminal_gate_validated") is True
        and value.get("fresh_C27R2_rebuild_may_start") is True
        and value.get("intended_process_exit_code") == 0
        and value.get("stage_total") == 3
        and value.get("C27R2_rebuild_candidate_created") is False
        and value.get("C27R2_rebuild_output_created") is False
        and value.get("C27R2_rebuild_seal_created") is False
        and value.get("C27R2_rebuild_service_created_or_started") is False
        and value.get("formal_credit") == 0
        and value.get("manifest_authorized") is False
        and value.get("C27R2")
            == "PREFLIGHT_GATE_PASS_ONLY__NOT_REBUILT_NOT_CREDITED"
        and value.get("C28") == "UNAUTHORIZED"
        and value.get("C29") == "UNAUTHORIZED"
        and value.get("CM2") == "NO-GO_FOR_CLAIM",
        "gate execution-root exact hardened-r2 semantics",
    )
    need(value.get("gate_receipt_file_sha256") == receipt_capture.sha256,
         "execution-root binds gate receipt file")
    receipt_object = receipt_capture.document("gate_receipt_sha256")
    need(value.get("gate_receipt_object_sha256")
         == receipt_object["gate_receipt_sha256"],
         "execution-root binds gate receipt object")
    directory = root_capture.path.parent
    verification = Capture(directory / "independent_verification.json",
                           "gate-root-independent-verification")
    attacks = Capture(directory / "coherent_attacks.json",
                      "gate-root-coherent-attacks")
    captures: list[Capture] = [verification, attacks]
    try:
        need(verification.sha256
             == value["independent_verification_file_sha256"]
             and attacks.sha256 == value["coherent_attacks_file_sha256"],
             "execution-root referenced evidence file pins")
        verification_value = verification.document("verification_sha256")
        attacks_value = attacks.document("attack_result_sha256")
        need(verification_value["verification_sha256"]
             == value["independent_verification_object_sha256"]
             and attacks_value["attack_result_sha256"]
             == value["coherent_attacks_object_sha256"],
             "execution-root referenced evidence object pins")
        stages = value.get("stages")
        need(type(stages) is list and [stage.get("name") for stage in stages]
             == ["producer", "independent_verifier", "coherent_attacks"],
             "execution-root exact stage order")
        for stage in stages:
            name = stage["name"]
            exit_capture = Capture(directory / f"{name}.exit_code.txt",
                                   f"gate-root-{name}-exit")
            stderr_capture = Capture(directory / f"{name}.stderr.log",
                                     f"gate-root-{name}-stderr")
            stdout_capture = Capture(directory / f"{name}.stdout.log",
                                     f"gate-root-{name}-stdout")
            captures.extend((exit_capture, stderr_capture, stdout_capture))
            need(exit_capture.bytes() == b"0\n"
                 and stderr_capture.bytes() == b""
                 and stdout_capture.sha256 == stage["stdout_sha256"]
                 and stderr_capture.sha256 == stage["stderr_sha256"]
                 and stage["expected_exit_code"] == 0
                 and stage["observed_exit_code"] == 0
                 and stage["stderr_empty"] is True,
                 "execution-root clean stage transcript:" + name)
        source_pins = value.get("source_pins")
        need(type(source_pins) is dict
             and set(source_pins) == {
                 "producer", "independent_verifier",
                 "coherent_attack_harness", "python"}
             and source_pins["python"] == external_sha(PYTHON),
             "execution-root source pin inventory/Python")
        return value, captures, sorted(
            str(capture.path.relative_to(ROOT)) for capture in captures)
    except BaseException:
        for capture in captures:
            capture.close()
        raise


def validate_gate(args: argparse.Namespace) -> tuple[
    dict[str, Any], list[Capture], dict[str, Any]
]:
    pins = (
        args.expect_gate_receipt_file_sha256,
        args.expect_gate_receipt_object_sha256,
        args.expect_gate_root_file_sha256,
        args.expect_gate_root_object_sha256,
        args.expect_gate_pass_lock_sha256,
    )
    need(all(valid_sha(value) for value in pins), "dynamic gate SHA pins")
    receipt_path = inside(args.gate_receipt)
    root_path = inside(args.gate_root_receipt)
    pass_path = inside(args.gate_pass_lock)
    need(len({receipt_path, root_path, pass_path}) == 3,
         "distinct gate receipt/root/PASS paths")
    receipt = Capture(receipt_path, "gate-receipt")
    root = Capture(root_path, "gate-execution-root-receipt")
    lock = Capture(pass_path, "gate-pass-lock")
    captures: list[Capture] = [receipt, root, lock]
    try:
        need(receipt.sha256 == args.expect_gate_receipt_file_sha256,
             "gate receipt dynamic file pin")
        need(root.sha256 == args.expect_gate_root_file_sha256,
             "gate root dynamic file pin")
        need(lock.sha256 == args.expect_gate_pass_lock_sha256,
             "gate PASS dynamic file pin")
        need(lock.bytes() == GATE_PASS_BYTES, "gate exact PASS bytes")
        value = receipt.document("gate_receipt_sha256")
        need(value["gate_receipt_sha256"]
             == args.expect_gate_receipt_object_sha256,
             "gate receipt dynamic object pin")
        need(
            value.get("schema") == GATE_SCHEMA
            and value.get("status") == GATE_STATUS
            and value.get("decision") == "PASS"
            and value.get("actual_v2_terminal_gate_validated") is True
            and value.get("fresh_C27R2_rebuild_may_start") is True
            and value.get("formal_credit") == 0
            and value.get("manifest_authorized") is False
            and value.get("C27R2")
                == "PREFLIGHT_GATE_PASS_ONLY__NOT_REBUILT_NOT_CREDITED"
            and value.get("C28") == "UNAUTHORIZED"
            and value.get("C29") == "UNAUTHORIZED"
            and value.get("CM2") == "NO-GO_FOR_CLAIM"
            and value.get("self_test_mode") is None,
            "gate exact semantic PASS",
        )
        contract = value.get("derived_post_rebuild_contract")
        need(type(contract) is dict
             and contract.get("counts_are_launch_contract_not_formal_C27R2_authority")
                 is True
             and contract.get("member_denominator") == 502_204
             and contract.get("initial_frozen_C15_components") == 57_876
             and contract.get("proof_derived_component_edges") == 14_860
             and contract.get("successful_DSU_merges") == 14_192
             and contract.get("cycle_edges") == 668
             and contract.get("post_C27R2_components") == 43_684
             and contract.get("total_unordered_member_pairs")
                 == 126_104_177_706
             and contract.get("post_C27R2_within_component_pairs")
                 == 542_179_508
             and contract.get("post_C27R2_cross_component_pair_denominator")
                 == 125_561_998_198,
             "gate exact downstream launch contract")
        root_value, root_members, root_verified = validate_gate_root_receipt(
            root, receipt, args.expect_gate_root_object_sha256)
        captures.extend(root_members)

        evidence = value.get("actual_v2_terminal_evidence")
        need(type(evidence) is dict, "gate actual-v2 evidence")
        terminal_receipt_claim = evidence.get("terminal_receipt")
        terminal_root_claim = evidence.get("terminal_root_manifest")
        terminal_payload_claim = evidence.get("terminal_payload_manifest")
        base_root_claim = evidence.get("base_root_manifest")
        base_payload_claim = evidence.get("base_payload_manifest")
        need(all(type(item) is dict for item in (
            terminal_receipt_claim, terminal_root_claim, terminal_payload_claim,
            base_root_claim, base_payload_claim,
        )), "gate selected actual-v2 descriptors")
        descriptor_claims = {
            "actual-terminal-receipt": terminal_receipt_claim,
            "actual-terminal-root": terminal_root_claim,
            "actual-terminal-payload": terminal_payload_claim,
            "actual-base-root": base_root_claim,
            "actual-base-payload": base_payload_claim,
        }
        evidence_captures: dict[str, Capture] = {}
        for label, claim in descriptor_claims.items():
            path = inside(claim["path"])
            capture = Capture(path, label)
            captures.append(capture)
            evidence_captures[label] = capture
            need(capture.sha256 == claim["sha256"]
                 and capture.before.st_size == claim["size"],
                 label + ":gate descriptor current")
        terminal_receipt_path = evidence_captures[
            "actual-terminal-receipt"].path
        terminal_dir = terminal_receipt_path.parent
        base_dir = evidence_captures["actual-base-root"].path.parent
        terminal_pass = Capture(terminal_dir / "PASS.lock",
                                "actual-terminal-PASS")
        base_receipt = Capture(base_dir / "receipt.json", "actual-base-receipt")
        captures.extend((terminal_pass, base_receipt))
        need(terminal_pass.bytes()
             == b"PASS_ACTUAL_V2_DUAL_SEED_TERMINAL_ZERO_CREDIT_SEAL\n",
             "actual terminal exact PASS")
        terminal_value = evidence_captures[
            "actual-terminal-receipt"].document("terminal_receipt_sha256")
        need(terminal_value["terminal_receipt_sha256"]
             == evidence["terminal_receipt_object_sha256"],
             "gate terminal receipt object pin")
        base_value = base_receipt.document("receipt_sha256")
        inputs = base_value.get("root_input_capture", {}).get("attestations")
        need(type(inputs) is dict, "actual base input attestations")
        edge1 = inputs.get("seed1_full_component_edge_union")
        edge2 = inputs.get("seed2_full_component_edge_union")
        c15_claim = inputs.get("frozen_C15")
        need(all(type(item) is dict for item in (edge1, edge2, c15_claim))
             and edge1["path"] != edge2["path"]
             and edge1["sha256"] == edge2["sha256"]
             and c15_claim["path"] == str(C15.relative_to(ROOT))
             and c15_claim["sha256"] == C15_SHA256,
             "actual seed1/seed2/C15 authority claims")
        derived = {
            "actual_terminal_dir": str(terminal_dir.relative_to(ROOT)),
            "actual_base_seal_dir": str(base_dir.relative_to(ROOT)),
            "actual_terminal_root_sha256": terminal_root_claim["sha256"],
            "actual_terminal_receipt_file_sha256":
                terminal_receipt_claim["sha256"],
            "actual_terminal_receipt_object_sha256":
                evidence["terminal_receipt_object_sha256"],
            "seed1_edge_path": edge1["path"],
            "seed1_edge_sha256": edge1["sha256"],
            "seed2_edge_path": edge2["path"],
            "seed2_edge_sha256": edge2["sha256"],
            "frozen_C15_path": c15_claim["path"],
            "frozen_C15_sha256": c15_claim["sha256"],
            "gate_root_verified_member_paths": root_verified,
            "gate_execution_root_object_sha256":
                root_value["execution_receipt_sha256"],
            "authority_input_paths": sorted(set(
                [str(capture.path.relative_to(ROOT)) for capture in captures]
                + [edge1["path"], edge2["path"], c15_claim["path"]]
            )),
        }
        return value, captures, derived
    except BaseException:
        for capture in captures:
            capture.close()
        raise


def validate_source_pins(args: argparse.Namespace) -> dict[str, str]:
    expected = {
        "producer": args.expect_producer_sha256,
        "independent_verifier": args.expect_verifier_sha256,
        "coherent_attack_harness": args.expect_attack_sha256,
        "transaction_runner": args.expect_runner_sha256,
        "gated_watcher": args.expect_watcher_sha256,
        "python": args.expect_python_sha256,
    }
    need(all(valid_sha(value) for value in expected.values()),
         "all source/Python SHA pins")
    observed = {
        "producer": file_sha(PRODUCER),
        "independent_verifier": file_sha(VERIFIER),
        "coherent_attack_harness": file_sha(ATTACKS),
        "transaction_runner": file_sha(RUNNER),
        "gated_watcher": file_sha(SELF),
        "python": external_sha(PYTHON),
    }
    need(observed == expected, "all source/Python pins exact")
    return observed


def target_paths(args: argparse.Namespace) -> dict[str, Path]:
    values = {
        "control": inside(args.control_dir, absent=True),
        "producer_candidate": inside(args.producer_candidate_dir, absent=True),
        "producer_run": inside(args.producer_run_dir, absent=True),
        "verifier_output": inside(args.verifier_output_dir, absent=True),
        "verifier_run": inside(args.verifier_run_dir, absent=True),
        "attack_work": inside(args.attack_work_dir, absent=True),
        "attack_run": inside(args.attack_run_dir, absent=True),
    }
    need(len(set(values.values())) == len(values), "all transaction paths distinct")
    need(all(not path.exists() for path in values.values()),
         "all transaction paths fresh")
    return values


def pinset(
    args: argparse.Namespace,
    gate: dict[str, Any],
    derived: dict[str, Any],
    sources: dict[str, str],
    targets: dict[str, Path],
) -> dict[str, Any]:
    body = {
        "schema": PINSET_SCHEMA,
        "status": "PASS_DYNAMIC_GATE_SOURCE_ROLE_AND_FRESH_PATH_PINSET__ZERO_CREDIT",
        "gate": {
            "receipt_path": str(inside(args.gate_receipt).relative_to(ROOT)),
            "receipt_file_sha256": args.expect_gate_receipt_file_sha256,
            "receipt_object_sha256": args.expect_gate_receipt_object_sha256,
            "execution_root_receipt_path":
                str(inside(args.gate_root_receipt).relative_to(ROOT)),
            "execution_root_receipt_file_sha256":
                args.expect_gate_root_file_sha256,
            "execution_root_receipt_object_sha256":
                args.expect_gate_root_object_sha256,
            "PASS_lock_path": str(inside(args.gate_pass_lock).relative_to(ROOT)),
            "PASS_lock_sha256": args.expect_gate_pass_lock_sha256,
            "gate_status": gate["status"],
        },
        "actual_v2_authority": derived,
        "source_pins": sources,
        "roles": {
            "seed1": "PRODUCER_WRITES_EXACT_FOUR_FILE_CANONICAL_CANDIDATE",
            "seed2": "NO_IMPORT_VERIFIER_REBUILDS_FROM_SEED2_AND_VERIFIES_SEED1_CANDIDATE",
            "dual_producer_candidates": False,
            "canonical_quotient_and_three_ledger_descriptors_must_agree": True,
        },
        "targets": {name: str(path.relative_to(ROOT))
                    for name, path in targets.items()},
        "run_attacks": args.run_attacks,
        "producer_stage_fixture_only": args.producer_stage_fixture_only,
        "formal_credit": 0,
        "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_RELEASE_CHAIN",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["pinset_sha256"] = digest(result)
    return result


def command_spec(
    stage: str,
    source: Path,
    source_sha: str,
    argv: list[str],
    input_paths: list[str],
    output_roots: list[dict[str, Any]],
    stdout_status: str,
    hash_seed: str,
    timeout: int,
    pinset_path: Path,
    pinset_value: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    body = {
        "schema": COMMAND_SCHEMA,
        "stage": stage,
        "source_path": str(source),
        "source_sha256": source_sha,
        "argv": argv,
        "environment": {
            "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
            "PYTHONHASHSEED": hash_seed,
        },
        "python_hash_seed": hash_seed,
        "timeout_seconds": timeout,
        "expected_stdout_status": stdout_status,
        "input_paths": sorted(set(input_paths)),
        "output_roots": output_roots,
        "pinset_file_sha256": file_sha(pinset_path),
        "pinset_object_sha256": pinset_value["pinset_sha256"],
        "runner_source_sha256": args.expect_runner_sha256,
        "python_sha256": args.expect_python_sha256,
        "formal_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["command_spec_sha256"] = digest(result)
    return result


def launch_runner(
    stage: str,
    spec_path: Path,
    pinset_path: Path,
    run_dir: Path,
    control_dir: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    command = [
        str(PYTHON), "-I", "-B", str(RUNNER),
        "--stage", stage,
        "--command-spec", str(spec_path),
        "--pinset", str(pinset_path),
        "--run-dir", str(run_dir),
        "--expect-runner-sha256", args.expect_runner_sha256,
        "--expect-python-sha256", args.expect_python_sha256,
    ]
    completed = subprocess.run(
        command, cwd=ROOT,
        env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
             "PYTHONHASHSEED": "30662720"},
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    prefix = control_dir / (stage + "_runner")
    write_once(prefix.with_suffix(".stdout.log"), completed.stdout)
    write_once(prefix.with_suffix(".stderr.log"), completed.stderr)
    write_once(prefix.with_suffix(".exit_code.txt"),
               (str(completed.returncode) + "\n").encode("ascii"))
    need(completed.returncode == 0 and completed.stderr == b"",
         stage + " transaction runner clean exit")
    need(completed.stdout.endswith(b"\n"), stage + " runner stdout newline")
    stdout = strict_load(completed.stdout[:-1])
    need(canonical(stdout) == completed.stdout[:-1]
         and stdout == {
             "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
             "stage": stage, "status": RUNNER_PASS,
         }, stage + " runner exact stdout")
    attestation_path = run_dir / "run_attestation.json"
    attestation = closed_document(attestation_path, "run_attestation_sha256")
    need(attestation.get("schema") == RUN_ATTESTATION_SCHEMA
         and attestation.get("status") == RUNNER_PASS
         and attestation.get("stage") == stage
         and attestation.get("numeric_exit_code") == 0
         and attestation.get("signal") is None
         and attestation.get("stderr_empty") is True
         and attestation.get("input_pre_post_sha_stat_identical") is True
         and attestation.get("formal_credit") == 0,
         stage + " run attestation semantics")
    need((run_dir / "PASS.lock").read_bytes()
         == ("PASS_C27R2_AUTHORITY_V2_" + stage.upper()
             + "_PROCESS_TRANSACTION__ZERO_CREDIT\n").encode("ascii")
         and not (run_dir / "FAILED.lock").exists(),
         stage + " run exact PASS-only state")
    return attestation


def closed_document(path: Path, closure: str) -> dict[str, Any]:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "document newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical document:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "document closure:" + str(path))
    return value


def ledger_rows(path: Path, schema: str, ordering_field: str) \
        -> tuple[int, str]:
    with path.open("rb") as header_stream:
        raw = header_stream.read(10)
    need(len(raw) == 10 and raw[:2] == b"\x1f\x8b"
         and raw[4:8] == b"\x00\x00\x00\x00",
         "deterministic gzip header:" + path.name)
    count = 0
    previous: Any = None
    sequence = hashlib.sha256()
    try:
        with gzip.open(path, "rb") as stream:
            for ordinal, line in enumerate(stream):
                need(line.endswith(b"\n"), f"{path.name}:newline:{ordinal}")
                payload = line[:-1]
                row = strict_load(payload)
                need(type(row) is dict and canonical(row) == payload
                     and row.get("schema") == schema
                     and row.get("ordinal") == ordinal
                     and row.get("formal_credit") == 0,
                     f"{path.name}:canonical-schema-ordinal-credit:{ordinal}")
                body = dict(row)
                claim = body.pop("row_sha256", None)
                need(valid_sha(claim) and claim == digest(body),
                     f"{path.name}:row-closure:{ordinal}")
                key = row.get(ordering_field)
                if ordering_field == "member_ordinal":
                    need(key == ordinal, f"{path.name}:member-order:{ordinal}")
                else:
                    need(type(key) is str
                         and (previous is None or previous < key),
                         f"{path.name}:strict-order:{ordinal}")
                previous = key
                sequence.update(claim.encode("ascii") + b"\n")
                count += 1
    except (EOFError, OSError, gzip.BadGzipFile) as error:
        raise Failure("gzip integrity:" + path.name) from error
    return count, sequence.hexdigest()


def validate_candidate(candidate_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    need(candidate_dir.is_dir() and not candidate_dir.is_symlink(),
         "producer candidate directory")
    need({entry.name for entry in candidate_dir.iterdir()}
         == set(OUTPUT_FILES.values()), "producer exact four-file inventory")
    result_path = candidate_dir / OUTPUT_FILES["result"]
    result = closed_document(result_path, "result_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("status") == RESULT_STATUS
         and result.get("exact_census") == EXPECTED_MATH
         and result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False
         and result.get("C27R2")
             == "UNAUTHORIZED_PENDING_INDEPENDENT_VERIFICATION_AND_TERMINAL_SEAL"
         and result.get("CM2") == "NO-GO_FOR_CLAIM",
         "producer result exact semantics")
    descriptors = result.get("ledgers")
    need(type(descriptors) is dict
         and set(descriptors) == set(LEDGER_CONTRACTS),
         "producer exact ledger descriptor inventory")
    summary: dict[str, Any] = {}
    for name, contract in LEDGER_CONTRACTS.items():
        descriptor = descriptors[name]
        path = candidate_dir / contract["filename"]
        need(type(descriptor) is dict
             and descriptor.get("filename") == contract["filename"]
             and descriptor.get("row_count") == contract["row_count"]
             and descriptor.get("row_schema") == contract["row_schema"]
             and descriptor.get("gzip_mtime") == 0
             and descriptor.get("canonical_jsonl") is True,
             name + ":descriptor static contract")
        count, sequence = ledger_rows(
            path, contract["row_schema"], contract["ordering_field"])
        info = path.stat()
        need(count == descriptor["row_count"]
             and sequence == descriptor["row_sequence_sha256"]
             and file_sha(path) == descriptor["sha256"]
             and info.st_size == descriptor["size"]
             and info.st_nlink == 1,
             name + ":gzip/count/sequence/file closure")
        summary[name] = descriptor
    return result, summary


def validate_verification(
    verification_path: Path,
    candidate_result: dict[str, Any],
    descriptors: dict[str, Any],
    derived: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    verification = closed_document(verification_path, "verification_sha256")
    need(verification.get("schema") == VERIFICATION_SCHEMA
         and verification.get("status") == VERIFICATION_STATUS
         and verification.get("producer_imported_or_executed") is False
         and verification.get("actual_v2_seed_used") == "seed2"
         and verification.get("candidate_result_object_sha256")
             == candidate_result["result_sha256"]
         and verification.get("formal_credit") == 0
         and verification.get("manifest_authorized") is False
         and verification.get("C27R2")
             == "UNAUTHORIZED_PENDING_ATTACKS_COLD_REPLAY_AND_TERMINAL_SEAL"
         and verification.get("CM2") == "NO-GO_FOR_CLAIM",
         "independent verification exact semantics")
    projection = verification.get("mathematical_projection")
    need(type(projection) is dict
         and projection.get("terminal_receipt_object_sha256")
             == derived["actual_terminal_receipt_object_sha256"]
         and projection.get("seed1_edge_sha256")
             == derived["seed1_edge_sha256"]
         and projection.get("seed2_edge_sha256")
             == derived["seed2_edge_sha256"]
         and projection.get("C15_sha256") == C15_SHA256
         and projection.get("old_components") == 57_876
         and projection.get("edges") == 14_860
         and projection.get("merges") == 14_192
         and projection.get("cycles") == 668
         and projection.get("post_components") == 43_684
         and projection.get("members") == 502_204
         and projection.get("within_pairs") == 542_179_508
         and projection.get("cross_pairs") == 125_561_998_198
         and projection.get("candidate_result_object_sha256")
             == candidate_result["result_sha256"]
         and verification.get("mathematical_projection_sha256")
             == digest(projection),
         "seed2 independent mathematical projection")
    attestations = verification.get("candidate_attestations")
    need(type(attestations) is dict, "verifier candidate attestations")
    labels = {
        "old_C15_component_to_post_component": "candidate-old-map",
        "member_to_post_component": "candidate-member-map",
        "post_component_census": "candidate-post-census",
    }
    agreement: dict[str, Any] = {}
    for name, label in labels.items():
        descriptor = descriptors[name]
        observed = attestations.get(label)
        need(type(observed) is dict
             and Path(observed["path"]).name == descriptor["filename"]
             and observed["sha256"] == descriptor["sha256"]
             and observed["size"] == descriptor["size"],
             name + ":producer descriptor equals verifier captured file")
        agreement[name] = {
            "descriptor_sha256": digest(descriptor),
            "file_sha256": descriptor["sha256"],
            "file_size": descriptor["size"],
            "seed2_verifier_replayed_exactly": True,
        }
    return verification, agreement


def validate_attacks(path: Path) -> dict[str, Any]:
    result = closed_document(path, "attack_harness_sha256")
    need(result.get("schema") == ATTACK_SCHEMA
         and result.get("status") == ATTACK_STATUS
         and result.get("attack_count") == 21
         and result.get("rejected") == 21
         and result.get("accepted") == 0
         and result.get("authoritative_candidate_pre_post_sha256_identical")
             is True
         and result.get("formal_credit") == 0
         and result.get("manifest_authorized") is False
         and result.get("C27R2") == "UNAUTHORIZED_PENDING_RELEASE_CHAIN"
         and result.get("CM2") == "NO-GO_FOR_CLAIM",
         "21 coherent attacks exact PASS")
    return result


def watcher_failure(control: Path, stage: str, error: BaseException,
                    pinset_path: Path | None) -> dict[str, Any]:
    body = {
        "schema": FAILURE_SCHEMA,
        "status": "FAILED_CLOSED_GATED_DUAL_SEED_TRANSACTION__ZERO_CREDIT",
        "stage": stage,
        "failed_at_utc": utc_now(),
        "error": f"{type(error).__name__}:{error}",
        "pinset_file_sha256": (
            file_sha(pinset_path) if pinset_path is not None
            and pinset_path.is_file() else None
        ),
        "formal_credit": 0,
        "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED",
        "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["failure_receipt_sha256"] = digest(result)
    if not (control / "failure_receipt.json").exists():
        write_json(control / "failure_receipt.json", result)
    if not (control / "FAILED.lock").exists():
        write_once(control / "FAILED.lock",
                   b"FAILED_CLOSED_C27R2_AUTHORITY_V2_GATED_TRANSACTION\n")
    return result


def execute(args: argparse.Namespace) -> dict[str, Any]:
    # Gate validation is first and creates nothing.
    gate, gate_captures, derived = validate_gate(args)
    control: Path | None = None
    pinset_path: Path | None = None
    stage = "source_pin_and_fresh_path_preflight"
    try:
        sources = validate_source_pins(args)
        targets = target_paths(args)
        preview_pinset = pinset(args, gate, derived, sources, targets)
        if args.preflight_only:
            return {
                "schema": PREFLIGHT_SCHEMA,
                "status": "PASS_GATE_SOURCE_ROLE_AND_FRESH_PATH_PREFLIGHT_ONLY__NO_PATHS_CREATED_ZERO_CREDIT",
                "gate_receipt_object_sha256": gate["gate_receipt_sha256"],
                "pinset_object_sha256": preview_pinset["pinset_sha256"],
                "formal_credit": 0,
                "manifest_authorized": False,
                "C27R2": "NOT_STARTED",
                "CM2": "NO-GO_FOR_CLAIM",
            }

        control = targets["control"]
        control.mkdir(parents=True, mode=0o700)
        pinset_path = control / "pinset.json"
        write_json(pinset_path, preview_pinset)
        preflight_body = {
            "schema": PREFLIGHT_SCHEMA,
            "status": "PASS_DYNAMIC_GATE_SOURCE_ROLE_FRESH_PATH_AND_PINSET_PREFLIGHT__ZERO_CREDIT",
            "preflight_at_utc": utc_now(),
            "gate_receipt_object_sha256": gate["gate_receipt_sha256"],
            "pinset_file_sha256": file_sha(pinset_path),
            "pinset_object_sha256": preview_pinset["pinset_sha256"],
            "no_candidate_or_run_path_existed_at_preflight": True,
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_SEED1_PRODUCER",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        preflight = dict(preflight_body)
        preflight["preflight_sha256"] = digest(preflight)
        write_json(control / "preflight.json", preflight)

        common_inputs = derived["authority_input_paths"] + [
            str(PRODUCER.relative_to(ROOT)), str(VERIFIER.relative_to(ROOT)),
            str(ATTACKS.relative_to(ROOT)), str(RUNNER.relative_to(ROOT)),
            str(SELF.relative_to(ROOT)),
            str((control / "preflight.json").relative_to(ROOT)),
        ]
        authority_args = [
            "--terminal-dir", str(ROOT / derived["actual_terminal_dir"]),
            "--base-seal-dir", str(ROOT / derived["actual_base_seal_dir"]),
            "--expect-terminal-root-sha256",
            derived["actual_terminal_root_sha256"],
            "--expect-terminal-receipt-file-sha256",
            derived["actual_terminal_receipt_file_sha256"],
            "--expect-terminal-receipt-object-sha256",
            derived["actual_terminal_receipt_object_sha256"],
        ]

        stage = "seed1_producer"
        producer_command = [
            str(PYTHON), "-I", "-B", str(PRODUCER), *authority_args,
            "--out-dir", str(targets["producer_candidate"]),
        ]
        producer_spec = command_spec(
            "producer", PRODUCER, sources["producer"], producer_command,
            common_inputs,
            [{
                "path": str(targets["producer_candidate"]),
                "kind": "directory",
                "precondition": "ABSENT",
                "exact_inventory": sorted(OUTPUT_FILES.values()),
                "required_relative_files": sorted(OUTPUT_FILES.values()),
            }],
            RESULT_STATUS, "30662721", args.producer_timeout_seconds,
            pinset_path, preview_pinset, args,
        )
        producer_spec_path = control / "producer_command_spec.json"
        write_json(producer_spec_path, producer_spec)
        producer_attestation = launch_runner(
            "producer", producer_spec_path, pinset_path,
            targets["producer_run"], control, args)
        candidate_result, descriptors = validate_candidate(
            targets["producer_candidate"])
        candidate_validation = {
            "schema": PREFLIGHT_SCHEMA + ".candidate-validation",
            "status": "PASS_EXACT_FOUR_GZIP_CANONICAL_ORDER_COUNT_ROW_AND_RESULT_CLOSURE__ZERO_CREDIT",
            "candidate_result_file_sha256": file_sha(
                targets["producer_candidate"] / OUTPUT_FILES["result"]),
            "candidate_result_object_sha256": candidate_result["result_sha256"],
            "ledger_descriptor_projection_sha256": digest(descriptors),
            "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        write_json(control / "candidate_validation.json", candidate_validation)

        if args.producer_stage_fixture_only:
            stage = "disposable_producer_stage_fixture_receipt"
            gate_final = {capture.label: capture.attest()
                          for capture in gate_captures}
            body = {
                "schema": PREFLIGHT_SCHEMA + ".producer-stage-disposable-fixture",
                "status": (
                    "PASS_DISPOSABLE_REAL_INPUT_SEED1_PRODUCER_EXACT_FOUR_FILE_"
                    "CANDIDATE_AND_RUNNER_ATTESTATION__ZERO_CREDIT"
                ),
                "completed_at_utc": utc_now(),
                "gate_receipt_file_sha256":
                    args.expect_gate_receipt_file_sha256,
                "gate_receipt_object_sha256":
                    args.expect_gate_receipt_object_sha256,
                "gate_execution_root_file_sha256":
                    args.expect_gate_root_file_sha256,
                "gate_execution_root_object_sha256":
                    args.expect_gate_root_object_sha256,
                "gate_PASS_lock_sha256": args.expect_gate_pass_lock_sha256,
                "gate_pre_post_attestations": gate_final,
                "pinset_file_sha256": file_sha(pinset_path),
                "pinset_object_sha256": preview_pinset["pinset_sha256"],
                "candidate_dir": str(
                    targets["producer_candidate"].relative_to(ROOT)),
                "candidate_exact_inventory": sorted(OUTPUT_FILES.values()),
                "candidate_result_file_sha256": file_sha(
                    targets["producer_candidate"] / OUTPUT_FILES["result"]),
                "candidate_result_object_sha256":
                    candidate_result["result_sha256"],
                "ledger_descriptor_projection_sha256": digest(descriptors),
                "producer_run_dir": str(
                    targets["producer_run"].relative_to(ROOT)),
                "producer_run_attestation_file_sha256": file_sha(
                    targets["producer_run"] / "run_attestation.json"),
                "producer_run_attestation_object_sha256":
                    producer_attestation["run_attestation_sha256"],
                "producer_numeric_exit_code": 0,
                "producer_signal": None,
                "producer_stderr_empty": True,
                "producer_inputs_pre_post_sha_stat_identical": True,
                "verifier_output_created":
                    targets["verifier_output"].exists(),
                "verifier_run_created": targets["verifier_run"].exists(),
                "attack_work_created": targets["attack_work"].exists(),
                "attack_run_created": targets["attack_run"].exists(),
                "disposable_fixture_not_formal_transaction": True,
                "formal_credit": 0,
                "manifest_authorized": False,
                "C27R2": "UNAUTHORIZED_DISPOSABLE_PRODUCER_FIXTURE_ONLY",
                "C28_C29": "UNAUTHORIZED",
                "CM2": "NO-GO_FOR_CLAIM",
            }
            need(body["verifier_output_created"] is False
                 and body["verifier_run_created"] is False
                 and body["attack_work_created"] is False
                 and body["attack_run_created"] is False,
                 "fixture stops before all downstream paths")
            receipt = dict(body)
            receipt["producer_stage_fixture_receipt_sha256"] = digest(receipt)
            write_json(control / "producer_stage_fixture_receipt.json", receipt)
            write_once(
                control / "PASS.fixture.lock",
                b"PASS_DISPOSABLE_C27R2_AUTHORITY_V2_REAL_PRODUCER_STAGE__ZERO_CREDIT\n",
            )
            return receipt

        stage = "seed2_no_import_independent_verifier"
        targets["verifier_output"].mkdir(parents=True, mode=0o700)
        verification_path = targets["verifier_output"] / "verification.json"
        verifier_command = [
            str(PYTHON), "-I", "-B", str(VERIFIER), *authority_args,
            "--candidate-dir", str(targets["producer_candidate"]),
            "--out-file", str(verification_path),
        ]
        verifier_inputs = common_inputs + [
            str((targets["producer_candidate"] / name).relative_to(ROOT))
            for name in sorted(OUTPUT_FILES.values())
        ] + [str((control / "candidate_validation.json").relative_to(ROOT))]
        verifier_spec = command_spec(
            "independent_verifier", VERIFIER,
            sources["independent_verifier"], verifier_command, verifier_inputs,
            [{
                "path": str(targets["verifier_output"]),
                "kind": "directory",
                "precondition": "EXISTING_EMPTY_DIRECTORY",
                "exact_inventory": ["verification.json"],
                "required_relative_files": ["verification.json"],
            }],
            VERIFICATION_STATUS, "30662722", args.verifier_timeout_seconds,
            pinset_path, preview_pinset, args,
        )
        verifier_spec_path = control / "verifier_command_spec.json"
        write_json(verifier_spec_path, verifier_spec)
        verifier_attestation = launch_runner(
            "independent_verifier", verifier_spec_path, pinset_path,
            targets["verifier_run"], control, args)
        verification, agreement = validate_verification(
            verification_path, candidate_result, descriptors, derived)
        agreement_value = {
            "schema": PREFLIGHT_SCHEMA + ".dual-seed-descriptor-agreement",
            "status": "PASS_SEED1_CANONICAL_QUOTIENT_DESCRIPTORS_BOUND_BY_SEED2_NO_IMPORT_REPLAY__ZERO_CREDIT",
            "seed1_result_object_sha256": candidate_result["result_sha256"],
            "seed2_verification_object_sha256":
                verification["verification_sha256"],
            "agreements": agreement,
            "agreement_projection_sha256": digest(agreement),
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_ATTACKS_AND_RELEASE_CHAIN",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        write_json(control / "dual_seed_descriptor_agreement.json",
                   agreement_value)

        attack_attestation: dict[str, Any] | None = None
        attack_result: dict[str, Any] | None = None
        if args.run_attacks:
            stage = "coherent_attacks_after_dual_seed_pass"
            attack_result_path = targets["attack_work"] / "coherent_attacks.json"
            attack_command = [
                str(PYTHON), "-I", "-B", str(ATTACKS), *authority_args,
                "--candidate-dir", str(targets["producer_candidate"]),
                "--work-dir", str(targets["attack_work"]),
                "--out-file", str(attack_result_path),
                "--expect-verifier-sha256", sources["independent_verifier"],
                "--expect-python-sha256", sources["python"],
                "--expect-harness-sha256", sources["coherent_attack_harness"],
            ]
            attack_inputs = verifier_inputs + [
                str(verification_path.relative_to(ROOT)),
                str((control / "dual_seed_descriptor_agreement.json").relative_to(ROOT)),
            ]
            attack_spec = command_spec(
                "coherent_attacks", ATTACKS,
                sources["coherent_attack_harness"], attack_command,
                attack_inputs,
                [{
                    "path": str(targets["attack_work"]),
                    "kind": "directory", "precondition": "ABSENT",
                    "exact_inventory": None,
                    "required_relative_files": [
                        "coherent_attacks.json", "baseline_verification.json"],
                }],
                ATTACK_STATUS, "30662723", args.attack_timeout_seconds,
                pinset_path, preview_pinset, args,
            )
            attack_spec_path = control / "attack_command_spec.json"
            write_json(attack_spec_path, attack_spec)
            attack_attestation = launch_runner(
                "coherent_attacks", attack_spec_path, pinset_path,
                targets["attack_run"], control, args)
            attack_result = validate_attacks(attack_result_path)

        stage = "transaction_receipt"
        gate_final = {capture.label: capture.attest()
                      for capture in gate_captures}
        body = {
            "schema": TRANSACTION_SCHEMA,
            "status": (
                "PASS_GATE_SEED1_FOUR_FILE_CANDIDATE_SEED2_NO_IMPORT_REPLAY_"
                + ("AND_21_ATTACKS" if args.run_attacks
                   else "__ATTACKS_NOT_RUN")
                + "__ZERO_CREDIT_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
            ),
            "completed_at_utc": utc_now(),
            "gate_receipt_file_sha256": args.expect_gate_receipt_file_sha256,
            "gate_receipt_object_sha256": args.expect_gate_receipt_object_sha256,
            "gate_execution_root_file_sha256":
                args.expect_gate_root_file_sha256,
            "gate_execution_root_object_sha256":
                args.expect_gate_root_object_sha256,
            "gate_PASS_lock_sha256": args.expect_gate_pass_lock_sha256,
            "gate_pre_post_attestations": gate_final,
            "pinset_file_sha256": file_sha(pinset_path),
            "pinset_object_sha256": preview_pinset["pinset_sha256"],
            "seed1": {
                "role": "PRODUCER",
                "actual_edge_sha256": derived["seed1_edge_sha256"],
                "candidate_result_file_sha256": file_sha(
                    targets["producer_candidate"] / OUTPUT_FILES["result"]),
                "candidate_result_object_sha256":
                    candidate_result["result_sha256"],
                "ledger_descriptor_projection_sha256": digest(descriptors),
                "run_attestation_file_sha256": file_sha(
                    targets["producer_run"] / "run_attestation.json"),
                "run_attestation_object_sha256":
                    producer_attestation["run_attestation_sha256"],
            },
            "seed2": {
                "role": "NO_IMPORT_INDEPENDENT_VERIFIER",
                "actual_edge_sha256": derived["seed2_edge_sha256"],
                "verification_file_sha256": file_sha(verification_path),
                "verification_object_sha256":
                    verification["verification_sha256"],
                "run_attestation_file_sha256": file_sha(
                    targets["verifier_run"] / "run_attestation.json"),
                "run_attestation_object_sha256":
                    verifier_attestation["run_attestation_sha256"],
            },
            "dual_seed_descriptor_agreement": agreement_value,
            "coherent_attacks": (
                None if attack_result is None else {
                    "file_sha256": file_sha(
                        targets["attack_work"] / "coherent_attacks.json"),
                    "object_sha256": attack_result["attack_harness_sha256"],
                    "run_attestation_object_sha256":
                        attack_attestation["run_attestation_sha256"],
                }
            ),
            "exact_process_closures": {
                "gate_passed_before_any_transaction_directory": True,
                "seed1_numeric_exit0_signal_null_stderr_empty_pre_post": True,
                "seed1_exact_four_gzip_canonical_count_closure": True,
                "seed2_numeric_exit0_signal_null_stderr_empty_pre_post": True,
                "seed2_no_import_independent_full_candidate_replay": True,
                "canonical_quotient_and_three_descriptors_agree": True,
                "attacks_started_only_after_seed1_and_seed2_pass":
                    args.run_attacks,
                "outer_verifier_or_seal_or_terminal_replay_created": False,
            },
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27R2": "UNAUTHORIZED_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY",
            "C28_C29": "UNAUTHORIZED",
            "Source_W": "UNCHANGED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        receipt = dict(body)
        receipt["transaction_receipt_sha256"] = digest(receipt)
        write_json(control / "transaction_receipt.json", receipt)
        write_once(control / "PASS.lock",
                   b"PASS_C27R2_AUTHORITY_V2_GATED_DUAL_SEED_CORE__ZERO_CREDIT\n")
        return receipt
    except BaseException as error:
        if control is not None and control.exists():
            watcher_failure(control, stage, error, pinset_path)
        raise
    finally:
        for capture in gate_captures:
            capture.close()


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--gate-receipt", required=True)
    value.add_argument("--gate-root-receipt", required=True)
    value.add_argument("--gate-pass-lock", required=True)
    value.add_argument("--expect-gate-receipt-file-sha256", required=True)
    value.add_argument("--expect-gate-receipt-object-sha256", required=True)
    value.add_argument("--expect-gate-root-file-sha256", required=True)
    value.add_argument("--expect-gate-root-object-sha256", required=True)
    value.add_argument("--expect-gate-pass-lock-sha256", required=True)
    value.add_argument("--expect-producer-sha256", required=True)
    value.add_argument("--expect-verifier-sha256", required=True)
    value.add_argument("--expect-attack-sha256", required=True)
    value.add_argument("--expect-runner-sha256", required=True)
    value.add_argument("--expect-watcher-sha256", required=True)
    value.add_argument("--expect-python-sha256", required=True)
    value.add_argument("--control-dir", required=True)
    value.add_argument("--producer-candidate-dir", required=True)
    value.add_argument("--producer-run-dir", required=True)
    value.add_argument("--verifier-output-dir", required=True)
    value.add_argument("--verifier-run-dir", required=True)
    value.add_argument("--attack-work-dir", required=True)
    value.add_argument("--attack-run-dir", required=True)
    value.add_argument("--run-attacks", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    value.add_argument("--producer-stage-fixture-only", action="store_true")
    value.add_argument("--producer-timeout-seconds", type=int, default=7_200)
    value.add_argument("--verifier-timeout-seconds", type=int, default=10_800)
    value.add_argument("--attack-timeout-seconds", type=int, default=43_200)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        need(all(60 <= value <= 86_400 for value in (
            args.producer_timeout_seconds, args.verifier_timeout_seconds,
            args.attack_timeout_seconds,
        )), "bounded stage timeouts")
        need(not (args.preflight_only and args.producer_stage_fixture_only)
             and not (args.run_attacks and args.producer_stage_fixture_only),
             "mutually exclusive preflight/fixture/attack modes")
        result = execute(args)
        sys.stdout.buffer.write(canonical({
            "CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0,
            "status": result["status"],
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
