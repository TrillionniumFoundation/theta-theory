#!/usr/bin/env python3
"""Freeze and permanently supersede the unpublished C79g v13 draft.

This guard has exactly two commands.  ``PREFLIGHT`` is read-only.
``FREEZE_REJECT`` is a one-shot append-only transition: under one official
writer lock it holds the eight pinned evidence files, freezes each to 0444,
terminally replays the joint exact8, completes one canonical object-closed
receipt on an anonymous O_TMPFILE inode, atomically publishes it through the
unprivileged /proc/self/fd route with linkat(AT_SYMLINK_FOLLOW) no-replace
semantics, and terminally replays the exact9.

The guard never imports or executes a v13 protocol source and never invokes
py_compile.  Source validation is limited to AST parsing and in-memory
``compile``.  Existing pyc files are treated only as inert incident evidence.
"""

from __future__ import annotations

import ast
import ctypes
import errno
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any


FINAL_V13_PREPUBLICATION_SUPERSESSION_GUARD_PINS_INSTALLED = True
ROOT_EXPECTED = Path(
    "/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
RECEIPT_REL = (
    f"deliverables/{BASE}_v13_prepublication_pyc_contamination_"
    "rejection_supersession_receipt_v1.json")


# These are the last accepted mutable identities of the unpublished v13
# draft.  st_dev/st_ino are deliberately checked live but never persisted.
# ctime is a pre-freeze pin only; fchmod necessarily advances it.
EVIDENCE_EXACT8: tuple[dict[str, Any], ...] = (
    {
        "name": "v13_build_only_producer_source",
        "role": "LIVE_SUCCESSOR_REQUIRED_INCIDENT_SOURCE",
        "path": f"deliverables/{BASE}_v13.py",
        "file_sha256": "ec4982babaec3bfb6693e29a220ca827087fb591c77f6c715889e934f124310e",
        "size": 469323,
        "mtime_ns": 1787216160026242689,
        "ctime_ns": 1787216160026242689,
    },
    {
        "name": "v13_independent_consumer_source",
        "role": "LIVE_SUCCESSOR_REQUIRED_INCIDENT_SOURCE",
        "path": (
            f"deliverables/{BASE}_independent_verifier_assembler_"
            "authority_consumer_v13.py"),
        "file_sha256": "a8b32b7e0073e70a95e6f5f17ad08b63b701ca64a1299f0f614215c5aa9f970a",
        "size": 728991,
        "mtime_ns": 1787217183411459996,
        "ctime_ns": 1787217183411459996,
    },
    {
        "name": "v13_cold_launcher_source",
        "role": "LIVE_SUCCESSOR_REQUIRED_INCIDENT_SOURCE",
        "path": f"deliverables/{BASE}_cold_launch_v13.py",
        "file_sha256": "aa1306ed3e764c69679db531c3dcd30d609ed1cbd699feda5ed17cc1e24da88b",
        "size": 426209,
        "mtime_ns": 1787216274620013909,
        "ctime_ns": 1787216274620013909,
    },
    {
        "name": "v13_json_draft_builder_tool",
        "role": "SUPPLEMENTAL_TOOLING_EVIDENCE",
        "path": "scripts/c79g_v13_json_draft_builder.py",
        "file_sha256": "2276f24b42b640b0887978313292b8733e0a6c2577e7db04f5605e20942d10aa",
        "size": 102351,
        "mtime_ns": 1787216680511245841,
        "ctime_ns": 1787216680511245841,
    },
    {
        "name": "v13_independent_static_review_tool",
        "role": "SUPPLEMENTAL_TOOLING_EVIDENCE",
        "path": "scripts/c79g_v13_independent_static_review.py",
        "file_sha256": "1d788514dc691007978fd0c3d4e66d285152f975a6b78130a463fbbc7f62df5b",
        "size": 124407,
        "mtime_ns": 1787217638328368977,
        "ctime_ns": 1787217638328368977,
    },
    {
        "name": "v13_build_only_producer_pyc",
        "role": "LIVE_SUCCESSOR_REQUIRED_INCIDENT_PYC",
        "path": (
            f"deliverables/__pycache__/{BASE}_v13.cpython-312.pyc"),
        "file_sha256": "0383cab58260ff076b18482f2077ed100456b21bcc2587afd5e457c8a19d7d36",
        "size": 505842,
        "mtime_ns": 1787216296545548868,
        "ctime_ns": 1787216296545548868,
        "source_path": f"deliverables/{BASE}_v13.py",
        "pep552_flags": 0,
        "pep552_timestamp": 1787216160,
        "pep552_source_size": 469323,
        "pep552_header_hex": "cb0d0d0a0000000020c1866a4b290700",
    },
    {
        "name": "v13_independent_consumer_pyc",
        "role": "LIVE_SUCCESSOR_REQUIRED_INCIDENT_PYC",
        "path": (
            f"deliverables/__pycache__/{BASE}_independent_verifier_assembler_"
            "authority_consumer_v13.cpython-312.pyc"),
        "file_sha256": "f13c8f7f40139bcbe6d5f20014fb14d8659539814baf985f73f99fbb13ffccaa",
        "size": 757095,
        "mtime_ns": 1787217214106131763,
        "ctime_ns": 1787217214106131763,
        "source_path": (
            f"deliverables/{BASE}_independent_verifier_assembler_"
            "authority_consumer_v13.py"),
        "pep552_flags": 0,
        "pep552_timestamp": 1787217183,
        "pep552_source_size": 728991,
        "pep552_header_hex": "cb0d0d0a000000001fc5866a9f1f0b00",
    },
    {
        "name": "v13_cold_launcher_pyc",
        "role": "LIVE_SUCCESSOR_REQUIRED_INCIDENT_PYC",
        "path": (
            f"deliverables/__pycache__/{BASE}_cold_launch_v13.cpython-312.pyc"),
        "file_sha256": "50a210fe6c414d140f7e0ac9a969500192f68fafae2de9d104526d73479365e0",
        "size": 502218,
        "mtime_ns": 1787216296813997199,
        "ctime_ns": 1787216296813997199,
        "source_path": f"deliverables/{BASE}_cold_launch_v13.py",
        "pep552_flags": 0,
        "pep552_timestamp": 1787216274,
        "pep552_source_size": 426209,
        "pep552_header_hex": "cb0d0d0a0000000092c1866ae1800600",
    },
)


V12_EXACT10: tuple[dict[str, Any], ...] = (
    {
        "path": f".cm2-runtime/c79g-v11-rejections-{CHECKPOINT}/rejection.json",
        "file_sha256": "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8",
        "object_sha256": "7ae86e38c5910bc9ceaa0a4e5cb1f8fbbf1e73de9c0314fedabbd8cb2db3bb7a",
    },
    {
        "path": f"deliverables/{BASE}_schema_v12.json",
        "file_sha256": "5ed911a55e8f90e750fdcaf6ab4fb6c9683bebaf66a4d6250329dff98acb2e28",
    },
    {
        "path": f"deliverables/{BASE}_contract_v12.json",
        "file_sha256": "72246725b15891f92cbc6e3fa1c07ab4a76cdaa19f1b366a736f47f51989b343",
        "object_sha256": "f5c1710817dc8e3aa7fe2bbf4b88e6e39baaa1b17bbeb0f8bf37c8c4575ae5d7",
    },
    {
        "path": f"deliverables/{BASE}_v12.py",
        "file_sha256": "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d",
    },
    {
        "path": (
            f"deliverables/{BASE}_independent_verifier_assembler_"
            "authority_consumer_v12.py"),
        "file_sha256": "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed",
    },
    {
        "path": (
            f"deliverables/{BASE}_v11_to_v12_static_launch_"
            "transition_receipt_v1.json"),
        "file_sha256": "45dabc1ef60eb2f8ba34aa7daa69f9d2b3bedccd4168d9c472bd4bbb696b5400",
        "object_sha256": "0673ecafaa9991cd78e905e144e7c8c1b91717a3d753befa13e82552d44a4072",
    },
    {
        "path": f"deliverables/{BASE}_static_audit_v12.json",
        "file_sha256": "ac29b1e31e0d1b51e8610b7699d1aaf55c80fa6f13f00b20b209c2889e121d37",
        "object_sha256": "c1473ae0f5a08d8772227f61a55bd32c479a7b5c7d40da17b37e796abf4d9783",
    },
    {
        "path": f"deliverables/{BASE}_cold_launch_v12.py",
        "file_sha256": "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba",
    },
    {
        "path": f"deliverables/{BASE}_cold_launch_manifest_v12.sha256",
        "file_sha256": "297e9f58dc7657c6fa959dd45081efffe4e7e8dadcd16ab89457863e2661ece6",
    },
    {
        "path": f"deliverables/{BASE}_cold_launch_outer_receipt_v12.json",
        "file_sha256": "27129990a9d5b6697fd13ee8e2086100cbf158f12e5b767166d771e63088b6d0",
        "object_sha256": "bc6d06141865954590bd11bfc96ad59dbbffa003f568355ecb47155a8a3a809d",
    },
)

V12_OFFICIAL_REJECTION = {
    "path": f".cm2-runtime/c79g-v12-rejections-{CHECKPOINT}/rejection.json",
    "file_sha256": "b6b087a3e31b25f0bbe0ffe6caa40f3c181b2f77c5c8b6169ce3af27439762b5",
    "object_sha256": "18951895ea97f455bc3294e8ef9cdaa937f3b16e9831275b047e88142e9b91f6",
}

FORBIDDEN_V13_STATIC = (
    f"deliverables/{BASE}_schema_v13.json",
    f"deliverables/{BASE}_contract_v13.json",
    f"deliverables/{BASE}_v12_to_v13_static_launch_transition_receipt_v1.json",
    f"deliverables/{BASE}_static_audit_v13.json",
    f"deliverables/{BASE}_cold_launch_manifest_v13.sha256",
    f"deliverables/{BASE}_cold_launch_outer_receipt_v13.json",
)

LIVE_EXACT6_NAMES = (
    "v13_build_only_producer_source",
    "v13_independent_consumer_source",
    "v13_cold_launcher_source",
    "v13_build_only_producer_pyc",
    "v13_independent_consumer_pyc",
    "v13_cold_launcher_pyc",
)
TOOLING_EXACT2_NAMES = (
    "v13_json_draft_builder_tool",
    "v13_independent_static_review_tool",
)

INHERITED_INCIDENT_EXACT10: tuple[dict[str, Any], ...] = (
    {"ordinal": 1, "role": "v10_producer",
     "fd_environment": "CM2_C79G_V13_V10_PRODUCER_FD",
     "path": f"deliverables/{BASE}_v10.py",
     "file_sha256": "99bb321da8a63855e52c8d6757d00886c0deeb2182f5044cac35f645e2ebd00a"},
    {"ordinal": 2, "role": "v9_launcher",
     "fd_environment": "CM2_C79G_V13_V9_LAUNCHER_FD",
     "path": f"deliverables/{BASE}_cold_launch_v9.py",
     "file_sha256": "f7559ceeb7d491b8489812670392cb63e3cd5f6a2764db469e2dd51d6b5577fa"},
    {"ordinal": 3, "role": "v11_producer",
     "fd_environment": "CM2_C79G_V13_V11_PRODUCER_FD",
     "path": f"deliverables/{BASE}_v11.py",
     "file_sha256": "f3b364afc0f5b2f729a3d7786eb8e9c25a9303959d6d2464a40395968090a30b"},
    {"ordinal": 4, "role": "v11_launcher",
     "fd_environment": "CM2_C79G_V13_V11_LAUNCHER_FD",
     "path": f"deliverables/{BASE}_cold_launch_v11.py",
     "file_sha256": "9f6971d2ca3e2c8f448a6aeed70bc16f38154c626f7744a4e20ba723e3082cc2"},
    {"ordinal": 5, "role": "v11_rejection",
     "fd_environment": "CM2_C79G_V13_V11_REJECTION_FD",
     "path": f".cm2-runtime/c79g-v11-rejections-{CHECKPOINT}/rejection.json",
     "file_sha256": "f6cc10d8b7e72553ef0b7a32bbfb99255f36cce16b735002f17be58ae51d3bc8"},
    {"ordinal": 6, "role": "v12_producer",
     "fd_environment": "CM2_C79G_V13_V12_PRODUCER_FD",
     "path": f"deliverables/{BASE}_v12.py",
     "file_sha256": "4cafc594f8a60063b7e7caaa82ddcc2b7983d0fbf0929034cd3cb5f360f3ed1d"},
    {"ordinal": 7, "role": "v12_consumer",
     "fd_environment": "CM2_C79G_V13_V12_CONSUMER_FD",
     "path": (f"deliverables/{BASE}_independent_verifier_assembler_"
              "authority_consumer_v12.py"),
     "file_sha256": "b74dee738257d485e9ca3357d7d138b5175b95e58f1c8ea87d1eca7bfc96b2ed"},
    {"ordinal": 8, "role": "v12_launcher",
     "fd_environment": "CM2_C79G_V13_V12_LAUNCHER_FD",
     "path": f"deliverables/{BASE}_cold_launch_v12.py",
     "file_sha256": "b7aaff67be866f8fd7a01f71e97ea1491574f69e62b7760b6ced9183997444ba"},
    {"ordinal": 9, "role": "v5_rejection",
     "fd_environment": "CM2_C79G_V13_V5_REJECTION_FD",
     "path": f".cm2-runtime/c79g-v5-rejections-{CHECKPOINT}/rejection.json",
     "file_sha256": "c49218967b2d5023d07e5c65fa53df12f0383d6644bf4bd7d35a8e50abeb85b5"},
    {"ordinal": 10, "role": "v12_rejection",
     "fd_environment": "CM2_C79G_V13_V12_REJECTION_FD",
     "path": f".cm2-runtime/c79g-v12-rejections-{CHECKPOINT}/rejection.json",
     "file_sha256": "b6b087a3e31b25f0bbe0ffe6caa40f3c181b2f77c5c8b6169ce3af27439762b5"},
)
INHERITED_INCIDENT_EXACT10_CANONICAL_SHA256 = (
    "600768327003f17f0f367e64b03d0fd9ada23f2933db64845a37cfee140c61b5")
INHERITED_INCIDENT_EXACT10_CANONICAL_BYTE_LENGTH = 2657
V12_V5_INCIDENT_HELPER_NORMALIZED_AST_SHA256 = (
    "fa4cf4f0bdb9e9f1b2a3bdeed7d7271830833395a2f58d32457f363e596fb5e9")
PRODUCER_USE_CHAIN_NORMALIZED_AST_SHA256 = {
    "HeldSelf.__init__":
        "c77800ff63f1a97fdec175f7d4682b5252861b7a603498aaceee08c209a2aca7",
    "HeldSelf.terminal_replay":
        "7478ab0646bd8774d26808f80378f21a44e0eddd16761e9b5f6b5ee301bf436c",
    "ensure_launch_configuration":
        "d144dc70f339ccc0021e6e346176993e7445c0a80c9c236c20b3dc5356b27bf8",
    "build":
        "832f08f822c98ec15370365a850f4cee80540f24ea9d1705af7eebb52c20036a",
    "main":
        "5acb73ffd38e49a16018675b04834610eed53ec008f108d0ef47d3db1e2bdb14",
}
CONSUMER_USE_CHAIN_NORMALIZED_AST_SHA256 = {
    "ensure_configuration":
        "e24e5ef9674952eb49ea9f879bf738c5b62f05e60342dde121fc1dd88798f79a",
    "HeldInheritedIncidentAuthorityExact10.__init__":
        "c5729262fca0cab83bf6937b59814c1b9779fbcdd34b6ff16b3e69ef2aa09368",
    "HeldInheritedIncidentAuthorityExact10._hold_and_validate_v12_predecessor":
        "cc3f4abb1f499fb3e3e1ea7c9f30a3f60a014421fb6c46582b05c6fce7044578",
    "HeldInheritedIncidentAuthorityExact10._require_v12_positive_and_stage_absence":
        "770eb91bffd1fb7b25bf40faa93a91a0f3731965e9a1a0cbbbe2073f334cb4f7",
    "HeldInheritedIncidentAuthorityExact10.terminal_replay":
        "690f88ceb855b668125765adecd8e3eae3b340172b849157cef2e3af2ec3d378",
    "HeldInheritedIncidentAuthorityExact10.close":
        "ac5c051f64f9f4cb3cec3480e3138428477b888c7f3b53271971bd1c6e8ba147",
    "main":
        "1393a7e162befe6a8429c8fdf64d216cd2f79ae9208f61a4202d29f0c23e0bb3",
}
LAUNCHER_USE_CHAIN_NORMALIZED_AST_SHA256 = {
    "HeldBundle.terminal_replay":
        "f2b63815ec103b2f63c78fedcc30334edb519a4cb2be5db23226b889fc5c7e86",
    "HeldV12PredecessorExact10.terminal_replay":
        "34b08990281a6e74a92138896aebb47f945d50a7ab42fd382224cdd583b6924f",
    "HeldV11PredecessorExact10.terminal_replay":
        "a369222de12e38799bd7fbf894242ea512a888d3f4b83245e543a1110ef787cd",
    "HeldSealedChildExec.terminal_replay":
        "571064f3fd73d596a339f6a39609540b711ca0d8f0d123000a632ee29183504d",
    "HeldEmptyRejectionNamespace.terminal_replay":
        "62846981e47d1ecd8d98917f4d3d76f9910972f69c41ceef857b681bf98f3ce5",
    "child_pass_fds":
        "60fb27b80794ec1457d452d05eaa4432a00d9fed7ada510cf27650d048bd2172",
    "run_non_authorize_child":
        "47157daf5116518f4ef7fd62f9fc98e9de428960019970acef8bd109c6ee219b",
    "run_authorize_child":
        "e3b362a5ed77145d907dc80f7e222aa3842f20eadac4e23b3e281e7eebee8230",
}


def strict_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        assert key not in result, f"duplicate JSON key: {key}"
        result[key] = value
    return result


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def verify_object(raw: bytes, expected: str) -> dict[str, Any]:
    value = json.loads(raw, object_pairs_hook=strict_pairs)
    assert isinstance(value, dict)
    assert value.get("object_sha256") == expected
    body = dict(value)
    del body["object_sha256"]
    assert sha256(canonical(body)) == expected
    return value


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    assert "object_sha256" not in body
    result = dict(body)
    result["object_sha256"] = sha256(canonical(body))
    return result


def safe_rel(rel: str) -> None:
    assert rel and not rel.startswith("/")
    assert ".." not in Path(rel).parts


AT_EMPTY_PATH = 0x1000
AT_SYMLINK_NOFOLLOW = 0x100
AT_FDCWD = -100
AT_SYMLINK_FOLLOW = 0x400
STATX_BASIC_STATS = 0x000007ff
STATX_MNT_ID = 0x00001000


class StatxTimestamp(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_int64), ("tv_nsec", ctypes.c_uint32),
        ("reserved", ctypes.c_int32),
    ]


class Statx(ctypes.Structure):
    _fields_ = [
        ("stx_mask", ctypes.c_uint32), ("stx_blksize", ctypes.c_uint32),
        ("stx_attributes", ctypes.c_uint64), ("stx_nlink", ctypes.c_uint32),
        ("stx_uid", ctypes.c_uint32), ("stx_gid", ctypes.c_uint32),
        ("stx_mode", ctypes.c_uint16), ("spare0", ctypes.c_uint16),
        ("stx_ino", ctypes.c_uint64), ("stx_size", ctypes.c_uint64),
        ("stx_blocks", ctypes.c_uint64),
        ("stx_attributes_mask", ctypes.c_uint64),
        ("stx_atime", StatxTimestamp), ("stx_btime", StatxTimestamp),
        ("stx_ctime", StatxTimestamp), ("stx_mtime", StatxTimestamp),
        ("stx_rdev_major", ctypes.c_uint32),
        ("stx_rdev_minor", ctypes.c_uint32),
        ("stx_dev_major", ctypes.c_uint32),
        ("stx_dev_minor", ctypes.c_uint32),
        ("stx_mnt_id", ctypes.c_uint64),
        ("stx_dio_mem_align", ctypes.c_uint32),
        ("stx_dio_offset_align", ctypes.c_uint32),
        ("spare3", ctypes.c_uint64 * 12),
    ]


def fd_mount_id(fd: int) -> int:
    library = ctypes.CDLL(None, use_errno=True)
    assert hasattr(library, "statx")
    info = Statx()
    ctypes.set_errno(0)
    outcome = library.statx(
        ctypes.c_int(fd), ctypes.c_char_p(b""),
        ctypes.c_int(AT_EMPTY_PATH | AT_SYMLINK_NOFOLLOW),
        ctypes.c_uint(STATX_BASIC_STATS | STATX_MNT_ID), ctypes.byref(info))
    assert outcome == 0 and bool(info.stx_mask & STATX_MNT_ID)
    statx_id = int(info.stx_mnt_id)
    rows = [
        line for line in Path(f"/proc/self/fdinfo/{fd}").read_text(
            encoding="ascii").splitlines()
        if line.startswith("mnt_id:\t")]
    assert len(rows) == 1 and int(rows[0].split("\t", 1)[1]) == statx_id
    return statx_id


def stat_identity(value: os.stat_result) -> tuple[int, int]:
    return value.st_dev, value.st_ino


class HeldDirectory:
    def __init__(self, path: Path, parent: "HeldDirectory | None",
                 child_name: str | None):
        self.path = path
        self.parent = parent
        self.child_name = child_name
        if parent is None:
            before = os.lstat(path)
            self.fd = os.open(
                path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW |
                os.O_CLOEXEC | getattr(os, "O_NOATIME", 0))
        else:
            assert child_name is not None and "/" not in child_name
            before = os.stat(
                child_name, dir_fd=parent.fd, follow_symlinks=False)
            self.fd = os.open(
                child_name,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC |
                getattr(os, "O_NOATIME", 0),
                dir_fd=parent.fd)
        try:
            after = os.fstat(self.fd)
            assert stat.S_ISDIR(before.st_mode) and stat.S_ISDIR(after.st_mode)
            assert stat_identity(before) == stat_identity(after)
            self.dev_ino = stat_identity(after)
            self.mount_id = fd_mount_id(self.fd)
        except BaseException:
            os.close(self.fd)
            raise

    def replay(self) -> os.stat_result:
        if self.parent is None:
            path_state = os.lstat(self.path)
        else:
            assert self.child_name is not None
            path_state = os.stat(
                self.child_name, dir_fd=self.parent.fd,
                follow_symlinks=False)
        fd_state = os.fstat(self.fd)
        assert stat.S_ISDIR(path_state.st_mode) and stat.S_ISDIR(fd_state.st_mode)
        assert stat_identity(path_state) == stat_identity(fd_state) == self.dev_ino
        assert fd_mount_id(self.fd) == self.mount_id
        return fd_state

    def close(self) -> None:
        try:
            os.close(self.fd)
        except OSError:
            pass


class HeldDirectories:
    def __init__(self, root: Path):
        created: list[HeldDirectory] = []
        try:
            self.root = HeldDirectory(root, None, None)
            created.append(self.root)
            self.output = HeldDirectory(
                root / "deliverables", self.root, "deliverables")
            created.append(self.output)
            self.runtime = HeldDirectory(
                root / ".cm2-runtime", self.root, ".cm2-runtime")
            created.append(self.runtime)
            self.pycache = HeldDirectory(
                root / "deliverables" / "__pycache__", self.output,
                "__pycache__")
            created.append(self.pycache)
            self.scripts = HeldDirectory(root / "scripts", self.root, "scripts")
            created.append(self.scripts)
            self.ordered = (
                self.root, self.output, self.runtime, self.pycache,
                self.scripts)
            assert len({item.dev_ino for item in self.ordered}) == 5
            assert len({item.replay().st_dev for item in self.ordered}) == 1
            assert len({item.mount_id for item in self.ordered}) == 1
        except BaseException:
            for item in reversed(created):
                item.close()
            raise

    def replay(self) -> None:
        for item in self.ordered:
            item.replay()

    def fsync_all(self) -> None:
        for item in (self.output, self.pycache, self.scripts,
                     self.runtime, self.root):
            os.fsync(item.fd)

    def fsync_receipt_boundaries(self) -> None:
        # The receipt link lives in output; runtime carries the official
        # writer lock, and root is the protocol durability boundary.
        for item in (self.output, self.runtime, self.root):
            os.fsync(item.fd)

    def close(self) -> None:
        for item in reversed(self.ordered):
            item.close()


class Resolver:
    def __init__(self, directories: HeldDirectories):
        self.directories = directories

    def _anchor(self, rel: str) -> tuple[HeldDirectory, tuple[str, ...]]:
        safe_rel(rel)
        parts = Path(rel).parts
        if parts[:2] == ("deliverables", "__pycache__"):
            return self.directories.pycache, tuple(parts[2:])
        if parts[0] == "deliverables":
            return self.directories.output, tuple(parts[1:])
        if parts[0] == "scripts":
            return self.directories.scripts, tuple(parts[1:])
        if parts[0] == ".cm2-runtime":
            return self.directories.runtime, tuple(parts[1:])
        raise AssertionError(f"unanchored path: {rel}")

    def _parent_fd(self, rel: str) -> tuple[int, str, list[int]]:
        anchor, parts = self._anchor(rel)
        assert parts and all(part not in {"", ".", ".."} for part in parts)
        current = anchor.fd
        opened: list[int] = []
        try:
            for part in parts[:-1]:
                before = os.stat(part, dir_fd=current, follow_symlinks=False)
                descriptor = os.open(
                    part,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW |
                    os.O_CLOEXEC | getattr(os, "O_NOATIME", 0),
                    dir_fd=current)
                after = os.fstat(descriptor)
                assert stat.S_ISDIR(before.st_mode) and stat.S_ISDIR(after.st_mode)
                assert stat_identity(before) == stat_identity(after)
                assert fd_mount_id(descriptor) == anchor.mount_id
                opened.append(descriptor)
                current = descriptor
            return current, parts[-1], opened
        except BaseException:
            for descriptor in reversed(opened):
                os.close(descriptor)
            raise

    def stat(self, rel: str) -> os.stat_result:
        parent_fd, name, opened = self._parent_fd(rel)
        try:
            return os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        finally:
            for descriptor in reversed(opened):
                os.close(descriptor)

    def exists(self, rel: str) -> bool:
        try:
            self.stat(rel)
            return True
        except FileNotFoundError:
            return False

    def open_regular(self, rel: str) -> tuple[int, os.stat_result]:
        parent_fd, name, opened = self._parent_fd(rel)
        try:
            before = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            assert stat.S_ISREG(before.st_mode) and not stat.S_ISLNK(before.st_mode)
            descriptor = os.open(
                name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC |
                getattr(os, "O_NOATIME", 0),
                dir_fd=parent_fd)
            try:
                after = os.fstat(descriptor)
                assert Held.identity(before) == Held.identity(after)
                return descriptor, before
            except BaseException:
                os.close(descriptor)
                raise
        finally:
            for intermediate in reversed(opened):
                os.close(intermediate)

    def open_directory(self, rel: str) -> tuple[int, os.stat_result]:
        parent_fd, name, opened = self._parent_fd(rel)
        try:
            before = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            descriptor = os.open(
                name,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC |
                getattr(os, "O_NOATIME", 0),
                dir_fd=parent_fd)
            try:
                after = os.fstat(descriptor)
                assert stat.S_ISDIR(before.st_mode) and stat.S_ISDIR(after.st_mode)
                assert stat_identity(before) == stat_identity(after)
                return descriptor, before
            except BaseException:
                os.close(descriptor)
                raise
        finally:
            for intermediate in reversed(opened):
                os.close(intermediate)

    def replay_file(self, rel: str, descriptor: int) -> os.stat_result:
        path_state = self.stat(rel)
        fd_state = os.fstat(descriptor)
        assert Held.identity(path_state) == Held.identity(fd_state)
        return fd_state


class Held:
    def __init__(self, resolver: Resolver, pin: dict[str, Any], modes: set[int]):
        self.resolver = resolver
        self.pin = dict(pin)
        self.rel = self.pin["path"]
        safe_rel(self.rel)
        self.fd, path_state = resolver.open_regular(self.rel)
        try:
            self.initial = os.fstat(self.fd)
            assert self.identity(path_state) == self.identity(self.initial)
            assert self.initial.st_nlink == 1
            assert stat.S_IMODE(self.initial.st_mode) in modes
            if "size" in self.pin:
                assert self.initial.st_size == self.pin["size"]
                assert self.initial.st_mtime_ns == self.pin["mtime_ns"]
                if stat.S_IMODE(self.initial.st_mode) == 0o664:
                    assert self.initial.st_ctime_ns == self.pin["ctime_ns"]
                else:
                    assert stat.S_IMODE(self.initial.st_mode) == 0o444
                    assert self.initial.st_ctime_ns >= self.pin["ctime_ns"]
            raw = self.read()
            assert sha256(raw) == self.pin["file_sha256"]
            object_sha = self.pin.get("object_sha256")
            if object_sha is not None:
                verify_object(raw, object_sha)
        except BaseException:
            os.close(self.fd)
            raise

    @staticmethod
    def identity(value: os.stat_result) -> tuple[int, int, int, int, int, int]:
        return (value.st_dev, value.st_ino, value.st_size, value.st_nlink,
                value.st_mtime_ns, value.st_ctime_ns)

    def read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while True:
            block = os.read(self.fd, 1 << 20)
            if not block:
                return b"".join(chunks)
            chunks.append(block)

    def freeze(self) -> os.stat_result:
        before = os.fstat(self.fd)
        mode = stat.S_IMODE(before.st_mode)
        assert mode in {0o444, 0o664}
        if mode == 0o664:
            os.fchmod(self.fd, 0o444)
        # A recovered 0444 prefix may reflect interruption after fchmod but
        # before the first successful file fsync.  Always fsync the held file;
        # never repeat fchmod on the frozen prefix.
        os.fsync(self.fd)
        return self.replay(require_frozen=True)[0]

    def replay(self, require_frozen: bool) -> tuple[os.stat_result, bytes]:
        fd_state = self.resolver.replay_file(self.rel, self.fd)
        assert stat.S_ISREG(fd_state.st_mode)
        assert fd_state.st_nlink == 1
        expected_mode = 0o444 if require_frozen else 0o664
        assert stat.S_IMODE(fd_state.st_mode) == expected_mode
        assert fd_state.st_size == self.pin.get("size", fd_state.st_size)
        assert fd_state.st_mtime_ns == self.pin.get("mtime_ns", fd_state.st_mtime_ns)
        raw = self.read()
        assert sha256(raw) == self.pin["file_sha256"]
        object_sha = self.pin.get("object_sha256")
        if object_sha is not None:
            verify_object(raw, object_sha)
        return fd_state, raw

    def close(self) -> None:
        try:
            os.close(self.fd)
        except OSError:
            pass


def read_all(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        block = os.read(descriptor, 1 << 20)
        if not block:
            return b"".join(chunks)
        chunks.append(block)


def write_all(descriptor: int, raw: bytes) -> None:
    offset = 0
    while offset < len(raw):
        count = os.write(descriptor, raw[offset:])
        assert count > 0
        offset += count


def linkat_path_raw(old_path: str, new_dir_fd: int,
                    new_name: str) -> tuple[int, int]:
    assert old_path.startswith("/proc/self/fd/")
    assert new_name and "/" not in new_name
    library = ctypes.CDLL(None, use_errno=True)
    assert hasattr(library, "linkat")
    ctypes.set_errno(0)
    outcome = library.linkat(
        ctypes.c_int(AT_FDCWD), ctypes.c_char_p(os.fsencode(old_path)),
        ctypes.c_int(new_dir_fd), ctypes.c_char_p(os.fsencode(new_name)),
        ctypes.c_int(AT_SYMLINK_FOLLOW))
    return int(outcome), int(ctypes.get_errno())


def proc_fd_path(descriptor: int) -> str:
    assert descriptor >= 0
    return f"/proc/self/fd/{descriptor}"


def verify_proc_fd_otmpfile_route(descriptor: int,
                                  output: HeldDirectory) -> None:
    path = proc_fd_path(descriptor)
    target = os.readlink(path)
    expected_prefix = str(ROOT_EXPECTED / "deliverables") + "/#"
    assert target.startswith(expected_prefix) and target.endswith(" (deleted)"), target
    route_fd = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOATIME", 0))
    try:
        original = os.fstat(descriptor)
        routed = os.fstat(route_fd)
        assert Held.identity(original) == Held.identity(routed)
        assert original.st_nlink == routed.st_nlink == 0
        assert fd_mount_id(descriptor) == fd_mount_id(route_fd) == output.mount_id
    finally:
        os.close(route_fd)


def linkat_proc_fd_no_replace(old_fd: int, output: HeldDirectory,
                               new_name: str) -> None:
    verify_proc_fd_otmpfile_route(old_fd, output)
    outcome, error = linkat_path_raw(
        proc_fd_path(old_fd), output.fd, new_name)
    assert outcome == 0, ("unprivileged proc-fd linkat failed", error)


def verify_otmpfile_linkat_capability(resolver: Resolver) -> None:
    """Probe anonymous publication without ever adding a directory entry."""
    output = resolver.directories.output
    descriptor = os.open(
        ".", os.O_RDWR | os.O_TMPFILE | os.O_CLOEXEC, 0o600,
        dir_fd=output.fd)
    try:
        marker = b"C79G_V13_O_TMPFILE_LINKAT_CAPABILITY_PROBE\n"
        write_all(descriptor, marker)
        os.fchmod(descriptor, 0o444)
        os.fsync(descriptor)
        state = os.fstat(descriptor)
        assert stat.S_ISREG(state.st_mode)
        assert stat.S_IMODE(state.st_mode) == 0o444
        assert state.st_nlink == 0 and read_all(descriptor) == marker
        verify_proc_fd_otmpfile_route(descriptor, output)
        # Prove source resolution happens before the destination EEXIST
        # result.  The invalid proc-fd source must fail ENOENT, while the
        # valid anonymous inode route reaches the immutable "." destination.
        invalid_fd = 1 << 30
        try:
            os.fstat(invalid_fd)
        except OSError as error_value:
            assert error_value.errno == errno.EBADF
        else:
            raise AssertionError("chosen invalid fd unexpectedly exists")
        outcome, error = linkat_path_raw(
            proc_fd_path(invalid_fd), output.fd, ".")
        assert outcome == -1 and error == errno.ENOENT, (outcome, error)
        outcome, error = linkat_path_raw(
            proc_fd_path(descriptor), output.fd, ".")
        assert outcome == -1 and error == errno.EEXIST, (outcome, error)
        assert os.fstat(descriptor).st_nlink == 0
        resolver.directories.replay()
    finally:
        os.close(descriptor)


class HeldReceipt:
    def __init__(self, resolver: Resolver, descriptor: int, raw: bytes,
                 object_sha: str):
        self.resolver = resolver
        self.rel = RECEIPT_REL
        self.fd = descriptor
        self.file_sha = sha256(raw)
        self.object_sha = object_sha
        self.initial = os.fstat(self.fd)

    @classmethod
    def open_existing(cls, resolver: Resolver, raw: bytes,
                      object_sha: str) -> "HeldReceipt":
        descriptor, _path_state = resolver.open_regular(RECEIPT_REL)
        self = cls(resolver, descriptor, raw, object_sha)
        try:
            _state, actual = self.replay()
            assert actual == raw
            return self
        except BaseException:
            self.close()
            raise

    @classmethod
    def publish_anonymous(cls, resolver: Resolver, raw: bytes,
                          object_sha: str,
                          frozen_max_ns: int) -> "HeldReceipt":
        output = resolver.directories.output
        assert not resolver.exists(RECEIPT_REL)
        descriptor = os.open(
            ".", os.O_RDWR | os.O_TMPFILE | os.O_CLOEXEC, 0o600,
            dir_fd=output.fd)
        linked = False
        try:
            write_all(descriptor, raw)
            os.fchmod(descriptor, 0o444)
            os.fsync(descriptor)
            anonymous_state = os.fstat(descriptor)
            assert stat.S_ISREG(anonymous_state.st_mode)
            assert stat.S_IMODE(anonymous_state.st_mode) == 0o444
            assert anonymous_state.st_nlink == 0 and anonymous_state.st_size == len(raw)
            assert frozen_max_ns < min(
                anonymous_state.st_mtime_ns, anonymous_state.st_ctime_ns)
            assert read_all(descriptor) == raw
            verify_object(raw, object_sha)
            verify_proc_fd_otmpfile_route(descriptor, output)
            linkat_proc_fd_no_replace(
                descriptor, output, Path(RECEIPT_REL).name)
            linked = True
            os.fsync(output.fd)
            self = cls(resolver, descriptor, raw, object_sha)
            state, actual = self.replay()
            assert actual == raw and state.st_nlink == 1
            return self
        except BaseException:
            os.close(descriptor)
            # A successful link is append-only evidence; never unlink it.
            # The next invocation may only accept it through exact recovery.
            _ = linked
            raise

    def read(self) -> bytes:
        return read_all(self.fd)

    def replay(self) -> tuple[os.stat_result, bytes]:
        fd_state = self.resolver.replay_file(self.rel, self.fd)
        assert stat.S_ISREG(fd_state.st_mode)
        assert stat.S_IMODE(fd_state.st_mode) == 0o444 and fd_state.st_nlink == 1
        assert full_file_identity(fd_state) == full_file_identity(self.initial)
        assert fd_mount_id(self.fd) == self.resolver.directories.output.mount_id
        raw = self.read()
        assert sha256(raw) == self.file_sha
        verify_object(raw, self.object_sha)
        return fd_state, raw

    def close(self) -> None:
        try:
            os.close(self.fd)
        except OSError:
            pass


def module_constants(raw: bytes, rel: str) -> tuple[ast.Module, dict[str, Any]]:
    source = raw.decode("utf-8")
    tree = ast.parse(source, filename=rel, mode="exec")
    compile(tree, rel, "exec", dont_inherit=True, optimize=0)
    values: dict[str, Any] = {}
    seen: set[str] = set()
    for node in tree.body:
        pairs: list[tuple[str, ast.expr]] = []
        if isinstance(node, ast.Assign):
            pairs = [(target.id, node.value) for target in node.targets
                     if isinstance(target, ast.Name)]
        elif (isinstance(node, ast.AnnAssign) and
              isinstance(node.target, ast.Name) and node.value is not None):
            pairs = [(node.target.id, node.value)]
        for name, value_node in pairs:
            assert name not in seen, (rel, "duplicate module assignment", name)
            seen.add(name)
            try:
                values[name] = ast.literal_eval(value_node)
            except (ValueError, TypeError):
                pass
    return tree, values


def direct_assignment_nodes(
        statements: list[ast.stmt]) -> dict[str, list[ast.expr]]:
    result: dict[str, list[ast.expr]] = {}
    for node in statements:
        pairs: list[tuple[str, ast.expr]] = []
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    pairs.append((target.id, node.value))
        elif (isinstance(node, ast.AnnAssign) and
              isinstance(node.target, ast.Name) and node.value is not None):
            pairs.append((node.target.id, node.value))
        for name, value in pairs:
            result.setdefault(name, []).append(value)
    return result


def unique_direct_assignment(
        assignments: dict[str, list[ast.expr]], name: str) -> ast.expr:
    matches = assignments.get(name, [])
    assert len(matches) == 1, (name, len(matches))
    return matches[0]


def unique_top_function(tree: ast.Module, name: str) -> ast.FunctionDef:
    matches = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name]
    assert len(matches) == 1, (name, len(matches))
    return matches[0]


def unique_class(tree: ast.Module, name: str) -> ast.ClassDef:
    matches = [
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == name]
    assert len(matches) == 1, (name, len(matches))
    return matches[0]


def unique_method(node: ast.ClassDef, name: str) -> ast.FunctionDef:
    matches = [
        child for child in node.body
        if isinstance(child, ast.FunctionDef) and child.name == name]
    assert len(matches) == 1, (node.name, name, len(matches))
    return matches[0]


def expression_ast_key(node: ast.AST) -> str:
    return ast.dump(node, annotate_fields=True, include_attributes=False)


def parsed_expression_ast_key(source: str) -> str:
    return expression_ast_key(ast.parse(source, mode="eval").body)


def normalized_ast_sha256(node: ast.AST) -> str:
    return sha256(expression_ast_key(node).encode("utf-8"))


def ast_expression_matches(node: ast.AST, source: str) -> list[ast.AST]:
    expected = parsed_expression_ast_key(source)
    return [child for child in ast.walk(node)
            if expression_ast_key(child) == expected]


def assert_expression_count(node: ast.AST, source: str, count: int = 1) -> None:
    matches = ast_expression_matches(node, source)
    assert len(matches) == count, (source, len(matches), count)


def assert_normalized_ast_pin(node: ast.AST, expected: str, label: str) -> None:
    assert normalized_ast_sha256(node) == expected, label


def ast_target_shape(node: ast.AST) -> Any:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, (ast.Tuple, ast.List)):
        return tuple(ast_target_shape(item) for item in node.elts)
    if isinstance(node, ast.Subscript):
        return ("SUBSCRIPT", expression_ast_key(node.value),
                expression_ast_key(node.slice))
    raise AssertionError(("unexpected assignment target", expression_ast_key(node)))


class StaticAstResolver:
    """Evaluate only inert literal/path-building AST used by the three sources."""

    def __init__(self, assignments: dict[str, list[ast.expr]],
                 seeds: dict[str, Any]):
        self.assignments = assignments
        self.seeds = dict(seeds)
        self.cache: dict[str, Any] = {}
        self.active: set[str] = set()

    @staticmethod
    def path_join(left: str, right: str) -> str:
        assert isinstance(left, str) and isinstance(right, str)
        if not left:
            return right.lstrip("/")
        return left.rstrip("/") + "/" + right.lstrip("/")

    def named(self, name: str) -> Any:
        if name in self.seeds:
            return self.seeds[name]
        if name in self.cache:
            return self.cache[name]
        assert name not in self.active, ("static AST name cycle", name)
        self.active.add(name)
        try:
            value = self.expression(unique_direct_assignment(
                self.assignments, name))
            self.cache[name] = value
            return value
        finally:
            self.active.remove(name)

    def expression(self, node: ast.AST) -> Any:
        if isinstance(node, ast.Constant):
            assert type(node.value) in {str, int, bool, type(None)}
            return node.value
        if isinstance(node, ast.Name):
            return self.named(node.id)
        if isinstance(node, ast.Tuple):
            return tuple(self.expression(item) for item in node.elts)
        if isinstance(node, ast.List):
            return [self.expression(item) for item in node.elts]
        if isinstance(node, ast.Dict):
            assert all(key is not None for key in node.keys)
            keys = [self.expression(key) for key in node.keys if key is not None]
            assert len(keys) == len(set(keys))
            return {
                key: self.expression(value)
                for key, value in zip(keys, node.values, strict=True)}
        if isinstance(node, ast.Subscript):
            key = self.expression(node.slice)
            # A selected field of a closed module-level literal dict must not
            # force evaluation of unrelated values.  In particular, the v12
            # incident object has one diagnostic ``sorted(...)`` value which
            # is deliberately outside this resolver's no-Call language.  The
            # selected source-hash fields remain independently extractable by
            # exact literal key, while duplicate, missing, or computed keys
            # fail closed.
            if isinstance(node.value, ast.Name):
                assignment = unique_direct_assignment(
                    self.assignments, node.value.id)
                if isinstance(assignment, ast.Dict):
                    assert all(isinstance(item, ast.Constant)
                               for item in assignment.keys)
                    literal_keys = [
                        item.value for item in assignment.keys
                        if isinstance(item, ast.Constant)]
                    assert all(type(item) in {str, int} for item in literal_keys)
                    assert len(literal_keys) == len(assignment.values)
                    assert len(literal_keys) == len(set(literal_keys))
                    assert key in literal_keys, (node.value.id, key)
                    index = literal_keys.index(key)
                    return self.expression(assignment.values[index])
            container = self.expression(node.value)
            assert isinstance(container, (tuple, list, dict))
            return container[key]
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left, right = self.expression(node.left), self.expression(node.right)
            assert isinstance(left, str) and isinstance(right, str)
            return left + right
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            left, right = self.expression(node.left), self.expression(node.right)
            return self.path_join(left, right)
        if isinstance(node, ast.JoinedStr):
            parts: list[str] = []
            for value in node.values:
                if isinstance(value, ast.Constant):
                    assert isinstance(value.value, str)
                    parts.append(value.value)
                else:
                    assert isinstance(value, ast.FormattedValue)
                    resolved = self.expression(value.value)
                    assert isinstance(resolved, (str, int))
                    assert value.conversion == -1 and value.format_spec is None
                    parts.append(str(resolved))
            return "".join(parts)
        raise AssertionError(("forbidden static AST expression", type(node).__name__,
                              expression_ast_key(node)))


def module_and_local_resolver(
        tree: ast.Module, local_statements: list[ast.stmt] | None = None
        ) -> StaticAstResolver:
    assignments = direct_assignment_nodes(tree.body)
    if local_statements is not None:
        local = direct_assignment_nodes(local_statements)
        assignments = dict(assignments)
        assignments.update(local)
    return StaticAstResolver(assignments, {
        "ROOT": "",
        "OUT": "deliverables",
        "RUNTIME": ".cm2-runtime",
    })


def normalize_incident_path(value: Any) -> str:
    assert isinstance(value, str)
    root_prefix = str(ROOT_EXPECTED).rstrip("/") + "/"
    if value.startswith(root_prefix):
        value = value[len(root_prefix):]
    value = value.lstrip("./") if value.startswith("./") else value
    safe_rel(value)
    assert value.startswith(("deliverables/", ".cm2-runtime/")), value
    return value


def expected_inherited_incident_table() -> list[dict[str, Any]]:
    result = [dict(row) for row in INHERITED_INCIDENT_EXACT10]
    exact_keys = {"ordinal", "role", "fd_environment", "path", "file_sha256"}
    assert len(result) == 10
    assert [row["ordinal"] for row in result] == list(range(1, 11))
    assert all(set(row) == exact_keys for row in result)
    assert len({row["role"] for row in result}) == 10
    assert len({row["fd_environment"] for row in result}) == 10
    assert len({row["path"] for row in result}) == 10
    assert all(re.fullmatch(r"[0-9a-f]{64}", row["file_sha256"])
               for row in result)
    raw = canonical(result)
    assert len(raw) == INHERITED_INCIDENT_EXACT10_CANONICAL_BYTE_LENGTH
    assert sha256(raw) == INHERITED_INCIDENT_EXACT10_CANONICAL_SHA256
    return result


def normalized_rows_from_triples(
        triples: list[tuple[Any, Any, Any]]) -> list[dict[str, Any]]:
    expected = expected_inherited_incident_table()
    assert len(triples) == 10
    result: list[dict[str, Any]] = []
    for expected_row, triple in zip(expected, triples, strict=True):
        assert isinstance(triple, tuple) and len(triple) == 3
        env_name, path, file_sha = triple
        row = {
            "ordinal": expected_row["ordinal"],
            "role": expected_row["role"],
            "fd_environment": env_name,
            "path": normalize_incident_path(path),
            "file_sha256": file_sha,
        }
        assert row == expected_row
        result.append(row)
    assert canonical(result) == canonical(expected)
    return result


def normalized_incident_helper_ast(tree: ast.Module) -> tuple[str, int]:
    helper = unique_top_function(tree, "derive_v12_v5_rejection_shape_incident")
    normalized = expression_ast_key(helper).encode("utf-8")
    digest = sha256(normalized)
    assert digest == V12_V5_INCIDENT_HELPER_NORMALIZED_AST_SHA256
    return digest, 1


def consumer_inherited_incident_extraction(
        tree: ast.Module) -> tuple[list[dict[str, Any]], bytes, str]:
    assignments = direct_assignment_nodes(tree.body)
    literal = unique_direct_assignment(
        assignments, "INCIDENT_AUTHORITY_INHERITED_EXACT10")
    resolved = module_and_local_resolver(tree).expression(literal)
    assert isinstance(resolved, tuple)
    rows = normalized_rows_from_triples(list(resolved))

    ensure = unique_top_function(tree, "ensure_configuration")
    ensure_assignments = direct_assignment_nodes(ensure.body)
    assert expression_ast_key(unique_direct_assignment(
        ensure_assignments, "incident_fd_texts")) == parsed_expression_ast_key(
            "tuple(os.environ.get(env_name, '') for env_name, _, _ in "
            "INCIDENT_AUTHORITY_INHERITED_EXACT10)")
    assert expression_ast_key(unique_direct_assignment(
        ensure_assignments, "all_fd_texts")) == parsed_expression_ast_key(
            "(exec_fd_text, source_fd_text, coordination_fd_text, root_fd_text, "
            "*incident_fd_texts)")
    assert_expression_count(
        ensure,
        "len(all_fd_texts) == len({int(value) for value in all_fd_texts}) == 14")
    assert expression_ast_key(one_direct_return(ensure).value) == \
        parsed_expression_ast_key("root_guard")
    assert_normalized_ast_pin(
        ensure, CONSUMER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "ensure_configuration"], "consumer ensure_configuration AST")

    holder_class = unique_class(tree, "HeldInheritedIncidentAuthorityExact10")
    constructor = unique_method(holder_class, "__init__")
    hold_v12 = unique_method(
        holder_class, "_hold_and_validate_v12_predecessor")
    absence = unique_method(
        holder_class, "_require_v12_positive_and_stage_absence")
    terminal = unique_method(holder_class, "terminal_replay")
    close = unique_method(holder_class, "close")
    assert_normalized_ast_pin(
        constructor, CONSUMER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "HeldInheritedIncidentAuthorityExact10.__init__"],
        "consumer incident holder constructor AST")
    assert_normalized_ast_pin(
        hold_v12, CONSUMER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "HeldInheritedIncidentAuthorityExact10._hold_and_validate_v12_predecessor"],
        "consumer held v12 exact10 method AST")
    assert_normalized_ast_pin(
        absence, CONSUMER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "HeldInheritedIncidentAuthorityExact10._require_v12_positive_and_stage_absence"],
        "consumer inherited positive/stage absence AST")
    assert_normalized_ast_pin(
        terminal, CONSUMER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "HeldInheritedIncidentAuthorityExact10.terminal_replay"],
        "consumer incident holder terminal AST")
    assert_normalized_ast_pin(
        close, CONSUMER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "HeldInheritedIncidentAuthorityExact10.close"],
        "consumer incident holder close AST")

    inherited_loops = [
        node for node in ast.walk(constructor) if isinstance(node, ast.For) and
        ast_target_shape(node.target) == ("env_name", "path", "file_pin") and
        expression_ast_key(node.iter) == parsed_expression_ast_key(
            "INCIDENT_AUTHORITY_INHERITED_EXACT10")]
    assert len(inherited_loops) == 1
    inherited_loop = inherited_loops[0]
    for source in (
        "os.environ.get(env_name)",
        "int(text)",
        "os.dup(inherited_fd)",
        "(inherited_before.st_dev, inherited_before.st_ino) == "
        "(before.st_dev, before.st_ino) == "
        "(path_before.st_dev, path_before.st_ino)",
        "inherited_mount_id == mount_id",
        "sha(raw) == file_pin",
        "fingerprint(inherited_before) == fingerprint(before) == "
        "fingerprint(path_before) == fingerprint(after) == "
        "fingerprint(path_after)",
        "statx_mount_id(descriptor) == mount_id",
    ):
        assert_expression_count(inherited_loop, source)
    assert_expression_count(
        constructor,
        "len(self.files) == len(identities) == 10 and len(mount_ids) == 1")
    assert_expression_count(
        constructor,
        "derive_v12_v5_rejection_shape_incident("
        "by_env[V12_PRODUCER_FD_ENV].raw, by_env[V12_CONSUMER_FD_ENV].raw, "
        "by_env[V12_LAUNCHER_FD_ENV].raw, by_env[V5_REJECTION_FD_ENV].raw, "
        "by_env[V12_REJECTION_FD_ENV].raw)")
    assert_expression_count(
        constructor, "self._hold_and_validate_v12_predecessor()")

    assert_expression_count(
        hold_v12, "len(member_by_path) == len(self.v12_members) == 6")
    assert_expression_count(
        hold_v12,
        "set(raw_by_path) == {path for path, _ in V12_FROZEN_FILES.values()} "
        "and len(raw_by_path) == len(set(identity_by_path.values())) == 10 "
        "and len(set(mount_by_path.values())) == 1 and "
        "tuple(V12_FROZEN_FILES[name][1] for name in V12_EXACT10_ORDER) == "
        "V12_PUBLISHED_EXACT10_FILE_SHA256_ORDER")
    v12_order_loops = [
        node for node in ast.walk(hold_v12) if isinstance(node, ast.For) and
        ast_target_shape(node.target) == "name" and
        expression_ast_key(node.iter) == parsed_expression_ast_key(
            "V12_EXACT10_ORDER")]
    assert len(v12_order_loops) == 1
    assert_expression_count(v12_order_loops[0], "sha_bytes(raw) == file_pin")

    terminal_file_loops = [
        node for node in ast.walk(terminal) if isinstance(node, ast.For) and
        ast_target_shape(node.target) == "item" and
        expression_ast_key(node.iter) == parsed_expression_ast_key("self.files")]
    terminal_v12_loops = [
        node for node in ast.walk(terminal) if isinstance(node, ast.For) and
        ast_target_shape(node.target) == "item" and
        expression_ast_key(node.iter) == parsed_expression_ast_key(
            "self.v12_members")]
    assert len(terminal_file_loops) == len(terminal_v12_loops) == 1
    for source in (
        "raw == item.raw", "sha(raw) == item.file_sha256",
        "fingerprint(before) == fingerprint(path_before) == "
        "fingerprint(after) == fingerprint(path_after) == "
        "fingerprint(item.before)",
        "statx_mount_id(descriptor) == item.mount_id",
    ):
        assert_expression_count(terminal_file_loops[0], source)
    assert_expression_count(terminal_v12_loops[0], "item.terminal_replay()")
    assert_expression_count(
        terminal, "self.v11_rejection_namespace.terminal_replay()")
    assert_expression_count(
        terminal, "self._require_v12_positive_and_stage_absence()")
    assert_expression_count(
        terminal,
        "derive_v12_v5_rejection_shape_incident("
        "self.by_env[V12_PRODUCER_FD_ENV].raw, "
        "self.by_env[V12_CONSUMER_FD_ENV].raw, "
        "self.by_env[V12_LAUNCHER_FD_ENV].raw, "
        "self.by_env[V5_REJECTION_FD_ENV].raw, "
        "self.by_env[V12_REJECTION_FD_ENV].raw)")
    assert_expression_count(
        terminal,
        "derive_v10_colon_prefix_witness("
        "self.by_env[V10_PRODUCER_FD_ENV].raw, "
        "self.by_env[V9_LAUNCHER_FD_ENV].raw)")

    main_function = unique_top_function(tree, "main")
    assert_normalized_ast_pin(
        main_function, CONSUMER_USE_CHAIN_NORMALIZED_AST_SHA256["main"],
        "consumer main AST")
    assert_expression_count(
        main_function, "HeldInheritedIncidentAuthorityExact10()")
    assert_expression_count(main_function, "incident_guard.terminal_replay()")
    assert_expression_count(main_function, "guard.close()")
    close_loops = [
        node for node in ast.walk(main_function) if isinstance(node, ast.For) and
        ast_target_shape(node.target) == "guard" and
        expression_ast_key(node.iter) == parsed_expression_ast_key(
            "(fixed_guard, c78_guard, runtime_parent, producer_guard, "
            "incident_guard, self_guard, workspace_root_guard)")]
    assert len(close_loops) == 1
    assert_expression_count(close_loops[0], "guard.close()")

    representation = b"\0".join([
        expression_ast_key(literal).encode("utf-8"),
        expression_ast_key(ensure).encode("utf-8"),
        expression_ast_key(constructor).encode("utf-8"),
        expression_ast_key(hold_v12).encode("utf-8"),
        expression_ast_key(absence).encode("utf-8"),
        expression_ast_key(terminal).encode("utf-8"),
        expression_ast_key(close).encode("utf-8"),
        expression_ast_key(main_function).encode("utf-8"),
    ])
    return rows, representation, (
        "MODULE_EXACT10_PLUS_CONFIGURATION_HOLDER_TERMINAL_CLOSE_MAIN_USE_CHAIN")


def environment_get_symbol(node: ast.AST) -> str:
    assert isinstance(node, ast.Call)
    assert expression_ast_key(node.func) == parsed_expression_ast_key(
        "os.environ.get")
    assert len(node.args) == 2 and not node.keywords
    assert isinstance(node.args[0], ast.Name)
    assert isinstance(node.args[1], ast.Constant) and node.args[1].value == ""
    return node.args[0].id


def producer_inherited_incident_extraction(
        tree: ast.Module) -> tuple[list[dict[str, Any]], bytes, str]:
    held_self = unique_class(tree, "HeldSelf")
    constructor = unique_method(held_self, "__init__")
    terminal = unique_method(held_self, "terminal_replay")
    assert [argument.arg for argument in constructor.args.args] == [
        "self", "exec_inherited", "source_inherited",
        "coordination_inherited", "root_inherited", "incident_inherited"]
    assert_normalized_ast_pin(
        constructor, PRODUCER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "HeldSelf.__init__"], "producer HeldSelf constructor AST")
    assert_normalized_ast_pin(
        terminal, PRODUCER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "HeldSelf.terminal_replay"], "producer HeldSelf terminal AST")
    constructor_assignments = direct_assignment_nodes(constructor.body)
    expected_pins_node = unique_direct_assignment(
        constructor_assignments, "expected_incident_pins")
    resolver = module_and_local_resolver(tree)
    expected_pins = resolver.expression(expected_pins_node)
    assert isinstance(expected_pins, dict) and len(expected_pins) == 10
    assert_expression_count(
        constructor,
        "set(incident_inherited) == set(expected_incident_pins)")
    assert_expression_count(constructor, "os.dup(inherited_fd)")
    assert_expression_count(
        constructor,
        "len({(value.st_dev, value.st_ino) for value in "
        "self.incident_before.values()}) == 10")
    assert_expression_count(
        constructor,
        "{path: self._read_fd(descriptor) for path, descriptor in "
        "self.incident_fds.items()}")
    assert_expression_count(
        constructor,
        "all(file_fingerprint(os.fstat(self.incident_fds[path])) == "
        "file_fingerprint(self.incident_before[path]) and "
        "statx_mount_id(self.incident_fds[path]) == "
        "self.incident_mount_ids[path] and "
        "sha_bytes(self.incident_raw[path]) == expected_incident_pins[path] "
        "for path in expected_incident_pins)")
    assert_expression_count(
        constructor,
        "file_fingerprint(path_before) == "
        "file_fingerprint(self.incident_before[path])")

    incident_loops = [
        node for node in ast.walk(constructor) if isinstance(node, ast.For) and
        ast_target_shape(node.target) == ("path", "inherited_fd") and
        expression_ast_key(node.iter) == parsed_expression_ast_key(
            "incident_inherited.items()")]
    descriptor_loops = [
        node for node in ast.walk(constructor) if isinstance(node, ast.For) and
        ast_target_shape(node.target) == ("path", "descriptor") and
        expression_ast_key(node.iter) == parsed_expression_ast_key(
            "self.incident_fds.items()")]
    path_loops = [
        node for node in ast.walk(constructor) if isinstance(node, ast.For) and
        ast_target_shape(node.target) == "path" and
        expression_ast_key(node.iter) == parsed_expression_ast_key(
            "expected_incident_pins")]
    assert len(incident_loops) == len(descriptor_loops) == len(path_loops) == 1

    def exact_assignment_count(scope: ast.AST, target_source: str,
                               value_source: str) -> int:
        expected_target = ast.parse(target_source + " = None").body[0]
        assert isinstance(expected_target, ast.Assign)
        target_shape = ast_target_shape(expected_target.targets[0])
        expected_value = parsed_expression_ast_key(value_source)
        return sum(
            len(node.targets) == 1 and
            ast_target_shape(node.targets[0]) == target_shape and
            expression_ast_key(node.value) == expected_value
            for node in ast.walk(scope) if isinstance(node, ast.Assign))

    assert exact_assignment_count(
        incident_loops[0], "self.incident_fds[path]",
        "os.dup(inherited_fd)") == 1
    assert exact_assignment_count(
        descriptor_loops[0], "self.incident_before[path]",
        "os.fstat(descriptor)") == 1
    assert exact_assignment_count(
        descriptor_loops[0], "self.incident_mount_ids[path]",
        "statx_mount_id(descriptor)") == 1
    assert exact_assignment_count(
        path_loops[0], "self.incident_path_before[path]", "path_before") == 1

    incident_derive = (
        "derive_v12_v5_rejection_shape_incident("
        "self.incident_raw[V12_FROZEN_PRODUCER], "
        "self.incident_raw[V12_FROZEN_CONSUMER], "
        "self.incident_raw[V12_FROZEN_LAUNCHER], "
        "self.incident_raw[V5_OFFICIAL_REJECTION], "
        "self.incident_raw[V12_OFFICIAL_REJECTION])")
    assert_expression_count(constructor, incident_derive)
    assert_expression_count(terminal, incident_derive)
    assert_expression_count(
        terminal,
        "all(self._read_fd(self.incident_fds[path]) == "
        "self.incident_raw[path] and "
        "file_fingerprint(os.fstat(self.incident_fds[path])) == "
        "file_fingerprint(self.incident_before[path]) == "
        "file_fingerprint(path.lstat()) and "
        "statx_mount_id(self.incident_fds[path]) == "
        "self.incident_mount_ids[path] for path in self.incident_fds)")

    launch = unique_top_function(tree, "ensure_launch_configuration")
    launch_assignments = direct_assignment_nodes(launch.body)
    roles = expected_inherited_incident_table()
    fd_variables = (
        "v10_producer_fd_text", "v9_launcher_fd_text",
        "v11_producer_fd_text", "v11_launcher_fd_text",
        "v11_rejection_fd_text", "v12_producer_fd_text",
        "v12_consumer_fd_text", "v12_launcher_fd_text",
        "v5_rejection_fd_text", "v12_rejection_fd_text",
    )
    env_symbols = (
        "V10_PRODUCER_FD_ENV", "V9_LAUNCHER_FD_ENV",
        "V11_PRODUCER_FD_ENV", "V11_LAUNCHER_FD_ENV",
        "V11_REJECTION_FD_ENV", "V12_PRODUCER_FD_ENV",
        "V12_CONSUMER_FD_ENV", "V12_LAUNCHER_FD_ENV",
        "V5_REJECTION_FD_ENV", "V12_REJECTION_FD_ENV",
    )
    env_assignment_nodes: list[ast.expr] = []
    for variable, env_symbol, expected_row in zip(
            fd_variables, env_symbols, roles, strict=True):
        node = unique_direct_assignment(launch_assignments, variable)
        env_assignment_nodes.append(node)
        assert environment_get_symbol(node) == env_symbol
        assert resolver.named(env_symbol) == expected_row["fd_environment"]

    held_self_calls = [
        node for node in ast.walk(launch)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and
        node.func.id == "HeldSelf"]
    assert len(held_self_calls) == 1
    call = held_self_calls[0]
    assert len(call.args) == 5 and not call.keywords
    incident_fd_dict = call.args[4]
    assert isinstance(incident_fd_dict, ast.Dict)
    assert len(incident_fd_dict.keys) == len(incident_fd_dict.values) == 10
    call_paths = [resolver.expression(key) for key in incident_fd_dict.keys
                  if key is not None]
    assert len(call_paths) == 10
    call_variables: list[str] = []
    for value in incident_fd_dict.values:
        assert isinstance(value, ast.Call)
        assert isinstance(value.func, ast.Name) and value.func.id == "int"
        assert len(value.args) == 1 and not value.keywords
        assert isinstance(value.args[0], ast.Name)
        call_variables.append(value.args[0].id)

    triples: list[tuple[Any, Any, Any]] = []
    for index, (path, file_sha) in enumerate(expected_pins.items()):
        assert normalize_incident_path(path) == roles[index]["path"]
        assert call_paths[index] == path
        assert call_variables[index] == fd_variables[index]
        triples.append((roles[index]["fd_environment"], path, file_sha))
    rows = normalized_rows_from_triples(triples)

    assert_normalized_ast_pin(
        launch, PRODUCER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "ensure_launch_configuration"],
        "producer ensure_launch_configuration AST")
    assert_expression_count(
        launch, "len({int(value) for value in fd_texts}) == 14")
    assert_expression_count(launch, "self_guard.terminal_replay()")
    assert expression_ast_key(one_direct_return(launch).value) == \
        parsed_expression_ast_key("self_guard")

    build_function = unique_top_function(tree, "build")
    main_function = unique_top_function(tree, "main")
    assert_normalized_ast_pin(
        build_function, PRODUCER_USE_CHAIN_NORMALIZED_AST_SHA256["build"],
        "producer build AST")
    assert_normalized_ast_pin(
        main_function, PRODUCER_USE_CHAIN_NORMALIZED_AST_SHA256["main"],
        "producer main AST")
    build_terminal = ast_expression_matches(
        build_function, "self_guard.terminal_replay()")
    build_commit = ast_expression_matches(
        build_function,
        "rename_candidate_noreplace(stage, outdir, stage_guard, "
        "output_guards, parent_guard)")
    assert len(build_terminal) == len(build_commit) == 1
    assert build_terminal[0].lineno < build_commit[0].lineno
    assert_expression_count(
        main_function, "ensure_launch_configuration()")
    assert_expression_count(
        main_function, "build(args.outdir, self_guard, coordination_parent)")
    assert_expression_count(main_function, "self_guard.terminal_replay()")
    main_build = ast_expression_matches(
        main_function, "build(args.outdir, self_guard, coordination_parent)")[0]
    main_terminal = ast_expression_matches(
        main_function, "self_guard.terminal_replay()")[0]
    assert main_build.lineno < main_terminal.lineno
    assert_expression_count(tree, "self_guard.terminal_replay()", 3)

    representation = b"\0".join([
        expression_ast_key(expected_pins_node).encode("utf-8"),
        *[expression_ast_key(node).encode("utf-8")
          for node in env_assignment_nodes],
        expression_ast_key(incident_fd_dict).encode("utf-8"),
        expression_ast_key(constructor).encode("utf-8"),
        expression_ast_key(terminal).encode("utf-8"),
        expression_ast_key(launch).encode("utf-8"),
        expression_ast_key(build_function).encode("utf-8"),
        expression_ast_key(main_function).encode("utf-8"),
    ])
    return rows, representation, (
        "HELDSELF_EXACT10_HOLD_TERMINAL_CONFIGURATION_BUILD_COMMIT_MAIN_USE_CHAIN")


def one_direct_return(function: ast.FunctionDef) -> ast.Return:
    matches = [node for node in function.body if isinstance(node, ast.Return)]
    assert len(matches) == 1 and matches[0].value is not None
    return matches[0]


def launcher_inherited_incident_extraction(
        tree: ast.Module) -> tuple[list[dict[str, Any]], bytes, str]:
    configure = unique_top_function(tree, "configure_workspace_paths")
    resolver = module_and_local_resolver(tree, configure.body)
    v9 = resolver.named("V9_EXACT10_PINS")
    v10 = resolver.named("V10_EXACT10_PINS")
    v11 = resolver.named("V11_EXACT10_PINS")
    v12 = resolver.named("V12_EXACT10_PINS")
    assert all(isinstance(value, tuple) and len(value) == 10
               for value in (v9, v10, v11, v12))
    raw_pairs = (
        (v10[3][0], v10[3][1]),
        (v9[7][0], v9[7][1]),
        (v11[3][0], v11[3][1]),
        (v11[7][0], v11[7][1]),
        (resolver.named("V11_OFFICIAL_REJECTION"),
         resolver.named("V11_REJECTION_FILE_PIN")),
        (v12[3][0], v12[3][1]),
        (v12[4][0], v12[4][1]),
        (v12[7][0], v12[7][1]),
        (resolver.named("V5_OFFICIAL_REJECTION"),
         resolver.named("V5_REJECTION_FILE_PIN")),
        (resolver.named("V12_OFFICIAL_REJECTION"),
         resolver.named("V12_REJECTION_FILE_PIN")),
    )
    env_symbols = (
        "HELD_V10_PRODUCER_FD_ENV", "HELD_V9_LAUNCHER_FD_ENV",
        "HELD_V11_PRODUCER_FD_ENV", "HELD_V11_LAUNCHER_FD_ENV",
        "HELD_V11_REJECTION_FD_ENV", "HELD_V12_PRODUCER_FD_ENV",
        "HELD_V12_CONSUMER_FD_ENV", "HELD_V12_LAUNCHER_FD_ENV",
        "HELD_V5_REJECTION_FD_ENV", "HELD_V12_REJECTION_FD_ENV",
    )
    triples = [
        (resolver.named(env_symbol), path, file_sha)
        for env_symbol, (path, file_sha) in zip(
            env_symbols, raw_pairs, strict=True)]
    rows = normalized_rows_from_triples(triples)

    v11_class = unique_class(tree, "HeldV11PredecessorExact10")
    v12_class = unique_class(tree, "HeldV12PredecessorExact10")
    bundle_class = unique_class(tree, "HeldBundle")
    child_exec_class = unique_class(tree, "HeldSealedChildExec")
    empty_namespace_class = unique_class(tree, "HeldEmptyRejectionNamespace")
    v11_method = unique_method(v11_class, "inherited_evidence_fds")
    v12_method = unique_method(v12_class, "inherited_v12_evidence_fds")
    bundle_method = unique_method(bundle_class, "inherited_incident_evidence_fds")
    v11_terminal = unique_method(v11_class, "terminal_replay")
    v12_terminal = unique_method(v12_class, "terminal_replay")
    bundle_terminal = unique_method(bundle_class, "terminal_replay")
    child_exec_terminal = unique_method(child_exec_class, "terminal_replay")
    empty_namespace_terminal = unique_method(
        empty_namespace_class, "terminal_replay")
    child_env = unique_top_function(tree, "child_environment")

    terminal_methods = {
        "HeldBundle.terminal_replay": bundle_terminal,
        "HeldV12PredecessorExact10.terminal_replay": v12_terminal,
        "HeldV11PredecessorExact10.terminal_replay": v11_terminal,
        "HeldSealedChildExec.terminal_replay": child_exec_terminal,
        "HeldEmptyRejectionNamespace.terminal_replay":
            empty_namespace_terminal,
    }
    for name, method in terminal_methods.items():
        assert_normalized_ast_pin(
            method, LAUNCHER_USE_CHAIN_NORMALIZED_AST_SHA256[name],
            f"launcher {name} AST")

    bundle_terminal_sequence = (
        "self.predecessor_v12.terminal_replay("
        "self.by_path[V12_OFFICIAL_REJECTION])",
        "self.predecessor_v11.terminal_replay("
        "self.predecessor_v12.by_path[V11_OFFICIAL_REJECTION])",
        "self.predecessor_v10.terminal_replay("
        "self.predecessor_v11.by_path[V10_OFFICIAL_REJECTION])",
        "self.predecessor_v9.terminal_replay("
        "self.predecessor_v10.by_path[V9_OFFICIAL_REJECTION])",
        "self.predecessor_v8.terminal_replay("
        "self.predecessor_v9.by_path[V8_OFFICIAL_REJECTION])",
        "self.predecessor_v7.terminal_replay("
        "self.predecessor_v8.by_path[V7_OFFICIAL_REJECTION])",
        "self.predecessor_v6.terminal_replay("
        "self.predecessor_v7.by_path[V6_OFFICIAL_REJECTION])",
        "self.predecessor_v5.terminal_replay("
        "self.predecessor_v6.by_path[V5_OFFICIAL_REJECTION])",
        "self.predecessor_v3.terminal_replay(self.v3_rejection)",
        "self.rejected_v4.terminal_replay()",
        "self.v3_rejection.terminal_replay()",
    )
    bundle_terminal_lines = []
    for expression in bundle_terminal_sequence:
        matches = ast_expression_matches(bundle_terminal, expression)
        assert len(matches) == 1
        bundle_terminal_lines.append(matches[0].lineno)
    assert bundle_terminal_lines == sorted(bundle_terminal_lines)
    bundle_guard_loops = [
        node for node in ast.walk(bundle_terminal)
        if isinstance(node, ast.For) and
        ast_target_shape(node.target) == "guard" and
        expression_ast_key(node.iter) == parsed_expression_ast_key(
            "[*self.files, self.manifest, self.outer]")]
    assert len(bundle_guard_loops) == 1
    assert_expression_count(
        bundle_guard_loops[0], "guard.terminal_replay()")
    assert_expression_count(bundle_terminal, "self.bootstrap.terminal_replay()")

    for predecessor_terminal in (v12_terminal, v11_terminal):
        file_loops = [
            node for node in ast.walk(predecessor_terminal)
            if isinstance(node, ast.For) and
            ast_target_shape(node.target) == "item" and
            expression_ast_key(node.iter) == parsed_expression_ast_key(
                "self.files")]
        assert len(file_loops) == 1
        assert_expression_count(file_loops[0], "item.terminal_replay()")
        assert_expression_count(
            predecessor_terminal, "self.namespace.terminal_replay(rejection)")
        assert_expression_count(
            predecessor_terminal, "self._assert_positive_runtime_absence()")
    assert_expression_count(
        v12_terminal,
        "derive_v12_v5_rejection_shape_incident("
        "self.by_path[V12_EXACT10_PINS[3][0]].raw,"
        "self.by_path[V12_EXACT10_PINS[4][0]].raw,"
        "self.by_path[V12_EXACT10_PINS[7][0]].raw,"
        "self.v5_rejection.raw,rejection.raw)==self.shape_incident")
    assert_expression_count(
        v11_terminal,
        "derive_v10_colon_prefix_witness("
        "self.predecessor_v10.by_path[V10_EXACT10_PINS[3][0]].raw,"
        "self.predecessor_v9.by_path[V9_EXACT10_PINS[7][0]].raw)"
        "==self.colon_witness")
    assert_expression_count(
        v11_terminal,
        "validate_v11_dual_validator_divergence("
        "self.by_path[V11_EXACT10_PINS[3][0]].raw,"
        "self.by_path[V11_EXACT10_PINS[7][0]].raw,self.colon_witness)")

    child_exec_assignments = direct_assignment_nodes(child_exec_terminal.body)
    child_exec_lines = [
        unique_direct_assignment(child_exec_assignments, name).lineno
        for name in ("before", "replay", "after", "seals")]
    assert child_exec_lines == sorted(child_exec_lines)
    assert_expression_count(child_exec_terminal, "os.fstat(self.fd)", 2)
    assert_expression_count(child_exec_terminal, "read_fd(self.fd)")
    assert_expression_count(
        child_exec_terminal, "fcntl.fcntl(self.fd,F_GET_SEALS)")
    assert_expression_count(
        child_exec_terminal,
        "fingerprint(before)==fingerprint(self.before)==fingerprint(after)"
        " and stat.S_IMODE(after.st_mode)==0o444 and after.st_nlink==0"
        " and seals==REQUIRED_EXEC_SEALS and replay==self.expected_raw"
        " and sha_bytes(replay)==self.expected_sha256")

    empty_assignments = direct_assignment_nodes(empty_namespace_terminal.body)
    empty_lines = [
        unique_direct_assignment(empty_assignments, name).lineno
        for name in ("before", "path_before", "first", "after", "path_after",
                     "second")]
    assert empty_lines == sorted(empty_lines)
    assert_expression_count(empty_namespace_terminal, "os.fstat(self.fd)", 2)
    assert_expression_count(
        empty_namespace_terminal, "root_lstat(self.path)", 2)
    assert_expression_count(
        empty_namespace_terminal, "set(os.listdir(self.fd))", 2)
    assert_expression_count(empty_namespace_terminal, "mount_id(self.fd)")
    assert_expression_count(
        empty_namespace_terminal,
        "fingerprint(before)==fingerprint(path_before)=="
        "fingerprint(self.before)==fingerprint(after)=="
        "fingerprint(path_after) and first==second==set() and "
        "stat.S_IMODE(after.st_mode)==0o555 and after.st_nlink==2 and "
        "mount_id(self.fd)==self.mount_id")

    expected_v11_return = (
        "(self.predecessor_v10.by_path[V10_EXACT10_PINS[3][0]].fd,"
        "self.predecessor_v9.by_path[V9_EXACT10_PINS[7][0]].fd,"
        "self.by_path[V11_EXACT10_PINS[3][0]].fd,"
        "self.by_path[V11_EXACT10_PINS[7][0]].fd,self.rejection.fd)")
    expected_v12_return = (
        "(self.by_path[V12_EXACT10_PINS[3][0]].fd,"
        "self.by_path[V12_EXACT10_PINS[4][0]].fd,"
        "self.by_path[V12_EXACT10_PINS[7][0]].fd,"
        "self.v5_rejection.fd,self.rejection.fd)")
    assert expression_ast_key(one_direct_return(v11_method).value) == \
        parsed_expression_ast_key(expected_v11_return)
    assert expression_ast_key(one_direct_return(v12_method).value) == \
        parsed_expression_ast_key(expected_v12_return)

    bundle_assignments = direct_assignment_nodes(bundle_method.body)
    bundle_result = unique_direct_assignment(bundle_assignments, "result")
    assert expression_ast_key(bundle_result) == parsed_expression_ast_key(
        "(*self.predecessor_v11.inherited_evidence_fds(),"
        "*self.predecessor_v12.inherited_v12_evidence_fds())")
    assert_expression_count(
        bundle_method, "len(result) == len(set(result)) == 10")
    assert expression_ast_key(one_direct_return(bundle_method).value) == \
        parsed_expression_ast_key("result")

    tuple_bindings = [
        node for node in child_env.body if isinstance(node, ast.Assign) and
        len(node.targets) == 1 and isinstance(node.targets[0], ast.Tuple)]
    expected_variables = (
        "v10_producer_fd", "v9_launcher_fd", "v11_producer_fd",
        "v11_launcher_fd", "v11_rejection_fd", "v12_producer_fd",
        "v12_consumer_fd", "v12_launcher_fd", "v5_rejection_fd",
        "v12_rejection_fd",
    )
    matching_bindings = [
        node for node in tuple_bindings
        if [item.id for item in node.targets[0].elts
            if isinstance(item, ast.Name)] == list(expected_variables)]
    assert len(matching_bindings) == 1
    binding = matching_bindings[0]
    assert len(binding.targets[0].elts) == 10
    assert expression_ast_key(binding.value) == parsed_expression_ast_key(
        "bundle.inherited_incident_evidence_fds()")
    child_return = one_direct_return(child_env)
    assert isinstance(child_return.value, ast.Dict)
    assert len(child_return.value.keys) >= 10
    tail_keys = child_return.value.keys[-10:]
    tail_values = child_return.value.values[-10:]
    for key, value, env_symbol, variable in zip(
            tail_keys, tail_values, env_symbols, expected_variables, strict=True):
        assert key is not None
        assert expression_ast_key(key) == parsed_expression_ast_key(env_symbol)
        assert expression_ast_key(value) == parsed_expression_ast_key(
            f"str({variable})")

    child_pass = unique_top_function(tree, "child_pass_fds")
    run_child = unique_top_function(tree, "run_non_authorize_child")
    authorize_child = unique_top_function(tree, "run_authorize_child")
    assert_normalized_ast_pin(
        child_pass, LAUNCHER_USE_CHAIN_NORMALIZED_AST_SHA256["child_pass_fds"],
        "launcher child_pass_fds AST")
    assert_normalized_ast_pin(
        run_child, LAUNCHER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "run_non_authorize_child"], "launcher subprocess.run path AST")
    assert_normalized_ast_pin(
        authorize_child, LAUNCHER_USE_CHAIN_NORMALIZED_AST_SHA256[
            "run_authorize_child"], "launcher subprocess.Popen path AST")
    child_pass_assignments = direct_assignment_nodes(child_pass.body)
    child_pass_result = unique_direct_assignment(
        child_pass_assignments, "result")
    assert expression_ast_key(child_pass_result) == parsed_expression_ast_key(
        "(child_exec.fd, source.fd, coordination.fd, "
        "bundle.bootstrap.root_fd, *bundle.inherited_incident_evidence_fds())")
    assert_expression_count(
        child_pass, "len(result) == 14 and len(set(result)) == 14")
    assert expression_ast_key(one_direct_return(child_pass).value) == \
        parsed_expression_ast_key("result")

    pass_fds_expression = (
        "child_pass_fds(bundle, child_exec, source, coordination)")
    assert_expression_count(tree, pass_fds_expression, 2)
    run_calls = [
        node for node in ast.walk(tree) if isinstance(node, ast.Call) and
        expression_ast_key(node.func) == parsed_expression_ast_key(
            "subprocess.run")]
    popen_calls = [
        node for node in ast.walk(tree) if isinstance(node, ast.Call) and
        expression_ast_key(node.func) == parsed_expression_ast_key(
            "subprocess.Popen")]
    assert len(run_calls) == len(popen_calls) == 1
    run_call, popen_call = run_calls[0], popen_calls[0]
    for call in (run_call, popen_call):
        assert all(keyword.arg is not None for keyword in call.keywords)
        keyword_names = [keyword.arg for keyword in call.keywords]
        assert len(keyword_names) == len(set(keyword_names))
        pass_keywords = [keyword for keyword in call.keywords
                         if keyword.arg == "pass_fds"]
        assert len(pass_keywords) == 1
        assert expression_ast_key(pass_keywords[0].value) == \
            parsed_expression_ast_key(pass_fds_expression)

    assert_expression_count(run_child, "bundle.terminal_replay()")
    assert_expression_count(run_child, "child_exec.terminal_replay()")
    assert_expression_count(run_child, "rejection_guard.terminal_replay()")
    assert_expression_count(run_child, "coordination.verify()")
    run_terminal = ast_expression_matches(
        run_child, "bundle.terminal_replay()")[0]
    run_return = one_direct_return(run_child)
    assert expression_ast_key(run_return.value) == parsed_expression_ast_key(
        "completed.stdout")
    assert run_call.lineno < run_terminal.lineno < run_return.lineno

    assert_expression_count(authorize_child, "bundle.terminal_replay()", 2)
    assert_expression_count(authorize_child, "child_exec.terminal_replay()", 3)
    assert_expression_count(
        authorize_child, "rejection_guard.terminal_replay()", 2)
    zero_output_branches = [
        node for node in ast.walk(authorize_child) if isinstance(node, ast.If) and
        expression_ast_key(node.test) == parsed_expression_ast_key(
            "inner_raw == b''")]
    assert len(zero_output_branches) == 1
    zero_branch = zero_output_branches[0]
    for source in (
        "process.wait()", "child_exec.terminal_replay()",
        "bundle.terminal_replay()", "rejection_guard.terminal_replay()",
        "coordination.verify()",
    ):
        assert_expression_count(zero_branch, source)
    false_returns = [
        node for node in ast.walk(zero_branch) if isinstance(node, ast.Return) and
        isinstance(node.value, ast.Constant) and node.value.value is False]
    assert len(false_returns) == 1
    zero_order = [
        ast_expression_matches(zero_branch, source)[0].lineno
        for source in (
            "process.wait()", "child_exec.terminal_replay()",
            "bundle.terminal_replay()", "rejection_guard.terminal_replay()",
            "coordination.verify()")]
    assert popen_call.lineno < min(zero_order)
    assert zero_order == sorted(zero_order)
    assert zero_order[-1] < false_returns[0].lineno

    authorize_bundle_terminals = sorted(
        ast_expression_matches(authorize_child, "bundle.terminal_replay()"),
        key=lambda node: node.lineno)
    assert len(authorize_bundle_terminals) == 2
    request_assignments = [
        node for node in ast.walk(authorize_child) if isinstance(node, ast.Assign) and
        len(node.targets) == 1 and ast_target_shape(node.targets[0]) == "request"]
    assert len(request_assignments) == 1
    stdin_writes = ast_expression_matches(
        authorize_child, "process.stdin.write(request_raw)")
    assert len(stdin_writes) == 1
    assert (popen_call.lineno < authorize_bundle_terminals[1].lineno <
            request_assignments[0].lineno < stdin_writes[0].lineno)

    configure_assignments = direct_assignment_nodes(configure.body)
    representation_nodes = [
        unique_direct_assignment(configure_assignments, name)
        for name in ("V9_EXACT10_PINS", "V10_EXACT10_PINS",
                     "V11_EXACT10_PINS", "V12_EXACT10_PINS")]
    representation = b"\0".join([
        *[expression_ast_key(node).encode("utf-8")
          for node in representation_nodes],
        expression_ast_key(v11_method).encode("utf-8"),
        expression_ast_key(v12_method).encode("utf-8"),
        expression_ast_key(bundle_method).encode("utf-8"),
        expression_ast_key(bundle_terminal).encode("utf-8"),
        expression_ast_key(v12_terminal).encode("utf-8"),
        expression_ast_key(v11_terminal).encode("utf-8"),
        expression_ast_key(child_exec_terminal).encode("utf-8"),
        expression_ast_key(empty_namespace_terminal).encode("utf-8"),
        expression_ast_key(child_env).encode("utf-8"),
        expression_ast_key(child_pass).encode("utf-8"),
        expression_ast_key(run_child).encode("utf-8"),
        expression_ast_key(authorize_child).encode("utf-8"),
    ])
    return rows, representation, (
        "CONFIGURED_EXACT10_HELD_FD_CHILD_ENV_PASS_FDS_RUN_POPEN_"
        "FIVE_TERMINAL_CALLEE_USE_CHAIN")


def derive_inherited_incident_source_contract(
        held: dict[str, Held]) -> dict[str, Any]:
    source_specs = (
        ("producer", "v13_build_only_producer_source",
         producer_inherited_incident_extraction),
        ("consumer", "v13_independent_consumer_source",
         consumer_inherited_incident_extraction),
        ("launcher", "v13_cold_launcher_source",
         launcher_inherited_incident_extraction),
    )
    expected = expected_inherited_incident_table()
    normalized_raw = canonical(expected)
    extractions: list[dict[str, Any]] = []
    representations: list[bytes] = []
    helper_digests: list[str] = []
    for source_role, name, extractor in source_specs:
        pins = [pin for pin in EVIDENCE_EXACT8 if pin["name"] == name]
        assert len(pins) == 1
        pin = pins[0]
        source = held[pin["path"]]
        raw = source.read()
        assert sha256(raw) == pin["file_sha256"]
        tree, _values = module_constants(raw, pin["path"])
        rows, representation_raw, representation_kind = extractor(tree)
        assert rows == expected and canonical(rows) == normalized_raw
        helper_digest, helper_match_count = normalized_incident_helper_ast(tree)
        representations.append(representation_raw)
        helper_digests.append(helper_digest)
        extractions.append({
            "source_role": source_role,
            "source_path": pin["path"],
            "source_file_sha256": pin["file_sha256"],
            "representation": representation_kind,
            "representation_normalized_ast_byte_length": len(representation_raw),
            "representation_normalized_ast_sha256": sha256(representation_raw),
            "normalized_exact10_canonical_sha256":
                INHERITED_INCIDENT_EXACT10_CANONICAL_SHA256,
            "unique_match_count": 1,
            "incident_helper_unique_match_count": helper_match_count,
            "incident_helper_normalized_ast_sha256": helper_digest,
        })
        if source_role == "launcher":
            extractions[-1][
                "terminal_replay_callee_method_normalized_ast_sha256"] = {
                    name: LAUNCHER_USE_CHAIN_NORMALIZED_AST_SHA256[name]
                    for name in (
                        "HeldBundle.terminal_replay",
                        "HeldV12PredecessorExact10.terminal_replay",
                        "HeldV11PredecessorExact10.terminal_replay",
                        "HeldSealedChildExec.terminal_replay",
                        "HeldEmptyRejectionNamespace.terminal_replay",
                    )
                }
            extractions[-1]["terminal_replay_callee_method_count"] = 5
    assert len({sha256(value) for value in representations}) == 3
    assert len(set(helper_digests)) == 1
    assert helper_digests[0] == V12_V5_INCIDENT_HELPER_NORMALIZED_AST_SHA256
    return {
        "normalized_ordered_members": expected,
        "normalized_ordered_member_count": 10,
        "normalized_record_exact_keys": [
            "ordinal", "role", "fd_environment", "path", "file_sha256"],
        "normalized_exact10_canonical_byte_length": len(normalized_raw),
        "normalized_exact10_canonical_sha256": sha256(normalized_raw),
        "source_extractions": extractions,
        "source_extraction_count": 3,
        "literal_source_representations_byte_identical": False,
        "three_source_normalized_tables_byte_identical": True,
        "three_source_actual_exact10_consumption_use_chains_ast_verified": True,
        "producer_hold_hash_path_mount_terminal_commit_and_main_chain_verified":
            True,
        "consumer_configuration_hold_terminal_close_and_main_chain_verified":
            True,
        "launcher_exact10_child_environment_pass_fds_run_Popen_and_five_"
        "terminal_callee_chains_verified": True,
        "incident_helper_three_source_normalized_asts_byte_identical": True,
        "incident_helper_normalized_ast_sha256":
            V12_V5_INCIDENT_HELPER_NORMALIZED_AST_SHA256,
        "fd_environment_names_are_historical_v13_records_not_v14_pins": True,
        "ast_only_no_target_import_or_execution": True,
    }


def validate_draft_flags_and_sources(held: dict[str, Held]) -> None:
    by_name = {item.pin["name"]: item for item in held.values()}
    required = {
        "v13_build_only_producer_source": {
            "V13_DRAFT_RUNTIME_DISABLED": True,
            "FINAL_V13_CORE_PINS_INSTALLED": False,
        },
        "v13_independent_consumer_source": {
            "V13_DRAFT_RUNTIME_DISABLED": True,
            "FINAL_CURRENT_V13_PINS_INSTALLED": False,
        },
        "v13_cold_launcher_source": {
            "V13_DRAFT_RUNTIME_DISABLED": True,
            "FINAL_BASE7_PINS_INSTALLED": False,
        },
        "v13_json_draft_builder_tool": {
            "V13_DRAFT_BUILDER_ENABLED": False,
        },
    }
    source_items = [item for item in EVIDENCE_EXACT8 if item["path"].endswith(".py")]
    assert len(source_items) == 5
    for pin in source_items:
        item = held[pin["path"]]
        _tree, values = module_constants(item.read(), pin["path"])
        for key, expected in required.get(pin["name"], {}).items():
            assert key in values and values[key] is expected, (pin["name"], key)
    assert set(required) <= set(by_name)


def validate_pep552(held: dict[str, Held]) -> list[dict[str, Any]]:
    assert sys.version_info[:2] == (3, 12)
    source_by_path = {
        pin["path"]: held[pin["path"]]
        for pin in EVIDENCE_EXACT8 if pin["path"].endswith(".py")
    }
    result: list[dict[str, Any]] = []
    for pin in EVIDENCE_EXACT8:
        if not pin["path"].endswith(".pyc"):
            continue
        raw = held[pin["path"]].read()
        assert len(raw) > 16
        assert raw[:4] == importlib.util.MAGIC_NUMBER
        flags = int.from_bytes(raw[4:8], "little")
        timestamp = int.from_bytes(raw[8:12], "little")
        source_size = int.from_bytes(raw[12:16], "little")
        header_hex = raw[:16].hex()
        assert flags == pin["pep552_flags"] == 0
        assert timestamp == pin["pep552_timestamp"]
        assert source_size == pin["pep552_source_size"]
        assert header_hex == pin["pep552_header_hex"]
        source = source_by_path[pin["source_path"]]
        source_state = os.fstat(source.fd)
        assert timestamp == (source_state.st_mtime_ns // 1_000_000_000) & 0xffffffff
        assert source_size == source_state.st_size & 0xffffffff
        result.append({
            "name": pin["name"],
            "path": pin["path"],
            "source_path": pin["source_path"],
            "file_sha256": pin["file_sha256"],
            "size": pin["size"],
            "pep552_magic_hex": raw[:4].hex(),
            "pep552_header_hex": header_hex,
            "pep552_flags": flags,
            "pep552_timestamp": timestamp,
            "pep552_source_size": source_size,
            "pep552_header_matches_pinned_source_stat": True,
        })
    assert len(result) == 3
    return result


def assert_no_v13_runtime_names(directory_fd: int,
                                seen: set[tuple[int, int]],
                                expected_mount_id: int) -> None:
    before_state = os.fstat(directory_fd)
    identity = stat_identity(before_state)
    assert identity not in seen
    seen.add(identity)
    assert fd_mount_id(directory_fd) == expected_mount_id
    names_before = sorted(os.listdir(directory_fd))
    for name in names_before:
        assert "c79g-v13" not in name.lower(), name
        child = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        if stat.S_ISDIR(child.st_mode):
            descriptor = os.open(
                name,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC |
                getattr(os, "O_NOATIME", 0),
                dir_fd=directory_fd)
            try:
                assert stat_identity(os.fstat(descriptor)) == stat_identity(child)
                assert fd_mount_id(descriptor) == expected_mount_id
                assert_no_v13_runtime_names(
                    descriptor, seen, expected_mount_id)
            finally:
                os.close(descriptor)
    names_after = sorted(os.listdir(directory_fd))
    after_state = os.fstat(directory_fd)
    assert names_after == names_before
    assert Held.identity(before_state) == Held.identity(after_state)


def assert_v13_unpublished_and_runtime_absent(resolver: Resolver) -> None:
    for rel in FORBIDDEN_V13_STATIC:
        assert not resolver.exists(rel), rel
    assert_no_v13_runtime_names(
        resolver.directories.runtime.fd, set(),
        resolver.directories.runtime.mount_id)
    resolver.directories.replay()


def assert_exact_three_target_v13_pyc(resolver: Resolver) -> None:
    expected = {
        Path(pin["path"]).name
        for pin in EVIDENCE_EXACT8 if pin["path"].endswith(".pyc")}
    directory = resolver.directories.pycache
    before_state = os.fstat(directory.fd)
    names_before = sorted(os.listdir(directory.fd))
    actual: set[str] = set()
    for name in names_before:
        state = os.stat(
            name, dir_fd=directory.fd,
            follow_symlinks=False)
        if (name.endswith(".pyc") and name.startswith(BASE) and
                "v13" in name):
            assert stat.S_ISREG(state.st_mode) and not stat.S_ISLNK(state.st_mode), (
                "v13 target pyc-shaped entry is not a regular file", name)
            actual.add(name)
    names_after = sorted(os.listdir(directory.fd))
    after_state = os.fstat(directory.fd)
    assert names_after == names_before
    assert Held.identity(before_state) == Held.identity(after_state)
    assert len(expected) == 3 and actual == expected
    directory.replay()


class HeldRejectionNamespace:
    def __init__(self, resolver: Resolver, rejection: Held,
                 official_rejection: dict[str, Any]):
        self.resolver = resolver
        self.rejection = rejection
        self.official_rejection = dict(official_rejection)
        assert self.rejection.pin["path"] == self.official_rejection["path"]
        self.rel = self.official_rejection["path"].rsplit("/", 1)[0]
        self.fd, path_state = resolver.open_directory(self.rel)
        try:
            fd_state = os.fstat(self.fd)
            assert stat_identity(path_state) == stat_identity(fd_state)
            self.initial = fd_state
            self.dev_ino = stat_identity(fd_state)
            self.mount_id = fd_mount_id(self.fd)
            self.initial_names = tuple(sorted(os.listdir(self.fd)))
            assert self.initial_names == ("rejection.json",)
            self.replay()
        except BaseException:
            os.close(self.fd)
            raise

    def replay(self) -> None:
        path_state = self.resolver.stat(self.rel)
        before = os.fstat(self.fd)
        assert stat_identity(path_state) == stat_identity(before) == self.dev_ino
        assert full_file_identity(path_state) == full_file_identity(before) == \
            full_file_identity(self.initial)
        assert stat.S_ISDIR(before.st_mode)
        assert stat.S_IMODE(before.st_mode) == 0o555 and before.st_nlink == 2
        assert fd_mount_id(self.fd) == self.mount_id
        names_before = sorted(os.listdir(self.fd))
        assert tuple(names_before) == self.initial_names
        rejection_state, _raw = self.rejection.replay(require_frozen=True)
        assert full_file_identity(rejection_state) == \
            full_file_identity(self.rejection.initial)
        assert rejection_state.st_dev == before.st_dev
        assert fd_mount_id(self.rejection.fd) == self.mount_id
        names_after = sorted(os.listdir(self.fd))
        after = os.fstat(self.fd)
        assert names_after == names_before
        assert full_file_identity(after) == full_file_identity(before) == \
            full_file_identity(self.initial)

    def close(self) -> None:
        try:
            os.close(self.fd)
        except OSError:
            pass


def validate_v12_anchor(
        resolver: Resolver
        ) -> tuple[list[Held], HeldRejectionNamespace, HeldRejectionNamespace]:
    opened: list[Held] = []
    v11_namespace: HeldRejectionNamespace | None = None
    v12_namespace: HeldRejectionNamespace | None = None
    try:
        pins = [*V12_EXACT10, V12_OFFICIAL_REJECTION]
        for pin in pins:
            item = Held(resolver, pin, {0o444})
            opened.append(item)
            item.replay(require_frozen=True)
        assert len({(item.initial.st_dev, item.initial.st_ino) for item in opened}) == 11
        assert len({item.initial.st_dev for item in opened}) == 1
        manifest = opened[8].read()
        expected_manifest = b"".join(
            (entry["file_sha256"] + "  " + entry["path"] + "\n").encode("ascii")
            for entry in V12_EXACT10[:8])
        assert manifest == expected_manifest
        outer_raw = opened[9].read()
        rejection_raw = opened[10].read()
        outer = verify_object(outer_raw, V12_EXACT10[9]["object_sha256"])
        rejection = verify_object(
            rejection_raw, V12_OFFICIAL_REJECTION["object_sha256"])
        assert outer_raw == canonical(outer) + b"\n"
        assert rejection_raw == canonical(rejection) + b"\n"
        assert outer["status"] == (
            "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__"
            "RUNTIME_DEFERRED")
        assert outer["formal_global_closure_credit"] == 0
        assert outer["D02_unlock"] is False
        assert outer["cold_launch_manifest"]["file_sha256"] == V12_EXACT10[8]["file_sha256"]
        assert outer["cold_launch_manifest"]["path"] == V12_EXACT10[8]["path"]
        assert outer["cold_launcher"] == {
            "path": V12_EXACT10[7]["path"],
            "file_sha256": V12_EXACT10[7]["file_sha256"],
        }
        assert outer["exact8_ordered_entries"] == [
            {"path": item["path"], "file_sha256": item["file_sha256"]}
            for item in V12_EXACT10[:8]
        ]
        assert rejection["status"] == "PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT"
        assert rejection["formal_global_closure_credit"] == 0
        assert rejection["D02_gate_credit"] == 0
        assert rejection["D02_task_credit"] == 0
        assert rejection["D02_unlock"] is False and rejection["D02_started"] is False
        assert rejection["D02_formal_pending_task_count"] == 33638
        assert rejection["standalone_authority"] is False
        assert rejection["closed_schema_file_sha256"] == \
            V12_EXACT10[1]["file_sha256"]
        assert rejection["contract_file_sha256"] == \
            V12_EXACT10[2]["file_sha256"]
        assert rejection["contract_object_sha256"] == \
            V12_EXACT10[2]["object_sha256"]
        assert rejection["producer_file_sha256"] == \
            V12_EXACT10[3]["file_sha256"]
        assert rejection["consumer_file_sha256"] == \
            V12_EXACT10[4]["file_sha256"]
        assert rejection["cold_launcher_file_sha256"] == \
            V12_EXACT10[7]["file_sha256"]
        assert rejection["cold_manifest_file_sha256"] == \
            V12_EXACT10[8]["file_sha256"]
        assert rejection["cold_outer_file_sha256"] == \
            V12_EXACT10[9]["file_sha256"]
        assert rejection["cold_outer_object_sha256"] == \
            V12_EXACT10[9]["object_sha256"]
        assert rejection["v11_official_rejection_file_sha256"] == \
            V12_EXACT10[0]["file_sha256"]
        assert rejection["v11_official_rejection_object_sha256"] == \
            V12_EXACT10[0]["object_sha256"]
        outer_state = opened[9].initial
        rejection_state = opened[10].initial
        assert max(outer_state.st_mtime_ns, outer_state.st_ctime_ns) < min(
            rejection_state.st_mtime_ns, rejection_state.st_ctime_ns)
        for item in opened:
            terminal_state, _raw = item.replay(require_frozen=True)
            assert full_file_identity(terminal_state) == \
                full_file_identity(item.initial)
        v11_namespace = HeldRejectionNamespace(
            resolver, opened[0], V12_EXACT10[0])
        v12_namespace = HeldRejectionNamespace(
            resolver, opened[10], V12_OFFICIAL_REJECTION)
        assert v11_namespace.mount_id == v12_namespace.mount_id == \
            resolver.directories.runtime.mount_id
        resolver.directories.replay()
        return opened, v11_namespace, v12_namespace
    except BaseException:
        if v12_namespace is not None:
            v12_namespace.close()
        if v11_namespace is not None:
            v11_namespace.close()
        for item in opened:
            item.close()
        raise


def full_file_identity(value: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (*Held.identity(value), stat.S_IMODE(value.st_mode))


def stable_directory_snapshot(
        directory: HeldDirectory) -> tuple[tuple[int, int, int, int, int, int, int],
                                           tuple[str, ...]]:
    before = os.fstat(directory.fd)
    names_before = tuple(sorted(os.listdir(directory.fd)))
    names_after = tuple(sorted(os.listdir(directory.fd)))
    after = os.fstat(directory.fd)
    assert names_after == names_before
    assert full_file_identity(after) == full_file_identity(before)
    directory.replay()
    return full_file_identity(before), names_before


def persisted_evidence(pin: dict[str, Any], frozen_state: os.stat_result) -> dict[str, Any]:
    result = {
        "name": pin["name"],
        "role": pin["role"],
        "path": pin["path"],
        "file_sha256": pin["file_sha256"],
        "size": pin["size"],
        "prefreeze_mode": "0664",
        "frozen_mode": "0444",
        "nlink": 1,
        "prefreeze_mtime_ns": pin["mtime_ns"],
        "prefreeze_ctime_ns": pin["ctime_ns"],
        "postfreeze_mtime_ns": frozen_state.st_mtime_ns,
        "postfreeze_ctime_ns": frozen_state.st_ctime_ns,
    }
    if pin["path"].endswith(".pyc"):
        result.update({
            "source_path": pin["source_path"],
            "pep552_magic_hex": importlib.util.MAGIC_NUMBER.hex(),
            "pep552_header_hex": pin["pep552_header_hex"],
            "pep552_flags": pin["pep552_flags"],
            "pep552_timestamp": pin["pep552_timestamp"],
            "pep552_source_size": pin["pep552_source_size"],
            "pep552_header_matches_pinned_source_stat": True,
        })
    return result


def v14_inherited_incident_exact16(
        live6: list[dict[str, Any]],
        source_contract: dict[str, Any]) -> dict[str, Any]:
    inherited = source_contract["normalized_ordered_members"]
    assert inherited == expected_inherited_incident_table()
    assert [row["name"] for row in live6] == list(LIVE_EXACT6_NAMES)
    ordered: list[dict[str, Any]] = [
        {
            "ordinal": row["ordinal"],
            "role": row["role"],
            "path": row["path"],
            "file_sha256": row["file_sha256"],
        }
        for row in inherited]
    ordered.extend({
        "ordinal": index,
        "role": row["name"],
        "path": row["path"],
        "file_sha256": row["file_sha256"],
    } for index, row in enumerate(live6, start=11))
    assert len(ordered) == 16
    assert [row["ordinal"] for row in ordered] == list(range(1, 17))
    assert len({row["path"] for row in ordered}) == 16
    assert all(set(row) == {"ordinal", "role", "path", "file_sha256"}
               for row in ordered)
    exact16_raw = canonical(ordered)
    return {
        "ordered_members": ordered,
        "ordered_member_count": 16,
        "ordered_member_exact_keys": [
            "ordinal", "role", "path", "file_sha256"],
        "inherited_normalized_exact10_count": 10,
        "ordered_live_v13_source_then_pyc_exact6_count": 6,
        "ordered_exact16_canonical_byte_length": len(exact16_raw),
        "ordered_exact16_canonical_sha256": sha256(exact16_raw),
        "v14_must_live_hold_and_terminally_replay_exact16_plus_this_receipt": True,
        "v13_fd_environment_names_are_historical_records_not_v14_pins": True,
        "this_receipt_pins_no_v14_successor_byte_or_v14_fd_number": True,
    }


def make_receipt(frozen: list[dict[str, Any]],
                 pep552: list[dict[str, Any]],
                 source_contract: dict[str, Any]) -> dict[str, Any]:
    by_name = {row["name"]: row for row in frozen}
    live6 = [by_name[name] for name in LIVE_EXACT6_NAMES]
    tooling2 = [by_name[name] for name in TOOLING_EXACT2_NAMES]
    assert len(live6) == 6 and len(tooling2) == 2
    assert source_contract["normalized_ordered_members"] == \
        expected_inherited_incident_table()
    exact16 = v14_inherited_incident_exact16(live6, source_contract)
    return close_object({
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer."
            "v13-prepublication-pyc-contamination-rejection-"
            "supersession-receipt.v1"),
        "status": (
            "FROZEN_APPEND_ONLY_V13_PREPUBLICATION_PYC_CONTAMINATION_"
            "REJECTION__V14_SUCCESSOR_ONLY"),
        "receipt_path": RECEIPT_REL,
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "transition_kind": (
            "PREPUBLICATION_PYC_CONTAMINATION_REJECTION_AND_SUPERSESSION_"
            "WITHOUT_IMPORT_EXECUTION_RUNTIME_OR_POSITIVE_PUBLICATION"),
        "credit": {
            "formal_global_closure_credit": 0,
            "D02_gate_credit": 0,
            "D02_task_credit": 0,
            "D02_unlock": False,
            "D02_started": False,
            "D02_formal_pending_task_count": 33638,
        },
        "frozen_v13_prepublication_evidence_exact8": {
            "ordered_members": frozen,
            "ordered_member_count": 8,
            "all_initially_regular_0664_nlink1": True,
            "all_frozen_regular_0444_nlink1": True,
            "all_unique_inode_and_same_st_dev_verified_live_not_persisted": True,
            "all_file_hash_size_mtime_and_prefreeze_ctime_pins_match": True,
            "exact8_joint_terminal_same_fd_replay_before_receipt": True,
        },
        "frozen_v13_inherited_incident_authority_exact10_source_contract":
            source_contract,
        "live_successor_required_incident_exact6": {
            "ordered_members": live6,
            "ordered_member_count": 6,
            "v14_must_live_hold_and_terminally_replay_all_six_plus_this_receipt": True,
        },
        "supplemental_tooling_exact2": {
            "ordered_members": tooling2,
            "ordered_member_count": 2,
            "v14_may_bind_these_only_through_this_receipt_file_and_object_hashes": True,
            "v14_need_not_live_hold_these_two_tool_files": True,
        },
        "pyc_contamination_incident": {
            "physical_target_protocol_pyc_file_count": 3,
            "supplemental_tooling_pyc_files_outside_incident_exact8_are_not_"
            "protocol_target_pyc_evidence": True,
            "ordered_pep552_evidence": pep552,
            "operator_reported_py_compile_command_invocation_count": 4,
            "operator_reported_command_shape": {
                "first_command_compiled_producer_consumer_and_launcher_together": True,
                "later_consumer_only_commands": 3,
            },
            "operator_reported_bytecode_write_event_count_by_source": {
                "producer_v13": 1,
                "consumer_v13": 4,
                "launcher_v13": 1,
            },
            "operator_reported_bytecode_write_event_count_total": 6,
            "consumer_prior_pyc_bytes_overwritten_and_not_replayable_count": 3,
            "guard_py_compile_invocation_count": 0,
            "guard_imported_target_module_count": 0,
            "guard_executed_target_code_count": 0,
            "guard_validation_limited_to_ast_and_in_memory_compile": True,
            "operator_attested_target_protocol_import_count": 0,
            "operator_attested_target_protocol_execution_count": 0,
        },
        "frozen_v12_authority_anchor": {
            "ordered_published_exact10": list(V12_EXACT10),
            "official_v12_rejection": dict(V12_OFFICIAL_REJECTION),
            "all_eleven_regular_0444_nlink1_hash_and_object_pins_match": True,
            "v12_rejection_is_canonical_singleton_zero_credit": True,
            "v11_and_v12_rejection_singleton_namespaces_held_to_terminal": True,
            "v12_rejection_generic_schema_contract_producer_consumer_launcher_"
            "manifest_outer_pins_match_held_exact10": True,
            "v12_outer_full_identity_times_strictly_precede_rejection": True,
            "v12_rejection_formal_D02_credit_zero_and_standalone_false": True,
        },
        "v13_no_run_no_publication_attestation": {
            "v13_schema_exists": False,
            "v13_contract_exists": False,
            "v12_to_v13_transition_exists": False,
            "v13_static_audit_exists": False,
            "v13_manifest_exists": False,
            "v13_outer_exists": False,
            "v13_runtime_surface_count": 0,
            "v13_protocol_import_count_by_this_guard": 0,
            "v13_protocol_execution_count_by_this_guard": 0,
            "v13_final_pin_flags_all_false_by_ast": True,
            "v13_runtime_disabled_flags_all_true_by_ast": True,
            "v13_builder_enabled_flag_false_by_ast": True,
        },
        "permanent_rejection_policy": {
            "v13_must_never_gain_schema_contract_transition_or_static_audit": True,
            "v13_must_never_gain_manifest_or_outer": True,
            "v13_must_never_gain_any_runtime_surface": True,
            "v13_build_verify_assemble_authorize_reject_commands_allowed": False,
            "exact8_overwrite_allowed": False,
            "exact8_delete_allowed": False,
            "exact8_path_or_inode_reuse_allowed": False,
            "exact8_promotion_to_authority_allowed": False,
            "orphan_policy": (
                "PRESERVE_AS_FROZEN_NON_AUTHORITATIVE_INCIDENT_EVIDENCE__"
                "NEVER_OVERWRITE_DELETE_REUSE_OR_PROMOTE"),
        },
        "v14_successor_contract": {
            "successor_version": 14,
            "inherited_incident_authority_exact16": exact16,
            "v14_current_exact8_first_member_must_be_this_receipt": True,
            "v14_must_pin_this_receipt_file_and_object_sha256": True,
            "this_receipt_does_not_pin_any_v14_successor_byte": True,
            "one_way_binding_avoids_hash_cycle": True,
            "v14_must_preserve_v12_exact10_and_official_rejection": True,
            "v14_predecessor_unique_live_identity_count": 105,
            "v14_prepublication_unique_live_identity_count": 113,
            "v14_terminal_unique_live_identity_count": 115,
            "v14_terminal_group_vector": [
                10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 1, 3, 3, 1,
            ],
            "v14_census_derivation": {
                "prior_history": 98,
                "v12_official_rejection_singleton": 1,
                "v13_live_successor_required_incident_exact6": 6,
                "predecessor_total": 105,
                "v14_current_exact8": 8,
                "prepublication_total": 113,
                "v14_manifest_and_outer": 2,
                "terminal_total": 115,
                "supplemental_tooling_exact2_not_separately_live_counted_by_v14": True,
            },
        },
        "publication_mechanics": {
            "official_writer_lock_held_for_entire_freeze_and_receipt_commit": True,
            "exact8_fds_held_from_preflight_through_terminal_exact9_replay": True,
            "root_output_runtime_pycache_and_scripts_directory_fds_held_and_"
            "identity_mount_replayed_through_terminal": True,
            "freeze_order_is_exact8_order": True,
            "interrupted_pre_receipt_freeze_resume_requires_only_0444_prefix_"
            "then_0664_suffix": True,
            "resumed_frozen_prefix_refchmod_count": 0,
            "resumed_frozen_prefix_held_files_are_fsynced_before_continuing": True,
            "receipt_commit_operation": (
                "O_TMPFILE_ANONYMOUS_COMPLETE_FCHMOD0444_FSYNC_VERIFY__"
                "PROC_SELF_FD_LINKAT_AT_SYMLINK_FOLLOW_ATOMIC_NO_REPLACE"),
            "anonymous_receipt_inode_nlink_before_publication": 0,
            "otmpfile_proc_self_fd_and_unprivileged_linkat_capability_verified_"
            "before_first_freeze": True,
            "formal_receipt_link_does_not_depend_on_linkat_AT_EMPTY_PATH_or_"
            "CAP_DAC_READ_SEARCH": True,
            "receipt_file_mode": "0444",
            "file_and_parent_fsync_required": True,
            "receipt_created_after_joint_frozen_exact8_terminal_replay": True,
            "terminal_exact9_same_fd_replay_required": True,
            "exact_existing_canonical_receipt_terminal_recovery_allowed": True,
            "existing_receipt_recovery_performs_no_content_write_chmod_or_"
            "overwrite": True,
            "existing_receipt_recovery_fsyncs_held_output_runtime_and_root_"
            "before_terminal_replay": True,
            "partial_or_inexact_existing_receipt_requires_new_receipt_version": True,
            "overwrite_or_delete_allowed": False,
            "unlink_called_at_any_stage": False,
        },
    })


def main() -> int:
    if not __debug__:
        raise RuntimeError("python -O is forbidden")
    assert FINAL_V13_PREPUBLICATION_SUPERSESSION_GUARD_PINS_INSTALLED is True
    assert len(sys.argv) == 3
    root = Path(sys.argv[1]).resolve(strict=True)
    command = sys.argv[2]
    assert root == ROOT_EXPECTED
    assert command in {"PREFLIGHT", "FREEZE_REJECT"}
    assert len(EVIDENCE_EXACT8) == 8
    assert [item["name"] for item in EVIDENCE_EXACT8] == [
        "v13_build_only_producer_source",
        "v13_independent_consumer_source",
        "v13_cold_launcher_source",
        "v13_json_draft_builder_tool",
        "v13_independent_static_review_tool",
        "v13_build_only_producer_pyc",
        "v13_independent_consumer_pyc",
        "v13_cold_launcher_pyc",
    ]
    assert len(set(LIVE_EXACT6_NAMES)) == 6
    assert len(set(TOOLING_EXACT2_NAMES)) == 2
    assert set(LIVE_EXACT6_NAMES) | set(TOOLING_EXACT2_NAMES) == {
        item["name"] for item in EVIDENCE_EXACT8}

    directories = HeldDirectories(root)
    resolver = Resolver(directories)
    locked = False
    cleanup_complete = False
    exact8: dict[str, Held] = {}
    v12_anchors: list[Held] = []
    v11_namespace: HeldRejectionNamespace | None = None
    v12_namespace: HeldRejectionNamespace | None = None
    receipt: HeldReceipt | None = None
    incident_source_contract: dict[str, Any] | None = None
    preflight_output_snapshot: tuple[
        tuple[int, int, int, int, int, int, int], tuple[str, ...]] | None = None
    result: dict[str, Any] | None = None
    try:
        fcntl.flock(directories.runtime.fd, fcntl.LOCK_EX)
        locked = True
        directories.replay()
        receipt_exists = resolver.exists(RECEIPT_REL)
        if command == "PREFLIGHT":
            assert not receipt_exists
            preflight_output_snapshot = stable_directory_snapshot(
                directories.output)
            assert Path(RECEIPT_REL).name not in preflight_output_snapshot[1]
        assert_v13_unpublished_and_runtime_absent(resolver)
        allowed_modes = ({0o664} if command == "PREFLIGHT" else
                         {0o444, 0o664})
        for pin in EVIDENCE_EXACT8:
            assert re.fullmatch(r"[0-9a-f]{64}", pin["file_sha256"])
            exact8[pin["path"]] = Held(resolver, pin, allowed_modes)
        assert len(exact8) == 8
        initial_ids = {(item.initial.st_dev, item.initial.st_ino)
                       for item in exact8.values()}
        assert len(initial_ids) == 8
        assert len({item.initial.st_dev for item in exact8.values()}) == 1
        assert {fd_mount_id(item.fd) for item in exact8.values()} == {
            directories.output.mount_id}
        initial_modes = [
            stat.S_IMODE(exact8[pin["path"]].initial.st_mode)
            for pin in EVIDENCE_EXACT8]
        if command == "PREFLIGHT":
            assert initial_modes == [0o664] * 8
            initial_frozen_prefix_count = 0
        else:
            initial_frozen_prefix_count = 0
            while (initial_frozen_prefix_count < 8 and
                   initial_modes[initial_frozen_prefix_count] == 0o444):
                initial_frozen_prefix_count += 1
            assert initial_modes == (
                [0o444] * initial_frozen_prefix_count +
                [0o664] * (8 - initial_frozen_prefix_count)), (
                    "only a 0444 prefix followed by a 0664 suffix is recoverable",
                    initial_modes)
            if receipt_exists:
                assert initial_frozen_prefix_count == 8, (
                    "existing receipt with an incomplete freeze is invalid; "
                    "a new receipt version is required")

        validate_draft_flags_and_sources(exact8)
        incident_source_contract = derive_inherited_incident_source_contract(
            exact8)
        pep552 = validate_pep552(exact8)
        assert_exact_three_target_v13_pyc(resolver)
        v12_anchors, v11_namespace, v12_namespace = validate_v12_anchor(
            resolver)
        assert {item.initial.st_dev for item in v12_anchors} == {
            item.initial.st_dev for item in exact8.values()}
        assert {fd_mount_id(item.fd) for item in v12_anchors} == {
            directories.runtime.mount_id}
        assert directories.runtime.mount_id == directories.output.mount_id
        assert_v13_unpublished_and_runtime_absent(resolver)
        directories.replay()

        if command == "PREFLIGHT":
            for item in exact8.values():
                state, _raw = item.replay(require_frozen=False)
                assert full_file_identity(state) == full_file_identity(item.initial)
            for item in v12_anchors:
                state, _raw = item.replay(require_frozen=True)
                assert full_file_identity(state) == full_file_identity(item.initial)
            assert v11_namespace is not None and v12_namespace is not None
            v11_namespace.replay()
            v12_namespace.replay()
            assert_exact_three_target_v13_pyc(resolver)
            assert_v13_unpublished_and_runtime_absent(resolver)
            assert derive_inherited_incident_source_contract(exact8) == \
                incident_source_contract
            assert not resolver.exists(RECEIPT_REL)
            assert preflight_output_snapshot is not None
            assert stable_directory_snapshot(directories.output) == \
                preflight_output_snapshot
            directories.replay()
            result = {
                "status": (
                    "PREFLIGHT_V13_PREPUBLICATION_PYC_CONTAMINATION_"
                    "EXACT8_READ_ONLY_PASS_UNDER_OFFICIAL_LOCK"),
                "held_unique_exact8": 8,
                "live_successor_required_incident_count": 6,
                "supplemental_tooling_count": 2,
                "all_regular_0664_nlink1_unique_inode_same_dev": True,
                "pep552_headers_match_pinned_sources": True,
                "three_source_inherited_incident_exact10_ast_contract_pass": True,
                "inherited_incident_exact10_canonical_sha256":
                    INHERITED_INCIDENT_EXACT10_CANONICAL_SHA256,
                "v12_exact10_rejection_and_namespace_terminally_replayed": True,
                "v13_json_manifest_outer_and_runtime_absent": True,
                "v13_final_flags_false_runtime_disabled_true_by_ast": True,
                "target_validation_was_ast_and_in_memory_compile_only": True,
                "no_chmod_write_import_execution_or_py_compile_performed": True,
            }
        else:
            recovered_prefix_refchmod_count = 0
            recovered_prefix_file_fsync_count = 0
            newly_frozen_suffix_fchmod_count = 0
            if not receipt_exists:
                verify_otmpfile_linkat_capability(resolver)
                assert not resolver.exists(RECEIPT_REL)
                assert_v13_unpublished_and_runtime_absent(resolver)
                directories.replay()
                for index, pin in enumerate(EVIDENCE_EXACT8):
                    exact8[pin["path"]].freeze()
                    if index < initial_frozen_prefix_count:
                        recovered_prefix_file_fsync_count += 1
                    else:
                        newly_frozen_suffix_fchmod_count += 1
                assert recovered_prefix_refchmod_count == 0
                assert recovered_prefix_file_fsync_count == \
                    initial_frozen_prefix_count
                assert newly_frozen_suffix_fchmod_count == \
                    8 - initial_frozen_prefix_count
                directories.fsync_all()
            else:
                assert initial_frozen_prefix_count == 8
                assert recovered_prefix_refchmod_count == 0
                assert recovered_prefix_file_fsync_count == 0
                assert newly_frozen_suffix_fchmod_count == 0

            frozen_replay = {
                pin["path"]: exact8[pin["path"]].replay(require_frozen=True)
                for pin in EVIDENCE_EXACT8}
            assert len({(state.st_dev, state.st_ino)
                        for state, _raw in frozen_replay.values()}) == 8
            assert len({state.st_dev for state, _raw in frozen_replay.values()}) == 1
            validate_draft_flags_and_sources(exact8)
            frozen_incident_source_contract = \
                derive_inherited_incident_source_contract(exact8)
            assert frozen_incident_source_contract == incident_source_contract
            pep552 = validate_pep552(exact8)
            assert_exact_three_target_v13_pyc(resolver)
            assert_v13_unpublished_and_runtime_absent(resolver)
            for item in v12_anchors:
                state, _raw = item.replay(require_frozen=True)
                assert full_file_identity(state) == full_file_identity(item.initial)
            assert v11_namespace is not None and v12_namespace is not None
            v11_namespace.replay()
            v12_namespace.replay()
            directories.replay()

            persisted = [
                persisted_evidence(pin, frozen_replay[pin["path"]][0])
                for pin in EVIDENCE_EXACT8]
            assert incident_source_contract is not None
            receipt_value = make_receipt(
                persisted, pep552, incident_source_contract)
            receipt_raw = canonical(receipt_value) + b"\n"
            frozen_max_ns = max(
                max(state.st_mtime_ns, state.st_ctime_ns)
                for state, _raw in frozen_replay.values())
            if receipt_exists:
                try:
                    receipt = HeldReceipt.open_existing(
                        resolver, receipt_raw, receipt_value["object_sha256"])
                except BaseException as error:
                    raise RuntimeError(
                        "EXISTING_RECEIPT_IS_NOT_THE_COMPLETE_CANONICAL_"
                        "EXPECTED_OBJECT__NEW_RECEIPT_VERSION_REQUIRED") from error
                directories.replay()
                directories.fsync_receipt_boundaries()
                directories.replay()
                recovery = True
            else:
                receipt = HeldReceipt.publish_anonymous(
                    resolver, receipt_raw, receipt_value["object_sha256"],
                    frozen_max_ns)
                directories.fsync_all()
                recovery = False

            final_replay = {
                pin["path"]: exact8[pin["path"]].replay(require_frozen=True)
                for pin in EVIDENCE_EXACT8}
            receipt_state, final_receipt_raw = receipt.replay()
            assert final_receipt_raw == receipt_raw
            assert full_file_identity(receipt_state) == \
                full_file_identity(receipt.initial)
            for rel, (final_state, _raw) in final_replay.items():
                assert full_file_identity(final_state) == full_file_identity(
                    frozen_replay[rel][0])
            exact9_ids = {
                (state.st_dev, state.st_ino)
                for state, _raw in final_replay.values()}
            exact9_ids.add((receipt_state.st_dev, receipt_state.st_ino))
            assert len(exact9_ids) == 9
            assert len({dev for dev, _ino in exact9_ids}) == 1
            assert frozen_max_ns < min(
                receipt_state.st_mtime_ns, receipt_state.st_ctime_ns)
            assert_exact_three_target_v13_pyc(resolver)
            assert_v13_unpublished_and_runtime_absent(resolver)
            terminal_incident_source_contract = \
                derive_inherited_incident_source_contract(exact8)
            assert terminal_incident_source_contract == incident_source_contract
            assert receipt_value[
                "frozen_v13_inherited_incident_authority_exact10_source_contract"
            ] == terminal_incident_source_contract
            for item in v12_anchors:
                state, _raw = item.replay(require_frozen=True)
                assert full_file_identity(state) == full_file_identity(item.initial)
            v11_namespace.replay()
            v12_namespace.replay()
            directories.replay()
            if not recovery:
                directories.fsync_all()
                directories.replay()
            result = {
                "status": (
                    ("TERMINAL_RECOVERY_" if recovery else "TERMINAL_") +
                    "EXACT9_REPLAY_PASS__V13_PREPUBLICATION_PYC_CONTAMINATION_"
                    "FROZEN_REJECTED__V14_ONLY"),
                "receipt_path": RECEIPT_REL,
                "receipt_file_sha256": receipt.file_sha,
                "receipt_object_sha256": receipt.object_sha,
                "frozen_exact8_unique_files": 8,
                "terminal_exact9_unique_files": 9,
                "existing_exact_receipt_terminal_recovery": recovery,
                "initial_frozen_prefix_count": initial_frozen_prefix_count,
                "recovered_prefix_refchmod_count":
                    recovered_prefix_refchmod_count,
                "recovered_prefix_file_fsync_count":
                    recovered_prefix_file_fsync_count,
                "newly_frozen_suffix_fchmod_count":
                    newly_frozen_suffix_fchmod_count,
                "same_st_dev_and_mount_id": True,
                "three_source_inherited_incident_exact10_terminal_ast_replay":
                    True,
                "v14_inherited_incident_exact16_bound_by_receipt": True,
                "v13_runtime_and_positive_publication_surface_count": 0,
                "D02_unlock": False,
                "D02_started": False,
                "D02_formal_pending_task_count": 33638,
            }
            if recovery:
                result["existing_receipt_recovery_content_write_or_chmod"] = False
                result[
                    "existing_receipt_recovery_output_runtime_root_directory_"
                    "fsync_performed"] = True

        # No PASS bytes may be emitted until all authority replays, closes,
        # held-directory path checks, and official unlock have succeeded.
        assert result is not None
        directories.replay()
        if receipt is not None:
            receipt.close()
            receipt = None
        if v12_namespace is not None:
            v12_namespace.close()
            v12_namespace = None
        if v11_namespace is not None:
            v11_namespace.close()
            v11_namespace = None
        for item in v12_anchors:
            item.close()
        v12_anchors.clear()
        for item in exact8.values():
            item.close()
        exact8.clear()
        directories.replay()
        fcntl.flock(directories.runtime.fd, fcntl.LOCK_UN)
        locked = False
        directories.close()
        cleanup_complete = True
    finally:
        if not cleanup_complete:
            if receipt is not None:
                receipt.close()
            if v12_namespace is not None:
                v12_namespace.close()
            if v11_namespace is not None:
                v11_namespace.close()
            for item in v12_anchors:
                item.close()
            for item in exact8.values():
                item.close()
            if locked:
                try:
                    fcntl.flock(directories.runtime.fd, fcntl.LOCK_UN)
                except OSError:
                    pass
            directories.close()
    assert result is not None and cleanup_complete
    print(canonical(result).decode("ascii"), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
