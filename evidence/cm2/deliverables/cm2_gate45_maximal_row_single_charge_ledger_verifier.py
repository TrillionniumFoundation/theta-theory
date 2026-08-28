#!/usr/bin/env python3
"""Fail-closed verifier for the maximal-row Gate-4/5 charge ledger."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.maximal-row-single-charge-ledger.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-maximal-row-single-charge-ledger-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate45_maximal_row_single_charge_ledger_cert.py"


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
    provenance = result.get("provenance", {})
    for key, expected in {
        "maximal_row_manifest": "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json",
        "global_current_manifest": "cm2-gate3-global-borel-current-assembly-manifest-2026-07-15.json",
        "maximal_row_registry_sha256": "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630",
        "global_current_rows_sha256": "90b7e85dcea38b6b90e9ae57e7943030d7d205e0e5b3dce57721e3231953621d",
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    ledger = result.get("global_structural_occurrence_ledger", {})
    for key, expected in {
        "maximal_physical_occurrence_count": 64,
        "common_positive_law_count": 64,
        "pre_recovery_single_charge_expression_count": 64,
        "singular_kac_coordinate_count": 128,
        "incorrect_per_coordinate_double_charge_count": 128,
        "occurrence_rows_sha256": "ac58e2ad57fa3f5e0db74a8c2b3ac3fff6896cbc1d8e5674f1552acbd75bc644",
    }.items():
        if ledger.get(key) != expected:
            errors.append(f"occurrence ledger mismatch: {key}")
    for key in (
        "same_occurrence_forward_reverse_views_on_every_row",
        "endpoint_views_are_nonadditive_on_every_row",
        "one_common_m_per_occurrence",
        "one_q_expression_per_occurrence",
        "all_singular_coordinate_pairs_share_mark_plus_one_minus_one",
    ):
        if ledger.get(key) is not True:
            errors.append(f"missing occurrence flag: {key}")
    try:
        if ledger["singular_kac_coordinate_count"] != 2 * ledger[
            "maximal_physical_occurrence_count"
        ]:
            errors.append("singular-coordinate count identity mismatch")
        if ledger["pre_recovery_single_charge_expression_count"] != ledger[
            "maximal_physical_occurrence_count"
        ]:
            errors.append("single-charge count identity mismatch")
    except (KeyError, TypeError):
        errors.append("invalid occurrence count ledger")

    kac = result.get("global_finite_borel_kac_layer", {})
    for key, expected in {
        "global_event_current_TV_upper_bound": "16128/5",
        "global_signed_scalar_coarea_mass": "0",
        "maximal_row_Jx_pair_count": 32,
        "algebra_sample_digest": "1ef7577d75af57eeaa0f3e00af1af88f374dca3494913a8d2fcc74c02fb263c6",
    }.items():
        if kac.get(key) != expected:
            errors.append(f"Borel Kac mismatch: {key}")
    for key in (
        "finite_borel_endpoint_adjoint_exact",
        "finite_borel_kac_tower_pairing_exact",
        "finite_borel_prefix_suffix_pairing_exact",
        "four_term_centered_algebra_exact",
        "singular_coordinates_share_one_occurrence_measure",
        "constant_observable_rowwise_singular_centering",
        "global_bounded_Borel_event_current_assembled",
    ):
        if kac.get(key) is not True:
            errors.append(f"missing Borel Kac flag: {key}")

    boundary = result.get("recovery_and_CM2_boundary", {})
    if boundary.get("forward_reverse_Borel_change_of_variables") is not True:
        errors.append("Borel two-view identity missing")
    if boundary.get("arbitrary_Borel_stopped_recovery") is not False:
        errors.append("arbitrary-Borel recovery must remain false")
    if boundary.get("global_Borel_TV_cost_is_not_C_fw_or_C_rev") is not True:
        errors.append("Borel/CM2 cost distinction missing")
    missing = boundary.get("missing_numeric_fields")
    if not isinstance(missing, list) or len(missing) != 6:
        errors.append("missing numeric field ledger mismatch")

    completion = result.get("completion", {})
    for key in (
        "maximal_connected_physical_event_rows",
        "global_finite_Borel_event_current",
        "global_signed_scalar_coarea_matching",
        "same_occurrence_two_view_common_m_on_every_maximal_row",
        "one_pre_recovery_q_expression_per_maximal_occurrence",
        "bounded_Borel_singular_Kac_typing_on_all_maximal_rows",
        "exact_four_term_Borel_Kac_algebra",
    ):
        if completion.get(key) is not True:
            errors.append(f"missing structural completion flag: {key}")
    for key in (
        "numeric_forward_reverse_CM2_costs",
        "controlled_stopped_parent_recovery",
        "standard_family_CM2_norm_lift",
        "flux_face_CM2_norm_lift",
        "dynamic_test_CM2_norm_lift",
        "physical_four_term_Kac_CM2_typing",
        "gate4_certified",
        "gate5_certified",
    ):
        if completion.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("maximal_row_single_charge_ledger") != "CERTIFIED":
        errors.append("single-charge ledger verdict mismatch")
    if verdict.get("global_finite_Borel_Kac_layer") != "CERTIFIED":
        errors.append("Borel Kac verdict mismatch")
    if verdict.get("stopped_recovery_and_CM2_norms") != "NOT_CERTIFIED":
        errors.append("CM2 completion verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_maximal_row_single_charge_ledger_cert as cert
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
        print("GATE45_MAXIMAL_ROW_SINGLE_CHARGE_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["global_structural_occurrence_ledger"][
            "pre_recovery_single_charge_expression_count"
        ] = 128
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (double-charge tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["completion"]["controlled_stopped_parent_recovery"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported recovery accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  double-charge tamper rejected")
        print("  unsupported recovery completion rejected")
        return 0
    print("GATE45_MAXIMAL_ROW_SINGLE_CHARGE_LEDGER: CERTIFIED")
    print("GATE45_GLOBAL_FINITE_BOREL_KAC_LAYER: CERTIFIED")
    if args.integrity_only:
        print("GATE45_MAXIMAL_ROW_SINGLE_CHARGE_INTEGRITY: PASS")
        return 0
    print("GATE45_STOPPED_RECOVERY_AND_CM2_NORMS: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
