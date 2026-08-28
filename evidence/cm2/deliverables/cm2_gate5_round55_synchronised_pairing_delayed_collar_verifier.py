#!/usr/bin/env python3
"""Fail-closed verifier for the Round-55 synchronised/delayed-collar leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round55_synchronised_pairing_delayed_collar_cert as cert


HERE = Path(__file__).resolve().parent
BLOCK_DEPTH = 9148
RHO = Q(111718729, 111718750) ** BLOCK_DEPTH
W_Z = (1 + 1 / RHO) / 2
GAMMA = Q(2000, 1999) * (1 + 48 * BLOCK_DEPTH) * Q(900337, 901685) ** BLOCK_DEPTH
ALPHA_LOWER = Q(12409395510954121, 10**19)
ALPHA_UPPER = Q(12409395510954122, 10**19)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_safe_local_regular_file(path: Path, base: Path = HERE) -> bool:
    """Check the unresolved leaf before resolving, then enforce one directory."""
    if path.is_symlink() or not path.is_file():
        return False
    return path.resolve().parent == base.resolve()


def strict_load(path: Path, base: Path = HERE) -> dict[str, Any]:
    if not is_safe_local_regular_file(path, base):
        raise RuntimeError("unsafe manifest")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=cert.strict_object,
        parse_constant=cert.reject_json_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError("manifest root")
    return value


def expected_pair_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_atom": "0",
            "source_mass": "1/2",
            "H_image": "0",
            "M_image": "0",
            "synchronised_cost": "0",
        },
        {
            "source_atom": "1",
            "source_mass": "1/2",
            "H_image": "1",
            "M_image": "1",
            "synchronised_cost": "0",
        },
    ]


def expected_collar_rows() -> list[dict[str, Any]]:
    rows = []
    for k in range(1, 9):
        mass = Q(1, 2**k)
        ell = Q(1, 2 ** (k + 1))
        rows.append(
            {
                "dyadic_level_k": k,
                "level_trace_mass_m_k": str(mass),
                "collar_length_ell_k": str(ell),
                "inverse_collar_debt_m_k_over_ell_k": str(mass / ell),
                "partial_debt_through_level_k": str(2 * k),
            }
        )
    return rows


def expected_delay_rows() -> list[dict[str, Any]]:
    return [
        {
            "level_k": k,
            "initial_debt": "z_(k,0)=2^(k+1)*m_k",
            "scheduled_C24_blocks": k + 1,
            "contracted_initial_term": "(2*gamma)^(k+1)*m_k<m_k",
        }
        for k in (0, 1, 2, 4, 8, 16)
    ]


def decimal_alpha() -> Decimal:
    with localcontext() as context:
        context.prec = 100
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        weight = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        return +(weight.ln() / Decimal(2).ln())


def expected_strict() -> dict[str, Any]:
    return {
        "Round54_product_pairing_bound_remains_valid": "CERTIFIED",
        "synchronised_same_source_pairing_bound": (
            "CERTIFIED_ALTERNATIVE_SAME_SOURCE_WITNESS_SOMETIMES_STRICTLY_BETTER"
        ),
        "combined_minimum_pairing_bound": (
            "CERTIFIED_NEVER_WORSE_THAN_ROUND54_PRODUCT"
        ),
        "physical_same_source_pair_rate": "NOT_CERTIFIED",
        "unconditional_signed_BL_resolvent": "NOT_CERTIFIED",
        "positive_F10_or_cemetery_from_signed_pairing": "NOT_CERTIFIED",
        "full_A_col_mass_implies_finite_Z_col": "FALSE_BY_CERTIFIED_COUNTEREXAMPLE",
        "analytic_transverse_full_mass_infinite_Z_col_separator": "CERTIFIED",
        "dyadic_delayed_recovery_abstract_theorem": "CERTIFIED_CONDITIONAL",
        "weak_clearance_moment_exact_threshold": "CERTIFIED",
        "physical_weak_clearance_moment": "NOT_CERTIFIED",
        "physical_k_plus_1_C24_suffix_schedule": "NOT_CERTIFIED",
        "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
        "quantitative_trace_survivor_contraction": "NOT_CERTIFIED",
        "unconditional_trace_resolvent": "NOT_CERTIFIED",
        "Arens_Eells_normal_trace_physical_import": "NOT_CERTIFIED",
        "complete_all_face_F10": "NOT_CERTIFIED",
        "strong_F13": "NOT_CERTIFIED",
        "F14_F15_F17_F18": "NOT_CERTIFIED",
        "strong_cemetery": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "Gate5_maturity": "10/18",
        "complete_18_field_operator_block_count": 0,
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def direct_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if result["schema"] != cert.RESULT_SCHEMA:
            errors.append("result schema")
        provenance = result["provenance"]
        if provenance["dependency_sha256"] != cert.DEPENDENCIES:
            errors.append("provenance dependencies")
        if provenance["old_artifacts_modified"] is not False:
            errors.append("append-only provenance")
        if "no moving-sequence theorem" not in provenance["parameter_scope"]:
            errors.append("parameter scope")
        if any(
            token not in provenance["claim_type"]
            for token in ("alternative synchronised", "never-worse minimum", "conditional dyadic")
        ):
            errors.append("claim scope")

        pair = result["synchronised_hit_miss_pairing"]
        if all(
            token in pair["scope"]
            for token in ("immutable physical source", "Jordan", "H_p,M_p")
        ) is False:
            errors.append("pair source scope")
        if pair["positive_marginals"] != (
            "mu_p^+=H_p*lambda_p^+ + M_p*lambda_p^- and "
            "mu_p^-=M_p*lambda_p^+ + H_p*lambda_p^-"
        ):
            errors.append("pair marginals definition")
        coupling = pair["synchronised_coupling"]
        if any(
            token not in coupling
            for token in (
                "H_p(x) tensor M_p(x)",
                "lambda_p^+(x)",
                "M_p(x) tensor H_p(x)",
                "lambda_p^-(x)",
            )
        ):
            errors.append("synchronised coupling")
        if pair["first_marginal"] != "(pr_1)_*pi_p^sync=mu_p^+":
            errors.append("first marginal")
        if pair["second_marginal"] != "(pr_2)_*pi_p^sync=mu_p^-":
            errors.append("second marginal")
        if pair["total_mass"] != "mass(pi_p^sync)=abs(lambda_p)(source)=m_p":
            errors.append("pair total mass")
        if "no measurable selection" not in pair["Borel_typing"]:
            errors.append("Borel pair typing")
        if pair["BL_bound"] != "norm(J_p)_(BL*)<=d_p^sync":
            errors.append("pair BL bound")
        if pair["Round54_product_cost"] != (
            "d_p^product=integral min(2,d(y+,y-)) d pi_p^product(y+,y-)"
        ):
            errors.append("product cost definition")
        if pair["best_available_cost"] != (
            "d_p^best=min(d_p^product,d_p^sync)"
        ):
            errors.append("best cost definition")
        if pair["combined_BL_bound"] != "norm(J_p)_(BL*)<=d_p^best":
            errors.append("combined BL bound")
        if any(
            token not in pair["comparison_scope"]
            for token in ("not totally ordered", "minimum", "never worse")
        ):
            errors.append("pair comparison scope")
        if "integral min(2,d(h_p(x),m_p(x)))" not in pair[
            "deterministic_reduction"
        ]:
            errors.append("deterministic pair reduction")
        if "w_Z*delta_sync<1" not in pair[
            "same_source_rate_sufficient_condition"
        ]:
            errors.append("conditional pair rate")
        pair_sep = pair["product_coupling_nonsharp_separator"]
        pair_rows = expected_pair_rows()
        if pair_sep["rows"] != pair_rows:
            errors.append("pair separator rows")
        if pair_sep["rows_sha256"] != cert.digest(pair_rows):
            errors.append("pair separator digest")
        if pair_sep["current"] != "J=(H-M)lambda=0":
            errors.append("zero current separator")
        if pair_sep["synchronised_cost"] != "0":
            errors.append("zero sync cost")
        if pair_sep["Round54_normalized_product_cost"] != "1/2":
            errors.append("product cost arithmetic")
        # On the two-point law, the normalized product has two off-diagonal
        # atoms of mass 1/4 and therefore cost 1/2.
        product_cost = Q(1, 4) + Q(1, 4)
        if product_cost != Q(1, 2):
            errors.append("product separator independent arithmetic")
        reverse = pair["synchronised_coupling_nonsharp_separator"]
        if any(
            token not in reverse["model"]
            for token in ("H=identity", "M=flip", "M(0)=1", "M(1)=0")
        ):
            errors.append("reverse pair separator model")
        if reverse["current"] != "J=(H-M)lambda=0":
            errors.append("reverse zero current")
        if reverse["synchronised_cost"] != "1":
            errors.append("reverse sync cost")
        if reverse["Round54_normalized_product_cost"] != "1/2":
            errors.append("reverse product cost")
        if any(
            token not in reverse["conclusion"]
            for token in ("can be worse", "no global ordering", "d_p^best")
        ):
            errors.append("reverse comparison conclusion")
        no_rate = pair["no_automatic_rate_separator"]
        if no_rate["current"] != "J_p=delta_0-delta_1":
            errors.append("no-rate current")
        if no_rate["exact_BL_norm"] != "1" or no_rate[
            "synchronised_cost"
        ] != "1":
            errors.append("no-rate norm")
        if pair["physical_same_source_pair_rate"] != "NOT_CERTIFIED":
            errors.append("physical pair-rate promotion")
        if pair["positive_face_or_cemetery_consequence"] != "NOT_CERTIFIED":
            errors.append("positive pair promotion")
        if pair["status"] != (
            "CERTIFIED_ALTERNATIVE_SAME_SOURCE_WITNESS_SOMETIMES_STRICTLY_BETTER"
        ):
            errors.append("pair status")

        collar = result["analytic_transverse_full_mass_collar_separator"]
        for token in ("t in (-1,1)", "nu=dt/2", "b_1(t)=t", "transverse"):
            if token not in collar["model"]:
                errors.append("analytic collar model")
                break
        if "exactly one analytic transverse zero" not in collar[
            "no_grazing_accumulation"
        ]:
            errors.append("single crossing")
        if collar["A_col_trace_mass"] != "nu(A_col)=1":
            errors.append("full A_col mass")
        if collar["zero_clearance_trace_mass"] != "nu({d=0})=0":
            errors.append("null zero-clearance mass")
        if collar["level_mass"] != "m_k=nu(C_k)=2^(-k)":
            errors.append("dyadic level mass")
        if collar["level_debt"] != "m_k/ell_k=2 for every k>=1":
            errors.append("dyadic level debt")
        collar_rows = expected_collar_rows()
        if collar["rows"] != collar_rows:
            errors.append("collar rows")
        if collar["rows_sha256"] != cert.digest(collar_rows):
            errors.append("collar rows digest")
        for row in collar_rows:
            if Q(row["level_trace_mass_m_k"]) / Q(
                row["collar_length_ell_k"]
            ) != 2:
                errors.append("collar row arithmetic")
                break
        if collar["collar_debt"] != "Z_col=sum_(k>=1) 2=infinity":
            errors.append("collar divergence")
        if "2/abs(t)<=ell(t)^(-1)<4/abs(t)" not in collar[
            "equivalent_integral_bound"
        ]:
            errors.append("collar integral comparison")
        if "Z_parent,B=2^14=16384" not in collar["finite_parent_debt"]:
            errors.append("finite parent debt")
        if "full A_col trace mass" not in collar["logical_conclusion"]:
            errors.append("collar conclusion")
        if collar["status"] != (
            "CERTIFIED_FULL_MASS_ANALYTIC_TRANSVERSE_INFINITE_COLLAR_DEBT_SEPARATOR"
        ):
            errors.append("collar status")

        delayed = result["dyadic_debt_layer_delayed_recovery"]
        if "z_(k,0)=2^(k+1)*m_k" not in delayed["abstract_layer_typing"]:
            errors.append("initial layer debt")
        if any(
            token not in delayed["required_same_operator_hypothesis"]
            for token in ("Round54", "Round42", "O_s^9148", "same owner IDs")
        ):
            errors.append("same-operator hypothesis")
        if "k+1 consecutive compatible" not in delayed[
            "required_suffix_horizon"
        ] or "m_(k,r)<=m_k" not in delayed["required_suffix_horizon"]:
            errors.append("suffix horizon hypothesis")
        if delayed["one_block_recurrence"] != (
            "z_(k,r+1)<=gamma*z_(k,r)+Z0*m_(k,r)"
        ):
            errors.append("Growth recurrence")
        constants = delayed["exact_constants"]
        if constants["gamma_bracket"] != "0.4999<gamma<1/2":
            errors.append("gamma bracket")
        if not Q(4999, 10000) < GAMMA < Q(1, 2):
            errors.append("gamma exact arithmetic")
        if constants["gamma_fraction_binary_sha256"] != cert.fraction_digest(
            GAMMA
        ):
            errors.append("gamma digest")
        if constants["Z0"] != "Z0=2/delta_open=54/(5*delta_9148)":
            errors.append("Z0 typing")
        if "gamma^(k+1)*2^(k+1)*m_k" not in delayed[
            "iteration_at_delay_k_plus_1"
        ]:
            errors.append("iterated recurrence")
        if "C_rec=1+Z0/(1-gamma)" not in delayed[
            "uniform_recovered_bound"
        ] or "2*gamma<1" not in delayed["uniform_recovered_bound"]:
            errors.append("uniform recovery")
        delay_rows = expected_delay_rows()
        if delayed["sample_levels"] != delay_rows:
            errors.append("delay rows")
        if delayed["sample_levels_sha256"] != cert.digest(delay_rows):
            errors.append("delay rows digest")
        if "sum_k w_Z^(k+1)*z_(k,k+1)" not in delayed[
            "discounted_emission_ledger"
        ]:
            errors.append("discounted emission")
        if delayed["weak_clearance_moment"] != (
            "M_col,w=sum_k w_Z^(k+1)*m_k<infinity"
        ):
            errors.append("weak moment")
        if "w_Z^2/(2-w_Z)<infinity" not in delayed[
            "strictly_weaker_than_Z_col"
        ]:
            errors.append("weak/strong separator")
        if "w_Z*2^(-alpha)<1" not in delayed[
            "clearance_tail_sufficient_condition"
        ]:
            errors.append("tail sufficient condition")
        if delayed["exact_critical_exponent"] != "alpha_*=log(w_Z)/log(2)":
            errors.append("critical exponent")
        if "iff alpha>alpha_*" not in delayed[
            "critical_iff_for_geometric_dyadic_tail"
        ]:
            errors.append("critical iff")
        if not Q(1) < W_Z < Q(2):
            errors.append("weight window")
        alpha = decimal_alpha()
        lower = Decimal(ALPHA_LOWER.numerator) / Decimal(ALPHA_LOWER.denominator)
        upper = Decimal(ALPHA_UPPER.numerator) / Decimal(ALPHA_UPPER.denominator)
        if not lower < alpha < upper:
            errors.append("critical rational bracket arithmetic")
        if delayed["critical_decimal_100_digit_audit"] != format(alpha, "f"):
            errors.append("critical decimal replay")
        if delayed["rho_fraction_binary_sha256"] != cert.fraction_digest(RHO):
            errors.append("rho digest")
        if delayed["weight_fraction_binary_sha256"] != cert.fraction_digest(W_Z):
            errors.append("weight digest")
        for key in (
            "physical_weak_clearance_moment",
            "physical_k_plus_1_C24_suffix_schedule",
            "physical_Round54_to_Round42_same_operator_join",
            "short_horizon_remainder_ledger",
            "quantitative_trace_contraction",
            "unconditional_trace_resolvent",
        ):
            if delayed[key] != "NOT_CERTIFIED":
                errors.append(f"delayed promotion {key}")
        if delayed["status"] != (
            "CERTIFIED_CONDITIONAL_DYADIC_DELAYED_RECOVERY_THEOREM_"
            "WITH_EXACT_WEAK_MOMENT_THRESHOLD"
        ):
            errors.append("delayed status")

        tech = result["Arens_Eells_normal_trace_technology_audit"]
        if tech["query_date"] != "2026-07-20":
            errors.append("technology date")
        if tech["bibliographic_pointer_only"] is not True:
            errors.append("technology dependency scope")
        if tech["source"]["arxiv"] != "2503.09536v2":
            errors.append("technology source")
        if any(
            token not in tech["relevant_typed_result"]
            for token in ("Arens-Eells", "bounded Lipschitz", "onto", "not-necessarily-linear")
        ):
            errors.append("technology theorem scope")
        if any(
            token not in tech["why_no_promotion"]
            for token in ("positivity", "same-ID", "numeric", "rho-rate")
        ):
            errors.append("technology nonpromotion")
        if tech["external_source_vendored_or_used_as_dependency"] is not False:
            errors.append("technology unpinned import")
        if tech["Gate5_field_credit"] != "NONE":
            errors.append("technology field credit")

        maturity = result["Gate5_maturity_update"]
        if maturity["previous_global_maturity"] != "10/18":
            errors.append("previous maturity")
        if maturity["new_global_field_completed"] is not None:
            errors.append("field promotion")
        if maturity["current_global_maturity"] != "10/18":
            errors.append("current maturity")
        if maturity["complete_18_field_operator_block_count"] != 0:
            errors.append("complete block promotion")
        if result["strict_nonpromotion"] != expected_strict():
            errors.append("strict nonpromotion")
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append(f"malformed result: {exc}")
    return errors


def dependency_integrity_errors(
    dependencies: dict[str, str] | None = None, base: Path = HERE
) -> list[str]:
    """Recheck every dependency on disk, including unresolved symlink status."""
    selected = cert.DEPENDENCIES if dependencies is None else dependencies
    errors: list[str] = []
    for name, expected_sha in selected.items():
        if Path(name).name != name:
            errors.append(f"unsafe dependency name: {name}")
            continue
        path = base / name
        if not is_safe_local_regular_file(path, base):
            errors.append(f"unsafe or missing dependency: {name}")
            continue
        if sha(path) != expected_sha:
            errors.append(f"dependency hash: {name}")
    return errors


def fast_integrity_errors(manifest: dict[str, Any]) -> list[str]:
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
        errors.append("dependencies")
    errors.extend(dependency_integrity_errors())
    result = manifest.get("result")
    if not isinstance(result, dict):
        errors.append("result")
        return errors
    replay_digest = result.get("internal_replay_digest")
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    if replay_digest != cert.digest(payload):
        errors.append("internal replay digest")
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
    paths: list[tuple[str, ...]] = [
        ("result", "schema"),
        ("result", "provenance", "dependency_sha256"),
        ("result", "provenance", "old_artifacts_modified"),
        ("result", "provenance", "parameter_scope"),
        ("result", "provenance", "claim_type"),
    ]
    sections = {
        "synchronised_hit_miss_pairing": (
            "scope",
            "positive_marginals",
            "synchronised_coupling",
            "first_marginal",
            "second_marginal",
            "total_mass",
            "Borel_typing",
            "BL_cost",
            "BL_bound",
            "Round54_product_cost",
            "best_available_cost",
            "combined_BL_bound",
            "comparison_scope",
            "deterministic_reduction",
            "same_source_rate_sufficient_condition",
            "product_coupling_nonsharp_separator",
            "synchronised_coupling_nonsharp_separator",
            "no_automatic_rate_separator",
            "physical_same_source_pair_rate",
            "positive_face_or_cemetery_consequence",
            "status",
        ),
        "analytic_transverse_full_mass_collar_separator": (
            "model",
            "no_grazing_accumulation",
            "collar_admissible_set",
            "A_col_trace_mass",
            "zero_clearance_trace_mass",
            "dyadic_level",
            "level_mass",
            "level_debt",
            "rows",
            "rows_sha256",
            "collar_debt",
            "equivalent_integral_bound",
            "finite_parent_debt",
            "logical_conclusion",
            "status",
        ),
        "dyadic_debt_layer_delayed_recovery": (
            "abstract_layer_typing",
            "required_same_operator_hypothesis",
            "required_suffix_horizon",
            "one_block_recurrence",
            "exact_constants",
            "iteration_at_delay_k_plus_1",
            "uniform_recovered_bound",
            "sample_levels",
            "sample_levels_sha256",
            "discounted_emission_ledger",
            "weak_clearance_moment",
            "strictly_weaker_than_Z_col",
            "clearance_tail_sufficient_condition",
            "exact_critical_exponent",
            "critical_iff_for_geometric_dyadic_tail",
            "critical_rational_bracket",
            "critical_decimal_100_digit_audit",
            "rho_decimal_100_digit_audit",
            "weight_decimal_100_digit_audit",
            "rho_fraction_binary_sha256",
            "weight_fraction_binary_sha256",
            "physical_weak_clearance_moment",
            "physical_k_plus_1_C24_suffix_schedule",
            "physical_Round54_to_Round42_same_operator_join",
            "short_horizon_remainder_ledger",
            "quantitative_trace_contraction",
            "unconditional_trace_resolvent",
            "status",
        ),
        "Arens_Eells_normal_trace_technology_audit": (
            "query_date",
            "bibliographic_pointer_only",
            "source",
            "relevant_typed_result",
            "possible_use",
            "why_no_promotion",
            "external_source_vendored_or_used_as_dependency",
            "Gate5_field_credit",
            "status",
        ),
        "Gate5_maturity_update": (
            "previous_global_maturity",
            "new_global_field_completed",
            "newly_certified_sublayers",
            "reason_no_new_field_credit",
            "current_global_maturity",
            "complete_18_field_operator_block_count",
        ),
    }
    for section, keys in sections.items():
        paths.extend(("result", section, key) for key in keys)
    paths.extend(
        ("result", "strict_nonpromotion", key) for key in expected_strict()
    )
    return paths


def replacement_for(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if value is None:
        return "CERTIFIED"
    if isinstance(value, dict):
        return {}
    if isinstance(value, list):
        return []
    return "HOSTILE_MUTATION"


def refresh_result_integrity(mutant: dict[str, Any]) -> None:
    result = mutant["result"]
    payload = dict(result)
    payload.pop("internal_replay_digest", None)
    result["internal_replay_digest"] = cert.digest(payload)
    mutant["verdict"] = result["strict_nonpromotion"]


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    failures = 0
    total = 0
    for path in hostile_paths():
        total += 1
        mutant = copy.deepcopy(manifest)
        current: Any = mutant
        for key in path:
            current = current[key]
        set_path(mutant, path, replacement_for(current))
        refresh_result_integrity(mutant)
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
        if not verify_object(mutant, replay=False):
            failures += 1
    total += 1
    mutant = copy.deepcopy(manifest)
    mutant["unexpected_key"] = True
    if not verify_object(mutant, replay=False):
        failures += 1
    total += 1
    mutant = copy.deepcopy(manifest)
    mutant["result"]["internal_replay_digest"] = "0" * 64
    if not verify_object(mutant, replay=False):
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
    with tempfile.TemporaryDirectory(prefix="cm2-r55-g5-hostile-") as temp_name:
        base = Path(temp_name)
        real_manifest = base / "real-manifest.json"
        real_manifest.write_text("{}\n", encoding="utf-8")
        linked_manifest = base / "linked-manifest.json"
        linked_manifest.symlink_to(real_manifest.name)
        total += 1
        try:
            strict_load(linked_manifest, base=base)
        except RuntimeError:
            pass
        else:
            failures += 1

        dependency = base / "dependency.json"
        dependency.write_bytes(b"frozen dependency\n")
        valid = {dependency.name: sha(dependency)}
        total += 1
        if dependency_integrity_errors(valid, base=base):
            failures += 1

        total += 1
        if not dependency_integrity_errors(
            {"missing.json": "0" * 64}, base=base
        ):
            failures += 1

        total += 1
        if not dependency_integrity_errors(
            {dependency.name: "0" * 64}, base=base
        ):
            failures += 1

        linked_dependency = base / "linked-dependency.json"
        linked_dependency.symlink_to(dependency.name)
        total += 1
        if not dependency_integrity_errors(
            {linked_dependency.name: sha(dependency)}, base=base
        ):
            failures += 1

        total += 1
        if not dependency_integrity_errors(
            {"../outside.json": "0" * 64}, base=base
        ):
            failures += 1
    return total - failures, total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=cert.DEFAULT_MANIFEST)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--integrity-only", action="store_true")
    actions.add_argument("--replay", action="store_true")
    actions.add_argument("--self-test", action="store_true")
    actions.add_argument("--reemit", action="store_true")
    args = parser.parse_args()
    try:
        # The unresolved user-supplied leaf must be checked before resolve(),
        # otherwise an internal symlink would be silently converted to its target.
        manifest = strict_load(args.manifest)
        manifest_path = args.manifest.resolve()
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1
    replay = args.replay or args.self_test or args.reemit or not args.integrity_only
    errors = verify_object(manifest, replay=replay)
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    if args.self_test:
        passed, total = self_test(manifest)
        print(f"HOSTILE_SELF_TEST: {passed}/{total}")
        return 0 if passed == total else 1
    if args.reemit:
        emitted = cert.render_manifest(Path(__file__).resolve())
        if emitted != manifest_path.read_bytes():
            print("FAIL: reemitted manifest is not byte-identical")
            return 1
        print("REEMIT: BYTE_IDENTICAL")
        return 0
    if args.integrity_only:
        print("INTEGRITY_ONLY: PASS")
        return 0
    if args.replay:
        print("REPLAY: PASS")
        return 0
    print("SAFE_MANIFEST: PASS")
    print("GATE5_MATURITY: 10/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
