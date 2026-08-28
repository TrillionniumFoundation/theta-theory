#!/usr/bin/env python3
"""Read-only r16 attack-name census entrypoint.

The historical census implementation is reused only as an AST/tokenizer
checker; this entrypoint fixes the candidate path to the r16 consumer and
labels the result as an r16 enumeration.  It never imports, compiles, or
executes the candidate source and never writes a report or runtime surface.
The result is enumeration evidence (137/137), not proof that the cold runtime
executed the attacks.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
CONSUMER = ROOT / (
    "deliverables/cm2_round306c79g_true_global_no_producer_consumer_"
    "independent_verifier_assembler_authority_consumer_v16r2r16_"
    "semantic_source.py")
LEGACY = Path(__file__).with_name("c79g_v16r2r11_attack_census.py")


def main() -> int:
    spec = importlib.util.spec_from_file_location("_r16_census_impl", LEGACY)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load read-only census implementation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # The implementation emits one canonical JSON report.  Capture its
    # structured result by using its normal entrypoint in a subprocess-like
    # argument path would be needlessly lossy, so call the pure CLI function
    # with an absolute path and preserve its stdout contract.
    return int(module.main(["--consumer", str(CONSUMER)]))


if __name__ == "__main__":
    raise SystemExit(main())
