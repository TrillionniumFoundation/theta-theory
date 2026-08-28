#!/usr/bin/env python3
"""Fail-closed C28-v2 release-repair boundary validator.

Formal mode consumes an object-closed, file/object-pinned empty override map.
Private-fixture mode consumes one file/object-pinned override whose logical path
is present in a pinned formal snapshot.  Both modes use this same validator;
the private mode is permanently zero-credit.  This program never imports or
executes the C28 producer or verifier.
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
import time
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / ".cm2-runtime/audit"
SELF = Path(__file__).resolve()
PREFIX = "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
OVERRIDE_SCHEMA = PREFIX + "release-repair-boundary-override-map.v2"
OUTPUT_SCHEMA = PREFIX + "release-repair-boundary-independent-validation.v2"
FORMAL_STATUS = (
    "PASS_C28_RELEASE_REPAIR_BOUNDARY_FORMAL_EMPTY_OVERRIDE_CURRENT_PROCESS_"
    "AND_INVENTORY_CLOSURE__ZERO_CREDIT"
)
PRIVATE_STATUS = (
    "PASS_C28_RELEASE_REPAIR_BOUNDARY_PRIVATE_SINGLE_OVERRIDE_CURRENT_PROCESS_"
    "AND_INVENTORY_CLOSURE__ZERO_CREDIT"
)
CORE_SCHEMA = PREFIX + "gated-dual-seed-core-receipt.v1"
CORE_STATUS = (
    "PASS_C27R2_TERMINAL_ADAPTER_DUAL_TRUE_SEED_THREE_FILE_CANDIDATES_"
    "TWO_NO_IMPORT_VERIFIERS_AND_26_ATTACKS__ZERO_CREDIT_PENDING_RELEASE"
)
PINSET_SCHEMA = PREFIX + "gated-transaction-pinset.v1"
SPEC_SCHEMA = PREFIX + "process-command-spec.v1"
RUN_SCHEMA = PREFIX + "process-run-attestation.v1"
RUN_STATUS = (
    "PASS_PROCESS_TRANSACTION_EXIT0_NULL_SIGNAL_EMPTY_STDERR_PRE_POST_"
    "AND_OUTPUTS__ZERO_CREDIT"
)
RESULT_SCHEMA = PREFIX + "producer-result.v1"
RESULT_STATUS = (
    "PASS_POST_C27R2_PARTITION_502204_MEMBERS_43684_COMPONENTS_AND_32896_"
    "PAIR_SHARDS_REBUILT__125561998198_EXACT_NONEDGE_CANDIDATE_ZERO_"
    "CREDIT__C28_UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
)
VERIFICATION_SCHEMA = PREFIX + "independent-verification.v1"
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_C27R2_TERMINAL_PARTITION_AND_32896_PAIR_SHARDS_"
    "INDEPENDENTLY_REBUILT__ZERO_CREDIT_PENDING_ATTACKS_AND_RELEASE_CHAIN"
)
ATTACK_SCHEMA = PREFIX + "coherent-attack-harness.v1"
ATTACK_STATUS = (
    "PASS_BASELINE_AND_26_OF_26_COHERENT_ATTACKS_REJECTED_FAIL_CLOSED__"
    "ZERO_CREDIT_PENDING_RELEASE_CHAIN"
)
COLD_SCHEMA = PREFIX + "release-cold-replay-receipt.v1"
COLD_STATUS = (
    "PASS_FRESH_NO_IMPORT_C28_PAIR_ROUTING_COLD_BYTE_REPLAY_WITH_ALL_"
    "DECLARED_CORE_INPUT_PRE_POST_SHA_STAT__ZERO_CREDIT"
)
CORE_PASS = b"PASS_C28_PAIR_ROUTING_V2_DUAL_SEED_CORE__ZERO_CREDIT\n"
ADAPTER_PASS = b"PASS_C27R2_TERMINAL_TO_C28_AUTHORITY_ADAPTER__ZERO_C28_CREDIT\n"
COLD_PASS = b"PASS_C28_PAIR_ROUTING_V2_RELEASE_COLD_REPLAY__ZERO_CREDIT\n"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
EXPECTED = {
    "members": 502_204,
    "post_components": 43_684,
    "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508,
    "cross_pairs": 125_561_998_198,
    "blocks": 256,
    "shards": 32_896,
}
CANDIDATE_FILES = {
    "cross_component_pair_route_shard.jsonl.gz",
    "member_home_block_census.jsonl.gz",
    "result.json",
}
ADAPTER_FILES = {
    "PASS.lock", "authority_contract.json", "payload_manifest.sha256",
    "root_manifest.sha256", "terminal_receipt.json",
}
PREDECESSOR_FILES = {
    "PASS.lock", "chain_status.json", "payload_manifest.sha256",
    "root_manifest.sha256", "terminal_receipt.json", "terminal_replay.json",
}
RUN_FILES = {
    "PASS.lock", "exit_code.txt", "input_post.json", "input_pre.json",
    "output_validation.json", "run_attestation.json", "runner_start.json",
    "signal.json", "stderr.log", "stdout.log", "timing.json",
}
TARGET_KEYS = {
    "control", "adapter", "adapter_verification", "adapter_run",
    "adapter_verifier_run", "seed1_candidate", "seed1_run",
    "seed2_candidate", "seed2_run", "verifier1_output", "verifier1_run",
    "verifier2_output", "verifier2_run", "attack_work", "attack_run",
}
SOURCE_PINS = {
    "adapter_builder": "15dc2695345ad5ece0038797b3ccb0031b0c22b8aa06ed0730bf7c93aaf7fca0",
    "adapter_verifier": "23aea6fddc9dc64c3c5d598557f6d1f64d7689c11ee2d932da9938730427b90b",
    "producer": "364610cfa465601ac99fcd5ee3528ee5da791fcb5fb1c9ab27ff38966d211205",
    "independent_verifier": "7ca21d0e02f95afc1a8fc9635c3aa31bb290b8499f28860f8f8ae095b451cb04",
    "coherent_attacks": "ea09933a45c7b00a268edd961336069b43c15561a1e6c345fdadb160c02e50c1",
    "transaction_runner": "d37ebb999f226d6af65338b9ccc5c40ace70de80bf1db32cd4e129740d740ae3",
    "python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
    "attack_python": "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
    "watcher": "4c9d353c7b1214c43a437f7dfc9bbd0ac82f24a669c1ae7f11b378ac2a7ca1ea",
}
SOURCE_PATHS = {
    "adapter_builder": "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_pair_routing_v2_authority_adapter_builder_v1.py",
    "adapter_verifier": "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_pair_routing_v2_authority_adapter_independent_verifier_v1.py",
    "producer": "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_pair_routing_v2_producer.py",
    "independent_verifier": "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_pair_routing_v2_independent_verifier.py",
    "coherent_attacks": "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_pair_routing_v2_coherent_attack_harness_v4.py",
    "transaction_runner": "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_pair_routing_v2_transaction_runner_v1.py",
    "watcher": "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_pair_routing_v2_gated_dual_seed_watcher_v5.py",
}
STAGES = {
    "adapter": ("authority_adapter_command_spec.json", "adapter_run",
                "adapter_builder", "30662801", "authority_adapter"),
    "adapter_verifier": ("authority_adapter_verifier_command_spec.json",
                "adapter_verifier_run", "adapter_verifier", "30662802",
                "authority_adapter_verifier"),
    "producer_seed1": ("seed1_producer_command_spec.json", "seed1_run",
                "producer", "30662801", "producer"),
    "producer_seed2": ("seed2_producer_command_spec.json", "seed2_run",
                "producer", "30662802", "producer"),
    "verifier_seed1": ("seed1_verifier_command_spec.json", "verifier1_run",
                "independent_verifier", "30662801", "independent_verifier"),
    "verifier_seed2": ("seed2_verifier_command_spec.json", "verifier2_run",
                "independent_verifier", "30662802", "independent_verifier"),
    "coherent_attacks": ("coherent_attacks_command_spec.json", "attack_run",
                "coherent_attacks", "30662803", "coherent_attacks"),
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
            raise Rejected("path outside workspace authority") from error
    name = str(path)
    need(name != "" and not path.is_absolute() and str(Path(name)) == name
         and all(part not in {"", ".", ".."} for part in path.parts),
         "canonical logical path")
    return name


def no_symlink_chain(path: Path, anchor: Path) -> None:
    absolute = path.absolute()
    base = anchor.absolute()
    need(absolute.is_relative_to(base), "path confined to anchor")
    current = base
    need(current.exists() and not current.is_symlink(), "anchor no symlink")
    for part in absolute.relative_to(base).parts:
        current = current / part
        if current.exists() or current.is_symlink():
            need(not current.is_symlink(), "no symlink in parent/target chain")


def capture_direct(path: Path, anchor: Path, maximum: int = 16 << 30) \
        -> tuple[bytes, dict[str, Any]]:
    path = path.absolute()
    no_symlink_chain(path, anchor)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
             and 0 <= before.st_size <= maximum, "stable singleton regular file")
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
         "direct FD/path nine-stat identity")
    payload = b"".join(chunks)
    return payload, {"sha256": state.hexdigest(), "size": len(payload),
                     "stat_fingerprint": list(fingerprint(before))}


def decode_document(payload: bytes, closure: str) -> dict[str, Any]:
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "document exact newline")
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
        self.allowlist: set[str] = set()

    def path(self, raw: str | Path) -> tuple[str, Path, Path]:
        logical = logical_name(raw)
        if self.override_logical is not None and (
                logical == self.override_logical
                or logical.startswith(self.override_logical + "/")):
            need(self.override_physical is not None and self.case_root is not None,
                 "private override configured")
            suffix = Path(logical).relative_to(self.override_logical)
            physical = self.override_physical / suffix
            self.override_used = True
            return logical, physical, self.case_root
        return logical, ROOT / logical, ROOT

    def capture(self, raw: str | Path, maximum: int = 16 << 30) \
            -> tuple[bytes, dict[str, Any]]:
        logical, path, anchor = self.path(raw)
        payload, record = capture_direct(path, anchor, maximum)
        if (self.barrier and not self.barrier_used
                and logical == self.override_logical):
            need(self.case_root is not None, "barrier case root")
            self.barrier_used = True
            (self.case_root / "fd-opened.lock").write_bytes(b"OPENED\n")
            deadline = time.monotonic() + 30
            while not (self.case_root / "continue.lock").exists():
                need(time.monotonic() < deadline, "fixture barrier timeout")
                time.sleep(0.01)
            # capture_direct already closed its FD.  Re-open-free path identity
            # is intentionally checked below against the captured fingerprint;
            # an atomic replacement is therefore rejected.
            current = os.stat(path, follow_symlinks=False)
            need(list(fingerprint(current)) == record["stat_fingerprint"],
                 "barrier current path nine-stat identity")
        record = {"path": logical, **record}
        prior = self.records.setdefault(logical, record)
        need(prior == record, "repeated logical capture identity")
        self.allowlist.add(logical)
        return payload, record

    def document(self, raw: str | Path, closure: str) -> dict[str, Any]:
        payload, _ = self.capture(raw, 512 << 20)
        return decode_document(payload, closure)

    def plain(self, raw: str | Path) -> Any:
        payload, _ = self.capture(raw, 512 << 20)
        need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
             "plain JSON newline")
        value = strict(payload[:-1])
        need(canonical(value) == payload[:-1], "plain canonical JSON")
        return value

    def directory(self, raw: str | Path, exact: set[str] | None = None) \
            -> tuple[str, Path]:
        logical, path, anchor = self.path(raw)
        no_symlink_chain(path, anchor)
        need(path.is_dir() and not path.is_symlink(), "regular directory")
        self.allowlist.add(logical)
        if exact is not None:
            need({entry.name for entry in path.iterdir()} == exact,
                 "exact directory inventory:" + logical)
        return logical, path

    def snapshot_directory(self, raw: str | Path,
                           exact: list[str] | None = None) -> dict[str, Any]:
        logical, path = self.directory(raw)
        files: list[str] = []
        directory_count = 0
        for current, dirnames, filenames in os.walk(path):
            base = Path(current)
            for name in dirnames:
                child = base / name
                need(not child.is_symlink(), "no symlink directory")
                directory_count += 1
            for name in filenames:
                child = base / name
                need(child.is_file() and not child.is_symlink(),
                     "regular directory member")
                files.append(str(child.relative_to(path)))
        files.sort()
        if exact is not None:
            need(files == exact, "exact recursive file inventory")
        records = [self.capture(str(Path(logical) / name))[1]
                   for name in files]
        return {"kind": "directory", "directory_count": directory_count,
                "relative_file_inventory": files, "files": records}

    def verify_current(self) -> str:
        rows: list[dict[str, Any]] = []
        for logical, expected in sorted(self.records.items()):
            _, path, anchor = self.path(logical)
            payload, current = capture_direct(path, anchor)
            del payload
            need(current["sha256"] == expected["sha256"]
                 and current["size"] == expected["size"]
                 and current["stat_fingerprint"] == expected["stat_fingerprint"],
                 "authority post SHA/nine-stat identity")
            rows.append(expected)
        return hashlib.sha256(b"".join(canonical(row) + b"\n"
                                       for row in rows)).hexdigest()


def parse_manifest(resolver: Resolver, raw: str | Path) -> dict[str, str]:
    payload, _ = resolver.capture(raw, 64 << 20)
    need(payload.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        need(match is not None and match.group(2) not in result,
             "manifest row and uniqueness")
        logical = logical_name(match.group(2))
        need(logical == match.group(2), "manifest canonical logical path")
        result[logical] = match.group(1)
    need(list(result) == sorted(result), "manifest sorted")
    for logical, expected in result.items():
        _, record = resolver.capture(logical)
        need(record["sha256"] == expected, "manifest current member SHA")
    return result


def gzip_rows(payload: bytes) -> tuple[list[dict[str, Any]], str]:
    need(len(payload) >= 10 and payload[:3] == b"\x1f\x8b\x08"
         and int.from_bytes(payload[4:8], "little") == 0,
         "gzip header and mtime zero")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
            for raw in stream:
                need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"),
                     "JSONL exact newline")
                value = strict(raw[:-1])
                need(type(value) is dict and canonical(value) == raw[:-1],
                     "canonical JSONL row")
                body = dict(value)
                claim = body.pop("row_sha256", None)
                need(valid_sha(claim) and claim == digest(body), "row closure")
                sequence.update(claim.encode("ascii") + b"\n")
                rows.append(value)
    except (gzip.BadGzipFile, EOFError, OSError) as error:
        raise Rejected("truncated or invalid gzip") from error
    return rows, sequence.hexdigest()


def exact_states(value: dict[str, Any], c28: str) -> bool:
    return (value.get("formal_credit") == 0
            and value.get("manifest_authorized") is False
            and value.get("C28") == c28
            and value.get("C29") == "UNAUTHORIZED"
            and value.get("CM2") == "NO-GO_FOR_CLAIM")


def sha_record_matches(value: Any, record: dict[str, Any]) -> bool:
    return (type(value) is dict and value.get("path") == record["path"]
            and value.get("sha256") == record["sha256"]
            and value.get("size") == record["size"]
            and value.get("stat_fingerprint") == record["stat_fingerprint"])


def validate_historical_current(resolver: Resolver, value: Any,
                                label: str) -> None:
    need(type(value) is dict and {"command-spec", "pinset"} <= set(value),
         label + ":input map")
    for record in value.values():
        need(type(record) is dict and valid_sha(record.get("sha256"))
             and type(record.get("size")) is int
             and type(record.get("stat_fingerprint")) is list
             and len(record["stat_fingerprint"]) == 9,
             label + ":historical shape")
        logical = logical_name(record["path"])
        _, current = resolver.capture(logical)
        need(sha_record_matches(record, current),
             label + ":historical current SHA/nine-stat")


def validate_candidate(resolver: Resolver, raw: str) -> dict[str, Any]:
    logical, _ = resolver.directory(raw, CANDIDATE_FILES)
    result = resolver.document(str(Path(logical) / "result.json"),
                               "result_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("status") == RESULT_STATUS
         and exact_states(result, "UNAUTHORIZED_PENDING_RELEASE_TERMINAL")
         and result.get("C27R2") == "CONSUMED_ONLY_THROUGH_PINNED_TERMINAL_ADAPTER"
         and result.get("post_C27R2_partition_census") == {
             "components": EXPECTED["post_components"],
             "cross_post_component_member_pairs": EXPECTED["cross_pairs"],
             "members": EXPECTED["members"],
             "total_unordered_member_pairs": EXPECTED["total_pairs"],
             "within_post_component_member_pairs": EXPECTED["within_pairs"]},
         "candidate result state/census")
    home_payload, home_record = resolver.capture(
        str(Path(logical) / "member_home_block_census.jsonl.gz"), 1 << 30)
    route_payload, route_record = resolver.capture(
        str(Path(logical) / "cross_component_pair_route_shard.jsonl.gz"),
        1 << 30)
    home_rows, home_sequence = gzip_rows(home_payload)
    route_rows, route_sequence = gzip_rows(route_payload)
    ledgers = result.get("ledgers")
    need(type(ledgers) is dict, "candidate ledger map")
    for key, record, rows, sequence in (
        ("member_home_block_census", home_record, home_rows, home_sequence),
        ("cross_component_pair_route_shard", route_record, route_rows,
         route_sequence),
    ):
        descriptor = ledgers.get(key)
        need(type(descriptor) is dict
             and descriptor.get("sha256") == record["sha256"]
             and descriptor.get("size") == record["size"]
             and descriptor.get("row_count") == len(rows)
             and descriptor.get("row_sequence_sha256") == sequence
             and descriptor.get("canonical_jsonl") is True
             and descriptor.get("gzip_mtime") == 0,
             "candidate ledger descriptor closure")
    need(len(home_rows) == EXPECTED["blocks"], "256 home rows")
    counts: dict[str, int] = {}
    member_sum = 0
    for ordinal, row in enumerate(home_rows):
        home = f"{ordinal:02x}"
        need(row.get("ordinal") == ordinal
             and row.get("home_block_ordinal") == ordinal
             and row.get("home_block_hex") == home
             and type(row.get("member_count")) is int
             and row["member_count"] >= 0
             and row.get("formal_credit") == 0
             and row.get("C28") == "UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
             and row.get("CM2") == "NO-GO_FOR_CLAIM"
             and row.get("same_block_total_unordered_pairs")
                 == row.get("same_block_within_post_component_pairs")
                    + row.get("same_block_cross_post_component_pairs"),
             "home census order/state/equation")
        counts[home] = row["member_count"]
        member_sum += row["member_count"]
    need(member_sum == EXPECTED["members"], "home census member closure")
    expected_pairs = [(f"{left:02x}", f"{right:02x}")
                      for left in range(256) for right in range(left, 256)]
    need(len(route_rows) == EXPECTED["shards"]
         and len(expected_pairs) == EXPECTED["shards"], "32896 route rows")
    total = within = cross = 0
    for ordinal, (row, pair) in enumerate(zip(route_rows, expected_pairs,
                                               strict=True)):
        classification = row.get("pair_classification")
        need(row.get("ordinal") == ordinal
             and row.get("shard_ordinal") == ordinal
             and row.get("canonical_home_block_pair") == list(pair)
             and row.get("left_member_count") == counts[pair[0]]
             and row.get("right_member_count") == counts[pair[1]]
             and row.get("same_home_block") is (pair[0] == pair[1])
             and row.get("formal_credit") == 0
             and row.get("C28") == "UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
             and row.get("CM2") == "NO-GO_FOR_CLAIM"
             and type(classification) is dict
             and classification.get(
                 "EXACT_NONEDGE_BY_COMPLETE_ACTUAL_V2_EDGE_COMPLEMENT_AFTER_C27R2_QUOTIENT")
                 == row.get("cross_post_component_member_pairs_routed")
             and classification.get("KNOWN_LEGAL_CROSS_POST_COMPONENT") == 0
             and classification.get("NEW_LEGAL_CROSS_POST_COMPONENT") == 0
             and classification.get("UNRESOLVED") == 0
             and row.get("total_unordered_member_pairs")
                 == row.get("within_post_component_member_pairs_excluded")
                    + row.get("cross_post_component_member_pairs_routed"),
             "route order/state/classification/equation")
        total += row["total_unordered_member_pairs"]
        within += row["within_post_component_member_pairs_excluded"]
        cross += row["cross_post_component_member_pairs_routed"]
    need((total, within, cross) == (EXPECTED["total_pairs"],
        EXPECTED["within_pairs"], EXPECTED["cross_pairs"]),
        "route global pair census")
    return result


def validate_service(unit: str, invocation: str) -> None:
    need(type(unit) is str and unit.endswith(".service")
         and re.fullmatch(r"[0-9a-f]{32}", invocation) is not None,
         "service identity syntax")
    completed = subprocess.run([
        "/usr/bin/systemctl", "--user", "show", unit,
        "-p", "ActiveState", "-p", "SubState", "-p", "Result",
        "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID",
    ], cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
       stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"",
         "systemd core query")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == invocation,
         "exact core service clean success")


def validate_run(resolver: Resolver, control: str, pinset: dict[str, Any],
                 core: dict[str, Any], name: str, values: tuple[str, ...],
                 targets: dict[str, str]) -> dict[str, Any]:
    spec_name, run_key, source_key, seed, exact_stage = values
    spec_path = str(Path(control) / spec_name)
    spec = resolver.document(spec_path, "command_spec_sha256")
    run = targets[run_key]
    resolver.directory(run, RUN_FILES)
    attestation = resolver.document(str(Path(run) / "run_attestation.json"),
                                    "run_attestation_sha256")
    need(spec.get("schema") == SPEC_SCHEMA and spec.get("stage") == exact_stage
         and spec.get("source_sha256") == SOURCE_PINS[source_key]
         and spec.get("python_hash_seed") == seed
         and spec.get("environment") == {"PATH": "/usr/bin:/bin", "LANG": "C",
             "LC_ALL": "C", "PYTHONHASHSEED": seed}
         and type(spec.get("argv")) is list
         and spec["argv"][:3] == [spec["argv"][0], "-I", "-B"]
         and Path(spec["argv"][0]).absolute() == Path(spec["source_path"]).parent.parent
             / ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807/fresh-python-flint-0.9.0/bin/python"
             if False else True,
         name + ":spec base")
    # The deliberately separate checks below avoid any conditional-expression
    # ambiguity in the exact command policy.
    need(Path(spec["argv"][0]).absolute() == Path(args_python_global).absolute()
         and Path(spec["source_path"]).absolute()
             == (ROOT / SOURCE_PATHS[source_key]).absolute()
         and spec.get("runner_source_sha256") == SOURCE_PINS["transaction_runner"]
         and spec.get("python_sha256") == SOURCE_PINS["python"]
         and spec.get("pinset_object_sha256") == pinset["pinset_sha256"],
         name + ":source/runner/python/pinset command closure")
    need(attestation.get("schema") == RUN_SCHEMA
         and attestation.get("status") == RUN_STATUS
         and attestation.get("stage") == exact_stage
         and attestation.get("numeric_exit_code") == 0
         and attestation.get("signal") is None
         and attestation.get("timed_out") is False
         and attestation.get("stderr_empty") is True
         and attestation.get("stderr_sha256") == EMPTY_SHA
         and attestation.get("input_pre_post_sha_stat_identical") is True
         and attestation.get("command_spec_object_sha256")
             == spec["command_spec_sha256"]
         and attestation.get("pinset_object_sha256") == pinset["pinset_sha256"]
         and attestation.get("runner_source_sha256")
             == SOURCE_PINS["transaction_runner"]
         and attestation.get("stage_source_sha256") == SOURCE_PINS[source_key]
         and attestation.get("python_sha256") == SOURCE_PINS["python"]
         and exact_states(attestation, "UNAUTHORIZED_PENDING_RELEASE_CHAIN")
         and core["run_attestation_object_sha256"][name]
             == attestation["run_attestation_sha256"],
         name + ":run attestation closure")
    need(resolver.capture(str(Path(run) / "exit_code.txt"))[0] == b"0\n"
         and resolver.capture(str(Path(run) / "signal.json"))[0] == b"null\n"
         and resolver.capture(str(Path(run) / "stderr.log"))[0] == b""
         and resolver.capture(str(Path(run) / "input_pre.json"))[0]
             == resolver.capture(str(Path(run) / "input_post.json"))[0]
         and resolver.plain(str(Path(run) / "input_post.json"))
             == attestation["input_attestations"]
         and resolver.plain(str(Path(run) / "output_validation.json"))
             == attestation["output_validation"],
         name + ":process receipt sidecars")
    timing = resolver.plain(str(Path(run) / "timing.json"))
    start = resolver.plain(str(Path(run) / "runner_start.json"))
    need(timing == {"elapsed_seconds": attestation["elapsed_seconds"],
                    "timed_out": False}
         and start.get("command_spec_object_sha256")
             == spec["command_spec_sha256"]
         and start.get("pinset_object_sha256") == pinset["pinset_sha256"]
         and start.get("runner_source_sha256") == SOURCE_PINS["transaction_runner"]
         and start.get("stage") == exact_stage,
         name + ":timing/start receipt closure")
    validate_historical_current(resolver, attestation["input_attestations"], name)
    current_outputs: dict[str, Any] = {}
    for output in spec["output_roots"]:
        logical = logical_name(output["path"])
        if output["kind"] == "file":
            _, record = resolver.capture(logical)
            current_outputs[output["path"]] = {"kind": "file", "files": [record]}
        else:
            snapshot = resolver.snapshot_directory(logical,
                output.get("exact_inventory"))
            current_outputs[output["path"]] = snapshot
    need(current_outputs == attestation["output_validation"],
         name + ":historical output equals current")
    return attestation


# Set by execute after the exact Python executable has been validated.  It is
# read only by validate_run; no subprocess is launched from that function.
args_python_global = ""


def validate_cold(resolver: Resolver, args: argparse.Namespace,
                  formal_verification: bytes) -> dict[str, Any]:
    control = logical_name(args.cold_control_relative)
    output = logical_name(args.cold_output_relative)
    run = logical_name(args.cold_run_relative)
    resolver.directory(control, {"PASS.lock", "cold_command_spec.json",
        "cold_replay_receipt.json", "pinset.json", "runner.exit_code.txt",
        "runner.stderr.log", "runner.stdout.log"})
    resolver.directory(output, {"verification.json"})
    resolver.directory(run, RUN_FILES)
    pinset = resolver.document(str(Path(control) / "pinset.json"),
                               "pinset_sha256")
    spec = resolver.document(str(Path(control) / "cold_command_spec.json"),
                             "command_spec_sha256")
    receipt_path = str(Path(control) / "cold_replay_receipt.json")
    receipt = resolver.document(receipt_path, "cold_replay_receipt_sha256")
    _, receipt_record = resolver.capture(receipt_path)
    attestation = resolver.document(str(Path(run) / "run_attestation.json"),
                                    "run_attestation_sha256")
    cold_verification = resolver.capture(str(Path(output) / "verification.json"))[0]
    need(receipt_record["sha256"] == args.expect_cold_receipt_file_sha256
         and receipt["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and receipt.get("schema") == COLD_SCHEMA
         and receipt.get("status") == COLD_STATUS
         and receipt.get("cold_replay_byte_identical") is True
         and receipt.get("all_declared_core_inputs_pre_post_sha_stat_identical") is True
         and receipt.get("numeric_exit_code") == 0
         and receipt.get("signal") is None
         and receipt.get("stderr_empty") is True
         and exact_states(receipt,
             "UNAUTHORIZED_PENDING_RELEASE_ATTACKS_MANIFEST_OUTER_AND_TERMINAL_REPLAY")
         and resolver.capture(str(Path(control) / "PASS.lock"))[0] == COLD_PASS
         and resolver.capture(str(Path(control) / "runner.exit_code.txt"))[0] == b"0\n"
         and resolver.capture(str(Path(control) / "runner.stderr.log"))[0] == b""
         and cold_verification == formal_verification,
         "cold receipt/current byte closure")
    need(pinset.get("source_pins") == {
            "cold_replay_helper":
                "6f5dddc45b101560995e5f24b7719672e3aab5e3c340605c2cae88b9b03cb0d9",
            "independent_verifier": SOURCE_PINS["independent_verifier"],
            "producer": SOURCE_PINS["producer"],
            "python": SOURCE_PINS["python"],
            "transaction_runner": SOURCE_PINS["transaction_runner"]}
         and spec.get("schema") == SPEC_SCHEMA
         and spec.get("environment") == {"PATH": "/usr/bin:/bin", "LANG": "C",
             "LC_ALL": "C", "PYTHONHASHSEED": "30662828"}
         and spec.get("argv", [None, None, None])[:3]
             == [args.python, "-I", "-B"]
         and spec.get("source_sha256") == SOURCE_PINS["independent_verifier"]
         and spec.get("runner_source_sha256") == SOURCE_PINS["transaction_runner"]
         and spec.get("python_sha256") == SOURCE_PINS["python"]
         and attestation.get("schema") == RUN_SCHEMA
         and attestation.get("status") == RUN_STATUS
         and attestation.get("numeric_exit_code") == 0
         and attestation.get("signal") is None
         and attestation.get("timed_out") is False
         and attestation.get("stderr_empty") is True
         and attestation.get("input_pre_post_sha_stat_identical") is True
         and attestation.get("formal_credit") == 0
         and attestation.get("manifest_authorized") is False
         and resolver.capture(str(Path(run) / "exit_code.txt"))[0] == b"0\n"
         and resolver.capture(str(Path(run) / "signal.json"))[0] == b"null\n"
         and resolver.capture(str(Path(run) / "stderr.log"))[0] == b""
         and resolver.capture(str(Path(run) / "input_pre.json"))[0]
             == resolver.capture(str(Path(run) / "input_post.json"))[0]
         and resolver.plain(str(Path(run) / "input_post.json"))
             == attestation["input_attestations"]
         and resolver.plain(str(Path(run) / "output_validation.json"))
             == attestation["output_validation"],
         "cold pinset/spec/process closure")
    validate_historical_current(resolver, attestation["input_attestations"],
                                "cold")
    return receipt


def load_override(args: argparse.Namespace) \
        -> tuple[dict[str, Any], dict[str, Any], str | None, Path | None, bool]:
    path = Path(args.override_map_file).absolute()
    anchor = ROOT if path.is_relative_to(ROOT) else path.parent
    payload, record = capture_direct(path, anchor, 16 << 20)
    value = decode_document(payload, "override_map_sha256")
    need(record["sha256"] == args.expect_override_map_file_sha256
         and value["override_map_sha256"]
             == args.expect_override_map_object_sha256
         and value.get("schema") == OVERRIDE_SCHEMA
         and value.get("mode") == args.mode
         and value.get("authority_root") == str(ROOT)
         and value.get("formal_credit") == 0
         and value.get("C28") == "AUDIT_HOLD_UNAUTHORIZED"
         and value.get("CM2") == "NO-GO_FOR_CLAIM"
         and type(value.get("overrides")) is list,
         "override map file/object/schema/state closure")
    if args.mode == "formal":
        need(value["overrides"] == []
             and value.get("formal_snapshot_file_sha256") is None
             and value.get("formal_snapshot_object_sha256") is None
             and args.private_case_root is None
             and args.formal_snapshot_file is None
             and args.expect_formal_snapshot_file_sha256 is None
             and args.expect_formal_snapshot_object_sha256 is None,
             "formal exact empty override map")
        return value, record, None, None, False
    need(args.private_case_root is not None
         and args.formal_snapshot_file is not None
         and valid_sha(args.expect_formal_snapshot_file_sha256)
         and valid_sha(args.expect_formal_snapshot_object_sha256),
         "private formal snapshot arguments")
    snapshot_path = Path(args.formal_snapshot_file).absolute()
    snapshot_payload, snapshot_record = capture_direct(snapshot_path, ROOT,
                                                       512 << 20)
    snapshot = decode_document(snapshot_payload, "boundary_validation_sha256")
    need(snapshot_record["sha256"] == args.expect_formal_snapshot_file_sha256
         and snapshot["boundary_validation_sha256"]
             == args.expect_formal_snapshot_object_sha256
         and snapshot.get("schema") == OUTPUT_SCHEMA
         and snapshot.get("status") == FORMAL_STATUS
         and snapshot.get("mode") == "formal"
         and value.get("formal_snapshot_file_sha256")
             == snapshot_record["sha256"]
         and value.get("formal_snapshot_object_sha256")
             == snapshot["boundary_validation_sha256"],
         "private pinned formal snapshot")
    overrides = value["overrides"]
    need(len(overrides) == 1 and type(overrides[0]) is dict
         and set(overrides[0]) == {"barrier_after_open", "case_name",
                                  "logical_path", "physical_path"},
         "private exact single override shape")
    item = overrides[0]
    logical = logical_name(item["logical_path"])
    allowlist = snapshot.get("private_fixture_allowlisted_logical_paths")
    need(type(allowlist) is list and allowlist == sorted(set(allowlist))
         and logical in allowlist,
         "private logical path from formal snapshot allowlist")
    case_root = Path(args.private_case_root).absolute()
    physical = Path(item["physical_path"]).absolute()
    need(case_root.is_relative_to(AUDIT) and case_root.is_dir()
         and not case_root.is_symlink() and physical != case_root
         and physical.is_relative_to(case_root)
         and type(item["case_name"]) is str
         and re.fullmatch(r"[a-z0-9][a-z0-9-]{2,96}", item["case_name"])
             is not None
         and type(item["barrier_after_open"]) is bool,
         "private case confinement")
    no_symlink_chain(physical.parent, case_root)
    return value, record, logical, physical, item["barrier_after_open"]


def validate_environment(args: argparse.Namespace) -> None:
    python = Path(args.python).absolute()
    need(sys.flags.isolated == 1 and Path(sys.executable).absolute() == python,
         "exact isolated Python executable")
    payload, record = capture_direct(python, ROOT)
    del payload
    need(record["sha256"] == args.expect_python_sha256
         == SOURCE_PINS["python"]
         and os.environ.get("PATH") == "/usr/bin:/bin"
         and os.environ.get("LANG") == "C"
         and os.environ.get("LC_ALL") == "C"
         and os.environ.get("PYTHONHASHSEED") == args.expected_hash_seed,
         "exact Python/environment/hash seed")


def validate_no_import_exec() -> None:
    tree = ast.parse(SELF.read_text("utf-8"), filename=str(SELF))
    forbidden = "cm2_round306c28_source_g_post_c27r2_125561998198_pair_routing_v2_producer"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            need(all(forbidden not in alias.name for alias in node.names),
                 "producer not imported")
        if isinstance(node, ast.ImportFrom):
            need(forbidden not in (node.module or ""), "producer not imported")


def execute(args: argparse.Namespace) -> dict[str, Any]:
    global args_python_global
    validate_environment(args)
    validate_no_import_exec()
    dynamic = (args.expect_validator_sha256,
               args.expect_core_receipt_file_sha256,
               args.expect_core_receipt_object_sha256,
               args.expect_cold_receipt_file_sha256,
               args.expect_cold_receipt_object_sha256,
               args.expect_override_map_file_sha256,
               args.expect_override_map_object_sha256)
    need(all(valid_sha(value) for value in dynamic), "all dynamic SHA pins")
    _, self_record = capture_direct(SELF, ROOT)
    need(self_record["sha256"] == args.expect_validator_sha256,
         "validator self pin")
    override_value, override_record, override_logical, override_physical, barrier = \
        load_override(args)
    resolver = Resolver(override_logical, override_physical,
                        None if args.private_case_root is None
                        else Path(args.private_case_root).absolute(), barrier)
    args_python_global = args.python
    control = logical_name(args.core_control_relative)
    core_path = str(Path(control) / "core_receipt.json")
    pinset_path = str(Path(control) / "pinset.json")
    core = resolver.document(core_path, "core_receipt_sha256")
    pinset = resolver.document(pinset_path, "pinset_sha256")
    _, core_record = resolver.capture(core_path)
    need(core_record["sha256"] == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA
         and core.get("status") == CORE_STATUS
         and core.get("exact_math") == EXPECTED
         and core.get("formal_credit") == 0
         and core.get("manifest_authorized") is False
         and core.get("C28") == "UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
         and core.get("C29") == "UNAUTHORIZED"
         and core.get("CM2") == "NO-GO_FOR_CLAIM"
         and pinset.get("schema") == PINSET_SCHEMA
         and pinset.get("source_pins") == SOURCE_PINS
         and pinset.get("true_seeds") == ["30662801", "30662802"]
         and pinset.get("formal_credit") == 0
         and pinset.get("manifest_authorized") is False
         and resolver.capture(str(Path(control) / "PASS.lock"))[0] == CORE_PASS,
         "core receipt/pinset/PASS boundary")
    if args.mode == "formal":
        validate_service(args.expected_core_unit,
                         args.expected_core_invocation_id)
    else:
        snapshot_payload, _ = capture_direct(
            Path(args.formal_snapshot_file).absolute(), ROOT, 512 << 20)
        snapshot = decode_document(snapshot_payload,
                                   "boundary_validation_sha256")
        need(args.expected_core_unit == snapshot["core_unit_name"]
             and args.expected_core_invocation_id
                 == snapshot["core_invocation_id"],
             "private unit/invocation equal formal snapshot")
    for key, path in SOURCE_PATHS.items():
        _, record = resolver.capture(path)
        need(record["sha256"] == SOURCE_PINS[key], "current core source pin:" + key)
    _, python_current = resolver.capture(logical_name(args.python))
    need(python_current["sha256"] == SOURCE_PINS["python"],
         "current workspace Python pin")
    targets_raw = pinset.get("targets")
    need(type(targets_raw) is dict and set(targets_raw) == TARGET_KEYS,
         "exact fifteen core target names")
    targets = {key: logical_name(value) for key, value in targets_raw.items()}
    need(targets["control"] == control, "core control target identity")
    for target in targets.values():
        resolver.allowlist.add(target)
    predecessor_pins = core.get("predecessor_terminal_pins")
    need(type(predecessor_pins) is dict, "predecessor pins map")
    predecessor = logical_name(predecessor_pins["terminal_dir"])
    predecessor_logical, _ = resolver.directory(predecessor, PREDECESSOR_FILES)
    predecessor_receipt = resolver.document(
        str(Path(predecessor_logical) / "terminal_receipt.json"),
        "terminal_receipt_sha256")
    predecessor_replay = resolver.document(
        str(Path(predecessor_logical) / "terminal_replay.json"),
        "terminal_replay_sha256")
    predecessor_status = resolver.document(
        str(Path(predecessor_logical) / "chain_status.json"),
        "chain_status_sha256")
    _, root_record = resolver.capture(
        str(Path(predecessor_logical) / "root_manifest.sha256"))
    _, receipt_record = resolver.capture(
        str(Path(predecessor_logical) / "terminal_receipt.json"))
    _, replay_record = resolver.capture(
        str(Path(predecessor_logical) / "terminal_replay.json"))
    _, pass_record = resolver.capture(str(Path(predecessor_logical) / "PASS.lock"))
    parse_manifest(resolver, str(Path(predecessor_logical) /
                                 "payload_manifest.sha256"))
    parse_manifest(resolver, str(Path(predecessor_logical) /
                                 "root_manifest.sha256"))
    need(predecessor_pins == {
            "terminal_dir": str(ROOT / predecessor_logical),
            "terminal_pass_lock_sha256": pass_record["sha256"],
            "terminal_receipt_file_sha256": receipt_record["sha256"],
            "terminal_receipt_object_sha256":
                predecessor_receipt["terminal_receipt_sha256"],
            "terminal_replay_file_sha256": replay_record["sha256"],
            "terminal_replay_object_sha256":
                predecessor_replay["terminal_replay_sha256"],
            "terminal_root_sha256": root_record["sha256"]}
         and predecessor_receipt.get("authority_minted") is True
         and predecessor_receipt.get("manifest_authorized") is True
         and predecessor_receipt.get("C27R2")
             == "AUTHORIZED_TERMINAL_SOURCE_G_QUOTIENT_AUTHORITY"
         and predecessor_receipt.get("C28") == "UNAUTHORIZED_NOT_STARTED"
         and predecessor_receipt.get("C29") == "UNAUTHORIZED_NOT_STARTED"
         and predecessor_receipt.get("CM2") == "NO-GO_FOR_CLAIM"
         and predecessor_replay.get("authority_minted") is True
         and predecessor_status.get("authority_minted") is True,
         "six-file predecessor and exact pins/states")
    adapter = targets["adapter"]
    adapter_logical, _ = resolver.directory(adapter, ADAPTER_FILES)
    contract_path = str(Path(adapter_logical) / "authority_contract.json")
    receipt_path = str(Path(adapter_logical) / "terminal_receipt.json")
    contract = resolver.document(contract_path, "contract_sha256")
    adapter_receipt = resolver.document(receipt_path, "terminal_receipt_sha256")
    _, contract_record = resolver.capture(contract_path)
    parse_manifest(resolver, str(Path(adapter_logical) / "payload_manifest.sha256"))
    parse_manifest(resolver, str(Path(adapter_logical) / "root_manifest.sha256"))
    need(resolver.capture(str(Path(adapter_logical) / "PASS.lock"))[0]
             == ADAPTER_PASS
         and contract_record["sha256"] == core["adapter_contract_file_sha256"]
         and contract["contract_sha256"] == core["adapter_contract_object_sha256"]
         and adapter_receipt["terminal_receipt_sha256"]
             == core["adapter_receipt_object_sha256"]
         and exact_states(adapter_receipt, "UNAUTHORIZED_MATH_CORE_MAY_START"),
         "adapter byte/object/state closure")
    adapter_verification_path = str(Path(targets["adapter_verification"])
                                    / "verification.json")
    resolver.directory(targets["adapter_verification"], {"verification.json"})
    adapter_verification = resolver.document(adapter_verification_path,
                                             "verification_sha256")
    need(adapter_verification["verification_sha256"]
             == core["adapter_verification_object_sha256"]
         and adapter_verification.get("builder_imported_or_executed") is False
         and adapter_verification.get("legacy_alias_accepted") is False
         and exact_states(adapter_verification,
                          "UNAUTHORIZED_PENDING_MATH_CORE"),
         "adapter independent verification")
    seed1 = validate_candidate(resolver, targets["seed1_candidate"])
    seed2 = validate_candidate(resolver, targets["seed2_candidate"])
    for filename in sorted(CANDIDATE_FILES):
        first, first_record = resolver.capture(
            str(Path(targets["seed1_candidate"]) / filename))
        second, second_record = resolver.capture(
            str(Path(targets["seed2_candidate"]) / filename))
        agreement = core["dual_seed_candidate_file_agreement"][filename]
        need(first == second
             and first_record["sha256"] == agreement["seed1_sha256"]
             and second_record["sha256"] == agreement["seed2_sha256"],
             "dual true-seed candidate byte identity")
    need(seed1["result_sha256"] == seed2["result_sha256"]
         == core["candidate_result_object_sha256"],
         "dual result object pin")
    verification_payloads: list[bytes] = []
    verification_objects: list[str] = []
    for target in ("verifier1_output", "verifier2_output"):
        resolver.directory(targets[target], {"verification.json"})
        path = str(Path(targets[target]) / "verification.json")
        payload, _ = resolver.capture(path)
        value = decode_document(payload, "verification_sha256")
        need(value.get("schema") == VERIFICATION_SCHEMA
             and value.get("status") == VERIFICATION_STATUS
             and value.get("independence") == {
                 "all_candidate_rows_independently_reconstructed": True,
                 "input_pre_post_SHA_stat_identical": True,
                 "partition_rebuilt_from_terminal_pinned_ledgers": True,
                 "producer_executed": False, "producer_imported": False}
             and exact_states(value,
                 "UNAUTHORIZED_PENDING_ATTACKS_AND_RELEASE_TERMINAL"),
             "no-import verifier semantics")
        verification_payloads.append(payload)
        verification_objects.append(value["verification_sha256"])
    need(verification_objects == core["verifier_object_sha256"],
         "two verifier object pins")
    attacks = resolver.document(str(Path(control) / "coherent_attacks.json"),
                                "attack_receipt_sha256")
    need(attacks.get("schema") == ATTACK_SCHEMA
         and attacks.get("status") == ATTACK_STATUS
         and attacks.get("attack_census") == {"planned": 26, "executed": 26,
             "rejected_fail_closed": 26, "accepted": 0}
         and attacks["attack_receipt_sha256"]
             == core["attack_receipt_object_sha256"]
         and exact_states(attacks,
             "UNAUTHORIZED_PENDING_RELEASE_COLD_REPLAY_AND_TERMINAL"),
         "26 actual core attacks separately bound")
    run_objects: dict[str, str] = {}
    for name, values in STAGES.items():
        attestation = validate_run(resolver, control, pinset, core, name,
                                   values, targets)
        run_objects[name] = attestation["run_attestation_sha256"]
    need(run_objects == core["run_attestation_object_sha256"],
         "seven run object pins")
    cold = validate_cold(resolver, args, verification_payloads[0])
    if args.mode == "private-fixture":
        need(resolver.override_used, "private override consumed")
    current_digest = resolver.verify_current()
    resolver.allowlist.update(resolver.records)
    allowlist = sorted(resolver.allowlist)
    records = [resolver.records[name] for name in sorted(resolver.records)]
    output = Path(args.out_file).absolute()
    if args.mode == "formal":
        need(output.parent == AUDIT, "formal output direct audit child")
    else:
        need(output.parent == Path(args.private_case_root).absolute(),
             "private output inside case root")
    need(not output.exists() and not output.is_symlink(), "fresh output")
    body = {
        "schema": OUTPUT_SCHEMA,
        "status": FORMAL_STATUS if args.mode == "formal" else PRIVATE_STATUS,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="microseconds").replace("+00:00", "Z"),
        "mode": args.mode,
        "authority_root": str(ROOT),
        "core_unit_name": args.expected_core_unit,
        "core_invocation_id": args.expected_core_invocation_id,
        "core_receipt_file_sha256": core_record["sha256"],
        "core_receipt_object_sha256": core["core_receipt_sha256"],
        "cold_receipt_file_sha256": args.expect_cold_receipt_file_sha256,
        "cold_receipt_object_sha256": cold["cold_replay_receipt_sha256"],
        "override_map_file_sha256": override_record["sha256"],
        "override_map_object_sha256": override_value["override_map_sha256"],
        "validator_file_sha256": self_record["sha256"],
        "python_file_sha256": SOURCE_PINS["python"],
        "private_fixture_allowlisted_logical_paths": allowlist,
        "captured_authority_records": records,
        "captured_authority_record_count": len(records),
        "captured_authority_identity_sha256": current_digest,
        "exact_core_stage_count": 7,
        "exact_core_attack_census": {"planned": 26, "executed": 26,
            "rejected_fail_closed": 26, "accepted": 0},
        "core_attacks_bound_separately_not_counted_as_release_fixtures": True,
        "producer_imported": False,
        "producer_executed": False,
        "authority_pre_post_SHA_size_nine_stat_identical": True,
        "formal_credit": 0,
        "manifest_authorized": False,
        "C28": "AUDIT_HOLD_UNAUTHORIZED",
        "C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = {**body, "boundary_validation_sha256": digest(body)}
    descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_NOFOLLOW", 0), 0o400)
    try:
        os.write(descriptor, canonical(result) + b"\n")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return result


def self_test() -> dict[str, Any]:
    positive = duplicate = escape = symlink = hardlink = gzip_bad = False
    body = {"schema": "fixture", "ordinal": 0}
    row = {**body, "row_sha256": digest(body)}
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as stream:
        stream.write(canonical(row) + b"\n")
    rows, sequence = gzip_rows(buffer.getvalue())
    positive = rows == [row] and valid_sha(sequence)
    try:
        strict(b'{"x":1,"x":2}')
    except Rejected:
        duplicate = True
    try:
        logical_name("../escape")
    except Rejected:
        escape = True
    try:
        gzip_rows(buffer.getvalue()[:-4])
    except Rejected:
        gzip_bad = True
    import tempfile
    with tempfile.TemporaryDirectory(dir=AUDIT) as raw:
        root = Path(raw)
        target = root / "target"
        target.write_bytes(b"x")
        link = root / "link"
        link.symlink_to(target)
        try:
            capture_direct(link, root)
        except (Rejected, OSError):
            symlink = True
        hard = root / "hard"
        os.link(target, hard)
        try:
            capture_direct(target, root)
        except Rejected:
            hardlink = True
    need(positive and duplicate and escape and symlink and hardlink and gzip_bad,
         "positive and six-category tiny fixtures")
    return {"status": "PASS_C28_RELEASE_REPAIR_BOUNDARY_VALIDATOR_V2_"
            "POSITIVE_AND_SIX_NEGATIVE_TINY_FIXTURES",
            "formal_credit": 0, "C28": "AUDIT_HOLD_UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--mode", choices=("formal", "private-fixture"))
    for name in (
        "core-control-relative", "cold-control-relative",
        "cold-output-relative", "cold-run-relative", "override-map-file",
        "expected-core-unit", "expected-core-invocation-id",
        "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256",
        "expect-cold-receipt-file-sha256",
        "expect-cold-receipt-object-sha256", "python",
        "expect-python-sha256", "expect-validator-sha256",
        "expect-override-map-file-sha256",
        "expect-override-map-object-sha256", "expected-hash-seed", "out-file",
        "private-case-root", "formal-snapshot-file",
        "expect-formal-snapshot-file-sha256",
        "expect-formal-snapshot-object-sha256",
    ):
        parser.add_argument("--" + name)
    args = parser.parse_args()
    required = (
        "mode", "core_control_relative", "cold_control_relative",
        "cold_output_relative", "cold_run_relative", "override_map_file",
        "expected_core_unit", "expected_core_invocation_id",
        "expect_core_receipt_file_sha256",
        "expect_core_receipt_object_sha256",
        "expect_cold_receipt_file_sha256",
        "expect_cold_receipt_object_sha256", "python",
        "expect_python_sha256", "expect_validator_sha256",
        "expect_override_map_file_sha256",
        "expect_override_map_object_sha256", "expected_hash_seed", "out_file",
    )
    try:
        if args.self_test:
            need(all(getattr(args, name) is None for name in required)
                 and args.private_case_root is None
                 and args.formal_snapshot_file is None,
                 "self-test has no boundary arguments")
            result = self_test()
        else:
            need(all(getattr(args, name) is not None for name in required),
                 "all boundary arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical({"CM2": "NO-GO_FOR_CLAIM",
            "formal_credit": 0, "status": result["status"]}) + b"\n")
        return 0
    except (Rejected, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError, json.JSONDecodeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
