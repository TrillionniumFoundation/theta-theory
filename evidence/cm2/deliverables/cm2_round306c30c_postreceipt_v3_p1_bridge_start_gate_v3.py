#!/usr/bin/env python3
"""Direct-Python ExecStartPre publisher v3 for the C30c bridge-v5 protocol.

The implementation is loaded from the exact watcher-v6 inode and held for the
whole gate.  The gate publishes pinset.json first and launch-anchor.json last;
it never starts or restarts a service itself.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
import subprocess
import sys
import types
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

WORKSPACE = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
SELF = WORKSPACE / "deliverables/cm2_round306c30c_postreceipt_v3_p1_bridge_start_gate_v3.py"
WATCHER = WORKSPACE / "deliverables/cm2_round306c30c_postreceipt_v3_p1_bridge_watch_v6.py"


class GateLoaderError(RuntimeError):
    pass


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_uid, value.st_gid, value.st_size,
        value.st_mtime_ns, value.st_ctime_ns,
    )


def stat9(value: os.stat_result) -> dict[str, int]:
    return {
        "dev": value.st_dev, "ino": value.st_ino, "mode": value.st_mode,
        "nlink": value.st_nlink, "uid": value.st_uid, "gid": value.st_gid,
        "size": value.st_size, "mtime_ns": value.st_mtime_ns,
        "ctime_ns": value.st_ctime_ns,
    }


def read_held(fd: int, maximum: int = 8 << 20) -> bytes:
    before = os.fstat(fd)
    if not (stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 <= before.st_size <= maximum):
        raise GateLoaderError("bounded singleton watcher-v6 source")
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    remaining = before.st_size
    while remaining:
        block = os.read(fd, min(1 << 20, remaining))
        if not block:
            raise GateLoaderError("complete watcher-v6 source read")
        chunks.append(block); remaining -= len(block)
    if os.read(fd, 1) != b"" or identity(before) != identity(os.fstat(fd)):
        raise GateLoaderError("stable watcher-v6 source read")
    return b"".join(chunks)


def load_held_watcher(
    expected_sha256: str | None,
) -> tuple[types.ModuleType, int, tuple[int, ...], str, dict[str, Any]]:
    if expected_sha256 is not None and re.fullmatch(
        r"[0-9a-f]{64}", expected_sha256,
    ) is None:
        raise GateLoaderError("approved watcher-v6 source SHA")
    before = WATCHER.lstat()
    if not (stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and stat.S_IMODE(before.st_mode) == 0o444
            and before.st_uid == 1000 and before.st_gid == 1000
            and 0 <= before.st_size <= 8 << 20):
        raise GateLoaderError(
            "raw watcher-v6 frozen owned bounded regular singleton",
        )
    fd = os.open(
        WATCHER, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(fd)
        if identity(before) != identity(opened):
            raise GateLoaderError("watcher-v6 loader open race")
        raw = read_held(fd)
        digest = hashlib.sha256(raw).hexdigest()
        if expected_sha256 is not None and digest != expected_sha256:
            raise GateLoaderError("watcher-v6 source SHA before compile")
        module = types.ModuleType("_cm2_bridge_watch_v6_held")
        module.__file__ = os.fspath(WATCHER)
        module.__package__ = ""
        sys.modules[module.__name__] = module
        exec(compile(raw, os.fspath(WATCHER), "exec"), module.__dict__)
        binding = {
            "path": os.fspath(WATCHER), "sha256": digest,
            "stat9": stat9(opened),
        }
        return module, fd, identity(opened), digest, binding
    except BaseException:
        os.close(fd)
        raise


def verify_loaded(fd: int, state: tuple[int, ...], digest: str) -> None:
    if identity(WATCHER.lstat()) != state or identity(os.fstat(fd)) != state:
        raise GateLoaderError("held watcher-v6 path/inode drift")
    if hashlib.sha256(read_held(fd)).hexdigest() != digest:
        raise GateLoaderError("held watcher-v6 byte drift")


def verify_executed_gate(
    fd: int, state: os.stat_result, raw: bytes,
    expected_sha256: str,
) -> dict[str, Any]:
    if Path(os.path.abspath(os.fspath(__file__))) != SELF:
        raise GateLoaderError("exact gate __file__ path")
    state_identity = identity(state)
    digest = hashlib.sha256(raw).hexdigest()
    if (re.fullmatch(r"[0-9a-f]{64}", expected_sha256) is None
            or digest != expected_sha256):
        raise GateLoaderError("executed gate raw expected SHA")
    if identity(SELF.lstat()) != state_identity or identity(os.fstat(fd)) != state_identity:
        raise GateLoaderError("executed gate path/held inode drift")
    replay = read_held(fd)
    if replay != raw:
        raise GateLoaderError("executed gate exact byte replay")
    return {
        "path": os.fspath(SELF),
        "sha256": digest,
        "stat9": stat9(state),
    }


def run_arguments(
    argv: list[str], executed_gate: dict[str, Any] | None,
) -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--publish", action="store_true")
    parser.add_argument("--bridge-dir", type=Path)
    parser.add_argument("--pinset", type=Path)
    parser.add_argument("--anchor", type=Path)
    parser.add_argument("--unit")
    parser.add_argument("--maximum-wait-seconds", type=int, default=7 * 24 * 3600)
    parser.add_argument("--watcher-source-sha256")
    arguments = parser.parse_args(argv)
    module: Any = None
    fd: int | None = None
    try:
        if arguments.publish:
            if re.fullmatch(
                r"[0-9a-f]{64}", arguments.watcher_source_sha256 or "",
            ) is None:
                raise GateLoaderError(
                    "production publish requires fragment-approved watcher SHA",
                )
            approved_watcher_sha256 = arguments.watcher_source_sha256
        else:
            if arguments.watcher_source_sha256 is not None:
                raise GateLoaderError(
                    "gate selftest rejects formal watcher source SHA",
                )
            approved_watcher_sha256 = None
        module, fd, state, digest, executed_watcher = load_held_watcher(
            approved_watcher_sha256,
        )
        if arguments.self_test:
            module.need(all(value is None for value in (
                arguments.bridge_dir, arguments.pinset,
                arguments.anchor, arguments.unit,
            )), "gate selftest has no formal launch material")
            result = module.gate_self_test(executed_gate)
        else:
            module.need(executed_gate is not None,
                        "production publish requires held -c gate bootstrap")
            module.need(arguments.bridge_dir is not None
                        and arguments.pinset is not None
                        and arguments.anchor is not None
                        and type(arguments.unit) is str,
                        "complete gate launch material")
            result = module.publish_gate_materials(
                arguments.bridge_dir, arguments.pinset, arguments.anchor,
                arguments.unit, arguments.maximum_wait_seconds, executed_gate,
                executed_watcher,
            )
        verify_loaded(fd, state, digest)
        print(module.canonical(result).decode("ascii"))
        return 0
    except (GateLoaderError, OSError, ValueError, TypeError, KeyError,
            subprocess.SubprocessError, RuntimeError) as error:
        if module is not None:
            failure = module.closed({
                "schema": "cm2.round306c30c.postreceipt-bridge-v5-start-gate-failure.v1",
                "status": "BLOCKED_FAIL_CLOSED_BEFORE_EXECSTART",
                "error": str(error), "formal_credit": 0,
                "source_W_formal_remainder": 80,
                "source_W_transition_authorized": False,
                "publication_authorized": False,
                "terminal_replay_completed": False,
                "CM2": "NO-GO_FOR_CLAIM",
            })
            print(module.canonical(failure).decode("ascii"), file=sys.stderr)
        else:
            print("start gate loader failure: " + str(error), file=sys.stderr)
        return 2
    finally:
        if fd is not None:
            os.close(fd)


def held_entry(
    gate_fd: int, gate_state: os.stat_result, gate_raw: bytes,
    expected_sha256: str, argv: list[str],
) -> int:
    try:
        binding = verify_executed_gate(
            gate_fd, gate_state, gate_raw, expected_sha256,
        )
        result = run_arguments(argv, binding)
        verify_executed_gate(
            gate_fd, gate_state, gate_raw, expected_sha256,
        )
        return result
    finally:
        os.close(gate_fd)


def main() -> int:
    return run_arguments(sys.argv[1:], None)


if __name__ == "__main__":
    raise SystemExit(main())
