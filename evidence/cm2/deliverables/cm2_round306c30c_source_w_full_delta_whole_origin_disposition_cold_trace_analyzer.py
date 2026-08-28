#!/usr/bin/env python3
"""Independently analyze the C30c cold-verifier full strace transcript.

The analyzer consumes retained bytes only.  It requires ``strace -f -yy
-s 4096 -e trace=all``, rejects interleaved unfinished records, identifies the
top-level verifier PID, and recomputes the small fail-closed census consumed by
the C30c evidence bundle and outer verifier.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any, Iterable

sys.dont_write_bytecode = True

WORKSPACE = Path(__file__).resolve().parent.parent
DELIVERABLES = WORKSPACE / "deliverables"
RUNTIME = WORKSPACE / ".cm2-runtime/python-flint-0.9.0"
CANDIDATES = WORKSPACE / ".cm2-runtime/candidates"
PREFIX = "cm2_round306c30c_source_w_full_delta_whole_origin_disposition"
CANDIDATE_SPECS = {
    "cm2_round306c30b_python_flint_runtime_attestation.json": (
        30352, "6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df"
    ),
    PREFIX + "_combined_boundary_atomic_owner_join_ledger.jsonl.gz": (
        14320015, "63f004bdb065d8674ecfde9eb957f3477ee6c3f806064ef8f151850cd391d251"
    ),
    PREFIX + "_delta_h_cell_ledger.jsonl.gz": (
        727361, "acbd71e9155d81d17ae4b42eecd31f0fc9d4bb91ac36aa93a7ab7df08e3dee50"
    ),
    PREFIX + "_inherited_h_cell_ledger.jsonl.gz": (
        719350, "d4142d7748e0546184542bea7b3b337c9f33e7312efa2e7c5271d2a9dba30abd"
    ),
    PREFIX + "_result.json": (
        11697, "96c1e9f627bd6113fc56f7b6d35856581b57b4afde049e997b10eef3f8c706f1"
    ),
    PREFIX + "_whole_origin_ledger.jsonl.gz": (
        4473069, "48a3e612de84004ba746d93d492e8f3e9f587ebf6b3574615fa946dddf21a573"
    ),
}

LINE = re.compile(r"^\s*(\d+)\s+([A-Za-z0-9_]+)\(")
RETURN = re.compile(r"\)\s+=\s+(-?\d+)(?:\s|$)")
FD_PATH = re.compile(r"\b-?\d+<([^>]+)>")
UNFINISHED = re.compile(
    r"^(?P<prefix>\s*(?P<pid>\d+)\s+"
    r"(?P<syscall>[A-Za-z0-9_]+)\(.*)\s+<unfinished \.\.\.>$"
)
RESUMED = re.compile(
    r"^\s*(?P<pid>\d+)\s+<\.\.\. "
    r"(?P<syscall>[A-Za-z0-9_]+) resumed>(?P<suffix>.*)$"
)
WRITE_OPEN_FLAGS = re.compile(
    r"(?:^|[|, ])O_(?:WRONLY|RDWR|CREAT|TRUNC|APPEND|TMPFILE)(?:[|, )]|$)"
)

PATH_MUTATIONS = frozenset({
    "chmod", "chown", "creat", "fchmodat", "fchownat", "lchown",
    "link", "linkat", "mkdir", "mkdirat", "mknod", "mknodat",
    "mount", "open_by_handle_at", "pivot_root", "rename", "renameat",
    "renameat2", "rmdir", "symlink", "symlinkat", "truncate",
    "umount", "umount2", "unlink", "unlinkat", "utime", "utimensat",
    "utimes",
})
FD_MUTATIONS = frozenset({
    "copy_file_range", "fallocate", "fchmod", "fchown", "fdatasync",
    "fremovexattr", "fsetxattr", "fsync", "ftruncate", "io_uring_enter",
    "msync", "pwrite64", "pwritev", "pwritev2", "sendfile", "splice",
    "sync_file_range", "tee", "vmsplice", "write", "writev",
})
NETWORK = frozenset({
    "accept", "accept4", "bind", "connect", "getpeername", "getsockname",
    "getsockopt", "listen", "recv", "recvfrom", "recvmmsg", "recvmsg",
    "send", "sendmmsg", "sendmsg", "sendto", "setsockopt", "shutdown",
    "socket",
    "socketcall", "socketpair",
})
OPEN_SYSCALLS = frozenset({"open", "openat", "openat2"})


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity(status: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        status.st_dev, status.st_ino, status.st_mode, status.st_nlink,
        status.st_size, status.st_mtime_ns, status.st_ctime_ns,
    )


def canonical_path(path: Path, label: str) -> Path:
    absolute = Path(os.path.abspath(os.fspath(path)))
    need(absolute.resolve(strict=True) == absolute, "no symlink parent chain:" + label)
    return absolute


def capture_regular(
    path: Path, label: str, maximum: int, allow_empty: bool = False,
) -> bytes:
    absolute = canonical_path(path, label)
    before_path = absolute.lstat()
    need(
        stat.S_ISREG(before_path.st_mode) and before_path.st_nlink == 1
        and before_path.st_size <= maximum
        and (allow_empty or before_path.st_size > 0),
        "regular singleton bounds:" + label,
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = absolute.lstat()
    raw = b"".join(chunks)
    need(
        identity(before_path) == identity(before) == identity(after) == identity(current)
        and len(raw) == before.st_size,
        "stable single capture:" + label,
    )
    return raw


def validate_candidate(candidate: Path) -> None:
    path_before = candidate.lstat()
    need(
        stat.S_ISDIR(path_before.st_mode) and not candidate.is_symlink(),
        "candidate directory",
    )
    descriptor = os.open(
        candidate,
        os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened_before = os.fstat(descriptor)
        need(
            (opened_before.st_dev, opened_before.st_ino, opened_before.st_mode,
             opened_before.st_nlink, opened_before.st_mtime_ns,
             opened_before.st_ctime_ns)
            == (path_before.st_dev, path_before.st_ino, path_before.st_mode,
                path_before.st_nlink, path_before.st_mtime_ns,
                path_before.st_ctime_ns)
            and set(os.listdir(descriptor)) == set(CANDIDATE_SPECS),
            "candidate exact member map",
        )
        for filename, (expected_size, expected_hash) in sorted(CANDIDATE_SPECS.items()):
            entry = os.stat(filename, dir_fd=descriptor, follow_symlinks=False)
            need(
                stat.S_ISREG(entry.st_mode) and entry.st_nlink == 1
                and entry.st_size == expected_size,
                "candidate member singleton:" + filename,
            )
            member_fd = os.open(
                filename,
                os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=descriptor,
            )
            try:
                before = os.fstat(member_fd)
                state = hashlib.sha256()
                size = 0
                while block := os.read(member_fd, 1 << 20):
                    state.update(block)
                    size += len(block)
                after = os.fstat(member_fd)
            finally:
                os.close(member_fd)
            current = os.stat(filename, dir_fd=descriptor, follow_symlinks=False)
            need(
                identity(entry) == identity(before) == identity(after) == identity(current)
                and size == expected_size and state.hexdigest() == expected_hash,
                "candidate member stable fixed bytes:" + filename,
            )
        opened_after = os.fstat(descriptor)
        path_after = candidate.lstat()
        need(
            (opened_after.st_dev, opened_after.st_ino, opened_after.st_mode,
             opened_after.st_nlink, opened_after.st_mtime_ns,
             opened_after.st_ctime_ns)
            == (path_after.st_dev, path_after.st_ino, path_after.st_mode,
                path_after.st_nlink, path_after.st_mtime_ns,
                path_after.st_ctime_ns)
            == (path_before.st_dev, path_before.st_ino, path_before.st_mode,
                path_before.st_nlink, path_before.st_mtime_ns,
                path_before.st_ctime_ns)
            and set(os.listdir(descriptor)) == set(CANDIDATE_SPECS),
            "candidate stable exact directory",
        )
    finally:
        os.close(descriptor)


def ascii_text(raw: bytes, label: str) -> str:
    try:
        return raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise Reject("non-ASCII " + label) from error


def time_exit_status(raw: bytes) -> int:
    lines = [line.strip() for line in ascii_text(raw, "GNU time").splitlines()]
    commands = [
        line.removeprefix("Command being timed:").strip()
        for line in lines if line.startswith("Command being timed:")
    ]
    need(len(commands) == 1, "one GNU time command")
    command = commands[0]
    for token in (
        "/usr/bin/strace", " -f ", " -yy ", " -s 4096 ",
        " -e trace=all ",
    ):
        need(token in command, "full strace command token:" + token.strip())
    need(
        not any(line.startswith("Command terminated by signal") for line in lines),
        "cold command terminated by signal",
    )
    statuses = [
        line.removeprefix("Exit status:").strip()
        for line in lines if line.startswith("Exit status:")
    ]
    need(statuses == ["0"], "cold GNU time exit zero")
    return 0


def path_markers(path: Path) -> tuple[str, ...]:
    absolute = Path(os.path.abspath(os.fspath(path)))
    markers = {os.fspath(absolute)}
    try:
        relative = absolute.relative_to(WORKSPACE).as_posix()
    except ValueError:
        pass
    else:
        markers.add(relative)
    return tuple(sorted(markers, key=len, reverse=True))


def mentions(line: str, marker_groups: Iterable[tuple[str, ...]]) -> bool:
    return any(marker in line for group in marker_groups for marker in group)


def fd_mentions(line: str, marker_groups: Iterable[tuple[str, ...]]) -> bool:
    paths = FD_PATH.findall(line)
    return any(marker in path for path in paths for group in marker_groups for marker in group)


def successful(line: str) -> bool:
    match = RETURN.search(line)
    return match is not None and int(match.group(1)) >= 0


def reassemble_unfinished_records(lines: list[str]) -> tuple[list[str], int]:
    """Strictly pair strace unfinished/resumed rows by PID and syscall.

    ``strace -f`` necessarily interleaves a waiting parent with its child.
    The raw transcript therefore uses unfinished/resumed pairs even when both
    programs are single-threaded.  Reassembly happens before any existing
    mutation/network/path rule, and malformed pairing fails closed.
    """
    pending: dict[int, tuple[str, str]] = {}
    output: list[str] = []
    pair_count = 0
    for line in lines:
        unfinished = UNFINISHED.fullmatch(line)
        if unfinished is not None:
            pid = int(unfinished.group("pid"))
            need(pid not in pending, "duplicate/nested unfinished PID")
            pending[pid] = (
                unfinished.group("syscall"), unfinished.group("prefix").rstrip(),
            )
            continue

        resumed = RESUMED.fullmatch(line)
        if resumed is not None:
            pid = int(resumed.group("pid"))
            need(pid in pending, "resumed record without same-PID unfinished")
            syscall, prefix = pending.pop(pid)
            need(syscall == resumed.group("syscall"),
                 "unfinished/resumed syscall mismatch")
            output.append(prefix + resumed.group("suffix"))
            pair_count += 1
            continue

        ordinary = LINE.match(line)
        if ordinary is not None:
            pid = int(ordinary.group(1))
            need(pid not in pending, "same-PID syscall before pending resume")
        output.append(line)

    need(not pending, "unresolved unfinished strace records")
    return output, pair_count


def analyze_trace(
    trace_raw: bytes,
    stdout_raw: bytes,
    stderr_raw: bytes,
    time_raw: bytes,
    candidate_root: Path,
) -> dict[str, Any]:
    candidate = canonical_path(candidate_root, "candidate")
    need(
        candidate.is_dir()
        and candidate.is_relative_to(WORKSPACE),
        "canonical cold candidate directory inside workspace",
    )
    validate_candidate(candidate)
    text = ascii_text(trace_raw, "strace")
    raw_lines = text.splitlines()
    need(bool(raw_lines), "nonempty strace")
    lines, unfinished_resumed_pair_count = reassemble_unfinished_records(raw_lines)
    exit_status = time_exit_status(time_raw)
    parsed: list[tuple[int, str, str]] = []
    for line in lines:
        match = LINE.match(line)
        if match is None:
            need(
                re.match(
                    r"^\s*\d+\s+--- SIGCHLD \{.*si_code=CLD_EXITED,.*"
                    r"si_status=0,.*\} ---$",
                    line,
                ) is not None
                or re.match(r"^\s*\d+\s+\+\+\+ exited with 0 \+\+\+$", line)
                is not None,
                "parse every strace line or clean child-exit notification",
            )
            continue
        parsed.append((int(match.group(1)), match.group(2), line))
    exec_rows = [row for row in parsed if row[1] == "execve"]
    need(bool(exec_rows), "top-level execve")
    top_pid = exec_rows[0][0]

    protected_paths = tuple(dict.fromkeys((
        DELIVERABLES.resolve(strict=True),
        RUNTIME.resolve(strict=True),
        CANDIDATES.resolve(strict=True),
        candidate,
    )))
    protected_markers = tuple(path_markers(path) for path in protected_paths)
    candidate_markers = path_markers(candidate)
    candidates_markers = path_markers(CANDIDATES.resolve(strict=True))

    protected_write_capable_opens = 0
    protected_path_mutations = 0
    protected_fd_writes = 0
    historical_candidate_reads = 0
    top_level_stdout_writes = 0
    stderr_write_syscalls = 0
    network_syscalls = 0
    for pid, syscall, line in parsed:
        is_success = successful(line)
        if syscall in OPEN_SYSCALLS:
            is_protected = mentions(line, protected_markers)
            write_capable = WRITE_OPEN_FLAGS.search(line) is not None
            if is_protected and write_capable:
                protected_write_capable_opens += 1
            if (
                is_success and not write_capable
                and any(marker in line for marker in candidates_markers)
                and not any(marker in line for marker in candidate_markers)
            ):
                historical_candidate_reads += 1
        if syscall in PATH_MUTATIONS and mentions(line, protected_markers):
            protected_path_mutations += 1
        if syscall in FD_MUTATIONS and fd_mentions(line, protected_markers):
            protected_fd_writes += 1
        if (
            pid == top_pid and syscall in {"write", "writev"}
            and re.search(r"\((?:1|1<[^>]+>),", line) is not None
            and is_success
        ):
            top_level_stdout_writes += 1
        if (
            syscall in {"write", "writev"}
            and re.search(r"\((?:2|2<[^>]+>),", line) is not None
            and is_success
        ):
            stderr_write_syscalls += 1
        if syscall in NETWORK:
            network_syscalls += 1

    passing = (
        exit_status == 0
        and top_level_stdout_writes == 1
        and len(stderr_raw) == 0
        and stderr_write_syscalls == 0
        and protected_write_capable_opens == 0
        and protected_path_mutations == 0
        and protected_fd_writes == 0
        and historical_candidate_reads == 0
        and network_syscalls == 0
    )
    return {
        "schema": "cm2.round306c30c.cold-strace-audit.v1",
        "status": (
            "PASS_C30C_COLD_TRACE_ZERO_PROTECTED_MUTATION"
            if passing else "FAIL_CLOSED_C30C_COLD_TRACE"
        ),
        "capture": {
            "follow_forks": True,
            "fd_path_decoding": True,
            "string_limit": 4096,
            "trace_all_syscalls": True,
        },
        "candidate_root": os.fspath(candidate),
        "candidate_member_count": len(CANDIDATE_SPECS),
        "protected_roots": [os.fspath(path) for path in protected_paths],
        "top_level_pid": top_pid,
        "trace_raw_line_count": len(raw_lines),
        "trace_line_count": len(lines),
        "unfinished_resumed_pair_count": unfinished_resumed_pair_count,
        "trace_sha256": sha256(trace_raw),
        "stdout_sha256": sha256(stdout_raw),
        "stderr_sha256": sha256(stderr_raw),
        "time_sha256": sha256(time_raw),
        "exit_status": exit_status,
        "top_level_stdout_writes": top_level_stdout_writes,
        "stderr_bytes": len(stderr_raw),
        "stderr_write_syscalls": stderr_write_syscalls,
        "protected_write_capable_opens": protected_write_capable_opens,
        "protected_path_mutations": protected_path_mutations,
        "protected_fd_writes": protected_fd_writes,
        "historical_candidate_reads": historical_candidate_reads,
        "network_syscalls": network_syscalls,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", required=True, type=Path)
    parser.add_argument("--stdout", required=True, type=Path)
    parser.add_argument("--stderr", required=True, type=Path)
    parser.add_argument("--time", required=True, type=Path)
    parser.add_argument("--candidate-dir", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        output = analyze_trace(
            capture_regular(arguments.trace, "trace", 256 << 20),
            capture_regular(arguments.stdout, "stdout", 64 << 20),
            capture_regular(arguments.stderr, "stderr", 64 << 20, allow_empty=True),
            capture_regular(arguments.time, "time", 4 << 20),
            arguments.candidate_dir,
        )
    except (Reject, OSError, ValueError, TypeError) as error:
        print(canonical({
            "schema": "cm2.round306c30c.cold-strace-audit.v1",
            "status": "FAIL_CLOSED_C30C_COLD_TRACE",
            "error": str(error),
        }).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0 if output["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
