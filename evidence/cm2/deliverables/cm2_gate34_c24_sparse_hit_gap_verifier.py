#!/usr/bin/env python3
"""Fail-closed verifier for the C24 sparse hit-gap and return-tail leaf."""

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
DEFAULT_MANIFEST = HERE / "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json"
CERTIFICATE = HERE / "cm2_gate34_c24_sparse_hit_gap_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate34.c24-sparse-hit-gap.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.c24-sparse-hit-gap.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "60b66c7ca5b52ec7061743d320a7b6027ed805b1a40831dab1f695e54f745a2c"
)
EXPECTED_RESULT_DIGEST = (
    "100681e630039cc58e86cb156ac17ecf7921163576b67211bb0e2a713ca8d1c1"
)
EXPECTED_DEPENDENCIES = {
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
}
EXPECTED_VERDICT = {
    "C24_recovered_cone_hit_gap_21_over_111718750": "CERTIFIED",
    "C24_uniform_unweighted_exponential_return_tail": "CERTIFIED",
    "C24_numeric_sparse_block_length_and_numeric_collision_rho": (
        "NOT_CERTIFIED"
    ),
    "q_weighted_exponential_excursion_cemetery_tail": "NOT_CERTIFIED",
    "full_2d_branch_materialized_Rn_Qn_partition": "NOT_CERTIFIED",
    "induced_common_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
    "Gate3": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED",
    "Gate5": "NOT_CERTIFIED",
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
    top_keys = {
        "schema", "certificate_sha256", "verifier_sha256", "dependencies",
        "result", "verdict",
    }
    if not exact_keys(data, top_keys):
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
    if not isinstance(result, dict):
        errors.append("result type")
    else:
        result_keys = {
            "schema", "provenance", "explicit_C1_bump",
            "uniform_recovered_cone_hit_gap", "scheduled_and_all_time_tail",
            "strict_scope", "internal_replay_digest",
        }
        if not exact_keys(result, result_keys):
            errors.append("result key set")
        if result.get("schema") != RESULT_SCHEMA:
            errors.append("result schema")
        actual_digest = result_digest(result)
        if result.get("internal_replay_digest") != actual_digest:
            errors.append("internal replay digest")
        if actual_digest != EXPECTED_RESULT_DIGEST:
            errors.append("frozen result digest")

        bump = result.get("explicit_C1_bump")
        if not isinstance(bump, dict):
            errors.append("bump type")
        else:
            expected_bump = {
                "normalized_collision_SRB_integral_strict_lower": "21/55859375",
                "unnormalized_collision_SRB_integral_strict_lower": "24/9765625",
                "one_dimensional_polynomial_integral": "16/15",
                "C1_norm_strict_upper": "2724",
                "pointwise_bounds": "0<=g<=1_C24<=1",
            }
            for key, expected in expected_bump.items():
                if bump.get(key) != expected:
                    errors.append(f"bump field: {key}")
            for key in (
                "support_closure_strictly_inside_one_C24_core",
                "boundary_value_and_first_derivative_zero",
                "global_C1_on_collision_section",
                "same_bump_and_integral_bound_for_every_|s|<=1/400",
            ):
                if bump.get(key) is not True:
                    errors.append(f"bump boolean/type: {key}")

        gap = result.get("uniform_recovered_cone_hit_gap")
        if not isinstance(gap, dict):
            errors.append("hit gap type")
        else:
            if gap.get("explicit_per_block_hit_gap_epsilon") != "21/111718750":
                errors.append("hit epsilon")
            if gap.get("explicit_per_block_survival_factor") != "111718729/111718750":
                errors.append("block factor")
            if gap.get("next_pre_hole_C24_mass_strict_lower") != "21/111718750":
                errors.append("next C24 hit")
            if gap.get("numeric_N_open", "missing") is not None:
                errors.append("numeric N overclaim")
            if gap.get("all_theorem_constants_uniform_over_compact_s_family") is not True:
                errors.append("uniform theorem constants")
            if gap.get("uniform_parameter_quantifier") != "one_N_open_for_all_|s|<=1/400":
                errors.append("uniform N quantifier")

        tail = result.get("scheduled_and_all_time_tail")
        if not isinstance(tail, dict):
            errors.append("tail type")
        else:
            if tail.get("uniform_unweighted_exponential_collision_return_tail") != "CERTIFIED":
                errors.append("unweighted tail")
            exponential = tail.get("collision_time_exponential_form")
            if not isinstance(exponential, dict):
                errors.append("exponential form type")
            else:
                if exponential.get("rho_open") != "(111718729/111718750)^(1/N_open)":
                    errors.append("rho formula")
                if exponential.get("rho_open_strictly_between_zero_and_one") is not True:
                    errors.append("rho interval")
                if exponential.get("A_open_rational_strict_upper") != "61445312500000/16422653163":
                    errors.append("A prefactor")
            if tail.get("block_length_is_theorem_supplied_not_numerically_materialized") is not True:
                errors.append("block typing")

        scope = result.get("strict_scope")
        if not isinstance(scope, dict):
            errors.append("scope type")
        else:
            if scope.get("C24_uniform_unweighted_exponential_return_tail") != "CERTIFIED":
                errors.append("scope tail")
            for key in (
                "C24_numeric_sparse_block_length",
                "C24_numeric_collision_time_rho",
                "q_weighted_exponential_excursion_cemetery_tail",
                "branch_materialized_2d_Rn_Qn_partition",
                "branch_Jacobian_distortion_mass_q_payload",
                "induced_common_strong_Lasota_Yorke_coefficient",
                "common_fw_rev_strong_restriction",
                "Gate3", "Gate4", "Gate5",
            ):
                if scope.get(key) != "NOT_CERTIFIED":
                    errors.append(f"scope overpromotion: {key}")
            if type(scope.get("complete_18_field_operator_blocks")) is not int or scope.get("complete_18_field_operator_blocks") != 0:
                errors.append("complete block count/type")

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
    spec = importlib.util.spec_from_file_location("cm2_c24_sparse_hit_frozen", CERTIFICATE)
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
        return 1 if value else True
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
    bad = copy.deepcopy(data); bad["dependencies"][sorted(EXPECTED_DEPENDENCIES)[0]] = "f" * 64; structural.append(("dependency", bad))
    bad = copy.deepcopy(data); bad["verdict"]["Gate4"] = "CERTIFIED"; structural.append(("gate", bad))
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
    if attempted != 74:
        failures.append(f"hostile test count changed: {attempted}")
    return failures, attempted


def print_status() -> None:
    print("C24_RECOVERED_CONE_HIT_GAP_21_OVER_111718750: CERTIFIED")
    print("C24_UNIFORM_UNWEIGHTED_EXPONENTIAL_RETURN_TAIL: CERTIFIED")
    print("C24_NUMERIC_SPARSE_BLOCK_AND_NUMERIC_RHO: NOT_CERTIFIED")
    print("C24_Q_WEIGHTED_EXPONENTIAL_TAIL: NOT_CERTIFIED")
    print("GATE3_GATE4_GATE5: NOT_CERTIFIED")


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
    print("LIVE_MODE: q-weighted strong tail and Gates 3/4/5 remain open", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
