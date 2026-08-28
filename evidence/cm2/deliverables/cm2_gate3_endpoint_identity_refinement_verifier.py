#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 endpoint-identity refinement."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.endpoint-identity-refinement.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-endpoint-identity-refinement-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate3_endpoint_identity_refinement_cert.py"


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
    exact = {
        "active_chart_signed_sheets": 384,
        "leaf_count": 80084,
        "physical_immutable_box_count": 11812,
        "physical_complete_label_count": 64,
        "certified_physical_parameter_area": "5569/25600",
        "certified_empty_parameter_area": "180207/51200",
        "unresolved_parameter_area": "5263/51200",
        "unresolved_area_fraction": "5263/196608",
        "total_parameter_area": "96/25",
        "predecessor_unresolved_parameter_area": "35721/102400",
        "predecessor_endpoint_collar_area": "15573/51200",
        "genuine_endpoint_collar_area": "1461/25600",
        "endpoint_collar_area_removed_by_identity": "12651/51200",
        "endpoint_collar_removed_fraction": "4217/5191",
    }
    for key, expected in exact.items():
        if result.get(key) != expected:
            errors.append(f"result mismatch: {key}")
    try:
        total = Fraction(result["total_parameter_area"])
        partition = (
            Fraction(result["certified_physical_parameter_area"])
            + Fraction(result["certified_empty_parameter_area"])
            + Fraction(result["unresolved_parameter_area"])
        )
        if total != partition:
            errors.append("parameter-area partition mismatch")
        if not (
            Fraction(result["unresolved_parameter_area"])
            < Fraction(result["predecessor_unresolved_parameter_area"])
        ):
            errors.append("unresolved area did not strictly decrease")
        normal = result.get("source_grazing_normal_form_atlas", {})
        if (
            Fraction(normal["transverse_graph_parameter_area"])
            + Fraction(normal["remaining_endpoint_edge_or_degeneracy_area"])
            != Fraction(result["genuine_endpoint_collar_area"])
        ):
            errors.append("source-grazing normal-form area mismatch")
    except (KeyError, ValueError, ZeroDivisionError, TypeError):
        errors.append("invalid exact area ledger")

    identities = result.get("exact_identity", {})
    for key in (
        "tangent_direction_unit",
        "source_normal_tangent_frame_orthonormal",
        "cp_squared_plus_p_squared_equals_one",
        "cp_positive_implies_source_coordinate_strictly_interior",
        "strict_tangent_radicand_implies_target_flight_positive",
        "coarea_sign_equals_sign_eta_epsilon_u_y_on_outgoing_rows",
    ):
        if identities.get(key) is not True:
            errors.append(f"missing exact identity: {key}")

    normal = result.get("source_grazing_normal_form_atlas", {})
    for key, expected in {
        "endpoint_leaf_count": 23376,
        "transverse_graph_box_count": 16304,
        "transverse_graph_parameter_area": "1019/25600",
        "remaining_endpoint_edge_or_degeneracy_area": "221/12800",
    }.items():
        if normal.get(key) != expected:
            errors.append(f"normal-form atlas mismatch: {key}")
    if normal.get("transverse_graph_axis_counts") != {"z_as_function_of_s": 16304}:
        errors.append("normal-form graph-axis ledger mismatch")

    components = result.get("connected_component_atlas", {})
    for key, expected in {
        "certified_connected_subrow_components": 64,
        "component_label_count": 64,
        "largest_component_box_count": 303,
    }.items():
        if components.get(key) != expected:
            errors.append(f"component atlas mismatch: {key}")
    symmetry = result.get("certified_bulk_symmetry_matching", {})
    if symmetry.get("Jx_Jy_label_orbit_count") != 16:
        errors.append("bulk symmetry orbit count mismatch")
    if symmetry.get("paired_bulk_polarity_weighted_parameter_area") != "0":
        errors.append("bulk symmetry area mismatch")

    limits = result.get("scope_limits", {})
    for key in (
        "components_maximal_across_remaining_collars",
        "components_quotiented_across_chart_seams",
        "global_dq",
        "global_scalar_matching",
        "remaining_source_grazing_edge_or_degeneracy_boxes_resolved",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    for key in (
        "redundant_source_coordinate_and_positive_flight_collars_removed",
        "coarea_product_dependency_collar_reduced_by_exact_sign_factor",
        "all_remaining_endpoint_collars_are_source_grazing_not_tau3",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing positive scope flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("endpoint_identity_refinement") != "CERTIFIED":
        errors.append("endpoint refinement verdict mismatch")
    if verdict.get("source_grazing_transverse_normal_form_subatlas") != "CERTIFIED":
        errors.append("normal-form subatlas verdict mismatch")
    if verdict.get("maximal_connected_event_rows") != "NOT_CERTIFIED":
        errors.append("maximal-row verdict must fail-close")
    if verdict.get("global_DQ_and_scalar_matching") != "NOT_CERTIFIED":
        errors.append("global-DQ verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_endpoint_identity_refinement_cert as cert
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
        print("GATE3_ENDPOINT_IDENTITY_REFINEMENT_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["unresolved_parameter_area"] = "0"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unresolved-area tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["global_dq"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported global DQ accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  unresolved-area tamper rejected")
        print("  unsupported global DQ rejected")
        return 0
    print("GATE3_ENDPOINT_IDENTITY_REFINEMENT: CERTIFIED")
    print("GATE3_SOURCE_GRAZING_TRANSVERSE_NORMAL_FORM_SUBATLAS: CERTIFIED")
    if args.integrity_only:
        print("GATE3_ENDPOINT_IDENTITY_REFINEMENT_INTEGRITY: PASS")
        return 0
    print("GATE3_MAXIMAL_ROWS_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
