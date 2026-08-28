#!/usr/bin/env python3
"""Round-67 Gate-2/4 actual-root, stable-tail and variation frontier."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round67_common import (
    CertError, digest, require, sha256_path, strict_json_path, validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate24.round67.actual-root-stable-tail-variation-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate24-round67-actual-root-stable-tail-variation-frontier"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_gate24_round67_actual_root_stable_tail_variation_frontier_verifier.py"

PINS = {
    "cm2_round67_common.py": "8e9d5959b4ce7d6012773e882d048a14e24c5bcae5d80dfc0b131d5ae96f7110",
    "cm2-sixty-sixth-direct-assault-2026-07-21.md": "690cfeb13108314a3a05f5e4cd342d573c41e66551464ebf7f4b5576f374b811",
    "cm2-sixty-sixth-direct-assault-manifest-2026-07-21.sha256": "b437761fb84aa431e468af587e2207adadf6e0a996ee593a93df467147be3b5d",
    "cm2-round66-independent-core-frontier-audit-2026-07-21.md": "68d9b65f843c6e35e9f8c5e6954fb76e87970fc9bc558e691cecaafeb9850ebd",
    "cm2-round66-independent-core-frontier-audit-manifest-2026-07-21.json": "b67b76e52d073989fac6fb41eaf3e49167aa1e166d32003c72129e08ec6d46b3",
    "cm2-round66-independent-core-frontier-audit-manifest-2026-07-21.sha256": "6d09b81b683464dcf45815ed9e98635c6c3a94087c19b0e4528eaf4c1659175e",
    "cm2-gate24-round66-collision-srb-product-variation-frontier-assault-2026-07-21.md": "13341aaa40ccc155b85119c457b12a5e09fed43fa618ed0aee280bef0af68b27",
    "cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.json": "be98266945e3e6bd7fee0bf27f49a3282dc41f67e95f74b0c41c041d0cd4bf94",
    "cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.sha256": "de30d5514982930c9dd485313e09a6eb668c2e3dbc1da05d4507ae6a032f1d20",
    "cm2-gate13-round66-same-representative-material-trace-frontier-assault-2026-07-21.md": "6d37428dde6b8360d759554a9bcd2bfeb91b0c67c0ab3bcc98d91d850fa49278",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json": "11bb7ba12e3302a547893dae3a897efc5a66223bbc2cf740bb6f7b5e53882224",
    "cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.sha256": "4d38f3145099b2cd4222930d32c88dd7ba6bc9797def4673fc9ea00415f3b38e",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-assault-2026-07-21.md": "9b8512389c8ede4c6b59a029565bc314f10502ec9339094036f13f33185463a2",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.json": "adc2654ed27fa62c83dd9d64ddce09832e173f50d518c464007d9bc320d6294f",
    "cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.sha256": "1122a6b11415e5f070ec4a86faa6d78a0a67a30ae836c288e3a732f1c0fa51f3",
    "cm2-gate2-round25-product-base-assault-2026-07-18.md": "db75a6a8741d435182a1e0d0510e06d1b75b15eaba3d0c26e090e9c5990664e6",
    "cm2-gate2-round25-product-base-manifest-2026-07-18.json": "8045c36fb14c69a145be4ebf4cd33ae11d55fd77f4591b91782f13516c80679b",
    "cm2-gate2-round25-product-base-manifest-2026-07-18.sha256": "4c1ab35de924739bb391aa594861ae0f2c3264d93a42073cc4868de9dec082fc",
    "cm2-gate2-actual-stable-plaque-continuation-2026-07-15.md": "3f1852862ea5192d4ab350c2c67dc874d5d69634856ee874f350fe2ca038e37d",
    "cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json": "1bfc3ea9f5eb587b41a94ba4fd808c03c309389269f8d5e903f9bfce09a4f871",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-assault-2026-07-20.md": "43f50426abfc92e041903af4d4eb6a416d686ea7ad25ad0f013bb56cd9f4110d",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json": "16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466",
    "cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.sha256": "985910708fe715d0c891cd6a288b37a5e1b88530db858a712e7e82e80cbb4b71",
    "cm2-gate34-collision-srb-kac-return-baseline-assault-2026-07-18.md": "87ea865ba97567cbe5f3d3029d9be1a6a6d58cd49f390f5558fdbab26c82b243",
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a",
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.sha256": "c6acef0c867602a8bccfbfc052b13cecb60b8216d16c926cdd707645f3a30863",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-assault-2026-07-20.md": "88f042ed434f6199123a5f164385572dabfcde0af13a8d6b9d7ca1385079d00f",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json": "08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3",
    "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.sha256": "4d7c3f06e1671319482c064ec3ea817562567202b111fd014434b7be0a460fac",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-assault-2026-07-21.md": "4acca86b074ce3f6792aa04625c9576d2affeacb0ad9d7cdeb09cabd08d45b00",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json": "e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256": "b94df87ba8362827bb1115f474c0beec59f887325e8db58b55a9020bf99ae6bc",
}

STRICT = {
    "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
    "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
    "actual_stable_tree_instantiation": "0/7",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
}


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def load_result(name: str) -> dict[str, Any]:
    data = strict_json_path(HERE / name)
    result = data.get("result")
    require(isinstance(result, dict), f"result object: {name}")
    return result


def verify_frozen_semantics() -> None:
    r25 = load_result("cm2-gate2-round25-product-base-manifest-2026-07-18.json")
    anchor = r25["shared_physical_anchor_registry"]
    require(anchor["physical_branch_class"] == "RETURN_AT_1_INNER" and
            anchor["whole_tile_has_same_unique_next_collision_and_returns_to_C24_at_time_1"] is True,
            "Round25 physical anchor")
    require(r25["candidate_maturity"]["invariant_stable_product_dynamical_layers_certified"] == 0,
            "Round25 stable guard")

    r15 = strict_json_path(HERE / "cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json")
    layers = r15["proved_layers"]
    require(layers["actual_stable_plaque_v0_crossing"] is True and
            layers["positive_width_actual_plaque_96_word_strip"] is True and
            layers["second_branch_stable_saturated"] is False,
            "Round15 96-word anchor")

    r59 = load_result("cm2-gate123-round59-physical-formula-shadow-dini-frontier-manifest-2026-07-20.json")
    shadows = r59["gate2"]["physical_finite_shadow_registry"]
    require(shadows["row_count"] == 96 and
            shadows["all_recorded_collision_shadows_empty"] is True and
            shadows["graph_transform_chart_defined_at_every_prefix"] == "NOT_CERTIFIED",
            "Round59 collision-shadow guard")

    r66 = load_result("cm2-gate24-round66-collision-srb-product-variation-frontier-manifest-2026-07-21.json")
    require(r66["actual_product_tree_interface"]["actual_rows_complete"] == "0/7" and
            r66["all_depth_first_failure"]["actual_full_first_failure_upper_bound_rows"] == 0,
            "Round66 Gate24 state")

    g13 = load_result("cm2-gate13-round66-same-representative-material-trace-frontier-manifest-2026-07-21.json")
    require(g13["gate3"]["physical_compact_interior_atlas"]["status"] ==
            "CERTIFIED_LOCAL",
            "Round66 material atlas")

    registry = load_result("cm2-round66-immutable-registry-junction-tree-positive-potential-frontier-manifest-2026-07-21.json")
    require(registry["physical_root_equivalence"]["actual_cm2_graph_supported_root"] ==
            "NOT_CERTIFIED", "Round66 global-root guard")

    kac = load_result("cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json")
    require(kac["frozen_measure_space_contract"]["invariant_probability"] ==
            "mu_s=normalized_cos(phi)dr_dphi=normalized_dr_dp", "collision law")

    r60 = load_result("cm2-gate4-round60-physical-rn-good-bad-assembly-frontier-manifest-2026-07-20.json")
    require(r60["actual_landing_RN_marker_bridge"]["status"].startswith("CERTIFIED_ACTUAL_RN_MARKER"),
            "landing marker")
    r62 = load_result("cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json")
    require(r62["actual_branch_RN_covariance"]["status"].startswith("CERTIFIED_EXACT_ACTUAL_TAGGED"),
            "branch covariance")


def actual_root_result() -> dict[str, Any]:
    s_lo, s_hi = Q(-3, 1600), Q(-1, 640)
    h = Q(1, 25600)
    t0, p0, radius = Q(-4479, 6400), Q(-31, 1600), Q(9, 25)
    require(s_hi - s_lo == Q(1, 3200), "s slab width")

    # A=D(t,p)/D(u,v).
    a11, a12, a21, a22 = Q(1), Q(1), Q(3, 2), Q(-3, 2)
    det = a11 * a22 - a12 * a21
    gram_diag = a11 * a11 + a21 * a21
    gram_off = a11 * a12 + a21 * a22
    require(det == -3 and gram_diag == Q(13, 4) and gram_off == Q(-5, 4),
            "affine derivative")
    singular_squared = [gram_diag + gram_off, gram_diag - gram_off]
    require(singular_squared == [Q(2), Q(9, 2)], "singular values")

    t_abs_lo, t_abs_hi = Q(8957, 12800), Q(8959, 12800)
    require(abs(t0 + 2 * h) == t_abs_lo and abs(t0 - 2 * h) == t_abs_hi,
            "tile t range")
    a2_lo = radius * radius / (1 - t_abs_lo * t_abs_lo) + Q(9, 4)
    a2_hi = radius * radius / (1 - t_abs_hi * t_abs_hi) + Q(9, 4)
    ratio2 = a2_hi / a2_lo
    require(ratio2 > 1 and ratio2**3 < Q(101, 100)**2, "metric path factor")

    fixed_mass_lower = Q(27, 4096000000)
    parameter_fraction = (s_hi - s_lo) / Q(1, 200)
    averaged_mass_lower = fixed_mass_lower * parameter_fraction
    require(parameter_fraction == Q(1, 16) and
            averaged_mass_lower == Q(27, 65536000000), "positive root mass")

    return {
        "root": {
            "Omega_0": "S x I x V",
            "S": [qstr(s_lo), qstr(s_hi)],
            "I_equals_V": [qstr(-h), qstr(h)],
            "source_collision_map": "t=t0+u+v; p=p0+(3/2)(u-v); r=R_G*asin(t)",
            "t0": qstr(t0), "p0": qstr(p0), "R_G": qstr(radius),
            "pullback_collision_density_up_to_normalization": "3*R_G/sqrt(1-t(u,v)^2) ds du dv",
            "fixed_parameter_mass_strict_lower": qstr(fixed_mass_lower),
            "parameter_averaged_mass_strict_lower": qstr(averaged_mass_lower),
        },
        "graph_supported_maps": {
            "owner": "frozen Round25 atom/s/source core/RETURN_AT_1_INNER/half-open owner",
            "source": "physical Gray collision coordinate (r,p)",
            "landing": "T_s(source) in frozen destination core",
            "affine_product": "(u,v)",
            "material": "s/source/destination/depth-1/persistent branch",
            "support": "joint deterministic pushforward is supported on every declared equality graph",
        },
        "scope_guards": {
            "is_Round50_58_owner_law": False,
            "is_invariant_stable_product": False,
            "is_crosswalked_to_common_landing_marker": False,
            "is_global_CM2_root": False,
        },
        "affine_chart": {
            "D_t_p_over_u_v": [[qstr(a11), qstr(a12)], [qstr(a21), qstr(a22)]],
            "determinant": qstr(det),
            "squared_singular_values": [qstr(x) for x in singular_squared],
            "exact_q": "q(u,v)=3*R_G/sqrt(1-t^2)",
            "exact_a": "a(u,v)=sqrt(R_G^2/(1-t^2)+9/4)",
            "exact_Z": "Z(v)=3*R_G*(asin(t0+h+v)-asin(t0-h+v))",
            "conditional_density": "rho_v=q/(Z(v)*a)",
            "candidate_holonomy_arclength_derivative": "lambda_(v,w)=a(u,w)/a(u,v)",
            "candidate_holonomy_RN": "J_(v,w)=q(u,v)Z(w)/(q(u,w)Z(v))",
            "compatibility": "J_(v,w)rho_w=rho_v/lambda_(v,w)",
            "t_absolute_range": [qstr(t_abs_lo), qstr(t_abs_hi)],
            "a_squared_bounds": [qstr(a2_lo), qstr(a2_hi)],
            "a_ratio_squared": qstr(ratio2),
            "metric_factor_strict_upper": "101/100",
            "sufficient_candidate_budget": "101*F*R<100*C_p*theta*L",
        },
        "C1_upgrade": {
            "hypothesis": "same-key chart Psi=A(u,v)+b+E with Lip(E)=epsilon<sqrt(2), plus physical graph-transform plaque semantics",
            "conclusion": "Psi is injective on the convex tile with lower Lipschitz constant sqrt(2)-epsilon",
            "actual_epsilon_bound": "NOT_CERTIFIED",
        },
        "status": "CERTIFIED_LOCAL_ACTUAL_GRAPH_SUPPORTED_OWNER_COLLISION_LANDING_MATERIAL_PRE_REGISTRY_AND_EXACT_AFFINE_SRB_CHART__STABLE_SEMANTICS_ABSENT",
    }


def distinct_anchor_result() -> dict[str, Any]:
    return {
        "Round25_root": {
            "positive_width": True,
            "exact_collision_disintegration": True,
            "same_unique_time_one_owner": True,
            "actual_invariant_stable_plaque_family": False,
        },
        "Round15_59_root": {
            "actual_stable_plaque_crossing": True,
            "positive_width_strict_96_word_strip": True,
            "collision_shadow_zero_rows": 96,
            "stable_saturation": False,
            "product_quotient": False,
        },
        "same_immutable_root_crosswalk": "NOT_CERTIFIED",
        "may_combine_exact_density_with_96_word_stable_crossing": False,
        "status": "CERTIFIED_TWO_DISTINCT_PHYSICAL_PARTIAL_ROOTS__NO_IDENTIFIER_JOIN",
    }


def hazard_result() -> dict[str, Any]:
    checkpoints = [1, 2, 8, 32, 96, 256]
    summable_rows = []
    divergent_rows = []
    prod_sum = Q(1)
    prod_div = Q(1)
    next_checkpoint = set(checkpoints)
    for n in range(1, max(checkpoints) + 1):
        hs = Q(1, (n + 1) ** 2)
        hd = Q(1, n + 1)
        prod_sum *= 1 - hs
        prod_div *= 1 - hd
        if n in next_checkpoint:
            require(prod_sum == Q(n + 2, 2 * (n + 1)), "summable hazard product")
            require(prod_div == Q(1, n + 1), "divergent hazard product")
            summable_rows.append({"N": n, "product": qstr(prod_sum)})
            divergent_rows.append({"N": n, "product": qstr(prod_div)})

    return {
        "definition": "F_N=S_(N-1)\\S_N; h_N=eta(F_N)/eta(S_(N-1)) while eta(S_(N-1))>0",
        "finite_identity": "eta(S_N)=eta(S_0)*product_(n<=N)(1-h_n)",
        "positive_all_depth_iff": "every h_n<1 and sum_n h_n<infinity",
        "summable_replay": {
            "hazard": "h_n=1/(n+1)^2",
            "closed_product": "product_(n<=N)(1-h_n)=(N+2)/(2(N+1))",
            "limit": "1/2",
            "rows": summable_rows,
        },
        "divergent_replay": {
            "hazard": "h_n=1/(n+1)",
            "closed_product": "product_(n<=N)(1-h_n)=1/(N+1)",
            "limit": "0",
            "rows": divergent_rows,
        },
        "lexicographic_full_failure_components": [
            "collision_singularity", "graph_transform_or_domain", "registry_or_key_loss"
        ],
        "actual_collision_component_zero_rows": 96,
        "actual_full_conditional_hazard_rows": 0,
        "sharp_actual_survivor_lower_bound": "0",
        "physical_positive_all_depth_survivor": "NOT_CERTIFIED",
        "shortest_future_interface": "same-root h_n<=b_n<1 with sum_n b_n<infinity",
        "status": "CERTIFIED_EXACT_CONDITIONAL_HAZARD_IFF_AND_SHARP_ZERO_ACTUAL_BOUND",
    }


def marker_variation_result() -> dict[str, Any]:
    return {
        "stable_saturation": {
            "same_root_criterion": "g(u,v)=g_bar(u) almost everywhere",
            "equivalent_rows": ["P_eta=0", "zero stable marker defects on a spanning holonomy tree"],
            "pre_registry_carries_actual_g_B": False,
            "actual_P_eta_zero": "NOT_CERTIFIED",
        },
        "candidate_budget": {
            "metric_factor": "(a_+/a_-)^3<101/100",
            "sufficient_strict_row": "101*F*R<100*C_p*theta*L",
            "actual_F_R_theta_L": "NOT_CERTIFIED",
            "physical_budget_paid": False,
        },
        "zero_defect_implies_BV": False,
        "status": "CERTIFIED_EXACT_SAME_ROOT_MARKER_AND_CANDIDATE_BUDGET_INTERFACE__ACTUAL_MARKER_ABSENT",
    }


def strong_recipient_result() -> dict[str, Any]:
    length = Q(1)
    q1_bv = Q(3, 2)  # ||x||_1+Var(x)
    q2_bv = Q(3, 2)  # ||1-x||_1+Var(1-x)
    weights = [1, 2]
    s_q = weights[0] * q1_bv + weights[1] * q2_bv
    lower, upper = s_q / length, 2 * max(Q(1), 1 / length) * s_q
    require((s_q, lower, upper) == (Q(9, 2), Q(9, 2), Q(9)), "BV multiplier replay")
    remainder_rows = []
    for n in [2, 4, 16, 64, 256]:
        quotient = s_q / n
        remainder_rows.append({"s": qstr(Q(1, n)),
                               "weighted_BV_remainder_over_abs_s": qstr(quotient)})
    return {
        "recipient": "Y=ell^1_a(BV(I)); ||f||_BV=||f||_1+Var(f)",
        "coefficient_ledger": "S_q=sum_r a_r||q_r||_BV",
        "boundedness_iff": "M_q:BV(I)->Y bounded iff S_q<infinity",
        "norm_bounds": "S_q/|I|<=||M_q||<=2*max(1,|I|^-1)*S_q",
        "moving_family": {
            "expansion": "q_r(s)=q_r(0)+s*qdot_r+R_r(s)",
            "operator_norm_differentiability_iff": "sum_r a_r||R_r(s)||_BV=o(|s|)",
            "replay": {
                "I": "[0,1]", "q": ["x", "1-x"], "weights": weights,
                "S_q": qstr(s_q), "operator_norm_bounds": [qstr(lower), qstr(upper)],
                "quadratic_remainder_rows": remainder_rows,
            },
        },
        "physical_local_depth96_material_atlas": "CERTIFIED_PINNED_C2_COMPACT_CORE_WITH_LOCAL_O(s^2)_PIOLA_REMAINDER",
        "same_root_as_Round25_pre_registry": False,
        "actual_global_weighted_BV_coefficient_sum": "NOT_CERTIFIED",
        "actual_anisotropic_intertwining": "NOT_CERTIFIED",
        "actual_all_depth_strong_Piola_recipient": "NOT_CERTIFIED",
        "status": "CERTIFIED_WEIGHTED_BV_MULTIPLIER_AND_PIOLA_REMAINDER_IFF__LOCAL_PHYSICAL_CORE_ONLY",
    }


def actual_interface_result() -> dict[str, Any]:
    rows = [
        [1, "all-depth positive stable base and product-rectangle/tree key", "NOT_CERTIFIED__LOCAL_PRE_REGISTRY_ONLY"],
        [2, "collision-SRB outer plaque law and measurable common-root trivialisation", "PARTIAL_ACTUAL_AFFINE_ROOT__NO_STABLE_PLAQUE_LAW"],
        [3, "source/landing stable holonomies with RN and arclength derivatives", "NOT_CERTIFIED__SAME_ROOT_CANDIDATE_FORMULAS_ONLY"],
        [4, "same branch keys and measurable commuting-square family", "PARTIAL_ONE_STEP_DYNAMIC_GRAPH_ONLY"],
        [5, "actual stable marker dispersion P_eta=0", "NOT_CERTIFIED__MARKER_NOT_CROSSWALKED"],
        [6, "actual essential path properness budget", "NOT_CERTIFIED__CANDIDATE_METRIC_FACTOR_ONLY"],
        [7, "weighted variation plus physical strong/Piola recipient", "PARTIAL_LOCAL_DEPTH96_PHYSICAL_CORE__NO_GLOBAL_SAME_ROOT_RECIPIENT"],
    ]
    return {
        "rows": [{"row": n, "required_object": name, "state": state} for n, name, state in rows],
        "actual_rows_complete": "0/7",
        "partial_rows": [2, 4, 7],
        "formula_or_local_rows_are_not_complete_materializations": True,
        "status": "AUDITED_0_OF_7__LOCAL_ACTUAL_PRE_REGISTRY_WITHOUT_STABLE_PRODUCT_PROMOTION",
    }


def technology_result() -> dict[str, Any]:
    return {
        "official_search_date": "2026-07-21",
        "arXiv_2502_07765v2": "sequential-system CLT with sequential dispersing billiard applications; no stable common marker root or moving-boundary Piola remainder",
        "arXiv_2104_06947v3": "projective cones for sequential dispersing billiards; starts from standard-family structure and does not construct this root/marker/recipient",
        "arXiv_2604_25881v1": "billiard measure of maximal entropy; wrong law for collision-SRB marker",
        "arXiv_2402_02496v2": "local product structure for smooth closed-manifold diffeomorphisms; wrong singular interface",
        "external_theorem_promoted": False,
        "wrong_law_promoted": False,
        "status": "AUDITED_NO_NEW_SAME_ROOT_SAME_LAW_STRONG_RECIPIENT_TECHNOLOGY",
    }


def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    verify_frozen_semantics()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {"append_only": True, "old_artifacts_modified": False,
                       "pinned_files": dict(PINS), "external_theorem_promoted": False},
        "actual_graph_supported_pre_registry": actual_root_result(),
        "distinct_physical_anchor_audit": distinct_anchor_result(),
        "all_depth_conditional_hazard": hazard_result(),
        "marker_saturation_and_budget": marker_variation_result(),
        "fixed_material_weighted_BV_recipient": strong_recipient_result(),
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
        print(f"ROUND67_GATE24_CERTIFICATE_ERROR: {exc}", file=sys.stderr)
        return 1
    print("GATE2: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
