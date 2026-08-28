#!/usr/bin/env python3
"""Fail-closed verifier for the Round-57 Gate-5 frontier leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from decimal import Decimal, ROUND_CEILING, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round57_clearance_negative_moment_ot_frontier_cert as cert


HERE = Path(__file__).resolve().parent
BLOCK_DEPTH = 9148
GAMMA = Q(2000, 1999) * (1 + 48 * BLOCK_DEPTH) * Q(900337, 901685) ** BLOCK_DEPTH
RHO = Q(111718729, 111718750) ** BLOCK_DEPTH
W_Z = (1 + 1 / RHO) / 2


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_safe_local_regular_file(path: Path, base: Path = HERE) -> bool:
    return path.is_file() and not path.is_symlink() and path.resolve().parent == base.resolve()


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


def independent_decimals() -> dict[str, Decimal]:
    with localcontext() as context:
        context.prec = 120
        gamma = (
            Decimal(2000)
            / Decimal(1999)
            * Decimal(1 + 48 * BLOCK_DEPTH)
            * (Decimal(900337) / Decimal(901685)) ** BLOCK_DEPTH
        )
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        weight = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        beta = Decimal(2).ln() / (-gamma.ln())
        alpha = beta * weight.ln() / Decimal(2).ln()
        return {
            "gamma": +gamma,
            "rho": +rho,
            "weight": +weight,
            "beta": +beta,
            "alpha_opt": +alpha,
            "inverse_square_pullback_power_limit": +(Decimal(2) / Decimal(3) / alpha),
        }


def independent_clock(k: int, beta: Decimal) -> int:
    return int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))


def expected_equivalence_rows() -> list[dict[str, Any]]:
    beta = independent_decimals()["beta"]
    rows: list[dict[str, Any]] = []
    for k in (0, 1, 2, 16, 4381, 10000):
        rows.append(
            {
                "dyadic_level_k": k,
                "optimal_clock_r_k": independent_clock(k, beta),
                "clearance_cell": (
                    "delta=1" if k == 0 else "2^(-k)<=delta<2^(-(k-1))"
                ),
                "pointwise_comparison": (
                    "w_Z^beta*delta^(-alpha_opt)<=w_Z^r_k<"
                    "w_Z^(beta+1)*2^alpha_opt*delta^(-alpha_opt)"
                ),
            }
        )
    return rows


def expected_separator_rows() -> list[dict[str, Any]]:
    alpha = independent_decimals()["alpha_opt"]
    rows: list[dict[str, Any]] = []
    for n in (1, 100, 500, 805, 806, 807, 1000, 2000):
        rows.append(
            {
                "record_n": n,
                "mass_p_n": "2^(-n)",
                "clearance_d_n": "2^(-n^2)",
                "dyadic_level": n * n,
                "log2_negative_moment_term": format(
                    alpha * Decimal(n * n) - Decimal(n), "f"
                ),
            }
        )
    return rows


def expected_transport_rows() -> list[dict[str, Any]]:
    return [
        {
            "block_p": p,
            "critical_polynomial_cost": "w_Z^(-p)/(p+1)^2",
            "weighted_term": f"1/{(p + 1) ** 2}",
        }
        for p in (0, 1, 2, 8, 32)
    ]


def expected_strict() -> dict[str, Any]:
    return {
        "optimal_clock_negative_moment_equivalence": "CERTIFIED",
        "critical_Dini_clearance_frontier": "CERTIFIED",
        "summable_pullback_Minkowski_route": "CERTIFIED_CONDITIONAL",
        "fixed_insertion_rank_tail_implies_weak_clearance": "FALSE_BY_CERTIFIED_SEPARATOR",
        "hybrid_long_short_suffix_ledger": "CERTIFIED_CONDITIONAL",
        "truncated_optimal_transport_BL_bound": "CERTIFIED",
        "OT_cost_never_worse_than_Round55_best": "CERTIFIED",
        "critical_polynomial_weighted_BL_route": "CERTIFIED_CONDITIONAL",
        "physical_same_law_negative_clearance_moment": "NOT_CERTIFIED",
        "physical_owner_density_or_Minkowski_constants": "NOT_CERTIFIED",
        "physical_pullback_gap_summability": "NOT_CERTIFIED",
        "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
        "physical_unbounded_or_hybrid_suffix_schedule": "NOT_CERTIFIED",
        "physical_same_source_or_OT_decay": "NOT_CERTIFIED",
        "unconditional_trace_resolvent": "NOT_CERTIFIED",
        "unconditional_signed_BL_resolvent": "NOT_CERTIFIED",
        "positive_F10_from_signed_transport": "NOT_CERTIFIED",
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
        if any(
            token not in provenance["parameter_scope"]
            for token in ("fixed-|s|<=1/400", "recordwise", "no moving-map sequence")
        ):
            errors.append("parameter scope")
        if any(
            token not in provenance["claim_type"]
            for token in ("negative-moment", "hybrid-suffix", "truncated-transport")
        ):
            errors.append("claim scope")

        dec = independent_decimals()
        if not Q(4999, 10000) < GAMMA < Q(1, 2):
            errors.append("gamma bracket")
        if not Q(1) < W_Z < Q(2):
            errors.append("weight window")
        alpha_lo = Decimal(12406563164308641) / Decimal(10**19)
        alpha_hi = Decimal(12406563164308642) / Decimal(10**19)
        if not alpha_lo < dec["alpha_opt"] < alpha_hi:
            errors.append("alpha bracket")
        with localcontext() as context:
            context.prec = 120
            alpha_replay = dec["beta"] * dec["weight"].ln() / Decimal(2).ln()
        if dec["alpha_opt"] != alpha_replay:
            errors.append("alpha identity")

        eq = result["exact_clearance_negative_moment_equivalence"]
        if all(token not in eq["same_law_variables"] for token in ("actual owner law", "A_col")):
            errors.append("same-law scope")
        if eq["critical_order"] != "alpha_opt=beta*log(w_Z)/log(2)":
            errors.append("critical order")
        if eq["alpha_opt_decimal_120_digit_audit"] != format(dec["alpha_opt"], "f"):
            errors.append("alpha decimal")
        if eq["clock_moment"] != "M_clock=integral w_Z^r_(k(omega)) dnu=sum_k w_Z^r_k*m_k":
            errors.append("clock moment")
        if eq["negative_clearance_moment"] != "M_neg=integral delta(omega)^(-alpha_opt) dnu":
            errors.append("negative moment")
        if eq["pointwise_two_sided_bound"] != (
            "w_Z^beta*delta^(-alpha_opt)<=w_Z^r_k<"
            "w_Z^(beta+1)*2^alpha_opt*delta^(-alpha_opt)"
        ):
            errors.append("pointwise equivalence")
        if eq["integrated_two_sided_bound"] != (
            "w_Z^beta*M_neg<=M_clock<w_Z^(beta+1)*2^alpha_opt*M_neg"
        ):
            errors.append("integrated equivalence")
        if eq["finiteness_equivalence"] != "M_clock<infinity iff M_neg<infinity":
            errors.append("finiteness equivalence")
        if all(token not in eq["layer_cake_identity"] for token in ("nu(A_col)", "t^(-alpha_opt-1)")):
            errors.append("layer cake")
        if "eta>alpha_opt" not in eq["power_tail_sufficient_condition"]:
            errors.append("power tail")
        if "(log(e/t))^(1+epsilon)" not in eq["critical_Dini_sufficient_condition"]:
            errors.append("Dini condition")
        if "infinite" not in eq["critical_log_separator"]:
            errors.append("critical separator")
        eq_rows = expected_equivalence_rows()
        if eq["rows"] != eq_rows:
            errors.append("equivalence rows")
        if eq["rows_sha256"] != cert.digest(eq_rows):
            errors.append("equivalence rows digest")
        if eq["physical_same_law_negative_moment"] != "NOT_CERTIFIED":
            errors.append("equivalence frontier")
        if eq["status"] != "CERTIFIED_EXACT_OPTIMAL_CLOCK_NEGATIVE_MOMENT_EQUIVALENCE":
            errors.append("equivalence status")

        # Numerically replay the clock inequalities in logarithmic coordinates.
        log_inv_gamma = -dec["gamma"].ln()
        log_two = Decimal(2).ln()
        for row in eq_rows:
            k = row["dyadic_level_k"]
            r = row["optimal_clock_r_k"]
            target = Decimal(k + 1) * log_two
            if Decimal(r) * log_inv_gamma < target:
                errors.append("clock upper inequality")
                break
            if r > 0 and not Decimal(r - 1) * log_inv_gamma < target:
                errors.append("clock predecessor inequality")
                break

        pull = result["recordwise_pullback_minkowski_dini_route"]
        for token in ("dnu_a/dc<=D_a", "epsilon^eta", "delta_a>=g_a", "dist(c,E_a)^q"):
            if token not in pull["recordwise_hypotheses"]:
                errors.append("pullback hypotheses")
                break
        if pull["recordwise_tail"] != (
            "nu_a{delta_a<t}<=D_a*A_a*g_a^(-eta/q)*t^(eta/q)"
        ):
            errors.append("pullback tail")
        if "sum_a" not in pull["aggregate_constant"] or "uniform boundedness" not in pull["aggregate_constant"]:
            errors.append("aggregate constant")
        if pull["sharp_exponent_condition"] != "eta/q>alpha_opt":
            errors.append("pullback exponent")
        if "C_pull<infinity" not in pull["aggregate_conclusion"]:
            errors.append("pullback conclusion")
        if "eta=2/3" not in pull["inverse_square_specialisation"]:
            errors.append("inverse-square specialization")
        if pull["inverse_square_pullback_power_limit_decimal"] != format(
            dec["inverse_square_pullback_power_limit"], "f"
        ):
            errors.append("pullback power limit")
        for key in (
            "physical_owner_density_bound",
            "physical_full_word_Minkowski_constants",
            "physical_pullback_gap_summability",
        ):
            if pull[key] != "NOT_CERTIFIED":
                errors.append(f"pullback frontier {key}")
        if pull["status"] != "CERTIFIED_CONDITIONAL_SUMMABLE_PULLBACK_MINKOWSKI_ROUTE":
            errors.append("pullback status")

        sep = result["rank_tail_optimal_clock_nonimplication_separator"]
        for token in ("p_n=2^(-n)", "B_n=14", "d_n=2^(-n^2)"):
            if token not in sep["law"]:
                errors.append("separator law")
                break
        if sep["total_mass"] != "sum_n p_n=1":
            errors.append("separator mass")
        if sep["A_col_mass"] != "nu(A_col)=1 and nu{d_other=0}=0":
            errors.append("separator A_col")
        if "exactly one other boundary" not in sep["boundary_complexity"]:
            errors.append("separator complexity")
        if sep["parent_debts"] != "Z_parent=1 and Z_parent,B=2^14=16384":
            errors.append("separator parent debt")
        if "nu{B>b}=0" not in sep["fixed_insertion_rank_tail"]:
            errors.append("separator rank tail")
        if "every finite q" not in sep["all_positive_rank_moments"]:
            errors.append("separator moments")
        if "infinity" not in sep["raw_collar_debt"] or "terms tend to infinity" not in sep["negative_moment"]:
            errors.append("separator divergence")
        if "two-sided equivalence" not in sep["optimal_clock_moment"]:
            errors.append("separator clock")
        sep_rows = expected_separator_rows()
        if sep["rows"] != sep_rows:
            errors.append("separator rows")
        if sep["rows_sha256"] != cert.digest(sep_rows):
            errors.append("separator rows digest")
        if not Decimal(sep_rows[5]["log2_negative_moment_term"]) > 0:
            errors.append("separator sign switch")
        if not Decimal(sep_rows[-1]["log2_negative_moment_term"]) > Decimal(1000):
            errors.append("separator term divergence")
        if sep["status"] != "CERTIFIED_RANK_TAIL_DOES_NOT_IMPLY_OPTIMAL_CLEARANCE_MOMENT":
            errors.append("separator status")

        hybrid = result["hybrid_suffix_horizon_criterion"]
        if all(token not in hybrid["joint_split"] for token in ("H>=r_k", "H<r_k")):
            errors.append("hybrid split")
        if "C_rec*w_Z^r_k*m_k^long" not in hybrid["long_part"]:
            errors.append("hybrid long")
        if "2^(k+1)*m_k^short" not in hybrid["short_part"]:
            errors.append("hybrid short")
        if hybrid["mixed_ledger"] != (
            "Q_hybrid<=C_rec*sum_k w_Z^r_k*m_k^long+"
            "sum_k 2^(k+1)*m_k^short"
        ):
            errors.append("hybrid ledger")
        if "both displayed sums finite" not in hybrid["abstract_sufficient_condition"]:
            errors.append("hybrid criterion")
        for key in (
            "physical_same_operator_long_join",
            "physical_short_horizon_direct_debt",
            "physical_hybrid_suffix_schedule",
        ):
            if hybrid[key] != "NOT_CERTIFIED":
                errors.append(f"hybrid frontier {key}")
        if hybrid["status"] != "CERTIFIED_CONDITIONAL_LONG_SHORT_HYBRID_SUFFIX_LEDGER":
            errors.append("hybrid status")

        ot = result["recordwise_truncated_transport_BL_frontier"]
        for token in ("immutable physical record/rank", "equal-mass", "metric target"):
            if token not in ot["scope"]:
                errors.append("OT scope")
                break
        if ot["truncated_cost"] != "c(y+,y-)=min(2,d(y+,y-))":
            errors.append("OT cost")
        if "inf_{pi in Couplings" not in ot["optimal_transport_scalar"]:
            errors.append("OT definition")
        if "no continuously indexed measurable" not in ot["no_selection_claim"]:
            errors.append("OT selection boundary")
        if ot["BL_bound"] != "norm(J_p)_(BL*)<=d_p^OT":
            errors.append("OT BL bound")
        if ot["dominance"] != "d_p^OT<=min(d_p^sync,d_p^product)=d_p^best":
            errors.append("OT dominance")
        if "d_OT=0<d_best=1/2<d_sync=1" not in ot["strict_flip_example"]:
            errors.append("OT strict example")
        if "sum_p w_Z^p*d_p^OT<infinity" not in ot["exact_weighted_interface"]:
            errors.append("OT weighted interface")
        if "m_p*epsilon_p+2*b_p" not in ot["good_bad_source_bound"]:
            errors.append("OT good/bad")
        if ot["critical_polynomial_route"] != (
            "d_p^OT<=w_Z^(-p)/(p+1)^2 gives weighted sum <=2"
        ):
            errors.append("OT critical polynomial")
        if "delta<1/w_Z" not in ot["strictly_weaker_than_geometric_rate"]:
            errors.append("OT nongeometric strictness")
        ot_rows = expected_transport_rows()
        if ot["critical_rows"] != ot_rows:
            errors.append("OT rows")
        if ot["critical_rows_sha256"] != cert.digest(ot_rows):
            errors.append("OT rows digest")
        if ot["physical_OT_or_good_bad_decay"] != "NOT_CERTIFIED":
            errors.append("OT physical frontier")
        if ot["positive_F10_or_cemetery_consequence"] != "NOT_CERTIFIED":
            errors.append("OT positivity frontier")
        if ot["status"] != "CERTIFIED_TRUNCATED_OT_DOMINANCE_AND_WEIGHTED_SUMMABILITY_ROUTE":
            errors.append("OT status")
        # Integral comparison: sum_{p>=0} 1/(p+1)^2 <= 1+int_1^inf x^-2 dx=2.
        if sum(Q(1, (p + 1) ** 2) for p in range(10000)) >= Q(2):
            errors.append("critical polynomial sum")

        tech = result["latest_technology_audit"]
        if tech["official_query_date"] != "2026-07-20" or tech["official_source"] != "export.arxiv.org API":
            errors.append("technology query provenance")
        if tech["relevant_versions"] != [
            "2606.10155v1",
            "2604.19671v2",
            "2503.09536v2",
            "2607.11467v1",
        ]:
            errors.append("technology versions")
        if tech["direct_owner_clearance_or_same_source_theorem_found"] is not False:
            errors.append("technology result")
        if tech["external_source_used_as_dependency"] is not False:
            errors.append("technology dependency boundary")
        if tech["status"] != "CHECKED_NO_DIRECT_PHYSICAL_GATE5_IMPORT":
            errors.append("technology status")

        maturity = result["Gate5_maturity_update"]
        if maturity["previous_global_maturity"] != "10/18" or maturity["current_global_maturity"] != "10/18":
            errors.append("maturity")
        if maturity["new_global_field_completed"] is not None:
            errors.append("field promotion")
        if maturity["complete_18_field_operator_block_count"] != 0:
            errors.append("block count")
        if len(maturity["newly_certified_sublayers"]) != 6:
            errors.append("sublayer count")
        for token in ("physical same-law", "same-operator", "signed cancellation cannot pay positive mass"):
            if token not in maturity["reason_no_new_field_credit"]:
                errors.append("maturity reason")
                break

        strict = result["strict_nonpromotion"]
        if strict != expected_strict():
            errors.append("strict frontier")

        replay_copy = copy.deepcopy(result)
        claimed = replay_copy.pop("internal_replay_digest")
        if claimed != cert.digest(replay_copy):
            errors.append("internal replay digest")
    except (KeyError, TypeError, ValueError, ArithmeticError) as exc:
        errors.append(f"malformed result: {exc}")
    return errors


def integrity_errors(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if manifest["schema"] != cert.MANIFEST_SCHEMA:
            errors.append("manifest schema")
        if manifest["certificate_sha256"] != sha(Path(cert.__file__).resolve()):
            errors.append("certificate hash")
        if manifest["verifier_sha256"] != sha(Path(__file__).resolve()):
            errors.append("verifier hash")
        if manifest["dependencies"] != cert.DEPENDENCIES:
            errors.append("manifest dependencies")
        for name, expected in cert.DEPENDENCIES.items():
            path = HERE / name
            if not is_safe_local_regular_file(path) or sha(path) != expected:
                errors.append(f"dependency integrity {name}")
        if manifest["verdict"] != manifest["result"]["strict_nonpromotion"]:
            errors.append("verdict mismatch")
        errors.extend(direct_errors(manifest["result"]))
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"malformed manifest: {exc}")
    return errors


def replay_errors(manifest: dict[str, Any]) -> list[str]:
    errors = integrity_errors(manifest)
    try:
        rebuilt = cert.build_result()
        if manifest["result"] != rebuilt:
            errors.append("deterministic result replay")
        if manifest["dependencies"] != cert.DEPENDENCIES:
            errors.append("dependency replay")
    except Exception as exc:  # fail closed on any dependency/replay error
        errors.append(f"replay exception: {exc}")
    return errors


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    node: Any = value
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = replacement


def redigest(result: dict[str, Any]) -> None:
    core = copy.deepcopy(result)
    core.pop("internal_replay_digest", None)
    result["internal_replay_digest"] = cert.digest(core)


def semantic_mutations() -> list[tuple[tuple[str, ...], Any]]:
    return [
        (("schema",), "mutated"),
        (("provenance", "dependency_sha256"), {}),
        (("provenance", "old_artifacts_modified"), True),
        (("provenance", "parameter_scope"), "global"),
        (("provenance", "claim_type"), "promotion"),
        (("exact_clearance_negative_moment_equivalence", "same_law_variables"), "another law"),
        (("exact_clearance_negative_moment_equivalence", "critical_order"), "alpha=1"),
        (("exact_clearance_negative_moment_equivalence", "alpha_opt_decimal_120_digit_audit"), "0.1"),
        (("exact_clearance_negative_moment_equivalence", "clock_moment"), "0"),
        (("exact_clearance_negative_moment_equivalence", "negative_clearance_moment"), "0"),
        (("exact_clearance_negative_moment_equivalence", "pointwise_two_sided_bound"), "false"),
        (("exact_clearance_negative_moment_equivalence", "integrated_two_sided_bound"), "false"),
        (("exact_clearance_negative_moment_equivalence", "finiteness_equivalence"), "one way"),
        (("exact_clearance_negative_moment_equivalence", "layer_cake_identity"), "missing"),
        (("exact_clearance_negative_moment_equivalence", "power_tail_sufficient_condition"), "eta=0"),
        (("exact_clearance_negative_moment_equivalence", "critical_Dini_sufficient_condition"), "no log"),
        (("exact_clearance_negative_moment_equivalence", "critical_log_separator"), "finite"),
        (("exact_clearance_negative_moment_equivalence", "rows"), []),
        (("exact_clearance_negative_moment_equivalence", "rows_sha256"), "0" * 64),
        (("exact_clearance_negative_moment_equivalence", "physical_same_law_negative_moment"), "CERTIFIED"),
        (("exact_clearance_negative_moment_equivalence", "status"), "PROMOTED"),
        (("recordwise_pullback_minkowski_dini_route", "recordwise_hypotheses"), "none"),
        (("recordwise_pullback_minkowski_dini_route", "recordwise_tail"), "constant"),
        (("recordwise_pullback_minkowski_dini_route", "aggregate_constant"), "uniform only"),
        (("recordwise_pullback_minkowski_dini_route", "sharp_exponent_condition"), "eta/q>=0"),
        (("recordwise_pullback_minkowski_dini_route", "aggregate_conclusion"), "automatic"),
        (("recordwise_pullback_minkowski_dini_route", "inverse_square_specialisation"), "eta=1"),
        (("recordwise_pullback_minkowski_dini_route", "inverse_square_pullback_power_limit_decimal"), "1"),
        (("recordwise_pullback_minkowski_dini_route", "physical_owner_density_bound"), "CERTIFIED"),
        (("recordwise_pullback_minkowski_dini_route", "physical_full_word_Minkowski_constants"), "CERTIFIED"),
        (("recordwise_pullback_minkowski_dini_route", "physical_pullback_gap_summability"), "CERTIFIED"),
        (("recordwise_pullback_minkowski_dini_route", "status"), "PROMOTED"),
        (("rank_tail_optimal_clock_nonimplication_separator", "law"), "B grows"),
        (("rank_tail_optimal_clock_nonimplication_separator", "total_mass"), "2"),
        (("rank_tail_optimal_clock_nonimplication_separator", "A_col_mass"), "zero"),
        (("rank_tail_optimal_clock_nonimplication_separator", "boundary_complexity"), "infinite per record"),
        (("rank_tail_optimal_clock_nonimplication_separator", "parent_debts"), "infinite"),
        (("rank_tail_optimal_clock_nonimplication_separator", "fixed_insertion_rank_tail"), "unknown"),
        (("rank_tail_optimal_clock_nonimplication_separator", "all_positive_rank_moments"), "diverge"),
        (("rank_tail_optimal_clock_nonimplication_separator", "raw_collar_debt"), "finite"),
        (("rank_tail_optimal_clock_nonimplication_separator", "negative_moment"), "finite"),
        (("rank_tail_optimal_clock_nonimplication_separator", "optimal_clock_moment"), "finite"),
        (("rank_tail_optimal_clock_nonimplication_separator", "rows"), []),
        (("rank_tail_optimal_clock_nonimplication_separator", "rows_sha256"), "0" * 64),
        (("rank_tail_optimal_clock_nonimplication_separator", "status"), "PROMOTED"),
        (("hybrid_suffix_horizon_criterion", "joint_split"), "no split"),
        (("hybrid_suffix_horizon_criterion", "long_part"), "free"),
        (("hybrid_suffix_horizon_criterion", "short_part"), "mass only"),
        (("hybrid_suffix_horizon_criterion", "mixed_ledger"), "0"),
        (("hybrid_suffix_horizon_criterion", "abstract_sufficient_condition"), "one sum"),
        (("hybrid_suffix_horizon_criterion", "physical_same_operator_long_join"), "CERTIFIED"),
        (("hybrid_suffix_horizon_criterion", "physical_short_horizon_direct_debt"), "CERTIFIED"),
        (("hybrid_suffix_horizon_criterion", "physical_hybrid_suffix_schedule"), "CERTIFIED"),
        (("hybrid_suffix_horizon_criterion", "status"), "PROMOTED"),
        (("recordwise_truncated_transport_BL_frontier", "scope"), "cross record"),
        (("recordwise_truncated_transport_BL_frontier", "truncated_cost"), "d"),
        (("recordwise_truncated_transport_BL_frontier", "optimal_transport_scalar"), "max"),
        (("recordwise_truncated_transport_BL_frontier", "no_selection_claim"), "selected"),
        (("recordwise_truncated_transport_BL_frontier", "BL_bound"), "reverse"),
        (("recordwise_truncated_transport_BL_frontier", "dominance"), "d_sync<=d_product"),
        (("recordwise_truncated_transport_BL_frontier", "strict_flip_example"), "ordered"),
        (("recordwise_truncated_transport_BL_frontier", "exact_weighted_interface"), "unweighted"),
        (("recordwise_truncated_transport_BL_frontier", "good_bad_source_bound"), "signed cancellation"),
        (("recordwise_truncated_transport_BL_frontier", "critical_polynomial_route"), "diverges"),
        (("recordwise_truncated_transport_BL_frontier", "strictly_weaker_than_geometric_rate"), "equivalent"),
        (("recordwise_truncated_transport_BL_frontier", "critical_rows"), []),
        (("recordwise_truncated_transport_BL_frontier", "critical_rows_sha256"), "0" * 64),
        (("recordwise_truncated_transport_BL_frontier", "physical_OT_or_good_bad_decay"), "CERTIFIED"),
        (("recordwise_truncated_transport_BL_frontier", "positive_F10_or_cemetery_consequence"), "CERTIFIED"),
        (("recordwise_truncated_transport_BL_frontier", "status"), "PROMOTED"),
        (("latest_technology_audit", "official_query_date"), "2020-01-01"),
        (("latest_technology_audit", "official_source"), "blog"),
        (("latest_technology_audit", "relevant_versions"), []),
        (("latest_technology_audit", "direct_owner_clearance_or_same_source_theorem_found"), True),
        (("latest_technology_audit", "external_source_used_as_dependency"), True),
        (("latest_technology_audit", "status"), "IMPORTED"),
        (("Gate5_maturity_update", "previous_global_maturity"), "18/18"),
        (("Gate5_maturity_update", "new_global_field_completed"), "F10"),
        (("Gate5_maturity_update", "newly_certified_sublayers"), []),
        (("Gate5_maturity_update", "reason_no_new_field_credit"), "complete"),
        (("Gate5_maturity_update", "current_global_maturity"), "11/18"),
        (("Gate5_maturity_update", "complete_18_field_operator_block_count"), 1),
        (("strict_nonpromotion", "physical_same_law_negative_clearance_moment"), "CERTIFIED"),
        (("strict_nonpromotion", "physical_Round54_to_Round42_same_operator_join"), "CERTIFIED"),
        (("strict_nonpromotion", "positive_F10_from_signed_transport"), "CERTIFIED"),
        (("strict_nonpromotion", "Gate5"), "CERTIFIED"),
        (("strict_nonpromotion", "Gate5_maturity"), "18/18"),
        (("strict_nonpromotion", "complete_18_field_operator_block_count"), 1),
        (("strict_nonpromotion", "complete_composite_gates"), "1/5"),
        (("strict_nonpromotion", "CM2"), "GO"),
    ]


def run_self_test() -> tuple[int, list[str]]:
    base = cert.build_result()
    failures: list[str] = []
    tests = semantic_mutations()
    for index, (path, replacement) in enumerate(tests):
        mutated = copy.deepcopy(base)
        set_path(mutated, path, replacement)
        redigest(mutated)  # hostile mutation forges the replay digest too
        if not direct_errors(mutated):
            failures.append(f"semantic mutation {index}: {'/'.join(path)}")

    # Strict-JSON hostile inputs.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        duplicate = root / "duplicate.json"
        duplicate.write_text('{"x":1,"x":2}\n', encoding="utf-8")
        nonfinite = root / "nonfinite.json"
        nonfinite.write_text('{"x":NaN}\n', encoding="utf-8")
        for label, path in (("duplicate", duplicate), ("nonfinite", nonfinite)):
            try:
                json.loads(
                    path.read_text(encoding="utf-8"),
                    object_pairs_hook=cert.strict_object,
                    parse_constant=cert.reject_json_constant,
                )
                failures.append(f"strict JSON {label}")
            except ValueError:
                pass
    return len(tests) + 2, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=cert.DEFAULT_MANIFEST)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--integrity-only", action="store_true")
    group.add_argument("--replay", action="store_true")
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--reemit", type=Path)
    args = parser.parse_args()

    if args.self_test:
        total, failures = run_self_test()
        if failures:
            print("HOSTILE_MUTATIONS: FAIL")
            for failure in failures:
                print(failure)
            return 1
        print(f"HOSTILE_MUTATIONS: {total}/{total} rejected")
        return 0

    if args.reemit:
        try:
            args.reemit.write_bytes(cert.render_manifest(Path(__file__).resolve()))
        except Exception as exc:
            print(f"REEMIT: FAIL: {exc}")
            return 1
        print(f"REEMIT: wrote {args.reemit}")
        return 0

    try:
        manifest = strict_load(args.manifest)
    except Exception as exc:
        print(f"LOAD: FAIL: {exc}")
        return 1

    errors = replay_errors(manifest) if args.replay else integrity_errors(manifest)
    if errors:
        print("VERIFY: FAIL")
        for error in errors:
            print(error)
        return 1

    if args.integrity_only:
        print("INTEGRITY: PASS")
        return 0
    if args.replay:
        print("REPLAY: PASS")
        return 0

    strict = manifest["verdict"]
    print("VERIFY: PASS")
    print("NEGATIVE_MOMENT_EQUIVALENCE:", strict["optimal_clock_negative_moment_equivalence"])
    print("OT_DOMINANCE:", strict["OT_cost_never_worse_than_Round55_best"])
    print("PHYSICAL_WEAK_CLEARANCE:", strict["physical_same_law_negative_clearance_moment"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
