#!/usr/bin/env python3
"""Materialize strict face patches for all Round277 depth-8 residual edges.

The search is seeded by exact active-factor normal forms, not by blind uniform
refinement.  Regular cells use a strictly signed extremal point on the
requested side.  The p=+/-1 tails use a strict requested boundary segment and
only thicken that segment inward.  Acceptance still requires a positive-area
face rectangle plus one correctly oriented positive-volume corridor in each
incident leaf.

This remains a zero-credit probe.  A formal producer and independent verifier
must reconstruct these witnesses before any component union.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import multiprocessing as mp
from fractions import Fraction as Q
from pathlib import Path

from flint import ctx

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement as r179
import cm2_round276_source_g_collar_region_face_binding_probe as r276
import cm2_round277_source_g_collar_common_face_match_probe as r277
import cm2_round277_source_g_depth8_residual_active_graph_strategy_probe as strategy


HERE = Path(__file__).resolve().parent
GROUPS = []


def jsonable(value):
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    if isinstance(value, Q):
        return str(value)
    return value


def point_coordinates(point):
    return (point.t0, point.p0, point.s0)


def point_box(coordinates, label):
    return r174.atlas.AtlasBox(
        coordinates[0],
        coordinates[0],
        coordinates[1],
        coordinates[1],
        coordinates[2],
        coordinates[2],
        0,
        label,
    )


def signature_hash(chart, target, box):
    signature, rejected = r174.dynamic_signature(
        chart, box, target, strategy.TABLES
    )
    if signature is None:
        return None, tuple(rejected)
    return r276.digest(r277.payload(signature, chart)), ()


def active_derivative_signs(chart, target, axis, coordinate, rect, reason):
    box = strategy.make_box(axis, coordinate, rect, "round277-seed-derivative")
    dual = strategy.active_dual(r179.interval_geometry(chart, target, box), reason)
    return [
        None
        if value is None
        else "EXACT_ZERO"
        if value == 0
        else r179.sign(value)
        for value in dual[1]
    ]


def extremal_points(axis, coordinate, rect, derivative_signs):
    rows = []
    for want_maximum in (False, True):
        coordinates = []
        j = 0
        for k in range(3):
            if k == axis:
                coordinates.append(coordinate)
                continue
            lower, upper = rect[j]
            j += 1
            sign = derivative_signs[k]
            if sign == "STRICT_POSITIVE":
                coordinates.append(upper if want_maximum else lower)
            elif sign == "STRICT_NEGATIVE":
                coordinates.append(lower if want_maximum else upper)
            elif sign == "EXACT_ZERO":
                coordinates.append((lower + upper) / 2)
            else:
                return []
        rows.append(tuple(coordinates))
    return rows


def midpoint(axis, coordinate, rect):
    result = []
    j = 0
    for k in range(3):
        if k == axis:
            result.append(coordinate)
        else:
            lower, upper = rect[j]
            j += 1
            result.append((lower + upper) / 2)
    return tuple(result)


def regular_seed(expected, chart, target, axis, coordinate, rect, reason):
    classification, _source, _tangent, _detail = strategy.classify_active_cell(
        chart, target, axis, coordinate, rect, reason
    )
    if classification == "ACTIVE_EQUALITY_ZERO_SET_ABSENT_BY_WHOLE_CELL_SIGN":
        points = [midpoint(axis, coordinate, rect)]
    elif classification in {
        "ACTIVE_EQUALITY_ZERO_SET_ABSENT_BY_EXTREMA",
        "ACTIVE_EQUALITY_REGULAR_MONOTONE_GRAPH",
    }:
        derivatives = active_derivative_signs(
            chart, target, axis, coordinate, rect, reason
        )
        points = extremal_points(axis, coordinate, rect, derivatives)
    else:
        return None
    for coordinates in points:
        actual, rejected = signature_hash(
            chart, target, point_box(coordinates, "round277-seed-point")
        )
        if actual == expected:
            return {
                "seed_kind": "STRICT_ACTIVE_FACTOR_SIDE_EXTREMUM",
                "active_reason": reason,
                "seed_point": coordinates,
            }
    return None


def endpoint_line_seed(expected, chart, target, axis, coordinate, rect, reason):
    if reason != "outgoing_chart_seam" or axis != 2:
        return None
    for endpoint in (Q(-1), Q(1)):
        if endpoint not in rect[1]:
            continue
        line_rect = (rect[0], (endpoint, endpoint))
        line = strategy.make_box(
            axis, coordinate, line_rect, "round277-p-endpoint-line"
        )
        actual, rejected = signature_hash(chart, target, line)
        if actual == expected:
            return {
                "seed_kind": "STRICT_P_ENDPOINT_BOUNDARY_SEGMENT",
                "active_reason": reason,
                "p_endpoint": endpoint,
                "strict_t_interval": rect[0],
            }
    return None


def face_patch_around_point(
    expected, chart, target, axis, coordinate, rect, coordinates
):
    tangential_axes = [k for k in range(3) if k != axis]
    for depth in range(1, 49):
        patch_rect = []
        for tangent_index, k in enumerate(tangential_axes):
            lower, upper = rect[tangent_index]
            value = coordinates[k]
            span = upper - lower
            width = span / (2**depth)
            if value == lower:
                interval = (lower, lower + width)
            elif value == upper:
                interval = (upper - width, upper)
            else:
                half = min(value - lower, upper - value) / (2**depth)
                if half <= 0:
                    break
                interval = (value - half, value + half)
            patch_rect.append(interval)
        else:
            patch = strategy.make_box(
                axis, coordinate, tuple(patch_rect), "round277-extremal-patch"
            )
            actual, rejected = signature_hash(chart, target, patch)
            if actual == expected:
                return patch, depth
    return None, None


def face_patch_from_endpoint_segment(
    expected, chart, target, axis, coordinate, rect, endpoint
):
    p_lower, p_upper = rect[1]
    inward_span = (
        p_upper - endpoint if endpoint == p_lower else endpoint - p_lower
    )
    assert inward_span > 0
    for depth in range(1, 65):
        width = inward_span / (2**depth)
        p_interval = (
            (endpoint, endpoint + width)
            if endpoint == p_lower
            else (endpoint - width, endpoint)
        )
        patch_rect = (rect[0], p_interval)
        patch = strategy.make_box(
            axis, coordinate, patch_rect, "round277-endpoint-wedge-patch"
        )
        actual, rejected = signature_hash(chart, target, patch)
        if actual == expected:
            return patch, depth
    return None, None


def box_payload(box):
    return [
        box.t0,
        box.t1,
        box.p0,
        box.p1,
        box.s0,
        box.s1,
    ]


def corridors(candidate_index, face_patch):
    a, b, expected, chart, target, axis, coordinate, _overlap = r277.CAND[
        candidate_index
    ]
    q = box_payload(face_patch)
    result = []
    for row_id in (a, b):
        leaf = r277.BOX[row_id]
        negative = leaf[2 * axis + 1] == coordinate
        positive = leaf[2 * axis] == coordinate
        if negative == positive:
            return None
        span = leaf[2 * axis + 1] - leaf[2 * axis]
        accepted = None
        for depth in range(1, 41):
            corridor = list(q)
            width = span / (2**depth)
            corridor[2 * axis : 2 * axis + 2] = (
                [coordinate - width, coordinate]
                if negative
                else [coordinate, coordinate + width]
            )
            box = r174.atlas.AtlasBox(
                *corridor, 0, "round277-materialized-corridor"
            )
            actual, rejected = signature_hash(chart, target, box)
            if actual == expected:
                accepted = {
                    "leaf_row_id": row_id,
                    "geometric_side": (
                        "NEGATIVE_SIDE_INWARD"
                        if negative
                        else "POSITIVE_SIDE_INWARD"
                    ),
                    "dyadic_normal_depth": depth,
                    "exact_corridor_box": corridor,
                }
                break
        if accepted is None:
            return None
        result.append(accepted)
    if sum(row["geometric_side"] == "NEGATIVE_SIDE_INWARD" for row in result) != 1:
        return None
    return result


def worker(group_index):
    (
        _a,
        _b,
        chart,
        target,
        axis,
        coordinate,
        overlap,
        hashes,
        indices,
    ) = GROUPS[group_index]
    assert len(indices) == len(hashes) == 1
    candidate_index = indices[0]
    expected = next(iter(hashes))
    endpoint_seeds = []
    for kind, rect, path, signature, reasons in strategy.terminal_cells(
        chart, target, axis, coordinate, overlap
    ):
        if kind != "ACTIVE" or len(reasons) != 1:
            continue
        reason = reasons[0]
        seed = regular_seed(
            expected, chart, target, axis, coordinate, rect, reason
        )
        if seed is not None:
            patch, patch_depth = face_patch_around_point(
                expected,
                chart,
                target,
                axis,
                coordinate,
                rect,
                seed["seed_point"],
            )
            if patch is not None:
                inward = corridors(candidate_index, patch)
                if inward is not None:
                    return (
                        "PASS_REGULAR_ACTIVE_SIDE_PATCH_AND_TWO_CORRIDORS",
                        candidate_index,
                        {
                            **seed,
                            "source_depth8_refinement_path": path,
                            "dyadic_tangent_shrink_depth": patch_depth,
                            "exact_positive_area_face_patch": box_payload(patch),
                            "two_inward_corridors": inward,
                        },
                    )
        endpoint = endpoint_line_seed(
            expected, chart, target, axis, coordinate, rect, reason
        )
        if endpoint is not None:
            endpoint_seeds.append((rect, path, endpoint))
    for rect, path, seed in endpoint_seeds:
        patch, patch_depth = face_patch_from_endpoint_segment(
            expected,
            chart,
            target,
            axis,
            coordinate,
            rect,
            seed["p_endpoint"],
        )
        if patch is None:
            continue
        inward = corridors(candidate_index, patch)
        if inward is None:
            continue
        return (
            "PASS_P_ENDPOINT_WEDGE_PATCH_AND_TWO_CORRIDORS",
            candidate_index,
            {
                **seed,
                "source_depth8_refinement_path": path,
                "dyadic_p_endpoint_inward_depth": patch_depth,
                "exact_positive_area_face_patch": box_payload(patch),
                "two_inward_corridors": inward,
            },
        )
    return ("FAILCLOSED_NO_STRICT_PATCH_AND_TWO_CORRIDORS", candidate_index, None)


def write_gzip(path, payload):
    raw = (
        json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode()
    path.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    global GROUPS
    parser = argparse.ArgumentParser()
    parser.add_argument("--processes", type=int, default=min(40, mp.cpu_count()))
    parser.add_argument("--limit-groups", type=int)
    args = parser.parse_args()
    ctx.prec = 256
    strategy.load_groups()
    GROUPS = strategy.GROUPS
    if args.limit_groups is not None:
        GROUPS = GROUPS[: args.limit_groups]
    results = []
    counts = collections.Counter()
    tangent_depths = collections.Counter()
    endpoint_depths = collections.Counter()
    corridor_depths = collections.Counter()
    with mp.get_context("fork").Pool(args.processes) as pool:
        for status, candidate_index, detail in pool.imap_unordered(
            worker, range(len(GROUPS)), chunksize=8
        ):
            counts[status] += 1
            results.append((status, candidate_index, detail))
            if detail is not None:
                if "dyadic_tangent_shrink_depth" in detail:
                    tangent_depths[detail["dyadic_tangent_shrink_depth"]] += 1
                if "dyadic_p_endpoint_inward_depth" in detail:
                    endpoint_depths[detail["dyadic_p_endpoint_inward_depth"]] += 1
                corridor_depths.update(
                    row["dyadic_normal_depth"]
                    for row in detail["two_inward_corridors"]
                )
            if len(results) % 5000 == 0:
                print(
                    json.dumps(
                        {
                            "progress": len(results),
                            "total": len(GROUPS),
                            "histogram": dict(sorted(counts.items())),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    results.sort(key=lambda row: row[1])
    rows = [
        {
            "candidate_index": candidate_index,
            "witness_classification": status,
            **detail,
        }
        for status, candidate_index, detail in results
        if detail is not None
    ]
    ledger = {
        "status": "ROUND277_DEPTH8_ACTIVE_GRAPH_FACE_EDGE_WITNESSES__ZERO_CREDIT",
        "row_count": len(rows),
        "candidate_indices_sha256": r276.digest(
            [row["candidate_index"] for row in rows]
        ),
        "rows_sha256": r276.digest(jsonable(rows)),
        "rows": rows,
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    ledger_path = (
        HERE
        / "cm2_round277_source_g_depth8_active_graph_face_edge_witnesses_zero_credit.json.gz"
    )
    ledger_sha = write_gzip(ledger_path, ledger)
    result = {
        "status": "ROUND277_DEPTH8_ACTIVE_GRAPH_PATCH_CORRIDOR_MATERIALIZATION_PROBE__ZERO_CREDIT",
        "input_depth8_residual_edge_count": len(GROUPS),
        "disposition_histogram": dict(sorted(counts.items())),
        "strict_positive_area_face_patch_count": len(rows),
        "inward_corridor_witness_count": 2 * len(rows),
        "remaining_failclosed_edge_count": len(GROUPS) - len(rows),
        "tangent_shrink_depth_histogram": dict(sorted(tangent_depths.items())),
        "p_endpoint_inward_depth_histogram": dict(sorted(endpoint_depths.items())),
        "normal_corridor_depth_histogram": dict(sorted(corridor_depths.items())),
        "witness_rows_sha256": ledger["rows_sha256"],
        "witness_ledger": ledger_path.name,
        "witness_ledger_file_sha256": ledger_sha,
        "strict_nonpromotion": ledger["strict_nonpromotion"],
    }
    result_path = (
        HERE
        / "cm2_round277_source_g_depth8_active_graph_patch_corridor_materialization_probe_result.json"
    )
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
