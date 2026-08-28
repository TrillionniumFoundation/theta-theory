#!/usr/bin/env python3
"""Fail-closed verifier for the Round-49 typed-measure F10/F17 frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round49_typed_measure_f10_f17_frontier_cert as cert


HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError("unsafe manifest")
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=cert.strict_object
    )
    if not isinstance(value, dict):
        raise RuntimeError("manifest root")
    return value


def direct_arithmetic_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        decomposition = result["Lebesgue_decomposition_D1_non_domination"]
        rows = decomposition["local_countermodel"]["representative_exact_rows"]
        expected_rows = []
        for exponent in (4, 8, 12, 16, 20):
            epsilon = Q(1, 1 << exponent)
            expected_rows.append(
                {
                    "epsilon": str(epsilon),
                    "volume_of_tube": str(2 * epsilon),
                    "face_measure_of_tube": "1",
                    "face_to_volume_ratio": str(1 / (2 * epsilon)),
                }
            )
        if rows != expected_rows:
            errors.append("Lebesgue rows")
        if cert.digest(rows) != decomposition["local_countermodel"]["rows_sha256"]:
            errors.append("Lebesgue rows digest")
        if decomposition["finite_constant_D1_domination_of_nonzero_face_current"] is not False:
            errors.append("D1 domination guard")

        depth = result["return_depth_weighted_coarea_countermodel"]
        if depth["certified_one_step_inputs"]["positive_coarea_mass_upper"] != str(
            Q(8064, 5)
        ):
            errors.append("coarea mass")
        if depth["certified_one_step_inputs"]["raw_rank_L3over2_upper"] != str(
            Q(46506443753721, 13750)
        ):
            errors.append("raw rank moment")
        if depth["certified_one_step_inputs"][
            "bidirectional_raw_F10_L3over2_upper"
        ] != str(Q(272016189515514129, 13750)):
            errors.append("bidirectional F10 moment")
        depth_rows = depth["countermodel"]["representative_partial_sums"]
        expected_depth_rows = []
        for cutoff in (4, 16, 64):
            expected_depth_rows.append(
                {
                    "cutoff": cutoff,
                    "partial_mass": str(
                        sum(
                            (Q(1, n * (n + 1)) for n in range(1, cutoff + 1)),
                            Q(),
                        )
                    ),
                    "partial_depth_weighted_mass": str(
                        sum((Q(1, n + 1) for n in range(1, cutoff + 1)), Q())
                    ),
                }
            )
        if depth_rows != expected_depth_rows:
            errors.append("depth rows")
        if cert.digest(depth_rows) != depth["countermodel"]["rows_sha256"]:
            errors.append("depth rows digest")
        if depth["return_depth_weighted_coarea_integrability"] != "NOT_CERTIFIED":
            errors.append("depth nonpromotion")

        f17 = result["F17_suffix_product_countermodel"]
        dmin = 150 * (1 << 14)
        r = Q(111718729, 111718750)
        if f17["crude_suffix"]["minimum_one_step_derivative_factor"] != dmin:
            errors.append("Dmin")
        if f17["crude_suffix"]["minimum_factor_times_r"] != str(dmin * r):
            errors.append("Dmin*r")
        if not dmin * r > 1:
            errors.append("product ratio inequality")
        x = Q(25, 151)
        f13 = Q(3816937, 47112000)
        if f17["source_time_current"]["full_source_over_D1"] != str(x + f13):
            errors.append("source ratio")
        if f17["source_time_current"]["strict_quarter_slack"] != str(
            Q(1, 4) - x - f13
        ):
            errors.append("quarter slack")
        thresholds = f17["future_dynamic_test_thresholds"]
        if thresholds["if_multiplier_Cdyn_keeps_total_below_one_quarter"] != (
            "C_dyn<7961063/7800000"
        ):
            errors.append("quarter threshold")
        if thresholds["if_multiplier_Cdyn_keeps_total_below_one"] != (
            "C_dyn<43295063/7800000"
        ):
            errors.append("unit threshold")

        route = result["conditional_boundary_ZB_alternative"]
        multiplier = Q(5) * Q(2000, 1999)
        tangency = Q(516607461656000000, 47978559724753)
        boundary = 52 * tangency + 121 * 40
        fixed = multiplier * (boundary + 192 * 55)
        rank = multiplier * 103
        if route["trace_multiplier"] != str(multiplier):
            errors.append("trace multiplier")
        if route["conditional_fixed_Z_coefficient"] != str(fixed):
            errors.append("fixed Z coefficient")
        if route["conditional_occurrence_ZB_coefficient"] != str(rank):
            errors.append("rank ZB coefficient")
        if route["same_ID_ZB_trace_theorem"] != "NOT_CERTIFIED":
            errors.append("ZB nonpromotion")

        kernel = result["fixed_record_typed_measure_kernel"]
        if kernel["status"] != "CERTIFIED_TYPED_FIXED_RECORD_DIRECT_SUM_ONLY":
            errors.append("kernel scope")
        if kernel["global_sigma_finite_kernel_joint_measurability"] != "NOT_CERTIFIED":
            errors.append("global kernel nonpromotion")

        strict = result["strict_nonpromotion"]
        required = {
            "typed_fixed_record_measure_join": "CERTIFIED",
            "global_all_record_same_measure_F10_kernel": "NOT_CERTIFIED",
            "physical_D1_dominates_face_measures": False,
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F17_bulk_dynamic_test": "NOT_CERTIFIED",
            "joint_insertion_suffix_rank_tail": "NOT_CERTIFIED",
            "strong_F13": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        for key, value in required.items():
            if strict.get(key) != value:
                errors.append(f"strict {key}")
        update = result["Gate5_maturity_update"]
        if update["new_global_field_completed"] is not None:
            errors.append("maturity field promotion")
        if update["current_global_maturity"] != "10/18":
            errors.append("maturity")
        if update["complete_18_field_operator_block_count"] != 0:
            errors.append("block count")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"result structure: {exc}")
    return errors


def verify_object(manifest: dict[str, Any], replay: bool) -> list[str]:
    errors: list[str] = []
    expected_top = {
        "schema",
        "certificate_sha256",
        "verifier_sha256",
        "dependencies",
        "result",
        "verdict",
    }
    if set(manifest) != expected_top:
        errors.append("manifest keys")
    if manifest.get("schema") != cert.MANIFEST_SCHEMA:
        errors.append("manifest schema")
    if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
        errors.append("verifier hash")
    if manifest.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependency ledger")
    for name, expected in cert.DEPENDENCIES.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            errors.append(f"unsafe dependency {name}")
        elif sha(path) != expected:
            errors.append(f"dependency hash {name}")

    result = manifest.get("result")
    if not isinstance(result, dict):
        errors.append("result root")
        return errors
    if result.get("schema") != cert.RESULT_SCHEMA:
        errors.append("result schema")
    replay_digest = result.get("internal_replay_digest")
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    if replay_digest != cert.digest(payload):
        errors.append("internal replay digest")
    errors.extend(direct_arithmetic_errors(result))
    if manifest.get("verdict") != result.get("strict_nonpromotion"):
        errors.append("verdict projection")
    if replay:
        try:
            expected_result = cert.build_result()
        except Exception as exc:  # fail closed on dependency/replay faults
            errors.append(f"certificate replay: {exc}")
        else:
            if result != expected_result:
                errors.append("deterministic result replay")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def hostile_paths() -> list[tuple[str, ...]]:
    return [
        ("result", "fixed_record_typed_measure_kernel", "parameter_scope"),
        ("result", "fixed_record_typed_measure_kernel", "depth_scope"),
        ("result", "fixed_record_typed_measure_kernel", "common_record_token"),
        ("result", "fixed_record_typed_measure_kernel", "typed_vector_kernel"),
        ("result", "fixed_record_typed_measure_kernel", "recordwise_dominating_measure"),
        ("result", "fixed_record_typed_measure_kernel", "recordwise_Radon_Nikodym_typing"),
        ("result", "fixed_record_typed_measure_kernel", "seven_face_extension_scope"),
        ("result", "fixed_record_typed_measure_kernel", "global_all_record_face_owner_deduplication"),
        ("result", "fixed_record_typed_measure_kernel", "global_sigma_finite_kernel_joint_measurability"),
        ("result", "fixed_record_typed_measure_kernel", "physical_D1_domination_from_master_measure"),
        ("result", "fixed_record_typed_measure_kernel", "status"),
        ("result", "Lebesgue_decomposition_D1_non_domination", "regular_face_zero_volume"),
        ("result", "Lebesgue_decomposition_D1_non_domination", "nonzero_face_current"),
        ("result", "Lebesgue_decomposition_D1_non_domination", "Lambda_D1_density_on_face_sector"),
        ("result", "Lebesgue_decomposition_D1_non_domination", "finite_constant_D1_domination_of_nonzero_face_current"),
        ("result", "Lebesgue_decomposition_D1_non_domination", "common_normalization_repairs_singularity"),
        ("result", "Lebesgue_decomposition_D1_non_domination", "Round48_formal_subunit_ratio_becomes_physical_theorem"),
        ("result", "Lebesgue_decomposition_D1_non_domination", "status"),
        ("result", "return_depth_weighted_coarea_countermodel", "certified_one_step_inputs", "positive_coarea_mass_upper"),
        ("result", "return_depth_weighted_coarea_countermodel", "certified_one_step_inputs", "raw_rank_L3over2_upper"),
        ("result", "return_depth_weighted_coarea_countermodel", "certified_one_step_inputs", "bidirectional_raw_F10_L3over2_upper"),
        ("result", "return_depth_weighted_coarea_countermodel", "countermodel", "return_level_face_mass"),
        ("result", "return_depth_weighted_coarea_countermodel", "countermodel", "total_face_mass"),
        ("result", "return_depth_weighted_coarea_countermodel", "countermodel", "rank"),
        ("result", "return_depth_weighted_coarea_countermodel", "countermodel", "raw_rank_L3over2_moment"),
        ("result", "return_depth_weighted_coarea_countermodel", "countermodel", "depth_weighted_mass"),
        ("result", "return_depth_weighted_coarea_countermodel", "collision_SRB_Kac_formula_applies_to_singular_face_measure"),
        ("result", "return_depth_weighted_coarea_countermodel", "return_depth_weighted_coarea_integrability"),
        ("result", "return_depth_weighted_coarea_countermodel", "status"),
        ("result", "F17_suffix_product_countermodel", "source_time_current", "X_over_D1"),
        ("result", "F17_suffix_product_countermodel", "source_time_current", "F13_over_D1"),
        ("result", "F17_suffix_product_countermodel", "source_time_current", "full_source_over_D1"),
        ("result", "F17_suffix_product_countermodel", "source_time_current", "strict_quarter_slack"),
        ("result", "F17_suffix_product_countermodel", "crude_suffix", "minimum_one_step_derivative_factor"),
        ("result", "F17_suffix_product_countermodel", "crude_suffix", "survival_rate_r"),
        ("result", "F17_suffix_product_countermodel", "crude_suffix", "minimum_factor_times_r"),
        ("result", "F17_suffix_product_countermodel", "crude_suffix", "minimum_factor_times_r_exceeds_one"),
        ("result", "F17_suffix_product_countermodel", "geometric_countermodel", "return_law"),
        ("result", "F17_suffix_product_countermodel", "geometric_countermodel", "ranks"),
        ("result", "F17_suffix_product_countermodel", "geometric_countermodel", "suffix_product_moment"),
        ("result", "F17_suffix_product_countermodel", "future_dynamic_test_thresholds", "if_multiplier_Cdyn_keeps_total_below_one_quarter"),
        ("result", "F17_suffix_product_countermodel", "future_dynamic_test_thresholds", "if_multiplier_Cdyn_keeps_total_below_one"),
        ("result", "F17_suffix_product_countermodel", "F17_dynamic_test_multiplier"),
        ("result", "F17_suffix_product_countermodel", "joint_insertion_suffix_rank_tail"),
        ("result", "F17_suffix_product_countermodel", "status"),
        ("result", "conditional_boundary_ZB_alternative", "trace_multiplier"),
        ("result", "conditional_boundary_ZB_alternative", "plain_boundary_Z"),
        ("result", "conditional_boundary_ZB_alternative", "rank_weighted_boundary_ZB"),
        ("result", "conditional_boundary_ZB_alternative", "conditional_fixed_Z_coefficient"),
        ("result", "conditional_boundary_ZB_alternative", "conditional_occurrence_ZB_coefficient"),
        ("result", "conditional_boundary_ZB_alternative", "conditional_target"),
        ("result", "conditional_boundary_ZB_alternative", "same_ID_ZB_trace_theorem"),
        ("result", "conditional_boundary_ZB_alternative", "insertion_time_aggregate_ZB_resolvent"),
        ("result", "conditional_boundary_ZB_alternative", "return_depth_integrability_from_this_route"),
        ("result", "conditional_boundary_ZB_alternative", "status"),
        ("result", "Gate5_maturity_update", "new_global_field_completed"),
        ("result", "Gate5_maturity_update", "current_global_maturity"),
        ("result", "Gate5_maturity_update", "complete_18_field_operator_block_count"),
        ("result", "strict_nonpromotion", "typed_fixed_record_measure_join"),
        ("result", "strict_nonpromotion", "global_all_record_same_measure_F10_kernel"),
        ("result", "strict_nonpromotion", "physical_D1_dominates_face_measures"),
        ("result", "strict_nonpromotion", "return_depth_weighted_face_integrability"),
        ("result", "strict_nonpromotion", "complete_all_face_F10"),
        ("result", "strict_nonpromotion", "F17_bulk_dynamic_test"),
        ("result", "strict_nonpromotion", "joint_insertion_suffix_rank_tail"),
        ("result", "strict_nonpromotion", "strong_F13"),
        ("result", "strict_nonpromotion", "strong_cemetery"),
        ("result", "strict_nonpromotion", "Gate5_maturity"),
        ("result", "strict_nonpromotion", "complete_18_field_operator_block_count"),
        ("result", "strict_nonpromotion", "complete_composite_gates"),
        ("result", "strict_nonpromotion", "CM2"),
    ]


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    failures = 0
    total = 0

    for path in hostile_paths():
        total += 1
        mutant = copy.deepcopy(manifest)
        current: Any = mutant
        for key in path:
            current = current[key]
        replacement: Any
        if isinstance(current, bool):
            replacement = not current
        elif isinstance(current, int):
            replacement = current + 1
        elif current is None:
            replacement = "CERTIFIED"
        else:
            replacement = "HOSTILE_MUTATION"
        set_path(mutant, path, replacement)
        if not verify_object(mutant, replay=True):
            failures += 1

    for key, replacement in (
        ("schema", "bad.schema"),
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
        ("verdict", {}),
    ):
        total += 1
        mutant = copy.deepcopy(manifest)
        mutant[key] = replacement
        if not verify_object(mutant, replay=True):
            failures += 1

    total += 1
    mutant = copy.deepcopy(manifest)
    mutant["result"]["internal_replay_digest"] = "0" * 64
    if not verify_object(mutant, replay=True):
        failures += 1

    total += 1
    try:
        json.loads('{"x":1,"x":2}', object_pairs_hook=cert.strict_object)
    except ValueError:
        pass
    else:
        failures += 1

    return total - failures, total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        manifest = strict_load(args.manifest.resolve())
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1

    replay = args.replay or args.self_test or not args.integrity_only
    errors = verify_object(manifest, replay=replay)
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1

    if args.self_test:
        passed, total = self_test(manifest)
        print(f"HOSTILE_SELF_TEST: {passed}/{total}")
        if passed != total:
            return 1
    elif args.integrity_only:
        print("INTEGRITY_ONLY: PASS")
    elif args.replay:
        print("REPLAY: PASS")
    else:
        print("SAFE_MANIFEST: PASS")

    if args.integrity_only or args.replay or args.self_test:
        return 0
    print("GATE5_MATURITY: 10/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
