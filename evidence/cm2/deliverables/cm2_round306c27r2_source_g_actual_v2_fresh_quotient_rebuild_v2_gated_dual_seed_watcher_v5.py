#!/usr/bin/env python3
"""Append-only v5 launcher for the frozen C27R2 v4 transaction core.

The v4 watcher constructed the coherent-attack output contract in semantic,
rather than canonical lexical, order.  The frozen v4 transaction runner
correctly rejects every non-canonical ``list == sorted(set(list))`` contract,
so the attack child was never started.  This shim preserves every frozen v4
mathematical and process contract and normalizes *all* list-valued output
inventories before the command specification is closed.

``SELF`` is rebound to this append-only source.  Consequently the normal v4
watcher self-pin remains effective and callers must explicitly pin these v5
bytes.  No old source or failed transaction is modified or resumed.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from typing import Any


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
BASE = ROOT / (
    "deliverables/"
    "cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_"
    "gated_dual_seed_watcher_v4.py"
)


def load_base() -> Any:
    spec = importlib.util.spec_from_file_location(
        "cm2_c27r2_gated_dual_seed_watcher_v4_frozen", BASE
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load frozen v4 watcher")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_base()
    module.SELF = SELF
    original = module.command_spec

    def canonical_command_spec(
        stage: str,
        source: Path,
        source_sha: str,
        argv: list[str],
        input_paths: list[str],
        output_roots: list[dict[str, Any]],
        stdout_status: str,
        hash_seed: str,
        timeout: int,
        pinset_path: Path,
        pinset_value: dict[str, Any],
        args: Any,
    ) -> dict[str, Any]:
        normalized: list[dict[str, Any]] = []
        for item in output_roots:
            clone = dict(item)
            for key in ("exact_inventory", "required_relative_files"):
                value = clone.get(key)
                if type(value) is list:
                    if not all(type(member) is str for member in value):
                        raise module.Failure(
                            "non-string output inventory member:" + key
                        )
                    clone[key] = sorted(set(value))
            normalized.append(clone)
        return original(
            stage, source, source_sha, argv, sorted(set(input_paths)),
            normalized, stdout_status, hash_seed, timeout, pinset_path,
            pinset_value, args,
        )

    module.command_spec = canonical_command_spec
    return module.main()


if __name__ == "__main__":
    raise SystemExit(main())
