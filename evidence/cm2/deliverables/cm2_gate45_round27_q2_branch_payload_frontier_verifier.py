#!/usr/bin/env python3
"""Fail-closed verifier for the round-27 strict-Q2 branch payload leaf."""

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
from typing import Any, Callable


Q = Fraction
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE / "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate45_round27_q2_branch_payload_frontier_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate45.round27-q2-branch-payload-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate45.round27-q2-branch-payload-frontier.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "be96ada6c90e792b7abe556982c65b78dae051498b680ebad3267117f44078c9"
)
EXPECTED_RESULT_DIGEST = (
    "f4ac65999b04719457678205abcd546a3cc90c02d6f85d00ac5da3c9300157ef"
)
EXPECTED_DEPENDENCIES = {
    "cm2_gate34_round26_q1_time2_frontier_cert.py": (
        "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9"
    ),
    "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json": (
        "9fe21726952e83e121536d2ad6344f586405c5699183f12d210929487190832d"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json": (
        "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}
EXPECTED_VERDICT = {
    "Q2_exact_mass_slots": "CERTIFIED_114006",
    "Q2_common_fw_rev_restriction_ids": "CERTIFIED_114006",
    "Q2_two_collision_invariant_area_Jacobians": "CERTIFIED_114006",
    "Q2_symbolic_once_charged_q2": "CERTIFIED_114006",
    "Q2_numeric_strong_q2": "NOT_CERTIFIED",
    "Q2_F5_F6": "NOT_CERTIFIED",
    "Q2_F14_F18": "NOT_CERTIFIED",
    "arbitrary_n_Rn_Qn": "NOT_CERTIFIED",
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
        "schema",
        "provenance",
        "Q2_exact_mass_and_restriction_registry",
        "Q2_invariant_area_Jacobian_registry",
        "Q2_conditional_unstable_payload_template",
        "Q2_symbolic_strong_charge_registry",
        "Q2_F14_F18_frontier",
        "strict_nonpromotion",
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
        for key, expected in {
            "old_artifacts_modified": False,
            "source_registry": "round26 strict Q2-inner depth<=16 admitted atoms",
            "physical_clock": "source core at time0; strict C24 avoidance at times1 and2",
            "replay_engine": "fresh round26 384-bit Arb whole-box geometry",
        }.items():
            if provenance.get(key) != expected or type(provenance.get(key)) is not type(expected):
                errors.append(f"provenance: {key}")

        registry = result.get("Q2_exact_mass_and_restriction_registry", {})
        for key, expected in {
            "strict_Q2_inner_atom_count": 114006,
            "exact_coordinate_base_mass_slot_count": 114006,
            "exact_symbolic_collision_area_mass_slot_count": 114006,
            "parameter_averaged_coordinate_base_mass_exact": "5257799/5120000000",
            "common_forward_reverse_restriction_id_count": 114006,
            "forward_view_id_count": 114006,
            "reverse_view_id_count": 114006,
            "forward_reverse_views_share_one_restriction_and_one_mass": True,
            "target_image_carrier_formula": "B_atom,s=T_s^2(A_atom,s)",
            "restriction_is_smooth_and_invertible_on_each_regular_fixed_s_slice": True,
            "common_strong_recovery_carrier_count": 0,
        }.items():
            if registry.get(key) != expected or type(registry.get(key)) is not type(expected):
                errors.append(f"registry: {key}")
        for key in (
            "mass_ledger_rows_sha256",
            "branch_payload_rows_sha256",
            "source_core_histogram_sha256",
            "collision_word_histogram_sha256",
        ):
            value = registry.get(key)
            if not isinstance(value, str) or len(value) != 64:
                errors.append(f"registry digest: {key}")
        source_histogram = registry.get("source_core_histogram")
        if not isinstance(source_histogram, dict) or sum(source_histogram.values()) != 114006:
            errors.append("source histogram")
        if registry.get("source_core_histogram_sha256") != digest(source_histogram):
            errors.append("source histogram digest")
        if not isinstance(registry.get("distinct_collision_word_count"), int) or registry[
            "distinct_collision_word_count"
        ] <= 0:
            errors.append("collision word count")
        representatives = registry.get("representative_rows")
        if not isinstance(representatives, list) or len(representatives) != 3:
            errors.append("representative rows")
        else:
            for index, row in enumerate(representatives):
                if not isinstance(row, dict):
                    errors.append(f"representative type: {index}")
                    continue
                if row.get("two_collision_invariant_area_Jacobian") != "1":
                    errors.append(f"representative area: {index}")
                if row.get("time1_homogeneity_child_id") is not None:
                    errors.append(f"representative time1 homogeneity: {index}")
                if row.get("time2_homogeneity_child_id") is not None:
                    errors.append(f"representative time2 homogeneity: {index}")
                if row.get("numeric_strong_q2") is not None:
                    errors.append(f"representative q2: {index}")
                for id_key in (
                    "mass_slot_id",
                    "restriction_id",
                    "forward_view_id",
                    "reverse_view_id",
                    "area_Jacobian_slot_id",
                    "conditional_unstable_template_id",
                    "symbolic_q2_charge_id",
                ):
                    value = row.get(id_key)
                    if not isinstance(value, str) or ":" not in value:
                        errors.append(f"representative ID {id_key}: {index}")

        area = result.get("Q2_invariant_area_Jacobian_registry", {})
        for key, expected in {
            "per_collision_area_Jacobian_slot_count": 228012,
            "two_collision_composed_area_Jacobian_slot_count": 114006,
            "per_collision_value": "1",
            "two_collision_composed_value": "1",
            "invariant_measure_type": "collision Birkhoff dr dp at fixed s",
            "adaptive_t_p_coordinate_Jacobian_is_one": False,
            "invariant_area_Jacobian_is_unstable_curve_Jacobian": False,
            "invariant_area_log_distortion_is_F6": False,
        }.items():
            if area.get(key) != expected or type(area.get(key)) is not type(expected):
                errors.append(f"area: {key}")

        template = result.get("Q2_conditional_unstable_payload_template", {})
        for key, expected in {
            "one_step_adapted_unstable_inverse_strict_upper": "144000/180337",
            "conditional_two_step_adapted_unstable_inverse_strict_upper": "20736000000/32521433569",
            "one_step_canonical_recut_log_variation_strict_upper": "3/200000",
            "conditional_two_step_canonical_recut_log_variation_strict_upper": "3/100000",
            "applies_directly_to_unsplit_Q2_atom": False,
            "F5_materialized_slot_count": 0,
            "F6_materialized_slot_count": 0,
        }.items():
            if template.get(key) != expected or type(template.get(key)) is not type(expected):
                errors.append(f"unstable template: {key}")
        try:
            if Q(template["conditional_two_step_adapted_unstable_inverse_strict_upper"]) != Q(
                template["one_step_adapted_unstable_inverse_strict_upper"]
            ) ** 2:
                errors.append("theta composition arithmetic")
            if Q(template["conditional_two_step_canonical_recut_log_variation_strict_upper"]) != 2 * Q(
                template["one_step_canonical_recut_log_variation_strict_upper"]
            ):
                errors.append("distortion composition arithmetic")
        except (KeyError, ValueError, ZeroDivisionError):
            errors.append("template rational parse")

        charge = result.get("Q2_symbolic_strong_charge_registry", {})
        for key, expected in {
            "symbolic_q2_charge_count": 114006,
            "formula": "q2_atom=max(C_fw(atom),C_rev(atom),2)*m2_atom",
            "same_restriction_id_and_exact_mass_used_by_both_views": True,
            "two_views_are_not_two_charges": True,
            "numeric_C_fw_count": 0,
            "numeric_C_rev_count": 0,
            "numeric_q2_count": 0,
            "strong_q2_weighted_mass_sum": "NOT_CERTIFIED",
        }.items():
            if charge.get(key) != expected or type(charge.get(key)) is not type(expected):
                errors.append(f"charge: {key}")

        frontier = result.get("Q2_F14_F18_frontier", {})
        rows = frontier.get("rows")
        if not isinstance(rows, list) or len(rows) != 5:
            errors.append("F14-F18 rows")
        else:
            if [row.get("field_index") for row in rows] != [14, 15, 16, 17, 18]:
                errors.append("F14-F18 indices")
            if any(row.get("materialized_Q2_slot_count") != 0 for row in rows):
                errors.append("F14-F18 nonzero")
            if any(row.get("status") != "NOT_CERTIFIED" for row in rows):
                errors.append("F14-F18 status")
            if frontier.get("rows_sha256") != digest(rows):
                errors.append("F14-F18 digest")
        blocker = frontier.get("first_missing_strong_field_on_the_Q2_candidate_schema", {})
        if blocker.get("field_index") != 2 or blocker.get("field_name") != "physical_homogeneity_subbranch_table":
            errors.append("first strong blocker")

        scope = result.get("strict_nonpromotion", {})
        for key in (
            "complete_limiting_R2_Q2_partition",
            "arbitrary_n_Rn_Qn_partition",
            "strong_q_weighted_tail",
            "induced_strong_Lasota_Yorke",
            "Gate3",
            "Gate4",
            "Gate5",
        ):
            if scope.get(key) != "NOT_CERTIFIED":
                errors.append(f"scope overpromotion: {key}")
        for key in (
            "depth16_R2_admitted_count_zero_means_physical_R2_empty",
            "collision_area_Jacobian_promoted_to_unstable_Jacobian",
            "coordinate_base_mass_promoted_to_exact_collision_SRB_mass",
            "symbolic_q2_promoted_to_numeric_q2",
            "common_Borel_smooth_restriction_promoted_to_common_strong_recovery_carrier",
        ):
            if scope.get(key) is not False:
                errors.append(f"scope boolean: {key}")
        for key in (
            "homogeneity_subbranch_rows_on_Q2_atoms",
            "F5_unstable_Jacobian_slots",
            "F6_unstable_distortion_slots",
            "F14_through_F18_slots",
        ):
            if scope.get(key) != 0 or type(scope.get(key)) is not int:
                errors.append(f"scope zero: {key}")
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
    spec = importlib.util.spec_from_file_location("cm2_r27_q2_payload_frozen", CERTIFICATE)
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


def full_replay(data: dict[str, Any]) -> list[str]:
    try:
        module = load_certificate()
        replayed = module.build_result()
    except Exception as exc:  # fail closed on every replay fault
        return [f"replay exception: {type(exc).__name__}: {exc}"]
    errors: list[str] = []
    if not strict_equal(replayed, data.get("result")):
        errors.append("full result replay mismatch")
    if module.verdict(replayed) != data.get("verdict"):
        errors.append("verdict replay mismatch")
    if replayed.get("internal_replay_digest") != EXPECTED_RESULT_DIGEST:
        errors.append("replay frozen digest")
    return errors


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def mutation_cases() -> list[tuple[str, tuple[Any, ...], Any]]:
    r = ("result",)
    registry = r + ("Q2_exact_mass_and_restriction_registry",)
    area = r + ("Q2_invariant_area_Jacobian_registry",)
    template = r + ("Q2_conditional_unstable_payload_template",)
    charge = r + ("Q2_symbolic_strong_charge_registry",)
    frontier = r + ("Q2_F14_F18_frontier",)
    scope = r + ("strict_nonpromotion",)
    cases: list[tuple[str, tuple[Any, ...], Any]] = [
        ("manifest schema", ("schema",), "bad"),
        ("certificate hash", ("certificate_sha256",), "0" * 64),
        ("dependency", ("dependencies", next(iter(EXPECTED_DEPENDENCIES))), "0" * 64),
        ("verdict mass", ("verdict", "Q2_exact_mass_slots"), "CERTIFIED_1"),
        ("verdict q", ("verdict", "Q2_numeric_strong_q2"), "CERTIFIED"),
        ("verdict F5", ("verdict", "Q2_F5_F6"), "CERTIFIED"),
        ("verdict Gate4", ("verdict", "Gate4"), "CERTIFIED"),
        ("verdict Gate5", ("verdict", "Gate5"), "CERTIFIED"),
        ("verdict CM2", ("verdict", "CM2"), "GO"),
        ("result schema", r + ("schema",), "bad"),
        ("result digest", r + ("internal_replay_digest",), "0" * 64),
        ("provenance deps", r + ("provenance", "dependency_sha256"), {}),
        ("old modified", r + ("provenance", "old_artifacts_modified"), True),
        ("source registry", r + ("provenance", "source_registry"), "cached"),
        ("clock", r + ("provenance", "physical_clock"), "time1"),
        ("engine", r + ("provenance", "replay_engine"), "float"),
        ("Q2 count", registry + ("strict_Q2_inner_atom_count",), 114005),
        ("base slots", registry + ("exact_coordinate_base_mass_slot_count",), 1),
        ("physical slots", registry + ("exact_symbolic_collision_area_mass_slot_count",), 1),
        ("base mass", registry + ("parameter_averaged_coordinate_base_mass_exact",), "1"),
        ("mass digest", registry + ("mass_ledger_rows_sha256",), "0" * 64),
        ("restriction count", registry + ("common_forward_reverse_restriction_id_count",), 1),
        ("fw count", registry + ("forward_view_id_count",), 1),
        ("rev count", registry + ("reverse_view_id_count",), 1),
        ("payload digest", registry + ("branch_payload_rows_sha256",), "0" * 64),
        ("source digest", registry + ("source_core_histogram_sha256",), "0" * 64),
        ("word count", registry + ("distinct_collision_word_count",), 0),
        ("word digest", registry + ("collision_word_histogram_sha256",), "0" * 64),
        ("same restriction", registry + ("forward_reverse_views_share_one_restriction_and_one_mass",), False),
        ("target formula", registry + ("target_image_carrier_formula",), "B=A"),
        ("smooth", registry + ("restriction_is_smooth_and_invertible_on_each_regular_fixed_s_slice",), False),
        ("strong carrier", registry + ("common_strong_recovery_carrier_count",), 1),
        ("area per slots", area + ("per_collision_area_Jacobian_slot_count",), 1),
        ("area composition slots", area + ("two_collision_composed_area_Jacobian_slot_count",), 1),
        ("area one", area + ("per_collision_value",), "2"),
        ("area composed", area + ("two_collision_composed_value",), "2"),
        ("area measure", area + ("invariant_measure_type",), "dt dp"),
        ("tp one", area + ("adaptive_t_p_coordinate_Jacobian_is_one",), True),
        ("area unstable", area + ("invariant_area_Jacobian_is_unstable_curve_Jacobian",), True),
        ("area F6", area + ("invariant_area_log_distortion_is_F6",), True),
        ("theta", template + ("one_step_adapted_unstable_inverse_strict_upper",), "1"),
        ("theta2", template + ("conditional_two_step_adapted_unstable_inverse_strict_upper",), "1"),
        ("variation", template + ("one_step_canonical_recut_log_variation_strict_upper",), "1"),
        ("variation2", template + ("conditional_two_step_canonical_recut_log_variation_strict_upper",), "1"),
        ("template applies", template + ("applies_directly_to_unsplit_Q2_atom",), True),
        ("F5 slot", template + ("F5_materialized_slot_count",), 1),
        ("F6 slot", template + ("F6_materialized_slot_count",), 1),
        ("missing rows", template + ("required_missing_row_fields",), []),
        ("q count", charge + ("symbolic_q2_charge_count",), 1),
        ("q formula", charge + ("formula",), "q2=2m"),
        ("q same", charge + ("same_restriction_id_and_exact_mass_used_by_both_views",), False),
        ("q double", charge + ("two_views_are_not_two_charges",), False),
        ("Cfw", charge + ("numeric_C_fw_count",), 1),
        ("Crev", charge + ("numeric_C_rev_count",), 1),
        ("numeric q", charge + ("numeric_q2_count",), 1),
        ("weighted", charge + ("strong_q2_weighted_mass_sum",), "CERTIFIED"),
        ("F14 slot", frontier + ("rows", 0, "materialized_Q2_slot_count"), 1),
        ("F15 status", frontier + ("rows", 1, "status"), "CERTIFIED"),
        ("F16 index", frontier + ("rows", 2, "field_index"), 99),
        ("F17 reason", frontier + ("rows", 3, "first_missing_dependency"), "none"),
        ("F18 field", frontier + ("rows", 4, "field_name"), "other"),
        ("frontier digest", frontier + ("rows_sha256",), "0" * 64),
        ("frontier count", frontier + ("F14_through_F18_materialized_Q2_slot_count",), 1),
        ("blocker index", frontier + ("first_missing_strong_field_on_the_Q2_candidate_schema", "field_index"), 5),
        ("blocker field", frontier + ("first_missing_strong_field_on_the_Q2_candidate_schema", "field_name"), "inverse_Jacobian_bound"),
        ("complete R2Q2", scope + ("complete_limiting_R2_Q2_partition",), "CERTIFIED"),
        ("R2 empty", scope + ("depth16_R2_admitted_count_zero_means_physical_R2_empty",), True),
        ("arbitrary n", scope + ("arbitrary_n_Rn_Qn_partition",), "CERTIFIED"),
        ("homogeneity rows", scope + ("homogeneity_subbranch_rows_on_Q2_atoms",), 1),
        ("scope F5", scope + ("F5_unstable_Jacobian_slots",), 1),
        ("scope F6", scope + ("F6_unstable_distortion_slots",), 1),
        ("scope F14", scope + ("F14_through_F18_slots",), 1),
        ("promote area", scope + ("collision_area_Jacobian_promoted_to_unstable_Jacobian",), True),
        ("promote base mass", scope + ("coordinate_base_mass_promoted_to_exact_collision_SRB_mass",), True),
        ("promote q", scope + ("symbolic_q2_promoted_to_numeric_q2",), True),
        ("promote carrier", scope + ("common_Borel_smooth_restriction_promoted_to_common_strong_recovery_carrier",), True),
        ("tail", scope + ("strong_q_weighted_tail",), "CERTIFIED"),
        ("LY", scope + ("induced_strong_Lasota_Yorke",), "CERTIFIED"),
        ("scope Gate3", scope + ("Gate3",), "CERTIFIED"),
        ("scope Gate4", scope + ("Gate4",), "CERTIFIED"),
        ("scope Gate5", scope + ("Gate5",), "CERTIFIED"),
        ("scope CM2", scope + ("CM2",), "GO"),
    ]
    return cases


def self_test(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    baseline = validate(data, check_integrity=False)
    if baseline:
        return ["baseline invalid before hostile tests: " + "; ".join(baseline)]
    cases = mutation_cases()
    if len(cases) < 60:
        return ["hostile case count below 60"]
    passed = 0
    for name, path, replacement in cases:
        mutated = copy.deepcopy(data)
        try:
            set_path(mutated, path, replacement)
        except Exception as exc:
            errors.append(f"hostile fixture failure {name}: {exc}")
            continue
        if validate(mutated, check_integrity=False):
            passed += 1
        else:
            errors.append(f"hostile mutation accepted: {name}")
    if passed != len(cases):
        errors.append(f"hostile tests: {passed}/{len(cases)}")
    return errors


def report_errors(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        data = load_json(args.manifest)
    except Exception as exc:
        print(f"FAIL: manifest parse: {type(exc).__name__}: {exc}")
        return 1
    errors = validate(data, check_integrity=True)
    if args.replay:
        errors.extend(full_replay(data))
    if args.self_test:
        errors.extend(self_test(data))
    if report_errors(errors):
        return 1
    print("Q2_BRANCH_PAYLOAD_INTEGRITY: PASS")
    if args.replay:
        print("Q2_BRANCH_PAYLOAD_FULL_384BIT_ARB_REPLAY: PASS")
    if args.self_test:
        print(f"HOSTILE_TESTS: {len(mutation_cases())}/{len(mutation_cases())} PASS")
    if args.integrity_only or args.replay or args.self_test:
        return 0
    print("Q2_EXACT_MASS_COMMON_FW_REV_AREA_JACOBIAN: CERTIFIED_114006")
    print("Q2_NUMERIC_STRONG_Q2_F14_F18: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    sys.exit(main())
