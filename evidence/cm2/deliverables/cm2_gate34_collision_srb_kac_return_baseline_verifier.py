#!/usr/bin/env python3
"""Fail-closed verifier for the collision-SRB Kac return baseline."""

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
SCHEMA = "cm2.gate34.collision-srb-kac-return-baseline.manifest.v1"
RESULT_SCHEMA = "cm2.gate34.collision-srb-kac-return-baseline.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json"
)
CERTIFICATE = HERE / "cm2_gate34_collision_srb_kac_return_baseline_cert.py"
EXPECTED_CERTIFICATE_SHA256 = (
    "6f0e263385dc26af5882ad7d6d7f27b4fbf07b4efc8ce7277a6658afe6ce16fd"
)
EXPECTED_RESULT_DIGEST = (
    "9effb2e70f009a7a55d453ebbe4e4843ac52faacda43443afcc77f3d824f1320"
)
EXPECTED_DEPENDENCIES = {
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json": (
        "886c5feb8709ad26fd653e598edf344ba39cc3e08e6efbd02c9ad1133f784c65"
    ),
    "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json": (
        "d66c8da53846ae86c373de5917e706fa183bfca265f0e4fb83a9be1c204dd053"
    ),
}
EXPECTED_VERDICT = {
    "collision_SRB_first_return_mass_identity": "CERTIFIED",
    "normalized_first_return_first_moment_strict_upper_550000_over_147": (
        "CERTIFIED"
    ),
    "uniform_parameterwise_Markov_tail": "CERTIFIED",
    "measurable_induced_L1_operator_baseline": "CERTIFIED",
    "branch_materialized_24_core_induced_operator": "NOT_CERTIFIED",
    "q_weighted_exponential_excursion_cemetery_tail": "NOT_CERTIFIED",
    "induced_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
    "Gate3": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED",
    "Gate5": "NOT_CERTIFIED",
}
Q = Fraction
SAMPLE_HORIZONS = (0, 1, 544, 648, 1530, 2018, 3741, 12108)


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


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def expected_tail_rows() -> list[dict[str, Any]]:
    mean_upper = Q(550000, 147)
    rows = []
    for n in SAMPLE_HORIZONS:
        rational = mean_upper / (n + 1)
        if rational < 1:
            displayed = rational
            relation = "strictly_less_than"
            reason = "Markov_plus_strict_mean_upper"
        else:
            displayed = Q(1)
            relation = "less_than_or_equal_to"
            reason = "probability_cap;_Markov_rational_bound_is_larger_than_one"
        rows.append(
            {
                "n": n,
                "normalized_survivor_event": "mu_C_s{tau_C_s_plus>n}",
                "displayed_upper": qstr(displayed),
                "relation": relation,
                "uncapped_strict_Markov_upper": qstr(rational),
                "reason": reason,
            }
        )
    return rows


def expected_measure_contract() -> dict[str, Any]:
    return {
        "quantifier": "for_every_fixed_s_with_|s|<=1/400",
        "collision_space": "N=G disjoint-union W in common arclength coordinates",
        "physical_map": "T_s=F_{K_s,K_s}",
        "invariant_probability": "mu_s=normalized_cos(phi)dr_dphi=normalized_dr_dp",
        "same_probability_formula_for_every_s": True,
        "map_invertible_and_measure_preserving_modulo_singular_null_set": (
            "standard_collision_map_theorem_on_the_frozen_fixed_configuration"
        ),
        "regular_collision_step_coverage": "1_modulo_collision-SRB_null",
        "singular_orbit_cemetery": (
            "countable_union_of_grazing_or_corner_preimages;_mu_s-null"
        ),
        "core_union": "C_s=union_of_24_frozen_compact_physical_cores",
        "core_count": 24,
        "core_union_is_Borel": True,
        "core_domains_pairwise_disjoint_for_mass_sum": True,
        "core_rows_sha256": (
            "c3042515b4a244b064f1aaef97ee236c5d3f6078a53fe3fb9e865a1976853b2f"
        ),
        "normalized_core_mass_strict_lower": "147/550000",
        "normalized_core_mass_positive": True,
        "hypotheses_bound_for_Poincare_and_general_Kac": True,
        "ergodicity_used": False,
    }


def expected_kac_baseline() -> dict[str, Any]:
    rows = expected_tail_rows()
    return {
        "return_clock": "tau_C_s_plus=inf{n>=1:T_s^n(x)_in_C_s}",
        "Poincare_recurrence_on_C_s": "mu_C_s{tau_C_s_plus<infinity}=1",
        "singular_before_return_normalized_mass": "0",
        "nonreturning_normalized_mass": "0",
        "first_return_level_sets_pairwise_disjoint_modulo_null": True,
        "aggregate_first_return_mass_identity": (
            "sum_{n>=1}mu_s(C_s_intersection_{tau_C_s_plus=n})=mu_s(C_s)"
        ),
        "general_Kac_identity": (
            "integral_C_s(tau_C_s_plus)dmu_s=mu_s(saturation_T_s(C_s))<=1"
        ),
        "normalized_first_moment_relation": (
            "E_mu_C_s[tau_C_s_plus]=mu_s(saturation_T_s(C_s))/mu_s(C_s)"
        ),
        "normalized_first_moment_strict_upper": "550000/147",
        "normalized_first_moment_finite": True,
        "tail_sum_identity": (
            "sum_{n>=0}mu_C_s{tau_C_s_plus>n}=E_mu_C_s[tau_C_s_plus]"
        ),
        "tail_sum_strict_upper": "550000/147",
        "all_horizon_Markov_statement": (
            "for_integer_n>=0:_mu_C_s{tau_C_s_plus>n}"
            "<=E_mu_C_s[tau_C_s_plus]/(n+1)"
            "<550000/(147*(n+1))"
        ),
        "sample_horizon_rows": rows,
        "sample_horizon_rows_sha256": digest(rows),
        "exact_fraction_witness": {
            "core_mass_strict_lower": "147/550000",
            "reciprocal_strict_mean_upper": "550000/147",
            "product_of_rational_bounds": "1",
            "strictness_reason": (
                "mu_s(C_s)>147/550000_so_1/mu_s(C_s)<550000/147"
            ),
        },
    }


def expected_induced_l1() -> dict[str, Any]:
    return {
        "induced_map": "T_C_s(x)=T_s^tau_C_s_plus(x)(x)",
        "defined_mu_C_s_almost_everywhere": True,
        "preserves_normalized_restriction_mu_C_s": True,
        "measurable_Perron_operator_on_L1_mu_C_s_exists": True,
        "Perron_operator_positive": True,
        "Perron_operator_preserves_integrals": True,
        "L1_operator_norm": "1",
        "status": "CERTIFIED_MEASURE_THEORETIC_BASELINE",
        "not_a_branch_materialized_CM2_operator": True,
    }


def expected_scope() -> dict[str, Any]:
    return {
        "ergodicity_or_full_saturation_claimed": False,
        "exact_mean_equals_inverse_core_mass_claimed": False,
        "branch_materialized_R_n_Q_n": "NOT_CERTIFIED",
        "connected_first_return_partition": "NOT_CERTIFIED",
        "branch_Jacobian_distortion_mass_q_payload": "NOT_CERTIFIED",
        "q_weighted_excursion_or_cemetery_tail": "NOT_CERTIFIED",
        "exponential_collision_SRB_tail": "NOT_CERTIFIED",
        "Kac_Markov_tail_is_exponential": False,
        "Kac_Markov_tail_closes_CM2_strong_summability": False,
        "four_local_labelled_boxes_promoted_to_collision_SRB": False,
        "common_two_view_strong_space": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
        "complete_18_field_operator_blocks": 0,
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }


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


def check(manifest: Any) -> list[str]:
    errors: list[str] = []
    if not exact_key_set(
        manifest,
        {"schema", "certificate_sha256", "verifier_sha256", "dependencies", "result", "verdict"},
    ):
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
    if not exact_key_set(
        result,
        {
            "schema",
            "provenance",
            "frozen_measure_space_contract",
            "collision_srb_kac_baseline",
            "measurable_induced_L1_baseline",
            "strict_nonpromotion",
            "internal_replay_digest",
        },
    ):
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
        "proof_basis": (
            "frozen_collision_measure_and_core_registry_plus_"
            "Poincare_recurrence_and_general_Kac_formula"
        ),
        "parameterwise_not_joint_parameter_measure": True,
    }
    for key, expected, label in (
        ("provenance", provenance, "provenance"),
        ("frozen_measure_space_contract", expected_measure_contract(), "measure contract"),
        ("collision_srb_kac_baseline", expected_kac_baseline(), "Kac baseline"),
        ("measurable_induced_L1_baseline", expected_induced_l1(), "induced L1"),
        ("strict_nonpromotion", expected_scope(), "strict nonpromotion"),
    ):
        if not strict_equal(result[key], expected):
            errors.append(label)
    if not strict_equal(manifest["verdict"], EXPECTED_VERDICT):
        errors.append("verdict")
    return errors


def load_certificate() -> ModuleType:
    if sha256_path(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise RuntimeError("certificate hash changed before import")
    spec = importlib.util.spec_from_file_location(
        "cm2_gate34_collision_srb_kac_return_baseline_cert_frozen", CERTIFICATE
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


def refresh(manifest: dict[str, Any]) -> None:
    manifest["result"]["internal_replay_digest"] = result_digest(manifest["result"])


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
    candidate = copy.deepcopy(manifest)
    candidate["unknown"] = True
    mutations.append(candidate)
    candidate = copy.deepcopy(manifest)
    candidate["dependencies"]["../escape.json"] = "0" * 64
    mutations.append(candidate)

    contract = ("result", "frozen_measure_space_contract")
    mutate(contract + ("quantifier",), "exists_s")
    mutate(contract + ("core_count",), 23)
    mutate(contract + ("core_count",), True)
    mutate(contract + ("core_union_is_Borel",), False)
    mutate(contract + ("core_domains_pairwise_disjoint_for_mass_sum",), False)
    mutate(contract + ("normalized_core_mass_strict_lower",), "146/550000")
    mutate(contract + ("normalized_core_mass_positive",), False)
    mutate(contract + ("same_probability_formula_for_every_s",), False)
    mutate(contract + ("hypotheses_bound_for_Poincare_and_general_Kac",), False)
    mutate(contract + ("ergodicity_used",), True)
    mutate(contract + ("core_rows_sha256",), "0" * 64)

    kac = ("result", "collision_srb_kac_baseline")
    mutate(kac + ("nonreturning_normalized_mass",), "positive")
    mutate(kac + ("singular_before_return_normalized_mass",), "unknown")
    mutate(kac + ("first_return_level_sets_pairwise_disjoint_modulo_null",), False)
    mutate(kac + ("aggregate_first_return_mass_identity",), "<=mu_s(C_s)")
    mutate(kac + ("general_Kac_identity",), "integral=1")
    mutate(kac + ("normalized_first_moment_strict_upper",), "550000/146")
    mutate(kac + ("normalized_first_moment_finite",), False)
    mutate(kac + ("tail_sum_strict_upper",), "infinity")
    mutate(kac + ("all_horizon_Markov_statement",), "exponential")
    mutate(kac + ("sample_horizon_rows", 5, "displayed_upper"), "3/4")
    mutate(kac + ("sample_horizon_rows", 5, "relation"), "strictly_less_than")
    mutate(kac + ("sample_horizon_rows", 6, "n"), 3740)
    mutate(kac + ("sample_horizon_rows", 7, "displayed_upper"), "1/4")
    mutate(kac + ("sample_horizon_rows_sha256",), "0" * 64)
    mutate(kac + ("exact_fraction_witness", "core_mass_strict_lower"), "147/500000")
    mutate(kac + ("exact_fraction_witness", "reciprocal_strict_mean_upper"), "550000/146")
    mutate(kac + ("exact_fraction_witness", "product_of_rational_bounds"), "0")

    induced = ("result", "measurable_induced_L1_baseline")
    mutate(induced + ("defined_mu_C_s_almost_everywhere",), False)
    mutate(induced + ("preserves_normalized_restriction_mu_C_s",), False)
    mutate(induced + ("Perron_operator_preserves_integrals",), False)
    mutate(induced + ("L1_operator_norm",), "<1")
    mutate(induced + ("not_a_branch_materialized_CM2_operator",), False)

    scope = ("result", "strict_nonpromotion")
    mutate(scope + ("ergodicity_or_full_saturation_claimed",), True)
    mutate(scope + ("exact_mean_equals_inverse_core_mass_claimed",), True)
    mutate(scope + ("branch_materialized_R_n_Q_n",), "CERTIFIED")
    mutate(scope + ("q_weighted_excursion_or_cemetery_tail",), "CERTIFIED")
    mutate(scope + ("exponential_collision_SRB_tail",), "CERTIFIED")
    mutate(scope + ("Kac_Markov_tail_is_exponential",), True)
    mutate(scope + ("Kac_Markov_tail_closes_CM2_strong_summability",), True)
    mutate(scope + ("four_local_labelled_boxes_promoted_to_collision_SRB",), True)
    mutate(scope + ("induced_strong_Lasota_Yorke_coefficient",), "CERTIFIED")
    mutate(scope + ("complete_18_field_operator_blocks",), 14)
    mutate(scope + ("Gate4",), "CERTIFIED")
    mutate(scope + ("Gate5",), "CERTIFIED")
    mutate(("verdict", "q_weighted_exponential_excursion_cemetery_tail"), "CERTIFIED")
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
    print("COLLISION_SRB_FIRST_RETURN_MASS_IDENTITY: CERTIFIED")
    print("NORMALIZED_FIRST_MOMENT_STRICT_UPPER: 550000/147")
    print("MEASURABLE_INDUCED_L1_BASELINE: CERTIFIED")
    print("Q_WEIGHTED_EXPONENTIAL_TAIL_AND_STRONG_INDUCED_OPERATOR: NOT_CERTIFIED")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
