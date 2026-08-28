#!/usr/bin/env python3
"""Safely materialize the canonical Round218 bounded-probe result."""

from __future__ import annotations

import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any

from flint import ctx


HERE = Path(__file__).resolve().parent
PROBE_NAME = "cm2_round218_source_w_compact_q_source_stratum_frontier.py"
PROBE_SHA256 = (
    "1dadb46be62853391898314b4a9fbbf5aae2750e70a21e3d891e975f45a3cfbf"
)
RESULT_NAME = (
    "cm2_round218_source_w_compact_q_source_stratum_frontier_result.json"
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def read_regular(path: Path, maximum: int = 512 * 1024) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE
        and absolute.parent.resolve() == HERE,
        f"input parent:{absolute.name}",
    )
    status = absolute.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1
        and 0 < status.st_size <= maximum,
        f"input object:{absolute.name}",
    )
    descriptor = os.open(
        absolute, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino)
            == (status.st_dev, status.st_ino)
            and stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size == status.st_size,
            f"input race:{absolute.name}",
        )
        raw = os.read(descriptor, opened.st_size)
        require(
            len(raw) == opened.st_size
            and not os.read(descriptor, 1),
            f"input bytes:{absolute.name}",
        )
    finally:
        os.close(descriptor)
    return raw


def output_allowed(path: Path) -> bool:
    try:
        resolved_parent = path.parent.resolve(strict=True)
    except OSError:
        return False
    if not (
        resolved_parent == HERE.resolve()
        and path.parent.absolute() == HERE.resolve()
        and path.name == RESULT_NAME
        and ".." not in path.parts
    ):
        return False
    if path.exists() or path.is_symlink():
        try:
            status = path.lstat()
        except OSError:
            return False
        return (
            stat.S_ISREG(status.st_mode)
            and not path.is_symlink()
            and status.st_nlink == 1
        )
    return True


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode()


def atomic_write(path: Path, payload: bytes) -> None:
    require(output_allowed(path), "authorized Round218 result output")
    descriptor, name = tempfile.mkstemp(
        prefix=".cm2_round218_result_", suffix=".tmp", dir=HERE
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(HERE, os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


require(
    hashlib.sha256(read_regular(HERE / PROBE_NAME)).hexdigest()
    == PROBE_SHA256,
    "Round218 probe pre-import pin",
)
if os.fspath(HERE) not in sys.path:
    sys.path.insert(0, os.fspath(HERE))
probe = importlib.import_module(PROBE_NAME[:-3])
require(
    Path(probe.__file__).resolve() == (HERE / PROBE_NAME).resolve(),
    "Round218 probe module identity",
)
require(
    hashlib.sha256(read_regular(HERE / PROBE_NAME)).hexdigest()
    == PROBE_SHA256,
    "Round218 probe post-import pin",
)


def main() -> int:
    ctx.prec = 192
    result = probe.rebuild()
    document = {
        "schema": probe.SCHEMA,
        "result": result,
        "result_sha256": probe.digest(result),
    }
    atomic_write(HERE / RESULT_NAME, pretty_bytes(document))
    print(document["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
