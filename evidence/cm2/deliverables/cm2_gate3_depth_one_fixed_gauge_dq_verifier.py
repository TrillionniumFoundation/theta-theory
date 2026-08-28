#!/usr/bin/env python3
"""Fail-closed verifier for the corrected depth-one fixed-gauge DQ."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.depth-one-fixed-gauge-dq.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate3_depth_one_fixed_gauge_dq_cert.py"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or not dependencies:
        errors.append("dependencies missing")
    else:
        for name, expected in dependencies.items():
            path = HERE / name
            if not path.is_file():
                errors.append(f"missing dependency: {name}")
            elif sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != "cm2.gate3.depth-one-fixed-gauge-dq.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    if provenance.get("maximal_row_registry_sha256") != (
        "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
    ):
        errors.append("maximal-row registry digest mismatch")
    if provenance.get("supersedes_global_current_scale_in") != (
        "cm2-gate3-global-borel-current-assembly-manifest-2026-07-15.json"
    ):
        errors.append("superseded-current provenance mismatch")

    correction = result.get("collision_coordinate_correction", {})
    coordinates = correction.get("collision_coordinates", {})
    derivatives = correction.get("exact_derivatives", {})
    for key, expected in {
        "p": "sin(phi)",
        "jacobian_identity": "dp=cp*dphi",
        "collision_law_before_normalization": "cos(phi)*dr*dphi=dr*dp",
    }.items():
        if coordinates.get(key) != expected:
            errors.append(f"collision-coordinate mismatch: {key}")
    for key, expected in {
        "partial_s_Delta": "2*eta*epsilon*R_T*u_y",
        "partial_p_Delta": "2*epsilon*R_T*ell_T/cp",
        "signed_face_coarea": "eta*epsilon*cp*u_y/ell_T",
    }.items():
        if derivatives.get(key) != expected:
            errors.append(f"coarea derivative mismatch: {key}")
    if correction.get("corrected_positive_row_law") != (
        "dm_e=R_source*cp*abs(u_y)/ell_T*dtheta"
    ):
        errors.append("corrected positive row law mismatch")
    if correction.get("old_to_corrected_density_ratio") != "cp":
        errors.append("old/corrected density ratio mismatch")

    assembly = result.get("corrected_current_assembly", {})
    for key, expected in {
        "maximal_row_current_count": 64,
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }.items():
        if assembly.get(key) != expected:
            errors.append(f"corrected current assembly mismatch: {key}")
    for key in (
        "corrected_positive_coarea_law_attached_to_every_row",
        "strict_hit_and_miss_trace_attached_to_every_row",
        "one_shared_plus_minus_mark_per_occurrence",
    ):
        if assembly.get(key) is not True:
            errors.append(f"missing corrected current flag: {key}")

    envelope = result.get("uniform_finite_measure_envelope", {})
    for key, expected in {
        "corrected_density_formula": "R_source*cp*abs(u_y)/ell_T",
        "superseded_density_formula": "R_source*cp^2*abs(u_y)/ell_T",
        "target_tangent_flight_strict_lower_bound": "1/10",
        "unnormalized_coarea_density_upper_bound_wrt_dtheta": "18/5",
        "global_event_current_TV_upper_bound": "16128/5",
    }.items():
        if envelope.get(key) != expected:
            errors.append(f"finite-envelope mismatch: {key}")
    if envelope.get("numerical_upper_bounds_unchanged_after_correction") is not True:
        errors.append("corrected-envelope preservation missing")
    try:
        if Fraction(envelope["global_event_current_TV_upper_bound"]) != 2 * Fraction(
            envelope["global_positive_mass_upper_bound"]
        ):
            errors.append("global TV identity mismatch")
    except (KeyError, TypeError, ValueError):
        errors.append("invalid corrected-envelope arithmetic")

    pairing = result.get("exact_Jx_scalar_pairing", {})
    for key, expected in {
        "exact_Jx_maximal_row_pair_count": 32,
        "global_signed_scalar_coarea_mass": "0",
        "Jx_pair_rows_sha256": (
            "11ee023e90fa2be2c318ad28c1691f6407eadf6b9a901b7543e4fdbe33ee6abb"
        ),
    }.items():
        if pairing.get(key) != expected:
            errors.append(f"Jx pairing mismatch: {key}")
    if pairing.get("transformation_law", {}).get("positive_density") != (
        "R_source*cp*abs(u_y)/ell_T preserved"
    ):
        errors.append("corrected Jx density mismatch")

    audit = result.get("finite_event_atlas_dependency_audit", {})
    for key, expected in {
        "physical_pair_simultaneous_first_occurrences": 0,
        "physical_triple_simultaneous_first_occurrences": 0,
        "physical_joint_vertices": 0,
        "remaining_two_dimensional_unresolved_parameter_area": "0",
    }.items():
        if audit.get(key) != expected:
            errors.append(f"event-atlas audit mismatch: {key}")
    for key in (
        "chart_seams_have_unique_physical_owner",
        "duplicate_chart_and_lift_traces_cancel_before_absolute_values",
    ):
        if audit.get(key) is not True:
            errors.append(f"missing event-atlas flag: {key}")

    dq = result.get("fixed_gauge_depth_one_DQ", {})
    radical = dq.get("regular_radical_stitching", {})
    for key, expected in {
        "maximal_connected_face_rows": 64,
        "state_changing_row_boundaries": 88,
        "uniform_abs_partial_phi_Delta_lower": "4/125",
        "face_law": "dm_e=R_source*cp*abs(u_y)/ell_T*dtheta",
    }.items():
        if radical.get(key) != expected:
            errors.append(f"radical stitching mismatch: {key}")
    for key in (
        "persistent_smooth_core_cover_is_finite",
        "finite_difference_quotient_converges_on_every_persistent_core",
    ):
        if dq.get("smooth_core_derivative", {}).get(key) is not True:
            errors.append(f"missing smooth-core flag: {key}")
    operator = dq.get("operator_conclusion", {})
    if operator.get("uncentered_depth_one_transfer_DQ") != "CERTIFIED":
        errors.append("uncentered depth-one DQ verdict mismatch")
    if operator.get("centered_depth_one_fixed_gauge_DQ") != "CERTIFIED":
        errors.append("centered depth-one DQ verdict mismatch")
    if operator.get(
        "limiting_defect_is_smooth_core_plus_corrected_face_current"
    ) is not True:
        errors.append("limiting defect assembly missing")

    limits = result.get("scope_limits", {})
    for key in (
        "corrected_global_finite_Borel_event_current",
        "corrected_global_signed_scalar_coarea_matching",
        "complete_depth_one_transfer_difference_quotient",
        "smooth_fixed_core_derivative",
        "regular_radical_boundary_tightness",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "dynamic_iterated_C1_test_tightness",
        "full_MT_DQ_interface",
        "CM2_time_decay_majorant",
        "numeric_forward_reverse_standard_family_costs",
        "controlled_stopped_parent_recovery",
        "gate3_certified",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("coarea_collision_coordinate_scale") != "CORRECTED":
        errors.append("coarea correction verdict mismatch")
    if verdict.get("complete_depth_one_fixed_gauge_DQ") != "CERTIFIED":
        errors.append("depth-one DQ verdict mismatch")
    if verdict.get("dynamic_iterated_test_MT_DQ") != "NOT_CERTIFIED":
        errors.append("dynamic MT_DQ must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_depth_one_fixed_gauge_dq_cert as cert
        actual = cert.certify()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["full certificate replay mismatch"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1
    errors = check_structure(data)
    if args.replay and not errors:
        errors.extend(check_replay(data))
    if errors:
        print("GATE3_DEPTH_ONE_FIXED_GAUGE_DQ_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["collision_coordinate_correction"][
            "corrected_positive_row_law"
        ] = "dm_e=R_source*cp^2*abs(u_y)/ell_T*dtheta"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (double-cp scale accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["full_MT_DQ_interface"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported MT_DQ completion accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  double-cp scale tamper rejected")
        print("  unsupported dynamic MT_DQ completion rejected")
        return 0
    print("GATE3_COAREA_COLLISION_COORDINATE_SCALE: CORRECTED")
    print("GATE3_COMPLETE_DEPTH_ONE_FIXED_GAUGE_DQ: CERTIFIED")
    if args.integrity_only:
        print("GATE3_DEPTH_ONE_FIXED_GAUGE_DQ_INTEGRITY: PASS")
        return 0
    print("GATE3_DYNAMIC_ITERATED_TEST_MT_DQ: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
