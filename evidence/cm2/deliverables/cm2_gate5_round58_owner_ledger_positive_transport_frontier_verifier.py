#!/usr/bin/env python3
"""Fail-closed verifier for the Round-58 Gate-5 owner-ledger leaf."""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import json
import tempfile
from decimal import Decimal, ROUND_CEILING, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate5_round58_owner_ledger_positive_transport_frontier_cert as cert


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


@functools.lru_cache(maxsize=1)
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
        }


def independent_clock(k: int, beta: Decimal) -> int:
    return int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))


def expected_audit_rows() -> list[dict[str, Any]]:
    return [
        {"leaf": "Round49", "available": "typed fixed-record measures and suffix-product nonimplication", "missing_for_owner_clock": "joint insertion/suffix law"},
        {"leaf": "Round50", "available": "global standard-Borel owner-deduplicated root registry", "missing_for_owner_clock": "finite all-depth owner aggregate"},
        {"leaf": "Round51", "available": "registry of all finite regular suffix branches", "missing_for_owner_clock": "a selected compatible horizon and physical operator embedding"},
        {"leaf": "Round52", "available": "constant-one fixed-insertion source-rank B tail", "missing_for_owner_clock": "all-time sum and any comparison B versus clearance K"},
        {"leaf": "Round53", "available": "owner root atom over the outer parent law", "missing_for_owner_clock": "collar-coordinate absolute continuity/density"},
        {"leaf": "Round54", "available": "Borel A_col, clearance d, level K, collar ell and labelled E/Tr", "missing_for_owner_clock": "A_col coverage and aggregate collar debt"},
        {"leaf": "Round55", "available": "conditional delayed recovery and exact required tags", "missing_for_owner_clock": "physical same-operator join and compatible horizon"},
        {"leaf": "Round56", "available": "pointwise minimal exact-gamma clock r_K", "missing_for_owner_clock": "same-law clock moment and post-recovery join"},
        {"leaf": "Round57", "available": "negative-moment equivalence and conditional hybrid ledger", "missing_for_owner_clock": "finite physical moment, H/J joint law and positive lift"},
        {"leaf": "Round42", "available": "numerical positive killed C24 operator recurrence O_s^9148", "missing_for_owner_clock": "Gate5 owner/event/side/word-cell domain equality"},
    ]


def expected_tail_rows() -> list[dict[str, Any]]:
    beta = independent_decimals()["beta"]
    rows: list[dict[str, Any]] = []
    for k in (0, 1, 2, 16, 4381, 10000):
        r = independent_clock(k, beta)
        r_next = independent_clock(k + 1, beta)
        rows.append(
            {
                "level_K": k,
                "clock_r_K": r,
                "weight_a_K": f"w_Z^{r}",
                "tail_increment": f"w_Z^{r_next}-w_Z^{r}",
            }
        )
    return rows


def expected_completion_rows() -> list[dict[str, Any]]:
    beta = independent_decimals()["beta"]
    return [
        {
            "n": n,
            "mass": f"2^-{n + 1}",
            "K": 2 * n,
            "r_K": independent_clock(2 * n, beta),
            "aligned_H": independent_clock(2 * n, beta),
            "short_H": 0,
            "raw_term": f"2^{n}",
        }
        for n in (0, 1, 2, 4, 8, 16)
    ]


def expected_positive_rows() -> list[dict[str, Any]]:
    alpha = independent_decimals()["alpha_opt"]
    rows: list[dict[str, Any]] = []
    for n in (1, 100, 806, 807, 1000, 2000):
        rows.append(
            {
                "record_n": n,
                "Jordan_mass_each_sign": "2^(-n)",
                "clearance": "2^(-n^2)",
                "d_OT": "0",
                "log2_one_sign_positive_term": format(alpha * Decimal(n * n) - Decimal(n), "f"),
            }
        )
    return rows


def expected_strict() -> dict[str, Any]:
    return {
        "physical_same_law_extended_clearance_ledger": "CERTIFIED_BOREL_EXTENDED_VALUED",
        "physical_same_law_clearance_ledger_finite": "NOT_CERTIFIED",
        "physical_A_col_full_coverage": "NOT_CERTIFIED",
        "physical_D_A_g_kernel_ledger_finite": "NOT_CERTIFIED",
        "physical_clearance_horizon_joint_law": "NOT_CERTIFIED",
        "physical_Round54_to_Round42_same_operator_join": "NOT_CERTIFIED",
        "physical_short_horizon_debt": "NOT_CERTIFIED",
        "physical_hybrid_suffix_schedule": "NOT_CERTIFIED",
        "clearance_marginal_implies_hybrid_suffix": "FALSE_BY_CERTIFIED_SEPARATOR",
        "signed_OT_implies_positive_F10": "FALSE_BY_CERTIFIED_SEPARATOR",
        "signed_OT_implies_strong_cemetery": "FALSE_BY_CERTIFIED_SEPARATOR",
        "unconditional_trace_resolvent": "NOT_CERTIFIED",
        "unconditional_signed_BL_resolvent": "NOT_CERTIFIED",
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
        if any(token not in provenance["parameter_scope"] for token in ("fixed-|s|<=1/400", "recordwise", "s=0")):
            errors.append("parameter scope")
        if any(token not in provenance["claim_type"] for token in ("same-owner", "K/H/J", "positive-transport")):
            errors.append("claim scope")

        dec = independent_decimals()
        if not Q(4999, 10000) < GAMMA < Q(1, 2):
            errors.append("gamma bracket")
        if not Q(1) < W_Z < Q(4, 3):
            errors.append("weight bracket")
        if not Decimal("0.0012406563164308641") < dec["alpha_opt"] < Decimal("0.0012406563164308642"):
            errors.append("alpha bracket")

        audit = result["frozen_chain_field_audit"]
        audit_rows = expected_audit_rows()
        if audit["rows"] != audit_rows:
            errors.append("audit rows")
        if audit["rows_sha256"] != cert.digest(audit_rows):
            errors.append("audit rows digest")
        if "Round49--57" not in audit["scope"] or "Round42" not in audit["scope"]:
            errors.append("audit scope")
        if any(token not in audit["positive_findings"] for token in ("owner/root registry", "clearance d", "minimal clock")):
            errors.append("audit positive findings")
        if any(token not in audit["negative_findings"] for token in ("finite same-law", "horizon H", "Boolean J")):
            errors.append("audit negative findings")
        if "independent" not in audit["rank_scope_guard"] or "K" not in audit["rank_scope_guard"]:
            errors.append("audit rank guard")
        if audit["status"] != "CERTIFIED_COMPLETE_FROZEN_CHAIN_FIELD_AUDIT":
            errors.append("audit status")

        ledger = result["physical_same_owner_extended_clearance_ledger"]
        if any(token not in ledger["physical_base"] for token in ("standard-Borel", "actual finite", "A_col")):
            errors.append("ledger physical base")
        if any(token not in ledger["Borel_marks"] for token in ("delta(a)", "K(a)", "ell(a)", "r(a)")):
            errors.append("ledger marks")
        if ledger["level_law"] != "m_k=nu({a in A_col:K(a)=k})":
            errors.append("ledger level law")
        if ledger["extended_clock_ledger"] != "M_clock=sum_(k>=0) w_Z^r_k*m_k in [0,infinity]":
            errors.append("extended ledger")
        if ledger["tail_function"] != "F_j=nu({a in A_col:K(a)>j})":
            errors.append("tail function")
        if ledger["exact_Abel_identity"] != (
            "M_clock=w_Z^r_0*nu(A_col)+sum_(j>=0)"
            "(w_Z^r_(j+1)-w_Z^r_j)*F_j"
        ):
            errors.append("Abel identity")
        if "increases to M_clock" not in ledger["truncation"]:
            errors.append("truncation")
        if "complete positive bridge" not in ledger["coverage_axis"]:
            errors.append("coverage axis")
        if ledger["coverage_not_certified"] != "nu(A_col^c)=0 is NOT_CERTIFIED":
            errors.append("coverage frontier")
        if ledger["finiteness_not_certified"] != "M_clock<infinity is NOT_CERTIFIED":
            errors.append("ledger frontier")
        tail_rows = expected_tail_rows()
        if ledger["rows"] != tail_rows or ledger["rows_sha256"] != cert.digest(tail_rows):
            errors.append("tail rows")
        if ledger["status"] != "CERTIFIED_PHYSICAL_SAME_LAW_EXTENDED_LEDGER_NOT_FINITE":
            errors.append("ledger status")

        # Independent finite-support replay of Abel summation.
        # Abel summation is algebraic.  Replaying it with small exact rational
        # increasing weights avoids repeatedly exponentiating the enormous
        # materialized Round42 rational during hostile testing.
        weights = [Q((k + 1) * (k + 1) + 3, 7) for k in range(12)]
        masses = [Q(k + 1, 1000) for k in range(12)]
        lhs = sum((weights[k] * masses[k] for k in range(12)), Q(0))
        rhs = weights[0] * sum(masses, Q(0))
        for j in range(11):
            rhs += (weights[j + 1] - weights[j]) * sum(masses[j + 1 :], Q(0))
        if lhs != rhs:
            errors.append("Abel arithmetic")

        density = result["root_density_kernelised_pullback_frontier"]
        if "root atom" not in density["root_law_type"] or "not an along-collar density" not in density["root_law_type"]:
            errors.append("root type")
        if "Dirac root" not in density["why_recordwise_Da_is_not_frozen"]:
            errors.append("D_a type")
        if density["artificial_extension_density"].count("ell(a)^(-1)") != 1:
            errors.append("extension density")
        if all(token not in density["extension_aggregate_identity"] for token in ("sum_k 2^(k+1)m_k", "Z_col")):
            errors.append("extension aggregate")
        if "missing raw collar debt" not in density["no_gain_from_constant_density"]:
            errors.append("constant density guard")
        for token in ("nu_b(dc)", "D_b", "A_b", "g_b", "dist(c,E_b)^q"):
            if token not in density["correct_kernel_hypotheses"]:
                errors.append("kernel hypotheses")
                break
        if "integral D_b*A_b*g_b^(-eta/q)" not in density["kernel_tail_bound"]:
            errors.append("kernel tail")
        if any(token not in density["kernel_sufficient_ledger"] for token in ("C_pull", "eta/q>alpha_opt", "M_clock<infinity")):
            errors.append("kernel sufficient ledger")
        if len(density["missing_kernel_fields"]) != 4:
            errors.append("kernel missing fields")
        if density["physical_D_A_g_ledger_finite"] != "NOT_CERTIFIED":
            errors.append("DAG frontier")
        if density["status"] != "CERTIFIED_ROOT_ATOM_DENSITY_TYPE_AUDIT_AND_KERNEL_ROUTE":
            errors.append("density status")

        horizon = result["clearance_horizon_same_operator_frontier"]
        for token in ("H(a)", "J(a)=1", "Round54", "Round42"):
            if token not in horizon["missing_marks"]:
                errors.append("missing horizon marks")
                break
        if horizon["joint_law_if_supplied"] != "Lambda=(K,H,J)_#(nu|A_col) on N x N x {0,1}":
            errors.append("joint law")
        if "recover when" not in horizon["canonical_positive_policy"]:
            errors.append("policy")
        if any(token not in horizon["policy_ledger"] for token in ("J=1,H>=r_K", "C_rec*w_Z^r_K", "2^(K+1)")):
            errors.append("policy ledger")
        if "both finite" not in horizon["exact_policy_criterion"]:
            errors.append("policy criterion")
        if "not a selected" not in horizon["why_Round51_is_not_H"]:
            errors.append("Round51 guard")
        if "no frozen equality" not in horizon["why_Round54_Round42_do_not_compose_yet"]:
            errors.append("operator guard")
        if "disjoint tagged carrier" not in horizon["typed_noncomposition_separator"]:
            errors.append("typed separator")
        sep = horizon["same_marginal_separator"]
        for token in ("K=2n", "m_n=2^(-(n+1))", "B=14", "full A_col"):
            if token not in sep["law"]:
                errors.append("completion separator law")
                break
        if sep["aligned_completion"] != "J=1 and H=r_K on every level":
            errors.append("aligned completion")
        if "w_Z^2/2<1" not in sep["aligned_bound"] or "infinity" not in sep["aligned_bound"]:
            errors.append("aligned bound")
        if sep["short_completion"] != "J=0 and H=0 on every level":
            errors.append("short completion")
        if "sum_n 2^n=infinity" not in sep["short_divergence"]:
            errors.append("short divergence")
        completion_rows = expected_completion_rows()
        if horizon["rows"] != completion_rows or horizon["rows_sha256"] != cert.digest(completion_rows):
            errors.append("completion rows")
        for key in ("physical_H_joint_law", "physical_J_same_operator", "physical_short_debt"):
            if horizon[key] != "NOT_CERTIFIED":
                errors.append(f"horizon frontier {key}")
        if horizon["status"] != "CERTIFIED_MINIMAL_K_H_J_POLICY_AND_TWO_COMPLETION_SEPARATOR":
            errors.append("horizon status")
        # Exact convergence check used by the two-completion separator.
        aligned_ratio = dec["weight"] * dec["weight"] / Decimal(2)
        if not aligned_ratio < 1:
            errors.append("aligned ratio")
        aligned_bound = (dec["weight"] / Decimal(2)) / (Decimal(1) - aligned_ratio)
        if not aligned_bound > 0:
            errors.append("aligned bound sign")

        positive = result["signed_OT_positive_charge_frontier"]
        if any(token not in positive["signed_scope"] for token in ("Jordan", "BL*", "J=mu^+-mu^-")):
            errors.append("signed scope")
        if positive["positive_cost_identity"] != (
            "for every nonnegative Borel charge a, integral[a(y+)+a(y-)]dpi="
            "integral a dmu^+ + integral a dmu^-; it is coupling-independent"
        ):
            errors.append("positive cost identity")
        if "iff" not in positive["necessary_and_sufficient_positive_interface"]:
            errors.append("positive iff")
        if any(token not in positive["conditional_transport_lift"] for token in ("a(y+)", "C*a(y-)", "L*c", "anchor")):
            errors.append("conditional lift")
        for token in ("mu_n^+=mu_n^-", "d_n^OT=0", "B=14", "infinity"):
            if token not in positive["zero_cost_infinite_positive_separator"]:
                errors.append("zero-cost separator")
                break
        if "signed cemetery current is zero" not in positive["strong_cemetery_separator"]:
            errors.append("cemetery separator")
        if positive["all_signed_weighted_resolvents"] != "identically zero in the separator":
            errors.append("signed resolvent")
        if "nu(A_col)=1" not in positive["full_A_col_and_rank_fields"]:
            errors.append("separator frozen fields")
        positive_rows = expected_positive_rows()
        if positive["rows"] != positive_rows or positive["rows_sha256"] != cert.digest(positive_rows):
            errors.append("positive rows")
        if not Decimal(positive_rows[3]["log2_one_sign_positive_term"]) > 0:
            errors.append("positive sign switch")
        if not Decimal(positive_rows[-1]["log2_one_sign_positive_term"]) > Decimal(1000):
            errors.append("positive divergence")
        if positive["positive_F10_from_signed_OT"] != "FALSE_BY_CERTIFIED_SEPARATOR":
            errors.append("positive F10 frontier")
        if positive["strong_cemetery_from_signed_OT"] != "FALSE_BY_CERTIFIED_SEPARATOR":
            errors.append("cemetery frontier")
        if positive["status"] != "CERTIFIED_COUPLING_INVARIANT_POSITIVE_COST_BOUNDARY":
            errors.append("positive status")

        coverage = result["A_col_coverage_moment_independence"]
        if "full A_col coverage" not in coverage["axis_one"] or "infinite moment" not in coverage["axis_one"]:
            errors.append("coverage axis one")
        if "A_col is empty" not in coverage["axis_two"] or "uncovered" not in coverage["axis_two"]:
            errors.append("coverage axis two")
        if "both" not in coverage["joint_requirement"] or "strong positive cemetery" not in coverage["joint_requirement"]:
            errors.append("coverage joint")
        if coverage["status"] != "CERTIFIED_COVERAGE_AND_MOMENT_LOGICAL_INDEPENDENCE":
            errors.append("coverage status")

        tech = result["latest_technology_audit"]
        if tech["official_query_date"] != "2026-07-20" or tech["official_source"] != "export.arxiv.org API":
            errors.append("technology provenance")
        if tech["new_relevant_version"] != "2606.19621v2":
            errors.append("technology version")
        if "inter-sign optimal transport" not in tech["new_relevant_title"]:
            errors.append("technology title")
        if tech["direct_physical_Gate5_import_found"] is not False:
            errors.append("technology result")
        if tech["external_source_used_as_dependency"] is not False:
            errors.append("technology dependency")
        if tech["status"] != "CHECKED_NO_DIRECT_OWNER_LEDGER_OR_POSITIVE_LIFT_IMPORT":
            errors.append("technology status")

        maturity = result["Gate5_maturity_update"]
        if maturity["previous_global_maturity"] != "10/18" or maturity["current_global_maturity"] != "10/18":
            errors.append("maturity")
        if maturity["new_global_field_completed"] is not None:
            errors.append("field promotion")
        if len(maturity["newly_certified_sublayers"]) != 7:
            errors.append("sublayer count")
        if maturity["complete_18_field_operator_block_count"] != 0:
            errors.append("block count")
        for token in ("not finite", "A_col coverage", "H/J", "signed cancellation"):
            if token not in maturity["reason_no_new_field_credit"]:
                errors.append("maturity reason")
                break

        if result["strict_nonpromotion"] != expected_strict():
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
        if manifest["result"] != cert.build_result():
            errors.append("deterministic result replay")
        if manifest["dependencies"] != cert.DEPENDENCIES:
            errors.append("dependency replay")
    except Exception as exc:
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
        (("frozen_chain_field_audit", "scope"), "one leaf"),
        (("frozen_chain_field_audit", "rows"), []),
        (("frozen_chain_field_audit", "rows_sha256"), "0" * 64),
        (("frozen_chain_field_audit", "positive_findings"), "none"),
        (("frozen_chain_field_audit", "negative_findings"), "all closed"),
        (("frozen_chain_field_audit", "rank_scope_guard"), "B=K"),
        (("frozen_chain_field_audit", "status"), "PROMOTED"),
        (("physical_same_owner_extended_clearance_ledger", "physical_base"), "another law"),
        (("physical_same_owner_extended_clearance_ledger", "Borel_marks"), "none"),
        (("physical_same_owner_extended_clearance_ledger", "level_law"), "m=0"),
        (("physical_same_owner_extended_clearance_ledger", "extended_clock_ledger"), "finite"),
        (("physical_same_owner_extended_clearance_ledger", "tail_function"), "F=0"),
        (("physical_same_owner_extended_clearance_ledger", "exact_Abel_identity"), "false"),
        (("physical_same_owner_extended_clearance_ledger", "truncation"), "uniformly bounded"),
        (("physical_same_owner_extended_clearance_ledger", "coverage_axis"), "automatic"),
        (("physical_same_owner_extended_clearance_ledger", "coverage_not_certified"), "CERTIFIED"),
        (("physical_same_owner_extended_clearance_ledger", "finiteness_not_certified"), "CERTIFIED"),
        (("physical_same_owner_extended_clearance_ledger", "rows"), []),
        (("physical_same_owner_extended_clearance_ledger", "rows_sha256"), "0" * 64),
        (("physical_same_owner_extended_clearance_ledger", "status"), "PROMOTED"),
        (("root_density_kernelised_pullback_frontier", "root_law_type"), "Lebesgue density"),
        (("root_density_kernelised_pullback_frontier", "why_recordwise_Da_is_not_frozen"), "D=1"),
        (("root_density_kernelised_pullback_frontier", "artificial_extension_density"), "D=1"),
        (("root_density_kernelised_pullback_frontier", "extension_aggregate_identity"), "zero"),
        (("root_density_kernelised_pullback_frontier", "no_gain_from_constant_density"), "free gain"),
        (("root_density_kernelised_pullback_frontier", "correct_kernel_hypotheses"), "none"),
        (("root_density_kernelised_pullback_frontier", "kernel_tail_bound"), "constant"),
        (("root_density_kernelised_pullback_frontier", "kernel_sufficient_ledger"), "automatic"),
        (("root_density_kernelised_pullback_frontier", "missing_kernel_fields"), []),
        (("root_density_kernelised_pullback_frontier", "physical_D_A_g_ledger_finite"), "CERTIFIED"),
        (("root_density_kernelised_pullback_frontier", "status"), "PROMOTED"),
        (("clearance_horizon_same_operator_frontier", "missing_marks"), "none"),
        (("clearance_horizon_same_operator_frontier", "joint_law_if_supplied"), "K only"),
        (("clearance_horizon_same_operator_frontier", "canonical_positive_policy"), "recover always"),
        (("clearance_horizon_same_operator_frontier", "policy_ledger"), "0"),
        (("clearance_horizon_same_operator_frontier", "exact_policy_criterion"), "one marginal"),
        (("clearance_horizon_same_operator_frontier", "why_Round51_is_not_H"), "is H"),
        (("clearance_horizon_same_operator_frontier", "why_Round54_Round42_do_not_compose_yet"), "equal"),
        (("clearance_horizon_same_operator_frontier", "typed_noncomposition_separator"), "scalar constants compose"),
        (("clearance_horizon_same_operator_frontier", "same_marginal_separator", "law"), "different marginals"),
        (("clearance_horizon_same_operator_frontier", "same_marginal_separator", "aligned_completion"), "short"),
        (("clearance_horizon_same_operator_frontier", "same_marginal_separator", "aligned_bound"), "infinite"),
        (("clearance_horizon_same_operator_frontier", "same_marginal_separator", "short_completion"), "long"),
        (("clearance_horizon_same_operator_frontier", "same_marginal_separator", "short_divergence"), "finite"),
        (("clearance_horizon_same_operator_frontier", "rows"), []),
        (("clearance_horizon_same_operator_frontier", "rows_sha256"), "0" * 64),
        (("clearance_horizon_same_operator_frontier", "physical_H_joint_law"), "CERTIFIED"),
        (("clearance_horizon_same_operator_frontier", "physical_J_same_operator"), "CERTIFIED"),
        (("clearance_horizon_same_operator_frontier", "physical_short_debt"), "CERTIFIED"),
        (("clearance_horizon_same_operator_frontier", "status"), "PROMOTED"),
        (("signed_OT_positive_charge_frontier", "signed_scope"), "positive"),
        (("signed_OT_positive_charge_frontier", "positive_cost_identity"), "depends on coupling"),
        (("signed_OT_positive_charge_frontier", "necessary_and_sufficient_positive_interface"), "OT finite"),
        (("signed_OT_positive_charge_frontier", "conditional_transport_lift"), "no anchor"),
        (("signed_OT_positive_charge_frontier", "zero_cost_infinite_positive_separator"), "positive finite"),
        (("signed_OT_positive_charge_frontier", "strong_cemetery_separator"), "signed nonzero"),
        (("signed_OT_positive_charge_frontier", "all_signed_weighted_resolvents"), "infinite"),
        (("signed_OT_positive_charge_frontier", "full_A_col_and_rank_fields"), "B grows"),
        (("signed_OT_positive_charge_frontier", "rows"), []),
        (("signed_OT_positive_charge_frontier", "rows_sha256"), "0" * 64),
        (("signed_OT_positive_charge_frontier", "positive_F10_from_signed_OT"), "CERTIFIED"),
        (("signed_OT_positive_charge_frontier", "strong_cemetery_from_signed_OT"), "CERTIFIED"),
        (("signed_OT_positive_charge_frontier", "status"), "PROMOTED"),
        (("A_col_coverage_moment_independence", "axis_one"), "finite"),
        (("A_col_coverage_moment_independence", "axis_two"), "covered"),
        (("A_col_coverage_moment_independence", "joint_requirement"), "one axis"),
        (("A_col_coverage_moment_independence", "status"), "PROMOTED"),
        (("latest_technology_audit", "official_query_date"), "2020-01-01"),
        (("latest_technology_audit", "official_source"), "blog"),
        (("latest_technology_audit", "new_relevant_version"), "none"),
        (("latest_technology_audit", "new_relevant_title"), "unrelated"),
        (("latest_technology_audit", "direct_physical_Gate5_import_found"), True),
        (("latest_technology_audit", "external_source_used_as_dependency"), True),
        (("latest_technology_audit", "status"), "IMPORTED"),
        (("Gate5_maturity_update", "previous_global_maturity"), "18/18"),
        (("Gate5_maturity_update", "new_global_field_completed"), "F10"),
        (("Gate5_maturity_update", "newly_certified_sublayers"), []),
        (("Gate5_maturity_update", "reason_no_new_field_credit"), "complete"),
        (("Gate5_maturity_update", "current_global_maturity"), "11/18"),
        (("Gate5_maturity_update", "complete_18_field_operator_block_count"), 1),
        (("strict_nonpromotion", "physical_same_law_clearance_ledger_finite"), "CERTIFIED"),
        (("strict_nonpromotion", "physical_A_col_full_coverage"), "CERTIFIED"),
        (("strict_nonpromotion", "physical_Round54_to_Round42_same_operator_join"), "CERTIFIED"),
        (("strict_nonpromotion", "signed_OT_implies_positive_F10"), "CERTIFIED"),
        (("strict_nonpromotion", "strong_cemetery"), "CERTIFIED"),
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
        redigest(mutated)
        if not direct_errors(mutated):
            failures.append(f"semantic mutation {index}: {'/'.join(path)}")

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
    print("PHYSICAL_LEDGER:", strict["physical_same_law_extended_clearance_ledger"])
    print("PHYSICAL_LEDGER_FINITE:", strict["physical_same_law_clearance_ledger_finite"])
    print("SIGNED_OT_POSITIVE_F10:", strict["signed_OT_implies_positive_F10"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
