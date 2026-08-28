#!/usr/bin/env python3
"""r46 append-only exact8 -> manifest -> outer-last adapter.

The r46 namespace is bound to the immutable r40 implementation through the
reviewed r41 adapter provenance.  Only the r46 config is translated in
memory; no prior candidate bytes are rewritten or reused.  A stale-residue
scan is an additional read-only gate, and publication requires the explicit
r46 acknowledgement token.
"""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import hashlib
import json
import os
import stat
import subprocess
import sys
from types import ModuleType
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
R41_ADAPTER = ROOT / "scripts/c79g_v16r2r41_cold_freeze_adapter.py"
R40_ADAPTER = ROOT / "scripts/c79g_v16r2r40_cold_freeze_adapter.py"
R41_ADAPTER_SHA256 = "a6e54aeb0314ac4d08979e25727c756cce47907b744b9b4366ab82e52c735f06"
R40_ADAPTER_SHA256 = "4ad1f559fc37ca835dce2897eced5802e119a3acdbf461f92cd05a51343ba449"
R46_SCHEMA = "cm2.c79g.r46.cold-freeze-config.v1"
R40_SCHEMA = "cm2.c79g.r40.cold-freeze-config.v1"
R46_TAG = "v16r2r46"
R44_TAG = "v16r2r44"
R46_ACK_ENV = "CM2_R46_PUBLISH_ACK"
R46_ACK = "EXACT8_MANIFEST_OUTER_LAST_R46"
R46_SCANNER_REL = "scripts/c79g_v16r2r42_stale_residue_scanner.py"
R46_SCANNER_SHA256 = "e5fdf024066984cbe74c8b988446b4c43204cb6a1cea7a9f67c511ee0bf9545b"
R45_PYC_REL = "scripts/__pycache__/c79g_v16r2r45_candidate_builder.cpython-312.pyc"
R45_PYC_SHA256 = "1c813fcba09c07a2613c1d3e96160edba2bc1fa80000ef464ac91b1e806ac892"
R45_PYC_SIZE = 41065
_PYC_INVENTORY: tuple[tuple[str, str, int, int, int], ...] | None = None


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _held_read(path: Path, expected_mode: int | None = None) -> bytes:
    """Read a tooling artifact through one held, no-follow descriptor."""
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (expected_mode is not None and stat.S_IMODE(before.st_mode) != expected_mode) or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable tooling artifact:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        named_after = os.lstat(path)
        if (len(raw) != before.st_size or
                (before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise RuntimeError(f"tooling artifact drift:{path}")
        return raw
    finally:
        os.close(fd)


def _pyc_inventory() -> tuple[tuple[str, str, int, int, int], ...]:
    rows: list[tuple[str, str, int, int, int]] = []
    for path in sorted(ROOT.rglob("*.pyc")):
        st = os.lstat(path)
        if (not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or
                path.is_symlink()):
            raise RuntimeError(f"invalid pyc artifact:{path}")
        raw = _held_read(path)
        rows.append((str(path.relative_to(ROOT)), sha(raw), len(raw),
                     stat.S_IMODE(st.st_mode), st.st_nlink))
    return tuple(rows)


def _assert_tooling_state() -> None:
    """Pin historical r45 PYC and keep the complete inventory immutable."""
    global _PYC_INVENTORY
    inventory = _pyc_inventory()
    expected = (str(Path(R45_PYC_REL)), R45_PYC_SHA256, R45_PYC_SIZE, 0o664, 1)
    rows = {row[0]: row for row in inventory}
    if rows.get(R45_PYC_REL) != expected:
        raise RuntimeError("r45 tooling-pyc witness drift")
    if any(R46_TAG in row[0] for row in inventory):
        raise RuntimeError("r46 pyc present")
    if _PYC_INVENTORY is None:
        _PYC_INVENTORY = inventory
    elif inventory != _PYC_INVENTORY:
        raise RuntimeError("pyc inventory changed during clean-room run")


def exec_pinned(path: Path, expected_sha: str, name: str) -> ModuleType:
    raw = path.read_bytes()
    if sha(raw) != expected_sha:
        raise RuntimeError(f"tooling source hash drift:{path}")
    tree = ast.parse(raw.decode("utf-8"), filename=str(path), mode="exec")
    module = ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = None
    sys.modules[name] = module
    exec(compile(tree, str(path), "exec"), module.__dict__, module.__dict__)
    return module


def load_base() -> ModuleType:
    # Execute r41 only for provenance, then load the pinned r40 parser/core.
    _assert_tooling_state()
    r41 = exec_pinned(R41_ADAPTER, R41_ADAPTER_SHA256, "_r46_r41_adapter_provenance")
    _assert_tooling_state()
    if getattr(r41, "BASE_ADAPTER_SHA256", None) != R40_ADAPTER_SHA256:
        raise RuntimeError("r41 declared r40 template pin drift")
    result = exec_pinned(R40_ADAPTER, R40_ADAPTER_SHA256, "_r46_r40_adapter")
    _assert_tooling_state()
    return result


class ConfigProxy:
    """Read-only view translating exactly one config schema literal."""

    def __init__(self, path: Path):
        self.path = path.resolve()

    def read_bytes(self) -> bytes:
        raw = self.path.read_bytes()
        old = R46_SCHEMA.encode("ascii")
        if raw.count(old) != 1:
            raise ValueError("r46 config schema literal count")
        return raw.replace(old, R40_SCHEMA.encode("ascii"), 1)

    def resolve(self) -> Path:
        return self.path

    def __str__(self) -> str:
        return str(self.path)


def load_config(path: Path):
    base = load_base()
    resolved = path.resolve()
    cfg = base.load_config(ConfigProxy(resolved))
    if cfg.tag != R46_TAG or cfg.predecessor != R44_TAG:
        raise ValueError("r46 config must bind v16r2r46<-v16r2r44")
    meta = json.loads(resolved.read_bytes().decode("utf-8"))
    scripts = meta.get("review_scripts") if isinstance(meta, dict) else None
    scanner_rel = scripts.get("stale_scan") if isinstance(scripts, dict) else None
    if scanner_rel != R46_SCANNER_REL:
        raise ValueError("r46 stale scanner path pin")
    scanner = ROOT / R46_SCANNER_REL
    if meta.get("stale_scanner_sha256") != R46_SCANNER_SHA256 or sha(scanner.read_bytes()) != R46_SCANNER_SHA256:
        raise ValueError("r46 stale scanner source hash drift")
    return base, cfg, resolved


def run_stale_scan(cfg: Any, config_path: Path) -> dict[str, Any]:
    _assert_tooling_state()
    scanner = ROOT / R46_SCANNER_REL
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "CM2_STALE_SCAN_TAG": cfg.tag,
                "CM2_STALE_SCAN_PREV": cfg.predecessor,
                "CM2_R46_CONFIG": str(config_path)})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", str(scanner)],
                          cwd=str(ROOT), env=env, capture_output=True,
                          check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"r46 stale scanner rc={proc.returncode}:{proc.stderr[-600:]!r}")
    _assert_tooling_state()
    value = json.loads(proc.stdout.decode("utf-8"))
    if (not isinstance(value, dict) or value.get("failed_check_count") != 0 or
            value.get("read_only") is not True or value.get("writes_performed") is not False or
            value.get("formal_global_closure_credit") != 0 or value.get("D02_unlock") is not False or
            value.get("runtime_authorized") is not False):
        raise RuntimeError("r46 stale scanner zero-credit predicate failed")
    return value


def guard_entrypoint(config_path: Path, argv: list[str]) -> int:
    base, cfg, resolved = load_config(config_path)
    if argv != ["--preflight"]:
        raise ValueError("r46 guard accepts only --preflight")
    run_stale_scan(cfg, resolved)
    return int(base.guard_entrypoint(ConfigProxy(resolved), argv))


def publisher_entrypoint(config_path: Path, publish: bool) -> int:
    base, cfg, resolved = load_config(config_path)
    if not publish:
        raise ValueError("r46 publisher refuses without --publish")
    if os.environ.get(R46_ACK_ENV) != R46_ACK:
        raise ValueError("missing r46 publish acknowledgement token")
    run_stale_scan(cfg, resolved)
    return int(base.build_publisher(cfg).main())


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args(argv)
    if args.preflight == args.publish:
        raise ValueError("choose exactly one of --preflight/--publish")
    if args.preflight:
        return guard_entrypoint(args.config, ["--preflight"])
    return publisher_entrypoint(args.config, True)


if __name__ == "__main__":
    try:
        raise SystemExit(cli())
    except Exception as exc:
        print(f"R46_ADAPTER_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
