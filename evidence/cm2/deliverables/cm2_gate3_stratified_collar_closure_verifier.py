#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 stratified collar certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.stratified-collar-closure.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-stratified-collar-closure-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate3_stratified_collar_closure_cert.py"


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
        "precision_bits": 192,
        "predecessor_unresolved_parameter_area": "5263/51200",
        "residual_first_or_miss_parameter_area": "18081/1638400",
        "residual_fraction_of_full_parameter_domain": "6027/2097152",
        "reduction_from_predecessor_unresolved_area": "30067/327680",
        "fraction_of_predecessor_unresolved_area_removed": "150335/168416",
    }
    for key, expected in exact.items():
        if result.get(key) != expected:
            errors.append(f"result mismatch: {key}")

    try:
        predecessor = Fraction(result["predecessor_unresolved_parameter_area"])
        residual = Fraction(result["residual_first_or_miss_parameter_area"])
        if not residual < predecessor:
            errors.append("residual area did not strictly decrease")
        if predecessor - residual != Fraction(
            result["reduction_from_predecessor_unresolved_area"]
        ):
            errors.append("reduction identity mismatch")
        if residual / Fraction(96, 25) != Fraction(
            result["residual_fraction_of_full_parameter_domain"]
        ):
            errors.append("full-domain residual fraction mismatch")
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        errors.append("invalid top-level exact-area ledger")

    separation = result.get("source_target_separation", {})
    for key, expected in {
        "source_target_pair_count": 64,
        "minimum_squared_circle_separation_margin": "36337/160000",
        "minimum_squared_angular_derivative_on_cp_zero": "36337/160000",
        "minimum_squared_z_derivative_on_cp_zero": "36337/320000",
        "registry_sha256": "e1503dbe5acd821be39883d7cf9c10029078df968e308613a9696863b033e723",
    }.items():
        if separation.get(key) != expected:
            errors.append(f"source-target separation mismatch: {key}")

    source_grazing = result.get("source_grazing_endpoint_stratification", {})
    for key, expected in {
        "endpoint_box_count": 23376,
        "ambient_endpoint_collar_area": "1461/25600",
        "predecessor_face-certified_normal_form_boxes": 16304,
        "physical_outgoing_half_label_count": 32,
        "rows_sha256": "e185ee0978c231a1b6f62cd8d4af9b96a4a34cc2c53f5e71b6535f9224beec6e",
    }.items():
        if source_grazing.get(key) != expected:
            errors.append(f"source-grazing ledger mismatch: {key}")
    if source_grazing.get("stratification_counts") != {
        "physical_outgoing_half": 4396,
        "uniformly_occluded": 18980,
    }:
        errors.append("source-grazing count mismatch")
    try:
        source_areas = source_grazing["stratification_ambient_box_areas"]
        if sum(map(Fraction, source_areas.values())) != Fraction(1461, 25600):
            errors.append("source-grazing area partition mismatch")
    except (KeyError, TypeError, ValueError):
        errors.append("invalid source-grazing area partition")
    boundary = source_grazing.get("boundary", {})
    if boundary.get("globally_regular_on_every_active_source-target sheet") is not True:
        errors.append("source-grazing regularity flag missing")
    if boundary.get("two_dimensional_parameter_measure") != "0":
        errors.append("source-grazing boundary measure mismatch")
    if boundary.get("signed_parameter_coarea_coefficient_on_boundary") != "0":
        errors.append("source-grazing boundary coarea mismatch")

    polarity = result.get("initial_parameter_polarity_stratification", {})
    for key, expected in {
        "box_count": 816,
        "ambient_box_area": "51/25600",
        "base_event_label_count": 8,
        "open_sign_strata_count_with_multiplicity": 1632,
        "rows_sha256": "a241a9aad27fda736c760b5eb30c2d5384dadbed97103c3d963658a890ab149f",
    }.items():
        if polarity.get(key) != expected:
            errors.append(f"initial polarity ledger mismatch: {key}")
    for key in (
        "all_boxes_have_strict_first_visibility_and_miss_owner",
        "all_uy_functions_have_pointwise_nonidentity_witness",
    ):
        if polarity.get(key) is not True:
            errors.append(f"initial polarity proof flag missing: {key}")

    deep = result.get("depth_thirteen_remaining_refinement", {})
    for key, expected in {
        "initial_depth_nine_first_or_miss_box_count": 17912,
        "initial_depth_nine_first_or_miss_area": "2239/51200",
        "maximum_refinement_depth": 13,
        "final_leaf_count": 127916,
        "residual_first_visibility_area": "413/204800",
        "residual_miss_owner_area": "14777/1638400",
        "residual_first_or_miss_area": "18081/1638400",
        "rows_sha256": "3b5dc2bb1a2f4db0a6086675479dcc9bad9cfaee9c12586127dbf9783a54cc46",
    }.items():
        if deep.get(key) != expected:
            errors.append(f"deep-refinement mismatch: {key}")
    try:
        areas = deep["classification_ambient_areas"]
        if sum(map(Fraction, areas.values())) != Fraction(2239, 51200):
            errors.append("deep-refinement area partition mismatch")
        if Fraction(areas[FIRST_KIND]) + Fraction(areas[MISS_KIND]) != Fraction(
            deep["residual_first_or_miss_area"]
        ):
            errors.append("deep residual identity mismatch")
    except (KeyError, TypeError, ValueError):
        errors.append("invalid deep-refinement exact-area ledger")

    limits = result.get("scope_limits", {})
    for key in (
        "all_parameter_polarity_boxes_sign_stratified",
        "all_source_grazing_endpoint_boxes_stratified",
        "source_grazing_and_polarity_boundaries_are_measure_zero",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "remaining_first_visibility_and_miss_owner_collars_closed",
        "maximal_connected_event_rows",
        "chart_seams_quotiented",
        "global_dq",
        "global_scalar_matching",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("source_grazing_endpoint_stratification") != "CERTIFIED":
        errors.append("source-grazing verdict mismatch")
    if verdict.get("parameter_polarity_stratification") != "CERTIFIED":
        errors.append("polarity verdict mismatch")
    if verdict.get("first_visibility_and_miss_owner_closure") != "NOT_CERTIFIED":
        errors.append("first/miss verdict must fail-close")
    if verdict.get("global_DQ_and_scalar_matching") != "NOT_CERTIFIED":
        errors.append("global-DQ verdict must fail-close")
    return errors


FIRST_KIND = "unresolved_first_visibility"
MISS_KIND = "unresolved_miss_owner"


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_stratified_collar_closure_cert as cert
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
        print("GATE3_STRATIFIED_COLLAR_CLOSURE_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["residual_first_or_miss_parameter_area"] = "0"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (residual-area tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["global_dq"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported global DQ accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  residual-area tamper rejected")
        print("  unsupported global DQ rejected")
        return 0
    print("GATE3_SOURCE_GRAZING_COLLAR_STRATIFICATION: CERTIFIED")
    print("GATE3_PARAMETER_POLARITY_STRATIFICATION: CERTIFIED")
    if args.integrity_only:
        print("GATE3_STRATIFIED_COLLAR_CLOSURE_INTEGRITY: PASS")
        return 0
    print("GATE3_FIRST_VISIBILITY_MISS_OWNER_CLOSURE: NOT_CERTIFIED")
    print("GATE3_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
