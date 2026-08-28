#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 global physical bulk atlas."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.global-physical-subrow-atlas.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-global-physical-subrow-atlas-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate3_global_physical_subrow_atlas_cert.py"


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
        "leaf_count": 200464,
        "physical_immutable_box_count": 11900,
        "physical_complete_label_count": 60,
        "certified_physical_parameter_area": "1127/6400",
        "certified_empty_parameter_area": "339463/102400",
        "unresolved_parameter_area": "35721/102400",
        "unresolved_area_fraction": "11907/131072",
        "total_parameter_area": "96/25",
    }
    for key, expected in exact.items():
        if result.get(key) != expected:
            errors.append(f"result mismatch: {key}")
    try:
        total = Fraction(result["total_parameter_area"])
        resolved = (
            Fraction(result["certified_physical_parameter_area"])
            + Fraction(result["certified_empty_parameter_area"])
            + Fraction(result["unresolved_parameter_area"])
        )
        if total != resolved:
            errors.append("parameter-area partition mismatch")
    except (KeyError, ValueError, ZeroDivisionError):
        errors.append("invalid parameter areas")

    components = result.get("connected_component_atlas", {})
    for key, expected in {
        "certified_connected_subrow_components": 60,
        "component_label_count": 60,
        "largest_component_box_count": 388,
    }.items():
        if components.get(key) != expected:
            errors.append(f"component atlas mismatch: {key}")
    symmetry = result.get("certified_bulk_symmetry_matching", {})
    for key, expected in {
        "Jx_Jy_label_orbit_count": 15,
        "four_labels_per_orbit": True,
        "box_count_and_parameter_area_equal_within_each_orbit": True,
        "Jx_reverses_parameter_coarea_polarity": True,
        "Jy_preserves_parameter_coarea_polarity": True,
        "paired_bulk_polarity_weighted_parameter_area": "0",
    }.items():
        if symmetry.get(key) != expected:
            errors.append(f"bulk symmetry mismatch: {key}")
    limits = result.get("scope_limits", {})
    for key in (
        "components_maximal_across_unresolved_collars",
        "components_quotiented_across_chart_seams",
        "global_dq",
        "global_scalar_matching",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    for key in (
        "boxes_are_compact_connected_immutable_physical_subrows",
        "same_label_shared_edge_unions_are_connected",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing positive flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("bulk_immutable_subrow_atlas") != "CERTIFIED":
        errors.append("bulk atlas verdict mismatch")
    if verdict.get("bulk_Jx_Jy_parameter_matching") != "CERTIFIED":
        errors.append("bulk symmetry verdict mismatch")
    if verdict.get("maximal_connected_event_rows") != "NOT_CERTIFIED":
        errors.append("maximal-row verdict must fail-close")
    if verdict.get("global_DQ_and_scalar_matching") != "NOT_CERTIFIED":
        errors.append("global-DQ verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_global_physical_subrow_atlas_cert as cert
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
        print("GATE3_GLOBAL_BULK_ATLAS_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["physical_immutable_box_count"] += 1
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (box-count tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["global_dq"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported global DQ accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  box-count tamper rejected")
        print("  unsupported global DQ rejected")
        return 0
    print("GATE3_GLOBAL_BULK_PHYSICAL_SUBROW_ATLAS: CERTIFIED")
    print("GATE3_BULK_JX_JY_PARAMETER_MATCHING: CERTIFIED")
    if args.integrity_only:
        print("GATE3_GLOBAL_BULK_ATLAS_INTEGRITY: PASS")
        return 0
    print("GATE3_MAXIMAL_ROWS_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
