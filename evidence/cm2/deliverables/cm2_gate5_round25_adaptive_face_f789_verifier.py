#!/usr/bin/env python3
"""Fail-closed verifier for the round-25 adaptive-face F7--F9 leaf."""

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
DEFAULT_MANIFEST = HERE / "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json"
CERTIFICATE = HERE / "cm2_gate5_round25_adaptive_face_f789_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate5.round25-adaptive-face-f789.manifest.v1"
RESULT_SCHEMA = "cm2.gate5.round25-adaptive-face-f789.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "d8c4b28ee856927f63bbbb746ea26fd2d7d473b2a3a0009d5c0836fadff3e63a"
)
EXPECTED_RESULT_DIGEST = (
    "7d2273f7c1993fab908deba696c7a4f1ce8b38d1a96f9d82811a1cda7ab4985c"
)
EXPECTED_DEPENDENCIES = {
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json": (
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
    ),
    "cm2-gate25-maximal-word-characteristic-frontier-manifest-2026-07-16.json": (
        "bb09f99519813ec49172f0bbbcc9015c1e0fcb2de07df7af734b81d2996a3f40"
    ),
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json": (
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}
EXPECTED_VERDICT = {
    "R1_inner_adaptive_F7_candidate_local_slots": "CERTIFIED_4216",
    "R1_inner_adaptive_F8_candidate_local_slots": "CERTIFIED_4216",
    "R1_inner_adaptive_F9_candidate_local_slots": "CERTIFIED_4216",
    "R1_candidate_local_maturity_after_companion_join": "9/18",
    "unresolved_outer_next_generation_split_plan": "CERTIFIED_26876",
    "finite_depth_unresolved_outer_exhaustion": "NOT_CERTIFIED",
    "complete_arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
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
        "schema", "provenance", "fixed_s_adaptive_face_theorem",
        "candidate_local_field_templates", "R1_candidate_local_F789_slot_registry",
        "unresolved_outer_next_generation_split_plan",
        "Gate5_candidate_local_maturity_update", "strict_nonpromotion",
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

        theorem = result.get("fixed_s_adaptive_face_theorem", {})
        expected_theorem = {
            "intersection_with_one_atom": "empty_or_one_interval",
            "phase_cut_face_count_per_atom": 4,
            "parameter_guard_faces_cut_fixed_s_phase_curve": False,
            "destination_core_preimage_face_is_redundant_after_strict_whole_box_admission": True,
            "new_artificial_endpoint_upper": 2,
            "unnormalized_Z_multiplier_upper": "2000/1999",
            "normalized_face_transversality_strict_lower": "1/30",
            "individual_coordinate_face_C2_seminorm_upper": "0",
        }
        for key, expected in expected_theorem.items():
            if theorem.get(key) != expected or type(theorem.get(key)) is not type(expected):
                errors.append(f"face theorem: {key}")

        templates = result.get("candidate_local_field_templates", {})
        if not exact_keys(templates, {"F7", "F8", "F9"}):
            errors.append("template key set")
        else:
            if templates["F7"].get("restriction_then_physical_step_strict_upper") != "720269600000/720626832337":
                errors.append("F7 coefficient")
            if templates["F7"].get("restriction_then_physical_step_is_contraction") is not True:
                errors.append("F7 contraction")
            if templates["F8"].get("common_normalized_face_transversality_strict_lower") != "1/30":
                errors.append("F8 transversality")
            if templates["F8"].get("destination_core_preimage_active_face_count") != 0:
                errors.append("F8 destination face count")
            if templates["F9"].get("common_face_C2_seminorm_upper") != "0":
                errors.append("F9 C2")
            if templates["F9"].get("global_coincident_face_assembly_claimed") is not False:
                errors.append("F9 assembly overclaim")

        registry = result.get("R1_candidate_local_F789_slot_registry", {})
        expected_registry = {
            "R1_inner_atom_count": 4216,
            "candidate_local_field_count_added_per_R1_atom": 3,
            "materialized_candidate_local_slot_count": 12648,
            "physical_homogeneity_subbranch_id_count": 4216,
            "R1_depth_histogram": {"13": 304, "14": 2588, "15": 1324},
            "R1_source_core_count": 16,
            "R1_destination_core_count": 16,
            "R1_atom_ids_sha256": "db9fbc97e5528f13d0e330b8905777d1128e9f99a4d4766b1020331efaea5faf",
            "candidate_local_slot_ids_sha256": "76cee6887dcf48a9762a364886c49c725c008d6a17700213e37fd8c3a0f820ee",
            "candidate_local_slot_rows_sha256": "d336aae962cb95d90843ea2bb3585bcffbd00858e4a2f787580d90b50afd6a08",
            "candidate_local_packet_rows_sha256": "7bdfe5e80720c0f1a993cf6cdc33040b97fe3ff98a16d06799154f85468a3f13",
        }
        for key, expected in expected_registry.items():
            if not strict_equal(registry.get(key), expected):
                errors.append(f"slot registry: {key}")
        if not strict_equal(
            registry.get("materialized_candidate_local_slot_count_per_field"),
            {
                "one_step_cut_growth_Z_sum": 4216,
                "face_transversality_lower": 4216,
                "face_C2_atlas_bound": 4216,
            },
        ):
            errors.append("slot per-field counts")
        if not isinstance(registry.get("representative_slot_rows"), list) or len(registry["representative_slot_rows"]) != 3:
            errors.append("representative slots")

        plan = result.get("unresolved_outer_next_generation_split_plan", {})
        expected_plan = {
            "current_unresolved_parent_count": 26876,
            "planned_next_generation_child_count": 53752,
            "current_unresolved_parameter_averaged_base_mass": "44519/256000000",
            "planned_next_generation_base_mass": "44519/256000000",
            "next_split_axis_histogram": {"t": 26876},
            "current_unresolved_depth_histogram": {"12": 6816, "15": 20060},
            "planned_split_record_rows_sha256": "7ab264eef8af4a156c988da008b271d9deb1c89e665d7ba99cbf8f9c63e6767b",
        }
        for key, expected in expected_plan.items():
            if not strict_equal(plan.get(key), expected):
                errors.append(f"split plan: {key}")
        if plan.get("every_planned_split_is_prefix_free_and_mass_conservative_modulo_shared_faces") is not True:
            errors.append("split conservation")
        if not isinstance(plan.get("representative_split_records"), list) or len(plan["representative_split_records"]) != 3:
            errors.append("representative split rows")
        plan_scope = plan.get("strict_nonpromotion", {})
        for key in (
            "numerical_unresolved_mass_decay_rate",
            "finite_depth_exhaustion_of_unresolved_outer_cover",
            "arbitrary_n_Rn_Qn_physical_partition",
        ):
            if plan_scope.get(key) != "NOT_CERTIFIED":
                errors.append(f"split plan overpromotion: {key}")

        maturity = result.get("Gate5_candidate_local_maturity_update", {})
        if maturity.get("candidate_local_R1_maturity_after_exact_companion_join") != "9/18":
            errors.append("candidate maturity")
        if maturity.get("global_Gate5_maturity_before_and_after") != "4/18 -> 4/18":
            errors.append("global maturity")
        if maturity.get("F10_through_F18_slots_materialized") != 0:
            errors.append("F10+ slot count")
        if maturity.get("complete_18_field_R1_operator_block_count") != 0:
            errors.append("complete block count")

        scope = result.get("strict_nonpromotion", {})
        for key in (
            "F7_bound_for_union_of_all_4216_atoms",
            "normalized_conditioned_Z_bound_uniform_in_atom_mass",
            "coincident_face_global_flux_assembly",
            "F10_coarea_density_regular_bound",
            "complete_R1_partition_modulo_null_from_finite_raw_rows",
            "complete_arbitrary_n_Rn_Qn_partition",
            "return_wide_three_CM2_norm_intertwiners",
            "induced_strong_Lasota_Yorke_coefficient",
            "Gate5",
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
    spec = importlib.util.spec_from_file_location("cm2_r25_f789_frozen", CERTIFICATE)
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
    if attempted != 91:
        failures.append(f"hostile test count changed: {attempted}")
    return failures, attempted


def print_status() -> None:
    print("R1_ADAPTIVE_FACE_F7_F8_F9_CANDIDATE_LOCAL_SLOTS: 4216 EACH")
    print("R1_CANDIDATE_LOCAL_MATURITY_AFTER_COMPANION_JOIN: 9/18")
    print("UNRESOLVED_NEXT_GENERATION_SPLIT_PLAN: 26876 -> 53752")
    print("FINITE_UNRESOLVED_EXHAUSTION: NOT_CERTIFIED")
    print("GATE5_GLOBAL_MATURITY: 4/18 (UNCHANGED)")
    print("GATE5: NOT_CERTIFIED")


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
    print("LIVE_MODE: complete R1/Q1 and Gate 5 remain open", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
