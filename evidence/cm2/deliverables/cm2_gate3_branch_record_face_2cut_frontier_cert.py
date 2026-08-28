#!/usr/bin/env python3
"""Gate-3 branch-record, face-product, and two-cutoff frontier.

This certificate closes three pieces that are genuinely implied by the
frozen pilot evidence.

* The limiting corrected 64-row graph current is completed to the exact
  face--product centered cluster required by MT_DQ.  Its actual marginals
  are used, its scalar mass is zero, and explicit typed norm bounds follow
  from the certified graph-current TV bound.
* The query-independent product depth law gives an exact positive
  pre-cancellation auxiliary tail after the parent-normalization charge.
  Combining the certified finite-parameter affine recovery clock with that
  law gives exponential auxiliary depth/recovery uniform integrability on
  the complete window |s|<=1/400.
* The recovery moment gives a summable two-time *clock* array by a Markov
  split and a proper-family coupling rate.  This is only the clock algebra:
  applying it to the physical current still requires recordwise current
  matching, propagated-q domination, a physical test lift, and finite-s
  uniformity.

Two exact countermodels guard the remaining logical boundary.  Pointwise
depth-one DQ plus a formal telescope does not imply fixed-time DQ when an
iterated source leaves the strong source space.  Fixed-(m,n) FACE_2CUT
tails do not imply a summable product-time majorant.

Accordingly this artifact does not certify a component-indexed iterated
moving atlas, dynamic branch-record MT_DQ, physical FACE_2CUT,
FACE_TIME_CM2/REC, or Gate 3.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent
V52_MANIFEST = HERE / "cm2-v52-manifest.sha256"
DQ_MANIFEST = HERE / "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
TELESCOPE_MANIFEST = (
    HERE / "cm2-gate3-moving-test-telescope-frontier-manifest-2026-07-16.json"
)
PRODUCT_MANIFEST = (
    HERE / "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
)
RECOVERY_MANIFEST = (
    HERE / "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
)
FINITE_S_RECOVERY_MANIFEST = (
    HERE / "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], ...]:
    dq = json.loads(DQ_MANIFEST.read_text(encoding="utf-8"))
    telescope = json.loads(TELESCOPE_MANIFEST.read_text(encoding="utf-8"))
    product = json.loads(PRODUCT_MANIFEST.read_text(encoding="utf-8"))
    recovery = json.loads(RECOVERY_MANIFEST.read_text(encoding="utf-8"))
    finite_recovery = json.loads(
        FINITE_S_RECOVERY_MANIFEST.read_text(encoding="utf-8")
    )
    v52_lines = V52_MANIFEST.read_text(encoding="utf-8").splitlines()
    assert any(
        line.startswith(
            "e4fd6c74c4be53ec97287b747e792ec8c32f9cd184cff05047189472481c5daa"
        )
        and line.endswith("deliverables/cm2-bridge-note-v52.tex")
        for line in v52_lines
    )
    assert dq["verdict"]["complete_depth_one_fixed_gauge_DQ"] == "CERTIFIED"
    assert telescope["verdict"][
        "fixed_time_noncommutative_DQ_telescope"
    ] == "CERTIFIED"
    assert telescope["verdict"][
        "dynamic_branch_record_full_MT_DQ"
    ] == "NOT_CERTIFIED"
    assert product["verdict"]["supercritical_depth_tail_and_E_2K"] == "CERTIFIED"
    assert recovery["verdict"]["controlled_s0_stopped_parent_recovery"] == "CERTIFIED"
    assert finite_recovery["verdict"][
        "uniform_one_time_finite_s_recovery"
    ] == "CERTIFIED"
    finite_limits = finite_recovery["result"]["scope_limits"]
    assert finite_limits["uniform_one_time_finite_s_stopped_parent_recovery"] is True
    assert finite_limits[
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas"
    ] is False
    assert finite_limits["common_branch_record_MT_DQ"] is False
    return dq, telescope, product, recovery, finite_recovery


def limiting_face_product_cluster(dq: dict[str, Any]) -> dict[str, Any]:
    result = dq["result"]
    envelope = result["uniform_finite_measure_envelope"]
    pairing = result["exact_Jx_scalar_pairing"]
    tv = Q(envelope["global_event_current_TV_upper_bound"])
    scalar = Q(pairing["global_signed_scalar_coarea_mass"])
    assert tv == Q(16128, 5)
    assert scalar == 0
    product_bound = 2 * tv + abs(scalar)
    cluster_bound = tv + product_bound
    assert product_bound == Q(32256, 5)
    assert cluster_bound == Q(48384, 5)
    return {
        "limiting_graph_current": "J_V on M_minus x M_plus from the corrected 64-row current",
        "graph_current_unnormalized_TV_upper": str(tv),
        "common_probability_normalization": (
            "multiply every displayed current norm bound by Z_N^-1"
        ),
        "actual_marginals": "m_V^-=(pr_-)_*J_V; m_V^+=(pr_+)_*J_V",
        "each_marginal_unnormalized_TV_upper": str(tv),
        "scalar_mass_c_V": str(scalar),
        "product_current_formula": (
            "P_V=-m_V^- tensor mu_0-mu_0 tensor m_V^+"
        ),
        "product_current_unnormalized_typed_norm_upper": str(product_bound),
        "centered_cluster_formula": "D_cur J_V=J_V+P_V",
        "centered_cluster_unnormalized_typed_sum_norm_upper": str(cluster_bound),
        "both_cluster_marginals_are_exactly_zero": True,
        "product_pairing_with_two_individually_centered_tests_is_zero": True,
        "cluster_pairing_equals_graph_pairing_on_centered_endpoint_tests": True,
        "uses_actual_marginals_not_substitute_measures": True,
        "limiting_s0_face_product_cluster": "CERTIFIED",
        "finite_s_face_product_cluster_convergence": False,
    }


def auxiliary_depth_rows(maximum_depth: int = 64) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for depth in range(maximum_depth + 1):
        weight = Q(3, 4) * Q(1, 4**depth)
        atom_count = 1 << depth
        atom_joint_mass = weight * Q(1, atom_count)
        parent_cost = atom_count
        charged_atom_mass = atom_joint_mass * parent_cost
        charged_level_mass = charged_atom_mass * atom_count
        expected = Q(3, 4) * Q(1, 2**depth)
        assert charged_level_mass == expected
        rows.append({
            "depth_K": depth,
            "depth_probability": str(weight),
            "atom_count": atom_count,
            "one_atom_joint_mass_coefficient": str(atom_joint_mass),
            "parent_normalization_cost": parent_cost,
            "charged_level_mass_coefficient": str(charged_level_mass),
        })
    total = sum((Q(3, 4) * Q(1, 2**k) for k in range(512)), Q(0))
    assert Q(3, 2) - total == Q(3, 2**513)
    return rows, {
        "parameter_window": "|s|<=1/400",
        "controlled_depth_is_auxiliary_K_not_physical_word_depth_ell": True,
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas": False,
        "positive_charged_level_mass": "a_K=2^K*w_K=(3/4)*2^-K",
        "total_parent_normalization_charge": "sum_K a_K=3/2",
        "strict_tail_after_L": "sum_(K>L) a_K=(3/4)*2^-L",
        "bare_depth_return_exponent": "log(4)",
        "parent_charge_growth_exponent": "log(2)",
        "bare_net_auxiliary_depth_exponent": "log(2)>0",
        "checked_depth_range": [0, maximum_depth],
        "depth_rows_sha256": canonical_digest(rows),
    }


def auxiliary_recovery_uniform_integrability(
    finite_recovery: dict[str, Any],
) -> dict[str, Any]:
    result = finite_recovery["result"]
    configuration = result["uniform_configuration_and_recovery"]
    path = configuration["compact_configuration_path"]
    atom = configuration["one_time_atom_typing"]
    theorem = configuration["uniform_recovery_theorem"]
    assert path["parameter_window"] == "|s|<=1/400"
    assert theorem["two_orientation_recovery_clock"] == (
        "R_fw+R_rev<=2*A0+2*A1*K"
    )
    assert theorem["uniform_depth_recovery_moment"] == (
        "for 0<gamma<log(2)/(2*A1), "
        "E[2^K exp(gamma(R_fw+R_rev))]<infinity"
    )
    assert theorem["constants_uniform_in_s_and_orientation"] is True
    assert theorem["controlled_one_time_finite_s_stopped_parent_recovery"] is True
    assert atom[
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas"
    ] is False
    assert atom["uniform_recovery_is_not_common_branch_record_MT_DQ"] is True
    return {
        "parameter_window": "|s|<=1/400",
        "certified_input": (
            "uniformly in |s|<=1/400, R_fw+R_rev<=2*A0+2*A1*K"
        ),
        "admissible_exponent": "choose 0<gamma<log(2)/(2*A1)",
        "charged_level_bound": (
            "(3/4)*exp(2*gamma*A0)*(exp(2*gamma*A1)/2)^K"
        ),
        "net_depth_recovery_exponent": "log(2)-2*gamma*A1>0",
        "strict_tail_after_L": (
            "<=(3/4)*exp(2*gamma*A0)*r^(L+1)/(1-r), "
            "r=exp(2*gamma*A1)/2<1"
        ),
        "finite_moment": (
            "sup_(|s|<=1/400) E_s[2^K*exp(gamma*(R_fw+R_rev))]<infinity"
        ),
        "uniform_finite_s_auxiliary_depth_recovery_tail": "CERTIFIED",
        "moving_dyadic_endpoints_move_with_u_e_s": True,
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas": False,
        "uniform_recovery_is_not_common_branch_record_MT_DQ": True,
        "physical_face_word_domination": False,
        "physical_word_depth_identified_with_K": False,
    }


def clock_only_two_time_split() -> dict[str, Any]:
    # Replay the exact count of lattice pairs with max(m,n)=N.
    shells = []
    cumulative = 0
    for depth in range(65):
        count = 1 if depth == 0 else 2 * depth + 1
        cumulative += count
        assert cumulative == (depth + 1) ** 2
        shells.append({
            "N=max(m,n)": depth,
            "ordered_pair_count": count,
            "cumulative_pair_count": cumulative,
        })
    return {
        "parameter_window": "|s|<=1/400",
        "moment_input": (
            "M_gamma=sup_(|s|<=1/400) "
            "E_s[2^K*exp(gamma*(R_fw+R_rev))]<infinity"
        ),
        "long_side_clock_tail": (
            "sup_s E_s[2^K*1_{R_o>delta*N}]"
            "<=M_gamma*exp(-gamma*delta*N), o=fw,rev"
        ),
        "proper_core_clock_factor": (
            "on R_o<=delta*N, exp(-c_mix*(N-R_o)) "
            "<=exp(-c_mix*(1-delta)*N)"
        ),
        "uniform_coupling_hypothesis": (
            "given one c_mix>0 uniform in |s|<=1/400 for the matched "
            "proper-family current"
        ),
        "balanced_delta": "delta=c_mix/(gamma+c_mix)",
        "clock_rate": "kappa=gamma*c_mix/(gamma+c_mix)>0",
        "max_time_array": "C*exp(-kappa*max(m,n))",
        "exact_double_sum_formula": (
            "sum_(m,n>=0) x^max(m,n)=(1+x)/(1-x)^2, x=exp(-kappa)<1"
        ),
        "clock_array_is_product_time_summable": True,
        "clock_array_uniform_for_abs_s_at_most_1_over_400": True,
        "same_s_K_j_record_has_both_oriented_recovery_clocks_uniformly": True,
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas": False,
        "physical_signed_proper_family_factorization": False,
        "restrictionwise_propagated_q_domination": False,
        "physical_test_norm_lift": False,
        "clock_only_not_FACE_TIME_REC": True,
        "pair_shell_rows_sha256": canonical_digest(shells),
    }


def branch_source_countermodel() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    for index in range(2, 65):
        s = Q(1, index)
        x_coordinate = Q(1, index)
        a_on_x = index * x_coordinate
        assert s * index == 1
        assert a_on_x == 1
        rows.append({
            "index_k": index,
            "s_k": str(s),
            "x_k": str(x_coordinate),
            "norm_Ak_x": str(a_on_x),
            "norm_Ak_e1": "0",
            "norm_iterated_DQ_on_e1": "1",
        })
    return rows, {
        "spaces": (
            "X=l2; Y={y:sum k^2|y_k|^2<infinity} continuously embedded in X"
        ),
        "operators": (
            "x=(1/k); P0 z=z_1*x; A_k z=k*z_k*e_1; "
            "s_k=1/k; P_(s_k)=P0+s_k*A_k"
        ),
        "uniform_operator_bound_on_X": (
            "sup_k ||P_(s_k)||<=||x||_2+1<infinity"
        ),
        "strong_continuity_on_X": (
            "||(P_(s_k)-P0)z||=|z_k|->0 for each z in X"
        ),
        "depth_one_DQ_on_fixed_strong_sources": (
            "||A_k y||=|k*y_k|->0 for every y in Y"
        ),
        "strong_source_not_invariant": (
            "P0 e_1=x notin Y because sum k^2|x_k|^2=sum 1=infinity"
        ),
        "exact_depth_two_telescope": (
            "(P_s^2-P0^2)/s=P_s*A_k+A_k*P0"
        ),
        "depth_two_failure": (
            "for h=e_1 and k>=2, P_s*A_k*h=0 but A_k*P0*h=e_1"
        ),
        "logical_verdict": (
            "fixed-source depth-one DQ plus formal telescope does not imply "
            "fixed-time DQ without branch-source invariance/extension"
        ),
        "countermodel_rows_sha256": canonical_digest(rows),
    }


def common_atlas_boundary_countermodel() -> dict[str, Any]:
    return {
        "currents": "J_s=delta_s on [-1,1], J_0=delta_0, s downarrow 0",
        "weak_current_convergence": "||J_s-J_0||_BL*<=s ->0",
        "singular_boundary": "S={0}",
        "branchwise_test": "Phi=1_(0,1] with Phi(0)=0",
        "off_boundary_behavior": (
            "for each fixed rho>0, Phi is BL on [-1,-rho] union [rho,1]"
        ),
        "pairing_failure": "J_s(Phi)=1 while J_0(Phi)=0",
        "failed_required_clause": (
            "sup_(0<s<rho) |J_s|([S]_rho)=1, so no C*rho^theta boundary tightness"
        ),
        "logical_verdict": (
            "weak current convergence and off-boundary branchwise tests need "
            "one common component atlas plus boundary-Z tightness"
        ),
    }


def face_two_cut_time_countermodel() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    partial_double_sum = 0
    for cutoff in range(65):
        # b_{m,n,ell}=1_{m=n}*2^{-(ell+1)}.  The depth sum is one
        # on the diagonal and zero off it.
        partial_double_sum += 1
        assert partial_double_sum == cutoff + 1
        rows.append({
            "time_box_max_index": cutoff,
            "diagonal_nonzero_pair_count": cutoff + 1,
            "complete_face_pairing_absolute_sum_in_box": cutoff + 1,
            "fixed_pair_tail_after_depth_L": "1_(m=n)*2^-(L+1)",
        })
    return rows, {
        "array": "b_(m,n,ell)=1_(m=n)*2^-(ell+1)",
        "per_depth_positive_decay": "2^-(ell+1)",
        "fixed_pair_tail": "sum_(ell>L)b_(m,n,ell)=1_(m=n)*2^-(L+1)",
        "every_fixed_pair_FACE_2CUT_tail_is_exponential": True,
        "complete_pairing": "B_(m,n)=1_(m=n)",
        "product_time_absolute_sum": "sum_(m,n)|B_(m,n)|=infinity",
        "logical_verdict": (
            "FACE_2CUT fixed-pair word-depth convergence does not imply a "
            "FACE_TIME product-time majorant"
        ),
        "countermodel_rows_sha256": canonical_digest(rows),
    }


def exact_frontier(
    telescope: dict[str, Any], finite_recovery: dict[str, Any],
) -> dict[str, Any]:
    t_limits = telescope["result"]["scope_limits"]
    r_limits = finite_recovery["result"]["scope_limits"]
    assert t_limits["fixed_time_dynamic_branch_record_MT_DQ"] is False
    assert t_limits["full_three_space_MT_DQ"] is False
    assert r_limits["uniform_one_time_finite_s_stopped_parent_recovery"] is True
    assert r_limits[
        "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas"
    ] is False
    assert r_limits["common_branch_record_MT_DQ"] is False
    return {
        "certified_now": [
            "limiting s=0 corrected face-product centered cluster with numeric typed bounds",
            "uniform |s|<=1/400 auxiliary K-depth parent-charge tail",
            "uniform |s|<=1/400 auxiliary depth-plus-recovery exponential tail",
            "uniform finite-s clock-only summable max(m,n) array from recovery moment plus coupling rate",
            "exact nonimplication countermodels for branch-source and product-time gaps",
        ],
        "still_missing_for_branch_record_MT_DQ": [
            "one component-indexed common moving atlas A_(L,m,n) for all iterated branch records",
            "fixed-time strong-space invariance/convergence of Q_s^m sources",
            "uniform BL modulus of moving branch tests off the common singular boundary",
            "boundary-Z tightness on every iterated singularity and atlas boundary",
            "finite-s regular/face/product/response typed convergence on the same atlas",
        ],
        "still_missing_for_physical_FACE_2CUT": [
            "identification of genuine physical word depth ell with an admissible record field",
            "positive coarea domination by the propagated q-law before cancellation",
            "uniform finite-s no-|s|^-1 per-depth bound",
            "actual/split constituent and component multiplicity accounting",
            "deep tail beyond L(s)",
        ],
        "still_missing_for_FACE_TIME": [
            "recordwise physical-current/proper-family matching",
            "restrictionwise source and scalar-current domination by propagated q",
            "physical bilinear test lift into the standard-family/flux-face norms",
            "finite-s uniform signed coupling after physical-current matching",
        ],
        "latest_literature_boundary": (
            "Stenlund--Young--Zhang arXiv:1210.0011v4 Lemmas 12 and 16 "
            "supply uniform one-time recovery on the compact configuration class, "
            "not a Gate3 DQ atlas; Demers--Liverani arXiv:2606.10155v1 "
            "Problem 8.7 leaves general characteristic-function restricted "
            "loss of memory open"
        ),
    }


def certify() -> dict[str, Any]:
    dq, telescope, product, _recovery0, finite_recovery = load_dependencies()
    cluster = limiting_face_product_cluster(dq)
    depth_rows, depth = auxiliary_depth_rows()
    recovery_tail = auxiliary_recovery_uniform_integrability(finite_recovery)
    clock = clock_only_two_time_split()
    branch_rows, branch_counter = branch_source_countermodel()
    atlas_counter = common_atlas_boundary_countermodel()
    face_rows, face_counter = face_two_cut_time_countermodel()
    frontier = exact_frontier(telescope, finite_recovery)
    kernel = product["result"]["mass_preserving_product_stopped_kernel"]
    assert kernel["exact_normalization_moment"] == "E[2^K]=3/2"
    assert kernel["same_K_j_mark_in_forward_and_reverse_views"] is True
    return {
        "schema": "cm2.gate3.branch-record-face-2cut-frontier.v1",
        "provenance": {
            "v52_manifest": V52_MANIFEST.name,
            "v52_tex_sha256": (
                "e4fd6c74c4be53ec97287b747e792ec8c32f9cd184cff05047189472481c5daa"
            ),
            "depth_one_DQ_manifest": DQ_MANIFEST.name,
            "moving_test_telescope_manifest": TELESCOPE_MANIFEST.name,
            "product_depth_manifest": PRODUCT_MANIFEST.name,
            "recovery_bridge_manifest": RECOVERY_MANIFEST.name,
            "finite_s_common_mesh_recovery_manifest": (
                FINITE_S_RECOVERY_MANIFEST.name
            ),
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "limiting_face_product_centered_cluster": cluster,
        "controlled_uniform_finite_s_auxiliary_depth_tail": depth,
        "controlled_uniform_finite_s_auxiliary_recovery_tail": recovery_tail,
        "clock_only_two_time_summability": clock,
        "branch_source_nonimplication_countermodel": branch_counter,
        "common_atlas_boundary_countermodel": atlas_counter,
        "FACE_2CUT_vs_FACE_TIME_countermodel": face_counter,
        "exact_remaining_frontier": frontier,
        "scope_limits": {
            "limiting_s0_face_product_centered_cluster": True,
            "numeric_limiting_face_product_typed_bounds": True,
            "controlled_uniform_finite_s_auxiliary_depth_tail": True,
            "controlled_uniform_finite_s_auxiliary_depth_recovery_tail": True,
            "uniform_finite_s_clock_only_two_time_array_summable": True,
            "moving_dyadic_endpoints_registered_in_Gate3_common_DQ_atlas": False,
            "physical_face_current_available_only_as_limiting_s0_cluster": True,
            "finite_s_face_product_cluster_convergence": False,
            "component_indexed_iterated_common_moving_atlas": False,
            "fixed_time_dynamic_branch_record_MT_DQ": False,
            "full_three_space_MT_DQ": False,
            "physical_FACE_2CUT": False,
            "physical_FACE_TIME_CM2_or_REC": False,
            "CM2_norm_lifts": False,
            "gate3_certified": False,
        },
        "internal_replay_digests": {
            "depth_rows": canonical_digest(depth_rows),
            "branch_countermodel_rows": canonical_digest(branch_rows),
            "face_time_countermodel_rows": canonical_digest(face_rows),
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_LIMITING_FACE_PRODUCT_CENTERED_CLUSTER: CERTIFIED")
    print("GATE3_UNIFORM_FINITE_S_AUXILIARY_DEPTH_RECOVERY_TAIL: CERTIFIED")
    print("GATE3_UNIFORM_FINITE_S_CLOCK_ONLY_TWO_TIME_ARRAY: CERTIFIED")
    print("GATE3_DYNAMIC_BRANCH_RECORD_MT_DQ_AND_PHYSICAL_FACE_2CUT: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
