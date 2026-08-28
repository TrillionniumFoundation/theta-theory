#!/usr/bin/env python3
"""Gate-4 product-kernel same-occurrence and joint-moment frontier.

This certificate combines only frozen inputs.  The product depth mark ``K``
is sampled before the physical row point, orientation, query and test.  Its
law is independent of the physical endpoint rank ``B`` and the same ``(K,j)``
record is used by the forward and reverse views of one occurrence.  The
newly numerical Growth constants therefore turn the previously symbolic
product-kernel estimate into an explicit joint ``(B,K)`` moment.

The result is deliberately narrower than the final CM2 Gate-4 contract.  It
certifies a controlled one-time product-kernel envelope and fixed-finite-H
registered restart numerators.  It does not replace the native physical
prefix antichain, make its countable time-zero boundary finite, regularize an
arbitrary physical indicator, or supply the missing strong-operator/MT_DQ
matching.  Consequently complete ``C_fw,C_rev``, final ``q`` and Gate 4 stay
fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json": (
        "200908d09b87c5bad5ee2f0d5d7d6af44c70110dd88017a847df10251a5145a1"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json": (
        "d5f563545c4ddaddfbb6b5cde5c4f5d8030247209e2284c06aeb9d3255a771f0"
    ),
    "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json": (
        "20f595ed4bcf62cb5cc5c89c22ab31a3ca039f43fff29fd35855673dc970b4a2"
    ),
    "cm2-v52-manifest.sha256": (
        "5cef5b8e60f0cfe2291da6bb34b2c57eed6cf2d1a13d164b74b566f752b6b368"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependencies() -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        if path.suffix == ".json":
            loaded[name] = json.loads(path.read_text(encoding="utf-8"))

    product = loaded[
        "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
    ]
    finite_s = loaded[
        "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
    ]
    numeric = loaded[
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    ]
    rows = loaded[
        "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json"
    ]
    native = loaded[
        "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json"
    ]

    kernel = product["result"]["mass_preserving_product_stopped_kernel"]
    assert kernel["depth_probability"] == "w_K=(3/4)*4^-K, K>=0"
    assert kernel["exact_normalization_moment"] == "E[2^K]=3/2"
    assert kernel["K_independent_of_physical_row_point_under_product_kernel"] is True
    assert kernel["same_K_j_mark_in_forward_and_reverse_views"] is True

    rank = finite_s["result"]["finite_s_rank_and_one_collision_cost"]
    assert rank["uniform_rank_tail"][
        "integral_2^B_uniform_upper_before_Z_N_inverse"
    ] == "43293270343755613/25600000"
    assert rank["canonical_finite_s_rank"]["core_rank"] == 20
    assert rank["finite_s_one_collision_cost"]["uniform_forward_subcost"] == (
        "C_fw^(geom)(s,a)<=204*2^B_s(a)"
    )
    assert rank["finite_s_one_collision_cost"]["uniform_reverse_subcost"] == (
        "C_rev^(geom)(s,a)<=204*2^B_s(a)"
    )
    assert finite_s["result"]["finite_s_density_mesh_and_numeric_C_mesh"][
        "explicit_initial_C_mesh"
    ] == "69986663973833932800"

    summary = numeric["replay_summary"]
    assert summary["A0"] == 301500
    assert summary["A1"] == 1005
    assert numeric["verdict"]["numeric_C_p_vartheta_p_A0_A1"] == "CERTIFIED"

    occurrence = rows["result"]["corrected_global_occurrence_ledger"]
    assert occurrence["maximal_physical_occurrence_count"] == 64
    assert occurrence["one_corrected_m_per_occurrence"] is True
    assert occurrence["same_occurrence_forward_reverse_views_on_every_row"] is True
    assert occurrence["endpoint_views_are_nonadditive_on_every_row"] is True

    assert native["replay_summary"]["single_indicator_Z"] == "infinity"
    assert native["replay_summary"]["repeated_cut_Z"] == "Z_h=4^h"
    assert native["verdict"]["hereditary_repeated_indicator_recovery"] == (
        "NOT_CERTIFIED"
    )
    return loaded


def same_occurrence_product_record() -> dict[str, Any]:
    return {
        "base_occurrence_count": 64,
        "base_positive_law": "one corrected m_e,s per physical occurrence",
        "product_extension": "d mhat_e,s=d m_e,s*(3/4)*4^-K",
        "atom_rule": "j=floor(2^K*u_e,s), 0<=j<2^K",
        "immutable_record": "(occurrence e,s,K,j,owner,polarity,restriction)",
        "mark_sampled_before": "orientation,time mode,linked query,final test",
        "K_independent_of_physical_point_and_B": True,
        "same_K_j_and_restriction_in_both_orientations": True,
        "forward_reverse_are_alternative_nonadditive_views": True,
        "product_extension_preserves_m_e_s_marginal": True,
        "query_independent_same_occurrence_product_record": "CERTIFIED",
        "native_physical_antichain": False,
    }


def joint_rank_depth_moment() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    endpoint_rank_moment = Q(43293270343755613, 25600000)
    A0 = 301500
    A1 = 1005
    gamma = Q(1, 12060)
    constant_exponent = gamma * 2 * A0
    level_exponent = gamma * 2 * A1
    assert constant_exponent == 50
    assert level_exponent == Q(1, 6)

    # Elementary rational proof of the only exponential comparisons used:
    # e<3 and 3<(5/4)^6, hence exp(1/6)<5/4 and exp(50)<3^50.
    assert Q(3) < Q(5, 4) ** 6
    kernel_ratio_upper = Q(5, 8)
    kernel_sum_upper = Q(3, 4) / (1 - kernel_ratio_upper)
    assert kernel_sum_upper == 2

    cutoffs = [0, 1, 2, 4, 8, 16, 32, 64]
    rows: list[dict[str, Any]] = []
    for cutoff in cutoffs:
        rational_kernel_majorant = sum(
            (Q(3, 4) * Q(1, 4**K) * (2**K) * Q(5, 4) ** K
             for K in range(cutoff + 1)),
            Q(0),
        )
        exact_payload_without_clock = sum(
            (Q(3, 4) * Q(1, 4**K) * (2**K)
             for K in range(cutoff + 1)),
            Q(0),
        )
        assert rational_kernel_majorant < kernel_sum_upper
        assert exact_payload_without_clock < Q(3, 2)
        rows.append({
            "cutoff_N": cutoff,
            "partial_E_2K": str(exact_payload_without_clock),
            "partial_clocked_kernel_rational_majorant": str(
                rational_kernel_majorant
            ),
        })

    joint_upper = endpoint_rank_moment * kernel_sum_upper * 3**50
    assert joint_upper == Q(
        31080151660381513756308599682583861157637, 12800000
    )
    return rows, {
        "finite_s_rank_moment_upper": str(endpoint_rank_moment),
        "product_depth_law": "w_K=(3/4)*4^-K",
        "two_orientation_recovery_clock": (
            "R_fw+R_rev<=603000+2010*K"
        ),
        "gamma": str(gamma),
        "constant_exponential_bound": "exp(50)<3^50",
        "level_exponential_bound": "exp(K/6)<(5/4)^K",
        "clocked_depth_series_ratio_strict_upper": str(kernel_ratio_upper),
        "clocked_depth_moment_strict_upper": str(kernel_sum_upper * 3**50),
        "joint_integrand": "2^(B_s+K)*exp(gamma*(R_fw+R_rev))",
        "joint_B_K_moment_strict_upper_before_Z_N_inverse": str(joint_upper),
        "joint_factorization_reason": (
            "K is independent of the physical row point and hence of B_s in "
            "the frozen product kernel"
        ),
        "uniform_in_parameter": "|s|<=1/400",
        "numeric_product_kernel_joint_B_K_moment": "CERTIFIED",
        "cutoff_rows_sha256": canonical_digest(rows),
    }


def boundary_and_fixed_history_frontier() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    c_mesh = Q(69986663973833932800)
    expected_2K = Q(3, 2)
    one_cut_numerator = c_mesh * expected_2K
    assert one_cut_numerator == 104979995960750899200
    clocked_one_stage_upper = 2 * 3**50

    rows: list[dict[str, Any]] = []
    for H in range(1, 9):
        rows.append({
            "fixed_registered_history_length_H": H,
            "normalization_payload_moment": str(expected_2K**H),
            "clocked_payload_moment_strict_upper": str(
                clocked_one_stage_upper**H
            ),
        })
    return rows, {
        "one_atom_oriented_boundary": "Z_fw,Z_rev<=C_mesh*2^K",
        "C_mesh": str(c_mesh),
        "exact_E_2K": str(expected_2K),
        "one_registered_cut_levelwise_boundary_numerator_coefficient_per_unit_incoming_mass": str(
            one_cut_numerator
        ),
        "both_orientations_use_one_max_not_an_additive_double_charge": True,
        "fixed_H_presampled_marks": "(K_1,j_1),...,(K_H,j_H)",
        "H_and_all_marks_fixed_before_the_later_query": True,
        "mandatory_restart_order": (
            "registered cut, retain occurrence record, recover both available "
            "orientations, then admit the next registered cut"
        ),
        "fixed_finite_H_registered_restart_moment": "CERTIFIED",
        "one_universal_kernel_for_query_selected_H": False,
        "arbitrary_physical_indicator": False,
        "unbounded_H_uniform_moment": False,
        "history_rows_sha256": canonical_digest(rows),
    }


def controlled_cost_envelope() -> dict[str, Any]:
    endpoint_rank_moment = Q(43293270343755613, 25600000)
    c_mesh = Q(69986663973833932800)
    rank_floor = 20
    total_mass_upper = endpoint_rank_moment / (2**rank_floor)
    clocked_depth_upper = Q(2 * 3**50)
    coefficient = Q(204) + (c_mesh + 2) / (2**rank_floor)
    envelope_mass_upper = clocked_depth_upper * endpoint_rank_moment * coefficient
    assert envelope_mass_upper == Q(
        1087598065258783059015245434544676138185728521412801591795461,
        6710886400000,
    )
    return {
        "declared_controlled_envelope": (
            "C_prod(s,a,K)=2^K*exp(gamma*(R_fw+R_rev))*"
            "max(204*2^B_s(a),C_mesh,2)"
        ),
        "dominates_forward_geometric_Z_clock_sublayers": True,
        "dominates_reverse_geometric_Z_clock_sublayers": True,
        "one_maximum_charged_once_on_the_common_product_law": True,
        "total_coarea_mass_upper_from_B_floor": str(total_mass_upper),
        "integral_C_prod_strict_upper_before_Z_N_inverse": str(
            envelope_mass_upper
        ),
        "numeric_controlled_product_forward_subcost": "CERTIFIED",
        "numeric_controlled_product_reverse_subcost": "CERTIFIED",
        "controlled_product_single_charge": "CERTIFIED",
        "not_included": [
            "complete recordwise strong-operator/source norm",
            "physical test lift on every recovered branch record",
            "Gate-3 common branch-record MT_DQ/current matching",
            "native or arbitrary repeated-indicator regularization",
        ],
        "complete_C_fw": False,
        "complete_C_rev": False,
        "final_same_occurrence_q": False,
    }


def exact_remaining_boundary() -> dict[str, Any]:
    return {
        "native_countable_initial_partition_time_zero_Z": "infinity",
        "product_kernel_is_not_native_antichain": True,
        "one_arbitrary_open_indicator_can_have_Z": "infinity",
        "quarter_cut_counterexample": "Z_h=4^h",
        "fixed_finite_registered_histories_do_not_imply_unbounded_history": True,
        "no_tail_on_number_of_repeated_cuts_H": True,
        "complete_same_occurrence_operator_ledger": False,
        "Gate3_common_branch_record_MT_DQ": False,
        "complete_numeric_C_fw_C_rev": False,
        "final_q_max_Cfw_Crev_2_m": False,
        "gate4_certified": False,
    }


def certify() -> dict[str, Any]:
    load_dependencies()
    cutoff_rows, joint = joint_rank_depth_moment()
    history_rows, history = boundary_and_fixed_history_frontier()
    result = {
        "schema": "cm2.gate4.product-same-occurrence-joint-moment-frontier.v1",
        "provenance": {
            "dependency_count": len(DEPENDENCIES),
            "parameter_window": "|s|<=1/400",
            "maximal_occurrence_count": 64,
        },
        "same_occurrence_product_record": same_occurrence_product_record(),
        "numeric_joint_rank_depth_moment": joint,
        "registered_repeated_cut_frontier": history,
        "controlled_product_cost_envelope": controlled_cost_envelope(),
        "exact_remaining_boundary": exact_remaining_boundary(),
        "internal_replay_digests": {
            "joint_cutoff_rows": canonical_digest(cutoff_rows),
            "fixed_history_rows": canonical_digest(history_rows),
        },
        "scope_limits": {
            "query_independent_product_same_occurrence_record": True,
            "numeric_joint_B_K_recovery_moment": True,
            "one_registered_cut_finite_levelwise_boundary_numerator": True,
            "fixed_finite_H_registered_restart_moment": True,
            "numeric_controlled_product_geometric_Z_clock_subcosts": True,
            "native_full_reweighted_recovery": False,
            "arbitrary_or_unbounded_repeated_indicator_recovery": False,
            "complete_numeric_C_fw_C_rev": False,
            "final_same_occurrence_q": False,
            "gate4_certified": False,
        },
    }
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE4_PRODUCT_SAME_OCCURRENCE_RECORD: CERTIFIED")
    print("GATE4_NUMERIC_JOINT_B_K_RECOVERY_MOMENT: CERTIFIED")
    print("GATE4_FIXED_FINITE_REGISTERED_RESTART_MOMENT: CERTIFIED")
    print("GATE4_COMPLETE_C_FW_C_REV_FINAL_Q: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
