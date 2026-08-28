#!/usr/bin/env python3
"""Fail-closed builder/checker for the additive C30a audit closure.

This file deliberately implements a non-self-referential five-layer chain::

    payload manifest
      -> cold/full-trace receipt
      -> outer verification
      -> root manifest
      -> terminal checker receipt

The payload manifest pins code and raw evidence, but never itself or any later
receipt.  The cold receipt pins the payload.  The outer verification pins the
payload and cold receipt.  The two-member root manifest pins the payload
manifest and outer verification.  A terminal receipt is created only after an
externally supplied root-manifest SHA256 has been checked.

Every mode's first workspace evidence operation is validation of the original
C30a manifest SHA, exact 13-member map, and all 13 member hashes.  Check modes
then validate the supplemental manifest exact map before reading supplemental
evidence.  Files are captured once with O_NOFOLLOW and pre/open/post identity
and metadata checks; subsequent semantic checks use the captured bytes.

The current repository intentionally lacks several mandatory final artifacts.
Consequently this checker is a fail-closed skeleton: it cannot mint a receipt
or print a release PASS until both true-seed candidates, both independent
verifier replays, persistent ten-attack evidence, and full ``strace -e
trace=all`` audits have been sealed.  A selective seed-1 trace may be retained
only as auxiliary evidence.  It is never authorization evidence.

No mode can add mathematical credit.  The only permitted conclusion is 160
original whole-origin exclusions, supplemental credit zero, Source-W
``252 -> 92``; ``252 -> 90`` is forbidden, D02 is blocked, and CM2 remains
``NO-GO_FOR_CLAIM``.
"""

from __future__ import annotations

import argparse
import ast
import ctypes
import hashlib
import json
import os
import re
import shlex
import stat
import sys
import types
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


sys.dont_write_bytecode = True

# Lexical paths only.  ``abspath`` does not read the filesystem; do not
# resolve/stat anything before validate_base().
SCRIPT = Path(os.path.abspath(__file__))
DELIVERABLES = SCRIPT.parent
WORKSPACE = DELIVERABLES.parent

BASE_PREFIX = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion"
)
BASE_MANIFEST_REL = "deliverables/" + BASE_PREFIX + "_manifest.sha256"
BASE_MANIFEST_SHA256 = (
    "0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc"
)
BASE_MEMBERS = {
    "cm2_round306c30a_python_flint_requirements.lock":
        "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c",
    "cm2_round306c30a_python_flint_runtime_lock.json":
        "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79",
    (
        "cm2_round306c30a_runtime/"
        "python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64."
        "manylinux_2_17_x86_64.whl"
    ): "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76",
    BASE_PREFIX + "_attack_harness.py":
        "debdb1ac9d3b840660600cec66dd2b6b1d45eb5847d366c989a652f893bb3c17",
    BASE_PREFIX + "_cold_replay.md":
        "6bac45a8150603370380afca729220fc2c6da9e3d3580ea3b535b9d2b37a94c5",
    BASE_PREFIX + "_independent_verifier.py":
        "5af75a97e9c306cc47a514e4c87ae875a8388bb75d9274d106b64e2ceee87c7c",
    BASE_PREFIX + "_producer.py":
        "41a3f11c3e44bdbbfcf95edf88902669365186e6fb6394aaee15a6846dc91714",
    BASE_PREFIX + "_report.md":
        "e2811b8c9a676e08e1e3014a10ca693ee651f4d143b38540a1ac53195f4b8562",
    BASE_PREFIX + "_verification.json":
        "f02f7e3144541284819947c549ce91d8f1d6e9df24c0bdb4b981077f1e358d07",
    "cm2_round306c30a_sealed/" + BASE_PREFIX + "_cell_ledger.jsonl.gz":
        "c4c0061a08983471428b2e5113aff60bbeccc67530cac691658a6bbad1ce9904",
    (
        "cm2_round306c30a_sealed/" + BASE_PREFIX
        + "_inherited_h_obstruction_ledger.jsonl.gz"
    ): "f86c6c3d90a4a87c7d4366b86a0e8119d019cbf86f5b5ab781140605ddc1e80e",
    "cm2_round306c30a_sealed/" + BASE_PREFIX + "_result.json":
        "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48",
    (
        "cm2_round306c30a_sealed/" + BASE_PREFIX
        + "_whole_origin_ledger.jsonl.gz"
    ): "778995522629a362183159420860b65d60c8719bc1453c4fc2657e8e8fba9649",
}

C29_PREFIX = (
    "cm2_round306c29_source_g_maximal_component_official_key_fibre_"
    "exhaustion_and_global_disposition"
)
C29_MANIFEST_REL = "deliverables/" + C29_PREFIX + "_manifest.sha256"
C29_MANIFEST_SHA256 = (
    "6ef42986bd1fd6b7ae99a57aebb0f5445d107e5cffe1543703a1dfb1fede6aa0"
)
C29_RESULT_OBJECT_SHA256 = (
    "184b2eef5cdcfe09616efc7e66a22445a4cdb4d06b2972674154fd823307ec1a"
)
PROTOCOL_SHA256 = (
    "72e6e24b4f625ba9a8f9112950a07a22f5521f935acef0f3c1650f654995cc4e"
)
CONTROLLED_LAUNCHER_SHA256 = (
    "1437e60dd0b49e213b50615a3d5a7991c5bee1199edfda8b7495424d35a767cf"
)
CONTROLLED_COMPARATOR_SHA256 = (
    "41319b2371fd90dcc182d08f2e68d552302daacde59988303810258639073603"
)
CONTROLLED_PROVENANCE_SCHEMA = (
    "cm2.round306c30a.controlled-hash-seed-replay.v1"
)
CONTROLLED_COMPARATOR_SCHEMA = (
    "cm2.round306c30a.controlled-dual-seed-release-receipt.v1"
)

SUP_PREFIX = "cm2_round306c30a_supplemental_audit_closure"
SEALED_REL = "deliverables/" + SUP_PREFIX + "_sealed"
PAYLOAD_MANIFEST_REL = "deliverables/" + SUP_PREFIX + "_payload_manifest.sha256"
COLD_RECEIPT_REL = "deliverables/" + SUP_PREFIX + "_cold_replay_receipt.json"
OUTER_VERIFICATION_REL = "deliverables/" + SUP_PREFIX + "_outer_verification.json"
ROOT_MANIFEST_REL = "deliverables/" + SUP_PREFIX + "_root_manifest.sha256"
TERMINAL_RECEIPT_REL = "deliverables/" + SUP_PREFIX + "_terminal_checker_receipt.json"

OUTPUT_NAMES = {
    BASE_PREFIX + "_cell_ledger.jsonl.gz",
    BASE_PREFIX + "_whole_origin_ledger.jsonl.gz",
    BASE_PREFIX + "_inherited_h_obstruction_ledger.jsonl.gz",
    BASE_PREFIX + "_result.json",
}
OUTPUT_HASHES = {
    BASE_PREFIX + "_cell_ledger.jsonl.gz":
        "c4c0061a08983471428b2e5113aff60bbeccc67530cac691658a6bbad1ce9904",
    BASE_PREFIX + "_whole_origin_ledger.jsonl.gz":
        "778995522629a362183159420860b65d60c8719bc1453c4fc2657e8e8fba9649",
    BASE_PREFIX + "_inherited_h_obstruction_ledger.jsonl.gz":
        "f86c6c3d90a4a87c7d4366b86a0e8119d019cbf86f5b5ab781140605ddc1e80e",
    BASE_PREFIX + "_result.json":
        "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48",
}
RESULT_OBJECT_SHA256 = (
    "32c449bc9af41a22ab5468d194431d14fadf5bc95b30067d639f9e4443538e09"
)
SEEDS = ("30630071", "30630929")
SEED_PROBES = {
    "30630071": 8841297538927089933,
    "30630929": 889641737497572634,
}
SUPERSEDED_V1_PINS = {
    "provenance": "3acfc9d15daf39ca328cbc0a87910e87fe0b2e2144e9b9756b5dc5cef88b3d3f",
    "stderr": "addac86a8584f1a097ddf37a779e30f2c573657e7323c9494dc0429b4504f7bf",
    "stdout": "ca33e31584f0c35708936f59e721de8185139ffda918731f4112d332e0e78a0b",
    "time": "37e3ddae3a809c6dca70e926f9f2ce669146c28813a35ba6dafdbee56c55b16c",
    "trace": "8421884d2dd3f7763dc666eeeac5d336062f75f9f677ea70a747ee7f8eb99314",
}
ATTACK_NAMES = (
    "promoted_origin_count",
    "remaining_origin_count",
    "D02_illegal_clear",
    "CM2_illegal_go",
    "child_volume_credit",
    "input_pin_retarget",
    "cell_ledger_full_reclosure",
    "origin_ledger_full_reclosure",
    "origin_order_full_reclosure",
    "held_to_promoted_162_overclaim_full_reclosure",
)
NETWORK_SYSCALLS = {
    "accept", "accept4", "bind", "connect", "getpeername", "getsockname",
    "getsockopt", "listen", "recv", "recvfrom", "recvmmsg", "recvmsg",
    "send", "sendmmsg", "sendmsg", "sendto", "setsockopt", "shutdown",
    "socket", "socketcall", "socketpair",
}
BASE_SNAPSHOT_SCHEMA = (
    "cm2.round306c30a.supplemental-base-snapshot.v1"
)
BASE_SNAPSHOT_PHASES = {
    "pre": (
        "RETROSPECTIVE_CURRENT_BASE_IDENTITY_WITH_RETAINED_PRECHECK"
    ),
    "post": (
        "CURRENT_BASE_IDENTITY_WITH_RETAINED_POSTCHECK"
    ),
}
TIMED_EXIT_SCHEMA = (
    "cm2.round306c30a.supplemental-timed-process-exit.v1"
)
ANALYZER_CONTRACT_SOURCE_PREFIX = (
    "c30a-release-checker-reconstructed-contract:"
)

SHA_LINE = re.compile(r"([0-9a-f]{64})  ([^\x00\r\n]+)\n")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
MAX_FILE = 2 * 1024 * 1024 * 1024
MAX_RETAIN = 64 * 1024 * 1024


class Reject(RuntimeError):
    """A release precondition failed closed."""


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_relpath(value: str) -> PurePosixPath:
    require(type(value) is str, "path string")
    pure = PurePosixPath(value)
    require(
        not pure.is_absolute()
        and pure.as_posix() == value
        and all(part not in {"", ".", ".."} for part in pure.parts),
        "safe canonical relative path:" + str(value),
    )
    return pure


@dataclass(frozen=True)
class Capture:
    relpath: str
    sha256: str
    size: int
    dev: int
    ino: int
    mtime_ns: int
    ctime_ns: int
    raw: bytes | None
    execve_lines: tuple[bytes, ...] = ()


def capture_once(relpath: str, *, retain: bool = False) -> Capture:
    pure = safe_relpath(relpath)
    absolute = Path(os.path.abspath(os.fspath(WORKSPACE / pure)))
    root = Path(os.path.abspath(os.fspath(WORKSPACE)))
    require(absolute.is_relative_to(root) and absolute != root,
            "workspace containment:" + relpath)
    before = absolute.lstat()
    require(
        stat.S_ISREG(before.st_mode)
        and not absolute.is_symlink()
        and before.st_nlink == 1
        and 0 <= before.st_size <= MAX_FILE,
        "regular singleton bounded file:" + relpath,
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    chunks: list[bytes] | None = [] if retain else None
    collect_execve = (
        relpath.endswith(".trace.raw")
        or "trace-all" in PurePosixPath(relpath).name
    )
    execve_lines: list[bytes] = []
    trace_tail = b""
    digest = hashlib.sha256()
    try:
        opened = os.fstat(descriptor)
        identity = (
            before.st_dev, before.st_ino, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns,
        )
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and (
                opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns, opened.st_ctime_ns,
            ) == identity,
            "pre/open race:" + relpath,
        )
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            require(bool(block), "short read:" + relpath)
            digest.update(block)
            if chunks is not None:
                require(opened.st_size <= MAX_RETAIN,
                        "retained file too large:" + relpath)
                chunks.append(block)
            if collect_execve:
                combined = trace_tail + block
                split = combined.splitlines(keepends=True)
                trace_tail = b""
                if split and not split[-1].endswith((b"\n", b"\r")):
                    trace_tail = split.pop()
                for line in split:
                    if b"execve(" in line:
                        require(len(line) <= 128 * 1024,
                                "bounded execve trace line:" + relpath)
                        execve_lines.append(line)
                        require(len(execve_lines) <= 256,
                                "bounded execve trace census:" + relpath)
            remaining -= len(block)
        if collect_execve and trace_tail and b"execve(" in trace_tail:
            require(len(trace_tail) <= 128 * 1024,
                    "bounded final execve trace line:" + relpath)
            execve_lines.append(trace_tail)
        require(not os.read(descriptor, 1), "growing file:" + relpath)
        final = os.fstat(descriptor)
        require(
            (
                final.st_dev, final.st_ino, final.st_size,
                final.st_mtime_ns, final.st_ctime_ns,
            ) == identity,
            "open/final race:" + relpath,
        )
    finally:
        os.close(descriptor)
    after = absolute.lstat()
    require(
        (
            after.st_dev, after.st_ino, after.st_size,
            after.st_mtime_ns, after.st_ctime_ns,
        ) == (
            before.st_dev, before.st_ino, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns,
        )
        and stat.S_ISREG(after.st_mode)
        and after.st_nlink == 1
        and not absolute.is_symlink(),
        "path post-read race:" + relpath,
    )
    return Capture(
        relpath=relpath,
        sha256=digest.hexdigest(),
        size=before.st_size,
        dev=before.st_dev,
        ino=before.st_ino,
        mtime_ns=before.st_mtime_ns,
        ctime_ns=before.st_ctime_ns,
        raw=None if chunks is None else b"".join(chunks),
        execve_lines=tuple(execve_lines),
    )


def require_captures_unchanged(captures: dict[str, Capture]) -> None:
    """Metadata/identity post-check without a second content read."""

    for relpath, captured in captures.items():
        status = (WORKSPACE / relpath).lstat()
        require(
            stat.S_ISREG(status.st_mode)
            and status.st_nlink == 1
            and not (WORKSPACE / relpath).is_symlink()
            and (
                status.st_dev, status.st_ino, status.st_size,
                status.st_mtime_ns, status.st_ctime_ns,
            ) == (
                captured.dev, captured.ino, captured.size,
                captured.mtime_ns, captured.ctime_ns,
            ),
            "post-validation capture changed:" + relpath,
        )


def strict_json(raw: bytes, label: str, *, newline: bool = True) -> dict[str, Any]:
    require(raw is not None and b"\x00" not in raw, "JSON bytes:" + label)
    body = raw[:-1] if newline and raw.endswith(b"\n") else raw
    if newline:
        require(raw.endswith(b"\n") and raw.count(b"\n") == 1,
                "one-line JSON:" + label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(type(key) is str and key not in output,
                    "unique JSON keys:" + label)
            output[key] = value
        return output

    def reject_constant(token: str) -> None:
        raise ValueError(token)

    try:
        value = json.loads(
            body.decode("utf-8", "strict"),
            object_pairs_hook=unique,
            parse_constant=reject_constant,
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    require(type(value) is dict and canonical(value) == body,
            "canonical JSON object:" + label)
    return value


def parse_manifest(raw: bytes, label: str) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as error:
        raise Reject("ASCII manifest:" + label) from error
    cursor = 0
    members: dict[str, str] = {}
    for match in SHA_LINE.finditer(text):
        require(match.start() == cursor, "canonical manifest lines:" + label)
        cursor = match.end()
        digest, name = match.groups()
        safe_relpath(name)
        require(name not in members, "unique manifest member:" + name)
        members[name] = digest
    require(cursor == len(text) and bool(members), "complete manifest:" + label)
    return members


def retain_member(relpath: str) -> bool:
    name = PurePosixPath(relpath).name
    return (
        name.endswith(".json")
        or name.endswith(".stdout")
        or name.endswith(".stdout.raw")
        or name.endswith(".stderr.raw")
        or name.endswith(".sha256")
        or name.endswith(".exit")
        or name.endswith(".time.txt")
        or name.endswith(".py")
    )


def validate_base() -> dict[str, Capture]:
    """The first workspace evidence operation in every mode."""

    manifest = capture_once(BASE_MANIFEST_REL, retain=True)
    require(manifest.sha256 == BASE_MANIFEST_SHA256,
            "base manifest trust-root SHA256")
    require(manifest.raw is not None, "base manifest retained")
    parsed = parse_manifest(manifest.raw, "base")
    require(parsed == BASE_MEMBERS and len(parsed) == 13,
            "base manifest exact 13-member map")
    captures = {BASE_MANIFEST_REL: manifest}
    for name, expected in parsed.items():
        relpath = "deliverables/" + name
        item = capture_once(
            relpath,
            retain=name.endswith("_result.json"),
        )
        require(item.sha256 == expected, "base member SHA256:" + name)
        captures[relpath] = item
    result_rel = (
        "deliverables/cm2_round306c30a_sealed/" + BASE_PREFIX + "_result.json"
    )
    result_cap = captures[result_rel]
    require(result_cap.raw is not None, "base result retained")
    result = strict_json(result_cap.raw, "base result", newline=False)
    transition = result["source_W_ledger_transition"]
    require(
        result["result_sha256"] == RESULT_OBJECT_SHA256
        and transition["before"]["remaining"] == 252
        and transition["after"]["remaining"] == 92
        and transition["new_whole_origin_exclusion_credit"] == 160
        and result["whole_origin_census"]["Round306C30A_new_promoted"] == 160
        and result["whole_origin_census"]["Round306C30A_inherited_H_held"] == 2
        and result["strict_nonpromotion"]["D02"]
        == "BLOCKED_BY_92_REMAINING_SOURCE_W_ORIGINS"
        and result["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "base fixed 160-credit 252-to-92 boundary",
    )
    return captures


def payload_static_members() -> set[str]:
    return {
        BASE_MANIFEST_REL,
        C29_MANIFEST_REL,
        "deliverables/cm2_round306c30a_python_flint_fresh_runtime_attestor.py",
        "deliverables/cm2_round306c30a_python_flint_fresh_runtime_rebuild.py",
        "deliverables/cm2_round306c30a_python_flint_fresh_runtime_completion.json",
        "deliverables/cm2_round306c30a_python_flint_fresh_runtime_rebuild_report.md",
        "deliverables/" + SUP_PREFIX + "_controlled_replay_launcher.py",
        "deliverables/" + SUP_PREFIX + "_controlled_seed_comparator.py",
        "deliverables/" + SUP_PREFIX + "_coherent_attack_harness.py",
        "deliverables/" + SUP_PREFIX + "_independent_verifier.py",
        "deliverables/" + SUP_PREFIX + "_protocol.md",
        "deliverables/" + SUP_PREFIX + "_strace_analyzer.py",
        "deliverables/" + SUP_PREFIX + "_release_checker.py",
    }


def sealed_required_files() -> set[str]:
    files = {
        "00_assembly_source_map.json",
        "00_base_manifest_pre.stdout",
        "00_base_manifest_pre.stderr.raw",
        "00_base_manifest_pre.exit.json",
        "00_base_manifest_pre.manifest.sha256",
        "00_base_manifest_pre.snapshot.json",
        "01_preflight.stdout.json",
        "01_preflight.stderr.raw",
        "01_preflight.exit.json",
        "05_controlled_seed_comparison.sha256",
        "05_controlled_seed_comparison.stdout",
        "05_controlled_seed_comparison.stderr.raw",
        "05_controlled_seed_comparison.exit.json",
        "05_controlled_seed_comparison.time.txt",
        "08_attacks.harness.stdout.json",
        "08_attacks.harness.stderr.raw",
        "08_attacks.harness.exit.json",
        "08_attacks.harness.time.txt",
        "09_base_manifest_post.stdout",
        "09_base_manifest_post.stderr.raw",
        "09_base_manifest_post.exit.json",
        "09_base_manifest_post.manifest.sha256",
        "09_base_manifest_post.snapshot.json",
        "10_invocations.json",
        "11_trace_audit.json",
        "12_closure_result.json",
    }
    fresh = {
        "completion.json",
        "rebuild_descriptor.json",
        "rebuild_invocation.stdout.json",
        "rebuild_invocation.stderr.raw",
        "rebuild_invocation.time.txt",
        "venv_create.stage.json",
        "venv_create.stdout.raw",
        "venv_create.stderr.raw",
        "offline_install.stage.json",
        "offline_install.stdout.raw",
        "offline_install.stderr.raw",
        "freeze.stage.json",
        "freeze.stdout",
        "freeze.stderr.raw",
        "attestation.stage.json",
        "attestation.stdout.json",
        "attestation.stderr.raw",
        "attestation_recheck.stdout.json",
        "attestation_recheck.stderr.raw",
        "attestation_recheck.time.txt",
    }
    files.update("02_fresh_runtime/" + name for name in fresh)
    c29 = {
        "manifest_check.stdout",
        "verifier.stdout.json",
        "verifier.stderr.raw",
        "verifier.exit.json",
        "verifier.time.txt",
    }
    files.update("02_c29/" + name for name in c29)
    for ordinal, seed in enumerate(SEEDS, start=3):
        tag = f"{ordinal:02d}_seed{seed}"
        files.update({
            tag + ".provenance.json",
            tag + ".producer.stdout.json",
            tag + ".producer.stderr.raw",
            tag + ".producer.exit.json",
            tag + ".producer.time.txt",
            tag + ".producer.trace.raw",
        })
        files.update(tag + ".candidate/" + name for name in OUTPUT_NAMES)
    for ordinal, seed in enumerate(SEEDS, start=6):
        tag = f"{ordinal:02d}_seed{seed}.verifier"
        files.update({
            tag + ".manifest_pre.stdout",
            tag + ".stdout.json",
            tag + ".stderr.raw",
            tag + ".exit.json",
            tag + ".time.txt",
            tag + ".trace.raw",
            tag + ".manifest_post.stdout",
        })
    files.add("08_attacks/attack_summary.json")
    for ordinal, name in enumerate(ATTACK_NAMES):
        root = f"08_attacks/{ordinal:02d}_{name}"
        files.update({
            root + "/attack_descriptor.json",
            root + "/verifier.stdout.raw",
            root + "/verifier.stderr.raw",
            root + "/verifier.exit.json",
        })
        files.update(root + "/candidate/" + item for item in OUTPUT_NAMES)
    return files


def expected_payload_paths() -> set[str]:
    return payload_static_members() | {
        SEALED_REL + "/" + name for name in sealed_required_files()
    }


def expected_tree_directories(files: set[str]) -> set[str]:
    directories = {SEALED_REL}
    prefix = SEALED_REL + "/"
    for relpath in files:
        require(relpath.startswith(prefix), "sealed path prefix")
        pure = PurePosixPath(relpath)
        parent = pure.parent
        while parent.as_posix().startswith(SEALED_REL):
            directories.add(parent.as_posix())
            if parent.as_posix() == SEALED_REL:
                break
            parent = parent.parent
    return directories


def scan_exact_sealed_tree(expected_files: set[str]) -> None:
    expected_dirs = expected_tree_directories(expected_files)
    actual_files: set[str] = set()
    actual_dirs: set[str] = set()
    pending = [SEALED_REL]
    while pending:
        rel_dir = pending.pop()
        safe_relpath(rel_dir)
        absolute = WORKSPACE / rel_dir
        before = absolute.lstat()
        require(
            stat.S_ISDIR(before.st_mode)
            and not absolute.is_symlink()
            and before.st_nlink >= 2,
            "sealed directory singleton boundary:" + rel_dir,
        )
        actual_dirs.add(rel_dir)
        with os.scandir(absolute) as iterator:
            entries = sorted(iterator, key=lambda item: os.fsencode(item.name))
            for entry in entries:
                require(entry.name not in {"", ".", ".."}, "safe tree entry")
                child = rel_dir + "/" + entry.name
                require(not entry.is_symlink(), "no sealed symlink:" + child)
                if entry.is_dir(follow_symlinks=False):
                    pending.append(child)
                elif entry.is_file(follow_symlinks=False):
                    actual_files.add(child)
                else:
                    raise Reject("sealed special entry:" + child)
        after = absolute.lstat()
        require(
            (
                after.st_dev, after.st_ino, after.st_mtime_ns,
                after.st_ctime_ns,
            ) == (
                before.st_dev, before.st_ino, before.st_mtime_ns,
                before.st_ctime_ns,
            ),
            "sealed directory race:" + rel_dir,
        )
    require(actual_files == expected_files,
            "sealed exact file map")
    require(actual_dirs == expected_dirs,
            "sealed exact directory map")


def scan_assembly_tree(root: Path, expected_relative_files: set[str]) -> None:
    """Reject any assembly-tree extra, missing, symlink, or special entry."""

    expected_dirs = {"."}
    for name in expected_relative_files:
        parent = PurePosixPath(name).parent
        while parent.as_posix() != ".":
            expected_dirs.add(parent.as_posix())
            parent = parent.parent
    actual_files: set[str] = set()
    actual_dirs = {"."}
    pending: list[tuple[Path, str]] = [(root, ".")]
    while pending:
        directory, rel_dir = pending.pop()
        before = directory.lstat()
        require(stat.S_ISDIR(before.st_mode) and not directory.is_symlink(),
                "assembly directory boundary:" + rel_dir)
        with os.scandir(directory) as iterator:
            entries = sorted(iterator, key=lambda item: os.fsencode(item.name))
            for entry in entries:
                child_rel = (
                    entry.name if rel_dir == "." else rel_dir + "/" + entry.name
                )
                require(not entry.is_symlink(),
                        "assembly no symlink:" + child_rel)
                if entry.is_dir(follow_symlinks=False):
                    actual_dirs.add(child_rel)
                    pending.append((directory / entry.name, child_rel))
                elif entry.is_file(follow_symlinks=False):
                    actual_files.add(child_rel)
                else:
                    raise Reject("assembly special entry:" + child_rel)
        after = directory.lstat()
        require(
            (after.st_dev, after.st_ino, after.st_mtime_ns, after.st_ctime_ns)
            == (before.st_dev, before.st_ino, before.st_mtime_ns, before.st_ctime_ns),
            "assembly directory race:" + rel_dir,
        )
    require(actual_files == expected_relative_files,
            "assembly exact file map")
    require(actual_dirs == expected_dirs,
            "assembly exact directory map")


def capture_payload_from_manifest(
    manifest_rel: str,
    expected_sha256: str,
    base: dict[str, Capture],
    *,
    manifest_capture: Capture | None = None,
) -> tuple[Capture, dict[str, Capture], dict[str, str]]:
    require(HEX64.fullmatch(expected_sha256) is not None
            and expected_sha256 != "0" * 64,
            "externally pinned payload manifest SHA256")
    manifest = (
        capture_once(manifest_rel, retain=True)
        if manifest_capture is None else manifest_capture
    )
    require(manifest.relpath == manifest_rel and manifest.raw is not None,
            "pre-captured payload manifest identity")
    require(manifest.sha256 == expected_sha256,
            "payload manifest external SHA256")
    require(manifest.raw is not None, "payload manifest retained")
    members = parse_manifest(manifest.raw, "supplemental payload")
    expected = expected_payload_paths()
    require(set(members) == expected,
            "supplemental payload exact member map")
    sealed_paths = {path for path in expected if path.startswith(SEALED_REL + "/")}
    scan_exact_sealed_tree(sealed_paths)
    captures: dict[str, Capture] = {}
    for relpath in sorted(members, key=os.fsencode):
        if relpath in base:
            item = base[relpath]
        else:
            item = capture_once(relpath, retain=retain_member(relpath))
        require(item.sha256 == members[relpath],
                "payload member SHA256:" + relpath)
        captures[relpath] = item
    return manifest, captures, members


def capture_staging_payload(base: dict[str, Capture]) -> dict[str, Capture]:
    paths = expected_payload_paths()
    sealed_paths = {path for path in paths if path.startswith(SEALED_REL + "/")}
    scan_exact_sealed_tree(sealed_paths)
    captures: dict[str, Capture] = {}
    for relpath in sorted(paths, key=os.fsencode):
        if relpath in base:
            captures[relpath] = base[relpath]
        else:
            captures[relpath] = capture_once(
                relpath, retain=retain_member(relpath)
            )
    return captures


def raw_of(captures: dict[str, Capture], sealed_name: str) -> bytes:
    relpath = SEALED_REL + "/" + sealed_name
    item = captures[relpath]
    require(item.raw is not None, "retained semantic evidence:" + sealed_name)
    return item.raw


def json_of(
    captures: dict[str, Capture],
    sealed_name: str,
    *,
    newline: bool = True,
) -> dict[str, Any]:
    return strict_json(raw_of(captures, sealed_name), sealed_name, newline=newline)


def require_exit_zero(value: dict[str, Any], label: str) -> None:
    code = value.get("exit_code", value.get("returncode"))
    require(type(code) is int and code == 0, "zero exit:" + label)


def require_empty(captures: dict[str, Capture], sealed_name: str) -> None:
    require(captures[SEALED_REL + "/" + sealed_name].size == 0,
            "empty file:" + sealed_name)


def expected_manifest_stdout(manifest_raw: bytes) -> bytes:
    members = parse_manifest(manifest_raw, "manifest stdout source")
    return b"".join(
        name.encode("ascii") + b": OK\n" for name in members
    )


def parse_gnu_time(raw: bytes, label: str) -> tuple[list[str], int]:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise Reject("GNU time UTF-8:" + label) from error
    commands = re.findall(
        r'^\s*Command being timed: "(.*)"\s*$', text, re.MULTILINE
    )
    signals = re.findall(
        r"^\s*Command terminated by signal\s+([^\r\n]+)\s*$",
        text,
        re.MULTILINE,
    )
    exits = re.findall(r"^\s*Exit status:\s*([0-9]+)\s*$", text, re.MULTILINE)
    require(len(commands) == 1 and not signals and exits == ["0"],
            "GNU time unique command and exit zero:" + label)
    try:
        argv = shlex.split(commands[0], posix=True)
    except ValueError as error:
        raise Reject("GNU time command shlex:" + label) from error
    require(bool(argv), "GNU time nonempty argv:" + label)
    return argv, 0


def validate_timed_exit(
    captures: dict[str, Capture],
    *,
    stdout_name: str,
    stderr_name: str,
    time_name: str,
    exit_name: str,
    program_basename: str,
    required_argv_tokens: tuple[str, ...],
    label: str,
) -> list[str]:
    stdout = captures[SEALED_REL + "/" + stdout_name]
    stderr = captures[SEALED_REL + "/" + stderr_name]
    timing = captures[SEALED_REL + "/" + time_name]
    require(timing.raw is not None, "retained GNU time:" + label)
    exit_object = json_of(captures, exit_name)
    require(
        set(exit_object) == {
            "schema", "exit_code",
            "stdout_sha256", "stdout_size",
            "stderr_sha256", "stderr_size",
            "time_sha256", "time_size",
        }
        and exit_object.get("schema") == TIMED_EXIT_SCHEMA,
        "timed exit exact schema:" + label,
    )
    require_exit_zero(exit_object, label)
    require(
        exit_object.get("stdout_sha256") == stdout.sha256
        and exit_object.get("stdout_size") == stdout.size
        and exit_object.get("stderr_sha256") == stderr.sha256
        and exit_object.get("stderr_size") == stderr.size
        and exit_object.get("time_sha256") == timing.sha256
        and exit_object.get("time_size") == timing.size,
        "timed exit raw artifact binding:" + label,
    )
    argv, _ = parse_gnu_time(timing.raw, label)
    require(
        sum(PurePosixPath(token).name == program_basename for token in argv) == 1
        and all(argv.count(token) == 1 for token in required_argv_tokens)
        and PurePosixPath(argv[0]).name == "env"
        and len(argv) >= 2
        and argv[1] == "-i",
        "timed exit command semantics:" + label,
    )
    return argv


def require_exact_environment(
    actual: Any, expected: dict[str, str], label: str
) -> None:
    require(type(actual) is dict, "environment object:" + label)
    require(
        actual == expected
        and all(type(key) is str and type(value) is str
                for key, value in actual.items()),
        "exact environment:" + label,
    )


def require_recomputed_analyzer_equal(
    recomputed: Any, reported: Any, label: str
) -> None:
    require(
        type(recomputed) is dict
        and type(reported) is dict
        and recomputed == reported,
        "recomputed analyzer object exact equality:" + label,
    )


def load_pinned_analyzer(captures: dict[str, Capture]) -> types.ModuleType:
    relpath = "deliverables/" + SUP_PREFIX + "_strace_analyzer.py"
    captured = captures[relpath]
    require(captured.raw is not None and captured.sha256
            == "e1d15f6384d86d95f6389c4e999f3fe801eeedace3c833de763fc968f245727a",
            "captured pinned analyzer bytes")
    name = "_cm2_c30a_release_checker_pinned_analyzer"
    module = types.ModuleType(name)
    module.__file__ = os.fspath(WORKSPACE / relpath)
    module.__package__ = ""
    sys.modules[name] = module
    try:
        exec(
            compile(captured.raw, module.__file__, "exec", dont_inherit=True),
            module.__dict__,
        )
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def source_path_from_assembly(
    assembly: dict[str, Any], sealed_name: str
) -> Path:
    row = assembly["sources"][sealed_name]
    source = Path(os.path.abspath(os.fspath(WORKSPACE / row["source_relpath"])))
    require(source.is_relative_to(WORKSPACE),
            "authoritative source workspace containment:" + sealed_name)
    return source


def build_authoritative_analyzer_contract(
    analyzer: types.ModuleType,
    captures: dict[str, Capture],
    assembly: dict[str, Any],
    role: str,
) -> dict[str, Any]:
    if role == "seed30630929_producer_authoritative":
        tag = "04_seed30630929"
        kind = "producer"
        seed = "30630929"
    elif role == "seed30630071_verifier_authoritative":
        tag = "06_seed30630071.verifier"
        kind = "verifier"
        seed = "30630071"
    elif role == "seed30630929_verifier_authoritative":
        tag = "07_seed30630929.verifier"
        kind = "verifier"
        seed = "30630929"
    else:
        raise Reject("unknown authoritative analyzer role:" + role)

    if kind == "producer":
        trace_name = tag + ".producer.trace.raw"
        stdout_name = tag + ".producer.stdout.json"
        stderr_name = tag + ".producer.stderr.raw"
        time_name = tag + ".producer.time.txt"
        candidate_prefix = tag + ".candidate"
        provenance_name = tag + ".provenance.json"
    else:
        trace_name = tag + ".trace.raw"
        stdout_name = tag + ".stdout.json"
        stderr_name = tag + ".stderr.raw"
        time_name = tag + ".time.txt"
        candidate_prefix = (
            ("03_seed30630071" if seed == "30630071" else "04_seed30630929")
            + ".candidate"
        )
        provenance_name = ""

    source_paths = {
        name: source_path_from_assembly(assembly, sealed)
        for name, sealed in {
            "trace": trace_name,
            "stdout": stdout_name,
            "stderr": stderr_name,
            "time": time_name,
        }.items()
    }
    candidate_sources = {
        name: source_path_from_assembly(
            assembly, candidate_prefix + "/" + name
        )
        for name in OUTPUT_NAMES
    }
    candidate_parents = {path.parent for path in candidate_sources.values()}
    require(len(candidate_parents) == 1,
            "authoritative candidate common source directory:" + role)
    candidate_dir = next(iter(candidate_parents))
    candidate_bindings = {
        name: "cm2_round306c30a_sealed/" + name for name in OUTPUT_NAMES
    }
    stdout_object = strict_json(
        raw_of(captures, stdout_name), role + " stdout", newline=True
    )
    allowed_write_paths: list[str]
    protected_roots: list[str]
    if kind == "producer":
        provenance = source_path_from_assembly(assembly, provenance_name)
        seed1_candidate_sources = {
            source_path_from_assembly(
                assembly, "03_seed30630071.candidate/" + name
            ).parent
            for name in OUTPUT_NAMES
        }
        require(len(seed1_candidate_sources) == 1,
                "seed1 candidate common source directory")
        allowed_write_paths = sorted([
            os.fspath(candidate_dir),
            os.fspath(provenance),
            *(os.fspath(candidate_dir / name) for name in OUTPUT_NAMES),
        ])
        protected_roots = [
            os.fspath(DELIVERABLES),
            os.fspath(WORKSPACE / ".cm2-runtime/python-flint-0.9.0"),
            os.fspath(WORKSPACE / ".cm2-runtime/candidates"),
            os.fspath(next(iter(seed1_candidate_sources))),
        ]
        profile = "c30a-controlled-producer-seed30630929-scrubbed-full-trace-v2"
    else:
        allowed_write_paths = []
        protected_roots = [
            os.fspath(DELIVERABLES),
            os.fspath(candidate_dir),
            os.fspath(WORKSPACE / ".cm2-runtime/python-flint-0.9.0"),
            os.fspath(WORKSPACE / ".cm2-runtime/candidates"),
        ]
        profile = "c30a-controlled-candidate-verifier-seed" + seed + "-full-trace-v2"
    return {
        "schema": analyzer.CONTRACT_SCHEMA,
        "profile": profile,
        "workspace": os.fspath(WORKSPACE),
        "paths": {
            **{name: os.fspath(path) for name, path in source_paths.items()},
            "manifest": os.fspath(WORKSPACE / BASE_MANIFEST_REL),
            "candidate_dir": os.fspath(candidate_dir),
        },
        "pins": {
            "trace_sha256": captures[SEALED_REL + "/" + trace_name].sha256,
            "stdout_sha256": captures[SEALED_REL + "/" + stdout_name].sha256,
            "stderr_sha256": captures[SEALED_REL + "/" + stderr_name].sha256,
            "time_sha256": captures[SEALED_REL + "/" + time_name].sha256,
            "manifest_sha256": BASE_MANIFEST_SHA256,
        },
        "manifest_members": BASE_MEMBERS,
        "candidate_members": OUTPUT_HASHES,
        "candidate_manifest_bindings": candidate_bindings,
        "stdout": {"policy": "one-canonical-json-write", "expected_object": stdout_object},
        "stderr": {
            "policy": "c30a-round215-diagnostics",
            "expected_line_count": 50,
        },
        "allowed_write_paths": allowed_write_paths,
        "protected_roots": protected_roots,
        "capture": {
            "require_follow_forks": True,
            "require_fd_path_decoding": True,
            "require_percent_file": True,
            "minimum_string_limit": 4096,
            "required_explicit_syscalls": analyzer.REQUIRED_EXPLICIT_CAPTURE_SYSCALLS,
        },
    }


def parse_trace_execve_argv(
    analyzer: types.ModuleType, captured: Capture, label: str
) -> list[tuple[str, list[str], int]]:
    require(bool(captured.execve_lines), "retained execve trace lines:" + label)
    calls = analyzer.parse_trace(b"".join(captured.execve_lines))
    output: list[tuple[str, list[str], int]] = []
    for call in calls:
        if call.name != "execve" or call.result_integer != 0 or len(call.args) < 3:
            continue
        try:
            executable = analyzer.decode_c_string(call.args[0]).decode("utf-8")
            argv = ast.literal_eval(call.args[1])
        except Exception as error:
            raise Reject("execve decode:" + label) from error
        require(
            type(argv) is list and all(type(item) is str for item in argv),
            "execve argv string list:" + label,
        )
        match = re.search(r"/\*\s*([0-9]+)\s+vars\s*\*/", call.args[2])
        require(match is not None, "execve environment count:" + label)
        output.append((executable, argv, int(match.group(1))))
    require(bool(output), "successful execve census:" + label)
    return output


def validate_authoritative_env_and_argv(
    analyzer: types.ModuleType,
    captures: dict[str, Capture],
    contract: dict[str, Any],
    role: str,
) -> None:
    if role == "seed30630929_producer_authoritative":
        trace_name = "04_seed30630929.producer.trace.raw"
        time_name = "04_seed30630929.producer.time.txt"
        expected_environment = {
            "HOME": "/nonexistent",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": "/usr/bin:/bin",
            "PYTHONHASHSEED": "30630929",
            "PYTHONPYCACHEPREFIX": os.fspath(
                WORKSPACE
                / ".cm2-runtime/audit/c30a-supplemental-controlled-seed30630929-v2-pycache"
            ),
            "TZ": "UTC",
        }
        python_flags = ["-P", "-s", "-B"]
    else:
        tag = "06_seed30630071" if "30630071" in role else "07_seed30630929"
        trace_name = tag + ".verifier.trace.raw"
        time_name = tag + ".verifier.time.txt"
        expected_environment = {
            "HOME": "/nonexistent",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": "/usr/bin:/bin",
            "TZ": "UTC",
        }
        python_flags = ["-I", "-B"]
    timing = captures[SEALED_REL + "/" + time_name]
    require(timing.raw is not None, "authoritative time retained:" + role)
    time_argv, _ = parse_gnu_time(timing.raw, role)
    require(time_argv[0] == "/usr/bin/strace",
            "authoritative time begins strace:" + role)
    require(
        time_argv[:9] == [
            "/usr/bin/strace", "-qq", "-f", "-yy", "-s", "4096",
            "-e", "trace=all", "-o",
        ],
        "authoritative exact full-trace flags:" + role,
    )
    output_index = time_argv.index("-o") + 1
    require(
        output_index < len(time_argv)
        and Path(os.path.abspath(os.fspath(
            WORKSPACE / time_argv[output_index]
        ))) == Path(contract["paths"]["trace"]),
        "authoritative raw time trace path/contract binding:" + role,
    )
    env_indices = [
        index for index, token in enumerate(time_argv)
        if PurePosixPath(token).name == "env"
    ]
    require(len(env_indices) == 1, "authoritative time one env:" + role)
    env_index = env_indices[0]
    require(
        time_argv[env_index] == "/usr/bin/env"
        and time_argv[env_index + 1] == "-i",
        "authoritative /usr/bin/env -i:" + role,
    )
    python_indices = [
        index for index in range(env_index + 2, len(time_argv))
        if time_argv[index].endswith("/bin/python")
    ]
    require(len(python_indices) == 1, "authoritative time one python:" + role)
    python_index = python_indices[0]
    assignments = time_argv[env_index + 2:python_index]
    parsed_environment: dict[str, str] = {}
    for assignment in assignments:
        require("=" in assignment, "authoritative env assignment:" + role)
        key, value = assignment.split("=", 1)
        require(key not in parsed_environment, "authoritative unique env key:" + role)
        parsed_environment[key] = value
    require_exact_environment(
        parsed_environment, expected_environment, "authoritative:" + role
    )
    require(time_argv[python_index + 1:python_index + 1 + len(python_flags)]
            == python_flags,
            "authoritative python flags:" + role)
    expected_python = os.fspath(
        WORKSPACE / ".cm2-runtime/python-flint-0.9.0/bin/python"
    )
    require(time_argv[python_index] == expected_python,
            "authoritative pinned Python path:" + role)
    program_index = python_index + 1 + len(python_flags)
    require(program_index < len(time_argv),
            "authoritative Python program argv:" + role)
    if role == "seed30630929_producer_authoritative":
        expected_program = DELIVERABLES / (
            SUP_PREFIX + "_controlled_replay_launcher.py"
        )
        expected_program_argv = [
            os.fspath(expected_program),
            "--expected-hash-seed", "30630929",
            "--expected-pycache-prefix",
            expected_environment["PYTHONPYCACHEPREFIX"],
            "--candidate-dir", contract["paths"]["candidate_dir"],
            "--provenance", os.fspath(
                WORKSPACE / ".cm2-runtime/audit/"
                "c30a-supplemental-controlled-seed30630929-v2-provenance.json"
            ),
        ]
    else:
        expected_program = DELIVERABLES / (BASE_PREFIX + "_independent_verifier.py")
        expected_program_argv = [
            os.fspath(expected_program),
            "--candidate-dir", contract["paths"]["candidate_dir"],
        ]
    require(
        Path(os.path.abspath(os.fspath(
            WORKSPACE / time_argv[program_index]
        ))) == expected_program,
        "authoritative pinned program path:" + role,
    )
    require(time_argv[program_index:] == expected_program_argv,
            "authoritative exact program argv:" + role)
    execves = parse_trace_execve_argv(
        analyzer, captures[SEALED_REL + "/" + trace_name], role
    )
    env_exec = [row for row in execves if PurePosixPath(row[0]).name == "env"]
    python_exec = [row for row in execves if row[0].endswith("/bin/python")]
    require(
            len(env_exec) == 1 and len(python_exec) == 1
            and env_exec[0][0] == "/usr/bin/env"
            and python_exec[0][0] == expected_python,
            "authoritative env/python execve census:" + role)
    require(env_exec[0][1] == time_argv[env_index:],
            "authoritative env execve argv/time binding:" + role)
    require(python_exec[0][1] == time_argv[python_index:],
            "authoritative python execve argv/time binding:" + role)
    require(python_exec[0][2] == len(expected_environment),
            "authoritative python execve environment count:" + role)
    require(
        os.path.abspath(contract["paths"]["candidate_dir"])
        in time_argv,
        "authoritative candidate argv/contract binding:" + role,
    )


def current_snapshot_row(captured: Capture) -> dict[str, Any]:
    path = WORKSPACE / captured.relpath
    status = path.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and status.st_nlink == 1
        and not path.is_symlink()
        and (
            status.st_dev, status.st_ino, status.st_size,
            status.st_mtime_ns, status.st_ctime_ns,
        ) == (
            captured.dev, captured.ino, captured.size,
            captured.mtime_ns, captured.ctime_ns,
        ),
        "snapshot/current captured identity:" + captured.relpath,
    )
    return {
        "relpath": captured.relpath,
        "sha256": captured.sha256,
        "size": captured.size,
        "dev": captured.dev,
        "ino": captured.ino,
        "mode": status.st_mode,
        "nlink": status.st_nlink,
        "mtime_ns": captured.mtime_ns,
        "ctime_ns": captured.ctime_ns,
    }


def current_stat7(captured: Capture) -> list[int]:
    path = WORKSPACE / captured.relpath
    status = path.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and status.st_nlink == 1
        and not path.is_symlink()
        and (
            status.st_dev, status.st_ino, status.st_size,
            status.st_mtime_ns, status.st_ctime_ns,
        ) == (
            captured.dev, captured.ino, captured.size,
            captured.mtime_ns, captured.ctime_ns,
        ),
        "current stat7 captured identity:" + captured.relpath,
    )
    return [
        status.st_dev, status.st_ino, status.st_mode, status.st_nlink,
        status.st_size, status.st_mtime_ns, status.st_ctime_ns,
    ]


def capture_directory_stat7(
    relpath: str, expected_names: set[str]
) -> list[int]:
    safe_relpath(relpath)
    path = WORKSPACE / relpath
    before = path.lstat()
    require(
        stat.S_ISDIR(before.st_mode) and not path.is_symlink(),
        "candidate directory boundary:" + relpath,
    )
    descriptor = os.open(
        path,
        os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev, opened.st_ino, opened.st_mode, opened.st_nlink,
                opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns,
            ) == (
                before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
                before.st_size, before.st_mtime_ns, before.st_ctime_ns,
            ),
            "candidate directory pre/open race:" + relpath,
        )
        names = set(os.listdir(descriptor))
        final = os.fstat(descriptor)
        require(
            names == expected_names
            and (
                final.st_dev, final.st_ino, final.st_mode, final.st_nlink,
                final.st_size, final.st_mtime_ns, final.st_ctime_ns,
            ) == (
                opened.st_dev, opened.st_ino, opened.st_mode, opened.st_nlink,
                opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns,
            ),
            "candidate directory exact map/final race:" + relpath,
        )
    finally:
        os.close(descriptor)
    after = path.lstat()
    require(
        (
            after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
            after.st_size, after.st_mtime_ns, after.st_ctime_ns,
        ) == (
            before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
            before.st_size, before.st_mtime_ns, before.st_ctime_ns,
        ),
        "candidate directory post race:" + relpath,
    )
    return [
        opened.st_dev, opened.st_ino, opened.st_mode, opened.st_nlink,
        opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns,
    ]


def expected_base_snapshot(
    base: dict[str, Capture],
    phase: str,
    retained_check: dict[str, Any],
) -> dict[str, Any]:
    require(phase in BASE_SNAPSHOT_PHASES.values(), "base snapshot phase")
    require(
        type(retained_check) is dict
        and set(retained_check) == {"stdout", "manifest_sha256_record"},
        "base snapshot retained check schema",
    )
    return {
        "schema": BASE_SNAPSHOT_SCHEMA,
        "phase": phase,
        "retained_check": retained_check,
        "manifest": current_snapshot_row(base[BASE_MANIFEST_REL]),
        "manifest_member_map": BASE_MEMBERS,
        "member_count": len(BASE_MEMBERS),
        "members": {
            name: current_snapshot_row(base["deliverables/" + name])
            for name in sorted(BASE_MEMBERS, key=os.fsencode)
        },
    }


def validate_base_snapshot_object(
    value: Any, expected: dict[str, Any], label: str
) -> None:
    require(type(value) is dict and value == expected,
            "base snapshot exact current capture:" + label)


def validate_base_checks(
    captures: dict[str, Capture],
    base: dict[str, Capture],
    assembly_sources: dict[str, Capture],
) -> None:
    base_manifest = base[BASE_MANIFEST_REL]
    require(base_manifest.raw is not None, "base manifest raw")
    expected = expected_manifest_stdout(base_manifest.raw)
    expected_manifest_record = (
        BASE_MANIFEST_SHA256.encode("ascii") + b"  "
        + BASE_MANIFEST_REL.encode("ascii") + b"\n"
    )
    for tag in ("00_base_manifest_pre", "09_base_manifest_post"):
        require(raw_of(captures, tag + ".stdout") == expected,
                "base manifest check stdout:" + tag)
        require(
            raw_of(captures, tag + ".manifest.sha256")
            == expected_manifest_record,
            "base manifest check trust-root record:" + tag,
        )
        require_empty(captures, tag + ".stderr.raw")
        require_exit_zero(json_of(captures, tag + ".exit.json"), tag)
    assembly = json_of(captures, "00_assembly_source_map.json")

    def source_capture(sealed_name: str) -> Capture:
        return assembly_sources[
            assembly["sources"][sealed_name]["source_relpath"]
        ]

    pre_stdout = source_capture("00_base_manifest_pre.stdout")
    pre_manifest_record = source_capture(
        "00_base_manifest_pre.manifest.sha256"
    )
    require(
        pre_stdout.relpath
        == (
            ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807/"
            "manifest_pre.txt"
        )
        and pre_manifest_record.relpath
        == (
            ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807/"
            "manifest_file_pre.sha256"
        ),
        "retained historical precheck exact source authority",
    )
    replay_sources = tuple(source_capture(name) for name in (
        "01_preflight.stdout.json",
        "02_fresh_runtime/completion.json",
        "02_c29/verifier.stdout.json",
        "02_c29/verifier.time.txt",
        "03_seed30630071.producer.stdout.json",
        "03_seed30630071.producer.time.txt",
        "04_seed30630929.producer.stdout.json",
        "04_seed30630929.producer.time.txt",
        "04_seed30630929.producer.trace.raw",
        "05_controlled_seed_comparison.stdout",
        "06_seed30630071.verifier.stdout.json",
        "06_seed30630071.verifier.time.txt",
        "06_seed30630071.verifier.trace.raw",
        "07_seed30630929.verifier.stdout.json",
        "07_seed30630929.verifier.time.txt",
        "07_seed30630929.verifier.trace.raw",
        "08_attacks.harness.stdout.json",
        "08_attacks.harness.time.txt",
        "08_attacks/attack_summary.json",
    ))
    for item in replay_sources:
        require(
            pre_stdout.mtime_ns < item.mtime_ns
            and pre_stdout.ctime_ns < item.ctime_ns
            and pre_manifest_record.mtime_ns < item.mtime_ns
            and pre_manifest_record.ctime_ns < item.ctime_ns,
            "retained precheck predates replay source:" + item.relpath,
        )
    post_stdout = source_capture("09_base_manifest_post.stdout")
    post_manifest_record = source_capture(
        "09_base_manifest_post.manifest.sha256"
    )
    post_snapshot_source = source_capture(
        "09_base_manifest_post.snapshot.json"
    )
    for item in replay_sources:
        require(
            post_stdout.mtime_ns > item.mtime_ns
            and post_stdout.ctime_ns > item.ctime_ns
            and post_manifest_record.mtime_ns > item.mtime_ns
            and post_manifest_record.ctime_ns > item.ctime_ns
            and post_snapshot_source.mtime_ns > item.mtime_ns
            and post_snapshot_source.ctime_ns > item.ctime_ns,
            "retained postcheck follows replay source:" + item.relpath,
        )
    pre = json_of(captures, "00_base_manifest_pre.snapshot.json")
    post = json_of(captures, "09_base_manifest_post.snapshot.json")
    expected_pre = expected_base_snapshot(
        base,
        BASE_SNAPSHOT_PHASES["pre"],
        {
            "stdout": current_snapshot_row(pre_stdout),
            "manifest_sha256_record": current_snapshot_row(
                pre_manifest_record
            ),
        },
    )
    expected_post = expected_base_snapshot(
        base,
        BASE_SNAPSHOT_PHASES["post"],
        {
            "stdout": current_snapshot_row(post_stdout),
            "manifest_sha256_record": current_snapshot_row(
                post_manifest_record
            ),
        },
    )
    validate_base_snapshot_object(pre, expected_pre, "pre")
    validate_base_snapshot_object(post, expected_post, "post")
    identity_keys = {
        "schema", "manifest", "manifest_member_map", "member_count", "members"
    }
    pre_identity = {key: pre[key] for key in identity_keys}
    post_identity = {key: post[key] for key in identity_keys}
    require(pre_identity == post_identity,
            "base pre/post hash, exact map, identity, and metadata unchanged")


def validate_assembly_source_map(
    captures: dict[str, Capture]
) -> dict[str, Capture]:
    value = json_of(captures, "00_assembly_source_map.json")
    sources = value.get("sources")
    expected = sealed_required_files() - {"00_assembly_source_map.json"}
    require(
        value.get("schema")
        == "cm2.round306c30a.supplemental-audit-assembly-map.v1"
        and value.get("base_manifest_sha256") == BASE_MANIFEST_SHA256
        and type(sources) is dict
        and set(sources) == expected,
        "sealed assembly exact source map",
    )
    source_captures: dict[str, Capture] = {}
    for sealed_name, row in sources.items():
        cap = captures[SEALED_REL + "/" + sealed_name]
        require(
            type(row) is dict
            and set(row) == {"source_relpath", "sha256", "size"}
            and type(row.get("source_relpath")) is str,
            "assembly source row exact schema:" + sealed_name,
        )
        source_relpath = row["source_relpath"]
        safe_relpath(source_relpath)
        require(
            not source_relpath.startswith(SEALED_REL + "/")
            and source_relpath not in source_captures,
            "assembly source external to seal and unique:" + sealed_name,
        )
        source = capture_once(source_relpath, retain=False)
        require(
            row.get("sha256") == cap.sha256 == source.sha256
            and row.get("size") == cap.size == source.size,
            "race-checked source/sealed byte equality:" + sealed_name,
        )
        source_captures[source_relpath] = source
    return source_captures


def validate_preflight(captures: dict[str, Capture]) -> None:
    value = json_of(captures, "01_preflight.stdout.json")
    require(
        value.get("status") == (
            "READY_FOR_EXPENSIVE_SUPPLEMENTAL_REPLAYS__"
            "NOT_A_C30A_AUDIT_CLOSURE_PASS"
        )
        and value.get("formal_credit", {}).get(
            "additional_whole_origin_exclusions"
        ) == 0
        and value.get("formal_credit", {}).get("source_W_transition")
        == "252_TO_92_ONLY"
        and value.get("formal_credit", {}).get("source_W_252_to_90")
        == "FORBIDDEN",
        "supplemental preflight non-closure boundary",
    )
    require_empty(captures, "01_preflight.stderr.raw")
    require_exit_zero(json_of(captures, "01_preflight.exit.json"), "preflight")


def validate_fresh_runtime(captures: dict[str, Capture]) -> None:
    completion = json_of(captures, "02_fresh_runtime/completion.json")
    completion_rel = (
        "deliverables/cm2_round306c30a_python_flint_fresh_runtime_completion.json"
    )
    require(captures[completion_rel].raw == raw_of(
        captures, "02_fresh_runtime/completion.json"
    ), "fresh runtime completion sealed copy")
    require(
        completion.get("status")
        == "PASS_FRESH_OFFLINE_RUNTIME_REBUILT_AND_INDEPENDENTLY_ATTESTED"
        and completion.get("math_credit_added") == 0
        and completion.get("original_c30a_manifest", {}).get("sha256")
        == BASE_MANIFEST_SHA256
        and completion.get("target", {}).get("precondition") == "ABSENT"
        and completion.get("target", {}).get("creation_policy")
        == "EXCLUSIVE_CREATE_NO_DELETE_NO_OVERWRITE",
        "fresh runtime completion",
    )
    descriptor = json_of(captures, "02_fresh_runtime/rebuild_descriptor.json")
    stages = descriptor.get("stages")
    require(
        descriptor.get("schema")
        == "cm2.round306c30a.python-flint-fresh-runtime-rebuild.v1"
        and descriptor.get("verdict") == "PASS"
        and descriptor.get("offline") is True
        and descriptor.get("target_precondition") == "ABSENT"
        and descriptor.get("target_policy")
        == "EXCLUSIVE_CREATE_NO_DELETE_NO_OVERWRITE"
        and descriptor.get("orchestrator_environment") == {
            "HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"
        }
        and type(stages) is list and len(stages) == 4
        and [row.get("stage") for row in stages]
        == ["venv_create", "offline_install", "freeze", "attestation"],
        "fresh runtime rebuild descriptor",
    )
    stage_by_name = {row["stage"]: row for row in stages}
    for stage in ("venv_create", "offline_install", "freeze", "attestation"):
        row = json_of(captures, f"02_fresh_runtime/{stage}.stage.json")
        require(row.get("stage") == stage, "fresh runtime stage name:" + stage)
        require_exit_zero(row, "fresh runtime stage:" + stage)
        require(row == stage_by_name[stage],
                "fresh runtime stage/descriptor byte semantics:" + stage)
        stdout_name = (
            "freeze.stdout" if stage == "freeze"
            else stage + ".stdout.json" if stage == "attestation"
            else stage + ".stdout.raw"
        )
        stderr_name = stage + ".stderr.raw"
        stdout_cap = captures[
            SEALED_REL + "/02_fresh_runtime/" + stdout_name
        ]
        stderr_cap = captures[
            SEALED_REL + "/02_fresh_runtime/" + stderr_name
        ]
        require(
            row.get("stdout", {}).get("sha256") == stdout_cap.sha256
            and row.get("stdout", {}).get("size") == stdout_cap.size
            and row.get("stderr", {}).get("sha256") == stderr_cap.sha256
            and row.get("stderr", {}).get("size") == stderr_cap.size,
            "fresh runtime stage raw stream binding:" + stage,
        )
    install_argv = stage_by_name["offline_install"].get("argv")
    venv_argv = stage_by_name["venv_create"].get("argv")
    require(
        type(venv_argv) is list
        and venv_argv[0:6] == [
            "/usr/bin/python3.12", "-I", "-B", "-m", "venv", "--copies"
        ]
        and type(install_argv) is list
        and all(flag in install_argv for flag in (
            "--no-index", "--no-deps", "--only-binary=:all:",
            "--require-hashes", "--no-cache-dir",
        )),
        "fresh offline exact rebuild argv contract",
    )
    attestation_raw = raw_of(captures, "02_fresh_runtime/attestation.stdout.json")
    recheck_raw = raw_of(
        captures, "02_fresh_runtime/attestation_recheck.stdout.json"
    )
    require(attestation_raw == recheck_raw,
            "fresh runtime attestation byte-identical recheck")
    attestation = strict_json(
        attestation_raw, "fresh runtime attestation", newline=True
    )
    require(
        attestation.get("verdict") == "PASS"
        and attestation.get("offline") is True
        and attestation.get("interpreter", {}).get("python_version") == "3.12.3"
        and attestation.get("interpreter", {}).get("glibc") == "2.39"
        and attestation.get("interpreter", {}).get("machine_executable_sha256")
        == "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
        and attestation.get("sealed_wheel", {}).get("sha256")
        == "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76"
        and attestation.get("sealed_wheel", {}).get(
            "record_verification", {}
        ).get("hashed_entry_count") == 112
        and attestation.get("installed_distribution", {}).get(
            "record_verification", {}
        ).get("hashed_entry_count") == 114
        and attestation.get("imported_flint", {}).get("python_flint_version")
        == "0.9.0"
        and attestation.get("imported_flint", {}).get("flint_version") == "3.6.0",
        "fresh runtime attestation semantics",
    )
    for name in (
        "rebuild_invocation.stderr.raw", "venv_create.stderr.raw",
        "offline_install.stderr.raw", "attestation.stderr.raw",
        "attestation_recheck.stderr.raw",
    ):
        require_empty(captures, "02_fresh_runtime/" + name)


def validate_c29(captures: dict[str, Capture]) -> dict[str, Capture]:
    manifest = captures[C29_MANIFEST_REL]
    require(manifest.sha256 == C29_MANIFEST_SHA256 and manifest.raw is not None,
            "C29 manifest trust root")
    members = parse_manifest(manifest.raw, "C29")
    require(len(members) == 10, "C29 exact ten-member manifest")
    chain: dict[str, Capture] = {}
    for name, expected in members.items():
        item = capture_once(
            "deliverables/" + name,
            retain=name.endswith("_result.json") or name.endswith("_verification.json"),
        )
        require(item.sha256 == expected, "C29 member SHA256:" + name)
        chain[name] = item
    expected_stdout = expected_manifest_stdout(manifest.raw)
    require(raw_of(captures, "02_c29/manifest_check.stdout") == expected_stdout,
            "C29 manifest check stdout")
    value = json_of(captures, "02_c29/verifier.stdout.json")
    require(
        value.get("status") == (
            "PASS_INDEPENDENT_C29_57876_COMPONENTS_124_FIBRES_"
            "502204_DISPOSITIONS_RECONSTRUCTED__D02_BOUNDARY_PRESERVED"
        )
        and value.get("component_rows") == 57876
        and value.get("fibre_rows") == 124
        and value.get("disposition_rows") == 502204
        and value.get("total_rows") == 560204
        and value.get("result_sha256") == C29_RESULT_OBJECT_SHA256,
        "C29 independent clean replay",
    )
    require_empty(captures, "02_c29/verifier.stderr.raw")
    argv = validate_timed_exit(
        captures,
        stdout_name="02_c29/verifier.stdout.json",
        stderr_name="02_c29/verifier.stderr.raw",
        time_name="02_c29/verifier.time.txt",
        exit_name="02_c29/verifier.exit.json",
        program_basename=C29_PREFIX + "_independent_verifier.py",
        required_argv_tokens=("-I", "-B", "--candidate-dir"),
        label="C29 independent verifier",
    )
    candidate_index = argv.index("--candidate-dir") + 1
    require(candidate_index < len(argv), "C29 candidate argv value")
    candidate_path = Path(os.path.abspath(os.fspath(
        WORKSPACE / argv[candidate_index]
    )))
    script_tokens = [
        token for token in argv
        if PurePosixPath(token).name == C29_PREFIX + "_independent_verifier.py"
    ]
    require(
        candidate_path == DELIVERABLES
        and len(script_tokens) == 1
        and Path(os.path.abspath(os.fspath(WORKSPACE / script_tokens[0])))
        == DELIVERABLES / (C29_PREFIX + "_independent_verifier.py"),
        "C29 timed command exact source and candidate authority",
    )
    result_name = next(name for name in members if name.endswith("_result.json"))
    result_cap = chain[result_name]
    require(result_cap.raw is not None, "C29 result retained")
    c29_result = strict_json(result_cap.raw, "C29 result", newline=False)
    require(c29_result.get("result_sha256") == C29_RESULT_OBJECT_SHA256,
            "C29 result object pin")
    return chain


def validate_candidate(captures: dict[str, Capture], tag: str) -> dict[str, str]:
    table: dict[str, str] = {}
    for name in OUTPUT_NAMES:
        relpath = SEALED_REL + "/" + tag + ".candidate/" + name
        item = captures[relpath]
        require(item.sha256 == OUTPUT_HASHES[name],
                "controlled candidate equals base seal:" + tag + ":" + name)
        table[name] = item.sha256
    result = json_of(
        captures,
        tag + ".candidate/" + BASE_PREFIX + "_result.json",
        newline=False,
    )
    require(
        result.get("result_sha256") == RESULT_OBJECT_SHA256
        and result.get("source_W_ledger_transition", {}).get("before", {}).get(
            "remaining"
        ) == 252
        and result.get("source_W_ledger_transition", {}).get("after", {}).get(
            "remaining"
        ) == 92,
        "controlled candidate fixed result:" + tag,
    )
    return table


def validate_controlled_seeds(
    captures: dict[str, Capture],
    assembly_sources: dict[str, Capture],
) -> dict[str, Any]:
    outputs: list[bytes] = []
    diagnostics: list[bytes] = []
    tables: list[dict[str, str]] = []
    provenance_rows: list[dict[str, Any]] = []
    for ordinal, seed in enumerate(SEEDS, start=3):
        tag = f"{ordinal:02d}_seed{seed}"
        provenance = json_of(captures, tag + ".provenance.json")
        expected_candidate_relpath = (
            ".cm2-runtime/audit/c30a-supplemental-controlled-seed"
            + seed + "-v2-candidate"
        )
        expected_pycache_relpath = (
            ".cm2-runtime/audit/c30a-supplemental-controlled-seed"
            + seed + "-v2-pycache"
        )
        expected_env = {
            "HOME": "/nonexistent",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": "/usr/bin:/bin",
            "PYTHONHASHSEED": seed,
            "PYTHONPYCACHEPREFIX": os.fspath(
                WORKSPACE / expected_pycache_relpath
            ),
            "TZ": "UTC",
        }
        python = provenance.get("python", {})
        producer = provenance.get("producer", {})
        require(
            CONTROLLED_PROVENANCE_SCHEMA is not None
            and provenance.get("schema") == CONTROLLED_PROVENANCE_SCHEMA
            and provenance.get("status") == "PREFLIGHT_PASS_REPLAY_NOT_YET_COMPLETE"
            and provenance.get("seed") == seed
            and provenance.get("hash_probe_value") == SEED_PROBES[seed]
            and provenance.get("environment") == expected_env
            and provenance.get("candidate_relpath") == expected_candidate_relpath
            and provenance.get("pycache_prefix_relpath")
            == expected_pycache_relpath
            and python.get("isolated") == 0
            and python.get("ignore_environment") == 0
            and python.get("safe_path") is True
            and python.get("no_user_site") == 1
            and python.get("dont_write_bytecode") == 1
            and python.get("hash_randomization") == 1
            and producer.get("sha256") == BASE_MEMBERS[BASE_PREFIX + "_producer.py"]
            and producer.get("transformed_sha256")
            == "6105ad2e3aeffbd2a27063a7e9b56cdadaeb22e8e96f8daf987f0a5763ac923e"
            and producer.get("transform") == "ONE_BYTE_ISOLATED_GUARD_1_TO_0"
            and producer.get("changed_byte_offset") == 36078,
            "true controlled seed provenance:" + seed,
        )
        stdout = raw_of(captures, tag + ".producer.stdout.json")
        value = strict_json(stdout, tag + " producer stdout", newline=True)
        require(
            value == {
                "result_sha256": RESULT_OBJECT_SHA256,
                "status": (
                    "PASS_12888_REDUCED_CLIPPED_DELTA_CELLS_DISPOSED__"
                    "12868_EXCLUDED__20_RESERVED_FOR_FULL_DELTA__"
                    "160_WHOLE_SOURCE_W_ORIGINS_PROMOTED__"
                    "2_INHERITED_H_OBSTRUCTIONS_HELD__D02_STILL_BLOCKED"
                ),
            },
            "producer canonical conclusion:" + seed,
        )
        require_exit_zero(json_of(captures, tag + ".producer.exit.json"),
                          "controlled producer:" + seed)
        stderr = raw_of(captures, tag + ".producer.stderr.raw")
        require(
            stderr.count(b"\n") == 50
            and b"PASS_12888_REDUCED" not in stderr
            and b'"result_sha256"' not in stderr,
            "producer stderr diagnostics-only contract:" + seed,
        )
        tables.append(validate_candidate(captures, tag))
        outputs.append(stdout)
        diagnostics.append(stderr)
        provenance_rows.append(provenance)
    require(outputs[0] == outputs[1], "controlled producer stdout byte identity")
    require(diagnostics[0] == diagnostics[1],
            "controlled producer stderr diagnostic byte identity")
    require(tables[0] == tables[1] == OUTPUT_HASHES,
            "controlled candidate two-seed byte identity")
    require(
        provenance_rows[0]["candidate_relpath"]
        != provenance_rows[1]["candidate_relpath"]
        and provenance_rows[0]["pycache_prefix_relpath"]
        != provenance_rows[1]["pycache_prefix_relpath"],
        "distinct controlled run candidate and pycache paths",
    )
    require(
        all(
            "-v2-" in row["candidate_relpath"]
            and "-v2-" in row["pycache_prefix_relpath"]
            for row in provenance_rows
        ),
        "seven-key v2 controlled replay provenance",
    )
    comparison_raw = raw_of(captures, "05_controlled_seed_comparison.stdout")
    comparison = strict_json(
        comparison_raw, "05 controlled-seed comparator receipt", newline=True
    )
    comparison_body = dict(comparison)
    comparison_object_hash = comparison_body.pop("payload_sha256", None)
    seed2_analyzer = comparison.get("seed2_full_trace_analyzer", {})
    seed2_audit = seed2_analyzer.get("result", {})
    seed2_supplement = seed2_analyzer.get("supplement", {})
    superseded_v1 = comparison.get("superseded_v1_fail_closed", {})
    require(
        CONTROLLED_COMPARATOR_SCHEMA is not None
        and comparison.get("schema") == CONTROLLED_COMPARATOR_SCHEMA
        and comparison.get("status") == (
            "PASS_C30A_CONTROLLED_DUAL_SEED_EVIDENCE__"
            "ADDITIONAL_CREDIT_0__252_TO_92_ONLY__252_TO_90_FORBIDDEN"
        )
        and comparison_object_hash
        == sha256(canonical(comparison_body) + b"\n")
        and comparison.get("comparisons", {}).get(
            "candidate_member_count_each"
        ) == 4
        and comparison.get("comparisons", {}).get(
            "candidate_files_seed1_equal_seed2"
        ) is True
        and comparison.get("comparisons", {}).get(
            "candidate_files_seed1_equal_seal"
        ) is True
        and comparison.get("comparisons", {}).get(
            "candidate_files_seed2_equal_seal"
        ) is True
        and comparison.get("comparisons", {}).get(
            "producer_stdout_bytes_identical"
        ) is True
        and comparison.get("conclusion", {}).get(
            "additional_whole_origin_credit"
        ) == 0
        and comparison.get("conclusion", {}).get("source_w_transition")
        == "252->92"
        and comparison.get("conclusion", {}).get("transition_252_to_90")
        == "FORBIDDEN"
        and comparison.get("seeds", {}).get("30630071", {}).get("trace_role")
        == "AUXILIARY_NON_AUTHORIZING_SELECTIVE_TRACE"
        and comparison.get("seeds", {}).get("30630929", {}).get("trace_role")
        == "RELEASE_AUTHORIZING_SCRUBBED_TRACE_ALL",
        "controlled-seed comparator release receipt",
    )
    require(
        superseded_v1.get("status")
        == "SUPERSEDED_FAIL_CLOSED_NETWORK_SYSCALLS_4"
        and superseded_v1.get("release_authority") == "NONE"
        and superseded_v1.get("network_syscall_count") == 4
        and superseded_v1.get("successful_socket_syscall_count") == 2
        and superseded_v1.get("failed_connect_enoent_count") == 2
        and superseded_v1.get("reason")
        == "MISSING_HOME_TRIGGERED_LOCAL_NSS_AF_UNIX_ATTEMPTS"
        and {
            name: row.get("sha256")
            for name, row in superseded_v1.get("evidence", {}).items()
        } == SUPERSEDED_V1_PINS,
        "old six-key v1 fixed and explicitly excluded from authority",
    )
    for seed in SEEDS:
        seed_receipt = comparison.get("seeds", {}).get(seed, {})
        ordinal = 3 if seed == "30630071" else 4
        tag = f"{ordinal:02d}_seed{seed}"
        expected_candidate_relpath = (
            ".cm2-runtime/audit/c30a-supplemental-controlled-seed"
            + seed + "-v2-candidate"
        )
        candidate_receipt = seed_receipt.get("candidate", {})
        receipt_members = candidate_receipt.get("members")
        require(
            seed_receipt.get("environment", {}).get("HOME") == "/nonexistent"
            and len(seed_receipt.get("environment", {})) == 7
            and candidate_receipt.get("path") == expected_candidate_relpath
            and type(receipt_members) is dict
            and set(receipt_members) == OUTPUT_NAMES
            and candidate_receipt.get("stat") == capture_directory_stat7(
                expected_candidate_relpath, OUTPUT_NAMES
            ),
            "comparator receipt exact v2 seven-key seed:" + seed,
        )
        assembly = json_of(captures, "00_assembly_source_map.json")
        for name in OUTPUT_NAMES:
            sealed_name = tag + ".candidate/" + name
            source_relpath = expected_candidate_relpath + "/" + name
            source_row = assembly["sources"][sealed_name]
            source_capture = assembly_sources[source_relpath]
            receipt_row = receipt_members[name]
            require(
                source_row.get("source_relpath") == source_relpath
                and set(receipt_row) == {"path", "sha256", "size", "stat"}
                and receipt_row.get("path") == source_relpath
                and receipt_row.get("sha256")
                == source_capture.sha256 == OUTPUT_HASHES[name]
                and receipt_row.get("size") == source_capture.size
                and receipt_row.get("stat") == current_stat7(source_capture),
                "comparator pre-verifier candidate stat/source-map binding:"
                + seed + ":" + name,
            )
    comparison_source = assembly_sources[
        assembly["sources"]["05_controlled_seed_comparison.stdout"][
            "source_relpath"
        ]
    ]
    for sealed_trace in (
        "06_seed30630071.verifier.trace.raw",
        "07_seed30630929.verifier.trace.raw",
    ):
        trace_source = assembly_sources[
            assembly["sources"][sealed_trace]["source_relpath"]
        ]
        require(
            comparison_source.mtime_ns < trace_source.mtime_ns
            and comparison_source.ctime_ns < trace_source.ctime_ns,
            "comparator candidate receipt predates verifier trace:"
            + sealed_trace,
        )
    require(
        seed2_audit.get("schema") == "cm2.c30a.supplemental.strace-audit.v1"
        and seed2_audit.get("status")
        == "PASS_C30A_STRACE_ZERO_MUTATION_CERTIFIED"
        and seed2_audit.get("errors") == []
        and seed2_audit.get("trace_contract", {}).get("captures_all_syscalls")
        is True
        and seed2_audit.get("trace_contract", {}).get(
            "capture_complete_for_claimed_scope"
        ) is True
        and seed2_audit.get("trace_contract", {}).get(
            "forbidden_mutation_attempt_count"
        ) == 0
        and seed2_audit.get("trace_contract", {}).get(
            "protected_mutation_attempt_count"
        ) == 0
        and seed2_audit.get("trace_contract", {}).get("sha256")
        == captures[
            SEALED_REL + "/04_seed30630929.producer.trace.raw"
        ].sha256
        and seed2_supplement.get("capture_complete") is True
        and seed2_supplement.get("captures_all_syscalls") is True
        and seed2_supplement.get("network_syscall_count") == 0
        and seed2_supplement.get("successful_pyc_access_count") == 0
        and seed2_supplement.get("historical_candidate_access_count") == 0,
        "comparator embedded authoritative seed2 trace=all audit",
    )
    require(
        comparison.get("dependencies", {}).get("strace_analyzer", {}).get(
            "sha256"
        )
        == captures[
            "deliverables/" + SUP_PREFIX + "_strace_analyzer.py"
        ].sha256,
        "comparator/analyzer payload binding",
    )
    require(
        comparison.get("dependencies", {}).get("launcher", {}).get("sha256")
        == captures[
            "deliverables/" + SUP_PREFIX + "_controlled_replay_launcher.py"
        ].sha256
        and comparison.get("dependencies", {}).get("protocol", {}).get("sha256")
        == captures["deliverables/" + SUP_PREFIX + "_protocol.md"].sha256,
        "comparator v2 launcher/protocol payload binding",
    )
    table_rows: dict[str, str] = {}
    for ordinal, seed in enumerate(SEEDS, start=3):
        tag = f"{ordinal:02d}_seed{seed}"
        table_rows[seed + "/producer.stdout.json"] = captures[
            SEALED_REL + "/" + tag + ".producer.stdout.json"
        ].sha256
        for name in OUTPUT_NAMES:
            table_rows[seed + "/candidate/" + name] = captures[
                SEALED_REL + "/" + tag + ".candidate/" + name
            ].sha256
    expected_table = b"".join(
        table_rows[name].encode("ascii") + b"  " + name.encode("ascii") + b"\n"
        for name in sorted(table_rows, key=os.fsencode)
    )
    require(raw_of(captures, "05_controlled_seed_comparison.sha256")
            == expected_table,
            "controlled-seed canonical comparison SHA table")
    require_exit_zero(json_of(captures, "05_controlled_seed_comparison.exit.json"),
                      "controlled-seed comparison")
    require_empty(captures, "05_controlled_seed_comparison.stderr.raw")
    return {"tables": tables, "provenance": provenance_rows}


def validate_verifiers(
    captures: dict[str, Capture],
    base: dict[str, Capture],
    trace_audit: dict[str, Any],
) -> None:
    base_manifest = base[BASE_MANIFEST_REL]
    require(base_manifest.raw is not None, "base manifest raw for verifier checks")
    manifest_stdout = expected_manifest_stdout(base_manifest.raw)
    authoritative: list[bytes] = []
    for ordinal, seed in enumerate(SEEDS, start=6):
        tag = f"{ordinal:02d}_seed{seed}.verifier"
        require(raw_of(captures, tag + ".manifest_pre.stdout") == manifest_stdout,
                "verifier manifest pre:" + seed)
        require(raw_of(captures, tag + ".manifest_post.stdout") == manifest_stdout,
                "verifier manifest post:" + seed)
        stdout = raw_of(captures, tag + ".stdout.json")
        value = strict_json(stdout, tag + " stdout", newline=True)
        require(
            value.get("status") == (
                "PASS_INDEPENDENT_C30A_12888_CELL_ROWS__"
                "160_WHOLE_ORIGIN_ROWS__2_INHERITED_H_HOLDS_RECONSTRUCTED__"
                "252_TO_92_TRANSITION_VERIFIED__D02_BOUNDARY_PRESERVED"
            )
            and value.get("cell_rows") == 12888
            and value.get("whole_origin_rows") == 160
            and value.get("held_origin_rows") == 2
            and value.get("total_rows") == 13050
            and value.get("result_sha256") == RESULT_OBJECT_SHA256,
            "independent verifier reconstruction:" + seed,
        )
        require_exit_zero(json_of(captures, tag + ".exit.json"),
                          "independent verifier:" + seed)
        diagnostics = raw_of(captures, tag + ".stderr.raw")
        require(
            diagnostics.count(b"\n") == 50
            and b"PASS_INDEPENDENT_C30A" not in diagnostics
            and b'"result_sha256"' not in diagnostics,
            "verifier stderr diagnostics-only contract:" + seed,
        )
        trace_role = "seed" + seed + "_verifier_authoritative"
        trace_row = trace_audit["traces"][trace_role]
        recomputed = trace_row["analyzer_result"]
        trace_contract = recomputed["trace_contract"]
        protected_roots = trace_contract["protected_roots"]
        expected_candidate = os.fspath(
            WORKSPACE / ".cm2-runtime/audit/"
            / ("c30a-supplemental-controlled-seed" + seed + "-v2-candidate")
        )
        require(
            trace_row.get("candidate_or_deliverable_verifier_mutations") == 0
            and recomputed.get("status")
            == "PASS_C30A_STRACE_ZERO_MUTATION_CERTIFIED"
            and trace_contract.get("forbidden_mutation_attempt_count") == 0
            and trace_contract.get("protected_mutation_attempt_count") == 0
            and expected_candidate in protected_roots,
            "recomputed verifier trace proves zero candidate writes:" + seed,
        )
        authoritative.append(stdout)
    require(authoritative[0] == authoritative[1],
            "two controlled-candidate verifier stdout byte identity")


def validate_attacks(captures: dict[str, Capture]) -> None:
    summary = json_of(captures, "08_attacks/attack_summary.json")
    require(
        summary.get("status") == "PASS_10_OF_10_COHERENT_ATTACKS_REJECTED"
        and summary.get("total") == 10
        and summary.get("rejected") == 10
        and type(summary.get("attacks")) is list
        and len(summary["attacks"]) == 10,
        "persistent ten-attack summary",
    )
    harness_stdout = raw_of(captures, "08_attacks.harness.stdout.json")
    require(harness_stdout == canonical(summary) + b"\n",
            "attack harness stdout equals retained summary")
    require_empty(captures, "08_attacks.harness.stderr.raw")
    argv = validate_timed_exit(
        captures,
        stdout_name="08_attacks.harness.stdout.json",
        stderr_name="08_attacks.harness.stderr.raw",
        time_name="08_attacks.harness.time.txt",
        exit_name="08_attacks.harness.exit.json",
        program_basename=SUP_PREFIX + "_coherent_attack_harness.py",
        required_argv_tokens=(
            "-I", "-B", "--candidate-dir", "--evidence-dir",
        ),
        label="persistent coherent attack harness",
    )
    candidate_index = argv.index("--candidate-dir") + 1
    evidence_index = argv.index("--evidence-dir") + 1
    require(candidate_index < len(argv) and evidence_index < len(argv),
            "attack harness path argv values")
    candidate = Path(os.path.abspath(os.fspath(
        WORKSPACE / argv[candidate_index]
    )))
    evidence = Path(os.path.abspath(os.fspath(
        WORKSPACE / argv[evidence_index]
    )))
    expected_candidate = (
        WORKSPACE
        / ".cm2-runtime/audit/"
        "c30a-supplemental-controlled-seed30630071-v2-candidate"
    )
    script_tokens = [
        token for token in argv
        if PurePosixPath(token).name
        == SUP_PREFIX + "_coherent_attack_harness.py"
    ]
    require(
        candidate == expected_candidate
        and evidence.is_relative_to(WORKSPACE / ".cm2-runtime")
        and evidence != WORKSPACE / ".cm2-runtime"
        and len(script_tokens) == 1
        and Path(os.path.abspath(os.fspath(WORKSPACE / script_tokens[0])))
        == DELIVERABLES / (SUP_PREFIX + "_coherent_attack_harness.py"),
        "attack harness timed command exact controlled candidate/evidence",
    )
    for ordinal, name in enumerate(ATTACK_NAMES):
        root = f"08_attacks/{ordinal:02d}_{name}"
        descriptor = json_of(captures, root + "/attack_descriptor.json")
        exit_object = json_of(captures, root + "/verifier.exit.json")
        stdout_cap = captures[SEALED_REL + "/" + root + "/verifier.stdout.raw"]
        stderr_cap = captures[SEALED_REL + "/" + root + "/verifier.stderr.raw"]
        require(
            descriptor.get("ordinal") == ordinal
            and descriptor.get("name") == name
            and descriptor.get("base_result_object_sha256")
            == RESULT_OBJECT_SHA256,
            "attack descriptor:" + name,
        )
        code = exit_object.get("exit_code")
        require(
            type(code) is int and code != 0
            and exit_object.get("stdout_sha256") == stdout_cap.sha256
            and exit_object.get("stdout_size") == stdout_cap.size
            and exit_object.get("stderr_sha256") == stderr_cap.sha256
            and exit_object.get("stderr_size") == stderr_cap.size,
            "per-attack rejection evidence:" + name,
        )
        for output_name in OUTPUT_NAMES:
            cap = captures[
                SEALED_REL + "/" + root + "/candidate/" + output_name
            ]
            require(cap.size > 0, "forged candidate retained:" + name)
    held_root = "08_attacks/09_held_to_promoted_162_overclaim_full_reclosure"
    forged = json_of(
        captures,
        held_root + "/candidate/" + BASE_PREFIX + "_result.json",
        newline=False,
    )
    body = dict(forged)
    object_hash = body.pop("result_sha256", None)
    require(
        object_hash == sha256(canonical(body))
        and forged.get("whole_origin_census", {}).get(
            "Round306C30A_new_promoted"
        ) == 162
        and forged.get("whole_origin_census", {}).get(
            "Round306C30A_inherited_H_held"
        ) == 0
        and forged.get("source_W_ledger_transition", {}).get("after", {}).get(
            "remaining"
        ) == 90
        and forged.get("formal_credit", {}).get(
            "whole_source_W_origin_exclusions"
        ) == 162,
        "fully reclosed 162/0 252-to-90 forgery retained and rejected",
    )


def validate_full_trace_audit(captures: dict[str, Capture]) -> dict[str, Any]:
    audit = json_of(captures, "11_trace_audit.json")
    audit_body = dict(audit)
    audit_object_hash = audit_body.pop("payload_sha256", None)
    rows = audit.get("traces")
    require(
        audit_object_hash == sha256(canonical(audit_body))
        and audit.get("schema")
        == "cm2.round306c30a.supplemental-full-trace-aggregate.v1"
        and audit.get("status")
        == "PASS_FULL_TRACE_AUDIT__NO_PROTECTED_MUTATIONS_OR_NETWORK"
        and type(rows) is dict,
        "trace audit top-level PASS",
    )
    required = {
        "seed30630071_producer_auxiliary",
        "seed30630929_producer_authoritative",
        "seed30630071_verifier_authoritative",
        "seed30630929_verifier_authoritative",
    }
    require(set(rows) == required, "trace audit exact trace roles")
    analyzer = load_pinned_analyzer(captures)
    assembly = json_of(captures, "00_assembly_source_map.json")
    recomputed_results: dict[str, dict[str, Any]] = {}
    trace_paths = {
        "seed30630071_producer_auxiliary":
            "03_seed30630071.producer.trace.raw",
        "seed30630929_producer_authoritative":
            "04_seed30630929.producer.trace.raw",
        "seed30630071_verifier_authoritative":
            "06_seed30630071.verifier.trace.raw",
        "seed30630929_verifier_authoritative":
            "07_seed30630929.verifier.trace.raw",
    }
    for role, sealed_name in trace_paths.items():
        row = rows[role]
        cap = captures[SEALED_REL + "/" + sealed_name]
        require(
            type(row) is dict
            and row.get("path") == sealed_name
            and row.get("sha256") == cap.sha256
            and row.get("size") == cap.size
            and cap.size > 0,
            "trace byte binding:" + role,
        )
        if role.endswith("auxiliary"):
            require(
                row.get("authorization_role") == "AUXILIARY_ONLY_NOT_AUTHORIZING"
                and row.get("trace_all") is False
                and row.get("claims_limited_to")
                == ["EXIT_STATUS", "HASH_SEED", "OUTPUT_BYTES"]
                and "protected_root_mutations" not in row
                and "network_syscalls" not in row,
                "selective seed1 trace cannot authorize",
            )
        else:
            expected_contract = build_authoritative_analyzer_contract(
                analyzer, captures, assembly, role
            )
            reported_contract = row.get("analyzer_contract")
            require(reported_contract == expected_contract,
                    "release-checker reconstructed analyzer contract:" + role)
            contract_source = ANALYZER_CONTRACT_SOURCE_PREFIX + role
            contract_sha256 = sha256(
                analyzer.canonical_bytes(expected_contract)
            )
            try:
                recomputed = analyzer.audit(
                    expected_contract, contract_source, contract_sha256
                )
            except Exception as error:
                raise Reject("authoritative analyzer execution:" + role) from error
            require_recomputed_analyzer_equal(
                recomputed, row.get("analyzer_result"), role
            )
            recomputed_results[role] = recomputed
            trace_contract = recomputed.get("trace_contract", {})
            syscall_counts = trace_contract.get("syscall_counts")
            require(
                type(syscall_counts) is dict
                and all(type(name) is str and type(count) is int and count >= 0
                        for name, count in syscall_counts.items()),
                "recomputed syscall census:" + role,
            )
            network_count = sum(
                syscall_counts.get(name, 0) for name in NETWORK_SYSCALLS
            )
            require(
                row.get("authorization_role") == "AUTHORITATIVE"
                and row.get("trace_all") is True
                and row.get("strace_selector") == "trace=all"
                and row.get("network_syscalls") == network_count == 0
                and row.get("protected_root_mutations")
                == trace_contract.get("protected_mutation_attempt_count") == 0
                and row.get("candidate_or_deliverable_verifier_mutations") == 0
                and row.get("unclassified_mutating_syscalls") == 0
                and recomputed.get("schema")
                == "cm2.c30a.supplemental.strace-audit.v1"
                and recomputed.get("status")
                == "PASS_C30A_STRACE_ZERO_MUTATION_CERTIFIED"
                and recomputed.get("errors") == []
                and recomputed.get("contract", {}).get("sha256")
                == contract_sha256
                and recomputed.get("contract", {}).get("source")
                == contract_source
                and trace_contract.get("sha256") == cap.sha256
                and trace_contract.get("captures_all_syscalls") is True
                and trace_contract.get("capture_complete_for_claimed_scope")
                is True
                and trace_contract.get("missing_explicit_mutation_syscalls") == []
                and trace_contract.get("forbidden_mutation_attempt_count") == 0
                and trace_contract.get("protected_mutation_attempt_count") == 0
                and recomputed.get("conclusion", {}).get(
                    "certifiable_zero_mutation_to_protected_roots"
                ) is True,
                "recomputed authoritative trace=all coverage:" + role,
            )
            validate_authoritative_env_and_argv(
                analyzer, captures, expected_contract, role
            )
    cold = rows["seed30630929_producer_authoritative"]
    require(
        cold.get("fresh_candidate_mkdir_succeeded") is True
        and cold.get("candidate_preexisted") is False
        and cold.get("pycache_prefix_preexisted") is False
        and cold.get("successful_pyc_reads") == 0,
        "scrubbed process/import/output cold replay",
    )
    require(cold.get("authoritative_stdout_writes") == 1,
            "cold producer one authoritative stdout write")
    require(cold.get("diagnostic_stderr_writes") == 50,
            "cold producer diagnostics write census")
    for role in (
        "seed30630071_verifier_authoritative",
        "seed30630929_verifier_authoritative",
    ):
        require(
                rows[role].get("authoritative_stdout_writes")
                == recomputed_results[role].get(
                    "stdout_contract", {}
                ).get("write_syscall_count") == 1,
                "verifier one authoritative stdout write:" + role)
        require(
                rows[role].get("diagnostic_stderr_writes")
                == recomputed_results[role].get(
                    "stderr_contract", {}
                ).get("write_syscall_count") == 50,
                "verifier diagnostics write census:" + role)
    require(
        cold.get("authoritative_stdout_writes")
        == recomputed_results[
            "seed30630929_producer_authoritative"
        ].get("stdout_contract", {}).get("write_syscall_count")
        and cold.get("diagnostic_stderr_writes")
        == recomputed_results[
            "seed30630929_producer_authoritative"
        ].get("stderr_contract", {}).get("write_syscall_count"),
        "cold producer write census recomputed by analyzer",
    )
    comparison = json_of(captures, "05_controlled_seed_comparison.stdout")
    require_recomputed_analyzer_equal(
        recomputed_results["seed30630929_producer_authoritative"],
        comparison.get("seed2_full_trace_analyzer", {}).get("result"),
        "comparator embedded seed2 analyzer result",
    )
    analyzer_rel = "deliverables/" + SUP_PREFIX + "_strace_analyzer.py"
    require(audit.get("analyzer_sha256") == captures[analyzer_rel].sha256,
            "trace analyzer source pin")
    return audit


def validate_invocations(captures: dict[str, Capture]) -> None:
    invocations = json_of(captures, "10_invocations.json")
    seeds = invocations.get("controlled_seed_runs")
    verifiers = invocations.get("controlled_candidate_verifiers")
    require(
        set(invocations) == {
            "schema", "status", "controlled_seed_runs",
            "controlled_candidate_verifiers",
        }
        and invocations.get("schema")
        == "cm2.round306c30a.supplemental-invocations.v1"
        and invocations.get("status")
        == "RECORDED_INVOCATIONS__RAW_TIME_AND_TRACE_ARE_AUTHORITATIVE"
        and type(seeds) is list and len(seeds) == 2
        and type(verifiers) is list and len(verifiers) == 2,
        "exact invocation summary schema/census",
    )
    for index, (expected_seed, row) in enumerate(
        zip(SEEDS, seeds, strict=True)
    ):
        argv = row.get("argv")
        environment = row.get("environment")
        require(
            set(row) == {
                "seed", "argv", "environment", "candidate_precondition",
                "pycache_precondition", "strace_selector",
            }
            and row.get("seed") == expected_seed
            and row.get("candidate_precondition") == "ABSENT"
            and row.get("pycache_precondition") == "ABSENT"
            and type(argv) is list
            and "-P" in argv and "-s" in argv and "-B" in argv
            and "-I" not in argv
            and type(environment) is dict
            and set(environment) == {
                "HOME", "LANG", "LC_ALL", "PATH", "PYTHONHASHSEED",
                "PYTHONPYCACHEPREFIX", "TZ",
            }
            and environment["HOME"] == "/nonexistent"
            and environment["LANG"] == "C.UTF-8"
            and environment["LC_ALL"] == "C.UTF-8"
            and environment["PATH"] == "/usr/bin:/bin"
            and environment["PYTHONHASHSEED"] == expected_seed
            and type(environment["PYTHONPYCACHEPREFIX"]) is str
            and "-v2-" in environment["PYTHONPYCACHEPREFIX"]
            and environment["TZ"] == "UTC"
            and row.get("strace_selector") == (
                "AUXILIARY_SELECTIVE_NON_AUTHORIZING"
                if index == 0 else "trace=all"
            ),
            "controlled producer invocation:" + expected_seed,
        )
    for expected_seed, row in zip(SEEDS, verifiers, strict=True):
        environment = row.get("environment")
        require(
            set(row) == {"seed", "argv", "environment", "strace_selector"}
            and row.get("seed") == expected_seed
            and type(row.get("argv")) is list
            and "-I" in row["argv"] and "-B" in row["argv"]
            and row.get("strace_selector") == "trace=all"
            and environment == {
                "HOME": "/nonexistent",
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "PATH": "/usr/bin:/bin",
                "TZ": "UTC",
            },
            "full-trace verifier invocation",
        )


def validate_closure_result(captures: dict[str, Capture]) -> dict[str, Any]:
    result = json_of(captures, "12_closure_result.json")
    body = dict(result)
    object_hash = body.pop("payload_sha256", None)
    require(
        set(result) == {
            "schema", "status",
            "original_c30a_whole_origin_exclusion_credit",
            "supplemental_additional_whole_origin_exclusion_credit",
            "source_W_transition", "source_W_252_to_90", "D02", "CM2",
            "payload_sha256",
        }
        and object_hash == sha256(canonical(body))
        and result.get("schema")
        == "cm2.round306c30a.supplemental-audit-closure-result.v1"
        and result.get("status")
        == "PASS_SUPPLEMENTAL_C30A_AUDIT_CLOSURE__252_TO_92_ONLY"
        and result.get("original_c30a_whole_origin_exclusion_credit") == 160
        and result.get("supplemental_additional_whole_origin_exclusion_credit")
        == 0
        and result.get("source_W_transition") == {"before": 252, "after": 92}
        and result.get("source_W_252_to_90") == "FORBIDDEN"
        and result.get("D02") == "BLOCKED_COMPOSITE"
        and result.get("CM2") == "NO-GO_FOR_CLAIM",
        "fixed zero-additional-credit closure result",
    )
    return result


def validate_payload_semantics(
    captures: dict[str, Capture], base: dict[str, Capture]
) -> dict[str, Any]:
    require(
        PROTOCOL_SHA256 is not None
        and HEX64.fullmatch(PROTOCOL_SHA256) is not None
        and captures["deliverables/" + SUP_PREFIX + "_protocol.md"].sha256
        == PROTOCOL_SHA256,
        "filled frozen seven-key v2 supplemental protocol pin",
    )
    require(
        captures["deliverables/" + SUP_PREFIX + "_strace_analyzer.py"].sha256
        == "e1d15f6384d86d95f6389c4e999f3fe801eeedace3c833de763fc968f245727a",
        "frozen strace analyzer pin",
    )
    require(
        CONTROLLED_LAUNCHER_SHA256 is not None
        and HEX64.fullmatch(CONTROLLED_LAUNCHER_SHA256) is not None
        and captures[
            "deliverables/" + SUP_PREFIX + "_controlled_replay_launcher.py"
        ].sha256 == CONTROLLED_LAUNCHER_SHA256,
        "filled frozen seven-key v2 controlled launcher pin",
    )
    require(
        CONTROLLED_COMPARATOR_SHA256 is not None
        and HEX64.fullmatch(CONTROLLED_COMPARATOR_SHA256) is not None
        and captures[
            "deliverables/" + SUP_PREFIX + "_controlled_seed_comparator.py"
        ].sha256
        == CONTROLLED_COMPARATOR_SHA256,
        "filled frozen seven-key v2 controlled-seed comparator pin",
    )
    assembly_sources = validate_assembly_source_map(captures)
    validate_base_checks(captures, base, assembly_sources)
    validate_preflight(captures)
    validate_fresh_runtime(captures)
    c29_chain = validate_c29(captures)
    validate_controlled_seeds(captures, assembly_sources)
    validate_attacks(captures)
    trace = validate_full_trace_audit(captures)
    validate_verifiers(captures, base, trace)
    validate_invocations(captures)
    closure = validate_closure_result(captures)
    require_captures_unchanged(c29_chain)
    require_captures_unchanged(assembly_sources)
    require_captures_unchanged(base)
    return {"trace_audit": trace, "closure_result": closure}


def write_exclusive(relpath: str, raw: bytes) -> Capture:
    safe_relpath(relpath)
    absolute = WORKSPACE / relpath
    require(absolute.parent.is_dir() and not absolute.parent.is_symlink(),
            "output parent")
    descriptor = os.open(
        absolute,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        0o444,
    )
    complete = False
    try:
        offset = 0
        while offset < len(raw):
            count = os.write(descriptor, raw[offset:])
            require(count > 0, "short output write")
            offset += count
        os.fsync(descriptor)
        complete = True
    finally:
        os.close(descriptor)
        if not complete:
            try:
                absolute.unlink()
            except OSError:
                pass
    return capture_once(relpath, retain=True)


def copy_capture_once(
    source_relpath: str,
    target: Path,
    target_relpath: str,
    *,
    retain: bool,
) -> Capture:
    """Capture a source once while exclusively writing its sealed copy."""

    safe_relpath(source_relpath)
    safe_relpath(target_relpath)
    source = WORKSPACE / source_relpath
    before = source.lstat()
    require(
        stat.S_ISREG(before.st_mode)
        and not source.is_symlink()
        and before.st_nlink == 1
        and 0 <= before.st_size <= MAX_FILE,
        "assembly source regular singleton:" + source_relpath,
    )
    source_fd = os.open(
        source,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    target_fd = os.open(
        target,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        0o444,
    )
    chunks: list[bytes] | None = [] if retain else None
    collect_execve = (
        target_relpath.endswith(".trace.raw")
        or "trace-all" in PurePosixPath(target_relpath).name
    )
    execve_lines: list[bytes] = []
    trace_tail = b""
    digest = hashlib.sha256()
    complete = False
    try:
        opened = os.fstat(source_fd)
        identity = (
            before.st_dev, before.st_ino, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns,
        )
        require(
            (
                opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns, opened.st_ctime_ns,
            ) == identity,
            "assembly source pre/open race:" + source_relpath,
        )
        remaining = opened.st_size
        while remaining:
            block = os.read(source_fd, min(1 << 20, remaining))
            require(bool(block), "assembly source short read:" + source_relpath)
            digest.update(block)
            if chunks is not None:
                require(opened.st_size <= MAX_RETAIN,
                        "assembly retained source too large:" + source_relpath)
                chunks.append(block)
            if collect_execve:
                combined = trace_tail + block
                split = combined.splitlines(keepends=True)
                trace_tail = b""
                if split and not split[-1].endswith((b"\n", b"\r")):
                    trace_tail = split.pop()
                for line in split:
                    if b"execve(" in line:
                        require(len(line) <= 128 * 1024,
                                "bounded assembly execve trace line")
                        execve_lines.append(line)
                        require(len(execve_lines) <= 256,
                                "bounded assembly execve trace census")
            offset = 0
            while offset < len(block):
                count = os.write(target_fd, block[offset:])
                require(count > 0, "assembly short target write:" + target_relpath)
                offset += count
            remaining -= len(block)
        if collect_execve and trace_tail and b"execve(" in trace_tail:
            require(len(trace_tail) <= 128 * 1024,
                    "bounded final assembly execve trace line")
            execve_lines.append(trace_tail)
        require(not os.read(source_fd, 1), "assembly growing source:" + source_relpath)
        os.fsync(target_fd)
        final = os.fstat(source_fd)
        target_stat = os.fstat(target_fd)
        require(
            (
                final.st_dev, final.st_ino, final.st_size,
                final.st_mtime_ns, final.st_ctime_ns,
            ) == identity
            and target_stat.st_size == opened.st_size
            and stat.S_ISREG(target_stat.st_mode)
            and target_stat.st_nlink == 1,
            "assembly source/target final identity:" + target_relpath,
        )
        complete = True
    finally:
        os.close(source_fd)
        os.close(target_fd)
    require(complete, "assembly copy complete:" + target_relpath)
    after = source.lstat()
    require(
        (
            after.st_dev, after.st_ino, after.st_size,
            after.st_mtime_ns, after.st_ctime_ns,
        ) == (
            before.st_dev, before.st_ino, before.st_size,
            before.st_mtime_ns, before.st_ctime_ns,
        ),
        "assembly source post race:" + source_relpath,
    )
    return Capture(
        relpath=target_relpath,
        sha256=digest.hexdigest(),
        size=before.st_size,
        dev=before.st_dev,
        ino=before.st_ino,
        mtime_ns=before.st_mtime_ns,
        ctime_ns=before.st_ctime_ns,
        raw=None if chunks is None else b"".join(chunks),
        execve_lines=tuple(execve_lines),
    )


def rename_noreplace(source: Path, target: Path) -> None:
    """Linux renameat2(RENAME_NOREPLACE); never emulate with racy rename."""

    library = ctypes.CDLL(None, use_errno=True)
    function = getattr(library, "renameat2", None)
    require(function is not None, "libc renameat2 availability")
    function.argtypes = [
        ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p,
        ctypes.c_uint,
    ]
    function.restype = ctypes.c_int
    at_fdcwd = -100
    rename_noreplace_flag = 1
    result = function(
        at_fdcwd, os.fsencode(source), at_fdcwd, os.fsencode(target),
        rename_noreplace_flag,
    )
    if result != 0:
        code = ctypes.get_errno()
        raise Reject("renameat2(RENAME_NOREPLACE):" + os.strerror(code))


def assemble_sealed(
    base: dict[str, Capture], source_map_relpath: str, assembly_tag: str
) -> dict[str, Any]:
    require(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", assembly_tag) is not None,
            "safe assembly tag")
    map_cap = capture_once(source_map_relpath, retain=True)
    require(map_cap.raw is not None, "assembly input source map")
    source_map = strict_json(
        map_cap.raw, "assembly input source map", newline=True
    )
    sources = source_map.get("sources")
    required = sealed_required_files() - {"00_assembly_source_map.json"}
    require(
        source_map.get("schema")
        == "cm2.round306c30a.supplemental-audit-assembly-input.v1"
        and type(sources) is dict
        and set(sources) == required
        and len(set(sources.values())) == len(required),
        "assembly input exact unique source map",
    )
    audit_prefix = ".cm2-runtime/audit/"
    for sealed_name, source_relpath in sources.items():
        safe_relpath(sealed_name)
        safe_relpath(source_relpath)
        allowed_static_copy = (
            sealed_name == "02_fresh_runtime/completion.json"
            and source_relpath
            == "deliverables/cm2_round306c30a_python_flint_fresh_runtime_completion.json"
        )
        require(source_relpath.startswith(audit_prefix) or allowed_static_copy,
                "assembly source below audit root or fixed completion:" + sealed_name)
        source = WORKSPACE / source_relpath
        status = source.lstat()
        require(
            stat.S_ISREG(status.st_mode)
            and not source.is_symlink()
            and status.st_nlink == 1,
            "assembly source preflight:" + sealed_name,
        )
    # All dynamic sources exist before any output directory is created.
    static_captures: dict[str, Capture] = dict(base)
    for relpath in sorted(payload_static_members() - set(base), key=os.fsencode):
        static_captures[relpath] = capture_once(
            relpath, retain=retain_member(relpath)
        )
    destination = WORKSPACE / SEALED_REL
    temporary = destination.parent / (
        "." + destination.name + ".assembling." + assembly_tag
    )
    require(not destination.exists() and not temporary.exists(),
            "fresh sealed destination and assembly directory")
    temporary.mkdir(mode=0o755)
    relative_directories = {
        PurePosixPath(name).parent.as_posix()
        for name in required
        if PurePosixPath(name).parent.as_posix() != "."
    }
    expanded: set[str] = set()
    for value in relative_directories:
        parent = PurePosixPath(value)
        while parent.as_posix() != ".":
            expanded.add(parent.as_posix())
            parent = parent.parent
    for rel_dir in sorted(expanded, key=lambda item: (item.count("/"), os.fsencode(item))):
        (temporary / rel_dir).mkdir(mode=0o755)
    mapped: dict[str, Capture] = {}
    assembly_rows: dict[str, dict[str, Any]] = {}
    for sealed_name in sorted(required, key=os.fsencode):
        source_relpath = sources[sealed_name]
        target_relpath = SEALED_REL + "/" + sealed_name
        cap = copy_capture_once(
            source_relpath,
            temporary / sealed_name,
            target_relpath,
            retain=retain_member(target_relpath),
        )
        mapped[target_relpath] = cap
        assembly_rows[sealed_name] = {
            "source_relpath": source_relpath,
            "sha256": cap.sha256,
            "size": cap.size,
        }
    assembly_object = {
        "schema": "cm2.round306c30a.supplemental-audit-assembly-map.v1",
        "base_manifest_sha256": BASE_MANIFEST_SHA256,
        "source_map_sha256": map_cap.sha256,
        "sources": assembly_rows,
    }
    assembly_raw = canonical(assembly_object) + b"\n"
    assembly_target = temporary / "00_assembly_source_map.json"
    descriptor = os.open(
        assembly_target,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        0o444,
    )
    try:
        offset = 0
        while offset < len(assembly_raw):
            count = os.write(descriptor, assembly_raw[offset:])
            require(count > 0, "assembly map short write")
            offset += count
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    map_status = assembly_target.lstat()
    mapped[SEALED_REL + "/00_assembly_source_map.json"] = Capture(
        relpath=SEALED_REL + "/00_assembly_source_map.json",
        sha256=sha256(assembly_raw),
        size=len(assembly_raw),
        dev=map_status.st_dev,
        ino=map_status.st_ino,
        mtime_ns=map_status.st_mtime_ns,
        ctime_ns=map_status.st_ctime_ns,
        raw=assembly_raw,
    )
    captures = {**static_captures, **mapped}
    validate_payload_semantics(captures, base)
    scan_assembly_tree(temporary, sealed_required_files())
    temporary_rel = temporary.relative_to(WORKSPACE).as_posix()
    for sealed_name in sorted(sealed_required_files(), key=os.fsencode):
        copied = capture_once(temporary_rel + "/" + sealed_name)
        source_capture = mapped[SEALED_REL + "/" + sealed_name]
        require(
            copied.sha256 == source_capture.sha256
            and copied.size == source_capture.size,
            "assembled target byte identity:" + sealed_name,
        )
    directory_fd = os.open(
        temporary,
        os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    rename_noreplace(temporary, destination)
    return {
        "status": "SEALED_EVIDENCE_ASSEMBLED__NOT_A_RELEASE_PASS",
        "sealed_relpath": SEALED_REL,
        "member_count": len(mapped),
        "next_required": "BUILD_PAYLOAD_MANIFEST",
        "conclusion": fixed_conclusion(),
    }


def manifest_bytes(captures: dict[str, Capture]) -> bytes:
    return b"".join(
        captures[path].sha256.encode("ascii") + b"  "
        + path.encode("ascii") + b"\n"
        for path in sorted(captures, key=os.fsencode)
    )


def fixed_conclusion() -> dict[str, Any]:
    return {
        "original_c30a_whole_origin_exclusion_credit": 160,
        "supplemental_additional_whole_origin_exclusion_credit": 0,
        "source_W_transition": {"before": 252, "after": 92},
        "source_W_252_to_90": "FORBIDDEN",
        "D02": "BLOCKED_COMPOSITE",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def close_object(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "payload_sha256": sha256(canonical(body))}


def read_json_file_after_base(relpath: str) -> tuple[Capture, dict[str, Any]]:
    cap = capture_once(relpath, retain=True)
    require(cap.raw is not None, "retained JSON:" + relpath)
    return cap, strict_json(cap.raw, relpath, newline=True)


def validate_cold_receipt(
    receipt: dict[str, Any], receipt_cap: Capture, payload_cap: Capture
) -> None:
    body = dict(receipt)
    object_hash = body.pop("payload_sha256", None)
    require(
        object_hash == sha256(canonical(body))
        and receipt.get("schema")
        == "cm2.round306c30a.supplemental-audit-cold-receipt.v1"
        and receipt.get("status")
        == "PASS_PAYLOAD_AND_AUTHORITATIVE_FULL_TRACE_COLD_REPLAY"
        and receipt.get("payload_manifest_sha256") == payload_cap.sha256
        and receipt.get("receipt_file_sha256") is None
        and receipt.get("conclusion") == fixed_conclusion()
        and receipt_cap.sha256 == sha256(receipt_cap.raw or b""),
        "cold replay receipt closure",
    )


def validate_outer(
    outer: dict[str, Any], payload_cap: Capture, receipt_cap: Capture
) -> None:
    body = dict(outer)
    object_hash = body.pop("payload_sha256", None)
    require(
        object_hash == sha256(canonical(body))
        and outer.get("schema")
        == "cm2.round306c30a.supplemental-audit-outer-verification.v1"
        and outer.get("status")
        == "PASS_SUPPLEMENTAL_AUDIT_CLOSURE__ZERO_ADDITIONAL_CREDIT"
        and outer.get("payload_manifest_sha256") == payload_cap.sha256
        and outer.get("cold_replay_receipt_sha256") == receipt_cap.sha256
        and outer.get("conclusion") == fixed_conclusion(),
        "outer verification closure",
    )


def expect_rejection(label: str, operation: Any) -> str:
    try:
        operation()
    except Reject:
        return label
    raise Reject("negative selftest unexpectedly accepted:" + label)


def run_forgery_negative_selftest(
    base: dict[str, Capture]
) -> dict[str, Any]:
    rejected: list[str] = []

    reported = {
        "schema": "cm2.c30a.supplemental.strace-audit.v1",
        "status": "PASS_C30A_STRACE_ZERO_MUTATION_CERTIFIED",
    }
    forged_reported = dict(reported)
    forged_reported["status"] = "FAIL_CLOSED_C30A_STRACE_AUDIT"
    rejected.append(expect_rejection(
        "forged_authoritative_analyzer_aggregate",
        lambda: require_recomputed_analyzer_equal(
            reported, forged_reported, "negative-selftest"
        ),
    ))

    expected_environment = {
        "HOME": "/nonexistent",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": "/usr/bin:/bin",
        "TZ": "UTC",
    }
    forged_environment = dict(expected_environment)
    forged_environment["PYTHONHASHSEED"] = "30630071"
    rejected.append(expect_rejection(
        "forged_verifier_environment_extra_key",
        lambda: require_exact_environment(
            forged_environment, expected_environment, "negative-selftest"
        ),
    ))

    expected_snapshot = expected_base_snapshot(
        base,
        BASE_SNAPSHOT_PHASES["pre"],
        {
            "stdout": current_snapshot_row(base[BASE_MANIFEST_REL]),
            "manifest_sha256_record": current_snapshot_row(
                base[BASE_MANIFEST_REL]
            ),
        },
    )
    forged_snapshot = json.loads(canonical(expected_snapshot))
    first_member = sorted(BASE_MEMBERS, key=os.fsencode)[0]
    forged_snapshot["members"][first_member]["sha256"] = "0" * 64
    rejected.append(expect_rejection(
        "forged_base_snapshot_member_hash",
        lambda: validate_base_snapshot_object(
            forged_snapshot, expected_snapshot, "negative-selftest"
        ),
    ))

    forged_phase = json.loads(canonical(expected_snapshot))
    forged_phase["phase"] = BASE_SNAPSHOT_PHASES["post"]
    rejected.append(expect_rejection(
        "forged_base_snapshot_phase",
        lambda: validate_base_snapshot_object(
            forged_phase, expected_snapshot, "negative-selftest"
        ),
    ))
    return {
        "status": (
            "PASS_4_OF_4_STATIC_FORGERY_NEGATIVE_TESTS__"
            "NOT_A_SUPPLEMENTAL_RELEASE_PASS"
        ),
        "rejected": rejected,
        "supplemental_additional_whole_origin_exclusion_credit": 0,
        "source_W_transition": {"before": 252, "after": 92},
        "source_W_252_to_90": "FORBIDDEN",
    }


def assembly_input_template() -> dict[str, Any]:
    sources = {
        name: ".cm2-runtime/audit/REPLACE_WITH_EXACT_SOURCE/" + name
        for name in sorted(
            sealed_required_files() - {"00_assembly_source_map.json"},
            key=os.fsencode,
        )
    }
    sources["02_fresh_runtime/completion.json"] = (
        "deliverables/"
        "cm2_round306c30a_python_flint_fresh_runtime_completion.json"
    )
    return {
        "schema": "cm2.round306c30a.supplemental-audit-assembly-input.v1",
        "sources": sources,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("mode", choices=(
        "build-payload-manifest",
        "assemble-sealed",
        "mint-cold-receipt",
        "mint-outer-verification",
        "build-root-manifest",
        "check-root",
        "selftest-forgery-rejections",
        "emit-assembly-input-template",
    ))
    value.add_argument("--expected-payload-manifest-sha256")
    value.add_argument("--expected-cold-receipt-sha256")
    value.add_argument("--expected-root-manifest-sha256")
    value.add_argument("--assembly-source-map")
    value.add_argument("--assembly-tag")
    value.add_argument("--terminal-receipt-output", default=TERMINAL_RECEIPT_REL)
    return value


def main(argv: list[str] | None = None) -> int:
    try:
        # Non-negotiable ordering: this is the first workspace evidence read.
        base = validate_base()
        require(
            sys.flags.isolated == 1
            and sys.flags.dont_write_bytecode == 1
            and sys.dont_write_bytecode is True
            and sys.prefix != sys.base_prefix
            and Path(sys.prefix).resolve(strict=True)
            == (WORKSPACE / ".cm2-runtime/python-flint-0.9.0").resolve(strict=True),
            "locked isolated release-checker runtime",
        )
        arguments = parser().parse_args(sys.argv[1:] if argv is None else argv)

        if arguments.mode == "emit-assembly-input-template":
            result = assembly_input_template()
        elif arguments.mode == "selftest-forgery-rejections":
            result = run_forgery_negative_selftest(base)
        elif arguments.mode == "assemble-sealed":
            require(type(arguments.assembly_source_map) is str,
                    "assembly source map argument")
            require(type(arguments.assembly_tag) is str,
                    "assembly tag argument")
            result = assemble_sealed(
                base, arguments.assembly_source_map, arguments.assembly_tag
            )
        elif arguments.mode == "build-payload-manifest":
            captures = capture_staging_payload(base)
            validate_payload_semantics(captures, base)
            require_captures_unchanged(captures)
            manifest = write_exclusive(PAYLOAD_MANIFEST_REL, manifest_bytes(captures))
            result = {
                "status": "PAYLOAD_MANIFEST_BUILT__NOT_A_RELEASE_PASS",
                "payload_manifest_sha256": manifest.sha256,
                "member_count": len(captures),
                "next_required": "EXTERNALLY_PIN_SHA256_THEN_MINT_COLD_RECEIPT",
                "conclusion": fixed_conclusion(),
            }
        elif arguments.mode == "mint-cold-receipt":
            payload, captures, _ = capture_payload_from_manifest(
                PAYLOAD_MANIFEST_REL,
                arguments.expected_payload_manifest_sha256 or "",
                base,
            )
            semantics = validate_payload_semantics(captures, base)
            require_captures_unchanged(captures)
            require_captures_unchanged({PAYLOAD_MANIFEST_REL: payload})
            body = {
                "schema": "cm2.round306c30a.supplemental-audit-cold-receipt.v1",
                "status": "PASS_PAYLOAD_AND_AUTHORITATIVE_FULL_TRACE_COLD_REPLAY",
                "payload_manifest_sha256": payload.sha256,
                "payload_member_count": len(captures),
                "trace_audit_payload_sha256": semantics["trace_audit"][
                    "payload_sha256"
                ],
                "receipt_file_sha256": None,
                "conclusion": fixed_conclusion(),
            }
            receipt = close_object(body)
            cap = write_exclusive(COLD_RECEIPT_REL, canonical(receipt) + b"\n")
            result = {
                "status": "COLD_RECEIPT_MINTED__NOT_A_RELEASE_PASS",
                "cold_replay_receipt_sha256": cap.sha256,
                "payload_manifest_sha256": payload.sha256,
                "next_required": "EXTERNALLY_PIN_RECEIPT_THEN_MINT_OUTER_VERIFICATION",
                "conclusion": fixed_conclusion(),
            }
        elif arguments.mode == "mint-outer-verification":
            payload, captures, _ = capture_payload_from_manifest(
                PAYLOAD_MANIFEST_REL,
                arguments.expected_payload_manifest_sha256 or "",
                base,
            )
            validate_payload_semantics(captures, base)
            receipt_cap, receipt = read_json_file_after_base(COLD_RECEIPT_REL)
            require(
                HEX64.fullmatch(arguments.expected_cold_receipt_sha256 or "")
                is not None
                and receipt_cap.sha256 == arguments.expected_cold_receipt_sha256,
                "external cold receipt SHA256",
            )
            validate_cold_receipt(receipt, receipt_cap, payload)
            require_captures_unchanged(captures)
            require_captures_unchanged({
                PAYLOAD_MANIFEST_REL: payload,
                COLD_RECEIPT_REL: receipt_cap,
            })
            body = {
                "schema": (
                    "cm2.round306c30a.supplemental-audit-outer-verification.v1"
                ),
                "status": (
                    "PASS_SUPPLEMENTAL_AUDIT_CLOSURE__ZERO_ADDITIONAL_CREDIT"
                ),
                "payload_manifest_sha256": payload.sha256,
                "cold_replay_receipt_sha256": receipt_cap.sha256,
                "conclusion": fixed_conclusion(),
            }
            outer = close_object(body)
            cap = write_exclusive(OUTER_VERIFICATION_REL, canonical(outer) + b"\n")
            result = {
                "status": "OUTER_VERIFICATION_MINTED__NOT_A_RELEASE_PASS",
                "outer_verification_sha256": cap.sha256,
                "next_required": "BUILD_AND_EXTERNALLY_PIN_TWO_MEMBER_ROOT_MANIFEST",
                "conclusion": fixed_conclusion(),
            }
        elif arguments.mode == "build-root-manifest":
            payload, captures, _ = capture_payload_from_manifest(
                PAYLOAD_MANIFEST_REL,
                arguments.expected_payload_manifest_sha256 or "",
                base,
            )
            validate_payload_semantics(captures, base)
            receipt_cap, receipt = read_json_file_after_base(COLD_RECEIPT_REL)
            require(
                receipt_cap.sha256 == (arguments.expected_cold_receipt_sha256 or ""),
                "external cold receipt SHA256",
            )
            validate_cold_receipt(receipt, receipt_cap, payload)
            outer_cap, outer = read_json_file_after_base(OUTER_VERIFICATION_REL)
            validate_outer(outer, payload, receipt_cap)
            require_captures_unchanged(captures)
            require_captures_unchanged({
                PAYLOAD_MANIFEST_REL: payload,
                COLD_RECEIPT_REL: receipt_cap,
                OUTER_VERIFICATION_REL: outer_cap,
            })
            root_bytes = manifest_bytes({
                PAYLOAD_MANIFEST_REL: payload,
                OUTER_VERIFICATION_REL: outer_cap,
            })
            root_cap = write_exclusive(ROOT_MANIFEST_REL, root_bytes)
            result = {
                "status": "TWO_MEMBER_ROOT_MANIFEST_BUILT__NOT_A_RELEASE_PASS",
                "root_manifest_sha256": root_cap.sha256,
                "next_required": "EXTERNALLY_PIN_ROOT_SHA256_THEN_RUN_CHECK_ROOT",
                "conclusion": fixed_conclusion(),
            }
        else:
            expected_root = arguments.expected_root_manifest_sha256 or ""
            require(HEX64.fullmatch(expected_root) is not None
                    and expected_root != "0" * 64,
                    "externally pinned root manifest SHA256")
            root_cap = capture_once(ROOT_MANIFEST_REL, retain=True)
            require(root_cap.sha256 == expected_root and root_cap.raw is not None,
                    "root manifest external SHA256")
            root_members = parse_manifest(root_cap.raw, "supplemental root")
            require(set(root_members) == {
                PAYLOAD_MANIFEST_REL, OUTER_VERIFICATION_REL
            } and len(root_members) == 2, "root exact two-member map")
            payload_cap = capture_once(PAYLOAD_MANIFEST_REL, retain=True)
            outer_cap = capture_once(OUTER_VERIFICATION_REL, retain=True)
            require(
                payload_cap.sha256 == root_members[PAYLOAD_MANIFEST_REL]
                and outer_cap.sha256 == root_members[OUTER_VERIFICATION_REL],
                "root member SHA256",
            )
            payload, captures, _ = capture_payload_from_manifest(
                PAYLOAD_MANIFEST_REL,
                payload_cap.sha256,
                base,
                manifest_capture=payload_cap,
            )
            validate_payload_semantics(captures, base)
            require(outer_cap.raw is not None, "outer retained")
            outer = strict_json(
                outer_cap.raw, OUTER_VERIFICATION_REL, newline=True
            )
            receipt_cap, receipt = read_json_file_after_base(COLD_RECEIPT_REL)
            validate_cold_receipt(receipt, receipt_cap, payload)
            validate_outer(outer, payload, receipt_cap)
            require_captures_unchanged(captures)
            require_captures_unchanged({
                ROOT_MANIFEST_REL: root_cap,
                PAYLOAD_MANIFEST_REL: payload,
                OUTER_VERIFICATION_REL: outer_cap,
                COLD_RECEIPT_REL: receipt_cap,
            })
            body = {
                "schema": (
                    "cm2.round306c30a.supplemental-audit-terminal-receipt.v1"
                ),
                "status": (
                    "PASS_TERMINAL_C30A_SUPPLEMENTAL_AUDIT_AUTHORIZATION__"
                    "252_TO_92_ONLY"
                ),
                "root_manifest_sha256": root_cap.sha256,
                "payload_manifest_sha256": payload.sha256,
                "outer_verification_sha256": outer_cap.sha256,
                "cold_replay_receipt_sha256": receipt_cap.sha256,
                "conclusion": fixed_conclusion(),
            }
            terminal = close_object(body)
            write_exclusive(
                arguments.terminal_receipt_output,
                canonical(terminal) + b"\n",
            )
            # Success stdout is byte-identical to the terminal receipt file;
            # its file SHA is intentionally external, never self-referential.
            result = terminal
        sys.stdout.buffer.write(canonical(result) + b"\n")
        sys.stdout.buffer.flush()
        return 0
    except Exception as error:
        print(
            "C30A_SUPPLEMENTAL_RELEASE_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
