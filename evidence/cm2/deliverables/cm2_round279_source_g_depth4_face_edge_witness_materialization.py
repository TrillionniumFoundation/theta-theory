#!/usr/bin/env python3
"""Freeze the corrected Round277 depth-4 face/corridor witness rows."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import multiprocessing as mp
from pathlib import Path

import cm2_round276_source_g_collar_region_face_binding_probe as r276
import cm2_round277_source_g_collar_common_face_match_probe as r277
import cm2_round277_source_g_depth4_residual_zero_credit_analysis as residual


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round279_source_g_depth4_face_edge_witnesses_zero_credit.json.gz"
)
ACCEPTED = []


def jsonable(value):
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return str(value) if value.__class__.__name__ == "Fraction" else value


def patch_from_path(overlap, path):
    rect = list(overlap)
    for step in path:
        split, side = map(int, step.split(":"))
        lower, upper = rect[split]
        middle = (lower + upper) / 2
        rect[split] = (
            (lower, middle) if side == 0 else (middle, upper)
        )
    return tuple(rect)


def face_box(axis, coordinate, rect):
    values = []
    j = 0
    for k in range(3):
        if k == axis:
            values += [coordinate, coordinate]
        else:
            values += list(rect[j])
            j += 1
    return values


def worker(candidate_index):
    status, returned_index, detail = residual.corrected_worker(candidate_index)
    assert returned_index == candidate_index
    assert status == "ACCEPT_POSITIVE_MATCH_PATCH_AND_TWO_INWARD_CORRIDORS"
    path, depths = detail
    (
        a,
        b,
        signature_sha256,
        chart,
        target,
        axis,
        coordinate,
        overlap,
    ) = r277.CAND[candidate_index]
    rect = patch_from_path(overlap, path)
    patch = face_box(axis, coordinate, rect)
    corridor_rows = []
    for row_id, depth in zip((a, b), depths, strict=True):
        leaf = r277.BOX[row_id]
        negative = leaf[2 * axis + 1] == coordinate
        positive = leaf[2 * axis] == coordinate
        assert negative != positive
        width = (leaf[2 * axis + 1] - leaf[2 * axis]) / (2**depth)
        corridor = list(patch)
        corridor[2 * axis : 2 * axis + 2] = (
            [coordinate - width, coordinate]
            if negative
            else [coordinate, coordinate + width]
        )
        corridor_rows.append(
            {
                "leaf_row_id": row_id,
                "geometric_side": (
                    "NEGATIVE_SIDE_INWARD"
                    if negative
                    else "POSITIVE_SIDE_INWARD"
                ),
                "dyadic_normal_depth": depth,
                "exact_corridor_box": corridor,
            }
        )
    row = {
        "candidate_index": candidate_index,
        "witness_partition": "DEPTH4_ADAPTIVE_STRICT_PATCH",
        "negative_or_positive_endpoint_leaf_ids_lexical": [a, b],
        "complete_10_field_return_signature_sha256": signature_sha256,
        "source_chart": chart,
        "owner_target": target,
        "common_face_axis": axis,
        "common_face_coordinate": coordinate,
        "source_refinement_path": path,
        "exact_positive_area_face_patch": patch,
        "two_inward_corridors": corridor_rows,
    }
    row["row_sha256"] = r276.digest(jsonable(row))
    return row


def install():
    # Reconstruct from the frozen certificate inputs.  Formal materialization
    # must never deserialize the unpinned executable /tmp cache that was used
    # only to speed up exploratory Round277 probes.
    r277.build()
    residual.R277.CAND = r277.CAND
    residual.R277.BOX = r277.BOX
    residual.R277.TABLES = r277.TABLES
    residual.R277.FACE_DEPTH = 4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--processes", type=int, default=min(40, mp.cpu_count()))
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    install()
    depth4_path = (
        HERE
        / "cm2_round277_source_g_depth4_residual_indices_zero_credit.json.gz"
    )
    depth4 = json.loads(gzip.decompress(depth4_path.read_bytes()))
    rejected = {row["candidate_index"] for row in depth4["rows"]}
    accepted = sorted(set(range(len(r277.CAND))) - rejected)
    assert len(accepted) == 240932
    rows = []
    with mp.get_context("fork").Pool(args.processes) as pool:
        for row in pool.imap_unordered(worker, accepted, chunksize=16):
            rows.append(row)
            if len(rows) % 20000 == 0:
                print(
                    json.dumps(
                        {"progress": len(rows), "total": len(accepted)},
                        sort_keys=True,
                    ),
                    flush=True,
                )
    rows.sort(key=lambda row: row["candidate_index"])
    payload = {
        "status": "ROUND279_DEPTH4_FACE_EDGE_WITNESS_MATERIALIZATION__ZERO_CREDIT",
        "row_count": len(rows),
        "candidate_indices_sha256": r276.digest(
            [row["candidate_index"] for row in rows]
        ),
        "rows_sha256": r276.digest(jsonable(rows)),
        "row_hashes_sha256": r276.digest(
            [row["row_sha256"] for row in rows]
        ),
        "rows": rows,
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    raw = (
        json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode()
    args.output.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
    print(
        json.dumps(
            {
                "status": payload["status"],
                "row_count": len(rows),
                "candidate_indices_sha256": payload[
                    "candidate_indices_sha256"
                ],
                "rows_sha256": payload["rows_sha256"],
                "row_hashes_sha256": payload["row_hashes_sha256"],
                "file_sha256": hashlib.sha256(
                    args.output.read_bytes()
                ).hexdigest(),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
