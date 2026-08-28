#!/usr/bin/env python3
"""Round-39 physical L^(3/2) bound for moving-occurrence F10 seeds.

The endpoint-rank coarea tail has exponent two and the round-33 moving-face
F10 seed derivatives grow at most linearly in 2^B.  Their same occurrence-ID
join therefore yields an explicit physical raw-coarea L^(3/2) moment on all
64 moving occurrence seeds and both orientations.

This is a seed-subatlas result.  It is not an arbitrary-R_n pullback F10
field, a fixed-s collision-mass estimate, or the final Gate-4 q tail.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round39-moving-occurrence-f10-l3over2.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate5-round39-moving-occurrence-f10-l3over2-manifest-2026-07-19.json"
)
DEPENDENCIES = {
    "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json": (
        "7594afb9fc37660e8ce7c47d57bfd385dde65bcedfbdab5872f52699f5a4e72d"
    ),
    "cm2-gate5-round33-safe-f9-f10-subatlas-manifest-2026-07-19.json": (
        "75871f5e0bad0d504ecfe3a796bff05318f56f7044041c35b25918701adc6afc"
    ),
    "cm2-gate5-round38-f10-margin-exponent-frontier-manifest-2026-07-19.json": (
        "210f63f8d46f767837dbf0fb5f34e8c6ee21bbad4ce10695de3c32a7c10364c1"
    ),
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json": (
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788"
    ),
}

POSITIVE_COAREA_MASS = Q(8064, 5)
RANK_TAIL_CONSTANT = Q(9158592, 6875)
RANK_MOMENT_3OVER2 = (
    POSITIVE_COAREA_MASS * (1 << 21) + Q(7, 128) * RANK_TAIL_CONSTANT
)
REVERSE_MOMENT_UPPER = 35**2 * RANK_MOMENT_3OVER2
FORWARD_MOMENT_UPPER = 68**2 * RANK_MOMENT_3OVER2


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
    endpoint = load(
        "cm2-gate45-endpoint-rank-first-order-cost-manifest-2026-07-16.json"
    )["result"]["endpoint_rank_tail_and_first_order_cost"]
    tail = endpoint["endpoint_tail"]
    raw = endpoint["raw_rank_moment"]
    if tail["global_tail_constant"] != qstr(RANK_TAIL_CONSTANT):
        raise RuntimeError("rank tail constant")
    if tail["tail_exponent_in_dyadic_rank"] != "2":
        raise RuntimeError("rank tail exponent")
    if tail["valid_integer_threshold"] != "b>=14":
        raise RuntimeError("rank threshold")
    if raw["positive_coarea_mass_upper_before_Z_N_inverse"] != qstr(
        POSITIVE_COAREA_MASS
    ):
        raise RuntimeError("coarea mass")
    if raw["all_rank_moments_2^(chi*B)_finite_for"] != "0<=chi<2":
        raise RuntimeError("rank moment scope")

    seed = load(
        "cm2-gate5-round33-safe-f9-f10-subatlas-manifest-2026-07-19.json"
    )["result"]
    joined = seed["same_occurrence_ID_join"]
    f10 = seed["moving_occurrence_F10_subatlas"]
    if joined["moving_occurrence_face_seed_count"] != 64:
        raise RuntimeError("seed count")
    if joined["oriented_trace_seed_count"] != 128:
        raise RuntimeError("trace count")
    if joined["rank_tail_exponent"] != 2:
        raise RuntimeError("joined exponent")
    if f10["positive_density_wrt_source_normal_angle_upper"] != "18/5":
        raise RuntimeError("density")
    if f10["reverse_density_derivative_wrt_normal_angle"] != (
        "<(4374/125)*2^B"
    ):
        raise RuntimeError("reverse derivative")
    if f10["forward_density_derivative_wrt_normal_angle"] != (
        "<(8424/125)*2^B"
    ):
        raise RuntimeError("forward derivative")
    if f10["F10_slots"] != "CERTIFIED_PARAMETERIZED_64_OCCURRENCE_SEEDS":
        raise RuntimeError("F10 seed slots")

    frontier = load(
        "cm2-gate5-round38-f10-margin-exponent-frontier-manifest-2026-07-19.json"
    )["result"]
    if frontier["dyadic_margin_integrability_theorem"][
        "sufficient_and_sharp_strict_condition"
    ] != "r*p<alpha":
        raise RuntimeError("integrability criterion")

    f9 = load(
        "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
    )["result"]["strict_nonpromotion"]
    if f9["complete_F9_physical_face_C2_parameterized_atlas"] != "CERTIFIED":
        raise RuntimeError("F9 maturity dependency")
    if f9["Gate5_maturity"] != "7/18":
        raise RuntimeError("Gate5 maturity")


def rank_moment_derivation() -> dict[str, Any]:
    if RANK_MOMENT_3OVER2 != Q(46506443753721, 13750):
        raise RuntimeError("rank moment arithmetic")
    return {
        "physical_measure": (
            "unnormalized positive endpoint coarea measure before Z_N inverse"
        ),
        "rank_scope": "B>=14 on the unique active endpoint collar",
        "positive_coarea_total_mass_upper": qstr(POSITIVE_COAREA_MASS),
        "rank_tail": (
            "m{B>b}<=(9158592/6875)*4^(-b) for every integer b>=14"
        ),
        "layer_cake_identity": (
            "a^B=a^14+(a-1)*sum_{b=14}^{B-1}a^b with a=2^(3/2)"
        ),
        "safe_rational_bounds": [
            "a^14=2^21",
            "a-1<2",
            "sum_{b>=14}(a/4)^b<7/256",
        ],
        "integral_2^(3B/2)_dm_strict_upper": qstr(RANK_MOMENT_3OVER2),
        "rank_L3over2_moment_status": "CERTIFIED_PHYSICAL_RAW_COAREA",
    }


def seed_f10_lp_installation() -> dict[str, Any]:
    reverse_coefficient = Q(4374, 125)
    forward_coefficient = Q(8424, 125)
    density = Q(18, 5)
    if not density + reverse_coefficient * (1 << 14) < 35 * (1 << 14):
        raise RuntimeError("reverse envelope")
    if not density + forward_coefficient * (1 << 14) < 68 * (1 << 14):
        raise RuntimeError("forward envelope")
    if REVERSE_MOMENT_UPPER != Q(2278815743932329, 550):
        raise RuntimeError("reverse moment")
    if FORWARD_MOMENT_UPPER != Q(107522897958602952, 6875):
        raise RuntimeError("forward moment")
    rows = []
    for rank in (14, 18, 24):
        rows.append(
            {
                "B": rank,
                "reverse_integer_envelope": 35 * (1 << rank),
                "forward_integer_envelope": 68 * (1 << rank),
            }
        )
    return {
        "same_occurrence_ID_seed_count": 64,
        "oriented_trace_count": 128,
        "raw_seed_cost_definition": (
            "positive density upper plus absolute normal-angle density derivative upper"
        ),
        "reverse_raw_seed_cost": "<18/5+(4374/125)*2^B<35*2^B",
        "forward_raw_seed_cost": "<18/5+(8424/125)*2^B<68*2^B",
        "valid_for_every_rank": "integer B>=14",
        "representative_integer_envelopes": rows,
        "Lp_power": "p=3/2",
        "rationalization": "35^(3/2)<35^2 and 68^(3/2)<68^2",
        "reverse_integral_raw_F10^(3/2)_strict_upper": qstr(
            REVERSE_MOMENT_UPPER
        ),
        "forward_integral_raw_F10^(3/2)_strict_upper": qstr(
            FORWARD_MOMENT_UPPER
        ),
        "bidirectional_seed_F10_L3over2_status": "CERTIFIED_PHYSICAL_RAW_COAREA",
    }


def exponent_match() -> dict[str, Any]:
    return {
        "same_margin_variable": "endpoint scale eta with B=max(14,ceil(log2(1/eta)))",
        "physical_margin_tail_exponent_alpha": "2 on this seed subatlas",
        "F10_blowup_exponent_r": "1 on this seed subatlas",
        "chosen_Lp_exponent_p": "3/2",
        "strict_product": "r*p=3/2<2=alpha",
        "round38_integrability_criterion_met": True,
        "arbitrary_Rn_or_all_face_exponent_claimed": False,
    }


def build_result() -> dict[str, Any]:
    validate_dependencies()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "claim_type": "same-ID moving-occurrence seed F10 physical raw-coarea L3/2 moment",
        },
        "physical_rank_L3over2_derivation": rank_moment_derivation(),
        "moving_occurrence_seed_F10_L3over2_installation": seed_f10_lp_installation(),
        "physical_margin_blowup_exponent_match": exponent_match(),
        "strict_nonpromotion": {
            "moving_occurrence_seed_F10_physical_L3over2": "CERTIFIED_64_SEEDS_128_TRACES",
            "fixed_s_collision_SRB_mass_moment": "NOT_ASSERTED_FROM_COAREA_MEASURE",
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
        default=HERE / "cm2_gate5_round39_moving_occurrence_f10_l3over2_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    print(
        "MOVING_OCCURRENCE_F10_L3OVER2:",
        result["strict_nonpromotion"][
            "moving_occurrence_seed_F10_physical_L3over2"
        ],
    )
    print("ARBITRARY_RN_ALL_FACE_F10: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
