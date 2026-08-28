#!/usr/bin/env python3
"""r41-specific append-only cold-freeze adapter.

This is a thin, pinned successor of the audited r40 adapter.  It does not
copy or rewrite r40/r39 candidate bytes and it does not create deliverables.
The r41 config is translated only in memory to the r40 adapter's parser, so
the strict exact8/direct-path/evidence/C53 checks and the corrected O_RDWR
same-FD publication helper are inherited without changing the r40 tooling.

No operation is implicit: the guard requires ``--config PATH --preflight``;
publication additionally requires ``--publish`` and
``CM2_R41_PUBLISH_ACK=EXACT8_MANIFEST_OUTER_LAST_R41``.  A failed or missing
config is a refusal and cannot touch a target namespace.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any

os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
BASE_ADAPTER = ROOT / "scripts/c79g_v16r2r40_cold_freeze_adapter.py"
BASE_ADAPTER_SHA256 = "4ad1f559fc37ca835dce2897eced5802e119a3acdbf461f92cd05a51343ba449"
R41_ACK_ENV = "CM2_R41_PUBLISH_ACK"
R41_ACK = "EXACT8_MANIFEST_OUTER_LAST_R41"
R41_SCHEMA = "cm2.c79g.r41.cold-freeze-config.v1"
R40_SCHEMA = "cm2.c79g.r40.cold-freeze-config.v1"


def _sha(raw: bytes) -> str:
    import hashlib
    return hashlib.sha256(raw).hexdigest()


def _load_base():
    raw = BASE_ADAPTER.read_bytes()
    if _sha(raw) != BASE_ADAPTER_SHA256:
        raise RuntimeError("r40 adapter template hash drift")
    spec = importlib.util.spec_from_file_location("_r41_r40_adapter", BASE_ADAPTER)
    if spec is None or spec.loader is None:
        raise RuntimeError("r40 adapter spec unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class _ConfigProxy:
    """Path-like read-only view replacing only the config schema in memory."""
    def __init__(self, path: Path):
        self.path = path.resolve()

    def read_bytes(self) -> bytes:
        raw = self.path.read_bytes()
        old = R41_SCHEMA.encode("ascii")
        new = R40_SCHEMA.encode("ascii")
        if raw.count(old) != 1:
            raise ValueError("r41 config schema literal count")
        return raw.replace(old, new, 1)

    def resolve(self) -> Path:
        return self.path

    def __str__(self) -> str:
        return str(self.path)


def load_config(path: Path):
    base = _load_base()
    proxy = _ConfigProxy(path)
    cfg = base.load_config(proxy)
    if cfg.tag != "v16r2r41" or cfg.predecessor != "v16r2r40":
        raise ValueError("r41 config must bind v16r2r41←v16r2r40")
    return base, cfg, proxy


def guard_entrypoint(config_path: Path, argv: list[str]) -> int:
    base, _cfg, proxy = load_config(config_path)
    if argv != ["--preflight"]:
        raise ValueError("r41 guard accepts only --preflight")
    return int(base.guard_entrypoint(proxy, argv))


def publisher_entrypoint(config_path: Path, publish: bool) -> int:
    base, cfg, _proxy = load_config(config_path)
    if not publish:
        raise ValueError("r41 publisher refuses without --publish")
    if os.environ.get(R41_ACK_ENV) != R41_ACK:
        raise ValueError("missing r41 publish acknowledgement token")
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
        print(f"R41_ADAPTER_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
