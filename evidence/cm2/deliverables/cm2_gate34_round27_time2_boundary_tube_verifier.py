#!/usr/bin/env python3
"""Fail-closed verifier for the round-27 composed time-two tube theorem."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round27-time2-boundary-tube-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_round27_time2_boundary_tube_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate34.round27-time2-boundary-tube.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.round27-time2-boundary-tube.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "f219accf6f75da15860b512b3e71e5dbfe6e4d5076dcd03b03e2b24ab2c9d695"
)
EXPECTED_RESULT_DIGEST = (
    "02a5e8ab77365e78ca074a8afe8530bb8040deac9c734a331f59aaaea2be1cc8"
)
EXPECTED_DEPENDENCIES = {
    "cm2_gate34_round26_boundary_tube_decay_cert.py": (
        "aaeff6582d966f873402986445cc370d22fd38606d4f1e7226b4677c03f94655"
    ),
    "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json": (
        "6ee5be1c2b60438043284c26837eef7681c94f95290abee33e52b7cab893e1d3"
    ),
    "cm2_gate34_round26_q1_time2_frontier_cert.py": (
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9"
    ),
    "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json": (
        "9fe21726952e83e121536d2ad6344f586405c5699183f12d210929487190832d"
    ),
    "cm2_standard_section_horizon_lift_cert.py": (
        "ce7215cdf5f37c1bb3cc55747b3ad0dd8ef5f080a661c8a77376984c1c3e62a0"
    ),
    "cm2_gate3_candidate_first_hit_cert.py": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
}
EXPECTED_VERDICT = {
    "dependency_neutral_composed_time2_boundary_tube_decay": "CERTIFIED",
    "limiting_full_physical_R2_Q2_partition_mod_collision_null_set": "CERTIFIED",
    "depth16_strict_R2_inner_admitted_count": "CERTIFIED_0_DEPTH16_ONLY",
    "physical_R2_set_empty": "NOT_CLAIMED",
    "finite_complete_R2_Q2_branch_ledger": "NOT_MATERIALIZED",
    "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
    "survivor_conditioned_recovery": "NOT_CERTIFIED",
    "strong_q_weighted_tail": "NOT_CERTIFIED",
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


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def exact_keys(value: Any, expected: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == expected


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


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


def independent_math_errors(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        require_values = result["composed_fair_boundary_tube_theorem"]
        # Recompute the candidate tangency tube without calling the producer.
        candidate_weight = Q(20108, 625)
        tangent_per_epsilon = Q(176, 7) * candidate_weight
        tangent_h = tangent_per_epsilon * 142
        if tangent_per_epsilon != Q(3539008, 4375):
            errors.append("independent tangent per epsilon")
        if tangent_h != Q(502539136, 4375):
            errors.append("independent tangent h coefficient")
        if tangent_h / 1024 >= 113:
            errors.append("independent tangent threshold")

        weighted_p, weighted_t, radius_sum = (
            Q(546, 3125), Q(39, 625), Q(156, 25)
        )
        linear = 12 * (18 * weighted_p + Q(1, 10) * weighted_t)
        quadratic = 96 * 18 * Q(1, 10) * radius_sum
        effective = linear + quadratic / 1024
        if (linear, quadratic, effective) != (
            Q(23634, 625), Q(134784, 125), Q(194337, 5000)
        ):
            errors.append("independent core face tube")
        if effective >= 39:
            errors.append("independent core threshold")
        if Q(160) / radius_sum != Q(1000, 39):
            errors.append("independent normalization")
        if require_values.get("threshold_h") != "1/1048576":
            errors.append("independent h field")
        if require_values.get("threshold_sqrt_h") != "1/1024":
            errors.append("independent sqrt h field")

        # Recompute obstacle gaps and the non-tangency derivative floor.
        if 1 - 2 * Q(9, 25) != Q(7, 25):
            errors.append("independent G gap")
        if Q(7, 10) - Q(13, 25) != Q(9, 50):
            errors.append("independent mixed gap")
        for radius in (Q(4, 25), Q(9, 25)):
            square = (radius + Q(9, 50)) ** 2 - (Q(17, 16) * radius) ** 2
            if square <= Q(1, 16):
                errors.append("independent tangent derivative floor")
    except Exception as exc:
        errors.append(f"independent math raised: {exc}")
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
        "schema", "provenance", "round26_finite_frontier_context",
        "complete_candidate_and_seam_audit",
        "obstacle_separation_and_root_order_audit",
        "composed_dependency_neutral_derivative_budget",
        "composed_fair_boundary_tube_theorem", "strict_nonpromotion",
        "internal_replay_digest",
    }
    if not exact_keys(result, result_keys):
        errors.append("result key set")
    elif isinstance(result, dict):
        if result.get("schema") != RESULT_SCHEMA:
            errors.append("result schema")
        actual = result_digest(result)
        if result.get("internal_replay_digest") != actual:
            errors.append("internal replay digest")
        if actual != EXPECTED_RESULT_DIGEST:
            errors.append("frozen result digest")

        context = result.get("round26_finite_frontier_context", {})
        if context.get("depth16_strict_R2_inner_admitted_count") != 0:
            errors.append("depth16 R2 count")
        if context.get("zero_R2_count_is_finite_depth_admission_only") is not True:
            errors.append("zero R2 typing")
        if context.get("step1_limiting_R1_Q1_partition_dependency") != "CERTIFIED":
            errors.append("step1 limiting dependency")

        candidate = result.get("complete_candidate_and_seam_audit", {})
        if candidate.get("eight_chart_candidate_entry_count_with_multiplicity") != 448:
            errors.append("candidate count")
        if candidate.get("sum_source_radius_times_target_radius") != "20108/625":
            errors.append("candidate weight")
        if candidate.get("adjacent_chart_union_at_exact_seam") is not True:
            errors.append("seam union")

        separation = result.get("obstacle_separation_and_root_order_audit", {})
        if separation.get("global_distinct_obstacle_boundary_gap_strict_lower") != "9/50":
            errors.append("obstacle gap")
        if separation.get("root_sign_or_order_tie_away_from_tangency") != "IMPOSSIBLE":
            errors.append("root order")

        derivative = result.get("composed_dependency_neutral_derivative_budget", {})
        expected_derivative = {
            "fair_depth_scale": "h_d=2^(-floor(d/3))",
            "second_impact_p_partial_derivative_strict_uppers_t_p_s": [
                "2488", "2825", "432"
            ],
            "exact_second_impact_center_to_box_radius_coefficient": "3501/50",
            "dependency_neutral_second_impact_radius_coefficient": "71",
            "second_root_Holder_radius_coefficient_in_sqrt_h": "6",
            "second_normal_chord_radius_coefficient_in_sqrt_h": "18",
            "natural_interval_dependency_used_for_decay_theorem": False,
        }
        for key, expected in expected_derivative.items():
            if not strict_equal(derivative.get(key), expected):
                errors.append(f"derivative: {key}")

        theorem = result.get("composed_fair_boundary_tube_theorem", {})
        expected_theorem = {
            "fair_absolute_binary_depth_threshold": 60,
            "threshold_h": "1/1048576",
            "threshold_sqrt_h": "1/1024",
            "candidate_tangency_outer_band_halfwidth": "142*h_d",
            "candidate_tangency_unnormalized_mass_coefficient_in_h": (
                "502539136/4375"
            ),
            "candidate_tangency_mass_strict_upper_at_threshold": (
                "113*sqrt(h_d)"
            ),
            "root_sign_and_root_order_resolved_off_tangency_tube": True,
            "time2_core_t_radius_coefficient_in_sqrt_h": "18",
            "time2_core_p_radius_coefficient_in_sqrt_h": "1/10",
            "time2_core_face_tube_linear_coefficient": "23634/625",
            "time2_core_face_tube_quadratic_coefficient": "134784/125",
            "time2_core_face_effective_coefficient_at_threshold": "194337/5000",
            "time2_core_face_mass_strict_upper": "39*sqrt(h_d)",
            "asymptotic_rate": "O(2^(-d/6))",
            "uniform_in_parameter_including_endpoints": True,
            "source_base_density_dominated_by_invariant_collision_density": True,
            "composed_singularity_and_core_face_preimage_collision_measure_zero": True,
            "limiting_full_physical_R2_Q2_partition_mod_collision_null_set": "CERTIFIED",
        }
        for key, expected in expected_theorem.items():
            if not strict_equal(theorem.get(key), expected):
                errors.append(f"theorem: {key}")
        if theorem.get("uniform_parameter_averaged_unresolved_base_mass_bound") != (
            "M_base(U2_d)<160*sqrt(h_d) for every fair frontier with d>=60"
        ):
            errors.append("base mass conclusion")
        if theorem.get("uniform_parameter_averaged_normalized_collision_SRB_bound") != (
            "mu(U2_d)<26*sqrt(h_d) for every fair frontier with d>=60"
        ):
            errors.append("normalized conclusion")

        scope = result.get("strict_nonpromotion", {})
        if scope.get("finite_complete_R2_Q2_branch_ledger") != "NOT_MATERIALIZED":
            errors.append("finite ledger promotion")
        for key in (
            "arbitrary_n_Rn_Qn_partition",
            "numeric_branchwise_mass_Jacobian_distortion_strong_q",
            "survivor_conditioned_recovery", "strong_q_weighted_tail",
            "induced_strong_Lasota_Yorke", "Gate3", "Gate4", "Gate5",
        ):
            if scope.get(key) != "NOT_CERTIFIED":
                errors.append(f"scope overpromotion: {key}")
        if scope.get("CM2") != "NO-GO_FOR_CLAIM":
            errors.append("CM2 scope")
        errors.extend(independent_math_errors(result))

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
    spec = importlib.util.spec_from_file_location("cm2_r27_time2_tube_frozen", CERTIFICATE)
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
    if len(paths) < 80:
        return ["insufficient scalar mutation paths"], attempted
    for path in paths[:80]:
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
    bad = copy.deepcopy(data); bad["unknown"] = 1; structural.append(("unknown", bad))
    bad = copy.deepcopy(data); del bad["result"]["strict_nonpromotion"]; structural.append(("missing", bad))
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
    if attempted != 92:
        failures.append(f"hostile test count changed: {attempted}")
    return failures, attempted


def print_status() -> None:
    print("COMPOSED_TIME2_BOUNDARY_TUBE_DECAY: CERTIFIED")
    print("LIMITING_FULL_PHYSICAL_R2_Q2_MOD_NULL: CERTIFIED")
    print("DEPTH16_R2_ADMITTED_COUNT: 0 (FINITE-DEPTH ONLY)")
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
    print("LIVE_MODE: arbitrary-n partition and strong gates remain open",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
