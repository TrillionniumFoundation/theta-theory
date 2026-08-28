#!/usr/bin/env python3
"""Producer for the Round-71 witnessed nonempty R1 face germs."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

from cm2_round68_common import (
    CertError, canonical_bytes, digest, require, sha256_path, strict_json_path,
    validate_pins,
)


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round71.r1-nonempty-face-germs.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round71-r1-nonempty-face-germs"
REPORT = HERE / f"{PREFIX}-assault-2026-07-21.md"
WITNESSES = HERE / "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
VERIFIER = HERE / "cm2_round71_r1_nonempty_face_germs_verifier.py"
COMMON = HERE / "cm2_round68_common.py"

ATLAS = "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json"
F8 = "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json"
F9 = "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json"
F10 = "cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json"
F16 = "cm2-gate5-round46-piola-f16-frontier-manifest-2026-07-19.json"
ROUND69 = "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json"

PINS = {
    "cm2-seventieth-direct-assault-2026-07-21.md": "c40d39523088d48cec62e3414a6b4596bc2ab1162887a2377c94a5efb03fa146",
    "cm2-seventieth-direct-assault-manifest-2026-07-21.sha256": "221b58f90e91c85c8044c1c8260f9c7c4e11499ec77ba33623701c3535ab7ee9",
    "cm2-round70-selected-nonempty-face-incidence-all-gate-manifest-2026-07-21.json": "057f60f2583134b765cec47756f766a591497e1898cbec9b89afd7febbfe99ad",
    ROUND69: "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
    ATLAS: "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    F8: "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e",
    F9: "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788",
    F10: "9bc22092f99cd9af0d4b4daf44c89f6e5b24ca90f4826ed870f754e02de9ce73",
    F16: "ee4a4fd441ff5b63e5607bcd367b04c336a49173d3e7be8ca4b5e1181d3e5a49",
    "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json": "3226044b8d0718a0d565c7ff9dd6c4736d2b1d28fa784c46443da92e85b61cc6",
    "cm2_round68_common.py": "f705d61157d5cbbf41f7ad4c4e72c6ad3fbd0466f34651137f15a03d6789d856",
}


@dataclass(frozen=True)
class Core:
    chart_id: str
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    target_id: str
    crossings: tuple[str, ...]

    @property
    def source(self) -> str:
        return self.chart_id.split(":")[0]


def physical_cores() -> tuple[Core, ...]:
    rows: list[Core] = []
    axis = {"E": (1, 0, "X+"), "W": (-1, 0, "X-"), "N": (0, 1, "Y+"), "S": (0, -1, "Y-")}
    for source in ("G", "W"):
        for cell in ("E", "W", "N", "S"):
            ix, iy, token = axis[cell]
            rows.append(Core(f"{source}:{cell}", Q(1, 100), Q(1, 50), -Q(1, 500), Q(1, 500),
                             f"{source}[{ix},{iy}]", () if source == "G" else (token,)))
    diagonal = {
        "G": {"NE": (("E", 1), ("N", 1), "W[0,0]"), "NW": (("W", 1), ("N", -1), "W[-1,0]"),
              "SE": (("E", -1), ("S", 1), "W[0,-1]"), "SW": (("W", -1), ("S", -1), "W[-1,-1]")},
        "W": {"NE": (("E", 1), ("N", 1), "G[1,1]"), "NW": (("W", 1), ("N", -1), "G[0,1]"),
              "SE": (("E", -1), ("S", 1), "G[1,0]"), "SW": (("W", -1), ("S", -1), "G[0,0]")},
    }
    for source in ("G", "W"):
        for direction in ("NE", "NW", "SE", "SW"):
            first, second, target = diagonal[source][direction]
            for cell, sign in (first, second):
                t0, t1 = (Q(69, 100), Q(7, 10)) if sign > 0 else (-Q(7, 10), -Q(69, 100))
                rows.append(Core(f"{source}:{cell}", t0, t1, -Q(1, 50), Q(1, 50), target, ()))
    rows.sort(key=lambda row: (row.chart_id, row.target_id, row.crossings, row.t0, row.t1, row.p0, row.p1))
    require(len(rows) == 24, "24 cores")
    return tuple(rows)


def core_id(core: Core) -> str:
    return "core:" + digest({
        "chart_id": core.chart_id, "t": [str(core.t0), str(core.t1)],
        "p": [str(core.p0), str(core.p1)], "target_id": core.target_id,
        "crossings": list(core.crossings),
    })


def face_id(core: Core, side: str) -> str:
    coordinate = side[0]
    value = core.t0 if side == "t_lower" else core.t1 if side == "t_upper" else core.p0 if side == "p_lower" else core.p1
    return "physical-core-face:" + digest({
        "core_id": core_id(core), "core_chart_id": core.chart_id,
        "core_source_obstacle": core.source, "side": side,
        "coordinate": coordinate, "coordinate_value": str(value),
        "outward_normal_sign": -1 if side.endswith("lower") else 1,
    })


@lru_cache(maxsize=1)
def build_result() -> dict[str, Any]:
    validate_pins(HERE, PINS)
    witness_document = strict_json_path(WITNESSES)
    require(witness_document["schema"] == "cm2.round71.r1-nonempty-face-witnesses.v1",
            "witness schema")
    witnesses = witness_document["rows"]
    require(isinstance(witnesses, list) and len(witnesses) == 32, "32 witnesses")
    cores = physical_cores()

    atlas = strict_json_path(HERE / ATLAS)["result"]
    require(atlas["R1_regular_core_preimage_face_family_seed_registry"]
            ["materialized_candidate_R1_core_preimage_equation_family_count"] == 1152,
            "candidate families")
    require(atlas["limiting_R1_face_seed_coverage"]
            ["nonempty_connected_face_component_ids_materialized"] == 0,
            "prior nonempty count")
    f8 = strict_json_path(HERE / F8)["result"]
    require(f8["same_ID_numeric_F8"]["common_normalized_transversality_strict_lower"] == "1/5",
            "F8 lower")
    f9 = strict_json_path(HERE / F9)["result"]
    require(f9["general_base_face_rank_path_recurrence"]["finite_for_every_finite_rank_path"] is True,
            "F9 recurrence")
    f10 = strict_json_path(HERE / F10)["result"]
    require(f10["canonical_dyadic_radius_and_F10_search"]
            ["canonical_finite_integer_F10_value_exists_for_each_germ"] is True,
            "F10 search")
    f16 = strict_json_path(HERE / F16)["result"]
    require(f16["strict_nonpromotion"]["all_five_face_arbitrary_suffix_F16"] == "CERTIFIED",
            "F16 schema")

    edge_rows = strict_json_path(HERE / ROUND69)["result"]["actual_base_s_return_root"]["edge_rows"]
    positive_edges = {(row["source_core_id"], row["destination_core_id"]) for row in edge_rows}
    require(len(positive_edges) == 16, "16 positive edges")

    component_rows = []
    for witness in witnesses:
        source = cores[witness["source_core_index"]]
        destination = cores[witness["destination_core_index"]]
        require(witness["source_core_id"] == core_id(source), "source ID")
        require(witness["destination_core_id"] == core_id(destination), "destination ID")
        require(witness["destination_face_id"] == face_id(destination, witness["side"]), "face ID")
        require((witness["source_core_id"], witness["destination_core_id"]) in positive_edges,
                "positive edge witness")
        component_key = {
            "candidate_family_id": witness["candidate_family_id"], "base_parameter": "s=0",
            "witness_minus": witness["witness_minus"], "witness_plus": witness["witness_plus"],
        }
        component_id = "physical-r1-face-component:" + digest(component_key)
        traces = [{
            "side_label": label,
            "trace_id": "physical-r1-trace:" + digest({"component_id": component_id, "side": label}),
        } for label in ("inside", "outside")]
        path_cell_id = "base-r1-edge-cell:" + digest({
            "source_core_id": witness["source_core_id"],
            "destination_core_id": witness["destination_core_id"], "s": "0",
        })
        component_rows.append({
            "component_id": component_id,
            "candidate_family_id": witness["candidate_family_id"],
            "destination_face_id": witness["destination_face_id"],
            "source_core_id": witness["source_core_id"],
            "destination_core_id": witness["destination_core_id"],
            "time_j": 1, "connected_rank": 0,
            "local_component_status": "CERTIFIED_NONEMPTY_REGULAR_CONNECTED_GERM",
            "path_cell_id": path_cell_id,
            "incidence_relation": "TERMINAL_CORE_PREIMAGE_FACE_GERM_INCIDENT_TO_BASE_R1_EDGE_CELL",
            "trace_rows": traces,
            "F8_normalized_transversality_strict_lower": "1/5",
            "F9_unit_speed_C2_upper": "691839371876953699123200",
            "F10_integer": "NOT_MATERIALIZED__TERMINATING_SEARCH_APPLIES",
            "F16": "PARAMETERIZED_PIOLA_IDENTITY_ONLY__NUMERIC_COST_REQUIRES_F13",
        })

    require(len({row["component_id"] for row in component_rows}) == 32, "component IDs")
    require(len({trace["trace_id"] for row in component_rows for trace in row["trace_rows"]}) == 64,
            "trace IDs")
    require(len({row["path_cell_id"] for row in component_rows}) == 16, "path cells")
    f9_each = 691839371876953699123200
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {"append_only": True, "old_artifacts_modified": False, "pinned_chain": PINS},
        "base_fibre_nonempty_face_witness_registry": {
            "status": "CERTIFIED_32_NONEMPTY_REGULAR_LOCAL_FACE_GERMS",
            "parameter": "s=0", "positive_R1_edge_cell_count": 16,
            "candidate_family_count_total": 1152,
            "witnessed_distinct_candidate_family_count": 32,
            "unresolved_candidate_family_count": 1120,
            "materialized_local_component_count_before_round71": 0,
            "materialized_local_component_count_after_round71": 32,
            "materialized_one_sided_trace_count": 64,
            "all_witness_segments_have_rational_endpoints": True,
            "all_endpoint_level_signs_replayed_independently": True,
            "rank14_map_Lipschitz_upper": 2457600,
            "maximum_source_segment_l1_length": "23/23058430092136939520000",
            "component_rows": component_rows,
        },
        "actual_local_field_attachment": {
            "status": "F8_F9_ACTUAL__F10_SEARCH_AND_F16_SCHEMA_ATTACHED_WITHOUT_NUMERIC_PROMOTION",
            "F8_common_normalized_strict_lower": "1/5",
            "F9_rank_path": [14], "F9_D1": 2457600, "F9_E1": 2457600,
            "F9_H1": 187673440721829888,
            "F9_per_face_unit_speed_C2_upper": str(f9_each),
            "F9_32_face_finite_sum_upper": str(32 * f9_each),
            "F10_actual_compact_germs_in_search_domain": 32,
            "F10_numeric_integers_materialized": 0,
            "F13_numeric_rows_materialized": 0,
            "F16_parameterized_Piola_rows_attached": 32,
            "F16_numeric_cost_rows_materialized": 0,
        },
        "strict_frontier": {
            "complete_1152_family_empty_nonempty_classification": "NOT_CERTIFIED__32_POSITIVE_1120_UNRESOLVED",
            "complete_limiting_R1_connected_face_atlas": "NOT_CERTIFIED",
            "common_face_subdivision_and_incidence_atlas": "NOT_CERTIFIED",
            "weighted_global_F9_F10_F13_F16_sum": "NOT_CERTIFIED",
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
    require(REPORT.is_file() and verifier.is_file() and COMMON.is_file(), "artifact presence")
    return {
        "schema": MANIFEST_SCHEMA, "pins": PINS,
        "report_sha256": sha256_path(REPORT),
        "witnesses_sha256": sha256_path(WITNESSES),
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
            result = build_result()["base_fibre_nonempty_face_witness_registry"]
            print(json.dumps({"faces": result["materialized_local_component_count_after_round71"],
                              "traces": result["materialized_one_sided_trace_count"],
                              "cells": result["positive_R1_edge_cell_count"], "status": "PASS"}, sort_keys=True))
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
        print(f"ROUND71_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND71 R1 NONEMPTY FACE GERMS: PARTIAL_ONLY")
    print("CM2: NO-GO_FOR_CLAIM")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
