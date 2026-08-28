#!/usr/bin/env python3
"""Fail-closed verifier for the C24 induced strong-payload frontier."""

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


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.gate45.induced-strong-payload-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate45.induced-strong-payload-frontier.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate45-induced-strong-payload-frontier-manifest-2026-07-18.json"
CERTIFICATE = HERE / "cm2_gate45_induced_strong_payload_frontier_cert.py"
EXPECTED_CERTIFICATE_SHA256 = "f32fd9342e10f18cd05a54e53bc2c37ecc51649c54e02a982093e47d20f03076"
EXPECTED_RESULT_DIGEST = "0e4e720bd7dadb5d6bfc6cc2476fd16b5561a1394c0dee36e32cbc2a144738d9"
EXPECTED_RESTRICTION_SCHEMA_ID = "restriction-schema:dc816cc8b577e2e8971974c9cff4fb1c58d62b1ba2ffe11c63b1c286026198e1"
EXPECTED_DEPENDENCIES = {
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a",
    "cm2-gate45-induced-strong-coefficient-obstruction-manifest-2026-07-18.json": "bad4bd8c12bccdcfad7210d44ed85fb023615c6db7aca9954e815a4729ce31e6",
    "cm2-gate25-selected-component-chart-field-slots-manifest-2026-07-17.json": "417464531cae76bf774bdc35f1d2f25799237d1efde39be8850cf3408740f271",
    "cm2-gate25-universal-operator-endpoint-template-frontier-manifest-2026-07-16.json": "d532eeab0fa24901228a589724ffc4dbcff721f7d174a2b519187d77faab883b",
    "cm2-gate5-physical-prefix-kac-norm-frontier-manifest-2026-07-16.json": "64f3820e2dc2f6d544be94bbe205fcf08f9517eef29131311e6fafa295060a93",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
}
EXPECTED_VERDICT = {
    "C24_normalized_collision_SRB_mass_strict_upper_29021_over_75000000": "CERTIFIED",
    "measurable_mod_null_first_return_payload": "CERTIFIED",
    "common_Borel_forward_reverse_restriction_schema": "CERTIFIED",
    "singular_zero_and_Kac_survivor_outer_mass": "CERTIFIED",
    "geometric_full_dimensional_Rn_Qn_payload": "NOT_CERTIFIED",
    "q_weighted_exponential_tail": "NOT_CERTIFIED",
    "induced_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED",
    "Gate5": "NOT_CERTIFIED",
}
Q = Fraction


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


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_equal(left: Any, right: Any) -> bool:
    return canonical_json(left) == canonical_json(right)


def exact_key_set(value: Any, keys: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == keys


def result_digest(result: dict[str, Any]) -> str:
    payload = copy.deepcopy(result)
    payload.pop("internal_replay_digest", None)
    return digest(payload)


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(manifest["result"])


def verify_frozen_paths() -> list[str]:
    errors: list[str] = []
    paths = {CERTIFICATE.name: EXPECTED_CERTIFICATE_SHA256, **EXPECTED_DEPENDENCIES}
    for name, expected in paths.items():
        path = HERE / name
        if not path.is_file():
            errors.append(f"missing frozen path: {name}")
        elif path.is_symlink() or path.resolve().parent != HERE:
            errors.append(f"unsafe frozen path: {name}")
        elif sha256_path(path) != expected:
            errors.append(f"frozen hash: {name}")
    return errors


def check_mass(mass: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(mass, dict):
        return ["mass type"]
    expected = {
        "lower": "147/550000",
        "upper": "29021/75000000",
        "raw_upper": "377273/156250000",
        "normalizer_lower": "156/25",
        "axis_witness": "2504000499/2500000000",
        "diagonal_witness": "100102851/100000000",
    }
    observed = {
        "lower": mass.get("normalized_core_mass_strict_lower"),
        "upper": mass.get("normalized_core_mass_strict_upper"),
        "raw_upper": mass.get("unnormalized_core_mass_strict_upper"),
        "normalizer_lower": mass.get("normalizer_strict_lower_using_pi_gt_3"),
        "axis_witness": mass.get("axis_squared_strict_witness"),
        "diagonal_witness": mass.get("diagonal_squared_strict_witness"),
    }
    if not strict_equal(observed, expected):
        errors.append("mass exact fractions")
    try:
        lower, upper = Q(observed["lower"]), Q(observed["upper"])
        if not lower < upper < Q(1, 2500):
            errors.append("mass strict interval")
        if Q(observed["axis_witness"]) <= 1 or Q(observed["diagonal_witness"]) <= 1:
            errors.append("derivative strict witnesses")
    except Exception:
        errors.append("mass fraction parse")
    if mass.get("normalized_core_mass_strict_upper_lt_1_over_2500") is not True:
        errors.append("mass 1/2500 flag")
    if mass.get("small_measure_alone_implies_open_hole_admissibility") is not False:
        errors.append("small-measure nonpromotion")
    census = mass.get("core_census", {})
    if census.get("axis_rectangle_count") != 8 or isinstance(census.get("axis_rectangle_count"), bool):
        errors.append("axis census")
    if census.get("diagonal_rectangle_count") != 16 or isinstance(census.get("diagonal_rectangle_count"), bool):
        errors.append("diagonal census")
    if census.get("source_obstacle_count_each") != {"G": 12, "W": 12}:
        errors.append("source census")
    return errors


def check_measurable(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["measurable payload type"]
    exact = {
        "source_atoms_partition_C_s_modulo_null": True,
        "target_atoms_partition_C_s_modulo_null": True,
        "all_preterminal_complement_guards_present_in_set_formula": True,
        "singular_orbit_cemetery_absolute_mass": "0",
        "nonreturning_absolute_mass": "0",
        "branch_masses_nonnegative": True,
        "absolute_mass_identity": "sum_{n>=1}m_s,n=mu_s(C_s)",
        "normalized_mass_identity": "sum_{n>=1}p_s,n=1",
        "collision_SRB_area_Jacobian_abs": "1",
        "log_collision_SRB_area_Jacobian_distortion": "0",
        "area_Jacobian_is_unstable_curve_Jacobian": False,
        "induced_L1_operator_norm": "1",
        "geometric_connected_branch_rows_materialized": 0,
        "numeric_exact_m_s_n_rows_materialized": 0,
        "stepwise_margin_rows_materialized": 0,
        "exponential_survivor_tail": "NOT_CERTIFIED",
    }
    for key, expected in exact.items():
        if key not in payload or not strict_equal(payload[key], expected):
            errors.append(f"measurable field: {key}")
    if payload.get("common_forward_reverse_restriction_schema_id") != EXPECTED_RESTRICTION_SCHEMA_ID:
        errors.append("restriction schema ID")
    for key in (
        "geometric_connected_branch_rows_materialized",
        "numeric_exact_m_s_n_rows_materialized",
        "stepwise_margin_rows_materialized",
    ):
        if isinstance(payload.get(key), bool):
            errors.append(f"boolean count: {key}")
    rows = payload.get("sample_absolute_survivor_outer_bounds")
    if not isinstance(rows, list) or len(rows) != 9:
        errors.append("survivor rows")
    else:
        horizons = [0, 1, 544, 648, 1530, 2018, 2584, 3741, 12108]
        if [row.get("n") for row in rows] != horizons:
            errors.append("survivor horizons")
        if rows[5].get("displayed_upper") != "29021/75000000":
            errors.append("2018 absolute tail")
        if rows[6].get("displayed_upper") != "1/2585":
            errors.append("tail crossover")
        if payload.get("sample_absolute_survivor_outer_bounds_sha256") != digest(rows):
            errors.append("survivor row digest")
    return errors


def check_seed_inventory(seed: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(seed, dict):
        return ["seed inventory type"]
    expected = {
        "selected_source_core_count": 24,
        "selected_source_component_level_count": 28,
        "completed_selected_source_field_count": 4,
        "component_local_seed_field_count": 2,
        "field5_universal_adapted_inverse_strict_upper": "144000/180337",
        "field5_universal_Euclidean_inverse_strict_upper": "27410400/180337",
        "field6_Holder_exponent": "1/3",
        "field6_canonical_curve_log_variation_strict_upper": "3/200000",
        "physical_Borel_prefix_suffix_TV_Linf_constant": "1",
        "one_collision_geometric_subcost": "204*2^B_s",
        "one_collision_log_Holder_constant": "52",
        "initial_C_mesh": "69986663973833932800",
        "these_payloads_attach_to_full_geometric_R_n_Q_n_branches": False,
        "completed_geometric_R_n_strong_field_slot_count": 0,
    }
    for key, expected_value in expected.items():
        if key not in seed or not strict_equal(seed[key], expected_value):
            errors.append(f"seed field: {key}")
    rows = seed.get("field_rows")
    if not isinstance(rows, list) or len(rows) != 18:
        errors.append("18 field rows")
    else:
        if [row.get("index") for row in rows] != list(range(1, 19)):
            errors.append("18 field indexes")
        if any(row.get("completed_on_geometric_R_n_branch_count") != 0 for row in rows):
            errors.append("geometric field promotion")
        if seed.get("field_rows_sha256") != digest(rows):
            errors.append("field row digest")
    return errors


def check_interface(frontier: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(frontier, dict):
        return ["interface type"]
    if frontier.get("required_interface_count") != 13 or isinstance(frontier.get("required_interface_count"), bool):
        errors.append("interface count")
    if frontier.get("interfaces_with_nontrivial_measurable_or_seed_payload") != 11:
        errors.append("partial interface count")
    if frontier.get("complete_geometric_strong_interface_count") != 0:
        errors.append("complete strong interface count")
    rows = frontier.get("records")
    if not isinstance(rows, list) or len(rows) != 13:
        errors.append("interface rows")
    else:
        if [row.get("index") for row in rows] != list(range(1, 14)):
            errors.append("interface indexes")
        if any(row.get("complete_strong_record") is not False for row in rows):
            errors.append("interface promotion")
        expected_fields = [
            "complete_collision_SRB_source_partition",
            "raw_first_return_branch_records",
            "all_preterminal_complement_guards",
            "homogeneity_and_hidden_recut_margins",
            "branch_source_mass_m_n",
            "unstable_Jacobian_and_inverse",
            "log_Jacobian_distortion_sum",
            "regular_standard_flux_dynamic_operator_costs",
            "common_fw_rev_restriction_id_and_carriers",
            "physical_four_term_Kac_typing",
            "singular_cemetery_and_survivor_outer_mass",
            "weighted_q_excursion_tail",
            "induced_common_space_contraction_coefficient",
        ]
        if [row.get("field") for row in rows] != expected_fields:
            errors.append("interface field order")
        if frontier.get("records_sha256") != digest(rows):
            errors.append("interface row digest")
    return errors


def check(manifest: Any) -> list[str]:
    errors: list[str] = []
    if not exact_key_set(manifest, {"schema", "certificate_sha256", "verifier_sha256", "dependencies", "result", "verdict"}):
        return ["manifest exact key set"]
    if manifest["schema"] != SCHEMA:
        errors.append("manifest schema")
    if manifest["certificate_sha256"] != EXPECTED_CERTIFICATE_SHA256:
        errors.append("certificate hash field")
    if manifest["verifier_sha256"] != sha256_path(Path(__file__)):
        errors.append("verifier hash")
    if not strict_equal(manifest["dependencies"], EXPECTED_DEPENDENCIES):
        errors.append("dependency table")
    errors.extend(verify_frozen_paths())

    result = manifest["result"]
    if not exact_key_set(result, {
        "schema", "provenance", "exact_C24_collision_SRB_mass_interval",
        "measurable_first_return_payload", "source_core_strong_seed_inventory",
        "induced_interface_maturity", "strict_nonpromotion", "internal_replay_digest",
    }):
        errors.append("result exact key set")
        return errors
    if result["schema"] != RESULT_SCHEMA:
        errors.append("result schema")
    if result["internal_replay_digest"] != result_digest(result):
        errors.append("result digest")
    if result["internal_replay_digest"] != EXPECTED_RESULT_DIGEST:
        errors.append("frozen result digest")
    provenance = {
        "dependency_sha256": EXPECTED_DEPENDENCIES,
        "old_artifacts_modified": False,
        "parameterwise_not_joint_parameter_measure": True,
        "typing_policy": "Borel_area_payload_is_not_unstable_strong_payload",
    }
    if not strict_equal(result["provenance"], provenance):
        errors.append("provenance")
    errors.extend(check_mass(result["exact_C24_collision_SRB_mass_interval"]))
    errors.extend(check_measurable(result["measurable_first_return_payload"]))
    errors.extend(check_seed_inventory(result["source_core_strong_seed_inventory"]))
    errors.extend(check_interface(result["induced_interface_maturity"]))
    expected_scope = {
        "small_core_measure_implies_open_hole_O1prime_O2": False,
        "Borel_level_sets_are_connected_geometric_branches": False,
        "invariant_area_Jacobian_is_unstable_curve_Jacobian": False,
        "symbolic_m_s_n_are_numeric_materialized_branch_masses": False,
        "common_Borel_restriction_schema_is_common_strong_carrier": False,
        "Kac_survivor_outer_bound_is_exponential_q_tail": False,
        "L1_operator_norm_one_is_strong_Lasota_Yorke_coefficient": False,
        "complete_18_field_operator_block_count": 0,
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
        "cm2_gate45_induced_strong_payload_frontier_cert_frozen", CERTIFICATE
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot create certificate import")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if Path(module.__file__).resolve() != CERTIFICATE.resolve():
        raise RuntimeError("certificate resolved path mismatch")
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate hash changed after import")
    if not strict_equal(module.DEPENDENCIES, EXPECTED_DEPENDENCIES):
        raise RuntimeError("certificate dependency table mismatch")
    return module


def self_test(manifest: dict[str, Any]) -> tuple[int, int]:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[Any, ...], value: Any) -> None:
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
    candidate = copy.deepcopy(manifest); candidate["unknown"] = True; mutations.append(candidate)
    candidate = copy.deepcopy(manifest); candidate["dependencies"]["../escape"] = "0" * 64; mutations.append(candidate)

    mass = ("result", "exact_C24_collision_SRB_mass_interval")
    mutate(mass + ("normalized_core_mass_strict_lower",), "148/550000")
    mutate(mass + ("normalized_core_mass_strict_upper",), "1/2500")
    mutate(mass + ("normalized_core_mass_strict_upper_lt_1_over_2500",), False)
    mutate(mass + ("axis_dtheta_dt_strict_upper",), "1")
    mutate(mass + ("axis_squared_strict_witness",), "1")
    mutate(mass + ("diagonal_dtheta_dt_strict_upper",), "7/5")
    mutate(mass + ("diagonal_squared_strict_witness",), "49/50")
    mutate(mass + ("unnormalized_core_mass_strict_upper",), "273/156250")
    mutate(mass + ("normalizer_strict_lower_using_pi_gt_3",), "88/7")
    mutate(mass + ("small_measure_alone_implies_open_hole_admissibility",), True)
    mutate(mass + ("core_census", "axis_rectangle_count"), 7)
    mutate(mass + ("core_census", "axis_rectangle_count"), True)
    mutate(mass + ("core_census", "diagonal_rectangle_count"), 17)
    mutate(mass + ("core_census", "source_obstacle_count_each", "G"), 11)

    measurable = ("result", "measurable_first_return_payload")
    mutate(measurable + ("source_atoms_partition_C_s_modulo_null",), False)
    mutate(measurable + ("target_atoms_partition_C_s_modulo_null",), False)
    mutate(measurable + ("all_preterminal_complement_guards_present_in_set_formula",), False)
    mutate(measurable + ("singular_orbit_cemetery_absolute_mass",), "unknown")
    mutate(measurable + ("nonreturning_absolute_mass",), "positive")
    mutate(measurable + ("absolute_mass_identity",), "<=")
    mutate(measurable + ("normalized_mass_identity",), "sum<1")
    mutate(measurable + ("common_forward_reverse_restriction_schema_id",), "restriction:swapped")
    mutate(measurable + ("forward_reverse_maps_are_mutual_inverses_modulo_singular_null",), False)
    mutate(measurable + ("collision_SRB_area_Jacobian_abs",), "2")
    mutate(measurable + ("area_Jacobian_is_unstable_curve_Jacobian",), True)
    mutate(measurable + ("induced_L1_operator_norm",), "<1")
    mutate(measurable + ("geometric_connected_branch_rows_materialized",), 1)
    mutate(measurable + ("geometric_connected_branch_rows_materialized",), False)
    mutate(measurable + ("numeric_exact_m_s_n_rows_materialized",), 1)
    mutate(measurable + ("stepwise_margin_rows_materialized",), 1)
    mutate(measurable + ("sample_absolute_survivor_outer_bounds", 5, "displayed_upper"), "3/4")
    mutate(measurable + ("sample_absolute_survivor_outer_bounds", 6, "n"), 2583)
    mutate(measurable + ("sample_absolute_survivor_outer_bounds", 6, "displayed_upper"), "29021/75000000")
    mutate(measurable + ("sample_absolute_survivor_outer_bounds_sha256",), "0" * 64)
    mutate(measurable + ("exponential_survivor_tail",), "CERTIFIED")

    seeds = ("result", "source_core_strong_seed_inventory")
    mutate(seeds + ("selected_source_core_count",), 23)
    mutate(seeds + ("selected_source_component_level_count",), 27)
    mutate(seeds + ("completed_selected_source_field_count",), 6)
    mutate(seeds + ("component_local_seed_field_count",), 4)
    mutate(seeds + ("field5_universal_adapted_inverse_strict_upper",), "1")
    mutate(seeds + ("field6_canonical_curve_log_variation_strict_upper",), "0")
    mutate(seeds + ("physical_Borel_prefix_suffix_TV_Linf_constant",), "<1")
    mutate(seeds + ("one_collision_geometric_subcost",), "1")
    mutate(seeds + ("these_payloads_attach_to_full_geometric_R_n_Q_n_branches",), True)
    mutate(seeds + ("completed_geometric_R_n_strong_field_slot_count",), 1)
    mutate(seeds + ("field_rows", 4, "completed_on_geometric_R_n_branch_count"), 1)
    mutate(seeds + ("field_rows_sha256",), "0" * 64)

    interface = ("result", "induced_interface_maturity")
    mutate(interface + ("required_interface_count",), 12)
    mutate(interface + ("required_interface_count",), True)
    mutate(interface + ("interfaces_with_nontrivial_measurable_or_seed_payload",), 13)
    mutate(interface + ("complete_geometric_strong_interface_count",), 1)
    mutate(interface + ("records", 0, "complete_strong_record"), True)
    mutate(interface + ("records", 0, "field"), "raw_first_return_branch_records")
    mutate(interface + ("records", 11, "measurable_or_seed_payload"), "CERTIFIED")
    mutate(interface + ("records_sha256",), "0" * 64)

    scope = ("result", "strict_nonpromotion")
    for key in (
        "small_core_measure_implies_open_hole_O1prime_O2",
        "Borel_level_sets_are_connected_geometric_branches",
        "invariant_area_Jacobian_is_unstable_curve_Jacobian",
        "symbolic_m_s_n_are_numeric_materialized_branch_masses",
        "common_Borel_restriction_schema_is_common_strong_carrier",
        "Kac_survivor_outer_bound_is_exponential_q_tail",
        "L1_operator_norm_one_is_strong_Lasota_Yorke_coefficient",
    ):
        mutate(scope + (key,), True)
    mutate(scope + ("complete_18_field_operator_block_count",), 1)
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(scope + ("Gate5",), "CERTIFIED")
    mutate(("verdict", "geometric_full_dimensional_Rn_Qn_payload"), "CERTIFIED")
    mutate(("verdict", "q_weighted_exponential_tail"), "CERTIFIED")
    mutate(("verdict", "Gate4"), "CERTIFIED")
    mutate(("verdict", "Gate5"), "CERTIFIED")

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
        print("ERROR: optimized Python rejected", file=sys.stderr)
        return 1
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--replay", action="store_true")
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
    if args.integrity_only or args.replay:
        print("REPLAY_AND_INTEGRITY: PASS")
        return 0
    print("C24_NORMALIZED_COLLISION_SRB_MASS_STRICT_UPPER: 29021/75000000")
    print("MEASURABLE_RETURN_LEVEL_PAYLOAD: CERTIFIED_MOD_NULL")
    print("GEOMETRIC_RN_STRONG_PAYLOAD: NOT_CERTIFIED")
    print("GATE4_GATE5: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
