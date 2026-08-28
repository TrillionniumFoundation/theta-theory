#!/usr/bin/env python3
"""r42-specific append-only cold-freeze adapter.

This is a pinned successor of the reviewed r41 adapter.  It translates only
the config schema in memory and delegates the strict exact8/direct-path,
evidence, C53, and corrected O_RDWR same-FD checks to the already reviewed
r41 -> r40 adapter chain.  It never repairs, overwrites, or reuses a prior
candidate and it has no implicit publication path.

The guard accepts ``--config PATH --preflight``.  Publication additionally
requires ``--publish`` and the explicit acknowledgement
``CM2_R42_PUBLISH_ACK=EXACT8_MANIFEST_OUTER_LAST_R42``.  This file itself
does not publish anything when merely imported or run without those gates.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
BASE_ADAPTER = ROOT / "scripts/c79g_v16r2r41_cold_freeze_adapter.py"
BASE_ADAPTER_SHA256 = "a6e54aeb0314ac4d08979e25727c756cce47907b744b9b4366ab82e52c735f06"
R42_ACK_ENV = "CM2_R42_PUBLISH_ACK"
R42_ACK = "EXACT8_MANIFEST_OUTER_LAST_R42"
R42_SCHEMA = "cm2.c79g.r42.cold-freeze-config.v1"
R40_SCHEMA = "cm2.c79g.r40.cold-freeze-config.v1"
R42_STALE_SCANNER = "scripts/c79g_v16r2r42_stale_residue_scanner.py"


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _load_base():
    raw = BASE_ADAPTER.read_bytes()
    if _sha(raw) != BASE_ADAPTER_SHA256:
        raise RuntimeError("r41 adapter template hash drift")
    spec = importlib.util.spec_from_file_location("_r42_r41_adapter", BASE_ADAPTER)
    if spec is None or spec.loader is None:
        raise RuntimeError("r41 adapter spec unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    # Pinning/loading r41 is part of the append-only provenance.  Its public
    # config loader enforces r41 tags, which cannot parse a fresh r42 config;
    # descend one audited layer to its pinned r40 implementation and bind the
    # fresh r42 pins there in memory.
    loader = getattr(module, "_load_base", None)
    if not callable(loader):
        raise RuntimeError("r41 adapter base-loader unavailable")
    return loader()


class _ConfigProxy:
    """Path-like read-only view translating only the config schema in memory."""

    def __init__(self, path: Path):
        self.path = path.resolve()

    def read_bytes(self) -> bytes:
        raw = self.path.read_bytes()
        old = R42_SCHEMA.encode("ascii")
        new = R40_SCHEMA.encode("ascii")
        if raw.count(old) != 1:
            raise ValueError("r42 config schema literal count")
        return raw.replace(old, new, 1)

    def resolve(self) -> Path:
        return self.path

    def __str__(self) -> str:
        return str(self.path)


def load_config(path: Path):
    base = _load_base()
    proxy = _ConfigProxy(path)
    cfg = base.load_config(proxy)
    if cfg.tag != "v16r2r42" or cfg.predecessor != "v16r2r41":
        raise ValueError("r42 config must bind v16r2r42<-v16r2r41")
    # The stale-residue scan is an explicit additional hard gate for r42.  It
    # is kept outside the inherited seven-check guard report so the older
    # guard's fixed check-count contract remains intact; this adapter runs it
    # before delegating to that guard and publisher.
    try:
        meta = json.loads(path.read_bytes().decode("utf-8"))
    except Exception as exc:
        raise ValueError("r42 config metadata unreadable") from exc
    scripts = meta.get("review_scripts") if isinstance(meta, dict) else None
    scanner_rel = scripts.get("stale_scan") if isinstance(scripts, dict) else None
    if scanner_rel != R42_STALE_SCANNER:
        raise ValueError("r42 stale scanner path pin")
    scanner_pin = meta.get("stale_scanner_sha256") if isinstance(meta, dict) else None
    scanner_path = ROOT / R42_STALE_SCANNER
    if not isinstance(scanner_pin, str) or _sha(scanner_path.read_bytes()) != scanner_pin:
        raise ValueError("r42 stale scanner source hash drift")
    return base, cfg, proxy


def _run_stale_scan(cfg: Any, config_path: Path) -> dict[str, Any]:
    """Run the independent scanner read-only and require a closed PASS JSON."""
    scanner = ROOT / R42_STALE_SCANNER
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "CM2_STALE_SCAN_TAG": cfg.tag,
                "CM2_STALE_SCAN_PREV": cfg.predecessor,
                "CM2_R42_CONFIG": str(config_path)})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", str(scanner)],
                          cwd=str(ROOT), env=env, capture_output=True,
                          check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"r42 stale scanner rc={proc.returncode}:"
                           f"{proc.stderr[-600:]!r}")
    try:
        value = json.loads(proc.stdout.decode("utf-8"))
    except Exception as exc:
        raise RuntimeError("r42 stale scanner did not emit one JSON object") from exc
    if (not isinstance(value, dict) or value.get("failed_check_count") != 0 or
            value.get("read_only") is not True or
            value.get("writes_performed") is not False or
            value.get("formal_global_closure_credit") != 0 or
            value.get("D02_unlock") is not False or
            value.get("runtime_authorized") is not False):
        raise RuntimeError("r42 stale scanner zero-credit predicate failed")
    return value


def guard_entrypoint(config_path: Path, argv: list[str]) -> int:
    base, cfg, proxy = load_config(config_path)
    if argv != ["--preflight"]:
        raise ValueError("r42 guard accepts only --preflight")
    _run_stale_scan(cfg, config_path)
    return int(base.guard_entrypoint(proxy, argv))


def publisher_entrypoint(config_path: Path, publish: bool) -> int:
    base, cfg, _proxy = load_config(config_path)
    if not publish:
        raise ValueError("r42 publisher refuses without --publish")
    if os.environ.get(R42_ACK_ENV) != R42_ACK:
        raise ValueError("missing r42 publish acknowledgement token")
    _run_stale_scan(cfg, config_path)
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
        print(f"R42_ADAPTER_REFUSED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(2)
