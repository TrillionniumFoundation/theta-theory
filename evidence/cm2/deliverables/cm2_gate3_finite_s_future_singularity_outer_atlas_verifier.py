#!/usr/bin/env python3
"""Fail-closed verifier for the finite-s future-candidate outer atlas."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate3.finite-s-future-singularity-outer-atlas.manifest.v1"
RESULT_SCHEMA = "cm2.gate3.finite-s-future-singularity-outer-atlas.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate3-finite-s-future-singularity-outer-atlas-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate3_finite_s_future_singularity_outer_atlas_cert.py"

# Filled after the first complete materialization, then frozen before the
# independent replay.  The ordered row-digest ledger avoids transporting a
# gigabyte of leaf dictionaries through the multiprocessing result pipe.
EXPECTED_ATLAS: dict[str, Any] = {
    "immutable_component_count": 626274,
    "transverse_candidate_root_strip_count": 6246,
    "terminal_unresolved_box_count": 129634,
    "ordered_row_record_digest_ledger_sha256": (
        "8c202faa1491cdca7351bd3ff9d0402f23504ff0eb3d8181ee20b72f0e810a28"
    ),
    "row_work_ledger_sha256": (
        "4817377eb109fd82d228a29a96a82aa3eab992554236a14fd11d7022512d9afc"
    ),
    "parameter_slice_ledger_sha256": (
        "b17617ec5e766e3575aac2ab5210ab12c35f31787279008602902ec79bd50b2c"
    ),
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
    if not isinstance(dependencies, dict) or len(dependencies) != 4:
        errors.append("dependency ledger mismatch")
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
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema mismatch")
    digest = result.get("internal_replay_digest")
    digest_payload = copy.deepcopy(result)
    digest_payload.pop("internal_replay_digest", None)
    if digest != canonical_digest(digest_payload):
        errors.append("internal replay digest mismatch")

    candidate = result.get("candidate_universe_and_filter_audit", {})
    for key, expected in {
        "candidate_discriminant_function_count": 4704,
        "candidate_only_full_equivalence_sample_count": 8,
        "candidate_only_full_equivalence": True,
    }.items():
        if candidate.get(key) != expected:
            errors.append(f"candidate/filter audit mismatch: {key}")
    for key in (
        "per_row_candidate_counts_sha256",
        "candidate_only_full_equivalence_samples_sha256",
    ):
        value = candidate.get(key)
        if not isinstance(value, str) or len(value) != 64:
            errors.append(f"candidate/filter digest malformed: {key}")

    atlas = result.get("future_outer_atlas", {})
    for key, expected in {
        "row_count": 64,
        "candidate_discriminant_function_count": 4704,
        "initial_t_cells_per_row_parameter_slab": 32,
        "initial_parameter_slabs": 8,
        "maximum_additional_t_depth": 5,
        "maximum_additional_parameter_depth": 3,
        "accepted_root_strip_t_width_upper": "1/1024",
        "outer_cover_is_not_singularity_mass": True,
        "v_half_open_except_last_closed": True,
        "v_is_not_probability_coordinate": True,
        "two_dimensional_bookkeeping_is_nonphysical_parameter_integrated": True,
        "root_graphs_not_certified_physical_first": True,
        "formal_two_point_mark_not_physical_current": True,
        "fixed_s_row_law_bounds_are_outer_charges_not_face_current_certificates": True,
        "uniform_fixed_s_artificial_rectangular_t_boundary_Z": True,
        "finite_common_future_singularity_outer_atlas": True,
    }.items():
        if atlas.get(key) != expected:
            errors.append(f"atlas fixed field mismatch: {key}")
    for key, expected in EXPECTED_ATLAS.items():
        if expected is None or atlas.get(key) != expected:
            errors.append(f"atlas frozen replay field mismatch: {key}")

    try:
        immutable = Fraction(atlas["immutable_normalized_parameter_area"])
        roots = Fraction(
            atlas["transverse_candidate_root_strip_normalized_parameter_area"]
        )
        unresolved = Fraction(atlas["terminal_unresolved_normalized_parameter_area"])
        bad = Fraction(atlas["total_bad_outer_cover_normalized_parameter_area"])
        fraction = Fraction(atlas["bad_outer_cover_fraction_of_64_row_carrier"])
        if min(immutable, roots, unresolved) < 0 or immutable + roots + unresolved != 64:
            errors.append("normalized parameter-area partition mismatch")
        if bad != roots + unresolved or fraction != bad / 64:
            errors.append("bad outer-cover parameter-area mismatch")

        density_bad = Fraction(
            atlas["parameter_integrated_density_weighted_bad_outer_bookkeeping"]
        )
        formal_bad = Fraction(
            atlas["parameter_integrated_formal_two_mark_bad_outer_bookkeeping"]
        )
        if density_bad != Fraction(126, 5) * bad or formal_bad != 2 * density_bad:
            errors.append("parameter-integrated bad bookkeeping mismatch")

        perimeter = Fraction(
            atlas["parameter_integrated_artificial_rectangle_perimeter_sum"]
        )
        boundary = Fraction(
            atlas["parameter_integrated_artificial_boundary_Leb_linear_coefficient"]
        )
        density_boundary = Fraction(
            atlas[
                "parameter_integrated_artificial_boundary_density_weighted_linear_bookkeeping"
            ]
        )
        formal_boundary = Fraction(
            atlas[
                "parameter_integrated_artificial_boundary_formal_two_mark_linear_bookkeeping"
            ]
        )
        if boundary != 2 * perimeter:
            errors.append("parameter-integrated boundary arithmetic mismatch")
        if density_boundary != Fraction(126, 5) * boundary:
            errors.append("parameter-integrated density boundary mismatch")
        if formal_boundary != 2 * density_boundary:
            errors.append("parameter-integrated formal-mark boundary mismatch")

        root_length = Fraction(
            atlas["parameter_integrated_candidate_root_graph_length_upper"]
        )
        root_tube = Fraction(
            atlas[
                "parameter_integrated_candidate_root_Leb_tube_linear_coefficient"
            ]
        )
        root_count = atlas["transverse_candidate_root_strip_count"]
        if root_tube != 2 * root_length + 4 * root_count:
            errors.append("candidate-root parameter-tube mismatch")
        root_density = Fraction(
            atlas[
                "parameter_integrated_candidate_root_density_weighted_linear_bookkeeping"
            ]
        )
        root_formal = Fraction(
            atlas[
                "parameter_integrated_candidate_root_formal_two_mark_linear_bookkeeping"
            ]
        )
        if root_density != Fraction(126, 5) * root_tube or root_formal != 2 * root_density:
            errors.append("candidate-root parameter bookkeeping mismatch")

        unresolved_perimeter = Fraction(
            atlas["parameter_integrated_unresolved_rectangle_perimeter_sum"]
        )
        unresolved_intercept = Fraction(
            atlas[
                "parameter_integrated_unresolved_density_weighted_intercept_bookkeeping"
            ]
        )
        unresolved_linear = Fraction(
            atlas[
                "parameter_integrated_unresolved_density_weighted_linear_bookkeeping"
            ]
        )
        unresolved_count = atlas["terminal_unresolved_box_count"]
        if unresolved_intercept != Fraction(126, 5) * unresolved:
            errors.append("unresolved parameter intercept mismatch")
        if unresolved_linear != Fraction(126, 5) * (
            2 * unresolved_perimeter + 4 * unresolved_count
        ):
            errors.append("unresolved parameter linear mismatch")

        max_all = atlas["maximum_all_artificial_rectangles_on_one_parameter_slice"]
        max_roots = atlas["maximum_candidate_root_graphs_on_one_parameter_slice"]
        max_unresolved = atlas["maximum_unresolved_boxes_on_one_parameter_slice"]
        slice_width = Fraction(
            atlas["uniform_parameter_slice_unresolved_t_width_outer"]
        )
        artificial_leb = Fraction(
            atlas[
                "uniform_fixed_s_artificial_rectangular_t_boundary_Leb_Z_linear_coefficient"
            ]
        )
        artificial_density = Fraction(
            atlas[
                "uniform_fixed_s_artificial_rectangular_t_boundary_row_law_density_Z_linear_coefficient"
            ]
        )
        artificial_formal = Fraction(
            atlas[
                "uniform_fixed_s_artificial_rectangular_t_boundary_formal_two_mark_Z_linear_coefficient"
            ]
        )
        if artificial_leb != 4 * max_all:
            errors.append("fixed-s artificial t-boundary count mismatch")
        if artificial_density != Fraction(126, 5) * artificial_leb:
            errors.append("fixed-s artificial t-boundary row-density mismatch")
        if artificial_formal != 2 * artificial_density:
            errors.append("fixed-s artificial t-boundary formal-mark mismatch")

        candidate_leb = Fraction(
            atlas["uniform_fixed_s_candidate_root_Leb_Z_linear_coefficient"]
        )
        candidate_density = Fraction(
            atlas[
                "uniform_fixed_s_candidate_root_row_law_density_Z_linear_coefficient"
            ]
        )
        candidate_formal = Fraction(
            atlas[
                "uniform_fixed_s_candidate_root_formal_two_mark_Z_linear_coefficient"
            ]
        )
        if candidate_leb != 2 * max_roots:
            errors.append("fixed-s candidate-root Z mismatch")
        if candidate_density != Fraction(126, 5) * candidate_leb:
            errors.append("fixed-s candidate-root density mismatch")
        if candidate_formal != 2 * candidate_density:
            errors.append("fixed-s candidate-root formal-mark mismatch")

        full_intercept = Fraction(
            atlas[
                "uniform_fixed_s_future_candidate_row_law_density_outer_intercept"
            ]
        )
        full_linear = Fraction(
            atlas[
                "uniform_fixed_s_future_candidate_row_law_density_outer_linear_coefficient"
            ]
        )
        full_formal_intercept = Fraction(
            atlas[
                "uniform_fixed_s_future_candidate_formal_two_mark_outer_intercept"
            ]
        )
        full_formal_linear = Fraction(
            atlas[
                "uniform_fixed_s_future_candidate_formal_two_mark_outer_linear_coefficient"
            ]
        )
        if full_intercept != Fraction(126, 5) * slice_width:
            errors.append("fixed-s future-candidate intercept mismatch")
        normalized_count = full_linear / Fraction(252, 5)
        if normalized_count.denominator != 1 or not (
            0 <= normalized_count <= max_roots + max_unresolved
        ):
            errors.append("fixed-s future-candidate linear mismatch")
        if full_formal_intercept != 2 * full_intercept or full_formal_linear != 2 * full_linear:
            errors.append("fixed-s future-candidate formal-mark mismatch")
        if atlas.get("uniform_fixed_s_full_future_zero_intercept_Z") != (slice_width == 0):
            errors.append("fixed-s zero-intercept flag mismatch")
        if atlas.get("finite_common_root_isolated_complete_atlas") != (unresolved_count == 0):
            errors.append("complete root-atlas flag mismatch")
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        errors.append("invalid rational atlas ledger")

    row_digests = atlas.get("ordered_row_record_digest_ledger")
    if not isinstance(row_digests, list) or len(row_digests) != 64:
        errors.append("ordered row-digest ledger mismatch")
    else:
        if [row.get("row_index") for row in row_digests] != list(range(64)):
            errors.append("ordered row-digest indices mismatch")
        if atlas.get("ordered_row_record_digest_ledger_sha256") != canonical_digest(row_digests):
            errors.append("ordered row-digest ledger hash mismatch")
        for row in row_digests:
            for key in ("immutable_digest", "root_digest", "unresolved_digest"):
                value = row.get(key)
                if not isinstance(value, str) or len(value) != 64:
                    errors.append(f"row record digest malformed: {key}")
                    break
        if sum(row.get("immutable_count", -1) for row in row_digests) != atlas.get("immutable_component_count"):
            errors.append("row immutable-count sum mismatch")
        if sum(row.get("root_count", -1) for row in row_digests) != atlas.get("transverse_candidate_root_strip_count"):
            errors.append("row root-count sum mismatch")
        if sum(row.get("unresolved_count", -1) for row in row_digests) != atlas.get("terminal_unresolved_box_count"):
            errors.append("row unresolved-count sum mismatch")

    work = atlas.get("row_work_ledger")
    if not isinstance(work, list) or len(work) != 64:
        errors.append("row work ledger mismatch")
    else:
        if atlas.get("row_work_ledger_sha256") != canonical_digest(work):
            errors.append("row work ledger hash mismatch")
        if sum(row.get("audit_call_count", -1) for row in work) != atlas.get("total_audit_call_count"):
            errors.append("audit-call sum mismatch")
        if max(row.get("audit_call_count", -1) for row in work) != atlas.get("maximum_audit_calls_on_one_row"):
            errors.append("maximum row work mismatch")

    status_counts = atlas.get("status_counts", {})
    if not isinstance(status_counts, dict) or sum(status_counts.values()) != (
        atlas.get("immutable_component_count", -1)
        + atlas.get("transverse_candidate_root_strip_count", -1)
        + atlas.get("terminal_unresolved_box_count", -1)
    ):
        errors.append("terminal status-count ledger mismatch")
    if atlas.get("all_root_strips_have_strict_dt_and_opposite_vertical_edge_signs") is not True:
        errors.append("root-strip transversality flag missing")

    limits = result.get("scope_limits", {})
    for key in (
        "full_finite_s_parameter_window",
        "fixed_finite_rectangular_common_carrier",
        "strictly_quantified_bad_parameter_outer_cover",
        "uniform_fixed_s_artificial_rectangular_t_boundary_Z",
        "uniform_fixed_s_candidate_root_outer_Z",
        "uniform_fixed_s_future_candidate_row_law_outer_charge",
    ):
        if limits.get(key) is not True:
            errors.append(f"missing certified scope flag: {key}")
    for key in (
        "two_dimensional_v_average_is_physical_mass_or_current",
        "candidate_root_graphs_are_certified_physical_first",
        "formal_two_point_mark_is_physical_current",
        "physical_face_or_current_on_future_atlas",
        "strong_source_invariance",
        "operator_norm_depth_two_DQ",
        "fixed_time_branch_record_MT_DQ",
        "physical_FACE_2CUT",
        "physical_FACE_TIME",
        "gate3_certified",
    ):
        if limits.get(key) is not False:
            errors.append(f"unsupported completion flag: {key}")
    if limits.get("complete_root_isolated_future_atlas") != atlas.get(
        "finite_common_root_isolated_complete_atlas"
    ):
        errors.append("complete-root scope flag mismatch")

    blockers = result.get("exact_remaining_blockers")
    if not isinstance(blockers, list) or len(blockers) != 6:
        errors.append("remaining blocker ledger mismatch")

    expected_verdict = {
        "finite_s_future_candidate_outer_atlas": "CERTIFIED",
        "uniform_fixed_s_artificial_rectangular_t_boundary_Z": "CERTIFIED",
        "uniform_fixed_s_candidate_root_outer_Z": "CERTIFIED",
        "complete_finite_s_root_isolated_future_atlas": "NOT_CERTIFIED",
        "physical_future_face_or_current": "NOT_CERTIFIED",
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
        import cm2_gate3_finite_s_future_singularity_outer_atlas_cert as cert
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
        mutations.append((name, tampered))

    mutate("candidate deletion", (
        "result", "candidate_universe_and_filter_audit",
        "candidate_discriminant_function_count",
    ), 4703)
    mutate("filter equivalence deletion", (
        "result", "candidate_universe_and_filter_audit",
        "candidate_only_full_equivalence",
    ), False)
    mutate("unresolved-area deletion", (
        "result", "future_outer_atlas",
        "terminal_unresolved_normalized_parameter_area",
    ), "0")
    mutate("v probability overtype", (
        "result", "scope_limits",
        "two_dimensional_v_average_is_physical_mass_or_current",
    ), True)
    mutate("physical-first overtype", (
        "result", "scope_limits",
        "candidate_root_graphs_are_certified_physical_first",
    ), True)
    mutate("physical-current overtype", (
        "result", "scope_limits",
        "formal_two_point_mark_is_physical_current",
    ), True)
    mutate("half-open ownership deletion", (
        "result", "future_outer_atlas", "v_half_open_except_last_closed",
    ), False)
    mutate("row digest corruption", (
        "result", "future_outer_atlas",
        "ordered_row_record_digest_ledger_sha256",
    ), "0" * 64)
    mutate("fixed-s artificial t-boundary Z corruption", (
        "result", "future_outer_atlas",
        "uniform_fixed_s_artificial_rectangular_t_boundary_Leb_Z_linear_coefficient",
    ), "1")
    mutate("MT_DQ overclaim", (
        "result", "scope_limits", "fixed_time_branch_record_MT_DQ",
    ), True)
    mutate("Gate-3 overclaim", (
        "result", "scope_limits", "gate3_certified",
    ), True)

    failed = []
    for name, mutation in mutations:
        if not check_structure(mutation):
            failed.append(name)
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
    print("FINITE_S_FUTURE_CANDIDATE_OUTER_ATLAS: CERTIFIED")
    print("UNIFORM_FIXED_S_ARTIFICIAL_RECTANGULAR_T_BOUNDARY_Z: CERTIFIED")
    print("UNIFORM_FIXED_S_CANDIDATE_ROOT_OUTER_Z: CERTIFIED")
    print("COMPLETE_FINITE_S_ROOT_ISOLATED_FUTURE_ATLAS: NOT_CERTIFIED")
    print("PHYSICAL_FUTURE_FACE_OR_CURRENT: NOT_CERTIFIED")
    print("FIXED_TIME_BRANCH_RECORD_MT_DQ: NOT_CERTIFIED")
    print("PHYSICAL_FACE_2CUT_AND_FACE_TIME: NOT_CERTIFIED")
    print("GATE3: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
