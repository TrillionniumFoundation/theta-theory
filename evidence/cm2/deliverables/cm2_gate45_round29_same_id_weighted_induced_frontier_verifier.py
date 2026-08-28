#!/usr/bin/env python3
"""Fail-closed verifier for the round-29 same-ID weighted/induced frontier."""

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
from typing import Any, Iterator


Q = Fraction
HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate45.round29-same-id-weighted-induced-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate45.round29-same-id-weighted-induced-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate45-round29-same-id-weighted-induced-frontier-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate45_round29_same_id_weighted_induced_frontier_cert.py"
EXPECTED_CERTIFICATE_SHA256 = (
    "c84130618cea9f050a5055ac3b15a2075754d265a29166a5368a2d0ac62dc318"
)
EXPECTED_RESULT_DIGEST = (
    "9193a023d6b1336cc6c6378162628333f0e4eb8409b443dd44e68ff2d23b156a"
)
EXPECTED_DEPENDENCIES = {
    "cm2-gate34-round28-nonempty-adaptive-component-registry-manifest-2026-07-18.json": (
        "120a3f1cba9f23cc4b2a9753491022f8143175810b19f1a9f9d8ee0214d66b60"
    ),
    "cm2-gate45-round28-q2-homogeneity-recut-manifest-2026-07-18.json": (
        "9fe09f46e2201a54e000ea67ac09521ce73e1fe012b5205e12541805787683b3"
    ),
    "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json": (
        "eef1071c1f4973892bf5e450421f3b91de7a2b426165e6a8c6f8bb4404eeac57"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate45-induced-strong-coefficient-obstruction-manifest-2026-07-18.json": (
        "bad4bd8c12bccdcfad7210d44ed85fb023615c6db7aca9954e815a4729ce31e6"
    ),
    "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json": (
        "f846df9e0afe3e81bedb9cb1a4cb80446d8b79eabb9fd6577e223f6aa1e282ab"
    ),
    "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json": (
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140"
    ),
}
EXPECTED_VERDICT = {
    "same_origin_finite_Q2_component_mass_restriction_homogeneity_F5_F6_skeleton": "CERTIFIED_114006",
    "finite_R1_first_return_component_anchors": "CERTIFIED_4216",
    "Q2_actual_parent_curve_recut_instances": "NOT_CERTIFIED_COUNT_0",
    "Q2_common_standard_family_recovery_carriers": "NOT_CERTIFIED_COUNT_0",
    "numeric_C_fw_C_rev_q": "NOT_CERTIFIED_COUNT_0",
    "Q2_payload_is_Rn_first_return_charge": False,
    "mass_zero_implies_strong_cemetery_charge_zero": False,
    "collision_null_to_boundary_Z_nonimplication": "CERTIFIED_EXACT_COUNTERMODEL",
    "survivor_conditioned_or_global_Lp_physical_envelope": "NOT_CERTIFIED_COUNT_0",
    "strong_q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
    "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
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


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


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
        errors.append("top-level key set")
    if data.get("schema") != SCHEMA:
        errors.append("manifest schema")
    if data.get("certificate_sha256") != EXPECTED_CERTIFICATE_SHA256:
        errors.append("certificate hash field")
    if not strict_equal(data.get("dependencies"), EXPECTED_DEPENDENCIES):
        errors.append("dependency table")
    if not strict_equal(data.get("verdict"), EXPECTED_VERDICT):
        errors.append("verdict")

    result = data.get("result")
    result_keys = {
        "schema",
        "provenance",
        "same_origin_finite_Q2_strong_skeleton",
        "weighted_tail_connectability",
        "strong_cemetery_mass_zero_nonimplication",
        "induced_strong_Lasota_Yorke_frontier",
        "strict_nonpromotion",
        "internal_replay_digest",
    }
    if not exact_keys(result, result_keys):
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
        if provenance.get("dependency_sha256") != EXPECTED_DEPENDENCIES:
            errors.append("provenance dependencies")
        if provenance.get("old_artifacts_modified") is not False:
            errors.append("old artifact scope")

        skeleton = result.get("same_origin_finite_Q2_strong_skeleton", {})
        exact_skeleton = {
            "nonempty_Q2_component_cell_count": 114006,
            "Q2_origin_atom_count": 114006,
            "Q2_adaptive_recut_depth_histogram": {"0": 114006},
            "Q2_finite_outer_count": 0,
            "Q2_parameter_averaged_coordinate_base_mass_exact": "5257799/5120000000",
            "Q2_exact_symbolic_collision_area_mass_row_count": 114006,
            "Q2_common_Borel_fw_rev_restriction_id_count": 114006,
            "Q2_two_step_physical_homogeneity_child_count": 114006,
            "Q2_canonical_recut_branch_rule_id_count": 228012,
            "Q2_F5_universal_branch_rule_slot_count": 114006,
            "Q2_F6_universal_branch_rule_slot_count": 114006,
            "Q2_F5_two_step_adapted_inverse_strict_upper": "20736000000/32521433569",
            "Q2_F6_two_step_log_variation_strict_upper": "3/100000",
            "same_origin_finite_Q2_skeleton_row_count": 114006,
            "same_origin_finite_Q2_skeleton_status": "CERTIFIED_114006",
        }
        for key, expected in exact_skeleton.items():
            if skeleton.get(key) != expected or type(skeleton.get(key)) is not type(expected):
                errors.append(f"Q2 skeleton: {key}")
        typed = skeleton.get("strong_type_boundary", {})
        expected_typed = {
            "Q2_level_type": "Q_2_SURVIVOR_NOT_R_n_FIRST_RETURN_SUMMAND",
            "actual_parent_curve_recut_instance_id_count": 0,
            "common_standard_family_recovery_carrier_count": 0,
            "numeric_C_fw_count": 0,
            "numeric_C_rev_count": 0,
            "numeric_q2_count": 0,
            "F7_characteristic_cut_growth_slot_count": 0,
            "F14_through_F18_slot_count": 0,
            "Borel_restriction_id_is_standard_family_recovery_carrier": False,
            "branch_rule_id_is_actual_parent_curve_recut_instance_id": False,
            "invariant_area_Jacobian_is_unstable_Jacobian": False,
            "Q2_survivor_charge_is_first_return_Rn_charge": False,
        }
        if not strict_equal(typed, expected_typed):
            errors.append("strong type boundary")
        r1 = skeleton.get("finite_R1_first_return_frontier", {})
        if r1.get("nonempty_R1_component_cell_count") != 4216:
            errors.append("R1 count")
        if r1.get("parameter_averaged_coordinate_base_mass_exact") != "6473/256000000":
            errors.append("R1 mass")
        if r1.get("candidate_local_maturity") != "13/18":
            errors.append("R1 maturity")
        if any(r1.get(key) != 0 for key in (
            "complete_F14_through_F18_slot_count",
            "numeric_first_return_C_fw_rows",
            "numeric_first_return_C_rev_rows",
            "numeric_first_return_q_rows",
        )):
            errors.append("R1 strong zero frontier")

        connect = result.get("weighted_tail_connectability", {})
        if connect.get("tail_prefactor_A") != "550000/147":
            errors.append("tail A")
        if connect.get("tail_block_factor_r") != "111718729/111718750":
            errors.append("tail r")
        if connect.get("Q2_payload_directly_admissible_as_Rn_return_charge_row_count") != 0:
            errors.append("Q2/Rn type")
        if connect.get("parameter_averaged_mass_implies_uniform_fixed_s_Lp_envelope") is not False:
            errors.append("parameter disintegration")
        rows = connect.get("required_interfaces")
        if not isinstance(rows, list) or len(rows) != 6:
            errors.append("connectability row count")
        else:
            if [row.get("index") for row in rows] != list(range(1, 7)):
                errors.append("connectability indices")
            if connect.get("required_interfaces_sha256") != digest(rows):
                errors.append("connectability rows digest")
            if rows[0].get("status") != "PARTIAL_FINITE_ANCHOR":
                errors.append("first interface scope")
            if any(row.get("status") != "NOT_CERTIFIED" for row in rows[1:]):
                errors.append("missing interface nonpromotion")
        for key in (
            "uniform_survivor_conditioned_Lp_envelope_count",
            "global_physical_first_return_Lp_envelope_count",
            "compatible_pointwise_first_return_envelope_count",
            "physical_Rn_q_density_rows_ready_for_tail_sum",
            "complete_interface_count",
        ):
            if connect.get(key) != 0:
                errors.append(f"connectability zero: {key}")

        cemetery = result.get("strong_cemetery_mass_zero_nonimplication", {})
        samples = cemetery.get("exact_samples")
        if cemetery.get("post_cut_boundary_Z") != "sum_components(weight/length)=N+1":
            errors.append("cemetery formula")
        if cemetery.get("physical_CM2_impossibility_claimed") is not False:
            errors.append("cemetery scope")
        if not isinstance(samples, list) or len(samples) != 7:
            errors.append("cemetery samples")
        else:
            if cemetery.get("samples_sha256") != digest(samples):
                errors.append("cemetery samples digest")
            for row in samples:
                n = row.get("N_internal_cut_points")
                if not isinstance(n, int) or n < 1:
                    errors.append("cemetery N")
                    continue
                if row.get("singular_set_Lebesgue_mass") != "0":
                    errors.append("cemetery mass")
                if row.get("complement_component_count") != n + 1:
                    errors.append("cemetery components")
                if Q(row.get("each_component_length", "0")) != Q(1, n + 1):
                    errors.append("cemetery length")
                if Q(row.get("each_component_weight", "0")) != Q(1, n + 1):
                    errors.append("cemetery weight")
                if Q(row.get("boundary_Z_sum_weight_over_length", "0")) != n + 1:
                    errors.append("cemetery Z")

        induced = result.get("induced_strong_Lasota_Yorke_frontier", {})
        numeric = induced.get("numeric_recovery_inputs", {})
        expected_numeric = {
            "vartheta_p": "360134800/360493663",
            "A0": 301500,
            "A1": 1005,
            "native_gamma": "1/12060",
            "all_iterate_D_std_strict_upper": "30000000",
        }
        if not strict_equal(numeric, expected_numeric):
            errors.append("numeric recovery inputs")
        nonimp = induced.get("typed_nonimplications", {})
        if not isinstance(nonimp, dict) or set(nonimp.values()) != {False}:
            errors.append("typed nonimplications")
        assembly = induced.get("assembly_rows")
        if not isinstance(assembly, list) or len(assembly) != 6:
            errors.append("induced assembly rows")
        else:
            if induced.get("assembly_rows_sha256") != digest(assembly):
                errors.append("induced assembly digest")
            if any(row.get("promotes_strong_coefficient") is not False for row in assembly):
                errors.append("induced promotion")
        if induced.get("complete_strong_assembly_row_count") != 0:
            errors.append("induced complete count")
        if induced.get("induced_strong_Lasota_Yorke") != "NOT_CERTIFIED":
            errors.append("induced status")

        scope = result.get("strict_nonpromotion", {})
        expected_scope = {
            "Q2_same_origin_skeleton_is_numeric_C_fw_C_rev_q": False,
            "Q2_survivor_cells_are_Rn_first_return_summands": False,
            "parameter_averaged_mass_is_uniform_fixed_s_strong_moment": False,
            "collision_null_cemetery_mass_is_zero_strong_cemetery_charge": False,
            "open_operator_bound_is_induced_operator_bound": False,
            "conditional_weighted_transfer_theorem_implies_current_weighted_tail": False,
            "strong_q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if not strict_equal(scope, expected_scope):
            errors.append("strict nonpromotion")

    if check_integrity:
        errors.extend(frozen_path_errors())
        if data.get("verifier_sha256") != sha256_path(Path(__file__).resolve()):
            errors.append("verifier hash field")
    return errors


def import_certificate() -> ModuleType:
    spec = importlib.util.spec_from_file_location("round29_cert", CERTIFICATE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import certificate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        module = import_certificate()
        rebuilt = module.build_result()
        if not strict_equal(data.get("result"), rebuilt):
            errors.append("certificate result replay")
        if not strict_equal(data.get("verdict"), module.verdict(rebuilt)):
            errors.append("certificate verdict replay")
    except Exception as exc:
        errors.append(f"replay exception: {type(exc).__name__}: {exc}")
    return errors


def scalar_paths(value: Any, prefix: tuple[Any, ...] = ()) -> Iterator[tuple[Any, ...]]:
    if isinstance(value, dict):
        for key in sorted(value):
            yield from scalar_paths(value[key], prefix + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from scalar_paths(item, prefix + (index,))
    else:
        yield prefix


def mutate_scalar(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "_MUTATED"
    if value is None:
        return "MUTATED"
    return None


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def self_test(data: dict[str, Any]) -> tuple[int, int, list[str]]:
    failures: list[str] = []
    if validate(data, check_integrity=False):
        return 0, 101, ["baseline manifest invalid"]

    mutations: list[tuple[str, dict[str, Any]]] = []
    for key in sorted(data):
        bad = copy.deepcopy(data)
        del bad[key]
        mutations.append((f"delete top-level {key}", bad))
    for key in sorted(EXPECTED_VERDICT):
        bad = copy.deepcopy(data)
        bad["verdict"][key] = mutate_scalar(bad["verdict"][key])
        mutations.append((f"verdict {key}", bad))
    for path in scalar_paths(data["result"]):
        if len(mutations) >= 99:
            break
        bad = copy.deepcopy(data)
        cursor = bad["result"]
        for key in path:
            cursor = cursor[key]
        set_path(bad["result"], path, mutate_scalar(cursor))
        mutations.append(("result path " + "/".join(map(str, path)), bad))
    if len(mutations) != 99:
        failures.append(f"mutation construction count {len(mutations)}")
    passed = 0
    for label, bad in mutations:
        if validate(bad, check_integrity=False):
            passed += 1
        else:
            failures.append(f"accepted mutation: {label}")

    parser_cases = [
        ('{"schema":"a","schema":"b"}', "duplicate JSON key"),
        ('{"x":NaN}', "nonfinite JSON"),
    ]
    for text, label in parser_cases:
        try:
            parse_json_text(text)
            failures.append(f"accepted parser mutation: {label}")
        except (DuplicateKeyError, ValueError):
            passed += 1
    return passed, 101, failures


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
        print(f"AUDIT_MODE: FAIL ({type(exc).__name__}: {exc})")
        return 1

    if args.self_test:
        passed, total, failures = self_test(data)
        if failures:
            print(f"HOSTILE_TESTS: {passed}/{total} FAIL")
            for failure in failures[:20]:
                print(f"- {failure}")
            return 1
        print(f"HOSTILE_TESTS: {passed}/{total} PASS")
        return 0

    errors = validate(data, check_integrity=True)
    if args.replay:
        errors.extend(replay_errors(data))
    if errors:
        print("AUDIT_MODE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("AUDIT_MODE: PASS")
    if args.integrity_only or args.replay:
        return 0
    print("SAME_ORIGIN_FINITE_Q2_STRONG_SKELETON: CERTIFIED_114006")
    print("NUMERIC_C_FW_C_REV_Q: NOT_CERTIFIED_COUNT_0")
    print("STRONG_Q_WEIGHTED_TAIL: NOT_CERTIFIED")
    print("INDUCED_STRONG_LASOTA_YORKE: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    sys.exit(main())
