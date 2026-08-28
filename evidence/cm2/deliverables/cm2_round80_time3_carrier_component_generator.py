#!/usr/bin/env python3
"""Connected components of the fixed-s=0 time-three carrier seed cover."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
SEEDS = HERE / "cm2-round79-time3-carrier-seeds-2026-07-21.json"
GRID = 64


def grid_cell(path: str) -> tuple[int, int]:
    prefix, base_i, tail = path.split(":")
    base_j, suffix = tail[:-2], tail[-2:]
    if prefix != "g32" or len(suffix) != 2 or any(bit not in "01" for bit in suffix):
        raise RuntimeError(f"unexpected depth-two seed path {path}")
    return 2 * int(base_i) + int(suffix[0]), 2 * int(base_j) + int(suffix[1])


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


def build() -> dict[str, Any]:
    seeds = json.loads(SEEDS.read_text())["result"]
    carrier_cells: dict[tuple[int, str], set[tuple[int, int]]] = defaultdict(set)
    carrier_incidence_count = Counter()
    for row in seeds["seed_rows"]:
        key = (row["source_core_index"], row["carrier"])
        carrier_cells[key].add(grid_cell(row["dyadic_path"]))
        carrier_incidence_count[key] += 1
    pair_rows = []
    component_count = 0
    physical_component_count = 0
    for (source_core_index, carrier), cells in sorted(carrier_cells.items()):
        component_rows = []
        for rank, component in enumerate(components(cells)):
            component_count += 1
            if carrier.startswith("THIRD_CANDIDATE:"):
                physical_component_count += 1
            iset = [cell[0] for cell in component]
            jset = [cell[1] for cell in component]
            by_p: dict[int, list[int]] = defaultdict(list)
            by_t: dict[int, list[int]] = defaultdict(list)
            for i, j in component:
                by_p[j].append(i)
                by_t[i].append(j)
            endpoints = sorted(
                cell for cell in component
                if sum(
                    (cell[0] + di, cell[1] + dj) in cells
                    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1))
                ) <= 1
            )
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
                "cell_set": [list(cell) for cell in component],
                "cell_set_sha256": digest(component),
            })
        pair_rows.append({
            "source_core_index": source_core_index,
            "carrier": carrier,
            "seed_incidence_count": carrier_incidence_count[(source_core_index, carrier)],
            "distinct_grid_cell_count": len(cells),
            "connected_component_count": len(component_rows),
            "components": component_rows,
        })
    result = {
        "fixed_parameter": "s=0",
        "grid_shape_per_core": [GRID, GRID],
        "source_carrier_family_count": len(pair_rows),
        "connected_component_count": component_count,
        "physical_third_tangency_component_count": physical_component_count,
        "pair_rows": pair_rows,
        "pair_rows_sha256": digest(pair_rows),
        "strict_scope": "connected components of the finite depth-two time-three carrier seed cover; not yet equality curves",
    }
    return {"schema": "cm2.round80.time3-carrier-components.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
