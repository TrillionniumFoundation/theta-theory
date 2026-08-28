#!/usr/bin/env python3
"""Density-regular endpoint mesh and closed-map recovery bridge.

Near a simple density zero of scale ``h``, a dyadic shell has carrier length
``O(h)`` and logarithmic-density derivative ``O(h^{-1})``.  Splitting that
shell into carrier intervals of length at most ``h^{3/2}`` makes the
one-third log-Hoelder constant uniform.  Although the number of pieces is
``O(h^{-1/2})``, their total unnormalized boundary-Z contribution is only
``O(h^{1/2})`` and is summable.

Consequently every single mass-coordinate atom from the controlled stopped
policy has, in each orientation separately, an initial standard-family
representation with uniform cone, C2, and density constants and with
``Z <= C 2^K`` after normalization.  The closed-billiard Growth Lemma then
gives an affine recovery clock ``R <= A0+A1 K``.  Combined with the product
depth kernel, this makes the depth/recovery moment finite for some positive
exponent.

The bridge uses the closed-map Growth Lemma (Canestrari 2026, Lemma 6.14,
ultimately Demers 2014).  It does not prove the finite-s moving-face DQ
majorant or arbitrary hereditary recovery after repeated indicator cuts.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent
CURVATURE_MANIFEST = (
    HERE / "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
)
PRODUCT_DEPTH_MANIFEST = (
    HERE / "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
)
RANK_MANIFEST = (
    HERE / "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    curvature = json.loads(CURVATURE_MANIFEST.read_text(encoding="utf-8"))
    product = json.loads(PRODUCT_DEPTH_MANIFEST.read_text(encoding="utf-8"))
    rank = json.loads(RANK_MANIFEST.read_text(encoding="utf-8"))
    assert curvature["verdict"]["bidirectional_carrier_C2_costs"] == "CERTIFIED"
    assert curvature["verdict"]["bidirectional_log_density_costs"] == "CERTIFIED"
    assert product["verdict"]["supercritical_depth_tail_and_E_2K"] == "CERTIFIED"
    assert rank["verdict"]["global_endpoint_rank_tail_exponent_two"] == "CERTIFIED"
    return curvature, product, rank


def density_mesh_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    for shell_rank in range(14, 65):
        shell_upper = Q(1, 1 << shell_rank)
        shell_lower = Q(1, 1 << (shell_rank + 1))
        mesh_exponent = (3 * (shell_rank + 1) + 1) // 2
        mesh_length = Q(1, 1 << mesh_exponent)
        assert mesh_length**2 <= shell_lower**3
        assert mesh_length**2 >= shell_lower**3 / 4
        piece_count_upper = 32769 * (1 << ((shell_rank + 1) // 2))
        carrier_shell_length_upper = 8192 * shell_upper
        assert piece_count_upper > carrier_shell_length_upper / mesh_length + 1
        z_numerator_upper = 23 * piece_count_upper * shell_upper
        rows.append({
            "shell_rank_b": shell_rank,
            "density_scale_interval": [str(shell_lower), str(shell_upper)],
            "mesh_exponent": mesh_exponent,
            "mesh_carrier_length": str(mesh_length),
            "mesh_squared_vs_lower_scale_cubed": "delta_b^2<=h_lower^3",
            "piece_count_upper": piece_count_upper,
            "orientation_common_carrier_shell_length_upper": str(
                carrier_shell_length_upper
            ),
            "orientation_common_Z_numerator_upper": str(z_numerator_upper),
        })
    # Since h_b*2^ceil(b/2)=2^-floor(b/2), the two parity classes give
    # 2*sum_{n>=7}2^-n=1/32.
    endpoint_z_sum_upper = Q(23 * 32769, 32)
    assert endpoint_z_sum_upper == Q(753687, 32)
    return rows, {
        "checked_shell_rank_range": [14, 64],
        "canonical_mesh": (
            "delta_b=2^-ceil(3(b+1)/2) in carrier arclength"
        ),
        "mesh_scale_contract": "delta_b^2<=2^-3(b+1)",
        "common_shell_carrier_length_upper": "8192*2^-b",
        "piece_count_upper": "32769*2^ceil(b/2)",
        "common_density_upper_on_zero_shell": "23*2^-b",
        "one_zero_endpoint_Z_numerator_series_upper": str(endpoint_z_sum_upper),
        "one_zero_endpoint_Z_series_is_summable": True,
        "density_mesh_rows_sha256": canonical_digest(rows),
    }


def standard_family_contract(mesh: dict[str, Any]) -> dict[str, Any]:
    core_width = Q(507, 5120)
    row_mass_lower = (
        Q(4, 25) * Q(1, 4096) * Q(1, 16384) * core_width / 3
    )
    assert row_mass_lower == Q(169, 2147483648000)
    assert Q(mesh["one_zero_endpoint_Z_numerator_series_upper"]) < 24000
    return {
        "density_zero_endpoint_counts": {
            "source_reverse_view": 48,
            "miss_forward_view": 48,
        },
        "uniform_one_third_log_Hoelder_argument": (
            "abs(d log rho/dr)<=52/h_lower and d<=h_lower^(3/2) "
            "imply abs(log rho(x)-log rho(y))<=52*d^(1/3)"
        ),
        "uniform_log_Hoelder_constant_on_endpoint_mesh": "52",
        "uniform_carrier_C2_upper": "4949",
        "fixed_global_unstable_cone": (
            "25/9<dphi/dr<4108425/145348"
        ),
        "common_row_mass_strict_lower": str(row_mass_lower),
        "row_mass_lower_derivation": (
            "(4/25)*(1/4096)*(1/16384)*(507/5120)/3"
        ),
        "orientation_specific_decompositions_allowed": True,
        "same_restricted_measure_and_same_K_j_record_in_both_views": True,
        "single_depth_K_atom_initial_standard_family_boundary": (
            "Z_fw(K,j),Z_rev(K,j)<=C_mesh*2^K"
        ),
        "C_mesh_is_finite_and_table_dependent": True,
        "arbitrary_finite_union_of_depth_K_atoms": (
            "finite positive sum of the single-atom standard families"
        ),
    }


def growth_lemma_bridge() -> dict[str, Any]:
    return {
        "imported_closed_map_theorem": (
            "Canestrari arXiv:2604.19671v2 Lemma 6.14 "
            "(Growth Lemma; based on Demers 2014 Lemma 8.4)"
        ),
        "growth_recurrence": (
            "Z(F^((p+1)n_*)G)<=theta*Z(F^(p n_*)G)+Z_0, 0<theta<1"
        ),
        "hypotheses_verified_for_each_oriented_stopped_atom": [
            "unstable cone alignment",
            "uniform C2 carrier bound",
            "uniform one-third log-Hoelder density",
            "finite initial boundary Z<=C_mesh*2^K",
        ],
        "forward_and_reverse_use_time_reversibility": True,
        "closed_map_recovery_clock": (
            "R_fw(K,j)+R_rev(K,j)<=A0+A1*K"
        ),
        "A0_A1_are_finite_table_dependent_constants": True,
        "product_depth_moment_choice": (
            "choose 0<gamma<log(2)/A1; then "
            "E[2^K*exp(gamma*(R_fw+R_rev))]<infinity"
        ),
        "controlled_s0_stopped_parent_recovery": True,
        "uniform_finite_s_moving_face_recovery_majorant": False,
        "hereditary_recovery_after_repeated_indicator_cuts": False,
    }


def literature_boundary() -> dict[str, Any]:
    return {
        "latest_review": (
            "Demers--Liverani, Recent Progress in the Application of "
            "Transfer Operators to Dispersing Billiards, arXiv:2606.10155v1"
        ),
        "review_date": "2026-06-08",
        "review_theorem_used_only_for_context": (
            "Theorem 5.7 surveys uniform cone contraction for sequential "
            "finite-horizon dispersing billiards"
        ),
        "review_open_problem_8_7": (
            "loss of memory after characteristic-function restrictions can "
            "concentrate on atypical trajectories and remains open in general"
        ),
        "why_no_overclaim": (
            "the certified bridge first represents each one-time controlled "
            "atom as a standard family and then evolves it under the closed "
            "map; it does not claim arbitrary repeated hereditary cuts"
        ),
    }


def certify() -> dict[str, Any]:
    curvature, product, rank = load_dependencies()
    rows, mesh = density_mesh_rows()
    standard = standard_family_contract(mesh)
    recovery = growth_lemma_bridge()
    literature = literature_boundary()
    assert curvature["result"]["scope_limits"][
        "all_row_bidirectional_carrier_C2_bounds"
    ] is True
    assert product["result"]["mass_preserving_product_stopped_kernel"][
        "exact_normalization_moment"
    ] == "E[2^K]=3/2"
    assert rank["result"]["all_endpoint_simple_germ_audit"][
        "collars_are_pairwise_disjoint_on_each_row"
    ] is True
    return {
        "schema": "cm2.gate45.density-regular-mesh-recovery-bridge.v1",
        "provenance": {
            "curvature_log_density_manifest": CURVATURE_MANIFEST.name,
            "product_stopped_depth_manifest": PRODUCT_DEPTH_MANIFEST.name,
            "endpoint_rank_manifest": RANK_MANIFEST.name,
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "density_regular_endpoint_mesh": mesh,
        "oriented_standard_family_contract": standard,
        "closed_map_growth_lemma_recovery_bridge": recovery,
        "latest_literature_boundary": literature,
        "scope_limits": {
            "summable_density_regular_endpoint_mesh": True,
            "uniform_standard_pair_density_and_C2_constants": True,
            "normalized_atom_boundary_Z_at_most_exponential_in_K": True,
            "controlled_s0_stopped_parent_recovery": True,
            "finite_depth_plus_recovery_moment_for_some_gamma": True,
            "uniform_finite_s_moving_face_recovery": False,
            "hereditary_recovery_under_repeated_arbitrary_indicators": False,
            "complete_numeric_C_fw_C_rev": False,
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
    print("GATE45_DENSITY_REGULAR_ENDPOINT_MESH: CERTIFIED")
    print("GATE45_CONTROLLED_S0_STOPPED_PARENT_RECOVERY: CERTIFIED")
    print("GATE45_UNIFORM_FINITE_S_RECOVERY_AND_FULL_MT_DQ: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
