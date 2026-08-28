#!/usr/bin/env python3
"""Fail-closed verifier for the Gate-3 physical-first graph frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate3.physical-first-unresolved-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate3.physical-first-unresolved-frontier.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-physical-first-unresolved-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate3_physical_first_unresolved_frontier_cert.py"

# Filled from one clean materialization and frozen before the independent
# replay.  No completion flag is inferred from these counts alone.
EXPECTED_FRONTIER: dict[str, Any] = {
    "conditionally_physical_first_graph_chart_count": 27356,
    "nonempty_physical_first_root_arc_count": 7122,
    "untyped_candidate_graph_chart_count": 368,
    "maximum_terminal_boxes_on_one_fixed_s_slice": 1492,
    "uniform_fixed_s_terminal_positive_t_width_outer": "373/256",
    "maximum_candidate_graph_charts_on_one_fixed_s_slice": 486,
    "maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice": 2956,
    "maximum_conditionally_physical_first_graph_charts_on_one_fixed_s_slice": 478,
    "maximum_nonempty_physical_first_root_arcs_on_one_fixed_s_slice": 144,
    "maximum_normalized_absolute_root_slope_sum_on_one_fixed_s_slice": 2938,
    "conditionally_physical_first_dt_sign_counts": {
        "-1": 13678,
        "1": 13678,
    },
    "closed_v1_endpoint_sweep_values": {
        "candidate_graph": {
            "count": 480,
            "normalized_slope_sum": 600,
        },
        "conditionally_physical": {
            "count": 474,
            "normalized_slope_sum": 592,
        },
        "nonempty_physical": {"count": 126},
        "terminal": {
            "reason:candidate_zero_with_dt_containing_zero:count": 174,
            "reason:candidate_zero_with_dt_containing_zero:width": "87/512",
            "reason:interval_geometry_exception:count": 1246,
            "reason:interval_geometry_exception:width": "623/512",
            "reason:source_cp_not_strict:count": 24,
            "reason:source_cp_not_strict:width": "3/128",
            "terminal:count": 1444,
            "terminal:width": "361/256",
        },
    },
    "ordered_row_summary_ledger_sha256": (
        "d3bb1708bcea4ceaa4ecfb189da591bb2039c90a11f68fafae0aa2d9d65de1ab"
    ),
    "total_audit_call_count": 1209088,
}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    if data.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash mismatch")
    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or len(dependencies) != 2:
        errors.append("dependency ledger mismatch")
    else:
        for name, digest in dependencies.items():
            path = HERE / name
            if not path.is_file():
                errors.append(f"missing dependency: {name}")
            elif sha256_path(path) != digest:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    replay_digest = result.get("internal_replay_digest")
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    if replay_digest != canonical_digest(payload):
        errors.append("internal replay digest mismatch")

    provenance = result.get("provenance", {})
    frozen_name = (
        "cm2-gate3-finite-s-future-singularity-outer-atlas-manifest-2026-07-16.json"
    )
    frozen_cert_name = (
        "cm2_gate3_finite_s_future_singularity_outer_atlas_cert.py"
    )
    if provenance.get("frozen_outer_manifest_sha256") != sha256_path(
        HERE / frozen_name
    ):
        errors.append("frozen outer manifest provenance mismatch")
    if provenance.get("frozen_outer_certificate_sha256") != sha256_path(
        HERE / frozen_cert_name
    ):
        errors.append("frozen outer certificate provenance mismatch")

    frontier = result.get("reason_resolved_frontier")
    if not isinstance(frontier, dict):
        return errors + ["frontier missing"]
    resolution = frontier.get("frozen_resolution", {})
    for key, expected in {
        "maximum_additional_t_depth": 5,
        "maximum_additional_parameter_depth": 3,
        "resolution_is_reason_audit_not_complete_root_isolation": True,
        "selective_terminal_t_depth": 5,
        "selective_terminal_parameter_depth": 3,
    }.items():
        if resolution.get(key) != expected:
            errors.append(f"resolution mismatch: {key}")
    for key, expected in {
        "partial_current_is_on_actual_zero_subsets_of_conditionally_physical_first_charts": True,
        "possibly_empty_chart_contributes_zero_current": True,
        "half_open_t_v_chart_ownership_is_unique": True,
        "partial_current_is_not_complete_future_current": True,
        "v_is_not_probability_coordinate": True,
        "two_dimensional_areas_are_nonphysical_parameter_bookkeeping": True,
        "artificial_rectangular_t_boundary_is_not_future_physical_current": True,
        "closed_final_v_endpoint_explicitly_included_in_all_sweeps": True,
    }.items():
        if frontier.get(key) != expected:
            errors.append(f"typing flag mismatch: {key}")
    for key, expected in EXPECTED_FRONTIER.items():
        if expected is None or frontier.get(key) != expected:
            errors.append(f"frozen frontier field mismatch: {key}")

    rows = frontier.get("ordered_row_summary_ledger")
    if not isinstance(rows, list) or len(rows) != 64:
        errors.append("ordered row ledger mismatch")
    else:
        if [row.get("row_index") for row in rows] != list(range(64)):
            errors.append("ordered row indices mismatch")
        if frontier.get("ordered_row_summary_ledger_sha256") != canonical_digest(rows):
            errors.append("ordered row digest mismatch")
        if sum(row.get("audit_call_count", -1) for row in rows) != frontier.get(
            "total_audit_call_count"
        ):
            errors.append("audit-call sum mismatch")
        if sum(
            row.get("conditionally_physical_first_graph_chart_count", -1)
            for row in rows
        ) != frontier.get(
            "conditionally_physical_first_graph_chart_count"
        ):
            errors.append("physical-first row-count sum mismatch")
        if sum(
            row.get("nonempty_physical_first_root_arc_count", -1)
            for row in rows
        ) != frontier.get("nonempty_physical_first_root_arc_count"):
            errors.append("nonempty root-arc row-count sum mismatch")
        if sum(
            row.get("untyped_candidate_graph_chart_count", -1)
            for row in rows
        ) != frontier.get(
            "untyped_candidate_graph_chart_count"
        ):
            errors.append("untyped-root row-count sum mismatch")
        aggregate_dt_signs: Counter[str] = Counter()
        for row in rows:
            row_dt_signs = row.get("conditionally_physical_first_dt_sign_counts")
            if (
                not isinstance(row_dt_signs, dict)
                or set(row_dt_signs) - {"-1", "1"}
                or sum(row_dt_signs.values())
                != row.get("conditionally_physical_first_graph_chart_count")
            ):
                errors.append("row physical dt-sign ledger mismatch")
                break
            aggregate_dt_signs.update(row_dt_signs)
            for key in (
                "terminal_reason_records_sha256",
                "conditionally_physical_first_graph_records_sha256",
                "untyped_candidate_graph_records_sha256",
                "terminal_event_map_sha256",
                "physical_event_map_sha256",
                "candidate_graph_event_map_sha256",
                "nonempty_physical_event_map_sha256",
            ):
                value = row.get(key)
                if not isinstance(value, str) or len(value) != 64:
                    errors.append(f"row digest malformed: {key}")
                    break
        if dict(sorted(aggregate_dt_signs.items())) != frontier.get(
            "conditionally_physical_first_dt_sign_counts"
        ):
            errors.append("global physical dt-sign ledger mismatch")

    try:
        terminal_width = Fraction(
            frontier["uniform_fixed_s_terminal_positive_t_width_outer"]
        )
        zero = frontier["uniform_fixed_s_future_candidate_zero_intercept_Z"]
        if zero != (terminal_width == 0):
            errors.append("zero-intercept flag mismatch")
        if terminal_width < 0:
            errors.append("negative terminal width")
        graph_count = frontier[
            "maximum_candidate_graph_charts_on_one_fixed_s_slice"
        ]
        graph_leb = Fraction(
            frontier[
                "uniform_fixed_s_actual_candidate_zero_set_Leb_Z_linear_coefficient"
            ]
        )
        graph_density = Fraction(
            frontier[
                "uniform_fixed_s_actual_candidate_zero_set_row_law_Z_linear_coefficient"
            ]
        )
        if graph_leb != 2 * graph_count:
            errors.append("candidate graph Lebesgue Z mismatch")
        if graph_density != Fraction(126, 5) * graph_leb:
            errors.append("candidate graph row-law Z mismatch")
        physical_slope = frontier[
            "maximum_normalized_absolute_root_slope_sum_on_one_fixed_s_slice"
        ]
        current_tv = Fraction(
            frontier["partial_genuine_physical_marked_current_TV_upper"]
        )
        if current_tv != 2 * Fraction(126, 5) * 200 * physical_slope:
            errors.append("physical marked-current TV mismatch")
        if frontier[
            "maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice"
        ] < physical_slope:
            errors.append("candidate slope sum below physical subfamily")
        if graph_count < frontier[
            "maximum_conditionally_physical_first_graph_charts_on_one_fixed_s_slice"
        ]:
            errors.append("candidate graph count below physical subfamily")
        if frontier[
            "maximum_conditionally_physical_first_graph_charts_on_one_fixed_s_slice"
        ] < frontier[
            "maximum_nonempty_physical_first_root_arcs_on_one_fixed_s_slice"
        ]:
            errors.append("conditional physical chart count below nonempty arcs")
        dt_sign_counts = frontier[
            "conditionally_physical_first_dt_sign_counts"
        ]
        if (
            set(dt_sign_counts) != {"-1", "1"}
            or min(dt_sign_counts.values()) <= 0
            or sum(dt_sign_counts.values())
            != frontier["conditionally_physical_first_graph_chart_count"]
        ):
            errors.append("physical current orientation count mismatch")
        if frontier.get("partial_current_definition") != (
            "sum_i (partial_s_Delta_i/abs(partial_t_Delta_i)) "
            "rho_e(t_i,s) "
            "[delta_grazing_hit_i-delta_first_miss_side_owner_i]"
        ):
            errors.append("oriented physical current definition mismatch")
        if frontier.get("graph_velocity_current_orientation_identity") != (
            "partial_s_Delta/abs(partial_t_Delta)="
            "-sign(partial_t_Delta)*dt_graph/ds"
        ):
            errors.append("graph-velocity current orientation identity mismatch")
        v1 = frontier["closed_v1_endpoint_sweep_values"]
        if Fraction(v1["terminal"]["terminal:width"]) > terminal_width:
            errors.append("closed-v1 terminal width exceeds frozen maximum")
        if v1["terminal"]["terminal:count"] > frontier[
            "maximum_terminal_boxes_on_one_fixed_s_slice"
        ]:
            errors.append("closed-v1 terminal count exceeds frozen maximum")
        if v1["conditionally_physical"]["count"] > frontier[
            "maximum_conditionally_physical_first_graph_charts_on_one_fixed_s_slice"
        ]:
            errors.append("closed-v1 physical count exceeds frozen maximum")
        if v1["conditionally_physical"]["normalized_slope_sum"] > physical_slope:
            errors.append("closed-v1 physical slope exceeds frozen maximum")
        if v1["candidate_graph"]["count"] > graph_count:
            errors.append("closed-v1 candidate count exceeds frozen maximum")
        if v1["candidate_graph"]["normalized_slope_sum"] > frontier[
            "maximum_candidate_graph_normalized_slope_sum_on_one_fixed_s_slice"
        ]:
            errors.append("closed-v1 candidate slope exceeds frozen maximum")
        if v1["nonempty_physical"]["count"] > frontier[
            "maximum_nonempty_physical_first_root_arcs_on_one_fixed_s_slice"
        ]:
            errors.append("closed-v1 nonempty count exceeds frozen maximum")
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        errors.append("invalid rational/numeric frontier ledger")

    limits = result.get("scope_limits", {})
    if limits.get("terminal_unresolved_reason_decomposition") is not True:
        errors.append("missing terminal-reason decomposition scope")
    for key, count_key in (
        (
            "certified_nonempty_physical_first_root_arc_subfamily",
            "nonempty_physical_first_root_arc_count",
        ),
        (
            "conditionally_physical_first_graph_chart_family",
            "conditionally_physical_first_graph_chart_count",
        ),
        (
            "partial_genuine_marked_current_on_certified_subfamily",
            "conditionally_physical_first_graph_chart_count",
        ),
    ):
        if limits.get(key) != (frontier.get(count_key, 0) > 0):
            errors.append(f"derived certified scope mismatch: {key}")
    if limits.get("zero_intercept_complete_future_candidate_boundary_Z") != frontier.get(
        "uniform_fixed_s_future_candidate_zero_intercept_Z"
    ):
        errors.append("zero-intercept scope mismatch")
    if limits.get("all_candidate_graph_charts_typed_physical_first") != (
        frontier.get("untyped_candidate_graph_chart_count") == 0
    ):
        errors.append("all-roots-typed scope mismatch")
    for key in (
        "complete_root_isolated_owner_atlas",
        "complete_physical_future_current",
        "strong_source_invariance",
        "operator_norm_depth_two_DQ",
        "fixed_time_branch_record_MT_DQ",
        "physical_FACE_2CUT",
        "physical_FACE_TIME",
        "gate3_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    blockers = result.get("exact_remaining_blockers")
    if not isinstance(blockers, list) or len(blockers) != 5:
        errors.append("remaining blocker ledger mismatch")

    expected_verdict = {
        "terminal_unresolved_reason_decomposition": "CERTIFIED",
        "zero_intercept_finite_s_future_candidate_boundary_Z": (
            "CERTIFIED"
            if frontier.get("uniform_fixed_s_future_candidate_zero_intercept_Z")
            else "NOT_CERTIFIED"
        ),
        "conditionally_physical_first_graph_charts_and_partial_marked_current": "CERTIFIED",
        "complete_root_isolated_owner_atlas": "NOT_CERTIFIED",
        "complete_physical_future_current": "NOT_CERTIFIED",
        "fixed_time_branch_record_MT_DQ": "NOT_CERTIFIED",
        "physical_FACE_2CUT_and_FACE_TIME": "NOT_CERTIFIED",
        "gate3": "NOT_CERTIFIED",
    }
    if data.get("verdict") != expected_verdict:
        errors.append("verdict mismatch")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate3_physical_first_unresolved_frontier_cert as cert
        actual = cert.build_manifest()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["full certificate replay mismatch"]


def run_self_test(data: dict[str, Any]) -> int:
    mutations: list[tuple[str, dict[str, Any]]] = []

    def mutate(name: str, path: tuple[str, ...], value: Any) -> None:
        tampered = copy.deepcopy(data)
        target = tampered
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        if path and path[0] == "result":
            digest_payload = copy.deepcopy(tampered["result"])
            digest_payload.pop("internal_replay_digest", None)
            tampered["result"]["internal_replay_digest"] = canonical_digest(
                digest_payload
            )
        mutations.append((name, tampered))

    mutate("v probability overtype", (
        "result", "reason_resolved_frontier", "v_is_not_probability_coordinate",
    ), False)
    mutate("2D physical overtype", (
        "result", "reason_resolved_frontier",
        "two_dimensional_areas_are_nonphysical_parameter_bookkeeping",
    ), False)
    mutate("artificial boundary overtype", (
        "result", "reason_resolved_frontier",
        "artificial_rectangular_t_boundary_is_not_future_physical_current",
    ), False)
    mutate("terminal width deletion", (
        "result", "reason_resolved_frontier",
        "uniform_fixed_s_terminal_positive_t_width_outer",
    ), "1")
    mutate("candidate graph deletion", (
        "result", "reason_resolved_frontier",
        "maximum_candidate_graph_charts_on_one_fixed_s_slice",
    ), 0)
    mutate("candidate Z corruption", (
        "result", "reason_resolved_frontier",
        "uniform_fixed_s_actual_candidate_zero_set_Leb_Z_linear_coefficient",
    ), "1")
    mutate("current TV corruption", (
        "result", "reason_resolved_frontier",
        "partial_genuine_physical_marked_current_TV_upper",
    ), "1")
    mutate("current orientation deletion", (
        "result", "reason_resolved_frontier", "partial_current_definition",
    ), "sum_i (dt_i/ds) rho_e [hit-miss]")
    mutate("graph velocity polarity corruption", (
        "result", "reason_resolved_frontier",
        "graph_velocity_current_orientation_identity",
    ), "partial_s_Delta/partial_t_Delta")
    mutate("dt-sign ledger corruption", (
        "result", "reason_resolved_frontier",
        "conditionally_physical_first_dt_sign_counts", "1",
    ), 13679)
    mutate("closed-v1 omission", (
        "result", "reason_resolved_frontier",
        "closed_final_v_endpoint_explicitly_included_in_all_sweeps",
    ), False)
    mutate("row digest corruption", (
        "result", "reason_resolved_frontier",
        "ordered_row_summary_ledger_sha256",
    ), "0" * 64)
    mutate("complete owner atlas overclaim", (
        "result", "scope_limits", "complete_root_isolated_owner_atlas",
    ), True)
    mutate("complete current overclaim", (
        "result", "scope_limits", "complete_physical_future_current",
    ), True)
    mutate("MT_DQ overclaim", (
        "result", "scope_limits", "fixed_time_branch_record_MT_DQ",
    ), True)
    mutate("Gate-3 overclaim", (
        "result", "scope_limits", "gate3_certified",
    ), True)

    failed = [name for name, mutation in mutations if not check_structure(mutation)]
    if failed:
        print("SELF_TEST_FAILED:", ", ".join(failed))
        return 1
    print(f"SELF_TEST: PASS ({len(mutations)} mutations rejected)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    path = Path(args.manifest)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"INVALID_MANIFEST: {exc}")
        return 1
    errors = check_structure(data)
    if args.replay and not errors:
        errors.extend(check_replay(data))
    if errors:
        print("INVALID:")
        for error in errors:
            print(f"  - {error}")
        return 1
    if args.self_test:
        return run_self_test(data)
    if args.integrity_only:
        print("INTEGRITY: PASS")
        return 0
    if args.replay:
        print("REPLAY: PASS")
        return 0
    print("TERMINAL_UNRESOLVED_REASON_DECOMPOSITION: CERTIFIED")
    zero = data["result"]["reason_resolved_frontier"][
        "uniform_fixed_s_future_candidate_zero_intercept_Z"
    ]
    print(
        "ZERO_INTERCEPT_FINITE_S_FUTURE_CANDIDATE_BOUNDARY_Z: "
        + ("CERTIFIED" if zero else "NOT_CERTIFIED")
    )
    print("CONDITIONALLY_PHYSICAL_FIRST_GRAPH_CHARTS_AND_PARTIAL_MARKED_CURRENT: CERTIFIED")
    print("COMPLETE_ROOT_ISOLATED_OWNER_ATLAS: NOT_CERTIFIED")
    print("COMPLETE_PHYSICAL_FUTURE_CURRENT: NOT_CERTIFIED")
    print("FIXED_TIME_BRANCH_RECORD_MT_DQ: NOT_CERTIFIED")
    print("PHYSICAL_FACE_2CUT_AND_FACE_TIME: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
