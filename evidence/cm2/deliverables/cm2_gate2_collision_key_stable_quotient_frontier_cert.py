#!/usr/bin/env python3
"""Gate-2 frontier after the 441280-key collision-return envelope.

The Gate-5 registry gives a finite key for every regular collision step on
the standard section.  Combining it with Poincare recurrence on the already
certified positive-SRB source rectangle produces a countable, full-measure
*two-dimensional path-key schema* for its first return.

This certificate proves the sharp no-promotion statement: refining the graph
of an invertible first-return map by arbitrarily many countable labels never
changes its reverse kernel from a Dirac mass.  A non-invertible physical
kernel appears only after a genuine stable quotient.  The collision keys do
not construct the stable-saturated base, holonomy projection, quotient
density, reverse weights, endpoint typing, or native stopping required by
Gate 2.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
GATE5_KEYS_MANIFEST = (
    HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
)
POST_CROSS_MANIFEST = HERE / "cm2-gate2-post-full-cross-manifest-2026-07-15.json"
SATURATION_MANIFEST = (
    HERE / "cm2-gate2-stable-saturation-scale-gap-manifest-2026-07-15.json"
)
FULL_MASS_MANIFEST = HERE / "cm2-gate2-full-mass-tail-manifest-2026-07-15.json"
ENERGY_MANIFEST = HERE / "cm2-gate2-wasserstein-energy-manifest-2026-07-15.json"
PLAQUE_MANIFEST = (
    HERE / "cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json"
)

KEY_COUNT = 441280


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
        "gate5": load_json(GATE5_KEYS_MANIFEST),
        "post_cross": load_json(POST_CROSS_MANIFEST),
        "saturation": load_json(SATURATION_MANIFEST),
        "full_mass": load_json(FULL_MASS_MANIFEST),
        "energy": load_json(ENERGY_MANIFEST),
        "plaque": load_json(PLAQUE_MANIFEST),
    }

    gate5 = dependencies["gate5"]["result"]
    registry = gate5["immutable_candidate_key_registry"]
    assert registry["candidate_return_word_key_count"] == KEY_COUNT
    assert registry["candidate_word_key_rows_sha256"] == (
        "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
    )
    assert gate5["completion"]["complete_regular_return_word_candidate_key_envelope"]
    assert gate5["completion"]["immutable_complete_return_word_operator_registry"] is False
    assert registry["complete_physical_operator_block_count"] == 0

    post = dependencies["post_cross"]
    assert post["proved_layers"]["q_anchored_positive_srb_2d_source_rectangle"]
    assert post["proved_layers"]["full_mass_2d_first_return_by_poincare"]
    assert post["proved_layers"]["two_dimensional_reverse_kernel_is_dirac"]
    assert post["physical_inputs"]["stable_saturated_young_rectangle"] is False
    assert post["physical_inputs"]["stable_holonomy_projection_to_reference_curve"] is False

    saturation = dependencies["saturation"]
    assert saturation["proved_layers"]["current_two_raw_strips_physical_fraction_upper"] == "0.097"
    assert saturation["proved_layers"]["unregistered_common_rectangle_fraction_lower"] == "0.903"
    assert saturation["physical_inputs"]["stable_quotient_density_rho"] is False

    full = dependencies["full_mass"]
    assert full["proved_layers"]["abstract_prefix_stopping_antichain"] is True
    assert full["physical_objects"]["actual_native_stopping_antichain"] is False
    assert full["physical_objects"]["actual_reverse_weight_registry"] is False

    energy = dependencies["energy"]
    assert energy["proved_layers"]["uniform_pair_energy_drift_theorem"] is True
    assert energy["physical_inputs"]["actual_one_state_full_mass_quotient"] is False

    plaque = dependencies["plaque"]
    assert plaque["proved_layers"]["two_local_physical_branches_in_common_rectangle"]
    assert plaque["physical_inputs"]["second_branch_stable_saturation"] is False
    return dependencies


def full_mass_2d_path_key_schema(
    dependencies: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    gate5 = dependencies["gate5"]["result"]
    base_digest = gate5["immutable_candidate_key_registry"][
        "candidate_word_key_rows_sha256"
    ]
    # At collision depth n the conservative word universe is the Cartesian
    # power K^n.  The first-return predicate selects a Borel subset; empty
    # paths remain in the common generator universe.
    depth_counts = {str(n): str(KEY_COUNT**n) for n in range(1, 10)}
    grammar = {
        "base_alphabet_size": KEY_COUNT,
        "base_alphabet_digest": base_digest,
        "depth_n_candidate_path_count": "441280^n",
        "first_return_predicate": (
            "x in S_A, T^j x notin S_A for 1<=j<n, T^n x in S_A, "
            "and each collision step has the recorded Gate5 key"
        ),
        "path_universe": "disjoint union over n>=1 of K^n",
        "empty_path_fibres_allowed": True,
        "singular_orbit_cemetery": (
            "countable union of grazing/corner preimages; collision-SRB null"
        ),
    }
    return {
        "q_anchored_source_rectangle": "S_A",
        "source_mass_interval": dependencies["post_cross"]["proved_layers"][
            "source_mass_interval"
        ],
        "normalized_source_return_mass": "1 modulo the singular cemetery",
        "regular_collision_step_key_coverage": "1 modulo collision-SRB null set",
        "two_dimensional_first_return_path_key_coverage": (
            "1 under normalized mu|S_A by Poincare recurrence"
        ),
        "fixed_depth_candidate_counts_n_1_to_9": depth_counts,
        "path_key_grammar": grammar,
        "path_key_grammar_sha256": canonical_digest(grammar),
        "countable_full_measure_2d_path_key_schema": True,
        "exact_nonempty_path_keys_enumerated": False,
        "homogeneous_connected_return_components_enumerated": False,
        "full_image_stable_quotient_branches_enumerated": False,
    }


def exact_dirac_refinement_theorem() -> dict[str, Any]:
    """Exact finite replay plus the general invertible-map implication."""

    # A 97-cycle is invertible.  Give each edge a label in a much larger
    # declared universe; every target still has exactly one physical past.
    size = 97
    step = 37
    assert math.gcd(size, step) == 1
    permutation = tuple((step * point + 11) % size for point in range(size))
    assert len(set(permutation)) == size
    predecessor = [None] * size
    for source, target in enumerate(permutation):
        predecessor[target] = source
    assert all(value is not None for value in predecessor)
    support_sizes = [1 for _target in range(size)]
    l2_weight_sums = [Fraction(1) for _target in range(size)]
    assert set(support_sizes) == {1}
    assert set(l2_weight_sums) == {Fraction(1)}

    alpha = Fraction(1, 20)
    # At the diagonal, the two-copy truncated Riesz energy is r^-alpha both
    # before and after the deterministic inverse step.  The coefficient is 1.
    return {
        "finite_replay_state_count": size,
        "finite_replay_affine_permutation": "F(i)=37*i+11 mod 97",
        "declared_label_universe_size": KEY_COUNT,
        "physical_reverse_support_size_at_every_target": 1,
        "physical_reverse_weight_l2_sum_at_every_target": "1",
        "pair_energy_exponent": str(alpha),
        "diagonal_pair_energy_before": "r^-alpha",
        "diagonal_pair_energy_after": "r^-alpha",
        "strict_pair_energy_contraction_kappa_lt_1": False,
        "general_theorem": (
            "if F is invertible mod zero, then for every countable measurable "
            "refinement of its graph the physical reverse conditional at y is "
            "delta_(F^-1 y, recorded_label(F^-1 y))"
        ),
        "countable_key_refinement_changes_dirac_reverse_kernel": False,
        "randomizing_by_forgetting_the_physical_state_is_stable_quotient": False,
        "genuine_noninvertible_stable_collapse_required": True,
    }


def physical_mass_and_registration_ledger(
    dependencies: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    saturation = dependencies["saturation"]["proved_layers"]
    gate5_registry = dependencies["gate5"]["result"][
        "immutable_candidate_key_registry"
    ]
    return {
        "collision_SRB_regular_step_key_coverage_fraction": "1 modulo null",
        "q_anchored_2d_return_path_key_coverage_fraction": "1 modulo null",
        "complete_physical_Gate5_operator_block_count": gate5_registry[
            "complete_physical_operator_block_count"
        ],
        "current_two_raw_strips_common_rectangle_fraction_upper": saturation[
            "current_two_raw_strips_physical_fraction_upper"
        ],
        "unregistered_common_rectangle_fraction_lower": saturation[
            "unregistered_common_rectangle_fraction_lower"
        ],
        "stable_quotient_branch_probability_mass": "UNDEFINED_BEFORE_QUOTIENT",
        "endpoint_typed_PPE_probability_mass": "UNDEFINED_BEFORE_ENDPOINT_REGISTRY",
        "Gate5_key_envelope_increases_stable_saturated_registered_mass": False,
        "do_not_replace_undefined_quotient_mass_by_zero": True,
        "mass_conclusion": (
            "full Borel collision/path coverage and stable-quotient physical "
            "registration are different typed quantities"
        ),
    }


def quotient_reverse_endpoint_stopping_frontier(
    dependencies: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    full = dependencies["full_mass"]
    fields = (
        "stable_saturated_product_base_Lambda_A",
        "reference_unstable_interval_I_A",
        "stable_holonomy_projection_pi_s",
        "stable_holonomy_conditional_SRB_Jacobian",
        "connected_first_return_strip_partition",
        "onto_full_image_quotient_branches_h_a",
        "quotient_density_rho_with_upper_lower_bounds",
        "physical_reverse_weights_p_a",
        "transported_projective_matrix_M_a_in_one_trivialisation",
        "same_carrier_endpoint_maps_X_Y",
        "endpoint_denominator_lower_bound",
        "nonzero_endpoint_wedge",
        "inverse_cylinder_diameter_registry",
        "native_scale_prefix_stopping_antichain",
        "overshoot_cemetery_and_two_sided_scale_comparison",
        "off_diagonal_projective_near_collision_bound",
        "parentwise_normalized_amplitude_moment",
    )
    positive = {
        "candidate_actual_unstable_reference_curve": True,
        "two_local_physical_branches_in_common_rectangle": True,
        "abstract_prefix_stopping_antichain_algebra": full["proved_layers"][
            "abstract_prefix_stopping_antichain"
        ],
        "conditional_reverse_weight_formula": (
            "p_a(x)=rho(h_a(x))*abs(h_a'(x))/rho(x)"
        ),
        "uniform_pair_energy_drift_theorem_conditional_on_kernel": True,
    }
    missing = {field: False for field in fields}
    # I_A is a certified curve candidate, but not the reference interval of a
    # stable-saturated full-image quotient.  Keep the required field false.
    return {
        "required_field_count": len(fields),
        "required_fields": list(fields),
        "required_field_schema_sha256": canonical_digest(fields),
        "positive_precursors": positive,
        "physical_completion_flags": missing,
        "first_missing_object": "stable_saturated_product_base_Lambda_A",
        "first_reverse_kernel_missing_object": "stable_holonomy_projection_pi_s",
        "first_endpoint_missing_object": "transported_projective_matrix_M_a_in_one_trivialisation",
        "first_native_stopping_missing_object": "inverse_cylinder_diameter_registry",
        "all_fields_share_one_branch_label_registry": False,
    }


def exact_no_cardinality_promotion_countermodel() -> dict[str, Any]:
    # Split a probability interval into KEY_COUNT Borel labels and let the map
    # be identity on every point.  All labels have positive mass and total
    # mass one, but the reverse law and any transported projective coordinate
    # are deterministic.  Cardinality/full coverage alone imply no PPE.
    label_mass = Fraction(1, KEY_COUNT)
    assert KEY_COUNT * label_mass == 1
    rows = {
        "space": "[0,1] split into 441280 equal Borel labels",
        "map": "identity",
        "label_count": KEY_COUNT,
        "mass_per_label": str(label_mass),
        "total_registered_Borel_mass": "1",
        "reverse_kernel": "delta_x",
        "projective_stationary_law_from_one_point": "atomic",
        "stable_saturated_product_base_from_labels": False,
        "rho_h_a_p_a_from_labels": False,
        "native_stopping_from_labels": False,
        "PPE_from_full_label_coverage": False,
    }
    rows["countermodel_sha256"] = canonical_digest(rows)
    return rows


def certify() -> dict[str, Any]:
    dependencies = load_dependencies()
    path_schema = full_mass_2d_path_key_schema(dependencies)
    dirac = exact_dirac_refinement_theorem()
    mass = physical_mass_and_registration_ledger(dependencies)
    frontier = quotient_reverse_endpoint_stopping_frontier(dependencies)
    countermodel = exact_no_cardinality_promotion_countermodel()
    result = {
        "schema": "cm2.gate2.collision-key-stable-quotient-frontier.v1",
        "provenance": {
            "Gate5_return_word_key_manifest": GATE5_KEYS_MANIFEST.name,
            "post_full_cross_manifest": POST_CROSS_MANIFEST.name,
            "stable_saturation_gap_manifest": SATURATION_MANIFEST.name,
            "full_mass_tail_manifest": FULL_MASS_MANIFEST.name,
            "wasserstein_energy_manifest": ENERGY_MANIFEST.name,
            "actual_stable_plaque_manifest": PLAQUE_MANIFEST.name,
        },
        "full_mass_2d_path_key_schema": path_schema,
        "exact_dirac_refinement_theorem": dirac,
        "physical_mass_and_registration_ledger": mass,
        "quotient_reverse_endpoint_stopping_frontier": frontier,
        "exact_no_cardinality_promotion_countermodel": countermodel,
        "completion": {
            "countable_full_measure_2d_first_return_path_key_schema": True,
            "exact_2d_reverse_kernel_is_dirac": True,
            "Gate5_key_refinement_preserves_dirac_reverse_kernel": True,
            "stable_saturated_young_rectangle": False,
            "one_state_full_branch_stable_quotient": False,
            "stable_quotient_density_rho": False,
            "physical_reverse_weight_registry": False,
            "same_carrier_endpoint_typing": False,
            "actual_native_stopping_antichain": False,
            "full_countable_pair_energy_drift": False,
            "physical_PPE": False,
            "gate2_certified": False,
        },
    }
    result["internal_replay_digest"] = canonical_digest(
        {
            "path": path_schema,
            "dirac": dirac,
            "mass": mass,
            "frontier": frontier,
            "countermodel": countermodel,
            "completion": result["completion"],
        }
    )
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE2_FULL_MASS_2D_RETURN_PATH_KEY_SCHEMA: CERTIFIED")
    print("GATE2_KEY_REFINED_2D_REVERSE_KERNEL: DIRAC_NO_CONTRACTION")
    print("GATE2_STABLE_QUOTIENT_REVERSE_WEIGHTS_ENDPOINT_NATIVE_STOPPING: NOT_CERTIFIED")
    print("GATE2_PHYSICAL_PPE: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
