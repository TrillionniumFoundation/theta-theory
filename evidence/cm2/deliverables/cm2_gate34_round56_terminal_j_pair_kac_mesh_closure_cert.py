#!/usr/bin/env python3
"""Round-56 Gate-4 terminal J_pair closure through a B_max Kac mesh.

This append-only certificate fills the three physical joins left open by
Round 55.  On each regular first-return path, the source rank-density mesh is
frozen at ``B_max=max_i B_inc(T^(i-1)x)``.  Its inverse scale is dominated by
the additive orbit charge, and the first-return Kac tower integrates that
charge against the physical collision-SRB law.

To keep the physical leaf type exact, the Round-35 slope-four collision-SRB
kernel is first used as the forward initial family.  A forward hereditary
replay produces exact tagged B subcurves; time reversal turns those very
curves into exact tagged I(B) reverse inputs; and a second hereditary replay
produces exact I(A) subcurves.  Applying time reversal once more gives a
once-charged finite-Z proof refinement of the exact Round-35 A leaves.  No
same-measure/transverse-redisintegration shortcut is used.

Common-refining that finite-Z family with the B_max grid has finite adapted
boundary Z: full grid cells are paid by the Kac charge and at most two
clipped cells per coarse parent are paid by the coarse terminal Z.  This is a
static re-expression of the same measure, so the hereditary Round-41/42
killed-Growth theorem can be replayed a third time on it.  Its forward
terminal images therefore also have finite Z.

Finally, the Round-55 global image-recut cap and density-ratio refinement
lemma control the common pullback refinement in both orientations.  This
proves physical adapted-metric J_pair<infinity and, through the exact
Round-53 bridge, physical I_D<infinity.  It does not prove J_cap, a physical
proper first-return kernel, later recovery clocks, q, the strong cemetery,
Gate 4, or CM2.
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
RESULT_SCHEMA = "cm2.gate34.round56-terminal-j-pair-kac-mesh-closure.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json"
)
DEFAULT_VERIFIER = (
    HERE / "cm2_gate34_round56_terminal_j_pair_kac_mesh_closure_verifier.py"
)

DEPENDENCIES = {
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
    "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json": (
        "a98203ebf820d959f9e04c213cd1d79c3809744671fd509c40e531bdc552c119"
    ),
    "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json": (
        "86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4"
    ),
    "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json": (
        "bb09f99519813ec49172f0bbbcc9015c1e0fcb2de07df7af734b81d2996a3f40"
    ),
    "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json": (
        "3a9fdd11c952fd8517a8fa068794c5737fee7265ee5532032af9605eae2feee3"
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
    "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json": (
        "2c6ab1c0b3b89000e6d96d04a60d7c662855ae1f24c1d9f43405df04732d7e58"
    ),
    "cm2-gate34-round55-hereditary-terminal-z-refinement-frontier-manifest-2026-07-20.json": (
        "275022bb78748941339bc27de022830346ebb220188d97b3bfa886af42049bfb"
    ),
    "cm2-gate34-round55-global-image-recut-cap-natural-mesh-frontier-manifest-2026-07-20.json": (
        "12270ccbdea2b3c6bf203529e94b31a298061d6b057ddc14757853763059e95e"
    ),
}

DENSITY_RATIO = Q(2000, 1999)
EUCLIDEAN_OVER_ADAPTED = Q(27, 5)
RANK_MOMENT_UPPER = Q(134217735, 64)
DELTA_TOWER_UPPER = 4 * RANK_MOMENT_UPPER
ADAPTED_FULL_CELL_UPPER = EUCLIDEAN_OVER_ADAPTED * DELTA_TOWER_UPPER
IMAGE_RECUT_COUNT_UPPER = 2397 * 10**90 + 1
IMAGE_REFINEMENT_MULTIPLIER = DENSITY_RATIO * IMAGE_RECUT_COUNT_UPPER
DEFECT_COEFFICIENT = Q(35, 99 * 2**309)
SAFE_BASE_LOG_OSC_UPPER = Q(648, 95 * 10**90)


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


def parse_json_text(text: str) -> Any:
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
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        value = parse_json_text(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency root: {name}")
        loaded[name] = value

    round27 = loaded[
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    ]["result"]["canonical_regular_connected_component_schema"]
    require(
        round27["R_n_and_Q_n_regular_component_partition_exists_mod_null"]
        is True,
        "Round27 return partition",
    )
    require(
        "homogeneity" in round27["regular_path_fibre_geometry"]
        and "core-avoidance" in round27["regular_path_fibre_geometry"],
        "Round27 regular path geometry",
    )
    require(
        round27["componentwise_forward_map_is_real_analytic_local_diffeomorphism"]
        is True
        and round27["componentwise_inverse_map_exists_on_regular_image"] is True,
        "Round27 branch diffeomorphism",
    )

    kac = loaded[
        "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json"
    ]["result"]
    baseline = kac["collision_srb_kac_baseline"]
    contract = kac["frozen_measure_space_contract"]
    require(
        contract["core_count"] == 24
        and contract["core_union"]
        == "C_s=union_of_24_frozen_compact_physical_cores",
        "Kac compact 24-core union",
    )
    require(
        baseline["first_return_level_sets_pairwise_disjoint_modulo_null"] is True,
        "Kac return levels",
    )
    require(
        baseline["nonreturning_normalized_mass"] == "0",
        "Kac recurrence",
    )
    require(
        contract["map_invertible_and_measure_preserving_modulo_singular_null_set"]
        == "standard_collision_map_theorem_on_the_frozen_fixed_configuration",
        "Kac invariance",
    )
    require(contract["ergodicity_used"] is False, "Kac no ergodicity")
    require(
        kac["measurable_induced_L1_baseline"]
        ["preserves_normalized_restriction_mu_C_s"]
        is True,
        "Kac induced invariance",
    )

    round41 = loaded[
        "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json"
    ]["result"]
    aggregate41 = round41["aggregate_canonical_Z_resolvent"]
    require(
        aggregate41["input"]
        == "a controlled canonical finite-Z physical initial family dominated as a positive measure by an admissible base-cone source",
        "Round41 replay input",
    )
    require(
        round41["unnormalized_killed_subfamily_Growth"]
        ["positive_subfamily_monotonicity"]
        == "for unnormalized weights, deleting descendants can only decrease mass and Z=sum_j p_j/|W_j|",
        "Round41 positivity",
    )

    round42 = loaded[
        "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
    ]["result"]
    growth42 = round42["numerical_C24_killed_Growth"]
    schedule42 = round42["explicit_short_curve_schedule"]
    require(
        growth42["hereditary_under_positive_C24_killing"] is True,
        "Round42 heredity",
    )
    require(
        schedule42["density_cone_ratio_at_delta_open_at_most"]
        == qstr(DENSITY_RATIO),
        "Round42 density ratio",
    )
    require(
        schedule42["delta_open_strictly_below_10^-90"] is True,
        "Round42 delta_open/source-recut order",
    )
    require(
        schedule42["metric_conversion"]
        == "length_E(W)<=(27/5)*length_*(W)",
        "Round42 metric conversion",
    )
    require(
        round42["aggregate_canonical_Z_resolvent"]
        ["block_index_weight_and_resolvent"]
        == "CERTIFIED_EXACT_SYMBOLIC",
        "Round42 resolvent",
    )

    maximal_manifest = loaded[
        "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json"
    ]
    require(
        maximal_manifest["dependencies"]
        ["cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"]
        == "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
        "maximal-word compact-core dependency",
    )
    maximal = maximal_manifest["result"]
    characteristic = maximal["positive_inner_core_characteristic_Z"]
    maximal_rows = maximal["seeded_implicit_maximal_component_registry"]["rows"]
    require(
        len(maximal_rows) == 24
        and all(
            "source/target central homogeneity abs(p)<3/10"
            in row["definition"]["component_predicate"]
            for row in maximal_rows
        ),
        "24 central non-grazing core predicates",
    )
    require(
        characteristic["registered_inner_core_rectangle_count"] == 24
        and characteristic[
            "finite_unnormalized_characteristic_Z_on_positive_inner_subfamily"
        ]
        is True
        and Q(characteristic["invariant_density_ratio_upper"])
        == DENSITY_RATIO,
        "inner-core finite-Z characteristic class",
    )

    inner = loaded[
        "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json"
    ]
    require(
        inner["verdict"]["core_local_standard_family_source_multiplier"]
        == "CERTIFIED",
        "inner-core source multiplier",
    )
    require(
        Q(inner["replay_summary"]["source_multiplier_norm_upper"])
        == DENSITY_RATIO,
        "inner-core source ratio",
    )

    carrier = loaded[
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    ]["result"]
    registry = carrier["arbitrary_Rn_parent_W_Borel_registry"]
    disintegration = carrier["collision_SRB_leaf_disintegration"]
    pair = carrier["common_forward_reverse_carrier_pair"]
    require(
        registry["incidence_rank_refinement"]
        == "one dyadic source/target cosine rank at every collision time",
        "Round35 path ranks",
    )
    require(
        registry["rank_density_mesh"]
        == "delta_B=2^-ceil(3(B+1)/2) in carrier arclength, followed by 1e-90 adapted recuts",
        "Round35 two-scale contract",
    )
    require(
        registry["canonical_leaf_equation"]
        == "phi(r)=4r+b; p(r)=sin(4r+b)"
        and registry["leaf_slope"] == "dphi/dr=4"
        and registry["inside_invariant_unstable_cone"] is True,
        "Round35 exact slope-four leaf type",
    )
    require(
        disintegration["conditional_density_wrt_dell"] == "cp/sqrt(17)"
        and disintegration["source_phase_graph_C2_seminorm"] == "0"
        and disintegration[
            "integrating_leaf_weights_recovers_mu_s_restricted_to_component"
        ]
        is True,
        "Round35 exact collision-SRB leaf kernel",
    )
    require(
        pair["forward_oriented_branch"] == "A -> B by H"
        and pair["reverse_oriented_branch"] == "I(B) -> I(A) by T_s^n",
        "Round35 orientation pair",
    )
    require(
        pair["forward_and_reverse_are_two_views_not_two_charges"] is True
        and pair["mu_s_A_equals_mu_s_B_equals_mu_s_I_B"] is True,
        "Round35 once charge",
    )

    rank = loaded[
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    ]["result"]["physical_collision_incidence_rank"]
    require(rank["chosen_q0"] == "3/2", "Round35 q0")
    require(
        Q(rank["global_collision_SRB_integral_2^(3B_inc/2)_strict_upper"])
        == RANK_MOMENT_UPPER,
        "Round35 rank moment",
    )
    require(
        rank["rank"]
        == "B_inc(x)=max(14,ceil(log2(1/cp(x))),ceil(log2(1/cp(T_s*x))))",
        "Round35 rank definition",
    )

    grouping = loaded[
        "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json"
    ]["result"]["physical_Borel_whole_family_grouping"]
    require(grouping["physical_full_registry_reconstructed"] is True, "Round50 law")
    require(
        "never two charges" in grouping["same_ID_two_view_join"],
        "Round50 once-charge join",
    )
    require(
        grouping["kernel_partition_identities_mod_null"]
        == [
            "sum_{k,j}K_fw(y,k,j;A)=K_par(y,A)",
            "sum_{k,j}K_rev(y,k,j;A)=K_par(y,A)",
        ],
        "Round50 partition identities",
    )

    round53 = loaded[
        "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json"
    ]["result"]["fractional_cell_Z_to_defect_moment"]
    require(
        round53["pair_boundary_numerator"]
        == "J_pair=integral sum_c p_c*(ell_fw,c^-1+ell_rev,c^-1) dlambda",
        "Round53 J_pair",
    )
    require(
        round53["direct_linear_tail_layer_cake_bound"]
        == "I_D<nu(X)+[35/(99*2^309)]*J_pair",
        "Round53 defect bridge",
    )

    terminal55 = loaded[
        "cm2-gate34-round55-hereditary-terminal-z-refinement-frontier-manifest-2026-07-20.json"
    ]["result"]
    terminal_join = terminal55["two_orientation_coarse_terminal_Z_join"]
    source_join = terminal55["all_time_killed_survivor_Z_join"]
    require(
        terminal_join["same_ID_terminal_levels"]
        == [
            "E_(fw,n+1)=1_C_s hat_F_fw(F_(fw,n)), IDs R_(n+1)",
            "E_(rev,n+1)=1_I(C_s) hat_F_rev(F_(rev,n)), IDs I(R_(n+1))",
        ],
        "Round55 terminal IDs",
    )
    require(
        terminal_join["status"]
        == "CERTIFIED_TWO_ORIENTATION_COARSE_TERMINAL_Z_L1_FINITE_NONNUMERIC_N_OPEN",
        "Round55 coarse terminal Z",
    )
    require(
        "preserves collision-SRB mass, carrier arclength, pulled-back density ratios and hence Z"
        in source_join["typing_joins"]["reverse_core"],
        "Round55 time reversal",
    )

    image55 = loaded[
        "cm2-gate34-round55-global-image-recut-cap-natural-mesh-frontier-manifest-2026-07-20.json"
    ]["result"]
    cap55 = image55["global_connected_image_recut_cap"]
    lemma55 = image55["density_ratio_refinement_lemma"]
    require(
        int(cap55["uniform_image_recut_count_upper"])
        == IMAGE_RECUT_COUNT_UPPER,
        "Round55 recut cap",
    )
    require(
        Q(lemma55["registered_density_ratio"]) == DENSITY_RATIO,
        "Round55 refinement ratio",
    )
    require(
        lemma55["refinement_inequality"]
        == "sum_j p_j/ell_j<=R*N*p/ell(W)",
        "Round55 refinement lemma",
    )
    return loaded


def mesh_exponent(B: int) -> int:
    require(isinstance(B, int) and B >= 14, "rank B")
    return (3 * (B + 1) + 1) // 2


def delta_inverse(B: int) -> int:
    return 1 << mesh_exponent(B)


def path_mesh_rows() -> list[dict[str, Any]]:
    paths = ([14], [14, 15], [20, 14, 17], [64, 65, 14], [100, 99, 100])
    rows: list[dict[str, Any]] = []
    for ranks in paths:
        b_max = max(ranks)
        inverse_max = delta_inverse(b_max)
        inverse_sum = sum(delta_inverse(B) for B in ranks)
        require(inverse_max <= inverse_sum, "path max/additive domination")
        for B in ranks:
            require(delta_inverse(B) ** 2 <= 16 * 2 ** (3 * B), "mesh square")
        rows.append(
            {
                "path_ranks": list(ranks),
                "B_max": b_max,
                "delta_Bmax_inverse": str(inverse_max),
                "sum_delta_Bi_inverse": str(inverse_sum),
                "max_is_one_path_term": True,
                "squared_rank_bound_each_i": "delta_Bi^-2<=16*2^(3B_i)",
            }
        )
    return rows


def tower_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in range(1, 6):
        rows.append(
            {
                "return_depth_n": n,
                "tower_levels": [f"T^{i}(R_{n})" for i in range(n)],
                "rank_indices": [f"B_{i + 1}=B_inc(T^{i}x)" for i in range(n)],
                "level_count": n,
                "last_level_before_return": f"T^{n - 1}(R_{n})",
            }
        )
    return rows


def path_max_kac_ledger() -> dict[str, Any]:
    rows = path_mesh_rows()
    towers = tower_rows()
    require(DELTA_TOWER_UPPER == Q(134217735, 16), "delta tower arithmetic")
    require(
        ADAPTED_FULL_CELL_UPPER == Q(724775769, 16),
        "adapted cell arithmetic",
    )
    return {
        "physical_rule": (
            "on one regular R_n incidence-rank path set B_max=max_(1<=i<=n)B_i "
            "and use one oriented half-open Euclidean carrier grid at "
            "delta_(B_max)=2^-ceil(3(B_max+1)/2)"
        ),
        "why_one_grid_is_admissible": (
            "B_max>=B_1, so this source grid refines the required source density-rank "
            "mesh; the remaining path ranks stay in the immutable regular branch code"
        ),
        "pathwise_domination": (
            "delta_(B_max)^-1<=sum_(i=1)^n delta_(B_i)^-1"
            "<=4*sum_(i=1)^n 2^(3B_i/2)"
        ),
        "mesh_arithmetic": "delta_B^-2<=16*2^(3B) for every integer B>=14",
        "sample_path_rows": rows,
        "sample_path_rows_sha256": digest(rows),
        "first_return_partition": "R_n=C_s intersect {tau_C_s^+=n}, n>=1",
        "tower_indexing": (
            "B_i(x)=B_inc(T_s^(i-1)x), 1<=i<=n; the occupied levels are i-1=0,...,n-1"
        ),
        "tower_disjointness_reason": (
            "if T^i x=T^j y for x in R_n,y in R_m and 0<=i<n,0<=j<m, "
            "invertibility would create an earlier C_s hit unless (n,i)=(m,j) mod null"
        ),
        "tower_sample_rows": towers,
        "tower_sample_rows_sha256": digest(towers),
        "occupation_identity": (
            "sum_(n>=1) integral_(R_n) sum_(i=1)^n f(T^(i-1)x)dmu_s"
            "=integral_(saturation(C_s)) f dmu_s"
        ),
        "ergodicity_used": False,
        "saturation_replaced_by_full_space_only_as_upper_bound": True,
        "rank_observable": "f(x)=2^(3B_inc(x)/2)>=0",
        "physical_rank_moment_strict_upper": qstr(RANK_MOMENT_UPPER),
        "physical_delta_charge_strict_upper": qstr(DELTA_TOWER_UPPER),
        "off_by_one_guard": "R_1 has exactly the level x itself and rank B_1=B_inc(x)",
        "status": "CERTIFIED_PHYSICAL_BMAX_MESH_AND_KAC_TOWER_L1_CHARGE",
    }


def paired_leafwise_reverse_replay() -> dict[str, Any]:
    require(SAFE_BASE_LOG_OSC_UPPER < Q(1, 2000), "safe base density ratio")
    return {
        "round35_kernel": (
            "Psi_s(b,r)=(r,phi=4r+b), p=sin(4r+b), with collision-SRB "
            "conditional density cp/sqrt(17) against slope-four arclength"
        ),
        "exact_leaf_type": (
            "phi(r)=4r+b, dphi/dr=4, inside the frozen invariant unstable cone, "
            "with source graph C2 seminorm zero"
        ),
        "safe_core_envelope_preparation": (
            "use finitely many half-open collision-chart envelopes covering only "
            "the 24 compact central-homogeneity cores; retain only slope-four "
            "parents whose closure stays in abs(p)<3/10 and meets C_s, then chop "
            "them by the fixed adapted delta_open grid"
        ),
        "core_nongrazing_bound": (
            "on every retained parent abs(p)<3/10, hence "
            "cp=sqrt(1-p^2)>sqrt(91)/10>19/20"
        ),
        "base_density_cone": (
            "along a slope-four parent abs(d_r log cp)=4*abs(p)/cp<24/19; "
            "ell_E<=(27/5)ell_* and delta_open<10^-90 make the density ratio "
            "strictly below 2000/1999"
        ),
        "base_log_density_oscillation_strict_upper": qstr(
            SAFE_BASE_LOG_OSC_UPPER
        ),
        "base_density_ratio_arithmetic": (
            "x=648/(95*10^90)<1/2000 and exp(x)<1/(1-x)<2000/1999"
        ),
        "safe_envelope_finite_Z_reason": (
            "there are finitely many bounded safe charts and b-ranges, the retained "
            "density is bounded above and below, and the fixed positive "
            "delta_open chop has finitely integrable full-cell and endpoint "
            "coarea boundary charge"
        ),
        "core_restriction": (
            "G_A0=1_(C_s)G_slope,safe; the certified 24-core characteristic "
            "multiplier has strong standard-family norm at most 2000/1999"
        ),
        "forward_initial_family": (
            "G_A0 is exactly mu_s|C_s without normalization, carried on positive "
            "subintervals of the Round35 slope-four leaves, and Z(G_A0)<infinity"
        ),
        "forward_killed_replay": (
            "apply the stationary C_s-killed Round41/42 hereditary Growth replay "
            "to G_A0 and retain the complementary first-return descendants"
        ),
        "forward_terminal_family": (
            "E_fw,total=disjoint_union_(n>=1)E_(fw,n), with the exact half-open "
            "R_n path tag retained on every proof atom"
        ),
        "forward_terminal_exact_inclusion": (
            "every forward terminal proof curve is B'=T_s^n(A') subset "
            "B=T_s^n(A), where A' is a subinterval of the exact Round35 "
            "slope-four A subset R_n leaf"
        ),
        "cuts_only_split": (
            "singularity, homogeneity, core-boundary and canonical Growth cuts only "
            "split analytic branch intervals; they never transversely redisintegrate"
        ),
        "forward_terminal_Z": "Z(E_fw,total)<infinity by the hereditary terminal residue sum",
        "induced_return_once_coverage": (
            "disjoint_union_(n>=1)E_(fw,n) represents "
            "(T_C_s)_#(mu_s|C_s)=mu_s|C_s exactly once, because the induced "
            "first-return map preserves normalized mu_C_s and the common scalar "
            "mu_s(C_s) is restored"
        ),
        "normalization_used": False,
        "reverse_start": (
            "G_IB=I_#E_fw,total is exactly mu_s|I(C_s), carried on the exact tagged "
            "I(B') subset I(B) curves, with Z(G_IB)=Z(E_fw,total)<infinity"
        ),
        "reverse_path_identity": (
            "for the tag B=T_s^n(A), T_s^k(I(B))=I(T_s^(n-k)(A)) for 0<=k<=n"
        ),
        "reverse_first_return": (
            "the R_n no-intermediate-C_s tag and the reverse path identity imply "
            "that I(B) first returns to I(C_s) at exactly n, at I(A)"
        ),
        "reverse_killed_replay": (
            "apply the stationary I(C_s)-killed Round41/42 hereditary Growth replay "
            "to G_IB, preserving the same n and regular-path tag"
        ),
        "reverse_terminal_exact_inclusion": (
            "every paired reverse terminal proof curve is I(A'') subset I(A) on "
            "the exact reverse branch I(B)->I(A), and the total terminal Z is finite"
        ),
        "source_recovery": (
            "G_src,coarse=I_#E_rev,paired,total; every proof carrier A'' is a "
            "subinterval of the exact Round35 slope-four A leaf"
        ),
        "source_measure_and_Z": (
            "G_src,coarse represents mu_s|C_s exactly once and "
            "Z_src,coarse=Z(E_rev,paired,total)<infinity"
        ),
        "no_same_measure_shortcut": True,
        "no_full_grazing_parent": True,
        "no_circularity": (
            "the paired construction uses only the finite-Z slope-four base, the "
            "hereditary terminal theorem, time reversal and induced invariance; "
            "the later B_max/source-short ledger is not used to establish it"
        ),
        "status": (
            "CERTIFIED_EXACT_ROUND35_SLOPE4_SOURCE_LEAF_REFINEMENT_BY_"
            "PAIRED_REVERSE_REPLAY"
        ),
    }


def metric_and_once_charge_ledger() -> dict[str, Any]:
    return {
        "source_return_atom": "A subset R_n on one regular rank-path branch",
        "target_return_atom": "B=T_s^n(A) subset C_s",
        "forward_view": "A -> B",
        "reverse_view": "I(B) -> I(A)",
        "coarse_terminal_outputs": {
            "forward": "exact tagged B subcurves from the paired forward replay",
            "reverse": "exact tagged I(A) subcurves from the paired reverse replay",
        },
        "source_recovery_from_reverse_terminal": (
            "apply I once to the paired reverse terminal output I(A'') subset I(A); "
            "this gives A'' subset A, not a second copy of A"
        ),
        "coarse_source_family": (
            "G_src,coarse=I_#E_rev,paired,total; its carriers refine the exact "
            "Round35 slope-four A leaves and represent mu_s|C_s exactly once"
        ),
        "coarse_source_Z": (
            "Z_src,coarse=Z(E_rev,paired,total)<infinity by the paired reverse "
            "hereditary terminal replay"
        ),
        "charge_policy": (
            "A owns one mass p; fw and rev contribute two length terms to J_pair "
            "but never two physical masses"
        ),
        "proof_refinement_policy": (
            "canonical Growth chops are retained as a proof-only subcode; projection "
            "forgets that subcode and reconstructs each Round35 physical cell once"
        ),
        "positive_coarsening_lemma": (
            "if a physical interval cell is a union of proof cells, p/ell is their "
            "length-weighted average and is at most the sum of their p_j/ell_j"
        ),
        "length_functionals": {
            "ell_fw_c": "adapted carrier length ell_*(A_c)",
            "ell_rev_c": "adapted carrier length ell_*(I(B_c))=ell_*(B_c)",
            "natural_delta_metric": "Euclidean carrier arclength ell_E on A",
            "image_recut_metric": "adapted carrier arclength ell_* on B",
        },
        "metric_conversion": (
            "ell_E<=27/5*ell_*, equivalently ell_*>=5/27*ell_E; "
            "27/5 is paid only for full Euclidean grid cells"
        ),
        "time_reversal_metric_rule": (
            "I preserves collision-SRB mass, Euclidean/adapted carrier arclength, "
            "density ratios and Z"
        ),
        "same_ID_final_cell": (
            "Round35 common restriction ID=(component/source-parent-W/natural-short-cell-k/"
            "image-recut-rank), with the proof-only canonical chop code forgotten"
        ),
        "status": "CERTIFIED_ADAPTED_METRIC_AND_ONCE_CHARGED_TERMINAL_SOURCE_JOIN",
    }


def finite_source_natural_z() -> dict[str, Any]:
    return {
        "coarse_parent": (
            "one I-pulled reverse terminal canonical atom A of mass p, adapted length "
            "ell_*(A), invariant density ratio at most 2000/1999, and one fixed B_max"
        ),
        "proof_only_prechop": (
            "first intersect every coarse A with an oriented adapted delta_open grid; "
            "delta_open is one fixed positive symbolic scale and delta_open<10^-90"
        ),
        "proof_only_prechop_bound": (
            "Z_src,pre,*<=mu_s(C_s)/delta_open+(4000/1999)*Z_src,coarse<infinity"
        ),
        "rank_grid_convention": (
            "intersect each proof-only prechop parent with one oriented half-open "
            "Euclidean delta_(B_max) grid; there are full cells plus at most two "
            "clipped endpoint cells"
        ),
        "full_cell_bound": (
            "sum_full p_j/ell_*(A_j)<=(27/5)*p/delta_(B_max)"
        ),
        "full_cell_metric_reason": (
            "every full cell has ell_E=delta_(B_max) and ell_*>=5/27*ell_E"
        ),
        "clipped_endpoint_bound": (
            "sum_at_most_two_endpoints p_j/ell_*(A_j)"
            "<=(4000/1999)*p/ell_*(A)"
        ),
        "endpoint_density_reason": (
            "restriction preserves the parent density ratio, so each child average "
            "density is at most (2000/1999) times the parent average"
        ),
        "rank_grid_global_bound": (
            "Z_src,rank,*<724775769/16+(4000/1999)*Z_src,pre,*<infinity"
        ),
        "numeric_Kac_full_cell_strict_upper": qstr(ADAPTED_FULL_CELL_UPPER),
        "coarse_source_Z_finite": True,
        "exact_source_short_recut": (
            "common-refine with the frozen adapted 10^-90 source grid carried by "
            "Round35/50 natural-short-cell-k"
        ),
        "source_short_two_cell_reason": (
            "every rank-grid proof cell lies in one adapted delta_open prechop parent, "
            "and delta_open<10^-90, so it meets at most two half-open 10^-90 cells"
        ),
        "source_short_refinement_bound": (
            "Z_src,short,*<=(4000/1999)*Z_src,rank,*<infinity"
        ),
        "static_not_moving": True,
        "same_physical_measure": (
            "G_src,short represents mu_s|C_s with no normalization and projects "
            "exactly to the Round35/50 source natural-short-cell law"
        ),
        "controlled_initial_family_checks": [
            "positive interval restrictions of canonical unstable parents",
            "same invariant unstable cone and curvature class",
            "same density-ratio cone on every proof cell",
            "finite total adapted boundary Z by the displayed bound",
            "dominated as the same positive measure by the admissible mu_s|C_s base source",
        ],
        "status": "CERTIFIED_PHYSICAL_FINITE_ADAPTED_Z_EXACT_SOURCE_SHORT_REFINEMENT",
    }


def hereditary_replay_and_final_join() -> dict[str, Any]:
    require(IMAGE_RECUT_COUNT_UPPER > 1, "image cap positivity")
    return {
        "replay_input": (
            "G_src,short, the static finite-Z canonical proof refinement of the exact "
            "Round35/50 source-short law on the same mu_s|C_s first-return IDs"
        ),
        "replay_scope": (
            "for each fixed |s|<=1/400 under the stationary T_s every-collision "
            "C24-killed operator; no arbitrary moving sequence"
        ),
        "mass_tail_unchanged": (
            "the refinement changes only the representation, so survivor masses are "
            "the same mu_s(Q_n) used by the hereditary resolvent"
        ),
        "hereditary_output": (
            "Z_img,short,*=sum_(n>=1)Z of the forward terminal descendants of "
            "G_src,short is finite"
        ),
        "physical_image_relation": (
            "the proof terminal descendants refine the physical B=T_s^n(A) natural "
            "images; positive coarsening gives Z_image,physical,short<=Z_img,short,*"
        ),
        "image_recut_count_upper": str(IMAGE_RECUT_COUNT_UPPER),
        "image_recut_density_ratio": qstr(DENSITY_RATIO),
        "image_refinement_multiplier": qstr(IMAGE_REFINEMENT_MULTIPLIER),
        "source_view_after_pullback_recut": (
            "each connected B parent has at most N_img adapted recut cells; their "
            "pullbacks split its A parent into the same number, so the Round55 "
            "R*N lemma applies to the source adapted length"
        ),
        "target_view_common_refinement": (
            "common-refine the physical image recut with the proof terminal chops; "
            "each proof parent sees at most N_img recut cells and physical cells are "
            "coarsenings of the proof cells"
        ),
        "paired_bound": (
            "J_pair,*<=((2000/1999)*(2397*10^90+1))*"
            "(Z_src,short,*+Z_img,short,*)<infinity"
        ),
        "same_ID_once_charge": True,
        "physical_J_pair_metric": "adapted carrier arclength in both views",
        "physical_J_pair": "CERTIFIED_FINITE",
        "status": "CERTIFIED_PHYSICAL_TERMINAL_REFINEMENT_TO_J_PAIR",
    }


def defect_join() -> dict[str, Any]:
    return {
        "tail_event": (
            "T_m=nu{ceil(log2(1/min(ell_fw,ell_rev)))_+>m}<2^-m*J_pair"
        ),
        "exact_bridge": "I_D<nu(X)+[35/(99*2^309)]*J_pair",
        "coefficient": qstr(DEFECT_COEFFICIENT),
        "same_measure": True,
        "physical_I_D": "CERTIFIED_FINITE",
        "status": "CERTIFIED_PHYSICAL_DEFECT_EXPONENTIAL_MOMENT_FROM_J_PAIR",
    }


def strict_frontier() -> dict[str, Any]:
    return {
        "natural_mesh_path_rule": "CERTIFIED_BMAX",
        "natural_mesh_Kac_tower_charge": "CERTIFIED_PHYSICAL_L1",
        "exact_round35_slope4_source_leaf_inclusion": (
            "CERTIFIED_BY_PAIRED_REVERSE_REPLAY"
        ),
        "natural_mesh_metric_alignment": "CERTIFIED_ADAPTED_TWO_VIEW_LEDGER",
        "natural_mesh_same_ID_terminal_join": "CERTIFIED_ONCE_CHARGED_WITH_PROOF_REFINEMENT",
        "finite_static_source_natural_Z": "CERTIFIED",
        "hereditary_terminal_replay_on_refined_source": "CERTIFIED",
        "global_connected_image_recut_count_cap": "CERTIFIED_PINNED_ROUND55",
        "terminal_cell_refinement_to_J_pair": "CERTIFIED",
        "physical_J_pair": "CERTIFIED_FINITE",
        "physical_defect_moment_I_D": "CERTIFIED_FINITE",
        "physical_common_refinement_J_cap_total": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_after_properisation": "NOT_CERTIFIED",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
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
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "return_scope": "the full collision-SRB first-return partition modulo the frozen null cemetery",
            "claim_type": (
                "B_max natural mesh, first-return Kac occupation charge, adapted metric/"
                "same-ID terminal-source join, hereditary finite-Z replay, physical "
                "J_pair closure and the exact I_D consequence"
            ),
            "external_source_promoted": False,
        },
        "path_max_mesh_and_Kac_tower": path_max_kac_ledger(),
        "paired_leafwise_reverse_replay": paired_leafwise_reverse_replay(),
        "metric_and_once_charge_terminal_source_join": metric_and_once_charge_ledger(),
        "finite_static_source_natural_Z": finite_source_natural_z(),
        "hereditary_replay_and_image_recut_join": hereditary_replay_and_final_join(),
        "physical_defect_moment_join": defect_join(),
        "strict_nonpromotion": strict_frontier(),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path = DEFAULT_VERIFIER) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file(), "verifier missing")
    require(not verifier.is_symlink(), "verifier symlink")
    require(verifier.parent == HERE, "verifier outside deliverables")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "dependencies": dict(DEPENDENCIES),
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
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.manifest_json:
        print(pretty_manifest(args.verifier), end="")
        return 0
    if args.write_manifest is not None:
        args.write_manifest.write_text(
            pretty_manifest(args.verifier), encoding="utf-8"
        )
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    strict = result["strict_nonpromotion"]
    print("NATURAL_MESH_KAC:", strict["natural_mesh_Kac_tower_charge"])
    print("PHYSICAL_J_PAIR:", strict["physical_J_pair"])
    print("PHYSICAL_I_D:", strict["physical_defect_moment_I_D"])
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    raise SystemExit(main())
