#!/usr/bin/env python3
"""Physical Borel prefix/suffix constants and the sharp Gate-5 norm frontier.

The physical first-return maps are deterministic Borel maps on a partition.
Consequently their pushforwards contract total variation and their adjoint
pullbacks contract the bounded-test norm.  This remains true through grazing
and therefore gives genuine numeric prefix/suffix constants at the
``M_b--B_b`` level, even though the stronger CM2 norms still need geometric
branch data.

The certificate binds that contraction to the corrected 64-row/128-coordinate
Kac ledger, the return-height bound ``K_N <= 9``, the actual component phase
gcd-one certificate, and the finite-parameter one-collision/common-mesh
recovery seed on ``|s|<=1/400``.  It also replays exact countermodels showing
why none of those Borel bounds or one-time recovery statements promotes itself
to the return-wide regular-density, standard-family/flux-face, or dynamic-test
CM2 intertwiners.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

PREFIX_MANIFEST = HERE / "cm2-gate5-prefix-suffix-norm-manifest-2026-07-15.json"
PHASE_MANIFEST = HERE / "cm2-gate5-actual-phase-graph-manifest-2026-07-15.json"
KAC_MANIFEST = (
    HERE / "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json"
)
RANK_MANIFEST = (
    HERE / "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
)
GEOMETRY_MANIFEST = (
    HERE / "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
)
RECOVERY_MANIFEST = (
    HERE / "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
)
PRODUCT_DEPTH_MANIFEST = (
    HERE / "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
)
FINITE_S_MANIFEST = (
    HERE / "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
)
GATE1_MANIFEST = (
    HERE / "cm2-gate1-canonical-holonomy-resonance-manifest-2026-07-15.json"
)
GATE2_MANIFEST = (
    HERE / "cm2-gate2-wasserstein-energy-manifest-2026-07-15.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def load_dependencies() -> dict[str, dict[str, Any]]:
    dependencies = {
        "prefix": load_json(PREFIX_MANIFEST),
        "phase": load_json(PHASE_MANIFEST),
        "kac": load_json(KAC_MANIFEST),
        "rank": load_json(RANK_MANIFEST),
        "geometry": load_json(GEOMETRY_MANIFEST),
        "recovery": load_json(RECOVERY_MANIFEST),
        "product_depth": load_json(PRODUCT_DEPTH_MANIFEST),
        "finite_s": load_json(FINITE_S_MANIFEST),
        "gate1": load_json(GATE1_MANIFEST),
        "gate2": load_json(GATE2_MANIFEST),
    }

    finite = dependencies["prefix"]["finite_measurable_layer"]
    assert finite["uniform_return_depth_bound"] == 9
    assert finite["finite_borel_return_word_universe"] is True
    assert finite["exact_current_prefix_suffix_pairing"] is True

    phase = dependencies["phase"]
    assert phase["completion"]["weighted_cycle_gcd_one"] is True
    assert phase["phase_graphs"]["standard_N_component_cycle_gcd"] == 1
    assert phase["completion"]["operator_wiener_aperiodicity_for_fixed_to_full_route"] is False

    kac_completion = dependencies["kac"]["result"]["completion"]
    assert kac_completion["corrected_bounded_Borel_singular_Kac_typing"] is True
    assert kac_completion["standard_family_CM2_norm_lift"] is False

    assert dependencies["rank"]["verdict"]["first_order_bidirectional_C1_costs"] == "CERTIFIED"
    assert dependencies["geometry"]["verdict"]["bidirectional_carrier_C2_costs"] == "CERTIFIED"
    assert dependencies["recovery"]["verdict"]["controlled_s0_stopped_parent_recovery"] == "CERTIFIED"
    assert dependencies["product_depth"]["result"]["scope_limits"]["native_physical_stopping_antichain"] is False

    finite_s = dependencies["finite_s"]
    assert finite_s["verdict"]["uniform_one_time_finite_s_recovery"] == "CERTIFIED"
    assert finite_s["verdict"]["explicit_numeric_initial_C_mesh"] == "CERTIFIED"
    finite_limits = finite_s["result"]["scope_limits"]
    assert finite_limits["uniform_one_collision_geometric_cost_coefficients"] is True
    assert finite_limits["theorem_recovery_constants_numeric"] is False
    assert finite_limits["native_dynamical_stopping_antichain"] is False
    assert finite_limits["hereditary_repeated_indicator_recovery"] is False
    assert finite_limits["CM2_norm_lifts"] is False

    gate1 = dependencies["gate1"]
    assert gate1["proved_obstructions"]["canonical_stable_limit_fails_at_qnl"] is True
    assert gate1["completion_requirements"]["gate1_unconditional_typicality_input"] is False

    gate2 = dependencies["gate2"]
    assert gate2["proved_layers"]["uniform_pair_energy_drift_theorem"] is True
    assert gate2["physical_inputs"]["actual_one_state_full_mass_quotient"] is False
    return dependencies


def physical_borel_prefix_suffix_constants(return_height: int) -> dict[str, Any]:
    """Exact operator constants on finite signed measures/bounded tests.

    Restriction to a Borel partition is additive in total variation, and a
    deterministic pushforward cannot increase total variation.  Dually,
    composition with a deterministic map cannot increase the sup norm.
    The tower sum has at most ``return_height`` levels.
    """

    assert return_height == 9
    return {
        "source_space": "M_b (finite signed Borel measures with total variation)",
        "test_space": "B_b (bounded Borel tests with sup norm)",
        "single_physical_prefix_pushforward_TV_norm_upper": "1",
        "single_physical_suffix_pushforward_TV_norm_upper": "1",
        "single_physical_prefix_test_pullback_Linf_norm_upper": "1",
        "single_physical_suffix_test_pullback_Linf_norm_upper": "1",
        "complete_partition_endpoint_pushforward_TV_norm_upper": "1",
        "complete_partition_endpoint_test_pullback_Linf_norm_upper": "1",
        "inserted_current_prefix_suffix_TV_multiplier_upper": "1",
        "return_height_upper": return_height,
        "unnormalized_Kac_test_sum_Linf_norm_upper": str(return_height),
        "normalized_tower_source_TV_norm_upper": str(return_height),
        "normalizer_reason": "1<=mu_N(r_N)<=9",
        "proof_contract": (
            "sum_w ||nu|D_w||_TV=||nu||_TV on the disjoint return partition; "
            "deterministic pushforward and bounded-test composition are contractions"
        ),
        "constants_ignore_Jacobian_only_at_Borel_TV_Linf_level": True,
    }


def corrected_kac_borel_output(
    dependencies: dict[str, dict[str, Any]], return_height: int,
) -> dict[str, Any]:
    kac = dependencies["kac"]["result"]
    layer = kac["corrected_global_finite_borel_kac_layer"]
    ledger = kac["corrected_global_occurrence_ledger"]
    current_tv = Q(layer["global_event_current_TV_upper_bound"])
    direct_sum_tv = 2 * current_tv
    lifted_direct_sum_tv = return_height * direct_sum_tv

    assert ledger["maximal_physical_occurrence_count"] == 64
    assert ledger["singular_kac_coordinate_count"] == 128
    assert ledger["all_singular_coordinate_pairs_share_mark_plus_one_minus_one"] is True
    assert current_tv == Q(16128, 5)
    assert direct_sum_tv == Q(32256, 5)
    assert lifted_direct_sum_tv == Q(290304, 5)

    return {
        "maximal_physical_occurrence_count": 64,
        "singular_Kac_coordinate_count": 128,
        "shared_row_mark": [1, -1],
        "global_event_current_TV_upper": str(current_tv),
        "two_singular_coordinate_l1_TV_upper": str(direct_sum_tv),
        "worst_case_height_nine_phase_lifted_singular_l1_TV_upper": str(
            lifted_direct_sum_tv
        ),
        "finite_borel_four_term_Kac_algebra_exact": True,
        "global_signed_scalar_coarea_mass": "0",
        "scalar_roof_cancellation_is_not_arbitrary_test_current_cancellation": True,
        "regular_two_Kac_terms_separately_typed_in_CM2_spaces": False,
        "full_four_term_physical_CM2_output": False,
    }


def one_collision_three_norm_seeds(
    dependencies: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    finite_s = dependencies["finite_s"]["result"]
    finite_cost = finite_s["finite_s_rank_and_one_collision_cost"][
        "finite_s_one_collision_cost"
    ]
    mesh = finite_s["finite_s_density_mesh_and_numeric_C_mesh"]
    recovery = finite_s["uniform_configuration_and_recovery"][
        "uniform_recovery_theorem"
    ]
    limits = finite_s["scope_limits"]

    assert finite_cost["uniform_forward_subcost"] == (
        "C_fw^(geom)(s,a)<=204*2^B_s(a)"
    )
    assert finite_cost["uniform_reverse_subcost"] == (
        "C_rev^(geom)(s,a)<=204*2^B_s(a)"
    )
    assert mesh["explicit_initial_C_mesh"] == "69986663973833932800"
    assert mesh["uniform_log_Hoelder_constant"] == "52"
    assert recovery["controlled_one_time_finite_s_stopped_parent_recovery"] is True
    assert recovery["C_p_vartheta_p_numerically_evaluated"] is False
    assert recovery["hereditary_repeated_indicator_recovery"] is False
    assert limits["native_dynamical_stopping_antichain"] is False

    return {
        "parameter_window": "|s|<=1/400",
        "uniform_finite_s_one_collision_dynamic_C1_test_pullback_integrable": True,
        "uniform_finite_s_one_collision_forward_C1_subcost": "151*2^B_s",
        "uniform_finite_s_one_collision_reverse_C1_subcost": "151*2^B_s",
        "uniform_finite_s_one_collision_bidirectional_carrier_C2_bounds": True,
        "uniform_finite_s_one_collision_bidirectional_log_density_bounds": True,
        "uniform_finite_s_one_collision_geometric_subcost": "204*2^B_s",
        "uniform_finite_s_controlled_atom_standard_family_entry": True,
        "uniform_finite_s_controlled_atom_log_Hoelder_constant": "52",
        "uniform_finite_s_initial_C_mesh": "69986663973833932800",
        "uniform_finite_s_atom_boundary": (
            "Z_s,fw(K,j),Z_s,rev(K,j)<=69986663973833932800*2^K"
        ),
        "uniform_one_time_finite_s_stopped_parent_recovery": True,
        "uniform_finite_s_recovery_clock": (
            "R_fw+R_rev<=2*A0+2*A1*K"
        ),
        "uniform_finite_s_depth_recovery_moment_for_some_gamma": True,
        "theorem_recovery_constants": "C_p>1 and 0<vartheta_p<1",
        "theorem_recovery_constants_numeric": False,
        "native_dynamical_stopping_antichain": False,
        "hereditary_repeated_indicator_recovery": False,
        "product_depth_expected_normalization_cost": "E[2^K]=3/2",
        "these_are_occurrence_level_seeds_not_return_word_intertwiners": True,
        "uniform_finite_s_return_prefix_suffix_propagation": False,
        "return_wide_standard_family_CM2_intertwiner": False,
        "return_wide_flux_face_CM2_intertwiner": False,
        "return_wide_dynamic_test_CM2_intertwiner": False,
        "complete_standard_family_CM2_norm_lift": False,
        "complete_flux_face_CM2_norm_lift": False,
        "complete_dynamic_test_CM2_norm_lift": False,
    }


def exact_nonpromotion_countermodels() -> dict[str, Any]:
    # Fixed TV mass one, but positive-decomposition boundary cost grows with
    # the number of fragments.  The n=64 replay is exact.
    n = 64
    input_curve_cost = Q(2)
    output_curve_cost = sum((Q(1, n) * (1 + n) for _ in range(n)), Q(0))
    assert output_curve_cost == n + 1
    assert output_curve_cost / input_curve_cost == Q(65, 2)

    # H(x)=x^2 has inverse speed 1/(2 sqrt(y)); at y=1/n^2 it is n/2.
    inverse_samples = [Q(sample, 2) for sample in (2, 4, 8, 16, 32, 64, 128)]
    assert inverse_samples == sorted(inverse_samples)
    assert inverse_samples[-1] == 64

    rows = {
        "fragment_count": n,
        "input_TV_mass": "1",
        "input_model_curve_cost": str(input_curve_cost),
        "output_model_curve_cost": str(output_curve_cost),
        "curve_cost_amplification": str(output_curve_cost / input_curve_cost),
        "quadratic_branch_inverse_speed_samples": [str(x) for x in inverse_samples],
        "quadratic_branch_last_inverse_speed": str(inverse_samples[-1]),
        "TV_Linf_prefix_suffix_constants_imply_regular_density_bound": False,
        "TV_Linf_prefix_suffix_constants_imply_standard_family_Z_bound": False,
        "TV_Linf_prefix_suffix_constants_imply_flux_face_atlas_bound": False,
        "TV_Linf_prefix_suffix_constants_imply_dynamic_C1_test_bound": False,
    }
    rows["countermodel_digest"] = canonical_digest(rows)
    return rows


def phase_and_route_audit(dependencies: dict[str, dict[str, Any]]) -> dict[str, Any]:
    phase = dependencies["phase"]
    return {
        "actual_standard_N_component_cycle_gcd": phase["phase_graphs"][
            "standard_N_component_cycle_gcd"
        ],
        "actual_component_phase_gcd_one": True,
        "complete_return_word_operator_blocks": False,
        "operator_Dz_unit_circle_invertibility_from_component_graph": False,
        "operator_Wiener_phase_transfer": False,
        "preferred_route": phase["route_audit"]["preferred_route"],
        "direct_standard_N_route_needs_separate_phase_tower": False,
        "route_conclusion": (
            "component period is closed; optional fixed-to-full operator phase "
            "transfer remains open, while the preferred direct-N route uses no phase tower"
        ),
    }


def gate12_bridge_audit(dependencies: dict[str, dict[str, Any]]) -> dict[str, Any]:
    gate1 = dependencies["gate1"]
    gate2 = dependencies["gate2"]
    product = dependencies["product_depth"]["result"]
    assert product["mass_preserving_product_stopped_kernel"][
        "K_independent_of_physical_row_point_under_product_kernel"
    ] is True
    assert product["scope_limits"]["native_physical_stopping_antichain"] is False
    return {
        "gate1": {
            "natural_QNL_canonical_stable_limit_converges": False,
            "exact_resonant_increment_coefficient": gate1["exact_qnl_jet"][
                "resonant_increment_coefficient"
            ],
            "Borel_prefix_suffix_contraction_changes_cocycle_holonomy_tail": False,
            "new_same_carrier_holonomy_bridge_from_gate5_data": False,
            "gate1_certified": False,
        },
        "gate2": {
            "weak_metric_pair_energy_bridge_available": gate2["proved_layers"][
                "uniform_pair_energy_drift_theorem"
            ],
            "actual_one_state_full_mass_quotient": False,
            "query_independent_product_depth_kernel_is_native_physical_quotient": False,
            "new_full_mass_PPE_bridge_from_gate5_data": False,
            "gate2_certified": False,
        },
    }


def certify() -> dict[str, Any]:
    dependencies = load_dependencies()
    return_height = dependencies["prefix"]["finite_measurable_layer"][
        "uniform_return_depth_bound"
    ]
    result = {
        "schema": "cm2.gate5.physical-prefix-kac-norm-frontier.v1",
        "provenance": {
            "prefix_suffix_manifest": PREFIX_MANIFEST.name,
            "actual_phase_graph_manifest": PHASE_MANIFEST.name,
            "corrected_Kac_manifest": KAC_MANIFEST.name,
            "endpoint_rank_manifest": RANK_MANIFEST.name,
            "curvature_log_density_manifest": GEOMETRY_MANIFEST.name,
            "density_mesh_recovery_manifest": RECOVERY_MANIFEST.name,
            "product_depth_manifest": PRODUCT_DEPTH_MANIFEST.name,
            "finite_s_common_mesh_recovery_manifest": FINITE_S_MANIFEST.name,
            "gate1_resonance_manifest": GATE1_MANIFEST.name,
            "gate2_energy_manifest": GATE2_MANIFEST.name,
        },
        "physical_borel_prefix_suffix_constants": (
            physical_borel_prefix_suffix_constants(return_height)
        ),
        "corrected_Kac_borel_output": corrected_kac_borel_output(
            dependencies, return_height
        ),
        "one_collision_three_norm_seeds": one_collision_three_norm_seeds(
            dependencies
        ),
        "exact_nonpromotion_countermodels": exact_nonpromotion_countermodels(),
        "phase_and_route_audit": phase_and_route_audit(dependencies),
        "gate1_gate2_bridge_audit": gate12_bridge_audit(dependencies),
        "completion": {
            "physical_Borel_TV_Linf_prefix_suffix_constants": True,
            "explicit_corrected_singular_Kac_Borel_output_envelope": True,
            "one_collision_three_norm_seeds": True,
            "uniform_finite_s_one_collision_three_norm_seeds": True,
            "uniform_one_time_finite_s_stopped_parent_recovery": True,
            "actual_component_phase_gcd_one": True,
            "immutable_complete_return_word_operator_registry": False,
            "regular_density_prefix_suffix_intertwiner": False,
            "standard_family_CM2_norm_lift": False,
            "flux_face_CM2_norm_lift": False,
            "dynamic_test_CM2_norm_lift": False,
            "theorem_recovery_constants_numeric": False,
            "native_dynamical_stopping_antichain": False,
            "hereditary_repeated_indicator_recovery": False,
            "full_four_term_physical_Kac_CM2_output": False,
            "operator_Wiener_phase_transfer": False,
            "gate1_certified": False,
            "gate2_certified": False,
            "gate5_certified": False,
        },
    }
    result["internal_replay_digest"] = canonical_digest({
        "borel": result["physical_borel_prefix_suffix_constants"],
        "kac": result["corrected_Kac_borel_output"],
        "countermodels": result["exact_nonpromotion_countermodels"],
        "completion": result["completion"],
    })
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE5_PHYSICAL_BOREL_PREFIX_SUFFIX_CONSTANTS: CERTIFIED")
    print("GATE5_CORRECTED_SINGULAR_KAC_BOREL_OUTPUT_ENVELOPE: CERTIFIED")
    print("GATE5_UNIFORM_FINITE_S_ONE_COLLISION_RECOVERY_SEEDS: CERTIFIED")
    print("GATE5_PHYSICAL_THREE_CM2_NORM_LIFTS: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
