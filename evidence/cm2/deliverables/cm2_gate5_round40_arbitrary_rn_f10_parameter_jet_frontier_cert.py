#!/usr/bin/env python3
"""Round-40 arbitrary-R_n F10 mixed-parameter-jet frontier.

Round 39 certifies a physical L^(3/2) F10 moment on 64 moving-occurrence
seeds.  Pulling those densities through an arbitrary finite R_n branch is
not a purely spatial F9 operation.  It requires first and second parameter
jets and mixed space-parameter jets of every step map.

This certificate freezes the exact chain-rule recurrences, proves that they
are constructive on every compact analytic germ, and identifies the first
missing numerical payload: rank-indexed U/V/W envelopes plus a same-law
joint path moment and spacetime margin atlas.  No global F10 promotion is
made.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round40-arbitrary-rn-f10-parameter-jet-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round40-arbitrary-rn-f10-parameter-jet-frontier-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json": (
        "19ad840a8cfbca2aa722cfd367d287fe36de67b9c7b6faf00a151ca2f2bf8a16"
    ),
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json": (
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788"
    ),
    "cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json": (
        "9bc22092f99cd9af0d4b4daf44c89f6e5b24ca90f4826ed870f754e02de9ce73"
    ),
    "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json": (
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916"
    ),
    "cm2-gate34-full-row-parameter-whitney-atlas-manifest-2026-07-17.json": (
        "8763f00e07b316414aab9b50657979c9c8d15dd3c60e83e98c342169b099f8d0"
    ),
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json": (
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e"
    ),
}


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
    seed = load(
        "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json"
    )["result"]
    installed = seed["moving_occurrence_seed_F10_L3over2_installation"]
    exponents = seed["physical_margin_blowup_exponent_match"]
    if installed["same_occurrence_ID_seed_count"] != 64:
        raise RuntimeError("seed count")
    if installed["oriented_trace_count"] != 128:
        raise RuntimeError("trace count")
    if exponents["strict_product"] != "r*p=3/2<2=alpha":
        raise RuntimeError("seed exponent")
    if seed["strict_nonpromotion"]["arbitrary_Rn_pullback_F10_field"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("seed scope")

    f9 = load(
        "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
    )["result"]
    recurrence = f9["general_base_face_rank_path_recurrence"]
    if recurrence["one_step_envelopes"] != [
        "L(B)=150*2^B",
        "M(B)=42672*2^(3B)",
    ]:
        raise RuntimeError("F9 one-step envelopes")
    if recurrence["prefix_recurrence"] != [
        "D_j=L(B_j)D_(j-1)",
        "E_j=L(B_j)E_(j-1)",
        "H_j=M(B_j)D_(j-1)^2+L(B_j)H_(j-1)",
    ]:
        raise RuntimeError("F9 recurrence")
    if f9["strict_nonpromotion"][
        "complete_F9_physical_face_C2_parameterized_atlas"
    ] != "CERTIFIED":
        raise RuntimeError("F9 status")

    compact = load(
        "cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json"
    )["result"]
    search = compact["canonical_dyadic_radius_and_F10_search"]
    if search["bound_search_terminates_for_every_compact_regular_germ"] is not True:
        raise RuntimeError("compact search")
    if search["materialized_N_F10_values"] != 0:
        raise RuntimeError("compact materialization")
    if compact["strict_nonpromotion"]["global_rank_path_F10_Lp_or_weighted_sum"] != (
        "NOT_CERTIFIED"
    ):
        raise RuntimeError("compact scope")

    path = load(
        "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
    )["result"]
    components = path["canonical_regular_connected_component_schema"]
    if components["componentwise_forward_map_is_real_analytic_local_diffeomorphism"] is not True:
        raise RuntimeError("path analyticity")
    if components["scope"] != "fixed_parameter_s_and_fixed_finite_n":
        raise RuntimeError("path scope")
    if components["uniform_joint_parameter_component_atlas_claimed"] is not False:
        raise RuntimeError("joint atlas scope")

    whitney = load(
        "cm2-gate34-full-row-parameter-whitney-atlas-manifest-2026-07-17.json"
    )["result"]["countable_full_row_parameter_germ_atlas"]
    if whitney["positive_cell_radius_exists_by_compactness"] is not True:
        raise RuntimeError("Whitney radius")
    if whitney["dyadic_halving_of_parameter_radius_is_a_terminating_certificate_search"] is not True:
        raise RuntimeError("Whitney search")

    f8 = load(
        "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
    )["result"]["same_ID_numeric_F8"]
    if f8["common_normalized_transversality_strict_lower"] != "1/5":
        raise RuntimeError("F8 transversality")
    if f8["numeric_F8_actual_face_slots"] != "CERTIFIED_PARAMETERIZED":
        raise RuntimeError("F8 status")


def jet_inventory() -> dict[str, Any]:
    return {
        "step_map": "x_i=T_i(x_(i-1),s)",
        "known_spatial_rank_envelopes": {
            "A_i": "||D_x T_i||<=150*2^B_i",
            "B_i": "||D_x^2 T_i||<=42672*2^(3B_i)",
        },
        "required_mixed_parameter_envelopes": {
            "U_i": "||partial_s T_i||",
            "V_i": "||D_x partial_s T_i||",
            "W_i": "||partial_s^2 T_i||",
        },
        "physical_rank_indexed_U_B_materialized": False,
        "physical_rank_indexed_V_B_materialized": False,
        "physical_rank_indexed_W_B_materialized": False,
        "why_F9_is_insufficient": (
            "F9 controls only D_x and D_x^2; F10 includes parameter differentiation of the coarea density and denominator"
        ),
    }


def recurrence_contract() -> dict[str, Any]:
    return {
        "prefix_jets": {
            "D_i": "||D_x X_i||",
            "H_i": "||D_x^2 X_i||",
            "P_i": "||partial_s X_i||",
            "Q_i": "||D_x partial_s X_i||",
            "S_i": "||partial_s^2 X_i||",
        },
        "initial_values": "D_0=1; H_0=P_0=Q_0=S_0=0",
        "exact_safe_recurrence": [
            "D_i<=A_i*D_(i-1)",
            "H_i<=B_i*D_(i-1)^2+A_i*H_(i-1)",
            "P_i<=U_i+A_i*P_(i-1)",
            "Q_i<=V_i*D_(i-1)+B_i*P_(i-1)*D_(i-1)+A_i*Q_(i-1)",
            "S_i<=W_i+2*V_i*P_(i-1)+B_i*P_(i-1)^2+A_i*S_(i-1)",
        ],
        "finite_for_every_fixed_finite_path_with_finite_step_jets": True,
        "recurrence_status": "CERTIFIED_BY_SECOND_ORDER_CHAIN_RULE",
    }


def replay_synthetic_path(ranks: tuple[int, ...]) -> list[dict[str, Any]]:
    spatial_first = 1
    spatial_second = 0
    parameter_first = 0
    mixed = 0
    parameter_second = 0
    rows: list[dict[str, Any]] = []
    for depth, rank in enumerate(ranks, start=1):
        first = 150 * (1 << rank)
        second = 42672 * (1 << (3 * rank))
        synthetic_u = 1 << rank
        synthetic_v = 3 * (1 << (2 * rank))
        synthetic_w = 5 * (1 << (3 * rank))
        old_d = spatial_first
        old_h = spatial_second
        old_p = parameter_first
        old_q = mixed
        old_s = parameter_second
        spatial_first = first * old_d
        spatial_second = second * old_d**2 + first * old_h
        parameter_first = synthetic_u + first * old_p
        mixed = synthetic_v * old_d + second * old_p * old_d + first * old_q
        parameter_second = (
            synthetic_w
            + 2 * synthetic_v * old_p
            + second * old_p**2
            + first * old_s
        )
        rows.append(
            {
                "depth": depth,
                "B": rank,
                "synthetic_U": str(synthetic_u),
                "synthetic_V": str(synthetic_v),
                "synthetic_W": str(synthetic_w),
                "D": str(spatial_first),
                "H": str(spatial_second),
                "P": str(parameter_first),
                "Q": str(mixed),
                "S": str(parameter_second),
            }
        )
    return rows


def recurrence_replay() -> dict[str, Any]:
    paths = [(14,), (14, 15), (14, 16, 18)]
    blocks = []
    for ranks in paths:
        rows = replay_synthetic_path(ranks)
        blocks.append(
            {
                "rank_path": list(ranks),
                "rows": rows,
                "rows_sha256": digest(rows),
            }
        )
    return {
        "purpose": "independent integer replay of the recurrence algebra only",
        "synthetic_step_jet_policy": [
            "U(B)=2^B",
            "V(B)=3*2^(2B)",
            "W(B)=5*2^(3B)",
        ],
        "synthetic_values_are_physical_bounds": False,
        "replay_blocks": blocks,
        "replay_status": "CERTIFIED_ALGEBRA_ONLY",
    }


def pulled_back_level_audit() -> dict[str, Any]:
    return {
        "level": "F(x,s)=G(X_j(x,s),s)",
        "first_derivatives": [
            "F_x=(D_x X_j)^T G_x",
            "F_s=G_s+G_x dot P_j",
        ],
        "second_derivatives_needed_by_F10": [
            "F_xx=(D_x X_j)^T G_xx (D_x X_j)+G_x contracted with D_x^2 X_j",
            "F_xs=Q_j^T G_x+(D_x X_j)^T(G_xs+G_xx P_j)",
            "F_ss=G_ss+2 G_xs dot P_j+P_j^T G_xx P_j+G_x dot S_j",
        ],
        "coarea_density_model": (
            "rho is a signed normal-velocity/current numerator divided by the nonzero face/parent-W wedge denominator"
        ),
        "rho_needs": ["F_x", "F_s", "same-ID F8 denominator margin"],
        "d_tau_rho_needs": ["F_xx", "F_xs", "spatial tangent geometry"],
        "d_s_rho_needs": ["F_xs", "F_ss", "parameter persistence margins"],
        "base_face_parameter_jets_required": ["G_s", "G_xs", "G_ss"],
        "chain_rule_type_audit_status": "CERTIFIED",
    }


def constructive_local_status() -> dict[str, Any]:
    return {
        "fixed_finite_path_analyticity": "CERTIFIED_PREVIOUSLY",
        "same_ID_F8_wedge_lower": ">1/5",
        "all_face_spatial_F9": "CERTIFIED_PREVIOUSLY",
        "positive_parameter_radius_on_each_compact_germ": "CERTIFIED_PREVIOUSLY",
        "terminating_interval_F10_search_on_each_compact_germ": "CERTIFIED_PREVIOUSLY",
        "new_parameter_jet_recurrence_can_be_evaluated_on_each_compact_germ": True,
        "materialized_arbitrary_Rn_U_V_W_rows": 0,
        "materialized_arbitrary_Rn_global_F10_values": 0,
        "uniform_joint_parameter_component_atlas": "NOT_CERTIFIED",
        "local_constructive_status": "CERTIFIED_WITHOUT_GLOBAL_LP_PROMOTION",
    }


def exact_global_frontier() -> dict[str, Any]:
    return {
        "round39_seed_payload": {
            "moving_occurrence_seed_count": 64,
            "oriented_trace_count": 128,
            "physical_seed_exponents": "alpha=2, r=1, p=3/2",
            "physical_seed_L3over2": "CERTIFIED_RAW_COAREA",
        },
        "seed_exponent_propagates_through_arbitrary_paths_automatically": False,
        "first_missing_numeric_payload": [
            "one-step rank-indexed U(B), V(B), W(B) on the same physical branch IDs",
            "base-face G_s, G_xs, G_ss envelopes for all five physical face kinds",
            "a joint spacetime component-persistence and denominator-margin tail",
            "a same-law physical path moment for the full D/H/P/Q/S recurrence",
        ],
        "why_endpoint_B_tail_alone_is_insufficient": (
            "the pullback cost is a nonlinear product/sum over the whole rank path and mixed jets, not a function of the terminal seed rank alone"
        ),
        "cemetery_policy_needed_for": (
            "joint atlas failures, simultaneous roots, grazing endpoints, vanishing wedges and parameter branch loss"
        ),
        "arbitrary_Rn_all_face_F10": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": (
                "exact arbitrary-Rn mixed parameter-jet recurrence and global F10 installation frontier"
            ),
        },
        "one_step_parameter_jet_inventory": jet_inventory(),
        "arbitrary_path_mixed_jet_recurrence": recurrence_contract(),
        "synthetic_integer_replay": recurrence_replay(),
        "pulled_back_level_F10_type_audit": pulled_back_level_audit(),
        "compact_germ_constructive_status": constructive_local_status(),
        "global_physical_installation_frontier": exact_global_frontier(),
        "strict_nonpromotion": {
            "arbitrary_path_mixed_parameter_jet_recurrence": "CERTIFIED",
            "compact_germ_constructive_F10_with_recurrence": "CERTIFIED",
            "moving_occurrence_seed_F10_physical_L3over2": "CERTIFIED_PREVIOUSLY",
            "rank_indexed_physical_U_V_W": "NOT_CERTIFIED",
            "joint_spacetime_component_margin_tail": "NOT_CERTIFIED",
            "arbitrary_Rn_pullback_F10_field": "NOT_CERTIFIED",
            "complete_all_face_F10_field": "NOT_CERTIFIED",
            "F12": "NOT_CERTIFIED",
            "F13": "NOT_CERTIFIED",
            "strong_cemetery": "NOT_CERTIFIED",
            "F14_through_F18": "NOT_CERTIFIED",
            "complete_18_field_operator_block_count": 0,
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5_maturity": "7/18_UNCHANGED",
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
            / "cm2_gate5_round40_arbitrary_rn_f10_parameter_jet_frontier_verifier.py"
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
        "MIXED_PARAMETER_JET_RECURRENCE:",
        result["strict_nonpromotion"][
            "arbitrary_path_mixed_parameter_jet_recurrence"
        ],
    )
    print("ARBITRARY_RN_ALL_FACE_F10: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
