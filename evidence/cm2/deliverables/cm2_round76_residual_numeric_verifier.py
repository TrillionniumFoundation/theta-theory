#!/usr/bin/env python3
"""Verifier for the Round-76 residual refinement and numeric R2 fields."""
from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round68_common import digest, require, sha256_path, strict_json_path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round76-residual-numeric-manifest-2026-07-21.json"
DEPTH20 = HERE / "cm2-round76-s0-depth20-residual-refinement-2026-07-21.json"
WITNESSES = HERE / "cm2-round74-s0-r2-pair-witnesses-2026-07-21.json"
NUMERIC = HERE / "cm2-round76-r2-numeric-fields-2026-07-21.json"
CERT = HERE / "cm2_round76_residual_numeric_cert.py"
RESIDUAL_GENERATOR = HERE / "cm2_round76_s0_depth20_residual_generator.py"
NUMERIC_GENERATOR = HERE / "cm2_round76_r2_numeric_fields_generator.py"
FLINT_PYTHON = Path(os.environ.get("CM2_FLINT_PYTHON", "/tmp/cm2-flint-venv/bin/python"))


def strict_json_bytes(blob: bytes) -> Any:
    text = blob.decode()

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    def constant(value: str) -> Any:
        raise ValueError(value)

    decoder = json.JSONDecoder(object_pairs_hook=pairs, parse_constant=constant)
    value, end = decoder.raw_decode(text)
    require(not text[end:].strip(), "trailing JSON")
    return value


def integrity(document: dict[str, Any]) -> None:
    require(document["schema"] == "cm2.round76.residual-numeric.v1", "schema")
    require(document["result_sha256"] == digest(document["result"]), "result digest")
    for name, expected in document["pins"].items():
        require(sha256_path(HERE / name) == expected, f"pin {name}")


def semantics(result: dict[str, Any]) -> None:
    refinement = result["depth20_residual_refinement"]
    require(refinement["maximum_binary_depth"] == 20 and refinement["terminal_leaves"] == 670724, "depth20 tree")
    require(refinement["classification_histogram"] == {"DEPTH2_OUTER": 263072, "Q2_INNER": 339388, "R1_INNER": 45080, "R2_INNER": 23184}, "depth20 histogram")
    require(refinement["normalized_area_ledger"] == {"DEPTH2_OUTER": "8221/32768", "Q2_INNER": "2993217/131072", "R1_INNER": "108625/131072", "R2_INNER": "5501/65536"}, "depth20 area")
    require(refinement["outer_contraction_ratio"] == "8221/32628" and refinement["outer_contraction_strictly_below_one_third"], "outer contraction")
    pairs = result["strict_R2_pair_registry"]
    require((pairs["strict_R2_leaves"], pairs["source_cores"], pairs["source_destination_pairs"]) == (23184, 8, 16), "pair counts")
    require((pairs["main_branch_strict_leaves"], pairs["narrow_corner_strict_leaves"]) == (23136, 48), "branch leaves")
    require(pairs["known_Round75_component_pairs_recovered"] == 16 and pairs["new_strict_pairs_outside_Round75"] == 0, "pair closure")
    numeric = result["physical_R2_numeric_fields"]
    require(numeric["face_rows"] == 32 and numeric["F8_common_normalized_transversality_dyadic_lower"] == "1/2", "F8 rows")
    require(numeric["F9_integer_range"] == numeric["F10_integer_range"] == [1, 1], "F9 F10 range")
    require(numeric["F9_32_face_integer_sum"] == numeric["F10_32_face_integer_sum"] == 32, "F9 F10 sums")
    require(numeric["F13_32_face_current_variation_strict_upper"] == numeric["F16_32_face_Piola_flux_cost_strict_upper"] == "5354421251/250000000000", "F13 F16")
    sums = result["finite_cross_rank_field_sums"]
    require(sums["counting_measure"]["F10_64_face_integer_sum"] == 512, "counting F10")
    weighted = sums["geometric_depth_weight"]
    require(weighted["weight_rule"] == "face at time_j receives 2^(-time_j)", "weight rule")
    require(weighted["F9_weighted_sum_upper"] == "11069429950031259185971208", "weighted F9")
    require(weighted["F10_weighted_sum_upper"] == "248", "weighted F10")
    require(weighted["F13_weighted_sum_strict_upper"] == weighted["F16_weighted_sum_strict_upper"] == "5354437251/1000000000000", "weighted F13 F16")
    require(sums["official_limiting_path_law_status"] == "NOT_CERTIFIED", "weighted nonpromotion")
    gate = result["gate_effect"]
    require(gate["F8_F9_F10_F13_F16_on_all_32_R2_faces"] == "CERTIFIED", "field certification")
    require(gate["complete_depth2_face_atlas"].startswith("NOT_CERTIFIED"), "atlas nonpromotion")
    require(gate["limiting_weighted_face_sum"].startswith("NOT_CERTIFIED"), "limiting sum nonpromotion")
    require(gate["Gate4"] == "NOT_CERTIFIED__LANDING_JOIN_1_OF_7", "Gate4")
    require(gate["Gate5"] == "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0", "Gate5")
    require(gate["complete_composite_gates"] == "0/5" and gate["CM2"] == "NO-GO_FOR_CLAIM", "verdict")
    frontier = result["strict_frontier"]
    require(frontier["residual_candidate_exhaustion"].startswith("NOT_CERTIFIED"), "residual frontier")
    require(frontier["numeric_R2_field_rows"] == "CERTIFIED_32_OF_32", "numeric frontier")


def replay_depth20() -> dict[str, str]:
    depth20 = strict_json_path(DEPTH20)
    require(depth20["schema"] == "cm2.round74.s0-depth2-adaptive.v1", "depth20 schema")
    result = depth20["result"]
    require(result["terminal_leaf_count"] == sum(result["classification_histogram"].values()) == 670724, "leaf sum")
    require(sum((Q(value) for value in result["normalized_24_core_area_ledger"].values()), Q(0)) == 24, "area sum")
    rows = result["R2_rows"]
    require(len(rows) == result["R2_strict_leaf_count"] == 23184, "R2 rows")
    require(result["R2_rows_sha256"] == digest(rows), "R2 digest")
    require(all(row["owner_status"] == "strict_unique_second_collision_owner" for row in rows), "R2 owners")
    witnesses = strict_json_path(WITNESSES)["result"]["rows"]
    expected = {(row["source_core_index"], row["destination_core_id"]): row["branch"] for row in witnesses}
    observed = {(row["source_core_index"], row["destination_core_id"]) for row in rows}
    require(observed == set(expected) and len(observed) == 16, "R2 pairs")
    branches = Counter(expected[(row["source_core_index"], row["destination_core_id"])] for row in rows)
    require(branches == {"main": 23136, "narrow_corner": 48}, "branch replay")
    require(len({row["source_core_index"] for row in rows}) == 8, "R2 sources")
    return {"depth20_leaves": "670724/670724", "strict_R2_rows": "23184/23184", "known_pair_labels": "16/16", "new_strict_pairs": "0"}


def replay_numeric() -> dict[str, str]:
    numeric = strict_json_path(NUMERIC)
    require(numeric["schema"] == "cm2.round76.r2-numeric-fields.v1", "numeric schema")
    result = numeric["result"]
    rows = result["rows"]
    require(len(rows) == 32 and result["rows_sha256"] == digest(rows), "numeric rows")
    require(len({row["curve_id"] for row in rows}) == 32, "numeric curve join")
    require(all(row["F8_normalized_transversality_dyadic_lower"] == "1/2" for row in rows), "row F8")
    require(all(row["F9_unit_speed_C2_integer_upper"] == row["F10_density_C1_integer_upper"] == 1 for row in rows), "row F9 F10")
    f13 = sum((Q(row["F13_full_face_current_variation_strict_upper"]) for row in rows), Q(0))
    f16 = sum((Q(row["F16_full_face_Piola_flux_cost_strict_upper"]) for row in rows), Q(0))
    require(str(f13) == result["F13_32_face_current_variation_strict_upper"], "row F13 sum")
    require(str(f16) == result["F16_32_face_Piola_flux_cost_strict_upper"], "row F16 sum")
    return {"numeric_R2_rows": "32/32", "F8_F9_F10_F13_F16": "PASS"}


def deterministic_manifest(document: dict[str, Any]) -> None:
    process = subprocess.run([sys.executable, str(CERT), "--manifest-json"], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    require(process.returncode == 0, process.stderr.decode())
    require(process.stdout == MANIFEST.read_bytes(), "manifest byte reemit")
    require(strict_json_bytes(process.stdout) == document, "manifest JSON reemit")


def deterministic_generators() -> dict[str, str]:
    require(FLINT_PYTHON.is_file(), "flint python")
    numeric = subprocess.run([str(FLINT_PYTHON), str(NUMERIC_GENERATOR)], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    require(numeric.returncode == 0, numeric.stderr.decode())
    require(numeric.stdout == NUMERIC.read_bytes(), "numeric byte reemit")
    residual = subprocess.run([str(FLINT_PYTHON), str(RESIDUAL_GENERATOR)], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=900)
    require(residual.returncode == 0, residual.stderr.decode())
    require(residual.stdout == DEPTH20.read_bytes(), "residual byte reemit")
    return {"numeric_generator_reemit": "PASS", "depth20_generator_reemit": "PASS"}


def hostile(document: dict[str, Any]) -> int:
    mutations = [
        (("result", "depth20_residual_refinement", "terminal_leaves"), 670723),
        (("result", "strict_R2_pair_registry", "source_destination_pairs"), 17),
        (("result", "strict_R2_pair_registry", "new_strict_pairs_outside_Round75"), 1),
        (("result", "physical_R2_numeric_fields", "face_rows"), 31),
        (("result", "finite_cross_rank_field_sums", "geometric_depth_weight", "F10_weighted_sum_upper"), "249"),
        (("result", "gate_effect", "complete_depth2_face_atlas"), "CERTIFIED"),
        (("result", "gate_effect", "Gate5"), "CERTIFIED"),
        (("result", "gate_effect", "complete_composite_gates"), "1/5"),
    ]
    cases = []
    for path, value in mutations:
        for _ in range(32):
            case = copy.deepcopy(document)
            node = case
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = value
            case["result_sha256"] = digest(case["result"])
            cases.append(case)
    rejected = 0
    for case in cases:
        try:
            semantics(case["result"])
        except Exception:
            rejected += 1
    require(rejected == len(cases), "hostile rejection")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--skip-generator-reemit", action="store_true")
    args = parser.parse_args()
    document = strict_json_path(MANIFEST)
    integrity(document)
    semantics(document["result"])
    replay = replay_depth20()
    replay.update(replay_numeric())
    if args.audit:
        deterministic_manifest(document)
        if not args.skip_generator_reemit:
            replay.update(deterministic_generators())
        bad = [b'{"a":1,"a":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1} trailing']
        rejected = 0
        for blob in bad:
            try:
                strict_json_bytes(blob)
            except Exception:
                rejected += 1
        require(rejected == 4, "strict JSON")
        replay.update({"hostile_semantic_rejections": f"{hostile(document)}/256", "strict_json_rejections": "4/4", "manifest_byte_identical_reemit": "PASS"})
    print(json.dumps({"status": "PASS", "replay": replay}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
