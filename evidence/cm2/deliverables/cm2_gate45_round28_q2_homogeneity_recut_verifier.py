#!/usr/bin/env python3
"""Fail-closed verifier for the round-28 Q2 homogeneity/recut leaf."""

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
    HERE / "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate45_round28_q2_homogeneity_recut_cert.py"
VERIFIER = Path(__file__).resolve()
MANIFEST_SCHEMA = "cm2.gate45.round28-q2-homogeneity-recut.manifest.v1"
RESULT_SCHEMA = "cm2.gate45.round28-q2-homogeneity-recut.v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "1acf1072caa22b676ed7f579cd2a909f06c6b8249396a7be4cdaa9c37997cf64"
)
EXPECTED_RESULT_DIGEST = (
    "97032e1446a6ba94e3fc81847a22a0c03dd1069ec7184ec0ccb4626c51012005"
)
EXPECTED_DEPENDENCIES = {
    "cm2_gate45_round27_q2_branch_payload_frontier_cert.py": (
        "be96ada6c90e792b7abe556982c65b78dae051498b680ebad3267117f44078c9"
    ),
    "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json": (
        "f846df9e0afe3e81bedb9cb1a4cb80446d8b79eabb9fd6577e223f6aa1e282ab"
    ),
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
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json": (
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691"
    ),
    "cm2_gate4_componentwise_global_growth_recovery_frontier_cert.py": (
        "90b7f7a9c0f02c19a80a9679ff393818318675c378ff4c1f139985ae23f069e1"
    ),
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json": (
        "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b"
    ),
    "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json": (
        "6b9354026a1707a25971925e02acbb5ea7e459ca177190a28ff1b39857283d86"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}
EXPECTED_VERDICT = {
    "Q2_two_step_physical_homogeneity_children": "CERTIFIED_114006",
    "Q2_canonical_recut_branch_rule_ids": "CERTIFIED_228012",
    "Q2_actual_curve_recut_instance_ids_materialized": 0,
    "Q2_numeric_F5_slots": "CERTIFIED_114006_UNIVERSAL_BRANCH_RULE_SLOTS",
    "Q2_numeric_F6_slots": "CERTIFIED_114006_UNIVERSAL_BRANCH_RULE_SLOTS",
    "Q2_numeric_strong_q2": "NOT_CERTIFIED",
    "Q2_F7_F14_F18": "NOT_CERTIFIED",
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


def is_digest(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


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
        "full_time2_Arb_replay",
        "Q2_two_step_homogeneity_and_recut_registry",
        "Q2_numeric_F5_F6_slot_registry",
        "strong_type_separation",
        "downstream_frontier",
        "strict_nonpromotion",
        "internal_replay_digest",
    }
    if not exact_keys(result, expected_result_keys):
        errors.append("result key set")
    elif isinstance(result, dict):
        if result.get("schema") != RESULT_SCHEMA:
            errors.append("result schema")
        actual = result_digest(result)
        if result.get("internal_replay_digest") != actual:
            errors.append("internal replay digest")
        if actual != EXPECTED_RESULT_DIGEST:
            errors.append("frozen result digest")

        provenance = result.get("provenance", {})
        if not strict_equal(provenance.get("dependency_sha256"), EXPECTED_DEPENDENCIES):
            errors.append("provenance dependencies")
        for key, expected in {
            "old_artifacts_modified": False,
            "source_registry": "round26 strict Q2-inner depth<=16 admitted atoms",
            "replay_engine": "fresh 384-bit Arb full adaptive geometry with retained collision states",
            "canonical_recut_policy": "deterministic adapted-arclength branch rules producing cells of length at most 1e-90",
        }.items():
            if provenance.get(key) != expected or type(provenance.get(key)) is not type(expected):
                errors.append(f"provenance: {key}")

        replay = result.get("full_time2_Arb_replay", {})
        for key, expected in {
            "precision_bits": 384,
            "Q1_parent_count": 2868,
            "terminal_leaf_count": 416994,
            "classification_histogram": {
                "SURVIVE_THROUGH_2_INNER": 114006,
                "UNRESOLVED_TIME2_OUTER": 302988,
            },
            "owner_status_histogram": {
                "strict_unique_second_collision_owner": 130794,
                "unresolved_competitor:unresolved_discriminant": 272840,
                "unresolved_time1_outgoing_chart_or_geometry": 13360,
            },
            "terminal_atom_ids_sha256": "30a8922a3763e3f8d6e049a744a2d41d82103c2b73b97c118c5c58b558d63aaf",
            "strict_Q2_atom_count": 114006,
            "Q2_coordinate_base_mass_exact": "5257799/5120000000",
            "unresolved_coordinate_base_mass_exact": "106721/204800000",
            "finite_depth_R2_admitted_count": 0,
        }.items():
            if replay.get(key) != expected or type(replay.get(key)) is not type(expected):
                errors.append(f"replay: {key}")
        depth = replay.get("depth_histogram")
        if not isinstance(depth, dict) or sum(depth.values()) != 416994:
            errors.append("replay depth histogram")
        if not is_digest(replay.get("strict_Q2_atom_ids_sha256")):
            errors.append("Q2 IDs digest")

        registry = result.get("Q2_two_step_homogeneity_and_recut_registry", {})
        for key, expected in {
            "homogeneity_cutoff_k0": 6121,
            "central_H0_target_cosine_strict_lower": "1/74933282",
            "strict_Q2_atom_count": 114006,
            "fully_materialized_Q2_atom_count": 114006,
            "blocked_Q2_atom_count": 0,
            "blocker_histogram": {},
            "first_blocker": None,
            "fresh_step1_parent_core_owner_replay_count": 24,
            "fresh_step2_unique_owner_Q2_count": 114006,
            "time1_physical_homogeneity_child_id_count": 114006,
            "time2_physical_homogeneity_child_id_count": 114006,
            "two_step_homogeneous_child_id_count": 114006,
            "canonical_recut_branch_rule_id_count": 228012,
            "canonical_recut_branch_rules_per_materialized_Q2_atom": 2,
            "actual_curve_recut_instance_id_count": 0,
            "actual_curve_recut_instance_id_schema": "recut-instance:(branch-rule-id):(parent-W-id):natural-index-j",
            "branch_rule_ids_are_actual_curve_instance_ids": False,
            "whole_atom_crosses_physical_homogeneity_boundary_count": 0,
            "strict_single_time2_target_chart_Q2_atom_count": 108726,
            "time2_target_chart_seam_not_strictly_excluded_Q2_atom_count": 5280,
            "chart_seams_are_representation_boundaries_not_physical_cuts": True,
            "chart_free_physical_homogeneity_recut_used_for_F5_F6": True,
        }.items():
            if registry.get(key) != expected or type(registry.get(key)) is not type(expected):
                errors.append(f"registry: {key}")
        chart1 = registry.get("time1_target_chart_histogram")
        if not isinstance(chart1, dict) or sum(chart1.values()) != 114006:
            errors.append("time1 chart histogram")
        elif {
            chart: sum(value for key, value in chart1.items() if key.endswith(":" + chart))
            for chart in ("E", "N", "S", "W")
        } != {"E": 26757, "N": 30246, "S": 30246, "W": 26757}:
            errors.append("time1 chart suffix histogram")
        # The exact obstacle-prefixed time-two chart histogram is checked by
        # its total and the frozen seam frontier; replay freezes its digest.
        chart2 = registry.get("time2_target_chart_histogram")
        if not isinstance(chart2, dict) or sum(chart2.values()) != 114006:
            errors.append("time2 chart histogram")
        if isinstance(chart2, dict) and chart2.get("UNRESOLVED_REPRESENTATION_SEAM") != 5280:
            errors.append("time2 chart seam histogram")
        for key in (
            "collision_target_word_histogram_sha256",
            "full_Q2_geometry_audit_rows_sha256",
            "materialized_payload_rows_sha256",
        ):
            if not is_digest(registry.get(key)):
                errors.append(f"registry digest: {key}")
        reps = registry.get("representative_materialized_rows")
        if not isinstance(reps, list) or len(reps) != 3:
            errors.append("representatives")
        else:
            for index, row in enumerate(reps):
                if row.get("F5_two_step_adapted_inverse_strict_upper") != "20736000000/32521433569":
                    errors.append(f"representative F5: {index}")
                if row.get("F6_two_step_log_variation_strict_upper") != "3/100000":
                    errors.append(f"representative F6: {index}")
                if row.get("numeric_strong_q2") is not None:
                    errors.append(f"representative q2: {index}")
                for id_key in (
                    "restriction_id", "mass_slot_id", "area_Jacobian_slot_id",
                    "time1_physical_homogeneity_child_id",
                    "time2_physical_homogeneity_child_id",
                    "two_step_homogeneous_child_id", "F5_numeric_slot_id", "F6_numeric_slot_id",
                ):
                    if not isinstance(row.get(id_key), str) or ":" not in row[id_key]:
                        errors.append(f"representative ID {id_key}: {index}")
                if not isinstance(row.get("canonical_recut_branch_rule_ids"), list) or len(row["canonical_recut_branch_rule_ids"]) != 2:
                    errors.append(f"representative recut: {index}")

        slots = result.get("Q2_numeric_F5_F6_slot_registry", {})
        for key, expected in {
            "materialized_two_step_homogeneous_child_count": 114006,
            "F5_universal_branch_rule_slot_count": 114006,
            "F6_universal_branch_rule_slot_count": 114006,
            "actual_curve_instance_slot_count": 0,
            "universal_quantifier": "for every actual canonical standard-curve recut instance generated by the two branch rules on this 2D Q2 branch",
            "slot_counts_are_actual_curve_instance_counts": False,
            "one_step_adapted_unstable_inverse_strict_upper": "144000/180337",
            "two_step_adapted_unstable_inverse_strict_upper": "20736000000/32521433569",
            "one_step_canonical_recut_log_variation_strict_upper": "3/200000",
            "two_step_canonical_recut_log_variation_strict_upper": "3/100000",
            "literal_prior_canonical_recut_component_field_filled": False,
            "literal_prior_conditional_template_join": "NOT_CERTIFIED",
            "universal_template_reinstantiated_as_branch_rule_theorem": True,
            "unsplit_Q2_atom_given_one_global_unstable_Jacobian_value": False,
        }.items():
            if slots.get(key) != expected or type(slots.get(key)) is not type(expected):
                errors.append(f"slots: {key}")
        try:
            if Q(slots["two_step_adapted_unstable_inverse_strict_upper"]) != Q(
                slots["one_step_adapted_unstable_inverse_strict_upper"]
            ) ** 2:
                errors.append("F5 composition arithmetic")
            if Q(slots["two_step_canonical_recut_log_variation_strict_upper"]) != 2 * Q(
                slots["one_step_canonical_recut_log_variation_strict_upper"]
            ):
                errors.append("F6 composition arithmetic")
        except (KeyError, ValueError, ZeroDivisionError):
            errors.append("slot rational parse")
        for key in (
            "F5_universal_branch_rule_slot_ids_sha256",
            "F6_universal_branch_rule_slot_ids_sha256",
            "homogeneity_child_ids_sha256",
            "canonical_recut_branch_rule_ids_sha256",
        ):
            if not is_digest(slots.get(key)):
                errors.append(f"slot digest: {key}")
        if not isinstance(slots.get("prior_conditional_template_reference_id"), str) or not slots[
            "prior_conditional_template_reference_id"
        ].startswith("template:q2:conditional-unstable:"):
            errors.append("prior template ID")

        typed = result.get("strong_type_separation", {})
        for key, expected in {
            "joined_prior_restriction_id_count": 114006,
            "joined_prior_coordinate_and_collision_mass_slot_count": 114006,
            "joined_prior_invariant_area_Jacobian_slot_count": 114006,
            "coordinate_base_mass_is_exact_collision_area_mass": False,
            "invariant_area_Jacobian_is_adaptive_coordinate_Jacobian": False,
            "invariant_area_Jacobian_is_unstable_one_dimensional_Jacobian": False,
            "invariant_area_log_distortion_is_F6": False,
            "F5_F6_use_only_the_frozen_universal_unstable_template_and_physical_homogeneity_recut_branch_rule_ids": True,
            "numeric_C_fw_count": 0,
            "numeric_C_rev_count": 0,
            "numeric_strong_q2_count": 0,
        }.items():
            if typed.get(key) != expected or type(typed.get(key)) is not type(expected):
                errors.append(f"typed: {key}")

        frontier = result.get("downstream_frontier", {})
        rows = frontier.get("rows")
        if not isinstance(rows, list) or [row.get("field_index") for row in rows] != [4, 7, 14, 15, 16, 17, 18]:
            errors.append("frontier rows")
        elif any(row.get("materialized_Q2_slot_count") != 0 or row.get("status") != "NOT_CERTIFIED" for row in rows):
            errors.append("frontier promotion")
        if frontier.get("rows_sha256") != digest(rows):
            errors.append("frontier rows digest")
        for key, expected in {
            "F4_strict_single_time2_chart_slot_count": 108726,
            "F7_materialized_Q2_slot_count": 0,
            "F14_through_F18_materialized_Q2_slot_count": 0,
        }.items():
            if frontier.get(key) != expected:
                errors.append(f"frontier: {key}")
        blocker = frontier.get("first_unfillable_field_on_the_full_Q2_chart_ledger", {})
        if blocker.get("field_index") != 4 or blocker.get("field_name") != "homogeneous_suffix_chart":
            errors.append("first full-chart blocker")

        scope = result.get("strict_nonpromotion", {})
        for key in (
            "arbitrary_n_component_registry", "F7_characteristic_cut_growth", "F14_through_F18",
            "numeric_strong_q2", "survivor_conditioned_recovery",
            "strong_q_weighted_excursion_cemetery_tail", "induced_strong_Lasota_Yorke",
            "Gate4", "Gate5",
        ):
            if scope.get(key) != "NOT_CERTIFIED":
                errors.append(f"scope overpromotion: {key}")
        for key in (
            "finite_depth_R2_admitted_zero_means_physical_R2_empty",
            "complete_limiting_R2_Q2_partition_reproved_here",
        ):
            if scope.get(key) is not False:
                errors.append(f"scope boolean: {key}")
        if scope.get("CM2") != "NO-GO_FOR_CLAIM":
            errors.append("CM2 scope")

    if check_integrity:
        errors.extend(frozen_path_errors())
        if data.get("verifier_sha256") != sha256_path(VERIFIER):
            errors.append("verifier hash")
    return errors


def load_certificate() -> ModuleType:
    if sys.flags.optimize != 0:
        raise RuntimeError("optimized Python is forbidden")
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate changed before import")
    spec = importlib.util.spec_from_file_location("cm2_r28_q2_homogeneity_frozen", CERTIFICATE)
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
    except Exception as exc:
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
    replay = r + ("full_time2_Arb_replay",)
    registry = r + ("Q2_two_step_homogeneity_and_recut_registry",)
    slots = r + ("Q2_numeric_F5_F6_slot_registry",)
    typed = r + ("strong_type_separation",)
    frontier = r + ("downstream_frontier",)
    scope = r + ("strict_nonpromotion",)
    cases: list[tuple[str, tuple[Any, ...], Any]] = [
        ("schema", ("schema",), "bad"),
        ("certificate", ("certificate_sha256",), "0" * 64),
        ("dependency", ("dependencies", next(iter(EXPECTED_DEPENDENCIES))), "0" * 64),
        ("verdict h", ("verdict", "Q2_two_step_physical_homogeneity_children"), "CERTIFIED_1"),
        ("verdict recut", ("verdict", "Q2_canonical_recut_branch_rule_ids"), "CERTIFIED_1"),
        ("verdict F5", ("verdict", "Q2_numeric_F5_slots"), "CERTIFIED_1"),
        ("verdict F6", ("verdict", "Q2_numeric_F6_slots"), "CERTIFIED_1"),
        ("verdict q", ("verdict", "Q2_numeric_strong_q2"), "CERTIFIED"),
        ("verdict Gate4", ("verdict", "Gate4"), "CERTIFIED"),
        ("verdict Gate5", ("verdict", "Gate5"), "CERTIFIED"),
        ("verdict CM2", ("verdict", "CM2"), "GO"),
        ("result schema", r + ("schema",), "bad"),
        ("result digest", r + ("internal_replay_digest",), "0" * 64),
        ("provenance deps", r + ("provenance", "dependency_sha256"), {}),
        ("old modified", r + ("provenance", "old_artifacts_modified"), True),
        ("replay engine", r + ("provenance", "replay_engine"), "float"),
        ("precision", replay + ("precision_bits",), 53),
        ("parents", replay + ("Q1_parent_count",), 1),
        ("leaves", replay + ("terminal_leaf_count",), 1),
        ("classification", replay + ("classification_histogram", "SURVIVE_THROUGH_2_INNER"), 1),
        ("owner", replay + ("owner_status_histogram", "strict_unique_second_collision_owner"), 1),
        ("terminal digest", replay + ("terminal_atom_ids_sha256",), "0" * 64),
        ("Q2 count", replay + ("strict_Q2_atom_count",), 1),
        ("Q2 IDs", replay + ("strict_Q2_atom_ids_sha256",), "x"),
        ("Q2 mass", replay + ("Q2_coordinate_base_mass_exact",), "1"),
        ("unresolved mass", replay + ("unresolved_coordinate_base_mass_exact",), "1"),
        ("R2 count", replay + ("finite_depth_R2_admitted_count",), 1),
        ("k0", registry + ("homogeneity_cutoff_k0",), 41),
        ("cosine", registry + ("central_H0_target_cosine_strict_lower",), "1"),
        ("registry Q2", registry + ("strict_Q2_atom_count",), 1),
        ("eligible", registry + ("fully_materialized_Q2_atom_count",), 1),
        ("blocked", registry + ("blocked_Q2_atom_count",), 1),
        ("blockers", registry + ("blocker_histogram",), {"bad": 1}),
        ("first blocker", registry + ("first_blocker",), {"bad": 1}),
        ("owner cores", registry + ("fresh_step1_parent_core_owner_replay_count",), 1),
        ("owner Q2", registry + ("fresh_step2_unique_owner_Q2_count",), 1),
        ("h1", registry + ("time1_physical_homogeneity_child_id_count",), 1),
        ("h2", registry + ("time2_physical_homogeneity_child_id_count",), 1),
        ("children", registry + ("two_step_homogeneous_child_id_count",), 1),
        ("recut rules", registry + ("canonical_recut_branch_rule_id_count",), 1),
        ("recut rules per atom", registry + ("canonical_recut_branch_rules_per_materialized_Q2_atom",), 1),
        ("homogeneity crossing", registry + ("whole_atom_crosses_physical_homogeneity_boundary_count",), 1),
        ("strict chart", registry + ("strict_single_time2_target_chart_Q2_atom_count",), 1),
        ("seam", registry + ("time2_target_chart_seam_not_strictly_excluded_Q2_atom_count",), 1),
        ("seam physical", registry + ("chart_seams_are_representation_boundaries_not_physical_cuts",), False),
        ("chart free", registry + ("chart_free_physical_homogeneity_recut_used_for_F5_F6",), False),
        ("time1 charts", registry + ("time1_target_chart_histogram",), {}),
        ("time2 charts", registry + ("time2_target_chart_histogram",), {}),
        ("word digest", registry + ("collision_target_word_histogram_sha256",), "0" * 64),
        ("audit digest", registry + ("full_Q2_geometry_audit_rows_sha256",), "0" * 64),
        ("payload digest", registry + ("materialized_payload_rows_sha256",), "0" * 64),
        ("F5 count", slots + ("F5_universal_branch_rule_slot_count",), 1),
        ("F6 count", slots + ("F6_universal_branch_rule_slot_count",), 1),
        ("theta", slots + ("one_step_adapted_unstable_inverse_strict_upper",), "1"),
        ("theta2", slots + ("two_step_adapted_unstable_inverse_strict_upper",), "1"),
        ("variation", slots + ("one_step_canonical_recut_log_variation_strict_upper",), "1"),
        ("variation2", slots + ("two_step_canonical_recut_log_variation_strict_upper",), "1"),
        ("F5 digest", slots + ("F5_universal_branch_rule_slot_ids_sha256",), "0" * 64),
        ("F6 digest", slots + ("F6_universal_branch_rule_slot_ids_sha256",), "0" * 64),
        ("h digest", slots + ("homogeneity_child_ids_sha256",), "0" * 64),
        ("recut digest", slots + ("canonical_recut_branch_rule_ids_sha256",), "0" * 64),
        ("branch theorem", slots + ("universal_template_reinstantiated_as_branch_rule_theorem",), False),
        ("global J", slots + ("unsplit_Q2_atom_given_one_global_unstable_Jacobian_value",), True),
        ("restrictions", typed + ("joined_prior_restriction_id_count",), 1),
        ("mass slots", typed + ("joined_prior_coordinate_and_collision_mass_slot_count",), 1),
        ("area slots", typed + ("joined_prior_invariant_area_Jacobian_slot_count",), 1),
        ("mass type", typed + ("coordinate_base_mass_is_exact_collision_area_mass",), True),
        ("coord J", typed + ("invariant_area_Jacobian_is_adaptive_coordinate_Jacobian",), True),
        ("unstable J", typed + ("invariant_area_Jacobian_is_unstable_one_dimensional_Jacobian",), True),
        ("area F6", typed + ("invariant_area_log_distortion_is_F6",), True),
        ("Cfw", typed + ("numeric_C_fw_count",), 1),
        ("Crev", typed + ("numeric_C_rev_count",), 1),
        ("q2", typed + ("numeric_strong_q2_count",), 1),
        ("F4 frontier", frontier + ("F4_strict_single_time2_chart_slot_count",), 114006),
        ("F7", frontier + ("F7_materialized_Q2_slot_count",), 1),
        ("F14", frontier + ("F14_through_F18_materialized_Q2_slot_count",), 1),
        ("frontier digest", frontier + ("rows_sha256",), "0" * 64),
        ("frontier status", frontier + ("rows", 1, "status"), "CERTIFIED"),
        ("R2 empty", scope + ("finite_depth_R2_admitted_zero_means_physical_R2_empty",), True),
        ("complete R2Q2", scope + ("complete_limiting_R2_Q2_partition_reproved_here",), True),
        ("arbitrary n", scope + ("arbitrary_n_component_registry",), "CERTIFIED"),
        ("scope F7", scope + ("F7_characteristic_cut_growth",), "CERTIFIED"),
        ("scope F14", scope + ("F14_through_F18",), "CERTIFIED"),
        ("scope q", scope + ("numeric_strong_q2",), "CERTIFIED"),
        ("recovery", scope + ("survivor_conditioned_recovery",), "CERTIFIED"),
        ("tail", scope + ("strong_q_weighted_excursion_cemetery_tail",), "CERTIFIED"),
        ("LY", scope + ("induced_strong_Lasota_Yorke",), "CERTIFIED"),
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
    print("Q2_HOMOGENEITY_RECUT_INTEGRITY: PASS")
    if args.replay:
        print("Q2_HOMOGENEITY_RECUT_FULL_384BIT_ARB_REPLAY: PASS")
    if args.self_test:
        print(f"HOSTILE_TESTS: {len(mutation_cases())}/{len(mutation_cases())} PASS")
    if args.integrity_only or args.replay or args.self_test:
        return 0
    print("Q2_PHYSICAL_HOMOGENEITY: CERTIFIED_114006")
    print("Q2_RECUT_BRANCH_RULE_IDS: CERTIFIED_228012; ACTUAL_CURVE_INSTANCE_IDS: 0")
    print("Q2_NUMERIC_F5_F6: CERTIFIED_114006_UNIVERSAL_BRANCH_RULE_SLOTS")
    print("Q2_TIME2_STRICT_SINGLE_CHART_SUBLEDGER: 108726; SEAM_FRONTIER: 5280")
    print("Q2_F7_F14_F18_AND_STRONG_Q2: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    sys.exit(main())
