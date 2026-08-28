#!/usr/bin/env python3
"""Round-48 fixed-s Borel survivor-kernel and ambient-clock certificate.

Round 47 upgraded a positive post-C24 survivor whole family by a dyadic
familywise recovery clock, but only stated the resulting shell lemma for a
finite/countable list.  This append-only layer separates two types:

* the existing arbitrary-R_n leaf/component registry gives a fixed-s Borel
  parent kernel and Borel forward/reverse survivor subkernels; and
* an abstract measurable grouping into whole proper families upgrades the
  dyadic calculation to a standard-Borel integral theorem.

The existing leaf kernel is not silently identified with that whole-family
grouping.  Forward and reverse survivors are also not asserted equal.  A
common-intersection mass has a useful ambient-clock moment, but the
intersection need not remain proper, so this is not a joint return, C_fw,
C_rev, q, cemetery, or Gate-4 certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round48-borel-survivor-kernel.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round48-borel-survivor-kernel-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json": (
        "79eeff7d5c18ec7d28a30c61ae857a733b3136202917c54f6aeaf93d7f414089"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
}

POSTCUT_BASE = 318
RECOVERY_HALF_BLOCK = 1005
POSTCUT_CLOCK_BASE = 319590
ETA_ONE = Q(1, 6030)
ETA_PAIR = Q(1, 12060)
HIT_BETA_THRESHOLD = Q(230400, 5197322039)
PROPER_C_P = Q(4 * 10**90 * 360493663, 358863)
LONG_LEAF_WEIGHT_LOWER = Q(1, 2)
DELTA_LONG = LONG_LEAF_WEIGHT_LOWER / PROPER_C_P
LONG_LEAF_CROSSING_FRACTION_REQUIRED = 2 * HIT_BETA_THRESHOLD


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


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
    round47 = load(
        "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json"
    )["result"]
    dyadic = round47["per_orientation_dyadic_postcut_return"]
    if dyadic["per_orientation_postcut_clock"] != (
        "R_post(k)=1005*(318+k)=319590+1005*k"
    ):
        raise RuntimeError("Round47 postcut clock")
    if round47["one_step_postcut_Z_envelope"]["large_9148_step_Z0_not_used"] is not True:
        raise RuntimeError("Round47 route")
    if round47["corrected_frontier"]["numeric_H_cover"] is not None:
        raise RuntimeError("H_cover overclaim")
    envelope = round47["one_step_postcut_Z_envelope"]
    if Q(envelope["P_exact"]) / Q(envelope["Z1"]) != PROPER_C_P:
        raise RuntimeError("Round47 proper constant")

    carrier = load(
        "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
    )["result"]
    registry = carrier["arbitrary_Rn_parent_W_Borel_registry"]
    disintegration = carrier["collision_SRB_leaf_disintegration"]
    pair = carrier["common_forward_reverse_carrier_pair"]
    if registry["registry_type"] != "standard-Borel parameterized actual curve registry":
        raise RuntimeError("Borel curve registry")
    if registry["U_intersection_leaf"] != "countable disjoint union of open intervals":
        raise RuntimeError("leaf sections")
    if disintegration["coordinate_change"] != "(r,b)->(r,p=sin(4r+b))":
        raise RuntimeError("leaf coordinates")
    if disintegration["absolute_Jacobian"] != "cos(phi)=cp":
        raise RuntimeError("leaf Jacobian")
    if disintegration["integrating_leaf_weights_recovers_mu_s_restricted_to_component"] is not True:
        raise RuntimeError("disintegration")
    if pair["actual_parameterized_common_fw_rev_carrier_pair_registry"] != "CERTIFIED":
        raise RuntimeError("same-ID carrier")
    if pair["forward_and_reverse_share_identical_component_and_restriction"] is not True:
        raise RuntimeError("same restriction")

    path = load(
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    )["result"]
    component = path["canonical_regular_connected_component_schema"]
    level = path["arbitrary_n_Rn_Qn_level_and_mass_schema"]
    if component["scope"] != "fixed_parameter_s_and_fixed_finite_n":
        raise RuntimeError("fixed-s component scope")
    if component["regular_open_fibre_has_at_most_countably_many_connected_components"] is not True:
        raise RuntimeError("component countability")
    if component["uniform_joint_parameter_component_atlas_claimed"] is not False:
        raise RuntimeError("joint-s overclaim")
    if level["path_fibre_refinement"]["singular_and_core_boundary_cemetery_mass"] != "0":
        raise RuntimeError("boundary mass")

    core_source = HERE / "cm2_gate25_physical_return_core_registry_cert.py"
    if not core_source.is_file() or core_source.is_symlink():
        raise RuntimeError("unsafe core source")
    if sha(core_source) != DEPENDENCIES[core_source.name]:
        raise RuntimeError("core source hash")
    source_text = core_source.read_text(encoding="utf-8")
    for token in (
        "DIAGONAL_T_LOWER = Q(69, 100)",
        "DIAGONAL_T_UPPER = Q(7, 10)",
        "DIAGONAL_P_HALF_WIDTH = Q(1, 50)",
        'for source in ("G", "W"):',
        'for direction in ("NE", "NW", "SE", "SW"):',
        "for cell, sign in (first, second):",
    ):
        if token not in source_text:
            raise RuntimeError(f"W-diagonal core token: {token}")


def stationary_wdiag_union_mass_comparison() -> dict[str, Any]:
    # Eight pairwise-disjoint W-source diagonal rectangles: four diagonal
    # directions and two wall-chart cells per direction.  Each raw area is
    # R_W*Delta_t*Delta_p=(4/25)*(1/100)*(1/25)=1/15625.  Dividing by the
    # global collision-volume upper 4*(22/7)*(13/25)=1144/175 gives 7/715000.
    one_core = Q(7, 715000)
    union = 8 * one_core
    difference = union - HIT_BETA_THRESHOLD
    ratio = union / HIT_BETA_THRESHOLD
    assert union == Q(7, 89375)
    assert difference == Q(1214558021, 35731589018125)
    assert ratio == Q(2798558021, 1584000000)
    assert one_core < HIT_BETA_THRESHOLD < union
    return {
        "selected_stationary_core_family": "the eight pairwise-disjoint W-source diagonal C24 cores",
        "core_count": 8,
        "one_core_collision_SRB_mass_strict_lower": str(one_core),
        "union_collision_SRB_mass_strict_lower": str(union),
        "Round47_required_crossing_weight_threshold": str(HIT_BETA_THRESHOLD),
        "union_minus_threshold": str(difference),
        "union_to_threshold_ratio": str(ratio),
        "single_core_below_threshold": True,
        "eight_core_union_above_threshold": True,
        "measure_type_mismatch": (
            "this is stationary two-dimensional collision-SRB mass, not the terminal-time weight of W-diagonal-crossing extended parents inside every singular proper standard family"
        ),
        "numeric_mixing_or_disintegration_bridge_available": False,
        "actual_beta_Wdiag_inferred": False,
        "strict_inferable_beta_lower_from_this_comparison": "0",
        "status": "CERTIFIED_STATIONARY_MASS_TARGET_COMPARISON_ONLY",
    }


def long_leaf_target_cover_reduction() -> dict[str, Any]:
    # If Z(G)<=C_p mass(G), the total family weight of leaves shorter than
    # delta is at most delta*Z(G).  For a normalized family, delta=(1/2)/C_p
    # therefore leaves at least half the weight on leaves of length >=delta.
    # A source-fraction zeta on every such long leaf gives
    # beta_Wdiag >= (1/2)*zeta.  This is a reduction, not the missing atlas.
    assert DELTA_LONG == Q(358863, 2883949304 * 10**90)
    assert LONG_LEAF_CROSSING_FRACTION_REQUIRED == Q(460800, 5197322039)
    assert LONG_LEAF_WEIGHT_LOWER * LONG_LEAF_CROSSING_FRACTION_REQUIRED == (
        HIT_BETA_THRESHOLD
    )
    return {
        "proper_family_hypothesis": "Z(G)<=C_p*mass(G)",
        "C_p": str(PROPER_C_P),
        "short_leaf_weight_inequality": (
            "weight{|W|_*<delta}<=delta*Z(G)<=delta*C_p*mass(G)"
        ),
        "chosen_short_weight_budget": "1/2",
        "delta_long": str(DELTA_LONG),
        "long_leaf_weight_lower": str(LONG_LEAF_WEIGHT_LOWER),
        "required_per_long_leaf_Wdiag_crossing_source_fraction": str(
            LONG_LEAF_CROSSING_FRACTION_REQUIRED
        ),
        "conditional_aggregation": (
            "if one common terminal H_cover supplies disjoint once-counted W-diagonal crossing extended parents of source fraction zeta_rect on every leaf with |W|_*>=delta_long, then beta_Wdiag>=(1/2)*zeta_rect>=230400/5197322039"
        ),
        "reference_rectangle_or_long_leaf_atlas_installed": False,
        "finite_cover_rows_materialized": False,
        "per_long_leaf_crossing_mass_lower_available": False,
        "numeric_H_cover": None,
        "numeric_actual_beta_Wdiag": None,
        "strict_inferable_actual_beta_lower": "0",
        "status": "CERTIFIED_LONG_LEAF_REDUCTION_ONLY",
    }


def fixed_s_parent_survivor_kernel() -> dict[str, Any]:
    return {
        "parameter_scope": "each fixed |s|<=1/400 and each fixed finite n; no joint-(s,component) atlas",
        "index_space": (
            "standard-Borel tuples y=(component-id,b,source-interval-rank,incidence-rank-path,short-cell-k)"
        ),
        "leaf_chart": "Psi_s(b,r)=(r,p=sin(4r+b))",
        "parent_kernel": (
            "K_par(y,A)=Z_N^-1*integral 1_(U_y intersect A)(Psi_s(b,r))*cos(4r+b) dr"
        ),
        "kernel_measurability_reason": (
            "the regular component sections are countable Borel/open intervals, Psi_s and the positive Jacobian are continuous on each rank cell, and parameter integration preserves Borel measurability"
        ),
        "mass_reconstruction": (
            "summing component kernels and integrating the leaf parameter recovers mu_s restricted to R_n or Q_n modulo its zero-mass boundary"
        ),
        "finite_schedule_survivor_predicate": (
            "for every frozen finite cut schedule and orientation sigma, S_sigma(y,x) is a Borel finite intersection of regular branch and C24 predicates"
        ),
        "survivor_subkernel": "K_sur^sigma(y,A)=K_par(y,A intersect S_sigma(y))",
        "Borel_mass_functions": [
            "p(y)=K_par(y,N)",
            "h_fw(y)=K_sur^fw(y,N)",
            "h_rev(y)=K_sur^rev(y,N)",
        ],
        "zero_survivor_policy": "h_sigma=0 is sent to cemetery and is never normalized",
        "same_ID_pair": (
            "K_sur^fw and K_sur^rev carry the same Round35 restriction ID and equal parent mass, but are two possibly different Borel subkernels"
        ),
        "identical_fw_rev_survivor_asserted": False,
        "common_shell_asserted": False,
        "whole_proper_family_grouping_installed": False,
        "status": "CERTIFIED_FIXED_S_BOREL_PARENT_SURVIVOR_SUBKERNEL_SCHEMA",
    }


def sample_pointwise_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for terminal_time, k in ((0, 0), (0, 14), (1005, 3), (2011, 64)):
        terminal_blocks = (terminal_time + 1004) // 1005
        rows.append(
            {
                "terminal_time_H": terminal_time,
                "terminal_block_ceiling": terminal_blocks,
                "shell_k": k,
                "clock": terminal_time + POSTCUT_CLOCK_BASE + RECOVERY_HALF_BLOCK * k,
                "rational_majorant_power": POSTCUT_BASE + terminal_blocks,
                "residual_shell_ratio_power": k,
            }
        )
    return rows


def standard_borel_whole_family_shell_theorem() -> dict[str, Any]:
    assert ETA_ONE * POSTCUT_CLOCK_BASE == 53
    assert ETA_ONE * RECOVERY_HALF_BLOCK == Q(1, 6)
    assert Q(1, 2) * Q(6, 5) == Q(3, 5)
    rows = sample_pointwise_rows()
    return {
        "extra_input": (
            "a standard-Borel outer kernel y->G_y of whole canonical proper families with p(y)=mass(G_y)>0, aggregate Z(G_y)<=C_p*p(y), and Borel post-cut mass h_sigma(y)"
        ),
        "this_extra_input_joined_to_Round35_leaf_kernel": False,
        "Borel_shell": (
            "E_sigma,k={y:2^(-(k+1))*p(y)<h_sigma(y)<=2^-k*p(y)} is Borel"
        ),
        "terminal_time_contract": (
            "H is the collision index of the terminal C24 test, inclusive; C_sigma=H+319590+1005*k_sigma"
        ),
        "one_step_route_clock_policy": (
            "Round47 uses the one-step post-cut envelope, so no 9148 is added; a Round42 hereditary-block route would add 9148 per orientation"
        ),
        "eta": "1/6030",
        "pointwise_sharpening": (
            "h_sigma*exp(eta*C_sigma)<p*(6/5)^(318+ceil(H/1005))*(3/5)^k_sigma"
        ),
        "integrated_bound": (
            "integral h_sigma*exp(C_sigma/6030) dlambda < (6/5)^(318+ceil(H/1005))*integral p dlambda"
        ),
        "improvement_over_Round47_discrete_bound": (
            "the pointwise shell assignment removes the former safe but nonsharp factor 5/2"
        ),
        "orientation_separable_sum_bound": (
            "the fw plus rev survivor-weighted moments are <2*(6/5)^(318+ceil(H/1005))*integral p dlambda"
        ),
        "numeric_H_available": False,
        "sample_rows": rows,
        "sample_rows_sha256": digest(rows),
        "status": "CERTIFIED_CONDITIONAL_STANDARD_BOREL_WHOLE_FAMILY_SHELL_THEOREM",
    }


def common_intersection_ambient_clock_moment() -> dict[str, Any]:
    assert ETA_PAIR * (2 * POSTCUT_CLOCK_BASE) == 53
    assert ETA_PAIR * RECOVERY_HALF_BLOCK == Q(1, 12)
    return {
        "intersection_subkernel": (
            "K_cap=K_par restricted to S_fw intersect S_rev is Borel and may have zero mass h_cap"
        ),
        "ambient_shells": (
            "i and j are the separate dyadic shells of h_fw/p and h_rev/p; h_cap<=min(h_fw,h_rev)<=2^-max(i,j)*p"
        ),
        "ambient_clocks": [
            "C_fw=H+319590+1005*i recovers the whole fw survivor",
            "C_rev=H+319590+1005*j recovers the whole rev survivor",
        ],
        "eta_pair": "1/12060",
        "key_inequality": (
            "i+j<=2*max(i,j), hence 2^-max(i,j)*exp((i+j)/12)<=(3/5)^max(i,j)<=1"
        ),
        "integrated_bound": (
            "integral h_cap*exp((C_fw+C_rev)/12060) dlambda < (6/5)^(318+ceil(H/1005))*integral p dlambda"
        ),
        "what_the_clocks_recover": "the two ambient survivor families separately, not their intersection",
        "intersection_same_proper_class_return": "NOT_CERTIFIED",
        "same_ID_joint_return_or_q_inferred": False,
        "status": "CERTIFIED_BOREL_COMMON_INTERSECTION_MASS_AMBIENT_CLOCK_MOMENT",
    }


def exact_nonpromotion_models() -> dict[str, Any]:
    rows = [
        {
            "model": "shrinking overlap",
            "parent": "uniform family on [0,1]",
            "fw_survivor": "[0,1/2+epsilon]",
            "rev_survivor": "[1/2,1]",
            "ambient_normalized_boundary_cost": "bounded by 2 in each orientation",
            "intersection": "[1/2,1/2+epsilon]",
            "intersection_normalized_boundary_cost": "1/epsilon -> infinity",
            "conclusion": "two proper ambient survivors do not make their intersection proper",
        },
        {
            "model": "marginal survivor clock versus parent charge",
            "parent_record_mass": "p_n=1/(n*(n+1)), n>=1",
            "shells": "k_fw=0, k_rev=n",
            "survivor_fractions": "x_fw=1, x_rev=2^-n",
            "survivor_weighted_rev_term": "p_n*2^-n*exp(n/6)<p_n*(3/5)^n, summable",
            "parent_weighted_max_clock_term": "p_n*exp(n/6)>p_n*(7/6)^n, whose terms do not tend to zero",
            "conclusion": "separate survivor-weighted marginal moments do not imply the parent-weighted max/sum clock needed by q",
        },
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "common_intersection_inherits_properness": False,
        "marginal_survivor_moments_imply_parent_q_moment": False,
        "status": "CERTIFIED_EXACT_MEASURE_THEORETIC_NONIMPLICATIONS",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "parameterwise for every fixed |s|<=1/400",
            "claim_type": (
                "fixed-s Borel parent/survivor subkernels, a conditional standard-Borel whole-family shell theorem, and a common-intersection ambient-clock moment"
            ),
        },
        "fixed_s_Borel_parent_survivor_kernel": fixed_s_parent_survivor_kernel(),
        "stationary_Wdiag_union_mass_target_comparison": (
            stationary_wdiag_union_mass_comparison()
        ),
        "proper_family_long_leaf_target_cover_reduction": (
            long_leaf_target_cover_reduction()
        ),
        "standard_Borel_whole_proper_family_shell_theorem": (
            standard_borel_whole_family_shell_theorem()
        ),
        "same_ID_common_intersection_ambient_clock_moment": (
            common_intersection_ambient_clock_moment()
        ),
        "exact_nonpromotion_countermodels": exact_nonpromotion_models(),
        "corrected_frontier": {
            "numeric_H_cover": None,
            "numeric_actual_beta_Wdiag": None,
            "measurable_whole_proper_family_grouping_and_aggregate_Z": "NOT_CERTIFIED",
            "same_ID_identical_fw_rev_survivor_and_common_shell": "NOT_CERTIFIED",
            "intersection_same_proper_class_return": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "fixed_s_Borel_parent_survivor_subkernel_schema": "CERTIFIED",
            "conditional_standard_Borel_whole_family_shell_theorem": "CERTIFIED",
            "common_intersection_mass_ambient_clock_moment": "CERTIFIED",
            "proper_family_long_leaf_target_cover_reduction": "CERTIFIED",
            "whole_proper_family_kernel_join": "NOT_CERTIFIED",
            "same_ID_two_orientation_postcut_return": "NOT_CERTIFIED",
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
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_round48_borel_survivor_kernel_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    strict = result["strict_nonpromotion"]
    print("FIXED_S_BOREL_SURVIVOR_KERNEL:", strict["fixed_s_Borel_parent_survivor_subkernel_schema"])
    print("BOREL_WHOLE_FAMILY_SHELL:", strict["conditional_standard_Borel_whole_family_shell_theorem"])
    print("SAME_ID_JOINT_RETURN: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
