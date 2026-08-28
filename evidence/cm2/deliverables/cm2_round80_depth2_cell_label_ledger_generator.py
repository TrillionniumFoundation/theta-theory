#!/usr/bin/env python3
"""Cell-label counts and two-sided tangency incidence for the complete depth-two quotient."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_round26_q1_time2_frontier_cert as time2
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
R1 = HERE / "cm2-round73-base-r1-quotient-vertices-2026-07-21.json"
R2 = HERE / "cm2-round75-r2-physical-curves-2026-07-21.json"
TANGENCIES = HERE / "cm2-round78-time2-tangency-curves-2026-07-21.json"


def tangency_incidence(curve: dict[str, Any], cores: tuple[Any, ...]) -> dict[str, Any]:
    slab = curve["slabs"][len(curve["slabs"]) // 2]
    parameter = tuple(map(Q, slab["parameter_interval"]))
    root = tuple(map(Q, slab["root_interval"]))
    parameter_midpoint = sum(parameter, Q()) / 2
    sides = []
    for side, root_coordinate in zip(("root_lower", "root_upper"), root):
        if curve["parameter_axis"] == "t":
            t, p = parameter_midpoint, root_coordinate
        else:
            t, p = root_coordinate, parameter_midpoint
        atom = step1.Atom(
            curve["source_core_index"], cores[curve["source_core_index"]],
            t, t, p, p, Q(0), Q(0), f"incidence:{curve['curve_id']}:{side}",
        )
        classification = time2.classify_time2(atom, cores)
        if classification["classification"] != "SURVIVE_THROUGH_2_INNER":
            raise RuntimeError(f"non-Q2 tangency side {curve['curve_id']}:{side}")
        sides.append({
            "side": side,
            "sample": {"t": str(t), "p": str(p)},
            "classification": classification["classification"],
            "owner_status": classification["owner_status"],
            "selected_target_id": classification["selected_target_id"],
            "witness_digest": classification["witness_digest"],
        })
    return {
        "physical_curve_id": curve["curve_id"],
        "source_core_index": curve["source_core_index"],
        "candidate_id": curve["candidate_id"],
        "two_sided_Q2_incidence": True,
        "side_rows": sides,
        "same_selected_owner_on_both_sides": sides[0]["selected_target_id"] == sides[1]["selected_target_id"],
    }


def build() -> dict[str, Any]:
    cores = core_cert.physical_cores()
    r1 = json.loads(R1.read_text())["result"]["rows"]
    r2_document = json.loads(R2.read_text())["result"]
    r2_components = r2_document["component_rows"]
    r2_curves = r2_document["curve_rows"]
    tangencies = json.loads(TANGENCIES.read_text())["result"]["curve_rows"]
    r1_by_core = Counter(row["source_core_index"] for row in r1)
    r2_component_by_core = Counter(row["source_core_index"] for row in r2_components)
    r2_curve_by_core = Counter(row["source_core_index"] for row in r2_curves)
    tangency_by_core = Counter(row["source_core_index"] for row in tangencies)
    cell_rows = []
    for row in r1:
        identity = {"label": "R1", "source": row["source_core_index"], "destination": row["destination_core_index"]}
        cell_rows.append({
            "cell_id": "physical-s0-depth2-cell:" + digest(identity),
            "label": "R1",
            "source_core_index": row["source_core_index"],
            "destination_core_index": row["destination_core_index"],
            "boundary_pullback_family_ids": row["pullback_family_ids"],
            "geometry_status": "CERTIFIED_ROUND73_CURVILINEAR_QUADRILATERAL",
        })
    for rank, row in enumerate(r2_components):
        identity = {"label": "R2", "source": row["source_core_index"], "destination": row["destination_core_index"], "rank": rank}
        cell_rows.append({
            "cell_id": "physical-s0-depth2-cell:" + digest(identity),
            "label": "R2",
            "source_core_index": row["source_core_index"],
            "destination_core_index": row["destination_core_index"],
            "boundary_physical_curve_ids": row["physical_curve_ids"],
            "branch": row["branch"],
            "geometry_status": "CERTIFIED_ROUND75_BOUNDARY_ATTACHED_BAND",
        })
    per_core_rows = []
    for source_index in range(len(cores)):
        q2_count = 1 + r2_curve_by_core[source_index] + tangency_by_core[source_index] - r2_component_by_core[source_index]
        if q2_count <= 0:
            raise RuntimeError("nonpositive Q2 cell count")
        for ordinal in range(q2_count):
            identity = {"label": "Q2", "source": source_index, "ordinal": ordinal}
            cell_rows.append({
                "cell_id": "physical-s0-depth2-cell:" + digest(identity),
                "label": "Q2",
                "source_core_index": source_index,
                "source_local_ordinal": ordinal,
                "geometry_status": "CERTIFIED_COUNTED_OPEN_CELL_SLOT__EXACT_BOUNDARY_WORD_PENDING",
            })
        per_core_rows.append({
            "source_core_index": source_index,
            "R1_cell_count": r1_by_core[source_index],
            "R2_cell_count": r2_component_by_core[source_index],
            "Q2_cell_count": q2_count,
            "total_cell_count": r1_by_core[source_index] + r2_component_by_core[source_index] + q2_count,
            "R2_crosscut_count": r2_curve_by_core[source_index],
            "tangency_crosscut_count": tangency_by_core[source_index],
        })
    cell_rows.sort(key=lambda row: row["cell_id"])
    incidence_rows = [tangency_incidence(curve, cores) for curve in tangencies]
    incidence_rows.sort(key=lambda row: row["physical_curve_id"])
    histogram = Counter(row["label"] for row in cell_rows)
    if histogram != Counter({"Q2": 132, "R1": 16, "R2": 16}):
        raise RuntimeError(f"cell histogram {histogram}")
    if len(cell_rows) != 164:
        raise RuntimeError("cell count")
    result = {
        "fixed_parameter": "s=0",
        "cell_count": len(cell_rows),
        "cell_label_histogram": dict(sorted(histogram.items())),
        "per_core_rows": per_core_rows,
        "per_core_rows_sha256": digest(per_core_rows),
        "cell_rows": cell_rows,
        "cell_rows_sha256": digest(cell_rows),
        "tangency_face_incidence_count": len(incidence_rows),
        "two_sided_strict_Q2_incidence_count": sum(row["two_sided_Q2_incidence"] for row in incidence_rows),
        "same_owner_both_sides_count": sum(row["same_selected_owner_on_both_sides"] for row in incidence_rows),
        "tangency_incidence_rows": incidence_rows,
        "tangency_incidence_rows_sha256": digest(incidence_rows),
        "strict_boundary": "all 164 label slots and all 92 tangency two-sided Q2 incidences are materialized; exact cyclic boundary words for the 132 Q2 slots remain pending",
        "gate4_commuting_square": "NOT_PROMOTED__EXACT_Q2_BOUNDARY_WORD_AND_CELL_MAP_ROWS_PENDING",
    }
    return {"schema": "cm2.round80.depth2-cell-label-ledger.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
