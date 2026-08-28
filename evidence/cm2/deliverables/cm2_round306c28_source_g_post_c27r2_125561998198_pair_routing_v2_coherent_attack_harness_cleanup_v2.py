#!/usr/bin/env python3
"""Append-only cleanup wrapper for the frozen C28-v2 26-attack harness.

The frozen v1 implementation remains the sole attack definition and is
byte-pinned before loading.  After all 26 attacks have been rejected and all
stderr hashes have been written to the receipt, this wrapper normalizes only
the two deliberately non-regular private clones (symlink and hardlink cases).
The authoritative candidate is never modified.  The successful scratch tree
therefore contains only regular single-link files and remains compatible with
the strict transaction-runner output snapshot.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
BASE = ROOT / (
    "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
    "pair_routing_v2_coherent_attack_harness.py"
)
BASE_SHA256 = "5ec0a477cfa9a78f4c104135ae58c6d6115c8cafef70e3e52653095054bf59be"
ROUTE_FILE = "cross_component_pair_route_shard.jsonl.gz"
LINK_CASES = (
    (17, "candidate-symlink-member", "symlink"),
    (18, "candidate-hardlink-member", "hardlink"),
)


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


def file_hash(path: Path) -> str:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular singleton:" + str(path))
        state = hashlib.sha256()
        while block := os.read(fd, 4 << 20):
            state.update(block)
        after = os.fstat(fd)
        need((before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
              before.st_size, before.st_mtime_ns, before.st_ctime_ns,
              before.st_uid, before.st_gid)
             == (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                 after.st_size, after.st_mtime_ns, after.st_ctime_ns,
                 after.st_uid, after.st_gid),
             "stable SHA/stat:" + str(path))
        return state.hexdigest()
    finally:
        os.close(fd)


def load_base() -> ModuleType:
    need(file_hash(BASE) == BASE_SHA256, "frozen v1 harness dependency pin")
    spec = importlib.util.spec_from_file_location("cm2_c28_attack_base_v1", BASE)
    need(spec is not None and spec.loader is not None,
         "v1 harness import specification")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    need(module.SELF == BASE and module.ROUTE_FILE == ROUTE_FILE,
         "v1 harness identity/constants")
    return module


def copy_regular(source: Path, target: Path) -> None:
    source_fd = os.open(source, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                        | getattr(os, "O_NOFOLLOW", 0))
    target_fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                        | getattr(os, "O_CLOEXEC", 0)
                        | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        source_info = os.fstat(source_fd)
        need(stat.S_ISREG(source_info.st_mode) and source_info.st_nlink == 1,
             "authoritative route regular singleton")
        while block := os.read(source_fd, 4 << 20):
            offset = 0
            while offset < len(block):
                offset += os.write(target_fd, block[offset:])
        os.fsync(target_fd)
    finally:
        os.close(target_fd)
        os.close(source_fd)
    info = os.lstat(target)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1
         and not target.is_symlink()
         and file_hash(target) == file_hash(source),
         "normalized route regular byte clone")


def normalize_link_cases(work: Path, authoritative: Path,
                         rejected: list[dict[str, Any]]) \
        -> list[dict[str, Any]]:
    by_ordinal = {record["ordinal"]: record for record in rejected}
    records: list[dict[str, Any]] = []
    source = authoritative / ROUTE_FILE
    source_sha = file_hash(source)
    for ordinal, name, kind in LINK_CASES:
        need(ordinal in by_ordinal and by_ordinal[ordinal]["name"] == name
             and by_ordinal[ordinal]["exit_code"] == 2
             and by_ordinal[ordinal]["verification_output_created"] is False
             and len(by_ordinal[ordinal]["stderr_sha256"]) == 64,
             "link attack rejection recorded before cleanup:" + name)
        attack_root = work / f"attack-{ordinal:02d}-{name}"
        private = attack_root / "candidate"
        target = private / ROUTE_FILE
        if kind == "symlink":
            info = os.lstat(target)
            need(stat.S_ISLNK(info.st_mode), "expected private symlink clone")
            target.unlink()
        else:
            sibling = attack_root / "hardlink-source-route.jsonl.gz"
            first = os.lstat(target)
            second = os.lstat(sibling)
            need(stat.S_ISREG(first.st_mode) and stat.S_ISREG(second.st_mode)
                 and first.st_ino == second.st_ino
                 and first.st_dev == second.st_dev
                 and first.st_nlink == 2 and second.st_nlink == 2,
                 "expected private two-link clone")
            target.unlink()
            sibling.unlink()
        copy_regular(source, target)
        records.append({
            "ordinal": ordinal, "name": name,
            "rejection_stderr_sha256": by_ordinal[ordinal]["stderr_sha256"],
            "nonregular_private_clone_removed_after_rejection": True,
            "normalized_route_sha256": file_hash(target),
            "authoritative_route_sha256": source_sha,
            "normalized_bytes_equal_authoritative":
                file_hash(target) == source_sha,
        })
    return records


def strict_regular_tree(root: Path) -> dict[str, Any]:
    file_count = 0
    for current, directory_names, file_names in os.walk(root):
        base = Path(current)
        for name in directory_names:
            path = base / name
            need(not path.is_symlink() and path.is_dir(),
                 "regular scratch directory topology:" + str(path))
        for name in file_names:
            path = base / name
            info = os.lstat(path)
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1
                 and not path.is_symlink(),
                 "regular single-link scratch member:" + str(path))
            file_count += 1
    need(file_count > 0, "nonempty normalized scratch tree")
    return {"all_files_regular_single_link": True,
            "all_directories_non_symlink": True,
            "file_count": file_count}


def rewrite_receipt(path: Path, value: dict[str, Any]) -> None:
    payload = canonical(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_TRUNC
                 | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "receipt regular singleton before cleanup annotation")
        offset = 0
        while offset < len(payload):
            offset += os.write(fd, payload[offset:])
        os.fsync(fd)
    finally:
        os.close(fd)
    need(path.read_bytes() == payload, "cleanup-annotated receipt bytes")


def run(args: Any, module: ModuleType) -> dict[str, Any]:
    module.SELF = SELF
    result = module.main_run(args)
    need(result.get("attack_census") == {
        "planned": 26, "executed": 26,
        "rejected_fail_closed": 26, "accepted": 0,
    }, "v1 exact 26/26 attack result")
    work = module.local(args.work_dir)
    candidate = module.local(args.candidate_dir)
    cleanup = normalize_link_cases(
        work, candidate, result["rejected_attacks"])
    tree = strict_regular_tree(work)
    body = dict(result)
    body.pop("attack_receipt_sha256", None)
    body["implementation_dependency"] = {
        "frozen_attack_harness_v1_path": str(BASE.relative_to(ROOT)),
        "frozen_attack_harness_v1_sha256": BASE_SHA256,
        "cleanup_wrapper_v2_sha256": args.expect_harness_sha256,
    }
    body["post_rejection_private_clone_cleanup"] = {
        "performed_only_after_all_26_rejection_error_hashes_recorded": True,
        "normalized_cases": cleanup,
        "authoritative_candidate_modified": False,
        "successful_scratch_tree": tree,
    }
    updated = {**body, "attack_receipt_sha256": digest(body)}
    rewrite_receipt(module.local(args.result_file), updated)
    return updated


def self_test(module: ModuleType) -> dict[str, Any]:
    base = module.self_test()
    need(base.get("status")
         == "PASS_SMALL_FIXTURE_CLOSURE_AND_PRIVATE_CLONE_TESTS",
         "frozen v1 self-test")
    with tempfile.TemporaryDirectory(prefix="cm2-c28-link-cleanup-v2-") as raw:
        root = Path(raw)
        source_dir = root / "authority"
        source_dir.mkdir()
        source = source_dir / ROUTE_FILE
        source.write_bytes(b"authoritative-route\n")
        records = [
            {"ordinal": ordinal, "name": name, "exit_code": 2,
             "stderr_sha256": hashlib.sha256(name.encode("ascii")).hexdigest(),
             "verification_output_created": False}
            for ordinal, name, _ in LINK_CASES
        ]
        for ordinal, name, kind in LINK_CASES:
            attack = root / f"attack-{ordinal:02d}-{name}"
            private = attack / "candidate"
            private.mkdir(parents=True)
            target = private / ROUTE_FILE
            if kind == "symlink":
                os.symlink(source, target)
            else:
                sibling = attack / "hardlink-source-route.jsonl.gz"
                sibling.write_bytes(source.read_bytes())
                os.link(sibling, target)
        cleanup = normalize_link_cases(root, source_dir, records)
        tree = strict_regular_tree(root)
        need(len(cleanup) == 2 and tree["all_files_regular_single_link"]
             and all(item["normalized_bytes_equal_authoritative"]
                     for item in cleanup),
             "link cleanup fixture")
    return {
        "schema": module.HARNESS_SCHEMA + ".cleanup-wrapper-v2.self-test",
        "status": "PASS_V1_26_ATTACK_DEPENDENCY_AND_POST_REJECTION_LINK_CLEANUP_FIXTURE",
        "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    try:
        module = load_base()
        args = module.parser().parse_args()
        fields = (
            "c27r2_terminal_dir", "authority_contract",
            "expect_authority_contract_sha256", "expect_terminal_root_sha256",
            "expect_terminal_receipt_file_sha256",
            "expect_terminal_receipt_object_sha256", "producer", "verifier",
            "python", "expect_producer_sha256", "expect_verifier_sha256",
            "expect_harness_sha256", "expect_python_sha256", "candidate_dir",
            "work_dir", "result_file",
        )
        if args.self_test:
            need(all(getattr(args, field) is None for field in fields),
                 "self-test accepts no attack arguments")
            result = self_test(module)
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all attack arguments required")
            need(file_hash(SELF) == args.expect_harness_sha256,
                 "cleanup wrapper self pin")
            result = run(args, module)
        sys.stdout.buffer.write(canonical({
            "status": result["status"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
