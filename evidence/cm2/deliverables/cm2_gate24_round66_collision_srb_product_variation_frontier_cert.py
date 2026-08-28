#!/usr/bin/env python3
"""Round-66 Gate-2/4 collision-SRB product/variation frontier."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round66_common import (
    CertError, digest, require, sha256_path, strict_json_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate24.round66.collision-srb-product-variation-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round66-collision-srb-product-variation-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_gate24_round66_collision_srb_product_variation_frontier_verifier.py"

PINS = {
    "cm2_round66_common.py": "34846761d5b448077a0cb5768d7e44fb2b354ae07f2b0d0475500bf96c85738f",
    "cm2-sixty-fifth-direct-assault-2026-07-21.md": "aeaafaf3411e90d6d1843159e248f18af12e5fdf993acfb9685adcc1b14e7bb0",
    "cm2-sixty-fifth-direct-assault-manifest-2026-07-21.sha256": "22283d37c12651e955b2502ad7660fa22d309c1d1902c471b1527470d6cc1cc2",
    "cm2-round65-independent-core-frontier-audit-2026-07-21.md": "b33405043f505f3f6323a6faf0de8f33e3f4c1f28db7ac891a56b2242a4df9e4",
    "cm2-round65-independent-core-frontier-audit-manifest-2026-07-21.json": "92ba883654f761a4df5974d889f99aa077769bb37ba0cd5d6fd03ceb8470629f",
    "cm2-round65-independent-core-frontier-audit-manifest-2026-07-21.sha256": "56cdbe5748338979e03eca9a859f119fda8c88d7b6663f530400f00f69583ed9",
    "cm2-gate24-round65-actual-product-tree-strong-assembly-frontier-assault-2026-07-21.md": "50868c8cee687425a43395e23210dbeddc8414006700fe23a7231721a4ee2e3a",
    "cm2-gate24-round65-actual-product-tree-strong-assembly-frontier-manifest-2026-07-21.json": "6b50742ac15f4fb4870d8e67b466252e57c1c796e48a1eaae5d2380f113cddd3",
    "cm2-gate24-round65-actual-product-tree-strong-assembly-frontier-manifest-2026-07-21.sha256": "924dbdc03b03b21094e637703353735ae348d9ef53c0c68b6e8acde5a4dfb1a3",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-assault-2026-07-21.md": "9bcf25242a4190e591919bd38233da4e036be22fc2c84739540a555f5f56b0ab",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.json": "f731715bd734649073e0bd35763c170a48ef8383f6dd892696b52a98ea86eb14",
    "cm2-round65-cross-gate-positive-potential-technology-frontier-manifest-2026-07-21.sha256": "ba3e550ac55d7e482d15817cdb9011c7a118100d90158d1c7aabdfeb94785b5a",
    "cm2-gate5-round58-owner-ledger-positive-transport-frontier-assault-2026-07-20.md": "eb971f719c58593114e3d187fd1de1aacac9fe9012b4c4934c6890bef6d68c9a",
    "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json": "27c5d2e9a6ac9ed8eeb3d42dc96aa1c0a8faa8e50e006811efea22b45c86b859",
    "cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.sha256": "6f0bce6fb81a58a9f4ecf940c0bb8e43f4b525f193341dc4ea497ac4e801391b",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-assault-2026-07-20.md": "2f66b1aff6551e97729d27f06c87a32957ab21404c0fb0ee3cc0210fa578b468",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json": "e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.sha256": "967421bc83b283510cdb25013f2e723e5761337e56471fad64a9ef74b35536c0",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-assault-2026-07-20.md": "88f042ed434f6199123a5f164385572dabfcde0af13a8d6b9d7ca1385079d00f",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json": "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.sha256": "4d7c3f06e1671319482c064ec3ea817562567202b111fd014434b7be0a460fac",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-assault-2026-07-20.md": "e99800b998a2fc547229a6b2a93dd84433634af76c691ef65c37b9024fc0d45c",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json": "2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.sha256": "a7499c939a1b167a21b62f8f0485ceaac5b44a9c21d2c59e3e22ee45805c56e2",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-assault-2026-07-21.md": "4acca86b074ce3f6792aa04625c9576d2affeacb0ad9d7cdeb09cabd08d45b00",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json": "e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256": "b94df87ba8362827bb1115f474c0beec59f887325e8db58b55a9020bf99ae6bc",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-assault-2026-07-21.md": "e57ba8db9a7ab0a8dc7643b575d02de99a10377ce36ba0efd1ba8ae75477325c",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.json": "955908ee74ff6ec0354224978850ef683aeacd1923ce85bffd1290467321d23f",
    "cm2-gate24-round63-stable-saturation-holonomy-square-frontier-manifest-2026-07-21.sha256": "a739ffbe1bb9f14fdc8c72c573594f56930a7c4f32efb77fa4dac60d256ec870",
    "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-assault-2026-07-21.md": "8c27993b71afa06f2b5a0432fea9aecb367329f1be6760d17e98bde0029b62c4",
    "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.json": "6eb0dbe73b21b5822e9e589b5f6a047b47966a349ec54e8e3b150b9bf203b1af",
    "cm2-gate24-round64-rooted-atlas-jacobian-tag-lift-frontier-manifest-2026-07-21.sha256": "474038420728935370c8ab9eb7be6df99fcf0da3e2baa88c01a8eff9c3f2d007",
    "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-assault-2026-07-21.md": "24555f1e5350d59f2be6f83208617c945ee12c10b925f05b7edc15c933044c76",
    "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.json": "5bb198256f2a5aa8837326f9eab70aa4845adb80417dc27379f27f7e8f24f8d0",
    "cm2-gate24-round64-weighted-tree-saturation-actual-join-obstruction-frontier-manifest-2026-07-21.sha256": "0943cc0316319a823f91ed29f732a1f828204db1e4376f8bad887523388809c6",
    "cm2-gate34-collision-srb-kac-return-baseline-assault-2026-07-18.md": "87ea865ba97567cbe5f3d3029d9be1a6a6d58cd49f390f5558fdbab26c82b243",
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a",
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.sha256": "c6acef0c867602a8bccfbfc052b13cecb60b8216d16c926cdd707645f3a30863",
    "cm2-gate2-round25-product-base-assault-2026-07-18.md": "db75a6a8741d435182a1e0d0510e06d1b75b15eaba3d0c26e090e9c5990664e6",
    "cm2-gate2-round25-product-base-manifest-2026-07-18.json": "8045c36fb14c69a145be4ebf4cd33ae11d55fd77f4591b91782f13516c80679b",
    "cm2-gate2-round25-product-base-manifest-2026-07-18.sha256": "4c1ab35de924739bb391aa594861ae0f2c3264d93a42073cc4868de9dec082fc",
    "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-assault-2026-07-20.md": "e6b87bd43bf4c35ca4804dc1a563a916d27cb0550c45e7b3fb1d670dddfd0934",
    "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.json": "42a035e38687acb4ae1a3ce43a1459c49ba08a1406083c811f919823ecc8d526",
    "cm2-gate123-round58-dini-shadow-cad-landing-join-frontier-manifest-2026-07-20.sha256": "83cf81e1ffd0630696d417f55fa6b2debd5a1bcb4e158c99bd92d3e976d92e62",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-assault-2026-07-20.md": "43f50426abfc92e041903af4d4eb6a416d686ea7ad25ad0f013bb56cd9f4110d",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json": "16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.sha256": "985910708fe715d0c891cd6a288b37a5e1b88530db858a712e7e82e80cbb4b71",
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-assault-2026-07-20.md": "f89fbb0180fe88cac358b14541d8e5f98a72a23a3d27a313f2fbef3a0a22d68f",
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.json": "f897d81a2e85c4a8e45c436f169043feaef93b019f18229a44da0227c75b2a88",
    "cm2-gate123-round60-combined-gauge-stable-strong-operator-frontier-manifest-2026-07-20.sha256": "6a29c47462a9526138a059f8577abcf879cd162feca14b435906cce1cd8c087a",
    "cm2-gate34-round26-boundary-tube-decay-assault-2026-07-18.md": "3a79058e3664b9dbd8cce4a3cecc8a05b7b6ba9f26a80cf0d491a27fff91924f",
    "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json": "6ee5be1c2b60438043284c26837eef7681c94f95290abee33e52b7cab893e1d3",
    "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.sha256": "b0815a082218d9191e08c23c224d7f6c9dac56775ba5772fd305c2b0c1f25670",
}

STRICT = {
    "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
    "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
    "actual_stable_tree_instantiation": "0/7",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
}


def qstr(x: Q) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def load_result(name: str) -> dict[str, Any]:
    data = strict_json_path(HERE / name)
    result = data.get("result")
    require(isinstance(result, dict), f"manifest result: {name}")
    return result


def verify_frozen_semantics() -> None:
    kac = load_result("cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json")
    require(kac["frozen_measure_space_contract"]["invariant_probability"] ==
            "mu_s=normalized_cos(phi)dr_dphi=normalized_dr_dp", "Sinai density pin")

    tile = load_result("cm2-gate2-round25-product-base-manifest-2026-07-18.json")
    require(tile["candidate_maturity"]["invariant_stable_product_dynamical_layers_certified"] == 0,
            "candidate/invariant guard")
    require(tile["exact_positive_cone_product_tile"]["affine_area_disintegration_only"]
            ["is_conditional_stable_holonomy_SRB_Jacobian"] is False, "affine type guard")

    r59 = load_result("cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json")
    finite = r59["gate2"]["physical_finite_shadow_registry"]
    require(finite["row_count"] == 96 and finite["all_recorded_collision_shadows_empty"] is True,
            "96 collision-shadow rows")
    require(finite["graph_transform_chart_defined_at_every_prefix"] == "NOT_CERTIFIED",
            "chart survival guard")

    tube = load_result("cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json")
    require(tube["fair_dyadic_boundary_tube_theorem"]["asymptotic_rate"] == "O(2^(-d/3))",
            "one-step tube rate")

    r60 = load_result("cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json")
    require(r60["actual_landing_RN_marker_bridge"]["status"].startswith("CERTIFIED_ACTUAL_RN_MARKER"),
            "actual landing marker")
    r62 = load_result("cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json")
    require(r62["actual_branch_RN_covariance"]["status"].startswith("CERTIFIED_EXACT_ACTUAL_TAGGED"),
            "actual branch covariance")

    r65 = load_result("cm2-gate24-round65-actual-product-tree-strong-assembly-frontier-manifest-2026-07-21.json")
    require(r65["actual_product_tree_interface"]["actual_rows_complete"] == "0/7",
            "Round65 actual product-tree state")
    require(r65["standard_Borel_plaque_law_saturation"]["actual_P_eta_zero"] == "NOT_CERTIFIED",
            "Round65 marker guard")


def chart_result() -> dict[str, Any]:
    # Phi(u,s)=(a(s)u,s), with two replay plaques a_s=1 and a_t=3/2.
    a_s, a_t = Q(1), Q(3, 2)
    q_s, q_t = a_s, a_t
    z_s, z_t = q_s, q_t
    rho_s, rho_t = q_s / (z_s * a_s), q_t / (z_t * a_t)
    lam = a_t / a_s
    jac = q_s * z_t / (q_t * z_s)
    require((rho_s, rho_t, lam, jac) == (Q(1), Q(2, 3), Q(3, 2), Q(1)),
            "chart replay values")
    require(jac * rho_t == rho_s / lam, "RN/arclength compatibility")

    q_lo, q_hi, a_lo, a_hi, length = Q(1), Q(3, 2), Q(1), Q(3, 2), Q(1)
    rho_lo = q_lo / (q_hi * length * a_hi)
    rho_hi = q_hi / (q_lo * length * a_lo)
    j_lo = (q_lo / q_hi) ** 2
    j_hi = (q_hi / q_lo) ** 2
    metric_factor = (a_hi / a_lo) ** 3
    require(rho_lo == Q(4, 9) and rho_hi == Q(3, 2), "density envelope")
    require(j_lo == Q(4, 9) and j_hi == Q(9, 4), "RN envelope")
    require(metric_factor == Q(27, 8), "path factor")
    return {
        "physical_invariant_density": "dmu=c*cos(phi)drdphi=c*drdp after p=sin(phi)",
        "product_chart": "Phi:I x S->R; a=|partial_u Phi|, q=c|det DPhi|, Z(s)=int_I q du",
        "conditional_arclength_density": "rho_s=q/(Z(s)*a)",
        "root_coordinate_holonomy": "h_st(Phi(u,s))=Phi(u,t)",
        "arclength_derivative": "lambda_st=a(u,t)/a(u,s)",
        "conditional_RN_factor": "J_st(Phi(u,t))=q(u,s)Z(t)/(q(u,t)Z(s))",
        "compatibility": "J_st(hx)rho_t(hx)=rho_s(x)/lambda_st(x)",
        "bounded_chart_consequence": {
            "hypotheses": "|I|=L_0, 0<q_-<=q<=q_+, 0<a_-<=a<=a_+",
            "rho_bounds": "q_-/(q_+ L_0 a_+)<=rho<=q_+/(q_- L_0 a_-)",
            "lambda_bounds": "a_-/a_+<=lambda<=a_+/a_-",
            "J_bounds": "(q_-/q_+)^2<=J<=(q_+/q_-)^2",
            "metric_path_budget": "F*R*(a_+/a_-)^3<C_p*theta*L",
        },
        "rational_replay": {
            "chart": "Phi(u,s)=(a(s)u,s)",
            "a_s": qstr(a_s), "a_t": qstr(a_t),
            "rho_s": qstr(rho_s), "rho_t": qstr(rho_t),
            "lambda_st": qstr(lam), "J_st": qstr(jac),
            "rho_envelope": [qstr(rho_lo), qstr(rho_hi)],
            "J_envelope": [qstr(j_lo), qstr(j_hi)],
            "metric_path_factor": qstr(metric_factor),
        },
        "round25_affine_chart_is_physical_stable_chart": False,
        "actual_product_chart_common_root_density_bounds": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_CONDITIONAL_DENSITY_RN_ARCLENGTH_CROSSWALK__ACTUAL_CHART_ABSENT",
    }


def crosswalk_result() -> dict[str, Any]:
    align = [(0, 0, Q(1, 2)), (1, 1, Q(1, 2))]
    switch = [(0, 1, Q(1, 2)), (1, 0, Q(1, 2))]

    def marg(rows: list[tuple[int, int, Q]], axis: int) -> list[Q]:
        return [sum((mass for o, s, mass in rows if (o, s)[axis] == k), Q(0))
                for k in (0, 1)]

    require(marg(align, 0) == marg(switch, 0) == [Q(1, 2), Q(1, 2)], "owner marginals")
    require(marg(align, 1) == marg(switch, 1) == [Q(1, 2), Q(1, 2)], "plaque marginals")
    comp_align = sum((m for o, s, m in align if o == s), Q(0))
    comp_switch = sum((m for o, s, m in switch if o == s), Q(0))
    require(comp_align == 1 and comp_switch == 0, "key compatibility split")
    return {
        "required_joint_law": "Lambda on owner records x product coordinates after matching total masses",
        "required_marginals": ["pr_owner#Lambda=nu_*", "(Phi o pr_(u,s))#Lambda=kappa_B"],
        "required_support": "immutable owner/tree/branch/physical-ID keys agree Lambda-a.e.",
        "same_marginals_do_not_determine_key_support": {
            "owner_marginal": ["1/2", "1/2"],
            "plaque_marginal": ["1/2", "1/2"],
            "align_rows": [[o, s, qstr(m)] for o, s, m in align],
            "switch_rows": [[o, s, qstr(m)] for o, s, m in switch],
            "compatible_mass_align": qstr(comp_align),
            "compatible_mass_switch": qstr(comp_switch),
            "immutable_relation": "owner_key=plaque_key",
            "status": "FALSE_BY_EXACT_TWO_COUPLING_SEPARATOR",
        },
        "actual_owner_landing_product_crosswalk": "NOT_CERTIFIED",
        "status": "CERTIFIED_EXACT_CROSSWALK_REQUIREMENT_AND_MARGINAL_NONIMPLICATION",
    }


def marker_result() -> dict[str, Any]:
    weights = [Q(1, 4)] * 4
    sat = [Q(1, 2)] * 4
    varied = [Q(5, 16), Q(7, 16), Q(9, 16), Q(11, 16)]

    def dispersion(values: list[Q]) -> Q:
        return sum((weights[i] * weights[j] * abs(values[i] - values[j])
                    for i in range(4) for j in range(i + 1, 4)), Q(0))

    def median_cost(values: list[Q]) -> Q:
        med = sorted(values)[1]
        return sum((w * abs(v - med) for w, v in zip(weights, values)), Q(0))

    p_sat, d_sat = dispersion(sat), median_cost(sat)
    p_var, d_var = dispersion(varied), median_cost(varied)
    require(sum((w * v for w, v in zip(weights, sat)), Q(0)) == Q(1, 2), "sat mass")
    require(sum((w * v for w, v in zip(weights, varied)), Q(0)) == Q(1, 2), "varied mass")
    require((p_sat, d_sat) == (0, 0), "sat replay")
    require((p_var, d_var) == (Q(5, 64), Q(1, 8)), "varied replay")
    require(p_var < d_var < 2 * p_var, "strict median sandwich")
    return {
        "shared_reference": "flat invariant unit product law, four equal plaques, identity holonomy and identity commuting branch square",
        "same_total_landing_mass": "1/2",
        "stable_completion": {"markers": [qstr(x) for x in sat], "P_eta": "0", "delta_eta": "0"},
        "varying_completion": {"markers": [qstr(x) for x in varied],
                               "P_eta": qstr(p_var), "delta_eta": qstr(d_var),
                               "strict_sandwich": True},
        "conclusion": "explicit invariant density, perfect product geometry and kappa_B<=mu_C do not imply P_eta=0",
        "actual_P_eta_zero": "NOT_CERTIFIED",
        "status": "FALSE_BY_SMOOTH_POSITIVE_SAME_MASS_MARKER_SEPARATOR",
    }


def failure_result() -> dict[str, Any]:
    a, sigma = Q(1, 4), Q(1, 2)
    rows = []
    partial = Q(0)
    for k in range(1, 13):
        bound = a * sigma**k
        partial += bound
        rows.append({"post_prefix_index": k, "first_failure_upper": qstr(bound),
                     "survivor_lower_after_row": qstr(1 - partial)})
    total = a * sigma / (1 - sigma)
    require(total == Q(1, 4) and 1 - total == Q(3, 4), "geometric failure replay")
    return {
        "full_failure_definition": "F_N=S_(N-1)\\S_N includes collision shadow and required graph-transform chart failure",
        "frozen_collision_shadow_rows": 96,
        "all_frozen_collision_shadow_measures": "0",
        "frozen_graph_transform_chart_survival": "NOT_CERTIFIED",
        "actual_full_first_failure_upper_bound_rows": 0,
        "sharp_actual_survivor_lower_bound": "0",
        "sharp_completion": "immediate full chart failure; even optimistically keeping depths 1..96, F_97=S_96",
        "round26_tube_type_guard": "adaptive one-step spatial resolution d has no pinned same-law map or schedule to temporal stable depth N",
        "kac_type_guard": "return-time tail is not a stable-chart first-failure tail",
        "geometric_future_interface": {
            "hypothesis": "eta(F_(96+k))<=A*sigma^k for k>=1 on identical base and keys, 0<sigma<1",
            "conclusion": "eta(S_infinity)>=eta(S_0)-A*sigma/(1-sigma)",
            "sample_A": qstr(a), "sample_sigma": qstr(sigma),
            "sample_rows_first_12": rows,
            "sample_total_failure_upper": qstr(total),
            "sample_survivor_lower": qstr(1 - total),
            "status": "CERTIFIED_EXACT_CONDITIONAL_AND_SHARP_AT_FAILURE_MASS_LEVEL",
        },
        "physical_positive_all_depth_survivor": "NOT_CERTIFIED",
        "status": "CERTIFIED_ZERO_ACTUAL_LOWER_BOUND_AND_SHORTEST_GEOMETRIC_FAILURE_INTERFACE",
    }


def variation_result() -> dict[str, Any]:
    variation_rows = [{"N": n, "marker": "1/2+(1/4)sin(2*pi*N*u)",
                       "range": "[1/4,3/4]", "total_mass": "1/2",
                       "P_eta": "0", "transverse_variation": str(n)}
                      for n in [1, 2, 17, 257, 4096]]
    # q1=x, q2=1-x, tag weights 1 and 2, f=1+x.
    b0, binf, b1 = Q(2), Q(3), Q(3)
    f_bv = Q(5, 2)
    output = Q(37, 6)
    bound = (b0 + binf + b1) * f_bv
    require(bound == 20 and output <= bound, "material BV replay")
    return {
        "zero_defect_unbounded_variation_separator": {
            "shared_geometry": "flat perfect product chart with the same marker on every plaque",
            "rows": variation_rows,
            "conclusion": "smooth invariant density plus P_eta=0 does not uniformly bound transverse BV",
            "status": "FALSE_BY_SMOOTH_SEPARATOR",
        },
        "material_tag_Piola_BV_bridge": {
            "definition": "q_r=b_r*k_r in one fixed material coordinate, tag weights a_r>=1",
            "hypotheses": [
                "B_0=||sum_r a_r|q_r|||_infinity<infinity",
                "B_inf=sum_r a_r||q_r||_infinity<infinity",
                "B_1=sum_r a_r Var(q_r)<infinity",
            ],
            "bound": "sum_r a_r||q_r f||_BV<=(B_0+B_inf+B_1)||f||_BV",
            "sample": {"q": ["x", "1-x"], "tag_weights": [1, 2], "f": "1+x",
                       "B_0": qstr(b0), "B_inf": qstr(binf), "B_1": qstr(b1),
                       "f_BV": qstr(f_bv), "output_tagged_BV": qstr(output),
                       "upper_bound": qstr(bound)},
            "status": "CERTIFIED_CONDITIONAL_FIXED_MATERIAL_BV_MULTIPLIER_BRIDGE",
        },
        "actual_weighted_transverse_variation": "NOT_CERTIFIED",
        "actual_physical_Piola_coefficients_and_remainder": "NOT_CERTIFIED",
        "physical_anisotropic_intertwining_recipient": "NOT_CERTIFIED",
        "status": "CERTIFIED_VARIATION_SEPARATOR_AND_CONDITIONAL_MATERIAL_BRIDGE__PHYSICAL_RECIPIENT_ABSENT",
    }


def actual_interface_result() -> dict[str, Any]:
    rows = [
        [1, "all-depth positive stable base and product-rectangle/tree key", "NOT_CERTIFIED"],
        [2, "collision-SRB outer plaque law and measurable common-root trivialisation", "NOT_CERTIFIED__FORMULA_ONLY"],
        [3, "source/landing stable holonomies with RN and arclength derivatives", "NOT_CERTIFIED__FORMULA_ONLY"],
        [4, "same branch keys and measurable commuting-square family", "PARTIAL_DYNAMIC_KEYS_ONLY"],
        [5, "actual stable marker dispersion P_eta=0", "NOT_CERTIFIED"],
        [6, "actual essential path properness budget", "NOT_CERTIFIED"],
        [7, "weighted variation plus physical strong/Piola recipient", "NOT_CERTIFIED"],
    ]
    return {
        "rows": [{"row": n, "required_object": name, "state": state}
                 for n, name, state in rows],
        "actual_rows_complete": "0/7",
        "formula_rows_are_not_actual_materializations": True,
        "minimum_joint_registry": "one strict-JSON owner/product/source/landing/material registry satisfying the joint law, all-depth, zero-defect, path-budget, variation and strong-recipient rows",
        "status": "AUDITED_0_OF_7__NO_PRODUCT_TREE_PROMOTION",
    }


def technology_result() -> dict[str, Any]:
    return {
        "arXiv_2604_25881v1": "billiard MME from symbolic Hausdorff leaf laws; wrong law for kappa_B=g_B mu_C",
        "arXiv_2604_19671v2": "starts from an already regular Sinai standard family and survivor normalization; does not construct this marked product law or Piola recipient",
        "arXiv_2606_10155v1": "transfer-operator review; no immutable crosswalk or first-failure constants",
        "fresh_official_API_query": "RATE_EXCEEDED__NO_RESULT_PROMOTED",
        "wrong_law_or_smooth_flow_promoted": False,
        "external_theorem_promoted": False,
        "status": "AUDITED_NO_NEW_SAME_LAW_SAME_RECIPIENT_TECHNOLOGY",
    }


def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    verify_frozen_semantics()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {"append_only": True, "old_artifacts_modified": False,
                       "pinned_files": dict(PINS), "external_theorem_promoted": False},
        "sinai_density_product_chart": chart_result(),
        "owner_landing_joint_crosswalk": crosswalk_result(),
        "stable_marker_saturation": marker_result(),
        "all_depth_first_failure": failure_result(),
        "weighted_variation_and_strong_recipient": variation_result(),
        "actual_product_tree_interface": actual_interface_result(),
        "latest_technology_boundary": technology_result(),
        "strict_status": dict(STRICT),
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(verifier.is_file() and not verifier.is_symlink() and verifier.parent == HERE,
            "verifier file")
    require(REPORT.is_file() and not REPORT.is_symlink() and REPORT.resolve().parent == HERE,
            "report file")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "pins": dict(PINS),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "report_sha256": sha256_path(REPORT),
        "result": result,
        "verdict": result["strict_status"],
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2, allow_nan=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    args = parser.parse_args()
    try:
        data = build_manifest(args.verifier)
        payload = render(data)
        if args.write_manifest:
            target = args.write_manifest.resolve()
            require(target.parent == HERE and target.name == MANIFEST.name, "manifest output")
            target.write_text(payload, encoding="utf-8")
            print(f"WROTE_MANIFEST: {target}")
            return 0
        if args.manifest_json:
            print(payload, end="")
            return 0
        if args.audit:
            print("AUDIT: PASS")
            print(f"PINNED_FILES: {len(PINS)}/{len(PINS)}")
            print("RESULT_SHA256:", data["result"]["internal_replay_digest"])
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, IndexError,
            ArithmeticError) as exc:
        print(f"ROUND66_GATE24_CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1
    print("GATE2: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
