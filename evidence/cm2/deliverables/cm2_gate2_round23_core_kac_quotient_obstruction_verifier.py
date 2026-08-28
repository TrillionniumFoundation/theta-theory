#!/usr/bin/env python3
"""Fail-closed verifier for the round-23 core/Kac Gate-2 obstruction."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate2.round23-core-kac-quotient-obstruction.manifest.v1"
RESULT_SCHEMA = "cm2.gate2.round23-core-kac-quotient-obstruction.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate2-round23-core-kac-quotient-obstruction-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate2_round23_core_kac_quotient_obstruction_cert.py"
EXPECTED_CERTIFICATE_SHA256 = (
    "6f5b094875a4974e6dabc1ac1e454401861d08f5aae5d1a3048bcf0f3347961e"
)
EXPECTED_RESULT_DIGEST = (
    "7a3f0ffb916a098d01e2c67a618f37a8a60a19f4023cdeddeab747aa00cc2fa7"
)
EXPECTED_DEPENDENCIES = {
    "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json": (
        "886c5feb8709ad26fd653e598edf344ba39cc3e08e6efbd02c9ad1133f784c65"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate45-corrected-maximal-row-kac-ledger-manifest-2026-07-15.json": (
        "d5f563545c4ddaddfbb6b5cde5c4f5d8030247209e2284c06aeb9d3255a771f0"
    ),
    "cm2-gate2-actual-stable-plaque-continuation-manifest-2026-07-15.json": (
        "1bfc3ea9f5eb587b41a94ba4fd808c03c309389269f8d5e903f9bfce09a4f871"
    ),
    "cm2-gate2-stable-saturation-scale-gap-manifest-2026-07-15.json": (
        "57bed82ae496750fa3c7d7202428c647e59b11029f823dc1752c93b9433ca0a7"
    ),
    "cm2-gate34-all-occurrence-first-core-stopping-manifest-2026-07-18.json": (
        "a40b52dcbeef8c9f3471115b2bbd2c438cc6e130c72bd619dd794d8925d97171"
    ),
    "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json": (
        "d66c8da53846ae86c373de5917e706fa183bfca265f0e4fb83a9be1c204dd053"
    ),
    "cm2-gate345-occurrence-core-component-slot-join-manifest-2026-07-18.json": (
        "826c7773b2a4989df8293e79419561fd4f7768f7fcf9434905b3a2032241cd0a"
    ),
}
EXPECTED_VERDICT = {
    "round23_core_kac_Gate2_precursor_audit": "CERTIFIED",
    "Gate2_field_promotion_after_round23": "0_OF_17",
    "core_kac_to_PPE_nonimplication": "CERTIFIED",
    "physical_stable_quotient_PPE": "NOT_CERTIFIED",
    "Gate2": "NOT_CERTIFIED",
}


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def parse_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=reject_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"nonfinite JSON: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def verify_paths() -> list[str]:
    errors: list[str] = []
    for name, expected in {
        CERTIFICATE.name: EXPECTED_CERTIFICATE_SHA256,
        **EXPECTED_DEPENDENCIES,
    }.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            errors.append(f"unsafe or missing path: {name}")
        elif sha256_path(path) != expected:
            errors.append(f"frozen hash: {name}")
    return errors


def check(manifest: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict) or set(manifest) != {
        "schema",
        "certificate_sha256",
        "verifier_sha256",
        "dependencies",
        "result",
        "verdict",
    }:
        return ["manifest exact key set"]
    if manifest["schema"] != SCHEMA:
        errors.append("manifest schema")
    if manifest["certificate_sha256"] != EXPECTED_CERTIFICATE_SHA256:
        errors.append("certificate hash field")
    if manifest["verifier_sha256"] != sha256_path(Path(__file__)):
        errors.append("verifier hash")
    if not strict_equal(manifest["dependencies"], EXPECTED_DEPENDENCIES):
        errors.append("dependencies")
    errors.extend(verify_paths())

    result = manifest["result"]
    expected_keys = {
        "schema",
        "provenance",
        "round23_precursor_inventory",
        "axis_type_guard",
        "Gate2_17_field_nonpromotion",
        "exact_core_kac_nonimplication_countermodel",
        "shortest_new_physical_input",
        "strict_nonpromotion",
        "internal_replay_digest",
    }
    if not isinstance(result, dict) or set(result) != expected_keys:
        errors.append("result exact key set")
        return errors
    if result["schema"] != RESULT_SCHEMA:
        errors.append("result schema")
    if result["internal_replay_digest"] != result_digest(result):
        errors.append("result digest")
    if result["internal_replay_digest"] != EXPECTED_RESULT_DIGEST:
        errors.append("frozen result digest")
    if not strict_equal(
        result["provenance"],
        {
            "dependency_sha256": EXPECTED_DEPENDENCIES,
            "old_artifacts_modified": False,
            "audit_policy": "carrier_and_branch_type_exact_nonpromotion",
        },
    ):
        errors.append("provenance")

    inventory = result["round23_precursor_inventory"]
    for key, expected in {
        "positive_collision_core_count": 24,
        "positive_collision_SRB_mass_strict_lower": "147/550000",
        "charged_first_core_entrance_cylinder_count": 128,
        "entrance_destination_core_count": 14,
        "entrance_cylinders_cover_entire_occurrence_rows": False,
        "local_source_current_box_count": 4,
        "local_finite_first_return_current_cylinder_count": 3,
        "local_boxes_are_full_2d_collision_core_rectangles": False,
        "local_equal_coordinate_fraction_is_collision_SRB_probability": False,
        "finite_Borel_four_term_Kac_algebra": "CERTIFIED",
        "physical_four_term_Kac_CM2_typing": "NOT_CERTIFIED",
    }.items():
        if not isinstance(inventory, dict) or not strict_equal(inventory.get(key), expected):
            errors.append(f"inventory: {key}")

    axes = result["axis_type_guard"]
    for key in (
        "parameter_side_is_Gate2_inverse_branch",
        "recovery_orientation_is_Gate2_inverse_branch",
        "singular_Kac_coordinate_is_Gate2_inverse_branch",
        "destination_core_label_is_stable_projection_fibre",
    ):
        if not isinstance(axes, dict) or axes.get(key) is not False:
            errors.append(f"axis: {key}")
    if not isinstance(axes, dict) or axes.get("fake_Gate2_branch_rows_materialized") != 0:
        errors.append("fake Gate2 branches")

    fields = result["Gate2_17_field_nonpromotion"]
    for key, expected in {
        "required_field_count": 17,
        "completed_physical_field_count_before_round23": 0,
        "completed_physical_field_count_after_round23": 0,
        "new_physical_Gate2_field_promotions": 0,
        "first_missing_object": "stable_saturated_product_base_Lambda_A",
        "field_rows_sha256": (
            "167b7b669242a3ecee441666f9dd6580d368e9007e20c521896c0211c569a3d9"
        ),
        "all_fields_share_one_physical_branch_registry": False,
    }.items():
        if not isinstance(fields, dict) or not strict_equal(fields.get(key), expected):
            errors.append(f"fields: {key}")

    counter = result["exact_core_kac_nonimplication_countermodel"]
    for key, expected in {
        "state_count": 128,
        "owner_count": 64,
        "destination_label_count": 14,
        "total_positive_mass": "1",
        "global_signed_Kac_sum": "0",
        "reverse_support_size_at_every_state": 1,
        "reverse_weight_square_sum_at_every_state": "1",
        "two_copy_diagonal_pair_energy_coefficient": "1",
        "strict_pair_energy_contraction_kappa_lt_1": False,
        "positive_core_mass_plus_exact_Kac_implies_PPE": False,
        "countermodel_payload_sha256": (
            "131f76f84e66b22e6981b385657463414d75bea711cc261ef666a3260080729f"
        ),
    }.items():
        if not isinstance(counter, dict) or not strict_equal(counter.get(key), expected):
            errors.append(f"countermodel: {key}")

    shortest = result["shortest_new_physical_input"]
    if not isinstance(shortest, dict) or shortest.get("first_required_object") != (
        "stable_saturated_product_base_Lambda_A"
    ):
        errors.append("shortest input")
    expected_scope = {
        "24_core_union_is_stable_saturated_product_base": False,
        "destination_core_id_is_stable_projection": False,
        "first_core_stopping_word_is_native_scale_stop": False,
        "local_return_current_box_is_stable_saturated_return_strip": False,
        "collision_SRB_core_mass_is_quotient_density": False,
        "parameter_or_recovery_axis_is_reverse_branch_axis": False,
        "Borel_Kac_coordinates_are_parentwise_PPE_amplitudes": False,
        "new_Gate2_fields_promoted": 0,
        "physical_PPE": "NOT_CERTIFIED",
        "Gate2": "NOT_CERTIFIED",
    }
    if not strict_equal(result["strict_nonpromotion"], expected_scope):
        errors.append("strict nonpromotion")
    if not strict_equal(manifest["verdict"], EXPECTED_VERDICT):
        errors.append("verdict")
    return errors


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(manifest["result"])


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[str, ...], value: Any) -> None:
        candidate = copy.deepcopy(manifest)
        target: Any = candidate
        for part in path[:-1]:
            target = target[part]
        target[path[-1]] = value
        if path[0] == "result":
            refresh(candidate)
        mutations.append(candidate)

    mutate(("schema",), "bad")
    mutate(("certificate_sha256",), "0" * 64)
    mutate(("verifier_sha256",), "0" * 64)
    candidate = copy.deepcopy(manifest)
    candidate["unknown"] = True
    mutations.append(candidate)
    candidate = copy.deepcopy(manifest)
    candidate["dependencies"]["../escape"] = "0" * 64
    mutations.append(candidate)

    inv = ("result", "round23_precursor_inventory")
    for key, value in (
        ("positive_collision_core_count", 23),
        ("positive_collision_SRB_mass_strict_lower", "1"),
        ("charged_first_core_entrance_cylinder_count", 127),
        ("entrance_destination_core_count", 13),
        ("entrance_cylinders_cover_entire_occurrence_rows", True),
        ("local_source_current_box_count", 3),
        ("local_finite_first_return_current_cylinder_count", 4),
        ("local_boxes_are_full_2d_collision_core_rectangles", True),
        ("local_equal_coordinate_fraction_is_collision_SRB_probability", True),
        ("physical_four_term_Kac_CM2_typing", "CERTIFIED"),
    ):
        mutate(inv + (key,), value)
    axes = ("result", "axis_type_guard")
    for key in (
        "parameter_side_is_Gate2_inverse_branch",
        "recovery_orientation_is_Gate2_inverse_branch",
        "singular_Kac_coordinate_is_Gate2_inverse_branch",
        "destination_core_label_is_stable_projection_fibre",
    ):
        mutate(axes + (key,), True)
    mutate(axes + ("fake_Gate2_branch_rows_materialized",), 128)

    fields = ("result", "Gate2_17_field_nonpromotion")
    mutate(fields + ("required_field_count",), 16)
    mutate(fields + ("completed_physical_field_count_after_round23",), 1)
    mutate(fields + ("new_physical_Gate2_field_promotions",), 1)
    mutate(fields + ("first_missing_object",), "reference_unstable_interval_I_A")
    mutate(fields + ("field_rows",), [])
    mutate(fields + ("field_rows_sha256",), "0" * 64)
    mutate(fields + ("all_fields_share_one_physical_branch_registry",), True)

    counter = ("result", "exact_core_kac_nonimplication_countermodel")
    for key, value in (
        ("total_positive_mass", "0"),
        ("global_signed_Kac_sum", "1"),
        ("reverse_support_size_at_every_state", 2),
        ("reverse_weight_square_sum_at_every_state", "1/2"),
        ("two_copy_diagonal_pair_energy_coefficient", "1/2"),
        ("strict_pair_energy_contraction_kappa_lt_1", True),
        ("stable_saturated_product_base_created", True),
        ("positive_core_mass_plus_exact_Kac_implies_PPE", True),
        ("countermodel_payload_sha256", "0" * 64),
    ):
        mutate(counter + (key,), value)

    scope = ("result", "strict_nonpromotion")
    for key in (
        "24_core_union_is_stable_saturated_product_base",
        "destination_core_id_is_stable_projection",
        "first_core_stopping_word_is_native_scale_stop",
        "local_return_current_box_is_stable_saturated_return_strip",
        "collision_SRB_core_mass_is_quotient_density",
        "parameter_or_recovery_axis_is_reverse_branch_axis",
        "Borel_Kac_coordinates_are_parentwise_PPE_amplitudes",
    ):
        mutate(scope + (key,), True)
    mutate(scope + ("new_Gate2_fields_promoted",), 1)
    mutate(scope + ("physical_PPE",), "CERTIFIED")
    mutate(scope + ("Gate2",), "CERTIFIED")
    mutate(("verdict", "Gate2_field_promotion_after_round23"), "1_OF_17")
    mutate(("verdict", "physical_stable_quotient_PPE"), "CERTIFIED")
    mutate(("verdict", "Gate2"), "CERTIFIED")
    mutate(inv + ("positive_collision_core_count",), True)

    duplicate = nonfinite = False
    try:
        parse_json('{"x":1,"x":2}')
    except DuplicateKeyError:
        duplicate = True
    try:
        parse_json('{"x":Infinity}')
    except ValueError:
        nonfinite = True
    rejected = sum(bool(check(candidate)) for candidate in mutations)
    rejected += int(duplicate) + int(nonfinite)
    return rejected, len(mutations) + 2


def load_certificate() -> Any:
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate hash changed")
    spec = importlib.util.spec_from_file_location("gate2_round23_frozen", CERTIFICATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import certificate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if Path(module.__file__).resolve() != CERTIFICATE.resolve():
        raise RuntimeError("certificate path mismatch")
    return module


def main() -> int:
    if sys.flags.optimize != 0:
        print("ERROR: optimized Python", file=sys.stderr)
        return 1
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.manifest.is_symlink():
            raise ValueError("manifest symlink")
        manifest = parse_json(args.manifest.read_text(encoding="utf-8"))
    except Exception as error:
        print(f"MANIFEST_READ_ERROR: {error}", file=sys.stderr)
        return 1
    errors = check(manifest)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.replay:
        try:
            replay = load_certificate().build_result()
        except Exception as error:
            print(f"ERROR: replay: {error}", file=sys.stderr)
            return 1
        if canonical_json(replay) != canonical_json(manifest["result"]):
            print("ERROR: replay mismatch", file=sys.stderr)
            return 1
    if args.self_test:
        rejected, total = self_test(manifest)
        status = "PASS" if rejected == total else "FAIL"
        print(f"SELF_TEST: {status} ({rejected}/{total} mutations rejected)")
        return 0 if rejected == total else 1
    if args.replay or args.integrity_only:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("ROUND23_CORE_KAC_GATE2_PRECURSOR_AUDIT: CERTIFIED")
    print("GATE2_FIELD_PROMOTION_AFTER_ROUND23: 0/17")
    print("CORE_KAC_TO_PPE_NONIMPLICATION: CERTIFIED")
    print("PHYSICAL_STABLE_QUOTIENT_PPE: NOT_CERTIFIED")
    print("GATE2: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
