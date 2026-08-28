#!/usr/bin/env python3
"""Uniform sparse-block hit gap and unweighted C24 return tail.

The preceding open-hole leaf certified the large-hole geometry but stopped
before an unnormalised mass-loss statement.  This follow-up installs that
missing scalar by testing each recovered density against one explicit global
C1 bump supported strictly inside the G:E axial core.

Demers--Liverani Lemma 8.8 / Proposition 8.7 first recover a killed density
into a fixed enlarged cone.  Additional closed mixing, via Theorem 7.3,
makes its normalized integral against the bump uniformly close to the SRB
integral of the bump.  Hence every sufficiently separated opening loses a
fixed positive fraction.  All-time C24 avoidance is a subset of scheduled
avoidance, which gives a uniform, qualitative collision-time exponential
return tail with an existential block length and an explicit per-block loss.

No branchwise q weight, numerical block length, full return partition, or
induced strong Lasota--Yorke coefficient is claimed.
"""

from __future__ import annotations

import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


Q = Fraction
HERE = Path(__file__).resolve().parent

DEPENDENCIES = {
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json": (
        "1213a6b66fca6d3a776a75244c334dacfeb822240f7c7eeadcb565553e62a53a"
    ),
    "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json": (
        "098f9f52580fbb71d2416b07330aefa4f67488115f000bb60d37eec521250625"
    ),
}

CORE_MASS_STRICT_LOWER = Q(147, 550000)
BUMP_MASS_STRICT_LOWER = Q(21, 55859375)
HIT_GAP = BUMP_MASS_STRICT_LOWER / 2
BLOCK_SURVIVAL_FACTOR = 1 - HIT_GAP


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
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def load_dependencies() -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency: {name}")
        require(sha256_path(path) == expected, f"dependency hash: {name}")
        value = parse_json_text(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency type: {name}")
        loaded[name] = value

    geometry = loaded[
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    ]
    require(
        geometry["verdict"]["C24_O1_O1prime_O2_open_hole_geometry"]
        == "CERTIFIED",
        "open-hole geometry",
    )
    require(
        geometry["verdict"][
            "C24_sparse_opening_cone_recovery_theorem_admission"
        ]
        == "CERTIFIED_QUALITATIVE",
        "sparse theorem admission",
    )
    mass = geometry["result"]["collision_SRB_core_mass_interval"]
    require(mass["normalized_core_mass_strict_lower"] == "147/550000", "mass lower")
    require(mass["normalized_core_mass_strict_upper_simplification"] == "1/2500", "mass upper")
    require(mass["normalized_core_mass_at_most_one_half"] is True, "mass half")
    stable = geometry["result"]["stable_curve_open_hole_geometry"]
    require(stable["O1_prime_complexity_P0"] == 49, "O1prime")
    require(stable["certified_O2_constant_Ct"] == 1493, "O2")

    kac = loaded[
        "cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json"
    ]
    require(
        kac["verdict"]["collision_SRB_first_return_mass_identity"] == "CERTIFIED",
        "Kac baseline",
    )
    require(
        kac["verdict"]["q_weighted_exponential_excursion_cemetery_tail"]
        == "NOT_CERTIFIED",
        "q-tail scope",
    )

    family = loaded[
        "cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json"
    ]["result"]["uniform_configuration_and_recovery"]
    require(family["compact_configuration_path"]["parameter_window"] == "|s|<=1/400", "parameter")
    require(family["compact_configuration_path"]["one_compact_SYZ_configuration_class"] is True, "compact family")
    require(
        family["solid_section_typing"]["configuration_sequence"]
        == "K_s,K_s,K_s,... (constant for each fixed s)",
        "constant sequence",
    )
    return loaded


def bump_witness() -> dict[str, Any]:
    center_t = Q(3, 200)
    half_t = Q(1, 250)
    half_p = Q(3, 2000)
    support_t = (center_t - half_t, center_t + half_t)
    support_p = (-half_p, half_p)
    require(support_t == (Q(11, 1000), Q(19, 1000)), "t support")
    require(Q(1, 100) < support_t[0] < support_t[1] < Q(1, 50), "strict t interior")
    require(-Q(1, 500) < support_p[0] < support_p[1] < Q(1, 500), "strict p interior")

    # u(x)=(1-x^2)^2 on [-1,1], zero outside.  Both u and u' vanish
    # at the endpoints, so the product bump is globally C1 after extension.
    one_dimensional_integral = Q(16, 15)
    radius_g = Q(9, 25)
    raw_lower = (
        radius_g * half_t * half_p * one_dimensional_integral**2
    )
    require(raw_lower == Q(24, 9765625), "raw bump mass")
    # dtheta/dt>=1 and total volume <4*(22/7)*(13/25).
    normalization_upper = 4 * Q(22, 7) * Q(13, 25)
    normalized_lower = raw_lower / normalization_upper
    require(normalized_lower == BUMP_MASS_STRICT_LOWER, "normalized bump mass")
    require(HIT_GAP == Q(21, 111718750), "hit gap")

    # |u'|<2.  In the G:E chart, |dt/dr|<1/R_G=25/9 and
    # |dp/dphi|<=1.  A conservative sum C1 norm is therefore <2724.
    dt_derivative = Q(2) / half_t
    dp_derivative = Q(2) / half_p
    dr_derivative = dt_derivative * Q(25, 9)
    c1_sum = 1 + dr_derivative + dp_derivative
    require(dt_derivative == 500, "t derivative")
    require(dp_derivative == Q(4000, 3), "p derivative")
    require(dr_derivative == Q(12500, 9), "r derivative")
    require(c1_sum == Q(24509, 9) < 2724, "C1 norm")

    return {
        "bump_id": "bump:C24:G:E:axis:center-3-over-200:v1",
        "chart": "G:E",
        "core_source_rectangle": {
            "t": ["1/100", "1/50"],
            "p": ["-1/500", "1/500"],
        },
        "support_rectangle": {
            "t": [qstr(support_t[0]), qstr(support_t[1])],
            "p": [qstr(support_p[0]), qstr(support_p[1])],
        },
        "scaled_coordinates": (
            "x=(t-3/200)/(1/250),_y=p/(3/2000)"
        ),
        "formula_on_support": "g=(1-x^2)^2*(1-y^2)^2",
        "formula_off_support": "g=0",
        "support_closure_strictly_inside_one_C24_core": True,
        "boundary_value_and_first_derivative_zero": True,
        "global_C1_on_collision_section": True,
        "pointwise_bounds": "0<=g<=1_C24<=1",
        "one_dimensional_polynomial_integral": qstr(one_dimensional_integral),
        "unnormalized_collision_SRB_integral_strict_lower": qstr(raw_lower),
        "normalized_collision_SRB_integral_strict_lower": qstr(
            normalized_lower
        ),
        "C1_norm_strict_upper": "2724",
        "same_bump_and_integral_bound_for_every_|s|<=1/400": True,
    }


def recovered_hit_gap() -> dict[str, Any]:
    require(BLOCK_SURVIVAL_FACTOR == Q(111718729, 111718750), "block factor")
    return {
        "base_cone": "C=C_{c,A,L}(delta)_from_Demers--Liverani",
        "pre_hole_density_contract": (
            "f>=0,_f_in_C,_integral(f)dmu_s=1"
        ),
        "hole_restriction": "h0=1_{C24^c}*f",
        "positive_surviving_mass": (
            "Lemma_8.8_equation_(8.7)_gives_a_strict_positive_lower_cone_"
            "seminorm_after_recovery"
        ),
        "large_hole_recovery": (
            "Lemma_8.8_and_Proposition_8.7:_there_is_a_uniform_existential_"
            "n_recover_with_L_s^n_recover(h0)_in_a_fixed_enlarged_cone_Cprime"
        ),
        "normalization": (
            "h=L_s^n_recover(h0)/integral(h0)dmu_s_is_in_Cprime_and_has_mass_1"
        ),
        "closed_mixing_comparison_density": "the_constant_invariant_density_1",
        "closed_mixing_theorem": (
            "Demers--Liverani_Theorem_7.3(b),_applied_in_Cprime_to_h_and_1"
        ),
        "test_observable": "the_global_C1_bump_g",
        "mixing_error_bound": (
            "|integral(g*L_s^m(h))dmu_s-integral(g)dmu_s|"
            "<=Cprime*vartheta_prime^m*|g|_C1"
        ),
        "uniform_existential_extra_mixing_time": (
            "choose_m_so_Cprime*vartheta_prime^m*2724"
            "<21/111718750"
        ),
        "combined_sparse_block_length": (
            "N_open_is_one_uniform_integer_large_enough_for_Proposition_8.7_"
            "base-cone_return_and_the_extra_Theorem_7.3_mixing"
        ),
        "numeric_N_open": None,
        "uniform_parameter_quantifier": "one_N_open_for_all_|s|<=1/400",
        "next_pre_hole_bump_mass_strict_lower": qstr(HIT_GAP),
        "next_pre_hole_C24_mass_strict_lower": qstr(HIT_GAP),
        "explicit_per_block_hit_gap_epsilon": qstr(HIT_GAP),
        "explicit_per_block_survival_factor": qstr(BLOCK_SURVIVAL_FACTOR),
        "induction_closure": (
            "Proposition_8.7_returns_every_normalized_block_output_to_the_"
            "same_base_cone_before_the_next_restriction"
        ),
        "all_theorem_constants_uniform_over_compact_s_family": True,
    }


def tail_result() -> dict[str, Any]:
    prefactor = (1 / CORE_MASS_STRICT_LOWER) / BLOCK_SURVIVAL_FACTOR
    require(prefactor == Q(61445312500000, 16422653163), "tail prefactor")
    return {
        "scheduled_opening_times": "N_open,2*N_open,3*N_open,...",
        "ambient_scheduled_survivor_bound": (
            "mu_s(intersection_{j=1}^k T_s^(-j*N_open)(C24^c))"
            "<(111718729/111718750)^k"
        ),
        "first_block_orientation": (
            "before_time_N_open_the_invariant_density_is_1,_so_the_first_"
            "scheduled_hit_mass_is_mu_s(C24)>147/550000>epsilon"
        ),
        "return_clock": "tau_C24_plus=inf{n>=1:T_s^n(x)_in_C24}",
        "all_time_avoidance_subset": (
            "{tau_C24_plus>n}_inside_{intersection_of_C24_at_time_0_and_"
            "C24^c_at_j*N_open,_1<=j<=floor(n/N_open)}"
        ),
        "normalized_core_return_tail": (
            "P_{mu_C24,s}(tau_C24_plus>n)"
            "<(550000/147)*(111718729/111718750)^floor(n/N_open)"
        ),
        "collision_time_exponential_form": {
            "rho_open": "(111718729/111718750)^(1/N_open)",
            "rho_open_strictly_between_zero_and_one": True,
            "A_open_rational_strict_upper": qstr(prefactor),
            "bound": "P_{mu_C24,s}(tau_C24_plus>n)<A_open*rho_open^n",
        },
        "uniform_unweighted_exponential_collision_return_tail": "CERTIFIED",
        "uniform_unweighted_positive_exponential_moment": (
            "CERTIFIED_FOR_EVERY_0<c<-log(rho_open)"
        ),
        "block_length_is_theorem_supplied_not_numerically_materialized": True,
    }


def strict_scope() -> dict[str, Any]:
    return {
        "C24_recovered_cone_explicit_hit_gap": "CERTIFIED",
        "C24_uniform_unweighted_exponential_return_tail": "CERTIFIED",
        "C24_numeric_sparse_block_length": "NOT_CERTIFIED",
        "C24_numeric_collision_time_rho": "NOT_CERTIFIED",
        "q_weighted_exponential_excursion_cemetery_tail": "NOT_CERTIFIED",
        "branch_materialized_2d_Rn_Qn_partition": "NOT_CERTIFIED",
        "branch_Jacobian_distortion_mass_q_payload": "NOT_CERTIFIED",
        "induced_common_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
        "common_fw_rev_strong_restriction": "NOT_CERTIFIED",
        "complete_18_field_operator_blocks": 0,
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }


def certify() -> dict[str, Any]:
    load_dependencies()
    result = {
        "schema": "cm2.gate34.c24-sparse-hit-gap.v1",
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "parameter_quantifier": "uniformly_for_all_|s|<=1/400",
            "theorem_source": (
                "Demers--Liverani,_Projective_cones_for_sequential_"
                "dispersing_billiards,_arXiv:2104.06947v3"
            ),
            "theorem_interfaces": [
                "Theorem_7.3(b)_closed_loss_of_memory_against_C1_tests",
                "Lemma_8.8_large-hole_recovery",
                "Proposition_8.7_sparse_opening_base-cone_return",
            ],
            "old_artifacts_modified": False,
        },
        "explicit_C1_bump": bump_witness(),
        "uniform_recovered_cone_hit_gap": recovered_hit_gap(),
        "scheduled_and_all_time_tail": tail_result(),
        "strict_scope": strict_scope(),
    }
    payload = copy.deepcopy(result)
    result["internal_replay_digest"] = canonical_digest(payload)
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("C24_RECOVERED_CONE_HIT_GAP_21_OVER_111718750: CERTIFIED")
    print("C24_UNIFORM_UNWEIGHTED_EXPONENTIAL_RETURN_TAIL: CERTIFIED")
    print("C24_NUMERIC_SPARSE_BLOCK_AND_NUMERIC_RHO: NOT_CERTIFIED")
    print("C24_Q_WEIGHTED_EXPONENTIAL_TAIL: NOT_CERTIFIED")
    print("GATE3_GATE4_GATE5: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
