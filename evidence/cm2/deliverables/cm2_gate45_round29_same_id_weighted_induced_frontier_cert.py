#!/usr/bin/env python3
"""Round-29 same-ID weighted-tail / induced-strong connectability audit.

This append-only leaf joins the finite nonempty R1/Q2 registries, the Q2
homogeneity/recut branch-rule payload, the round-28 weighted-tail transfer
theorem, and the numerical Growth/recovery stack.  It certifies the strongest
currently nonempty same-origin finite payload and then freezes the exact type
breaks that prevent numerical C_fw/C_rev/q, a strong cemetery charge, or an
induced strong Lasota--Yorke coefficient.

In particular, Q2 cells are survivor cells, not R_n first-return summands;
Borel restriction IDs are not standard-family recovery carriers; universal
recut branch rules are not actual parent-curve recut instances; and a
collision-null singular set does not control characteristic-cut boundary Z.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round29-same-id-weighted-induced-frontier.v1"
MANIFEST_SCHEMA = (
    "cm2.gate45.round29-same-id-weighted-induced-frontier.manifest.v1"
)
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate45-round29-same-id-weighted-induced-frontier-manifest-2026-07-18.json"
)

DEPENDENCIES = {
    "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json": (
        "120a3f1cba9f23cc4b2a9753491022f8143175810b19f1a9f9d8ee0214d66b60"
    ),
    "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json": (
        "9fe09f46e2201a54e000ea67ac09521ce73e1fe012b5205e12541805787683b3"
    ),
    "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json": (
        "eef1071c1f4973892bf5e450421f3b91de7a2b426165e6a8c6f8bb4404eeac57"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate45-induced-strong-coefficient-obstruction-manifest-2026-07-18.json": (
        "bad4bd8c12bccdcfad7210d44ed85fb023615c6db7aca9954e815a4729ce31e6"
    ),
    "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json": (
        "f846df9e0afe3e81bedb9cb1a4cb80446d8b79eabb9fd6577e223f6aa1e282ab"
    ),
    "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json": (
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140"
    ),
}

TAIL_A = Q(550000, 147)
TAIL_R = Q(111718729, 111718750)
F5_TWO_STEP = Q(20736000000, 32521433569)
F6_TWO_STEP = Q(3, 100000)
VARTTHETA_P = Q(360134800, 360493663)


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency mismatch: {name}")
        value = parse_json_text(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency root type: {name}")
        loaded[name] = value

    nonempty = loaded[
        "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json"
    ]
    r1 = nonempty["result"]["R1_nonempty_adaptive_component_registry"]
    q2 = nonempty["result"]["Q2_nonempty_adaptive_component_registry"]
    require(r1["materialized_nonempty_adaptive_component_count"] == 4216, "R1 count")
    require(q2["materialized_nonempty_depth2_adaptive_component_count"] == 114006, "Q2 count")
    require(q2["origin_atom_count"] == 114006, "Q2 origin count")
    require(q2["terminal_adaptive_cell_count"] == 114006, "Q2 terminal count")
    require(q2["recut_depth_histogram"] == {"0": 114006}, "Q2 no wall recut")
    require(q2["finite_wall_unresolved_outer_cell_count"] == 0, "Q2 outer count")
    require(q2["complete_frozen_Q2_inner_anchor_depth2_key_ownership"] is True, "Q2 ownership")
    require(
        q2["finite_source_registry"]
        == "all frozen strict Q2-inner depth<=16 atoms",
        "Q2 nonempty source contract",
    )

    homog = loaded[
        "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json"
    ]
    hg = homog["result"]["Q2_two_step_homogeneity_and_recut_registry"]
    slots = homog["result"]["Q2_numeric_F5_F6_slot_registry"]
    types = homog["result"]["strong_type_separation"]
    require(
        homog["result"]["provenance"]["source_registry"]
        == "round26 strict Q2-inner depth<=16 admitted atoms",
        "Q2 homogeneous source contract",
    )
    require(hg["strict_Q2_atom_count"] == 114006, "homogeneous Q2 source count")
    require(hg["fully_materialized_Q2_atom_count"] == 114006, "homogeneous Q2 count")
    require(hg["blocked_Q2_atom_count"] == 0, "homogeneous blocker")
    require(hg["canonical_recut_branch_rule_id_count"] == 228012, "recut rules")
    require(hg["actual_curve_recut_instance_id_count"] == 0, "actual recut scope")
    require(slots["F5_universal_branch_rule_slot_count"] == 114006, "F5 count")
    require(slots["F6_universal_branch_rule_slot_count"] == 114006, "F6 count")
    require(slots["two_step_adapted_unstable_inverse_strict_upper"] == str(F5_TWO_STEP), "F5 value")
    require(slots["two_step_canonical_recut_log_variation_strict_upper"] == str(F6_TWO_STEP), "F6 value")
    require(slots["actual_curve_instance_slot_count"] == 0, "curve instance scope")
    require(types["joined_prior_restriction_id_count"] == 114006, "restriction join")
    require(types["numeric_C_fw_count"] == 0, "Cfw scope")
    require(types["numeric_C_rev_count"] == 0, "Crev scope")
    require(types["numeric_strong_q2_count"] == 0, "q2 scope")

    prior_q2 = loaded[
        "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json"
    ]["result"]
    registry = prior_q2["Q2_exact_mass_and_restriction_registry"]
    charge = prior_q2["Q2_symbolic_strong_charge_registry"]
    require(registry["common_forward_reverse_restriction_id_count"] == 114006, "Borel restrictions")
    require(registry["common_strong_recovery_carrier_count"] == 0, "strong carriers")
    require(charge["symbolic_q2_charge_count"] == 114006, "symbolic q2")
    require(charge["numeric_q2_count"] == 0, "numeric q2")

    weighted = loaded[
        "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json"
    ]
    require(weighted["verdict"]["survivor_conditioned_Lp_weighted_tail_transfer"] == "CERTIFIED_CONDITIONAL_THEOREM", "Lp theorem")
    status = weighted["result"]["current_frozen_stack_instantiation"]["new_transfer_hypothesis_status"]
    require(status["uniform_survivor_conditioned_Lp_first_return_envelope_count"] == 0, "Lp scope")
    require(status["numeric_strong_cemetery_charge_rows"] == 0, "cemetery scope")

    arbitrary = loaded[
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    ]
    level = arbitrary["result"]["arbitrary_n_Rn_Qn_level_and_mass_schema"]
    require(level["level_identity_mod_null"] == "Q_(n-1)=R_n disjoint_union Q_n", "Rn/Qn typing")
    require(level["q_weighted_strong_tail"] == "NOT_CERTIFIED", "weighted scope")

    numeric = loaded[
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    ]
    summary = numeric["replay_summary"]
    require(summary["vartheta_p"] == str(VARTTHETA_P), "vartheta")
    require(summary["A0"] == 301500 and summary["A1"] == 1005, "recovery clocks")
    require(summary["native_gamma"] == "1/12060", "gamma")
    require(numeric["verdict"]["complete_numeric_C_fw_C_rev_final_q"] == "NOT_CERTIFIED", "numeric q scope")

    obstruction = loaded[
        "cm2-gate45-induced-strong-coefficient-obstruction-manifest-2026-07-18.json"
    ]
    require(obstruction["verdict"]["open_to_induced_coefficient_nonimplication"] == "CERTIFIED", "operator obstruction")
    require(obstruction["verdict"]["induced_strong_coefficient"] == "NOT_CERTIFIED", "induced scope")

    faces = loaded[
        "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
    ]
    require(faces["verdict"]["F14_through_F18"] == "NOT_CERTIFIED", "F14-F18")
    require(faces["verdict"]["complete_18_field_operator_blocks"] == 0, "operator blocks")
    return loaded


def same_id_q2_skeleton(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    nonempty = loaded[
        "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json"
    ]["result"]
    r1 = nonempty["R1_nonempty_adaptive_component_registry"]
    q2 = nonempty["Q2_nonempty_adaptive_component_registry"]
    homog = loaded[
        "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json"
    ]["result"]
    slots = homog["Q2_numeric_F5_F6_slot_registry"]
    hg = homog["Q2_two_step_homogeneity_and_recut_registry"]
    prior = loaded[
        "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json"
    ]["result"]
    registry = prior["Q2_exact_mass_and_restriction_registry"]

    return {
        "join_scope": "all frozen strict finite Q2-inner origin atoms at depth<=16",
        "origin_identity_field": "time2_atom_id=full-core-time2:sha256(canonical_terminal_identity)",
        "source_registry_contracts": {
            "nonempty_registry": "all frozen strict Q2-inner depth<=16 atoms",
            "homogeneity_payload": "round26 strict Q2-inner depth<=16 admitted atoms",
            "both_replay_the_same_frozen_round26_strict_Q2_inner_set": True,
        },
        "same_origin_join_policy": (
            "one exhaustive frozen time2_atom_id source registry; one depth-zero "
            "adaptive cell, one mass/restriction row and one homogeneous branch-rule "
            "payload per origin"
        ),
        "nonempty_Q2_component_cell_count": q2[
            "materialized_nonempty_depth2_adaptive_component_count"
        ],
        "Q2_origin_atom_count": q2["origin_atom_count"],
        "Q2_adaptive_recut_depth_histogram": q2["recut_depth_histogram"],
        "Q2_finite_outer_count": q2["finite_wall_unresolved_outer_cell_count"],
        "Q2_parameter_averaged_coordinate_base_mass_exact": q2[
            "parameter_averaged_admitted_coordinate_base_mass_exact"
        ],
        "Q2_exact_symbolic_collision_area_mass_row_count": registry[
            "exact_symbolic_collision_area_mass_slot_count"
        ],
        "Q2_common_Borel_fw_rev_restriction_id_count": registry[
            "common_forward_reverse_restriction_id_count"
        ],
        "Q2_two_step_physical_homogeneity_child_count": hg[
            "two_step_homogeneous_child_id_count"
        ],
        "Q2_canonical_recut_branch_rule_id_count": hg[
            "canonical_recut_branch_rule_id_count"
        ],
        "Q2_F5_universal_branch_rule_slot_count": slots[
            "F5_universal_branch_rule_slot_count"
        ],
        "Q2_F6_universal_branch_rule_slot_count": slots[
            "F6_universal_branch_rule_slot_count"
        ],
        "Q2_F5_two_step_adapted_inverse_strict_upper": str(F5_TWO_STEP),
        "Q2_F6_two_step_log_variation_strict_upper": str(F6_TWO_STEP),
        "same_origin_finite_Q2_skeleton_row_count": 114006,
        "same_origin_finite_Q2_skeleton_status": "CERTIFIED_114006",
        "strong_type_boundary": {
            "Q2_level_type": "Q_2_SURVIVOR_NOT_R_n_FIRST_RETURN_SUMMAND",
            "actual_parent_curve_recut_instance_id_count": 0,
            "common_standard_family_recovery_carrier_count": registry[
                "common_strong_recovery_carrier_count"
            ],
            "numeric_C_fw_count": 0,
            "numeric_C_rev_count": 0,
            "numeric_q2_count": 0,
            "F7_characteristic_cut_growth_slot_count": 0,
            "F14_through_F18_slot_count": 0,
            "Borel_restriction_id_is_standard_family_recovery_carrier": False,
            "branch_rule_id_is_actual_parent_curve_recut_instance_id": False,
            "invariant_area_Jacobian_is_unstable_Jacobian": False,
            "Q2_survivor_charge_is_first_return_Rn_charge": False,
        },
        "finite_R1_first_return_frontier": {
            "nonempty_R1_component_cell_count": r1[
                "materialized_nonempty_adaptive_component_count"
            ],
            "parameter_averaged_coordinate_base_mass_exact": r1[
                "parameter_averaged_coordinate_base_mass_exact"
            ],
            "candidate_local_maturity": "13/18",
            "complete_F14_through_F18_slot_count": 0,
            "numeric_first_return_C_fw_rows": 0,
            "numeric_first_return_C_rev_rows": 0,
            "numeric_first_return_q_rows": 0,
        },
    }


def weighted_connectability() -> dict[str, Any]:
    rows = [
        {
            "index": 1,
            "interface": "positive_mass_Rn_first_return_component_on_fixed_parameter_slice",
            "current_nonempty_count": 4216,
            "current_scope": "finite_R1_inner_cells_only_not_complete_limiting_R1_or_arbitrary_n",
            "status": "PARTIAL_FINITE_ANCHOR",
        },
        {
            "index": 2,
            "interface": "same_component_actual_parent_curve_recuts_and_common_fw_rev_strong_carrier",
            "current_complete_count": 0,
            "first_blocker": "actual_recut_instance_and_standard_family_carrier_IDs_absent",
            "status": "NOT_CERTIFIED",
        },
        {
            "index": 3,
            "interface": "numeric_C_fw_C_rev_and_once_charged_c_equals_q_over_m",
            "current_complete_count": 0,
            "first_blocker": "F7_and_F14_F17_operator_costs_absent",
            "status": "NOT_CERTIFIED",
        },
        {
            "index": 4,
            "interface": "uniform_fixed_s_survivor_conditioned_or_global_Lp_envelope",
            "current_complete_count": 0,
            "first_blocker": "no_fixed_s_same_ID_numeric_charge_disintegration",
            "status": "NOT_CERTIFIED",
        },
        {
            "index": 5,
            "interface": "numerical_strong_singularity_cemetery_charge",
            "current_complete_count": 0,
            "first_blocker": "collision_null_mass_does_not_control_boundary_Z_or_trace_norm",
            "status": "NOT_CERTIFIED",
        },
        {
            "index": 6,
            "interface": "induced_common_strong_space_Lasota_Yorke_block",
            "current_complete_count": 0,
            "first_blocker": "weighted_tail_and_F14_F18_common_block_absent",
            "status": "NOT_CERTIFIED",
        },
    ]
    return {
        "tail_prefactor_A": str(TAIL_A),
        "tail_block_factor_r": str(TAIL_R),
        "N_open": "one_uniform_theorem_supplied_integer>=1_not_numeric",
        "conditional_survivor_Lp_transfer_theorem": "CERTIFIED",
        "uniform_survivor_conditioned_Lp_envelope_count": 0,
        "global_physical_first_return_Lp_envelope_count": 0,
        "compatible_pointwise_first_return_envelope_count": 0,
        "physical_Rn_q_density_rows_ready_for_tail_sum": 0,
        "Q2_payload_directly_admissible_as_Rn_return_charge_row_count": 0,
        "parameter_quantifier_required_by_tail": "every_fixed_|s|<=1/400",
        "finite_registry_mass_currently_globally_summed_as": "parameter_averaged_coordinate_base_mass",
        "parameter_averaged_mass_implies_uniform_fixed_s_Lp_envelope": False,
        "required_interfaces": rows,
        "required_interfaces_sha256": canonical_digest(rows),
        "complete_interface_count": 0,
    }


def cemetery_countermodel() -> dict[str, Any]:
    samples = []
    for n in (1, 2, 4, 8, 16, 32, 64):
        component_length = Q(1, n + 1)
        component_weight = component_length
        boundary_z = (n + 1) * component_weight / component_length
        require(boundary_z == n + 1, "countermodel arithmetic")
        samples.append(
            {
                "N_internal_cut_points": n,
                "singular_set_Lebesgue_mass": "0",
                "complement_component_count": n + 1,
                "each_component_length": str(component_length),
                "each_component_weight": str(component_weight),
                "boundary_Z_sum_weight_over_length": str(boundary_z),
            }
        )
    return {
        "model": "uniform_standard_pair_on_[0,1]_cut_at_S_N={j/(N+1):1<=j<=N}",
        "singular_set_mass_for_every_finite_N": "0",
        "post_cut_component_count": "N+1",
        "post_cut_boundary_Z": "sum_components(weight/length)=N+1",
        "unbounded_limit": "boundary_Z_to_infinity_as_N_to_infinity",
        "exact_samples": samples,
        "samples_sha256": canonical_digest(samples),
        "certified_nonimplication": (
            "collision_SRB_null_singular_or_core_boundary_cemetery_does_not_by_itself_"
            "bound_strong_characteristic_cut_boundary_Z_or_trace_charge"
        ),
        "physical_CM2_impossibility_claimed": False,
        "needed_escape": (
            "summable_singularity_complexity_or_direct_trace_Z_bound_on_the_same_"
            "strong_carrier"
        ),
    }


def induced_frontier() -> dict[str, Any]:
    rows = [
        {
            "record": "measurable_induced_L1_Perron_norm",
            "current": "CERTIFIED_EQUAL_1",
            "promotes_strong_coefficient": False,
        },
        {
            "record": "open_operator_scalar_b_core",
            "current": "CERTIFIED_FOR_O_EQUALS_L_M_C",
            "promotes_strong_coefficient": False,
        },
        {
            "record": "weighted_first_return_excursion_tail",
            "current": "NOT_CERTIFIED",
            "promotes_strong_coefficient": False,
        },
        {
            "record": "strong_cemetery_charge",
            "current": "NOT_CERTIFIED",
            "promotes_strong_coefficient": False,
        },
        {
            "record": "F14_F18_common_operator_block",
            "current": "0_COMPLETE_BLOCKS",
            "promotes_strong_coefficient": False,
        },
        {
            "record": "common_fw_rev_strong_space_and_restriction",
            "current": "NOT_CERTIFIED",
            "promotes_strong_coefficient": False,
        },
    ]
    return {
        "numeric_recovery_inputs": {
            "vartheta_p": str(VARTTHETA_P),
            "A0": 301500,
            "A1": 1005,
            "native_gamma": "1/12060",
            "all_iterate_D_std_strict_upper": "30000000",
        },
        "typed_nonimplications": {
            "open_O_equals_L_M_C_coefficient_is_Rn_induced_coefficient": False,
            "L1_norm_one_is_strong_Lasota_Yorke_coefficient": False,
            "area_Jacobian_one_is_unstable_Jacobian_or_strong_norm_cost": False,
            "product_depth_mark_is_physical_first_return_recovery_history": False,
            "finite_fixed_H_restart_is_unbounded_return_history_recovery": False,
        },
        "assembly_rows": rows,
        "assembly_rows_sha256": canonical_digest(rows),
        "complete_strong_assembly_row_count": 0,
        "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "audit_policy": "exact_frozen_manifest_join_plus_exact_type_and_countermodel_audit",
            "parameter_scope": "uniform_target_is_every_fixed_|s|<=1/400",
        },
        "same_origin_finite_Q2_strong_skeleton": same_id_q2_skeleton(loaded),
        "weighted_tail_connectability": weighted_connectability(),
        "strong_cemetery_mass_zero_nonimplication": cemetery_countermodel(),
        "induced_strong_Lasota_Yorke_frontier": induced_frontier(),
        "strict_nonpromotion": {
            "Q2_same_origin_skeleton_is_numeric_C_fw_C_rev_q": False,
            "Q2_survivor_cells_are_Rn_first_return_summands": False,
            "parameter_averaged_mass_is_uniform_fixed_s_strong_moment": False,
            "collision_null_cemetery_mass_is_zero_strong_cemetery_charge": False,
            "open_operator_bound_is_induced_operator_bound": False,
            "conditional_weighted_transfer_theorem_implies_current_weighted_tail": False,
            "strong_q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    payload = copy.deepcopy(result)
    result["internal_replay_digest"] = canonical_digest(payload)
    return result


def verdict(result: dict[str, Any]) -> dict[str, Any]:
    skeleton = result["same_origin_finite_Q2_strong_skeleton"]
    return {
        "same_origin_finite_Q2_component_mass_restriction_homogeneity_F5_F6_skeleton": (
            skeleton["same_origin_finite_Q2_skeleton_status"]
        ),
        "finite_R1_first_return_component_anchors": "CERTIFIED_4216",
        "Q2_actual_parent_curve_recut_instances": "NOT_CERTIFIED_COUNT_0",
        "Q2_common_standard_family_recovery_carriers": "NOT_CERTIFIED_COUNT_0",
        "numeric_C_fw_C_rev_q": "NOT_CERTIFIED_COUNT_0",
        "Q2_payload_is_Rn_first_return_charge": False,
        "mass_zero_implies_strong_cemetery_charge_zero": False,
        "collision_null_to_boundary_Z_nonimplication": "CERTIFIED_EXACT_COUNTERMODEL",
        "survivor_conditioned_or_global_Lp_physical_envelope": "NOT_CERTIFIED_COUNT_0",
        "strong_q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def write_manifest(path: Path, verifier_path: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": dict(DEPENDENCIES),
        "result": result,
        "verdict": verdict(result),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate45_round29_same_id_weighted_induced_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print("SAME_ORIGIN_FINITE_Q2_STRONG_SKELETON: CERTIFIED_114006")
    print("NUMERIC_C_FW_C_REV_Q: NOT_CERTIFIED_COUNT_0")
    print("COLLISION_NULL_TO_STRONG_CEMETERY_NONIMPLICATION: CERTIFIED")
    print("STRONG_Q_WEIGHTED_TAIL: NOT_CERTIFIED")
    print("INDUCED_STRONG_LASOTA_YORKE: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
