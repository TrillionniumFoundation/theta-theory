#!/usr/bin/env python3
"""Publish the last, zero-credit C72b2 completion receipt."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
SCHEMA = "cm2.round306c72b2.boundary-arrangement-physical-glue.completion-outer-receipt.v2"
PREFIX = "cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2"
NAMES = (
    PREFIX + ".jsonl.gz",
    PREFIX + "_root_incidence.jsonl.gz",
    PREFIX + "_result.json",
    PREFIX + "_report.md",
    "ZERO_CREDIT_STAGED_BOUNDARY_PHYSICAL_GLUE_ORACLE_ONLY.lock",
)
SOURCE_PINS = {
    "producer": "3eb4d9c917da67b9ab3dd186b37075040b8e6f01202129385d320c4ba7bca52f",
    "pure_core": "98f13225cbd9caf886242fbedf5071846b77df192727a7bdbc4075eb89a8adc8",
    "independent_verifier": "3212bb3d195e07ebac2ace134df93a8d602515b4fd2673c12da89e55722ef023",
}
SOURCE_PATHS = {
    "producer": ROOT / "deliverables/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2.py",
    "pure_core": ROOT / "deliverables/cm2_round306c72x_implicit_h1_root_physical_glue_core_v1.py",
    "independent_verifier": ROOT / "deliverables/cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_independent_verifier_v2.py",
}
RESULT_FILE_PIN = "0c8c56a86d3293dd08bc1fef95a72fe0aedc3a35edb20ff0ec9c6e19cd69d1f3"
RESULT_OBJECT_PIN = "a53e531998c8fe4a6ffbcaf11a2b4cfa8741e39c6aa4a979ebb45d10f807e241"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def capture(path: Path) -> tuple[bytes, dict[str, Any]]:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link:" + str(path))
        hasher = hashlib.sha256()
        parts = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
            parts.append(block)
        after = os.fstat(descriptor)
        identity = (before.st_dev, before.st_ino, before.st_size,
                    before.st_mtime_ns, before.st_ctime_ns)
        need(identity == (after.st_dev, after.st_ino, after.st_size,
                          after.st_mtime_ns, after.st_ctime_ns),
             "TOCTOU:" + str(path))
        return b"".join(parts), {
            "device": before.st_dev, "inode": before.st_ino,
            "size": before.st_size, "link_count": before.st_nlink,
            "sha256": hasher.hexdigest(), "terminal_byte_replay": True}
    finally:
        os.close(descriptor)


def closed_object(raw: bytes, label: str) -> dict[str, Any]:
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw,
         label + ":canonical object")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":closure")
    return value


def write_exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_CLOEXEC", 0), 0o644)
    try:
        view = memoryview(raw)
        while view:
            size = os.write(descriptor, view)
            need(size > 0, "short write")
            view = view[size:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def publish(stage_a: Path, stage_b: Path, verify_a: Path,
            verify_b: Path, output: Path) -> dict[str, Any]:
    need(stage_a != stage_b and verify_a != verify_b and not output.exists(),
         "distinct inputs/fresh output")
    need({path.name for path in stage_a.iterdir()} == set(NAMES) and
         {path.name for path in stage_b.iterdir()} == set(NAMES),
         "exact five-member stage sets")
    for key, path in SOURCE_PATHS.items():
        _raw, record = capture(path)
        need(record["sha256"] == SOURCE_PINS[key], "source pin:" + key)

    records: dict[str, dict[str, Any]] = {"build_a": {}, "build_b": {}}
    bytes_by_label: dict[str, bytes] = {}
    for name in NAMES:
        left_raw, left = capture(stage_a / name)
        right_raw, right = capture(stage_b / name)
        need(left_raw == right_raw and left["sha256"] == right["sha256"] and
             (left["device"], left["inode"]) !=
             (right["device"], right["inode"]),
             "dual byte identity/distinct inode:" + name)
        records["build_a"][name] = left
        records["build_b"][name] = right
        bytes_by_label["build_a/" + name] = left_raw
        bytes_by_label["build_b/" + name] = right_raw

    result_name = PREFIX + "_result.json"
    need(records["build_a"][result_name]["sha256"] == RESULT_FILE_PIN,
         "result file pin")
    result = closed_object(bytes_by_label["build_a/" + result_name], "result")
    need(result["object_sha256"] == RESULT_OBJECT_PIN and
         result["strict_whole_child_exclusion_count"] == 55216 and
         result["implicit_graph_strict_exclusion_count"] == 55213 and
         result["graph_endpoint_occurrence_count"] == 110426 and
         result["graph_endpoint_occurrence_unique_count"] == 110426 and
         result["unique_H1_boundary_root_count"] == 64262 and
         result["target_graph_root_degree_census"] ==
            {"1": 18098, "2": 46164} and
         result["explicit_residual_child_count"] == 0,
         "result exact census")

    verify_a_raw, verify_a_record = capture(verify_a)
    verify_b_raw, verify_b_record = capture(verify_b)
    need(verify_a_raw == verify_b_raw and
         verify_a_record["sha256"] == verify_b_record["sha256"] and
         (verify_a_record["device"], verify_a_record["inode"]) !=
         (verify_b_record["device"], verify_b_record["inode"]),
         "dual verification byte identity/distinct inode")
    verification = closed_object(verify_a_raw, "verification")
    coverage = verification["coverage"]
    need(verification["candidate_object_sha256"] == RESULT_OBJECT_PIN and
         verification["producer_source_sha256_declared_only"] ==
            SOURCE_PINS["producer"] and
         verification["verifier_file_sha256"] ==
            SOURCE_PINS["independent_verifier"] and
         verification["producer_source_imported_read_decoded_compiled_or_executed"]
            is False and
         verification["producer_source_path_opened_or_statted"] is False and
         verification["coherent_attacks"]["attack_count"] == 48 and
         coverage["whole_child_strict_exclusion_count"] == 55216 and
         coverage["implicit_graph_strict_exclusion_count"] == 55213 and
         coverage["graph_endpoint_occurrence_count"] == 110426 and
         coverage["unique_H1_boundary_root_count"] == 64262 and
         coverage["sum_incidence_count"] == 110426 and
         verification["formal_credit"] == verification["whole_parent_credit"] ==
         verification["D02_gate_credit"] == verification["CM2_credit"] == 0,
         "independent verification exact boundary")
    records["independent_verification_a"] = verify_a_record
    records["independent_verification_b"] = verify_b_record
    bytes_by_label["independent_verification_a"] = verify_a_raw
    bytes_by_label["independent_verification_b"] = verify_b_raw

    # Recapture every pre-receipt member immediately before the last write.
    paths = {
        **{"build_a/" + name: stage_a / name for name in NAMES},
        **{"build_b/" + name: stage_b / name for name in NAMES},
        "independent_verification_a": verify_a,
        "independent_verification_b": verify_b,
    }
    for label, path in paths.items():
        raw, _record = capture(path)
        need(raw == bytes_by_label[label], "pre-receipt terminal replay:" + label)
    ordered = [{"label": label, "sha256": hashlib.sha256(raw).hexdigest(),
                "size": len(raw)}
               for label, raw in sorted(bytes_by_label.items())]
    receipt = {
        "schema": SCHEMA,
        "status": "PASS_DUAL_5_OF_5_BYTE_IDENTICAL__DUAL_NO_PRODUCER_VERIFICATION_BYTE_IDENTICAL__55216_WHOLE_EXCLUSIONS__110426_ENDPOINTS_CONSERVED__OUTER_LAST__ZERO_CREDIT",
        "receipt_source_sha256": capture(SELF)[1]["sha256"],
        "source_file_sha256": SOURCE_PINS,
        "candidate_result_file_sha256": RESULT_FILE_PIN,
        "candidate_result_object_sha256": RESULT_OBJECT_PIN,
        "dual_build_records": records,
        "independent_verification_file_sha256": verify_a_record["sha256"],
        "independent_verification_object_sha256":
            verification["object_sha256"],
        "endpoint_conservation": {
            "graph_count": 55213, "endpoint_occurrence_count": 110426,
            "unique_root_count": 64262,
            "target_root_degree_census": {"1": 18098, "2": 46164},
            "identity": "18098+2*46164=110426"},
        "terminal_byte_replay": {
            "pre_receipt_member_count": len(ordered),
            "ordered_member_records_sha256": digest(ordered),
            "all_members_stable_single_link_exact_bytes": True,
            "outer_receipt_exclusive_write_and_replay": True},
        "candidate_is_authority": False,
        "global_consumption_ready": False,
        "runtime_canonical_pointer_or_seal_writes": False,
        "formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0, "CM2_credit": 0}
    receipt["object_sha256"] = digest(receipt)
    raw = canonical(receipt) + b"\n"
    write_exclusive(output, raw)
    replay, record = capture(output)
    need(replay == raw and record["sha256"] == hashlib.sha256(raw).hexdigest(),
         "outer receipt terminal replay")
    for label, path in paths.items():
        replay_member, _record = capture(path)
        need(replay_member == bytes_by_label[label],
             "post-receipt terminal replay:" + label)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage-a", type=Path, required=True)
    parser.add_argument("--stage-b", type=Path, required=True)
    parser.add_argument("--verify-a", type=Path, required=True)
    parser.add_argument("--verify-b", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = publish(args.stage_a.resolve(), args.stage_b.resolve(),
                     args.verify_a.resolve(), args.verify_b.resolve(),
                     args.output.resolve())
    print(json.dumps({"status": result["status"],
                      "object_sha256": result["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, ValueError, KeyError) as error:
        print(json.dumps({"status": "REJECTED", "reason": str(error)},
                         sort_keys=True), file=__import__("sys").stderr)
        raise SystemExit(2)
