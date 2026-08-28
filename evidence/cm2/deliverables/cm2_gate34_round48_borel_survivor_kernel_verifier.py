#!/usr/bin/env python3
"""Fail-closed verifier for the Round-48 Borel survivor-kernel layer."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round48_borel_survivor_kernel_cert as cert


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
    if Q(1, 6030) * 319590 != 53:
        errors.append("one-orientation base")
    if Q(1, 6030) * 1005 != Q(1, 6):
        errors.append("one-orientation slope")
    if Q(1, 12060) * 639180 != 53:
        errors.append("pair base")
    if Q(1, 12060) * 1005 != Q(1, 12):
        errors.append("pair slope")
    if Q(1, 2) * Q(6, 5) != Q(3, 5):
        errors.append("shell ratio")
    union = 8 * Q(7, 715000)
    threshold = Q(230400, 5197322039)
    if union != Q(7, 89375):
        errors.append("Wdiag union")
    if union - threshold != Q(1214558021, 35731589018125):
        errors.append("Wdiag excess")
    if union / threshold != Q(2798558021, 1584000000):
        errors.append("Wdiag ratio")
    proper_c_p = Q(4 * 10**90 * 360493663, 358863)
    delta_long = Q(1, 2) / proper_c_p
    zeta_required = 2 * threshold
    if delta_long != Q(358863, 2883949304 * 10**90):
        errors.append("long-leaf delta")
    if zeta_required != Q(460800, 5197322039):
        errors.append("long-leaf source fraction")
    if Q(1, 2) * zeta_required != threshold:
        errors.append("long-leaf aggregation")

    rows = []
    for terminal_time, k in ((0, 0), (0, 14), (1005, 3), (2011, 64)):
        blocks = (terminal_time + 1004) // 1005
        rows.append(
            {
                "terminal_time_H": terminal_time,
                "terminal_block_ceiling": blocks,
                "shell_k": k,
                "clock": terminal_time + 319590 + 1005 * k,
                "rational_majorant_power": 318 + blocks,
                "residual_shell_ratio_power": k,
            }
        )
    theorem = result.get("standard_Borel_whole_proper_family_shell_theorem", {})
    if theorem.get("sample_rows") != rows:
        errors.append("sample rows")
    if theorem.get("sample_rows_sha256") != cert.digest(rows):
        errors.append("sample digest")

    for i, j in ((0, 0), (0, 17), (5, 2), (64, 127)):
        maximum = max(i, j)
        if i + j > 2 * maximum:
            errors.append("max shell inequality")
        # e^(1/6)<6/5 is used symbolically; after this replacement the
        # exact rational residual is (3/5)^max.
        residual = Q(1, 2) ** maximum * Q(6, 5) ** maximum
        if residual != Q(3, 5) ** maximum or residual > 1:
            errors.append("intersection residual")
    return errors


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        if not path.is_file() or path.is_symlink():
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
        kernel = result.get("fixed_s_Borel_parent_survivor_kernel", {})
        if kernel.get("status") != (
            "CERTIFIED_FIXED_S_BOREL_PARENT_SURVIVOR_SUBKERNEL_SCHEMA"
        ):
            errors.append("kernel status")
        if "no joint-(s,component) atlas" not in kernel.get("parameter_scope", ""):
            errors.append("joint-s scope")
        if kernel.get("identical_fw_rev_survivor_asserted") is not False:
            errors.append("survivor equality overclaim")
        if kernel.get("common_shell_asserted") is not False:
            errors.append("common shell overclaim")
        if kernel.get("whole_proper_family_grouping_installed") is not False:
            errors.append("whole-family overclaim")
        if kernel.get("zero_survivor_policy") != (
            "h_sigma=0 is sent to cemetery and is never normalized"
        ):
            errors.append("zero survivor")

        stationary = result.get("stationary_Wdiag_union_mass_target_comparison", {})
        if stationary.get("status") != (
            "CERTIFIED_STATIONARY_MASS_TARGET_COMPARISON_ONLY"
        ):
            errors.append("stationary comparison")
        if stationary.get("core_count") != 8:
            errors.append("Wdiag core count")
        if stationary.get("union_collision_SRB_mass_strict_lower") != "7/89375":
            errors.append("Wdiag union field")
        if stationary.get("union_minus_threshold") != (
            "1214558021/35731589018125"
        ):
            errors.append("Wdiag excess field")
        if stationary.get("actual_beta_Wdiag_inferred") is not False:
            errors.append("stationary beta overclaim")
        if stationary.get("strict_inferable_beta_lower_from_this_comparison") != "0":
            errors.append("stationary beta lower")
        if stationary.get("numeric_mixing_or_disintegration_bridge_available") is not False:
            errors.append("stationary mixing overclaim")

        reduction = result.get("proper_family_long_leaf_target_cover_reduction", {})
        if reduction.get("status") != "CERTIFIED_LONG_LEAF_REDUCTION_ONLY":
            errors.append("long-leaf status")
        if reduction.get("delta_long") != str(
            Q(358863, 2883949304 * 10**90)
        ):
            errors.append("long-leaf delta field")
        if reduction.get("long_leaf_weight_lower") != "1/2":
            errors.append("long-leaf weight")
        if reduction.get(
            "required_per_long_leaf_Wdiag_crossing_source_fraction"
        ) != "460800/5197322039":
            errors.append("long-leaf crossing field")
        for key in (
            "reference_rectangle_or_long_leaf_atlas_installed",
            "finite_cover_rows_materialized",
            "per_long_leaf_crossing_mass_lower_available",
        ):
            if reduction.get(key) is not False:
                errors.append(f"long-leaf overclaim: {key}")
        if reduction.get("numeric_H_cover") is not None:
            errors.append("long-leaf H overclaim")
        if reduction.get("numeric_actual_beta_Wdiag") is not None:
            errors.append("long-leaf beta overclaim")
        if reduction.get("strict_inferable_actual_beta_lower") != "0":
            errors.append("long-leaf strict beta")

        theorem = result.get("standard_Borel_whole_proper_family_shell_theorem", {})
        if theorem.get("status") != (
            "CERTIFIED_CONDITIONAL_STANDARD_BOREL_WHOLE_FAMILY_SHELL_THEOREM"
        ):
            errors.append("Borel shell status")
        if theorem.get("this_extra_input_joined_to_Round35_leaf_kernel") is not False:
            errors.append("leaf/whole join overclaim")
        if theorem.get("numeric_H_available") is not False:
            errors.append("numeric H overclaim")
        if "no 9148 is added" not in theorem.get("one_step_route_clock_policy", ""):
            errors.append("9148 route")
        if "collision index of the terminal C24 test, inclusive" not in theorem.get(
            "terminal_time_contract", ""
        ):
            errors.append("terminal clock origin")
        if "(3/5)^k_sigma" not in theorem.get("pointwise_sharpening", ""):
            errors.append("pointwise sharpening")
        if "<2*(6/5)" not in theorem.get("orientation_separable_sum_bound", ""):
            errors.append("orientation sum")

        intersection = result.get(
            "same_ID_common_intersection_ambient_clock_moment", {}
        )
        if intersection.get("status") != (
            "CERTIFIED_BOREL_COMMON_INTERSECTION_MASS_AMBIENT_CLOCK_MOMENT"
        ):
            errors.append("intersection moment")
        if intersection.get("intersection_same_proper_class_return") != "NOT_CERTIFIED":
            errors.append("intersection return overclaim")
        if intersection.get("same_ID_joint_return_or_q_inferred") is not False:
            errors.append("intersection q overclaim")
        if intersection.get("what_the_clocks_recover") != (
            "the two ambient survivor families separately, not their intersection"
        ):
            errors.append("ambient clock type")

        counter = result.get("exact_nonpromotion_countermodels", {})
        if counter.get("common_intersection_inherits_properness") is not False:
            errors.append("intersection countermodel")
        if counter.get("marginal_survivor_moments_imply_parent_q_moment") is not False:
            errors.append("marginal countermodel")
        if counter.get("rows_sha256") != cert.digest(counter.get("rows", [])):
            errors.append("countermodel digest")

        frontier = result.get("corrected_frontier", {})
        if frontier.get("numeric_H_cover") is not None:
            errors.append("H overclaim")
        if frontier.get("numeric_actual_beta_Wdiag") is not None:
            errors.append("beta overclaim")
        for key in (
            "measurable_whole_proper_family_grouping_and_aggregate_Z",
            "same_ID_identical_fw_rev_survivor_and_common_shell",
            "intersection_same_proper_class_return",
            "complete_numeric_C_fw_C_rev_q",
            "strong_cemetery",
        ):
            if frontier.get(key) != "NOT_CERTIFIED":
                errors.append(f"frontier overclaim: {key}")

        strict = result.get("strict_nonpromotion", {})
        expected = {
            "fixed_s_Borel_parent_survivor_subkernel_schema": "CERTIFIED",
            "conditional_standard_Borel_whole_family_shell_theorem": "CERTIFIED",
            "common_intersection_mass_ambient_clock_moment": "CERTIFIED",
            "proper_family_long_leaf_target_cover_reduction": "CERTIFIED",
            "whole_proper_family_kernel_join": "NOT_CERTIFIED",
            "same_ID_two_orientation_postcut_return": "NOT_CERTIFIED",
            "numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if strict != expected:
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
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "parameter_scope"), "joint s"),
        (("result", "fixed_s_Borel_parent_survivor_kernel", "status"), "NOT_CERTIFIED"),
        (("result", "fixed_s_Borel_parent_survivor_kernel", "parameter_scope"), "joint-(s,c)"),
        (("result", "fixed_s_Borel_parent_survivor_kernel", "parent_kernel"), "not a kernel"),
        (("result", "fixed_s_Borel_parent_survivor_kernel", "survivor_subkernel"), "unknown"),
        (("result", "fixed_s_Borel_parent_survivor_kernel", "identical_fw_rev_survivor_asserted"), True),
        (("result", "fixed_s_Borel_parent_survivor_kernel", "common_shell_asserted"), True),
        (("result", "fixed_s_Borel_parent_survivor_kernel", "whole_proper_family_grouping_installed"), True),
        (("result", "fixed_s_Borel_parent_survivor_kernel", "zero_survivor_policy"), "normalize zero"),
        (("result", "stationary_Wdiag_union_mass_target_comparison", "status"), "CERTIFIED_MINORISATION"),
        (("result", "stationary_Wdiag_union_mass_target_comparison", "core_count"), 1),
        (("result", "stationary_Wdiag_union_mass_target_comparison", "union_collision_SRB_mass_strict_lower"), "1"),
        (("result", "stationary_Wdiag_union_mass_target_comparison", "union_minus_threshold"), "0"),
        (("result", "stationary_Wdiag_union_mass_target_comparison", "actual_beta_Wdiag_inferred"), True),
        (("result", "stationary_Wdiag_union_mass_target_comparison", "strict_inferable_beta_lower_from_this_comparison"), "7/89375"),
        (("result", "stationary_Wdiag_union_mass_target_comparison", "numeric_mixing_or_disintegration_bridge_available"), True),
        (("result", "proper_family_long_leaf_target_cover_reduction", "status"), "CERTIFIED_COVER"),
        (("result", "proper_family_long_leaf_target_cover_reduction", "delta_long"), "1"),
        (("result", "proper_family_long_leaf_target_cover_reduction", "long_leaf_weight_lower"), "1"),
        (("result", "proper_family_long_leaf_target_cover_reduction", "required_per_long_leaf_Wdiag_crossing_source_fraction"), "0"),
        (("result", "proper_family_long_leaf_target_cover_reduction", "reference_rectangle_or_long_leaf_atlas_installed"), True),
        (("result", "proper_family_long_leaf_target_cover_reduction", "finite_cover_rows_materialized"), True),
        (("result", "proper_family_long_leaf_target_cover_reduction", "per_long_leaf_crossing_mass_lower_available"), True),
        (("result", "proper_family_long_leaf_target_cover_reduction", "numeric_H_cover"), 1),
        (("result", "proper_family_long_leaf_target_cover_reduction", "numeric_actual_beta_Wdiag"), "1/22557"),
        (("result", "proper_family_long_leaf_target_cover_reduction", "strict_inferable_actual_beta_lower"), "1/22557"),
        (("result", "standard_Borel_whole_proper_family_shell_theorem", "status"), "NOT_CERTIFIED"),
        (("result", "standard_Borel_whole_proper_family_shell_theorem", "this_extra_input_joined_to_Round35_leaf_kernel"), True),
        (("result", "standard_Borel_whole_proper_family_shell_theorem", "eta"), "1"),
        (("result", "standard_Borel_whole_proper_family_shell_theorem", "terminal_time_contract"), "omit H"),
        (("result", "standard_Borel_whole_proper_family_shell_theorem", "one_step_route_clock_policy"), "add 9148"),
        (("result", "standard_Borel_whole_proper_family_shell_theorem", "pointwise_sharpening"), "factor 1"),
        (("result", "standard_Borel_whole_proper_family_shell_theorem", "orientation_separable_sum_bound"), "one copy"),
        (("result", "standard_Borel_whole_proper_family_shell_theorem", "numeric_H_available"), True),
        (("result", "standard_Borel_whole_proper_family_shell_theorem", "sample_rows"), []),
        (("result", "standard_Borel_whole_proper_family_shell_theorem", "sample_rows_sha256"), "0" * 64),
        (("result", "same_ID_common_intersection_ambient_clock_moment", "status"), "NOT_CERTIFIED"),
        (("result", "same_ID_common_intersection_ambient_clock_moment", "eta_pair"), "1"),
        (("result", "same_ID_common_intersection_ambient_clock_moment", "intersection_same_proper_class_return"), "CERTIFIED"),
        (("result", "same_ID_common_intersection_ambient_clock_moment", "same_ID_joint_return_or_q_inferred"), True),
        (("result", "same_ID_common_intersection_ambient_clock_moment", "what_the_clocks_recover"), "intersection"),
        (("result", "exact_nonpromotion_countermodels", "rows"), []),
        (("result", "exact_nonpromotion_countermodels", "rows_sha256"), "0" * 64),
        (("result", "exact_nonpromotion_countermodels", "common_intersection_inherits_properness"), True),
        (("result", "exact_nonpromotion_countermodels", "marginal_survivor_moments_imply_parent_q_moment"), True),
        (("result", "corrected_frontier", "numeric_H_cover"), 1),
        (("result", "corrected_frontier", "numeric_actual_beta_Wdiag"), "1/22557"),
        (("result", "corrected_frontier", "measurable_whole_proper_family_grouping_and_aggregate_Z"), "CERTIFIED"),
        (("result", "corrected_frontier", "same_ID_identical_fw_rev_survivor_and_common_shell"), "CERTIFIED"),
        (("result", "corrected_frontier", "intersection_same_proper_class_return"), "CERTIFIED"),
        (("result", "corrected_frontier", "complete_numeric_C_fw_C_rev_q"), "CERTIFIED"),
        (("result", "corrected_frontier", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "same_ID_two_orientation_postcut_return"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_H_cover_and_actual_beta"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_collision_time_q"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "strong_cemetery"), "CERTIFIED"),
    ]
    mutations: list[tuple[str, str]] = []
    for index, (keys, replacement) in enumerate(changes):
        mutation = copy.deepcopy(source)
        set_path(mutation, keys, replacement)
        mutations.append((f"mutation-{index}.json", json.dumps(mutation)))
    for key, replacement in (
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
    ):
        mutation = copy.deepcopy(source)
        mutation[key] = replacement
        mutations.append((f"mutation-{len(mutations)}.json", json.dumps(mutation)))
    duplicate = path.read_text(encoding="utf-8").rstrip()
    duplicate = duplicate[:-1] + ',"schema":"duplicate"}'
    mutations.append((f"mutation-{len(mutations)}.json", duplicate))

    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for name, body in mutations:
            target = Path(directory) / name
            target.write_text(body, encoding="utf-8")
            rejected += bool(verify(target))
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors = verify(args.manifest)
    if errors:
        print("AUDIT_MODE: FAIL")
        for error in errors:
            print(error)
        return 1
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
        return 0 if rejected == total else 1
    if args.integrity_only or args.replay:
        print("AUDIT_MODE: PASS")
        return 0
    print("AUDIT_MODE: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
