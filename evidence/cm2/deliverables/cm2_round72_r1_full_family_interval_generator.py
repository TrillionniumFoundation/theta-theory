#!/usr/bin/env python3
"""Arb generator for the full base-fibre R1 family classification proof."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as adaptive_cert
import cm2_gate5_round28_limiting_physical_face_atlas_frontier_cert as atlas_cert


HERE = Path(__file__).resolve().parent
WITNESSES = HERE / "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json"
SCHEMA = "cm2.round72.r1-full-family-interval-proof.v1"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def maybe_equal(interval: arb, value: Q) -> bool:
    point = adaptive_cert.arbq(value)
    return not bool(interval < point) and not bool(interval > point)


def overlap(interval: arb, lower: Q, upper: Q) -> bool:
    return not bool(interval < adaptive_cert.arbq(lower)) and not bool(interval > adaptive_cert.arbq(upper))


def exclusion_reason(geometry: dict[str, arb], face: dict[str, Any], destination: Any) -> str | None:
    cell = destination.chart_id.split(":")[1]
    normal_x, normal_y = geometry["normal_x"], geometry["normal_y"]
    if cell == "E" and bool(normal_x < 0):
        return "chart_E_normal_x_strict_negative"
    if cell == "W" and bool(normal_x > 0):
        return "chart_W_normal_x_strict_positive"
    if cell == "N" and bool(normal_y < 0):
        return "chart_N_normal_y_strict_negative"
    if cell == "S" and bool(normal_y > 0):
        return "chart_S_normal_y_strict_positive"
    target_t = normal_y if cell in ("E", "W") else normal_x
    target_p = geometry["p_target"]
    if face["coordinate"] == "t":
        level_interval, level = target_t, Q(face["coordinate_value"])
        other_interval, other_lower, other_upper = target_p, destination.p0, destination.p1
    else:
        level_interval, level = target_p, Q(face["coordinate_value"])
        other_interval, other_lower, other_upper = target_t, destination.t0, destination.t1
    if bool(level_interval < adaptive_cert.arbq(level)):
        return "level_interval_strict_below"
    if bool(level_interval > adaptive_cert.arbq(level)):
        return "level_interval_strict_above"
    if bool(other_interval < adaptive_cert.arbq(other_lower)):
        return "other_coordinate_strict_below_face"
    if bool(other_interval > adaptive_cert.arbq(other_upper)):
        return "other_coordinate_strict_above_face"
    return None


def geometry(core: Any, box: tuple[Q, Q, Q, Q, str]) -> dict[str, arb]:
    t0, t1, p0, p1, path = box
    value = adaptive_cert.atom_geometry(
        adaptive_cert.Atom(0, core, t0, t1, p0, p1, Q(0), Q(0), path)
    )
    if value is None:
        raise RuntimeError(f"unresolved collision geometry: {core.chart_id}:{path}")
    return value


def split(core: Any, box: tuple[Q, Q, Q, Q, str]) -> tuple[tuple[Q, Q, Q, Q, str], ...]:
    t0, t1, p0, p1, path = box
    t_scale = (t1 - t0) / (core.t1 - core.t0)
    p_scale = (p1 - p0) / (core.p1 - core.p0)
    if t_scale >= p_scale:
        middle = (t0 + t1) / 2
        return ((t0, middle, p0, p1, path + "0"), (middle, t1, p0, p1, path + "1"))
    middle = (p0 + p1) / 2
    return ((t0, t1, p0, middle, path + "0"), (t0, t1, middle, p1, path + "1"))


def build_proof() -> dict[str, Any]:
    witness_document = json.loads(WITNESSES.read_text(encoding="utf-8"))
    positive_ids = sorted(row["candidate_family_id"] for row in witness_document["rows"])
    positive_keys = {(row["source_core_id"], row["destination_face_id"])
                     for row in witness_document["rows"]}
    cores = core_cert.physical_cores()
    core_by_id = {adaptive_cert.core_id(core): core for core in cores}
    faces, face_registry = atlas_cert.core_face_registry()
    face_by_id = {row["immutable_face_id"]: row for row in faces}
    families, family_registry = atlas_cert.r1_core_preimage_seed_registry(faces)
    families_by_source: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    for family in families:
        families_by_source[family["source_core_id"]].append(
            (family, face_by_id[family["destination_core_face_id"]])
        )

    source_rows = []
    empty_ids: list[str] = []
    total_tests = 0
    total_leaves = 0
    global_reasons: Counter[str] = Counter()
    for source_index, core in enumerate(cores):
        source_id = adaptive_cert.core_id(core)
        unknown = [(family, face) for family, face in families_by_source[source_id]
                   if (source_id, face["immutable_face_id"]) not in positive_keys]
        empty_ids.extend(family["immutable_face_family_id"] for family, _face in unknown)
        root = (core.t0, core.t1, core.p0, core.p1, "")
        stack: list[tuple[tuple[Q, Q, Q, Q, str], list[tuple[dict[str, Any], dict[str, Any]]], int]] = [
            (root, unknown, 0)
        ]
        leaves = []
        tests = 0
        maximum_depth = 0
        while stack:
            box, candidates, depth = stack.pop()
            output = geometry(core, box)
            tests += 1
            exclusions = []
            possible = []
            for family, face in candidates:
                destination = core_by_id[face["core_id"]]
                reason = exclusion_reason(output, face, destination)
                if reason is None:
                    possible.append((family, face))
                else:
                    exclusions.append((family["immutable_face_family_id"], reason))
            if possible:
                if depth >= 24:
                    raise RuntimeError(f"unresolved family at depth 24: {source_index}:{box[-1]}")
                for child in reversed(split(core, box)):
                    stack.append((child, possible, depth + 1))
                continue
            histogram = Counter(reason for _family_id, reason in exclusions)
            global_reasons.update(histogram)
            leaves.append({
                "dyadic_path": box[-1],
                "depth": depth,
                "candidate_count_on_entry": len(candidates),
                "excluded_candidate_count": len(exclusions),
                "exclusion_reason_histogram": dict(sorted(histogram.items())),
                "exclusion_rows_sha256": digest(sorted(exclusions)),
                "possible_unknown_family_count": 0,
            })
            maximum_depth = max(maximum_depth, depth)
        leaves.sort(key=lambda row: row["dyadic_path"])
        source_rows.append({
            "source_core_index": source_index,
            "source_core_id": source_id,
            "positive_family_count": 48 - len(unknown),
            "certified_empty_family_count": len(unknown),
            "tree_test_count": tests,
            "leaf_count": len(leaves),
            "maximum_depth": maximum_depth,
            "leaf_paths_sha256": digest([row["dyadic_path"] for row in leaves]),
            "leaf_rows": leaves,
        })
        total_tests += tests
        total_leaves += len(leaves)

    all_ids = sorted(positive_ids + empty_ids)
    if len(set(positive_ids)) != 32 or len(set(empty_ids)) != 1120 or len(set(all_ids)) != 1152:
        raise RuntimeError("family classification counts")
    if digest(all_ids) != family_registry["family_ids_sha256"]:
        raise RuntimeError("family registry digest")
    return {
        "schema": SCHEMA,
        "engine": {
            "arithmetic": "python-flint arb outward ball arithmetic",
            "parameter": "s=0",
            "split_rule": "bisect larger normalized t/p width; t on ties",
            "maximum_allowed_depth": 24,
            "chart_sign_test_included": True,
            "corner_endpoint_policy": "zero_collision_line_measure_cemetery",
        },
        "classification": {
            "candidate_family_count": 1152,
            "positive_family_count": 32,
            "certified_empty_family_count": 1120,
            "unresolved_family_count": 0,
            "positive_family_ids": positive_ids,
            "certified_empty_family_ids": sorted(empty_ids),
            "all_family_ids_sha256": digest(all_ids),
            "frozen_registry_family_ids_sha256": family_registry["family_ids_sha256"],
        },
        "tree_audit": {
            "source_core_count": 24,
            "total_interval_map_test_count": total_tests,
            "total_leaf_count": total_leaves,
            "global_maximum_depth": max(row["maximum_depth"] for row in source_rows),
            "global_exclusion_reason_histogram": dict(sorted(global_reasons.items())),
            "source_rows_sha256": digest(source_rows),
            "source_rows": source_rows,
        },
        "frozen_seed_registry": {
            "physical_core_face_count": face_registry["materialized_physical_core_face_count"],
            "candidate_family_count": family_registry["materialized_candidate_R1_core_preimage_equation_family_count"],
            "family_ids_sha256": family_registry["family_ids_sha256"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_proof()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(payload)
    else:
        args.output.write_text(payload, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
