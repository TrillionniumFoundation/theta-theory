#!/usr/bin/env python3
"""Fail-closed verifier for the corrected Gate-3 local component orbit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.component-orbit-dedup.v1"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_MANIFEST = HERE / "cm2-gate3-component-orbit-dedup-manifest-2026-07-15.json"
OPEN_GLOBAL = (
    "all_288_sheet_connected_components",
    "global_duplicate_endpoint_quotient",
    "global_immutable_physical_event_rows",
    "global_dq",
    "global_scalar_matching",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_provenance(data: dict[str, Any], errors: list[str]) -> None:
    rows = data.get("provenance")
    if not isinstance(rows, list) or not rows:
        errors.append("provenance missing")
        return
    for row in rows:
        relative = row.get("path") if isinstance(row, dict) else None
        expected = row.get("sha256") if isinstance(row, dict) else None
        path = ROOT / relative if isinstance(relative, str) else None
        if path is None or not path.is_file():
            errors.append(f"missing provenance: {relative!r}")
        elif digest(path) != expected:
            errors.append(f"provenance mismatch: {relative}")


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    check_provenance(data, errors)

    resolution = data.get("full_320_descriptor_resolution", {})
    if resolution != {
        "status": "CERTIFIED_PHYSICALLY_EMPTY",
        "descriptor_count": 320,
        "empty": 320,
        "physical": 0,
        "unresolved": 0,
    }:
        errors.append("full 320-descriptor resolution mismatch")

    audit = data.get("corrected_forward_time_audit", {})
    for key, expected in {
        "replayed_retracted_seed_count": 16,
        "uniform_forward_target_count": 16,
        "uniform_other_behind_source_count": 16,
        "physical_forward_joint_vertex_count": 0,
        "classification": "NONPHYSICAL_OTHER_CONTACT_BEHIND_SOURCE",
    }.items():
        if audit.get(key) != expected:
            errors.append(f"forward-time audit mismatch: {key}")
    if not isinstance(audit.get("rows_sha256"), str) or len(audit["rows_sha256"]) != 64:
        errors.append("invalid forward-time rows digest")

    orbit = data.get("certified_immutable_local_orbit", {})
    expected_orbit = {
        "row_count": 4,
        "full_parameter_window_on_every_row": True,
        "constant_miss_trace_on_every_row": True,
        "constant_nonzero_parameter_coarea_polarity_on_every_row": True,
        "polarity_pattern": [1,-1,1,-1],
        "symmetry_invariant_scalar_current_cancels_pairwise": True,
        "arbitrary_test_distributional_cancellation": False,
        "maximal_connected_sheet_components": False,
    }
    for key, expected in expected_orbit.items():
        if orbit.get(key) != expected:
            errors.append(f"local orbit mismatch: {key}")
    rows = orbit.get("rows")
    if not isinstance(rows, list) or len(rows) != 4:
        errors.append("local orbit row registry mismatch")
    else:
        expected_labels = (
            ("id","G:E","W[0,0]",1,"G[1,1]",1),
            ("Jx","G:W","W[-1,0]",-1,"G[-1,1]",-1),
            ("Jy","G:E","W[0,-1]",-1,"G[1,-1]",1),
            ("JxJy","G:W","W[-1,-1]",1,"G[-1,-1]",-1),
        )
        for row, expected in zip(rows, expected_labels):
            actual = (
                row.get("symmetry"),row.get("chart"),row.get("target"),
                row.get("epsilon"),row.get("miss"),row.get("polarity"),
            )
            if actual != expected:
                errors.append(f"local orbit label mismatch: {actual}")

    reduction = data.get("global_finite_reduction", {})
    for key, expected in {
        "global_signed_sheets": 288,
        "parameter_active_cross_color_sheets": 128,
        "inactive_same_color_sheets": 160,
        "active_Jx_Jy_orbits": 32,
        "raw_active_endpoint_descriptors": 36992,
    }.items():
        if reduction.get(key) != expected:
            errors.append(f"global reduction mismatch: {key}")
    breakdown = reduction.get("raw_active_endpoint_breakdown", {})
    expected_breakdown = {
        "target_target": 36352,
        "source_grazing": 256,
        "parameter_boundary": 256,
        "polarity_split": 128,
    }
    if breakdown != expected_breakdown or sum(breakdown.values()) != 36992:
        errors.append("active endpoint breakdown mismatch")

    completion = data.get("global_completion", {})
    for key in (
        "sixteen_nonforward_vertex_claims_retracted_and_replayed",
        "one_complete_Jx_Jy_immutable_subrow_orbit",
    ):
        if completion.get(key) is not True:
            errors.append(f"positive completion flag missing: {key}")
    for key in OPEN_GLOBAL:
        if completion.get(key) is not None:
            errors.append(f"global claim must remain fail-closed: {key}")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_component_orbit_dedup_cert as cert
        summary = cert.full_summary()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]
    errors: list[str] = []
    if data.get("full_320_descriptor_resolution") != summary.get(
        "full_320_descriptor_resolution"
    ):
        errors.append("full 320-descriptor replay mismatch")
    audit = summary["corrected_forward_time_audit"]
    manifest_audit = data["corrected_forward_time_audit"]
    for key in (
        "replayed_retracted_seed_count", "uniform_forward_target_count",
        "uniform_other_behind_source_count", "physical_forward_joint_vertex_count",
        "rows_sha256",
    ):
        if manifest_audit.get(key) != audit.get(key):
            errors.append(f"forward-time replay mismatch: {key}")
    orbit = summary["certified_immutable_local_orbit"]
    manifest_orbit = data["certified_immutable_local_orbit"]
    for key in (
        "row_count", "polarity_pattern", "rows_sha256",
        "constant_miss_trace_on_every_row",
        "constant_nonzero_parameter_coarea_polarity_on_every_row",
    ):
        if manifest_orbit.get(key) != orbit.get(key):
            errors.append(f"local orbit replay mismatch: {key}")
    reduction = summary["global_finite_reduction"]
    manifest_reduction = data["global_finite_reduction"]
    for key in (
        "global_signed_sheets", "parameter_active_cross_color_sheets",
        "inactive_same_color_sheets", "active_Jx_Jy_orbits",
        "active_sheet_orbits_sha256", "raw_active_endpoint_descriptors",
        "raw_active_endpoint_breakdown",
    ):
        if manifest_reduction.get(key) != reduction.get(key):
            errors.append(f"global reduction replay mismatch: {key}")
    return errors


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
        print("GATE3_COMPONENT_ORBIT_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1
    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["corrected_forward_time_audit"]["physical_forward_joint_vertex_count"] = 16
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (retracted vertex claim accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["global_completion"]["global_dq"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported global DQ accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  retracted vertex claim rejected")
        print("  unsupported global DQ claim rejected")
        return 0
    print("GATE3_RETRACTED_16_NONFORWARD_VERTEX_AUDIT: CERTIFIED")
    print("GATE3_ONE_COMPLETE_JX_JY_IMMUTABLE_SUBROW_ORBIT: CERTIFIED")
    if args.integrity_only:
        print("GATE3_COMPONENT_ORBIT_INTEGRITY: PASS")
        return 0
    print("GATE3_ALL_288_CONNECTED_EVENT_ROWS_DQ_MATCHING: NOT_CERTIFIED")
    for key in OPEN_GLOBAL:
        print(f"  missing={key}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
