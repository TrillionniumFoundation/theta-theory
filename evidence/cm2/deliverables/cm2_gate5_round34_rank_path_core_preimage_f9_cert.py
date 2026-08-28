#!/usr/bin/env python3
"""Rank-path C2 bounds for regular pullbacks of the stationary C24 faces."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round34-rank-path-core-preimage-f9.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate5-round34-rank-path-core-preimage-f9-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json": (
        "6b9354026a1707a25971925e02acbb5ea7e459ca177190a28ff1b39857283d86"
    ),
    "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json": (
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140"
    ),
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json": (
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e"
    ),
    "cm2-gate5-round33-safe-f9-f10-subatlas-manifest-2026-07-19.json": (
        "75871f5e0bad0d504ecfe3a796bff05318f56f7044041c35b25918701adc6afc"
    ),
    "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json": (
        "ee1ac2acb72af04ac254e2f0a33981df478b022cde0dc08f9988762ff1c8bcc9"
    ),
    "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json": (
        "7594afb9fc37660e8ce7c47d57bfd385dde65bcedfbdab5872f52699f5a4e72d"
    ),
}

MINIMUM_RANK = 14
DERIVATIVE_NUMERATOR = 150
HESSIAN_NUMERATOR = 42672


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


def one_step_bounds(rank: int) -> tuple[int, int]:
    if type(rank) is not int or rank < MINIMUM_RANK:
        raise ValueError("rank must be an integer at least 14")
    derivative = DERIVATIVE_NUMERATOR * (1 << rank)
    hessian = HESSIAN_NUMERATOR * (1 << (3 * rank))
    return derivative, hessian


def expanded_hessian_bound(ranks: Iterable[int]) -> int:
    rank_path = tuple(ranks)
    derivative_bounds = [one_step_bounds(rank)[0] for rank in rank_path]
    hessian_bounds = [one_step_bounds(rank)[1] for rank in rank_path]
    total = 0
    for index, hessian in enumerate(hessian_bounds):
        prefix = 1
        for derivative in derivative_bounds[:index]:
            prefix *= derivative
        suffix = 1
        for derivative in derivative_bounds[index + 1 :]:
            suffix *= derivative
        total += suffix * hessian * prefix * prefix
    return total


def rank_path_bounds(ranks: Iterable[int]) -> dict[str, Any]:
    rank_path = tuple(ranks)
    derivative = 1
    inverse_derivative = 1
    hessian = 0
    recurrence_rows: list[dict[str, Any]] = []
    for time_index, rank in enumerate(rank_path, start=1):
        one_derivative, one_hessian = one_step_bounds(rank)
        previous_derivative = derivative
        hessian = (
            one_hessian * previous_derivative * previous_derivative
            + one_derivative * hessian
        )
        derivative = one_derivative * previous_derivative
        inverse_derivative = one_derivative * inverse_derivative
        recurrence_rows.append(
            {
                "time_index": time_index,
                "incidence_rank": rank,
                "one_step_D_infinity_strict_upper": str(one_derivative),
                "one_step_D2_infinity_strict_upper": str(one_hessian),
                "prefix_D_infinity_strict_upper": str(derivative),
                "prefix_inverse_D_infinity_strict_upper": str(inverse_derivative),
                "prefix_D2_infinity_strict_upper": str(hessian),
            }
        )
    if hessian != expanded_hessian_bound(rank_path):
        raise RuntimeError("composition Hessian recurrence")
    curvature = Q(3, 2) * inverse_derivative * hessian
    return {
        "rank_path": list(rank_path),
        "time_depth": len(rank_path),
        "prefix_D_infinity_strict_upper": str(derivative),
        "prefix_inverse_D_infinity_strict_upper": str(inverse_derivative),
        "prefix_D2_infinity_strict_upper": str(hessian),
        "level_gradient_l1_strict_lower": f"1/{inverse_derivative}",
        "unit_speed_face_C2_seminorm_strict_upper": str(curvature),
        "recurrence_rows": recurrence_rows,
    }


def build_result() -> dict[str, Any]:
    core = load(
        "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
    )["result"]["physical_return_core_registry"]
    affine = load(
        "cm2-gate5-round25-adaptive-face-f789-manifest-2026-07-18.json"
    )["result"]["fixed_s_adaptive_face_theorem"]
    atlas = load(
        "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
    )["result"]
    f8 = load(
        "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
    )["result"]
    prior = load(
        "cm2-gate5-round33-safe-f9-f10-subatlas-manifest-2026-07-19.json"
    )["result"]
    growth = load(
        "cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json"
    )["replay_summary"]
    endpoint = load(
        "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
    )["result"]["endpoint_rank_tail_and_first_order_cost"]

    if core["physical_compact_homogeneous_core_count"] != 24:
        raise RuntimeError("C24 count")
    if affine["phase_cut_face_types"] != ["r=constant", "phi=constant"]:
        raise RuntimeError("affine Birkhoff face types")
    if affine["individual_coordinate_face_C2_seminorm_upper"] != "0":
        raise RuntimeError("affine face curvature")
    face_registry = atlas["physical_C24_core_face_and_trace_registry"]
    if face_registry["materialized_physical_core_face_count"] != 96:
        raise RuntimeError("physical C24 faces")
    if not f8["parameterized_connected_face_registry"][
        "all_five_physical_face_grammars_covered"
    ]:
        raise RuntimeError("face grammar")
    if f8["same_ID_numeric_F8"][
        "common_normalized_transversality_strict_lower"
    ] != "1/5":
        raise RuntimeError("F8")
    if prior["strict_nonpromotion"]["Gate5_maturity"] != "6/18_UNCHANGED":
        raise RuntimeError("round33 maturity")
    if growth["D2T_coordinate_infinity_operator"] != "<42672/c_1^3":
        raise RuntimeError("one-step Hessian")
    one_collision = endpoint["one_collision_birkhoff_derivative"]
    if one_collision["forward_derivative_bound"] != "||DF_e||_infinity<150/cp_miss":
        raise RuntimeError("forward derivative")
    if one_collision["reverse_derivative_bound"] != "||DF_e^-1||_infinity<150/cp_source":
        raise RuntimeError("reverse derivative")
    if not one_collision["rank_dominates_both_inverse_incidence_scales"]:
        raise RuntimeError("incidence rank")
    if endpoint["canonical_rank_definition"]["core_rank"] != MINIMUM_RANK:
        raise RuntimeError("minimum rank")

    sample_paths = [
        rank_path_bounds(()),
        rank_path_bounds((14,)),
        rank_path_bounds((14, 15)),
        rank_path_bounds((14, 16, 18)),
        rank_path_bounds((20, 14, 17, 15)),
    ]
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "parameter_scope": "every fixed |s|<=1/400",
            "face_scope": (
                "regular homogeneous connected components of pullbacks of "
                "the 96 stationary C24 core faces"
            ),
        },
        "stationary_C24_affine_level_functions": {
            "physical_core_count": 24,
            "stationary_core_face_count": 96,
            "base_face_types": ["r=constant", "phi=constant"],
            "t_constant_face_represented_by": "r-r_edge=0",
            "p_constant_face_represented_by": "phi-arcsin(p_edge)=0",
            "representation_reason": (
                "t is monotone in boundary arclength on each frozen chart; "
                "p=sin(phi) is injective on the central |p|<3/10 core"
            ),
            "base_level_gradient_coordinate_l1_norm": "1",
            "base_level_Hessian": "0",
            "base_unit_speed_face_C2_seminorm": "0",
            "no_t_or_p_coordinate_change_derivative_is_charged": True,
        },
        "ranked_one_collision_C2_envelope": {
            "rank_contract": (
                "on each homogeneous step choose integer B>=14 with "
                "1/cp_source<2^B and 1/cp_target<2^B"
            ),
            "forward_D_infinity_strict_upper": "L(B)=150*2^B",
            "inverse_D_infinity_strict_upper": "L(B)=150*2^B",
            "D2_infinity_strict_upper": "M(B)=42672*2^(3B)",
            "rank_is_incidence_collar_rank_not_connected_component_rank": True,
            "valid_only_off_collision_singularities_and_owner_changes": True,
        },
        "arbitrary_time_composition_recurrence": {
            "initial_values": "D_0=E_0=1, H_0=0",
            "recurrence": [
                "D_j=L(B_j)*D_(j-1)",
                "E_j=L(B_j)*E_(j-1)",
                "H_j=M(B_j)*D_(j-1)^2+L(B_j)*H_(j-1)",
            ],
            "level_function": "F_j=e_coordinate o T_s^j-c",
            "gradient_lower": "||dF_j||_1>1/E_j",
            "gradient_reason": "e=dF_j o D(T_s^j)^(-1) in dual l1/linfinity norms",
            "Euclidean_gradient_lower": "||dF_j||_2>1/(sqrt(2)*E_j)",
            "Euclidean_Hessian_upper": "||D2F_j||_2<H_j",
            "unit_speed_C2_bound": "curvature(F_j=0)<sqrt(2)*E_j*H_j<(3/2)*E_j*H_j",
            "finite_for_every_finite_rank_path": True,
            "sample_rank_path_replays": sample_paths,
            "sample_rank_path_replays_sha256": digest(sample_paths),
        },
        "five_face_kind_matrix": {
            "source_core_clipping_face": {
                "F9": "CERTIFIED_LEVEL_ZERO",
                "F10": "CERTIFIED_ZERO_PARAMETER_CURRENT",
            },
            "intermediate_core_avoidance_preimage_face": {
                "F9": "CERTIFIED_RANK_PATH_TEMPLATE_ON_EACH_REGULAR_COMPONENT",
                "F10": "NOT_CERTIFIED",
            },
            "terminal_core_preimage_face": {
                "F9": "CERTIFIED_RANK_PATH_TEMPLATE_ON_EACH_REGULAR_COMPONENT",
                "F10": "NOT_CERTIFIED",
            },
            "collision_singularity_or_owner_change_face": {
                "F9": "NOT_CERTIFIED",
                "F10": "NOT_CERTIFIED",
            },
            "moving_occurrence_face": {
                "F9": "NOT_CERTIFIED",
                "F10": "CERTIFIED_SEED_LEVEL_PARAMETERIZED",
            },
        },
        "strict_nonpromotion": {
            "rank_path_template_is_complete_instantiated_face_atlas": False,
            "rank_path_template_is_uniform_in_depth_and_rank": False,
            "owner_change_or_singularity_F9": "NOT_CERTIFIED",
            "moving_occurrence_face_F9": "NOT_CERTIFIED",
            "complete_F9_physical_face_C2_atlas": "NOT_CERTIFIED",
            "complete_F10_all_face_coarea_regular_atlas": "NOT_CERTIFIED",
            "Gate5_maturity": "6/18_UNCHANGED",
            "complete_18_field_operator_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
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
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate5_round34_rank_path_core_preimage_f9_verifier.py",
    )
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print("CORE_PREIMAGE_F9_RANK_PATH_TEMPLATE: CERTIFIED")
    print(result["strict_nonpromotion"]["Gate5_maturity"])
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
