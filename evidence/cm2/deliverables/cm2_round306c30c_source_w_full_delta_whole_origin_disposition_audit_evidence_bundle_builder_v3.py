#!/usr/bin/env python3
"""Build the immutable C30c v3 raw-evidence bundle.

This version consumes only the exact v3 receipt transaction and the exact
post-receipt v3 bridge.  It never imports or accepts the legacy 20260807
receipt, adapters, publication directory, or publication tools.  A successful
bundle is still zero credit and cannot move Source-W from 80.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import stat
import tarfile
import tempfile
from pathlib import Path
from typing import Any

sys_dont_write_bytecode = True

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
AUDIT = WORKSPACE / ".cm2-runtime/audit"
RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260808T0635Z-receipt-v3"
BRIDGE_NAME = "c30c-postreceipt-v3-p1-bridge-v1-20260808T0655Z"
RUN = AUDIT / RUN_NAME
RECEIPT = WORKSPACE / ".cm2-runtime/receipts" / RUN_NAME
BRIDGE = AUDIT / BRIDGE_NAME
EXPECTED_VALIDATOR_SHA256 = "c68633b3cc996c344c737f1e6c71da382a81c8f6bf6c4318b233b6d9db34c97a"
EXPECTED_BRIDGE_SHA256 = "a7cd601b167f484fcddc2b4bd7a901cdbdcb0ada36b086ef5380057e769ba83c"
EXPECTED_RESULT_SHA256 = "df4531942e743389f5e8f85b2d013132f0808f562c21f430e7904577d67087d4"

RUN_FILES = frozenset({
    "command.txt", "end_utc.txt", "exit_code.txt", "observed_child_pids.txt",
    "post.sha256", "post.stat", "pre.sha256", "pre.stat", "provenance.json",
    "run.sh", "start_utc.txt", "stderr.log", "stdout.json", "time.txt",
    "time_pid.txt", "wrapper_pid.txt",
})
RECEIPT_FILES = frozenset({
    "build.json", "postrun-pin-check.log", "preflight-pin-check.log",
    "preflight.exit", "preflight.json", "preflight.stderr", "receipt.exit",
    "receipt.json", "receipt.stderr", "transaction-end-utc.txt",
    "transaction-run.exit",
})
BRIDGE_ROOT_FILES = frozenset({
    "preflight.json", "receipt_gate.json", "dual_checker_receipt.json",
    "cold_replay_receipt.json", "downstream_inventory.json",
    "terminal_status.json",
})
DUAL_FILES = frozenset({
    "pre.sha256", "pre.stat.json", "stdout.json", "stderr.log", "time.txt",
    "exit.txt", "post.sha256", "post.stat.json",
})
COLD_FILES = frozenset({
    "pre.sha256", "pre.stat.json", "trace.raw", "stdout.json", "stderr.log",
    "time.txt", "exit.txt", "post.sha256", "post.stat.json",
    "trace_audit.json", "trace_audit.stderr", "pairing_gate.json",
    "pairing_gate.stderr",
})


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Blocked(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def capture(path: Path, maximum: int = 64 << 30) -> tuple[bytes, tuple[int, ...]]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "canonical path:" + os.fspath(path))
    descriptor = os.open(absolute, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
             0 <= before.st_size <= maximum, "bounded singleton:" + os.fspath(path))
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(descriptor, min(4 << 20, remaining))
            need(bool(block), "complete read:" + os.fspath(path))
            chunks.append(block)
            remaining -= len(block)
        need(os.read(descriptor, 1) == b"", "stable EOF:" + os.fspath(path))
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after), "stable capture:" + os.fspath(path))
    return b"".join(chunks), identity(before)


def hash_size(path: Path) -> tuple[str, int]:
    state = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "hash singleton:" + os.fspath(path))
        total = 0
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
            total += len(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after) and total == before.st_size,
         "stable hash:" + os.fspath(path))
    return state.hexdigest(), total


def digest(path: Path) -> str:
    return hash_size(path)[0]


def strict_object(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(type(key) is str and key not in output, "unique key:" + label)
            output[key] = value
        return output
    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=unique,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise Blocked("strict JSON:" + label) from error
    need(type(value) is dict and raw in {canonical(value), canonical(value) + b"\n"},
         "canonical object:" + label)
    return value


def exact_members(directory: Path, expected: frozenset[str], label: str) -> None:
    need(directory.is_dir() and not directory.is_symlink(), "real directory:" + label)
    need({entry.name for entry in os.scandir(directory)} == set(expected),
         "exact members:" + label)


def sources() -> dict[str, Path]:
    exact_members(RUN, RUN_FILES, "v3 run")
    exact_members(RECEIPT, RECEIPT_FILES, "v3 receipt")
    root_names = {entry.name for entry in os.scandir(BRIDGE)}
    need(root_names == set(BRIDGE_ROOT_FILES) |
         {"dual-seed-30630071", "dual-seed-30630929", "cold-seed-30630071"},
         "exact bridge root")
    exact_members(BRIDGE / "dual-seed-30630071", DUAL_FILES, "dual 30630071")
    exact_members(BRIDGE / "dual-seed-30630929", DUAL_FILES, "dual 30630929")
    exact_members(BRIDGE / "cold-seed-30630071", COLD_FILES, "cold replay")
    output = {"transaction/run/" + name: RUN / name for name in RUN_FILES}
    output.update({"transaction/receipt/" + name: RECEIPT / name
                   for name in RECEIPT_FILES})
    output.update({"bridge/" + name: BRIDGE / name for name in BRIDGE_ROOT_FILES})
    for seed in ("30630071", "30630929"):
        output.update({"bridge/dual-seed-" + seed + "/" + name:
                       BRIDGE / ("dual-seed-" + seed) / name for name in DUAL_FILES})
    output.update({"bridge/cold-seed-30630071/" + name:
                   BRIDGE / "cold-seed-30630071" / name for name in COLD_FILES})
    return dict(sorted(output.items()))


def validate_boundary() -> dict[str, Any]:
    validator = WORKSPACE / "deliverables/cm2_round306c30c_62_attack_run_receipt_validator_v3.py"
    bridge_program = WORKSPACE / "deliverables/cm2_round306c30c_postreceipt_v3_p1_bridge_watch_v1.py"
    need(digest(validator) == EXPECTED_VALIDATOR_SHA256, "exact v3 validator bytes")
    need(digest(bridge_program) == EXPECTED_BRIDGE_SHA256, "exact v3 bridge bytes")
    receipt_raw, _ = capture(RECEIPT / "receipt.json", 4 << 20)
    receipt = strict_object(receipt_raw, "transaction receipt")
    need(receipt.get("schema") == "cm2.round306c30c.attack-run-receipt-validation.v3"
         and receipt.get("status") ==
         "PASS_COMPLETE_C30C_62_ATTACK_RUN_RECEIPT_V3__ZERO_FORMAL_CREDIT"
         and receipt.get("validator_sha256") == EXPECTED_VALIDATOR_SHA256
         and receipt.get("run_directory") == RUN_NAME
         and receipt.get("attack_count") == 62
         and receipt.get("numeric_exit_code") == 0
         and receipt.get("signal") is None
         and receipt.get("formal_credit") == 0
         and receipt.get("source_W_formal_remainder") == 80
         and receipt.get("source_W_transition_authorized") is False
         and receipt.get("downstream_publication_authorized") is False,
         "exact v3 transaction boundary")
    terminal_raw, _ = capture(BRIDGE / "terminal_status.json", 4 << 20)
    terminal = strict_object(terminal_raw, "bridge terminal")
    need(terminal.get("schema") == "cm2.round306c30c.postreceipt-v3-p1-bridge-watch.v1"
         and terminal.get("status") ==
         "PASS_ZERO_CREDIT_THROUGH_DUAL_AND_COLD__BLOCKED_BEFORE_PUBLICATION"
         and terminal.get("terminal_replay_completed") is False
         and terminal.get("formal_credit") == 0
         and terminal.get("source_W_formal_remainder") == 80
         and terminal.get("source_W_transition_authorized") is False
         and terminal.get("CM2") == "NO-GO_FOR_CLAIM",
         "exact bridge terminal zero-credit PASS")
    for key, name in (
        ("receipt_gate_sha256", "receipt_gate.json"),
        ("dual_checker_receipt_sha256", "dual_checker_receipt.json"),
        ("cold_replay_receipt_sha256", "cold_replay_receipt.json"),
        ("downstream_inventory_sha256", "downstream_inventory.json"),
    ):
        need(terminal.get(key) == digest(BRIDGE / name), "bridge hash binding:" + name)
    dual = strict_object(capture(BRIDGE / "dual_checker_receipt.json", 4 << 20)[0],
                         "dual checker receipt")
    cold = strict_object(capture(BRIDGE / "cold_replay_receipt.json", 4 << 20)[0],
                         "cold replay receipt")
    need(dual.get("status") ==
         "PASS_FRESH_DUAL_CONTROLLED_SEED_CHECKER__ZERO_FORMAL_CREDIT"
         and dual.get("candidate_result_sha256") == EXPECTED_RESULT_SHA256
         and dual.get("formal_credit") == 0
         and dual.get("source_W_transition_authorized") is False,
         "dual checker conclusion")
    need(cold.get("status") ==
         "PASS_FRESH_FULL_TRACE_COLD_REPLAY__ZERO_FORMAL_CREDIT"
         and cold.get("formal_credit") == 0
         and cold.get("source_W_transition_authorized") is False,
         "cold replay conclusion")
    return {"transaction_receipt_sha256": hashlib.sha256(receipt_raw).hexdigest(),
            "bridge_terminal_sha256": hashlib.sha256(terminal_raw).hexdigest()}


def exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o400)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(descriptor, view)
            need(count > 0, "complete write:" + path.name)
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def build(chain_dir: Path) -> dict[str, Any]:
    need(chain_dir.is_dir() and not chain_dir.is_symlink(), "real chain directory")
    boundary = validate_boundary()
    paths = sources()
    entries: dict[str, dict[str, Any]] = {}
    for name, path in paths.items():
        item_hash, item_size = hash_size(path)
        entries[name] = {"sha256": item_hash, "size": item_size}
    manifest = b"".join(
        (entries[name]["sha256"] + "  " + name + "\n").encode("ascii")
        for name in sorted(entries)
    )
    bundle = chain_dir / "c30c_v3_audit_evidence.tar.gz"
    need(not bundle.exists(), "fresh evidence bundle output")
    temporary = tempfile.NamedTemporaryFile(prefix=".c30c-v3-bundle-", dir=chain_dir,
                                             delete=False)
    temporary_path = Path(temporary.name)
    try:
        with temporary:
            with gzip.GzipFile(filename="", mode="wb", compresslevel=9,
                               fileobj=temporary, mtime=0) as compressed:
                with tarfile.open(fileobj=compressed, mode="w|",
                                  format=tarfile.GNU_FORMAT) as archive:
                    manifest_info = tarfile.TarInfo("MANIFEST.sha256")
                    manifest_info.size = len(manifest)
                    manifest_info.mode = 0o400
                    manifest_info.uid = manifest_info.gid = 0
                    manifest_info.uname = manifest_info.gname = ""
                    manifest_info.mtime = 0
                    import io
                    archive.addfile(manifest_info, io.BytesIO(manifest))
                    for name, path in paths.items():
                        info = tarfile.TarInfo(name)
                        info.size = entries[name]["size"]
                        info.mode = 0o400
                        info.uid = info.gid = 0
                        info.uname = info.gname = ""
                        info.mtime = 0
                        descriptor = os.open(
                            path, os.O_RDONLY | os.O_CLOEXEC |
                            getattr(os, "O_NOFOLLOW", 0),
                        )
                        try:
                            before = os.fstat(descriptor)
                            need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
                                 and before.st_size == entries[name]["size"],
                                 "archive source identity:" + name)
                            with os.fdopen(descriptor, "rb", closefd=False) as source:
                                archive.addfile(info, source)
                                need(source.tell() == before.st_size,
                                     "complete archive source read:" + name)
                            after = os.fstat(descriptor)
                        finally:
                            os.close(descriptor)
                        need(identity(before) == identity(after),
                             "archive source stable:" + name)
                        post_hash, post_size = hash_size(path)
                        need(post_hash == entries[name]["sha256"] and
                             post_size == entries[name]["size"],
                             "source unchanged across archive:" + name)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.link(temporary_path, bundle)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
    receipt = {
        "schema": "cm2.round306c30c.v3-audit-evidence-bundle.v1",
        "status": "PASS_EXACT_V3_TRANSACTION_AND_BRIDGE_EVIDENCE_BUNDLED__ZERO_FORMAL_CREDIT",
        "bundle": bundle.name,
        "bundle_sha256": digest(bundle),
        "entry_count": len(entries),
        "entries": entries,
        **boundary,
        "prior_authority_required": "ROUND306C30B_EXACT_MANIFEST",
        "formal_credit": 0,
        "source_W_formal_remainder": 80,
        "source_W_transition_authorized": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    exclusive(chain_dir / "evidence_bundle_receipt.json", canonical(receipt) + b"\n")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain-dir", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        result = build(arguments.chain_dir.resolve(strict=True))
    except (Blocked, OSError, ValueError, TypeError, KeyError) as error:
        print(canonical({"schema": "cm2.round306c30c.v3-audit-evidence-bundle.v1",
                         "status": "BLOCKED_FAIL_CLOSED", "error": str(error),
                         "formal_credit": 0, "source_W_formal_remainder": 80,
                         "source_W_transition_authorized": False,
                         "CM2": "NO-GO_FOR_CLAIM"}).decode("ascii"))
        return 1
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
