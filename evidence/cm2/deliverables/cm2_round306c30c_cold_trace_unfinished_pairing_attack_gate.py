#!/usr/bin/env python3
"""Attack/unit gate for strict C30c strace unfinished-pair reassembly."""
from __future__ import annotations

import hashlib
import json
import os
import stat
import types
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parent.parent
ANALYZER = (
    WORKSPACE / "deliverables"
    / "cm2_round306c30c_source_w_full_delta_whole_origin_disposition_"
      "cold_trace_analyzer.py"
)
ANALYZER_SHA256 = "a9f6c95a0def5f241ecbe25fc815c51a606b11a494b20fb43fbf82713f54732b"


class GateFailure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise GateFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def capture_analyzer() -> bytes:
    descriptor = os.open(
        ANALYZER, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1
            and 0 < before.st_size <= 4 << 20,
            "bounded analyzer singleton",
        )
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    fields = lambda value: (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )
    need(fields(before) == fields(after), "stable analyzer capture")
    raw = b"".join(chunks)
    need(hashlib.sha256(raw).hexdigest() == ANALYZER_SHA256,
         "pinned analyzer hash")
    return raw


def load_analyzer(raw: bytes) -> Any:
    module = types.ModuleType("cm2_c30c_pinned_trace_pairing_under_test")
    module.__file__ = os.fspath(ANALYZER)
    module.__package__ = ""
    exec(compile(raw, os.fspath(ANALYZER), "exec", dont_inherit=True), module.__dict__)
    need(callable(getattr(module, "reassemble_unfinished_records", None)),
         "pairing function present")
    return module


def rejected(module: Any, lines: list[str], expected: str) -> str:
    try:
        module.reassemble_unfinished_records(lines)
    except module.Reject as error:
        reason = str(error)
        need(reason == expected, "exact rejection reason:" + expected + ":" + reason)
        return reason
    raise GateFailure("malformed pairing accepted:" + expected)


def run() -> dict[str, Any]:
    module = load_analyzer(capture_analyzer())

    legal_single, count_single = module.reassemble_unfinished_records([
        "100 read(3</tmp/x>,  <unfinished ...>",
        "101 write(1</tmp/y>, \"x\", 1) = 1",
        "100 <... read resumed>\"\", 1) = 0",
    ])
    need(
        count_single == 1
        and legal_single == [
            "101 write(1</tmp/y>, \"x\", 1) = 1",
            "100 read(3</tmp/x>,\"\", 1) = 0",
        ],
        "one legal interleaved pairing",
    )

    legal_dual, count_dual = module.reassemble_unfinished_records([
        "200 vfork( <unfinished ...>",
        "201 execve(\"/bin/true\", [\"/bin/true\"], 0x0 <unfinished ...>",
        "200 <... vfork resumed>) = 201",
        "201 <... execve resumed>) = 0",
    ])
    need(
        count_dual == 2
        and legal_dual == ["200 vfork() = 201", "201 execve(\"/bin/true\", [\"/bin/true\"], 0x0) = 0"],
        "two legal cross-process pairings",
    )

    attacks = {
        "duplicate_unfinished": rejected(module, [
            "300 read(3,  <unfinished ...>",
            "300 read(3,  <unfinished ...>",
        ], "duplicate/nested unfinished PID"),
        "nested_unfinished": rejected(module, [
            "301 read(3,  <unfinished ...>",
            "301 write(4, \"x\", 1 <unfinished ...>",
        ], "duplicate/nested unfinished PID"),
        "wrong_syscall_name": rejected(module, [
            "302 read(3,  <unfinished ...>",
            "302 <... write resumed>\"\", 1) = 0",
        ], "unfinished/resumed syscall mismatch"),
        "dangling_unfinished": rejected(module, [
            "303 wait4(9,  <unfinished ...>",
        ], "unresolved unfinished strace records"),
        "cross_pid_resume": rejected(module, [
            "304 read(3,  <unfinished ...>",
            "305 <... read resumed>\"\", 1) = 0",
        ], "resumed record without same-PID unfinished"),
        "resume_without_unfinished": rejected(module, [
            "306 <... close resumed>) = 0",
        ], "resumed record without same-PID unfinished"),
        "same_pid_syscall_before_resume": rejected(module, [
            "307 read(3,  <unfinished ...>",
            "307 close(4) = 0",
        ], "same-PID syscall before pending resume"),
    }
    return {
        "schema": "cm2.round306c30c.cold-trace-unfinished-pairing-attack-gate.v1",
        "status": "PASS_STRICT_PID_SYSCALL_PAIRING_AND_7_ATTACKS__ZERO_FORMAL_CREDIT",
        "analyzer_sha256": ANALYZER_SHA256,
        "legal_pairing_tests": 2,
        "malformed_pairing_attacks": attacks,
        "attack_count": len(attacks),
        "formal_credit": 0,
        "source_W_transition_authorized": False,
    }


def main() -> int:
    try:
        output = run()
    except (GateFailure, OSError, ValueError, TypeError) as error:
        print(canonical({
            "schema": "cm2.round306c30c.cold-trace-unfinished-pairing-attack-gate.v1",
            "status": "BLOCKED_FAIL_CLOSED",
            "error": str(error),
            "formal_credit": 0,
            "source_W_transition_authorized": False,
        }).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
