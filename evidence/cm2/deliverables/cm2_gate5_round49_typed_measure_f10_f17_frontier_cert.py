#!/usr/bin/env python3
"""Round-49 typed-measure F10/F17 frontier.

This append-only layer performs the measure-type join left open in Round 48.
For every fixed regular finite-depth record one may put the collision-SRB
volume, occurrence coarea currents, core traces and the seven face-current
types under one *dominating* measure.  This type-checks a recordwise direct
sum, but it does not make the singular face measures absolutely continuous
with respect to the collision-SRB D1 charge.

Two exact countermodels are frozen:

* finite one-step coarea L^(3/2) rank moments do not imply a return-depth
  weighted face-tower moment; and
* the existing exponential return tail plus the D1 rank-sum moment does not
  control a multiplicative suffix derivative.

Finally, a conditional boundary-Z_B route is recorded.  No complete F10 or
F17 field is promoted and Gate-5 maturity remains 10/18.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round49-typed-measure-f10-f17-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round49-typed-measure-f10-f17-frontier-manifest-2026-07-19.json"
)

DEPENDENCIES = {
    "cm2-gate5-round48-seven-boundary-f10-seed-frontier-manifest-2026-07-19.json": (
        "d2eb549656098abfc3fd57ae3eb5796e4ec3d57ebf579b21497ee3721ee3116c"
    ),
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json": (
        "19ad840a8cfbca2aa722cfd367d287fe36de67b9c7b6faf00a151ca2f2bf8a16"
    ),
    "cm2-gate5-round47-regular-c1dual-f13-manifest-2026-07-19.json": (
        "3415f8533865e9ed907df823c1453ee981f3f1f1d5e04333fc14a90ddb2884d0"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json": (
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e"
    ),
    "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json": (
        "68f0ee7595688ef4ea1ab5eb1e101ab8c2ccd327d3bcf40876ccbd40a5d9bfab"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
}

BASE_RANK = 14
D1_COEFFICIENT = 151
DERIVATIVE_COEFFICIENT = 150
SURVIVAL_R = Q(111718729, 111718750)
MIN_SUFFIX_FACTOR = DERIVATIVE_COEFFICIENT * (1 << BASE_RANK)

POSITIVE_COAREA_MASS = Q(8064, 5)
RAW_RANK_L3OVER2 = Q(46506443753721, 13750)
REVERSE_F10_L3OVER2 = Q(2278815743932329, 550)
FORWARD_F10_L3OVER2 = Q(107522897958602952, 6875)
BIDIRECTIONAL_F10_L3OVER2 = REVERSE_F10_L3OVER2 + FORWARD_F10_L3OVER2

F13_OVER_D1 = Q(3816937, 47112000)
X_OVER_D1 = Q(25, 151)
FULL_SOURCE_OVER_D1 = F13_OVER_D1 + X_OVER_D1

DENSITY_RATIO = Q(2000, 1999)
F8_INVERSE = Q(5)
TRACE_Z_MULTIPLIER = DENSITY_RATIO * F8_INVERSE
TANGENCY_C1 = Q(516607461656000000, 47978559724753)
BOUNDARY_FIXED_COST = 52 * TANGENCY_C1 + 121 * 40
CORE_FIXED_COST = 192 * 55
TRACE_Z_FIXED_COEFFICIENT = TRACE_Z_MULTIPLIER * (
    BOUNDARY_FIXED_COST + CORE_FIXED_COST
)
TRACE_Z_RANK_COEFFICIENT = TRACE_Z_MULTIPLIER * 103


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=strict_object
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependencies() -> None:
    round48 = load(
        "cm2-gate5-round48-seven-boundary-f10-seed-frontier-manifest-2026-07-19.json"
    )["result"]
    if round48["conditional_all_face_charge_ledger"]["formal_all_face_ratio"] != (
        "13571096530812446357/14837273637760415744"
    ):
        raise RuntimeError("Round48 formal ratio")
    if round48["strict_nonpromotion"]["same_measure_arbitrary_Rn_F10_join"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("Round48 measure scope")
    if round48["strict_nonpromotion"]["Gate5_maturity"] != "10/18":
        raise RuntimeError("Round48 maturity")
    if round48["cross_colour_tangency_F10_base_seed"][
        "C1_cost_exact_strict_upper"
    ] != qstr(TANGENCY_C1):
        raise RuntimeError("tangency cost")

    round39 = load(
        "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json"
    )["result"]
    rank = round39["physical_rank_L3over2_derivation"]
    install = round39["moving_occurrence_seed_F10_L3over2_installation"]
    if rank["positive_coarea_total_mass_upper"] != qstr(POSITIVE_COAREA_MASS):
        raise RuntimeError("coarea mass")
    if rank["integral_2^(3B/2)_dm_strict_upper"] != qstr(RAW_RANK_L3OVER2):
        raise RuntimeError("rank moment")
    if install["reverse_integral_raw_F10^(3/2)_strict_upper"] != qstr(
        REVERSE_F10_L3OVER2
    ):
        raise RuntimeError("reverse F10 moment")
    if install["forward_integral_raw_F10^(3/2)_strict_upper"] != qstr(
        FORWARD_F10_L3OVER2
    ):
        raise RuntimeError("forward F10 moment")

    round47 = load(
        "cm2-gate5-round47-regular-c1dual-f13-manifest-2026-07-19.json"
    )["result"]
    guard = round47["bulk_current_and_Piola_nonpromotion_guard"]
    if "11616937/47112000" not in guard["source_time_C1dual_bound"]:
        raise RuntimeError("source current ratio")
    if round47["finite_regular_path_two_trace_C1dual_F13_sublayer"][
        "C1_dual_embedding_multiplier"
    ] != "1":
        raise RuntimeError("two trace multiplier")

    d1 = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]
    charge = d1["arbitrary_Rn_additive_rank_sum_charge"]
    if charge["pointwise_density"] != "c_D1,n(x)=151*sum_{i=1}^n 2^B_i(x)":
        raise RuntimeError("D1 density")
    if d1["physical_rank_sum_weighted_tail"]["block_exponent"] != "1/6":
        raise RuntimeError("D1 block exponent")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    if carrier["arbitrary_Rn_parent_W_Borel_registry"]["registry_type"] != (
        "standard-Borel parameterized actual curve registry"
    ):
        raise RuntimeError("carrier Borel registry")
    if carrier["collision_SRB_leaf_disintegration"][
        "integrating_leaf_weights_recovers_mu_s_restricted_to_component"
    ] is not True:
        raise RuntimeError("collision disintegration")

    f8 = load(
        "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
    )["result"]
    if f8["same_ID_numeric_F8"][
        "common_normalized_transversality_strict_lower"
    ] != "1/5":
        raise RuntimeError("F8 transversality")
    if f8["parameterized_connected_face_registry"][
        "each_parent_W_face_family_intersection_count"
    ] != "0_or_1":
        raise RuntimeError("face intersection count")

    borel = load(
        "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json"
    )["result"]
    if borel["fixed_s_Borel_parent_survivor_kernel"]["status"] != (
        "CERTIFIED_FIXED_S_BOREL_PARENT_SURVIVOR_SUBKERNEL_SCHEMA"
    ):
        raise RuntimeError("fixed-s Borel kernel")

    cone = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )
    if cone["replay_summary"]["density_ratio"] != qstr(DENSITY_RATIO):
        raise RuntimeError("density ratio")


def fixed_record_typed_kernel() -> dict[str, Any]:
    return {
        "parameter_scope": "base parameter s=0",
        "depth_scope": "each fixed finite n and each fixed regular arbitrary-R_n restriction record",
        "common_record_token": (
            "(component-id,n,path-key,parent-W-id,time-j,face-kind,primitive-key,connected-rank-0,trace-side)"
        ),
        "collision_volume_kernel": (
            "K_mu(y,A)=mu_0(A intersect R_y), carrying c_D1,n=151*sum_i 2^B_i"
        ),
        "occurrence_coarea_kernel": (
            "K_occ(y,e,A)=Z_N^-1*integral 1_(A intersect R_y)(iota_e(theta))*w_e(theta)dtheta"
        ),
        "core_trace_kernel": (
            "K_core(y,c,A)=the Round47 finite signed two-trace measure restricted to R_y"
        ),
        "seven_face_germ_kernel": (
            "K_7(y,f,A)=the Round48 regular noncorner face-current measure restricted to one registered germ"
        ),
        "typed_vector_kernel": "K=(K_mu,K_occ,K_core,K_7)",
        "recordwise_dominating_measure": (
            "Lambda_y=K_mu+sum_e |K_occ|+sum_c |K_core|+sum_f |K_7|"
        ),
        "recordwise_Radon_Nikodym_typing": True,
        "normalization_note": (
            "the common Z_N^-1 factor can be installed on every physical collision current but does not alter Lebesgue type"
        ),
        "materialized_unconditional_layers": [
            "collision-SRB parent/restriction kernel",
            "64 occurrence seeds and their 128 oriented traces",
            "finite-regular-path two-trace/core sublayer",
        ],
        "seven_face_extension_scope": (
            "conditional on an individually registered nonempty regular germ; Round48 freezes seed types and candidate slots, not a global nonempty-component enumeration"
        ),
        "global_all_record_face_owner_deduplication": "NOT_CERTIFIED",
        "global_sigma_finite_kernel_joint_measurability": "NOT_CERTIFIED",
        "physical_D1_domination_from_master_measure": False,
        "status": "CERTIFIED_TYPED_FIXED_RECORD_DIRECT_SUM_ONLY",
    }


def lebesgue_decomposition_guard() -> dict[str, Any]:
    rows = []
    for exponent in (4, 8, 12, 16, 20):
        epsilon = Q(1, 1 << exponent)
        rows.append(
            {
                "epsilon": qstr(epsilon),
                "volume_of_tube": qstr(2 * epsilon),
                "face_measure_of_tube": "1",
                "face_to_volume_ratio": qstr(1 / (2 * epsilon)),
            }
        )
    return {
        "physical_types": {
            "D1": "two-dimensional collision-SRB density c_D1,n*dmu_s",
            "occurrence": "one-dimensional positive coarea curve measure",
            "core_and_two_trace": "one-dimensional finite signed boundary measures",
            "seven_face_seed": "density relative to a regular one-dimensional face measure",
        },
        "regular_face_zero_volume": "mu_s(Gamma)=0 for every smooth regular collision face Gamma",
        "nonzero_face_current": (
            "the selected moving-occurrence coarea density is positive on every nonempty regular selected germ"
        ),
        "Lambda_D1_density_on_face_sector": "d(c_D1*mu_s)/dLambda=0",
        "finite_constant_D1_domination_of_nonzero_face_current": False,
        "local_countermodel": {
            "space": "[0,1]^2",
            "volume": "mu=dx*dy",
            "face": "Gamma={x=1/2}",
            "face_measure": "nu=H^1 restricted to Gamma",
            "tube": "A_epsilon={abs(x-1/2)<epsilon}",
            "values": "nu(A_epsilon)=1 while mu(A_epsilon)=2*epsilon",
            "representative_exact_rows": rows,
            "rows_sha256": digest(rows),
        },
        "common_normalization_repairs_singularity": False,
        "Round48_formal_subunit_ratio_becomes_physical_theorem": False,
        "status": "CERTIFIED_LEBESGUE_DECOMPOSITION_OBSTRUCTION",
    }


def return_depth_countermodel() -> dict[str, Any]:
    rows = []
    for cutoff in (4, 16, 64):
        total_mass = sum((Q(1, n * (n + 1)) for n in range(1, cutoff + 1)), Q())
        weighted = sum((Q(1, n + 1) for n in range(1, cutoff + 1)), Q())
        rows.append(
            {
                "cutoff": cutoff,
                "partial_mass": qstr(total_mass),
                "partial_depth_weighted_mass": qstr(weighted),
            }
        )
    assert BIDIRECTIONAL_F10_L3OVER2 == Q(272016189515514129, 13750)
    return {
        "certified_one_step_inputs": {
            "positive_coarea_mass_upper": qstr(POSITIVE_COAREA_MASS),
            "raw_rank_L3over2_upper": qstr(RAW_RANK_L3OVER2),
            "bidirectional_raw_F10_L3over2_upper": qstr(
                BIDIRECTIONAL_F10_L3OVER2
            ),
        },
        "countermodel": {
            "return_level_face_mass": "b_n=1/(n*(n+1))",
            "total_face_mass": "sum_n b_n=1",
            "rank": "B=14 identically",
            "raw_rank_L3over2_moment": str(1 << 21),
            "depth_weighted_mass": "sum_n n*b_n=sum_n 1/(n+1)=infinity",
            "representative_partial_sums": rows,
            "rows_sha256": digest(rows),
        },
        "logical_conclusion": (
            "finite raw coarea mass and even a bounded rank do not imply return-depth weighted face-current integrability"
        ),
        "collision_SRB_Kac_formula_applies_to_singular_face_measure": False,
        "required_new_input": (
            "a face-tower moment or a same-ID trace/boundary-Z_B theorem with summable insertion-time aggregate resolvent"
        ),
        "return_depth_weighted_coarea_integrability": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_RETURN_DEPTH_NONIMPLICATION",
    }


def f17_suffix_product_guard() -> dict[str, Any]:
    product_ratio = MIN_SUFFIX_FACTOR * SURVIVAL_R
    assert MIN_SUFFIX_FACTOR == 2457600
    assert product_ratio == Q(5491198967808, 2234375)
    assert product_ratio > 1
    assert FULL_SOURCE_OVER_D1 == Q(11616937, 47112000)
    assert Q(1, 4) - FULL_SOURCE_OVER_D1 == Q(161063, 47112000)
    quarter_threshold = (Q(1, 4) - F13_OVER_D1) / X_OVER_D1
    unit_threshold = (1 - F13_OVER_D1) / X_OVER_D1
    assert quarter_threshold == Q(7961063, 7800000)
    assert unit_threshold == Q(43295063, 7800000)
    return {
        "source_time_current": {
            "X_over_D1": qstr(X_OVER_D1),
            "F13_over_D1": qstr(F13_OVER_D1),
            "full_source_over_D1": qstr(FULL_SOURCE_OVER_D1),
            "strict_quarter_slack": qstr(Q(1, 4) - FULL_SOURCE_OVER_D1),
        },
        "crude_suffix": {
            "minimum_one_step_derivative_factor": MIN_SUFFIX_FACTOR,
            "survival_rate_r": qstr(SURVIVAL_R),
            "minimum_factor_times_r": qstr(product_ratio),
            "minimum_factor_times_r_exceeds_one": True,
        },
        "geometric_countermodel": {
            "return_law": "P(N=n)=(1-r)*r^(n-1), n>=1",
            "one_minus_r": qstr(1 - SURVIVAL_R),
            "ranks": "B_i=14 for all i",
            "D1_charge": "151*2^14*N, hence every polynomial D1 moment is finite",
            "first_insertion_suffix_multiplier": "2457600^(N-1)",
            "suffix_expectation_series_ratio": qstr(product_ratio),
            "suffix_product_moment": "infinite",
            "works_already_at_best_case_N_open": 1,
        },
        "logical_conclusion": (
            "the certified D1 L6/5 moment and exponential return tail do not imply a joint insertion/suffix product moment"
        ),
        "future_dynamic_test_thresholds": {
            "if_multiplier_Cdyn_keeps_total_below_one_quarter": (
                "C_dyn<7961063/7800000"
            ),
            "if_multiplier_Cdyn_keeps_total_below_one": (
                "C_dyn<43295063/7800000"
            ),
            "unit_multiplier_would_preserve_source_quarter_bound": True,
        },
        "F17_dynamic_test_multiplier": "NOT_CERTIFIED",
        "joint_insertion_suffix_rank_tail": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_SUFFIX_PRODUCT_NONIMPLICATION",
    }


def conditional_boundary_z_route() -> dict[str, Any]:
    assert TRACE_Z_MULTIPLIER == Q(10000, 1999)
    assert BOUNDARY_FIXED_COST == Q(
        27095804235179804520, 47978559724753
    )
    assert TRACE_Z_FIXED_COEFFICIENT == Q(
        276024578258731962000000, 95909140889781247
    )
    assert TRACE_Z_RANK_COEFFICIENT == Q(1030000, 1999)
    return {
        "conditional_hypotheses": [
            "one registered regular face intersects each canonical parent W at most once",
            "conditional leaf density ratio is at most 2000/1999",
            "the normalized F8 wedge is strictly above 1/5",
            "face ownership and one-sided trace multiplicity are deduplicated on the same restriction ID",
        ],
        "single_intersection_TV_bridge": (
            "face atom amplitude <=(10000/1999)*A_face/length(W)"
        ),
        "plain_boundary_Z": "Z(G)=integral length(W)^(-1)dlam(W)",
        "rank_weighted_boundary_ZB": (
            "Z_B(G)=integral 2^B(W intersect Gamma)*length(W)^(-1)dlam(W)"
        ),
        "trace_multiplier": qstr(TRACE_Z_MULTIPLIER),
        "fixed_cost_inputs": {
            "seven_boundary_W_worst_cost": qstr(BOUNDARY_FIXED_COST),
            "C24_core_cost": str(CORE_FIXED_COST),
        },
        "conditional_fixed_Z_coefficient": qstr(TRACE_Z_FIXED_COEFFICIENT),
        "conditional_occurrence_ZB_coefficient": qstr(
            TRACE_Z_RANK_COEFFICIENT
        ),
        "conditional_target": (
            "Q_F10(G)<=(276024578258731962000000/95909140889781247)*Z(G)+(1030000/1999)*Z_B(G)"
        ),
        "scope_warning": (
            "this is an atom/TV trace lemma, not the missing full C1 density theorem; leaf log-density derivatives and owner/cemetery labels still have to be joined"
        ),
        "same_ID_ZB_trace_theorem": "NOT_CERTIFIED",
        "insertion_time_aggregate_ZB_resolvent": "NOT_CERTIFIED",
        "return_depth_integrability_from_this_route": "NOT_CERTIFIED",
        "status": "CERTIFIED_CONDITIONAL_ALTERNATIVE_ROUTE_ONLY",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "base parameter s=0",
            "depth_scope": "every fixed finite regular arbitrary-R_n record, followed by an audit of the unbounded return-depth sum",
            "claim_type": (
                "typed recordwise measure kernel, exact measure/return/suffix nonimplication guards, and a conditional boundary-Z_B route"
            ),
        },
        "fixed_record_typed_measure_kernel": fixed_record_typed_kernel(),
        "Lebesgue_decomposition_D1_non_domination": lebesgue_decomposition_guard(),
        "return_depth_weighted_coarea_countermodel": return_depth_countermodel(),
        "F17_suffix_product_countermodel": f17_suffix_product_guard(),
        "conditional_boundary_ZB_alternative": conditional_boundary_z_route(),
        "Gate5_maturity_update": {
            "previous_global_maturity": "10/18",
            "new_global_field_completed": None,
            "newly_certified_sublayers": [
                "typed fixed-record direct-sum measure kernel",
                "Lebesgue-decomposition obstruction to D1 domination",
                "return-depth and suffix-product exact nonimplication guards",
                "conditional boundary-Z_B alternative interface",
            ],
            "reason_no_new_field_credit": (
                "the all-record Borel owner join, face-tower moment, Z_B resolvent, F17 dynamic-test estimate and cemetery remain missing"
            ),
            "current_global_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "typed_fixed_record_measure_join": "CERTIFIED",
            "global_all_record_same_measure_F10_kernel": "NOT_CERTIFIED",
            "physical_D1_dominates_face_measures": False,
            "return_depth_weighted_face_integrability": "NOT_CERTIFIED",
            "complete_all_face_F10": "NOT_CERTIFIED",
            "F17_bulk_dynamic_test": "NOT_CERTIFIED",
            "joint_insertion_suffix_rank_tail": "NOT_CERTIFIED",
            "strong_F13": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "F14_F15_F17_F18": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "Gate5_maturity": "10/18",
            "complete_18_field_operator_block_count": 0,
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
        "dependencies": dict(DEPENDENCIES),
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
        default=HERE / "cm2_gate5_round49_typed_measure_f10_f17_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    strict = result["strict_nonpromotion"]
    print("TYPED_RECORD_KERNEL:", strict["typed_fixed_record_measure_join"])
    print("GLOBAL_SAME_MEASURE_F10:", strict["global_all_record_same_measure_F10_kernel"])
    print("GATE5_MATURITY:", strict["Gate5_maturity"])
    print("CM2:", strict["CM2"])
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
