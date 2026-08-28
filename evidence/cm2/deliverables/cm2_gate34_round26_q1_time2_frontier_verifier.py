#!/usr/bin/env python3
"""Fail-closed verifier for the round-26 Q1-to-time-two frontier leaf."""

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
    HERE / "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_round26_q1_time2_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate34.round26-q1-time2-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.round26-q1-time2-frontier.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9"
)
EXPECTED_RESULT_DIGEST = (
    "8ce5c2ec039fdb847234f925e307b2073539e92b581ba9b0b8524d54af145b6e"
)
EXPECTED_DEPENDENCIES = {
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate3_candidate_first_hit_cert.py": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
    "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json": (
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4"
    ),
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json": (
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
    ),
}
EXPECTED_VERDICT = {
    "strict_R2_inner_atoms": "CERTIFIED_0",
    "strict_Q2_inner_atoms": "CERTIFIED_114006",
    "Q1_time2_mass_conservation": "CERTIFIED",
    "complete_R2_Q2_partition": "NOT_CERTIFIED",
    "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
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
    expected_result_keys = {
        "schema", "provenance", "Q1_time2_adaptive_registry",
        "Q1_time2_mass_frontier", "strict_nonpromotion",
        "internal_replay_digest",
    }
    if not exact_keys(result, expected_result_keys):
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
        if provenance.get("dependency_sha256") != EXPECTED_DEPENDENCIES:
            errors.append("provenance dependencies")
        expected_provenance = {
            "old_artifacts_modified": False,
            "admission_engine": "python-flint Arb",
            "precision_bits": 384,
            "clock": "source_core_time0_then_time1_Q1_then_time2",
            "candidate_search": "complete_translated_eight_chart_retained_table",
        }
        for key, expected in expected_provenance.items():
            if provenance.get(key) != expected or type(provenance.get(key)) is not type(expected):
                errors.append(f"provenance: {key}")

        registry = result.get("Q1_time2_adaptive_registry", {})
        expected_registry = {
            "frozen_Q1_parent_atom_count": 2868,
            "maximum_total_binary_depth": 16,
            "time2_leaf_count": 416994,
            "classification_histogram": {
                "SURVIVE_THROUGH_2_INNER": 114006,
                "UNRESOLVED_TIME2_OUTER": 302988,
            },
            "strict_R2_inner_atom_count": 0,
            "strict_Q2_inner_atom_count": 114006,
        }
        for key, expected in expected_registry.items():
            if not strict_equal(registry.get(key), expected):
                errors.append(f"registry: {key}")
        for key in (
            "time2_leaf_rows_sha256", "time2_atom_ids_sha256",
            "Q1_parent_atom_ids_sha256",
        ):
            value = registry.get(key)
            if not isinstance(value, str) or len(value) != 64:
                errors.append(f"registry digest: {key}")
        if not isinstance(registry.get("depth_histogram"), dict):
            errors.append("depth histogram")
        if not isinstance(registry.get("owner_status_histogram"), dict):
            errors.append("owner status histogram")
        if not isinstance(registry.get("representative_rows"), list) or len(
            registry["representative_rows"]
        ) != 2:
            errors.append("representative rows")

        mass = result.get("Q1_time2_mass_frontier", {})
        expected_mass = {
            "parameter_averaged_Q1_inner_base_mass": "123841/80000000",
            "R2_inner_base_mass": "0",
            "Q2_inner_base_mass": "5257799/5120000000",
            "time2_unresolved_outer_base_mass": "106721/204800000",
            "mass_identity_R2_plus_Q2_plus_unresolved_equals_Q1": True,
            "every_R2_inner_leaf_is_first_return_at_exact_time2": True,
            "every_Q2_inner_leaf_avoids_C24_at_times1_and2": True,
        }
        for key, expected in expected_mass.items():
            if mass.get(key) != expected or type(mass.get(key)) is not type(expected):
                errors.append(f"mass frontier: {key}")

        scope = result.get("strict_nonpromotion", {})
        for key in (
            "complete_R2_Q2_partition", "arbitrary_n_Rn_Qn_partition",
            "q_weighted_return_tail", "induced_strong_Lasota_Yorke",
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
    spec = importlib.util.spec_from_file_location("cm2_r26_q1_time2_frozen", CERTIFICATE)
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
        module = load_certificate()
        actual = module.build_result()
        actual_verdict = module.verdict(actual)
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
    if canonical_json(actual_verdict) != canonical_json(data.get("verdict")):
        errors.append("verdict replay differs")
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
    print("Q1_TIME2_ADAPTIVE_FRONTIER: CERTIFIED")
    print("STRICT_Q2_INNER_ATOMS: 114006")
    print("STRICT_R2_INNER_ATOMS_AT_DEPTH16: 0")
    print("COMPLETE_R2_Q2_PARTITION: NOT_CERTIFIED")
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
    print("LIVE_MODE: arbitrary-n return partition and strong gates remain open", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
