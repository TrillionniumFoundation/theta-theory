#!/usr/bin/env python3
"""Materialized interface and obstruction for the physical first-return partition.

The frozen artifacts provide three different objects which must not be
identified:

* 128 Borel stopping ledgers on full three-coordinate ``(z,s,h)`` germs;
* 128 positive ``(z,h)`` charged subatoms at the fixed phase coordinate
  ``s=0``, with a suffix-relative first-core word.  Only four of them are
  contained in the previously registered full germs; the other 124 use new
  source centers and cannot be joined by occurrence ID alone;
* four much smaller ``(z,h)`` post-core boxes, three with a finite local
  return and one surviving through time 2018.

This certificate performs the exact keyed join between those objects.  It
materializes every charged entrance atom, its germ ledger, first-core slot,
dyadic labelled area, and every available local R_n/Q_n candidate atom.

The join also exposes the decisive physical obstruction.  At a fixed
parameter the available atoms are one-dimensional analytic source curves,
whereas every frozen collision core is a two-dimensional positive-SRB-mass
rectangle.  Thus the current atoms have zero collision-SRB area and cannot
be a source/core partition.  Their positive labelled ``dz dh`` areas are not
physical masses.  No global return mass, survivor mass, cemetery tail, or
induced operator is promoted.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import cm2_gate34_all_occurrence_first_core_stopping_cert as stopping
import cm2_gate34_local_core_return_tail_cert as local_return
import cm2_gate34_selected_germ_core_cemetery_ledger_cert as ledger


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json": (
        "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8"
    ),
    "cm2_gate34_parameter_dq_all_scale_shell_cert.py": (
        "ea5b6b7fa265990b1eaa1c106e2c0f82f024b58951bbe65ff55757cbc23df458"
    ),
    "cm2-gate34-selected-germ-core-cemetery-ledger-manifest-2026-07-17.json": (
        "ae6c31fb385070bec1c85463d0d125a504089da6c035c8d34d892a768a6f8c2e"
    ),
    "cm2_gate34_selected_germ_core_cemetery_ledger_cert.py": (
        "c97279ca88ff8ce748b2c9a5d265563e5b550cfe1881f3c56e9d4e2a6ff4ae2a"
    ),
    "cm2-gate34-all-occurrence-positive-core-hit-manifest-2026-07-17.json": (
        "fa590ec6fbaeb08b6f5d9e38d45c2fdc3a06dc170451ded93892f7c531653b51"
    ),
    "cm2_gate34_all_occurrence_positive_core_hit_cert.py": (
        "98c7642856bac56a5309a0fcc6a362e971f25f08c3b52292aaa13eace7d2e76f"
    ),
    "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json": (
        "a40b52dcbeef8c9f3471115b2bbd2c438cc6e130c72bd619dd794d8925d97171"
    ),
    "cm2_gate34_all_occurrence_first_core_stopping_cert.py": (
        "8a22c1a2483822b849562acb06775298a8e9d3a84d753e29ebe86229d35ad1fb"
    ),
    "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json": (
        "d66c8da53846ae86c373de5917e706fa183bfca265f0e4fb83a9be1c204dd053"
    ),
    "cm2_gate34_local_core_return_tail_cert.py": (
        "622d09d937d14fa6b5903e698e6cbe5fb223b1b14549d4d7c69b696bc002056a"
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(name: str) -> dict[str, Any]:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
        if path.suffix == ".json":
            loaded[name] = load_json(name)

    cores = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]["result"]["physical_return_core_registry"]
    assert cores["physical_compact_homogeneous_core_count"] == 24
    assert cores["collision_SRB_normalized_mass_strict_lower_using_pi_lt_22_over_7"] == "147/550000"

    germs = loaded[
        "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json"
    ]["result"]["selected_parameter_dq_all_scale_germ_registry"]
    assert germs["selected_occurrence_parameter_germ_count"] == 64
    assert germs["oriented_actual_parameter_tube_germ_count"] == 128

    borel = loaded[
        "cm2-gate34-selected-germ-core-cemetery-ledger-manifest-2026-07-17.json"
    ]["result"]
    assert borel["selected_branch_stopping_registry"]["oriented_branch_ledger_count"] == 128
    assert borel["measurable_core_cemetery_stopping_theorem"][
        "exact_measure_decomposition_for_every_finite_germ_measure"
    ] is True

    positive = loaded[
        "cm2-gate34-all-occurrence-positive-core-hit-manifest-2026-07-17.json"
    ]
    assert positive["verdict"]["positive_all_scale_core_hit_oriented_branches_128"] == "CERTIFIED"

    first = loaded[
        "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json"
    ]
    assert first["verdict"]["charged_first_core_stopping_cylinders_128"] == "CERTIFIED"
    assert first["result"]["strict_nonpromotion"]["whole_germ_domain_first_core_stopping"] == "NOT_CERTIFIED"

    returns = loaded[
        "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json"
    ]
    assert returns["verdict"]["local_first_return_current_cylinders_3"] == "CERTIFIED"
    assert returns["verdict"]["local_tau_core_plus_gt_2018_survivor_boxes_1"] == "CERTIFIED"
    assert returns["verdict"]["full_24_core_induced_operator"] == "NOT_CERTIFIED"

    # Re-run each dependency's own hash admission before using its helpers.
    ledger.load_dependencies()
    stopping.load_dependencies()
    local_return.load_dependencies()
    return loaded


def dyadic(power: int) -> dict[str, int]:
    assert power >= 0
    return {"numerator": 1, "denominator_power_of_two": power}


def charged_entrance_atoms() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    maximal_rows, _registry = stopping.current.load_maximal_rows()
    by_occurrence = {row["occurrence_id"]: row for row in maximal_rows}
    assert len(by_occurrence) == 64
    specifications = stopping.occurrence_specifications(maximal_rows)

    germ_rows = ledger.selected_germ_rows()
    germ_by_occurrence = {row["occurrence_id"]: row for row in germ_rows}
    branch_rows = ledger.branch_ledgers(germ_rows)
    ledger_by_key = {
        (row["occurrence_id"], row["side"]): row for row in branch_rows
    }
    assert len(germ_by_occurrence) == 64
    assert len(ledger_by_key) == 128

    stopping.all_charge.refresh_arb_constants()
    atoms: list[dict[str, Any]] = []
    total_labelled_area = Q(0)
    for occurrence_id, specification in sorted(specifications.items()):
        original = by_occurrence[occurrence_id]
        owner = stopping.physical_row_and_owner_audit(original, specification)
        germ = germ_by_occurrence[occurrence_id]
        radius_power = int(specification["radius_power"])
        radius = Q(1, 2**radius_power)
        germ_half_width = Q(germ["base_half_width"])
        germ_parameter_radius = Q(germ["parameter_magnitude_interval"][1])
        original_z = Q(original["witness"]["z"])
        charged_z = Q(specification["z"])
        z_contained = abs(charged_z - original_z) + radius < germ_half_width
        h_contained = radius < germ_parameter_radius
        assert h_contained
        assert germ["source_event_chart"] == specification["source_chart"]

        for side in ("hit", "miss"):
            branch = stopping.replay_first_stopping_branch(
                original,
                specification,
                side,
                owner["source_owner_audit_id"],
            )
            stopping_ledger = ledger_by_key[(occurrence_id, side)]
            expected_sign = (
                germ["hit_parameter_sign"]
                if side == "hit"
                else germ["miss_parameter_sign"]
            )
            assert stopping_ledger["parameter_sign"] == expected_sign
            slot_payload = {
                "branch_ledger_id": stopping_ledger["branch_ledger_id"],
                "time": branch["first_core_stopping_time_from_regular_suffix"],
                "core_id": branch["destination_core_id"],
            }
            candidate_slot_id = "core-hit:" + canonical_digest(slot_payload)
            typed_slot_id = candidate_slot_id if z_contained else None
            atom_payload = {
                "occurrence_id": occurrence_id,
                "side": side,
                "source_chart": specification["source_chart"],
                "z_center": str(charged_z),
                "radius_power": radius_power,
            }
            atom_area = 2 * radius * radius
            total_labelled_area += atom_area
            atoms.append({
                "entrance_atom_id": "entrance-atom:" + canonical_digest(atom_payload),
                "occurrence_id": occurrence_id,
                "parameter_side": side,
                "parameter_sign": expected_sign,
                "source_chart": specification["source_chart"],
                "occurrence_matched_selected_germ_id": germ["germ_id"],
                "occurrence_matched_stopping_ledger_id": stopping_ledger[
                    "branch_ledger_id"
                ],
                "source_owner_audit_id": owner["source_owner_audit_id"],
                "upstream_first_stopping_branch_id": branch["first_stopping_branch_id"],
                "source_coordinates": {
                    "ambient_parameterized_germ_coordinates": ["z", "s", "h"],
                    "charged_atom_coordinates": ["z", "h"],
                    "fixed_phase_coordinate": "s=0",
                    "z_center": str(charged_z),
                    "z_half_width": dyadic(radius_power),
                    "parameter_magnitude_interval": ["0_open", str(radius)],
                    "parameter_sign": expected_sign,
                },
                "z_interval_strictly_contained_in_occurrence_matched_germ": (
                    z_contained
                ),
                "s_equals_zero_contained_in_occurrence_matched_germ": True,
                "h_interval_strictly_contained_in_occurrence_matched_germ": (
                    h_contained
                ),
                "typed_existing_germ_ledger_attachment_admitted": z_contained,
                "occurrence_id_only_ledger_join_rejected": not z_contained,
                "parameterized_ambient_dimension": 3,
                "parameterized_charged_atom_dimension": 2,
                "fixed_parameter_collision_source_dimension": 1,
                "labelled_dz_dh_area": dyadic(2 * radius_power - 1),
                "ambient_dz_ds_dh_Lebesgue_volume": "0",
                "suffix_relative_first_core_time": branch[
                    "first_core_stopping_time_from_regular_suffix"
                ],
                "source_collision_count_to_regular_suffix": branch[
                    "source_collision_count_to_regular_suffix"
                ],
                "destination_core_id": branch["destination_core_id"],
                "candidate_countable_first_core_slot_id": candidate_slot_id,
                "typed_existing_ledger_first_core_slot_id": typed_slot_id,
                "typed_slot_is_in_materialized_horizon_8_prefix": (
                    branch["first_core_stopping_time_from_regular_suffix"] <= 8
                    if z_contained else None
                ),
                "every_suffix_preterminal_state_strictly_outside_C24": True,
                "terminal_state_strictly_inside_unique_core": True,
                "complete_itinerary_sha256": branch["complete_itinerary_sha256"],
                "classification_records_sha256": branch[
                    "classification_records_sha256"
                ],
                "source_relative_first_event_guard": "NOT_CERTIFIED_IN_THIS_LEAF",
                "collision_SRB_mass": "0_AT_EACH_FIXED_PARAMETER",
            })

    atoms.sort(key=lambda row: (row["occurrence_id"], row["parameter_side"]))
    assert len(atoms) == 128
    assert len({row["entrance_atom_id"] for row in atoms}) == 128
    assert sum(row["typed_existing_germ_ledger_attachment_admitted"] for row in atoms) == 4
    assert sum(row["occurrence_id_only_ledger_join_rejected"] for row in atoms) == 124
    assert len({
        row["occurrence_matched_stopping_ledger_id"]
        for row in atoms
        if row["typed_existing_germ_ledger_attachment_admitted"]
    }) == 4
    assert len({
        row["typed_existing_ledger_first_core_slot_id"]
        for row in atoms
        if row["typed_existing_germ_ledger_attachment_admitted"]
    }) == 4
    assert sum(
        row["typed_slot_is_in_materialized_horizon_8_prefix"] is True
        for row in atoms
    ) == 0
    assert len({row["destination_core_id"] for row in atoms}) == 14

    positive_manifest = load_json(
        "cm2-gate34-all-occurrence-positive-core-hit-manifest-2026-07-17.json"
    )
    upstream_total = Q(
        positive_manifest["result"]["all_occurrence_positive_core_hit_registry"]
        ["all_64_labelled_base_parameter_coordinate_volume"]
    )
    assert total_labelled_area == upstream_total
    radius_histogram = Counter(
        row["source_coordinates"]["z_half_width"]["denominator_power_of_two"]
        for row in atoms
    )
    assert radius_histogram == Counter({80: 64, 100: 16, 120: 32, 180: 4, 200: 8, 220: 4})
    summary = {
        "charged_entrance_atom_count": 128,
        "occurrence_matched_existing_germ_candidate_count": 128,
        "typed_existing_germ_ledger_attachment_count": 4,
        "occurrence_only_ledger_join_rejection_count": 124,
        "unique_typed_existing_first_core_slot_count": 4,
        "typed_slots_inside_materialized_horizon_8_prefix": 0,
        "typed_slots_after_materialized_horizon_8_prefix": 4,
        "distinct_destination_core_count": 14,
        "radius_power_histogram_by_oriented_atom": {
            str(key): value for key, value in sorted(radius_histogram.items())
        },
        "total_positive_labelled_dz_dh_area": str(total_labelled_area),
        "total_positive_labelled_dz_dh_area_strict_lower_bound": "2^-153",
        "total_positive_labelled_dz_dh_area_strict_upper_bound": "2^-152",
        "total_ambient_dz_ds_dh_volume": "0",
        "fixed_parameter_collision_SRB_mass_of_union": "0",
        "all_atoms_strictly_contained_in_their_occurrence_matched_full_germs": False,
        "only_original_two_occurrences_four_sides_attach_to_existing_ledgers": True,
        "all_128_ledgers_receive_one_typed_charged_subatom": False,
        "charged_subatoms_exhaust_their_full_germ_ledgers": False,
        "entrance_atom_rows_sha256": canonical_digest(atoms),
    }
    return atoms, summary


def local_return_candidate_atoms(
    entrance_atoms: list[dict[str, Any]],
    loaded: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    local_manifest = loaded[
        "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json"
    ]
    registry = local_manifest["result"]["local_core_return_tail_registry"]
    outcomes = registry["branch_key_to_return_outcome"]
    entrance_by_key = {
        f"{row['occurrence_id']}|{row['parameter_side']}": row
        for row in entrance_atoms
    }
    maximal_rows, _registry = stopping.current.load_maximal_rows()
    source_z = {row["occurrence_id"]: Q(row["witness"]["z"]) for row in maximal_rows}
    radius = local_return.materialized.RADIUS
    magnitude_center = local_return.materialized.frozen_dwell.POINT_PARAMETER_MAGNITUDE
    assert radius == Q(1, 2**8000)
    assert magnitude_center == Q(1, 2**300)

    atoms: list[dict[str, Any]] = []
    for branch_key, outcome in sorted(outcomes.items()):
        occurrence_id, side = branch_key.split("|")
        entrance = entrance_by_key[branch_key]
        specification = local_return.charge.SELECTED[occurrence_id]
        z_center = source_z[occurrence_id] + Q(specification["z_shift"])
        entrance_power = entrance["source_coordinates"]["z_half_width"][
            "denominator_power_of_two"
        ]
        entrance_radius = Q(1, 2**entrance_power)
        assert abs(z_center - Q(entrance["source_coordinates"]["z_center"])) + radius < entrance_radius
        assert magnitude_center + radius < entrance_radius
        finite = isinstance(outcome["first_return_time"], int)
        payload = {
            "branch_key": branch_key,
            "initial_core_id": entrance["destination_core_id"],
            "first_return_time": outcome["first_return_time"],
            "first_return_core_id": outcome["first_return_core_id"],
        }
        atoms.append({
            "local_candidate_atom_id": "local-induced-atom:" + canonical_digest(payload),
            "branch_key": branch_key,
            "occurrence_id": occurrence_id,
            "parameter_side": side,
            "contained_in_entrance_atom_id": entrance["entrance_atom_id"],
            "source_core_id": entrance["destination_core_id"],
            "source_coordinates": {
                "coordinates": ["z", "h"],
                "z_center": str(z_center),
                "parameter_magnitude_center": str(magnitude_center),
                "common_half_width": dyadic(8000),
            },
            "parameterized_box_dimension": 2,
            "fixed_parameter_collision_source_dimension": 1,
            "full_collision_core_source_dimension": 2,
            "box_is_full_collision_core_rectangle": False,
            "single_labelled_dz_dh_area": dyadic(15998),
            "fixed_parameter_collision_SRB_mass": "0",
            "candidate_operator_term": "R_n" if finite else "Q_2018",
            "first_return_time_or_censoring": outcome["first_return_time"],
            "first_return_core_id": outcome["first_return_core_id"],
            "all_core_reentry_times_through_2018": outcome[
                "all_core_reentry_times_through_2018"
            ],
            "first_event_guard_through_reported_time": True,
            "all_2018_collisions_unique_regular_and_core_classified": True,
            "survivor_is_not_declared_nonreturning_cemetery": not finite,
        })

    assert len(atoms) == 4
    assert len({row["local_candidate_atom_id"] for row in atoms}) == 4
    assert len({row["source_core_id"] for row in atoms}) == 2
    assert sum(row["candidate_operator_term"] == "R_n" for row in atoms) == 3
    assert sum(row["candidate_operator_term"] == "Q_2018" for row in atoms) == 1
    assert sum(row["fixed_parameter_collision_SRB_mass"] == "0" for row in atoms) == 4
    assert registry["total_labelled_coordinate_volume"] == "2^-15996"
    summary = {
        "local_candidate_atom_count": 4,
        "distinct_source_core_count": 2,
        "untouched_source_core_count": 22,
        "finite_R_n_candidate_atom_count": 3,
        "censored_Q_2018_candidate_atom_count": 1,
        "finite_return_times": [545, 649, 1531],
        "parameterized_labelled_dz_dh_volume": "2^-15996",
        "fixed_parameter_collision_SRB_mass": "0",
        "full_C24_source_coverage": False,
        "local_candidate_atom_rows_sha256": canonical_digest(atoms),
    }
    return atoms, summary


def physical_partition_obstruction() -> dict[str, Any]:
    return {
        "frozen_physical_source_carrier": "C24_subset_of_two_dimensional_collision_section",
        "frozen_core_count": 24,
        "frozen_C24_collision_SRB_normalized_mass_strict_lower": "147/550000",
        "available_fixed_parameter_source_object": "finite_union_of_regular_analytic_curves",
        "available_fixed_parameter_source_dimension": 1,
        "required_physical_source_dimension": 2,
        "finite_union_of_regular_analytic_curves_has_two_dimensional_area_zero": True,
        "available_atom_union_collision_SRB_mass": "0",
        "uncovered_C24_collision_SRB_mass_strict_lower": "147/550000",
        "positive_labelled_dz_dh_area_is_not_collision_SRB_mass": True,
        "current_atoms_can_cover_a_positive_SRB_mass_core_rectangle": False,
        "current_atoms_form_a_physical_source_core_partition": False,
        "occurrence_id_alone_is_a_valid_germ_domain_join_key": False,
        "charged_atoms_outside_occurrence_matched_registered_germs": 124,
        "obstruction_scope": "current_frozen_materialization_only",
        "future_full_dimensional_partition_is_mathematically_refuted": False,
    }


def required_raw_partition_interface() -> dict[str, Any]:
    required_fields = [
        "raw_atom_id",
        "full_two_dimensional_source_core_domain",
        "complete_collision_word",
        "unique_first_collision_owner_margin_at_every_step",
        "strict_preterminal_C24_separation_margin_at_every_step",
        "first_return_time_and_destination_core",
        "singular_or_unresolved_outer_cover",
        "collision_SRB_atom_mass_m_i",
        "return_map_Jacobian_and_distortion",
        "strong_source_envelope_q_i",
        "survivor_parent_id_and_first_failure_guard",
        "common_fw_rev_restriction_id",
    ]
    missing = [
        "full_two_dimensional_source_core_domain",
        "unique_first_collision_owner_margin_at_every_step",
        "strict_preterminal_C24_separation_margin_at_every_step",
        "singular_or_unresolved_outer_cover",
        "collision_SRB_atom_mass_m_i",
        "return_map_Jacobian_and_distortion",
        "strong_source_envelope_q_i",
        "survivor_parent_id_and_first_failure_guard",
        "common_fw_rev_restriction_id",
    ]
    return {
        "target_operator_atoms": {
            "R_n": "M_C L (M_Cc L)^(n-1) M_C",
            "Q_n": "(M_Cc L)^n M_C",
        },
        "required_raw_atom_fields": required_fields,
        "fields_missing_from_current_materialization": missing,
        "required_global_conservation_identity": (
            "mu_C=sum_n>=1 sum_Rn_atoms m_i + singular_cemetery_mass + survivor_mass"
        ),
        "required_weighted_tail": "sum_{tau>n} q_tau <= C rho^n",
        "current_physical_mass_terms_available": 0,
        "current_strong_q_terms_available": 0,
        "mass_conservation_identity_evaluable": False,
        "weighted_tail_evaluable": False,
        "induced_strong_Lasota_Yorke_coefficient_evaluable": False,
    }


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    entrance_atoms, entrance_summary = charged_entrance_atoms()
    local_atoms, local_summary = local_return_candidate_atoms(
        entrance_atoms, loaded
    )
    result: dict[str, Any] = {
        "schema": "cm2.gate34.physical-first-return-partition-interface.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "join_policy": "exact_occurrence_parameter_side_and_canonical_ids",
            "dimension_policy": "fixed_parameter_physical_collision_carrier",
        },
        "charged_entrance_interface": entrance_summary,
        "charged_entrance_atom_rows": entrance_atoms,
        "local_return_candidate_interface": local_summary,
        "local_return_candidate_atom_rows": local_atoms,
        "physical_partition_obstruction": physical_partition_obstruction(),
        "required_raw_partition_interface": required_raw_partition_interface(),
        "strict_nonpromotion": {
            "suffix_relative_entrance_is_source_relative_first_entrance": False,
            "occurrence_id_only_join_identifies_equal_germ_domains": False,
            "charged_atoms_exhaust_full_germ_domains": False,
            "labelled_dz_dh_area_is_collision_SRB_mass": False,
            "four_local_boxes_partition_C24": False,
            "three_local_returns_construct_induced_operator": False,
            "censored_box_is_nonreturning_cemetery": False,
            "physical_source_core_first_return_partition": "NOT_CERTIFIED",
            "collision_SRB_mass_conservation": "NOT_CERTIFIED",
            "quantitative_excursion_cemetery_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
            "common_two_view_induced_operator": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("CHARGED_ENTRANCE_RAW_ATOMS_128: CERTIFIED")
    print("TYPED_EXISTING_GERM_LEDGER_SLOT_ATTACHMENTS_4: CERTIFIED")
    print("OCCURRENCE_ONLY_LEDGER_DOMAIN_MISMATCHES_124: CERTIFIED_REJECTED")
    print("LOCAL_RN_CANDIDATE_ATOMS_3_AND_Q2018_CANDIDATE_1: CERTIFIED_TYPED")
    print("CURRENT_ATOMS_FIXED_PARAMETER_COLLISION_SRB_MASS_ZERO: CERTIFIED")
    print("PHYSICAL_SOURCE_CORE_FIRST_RETURN_PARTITION: NOT_CERTIFIED")
    print("COLLISION_SRB_MASS_CONSERVATION: NOT_CERTIFIED")
    print("QUANTITATIVE_EXCURSION_CEMETERY_TAIL: NOT_CERTIFIED")
    print("INDUCED_STRONG_OPERATOR: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
