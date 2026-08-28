#!/usr/bin/env python3
"""Round-57 exact-slope-four common-refinement frontier.

Round 56 certifies the physical first-return endpoint numerator ``J_pair``
and the complete ambient preproperisation clock.  Those facts alone do not
pay the crossed boundary multiplicity of the transported common terminal
survivor.  This leaf supplies the missing physical structure: a tagged
palindromic stopped-cut replay pulls each terminal predicate back to the same
exact slope-four source without inverse-expansion loss.  Two hereditary
paired first-return replays then give finite boundary Z in both proper views,
closing physical ``J_cap`` and the single ``D_cap`` properisation clock.

The leaf also proves the exact component-count equivalence and retains a
field-level separator explaining why generic Borel transport was
insufficient.  It does not promote a proper physical first return,
intermediate C24 avoidance, later clocks, physical q, the strong cemetery,
Gate 4, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round57-exact-slope4-cross-endpoint-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json"
)
DEFAULT_VERIFIER = (
    HERE / "cm2_gate34_round57_exact_slope4_cross_endpoint_frontier_verifier.py"
)

DEPENDENCIES = {
    "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json": (
        "a98203ebf820d959f9e04c213cd1d79c3809744671fd509c40e531bdc552c119"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json": (
        "79eeff7d5c18ec7d28a30c61ae857a733b3136202917c54f6aeaf93d7f414089"
    ),
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json": (
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json": (
        "028c5a8f59a6efffa9df93cfba841f3844d244988dc235038183eef222d21abc"
    ),
    "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json": (
        "7ddecb544fa5a2b243882eaf2028159c22f8437fc3fbb49fda4eb487ab181798"
    ),
    "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json": (
        "2c6ab1c0b3b89000e6d96d04a60d7c662855ae1f24c1d9f43405df04732d7e58"
    ),
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json": (
        "7c9d089219ef00234b7e7bdafaea706bd4c91a46990d6f14d0837ea360406414"
    ),
    "cm2-gate34-round56-preproperisation-full-clock-downstream-manifest-2026-07-20.json": (
        "d7d7b78bda056ddf50c57fd10336592d4484f6c09afc5698d4bbd6c6aec7711c"
    ),
}

PINNED_REPORTS = {
    "cm2-gate34-round42-numeric-c24-growth-block-assault-2026-07-19.md": (
        "c81dfbf71e591a34e282cd03f595da947a6db38e4b4c2b2fb503a751c0ef5823"
    ),
}

DENSITY_RATIO = Q(2000, 1999)
CLOSED_A = Q(360134800, 360493663)
C_P = Q(4 * 10**90 * 360493663, 358863)
CUT_Z1 = Q(18367592526, 360493663)
PAL_MASS_COEFF = (CUT_Z1 + 1) * C_P / 2
FRACTION_F = Q(999, 1000)
FRACTION_COMMON = Q(499, 500)
FRACTION_GAP = Q(1, 1000)
CP_LOWER = Q(19, 20)
REVIEW_PDF_SHA256 = "3330b5467c5c7107e58ba7966a0386f2ab51415990399b387ad2f7e571f61798"


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(key)
        value[key] = item
    return value


def strict_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"dependency path: {name}")
        require(path.resolve().parent == HERE, f"dependency scope: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        value = strict_json(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency root: {name}")
        loaded[name] = value

    for name, expected in PINNED_REPORTS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"report path: {name}")
        require(path.resolve().parent == HERE, f"report scope: {name}")
        require(sha256_path(path) == expected, f"report hash: {name}")
        report = path.read_text(encoding="utf-8")
        require("Thus every unnormalised C24-killed canonical family satisfies" in report, "Round42 arbitrary canonical scope")
        require("Z(O_s G)<=Z1 Z(G)." in report, "Round42 arbitrary one-step bound")

    r41 = loaded[
        "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json"
    ]["result"]
    hereditary = r41["unnormalized_killed_subfamily_Growth"]
    require(hereditary["conditional_survival_normalization_used"] is False, "Round41 unnormalised")
    require(hereditary["positive_subfamily_monotonicity"].startswith("for unnormalized weights"), "Round41 subfamilies")
    require(r41["aggregate_canonical_Z_resolvent"]["physical_aggregate_Z_weighted_tail"] == "CERTIFIED_QUALITATIVE_FOR_CONTROLLED_FINITE_Z_INITIAL_FAMILIES", "Round41 resolvent")

    r42 = loaded[
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    ]["result"]
    numerical = r42["numerical_C24_killed_Growth"]
    require(numerical["hereditary_under_positive_C24_killing"] is True, "Round42 hereditary")
    require(numerical["one_step_Z_multiplier_Z1"] == "18367592526/360493663", "Round42 cut multiplier")

    r47 = loaded[
        "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json"
    ]["result"]
    postcut = r47["one_step_postcut_Z_envelope"]
    require(postcut["killed_output"].startswith("H=O_s G"), "Round47 terminal cut")
    require(postcut["Z1"] == "18367592526/360493663", "Round47 Z1")

    r50 = loaded[
        "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
    ]["result"]
    closed = r50["recordwise_properization_and_common_parent_law"]
    require(closed["closed_recurrence"] == "Z(T^r G)/mass(G)<=a^r*Z(G)/mass(G)+C_p/2", "Round50 closed recurrence")
    require(closed["common_preproperization_clock"] == "R0(y)=696*Dbar(M(y))", "Round50 stopped clock")
    require(closed["Borel_stopped_kernel_reason"].startswith("Dbar is integer-valued Borel"), "Round50 stopped Borel")

    r35 = loaded[
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    ]["result"]
    leaf = r35["collision_SRB_leaf_disintegration"]
    pair = r35["common_forward_reverse_carrier_pair"]
    require(leaf["conditional_density_wrt_dell"] == "cp/sqrt(17)", "Round35 density")
    require(leaf["source_phase_graph_C2_seminorm"] == "0", "Round35 slope four")
    require(pair["actual_parameterized_common_fw_rev_carrier_pair_registry"] == "CERTIFIED", "Round35 pair")
    require(pair["forward_and_reverse_are_two_views_not_two_charges"] is True, "Round35 once charge")

    r51 = loaded[
        "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json"
    ]["result"]
    view = r51["physical_two_proper_view_object_lemma"]
    common = r51["selected_forward_proper_common_law"]
    require(view["status"] == "CERTIFIED_PHYSICAL_BOREL_TWO_PROPER_VIEW_MEASURE_ISOMORPHISM", "Round51 views")
    require(view["same_ID_once_charge"] is True, "Round51 charge")
    require("Theta" in common["view_transfer_map"], "Round51 Theta")

    r52 = loaded[
        "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json"
    ]["result"]
    terminal = r52["uniform_outer_majorant_terminal_join"]
    separator = r52["large_common_mass_geometric_nonpromotion"]
    require(
        terminal["same_ID_once_charged_common_terminal_survivor_fraction_strict_lower"]
        == "249/250",
        "Round52 mass",
    )
    require(terminal["terminal_not_intermediate"].startswith("the conclusion controls"), "Round52 terminal scope")
    require(separator["status"] == "CERTIFIED_LARGE_COMMON_MASS_BOREL_TWO_VIEW_FIELDS_DO_NOT_IMPLY_PROPER_INTERSECTION", "Round52 separator")

    r53 = loaded[
        "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json"
    ]["result"]
    cap = r53["common_refinement_Z_to_proper_return_clock"]
    require(cap["physical_common_refinement_J_cap_certified"] is False, "Round53 cap open")
    require(cap["physical_proper_same_ID_return_certified"] is False, "Round53 return open")
    require("J_cap,total" in cap["global_hypothesis"], "Round53 target")

    r56j = loaded[
        "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json"
    ]["result"]
    paired56 = r56j["paired_leafwise_reverse_replay"]
    metric56 = r56j["metric_and_once_charge_terminal_source_join"]
    require(r56j["strict_nonpromotion"]["physical_J_pair"] == "CERTIFIED_FINITE", "Round56 J_pair")
    require(paired56["no_same_measure_shortcut"] is True, "Round56 paired replay")
    require(paired56["exact_leaf_type"].startswith("phi(r)=4r+b"), "Round56 exact slope four")
    require(paired56["reverse_first_return"].startswith("the R_n no-intermediate-C_s tag"), "Round56 reverse first return")
    require(paired56["reverse_path_identity"] == "for the tag B=T_s^n(A), T_s^k(I(B))=I(T_s^(n-k)(A)) for 0<=k<=n", "Round56 reverse identity")
    require(metric56["time_reversal_metric_rule"] == "I preserves collision-SRB mass, Euclidean/adapted carrier arclength, density ratios and Z", "Round56 I metric")
    require(r56j["hereditary_replay_and_image_recut_join"]["same_ID_once_charge"] is True, "Round56 same-ID charge")
    require(metric56["forward_view"] == "A -> B" and metric56["reverse_view"] == "I(B) -> I(A)", "Round56 directions")

    r56d = loaded[
        "cm2-gate34-round56-preproperisation-full-clock-downstream-manifest-2026-07-20.json"
    ]["result"]
    require(r56d["actual_full_clock_consequence"]["full_ambient_two_view_max_clock_exponential_moment"] == "CERTIFIED_QUALITATIVELY_FINITE", "Round56 clock")
    require(r56d["strict_nonpromotion"]["physical_common_refinement_J_cap_total"] == "NOT_CERTIFIED", "Round56 cap frontier")
    return loaded


def separator_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for k in (1, 2, 4, 8, 16, 32):
        dyadic = Q(1, 2**k)
        common_partial = FRACTION_COMMON * (1 - dyadic)
        gap_partial = FRACTION_GAP * (1 - dyadic)
        rows.append(
            {
                "K": k,
                "source_blocks_mass": qstr(FRACTION_F * (1 - dyadic)),
                "forward_common_partial_mass": qstr(common_partial),
                "source_gap_partial_mass": qstr(gap_partial),
                "forward_common_u_boundary_Z": str(k),
                "forward_excess_cross_multiplicity_energy": str(max(0, k - 1)),
                "reverse_common_u_boundary_Z": "1",
                "total_common_u_boundary_Z": str(k + 1),
            }
        )
    return rows


def rank_moment_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ell in (Q(3, 2), Q(1), Q(3, 4), Q(1, 8), Q(1, 1024)):
        m = 0
        while Q(2**m) * ell < 1:
            m += 1
        lhs = Q(2**m)
        rhs = Q(1) + Q(2, 1) / ell
        require(lhs <= rhs, "rank moment sample")
        rows.append(
            {
                "min_length": qstr(ell),
                "M": m,
                "two_to_M": qstr(lhs),
                "one_plus_two_over_min_length": qstr(rhs),
                "inequality": True,
            }
        )
    return rows


def cross_component_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in (0, 1, 2, 5, 17, 100):
        base = Q(7, 11)
        lower = Q(n) * base / DENSITY_RATIO
        upper = Q(n) * base * DENSITY_RATIO
        rows.append(
            {
                "positive_common_components_N": n,
                "parent_boundary_density": qstr(base),
                "lower_common_Z": qstr(lower),
                "upper_common_Z": qstr(upper),
                "density_ratio": qstr(DENSITY_RATIO),
            }
        )
    return rows


def palindrome_affine_rows() -> list[dict[str, Any]]:
    """Affine Z bounds Z_stage <= A*Z_in+B*mass_in.

    We deliberately replace every a^K by one.  This makes the rows uniform
    for the unbounded tag-constant stopped time K while retaining finiteness.
    """
    rows = [
        {
            "stage": "input",
            "A_on_Z_in": "1",
            "B_on_mass_in": "0",
        },
        {
            "stage": "first_closed_T_power_K_minus_1",
            "A_on_Z_in": "1",
            "B_on_mass_in": qstr(C_P / 2),
        },
        {
            "stage": "terminal_positive_C24_cut",
            "A_on_Z_in": qstr(CUT_Z1),
            "B_on_mass_in": qstr(CUT_Z1 * C_P / 2),
        },
        {
            "stage": "time_reversal_I",
            "A_on_Z_in": qstr(CUT_Z1),
            "B_on_mass_in": qstr(CUT_Z1 * C_P / 2),
        },
        {
            "stage": "second_closed_T_power_K",
            "A_on_Z_in": qstr(CUT_Z1),
            "B_on_mass_in": qstr(PAL_MASS_COEFF),
        },
        {
            "stage": "final_time_reversal_I_back_to_source",
            "A_on_Z_in": qstr(CUT_Z1),
            "B_on_mass_in": qstr(PAL_MASS_COEFF),
        },
    ]
    require(CLOSED_A < 1, "closed coefficient")
    require(CUT_Z1 > 1, "cut multiplier")
    require(PAL_MASS_COEFF == (CUT_Z1 + 1) * C_P / 2, "palindrome coefficient")
    return rows


def direct_J_pair_consequence() -> dict[str, Any]:
    rows = rank_moment_rows()
    return {
        "cellwise_definition": "M_c=ceil(log2(1/min(ell_fw,c,ell_rev,c)))_+",
        "cellwise_bound": "p_c*2^M_c<=p_c+2*p_c/min(ell_fw,c,ell_rev,c)",
        "integrated_bound": "integral sum_c p_c*2^M_c<=nu(X)+2*J_pair<infinity",
        "physical_full_dyadic_rank_first_moment": "CERTIFIED_FINITE",
        "Dbar_exact_formula": "Dbar=0 for M<=310 and Dbar=M-309 for M>=311",
        "full_dyadic_Dbar_bound": "integral sum_c p_c*2^Dbar(c)<=nu(X)+2^-309*(nu(X)+2*J_pair)<infinity",
        "physical_full_dyadic_Dbar_first_moment": "CERTIFIED_FINITE",
        "why_it_does_not_pay_J_cap": "crossed stopped-map component multiplicity is an independent mark and can be infinite already at M_c=0",
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_FULL_FIRST_POWER_DYADIC_LENGTH_RANK_MOMENT_FROM_J_PAIR",
    }


def exact_slope4_separator() -> dict[str, Any]:
    rows = separator_rows()
    require(FRACTION_COMMON > Q(249, 250), "strict common mass")
    require(FRACTION_F > Q(499, 500), "strict marginal mass")
    return {
        "carrier": "one compact nongrazing exact Round35 leaf phi(r)=4r+b inside a Round56 safe envelope",
        "conditional_mass_coordinate": "u(r)=mu_W([r0,r])/mu_W(W); cp>19/20 makes u an analytic increasing diffeomorphism",
        "views_and_metric": "both ambient views use the same W, the same adapted arclength, and the same positive density-ratio class R=2000/1999",
        "marginal_survivors": "F=R=[0,999/1000) in u-coordinate; each is one connected proper marginal restriction",
        "source_blocks": "block k has u-length (999/1000)2^-k and is A_k of length (998/1000)2^-k followed by gap G_k of length (1/1000)2^-k",
        "source_set_A": "A=(union_k A_k) union [999/1000,1), of mass 999/1000",
        "transport": "theta maps each A_k by translation onto consecutive intervals partitioning [0,998/1000), maps the tail onto [998/1000,999/1000), and maps G_k onto consecutive intervals partitioning [999/1000,1)",
        "physical_coordinate_transport": "Theta_W=u^-1 o theta o u is measure preserving, standard-Borel, and real analytic with bounded positive derivative on every half-open branch",
        "common_forward": "F intersect Theta_W^-1(R)=disjoint union_k A_k",
        "common_reverse": "Theta_W(F) intersect R=[0,998/1000) in u-coordinate",
        "marginal_hit_mass": "1/1000 in each view",
        "common_mass": "499/500>249/250",
        "abstract_normalized_J_pair": "2",
        "abstract_M": 0,
        "marginal_boundary_Z": "1+1=2 in u-coordinate and finite in the adapted metric",
        "forward_common_boundary_divergence": "each A_k restriction has average adapted density at least (1999/2000)*mu_W(W)/ell_*(W)>0, so J_cap,fw=infinity",
        "reverse_common_boundary": "finite: one connected component",
        "conclusion": "finite physical-type J_pair, M=0, finite marginal Z, branchwise analytic bounded-Jacobian transport, and common mass 499/500 do not imply finite J_cap",
        "scope": "field-level nonimplication on the exact carrier class; it is not asserted that the billiard stopped maps realize theta",
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_EXACT_SLOPE4_SAME_METRIC_CROSS_ENDPOINT_SEPARATOR",
    }


def cross_endpoint_theorem() -> dict[str, Any]:
    rows = cross_component_rows()
    return {
        "input_atlas": "standard-Borel connected marginal survivor components W in each view, exact outer disintegration, and no duplicate charge",
        "forward_count": "N_rev_to_fw(W)=number of positive connected components of W intersect Theta^-1(R)",
        "reverse_count": "N_fw_to_rev(W')=number of positive connected components of W' intersect Theta(F)",
        "excess_energy": "E_cross=integral[sum_fw (N_rev_to_fw-1)_+ p_W/ell_*(W)+sum_rev (N_fw_to_rev-1)_+ p_W'/ell_*(W')]",
        "component_inequality": "for density ratio R, (N/R)*p_W/ell_*(W)<=sum_components p_U/ell_*(U)<=R*N*p_W/ell_*(W)",
        "global_upper": "J_cap,total<=R*(Z_fw,marginal+Z_rev,marginal+E_cross)",
        "global_reverse_control": "E_cross<=R*J_cap,total; hence with finite marginal Z, E_cross<infinity iff J_cap,total<infinity",
        "pinned_marginal_fact": "Round47/52 give finite marginal terminal Z; only E_cross is new",
        "shortest_new_physical_input": "construct the common connected-component kernels on the exact paired carrier and prove E_cross<infinity for the actual stopped maps P_fw,P_rev and terminal predicates",
        "conditional_consequence": "E_cross<infinity discharges Round53 J_cap and yields a proper once-charged common terminal two-view reference carrier plus the moment of the single 696*D_cap clock",
        "physical_input_supplied_in_this_leaf": "YES_BY_PALINDROMIC_STOPPED_CUT_REPLAY",
        "not_a_first_return": "the conditional consequence remains two orientation-specific proper pushforwards, not one physical stopping kernel",
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_EXACT_CROSS_COMPONENT_EQUIVALENCE_AND_SHORTEST_INPUT",
    }


def palindromic_stopped_cut_replay() -> dict[str, Any]:
    rows = palindrome_affine_rows()
    return {
        "terminal_time_choice": "choose the pinned uniform terminal time H_joint>=1 beyond both Round52 SYZ thresholds",
        "tagged_time": "K(c)=696*Dbar(c)+H_joint>=1, constant on every immutable Round52/56 physical cell tag c and finite on every tag",
        "exact_identity": "the underlying surviving point reaches T_s^K x and I o T_s^K o I o T_s^K=id on every regular branch, equivalently T_s^K o I o T_s^K=I",
        "operator_off_by_one": "O_s is the pinned one-collision transfer-plus-kill, not a pure current-time restriction; therefore the first closed leg is T_s^(K-1), then O_s supplies collision K",
        "first_leg": "evolve the controlled finite-Z tagged source or positive subfamily by closed T_s^(K-1), retaining every canonical singularity, homogeneity, Growth and recut tag",
        "terminal_cut_scope": "the hash-pinned Round42 report states that every unnormalised C24-killed canonical family satisfies Z(O_s G)<=Z1 Z(G); no properness or survivor normalization is required",
        "terminal_cut": "apply the unnormalised one-collision terminal survivor operator O_s once, whose output is at T_s^K x and obeys Z(O_s G)<=Z1*Z(G)",
        "second_palindrome_scope": "after imposing the forward predicate and transferring to I(B), the input may be an arbitrarily thin nonproper positive canonical subfamily; the same Round42 arbitrary-finite-Z one-step bound applies",
        "marginal_estimate_separation": "properness is used only in the already pinned Round52 marginal SYZ hit estimate; this palindrome reuses its predicate and mass bound but reruns only finite-Z positive-subfamily geometry",
        "return_leg": "from the cut output at T_s^K x apply I, replay closed T_s^K with all branch tags retained, then apply I; surviving atoms return to x as subintervals of their original source carrier",
        "point_set_returned": "exactly the pullback of the chosen terminal survivor predicate, with no normalization and no duplicate charge",
        "cuts_only_refine": "all canonical cuts split analytic branch intervals; the palindrome never transversely redisintegrates the source measure",
        "variable_K_bound": "because 0<a<1, two closed recurrences and one terminal cut give Z_return<=Z1*Z_in+((Z1+1)*C_p/2)*mass_in uniformly in K",
        "Borel_reason": "K is integer-valued Borel, so the stopped palindrome is the countable disjoint union of its finite-K strata; all half-open tags are retained",
        "density_and_domination": "positive interval restriction preserves the invariant cone, curvature and density-ratio class and stays dominated by the same admissible base source",
        "why_fixed_depth_Hardt_is_not_used": "Hardt gives only stratumwise N(696d+H_joint,B0); the palindrome uses Growth Z instead of a component count uniform in unbounded d",
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_UNBOUNDED_STOPPED_TIME_TERMINAL_CUT_PULLBACK_WITH_FINITE_Z",
    }


def physical_common_refinement_closure() -> dict[str, Any]:
    return {
        "index_layers": "y is the Round52 same-parent outer record on which the marginal SYZ mass bounds are stated; c is a Round52/56 once-charged physical cell below y and carries the immutable Dbar,K,path tags",
        "starting_law": "the Round56 exact slope-four once-charged physical cell law A_c<->I(B_c), summed without duplication below each y, with Z_A<=J_pair<infinity and Z_IB<=J_pair<infinity",
        "step_1_forward_predicate": "apply the stopped-cut palindrome on A_c; obtain the exact forward terminal-survivor restriction G_A_fw with finite adapted Z on A",
        "step_2_to_reverse_start": "use the Round41/42 hereditary first-return terminal replay A->B and time reversal B->I(B), preserving c,n,K tags; positive domination makes the total terminal Z finite",
        "step_3_reverse_predicate": "apply the same stopped-cut palindrome on I(B_c); obtain the exact fw-and-rev common restriction G_IB_cap with finite adapted Z on I(B)",
        "step_4_back_to_source": "use the paired hereditary reverse first-return replay I(B)->I(A), then I; obtain G_A_cap on subintervals of the exact original A_c leaves with finite adapted Z",
        "step_5_two_orientation_views": "push G_A_cap by T_s^(696Dbar) to the Round51 forward proper starting view; separately replay A->B->I(B) and push by the same T_s^(696Dbar) to the reverse proper starting view. The closed recurrence gives finite Z in both geometries; continuing the fixed H_joint schedule and O_s also gives finite terminal-output Z",
        "same_raw_restriction": "every proof atom represents the identical raw point restriction S_fw intersect S_rev; forward and reverse are two views of one mass, not two charges",
        "proof_component_kernel": "canonical half-open proof atoms give countable standard-Borel regular connected interval kernels with exact outer disintegration and no duplicate charge; this connected refinement already suffices for the Round53 properisation theorem",
        "physical_maximal_component_registry": "within each fixed y, view and physical carrier chart, merge proof intervals only along an actual-union connected adjacency: the shared endpoint has its unique half-open owner, belongs to the regular common set, and the two-atom union is connected. Closure-touching across an omitted singular, null or cemetery puncture is never merged. Every positive maximal interval contains a rational chart point; the least-rational owner and Borel endpoint infimum/supremum give a standard-Borel enumeration, null singleton components stay in the frozen cemetery, and components are never merged across y",
        "coarsening_inequality": "each physical positive maximal component is a union of proof intervals and p/ell is their length-weighted average, so J_cap,physical<=Z_cap,proof",
        "physical_common_mass": "h_cap(y)>249*p(y)/250 from the pinned Round52 once-charged union bound at the y layer; no such lower bound is asserted for an individual proof cell c",
        "per_y_finiteness": "each y has a finite physical c-fibre; every c has finite n,Dbar,K and every canonical replay has finite Z, hence J_cap(y)<infinity",
        "global_integrability": "the uniform affine palindrome bounds plus the Round41/42 hereditary terminal resolvent and J_pair<infinity give integral J_cap(y)dlambda(y)<infinity",
        "global_affine_chain": "write P(Z,m)=Z1*Z+((Z1+1)*C_p/2)*m and let R(Z,m)=A_R*Z+B_R*m be the Round41/42 hereditary total first-return terminal bound with finite uniform A_R,B_R; then Z1cap<=P(J_pair,nu), Z2cap<=R(Z1cap,nu), Z3cap<=P(Z2cap,nu), Z4cap<=R(Z3cap,nu), and the two proper-view outputs are bounded by closed affine images of Z4cap",
        "uniformity_of_global_constants": "Z1,C_p,A_R,B_R are independent of y,c,n,Dbar and K; all unbounded stopped depths are absorbed by a^r<=1 and all first-return depths are summed by the pinned hereditary terminal resolvent",
        "physical_J_cap_total": "J_cap,total<=Z_cap,fw-proper-view,proof+Z_cap,rev-proper-view,proof<infinity",
        "physical_cross_endpoint_energy": "finite by the certified component equivalence because marginal Z and J_cap,total are finite",
        "Round53_join": "the now-actual y-indexed J_cap hypothesis gives Borel D_cap(y), synchronized 696*D_cap(y) properisation, and the finite exp(D_cap/6) moment on the common law",
        "full_dyadic_D_cap_bound": "integral h(y)*2^D_cap(y)dlambda(y)<=H+(4/C_p)*J_cap,total<infinity, using D_cap=0 or 2^D_cap<=4*z_cap/C_p",
        "physical_full_dyadic_D_cap_first_moment": "CERTIFIED_FINITE",
        "actual_proper_object": "a proper once-charged common terminal-survivor two-view reference carrier with one selected proper view and transported reverse data",
        "not_yet_physical_first_return": "the common raw restriction inherits the original tau_R=n same-ID A->B first-return graph and its no-earlier-C_s tag, but its landing family is not thereby the required proper common kernel; the two later stopped orientation-specific pushforwards still do not define one physical first-hit landing map",
        "status": "CERTIFIED_PHYSICAL_COMMON_REFINEMENT_J_CAP_AND_SINGLE_D_CAP_CLOCK",
    }


def independent_later_obstructions() -> dict[str, Any]:
    return {
        "proper_same_ID_first_return": {
            "inherited_but_insufficient_graph": "the common raw restriction retains tau_R=n and the original A->B same-ID first-return graph with no earlier C_s hit",
            "missing_object": "a proof that the inherited landing restriction is one proper common physical target kernel, or another Borel tau_cap and Q_cap(x)=T_s^tau_cap(x) with the same physical restriction ID, first-hit semantics for the required target, exact once charge, and no normalization",
            "two_view_transport_is_insufficient": "two proper pushforwards linked by Theta can land in disjoint labelled target carriers and therefore need not define one physical landing map",
            "status": "INDEPENDENT_PHYSICAL_KERNEL_INTERFACE_NOT_CERTIFIED",
        },
        "intermediate_C24_avoidance": {
            "separator": "on X={0,1,2}x[0,1], T(i,u)=(i+1 mod 3,u), start at state 0, C24={state 1}, and terminal time 2; terminal nonhit mass is one while intermediate-avoidance mass is zero",
            "needed_input": "a killed/stopped path predicate excluding C24 at every required intermediate collision on the same tau_cap kernel",
            "status": "TERMINAL_NONHIT_DOES_NOT_IMPLY_INTERMEDIATE_AVOIDANCE",
        },
        "later_repeated_clocks": {
            "separator": "on atoms A_n of mass 2^-n, let later clock L_n=n^2 on A_n and zero elsewhere; every fixed-stage exponential moment is finite, but the exponential moment of sup_n L_n contains sum_n 2^-n exp(n^2/4176)=infinity",
            "needed_input": "one summable or dominating exponential envelope for all later/repeated clocks on the tau_cap law",
            "status": "ONE_OR_FIXED_STAGE_CLOCK_MOMENTS_DO_NOT_IMPLY_ALL_STAGE_MOMENT",
        },
        "physical_q_and_cemetery": {
            "needed_q_join": "only after tau_cap, intermediate avoidance and the all-stage clock envelope exist may the Round28 physical q be typed and tested in L^(6/5)",
            "strong_cemetery": "absolute-continuous exhaustion remains insufficient for singular trace/current charge",
            "status": "NOT_CERTIFIED_INDEPENDENT_INTERFACES",
        },
    }


def literature_audit() -> dict[str, Any]:
    return {
        "source": "Demers--Liverani, Recent Progress in the Application of Transfer Operators to Dispersing Billiards, arXiv:2606.10155v1",
        "official_pdf": "https://arxiv.org/pdf/2606.10155v1",
        "retrieved": "2026-07-20",
        "pdf_sha256": REVIEW_PDF_SHA256,
        "targeted_text_hits": {"coupling": 1, "holonomy": 2, "standard_famil": 0, "common_return": 0, "common_refinement": 0, "same_ID": 0, "cemetery": 0},
        "conclusion": "the review supplies context on transfer operators, coupling and absolute-continuous holonomy, but no theorem located there instantiates E_cross, the exact same-ID stopping kernel, all-intermediate avoidance, or the strong cemetery for this carrier",
        "external_theorem_promoted": False,
        "status": "TARGETED_OFFICIAL_LITERATURE_AUDIT_NO_DIRECT_INTERFACE_FOUND",
    }


def strict_frontier() -> dict[str, Any]:
    return {
        "physical_J_pair": "CERTIFIED_FINITE_PINNED_ROUND56",
        "physical_defect_moment_I_D": "CERTIFIED_FINITE_PINNED_ROUND56",
        "full_ambient_two_view_max_clock_moment": "CERTIFIED_QUALITATIVELY_FINITE_PINNED_ROUND56",
        "physical_full_dyadic_length_rank_first_moment": "CERTIFIED_FINITE",
        "physical_full_dyadic_Dbar_first_moment": "CERTIFIED_FINITE",
        "exact_cross_component_equivalence": "CERTIFIED",
        "exact_slope4_same_metric_nonimplication": "CERTIFIED",
        "palindromic_unbounded_stopped_cut_replay": "CERTIFIED_FINITE_Z",
        "physical_cross_endpoint_energy_E_cross": "CERTIFIED_FINITE",
        "physical_common_refinement_J_cap_total": "CERTIFIED_FINITE",
        "single_common_properisation_clock_D_cap_moment": "CERTIFIED_FINITE",
        "physical_full_dyadic_D_cap_first_moment": "CERTIFIED_FINITE",
        "proper_common_terminal_two_view_carrier": "CERTIFIED",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_after_properisation": "NOT_CERTIFIED",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def build_result() -> dict[str, Any]:
    load_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "claim_type": "palindromic stopped-cut finite-Z replay, physical J_cap/D_cap closure, and strict remaining frontier",
            "external_theorem_promoted": False,
        },
        "direct_J_pair_rank_moment_consequence": direct_J_pair_consequence(),
        "exact_slope4_cross_endpoint_separator": exact_slope4_separator(),
        "cross_endpoint_component_theorem": cross_endpoint_theorem(),
        "palindromic_stopped_cut_replay": palindromic_stopped_cut_replay(),
        "physical_common_refinement_closure": physical_common_refinement_closure(),
        "independent_downstream_obstructions": independent_later_obstructions(),
        "latest_technical_literature_audit": literature_audit(),
        "strict_nonpromotion": strict_frontier(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = DEFAULT_VERIFIER) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file() and not verifier.is_symlink(), "verifier path")
    require(verifier.parent == HERE, "verifier outside deliverables")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "dependencies": dict(DEPENDENCIES),
        "pinned_reports": dict(PINNED_REPORTS),
        "result": result,
        "verdict": dict(result["strict_nonpromotion"]),
    }


def pretty_manifest(verifier: Path = DEFAULT_VERIFIER) -> str:
    return json.dumps(build_manifest(verifier), indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    text = pretty_manifest(args.verifier)
    if args.write_manifest is not None:
        target = args.write_manifest.resolve()
        require(target.parent == HERE, "manifest target outside deliverables")
        target.write_text(text, encoding="utf-8")
        return 0
    if args.manifest_json:
        print(text, end="")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("DYADIC_RANK_MOMENT:", strict["physical_full_dyadic_length_rank_first_moment"])
    print("PALINDROMIC_REPLAY:", strict["palindromic_unbounded_stopped_cut_replay"])
    print("PHYSICAL_E_CROSS:", strict["physical_cross_endpoint_energy_E_cross"])
    print("PHYSICAL_J_CAP:", strict["physical_common_refinement_J_cap_total"])
    print("PHYSICAL_Q:", strict["physical_collision_time_q_L6over5"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
