#!/usr/bin/env python3
"""Materialize positive fixed-s=0 R2 boxes for all observed destination pairs."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from typing import Any

import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round26_q1_time2_frontier_cert as time2


SCHEMA = "cm2.round74.s0-r2-pair-witnesses.v1"
PAIR_INDEX = {
    12: (12, 19), 13: (13, 16), 15: (15, 22), 16: (16, 13),
    18: (18, 21), 19: (19, 12), 21: (21, 18), 22: (22, 15),
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def build() -> dict[str, Any]:
    cores = time2.core_cert.physical_cores()
    radius = Q(1, 10_000_000)
    rows = []
    for source_index, destination_indices in sorted(PAIR_INDEX.items()):
        source = cores[source_index]
        t_sign = -1 if source.t1 < 0 else 1
        p_sign = -1 if source_index in (12, 16, 18, 22) else 1
        for branch, destination_index in zip(("main", "narrow_corner"), destination_indices):
            t_center = t_sign * (Q(349, 500) if branch == "main" else Q(3499, 5000))
            p_center = p_sign * (Q(2, 125) if branch == "main" else Q(12, 625))
            atom = step1.Atom(
                source_index, source,
                t_center - radius, t_center + radius,
                p_center - radius, p_center + radius,
                Q(0), Q(0), "round74-witness",
            )
            first = step1.classify_atom(atom, cores)
            if first["classification"] != "SURVIVE_THROUGH_1_INNER":
                raise RuntimeError("R2 witness does not have Q1 parent")
            second = time2.classify_time2(atom, cores)
            expected_destination = step1.core_id(cores[destination_index])
            if second["classification"] != "RETURN_AT_2_INNER" or second["destination_core_id"] != expected_destination:
                raise RuntimeError("R2 witness destination mismatch")
            payload = {
                "source_core_index": source_index,
                "source_core_id": step1.core_id(source),
                "destination_core_index": destination_index,
                "destination_core_id": expected_destination,
                "branch": branch,
                "fixed_parameter": "s=0",
                "t_interval": [str(atom.t0), str(atom.t1)],
                "p_interval": [str(atom.p0), str(atom.p1)],
            }
            rows.append({
                **payload,
                "witness_box_id": "physical-s0-r2-box:" + digest(payload),
                "strict_time1_classification": first["classification"],
                "strict_time2_classification": second["classification"],
                "strict_second_owner_status": second["owner_status"],
                "selected_second_target_id": second["selected_target_id"],
                "positive_coordinate_area": str((atom.t1 - atom.t0) * (atom.p1 - atom.p0)),
                "rank0_parent_cell": "Round73 survival two-cell on the same source core",
                "rank_join_type": "strict interior containment",
            })
    rows.sort(key=canonical)
    result = {
        "positive_R2_witness_boxes": len(rows),
        "source_core_count": len({row["source_core_id"] for row in rows}),
        "source_destination_pair_count": len({(row["source_core_id"], row["destination_core_id"]) for row in rows}),
        "main_pair_count": sum(row["branch"] == "main" for row in rows),
        "narrow_corner_pair_count": sum(row["branch"] == "narrow_corner" for row in rows),
        "all_boxes_have_strict_Q1_parent": all(row["strict_time1_classification"] == "SURVIVE_THROUGH_1_INNER" for row in rows),
        "all_boxes_are_strict_R2": all(row["strict_time2_classification"] == "RETURN_AT_2_INNER" for row in rows),
        "all_boxes_have_unique_second_owner": all(row["strict_second_owner_status"] == "strict_unique_second_collision_owner" for row in rows),
        "rows": rows,
        "rows_sha256": digest(rows),
    }
    return {"schema": SCHEMA, "construction": {"arithmetic": "384-bit Arb", "box_half_width_each_coordinate": str(radius)}, "result": result}


if __name__ == "__main__":
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
