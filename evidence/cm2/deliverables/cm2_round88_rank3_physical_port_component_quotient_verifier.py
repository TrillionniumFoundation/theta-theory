#!/usr/bin/env python3
"""Independent closed-schema verifier for the Round-88 port quotient."""
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round88-rank3-physical-port-component-quotient-2026-07-22.json"
PORTS = HERE / "cm2-round85-rank3-registered-arc-port-census-2026-07-22.json"
EVENTS = HERE / "cm2-round87-rank3-port-event-continuation-2026-07-22.json"
FILE_PINS = {
    MANIFEST.name: "35e4b0ee448476837644f66a55aaaf385bcb4027c27a36fdc37f54bfb4f40d42",
    "cm2_round88_rank3_physical_port_component_quotient_cert.py": "dbeb5ebf5a48e6a14c1e8b6baabe6b15bd1949c1f2637607c269b3d255e72107",
    PORTS.name: "11feee98133d133ecc20654389dd559fa1fbd06f9210ef10d52ec6d86f479f2d",
    EVENTS.name: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
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
    raise ValueError(value)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key: {key}")
        out[key] = value
    return out


def parse(path: Path, schema: str) -> dict[str, Any]:
    doc = json.loads(path.read_text(), object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
    if set(doc) != {"schema", "result", "result_sha256"} or doc["schema"] != schema:
        raise RuntimeError("closed schema failure")
    if digest(doc["result"]) != doc["result_sha256"]:
        raise RuntimeError("digest failure")
    return doc


def independent_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, int]]]:
    census = parse(PORTS, "cm2.round85.rank3-registered-arc-port-census.v1")["result"]
    events = parse(EVENTS, "cm2.round87.rank3-port-event-continuation.v1")["result"]
    event_by_port = {row["registered_port_id"]: row for row in events["port_event_rows"]}
    ports_by_component: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for port in census["port_rows"]:
        ports_by_component[port["physical_root_component_id"]].append(port)
    rows, pairs = [], []
    totals: Counter[tuple[str, str]] = Counter()
    for component in sorted(census["component_rows"], key=lambda row: row["physical_root_component_id"]):
        cid = component["physical_root_component_id"]
        ports = ports_by_component[cid]
        source_ids = sorted(p["registered_port_id"] for p in ports if p["port_scope"] == "SOURCE_CORE_BOUNDARY")
        ns = sorted(p["registered_port_id"] for p in ports if p["port_scope"] == "NON_SOURCE_REGISTERED_UNION_BOUNDARY")
        physical_ids = sorted(pid for pid in ns if event_by_port[pid]["local_event_classification"] == "PHYSICAL_NEXT_TANGENCY__LOCAL_CONTINUATION" and event_by_port[pid]["port_is_locally_physical_third_tangency"] is True)
        nonphysical_ids = sorted(pid for pid in ns if pid not in set(physical_ids))
        arcs = component["registered_elementary_arc_census_count"]
        if len(ports) != 2 * arcs:
            raise RuntimeError("Euler identity failure")
        kind = "MIXED_NON_SOURCE_PORT_PHYSICALITY" if physical_ids and nonphysical_ids else "PHYSICAL_OPEN_COMPONENT" if physical_ids else "NONPHYSICAL_OPEN_COMPONENT" if nonphysical_ids else "SOURCE_BOUNDARY_ONLY_COMPONENT"
        row = {
            "physical_root_component_id": cid,
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
        for field, value in (("components", 1), ("arcs", arcs), ("source_ports", len(source_ids)), ("physical_ports", len(physical_ids)), ("nonphysical_ports", len(nonphysical_ids))):
            totals[(kind, field)] += value
        if kind == "PHYSICAL_OPEN_COMPONENT" and arcs == 1:
            pairs.append({
                "physical_root_component_id": cid,
                "registered_elementary_arc_endpoint_port_ids": sorted(source_ids + physical_ids),
                "pair_type": "PHYSICAL_PORT_TO_PHYSICAL_PORT" if len(physical_ids) == 2 else "SOURCE_BOUNDARY_TO_PHYSICAL_PORT",
            })
    kinds = ["SOURCE_BOUNDARY_ONLY_COMPONENT", "PHYSICAL_OPEN_COMPONENT", "NONPHYSICAL_OPEN_COMPONENT", "MIXED_NON_SOURCE_PORT_PHYSICALITY"]
    partition = {kind: {field: totals[(kind, field)] for field in ("components", "arcs", "source_ports", "physical_ports", "nonphysical_ports")} for kind in kinds}
    return rows, pairs, partition


def verify_document(doc: dict[str, Any]) -> None:
    if set(doc) != {"schema", "result", "result_sha256"} or doc["schema"] != "cm2.round88.rank3-physical-port-component-quotient.v1":
        raise RuntimeError("manifest closed schema failure")
    if digest(doc["result"]) != doc["result_sha256"]:
        raise RuntimeError("manifest digest failure")
    result = doc["result"]
    rows, pairs, partition = independent_rows()
    if result["component_quotient_rows"] != rows or result["component_quotient_rows_sha256"] != digest(rows):
        raise RuntimeError("independent component row mismatch")
    if result["exact_single_arc_registered_side_pair_rows"] != pairs or result["exact_single_arc_registered_side_pair_rows_sha256"] != digest(pairs):
        raise RuntimeError("independent exact pair row mismatch")
    if result["component_frontier_partition"] != partition:
        raise RuntimeError("partition mismatch")
    if (len(rows), sum(x["registered_elementary_arc_count"] for x in rows)) != (1672, 2108):
        raise RuntimeError("input census mismatch")
    if len(pairs) != 320 or Counter(x["pair_type"] for x in pairs) != {"PHYSICAL_PORT_TO_PHYSICAL_PORT": 285, "SOURCE_BOUNDARY_TO_PHYSICAL_PORT": 35}:
        raise RuntimeError("pair frontier mismatch")
    if result["mixed_non_source_port_physicality_component_count"] != 0:
        raise RuntimeError("mixed component exists")
    expected_scalars = {
        "input_registered_box_component_count": 1672,
        "input_registered_elementary_arc_count": 2108,
        "input_registered_port_count": 4216,
        "live_global_physical_continuation_component_count": 352,
        "live_global_physical_continuation_registered_arc_count": 496,
        "live_global_physical_continuation_non_source_port_count": 945,
        "exact_single_arc_registered_side_pair_count": 320,
        "multi_arc_live_component_count": 32,
        "multi_arc_live_registered_arc_count": 176,
        "multi_arc_live_physical_port_count": 340,
        "multi_arc_live_source_port_count": 12,
    }
    for key, value in expected_scalars.items():
        if result[key] != value:
            raise RuntimeError(f"scalar mismatch: {key}")


def mutated_rejection_count(doc: dict[str, Any]) -> int:
    mutations = []
    for key, value in (
        ("live_global_physical_continuation_component_count", 351),
        ("live_global_physical_continuation_registered_arc_count", 495),
        ("live_global_physical_continuation_non_source_port_count", 944),
        ("exact_single_arc_registered_side_pair_count", 319),
        ("multi_arc_live_component_count", 31),
        ("mixed_non_source_port_physicality_component_count", 1),
    ):
        bad = copy.deepcopy(doc); bad["result"][key] = value; bad["result_sha256"] = digest(bad["result"]); mutations.append(bad)
    rejected = 0
    for bad in mutations:
        try: verify_document(bad)
        except Exception: rejected += 1
    return rejected


def strict_json_rejection_count(doc: dict[str, Any]) -> int:
    rejected = 0
    attacks = [
        '{"schema":"x","schema":"y","result":{},"result_sha256":"z"}',
        '{"schema":"x","result":{"bad":NaN},"result_sha256":"z"}',
    ]
    for raw in attacks:
        try:
            json.loads(raw, object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
        except Exception:
            rejected += 1
    extra = copy.deepcopy(doc); extra["unexpected"] = True
    missing = copy.deepcopy(doc); del missing["schema"]
    for bad in (extra, missing):
        try:
            verify_document(bad)
        except Exception:
            rejected += 1
    return rejected


def main() -> int:
    for name, expected in FILE_PINS.items():
        if file_sha256(HERE / name) != expected:
            raise RuntimeError(f"file pin mismatch: {name}")
    doc = parse(MANIFEST, "cm2.round88.rank3-physical-port-component-quotient.v1")
    verify_document(doc)
    semantic_rejections = mutated_rejection_count(doc)
    if semantic_rejections != 6:
        raise RuntimeError("hostile semantic mutation survived")
    strict_rejections = strict_json_rejection_count(doc)
    if strict_rejections != 4:
        raise RuntimeError("strict JSON attack survived")
    audit_result = {
        "status": "PASS",
        "closed_schema_and_canonical_digest_verified": True,
        "independent_full_component_port_incidence_recomputation": True,
        "independent_round87_physicality_crosswalk_recomputation": True,
        "verified_component_count": 1672,
        "verified_registered_arc_count": 2108,
        "verified_live_component_count": 352,
        "verified_live_arc_count": 496,
        "verified_live_physical_port_count": 945,
        "verified_exact_single_arc_pair_count": 320,
        "verified_remaining_multi_arc_live_component_count": 32,
        "hostile_semantic_mutations_rejected": f"{semantic_rejections}/6",
        "strict_json_attacks_rejected": f"{strict_rejections}/4",
        "file_pins_verified": f"{len(FILE_PINS)}/{len(FILE_PINS)}",
        "strict_nonclaim": "NO_OUTWARD_BRANCH_PAIRING_OR_COMPLETE_PHYSICAL_FACE_COUNT_VERIFIED",
    }
    print(json.dumps({"schema": "cm2.round88.rank3-physical-port-component-quotient-audit.v1", "result": audit_result, "result_sha256": digest(audit_result)}, sort_keys=True, separators=(",", ":"), ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
