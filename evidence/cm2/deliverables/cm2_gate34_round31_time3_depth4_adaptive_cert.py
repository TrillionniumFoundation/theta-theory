#!/usr/bin/env python3
"""Round-31 depth-four adaptive time-three certificate on every Q2 anchor."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round30_time3_depth2_adaptive_cert as r30


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round31-time3-depth4-adaptive.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate34-round31-time3-depth4-adaptive-manifest-2026-07-19.json"
DEPENDENCIES = {
    "cm2_gate34_round30_time3_depth2_adaptive_cert.py":
        "1c5cd857576ee57ca0c3c3a66b397e4871a53e7e85e068bc850360b53b82e139",
    "cm2-gate34-round30-time3-depth2-adaptive-manifest-2026-07-19.json":
        "3ca7a9314cd2f8a65f8ba39e2c0fed3bd2d48d809b64c59f02ed8d0406378a75",
}
FROZEN_LEDGER = {
    "Q2_anchor_count": 114006,
    "root_Q3_inner_count": 4088,
    "root_unresolved_count": 109918,
    "terminal_Q3_inner_count": 244704,
    "terminal_R3_inner_count": 0,
    "terminal_unresolved_count": 1285588,
    "terminal_depth_histogram": {"0": 4088, "1": 15898, "2": 18986, "3": 64240, "4": 1427080},
    "terminal_blocker_histogram": {
        "unresolved_competitor:unresolved_discriminant": 1244086,
        "unresolved_time2_outgoing_chart_or_geometry": 41502,
    },
    "Q3_coordinate_base_mass": "5728337/40960000000",
    "R3_coordinate_base_mass": "0",
    "unresolved_coordinate_base_mass": "7266811/8192000000",
    "total_Q2_coordinate_base_mass": "5257799/5120000000",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise RuntimeError(f"unsafe dependency: {name}")
        if sha(path) != expected:
            raise RuntimeError(f"dependency hash: {name}")


def build_result() -> dict[str, Any]:
    verify_dependencies()
    ledger = dict(FROZEN_LEDGER)
    ledger["Q3_gain_over_round30_depth2"] = 205732
    ledger["terminal_leaf_count"] = 1530292
    ledger["depth4_over_depth2_unresolved_mass_ratio"] = "36334055/40380532"
    ledger["depth4_unresolved_mass_strictly_below_depth2"] = True
    if Q(ledger["Q3_coordinate_base_mass"]) + Q(ledger["R3_coordinate_base_mass"]) + Q(ledger["unresolved_coordinate_base_mass"]) != Q(ledger["total_Q2_coordinate_base_mass"]):
        raise RuntimeError("mass conservation")
    result = {
        "schema": RESULT_SCHEMA,
        "adaptive_protocol": {
            "root_family": "all 114006 certified Q2 anchors",
            "split_rule": "longest normalized (t,p,s) side, binary midpoint",
            "maximum_additional_depth": 4,
            "arithmetic": "384-bit Arb plus exact rational mass",
            "coverage": "complete",
        },
        "time3_depth4_ledger": ledger,
        "strict_nonpromotion": {
            "observed_mass_ratio_promoted_to_uniform_contraction": False,
            "finite_R3_zero_promoted_to_physical_R3_emptiness": False,
            "complete_limiting_R3_Q3_component_enumeration": "NOT_CERTIFIED",
            "uniform_adaptive_time3_termination_rate": "NOT_CERTIFIED",
            "survivor_conditioned_recovery": "NOT_CERTIFIED",
            "strong_q_weighted_tail": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = hashlib.sha256(
        json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return result


def replay(workers: int) -> dict[str, Any]:
    old_depth, old_ledger = r30.MAX_EXTRA_DEPTH, r30.FROZEN_LEDGER
    try:
        r30.MAX_EXTRA_DEPTH = 4
        r30.FROZEN_LEDGER = FROZEN_LEDGER
        r30.replay(workers)
    finally:
        r30.MAX_EXTRA_DEPTH, r30.FROZEN_LEDGER = old_depth, old_ledger
    return build_result()


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate34_round31_time3_depth4_adaptive_verifier.py")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = replay(args.workers) if args.replay else build_result()
    print(f"Q3_COMPONENTS: {result['time3_depth4_ledger']['terminal_Q3_inner_count']}")
    print("GATE3: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.replay else 2


if __name__ == "__main__":
    raise SystemExit(main())
