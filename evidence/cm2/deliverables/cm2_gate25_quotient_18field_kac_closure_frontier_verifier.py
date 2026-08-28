#!/usr/bin/env python3
"""Fail-closed verifier for the quotient/18-field/Kac frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate25_quotient_18field_kac_closure_frontier_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate25.quotient-18field-kac-closure-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate25.quotient-18field-kac-closure-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate25-quotient-18field-kac-closure-frontier-manifest-2026-07-17.json"
)
CERTIFICATE = (
    HERE / "cm2_gate25_quotient_18field_kac_closure_frontier_cert.py"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def check(manifest: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest type"]
    if manifest.get("schema") != SCHEMA:
        errors.append("manifest schema")
    if manifest.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash")
    if manifest.get("dependencies") != certificate.DEPENDENCIES:
        errors.append("dependency table")
    else:
        for name, expected in certificate.DEPENDENCIES.items():
            path = HERE / name
            if not path.is_file() or sha256_path(path) != expected:
                errors.append(f"dependency {name}")

    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")

    countermodel = result.get("class_H_PPE_nonimplication", {})
    expected_countermodel = {
        "base_is_invertible": True,
        "holonomy_Holder_constant": 0,
        "cocycle_is_class_H": True,
        "reverse_conditional_support_size_at_every_target": 1,
        "reverse_kernel": "Dirac",
        "diagonal_two_copy_Riesz_coefficient": "1",
        "uniform_pair_energy_contraction_kappa_less_than_one": False,
        "class_H_implies_physical_PPE": False,
    }
    for key, expected in expected_countermodel.items():
        if countermodel.get(key) != expected:
            errors.append(f"countermodel {key}")

    gate2 = result.get("Gate2_17_field_completion", {})
    if gate2.get("required_field_count") != 17:
        errors.append("Gate2 field count")
    if gate2.get("completed_physical_field_count") != 0:
        errors.append("Gate2 completed count")
    rows2 = gate2.get("rows", [])
    if not isinstance(rows2, list) or len(rows2) != 17:
        errors.append("Gate2 rows")
    elif any(row.get("physical_completion") is not False for row in rows2):
        errors.append("Gate2 false flags")
    if gate2.get("separate_class_H_theorem_populates_any_physical_quotient_field") is not False:
        errors.append("Gate2 class H scope")
    if gate2.get("stable_quotient") != "NOT_CERTIFIED":
        errors.append("Gate2 quotient status")
    if gate2.get("physical_PPE") != "NOT_CERTIFIED":
        errors.append("Gate2 PPE status")

    gate5 = result.get("Gate5_18_field_maturity", {})
    expected_gate5 = {
        "required_field_count_per_level": 18,
        "schema_level_all_key_formula_field_count": 1,
        "schema_level_all_key_formula_fields": ["one_step_cut_growth_Z_sum"],
        "core_local_seed_field_count": 2,
        "core_local_seed_fields": [
            "inverse_Jacobian_bound",
            "log_Jacobian_distortion_sum",
        ],
        "field7_growth_contraction": False,
        "homogeneous_subbranch_ids_materialized": False,
        "complete_physical_homogeneous_slot_field_count": 0,
        "complete_18_field_operator_block_count": 0,
    }
    for key, expected in expected_gate5.items():
        if gate5.get(key) != expected:
            errors.append(f"Gate5 maturity {key}")
    rows5 = gate5.get("rows", [])
    if not isinstance(rows5, list) or len(rows5) != 18:
        errors.append("Gate5 rows")
    elif any(
        row.get("complete_physical_homogeneous_slot") is not False
        for row in rows5
    ):
        errors.append("Gate5 slot completion")
    else:
        by_field = {row.get("field"): row for row in rows5}
        if by_field.get("inverse_Jacobian_bound", {}).get("maturity") != (
            "24_CORE_LOCAL_SEED"
        ):
            errors.append("field5 maturity")
        if by_field.get("log_Jacobian_distortion_sum", {}).get("maturity") != (
            "24_CORE_LOCAL_SEED"
        ):
            errors.append("field6 maturity")
        if by_field.get("one_step_cut_growth_Z_sum", {}).get("maturity") != (
            "ALL_441280_KEYS_AND_COMPONENTS_FINITE_FORMULA_NONCONTRACTING"
        ):
            errors.append("field7 maturity")

    closure = result.get("three_norm_Kac_phase", {})
    norm_rows = closure.get("three_norm_rows", [])
    if not isinstance(norm_rows, list) or len(norm_rows) != 3:
        errors.append("three norm rows")
    elif any(row.get("return_wide_completion") is not False for row in norm_rows):
        errors.append("three norm completion")
    if closure.get("one_collision_three_norm_seeds") != "CERTIFIED":
        errors.append("norm seeds")
    if closure.get("return_wide_three_norm_intertwiners") != "NOT_CERTIFIED":
        errors.append("norm status")
    kac = closure.get("Kac", {})
    if kac.get("finite_Borel_four_term_algebra") != "CERTIFIED":
        errors.append("Kac algebra")
    if kac.get("full_four_term_physical_Kac_CM2_output") != "NOT_CERTIFIED":
        errors.append("Kac scope")
    phase = closure.get("phase", {})
    expected_phase = {
        "preferred_route": "direct_standard_N",
        "component_cycle_gcd": 1,
        "component_period_obstruction_removed": True,
        "separate_phase_tower_required_on_preferred_route": False,
        "direct_route_phase_choice": "CERTIFIED",
        "all_return_word_operator_phase_blocks_registered": False,
        "optional_operator_Wiener_phase_transfer": "NOT_CERTIFIED",
    }
    for key, expected in expected_phase.items():
        if phase.get(key) != expected:
            errors.append(f"phase {key}")
    conditional = closure.get("conditional_direct_route_closure", {})
    if conditional.get("hypotheses_currently_met") is not False:
        errors.append("conditional closure scope")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "separate_class_H_gauges_imply_stable_quotient",
        "class_H_implies_reverse_randomness_or_PPE",
        "field7_formula_implies_complete_18_field_block",
        "one_collision_norm_seeds_imply_return_wide_intertwiners",
        "component_gcd_one_implies_operator_phase_blocks",
        "Borel_Kac_algebra_implies_physical_CM2_Kac_output",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in ("Gate1", "Gate2", "Gate5"):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "class_H_to_physical_PPE_nonimplication": "CERTIFIED",
        "Gate2_completed_physical_quotient_fields": "0/17",
        "Gate5_all_key_formula_fields": "1/18",
        "Gate5_complete_physical_operator_blocks": 0,
        "direct_standard_N_phase_route_choice": "CERTIFIED",
        "stable_quotient_PPE_three_norm_Kac": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    if manifest.get("verdict") != expected_verdict:
        errors.append("verdict")
    return errors


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(
        manifest["result"]
    )


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[str, ...], value: Any) -> None:
        candidate = copy.deepcopy(manifest)
        target: Any = candidate
        for part in path[:-1]:
            target = target[part]
        target[path[-1]] = value
        if path[0] == "result":
            refresh(candidate)
        mutations.append(candidate)

    mutate(("result", "class_H_PPE_nonimplication", "reverse_kernel"), "NON_DIRAC")
    mutate(("result", "class_H_PPE_nonimplication", "class_H_implies_physical_PPE"), True)
    mutate(("result", "Gate2_17_field_completion", "completed_physical_field_count"), 1)
    mutate(("result", "Gate2_17_field_completion", "stable_quotient"), "CERTIFIED")
    mutate(("result", "Gate5_18_field_maturity", "schema_level_all_key_formula_field_count"), 3)
    mutate(("result", "Gate5_18_field_maturity", "field7_growth_contraction"), True)
    mutate(("result", "Gate5_18_field_maturity", "complete_18_field_operator_block_count"), 1)
    mutate(("result", "three_norm_Kac_phase", "return_wide_three_norm_intertwiners"), "CERTIFIED")
    mutate(("result", "three_norm_Kac_phase", "Kac", "full_four_term_physical_Kac_CM2_output"), "CERTIFIED")
    mutate(("result", "three_norm_Kac_phase", "phase", "component_cycle_gcd"), 2)
    mutate(("result", "three_norm_Kac_phase", "phase", "all_return_word_operator_phase_blocks_registered"), True)
    mutate(("result", "three_norm_Kac_phase", "conditional_direct_route_closure", "hypotheses_currently_met"), True)
    mutate(("result", "strict_nonpromotion", "class_H_implies_reverse_randomness_or_PPE"), True)
    mutate(("verdict", "Gate5"), "CERTIFIED")
    rejected = sum(bool(check(candidate)) for candidate in mutations)
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as error:
        print(f"MANIFEST_READ_ERROR: {error}", file=sys.stderr)
        return 1
    errors = check(manifest)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.replay and certificate.build_result() != manifest["result"]:
        print("ERROR: replay mismatch", file=sys.stderr)
        return 1
    if args.self_test:
        rejected, total = self_test(manifest)
        status = "PASS" if rejected == total else "FAIL"
        print(f"SELF_TEST: {status} ({rejected}/{total} mutations rejected)")
        return 0 if rejected == total else 1
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("ALL_KEY_GATE5_FIELD7_FORMULA: CERTIFIED_NONCONTRACTING")
    print("DIRECT_STANDARD_N_PHASE_ROUTE_CHOICE: CERTIFIED")
    print("STABLE_QUOTIENT_PPE_18_FIELDS_THREE_NORMS_KAC: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
