#!/usr/bin/env python3
"""Audit 2026 small-hole results against the frozen C24 open system."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate134.round33-2026-small-hole-interface.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate134-round33-2026-small-hole-interface-manifest-2026-07-19.json"
DEPENDENCIES = {
    "cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json":
        "f0521bb84fc5b1c824d8361d375013aff024a89460cbc439f5aa7a04d7525183",
    "cm2-gate2-round23-core-kac-quotient-obstruction-manifest-2026-07-18.json":
        "cb857a533c3c23658cc354d46cd29e87511be9a36679f37c4a6326bae19731ba",
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json":
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e",
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
    geometry = load("cm2-gate34-c24-open-hole-geometry-manifest-2026-07-18.json")
    quotient = load("cm2-gate2-round23-core-kac-quotient-obstruction-manifest-2026-07-18.json")
    face = load("cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json")
    if geometry["verdict"]["C24_O1_O1prime_O2_open_hole_geometry"] != "CERTIFIED":
        raise RuntimeError("C24 geometry")
    if face["verdict"]["numeric_F8"] != "CERTIFIED_PARAMETERIZED":
        raise RuntimeError("F8")
    if quotient["verdict"]["Gate2"] != "NOT_CERTIFIED":
        raise RuntimeError("Gate2 frontier")
    result = {
        "schema": RESULT_SCHEMA,
        "sources_checked": {
            "arxiv_2604_19671": {
                "title": "Linear response for Sinai billiards with small holes",
                "author": "Giovanni Canestrari",
                "version_date": "2026-04-21",
                "pdf_sha256": "fc00f45a8ec6513763665bf8fa34569a95ca5d6d6b9fa5d90b7e1089fabd9004",
                "theorem_2_1_scope": "one boundary strip H_t centered at one arclength location and spanning the full angle interval",
                "theorem_4_7_scope": "normalized conditional loss of memory for that one-parameter strip-hole family",
            },
            "arxiv_2606_10155": {
                "title": "Recent Progress in the Application of Transfer Operators to Dispersing Billiards",
                "authors": ["Mark F. Demers", "Carlangelo Liverani"],
                "version_date": "2026-06-08",
                "pdf_sha256": "3330b5467c5c7107e58ba7966a0386f2ab51415990399b387ad2f7e571f61798",
                "section_5_6_1_scope": "projective-cone recovery for sufficiently small regular holes; large holes require sparse openings",
            },
            "arxiv_2104_06947": {
                "title": "Projective cones for sequential dispersing billiards",
                "authors": ["Mark F. Demers", "Carlangelo Liverani"],
                "pdf_sha256": "93f32b272fe837f72c3a0927fb772957c797a23732f9dfe78d0050f03d55cf7c",
                "section_8_scope": "O1/O2 cone recovery after an existential mixing block n_star",
            },
        },
        "exact_interface_matrix": {
            "finite_horizon_dispersing_table": "MATCH",
            "C24_O1_O1prime_O2": "MATCH_EXISTING_CERTIFICATE",
            "C24_mass_below_1_over_2500": "MATCH_EXISTING_CERTIFICATE",
            "single_full_angle_boundary_strip_H_t": "MISMATCH_24_DISJOINT_TWO_DIMENSIONAL_RECTANGLES",
            "explicit_C24_small_hole_threshold": "ABSENT",
            "unnormalized_recovered_cone_hit_lower": "ABSENT",
            "stationary_killed_operator_radius_strictly_below_one": "ABSENT",
            "Gate2_stable_quotient_inverse_branch_PPE": "ABSENT",
        },
        "safe_advances": {
            "latest_2026_every_step_small_hole_theorem_identified": True,
            "theorem_shape_mismatch_is_now_machine_checked": True,
            "C24_sparse_opening_admission_unchanged": "CERTIFIED_QUALITATIVE",
            "C24_every_collision_exponential_survivor_tail": "NOT_CERTIFIED",
            "physical_Green_rate_or_exact_nonlinear_cancellation": "NOT_CERTIFIED",
        },
        "strict_nonpromotion": {
            "Gate1": "NOT_CERTIFIED",
            "Gate2": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED_6_OF_18",
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
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate134_round33_2026_small_hole_interface_verifier.py")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        return 0
    print("2026_SMALL_HOLE_INTERFACE: AUDITED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
