#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2 common two-branch rectangle audit."""

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


SCHEMA = "cm2.gate2.two-branch-common-rectangle-obstruction.v1"
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "cm2-gate2-two-branch-common-rectangle-manifest-2026-07-15.json"
LOCAL_CERT = HERE / "cm2_gate2_two_branch_common_rectangle_obstruction_cert.py"
CLOSED_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"
FLINT_PYTHON = Path("/tmp/cm2-flint-venv/bin/python")

PROVED_TRUE = (
    "common_qnl_perron_product_rectangle",
    "qnl_fixed_point_in_common_rectangle",
    "shadow_96_word_fixed_point_in_common_rectangle",
    "short_qnl_full_height_source_strip",
    "short_qnl_physical_first_hit_word",
    "short_qnl_unstable_face_covering",
    "short_qnl_stable_face_entry",
    "short_qnl_uniform_hyperbolic_cones",
    "candidate_source_u_intervals_disjoint",
    "mixed_corner_forced_for_full_height_vertical_loop_strip",
    "qnl_perron_mixed_corner_first_69_collisions",
    "qnl_perron_intended_collision_70_impossible",
    "loop_perron_mixed_corner_first_73_collisions",
    "loop_perron_intended_collision_74_impossible",
    "narrow_cone_full_height_graph_class_ruled_out",
    "audited_affine_fixed_96_word_route_ruled_out",
)

PROVED_FALSE = (
    "arbitrary_affine_coordinate_route_ruled_out",
    "curvilinear_route_ruled_out",
    "uses_floating_point_acceptance",
    "uses_truncation_renormalisation",
)

PHYSICAL = (
    "curvilinear_stable_saturated_loop_source",
    "curvilinear_stable_saturated_loop_target",
    "interval_indexed_common_stable_foliation",
    "leaf_invariance_for_second_branch",
    "two_physical_onto_quotient_branches",
    "full_mass_countable_return_partition",
    "stable_quotient_density_rho",
    "actual_reverse_weight_registry",
    "closed_projective_map_registry",
    "off_diagonal_projective_near_collision_bound",
    "full_countable_pair_energy_drift",
    "actual_native_stopping_antichain",
    "same_carrier_physical_endpoint_identity",
    "exhaustive_amplitude_registry",
    "parentwise_normalized_amplitude_moment",
    "physical_gate2",
)

LOCAL_LINES = (
    "COMMON_GRAY_PERRON_CHART: CERTIFIED",
    "SHORT_QNL_COMMON_RECTANGLE_FULL_CROSS: CERTIFIED",
    "CANDIDATE_SOURCE_STRIPS_DISJOINT: CERTIFIED",
    "MIXED_CORNER_IN_EVERY_AXIS_ALIGNED_COMMON_VERTICAL_STRIP: CERTIFIED",
    "MIXED_CORNER_FIRST_69_COLLISIONS: CERTIFIED",
    "MIXED_CORNER_INTENDED_COLLISION_70: IMPOSSIBLE",
    "LOOP_PERRON_MIXED_CORNER_FIRST_73_COLLISIONS: CERTIFIED",
    "LOOP_PERRON_MIXED_CORNER_INTENDED_COLLISION_74: IMPOSSIBLE",
    "NARROW_CONE_FULL_HEIGHT_PLAQUE_CLASS: RULED_OUT",
    "QNL_PERRON_FIXED_96_WORD_FULL_HEIGHT_BRANCH: RULED_OUT",
    "LOOP_PERRON_FIXED_96_WORD_FULL_HEIGHT_BRANCH: RULED_OUT",
    "AUDITED_AFFINE_TWO_BRANCH_COMMON_RECTANGLE_ROUTE: RULED_OUT",
    "ARBITRARY_AFFINE_COORDINATE_TWO_BRANCH_HORSESHOE: NOT_CERTIFIED",
    "CURVILINEAR_STABLE_SATURATED_TWO_BRANCH_HORSESHOE: NOT_CERTIFIED",
    "FULL_MASS_COUNTABLE_RETURN_PARTITION: NOT_CERTIFIED",
    "PHYSICAL_GATE2: NOT_CERTIFIED",
)

CLOSED_LINES = (
    "REVERSIBLE_SHADOW_INTERVAL_NEWTON: CERTIFIED",
    "CLOSED_COMMON_VERTEX_LOOP_WORD: CERTIFIED",
    "SAME_BASEPOINT_DERIVATIVE_CHAIN: CERTIFIED",
    "CLOSED_COMMON_VERTEX_LOOP_DERIVATIVE: CERTIFIED",
    "FINITE_CLOSED_SAME_ORBIT_SHADOW_LOOP: CERTIFIED",
    "BONATTI_VIANA_QNL_FIBER_HOLONOMY_IDENTIFICATION: NOT CERTIFIED",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(script: Path, required: tuple[str, ...], timeout: int) -> list[str]:
    python = FLINT_PYTHON if FLINT_PYTHON.is_file() else Path(sys.executable)
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(HERE)
    try:
        run = subprocess.run(
            [str(python), str(script)],
            cwd=ROOT,
            env=environment,
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


def semantic_errors(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if data.get("verdict") != "OPEN_NO_GO":
        errors.append("verdict must remain OPEN_NO_GO")
    if not data.get("model_id"):
        errors.append("model_id missing")

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
            "common_half_width": "4.2e-15",
            "minimum_any_centered_common_half_width_lower_bound": "4.14e-15",
            "qnl_perron_collision_70_discriminant_upper_bound": "-0.29",
            "loop_perron_collision_74_discriminant_upper_bound": "-0.21",
            "narrow_cone_graph_lipschitz_bound": "1e-100",
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
    errors.extend(replay(LOCAL_CERT, LOCAL_LINES, 180))
    errors.extend(replay(CLOSED_CERT, CLOSED_LINES, 180))
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
    promoted["physical_inputs"]["curvilinear_stable_saturated_loop_source"] = False
    assert "curvilinear_stable_saturated_loop_source" in missing(promoted)

    overclaim = deepcopy(data)
    overclaim["proved_layers"]["curvilinear_route_ruled_out"] = True
    assert "fail-closed field promoted or missing: curvilinear_route_ruled_out" in semantic_errors(overclaim)
    overclaim = deepcopy(data)
    overclaim["proved_layers"]["narrow_cone_graph_lipschitz_bound"] = "1e-53"
    assert "quantitative field changed: narrow_cone_graph_lipschitz_bound" in semantic_errors(overclaim)


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
        print("TWO_BRANCH_COMMON_RECTANGLE_MANIFEST: INVALID")
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
        "short_qnl_common_rectangle_full_cross": True,
        "audited_affine_fixed_96_word_route_ruled_out": True,
        "narrow_cone_graph_lipschitz_bound": "1e-100",
        "curvilinear_stable_saturated_second_branch": False,
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
