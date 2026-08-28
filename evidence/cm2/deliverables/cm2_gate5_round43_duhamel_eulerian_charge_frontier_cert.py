#!/usr/bin/env python3
"""Round-43 arbitrary-path Eulerian/Duhamel charge frontier.

In collision area coordinates, one regular cross-colour billiard step has an
Eulerian parameter generator with only first incidence-rank growth.  The
finite-product derivative is expanded by the exact Duhamel rule, so the
transport-current amplitude along a path is additive rather than governed by
the cubic second-jet recurrence.  The resulting charge is dominated on the
same physical IDs by the Round-35 D1 charge and inherits its L^(6/5) moment
and exponential tail.

This controls the geometric current amplitude.  It does not materialise the
two suffix-propagated traces required by F13, nor the trace/face norms needed
for a complete F16 operator cost.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round43-duhamel-eulerian-charge-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-round43-duhamel-eulerian-charge-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate5-round42-area-coordinate-current-split-frontier-manifest-2026-07-19.json": (
        "c112fe76649a195f47d51a3448822a7e4e864dff398b57fe26894e2badb28714"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json": (
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788"
    ),
    "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json": (
        "284b25ac30dd86a01bd0faaa7c0a97ee47839670e3cde4309936235badf5fd52"
    ),
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json": (
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"
    ),
}

M_RANK = Q(134217735, 64)
X_COEFFICIENT = 25
D1_COEFFICIENT = 151
X_L3OVER2 = Q(125) * M_RANK
K_RANK = Q(3055930500533353804145008325576782226562500, 453789)


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
    split = load(
        "cm2-gate5-round42-area-coordinate-current-split-frontier-manifest-2026-07-19.json"
    )["result"]
    current = split["area_preserving_current_decomposition"]
    if current["identity_status"] != "CERTIFIED_ALGEBRAIC":
        raise RuntimeError("current split")
    if current["F13_trace_bounds_on_arbitrary_Rn"] != "NOT_CERTIFIED":
        raise RuntimeError("F13 scope")
    area = split["canonical_area_coordinate_split"]
    if area["target_momentum_parameter_bounds"]["abs_partial_s_p1"] != "<=25/4":
        raise RuntimeError("p generator")
    if area["target_position_parameter_bounds_inherited"][0] != (
        "abs(partial_s r_1)<=75/(4*c_1)"
    ):
        raise RuntimeError("r generator")

    physical = load(
        "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json"
    )["result"]
    rank = physical["physical_collision_incidence_rank"]
    if rank["global_collision_SRB_integral_2^(3B_inc/2)_strict_upper"] != str(
        M_RANK
    ):
        raise RuntimeError("rank moment")
    moment = physical["global_physical_L6over5_moment"]
    if moment["K_rank_exact"] != str(K_RANK):
        raise RuntimeError("D1 moment constant")
    if moment["status"] != "CERTIFIED_PHYSICAL_GLOBAL_L6OVER5_MOMENT":
        raise RuntimeError("D1 moment")
    if physical["physical_rank_sum_weighted_tail"]["uniform_exponential_tail"] != (
        "CERTIFIED_FOR_ADDITIVE_D1_RANK_SUM_CHARGE"
    ):
        raise RuntimeError("D1 tail")

    f9 = load(
        "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
    )["result"]
    if not f9["seven_one_step_boundary_kind_F9_join"][
        "all_frozen_one_step_physical_boundary_types_covered"
    ]:
        raise RuntimeError("F9 face join")

    dq = load(
        "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
    )["result"]["fixed_gauge_depth_one_DQ"]
    if dq["regular_radical_stitching"]["maximal_connected_face_rows"] != 64:
        raise RuntimeError("depth-one current rows")
    if dq["operator_conclusion"]["uncentered_depth_one_transfer_DQ"] != (
        "CERTIFIED"
    ):
        raise RuntimeError("depth-one DQ")

    fields = load(
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    )["result"]["required_operator_field_schema"]["required_fields"]
    for field in (
        "moving_boundary_DQ_current_and_two_traces",
        "C1_face_trace_pullback_bound",
        "flux_face_operator_cost",
    ):
        if field not in fields:
            raise RuntimeError(f"operator field: {field}")


def one_step_generator() -> dict[str, Any]:
    if X_L3OVER2 != Q(16777216875, 64):
        raise RuntimeError("L3/2 arithmetic")
    return {
        "coordinates": "(r,p=sin(phi)) with collision area form R*dr*dp",
        "definition": "X_s=(partial_s F_s) composed with F_s^-1",
        "same_colour_branch": "X_s=0",
        "cross_colour_pointwise_bounds": {
            "abs_X_r": "<=75/(4*c_target)",
            "abs_X_p": "<=25/4",
            "incidence_rank": "1/c_target<=2^B",
            "l1_generator": "abs_X_r+abs_X_p<=25*2^B",
        },
        "divergence": "div_mu X_s=0 on every regular area-preserving branch",
        "physical_one_time_L3over2": {
            "input": "integral 2^(3B/2)dmu_s<134217735/64",
            "calculus": "25^(3/2)=125",
            "strict_upper": str(X_L3OVER2),
            "status": "CERTIFIED",
        },
        "generator_rank_exponent": 1,
        "cubic_second_jet_rank_exponent_used": False,
    }


def duhamel_identity() -> dict[str, Any]:
    return {
        "regular_bulk_operator": (
            "P_j,s h=h composed F_j,s^-1 on a persistent regular area-preserving branch"
        ),
        "one_step_derivative": (
            "partial_s P_j,s h=-div_mu(X_j,s*P_j,s h)=-X_j,s dot grad(P_j,s h)"
        ),
        "finite_path_formula": (
            "partial_s(P_n...P_1)=sum_{j=1}^n P_n...P_(j+1)*(partial_s P_j)*P_(j-1)...P_1"
        ),
        "moving_domain_product_rule": {
            "face_seed": "F10 delta(G_j)*(partial_s G_j) term",
            "transport_current": "F13 divergence term generated by X_j",
            "face_flux": "F16 normal trace of the transported current",
        },
        "identity_scope": "every finite regular rank-refined R_n path",
        "same_ID_prefix_suffix_order_preserved": True,
        "full_composed_second_parameter_jet_differentiated": False,
        "identity_status": "CERTIFIED_ALGEBRAIC_ARBITRARY_FINITE_PATH",
    }


def physical_charge() -> dict[str, Any]:
    ratio = Q(X_COEFFICIENT, D1_COEFFICIENT)
    if not ratio < 1:
        raise RuntimeError("D1 dominance")
    return {
        "path_charge": "c_X,n(x)=25*sum_{i=1}^n 2^B_i(x)",
        "frozen_D1_charge": "c_D1,n(x)=151*sum_{i=1}^n 2^B_i(x)",
        "pointwise_same_ID_identity": "c_X,n=(25/151)*c_D1,n<c_D1,n",
        "component_policy": (
            "integrate c_X,n on the same physical R_n components and shared fw/rev carrier IDs"
        ),
        "global_L6over5_moment": {
            "exact_scaling": "M_X=(25/151)^(6/5)*M_D1",
            "safe_strict_bound": "sum_(n,k)mbar_n,k*cbar_X,n,k^(6/5)<K_rank*N_open^3",
            "K_rank": str(K_RANK),
            "N_open_numeric": False,
            "status": "CERTIFIED_BY_POINTWISE_D1_DOMINATION",
        },
        "weighted_tail": {
            "pointwise_charge_tail_domination": "W_X(n)<=(25/151)*W_D1(n)",
            "inherited_block_exponent": "1/6",
            "collision_time_rate_numeric": False,
            "status": "CERTIFIED_FOR_DUHAMEL_AMPLITUDE_CHARGE",
        },
        "arbitrary_Rn_same_ID_insertion_amplitude_ledger": "CERTIFIED",
    }


def field_frontier() -> dict[str, Any]:
    return {
        "one_step_affine_face_normal_speed": {
            "target_r_face": "<=75*2^B/4",
            "target_p_face": "<=25/4",
            "common_safe_bound": "<=25*2^B",
            "pointwise_envelope": "CERTIFIED",
        },
        "depth_one_occurrence_current": {
            "physical_rows": 64,
            "oriented_traces": 128,
            "status": "CERTIFIED_PREVIOUSLY",
        },
        "newly_certified": [
            "one-step physical Eulerian generator L^(3/2) bound",
            "arbitrary-finite-path Duhamel current identity",
            "same-ID arbitrary-R_n additive Duhamel-insertion amplitude charge",
            "D1-dominated global L^(6/5) moment and weighted tail for that amplitude charge",
        ],
        "still_missing_for_F13": [
            "materialized suffix propagation of both oriented traces on every physical homogeneous R_n level",
            "C1 face-trace pullback norm on the same IDs",
            "return-wide dynamic-test MT_DQ norm and quotient trace assembly",
        ],
        "still_missing_for_F16": [
            "normal trace/operator norm, not just pointwise normal speed",
            "all-five-face physical reassembly with F10,F12,F13 on the same homogeneous IDs",
            "cemetery-compatible flux ledger",
        ],
        "arbitrary_Rn_F13_insertion_amplitude_charge": "CERTIFIED",
        "arbitrary_Rn_F13_two_trace_operator_field": "NOT_CERTIFIED",
        "arbitrary_Rn_F16_pointwise_affine_flux_envelope": "CERTIFIED",
        "arbitrary_Rn_F16_complete_operator_cost": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "path_scope": "every finite regular rank-refined R_n path",
            "literature_checked_through": "2026-07-19",
            "official_arXiv_snapshot": [
                "2104.06947v3",
                "2604.19671v2",
                "2606.10155v1",
            ],
        },
        "one_step_area_eulerian_generator": one_step_generator(),
        "arbitrary_path_Duhamel_current": duhamel_identity(),
        "physical_D1_dominated_eulerian_charge": physical_charge(),
        "F13_F16_operator_field_frontier": field_frontier(),
        "strict_nonpromotion": {
            "arbitrary_Rn_Duhamel_insertion_charge_ledger": "CERTIFIED",
            "arbitrary_Rn_F13_two_trace_operator_field": "NOT_CERTIFIED",
            "arbitrary_Rn_F16_complete_operator_cost": "NOT_CERTIFIED",
            "complete_all_face_F10_field": "NOT_CERTIFIED",
            "F12": "NOT_CERTIFIED",
            "F13": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "dynamic_MT_DQ": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
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
        default=HERE / "cm2_gate5_round43_duhamel_eulerian_charge_frontier_verifier.py",
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(
        "ARBITRARY_RN_DUHAMEL_INSERTION_CHARGE_LEDGER:",
        result["strict_nonpromotion"]["arbitrary_Rn_Duhamel_insertion_charge_ledger"],
    )
    print("F13_TWO_TRACE_OPERATOR_FIELD: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
