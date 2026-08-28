#!/usr/bin/env python3
"""Independent conditional outer verifier for the C27R2 release package.

This source does not import any release builder.  It verifies both manifests,
all current member bytes, the service/core/cold/attack boundaries, and all
three compressed quotient ledgers.  Its PASS is explicitly conditional and
zero credit until a separate terminal byte replay succeeds.
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
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
AUDIT = ROOT / ".cm2-runtime/audit"
UNIT = "cm2-c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523.service"
INVOCATION_ID = "aa82e1c6611f4910ae80b94307fb9ca9"
STEM = "c27r2-source-g-authority-v2-v6-formal-r2-20260808T180523"
CONTROL = AUDIT / (STEM + "-control")
CANDIDATE = AUDIT / (STEM + "-candidate")
VERIFICATION = AUDIT / (STEM + "-verifier-output/verification.json")
ATTACKS = AUDIT / (STEM + "-attack-work/coherent_attacks.json")
LEDGERS = {
    "old_C15_component_to_post_component": (
        "old_c15_component_to_post_component.jsonl.gz", 57_876,
        "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
        "old-c15-component-to-post-component-row.v1", "old_C15_component_id"),
    "member_to_post_component": (
        "member_to_post_component.jsonl.gz", 502_204,
        "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
        "member-to-post-component-row.v1", "member_ordinal"),
    "post_component_census": (
        "post_component_census.jsonl.gz", 43_684,
        "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
        "post-component-census-row.v1", "post_C27R2_component_id"),
}
EXPECTED_MATH = {
    "frozen_C15_members": 502_204, "frozen_C15_components": 57_876,
    "proof_derived_component_edges": 14_860,
    "successful_DSU_merges": 14_192, "cycle_edges": 668,
    "post_C27R2_components": 43_684,
    "total_unordered_member_pairs": 126_104_177_706,
    "within_post_component_member_pairs": 542_179_508,
    "cross_post_component_member_pairs": 125_561_998_198,
}
MANIFEST_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-manifest-receipt.v1"
)
EVIDENCE_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-evidence-bundle.v1"
)
COLD_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-cold-replay-receipt.v1"
)
RELEASE_ATTACK_SCHEMA = (
    "cm2.round306c27r2.source-g-authority-v2.release-only-attack-harness.v1"
)


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
            need(type(key) is str and key not in result, "unique JSON key")
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
    descriptor = os.open(absolute, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                         | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        chunks: list[bytes] = []
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            chunks.append(block)
            state.update(block)
        after = os.fstat(descriptor)
        need(fingerprint(before) == fingerprint(after)
             and fingerprint(os.stat(absolute, follow_symlinks=False))
                 == fingerprint(before), "stable path SHA/stat:" + str(path))
        return b"".join(chunks), state.hexdigest(), fingerprint(before)
    finally:
        os.close(descriptor)


def file_sha(path: Path) -> str:
    return capture(path)[1]


def document(path: Path, closure: str) -> dict[str, Any]:
    payload, _, _ = capture(path)
    need(payload.endswith(b"\n"), "JSON newline:" + str(path))
    value = strict_load(payload[:-1])
    need(type(value) is dict and canonical(value) == payload[:-1],
         "canonical JSON:" + str(path))
    body = dict(value)
    claim = body.pop(closure, None)
    need(valid_sha(claim) and claim == digest(body),
         "object closure:" + str(path))
    return value


def manifest(path: Path) -> dict[str, str]:
    payload, _, _ = capture(path)
    need(payload.endswith(b"\n"), "manifest newline")
    result: dict[str, str] = {}
    for line in payload.decode("ascii").splitlines():
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and valid_sha(pieces[0])
             and pieces[1] != "" and pieces[1] not in result,
             "manifest row syntax/unique")
        relative = Path(pieces[1])
        need(not relative.is_absolute()
             and all(part not in {"", ".", ".."} for part in relative.parts)
             and str(relative) == pieces[1], "canonical manifest path")
        result[pieces[1]] = pieces[0]
    need(list(result) == sorted(result), "manifest sorted paths")
    return result


def verify_manifest(path: Path) -> dict[str, str]:
    rows = manifest(path)
    for relative, expected in rows.items():
        need(file_sha(ROOT / relative) == expected,
             "manifest current member:" + relative)
    return rows


def service_success() -> None:
    completed = subprocess.run(
        ["/usr/bin/systemctl", "--user", "show", UNIT,
         "-p", "ActiveState", "-p", "SubState", "-p", "Result",
         "-p", "ExecMainCode", "-p", "ExecMainStatus", "-p", "InvocationID"],
        cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
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
         and fields.get("InvocationID") == INVOCATION_ID,
         "unique formal core clean service")


def ledger(path: Path, row_schema: str, ordering: str) -> tuple[int, str]:
    header, _, _ = capture(path)
    need(len(header) >= 10 and header[:2] == b"\x1f\x8b"
         and header[4:8] == b"\x00\x00\x00\x00",
         "deterministic gzip header:" + path.name)
    count = 0
    previous: Any = None
    sequence = hashlib.sha256()
    try:
        with gzip.open(path, "rb") as stream:
            for ordinal, line in enumerate(stream):
                need(line.endswith(b"\n"), "ledger row newline")
                row = strict_load(line[:-1])
                need(type(row) is dict and canonical(row) == line[:-1]
                     and row.get("schema") == row_schema
                     and row.get("ordinal") == ordinal
                     and row.get("formal_credit") == 0,
                     "canonical ledger row/schema/ordinal")
                body = dict(row)
                closure = body.pop("row_sha256", None)
                need(valid_sha(closure) and closure == digest(body),
                     "ledger row closure")
                key = row.get(ordering)
                if ordering == "member_ordinal":
                    need(key == ordinal, "member ordinal order")
                else:
                    need(type(key) is str
                         and (previous is None or previous < key),
                         "strict lexical ledger order")
                previous = key
                sequence.update(closure.encode("ascii") + b"\n")
                count += 1
    except (OSError, EOFError, gzip.BadGzipFile) as error:
        raise Blocked("gzip integrity:" + path.name) from error
    return count, sequence.hexdigest()


def execute(args: argparse.Namespace) -> dict[str, Any]:
    pins = (args.expect_outer_sha256, args.expect_manifest_receipt_file_sha256,
            args.expect_manifest_receipt_object_sha256,
            args.expect_payload_manifest_sha256,
            args.expect_root_manifest_sha256)
    need(all(valid_sha(value) for value in pins)
         and file_sha(SELF) == args.expect_outer_sha256,
         "outer/dynamic SHA pins")
    service_success()
    directory = Path(args.manifest_dir).absolute()
    need(directory.is_dir() and not directory.is_symlink()
         and {entry.name for entry in directory.iterdir()} == {
             "manifest_receipt.json", "payload_manifest.sha256",
             "root_manifest.sha256"}, "exact manifest directory")
    receipt_path = directory / "manifest_receipt.json"
    payload_path = directory / "payload_manifest.sha256"
    root_path = directory / "root_manifest.sha256"
    receipt = document(receipt_path, "manifest_receipt_sha256")
    need(file_sha(receipt_path) == args.expect_manifest_receipt_file_sha256
         and receipt["manifest_receipt_sha256"]
             == args.expect_manifest_receipt_object_sha256
         and receipt.get("schema") == MANIFEST_SCHEMA
         and receipt.get("formal_credit") == 0
         and receipt.get("manifest_authorized") is False
         and file_sha(payload_path) == args.expect_payload_manifest_sha256
             == receipt["payload_manifest_file_sha256"]
         and file_sha(root_path) == args.expect_root_manifest_sha256
             == receipt["root_manifest_file_sha256"],
         "manifest receipt and dynamic pins")
    payload = verify_manifest(payload_path)
    root = verify_manifest(root_path)
    need(len(payload) == receipt["payload_member_count"]
         and len(root) == receipt["root_member_count"]
         and str(payload_path.relative_to(ROOT)) in root,
         "manifest counts/root binds payload")
    evidence_paths = [path for path in payload if path.endswith("evidence_bundle.json")]
    cold_paths = [path for path in payload if path.endswith("cold_replay_receipt.json")]
    release_paths = [path for path in payload
                     if path.endswith("release_attacks.json")]
    need(len(evidence_paths) == len(cold_paths) == len(release_paths) == 1,
         "unique evidence/cold/release attack payload members")
    evidence = document(ROOT / evidence_paths[0], "evidence_bundle_sha256")
    cold = document(ROOT / cold_paths[0], "cold_replay_receipt_sha256")
    release = document(ROOT / release_paths[0],
                       "release_attack_harness_sha256")
    need(evidence.get("schema") == EVIDENCE_SCHEMA
         and evidence.get("formal_credit") == 0
         and cold.get("schema") == COLD_SCHEMA
         and cold.get("formal_verification_byte_identical") is True
         and cold.get("all_core_inputs_pre_post_sha_stat_identical") is True
         and release.get("schema") == RELEASE_ATTACK_SCHEMA
         and release.get("attack_count") == 20
         and release.get("rejected") == 20
         and release.get("accepted") == 0
         and release.get("formal_credit") == 0,
         "independent evidence/cold/20-attacks semantics")
    result = document(CANDIDATE / "result.json", "result_sha256")
    verification = document(VERIFICATION, "verification_sha256")
    attacks = document(ATTACKS, "attack_harness_sha256")
    need(result.get("exact_census") == EXPECTED_MATH
         and verification.get("candidate_result_object_sha256")
             == result["result_sha256"]
         and verification.get("producer_imported_or_executed") is False
         and attacks.get("attack_count") == 21
         and attacks.get("rejected") == 21
         and attacks.get("accepted") == 0,
         "independent core math/verifier/attacks projection")
    descriptors = result.get("ledgers")
    need(type(descriptors) is dict and set(descriptors) == set(LEDGERS),
         "exact ledger descriptor inventory")
    ledger_projection: dict[str, Any] = {}
    for name, (filename, expected_count, schema, ordering) in LEDGERS.items():
        count, sequence = ledger(CANDIDATE / filename, schema, ordering)
        descriptor = descriptors[name]
        need(count == expected_count == descriptor["row_count"]
             and sequence == descriptor["row_sequence_sha256"]
             and file_sha(CANDIDATE / filename) == descriptor["sha256"],
             "full ledger count/sequence/file closure:" + name)
        ledger_projection[name] = {"row_count": count,
                                   "row_sequence_sha256": sequence,
                                   "file_sha256": descriptor["sha256"]}
    body = {
        "schema": "cm2.round306c27r2.source-g-authority-v2.release-outer-verification.v1",
        "status": "PASS_INDEPENDENT_RELEASE_OUTER_FULL_LEDGER_MANIFEST_COLD_AND_ATTACK_CHECK__CONDITIONAL_C27R2_ZERO_CREDIT",
        "manifest_receipt_file_sha256": args.expect_manifest_receipt_file_sha256,
        "manifest_receipt_object_sha256":
            args.expect_manifest_receipt_object_sha256,
        "payload_manifest_sha256": args.expect_payload_manifest_sha256,
        "root_manifest_sha256": args.expect_root_manifest_sha256,
        "ledger_projection": ledger_projection,
        "exact_census": EXPECTED_MATH,
        "cold_replay_byte_identical": True,
        "core_attacks_rejected": 21, "release_attacks_rejected": 20,
        "outer_is_conditional_until_independent_terminal_byte_replay": True,
        "formal_credit": 0, "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_TERMINAL_BYTE_REPLAY",
        "C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**body, "outer_verification_sha256": digest(body)}


def self_test() -> dict[str, Any]:
    body = {"schema": "fixture", "formal_credit": 0}
    need(digest(body) == hashlib.sha256(canonical(body)).hexdigest(),
         "outer closure fixture")
    return {"status": "PASS_OUTER_CANONICAL_CLOSURE_FIXTURE"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--manifest-dir")
    parser.add_argument("--expect-outer-sha256")
    parser.add_argument("--expect-manifest-receipt-file-sha256")
    parser.add_argument("--expect-manifest-receipt-object-sha256")
    parser.add_argument("--expect-payload-manifest-sha256")
    parser.add_argument("--expect-root-manifest-sha256")
    args = parser.parse_args()
    fields = ("manifest_dir", "expect_outer_sha256",
              "expect_manifest_receipt_file_sha256",
              "expect_manifest_receipt_object_sha256",
              "expect_payload_manifest_sha256", "expect_root_manifest_sha256")
    try:
        if args.self_test:
            need(all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all run arguments")
            result = execute(args)
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
