#!/usr/bin/env python3
"""Fail-closed verifier for the round-28 nonempty component registry."""

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
    HERE
    / "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = (
    "cm2.gate34.round28-nonempty-adaptive-component-registry.manifest.v1"
)
RESULT_SCHEMA = "cm2.gate34.round28-nonempty-adaptive-component-registry.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6"
)
EXPECTED_RESULT_DIGEST = (
    "e64742efcc3a8fefd7452e1625d448d97afe794c9f479254addc44f04832c462"
)
EXPECTED_DEPENDENCIES = {
    "cm2_gate5_return_word_three_norm_frontier_cert.py": (
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
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
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json": (
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
    ),
    "cm2_gate34_round26_q1_time2_frontier_cert.py": (
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9"
    ),
    "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json": (
        "9fe21726952e83e121536d2ad6344f586405c5699183f12d210929487190832d"
    ),
    "cm2-gate34-round27-time2-boundary-tube-manifest-2026-07-18.json": (
        "a6d7c9dad800a7df7aa17b4f94f9bf45363d2839ff3711f35075ea998de07089"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json": (
        "f846df9e0afe3e81bedb9cb1a4cb80446d8b79eabb9fd6577e223f6aa1e282ab"
    ),
}
EXPECTED_VERDICT = {
    "R1_inner_nonempty_adaptive_components": "CERTIFIED_4216",
    "Q2_inner_nonempty_depth2_adaptive_components": "CERTIFIED_114006",
    "Q2_inner_anchor_depth2_key_ownership": "CERTIFIED_COMPLETE",
    "finite_anchor_parameter_averaged_coordinate_base_mass_conservation": "CERTIFIED",
    "maximal_path_fibre_component_enumeration": "NOT_CERTIFIED",
    "arbitrary_n_nonempty_component_registry": "NOT_CERTIFIED",
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
        {
            "schema", "certificate_sha256", "verifier_sha256",
            "dependencies", "result", "verdict",
        },
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
        "schema", "provenance", "adaptive_component_contract",
        "R1_nonempty_adaptive_component_registry",
        "Q2_nonempty_adaptive_component_registry",
        "first_remaining_arbitrary_n_blocker", "strict_nonpromotion",
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
        if not strict_equal(provenance.get("dependency_sha256"), EXPECTED_DEPENDENCIES):
            errors.append("provenance dependencies")
        if provenance.get("old_artifacts_modified") is not False:
            errors.append("old artifact mutation")
        if provenance.get("precision_bits") != 384:
            errors.append("precision")
        if provenance.get("full_441280_word_alphabet_replayed") is not True:
            errors.append("word alphabet replay")
        if provenance.get("frozen_word_alphabet_rows_sha256") != (
            "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
        ):
            errors.append("word alphabet digest")

        contract = result.get("adaptive_component_contract", {})
        contract_expected = {
            "fixed_parameter_slice_dimension": 2,
            "maximal_component_of_entire_path_fibre": False,
            "candidate_word_alone_is_a_nonempty_component": False,
            "finite_unresolved_outer_boxes_are_null": False,
        }
        for key, expected in contract_expected.items():
            if contract.get(key) != expected or type(contract.get(key)) is not type(expected):
                errors.append(f"component contract: {key}")
        if contract.get("artificial_t_and_p_dyadic_faces") != (
            "collision-area null on every fixed-s two-dimensional slice"
        ):
            errors.append("t/p face typing")
        s_face = contract.get("artificial_s_endpoint_faces", "")
        if not isinstance(s_face, str) or "exceptional slice s=c" not in s_face:
            errors.append("s face typing")

        r1 = result.get("R1_nonempty_adaptive_component_registry", {})
        r1_expected = {
            "origin_atom_count": 4216,
            "materialized_nonempty_adaptive_component_count": 4216,
            "distinct_frozen_word_key_count": 16,
            "parameter_averaged_coordinate_base_mass_exact": "6473/256000000",
            "parameter_averaged_coordinate_base_mass_sum_equals_frozen_R1_inner_coordinate_base_mass": True,
            "all_origin_dyadic_paths_prefix_free_within_source_core": True,
            "every_registered_cell_has_one_exact_frozen_depth1_word_owner": True,
            "every_registered_cell_is_nonempty_not_merely_a_candidate_word": True,
        }
        for key, expected in r1_expected.items():
            if r1.get(key) != expected or type(r1.get(key)) is not type(expected):
                errors.append(f"R1 registry: {key}")
        if not isinstance(r1.get("representative_rows"), list) or len(
            r1.get("representative_rows", [])
        ) != 3:
            errors.append("R1 representatives")

        q2 = result.get("Q2_nonempty_adaptive_component_registry", {})
        q2_expected = {
            "origin_atom_count": 114006,
            "maximum_additional_wall_recut_binary_depth": 6,
            "terminal_adaptive_cell_count": 114006,
            "materialized_nonempty_depth2_adaptive_component_count": 114006,
            "distinct_depth2_frozen_word_prefix_count": 36,
            "recut_depth_histogram": {"0": 114006},
            "parameter_averaged_admitted_coordinate_base_mass_exact": "5257799/5120000000",
            "finite_wall_unresolved_outer_cell_count": 0,
            "parameter_averaged_finite_wall_unresolved_outer_coordinate_base_mass_exact": "0",
            "finite_wall_first_blocker_histogram": {},
            "parameter_averaged_admitted_plus_unresolved_equals_frozen_Q2_inner_coordinate_base_mass": True,
            "every_registered_cell_has_one_exact_frozen_depth2_word_prefix_owner": True,
            "every_registered_cell_is_nonempty_not_merely_a_candidate_word": True,
            "complete_frozen_Q2_inner_anchor_depth2_key_ownership": True,
            "finite_unresolved_outer_boxes_promoted_to_collision_null": False,
        }
        for key, expected in q2_expected.items():
            if not strict_equal(q2.get(key), expected):
                errors.append(f"Q2 registry: {key}")
        if not isinstance(q2.get("representative_rows"), list) or len(
            q2.get("representative_rows", [])
        ) != 3:
            errors.append("Q2 representatives")
        if q2.get("unresolved_representative_rows") != []:
            errors.append("Q2 unresolved representatives")
        representatives = list(r1.get("representative_rows", [])) + list(
            q2.get("representative_rows", [])
        )
        for index, row in enumerate(representatives):
            if "coordinate_base_mass_exact_rational" in row:
                errors.append(f"untyped coordinate mass field {index}")
            if not isinstance(
                row.get("parameter_averaged_coordinate_base_mass_exact_rational"), str
            ):
                errors.append(f"parameter-averaged coordinate mass {index}")
            if row.get("parameter_averaged_coordinate_base_measure_type") != (
                "R_source*dt*dp times normalized ds/parameter_window_width"
            ):
                errors.append(f"parameter-averaged coordinate mass type {index}")
            if row.get("parameter_averaged_coordinate_base_mass_formula") != (
                "R_source*(t1-t0)*(p1-p0)*(s1-s0)/(1/200)"
            ):
                errors.append(f"parameter-averaged coordinate mass formula {index}")
            typed = {
                "t_and_p_dyadic_faces_collision_area_null_on_every_fixed_s_slice": True,
                "s_endpoint_faces_parameter_averaged_product_null": True,
                "s_endpoint_face_collision_area_null_on_exceptional_slice_s_equals_endpoint_claimed": False,
                "fixed_s_slice_claim_includes_cell_s_endpoints": False,
            }
            for key, expected in typed.items():
                if row.get(key) is not expected:
                    errors.append(f"representative face typing {index}: {key}")

        blocker = result.get("first_remaining_arbitrary_n_blocker", {})
        if blocker.get(
            "first_unmaterialized_extension_depth_from_certified_Q2_inner_anchors"
        ) != 3:
            errors.append("first unmaterialized extension depth")
        if blocker.get("Q1_nonempty_component_registry_materialized_by_this_leaf") is not False:
            errors.append("Q1 materialization overclaim")
        if blocker.get("limiting_physical_R2_component_enumeration_materialized") is not False:
            errors.append("limiting R2 materialization overclaim")
        if blocker.get("depth16_R2_admitted_zero_implies_physical_R2_empty") is not False:
            errors.append("finite R2 empty overclaim")
        if blocker.get("maximal_path_fibre_component_merging_also_open") is not True:
            errors.append("maximal component blocker")

        scope = result.get("strict_nonpromotion", {})
        for key in (
            "complete_limiting_R1_component_enumeration",
            "Q1_nonempty_component_registry",
            "limiting_physical_R2_component_enumeration",
            "complete_limiting_R2_Q2_component_enumeration",
            "arbitrary_n_nonempty_component_registry",
            "maximal_connected_path_fibre_components",
            "homogeneity_child_and_canonical_recut_registry",
            "numeric_unstable_Jacobian_and_distortion",
            "strong_q_weighted_tail",
            "induced_strong_Lasota_Yorke",
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
    spec = importlib.util.spec_from_file_location("cm2_r28_components_frozen", CERTIFICATE)
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
    if attempted != 92:
        failures.append(f"hostile test count changed: {attempted}")
    return failures, attempted


def print_status() -> None:
    print("R1_NONEMPTY_ADAPTIVE_COMPONENTS: CERTIFIED_4216")
    print("Q2_NONEMPTY_DEPTH2_ADAPTIVE_COMPONENTS: CERTIFIED_114006")
    print("Q2_FINITE_ANCHOR_DEPTH2_KEY_OWNERSHIP: CERTIFIED_COMPLETE")
    print("ARBITRARY_N_NONEMPTY_COMPONENT_REGISTRY: NOT_CERTIFIED")
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
    print("LIVE_MODE: arbitrary-n and strong gates remain open", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
