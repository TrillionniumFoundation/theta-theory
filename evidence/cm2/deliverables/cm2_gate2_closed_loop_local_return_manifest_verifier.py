#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2 closed-loop local-return snapshot."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


SCHEMA = "cm2.gate2.closed-loop-local-return.v1"
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "cm2-gate2-closed-loop-local-return-manifest-2026-07-15.json"
LOCAL_CERT = HERE / "cm2_gate2_closed_loop_local_return_cert.py"
GATE1_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"
FLINT_PYTHON = Path("/tmp/cm2-flint-venv/bin/python")

PROVED = (
    "exact_closed_96_collision_word",
    "same_orbit_loop_derivative",
    "exact_perron_chart",
    "positive_width_prescribed_word_return_strip",
    "strict_unstable_face_covering",
    "strict_stable_face_entry",
    "regular_first_hit_word_on_full_strip",
    "positive_collision_srb_mass",
    "uniform_unstable_cone",
    "uniform_stable_inverse_cone",
    "fixed_point_local_stable_plaque",
    "fixed_point_local_unstable_plaque",
)

PHYSICAL = (
    "earlier_return_exclusion_for_new_rectangle",
    "stable_saturated_source_product",
    "stable_saturated_target_product",
    "interval_indexed_local_stable_foliation",
    "leaf_invariance_under_96_word",
    "stable_holonomy_projection",
    "single_nontrivial_onto_stable_quotient_branch",
    "stable_holonomy_bv_or_absolute_continuity",
    "stable_holonomy_jacobian",
    "full_mass_countable_return_partition",
    "stable_quotient_density_rho",
    "actual_reverse_weight_registry",
    "closed_branch_projective_map_registry",
    "exponential_return_grazing_context_tail",
    "off_diagonal_projective_near_collision_bound",
    "full_countable_pair_energy_drift",
    "actual_native_stopping_antichain",
    "same_carrier_physical_endpoint_identity",
    "exhaustive_amplitude_registry",
    "parentwise_normalized_amplitude_moment",
    "physical_gate2",
)

LOCAL_LINES = (
    "CLOSED_96_WORD_INPUT: VERIFIED",
    "LOCAL_RETURN_PERRON_CHART: CERTIFIED",
    "POSITIVE_WIDTH_96_COLLISION_RETURN_STRIP: CERTIFIED",
    "LOCAL_HYPERBOLIC_CONES: CERTIFIED",
    "FIXED_POINT_LOCAL_STABLE_UNSTABLE_PLAQUES: CERTIFIED_BY_GRAPH_TRANSFORM",
    "INTERVAL_INDEXED_LOCAL_STABLE_FOLIATION: NOT_CERTIFIED",
    "FIRST_ONTO_STABLE_QUOTIENT_INVERSE_BRANCH: NOT_CERTIFIED",
    "FULL_MASS_COUNTABLE_RETURN_PARTITION: NOT_CERTIFIED",
    "PHYSICAL_GATE2: NOT_CERTIFIED",
)

GATE1_LINES = (
    "CLOSED_COMMON_VERTEX_LOOP_WORD: CERTIFIED",
    "SAME_BASEPOINT_DERIVATIVE_CHAIN: CERTIFIED",
    "CLOSED_COMMON_VERTEX_LOOP_DERIVATIVE: CERTIFIED",
    "TRANSPORTED_PINCHING: CERTIFIED",
    "TRANSPORTED_TWISTING: CERTIFIED",
    "FINITE_CLOSED_SAME_ORBIT_SHADOW_LOOP: CERTIFIED",
    "BONATTI_VIANA_QNL_FIBER_HOLONOMY_IDENTIFICATION: NOT CERTIFIED",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(script: Path, required: tuple[str, ...], timeout: int) -> list[str]:
    python = FLINT_PYTHON if FLINT_PYTHON.is_file() else Path(sys.executable)
    try:
        run = subprocess.run(
            [str(python), str(script)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [f"replay failed {script.name}: {exc}"]
    errors: list[str] = []
    if run.returncode != 0:
        errors.append(
            f"{script.name} exited {run.returncode}: "
            f"{(run.stderr or run.stdout).strip()}"
        )
    for line in required:
        if line not in run.stdout:
            errors.append(f"{script.name} missing output: {line}")
    return errors


def integrity(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if not data.get("model_id"):
        errors.append("model_id missing")
    if data.get("verdict") != "OPEN_NO_GO":
        errors.append("verdict must remain OPEN_NO_GO")

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

    proved = data.get("proved_layers")
    if not isinstance(proved, dict):
        errors.append("proved_layers missing")
    else:
        for field in PROVED:
            if proved.get(field) is not True:
                errors.append(f"proved layer missing: {field}")
        exact_values = {
            "source_strip_half_width_u": "1.86e-96",
            "source_strip_half_width_v": "1e-43",
            "target_rectangle_half_width_u": "1e-43",
            "target_rectangle_half_width_v": "1e-43",
            "collision_srb_mass_lower_bound": "1e-139",
        }
        for field, expected in exact_values.items():
            if proved.get(field) != expected:
                errors.append(f"quantitative field changed: {field}")
        if proved.get("certified_as_first_return") is not False:
            errors.append("96-word falsely promoted to first return")
        if proved.get("affine_perron_fibres_promoted_to_stable_holonomy") is not False:
            errors.append("affine fibres falsely promoted to stable holonomy")
        if proved.get("uses_truncation_renormalisation") is not False:
            errors.append("truncation renormalisation must remain disabled")

    errors.extend(replay(LOCAL_CERT, LOCAL_LINES, 180))
    errors.extend(replay(GATE1_CERT, GATE1_LINES, 180))
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
    promoted["physical_inputs"]["interval_indexed_local_stable_foliation"] = False
    assert "interval_indexed_local_stable_foliation" in missing(promoted)
    promoted["physical_inputs"]["interval_indexed_local_stable_foliation"] = True
    promoted["physical_inputs"]["full_mass_countable_return_partition"] = False
    assert "full_mass_countable_return_partition" in missing(promoted)


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
        print("CLOSED_LOOP_LOCAL_RETURN_MANIFEST: INVALID")
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
        "positive_width_96_collision_return_strip": True,
        "fixed_point_local_plaques": True,
        "interval_indexed_local_stable_foliation": False,
        "single_nontrivial_onto_stable_quotient_branch": False,
        "full_mass_countable_return_partition": False,
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
