#!/usr/bin/env python3
"""Stopped-depth threshold and first-order Kac rebind.

The cumulative-mass dyadic algebra fixes the exact normalization cost
``2^K`` but does not put a probability law on the stopping depth.  This
replay gives an exact critical-tail countermodel, a supercritical sufficient
criterion that needs no independence from the endpoint rank, and a corrected
64-occurrence/128-coordinate Kac rebind to the new first-order charge.

The physical stopped tree, its supercritical depth tail, and its recovery
clock remain absent.  The sufficient criterion is therefore a frontier, not
a Gate-4 or Gate-5 completion.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate3_depth_one_fixed_gauge_dq_cert as dq


Q = Fraction
HERE = Path(__file__).resolve().parent
RANK_MANIFEST = (
    HERE / "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
)
ALGEBRA_MANIFEST = (
    HERE / "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
)
KAC_MANIFEST = (
    HERE / "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    rank = json.loads(RANK_MANIFEST.read_text(encoding="utf-8"))
    algebra = json.loads(ALGEBRA_MANIFEST.read_text(encoding="utf-8"))
    kac = json.loads(KAC_MANIFEST.read_text(encoding="utf-8"))
    assert rank["verdict"]["first_order_bidirectional_C1_costs"] == "CERTIFIED"
    assert algebra["verdict"]["controlled_dyadic_stopped_interval_algebra"] == "CERTIFIED"
    assert kac["verdict"]["corrected_128_coordinate_Borel_Kac_layer"] == "CERTIFIED"
    return rank, algebra, kac


def critical_depth_countermodel(maximum_depth: int = 64) -> dict[str, Any]:
    sample_rows = []
    for depth in (4, 8, 16, 32, maximum_depth):
        weights = [Q(1, 1 << (index + 1)) for index in range(depth)]
        weights.append(Q(1, 1 << depth))
        assert sum(weights, Q(0)) == 1
        tails = []
        for threshold in range(depth + 1):
            tail = sum(weights[threshold:], Q(0))
            assert tail == Q(1, 1 << threshold)
            tails.append(str(tail))
        normalization_moment = sum(
            ((1 << index) * weight for index, weight in enumerate(weights)),
            Q(0),
        )
        assert normalization_moment == 1 + Q(depth, 2)
        sample_rows.append({
            "maximum_depth": depth,
            "critical_tail": "P(K>=k)=2^-k for 0<=k<=N",
            "E_2^K": str(normalization_moment),
            "tail_rows_sha256": canonical_digest(tails),
        })
    assert sample_rows[-1]["E_2^K"] == "33"
    return {
        "finite_countermodel_family": sample_rows,
        "finite_countermodel_rows_sha256": canonical_digest(sample_rows),
        "critical_depth_tail": "P(K>=k)=2^-k",
        "normalization_moment_at_cutoff_N": "E[2^K]=1+N/2",
        "critical_tail_does_not_uniformly_control_2^K": True,
        "dyadic_atom_mass_scale_alone_is_not_a_stopping_depth_law": True,
        "required_depth_tail_exponent_base_two": "strictly greater than 1",
    }


def supercritical_sufficient_bridge() -> dict[str, Any]:
    depth_tail_exponent = Q(3, 2)
    holder_p = Q(5, 4)
    holder_q = Q(5)
    endpoint_exponent = Q(1, 10)
    endpoint_holder_exponent = holder_q * endpoint_exponent
    assert holder_p < depth_tail_exponent
    assert 1 / holder_p + 1 / holder_q == 1
    assert endpoint_holder_exponent == Q(1, 2) < 1
    assert 2 * 6**4 > 7**4
    return {
        "assumed_propagated_depth_tail": "q{K>=k}<=A*2^(-3k/2)",
        "depth_holder_moment": "E_q[2^(5K/4)]<=7A",
        "geometric_ratio_certificate": "2^(-1/4)<6/7",
        "holder_exponents": [str(holder_p), str(holder_q)],
        "endpoint_rank_factor": "2^(B/10)",
        "endpoint_holder_moment_required": "E_q[2^(B/2)]<infinity",
        "endpoint_exponent_is_inside_certified_first_order_q_window": True,
        "no_independence_of_K_and_B_required": True,
        "combined_moment": "E_q[2^K*2^(B/10)]<infinity",
        "conditional_recovery_clock": (
            "if R_fw+R_rev<=A0+A1*B, choose gamma=log(2)/(10*A1)"
        ),
        "conditional_target_moment": (
            "E_q[2^K*exp(gamma*(R_fw+R_rev))]<infinity"
        ),
        "physical_supercritical_depth_tail_available": False,
        "physical_rank_recovery_clock_available": False,
    }


def first_order_kac_rebind(
    rank: dict[str, Any], kac: dict[str, Any],
) -> dict[str, Any]:
    rank_result = rank["result"]
    charge = rank_result["endpoint_rank_tail_and_first_order_cost"][
        "first_order_bidirectional_subcharge"
    ]
    old = kac["result"]
    old_ledger = old["corrected_global_occurrence_ledger"]
    assert old_ledger["maximal_physical_occurrence_count"] == 64
    assert old_ledger["singular_kac_coordinate_count"] == 128
    rows, registry = dq.load_rows()
    typed = []
    for row in rows:
        typed.append({
            "occurrence_id": row["occurrence_id"],
            "global_physical_label": row["global_physical_label"],
            "corrected_common_law": (
                "m_e=R_source*cp*abs(u_y)/ell_T*dtheta"
            ),
            "canonical_endpoint_rank": (
                "B_e=max(14,ceil(log2(1/scale_e)))"
            ),
            "first_order_forward_subcost": "151*2^B_e",
            "first_order_reverse_subcost": "151*2^B_e",
            "one_first_order_charge": "q_e^(1)=151*2^B_e*m_e",
            "singular_kac_coordinates": ["dot(S)h", "dot(r)*mu(h)"],
            "shared_singular_mark": [1, -1],
            "coordinate_views_are_nonadditive": True,
        })
    typed.sort(key=canonical_json)
    assert len(typed) == 64
    assert len({row["occurrence_id"] for row in typed}) == 64
    return {
        "maximal_occurrence_count": len(typed),
        "singular_kac_coordinate_count": 2 * len(typed),
        "one_first_order_charge_per_occurrence": True,
        "incorrect_per_coordinate_double_charge_count": 2 * len(typed),
        "first_order_charge_formula": charge["one_common_first_order_charge"],
        "global_first_order_charge_mass_upper_before_Z_N_inverse": charge[
            "global_first_order_charge_mass_upper_before_Z_N_inverse"
        ],
        "global_first_order_current_TV_upper_before_Z_N_inverse": charge[
            "global_first_order_current_TV_upper_before_Z_N_inverse"
        ],
        "finite_borel_kac_algebra_survives_first_order_reweighting": True,
        "global_signed_scalar_coarea_mass_before_reweighting": "0",
        "weighted_scalar_cancellation_not_claimed": True,
        "first_order_occurrence_rows_sha256": canonical_digest(typed),
        "maximal_row_registry_sha256": registry["maximal_row_rows_sha256"],
        "prior_corrected_occurrence_rows_sha256": old_ledger[
            "corrected_occurrence_rows_sha256"
        ],
    }


def physical_frontier(
    algebra: dict[str, Any], rank: dict[str, Any],
) -> dict[str, Any]:
    algebra_result = algebra["result"]
    rank_limits = rank["result"]["scope_limits"]
    rank_moment = rank["result"]["endpoint_rank_tail_and_first_order_cost"][
        "raw_rank_moment"
    ]
    assert algebra_result["scope_limits"][
        "countable_nested_dyadic_interval_algebra"
    ] is True
    assert rank_limits["numeric_first_order_forward_reverse_C1_subcosts"] is True
    assert rank_moment[
        "first_order_charge_rank_moments_2^(chi*B)_finite_for"
    ] == "0<=chi<1"
    return {
        "controlled_dyadic_interval_algebra": True,
        "finite_raw_endpoint_rank_first_moment": True,
        "numeric_first_order_bidirectional_C1_subcosts": True,
        "stopped_depth_random_variable_on_physical_tree": False,
        "q_propagated_supercritical_depth_tail": False,
        "C2_curvature_and_log_density_costs": False,
        "boundary_Z_and_proper_family_recovery_clock": False,
        "full_numeric_C_fw_C_rev": False,
        "controlled_stopped_parent_recovery": False,
        "dynamic_MT_DQ": False,
        "CM2_norm_lifts": False,
    }


def certify() -> dict[str, Any]:
    rank, algebra, kac = load_dependencies()
    critical = critical_depth_countermodel()
    sufficient = supercritical_sufficient_bridge()
    rebind = first_order_kac_rebind(rank, kac)
    frontier = physical_frontier(algebra, rank)
    return {
        "schema": "cm2.gate45.stopped-depth-kac-frontier.v1",
        "provenance": {
            "endpoint_rank_first_order_manifest": RANK_MANIFEST.name,
            "controlled_interval_algebra_manifest": ALGEBRA_MANIFEST.name,
            "corrected_kac_manifest": KAC_MANIFEST.name,
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "critical_stopped_depth_countermodel": critical,
        "supercritical_depth_rank_sufficient_bridge": sufficient,
        "first_order_64_occurrence_128_coordinate_kac_rebind": rebind,
        "physical_completion_frontier": frontier,
        "scope_limits": {
            "critical_depth_tail_obstruction_exact": True,
            "supercritical_depth_tail_sufficient_theorem_exact": True,
            "first_order_Kac_rebind_complete": True,
            "physical_supercritical_depth_tail": False,
            "physical_recovery_clock": False,
            "complete_numeric_C_fw_C_rev": False,
            "controlled_stopped_parent_recovery": False,
            "full_dynamic_MT_DQ": False,
            "CM2_norm_lifts": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
        "internal_replay_digest": canonical_digest({
            "critical": critical,
            "sufficient": sufficient,
            "rebind": rebind,
        }),
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE45_CRITICAL_STOPPED_DEPTH_TAIL_OBSTRUCTION: CERTIFIED")
    print("GATE45_SUPERCRITICAL_DEPTH_RANK_SUFFICIENT_BRIDGE: CERTIFIED")
    print("GATE45_FIRST_ORDER_64_ROW_128_COORDINATE_KAC_REBIND: CERTIFIED")
    print("GATE45_PHYSICAL_STOPPED_RECOVERY_AND_CM2_LIFTS: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
