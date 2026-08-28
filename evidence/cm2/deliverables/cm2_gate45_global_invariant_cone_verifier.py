#!/usr/bin/env python3
"""Fail-closed verifier for the global invariant geometric cone."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate45.global-invariant-cone.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate45_global_invariant_cone_cert.py"


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
    if result.get("schema") != "cm2.gate45.global-invariant-cone.v1":
        errors.append("result schema mismatch")
    provenance = result.get("provenance", {})
    for key, expected in {
        "all_row_slope_manifest": (
            "cm2-gate45-all-row-oriented-slope-envelope-manifest-2026-07-15.json"
        ),
        "bidirectional_boundary_Z_manifest": (
            "cm2-gate45-bidirectional-boundary-z-cost-manifest-2026-07-16.json"
        ),
        "corrected_current_rows_sha256": (
            "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
        ),
    }.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    cone = result.get("global_invariant_geometric_cone", {})
    for key, expected in {
        "fixed_geometric_unstable_cone": (
            "25/9<V=dphi/dr<4108425/145348<29"
        ),
        "curvature_lower": "25/9",
        "curvature_upper": "25/4",
        "global_free_flight_strict_lower": "36337/800000",
        "cone_upper": "4108425/145348",
        "wavefront_recurrence": (
            "V_1=kappa_1+cp_1/(tau+cp_0/(V_0+kappa_0))"
        ),
        "recurrence_matches_frozen_birkhoff_matrix": True,
        "positive_denominator_for_every_input_in_cone": True,
        "strict_forward_invariance": True,
        "source_reversal_slope": "V_rev=kappa_source+cp_source/ell_T",
        "source_reversal_strict_upper": "65/4",
        "miss_image_slope": (
            "V_fw=kappa_miss+cp_miss/(t_miss-ell_T)"
        ),
        "both_orientations_enter_cone_at_time_zero": True,
    }.items():
        if cone.get(key) != expected:
            errors.append(f"invariant-cone mismatch: {key}")

    audit = result.get("all_row_bidirectional_cone_typing", {})
    for key, expected in {
        "maximal_occurrence_count": 64,
        "source_reverse_carriers_in_fixed_unstable_cone": 64,
        "miss_forward_carriers_in_fixed_unstable_cone": 64,
        "zero_step_reverse_cone_entries": 64,
        "zero_step_forward_cone_entries": 64,
        "all_row_cone_typing_rows_sha256": (
            "0b30335b30b6d3b69c6d754e8d257bb585935d157dd26c593d5451085b029dc1"
        ),
        "maximal_row_registry_sha256": (
            "0857fdfde5845026f47d1b9a343eaf06fd873782efcf2359618fe9d4f46fe630"
        ),
    }.items():
        if audit.get(key) != expected:
            errors.append(f"row cone audit mismatch: {key}")

    limits = result.get("scope_limits", {})
    for key in (
        "fixed_global_geometric_unstable_cone",
        "all_source_reverse_carriers_cone_typed",
        "all_miss_forward_carriers_cone_typed",
        "both_oriented_cone_entry_times_zero",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "proper_family_C2_curvature_bound",
        "proper_family_log_density_bound",
        "proper_family_minimum_length_or_recovery",
        "complete_numeric_C_fw_C_rev",
        "controlled_stopped_parent_recovery",
        "full_dynamic_MT_DQ",
        "CM2_norm_lifts",
        "gate3_certified",
        "gate4_certified",
        "gate5_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    if result.get("internal_replay_digest") != (
        "0b30335b30b6d3b69c6d754e8d257bb585935d157dd26c593d5451085b029dc1"
    ):
        errors.append("internal replay digest mismatch")

    verdict = data.get("verdict", {})
    if verdict.get("global_invariant_geometric_unstable_cone") != "CERTIFIED":
        errors.append("global cone verdict mismatch")
    if verdict.get("all_row_bidirectional_zero_step_cone_typing") != "CERTIFIED":
        errors.append("all-row cone typing verdict mismatch")
    if verdict.get("complete_proper_family_costs_and_recovery") != "NOT_CERTIFIED":
        errors.append("complete proper-family verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate45_global_invariant_cone_cert as cert
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
        print("GATE45_GLOBAL_INVARIANT_CONE_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["result"]["global_invariant_geometric_cone"][
            "wavefront_recurrence"
        ] = "V_1=0"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (recurrence tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["scope_limits"][
            "complete_numeric_C_fw_C_rev"
        ] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported complete costs accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  recurrence-sign tamper rejected")
        print("  unsupported complete C_fw/C_rev rejected")
        return 0
    print("GATE45_GLOBAL_INVARIANT_GEOMETRIC_UNSTABLE_CONE: CERTIFIED")
    print("GATE45_ALL_ROW_BIDIRECTIONAL_ZERO_STEP_CONE_TYPING: CERTIFIED")
    if args.integrity_only:
        print("GATE45_GLOBAL_INVARIANT_CONE_INTEGRITY: PASS")
        return 0
    print("GATE45_COMPLETE_PROPER_FAMILY_COSTS_AND_RECOVERY: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
