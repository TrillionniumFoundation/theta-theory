#!/usr/bin/env python3
"""Fail-closed verifier for the round-27 arbitrary-n C24 path schema."""

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
    HERE / "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_round27_arbitrary_n_path_schema_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate34.round27-arbitrary-n-path-schema.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.round27-arbitrary-n-path-schema.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "b3071b4af22ad9b4f7941a9896a25cf059e46106c14b1ffb5df0901f90bc3fda"
)
EXPECTED_RESULT_DIGEST = "b5b85bdf4b2fa1380349d6ac04158009e0c1789eb4daaa7495dd4be8634b5609"
EXPECTED_DEPENDENCIES = {
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json": (
        "886c5feb8709ad26fd653e598edf344ba39cc3e08e6efbd02c9ad1133f784c65"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json": (
        "6ee5be1c2b60438043284c26837eef7681c94f95290abee33e52b7cab893e1d3"
    ),
    "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json": (
        "9fe21726952e83e121536d2ad6344f586405c5699183f12d210929487190832d"
    ),
}
EXPECTED_VERDICT = {
    "C24_arbitrary_n_full_dimensional_candidate_path_coverage": (
        "CERTIFIED_MOD_SINGULAR_NULL"
    ),
    "arbitrary_n_Rn_Qn_measurable_level_and_mass_schema": "CERTIFIED",
    "arbitrary_n_regular_connected_component_existence_schema": (
        "CERTIFIED_NONCONSTRUCTIVE"
    ),
    "uniform_unweighted_exponential_Qn_mass_tail": "CERTIFIED",
    "nonempty_component_enumeration_and_numeric_payload": "NOT_CERTIFIED",
    "q_weighted_strong_tail": "NOT_CERTIFIED",
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
    expected_result_keys = {
        "schema", "provenance",
        "C24_full_dimensional_arbitrary_n_candidate_path_join",
        "arbitrary_n_Rn_Qn_level_and_mass_schema",
        "canonical_regular_connected_component_schema",
        "round26_constructive_anchors", "strict_nonpromotion",
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
        if provenance.get("old_artifacts_modified") is not False:
            errors.append("old artifact mutation")
        if provenance.get("parameterwise_not_joint_parameter_component_claim") is not True:
            errors.append("parameter typing")

        join = result.get("C24_full_dimensional_arbitrary_n_candidate_path_join", {})
        expected_join = {
            "source_core_tag_count": 24,
            "regular_collision_step_key_alphabet_size": 441280,
            "depth_n_candidate_universe_size": "24*441280^n",
            "path_universe_over_all_finite_n_is_countable": True,
            "empty_path_fibres_allowed": True,
            "each_regular_orbit_segment_has_at_least_one_recorded_step_key": True,
            "each_regular_collision_step_has_exactly_one_frozen_key_owner": True,
            "candidate_path_fibres_cover_C24_mod_singular_collision_null": True,
            "source_dimension_at_fixed_parameter": 2,
            "positive_area_source_not_occurrence_curve": True,
            "exact_nonempty_candidate_path_keys_enumerated": False,
        }
        for key, expected in expected_join.items():
            if join.get(key) != expected or type(join.get(key)) is not type(expected):
                errors.append(f"path join: {key}")
        rows = join.get("fixed_depth_candidate_count_rows")
        if not isinstance(rows, list) or len(rows) != 9:
            errors.append("candidate count rows")
        else:
            for index, row in enumerate(rows, 1):
                one = 441280**index
                if row.get("n") != index:
                    errors.append(f"candidate row depth: {index}")
                if row.get("one_source_core_candidate_word_count") != str(one):
                    errors.append(f"candidate row one core: {index}")
                if row.get("C24_source_tagged_candidate_word_count") != str(24 * one):
                    errors.append(f"candidate row C24: {index}")

        level = result.get("arbitrary_n_Rn_Qn_level_and_mass_schema", {})
        expected_level = {
            "Q_0": "C_s",
            "level_identity_mod_null": "Q_(n-1)=R_n disjoint_union Q_n",
            "infinite_first_return_partition_mod_null": (
                "C_s=disjoint_union_{n>=1}R_n; intersection_n Q_n has mu_s-mass 0"
            ),
            "N_open": "one_uniform_theorem_supplied_integer>=1_not_numeric",
            "unweighted_exponential_Rn_Qn_mass_ledger": "CERTIFIED_SYMBOLIC",
            "q_weighted_strong_tail": "NOT_CERTIFIED",
        }
        for key, expected in expected_level.items():
            if level.get(key) != expected:
                errors.append(f"level schema: {key}")
        symbolic = level.get("symbolic_physical_mass", {})
        if symbolic.get("numeric_component_masses_materialized") is not False:
            errors.append("numeric mass overclaim")
        if level.get("path_fibre_refinement", {}).get(
            "singular_and_core_boundary_cemetery_mass"
        ) != "0":
            errors.append("cemetery mass")

        component = result.get("canonical_regular_connected_component_schema", {})
        expected_component = {
            "scope": "fixed_parameter_s_and_fixed_finite_n",
            "regular_path_fibre_is_open_relative_to_source_core_interior": True,
            "finite_depth_boundary_collision_SRB_mass": "0",
            "regular_open_fibre_has_at_most_countably_many_connected_components": True,
            "R_n_and_Q_n_regular_component_partition_exists_mod_null": True,
            "componentwise_forward_map_is_real_analytic_local_diffeomorphism": True,
            "componentwise_inverse_map_exists_on_regular_image": True,
            "collision_area_Jacobian_of_full_invertible_map": "1",
            "canonical_component_rank": (
                "least natural-number index in a fixed bijective enumeration of rational "
                "dyadic basis elements whose closure is contained in the component"
            ),
            "canonical_component_id": (
                "c24-component:(source_core_id,n,path_key,least_dyadic_basis_index)"
            ),
            "component_coordinates_and_nonempty_ranks_enumerated": False,
            "uniform_joint_parameter_component_atlas_claimed": False,
            "unstable_Jacobian_or_distortion_inferred_from_area_Jacobian": False,
        }
        for key, expected in expected_component.items():
            if component.get(key) != expected or type(component.get(key)) is not type(expected):
                errors.append(f"component schema: {key}")

        anchors = result.get("round26_constructive_anchors", {})
        expected_anchors = {
            "limiting_step1_R1_Q1_mod_collision_null": "CERTIFIED",
            "step1_fair_boundary_tube_rate": "O(2^(-d/3))",
            "strict_Q2_inner_finite_anchor_count": 114006,
            "strict_Q2_inner_finite_anchor_mass": "5257799/5120000000",
            "time2_unresolved_outer_mass": "106721/204800000",
            "finite_time2_anchor_is_complete_R2_Q2": False,
            "arbitrary_n_schema_does_not_enumerate_missing_time2_components": True,
        }
        for key, expected in expected_anchors.items():
            if anchors.get(key) != expected or type(anchors.get(key)) is not type(expected):
                errors.append(f"anchor: {key}")

        scope = result.get("strict_nonpromotion", {})
        if scope.get("finite_complete_Rn_Qn_raw_branch_table") != "NOT_MATERIALIZED":
            errors.append("raw branch table overclaim")
        for key in (
            "unstable_Jacobian_and_distortion_payload", "common_fw_rev_strong_restriction",
            "strong_q_n_payload", "q_weighted_excursion_cemetery_tail",
            "induced_strong_Lasota_Yorke", "Gate3", "Gate4", "Gate5",
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
    spec = importlib.util.spec_from_file_location("cm2_r27_path_schema_frozen", CERTIFICATE)
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
        actual_verdict = module.verdict()
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
        "duplicate": '{"x":1,"x":2}', "nan": '{"x":NaN}',
        "infinity": '{"x":Infinity}', "negative-infinity": '{"x":-Infinity}',
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
    print("C24_ARBITRARY_N_CANDIDATE_PATH_COVERAGE: CERTIFIED_MOD_SINGULAR_NULL")
    print("ARBITRARY_N_RN_QN_LEVEL_AND_MASS_SCHEMA: CERTIFIED")
    print("REGULAR_COMPONENT_EXISTENCE_SCHEMA: CERTIFIED_NONCONSTRUCTIVE")
    print("NONEMPTY_COMPONENT_ENUMERATION_AND_STRONG_PAYLOAD: NOT_CERTIFIED")
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
    print("LIVE_MODE: numeric components and strong gates remain open", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
