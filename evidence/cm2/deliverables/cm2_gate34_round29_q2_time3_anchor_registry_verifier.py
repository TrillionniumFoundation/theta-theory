#!/usr/bin/env python3
"""Fail-closed verifier for the round-29 Q2-to-time3 anchor registry."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterator

import cm2_gate34_round29_q2_time3_anchor_registry_cert as cert


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round29-q2-time3-anchor-registry-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_round29_q2_time3_anchor_registry_cert.py"
VERIFIER = Path(__file__).resolve()
EXPECTED_CERTIFICATE_SHA256 = (
    "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b"
)
HOSTILE_TEST_COUNT = 101


class DuplicateKeyError(ValueError):
    pass


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(key)
        out[key] = value
    return out


def parse_json_text(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def load_json(path: Path) -> dict[str, Any]:
    value = parse_json_text(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root is not an object")
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_keys(value: Any, expected: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == expected


def frozen_path_errors() -> list[str]:
    errors: list[str] = []
    frozen = {CERTIFICATE.name: EXPECTED_CERTIFICATE_SHA256, **cert.DEPENDENCIES}
    for name, expected in frozen.items():
        path = HERE / name
        if not path.is_file():
            errors.append(f"missing frozen path: {name}")
        elif path.is_symlink() or path.resolve().parent != HERE:
            errors.append(f"unsafe frozen path: {name}")
        elif sha256_path(path) != expected:
            errors.append(f"frozen hash mismatch: {name}")
    return errors


def semantic_errors(result: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(result, dict):
        return ["result type"]
    if result.get("schema") != cert.RESULT_SCHEMA:
        errors.append("result schema")
    provenance = result.get("provenance", {})
    expected_provenance = {
        "old_artifacts_modified": False,
        "precision_bits": 384,
        "full_Q2_anchor_replay": True,
        "frozen_Q2_anchor_count": 114006,
    }
    for key, expected in expected_provenance.items():
        if provenance.get(key) != expected or type(provenance.get(key)) is not type(expected):
            errors.append(f"provenance: {key}")
    if not strict_equal(provenance.get("dependency_sha256"), cert.DEPENDENCIES):
        errors.append("provenance dependencies")

    contract = result.get("time3_finite_root_registry_contract", {})
    contract_expected = {
        "adaptive_extra_depth": 0,
        "maximal_component_of_full_physical_path_fibre": False,
        "finite_outer_is_collision_null": False,
        "finite_admitted_zero_would_imply_physical_R3_empty": False,
        "observed_ratios_are_uniform_or_iterable": False,
    }
    for key, expected in contract_expected.items():
        if contract.get(key) != expected or type(contract.get(key)) is not type(expected):
            errors.append(f"contract: {key}")

    registry = result.get("Q2_to_time3_whole_box_registry", {})
    histogram = registry.get("classification_histogram", {})
    required_kinds = {
        "RETURN_AT_3_INNER", "SURVIVE_THROUGH_3_INNER",
        "UNRESOLVED_TIME3_OUTER",
    }
    if not isinstance(histogram, dict) or not required_kinds.issubset(histogram):
        errors.append("classification histogram")
    elif any(type(histogram[key]) is not int or histogram[key] < 0 for key in required_kinds):
        errors.append("classification histogram values")
    else:
        if sum(histogram[key] for key in required_kinds) != 114006:
            errors.append("classification total")
        if registry.get("materialized_R3_inner_component_count") != histogram[
            "RETURN_AT_3_INNER"
        ]:
            errors.append("R3 count")
        if registry.get("materialized_Q3_inner_component_count") != histogram[
            "SURVIVE_THROUGH_3_INNER"
        ]:
            errors.append("Q3 count")
        if registry.get("materialized_admitted_component_count") != (
            histogram["RETURN_AT_3_INNER"]
            + histogram["SURVIVE_THROUGH_3_INNER"]
        ):
            errors.append("admitted count")
    registry_expected = {
        "Q2_anchor_count": 114006,
        "time3_terminal_root_box_count": 114006,
        "parameter_averaged_total_Q2_anchor_mass_exact":
            "5257799/5120000000",
        "R3_plus_Q3_plus_finite_outer_mass_equals_Q2_anchor_mass": True,
        "every_R3_cell_is_first_return_at_exact_collision_time3": True,
        "every_Q3_cell_avoids_C24_at_collision_times1_2_3": True,
    }
    for key, expected in registry_expected.items():
        if registry.get(key) != expected or type(registry.get(key)) is not type(expected):
            errors.append(f"registry: {key}")
    if not isinstance(registry.get("representative_admitted_rows"), list):
        errors.append("admitted representatives")
    if not isinstance(registry.get("representative_finite_outer_rows"), list):
        errors.append("outer representatives")

    payload = result.get("time3_typed_payload_frontier", {})
    admitted = registry.get("materialized_admitted_component_count")
    if type(admitted) is int:
        if payload.get("common_forward_reverse_restriction_id_count") != admitted:
            errors.append("restriction count")
    strict_h3 = payload.get("time3_homogeneity_child_id_count")
    for key in (
        "time3_canonical_recut_branch_rule_id_count",
        "F5_three_step_universal_branch_rule_slot_count",
        "F6_three_step_universal_branch_rule_slot_count",
    ):
        if payload.get(key) != strict_h3:
            errors.append(f"homogeneity payload: {key}")
    payload_expected = {
        "actual_curve_recut_instance_id_count": 0,
        "F5_three_step_inverse_strict_upper":
            str(cert.homogeneity_cert.THETA ** 3),
        "F6_three_step_log_variation_strict_upper":
            str(3 * cert.homogeneity_cert.ONE_STEP_LOG_VARIATION),
        "invariant_area_Jacobian_value_on_every_admitted_branch": "1",
        "invariant_area_Jacobian_is_unstable_Jacobian": False,
        "numeric_C_fw_count": 0,
        "numeric_C_rev_count": 0,
        "numeric_strong_q3_count": 0,
        "charged_characteristic_Z_F7_count": 0,
    }
    for key, expected in payload_expected.items():
        if payload.get(key) != expected or type(payload.get(key)) is not type(expected):
            errors.append(f"payload: {key}")

    frontier = result.get("arbitrary_n_and_limiting_frontier", {})
    frontier_expected = {
        "round27_arbitrary_n_regular_component_existence_schema":
            "CERTIFIED_NONCONSTRUCTIVE_DEPENDENCY",
        "complete_limiting_physical_R3_Q3_partition_mod_collision_null":
            "CERTIFIED_NONCONSTRUCTIVE_DEPENDENCY",
        "complete_limiting_R3_Q3_component_enumeration": "NOT_CERTIFIED",
        "uniform_adaptive_time3_termination_rate": "NOT_CERTIFIED",
        "arbitrary_n_numeric_singularity_growth": "NOT_CERTIFIED",
        "survivor_conditioned_recovery": "NOT_CERTIFIED",
        "strong_q_weighted_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
    }
    for key, expected in frontier_expected.items():
        if frontier.get(key) != expected:
            errors.append(f"frontier: {key}")

    nonpromotion = result.get("strict_nonpromotion", {})
    for key in ("Gate3", "Gate4", "Gate5"):
        if nonpromotion.get(key) != "NOT_CERTIFIED":
            errors.append(f"nonpromotion: {key}")
    if nonpromotion.get("CM2") != "NO-GO_FOR_CLAIM":
        errors.append("CM2 nonpromotion")
    if nonpromotion.get("finite_outer_promoted_to_null") is not False:
        errors.append("finite outer promotion")
    if nonpromotion.get("finite_histogram_extrapolated_to_tail") is not False:
        errors.append("histogram promotion")

    internal = result.get("internal_replay_digest")
    payload_copy = copy.deepcopy(result)
    payload_copy.pop("internal_replay_digest", None)
    if internal != cert.canonical_digest(payload_copy):
        errors.append("internal replay digest")
    return errors


def validate(
    data: dict[str, Any], *, replay_result: dict[str, Any] | None,
    check_integrity: bool,
) -> list[str]:
    errors: list[str] = []
    if not exact_keys(data, {
        "schema", "certificate_sha256", "verifier_sha256",
        "dependencies", "result", "verdict",
    }):
        errors.append("manifest top-level key set")
    if data.get("schema") != cert.MANIFEST_SCHEMA:
        errors.append("manifest schema")
    if data.get("certificate_sha256") != EXPECTED_CERTIFICATE_SHA256:
        errors.append("certificate hash field")
    if data.get("verifier_sha256") != sha256_path(VERIFIER):
        errors.append("verifier hash field")
    if not strict_equal(data.get("dependencies"), cert.DEPENDENCIES):
        errors.append("dependency table")
    errors.extend(semantic_errors(data.get("result")))
    if replay_result is not None:
        if not strict_equal(data.get("result"), replay_result):
            errors.append("fresh full replay mismatch")
        if not strict_equal(data.get("verdict"), cert.verdict(replay_result)):
            errors.append("verdict mismatch")
    elif not isinstance(data.get("verdict"), dict):
        errors.append("verdict type")
    if check_integrity:
        errors.extend(frozen_path_errors())
    return errors


def scalar_paths(value: Any, prefix: tuple[Any, ...] = ()) -> Iterator[tuple[Any, ...]]:
    if isinstance(value, dict):
        for key in sorted(value):
            yield from scalar_paths(value[key], prefix + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from scalar_paths(item, prefix + (index,))
    else:
        yield prefix


def mutate_at_path(value: Any, path: tuple[Any, ...], serial: int) -> None:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    key = path[-1]
    old = cursor[key]
    if type(old) is bool:
        cursor[key] = not old
    elif type(old) is int:
        cursor[key] = old + 1 + serial
    elif old is None:
        cursor[key] = f"hostile-{serial}"
    elif isinstance(old, str):
        cursor[key] = old + f"#hostile-{serial}"
    else:
        cursor[key] = {"hostile": serial}


def hostile_self_test(data: dict[str, Any]) -> tuple[int, int]:
    tests: list[dict[str, Any]] = []
    paths = list(scalar_paths(data))
    for serial, path in enumerate(paths[:HOSTILE_TEST_COUNT]):
        mutant = copy.deepcopy(data)
        mutate_at_path(mutant, path, serial)
        tests.append(mutant)
    if len(tests) < HOSTILE_TEST_COUNT:
        raise RuntimeError("insufficient hostile scalar paths")
    passed = 0
    frozen_replay = data["result"]
    for mutant in tests:
        if validate(mutant, replay_result=frozen_replay, check_integrity=False):
            passed += 1
    return passed, len(tests)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    try:
        data = load_json(args.manifest)
    except Exception as exc:
        print(f"MANIFEST_PARSE: FAIL: {exc}")
        return 1

    if args.self_test:
        passed, total = hostile_self_test(data)
        print(f"HOSTILE_TESTS: {passed}/{total}")
        return 0 if passed == total == HOSTILE_TEST_COUNT else 1

    replay_result = cert.build_result() if args.replay else None
    errors = validate(
        data, replay_result=replay_result,
        check_integrity=True,
    )
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("INTEGRITY: PASS")
    if args.replay:
        print("FULL_114006_Q2_TIME3_REPLAY: PASS")
        print("VERDICT_REPLAY: PASS")
        return 0
    if args.integrity_only:
        return 0
    print("LIVE_GATE3_GATE4_GATE5: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
