#!/usr/bin/env python3
"""768-bit independent verifier for the Round-88 multi-arc resolver."""
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round80_time3_adaptive_carrier_resolver import centered_taylor, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round88-rank3-multi-arc-zero-overlap-resolver-2026-07-22.json"
MANIFEST_SHA = "370a9861749d628dd8993d03236155e41c003863fd08ca18ad222bfa661eb48e"
PRODUCER_SHA = "2ac79034736d3c89abd5cbd8ee8d7a8e770cba8c45614062ee2e4980b18e9485"
PRODUCER = HERE / "cm2_round88_rank3_multi_arc_zero_overlap_resolver_cert.py"
QUOTIENT = HERE / "cm2-round88-rank3-physical-port-component-quotient-2026-07-22.json"
CENSUS = HERE / "cm2-round85-rank3-registered-arc-port-census-2026-07-22.json"
ATLAS = HERE / "cm2-round82-rank3-physical-patch-atlas-2026-07-21.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
EXPECTED_UPSTREAM_PINS = {
    QUOTIENT.name: "35e4b0ee448476837644f66a55aaaf385bcb4027c27a36fdc37f54bfb4f40d42",
    CENSUS.name: "11feee98133d133ecc20654389dd559fa1fbd06f9210ef10d52ec6d86f479f2d",
    ATLAS.name: "013d5469c7a5caf47f450437a6b5f3639f040b3b9eca950a480b58e9b6eda018",
    JOINS.name: "f211d6f17d764d2913937c34c3cdcdbc80c330b420a6011e22f993dc85663561",
    "cm2_round88_rank3_physical_port_component_quotient_cert.py": "dbeb5ebf5a48e6a14c1e8b6baabe6b15bd1949c1f2637607c269b3d255e72107",
    "cm2_round80_time3_tangency_curve_generator.py": "68d17d088e94a8d5b0b97a6518691e19da2560be7df7fcff32eacdfd367aa659",
    "cm2_round80_time3_adaptive_carrier_resolver.py": "e53a4f53e1d2516c70f85f7078f9e4bc116d2d9c03688a4faa1395e3bf78a8c0",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out = {}
    for key, value in items:
        if key in out:
            raise ValueError(key)
        out[key] = value
    return out


def parse(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(), object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def rect_intersection(left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]) -> tuple[Q, Q, Q, Q] | None:
    box = max(left[0], right[0]), min(left[1], right[1]), max(left[2], right[2]), min(left[3], right[3])
    return None if box[0] > box[1] or box[2] > box[3] else box


def contains_zero(source: Any, second: str, candidate: str, box: tuple[Q, Q, Q, Q]) -> tuple[bool, tuple[int, int]]:
    _value, gradient = centered_taylor(source, second, candidate, box)
    gradient_signs = strict_sign(gradient[0]), strict_sign(gradient[1])
    if 0 in gradient_signs:
        raise RuntimeError("indeterminate overlap gradient")
    signs = []
    for t in sorted(set(box[:2])):
        for p in sorted(set(box[2:])):
            sign = strict_sign(third_tangency_jet(source, second, candidate, t, t, p, p).value)
            if sign == 0:
                raise RuntimeError("indeterminate overlap corner")
            signs.append(sign)
    return min(signs) < 0 < max(signs), gradient_signs


def port_box_incidence(port: dict[str, Any], box: tuple[Q, Q, Q, Q]) -> bool:
    fixed = Q(port["fixed_coordinate"]); lower, upper = map(Q, port["root_bracket"])
    if port["boundary_axis"] == "p":
        return fixed in (box[0], box[1]) and max(lower, box[2]) < min(upper, box[3])
    return fixed in (box[2], box[3]) and max(lower, box[0]) < min(upper, box[1])


def independent_recompute(bits: int = 768) -> dict[str, Any]:
    ctx.prec = bits
    qdoc, cdoc, adoc, jdoc = map(parse, (QUOTIENT, CENSUS, ATLAS, JOINS))
    expected_schemas = (
        "cm2.round88.rank3-physical-port-component-quotient.v1",
        "cm2.round85.rank3-registered-arc-port-census.v1",
        "cm2.round82.rank3-physical-patch-atlas.v1",
        "cm2.round82.rank3-cross-tube-joins.v1",
    )
    for document, schema in zip((qdoc, cdoc, adoc, jdoc), expected_schemas):
        if set(document) != {"schema", "result", "result_sha256"} or document["schema"] != schema or document["result_sha256"] != digest(document["result"]):
            raise RuntimeError("upstream closed schema or digest")
    quotient, census, atlas, joins = qdoc["result"], cdoc["result"], adoc["result"], jdoc["result"]
    patches = {row["physical_patch_id"]: row for row in atlas["physical_patch_rows"]}
    join_map = {row["physical_root_component_id"]: row for row in joins["component_rows"]}
    ports: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for port in census["port_rows"]:
        ports[port["physical_root_component_id"]].append(port)
    live = [row for row in quotient["component_quotient_rows"] if row["component_frontier_class"] == "PHYSICAL_OPEN_COMPONENT" and row["registered_elementary_arc_count"] > 1]
    cores = core_cert.physical_cores()
    resolved, component_rows = [], []
    total_boxes = tested_total = connected_total = excluded_total = 0
    for qrow in live:
        cid = qrow["physical_root_component_id"]; joined = join_map[cid]
        source = cores[joined["source_core_index"]]; second = joined["second_selected_target_id"]; candidate = joined["third_candidate_id"]
        boxes = sorted(set(tuple(map(Q, raw)) for patch_id in joined["physical_patch_ids"] for raw in patches[patch_id]["boxes"]))
        total_boxes += len(boxes); parent = list(range(len(boxes)))
        def find(i: int) -> int:
            while parent[i] != i:
                parent[i] = parent[parent[i]]; i = parent[i]
            return i
        def union(i: int, j: int) -> None:
            i, j = find(i), find(j)
            if i != j: parent[j] = i
        tested = connected = excluded = 0; sign_hist: Counter[str] = Counter()
        for right in range(len(boxes)):
            for left in range(right):
                shared = rect_intersection(boxes[left], boxes[right])
                if shared is None: continue
                tested += 1; has_zero, signs = contains_zero(source, second, candidate, shared); sign_hist[f"{signs[0]},{signs[1]}"] += 1
                if has_zero: connected += 1; union(left, right)
                else: excluded += 1
        groups: dict[int, list[int]] = defaultdict(list)
        for i in range(len(boxes)): groups[find(i)].append(i)
        piece_ports: dict[int, list[str]] = defaultdict(list)
        for port in ports[cid]:
            hits = {find(i) for i, box in enumerate(boxes) if port_box_incidence(port, box)}
            if len(hits) != 1: raise RuntimeError("ambiguous incidence")
            piece_ports[next(iter(hits))].append(port["registered_port_id"])
        if len(groups) != qrow["registered_elementary_arc_count"] or any(len(piece_ports[root]) != 2 for root in groups): raise RuntimeError("piece census")
        pieces = []; source_ids = set(qrow["source_boundary_port_ids"]); physical_ids = set(qrow["locally_physical_non_source_port_ids"])
        for root in sorted(groups, key=lambda key: [boxes[i] for i in groups[key]]):
            member_boxes = [[str(v) for v in boxes[i]] for i in sorted(groups[root])]; endpoints = sorted(piece_ports[root]); nphysical = len(set(endpoints) & physical_ids)
            kind = "PHYSICAL_PORT_TO_PHYSICAL_PORT" if nphysical == 2 else "SOURCE_BOUNDARY_TO_PHYSICAL_PORT" if nphysical == 1 else "SOURCE_BOUNDARY_TO_SOURCE_BOUNDARY"
            row = {"zero_overlap_piece_id": "physical-s0-rank3-zero-overlap-piece:" + digest([cid, member_boxes]), "physical_root_component_id": cid, "registered_box_count": len(member_boxes), "registered_boxes_sha256": digest(member_boxes), "registered_elementary_arc_endpoint_port_ids": endpoints, "pair_type": kind}
            pieces.append(row); resolved.append(row)
        component_rows.append({"physical_root_component_id": cid, "input_registered_box_count": len(boxes), "overlapping_box_pair_test_count": tested, "zero_connecting_overlap_count": connected, "strict_zero_excluding_overlap_count": excluded, "overlap_gradient_sign_histogram": dict(sorted(sign_hist.items())), "expected_elementary_arc_count": qrow["registered_elementary_arc_count"], "resolved_zero_overlap_piece_count": len(pieces), "all_piece_port_degrees_equal_two": True, "ambiguous_port_incidence_count": 0, "piece_rows": pieces, "piece_rows_sha256": digest(pieces)})
        tested_total += tested; connected_total += connected; excluded_total += excluded
    component_rows.sort(key=lambda row: row["physical_root_component_id"]); resolved.sort(key=lambda row: row["zero_overlap_piece_id"])
    return {"components": component_rows, "resolved": resolved, "boxes": total_boxes, "tested": tested_total, "connected": connected_total, "excluded": excluded_total}


def verify(doc: dict[str, Any], independent: dict[str, Any]) -> None:
    if set(doc) != {"schema", "result", "result_sha256"} or doc["schema"] != "cm2.round88.rank3-multi-arc-zero-overlap-resolver.v1" or doc["result_sha256"] != digest(doc["result"]): raise RuntimeError("closed manifest")
    result = doc["result"]
    if result["upstream_and_executable_pins"] != EXPECTED_UPSTREAM_PINS: raise RuntimeError("embedded pin ledger")
    if result["multi_arc_component_resolution_rows"] != independent["components"] or result["multi_arc_resolved_pair_rows"] != independent["resolved"]: raise RuntimeError("independent rows")
    for key, source in (("input_live_multi_arc_registered_box_count", "boxes"), ("overlapping_box_pair_test_count", "tested"), ("zero_connecting_overlap_count", "connected"), ("strict_zero_excluding_overlap_count", "excluded")):
        if result[key] != independent[source]: raise RuntimeError(key)
    if (len(independent["components"]), len(independent["resolved"]), result["complete_live_registered_side_pair_count"], result["complete_live_registered_side_distinct_endpoint_count"]) != (32, 176, 496, 992): raise RuntimeError("final census")
    if result["resolved_zero_overlap_elementary_piece_count"] != 176 or result["ambiguous_port_to_piece_incidence_count"] != 0 or result["registered_side_pairing_complete_for_all_496_live_arcs"] is not True: raise RuntimeError("resolution verdict")
    if result["complete_live_registered_side_pair_type_histogram"] != {"PHYSICAL_PORT_TO_PHYSICAL_PORT": 449, "SOURCE_BOUNDARY_TO_PHYSICAL_PORT": 47}: raise RuntimeError("pair histogram")


def main() -> int:
    if sha(MANIFEST) != MANIFEST_SHA or sha(PRODUCER) != PRODUCER_SHA: raise RuntimeError("direct pin")
    for name, expected in EXPECTED_UPSTREAM_PINS.items():
        if sha(HERE / name) != expected: raise RuntimeError(f"upstream pin: {name}")
    doc = parse(MANIFEST); independent = independent_recompute(); verify(doc, independent)
    rejected = 0
    for key, value in (("resolved_zero_overlap_elementary_piece_count", 175), ("ambiguous_port_to_piece_incidence_count", 1), ("complete_live_registered_side_pair_count", 495), ("complete_live_registered_side_distinct_endpoint_count", 991), ("registered_side_pairing_complete_for_all_496_live_arcs", False), ("zero_connecting_overlap_count", -1)):
        bad = copy.deepcopy(doc); bad["result"][key] = value; bad["result_sha256"] = digest(bad["result"])
        try: verify(bad, independent)
        except Exception: rejected += 1
    strict = 0
    for raw in ('{"x":1,"x":2}', '{"x":NaN}'):
        try: json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        except Exception: strict += 1
    for bad in ({**doc, "extra": 1}, {key: value for key, value in doc.items() if key != "schema"}):
        try: verify(bad, independent)
        except Exception: strict += 1
    if rejected != 6 or strict != 4: raise RuntimeError("mutation audit")
    audit = {"status": "PASS", "independent_precision_bits": 768, "independent_zero_overlap_pair_tests": independent["tested"], "independent_resolved_piece_count": len(independent["resolved"]), "verified_complete_live_registered_side_pair_count": 496, "verified_distinct_registered_side_endpoint_count": 992, "ambiguous_incidence_count": 0, "hostile_semantic_mutations_rejected": "6/6", "strict_json_attacks_rejected": "4/4", "file_pins_verified": "10/10", "strict_nonclaim": "NO_OUTWARD_GLOBAL_BRANCH_PAIRING_OR_COMPLETE_PHYSICAL_FACE_COUNT"}
    print(json.dumps({"schema": "cm2.round88.rank3-multi-arc-zero-overlap-resolver-audit.v1", "result": audit, "result_sha256": digest(audit)}, sort_keys=True, separators=(",", ":"), ensure_ascii=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
