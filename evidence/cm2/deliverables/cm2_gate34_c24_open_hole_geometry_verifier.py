#!/usr/bin/env python3
"""Fail-closed verifier for the C24 open-hole geometry certificate."""

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
    HERE / "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_c24_open_hole_geometry_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate34.c24-open-hole-geometry.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.c24-open-hole-geometry.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "651928f514024ad10dd03f30a23307a212cc3cdd462970cc78f39f805b6c858b"
)
EXPECTED_RESULT_DIGEST = (
    "5c5e45e501fc29c3d6d128be604d9e856d521c23d1e1635fbe409fb0a8ac7bd5"
)
EXPECTED_DEPENDENCIES = {
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json": (
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
}
EXPECTED_VERDICT = {
    "C24_normalized_collision_SRB_mass_strict_upper_1_over_2500": "CERTIFIED",
    "C24_O1_O1prime_O2_open_hole_geometry": "CERTIFIED",
    "C24_sparse_opening_cone_recovery_theorem_admission": (
        "CERTIFIED_QUALITATIVE"
    ),
    "C24_every_collision_unweighted_exponential_survivor_tail": (
        "NOT_CERTIFIED"
    ),
    "q_weighted_exponential_excursion_cemetery_tail": "NOT_CERTIFIED",
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
        expected_result_keys = {
            "schema", "provenance", "frozen_core_inventory",
            "collision_SRB_core_mass_interval",
            "stable_curve_open_hole_geometry",
            "sparse_opening_theorem_interface", "strict_scope",
            "internal_replay_digest",
        }
        if not exact_keys(result, expected_result_keys):
            errors.append("result key set")
        if result.get("schema") != RESULT_SCHEMA:
            errors.append("result schema")
        actual_digest = result_digest(result)
        if result.get("internal_replay_digest") != actual_digest:
            errors.append("internal replay digest")
        if actual_digest != EXPECTED_RESULT_DIGEST:
            errors.append("frozen result digest")

        inventory = result.get("frozen_core_inventory")
        if not isinstance(inventory, dict):
            errors.append("inventory type")
        else:
            if type(inventory.get("core_count")) is not int or inventory.get("core_count") != 24:
                errors.append("core count/type")
            if inventory.get("rectangle_count_per_collision_component") != {"G": 12, "W": 12}:
                errors.append("rectangle counts")
            if inventory.get("boundary_edge_count_per_collision_component") != 48:
                errors.append("edge count")

        mass = result.get("collision_SRB_core_mass_interval")
        if not isinstance(mass, dict):
            errors.append("mass type")
        else:
            required_mass = {
                "normalized_core_mass_strict_lower": "147/550000",
                "normalized_core_mass_strict_upper": "29021/75000000",
                "normalized_core_mass_strict_upper_simplification": "1/2500",
                "collision_SRB_unnormalized_strict_upper": "377273/156250000",
            }
            for key, expected in required_mass.items():
                if mass.get(key) != expected:
                    errors.append(f"mass field: {key}")
            if mass.get("normalized_core_mass_at_most_one_half") is not True:
                errors.append("mass half admission")

        geometry = result.get("stable_curve_open_hole_geometry")
        if not isinstance(geometry, dict):
            errors.append("geometry type")
        else:
            if type(geometry.get("O1_complexity_P0")) is not int or geometry.get("O1_complexity_P0") != 49:
                errors.append("O1 P0")
            if type(geometry.get("O1_prime_complexity_P0")) is not int or geometry.get("O1_prime_complexity_P0") != 49:
                errors.append("O1prime P0")
            if type(geometry.get("certified_O2_constant_Ct")) is not int or geometry.get("certified_O2_constant_Ct") != 1493:
                errors.append("O2 Ct")
            if geometry.get("summed_O2_coefficient_strict_upper") != "7464/5":
                errors.append("O2 exact sum")
            if geometry.get("C24_stable_diameter_strict_upper") != "1/20":
                errors.append("stable diameter")

        theorem = result.get("sparse_opening_theorem_interface")
        if not isinstance(theorem, dict):
            errors.append("theorem type")
        else:
            if theorem.get("large_hole_sparse_opening_cone_recovery") != (
                "CERTIFIED_THEOREM_MATCH_WITH_EXISTENTIAL_DELTA_CHI_J_NSTAR"
            ):
                errors.append("sparse theorem match")
            for key in (
                "numeric_delta", "numeric_sparse_block_n_star",
                "numeric_cone_contraction_chi",
            ):
                if theorem.get(key, "missing") is not None:
                    errors.append(f"illegal numeric theorem constant: {key}")
            for key in (
                "stationary_unnormalized_mass_loss_gap",
                "sampled_survivor_exponential_mass_bound",
                "every_collision_survivor_exponential_mass_bound",
            ):
                if theorem.get(key) != "NOT_CERTIFIED":
                    errors.append(f"tail overpromotion: {key}")

        scope = result.get("strict_scope")
        if not isinstance(scope, dict):
            errors.append("scope type")
        else:
            for key in ("Gate3", "Gate4", "Gate5"):
                if scope.get(key) != "NOT_CERTIFIED":
                    errors.append(f"gate overpromotion: {key}")
            if scope.get("unweighted_every_collision_exponential_return_tail") != "NOT_CERTIFIED":
                errors.append("unweighted tail overpromotion")
            if scope.get("q_weighted_exponential_excursion_cemetery_tail") != "NOT_CERTIFIED":
                errors.append("q tail overpromotion")

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
    spec = importlib.util.spec_from_file_location("cm2_c24_open_hole_frozen", CERTIFICATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot create certificate import spec")
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
        module = load_certificate()
        actual = module.certify()
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

    scalar_paths = flatten_scalar_paths(result)
    if len(scalar_paths) < 60:
        return ["insufficient scalar mutation paths"], attempted
    for path in scalar_paths[:60]:
        bad = copy.deepcopy(data)
        parent, key = get_parent(bad["result"], path)
        parent[key] = hostile_value(parent[key])
        bad_result = bad["result"]
        bad_result["internal_replay_digest"] = result_digest(bad_result)
        attempted += 1
        if not validate(bad, check_integrity=True):
            failures.append("coordinated semantic mutation accepted: " + "/".join(map(str, path)))

    structural: list[tuple[str, Any]] = []
    bad = copy.deepcopy(data); bad["schema"] += "!"; structural.append(("schema", bad))
    bad = copy.deepcopy(data); bad["certificate_sha256"] = "0" * 64; structural.append(("certificate", bad))
    bad = copy.deepcopy(data); bad["dependencies"][sorted(EXPECTED_DEPENDENCIES)[0]] = "f" * 64; structural.append(("dependency", bad))
    bad = copy.deepcopy(data); bad["verdict"]["Gate3"] = "CERTIFIED"; structural.append(("gate", bad))
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
    if attempted != 70:
        failures.append(f"hostile test count changed: {attempted}")
    return failures, attempted


def print_status() -> None:
    print("C24_NORMALIZED_COLLISION_SRB_MASS_STRICT_UPPER_1_OVER_2500: CERTIFIED")
    print("C24_OPEN_HOLE_O1_O1PRIME_O2: CERTIFIED")
    print("C24_SPARSE_OPENING_THEOREM_ADMISSION: CERTIFIED_QUALITATIVE")
    print("C24_EVERY_COLLISION_EXPONENTIAL_SURVIVOR_TAIL: NOT_CERTIFIED")
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
    print("LIVE_MODE: unresolved exponential tail and Gates 3/4/5", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
