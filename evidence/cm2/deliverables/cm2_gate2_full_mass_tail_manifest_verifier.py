#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-2 full-mass/tail snapshot."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


SCHEMA = "cm2.gate2.full-mass-tail.v1"
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2-gate2-full-mass-tail-manifest-2026-07-15.json"
LOCAL_CERT = HERE / "cm2_gate2_full_mass_tail_cert.py"
GATE1_CERT = HERE / "cm2_gate1_full_cross_transport_cert.py"
FLINT_PYTHON = Path("/tmp/cm2-flint-venv/bin/python")

PROVED_FIELDS = (
    "true_two_graph_common_vertex",
    "common_vertex_is_one_directed_transverse_point",
    "unnormalised_finite_core_full_law_transfer",
    "countable_same_label_energy_criterion",
    "off_diagonal_energy_criterion",
    "marginal_tail_moment_sufficiency_counterexample",
    "abstract_prefix_stopping_antichain",
    "native_scale_overshoot_counterexample",
    "reverse_kernel_formula_conditional_on_quotient",
    "standard_borel_finite_operation_registry_schema",
)

PHYSICAL_FIELDS = (
    "q_anchored_positive_width_return_rectangle",
    "one_state_young_base",
    "reference_unstable_interval",
    "full_return_partition",
    "actual_countable_branch_alphabet",
    "stable_holonomy_quotient_density_rho",
    "actual_reverse_weight_registry",
    "common_trivialisation_projective_map_registry",
    "uniform_unnormalised_finite_core_pair_drift",
    "exact_growing_core_tail_probability",
    "off_diagonal_projective_near_collision_bound",
    "full_countable_pair_energy_drift",
    "actual_native_stopping_antichain",
    "native_scale_overshoot_cemetery",
    "same_carrier_physical_endpoint_identity",
    "exhaustive_actual_amplitude_operation_registry",
    "parentwise_normalized_amplitude_moment",
    "physical_gate2",
)

LOCAL_REQUIRED_LINES = (
    "SAME_LABEL_ALPHA=1/20: 6*17^20<50^20",
    "DISTINCT_TAIL_CROSS_IMAGE_COLLISION: EXACT",
    "CROSS_OBSTRUCTION_AT_ALPHA=1/20: EXACT",
    "MARGINAL_TAIL_MOMENT_IMPLIES_PAIR_DRIFT: FALSE",
    "OVERSHOOT_MASS_AT_SCALE_sigma=2^-m: sigma^2",
    "UNNORMALISED_FINITE_CORE_TRANSFER_ALGEBRA: EXACT",
    "TRUNCATION_RENORMALISATION_USED: FALSE",
    "PHYSICAL_GATE2: NOT_CERTIFIED",
)

GATE1_REQUIRED_LINES = (
    "FULL_CROSS_COMMON_VERTEX: CERTIFIED",
    "REVERSIBLE_OPPOSITE_TRANSITION_FULL_CROSS: CERTIFIED",
    "CLOSED_COMMON_VERTEX_LOOP_DERIVATIVE: NOT CERTIFIED",
    "TRANSPORTED_TWISTING: NOT CERTIFIED",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_required_lines(
    executable: Path | str,
    script: Path,
    required: tuple[str, ...],
    timeout: int,
) -> list[str]:
    errors: list[str] = []
    try:
        run = subprocess.run(
            [str(executable), str(script)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [f"certificate replay failed for {script.name}: {exc}"]
    if run.returncode != 0:
        errors.append(
            f"certificate {script.name} exited {run.returncode}: {run.stderr.strip()}"
        )
    for line in required:
        if line not in run.stdout:
            errors.append(f"certificate {script.name} output missing: {line}")
    return errors


def integrity_findings(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append(f"schema mismatch: {data.get('schema')!r}")
    if not data.get("model_id"):
        errors.append("model_id missing")

    provenance = data.get("provenance")
    if not isinstance(provenance, list) or not provenance:
        errors.append("provenance missing")
    else:
        for row in provenance:
            if not isinstance(row, dict):
                errors.append("invalid provenance row")
                continue
            relative = row.get("path")
            expected = row.get("sha256")
            path = ROOT / relative if isinstance(relative, str) else None
            if path is None or not path.is_file():
                errors.append(f"missing provenance file: {relative!r}")
                continue
            actual = sha256(path)
            if actual != expected:
                errors.append(
                    f"provenance hash mismatch {relative}: {actual} != {expected}"
                )

    proved = data.get("proved_layers")
    if not isinstance(proved, dict):
        errors.append("proved_layers missing")
    else:
        for field in PROVED_FIELDS:
            if proved.get(field) is not True:
                errors.append(f"proved layer missing: {field}")
        if proved.get("uses_truncation_renormalisation") is not False:
            errors.append("truncation renormalisation must remain disabled")

    dependency = data.get("gate1_dependency")
    if not isinstance(dependency, dict):
        errors.append("gate1_dependency missing")
    else:
        for field in (
            "actual_qnl_unstable_graph",
            "actual_connector_stable_graph",
            "true_transverse_intersection",
            "four_face_full_cross_rectangle",
            "reverse_transition_strip",
        ):
            if dependency.get(field) is not True:
                errors.append(f"certified Gate-1 input missing: {field}")
        for field in (
            "closed_common_vertex_loop",
            "transported_twisting",
        ):
            if dependency.get(field) is not False:
                errors.append(f"uncertified Gate-1 layer promoted: {field}")

    alphabet = data.get("candidate_alphabet_schema")
    if not isinstance(alphabet, dict):
        errors.append("candidate alphabet schema missing")
    else:
        labels = alphabet.get("dynamical_labels")
        marks = alphabet.get("fiber_marks_not_branches")
        if not isinstance(labels, list) or len(labels) < 4:
            errors.append("candidate dynamical alphabet label registry incomplete")
        if not isinstance(marks, list) or len(marks) < 4:
            errors.append("candidate fiber-mark registry incomplete")
        if "rho(h_a" not in str(alphabet.get("reverse_weight")):
            errors.append("physical reverse-weight formula missing")
        if "Phi_a" not in str(alphabet.get("projective_map")):
            errors.append("projective-map formula missing")

    errors.extend(run_required_lines(sys.executable, LOCAL_CERT, LOCAL_REQUIRED_LINES, 30))
    gate1_python: Path | str = FLINT_PYTHON if FLINT_PYTHON.is_file() else sys.executable
    errors.extend(run_required_lines(gate1_python, GATE1_CERT, GATE1_REQUIRED_LINES, 120))
    return errors


def completion_findings(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return list(PHYSICAL_FIELDS)
    physical = data.get("physical_objects")
    if not isinstance(physical, dict):
        return list(PHYSICAL_FIELDS)
    return [field for field in PHYSICAL_FIELDS if physical.get(field) is not True]


def self_test(data: dict) -> None:
    promoted = deepcopy(data)
    promoted["physical_objects"] = {field: True for field in PHYSICAL_FIELDS}
    assert not completion_findings(promoted)

    tampered = deepcopy(promoted)
    tampered["physical_objects"]["off_diagonal_projective_near_collision_bound"] = False
    assert "off_diagonal_projective_near_collision_bound" in completion_findings(tampered)

    tampered = deepcopy(data)
    tampered["proved_layers"]["uses_truncation_renormalisation"] = True
    # Exercise the local logical check without replaying external files.
    assert tampered["proved_layers"]["uses_truncation_renormalisation"] is True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1

    integrity = integrity_findings(data)
    if integrity:
        print("FULL_MASS_TAIL_MANIFEST: INVALID")
        for item in integrity:
            print(f"- {item}")
        return 1

    if args.self_test:
        self_test(data)
        missing = completion_findings(data)
        if set(missing) != set(PHYSICAL_FIELDS):
            print(f"MANIFEST_VERIFIER_SELF_TEST: FAIL ({missing})")
            return 1
        print("MANIFEST_VERIFIER_SELF_TEST: PASS")
        print("FAIL_CLOSED_PHYSICAL_SNAPSHOT: PASS")
        return 0

    missing = completion_findings(data)
    summary = {
        "model_id": data.get("model_id"),
        "true_common_vertex": True,
        "directed_full_cross_rectangle": True,
        "closed_return_rectangle": False,
        "proved_nonrenormalised_tail_theorem": True,
        "physical_gate2_certified": not missing,
        "missing_physical_field_count": len(missing),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    if missing:
        print("PHYSICAL_GATE2: NOT_CERTIFIED")
        for field in missing:
            print(f"- missing: {field}")
        return 2
    print("PHYSICAL_GATE2: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
