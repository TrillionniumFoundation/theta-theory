#!/usr/bin/env python3
"""Fail-closed verifier for the round-27 R1 empty physical-face join."""

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
DEFAULT_MANIFEST = HERE / "cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json"
CERTIFICATE = HERE / "cm2_gate5_round27_r1_empty_physical_face_join_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate5.round27-r1-empty-physical-face-join.manifest.v1"
RESULT_SCHEMA = "cm2.gate5.round27-r1-empty-physical-face-join.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "aabe7f375036e68b742695f27a3a274bc47f594e547579e3592cf97f46989c43"
)
EXPECTED_RESULT_DIGEST = (
    "4a2457f6c86aa02f7885a4fe2f4908a2e14ef06d03798d0ba05d936263545580"
)
EXPECTED_DEPENDENCIES = {
    "cm2_gate5_round26_r1_f10_f13_frontier_cert.py": (
        "aaf30efeb424cf2ab9903e52902bc5335452e2c707216765a6e87e833bd29ee4"
    ),
    "cm2-gate5-round26-r1-f10-f13-frontier-manifest-2026-07-18.json": (
        "2078787d2f4bb990be8a20570a1ca5722ed7bca5f5ff4e0fbf77408c2ca30b4a"
    ),
    "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json": (
        "f6950d0a6ccf6984f888a102d846557e807becfddf3a95a72565e514934783e4"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
    "cm2_gate3_depth_one_fixed_gauge_dq_cert.py": (
        "8ce2490ee2b2bdfc251ac1892cb260e40f3eb5d87ce7f232c2076a10c4a9c066"
    ),
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2_gate34_occurrence_boundary_recovery_carrier_cert.py": (
        "9e69879f921681da4a8eeda9a2af8755c3713151128027784e72cd12896a053a"
    ),
    "cm2-gate34-occurrence-boundary-recovery-carrier-manifest-2026-07-17.json": (
        "dd16bd1e3407a6f886ddbf1270ca7ff7289a7d6792e81235f69014cafaf49cb5"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}
EXPECTED_VERDICT = {
    "R1_F10_empty_physical_face_slots": "CERTIFIED_4216",
    "R1_F13_empty_physical_current_slots": "CERTIFIED_4216",
    "atom_occurrence_pair_audit": "CERTIFIED_269824",
    "intersecting_atom_occurrence_pairs": 0,
    "R1_candidate_local_maturity": "13/18",
    "limiting_R1_physical_boundary_face_atlas": "NOT_CERTIFIED",
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
        "schema", "provenance", "physical_occurrence_and_trace_replay",
        "R1_empty_physical_face_F10_F13_slot_registry",
        "Gate5_R1_candidate_local_maturity", "F14_F18_frontier",
        "strict_nonpromotion", "internal_replay_digest",
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

        physical = result.get("physical_occurrence_and_trace_replay", {})
        expected_physical = {
            "occurrence_row_count": 64,
            "physical_hit_trace_seed_count": 64,
            "physical_miss_trace_seed_count": 64,
            "distinct_trace_seed_count": 128,
            "occurrence_ids_sha256": "533d028533771dc92174125af0faa13a0de4af584f8eadb178c001e284f76314",
            "carrier_rows_sha256": "36e6b5a307560ee4ad40f713d94816abe0aecd6894827bbab2026700254851c9",
            "trace_ids_sha256": "c3607a44db1a8faf5531ef91af7d2b99066ddfa1f004cdf4441d68eedfc8c75a",
            "every_occurrence_target_is_grazing_with_p_equal_epsilon": True,
            "grazing_target_abs_p": "1",
        }
        for key, expected in expected_physical.items():
            if not strict_equal(physical.get(key), expected):
                errors.append(f"physical replay: {key}")

        registry = result.get("R1_empty_physical_face_F10_F13_slot_registry", {})
        expected_registry = {
            "R1_inner_atom_count": 4216,
            "physical_homogeneity_subbranch_id_count": 4216,
            "used_source_core_count": 16,
            "physical_occurrence_face_count": 64,
            "atom_occurrence_pair_audit_count": 269824,
            "certified_intersecting_atom_occurrence_pair_count": 0,
            "materialized_candidate_local_slot_count": 8432,
            "empty_physical_face_F10_slot_count": 4216,
            "empty_physical_face_F13_slot_count": 4216,
            "artificial_R1_phase_face_incidence_count": 16864,
            "artificial_R1_phase_faces_used_as_physical_carriers": False,
            "source_obstacle_histogram": {"G": 2164, "W": 2052},
            "atom_ids_sha256": "db9fbc97e5528f13d0e330b8905777d1128e9f99a4d4766b1020331efaea5faf",
            "homogeneity_ids_sha256": "4e395b2c6b2f58be25bf97683b87b1bac30c4f6a29f076cbabd1f6506c52f4e6",
            "selected_target_histogram_sha256": "0ddccb9b953f545586ed9e899d3525d543cfd01c3869a46914cb80113e8007d4",
            "slot_ids_sha256": "229bee854deedaa44edd31fb21d0d2704ac77e7c641b6d26f29e46b6b6aa3694",
            "slot_rows_sha256": "7349a818ab6e4cae4c613bba20b4a4d7dc028a973081cce1478418c85a4ba156",
        }
        for key, expected in expected_registry.items():
            if not strict_equal(registry.get(key), expected):
                errors.append(f"slot registry: {key}")
        expected_reasons = {
            "different_collision_section_component": 133568,
            "different_first_target_excluded_by_strict_first_owner": 106520,
            "same_target_grazing_abs_p_1_disjoint_from_core_abs_p_lt_3_over_10": 29736,
        }
        if not strict_equal(registry.get("atom_occurrence_pair_reason_histogram"), expected_reasons):
            errors.append("pair reason histogram")
        if not strict_equal(
            registry.get("materialized_candidate_local_slot_count_per_field"),
            {
                "coarea_density_regular_bound": 4216,
                "moving_boundary_DQ_current_and_two_traces": 4216,
            },
        ):
            errors.append("per-field slot counts")

        samples = registry.get("representative_slot_rows")
        if not isinstance(samples, list) or len(samples) != 4:
            errors.append("representative slot rows")
        else:
            fields = [row.get("field_name") for row in samples]
            if fields != [
                "coarea_density_regular_bound",
                "moving_boundary_DQ_current_and_two_traces",
                "coarea_density_regular_bound",
                "moving_boundary_DQ_current_and_two_traces",
            ]:
                errors.append("representative field order")
            for row in samples:
                if row.get("physical_occurrence_intersection_count") != 0:
                    errors.append("representative nonempty incidence")
                if row.get("intersecting_physical_occurrence_ids") != []:
                    errors.append("representative occurrence ids")
                if row.get("artificial_R1_phase_faces_used_as_physical_occurrence_faces") is not False:
                    errors.append("representative artificial face promotion")
            f10 = samples[0]
            if f10.get("coarea_density_regular_cost") != "0" or f10.get("empty_sum_convention") is not True:
                errors.append("F10 empty cost")
            f13 = samples[1]
            if f13.get("moving_boundary_current_on_fixed_R1_inner_restriction") != "0":
                errors.append("F13 empty current")
            if f13.get("trace_pair_count") != 0 or f13.get("vacuous_truth_on_certified_empty_physical_face_family") is not True:
                errors.append("F13 trace family")
            if f13.get("smooth_branch_parameter_derivative_is_zero_claimed") is not False:
                errors.append("smooth derivative overpromotion")

        maturity = result.get("Gate5_R1_candidate_local_maturity", {})
        expected_maturity = {
            "required_field_count": 18,
            "prior_candidate_local_maturity": "11/18",
            "new_candidate_local_fields_installed": [
                "coarea_density_regular_bound",
                "moving_boundary_DQ_current_and_two_traces",
            ],
            "candidate_local_maturity_after_exact_empty_face_join": "13/18",
            "first_missing_candidate_local_field": "regular_density_operator_cost",
            "complete_18_field_R1_operator_block_count": 0,
            "global_Gate5_field_credit_added": 0,
            "global_Gate5_maturity_before_and_after": "4/18 -> 4/18",
        }
        for key, expected in expected_maturity.items():
            if not strict_equal(maturity.get(key), expected):
                errors.append(f"maturity: {key}")
        rows = maturity.get("rows")
        if not isinstance(rows, list) or len(rows) != 18:
            errors.append("maturity rows")
        elif sum(row.get("candidate_local_R1_atom_slot_count") == 4216 for row in rows) != 13:
            errors.append("maturity installed count")

        frontier = result.get("F14_F18_frontier", {})
        if frontier.get("F14_through_F18_materialized_slot_count") != 0:
            errors.append("F14-F18 slots")
        if frontier.get("complete_operator_phase_block_count") != 0:
            errors.append("phase blocks")
        if not isinstance(frontier.get("F14_through_F18_rows"), list) or len(frontier["F14_through_F18_rows"]) != 5:
            errors.append("F14-F18 rows")

        scope = result.get("strict_nonpromotion", {})
        for key in (
            "artificial_phase_face_used_as_physical_occurrence_face",
            "stationary_artificial_face_speed_used_as_coarea_density",
            "occurrence_density_seed_copied_to_empty_atom_face_family",
            "empty_local_current_claimed_as_global_depth_one_DQ_current",
            "smooth_branch_parameter_derivative_claimed_zero",
        ):
            if scope.get(key) is not False:
                errors.append(f"scope overpromotion: {key}")
        if scope.get("limiting_R1_physical_boundary_face_atlas") != "NOT_CERTIFIED":
            errors.append("limiting face atlas")
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
    spec = importlib.util.spec_from_file_location("cm2_r27_f10_f13_frozen", CERTIFICATE)
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
    bad = copy.deepcopy(data); bad["verdict"]["intersecting_atom_occurrence_pairs"] = 1; structural.append(("incidence", bad))
    bad = copy.deepcopy(data); bad["unknown"] = 1; structural.append(("unknown-key", bad))
    bad = copy.deepcopy(data); del bad["result"]["strict_nonpromotion"]; structural.append(("missing-key", bad))
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
    if attempted != 83:
        failures.append(f"hostile test count changed: {attempted}")
    return failures, attempted


def print_status() -> None:
    print("R1_F10_EMPTY_PHYSICAL_FACE_SLOTS: 4216 CERTIFIED")
    print("R1_F13_EMPTY_PHYSICAL_CURRENT_SLOTS: 4216 CERTIFIED")
    print("ATOM_OCCURRENCE_PAIR_AUDIT: 269824/269824 DISJOINT")
    print("R1_CANDIDATE_LOCAL_MATURITY: 13/18")
    print("LIMITING_R1_PHYSICAL_FACE_ATLAS: NOT_CERTIFIED")
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
    print("LIVE_MODE: limiting R1 physical faces, F14-F18 and Gate 5 remain open", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
