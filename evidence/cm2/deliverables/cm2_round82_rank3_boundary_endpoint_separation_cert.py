#!/usr/bin/env python3
"""Pairwise separation audit for all refined rank-three boundary endpoints."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
ENDPOINTS = HERE / "cm2-round82-rank3-boundary-endpoints-2026-07-21.json"


def build() -> dict[str, Any]:
    rows = json.loads(ENDPOINTS.read_text())["result"]["endpoint_rows"]
    grouped: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["source_core_index"], row["source_boundary_side"])].append(row)
    group_rows = []
    total_pairs = 0
    for (source_index, side), endpoints in sorted(grouped.items()):
        endpoints.sort(key=lambda row: tuple(map(Q, row["parameter_interval"])))
        pair_count = len(endpoints) * (len(endpoints) - 1) // 2
        total_pairs += pair_count
        for left, right in zip(endpoints, endpoints[1:]):
            if Q(left["parameter_interval"][1]) >= Q(right["parameter_interval"][0]):
                raise RuntimeError(f"overlapping endpoints {left['physical_endpoint_id']} {right['physical_endpoint_id']}")
        group_rows.append({
            "source_core_index": source_index,
            "source_boundary_side": side,
            "endpoint_count": len(endpoints),
            "pair_count": pair_count,
            "ordered_endpoint_ids_sha256": digest([row["physical_endpoint_id"] for row in endpoints]),
        })
    histogram = Counter(row["endpoint_count"] for row in group_rows)
    result = {
        "certified_endpoint_count": len(rows),
        "nonempty_source_boundary_side_count": len(group_rows),
        "endpoint_count_per_side_histogram": {str(key): value for key, value in sorted(histogram.items())},
        "same_source_boundary_side_pair_count": total_pairs,
        "strictly_interval_disjoint_pair_count": total_pairs,
        "unresolved_or_overlapping_pair_count": 0,
        "directed_bisection_refinement_steps_per_endpoint": 80,
        "group_rows": group_rows,
        "group_rows_sha256": digest(group_rows),
    }
    return {"schema": "cm2.round82.rank3-boundary-endpoint-separation.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
