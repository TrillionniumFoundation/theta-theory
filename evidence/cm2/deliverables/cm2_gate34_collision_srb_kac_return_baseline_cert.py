#!/usr/bin/env python3
"""Collision-SRB Kac baseline for the frozen union of 24 physical cores.

This certificate applies Poincare recurrence and the general (not necessarily
ergodic) Kac formula to the finite Borel union C_s of the 24 compact physical
cores.  It freezes an aggregate, parameterwise collision-SRB mass identity,
an exact first-moment upper bound, and the resulting Markov tail bound.

It deliberately does not materialize first-return branches, produce a
q-weighted or exponential excursion tail, or construct the CM2 strong
induced operator.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
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

CORE_MASS_STRICT_LOWER = Q(147, 550000)
MEAN_STRICT_UPPER = 1 / CORE_MASS_STRICT_LOWER
SAMPLE_HORIZONS = (0, 1, 544, 648, 1530, 2018, 3741, 12108)


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


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


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency path: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        value = parse_json_text(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency JSON type: {name}")
        loaded[name] = value

    core = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]
    core_registry = core["result"]["physical_return_core_registry"]
    require(
        core["verdict"]["positive_mass_physical_core_registry"] == "CERTIFIED",
        "positive core mass not certified",
    )
    require(core_registry["physical_compact_homogeneous_core_count"] == 24, "core count")
    require(
        core_registry["collision_SRB_normalized_mass_strict_lower_using_pi_lt_22_over_7"]
        == qstr(CORE_MASS_STRICT_LOWER),
        "core mass lower",
    )
    require(core_registry["mass_lower_bound_sums_only_pairwise_disjoint_core_domains"] is True, "core disjointness")
    require(core_registry["all_cores_uniform_on_full_parameter_window"] is True, "core uniformity")

    finite = loaded[
        "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
    ]["result"]["uniform_configuration_and_recovery"]
    require(
        finite["compact_configuration_path"]["parameter_window"] == "|s|<=1/400",
        "parameter window",
    )
    require(
        finite["solid_section_typing"]["map_used"]
        == "T_s=F_{K_s,K_s} in the canonical fixed-configuration gauge",
        "fixed configuration map",
    )
    require(
        finite["solid_section_typing"]["section"]
        == "N=G disjoint-union W, the usual solid-boundary collision section",
        "solid collision section",
    )

    gauge = loaded[
        "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
    ]["result"]["fixed_gauge_depth_one_DQ"]["common_fixed_gauge"]
    require(
        gauge["invariant_probability"]
        == "the same normalized cos(phi)dr dphi for every s",
        "invariant probability",
    )
    require(
        gauge["collision_space"]
        == "N=G disjoint-union W in common arclength coordinates",
        "collision space",
    )

    path = loaded[
        "cm2-gate2-collision-key-stable-quotient-frontier-manifest-2026-07-16.json"
    ]["result"]["full_mass_2d_path_key_schema"]
    require(
        path["regular_collision_step_key_coverage"]
        == "1 modulo collision-SRB null set",
        "regular collision coverage",
    )
    require(
        path["path_key_grammar"]["singular_orbit_cemetery"]
        == "countable union of grazing/corner preimages; collision-SRB null",
        "singular orbit null set",
    )

    local = loaded[
        "cm2-gate34-local-core-return-tail-manifest-2026-07-18.json"
    ]
    require(
        local["verdict"]["full_24_core_induced_operator"] == "NOT_CERTIFIED",
        "local return nonpromotion",
    )
    require(
        local["result"]["strict_nonpromotion"][
            "labelled_coordinate_fraction_is_collision_SRB_probability"
        ]
        is False,
        "local coordinate fraction typing",
    )
    return loaded


def tail_bound_row(n: int) -> dict[str, Any]:
    require(isinstance(n, int) and not isinstance(n, bool) and n >= 0, "horizon")
    rational = MEAN_STRICT_UPPER / (n + 1)
    if rational < 1:
        displayed = rational
        relation = "strictly_less_than"
        reason = "Markov_plus_strict_mean_upper"
    else:
        displayed = Q(1)
        relation = "less_than_or_equal_to"
        reason = "probability_cap;_Markov_rational_bound_is_larger_than_one"
    return {
        "n": n,
        "normalized_survivor_event": "mu_C_s{tau_C_s_plus>n}",
        "displayed_upper": qstr(displayed),
        "relation": relation,
        "uncapped_strict_Markov_upper": qstr(rational),
        "reason": reason,
    }


def frozen_measure_contract(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    core = loaded[
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    ]["result"]["physical_return_core_registry"]
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
        "core_rows_sha256": core["rows_sha256"],
        "normalized_core_mass_strict_lower": qstr(CORE_MASS_STRICT_LOWER),
        "normalized_core_mass_positive": True,
        "hypotheses_bound_for_Poincare_and_general_Kac": True,
        "ergodicity_used": False,
    }


def kac_baseline() -> dict[str, Any]:
    require(CORE_MASS_STRICT_LOWER > 0, "positive core mass")
    require(CORE_MASS_STRICT_LOWER * MEAN_STRICT_UPPER == 1, "reciprocal")
    rows = [tail_bound_row(n) for n in SAMPLE_HORIZONS]
    require(rows[5]["n"] == 2018 and rows[5]["displayed_upper"] == "1", "2018 cap")
    require(rows[-1]["displayed_upper"] != "1", "12108 nontrivial bound")
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
        "normalized_first_moment_strict_upper": qstr(MEAN_STRICT_UPPER),
        "normalized_first_moment_finite": True,
        "tail_sum_identity": (
            "sum_{n>=0}mu_C_s{tau_C_s_plus>n}=E_mu_C_s[tau_C_s_plus]"
        ),
        "tail_sum_strict_upper": qstr(MEAN_STRICT_UPPER),
        "all_horizon_Markov_statement": (
            "for_integer_n>=0:_mu_C_s{tau_C_s_plus>n}"
            "<=E_mu_C_s[tau_C_s_plus]/(n+1)"
            "<550000/(147*(n+1))"
        ),
        "sample_horizon_rows": rows,
        "sample_horizon_rows_sha256": canonical_digest(rows),
        "exact_fraction_witness": {
            "core_mass_strict_lower": qstr(CORE_MASS_STRICT_LOWER),
            "reciprocal_strict_mean_upper": qstr(MEAN_STRICT_UPPER),
            "product_of_rational_bounds": qstr(
                CORE_MASS_STRICT_LOWER * MEAN_STRICT_UPPER
            ),
            "strictness_reason": (
                "mu_s(C_s)>147/550000_so_1/mu_s(C_s)<550000/147"
            ),
        },
    }


def measurable_induced_l1_baseline() -> dict[str, Any]:
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


def build_result() -> dict[str, Any]:
    loaded = load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.collision-srb-kac-return-baseline.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "proof_basis": (
                "frozen_collision_measure_and_core_registry_plus_"
                "Poincare_recurrence_and_general_Kac_formula"
            ),
            "parameterwise_not_joint_parameter_measure": True,
        },
        "frozen_measure_space_contract": frozen_measure_contract(loaded),
        "collision_srb_kac_baseline": kac_baseline(),
        "measurable_induced_L1_baseline": measurable_induced_l1_baseline(),
        "strict_nonpromotion": {
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
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("COLLISION_SRB_FIRST_RETURN_MASS_IDENTITY: CERTIFIED")
    print("NORMALIZED_FIRST_MOMENT_STRICT_UPPER: 550000/147")
    print("MEASURABLE_INDUCED_L1_BASELINE: CERTIFIED")
    print("Q_WEIGHTED_EXPONENTIAL_TAIL_AND_STRONG_INDUCED_OPERATOR: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
