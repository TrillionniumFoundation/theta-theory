#!/usr/bin/env python3
"""Fail-closed verifier for the all-row oriented slope envelope."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.all-row-oriented-slope-envelope.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
)
CERTIFICATE = HERE / "cm2_gate45_all_row_oriented_slope_envelope_cert.py"


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
    if result.get("schema") != "cm2.gate45.all-row-oriented-slope-envelope.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "controlled_interval_algebra_manifest": (
            "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
        ),
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    separation = result.get("global_disk_separation", {})
    for key, expected in {
        "same_G_squared_separation_margin": "301/625",
        "same_W_squared_separation_margin": "561/625",
        "cross_colour_squared_separation_margin": "36337/160000",
        "global_squared_separation_margin": "36337/160000",
        "physical_center_distance_plus_radius_sum_strict_upper": "5",
        "tangent_to_miss_boundary_gap_strict_lower": "36337/800000",
    }.items():
        if separation.get(key) != expected:
            errors.append(f"separation mismatch: {key}")

    bounds = result.get("exact_oriented_slope_bounds", {})
    for key, expected in {
        "curvature_min": "25/9",
        "curvature_max": "25/4",
        "source_absolute_slope_strict_upper": "65/4",
        "miss_image_slope_strict_upper": "4108425/145348",
        "common_broad_oriented_slope_envelope": "29",
        "source_slope_interval": "(-65/4,-25/9)",
        "miss_image_slope_interval": "(25/9,4108425/145348)",
    }.items():
        if bounds.get(key) != expected:
            errors.append(f"slope bound mismatch: {key}")
    for key in ("stable_source_orientation", "unstable_miss_image_orientation"):
        if bounds.get(key) is not True:
            errors.append(f"missing slope orientation flag: {key}")
    try:
        if Fraction(bounds["source_absolute_slope_strict_upper"]) >= 29:
            errors.append("source slope exceeds common envelope")
        if Fraction(bounds["miss_image_slope_strict_upper"]) >= 29:
            errors.append("miss slope exceeds common envelope")
    except (KeyError, TypeError, ValueError):
        errors.append("invalid slope arithmetic")

    audit = result.get("all_maximal_row_slope_audit", {})
    for key, expected in {
        "maximal_row_count": 64,
        "all_raw_slopes_strictly_bounded_by": "29",
        "source_miss_obstacle_pair_counts": {
            "G->G": 36,
            "G->W": 8,
            "W->G": 8,
            "W->W": 12,
        },
        "row_slope_contracts_sha256": (
            "8cbe95f3b1b0548ebaaf17d32db1f977b2175b526f970ec999b73a3c4b5dda0d"
        ),
    }.items():
        if audit.get(key) != expected:
            errors.append(f"all-row slope audit mismatch: {key}")
    for key in (
        "all_source_carriers_stable_oriented",
        "all_miss_image_carriers_unstable_oriented",
    ):
        if audit.get(key) is not True:
            errors.append(f"missing all-row orientation flag: {key}")

    charge = result.get("slope_only_single_charge", {})
    for key, expected in {
        "slope_only_occurrence_envelope": "q_e^slope=29*m_e",
        "global_slope_charge_mass_upper_before_Z_N_inverse": "233856/5",
        "global_slope_weighted_current_TV_upper_before_Z_N_inverse": "467712/5",
        "one_slope_charge_per_occurrence": True,
        "slope_only_charge_is_not_final_q": True,
    }.items():
        if charge.get(key) != expected:
            errors.append(f"slope charge mismatch: {key}")

    boundary = result.get("remaining_cost_boundary", {})
    if boundary.get("broad_orientation_is_not_invariant_standard_cone_typing") is not True:
        errors.append("broad-cone limitation missing")
    if boundary.get("numeric_C_fw_C_rev_complete") is not False:
        errors.append("complete C_fw/C_rev must remain false")
    if boundary.get("controlled_stopped_recovery") is not False:
        errors.append("controlled recovery must remain false")
    missing = boundary.get("still_missing_numeric_costs")
    if not isinstance(missing, list) or len(missing) != 5:
        errors.append("remaining cost ledger mismatch")

    limits = result.get("scope_limits", {})
    for key in (
        "all_row_source_stable_orientation",
        "all_row_miss_image_unstable_orientation",
        "global_numeric_broad_slope_envelope",
        "one_numeric_slope_only_charge_per_occurrence",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "proper_standard_family_cone_typing",
        "complete_numeric_C_fw_C_rev",
        "controlled_stopped_recovery",
        "CM2_norm_lifts",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("all_row_oriented_slope_envelope_lt_29") != "CERTIFIED":
        errors.append("slope envelope verdict mismatch")
    if verdict.get("slope_only_single_charge_q_29m") != "CERTIFIED":
        errors.append("slope charge verdict mismatch")
    if verdict.get("complete_C_fw_C_rev_and_recovery") != "NOT_CERTIFIED":
        errors.append("complete cost/recovery verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_all_row_oriented_slope_envelope_cert as cert
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
        print("GATE45_ALL_ROW_SLOPE_ENVELOPE_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["exact_oriented_slope_bounds"][
            "common_broad_oriented_slope_envelope"
        ] = "1"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (slope envelope tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"]["complete_numeric_C_fw_C_rev"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported complete costs accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  slope-envelope tamper rejected")
        print("  unsupported complete C_fw/C_rev rejected")
        return 0
    print("GATE45_ALL_ROW_ORIENTED_SLOPE_ENVELOPE_LT_29: CERTIFIED")
    print("GATE45_SLOPE_ONLY_SINGLE_CHARGE_q_29m: CERTIFIED")
    if args.integrity_only:
        print("GATE45_ALL_ROW_SLOPE_ENVELOPE_INTEGRITY: PASS")
        return 0
    print("GATE45_COMPLETE_C_FW_C_REV_AND_RECOVERY: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
