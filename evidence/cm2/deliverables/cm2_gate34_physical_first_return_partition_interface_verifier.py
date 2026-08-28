#!/usr/bin/env python3
"""Fail-closed verifier for the physical first-return partition interface."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import cm2_gate34_physical_first_return_partition_interface_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.physical-first-return-partition-interface.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.physical-first-return-partition-interface.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-physical-first-return-partition-interface-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_physical_first_return_partition_interface_cert.py"

TOTAL_LABELLED_AREA = (
    "31082702275618732522970516901998989768203685434594281004917322418204724867259386822657/"
    "354901720847464302026037015570314714039863945648104521621821386318671527399120079749116723981329865996466075003059657194108692201472"
)
ENTRANCE_ROWS_SHA256 = "3da358b5ed64d9616ac51597cfaaa5c721daf68d2f67b9c112557665ea163ec5"
LOCAL_ROWS_SHA256 = "7c274689bd2e1f5b8dca238ba2e32c5edd0565038b33c78d295c374a56da03c2"
ATTACHED_OCCURRENCES = {
    "occ:c5fde0378e6e76eec93a0ceb",
    "occ:f2b4833eb8dccd403eec3485",
}


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def strict_load(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"non-finite constant {value}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def expected_entrance_summary() -> dict[str, Any]:
    return {
        "charged_entrance_atom_count": 128,
        "occurrence_matched_existing_germ_candidate_count": 128,
        "typed_existing_germ_ledger_attachment_count": 4,
        "occurrence_only_ledger_join_rejection_count": 124,
        "unique_typed_existing_first_core_slot_count": 4,
        "typed_slots_inside_materialized_horizon_8_prefix": 0,
        "typed_slots_after_materialized_horizon_8_prefix": 4,
        "distinct_destination_core_count": 14,
        "radius_power_histogram_by_oriented_atom": {
            "80": 64,
            "100": 16,
            "120": 32,
            "180": 4,
            "200": 8,
            "220": 4,
        },
        "total_positive_labelled_dz_dh_area": TOTAL_LABELLED_AREA,
        "total_positive_labelled_dz_dh_area_strict_lower_bound": "2^-153",
        "total_positive_labelled_dz_dh_area_strict_upper_bound": "2^-152",
        "total_ambient_dz_ds_dh_volume": "0",
        "fixed_parameter_collision_SRB_mass_of_union": "0",
        "all_atoms_strictly_contained_in_their_occurrence_matched_full_germs": False,
        "only_original_two_occurrences_four_sides_attach_to_existing_ledgers": True,
        "all_128_ledgers_receive_one_typed_charged_subatom": False,
        "charged_subatoms_exhaust_their_full_germ_ledgers": False,
        "entrance_atom_rows_sha256": ENTRANCE_ROWS_SHA256,
    }


def expected_local_summary() -> dict[str, Any]:
    return {
        "local_candidate_atom_count": 4,
        "distinct_source_core_count": 2,
        "untouched_source_core_count": 22,
        "finite_R_n_candidate_atom_count": 3,
        "censored_Q_2018_candidate_atom_count": 1,
        "finite_return_times": [545, 649, 1531],
        "parameterized_labelled_dz_dh_volume": "2^-15996",
        "fixed_parameter_collision_SRB_mass": "0",
        "full_C24_source_coverage": False,
        "local_candidate_atom_rows_sha256": LOCAL_ROWS_SHA256,
    }


def expected_obstruction() -> dict[str, Any]:
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


def expected_scope() -> dict[str, Any]:
    return {
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
    }


def expected_verdict() -> dict[str, Any]:
    return {
        "charged_entrance_raw_atoms_128": "CERTIFIED",
        "typed_existing_germ_ledger_slot_attachments_4": "CERTIFIED",
        "occurrence_only_ledger_domain_mismatches_124": "CERTIFIED_REJECTED",
        "local_Rn_candidate_atoms_3": "CERTIFIED_TYPED",
        "local_Q2018_candidate_atoms_1": "CERTIFIED_TYPED",
        "current_atoms_fixed_parameter_collision_SRB_mass_zero": "CERTIFIED",
        "physical_source_core_first_return_partition": "NOT_CERTIFIED",
        "collision_SRB_mass_conservation": "NOT_CERTIFIED",
        "quantitative_excursion_cemetery_tail": "NOT_CERTIFIED",
        "induced_strong_operator": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }


ENTRANCE_KEYS = {
    "entrance_atom_id",
    "occurrence_id",
    "parameter_side",
    "parameter_sign",
    "source_chart",
    "occurrence_matched_selected_germ_id",
    "occurrence_matched_stopping_ledger_id",
    "source_owner_audit_id",
    "upstream_first_stopping_branch_id",
    "source_coordinates",
    "z_interval_strictly_contained_in_occurrence_matched_germ",
    "s_equals_zero_contained_in_occurrence_matched_germ",
    "h_interval_strictly_contained_in_occurrence_matched_germ",
    "typed_existing_germ_ledger_attachment_admitted",
    "occurrence_id_only_ledger_join_rejected",
    "parameterized_ambient_dimension",
    "parameterized_charged_atom_dimension",
    "fixed_parameter_collision_source_dimension",
    "labelled_dz_dh_area",
    "ambient_dz_ds_dh_Lebesgue_volume",
    "suffix_relative_first_core_time",
    "source_collision_count_to_regular_suffix",
    "destination_core_id",
    "candidate_countable_first_core_slot_id",
    "typed_existing_ledger_first_core_slot_id",
    "typed_slot_is_in_materialized_horizon_8_prefix",
    "every_suffix_preterminal_state_strictly_outside_C24",
    "terminal_state_strictly_inside_unique_core",
    "complete_itinerary_sha256",
    "classification_records_sha256",
    "source_relative_first_event_guard",
    "collision_SRB_mass",
}

LOCAL_KEYS = {
    "local_candidate_atom_id",
    "branch_key",
    "occurrence_id",
    "parameter_side",
    "contained_in_entrance_atom_id",
    "source_core_id",
    "source_coordinates",
    "parameterized_box_dimension",
    "fixed_parameter_collision_source_dimension",
    "full_collision_core_source_dimension",
    "box_is_full_collision_core_rectangle",
    "single_labelled_dz_dh_area",
    "fixed_parameter_collision_SRB_mass",
    "candidate_operator_term",
    "first_return_time_or_censoring",
    "first_return_core_id",
    "all_core_reentry_times_through_2018",
    "first_event_guard_through_reported_time",
    "all_2018_collisions_unique_regular_and_core_classified",
    "survivor_is_not_declared_nonreturning_cemetery",
}


def check_entrance_rows(rows: Any) -> list[str]:
    if not isinstance(rows, list) or len(rows) != 128:
        return ["entrance row count"]
    errors: list[str] = []
    if digest(rows) != ENTRANCE_ROWS_SHA256:
        errors.append("entrance row digest")
    if any(not isinstance(row, dict) or set(row) != ENTRANCE_KEYS for row in rows):
        errors.append("entrance row keys")
        return errors
    keys = [(row["occurrence_id"], row["parameter_side"]) for row in rows]
    if len(set(keys)) != 128 or len({key[0] for key in keys}) != 64:
        errors.append("entrance branch key set")
    if Counter(row["parameter_side"] for row in rows) != Counter({"hit": 64, "miss": 64}):
        errors.append("entrance side histogram")
    attached = [row for row in rows if row["typed_existing_germ_ledger_attachment_admitted"] is True]
    rejected = [row for row in rows if row["occurrence_id_only_ledger_join_rejected"] is True]
    if len(attached) != 4 or len(rejected) != 124:
        errors.append("typed domain admission count")
    if {row["occurrence_id"] for row in attached} != ATTACHED_OCCURRENCES:
        errors.append("typed domain admission owners")
    for row in rows:
        admitted = row["typed_existing_germ_ledger_attachment_admitted"]
        rejected_join = row["occurrence_id_only_ledger_join_rejected"]
        if type(admitted) is not bool or type(rejected_join) is not bool:
            errors.append("typed domain admission boolean")
            break
        if admitted == rejected_join:
            errors.append("typed domain admission complement")
            break
        if admitted != row["z_interval_strictly_contained_in_occurrence_matched_germ"]:
            errors.append("z containment admission")
            break
        if row["s_equals_zero_contained_in_occurrence_matched_germ"] is not True:
            errors.append("s containment")
            break
        if row["h_interval_strictly_contained_in_occurrence_matched_germ"] is not True:
            errors.append("h containment")
            break
        if (row["typed_existing_ledger_first_core_slot_id"] is not None) != admitted:
            errors.append("typed slot nullability")
            break
        if (row["typed_slot_is_in_materialized_horizon_8_prefix"] is not None) != admitted:
            errors.append("prefix typing nullability")
            break
        if admitted and row["typed_slot_is_in_materialized_horizon_8_prefix"] is not False:
            errors.append("typed prefix membership")
            break
        if [row["parameterized_ambient_dimension"], row["parameterized_charged_atom_dimension"], row["fixed_parameter_collision_source_dimension"]] != [3, 2, 1]:
            errors.append("entrance dimensions")
            break
        if row["ambient_dz_ds_dh_Lebesgue_volume"] != "0" or row["collision_SRB_mass"] != "0_AT_EACH_FIXED_PARAMETER":
            errors.append("entrance zero mass")
            break
        if row["source_relative_first_event_guard"] != "NOT_CERTIFIED_IN_THIS_LEAF":
            errors.append("source-relative scope")
            break
        if row["parameter_side"] == "hit" and row["source_collision_count_to_regular_suffix"] != 2:
            errors.append("hit collision offset")
            break
        if row["parameter_side"] == "miss" and row["source_collision_count_to_regular_suffix"] != 1:
            errors.append("miss collision offset")
            break
    time_histogram = Counter(row["suffix_relative_first_core_time"] for row in rows)
    if time_histogram != Counter({2: 44, 3: 20, 4: 16, 7: 16, 8: 8, 9: 8, 16: 4, 19: 8, 20: 4}):
        errors.append("entrance time histogram")
    if len({row["destination_core_id"] for row in rows}) != 14:
        errors.append("entrance destinations")
    return errors


def check_local_rows(rows: Any, entrance_rows: Any) -> list[str]:
    if not isinstance(rows, list) or len(rows) != 4:
        return ["local row count"]
    errors: list[str] = []
    if digest(rows) != LOCAL_ROWS_SHA256:
        errors.append("local row digest")
    if any(not isinstance(row, dict) or set(row) != LOCAL_KEYS for row in rows):
        errors.append("local row keys")
        return errors
    entrance_ids = {
        row["entrance_atom_id"] for row in entrance_rows
        if isinstance(row, dict) and "entrance_atom_id" in row
    }
    if any(row["contained_in_entrance_atom_id"] not in entrance_ids for row in rows):
        errors.append("local entrance binding")
    if len({row["branch_key"] for row in rows}) != 4:
        errors.append("local branch keys")
    if len({row["source_core_id"] for row in rows}) != 2:
        errors.append("local source cores")
    if Counter(row["candidate_operator_term"] for row in rows) != Counter({"R_n": 3, "Q_2018": 1}):
        errors.append("local operator term histogram")
    times = sorted(
        row["first_return_time_or_censoring"]
        for row in rows if isinstance(row["first_return_time_or_censoring"], int)
    )
    if times != [545, 649, 1531]:
        errors.append("local return times")
    survivor = [row for row in rows if row["candidate_operator_term"] == "Q_2018"]
    if len(survivor) != 1 or survivor[0]["first_return_time_or_censoring"] != ">2018" or survivor[0]["survivor_is_not_declared_nonreturning_cemetery"] is not True:
        errors.append("local survivor typing")
    for row in rows:
        if [row["parameterized_box_dimension"], row["fixed_parameter_collision_source_dimension"], row["full_collision_core_source_dimension"]] != [2, 1, 2]:
            errors.append("local dimensions")
            break
        if row["box_is_full_collision_core_rectangle"] is not False:
            errors.append("local rectangle scope")
            break
        if row["fixed_parameter_collision_SRB_mass"] != "0":
            errors.append("local zero mass")
            break
        if row["first_event_guard_through_reported_time"] is not True or row["all_2018_collisions_unique_regular_and_core_classified"] is not True:
            errors.append("local first event replay")
            break
    return errors


def check(manifest: Any) -> list[str]:
    if not isinstance(manifest, dict):
        return ["manifest type"]
    errors: list[str] = []
    if set(manifest) != {"schema", "certificate_sha256", "verifier_sha256", "dependencies", "result", "verdict"}:
        errors.append("manifest keys")
    if manifest.get("schema") != SCHEMA:
        errors.append("manifest schema")
    if manifest.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash")
    if not strict_equal(manifest.get("dependencies"), certificate.DEPENDENCIES):
        errors.append("dependency table")
    result = manifest.get("result")
    if not isinstance(result, dict):
        return errors + ["result type"]
    expected_result_keys = {
        "schema",
        "provenance",
        "charged_entrance_interface",
        "charged_entrance_atom_rows",
        "local_return_candidate_interface",
        "local_return_candidate_atom_rows",
        "physical_partition_obstruction",
        "required_raw_partition_interface",
        "strict_nonpromotion",
        "internal_replay_digest",
    }
    if set(result) != expected_result_keys:
        errors.append("result keys")
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")
    expected_provenance = {
        "dependency_sha256": certificate.DEPENDENCIES,
        "old_artifacts_modified": False,
        "join_policy": "exact_occurrence_parameter_side_and_canonical_ids",
        "dimension_policy": "fixed_parameter_physical_collision_carrier",
    }
    if not strict_equal(result.get("provenance"), expected_provenance):
        errors.append("provenance")
    if not strict_equal(result.get("charged_entrance_interface"), expected_entrance_summary()):
        errors.append("entrance summary")
    entrance_rows = result.get("charged_entrance_atom_rows")
    errors.extend(check_entrance_rows(entrance_rows))
    if not strict_equal(result.get("local_return_candidate_interface"), expected_local_summary()):
        errors.append("local summary")
    errors.extend(check_local_rows(result.get("local_return_candidate_atom_rows"), entrance_rows if isinstance(entrance_rows, list) else []))
    if not strict_equal(result.get("physical_partition_obstruction"), expected_obstruction()):
        errors.append("physical obstruction")
    if not strict_equal(result.get("required_raw_partition_interface"), certificate.required_raw_partition_interface()):
        errors.append("required raw interface")
    if not strict_equal(result.get("strict_nonpromotion"), expected_scope()):
        errors.append("strict nonpromotion")
    if not strict_equal(manifest.get("verdict"), expected_verdict()):
        errors.append("verdict")
    return errors


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(manifest["result"])


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[Any, ...], value: Any) -> None:
        candidate = copy.deepcopy(manifest)
        target: Any = candidate
        for part in path[:-1]:
            target = target[part]
        target[path[-1]] = value
        if path[0] == "result":
            refresh(candidate)
        mutations.append(candidate)

    entrance = ("result", "charged_entrance_interface")
    mutate(entrance + ("charged_entrance_atom_count",), 127)
    mutate(entrance + ("typed_existing_germ_ledger_attachment_count",), 128)
    mutate(entrance + ("occurrence_only_ledger_join_rejection_count",), 0)
    mutate(entrance + ("unique_typed_existing_first_core_slot_count",), 128)
    mutate(entrance + ("typed_slots_inside_materialized_horizon_8_prefix",), 104)
    mutate(entrance + ("distinct_destination_core_count",), 24)
    mutate(entrance + ("total_positive_labelled_dz_dh_area",), "1")
    mutate(entrance + ("total_ambient_dz_ds_dh_volume",), TOTAL_LABELLED_AREA)
    mutate(entrance + ("fixed_parameter_collision_SRB_mass_of_union",), TOTAL_LABELLED_AREA)
    mutate(entrance + ("all_atoms_strictly_contained_in_their_occurrence_matched_full_germs",), True)
    mutate(entrance + ("all_128_ledgers_receive_one_typed_charged_subatom",), True)
    mutate(entrance + ("entrance_atom_rows_sha256",), "0" * 64)

    row = ("result", "charged_entrance_atom_rows", 0)
    mutate(row + ("occurrence_id_only_ledger_join_rejected",), False)
    mutate(row + ("typed_existing_germ_ledger_attachment_admitted",), True)
    mutate(row + ("z_interval_strictly_contained_in_occurrence_matched_germ",), True)
    mutate(row + ("typed_existing_ledger_first_core_slot_id",), "core-hit:" + "0" * 64)
    mutate(row + ("typed_slot_is_in_materialized_horizon_8_prefix",), True)
    mutate(row + ("parameterized_charged_atom_dimension",), 3)
    mutate(row + ("fixed_parameter_collision_source_dimension",), 2)
    mutate(row + ("ambient_dz_ds_dh_Lebesgue_volume",), "1")
    mutate(row + ("collision_SRB_mass",), "POSITIVE")
    mutate(row + ("source_relative_first_event_guard",), "CERTIFIED")
    mutate(row + ("suffix_relative_first_core_time",), 1)
    mutate(row + ("destination_core_id",), "core:" + "0" * 64)
    mutate(row + ("classification_records_sha256",), "0" * 64)

    local = ("result", "local_return_candidate_interface")
    mutate(local + ("local_candidate_atom_count",), 24)
    mutate(local + ("distinct_source_core_count",), 24)
    mutate(local + ("untouched_source_core_count",), 0)
    mutate(local + ("finite_R_n_candidate_atom_count",), 4)
    mutate(local + ("censored_Q_2018_candidate_atom_count",), 0)
    mutate(local + ("fixed_parameter_collision_SRB_mass",), "2^-15996")
    mutate(local + ("full_C24_source_coverage",), True)
    mutate(local + ("local_candidate_atom_rows_sha256",), "0" * 64)

    local_row = ("result", "local_return_candidate_atom_rows", 0)
    mutate(local_row + ("candidate_operator_term",), "Q_2018")
    mutate(local_row + ("first_return_time_or_censoring",), 546)
    mutate(local_row + ("fixed_parameter_collision_source_dimension",), 2)
    mutate(local_row + ("box_is_full_collision_core_rectangle",), True)
    mutate(local_row + ("fixed_parameter_collision_SRB_mass",), "1")
    mutate(local_row + ("first_event_guard_through_reported_time",), False)

    obstruction = ("result", "physical_partition_obstruction")
    mutate(obstruction + ("charged_atoms_outside_occurrence_matched_registered_germs",), 0)
    mutate(obstruction + ("occurrence_id_alone_is_a_valid_germ_domain_join_key",), True)
    mutate(obstruction + ("available_fixed_parameter_source_dimension",), 2)
    mutate(obstruction + ("finite_union_of_regular_analytic_curves_has_two_dimensional_area_zero",), False)
    mutate(obstruction + ("available_atom_union_collision_SRB_mass",), "147/550000")
    mutate(obstruction + ("current_atoms_form_a_physical_source_core_partition",), True)
    mutate(obstruction + ("future_full_dimensional_partition_is_mathematically_refuted",), True)

    raw = ("result", "required_raw_partition_interface")
    mutate(raw + ("current_physical_mass_terms_available",), 4)
    mutate(raw + ("current_strong_q_terms_available",), 4)
    mutate(raw + ("mass_conservation_identity_evaluable",), True)
    mutate(raw + ("weighted_tail_evaluable",), True)
    mutate(raw + ("induced_strong_Lasota_Yorke_coefficient_evaluable",), True)

    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("occurrence_id_only_join_identifies_equal_germ_domains",), True)
    mutate(scope + ("labelled_dz_dh_area_is_collision_SRB_mass",), True)
    mutate(scope + ("four_local_boxes_partition_C24",), True)
    mutate(scope + ("physical_source_core_first_return_partition",), "CERTIFIED")
    mutate(scope + ("collision_SRB_mass_conservation",), "CERTIFIED")
    mutate(scope + ("quantitative_excursion_cemetery_tail",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "physical_source_core_first_return_partition"), "CERTIFIED")
    mutate(("verdict", "Gate4"), "CERTIFIED")
    mutate(entrance + ("typed_existing_germ_ledger_attachment_count",), True)

    rejected = sum(bool(check(candidate)) for candidate in mutations)

    parser_tests = [
        '{"x":1,"x":2}',
        '{"x":NaN}',
        '{"x":Infinity}',
    ]
    for source in parser_tests:
        try:
            json.loads(
                source,
                object_pairs_hook=reject_duplicate_pairs,
                parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
            )
        except (DuplicateKeyError, ValueError):
            rejected += 1
        mutations.append({})
    return rejected, len(mutations)


def main() -> int:
    if sys.flags.optimize != 0:
        print("ERROR: optimized Python is not admitted", file=sys.stderr)
        return 1
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = strict_load(args.manifest)
    except Exception as error:
        print(f"MANIFEST_READ_ERROR: {error}", file=sys.stderr)
        return 1
    errors = check(manifest)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.replay:
        replay = certificate.build_result()
        if not strict_equal(replay, manifest["result"]):
            print("ERROR: replay mismatch", file=sys.stderr)
            return 1
    if args.self_test:
        rejected, total = self_test(manifest)
        status = "PASS" if rejected == total else "FAIL"
        print(f"SELF_TEST: {status} ({rejected}/{total} mutations rejected)")
        return 0 if rejected == total else 1
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
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
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
