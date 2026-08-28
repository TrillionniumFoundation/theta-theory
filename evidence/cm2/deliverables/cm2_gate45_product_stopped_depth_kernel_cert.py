#!/usr/bin/env python3
"""Mass-preserving supercritical product stopped-depth kernel.

The cumulative-mass dyadic algebra does not prescribe a law for its depth.
This certificate supplies a query-independent auxiliary kernel.  Before the
orientation, product time, and final test are chosen, sample

    w_K = (3/4) 4^{-K},  K >= 0,

independently of the physical row point.  The depth-K atom index is then the
unique ``j=floor(2^K u_e)`` containing that point.  Forgetting ``(K,j)``
returns the exact physical row law.  The same mark is used in both oriented
views, its tail is exactly ``4^{-K}``, and ``E[2^K]=3/2``.

This removes the critical depth-tail obstruction inside the declared
controlled policy.  It is not a native dynamical stopping antichain and it
does not supply the billiard recovery clock.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent
ALGEBRA_MANIFEST = (
    HERE / "cm2-gate45-controlled-stopped-interval-algebra-manifest-2026-07-15.json"
)
GEOMETRIC_COST_MANIFEST = (
    HERE / "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any]]:
    algebra = json.loads(ALGEBRA_MANIFEST.read_text(encoding="utf-8"))
    costs = json.loads(GEOMETRIC_COST_MANIFEST.read_text(encoding="utf-8"))
    assert algebra["verdict"][
        "controlled_dyadic_stopped_interval_algebra"
    ] == "CERTIFIED"
    assert costs["verdict"]["bidirectional_carrier_C2_costs"] == "CERTIFIED"
    assert costs["verdict"]["bidirectional_log_density_costs"] == "CERTIFIED"
    return algebra, costs


def finite_cutoff_audit() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    for cutoff in (4, 8, 16, 32, 64):
        level_weights = [Q(3, 4) * Q(1, 4**depth) for depth in range(cutoff)]
        tail = Q(1, 4**cutoff)
        assert sum(level_weights, Q(0)) + tail == 1
        first_moment_partial = sum(
            ((1 << depth) * weight for depth, weight in enumerate(level_weights)),
            Q(0),
        )
        first_moment_with_tail_upper = first_moment_partial + (1 << cutoff) * tail
        assert first_moment_with_tail_upper < Q(3, 2)
        rows.append({
            "cutoff_N": cutoff,
            "listed_level_mass": str(sum(level_weights, Q(0))),
            "unlisted_tail_mass": str(tail),
            "partial_E_2^K": str(first_moment_partial),
            "partial_plus_cutoff_tail_lower_charge": str(
                first_moment_with_tail_upper
            ),
        })
    return rows, {
        "checked_cutoffs": [4, 8, 16, 32, 64],
        "all_finite_cutoff_mass_identities_exact": True,
        "finite_cutoff_rows_sha256": canonical_digest(rows),
    }


def product_kernel_contract() -> dict[str, Any]:
    first_moment = Q(3, 4) / (1 - Q(1, 2))
    assert first_moment == Q(3, 2)
    # 2^(1/4)<6/5, hence 2^(5/4)/4<3/5.
    holder_moment_upper = Q(3, 4) / (1 - Q(3, 5))
    assert 2**4 < Q(6, 5) ** 16
    assert holder_moment_upper == Q(15, 8)
    return {
        "depth_probability": "w_K=(3/4)*4^-K, K>=0",
        "depth_tail": "P(K>=k)=4^-k",
        "tail_exponent_base_two": "2",
        "depth_K_atom_count": "2^K",
        "one_depth_K_atom_joint_mass": (
            "w_K*2^-K*m_e=(3/4)*8^-K*m_e"
        ),
        "atom_index": "j=floor(2^K*u_e), 0<=j<2^K",
        "row_marginal_identity": (
            "sum_K sum_j (3/4)*8^-K*m_e|I(K,j)=m_e"
        ),
        "same_K_j_mark_in_forward_and_reverse_views": True,
        "K_sampled_before_orientation_time_mode_and_final_test": True,
        "K_independent_of_physical_row_point_under_product_kernel": True,
        "exact_normalization_moment": "E[2^K]=3/2",
        "holder_depth_moment": "E[2^(5K/4)]<15/8",
        "holder_bound_uses": "2^(1/4)<6/5",
    }


def recovery_factorization_frontier() -> dict[str, Any]:
    return {
        "finite_q_product_extension": (
            "d qhat(e,u,K)=d q(e,u)*(3/4)*4^-K"
        ),
        "q_marginal_preserved_exactly": True,
        "depth_only_target": "E_qhat[2^K]=3/2",
        "conditional_affine_clock_bridge": (
            "if R_fw+R_rev<=A0+A1*B+A2*K and 0<gamma<log(2)/A2, "
            "the K factor in E[2^K exp(gamma(R_fw+R_rev))] is finite"
        ),
        "remaining_endpoint_factor": "E_q[exp(gamma*A1*B)]",
        "critical_K_tail_obstruction_removed_in_declared_policy": True,
        "native_dynamical_stopping_antichain_constructed": False,
        "physical_recovery_clock_constructed": False,
    }


def certify() -> dict[str, Any]:
    algebra, costs = load_dependencies()
    rows, cutoff_audit = finite_cutoff_audit()
    kernel = product_kernel_contract()
    frontier = recovery_factorization_frontier()
    algebra_result = algebra["result"]
    assert algebra_result["all_maximal_row_contracts"][
        "maximal_occurrence_count"
    ] == 64
    partial_cost = costs["result"]["curvature_log_density_and_partial_cost"][
        "numeric_one_collision_geometric_subcosts"
    ]
    assert partial_cost["partial_charge_is_finite"] is True
    return {
        "schema": "cm2.gate45.product-stopped-depth-kernel.v1",
        "provenance": {
            "controlled_interval_algebra_manifest": ALGEBRA_MANIFEST.name,
            "curvature_log_density_cost_manifest": GEOMETRIC_COST_MANIFEST.name,
            "maximal_occurrence_count": 64,
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "finite_cutoff_replay": cutoff_audit,
        "mass_preserving_product_stopped_kernel": kernel,
        "recovery_moment_factorization_frontier": frontier,
        "scope_limits": {
            "query_independent_mass_preserving_depth_kernel": True,
            "exact_supercritical_depth_tail": True,
            "finite_expected_parent_normalization_cost": True,
            "same_stopped_mark_for_both_orientations": True,
            "critical_depth_tail_obstruction_removed_in_controlled_policy": True,
            "native_physical_stopping_antichain": False,
            "physical_recovery_clock": False,
            "complete_numeric_C_fw_C_rev": False,
            "controlled_stopped_parent_recovery": False,
            "full_dynamic_MT_DQ": False,
            "CM2_norm_lifts": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
        "internal_replay_digest": canonical_digest(rows),
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE45_MASS_PRESERVING_PRODUCT_STOPPED_DEPTH_KERNEL: CERTIFIED")
    print("GATE45_SUPERCRITICAL_DEPTH_TAIL_AND_E_2K: CERTIFIED")
    print("GATE45_NATIVE_PHYSICAL_STOPPED_RECOVERY: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
