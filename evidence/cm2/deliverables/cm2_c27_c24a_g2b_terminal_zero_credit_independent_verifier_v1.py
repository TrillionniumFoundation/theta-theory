#!/usr/bin/env python3
"""Independent verifier for the C24A G2B zero-credit terminal receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
RECEIPT_SHA = "2e81e5084eb16f20d02865d0e90696f3a776673b8df0f727a7438703ce78549f"
MANIFEST_SHA = "8874e499909bb4b70970133186b20682b78628ae71f82e2b47d25a516d8f5bcf"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def stable_read(path: Path, expected: str | None = None) -> tuple[bytes, str]:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode), "regular:" + str(path))
        state = hashlib.sha256()
        pieces: list[bytes] = []
        while block := os.read(fd, 4 << 20):
            state.update(block)
            pieces.append(block)
        observed = state.hexdigest()
        if expected is not None:
            need(observed == expected, "sha256:" + str(path))
        after = os.fstat(fd)
        need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
              before.st_ctime_ns, before.st_mode, before.st_uid, before.st_gid)
             == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                 after.st_ctime_ns, after.st_mode, after.st_uid, after.st_gid),
             "stable fstat:" + str(path))
        return b"".join(pieces), observed
    finally:
        os.close(fd)


def verify(args: argparse.Namespace) -> dict[str, Any]:
    receipt_path = Path(args.receipt).resolve()
    manifest_path = Path(args.manifest).resolve()
    receipt_raw, _ = stable_read(receipt_path, RECEIPT_SHA)
    manifest_raw, _ = stable_read(manifest_path, MANIFEST_SHA)
    receipt = json.loads(receipt_raw)
    need(type(receipt) is dict and canonical(receipt) + b"\n" == receipt_raw,
         "receipt canonical bytes")
    body = dict(receipt)
    claimed = body.pop("result_sha256")
    need(claimed == digest(body) == "a2c444105fc9677dea2e17d4144dc0f6c6cb5de695353fa46da367d141f42ac0",
         "receipt closure")
    need(receipt["status"]
         == "PASS_TERMINAL_DIAGNOSTIC_C24A_G2B_EXACT_ROUTE__ZERO_FORMAL_CREDIT"
         and receipt["G2B_closed_diagnostic"] == {
             "candidate_pairs": 18800,
             "cross_current_C15_positive_member_pairs": 596,
             "edges_already_in_C27R1D": 144,
             "exact_empty": 9392,
             "exact_positive": 9408,
             "incremental_rank_reduction_after_C27R1D": 0,
             "new_component_edges_after_C27R1D": 0,
             "unique_old_C15_component_edges": 144,
             "unresolved": 0,
         }
         and receipt["three_terminal_priority"]["union"] == 45548
         and receipt["dual_implementation_exact_mismatch_count"] == 0
         and receipt["coherent_attacks"] == {"accepted": 0, "rejected": 37},
         "terminal diagnostic census")
    need(receipt["open_blockers"] == [
             "C24A_G2A_5264_RELATIVE_2D_COMPLETE_OR_UNIQUE_DIMENSIONAL_ROUTE_OPEN",
             "THREE_TERMINAL_GLOBAL_CANDIDATE_TOTALITY_AND_UNIQUE_ASSIGNMENT_OPEN",
             "C27_C28_C29_FULL_REBUILD_MUST_UNION_ALL_EXISTING_STRICT_VOLUME_AND_C19_WITNESSES_WITH_C24A_BRANCH",
             "NO_PATCH_PROMOTION_AND_NO_PHYSICAL_MAXIMALITY_CLAIM",
         ]
         and receipt["formal_state_unchanged"] == {
             "C27_transition_totality": 0,
             "C28_pair_routing": 0,
             "C29_physical_maximality": 0,
             "CM2": "NO-GO_FOR_CLAIM",
             "Source_W_remaining": 80,
             "formal_credit": 0,
             "latest_formal_seal": "Round306C30b",
             "manifest_authorized": False,
         }, "strict zero-credit state")

    lines = manifest_raw.decode("ascii").splitlines()
    need(len(lines) == 39 and lines == sorted(lines, key=lambda line: line.split("  ", 1)[1]),
         "manifest census/order")
    entries: dict[str, str] = {}
    for line in lines:
        sha, relative = line.split("  ", 1)
        need(len(sha) == 64 and relative not in entries, "manifest entry")
        entries[relative] = sha
        stable_read(ROOT / relative, sha)
    receipt_relative = str(receipt_path.relative_to(ROOT))
    need(entries[receipt_relative] == RECEIPT_SHA, "manifest receipt member")
    authorities = receipt["root_input_capture"]["authorities"]
    need(len(authorities) == 20, "authority count")
    for item in authorities.values():
        need(entries[item["path"]] == item["sha256"]
             and item["O_NOFOLLOW"] is True
             and item["single_open_file_description_hash_parse_fstat"] is True,
             "authority receipt/manifest binding")
    clean_runs = receipt["root_input_capture"]["clean_run_receipts"]
    need(set(clean_runs) == {"primary_seed1", "primary_seed2", "priority_seed1",
                             "priority_seed2", "comparator", "attacks"},
         "clean run set")
    for run in clean_runs.values():
        for filename, expected in (("exit_code.txt", b"0\n"),
                                   ("signal.txt", b"null\n"),
                                   ("stderr.log", b"")):
            item = run[filename]
            need(entries[item["path"]] == item["sha256"],
                 "clean run receipt/manifest binding")
            raw, observed = stable_read(ROOT / item["path"], item["sha256"])
            need(raw == expected and observed == item["sha256"], "clean run receipt")

    result = {
        "schema": "cm2.c27-independent.c24a-g2b-terminal-zero-credit-verification.v1",
        "status": "PASS_INDEPENDENT_TERMINAL_RECEIPT_AND_MANIFEST_VERIFICATION__ZERO_CREDIT",
        "manifest_entry_count": len(entries),
        "authority_count": len(authorities),
        "clean_run_count": len(clean_runs),
        "receipt_file_sha256": RECEIPT_SHA,
        "receipt_result_sha256": claimed,
        "manifest_file_sha256": MANIFEST_SHA,
        "G2A_5264": "OPEN",
        "three_terminal_global_totality": "OPEN",
        "C27_C28_C29": "FULL_REBUILD_REQUIRED__NO_PATCH_PROMOTION",
        "formal_credit": 0,
        "manifest_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result["result_sha256"] = digest(result)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=False)
    (out / "verification.json").write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    try:
        result = verify(args)
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
