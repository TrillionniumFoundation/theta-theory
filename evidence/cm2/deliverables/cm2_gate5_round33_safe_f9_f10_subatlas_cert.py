#!/usr/bin/env python3
"""Safe F9/F10 subatlas without retyping carrier curvature as face curvature."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round33-safe-f9-f10-subatlas.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate5-round33-safe-f9-f10-subatlas-manifest-2026-07-19.json"
DEPENDENCIES = {
    "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json":
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json":
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e",
    "cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json":
        "b38772a41d0b610e1e1cd4fb4509cfb76227cc8f4983af0699d2cf38e60650c5",
    "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json":
        "7594afb9fc37660e8ce7c47d57bfd385dde65bcedfbdab5872f52699f5a4e72d",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def build_result() -> dict[str, Any]:
    atlas = load("cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json")
    f8 = load("cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json")
    geometric = load("cm2-gate45-curvature-log-density-cost-manifest-2026-07-16.json")
    endpoint = load("cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json")
    core = atlas["result"]["physical_C24_core_face_and_trace_registry"]
    occurrence = atlas["result"]["moving_occurrence_coarea_DQ_face_seed_registry"]
    cost = geometric["result"]["curvature_log_density_and_partial_cost"]
    rank = endpoint["result"]["endpoint_rank_tail_and_first_order_cost"]
    if core["materialized_physical_core_face_count"] != 96:
        raise RuntimeError("core faces")
    if occurrence["materialized_physical_moving_occurrence_face_seed_count"] != 64:
        raise RuntimeError("occurrence faces")
    if occurrence["corrected_unnormalized_density_upper_bound_wrt_dtheta"] != "18/5":
        raise RuntimeError("density upper")
    if f8["verdict"]["Gate5_maturity"] != "6/18":
        raise RuntimeError("F8 frontier")
    if geometric["result"]["provenance"]["corrected_current_rows_sha256"] != "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd":
        raise RuntimeError("current rows")
    if rank["canonical_rank_definition"]["core_rank"] != 14:
        raise RuntimeError("rank")
    reverse_theta_derivative = Q(18, 5) * Q(9, 25) * 27
    forward_theta_derivative = Q(18, 5) * Q(9, 25) * 52
    if reverse_theta_derivative != Q(4374, 125) or forward_theta_derivative != Q(8424, 125):
        raise RuntimeError("derivative arithmetic")
    result = {
        "schema": RESULT_SCHEMA,
        "same_occurrence_ID_join": {
            "corrected_current_rows_sha256": "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd",
            "moving_occurrence_face_seed_count": 64,
            "oriented_trace_seed_count": 128,
            "canonical_endpoint_rank": "B=max(14,ceil(log2(1/scale))) on the unique active collar",
            "rank_tail_exponent": 2,
            "rank_joined_without_copying_seed_to_unrelated_face_kinds": True,
        },
        "stationary_source_core_subatlas": {
            "physical_face_count": 96,
            "one_sided_trace_count": 192,
            "fixed_chart_face_types": ["t=constant", "p=constant"],
            "F9_face_C2_atlas_bound": "0",
            "parameter_speed": "0",
            "F10_parameter_coarea_density_regular_bound": "0",
            "collision_trace_measure_declared_zero": False,
            "F9_F10_slots": "CERTIFIED_96_LEVEL_ZERO_FACES",
        },
        "moving_occurrence_F10_subatlas": {
            "positive_density_wrt_source_normal_angle_upper": "18/5",
            "source_or_target_radius_upper": "9/25",
            "reverse_log_density_derivative_wrt_arclength": "<27*2^B",
            "forward_log_density_derivative_wrt_arclength": "<52*2^B",
            "reverse_density_derivative_wrt_normal_angle": "<(4374/125)*2^B",
            "forward_density_derivative_wrt_normal_angle": "<(8424/125)*2^B",
            "F10_slots": "CERTIFIED_PARAMETERIZED_64_OCCURRENCE_SEEDS",
            "F9_physical_face_C2_from_carrier_4949": "NOT_CERTIFIED_WRONG_TYPE",
        },
        "five_face_kind_matrix": {
            "source_core_clipping_face": {"F9": "CERTIFIED_LEVEL_ZERO", "F10": "CERTIFIED_ZERO_PARAMETER_CURRENT"},
            "intermediate_core_avoidance_preimage_face": {"F9": "NOT_CERTIFIED", "F10": "NOT_CERTIFIED"},
            "terminal_core_preimage_face": {"F9": "NOT_CERTIFIED", "F10": "NOT_CERTIFIED"},
            "collision_singularity_or_owner_change_face": {"F9": "NOT_CERTIFIED", "F10": "NOT_CERTIFIED"},
            "moving_occurrence_face": {"F9": "NOT_CERTIFIED", "F10": "CERTIFIED_SEED_LEVEL_PARAMETERIZED"},
        },
        "strict_nonpromotion": {
            "carrier_C2_4949_retyped_as_all_face_F9": False,
            "complete_F9_physical_face_C2_atlas": "NOT_CERTIFIED",
            "complete_F10_all_face_coarea_regular_atlas": "NOT_CERTIFIED",
            "Gate5_maturity": "6/18_UNCHANGED",
            "complete_18_field_operator_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["internal_replay_digest"] = hashlib.sha256(
        json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
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
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate5_round33_safe_f9_f10_subatlas_verifier.py")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    result = build_result()
    print(result["stationary_source_core_subatlas"]["F9_F10_slots"])
    print(result["moving_occurrence_F10_subatlas"]["F10_slots"])
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
