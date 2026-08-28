#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2 actual stable-plaque continuation."""

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


SCHEMA = "cm2.gate2.actual-stable-plaque-continuation.v1"
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json"
CERT = HERE / "cm2_gate2_actual_stable_plaque_continuation_cert.py"
FLINT_PYTHON = Path("/tmp/cm2-flint-venv/bin/python")

PROVED_TRUE = (
    "two_return_actual_unstable_plaque_continuation",
    "actual_stable_plaque_v0_crossing",
    "actual_crossing_96_first_hits",
    "positive_width_actual_plaque_96_word_strip",
    "second_strip_unstable_face_covering",
    "second_strip_stable_entry",
    "second_strip_uniform_cones",
    "qnl_and_actual_plaque_source_strips_disjoint",
    "two_local_physical_branches_in_common_rectangle",
)

PROVED_FALSE = (
    "second_branch_stable_saturated",
    "two_branch_physical_quotient",
    "uses_floating_point_acceptance",
)

PHYSICAL = (
    "second_branch_stable_saturation",
    "common_invariant_stable_holonomy",
    "two_onto_quotient_inverse_branches",
    "full_mass_countable_return_partition",
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
    "REFINED_2400_BIT_REVERSIBLE_ROOT: CERTIFIED",
    "TWO_RETURN_ACTUAL_UNSTABLE_PLAQUE_CONTINUATION: CERTIFIED",
    "ACTUAL_STABLE_PLAQUE_V0_CROSSING: CERTIFIED",
    "ACTUAL_CROSSING_96_FIRST_HITS: CERTIFIED",
    "POSITIVE_WIDTH_ACTUAL_PLAQUE_96_WORD_STRIP: CERTIFIED",
    "ACTUAL_PLAQUE_SECOND_BRANCH_CONES: CERTIFIED",
    "TWO_LOCAL_PHYSICAL_BRANCHES_IN_COMMON_RECTANGLE: CERTIFIED",
    "SECOND_BRANCH_STABLE_SATURATION: NOT_CERTIFIED",
    "FULL_MASS_COUNTABLE_RETURN_PARTITION: NOT_CERTIFIED",
    "PHYSICAL_GATE2: NOT_CERTIFIED",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(timeout: int = 300) -> list[str]:
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
    if data.get("verdict") != "OPEN_NO_GO":
        errors.append("verdict must remain OPEN_NO_GO")
    if data.get("model_id") != "cm2-actual-plaque-96-word-second-local-branch":
        errors.append("model_id mismatch")

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
        exact = {
            "refined_reversible_root_radius": "1e-600",
            "crossing_uncertainty_upper_bound": "8.53e-172",
            "second_source_u_radius": "8e-68",
            "second_source_v_radius": "1e-80",
            "second_strip_cone_slope": "1e-20",
        }
        for field, expected in exact.items():
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

    tampered = deepcopy(data)
    tampered["physical_inputs"]["second_branch_stable_saturation"] = True
    assert "common_invariant_stable_holonomy" in missing(tampered)

    overclaim = deepcopy(data)
    overclaim["proved_layers"]["second_branch_stable_saturated"] = True
    assert (
        "fail-closed field promoted or missing: second_branch_stable_saturated"
        in semantic_errors(overclaim)
    )

    changed = deepcopy(data)
    changed["proved_layers"]["crossing_uncertainty_upper_bound"] = "1e-160"
    assert (
        "quantitative field changed: crossing_uncertainty_upper_bound"
        in semantic_errors(changed)
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
        print("ACTUAL_STABLE_PLAQUE_MANIFEST: INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    if args.self_test:
        self_test(data)
        if set(missing(data)) != set(PHYSICAL):
            print("MANIFEST_VERIFIER_SELF_TEST: FAIL")
            return 1
        print("MANIFEST_VERIFIER_SELF_TEST: PASS")
        print("FAIL_CLOSED_PHYSICAL_SNAPSHOT: PASS")
        return 0

    absent = missing(data)
    print(json.dumps({
        "model_id": data.get("model_id"),
        "actual_stable_plaque_v0_crossing": True,
        "actual_crossing_96_first_hits": True,
        "two_local_physical_branches_in_common_rectangle": True,
        "second_branch_stable_saturated": False,
        "two_branch_physical_quotient": False,
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
