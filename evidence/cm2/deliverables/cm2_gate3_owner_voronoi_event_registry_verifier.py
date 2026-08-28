#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 owner/endpoint registry."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate3.owner-voronoi-event-registry.v1"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-owner-voronoi-event-registry-manifest-2026-07-15.json"
)
OPEN_GLOBAL = (
    "duplicate_endpoint_quotient_across_distinct_descriptors",
    "connected_visible_component_registry",
    "constant_miss_trace_subrows",
    "constant_parameter_polarity_subrows",
    "immutable_global_event_rows",
    "global_dq",
    "global_scalar_matching",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_digest(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def check_provenance(data: dict[str, Any], errors: list[str]) -> None:
    rows = data.get("provenance")
    if not isinstance(rows, list) or not rows:
        errors.append("provenance missing")
        return
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"provenance[{index}] malformed")
            continue
        relative = row.get("path")
        expected = row.get("sha256")
        path = ROOT / relative if isinstance(relative, str) else None
        if path is None or not path.is_file():
            errors.append(f"provenance missing: {relative!r}")
        elif not is_digest(expected) or digest(path) != expected:
            errors.append(f"provenance hash mismatch: {relative}")


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    check_provenance(data, errors)

    scope = data.get("scope", {})
    expected_scope = {
        "parameter_window": "|s|<=1/400",
        "parent_multi_candidate_leaves": 95596,
        "global_G_candidate_union": 76,
        "global_W_candidate_union": 68,
        "global_owner_predicate_rows": 144,
        "global_signed_tangency_sheets": 288,
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"scope {key} mismatch")

    owner = data.get("owner_partition", {})
    if owner.get("status") != "CERTIFIED_FINITE_BOOLEAN_SINGLE_OWNER_PARTITION":
        errors.append("owner partition status mismatch")
    for key, expected in {
        "chart_owner_predicate_rows": 448,
        "chart_signed_tangency_sheets": 896,
    }.items():
        if owner.get(key) != expected:
            errors.append(f"owner {key} mismatch")
    for key in (
        "chart_owner_rows_sha256", "chart_sheet_rows_sha256",
        "global_owner_rows_sha256", "global_sheet_rows_sha256",
    ):
        if not is_digest(owner.get(key)):
            errors.append(f"invalid owner digest {key}")

    raw = data.get("raw_endpoint_universe", {})
    expected_raw = {
        "target_target_common_tangent_descriptors": 82048,
        "source_grazing_equations": 576,
        "raw_analytic_endpoint_descriptors": 82624,
        "parameter_boundary_sheet_rows": 576,
        "constant_polarity_split_equations": 288,
    }
    for key, expected in expected_raw.items():
        if raw.get(key) != expected:
            errors.append(f"raw endpoint {key} mismatch")
    if raw.get("target_target_common_tangent_descriptors", 0) + raw.get(
        "source_grazing_equations", 0
    ) != raw.get("raw_analytic_endpoint_descriptors"):
        errors.append("raw endpoint arithmetic mismatch")
    for key in ("target_target_descriptors_sha256", "source_grazing_equations_sha256"):
        if not is_digest(raw.get(key)):
            errors.append(f"invalid raw endpoint digest {key}")

    first = data.get("full_window_first_pass", {})
    if first.get("strictly_classified_descriptor_count") != 81760:
        errors.append("first-pass strict count mismatch")
    if first.get("initial_unresolved_descriptor_count") != 288:
        errors.append("first-pass unresolved count mismatch")
    if first.get("source_grazing_identity_boundaries") != 832:
        errors.append("source-grazing identity count mismatch")
    if first.get("strictly_classified_descriptor_count", 0) + first.get(
        "initial_unresolved_descriptor_count", 0
    ) != raw.get("target_target_common_tangent_descriptors"):
        errors.append("first-pass descriptor arithmetic mismatch")
    for key in ("classified_rows_sha256", "unresolved_descriptors_sha256"):
        if not is_digest(first.get(key)):
            errors.append(f"invalid first-pass digest {key}")

    adaptive = data.get("adaptive_endpoint_completion", {})
    expected_adaptive = {
        "adaptive_depth": 24,
        "dyadic_grid_width": "1/3355443200",
        "descriptors_fully_resolved_after_subdivision": 284,
        "regular_subinterval_leaf_count": 3328,
        "merged_transition_collar_count": 4,
        "maximum_merged_collar_width": "11/1677721600",
        "maximum_collar_grid_widths": "22",
        "transition_collar_orbits_under_Jx_Jy": 1,
        "transition_collar_orbit_size": 4,
        "exact_third_target_tangency_vertices": 0,
        "physical_transition_vertex_orbits_under_Jx_Jy": 0,
        "nonphysical_tau_three_crossing_collars": 4,
        "nonphysical_tau_three_orbits_under_Jx_Jy": 1,
        "all_transition_collars_exactly_typed": True,
        "numerically_unresolved_transition_collar_count": 0,
    }
    for key, expected in expected_adaptive.items():
        if adaptive.get(key) != expected:
            errors.append(f"adaptive {key} mismatch")
    if adaptive.get("descriptors_fully_resolved_after_subdivision", 0) + adaptive.get(
        "merged_transition_collar_count", 0
    ) != first.get("initial_unresolved_descriptor_count"):
        errors.append("adaptive descriptor arithmetic mismatch")
    if adaptive.get("exact_third_target_tangency_vertices", 0) + adaptive.get(
        "nonphysical_tau_three_crossing_collars", 0
    ) != adaptive.get("merged_transition_collar_count"):
        errors.append("transition collar typing arithmetic mismatch")
    if adaptive.get("physical_transition_vertex_orbits_under_Jx_Jy", 0) * adaptive.get(
        "transition_collar_orbit_size", 0
    ) != adaptive.get("exact_third_target_tangency_vertices"):
        errors.append("physical transition orbit arithmetic mismatch")
    if adaptive.get("nonphysical_tau_three_orbits_under_Jx_Jy", 0) * adaptive.get(
        "transition_collar_orbit_size", 0
    ) != adaptive.get("nonphysical_tau_three_crossing_collars"):
        errors.append("nonphysical transition orbit arithmetic mismatch")
    for key in (
        "regular_subinterval_rows_sha256", "merged_transition_collars_sha256",
        "transition_collar_orbits_sha256",
    ):
        if not is_digest(adaptive.get(key)):
            errors.append(f"invalid adaptive digest {key}")

    completion = data.get("global_completion", {})
    for key in (
        "all_95596_multi_leaves_have_exact_owner_predicate_partition",
        "all_82048_target_target_descriptors_interval_typed",
        "retracted_sixteen_physical_transition_vertex_claim",
        "nonphysical_tau_three_collars_uniformly_discarded",
    ):
        if completion.get(key) is not True:
            errors.append(f"positive completion flag missing: {key}")
    if completion.get("corrected_physical_transition_vertex_count") != 0:
        errors.append("corrected physical-transition count mismatch")

    retracted = data.get("retracted_pre_forward_time_audit", {})
    if retracted.get("status") != "RETRACTED_BY_MISSING_ELL_OTHER_POSITIVITY_CHECK":
        errors.append("retracted-audit status mismatch")
    if retracted.get("old_unresolved_descriptor_count") != 320:
        errors.append("retracted-audit old count mismatch")
    if retracted.get("old_unresolved_descriptors_sha256") != (
        "c04fc55676bcb0341c24f8ae5f50116913bb9b70b18ca901873c7e1ff15238a2"
    ):
        errors.append("retracted-audit old digest mismatch")
    if retracted.get("old_claimed_third_target_vertex_count") != 16:
        errors.append("retracted-audit old vertex count mismatch")
    for key in OPEN_GLOBAL:
        if completion.get(key) is not None:
            errors.append(f"global claim must remain fail-closed: {key}")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_owner_voronoi_event_registry_cert as cert

        summary = cert.full_summary()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]

    owner = summary["owner_partition"]
    manifest_owner = data["owner_partition"]
    for manifest_key, summary_key in {
        "chart_owner_predicate_rows": "chart_owner_predicate_rows",
        "chart_owner_rows_sha256": "chart_owner_rows_sha256",
        "chart_signed_tangency_sheets": "chart_signed_tangency_sheets",
        "chart_sheet_rows_sha256": "chart_sheet_rows_sha256",
        "global_owner_rows_sha256": "global_owner_rows_sha256",
        "global_sheet_rows_sha256": "global_sheet_rows_sha256",
    }.items():
        if manifest_owner.get(manifest_key) != owner.get(summary_key):
            errors.append(f"owner replay mismatch: {manifest_key}")

    critical = summary["critical_endpoint_registry"]
    raw = data["raw_endpoint_universe"]
    for manifest_key, summary_key in {
        "target_target_common_tangent_descriptors": "raw_target_target_common_tangent_curve_descriptors",
        "target_target_descriptors_sha256": "target_target_descriptors_sha256",
        "source_grazing_equations": "raw_source_grazing_equations",
        "source_grazing_equations_sha256": "source_grazing_equations_sha256",
        "raw_analytic_endpoint_descriptors": "total_raw_analytic_endpoint_descriptors",
        "parameter_boundary_sheet_rows": "raw_parameter_boundary_sheet_rows",
        "constant_polarity_split_equations": "raw_constant_polarity_split_equations_u_y_zero",
    }.items():
        if raw.get(manifest_key) != critical.get(summary_key):
            errors.append(f"raw endpoint replay mismatch: {manifest_key}")

    first = critical["full_window_first_pass"]
    manifest_first = data["full_window_first_pass"]
    if manifest_first.get("initial_unresolved_descriptor_count") != first.get(
        "unresolved_descriptor_count"
    ):
        errors.append("first-pass unresolved replay mismatch")
    for key in ("classified_rows_sha256", "unresolved_descriptors_sha256"):
        if manifest_first.get(key) != first.get(key):
            errors.append(f"first-pass digest replay mismatch: {key}")

    adaptive = critical["adaptive_interval_isolation"]
    manifest_adaptive = data["adaptive_endpoint_completion"]
    replay_keys = (
        "adaptive_depth", "dyadic_grid_width",
        "descriptors_fully_resolved_after_subdivision",
        "regular_subinterval_leaf_count", "regular_subinterval_rows_sha256",
        "merged_transition_collar_count", "maximum_merged_collar_width",
        "maximum_collar_grid_widths", "merged_transition_collars_sha256",
        "transition_collar_orbits_under_Jx_Jy", "transition_collar_orbit_size",
        "transition_collar_orbits_sha256", "exact_third_target_tangency_vertices",
        "physical_transition_vertex_orbits_under_Jx_Jy",
        "nonphysical_tau_three_crossing_collars",
        "nonphysical_tau_three_orbits_under_Jx_Jy",
        "all_transition_collars_exactly_typed",
        "numerically_unresolved_transition_collar_count",
    )
    for key in replay_keys:
        if manifest_adaptive.get(key) != adaptive.get(key):
            errors.append(f"adaptive replay mismatch: {key}")
    return errors


def missing_global(data: dict[str, Any]) -> list[str]:
    completion = data.get("global_completion", {})
    return [key for key in OPEN_GLOBAL if completion.get(key) is not True]


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
        print("GATE3_OWNER_ENDPOINT_REGISTRY_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1

    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["adaptive_endpoint_completion"][
            "numerically_unresolved_transition_collar_count"
        ] = 1
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unresolved-count tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["global_completion"]["immutable_global_event_rows"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported global-row claim accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  unresolved-count tamper rejected")
        print("  unsupported global-row claim rejected")
        return 0

    print("GATE3_OWNER_PARTITION: CERTIFIED")
    print("GATE3_TARGET_TARGET_ENDPOINT_INTERVAL_TYPING: CERTIFIED")
    print("  first_pass_unresolved=288")
    print("  adaptive_regular=284")
    print("  corrected_physical_vertices=0")
    print("  retracted_nonforward_vertex_claims=16")
    print("  uniformly_nonphysical_tau3=4")
    print("  numerically_unresolved_transition_collars=0")
    if args.integrity_only:
        print("GATE3_OWNER_ENDPOINT_REGISTRY_INTEGRITY: PASS")
        return 0

    missing = missing_global(data)
    if missing:
        print("GATE3_CONNECTED_EVENT_ROWS_DQ_SCALAR_MATCHING: NOT_CERTIFIED")
        for key in missing:
            print(f"  missing={key}")
        return 2
    print("GATE3_CONNECTED_EVENT_ROWS_DQ_SCALAR_MATCHING: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
