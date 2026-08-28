#!/usr/bin/env python3
"""Round-30 depth-eight fair refinement of the Q2 chart seam."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_gate45_round29_q2_seam_recut_face_frontier_cert as r29


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate45.round30-q2-seam-depth8.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate45-round30-q2-seam-depth8-manifest-2026-07-19.json"
DEPENDENCIES = {
    "cm2_gate45_round29_q2_seam_recut_face_frontier_cert.py":
        "5491e35bd249deb384c8231e9f4a90033746bcc59d0fbe4512d0bb7b8ffbea62",
    "cm2-gate45-round29-q2-seam-recut-face-frontier-manifest-2026-07-18.json":
        "36ed8c2cd695a7bafffb0cb2522cdd39eea73bedac4fe7b6ee8adc14abcef145",
}
EXPECTED = {
    "maximum_additional_fair_dyadic_depth": 8,
    "refined_terminal_cell_count": 457964,
    "resolved_strict_single_chart_child_count": 163330,
    "residual_representation_seam_outer_count": 294634,
    "original_plus_refined_strict_single_chart_cell_count": 272056,
    "resolved_base_mass": "64527087/655360000000",
    "residual_base_mass": "2559121/655360000000",
    "refined_rows_sha256": "5cb89fd4d7babd4322fe8d78416186ad4c78c29a425b055fe0bd2b179453f73a",
    "refined_cell_ids_sha256": "8ce6e71625dee84206f74857a8db95ea25450e83c4e385abfd2b2a3e815e842d",
}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise RuntimeError(f"unsafe dependency: {name}")
        if sha256_path(path) != expected:
            raise RuntimeError(f"dependency hash: {name}")


def validate_result(result: dict[str, Any]) -> None:
    seam = result["Q2_time2_target_chart_seam_refinement"]
    for key, expected in EXPECTED.items():
        if seam.get(key) != expected:
            raise RuntimeError(f"depth-eight ledger: {key}")
    if seam["resolved_strict_single_chart_child_count"] + seam["residual_representation_seam_outer_count"] != seam["refined_terminal_cell_count"]:
        raise RuntimeError("terminal count identity")
    if result["Q2_actual_parent_W_recut_instance_frontier"]["actual_curve_recut_instance_id_count"] != 0:
        raise RuntimeError("actual instance type barrier")
    if result["Gate5_frontier"]["CM2"] != "NO-GO_FOR_CLAIM":
        raise RuntimeError("CM2 fail-close")


def build_result() -> dict[str, Any]:
    verify_dependencies()
    old_depth = r29.MAX_EXTRA_SEAM_DEPTH
    try:
        r29.MAX_EXTRA_SEAM_DEPTH = 8
        result = r29.build_result()
    finally:
        r29.MAX_EXTRA_SEAM_DEPTH = old_depth
    result["schema"] = RESULT_SCHEMA
    result["provenance"]["round30_parent_sha256"] = DEPENDENCIES
    result["provenance"]["replay_engine"] = (
        "fresh complete 384-bit Arb time-two recursion plus depth-8 fair seam refinement"
    )
    result.pop("internal_replay_digest", None)
    result["internal_replay_digest"] = r29.digest(result)
    validate_result(result)
    return result


def write_manifest(path: Path, verifier: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": result["Gate5_frontier"],
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate45_round30_q2_seam_depth8_verifier.py")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    seam = result["Q2_time2_target_chart_seam_refinement"]
    print(f"F4_STRICT_SINGLE_CHART_CELLS: {seam['original_plus_refined_strict_single_chart_cell_count']}")
    print("ACTUAL_PARENT_W_INSTANCES: 0")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
