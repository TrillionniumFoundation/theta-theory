#!/usr/bin/env python3
"""Resolve every live Round-88 multi-arc registered component exactly.

Two registered boxes are adjacent in the zero set iff their exact rectangular
intersection contains a zero of the pinned third-tangency discriminant.  Both
coordinate derivatives are certified nonzero on every tested intersection;
strict corner signs therefore decide existence without topology-by-box-touch.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round80_time3_adaptive_carrier_resolver import strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet

HERE = Path(__file__).resolve().parent
QUOTIENT = HERE / "cm2-round88-rank3-physical-port-component-quotient-2026-07-22.json"
CENSUS = HERE / "cm2-round85-rank3-registered-arc-port-census-2026-07-22.json"
ATLAS = HERE / "cm2-round82-rank3-physical-patch-atlas-2026-07-21.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
PINS = {
    QUOTIENT.name: "35e4b0ee448476837644f66a55aaaf385bcb4027c27a36fdc37f54bfb4f40d42",
    CENSUS.name: "11feee98133d133ecc20654389dd559fa1fbd06f9210ef10d52ec6d86f479f2d",
    ATLAS.name: "013d5469c7a5caf47f450437a6b5f3639f040b3b9eca950a480b58e9b6eda018",
    JOINS.name: "f211d6f17d764d2913937c34c3cdcdbc80c330b420a6011e22f993dc85663561",
    "cm2_round88_rank3_physical_port_component_quotient_cert.py": "dbeb5ebf5a48e6a14c1e8b6baabe6b15bd1949c1f2637607c269b3d255e72107",
    "cm2_round80_time3_tangency_curve_generator.py": "68d17d088e94a8d5b0b97a6518691e19da2560be7df7fcff32eacdfd367aa659",
    "cm2_round80_time3_adaptive_carrier_resolver.py": "e53a4f53e1d2516c70f85f7078f9e4bc116d2d9c03688a4faa1395e3bf78a8c0",
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
}
PRECISION_BITS = 512


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load(path: Path, schema: str) -> dict[str, Any]:
    doc = json.loads(path.read_text(), object_pairs_hook=strict_pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    if set(doc) != {"schema", "result", "result_sha256"} or doc["schema"] != schema or doc["result_sha256"] != digest(doc["result"]):
        raise RuntimeError(f"invalid closed upstream: {path.name}")
    return doc["result"]


def overlap(a: tuple[Q, Q, Q, Q], b: tuple[Q, Q, Q, Q]) -> tuple[Q, Q, Q, Q] | None:
    result = max(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), min(a[3], b[3])
    return None if result[0] > result[1] or result[2] > result[3] else result


def zero_on_overlap(source: Any, second: str, candidate: str, box: tuple[Q, Q, Q, Q]) -> tuple[bool, tuple[int, int]]:
    jet = third_tangency_jet(source, second, candidate, *box)
    gradient_signs = strict_sign(jet.gradient[0]), strict_sign(jet.gradient[1])
    if 0 in gradient_signs:
        raise RuntimeError("critical or indeterminate overlap")
    corner_signs = []
    for t in sorted(set(box[:2])):
        for p in sorted(set(box[2:])):
            sign = strict_sign(third_tangency_jet(source, second, candidate, t, t, p, p).value)
            if sign == 0:
                raise RuntimeError("corner equality or indeterminacy")
            corner_signs.append(sign)
    return min(corner_signs) < 0 < max(corner_signs), gradient_signs


def port_hits_box(port: dict[str, Any], box: tuple[Q, Q, Q, Q]) -> bool:
    fixed = Q(port["fixed_coordinate"])
    lower, upper = map(Q, port["root_bracket"])
    if port["boundary_axis"] == "p":
        return fixed in box[:2] and max(lower, box[2]) < min(upper, box[3])
    return fixed in box[2:] and max(lower, box[0]) < min(upper, box[1])


def build(bits: int = PRECISION_BITS) -> dict[str, Any]:
    ctx.prec = bits
    for name, expected in PINS.items():
        if file_sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    quotient = load(QUOTIENT, "cm2.round88.rank3-physical-port-component-quotient.v1")
    census = load(CENSUS, "cm2.round85.rank3-registered-arc-port-census.v1")
    atlas = load(ATLAS, "cm2.round82.rank3-physical-patch-atlas.v1")
    joins = load(JOINS, "cm2.round82.rank3-cross-tube-joins.v1")
    patches = {row["physical_patch_id"]: row for row in atlas["physical_patch_rows"]}
    join_map = {row["physical_root_component_id"]: row for row in joins["component_rows"]}
    ports_by_component: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for port in census["port_rows"]:
        ports_by_component[port["physical_root_component_id"]].append(port)
    live_multi = [row for row in quotient["component_quotient_rows"] if row["component_frontier_class"] == "PHYSICAL_OPEN_COMPONENT" and row["registered_elementary_arc_count"] > 1]
    cores = core_cert.physical_cores()
    component_rows, resolved_pair_rows = [], []
    overlap_hist: Counter[str] = Counter()
    total_boxes = 0
    for qrow in live_multi:
        cid = qrow["physical_root_component_id"]
        joined = join_map[cid]
        source = cores[joined["source_core_index"]]
        second, candidate = joined["second_selected_target_id"], joined["third_candidate_id"]
        boxes = sorted(set(tuple(map(Q, raw)) for patch_id in joined["physical_patch_ids"] for raw in patches[patch_id]["boxes"]))
        total_boxes += len(boxes)
        parent = list(range(len(boxes)))
        def find(index: int) -> int:
            while parent[index] != index:
                parent[index] = parent[parent[index]]
                index = parent[index]
            return index
        def union(left: int, right: int) -> None:
            left, right = find(left), find(right)
            if left != right:
                parent[right] = left
        tested = connected = excluded = 0
        sign_hist: Counter[str] = Counter()
        for right in range(len(boxes)):
            for left in range(right):
                shared = overlap(boxes[left], boxes[right])
                if shared is None:
                    continue
                tested += 1
                has_zero, signs = zero_on_overlap(source, second, candidate, shared)
                sign_hist[f"{signs[0]},{signs[1]}"] += 1
                if has_zero:
                    connected += 1
                    union(left, right)
                else:
                    excluded += 1
        groups: dict[int, list[int]] = defaultdict(list)
        for index in range(len(boxes)):
            groups[find(index)].append(index)
        piece_ports: dict[int, list[str]] = defaultdict(list)
        for port in ports_by_component[cid]:
            hits = {find(index) for index, box in enumerate(boxes) if port_hits_box(port, box)}
            if len(hits) != 1:
                raise RuntimeError("ambiguous or missing port-to-zero-piece incidence")
            piece_ports[next(iter(hits))].append(port["registered_port_id"])
        if len(groups) != qrow["registered_elementary_arc_count"] or set(groups) != set(piece_ports) or any(len(ids) != 2 for ids in piece_ports.values()):
            raise RuntimeError("multi-arc zero-overlap resolution failed")
        piece_rows = []
        source_ids = set(qrow["source_boundary_port_ids"])
        physical_ids = set(qrow["locally_physical_non_source_port_ids"])
        for root in sorted(groups, key=lambda key: [boxes[i] for i in groups[key]]):
            member_boxes = [[str(value) for value in boxes[index]] for index in sorted(groups[root])]
            endpoints = sorted(piece_ports[root])
            if not set(endpoints) <= source_ids | physical_ids:
                raise RuntimeError("piece endpoint leaves live physical component ledger")
            physical_count = len(set(endpoints) & physical_ids)
            pair_type = "PHYSICAL_PORT_TO_PHYSICAL_PORT" if physical_count == 2 else "SOURCE_BOUNDARY_TO_PHYSICAL_PORT" if physical_count == 1 else "SOURCE_BOUNDARY_TO_SOURCE_BOUNDARY"
            piece_id = "physical-s0-rank3-zero-overlap-piece:" + digest([cid, member_boxes])
            piece = {
                "zero_overlap_piece_id": piece_id,
                "physical_root_component_id": cid,
                "registered_box_count": len(member_boxes),
                "registered_boxes_sha256": digest(member_boxes),
                "registered_elementary_arc_endpoint_port_ids": endpoints,
                "pair_type": pair_type,
            }
            piece_rows.append(piece)
            resolved_pair_rows.append(piece)
        component_rows.append({
            "physical_root_component_id": cid,
            "input_registered_box_count": len(boxes),
            "overlapping_box_pair_test_count": tested,
            "zero_connecting_overlap_count": connected,
            "strict_zero_excluding_overlap_count": excluded,
            "overlap_gradient_sign_histogram": dict(sorted(sign_hist.items())),
            "expected_elementary_arc_count": qrow["registered_elementary_arc_count"],
            "resolved_zero_overlap_piece_count": len(piece_rows),
            "all_piece_port_degrees_equal_two": True,
            "ambiguous_port_incidence_count": 0,
            "piece_rows": piece_rows,
            "piece_rows_sha256": digest(piece_rows),
        })
        overlap_hist["tested"] += tested
        overlap_hist["connected"] += connected
        overlap_hist["excluded"] += excluded
    component_rows.sort(key=lambda row: row["physical_root_component_id"])
    resolved_pair_rows.sort(key=lambda row: row["zero_overlap_piece_id"])
    prior_pairs = quotient["exact_single_arc_registered_side_pair_rows"]
    all_pairs = sorted([
        {"physical_root_component_id": row["physical_root_component_id"], "registered_elementary_arc_endpoint_port_ids": row["registered_elementary_arc_endpoint_port_ids"], "pair_type": row["pair_type"], "resolution_source": "ROUND88_SINGLE_ARC_COMPONENT_IDENTITY"}
        for row in prior_pairs
    ] + [
        {"physical_root_component_id": row["physical_root_component_id"], "registered_elementary_arc_endpoint_port_ids": row["registered_elementary_arc_endpoint_port_ids"], "pair_type": row["pair_type"], "resolution_source": "ROUND88_STRICT_ZERO_OVERLAP_GRAPH"}
        for row in resolved_pair_rows
    ], key=lambda row: (row["physical_root_component_id"], row["registered_elementary_arc_endpoint_port_ids"]))
    pair_hist = dict(sorted(Counter(row["pair_type"] for row in all_pairs).items()))
    endpoint_ids = [pid for row in all_pairs for pid in row["registered_elementary_arc_endpoint_port_ids"]]
    if len(component_rows) != 32 or len(resolved_pair_rows) != 176 or len(all_pairs) != 496 or len(endpoint_ids) != len(set(endpoint_ids)) != 992:
        raise RuntimeError("final live pairing census mismatch")
    result = {
        "precision_bits": bits,
        "upstream_and_executable_pins": PINS,
        "input_live_multi_arc_component_count": 32,
        "input_live_multi_arc_registered_box_count": total_boxes,
        "input_live_multi_arc_expected_elementary_arc_count": 176,
        "overlapping_box_pair_test_count": overlap_hist["tested"],
        "zero_connecting_overlap_count": overlap_hist["connected"],
        "strict_zero_excluding_overlap_count": overlap_hist["excluded"],
        "resolved_zero_overlap_elementary_piece_count": len(resolved_pair_rows),
        "resolved_piece_port_degree_histogram": {"2": len(resolved_pair_rows)},
        "ambiguous_port_to_piece_incidence_count": 0,
        "multi_arc_component_resolution_rows": component_rows,
        "multi_arc_component_resolution_rows_sha256": digest(component_rows),
        "multi_arc_resolved_pair_rows": resolved_pair_rows,
        "multi_arc_resolved_pair_rows_sha256": digest(resolved_pair_rows),
        "complete_live_registered_side_pair_count": len(all_pairs),
        "complete_live_registered_side_pair_type_histogram": pair_hist,
        "complete_live_registered_side_distinct_endpoint_count": len(set(endpoint_ids)),
        "complete_live_registered_side_pair_rows": all_pairs,
        "complete_live_registered_side_pair_rows_sha256": digest(all_pairs),
        "registered_side_pairing_complete_for_all_496_live_arcs": True,
        "strict_scope": "ZERO_SET_INCIDENCE_AND_ENDPOINT_PAIRING_INSIDE_PINNED_REGISTERED_BOX_UNIONS_ONLY",
        "strict_nonclaims": [
            "NO_PAIRING_OF_THE_945_PHYSICAL_PORTS_OUTSIDE_REGISTERED_UNIONS_IS_ASSERTED",
            "NO_SOURCE_BOUNDARY_PORT_IS_RELABELLED_AS_A_PHYSICAL_ENDPOINT",
            "NO_COMPLETE_PHYSICAL_FACE_COUNT_IS_ASSERTED",
            "NO_GATE5_OR_RN_PROMOTION_IS_ASSERTED",
        ],
    }
    return {"schema": "cm2.round88.rank3-multi-arc-zero-overlap-resolver.v1", "result": result, "result_sha256": digest(result)}


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, separators=(",", ":"), ensure_ascii=True))
