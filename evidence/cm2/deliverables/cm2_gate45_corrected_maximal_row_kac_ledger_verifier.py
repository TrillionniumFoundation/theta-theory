#!/usr/bin/env python3
"""Fail-closed verifier for the corrected maximal-row Kac ledger."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.corrected-maximal-row-kac-ledger.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate45_corrected_maximal_row_kac_ledger_cert.py"


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
    if result.get("schema") != "cm2.gate45.corrected-maximal-row-kac-ledger.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "corrected_DQ_manifest": (
            "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
        ),
        "controlled_interval_algebra_manifest": (
            "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
        ),
        "all_row_slope_manifest": (
            "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
        ),
        "maximal_row_registry_sha256": (
            "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
        ),
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
        "supersedes_structural_scale_binding_in": (
            "cm2-gate45-maximal-row-single-charge-ledger-manifest-2026-07-15.json"
        ),
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    ledger = result.get("corrected_global_occurrence_ledger", {})
    for key, expected in {
        "maximal_physical_occurrence_count": 64,
        "corrected_common_positive_law_count": 64,
        "pre_recovery_single_charge_expression_count": 64,
        "slope_only_numeric_subcharge_count": 64,
        "controlled_mass_coordinate_count": 64,
        "singular_kac_coordinate_count": 128,
        "incorrect_per_coordinate_double_charge_count": 128,
        "corrected_occurrence_rows_sha256": (
            "dee3b15f6747e81a7c63ef7b3c5e3c9b2e3ed3fc61339c0113f0ec618c5cb30f"
        ),
    }.items():
        if ledger.get(key) != expected:
            errors.append(f"corrected occurrence ledger mismatch: {key}")
    for key in (
        "same_occurrence_forward_reverse_views_on_every_row",
        "endpoint_views_are_nonadditive_on_every_row",
        "one_corrected_m_per_occurrence",
        "one_q_expression_per_occurrence",
        "all_singular_coordinate_pairs_share_mark_plus_one_minus_one",
    ):
        if ledger.get(key) is not True:
            errors.append(f"missing corrected occurrence flag: {key}")

    kac = result.get("corrected_global_finite_borel_kac_layer", {})
    for key, expected in {
        "global_event_current_TV_upper_bound": "16128/5",
        "global_signed_scalar_coarea_mass": "0",
        "maximal_row_Jx_pair_count": 32,
        "algebra_sample_digest": (
            "1ef7577d75af57eeaa0f3e00af1af88f374dca3494913a8d2fcc74c02fb263c6"
        ),
    }.items():
        if kac.get(key) != expected:
            errors.append(f"corrected Kac mismatch: {key}")
    for key in (
        "finite_borel_endpoint_adjoint_exact",
        "finite_borel_kac_tower_pairing_exact",
        "finite_borel_prefix_suffix_pairing_exact",
        "four_term_centered_algebra_exact",
        "singular_coordinates_share_one_corrected_occurrence_measure",
        "constant_observable_rowwise_singular_centering",
        "global_corrected_bounded_borel_event_current_assembled",
    ):
        if kac.get(key) is not True:
            errors.append(f"missing corrected Kac flag: {key}")

    boundary = result.get("controlled_recovery_and_CM2_boundary", {})
    for key, expected in {
        "arbitrary_Borel_stopped_recovery": False,
        "controlled_dyadic_restriction_algebra": True,
        "fat_Cantor_restrictions_excluded_by_policy": True,
        "all_row_source_stable_and_miss_image_unstable_orientation": True,
        "global_broad_slope_envelope": "29",
        "slope_only_single_charge": "q_e^slope=29*m_e",
        "controlled_dyadic_stopped_recovery": False,
        "complete_numeric_C_fw_C_rev": False,
    }.items():
        if boundary.get(key) != expected:
            errors.append(f"corrected recovery boundary mismatch: {key}")

    completion = result.get("completion", {})
    for key in (
        "corrected_global_finite_Borel_event_current",
        "corrected_global_signed_scalar_matching",
        "complete_depth_one_fixed_gauge_DQ",
        "same_occurrence_two_view_corrected_m_on_every_row",
        "one_symbolic_q_expression_per_maximal_occurrence",
        "one_numeric_slope_subcharge_per_maximal_occurrence",
        "controlled_dyadic_restriction_algebra",
        "corrected_bounded_Borel_singular_Kac_typing",
        "exact_four_term_Borel_Kac_algebra",
    ):
        if completion.get(key) is not True:
            errors.append(f"missing corrected completion flag: {key}")
    for key in (
        "complete_numeric_forward_reverse_CM2_costs",
        "controlled_stopped_parent_recovery",
        "dynamic_test_MT_DQ",
        "standard_family_CM2_norm_lift",
        "flux_face_CM2_norm_lift",
        "dynamic_test_CM2_norm_lift",
        "physical_four_term_Kac_CM2_typing",
        "gate4_certified",
        "gate5_certified",
    ):
        if completion.get(key) is not False:
            errors.append(f"unsupported corrected completion flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("corrected_64_row_single_charge_ledger") != "CERTIFIED":
        errors.append("corrected charge ledger verdict mismatch")
    if verdict.get("corrected_128_coordinate_Borel_Kac_layer") != "CERTIFIED":
        errors.append("corrected Kac verdict mismatch")
    if verdict.get("physical_recovery_and_CM2_norm_lifts") != "NOT_CERTIFIED":
        errors.append("physical completion verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_corrected_maximal_row_kac_ledger_cert as cert
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
        print("GATE45_CORRECTED_MAXIMAL_ROW_KAC_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["corrected_global_occurrence_ledger"][
            "singular_kac_coordinate_count"
        ] = 64
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (Kac coordinate tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["completion"]["controlled_stopped_parent_recovery"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported recovery accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  Kac-coordinate tamper rejected")
        print("  unsupported physical recovery rejected")
        return 0
    print("GATE45_CORRECTED_64_ROW_SINGLE_CHARGE_LEDGER: CERTIFIED")
    print("GATE45_CORRECTED_128_COORDINATE_BOREL_KAC_LAYER: CERTIFIED")
    if args.integrity_only:
        print("GATE45_CORRECTED_MAXIMAL_ROW_KAC_INTEGRITY: PASS")
        return 0
    print("GATE45_PHYSICAL_RECOVERY_AND_CM2_NORM_LIFTS: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
