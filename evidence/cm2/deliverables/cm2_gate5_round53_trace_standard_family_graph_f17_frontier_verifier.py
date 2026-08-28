#!/usr/bin/env python3
"""Fail-closed verifier for the Round-53 Gate-5 trace/graph frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round53_trace_standard_family_graph_f17_frontier_cert as cert


HERE = Path(__file__).resolve().parent
RHO = Q(111718729, 111718750) ** 9148
W_Z = (1 + 1 / RHO) / 2
KAPPA = 1 / W_Z


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


def direct_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        provenance = result["provenance"]
        if provenance["parameter_scope"] != "base parameter s=0":
            errors.append("parameter scope")
        if "fixed insertion time j" not in provenance["owner_scope"]:
            errors.append("fixed-j scope")
        if "n>j" not in provenance["owner_scope"]:
            errors.append("registered time scope")
        if "no common-target Borel domination" not in provenance["owner_scope"]:
            errors.append("target-set overclaim")

        trace = result["transverse_trace_standard_family_audit"]
        expected_trace_rows = []
        for exponent in (0, 2, 6, 10):
            epsilon = Q(1, 1 << exponent)
            expected_trace_rows.append(
                {
                    "epsilon": str(epsilon),
                    "trace_mass_of_A_epsilon": "1",
                    "uniform_proper_family_mass_of_A_epsilon": str(epsilon),
                    "trace_to_family_mass_ratio": str(1 << exponent),
                }
            )
        if trace["rows"] != expected_trace_rows:
            errors.append("trace rows")
        if trace["rows_sha256"] != cert.digest(expected_trace_rows):
            errors.append("trace rows digest")
        if trace["singular_set_test"] != "nu(Gamma)=1 while sigma(Gamma)=0":
            errors.append("trace singular set")
        if trace["finite_positive_domination_nu_by_sigma"] is not False:
            errors.append("trace domination overclaim")
        if trace["direct_Round42_collision_or_proper_family_minorisation_transfer"] is not False:
            errors.append("Growth transfer overclaim")
        if trace["owner_trace_is_an_unstable_standard_family_law"] is not False:
            errors.append("standard-family overclaim")
        expected_bridge = {
            "trace_extension": (
                "E maps each same-ID owner trace law into the Round42 proper-family class"
            ),
            "trace_recovery": "Tr maps the extended law back to the same owner trace ID",
            "recovery_identity": "Tr composed E = Id on the owner trace laws",
            "positive_operator_norms": "norm(E)<=1 and norm(Tr)<=1",
            "killed_block_survivor_intertwining": (
                "K_trace=Tr composed K_proper composed E"
            ),
            "zero_extension_or_recovery_is_excluded": True,
            "conditional_conclusion": "kappa_trace<=rho<2rho/(1+rho)",
        }
        if trace["conditional_unit_loss_bridge"] != expected_bridge:
            errors.append("conditional unit-loss bridge")
        if trace["conditional_unit_loss_bridge_is_installed"] is not False:
            errors.append("conditional bridge promotion")
        if trace["status"] != (
            "CERTIFIED_TRANSVERSE_TRACE_NOT_PROPER_STANDARD_FAMILY_SEPARATOR"
        ):
            errors.append("trace status")

        closure = result["trace_nullity_and_weighted_closure_audit"]
        nullity = closure["trace_nullity_separator"]
        expected_nullity_rows = []
        for p in (0, 1, 4, 16):
            trace_mass = Q(1, p + 1)
            expected_nullity_rows.append(
                {
                    "block_index": p,
                    "collision_survivor_mass": (
                        "1" if p == 0 else f"rho^{p}/{p + 1}"
                    ),
                    "trace_survivor_mass": str(trace_mass),
                    "constant_rank": 14,
                    "owner_charge": str((1 << 14) * trace_mass),
                }
            )
        if nullity["rows"] != expected_nullity_rows:
            errors.append("nullity rows")
        if nullity["rows_sha256"] != cert.digest(expected_nullity_rows):
            errors.append("nullity rows digest")
        if nullity["collision_and_trace_nullity"] != (
            "mu(intersection Q_p)=nu(intersection Q_p)=0"
        ):
            errors.append("trace-null intersection")
        if nullity["trace_nullity_alone_implies_exponentially_weighted_face_tower"] is not False:
            errors.append("trace-null promotion")
        if nullity["status"] != (
            "CERTIFIED_TRACE_NULLITY_WITHOUT_EXPONENTIAL_TOWER_SEPARATOR"
        ):
            errors.append("nullity status")
        if not Q(1) < W_Z < 1 / RHO or W_Z * RHO != (1 + RHO) / 2:
            errors.append("aggregate weight")

        holder = closure["sharp_conditional_holder_closure"]
        if holder["weighted_sum_criterion"] != "w*delta^(1-1/q)<1":
            errors.append("Holder criterion")
        if holder["fixed_weight_factor"] != "kappa_*=1/w_Z=2rho/(1+rho)":
            errors.append("fixed threshold")
        if holder["if_delta_equals_rho_critical_q_formula"] != (
            "q_*=1/(1-log(kappa_*)/log(rho))"
        ):
            errors.append("critical q formula")
        with localcontext() as ctx:
            ctx.prec = 80
            drho = (Decimal(111718729) / Decimal(111718750)) ** 9148
            dkappa = 2 * drho / (1 + drho)
            critical = Decimal(1) / (Decimal(1) - dkappa.ln() / drho.ln())
            expected_decimal = format(critical, ".34f")
        if holder["if_delta_equals_rho_critical_q_decimal"] != expected_decimal:
            errors.append("critical q decimal")
        if not Decimal("2.0008") < critical < Decimal("2.001"):
            errors.append("critical q bracket")
        if not KAPPA**2 < RHO:
            errors.append("q=2 failure")
        if holder["q_equals_two_fails_exactly"] != (
            "kappa_*<sqrt(rho), directly equivalent to (1-sqrt(rho))^2>0; "
            "after squaring, equivalent to (1-rho)^2>0"
        ):
            errors.append("q=2 equivalence typing")
        if not (1 + RHO) ** 3 < 8 * RHO:
            errors.append("q=3 safe point")
        if not RHO > KAPPA**3:
            errors.append("q=3/2 rho failure")
        if holder["delta_equals_rho_fails_q_three_halves"] is not True:
            errors.append("q=3/2 promotion")
        if holder["kappa_fraction_binary_sha256"] != cert.fraction_digest(KAPPA):
            errors.append("kappa digest")
        if holder["weaker_weight_route_is_unconditional"] is not False:
            errors.append("weak weight overclaim")
        expected_extremizer = {
            "shells": (
                "Q_p=disjoint_union_(r>=p)S_r with nu_0(S_r)="
                "(1-delta)*delta^r, hence nu_0(Q_p)=delta^p"
            ),
            "mark": (
                "g|S_r=delta^(-r/q)/(r+1)^a, a=(q+1)/(2q), "
                "and g_tilde=2^max(14,ceil(log2(g))); for all sufficiently "
                "large r, g<=g_tilde<2g, while finitely many initial shells "
                "do not affect convergence or divergence"
            ),
            "Lq_check": (
                "integral g^q dnu_0 is comparable to sum_(r>=0)"
                "(r+1)^(-(q+1)/2)<infinity"
            ),
            "tail_charge": (
                "b_p is comparable to delta^(p*(1-1/q))/(p+1)^a"
            ),
            "critical_weight_failure": (
                "if w*delta^(1-1/q)=1 then sum_p w^p*b_p is comparable "
                "to sum_p (p+1)^(-a)=infinity because 1/q<a<1"
            ),
            "strict_inequality_is_sharp_for_this_information": True,
        }
        if holder["critical_equality_shell_extremizer"] != expected_extremizer:
            errors.append("critical equality extremizer")
        if holder["status"] != (
            "CERTIFIED_SHARP_CONDITIONAL_TRACE_HOLDER_WEIGHT_REGION"
        ):
            errors.append("Holder status")

        raw = result["raw_rank_moment_criticality_audit"]
        coefficient = Q(9158592, 6875)
        scale = 4 * coefficient * Q(1, 4**14)
        if scale != Q(143103, 7208960000):
            errors.append("raw scale arithmetic")
        if raw["total_mass"] != str(scale):
            errors.append("raw scale")
        if not scale < Q(8064, 5):
            errors.append("raw mass upper")
        expected_raw_rows = []
        for k in (0, 1, 4, 16):
            atom_mass = scale * Q(3, 4 ** (k + 1))
            expected_raw_rows.append(
                {
                    "rank": 14 + k,
                    "atom_mass": str(atom_mass),
                    "tail_after_this_rank": (
                        f"(9158592/6875)*4^(-{14 + k})"
                    ),
                    "2^(2B)_atom_contribution": str(
                        atom_mass * (1 << (2 * (14 + k)))
                    ),
                }
            )
        if raw["rows"] != expected_raw_rows:
            errors.append("raw rows")
        if raw["rows_sha256"] != cert.digest(expected_raw_rows):
            errors.append("raw rows digest")
        contributions = [Q(row["2^(2B)_atom_contribution"]) for row in raw["rows"]]
        if len(set(contributions)) != 1 or contributions[0] != 3 * coefficient:
            errors.append("q=2 constant contributions")
        if raw["finite_moment_range"] != "q<2":
            errors.append("raw finite range")
        if raw["critical_and_supercritical_moments"] != (
            "integral 2^(qB)=infinity for q>=2"
        ):
            errors.append("raw criticality")
        if raw["does_not_assert_actual_owner_law_saturates_the_tail"] is not True:
            errors.append("raw logical scope")
        if raw["status"] != "CERTIFIED_RAW_TAIL_Q_EQUALS_TWO_CRITICAL_SEPARATOR":
            errors.append("raw status")

        graph = result["physical_graph_current_F17_audit"]
        if graph["combined_source_graph_injection_constant"] != "1":
            errors.append("source graph constant")
        if graph["source_graph_injection_status"] != "CERTIFIED":
            errors.append("source graph status")
        if graph["boundary_trace_TV_suffix_constant"] != "1":
            errors.append("trace Piola constant")
        expected_graph_rows = []
        for scale_value in (1, 16, 256, 4096, 65536):
            expected_graph_rows.append(
                {
                    "L": scale_value,
                    "source_domain": f"[0,1/{scale_value}]x[0,1]",
                    "target_domain": f"[0,1]x[0,1/{scale_value}]",
                    "area_preserving_suffix": (
                        f"S_L=diag({scale_value},1/{scale_value})"
                    ),
                    "source_vector": "K=e_1",
                    "source_L1_bulk_cost": str(Q(1, scale_value)),
                    "Piola_target_vector": f"K'={scale_value}*e_1",
                    "target_L1_bulk_cost": "1",
                    "unit_physical_test": "phi(y)=y_1",
                    "target_pairing": "1",
                    "required_multiplier_lower": str(scale_value),
                }
            )
        separator = graph["determinant_one_separator"]
        if separator["rows"] != expected_graph_rows:
            errors.append("graph rows")
        if separator["rows_sha256"] != cert.digest(expected_graph_rows):
            errors.append("graph rows digest")
        if graph["generic_Hdiv_or_L1_graph_space_has_uniform_area_preserving_suffix_constant"] is not False:
            errors.append("generic Hdiv overclaim")
        if graph["physical_F17_suffix_constant"] != "NOT_CERTIFIED":
            errors.append("F17 promotion")
        if graph["complete_strong_F13_intertwiner"] != "NOT_CERTIFIED":
            errors.append("strong F13 promotion")
        if graph["status"] != (
            "CERTIFIED_SOURCE_GRAPH_INJECTION_AND_BULK_PIOLA_SEPARATOR"
        ):
            errors.append("graph status")

        gate3 = result["Gate3_common_graph_conditional_bridge"]
        expected_conditions = [
            "same physical branch/component and owner IDs for every moving Gate3 slot",
            "artificial and duplicate traces assembled before absolute values",
            "uniform moving-test convergence on the component-indexed atlas",
            "bounded physical observable inclusion and the F17 suffix constant",
            "all 18 operator fields on one common recovered block",
            "cemetery and growing-depth no-|s|^-1 current tail",
        ]
        if gate3["conditions_still_required"] != expected_conditions:
            errors.append("Gate3 conditions")
        if gate3["conditions_sha256"] != cert.digest(expected_conditions):
            errors.append("Gate3 conditions digest")
        if gate3["physical_Qs_Rs_lift_quotient"] != "NOT_CERTIFIED":
            errors.append("Gate3 lift promotion")
        if gate3["dynamic_branch_record_MT_DQ"] != "NOT_CERTIFIED":
            errors.append("Gate3 MT_DQ promotion")
        if gate3["automatic_promotion_from_source_graph_injection"] is not False:
            errors.append("Gate3 automatic promotion")

        tech = result["latest_technology_audit"]
        if tech["official_versions_checked_2026_07_20"] != [
            "2606.10155v1",
            "2502.07765v2",
        ]:
            errors.append("technology versions")
        if tech["singular_transverse_owner_trace_injection_found"] is not False:
            errors.append("technology trace overclaim")
        if tech["vector_current_Hdiv_F17_with_numeric_suffix_constant_found"] is not False:
            errors.append("technology F17 overclaim")

        update = result["Gate5_maturity_update"]
        if update["new_global_field_completed"] is not None:
            errors.append("field promotion")
        if update["current_global_maturity"] != "10/18":
            errors.append("maturity")
        if update["complete_18_field_operator_block_count"] != 0:
            errors.append("block count")

        strict = result["strict_nonpromotion"]
        required = {
            "fixed_insertion_same_ID_owner_tail_transfer": "CERTIFIED_PREVIOUSLY",
            "owner_trace_is_proper_standard_family": "NOT_CERTIFIED",
            "trace_to_proper_standard_family_injection": "NOT_CERTIFIED",
            "trace_nullity_of_never_return_cemetery": "NOT_CERTIFIED",
            "quantitative_trace_survivor_contraction": "NOT_CERTIFIED",
            "fixed_weight_q_above_critical_owner_moment": "NOT_CERTIFIED",
            "unconditional_weak_weight_face_resolvent": "NOT_CERTIFIED",
            "same_ID_full_ZB_one_step_recurrence": "NOT_CERTIFIED",
            "unconditional_aggregate_ZB_resolvent": "NOT_CERTIFIED",
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "physical_graph_current_source_injection": "CERTIFIED",
            "physical_F17_bulk_suffix_constant": "NOT_CERTIFIED",
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
        if set(strict) != set(required):
            errors.append("strict key set")
        for key, value in required.items():
            if strict.get(key) != value:
                errors.append(f"strict {key}")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"result structure: {exc}")
    return errors


def verify_object(manifest: dict[str, Any], replay: bool) -> list[str]:
    errors: list[str] = []
    expected_keys = {
        "schema",
        "certificate_sha256",
        "verifier_sha256",
        "dependencies",
        "result",
        "verdict",
    }
    if set(manifest) != expected_keys:
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
    errors.extend(direct_errors(result))
    if manifest.get("verdict") != result.get("strict_nonpromotion"):
        errors.append("verdict projection")
    if replay:
        try:
            expected_result = cert.build_result()
        except Exception as exc:
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


def fast_integrity_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(manifest) != {
        "schema",
        "certificate_sha256",
        "verifier_sha256",
        "dependencies",
        "result",
        "verdict",
    }:
        errors.append("manifest keys")
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


def hostile_paths() -> list[tuple[str, ...]]:
    trace = "transverse_trace_standard_family_audit"
    closure = "trace_nullity_and_weighted_closure_audit"
    nullity = "trace_nullity_separator"
    holder = "sharp_conditional_holder_closure"
    raw = "raw_rank_moment_criticality_audit"
    graph = "physical_graph_current_F17_audit"
    gate3 = "Gate3_common_graph_conditional_bridge"
    tech = "latest_technology_audit"
    strict = "strict_nonpromotion"
    paths: list[tuple[str, ...]] = [
        ("result", "provenance", "parameter_scope"),
        ("result", "provenance", "owner_scope"),
        ("result", "provenance", "claim_type"),
        ("result", trace, "typed_owner_law"),
        ("result", trace, "separator_space"),
        ("result", trace, "owner_trace"),
        ("result", trace, "singular_set_test"),
        ("result", trace, "rows_sha256"),
        ("result", trace, "finite_positive_domination_nu_by_sigma"),
        ("result", trace, "direct_Round42_collision_or_proper_family_minorisation_transfer"),
        ("result", trace, "owner_trace_is_an_unstable_standard_family_law"),
        ("result", trace, "minimal_missing_bridge"),
        ("result", trace, "conditional_unit_loss_bridge"),
        ("result", trace, "conditional_unit_loss_bridge_is_installed"),
        ("result", trace, "status"),
        ("result", closure, nullity, "nested_survivors"),
        ("result", closure, nullity, "collision_and_trace_nullity"),
        ("result", closure, nullity, "owner_charge"),
        ("result", closure, nullity, "weighted_owner_charge"),
        ("result", closure, nullity, "recurrence_conclusion"),
        ("result", closure, nullity, "rows_sha256"),
        ("result", closure, nullity, "trace_nullity_alone_implies_exponentially_weighted_face_tower"),
        ("result", closure, nullity, "status"),
        ("result", closure, holder, "required_common_measure_typing"),
        ("result", closure, holder, "hypotheses"),
        ("result", closure, holder, "holder_bound"),
        ("result", closure, holder, "weighted_sum_criterion"),
        ("result", closure, holder, "fixed_weight_factor"),
        ("result", closure, holder, "if_delta_equals_rho_critical_q_formula"),
        ("result", closure, holder, "if_delta_equals_rho_critical_q_decimal"),
        ("result", closure, holder, "q_equals_two_fails_exactly"),
        ("result", closure, holder, "q_equals_three_is_safe"),
        ("result", closure, holder, "delta_equals_rho_fails_q_three_halves"),
        ("result", closure, holder, "kappa_fraction_binary_sha256"),
        ("result", closure, holder, "weaker_weight_route_is_unconditional"),
        ("result", closure, holder, "critical_equality_shell_extremizer"),
        ("result", closure, holder, "status"),
        ("result", raw, "separator_law"),
        ("result", raw, "total_mass"),
        ("result", raw, "tail_identity"),
        ("result", raw, "moment_ratio"),
        ("result", raw, "finite_moment_range"),
        ("result", raw, "critical_and_supercritical_moments"),
        ("result", raw, "rows_sha256"),
        ("result", raw, "does_not_assert_actual_owner_law_saturates_the_tail"),
        ("result", raw, "status"),
        ("result", graph, "source_current"),
        ("result", graph, "physical_test_norm"),
        ("result", graph, "bulk_injection"),
        ("result", graph, "trace_injection"),
        ("result", graph, "combined_source_graph_injection_constant"),
        ("result", graph, "source_graph_injection_status"),
        ("result", graph, "area_preserving_suffix_identity"),
        ("result", graph, "boundary_trace_TV_suffix_constant"),
        ("result", graph, "bulk_vector_suffix_bound"),
        ("result", graph, "determinant_one_separator", "rows_sha256"),
        ("result", graph, "generic_Hdiv_or_L1_graph_space_has_uniform_area_preserving_suffix_constant"),
        ("result", graph, "precise_missing_billiard_input"),
        ("result", graph, "required_F17_threshold"),
        ("result", graph, "physical_F17_suffix_constant"),
        ("result", graph, "complete_strong_F13_intertwiner"),
        ("result", graph, "status"),
        ("result", gate3, "available_join"),
        ("result", gate3, "conditional_use"),
        ("result", gate3, "conditions_sha256"),
        ("result", gate3, "physical_Qs_Rs_lift_quotient"),
        ("result", gate3, "dynamic_branch_record_MT_DQ"),
        ("result", gate3, "automatic_promotion_from_source_graph_injection"),
        ("result", gate3, "status"),
        ("result", tech, "official_versions_checked_2026_07_20"),
        ("result", tech, "official_source_archive_sha256"),
        ("result", tech, "singular_transverse_owner_trace_injection_found"),
        ("result", tech, "vector_current_Hdiv_F17_with_numeric_suffix_constant_found"),
        ("result", tech, "status"),
        ("result", "Gate5_maturity_update", "new_global_field_completed"),
        ("result", "Gate5_maturity_update", "current_global_maturity"),
        ("result", "Gate5_maturity_update", "complete_18_field_operator_block_count"),
    ]
    for key in (
        "owner_trace_is_proper_standard_family",
        "trace_to_proper_standard_family_injection",
        "trace_nullity_of_never_return_cemetery",
        "quantitative_trace_survivor_contraction",
        "fixed_weight_q_above_critical_owner_moment",
        "unconditional_weak_weight_face_resolvent",
        "same_ID_full_ZB_one_step_recurrence",
        "unconditional_aggregate_ZB_resolvent",
        "return_depth_weighted_face_integrability",
        "physical_graph_current_source_injection",
        "physical_F17_bulk_suffix_constant",
        "complete_all_face_F10",
        "strong_F13",
        "F14_F15_F17_F18",
        "strong_cemetery",
        "Gate3_Qs_Rs_physical_lift_quotient",
        "Gate3_MT_DQ",
        "Gate3",
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
