#!/usr/bin/env python3
"""Fail-closed verifier for the Round-49 incidence-safe long-leaf atlas."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round49_incidence_safe_long_leaf_atlas_cert as cert


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def read(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=strict_object
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def independent_arithmetic(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    density = Q(2000, 1999)
    delta = Q(358863, 2883949304 * 10**90)
    source_cp = Q(175, 13959) * delta
    slope4_cp = Q(28, 451) * delta
    collar = Q(1, 8 * 152)
    total_collar = 2 * 152 * collar
    r_distance = collar / (Q(25, 4) + 29)
    target_cp2 = Q(36337, 900000) * delta * r_distance / Q(9, 25) ** 2
    short_cut = Q(1, 8 * 153)
    remaining = Q(1, 2) - total_collar - 153 * short_cut
    family_mass = Q(1, 2) * remaining / density
    delta_e = delta * short_cut / (Q(25, 4) + 29)
    beta = Q(230400, 5197322039)
    hit = Q(21, 111718750)
    central_mass = Q(1, 2) * Q(1, 2) / density
    if source_cp <= Q(1, 2**319) or source_cp >= Q(1, 2**318):
        errors.append("source rank bracket")
    if slope4_cp <= Q(1, 2**316) or slope4_cp >= Q(1, 2**315):
        errors.append("slope4 rank bracket")
    if collar != Q(1, 1216) or total_collar != Q(1, 4):
        errors.append("collar budget")
    if r_distance != Q(1, 42864):
        errors.append("target r distance")
    if target_cp2 != Q(4346668277, 480625240334358528 * 10**91):
        errors.append("target cp2 exact")
    if target_cp2 <= Q(1, 2**330):
        errors.append("target rank bracket")
    if short_cut != Q(1, 1224) or remaining != Q(1, 8):
        errors.append("short-component budget")
    if central_mass != Q(1999, 8000):
        errors.append("central mass")
    if family_mass != Q(1999, 32000):
        errors.append("incidence-safe mass")
    if delta_e != delta / 43146:
        errors.append("Euclidean delta")
    if beta / central_mass != Q(1843200000, 10389446755961):
        errors.append("central threshold")
    if beta / family_mass != Q(7372800000, 10389446755961):
        errors.append("Wdiag threshold")
    if hit / family_mass != Q(2688, 893303125):
        errors.append("direct threshold")
    if not (Q(1, 1409) > beta / family_mass > Q(1, 1410)):
        errors.append("Wdiag reciprocal")
    if not (Q(1, 332330) > hit / family_mass > Q(1, 332331)):
        errors.append("direct reciprocal")

    core = result.get("incidence_safe_long_leaf_compact_core", {})
    rows = [
        {
            "kind": "general invariant proper leaf",
            "source_rank_upper": 319,
            "target_rank_upper": 165,
            "incidence_rank_upper": 319,
        },
        {
            "kind": "slope-4 canonical leaf sub-class",
            "source_rank_upper": 316,
            "target_rank_upper": 165,
            "incidence_rank_upper": 316,
        },
    ]
    if core.get("rank_rows") != rows:
        errors.append("rank rows")
    if core.get("rank_rows_sha256") != cert.digest(rows):
        errors.append("rank digest")
    return errors


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        if (
            not path.is_file()
            or path.is_symlink()
            or path.resolve().parent != cert.HERE
        ):
            return ["unsafe manifest"]
        source = read(path)
        if source.get("schema") != cert.MANIFEST_SCHEMA:
            errors.append("manifest schema")
        if source.get("certificate_sha256") != cert.sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if source.get("verifier_sha256") != cert.sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if source.get("dependencies") != cert.DEPENDENCIES:
            errors.append("dependencies")
        replay = cert.build_result()
        if source.get("result") != replay:
            errors.append("result replay")
        if source.get("verdict") != replay["strict_nonpromotion"]:
            errors.append("verdict replay")
        result = source.get("result", {})
        errors.extend(independent_arithmetic(result))

        core = result.get("incidence_safe_long_leaf_compact_core", {})
        if core.get("status") != (
            "CERTIFIED_CONDITIONAL_PER_ADMISSIBLE_FAMILY_NUMERIC_COMPACT_CORE"
        ):
            errors.append("compact core status")
        if "physical arbitrary-R_n whole-family grouping is not installed" not in core.get(
            "object_scope", ""
        ):
            errors.append("compact core object scope")
        if "canonical conditional density ratio is <2000/1999" not in core.get(
            "leaf_hypothesis", ""
        ):
            errors.append("compact core density hypothesis")
        if core.get("central_half_family_mass_strict_lower") != "1999/8000":
            errors.append("central mass field")
        if core.get("incidence_safe_family_mass_strict_lower") != "1999/32000":
            errors.append("safe mass field")
        if core.get("target_rank_upper") != 165:
            errors.append("target rank field")
        if "if the path exits that region" not in core.get(
            "target_cp_case_split", ""
        ):
            errors.append("target cp case split")
        if core.get("incidence_safe_piece_count_per_leaf_upper") != 153:
            errors.append("piece count")
        if core.get("all_tangency_collars_adapted_length_fraction_upper") != "1/4":
            errors.append("collar fraction field")
        if core.get("incidence_safe_adapted_length_fraction_strict_lower") != "1/8":
            errors.append("safe length field")

        ledger = result.get("exact_remaining_cover_thresholds", {})
        if ledger.get("status") != "CERTIFIED_EXACT_CONDITIONAL_THRESHOLD_LEDGER":
            errors.append("threshold status")
        if ledger.get("incidence_safe_required_Wdiag_fraction") != (
            "7372800000/10389446755961"
        ):
            errors.append("Wdiag threshold field")
        if ledger.get("incidence_safe_required_direct_C24_fraction") != (
            "2688/893303125"
        ):
            errors.append("direct threshold field")
        if ledger.get("actual_fraction_certified") is not False:
            errors.append("fraction overclaim")

        tech = result.get("latest_sufficient_rectangles_interface", {})
        if tech.get("status") != "CONDITIONAL_FIXED_S_TARGET_INTERFACE":
            errors.append("technology status")
        if tech.get("target_rectangle_inside_C24") != (
            "QUALITATIVE_FIXED_S_EXISTENCE_SEPARATE_FROM_THE_SUFFICIENT_COVER"
        ):
            errors.append("target rectangle")
        if tech.get("fixed_s_target_sensitive_hit") != (
            "CONDITIONAL_ON_TARGET_RECTANGLE_IN_SUFFICIENT_COVER"
        ):
            errors.append("target-sensitive hit scope")
        if tech.get("same_cover_bridge_installed") is not False:
            errors.append("same-cover bridge overclaim")
        if tech.get("common_over_parameter_window") is not False:
            errors.append("parameter uniformity overclaim")
        if tech.get("numeric_rectangle_rows_materialized") is not False:
            errors.append("rectangle rows overclaim")
        for key in (
            "numeric_N",
            "numeric_source_subcurve_fraction",
            "numeric_H_cover",
            "numeric_actual_beta_Wdiag",
        ):
            if tech.get(key) is not None:
                errors.append(f"technology overclaim: {key}")
        if tech.get("strict_inferable_uniform_beta_lower") != "0":
            errors.append("uniform beta lower")
        if tech.get("not_the_Round47_full_p_band_predicate") is not True:
            errors.append("predicate distinction")

        frontier = result.get("corrected_frontier", {})
        if frontier.get("numeric_long_leaf_incidence_safe_core") != (
            "CERTIFIED_CONDITIONAL_PER_ADMISSIBLE_FAMILY"
        ):
            errors.append("frontier compact-core scope")
        if frontier.get("fixed_s_qualitative_C24_target_hit") != (
            "NOT_CERTIFIED_PENDING_SAME_COVER_BRIDGE"
        ):
            errors.append("frontier same-cover bridge")
        if frontier.get("numeric_H_cover") is not None:
            errors.append("frontier H overclaim")
        if frontier.get("numeric_actual_beta_Wdiag") is not None:
            errors.append("frontier beta overclaim")
        for key in (
            "uniform_parameter_window_numeric_rectangle_atlas",
            "same_ID_two_orientation_cover",
            "complete_numeric_C_fw_C_rev_q",
            "strong_cemetery",
        ):
            if frontier.get(key) != "NOT_CERTIFIED":
                errors.append(f"frontier promotion: {key}")

        expected = {
            "numeric_incidence_safe_long_leaf_compact_core": "CERTIFIED_CONDITIONAL_PER_ADMISSIBLE_FAMILY",
            "exact_conditional_Wdiag_and_direct_C24_thresholds": "CERTIFIED",
            "fixed_s_qualitative_target_sensitive_rectangle_interface": "CONDITIONAL_NOT_INSTALLED",
            "uniform_numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if result.get("strict_nonpromotion") != expected:
            errors.append("strict nonpromotion")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(path: Path) -> tuple[int, int]:
    source = read(path)
    changes: list[tuple[tuple[str, ...], Any]] = [
        (("schema",), "bad"),
        (("certificate_sha256",), "0" * 64),
        (("verifier_sha256",), "0" * 64),
        (("dependencies",), {}),
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "parameter_scope"), "uniform theorem"),
        (("result", "incidence_safe_long_leaf_compact_core", "status"), "NOT_CERTIFIED"),
        (("result", "incidence_safe_long_leaf_compact_core", "object_scope"), "GLOBAL_INSTALLED"),
        (("result", "incidence_safe_long_leaf_compact_core", "leaf_hypothesis"), "NO_DENSITY_HYPOTHESIS"),
        (("result", "incidence_safe_long_leaf_compact_core", "target_cp_case_split"), "OMITTED"),
        (("result", "incidence_safe_long_leaf_compact_core", "invariant_cone"), "V=4"),
        (("result", "incidence_safe_long_leaf_compact_core", "central_half_family_mass_strict_lower"), "1"),
        (("result", "incidence_safe_long_leaf_compact_core", "tangency_sheet_count_upper"), 151),
        (("result", "incidence_safe_long_leaf_compact_core", "true_component_count_upper"), 152),
        (("result", "incidence_safe_long_leaf_compact_core", "all_tangency_collars_adapted_length_fraction_upper"), "0"),
        (("result", "incidence_safe_long_leaf_compact_core", "target_rank_upper"), 164),
        (("result", "incidence_safe_long_leaf_compact_core", "incidence_safe_family_mass_strict_lower"), "1999/8000"),
        (("result", "incidence_safe_long_leaf_compact_core", "incidence_safe_piece_count_per_leaf_upper"), 152),
        (("result", "incidence_safe_long_leaf_compact_core", "rank_rows_sha256"), "0" * 64),
        (("result", "exact_remaining_cover_thresholds", "status"), "THEOREM"),
        (("result", "exact_remaining_cover_thresholds", "incidence_safe_required_Wdiag_fraction"), "1/1410"),
        (("result", "exact_remaining_cover_thresholds", "incidence_safe_Wdiag_safe_reciprocal"), "1/1410"),
        (("result", "exact_remaining_cover_thresholds", "incidence_safe_required_direct_C24_fraction"), "0"),
        (("result", "exact_remaining_cover_thresholds", "direct_C24_safe_reciprocal"), "1/332331"),
        (("result", "exact_remaining_cover_thresholds", "actual_fraction_certified"), True),
        (("result", "latest_sufficient_rectangles_interface", "status"), "CERTIFIED_NUMERIC"),
        (("result", "latest_sufficient_rectangles_interface", "numeric_input_delta_rect"), "0"),
        (("result", "latest_sufficient_rectangles_interface", "target_rectangle_inside_C24"), "NUMERIC"),
        (("result", "latest_sufficient_rectangles_interface", "fixed_s_target_sensitive_hit"), "CERTIFIED"),
        (("result", "latest_sufficient_rectangles_interface", "same_cover_bridge_installed"), True),
        (("result", "latest_sufficient_rectangles_interface", "common_over_parameter_window"), True),
        (("result", "latest_sufficient_rectangles_interface", "numeric_rectangle_rows_materialized"), True),
        (("result", "latest_sufficient_rectangles_interface", "numeric_N"), 1),
        (("result", "latest_sufficient_rectangles_interface", "numeric_source_subcurve_fraction"), "1/2"),
        (("result", "latest_sufficient_rectangles_interface", "numeric_H_cover"), 1),
        (("result", "latest_sufficient_rectangles_interface", "numeric_actual_beta_Wdiag"), "1/1409"),
        (("result", "latest_sufficient_rectangles_interface", "strict_inferable_uniform_beta_lower"), "1/1409"),
        (("result", "latest_sufficient_rectangles_interface", "not_the_Round47_full_p_band_predicate"), False),
        (("result", "corrected_frontier", "numeric_H_cover"), 1),
        (("result", "corrected_frontier", "numeric_actual_beta_Wdiag"), "1/1409"),
        (("result", "corrected_frontier", "same_ID_two_orientation_cover"), "CERTIFIED"),
        (("result", "corrected_frontier", "complete_numeric_C_fw_C_rev_q"), "CERTIFIED"),
        (("result", "corrected_frontier", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "1/5"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "Gate4"), "CERTIFIED"),
        (("verdict", "CM2"), "GO"),
    ]
    passed = 0
    bodies: list[str] = []
    for field_path, replacement in changes:
        mutation = copy.deepcopy(source)
        set_path(mutation, field_path, replacement)
        bodies.append(json.dumps(mutation, sort_keys=True) + "\n")
    bodies.append('{"schema":"x","schema":"y"}\n')
    for body in bodies:
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=".cm2-r49-atlas-hostile-",
            suffix=".json",
            dir=cert.HERE,
            delete=False,
        )
        candidate = Path(handle.name)
        try:
            with handle:
                handle.write(body)
            errors = verify(candidate)
            if errors and errors != ["unsafe manifest"]:
                passed += 1
        finally:
            candidate.unlink(missing_ok=True)
    return passed, len(changes) + 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.self_test:
        passed, total = self_test(args.manifest)
        print(f"SELF_TEST: {passed}/{total}")
        return 0 if passed == total else 1
    print("VERIFY: PASS")
    if args.integrity_only or args.replay:
        return 0
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
