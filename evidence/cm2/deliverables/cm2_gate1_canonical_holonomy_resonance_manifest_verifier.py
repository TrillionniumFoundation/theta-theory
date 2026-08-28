#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-1 canonical-holonomy resonance audit."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


SCHEMA = "cm2.gate1.canonical-holonomy-resonance.v1"
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate1-canonical-holonomy-resonance-manifest-2026-07-15.json"
)
CERT = HERE / "cm2_gate1_canonical_holonomy_resonance_cert.py"
FLINT_PYTHON = Path("/tmp/cm2-flint-venv/bin/python")

PROVED_FIELDS = (
    "failure_of_uniform_fiber_bunching_on_natural_two_step_coding",
    "failure_of_uniform_fiber_bunching_on_induced_qnl_return",
    "shadow_basepoint_is_not_qnl_homoclinic",
    "global_gray_identity_is_not_canonical_holonomy",
    "canonical_stable_limit_fails_at_qnl",
    "butler_park_class_H_canonical_limit_fails_on_faithful_frozen_representative",
    "finite_shadow_is_not_qnl_canonical_holonomy",
    "park_piraino_on_two_frozen_natural_codings_no_go",
)

POSITIVE_FIELDS = (
    "true_common_vertex",
    "twenty_four_collision_four_face_full_cross",
    "ninety_six_collision_finite_shadow",
    "four_finite_shadow_wedges",
)

COMPLETION_FIELDS = (
    "actual_full_mass_physical_quotient",
    "direct_place_dependent_projective_frostman_or_pair_energy_theorem",
    "alternative_lower_dimensional_cocycle_with_exact_endpoint_typing",
    "holder_cohomological_rescue_with_valid_holonomies",
    "theorem_accepting_that_actual_cocycle_without_failed_full_tangent_holonomy",
    "gate1_unconditional_typicality_input",
    "unconditional_cm2",
)

CERT_REQUIRED_LINES = (
    "FROZEN_GATE1_RESONANCE_DEPENDENCIES: VERIFIED",
    "QNL_EIGENJET_ALL_QUADRATIC_DERIVATIVES_ZERO: EXACT",
    "F2_xyy_over_stable=-325/72",
    "limiting_increment_coefficient=325/144",
    "CANONICAL_STABLE_HOLONOMY_AT_QNL: DOES_NOT_CONVERGE",
    "BUTLER_PARK_CLASS_H_CANONICAL_LIMIT_CONDITION_ON_FAITHFUL_FROZEN_REPRESENTATIVE: FAILS",
    "HOLDER_COHOMOLOGY_TO_LOCALLY_CONSTANT_QNL_COCYCLE: NOT CERTIFIED",
    "FINITE_SHADOW_AS_QNL_CANONICAL_HOLONOMY: REFUTED",
    "PARK_PIRAINO_ON_TWO_FROZEN_NATURAL_CODINGS: NO_GO",
    "BUTLER_PARK_H_VIA_NEW_COHOMOLOGY_OR_OTHER_NON_FB_THEOREM: OPEN",
    "GENUINELY_ALTERNATIVE_CODING_OR_TRANSPORT: OPEN",
    "GATE1_UNCONDITIONAL_TYPICALITY_INPUT: OPEN / FAIL-CLOSED",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certificate_findings() -> list[str]:
    executable: Path | str = FLINT_PYTHON if FLINT_PYTHON.is_file() else sys.executable
    try:
        run = subprocess.run(
            [str(executable), str(CERT)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return [f"certificate replay failed: {exc}"]
    errors: list[str] = []
    if run.returncode != 0:
        errors.append(f"certificate exited {run.returncode}: {run.stderr.strip()}")
    for line in CERT_REQUIRED_LINES:
        if line not in run.stdout:
            errors.append(f"certificate output missing: {line}")
    return errors


def integrity_findings(data: Any, replay: bool = True) -> list[str]:
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

    jet = data.get("exact_qnl_jet")
    if not isinstance(jet, dict):
        errors.append("exact_qnl_jet missing")
    else:
        if jet.get("lambda_times_mu") != "1 exactly":
            errors.append("reciprocal multiplier identity missing")
        if jet.get("all_second_derivatives_zero") is not True:
            errors.append("vanishing quadratic jet missing")
        if jet.get("F2_xyy_over_mu") != "-325/72 exactly":
            errors.append("resonant cubic coefficient changed")
        if jet.get("resonant_increment_coefficient") != "325/144 exactly":
            errors.append("resonant increment coefficient changed")

    lemma = data.get("resonant_increment_lemma")
    if not isinstance(lemma, dict):
        errors.append("resonant_increment_lemma missing")
    else:
        if lemma.get("canonical_stable_holonomy_at_qnl") != "DOES_NOT_CONVERGE":
            errors.append("canonical nonconvergence verdict missing")
        if "325/144" not in str(lemma.get("certified_limit")):
            errors.append("certified limiting increment missing")

    proved = data.get("proved_obstructions")
    if not isinstance(proved, dict):
        errors.append("proved_obstructions missing")
    else:
        for field in PROVED_FIELDS:
            if proved.get(field) is not True:
                errors.append(f"proved obstruction missing: {field}")

    positive = data.get("frozen_positive_predecessors")
    if not isinstance(positive, dict):
        errors.append("frozen_positive_predecessors missing")
    else:
        for field in POSITIVE_FIELDS:
            if positive.get(field) is not True:
                errors.append(f"positive predecessor retracted: {field}")
        if positive.get("positive_results_retracted") is not False:
            errors.append("positive predecessor retraction flag must be false")

    literature = data.get("literature_audit")
    if not isinstance(literature, list) or len(literature) < 5:
        errors.append("literature audit is incomplete")

    unresolved_alternatives = data.get("unresolved_alternative_routes")
    if not isinstance(unresolved_alternatives, dict):
        errors.append("unresolved_alternative_routes ledger missing")
    elif unresolved_alternatives.get(
        "faithful_holder_cohomology_to_a_locally_constant_model"
    ) != "NOT_CERTIFIED_NOT_REFUTED":
        errors.append("uncertified Holder cohomology was promoted")

    if replay:
        errors.extend(certificate_findings())
    return errors


def completion_findings(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return list(COMPLETION_FIELDS)
    completion = data.get("completion_requirements")
    if not isinstance(completion, dict):
        return list(COMPLETION_FIELDS)
    return [field for field in COMPLETION_FIELDS if completion.get(field) is not True]


def self_test(data: dict) -> None:
    promoted = deepcopy(data)
    promoted["completion_requirements"] = {
        field: True for field in COMPLETION_FIELDS
    }
    assert not completion_findings(promoted)

    tampered = deepcopy(promoted)
    tampered["completion_requirements"]["gate1_unconditional_typicality_input"] = False
    assert "gate1_unconditional_typicality_input" in completion_findings(tampered)

    tampered = deepcopy(data)
    tampered["exact_qnl_jet"]["resonant_increment_coefficient"] = "0"
    findings = integrity_findings(tampered, replay=False)
    assert "resonant increment coefficient changed" in findings

    tampered = deepcopy(data)
    tampered["frozen_positive_predecessors"]["positive_results_retracted"] = True
    findings = integrity_findings(tampered, replay=False)
    assert "positive predecessor retraction flag must be false" in findings

    tampered = deepcopy(data)
    tampered["unresolved_alternative_routes"][
        "faithful_holder_cohomology_to_a_locally_constant_model"
    ] = "CERTIFIED"
    findings = integrity_findings(tampered, replay=False)
    assert "uncertified Holder cohomology was promoted" in findings


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
        print("GATE1_CANONICAL_HOLONOMY_RESONANCE_MANIFEST: INVALID")
        for item in integrity:
            print(f"- {item}")
        return 1

    if args.self_test:
        self_test(data)
        missing = completion_findings(data)
        if set(missing) != set(COMPLETION_FIELDS):
            print(f"MANIFEST_VERIFIER_SELF_TEST: FAIL ({missing})")
            return 1
        print("MANIFEST_VERIFIER_SELF_TEST: PASS")
        print("FAIL_CLOSED_GATE1_SNAPSHOT: PASS")
        return 0

    missing = completion_findings(data)
    summary = {
        "model_id": data.get("model_id"),
        "finite_shadow_twisting_certified": True,
        "canonical_stable_holonomy_at_qnl": "DOES_NOT_CONVERGE",
        "park_piraino_on_two_frozen_natural_codings": "NO_GO",
        "butler_park_h_via_new_cohomology_or_other_non_fb_theorem": "OPEN_NOT_CERTIFIED",
        "genuinely_alternative_coding_or_transport": "OPEN_NOT_CERTIFIED",
        "gate1_unconditional_certified": not missing,
        "missing_completion_field_count": len(missing),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    if missing:
        print("GATE1_UNCONDITIONAL_TYPICALITY_INPUT: NOT_CERTIFIED")
        for field in missing:
            print(f"- missing: {field}")
        return 2
    print("GATE1_UNCONDITIONAL_TYPICALITY_INPUT: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
