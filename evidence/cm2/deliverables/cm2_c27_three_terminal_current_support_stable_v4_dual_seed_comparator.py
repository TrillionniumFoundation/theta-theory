#!/usr/bin/env python3
"""Fail-closed dual-seed comparator for stable current-support v4b outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any


WHITELIST = (
    "/fresh_positive_primitive_scan/inner_result_file_sha256",
    "/fresh_positive_primitive_scan/inner_result_sha256",
    "/invocation_seed",
    "/result_sha256",
    "/root_input_capture/attestations/self_produced_inner_result/path",
    "/root_input_capture/attestations/self_produced_inner_result/sha256",
    "/root_input_capture/attestations/self_produced_inner_result/stat_fingerprint/1",
    "/root_input_capture/attestations/self_produced_inner_result/stat_fingerprint/3",
    "/root_input_capture/attestations/self_produced_inner_result/stat_fingerprint/4",
    "/root_input_capture/attestations/self_produced_positive_ledger/path",
    "/root_input_capture/attestations/self_produced_positive_ledger/stat_fingerprint/1",
    "/root_input_capture/attestations/self_produced_positive_ledger/stat_fingerprint/3",
    "/root_input_capture/attestations/self_produced_positive_ledger/stat_fingerprint/4",
    "/semantic_projection_sha256",
)


class Reject(RuntimeError):
    pass


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise Reject(message)


def canon(x: Any) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def digest(x: Any) -> str:
    return hashlib.sha256(canon(x)).hexdigest()


def diff_paths(a: Any, b: Any, path: str = "") -> set[str]:
    if type(a) is not type(b):
        return {path or "/"}
    if isinstance(a, dict):
        if set(a) != set(b):
            return {path or "/"}
        out: set[str] = set()
        for key in sorted(a):
            out |= diff_paths(a[key], b[key], path + "/" + key)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return {path or "/"}
        out = set()
        for index, (left, right) in enumerate(zip(a, b)):
            out |= diff_paths(left, right, path + "/" + str(index))
        return out
    return set() if a == b else {path or "/"}


def normalize(value: dict[str, Any]) -> dict[str, Any]:
    copy = json.loads(canon(value))
    for pointer in WHITELIST:
        parts = pointer.strip("/").split("/")
        cursor: Any = copy
        for part in parts[:-1]:
            cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
        if isinstance(cursor, list):
            cursor[int(parts[-1])] = "__WHITELISTED_RUN_LOCAL_LEAF__"
        else:
            cursor[parts[-1]] = "__WHITELISTED_RUN_LOCAL_LEAF__"
    return copy


def validate_result(value: dict[str, Any], expected_seed: int,
                    expected_priority_sha: str, expected_positive_sha: str) -> None:
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(claimed == digest(body), "result closure")
    need(value["invocation_seed"] == expected_seed, "invocation seed")
    need(value["formal_credit"] == 0 and value["manifest_authorized"] is False,
         "zero-credit governance")
    need(value["CM2"] == "NO-GO_FOR_CLAIM", "CM2 governance")
    need(value["priority_ledger"] == {
        "file_sha256": expected_priority_sha,
        "filename": "current_support_91672_unique_priority_routes.jsonl.gz",
        "row_count": 91_672,
        "row_sequence_sha256": "4288caa4e676e82515bc643feab90718a8ff20f5522b0dfec6865e9cc6ead82e",
    }, "priority binding")
    need(value["fresh_positive_primitive_scan"]["positive_ledger_file_sha256"]
         == expected_positive_sha, "positive binding")
    need(value["primitive_pair_sets"] == {
        "COMPLETE": 36_140, "COMPLETE_only": 10_688, "POSITIVE_C19": 55_532,
        "POSITIVE_intersection_COMPLETE": 0, "POSITIVE_intersection_SIGNED": 0,
        "SIGNED": 25_452, "SIGNED_subset_COMPLETE": True, "union": 91_672,
    }, "primitive census")
    need(value["unique_priority_assignment_census"] == {
        "COMPLETE_BOUNDARY_FACES": 10_688,
        "POSITIVE_VOLUME_CARRIERS": 55_532,
        "SIGNED_BOUNDARY_FACES": 25_452,
    }, "priority census")


def compare_objects(seed1: dict[str, Any], seed2: dict[str, Any],
                    priority_sha: str, positive_sha: str) -> dict[str, Any]:
    validate_result(seed1, 30637101, priority_sha, positive_sha)
    validate_result(seed2, 30637991, priority_sha, positive_sha)
    observed = diff_paths(seed1, seed2)
    need(observed == set(WHITELIST), "exact difference whitelist")
    left, right = normalize(seed1), normalize(seed2)
    need(left == right, "normalized equality")
    return {
        "normalized_projection_sha256": digest(left),
        "observed_difference_paths": sorted(observed),
    }


def capture(path: Path, expected_sha: str) -> tuple[bytes, dict[str, Any]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode), "regular input")
        data = bytearray()
        h = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            h.update(block)
            data.extend(block)
        need(h.hexdigest() == expected_sha, "input pin")
        after = os.fstat(fd)
        fp = lambda st: (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns,
                         st.st_ctime_ns, st.st_mode, st.st_uid, st.st_gid)
        need(fp(before) == fp(after), "stable input")
        return bytes(data), {"path": str(path), "sha256": expected_sha,
                             "stat_fingerprint": list(fp(after)), "O_NOFOLLOW": True,
                             "single_open_file_description_hash_parse_fstat": True}
    finally:
        os.close(fd)


def main() -> int:
    ap = argparse.ArgumentParser()
    for prefix in ("seed1", "seed2"):
        for kind in ("result", "priority", "positive"):
            ap.add_argument(f"--{prefix}-{kind}", type=Path, required=True)
            ap.add_argument(f"--{prefix}-{kind}-sha256", required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    try:
        captured: dict[str, bytes] = {}
        attest: dict[str, Any] = {}
        for prefix in ("seed1", "seed2"):
            for kind in ("result", "priority", "positive"):
                label = prefix + "_" + kind
                data, receipt = capture(getattr(args, label), getattr(args, label + "_sha256"))
                captured[label], attest[label] = data, receipt
        need(captured["seed1_priority"] == captured["seed2_priority"], "priority byte identity")
        need(captured["seed1_positive"] == captured["seed2_positive"], "positive byte identity")
        seed1 = json.loads(captured["seed1_result"])
        seed2 = json.loads(captured["seed2_result"])
        comparison = compare_objects(seed1, seed2, args.seed1_priority_sha256,
                                     args.seed1_positive_sha256)
        need(args.seed1_priority_sha256 == args.seed2_priority_sha256
             and args.seed1_positive_sha256 == args.seed2_positive_sha256,
             "dual seed ledger pins")
        result = {
            "schema": "cm2.c27-independent.current-support-91672.dual-seed-comparison.v1",
            "status": "PASS_EXACT_WHITELISTED_NORMALIZATION_AND_BYTE_IDENTICAL_LEDGERS__ZERO_CREDIT",
            "formal_credit": 0,
            "manifest_authorized": False,
            "primary_priority_ledgers_byte_identical": True,
            "primary_positive_ledgers_byte_identical": True,
            "priority_ledger_sha256": args.seed1_priority_sha256,
            "positive_ledger_sha256": args.seed1_positive_sha256,
            "normalization": comparison,
            "run_local_difference_whitelist": list(WHITELIST),
            "root_input_capture": {"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                                   "attestations": attest},
            "C27_C28_C29": "FULL_REBUILD_REQUIRED__NO_PATCH_PROMOTION",
            "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result["result_sha256"] = digest(result)
        args.out_dir.mkdir(parents=True, exist_ok=False)
        path = args.out_dir / "comparison.json"
        path.write_bytes(canon(result) + b"\n")
        print(canon({"result": str(path), "result_sha256": result["result_sha256"]}).decode())
        return 0
    except (Reject, KeyError, IndexError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
