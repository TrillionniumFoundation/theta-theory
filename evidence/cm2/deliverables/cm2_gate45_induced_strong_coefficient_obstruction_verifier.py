#!/usr/bin/env python3
"""Fail-closed verifier for the open-to-induced coefficient obstruction."""

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
SCHEMA = "cm2.gate45.induced-strong-coefficient-obstruction.manifest.v1"
RESULT_SCHEMA = "cm2.gate45.induced-strong-coefficient-obstruction.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate45-induced-strong-coefficient-obstruction-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate45_induced_strong_coefficient_obstruction_cert.py"
EXPECTED_CERTIFICATE_SHA256 = (
    "dc114c298548947365c169e14e27e9060f0376b4698a09ffbb9a411ad7b67018"
)
EXPECTED_RESULT_DIGEST = (
    "c6eecca112ba45645dbaa03137620e491e73e677c37ead08c90ba6ccd86867a8"
)
EXPECTED_DEPENDENCIES = {
    "cm2-gate345-occurrence-core-component-slot-join-manifest-2026-07-18.json": (
        "826c7773b2a4989df8293e79419561fd4f7768f7fcf9434905b3a2032241cd0a"
    ),
    "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json": (
        "d66c8da53846ae86c373de5917e706fa183bfca265f0e4fb83a9be1c204dd053"
    ),
    "cm2-gate4-fixed-core-green-kernel-unbounded-cut-frontier-manifest-2026-07-17.json": (
        "3475b2cf6af105b4d229e9683eb2f61433be2e4cefc8f1e8f2318c07762f3dd5"
    ),
    "cm2-gate45-sparse-cut-dwell-contraction-frontier-manifest-2026-07-17.json": (
        "8fc54ac0484bdf3b97ed0d3d4b267f208ead4d762213f595c08f44c7ed84c98a"
    ),
    "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json": (
        "417464531cae76bf774bdc35f1d2f25799237d1efde39be8850cf3408740f271"
    ),
    "cm2-gate25-quotient-18field-kac-closure-frontier-manifest-2026-07-17.json": (
        "7e54075f64a44a19dbf12599314d0ad7044d4463cfe90cc81c6499c5a3af793b"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
    "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json": (
        "64f3820e2dc2f6d544be94bbe205fcf08f9517eef29131311e6fafa295060a93"
    ),
}
EXPECTED_MISSING_FIELDS = [
    "physical_homogeneity_subbranch_table",
    "inverse_Jacobian_bound",
    "log_Jacobian_distortion_sum",
    "face_transversality_lower",
    "face_C2_atlas_bound",
    "coarea_density_regular_bound",
    "dynamic_Holder_test_pullback_bound",
    "C1_face_trace_pullback_bound",
    "moving_boundary_DQ_current_and_two_traces",
    "regular_density_operator_cost",
    "standard_family_operator_cost",
    "flux_face_operator_cost",
    "dynamic_test_operator_cost",
    "operator_phase_block",
]
EXPECTED_VERDICT = {
    "round23_entrance_incidence_join_64_128_14": "CERTIFIED",
    "selected_component_field_maturity": "4_OF_18",
    "field5_field6_seed_to_slot_promotion": "NOT_CERTIFIED",
    "open_to_induced_coefficient_nonimplication": "CERTIFIED",
    "induced_strong_coefficient": "NOT_CERTIFIED",
    "complete_18_field_operator_blocks": 0,
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


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def exact_key_set(value: Any, keys: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == keys


def verify_frozen_paths() -> list[str]:
    errors: list[str] = []
    paths = {CERTIFICATE.name: EXPECTED_CERTIFICATE_SHA256, **EXPECTED_DEPENDENCIES}
    for name, expected in paths.items():
        path = HERE / name
        if not path.is_file():
            errors.append(f"missing frozen path: {name}")
            continue
        if path.is_symlink() or path.resolve().parent != HERE:
            errors.append(f"unsafe frozen path: {name}")
            continue
        if sha256_path(path) != expected:
            errors.append(f"frozen hash: {name}")
    return errors


def check(manifest: Any) -> list[str]:
    errors: list[str] = []
    if not exact_key_set(
        manifest,
        {
            "schema",
            "certificate_sha256",
            "verifier_sha256",
            "dependencies",
            "result",
            "verdict",
        },
    ):
        return ["manifest exact key set"]
    assert isinstance(manifest, dict)
    if manifest["schema"] != SCHEMA:
        errors.append("manifest schema")
    if manifest["certificate_sha256"] != EXPECTED_CERTIFICATE_SHA256:
        errors.append("certificate hash field")
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        errors.append("certificate hash on disk")
    if manifest["verifier_sha256"] != sha256_path(Path(__file__)):
        errors.append("verifier hash")
    if not strict_equal(manifest["dependencies"], EXPECTED_DEPENDENCIES):
        errors.append("dependency table")
    errors.extend(verify_frozen_paths())

    result = manifest["result"]
    if not exact_key_set(
        result,
        {
            "schema",
            "provenance",
            "round23_join_and_field_boundary",
            "open_vs_induced_semantic_audit",
            "exact_operator_signature_countermodel",
            "missing_induced_strong_interface",
            "strict_nonpromotion",
            "internal_replay_digest",
        },
    ):
        errors.append("result exact key set")
        return errors
    assert isinstance(result, dict)
    if result["schema"] != RESULT_SCHEMA:
        errors.append("result schema")
    if result["internal_replay_digest"] != result_digest(result):
        errors.append("internal replay digest")
    if result["internal_replay_digest"] != EXPECTED_RESULT_DIGEST:
        errors.append("frozen result digest")
    expected_provenance = {
        "dependency_sha256": EXPECTED_DEPENDENCIES,
        "old_artifacts_modified": False,
        "audit_policy": "exact_manifest_join_plus_finite_state_countermodel",
    }
    if not strict_equal(result["provenance"], expected_provenance):
        errors.append("provenance")

    join = result["round23_join_and_field_boundary"]
    expected_join_scalars = {
        "occurrence_owner_count": 64,
        "parameter_side_branch_count": 128,
        "destination_core_count": 14,
        "selected_roof_one_component_count": 14,
        "entrance_incidence_join": "CERTIFIED",
        "bound_completed_selected_level_field_count": 4,
        "missing_completed_selected_level_field_count": 14,
        "field5_field6_component_local_seed_packet_count": 24,
        "field5_field6_completed_roof_level_slot_count": 0,
        "field5_field6_seed_to_slot_promotion": "NOT_CERTIFIED",
        "complete_18_field_operator_block_count": 0,
        "common_fw_rev_restriction_id": "NOT_CERTIFIED",
        "complete_four_term_physical_Kac_typing": "NOT_CERTIFIED",
    }
    if not isinstance(join, dict):
        errors.append("join boundary type")
    else:
        for key, expected in expected_join_scalars.items():
            if not strict_equal(join.get(key), expected):
                errors.append(f"join boundary: {key}")
        if not strict_equal(
            join.get("bound_completed_selected_level_fields"),
            [
                "nonempty_or_empty_domain_proof",
                "homogeneous_prefix_chart",
                "homogeneous_suffix_chart",
                "one_step_cut_growth_Z_sum",
            ],
        ):
            errors.append("bound field list")
        if not strict_equal(
            join.get("missing_completed_selected_level_fields"),
            EXPECTED_MISSING_FIELDS,
        ):
            errors.append("missing field list")

    semantic = result["open_vs_induced_semantic_audit"]
    expected_semantic = {
        "frozen_open_operator": "O=L M_C",
        "target_first_return_operator": (
            "R_n=M_C L (M_complement L)^(n-1) M_C"
        ),
        "target_survivor_operator": "Q_n=(M_complement L)^n M_C",
        "operator_signatures_identical": False,
        "four_local_boxes_strictly_outside_core_at_post_core_time_one": True,
        "repeated_open_power_tracks_these_excursions_until_return": False,
        "b_core_reusable_as_induced_Lasota_Yorke_coefficient": False,
    }
    if not isinstance(semantic, dict):
        errors.append("semantic audit type")
    else:
        for key, expected in expected_semantic.items():
            if not strict_equal(semantic.get(key), expected):
                errors.append(f"semantic audit: {key}")

    counter = result["exact_operator_signature_countermodel"]
    expected_counter = {
        "O_squared": [[0, 0], [0, 0]],
        "R_2_equals_M_core_L_M_complement_L_M_core": [[1, 0], [0, 0]],
        "l1_operator_norm_O_squared": 0,
        "l1_operator_norm_R_2": 1,
        "O_squared_norm_le_b_core_squared": True,
        "R_2_norm_gt_b_core_squared": True,
        "formal_implication_open_power_bound_to_induced_return_bound": False,
        "matrix_payload_sha256": (
            "6c7318cc0501404014a8609ebab542995da3facf59ee0e9c1a26a458f6893461"
        ),
    }
    if not isinstance(counter, dict):
        errors.append("countermodel type")
    else:
        for key, expected in expected_counter.items():
            if not strict_equal(counter.get(key), expected):
                errors.append(f"countermodel: {key}")

    missing = result["missing_induced_strong_interface"]
    expected_missing = {
        "required_record_count": 13,
        "certified_complete_record_count": 0,
        "records_sha256": (
            "dcac8aae3d28b728cbd0b20e6afd3de5718ccbe0e49b6b0e46e727303ae656fc"
        ),
        "mass_identity_target": (
            "source_mass=sum_first_return_mass+singular_cemetery_mass+survivor_mass"
        ),
        "weighted_tail_target": "sum_{tau>n}q_tau<=C*rho^n",
        "coefficient_compatibility_target": "rho*exp(A_loss)<1",
    }
    if not isinstance(missing, dict):
        errors.append("missing interface type")
    else:
        for key, expected in expected_missing.items():
            if not strict_equal(missing.get(key), expected):
                errors.append(f"missing interface: {key}")

    expected_scope = {
        "entrance_incidence_join_implies_common_recovery_carrier": False,
        "component_local_field5_field6_seeds_imply_completed_slots": False,
        "open_operator_power_bound_implies_first_return_operator_bound": False,
        "four_local_return_boxes_imply_full_collision_SRB_partition": False,
        "Borel_TV_Linf_constants_imply_three_CM2_norm_intertwiners": False,
        "b_core_is_induced_Lasota_Yorke_coefficient": False,
        "complete_18_field_operator_blocks": 0,
        "induced_strong_coefficient": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    if not strict_equal(result["strict_nonpromotion"], expected_scope):
        errors.append("strict nonpromotion")
    if not strict_equal(manifest["verdict"], EXPECTED_VERDICT):
        errors.append("verdict")
    return errors


def load_certificate() -> ModuleType:
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate hash changed before import")
    spec = importlib.util.spec_from_file_location(
        "cm2_gate45_induced_strong_coefficient_obstruction_cert_frozen",
        CERTIFICATE,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot create frozen certificate import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if Path(module.__file__).resolve() != CERTIFICATE.resolve():
        raise RuntimeError("certificate resolved path mismatch")
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate hash changed after import")
    return module


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(
        manifest["result"]
    )


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

    mutate(("schema",), "cm2.bad")
    mutate(("certificate_sha256",), "0" * 64)
    mutate(("verifier_sha256",), "0" * 64)
    candidate = copy.deepcopy(manifest)
    candidate["unknown"] = True
    mutations.append(candidate)
    candidate = copy.deepcopy(manifest)
    candidate["dependencies"]["../escape.json"] = "0" * 64
    mutations.append(candidate)

    join = ("result", "round23_join_and_field_boundary")
    mutate(join + ("occurrence_owner_count",), 63)
    mutate(join + ("parameter_side_branch_count",), 127)
    mutate(join + ("destination_core_count",), 13)
    mutate(join + ("selected_roof_one_component_count",), 13)
    mutate(join + ("entrance_incidence_join",), "NOT_CERTIFIED")
    mutate(join + ("bound_completed_selected_level_field_count",), 5)
    mutate(join + ("missing_completed_selected_level_field_count",), 13)
    mutate(join + ("field5_field6_completed_roof_level_slot_count",), 28)
    mutate(join + ("field5_field6_seed_to_slot_promotion",), "CERTIFIED")
    mutate(join + ("complete_18_field_operator_block_count",), 14)
    mutate(join + ("common_fw_rev_restriction_id",), "CERTIFIED")
    mutate(join + ("complete_four_term_physical_Kac_typing",), "CERTIFIED")
    mutate(join + ("missing_completed_selected_level_fields",), [])
    mutate(join + ("field_status_rows_sha256",), "0" * 64)

    semantic = ("result", "open_vs_induced_semantic_audit")
    mutate(semantic + ("frozen_open_operator",), "R_n")
    mutate(semantic + ("operator_signatures_identical",), True)
    mutate(
        semantic + ("four_local_boxes_strictly_outside_core_at_post_core_time_one",),
        False,
    )
    mutate(semantic + ("repeated_open_power_tracks_these_excursions_until_return",), True)
    mutate(semantic + ("local_return_current_cylinders_form_full_source_partition",), True)
    mutate(semantic + ("native_no_hidden_recut_dwell_schedule",), "CERTIFIED")
    mutate(semantic + ("strong_complement_cemetery_payload",), "CERTIFIED")
    mutate(semantic + ("b_core_reusable_as_induced_Lasota_Yorke_coefficient",), True)

    counter = ("result", "exact_operator_signature_countermodel")
    mutate(counter + ("O_squared",), [[1, 0], [0, 0]])
    mutate(counter + ("R_2_equals_M_core_L_M_complement_L_M_core",), [[0, 0], [0, 0]])
    mutate(counter + ("l1_operator_norm_O_squared",), 1)
    mutate(counter + ("l1_operator_norm_R_2",), 0)
    mutate(counter + ("O_squared_norm_le_b_core_squared",), False)
    mutate(counter + ("R_2_norm_gt_b_core_squared",), False)
    mutate(counter + ("formal_implication_open_power_bound_to_induced_return_bound",), True)
    mutate(counter + ("matrix_payload_sha256",), "0" * 64)

    missing = ("result", "missing_induced_strong_interface")
    mutate(missing + ("required_record_count",), 12)
    mutate(missing + ("certified_complete_record_count",), 13)
    mutate(missing + ("records",), [])
    mutate(missing + ("records_sha256",), "0" * 64)
    mutate(missing + ("weighted_tail_target",), "mass-only")
    mutate(missing + ("coefficient_compatibility_target",), "rho<1")

    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("entrance_incidence_join_implies_common_recovery_carrier",), True)
    mutate(scope + ("component_local_field5_field6_seeds_imply_completed_slots",), True)
    mutate(scope + ("open_operator_power_bound_implies_first_return_operator_bound",), True)
    mutate(scope + ("Borel_TV_Linf_constants_imply_three_CM2_norm_intertwiners",), True)
    mutate(scope + ("b_core_is_induced_Lasota_Yorke_coefficient",), True)
    mutate(scope + ("induced_strong_coefficient",), "CERTIFIED")
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(scope + ("Gate5",), "CERTIFIED")
    mutate(("verdict", "open_to_induced_coefficient_nonimplication"), "NOT_CERTIFIED")
    mutate(("verdict", "induced_strong_coefficient"), "CERTIFIED")
    mutate(("verdict", "complete_18_field_operator_blocks"), 14)
    mutate(("verdict", "Gate4"), "CERTIFIED")
    mutate(("verdict", "Gate5"), "CERTIFIED")
    mutate(join + ("occurrence_owner_count",), True)

    duplicate_rejected = False
    nonfinite_rejected = False
    try:
        parse_json_text('{"x":1,"x":2}')
    except DuplicateKeyError:
        duplicate_rejected = True
    try:
        parse_json_text('{"x":NaN}')
    except ValueError:
        nonfinite_rejected = True

    rejected = sum(bool(check(candidate)) for candidate in mutations)
    rejected += int(duplicate_rejected) + int(nonfinite_rejected)
    return rejected, len(mutations) + 2


def main() -> int:
    if sys.flags.optimize != 0:
        print("ERROR: optimized Python disables proof assertions", file=sys.stderr)
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
            raise ValueError("manifest symlink rejected")
        manifest = parse_json_text(args.manifest.read_text(encoding="utf-8"))
    except Exception as error:
        print(f"MANIFEST_READ_ERROR: {error}", file=sys.stderr)
        return 1
    errors = check(manifest)
    if errors:
        print("ERROR: " + "; ".join(errors), file=sys.stderr)
        return 1
    if args.replay:
        try:
            certificate = load_certificate()
            replay = certificate.build_result()
        except Exception as error:
            print(f"ERROR: replay failure: {error}", file=sys.stderr)
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
    print("ROUND23_ENTRANCE_INCIDENCE_JOIN_64_128_14: CERTIFIED")
    print("SELECTED_COMPONENT_FIELD_MATURITY: 4/18")
    print("OPEN_TO_INDUCED_COEFFICIENT_NONIMPLICATION: CERTIFIED")
    print("INDUCED_STRONG_COEFFICIENT: NOT_CERTIFIED")
    print("GATE4_GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
