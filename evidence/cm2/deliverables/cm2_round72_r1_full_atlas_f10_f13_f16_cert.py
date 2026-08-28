#!/usr/bin/env python3
"""Producer for the Round-72 full base-R1 family classification."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

from cm2_round68_common import (
    CertError, canonical_bytes, digest, require, sha256_path, strict_json_path,
    validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round72.r1-full-atlas-f10-f13-f16.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round72-r1-full-atlas-f10-f13-f16"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round72_r1_full_atlas_f10_f13_f16_verifier.py"
COMMON = HERE / "cm2_round68_common.py"
FAMILY_PROOF = HERE / "cm2-round72-r1-full-family-interval-proof-2026-07-21.json"
MONO_PROOF = HERE / "cm2-round72-r1-positive-component-monotonicity-proof-2026-07-21.json"
FIELD_PROOF = HERE / "cm2-round72-r1-component-f10-f13-f16-proof-2026-07-21.json"
FAMILY_GENERATOR = HERE / "cm2_round72_r1_full_family_interval_generator.py"
MONO_GENERATOR = HERE / "cm2_round72_r1_positive_component_monotonicity_generator.py"
FIELD_GENERATOR = HERE / "cm2_round72_r1_component_f10_f13_f16_generator.py"
ROUND71 = "cm2-round71-r1-nonempty-face-germs-manifest-2026-07-21.json"

PINS = {
    "cm2-seventy-first-direct-assault-2026-07-21.md": "c58de9175953774c5dd96ae40993ebc204ed7ba6589397335ebd498b2305799e",
    "cm2-seventy-first-direct-assault-manifest-2026-07-21.sha256": "675e193eead58cb7f1e70666e6c382e7f50ac7cc02b19e5882b74cd12568aaec",
    ROUND71: "fb7fd4233d14834ca6a3efc488c2e8f1fcdf97bdeb410a1b93eda8d9b59d50f9",
    "cm2_round68_common.py": "f705d61157d5cbbf41f7ad4c4e72c6ad3fbd0466f34651137f15a03d6789d856",
}

ARTIFACT_HASHES = {
    FAMILY_PROOF.name: "904bac4bdec9a0c26918b4c75643bc9bb3ad439dbfca37fa11aaaa2afdef4342",
    FAMILY_GENERATOR.name: "941f21c10a4d8bcecafd59744e28a54f472a5f7c082ba388b27b753247a23cd4",
    MONO_PROOF.name: "4d171378ea31e68ff92efa62244d553e9b6b09ad843e4a70f8df3663ec3fb4fc",
    MONO_GENERATOR.name: "936941252832975e3dc205969c4c1f824ecea1180068a0e34fd92515e45c2382",
    FIELD_PROOF.name: "12c1f1db87030cf63552621a24ac0ebb1adb39933dc420497b425fb3c1f8e8a9",
    FIELD_GENERATOR.name: "20eb60b52acce9173e2685979aa44bd532c02ec10fd2c2d3862a5e10c92d0381",
}


def validate_artifacts() -> None:
    for name, expected in ARTIFACT_HASHES.items():
        require(sha256_path(HERE / name) == expected, f"artifact hash: {name}")


def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    validate_artifacts()
    family = strict_json_path(FAMILY_PROOF)
    mono = strict_json_path(MONO_PROOF)
    fields = strict_json_path(FIELD_PROOF)
    round71 = strict_json_path(HERE / ROUND71)["result"]

    classification = family["classification"]
    require(classification["candidate_family_count"] == 1152 and
            classification["positive_family_count"] == 32 and
            classification["certified_empty_family_count"] == 1120 and
            classification["unresolved_family_count"] == 0, "family exhaustion")
    require(classification["all_family_ids_sha256"] ==
            classification["frozen_registry_family_ids_sha256"] ==
            "feaf1a97c8b746596b5fb46b23a6de59a5d381d0648095b5c14b6d9071905b8b",
            "family digest")
    tree = family["tree_audit"]
    require(tree["total_interval_map_test_count"] == 824 and
            tree["total_leaf_count"] == 424 and tree["global_maximum_depth"] == 13,
            "classification tree")
    require(mono["theorem"]["each_clipped_positive_face_is_one_connected_graph_component"] is True,
            "connected components")
    require(mono["audit"]["positive_source_core_count"] == 16 and
            mono["audit"]["positive_face_count"] == 32 and
            mono["audit"]["total_tree_test_count"] == 112 and
            mono["audit"]["total_leaf_count"] == 64 and
            mono["audit"]["global_maximum_depth"] == 2, "monotonicity tree")
    field_result = fields["result"]
    require(field_result["component_count"] == 32 and
            field_result["F10_numeric_row_count"] == 32 and
            field_result["F10_integer_minimum"] == 3 and
            field_result["F10_integer_maximum"] == 39 and
            field_result["F10_integer_sum"] == 480, "F10 rows")
    require(field_result["F13_numeric_row_count"] == 32 and
            field_result["F13_32_face_current_variation_strict_upper"] == "4/125000000" and
            field_result["F16_numeric_Piola_row_count"] == 32 and
            field_result["F16_32_face_flux_cost_strict_upper"] == "4/125000000",
            "F13 F16 rows")

    old_components = round71["base_fibre_nonempty_face_witness_registry"]["component_rows"]
    old_ids = {row["component_id"] for row in old_components}
    require(old_ids == {row["component_id"] for row in field_result["rows"]}, "same components")

    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "append_only": True, "old_artifacts_modified": False,
            "pinned_chain": PINS, "proof_and_generator_hashes": ARTIFACT_HASHES,
        },
        "complete_base_fibre_terminal_preimage_family_atlas": {
            "status": "CERTIFIED_COMPLETE_1152_FAMILY_CLASSIFICATION",
            "parameter": "s=0", "candidate_family_count": 1152,
            "positive_family_count": 32, "certified_empty_family_count": 1120,
            "unresolved_family_count": 0,
            "family_ids_sha256": classification["all_family_ids_sha256"],
            "interval_map_test_count": 824, "interval_leaf_count": 424,
            "maximum_interval_depth": 13, "corner_residual_count": 0,
        },
        "complete_positive_component_registry": {
            "status": "CERTIFIED_32_UNIQUE_FULL_CLIPPED_CONNECTED_COMPONENTS",
            "positive_source_core_count": 16, "component_count": 32,
            "connected_rank": 0, "one_sided_trace_count": 64,
            "derivative_interval_test_count": 112,
            "derivative_leaf_count": 64, "maximum_derivative_depth": 2,
            "level_strictly_monotone_in_source_p": True,
            "target_coordinate_Jacobian_never_zero": True,
        },
        "numeric_local_field_registry": {
            "status": "CERTIFIED_32_ACTUAL_F10_F13_F16_COMPONENT_ROWS",
            "F8_rows_inherited": 32, "F9_rows_inherited": 32,
            "F10_numeric_rows": 32, "F10_integer_minimum": 3,
            "F10_integer_maximum": 39, "F10_integer_sum": 480,
            "F13_numeric_rows": 32,
            "F13_32_face_current_variation_strict_upper": "4/125000000",
            "F16_numeric_rows": 32,
            "F16_32_face_flux_cost_strict_upper": "4/125000000",
            "component_field_rows_sha256": field_result["rows_sha256"],
            "component_field_rows": field_result["rows"],
        },
        "strict_frontier": {
            "base_fibre_terminal_preimage_family_classification": "CERTIFIED_COMPLETE",
            "base_fibre_positive_clipped_components": "CERTIFIED_COMPLETE_32",
            "base_fibre_numeric_F10_F13_F16_rows": "CERTIFIED_32",
            "shared_96_stationary_plus_32_pullback_face_subdivision_incidence_quotient": "NOT_CERTIFIED",
            "arbitrary_depth_Rn_face_atlas": "NOT_CERTIFIED",
            "limiting_rank_path_weighted_sum": "NOT_CERTIFIED",
            "F14": "NOT_CERTIFIED", "F15": "NOT_CERTIFIED",
            "F17": "NOT_CERTIFIED", "F18": "NOT_CERTIFIED",
            "Gate1": "NOT_CERTIFIED", "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
            "Gate3": "NOT_CERTIFIED", "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7",
            "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
            "complete_composite_gates": "0/5", "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    replay = copy.deepcopy(result)
    result["internal_replay_digest"] = digest(replay)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    result = build_result()
    require(REPORT.is_file() and verifier.is_file(), "artifact presence")
    return {
        "schema": MANIFEST_SCHEMA, "pins": PINS,
        "proof_and_generator_hashes": ARTIFACT_HASHES,
        "report_sha256": sha256_path(REPORT),
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier.resolve()),
        "common_sha256": sha256_path(COMMON),
        "result": result, "verdict": result["strict_frontier"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--verifier", type=Path, default=VERIFIER)
    args = parser.parse_args()
    try:
        if args.replay:
            result = build_result()
            print(json.dumps({"families": "1152/1152", "positive": 32, "empty": 1120,
                              "F10_sum": result["numeric_local_field_registry"]["F10_integer_sum"],
                              "status": "PASS"}, sort_keys=True))
            return 0
        manifest = build_manifest(args.verifier)
        payload = canonical_bytes(manifest)
        if args.manifest_json:
            sys.stdout.buffer.write(payload)
            return 0
        if args.write_manifest is not None:
            args.write_manifest.write_bytes(payload)
            return 0
    except (CertError, OSError, ValueError, KeyError, TypeError, ArithmeticError) as exc:
        print(f"ROUND72_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND72 BASE-R1 FULL FAMILY ATLAS: PARTIAL_GLOBAL_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
