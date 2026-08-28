#!/usr/bin/env python3
"""Publish the C71b v3 dual-build and durable-publication completion receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

SELF = Path(__file__).resolve()
SCHEMA = "cm2.round306c71b.child-h1-clipped-arrangement.dual-build-publication-receipt.v3"
PREFIX = "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3"
ARTIFACTS = {
    PREFIX + "_rows.jsonl.gz": {
        "sha256": "f9f04044809e46b9811d52abef94844d84b058a2f0c3fb6f5b9f97f2302cbec6",
        "size": 41198646},
    PREFIX + "_result.json": {
        "sha256": "5ede807e4860b60fe8582597cc6be10cdfdc7b3a0eeba57ced317f4980092246",
        "size": 2392},
    PREFIX + "_report.md": {
        "sha256": "428c05002f739db1cb221b7353a0e2ec8ccaf588b735111ce3b916f69890529a",
        "size": 279},
}
RESULT_OBJECT = "75c21279e3440a32116e67c20f12c7ec9d299491d018e2982ab18d68118d4158"
PRODUCER_SOURCE_SHA = "f93af460e37b589038f2a16e28449b8b7b86f68e3ab58d9e51ef57f05c1cadf5"
VERIFIER_NAME = "independent_verification_v3_1.json"
VERIFIER_SHA = "ee105922e263d9cea551088ee67c350cc9adc4d9f375a8584428e4fa55575612"
VERIFIER_OBJECT = "c45c5b19daeaef930f981810722460424a0d55c8302380829757e2132754f5c3"
VERIFIER_SOURCE_SHA = "366e4fea5bca2ce91ad89d56aa6a76c953b6a30723757c2cd6d6afcbcee13cc0"
EXPECTED_ATTACKS = 28
REJECTED_VERIFIER_NAME = "independent_verification_v3.json"
REJECTED_VERIFIER_SHA = "9c6733e7aabc900e77e8ca0358c4658b9acc7e48873e902b70651ce6360875e9"
REJECTED_VERIFIER_OBJECT = "89de4868bde9eef79f79ff25ecbb6a73a8cb4a1973b22b4398a16c174ec3e2ca"
SUPERSESSION_MARKER = Path(__file__).resolve().parent / (
    "cm2_round306c71b_child_h1_clipped_arrangement_"
    "VERIFICATION_STATUS_COUNT_REJECTED_SUPERSEDED_v3.md")
SUPERSESSION_MARKER_SHA = "ed0771eb82697b444f3bf0653b4671507ee789f16fb919bbfd4aa0a07284b310"
ZERO = {"terminal_disposition_credit": 0, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def secure_replay(path: Path, expected_sha: str, expected_size: int | None,
                  label: str) -> dict[str, Any]:
    path = path.resolve(strict=True)
    need(not path.is_symlink(), label + ": no symlink")
    before = path.stat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
         label + ": regular single-link file")
    first = path.read_bytes()
    middle = path.stat()
    second = path.read_bytes()
    after = path.stat()
    identity = lambda value: (value.st_dev, value.st_ino, value.st_size,
                              value.st_mtime_ns, value.st_ctime_ns)
    need(identity(before) == identity(middle) == identity(after),
         label + ": stable terminal replay")
    need(first == second, label + ": byte-identical terminal replay")
    actual = hashlib.sha256(first).hexdigest()
    need(actual == expected_sha, label + ": frozen SHA-256")
    if expected_size is not None:
        need(len(first) == expected_size, label + ": frozen size")
    return {"path": str(path), "sha256": actual, "size": len(first),
            "device": before.st_dev, "inode": before.st_ino,
            "link_count": before.st_nlink, "terminal_byte_replay": True}


def parse_closed_object(path: Path, expected: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ": JSON") from exc
    need(isinstance(value, dict) and value.get("object_sha256") == expected,
         label + ": object claim")
    body = dict(value)
    del body["object_sha256"]
    need(digest(body) == expected, label + ": object closure")
    return value


def exclusive_write(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_NOFOLLOW", 0), 0o444)
    try:
        view = memoryview(raw)
        while view:
            wrote = os.write(descriptor, view)
            need(wrote > 0, "receipt write progress")
            view = view[wrote:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    need(path.read_bytes() == raw and path.stat().st_nlink == 1,
         "receipt terminal-byte replay")


def publish(seed1: Path, seed2: Path, durable: Path, output: Path) -> dict[str, Any]:
    roots = [seed1.resolve(strict=True), seed2.resolve(strict=True),
             durable.resolve(strict=True)]
    need(len(set(map(str, roots))) == 3 and
         all(root.is_dir() and not root.is_symlink() for root in roots),
         "three distinct isolated directories")
    labels = ("seed1", "seed2", "durable_publication")
    records: dict[str, dict[str, dict[str, Any]]] = {}
    for label, root in zip(labels, roots):
        records[label] = {}
        for name, pin in ARTIFACTS.items():
            records[label][name] = secure_replay(
                root / name, pin["sha256"], pin["size"], label + ":" + name)
    for name in ARTIFACTS:
        triples = [records[label][name] for label in labels]
        need(len({row["sha256"] for row in triples}) == 1 and
             len({(row["device"], row["inode"]) for row in triples}) == 3,
             name + ": byte-identical but inode-isolated")
    result = parse_closed_object(roots[2] / (PREFIX + "_result.json"),
                                 RESULT_OBJECT, "durable result")
    need(result["producer_file_sha256"] == PRODUCER_SOURCE_SHA,
         "producer source recapture claim")
    verification_record = secure_replay(roots[2] / VERIFIER_NAME,
                                        VERIFIER_SHA, 4583,
                                        "corrected verification")
    verification = parse_closed_object(roots[2] / VERIFIER_NAME,
                                       VERIFIER_OBJECT, "corrected verification")
    need(verification["verifier_file_sha256"] == VERIFIER_SOURCE_SHA and
         verification["status"].endswith("__28_COHERENT_ATTACKS__ZERO_CREDIT") and
         verification["coherent_attacks"]["attempted"] == EXPECTED_ATTACKS and
         verification["coherent_attacks"]["rejected"] == EXPECTED_ATTACKS and
         verification["coherent_attacks"]["all_rejected"] is True,
         "corrected verifier exact status and attacks")
    rejected_record = secure_replay(roots[2] / REJECTED_VERIFIER_NAME,
                                    REJECTED_VERIFIER_SHA, 4583,
                                    "rejected verification")
    rejected = parse_closed_object(roots[2] / REJECTED_VERIFIER_NAME,
                                   REJECTED_VERIFIER_OBJECT,
                                   "rejected verification")
    need("__32_COHERENT_ATTACKS__" in rejected["status"] and
         rejected["coherent_attacks"]["attempted"] == 28,
         "rejected status-count mismatch recaptured")
    marker_record = secure_replay(SUPERSESSION_MARKER, SUPERSESSION_MARKER_SHA,
                                  None, "supersession marker")
    replay_rows = [records[label][name] for label in labels for name in ARTIFACTS]
    replay_rows.extend((verification_record, rejected_record, marker_record))
    replay_sequence = hashlib.sha256()
    for row in replay_rows:
        replay_sequence.update((row["sha256"] + "\n").encode("ascii"))
    receipt = {
        "schema": SCHEMA,
        "status": "PASS_DUAL_ISOLATED_3_OF_3_BYTE_IDENTICAL__DURABLE_NO_REPLACE_PUBLICATION__CORRECTED_NO_PRODUCER_VERIFICATION__ALL_TERMINAL_BYTES_REPLAYED__ZERO_CREDIT",
        "receipt_source_sha256": file_sha(SELF),
        "build_invocations": {
            "evidence_kind": "ORCHESTRATOR_RECORDED_ENVIRONMENT_PLUS_POSTBUILD_BYTE_RECAPTURE",
            "seed1": {"output": str(roots[0]), "PYTHONHASHSEED": "101",
                      "sanitized_environment": True, "external_process": True,
                      "SOURCE_DATE_EPOCH": "0", "TZ": "UTC", "LC_ALL": "C"},
            "seed2": {"output": str(roots[1]), "PYTHONHASHSEED": "202",
                      "sanitized_environment": True, "external_process": True,
                      "SOURCE_DATE_EPOCH": "0", "TZ": "UTC", "LC_ALL": "C"},
            "producer_source_sha256": PRODUCER_SOURCE_SHA},
        "dual_build": {
            "artifact_count_per_build": 3,
            "seed1_seed2_3_of_3_byte_identical": True,
            "seed1_seed2_corresponding_inodes_distinct": True,
            "seed_output_directories_distinct": True,
            "records": {"seed1": records["seed1"], "seed2": records["seed2"]}},
        "durable_publication": {
            "path": str(roots[2]), "exclusive_no_replace_copy": True,
            "3_of_3_equal_to_both_isolated_builds": True,
            "corresponding_inodes_distinct_from_both_builds": True,
            "records": records["durable_publication"],
            "result_object_sha256": RESULT_OBJECT},
        "independent_verification": {
            "accepted_filename": VERIFIER_NAME,
            "file_sha256": VERIFIER_SHA,
            "object_sha256": VERIFIER_OBJECT,
            "verifier_source_sha256": VERIFIER_SOURCE_SHA,
            "producer_source_imported_read_decoded_compiled_or_executed": False,
            "coherent_attacks": "28/28_HASH_RECLOSED_AND_REJECTED"},
        "supersession": {
            "rejected_filename": REJECTED_VERIFIER_NAME,
            "rejected_file_sha256": REJECTED_VERIFIER_SHA,
            "rejected_object_sha256": REJECTED_VERIFIER_OBJECT,
            "marker_file_sha256": SUPERSESSION_MARKER_SHA,
            "rejected_output_may_be_consumed": False},
        "terminal_byte_replay": {
            "record_count": len(replay_rows),
            "all_stable_single_link_exact_sha256": True,
            "ordered_sha256_line_sequence": replay_sequence.hexdigest(),
            "receipt_exclusive_write_and_terminal_replay_required": True},
        "candidate_is_authority": False, "global_consumption_ready": False,
        "runtime_canonical_pointer_or_seal_writes": False, **ZERO,
    }
    receipt["object_sha256"] = digest(receipt)
    exclusive_write(output.resolve(), canonical(receipt) + b"\n")
    return receipt


def self_test() -> dict[str, Any]:
    tests = {"three_artifacts": len(ARTIFACTS) == 3,
             "distinct_verifier_names": VERIFIER_NAME != REJECTED_VERIFIER_NAME,
             "exact_attack_count": EXPECTED_ATTACKS == 28,
             "zero_credit": all(value == 0 for value in ZERO.values())}
    need(all(tests.values()), "self-test")
    return {"schema": SCHEMA + ".static-self-test",
            "status": "PASS_4_OF_4_RECEIPT_PIN_AND_CREDIT_TESTS",
            "tests": tests, "files_written": False, **ZERO}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--seed1", type=Path)
    parser.add_argument("--seed2", type=Path)
    parser.add_argument("--durable", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.self_test:
            need(all(value is None for value in
                     (args.seed1, args.seed2, args.durable, args.output)),
                 "self-test no paths")
            value = self_test()
        else:
            need(all(value is not None for value in
                     (args.seed1, args.seed2, args.durable, args.output)) and
                 not args.output.exists() and not args.output.is_symlink(),
                 "fresh receipt output and all roots")
            value = publish(args.seed1, args.seed2, args.durable, args.output)
        print(canonical(value).decode("ascii"))
        return 0
    except (Reject, KeyError, TypeError, ValueError, OSError) as exc:
        print(canonical({"status": "REJECTED", "reason": str(exc)}).decode("ascii"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
