#!/usr/bin/env python3
"""Replay and fail-closed verifier for the Gate-5 physical norm frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "cm2.gate5.physical-prefix-kac-norm-frontier.manifest.v1"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json"
)
CERTIFICATE = HERE / "cm2_gate5_physical_prefix_kac_norm_frontier_cert.py"
VERIFIER = HERE / "cm2_gate5_physical_prefix_kac_norm_frontier_verifier.py"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_structure(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["manifest is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append("schema mismatch")
    if data.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash mismatch")
    if data.get("verifier_sha256") != sha256_path(VERIFIER):
        errors.append("verifier hash mismatch")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict) or not dependencies:
        errors.append("dependencies missing")
    else:
        required_finite_s_dependency = (
            "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
        )
        if required_finite_s_dependency not in dependencies:
            errors.append("finite-s common-mesh/recovery dependency missing")
        for name, expected in dependencies.items():
            path = HERE / name
            if not path.is_file():
                errors.append(f"missing dependency: {name}")
            elif sha256_path(path) != expected:
                errors.append(f"dependency hash mismatch: {name}")

    result = data.get("result")
    if not isinstance(result, dict):
        return errors + ["result missing"]
    if result.get("schema") != "cm2.gate5.physical-prefix-kac-norm-frontier.v1":
        errors.append("result schema mismatch")

    provenance = result.get("provenance", {})
    expected_provenance = {
        "prefix_suffix_manifest": (
            "cm2-gate5-prefix-suffix-norm-manifest-2026-07-15.json"
        ),
        "actual_phase_graph_manifest": (
            "cm2-gate5-actual-phase-graph-manifest-2026-07-15.json"
        ),
        "corrected_Kac_manifest": (
            "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json"
        ),
        "endpoint_rank_manifest": (
            "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
        ),
        "curvature_log_density_manifest": (
            "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json"
        ),
        "density_mesh_recovery_manifest": (
            "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
        ),
        "product_depth_manifest": (
            "cm2-gate45-product-stopped-depth-kernel-manifest-2026-07-16.json"
        ),
        "finite_s_common_mesh_recovery_manifest": (
            "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
        ),
        "gate1_resonance_manifest": (
            "cm2-gate1-canonical-holonomy-resonance-manifest-2026-07-15.json"
        ),
        "gate2_energy_manifest": (
            "cm2-gate2-wasserstein-energy-manifest-2026-07-15.json"
        ),
    }
    for key, expected in expected_provenance.items():
        if provenance.get(key) != expected:
            errors.append(f"provenance mismatch: {key}")

    borel = result.get("physical_borel_prefix_suffix_constants", {})
    expected_borel = {
        "single_physical_prefix_pushforward_TV_norm_upper": "1",
        "single_physical_suffix_pushforward_TV_norm_upper": "1",
        "single_physical_prefix_test_pullback_Linf_norm_upper": "1",
        "single_physical_suffix_test_pullback_Linf_norm_upper": "1",
        "complete_partition_endpoint_pushforward_TV_norm_upper": "1",
        "complete_partition_endpoint_test_pullback_Linf_norm_upper": "1",
        "inserted_current_prefix_suffix_TV_multiplier_upper": "1",
        "return_height_upper": 9,
        "unnormalized_Kac_test_sum_Linf_norm_upper": "9",
        "normalized_tower_source_TV_norm_upper": "9",
        "constants_ignore_Jacobian_only_at_Borel_TV_Linf_level": True,
    }
    for key, expected in expected_borel.items():
        if borel.get(key) != expected:
            errors.append(f"Borel prefix/suffix mismatch: {key}")

    kac = result.get("corrected_Kac_borel_output", {})
    expected_kac = {
        "maximal_physical_occurrence_count": 64,
        "singular_Kac_coordinate_count": 128,
        "shared_row_mark": [1, -1],
        "global_event_current_TV_upper": "16128/5",
        "two_singular_coordinate_l1_TV_upper": "32256/5",
        "worst_case_height_nine_phase_lifted_singular_l1_TV_upper": "290304/5",
        "finite_borel_four_term_Kac_algebra_exact": True,
        "global_signed_scalar_coarea_mass": "0",
        "regular_two_Kac_terms_separately_typed_in_CM2_spaces": False,
        "full_four_term_physical_CM2_output": False,
    }
    for key, expected in expected_kac.items():
        if kac.get(key) != expected:
            errors.append(f"Kac Borel output mismatch: {key}")

    seeds = result.get("one_collision_three_norm_seeds", {})
    for key in (
        "uniform_finite_s_one_collision_dynamic_C1_test_pullback_integrable",
        "uniform_finite_s_one_collision_bidirectional_carrier_C2_bounds",
        "uniform_finite_s_one_collision_bidirectional_log_density_bounds",
        "uniform_finite_s_controlled_atom_standard_family_entry",
        "uniform_one_time_finite_s_stopped_parent_recovery",
        "uniform_finite_s_depth_recovery_moment_for_some_gamma",
        "these_are_occurrence_level_seeds_not_return_word_intertwiners",
    ):
        if seeds.get(key) is not True:
            errors.append(f"one-collision seed missing: {key}")
    for key, expected in {
        "parameter_window": "|s|<=1/400",
        "uniform_finite_s_one_collision_forward_C1_subcost": "151*2^B_s",
        "uniform_finite_s_one_collision_reverse_C1_subcost": "151*2^B_s",
        "uniform_finite_s_one_collision_geometric_subcost": "204*2^B_s",
        "uniform_finite_s_controlled_atom_log_Hoelder_constant": "52",
        "uniform_finite_s_initial_C_mesh": "69986663973833932800",
        "uniform_finite_s_atom_boundary": (
            "Z_s,fw(K,j),Z_s,rev(K,j)<=69986663973833932800*2^K"
        ),
        "uniform_finite_s_recovery_clock": "R_fw+R_rev<=2*A0+2*A1*K",
        "theorem_recovery_constants": "C_p>1 and 0<vartheta_p<1",
        "product_depth_expected_normalization_cost": "E[2^K]=3/2",
    }.items():
        if seeds.get(key) != expected:
            errors.append(f"finite-s seed mismatch: {key}")
    for key in (
        "theorem_recovery_constants_numeric",
        "native_dynamical_stopping_antichain",
        "hereditary_repeated_indicator_recovery",
        "uniform_finite_s_return_prefix_suffix_propagation",
        "return_wide_standard_family_CM2_intertwiner",
        "return_wide_flux_face_CM2_intertwiner",
        "return_wide_dynamic_test_CM2_intertwiner",
        "complete_standard_family_CM2_norm_lift",
        "complete_flux_face_CM2_norm_lift",
        "complete_dynamic_test_CM2_norm_lift",
    ):
        if seeds.get(key) is not False:
            errors.append(f"unsupported one-collision promotion: {key}")

    countermodels = result.get("exact_nonpromotion_countermodels", {})
    for key, expected in {
        "fragment_count": 64,
        "input_TV_mass": "1",
        "input_model_curve_cost": "2",
        "output_model_curve_cost": "65",
        "curve_cost_amplification": "65/2",
        "quadratic_branch_last_inverse_speed": "64",
    }.items():
        if countermodels.get(key) != expected:
            errors.append(f"countermodel mismatch: {key}")
    for key in (
        "TV_Linf_prefix_suffix_constants_imply_regular_density_bound",
        "TV_Linf_prefix_suffix_constants_imply_standard_family_Z_bound",
        "TV_Linf_prefix_suffix_constants_imply_flux_face_atlas_bound",
        "TV_Linf_prefix_suffix_constants_imply_dynamic_C1_test_bound",
    ):
        if countermodels.get(key) is not False:
            errors.append(f"invalid norm implication: {key}")

    phase = result.get("phase_and_route_audit", {})
    for key, expected in {
        "actual_standard_N_component_cycle_gcd": 1,
        "actual_component_phase_gcd_one": True,
        "complete_return_word_operator_blocks": False,
        "operator_Dz_unit_circle_invertibility_from_component_graph": False,
        "operator_Wiener_phase_transfer": False,
        "preferred_route": "direct_standard_N",
        "direct_standard_N_route_needs_separate_phase_tower": False,
    }.items():
        if phase.get(key) != expected:
            errors.append(f"phase/route mismatch: {key}")

    bridge = result.get("gate1_gate2_bridge_audit", {})
    gate1 = bridge.get("gate1", {})
    gate2 = bridge.get("gate2", {})
    for key in (
        "natural_QNL_canonical_stable_limit_converges",
        "Borel_prefix_suffix_contraction_changes_cocycle_holonomy_tail",
        "new_same_carrier_holonomy_bridge_from_gate5_data",
        "gate1_certified",
    ):
        if gate1.get(key) is not False:
            errors.append(f"Gate-1 audit mismatch: {key}")
    if gate2.get("weak_metric_pair_energy_bridge_available") is not True:
        errors.append("Gate-2 positive bridge missing")
    for key in (
        "actual_one_state_full_mass_quotient",
        "query_independent_product_depth_kernel_is_native_physical_quotient",
        "new_full_mass_PPE_bridge_from_gate5_data",
        "gate2_certified",
    ):
        if gate2.get(key) is not False:
            errors.append(f"Gate-2 audit mismatch: {key}")

    completion = result.get("completion", {})
    for key in (
        "physical_Borel_TV_Linf_prefix_suffix_constants",
        "explicit_corrected_singular_Kac_Borel_output_envelope",
        "one_collision_three_norm_seeds",
        "uniform_finite_s_one_collision_three_norm_seeds",
        "uniform_one_time_finite_s_stopped_parent_recovery",
        "actual_component_phase_gcd_one",
    ):
        if completion.get(key) is not True:
            errors.append(f"missing certified completion: {key}")
    for key in (
        "immutable_complete_return_word_operator_registry",
        "regular_density_prefix_suffix_intertwiner",
        "standard_family_CM2_norm_lift",
        "flux_face_CM2_norm_lift",
        "dynamic_test_CM2_norm_lift",
        "theorem_recovery_constants_numeric",
        "native_dynamical_stopping_antichain",
        "hereditary_repeated_indicator_recovery",
        "full_four_term_physical_Kac_CM2_output",
        "operator_Wiener_phase_transfer",
        "gate1_certified",
        "gate2_certified",
        "gate5_certified",
    ):
        if completion.get(key) is not False:
            errors.append(f"unsupported completion: {key}")

    verdict = data.get("verdict", {})
    if verdict.get("physical_Borel_prefix_suffix_and_Kac_output") != "CERTIFIED":
        errors.append("Borel verdict mismatch")
    if verdict.get("one_collision_three_norm_seeds") != "CERTIFIED":
        errors.append("local seed verdict mismatch")
    if verdict.get("uniform_finite_s_one_collision_recovery_seed") != "CERTIFIED":
        errors.append("finite-s recovery seed verdict mismatch")
    if verdict.get("physical_three_CM2_norm_lifts") != "NOT_CERTIFIED":
        errors.append("three-norm verdict must fail-close")
    if verdict.get("gate5") != "NOT_CERTIFIED":
        errors.append("Gate-5 verdict must fail-close")
    return errors


def check_replay(data: dict[str, Any]) -> list[str]:
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    try:
        import cm2_gate5_physical_prefix_kac_norm_frontier_cert as cert

        actual = cert.certify()
    except Exception as exc:
        return [f"certificate replay failed: {exc}"]
    return [] if data.get("result") == actual else ["full certificate replay mismatch"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1

    errors = check_structure(data)
    if args.replay and not errors:
        errors.extend(check_replay(data))
    if errors:
        print("GATE5_PHYSICAL_PREFIX_KAC_NORM_FRONTIER_INTEGRITY: FAIL")
        for error in errors:
            print(f"  {error}")
        return 1

    if args.self_test:
        tampered = copy.deepcopy(data)
        tampered["dependencies"].pop(
            "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
        )
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (finite-s dependency deletion accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["physical_borel_prefix_suffix_constants"][
            "single_physical_prefix_pushforward_TV_norm_upper"
        ] = "2"
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (Borel constant tamper accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["completion"]["standard_family_CM2_norm_lift"] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported CM2 norm lift accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["one_collision_three_norm_seeds"][
            "theorem_recovery_constants_numeric"
        ] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (numeric recovery theorem constants accepted)")
            return 1
        tampered = copy.deepcopy(data)
        tampered["result"]["gate1_gate2_bridge_audit"]["gate2"][
            "new_full_mass_PPE_bridge_from_gate5_data"
        ] = True
        if not check_structure(tampered):
            print("SELF_TEST: FAIL (unsupported Gate-2 bridge accepted)")
            return 1
        print("SELF_TEST: PASS")
        print("  finite-s dependency deletion rejected")
        print("  Borel contraction tamper rejected")
        print("  unsupported CM2 norm promotion rejected")
        print("  unsupported numeric recovery constants rejected")
        print("  unsupported Gate-2 bridge rejected")
        return 0

    print("GATE5_PHYSICAL_BOREL_PREFIX_SUFFIX_CONSTANTS: CERTIFIED")
    print("GATE5_CORRECTED_SINGULAR_KAC_BOREL_OUTPUT_ENVELOPE: CERTIFIED")
    print("GATE5_UNIFORM_FINITE_S_ONE_COLLISION_RECOVERY_SEEDS: CERTIFIED")
    if args.integrity_only:
        print("GATE5_PHYSICAL_PREFIX_KAC_NORM_FRONTIER_INTEGRITY: PASS")
        return 0
    print("GATE5_PHYSICAL_THREE_CM2_NORM_LIFTS: NOT_CERTIFIED")
    print("GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
