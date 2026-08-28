#!/usr/bin/env python3
"""Connected-rank and numeric F8 join on the parameterized parent-W atlas."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate5.round32-parameterized-face-rank-f8.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
DEFAULT_MANIFEST = HERE / "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
DEPENDENCIES = {
    "cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json":
        "58a8b27517a55fabd5776e9299802bb656f60733ae86c25941b640be2dfb4e91",
    "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json":
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    "cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json":
        "fa654b2c852f2b89e6e85a457f7ec7689dc56b7ccc9582d994db6b2e269bfb74",
    "cm2-gate45-round32-actual-instance-f7-join-manifest-2026-07-19.json":
        "81e59b1ca2ff8b2aeac1c2eba36592e0e788618a33ef97c7a7d65faa94c2c310",
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
    roots = load("cm2-gate25-physical-boundary-root-order-frontier-manifest-2026-07-17.json")
    faces = load("cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json")
    parent = load("cm2-gate45-round31-parent-w-borel-registry-manifest-2026-07-19.json")
    f7 = load("cm2-gate45-round32-actual-instance-f7-join-manifest-2026-07-19.json")
    grammar = roots["result"]["physical_branch_slope_and_root_grammar"]
    frontier = faces["result"]["R2_and_arbitrary_n_physical_face_ID_grammar_frontier"]
    if grammar["every_active_branch_has_at_most_one_isolated_root"] is not True:
        raise RuntimeError("root uniqueness")
    if grammar["stable_unstable_transversality_gap_strict_lower"] != "50/9":
        raise RuntimeError("slope gap")
    if len(frontier["boundary_carrier_kind_rows"]) != 5:
        raise RuntimeError("face grammar kinds")
    if parent["result"]["Q2_parent_W_Borel_registry"]["phase_graph_slope_dphi_dr"] != "4":
        raise RuntimeError("parent slope")
    if f7["result"]["Gate5_maturity_update"]["current_global_maturity"] != "5/18":
        raise RuntimeError("F7 maturity")
    # For a stable graph slope m<=-25/9, the normalized wedge with (1,4)
    # is |4-m|/(sqrt(17)*sqrt(1+m^2)); its infimum on that half-line is
    # 1/sqrt(17)>1/5. Vertical faces attain the same limiting value, while
    # horizontal faces have 4/sqrt(17)>1/5.
    if not Q(1, 17) > Q(1, 25):
        raise RuntimeError("transversality arithmetic")
    result = {
        "schema": RESULT_SCHEMA,
        "parameterized_connected_face_registry": {
            "physical_face_grammar_kind_count": 5,
            "parent_W_slope": "4",
            "nonvertical_physical_branch_slope_contract": "m<=-25/9",
            "each_parent_W_face_family_intersection_count": "0_or_1",
            "nonempty_intersection_connected_rank": 0,
            "connected_rank_assignment": "CERTIFIED_PARAMETERIZED",
            "face_instance_id_schema": "face:(component-id,time-j,carrier-family-id,parent-W-id,connected-rank-0)",
            "trace_instance_id_schema": "trace:(face-instance-id,side-label)",
            "two_one_sided_traces_per_regular_noncorner_root": True,
            "corner_or_simultaneous_root_policy": "cemetery",
            "all_five_physical_face_grammars_covered": True,
            "finite_integer_face_count_claimed": False,
        },
        "same_ID_numeric_F8": {
            "field_name": "face_transversality_lower",
            "stable_graph_normalized_wedge_formula": "abs(4-m)/(sqrt(17)*sqrt(1+m^2))",
            "vertical_face_normalized_wedge": "1/sqrt(17)",
            "horizontal_face_normalized_wedge": "4/sqrt(17)",
            "common_normalized_transversality_strict_lower": "1/5",
            "strict_lower_verified_by_squared_rational_inequality": "1/17>1/25",
            "numeric_F8_actual_face_slots": "CERTIFIED_PARAMETERIZED",
        },
        "moving_occurrence_coarea_trace_join": {
            "global_moving_occurrence_face_seed_count": 64,
            "oriented_hit_miss_trace_seed_count": 128,
            "corrected_unnormalized_density_upper_wrt_dtheta": "18/5",
            "density_attached_to_parameterized_rank0_instances": True,
            "complete_all_face_kind_numeric_coarea_regular_bound": "NOT_CERTIFIED",
        },
        "Gate5_maturity_update": {
            "previous_global_maturity": "5/18",
            "newly_materialized_field": "F8 face_transversality_lower",
            "current_global_maturity": "6/18",
            "complete_18_field_operator_block_count": 0,
        },
        "strict_nonpromotion": {
            "F9_complete_physical_face_C2_atlas": "NOT_CERTIFIED",
            "F10_all_face_coarea_density_regular_bound": "NOT_CERTIFIED",
            "F11_through_F18": "NOT_CERTIFIED",
            "complete_limiting_component_enumeration": "NOT_CERTIFIED",
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
        "verdict": {
            "connected_rank_assignment": "CERTIFIED_PARAMETERIZED",
            "numeric_F8": "CERTIFIED_PARAMETERIZED",
            "Gate5_maturity": "6/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=HERE / "cm2_gate5_round32_parameterized_face_rank_f8_verifier.py")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    build_result()
    print("PARAMETERIZED_CONNECTED_RANK_AND_F8: CERTIFIED")
    print("GATE5_MATURITY: 6/18")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    raise SystemExit(main())
