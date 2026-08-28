#!/usr/bin/env python3
"""Round-55 Gate-4 hereditary terminal-Z and refinement frontier.

The Round-41/42 every-collision C24-killed Growth theorem already controls
the survivor family on blocks of ``L=9148*N_open`` collisions.  This leaf
fills the finitely many residues with the numerical one-step constant and
replays the same estimate for the all-mass extra-cut operator.  Terminal
return pieces are positive subfamilies of that all-mass image.  Consequently
the *coarse* forward/reverse terminal boundary numerator is summable without
the Round-54 ``Phi_pair`` forcing ledger.

The result deliberately stops before physical ``J_pair``.  The deterministic
natural-cell/image-recut subdivision needs a multiplicity-weighted terminal
numerator.  Recordwise finite subdivision and the frozen one-time rank/D1
moments do not supply its global integral; Round 36 contains an exact
perfectly-correlated-rank nonimplication model.  The official gap-extension
cutpoint also cannot be used as a zero-debit density join: either the whole
gap retains an 11/9 jump, or the two constant-density halves can have
arbitrarily small individual lengths.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round55-hereditary-terminal-z-refinement-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round55-hereditary-terminal-z-refinement-frontier-manifest-2026-07-20.json"
)

DEPENDENCIES = {
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json": (
        "a98203ebf820d959f9e04c213cd1d79c3809744671fd509c40e531bdc552c119"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate34-round54-survivor-mass-terminal-extraction-common-atlas-manifest-2026-07-20.json": (
        "941929e86bdecd1d3fc8d935ed685b346ea2bedc3fba0c24bd949f5f88b66c2f"
    ),
    "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json": (
        "2c6ab1c0b3b89000e6d96d04a60d7c662855ae1f24c1d9f43405df04732d7e58"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json": (
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73"
    ),
    "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json": (
        "8b6bd9a1b72e1d222ea0b370f046defbf90b10935c55271d4f5bf81a36835ba5"
    ),
    "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json": (
        "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3"
    ),
}

N_STAR = 9148
B0 = 49
DENSITY_RATIO = Q(2000, 1999)
THETA = Q(900337, 901685)
Z1 = Q(18367592526, 360493663)
SURVIVAL = Q(111718729, 111718750)
BASE_RANK = 14
PATH_FACTOR_AT_BASE_RANK = 150 * 2**BASE_RANK
D1_FACTOR_AT_BASE_RANK = 151 * 2**BASE_RANK

ARXIV_SOURCE_AUDIT = {
    "paper": "Stenlund--Young--Zhang, arXiv:1210.0011v4",
    "official_source_url": "https://export.arxiv.org/e-print/1210.0011v4",
    "official_source_tar_sha256": (
        "b705ed4fc89a42ac8e78957d65873211c71f9566599bfba90173812fe5ffe5c5"
    ),
    "extracted_Moving_final_tex_sha256": (
        "921fe3477c2f3280a256a459c9e2a2bc6b719a971016a8320e6d0d5e9cd25f44"
    ),
    "retrieved_utc_date": "2026-07-20",
}


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(key)
        value[key] = item
    return value


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
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
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency mismatch: {name}")
        value = parse_json_text(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency root: {name}")
        loaded[name] = value

    c24_geometry = loaded[
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    ]["result"]
    require(
        c24_geometry["frozen_core_inventory"]["core_count"] == 24,
        "C24 core count",
    )
    require(
        c24_geometry["stable_curve_open_hole_geometry"][
            "time_reversal_of_frozen_invariant_unstable_cone"
        ]
        is True,
        "C24 time-reversal cone",
    )
    require(
        c24_geometry["sparse_opening_theorem_interface"]["hole"]
        == "H=C24_in_the_common_solid_collision_section",
        "C24 hole identity",
    )

    round27 = loaded[
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    ]["result"]
    c24_path = round27["C24_full_dimensional_arbitrary_n_candidate_path_join"]
    require(
        c24_path["source_carrier"]
        == "C_s=disjoint_mod_faces_union_of_24_physical_2D_cores",
        "Round27 C_s source",
    )
    require(
        c24_path["candidate_path_fibres_cover_C24_mod_singular_collision_null"]
        is True,
        "Round27 C_s/C24 join",
    )

    round41 = loaded[
        "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json"
    ]["result"]
    extra = round41["extra_cut_standard_family_Growth"]
    killed = round41["unnormalized_killed_subfamily_Growth"]
    aggregate = round41["aggregate_canonical_Z_resolvent"]
    require(extra["extra_cut_map_keeps_all_mass"] is True, "Round41 all mass")
    require(
        extra["extra_cut_map"] == "hat_F_(s,C24)", "Round41 extra-cut map"
    )
    require(
        killed["same_ID_registry"] is True
        and killed["conditional_survival_normalization_used"] is False,
        "Round41 killed typing",
    )
    require(
        aggregate["common_block"] == "L=N_open*n_* collision steps",
        "Round41 common block",
    )
    require(
        aggregate["physical_aggregate_Z_weighted_tail"]
        == "CERTIFIED_QUALITATIVE_FOR_CONTROLLED_FINITE_Z_INITIAL_FAMILIES",
        "Round41 aggregate Z",
    )
    require(
        aggregate["input"]
        == "a controlled canonical finite-Z physical initial family dominated as a positive measure by an admissible base-cone source",
        "Round41 base-source domination",
    )

    round42 = loaded[
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    ]["result"]
    numerical = round42["numerical_C24_killed_Growth"]
    resolvent = round42["aggregate_canonical_Z_resolvent"]
    require(numerical["block_depth_n_star"] == N_STAR, "Round42 n star")
    require(
        numerical["one_step_Z_multiplier_Z1"] == qstr(Z1), "Round42 Z1"
    )
    require(
        numerical["hereditary_under_positive_C24_killing"] is True,
        "Round42 heredity",
    )
    require(
        resolvent["common_collision_block"] == "L=9148*N_open",
        "Round42 collision block",
    )
    require(
        resolvent["block_index_weight_and_resolvent"]
        == "CERTIFIED_EXACT_SYMBOLIC",
        "Round42 weighted resolvent",
    )

    round54 = loaded[
        "cm2-gate34-round54-survivor-mass-terminal-extraction-common-atlas-manifest-2026-07-20.json"
    ]["result"]
    mass = round54["killed_survivor_mass_join"]
    terminal = round54["two_orientation_terminal_extraction"]
    require(
        mass["mass_identity"]
        == "m_n=mass(F_n)=mu_s(Q_n)=mu_s(C_s)*S_n",
        "Round54 survivor IDs",
    )
    require(
        mass["initial_state"]
        == "F_0=mu_s restricted to Q_0=mu_s restricted to C_s",
        "Round54 physical initial state",
    )
    require(
        mass["terminal_and_survivor_split"]
        == [
            "E_(n+1)=1_C_s G_(n+1), carrying exactly the R_(n+1) terminal IDs",
            "F_(n+1)=1_(C_s^c) G_(n+1), carrying exactly the Q_(n+1) prefix IDs",
        ],
        "Round54 complementary IDs",
    )
    require(
        terminal["first_level_check"].startswith("n=0 produces the forward R_1"),
        "Round54 terminal index",
    )
    require(
        terminal["orientation_specific_cores"][
            "no_time_reversal_invariance_of_the_literal_core_asserted"
        ]
        is True,
        "Round54 distinct cores",
    )
    require(
        "preserves collision-SRB measure and the adapted/Euclidean carrier arclength"
        in terminal["orientation_specific_cores"]["same_multiplier_reason"],
        "Round54 time-reversal isometry",
    )
    require(
        terminal["terminal_cell_refinement_to_J_pair_same_ID_Z_join"]
        == "NOT_CERTIFIED",
        "Round54 refinement frontier",
    )

    round53 = loaded[
        "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json"
    ]["result"]
    bridge = round53["fractional_cell_Z_to_defect_moment"]
    require(
        bridge["pair_boundary_numerator"]
        == "J_pair=integral sum_c p_c*(ell_fw,c^-1+ell_rev,c^-1) dlambda",
        "Round53 J_pair",
    )
    require(
        bridge["direct_linear_tail_layer_cake_bound"]
        == "I_D<nu(X)+[35/(99*2^309)]*J_pair",
        "Round53 defect bridge",
    )

    carrier = loaded[
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    ]["result"]["common_forward_reverse_carrier_pair"]
    require(
        carrier["actual_parameterized_common_fw_rev_carrier_pair_registry"]
        == "CERTIFIED",
        "Round35 carrier",
    )
    require(
        carrier["forward_and_reverse_are_two_views_not_two_charges"] is True,
        "Round35 once charge",
    )
    require(
        carrier["mu_s_A_equals_mu_s_B_equals_mu_s_I_B"] is True
        and carrier["reverse_oriented_branch"] == "I(B) -> I(A) by T_s^n",
        "Round35 reverse mass conjugacy",
    )

    rank = loaded[
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    ]["result"]
    require(
        rank["global_physical_L6over5_moment"]["status"]
        == "CERTIFIED_PHYSICAL_GLOBAL_L6OVER5_MOMENT",
        "Round35 rank moment",
    )
    require(
        rank["strict_nonpromotion"][
            "D1_rank_sum_dominates_complete_C_fw_C_rev"
        ]
        is False,
        "Round35 rank scope",
    )

    grouping = loaded[
        "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
    ]["result"]
    require(
        grouping["physical_Borel_whole_family_grouping"]["status"]
        == "CERTIFIED_PHYSICAL_BOREL_WHOLE_STANDARD_FAMILY_GROUPING_WITH_RECORDWISE_FINITE_J",
        "Round50 grouping",
    )
    require(
        grouping["D1_inverse_length_nonimplication"][
            "Round35_D1_implies_D_Z_moment"
        ]
        is False,
        "Round50 D1 nonimplication",
    )

    round36 = loaded[
        "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json"
    ]["result"]
    counter = round36["retained_depth_marginal_countermodel"]
    require(
        counter["exact_tail"] == "P(B>b)=4^-b for every integer b>=14",
        "Round36 rank tail",
    )
    require(
        counter["failure"]
        == "for every beta>0, E[N_recut,n^beta]=infinity once beta*n>=2",
        "Round36 product failure",
    )
    require(
        counter["claims_physical_rank_process_has_perfect_correlation"] is False,
        "Round36 logical scope",
    )

    inner = loaded[
        "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json"
    ]
    require(
        inner["verdict"]["core_local_standard_family_source_multiplier"]
        == "CERTIFIED",
        "inner-core finite-Z source restriction",
    )
    require(
        inner["replay_summary"]["source_multiplier_norm_upper"]
        == qstr(DENSITY_RATIO),
        "inner-core source multiplier",
    )
    return loaded


def all_mass_one_step_replay() -> dict[str, Any]:
    raw = DENSITY_RATIO * B0 * THETA + 2
    require(raw == Z1, "all-mass Z1 arithmetic")
    return {
        "operator": (
            "hat_F_(sigma) is the all-mass closed billiard image with the boundary "
            "of C_sigma added as an artificial singularity; sigma=fw uses C_s and "
            "sigma=rev uses I(C_s) by time-reversal conjugacy"
        ),
        "all_mass_not_survivor_operator": True,
        "one_step_derivation": "Z(hat_F_sigma G)<=((2000/1999)*49*(900337/901685)+2)*Z(G)",
        "density_ratio": qstr(DENSITY_RATIO),
        "artificial_cut_piece_bound": B0,
        "closed_one_step_expansion": qstr(THETA),
        "chopping_term": "2",
        "all_mass_one_step_Z_multiplier_Z1": qstr(raw),
        "positive_subfamily_rule": (
            "every retained or terminal subfamily obtained by deleting connected "
            "descendants has mass and Z no larger than the all-mass family"
        ),
        "scope": (
            "canonical finite-Z physical initial families in the frozen invariant "
            "density/curvature class, uniformly for every fixed |s|<=1/400"
        ),
        "status": "CERTIFIED_NUMERICAL_ALL_MASS_ONE_STEP_REPLAY",
    }


def residue_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for j in range(5):
        multiplier = Z1**j
        rows.append(
            {
                "residue_j": j,
                "bound": f"Z(F_(pL+{j}))<=Z1^{j}*z_p",
                "Z1_power": qstr(multiplier),
            }
        )
    return rows


def all_time_survivor_z_join() -> dict[str, Any]:
    rows = residue_rows()
    require(Z1 > 1, "Z1 direction")
    require(SURVIVAL < 1, "survival direction")
    return {
        "orientation_scope": "sigma in {fw,rev}, with C_fw=C_s and C_rev=I(C_s)",
        "typing_joins": {
            "physical_initial_family": (
                "F_(fw,0)=mu_s restricted to C_s with the frozen canonical finite-Z "
                "inner-core characteristic representation, dominated by the admissible "
                "base-cone source; F_(rev,0) is its I-conjugate"
            ),
            "physical_initial_family_evidence": (
                "Round41 controlled finite-Z/base-source input + the pinned inner-core "
                "strong source multiplier 2000/1999 + Round54 F_0=mu_s|C_s"
            ),
            "C_s_equals_C24_mod_frozen_faces": (
                "Round27 identifies C_s as the disjoint-mod-faces union of the same 24 "
                "physical cores and its candidate paths cover C24 modulo the singular null set"
            ),
            "killed_operator_to_Qn_IDs": (
                "the Round41/42 O_sigma deletion and the Round54 Q_n half-open prefix "
                "owners are the same every-collision complement restriction"
            ),
            "terminal_operator_to_Rn_IDs": (
                "the complementary descendants of the same all-mass hat_F step carry "
                "the Round54 R_(n+1) half-open terminal IDs"
            ),
            "reverse_core": (
                "the reverse proof is transported by I to I(C_s); the frozen cone is "
                "time-reversal invariant and I preserves collision-SRB mass, carrier "
                "arclength, pulled-back density ratios and hence Z; no literal equality "
                "I(C_s)=C_s is used"
            ),
            "status": "CERTIFIED_SAME_ID_OPERATOR_AND_INITIAL_FAMILY_JOIN",
        },
        "physical_state": (
            "F_(sigma,n)=the unnormalised exact same-ID survivor after avoiding "
            "C_sigma at every one of the first n collisions"
        ),
        "block_state": "z_(sigma,p)=Z(F_(sigma,pL)), L=9148*N_open",
        "pinned_weighted_block_result": (
            "there is an exact w_Z>1 for which sum_(p>=0)w_Z^p*z_(sigma,p)<infinity"
        ),
        "explicit_block_symbols": {
            "gamma": "(2000/1999)*(1+48*9148)*(900337/901685)^9148<1/2",
            "g": "gamma^N_open<1",
            "rho": "(111718729/111718750)^9148<1",
            "C_N": "Z0*(1-g)/(1-gamma)<=Z0/(1-gamma)",
        },
        "unweighted_block_resolvent": (
            "sum_(p>=0)z_p<=z_0/(1-g)+C_N*m_base/((1-g)*(1-rho))"
        ),
        "unweighted_block_consequence": "sum_(p>=0)z_(sigma,p)<infinity",
        "residue_bound": (
            "for n=pL+j with 0<=j<L, repeated all-mass/subfamily monotonicity gives "
            "Z(F_(sigma,n))<=Z1^j*z_(sigma,p)"
        ),
        "finite_residue_multiplier": (
            "A_L=sum_(j=0)^(L-1)Z1^j=(Z1^L-1)/(Z1-1)<infinity"
        ),
        "exact_all_time_bound": (
            "sum_(n>=0)Z(F_(sigma,n))<=A_L*sum_(p>=0)z_(sigma,p)<infinity"
        ),
        "N_open_materialized": False,
        "why_nonnumeric_is_still_finite": (
            "the frozen projective theorem supplies one finite uniform integer N_open; "
            "its absent numeral prevents a collision-time rate, not finite residue summation"
        ),
        "normalisation_used": False,
        "sample_residue_rows": rows,
        "sample_residue_rows_sha256": digest(rows),
        "status": "CERTIFIED_PHYSICAL_ALL_COLLISION_SURVIVOR_Z_L1_FINITE_NONNUMERIC_N_OPEN",
    }


def terminal_z_join() -> dict[str, Any]:
    return {
        "same_ID_terminal_levels": [
            "E_(fw,n+1)=1_C_s hat_F_fw(F_(fw,n)), IDs R_(n+1)",
            "E_(rev,n+1)=1_I(C_s) hat_F_rev(F_(rev,n)), IDs I(R_(n+1))",
        ],
        "first_level": "n=0 extracts R_1 and I(R_1)",
        "positive_subfamily_bound": (
            "Z(E_(sigma,n+1))<=Z(hat_F_sigma(F_(sigma,n)))<=Z1*Z(F_(sigma,n))"
        ),
        "pair_definition": (
            "Z_term,coarse,pair=sum_(n>=0)[Z(E_(fw,n+1))+Z(E_(rev,n+1))]"
        ),
        "pair_bound": (
            "Z_term,coarse,pair<=Z1*sum_(n>=0)[Z(F_(fw,n))+Z(F_(rev,n))]<infinity"
        ),
        "Phi_pair_used": False,
        "Round54_closed_step_face_recurrence_used": False,
        "route_relation": (
            "this bypasses the need to sum the Round54 C24-complement forcing "
            "Phi_pair for the coarse terminal conclusion; it does not prove that "
            "Phi_pair itself is summable"
        ),
        "physical_cell_refinement_included": False,
        "status": "CERTIFIED_TWO_ORIENTATION_COARSE_TERMINAL_Z_L1_FINITE_NONNUMERIC_N_OPEN",
    }


def gap_cutpoint_audit() -> dict[str, Any]:
    return {
        "source": ARXIV_SOURCE_AUDIT,
        "official_extension": (
            "on every gap V=(x,y), choose z and extend checkrho constantly from "
            "rho(x) on (x,z) and from rho(y) on (z,y), allowing a jump at z"
        ),
        "whole_gap_density_ratio_upper": "11/9",
        "registered_numeric_cone_ratio": qstr(DENSITY_RATIO),
        "strict_ratio_comparison": "11/9>2000/1999",
        "split_halves_density_debit": "zero on each open half separately",
        "fatal_length_issue": (
            "the rank-growth entry controls the whole image gap, not the two z-halves; "
            "the chosen z has no certified uniform distance from either endpoint, so one "
            "half can have arbitrarily small entry length and arbitrarily large boundary Z"
        ),
        "same_ID_canonical_chop_repairs_entry_length": False,
        "zero_density_debit_join": "REJECTED",
        "minimal_missing_new_input": (
            "either a uniform cutpoint-position/lower-length theorem or a one-jump paired-carrier Growth lemma"
        ),
        "stationary_only": True,
        "moving_sequence_Growth_claimed": False,
        "status": "CERTIFIED_STRICT_NONPROMOTION_AUDIT",
    }


def refinement_frontier() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for n in (1, 2, 3, 5, 8):
        rows.append(
            {
                "path_depth_n": n,
                "all_ranks_B_i": BASE_RANK,
                "additive_D1": f"{D1_FACTOR_AT_BASE_RANK}*{n}",
                "image_recut_product_model": f"{PATH_FACTOR_AT_BASE_RANK}^{n}",
                "claim_physical_path_has_constant_rank": False,
            }
        )
    return {
        "target": (
            "J_pair=integral sum_c p_c*(ell_fw,c^-1+ell_rev,c^-1) dlambda "
            "after the exact natural-short-cell/image-recut subdivision"
        ),
        "coarse_record_variables": (
            "for each terminal record j and orientation sigma, p_j and ell_(sigma,j) "
            "are its coarse mass and length, and N_(sigma,j) is the number of final cells"
        ),
        "density_oscillation_cell_bound": (
            "sum_(c subset j)p_c/ell_(sigma,c)<=(2000/1999)*N_(sigma,j)*p_j/ell_(sigma,j)"
        ),
        "missing_numerator": (
            "K_mult,pair=sum_(sigma,j)N_(sigma,j)*p_j/ell_(sigma,j)"
        ),
        "sufficient_join": (
            "K_mult,pair<infinity on the identical once-charged terminal law implies "
            "J_pair<=(2000/1999)*K_mult,pair<infinity"
        ),
        "recordwise_finite_subdivision": "CERTIFIED_BY_ROUND50",
        "global_integrability_of_K_mult_pair": "NOT_CERTIFIED",
        "why_current_rank_moment_does_not_close_it": (
            "the physical D1 channel is additive in sum_i 2^B_i, whereas image-recut "
            "multiplicity may contain a product comparable to 2^(sum_i B_i)"
        ),
        "pinned_sharp_nonimplication": (
            "Round36 has a perfectly-correlated logical rank law with the stronger "
            "one-time tail P(B>b)=4^-b and every fixed-depth D1 L^(6/5) moment, "
            "but no positive moment of the n-step recut product once beta*n>=2"
        ),
        "countermodel_asserted_physical": False,
        "constant_rank_growth_rows": rows,
        "constant_rank_growth_rows_sha256": digest(rows),
        "physical_J_pair": "NOT_CERTIFIED",
        "physical_I_D": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_MULTIPLICITY_WEIGHTED_REFINEMENT_FRONTIER",
    }


def strict_frontier() -> dict[str, Any]:
    return {
        "all_mass_hatF_one_step_Z1": "CERTIFIED_NUMERICAL_REPLAY",
        "physical_all_collision_survivor_Z_l1": (
            "CERTIFIED_FINITE_NONNUMERIC_N_OPEN"
        ),
        "two_orientation_coarse_terminal_Z_l1": (
            "CERTIFIED_FINITE_NONNUMERIC_N_OPEN"
        ),
        "Phi_pair_l1_needed_for_coarse_terminal_Z": (
            "BYPASSED_BY_HEREDITARY_EVERY_COLLISION_KILLED_GROWTH"
        ),
        "Phi_pair_l1_itself": "NOT_CERTIFIED",
        "official_gap_extension_zero_density_debit_join": "REJECTED",
        "terminal_cell_refinement_to_J_pair_same_ID_Z_join": "NOT_CERTIFIED",
        "multiplicity_weighted_terminal_K_mult_pair": "NOT_CERTIFIED",
        "physical_J_pair": "NOT_CERTIFIED",
        "physical_defect_moment_I_D": "NOT_CERTIFIED",
        "physical_common_refinement_J_cap_total": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "full_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
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
            "parameter_scope": "uniformly for every fixed |s|<=1/400",
            "depth_scope": "all collision times and all finite first-return levels",
            "claim_type": (
                "all-mass one-step Growth replay, killed-survivor residue summation, "
                "coarse terminal-Z extraction, gap-cutpoint no-go audit, and the exact "
                "multiplicity-weighted physical refinement frontier"
            ),
            "external_source_audit": ARXIV_SOURCE_AUDIT,
        },
        "all_mass_extra_cut_one_step_replay": all_mass_one_step_replay(),
        "all_time_killed_survivor_Z_join": all_time_survivor_z_join(),
        "two_orientation_coarse_terminal_Z_join": terminal_z_join(),
        "official_gap_cutpoint_density_audit": gap_cutpoint_audit(),
        "physical_cell_refinement_frontier": refinement_frontier(),
        "strict_nonpromotion": strict_frontier(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-manifest", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=(
            HERE
            / "cm2_gate34_round55_hereditary_terminal_z_refinement_frontier_verifier.py"
        ),
    )
    args = parser.parse_args()
    if args.print_manifest:
        print(json.dumps(build_manifest(args.verifier), indent=2, sort_keys=True))
        return 0
    if args.write_manifest is not None:
        manifest = build_manifest(args.verifier)
        args.write_manifest.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    frontier = result["strict_nonpromotion"]
    print("ALL_TIME_SURVIVOR_Z:", frontier["physical_all_collision_survivor_Z_l1"])
    print("COARSE_TERMINAL_Z:", frontier["two_orientation_coarse_terminal_Z_l1"])
    print("PHI_PAIR_ROUTE:", frontier["Phi_pair_l1_needed_for_coarse_terminal_Z"])
    print("REFINEMENT_TO_J_PAIR:", frontier["terminal_cell_refinement_to_J_pair_same_ID_Z_join"])
    print("GAP_DENSITY_SHORTCUT:", frontier["official_gap_extension_zero_density_debit_join"])
    print("GATE4:", frontier["Gate4"])
    print("CM2:", frontier["CM2"])
    return 2


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    raise SystemExit(main())
