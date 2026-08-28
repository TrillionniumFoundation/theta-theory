#!/usr/bin/env python3
"""Immutable Gate-5 return-word key registry and three-norm frontier.

This certificate turns the already proved finite-height statement into an
explicit, replayable *candidate-key* registry.  It deliberately distinguishes
three objects which earlier prose could blur:

* a complete finite key envelope for every regular first return to the solid
  section (empty fibres are allowed);
* a symbolic prefix/suffix factorisation at every roof level; and
* the much stronger physical homogeneous operator registry required by CM2.

Only the first two are certified here.  The source-chart/target classification
is imported from the frozen exact first-hit certificate.  A free flight of
length less than three has at most four recorded transparent crossings in
each coordinate direction.  Straightness makes the signs monotone.  Hence a
finite grammar enumerates every possible recorded crossing word.

No TV contraction is promoted to a regular-density, standard-family,
flux/face, or dynamic-test bound.  Every missing operator field is recorded
explicitly and Gate 5 remains fail-closed.

Dependency: python-flint==0.9.0, needed by the imported frozen first-hit
certificate even though this registry itself uses only exact integer data.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterator

import cm2_gate3_candidate_first_hit_cert as first_hit


HERE = Path(__file__).resolve().parent

FIRST_HIT_MANIFEST = HERE / "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"
PREFIX_MANIFEST = HERE / "cm2-gate5-prefix-suffix-norm-manifest-2026-07-15.json"
PHASE_MANIFEST = HERE / "cm2-gate5-actual-phase-graph-manifest-2026-07-15.json"
KAC_MANIFEST = (
    HERE / "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json"
)
FINITE_S_MANIFEST = (
    HERE / "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
)
FRONTIER_MANIFEST = (
    HERE / "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json"
)
GATE2_SATURATION_MANIFEST = (
    HERE / "cm2-gate2-stable-saturation-scale-gap-manifest-2026-07-15.json"
)
GATE2_FULL_MASS_MANIFEST = (
    HERE / "cm2-gate2-full-mass-tail-manifest-2026-07-15.json"
)

SOURCE_CHARTS = tuple(
    f"{source}:{cell}"
    for source in ("G", "W")
    for cell in ("E", "W", "N", "S")
)
MAX_CROSSINGS_PER_AXIS = 4
MAX_RETURN_HEIGHT = 9
TARGET_INDEX_BOX = (-4, 4)


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
        "first_hit": load_json(FIRST_HIT_MANIFEST),
        "prefix": load_json(PREFIX_MANIFEST),
        "phase": load_json(PHASE_MANIFEST),
        "kac": load_json(KAC_MANIFEST),
        "finite_s": load_json(FINITE_S_MANIFEST),
        "frontier": load_json(FRONTIER_MANIFEST),
        "gate2_saturation": load_json(GATE2_SATURATION_MANIFEST),
        "gate2_full_mass": load_json(GATE2_FULL_MASS_MANIFEST),
    }

    first = dependencies["first_hit"]["candidate_reduction"]
    assert first["chart_target_pair_count"] == 1296
    assert first["retained_pair_count"] == 448
    assert first["certified_empty_pair_count"] == 848
    assert first["target_universe"]["target_count"] == 162
    assert first["target_universe"]["index_box"] == [[-4, 4], [-4, 4]]

    finite = dependencies["prefix"]["finite_measurable_layer"]
    assert finite["uniform_return_depth_bound"] == MAX_RETURN_HEIGHT
    assert finite["finite_borel_return_word_universe"] is True
    assert dependencies["prefix"]["local_physical_layer"][
        "covers_every_return_word_and_homogeneity_subbranch"
    ] is False

    phase = dependencies["phase"]
    assert phase["completion"]["weighted_cycle_gcd_one"] is True
    assert phase["completion"]["complete_return_word_manifest"] is False
    assert phase["logical_scope"]["all_return_word_operator_blocks_registered"] is False

    kac_completion = dependencies["kac"]["result"]["completion"]
    assert kac_completion["exact_four_term_Borel_Kac_algebra"] is True
    assert kac_completion["physical_four_term_Kac_CM2_typing"] is False

    finite_s = dependencies["finite_s"]
    assert finite_s["verdict"]["uniform_one_time_finite_s_recovery"] == "CERTIFIED"
    assert finite_s["result"]["scope_limits"]["physical_prefix_suffix_costs"] is False
    assert finite_s["result"]["scope_limits"]["CM2_norm_lifts"] is False

    frontier = dependencies["frontier"]["result"]
    assert frontier["completion"]["physical_Borel_TV_Linf_prefix_suffix_constants"] is True
    assert frontier["completion"]["immutable_complete_return_word_operator_registry"] is False
    assert frontier["completion"]["full_four_term_physical_Kac_CM2_output"] is False

    saturation = dependencies["gate2_saturation"]
    assert saturation["physical_inputs"]["full_countable_pair_energy_drift"] is False
    assert saturation["physical_inputs"]["stable_quotient_density_rho"] is False
    assert saturation["physical_inputs"]["full_mass_countable_return_partition"] is False
    full_mass = dependencies["gate2_full_mass"]
    assert full_mass["physical_objects"]["one_state_young_base"] is False
    assert full_mass["physical_objects"]["stable_holonomy_quotient_density_rho"] is False
    assert full_mass["physical_objects"]["full_return_partition"] is False
    return dependencies


def orientation_choices(count: int) -> tuple[int, ...]:
    return (0,) if count == 0 else (-1, 1)


def crossing_patterns() -> Iterator[tuple[str, ...]]:
    """Enumerate every monotone clean-wall record with <=4 hits per axis."""

    for nx in range(MAX_CROSSINGS_PER_AXIS + 1):
        for ny in range(MAX_CROSSINGS_PER_AXIS + 1):
            length = nx + ny
            for sx in orientation_choices(nx):
                for sy in orientation_choices(ny):
                    for x_positions in itertools.combinations(range(length), nx):
                        x_set = set(x_positions)
                        x_token = "X+" if sx > 0 else "X-"
                        y_token = "Y+" if sy > 0 else "Y-"
                        yield tuple(
                            x_token if index in x_set else y_token
                            for index in range(length)
                        )


def crossing_grammar() -> dict[str, Any]:
    patterns = tuple(crossing_patterns())
    assert len(patterns) == 985
    assert len(set(patterns)) == len(patterns)
    histogram = Counter(len(pattern) for pattern in patterns)
    expected = {0: 1, 1: 4, 2: 12, 3: 28, 4: 60, 5: 120, 6: 200, 7: 280, 8: 280}
    assert dict(sorted(histogram.items())) == expected
    assert max(histogram) + 1 == MAX_RETURN_HEIGHT
    return {
        "event_alphabet": ["X-", "X+", "Y-", "Y+"],
        "straight_flight_monotone_sign_per_axis": True,
        "maximum_recorded_crossings_per_axis": MAX_CROSSINGS_PER_AXIS,
        "crossing_pattern_count": len(patterns),
        "wall_count_histogram": {str(key): value for key, value in sorted(histogram.items())},
        "crossing_pattern_rows_sha256": canonical_digest(patterns),
        "singular_simultaneous_corner_crossings_sent_to_cemetery": True,
    }


def retained_chart_target_pairs() -> tuple[tuple[str, str], ...]:
    pairs = tuple(
        (chart_id, target_id)
        for chart_id in SOURCE_CHARTS
        for target_id in first_hit.candidate_ids(chart_id)
    )
    assert len(pairs) == 448
    assert len(set(pairs)) == 448
    return pairs


def registry_key_row(
    chart_id: str, target_id: str, crossings: tuple[str, ...]
) -> tuple[Any, ...]:
    return (
        chart_id,
        target_id,
        crossings,
        len(crossings) + 1,
    )


def candidate_key_registry() -> dict[str, Any]:
    pairs = retained_chart_target_pairs()
    patterns = tuple(crossing_patterns())
    digest = hashlib.sha256()
    word_count = 0
    roof_level_factor_count = 0
    boundary_factor_count = 0
    roof_histogram: Counter[int] = Counter()

    for chart_id, target_id in pairs:
        for crossings in patterns:
            row = registry_key_row(chart_id, target_id, crossings)
            digest.update(canonical_json(row).encode("utf-8"))
            digest.update(b"\n")
            roof = len(crossings) + 1
            word_count += 1
            roof_level_factor_count += roof
            boundary_factor_count += roof + 1
            roof_histogram[roof] += 1

    assert word_count == 441280
    assert roof_level_factor_count == 3286976
    assert boundary_factor_count == 3728256
    expected_histogram = {
        1: 448,
        2: 1792,
        3: 5376,
        4: 12544,
        5: 26880,
        6: 53760,
        7: 89600,
        8: 125440,
        9: 125440,
    }
    assert dict(sorted(roof_histogram.items())) == expected_histogram

    domain_contract = {
        "word_key": "(source normal chart, retained target lift, monotone clean-wall record)",
        "domain_formula": (
            "D_w(s)={x in chart: the ordered clean-wall records are exactly w, "
            "and the next solid first hit is the recorded target}; empty fibres allowed"
        ),
        "source_chart_seam_rule": "dominant normal cell with fixed E,W,N,S boundary tie order",
        "target_filter": "exact horizon/outgoing-halfspace necessary-condition reduction",
        "regular_domain_partition": True,
        "coverage_statement": (
            "every regular first return belongs to exactly one key; grazing, source-chart "
            "seams and simultaneous wall-corner events require one-sided trace/cemetery typing"
        ),
        "all_parameter_fibres_share_one_key_universe": True,
        "parameter_window": "|s|<=1/400",
    }

    factor_contract = {
        "roof_level_index": "0<=j<r(w)",
        "prefix_token": "P[w,j]=U_c^j restricted to D_w",
        "suffix_token": "S[w,j]=U_c^(r(w)-j) on the j-th image of D_w",
        "source_test_adjoint_token": "<S J P nu,phi>=<J P nu,S^* phi>",
        "roof_level_prefix_suffix_factor_pair_count": roof_level_factor_count,
        "including_endpoint_boundary_split_count": boundary_factor_count,
        "symbolic_factorisation_complete_on_every_candidate_key": True,
        "homogeneous_subbranch_index_instantiated": False,
    }

    return {
        "source_chart_count": len(SOURCE_CHARTS),
        "conservative_target_lift_count": 162,
        "retained_chart_target_pair_count": len(pairs),
        "certified_empty_chart_target_pair_count": 848,
        "crossing_pattern_count_per_pair": len(patterns),
        "candidate_return_word_key_count": word_count,
        "roof_histogram": {str(key): value for key, value in sorted(roof_histogram.items())},
        "candidate_word_key_rows_sha256": digest.hexdigest(),
        "chart_target_pair_rows_sha256": canonical_digest(pairs),
        "domain_contract": domain_contract,
        "prefix_suffix_factor_contract": factor_contract,
        "exact_nonempty_candidate_key_count": None,
        "complete_physical_operator_block_count": 0,
    }


def required_operator_field_schema() -> dict[str, Any]:
    fields = (
        "nonempty_or_empty_domain_proof",
        "physical_homogeneity_subbranch_table",
        "homogeneous_prefix_chart",
        "homogeneous_suffix_chart",
        "inverse_Jacobian_bound",
        "log_Jacobian_distortion_sum",
        "one_step_cut_growth_Z_sum",
        "face_transversality_lower",
        "face_C2_atlas_bound",
        "coarea_density_regular_bound",
        "dynamic_Holder_test_pullback_bound",
        "C1_face_trace_pullback_bound",
        "moving_boundary_DQ_current_and_two_traces",
        "regular_density_operator_cost",
        "standard_family_operator_cost",
        "flux_face_operator_cost",
        "dynamic_test_operator_cost",
        "operator_phase_block",
    )
    seed_bindings = {
        "physical_Borel_TV_Linf_prefix_suffix_constant": "1",
        "Kac_height_constant": "9",
        "one_collision_geometric_seed": "204*2^B_s",
        "one_time_initial_standard_family_seed": "C_mesh*2^K",
        "C_mesh": "69986663973833932800",
        "known_positive_component_phase_edges": 3,
        "known_corrected_singular_occurrence_rows": 64,
        "known_corrected_singular_Kac_coordinates": 128,
        "seeds_bound_to_every_return_word_key": False,
    }
    return {
        "required_field_count_per_physical_homogeneous_level": len(fields),
        "required_fields": list(fields),
        "required_field_schema_sha256": canonical_digest(fields),
        "immutable_slot_key": "(word_key, homogeneous_subbranch_id, roof_level_j, field_name)",
        "word_key_and_symbolic_level_slots_declared": True,
        "homogeneous_subbranch_ids_materialized": False,
        "all_required_fields_populated": False,
        "seed_bindings": seed_bindings,
        "first_missing_field": "nonempty_or_empty_domain_proof",
        "first_strong_norm_missing_field": "physical_homogeneity_subbranch_table",
        "no_occurrence_level_seed_is_silently_copied_to_all_word_keys": True,
    }


def exact_nonpromotion_countermodels() -> dict[str, Any]:
    # One height-one deterministic Borel word: H(x)=x^2.  At y=1/n^2 the
    # inverse speed and pushed density are exactly n/2 although TV stays one.
    inverse_samples = [Fraction(n, 2) for n in (2, 4, 8, 16, 32, 64, 128)]
    assert inverse_samples[-1] == 64

    # One word split into 64 homogeneous fragments.  TV remains one, while
    # sum_j m_j(1+1/|W_j|)=65 versus input cost two.
    fragments = 64
    output_curve_cost = sum(
        (Fraction(1, fragments) * (1 + fragments) for _ in range(fragments)),
        Fraction(0),
    )
    assert output_curve_cost == 65
    assert output_curve_cost / 2 == Fraction(65, 2)

    # A one-component weight-one graph has cycle gcd one.  On a hidden
    # two-dimensional fibre U=diag(1,-1), however, I-zU is singular on the
    # centered vector e_2 at z=-1.  Component gcd therefore is not an
    # operator Wiener theorem.
    component_cycle_gcd = 1
    hidden_fibre_eigenvalues = (1, -1)
    phase = -1
    centered_denominator = 1 - phase * hidden_fibre_eigenvalues[1]
    assert centered_denominator == 0

    rows = {
        "same_one_word_Borel_registry_TV_constant": "1",
        "quadratic_inverse_speed_samples": [str(value) for value in inverse_samples],
        "quadratic_last_inverse_speed": str(inverse_samples[-1]),
        "fragment_count": fragments,
        "curve_cost_amplification": str(output_curve_cost / 2),
        "component_cycle_gcd": component_cycle_gcd,
        "hidden_fibre_operator": "diag(1,-1)",
        "hidden_centered_unit_phase_resonance": "z=-1",
        "finite_word_keys_imply_three_CM2_intertwiners": False,
        "component_gcd_one_implies_operator_Wiener_invertibility": False,
    }
    rows["countermodel_rows_sha256"] = canonical_digest(rows)
    return rows


def kac_phase_frontier(dependencies: dict[str, dict[str, Any]]) -> dict[str, Any]:
    frontier = dependencies["frontier"]["result"]
    kac = frontier["corrected_Kac_borel_output"]
    phase = dependencies["phase"]
    return {
        "finite_Borel_four_term_Kac_algebra_exact": True,
        "singular_Kac_Borel_event_current_TV_upper": kac["global_event_current_TV_upper"],
        "height_nine_singular_phase_lift_upper": kac[
            "worst_case_height_nine_phase_lifted_singular_l1_TV_upper"
        ],
        "regular_two_Kac_terms_typed_in_CM2_spaces": False,
        "return_word_propagated_singular_terms_typed_in_CM2_spaces": False,
        "full_four_term_physical_Kac_CM2_output": False,
        "actual_component_cycle_gcd": phase["phase_graphs"][
            "standard_N_component_cycle_gcd"
        ],
        "component_period_obstruction_removed": True,
        "all_return_word_operator_phase_blocks_registered": False,
        "operator_Wiener_phase_transfer": False,
        "preferred_direct_standard_N_route_needs_separate_phase_tower": False,
    }


def gate2_nonpromotion_audit(
    dependencies: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    saturation = dependencies["gate2_saturation"]
    full_mass = dependencies["gate2_full_mass"]
    return {
        "this_registry_section": "collision section N=G disjoint-union W",
        "regular_collision_SRB_domain_covered_mod_singular_set": True,
        "registry_is_stable_saturated_Young_base": False,
        "stable_holonomy_quotient_constructed": False,
        "stable_quotient_density_rho_constructed": False,
        "physical_reverse_kernel_constructed": False,
        "one_state_full_branch_quotient_constructed": False,
        "native_stopping_antichain_constructed": False,
        "unregistered_common_rectangle_fraction_lower": saturation["proved_layers"][
            "unregistered_common_rectangle_fraction_lower"
        ],
        "gate2_full_return_partition": full_mass["physical_objects"][
            "full_return_partition"
        ],
        "candidate_Borel_return_keys_feed_Gate2_one_state_quotient": False,
        "reason": (
            "a collision-SRB first-return key partition on N does not supply a "
            "stable-saturated Young rectangle, holonomy quotient, rho, onto inverse "
            "branches, reverse weights, or native stopping"
        ),
        "gate2_certified": False,
    }


def certify() -> dict[str, Any]:
    dependencies = load_dependencies()
    grammar = crossing_grammar()
    registry = candidate_key_registry()
    fields = required_operator_field_schema()
    countermodels = exact_nonpromotion_countermodels()
    kac_phase = kac_phase_frontier(dependencies)
    gate2 = gate2_nonpromotion_audit(dependencies)

    result = {
        "schema": "cm2.gate5.return-word-three-norm-frontier.v1",
        "provenance": {
            "first_hit_atlas_manifest": FIRST_HIT_MANIFEST.name,
            "prefix_suffix_manifest": PREFIX_MANIFEST.name,
            "actual_phase_graph_manifest": PHASE_MANIFEST.name,
            "corrected_Kac_manifest": KAC_MANIFEST.name,
            "finite_s_common_mesh_recovery_manifest": FINITE_S_MANIFEST.name,
            "physical_prefix_Kac_frontier_manifest": FRONTIER_MANIFEST.name,
            "gate2_stable_saturation_manifest": GATE2_SATURATION_MANIFEST.name,
            "gate2_full_mass_tail_manifest": GATE2_FULL_MASS_MANIFEST.name,
        },
        "crossing_grammar": grammar,
        "immutable_candidate_key_registry": registry,
        "required_operator_field_schema": fields,
        "exact_nonpromotion_countermodels": countermodels,
        "Kac_and_phase_frontier": kac_phase,
        "Gate2_nonpromotion_audit": gate2,
        "completion": {
            "complete_regular_return_word_candidate_key_envelope": True,
            "immutable_candidate_word_key_digest": True,
            "symbolic_prefix_suffix_factorization_every_roof_level": True,
            "physical_Borel_TV_Linf_prefix_suffix_constants": True,
            "complete_nonempty_return_word_domain_decisions": False,
            "physical_homogeneous_subbranch_registry": False,
            "immutable_complete_return_word_operator_registry": False,
            "regular_density_prefix_suffix_intertwiner": False,
            "standard_family_CM2_norm_lift": False,
            "flux_face_CM2_norm_lift": False,
            "dynamic_test_CM2_norm_lift": False,
            "full_four_term_physical_Kac_CM2_output": False,
            "operator_Wiener_phase_transfer": False,
            "gate5_certified": False,
        },
    }
    result["internal_replay_digest"] = canonical_digest(
        {
            "grammar": grammar,
            "registry": registry,
            "fields": fields,
            "countermodels": countermodels,
            "gate2": gate2,
            "completion": result["completion"],
        }
    )
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE5_COMPLETE_REGULAR_RETURN_WORD_CANDIDATE_KEY_ENVELOPE: CERTIFIED")
    print("GATE5_SYMBOLIC_PREFIX_SUFFIX_LEVEL_REGISTRY: CERTIFIED")
    print("GATE5_PHYSICAL_HOMOGENEOUS_OPERATOR_REGISTRY: NOT_CERTIFIED")
    print("GATE5_THREE_CM2_NORM_INTERTWINERS: NOT_CERTIFIED")
    print("GATE5_FULL_KAC_OPERATOR_PHASE_TRANSFER: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
