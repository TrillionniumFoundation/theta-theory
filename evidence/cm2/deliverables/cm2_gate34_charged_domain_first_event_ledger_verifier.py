#!/usr/bin/env python3
"""Fail-closed verifier for charged-domain first-event ledgers."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import cm2_gate34_charged_domain_first_event_ledger_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.charged-domain-first-event-ledger.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.charged-domain-first-event-ledger.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-charged-domain-first-event-ledger-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_charged_domain_first_event_ledger_cert.py"

ROWS_SHA256 = "cb147ec5c19f87b73d58012b7b32911c292197103cfcccafc65bc5e87a86bc94"
ALL_SLOTS_SHA256 = "16ab08934fc72f9bb9b0f8821d4f2de9daec418489150cf68de9e092b4557602"
EMPTY_SLOTS_SHA256 = "69fe0459dab9484a6878f602a6d77e305e59000e0a97fdf56e84afacc599ba35"
TIME_HISTOGRAM = {
    "3": 22, "4": 32, "5": 18, "6": 8, "8": 8, "9": 12,
    "10": 8, "11": 4, "17": 2, "18": 2, "20": 4, "21": 6,
    "22": 2,
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
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
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


def expected_registry() -> dict[str, Any]:
    return {
        "exact_charged_borel_domain_count": 128,
        "domain_specific_first_event_ledger_count": 128,
        "domain_equal_unique_nonempty_first_event_slot_count": 128,
        "old_selected_germ_ledger_reuse_count": 0,
        "prior_occurrence_only_domain_mismatch_count": 124,
        "domain_specific_registration_resolves_prior_mismatch_count": 124,
        "source_relative_first_core_time_histogram": TIME_HISTOGRAM,
        "maximum_source_relative_first_core_time": 22,
        "strict_preterminal_outside_regular_state_count": 948,
        "finite_prefix_total_first_event_slot_count": 26900,
        "finite_prefix_unique_nonempty_core_slot_count": 128,
        "finite_prefix_empty_core_slot_count": 25696,
        "finite_prefix_empty_singular_slot_count": 1076,
        "finite_prefix_total_empty_slot_count": 26772,
        "post_stop_slot_count": 0,
        "nonreturning_cemetery_slot_count": 0,
        "all_domains_equal_their_certified_charged_cylinders": True,
        "all_128_first_event_slots_equal_their_whole_domains": True,
        "all_preterminal_core_and_singular_slots_empty": True,
        "all_terminal_wrong_core_and_singular_slots_empty": True,
        "charged_domain_ledger_rows_sha256": ROWS_SHA256,
        "all_finite_prefix_slot_ids_sha256": ALL_SLOTS_SHA256,
        "all_finite_prefix_empty_slot_ids_sha256": EMPTY_SLOTS_SHA256,
    }


def expected_finite_scope() -> dict[str, Any]:
    return {
        "materialized_times_per_ledger": "0_through_source_relative_first_core_time",
        "preterminal_core_slots": "EMPTY_BY_STRICT_OUTSIDE_C24",
        "finite_word_singular_slots": "EMPTY_BY_UNIQUE_REGULAR_COLLISION_REPLAY",
        "terminal_destination_slot": "WHOLE_EXACT_CHARGED_DOMAIN",
        "terminal_other_23_core_slots": "EMPTY_BY_UNIQUE_CORE_INTERIOR",
        "post_stop_slots": "NOT_MATERIALIZED",
        "nonreturning_cemetery_slot": "NOT_MATERIALIZED",
    }


def expected_scope() -> dict[str, Any]:
    return {
        "domain_specific_ledgers_are_old_selected_germ_ledgers": False,
        "charged_domains_cover_whole_all_scale_germs": False,
        "charged_domains_have_positive_fixed_parameter_collision_SRB_mass": False,
        "finite_prefix_singular_emptiness_is_global_cemetery_tail": False,
        "nonreturning_cemetery_is_materialized": False,
        "post_core_first_return_partition": "NOT_CERTIFIED",
        "collision_SRB_mass_or_normalized_hit_fraction": "NOT_CERTIFIED",
        "quantitative_excursion_cemetery_tail": "NOT_CERTIFIED",
        "induced_core_return_operator": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }


def expected_verdict() -> dict[str, Any]:
    return {
        "exact_charged_Borel_domains_128": "CERTIFIED",
        "domain_specific_first_event_ledgers_128": "CERTIFIED",
        "domain_equal_unique_nonempty_source_first_core_slots_128": "CERTIFIED",
        "prior_occurrence_only_mismatches_resolved_by_new_domain_registration_124": "CERTIFIED",
        "finite_prefix_empty_core_slots_25696": "CERTIFIED",
        "finite_prefix_empty_singular_slots_1076": "CERTIFIED",
        "nonreturning_cemetery_slot": "NOT_MATERIALIZED",
        "collision_SRB_mass": "NOT_CERTIFIED",
        "post_core_return_operator": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }


ROW_KEYS = {
    "charged_domain_ledger_id",
    "charged_borel_domain_id",
    "occurrence_id",
    "parameter_side",
    "canonical_domain",
    "domain_equals_upstream_certified_charged_cylinder",
    "upstream_entrance_atom_id",
    "upstream_source_relative_branch_id",
    "source_owner_audit_id",
    "source_state_classification_id",
    "hit_intermediate_classification_id",
    "clock_origin",
    "source_relative_first_core_time",
    "destination_core_id",
    "unique_nonempty_first_event_slot_id",
    "unique_nonempty_slot_equals_whole_charged_domain",
    "strict_preterminal_outside_regular_state_count",
    "all_preterminal_states_strictly_outside_C24",
    "all_collisions_in_certified_finite_word_unique_and_regular",
    "hit_open_side_intermediate_regular_guard",
    "terminal_strictly_inside_unique_destination_core",
    "finite_prefix_core_empty_slot_count",
    "finite_prefix_singular_empty_slot_count",
    "finite_prefix_empty_slot_count",
    "finite_prefix_total_slot_count",
    "finite_prefix_empty_slot_ids_sha256",
    "old_selected_germ_ledger_reused",
    "occurrence_id_only_domain_join_used",
    "post_stop_slots_materialized",
    "nonreturning_cemetery_slot_materialized",
}

DOMAIN_KEYS = {
    "occurrence_id",
    "parameter_side",
    "source_chart",
    "z_interval_closed",
    "fixed_phase_coordinate",
    "signed_h_interval",
    "parameter_magnitude_interval",
    "parameter_sign",
    "coordinates",
    "parameterized_dimension",
    "fixed_parameter_collision_source_dimension",
    "is_Borel",
    "open_side_source_map_is_Borel",
}


def check_rows(rows: Any) -> list[str]:
    if not isinstance(rows, list) or len(rows) != 128:
        return ["ledger row count"]
    errors: list[str] = []
    if digest(rows) != ROWS_SHA256:
        errors.append("ledger row digest")
    if any(not isinstance(row, dict) or set(row) != ROW_KEYS for row in rows):
        errors.append("ledger row keys")
        return errors
    if any(not isinstance(row["canonical_domain"], dict) or set(row["canonical_domain"]) != DOMAIN_KEYS for row in rows):
        errors.append("canonical domain keys")
        return errors
    keys = [(row["occurrence_id"], row["parameter_side"]) for row in rows]
    if len(set(keys)) != 128 or len({key[0] for key in keys}) != 64:
        errors.append("oriented domain key set")
    if Counter(row["parameter_side"] for row in rows) != Counter({"hit": 64, "miss": 64}):
        errors.append("side histogram")
    for field in (
        "charged_borel_domain_id",
        "charged_domain_ledger_id",
        "unique_nonempty_first_event_slot_id",
    ):
        if len({row[field] for row in rows}) != 128:
            errors.append(f"unique {field}")
    for row in rows:
        domain = row["canonical_domain"]
        time = row["source_relative_first_core_time"]
        if type(time) is not int or not 3 <= time <= 22:
            errors.append("stop time type/range")
            break
        if domain["occurrence_id"] != row["occurrence_id"] or domain["parameter_side"] != row["parameter_side"]:
            errors.append("domain owner binding")
            break
        if domain["fixed_phase_coordinate"] != "s=0" or domain["coordinates"] != ["z", "h"]:
            errors.append("domain coordinates")
            break
        if [domain["parameterized_dimension"], domain["fixed_parameter_collision_source_dimension"]] != [2, 1]:
            errors.append("domain dimensions")
            break
        if domain["is_Borel"] is not True or domain["open_side_source_map_is_Borel"] is not True:
            errors.append("Borel domain")
            break
        if row["domain_equals_upstream_certified_charged_cylinder"] is not True:
            errors.append("domain equality")
            break
        if row["clock_origin"] != "source_collision_state_at_time_0":
            errors.append("clock origin")
            break
        if row["strict_preterminal_outside_regular_state_count"] != time:
            errors.append("preterminal count")
            break
        if row["finite_prefix_core_empty_slot_count"] != time * 24 + 23:
            errors.append("per-ledger core empty count")
            break
        if row["finite_prefix_singular_empty_slot_count"] != time + 1:
            errors.append("per-ledger singular empty count")
            break
        if row["finite_prefix_total_slot_count"] != (time + 1) * 25:
            errors.append("per-ledger total slot count")
            break
        if row["finite_prefix_empty_slot_count"] != (time + 1) * 25 - 1:
            errors.append("per-ledger total empty count")
            break
        if any(row[field] is not True for field in (
            "unique_nonempty_slot_equals_whole_charged_domain",
            "all_preterminal_states_strictly_outside_C24",
            "all_collisions_in_certified_finite_word_unique_and_regular",
            "terminal_strictly_inside_unique_destination_core",
        )):
            errors.append("finite first-event guards")
            break
        if row["parameter_side"] == "hit":
            if row["hit_intermediate_classification_id"] is None or row["hit_open_side_intermediate_regular_guard"] is not True:
                errors.append("hit intermediate guard")
                break
        else:
            if row["hit_intermediate_classification_id"] is not None or row["hit_open_side_intermediate_regular_guard"] is not None:
                errors.append("miss intermediate typing")
                break
        if row["old_selected_germ_ledger_reused"] is not False or row["occurrence_id_only_domain_join_used"] is not False:
            errors.append("old ledger nonreuse")
            break
        if row["post_stop_slots_materialized"] != 0 or row["nonreturning_cemetery_slot_materialized"] is not False:
            errors.append("post-stop scope")
            break
    histogram = Counter(row["source_relative_first_core_time"] for row in rows)
    if {str(key): value for key, value in sorted(histogram.items())} != TIME_HISTOGRAM:
        errors.append("time histogram")
    if sum(row["finite_prefix_core_empty_slot_count"] for row in rows) != 25696:
        errors.append("aggregate core empty count")
    if sum(row["finite_prefix_singular_empty_slot_count"] for row in rows) != 1076:
        errors.append("aggregate singular empty count")
    if sum(row["finite_prefix_total_slot_count"] for row in rows) != 26900:
        errors.append("aggregate total slot count")
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
    if set(result) != {
        "schema", "provenance", "charged_domain_first_event_ledger_registry",
        "charged_domain_first_event_ledger_rows", "finite_prefix_scope",
        "strict_nonpromotion", "internal_replay_digest",
    }:
        errors.append("result keys")
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")
    expected_provenance = {
        "dependency_sha256": certificate.DEPENDENCIES,
        "old_artifacts_modified": False,
        "domain_policy": "exact_charged_cylinder_not_occurrence_matched_old_germ",
        "first_event_clock": "source_collision_state_at_time_0",
        "admission_engine": "python-flint Arb plus canonical Borel IDs",
        "precision_bits": 2048,
    }
    if not strict_equal(result.get("provenance"), expected_provenance):
        errors.append("provenance")
    if not strict_equal(result.get("charged_domain_first_event_ledger_registry"), expected_registry()):
        errors.append("registry")
    errors.extend(check_rows(result.get("charged_domain_first_event_ledger_rows")))
    if not strict_equal(result.get("finite_prefix_scope"), expected_finite_scope()):
        errors.append("finite prefix scope")
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

    registry = ("result", "charged_domain_first_event_ledger_registry")
    mutate(registry + ("exact_charged_borel_domain_count",), 127)
    mutate(registry + ("domain_specific_first_event_ledger_count",), 4)
    mutate(registry + ("domain_equal_unique_nonempty_first_event_slot_count",), 127)
    mutate(registry + ("old_selected_germ_ledger_reuse_count",), 4)
    mutate(registry + ("prior_occurrence_only_domain_mismatch_count",), 0)
    mutate(registry + ("domain_specific_registration_resolves_prior_mismatch_count",), 0)
    mutate(registry + ("maximum_source_relative_first_core_time",), 20)
    mutate(registry + ("strict_preterminal_outside_regular_state_count",), 947)
    mutate(registry + ("finite_prefix_total_first_event_slot_count",), 26899)
    mutate(registry + ("finite_prefix_unique_nonempty_core_slot_count",), 127)
    mutate(registry + ("finite_prefix_empty_core_slot_count",), 25695)
    mutate(registry + ("finite_prefix_empty_singular_slot_count",), 1075)
    mutate(registry + ("finite_prefix_total_empty_slot_count",), 26771)
    mutate(registry + ("post_stop_slot_count",), 128)
    mutate(registry + ("nonreturning_cemetery_slot_count",), 128)
    mutate(registry + ("all_domains_equal_their_certified_charged_cylinders",), False)
    mutate(registry + ("all_128_first_event_slots_equal_their_whole_domains",), False)
    mutate(registry + ("charged_domain_ledger_rows_sha256",), "0" * 64)
    mutate(registry + ("all_finite_prefix_slot_ids_sha256",), "0" * 64)
    mutate(registry + ("all_finite_prefix_empty_slot_ids_sha256",), "0" * 64)

    row = ("result", "charged_domain_first_event_ledger_rows", 0)
    mutate(row + ("charged_borel_domain_id",), "charged-borel-domain:" + "0" * 64)
    mutate(row + ("charged_domain_ledger_id",), "charged-first-event-ledger:" + "0" * 64)
    mutate(row + ("domain_equals_upstream_certified_charged_cylinder",), False)
    mutate(row + ("source_relative_first_core_time",), 2)
    mutate(row + ("destination_core_id",), "core:" + "0" * 64)
    mutate(row + ("unique_nonempty_first_event_slot_id",), "charged-first-event-slot:" + "0" * 64)
    mutate(row + ("unique_nonempty_slot_equals_whole_charged_domain",), False)
    mutate(row + ("strict_preterminal_outside_regular_state_count",), 0)
    mutate(row + ("all_preterminal_states_strictly_outside_C24",), False)
    mutate(row + ("all_collisions_in_certified_finite_word_unique_and_regular",), False)
    mutate(row + ("terminal_strictly_inside_unique_destination_core",), False)
    mutate(row + ("finite_prefix_core_empty_slot_count",), 0)
    mutate(row + ("finite_prefix_singular_empty_slot_count",), 0)
    mutate(row + ("finite_prefix_total_slot_count",), 1)
    mutate(row + ("old_selected_germ_ledger_reused",), True)
    mutate(row + ("occurrence_id_only_domain_join_used",), True)
    mutate(row + ("post_stop_slots_materialized",), 1)
    mutate(row + ("nonreturning_cemetery_slot_materialized",), True)
    mutate(row + ("canonical_domain", "fixed_phase_coordinate"), "s_interval")
    mutate(row + ("canonical_domain", "parameterized_dimension"), 3)
    mutate(row + ("canonical_domain", "is_Borel"), False)
    mutate(row + ("canonical_domain", "open_side_source_map_is_Borel"), False)

    finite = ("result", "finite_prefix_scope")
    mutate(finite + ("post_stop_slots",), "MATERIALIZED")
    mutate(finite + ("nonreturning_cemetery_slot",), "EMPTY")
    mutate(finite + ("terminal_destination_slot",), "POINT_SUBSET")

    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("domain_specific_ledgers_are_old_selected_germ_ledgers",), True)
    mutate(scope + ("charged_domains_cover_whole_all_scale_germs",), True)
    mutate(scope + ("charged_domains_have_positive_fixed_parameter_collision_SRB_mass",), True)
    mutate(scope + ("finite_prefix_singular_emptiness_is_global_cemetery_tail",), True)
    mutate(scope + ("nonreturning_cemetery_is_materialized",), True)
    mutate(scope + ("post_core_first_return_partition",), "CERTIFIED")
    mutate(scope + ("collision_SRB_mass_or_normalized_hit_fraction",), "CERTIFIED")
    mutate(scope + ("quantitative_excursion_cemetery_tail",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "collision_SRB_mass"), "CERTIFIED")
    mutate(("verdict", "Gate4"), "CERTIFIED")
    mutate(registry + ("exact_charged_borel_domain_count",), True)

    rejected = sum(bool(check(candidate)) for candidate in mutations)
    parser_sources = ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}']
    for source in parser_sources:
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
    if args.replay and not strict_equal(certificate.build_result(), manifest["result"]):
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
    print("EXACT_CHARGED_BOREL_DOMAINS_128: CERTIFIED")
    print("DOMAIN_SPECIFIC_FIRST_EVENT_LEDGERS_128: CERTIFIED")
    print("DOMAIN_EQUAL_UNIQUE_NONEMPTY_SOURCE_FIRST_CORE_SLOTS_128: CERTIFIED")
    print("PRIOR_OCCURRENCE_ONLY_MISMATCHES_RESOLVED_BY_NEW_DOMAIN_REGISTRATION_124: CERTIFIED")
    print("FINITE_PREFIX_EMPTY_CORE_SLOTS_25696: CERTIFIED")
    print("FINITE_PREFIX_EMPTY_SINGULAR_SLOTS_1076: CERTIFIED")
    print("NONRETURNING_CEMETERY_SLOT: NOT_MATERIALIZED")
    print("COLLISION_SRB_MASS: NOT_CERTIFIED")
    print("POST_CORE_RETURN_OPERATOR: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
