#!/usr/bin/env python3
"""r43 append-only cold-freeze adapter (tooling only).

The adapter binds a fresh r43 config to the immutable r43 exact8 and delegates
the reviewed r40 guard/publisher implementation in memory.  The r41 and r40
tooling sources are pinned and AST/compiled in memory; no source-file import
or bytecode cache is used.  A read-only r43 stale-residue scanner is an
additional hard predicate before the inherited seven-check guard runs.

Publication is impossible without both ``--publish`` and
``CM2_R43_PUBLISH_ACK=EXACT8_MANIFEST_OUTER_LAST_R43``.  This module never
creates a manifest/outer/runtime surface merely by being loaded.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
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
R43_SCHEMA = "cm2.c79g.r43.cold-freeze-config.v1"
R40_SCHEMA = "cm2.c79g.r40.cold-freeze-config.v1"
R43_TAG = "v16r2r43"
R42_TAG = "v16r2r42"
R43_ACK_ENV = "CM2_R43_PUBLISH_ACK"
R43_ACK = "EXACT8_MANIFEST_OUTER_LAST_R43"
R43_SCANNER_REL = "scripts/c79g_v16r2r43_stale_residue_scanner.py"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def exec_pinned(path: Path, expected_sha: str, name: str) -> ModuleType:
    """AST-compile and execute a tooling source without SourceFileLoader."""
    raw = path.read_bytes()
    if sha(raw) != expected_sha:
        raise RuntimeError(f"tooling source hash drift:{path}")
    tree = ast.parse(raw.decode("utf-8"), filename=str(path), mode="exec")
    code = compile(tree, str(path), "exec")
    module = ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = None
    sys.modules[name] = module
    exec(code, module.__dict__, module.__dict__)
    return module


def load_base() -> ModuleType:
    # Execute r41 solely to prove the pinned append-only provenance and its
    # declared r40 template pin, then execute the r40 implementation itself in
    # memory.  We do not call r41's r41-only config validator for fresh r43.
    r41 = exec_pinned(R41_ADAPTER, R41_ADAPTER_SHA256, "_r43_r41_adapter_provenance")
    if getattr(r41, "BASE_ADAPTER_SHA256", None) != R40_ADAPTER_SHA256:
        raise RuntimeError("r41 declared r40 template pin drift")
    return exec_pinned(R40_ADAPTER, R40_ADAPTER_SHA256, "_r43_r40_adapter")


class ConfigProxy:
    """Translate only r43 schema to the audited r40 parser schema in memory."""

    def __init__(self, path: Path):
        self.path = path.resolve()

    def read_bytes(self) -> bytes:
        raw = self.path.read_bytes()
        old = R43_SCHEMA.encode("ascii")
        if raw.count(old) != 1:
            raise ValueError("r43 config schema literal count")
        return raw.replace(old, R40_SCHEMA.encode("ascii"), 1)

    def resolve(self) -> Path:
        return self.path

    def __str__(self) -> str:
        return str(self.path)


def load_config(path: Path):
    base = load_base()
    cfg = base.load_config(ConfigProxy(path))
    if cfg.tag != R43_TAG or cfg.predecessor != R42_TAG:
        raise ValueError("r43 config must bind v16r2r43<-v16r2r42")
    try:
        meta = json.loads(path.read_bytes().decode("utf-8"))
    except Exception as exc:
        raise ValueError("r43 config metadata unreadable") from exc
    scripts = meta.get("review_scripts") if isinstance(meta, dict) else None
    scanner_rel = scripts.get("stale_scan") if isinstance(scripts, dict) else None
    if scanner_rel != R43_SCANNER_REL:
        raise ValueError("r43 stale scanner path pin")
    scanner_pin = meta.get("stale_scanner_sha256") if isinstance(meta, dict) else None
    scanner_path = ROOT / R43_SCANNER_REL
    if not isinstance(scanner_pin, str) or sha(scanner_path.read_bytes()) != scanner_pin:
        raise ValueError("r43 stale scanner source hash drift")
    return base, cfg, path.resolve()


def run_stale_scan(cfg: Any, config_path: Path) -> dict[str, Any]:
    scanner = ROOT / R43_SCANNER_REL
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "CM2_STALE_SCAN_TAG": cfg.tag,
                "CM2_STALE_SCAN_PREV": cfg.predecessor,
                "CM2_R43_CONFIG": str(config_path)})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", str(scanner)],
                          cwd=str(ROOT), env=env, capture_output=True,
                          check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"r43 stale scanner rc={proc.returncode}:"
                           f"{proc.stderr[-600:]!r}")
    try:
        value = json.loads(proc.stdout.decode("utf-8"))
    except Exception as exc:
        raise RuntimeError("r43 stale scanner did not emit one JSON object") from exc
    if (not isinstance(value, dict) or value.get("failed_check_count") != 0 or
            value.get("read_only") is not True or
            value.get("writes_performed") is not False or
            value.get("formal_global_closure_credit") != 0 or
            value.get("D02_unlock") is not False or
            value.get("runtime_authorized") is not False):
        raise RuntimeError("r43 stale scanner zero-credit predicate failed")
    return value


def guard_entrypoint(config_path: Path, argv: list[str]) -> int:
    base, cfg, resolved = load_config(config_path)
    if argv != ["--preflight"]:
        raise ValueError("r43 guard accepts only --preflight")
    run_stale_scan(cfg, resolved)
    return int(base.guard_entrypoint(ConfigProxy(resolved), argv))


def publisher_entrypoint(config_path: Path, publish: bool) -> int:
    base, cfg, resolved = load_config(config_path)
    if not publish:
        raise ValueError("r43 publisher refuses without --publish")
    if os.environ.get(R43_ACK_ENV) != R43_ACK:
        raise ValueError("missing r43 publish acknowledgement token")
    run_stale_scan(cfg, resolved)
    module = base.build_publisher(cfg)
    return int(module.main())


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
        print(f"R43_ADAPTER_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
