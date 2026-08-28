#!/usr/bin/env python3
"""Resolve Round-77 carrier tubes into source-labelled grid components."""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import sys
from collections import Counter, defaultdict, deque
from typing import Any

import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_round77_boundary_taxonomy_generator as taxonomy


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def grid_cell(path: str) -> tuple[int, int]:
    if len(path) != 20:
        raise RuntimeError("expected depth-20 path")
    return int(path[0::2], 2), int(path[1::2], 2)


def components(cells: set[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    remaining = set(cells)
    result = []
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        queue = deque([seed])
        component = []
        while queue:
            cell = queue.popleft()
            component.append(cell)
            i, j = cell
            for neighbor in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    queue.append(neighbor)
        component.sort()
        result.append(component)
    result.sort(key=lambda row: row[0])
    return result


def build(workers: int) -> dict[str, Any]:
    cores = time2.core_cert.physical_cores()
    context = mp.get_context("fork")
    with context.Pool(
        workers, initializer=taxonomy.init_worker, initargs=(cores, 20)
    ) as pool:
        core_rows = pool.map(taxonomy.process_core, range(len(cores)))
    carrier_cells: dict[tuple[int, str], set[tuple[int, int]]] = defaultdict(set)
    carrier_paths: dict[tuple[int, str], list[str]] = defaultdict(list)
    outer_count = 0
    for core in core_rows:
        for row in core["outer_rows"]:
            outer_count += 1
            cell = grid_cell(row["dyadic_path"])
            for carrier in row["carriers"]:
                key = (row["source_core_index"], carrier)
                carrier_cells[key].add(cell)
                carrier_paths[key].append(row["dyadic_path"])
    if outer_count != 263072:
        raise RuntimeError("outer count changed")
    pair_rows = []
    component_count = 0
    for (source_core_index, carrier), cells in sorted(carrier_cells.items()):
        component_rows = []
        for rank, component in enumerate(components(cells)):
            component_count += 1
            iset = [cell[0] for cell in component]
            jset = [cell[1] for cell in component]
            endpoints = sorted(
                cell for cell in component
                if sum((cell[0] + di, cell[1] + dj) in cells for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1))) <= 1
            )
            by_p: dict[int, list[int]] = defaultdict(list)
            by_t: dict[int, list[int]] = defaultdict(list)
            for i, j in component:
                by_p[j].append(i)
                by_t[i].append(j)
            component_rows.append({
                "connected_rank": rank,
                "cell_count": len(component),
                "grid_bbox_half_open": [min(iset), max(iset) + 1, min(jset), max(jset) + 1],
                "endpoint_cells": [list(cell) for cell in endpoints],
                "p_slice_envelopes": [
                    [j, min(indices), max(indices) + 1, len(indices)]
                    for j, indices in sorted(by_p.items())
                ],
                "t_slice_envelopes": [
                    [i, min(indices), max(indices) + 1, len(indices)]
                    for i, indices in sorted(by_t.items())
                ],
                "cell_set_sha256": digest(component),
            })
        paths = sorted(carrier_paths[(source_core_index, carrier)])
        pair_rows.append({
            "source_core_index": source_core_index,
            "source_core_id": time2.step1.core_id(cores[source_core_index]),
            "carrier": carrier,
            "leaf_count": len(paths),
            "connected_component_count": len(component_rows),
            "components": component_rows,
            "path_set_sha256": digest(paths),
        })
    family_hist = Counter()
    for row in pair_rows:
        carrier = row["carrier"]
        family = (
            "time1_destination" if carrier.startswith("TIME1_DESTINATION_FACE:")
            else "time2_tangency" if carrier.startswith("SECOND_CANDIDATE:")
            else "time2_destination" if carrier.startswith("TIME2_DESTINATION_CORE:")
            else "outgoing_seam_geometry"
        )
        family_hist[family] += row["connected_component_count"]
    return {
        "schema": "cm2.round78.carrier-components.v1",
        "result": {
            "fixed_parameter": "s=0",
            "dyadic_depth": 20,
            "grid_shape_per_core": [1024, 1024],
            "outer_leaf_count": outer_count,
            "source_carrier_pair_count": len(pair_rows),
            "connected_component_count": component_count,
            "component_family_histogram": dict(sorted(family_hist.items())),
            "pair_rows": pair_rows,
            "pair_rows_sha256": digest(pair_rows),
            "scope": "connected components of the certified Round-77 interval tube cover; not yet physical equality curves",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=16)
    args = parser.parse_args()
    json.dump(build(args.workers), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
