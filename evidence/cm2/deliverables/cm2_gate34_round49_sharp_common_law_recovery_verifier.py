#!/usr/bin/env python3
"""Fail-closed verifier for the Round-49 sharp common-law recovery layer."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round49_sharp_common_law_recovery_cert as cert


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


def expected_clock_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for terminal_time, k in ((0, 0), (0, 14), (696, 3), (1393, 64)):
        terminal_blocks = (terminal_time + 695) // 696
        rows.append(
            {
                "terminal_time_H": terminal_time,
                "terminal_block_ceiling": terminal_blocks,
                "shell_k": k,
                "clock": terminal_time + 221328 + 696 * k,
                "rational_majorant_power": 318 + terminal_blocks,
                "residual_shell_ratio_power": k,
            }
        )
    return rows


def independent_arithmetic(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    numerator = 360134800
    denominator = 360493663
    a = Q(numerator, denominator)

    if not 2 * numerator**695 > denominator**695:
        errors.append("695 predecessor comparison")
    if not 2 * numerator**696 < denominator**696:
        errors.append("696 half comparison")
    first = next(
        (ell for ell in range(1, 1006) if 2 * numerator**ell < denominator**ell),
        None,
    )
    if first != 696:
        errors.append("minimal half block")
    if 696 * 318 != 221328:
        errors.append("clock base")
    if Q(1, 4176) * 696 != Q(1, 6):
        errors.append("eta slope")
    if Q(1, 4176) * 221328 != 53:
        errors.append("eta base")
    if Q(1, 4176) / 6 != Q(1, 25056):
        errors.append("r6 gamma")
    if Q(1, 4176) / 12 != Q(1, 50112):
        errors.append("r12 gamma")
    if Q(1, 2) * Q(6, 5) != Q(3, 5):
        errors.append("shell residual")
    c_p = Q(4 * 10**90 * denominator, 358863)
    if Q(2 * 10**90) / (1 - a) != c_p / 2:
        errors.append("steady term")
    if a * c_p + Q(2 * 10**90) != (1 + a) * c_p / 2:
        errors.append("proper invariance identity")
    if not (1 + a) * c_p / 2 < c_p:
        errors.append("proper invariance strictness")
    if not 2**6 < 3**5:
        errors.append("2^(6/5)<3")
    # e=1+1+1/2+sum_(n>=3)1/n! < 5/2+1/4=11/4 because
    # n!>=2*3^(n-2) for n>=3.  The second exact comparison completes
    # exp(1/6)<6/5 without floating point.
    if not 11 * 5**6 < 4 * 6**6:
        errors.append("e rational majorant")
    factorial = 1
    for n in range(1, 25):
        factorial *= n
        if n >= 3 and factorial < 2 * 3 ** (n - 2):
            errors.append("factorial tail majorant")

    sharp = result.get("exact_sharp_closed_half_block", {})
    if sharp.get("shortest_positive_integer_L_with_a_power_below_half") != first:
        errors.append("sharp block field")
    if sharp.get("closed_Growth_coefficient_a") != str(a):
        errors.append("closed a field")

    rows = expected_clock_rows()
    shell = result.get("sharp_per_orientation_whole_family_shell_theorem", {})
    if shell.get("sample_rows") != rows:
        errors.append("clock sample rows")
    if shell.get("sample_rows_sha256") != cert.digest(rows):
        errors.append("clock sample digest")

    r_rows = [
        {
            "r": 6,
            "gamma": "1/25056",
            "holder_output": "integral c*W_6<=||c||_(6/5)*(1+2*A_H)^(1/6) for unit parent mass",
        },
        {
            "r": 12,
            "gamma": "1/50112",
            "holder_output": (
                "integral (c*W_12)^(12/11)<=(integral c^(6/5))^(10/11)*(1+2*A_H)^(1/11) for unit parent mass"
            ),
        },
    ]
    common = result.get("same_ID_common_parent_law_W_r_theorem", {})
    if common.get("r_instances") != r_rows:
        errors.append("r instances")
    if common.get("r_instances_sha256") != cert.digest(r_rows):
        errors.append("r digest")

    d1 = result.get("conditional_physical_D1_recovery_interface", {})
    k_rank = Q(
        3055930500533353804145008325576782226562500,
        453789,
    )
    if Q(d1.get("K_rank_exact", "0")) != k_rank:
        errors.append("D1 K_rank")
    tail = d1.get("tail_inputs", {})
    if Q(tail.get("A_tail", "0")) != Q(550000, 147):
        errors.append("D1 tail A")
    if Q(tail.get("r_tail", "0")) != Q(111718729, 111718750):
        errors.append("D1 tail r")

    grouping = result.get("whole_family_grouping_obstructions", {})
    finite = grouping.get("finite_mass_infinite_Z_countermodel", {})
    finite_rows = finite.get("rows", [])
    if finite.get("rows_sha256") != cert.digest(finite_rows):
        errors.append("finite-Z rows digest")
    if len(finite_rows) != 8:
        errors.append("finite-Z rows count")
    for n in range(1, 9):
        if Q(1, 4**n) / Q(1, 4**n) != 1:
            errors.append("finite-Z term")
    if sum(Q(1, 4**n) for n in range(1, 40)) >= Q(1, 3):
        errors.append("finite mass partial sum")

    defect = grouping.get(
        "finite_recordwise_J_no_global_clock_moment_countermodel", {}
    )
    defect_rows = defect.get("rows", [])
    if defect.get("rows_sha256") != cert.digest(defect_rows):
        errors.append("defect rows digest")
    if len(defect_rows) != 5:
        errors.append("defect rows count")
    for n in range(1, 6):
        count = 2 ** (n * n)
        length = Q(1, 2 ** (n * n))
        leaf_mass = Q(1, 2 ** (n + n * n))
        group_mass = count * leaf_mass
        numerator_J = count * leaf_mass / length
        if group_mass != Q(1, 2**n):
            errors.append("defect group mass")
        if numerator_J / group_mass != 2 ** (n * n):
            errors.append("defect ratio")

    intersection = result.get("intersection_and_cemetery_nonpromotion", {})
    inter_rows = intersection.get("rows", [])
    if intersection.get("rows_sha256") != cert.digest(inter_rows):
        errors.append("intersection rows digest")

    replay_copy = copy.deepcopy(result)
    stored_digest = replay_copy.pop("internal_replay_digest", None)
    if stored_digest != cert.digest(replay_copy):
        errors.append("internal replay digest")
    return errors


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        if not path.is_file() or path.is_symlink() or path.resolve().parent != cert.HERE:
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
        if not isinstance(result, dict):
            return errors + ["result type"]
        errors.extend(independent_arithmetic(result))

        sharp = result.get("exact_sharp_closed_half_block", {})
        if sharp.get("status") != "CERTIFIED_EXACT_SHORTEST_HALF_CONTRACTION_BLOCK":
            errors.append("sharp status")
        if sharp.get("former_1005_block_is_safe_but_not_minimal") is not True:
            errors.append("1005 minimality correction")
        if "whole positive survivor" not in sharp.get("proof_scope", ""):
            errors.append("sharp whole-family type")

        shell = result.get("sharp_per_orientation_whole_family_shell_theorem", {})
        if shell.get("status") != (
            "CERTIFIED_CONDITIONAL_SHARP_WHOLE_FAMILY_SHELL_THEOREM"
        ):
            errors.append("shell status")
        if shell.get("extra_input_joined_to_physical_arbitrary_Rn_leaf_kernel") is not False:
            errors.append("shell join overclaim")
        if shell.get("sharp_clock") != (
            "C_sigma(H,k)=H+696*(318+k)=H+221328+696*k"
        ):
            errors.append("sharp clock field")
        if shell.get("eta") != "1/4176":
            errors.append("eta field")
        if shell.get("postcut_whole_survivor_inheritance") != (
            "H_sigma(y) is the whole killed survivor family and Round47 gives Z(H_sigma)<=P*p(y) with P<2^317"
        ):
            errors.append("postcut survivor inheritance")
        if "no 9148" not in shell.get("one_step_route", ""):
            errors.append("9148 overcharge")
        if shell.get("rational_exponential_majorant") != (
            "e<11/4<(6/5)^6, hence exp(1/6)<6/5"
        ):
            errors.append("exponential majorant")
        if shell.get("numeric_H_cover_available") is not False:
            errors.append("H overclaim")
        if shell.get("fixed_H_scope") is not True:
            errors.append("fixed H scope")
        if "k_sigma=0 and C_sigma=0" not in shell.get("zero_survivor_policy", ""):
            errors.append("shell zero convention")

        common = result.get("same_ID_common_parent_law_W_r_theorem", {})
        if common.get("status") != (
            "CERTIFIED_CONDITIONAL_COMMON_PARENT_LAW_W_R_THEOREM"
        ):
            errors.append("common-law status")
        if common.get("hypotheses_installed_for_physical_arbitrary_Rn_registry") is not False:
            errors.append("common-law join overclaim")
        if common.get("parent_charged_once") is not True:
            errors.append("once charge")
        for key in (
            "identical_fw_rev_survivor_required",
            "common_shell_required",
            "proper_intersection_required",
        ):
            if common.get(key) is not False:
                errors.append(f"common-law false hypothesis: {key}")
        hypotheses = common.get("hypotheses", {})
        if "same m" not in hypotheses.get("single_common_parent_law", ""):
            errors.append("single common law")
        if "K_par(y,X)=p(y)=mass(G_y)" not in hypotheses.get(
            "finite_kernel_normalization", ""
        ):
            errors.append("kernel normalization")
        if "Z(H_sigma)<=P*p" not in hypotheses.get("aggregate_properness", ""):
            errors.append("survivor envelope")
        if "k_sigma=C_sigma=0" not in hypotheses.get("zero_survivor", ""):
            errors.append("zero survivor")
        if common.get("general_Holder_outputs") != [
            "integral c*W_6<=(integral c^(6/5))^(5/6)*((1+2*A_H)*integral p)^(1/6)",
            "integral (c*W_12)^(12/11)<=(integral c^(6/5))^(10/11)*((1+2*A_H)*integral p)^(1/11)",
        ]:
            errors.append("general Holder outputs")

        pair = result.get("synchronized_two_ambient_family_properness", {})
        if pair.get("status") != "CERTIFIED_SYNCHRONIZED_AMBIENT_PAIR_PROPERNESS_ONLY":
            errors.append("ambient pair status")
        for key in (
            "one_common_physical_survivor_inferred",
            "intersection_properness_inferred",
            "parent_weighted_exponential_moment_of_C_pair_inferred",
        ):
            if pair.get(key) is not False:
                errors.append(f"ambient pair overclaim: {key}")

        d1 = result.get("conditional_physical_D1_recovery_interface", {})
        if d1.get("status") != (
            "CERTIFIED_FORMULAS_CONDITIONAL_ON_MISSING_COMMON_LAW_JOIN"
        ):
            errors.append("D1 conditional status")
        if d1.get("missing_condition_installed") is not False:
            errors.append("D1 join overclaim")
        if "integral p dlambda=1" not in d1.get("normalization_scope", ""):
            errors.append("D1 normalization")
        if d1.get("general_mass_M0_once_charge_bound") != (
            "for M0=integral p dlambda, integral c0^(6/5)<M_D+3*M0"
        ):
            errors.append("D1 general mass")
        if d1.get("normalized_once_charge_bound") != (
            "integral c0^(6/5)<M_D+3"
        ):
            errors.append("D1 normalized mass")
        if d1.get("conditional_block_exponent") != "1/12":
            errors.append("D1 block exponent")
        if d1.get("D1_dominates_complete_C_fw_C_rev") is not False:
            errors.append("D1 domination overclaim")
        if d1.get("D1_recovery_tail_is_final_q_tail") is not False:
            errors.append("D1 q overclaim")
        if d1.get("strong_singular_corner_trace_cemetery") != "NOT_CERTIFIED":
            errors.append("D1 cemetery overclaim")

        grouping = result.get("whole_family_grouping_obstructions", {})
        if grouping.get("status") != (
            "CERTIFIED_EXACT_WHOLE_FAMILY_GROUPING_NONIMPLICATIONS"
        ):
            errors.append("grouping obstruction status")
        required = grouping.get("required_grouping_fields", {})
        for key in (
            "Borel_family_id",
            "exact_outer_disintegration_reconstructing_physical_mass",
            "physical_tail_or_exponential_moment_of_D_Z",
        ):
            if required.get(key) != "NOT_INSTALLED":
                errors.append(f"grouping overclaim: {key}")
        if required.get("defect_recovery_clock") != "696*D_Z(z)":
            errors.append("defect clock")

        intersection = result.get("intersection_and_cemetery_nonpromotion", {})
        if intersection.get("status") != (
            "CERTIFIED_EXACT_INTERSECTION_AND_CEMETERY_NONIMPLICATIONS"
        ):
            errors.append("intersection obstruction status")
        if intersection.get("full_intersection_proper") != "NOT_CERTIFIED":
            errors.append("intersection proper overclaim")
        if intersection.get("intersection_clock_moment") != "NOT_CERTIFIED":
            errors.append("intersection clock overclaim")
        if intersection.get("strong_cemetery_from_vanishing_discarded_mass") is not False:
            errors.append("mass cemetery overclaim")

        frontier = result.get("corrected_frontier", {})
        if frontier.get("numeric_H_cover") is not None:
            errors.append("frontier H overclaim")
        if frontier.get("numeric_actual_beta_Wdiag") is not None:
            errors.append("frontier beta overclaim")
        if frontier.get("strict_inferable_uniform_beta_lower") != "0":
            errors.append("frontier strict beta")
        for key in (
            "physical_arbitrary_Rn_whole_proper_family_grouping",
            "finite_J_and_physical_D_Z_tail",
            "full_same_ID_common_law_C_fw_C_rev_density_in_L6over5",
            "proper_common_fw_rev_intersection",
            "complete_numeric_C_fw_C_rev_q",
            "strong_singular_corner_trace_cemetery",
        ):
            if frontier.get(key) != "NOT_CERTIFIED":
                errors.append(f"frontier overclaim: {key}")

        expected_strict = {
            "exact_shortest_closed_half_block_696": "CERTIFIED",
            "sharp_clock_H_plus_221328_plus_696k": "CERTIFIED_CONDITIONAL_WHOLE_FAMILY",
            "common_parent_law_W_r_theorem": "CERTIFIED_CONDITIONAL_ABSTRACT",
            "D1_recovery_weighted_L12over11_and_tail": "CONDITIONAL_NOT_PHYSICALLY_JOINED",
            "whole_proper_family_kernel_join": "NOT_CERTIFIED",
            "numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if result.get("strict_nonpromotion") != expected_strict:
            errors.append("strict nonpromotion")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(path: Path) -> tuple[int, int]:
    source = read(path)
    changes: list[tuple[tuple[Any, ...], Any]] = [
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "old_artifacts_modified"), True),
        (("result", "provenance", "parameter_scope"), "joint all parameters"),
        (("result", "exact_sharp_closed_half_block", "status"), "NOT_CERTIFIED"),
        (("result", "exact_sharp_closed_half_block", "closed_Growth_coefficient_a"), "1"),
        (("result", "exact_sharp_closed_half_block", "exact_predecessor_comparison"), "false"),
        (("result", "exact_sharp_closed_half_block", "exact_sharp_comparison"), "false"),
        (("result", "exact_sharp_closed_half_block", "shortest_positive_integer_L_with_a_power_below_half"), 695),
        (("result", "exact_sharp_closed_half_block", "former_1005_block_is_safe_but_not_minimal"), False),
        (("result", "exact_sharp_closed_half_block", "steady_term_identity"), "0"),
        (("result", "exact_sharp_closed_half_block", "proof_scope"), "single leaf"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "status"), "NOT_CERTIFIED"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "extra_input_joined_to_physical_arbitrary_Rn_leaf_kernel"), True),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "conditional_extra_input"), "nonfinite kernel"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "postcut_whole_survivor_inheritance"), "missing"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "dyadic_shell"), "nonmeasurable"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "zero_survivor_policy"), "normalize zero"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "terminal_time_contract"), "omit H"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "sharp_clock"), "H+319590+1005*k"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "one_step_route"), "add 9148"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "eta"), "1/6030"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "A_H"), "1"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "rational_exponential_majorant"), "unsupported"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "pointwise_bound"), "false"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "integrated_bound"), "false"),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "fixed_H_scope"), False),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "numeric_H_cover_available"), True),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "sample_rows"), []),
        (("result", "sharp_per_orientation_whole_family_shell_theorem", "sample_rows_sha256"), "0" * 64),
        (("result", "same_ID_common_parent_law_W_r_theorem", "status"), "NOT_CERTIFIED"),
        (("result", "same_ID_common_parent_law_W_r_theorem", "hypotheses_installed_for_physical_arbitrary_Rn_registry"), True),
        (("result", "same_ID_common_parent_law_W_r_theorem", "hypotheses", "finite_kernel_normalization"), "K total arbitrary"),
        (("result", "same_ID_common_parent_law_W_r_theorem", "hypotheses", "aggregate_properness"), "parent only"),
        (("result", "same_ID_common_parent_law_W_r_theorem", "hypotheses", "zero_survivor"), "undefined clock"),
        (("result", "same_ID_common_parent_law_W_r_theorem", "definition"), "sum two laws"),
        (("result", "same_ID_common_parent_law_W_r_theorem", "pointwise_once_charge"), "double charge"),
        (("result", "same_ID_common_parent_law_W_r_theorem", "integrated_common_law_bound"), "unbounded"),
        (("result", "same_ID_common_parent_law_W_r_theorem", "parent_charged_once"), False),
        (("result", "same_ID_common_parent_law_W_r_theorem", "identical_fw_rev_survivor_required"), True),
        (("result", "same_ID_common_parent_law_W_r_theorem", "common_shell_required"), True),
        (("result", "same_ID_common_parent_law_W_r_theorem", "proper_intersection_required"), True),
        (("result", "same_ID_common_parent_law_W_r_theorem", "general_Holder_outputs"), []),
        (("result", "same_ID_common_parent_law_W_r_theorem", "r_instances"), []),
        (("result", "same_ID_common_parent_law_W_r_theorem", "r_instances_sha256"), "0" * 64),
        (("result", "synchronized_two_ambient_family_properness", "status"), "JOINT_RETURN"),
        (("result", "synchronized_two_ambient_family_properness", "common_ambient_clock"), "omit H"),
        (("result", "synchronized_two_ambient_family_properness", "one_common_physical_survivor_inferred"), True),
        (("result", "synchronized_two_ambient_family_properness", "intersection_properness_inferred"), True),
        (("result", "synchronized_two_ambient_family_properness", "parent_weighted_exponential_moment_of_C_pair_inferred"), True),
        (("result", "conditional_physical_D1_recovery_interface", "status"), "CERTIFIED_UNCONDITIONAL"),
        (("result", "conditional_physical_D1_recovery_interface", "K_rank_exact"), "0"),
        (("result", "conditional_physical_D1_recovery_interface", "N_open_numeric"), 1),
        (("result", "conditional_physical_D1_recovery_interface", "missing_condition_installed"), True),
        (("result", "conditional_physical_D1_recovery_interface", "normalization_scope"), "arbitrary mass"),
        (("result", "conditional_physical_D1_recovery_interface", "general_mass_M0_once_charge_bound"), "M_D+3"),
        (("result", "conditional_physical_D1_recovery_interface", "normalized_once_charge_bound"), "M_D"),
        (("result", "conditional_physical_D1_recovery_interface", "r6_L1_recovery_moment"), "false"),
        (("result", "conditional_physical_D1_recovery_interface", "r12_L12over11_moment"), "false"),
        (("result", "conditional_physical_D1_recovery_interface", "conditional_recovery_weighted_tail"), "false"),
        (("result", "conditional_physical_D1_recovery_interface", "conditional_block_exponent"), "1/6"),
        (("result", "conditional_physical_D1_recovery_interface", "D1_dominates_complete_C_fw_C_rev"), True),
        (("result", "conditional_physical_D1_recovery_interface", "D1_recovery_tail_is_final_q_tail"), True),
        (("result", "conditional_physical_D1_recovery_interface", "strong_singular_corner_trace_cemetery"), "CERTIFIED"),
        (("result", "whole_family_grouping_obstructions", "status"), "NO_OBSTRUCTION"),
        (("result", "whole_family_grouping_obstructions", "finite_mass_infinite_Z_countermodel", "aggregate_Z"), "finite"),
        (("result", "whole_family_grouping_obstructions", "finite_mass_infinite_Z_countermodel", "rows"), []),
        (("result", "whole_family_grouping_obstructions", "finite_mass_infinite_Z_countermodel", "rows_sha256"), "0" * 64),
        (("result", "whole_family_grouping_obstructions", "required_grouping_fields", "Borel_family_id"), "INSTALLED"),
        (("result", "whole_family_grouping_obstructions", "required_grouping_fields", "exact_outer_disintegration_reconstructing_physical_mass"), "INSTALLED"),
        (("result", "whole_family_grouping_obstructions", "required_grouping_fields", "defect_recovery_clock"), "1005*D"),
        (("result", "whole_family_grouping_obstructions", "required_grouping_fields", "physical_tail_or_exponential_moment_of_D_Z"), "INSTALLED"),
        (("result", "whole_family_grouping_obstructions", "finite_recordwise_J_no_global_clock_moment_countermodel", "moment_failure"), "summable"),
        (("result", "whole_family_grouping_obstructions", "finite_recordwise_J_no_global_clock_moment_countermodel", "rows"), []),
        (("result", "whole_family_grouping_obstructions", "finite_recordwise_J_no_global_clock_moment_countermodel", "rows_sha256"), "0" * 64),
        (("result", "intersection_and_cemetery_nonpromotion", "status"), "JOINT_RETURN"),
        (("result", "intersection_and_cemetery_nonpromotion", "full_intersection_proper"), "CERTIFIED"),
        (("result", "intersection_and_cemetery_nonpromotion", "uniform_intersection_boundary_numerator"), "CERTIFIED"),
        (("result", "intersection_and_cemetery_nonpromotion", "intersection_clock_moment"), "CERTIFIED"),
        (("result", "intersection_and_cemetery_nonpromotion", "strong_cemetery_from_vanishing_discarded_mass"), True),
        (("result", "intersection_and_cemetery_nonpromotion", "rows"), []),
        (("result", "intersection_and_cemetery_nonpromotion", "rows_sha256"), "0" * 64),
        (("result", "corrected_frontier", "numeric_H_cover"), 1),
        (("result", "corrected_frontier", "numeric_actual_beta_Wdiag"), "1/22557"),
        (("result", "corrected_frontier", "strict_inferable_uniform_beta_lower"), "1/22557"),
        (("result", "corrected_frontier", "physical_arbitrary_Rn_whole_proper_family_grouping"), "CERTIFIED"),
        (("result", "corrected_frontier", "finite_J_and_physical_D_Z_tail"), "CERTIFIED"),
        (("result", "corrected_frontier", "full_same_ID_common_law_C_fw_C_rev_density_in_L6over5"), "CERTIFIED"),
        (("result", "corrected_frontier", "proper_common_fw_rev_intersection"), "CERTIFIED"),
        (("result", "corrected_frontier", "complete_numeric_C_fw_C_rev_q"), "CERTIFIED"),
        (("result", "corrected_frontier", "strong_singular_corner_trace_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "whole_proper_family_kernel_join"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_H_cover_and_actual_beta"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_numeric_C_fw_C_rev"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_collision_time_q"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "5/5"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "Gate4"), "CERTIFIED"),
        (("verdict", "CM2"), "GO"),
    ]

    mutations: list[tuple[str, str]] = []
    for index, (keys, replacement) in enumerate(changes):
        mutation = copy.deepcopy(source)
        set_path(mutation, keys, replacement)
        mutations.append((f"mutation-{index}.json", json.dumps(mutation)))
    for key, replacement in (
        ("schema", "bad"),
        ("certificate_sha256", "0" * 64),
        ("verifier_sha256", "0" * 64),
        ("dependencies", {}),
        ("result", {}),
        ("verdict", {}),
    ):
        mutation = copy.deepcopy(source)
        mutation[key] = replacement
        mutations.append((f"mutation-{len(mutations)}.json", json.dumps(mutation)))
    duplicate = path.read_text(encoding="utf-8").rstrip()
    duplicate = duplicate[:-1] + ',"schema":"duplicate"}'
    mutations.append((f"mutation-{len(mutations)}.json", duplicate))

    rejected = 0
    # Production verification accepts manifests only directly inside HERE.
    # Put each hostile fixture there temporarily so mutations reach all
    # replay/field checks instead of being rejected early as an unsafe path.
    for name, body in mutations:
        del name
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=".cm2-r49-hostile-",
            suffix=".json",
            dir=cert.HERE,
            delete=False,
        )
        target = Path(handle.name)
        try:
            with handle:
                handle.write(body)
            mutation_errors = verify(target)
            # An early path-safety rejection would make the hostile suite an
            # empty test.  Count only mutations that reached substantive
            # manifest/replay/field validation (duplicate-key parse failures
            # are substantive exceptions, not path failures).
            rejected += bool(
                mutation_errors and mutation_errors != ["unsafe manifest"]
            )
        finally:
            target.unlink(missing_ok=True)
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=cert.DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--independent-arithmetic-only", action="store_true")
    args = parser.parse_args()

    if args.independent_arithmetic_only:
        result = cert.build_result()
        errors = independent_arithmetic(result)
        if errors:
            print("INDEPENDENT_ARITHMETIC: FAIL")
            for error in errors:
                print(error)
            return 1
        print("INDEPENDENT_ARITHMETIC: PASS")
        return 0

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
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
