#!/usr/bin/env python3
"""Exact registered-side quotient of the Round-87 physical port frontier.

This is deliberately a combinatorial certificate over two pinned analytic
certificates.  It does not continue a tangent branch outside the registered
box union.  Its purpose is to remove the large false ambiguity caused by
calling every one of the 2,108 registered arcs a live physical continuation
candidate.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PORTS = HERE / "cm2-round85-rank3-registered-arc-port-census-2026-07-22.json"
EVENTS = HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json"
PINS = {
    PORTS.name: "11feee98133d133ecc20654389dd559fa1fbd06f9210ef10d52ec6d86f479f2d",
    EVENTS.name: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    "cm2_round85_rank3_registered_arc_port_generator.py": "ee50e212ab9bdd6c649ec56b5d94b162db198ec6cbdded0d3cd4a540a47fe124",
    "cm2_round87_rank3_port_event_continuation_cert.py": "71f10cde22ea191c7710090e2e7474fdbc2925ded94fe60071159b2c262dc834",
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def reject_nonfinite(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load(path: Path, schema: str) -> dict[str, Any]:
    document = json.loads(path.read_text(), object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError(f"non-closed upstream document: {path.name}")
    if document["schema"] != schema or document["result_sha256"] != digest(document["result"]):
        raise RuntimeError(f"invalid upstream document: {path.name}")
    return document["result"]


def build() -> dict[str, Any]:
    for name, expected in PINS.items():
        if file_sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    census = load(PORTS, "cm2.round85.rank3-registered-arc-port-census.v1")
    events = load(EVENTS, "cm2.round87.rank3-port-event-continuation.v1")
    event_by_port = {row["registered_port_id"]: row for row in events["port_event_rows"]}
    if len(event_by_port) != 3212:
        raise RuntimeError("Round87 event rows are not a bijection on non-source ports")
    ports_by_component: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for port in census["port_rows"]:
        ports_by_component[port["physical_root_component_id"]].append(port)

    rows = []
    totals: Counter[tuple[str, str]] = Counter()
    exact_pair_rows = []
    for component in sorted(census["component_rows"], key=lambda row: row["physical_root_component_id"]):
        component_id = component["physical_root_component_id"]
        ports = ports_by_component[component_id]
        source_ids = sorted(p["registered_port_id"] for p in ports if p["port_scope"] == "SOURCE_CORE_BOUNDARY")
        non_source_ids = sorted(p["registered_port_id"] for p in ports if p["port_scope"] == "NON_SOURCE_REGISTERED_UNION_BOUNDARY")
        physical_ids = sorted(pid for pid in non_source_ids if event_by_port[pid]["port_is_locally_physical_third_tangency"])
        nonphysical_ids = sorted(pid for pid in non_source_ids if not event_by_port[pid]["port_is_locally_physical_third_tangency"])
        arcs = component["registered_elementary_arc_census_count"]
        if len(ports) != 2 * arcs:
            raise RuntimeError("component port/arc Euler identity failed")
        if physical_ids and nonphysical_ids:
            kind = "MIXED_NON_SOURCE_PORT_PHYSICALITY"
        elif physical_ids:
            kind = "PHYSICAL_OPEN_COMPONENT"
        elif nonphysical_ids:
            kind = "NONPHYSICAL_OPEN_COMPONENT"
        else:
            kind = "SOURCE_BOUNDARY_ONLY_COMPONENT"
        row = {
            "physical_root_component_id": component_id,
            "source_core_index": component["source_core_index"],
            "second_selected_target_id": component["second_selected_target_id"],
            "third_candidate_id": component["third_candidate_id"],
            "component_frontier_class": kind,
            "registered_elementary_arc_count": arcs,
            "source_boundary_port_ids": source_ids,
            "locally_physical_non_source_port_ids": physical_ids,
            "locally_nonphysical_non_source_port_ids": nonphysical_ids,
            "port_count_equals_twice_arc_count": True,
        }
        rows.append(row)
        totals[(kind, "components")] += 1
        totals[(kind, "arcs")] += arcs
        totals[(kind, "source_ports")] += len(source_ids)
        totals[(kind, "physical_ports")] += len(physical_ids)
        totals[(kind, "nonphysical_ports")] += len(nonphysical_ids)
        if kind == "PHYSICAL_OPEN_COMPONENT" and arcs == 1:
            endpoints = source_ids + physical_ids
            if len(endpoints) != 2:
                raise RuntimeError("single-arc physical component lacks two endpoints")
            exact_pair_rows.append({
                "physical_root_component_id": component_id,
                "registered_elementary_arc_endpoint_port_ids": sorted(endpoints),
                "pair_type": "PHYSICAL_PORT_TO_PHYSICAL_PORT" if len(physical_ids) == 2 else "SOURCE_BOUNDARY_TO_PHYSICAL_PORT",
            })

    kinds = ["SOURCE_BOUNDARY_ONLY_COMPONENT", "PHYSICAL_OPEN_COMPONENT", "NONPHYSICAL_OPEN_COMPONENT", "MIXED_NON_SOURCE_PORT_PHYSICALITY"]
    partition = {
        kind: {field: totals[(kind, field)] for field in ("components", "arcs", "source_ports", "physical_ports", "nonphysical_ports")}
        for kind in kinds
    }
    pair_hist = dict(sorted(Counter(row["pair_type"] for row in exact_pair_rows).items()))
    result = {
        "upstream_pins": PINS,
        "input_registered_box_component_count": len(rows),
        "input_registered_elementary_arc_count": census["registered_elementary_arc_census_count"],
        "input_registered_port_count": census["certified_registered_port_count"],
        "component_frontier_partition": partition,
        "mixed_non_source_port_physicality_component_count": partition["MIXED_NON_SOURCE_PORT_PHYSICALITY"]["components"],
        "live_global_physical_continuation_component_count": partition["PHYSICAL_OPEN_COMPONENT"]["components"],
        "live_global_physical_continuation_registered_arc_count": partition["PHYSICAL_OPEN_COMPONENT"]["arcs"],
        "live_global_physical_continuation_non_source_port_count": partition["PHYSICAL_OPEN_COMPONENT"]["physical_ports"],
        "exact_single_arc_registered_side_pair_count": len(exact_pair_rows),
        "exact_single_arc_pair_type_histogram": pair_hist,
        "multi_arc_live_component_count": sum(1 for row in rows if row["component_frontier_class"] == "PHYSICAL_OPEN_COMPONENT" and row["registered_elementary_arc_count"] > 1),
        "multi_arc_live_registered_arc_count": sum(row["registered_elementary_arc_count"] for row in rows if row["component_frontier_class"] == "PHYSICAL_OPEN_COMPONENT" and row["registered_elementary_arc_count"] > 1),
        "multi_arc_live_physical_port_count": sum(len(row["locally_physical_non_source_port_ids"]) for row in rows if row["component_frontier_class"] == "PHYSICAL_OPEN_COMPONENT" and row["registered_elementary_arc_count"] > 1),
        "multi_arc_live_source_port_count": sum(len(row["source_boundary_port_ids"]) for row in rows if row["component_frontier_class"] == "PHYSICAL_OPEN_COMPONENT" and row["registered_elementary_arc_count"] > 1),
        "exact_single_arc_registered_side_pair_rows": exact_pair_rows,
        "exact_single_arc_registered_side_pair_rows_sha256": digest(exact_pair_rows),
        "component_quotient_rows": rows,
        "component_quotient_rows_sha256": digest(rows),
        "strict_scope": "EXACT_REGISTERED_SIDE_COMPONENT_PORT_INCIDENCE_QUOTIENT_OVER_PINNED_ROUND85_AND_ROUND87_CERTIFICATES",
        "strict_nonclaims": [
            "NO_OUTWARD_PHYSICAL_TANGENT_BRANCH_PAIRING_IS_ASSERTED",
            "NO_MULTI_ARC_COMPONENT_PORT_PAIRING_IS_ASSERTED",
            "LOCALLY_NONPHYSICAL_AT_A_PORT_DOES_NOT_PROVE_GLOBAL_ABSENCE_OF_AN_INTERNAL_PHYSICAL_SUBARC",
            "SOURCE_CORE_BOUNDARY_PORTS_ARE_NOT_RELABELLED_AS_PHYSICAL_ENDPOINTS",
            "NO_COMPLETE_PHYSICAL_FACE_COUNT_OR_GATE5_PROMOTION_IS_ASSERTED",
        ],
    }
    if partition != {
        "SOURCE_BOUNDARY_ONLY_COMPONENT": {"components": 400, "arcs": 400, "source_ports": 800, "physical_ports": 0, "nonphysical_ports": 0},
        "PHYSICAL_OPEN_COMPONENT": {"components": 352, "arcs": 496, "source_ports": 47, "physical_ports": 945, "nonphysical_ports": 0},
        "NONPHYSICAL_OPEN_COMPONENT": {"components": 920, "arcs": 1212, "source_ports": 157, "physical_ports": 0, "nonphysical_ports": 2267},
        "MIXED_NON_SOURCE_PORT_PHYSICALITY": {"components": 0, "arcs": 0, "source_ports": 0, "physical_ports": 0, "nonphysical_ports": 0},
    }:
        raise RuntimeError("unexpected Round88 component frontier partition")
    if len(exact_pair_rows) != 320 or pair_hist != {"PHYSICAL_PORT_TO_PHYSICAL_PORT": 285, "SOURCE_BOUNDARY_TO_PHYSICAL_PORT": 35}:
        raise RuntimeError("unexpected single-arc pairing frontier")
    return {"schema": "cm2.round88.rank3-physical-port-component-quotient.v1", "result": result, "result_sha256": digest(result)}


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, separators=(",", ":"), ensure_ascii=True))
