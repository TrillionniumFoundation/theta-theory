#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 chart-seam quotient."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.chart-seam-quotient.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
CERTIFICATE = HERE / "cm2_gate3_chart_seam_quotient_cert.py"


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
    owner = result.get("unique_half_open_owner_rule", {})
    for key, expected in {
        "source_obstacle_count": 2,
        "diagonal_seams_per_source": 4,
        "total_chart_seams": 8,
        "diagonal_tie": "E or W owns; N or S excludes",
        "seam_geometry_rows_sha256": "53d991784439d87363b06df11315cbe5be50c701c3a232fcece9781fd3400e10",
    }.items():
        if owner.get(key) != expected:
            errors.append(f"seam-owner mismatch: {key}")
    for key in (
        "same_physical_normal_on_paired_representations",
        "same_absolute_chart_jacobian_on_paired_representations",
        "duplicate_trace_is_identified_not_added",
    ):
        if owner.get(key) is not True:
            errors.append(f"missing seam identity: {key}")

    bulk = result.get("rectangular_bulk_quotient", {})
    for key, expected in {
        "physical_rectangular_bulk_box_count": 11812,
        "bulk_boxes_touching_chart_seams": 344,
        "complete_physical_seam_label_keys": 16,
        "two_chart_duplicate_seam_keys": 12,
        "one_chart_owner_only_seam_keys": 4,
        "positive_s_overlap_pairs_identified": 96,
        "prequotient_connected_component_count": 64,
        "postquotient_connected_component_count": 52,
        "component_count_reduction": 12,
        "two_chart_seam_rows_sha256": "9290d7a2aa9335ced284833e374e51723c946349a491b20f28463ae06a0ffde2",
        "one_chart_seam_rows_sha256": "257579ba87f94fb0d710a0ab86f35ff509d7f44064f32a7a367106b1932eebc8",
        "quotient_component_rows_sha256": "26601a187421ca5cb939678203f286b9e82f517eb44dbea4ef62226ae9d908b3",
    }.items():
        if bulk.get(key) != expected:
            errors.append(f"bulk seam quotient mismatch: {key}")
    try:
        if bulk["prequotient_connected_component_count"] - bulk[
            "postquotient_connected_component_count"
        ] != bulk["component_count_reduction"]:
            errors.append("component reduction identity mismatch")
    except (KeyError, TypeError):
        errors.append("invalid component reduction ledger")

    limits = result.get("scope_limits", {})
    for key in (
        "all_eight_chart_seams_have_unique_owner",
        "coordinate_duplicate_traces_removed_by_exact_identity",
        "rectangular_bulk_components_quotiented_across_seams",
        "ownership_rule_applies_to_analytic_strata",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "full_stratified_maximal_component_registry",
        "global_coarea_current_assembled",
        "global_dq",
        "global_scalar_matching",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("eight_chart_seam_ownership") != "CERTIFIED":
        errors.append("seam ownership verdict mismatch")
    if verdict.get("rectangular_bulk_seam_quotient") != "CERTIFIED":
        errors.append("bulk seam quotient verdict mismatch")
    if verdict.get("full_maximal_rows_global_DQ") != "NOT_CERTIFIED":
        errors.append("global verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_chart_seam_quotient_cert as cert
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
        print("GATE3_CHART_SEAM_QUOTIENT_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["rectangular_bulk_quotient"]["postquotient_connected_component_count"] = 64
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (component tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["global_dq"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported global DQ accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  component tamper rejected")
        print("  unsupported global DQ rejected")
        return 0
    print("GATE3_EIGHT_CHART_SEAM_OWNERSHIP: CERTIFIED")
    print("GATE3_RECTANGULAR_BULK_SEAM_QUOTIENT: CERTIFIED")
    if args.integrity_only:
        print("GATE3_CHART_SEAM_QUOTIENT_INTEGRITY: PASS")
        return 0
    print("GATE3_FULL_MAXIMAL_ROWS_GLOBAL_DQ: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
