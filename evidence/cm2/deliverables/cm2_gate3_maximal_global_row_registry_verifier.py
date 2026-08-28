#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 maximal global row registry."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.maximal-global-row-registry.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-maximal-global-row-registry-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate3_maximal_global_row_registry_cert.py"


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
    if result.get("precision_bits") != 256:
        errors.append("precision mismatch")
    domain = result.get("domain", {})
    if domain.get("active_global_signed_sheets") != 128:
        errors.append("active global sheet count mismatch")
    if domain.get("parameter_s") != ["-1/400", "1/400"]:
        errors.append("parameter window mismatch")

    claims = result.get("dependency_claims", {})
    for key, expected in {
        "source_grazing_stratification": "CERTIFIED",
        "parameter_polarity_stratification": "CERTIFIED",
        "active_first_visibility_stratification": "CERTIFIED",
        "active_miss_owner_stratification": "CERTIFIED",
        "remaining_two_dimensional_unresolved_parameter_area": "0",
        "physical_target_transition_joint_vertices": 0,
        "eight_chart_seam_ownership": "CERTIFIED",
    }.items():
        if claims.get(key) != expected:
            errors.append(f"dependency claim mismatch: {key}")

    candidates = result.get("candidate_transition_registry", {})
    for key, expected in {
        "active_global_signed_sheet_count": 128,
        "source_target_pair_count": 64,
        "candidate_curve_count": 328,
        "candidate_curve_rows_sha256": "f095027df9b8a9b92f80b07377b60f8322368af3ab41a1740be7b05a64e00fb1",
    }.items():
        if candidates.get(key) != expected:
            errors.append(f"candidate registry mismatch: {key}")
    if candidates.get("candidate_curve_counts_by_kind") != {
        "parameter_polarity": 24,
        "physical_earlier_occlusion_boundary": 16,
        "physical_later_miss_switch_boundary": 32,
        "source_grazing": 256,
    }:
        errors.append("candidate kind counts mismatch")

    separation = result.get("pairwise_curve_separation", {})
    for key, expected in {
        "same_sheet_candidate_pair_count": 320,
        "full_window_strict_pair_count": 304,
        "pairs_requiring_subdivision": 16,
        "maximum_separation_depth": 1,
        "strict_separation_leaf_count": 336,
        "separation_rows_sha256": "a31f2207c317ecb24d9f02222883993c4763c660b5fc7e4d4e05bafaca357803",
    }.items():
        if separation.get(key) != expected:
            errors.append(f"separation mismatch: {key}")
    for key in (
        "all_candidate_curves_pairwise_disjoint",
        "cyclic_order_constant_on_full_parameter_window",
    ):
        if separation.get(key) is not True:
            errors.append(f"missing separation flag: {key}")

    boundaries = result.get("state_changing_boundary_registry", {})
    for key, expected in {
        "state_changing_boundary_count": 88,
        "physical_row_endpoint_incidence_count": 128,
        "candidate_open_arc_count": 328,
        "cyclic_order_rows_sha256": "484f5ececb052909404eed5ae3584b32b73aa3cfb4999440fd5e6132f147ddcb",
        "open_arc_state_rows_sha256": "b986252cd639b3ec16f6f902ce4f8c0b428560ef843e4fd5c2c65ca0b57d8145",
        "state_changing_boundary_rows_sha256": "4a2f7d3ea2452d4acadc23a781eb421978d72eabede35c05112fcc27bd9d6958",
    }.items():
        if boundaries.get(key) != expected:
            errors.append(f"boundary registry mismatch: {key}")
    if boundaries.get("state_changing_counts_by_kind") != {
        "parameter_polarity": 8,
        "physical_earlier_occlusion_boundary": 16,
        "physical_later_miss_switch_boundary": 32,
        "source_grazing": 32,
    }:
        errors.append("state-changing boundary counts mismatch")

    rows = result.get("maximal_row_registry", {})
    for key, expected in {
        "maximal_connected_physical_row_count": 64,
        "unique_complete_global_physical_label_count": 64,
        "physical_row_endpoint_incidence_count": 128,
        "maximal_row_rows_sha256": "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630",
    }.items():
        if rows.get(key) != expected:
            errors.append(f"maximal row mismatch: {key}")
    if rows.get("active_sheet_count_by_physical_row_multiplicity") != {
        "0": 104,
        "1": 8,
        "2": 4,
        "3": 4,
        "4": 4,
        "5": 4,
    }:
        errors.append("active-sheet row multiplicities mismatch")
    for key in (
        "every_row_has_two_boundary_incidences",
        "every_row_is_a_connected_open_band_over_full_parameter_window",
        "every_retained_boundary_has_strict_distinct_side_states",
        "adjacent_equal_states_merged",
        "rows_are_maximal_in_exhaustive_transition_arrangement",
    ):
        if rows.get(key) is not True:
            errors.append(f"missing maximal-row flag: {key}")
    try:
        if rows["physical_row_endpoint_incidence_count"] != 2 * rows[
            "maximal_connected_physical_row_count"
        ]:
            errors.append("row endpoint incidence identity mismatch")
    except (KeyError, TypeError):
        errors.append("invalid row endpoint incidence ledger")

    symmetry = result.get("maximal_row_symmetry", {})
    for key, expected in {
        "Jx_Jy_four_row_orbit_count": 16,
        "exact_Jx_row_pair_count": 32,
        "row_orbits_sha256": "06b1151fc0634e94cb6a686218cf1b93391dad8c50e0d6a872a78c8c6ce47c22",
    }.items():
        if symmetry.get(key) != expected:
            errors.append(f"symmetry mismatch: {key}")
    for key in (
        "four_rows_per_orbit",
        "Jx_reverses_parameter_coarea_polarity",
        "Jy_preserves_parameter_coarea_polarity",
    ):
        if symmetry.get(key) is not True:
            errors.append(f"missing symmetry flag: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "all_active_transition_curves_enumerated",
        "all_candidate_curves_pairwise_disjoint_on_each_sheet",
        "all_open_bands_have_strict_constant_physical_state",
        "chart_seams_quotiented_in_global_normal_circle",
        "maximal_connected_event_rows",
        "complete_hit_miss_polarity_labels",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "global_coarea_current_assembled",
        "arbitrary_test_distributional_quotient",
        "global_scalar_matching",
        "gate3_certified",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("maximal_connected_event_rows") != "CERTIFIED":
        errors.append("maximal row verdict mismatch")
    if verdict.get("global_chart_quotiented_row_registry") != "CERTIFIED":
        errors.append("global row registry verdict mismatch")
    if verdict.get("global_coarea_DQ") != "NOT_CERTIFIED":
        errors.append("global DQ verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_maximal_global_row_registry_cert as cert
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
        print("GATE3_MAXIMAL_GLOBAL_ROW_REGISTRY_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["maximal_row_registry"][
            "maximal_connected_physical_row_count"
        ] = 52
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (row-count tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["global_coarea_current_assembled"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported current completion accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  maximal-row count tamper rejected")
        print("  unsupported current completion rejected")
        return 0
    print("GATE3_MAXIMAL_CONNECTED_EVENT_ROWS: CERTIFIED")
    print("GATE3_GLOBAL_CHART_QUOTIENTED_ROW_REGISTRY: CERTIFIED")
    if args.integrity_only:
        print("GATE3_MAXIMAL_GLOBAL_ROW_REGISTRY_INTEGRITY: PASS")
        return 0
    print("GATE3_GLOBAL_COAREA_DQ: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
