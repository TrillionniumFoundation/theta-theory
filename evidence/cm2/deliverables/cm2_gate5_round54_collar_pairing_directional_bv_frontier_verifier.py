#!/usr/bin/env python3
"""Fail-closed verifier for the Round-54 Gate-5 collar/BV frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round54_collar_pairing_directional_bv_frontier_cert as cert


HERE = Path(__file__).resolve().parent
RHO = Q(111718729, 111718750) ** 9148
W_Z = (1 + 1 / RHO) / 2
KAPPA = 1 / W_Z
C_FLUX = Q(8064, 5)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError("unsafe manifest")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=cert.strict_object,
        parse_constant=cert.reject_json_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError("manifest root")
    return value


def collar_rows() -> list[dict[str, Any]]:
    source = [
        ("a0", Q(1, 2), Q(1, 2)),
        ("a1", Q(1, 4), Q(1, 8)),
        ("a2", Q(1, 8), Q(1, 64)),
        ("a3", Q(1, 8), Q(1, 4096)),
    ]
    return [
        {
            "owner_label": label,
            "trace_mass": str(mass),
            "dyadic_collar_length": str(ell),
            "constant_density": str(1 / ell),
            "collar_Z_contribution": str(mass / ell),
        }
        for label, mass, ell in source
    ]


def pairing_rows() -> list[dict[str, Any]]:
    return [
        {
            "paired_distance": str(distance),
            "BL_difference_factor": str(min(Q(2), distance)),
            "physical_flux_BL_charge_upper": str(
                C_FLUX * min(Q(2), distance)
            ),
        }
        for distance in (Q(2), Q(1), Q(1, 16), Q(1, 1024))
    ]


def bv_rows() -> list[dict[str, Any]]:
    return [
        {
            "triangle_wave_periods": periods,
            "L_infinity": "1",
            "directional_BV_variation": str(4 * periods),
            "variation_to_Linfinity_ratio": str(4 * periods),
        }
        for periods in (1, 4, 16, 64, 256)
    ]


def direct_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        provenance = result["provenance"]
        if provenance["parameter_scope"] != "base parameter s=0":
            errors.append("parameter scope")
        if "finite regular owner record" not in provenance["owner_scope"]:
            errors.append("owner record scope")
        if "all insertion times" not in provenance["owner_scope"]:
            errors.append("aggregate scope")

        collar = result["recordwise_owner_collar_E_Tr"]
        if "stage dependent" not in collar["physical_scope"]:
            errors.append("stage-dependent scope")
        if "word-cell" not in collar["same_ID_label"]:
            errors.append("word-cell ID")
        clearance = collar["positive_clearance_predicate"]
        if any(token not in clearance for token in ("A_col", "d_a>0", "next OTHER", "anchor face", "excluded")):
            errors.append("clearance predicate")
        if "may be continuous" not in collar["trace_law_typing"]:
            errors.append("continuous trace law")
        joint = collar["joint_labelled_carrier"]
        if "Mtilde_j" not in joint or "overlapping physical collar images are not identified" not in joint:
            errors.append("joint labelled carrier")
        selection = collar["canonical_Borel_selection"]
        if "ell(omega)=2^(-(k(omega)+1))<d(omega)" not in selection:
            errors.append("dyadic selection")
        borel_proof = collar["Borel_kernel_proof"]
        for token in ("anchored", "half-open", "except the designated anchor face", "Borel", "countable union", "probability kernel"):
            if token not in borel_proof:
                errors.append("Borel collar kernel")
                break
        anchored = collar["anchored_half_open_geometry"]
        for token in ("(xi_", "[xi_", "closure may", "root face only", "far endpoint", "ell<d"):
            if token not in anchored:
                errors.append("anchored half-open geometry")
                break
        if "Borel Markov kernel" not in collar["source_stage_extension"] or "{omega}xI_" not in collar["source_stage_extension"]:
            errors.append("stage extension")
        if any(token not in collar["stage_recovery"] for token in ("deterministic Borel kernel", "retained label", "one-sided", "^side")):
            errors.append("mapped recovery")
        if collar["mass_norms"] != "norm_mass(E)=norm_mass(Tr)=1 on measures restricted to A_col":
            errors.append("mass norms")
        if collar["recovery_identity"] != (
            "Tr_j composed E_j = Id on the stage-j owner trace laws restricted to A_col"
        ):
            errors.append("recovery identity")
        if collar["killed_word_intertwining"] != (
            "K_trace_(j,t)=Tr_t composed K_word_(j,t) composed E_j because the whole "
            "anchored one-sided labelled collar fiber I_a,j has the same half-open "
            "killed-word bit as xi_a,j and K_word acts fiberwise without dropping omega"
        ):
            errors.append("killed-word intertwining")
        no_cut = collar["no_internal_cut_or_mass_leak"]
        for token in ("designated anchor root face", "every other", "open side cell", "regular diffeomorphic one-sided branch", "half-open", "preserves its total mass"):
            if token not in no_cut:
                errors.append("no-cut typing")
                break
        if collar["zero_map_excluded"] is not True:
            errors.append("zero map")
        if "integral_(A_col)" not in collar["standard_family_shape_debt"] or "finiteness is NOT_CERTIFIED" not in collar["standard_family_shape_debt"]:
            errors.append("collar debt")
        if "integral_(A_col)" not in collar["full_rank_shape_debt"]:
            errors.append("rank collar debt")
        expected_collar = collar_rows()
        if collar["sample_rows"] != expected_collar:
            errors.append("collar rows")
        if collar["sample_rows_sha256"] != cert.digest(expected_collar):
            errors.append("collar digest")
        if sum(
            Q(row["trace_mass"]) / Q(row["dyadic_collar_length"])
            for row in expected_collar
        ) != 523:
            errors.append("collar arithmetic")
        if collar["sample_Z_col"] != "523":
            errors.append("collar total")
        if collar["collar_admissible_stagewise_mass_E_Tr_schema_installed"] is not True:
            errors.append("recordwise schema")
        if collar["all_physical_owner_records_stagewise_E_Tr_installed"] is not False:
            errors.append("all-owner bridge promotion")
        if collar["nu_mass_of_A_col_positive_or_full"] != "NOT_CERTIFIED":
            errors.append("A_col mass promotion")
        if collar["Round53_uniform_proper_bridge_installed"] is not False:
            errors.append("proper bridge promotion")
        if "finite Z_col" not in collar["why_not_the_Round53_genuine_bridge"]:
            errors.append("aggregate properness")
        if collar["quantitative_trace_contraction_installed"] is not False:
            errors.append("trace contraction promotion")
        separator = collar["parent_Z_does_not_control_collar_Z_separator"]
        if separator["trace_mass"] != "sum_k 2^(-k)=1":
            errors.append("separator mass")
        if separator["unranked_parent_inverse_length_debt"] != "sum_k p_k/1=1":
            errors.append("unranked parent debt")
        if separator["full_parent_owner_ZB_at_B14"] != (
            "sum_k 2^14*p_k/1=2^14=16384, finite"
        ):
            errors.append("full parent ZB")
        if "terms do not tend to zero" not in separator["collar_inverse_length_debt"]:
            errors.append("separator divergence")
        if separator["full_rank_collar_debt"] != (
            "sum_k 2^14*p_k/ell_k=2^14*infinity=infinity"
        ):
            errors.append("full collar ZB")
        if "cannot be renamed" not in separator["logical_conclusion"]:
            errors.append("parent/collar typing")
        grazing = collar["grazing_homogeneity_accumulation_separator"]
        if "dc/ell" not in grazing["model"] or "k>=1" not in grazing["model"]:
            errors.append("grazing model")
        if "telescope to one" not in grazing["uniform_collar_subdivision"]:
            errors.append("grazing normalization")
        if grazing["shape_debt"] != (
            "sum over the infinitely many nonempty shells of 1/ell=infinity"
        ):
            errors.append("grazing debt")
        if "extra physical predicate" not in grazing["logical_conclusion"]:
            errors.append("grazing conclusion")
        if collar["status"] != (
            "CERTIFIED_A_COL_STAGEWISE_COLLAR_E_TR_WITH_UNCONTROLLED_SHAPE_DEBT"
        ):
            errors.append("collar status")

        pair = result["signed_hit_miss_pairing_resolvent"]
        if "retained source-rank B" not in pair["pairing_scope"] or "no product coupling" not in pair["pairing_scope"]:
            errors.append("pairing fiber scope")
        if all(token in pair["physical_signed_pair"] for token in ("lambda_p^+", "lambda_p^-", "mu_p^+", "mu_p^-", "equal mass", "J_p=mu_p^+-mu_p^-")) is False:
            errors.append("equal pair mass")
        flux_typing = pair["physical_flux_typing"]
        if any(token not in flux_typing for token in ("actual physical sigma_e", "2^B", "not identified")):
            errors.append("physical flux typing")
        if pair["physical_positive_mass_upper"] != "m_p<=C_flux=8064/5":
            errors.append("physical flux mass")
        coupling = pair["coupling_kernel"]
        if any(token not in coupling for token in ("pi_p=0", "(mu_p^+ tensor mu_p^-)/m_p", "marginals", "Borel kernel", "without any measurable-choice")):
            errors.append("Borel coupling")
        if pair["constant_test"] != "J_p(1)=0":
            errors.append("constant cancellation")
        if pair["pointwise_bound"] != (
            "abs(phi(y+)-phi(y-))<=min(2,d(y+,y-))*norm(phi)_BL"
        ):
            errors.append("BL pointwise")
        if pair["canonical_pair_charge"] != (
            "d_p(pi_p)=integral min(2,d(y+,y-))d pi_p(y+,y-)"
        ):
            errors.append("physical pair charge")
        expected_pair = pairing_rows()
        if pair["rows"] != expected_pair:
            errors.append("pair rows")
        if pair["rows_sha256"] != cert.digest(expected_pair):
            errors.append("pair digest")
        if [row["physical_flux_BL_charge_upper"] for row in expected_pair] != [
            "16128/5", "8064/5", "504/5", "63/40"
        ]:
            errors.append("physical pair row arithmetic")
        if pair["weighted_resolvent_condition"] != "w*delta_pair<1":
            errors.append("paired resolvent condition")
        if pair["weighted_resolvent_bound"] != (
            "sum_p w^p norm(J_p)_(BL*)<=C_pair/(1-w*delta_pair)"
        ):
            errors.append("paired resolvent bound")
        rho_route = pair["rho_rate_at_Round42_weight"]
        if not Q(1) < W_Z < 1 / RHO:
            errors.append("weight window")
        if W_Z * RHO != (1 + RHO) / 2 or not W_Z * RHO < 1:
            errors.append("rho route arithmetic")
        if 1 - W_Z * RHO != (1 - RHO) / 2:
            errors.append("rho denominator")
        if rho_route["rho_fraction_binary_sha256"] != cert.fraction_digest(RHO):
            errors.append("rho digest")
        if rho_route["kappa_fraction_binary_sha256"] != cert.fraction_digest(KAPPA):
            errors.append("kappa digest")
        physical_sufficient = pair["physical_flux_distance_sufficient_condition"]
        if "8064/5" not in physical_sufficient or "support" not in physical_sufficient:
            errors.append("physical distance sufficient condition")
        rank_envelope = pair["rank_envelope_conditional"]
        if any(token not in rank_envelope for token in ("m_p<=C_sigma*2^B", "2^(-B)", "never the equality sigma_e=2^B")):
            errors.append("rank envelope conditional")
        if pair["physical_pair_separation_rate"] != "NOT_CERTIFIED":
            errors.append("pair rate promotion")
        if pair["positive_F10_or_TV_face_tower_from_signed_pairing"] != "NOT_CERTIFIED":
            errors.append("positive pairing promotion")
        if pair["unconditional_signed_BL_resolvent"] != "NOT_CERTIFIED":
            errors.append("signed resolvent promotion")
        if pair["status"] != (
            "CERTIFIED_SIGNED_PAIR_BL_BOUND_AND_CONDITIONAL_RHO_WEIGHT_ROUTE"
        ):
            errors.append("pair status")

        bv = result["directional_BV_F17_order_reduction"]
        if "div_mu X_s=0" not in bv["physical_generator"]:
            errors.append("divergence-free generator")
        if "finite signed directional" not in bv["directional_source_space"] or "Gauss-Green" not in bv["directional_source_space"]:
            errors.append("BV_X type")
        if any(token not in bv["directional_derivative_typing"] for token in ("relative to mu", "integral phi d(D_X h)", "-integral h*X(phi)dmu")):
            errors.append("directional derivative typing")
        if bv["compact_interior_identity"] != (
            "T_h=-D_X h as an order-zero signed measure, with D_X h typed relative to mu"
        ):
            errors.append("interior order reduction")
        if any(token not in bv["domain_identity"] for token in ("gamma_Xh=(R*h*X dot n_U)H^1", "mu=R*dr*dp", "physical boundary")):
            errors.append("domain boundary")
        if bv["source_cost"] != "C_BVXtr(h;U)=TV(D_X h)+TV(gamma_Xh)":
            errors.append("BV trace cost")
        if bv["order_zero_TV_bound"] != "TV(T_h)<=C_BVXtr(h;U)":
            errors.append("TV bound")
        if bv["suffix_multiplier_on_directional_BV_subcarrier"] != (
            "C_dyn=1 in the order-zero TV/C0-dual transport norm"
        ):
            errors.append("BV suffix norm")
        if "no bounded identification" not in bv["not_a_single_fixed_physical_dynamic_test_field"]:
            errors.append("physical field boundary")
        if bv["passes_quarter_threshold"] is not True:
            errors.append("quarter threshold")
        if not Q(1) < Q(7961063, 7800000):
            errors.append("quarter arithmetic")
        expected_bv = bv_rows()
        separator_bv = bv["Linfinity_nonimplication_separator"]
        if separator_bv["space"] != (
            "U=[0,1]^2, X=e_1 and R=1 in this logical flat model"
        ):
            errors.append("BV separator density")
        if separator_bv["rows"] != expected_bv:
            errors.append("BV rows")
        if separator_bv["rows_sha256"] != cert.digest(expected_bv):
            errors.append("BV digest")
        if separator_bv["rows"][-1]["directional_BV_variation"] != "1024":
            errors.append("BV last row")
        if bv["physical_all_input_directional_BV_bound"] != "NOT_CERTIFIED":
            errors.append("BV source promotion")
        if bv["same_ID_boundary_flux_join_for_order_reduction"] != "NOT_CERTIFIED":
            errors.append("BV boundary promotion")
        if bv["complete_physical_F17"] != "NOT_CERTIFIED":
            errors.append("F17 promotion")
        if bv["status"] != (
            "CERTIFIED_DIRECTIONAL_BV_ORDER_REDUCTION_WITH_SUFFIX_CONSTANT_ONE"
        ):
            errors.append("BV status")

        gate3 = result["Gate3_directional_BV_conditional_join"]
        free_match = gate3["free_carrier_match"]
        for token in ("bulk -D_X h", "(C^{1,alpha}(N))* summand", "boundary graph fluxes", "l1(Omega_<=2;M(I))", "no bulk measure", "41508 graph slots"):
            if token not in free_match:
                errors.append("Gate3 carrier split")
                break
        if gate3["bulk_destination"] != "-D_X h -> (C^{1,alpha}(N))*":
            errors.append("Gate3 bulk destination")
        if gate3["boundary_destination"] != (
            "parameterized gamma_Xh graph fluxes -> l1(Omega_<=2;M(I)), with 41508 slots"
        ):
            errors.append("Gate3 boundary destination")
        if gate3["bulk_graph_slot_conflation_excluded"] is not True:
            errors.append("Gate3 slot conflation")
        expected_conditions = [
            "bind every parameterized moving physical boundary graph/component and owner ID to one of the 41508 fixed graph slots",
            "lift the physical B2 input into a uniformly bounded directional-BV_X^tr payload",
            "assemble duplicate/artificial domain-flux traces before total variation",
            "prove bounded inclusion of the bulk order-zero measure and the boundary graph-slot family in physical B0",
            "prove common-atlas moving-limit convergence and the growing-depth no-|s|^-1 tail",
            "complete the remaining 17 operator fields on one recovered physical block",
        ]
        if gate3["conditions"] != expected_conditions:
            errors.append("Gate3 conditions")
        if gate3["conditions_sha256"] != cert.digest(expected_conditions):
            errors.append("Gate3 digest")
        for key in (
            "physical_Rs_directional_BV_lift",
            "physical_Qs_order_zero_quotient",
            "intertwining_Qs_Phat_Rs",
            "dynamic_branch_record_MT_DQ",
        ):
            if gate3[key] != "NOT_CERTIFIED":
                errors.append(f"Gate3 promotion {key}")
        if gate3["automatic_promotion_from_order_reduction"] is not False:
            errors.append("automatic Gate3 promotion")

        tech = result["latest_technology_audit"]
        if tech["official_query_date"] != "2026-07-20":
            errors.append("technology date")
        if tech["newer_direct_trace_contraction_or_vector_current_theorem_found"] is not False:
            errors.append("technology overclaim")
        if tech["status"] != "CHECKED_NO_DIRECT_TYPED_UPGRADE":
            errors.append("technology status")

        maturity = result["Gate5_maturity_update"]
        if maturity["new_global_field_completed"] is not None:
            errors.append("field promotion")
        if maturity["current_global_maturity"] != "10/18":
            errors.append("maturity")
        if maturity["complete_18_field_operator_block_count"] != 0:
            errors.append("complete blocks")

        strict = result["strict_nonpromotion"]
        expected_strict = {
            "collar_admissible_stagewise_mass_same_ID_collar_Ej_Trj": "CERTIFIED",
            "all_physical_owner_recordwise_Ej_Trj": "NOT_CERTIFIED",
            "positive_or_full_owner_trace_mass_of_A_col": "NOT_CERTIFIED",
            "A_col_killed_word_intertwining": "CERTIFIED",
            "Round53_uniformly_proper_trace_extension_bridge": "NOT_CERTIFIED",
            "global_owner_collar_Z_integrability": "NOT_CERTIFIED",
            "quantitative_trace_survivor_contraction": "NOT_CERTIFIED",
            "fixed_weight_q_above_critical_owner_moment": "NOT_CERTIFIED",
            "signed_pair_BL_bound": "CERTIFIED",
            "physical_paired_image_rho_rate": "NOT_CERTIFIED",
            "unconditional_signed_BL_resolvent": "NOT_CERTIFIED",
            "positive_F10_face_tower_from_signed_pairing": "NOT_CERTIFIED",
            "directional_BV_order_reduction_suffix_constant_one": "CERTIFIED_SUBCARRIER",
            "physical_all_input_directional_BV_source_bound": "NOT_CERTIFIED",
            "physical_F17_bulk_suffix_constant": "NOT_CERTIFIED",
            "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
            "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "strong_F13": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate3_Qs_Rs_physical_lift_quotient": "NOT_CERTIFIED",
            "Gate3_MT_DQ": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if strict != expected_strict:
            errors.append("strict nonpromotion")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"malformed result: {exc}")
    return errors


def fast_integrity_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema") != cert.MANIFEST_SCHEMA:
        errors.append("schema")
    if manifest.get("certificate_sha256") != sha(Path(cert.__file__).resolve()):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha(Path(__file__).resolve()):
        errors.append("verifier hash")
    if manifest.get("dependencies") != cert.DEPENDENCIES:
        errors.append("dependencies")
    result = manifest.get("result")
    if not isinstance(result, dict):
        errors.append("result")
        return errors
    replay_digest = result.get("internal_replay_digest")
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    if replay_digest != cert.digest(payload):
        errors.append("internal digest")
    if manifest.get("verdict") != result.get("strict_nonpromotion"):
        errors.append("verdict")
    return errors


def verify_object(manifest: dict[str, Any], replay: bool = True) -> list[str]:
    errors = fast_integrity_errors(manifest)
    if not errors:
        errors.extend(direct_errors(manifest["result"]))
    if replay and not errors:
        try:
            replayed = cert.build_result()
        except Exception as exc:
            errors.append(f"dependency replay: {exc}")
        else:
            if manifest["result"] != replayed:
                errors.append("deterministic replay")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    current: Any = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement


def hostile_paths() -> list[tuple[str, ...]]:
    collar = "recordwise_owner_collar_E_Tr"
    pair = "signed_hit_miss_pairing_resolvent"
    bv = "directional_BV_F17_order_reduction"
    gate3 = "Gate3_directional_BV_conditional_join"
    tech = "latest_technology_audit"
    strict = "strict_nonpromotion"
    paths = [
        ("result", "provenance", "parameter_scope"),
        ("result", "provenance", "owner_scope"),
        ("result", "provenance", "claim_type"),
    ]
    for key in (
        "physical_scope",
        "same_ID_label",
        "trace_law_typing",
        "joint_labelled_carrier",
        "positive_clearance_predicate",
        "canonical_Borel_selection",
        "Borel_kernel_proof",
        "anchored_half_open_geometry",
        "source_stage_extension",
        "stage_recovery",
        "mass_norms",
        "recovery_identity",
        "killed_word_intertwining",
        "no_internal_cut_or_mass_leak",
        "zero_map_excluded",
        "extension_density_regularity",
        "standard_family_shape_debt",
        "full_rank_shape_debt",
        "sample_rows_sha256",
        "sample_Z_col",
        "uniformly_proper_if",
        "collar_admissible_stagewise_mass_E_Tr_schema_installed",
        "all_physical_owner_records_stagewise_E_Tr_installed",
        "nu_mass_of_A_col_positive_or_full",
        "Round53_uniform_proper_bridge_installed",
        "why_not_the_Round53_genuine_bridge",
        "quantitative_trace_contraction_installed",
        "parent_Z_does_not_control_collar_Z_separator",
        "grazing_homogeneity_accumulation_separator",
        "first_missing_global_join",
        "status",
    ):
        paths.append(("result", collar, key))
    for key in (
        "physical_signed_pair",
        "physical_flux_typing",
        "physical_positive_mass_upper",
        "pairing_scope",
        "coupling_kernel",
        "constant_test",
        "test_norm",
        "pointwise_bound",
        "canonical_pair_charge",
        "BL_dual_bound",
        "rows_sha256",
        "weighted_resolvent_hypothesis",
        "weighted_resolvent_condition",
        "weighted_resolvent_bound",
        "rho_rate_at_Round42_weight",
        "physical_flux_distance_sufficient_condition",
        "rank_envelope_conditional",
        "why_q_star_is_bypassed",
        "physical_pair_separation_rate",
        "positive_F10_or_TV_face_tower_from_signed_pairing",
        "unconditional_signed_BL_resolvent",
        "logical_scope",
        "status",
    ):
        paths.append(("result", pair, key))
    for key in (
        "coordinates",
        "physical_generator",
        "directional_source_space",
        "directional_derivative_typing",
        "compact_interior_identity",
        "domain_identity",
        "source_cost",
        "order_zero_TV_bound",
        "finite_regular_suffix",
        "suffix_multiplier_on_directional_BV_subcarrier",
        "not_a_single_fixed_physical_dynamic_test_field",
        "passes_quarter_threshold",
        "piecewise_constant_flat_density_sublayer",
        "Linfinity_nonimplication_separator",
        "physical_all_input_directional_BV_bound",
        "same_ID_boundary_flux_join_for_order_reduction",
        "complete_physical_F17",
        "precise_gain",
        "status",
    ):
        paths.append(("result", bv, key))
    for key in (
        "new_typed_payload",
        "free_carrier_match",
        "bulk_destination",
        "boundary_destination",
        "bulk_graph_slot_conflation_excluded",
        "finite_record_distribution_identity",
        "conditions_sha256",
        "physical_Rs_directional_BV_lift",
        "physical_Qs_order_zero_quotient",
        "intertwining_Qs_Phat_Rs",
        "dynamic_branch_record_MT_DQ",
        "automatic_promotion_from_order_reduction",
        "status",
    ):
        paths.append(("result", gate3, key))
    for key in (
        "official_query_date",
        "official_versions_checked",
        "official_source_archive_sha256_replayed_from_Round53",
        "newer_direct_trace_contraction_or_vector_current_theorem_found",
        "relevant_existing_mechanisms",
        "why_not_imported",
        "status",
    ):
        paths.append(("result", tech, key))
    for key in (
        "new_global_field_completed",
        "newly_certified_sublayers",
        "reason_no_new_field_credit",
        "current_global_maturity",
        "complete_18_field_operator_block_count",
    ):
        paths.append(("result", "Gate5_maturity_update", key))
    for key in (
        "collar_admissible_stagewise_mass_same_ID_collar_Ej_Trj",
        "all_physical_owner_recordwise_Ej_Trj",
        "positive_or_full_owner_trace_mass_of_A_col",
        "A_col_killed_word_intertwining",
        "Round53_uniformly_proper_trace_extension_bridge",
        "global_owner_collar_Z_integrability",
        "quantitative_trace_survivor_contraction",
        "fixed_weight_q_above_critical_owner_moment",
        "signed_pair_BL_bound",
        "physical_paired_image_rho_rate",
        "unconditional_signed_BL_resolvent",
        "positive_F10_face_tower_from_signed_pairing",
        "directional_BV_order_reduction_suffix_constant_one",
        "physical_all_input_directional_BV_source_bound",
        "physical_F17_bulk_suffix_constant",
        "same_ID_full_ZB_one_step_recurrence",
        "unconditional_aggregate_ZB_resolvent",
        "return_depth_weighted_face_integrability",
        "complete_all_face_F10",
        "strong_F13",
        "F14_F15_F17_F18",
        "strong_cemetery",
        "Gate3_Qs_Rs_physical_lift_quotient",
        "Gate3_MT_DQ",
        "Gate3",
        "Gate4",
        "Gate5",
        "Gate5_maturity",
        "complete_18_field_operator_block_count",
        "complete_composite_gates",
        "CM2",
    ):
        paths.append(("result", strict, key))
    return paths


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    failures = 0
    total = 0
    for path in hostile_paths():
        total += 1
        mutant = copy.deepcopy(manifest)
        current: Any = mutant
        for key in path:
            current = current[key]
        if isinstance(current, bool):
            replacement: Any = not current
        elif isinstance(current, int):
            replacement = current + 1
        elif current is None:
            replacement = "CERTIFIED"
        elif isinstance(current, (dict, list)):
            replacement = {}
        else:
            replacement = "HOSTILE_MUTATION"
        set_path(mutant, path, replacement)
        if not fast_integrity_errors(mutant):
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
        if not fast_integrity_errors(mutant):
            failures += 1
    total += 1
    mutant = copy.deepcopy(manifest)
    mutant["result"]["internal_replay_digest"] = "0" * 64
    if not fast_integrity_errors(mutant):
        failures += 1
    for payload in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
        total += 1
        try:
            json.loads(
                payload,
                object_pairs_hook=cert.strict_object,
                parse_constant=cert.reject_json_constant,
            )
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
