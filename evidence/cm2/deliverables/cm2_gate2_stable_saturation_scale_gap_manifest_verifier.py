#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2 saturation scale/mass gap."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


SCHEMA = "cm2.gate2.stable-saturation-scale-gap.v1"
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "cm2-gate2-stable-saturation-scale-gap-manifest-2026-07-15.json"
CERT = HERE / "cm2_gate2_stable_saturation_scale_gap_cert.py"
FLINT_PYTHON = Path("/tmp/cm2-flint-venv/bin/python")

PROVED_TRUE = (
    "predecessor_actual_single_stable_leaf_endpoints",
    "predecessor_two_local_physical_branches",
    "current_tube_full_height_route_ruled_out",
    "current_two_raw_strips_full_mass_partition_ruled_out",
)
PROVED_FALSE = (
    "curvilinear_stable_saturation_impossible",
    "uses_floating_point_acceptance",
)
EXACT = {
    "stable_endpoint_separation_lower": "8.29e-15",
    "certified_second_source_v_halfheight": "1e-80",
    "endpoint_reach_factor_lower": "8.29e65",
    "common_halfheight_factor_exact": "4.2e65",
    "current_height_fraction_upper": "2.39e-66",
    "crossing_uncertainty_over_source_u_upper": "1.07e-104",
    "qnl_source_physical_fraction_exact": "27/280",
    "loop_source_physical_fraction_upper": "4.54e-119",
    "current_two_raw_strips_physical_fraction_upper": "0.097",
    "unregistered_common_rectangle_fraction_lower": "0.903",
}
PHYSICAL = (
    "uniform_tube_along_full_stable_endpoint_segment",
    "interval_indexed_invariant_stable_plaque_family",
    "common_physical_stable_holonomy",
    "stable_holonomy_conditional_srb_jacobian",
    "two_onto_quotient_inverse_branches",
    "full_mass_countable_return_partition",
    "unregistered_complement_return_registry",
    "stable_quotient_density_rho",
    "actual_reverse_weight_registry",
    "off_diagonal_projective_near_collision_bound",
    "full_countable_pair_energy_drift",
    "actual_native_stopping_antichain",
    "same_carrier_physical_endpoint_identity",
    "exhaustive_amplitude_registry",
    "parentwise_normalized_amplitude_moment",
    "physical_gate2",
)
CERT_LINES = (
    "PREDECESSOR_TWO_LOCAL_PHYSICAL_BRANCHES: VERIFIED",
    "ACTUAL_SINGLE_STABLE_LEAF_ENDPOINTS: VERIFIED",
    "CURRENT_96_WORD_TUBE_SCALE_GAP: CERTIFIED",
    "CURRENT_TWO_RAW_STRIPS_FULL_MASS_ROUTE: RULED_OUT",
    "CURVILINEAR_STABLE_SATURATION_ROUTE: OPEN",
    "INTERVAL_INDEXED_INVARIANT_PLAQUE_FAMILY: NOT_CERTIFIED",
    "FULL_MASS_COUNTABLE_RETURN_PARTITION: NOT_CERTIFIED",
    "ACTUAL_SRB_GIBBS_WEIGHTS_AND_STOPPED_PPE: NOT_CERTIFIED",
    "PHYSICAL_GATE2: NOT_CERTIFIED",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(timeout: int = 180) -> list[str]:
    python = FLINT_PYTHON if FLINT_PYTHON.is_file() else Path(sys.executable)
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(HERE)
    try:
        run = subprocess.run(
            [str(python), str(CERT)],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [f"certificate replay failed: {exc}"]
    errors: list[str] = []
    if run.returncode != 0:
        errors.append(
            f"certificate exited {run.returncode}: "
            f"{(run.stderr or run.stdout).strip()}"
        )
    for line in CERT_LINES:
        if line not in run.stdout:
            errors.append(f"certificate missing output: {line}")
    return errors


def semantic_errors(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    errors: list[str] = []
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if data.get("model_id") != "cm2-gate2-current-two-strip-scale-and-mass-gap":
        errors.append("model_id mismatch")
    if data.get("verdict") != "OPEN_NO_GO":
        errors.append("verdict must remain OPEN_NO_GO")
    proved = data.get("proved_layers")
    if not isinstance(proved, dict):
        errors.append("proved_layers missing")
    else:
        for field in PROVED_TRUE:
            if proved.get(field) is not True:
                errors.append(f"proved layer missing: {field}")
        for field in PROVED_FALSE:
            if proved.get(field) is not False:
                errors.append(f"fail-closed field promoted or missing: {field}")
        for field, expected in EXACT.items():
            if proved.get(field) != expected:
                errors.append(f"quantitative field changed: {field}")
    return errors


def integrity(data: Any) -> list[str]:
    errors = semantic_errors(data)
    if not isinstance(data, dict):
        return errors
    rows = data.get("provenance")
    if not isinstance(rows, list) or not rows:
        errors.append("provenance missing")
    else:
        for row in rows:
            relative = row.get("path") if isinstance(row, dict) else None
            expected = row.get("sha256") if isinstance(row, dict) else None
            path = ROOT / relative if isinstance(relative, str) else None
            if path is None or not path.is_file():
                errors.append(f"missing provenance file: {relative}")
            elif digest(path) != expected:
                errors.append(f"provenance hash mismatch: {relative}")
    errors.extend(replay())
    return errors


def missing(data: Any) -> list[str]:
    physical = data.get("physical_inputs") if isinstance(data, dict) else None
    if not isinstance(physical, dict):
        return list(PHYSICAL)
    return [field for field in PHYSICAL if physical.get(field) is not True]


def self_test(data: dict) -> None:
    promoted = deepcopy(data)
    promoted["physical_inputs"] = {field: True for field in PHYSICAL}
    assert not missing(promoted)

    one_leaf = deepcopy(data)
    one_leaf["physical_inputs"][
        "uniform_tube_along_full_stable_endpoint_segment"
    ] = True
    assert "interval_indexed_invariant_stable_plaque_family" in missing(one_leaf)

    partition_only = deepcopy(data)
    partition_only["physical_inputs"]["full_mass_countable_return_partition"] = True
    assert "stable_quotient_density_rho" in missing(partition_only)

    overclaim = deepcopy(data)
    overclaim["proved_layers"]["curvilinear_stable_saturation_impossible"] = True
    assert (
        "fail-closed field promoted or missing: curvilinear_stable_saturation_impossible"
        in semantic_errors(overclaim)
    )

    weakened = deepcopy(data)
    weakened["proved_layers"]["unregistered_common_rectangle_fraction_lower"] = "0.90"
    assert (
        "quantitative field changed: unregistered_common_rectangle_fraction_lower"
        in semantic_errors(weakened)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1

    errors = integrity(data)
    if errors:
        print("GATE2_STABLE_SATURATION_SCALE_GAP_MANIFEST: INVALID")
        for error in errors:
            print(f"- {error}")
        return 1

    absent = missing(data)
    if args.self_test:
        self_test(data)
        if set(absent) != set(PHYSICAL):
            print("MANIFEST_VERIFIER_SELF_TEST: FAIL")
            return 1
        print("MANIFEST_VERIFIER_SELF_TEST: PASS")
        print("FAIL_CLOSED_PHYSICAL_SNAPSHOT: PASS")
        return 0

    print(json.dumps({
        "model_id": data.get("model_id"),
        "actual_single_stable_leaf_endpoints": True,
        "two_local_physical_branches": True,
        "endpoint_reach_factor_lower": "8.29e65",
        "current_two_raw_strips_physical_fraction_upper": "0.097",
        "unregistered_common_rectangle_fraction_lower": "0.903",
        "curvilinear_stable_saturation_impossible": False,
        "missing_physical_field_count": len(absent),
        "physical_gate2_certified": not absent,
    }, indent=2, sort_keys=True))
    if absent:
        print("PHYSICAL_GATE2: NOT_CERTIFIED")
        for field in absent:
            print(f"- missing: {field}")
        return 2
    print("PHYSICAL_GATE2: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
