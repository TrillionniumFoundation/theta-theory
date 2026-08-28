#!/usr/bin/env python3
"""Round-50 physical whole-family grouping and common-law join frontier.

This leaf performs the object-level join that was missing in Round 49.  At
fixed ``s`` and finite return depth, the Round-35 standard-Borel registry is
projected onto one complete source-fibre interval.  All deterministic natural
short cells (and their reverse image recuts) are grouped under that one ID.
The group is finite, hence has finite boundary numerator in each orientation.

The physical grouping and the two orientation-specific recordwise
properizations are real.  They do *not*, however, make the raw ``K_par`` fibre
itself a proper family.  A two-proper-view pullback lemma (or one explicitly
chosen common proper pushforward kernel) is still required before the abstract
Round-49 common-parent-law ``W_r`` theorem can be installed.  The physical
exponential moment of the variable pre-recovery clock is also unavailable.
The file therefore deliberately does not promote C_fw/C_rev/q, the strong
cemetery, Gate 4, or CM2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round50-physical-whole-family-grouping.v2"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v2"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
    "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json": (
        "68f0ee7595688ef4ea1ab5eb1e101ab8c2ccd327d3bcf40876ccbd40a5d9bfab"
    ),
    "cm2-gate34-round49-sharp-common-law-recovery-manifest-2026-07-19.json": (
        "0cf5d0d6eac469a2ab6f1100a738384af2873473a4ef6457beb1bb45e734f00a"
    ),
    "cm2-gate5-round34-rank-path-core-preimage-f9-manifest-2026-07-19.json": (
        "323cdeb40a78d29e0e767b438ef1e6fe0c28d8da80a10e0b4f4d717d4f308515"
    ),
}

CLOSED_A = Q(360134800, 360493663)
CLOSED_B = Q(2 * 10**90)
C_P = Q(4 * 10**90 * 360493663, 358863)
HALF_BLOCK = 696
ETA = Q(1, 4176)
BASE_RANK = 14
D1_ONE = 151 * 2**BASE_RANK


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependencies() -> None:
    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    registry = carrier["arbitrary_Rn_parent_W_Borel_registry"]
    disintegration = carrier["collision_SRB_leaf_disintegration"]
    pair = carrier["common_forward_reverse_carrier_pair"]
    if registry["registry_type"] != "standard-Borel parameterized actual curve registry":
        raise RuntimeError("registry type")
    if registry["U_intersection_leaf"] != "countable disjoint union of open intervals":
        raise RuntimeError("source intervals")
    if disintegration["integrating_leaf_weights_recovers_mu_s_restricted_to_component"] is not True:
        raise RuntimeError("physical disintegration")
    if pair["actual_parameterized_common_fw_rev_carrier_pair_registry"] != "CERTIFIED":
        raise RuntimeError("common pair")
    if pair["forward_and_reverse_are_two_views_not_two_charges"] is not True:
        raise RuntimeError("once charge")

    d1 = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]
    if d1["global_physical_L6over5_moment"]["status"] != (
        "CERTIFIED_PHYSICAL_GLOBAL_L6OVER5_MOMENT"
    ):
        raise RuntimeError("D1 moment")
    if d1["strict_nonpromotion"]["D1_rank_sum_dominates_complete_C_fw_C_rev"] is not False:
        raise RuntimeError("D1 scope")

    round48 = load(
        "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json"
    )["result"]
    if round48["fixed_s_Borel_parent_survivor_kernel"]["status"] != (
        "CERTIFIED_FIXED_S_BOREL_PARENT_SURVIVOR_SUBKERNEL_SCHEMA"
    ):
        raise RuntimeError("Round48 Borel kernel")
    if round48["strict_nonpromotion"]["whole_proper_family_kernel_join"] != "NOT_CERTIFIED":
        raise RuntimeError("Round48 frontier")

    round49 = load(
        "cm2-gate34-round49-sharp-common-law-recovery-manifest-2026-07-19.json"
    )["result"]
    if round49["exact_sharp_closed_half_block"][
        "shortest_positive_integer_L_with_a_power_below_half"
    ] != HALF_BLOCK:
        raise RuntimeError("half block")
    if round49["same_ID_common_parent_law_W_r_theorem"]["status"] != (
        "CERTIFIED_CONDITIONAL_COMMON_PARENT_LAW_W_R_THEOREM"
    ):
        raise RuntimeError("common-law theorem")
    if round49["strict_nonpromotion"]["Gate4"] != "NOT_CERTIFIED":
        raise RuntimeError("Round49 Gate4")

    f9 = load(
        "cm2-gate5-round34-rank-path-core-preimage-f9-manifest-2026-07-19.json"
    )["result"]
    ranked = f9["ranked_one_collision_C2_envelope"]
    composition = f9["arbitrary_time_composition_recurrence"]
    if ranked["forward_D_infinity_strict_upper"] != "L(B)=150*2^B":
        raise RuntimeError("rank-path derivative factor")
    if composition["finite_for_every_finite_rank_path"] is not True:
        raise RuntimeError("finite rank-path derivative product")


def safe_defect_from_min_length_rank(M: int) -> int:
    """Safe common fw/rev properization defect for Z/m <= 2^M."""
    ratio = Q(2**M)
    if ratio <= C_P:
        return 0
    defect = 1
    while Q(1, 2**defect) * ratio >= C_P / 2:
        defect += 1
    return defect


def defect_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for M in (0, 14, 299, 310, 311, 319, 330, 400):
        defect = safe_defect_from_min_length_rank(M)
        rows.append(
            {
                "common_min_length_rank_M": M,
                "common_Z_over_mass_upper": f"2^{M}",
                "safe_defect_Dbar": defect,
                "preproperization_clock": HALF_BLOCK * defect,
                "already_proper_from_upper_bound": defect == 0,
            }
        )
    return rows


def physical_grouping() -> dict[str, Any]:
    rows = defect_rows()
    return {
        "parameter_scope": "every fixed |s|<=1/400 and fixed finite n",
        "Borel_family_id": (
            "rn-whole-family:(s,component-id,b,source-interval-rank,incidence-rank-path)"
        ),
        "grouping_projection": (
            "forget natural-short-cell-k and image-recut-rank; retain exactly one complete positive source-fibre interval and all of its deterministic source cells/image recuts"
        ),
        "source_interval_geometry": (
            "the complete positive interval lies in one bounded C24 source chart, so its Euclidean carrier length L_src(y) is finite"
        ),
        "half_open_endpoint_owner": (
            "use oriented half-open natural cells [k*1e-90,(k+1)*1e-90), clipped to the open source interval; use the same one-sided owner for image recuts"
        ),
        "endpoint_scope": (
            "internal endpoints have exactly one owner; the two outer open-interval endpoints remain in the already null regular-boundary cemetery"
        ),
        "upstream_recut_compatibility": (
            "the half-open representative only retypes shared null endpoints of the frozen deterministic recuts; it changes no positive-mass Round35 restriction"
        ),
        "finite_rank_path_derivative_product": (
            "D_path(y)=product_{i=1}^n(150*2^B_i)<infinity for every fixed finite incidence-rank path"
        ),
        "source_short_cell_count": (
            "N_src(y)<=ceil(L_src(y)*10^90)+1<infinity"
        ),
        "image_length_bound": (
            "length(H(A_k))<=D_path(y)*length(A_k)<infinity"
        ),
        "image_recut_count": (
            "N_img(y,k)<=ceil(length(H(A_k))*10^90)+1<infinity"
        ),
        "why_each_group_has_finitely_many_cells": (
            "the bounded source interval has finitely many 1e-90 cells, and the uniform finite rank-path derivative product gives every source cell finite image length and hence finite image-recut counts"
        ),
        "finite_fibre_Borel_projection": (
            "the Round35 record space is Borel and the projection forgetting (natural-short-cell-k,image-recut-rank) has finite fibres; Lusin-Novikov therefore makes its image Borel and supplies Borel record enumerations"
        ),
        "outer_index_space": (
            "standard-Borel: countable component/interval/path codes times the Borel leaf intercept b"
        ),
        "parent_kernel": (
            "K_par(y,A)=the Round35 collision-SRB leaf kernel restricted to the complete interval group y"
        ),
        "exact_outer_disintegration": (
            "integrating K_par over b and summing the countable component/interval/path codes reconstructs mu_s on the regular arbitrary-R_n registry modulo its null boundary"
        ),
        "kernel_partition_identities_mod_null": [
            "sum_{k,j}K_fw(y,k,j;A)=K_par(y,A)",
            "sum_{k,j}K_rev(y,k,j;A)=K_par(y,A)",
        ],
        "kernel_identity_scope": (
            "both identities hold after pulling the deterministic image recuts back to the source restriction; half-open ownership removes internal duplication and only the pre-existing null outer boundary is omitted"
        ),
        "same_ID_two_view_join": (
            "the deterministic image recuts are pulled back to the identical Round35 restriction ID; fw and rev are two alternative finite partitions of one K_par charge, never two charges"
        ),
        "orientation_lengths": (
            "ell_fw(y,j),ell_rev(y,j)>0 are Borel on every regular finite-recut record"
        ),
        "boundary_numerators": [
            "J_fw(y)=sum_j p_fw(y,j)/ell_fw(y,j)<infinity",
            "J_rev(y)=sum_j p_rev(y,j)/ell_rev(y,j)<infinity",
        ],
        "recordwise_finite_J_reason": "finite sum of finite positive-length terms",
        "physical_full_registry_reconstructed": True,
        "numeric_nonempty_component_enumeration_claimed": False,
        "uniform_J_over_mass_bound_claimed": False,
        "status": "CERTIFIED_PHYSICAL_BOREL_WHOLE_STANDARD_FAMILY_GROUPING_WITH_RECORDWISE_FINITE_J",
        "sample_defect_rows": rows,
        "sample_defect_rows_sha256": digest(rows),
    }


def recordwise_properization_and_common_law() -> dict[str, Any]:
    assert CLOSED_B / (1 - CLOSED_A) == C_P / 2
    assert 2 * CLOSED_A.numerator**695 > CLOSED_A.denominator**695
    assert 2 * CLOSED_A.numerator**696 < CLOSED_A.denominator**696
    return {
        "common_min_length_rank": (
            "M(y)=ceil(log2(1/min_j(ell_fw(y,j),ell_rev(y,j))))_+ is finite and Borel"
        ),
        "two_orientation_boundary_bound": "max(J_fw,J_rev)<=2^M*p(y)",
        "safe_defect": (
            "Dbar(M)=0 if 2^M<=C_p; otherwise the least d>=1 with 2^(-d)*2^M<C_p/2"
        ),
        "closed_recurrence": (
            "Z(T^r G)/mass(G)<=a^r*Z(G)/mass(G)+C_p/2"
        ),
        "common_preproperization_clock": "R0(y)=696*Dbar(M(y))",
        "recordwise_conclusion": (
            "after their respective orientation-specific measure-preserving 696*Dbar evolutions, each pushforward whole family is in Z<C_p*mass; this does not assert that raw K_par is proper"
        ),
        "Borel_stopped_kernel_reason": (
            "Dbar is integer-valued Borel, so the stopped pushforward is the countable Borel union over {Dbar=d}"
        ),
        "raw_common_charge_law": (
            "m_raw(dy,dx)=lambda(dy)K_par(y,dx) charges the original physical parent restriction once"
        ),
        "raw_K_par_is_a_proper_whole_family": False,
        "raw_K_par_type_mismatch_with_Round49": (
            "Round49 requires one outer kernel whose fibre G_y is itself proper; pulling two different orientation-specific proper pushforwards back to m_raw does not make the raw K_par geometry proper"
        ),
        "literal_single_common_proper_kernel": "NOT_INSTALLED",
        "two_proper_view_pullback_lemma": "NOT_INSTALLED",
        "repair_route": (
            "either prove a Borel measure-preserving two-proper-view pullback lemma, or choose K_par_star=(F_fw)_#K_par as one common proper law and transport the reverse predicate through F_rev o F_fw^-1"
        ),
        "Round49_W_r_hypotheses_after_recordwise_properization": False,
        "conditional_postproperization_fixed_H_W_r_moment": (
            "if the missing pullback/common-proper-kernel lemma is installed, integral W_r^r dm<(1+2*A_H)*integral p dlambda for every fixed finite H"
        ),
        "postproperization_fixed_H_W_r_moment_certified": False,
        "preproperization_clock_included_in_conditional_W_r": False,
        "conditional_complete_total_clock_weight": (
            "after that missing join, Wtilde_r=exp(Dbar/(6*r))*W_r because R0/(4176*r)=Dbar/(6*r)"
        ),
        "missing_integrability_for_total_clock": (
            "integral p(y)*exp(Dbar(y)/6) dlambda(y)<infinity"
        ),
        "rational_sufficient_moment": (
            "integral p(y)*(6/5)^Dbar(y) dlambda(y)<infinity"
        ),
        "status": "CERTIFIED_RECORDWISE_TWO_ORIENTATION_PROPERIZATION__COMMON_PARENT_LAW_JOIN_NOT_INSTALLED",
    }


def short_length_tail_bridge() -> dict[str, Any]:
    # If P(M>m)<=C*2^-m, layer cake for a=6/5 gives
    # E a^M <= 1+C(a-1)/(1-a/2)=1+C/2.
    a = Q(6, 5)
    coefficient = (a - 1) / (1 - a / 2)
    assert coefficient == Q(1, 2)
    return {
        "target_tail": (
            "integral_{M>m}p(y)dlambda <= C_len*2^-m for all integers m>=0"
        ),
        "exact_layer_cake": (
            "integral (6/5)^M p <= integral p + sum_m((6/5)^(m+1)-(6/5)^m)*mass{M>m}"
        ),
        "geometric_ratio": "(6/5)/2=3/5",
        "conditional_bound": "integral (6/5)^M p <= mass_total+C_len/2",
        "Dbar_dominated_by_M_up_to_the_fixed_C_p_offset": True,
        "would_close_preproperization_clock_moment": True,
        "available_for_physical_arbitrary_Rn_grouped_restrictions": False,
        "Round26_C24_one_step_tube_is_this_same_measure_kernel": False,
        "status": "CERTIFIED_CONDITIONAL_LINEAR_SHORT_LENGTH_TAIL_BRIDGE",
    }


def d1_nonimplication_countermodel() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for n in (19, 20, 21, 22, 24):
        count = 2 ** (n * n)
        width = Q(1, 2**n)
        length = Q(1, count)
        mass = width
        J = width * count
        actual_defect = 0
        ratio = Q(count)
        if ratio > C_P:
            actual_defect = 1
            while Q(1, 2**actual_defect) * ratio >= C_P / 2:
                actual_defect += 1
        rows.append(
            {
                "band_n": n,
                "b_band_width": qstr(width),
                "interval_count": f"2^{n*n}",
                "each_interval_length": f"2^-{n*n}",
                "band_mass": qstr(mass),
                "boundary_J": f"2^{n*n-n}",
                "J_over_mass": f"2^{n*n}",
                "safe_actual_defect": actual_defect,
            }
        )
    return {
        "construction": (
            "on disjoint b-bands of width 2^-n, partition the unit r-fibre into 2^(n^2) equal open intervals; use uniform 2D density and constant incidence rank B=14"
        ),
        "physical_mass": "band n has mass 2^-n, so total mass is finite",
        "D1_density": f"constant one-step c_D1={D1_ONE}",
        "D1_L6over5": "finite because c_D1 is constant and sum_n 2^-n<infinity",
        "boundary_ratio": "J_n/m_n=2^(n^2)",
        "defect_growth": "D_Z(n)>=n^2-ceil(log2(C_p))-2 for all sufficiently large n",
        "missing_moment_diverges": (
            "2^-n*(6/5)^D_Z(n) does not tend to zero; successive ratios eventually dominate (1/2)*(6/5)^(2n+1)"
        ),
        "logical_scope": (
            "an exact standard-Borel uniform-area partition model showing that the currently certified disintegration, finite mass, and D1 rank moment do not imply the required inverse-length/defect moment; it is not asserted to be an actual billiard fibre"
        ),
        "Round35_D1_implies_D_Z_moment": False,
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_EXACT_D1_VERSUS_INVERSE_LENGTH_NONIMPLICATION",
    }


def weak_and_strong_cemetery() -> dict[str, Any]:
    return {
        "scope": (
            "for every fixed (s,n); for the countable full first-return union, include the return depth n among the bounded family-code ranks"
        ),
        "finite_rank_exhaustion": (
            "E_M(s,n)={family-code ranks<=M and common minimum cell length>=2^-M}; E_M^global additionally requires n<=M"
        ),
        "global_depth_owner": "return depth n is an explicit code rank in E_M^global",
        "Borel_and_nested": True,
        "union_covers_regular_registry": True,
        "weak_discarded_mass": (
            "m(E_M(s,n)^c)->0 at fixed (s,n), and m((E_M^global)^c)->0 on the countable finite-mass first-return union, by monotone convergence"
        ),
        "weak_L1_cemetery": "CERTIFIED",
        "discarded_boundary_J_tends_to_zero": "NOT_CERTIFIED",
        "discarded_D_Z_weighted_mass_tends_to_zero": "NOT_CERTIFIED",
        "strong_trace_current_cemetery": "NOT_CERTIFIED",
        "reason": (
            "mass exhaustion has no uniform-integrability content for inverse length; the D1 countermodel can have vanishing discarded mass and divergent discarded J"
        ),
        "proper_common_fw_rev_intersection": "NOT_CERTIFIED",
        "status": "CERTIFIED_WEAK_MASS_CEMETERY_ONLY",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "depth_scope": "every fixed finite first-return depth n",
        },
        "physical_Borel_whole_family_grouping": physical_grouping(),
        "recordwise_properization_and_common_parent_law": (
            recordwise_properization_and_common_law()
        ),
        "conditional_linear_short_length_tail_bridge": short_length_tail_bridge(),
        "D1_inverse_length_nonimplication": d1_nonimplication_countermodel(),
        "cemetery_frontier": weak_and_strong_cemetery(),
        "corrected_frontier": {
            "Borel_family_id": "CERTIFIED",
            "exact_outer_disintegration_reconstructing_physical_mass": "CERTIFIED",
            "recordwise_finite_J_fw_J_rev": "CERTIFIED",
            "Borel_D_Z_and_recordwise_696_D_Z_properization": "CERTIFIED",
            "raw_K_par_is_Round49_proper_outer_kernel": False,
            "two_proper_view_pullback_lemma": "NOT_INSTALLED",
            "same_ID_common_parent_law_join_after_recordwise_properization": "NOT_CERTIFIED",
            "conditional_postproperization_W_r_formula": (
                "CERTIFIED_CONDITIONAL_ON_TWO_PROPER_VIEW_PULLBACK_LEMMA"
            ),
            "physical_exponential_moment_of_preproperization_D_Z": "NOT_CERTIFIED",
            "full_total_clock_common_law_Lp_join": "NOT_CERTIFIED",
            "proper_common_fw_rev_intersection": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "numeric_H_cover": None,
            "numeric_actual_beta": None,
        },
        "strict_nonpromotion": {
            "physical_Borel_whole_standard_family_grouping": "CERTIFIED",
            "recordwise_finite_J_and_properization": "CERTIFIED",
            "postproperization_same_ID_common_parent_law": "NOT_CERTIFIED",
            "Round49_W_r_literal_join": "NOT_INSTALLED",
            "global_preproperization_clock_moment": "NOT_CERTIFIED",
            "full_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "numeric_collision_time_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_round50_physical_whole_family_grouping_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    strict = result["strict_nonpromotion"]
    print("WHOLE_STANDARD_FAMILY_GROUPING:", strict["physical_Borel_whole_standard_family_grouping"])
    print("RECORDWISE_PROPERIZATION:", strict["recordwise_finite_J_and_properization"])
    print("GLOBAL_DZ_MOMENT:", strict["global_preproperization_clock_moment"])
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
