#!/usr/bin/env python3
"""Independently analyze the C30c cold-verifier full strace transcript (v2).

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
WRITE_PREFIX = re.compile(r"^\s*\d+\s+(?:write|writev)\(")

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


def decimal_at(text: str, offset: int) -> tuple[int, int] | None:
    match = re.match(r"-?\d+", text[offset:])
    if match is None:
        return None
    return int(match.group(0)), offset + len(match.group(0))


def consume_fd_annotation(text: str, offset: int) -> int | None:
    """Consume one nonempty, printable ``strace -yy`` target decoration."""
    if offset >= len(text) or text[offset] != "<":
        return offset
    depth = 0
    cursor = offset
    nonspace: list[bool] = []
    while cursor < len(text):
        character = text[cursor]
        if not (0x20 <= ord(character) <= 0x7e):
            return None
        if character == "<":
            if nonspace and not nonspace[-1]:
                return None
            depth += 1
            nonspace.append(False)
        elif character == ">":
            if not nonspace or not nonspace[-1]:
                return None
            nonspace.pop()
            depth -= 1
            if depth == 0:
                cursor += 1
                break
            if depth < 0:
                return None
        elif not character.isspace():
            nonspace[-1] = True
        cursor += 1
    if depth != 0 or nonspace:
        return None
    if text.startswith("(deleted)", cursor):
        cursor += len("(deleted)")
    return cursor


def return_value(line: str, *, allow_fd_annotation: bool = True) -> int | None:
    """Parse only the return attached to the balanced outer syscall call.

    Looking merely for the last ``) = N`` is unsafe: a truncated record can
    end with those bytes inside a quoted payload.  Walk from the syscall's
    opening parenthesis, ignore escaped quoted data and balanced ``-yy`` FD
    annotations, and accept a result only after the outer call closes.  The
    remaining return grammar must consume the physical line through EOF.
    """
    prefix = LINE.match(line)
    if prefix is None:
        return None

    cursor = prefix.end()
    depth = 1
    quoted = False
    escaped = False
    while cursor < len(line):
        character = line[cursor]
        if character in "\r\n":
            return None
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            cursor += 1
            continue
        if character == '"':
            quoted = True
            cursor += 1
            continue
        if character == "<":
            annotated = consume_fd_annotation(line, cursor)
            if annotated is None or annotated == cursor:
                return None
            cursor = annotated
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                cursor += 1
                break
            if depth < 0:
                return None
        cursor += 1
    if depth != 0 or quoted or escaped:
        return None

    result = re.fullmatch(r"[ \t]*=[ \t]+(-?\d+)(.*)", line[cursor:])
    if result is None:
        return None
    value = int(result.group(1))
    suffix = result.group(2)
    annotated = consume_fd_annotation(suffix, 0)
    if annotated is None:
        return None
    if annotated != 0 and (not allow_fd_annotation or value < 0):
        return None
    remainder = suffix[annotated:]
    if value >= 0:
        if re.fullmatch(r"[ \t]*", remainder) is None:
            return None
    elif re.fullmatch(
        r"[ \t]+[A-Z][A-Z0-9_]+[ \t]+\([^\r\n]*\)[ \t]*", remainder,
    ) is None:
        return None
    return value


def successful(line: str) -> bool:
    value = return_value(line)
    return value is not None and value >= 0


def first_fd(line: str) -> int | None:
    """Return a syscall's first numeric FD despite ``strace -yy`` suffixes.

    Anonymous capture FDs are rendered as ``1</memfd:name>(deleted)``.  The
    v1 counter accepted ``1`` and ``1<path>`` but silently missed the
    additional controlled ``(deleted)`` suffix, so a real clean stdout write
    was miscounted as zero.  Parse the numeric argument itself and treat the
    ``-yy`` annotation as non-authoritative display metadata.
    """
    prefix = WRITE_PREFIX.match(line)
    if prefix is None:
        return None
    parsed = decimal_at(line, prefix.end())
    if parsed is None:
        return None
    descriptor, cursor = parsed
    annotated = consume_fd_annotation(line, cursor)
    if annotated is None or annotated >= len(line) or line[annotated] != ",":
        return None
    return descriptor


def write_census(
    rows: Iterable[tuple[int, str, str]], top_pid: int,
) -> tuple[int, int, int]:
    """Strictly census successful stdout bytes and every stderr write call."""
    stdout_calls = 0
    stdout_bytes = 0
    stderr_calls = 0
    for pid, syscall, line in rows:
        if syscall not in {"write", "writev"}:
            continue
        descriptor = first_fd(line)
        returned = return_value(line, allow_fd_annotation=False)
        need(descriptor is not None and returned is not None,
             "strict write/writev FD and anchored return grammar")
        if pid == top_pid and descriptor == 1 and returned >= 0:
            stdout_calls += 1
            stdout_bytes += returned
        if descriptor == 2 and returned >= 0:
            stderr_calls += 1
    return stdout_calls, stdout_bytes, stderr_calls


def exact_stdout_contract(calls: int, returned_bytes: int, captured_bytes: int) -> bool:
    return calls == 1 and returned_bytes == captured_bytes == 1839


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

    (top_level_stdout_writes, top_level_stdout_write_bytes,
     stderr_write_syscalls) = write_census(parsed, top_pid)
    protected_write_capable_opens = 0
    protected_path_mutations = 0
    protected_fd_writes = 0
    historical_candidate_reads = 0
    network_syscalls = 0
    for pid, syscall, line in parsed:
        is_success = successful(line)
        if syscall in OPEN_SYSCALLS:
            returned = return_value(line)
            need(returned is not None, "strict open/openat/openat2 anchored return")
            is_success = returned >= 0
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
        if syscall in NETWORK:
            network_syscalls += 1

    passing = (
        exit_status == 0
        and exact_stdout_contract(
            top_level_stdout_writes, top_level_stdout_write_bytes,
            len(stdout_raw),
        )
        and len(stderr_raw) == 0
        and stderr_write_syscalls == 0
        and protected_write_capable_opens == 0
        and protected_path_mutations == 0
        and protected_fd_writes == 0
        and historical_candidate_reads == 0
        and network_syscalls == 0
    )
    return {
        "schema": "cm2.round306c30c.cold-strace-audit.v2",
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
        "top_level_stdout_write_bytes": top_level_stdout_write_bytes,
        "stderr_bytes": len(stderr_raw),
        "stderr_write_syscalls": stderr_write_syscalls,
        "protected_write_capable_opens": protected_write_capable_opens,
        "protected_path_mutations": protected_path_mutations,
        "protected_fd_writes": protected_fd_writes,
        "historical_candidate_reads": historical_candidate_reads,
        "network_syscalls": network_syscalls,
    }


def self_test() -> dict[str, Any]:
    rows = {
        "plain_stdout": ("101 write(1, \"x\", 1) = 1", 1),
        "annotated_stdout": (
            "101 write(1</tmp/out>, \"x\", 1) = 1", 1,
        ),
        "deleted_memfd_stdout": (
            "101 write(1</memfd:cm2-v3-stdout>(deleted), \"x\", 1) = 1", 1,
        ),
        "deleted_memfd_stderr": (
            "101 writev(2</memfd:cm2-v3-stderr>(deleted), [], 0) = 0", 2,
        ),
        "two_digit_fd": ("101 write(10</tmp/out>, \"x\", 1) = 1", 10),
        "not_a_fd_call": ("101 +++ exited with 0 +++", None),
        "missing_close_angle": (
            "101 write(1</memfd:out(deleted), \"x\", 1) = 1", None,
        ),
        "duplicate_deleted": (
            "101 write(1</memfd:out>(deleted)(deleted), \"x\", 1) = 1", None,
        ),
        "garbage_after_annotation": (
            "101 write(1</memfd:out>junk, \"x\", 1) = 1", None,
        ),
        "empty_annotation": ("101 write(1<>, \"x\", 1) = 1", None),
        "nested_empty_annotation": (
            "101 write(1<<>>, \"x\", 1) = 1", None,
        ),
        "nonnumeric_fd": ("101 write(one, \"x\", 1) = 1", None),
        "bare_deleted": ("101 write(1(deleted), \"x\", 1) = 1", None),
        "pipe_stdout": ("101 write(1<pipe:[77]>, \"x\", 1) = 1", 1),
        "nested_char_device": (
            "101 write(1</dev/null<char 1:3>>, \"x\", 1) = 1", 1,
        ),
    }
    for label, (line, expected) in rows.items():
        need(first_fd(line) == expected, "first-FD regression:" + label)
    need(return_value(
        "101 write(1</memfd:out>(deleted), \"payload ) = 9\", 14) = 14"
    ) == 14, "anchored return ignores payload forgery")
    need(return_value(
        "101 write(1</memfd:o>(deleted), \"payload ) = 1839 forged\", 1)"
    ) is None, "missing physical return rejected despite payload forgery")
    need(return_value(
        "101 write(1</memfd:o>(deleted), \"payload ) = 1839"
    ) is None, "unterminated payload cannot forge line-tail return")
    need(return_value(
        "101 write(1</memfd:out>(deleted), \"x\", 1) = -1 EBADF (Bad file descriptor)"
    ) == -1, "anchored negative return")
    need(return_value(
        "101 openat(AT_FDCWD, \"/dev/null\", O_RDWR) = 5</dev/null<char 1:3>>"
    ) == 5, "nested strace return FD annotation")
    need(return_value(
        "101 openat(AT_FDCWD, \"/dev/null\", O_RDWR)"
        " = -1<fake> EBADF (Bad file descriptor)"
    ) is None, "negative return cannot carry FD target decoration")
    need(return_value(
        "101 write(1, \"x\", 1) = 1839<fake>",
        allow_fd_annotation=False,
    ) is None, "write scalar return cannot carry FD target decoration")
    census_rows = [
        (101, "write", "101 write(1</memfd:out>(deleted), \"x\", 1839) = 1839"),
        (101, "write", "101 write(10</tmp/fd10>, \"x\", 1) = 1"),
        (202, "write", "202 write(1<pipe:[88]>, \"x\", 1) = 1"),
        (101, "write", "101 write(1</memfd:out>(deleted), \"x\", 1) = -1 EBADF (Bad file descriptor)"),
    ]
    need(write_census(census_rows, 101) == (1, 1839, 0),
         "fd10/child/failing stdout writes excluded")
    need(exact_stdout_contract(*write_census(census_rows, 101)[:2], 1839),
         "one exact 1839-byte stdout contract")
    need(not exact_stdout_contract(0, 0, 1839)
         and not exact_stdout_contract(2, 1839, 1839)
         and not exact_stdout_contract(1, 1838, 1839)
         and not exact_stdout_contract(1, 1839, 1838),
         "zero/two/return-size/capture-size stdout contracts rejected")
    need(write_census([
        (101, "writev", "101 writev(2</memfd:err>(deleted), [], 0) = 0"),
    ], 101) == (0, 0, 1), "successful fd2 write counted")
    malformed_write_rejected = False
    try:
        write_census([
            (101, "write", "101 write(1</memfd:out>junk, \"x\", 1) = 1"),
        ], 101)
    except Reject:
        malformed_write_rejected = True
    need(malformed_write_rejected, "every malformed write is rejected")
    payload_return_rejected = False
    try:
        write_census([(
            101, "write",
            "101 write(1</memfd:o>(deleted), \"payload ) = 1839 forged\", 1)",
        )], 101)
    except Reject:
        payload_return_rejected = True
    need(payload_return_rejected,
         "payload return forgery cannot enter stdout census")
    write_return_annotation_rejected = False
    try:
        write_census([(
            101, "write", "101 write(1, \"x\", 1) = 1839<fake>",
        )], 101)
    except Reject:
        write_return_annotation_rejected = True
    need(write_return_annotation_rejected,
         "write return annotation cannot enter stdout census")
    paired, pair_count = reassemble_unfinished_records([
        "101 write(1</memfd:out>(deleted), \"x\", 1 <unfinished ...>",
        "102 write(2</memfd:err>(deleted), \"\", 0) = 0",
        "101 <... write resumed>) = 1",
    ])
    need(pair_count == 1 and len(paired) == 2
         and first_fd(paired[0]) == 2 and first_fd(paired[1]) == 1,
         "strict same-PID unfinished/resumed reassembly")
    malformed_resumed_rejected = False
    try:
        reassemble_unfinished_records([
            "101 write(1, \"x\", 1 <unfinished ...>",
            "101 <... writev resumed>) = 1",
        ])
    except Reject:
        malformed_resumed_rejected = True
    need(malformed_resumed_rejected, "mismatched resumed pairing rejected")
    return {
        "schema": "cm2.round306c30c.cold-strace-analyzer-v2-self-test.v1",
        "status": (
            "PASS_STRICT_STRACE_YY_DELETED_MEMFD_FD_RETURN_AND_PAIR_PARSE"
        ),
        "fd_case_count": len(rows), "census_case_count": 10,
        "pair_case_count": 2,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--trace", type=Path)
    parser.add_argument("--stdout", type=Path)
    parser.add_argument("--stderr", type=Path)
    parser.add_argument("--time", type=Path)
    parser.add_argument("--candidate-dir", type=Path)
    arguments = parser.parse_args()
    paths = (
        arguments.trace, arguments.stdout, arguments.stderr, arguments.time,
        arguments.candidate_dir,
    )
    if arguments.self_test:
        if any(path is not None for path in paths):
            parser.error("--self-test accepts no production inputs")
        print(canonical(self_test()).decode("ascii"))
        return 0
    if any(path is None for path in paths):
        parser.error("production mode requires all five input paths")
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
            "schema": "cm2.round306c30c.cold-strace-audit.v2",
            "status": "FAIL_CLOSED_C30C_COLD_TRACE",
            "error": str(error),
        }).decode("ascii"))
        return 1
    print(canonical(output).decode("ascii"))
    return 0 if output["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
