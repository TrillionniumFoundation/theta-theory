#!/usr/bin/env python3
"""Independently verify the conditional C28-v2 release package.

This no-import verifier rechecks the live formal core boundary, both release
manifests and every member, the cold/evidence/32-attack chain, and every row
of both C28 ledgers.  It writes only a conditional zero-credit outer receipt;
authority remains impossible until the separate terminal byte replay passes.
"""

from __future__ import annotations

import argparse
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
AUDIT = ROOT / ".cm2-runtime/audit"
PREFIX = (
    "cm2.round306c28.source-g-post-c27r2-125561998198-pair-routing.v2."
)
CORE_SCHEMA = PREFIX + "gated-dual-seed-core-receipt.v1"
CORE_STATUS = (
    "PASS_C27R2_TERMINAL_ADAPTER_DUAL_TRUE_SEED_THREE_FILE_CANDIDATES_"
    "TWO_NO_IMPORT_VERIFIERS_AND_26_ATTACKS__ZERO_CREDIT_PENDING_RELEASE"
)
COLD_SCHEMA = PREFIX + "release-cold-replay-receipt.v1"
EVIDENCE_SCHEMA = PREFIX + "release-evidence-bundle.v1"
RELEASE_ATTACK_SCHEMA = PREFIX + "release-only-attack-harness.v1"
MANIFEST_SCHEMA = PREFIX + "release-manifest-receipt.v1"
MANIFEST_STATUS = (
    "PASS_C28_MANIFEST_FIRST_PAYLOAD_AND_C27R2_ROOT_CLOSURE__ZERO_"
    "CREDIT_PENDING_OUTER_SEAL_AND_TERMINAL_REPLAY"
)
RESULT_SCHEMA = PREFIX + "producer-result.v1"
RESULT_STATUS = (
    "PASS_POST_C27R2_PARTITION_502204_MEMBERS_43684_COMPONENTS_AND_"
    "32896_PAIR_SHARDS_REBUILT__125561998198_EXACT_NONEDGE_CANDIDATE_"
    "ZERO_CREDIT__C28_UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
)
VERIFICATION_SCHEMA = PREFIX + "independent-verification.v1"
VERIFICATION_STATUS = (
    "PASS_NO_IMPORT_C27R2_TERMINAL_PARTITION_AND_32896_PAIR_SHARDS_"
    "INDEPENDENTLY_REBUILT__ZERO_CREDIT_PENDING_ATTACKS_AND_RELEASE_CHAIN"
)
CORE_ATTACK_SCHEMA = PREFIX + "coherent-attack-harness.v1"
BLOCK_SCHEMA = PREFIX + "member-home-block-census-row.v1"
ROUTE_SCHEMA = PREFIX + "cross-component-pair-route-shard-row.v1"
OUTER_SCHEMA = PREFIX + "release-outer-verification.v1"
OUTER_STATUS = (
    "PASS_INDEPENDENT_C28_FULL_PAIR_LEDGER_MANIFEST_COLD_AND_32_RELEASE_"
    "ATTACK_CHECK__CONDITIONAL_ZERO_CREDIT"
)
EXPECTED = {
    "members": 502_204, "post_components": 43_684, "blocks": 256,
    "shards": 32_896, "total_pairs": 126_104_177_706,
    "within_pairs": 542_179_508, "cross_pairs": 125_561_998_198,
}
C27_ROOT = "1f65a624c889773e3104c4311788fc06be04d6ca92e033205074b8cc7f5b27fc"
ADAPTER_RECEIPT_OBJECT = (
    "1dc2c671b78bdbcf015f254867da4fdd71c3f1435d3e2a61a9e214ffd89de604"
)
CANDIDATE_FILES = {
    "member_home_block_census.jsonl.gz",
    "cross_component_pair_route_shard.jsonl.gz", "result.json",
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


def capture(path: Path) -> tuple[bytes, str, tuple[int, ...]]:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute,
         "canonical path:" + str(path))
    fd = os.open(absolute, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        chunks: list[bytes] = []
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            chunks.append(block)
            state.update(block)
        need(fingerprint(before) == fingerprint(os.fstat(fd))
             == fingerprint(os.stat(absolute, follow_symlinks=False)),
             "stable fd/path SHA/stat:" + str(path))
        return b"".join(chunks), state.hexdigest(), fingerprint(before)
    finally:
        os.close(fd)


def file_sha(path: Path) -> str:
    return capture(path)[1]


def document(path: Path, closure: str) -> dict[str, Any]:
    payload, _, _ = capture(path)
    need(payload.endswith(b"\n") and not payload.endswith(b"\n\n"),
         "JSON newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "object closure:" + str(path))
    return value


def parse_manifest(path: Path) -> dict[str, str]:
    payload, _, _ = capture(path)
    need(payload.endswith(b"\n") and payload != b"\n", "manifest nonempty")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and valid_sha(fields[0])
             and fields[1] not in result and fields[1] != "",
             "manifest row syntax/unique")
        relative = Path(fields[1])
        need(not relative.is_absolute()
             and all(part not in {"", ".", ".."} for part in relative.parts)
             and str(relative) == fields[1], "canonical manifest path")
        result[fields[1]] = fields[0]
    need(list(result) == sorted(result), "manifest path ordering")
    for relative, expected in result.items():
        need(file_sha(ROOT / relative) == expected,
             "manifest member current:" + relative)
    return result


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


def service_success(unit: str, invocation: str) -> None:
    need(type(unit) is str and unit.endswith(".service")
         and type(invocation) is str and len(invocation) == 32
         and all(character in "0123456789abcdef" for character in invocation),
         "core unit/invocation syntax")
    completed = subprocess.run([
        "/usr/bin/systemctl", "--user", "show", unit,
        "-p", "ActiveState", "-p", "SubState", "-p", "Result",
        "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID",
    ], cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
       stderr=subprocess.PIPE, check=False)
    need(completed.returncode == 0 and completed.stderr == b"",
         "query formal core service")
    fields = dict(line.split("=", 1) for line in
                  completed.stdout.decode("ascii").splitlines() if "=" in line)
    need(fields.get("ActiveState") == "active"
         and fields.get("SubState") == "exited"
         and fields.get("Result") == "success"
         and fields.get("ExecMainCode") in {"1", "exited"}
         and fields.get("ExecMainStatus") == "0"
         and fields.get("InvocationID") == invocation,
         "unique formal core clean success")


def pairs() -> Iterator[tuple[int, int]]:
    for left in range(EXPECTED["blocks"]):
        for right in range(left, EXPECTED["blocks"]):
            yield left, right


def ledger(path: Path, schema: str,
           block_counts: list[int] | None = None) \
        -> tuple[dict[str, Any], dict[str, int], list[int]]:
    header, sha256, file_stat = capture(path)
    need(len(header) >= 10 and header[:2] == b"\x1f\x8b"
         and header[4:8] == b"\x00\x00\x00\x00",
         "deterministic gzip header:" + path.name)
    sequence = hashlib.sha256()
    count = 0
    counts: list[int] = []
    totals = {"members": 0, "total": 0, "within": 0, "cross": 0}
    pair_order = pairs()
    try:
        with gzip.open(path, "rb") as stream:
            for ordinal, line in enumerate(stream):
                need(line.endswith(b"\n") and not line.endswith(b"\n\n"),
                     "ledger row newline")
                row = strict_load(line[:-1])
                need(type(row) is dict and canonical(row) == line[:-1]
                     and row.get("schema") == schema
                     and row.get("ordinal") == ordinal
                     and row.get("formal_credit") == 0
                     and row.get("C28")
                         == "UNAUTHORIZED_PENDING_RELEASE_TERMINAL"
                     and row.get("CM2") == "NO-GO_FOR_CLAIM",
                     "canonical ledger row/schema/ordinal")
                body = dict(row)
                closure = body.pop("row_sha256", None)
                need(valid_sha(closure) and closure == digest(body),
                     "ledger row closure")
                sequence.update(closure.encode("ascii") + b"\n")
                if schema == BLOCK_SCHEMA:
                    need(ordinal < EXPECTED["blocks"]
                         and row.get("home_block_ordinal") == ordinal
                         and row.get("home_block_hex") == f"{ordinal:02x}"
                         and row.get("home_block_definition")
                             == "FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID"
                         and type(row.get("member_count")) is int
                         and row["member_count"] > 0
                         and row.get("same_block_total_unordered_pairs")
                             == row["member_count"] * (row["member_count"] - 1) // 2
                         and row.get("same_block_within_post_component_pairs")
                             + row.get("same_block_cross_post_component_pairs")
                             == row["same_block_total_unordered_pairs"]
                         and row.get("partition_authority", {}).get(
                             "c27r2_terminal_receipt_object_sha256")
                             == ADAPTER_RECEIPT_OBJECT,
                         "block ledger independent semantics")
                    counts.append(row["member_count"])
                    totals["members"] += row["member_count"]
                else:
                    need(block_counts is not None, "route needs block census")
                    expected_pair = next(pair_order, None)
                    need(expected_pair is not None, "route bounded pair order")
                    left, right = expected_pair
                    expected_total = (block_counts[left]
                                      * (block_counts[left] - 1) // 2
                                      if left == right else
                                      block_counts[left] * block_counts[right])
                    classification = row.get("pair_classification", {})
                    proof = row.get("proof_binding", {})
                    cross = row.get("cross_post_component_member_pairs_routed")
                    within = row.get("within_post_component_member_pairs_excluded")
                    need(row.get("shard_ordinal") == ordinal
                         and row.get("canonical_home_block_pair")
                             == [f"{left:02x}", f"{right:02x}"]
                         and row.get("left_member_count") == block_counts[left]
                         and row.get("right_member_count") == block_counts[right]
                         and row.get("same_home_block") is (left == right)
                         and row.get("total_unordered_member_pairs") == expected_total
                         and type(within) is int and type(cross) is int
                         and within >= 0 and cross >= 0
                         and within + cross == expected_total
                         and classification == {
                             "EXACT_NONEDGE_BY_COMPLETE_ACTUAL_V2_EDGE_"
                             "COMPLEMENT_AFTER_C27R2_QUOTIENT": cross,
                             "KNOWN_LEGAL_CROSS_POST_COMPONENT": 0,
                             "NEW_LEGAL_CROSS_POST_COMPONENT": 0,
                             "UNRESOLVED": 0}
                         and proof.get("c27r2_terminal_receipt_object_sha256")
                             == ADAPTER_RECEIPT_OBJECT
                         and proof.get("within_pairs_removed_by_exact_post_"
                                      "component_block_convolution") is True
                         and proof.get("remaining_pairs_are_cross_post_component")
                             is True
                         and proof.get("actual_v2_edge_complement_complete_after_"
                                      "C27R2_quotient") is True,
                         "route ledger independent pair semantics")
                    totals["total"] += expected_total
                    totals["within"] += within
                    totals["cross"] += cross
                count += 1
    except (OSError, EOFError, gzip.BadGzipFile) as error:
        raise Blocked("gzip integrity:" + path.name) from error
    if schema == BLOCK_SCHEMA:
        need(count == EXPECTED["blocks"] and totals["members"] == EXPECTED["members"],
             "block ledger exact count/member total")
        ordering = ["home_block_ordinal"]
        unique_key = "home_block_hex"
    else:
        need(count == EXPECTED["shards"] and next(pair_order, None) is None
             and totals == {"members": 0, "total": EXPECTED["total_pairs"],
                             "within": EXPECTED["within_pairs"],
                             "cross": EXPECTED["cross_pairs"]},
             "route ledger exact exhaustion/global identity")
        ordering = ["canonical_home_block_pair"]
        unique_key = "canonical_home_block_pair"
    descriptor = {
        "filename": path.name, "sha256": sha256, "size": file_stat[4],
        "row_count": count, "row_schema": schema, "ordering": ordering,
        "unique_key": unique_key, "row_sequence_sha256": sequence.hexdigest(),
        "gzip_mtime": 0, "canonical_jsonl": True,
        "row_closure": "row_sha256=SHA256(canonical row without row_sha256)",
    }
    return descriptor, totals, counts


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (
        args.expect_outer_sha256, args.expect_manifest_receipt_file_sha256,
        args.expect_manifest_receipt_object_sha256,
        args.expect_payload_manifest_sha256, args.expect_root_manifest_sha256,
        args.expect_core_receipt_file_sha256,
        args.expect_core_receipt_object_sha256, args.expect_core_pass_sha256,
        args.expect_cold_receipt_file_sha256,
        args.expect_cold_receipt_object_sha256,
        args.expect_release_attack_file_sha256,
        args.expect_release_attack_object_sha256,
        args.expect_evidence_file_sha256, args.expect_evidence_object_sha256,
    )
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_outer_sha256,
         "outer verifier self/all dynamic pins")
    service_success(args.core_unit, args.expect_core_invocation_id)
    control = Path(args.core_control_dir).absolute()
    candidate = Path(args.candidate_dir).absolute()
    formal = Path(args.formal_verification_file).absolute()
    core_attacks_path = Path(args.core_attacks_file).absolute()
    cold_control = Path(args.cold_control_dir).absolute()
    release_dir = Path(args.release_attack_dir).absolute()
    evidence_dir = Path(args.evidence_dir).absolute()
    manifest_dir = Path(args.manifest_dir).absolute()
    output = Path(args.output_file).absolute()
    need(all(path.parent == AUDIT and path.is_dir() and not path.is_symlink()
             for path in (control, candidate, cold_control, release_dir,
                          evidence_dir, manifest_dir)), "direct audit inputs")
    need(output.parent == AUDIT and not output.exists()
         and not output.is_symlink(), "fresh outer output")
    need({entry.name for entry in candidate.iterdir()} == CANDIDATE_FILES,
         "candidate exact inventory")
    need({entry.name for entry in manifest_dir.iterdir()} == {
        "manifest_receipt.json", "payload_manifest.sha256",
        "root_manifest.sha256"}, "manifest exact inventory")
    manifest_receipt_path = manifest_dir / "manifest_receipt.json"
    payload_path = manifest_dir / "payload_manifest.sha256"
    root_path = manifest_dir / "root_manifest.sha256"
    manifest_receipt = document(manifest_receipt_path,
                                "manifest_receipt_sha256")
    payload = parse_manifest(payload_path)
    root = parse_manifest(root_path)
    need(file_sha(manifest_receipt_path)
             == args.expect_manifest_receipt_file_sha256
         and manifest_receipt["manifest_receipt_sha256"]
             == args.expect_manifest_receipt_object_sha256
         and manifest_receipt.get("schema") == MANIFEST_SCHEMA
         and manifest_receipt.get("status") == MANIFEST_STATUS
         and file_sha(payload_path) == args.expect_payload_manifest_sha256
             == manifest_receipt.get("payload_manifest_file_sha256")
         and file_sha(root_path) == args.expect_root_manifest_sha256
             == manifest_receipt.get("root_manifest_file_sha256")
         and len(payload) == manifest_receipt.get("payload_member_count")
         and len(root) == manifest_receipt.get("root_member_count")
         and manifest_receipt.get("C27R2_terminal_root_manifest_sha256")
             == C27_ROOT
         and manifest_receipt.get("formal_credit") == 0
         and manifest_receipt.get("manifest_authorized") is False,
         "manifest receipt/payload/root closure")
    core_path = control / "core_receipt.json"
    cold_path = cold_control / "cold_replay_receipt.json"
    release_path = release_dir / "release_attacks.json"
    evidence_path = evidence_dir / "evidence_bundle.json"
    core = document(core_path, "core_receipt_sha256")
    cold = document(cold_path, "cold_replay_receipt_sha256")
    release = document(release_path, "release_attack_receipt_sha256")
    evidence = document(evidence_path, "evidence_bundle_sha256")
    need(file_sha(core_path) == args.expect_core_receipt_file_sha256
         and core["core_receipt_sha256"]
             == args.expect_core_receipt_object_sha256
         and core.get("schema") == CORE_SCHEMA and core.get("status") == CORE_STATUS
         and core.get("exact_math") == EXPECTED
         and file_sha(control / "PASS.lock") == args.expect_core_pass_sha256
         and file_sha(cold_path) == args.expect_cold_receipt_file_sha256
         and cold["cold_replay_receipt_sha256"]
             == args.expect_cold_receipt_object_sha256
         and cold.get("schema") == COLD_SCHEMA
         and cold.get("cold_replay_byte_identical") is True
         and file_sha(release_path) == args.expect_release_attack_file_sha256
         and release["release_attack_receipt_sha256"]
             == args.expect_release_attack_object_sha256
         and release.get("schema") == RELEASE_ATTACK_SCHEMA
         and release.get("attack_census") == {
             "planned": 32, "executed": 32,
             "rejected_fail_closed": 32, "accepted": 0}
         and file_sha(evidence_path) == args.expect_evidence_file_sha256
         and evidence["evidence_bundle_sha256"]
             == args.expect_evidence_object_sha256
         and evidence.get("schema") == EVIDENCE_SCHEMA
         and all(item.get("formal_credit") == 0
                 and item.get("manifest_authorized") is False
                 for item in (core, cold, release, evidence)),
         "core/cold/release/evidence chain")
    result_path = candidate / "result.json"
    result = document(result_path, "result_sha256")
    verification = document(formal, "verification_sha256")
    core_attacks = document(core_attacks_path, "attack_receipt_sha256")
    need(result.get("schema") == RESULT_SCHEMA
         and result.get("status") == RESULT_STATUS
         and verification.get("schema") == VERIFICATION_SCHEMA
         and verification.get("status") == VERIFICATION_STATUS
         and verification.get("candidate_result_sha256")
             == result["result_sha256"]
         and verification.get("verified_census") == EXPECTED
         and verification.get("independence", {}).get("producer_imported")
             is False
         and verification.get("independence", {}).get("producer_executed")
             is False
         and core_attacks.get("schema") == CORE_ATTACK_SCHEMA
         and core_attacks.get("attack_census") == {
             "planned": 26, "executed": 26,
             "rejected_fail_closed": 26, "accepted": 0},
         "independent core math/verifier/26 attacks")
    block_descriptor, block_totals, block_counts = ledger(
        candidate / "member_home_block_census.jsonl.gz", BLOCK_SCHEMA)
    route_descriptor, route_totals, _ = ledger(
        candidate / "cross_component_pair_route_shard.jsonl.gz",
        ROUTE_SCHEMA, block_counts)
    descriptors = result.get("ledgers", {})
    need(descriptors.get("member_home_block_census") == block_descriptor
         and descriptors.get("cross_component_pair_route_shard")
             == route_descriptor
         and result.get("post_C27R2_partition_census") == {
             "members": EXPECTED["members"],
             "components": EXPECTED["post_components"],
             "total_unordered_member_pairs": EXPECTED["total_pairs"],
             "within_post_component_member_pairs": EXPECTED["within_pairs"],
             "cross_post_component_member_pairs": EXPECTED["cross_pairs"]}
         and result.get("pair_route_census", {}).get(
             "cross_post_component_pairs_routed") == EXPECTED["cross_pairs"]
         and result.get("pair_route_census", {}).get(
             "new_legal_cross_post_component_pairs") == 0
         and result.get("pair_route_census", {}).get("unresolved_pairs") == 0,
         "result descriptors/exact pair census")
    required_payload = {str(path.relative_to(ROOT)) for path in {
        *(candidate / name for name in CANDIDATE_FILES), formal,
        core_attacks_path, core_path, control / "PASS.lock", cold_path,
        cold_control / "PASS.lock", release_path, release_dir / "PASS.lock",
        evidence_path, evidence_dir / "authority_inventory.sha256",
    }}
    need(required_payload <= set(payload)
         and str(payload_path.relative_to(ROOT)) in root,
         "required payload/root coverage")
    if args.preflight_only:
        return {"status":
                "PASS_C28_INDEPENDENT_OUTER_AND_FRESH_OUTPUT_PREFLIGHT__NO_"
                "OUTPUT_CREATED_ZERO_CREDIT"}
    body = {
        "schema": OUTER_SCHEMA, "status": OUTER_STATUS,
        "manifest_receipt_file_sha256":
            args.expect_manifest_receipt_file_sha256,
        "manifest_receipt_object_sha256":
            args.expect_manifest_receipt_object_sha256,
        "payload_manifest_sha256": args.expect_payload_manifest_sha256,
        "root_manifest_sha256": args.expect_root_manifest_sha256,
        "core_receipt_object_sha256": args.expect_core_receipt_object_sha256,
        "cold_replay_object_sha256": args.expect_cold_receipt_object_sha256,
        "release_attack_object_sha256": args.expect_release_attack_object_sha256,
        "evidence_bundle_object_sha256": args.expect_evidence_object_sha256,
        "candidate_result_object_sha256": result["result_sha256"],
        "independent_verification_object_sha256":
            verification["verification_sha256"],
        "C27R2_terminal_root_manifest_sha256": C27_ROOT,
        "ledger_projection": {
            "member_home_block_census": block_descriptor,
            "cross_component_pair_route_shard": route_descriptor},
        "independent_ledger_aggregates": {
            "block": block_totals, "route": route_totals},
        "exact_census": EXPECTED,
        "all_256_blocks_and_32896_shards_independently_replayed": True,
        "cold_replay_byte_identical": True,
        "core_attacks_rejected": 26, "release_attacks_rejected": 32,
        "outer_is_conditional_until_independent_terminal_byte_replay": True,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "AUTHORIZED_PREDECESSOR_ONLY",
        "C28": "UNAUTHORIZED_PENDING_TERMINAL_BYTE_REPLAY",
        "C29": "UNAUTHORIZED", "Source_W": "UNCHANGED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    outer = {**body, "outer_verification_sha256": digest(body)}
    write_once(output, canonical(outer) + b"\n")
    return outer


def self_test() -> dict[str, Any]:
    need(sum(1 for _ in pairs()) == EXPECTED["shards"]
         and EXPECTED["total_pairs"]
             == EXPECTED["within_pairs"] + EXPECTED["cross_pairs"],
         "pair enumeration/math fixtures")
    return {"status": "PASS_C28_RELEASE_OUTER_VERIFIER_SELF_TEST",
            "formal_credit": 0, "C28": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--preflight-only", action="store_true")
    for name in (
        "core-unit", "expect-core-invocation-id", "core-control-dir",
        "candidate-dir", "formal-verification-file", "core-attacks-file",
        "cold-control-dir", "release-attack-dir", "evidence-dir",
        "manifest-dir", "output-file", "expect-outer-sha256",
        "expect-manifest-receipt-file-sha256",
        "expect-manifest-receipt-object-sha256",
        "expect-payload-manifest-sha256", "expect-root-manifest-sha256",
        "expect-core-receipt-file-sha256",
        "expect-core-receipt-object-sha256", "expect-core-pass-sha256",
        "expect-cold-receipt-file-sha256",
        "expect-cold-receipt-object-sha256",
        "expect-release-attack-file-sha256",
        "expect-release-attack-object-sha256",
        "expect-evidence-file-sha256", "expect-evidence-object-sha256",
    ):
        value.add_argument("--" + name)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = tuple(name for name in vars(args)
                   if name not in {"self_test", "preflight_only"})
    try:
        if args.self_test:
            need(not args.preflight_only
                 and all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
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
