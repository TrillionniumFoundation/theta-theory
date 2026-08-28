#!/usr/bin/env python3
"""Fail-closed verifier for the selected-germ core/cemetery ledger."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import cm2_gate34_selected_germ_core_cemetery_ledger_cert as certificate


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate34.selected-germ-core-cemetery-ledger.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.selected-germ-core-cemetery-ledger.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-selected-germ-core-cemetery-ledger-manifest-2026-07-17.json"
)
CERTIFICATE = HERE / "cm2_gate34_selected_germ_core_cemetery_ledger_cert.py"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def check(manifest: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest type"]
    if manifest.get("schema") != SCHEMA:
        errors.append("manifest schema")
    if manifest.get("certificate_sha256") != sha256_path(CERTIFICATE):
        errors.append("certificate hash")
    if manifest.get("verifier_sha256") != sha256_path(Path(__file__)):
        errors.append("verifier hash")
    if manifest.get("dependencies") != certificate.DEPENDENCIES:
        errors.append("dependency table")

    result = manifest.get("result", {})
    if result.get("schema") != RESULT_SCHEMA:
        errors.append("result schema")
    if result.get("internal_replay_digest") != result_digest(result):
        errors.append("result digest")

    registry = result.get("selected_branch_stopping_registry", {})
    expected_registry = {
        "selected_parameter_germ_count": 64,
        "oriented_branch_ledger_count": 128,
        "finite_destination_core_count": 24,
        "hit_branch_count": 64,
        "miss_branch_count": 64,
    }
    for key, value in expected_registry.items():
        if registry.get(key) != value:
            errors.append(f"registry {key}")
    for key in (
        "branch_ledgers_sha256",
        "destination_cores_sha256",
        "first_branch_ledger_id",
        "last_branch_ledger_id",
    ):
        if not isinstance(registry.get(key), str) or not registry[key]:
            errors.append(f"registry digest {key}")

    theorem = result.get("measurable_core_cemetery_stopping_theorem", {})
    expected_true = (
        "extended_billiard_map_T_hat_is_Borel",
        "T_hat_sends_singular_set_to_absorbing_dagger",
        "frozen_24_core_union_is_finite_compact_Borel_union",
        "finite_time_core_hit_sets_are_Borel",
        "finite_time_singular_cemetery_sets_are_Borel",
        "nonreturning_cemetery_is_countable_intersection_of_Borel_sets",
        "analytic_germ_pullbacks_preserve_Borel_measurability",
        "core_hit_singular_and_nonreturning_classes_are_pairwise_disjoint",
        "core_hit_singular_and_nonreturning_classes_exhaust_each_germ_domain",
        "exact_measure_decomposition_for_every_finite_germ_measure",
    )
    for key in expected_true:
        if theorem.get(key) is not True:
            errors.append(f"theorem {key}")
    if theorem.get("countable_core_hit_cylinder_schema") != (
        "(branch_ledger_id,n,core_id) for n>=0"
    ):
        errors.append("core-hit cylinder schema")

    prefix = result.get("materialized_horizon_8_partition_prefix", {})
    expected_prefix = {
        "materialized_horizon": 8,
        "core_hit_cylinder_slot_count": 27648,
        "singular_cemetery_cylinder_slot_count": 1152,
        "unresolved_after_horizon_tail_slot_count": 128,
        "total_prefix_partition_slot_count": 28928,
        "slots_may_be_empty": True,
    }
    for key, value in expected_prefix.items():
        if prefix.get(key) != value:
            errors.append(f"prefix {key}")
    if not isinstance(prefix.get("prefix_slot_ids_sha256"), str):
        errors.append("prefix slot digest")

    attachment = result.get("conditional_core_contraction_attachment", {})
    expected_attachment = {
        "finite_core_hit_branches_may_attach_frozen_core_packet": True,
        "shell_dwell_steps": 2018,
        "raw_field7_dwell_steps": 12108,
        "core_2018_step_upper_3_over_8": "CERTIFIED_ABSTRACTLY",
        "attachment_requires_native_no_hidden_recut_audit": True,
        "native_no_hidden_recut_audit": "NOT_CERTIFIED",
    }
    for key, value in expected_attachment.items():
        if attachment.get(key) != value:
            errors.append(f"attachment {key}")

    scope = result.get("strict_nonpromotion", {})
    for key in (
        "branch_ledger_ids_materialize_pointwise_first_core_values",
        "Borel_partition_implies_positive_core_hit_fraction",
        "Borel_partition_implies_quantitative_cemetery_tail",
        "empty_cylinder_slots_are_declared_nonempty",
    ):
        if scope.get(key) is not False:
            errors.append(f"nonpromotion {key}")
    for key in (
        "selected_germ_core_hit_fraction",
        "selected_germ_first_core_destinations",
        "quantitative_cemetery_payload",
        "native_2018_12108_no_recut_dwell",
        "common_strong_space_recovery_operator",
        "Gate3",
        "Gate4",
    ):
        if scope.get(key) != "NOT_CERTIFIED":
            errors.append(f"scope {key}")

    expected_verdict = {
        "selected_oriented_branch_stopping_ledgers_128": "CERTIFIED_TYPED_BOREL",
        "core_singular_nonreturning_decomposition": "CERTIFIED",
        "horizon8_partition_slots_28928": "CERTIFIED_SCHEMA",
        "selected_germ_positive_core_hit_fraction": "NOT_CERTIFIED",
        "quantitative_cemetery_payload": "NOT_CERTIFIED",
        "native_2018_12108_no_recut_dwell": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
    }
    if manifest.get("verdict") != expected_verdict:
        errors.append("verdict")
    return errors


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(
        manifest["result"]
    )


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[str, ...], value: Any) -> None:
        candidate = copy.deepcopy(manifest)
        target: Any = candidate
        for part in path[:-1]:
            target = target[part]
        target[path[-1]] = value
        if path[0] == "result":
            refresh(candidate)
        mutations.append(candidate)

    registry = ("result", "selected_branch_stopping_registry")
    mutate(registry + ("selected_parameter_germ_count",), 63)
    mutate(registry + ("oriented_branch_ledger_count",), 127)
    mutate(registry + ("finite_destination_core_count",), 23)
    mutate(registry + ("hit_branch_count",), 63)
    theorem = ("result", "measurable_core_cemetery_stopping_theorem")
    mutate(theorem + ("extended_billiard_map_T_hat_is_Borel",), False)
    mutate(theorem + ("finite_time_core_hit_sets_are_Borel",), False)
    mutate(theorem + ("nonreturning_cemetery_is_countable_intersection_of_Borel_sets",), False)
    mutate(theorem + ("core_hit_singular_and_nonreturning_classes_are_pairwise_disjoint",), False)
    mutate(theorem + ("core_hit_singular_and_nonreturning_classes_exhaust_each_germ_domain",), False)
    mutate(theorem + ("exact_measure_decomposition_for_every_finite_germ_measure",), False)
    prefix = ("result", "materialized_horizon_8_partition_prefix")
    mutate(prefix + ("materialized_horizon",), 7)
    mutate(prefix + ("core_hit_cylinder_slot_count",), 27647)
    mutate(prefix + ("singular_cemetery_cylinder_slot_count",), 1151)
    mutate(prefix + ("total_prefix_partition_slot_count",), 0)
    mutate(prefix + ("slots_may_be_empty",), False)
    attachment = ("result", "conditional_core_contraction_attachment")
    mutate(attachment + ("shell_dwell_steps",), 2017)
    mutate(attachment + ("native_no_hidden_recut_audit",), "CERTIFIED")
    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("branch_ledger_ids_materialize_pointwise_first_core_values",), True)
    mutate(scope + ("Borel_partition_implies_positive_core_hit_fraction",), True)
    mutate(scope + ("Borel_partition_implies_quantitative_cemetery_tail",), True)
    mutate(scope + ("selected_germ_core_hit_fraction",), "1")
    mutate(scope + ("quantitative_cemetery_payload",), "CERTIFIED")
    mutate(scope + ("native_2018_12108_no_recut_dwell",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(("verdict", "selected_germ_positive_core_hit_fraction"), "CERTIFIED")
    mutate(("verdict", "Gate4"), "CERTIFIED")
    rejected = sum(bool(check(candidate)) for candidate in mutations)
    return rejected, len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except Exception as error:
        print(f"MANIFEST_READ_ERROR: {error}", file=sys.stderr)
        return 1
    errors = check(manifest)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.replay and certificate.build_result() != manifest["result"]:
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
    print("SELECTED_ORIENTED_BRANCH_STOPPING_LEDGERS_128: CERTIFIED_TYPED_BOREL")
    print("CORE_SINGULAR_NONRETURNING_DECOMPOSITION: CERTIFIED")
    print("HORIZON8_PARTITION_SLOTS_28928: CERTIFIED_SCHEMA")
    print("SELECTED_GERM_POSITIVE_CORE_HIT_FRACTION: NOT_CERTIFIED")
    print("QUANTITATIVE_CEMETERY_PAYLOAD: NOT_CERTIFIED")
    print("NATIVE_2018_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
