#!/usr/bin/env python3
"""Round-49 sharp closed recovery and common-parent-law certificate.

This append-only layer makes two corrections/extensions to the Round-47/48
post-C24 bookkeeping.

* The exact shortest integer closed block which halves the inherited Growth
  term is 696, not the former safe value 1005.  Consequently the sharp safe
  per-orientation clock is H+221328+696*k and eta=1/4176.
* Under an explicitly stated *single common parent law*, a pointwise maximum
  W_r pays forward and reverse recovery on their own survivor supports.  This
  avoids any false assertion that the two survivors, shells, or proper
  returned families coincide.

The needed measurable grouping of the physical arbitrary-R_n leaf registry
into whole proper families is not installed.  Exact countermodels show why a
Borel leaf kernel alone cannot supply aggregate Z or a recovery-clock moment.
Accordingly C_fw, C_rev, q, strong cemetery, Gate 4, and CM2 remain open.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round49-sharp-common-law-recovery.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round49-sharp-common-law-recovery-manifest-2026-07-19.json"
)
DEFAULT_VERIFIER = HERE / "cm2_gate34_round49_sharp_common_law_recovery_verifier.py"

DEPENDENCIES = {
    "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json": (
        "79eeff7d5c18ec7d28a30c61ae857a733b3136202917c54f6aeaf93d7f414089"
    ),
    "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json": (
        "68f0ee7595688ef4ea1ab5eb1e101ab8c2ccd327d3bcf40876ccbd40a5d9bfab"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
}

CLOSED_NUMERATOR = 360134800
CLOSED_DENOMINATOR = 360493663
CLOSED_A = Q(CLOSED_NUMERATOR, CLOSED_DENOMINATOR)
CLOSED_MARGIN = Q(358863, CLOSED_DENOMINATOR)
SHARP_HALF_BLOCK = 696
FORMER_SAFE_BLOCK = 1005
POSTCUT_BASE = 318
SHARP_POSTCUT_BASE = SHARP_HALF_BLOCK * POSTCUT_BASE
ETA = Q(1, 6 * SHARP_HALF_BLOCK)
ETA_DENOMINATOR = 4176
PROPER_C_P = Q(4 * 10**90 * CLOSED_DENOMINATOR, 358863)
CLOSED_ADDITIVE = Q(2 * 10**90)

TAIL_A = Q(550000, 147)
TAIL_R = Q(111718729, 111718750)
K_RANK = Q(
    3055930500533353804145008325576782226562500,
    453789,
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    return str(value)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


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
    round47 = load(
        "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json"
    )["result"]
    envelope = round47["one_step_postcut_Z_envelope"]
    if envelope["P_power_bracket"] != "2^316<P<2^317":
        raise RuntimeError("Round47 P bracket")
    if not (Q(2) ** 316 < Q(envelope["P_exact"]) < Q(2) ** 317):
        raise RuntimeError("Round47 P arithmetic")
    if Q(envelope["P_exact"]) / Q(envelope["Z1"]) != PROPER_C_P:
        raise RuntimeError("Round47 proper constant")
    dyadic = round47["per_orientation_dyadic_postcut_return"]
    if "a^1005<=1/2" not in dyadic["proof"]:
        raise RuntimeError("Round47 safe block")
    if dyadic["single_short_leaf_assumed_proper"] is not False:
        raise RuntimeError("Round47 whole-family type")
    if dyadic["same_ID_forward_reverse_survivor_or_common_k_asserted"] is not False:
        raise RuntimeError("Round47 pair overclaim")

    round48 = load(
        "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json"
    )["result"]
    kernel = round48["fixed_s_Borel_parent_survivor_kernel"]
    if kernel["whole_proper_family_grouping_installed"] is not False:
        raise RuntimeError("Round48 grouping overclaim")
    if kernel["identical_fw_rev_survivor_asserted"] is not False:
        raise RuntimeError("Round48 survivor equality")
    theorem = round48["standard_Borel_whole_proper_family_shell_theorem"]
    if theorem["this_extra_input_joined_to_Round35_leaf_kernel"] is not False:
        raise RuntimeError("Round48 missing join")
    if "C_sigma=H+319590+1005*k_sigma" not in theorem["terminal_time_contract"]:
        raise RuntimeError("Round48 predecessor clock")
    if round48["strict_nonpromotion"]["Gate4"] != "NOT_CERTIFIED":
        raise RuntimeError("Round48 Gate4")

    d1 = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]
    moment = d1["global_physical_L6over5_moment"]
    if Q(moment["K_rank_exact"]) != K_RANK:
        raise RuntimeError("Round35 K_rank")
    if Q(moment["A"]) != TAIL_A or Q(moment["r"]) != TAIL_R:
        raise RuntimeError("Round35 tail inputs")
    if moment["N_open_type"] != "one uniform theorem-supplied integer>=1, not numeric":
        raise RuntimeError("Round35 N_open type")
    if d1["strict_nonpromotion"]["D1_rank_sum_dominates_complete_C_fw_C_rev"] is not False:
        raise RuntimeError("Round35 D1 overclaim")


def sharp_half_block_certificate() -> dict[str, Any]:
    assert SHARP_POSTCUT_BASE == 221328
    assert ETA == Q(1, ETA_DENOMINATOR)
    assert 2 * CLOSED_NUMERATOR**695 > CLOSED_DENOMINATOR**695
    assert 2 * CLOSED_NUMERATOR**696 < CLOSED_DENOMINATOR**696
    assert CLOSED_ADDITIVE / (1 - CLOSED_A) == PROPER_C_P / 2
    return {
        "closed_Growth_coefficient_a": qstr(CLOSED_A),
        "closed_margin_1_minus_a": qstr(CLOSED_MARGIN),
        "exact_predecessor_comparison": (
            "2*360134800^695>360493663^695, hence a^695>1/2"
        ),
        "exact_sharp_comparison": (
            "2*360134800^696<360493663^696, hence a^696<1/2"
        ),
        "shortest_positive_integer_L_with_a_power_below_half": SHARP_HALF_BLOCK,
        "former_1005_block_is_safe_but_not_minimal": True,
        "closed_recurrence": (
            "Z(T_s^r H)/mass(H)<=a^r*Z(H)/mass(H)+2e90/(1-a)"
        ),
        "steady_term_identity": "2e90/(1-a)=C_p/2",
        "one_half_block_action": (
            "one 696-block halves the inherited normalized-Z term strictly; the steady term remains C_p/2"
        ),
        "proof_scope": (
            "closed post-cut evolution of one whole positive survivor standard family; no leafwise properness claim"
        ),
        "status": "CERTIFIED_EXACT_SHORTEST_HALF_CONTRACTION_BLOCK",
    }


def sample_clock_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for terminal_time, k in ((0, 0), (0, 14), (696, 3), (1393, 64)):
        terminal_blocks = (terminal_time + SHARP_HALF_BLOCK - 1) // SHARP_HALF_BLOCK
        rows.append(
            {
                "terminal_time_H": terminal_time,
                "terminal_block_ceiling": terminal_blocks,
                "shell_k": k,
                "clock": terminal_time + SHARP_POSTCUT_BASE + SHARP_HALF_BLOCK * k,
                "rational_majorant_power": POSTCUT_BASE + terminal_blocks,
                "residual_shell_ratio_power": k,
            }
        )
    return rows


def sharp_per_orientation_shell_theorem() -> dict[str, Any]:
    rows = sample_clock_rows()
    assert ETA * SHARP_HALF_BLOCK == Q(1, 6)
    assert ETA * SHARP_POSTCUT_BASE == 53
    assert Q(1, 2) * Q(6, 5) == Q(3, 5)
    return {
        "conditional_extra_input": (
            "a finite standard-Borel outer kernel y->G_y of whole canonical proper families, K_par(y,X)=p(y)=mass(G_y)>0, Z(G_y)<=C_p*p(y), and Borel post-cut mass h_sigma(y)"
        ),
        "postcut_whole_survivor_inheritance": (
            "H_sigma(y) is the whole killed survivor family and Round47 gives Z(H_sigma)<=P*p(y) with P<2^317"
        ),
        "extra_input_joined_to_physical_arbitrary_Rn_leaf_kernel": False,
        "dyadic_shell": (
            "unique k_sigma>=0 with 2^(-(k_sigma+1))*p<h_sigma<=2^(-k_sigma)*p"
        ),
        "zero_survivor_policy": (
            "if h_sigma=0 set k_sigma=0 and C_sigma=0 and set its survivor-supported weighted term to zero; never normalize the zero family"
        ),
        "terminal_time_contract": (
            "H is the collision index of the terminal C24 test, inclusive"
        ),
        "sharp_clock": "C_sigma(H,k)=H+696*(318+k)=H+221328+696*k",
        "one_step_route": "the Round47 one-step post-cut envelope is used, so no 9148 block is added",
        "eta": qstr(ETA),
        "A_H": "(6/5)^(318+ceil(H/696))",
        "rational_exponential_majorant": (
            "e<11/4<(6/5)^6, hence exp(1/6)<6/5"
        ),
        "pointwise_bound": (
            "h_sigma*exp(C_sigma/4176)<p*(6/5)^(318+ceil(H/696))*(3/5)^k_sigma"
        ),
        "integrated_bound": (
            "integral h_sigma*exp(C_sigma/4176) dlambda<A_H*integral p dlambda"
        ),
        "fixed_H_scope": True,
        "Borel_variable_H_extension": (
            "valid only with the additional integrability of (6/5)^ceil(H(y)/696) against p(y)dlambda"
        ),
        "numeric_H_cover_available": False,
        "sample_rows": rows,
        "sample_rows_sha256": digest(rows),
        "status": "CERTIFIED_CONDITIONAL_SHARP_WHOLE_FAMILY_SHELL_THEOREM",
    }


def common_parent_law_theorem() -> dict[str, Any]:
    r_rows = [
        {
            "r": 6,
            "gamma": "1/25056",
            "holder_output": "integral c*W_6<=||c||_(6/5)*(1+2*A_H)^(1/6) for unit parent mass",
        },
        {
            "r": 12,
            "gamma": "1/50112",
            "holder_output": (
                "integral (c*W_12)^(12/11)<=(integral c^(6/5))^(10/11)*(1+2*A_H)^(1/11) for unit parent mass"
            ),
        },
    ]
    assert ETA / 6 == Q(1, 25056)
    assert ETA / 12 == Q(1, 50112)
    return {
        "hypotheses": {
            "outer_kernel": (
                "a standard-Borel kernel (Y,lambda), y->whole canonical proper family G_y"
            ),
            "finite_kernel_normalization": (
                "K_par(y,X)=p(y)=mass(G_y), so m(YxX)=integral p dlambda<infinity"
            ),
            "aggregate_properness": (
                "p(y)>0, Z(G_y)<=C_p*p(y), and each whole postcut survivor satisfies Z(H_sigma)<=P*p with P<2^317"
            ),
            "single_common_parent_law": (
                "m(dy,dx)=lambda(dy)K_par(y,dx); fw and rev are Borel predicates on this same m, not separately normalized laws"
            ),
            "same_physical_restriction": (
                "both predicates are pulled through the Round35 measure-preserving two-view maps to the identical parent restriction ID"
            ),
            "Borel_masses_and_shells": (
                "h_sigma(y)=K_par(y,S_sigma(y)) and k_sigma(y) are Borel"
            ),
            "terminal_time": "one fixed finite common H; a variable H needs the extra A_H integrability stated above",
            "zero_survivor": (
                "on h_sigma=0 define k_sigma=C_sigma=0 and the survivor-supported exponential term as zero; never normalize it"
            ),
        },
        "hypotheses_installed_for_physical_arbitrary_Rn_registry": False,
        "definition": (
            "W_r(y,x)=max(1,1_Sfw*exp(C_fw/(4176*r)),1_Srev*exp(C_rev/(4176*r)))"
        ),
        "pointwise_once_charge": (
            "W_r^r<=1+1_Sfw*exp(C_fw/4176)+1_Srev*exp(C_rev/4176)"
        ),
        "integrated_common_law_bound": (
            "integral W_r^r dm<(1+2*A_H)*integral p dlambda"
        ),
        "general_Holder_outputs": [
            "integral c*W_6<=(integral c^(6/5))^(5/6)*((1+2*A_H)*integral p)^(1/6)",
            "integral (c*W_12)^(12/11)<=(integral c^(6/5))^(10/11)*((1+2*A_H)*integral p)^(1/11)",
        ],
        "parent_charged_once": True,
        "identical_fw_rev_survivor_required": False,
        "common_shell_required": False,
        "proper_intersection_required": False,
        "r_instances": r_rows,
        "r_instances_sha256": digest(r_rows),
        "status": "CERTIFIED_CONDITIONAL_COMMON_PARENT_LAW_W_R_THEOREM",
    }


def synchronized_ambient_pair() -> dict[str, Any]:
    assert CLOSED_A * PROPER_C_P + CLOSED_ADDITIVE == (
        (1 + CLOSED_A) * PROPER_C_P / 2
    )
    assert (1 + CLOSED_A) * PROPER_C_P / 2 < PROPER_C_P
    return {
        "closed_proper_class_forward_invariant": (
            "a*C_p+2e90=(1+a)*C_p/2<C_p"
        ),
        "common_ambient_clock": (
            "C_pair=H+221328+696*max(k_fw,k_rev) makes both separate ambient survivor families proper"
        ),
        "two_ambient_families_are_alternative_views": True,
        "one_common_physical_survivor_inferred": False,
        "intersection_properness_inferred": False,
        "parent_weighted_exponential_moment_of_C_pair_inferred": False,
        "correct_moment_bypass": "use W_r, which pays each clock only on its own survivor support",
        "status": "CERTIFIED_SYNCHRONIZED_AMBIENT_PAIR_PROPERNESS_ONLY",
    }


def conditional_D1_interface() -> dict[str, Any]:
    # Exact fifth-power comparison: 2^(6/5)<3 iff 2^6<3^5.
    assert 2**6 < 3**5
    return {
        "physical_D1_density": "d_D1=151*sum_i 2^B_i",
        "once_charge": "c0=max(2,d_D1)",
        "Round35_moment": "integral d_D1^(6/5)<M_D=K_rank*N_open^3",
        "K_rank_exact": qstr(K_RANK),
        "N_open_numeric": None,
        "normalization_scope": (
            "the displayed M_D+3 and tail formulas use the Round35 normalized physical parent probability, integral p dlambda=1"
        ),
        "general_mass_M0_once_charge_bound": (
            "for M0=integral p dlambda, integral c0^(6/5)<M_D+3*M0"
        ),
        "normalized_once_charge_bound": "integral c0^(6/5)<M_D+3",
        "missing_condition": (
            "the physical arbitrary-R_n leaf/component registry must first be grouped measurably into the whole-proper-family single common parent law required by W_r"
        ),
        "missing_condition_installed": False,
        "r6_L1_recovery_moment": (
            "integral c0*W_6<=(M_D+3)^(5/6)*(1+2*A_H)^(1/6)"
        ),
        "r12_L12over11_moment": (
            "integral (c0*W_12)^(12/11)<=(M_D+3)^(10/11)*(1+2*A_H)^(1/11)"
        ),
        "tail_inputs": {
            "A_tail": qstr(TAIL_A),
            "r_tail": qstr(TAIL_R),
            "block_integer": "N_open>=1, theorem-supplied and nonnumeric",
        },
        "conditional_recovery_weighted_tail": (
            "Wbar_D1rec(n)<(M_D+3)^(5/6)*((1+2*A_H)*A_tail)^(1/12)*r_tail^(floor(n/N_open)/12)"
        ),
        "conditional_block_exponent": "1/12",
        "D1_dominates_complete_C_fw_C_rev": False,
        "D1_recovery_tail_is_final_q_tail": False,
        "conditional_AC_D1_recovery_cemetery_only": True,
        "strong_singular_corner_trace_cemetery": "NOT_CERTIFIED",
        "status": "CERTIFIED_FORMULAS_CONDITIONAL_ON_MISSING_COMMON_LAW_JOIN",
    }


def whole_family_grouping_obstructions() -> dict[str, Any]:
    finite_mass_rows = [
        {
            "n": n,
            "leaf_length": f"4^-{n}",
            "leaf_mass": f"4^-{n}",
            "boundary_Z_term": "1",
        }
        for n in range(1, 9)
    ]
    defect_rows = [
        {
            "group_n": n,
            "group_mass": f"2^-{n}",
            "leaf_count": f"2^({n}^2)",
            "each_leaf_length": f"2^-({n}^2)",
            "each_leaf_mass": f"2^-({n}+{n}^2)",
            "J_over_mass": f"2^({n}^2)",
        }
        for n in range(1, 6)
    ]
    return {
        "finite_mass_infinite_Z_countermodel": {
            "construction": "leaves n>=1 with ell_n=4^-n, p_n=4^-n, constant density",
            "total_mass": "sum_(n>=1)4^-n=1/3",
            "aggregate_Z": "sum_(n>=1)p_n/ell_n=sum_(n>=1)1=infinity",
            "rows": finite_mass_rows,
            "rows_sha256": digest(finite_mass_rows),
            "conclusion": "a Borel leaf kernel and finite total mass do not imply finite aggregate Z or a whole proper family",
        },
        "required_grouping_fields": {
            "Borel_family_id": "NOT_INSTALLED",
            "exact_outer_disintegration_reconstructing_physical_mass": "NOT_INSTALLED",
            "finite_boundary_numerator": "J(z)=integral p(y)/ell_*(y) dlambda_z(y)<infinity",
            "group_mass": "m(z)=integral p(y) dlambda_z(y)>0",
            "dyadic_defect": (
                "D_Z(z)=0 if J<=C_p*m; otherwise ceil(log2(2*J/(C_p*m)))"
            ),
            "defect_recovery_clock": "696*D_Z(z)",
            "physical_tail_or_exponential_moment_of_D_Z": "NOT_INSTALLED",
        },
        "finite_recordwise_J_no_global_clock_moment_countermodel": {
            "construction": (
                "group n has mass 2^-n split over 2^(n^2) leaves, each of length 2^(-n^2) and mass 2^(-(n+n^2))"
            ),
            "recordwise_J": "J_n=2^(n^2-n)<infinity",
            "ratio": "J_n/m_n=2^(n^2), so D_Z grows quadratically",
            "moment_failure": (
                "for every eta>0, 2^-n*exp(eta*696*D_Z(n)) does not tend to zero"
            ),
            "rows": defect_rows,
            "rows_sha256": digest(defect_rows),
            "conclusion": "recordwise finite J alone supplies no physical recovery-clock moment",
        },
        "status": "CERTIFIED_EXACT_WHOLE_FAMILY_GROUPING_NONIMPLICATIONS",
    }


def intersection_and_cemetery_nonpromotion() -> dict[str, Any]:
    rows = [
        {
            "model": "shrinking overlap",
            "fw_survivor": "[0,1/2+epsilon]",
            "rev_survivor": "[1/2,1]",
            "intersection": "[1/2,1/2+epsilon]",
            "ambient_normalized_boundary_cost": "bounded",
            "intersection_normalized_boundary_cost": "1/epsilon -> infinity",
            "conclusion": "two ambient proper returns do not make their intersection proper",
        },
        {
            "model": "vanishing mass but infinite boundary trace",
            "components": "countably many intervals with mass 2^-j and length 2^-j",
            "discarded_mass_after_finite_truncation": "tends to zero",
            "discarded_boundary_Z": "sum_(j>N)1=infinity",
            "conclusion": "mass truncation does not imply strong cemetery or trace control",
        },
    ]
    return {
        "Borel_intersection_subkernel_exists": True,
        "finite_component_truncations_can_be_made_Borel": True,
        "full_intersection_proper": "NOT_CERTIFIED",
        "uniform_intersection_boundary_numerator": "NOT_CERTIFIED",
        "intersection_clock_moment": "NOT_CERTIFIED",
        "strong_cemetery_from_vanishing_discarded_mass": False,
        "rows": rows,
        "rows_sha256": digest(rows),
        "status": "CERTIFIED_EXACT_INTERSECTION_AND_CEMETERY_NONIMPLICATIONS",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "parameterwise for each fixed |s|<=1/400 and finite n",
            "claim_type": (
                "exact sharp closed recovery, conditional common-parent-law recovery moments, and exact grouping/intersection nonimplications"
            ),
        },
        "exact_sharp_closed_half_block": sharp_half_block_certificate(),
        "sharp_per_orientation_whole_family_shell_theorem": (
            sharp_per_orientation_shell_theorem()
        ),
        "same_ID_common_parent_law_W_r_theorem": common_parent_law_theorem(),
        "synchronized_two_ambient_family_properness": synchronized_ambient_pair(),
        "conditional_physical_D1_recovery_interface": conditional_D1_interface(),
        "whole_family_grouping_obstructions": whole_family_grouping_obstructions(),
        "intersection_and_cemetery_nonpromotion": (
            intersection_and_cemetery_nonpromotion()
        ),
        "corrected_frontier": {
            "numeric_H_cover": None,
            "numeric_actual_beta_Wdiag": None,
            "strict_inferable_uniform_beta_lower": "0",
            "physical_arbitrary_Rn_whole_proper_family_grouping": "NOT_CERTIFIED",
            "finite_J_and_physical_D_Z_tail": "NOT_CERTIFIED",
            "full_same_ID_common_law_C_fw_C_rev_density_in_L6over5": "NOT_CERTIFIED",
            "proper_common_fw_rev_intersection": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_singular_corner_trace_cemetery": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "exact_shortest_closed_half_block_696": "CERTIFIED",
            "sharp_clock_H_plus_221328_plus_696k": "CERTIFIED_CONDITIONAL_WHOLE_FAMILY",
            "common_parent_law_W_r_theorem": "CERTIFIED_CONDITIONAL_ABSTRACT",
            "D1_recovery_weighted_L12over11_and_tail": "CONDITIONAL_NOT_PHYSICALLY_JOINED",
            "whole_proper_family_kernel_join": "NOT_CERTIFIED",
            "numeric_H_cover_and_actual_beta": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
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
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    strict = build_result()["strict_nonpromotion"]
    print("SHARP_HALF_BLOCK_696:", strict["exact_shortest_closed_half_block_696"])
    print("COMMON_PARENT_LAW_W_R:", strict["common_parent_law_W_r_theorem"])
    print("PHYSICAL_WHOLE_FAMILY_JOIN: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
