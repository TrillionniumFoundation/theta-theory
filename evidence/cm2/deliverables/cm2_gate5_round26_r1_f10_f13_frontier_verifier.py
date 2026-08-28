#!/usr/bin/env python3
"""Fail-closed verifier for the round-26 R1 F10--F13 typed frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2-gate5-round26-r1-f10-f13-frontier-manifest-2026-07-18.json"
CERTIFICATE = HERE / "cm2_gate5_round26_r1_f10_f13_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate5.round26-r1-f10-f13-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate5.round26-r1-f10-f13-frontier.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "aaf30efeb424cf2ab9903e52902bc5335452e2c707216765a6e87e833bd29ee4"
)
EXPECTED_RESULT_DIGEST = (
    "2ef722e84b000768d2d598eeb600bf94319bda321fdb852134ea4c7483fcd36a"
)
EXPECTED_DEPENDENCIES = {
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json": (
        "f6950d0a6ccf6984f888a102d846557e807becfddf3a95a72565e514934783e4"
    ),
    "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json": (
        "6b9354026a1707a25971925e02acbb5ea7e459ca177190a28ff1b39857283d86"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json": (
        "b38772a41d0b610e1e1cd4fb4509cfb76227cc8f4983af0699d2cf38e60650c5"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}
EXPECTED_VERDICT = {
    "R1_candidate_local_F11_slots": "CERTIFIED_4216",
    "R1_candidate_local_F12_slots": "CERTIFIED_4216",
    "first_unfillable_candidate_local_field_F10": "NOT_CERTIFIED",
    "F13_moving_boundary_DQ": "NOT_CERTIFIED",
    "R1_candidate_local_maturity": "11/18",
    "complete_18_field_R1_operator_blocks": 0,
    "global_Gate5_maturity": "4/18_UNCHANGED",
    "Gate5": "NOT_CERTIFIED",
    "CM2": "NO-GO_FOR_CLAIM",
}


class DuplicateKeyError(ValueError):
    pass


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


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise ValueError("manifest path")
    value = parse_json_text(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root")
    return value


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


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def exact_keys(value: Any, expected: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == expected


def frozen_path_errors() -> list[str]:
    errors: list[str] = []
    frozen = {CERTIFICATE.name: EXPECTED_CERTIFICATE_SHA256, **EXPECTED_DEPENDENCIES}
    for name, expected in frozen.items():
        path = HERE / name
        if not path.is_file():
            errors.append(f"missing frozen path: {name}")
        elif path.is_symlink() or path.resolve().parent != HERE:
            errors.append(f"unsafe frozen path: {name}")
        elif sha256_path(path) != expected:
            errors.append(f"frozen hash mismatch: {name}")
    return errors


def validate(data: dict[str, Any], *, check_integrity: bool) -> list[str]:
    errors: list[str] = []
    if not exact_keys(
        data,
        {"schema", "certificate_sha256", "verifier_sha256", "dependencies", "result", "verdict"},
    ):
        errors.append("manifest top-level key set")
    if data.get("schema") != MANIFEST_SCHEMA:
        errors.append("manifest schema")
    if data.get("certificate_sha256") != EXPECTED_CERTIFICATE_SHA256:
        errors.append("certificate hash field")
    if not strict_equal(data.get("dependencies"), EXPECTED_DEPENDENCIES):
        errors.append("dependency table")
    if not strict_equal(data.get("verdict"), EXPECTED_VERDICT):
        errors.append("verdict")

    result = data.get("result")
    result_keys = {
        "schema", "provenance", "candidate_local_F11_F12_templates",
        "R1_candidate_local_F11_F12_slot_registry",
        "F10_coarea_density_regular_obstruction",
        "F13_moving_boundary_DQ_obstruction", "F14_F18_frontier",
        "Gate5_R1_candidate_local_maturity", "strict_nonpromotion",
        "internal_replay_digest",
    }
    if not exact_keys(result, result_keys):
        errors.append("result key set")
    elif isinstance(result, dict):
        if result.get("schema") != RESULT_SCHEMA:
            errors.append("result schema")
        actual_digest = result_digest(result)
        if result.get("internal_replay_digest") != actual_digest:
            errors.append("internal replay digest")
        if actual_digest != EXPECTED_RESULT_DIGEST:
            errors.append("frozen result digest")

        templates = result.get("candidate_local_F11_F12_templates", {})
        if not exact_keys(templates, {"F11", "F12"}):
            errors.append("template key set")
        else:
            if templates["F11"].get("fixed_s_full_collision_branch_pullback_cost_strict_upper") != "158":
                errors.append("F11 coefficient")
            if templates["F11"].get("return_wide_dynamic_test_operator_cost_claimed") is not False:
                errors.append("F11 overpromotion")
            if templates["F12"].get("C1_sum_norm_pullback_strict_upper") != "159":
                errors.append("F12 coefficient")
            if templates["F12"].get("physical_hit_miss_trace_or_DQ_current_claimed") is not False:
                errors.append("F12 overpromotion")

        registry = result.get("R1_candidate_local_F11_F12_slot_registry", {})
        expected_registry = {
            "R1_inner_atom_count": 4216,
            "materialized_candidate_local_slot_count": 8432,
            "fixed_s_phase_face_incidence_count": 16864,
            "physical_homogeneity_subbranch_id_count": 4216,
            "source_core_count": 16,
            "destination_core_count": 16,
            "distinct_parameter_guard_interval_count": 48,
            "parameter_guards_touching_s0_count": 352,
            "parameter_guards_owning_s0_count": 176,
            "parameter_guards_with_s0_in_relative_interior_count": 0,
            "atom_ids_sha256": "db9fbc97e5528f13d0e330b8905777d1128e9f99a4d4766b1020331efaea5faf",
            "homogeneity_ids_sha256": "4e395b2c6b2f58be25bf97683b87b1bac30c4f6a29f076cbabd1f6506c52f4e6",
            "slot_ids_sha256": "2c7de87ed6cf3c73e0bc8ca66e7d1b46e936ec36747e9530621087a2556a8a29",
            "slot_rows_sha256": "17ec6eef1e6a63cf001cb231bb1116626f249863213f275fc0f67ba8f753c580",
            "companion_packet_rows_sha256": "80226c09c164727e5d914e244ef355889a5aaf39a8fa0bd9e2708ca6f6308a59",
            "parameter_guard_histogram_sha256": "6aa421acd6027ec8b8889ab7a4c99c3603b83a2cf410afce839bbe7872d7dce4",
        }
        for key, expected in expected_registry.items():
            if not strict_equal(registry.get(key), expected):
                errors.append(f"slot registry: {key}")
        if not strict_equal(
            registry.get("materialized_candidate_local_slot_count_per_field"),
            {
                "dynamic_Holder_test_pullback_bound": 4216,
                "C1_face_trace_pullback_bound": 4216,
            },
        ):
            errors.append("slot per-field counts")
        if registry.get("exact_F1_F9_companion_atom_join") is not True:
            errors.append("companion join")
        if registry.get("all_artificial_phase_faces_have_zero_velocity_in_common_fixed_section_coordinates") is not True:
            errors.append("fixed-section face audit")
        if not isinstance(registry.get("representative_slot_rows"), list) or len(registry["representative_slot_rows"]) != 4:
            errors.append("representative slots")

        f10 = result.get("F10_coarea_density_regular_obstruction", {})
        expected_f10 = {
            "field_index": 10,
            "field_name": "coarea_density_regular_bound",
            "frozen_physical_occurrence_face_count": 64,
            "physical_occurrence_density_magnitude_upper": "18/5",
            "R1_artificial_fixed_s_phase_face_incidence_count": 16864,
            "materialized_occurrence_id_to_R1_atom_id_to_phase_face_id_join_count": 0,
            "F10_candidate_local_slot_count": 0,
            "F10_status": "NOT_CERTIFIED",
        }
        for key, expected in expected_f10.items():
            if not strict_equal(f10.get(key), expected):
                errors.append(f"F10 obstruction: {key}")

        f13 = result.get("F13_moving_boundary_DQ_obstruction", {})
        expected_f13 = {
            "field_index": 13,
            "field_name": "moving_boundary_DQ_current_and_two_traces",
            "R1_parameter_guards_touching_s0_count": 352,
            "R1_parameter_guards_owning_s0_count": 176,
            "R1_parameter_guards_with_s0_in_relative_interior_count": 0,
            "half_open_guard_endpoint_is_DQ_atlas_row": False,
            "fixed_s_artificial_phase_face_zero_speed_is_physical_DQ_current": False,
            "materialized_occurrence_hit_miss_trace_to_R1_face_join_count": 0,
            "F13_candidate_local_slot_count": 0,
            "F13_status": "NOT_CERTIFIED",
        }
        for key, expected in expected_f13.items():
            if not strict_equal(f13.get(key), expected):
                errors.append(f"F13 obstruction: {key}")

        downstream = result.get("F14_F18_frontier", {})
        if downstream.get("F14_through_F18_materialized_slot_count") != 0:
            errors.append("F14-F18 slots")
        if downstream.get("operator_phase_block_count") != 0:
            errors.append("phase blocks")
        rows = downstream.get("F14_through_F18_rows")
        if not isinstance(rows, list) or len(rows) != 5:
            errors.append("F14-F18 rows")

        maturity = result.get("Gate5_R1_candidate_local_maturity", {})
        expected_maturity = {
            "prior_candidate_local_maturity": "9/18",
            "candidate_local_maturity_after_independent_join": "11/18",
            "first_missing_candidate_local_field": "coarea_density_regular_bound",
            "complete_18_field_R1_operator_block_count": 0,
            "global_Gate5_field_credit_added": 0,
            "global_Gate5_maturity_before_and_after": "4/18 -> 4/18",
        }
        for key, expected in expected_maturity.items():
            if not strict_equal(maturity.get(key), expected):
                errors.append(f"maturity: {key}")
        if not isinstance(maturity.get("rows"), list) or len(maturity["rows"]) != 18:
            errors.append("maturity rows")

        scope = result.get("strict_nonpromotion", {})
        for key in (
            "zero_speed_artificial_face_used_as_physical_coarea_current",
            "collision_SRB_area_Jacobian_used_as_face_density_or_unstable_Jacobian",
            "occurrence_level_density_seed_copied_to_R1_atoms_without_join",
            "half_open_parameter_guard_promoted_to_dynamic_DQ_atlas",
            "F11_F12_candidate_slots_are_return_wide_operator_costs",
        ):
            if scope.get(key) is not False:
                errors.append(f"scope overpromotion: {key}")
        if scope.get("Gate5") != "NOT_CERTIFIED" or scope.get("CM2") != "NO-GO_FOR_CLAIM":
            errors.append("scope verdict")

    if check_integrity:
        errors.extend(frozen_path_errors())
        verifier_sha = data.get("verifier_sha256")
        if not isinstance(verifier_sha, str) or verifier_sha != sha256_path(VERIFIER):
            errors.append("verifier hash")
    return errors


def load_certificate() -> ModuleType:
    if sys.flags.optimize != 0:
        raise RuntimeError("optimized Python is forbidden")
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate changed before import")
    spec = importlib.util.spec_from_file_location("cm2_r26_f10_f13_frozen", CERTIFICATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("certificate import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    imported = Path(module.__file__).resolve()
    if imported != CERTIFICATE.resolve() or imported.is_symlink():
        raise RuntimeError("certificate import path")
    if sha256_path(imported) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate changed during import")
    return module


def replay(data: dict[str, Any]) -> list[str]:
    before = {
        name: sha256_path(HERE / name)
        for name in (CERTIFICATE.name, *EXPECTED_DEPENDENCIES)
    }
    try:
        actual = load_certificate().certify()
    except Exception as exc:
        return [f"certificate replay raised: {exc}"]
    after = {
        name: sha256_path(HERE / name)
        for name in (CERTIFICATE.name, *EXPECTED_DEPENDENCIES)
    }
    errors: list[str] = []
    if before != after:
        errors.append("frozen files changed during replay")
    if canonical_json(actual) != canonical_json(data.get("result")):
        errors.append("certificate replay differs")
    return errors


def flatten_scalar_paths(value: Any, prefix: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    paths: list[tuple[Any, ...]] = []
    if isinstance(value, dict):
        for key in sorted(value):
            if key == "internal_replay_digest":
                continue
            paths.extend(flatten_scalar_paths(value[key], prefix + (key,)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            paths.extend(flatten_scalar_paths(item, prefix + (index,)))
    else:
        paths.append(prefix)
    return paths


def get_parent(value: Any, path: tuple[Any, ...]) -> tuple[Any, Any]:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    return cursor, path[-1]


def hostile_value(value: Any) -> Any:
    if value is None:
        return 0
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if isinstance(value, str):
        return value + "!"
    raise TypeError(type(value).__name__)


def self_test(data: dict[str, Any]) -> tuple[list[str], int]:
    failures: list[str] = []
    attempted = 0
    result = data.get("result")
    if not isinstance(result, dict):
        return ["self-test requires result"], attempted
    paths = flatten_scalar_paths(result)
    if len(paths) < 70:
        return ["insufficient scalar mutation paths"], attempted
    for path in paths[:70]:
        bad = copy.deepcopy(data)
        parent, key = get_parent(bad["result"], path)
        parent[key] = hostile_value(parent[key])
        bad["result"]["internal_replay_digest"] = result_digest(bad["result"])
        attempted += 1
        if not validate(bad, check_integrity=True):
            failures.append("semantic mutation accepted: " + "/".join(map(str, path)))

    structural: list[tuple[str, Any]] = []
    bad = copy.deepcopy(data); bad["schema"] += "!"; structural.append(("schema", bad))
    bad = copy.deepcopy(data); bad["certificate_sha256"] = "0" * 64; structural.append(("certificate", bad))
    bad = copy.deepcopy(data); bad["verifier_sha256"] = "0" * 64; structural.append(("verifier", bad))
    bad = copy.deepcopy(data); bad["dependencies"][sorted(EXPECTED_DEPENDENCIES)[0]] = "f" * 64; structural.append(("dependency", bad))
    bad = copy.deepcopy(data); bad["verdict"]["Gate5"] = "CERTIFIED"; structural.append(("gate", bad))
    bad = copy.deepcopy(data); bad["unknown"] = 1; structural.append(("unknown-key", bad))
    for name, bad in structural:
        attempted += 1
        if not validate(bad, check_integrity=True):
            failures.append(f"structural mutation accepted: {name}")

    raw_cases = {
        "duplicate": '{"x":1,"x":2}',
        "nan": '{"x":NaN}',
        "infinity": '{"x":Infinity}',
        "negative-infinity": '{"x":-Infinity}',
        "malformed": '{"x":',
    }
    for name, raw in raw_cases.items():
        attempted += 1
        try:
            parse_json_text(raw)
        except Exception:
            continue
        failures.append(f"raw parser mutation accepted: {name}")
    if attempted != 81:
        failures.append(f"hostile test count changed: {attempted}")
    return failures, attempted


def print_status() -> None:
    print("R1_CANDIDATE_LOCAL_F11_SLOTS: 4216 CERTIFIED")
    print("R1_CANDIDATE_LOCAL_F12_SLOTS: 4216 CERTIFIED")
    print("FIRST_UNFILLABLE_FIELD_F10: NOT_CERTIFIED")
    print("F13_MOVING_BOUNDARY_DQ: NOT_CERTIFIED")
    print("R1_CANDIDATE_LOCAL_MATURITY: 11/18")
    print("COMPLETE_18_FIELD_R1_BLOCKS: 0")
    print("GLOBAL_GATE5_MATURITY: 4/18 UNCHANGED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = load_json(args.manifest)
    except Exception as exc:
        print(f"manifest load failed: {exc}", file=sys.stderr)
        return 1
    errors = validate(data, check_integrity=True)
    attempted = 0
    if args.replay:
        errors.extend(replay(data))
    if args.self_test:
        test_errors, attempted = self_test(data)
        errors.extend(test_errors)
    print_status()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.self_test:
        print(f"HOSTILE_TESTS: {attempted}/{attempted} PASS")
    if args.integrity_only or args.replay or args.self_test:
        print("AUDIT_MODE: PASS")
        return 0
    print("LIVE_MODE: F10, F13, complete R1 and Gate 5 remain open", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
