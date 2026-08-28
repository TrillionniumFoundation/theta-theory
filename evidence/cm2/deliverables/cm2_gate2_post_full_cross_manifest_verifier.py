#!/usr/bin/env python3
"""Fail-closed verifier for the post-full-cross Gate-2 snapshot."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


SCHEMA = "cm2.gate2.post-full-cross.v1"
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "cm2-gate2-post-full-cross-manifest-2026-07-15.json"
LOCAL_CERT = HERE / "cm2_gate2_post_full_cross_return_base_cert.py"
GATE1_CERT = HERE / "cm2_gate1_full_cross_transport_cert.py"
FLINT_PYTHON = Path("/tmp/cm2-flint-venv/bin/python")

PROVED = (
    "directed_physical_full_cross",
    "reverse_inherited_transition_strip",
    "actual_transition_endpoint_derivatives",
    "q_anchored_positive_srb_2d_source_rectangle",
    "exact_source_srb_mass",
    "full_mass_2d_first_return_by_poincare",
    "kac_mean_first_return",
    "actual_2d_return_alphabet_schema",
    "two_dimensional_reverse_kernel_is_dirac",
    "dirac_kernel_pair_energy_contraction_impossible",
    "transition_24_disjoint_from_source",
    "candidate_actual_unstable_reference_curve",
)

PHYSICAL = (
    "closed_q_anchored_return_word",
    "executable_first_return_branch",
    "stable_saturated_young_rectangle",
    "stable_holonomy_projection_to_reference_curve",
    "onto_countable_stable_quotient_alphabet",
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
    "DIRECTED_FULL_CROSS_INPUT: CERTIFIED",
    "Q_ANCHORED_2D_SOURCE_RECTANGLE: CERTIFIED",
    "exact_mass_formula=(105*k_A/(13*pi))*10^-38",
    "TRANSITION_24_IS_NOT_A_RETURN_TO_SOURCE: CERTIFIED",
    "TWO_DIMENSIONAL_FIRST_RETURN_FULL_MASS: PROVED_BY_POINCARE",
    "TWO_DIMENSIONAL_REVERSE_KERNEL: DETERMINISTIC_DIRAC",
    "STABLE_SATURATED_YOUNG_RECTANGLE: NOT_CERTIFIED",
    "PHYSICAL_GATE2: NOT_CERTIFIED",
)

GATE1_LINES = (
    "FULL_CROSS_COMMON_VERTEX: CERTIFIED",
    "REVERSIBLE_OPPOSITE_TRANSITION_FULL_CROSS: CERTIFIED",
    "ACTUAL_VERTEX_TRANSITION_DERIVATIVE: CERTIFIED",
    "CLOSED_COMMON_VERTEX_LOOP_DERIVATIVE: NOT CERTIFIED",
    "TRANSPORTED_TWISTING: NOT CERTIFIED",
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
        errors.append(f"{script.name} exited {run.returncode}: {run.stderr.strip()}")
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
        if proved.get("transition_24_is_return_branch") is not False:
            errors.append("24-transition falsely promoted to return branch")
        if proved.get("uses_truncation_renormalisation") is not False:
            errors.append("truncation renormalisation must remain disabled")

    errors.extend(replay(LOCAL_CERT, LOCAL_LINES, 120))
    errors.extend(replay(GATE1_CERT, GATE1_LINES, 120))
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
    promoted["physical_inputs"]["stable_saturated_young_rectangle"] = False
    assert "stable_saturated_young_rectangle" in missing(promoted)


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
        print("POST_FULL_CROSS_MANIFEST: INVALID")
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
        "directed_full_cross": True,
        "q_anchored_2d_return_base": True,
        "stable_quotient": False,
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
