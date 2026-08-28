#!/usr/bin/env python3
"""Fail-closed verifier for the round-28 weighted-tail transfer frontier."""

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
SCHEMA = "cm2.gate45.round28-weighted-tail-transfer-frontier.manifest.v1"
RESULT_SCHEMA = "cm2.gate45.round28-weighted-tail-transfer-frontier.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate45_round28_weighted_tail_transfer_frontier_cert.py"
EXPECTED_CERTIFICATE_SHA256 = (
    "3ccbb8ca0f24ffab813d07d4304f16d5f92bba298337882f32d243a48beac6cc"
)
EXPECTED_RESULT_DIGEST = (
    "ae14d9ee49e3bdc0dcb6704a8f5c714c8140877f08d25f86b2a3c801a1af3548"
)
EXPECTED_DEPENDENCIES = {
    "cm2-gate34-c24-sparse-hit-gap-manifest-2026-07-18.json": (
        "02277a2c10ea905fd8a4cf9998ae364a4b024087624fd3bea0a8a4175405727d"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate45-round27-q2-branch-payload-frontier-manifest-2026-07-18.json": (
        "f846df9e0afe3e81bedb9cb1a4cb80446d8b79eabb9fd6577e223f6aa1e282ab"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate4-product-same-occurrence-joint-moment-frontier-manifest-2026-07-16.json": (
        "67db1ec8aead4cbb0ff966e9136508636690074acb5959a6d705893eeef00eff"
    ),
    "cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json": (
        "20f595ed4bcf62cb5cc5c89c22ab31a3ca039f43fff29fd35855673dc970b4a2"
    ),
    "cm2-gate45-induced-strong-coefficient-obstruction-manifest-2026-07-18.json": (
        "bad4bd8c12bccdcfad7210d44ed85fb023615c6db7aca9954e815a4729ce31e6"
    ),
}
EXPECTED_VERDICT = {
    "C24_first_return_mass_and_unweighted_tail_join": "CERTIFIED",
    "survivor_conditioned_Lp_weighted_tail_transfer": "CERTIFIED_CONDITIONAL_THEOREM",
    "global_Lp_weighted_tail_transfer": "CERTIFIED_CONDITIONAL_THEOREM",
    "pointwise_exponential_series_compatibility_threshold": "CERTIFIED_EXACT",
    "current_physical_first_return_transfer_hypothesis": "NOT_CERTIFIED",
    "current_strong_q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
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
    top_keys = {
        "schema",
        "certificate_sha256",
        "verifier_sha256",
        "dependencies",
        "result",
        "verdict",
    }
    if not exact_keys(data, top_keys):
        errors.append("manifest top-level key set")
    if data.get("schema") != SCHEMA:
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
        "first_return_mass_ledger_join",
        "weighted_tail_transfer_theorem",
        "current_frozen_stack_instantiation",
        "missing_first_return_strong_interface",
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

        provenance = result.get("provenance")
        expected_provenance = {
            "dependency_sha256": EXPECTED_DEPENDENCIES,
            "old_artifacts_modified": False,
            "audit_policy": "exact_manifest_join_plus_exact_rational_tail_transfer_lemmas",
            "parameter_quantifier": "uniformly_for_every_fixed_|s|<=1/400",
            "charge_typing": "one_physical_first_return_component_one_once_charged_q",
        }
        if not strict_equal(provenance, expected_provenance):
            errors.append("provenance")

        join = result.get("first_return_mass_ledger_join", {})
        expected_join = {
            "tail_prefactor_A": "550000/147",
            "tail_block_factor_r": "111718729/111718750",
            "tail_hit_gap_epsilon": "21/111718750",
            "N_open": "one_uniform_theorem_supplied_integer>=1_not_numeric",
            "singular_and_core_boundary_cemetery_collision_SRB_mass": "0",
            "regular_component_partition_exists_mod_null": True,
            "exact_nonempty_component_rows_enumerated": False,
            "numeric_arbitrary_n_component_masses_materialized": False,
            "finite_Q2_exact_mass_and_common_restriction_rows": 114006,
            "finite_Q2_symbolic_once_charged_rows": 114006,
            "finite_Q2_numeric_C_fw_rows": 0,
            "finite_Q2_numeric_C_rev_rows": 0,
            "finite_Q2_numeric_q_rows": 0,
            "finite_Q2_common_strong_recovery_carrier_rows": 0,
            "physical_first_return_q_density_rows_ready_for_tail_sum": 0,
        }
        if not isinstance(join, dict):
            errors.append("mass join type")
        else:
            for key, expected in expected_join.items():
                if join.get(key) != expected or type(join.get(key)) is not type(expected):
                    errors.append(f"mass join: {key}")
            if join.get("level_identity_mod_null") != "Q_(n-1)=R_n disjoint_union Q_n":
                errors.append("mass join telescope")

        theorem = result.get("weighted_tail_transfer_theorem", {})
        theorem_keys = {
            "definitions",
            "survivor_conditioned_Lp_transfer",
            "global_Lp_transfer",
            "pointwise_per_collision_exponential_transfer",
            "pointwise_per_block_exponential_transfer",
            "exact_compatibility_window",
        }
        if not exact_keys(theorem, theorem_keys):
            errors.append("transfer theorem key set")
        elif isinstance(theorem, dict):
            conditional = theorem["survivor_conditioned_Lp_transfer"]
            if conditional.get("status") != "CERTIFIED_CONDITIONAL_TRANSFER_THEOREM":
                errors.append("conditional Lp status")
            if conditional.get("conclusion") != "Wbar_n<K_p*A*r^floor(n/N_open)":
                errors.append("conditional Lp conclusion")
            global_lp = theorem["global_Lp_transfer"]
            if global_lp.get("status") != "CERTIFIED_CONDITIONAL_TRANSFER_THEOREM":
                errors.append("global Lp status")
            if global_lp.get("rate_effect") != "block_exponent_is_multiplied_by_1-1/p":
                errors.append("global Lp rate")
            pointwise = theorem["pointwise_per_collision_exponential_transfer"]
            if pointwise.get("series_route_compatibility") != "G^N_open*r<1 iff G<r^(-1/N_open)":
                errors.append("pointwise compatibility")
            if pointwise.get("necessity_scope") != (
                "compatibility is necessary only for this geometric upper-series route, not for the physical CM2 tail"
            ):
                errors.append("pointwise necessity scope")
            blockwise = theorem["pointwise_per_block_exponential_transfer"]
            if blockwise.get("series_route_compatibility") != "H*r<1 iff H<1/r":
                errors.append("block compatibility")
            window = theorem["exact_compatibility_window"]
            expected_window = {
                "r": "111718729/111718750",
                "epsilon_equals_1_minus_r": "21/111718750",
                "one_over_r": "111718750/111718729",
                "one_over_r_minus_one": "21/111718729",
                "exact_log_window": "21/111718750 < -log(r) < 21/111718729",
                "any_G_at_least_one_over_r_fails_the_series_condition_for_every_integer_N_open_at_least_1": True,
                "any_H_at_least_one_over_r_fails_the_block_series_condition": True,
                "every_integer_G_at_least_2_fails_the_series_condition": True,
                "numeric_N_open_needed_to_turn_r^(-1/N_open)_into_a_numeric_per_collision_threshold": True,
                "no_impossibility_claim_for_other_transfer_routes": True,
            }
            for key, expected in expected_window.items():
                if window.get(key) != expected or type(window.get(key)) is not type(expected):
                    errors.append(f"compatibility window: {key}")
            r = Q(111718729, 111718750)
            epsilon = Q(21, 111718750)
            reciprocal = Q(111718750, 111718729)
            if r != 1 - epsilon or r * reciprocal != 1:
                errors.append("exact compatibility arithmetic")
            if not (1 < reciprocal < Q(1000001, 1000000)):
                errors.append("reciprocal scale")

        stack = result.get("current_frozen_stack_instantiation", {})
        hypothesis = stack.get("new_transfer_hypothesis_status", {}) if isinstance(stack, dict) else {}
        expected_hypothesis = {
            "uniform_survivor_conditioned_Lp_first_return_envelope_count": 0,
            "global_Lp_physical_first_return_charge_envelope_count": 0,
            "compatible_pointwise_exponential_first_return_envelope_count": 0,
            "numeric_strong_cemetery_charge_rows": 0,
            "transfer_hypothesis_satisfied_by_current_frozen_stack": False,
        }
        if not strict_equal(hypothesis, expected_hypothesis):
            errors.append("current transfer hypothesis status")
        boundary = stack.get("strict_type_boundary", {}) if isinstance(stack, dict) else {}
        if boundary.get("product_fixed_finite_H_restart") != "CERTIFIED":
            errors.append("fixed H input")
        if boundary.get("product_arbitrary_or_unbounded_repeated_indicator_recovery") != "NOT_CERTIFIED":
            errors.append("unbounded recovery scope")
        if boundary.get("fixed_product_mark_is_a_physical_first_return_component_moment") is not False:
            errors.append("product/physical typing")
        if boundary.get("open_power_coefficient_is_an_induced_first_return_coefficient") is not False:
            errors.append("open/induced typing")

        missing = result.get("missing_first_return_strong_interface", {})
        rows = missing.get("rows") if isinstance(missing, dict) else None
        if missing.get("required_record_count") != 6:
            errors.append("missing record count")
        if missing.get("currently_complete_record_count") != 0:
            errors.append("complete missing records")
        if not isinstance(rows, list) or len(rows) != 6:
            errors.append("missing rows")
        else:
            if [row.get("index") for row in rows] != list(range(1, 7)):
                errors.append("missing row indices")
            if rows[0].get("record") != "nonempty_physical_first_return_component_rows":
                errors.append("first missing row")
            if rows[-1].get("record") != "induced_common_space_Lasota_Yorke_assembly":
                errors.append("last missing row")
            if missing.get("rows_sha256") != digest(rows):
                errors.append("missing rows digest")

        scope = result.get("strict_nonpromotion", {})
        expected_scope = {
            "conditional_transfer_theorem_implies_current_CM2_weighted_tail": False,
            "fixed_finite_H_product_restart_is_unbounded_physical_return_recovery": False,
            "unweighted_tail_plus_symbolic_q_implies_weighted_tail": False,
            "collision_null_cemetery_mass_alone_bounds_strong_cemetery_charge": False,
            "open_operator_coefficient_reused_as_induced_coefficient": False,
            "q_weighted_excursion_cemetery_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "complete_18_field_operator_blocks": 0,
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        }
        if not strict_equal(scope, expected_scope):
            errors.append("strict nonpromotion")

    if check_integrity:
        errors.extend(frozen_path_errors())
        verifier_sha = data.get("verifier_sha256")
        if not isinstance(verifier_sha, str) or verifier_sha != sha256_path(Path(__file__)):
            errors.append("verifier hash")
    return errors


def load_certificate() -> ModuleType:
    if sys.flags.optimize != 0:
        raise RuntimeError("optimized Python is forbidden")
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate changed before import")
    spec = importlib.util.spec_from_file_location("cm2_r28_weighted_tail_frozen", CERTIFICATE)
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
        actual_result = module.build_result()
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
    if not strict_equal(actual_result, data.get("result")):
        errors.append("certificate replay differs")
    if not strict_equal(actual_verdict, data.get("verdict")):
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
    if len(paths) < 70:
        return ["insufficient scalar mutation paths"], attempted
    for path in paths[:70]:
        bad = copy.deepcopy(data)
        parent, key = get_parent(bad["result"], path)
        parent[key] = hostile_value(parent[key])
        bad["result"]["internal_replay_digest"] = result_digest(bad["result"])
        attempted += 1
        if not validate(bad, check_integrity=True):
            failures.append("semantic mutation accepted: " + "/".join(map(str, path)))

    structural: list[tuple[str, dict[str, Any]]] = []
    bad = copy.deepcopy(data); bad["schema"] += "!"; structural.append(("schema", bad))
    bad = copy.deepcopy(data); bad["certificate_sha256"] = "0" * 64; structural.append(("certificate", bad))
    bad = copy.deepcopy(data); bad["verifier_sha256"] = "0" * 64; structural.append(("verifier", bad))
    bad = copy.deepcopy(data); bad["dependencies"][sorted(EXPECTED_DEPENDENCIES)[0]] = "f" * 64; structural.append(("dependency", bad))
    bad = copy.deepcopy(data); bad["verdict"]["Gate5"] = "CERTIFIED"; structural.append(("gate", bad))
    bad = copy.deepcopy(data); bad["unknown"] = 1; structural.append(("unknown-top-key", bad))
    bad = copy.deepcopy(data); bad["result"].pop("strict_nonpromotion"); structural.append(("missing-result-key", bad))
    bad = copy.deepcopy(data); bad["result"]["unknown"] = 1; structural.append(("unknown-result-key", bad))
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
    if attempted != 83:
        failures.append(f"hostile test count changed: {attempted}")
    return failures, attempted


def print_status() -> None:
    print("C24_FIRST_RETURN_MASS_AND_UNWEIGHTED_TAIL_JOIN: CERTIFIED")
    print("SURVIVOR_CONDITIONED_LP_TRANSFER: CERTIFIED_CONDITIONAL_THEOREM")
    print("GLOBAL_LP_TRANSFER: CERTIFIED_CONDITIONAL_THEOREM")
    print("POINTWISE_EXPONENTIAL_SERIES_THRESHOLD: CERTIFIED_EXACT")
    print("CURRENT_PHYSICAL_STRONG_Q_TAIL: NOT_CERTIFIED")
    print("INDUCED_STRONG_LASOTA_YORKE: NOT_CERTIFIED")
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
    print("LIVE_MODE: physical strong-q tail and induced coefficient remain open", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
