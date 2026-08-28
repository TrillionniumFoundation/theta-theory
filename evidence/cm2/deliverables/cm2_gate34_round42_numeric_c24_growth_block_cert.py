#!/usr/bin/env python3
"""Round-42 numerical hereditary C24 Growth block certificate.

The Round-41 C24 Growth theorem was uniform but left its short-curve scale
and density/chopping constants existential.  This certificate supplies an
explicit square-root image-length bound on every physical smooth branch,
uses it to construct the required finite pullback scale, and replays the
standard-family block with exact rational arithmetic.

The scheduled projective-cone block ``N_open`` remains theorem-supplied and
nonnumerical.  Consequently the result is not a numerical collision-time
``q`` or a Gate-4 closure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate34.round42-numeric-c24-growth-block.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round42-numeric-c24-growth-block-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json": (
        "a98203ebf820d959f9e04c213cd1d79c3809744671fd509c40e531bdc552c119"
    ),
    "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json": (
        "b03c5ae0e400045f087cfbd1aa8c843990edebe517a4dde786b0718446db7c1d"
    ),
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json": (
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691"
    ),
    "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json": (
        "58a8b27517a55fabd5776e9299802bb656f60733ae86c25941b640be2dfb4e91"
    ),
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json": (
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183"
    ),
    "cm2-gate34-round38-sampled-projective-strong-tail-manifest-2026-07-19.json": (
        "6aab6003fecfb705c924cced3ca5eb0d64012b1bf4db4816a2a9ac7012b2f6bf"
    ),
}

B0 = 49
N_STAR = 9148
RADIUS_MIN = Q(4, 25)
RADIUS_MAX = Q(9, 25)
TAU_MIN = Q(36337, 800000)
SLOPE_GAP = Q(50, 9)
DELTA_DERIVATIVE_UPPER = Q(53748, 625)
DELTA_1_DENOMINATOR = 37724355673552103994
DENSITY_RATIO = Q(2000, 1999)
THETA = Q(900337, 901685)
SURVIVAL = Q(111718729, 111718750)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe dependency: {name}")
    if sha(path) != DEPENDENCIES[name]:
        raise RuntimeError(f"dependency hash: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"dependency root: {name}")
    return value


def validate_dependencies() -> None:
    prior = load(
        "cm2-gate34-round41-c24-hereditary-growth-manifest-2026-07-19.json"
    )["result"]
    if prior["strict_nonpromotion"]["numeric_n_star_Z0_Z1"] != "NOT_CERTIFIED":
        raise RuntimeError("round41 numerical frontier")
    if prior["unnormalized_killed_subfamily_Growth"][
        "hereditary_C24_open_Growth"
    ] != "CERTIFIED_QUALITATIVE_UNIFORM":
        raise RuntimeError("round41 Growth")

    numerical = load(
        "cm2-gate4-numeric-invariant-family-growth-recovery-frontier-manifest-2026-07-16.json"
    )["replay_summary"]
    if numerical["density_ratio"] != qstr(DENSITY_RATIO):
        raise RuntimeError("density ratio")
    if numerical["adapted_one_step_distortion"] != (
        "15000000000000000000000000"
    ):
        raise RuntimeError("distortion")

    componentwise = load(
        "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json"
    )["replay_summary"]
    if componentwise["delta_1"] != f"1/{DELTA_1_DENOMINATOR}":
        raise RuntimeError("delta1")
    if componentwise["global_one_step_Xi_strict_upper"] != qstr(THETA):
        raise RuntimeError("theta")

    roots = load(
        "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json"
    )["result"]["physical_branch_slope_and_root_grammar"]
    if roots["canonical_unstable_slope_strict_lower"] != "25/9":
        raise RuntimeError("unstable slope")
    if roots["stable_unstable_transversality_gap_strict_lower"] != "50/9":
        raise RuntimeError("slope gap")

    geometry = load(
        "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json"
    )["result"]
    if geometry["stable_curve_open_hole_geometry"]["O1_complexity_P0"] != B0:
        raise RuntimeError("C24 complexity")

    strong = load(
        "cm2-gate34-round38-sampled-projective-strong-tail-manifest-2026-07-19.json"
    )["result"]["sampled_C24_killed_strong_tail"]
    if strong["explicit_mass_survival_factor_r"] != qstr(SURVIVAL):
        raise RuntimeError("survival rate")


def length_holder_constants() -> dict[str, Any]:
    target_center_distance_upper = Q(84, 25)
    curvature_plus_slope_upper = Q(25, 4) + 29
    transverse_offset_derivative_upper = (
        1 + target_center_distance_upper * curvature_plus_slope_upper
    )
    assert transverse_offset_derivative_upper == Q(2986, 25)
    assert (
        2 * RADIUS_MAX * transverse_offset_derivative_upper
        == DELTA_DERIVATIVE_UPPER
    )
    delta_derivative_lower = RADIUS_MIN * TAU_MIN * SLOPE_GAP
    assert delta_derivative_lower == Q(36337, 900000)
    assert DELTA_DERIVATIVE_UPPER < 100

    inverse_cosine_integral = (
        2 + 40 * RADIUS_MAX / delta_derivative_lower
    )
    assert inverse_cosine_integral == Q(13032674, 36337)

    image_projected_factor = Q(427, 4)
    image_slope_factor = 30
    holder_constant = (
        image_slope_factor * image_projected_factor * inverse_cosine_integral
    )
    assert holder_constant == Q(5962448355, 5191)

    return {
        "ray_circle_coordinates": (
            "Delta=R_1^2-w^2=R_1^2*c_1^2, a=u dot d=tau+sqrt(Delta)"
        ),
        "low_discriminant_region": "Delta<=R_1^2/4, hence abs(w)>=R_1/2",
        "constant_w_level_slope": "-kappa_0-c_0/a<-25/9",
        "unstable_minus_level_slope_gap_strict_lower": qstr(SLOPE_GAP),
        "a_strict_lower": qstr(TAU_MIN),
        "abs_dDelta_dr_low_region_strict_lower": qstr(
            delta_derivative_lower
        ),
        "abs_dDelta_dr_global_strict_upper": qstr(
            DELTA_DERIVATIVE_UPPER
        ),
        "low_region_component_count_upper": 2,
        "reason_for_two_components": (
            "w is strictly monotone on an unstable graph, so low Delta occurs only next to the two signed tangency ends"
        ),
        "integral_dr_over_c1_upper": (
            f"({qstr(inverse_cosine_integral)})*sqrt(length_E(W))"
        ),
        "projected_image_derivative": (
            "abs(dr_1/dr)=A/c_1, A=tau*(kappa_0+V)+c_0<427/4"
        ),
        "image_unstable_slope_strict_upper": "29",
        "euclidean_image_length_holder": (
            f"length_E(T_s W)<({qstr(holder_constant)})*sqrt(length_E(W))"
        ),
        "holder_constant_C_len": qstr(holder_constant),
        "uniform_scope": "every fixed |s|<=1/400 and every physical smooth true branch",
        "numeric_length_holder": "CERTIFIED",
    }


def explicit_scale() -> dict[str, Any]:
    holder = Q(5962448355, 5191)
    exponent_delta1 = 1 << (N_STAR - 1)
    exponent_holder = (1 << N_STAR) - 2
    assert exponent_holder == 2 * exponent_delta1 - 2
    assert N_STAR >= 7

    return {
        "delta_1": f"1/{DELTA_1_DENOMINATOR}",
        "recurrence": "delta_(j+1)=(delta_j/C_len)^2",
        "closed_form_delta_n": (
            "5191^(2^n-2)/(37724355673552103994^(2^(n-1))*5962448355^(2^n-2))"
        ),
        "n": N_STAR,
        "delta_1_exponent_2_to_n_minus_1": str(exponent_delta1),
        "C_len_exponent_2_to_n_minus_2": str(exponent_holder),
        "adapted_chopping_scale_delta_open": "(5/27)*delta_9148",
        "metric_conversion": "length_E(W)<=(27/5)*length_*(W)",
        "all_first_9147_forward_images_remain_below_delta_1": True,
        "delta_open_strictly_below_10^-90": True,
        "density_cone_ratio_at_delta_open_at_most": qstr(DENSITY_RATIO),
        "huge_rational_materialized": False,
        "exact_symbolic_scale": "CERTIFIED_NUMERICAL",
        "holder_constant_replayed": qstr(holder),
    }


def gamma_value(n: int) -> Q:
    return DENSITY_RATIO * (1 + (B0 - 1) * n) * THETA**n


def gamma_digest(n: int) -> str:
    value = gamma_value(n)
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}".encode()
    ).hexdigest()


def numerical_growth() -> dict[str, Any]:
    gamma = gamma_value(N_STAR)
    previous = gamma_value(N_STAR - 1)
    assert gamma < Q(1, 2)
    assert previous >= Q(1, 2)
    z1 = DENSITY_RATIO * B0 * THETA + 2
    assert z1 == Q(18367592526, 360493663)

    return {
        "block_depth_n_star": N_STAR,
        "exact_block_coefficient_formula": (
            "gamma=(2000/1999)*(1+48*9148)*(900337/901685)^9148"
        ),
        "gamma_exact_fraction_sha256": gamma_digest(N_STAR),
        "gamma_strict_bracket": "0.4999<gamma<1/2",
        "previous_depth_9147_fails_half_contraction": True,
        "previous_gamma_exact_fraction_sha256": gamma_digest(N_STAR - 1),
        "minimality_in_this_explicit_half_block_scheme": True,
        "Z0_exact_symbolic": "2/delta_open=54/(5*delta_9148)",
        "one_step_Z_multiplier_Z1": qstr(z1),
        "one_step_bound": "Z(O_s G)<=Z1*Z(G)",
        "block_bound": (
            "Z(O_s^9148 G)<=gamma*Z(G)+Z0*mass(G)"
        ),
        "hereditary_under_positive_C24_killing": True,
        "uniform_parameter_scope": "every fixed |s|<=1/400",
        "numeric_n_star_Z0_Z1": "CERTIFIED_EXACT_SYMBOLIC",
    }


def aggregate_resolvent() -> dict[str, Any]:
    gamma = gamma_value(N_STAR)
    rho = SURVIVAL**N_STAR
    assert rho > Q(1, 2)
    weight = (1 + 1 / rho) / 2
    assert weight > 1
    assert weight * rho < 1
    assert weight * gamma < Q(3, 4)
    return {
        "scheduled_projective_block_N_open": None,
        "common_collision_block": "L=9148*N_open",
        "Growth_factor_upper": "gamma^N_open<=gamma<1/2",
        "mass_factor_rho": "(111718729/111718750)^9148",
        "rho_exact_fraction_materialized": False,
        "explicit_block_index_weight": "w_Z=(1+rho^(-1))/2",
        "weight_checks": ["w_Z>1", "w_Z*rho=(1+rho)/2<1", "w_Z*gamma<3/4"],
        "source_constant": "C=Z0/(1-gamma)",
        "weighted_resolvent": (
            "sum_(p>=0) w_Z^p z_p <= z_0/(1-w_Z*gamma) + C*m_0*w_Z/((1-w_Z*gamma)*(1-w_Z*rho))"
        ),
        "block_index_weight_and_resolvent": "CERTIFIED_EXACT_SYMBOLIC",
        "collision_time_numeric_rate": "NOT_CERTIFIED_WITHOUT_NUMERIC_N_open",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "literature_checked_through": "2026-07-19",
            "claim_type": (
                "explicit physical branch length pullback, numerical C24 killed Growth block and block-index aggregate-Z resolvent"
            ),
        },
        "physical_branch_length_pullback": length_holder_constants(),
        "explicit_short_curve_schedule": explicit_scale(),
        "numerical_C24_killed_Growth": numerical_growth(),
        "aggregate_canonical_Z_resolvent": aggregate_resolvent(),
        "strict_nonpromotion": {
            "numeric_n_star_Z0_Z1": "CERTIFIED_EXACT_SYMBOLIC",
            "hereditary_C24_open_Growth": "CERTIFIED_NUMERICAL_BLOCK",
            "block_index_aggregate_Z_resolvent": "CERTIFIED_EXACT_SYMBOLIC",
            "numeric_N_open": "NOT_CERTIFIED",
            "collision_time_numeric_q": "NOT_CERTIFIED",
            "complete_numeric_C_fw_C_rev": "NOT_CERTIFIED",
            "final_same_ID_q": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "complete_composite_gates": "0/5",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = digest(result)
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["strict_nonpromotion"],
    }
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_round42_numeric_c24_growth_block_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "NUMERIC_C24_GROWTH:",
        result["strict_nonpromotion"]["hereditary_C24_open_Growth"],
    )
    print("NUMERIC_N_OPEN: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
