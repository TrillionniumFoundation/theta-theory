#!/usr/bin/env python3
"""Pruned depth-8 probe of Round277's depth-4 face residuals.

Strictly different complete signatures are terminal on their certified closed
cells and are therefore pruned.  Only unresolved active-factor cells are
refined.  Newly found MATCH patches receive correctly oriented inward corridor
probes.  Every row remains zero-credit.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import multiprocessing as mp
import pickle
from pathlib import Path

import cm2_round276_source_g_collar_region_face_binding_probe as P
import cm2_round277_source_g_collar_common_face_match_probe as R277

HERE = Path(__file__).resolve().parent
DEPTH_LIMIT = 8


def load_depth4_ledger():
    path = HERE / "cm2_round277_source_g_depth4_residual_indices_zero_credit.json.gz"
    return json.loads(gzip.decompress(path.read_bytes()))


def install_candidate_universe():
    cache = Path("/tmp/cm2_round277_candidate_runtime_cache.pkl")
    if cache.exists():
        R277.CAND, R277.BOX, R277.TABLES = pickle.loads(cache.read_bytes())
    else:
        R277.build()
        cache.write_bytes(
            pickle.dumps((R277.CAND, R277.BOX, R277.TABLES), protocol=pickle.HIGHEST_PROTOCOL)
        )


def split(rect):
    widths = [x[1] - x[0] for x in rect]
    axis = 0 if widths[0] >= widths[1] else 1
    middle = (rect[axis][0] + rect[axis][1]) / 2
    children = []
    for side, interval in enumerate(
        ((rect[axis][0], middle), (middle, rect[axis][1]))
    ):
        child = list(rect)
        child[axis] = interval
        children.append((tuple(child), f"{axis}:{side}"))
    return children


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


def face_worker(i):
    _, _, expected, chart, target, axis, coordinate, overlap = R277.CAND[i]
    pending = [(overlap, 0, [])]
    visited = 0
    pruned = collections.Counter()
    terminal = collections.Counter()
    while pending:
        rect, depth, path = pending.pop()
        values = face_box(axis, coordinate, rect)
        signature, reasons = R277.R.dynamic_signature(
            chart,
            R277.R.atlas.AtlasBox(*values, 0, f"r277d8:{i}:{depth}"),
            target,
            R277.TABLES,
        )
        visited += 1
        if signature is not None:
            actual = P.digest(R277.payload(signature, chart))
            if actual == expected:
                return (
                    "FOUND_STRICT_POSITIVE_MATCH_PATCH",
                    i,
                    {
                        "refinement_path": path,
                        "exact_face_patch": values,
                        "visited_cell_count": visited,
                        "strict_other_pruned_histogram": dict(sorted(pruned.items())),
                    },
                )
            pruned[str(depth)] += 1
            continue
        reason = "|".join(sorted(reasons))
        if depth == DEPTH_LIMIT:
            terminal[reason] += 1
            continue
        children = split(rect)
        for child, step in children:
            pending.append((child, depth + 1, path + [step]))
    return (
        "FAILCLOSED_NO_MATCH_PATCH_AT_DEPTH8",
        i,
        {
            "visited_cell_count": visited,
            "strict_other_pruned_histogram": dict(sorted(pruned.items())),
            "depth8_unresolved_terminal_reason_histogram": dict(sorted(terminal.items())),
        },
    )


def corridor_worker(task):
    i, face_detail = task
    a, b, expected, chart, target, axis, coordinate, _ = R277.CAND[i]
    values = face_detail["exact_face_patch"]
    directions = []
    for row_id in (a, b):
        box = R277.BOX[row_id]
        negative = box[2 * axis + 1] == coordinate
        positive = box[2 * axis] == coordinate
        if negative == positive:
            return ("FAILCLOSED_INVALID_FACE_ORIENTATION", i, None)
        directions.append((row_id, negative))
    if sum(int(negative) for _, negative in directions) != 1:
        return ("FAILCLOSED_INVALID_FACE_ORIENTATION", i, None)
    rows = []
    for row_id, negative in directions:
        box = R277.BOX[row_id]
        span = box[2 * axis + 1] - box[2 * axis]
        accepted = None
        for depth in range(1, 25):
            corridor = list(values)
            width = span / (2**depth)
            corridor[2 * axis : 2 * axis + 2] = (
                [coordinate - width, coordinate]
                if negative
                else [coordinate, coordinate + width]
            )
            if R277.evaluate(
                chart, target, expected, corridor, f"r277d8:{i}:corridor:{depth}"
            ):
                accepted = {
                    "leaf_row_id": row_id,
                    "side": "NEGATIVE_SIDE_INWARD" if negative else "POSITIVE_SIDE_INWARD",
                    "dyadic_normal_depth": depth,
                    "exact_corridor_box": corridor,
                }
                break
        if accepted is None:
            return ("FAILCLOSED_NO_TWO_SIDED_INWARD_CORRIDOR", i, None)
        rows.append(accepted)
    return ("ACCEPT_TWO_INWARD_CORRIDORS", i, rows)


def parallel(worker, tasks, processes, progress_total):
    result = []
    counts = collections.Counter()
    ctx = mp.get_context("fork")
    with ctx.Pool(processes) as pool:
        for row in pool.imap_unordered(worker, tasks, chunksize=16):
            result.append(row)
            counts[row[0]] += 1
            if len(result) % 10000 == 0:
                print(
                    json.dumps(
                        {
                            "progress": len(result),
                            "total": progress_total,
                            "histogram": dict(sorted(counts.items())),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    return result, counts


def jsonable(value):
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return str(value) if value.__class__.__name__ == "Fraction" else value


def write_gzip(path, payload):
    raw = (json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")) + "\n").encode()
    path.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--processes", type=int, default=min(40, mp.cpu_count()))
    args = ap.parse_args()
    install_candidate_universe()
    depth4 = load_depth4_ledger()
    rows4 = {row["candidate_index"]: row for row in depth4["rows"]}
    indices = sorted(rows4)
    assert len(R277.CAND) == 330724
    assert len(indices) == depth4["residual_count"] == 89792
    assert P.digest(indices) == depth4["candidate_indices_sha256"]

    face_results, face_counts = parallel(face_worker, indices, args.processes, len(indices))
    found = {i: detail for status, i, detail in face_results if status == "FOUND_STRICT_POSITIVE_MATCH_PATCH"}
    residual = {i: detail for status, i, detail in face_results if status == "FAILCLOSED_NO_MATCH_PATCH_AT_DEPTH8"}
    assert len(found) + len(residual) == len(indices)

    corridor_results, corridor_counts = parallel(
        corridor_worker, sorted(found.items()), args.processes, len(found)
    )
    corridor = {
        i: detail
        for status, i, detail in corridor_results
        if status == "ACCEPT_TWO_INWARD_CORRIDORS"
    }
    failed_corridor = sorted(set(found) - set(corridor))

    accepted_rows = []
    for i in sorted(corridor):
        accepted_rows.append(
            {
                "candidate_index": i,
                "depth4_classification": rows4[i],
                "depth8_match_patch": found[i],
                "two_inward_corridors": corridor[i],
            }
        )
    residual_rows = []
    for i in sorted(residual):
        residual_rows.append(
            {
                "candidate_index": i,
                "depth4_classification": rows4[i],
                "depth8_failclosed_search": residual[i],
            }
        )

    accepted_payload = {
        "status": "ROUND277_DEPTH8_NEW_MATCH_PATCH_LEDGER__ZERO_CREDIT",
        "source_depth4_residual_count": len(indices),
        "accepted_patch_and_corridor_count": len(accepted_rows),
        "rows": accepted_rows,
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    residual_payload = {
        "status": "ROUND277_DEPTH8_RESIDUAL_LEDGER__ZERO_CREDIT",
        "source_depth4_residual_count": len(indices),
        "depth8_residual_count": len(residual_rows),
        "candidate_indices_sha256": P.digest(sorted(residual)),
        "rows": residual_rows,
        "strict_warning": "FINITE_DEPTH_NO_MATCH_IS FAIL-CLOSED, NOT ABSENCE",
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    accepted_path = HERE / "cm2_round277_source_g_depth8_new_match_patches_zero_credit.json.gz"
    residual_path = HERE / "cm2_round277_source_g_depth8_residual_indices_zero_credit.json.gz"
    accepted_file_sha = write_gzip(accepted_path, accepted_payload)
    residual_file_sha = write_gzip(residual_path, residual_payload)

    by_family_status = collections.Counter()
    by_round_status = collections.Counter()
    unresolved_reasons = collections.Counter()
    visited = collections.Counter()
    for i in indices:
        status = "FOUND" if i in found else "RESIDUAL"
        row = rows4[i]
        family = next(
            key.split(":", 2)[1]
            for key, _ in row["depth4_terminal_profile"]
            if key.startswith("REJECT:")
        )
        by_family_status[(family, status)] += 1
        by_round_status[(row["round_pair"], status)] += 1
        detail = found.get(i, residual.get(i))
        visited[status] += detail["visited_cell_count"]
        if i in residual:
            unresolved_reasons.update(
                residual[i]["depth8_unresolved_terminal_reason_histogram"]
            )

    result = {
        "status": "ROUND277_DEPTH8_RESIDUAL_PATCH_PROBE__ZERO_CREDIT",
        "source_depth4_residual_count": len(indices),
        "face_depth_limit": DEPTH_LIMIT,
        "safe_pruning_rule": "STRICT_DIFFERENT_COMPLETE_SIGNATURE_ON_CLOSED_CELL",
        "face_disposition_histogram": dict(sorted(face_counts.items())),
        "corridor_disposition_histogram": dict(sorted(corridor_counts.items())),
        "new_match_patch_count": len(found),
        "new_two_inward_corridor_count": len(corridor),
        "corridor_failure_count": len(failed_corridor),
        "remaining_depth8_failclosed_count": len(residual),
        "by_active_family_and_status": {
            "|".join(key): count for key, count in sorted(by_family_status.items())
        },
        "by_round_pair_and_status": {
            "|".join(key): count for key, count in sorted(by_round_status.items())
        },
        "depth8_residual_unresolved_terminal_reason_histogram": dict(
            sorted(unresolved_reasons.items())
        ),
        "face_evaluator_visited_cell_count_by_status": dict(sorted(visited.items())),
        "accepted_witness_rows_sha256": P.digest(jsonable(accepted_rows)),
        "residual_candidate_indices_sha256": P.digest(sorted(residual)),
        "accepted_ledger": accepted_path.name,
        "accepted_ledger_file_sha256": accepted_file_sha,
        "residual_ledger": residual_path.name,
        "residual_ledger_file_sha256": residual_file_sha,
        "strict_interpretation": [
            "DEPTH8 RESIDUALS REMAIN FAIL-CLOSED AND ARE NOT ABSENCE CERTIFICATES",
            "ALL PATCHES AND CORRIDORS REMAIN PROBE-LEVEL AND EARN ZERO CREDIT",
        ],
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
