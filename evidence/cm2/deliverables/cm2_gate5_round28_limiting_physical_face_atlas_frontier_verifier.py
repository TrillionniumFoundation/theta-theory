#!/usr/bin/env python3
"""Fail-closed verifier for the round-28 limiting physical face frontier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
CERTIFICATE = HERE / "cm2_gate5_round28_limiting_physical_face_atlas_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate5.round28-limiting-physical-face-atlas-frontier.manifest.v3"
RESULT_SCHEMA = "cm2.gate5.round28-limiting-physical-face-atlas-frontier.v3"
EXPECTED_CERTIFICATE_SHA256 = "b0dda23ec7e8c9dbe82aff861be6b4e1d38ecf281a82165949537b923150ba27"
EXPECTED_RESULT_DIGEST = "9afd938cdb337136a03119055fa284325376e2d17c6d9267945d0ab1e98996c0"
EXPECTED_DEPENDENCIES = {
    "cm2_gate5_round27_r1_empty_physical_face_join_cert.py": "aabe7f375036e68b742695f27a3a274bc47f594e547579e3592cf97f46989c43",
    "cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json": "9d900f2d0fee5ab8ad1a7e1f999e640ef88edc928ba6208987d1a74c93ca0e38",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "cm2-gate5-round25-r1-field-join-manifest-2026-07-18.json": "f6950d0a6ccf6984f888a102d846557e807becfddf3a95a72565e514934783e4",
    "cm2_gate3_depth_one_fixed_gauge_dq_cert.py": "8ce2490ee2b2bdfc251ac1892cb260e40f3eb5d87ce7f232c2076a10c4a9c066",
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52",
    "cm2_gate34_occurrence_boundary_recovery_carrier_cert.py": "9e69879f921681da4a8eeda9a2af8755c3713151128027784e72cd12896a053a",
    "cm2-gate34-occurrence-boundary-recovery-carrier-manifest-2026-07-17.json": "dd16bd1e3407a6f886ddbf1270ca7ff7289a7d6792e81235f69014cafaf49cb5",
    "cm2_gate34_parameter_dq_all_scale_shell_cert.py": "ea5b6b7fa265990b1eaa1c106e2c0f82f024b58951bbe65ff55757cbc23df458",
    "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json": "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8",
    "cm2-gate3-global-borel-current-assembly-manifest-2026-07-15.json": "dce243c64d4e4fef44a023e8145b22c68233fcce7a8447d83ff86aa0a2d32bdf",
    "cm2-gate34-round26-boundary-tube-decay-manifest-2026-07-18.json": "6ee5be1c2b60438043284c26837eef7681c94f95290abee33e52b7cab893e1d3",
    "cm2-gate34-round27-time2-boundary-tube-manifest-2026-07-18.json": "a6d7c9dad800a7df7aa17b4f94f9bf45363d2839ff3711f35075ea998de07089",
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
}
EXPECTED_VERDICT = {
    "physical_C24_core_faces": "CERTIFIED_96",
    "physical_C24_one_sided_core_traces": "CERTIFIED_192",
    "R1_candidate_core_preimage_face_equation_families": "CERTIFIED_1152",
    "R1_candidate_core_preimage_one_sided_trace_families": "CERTIFIED_2304",
    "moving_occurrence_coarea_DQ_faces": "CERTIFIED_64",
    "moving_occurrence_oriented_hit_miss_traces": "CERTIFIED_128",
    "artificial_dyadic_phase_faces_separated": "CERTIFIED_16864",
    "limiting_R1_complete_physical_face_component_atlas": "NOT_CERTIFIED",
    "limiting_R2_complete_physical_face_component_atlas": "NOT_CERTIFIED",
    "arbitrary_n_face_ID_grammar": (
        "CARRIER_FAMILY_GRAMMAR_ONLY_CONNECTED_RANK_ASSIGNMENT_NOT_CERTIFIED"
    ),
    "F14_through_F18": "NOT_CERTIFIED",
    "R1_candidate_local_maturity": "13/18_UNCHANGED",
    "complete_18_field_operator_blocks": 0,
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
        "schema", "provenance", "physical_C24_core_face_and_trace_registry",
        "R1_regular_core_preimage_face_family_seed_registry",
        "moving_occurrence_coarea_DQ_face_seed_registry",
        "artificial_dyadic_face_separation_registry",
        "strict_inner_R1_certified_empty_F10_F13_family",
        "limiting_R1_face_seed_coverage",
        "R2_and_arbitrary_n_physical_face_ID_grammar_frontier",
        "F14_F18_frontier", "strict_nonpromotion", "internal_replay_digest",
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

        core = result.get("physical_C24_core_face_and_trace_registry", {})
        expected_core = {
            "physical_C24_core_count": 24,
            "materialized_physical_core_face_count": 96,
            "materialized_one_sided_core_trace_count": 192,
            "face_ids_sha256": "7535ed0d98ea07c2c6134997b738f0423e446743ea57e05d60b4613bb2a84465",
            "trace_ids_sha256": "7edd9dcd8644278b8ef80985087188ad6500a5b4f532baeaf4a4c873e2f4f0c1",
            "face_rows_sha256": "a20eac4da1a7895f7139bbfaf950577b4160695b06be103504df20241190374b",
            "zero_parameter_current_not_retyped_as_zero_collision_trace_measure": True,
        }
        for key, expected in expected_core.items():
            if not strict_equal(core.get(key), expected):
                errors.append(f"core registry: {key}")

        r1 = result.get("R1_regular_core_preimage_face_family_seed_registry", {})
        expected_r1 = {
            "regular_source_core_count": 24,
            "obstacle_compatible_destination_core_face_count_per_source": 48,
            "materialized_candidate_R1_core_preimage_equation_family_count": 1152,
            "materialized_candidate_R1_one_sided_trace_family_count": 2304,
            "family_ids_sha256": "feaf1a97c8b746596b5fb46b23a6de59a5d381d0648095b5c14b6d9071905b8b",
            "trace_family_ids_sha256": "fd914176c1d212e07ef80b47cfa19a1ca4151c54dcb8fc7723fa3c55f9f665aa",
            "family_rows_sha256": "743b2078c5d179ade006bc3dd00562f146143429d27291e77982b29b8dc97f19",
            "numeric_coarea_density_bounds_materialized": 0,
            "nonempty_connected_face_component_ids_materialized": 0,
            "candidate_family_id_is_not_face_component_id": True,
        }
        for key, expected in expected_r1.items():
            if not strict_equal(r1.get(key), expected):
                errors.append(f"R1 seed registry: {key}")

        occurrence = result.get("moving_occurrence_coarea_DQ_face_seed_registry", {})
        expected_occurrence = {
            "materialized_physical_moving_occurrence_face_seed_count": 64,
            "materialized_oriented_hit_miss_trace_seed_count": 128,
            "materialized_selected_all_scale_parameter_germ_count": 64,
            "face_ids_sha256": "17dd59a93d8c5fcfca49687b5c6dfe037a037787c55fff3924f71250f95eef21",
            "trace_seed_ids_sha256": "c3607a44db1a8faf5531ef91af7d2b99066ddfa1f004cdf4441d68eedfc8c75a",
            "parameter_germ_ids_sha256": "f778562c298acf4e14ac30c624cefb7761e2d2fe88548fc51bff3e7fd199fced",
            "face_rows_sha256": "18ae7b527eec724fc43fbc70008108e1a50c654b03f7038c76bd832252c56ff3",
            "full_C24_core_occurrence_pair_audit_count": 1536,
            "intersecting_full_C24_core_occurrence_face_pairs": 0,
            "moving_occurrence_faces_are_internal_R1_boundary_faces": False,
        }
        for key, expected in expected_occurrence.items():
            if not strict_equal(occurrence.get(key), expected):
                errors.append(f"occurrence registry: {key}")
        if sum(occurrence.get("full_C24_core_occurrence_pair_reason_histogram", {}).values()) != 1536:
            errors.append("occurrence pair histogram")

        artificial = result.get("artificial_dyadic_face_separation_registry", {})
        expected_artificial = {
            "strict_R1_inner_atom_count": 4216,
            "materialized_artificial_dyadic_phase_face_count": 16864,
            "materialized_artificial_computational_trace_count": 33728,
            "artificial_face_ids_sha256": "c9d3a5b10e1f0f80fcab828caf62ffbfb04619f2c5c032bfc5d25ae03e29e6aa",
            "artificial_trace_ids_sha256": "685036a23fadd4b504dd5db0241ee7a7458ec5bedda92b8918d08332cdaca705",
            "artificial_face_rows_sha256": "bf7b05278725897af08c89d9a9c60c7e63fcdaae5755ba8fcc3c4a1df50b75fc",
            "artificial_faces_used_as_physical_carriers": False,
            "stationary_artificial_speed_used_as_physical_coarea_density": False,
        }
        for key, expected in expected_artificial.items():
            if not strict_equal(artificial.get(key), expected):
                errors.append(f"artificial registry: {key}")

        empty = result.get("strict_inner_R1_certified_empty_F10_F13_family", {})
        if empty.get("R1_inner_atom_count") != 4216:
            errors.append("empty atom count")
        if empty.get("F10_empty_physical_face_slot_count") != 4216:
            errors.append("empty F10")
        if empty.get("F13_empty_physical_current_slot_count") != 4216:
            errors.append("empty F13")
        if empty.get("intersecting_atom_occurrence_pair_count") != 0:
            errors.append("empty intersection")

        coverage = result.get("limiting_R1_face_seed_coverage", {})
        if coverage.get("limiting_R1_Q1_partition_mod_collision_null") != "CERTIFIED":
            errors.append("R1 partition")
        if coverage.get("complete_limiting_R1_physical_coarea_DQ_face_atlas") != "NOT_CERTIFIED":
            errors.append("R1 atlas fail closed")
        if coverage.get("nonempty_connected_face_component_ids_materialized") != 0:
            errors.append("R1 component promotion")

        higher = result.get("R2_and_arbitrary_n_physical_face_ID_grammar_frontier", {})
        kinds = higher.get("boundary_carrier_kind_rows")
        if not isinstance(kinds, list) or len(kinds) != 5:
            errors.append("higher face kinds")
        elif len({row.get("immutable_grammar_id") for row in kinds}) != 5:
            errors.append("higher grammar ids")
        if higher.get("R2_instantiated_face_component_id_count") != 0:
            errors.append("R2 components")
        if higher.get("R2_instantiated_occurrence_pullback_face_component_id_count") != 0:
            errors.append("R2 occurrence pullback components")
        if higher.get("arbitrary_n_instantiated_face_component_id_count") != 0:
            errors.append("Rn components")
        if higher.get("arbitrary_n_instantiated_occurrence_pullback_face_component_id_count") != 0:
            errors.append("Rn occurrence pullback components")
        if higher.get("R2_complete_physical_coarea_DQ_face_atlas") != "NOT_CERTIFIED":
            errors.append("R2 atlas fail closed")
        if higher.get("boundary_carrier_kind_rows_sha256") != "76ded27ba1abc82818af3956e12f7609e224a9a5e5a4d65e2833dc9d4f3656cf":
            errors.append("higher grammar digest")
        if isinstance(kinds, list):
            expected_carriers = {
                "source_core_clipping_face": (
                    "source-core-face-family:(source_core_face_id)",
                    "time_j=0", "inside_or_outside",
                ),
                "intermediate_core_avoidance_preimage_face": (
                    "intermediate-core-preimage-family:(time_j,core_face_id)",
                    "1<=time_j<n", "avoid_or_enter",
                ),
                "terminal_core_preimage_face": (
                    "terminal-core-preimage-family:(time_n,core_face_id)",
                    "time_j=n", "return_or_survive",
                ),
                "collision_singularity_or_owner_change_face": (
                    "collision-boundary-family:(time_j,frozen_step_boundary_key)",
                    "1<=time_j<=n", "left_owner_or_right_owner_or_cemetery",
                ),
                "moving_occurrence_face": (
                    "occurrence-pullback-family:(time_j,occurrence_face_seed_id)",
                    "1<=time_j<=n", "hit_or_miss",
                ),
            }
            by_kind = {row.get("kind"): row for row in kinds}
            if set(by_kind) != set(expected_carriers):
                errors.append("higher carrier kind set")
            common = {
                "instance_face_id_grammar": (
                    "face:(component_id,time_j,carrier_family_or_seed_id,connected_rank)"
                ),
                "instance_trace_id_grammar": (
                    "trace:(component_id,time_j,carrier_family_or_seed_id,"
                    "connected_rank,side_label)"
                ),
                "connected_rank_domain": "N",
                "connected_rank_rule": (
                    "least natural-number index in a fixed bijective enumeration of "
                    "rational dyadic intervals in a canonical 1D carrier parameter "
                    "whose closure is contained in the connected piece"
                ),
                "connected_rank_rule_status": (
                    "NOT_CERTIFIED_BEFORE_CANONICAL_1D_PARAMETERIZATION_AND_PIECE_ENUMERATION"
                ),
                "carrier_family_or_seed_id_is_instance_face_component_id": False,
            }
            for kind, expected in expected_carriers.items():
                row = by_kind.get(kind, {})
                carrier, time_contract, side_contract = expected
                expected_specific = {
                    "carrier_family_id_grammar": carrier,
                    "time_index_contract": time_contract,
                    "side_label_contract": side_contract,
                }
                for key, value in {**common, **expected_specific}.items():
                    if not strict_equal(row.get(key), value):
                        errors.append(f"{kind} grammar: {key}")
            moving = by_kind.get("moving_occurrence_face", {})
            if moving.get("global_seed_id_grammar") != (
                "physical-moving-occurrence-face-seed:(occurrence_id)"
            ):
                errors.append("moving global seed grammar")
            if moving.get("global_seed_is_pullback_component_id") is not False:
                errors.append("moving global seed typing")
        if higher.get("all_five_instance_face_grammars_include_connected_rank") is not True:
            errors.append("all face grammars connected rank")
        if higher.get("all_five_instance_trace_grammars_include_connected_rank") is not True:
            errors.append("all trace grammars connected rank")
        if higher.get("connected_rank_assignment_certified_on_instantiated_faces") is not False:
            errors.append("connected rank promotion")
        if higher.get("grammar_certification_level") != "CARRIER_FAMILY_GRAMMAR_ONLY":
            errors.append("grammar certification level")

        frontier = result.get("F14_F18_frontier", {})
        rows = frontier.get("rows")
        if not isinstance(rows, list) or len(rows) != 5:
            errors.append("F14-F18 rows")
        elif [row.get("index") for row in rows] != [14, 15, 16, 17, 18]:
            errors.append("F14-F18 indices")
        elif any(row.get("materialized_candidate_local_slot_count") != 0 for row in rows):
            errors.append("F14-F18 slots")
        if frontier.get("complete_18_field_operator_block_count") != 0:
            errors.append("complete blocks")
        if frontier.get("global_Gate5_maturity_before_and_after") != "4/18 -> 4/18":
            errors.append("Gate5 maturity frontier")

        strict = result.get("strict_nonpromotion", {})
        expected_strict = {
            "artificial_dyadic_face_used_as_physical_carrier": False,
            "candidate_face_family_id_claimed_as_nonempty_component_id": False,
            "symbolic_DQ_current_claimed_as_numeric_current_bound": False,
            "F14_through_F18_materialized_slot_count": 0,
            "complete_18_field_operator_block_count": 0,
            "R1_candidate_local_maturity": "13/18_UNCHANGED",
            "global_Gate5_maturity": "4/18_UNCHANGED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        for key, expected in expected_strict.items():
            if not strict_equal(strict.get(key), expected):
                errors.append(f"strict nonpromotion: {key}")

    if check_integrity:
        errors.extend(frozen_path_errors())
        if data.get("verifier_sha256") != sha256_path(VERIFIER):
            errors.append("verifier hash field")
    return errors


def load_certificate() -> ModuleType:
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise ValueError("certificate hash before import")
    spec = importlib.util.spec_from_file_location("cm2_round28_face_cert", CERTIFICATE)
    if spec is None or spec.loader is None:
        raise ValueError("certificate import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        certificate = load_certificate()
        replayed = certificate.build_result()
        replayed_verdict = certificate.verdict()
    except Exception as exc:  # fail closed
        return [f"certificate replay exception: {exc}"]
    if not strict_equal(data.get("result"), replayed):
        errors.append("certificate result replay mismatch")
    if not strict_equal(data.get("verdict"), replayed_verdict):
        errors.append("certificate verdict replay mismatch")
    return errors


def scalar_paths(value: Any, path: tuple[Any, ...] = ()) -> Iterable[tuple[Any, ...]]:
    if isinstance(value, dict):
        for key in sorted(value):
            yield from scalar_paths(value[key], path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from scalar_paths(child, path + (index,))
    else:
        yield path


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    parent = value
    for key in path[:-1]:
        parent = parent[key]
    parent[path[-1]] = replacement


def hostile_replacement(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if value is None:
        return "tampered"
    if isinstance(value, str):
        return value + ":tampered"
    return "tampered"


def self_test(data: dict[str, Any]) -> tuple[int, int, list[str]]:
    tests: list[dict[str, Any]] = []

    structural = copy.deepcopy(data)
    structural["schema"] = "tampered"
    tests.append(structural)
    structural = copy.deepcopy(data)
    structural["certificate_sha256"] = "0" * 64
    tests.append(structural)
    structural = copy.deepcopy(data)
    structural["verifier_sha256"] = "0" * 64
    tests.append(structural)
    structural = copy.deepcopy(data)
    structural["dependencies"] = {}
    tests.append(structural)
    structural = copy.deepcopy(data)
    structural["verdict"]["Gate5"] = "CERTIFIED"
    tests.append(structural)
    structural = copy.deepcopy(data)
    structural["verdict"]["global_Gate5_maturity"] = "18/18"
    tests.append(structural)
    structural = copy.deepcopy(data)
    structural.pop("result")
    tests.append(structural)
    structural = copy.deepcopy(data)
    structural["extra"] = True
    tests.append(structural)

    # Eight structural attacks plus 88 distinct leaf attacks: 96 total.
    paths = list(scalar_paths(data["result"]))
    selected = paths[:44] + paths[-44:]
    if len(selected) != 88:
        raise RuntimeError("insufficient scalar leaves for hostile tests")
    for path in selected:
        tampered = copy.deepcopy(data)
        old = tampered["result"]
        for key in path:
            old = old[key]
        set_path(tampered["result"], path, hostile_replacement(old))
        tests.append(tampered)

    failures: list[str] = []
    passed = 0
    for index, tampered in enumerate(tests, start=1):
        if validate(tampered, check_integrity=True):
            passed += 1
        else:
            failures.append(f"hostile mutation accepted: {index}")
    return passed, len(tests), failures


def print_summary() -> None:
    print("PHYSICAL_C24_CORE_FACES: CERTIFIED_96")
    print("R1_CORE_PREIMAGE_FACE_FAMILY_SEEDS: CERTIFIED_1152")
    print("MOVING_OCCURRENCE_COAREA_DQ_FACES: CERTIFIED_64")
    print("ARTIFICIAL_DYADIC_FACES_SEPARATED: CERTIFIED_16864")
    print("LIMITING_R1_R2_COMPLETE_FACE_COMPONENT_ATLAS: NOT_CERTIFIED")
    print("F14_F18: NOT_CERTIFIED")
    print("GLOBAL_GATE5: 4/18_UNCHANGED")
    print("CM2: NO-GO_FOR_CLAIM")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = load_json(args.manifest)
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1

    errors = validate(data, check_integrity=True)
    if args.replay or args.self_test:
        errors.extend(replay(data))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    if args.self_test:
        passed, total, failures = self_test(data)
        if failures:
            for failure in failures:
                print(f"FAIL: {failure}")
            return 1
        print(f"HOSTILE_TESTS: {passed}/{total} PASS")
        return 0
    if args.integrity_only:
        print("INTEGRITY: PASS")
        return 0
    if args.replay:
        print("REPLAY: PASS")
        print_summary()
        return 0

    print_summary()
    return 2


if __name__ == "__main__":
    sys.exit(main())
