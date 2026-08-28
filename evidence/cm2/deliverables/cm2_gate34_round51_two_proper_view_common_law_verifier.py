#!/usr/bin/env python3
"""Fail-closed verifier for the Round-51 two-proper-view common-law leaf."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round51_two_proper_view_common_law_cert as cert


TOP_LEVEL_KEYS = {
    "schema",
    "certificate_sha256",
    "verifier_sha256",
    "dependencies",
    "result",
    "verdict",
}


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def read(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    if set(value) != TOP_LEVEL_KEYS:
        raise ValueError("manifest exact top-level keys")
    return value


def expected_view_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for M in (0, 14, 310, 311, 319, 400):
        defect = cert.safe_defect(M)
        stopped = 696 * defect
        rows.append(
            {
                "minimum_length_rank_M": M,
                "safe_defect_Dbar": defect,
                "stopped_time_R0": stopped,
                "forward_view_map": f"P_fw=T_s^{stopped} o V_fw",
                "reverse_view_map": f"P_rev=T_s^{stopped} o V_rev",
                "inverse_time_exponent": -stopped,
            }
        )
    return rows


def expected_counter_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in (19, 20, 21, 22, 24):
        M = n * n
        defect = cert.safe_defect(M)
        rows.append(
            {
                "band_n": n,
                "band_mass": f"2^-{n}",
                "group_count": f"2^{M}",
                "group_length": f"2^-{M}",
                "minimum_length_rank_M": M,
                "safe_defect_Dbar": defect,
                "tail_test_m": M - 1,
                "mass_over_2^-m_lower_ratio": f"2^{M-n-1}",
                "rational_moment_band_term": f"2^-{n}*(6/5)^{defect}",
            }
        )
    return rows


def independent_arithmetic(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    cp = Q(4 * 10**90 * 360493663, 358863)
    closed_a = Q(360134800, 360493663)
    if Q(2 * 10**90) / (1 - closed_a) != cp / 2:
        errors.append("closed steady term")
    if not Q(2**310) < cp < Q(2**311):
        errors.append("C_p dyadic bracket")
    if Q(696, 4176) != Q(1, 6):
        errors.append("preclock exponent")
    if not 11 * 5**6 < 4 * 6**6:
        errors.append("exp upper rational comparison")
    if not Q(7, 6) < Q(6, 5):
        errors.append("exp lower witness comparison")

    for M in range(0, 701):
        defect = cert.safe_defect(M)
        if M <= 310:
            if defect != 0 or not Q(2**M) < cp:
                errors.append(f"defect low formula {M}")
        else:
            if defect != M - 309:
                errors.append(f"defect high formula {M}")
            if not Q(2**M, 2**defect) < cp / 2:
                errors.append(f"defect safety {M}")
            if not Q(2**M, 2 ** (defect - 1)) >= cp / 2:
                errors.append(f"defect minimality {M}")

    a = Q(6, 5)
    first_two = (a**2 - 1) * Q(1, 2**310)
    geometric_tail = Q(1, 2**309) * (a - 1) * (a / 2) ** 2 / (1 - a / 2)
    if (first_two + geometric_tail) * Q(2**310) != Q(4, 5):
        errors.append("sharp shifted layer cake coefficient")
    if a / 2 != Q(3, 5):
        errors.append("tail geometric ratio")

    obj = result.get("physical_two_proper_view_object_lemma", {})
    view_rows = expected_view_rows()
    if obj.get("sample_view_map_rows") != view_rows:
        errors.append("view rows")
    if obj.get("sample_view_map_rows_sha256") != cert.digest(view_rows):
        errors.append("view rows digest")

    counter = result.get("short_tail_nonimplication", {})
    counter_rows = expected_counter_rows()
    if counter.get("rows") != counter_rows:
        errors.append("counter rows")
    if counter.get("rows_sha256") != cert.digest(counter_rows):
        errors.append("counter rows digest")
    previous_ratio_exponent = -1
    for row in counter_rows:
        n = row["band_n"]
        M = n * n
        if Q(1, 2**n) / Q(1, 2 ** (M - 1)) != Q(2 ** (M - n - 1)):
            errors.append("tail witness ratio")
        if row["safe_defect_Dbar"] != M - 309:
            errors.append("counter defect")
        ratio_exponent = M - n - 1
        if ratio_exponent <= previous_ratio_exponent:
            errors.append("tail ratios not increasing")
        previous_ratio_exponent = ratio_exponent

    replay = copy.deepcopy(result)
    stored = replay.pop("internal_replay_digest", None)
    if stored != cert.digest(replay):
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

        obj = result.get("physical_two_proper_view_object_lemma", {})
        if obj.get("status") != (
            "CERTIFIED_PHYSICAL_BOREL_TWO_PROPER_VIEW_MEASURE_ISOMORPHISM"
        ):
            errors.append("object lemma status")
        if obj.get("raw_geometry_is_proper") is not False:
            errors.append("raw properness overclaim")
        if "same K_par" not in obj.get("common_raw_record", ""):
            errors.append("common raw charge")
        initial = obj.get("initial_view_maps", {})
        if "I o H" not in initial.get("V_rev", ""):
            errors.append("reverse initial map")
        if "real-analytic inverse" not in initial.get("H", ""):
            errors.append("component inverse")
        if "Borel involution" not in initial.get("I", ""):
            errors.append("time reversal")
        if "m_raw-null" not in obj.get("full_measure_regular_domain", ""):
            errors.append("null regular domain")
        if obj.get("stopped_view_maps") != [
            "P_fw(y,x)=T_s^(696*Dbar(y))(V_fw(y,x))",
            "P_rev(y,x)=T_s^(696*Dbar(y))(V_rev(y,x))",
        ]:
            errors.append("stopped view maps")
        if obj.get("fibrewise_inverse_maps") != [
            "P_fw^-1=V_fw^-1 o T_s^(-696*Dbar)",
            "P_rev^-1=V_rev^-1 o T_s^(-696*Dbar)",
        ]:
            errors.append("inverse maps")
        if "Lusin-Souslin" not in obj.get("Borel_isomorphism_reason", ""):
            errors.append("Borel inverse reason")
        if "(P_sigma(y,.))_#K_par" not in obj.get("measure_transport", ""):
            errors.append("pushforward definition")
        if "whole proper standard-family kernels" not in obj.get(
            "proper_view_conclusion", ""
        ):
            errors.append("per-view properness")
        if obj.get("cuts_change_point_map_or_charge") is not False:
            errors.append("cut charge overclaim")
        if obj.get("same_ID_once_charge") is not True:
            errors.append("same-ID once charge")

        selected = result.get("selected_forward_proper_common_law", {})
        if selected.get("status") != (
            "CERTIFIED_SELECTED_FORWARD_PROPER_COMMON_LAW_WITH_BOREL_REVERSE_TRANSPORT"
        ):
            errors.append("selected common law status")
        if "K_fw_star" not in selected.get("selected_reference_law", ""):
            errors.append("selected forward law")
        if selected.get("view_transfer_map") != (
            "Theta_y=P_rev,y o P_fw,y^-1 from the forward proper view to the reverse proper view"
        ):
            errors.append("view transfer map")
        if selected.get("Theta_is_Borel_mod_null") is not True:
            errors.append("Theta Borel")
        if selected.get("Theta_pushforward_identity") != (
            "(Theta_y)_#K_fw_star(y,.)=K_rev_star(y,.)"
        ):
            errors.append("Theta pushforward")
        if "S_rev(y,Theta_y(z))" not in selected.get(
            "transported_reverse_predicate", ""
        ):
            errors.append("reverse predicate transport")
        if selected.get("transported_reverse_clock") != (
            "C_rev_star(y,z)=C_rev(y,Theta_y(z))"
        ):
            errors.append("reverse clock transport")
        if len(selected.get("orientation_integral_identities", [])) != 2:
            errors.append("two integral identities")
        if selected.get("separate_normalization_used") is not False:
            errors.append("separate normalization")
        if selected.get("parent_charged_once") is not True:
            errors.append("selected once charge")
        if selected.get(
            "transported_reverse_subset_is_geometrically_proper_inside_forward_view"
        ) != "NOT_ASSERTED":
            errors.append("transported geometry overclaim")

        wr = result.get("physical_postproperization_W_r_join", {})
        if wr.get("status") != (
            "CERTIFIED_PHYSICAL_POSTPROPERIZATION_TWO_VIEW_W_R_ONCE_CHARGE_MOMENT"
        ):
            errors.append("W_r join status")
        if "fixed finite terminal time H" not in wr.get("scope", ""):
            errors.append("fixed H scope")
        if wr.get("per_view_post_clock") != (
            "C_sigma_post=H+221328+696*k_sigma on its own proper pushforward view"
        ):
            errors.append("per-view post clock")
        if "K_sigma_star" not in wr.get("per_view_envelope", ""):
            errors.append("per-view moment law")
        if wr.get("pointwise_once_charge") != (
            "W_r_star^r<=1+1_Sfw_star*exp(C_fw_star/4176)+1_Srev_star*exp(C_rev_star/4176)"
        ):
            errors.append("pointwise max inequality")
        if wr.get("integrated_bound") != (
            "integral W_r_star^r dm_star<(1+2*A_H)*integral p dlambda"
        ):
            errors.append("integrated W_r bound")
        for key in (
            "physical_two_proper_view_join_installed",
            "postproperization_clock_only",
        ):
            if wr.get(key) is not True:
                errors.append(f"W_r true field: {key}")
        for key in (
            "raw_K_par_properness_used",
            "proper_intersection_used",
            "common_survivor_or_common_shell_used",
        ):
            if wr.get(key) is not False:
                errors.append(f"W_r false field: {key}")

        full = result.get("full_clock_conditional_bridge", {})
        if full.get("status") != (
            "CERTIFIED_EXACT_FULL_CLOCK_FORMULA_CONDITIONAL_ON_MISSING_DEFECT_MOMENT"
        ):
            errors.append("full clock status")
        if full.get("exact_preclock_exponent") != "696/4176=1/6":
            errors.append("preclock exponent field")
        if "exp(Dbar(y)/6)" not in full.get("required_same_kernel_moment", ""):
            errors.append("required defect moment")
        if full.get("conditional_integrated_bound") != (
            "integral Wtilde_r_star^r dm_star<integral p dlambda+2*A_H*I_D"
        ):
            errors.append("conditional full bound")
        if "(6/5)^Dbar" not in full.get("rational_sufficient_moment", ""):
            errors.append("rational defect moment")
        if full.get("physical_I_D_certified") is not False:
            errors.append("physical I_D overclaim")
        if full.get("complete_total_clock_W_r_certified") is not False:
            errors.append("total clock overclaim")

        tail = result.get("exact_defect_and_short_tail_frontier", {})
        if tail.get("status") != (
            "CERTIFIED_EXACT_DEFECT_FORMULA_AND_CONDITIONAL_SHORT_TAIL_BRIDGE"
        ):
            errors.append("tail frontier status")
        if tail.get("exact_C_p_bracket") != "2^310<C_p<2^311":
            errors.append("C_p bracket field")
        if tail.get("exact_defect_formula") != [
            "Dbar(M)=0 for 0<=M<=310",
            "Dbar(M)=M-309 for every integer M>=311; in particular Dbar never equals 1",
        ]:
            errors.append("defect formula field")
        if tail.get("unconditional_finite_ae") is not True:
            errors.append("finite-ae tail")
        if "continuity from above" not in tail.get("strongest_unconditional_tail", ""):
            errors.append("unconditional tail reason")
        if tail.get("quantitative_rate_from_current_fields") != "NONE_CERTIFIED":
            errors.append("tail rate overclaim")
        if tail.get("target_tail_available") is not False:
            errors.append("target tail overclaim")
        if tail.get("conditional_sharp_bound_from_target_tail") != (
            "integral (6/5)^Dbar p<=mass_total+(4/5)*C_len*2^-310"
        ):
            errors.append("shifted tail bound")
        if tail.get("conditional_bound_coefficient") != "(4/5)*2^-310":
            errors.append("shifted coefficient field")

        counter = result.get("short_tail_nonimplication", {})
        if counter.get("status") != (
            "CERTIFIED_EXACT_CURRENT_FIELDS_DO_NOT_IMPLY_SHORT_ENDPOINT_RATE"
        ):
            errors.append("countermodel status")
        if "single clipped endpoint cell" not in counter.get("natural_recut_scope", ""):
            errors.append("countermodel recut scope")
        if counter.get("linear_tail_consequence") != "no finite C_len works in this model":
            errors.append("linear tail nonimplication")
        if "not a claim" not in counter.get("logical_scope", ""):
            errors.append("countermodel logical scope")
        if counter.get("actual_billiard_short_tail_disproved") is not False:
            errors.append("actual billiard overclaim")

        gate = result.get("intersection_and_gate_frontier", {})
        if gate.get("status") != (
            "CERTIFIED_MEASURE_TRANSPORT_DOES_NOT_PROMOTE_GEOMETRIC_INTERSECTION_OR_GATE4"
        ):
            errors.append("intersection frontier status")
        if gate.get("joint_predicate_is_a_proper_standard_family") != "NOT_CERTIFIED":
            errors.append("joint properness overclaim")
        if "transports integrals, not boundary geometry" not in gate.get("reason", ""):
            errors.append("intersection reason")
        for key in (
            "proper_common_fw_rev_return",
            "numeric_H_cover_and_actual_beta",
            "complete_numeric_C_fw_C_rev",
            "collision_time_q",
            "strong_trace_current_cemetery",
        ):
            if gate.get(key) != "NOT_CERTIFIED":
                errors.append(f"gate overclaim: {key}")
        if gate.get("weak_mass_cemetery_inherited") != "CERTIFIED":
            errors.append("weak cemetery inheritance")
        if gate.get("Gate4") != "NOT_CERTIFIED" or gate.get("CM2") != "NO-GO_FOR_CLAIM":
            errors.append("gate verdict")

        frontier = result.get("corrected_frontier", {})
        expected_frontier = {
            "raw_K_par_proper": False,
            "physical_two_proper_view_pullback_lemma": "CERTIFIED",
            "selected_forward_proper_common_law": "CERTIFIED",
            "postproperization_same_ID_once_charge_W_r": "CERTIFIED_FIXED_H",
            "raw_parent_charged_once": True,
            "physical_preproperization_defect_exponential_moment": "NOT_CERTIFIED",
            "full_total_clock_common_law_Lp_join": "CONDITIONAL_NOT_CLOSED",
            "physical_linear_short_endpoint_tail": "NOT_CERTIFIED",
            "proper_common_fw_rev_intersection": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
        }
        if frontier != expected_frontier:
            errors.append("corrected frontier")

        expected_strict = {
            "two_proper_view_measure_isomorphism": "CERTIFIED",
            "postproperization_same_ID_common_parent_law": "CERTIFIED_MEASURE_THEORETIC_FIXED_H",
            "global_preproperization_clock_moment": "NOT_CERTIFIED",
            "full_total_clock_W_r": "CONDITIONAL_NOT_CLOSED",
            "proper_common_intersection": "NOT_CERTIFIED",
            "full_numeric_C_fw_C_rev": "NOT_CERTIFIED",
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
        (("result", "provenance", "parameter_scope"), "joint-s"),
        (("result", "physical_two_proper_view_object_lemma", "status"), "NOT_CERTIFIED"),
        (("result", "physical_two_proper_view_object_lemma", "raw_geometry_is_proper"), True),
        (("result", "physical_two_proper_view_object_lemma", "common_raw_record"), "two laws"),
        (("result", "physical_two_proper_view_object_lemma", "initial_view_maps", "V_rev"), "unrelated"),
        (("result", "physical_two_proper_view_object_lemma", "initial_view_maps", "H"), "noninvertible"),
        (("result", "physical_two_proper_view_object_lemma", "initial_view_maps", "I"), "not Borel"),
        (("result", "physical_two_proper_view_object_lemma", "full_measure_regular_domain"), "keeps singular mass"),
        (("result", "physical_two_proper_view_object_lemma", "stopped_view_maps"), []),
        (("result", "physical_two_proper_view_object_lemma", "fibrewise_inverse_maps"), []),
        (("result", "physical_two_proper_view_object_lemma", "Borel_isomorphism_reason"), "automatic"),
        (("result", "physical_two_proper_view_object_lemma", "measure_transport"), "unrelated kernel"),
        (("result", "physical_two_proper_view_object_lemma", "proper_view_conclusion"), "raw proper"),
        (("result", "physical_two_proper_view_object_lemma", "cuts_change_point_map_or_charge"), True),
        (("result", "physical_two_proper_view_object_lemma", "same_ID_once_charge"), False),
        (("result", "physical_two_proper_view_object_lemma", "sample_view_map_rows"), []),
        (("result", "physical_two_proper_view_object_lemma", "sample_view_map_rows_sha256"), "0" * 64),
        (("result", "selected_forward_proper_common_law", "status"), "CONDITIONAL"),
        (("result", "selected_forward_proper_common_law", "selected_reference_law"), "raw"),
        (("result", "selected_forward_proper_common_law", "view_transfer_map"), "identity"),
        (("result", "selected_forward_proper_common_law", "Theta_is_Borel_mod_null"), False),
        (("result", "selected_forward_proper_common_law", "Theta_pushforward_identity"), "false"),
        (("result", "selected_forward_proper_common_law", "transported_reverse_predicate"), "not transported"),
        (("result", "selected_forward_proper_common_law", "transported_reverse_clock"), "0"),
        (("result", "selected_forward_proper_common_law", "orientation_integral_identities"), []),
        (("result", "selected_forward_proper_common_law", "separate_normalization_used"), True),
        (("result", "selected_forward_proper_common_law", "parent_charged_once"), False),
        (("result", "selected_forward_proper_common_law", "transported_reverse_subset_is_geometrically_proper_inside_forward_view"), "CERTIFIED"),
        (("result", "physical_postproperization_W_r_join", "status"), "NOT_CERTIFIED"),
        (("result", "physical_postproperization_W_r_join", "scope"), "variable H"),
        (("result", "physical_postproperization_W_r_join", "per_view_post_clock"), "wrong clock"),
        (("result", "physical_postproperization_W_r_join", "per_view_envelope"), "raw envelope"),
        (("result", "physical_postproperization_W_r_join", "pointwise_once_charge"), "sum parents twice"),
        (("result", "physical_postproperization_W_r_join", "integrated_bound"), "infinite"),
        (("result", "physical_postproperization_W_r_join", "physical_two_proper_view_join_installed"), False),
        (("result", "physical_postproperization_W_r_join", "raw_K_par_properness_used"), True),
        (("result", "physical_postproperization_W_r_join", "proper_intersection_used"), True),
        (("result", "physical_postproperization_W_r_join", "common_survivor_or_common_shell_used"), True),
        (("result", "physical_postproperization_W_r_join", "postproperization_clock_only"), False),
        (("result", "full_clock_conditional_bridge", "status"), "UNCONDITIONAL"),
        (("result", "full_clock_conditional_bridge", "exact_preclock_exponent"), "1"),
        (("result", "full_clock_conditional_bridge", "required_same_kernel_moment"), "none"),
        (("result", "full_clock_conditional_bridge", "conditional_integrated_bound"), "no defect"),
        (("result", "full_clock_conditional_bridge", "rational_sufficient_moment"), "L1"),
        (("result", "full_clock_conditional_bridge", "physical_I_D_certified"), True),
        (("result", "full_clock_conditional_bridge", "complete_total_clock_W_r_certified"), True),
        (("result", "exact_defect_and_short_tail_frontier", "status"), "TAIL_CERTIFIED"),
        (("result", "exact_defect_and_short_tail_frontier", "exact_C_p_bracket"), "2^311<Cp"),
        (("result", "exact_defect_and_short_tail_frontier", "exact_defect_formula"), []),
        (("result", "exact_defect_and_short_tail_frontier", "unconditional_finite_ae"), False),
        (("result", "exact_defect_and_short_tail_frontier", "strongest_unconditional_tail"), "exponential"),
        (("result", "exact_defect_and_short_tail_frontier", "quantitative_rate_from_current_fields"), "2^-m"),
        (("result", "exact_defect_and_short_tail_frontier", "target_tail_available"), True),
        (("result", "exact_defect_and_short_tail_frontier", "conditional_sharp_bound_from_target_tail"), "mass+C/2"),
        (("result", "exact_defect_and_short_tail_frontier", "conditional_bound_coefficient"), "1/2"),
        (("result", "short_tail_nonimplication", "status"), "NO_OBSTRUCTION"),
        (("result", "short_tail_nonimplication", "natural_recut_scope"), "infinite cells per group"),
        (("result", "short_tail_nonimplication", "linear_tail_consequence"), "tail holds"),
        (("result", "short_tail_nonimplication", "logical_scope"), "actual billiard theorem"),
        (("result", "short_tail_nonimplication", "actual_billiard_short_tail_disproved"), True),
        (("result", "short_tail_nonimplication", "rows"), []),
        (("result", "short_tail_nonimplication", "rows_sha256"), "0" * 64),
        (("result", "intersection_and_gate_frontier", "status"), "GATE4"),
        (("result", "intersection_and_gate_frontier", "joint_predicate_is_a_proper_standard_family"), "CERTIFIED"),
        (("result", "intersection_and_gate_frontier", "reason"), "proper by transport"),
        (("result", "intersection_and_gate_frontier", "proper_common_fw_rev_return"), "CERTIFIED"),
        (("result", "intersection_and_gate_frontier", "numeric_H_cover_and_actual_beta"), "CERTIFIED"),
        (("result", "intersection_and_gate_frontier", "complete_numeric_C_fw_C_rev"), "CERTIFIED"),
        (("result", "intersection_and_gate_frontier", "collision_time_q"), "CERTIFIED"),
        (("result", "intersection_and_gate_frontier", "strong_trace_current_cemetery"), "CERTIFIED"),
        (("result", "intersection_and_gate_frontier", "weak_mass_cemetery_inherited"), "NOT_CERTIFIED"),
        (("result", "intersection_and_gate_frontier", "Gate4"), "CERTIFIED"),
        (("result", "intersection_and_gate_frontier", "CM2"), "GO"),
        (("result", "corrected_frontier", "raw_K_par_proper"), True),
        (("result", "corrected_frontier", "physical_two_proper_view_pullback_lemma"), "NOT_CERTIFIED"),
        (("result", "corrected_frontier", "selected_forward_proper_common_law"), "NOT_CERTIFIED"),
        (("result", "corrected_frontier", "physical_preproperization_defect_exponential_moment"), "CERTIFIED"),
        (("result", "corrected_frontier", "full_total_clock_common_law_Lp_join"), "CERTIFIED"),
        (("result", "corrected_frontier", "physical_linear_short_endpoint_tail"), "CERTIFIED"),
        (("result", "corrected_frontier", "proper_common_fw_rev_intersection"), "CERTIFIED"),
        (("result", "corrected_frontier", "complete_numeric_C_fw_C_rev_q"), "CERTIFIED"),
        (("result", "corrected_frontier", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "global_preproperization_clock_moment"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "full_total_clock_W_r"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "proper_common_intersection"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "full_numeric_C_fw_C_rev"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_collision_time_q"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "strong_cemetery"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "5/5"),
        (("result", "strict_nonpromotion", "CM2"), "GO"),
        (("verdict", "Gate4"), "CERTIFIED"),
        (("verdict", "CM2"), "GO"),
    ]
    mutations: list[str] = []
    for keys, replacement in changes:
        mutation = copy.deepcopy(source)
        set_path(mutation, keys, replacement)
        mutations.append(json.dumps(mutation))
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
        mutations.append(json.dumps(mutation))
    mutation = copy.deepcopy(source)
    mutation["unexpected_top_level_key"] = True
    mutations.append(json.dumps(mutation))
    mutation = copy.deepcopy(source)
    mutation["result"]["exact_defect_and_short_tail_frontier"]["target_tail_available"] = float("nan")
    mutations.append(json.dumps(mutation))
    duplicate = path.read_text(encoding="utf-8").rstrip()
    mutations.append(duplicate[:-1] + ',"schema":"duplicate"}')

    rejected = 0
    for body in mutations:
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=".cm2-r51-two-view-hostile-",
            suffix=".json",
            dir=cert.HERE,
            delete=False,
        )
        target = Path(handle.name)
        try:
            with handle:
                handle.write(body)
            errs = verify(target)
            rejected += bool(errs and errs != ["unsafe manifest"])
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
    errors = verify(args.manifest)
    if errors:
        print("AUDIT_MODE: FAIL")
        for error in errors:
            print("ERROR:", error)
        return 1
    if args.self_test:
        rejected, total = self_test(args.manifest)
        print(f"SELF_TEST: {rejected}/{total}")
        return 0 if rejected == total else 1
    if args.independent_arithmetic_only:
        print("INDEPENDENT_ARITHMETIC: PASS")
        return 0
    if args.integrity_only:
        print("INTEGRITY: PASS")
        return 0
    if args.replay:
        print("AUDIT_MODE: PASS")
        return 0
    print("MANIFEST: PASS")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
