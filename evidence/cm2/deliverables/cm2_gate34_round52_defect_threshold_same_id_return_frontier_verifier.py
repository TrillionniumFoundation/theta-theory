#!/usr/bin/env python3
"""Fail-closed verifier for the Round-52 Gate-4 return frontier leaf."""

from __future__ import annotations

import argparse
import copy
import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round52_defect_threshold_same_id_return_frontier_cert as cert


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


def expected_quarter_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for m in (0, 4, 16, 310, 311, 312, 315, 316, 320):
        rows.append(
            {
                "tail_index_m": m,
                "quarter_block_index": m // 4,
                "tail_majorant": f"C_quarter*2^-{m // 4}",
                "positive_defect_tail_event": (
                    "{Dbar>0}={M>310}"
                    if m == 310
                    else (f"{{Dbar>{m - 309}}}={{M>{m}}}" if m >= 311 else "not_used")
                ),
            }
        )
    return rows


def expected_critical_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for k in (0, 1, 2, 4, 8, 16):
        rows.append(
            {
                "k": k,
                "M": 311 + k,
                "Dbar": 2 + k,
                "rational_atom_mass": cert.qstr(Q(1, 7) * Q(6, 7) ** k),
                "required_moment_term_strict_lower": "7/36",
                "tail_at_m_equals_310_plus_k": cert.qstr(Q(6, 7) ** k),
            }
        )
    return rows


def expected_cell_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in (18, 19, 20, 24):
        M = n * n
        Dbar = M - 309
        rows.append(
            {
                "band_n": n,
                "band_mass": f"2^-{n}",
                "cell_count": f"2^{M}",
                "each_cell_length": f"2^-{M}",
                "leaf_density_rho_j": "1",
                "fixed_physical_D1_density_d_D1": "D0 (one fixed finite positive constant)",
                "cell_length_rank_M": M,
                "safe_defect_Dbar": Dbar,
                "band_defect_moment_strict_lower": cert.qstr(
                    Q(1, 2**n) * Q(7, 6) ** Dbar
                ),
                "next_band_lower_term_ratio": cert.qstr(
                    Q(1, 2) * Q(7, 6) ** (2 * n + 1)
                ),
            }
        )
    return rows


def independent_arithmetic(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    lower = Q(7, 6)
    sharp_upper = Q(241, 204)
    upper = Q(13, 11)
    tail_upper = Q(1, 72) / (1 - Q(1, 18))
    if tail_upper != Q(1, 68):
        errors.append("exponential series tail")
    if 1 + Q(1, 6) + tail_upper != sharp_upper:
        errors.append("exponential upper sum")
    if not lower < sharp_upper < upper:
        errors.append("exponential rational bracket")
    if sharp_upper.numerator * upper.denominator + 1 != (
        upper.numerator * sharp_upper.denominator
    ):
        errors.append("upper cross-product gap")
    if not upper**4 < 2:
        errors.append("quarter block contraction")
    if upper**4 / 2 != Q(28561, 29282):
        errors.append("quarter block ratio")

    cp = Q(4 * 10**90 * 360493663, 358863)
    if not Q(2**310) < cp < Q(2**311):
        errors.append("C_p dyadic bracket")
    for M in range(0, 701):
        expected = 0 if M <= 310 else M - 309
        if cert.safe_defect(M) != expected:
            errors.append(f"defect formula {M}")

    grouped = upper**2 + Q(1, 2) * upper**3 * (
        1 + upper + upper**2 + upper**3
    ) / (1 - upper**4 / 2)
    coefficient0 = upper**2 - 1 + (upper - 1) * grouped
    coefficient = coefficient0 / Q(2**77)
    if coefficient0 != Q(23446, 721):
        errors.append("quarter coefficient before scale")
    if coefficient != Q(11723, 54477219746384227185197056):
        errors.append("quarter coefficient")

    threshold = result.get("sharp_defect_moment_tail_threshold", {})
    qrows = expected_quarter_rows()
    if threshold.get("quarter_tail_rows") != qrows:
        errors.append("quarter rows")
    if threshold.get("quarter_tail_rows_sha256") != cert.digest(qrows):
        errors.append("quarter rows digest")
    if threshold.get("quarter_tail_coefficient") != cert.qstr(coefficient):
        errors.append("quarter coefficient field")

    counters = result.get("critical_tail_countermodels", {})
    crows = expected_critical_rows()
    if counters.get("rows") != crows:
        errors.append("critical rows")
    if counters.get("rows_sha256") != cert.digest(crows):
        errors.append("critical rows digest")
    for row in crows:
        k = row["k"]
        mass = Q(1, 7) * Q(6, 7) ** k
        # exp((k+2)/6)>(7/6)^(k+2), so the rational lower product is 7/36.
        if mass * Q(7, 6) ** (k + 2) != Q(7, 36):
            errors.append(f"rational counter term {k}")
        if Q(row["tail_at_m_equals_310_plus_k"]) != Q(6, 7) ** k:
            errors.append(f"rational counter tail {k}")

    outer = result.get("uniform_outer_majorant_terminal_join", {})
    support = Q(87603, 125000000)
    if not support < Q(1, 1000):
        errors.append("outer support mass")
    if not support + Q(1, 1000) < Q(1, 500):
        errors.append("outer terminal hit")
    if Q(outer.get("collision_SRB_support_mass_strict_upper", "0")) != support:
        errors.append("outer support field")
    if Q(outer.get("inner_strict_lower", "0")) != Q(21, 111718750):
        errors.append("inner hit field")
    if Q(outer.get("outer_strict_upper", "0")) != Q(1, 500):
        errors.append("outer hit field")
    if Q(outer.get("per_orientation_terminal_survivor_fraction_strict_lower", "0")) != Q(499, 500):
        errors.append("marginal survivor field")
    if Q(outer.get("same_ID_once_charged_common_terminal_survivor_fraction_strict_lower", "0")) != Q(249, 250):
        errors.append("common survivor field")

    cell = result.get("cell_level_retyping_audit", {})
    rows = expected_cell_rows()
    if cell.get("rows") != rows:
        errors.append("cell rows")
    if cell.get("rows_sha256") != cert.digest(rows):
        errors.append("cell rows digest")
    for row in rows:
        n = row["band_n"]
        M = n * n
        Dbar = M - 309
        if row["safe_defect_Dbar"] != Dbar:
            errors.append(f"cell defect {n}")
        if Q(row["band_defect_moment_strict_lower"]) != Q(1, 2**n) * Q(7, 6) ** Dbar:
            errors.append(f"cell lower term {n}")
        ratio = Q(1, 2) * Q(7, 6) ** (2 * n + 1)
        if Q(row["next_band_lower_term_ratio"]) != ratio or ratio <= 1:
            errors.append(f"cell ratio {n}")

    geometry = result.get("large_common_mass_geometric_nonpromotion", {})
    if Q(geometry.get("each_terminal_hit_fraction", "0")) != Q(1, 1000):
        errors.append("geometry hit mass")
    if Q(geometry.get("both_marginal_survivor_fractions", "0")) != Q(999, 1000):
        errors.append("geometry marginal mass")
    if Q(geometry.get("same_ID_common_mass", "0")) != Q(499, 500):
        errors.append("geometry common mass")
    if not Q(499, 500) > Q(249, 250):
        errors.append("geometry union-bound comparison")
    if not Q(1000, 999) < cp:
        errors.append("geometry ambient proper comparison")

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

        bracket = result.get("exp_one_sixth_rational_bracket", {})
        if bracket.get("status") != (
            "CERTIFIED_EXACT_RATIONAL_BRACKET_FOR_EXP_ONE_SIXTH"
        ):
            errors.append("exponential bracket status")
        if bracket.get("upper_bound") != "exp(1/6)<241/204<13/11":
            errors.append("exponential upper field")
        if bracket.get("quarter_block_ratio") != "28561/29282":
            errors.append("quarter ratio field")

        threshold = result.get("sharp_defect_moment_tail_threshold", {})
        if threshold.get("status") != (
            "CERTIFIED_SHARP_DEFECT_EXPONENTIAL_TAIL_THRESHOLD_AND_RATIONAL_QUARTER_TAIL_BRIDGE"
        ):
            errors.append("threshold status")
        if threshold.get("critical_tail_base") != "b_c=exp(-1/6)":
            errors.append("critical base")
        if threshold.get("critical_dyadic_exponent") != (
            "alpha_c=log_2(exp(1/6))=1/(6*log(2))"
        ):
            errors.append("critical exponent")
        if "T_m<=C*b^m" not in threshold.get("general_exponential_tail_bridge", ""):
            errors.append("general tail bridge")
        if "floor(m/4)" not in threshold.get(
            "strictly_weaker_rational_sufficient_tail", ""
        ):
            errors.append("quarter tail interface")
        if threshold.get("old_round51_sufficient_tail") != "T_m<=C_len*2^-m":
            errors.append("old tail comparison")
        if threshold.get("actual_physical_quarter_tail_available") is not False:
            errors.append("physical tail overclaim")
        if threshold.get("actual_physical_I_D_certified") is not False:
            errors.append("physical I_D overclaim")

        critical = result.get("critical_tail_countermodels", {})
        if critical.get("status") != (
            "CERTIFIED_CRITICAL_AND_RATIONAL_BELOW_THRESHOLD_COUNTERMODELS"
        ):
            errors.append("critical model status")
        if "exactly the critical base" not in critical.get("sharp_symbolic_tail", ""):
            errors.append("critical exact tail")
        if "I_D=infinity" not in critical.get("sharp_symbolic_moment_failure", ""):
            errors.append("critical moment failure")
        if "not a claim" not in critical.get("logical_scope", ""):
            errors.append("critical logical scope")
        if critical.get("actual_billiard_defect_moment_disproved") is not False:
            errors.append("physical defect disproof overclaim")

        outer = result.get("uniform_outer_majorant_terminal_join", {})
        if outer.get("status") != (
            "CERTIFIED_UNIFORM_LARGE_COMMON_TERMINAL_SURVIVOR_AND_AMBIENT_CLOCK_TRANSFER"
        ):
            errors.append("outer join status")
        if outer.get("H_joint_exists_uniformly_for_all_parameters_and_proper_views") is not True:
            errors.append("outer common time")
        if outer.get("numeric_H_joint") is not None:
            errors.append("outer numeric-time overclaim")
        if outer.get("dyadic_shells") != (
            "k_fw=k_rev=0 because h_fw/p,h_rev/p>499/500>1/2"
        ):
            errors.append("outer zero shells")
        if outer.get("old_marginal_shell_obstruction") != (
            "ELIMINATED_FOR_THIS_COMMON_TERMINAL_SCHEDULE"
        ):
            errors.append("outer q obstruction update")
        if outer.get("common_terminal_subkernel_is_Borel_and_positive") is not True:
            errors.append("outer positive common kernel")
        if outer.get("common_terminal_subkernel_is_geometrically_proper") is not False:
            errors.append("outer properness overclaim")
        if "does not assert avoidance" not in outer.get("terminal_not_intermediate", ""):
            errors.append("outer terminal scope")
        if outer.get("physical_collision_time_q_L6over5") != "NOT_CERTIFIED":
            errors.append("ambient envelope promoted to physical q")
        if outer.get("strong_singular_current_cemetery") != "NOT_CERTIFIED":
            errors.append("ambient exhaustion promoted to strong cemetery")
        if "proper same-ID common return" not in outer.get("physical_q_requires", ""):
            errors.append("physical q missing-interface typing")

        cell = result.get("cell_level_retyping_audit", {})
        if cell.get("status") != (
            "CERTIFIED_CELL_REINDEXING_REMOVES_GROUP_MIN_POISONING_BUT_NOT_CELL_MULTIPLICITY_DEFECT"
        ):
            errors.append("cell retyping status")
        if not cell.get("Borel_and_once_charge", "").startswith("CERTIFIED"):
            errors.append("cell once charge")
        if not cell.get("singleton_family_typing", "").startswith("CERTIFIED"):
            errors.append("cell singleton typing")
        if "sum_j rho_j" not in cell.get("missing_counting_density_interface", ""):
            errors.append("cell missing interface")
        if "D0^(6/5)*sum_n 2^-n" not in cell.get(
            "physical_D1_type_moment", ""
        ):
            errors.append("cell D1/source-density type separation")
        if cell.get("physical_defect_moment_disproved") is not False:
            errors.append("cell physical disproof overclaim")
        if cell.get("cell_retyping_closes_I_D") is not False:
            errors.append("cell I_D overclaim")

        geometry = result.get("large_common_mass_geometric_nonpromotion", {})
        if geometry.get("status") != (
            "CERTIFIED_LARGE_COMMON_MASS_BOREL_TWO_VIEW_FIELDS_DO_NOT_IMPLY_PROPER_INTERSECTION"
        ):
            errors.append("geometric status")
        if geometry.get("transported_reverse_survivor") != "Theta^-1(R)=A":
            errors.append("transported reverse predicate")
        if geometry.get("common_boundary_numerator") != (
            "sum_k mass(A_k)/length(A_k)=sum_k 1=infinity"
        ):
            errors.append("common infinite boundary")
        if "positive-length gap" not in geometry.get(
            "positive_gap_forces_distinct_regular_components", ""
        ):
            errors.append("common-component lower-bound reason")
        if geometry.get("common_standard_family_proper") is not False:
            errors.append("common properness")
        if geometry.get("physical_proper_common_return_disproved") is not False:
            errors.append("physical return disproof overclaim")
        if geometry.get("proper_same_ID_fw_rev_return_inferred") is not False:
            errors.append("same-ID return overclaim")

        frontier = result.get("compressed_physical_frontier", {})
        expected_frontier = {
            "two_proper_view_measure_transport": "CERTIFIED_IN_ROUND51",
            "uniform_common_terminal_survivor_mass_gt_249_over_250": "CERTIFIED",
            "same_ID_geometric_return": "POSITIVE_BOREL_SUBKERNEL_CERTIFIED__PROPERNESS_NOT_CERTIFIED",
            "cell_level_once_charge_retyping": "CERTIFIED_BUT_I_D_STILL_NOT_CLOSED",
            "old_linear_short_endpoint_tail_needed": False,
            "sharp_pure_exponential_tail_threshold": "alpha>1/(6*log(2))",
            "rational_quarter_block_tail_would_suffice": True,
            "physical_quarter_block_tail": "NOT_CERTIFIED",
            "physical_defect_moment": "NOT_CERTIFIED",
            "full_total_ambient_max_clock_Lp_envelope": "CONDITIONAL_ON_PHYSICAL_I_D",
            "old_marginal_shell_q_obstruction": "ELIMINATED_BY_x_sigma_gt_499_over_500",
            "parent_charged_postclock_ambient_max_envelope_L6over5": "CERTIFIED_QUALITATIVELY_FINITE",
            "parent_charged_total_ambient_max_envelope_L6over5": "CONDITIONAL_ON_PHYSICAL_I_D",
            "ambient_envelope_Borel_exhaustion_tail": "CONDITIONAL_ON_PHYSICAL_I_D",
            "physical_collision_time_q_L6over5": "NOT_CERTIFIED_REQUIRES_PROPER_COMMON_RETURN_AND_RECOVERY_JOIN",
            "strong_singular_current_cemetery": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "common_intersection_boundary_Z": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if frontier != expected_frontier:
            errors.append("compressed frontier")

        expected_strict = {
            "sharp_defect_tail_threshold": "CERTIFIED",
            "rational_quarter_tail_conditional_bridge": "CERTIFIED",
            "uniform_large_common_terminal_survivor": "CERTIFIED",
            "cell_level_once_charge_retyping": "CERTIFIED",
            "physical_quarter_tail_or_defect_moment": "NOT_CERTIFIED",
            "proper_same_ID_geometric_return": "NOT_CERTIFIED",
            "parent_charged_postclock_ambient_max_envelope_L6over5": "CERTIFIED_QUALITATIVELY_FINITE",
            "parent_charged_total_ambient_max_envelope_L6over5": "CONDITIONAL_NOT_CLOSED",
            "ambient_envelope_Borel_exhaustion_tail": "CONDITIONAL_NOT_CLOSED",
            "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
            "full_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_singular_current_cemetery": "NOT_CERTIFIED",
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
        (("result", "provenance", "parameter_scope"), "uniform joint-s"),
        (("result", "exp_one_sixth_rational_bracket", "status"), "UNPROVED"),
        (("result", "exp_one_sixth_rational_bracket", "upper_bound"), "exp<6/5"),
        (("result", "exp_one_sixth_rational_bracket", "quarter_block_ratio"), "1"),
        (("result", "sharp_defect_moment_tail_threshold", "status"), "NOT_CERTIFIED"),
        (("result", "sharp_defect_moment_tail_threshold", "critical_tail_base"), "1/2"),
        (("result", "sharp_defect_moment_tail_threshold", "critical_dyadic_exponent"), "1"),
        (("result", "sharp_defect_moment_tail_threshold", "general_exponential_tail_bridge"), "all b"),
        (("result", "sharp_defect_moment_tail_threshold", "old_round51_sufficient_tail"), "none"),
        (("result", "sharp_defect_moment_tail_threshold", "strictly_weaker_rational_sufficient_tail"), "2^-m"),
        (("result", "sharp_defect_moment_tail_threshold", "quarter_tail_coefficient"), "1"),
        (("result", "sharp_defect_moment_tail_threshold", "quarter_tail_rows"), []),
        (("result", "sharp_defect_moment_tail_threshold", "quarter_tail_rows_sha256"), "0" * 64),
        (("result", "sharp_defect_moment_tail_threshold", "actual_physical_quarter_tail_available"), True),
        (("result", "sharp_defect_moment_tail_threshold", "actual_physical_I_D_certified"), True),
        (("result", "critical_tail_countermodels", "status"), "NO_OBSTRUCTION"),
        (("result", "critical_tail_countermodels", "sharp_symbolic_tail"), "faster"),
        (("result", "critical_tail_countermodels", "sharp_symbolic_moment_failure"), "finite"),
        (("result", "critical_tail_countermodels", "logical_scope"), "physical billiard theorem"),
        (("result", "critical_tail_countermodels", "actual_billiard_defect_moment_disproved"), True),
        (("result", "critical_tail_countermodels", "rows"), []),
        (("result", "critical_tail_countermodels", "rows_sha256"), "0" * 64),
        (("result", "uniform_outer_majorant_terminal_join", "status"), "NO_OUTER_JOIN"),
        (("result", "uniform_outer_majorant_terminal_join", "collision_SRB_support_mass_strict_upper"), "1"),
        (("result", "uniform_outer_majorant_terminal_join", "inner_strict_lower"), "0"),
        (("result", "uniform_outer_majorant_terminal_join", "outer_strict_upper"), "1/1000"),
        (("result", "uniform_outer_majorant_terminal_join", "per_orientation_terminal_survivor_fraction_strict_lower"), "1/2"),
        (("result", "uniform_outer_majorant_terminal_join", "same_ID_once_charged_common_terminal_survivor_fraction_strict_lower"), "0"),
        (("result", "uniform_outer_majorant_terminal_join", "H_joint_exists_uniformly_for_all_parameters_and_proper_views"), False),
        (("result", "uniform_outer_majorant_terminal_join", "numeric_H_joint"), 1),
        (("result", "uniform_outer_majorant_terminal_join", "dyadic_shells"), "unbounded"),
        (("result", "uniform_outer_majorant_terminal_join", "old_marginal_shell_obstruction"), "ACTIVE"),
        (("result", "uniform_outer_majorant_terminal_join", "common_terminal_subkernel_is_Borel_and_positive"), False),
        (("result", "uniform_outer_majorant_terminal_join", "common_terminal_subkernel_is_geometrically_proper"), True),
        (("result", "uniform_outer_majorant_terminal_join", "terminal_not_intermediate"), "all-time avoidance"),
        (("result", "uniform_outer_majorant_terminal_join", "physical_collision_time_q_L6over5"), "CERTIFIED"),
        (("result", "uniform_outer_majorant_terminal_join", "strong_singular_current_cemetery"), "CERTIFIED"),
        (("result", "uniform_outer_majorant_terminal_join", "physical_q_requires"), "nothing else"),
        (("result", "cell_level_retyping_audit", "status"), "I_D_CLOSED"),
        (("result", "cell_level_retyping_audit", "Borel_and_once_charge"), "FAILED"),
        (("result", "cell_level_retyping_audit", "singleton_family_typing"), "FAILED"),
        (("result", "cell_level_retyping_audit", "missing_counting_density_interface"), "none"),
        (("result", "cell_level_retyping_audit", "physical_defect_moment_disproved"), True),
        (("result", "cell_level_retyping_audit", "cell_retyping_closes_I_D"), True),
        (("result", "cell_level_retyping_audit", "rows"), []),
        (("result", "cell_level_retyping_audit", "rows_sha256"), "0" * 64),
        (("result", "large_common_mass_geometric_nonpromotion", "status"), "RETURN_CERTIFIED"),
        (("result", "large_common_mass_geometric_nonpromotion", "each_terminal_hit_fraction"), "1/2"),
        (("result", "large_common_mass_geometric_nonpromotion", "both_marginal_survivor_fractions"), "1/2"),
        (("result", "large_common_mass_geometric_nonpromotion", "same_ID_common_mass"), "1/2"),
        (("result", "large_common_mass_geometric_nonpromotion", "transported_reverse_survivor"), "R"),
        (("result", "large_common_mass_geometric_nonpromotion", "common_boundary_numerator"), "finite"),
        (("result", "large_common_mass_geometric_nonpromotion", "positive_gap_forces_distinct_regular_components"), "canonical representation only"),
        (("result", "large_common_mass_geometric_nonpromotion", "common_standard_family_proper"), True),
        (("result", "large_common_mass_geometric_nonpromotion", "physical_proper_common_return_disproved"), True),
        (("result", "large_common_mass_geometric_nonpromotion", "proper_same_ID_fw_rev_return_inferred"), True),
        (("result", "compressed_physical_frontier", "old_linear_short_endpoint_tail_needed"), True),
        (("result", "compressed_physical_frontier", "rational_quarter_block_tail_would_suffice"), False),
        (("result", "compressed_physical_frontier", "physical_quarter_block_tail"), "CERTIFIED"),
        (("result", "compressed_physical_frontier", "physical_defect_moment"), "CERTIFIED"),
        (("result", "compressed_physical_frontier", "same_ID_geometric_return"), "CERTIFIED"),
        (("result", "compressed_physical_frontier", "uniform_common_terminal_survivor_mass_gt_249_over_250"), "NOT_CERTIFIED"),
        (("result", "compressed_physical_frontier", "cell_level_once_charge_retyping"), "FAILED"),
        (("result", "compressed_physical_frontier", "old_marginal_shell_q_obstruction"), "ACTIVE"),
        (("result", "compressed_physical_frontier", "parent_charged_postclock_ambient_max_envelope_L6over5"), "NOT_CERTIFIED"),
        (("result", "compressed_physical_frontier", "parent_charged_total_ambient_max_envelope_L6over5"), "CERTIFIED"),
        (("result", "compressed_physical_frontier", "ambient_envelope_Borel_exhaustion_tail"), "CERTIFIED_UNCONDITIONALLY"),
        (("result", "compressed_physical_frontier", "physical_collision_time_q_L6over5"), "CERTIFIED"),
        (("result", "compressed_physical_frontier", "strong_singular_current_cemetery"), "CERTIFIED"),
        (("result", "compressed_physical_frontier", "numeric_collision_time_q"), "CERTIFIED"),
        (("result", "compressed_physical_frontier", "common_intersection_boundary_Z"), "CERTIFIED"),
        (("result", "compressed_physical_frontier", "Gate4"), "CERTIFIED"),
        (("result", "compressed_physical_frontier", "CM2"), "GO"),
        (("result", "strict_nonpromotion", "sharp_defect_tail_threshold"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "uniform_large_common_terminal_survivor"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "cell_level_once_charge_retyping"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "physical_quarter_tail_or_defect_moment"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "proper_same_ID_geometric_return"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "parent_charged_postclock_ambient_max_envelope_L6over5"), "NOT_CERTIFIED"),
        (("result", "strict_nonpromotion", "parent_charged_total_ambient_max_envelope_L6over5"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "ambient_envelope_Borel_exhaustion_tail"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "physical_collision_time_q_L6over5"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "full_numeric_C_fw_C_rev"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "numeric_collision_time_q"), "CERTIFIED"),
        (("result", "strict_nonpromotion", "strong_singular_current_cemetery"), "CERTIFIED"),
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
    mutation["result"]["sharp_defect_moment_tail_threshold"][
        "actual_physical_I_D_certified"
    ] = float("nan")
    mutations.append(json.dumps(mutation))
    duplicate = path.read_text(encoding="utf-8").rstrip()
    mutations.append(duplicate[:-1] + ',"schema":"duplicate"}')

    rejected = 0
    for body in mutations:
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=".cm2-r52-defect-return-hostile-",
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
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
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
