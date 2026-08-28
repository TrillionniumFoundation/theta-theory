#!/usr/bin/env python3
"""Fail-close C30a controlled dual-seed comparison and release receipt.

This additive audit tool grants no mathematical credit.  It first validates
the immutable thirteen-member C30a manifest and exact four-member seal.  It
then race-checks the two controlled producer runs, proves that the real hash
seeds were distinct and honoured, and compares every candidate byte with the
original seal.  The first run's selective trace is retained as auxiliary
evidence only.  The second run must have a complete ``trace=all`` capture and
must pass the independently pinned strace analyzer in-process.

The tool is intentionally stdout-only: it emits exactly one canonical JSON
line and never writes a receipt itself.  Redirect that line into the eventual
supplemental evidence directory and pin it in the additive manifest.  Missing
or still-changing evidence produces a canonical fail-closed receipt and a
nonzero exit status.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

SCHEMA = "cm2.round306c30a.controlled-dual-seed-release-receipt.v1"
WORKSPACE = Path(
    "/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572"
)
DELIVERABLES = WORKSPACE / "deliverables"
AUDIT_ROOT = WORKSPACE / ".cm2-runtime/audit"

BASE_MANIFEST = DELIVERABLES / (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion_manifest.sha256"
)
BASE_MANIFEST_SHA256 = (
    "0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc"
)
SEALED_DIR = DELIVERABLES / "cm2_round306c30a_sealed"
PRODUCER = DELIVERABLES / (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion_producer.py"
)
PRODUCER_SHA256 = (
    "41a3f11c3e44bdbbfcf95edf88902669365186e6fb6394aaee15a6846dc91714"
)
TRANSFORMED_PRODUCER_SHA256 = (
    "6105ad2e3aeffbd2a27063a7e9b56cdadaeb22e8e96f8daf987f0a5763ac923e"
)
ORIGINAL_GUARD = b"sys.flags.isolated == 1 and sys.dont_write_bytecode is True,"
CONTROLLED_GUARD = b"sys.flags.isolated == 0 and sys.dont_write_bytecode is True,"
CHANGED_BYTE_OFFSET = 36078

LAUNCHER = DELIVERABLES / (
    "cm2_round306c30a_supplemental_audit_closure_"
    "controlled_replay_launcher.py"
)
LAUNCHER_SHA256 = (
    "1437e60dd0b49e213b50615a3d5a7991c5bee1199edfda8b7495424d35a767cf"
)
ANALYZER = DELIVERABLES / (
    "cm2_round306c30a_supplemental_audit_closure_strace_analyzer.py"
)
ANALYZER_SHA256 = (
    "e1d15f6384d86d95f6389c4e999f3fe801eeedace3c833de763fc968f245727a"
)
PROTOCOL = DELIVERABLES / (
    "cm2_round306c30a_supplemental_audit_closure_protocol.md"
)
PROTOCOL_SHA256 = (
    "72e6e24b4f625ba9a8f9112950a07a22f5521f935acef0f3c1650f654995cc4e"
)

SEEDS = ("30630071", "30630929")
SEED_PROBES = {
    "30630071": 8841297538927089933,
    "30630929": 889641737497572634,
}
HASH_PROBE_TEXT = "CM2-C30a-controlled-hash-seed-v1"
PREFIXES = {
    seed: AUDIT_ROOT / f"c30a-supplemental-controlled-seed{seed}-v2"
    for seed in SEEDS
}
TRACE_SUFFIXES = {
    "30630071": "-trace.log",
    "30630929": "-trace-all.log",
}
SUPERSEDED_V1_PREFIX = (
    AUDIT_ROOT / "c30a-supplemental-controlled-seed30630929-v1"
)
SUPERSEDED_V1_PINS = {
    "provenance":
        "3acfc9d15daf39ca328cbc0a87910e87fe0b2e2144e9b9756b5dc5cef88b3d3f",
    "stderr":
        "addac86a8584f1a097ddf37a779e30f2c573657e7323c9494dc0429b4504f7bf",
    "stdout":
        "ca33e31584f0c35708936f59e721de8185139ffda918731f4112d332e0e78a0b",
    "time":
        "37e3ddae3a809c6dca70e926f9f2ce669146c28813a35ba6dafdbee56c55b16c",
    "trace":
        "8421884d2dd3f7763dc666eeeac5d336062f75f9f677ea70a747ee7f8eb99314",
}

CELL_LEDGER = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion_cell_ledger.jsonl.gz"
)
WHOLE_ORIGIN_LEDGER = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion_whole_origin_ledger.jsonl.gz"
)
HELD_LEDGER = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion_inherited_h_obstruction_ledger.jsonl.gz"
)
RESULT = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion_result.json"
)

SEALED_MEMBERS = {
    CELL_LEDGER:
        "c4c0061a08983471428b2e5113aff60bbeccc67530cac691658a6bbad1ce9904",
    HELD_LEDGER:
        "f86c6c3d90a4a87c7d4366b86a0e8119d019cbf86f5b5ab781140605ddc1e80e",
    RESULT:
        "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48",
    WHOLE_ORIGIN_LEDGER:
        "778995522629a362183159420860b65d60c8719bc1453c4fc2657e8e8fba9649",
}

BASE_MANIFEST_MEMBERS = {
    "cm2_round306c30a_python_flint_requirements.lock":
        "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c",
    "cm2_round306c30a_python_flint_runtime_lock.json":
        "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79",
    (
        "cm2_round306c30a_runtime/python_flint-0.9.0-cp310-abi3-"
        "manylinux2014_x86_64.manylinux_2_17_x86_64.whl"
    ): "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_attack_harness.py"
    ): "debdb1ac9d3b840660600cec66dd2b6b1d45eb5847d366c989a652f893bb3c17",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_cold_replay.md"
    ): "6bac45a8150603370380afca729220fc2c6da9e3d3580ea3b535b9d2b37a94c5",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_independent_verifier.py"
    ): "5af75a97e9c306cc47a514e4c87ae875a8388bb75d9274d106b64e2ceee87c7c",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_producer.py"
    ): PRODUCER_SHA256,
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_report.md"
    ): "e2811b8c9a676e08e1e3014a10ca693ee651f4d143b38540a1ac53195f4b8562",
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_whole_origin_"
        "promotion_verification.json"
    ): "f02f7e3144541284819947c549ce91d8f1d6e9df24c0bdb4b981077f1e358d07",
    f"cm2_round306c30a_sealed/{CELL_LEDGER}": SEALED_MEMBERS[CELL_LEDGER],
    f"cm2_round306c30a_sealed/{HELD_LEDGER}": SEALED_MEMBERS[HELD_LEDGER],
    f"cm2_round306c30a_sealed/{RESULT}": SEALED_MEMBERS[RESULT],
    f"cm2_round306c30a_sealed/{WHOLE_ORIGIN_LEDGER}":
        SEALED_MEMBERS[WHOLE_ORIGIN_LEDGER],
}

EXPECTED_STDOUT_OBJECT = {
    "result_sha256":
        "32c449bc9af41a22ab5468d194431d14fadf5bc95b30067d639f9e4443538e09",
    "status": (
        "PASS_12888_REDUCED_CLIPPED_DELTA_CELLS_DISPOSED__"
        "12868_EXCLUDED__20_RESERVED_FOR_FULL_DELTA__"
        "160_WHOLE_SOURCE_W_ORIGINS_PROMOTED__"
        "2_INHERITED_H_OBSTRUCTIONS_HELD__D02_STILL_BLOCKED"
    ),
}

EXPECTED_PYTHON = {
    "cache_tag": "cpython-312",
    "dont_write_bytecode": 1,
    "hash_algorithm": "siphash13",
    "hash_randomization": 1,
    "hash_width": 64,
    "ignore_environment": 0,
    "isolated": 0,
    "no_user_site": 1,
    "safe_path": True,
    "version": "3.12.3",
}

NETWORK_SYSCALLS = {
    "accept", "accept4", "bind", "connect", "getpeername", "getsockname",
    "getsockopt", "listen", "recv", "recvfrom", "recvmmsg", "recvmsg",
    "send", "sendmmsg", "sendmsg", "sendto", "setsockopt", "shutdown",
    "socket", "socketcall", "socketpair",
}


class Reject(RuntimeError):
    """An evidence or release precondition was not met."""


@dataclass(frozen=True)
class Capture:
    path: str
    raw: bytes
    sha256: str
    size: int
    stat_tuple: tuple[int, ...]


@dataclass(frozen=True)
class DirectoryCapture:
    path: str
    members: dict[str, Capture]
    stat_tuple: tuple[int, ...]


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("ascii")


def stat_tuple(status: os.stat_result) -> tuple[int, ...]:
    return (
        status.st_dev,
        status.st_ino,
        status.st_mode,
        status.st_nlink,
        status.st_size,
        status.st_mtime_ns,
        status.st_ctime_ns,
    )


def ensure_no_symlink_chain(path: Path) -> None:
    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        status = os.lstat(current)
        require(not stat.S_ISLNK(status.st_mode), "symlink chain:" + str(current))


def capture_regular(
    path: Path,
    *,
    maximum: int = 256 * 1024 * 1024,
    allow_empty: bool = False,
) -> Capture:
    absolute = Path(os.path.abspath(os.fspath(path)))
    ensure_no_symlink_chain(absolute)
    before_path = absolute.lstat()
    require(
        stat.S_ISREG(before_path.st_mode)
        and before_path.st_nlink == 1
        and before_path.st_size <= maximum
        and (allow_empty or before_path.st_size > 0),
        "regular singleton bounds:" + str(absolute),
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and stat_tuple(opened) == stat_tuple(before_path),
            "open identity race:" + str(absolute),
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            require(bool(block), "short read:" + str(absolute))
            chunks.append(block)
            remaining -= len(block)
        require(not os.read(descriptor, 1), "growing file:" + str(absolute))
        after = os.fstat(descriptor)
        require(stat_tuple(after) == stat_tuple(opened),
                "fd metadata race:" + str(absolute))
        after_path = absolute.lstat()
        require(stat_tuple(after_path) == stat_tuple(opened),
                "path metadata race:" + str(absolute))
        raw = b"".join(chunks)
        require(len(raw) == opened.st_size, "captured size:" + str(absolute))
        return Capture(
            path=str(absolute),
            raw=raw,
            sha256=sha256(raw),
            size=len(raw),
            stat_tuple=stat_tuple(opened),
        )
    finally:
        os.close(descriptor)


def capture_exact_directory(
    path: Path,
    expected: dict[str, str],
) -> DirectoryCapture:
    absolute = Path(os.path.abspath(os.fspath(path)))
    ensure_no_symlink_chain(absolute)
    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(absolute, flags)
    try:
        before = os.fstat(descriptor)
        require(stat.S_ISDIR(before.st_mode), "candidate not directory:" + str(absolute))
        names = sorted(os.listdir(descriptor))
        require(names == sorted(expected), "candidate exact member map:" + str(absolute))
        members: dict[str, Capture] = {}
        for name in names:
            member_fd = os.open(
                name,
                os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=descriptor,
            )
            try:
                member_before = os.fstat(member_fd)
                require(
                    stat.S_ISREG(member_before.st_mode)
                    and member_before.st_nlink == 1
                    and 0 < member_before.st_size <= 32 * 1024 * 1024,
                    "candidate regular singleton:" + name,
                )
                chunks: list[bytes] = []
                remaining = member_before.st_size
                while remaining:
                    block = os.read(member_fd, min(1 << 20, remaining))
                    require(bool(block), "candidate short read:" + name)
                    chunks.append(block)
                    remaining -= len(block)
                require(not os.read(member_fd, 1), "candidate growing:" + name)
                member_after = os.fstat(member_fd)
                require(
                    stat_tuple(member_before) == stat_tuple(member_after),
                    "candidate member race:" + name,
                )
                raw = b"".join(chunks)
                digest = sha256(raw)
                require(digest == expected[name], "candidate member sha256:" + name)
                members[name] = Capture(
                    path=str(absolute / name),
                    raw=raw,
                    sha256=digest,
                    size=len(raw),
                    stat_tuple=stat_tuple(member_before),
                )
            finally:
                os.close(member_fd)
        require(sorted(os.listdir(descriptor)) == names,
                "candidate member map race:" + str(absolute))
        after = os.fstat(descriptor)
        require(stat_tuple(before) == stat_tuple(after),
                "candidate directory race:" + str(absolute))
        return DirectoryCapture(str(absolute), members, stat_tuple(before))
    finally:
        os.close(descriptor)


def parse_manifest(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise Reject("base manifest ascii") from error
    require(text.endswith("\n"), "base manifest final newline")
    result: dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), 1):
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        require(match is not None, f"base manifest line:{number}")
        digest, relative = match.groups()
        member = Path(relative)
        require(
            not member.is_absolute()
            and relative not in {"", "."}
            and ".." not in member.parts
            and relative not in result,
            "base manifest safe unique member:" + relative,
        )
        result[relative] = digest
    return result


def capture_base_manifest() -> dict[str, Any]:
    # This is deliberately the first filesystem evidence operation in main.
    manifest = capture_regular(BASE_MANIFEST, maximum=64 * 1024)
    require(manifest.sha256 == BASE_MANIFEST_SHA256, "base manifest sha256")
    mapping = parse_manifest(manifest.raw)
    require(mapping == BASE_MANIFEST_MEMBERS, "base manifest exact thirteen-member map")
    member_captures: dict[str, Capture] = {}
    for relative, expected in sorted(mapping.items()):
        captured = capture_regular(DELIVERABLES / relative)
        require(captured.sha256 == expected, "base manifest member sha256:" + relative)
        member_captures[relative] = captured
    seal = capture_exact_directory(SEALED_DIR, SEALED_MEMBERS)
    manifest_after = capture_regular(BASE_MANIFEST, maximum=64 * 1024)
    require(manifest_after == manifest, "base manifest changed during capture")
    for relative, first in member_captures.items():
        second = capture_regular(DELIVERABLES / relative)
        require(second == first, "base member changed during capture:" + relative)
    return {
        "manifest": manifest,
        "members": member_captures,
        "seal": seal,
    }


def load_json_strict(raw: bytes, label: str) -> Any:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            require(key not in result, label + " duplicate key:" + key)
            result[key] = value
        return result

    try:
        return json.loads(
            raw.decode("ascii"),
            object_pairs_hook=pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(
                Reject(label + " non-finite:" + value)
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Reject(label + " strict json") from error


def artifact_record(captured: Capture) -> dict[str, Any]:
    return {
        "path": str(Path(captured.path).relative_to(WORKSPACE)),
        "sha256": captured.sha256,
        "size": captured.size,
        "stat": list(captured.stat_tuple),
    }


def directory_record(captured: DirectoryCapture) -> dict[str, Any]:
    return {
        "path": str(Path(captured.path).relative_to(WORKSPACE)),
        "stat": list(captured.stat_tuple),
        "members": {
            name: artifact_record(item)
            for name, item in sorted(captured.members.items())
        },
    }


def expected_environment(seed: str, pycache: Path) -> dict[str, str]:
    return {
        "HOME": "/nonexistent",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": "/usr/bin:/bin",
        "PYTHONHASHSEED": seed,
        "PYTHONPYCACHEPREFIX": str(pycache),
        "TZ": "UTC",
    }


def validate_provenance(
    seed: str,
    captured: Capture,
    candidate: Path,
    pycache: Path,
) -> dict[str, Any]:
    value = load_json_strict(captured.raw, "seed provenance")
    require(isinstance(value, dict), "seed provenance object")
    require(captured.raw == canonical(value), "seed provenance canonical one-line json")
    payload = dict(value)
    payload_sha = payload.pop("payload_sha256", None)
    require(
        payload_sha == sha256(canonical(payload).removesuffix(b"\n")),
        "seed provenance payload sha256",
    )
    require(
        set(value) == {
            "candidate_relpath", "environment", "expected_output_names",
            "hash_probe_text", "hash_probe_value", "payload_sha256",
            "producer", "pycache_prefix_relpath", "python", "schema",
            "seed", "status",
        },
        "seed provenance exact keys",
    )
    require(
        value["schema"] == "cm2.round306c30a.controlled-hash-seed-replay.v1"
        and value["status"] == "PREFLIGHT_PASS_REPLAY_NOT_YET_COMPLETE"
        and value["seed"] == seed
        and value["hash_probe_text"] == HASH_PROBE_TEXT
        and value["hash_probe_value"] == SEED_PROBES[seed],
        "seed provenance identity and probe",
    )
    require(value["python"] == EXPECTED_PYTHON, "seed provenance python flags")
    require(value["environment"] == expected_environment(seed, pycache),
            "seed provenance exact env-i environment")
    require(
        value["candidate_relpath"] == candidate.relative_to(WORKSPACE).as_posix()
        and value["pycache_prefix_relpath"] == pycache.relative_to(WORKSPACE).as_posix()
        and value["expected_output_names"] == sorted(SEALED_MEMBERS),
        "seed provenance output paths",
    )
    require(
        value["producer"] == {
            "changed_byte_offset": CHANGED_BYTE_OFFSET,
            "compiled_filename": PRODUCER.relative_to(WORKSPACE).as_posix(),
            "path": PRODUCER.relative_to(WORKSPACE).as_posix(),
            "sha256": PRODUCER_SHA256,
            "transform": "ONE_BYTE_ISOLATED_GUARD_1_TO_0",
            "transformed_sha256": TRANSFORMED_PRODUCER_SHA256,
        },
        "seed provenance producer transform",
    )
    return value


def validate_time(seed: str, captured: Capture, *, require_full_trace: bool) -> None:
    try:
        text = captured.raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Reject("time report utf8") from error
    exits = re.findall(r"^\s*Exit status:\s*([^\r\n]+)\s*$", text, re.MULTILINE)
    require(exits == ["0"], "time report exactly one exit status zero")
    require(text.startswith("\tCommand being timed: \"/usr/bin/strace "),
            "time command begins with strace")
    prefix = PREFIXES[seed]
    required_fragments = [
        " -f ", " -yy ", " -s 4096 ", " /usr/bin/env -i ",
        "HOME=/nonexistent",
        f"PYTHONHASHSEED={seed}",
        f"PYTHONPYCACHEPREFIX={prefix}-pycache",
        " -P -s -B ", str(LAUNCHER), "--expected-hash-seed " + seed,
        "--expected-pycache-prefix " + str(prefix) + "-pycache",
        "--candidate-dir " + str(prefix) + "-candidate",
        "--provenance " + str(prefix) + "-provenance.json",
    ]
    require(all(fragment in text for fragment in required_fragments),
            "time command controlled replay shape")
    require(" -I " not in text, "producer command does not use -I")
    if require_full_trace:
        require(" -e trace=all " in text, "seed2 trace=all command")
    else:
        require(" -e trace=all " not in text and "%file" in text,
                "seed1 selective trace is auxiliary")


def capture_seed(seed: str) -> dict[str, Any]:
    prefix = PREFIXES[seed]
    candidate_path = Path(str(prefix) + "-candidate")
    pycache = Path(str(prefix) + "-pycache")
    require(not os.path.lexists(pycache), "pycache prefix remains absent:" + seed)
    paths = {
        "provenance": Path(str(prefix) + "-provenance.json"),
        "stdout": Path(str(prefix) + "-stdout.json"),
        "stderr": Path(str(prefix) + "-stderr.log"),
        "time": Path(str(prefix) + "-time.txt"),
        "trace": Path(str(prefix) + TRACE_SUFFIXES[seed]),
    }
    first = {
        "provenance": capture_regular(paths["provenance"], maximum=64 * 1024),
        "stdout": capture_regular(paths["stdout"], maximum=64 * 1024),
        "stderr": capture_regular(paths["stderr"], maximum=64 * 1024),
        "time": capture_regular(paths["time"], maximum=64 * 1024),
        "trace": capture_regular(paths["trace"], maximum=256 * 1024 * 1024),
    }
    candidate = capture_exact_directory(candidate_path, SEALED_MEMBERS)
    provenance = validate_provenance(
        seed, first["provenance"], candidate_path, pycache
    )
    stdout_value = load_json_strict(first["stdout"].raw, "producer stdout")
    require(
        first["stdout"].raw == canonical(stdout_value)
        and stdout_value == EXPECTED_STDOUT_OBJECT,
        "producer stdout canonical expected object",
    )
    require(
        first["stderr"].raw.endswith(b"\n")
        and len(first["stderr"].raw.splitlines()) == 50,
        "producer stderr retained fifty diagnostics",
    )
    validate_time(seed, first["time"], require_full_trace=(seed == SEEDS[1]))
    second = {
        label: capture_regular(
            paths[label],
            maximum=256 * 1024 * 1024 if label == "trace" else 64 * 1024,
        )
        for label in first
    }
    require(second == first, "seed evidence changed during capture:" + seed)
    candidate_after = capture_exact_directory(candidate_path, SEALED_MEMBERS)
    require(candidate_after == candidate, "candidate changed during capture:" + seed)
    require(not os.path.lexists(pycache), "pycache appeared during capture:" + seed)
    return {
        "seed": seed,
        "prefix": prefix,
        "candidate": candidate,
        "candidate_path": candidate_path,
        "pycache": pycache,
        "paths": paths,
        "files": first,
        "provenance_object": provenance,
    }


def capture_superseded_v1_failure() -> dict[str, Any]:
    """Bind, but never authorize from, the retained six-key v1 failure."""
    prefix = SUPERSEDED_V1_PREFIX
    paths = {
        "provenance": Path(str(prefix) + "-provenance.json"),
        "stdout": Path(str(prefix) + "-stdout.json"),
        "stderr": Path(str(prefix) + "-stderr.log"),
        "time": Path(str(prefix) + "-time.txt"),
        "trace": Path(str(prefix) + "-trace-all.log"),
    }
    captured = {
        label: capture_regular(
            path,
            maximum=256 * 1024 * 1024 if label == "trace" else 64 * 1024,
        )
        for label, path in paths.items()
    }
    require(
        {label: item.sha256 for label, item in captured.items()}
        == SUPERSEDED_V1_PINS,
        "superseded v1 exact evidence pins",
    )
    candidate = capture_exact_directory(
        Path(str(prefix) + "-candidate"), SEALED_MEMBERS
    )
    provenance = load_json_strict(captured["provenance"].raw, "v1 provenance")
    require(
        provenance.get("seed") == SEEDS[1]
        and "HOME" not in provenance.get("environment", {})
        and len(provenance.get("environment", {})) == 6,
        "superseded v1 six-key environment",
    )
    stdout = load_json_strict(captured["stdout"].raw, "v1 stdout")
    require(
        captured["stdout"].raw == canonical(stdout)
        and stdout == EXPECTED_STDOUT_OBJECT,
        "superseded v1 deterministic output",
    )
    try:
        trace_text = captured["trace"].raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Reject("superseded v1 trace utf8") from error
    socket_lines = re.findall(
        r"^[0-9]+ socket\(AF_UNIX,.*\) = [0-9]+<UNIX-STREAM:",
        trace_text,
        re.MULTILINE,
    )
    nscd_lines = re.findall(
        r'^\d+ connect\(.*sun_path="/var/run/nscd/socket".*\) = -1 ENOENT ',
        trace_text,
        re.MULTILINE,
    )
    all_network = re.findall(
        r"^[0-9]+ (?:" + "|".join(sorted(NETWORK_SYSCALLS)) + r")\(",
        trace_text,
        re.MULTILINE,
    )
    require(
        len(socket_lines) == 2
        and len(nscd_lines) == 2
        and len(all_network) == 4,
        "superseded v1 exact four local NSS network syscalls",
    )
    require(not os.path.lexists(Path(str(prefix) + "-pycache")),
            "superseded v1 pycache absent")
    return {
        "candidate": directory_record(candidate),
        "evidence": {
            label: artifact_record(item)
            for label, item in sorted(captured.items())
        },
        "failed_connect_enoent_count": 2,
        "network_syscall_count": 4,
        "reason": "MISSING_HOME_TRIGGERED_LOCAL_NSS_AF_UNIX_ATTEMPTS",
        "release_authority": "NONE",
        "status": "SUPERSEDED_FAIL_CLOSED_NETWORK_SYSCALLS_4",
        "successful_socket_syscall_count": 2,
    }


def verify_guard_transform(producer_raw: bytes) -> dict[str, Any]:
    require(sha256(producer_raw) == PRODUCER_SHA256, "producer source pin")
    require(producer_raw.count(ORIGINAL_GUARD) == 1, "unique original guard")
    require(CONTROLLED_GUARD not in producer_raw, "controlled guard absent upstream")
    transformed = producer_raw.replace(ORIGINAL_GUARD, CONTROLLED_GUARD, 1)
    changes = [
        index
        for index, pair in enumerate(zip(producer_raw, transformed, strict=True))
        if pair[0] != pair[1]
    ]
    require(
        changes == [CHANGED_BYTE_OFFSET]
        and producer_raw[CHANGED_BYTE_OFFSET:CHANGED_BYTE_OFFSET + 1] == b"1"
        and transformed[CHANGED_BYTE_OFFSET:CHANGED_BYTE_OFFSET + 1] == b"0"
        and sha256(transformed) == TRANSFORMED_PRODUCER_SHA256,
        "single byte producer guard transform",
    )
    compile(transformed, str(PRODUCER), "exec", dont_inherit=True)
    return {
        "changed_byte_offset": CHANGED_BYTE_OFFSET,
        "original_sha256": PRODUCER_SHA256,
        "transformed_sha256": TRANSFORMED_PRODUCER_SHA256,
        "transform": "ONE_BYTE_ISOLATED_GUARD_1_TO_0",
    }


def load_pinned_analyzer(raw: bytes) -> types.ModuleType:
    require(sha256(raw) == ANALYZER_SHA256, "strace analyzer sha256")
    name = "_cm2_c30a_pinned_strace_analyzer"
    module = types.ModuleType(name)
    module.__file__ = str(ANALYZER)
    module.__package__ = ""
    sys.modules[name] = module
    try:
        exec(compile(raw, str(ANALYZER), "exec", dont_inherit=True), module.__dict__)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def build_seed2_analyzer_contract(
    analyzer: types.ModuleType,
    seed2: dict[str, Any],
) -> dict[str, Any]:
    files: dict[str, Capture] = seed2["files"]
    candidate_path: Path = seed2["candidate_path"]
    provenance_path: Path = seed2["paths"]["provenance"]
    manifest_bindings = {
        name: f"cm2_round306c30a_sealed/{name}"
        for name in SEALED_MEMBERS
    }
    return {
        "schema": analyzer.CONTRACT_SCHEMA,
        "profile": "c30a-controlled-producer-seed30630929-scrubbed-full-trace-v2",
        "workspace": str(WORKSPACE),
        "paths": {
            "trace": files["trace"].path,
            "stdout": files["stdout"].path,
            "stderr": files["stderr"].path,
            "time": files["time"].path,
            "manifest": str(BASE_MANIFEST),
            "candidate_dir": str(candidate_path),
        },
        "pins": {
            "trace_sha256": files["trace"].sha256,
            "stdout_sha256": files["stdout"].sha256,
            "stderr_sha256": files["stderr"].sha256,
            "time_sha256": files["time"].sha256,
            "manifest_sha256": BASE_MANIFEST_SHA256,
        },
        "manifest_members": BASE_MANIFEST_MEMBERS,
        "candidate_members": SEALED_MEMBERS,
        "candidate_manifest_bindings": manifest_bindings,
        "stdout": {
            "policy": "one-canonical-json-write",
            "expected_object": EXPECTED_STDOUT_OBJECT,
        },
        "stderr": {
            "policy": "c30a-round215-diagnostics",
            "expected_line_count": 50,
        },
        "allowed_write_paths": sorted([
            str(candidate_path),
            str(provenance_path),
            *(str(candidate_path / name) for name in SEALED_MEMBERS),
        ]),
        "protected_roots": [
            str(DELIVERABLES),
            str(WORKSPACE / ".cm2-runtime/python-flint-0.9.0"),
            str(WORKSPACE / ".cm2-runtime/candidates"),
            str(PREFIXES[SEEDS[0]]) + "-candidate",
        ],
        "capture": {
            "require_follow_forks": True,
            "require_fd_path_decoding": True,
            "require_percent_file": True,
            "minimum_string_limit": 4096,
            "required_explicit_syscalls": analyzer.REQUIRED_EXPLICIT_CAPTURE_SYSCALLS,
        },
    }


def decoded_path(analyzer: types.ModuleType, call: Any) -> str | None:
    index: int | None = None
    if call.name in {"open", "stat", "lstat", "access", "readlink", "mkdir"}:
        index = 0
    elif call.name in {
        "openat", "openat2", "newfstatat", "faccessat", "faccessat2",
        "readlinkat", "mkdirat",
    }:
        index = 1
    if index is None or len(call.args) <= index:
        return None
    try:
        raw = analyzer.decode_c_string(call.args[index])
    except Exception:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def supplement_full_trace_audit(
    analyzer: types.ModuleType,
    seed2: dict[str, Any],
    audit: dict[str, Any],
) -> dict[str, Any]:
    trace_raw = seed2["files"]["trace"].raw
    calls = analyzer.parse_trace(trace_raw)
    candidate = str(seed2["candidate_path"])
    seed1_candidate = str(PREFIXES[SEEDS[0]]) + "-candidate"
    historical_root = str(WORKSPACE / ".cm2-runtime/candidates")
    successful_candidate_mkdir: list[int] = []
    failed_candidate_mkdir: list[int] = []
    successful_pyc_access: list[int] = []
    unsuccessful_pyc_probes = 0
    historical_candidate_observations: list[int] = []
    network_attempts: list[int] = []

    for call in calls:
        if call.name in NETWORK_SYSCALLS:
            network_attempts.append(call.line_number)
        path = decoded_path(analyzer, call)
        normalized = None
        if path is not None:
            normalized = str(
                Path(path) if os.path.isabs(path) else WORKSPACE / path
            )
            if call.name in {"mkdir", "mkdirat"} and normalized == candidate:
                if call.result_integer == 0:
                    successful_candidate_mkdir.append(call.line_number)
                else:
                    failed_candidate_mkdir.append(call.line_number)
            if path.endswith(".pyc") and call.name in {"open", "openat", "openat2"}:
                if call.result_integer is not None and call.result_integer >= 0:
                    successful_pyc_access.append(call.line_number)
                else:
                    unsuccessful_pyc_probes += 1
            if (
                (historical_root in normalized or seed1_candidate in normalized)
                and call.result_integer is not None
                and call.result_integer >= 0
            ):
                historical_candidate_observations.append(call.line_number)
        if call.name in {"read", "readv", "pread64", "preadv", "preadv2"}:
            first_arg = call.args[0] if call.args else ""
            if ".pyc>" in first_arg and call.result_integer is not None and call.result_integer >= 0:
                successful_pyc_access.append(call.line_number)
            if (
                (historical_root in first_arg or seed1_candidate in first_arg)
                and call.result_integer is not None
                and call.result_integer >= 0
            ):
                historical_candidate_observations.append(call.line_number)

    require(audit["status"] == "PASS_C30A_STRACE_ZERO_MUTATION_CERTIFIED",
            "pinned full trace analyzer PASS")
    require(audit["errors"] == [], "pinned full trace analyzer zero errors")
    trace_contract = audit["trace_contract"]
    require(
        trace_contract["captures_all_syscalls"] is True
        and trace_contract["capture_complete_for_claimed_scope"] is True
        and trace_contract["missing_explicit_mutation_syscalls"] == []
        and trace_contract["forbidden_mutation_attempt_count"] == 0
        and trace_contract["protected_mutation_attempt_count"] == 0
        and trace_contract["sha256"] == seed2["files"]["trace"].sha256,
        "pinned full trace analyzer release fields",
    )
    require(
        audit["conclusion"]["certifiable_zero_mutation_to_protected_roots"] is True
        and audit["manifest"]["exact_map_matches_contract"] is True
        and audit["manifest"]["members_all_match"] is True
        and audit["candidate"]["manifest_bound"] is True
        and audit["stdout_contract"]["canonical_json"] is True
        and audit["stdout_contract"]["object_matches_contract"] is True
        and audit["time_contract"]["exit_status"] == 0,
        "pinned full trace analyzer semantic fields",
    )
    require(successful_candidate_mkdir and len(successful_candidate_mkdir) == 1,
            "scrubbed trace exactly one successful fresh candidate mkdir")
    require(not failed_candidate_mkdir, "scrubbed trace no failed/reused candidate mkdir")
    require(not successful_pyc_access, "scrubbed trace no successful pyc access")
    require(not historical_candidate_observations,
            "scrubbed trace no successful historical candidate access")
    require(not network_attempts, "scrubbed trace no network syscall")
    require(not os.path.lexists(seed2["pycache"]),
            "scrubbed pycache prefix absent after full trace audit")
    return {
        "analyzer_result_sha256": sha256(canonical(audit)),
        "capture_complete": True,
        "captures_all_syscalls": True,
        "fresh_candidate_mkdir_line": successful_candidate_mkdir[0],
        "historical_candidate_access_count": 0,
        "network_syscall_count": 0,
        "protected_mutation_attempt_count": 0,
        "status": audit["status"],
        "successful_pyc_access_count": 0,
        "unsuccessful_pyc_probe_count": unsuccessful_pyc_probes,
    }


def audit_seed2_trace(
    analyzer_raw: bytes,
    seed2: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    analyzer = load_pinned_analyzer(analyzer_raw)
    # Durable regression check for the exact ambiguity that previously made a
    # producer trace unauditable: child Python's ``-s`` is not strace's ``-s``.
    test_argv = [
        "/usr/bin/strace", "-qq", "-f", "-yy", "-s", "4096",
        "-e", "trace=all", "-o", "trace.raw", "/usr/bin/env", "-i",
        "python", "-P", "-s", "-B", "producer.py",
    ]
    tokens, limit, output, flags = analyzer.parse_trace_filter(test_argv)
    require(
        tokens == {"all"}
        and limit == 4096
        and output == "trace.raw"
        and flags == {"follow_forks": True, "fd_paths": True},
        "analyzer child-python-minus-s option-boundary regression",
    )
    contract = build_seed2_analyzer_contract(analyzer, seed2)
    contract_sha = sha256(analyzer.canonical_bytes(contract))
    audit = analyzer.audit(contract, "pinned-in-process-analyzer", contract_sha)
    supplement = supplement_full_trace_audit(analyzer, seed2, audit)
    supplement["child_python_minus_s_option_boundary_regression"] = "PASS"
    return contract, audit, supplement


def recapture_seed(seed_record: dict[str, Any]) -> None:
    for label, first in seed_record["files"].items():
        second = capture_regular(
            seed_record["paths"][label],
            maximum=256 * 1024 * 1024 if label == "trace" else 64 * 1024,
        )
        require(second == first, "seed evidence changed after audit:" + seed_record["seed"])
    candidate = capture_exact_directory(seed_record["candidate_path"], SEALED_MEMBERS)
    require(candidate == seed_record["candidate"],
            "candidate changed after audit:" + seed_record["seed"])
    require(not os.path.lexists(seed_record["pycache"]),
            "pycache appeared after audit:" + seed_record["seed"])


def recapture_base(base: dict[str, Any]) -> None:
    manifest = capture_regular(BASE_MANIFEST, maximum=64 * 1024)
    require(manifest == base["manifest"], "base manifest changed after comparison")
    for relative, first in base["members"].items():
        second = capture_regular(DELIVERABLES / relative)
        require(second == first, "base member changed after comparison:" + relative)
    seal = capture_exact_directory(SEALED_DIR, SEALED_MEMBERS)
    require(seal == base["seal"], "base seal changed after comparison")


def success_receipt(
    base: dict[str, Any],
    seed_records: dict[str, dict[str, Any]],
    dependencies: dict[str, Capture],
    transform: dict[str, Any],
    contract: dict[str, Any],
    trace_audit: dict[str, Any],
    trace_supplement: dict[str, Any],
    superseded_v1: dict[str, Any],
) -> dict[str, Any]:
    seed1 = seed_records[SEEDS[0]]
    seed2 = seed_records[SEEDS[1]]
    require(SEED_PROBES[SEEDS[0]] != SEED_PROBES[SEEDS[1]],
            "controlled hash probes are distinct")
    require(seed1["files"]["stdout"].raw == seed2["files"]["stdout"].raw,
            "producer stdout bytes identical across seeds")
    require(seed1["files"]["stderr"].raw == seed2["files"]["stderr"].raw,
            "producer diagnostic bytes identical across seeds")
    for name, sealed in base["seal"].members.items():
        first = seed1["candidate"].members[name]
        second = seed2["candidate"].members[name]
        require(first.raw == second.raw == sealed.raw,
                "candidate bytes equal both seeds and seal:" + name)

    seed_receipts: dict[str, Any] = {}
    for seed in SEEDS:
        item = seed_records[seed]
        files: dict[str, Capture] = item["files"]
        seed_receipts[seed] = {
            "candidate": directory_record(item["candidate"]),
            "completion": {
                "exit_status": 0,
                "producer_stdout_matches_expected": True,
                "stderr_diagnostic_line_count": 50,
            },
            "environment": expected_environment(seed, item["pycache"]),
            "evidence": {
                label: artifact_record(captured)
                for label, captured in sorted(files.items())
            },
            "hash_probe": {
                "text": HASH_PROBE_TEXT,
                "value": SEED_PROBES[seed],
            },
            "provenance_status": item["provenance_object"]["status"],
            "pycache_prefix_absent_after_run": True,
            "python_flags": EXPECTED_PYTHON,
            "trace_role": (
                "AUXILIARY_NON_AUTHORIZING_SELECTIVE_TRACE"
                if seed == SEEDS[0]
                else "RELEASE_AUTHORIZING_SCRUBBED_TRACE_ALL"
            ),
        }

    receipt = {
        "base_authority": {
            "manifest_member_count": 13,
            "manifest_members": BASE_MANIFEST_MEMBERS,
            "manifest_sha256": BASE_MANIFEST_SHA256,
            "seal": directory_record(base["seal"]),
        },
        "comparisons": {
            "candidate_files_seed1_equal_seed2": True,
            "candidate_files_seed1_equal_seal": True,
            "candidate_files_seed2_equal_seal": True,
            "candidate_member_count_each": 4,
            "hash_probes_distinct": True,
            "producer_stderr_bytes_identical": True,
            "producer_stdout_bytes_identical": True,
            "producer_stdout_sha256": seed1["files"]["stdout"].sha256,
        },
        "conclusion": {
            "additional_whole_origin_credit": 0,
            "d02": "BLOCKED",
            "held_whole_origins": 2,
            "original_c30a_whole_origin_exclusions": 160,
            "source_w_transition": "252->92",
            "transition_252_to_90": "FORBIDDEN",
        },
        "dependencies": {
            name: artifact_record(item)
            for name, item in sorted(dependencies.items())
        },
        "producer_guard_transform": transform,
        "schema": SCHEMA,
        "seed2_full_trace_analyzer": {
            "contract": contract,
            "contract_sha256": sha256(canonical(contract)),
            "result": trace_audit,
            "supplement": trace_supplement,
        },
        "seeds": seed_receipts,
        "status": (
            "PASS_C30A_CONTROLLED_DUAL_SEED_EVIDENCE__"
            "ADDITIONAL_CREDIT_0__252_TO_92_ONLY__252_TO_90_FORBIDDEN"
        ),
        "superseded_v1_fail_closed": superseded_v1,
    }
    receipt["payload_sha256"] = sha256(canonical(receipt))
    return receipt


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audit-root",
        type=Path,
        default=AUDIT_ROOT,
        help="must resolve to the frozen .cm2-runtime/audit root",
    )
    return parser.parse_args(argv)


def run(argv: list[str]) -> dict[str, Any]:
    arguments = parse_arguments(argv)
    # Manifest-first boundary: do not inspect any replay evidence before this.
    base = capture_base_manifest()

    require(
        arguments.audit_root.resolve(strict=True) == AUDIT_ROOT.resolve(strict=True),
        "fixed audit root",
    )

    dependencies = {
        "launcher": capture_regular(LAUNCHER, maximum=256 * 1024),
        "protocol": capture_regular(PROTOCOL, maximum=256 * 1024),
        "strace_analyzer": capture_regular(ANALYZER, maximum=256 * 1024),
    }
    require(dependencies["launcher"].sha256 == LAUNCHER_SHA256,
            "controlled replay launcher sha256")
    require(dependencies["protocol"].sha256 == PROTOCOL_SHA256,
            "supplemental protocol sha256")
    require(dependencies["strace_analyzer"].sha256 == ANALYZER_SHA256,
            "strace analyzer sha256")
    transform = verify_guard_transform(base["members"][PRODUCER.name].raw)
    superseded_v1 = capture_superseded_v1_failure()

    seed_records = {seed: capture_seed(seed) for seed in SEEDS}
    contract, trace_audit, trace_supplement = audit_seed2_trace(
        dependencies["strace_analyzer"].raw,
        seed_records[SEEDS[1]],
    )

    for item in seed_records.values():
        recapture_seed(item)
    recapture_base(base)
    require(capture_superseded_v1_failure() == superseded_v1,
            "superseded v1 evidence changed during comparison")
    for name, first in dependencies.items():
        second = capture_regular(Path(first.path), maximum=256 * 1024)
        require(second == first, "dependency changed during comparison:" + name)

    return success_receipt(
        base,
        seed_records,
        dependencies,
        transform,
        contract,
        trace_audit,
        trace_supplement,
        superseded_v1,
    )


def failure_receipt(error: Exception) -> dict[str, Any]:
    return {
        "conclusion": {
            "additional_whole_origin_credit": 0,
            "d02": "BLOCKED",
            "source_w_transition": "252->92",
            "transition_252_to_90": "FORBIDDEN",
        },
        "errors": [f"{type(error).__name__}:{error}"],
        "schema": SCHEMA,
        "status": "FAIL_CLOSED_C30A_CONTROLLED_DUAL_SEED_EVIDENCE",
    }


def main(argv: list[str] | None = None) -> int:
    try:
        receipt = run(sys.argv[1:] if argv is None else argv)
    except Exception as error:  # one canonical fail-close boundary
        receipt = failure_receipt(error)
    sys.stdout.buffer.write(canonical(receipt))
    return 0 if receipt["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
