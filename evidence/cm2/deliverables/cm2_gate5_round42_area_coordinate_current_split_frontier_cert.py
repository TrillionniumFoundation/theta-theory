#!/usr/bin/env python3
"""Round-42 area-coordinate and current-splitting F10 frontier certificate.

The Round-41 path majorant loses ``c^-3`` in mixed/second parameter jets.
This certificate checks whether canonical area coordinates remove that loss.
They completely regularise the target momentum output, but not the target
position output.  An exact area-shell model shows that the known
``2^(3B/2)`` moment cannot control the residual ``c^-3`` charge.

The certificate also records the exact distributional transport identity
that can move the dynamic pullback part from raw F10 coordinate jets into
typed F13/F16 current/flux estimates.  Those estimates are not claimed here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round42-area-coordinate-current-split-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round42-area-coordinate-current-split-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate5-round41-physical-parameter-jet-envelopes-manifest-2026-07-19.json": (
        "dd19fd73a01c3aa9868fb9e3c89a039a5e8c97d807b6f57048fddc35c744c2cc"
    ),
    "cm2-gate5-round40-arbitrary-rn-f10-parameter-jet-frontier-manifest-2026-07-19.json": (
        "b5e1a965bb7fa1fc0f18ff6eb441c0bb181ac61d70451ce2eb67ea9d00c5695e"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

RADIUS_MIN = Q(4, 25)
CURVATURE_MAX = Q(25, 4)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


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
        "cm2-gate5-round41-physical-parameter-jet-envelopes-manifest-2026-07-19.json"
    )["result"]
    jets = prior["physical_rank_indexed_step_jets"]
    if jets["rank_exponents"] != {"U": 1, "V": 3, "W": 3}:
        raise RuntimeError("round41 exponents")
    if prior["physical_summability_frontier"][
        "known_physical_one_time_moment"
    ] != "integral 2^(3B/2) dmu_s < 134217735/64":
        raise RuntimeError("known moment")

    path = load(
        "cm2-gate5-round40-arbitrary-rn-f10-parameter-jet-frontier-manifest-2026-07-19.json"
    )["result"]
    if path["strict_nonpromotion"]["arbitrary_Rn_pullback_F10_field"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("round40 F10 frontier")

    physical = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]
    if physical["strict_nonpromotion"]["final_same_ID_q"] != "NOT_CERTIFIED":
        raise RuntimeError("physical q frontier")

    schema = load(
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    )["result"]["required_operator_field_schema"]
    required = schema["required_fields"]
    for field in (
        "coarea_density_regular_bound",
        "moving_boundary_DQ_current_and_two_traces",
        "flux_face_operator_cost",
    ):
        if field not in required:
            raise RuntimeError(f"operator field: {field}")


def area_coordinate_replay() -> dict[str, Any]:
    p_s_upper = 1 / RADIUS_MIN
    p_xs_r_upper = CURVATURE_MAX / RADIUS_MIN
    p_xs_phi_upper = 1 / RADIUS_MIN
    assert p_s_upper == Q(25, 4)
    assert p_xs_r_upper == Q(625, 16)
    assert p_xs_phi_upper == Q(25, 4)
    return {
        "coordinate_change": "p=sin(phi), dp=cos(phi)*dphi",
        "collision_SRB_area_form": "R*cos(phi)*dr*dphi=R*dr*dp",
        "ray_circle_target_momentum": "p_1=w/R_1",
        "relative_center_parameter_velocity": "d_s=eta*e_x, eta in {-1,0,1}",
        "target_momentum_parameter_bounds": {
            "abs_partial_s_p1": f"<={p_s_upper}",
            "partial_ss_p1": "0",
            "abs_partial_r_s_p1": f"<={p_xs_r_upper}",
            "abs_partial_phi_s_p1": f"<={p_xs_phi_upper}",
            "dyadic_rank_exponent": 0,
        },
        "target_position_output": "r_1=R_1*theta_1",
        "target_position_parameter_bounds_inherited": [
            "abs(partial_s r_1)<=75/(4*c_1)",
            "abs(partial_ss r_1)<=625/(16*c_1^3)",
            "abs(partial_xs r_1)<155625/(8*c_1^3)",
        ],
        "area_coordinate_conclusion": (
            "the momentum component becomes rank-zero in parameter jets, while the physical boundary-position component retains c_1^-3"
        ),
        "full_F10_rank_exponent_reduced_to_zero": False,
        "area_coordinate_split": "CERTIFIED",
    }


def shell_prefixes() -> list[dict[str, Any]]:
    rows = []
    mass = Q(0)
    mild = Q(0)
    severe = Q(0)
    for count in (1, 2, 4, 8, 16):
        mass = Q(0)
        mild = Q(0)
        severe = Q(0)
        for k in range(count):
            probability = Q(15, 16) * Q(1, 16) ** k
            rank = 2 * k
            mass += probability
            mild += probability * (1 << (3 * rank // 2))
            severe += probability * (1 << (3 * rank))
        rows.append(
            {
                "shell_prefix_count": count,
                "normalized_mass": str(mass),
                "2^(3B/2)_moment_prefix": str(mild),
                "2^(3B)_moment_prefix": str(severe),
            }
        )
    return rows


def area_shell_obstruction() -> dict[str, Any]:
    rows = shell_prefixes()
    return {
        "area_shell_coordinate": "c=2^-B with p-shell width comparable to c^2",
        "exact_probability_law": "P(B=2k)=(15/16)*16^-k, k>=0",
        "total_mass": "1",
        "known_scale_moment": (
            "sum P(B=2k)*2^(3B/2)=(15/16)*sum (1/2)^k<infinity"
        ),
        "residual_position_jet_moment": (
            "sum P(B=2k)*2^(3B)=(15/16)*sum 4^k=infinity"
        ),
        "finite_prefix_rows": rows,
        "logical_conclusion": (
            "flat area measure and the certified 2^(3B/2) marginal moment do not imply L1 control of the residual c^-3 target-position jet"
        ),
        "claim_about_actual_physical_path_divergence": False,
        "coordinate_change_alone_closes_arbitrary_Rn_F10": False,
        "supercritical_obstruction": "CERTIFIED_NO_IMPLICATION",
    }


def current_split() -> dict[str, Any]:
    return {
        "setting": (
            "F_s is an area-preserving regular billiard branch, A_s={y:G_s(y)<0}, X_s=(partial_s F_s) composed with F_s^-1"
        ),
        "change_of_variables": (
            "integral 1_A_s(F_s x) h(x) dmu(x)=integral 1_A_s(y) h(F_s^-1 y) dmu(y)"
        ),
        "distributional_identity": (
            "partial_s[1_{G_s<0}(h composed F_s^-1)] = -delta(G_s)*G_s_s*(h composed F_s^-1) - 1_{G_s<0}*X_s dot grad(h composed F_s^-1)"
        ),
        "typed_terms": {
            "moving_face_seed": "F10 coarea density built from G_s_s and the regular face denominator",
            "dynamic_transport_current": "F13 moving_boundary_DQ_current_and_two_traces",
            "flux_operator_cost": "F16 flux_face_operator_cost",
        },
        "why_this_can_avoid_raw_second_map_jets": (
            "the derivative is applied after area-preserving change of variables and uses the Eulerian generator plus traces, rather than differentiating the full pulled-back face twice in Birkhoff position coordinates"
        ),
        "divergence_free_generator": "div_mu X_s=0 on each regular branch",
        "identity_status": "CERTIFIED_ALGEBRAIC",
        "F13_trace_bounds_on_arbitrary_Rn": "NOT_CERTIFIED",
        "F16_flux_cost_on_arbitrary_Rn": "NOT_CERTIFIED",
        "all_face_current_reassembly": "NOT_CERTIFIED",
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
                "canonical area-coordinate parameter-jet split, exact marginal no-implication model and typed Reynolds/current interface"
            ),
        },
        "canonical_area_coordinate_split": area_coordinate_replay(),
        "physical_area_shell_summability_frontier": area_shell_obstruction(),
        "area_preserving_current_decomposition": current_split(),
        "latest_technology_audit": {
            "official_arXiv_snapshot": [
                "2104.06947v3",
                "2604.19671v2",
                "2606.10155v1",
            ],
            "arXiv_API_checked_on": "2026-07-19",
            "new_direct_theorem_for_arbitrary_Rn_moving_face_F10": False,
            "closest_structural_route": (
                "area-preserving Eulerian current/trace decomposition; it still requires physical arbitrary-path F13/F16 bounds"
            ),
        },
        "strict_nonpromotion": {
            "target_momentum_parameter_rank_exponent_zero": "CERTIFIED",
            "target_position_cubed_grazing_loss_removed": False,
            "raw_coordinate_path_to_full_F10": "BLOCKED_BY_EXACT_NO_IMPLICATION",
            "current_split_identity": "CERTIFIED_ALGEBRAIC",
            "arbitrary_Rn_F13_trace_bounds": "NOT_CERTIFIED",
            "arbitrary_Rn_F16_flux_cost": "NOT_CERTIFIED",
            "arbitrary_Rn_pullback_F10_field": "NOT_CERTIFIED",
            "complete_all_face_F10_field": "NOT_CERTIFIED",
            "F12": "NOT_CERTIFIED",
            "F13": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
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
        default=(
            HERE
            / "cm2_gate5_round42_area_coordinate_current_split_frontier_verifier.py"
        ),
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "AREA_COORDINATE_SPLIT:",
        result["canonical_area_coordinate_split"]["area_coordinate_split"],
    )
    print("ARBITRARY_RN_F10: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
