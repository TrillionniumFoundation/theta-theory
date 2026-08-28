#!/usr/bin/env python3
"""Strict workspace-Python entrypoint for the C28-v2 cleanup harness v3.

This append-only entrypoint pins both the frozen 26-attack implementation and
the post-rejection link-cleanup implementation.  It explicitly requires the
attack interpreter to be a regular single-link file inside this workspace;
the earlier experimental /usr/bin path exemption is neither imported nor
used.  Only private symlink/hardlink attack clones are normalized after their
fail-closed stderr hashes have been recorded.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
CLEANUP = ROOT / (
    "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
    "pair_routing_v2_coherent_attack_harness_cleanup_v2.py"
)
CLEANUP_SHA256 = "82d81a7b06986e094c49304fd4f67d100ccbcde062c52d074207029935e650f4"
BASE = ROOT / (
    "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
    "pair_routing_v2_coherent_attack_harness.py"
)
BASE_SHA256 = "5ec0a477cfa9a78f4c104135ae58c6d6115c8cafef70e3e52653095054bf59be"
RUNNER = ROOT / (
    "deliverables/cm2_round306c28_source_g_post_c27r2_125561998198_"
    "pair_routing_v2_transaction_runner_v1.py"
)
RUNNER_SHA256 = "d37ebb999f226d6af65338b9ccc5c40ace70de80bf1db32cd4e129740d740ae3"
WORKSPACE_PYTHON = ROOT / (
    ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807/"
    "fresh-python-flint-0.9.0/bin/python"
)
PYTHON_SHA256 = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"


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


def load_cleanup() -> ModuleType:
    need(file_hash(CLEANUP) == CLEANUP_SHA256,
         "cleanup implementation dependency pin")
    need(file_hash(BASE) == BASE_SHA256,
         "frozen 26-attack implementation dependency pin")
    spec = importlib.util.spec_from_file_location("cm2_c28_attack_cleanup_v2",
                                                   CLEANUP)
    need(spec is not None and spec.loader is not None,
         "cleanup import specification")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    need(module.BASE == BASE and module.BASE_SHA256 == BASE_SHA256,
         "cleanup dependency identity")
    return module


def load_runner() -> ModuleType:
    need(file_hash(RUNNER) == RUNNER_SHA256,
         "strict transaction-runner dependency pin")
    spec = importlib.util.spec_from_file_location("cm2_c28_transaction_runner_v1",
                                                   RUNNER)
    need(spec is not None and spec.loader is not None,
         "transaction-runner import specification")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    need(module.ROOT == ROOT, "transaction-runner workspace identity")
    return module


def workspace_regular_python(raw: str | Path, expected: str) -> Path:
    path = Path(raw).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Failure("attack Python outside workspace:" + str(path)) from error
    need(all(part not in {"", ".", ".."} for part in relative.parts),
         "canonical workspace Python path")
    cursor = ROOT
    for part in relative.parts:
        cursor = cursor / part
        need(cursor.exists() and not cursor.is_symlink(),
             "existing non-symlink Python path component:" + str(cursor))
    info = os.lstat(path)
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1
         and file_hash(path) == expected,
         "workspace regular single-link Python pin")
    return path


def run(args: Any, cleanup: ModuleType) -> dict[str, Any]:
    need(file_hash(SELF) == args.expect_harness_sha256,
         "harness v3 self pin")
    workspace_regular_python(args.python, args.expect_python_sha256)
    cleanup.SELF = SELF
    base = cleanup.load_base()
    result = cleanup.run(args, base)
    body = dict(result)
    body.pop("attack_receipt_sha256", None)
    body["implementation_dependency"] = {
        "frozen_attack_harness_v1_path": str(BASE.relative_to(ROOT)),
        "frozen_attack_harness_v1_sha256": BASE_SHA256,
        "post_rejection_cleanup_library_path":
            str(CLEANUP.relative_to(ROOT)),
        "post_rejection_cleanup_library_sha256": CLEANUP_SHA256,
        "strict_workspace_entrypoint_v3_sha256":
            args.expect_harness_sha256,
        "attack_python_policy":
            "WORKSPACE_REGULAR_SINGLE_LINK_ONLY__NO_USR_BIN_EXEMPTION",
        "attack_python_sha256": args.expect_python_sha256,
    }
    updated = {**body, "attack_receipt_sha256": digest(body)}
    cleanup.rewrite_receipt(cleanup.local(args.result_file), updated)
    return updated


def self_test(cleanup: ModuleType) -> dict[str, Any]:
    cleanup.SELF = SELF
    base = cleanup.load_base()
    nested = cleanup.self_test(base)
    need(nested.get("status")
         == "PASS_V1_26_ATTACK_DEPENDENCY_AND_POST_REJECTION_LINK_CLEANUP_FIXTURE",
         "cleanup dependency self-test")
    workspace_regular_python(WORKSPACE_PYTHON, PYTHON_SHA256)
    rejected_external = False
    try:
        workspace_regular_python(Path("/usr/bin/python3.12"), PYTHON_SHA256)
    except Failure:
        rejected_external = True
    need(rejected_external, "explicit /usr/bin Python rejection fixture")
    runner = load_runner()
    snapshot_passed = False
    strict_snapshot_rejected_nonregular = False
    with tempfile.TemporaryDirectory(
            prefix="cm2-c28-output-snapshot-cleanup-v3-",
            dir=ROOT / ".cm2-runtime/audit") as raw:
        fixture = Path(raw)
        source_dir = fixture / "authority"
        source_dir.mkdir()
        source = source_dir / cleanup.ROUTE_FILE
        source.write_bytes(b"authoritative-route\n")
        records = [
            {"ordinal": ordinal, "name": name, "exit_code": 2,
             "stderr_sha256": hashlib.sha256(name.encode("ascii")).hexdigest(),
             "verification_output_created": False}
            for ordinal, name, _ in cleanup.LINK_CASES
        ]
        for ordinal, name, kind in cleanup.LINK_CASES:
            attack = fixture / f"attack-{ordinal:02d}-{name}"
            private = attack / "candidate"
            private.mkdir(parents=True)
            target = private / cleanup.ROUTE_FILE
            if kind == "symlink":
                os.symlink(source, target)
            else:
                sibling = attack / "hardlink-source-route.jsonl.gz"
                sibling.write_bytes(source.read_bytes())
                os.link(sibling, target)
        specification = [{
            "path": str(fixture), "kind": "directory",
            "precondition": "ABSENT", "exact_inventory": None,
            "required_relative_files": [],
        }]
        try:
            runner.output_snapshot(specification)
        except runner.Failure:
            strict_snapshot_rejected_nonregular = True
        cleanup_records = cleanup.normalize_link_cases(
            fixture, source_dir, records)
        tree = cleanup.strict_regular_tree(fixture)
        snapshot = runner.output_snapshot(specification)
        snapshot_passed = (
            tree["all_files_regular_single_link"] is True
            and len(cleanup_records) == 2
            and snapshot[str(fixture)]["kind"] == "directory"
            and len(snapshot[str(fixture)]["files"]) == tree["file_count"]
        )
    need(strict_snapshot_rejected_nonregular and snapshot_passed,
         "strict output snapshot rejects before and passes after cleanup")
    return {
        "schema": base.HARNESS_SCHEMA + ".strict-cleanup-v3.self-test",
        "status": "PASS_26_ATTACK_LINK_CLEANUP_WORKSPACE_PYTHON_AND_STRICT_OUTPUT_SNAPSHOT_FIXTURE",
        "formal_credit": 0, "CM2": "NO-GO_FOR_CLAIM",
    }


def main() -> int:
    cleanup: ModuleType | None = None
    base: ModuleType | None = None
    try:
        cleanup = load_cleanup()
        base = cleanup.load_base()
        args = base.parser().parse_args()
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
            result = self_test(cleanup)
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all attack arguments required")
            result = run(args, cleanup)
        sys.stdout.buffer.write(canonical({
            "status": result["status"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2
    except Exception as error:
        if ((cleanup is not None and isinstance(error, cleanup.Failure))
                or (base is not None and isinstance(error, base.Failure))):
            sys.stderr.write("REJECT:" + str(error) + "\n")
            return 2
        raise


if __name__ == "__main__":
    raise SystemExit(main())
