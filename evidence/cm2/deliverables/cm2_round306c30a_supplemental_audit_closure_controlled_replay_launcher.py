#!/usr/bin/env python3
"""Controlled-hash-seed replay launcher for the sealed C30a producer.

This is an additive audit tool.  It never edits the sealed producer.  It pins
the producer bytes, changes exactly the single isolated-runtime guard from
``isolated == 1`` to ``isolated == 0`` in memory, and executes the resulting
code with the original producer filename.  The change is necessary because
CPython ``-I`` ignores ``PYTHONHASHSEED``; this launcher must instead be run
with ``env -i`` and ``python -P -s -B`` as frozen in the supplemental protocol.
The exact environment includes ``HOME=/nonexistent`` so Python startup does
not perform an NSS lookup (and therefore no AF_UNIX nscd socket attempt).

The two permitted seeds have distinct, pinned hash probes.  A provenance JSON
file is exclusively created before the expensive replay begins.  Any source,
environment, flag, seed, path, or transform mismatch fails closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

SCRIPT = Path(__file__).resolve(strict=True)
DELIVERABLES = SCRIPT.parent
WORKSPACE = DELIVERABLES.parent
PRODUCER_NAME = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion_producer.py"
)
PRODUCER = DELIVERABLES / PRODUCER_NAME
PRODUCER_SHA256 = (
    "41a3f11c3e44bdbbfcf95edf88902669365186e6fb6394aaee15a6846dc91714"
)
ORIGINAL_GUARD = (
    b"sys.flags.isolated == 1 and sys.dont_write_bytecode is True,"
)
CONTROLLED_GUARD = (
    b"sys.flags.isolated == 0 and sys.dont_write_bytecode is True,"
)
HASH_PROBE_TEXT = "CM2-C30a-controlled-hash-seed-v1"
SEED_PROBES = {
    "30630071": 8841297538927089933,
    "30630929": 889641737497572634,
}
EXACT_ENVIRONMENT = {
    "HOME": "/nonexistent",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PATH": "/usr/bin:/bin",
    "TZ": "UTC",
}
EXPECTED_VENV = WORKSPACE / ".cm2-runtime/python-flint-0.9.0"
OUTPUT_NAMES = {
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
        "whole_origin_promotion_cell_ledger.jsonl.gz"
    ),
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
        "whole_origin_promotion_whole_origin_ledger.jsonl.gz"
    ),
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
        "whole_origin_promotion_inherited_h_obstruction_ledger.jsonl.gz"
    ),
    (
        "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
        "whole_origin_promotion_result.json"
    ),
}


class Reject(RuntimeError):
    """A controlled replay precondition was not met."""


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


def read_regular(path: Path, maximum: int = 8 * 1024 * 1024) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    status = absolute.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1
        and 0 < status.st_size <= maximum,
        "regular singleton:" + os.fspath(path),
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
            and (opened.st_dev, opened.st_ino, opened.st_size)
            == (status.st_dev, status.st_ino, status.st_size),
            "opened identity:" + os.fspath(path),
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            require(bool(block), "short read:" + os.fspath(path))
            chunks.append(block)
            remaining -= len(block)
        require(not os.read(descriptor, 1), "growing input:" + os.fspath(path))
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def write_exclusive(path: Path, raw: bytes) -> None:
    require(path.parent.is_dir() and not path.parent.is_symlink(),
            "provenance parent")
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    complete = False
    try:
        offset = 0
        payload = raw + b"\n"
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            require(written > 0, "provenance short write")
            offset += written
        os.fsync(descriptor)
        complete = True
    finally:
        os.close(descriptor)
        if not complete:
            try:
                path.unlink()
            except OSError:
                pass


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-hash-seed", choices=sorted(SEED_PROBES),
                        required=True)
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--provenance", required=True)
    parser.add_argument("--expected-pycache-prefix", required=True)
    return parser.parse_args(argv)


def preflight(arguments: argparse.Namespace) -> tuple[bytes, dict[str, Any]]:
    require(SCRIPT.parent == DELIVERABLES, "launcher canonical location")
    expected_environment = {
        **EXACT_ENVIRONMENT,
        "PYTHONHASHSEED": arguments.expected_hash_seed,
        "PYTHONPYCACHEPREFIX": arguments.expected_pycache_prefix,
    }
    require(dict(os.environ) == expected_environment,
            "env -i exact environment")
    require(
        sys.flags.isolated == 0
        and sys.flags.ignore_environment == 0
        and sys.flags.safe_path is True
        and sys.flags.no_user_site == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.flags.hash_randomization == 1
        and sys.dont_write_bytecode is True,
        "required python -P -s -B flags without -I",
    )
    require(
        sys.prefix != sys.base_prefix
        and Path(sys.prefix).resolve(strict=True)
        == EXPECTED_VENV.resolve(strict=True),
        "locked venv prefix",
    )
    require(
        sys.implementation.name == "cpython"
        and sys.implementation.cache_tag == "cpython-312"
        and tuple(sys.version_info[:3]) == (3, 12, 3),
        "locked CPython identity",
    )
    actual_probe = hash(HASH_PROBE_TEXT)
    require(actual_probe == SEED_PROBES[arguments.expected_hash_seed],
            "controlled hash seed probe")

    candidate = Path(arguments.candidate_dir)
    candidate_absolute = Path(os.path.abspath(os.fspath(candidate)))
    require(
        not candidate_absolute.exists()
        and candidate_absolute != WORKSPACE
        and candidate_absolute != DELIVERABLES
        and candidate_absolute.is_relative_to(WORKSPACE / ".cm2-runtime"),
        "fresh candidate path inside .cm2-runtime",
    )
    provenance = Path(arguments.provenance)
    provenance_absolute = Path(os.path.abspath(os.fspath(provenance)))
    require(
        not provenance_absolute.exists()
        and provenance_absolute.is_relative_to(WORKSPACE / ".cm2-runtime")
        and not provenance_absolute.is_relative_to(candidate_absolute),
        "fresh provenance path inside .cm2-runtime and outside candidate",
    )
    pycache = Path(arguments.expected_pycache_prefix)
    pycache_absolute = Path(os.path.abspath(os.fspath(pycache)))
    require(
        not pycache_absolute.exists()
        and pycache_absolute.is_relative_to(WORKSPACE / ".cm2-runtime")
        and not pycache_absolute.is_relative_to(candidate_absolute)
        and pycache_absolute != provenance_absolute
        and sys.pycache_prefix == os.fspath(pycache_absolute),
        "fresh isolated pycache prefix inside .cm2-runtime",
    )

    source = read_regular(PRODUCER)
    require(sha256(source) == PRODUCER_SHA256, "sealed producer sha256")
    require(source.count(ORIGINAL_GUARD) == 1, "unique original guard")
    require(CONTROLLED_GUARD not in source, "controlled guard absent upstream")
    transformed = source.replace(ORIGINAL_GUARD, CONTROLLED_GUARD, 1)
    differences = [
        index
        for index, pair in enumerate(zip(source, transformed, strict=True))
        if pair[0] != pair[1]
    ]
    require(
        len(source) == len(transformed)
        and len(differences) == 1
        and source[differences[0]:differences[0] + 1] == b"1"
        and transformed[differences[0]:differences[0] + 1] == b"0",
        "single-byte isolated guard transform",
    )
    # Compile before emitting provenance so syntax failure leaves no apparent
    # launch record.  The original producer path is retained for __file__/ROOT.
    compile(transformed, os.fspath(PRODUCER), "exec", dont_inherit=True)
    provenance_object: dict[str, Any] = {
        "schema": "cm2.round306c30a.controlled-hash-seed-replay.v1",
        "status": "PREFLIGHT_PASS_REPLAY_NOT_YET_COMPLETE",
        "seed": arguments.expected_hash_seed,
        "hash_probe_text": HASH_PROBE_TEXT,
        "hash_probe_value": actual_probe,
        "python": {
            "version": ".".join(str(value) for value in sys.version_info[:3]),
            "cache_tag": sys.implementation.cache_tag,
            "hash_algorithm": sys.hash_info.algorithm,
            "hash_width": sys.hash_info.width,
            "isolated": sys.flags.isolated,
            "ignore_environment": sys.flags.ignore_environment,
            "safe_path": sys.flags.safe_path,
            "no_user_site": sys.flags.no_user_site,
            "dont_write_bytecode": sys.flags.dont_write_bytecode,
            "hash_randomization": sys.flags.hash_randomization,
        },
        "environment": expected_environment,
        "producer": {
            "path": PRODUCER.relative_to(WORKSPACE).as_posix(),
            "sha256": sha256(source),
            "transformed_sha256": sha256(transformed),
            "transform": "ONE_BYTE_ISOLATED_GUARD_1_TO_0",
            "changed_byte_offset": differences[0],
            "compiled_filename": PRODUCER.relative_to(WORKSPACE).as_posix(),
        },
        "candidate_relpath": candidate_absolute.relative_to(WORKSPACE).as_posix(),
        "pycache_prefix_relpath":
            pycache_absolute.relative_to(WORKSPACE).as_posix(),
        "expected_output_names": sorted(OUTPUT_NAMES),
    }
    provenance_object["payload_sha256"] = sha256(canonical(provenance_object))
    write_exclusive(provenance_absolute, canonical(provenance_object))
    return transformed, provenance_object


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    try:
        transformed, _ = preflight(arguments)
    except Exception as error:
        print(
            "C30A_CONTROLLED_REPLAY_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1

    producer_globals: dict[str, Any] = {
        "__name__": "__main__",
        "__file__": os.fspath(PRODUCER),
        "__package__": None,
        "__cached__": None,
    }
    sys.argv = [os.fspath(PRODUCER), "--candidate-dir", arguments.candidate_dir]
    exec(
        compile(transformed, os.fspath(PRODUCER), "exec", dont_inherit=True),
        producer_globals,
        producer_globals,
    )
    raise AssertionError("sealed producer main returned without SystemExit")


if __name__ == "__main__":
    raise SystemExit(main())
