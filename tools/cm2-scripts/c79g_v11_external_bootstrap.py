#!/usr/bin/env python3
"""External held-FD bootstrap for the frozen C79g v11 cold launcher.

This program launches exactly one explicitly requested positive-protocol
command.  It never retries.  It first pins the complete published v11 exact10,
checks the exact phase surface, copies the pinned launcher bytes into a fresh
sealed memfd, and finally execs the frozen launcher under Python isolated mode.

The launcher, not this wrapper, creates and owns the official coordination FD
and propagates the v11 coordination environment to its producer/consumer child.
"""

from __future__ import annotations

import ctypes
import fcntl
import hashlib
import json
import os
import stat
import sys
from typing import Any


ROOT_LABEL = "/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572"
ROOT_REL = b"home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
PYTHON = "/usr/bin/python3.12"

V10_REJECTION_REL = (
    ".cm2-runtime/c79g-v10-rejections-" + CHECKPOINT + "/rejection.json"
)
SCHEMA_REL = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "schema_v11.json"
)
CONTRACT_REL = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "contract_v11.json"
)
PRODUCER_REL = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_v11.py"
)
CONSUMER_REL = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "independent_verifier_assembler_authority_consumer_v11.py"
)
TRANSITION_REL = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "v10_to_v11_static_launch_transition_receipt_v1.json"
)
AUDIT_REL = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "static_audit_v11.json"
)
LAUNCHER_REL = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_v11.py"
)
MANIFEST_REL = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_manifest_v11.sha256"
)
OUTER_REL = (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "cold_launch_outer_receipt_v11.json"
)

# (root-relative path, file SHA-256, canonical object SHA-256 or None)
EXACT10: tuple[tuple[str, str, str | None], ...] = (
    (
        V10_REJECTION_REL,
        "1b5bbd9ec04f07e7d7d433685aa693b73bf2315a91e4813960bd5a81e8112828",
        "efdb614e870e70c20202834d3c6ec1a7513a3e98ba5cb4e1b32f87976a529d76",
    ),
    (
        SCHEMA_REL,
        "cf1630e3ab1b590876c663b8752d702eae5fe37b7bdbcc7824efbd03bbdbd8e2",
        None,
    ),
    (
        CONTRACT_REL,
        "c8851778bc8df7a9804efb5fc226548424b58119a2dff3f75bdea9fcac0ec5cf",
        "b998162a009927f13eb34a88e37f657515e43ae160b3d550de5edb0040486af9",
    ),
    (
        PRODUCER_REL,
        "f3b364afc0f5b2f729a3d7786eb8e9c25a9303959d6d2464a40395968090a30b",
        None,
    ),
    (
        CONSUMER_REL,
        "d8ad069e3486b9d657e4840e504885bf13129050f68e6cc04e47b71f149370ec",
        None,
    ),
    (
        TRANSITION_REL,
        "31b33566b898277fb8b272a6f3cd3b51b0b80eac4f58f43979dddfa647a38f4e",
        "9a253960a378521423751735dd272e06dec5c99cfc016d27bf66cfbe7673caaf",
    ),
    (
        AUDIT_REL,
        "6c94068e3f60a89fb608585ae5e6c7dbe02af17880195132bf7c9033ab797115",
        "007fba200b67c7704360bb85819435ed13cc6459c8dbac381b99c3adaaf884c3",
    ),
    (
        LAUNCHER_REL,
        "9f6971d2ca3e2c8f448a6aeed70bc16f38154c626f7744a4e20ba723e3082cc2",
        None,
    ),
    (
        MANIFEST_REL,
        "e27e9b58dbf57a72550da701589819dad7ebb01f6b3c649a56b701c99ef13135",
        None,
    ),
    (
        OUTER_REL,
        "689a4a323e742427c7f50ec6a7bbea08cdf28c36cbdb43d855a29601329f8c8f",
        "369dfe73b1dbc68e4147ba39e1c1b7155555b5443d9471159c5ac748723414a4",
    ),
)

EXPECTED_LAUNCHER_SHA256 = EXACT10[7][1]
EXPECTED_MANIFEST_SHA256 = EXACT10[8][1]

RUNTIME_REL = ".cm2-runtime"
AUTHORITY_HEADS_REL = RUNTIME_REL + "/cm2-global-authority-heads"
REJECTION_NAME = "c79g-v11-rejections-" + CHECKPOINT
CANDIDATE_A_NAME = "c79g-v11-candidate-a-" + CHECKPOINT
CANDIDATE_B_NAME = "c79g-v11-candidate-b-" + CHECKPOINT
VERIFICATION_A_NAME = "c79g-v11-verification-a-" + CHECKPOINT
VERIFICATION_B_NAME = "c79g-v11-verification-b-" + CHECKPOINT
COMPLETION_NAME = "c79g-v11-committed-completion-" + CHECKPOINT
AUTHORITY_NAME = "c79g-v11-" + CHECKPOINT + ".seal"

POSITIVE_NAMES = (
    CANDIDATE_A_NAME,
    CANDIDATE_B_NAME,
    VERIFICATION_A_NAME,
    VERIFICATION_B_NAME,
    COMPLETION_NAME,
)

REQUIRED_EXEC_SEALS = (
    getattr(fcntl, "F_SEAL_WRITE", 0x0008)
    | getattr(fcntl, "F_SEAL_GROW", 0x0004)
    | getattr(fcntl, "F_SEAL_SHRINK", 0x0002)
    | getattr(fcntl, "F_SEAL_SEAL", 0x0001)
)
F_ADD_SEALS = getattr(fcntl, "F_ADD_SEALS", 1033)
F_GET_SEALS = getattr(fcntl, "F_GET_SEALS", 1034)
MFD_CLOEXEC = getattr(os, "MFD_CLOEXEC", 0x0001)
MFD_ALLOW_SEALING = getattr(os, "MFD_ALLOW_SEALING", 0x0002)


class BootstrapFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise BootstrapFailure(message)


class OpenHow(ctypes.Structure):
    _fields_ = [
        ("flags", ctypes.c_uint64),
        ("mode", ctypes.c_uint64),
        ("resolve", ctypes.c_uint64),
    ]


LIBC = ctypes.CDLL(None, use_errno=True)
LIBC.syscall.restype = ctypes.c_long


def openat2(dirfd: int, path: str | bytes, flags: int) -> int:
    raw = path if isinstance(path, bytes) else os.fsencode(path)
    need(raw not in (b"", b".") and not raw.startswith(b"/"),
         "openat2 path must be a nonempty root-relative label")
    need(b".." not in raw.split(b"/"), "openat2 path traversal forbidden")
    resolve_no_xdev = 0x01
    resolve_no_magiclinks = 0x02
    resolve_no_symlinks = 0x04
    resolve_beneath = 0x08
    how = OpenHow(
        flags | os.O_CLOEXEC,
        0,
        resolve_no_xdev
        | resolve_no_magiclinks
        | resolve_no_symlinks
        | resolve_beneath,
    )
    ctypes.set_errno(0)
    descriptor = LIBC.syscall(
        437,
        dirfd,
        ctypes.c_char_p(raw),
        ctypes.byref(how),
        ctypes.sizeof(how),
    )
    if descriptor < 0:
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code), os.fsdecode(raw))
    return int(descriptor)


def read_all(fd: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            return b"".join(chunks)
        chunks.append(block)


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_uid,
        value.st_gid,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_object_sha256(raw: bytes) -> str:
    value = json.loads(raw)
    need(type(value) is dict, "canonical object must be a JSON object")
    declared = value.get("object_sha256")
    need(type(declared) is str, "canonical object declares object_sha256")
    material: dict[str, Any] = dict(value)
    del material["object_sha256"]
    canonical = json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    digest = sha256(canonical)
    need(declared == digest, "declared canonical object SHA-256")
    return digest


class HeldExact:
    def __init__(
        self,
        root_fd: int,
        relative: str,
        expected_file: str,
        expected_object: str | None,
    ) -> None:
        self.relative = relative
        self.expected_file = expected_file
        self.expected_object = expected_object
        self.fd = openat2(root_fd, relative, os.O_RDONLY)
        try:
            self.before = os.fstat(self.fd)
            self.raw = read_all(self.fd)
            after = os.fstat(self.fd)
            need(
                stat.S_ISREG(self.before.st_mode)
                and stat.S_IMODE(self.before.st_mode) == 0o444
                and self.before.st_nlink == 1,
                relative + ": regular 0444 nlink1",
            )
            need(
                fingerprint(self.before) == fingerprint(after),
                relative + ": identity-bracketed initial read",
            )
            need(sha256(self.raw) == expected_file, relative + ": file pin")
            if expected_object is not None:
                need(
                    canonical_object_sha256(self.raw) == expected_object,
                    relative + ": object pin",
                )
        except BaseException:
            os.close(self.fd)
            self.fd = -1
            raise

    def replay(self, root_fd: int) -> None:
        before = os.fstat(self.fd)
        raw = read_all(self.fd)
        after = os.fstat(self.fd)
        path_fd = openat2(root_fd, self.relative, os.O_RDONLY)
        try:
            path_state = os.fstat(path_fd)
            need(
                fingerprint(before)
                == fingerprint(self.before)
                == fingerprint(after)
                == fingerprint(path_state),
                self.relative + ": terminal fd/path identity replay",
            )
            need(raw == self.raw and sha256(raw) == self.expected_file,
                 self.relative + ": terminal byte replay")
        finally:
            os.close(path_fd)

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


def verify_publication(held: tuple[HeldExact, ...]) -> None:
    need(len(held) == 10, "published exact10 count")
    need(len({(item.before.st_dev, item.before.st_ino) for item in held}) == 10,
         "published exact10 inode identities are unique")
    need(len({item.before.st_dev for item in held}) == 1,
         "published exact10 share one device")
    manifest = b"".join(
        (item.expected_file + "  " + item.relative + "\n").encode("utf-8")
        for item in held[:8]
    )
    need(held[8].raw == manifest, "ordered exact8 manifest bytes")
    outer = json.loads(held[9].raw)
    expected_entries = [
        {"file_sha256": item.expected_file, "path": item.relative}
        for item in held[:8]
    ]
    need(
        type(outer) is dict
        and outer.get("schema")
        == "cm2.round306c79g.true-global-no-producer-consumer."
           "cold-launch-outer-receipt.v11"
        and outer.get("status")
        == "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__"
           "RUNTIME_DEFERRED"
        and outer.get("effective_checkpoint_object_sha256") == CHECKPOINT
        and outer.get("exact8_ordered_entries") == expected_entries
        and outer.get("cold_launch_manifest")
        == {
            "file_sha256": EXPECTED_MANIFEST_SHA256,
            "ordered_entry_count": 8,
            "path": MANIFEST_REL,
        }
        and outer.get("cold_launcher")
        == {"file_sha256": EXPECTED_LAUNCHER_SHA256, "path": LAUNCHER_REL}
        and outer.get("formal_global_closure_credit") == 0
        and outer.get("D02_unlock") is False
        and outer.get("runtime_executed_during_static_freeze") is False
        and outer.get("outer_published_after_exact8_manifest") is True
        and outer.get("runtime_entry_must_be_cold_launcher") is True,
        "v11 outer-last publication closure",
    )


def parse_command(argv: list[str]) -> tuple[list[str], str, set[str]]:
    candidate_a_rel = RUNTIME_REL + "/" + CANDIDATE_A_NAME
    candidate_b_rel = RUNTIME_REL + "/" + CANDIDATE_B_NAME
    candidate_a_abs = ROOT_LABEL + "/" + candidate_a_rel
    candidate_b_abs = ROOT_LABEL + "/" + candidate_b_rel

    if len(argv) == 3 and argv[0] == "build" and argv[1] == "--outdir":
        if argv[2] in (candidate_a_rel, candidate_a_abs):
            return ["build", "--outdir", candidate_a_abs], "build-a", set()
        if argv[2] in (candidate_b_rel, candidate_b_abs):
            return (
                ["build", "--outdir", candidate_b_abs],
                "build-b",
                {CANDIDATE_A_NAME},
            )
    if argv == ["verify", "--orientation", "a"]:
        return (
            list(argv),
            "verify-a",
            {CANDIDATE_A_NAME, CANDIDATE_B_NAME},
        )
    if argv == ["verify", "--orientation", "b"]:
        return (
            list(argv),
            "verify-b",
            {CANDIDATE_A_NAME, CANDIDATE_B_NAME, VERIFICATION_A_NAME},
        )
    if argv == ["assemble"]:
        return (
            list(argv),
            "assemble",
            {
                CANDIDATE_A_NAME,
                CANDIDATE_B_NAME,
                VERIFICATION_A_NAME,
                VERIFICATION_B_NAME,
            },
        )
    if argv == ["authorize"]:
        return (
            list(argv),
            "authorize",
            {
                CANDIDATE_A_NAME,
                CANDIDATE_B_NAME,
                VERIFICATION_A_NAME,
                VERIFICATION_B_NAME,
                COMPLETION_NAME,
            },
        )
    if argv == ["reject"]:
        return (list(argv), "reject", set())
    raise BootstrapFailure(
        "exactly one command required: build --outdir <exact A/B>, "
        "verify --orientation a/b, assemble, authorize, or reject"
    )


def verify_directory_member(parent_fd: int, name: str, label: str) -> None:
    state = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    need(
        stat.S_ISDIR(state.st_mode)
        and stat.S_IMODE(state.st_mode) == 0o555
        and state.st_nlink == 2,
        label + ": exact sealed directory",
    )


def verify_runtime_phase(root_fd: int, phase: str, expected: set[str]) -> None:
    runtime_fd = openat2(root_fd, RUNTIME_REL, os.O_RDONLY | os.O_DIRECTORY)
    authority_fd = -1
    try:
        runtime_names = set(os.listdir(runtime_fd))
        if phase == "reject":
            return
        current_names = {name for name in runtime_names if "c79g-v11" in name}
        if phase == "build-a":
            need(current_names == set(),
                 "build-a requires a wholly absent v11 runtime namespace")
        else:
            need(current_names == expected | {REJECTION_NAME},
                 phase + ": exact expected prior surfaces and empty rejection namespace")
            verify_directory_member(
                runtime_fd, REJECTION_NAME, phase + " rejection namespace"
            )
            rejection_fd = openat2(
                runtime_fd, REJECTION_NAME, os.O_RDONLY | os.O_DIRECTORY
            )
            try:
                need(os.listdir(rejection_fd) == [],
                     phase + ": rejection namespace remains exactly empty")
            finally:
                os.close(rejection_fd)
        for name in expected:
            verify_directory_member(runtime_fd, name, phase + " " + name)

        authority_fd = openat2(
            runtime_fd, "cm2-global-authority-heads", os.O_RDONLY | os.O_DIRECTORY
        )
        authority_names = {
            name for name in os.listdir(authority_fd) if "c79g-v11" in name
        }
        if phase == "authorize":
            need(authority_names in (set(), {AUTHORITY_NAME}),
                 "authorize permits only absent or exact committed v11 authority seal")
            if authority_names:
                state = os.stat(
                    AUTHORITY_NAME, dir_fd=authority_fd, follow_symlinks=False
                )
                need(
                    stat.S_ISREG(state.st_mode)
                    and stat.S_IMODE(state.st_mode) == 0o444
                    and state.st_nlink == 1,
                    "existing v11 authority is exact frozen seal",
                )
        else:
            need(authority_names == set(), phase + ": no v11 authority/stage surface")
    finally:
        if authority_fd >= 0:
            os.close(authority_fd)
        os.close(runtime_fd)


def make_sealed_exec(raw: bytes) -> int:
    need(hasattr(os, "memfd_create"), "Linux memfd_create is required")
    descriptor = os.memfd_create(
        "c79g-v11-external-bootstrap",
        MFD_CLOEXEC | MFD_ALLOW_SEALING,
    )
    try:
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            need(written > 0, "complete sealed memfd write")
            offset += written
        os.fsync(descriptor)
        os.fchmod(descriptor, 0o444)
        fcntl.fcntl(descriptor, F_ADD_SEALS, REQUIRED_EXEC_SEALS)
        before = os.fstat(descriptor)
        replay = read_all(descriptor)
        after = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode)
            and stat.S_IMODE(before.st_mode) == 0o444
            and before.st_nlink == 0
            and fingerprint(before) == fingerprint(after)
            and fcntl.fcntl(descriptor, F_GET_SEALS) == REQUIRED_EXEC_SEALS
            and replay == raw
            and sha256(replay) == EXPECTED_LAUNCHER_SHA256,
            "fresh launcher memfd exact bytes/mode/nlink/seals",
        )
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def close_unlisted_fds(keep: set[int]) -> None:
    for name in os.listdir("/proc/self/fd"):
        try:
            descriptor = int(name)
        except ValueError:
            continue
        if descriptor > 2 and descriptor not in keep:
            try:
                os.close(descriptor)
            except OSError:
                pass


def main(argv: list[str] | None = None) -> int:
    forwarded, phase, expected = parse_command(
        list(sys.argv[1:] if argv is None else argv)
    )
    slash_fd = os.open(
        "/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW
    )
    root_fd = -1
    exec_fd = -1
    held: tuple[HeldExact, ...] = ()
    try:
        root_fd = openat2(slash_fd, ROOT_REL, os.O_RDONLY | os.O_DIRECTORY)
        root_before = os.fstat(root_fd)
        root_path = os.lstat(ROOT_LABEL)
        need(
            stat.S_ISDIR(root_before.st_mode)
            and fingerprint(root_before) == fingerprint(root_path),
            "workspace label equals held root identity",
        )
        held = tuple(HeldExact(root_fd, *entry) for entry in EXACT10)
        try:
            verify_publication(held)
            verify_runtime_phase(root_fd, phase, expected)
            for item in held:
                item.replay(root_fd)
            launcher = held[7]
            need(launcher.relative == LAUNCHER_REL, "exact10 launcher position")
            exec_fd = make_sealed_exec(launcher.raw)
            need(
                len({exec_fd, launcher.fd, root_fd}) == 3
                and all(fd >= 3 for fd in (exec_fd, launcher.fd, root_fd)),
                "three distinct inherited bootstrap descriptors",
            )

            os.close(slash_fd)
            slash_fd = -1
            keep = {exec_fd, launcher.fd, root_fd}
            for item in held:
                if item is not launcher:
                    item.close()
            close_unlisted_fds(keep)
            for descriptor in keep:
                os.set_inheritable(descriptor, True)

            exec_argv = [
                PYTHON,
                "-I",
                "-B",
                "-S",
                "/proc/self/fd/" + str(exec_fd),
                "--bootstrap-exec-fd",
                str(exec_fd),
                "--bootstrap-source-fd",
                str(launcher.fd),
                "--bootstrap-root-fd",
                str(root_fd),
                "--cold-workspace-root",
                ROOT_LABEL,
                "--expected-launcher-sha256",
                EXPECTED_LAUNCHER_SHA256,
                *forwarded,
            ]
            clean_env = {
                "PATH": "/usr/bin:/bin",
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "TZ": "UTC",
            }
            os.execve(PYTHON, exec_argv, clean_env)
        finally:
            for item in held:
                item.close()
    except BootstrapFailure as exc:
        os.write(2, ("C79G_V11_BOOTSTRAP_REJECT: " + str(exc) + "\n").encode())
        return 2
    finally:
        for descriptor in (exec_fd, root_fd, slash_fd):
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
