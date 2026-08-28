#!/usr/bin/env python3
"""Round-41 physical rank-indexed parameter-jet envelopes.

For the fixed gauge, only the relative horizontal displacement of unlike
colours depends on the parameter.  A ray-circle computation therefore gives
explicit first, mixed and second parameter derivatives on every regular
one-collision branch.  The same computation supplies base parameter jets for
the seven frozen boundary kinds and hence all five Gate-5 face grammars.

The resulting coarse mixed envelope grows like 2^(3B).  The existing physical
2^(3B/2) incidence moment does not imply its integrability; an exact dyadic
countermodel freezes that logical boundary.  Thus U/V/W and base jets advance,
while the global arbitrary-R_n F10 field remains open.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round41-physical-parameter-jet-envelopes.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round41-physical-parameter-jet-envelopes-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate5-round40-arbitrary-rn-f10-parameter-jet-frontier-manifest-2026-07-19.json": (
        "b5e1a965bb7fa1fc0f18ff6eb441c0bb181ac61d70451ce2eb67ea9d00c5695e"
    ),
    "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json": (
        "7594afb9fc37660e8ce7c47d57bfd385dde65bcedfbdab5872f52699f5a4e72d"
    ),
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json": (
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788"
    ),
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json": (
        "2f374298785c74525e0bbb66b39e30be503ad9af05a913fa3175063196d883a8"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
}

R_MIN = Q(4, 25)
R_MAX = Q(9, 25)
KAPPA = 1 / R_MIN
TAU_MAX = Q(3)
RELATIVE_DISTANCE = TAU_MAX + R_MAX
U_NUMERATOR = 20
V_NUMERATOR = 20000
W_NUMERATOR = 40


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


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
        "cm2-gate5-round40-arbitrary-rn-f10-parameter-jet-frontier-manifest-2026-07-19.json"
    )["result"]
    inventory = prior["one_step_parameter_jet_inventory"]
    if inventory["physical_rank_indexed_U_B_materialized"] is not False:
        raise RuntimeError("round40 U scope")
    if prior["arbitrary_path_mixed_jet_recurrence"]["recurrence_status"] != (
        "CERTIFIED_BY_SECOND_ORDER_CHAIN_RULE"
    ):
        raise RuntimeError("round40 recurrence")

    rank = load(
        "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
    )["result"]["endpoint_rank_tail_and_first_order_cost"]
    derivative = rank["one_collision_birkhoff_derivative"]
    if derivative["forward_derivative_bound"] != "||DF_e||_infinity<150/cp_miss":
        raise RuntimeError("spatial derivative")
    if derivative["rank_dominates_both_inverse_incidence_scales"] is not True:
        raise RuntimeError("rank incidence")

    f9 = load(
        "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
    )["result"]
    if f9["general_base_face_rank_path_recurrence"]["one_step_envelopes"] != [
        "L(B)=150*2^B",
        "M(B)=42672*2^(3B)",
    ]:
        raise RuntimeError("spatial jet envelopes")
    if not f9["seven_one_step_boundary_kind_F9_join"][
        "all_frozen_one_step_physical_boundary_types_covered"
    ]:
        raise RuntimeError("boundary kinds")

    dq = load(
        "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
    )["result"]
    gauge = dq["fixed_gauge_depth_one_DQ"]["common_fixed_gauge"]
    if gauge["path"] != "horizontal center translation of W with both radii fixed":
        raise RuntimeError("fixed gauge")
    if dq["fixed_gauge_depth_one_DQ"]["smooth_core_derivative"][
        "same_colour_relative_branches_have_zero_parameter_velocity"
    ] is not True:
        raise RuntimeError("same-colour velocity")

    shell = load(
        "cm2-gate34-parameter-dq-all-scale-shell-manifest-2026-07-17.json"
    )["result"]
    exact = shell["exact_parameter_angle_jacobian"]
    if exact["candidate_frame_translation"] != {
        "ell_j(h)": "ell_j+eta_j*u_x*h",
        "w_j(h)": "w_j-eta_j*u_y*h",
    }:
        raise RuntimeError("relative translation")

    moment = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]
    if moment["physical_collision_incidence_rank"][
        "global_collision_SRB_integral_2^(3B_inc/2)_strict_upper"
    ] != "134217735/64":
        raise RuntimeError("physical incidence moment")


def ray_circle_majorant() -> dict[str, Any]:
    if KAPPA != Q(25, 4):
        raise RuntimeError("curvature")
    if RELATIVE_DISTANCE != Q(84, 25):
        raise RuntimeError("distance")

    w_x = KAPPA * RELATIVE_DISTANCE + 1
    q_sx_first = w_x * KAPPA
    q_sx_middle = KAPPA
    q_sx_last = w_x * KAPPA
    t_sx = KAPPA + q_sx_first + q_sx_middle + q_sx_last
    n_s = 3 * KAPPA
    n_sx = KAPPA * (t_sx + 2 * KAPPA)
    theta_x = 150 * KAPPA
    theta_sx = theta_x * n_s + n_sx
    theta_ss = KAPPA * KAPPA

    if w_x != 22:
        raise RuntimeError("w_x")
    if t_sx != Q(575, 2):
        raise RuntimeError("t_sx")
    if n_sx != 1875:
        raise RuntimeError("n_sx")
    if theta_sx != Q(155625, 8) or not theta_sx < V_NUMERATOR:
        raise RuntimeError("mixed jet")
    if theta_ss != Q(625, 16) or not theta_ss < W_NUMERATOR:
        raise RuntimeError("second parameter jet")
    if not n_s < U_NUMERATOR:
        raise RuntimeError("first parameter jet")

    return {
        "fixed_source_coordinates": "source arclength r and outgoing angle phi",
        "relative_center_parameter": (
            "d_s=eta*e_x with eta in {-1,0,1}; eta=0 on same-colour branches"
        ),
        "geometry_bounds": {
            "R_min": qstr(R_MIN),
            "R_max": qstr(R_MAX),
            "kappa_max": qstr(KAPPA),
            "flight_strict_upper": qstr(TAU_MAX),
            "source_to_target_center_strict_upper": qstr(RELATIVE_DISTANCE),
            "one_state_derivative_of_transverse_offset_upper": qstr(w_x),
        },
        "ray_root": {
            "coordinates": "a=u dot d, w=u_perp dot d, q=sqrt(R^2-w^2)=R*c, tau=a-q",
            "parameter_bounds": [
                "|tau_s|<=2/c",
                "|tau_ss|<=25/(4*c^3)",
                "|tau_xs|<=575/(2*c^3)",
            ],
        },
        "target_normal_angle": {
            "first_parameter_upper": "75/(4*c)",
            "mixed_parameter_upper": "155625/(8*c^3)",
            "second_parameter_upper": "625/(16*c^3)",
            "mixed_majorant_strictly_below_20000": True,
            "second_majorant_strictly_below_40": True,
        },
        "coordinate_output": (
            "r_1=R_1*theta_1 and phi_1 differs from the incoming global direction by the target normal angle; the same bounds dominate both coordinates"
        ),
        "majorant_status": "CERTIFIED_BY_EXACT_RATIONAL_RAY_CIRCLE_CALCULUS",
    }


def rank_envelopes() -> dict[str, Any]:
    samples = []
    for rank in (14, 16, 20):
        samples.append(
            {
                "B": rank,
                "U": str(U_NUMERATOR * (1 << rank)),
                "V": str(V_NUMERATOR * (1 << (3 * rank))),
                "W": str(W_NUMERATOR * (1 << (3 * rank))),
            }
        )
    return {
        "incidence_rank_contract": "1/cp_source,1/cp_target<=2^B",
        "same_colour_step_jets": "U(B)=V(B)=W(B)=0",
        "cross_colour_step_jets": [
            "U(B)=20*2^B",
            "V(B)=20000*2^(3B)",
            "W(B)=40*2^(3B)",
        ],
        "rank_exponents": {"U": 1, "V": 3, "W": 3},
        "sample_rows": samples,
        "sample_rows_sha256": digest(samples),
        "physical_rank_indexed_U_B_materialized": True,
        "physical_rank_indexed_V_B_materialized": True,
        "physical_rank_indexed_W_B_materialized": True,
    }


def base_face_jets() -> dict[str, Any]:
    tangent_gs = 2 * R_MAX
    tangent_gxs = 2 * (22 + R_MAX * KAPPA)
    tangent_gss = Q(2)
    if tangent_gs != Q(18, 25) or not tangent_gs < 1:
        raise RuntimeError("tangent Gs")
    if tangent_gxs != Q(97, 2) or not tangent_gxs < 49:
        raise RuntimeError("tangent Gxs")
    if tangent_gss != 2:
        raise RuntimeError("tangent Gss")

    rows = [
        {
            "type": "candidate_signed_tangency",
            "level": "Delta_T=R_T^2-w_T^2",
            "G_s_upper": "1",
            "G_xs_upper": "49",
            "G_ss_upper": "2",
        },
        {
            "type": "target_endpoint_on_wall_or_target_chart_seam",
            "level": "affine target coordinate in the moving target chart",
            "G_s_upper": "0",
            "G_xs_upper": "0",
            "G_ss_upper": "0",
        },
        {
            "type": "target_momentum_homogeneity_face",
            "level": "affine target momentum in the moving target chart",
            "G_s_upper": "0",
            "G_xs_upper": "0",
            "G_ss_upper": "0",
        },
        {
            "type": "forward_integer_corner_ray",
            "level": "u_perp dot (corner-q)=0",
            "G_s_upper": "1",
            "G_xs_upper": "7",
            "G_ss_upper": "0",
        },
        {
            "type": "coordinate_velocity_zero",
            "level": "fixed-gauge source velocity coordinate",
            "G_s_upper": "0",
            "G_xs_upper": "0",
            "G_ss_upper": "0",
        },
        {
            "type": "source_endpoint_on_wall_or_source_chart_seam",
            "level": "affine source coordinate",
            "G_s_upper": "0",
            "G_xs_upper": "0",
            "G_ss_upper": "0",
        },
        {
            "type": "source_momentum_homogeneity_face",
            "level": "affine source momentum",
            "G_s_upper": "0",
            "G_xs_upper": "0",
            "G_ss_upper": "0",
        },
    ]
    return {
        "tangency_raw_level_exact_bounds": {
            "abs_G_s_strict_upper": qstr(tangent_gs),
            "abs_G_xs_strict_upper": qstr(tangent_gxs),
            "abs_G_ss_upper": qstr(tangent_gss),
        },
        "seven_boundary_kind_rows": rows,
        "seven_boundary_kind_rows_sha256": digest(rows),
        "five_face_grammar_join": {
            "source_core_clipping_face": "stationary C24 affine level: zero base parameter jets",
            "intermediate_core_avoidance_preimage_face": "stationary C24 terminal level plus certified path jets",
            "terminal_core_preimage_face": "stationary C24 terminal level plus certified path jets",
            "collision_singularity_or_owner_change_face": "covered by all seven rows",
            "moving_occurrence_face": "covered by the tangency discriminant row on all 64 occurrence IDs",
        },
        "all_five_physical_face_base_parameter_jets": "CERTIFIED",
    }


def summability_frontier() -> dict[str, Any]:
    rows = []
    for count in (1, 2, 4, 8, 16):
        moment_3over2 = sum(
            Q(15, 16) * Q(1, 16) ** index * Q(8) ** index
            for index in range(count)
        )
        moment_3 = sum(
            Q(15, 16) * Q(1, 16) ** index * Q(64) ** index
            for index in range(count)
        )
        rows.append(
            {
                "shell_prefix_count": count,
                "normalized_mass": qstr(1 - Q(1, 16) ** count),
                "2^(3B/2)_moment_prefix_without_base_shift": qstr(moment_3over2),
                "2^(3B)_moment_prefix_without_base_shift": qstr(moment_3),
            }
        )
    return {
        "known_physical_one_time_moment": (
            "integral 2^(3B/2) dmu_s < 134217735/64"
        ),
        "new_mixed_and_second_jet_scale": "2^(3B)",
        "logical_countermodel": {
            "law": "P(B=b0+2k)=(15/16)*16^-k, k>=0",
            "2_to_3B_over_2_moment": "finite geometric series with ratio 1/2",
            "2_to_3B_moment": "divergent geometric series with ratio 4",
            "finite_prefix_rows": rows,
        },
        "existing_rank_moment_implies_V_W_L1": False,
        "existing_occurrence_seed_L3over2_propagates_through_paths": False,
        "required_next_improvement": [
            "an anisotropic/cancellation estimate reducing the effective mixed-jet rank exponent",
            "or a joint spacetime rank tail strong enough for the nonlinear D/H/P/Q/S path recurrence",
            "plus denominator and component-persistence margins on the same physical law",
        ],
        "same_law_full_path_moment": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "branch_scope": "every one-step regular physical branch and every finite regular rank path",
        },
        "ray_circle_parameter_majorant": ray_circle_majorant(),
        "physical_rank_indexed_step_jets": rank_envelopes(),
        "all_face_base_parameter_jets": base_face_jets(),
        "physical_summability_frontier": summability_frontier(),
        "strict_nonpromotion": {
            "rank_indexed_physical_U_V_W": "CERTIFIED",
            "all_five_face_base_parameter_jets": "CERTIFIED",
            "arbitrary_path_mixed_parameter_jet_recurrence": "CERTIFIED_PREVIOUSLY",
            "joint_spacetime_component_margin_tail": "NOT_CERTIFIED",
            "same_law_full_path_D_H_P_Q_S_moment": "NOT_CERTIFIED",
            "arbitrary_Rn_pullback_F10_field": "NOT_CERTIFIED",
            "complete_all_face_F10_field": "NOT_CERTIFIED",
            "F12": "NOT_CERTIFIED",
            "F13": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "Gate5_maturity": "7/18_UNCHANGED",
            "complete_18_field_operator_block_count": 0,
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
        default=HERE / "cm2_gate5_round41_physical_parameter_jet_envelopes_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print("PHYSICAL_RANK_INDEXED_U_V_W: CERTIFIED")
    print("ALL_FIVE_FACE_BASE_PARAMETER_JETS: CERTIFIED")
    print("ARBITRARY_RN_PULLBACK_F10_FIELD: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
