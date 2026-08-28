#!/usr/bin/env python3
"""Canonical-provenance binding of the pinned C30c receipt validator."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "deliverables/cm2_round306c30c_62_attack_run_receipt_validator.py"
BASE_SHA256 = "8692c8a8e57d535ba8f8162bd4f7f51e8acb04f28755384158b45b4eb2629b61"
RUN_NAME = "c30c-v5-toctou-robustness-rerun-20260808T1325-canonical-v2"
PROVENANCE_SHA256 = "485e24388f71bd07988b53e8dc165d3e1b061d5d91c1819fe378ea18dfdab2be"
RUNNER_SHA256 = "407be71a35d62a1e532b185cc8084633e5ffad034572848420409f2f8697dc4c"


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def load_base():
    if file_sha256(BASE) != BASE_SHA256:
        raise RuntimeError("pinned base receipt validator bytes")
    specification = importlib.util.spec_from_file_location(
        "cm2_c30c_pinned_receipt_validator_v1", BASE)
    if specification is None or specification.loader is None:
        raise RuntimeError("base validator import specification")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    module.EXPECTED_RUN_NAME = RUN_NAME
    module.EXPECTED_PROVENANCE_SHA256 = PROVENANCE_SHA256
    module.EXPECTED_RUNNER_SHA256 = RUNNER_SHA256
    return module


def main() -> int:
    module = load_base()
    try:
        return module.main()
    except (module.Reject, OSError, KeyError, TypeError, ValueError) as error:
        print("REJECT_C30C_ATTACK_RUN_RECEIPT:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
