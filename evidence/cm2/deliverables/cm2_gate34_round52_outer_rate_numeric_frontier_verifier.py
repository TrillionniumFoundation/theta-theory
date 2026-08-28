#!/usr/bin/env python3
"""Fail-closed verifier for the Round-52 Gate-4 outer-rate frontier."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round52_outer_rate_numeric_frontier_cert as cert


EXPECTED_MANIFEST_KEYS = {
    "schema",
    "certificate_sha256",
    "verifier_sha256",
    "dependencies",
    "result",
    "verdict",
}


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate key: {key}")
        value[key] = item
    return value


def reject_json_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def read(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_json_constant,
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


def independent_arithmetic(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    hit = Q(21, 111718750)
    bump_norm = Q(2724)
    c_hat = Q(20, 3807)
    expansion = Q(180337, 144000)
    rate = Q(9, 10)
    outer_c = Q(3807, 10)

    if 2 / c_hat != outer_c:
        errors.append("outer C arithmetic")
    if not (1 / c_hat > 2 > 1):
        errors.append("prefactor dominance")
    if not (1 / expansion < rate**2):
        errors.append("safe square-root rate")
    if 144000 * 100 >= 81 * 180337:
        errors.append("integer square comparison")
    if bump_norm * outer_c / hit != Q(38618445937500, 7):
        errors.append("scale ratio")
    if bump_norm * outer_c * Q(3, 4) != Q(7777701, 10):
        errors.append("non-effectivity floor")
    if Q(1999, 32000) * Q(2688, 893303125) != hit:
        errors.append("direct cover threshold")

    axis_base = 4 * (Q(9, 25) + Q(4, 25)) * Q(3, 250) * Q(3, 500)
    diagonal_base = 8 * (Q(9, 25) + Q(4, 25)) * Q(3, 250) * Q(3, 50)
    if axis_base != Q(117, 781250):
        errors.append("outer axis support base")
    if diagonal_base != Q(234, 78125):
        errors.append("outer diagonal support base")
    if not (Q(1001, 1000) ** 2 * (1 - Q(21, 1000) ** 2) > 1):
        errors.append("outer axis derivative")
    if not (Q(141, 100) ** 2 * (1 - Q(701, 1000) ** 2) > 1):
        errors.append("outer diagonal derivative")
    outer_raw = axis_base * Q(1001, 1000) + diagonal_base * Q(141, 100)
    outer_mass = outer_raw / Q(156, 25)
    if outer_raw != Q(3416517, 781250000):
        errors.append("outer raw mass")
    if outer_mass != Q(87603, 125000000) or not outer_mass < Q(1, 1000):
        errors.append("outer normalized mass")
    if Q(25, 4) * 1000 + 1000 != 7250:
        errors.append("outer axis Lipschitz")
    if Q(25, 4) * 1000 + 100 != 6350:
        errors.append("outer diagonal Lipschitz")

    sample = cert.conditional_block_time(Q(1, 2), 1)
    if sample["minimal_safe_block_count_m"] != 140:
        errors.append("conditional sample m")
    if sample["safe_collision_time_H"] != 280:
        errors.append("conditional sample H")
    scale = bump_norm * outer_c
    if not (scale * Q(3, 4) ** 140 < hit):
        errors.append("sample coupling pass")
    if not (scale * rate**280 < hit):
        errors.append("sample hyperbolic pass")
    if scale * rate**278 < hit:
        errors.append("sample previous should fail")

    outer = result.get("proof_level_outer_rate", {})
    numeric = outer.get("numeric_hyperbolicity", {})
    if numeric.get("hat_c") != str(c_hat):
        errors.append("hat_c field")
    if numeric.get("Lambda") != str(expansion):
        errors.append("Lambda field")
    if numeric.get("safe_Lambda_inverse_square_root_upper") != str(rate):
        errors.append("rate field")
    prefactor = outer.get("numeric_outer_prefactor", {})
    if prefactor.get("C_bump_proof_outer_upper") != str(outer_c):
        errors.append("outer C field")

    interface = result.get("two_scalar_effectivity_interface", {})
    rows = interface.get("missing_rate_scalars", [])
    if [row.get("id") for row in rows] != ["tilde_zeta_lower", "Delta_upper"]:
        errors.append("missing scalar ids")
    if any(row.get("value", "bad") is not None for row in rows):
        errors.append("missing scalar overclaim")
    if interface.get("missing_rate_scalars_sha256") != cert.digest(rows):
        errors.append("missing scalar digest")
    if interface.get("formal_arithmetic_sample_not_a_physical_claim") != sample:
        errors.append("sample replay")

    majorant = result.get(
        "uniform_C24_outer_majorant_and_common_terminal_survivor", {}
    )
    support = majorant.get("support_mass", {})
    if support.get("padded_union_unnormalized_mass_strict_upper_by_sum") != str(
        outer_raw
    ):
        errors.append("outer raw field")
    if support.get("mu_s_support_strict_upper") != str(outer_mass):
        errors.append("outer mass field")
    construction = majorant.get("construction", {})
    box_rows = construction.get("box_rows", [])
    if construction.get("box_rows_sha256") != cert.digest(box_rows):
        errors.append("outer box digest")
    if sum(row.get("count", 0) for row in box_rows) != 24:
        errors.append("outer box count")

    literature = result.get("latest_technology_audit", {})
    rows_lit = literature.get("rows", [])
    if literature.get("rows_sha256") != cert.digest(rows_lit):
        errors.append("literature digest")
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
        if set(source) != EXPECTED_MANIFEST_KEYS:
            errors.append("manifest keys")
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
        if isinstance(result, dict):
            payload = dict(result)
            stored = payload.pop("internal_replay_digest", None)
            if stored != cert.digest(payload):
                errors.append("internal replay digest")
        else:
            errors.append("result root")
            result = {}
        errors.extend(independent_arithmetic(result))

        provenance = result.get("provenance", {})
        if provenance.get("dependency_sha256") != cert.DEPENDENCIES:
            errors.append("provenance dependencies")
        if provenance.get("old_artifacts_modified") is not False:
            errors.append("old artifact mutation")

        outer = result.get("proof_level_outer_rate", {})
        if outer.get("status") != (
            "CERTIFIED_NUMERIC_OUTER_PREFACTOR_AND_TWO_SCALAR_RATE_REDUCTION"
        ):
            errors.append("outer status")
        proper = outer.get("proper_start_scope_reduction", {})
        if proper.get("status") != (
            "CERTIFIED_EXISTENTIAL_PROPER_REPRESENTATION_REDUCTION"
        ):
            errors.append("proper representation status")
        if proper.get("no_numeric_regularisation_shift_added_to_H") is not True:
            errors.append("regularisation shift")
        formula = outer.get("proof_level_formula_gamma_1", {})
        if formula.get("immediately_preceding_hyperbolic_decay") != (
            "2*Lip_1(f)*hat_c^(-1)*Lambda^(-n/2)"
        ):
            errors.append("preceding hyperbolic estimate")
        if formula.get("printed_final_hyperbolic_factor") != "Lambda^(-1)/2":
            errors.append("printed factor audit")
        if formula.get("safe_extracted_hyperbolic_rate") != "Lambda^(-1/2)":
            errors.append("safe rate extraction")
        if formula.get("printed_factor_used") is not False:
            errors.append("printed rate misuse")
        prefactor = outer.get("numeric_outer_prefactor", {})
        if prefactor.get("status") != "CERTIFIED_NUMERIC_PROOF_OUTER_PREFACTOR":
            errors.append("prefactor status")
        if outer.get("safe_rate_with_two_hidden_scalars") != (
            "theta_safe=max((1-tilde_zeta/2)^(1/(2*Delta)),9/10)"
        ):
            errors.append("safe rate formula")

        interface = result.get("two_scalar_effectivity_interface", {})
        if interface.get("status") != (
            "TWO_SCALAR_EFFECTIVITY_INTERFACE_EXACT_BUT_INPUTS_NOT_NUMERIC"
        ):
            errors.append("interface status")
        for key in (
            "numeric_tilde_zeta_lower",
            "numeric_Delta_upper",
            "numeric_H_bump",
        ):
            if interface.get(key) is not None:
                errors.append(f"interface overclaim: {key}")
        if "H=2*D*m is safe" not in interface.get(
            "exact_conditional_integer_interface", ""
        ):
            errors.append("conditional integer interface")

        majorant = result.get(
            "uniform_C24_outer_majorant_and_common_terminal_survivor", {}
        )
        if majorant.get("status") != (
            "CERTIFIED_NUMERIC_OUTER_MAJORANT_AND_EXISTENTIAL_COMMON_TERMINAL_SURVIVOR"
        ):
            errors.append("outer majorant status")
        construction = majorant.get("construction", {})
        if construction.get("global_function") != (
            "g_out=max of the twenty-four one-box products"
        ):
            errors.append("outer majorant construction")
        if construction.get("pointwise_relation") != "1_C24<=g_out<=1":
            errors.append("outer majorant pointwise")
        if construction.get("axis_padding") != {"t": "1/1000", "p": "1/1000"}:
            errors.append("outer axis padding")
        if construction.get("diagonal_padding") != {"t": "1/1000", "p": "1/100"}:
            errors.append("outer diagonal padding")
        support = majorant.get("support_mass", {})
        if support.get("simple_uniform_upper") != "1/1000":
            errors.append("outer simple mass")
        lipschitz = majorant.get("Lipschitz_bound", {})
        if lipschitz.get("norm_infinity_plus_Lip_1_strict_upper") != "7251":
            errors.append("outer theorem norm")
        if lipschitz.get(
            "finite_max_preserves_maximum_Lipschitz_constant"
        ) is not True:
            errors.append("outer max Lipschitz")
        terminal = majorant.get("uniform_existential_small_terminal_hit", {})
        if "absolute common nonhit mass is >249*p/250" not in terminal.get(
            "normalization_scope", ""
        ):
            errors.append("terminal parent-mass normalization scope")
        if terminal.get("status") != (
            "CERTIFIED_UNIFORM_EXISTENTIAL_TIME_COMMON_TERMINAL_NONHIT"
        ):
            errors.append("terminal survivor status")
        if terminal.get("numeric_H_out") is not None:
            errors.append("H_out overclaim")
        if terminal.get("per_proper_view_terminal_C24_mass_strict_upper") != "1/500":
            errors.append("per-view terminal loss")
        if terminal.get("same_parent_common_terminal_nonhit_mass_strict_lower") != "249/250":
            errors.append("common terminal survivor")
        scope = majorant.get("strict_scope", {})
        if scope.get("terminal_test_only") is not True:
            errors.append("terminal-only scope")
        if scope.get("intermediate_C24_avoidance") != "NOT_CERTIFIED":
            errors.append("intermediate avoidance overclaim")
        if scope.get("properness_of_common_nonhit_restriction") != "NOT_CERTIFIED":
            errors.append("common restriction overclaim")
        if scope.get("proper_same_ID_fw_rev_return") != "NOT_CERTIFIED":
            errors.append("proper return overclaim")

        obstruction = result.get("sharp_non_effectivity", {})
        if obstruction.get("status") != (
            "CERTIFIED_SHARP_TWO_SCALAR_NONEFFECTIVITY_OF_AVAILABLE_PROOF_DATA"
        ):
            errors.append("non-effectivity status")
        if obstruction.get(
            "both_numeric_rows_are_individually_necessary_for_this_proof_route"
        ) is not True:
            errors.append("individual necessity")
        if obstruction.get("majorant_still_exceeds_required_gap") is not True:
            errors.append("majorant gap")
        if "not physical billiard counterexamples" not in obstruction.get(
            "logical_scope", ""
        ):
            errors.append("logical scope")

        separation = result.get("H_bump_H_cover_beta_type_separation", {})
        if separation.get("status") != (
            "CERTIFIED_OBJECT_TYPE_SEPARATION_NO_COVER_PROMOTION"
        ):
            errors.append("type separation status")
        if separation.get("numeric_H_bump_cannot_be_renamed_H_cover") is not True:
            errors.append("H rename guard")
        cover = separation.get("sufficient_rectangles_route", {})
        if cover.get("actual_numeric_fraction") is not None:
            errors.append("cover fraction overclaim")
        if cover.get("strict_inferable_lower") != "0":
            errors.append("cover strict lower")
        if separation.get("numeric_H_cover") is not None:
            errors.append("H_cover overclaim")
        if separation.get("numeric_beta") is not None:
            errors.append("beta overclaim")

        tech = result.get("latest_technology_audit", {})
        if tech.get("newer_official_numeric_rate_or_cover_theorem_found") is not False:
            errors.append("technology overclaim")
        if tech.get("rows") != cert.literature_audit()["rows"]:
            errors.append("technology rows")

        corrected = result.get("corrected_frontier", {})
        expected_corrected = {
            "numeric_C_bump_proof_outer_upper": "3807/10",
            "numeric_safe_hyperbolic_rate_upper": "9/10",
            "numeric_tilde_zeta_lower": None,
            "numeric_Delta_upper": None,
            "numeric_theta_bump": None,
            "numeric_H_bump": None,
            "numeric_outer_majorant_mass_upper": "87603/125000000",
            "numeric_outer_majorant_theorem_norm_upper": "7251",
            "uniform_existential_H_out": "CERTIFIED_NONNUMERIC",
            "numeric_H_out": None,
            "same_parent_common_terminal_nonhit_mass": "relative fraction >249/250 (absolute mass >249*p/250)",
            "proper_common_terminal_nonhit_restriction": "NOT_CERTIFIED",
            "numeric_H_cover": None,
            "numeric_beta": None,
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
        }
        if corrected != expected_corrected:
            errors.append("corrected frontier")

        expected_verdict = {
            "numeric_proof_outer_C_bump_upper": "CERTIFIED_3807/10",
            "safe_hyperbolic_rate_upper": "CERTIFIED_9/10",
            "numeric_magnet_tilde_zeta_Delta": "NOT_CERTIFIED",
            "numeric_H_bump": "NOT_CERTIFIED",
            "uniform_existential_common_terminal_nonhit": "CERTIFIED_RELATIVE_FRACTION_>249/250",
            "numeric_H_out": "NOT_CERTIFIED",
            "proper_common_terminal_nonhit_restriction": "NOT_CERTIFIED",
            "uniform_numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if result.get("strict_nonpromotion") != expected_verdict:
            errors.append("strict nonpromotion")
    except Exception as exc:
        errors.append(f"exception: {exc}")
    return errors


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(path: Path) -> tuple[int, int]:
    source = read(path)
    changes: list[tuple[tuple[Any, ...], Any]] = [
        (("schema",), "bad"),
        (("certificate_sha256",), "0" * 64),
        (("verifier_sha256",), "0" * 64),
        (("dependencies",), {}),
        (("result", "schema"), "bad"),
        (("result", "internal_replay_digest"), "0" * 64),
        (("result", "provenance", "old_artifacts_modified"), True),
        (("result", "provenance", "claim_type"), "full closure"),
        (("result", "proof_level_outer_rate", "status"), "NUMERIC_H"),
        (("result", "proof_level_outer_rate", "official_source", "main_member_sha256"), "0" * 64),
        (("result", "proof_level_outer_rate", "proper_start_scope_reduction", "status"), "NOT_CERTIFIED"),
        (("result", "proof_level_outer_rate", "proper_start_scope_reduction", "no_numeric_regularisation_shift_added_to_H"), False),
        (("result", "proof_level_outer_rate", "proof_level_formula_gamma_1", "published_outer_prefactor_formula"), "C=1"),
        (("result", "proof_level_outer_rate", "proof_level_formula_gamma_1", "immediately_preceding_hyperbolic_decay"), "Lambda^-n"),
        (("result", "proof_level_outer_rate", "proof_level_formula_gamma_1", "printed_final_hyperbolic_factor"), "Lambda^(-1/2)"),
        (("result", "proof_level_outer_rate", "proof_level_formula_gamma_1", "safe_extracted_hyperbolic_rate"), "Lambda^(-1)/2"),
        (("result", "proof_level_outer_rate", "proof_level_formula_gamma_1", "printed_factor_used"), True),
        (("result", "proof_level_outer_rate", "numeric_hyperbolicity", "hat_c"), "1"),
        (("result", "proof_level_outer_rate", "numeric_hyperbolicity", "Lambda"), "1"),
        (("result", "proof_level_outer_rate", "numeric_hyperbolicity", "Lambda_inverse"), "1"),
        (("result", "proof_level_outer_rate", "numeric_hyperbolicity", "safe_Lambda_inverse_square_root_upper"), "4/5"),
        (("result", "proof_level_outer_rate", "numeric_outer_prefactor", "hat_c_inverse"), "1"),
        (("result", "proof_level_outer_rate", "numeric_outer_prefactor", "C_bump_proof_outer_upper"), "1"),
        (("result", "proof_level_outer_rate", "numeric_outer_prefactor", "status"), "NOT_CERTIFIED"),
        (("result", "proof_level_outer_rate", "safe_rate_with_two_hidden_scalars"), "theta=1/2"),
        (("result", "two_scalar_effectivity_interface", "known_exact_scale_ratio_2724_C_over_epsilon"), "1"),
        (("result", "two_scalar_effectivity_interface", "missing_rate_scalars_sha256"), "0" * 64),
        (("result", "two_scalar_effectivity_interface", "missing_rate_scalars", 0, "id"), "zeta"),
        (("result", "two_scalar_effectivity_interface", "missing_rate_scalars", 0, "value"), "1/2"),
        (("result", "two_scalar_effectivity_interface", "missing_rate_scalars", 1, "value"), 1),
        (("result", "two_scalar_effectivity_interface", "formal_arithmetic_sample_not_a_physical_claim", "minimal_safe_block_count_m"), 139),
        (("result", "two_scalar_effectivity_interface", "formal_arithmetic_sample_not_a_physical_claim", "safe_collision_time_H"), 1),
        (("result", "two_scalar_effectivity_interface", "numeric_tilde_zeta_lower"), "1/2"),
        (("result", "two_scalar_effectivity_interface", "numeric_Delta_upper"), 1),
        (("result", "two_scalar_effectivity_interface", "numeric_H_bump"), 280),
        (("result", "two_scalar_effectivity_interface", "status"), "CLOSED"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "status"), "NOT_CERTIFIED"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "construction", "global_function"), "sum"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "construction", "pointwise_relation"), "g_out<=1_C24"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "construction", "box_rows_sha256"), "0" * 64),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "construction", "box_rows", 0, "count"), 5),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "support_mass", "mu_s_support_strict_upper"), "1/2"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "support_mass", "simple_uniform_upper"), "1/8"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "Lipschitz_bound", "norm_infinity_plus_Lip_1_strict_upper"), "1"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "uniform_existential_small_terminal_hit", "numeric_H_out"), 1),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "uniform_existential_small_terminal_hit", "normalization_scope"), "absolute mass >249/250 for every parent"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "uniform_existential_small_terminal_hit", "per_proper_view_terminal_C24_mass_strict_upper"), "1"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "uniform_existential_small_terminal_hit", "same_parent_common_terminal_nonhit_mass_strict_lower"), "0"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "strict_scope", "terminal_test_only"), False),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "strict_scope", "intermediate_C24_avoidance"), "CERTIFIED"),
        (("result", "uniform_C24_outer_majorant_and_common_terminal_survivor", "strict_scope", "properness_of_common_nonhit_restriction"), "CERTIFIED"),
        (("result", "sharp_non_effectivity", "no_Delta_upper_model"), "false"),
        (("result", "sharp_non_effectivity", "no_zeta_lower_model"), "false"),
        (("result", "sharp_non_effectivity", "corresponding_RHS_majorant_strict_lower"), "0"),
        (("result", "sharp_non_effectivity", "majorant_still_exceeds_required_gap"), False),
        (("result", "sharp_non_effectivity", "logical_scope"), "physical counterexample"),
        (("result", "sharp_non_effectivity", "both_numeric_rows_are_individually_necessary_for_this_proof_route"), False),
        (("result", "sharp_non_effectivity", "status"), "NOT_CERTIFIED"),
        (("result", "H_bump_H_cover_beta_type_separation", "status"), "CONVERTED"),
        (("result", "H_bump_H_cover_beta_type_separation", "numeric_H_bump_cannot_be_renamed_H_cover"), False),
        (("result", "H_bump_H_cover_beta_type_separation", "sufficient_rectangles_route", "required_per_leaf_direct_fraction"), "0"),
        (("result", "H_bump_H_cover_beta_type_separation", "sufficient_rectangles_route", "actual_numeric_fraction"), "1"),
        (("result", "H_bump_H_cover_beta_type_separation", "sufficient_rectangles_route", "strict_inferable_lower"), "1"),
        (("result", "H_bump_H_cover_beta_type_separation", "numeric_H_cover"), 280),
        (("result", "H_bump_H_cover_beta_type_separation", "numeric_beta"), "1"),
        (("result", "latest_technology_audit", "rows_sha256"), "0" * 64),
        (("result", "latest_technology_audit", "rows", 0, "main_member_sha256"), "0" * 64),
        (("result", "latest_technology_audit", "rows", 1, "finding"), "numeric magnet"),
        (("result", "latest_technology_audit", "newer_official_numeric_rate_or_cover_theorem_found"), True),
        (("result", "corrected_frontier", "numeric_C_bump_proof_outer_upper"), "1"),
        (("result", "corrected_frontier", "numeric_safe_hyperbolic_rate_upper"), "1/2"),
        (("result", "corrected_frontier", "numeric_tilde_zeta_lower"), "1/2"),
        (("result", "corrected_frontier", "numeric_Delta_upper"), 1),
        (("result", "corrected_frontier", "numeric_theta_bump"), "1/2"),
        (("result", "corrected_frontier", "numeric_H_bump"), 280),
        (("result", "corrected_frontier", "numeric_outer_majorant_mass_upper"), "1"),
        (("result", "corrected_frontier", "numeric_H_out"), 1),
        (("result", "corrected_frontier", "same_parent_common_terminal_nonhit_mass"), "1"),
        (("result", "corrected_frontier", "proper_common_terminal_nonhit_restriction"), "CERTIFIED"),
        (("result", "corrected_frontier", "numeric_H_cover"), 280),
        (("result", "corrected_frontier", "numeric_beta"), "1"),
        (("result", "corrected_frontier", "complete_numeric_C_fw_C_rev_q"), "CERTIFIED"),
        (("result", "corrected_frontier", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_proof_outer_C_bump_upper"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_magnet_tilde_zeta_Delta"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_H_bump"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "uniform_existential_common_terminal_nonhit"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_H_out"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "proper_common_terminal_nonhit_restriction"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "uniform_numeric_H_cover_and_actual_beta"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "1/5"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "Gate4"), "CERTIFIED"),
        (("verdict", "CM2"), "GO"),
    ]
    bodies: list[str] = []
    for field_path, replacement in changes:
        mutation = copy.deepcopy(source)
        set_path(mutation, field_path, replacement)
        bodies.append(json.dumps(mutation, sort_keys=True) + "\n")
    bodies.append('{"schema":"x","schema":"y"}\n')
    extra = copy.deepcopy(source)
    extra["unexpected"] = 1
    bodies.append(json.dumps(extra, sort_keys=True) + "\n")
    valid = json.dumps(source, sort_keys=True)
    bodies.append(valid[:-1] + ',"unexpected":NaN}\n')

    passed = 0
    for body in bodies:
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=".cm2-r52-outer-rate-hostile-",
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
    return passed, len(bodies)


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
