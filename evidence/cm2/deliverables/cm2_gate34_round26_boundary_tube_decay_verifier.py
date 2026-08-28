#!/usr/bin/env python3
"""Fail-closed verifier for the round-26 C24 boundary-tube decay leaf."""

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
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_round26_boundary_tube_decay_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate34.round26-boundary-tube-decay.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.round26-boundary-tube-decay.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "aaeff6582d966f873402986445cc370d22fd38606d4f1e7226b4677c03f94655"
)
EXPECTED_RESULT_DIGEST = (
    "8cd36f1dd3a626719b15be6736c9167b6b180cf7651823527e239ee9c7e37be9"
)
EXPECTED_DEPENDENCIES = {
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json": (
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
    ),
    "cm2_gate5_round25_adaptive_face_f789_cert.py": (
        "d8c4b28ee856927f63bbbb746ea26fd2d7d473b2a3a0009d5c0836fadff3e63a"
    ),
    "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json": (
        "6b9354026a1707a25971925e02acbb5ea7e459ca177190a28ff1b39857283d86"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_gate3_candidate_first_hit_cert.py": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
}
EXPECTED_VERDICT = {
    "round25_53752_child_fresh_Arb_replay": "CERTIFIED",
    "one_generation_residual_mass_ratio_lt_7_over_8": "CERTIFIED_NONITERABLE",
    "dependency_neutral_fair_boundary_tube_decay_O_2_to_minus_d_over_3": "CERTIFIED",
    "limiting_step1_R1_Q1_partition_mod_collision_null_set": "CERTIFIED",
    "finite_depth_unresolved_exhaustion": "NOT_CERTIFIED",
    "finite_complete_step1_branch_ledger": "NOT_MATERIALIZED",
    "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
    "q_weighted_return_tail": "NOT_CERTIFIED",
    "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
    "Gate3": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED",
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
    value = parse_json_text(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root is not an object")
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
        "schema", "provenance", "frozen_parent_frontier",
        "fresh_53752_child_replay", "regular_local_diffeomorphism_audit",
        "dependency_neutral_derivative_budget", "fair_dyadic_boundary_tube_theorem",
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

        provenance = result.get("provenance", {})
        if provenance.get("finite_child_precision_bits") != 384:
            errors.append("child precision")
        if provenance.get("decay_engine") != (
            "exact midpoint Lipschitz radius plus adaptive-precision Arb"
        ):
            errors.append("decay engine")

        parent = result.get("frozen_parent_frontier", {})
        expected_parent = {
            "unresolved_parent_count": 26876,
            "planned_child_count": 53752,
            "unresolved_parent_base_mass": "44519/256000000",
            "parent_depth_histogram": {"12": 6816, "15": 20060},
            "scheduled_split_axis_histogram": {"t": 26876},
            "planned_split_record_rows_sha256": (
                "7ab264eef8af4a156c988da008b271d9deb1c89e665d7ba99cbf8f9c63e6767b"
            ),
        }
        if not strict_equal(parent, expected_parent):
            errors.append("parent frontier")

        child = result.get("fresh_53752_child_replay", {})
        expected_child = {
            "fresh_child_count": 53752,
            "classification_histogram": {
                "RETURN_AT_1_INNER": 4088,
                "SURVIVE_THROUGH_1_INNER": 2048,
                "UNRESOLVED_OUTER": 47616,
            },
            "child_depth_histogram": {"13": 13632, "16": 40120},
            "mass_by_class": {
                "RETURN_AT_1_INNER": "5953/1024000000",
                "SURVIVE_THROUGH_1_INNER": "17319/1024000000",
                "UNRESOLVED_OUTER": "38701/256000000",
            },
            "exact_total_child_mass": "44519/256000000",
            "residual_mass_ratio_to_parent": "38701/44519",
            "residual_mass_ratio_strict_upper_benchmark": "7/8",
            "new_terminal_child_count": 6136,
            "new_terminal_base_mass": "2909/128000000",
            "fresh_child_rows_sha256": (
                "1afa9d1337bdacec5082b9d7f507e673fa69e2bd05a9bd011da8132e917faa05"
            ),
            "parent_conservation_rows_sha256": (
                "1c37459c71f51d2d86cfba422e0a29342ac3f4512e5c2a2188f7bd732ac99b10"
            ),
        }
        for key, expected in expected_child.items():
            if not strict_equal(child.get(key), expected):
                errors.append(f"child replay: {key}")
        if not isinstance(child.get("representative_child_rows"), list) or len(
            child["representative_child_rows"]
        ) != 3:
            errors.append("representative child rows")

        regularity = result.get("regular_local_diffeomorphism_audit", {})
        expected_regularity = {
            "regular_parent_branch_count": 24,
            "all_parent_branches_strict_first_owner": True,
            "all_parent_branches_abs_output_p_lt_1_over_5": True,
            "all_parent_branches_reversible_local_diffeomorphisms": True,
            "invariant_area_form": "R_obstacle dtheta dp",
            "billiard_map_absolute_invariant_area_Jacobian": "1",
            "parent_regularity_rows_sha256": (
                "c16c00900985100419ae083ca661364b9c4523140283351c99ccc7b2b9b24a0d"
            ),
        }
        for key, expected in expected_regularity.items():
            if not strict_equal(regularity.get(key), expected):
                errors.append(f"regularity: {key}")
        if not isinstance(regularity.get("representative_parent_regularity_rows"), list) or len(
            regularity["representative_parent_regularity_rows"]
        ) != 3:
            errors.append("representative regularity rows")

        derivative = result.get("dependency_neutral_derivative_budget", {})
        expected_derivative = {
            "fair_depth_scale": "h_d=2^(-floor(d/3))",
            "source_normal_t_derivative_strict_upper": "3/2",
            "source_velocity_p_derivative_strict_upper": "2",
            "center_distance_strict_upper": "4",
            "output_p_partial_derivative_strict_uppers_t_p_s": ["44", "50", "7"],
            "target_normal_component_partial_derivative_strict_uppers_t_p_s": [
                "48", "55", "8"
            ],
            "exact_center_to_box_output_p_radius_coefficient": "99/80",
            "exact_center_to_box_target_t_radius_coefficient": "34/25",
            "Arb_center_ball_required_radius_relative_to_h": "1/100",
            "dependency_neutral_output_p_radius_coefficient": "5/4",
            "dependency_neutral_target_t_radius_coefficient": "7/5",
            "natural_interval_dependency_used_for_decay_theorem": False,
        }
        for key, expected in expected_derivative.items():
            if not strict_equal(derivative.get(key), expected):
                errors.append(f"derivative budget: {key}")

        tube = result.get("fair_dyadic_boundary_tube_theorem", {})
        expected_tube = {
            "fair_absolute_binary_depth_threshold": 24,
            "threshold_h": "1/256",
            "destination_core_rectangle_count": 24,
            "physical_t_face_count": 48,
            "physical_p_face_count": 48,
            "additional_chart_seam_face_count": 0,
            "major_normal_component_strict_lower_at_threshold": "7/10",
            "max_twice_expanded_abs_t_at_threshold": "91/128",
            "expanded_dtheta_dt_strict_upper": "3/2",
            "radius_weighted_p_width_sum": "546/3125",
            "radius_weighted_t_width_sum": "39/625",
            "radius_multiplicity_sum": "156/25",
            "outer_tube_linear_coefficient": "60489/15625",
            "outer_tube_quadratic_coefficient": "26208/25",
            "outer_tube_effective_coefficient_at_h_le_1_over_256": (
                "995787/125000"
            ),
            "outer_tube_effective_coefficient_strict_upper": "8",
            "asymptotic_rate": "O(2^(-d/3))",
            "uniform_in_parameter_including_endpoints": True,
            "boundary_preimage_collision_measure_zero": True,
            "limiting_step1_R1_Q1_partition_mod_collision_null_set": "CERTIFIED",
        }
        for key, expected in expected_tube.items():
            if not strict_equal(tube.get(key), expected):
                errors.append(f"tube theorem: {key}")
        if tube.get("uniform_parameter_averaged_unresolved_base_mass_bound") != (
            "M_base(U_d)<=B(h_d)<8h_d for every fair frontier with d>=24"
        ):
            errors.append("base tube conclusion")
        if tube.get("uniform_parameter_averaged_normalized_collision_SRB_bound") != (
            "mu(U_d)<(50/39)h_d for every fair frontier with d>=24"
        ):
            errors.append("normalized tube conclusion")
        if tube.get("three_split_cycle_bound") != (
            "M_base(U_(24+3j))<2^(-5-j) for every integer j>=0"
        ):
            errors.append("cycle conclusion")

        scope = result.get("strict_nonpromotion", {})
        if scope.get("natural_Arb_one_generation_ratio_automatically_iterable") is not False:
            errors.append("natural Arb overpromotion")
        if scope.get("finite_depth_unresolved_cover_empty") is not False:
            errors.append("finite exhaustion overpromotion")
        if scope.get("finite_complete_step1_R1_Q1_ledger") != "NOT_MATERIALIZED":
            errors.append("finite ledger scope")
        for key in (
            "arbitrary_n_Rn_Qn_partition", "survivor_conditioned_recovery",
            "strong_q_weighted_tail", "induced_strong_Lasota_Yorke",
            "Gate3", "Gate4", "Gate5",
        ):
            if scope.get(key) != "NOT_CERTIFIED":
                errors.append(f"scope overpromotion: {key}")
        if scope.get("CM2") != "NO-GO_FOR_CLAIM":
            errors.append("CM2 scope")

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
    spec = importlib.util.spec_from_file_location("cm2_r26_boundary_tube_frozen", CERTIFICATE)
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
    if len(paths) < 64:
        return ["insufficient scalar mutation paths"], attempted
    for path in paths[:64]:
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
    if attempted != 75:
        failures.append(f"hostile test count changed: {attempted}")
    return failures, attempted


def print_status() -> None:
    print("ROUND25_53752_CHILD_FRESH_ARB_REPLAY: CERTIFIED")
    print("ONE_GENERATION_RESIDUAL_RATIO: 38701/44519 < 7/8 (NONITERABLE)")
    print("FAIR_BOUNDARY_TUBE_DECAY: O(2^(-d/3)) CERTIFIED")
    print("LIMITING_STEP1_R1_Q1_MOD_NULL: CERTIFIED")
    print("ARBITRARY_N_RN_QN: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")


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
    print("LIVE_MODE: arbitrary-n return partition and strong gates remain open",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
