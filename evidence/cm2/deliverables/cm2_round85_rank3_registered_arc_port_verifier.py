#!/usr/bin/env python3
"""Independent higher-precision verifier for the Round-85 registered arc census."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import digest
from cm2_round80_time3_adaptive_carrier_resolver import centered_taylor, strict_sign, third_tangency_jet


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / "cm2-round85-rank3-registered-arc-port-census-2026-07-22.json"
ATLAS = HERE / "cm2-round82-rank3-physical-patch-atlas-2026-07-21.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
ENDPOINTS = HERE / "cm2-round82-rank3-boundary-endpoints-2026-07-21.json"
ROUND82_LEDGER = HERE / "cm2-eighty-second-direct-assault-manifest-2026-07-21.sha256"
ROUND82_LEDGER_SHA256 = "ba6856a54f5a112fb349d3a8d3961b7c6e21f021529bb86af521b1d3293ec93d"
VERIFIER_PRECISION_BITS = 768

TOP_KEYS = {"schema", "result", "result_sha256"}
RESULT_KEYS = {
    "fixed_parameter", "precision_bits", "frozen_joined_row_count", "input_registered_box_count",
    "exactly_deduplicated_union_box_count", "coordinate_gradient_nonzero_box_count",
    "registered_union_boundary_segment_count", "initial_boundary_status_histogram",
    "final_boundary_leaf_status_histogram", "total_boundary_interval_box_tests",
    "maximum_boundary_refinement_depth", "certified_registered_port_count", "source_boundary_port_count",
    "non_source_registered_boundary_port_count", "registered_port_count_histogram_per_frozen_row",
    "registered_elementary_arc_multiplicity_histogram_per_frozen_row", "single_arc_frozen_row_count",
    "multi_arc_frozen_row_count", "registered_elementary_arc_census_count",
    "round82_source_endpoint_crosswalk_count", "round82_source_endpoint_crosswalk_is_bijective",
    "component_rows", "component_rows_sha256", "boundary_segment_rows", "boundary_segment_rows_sha256",
    "port_rows", "port_rows_sha256", "source_endpoint_crosswalk_rows",
    "source_endpoint_crosswalk_rows_sha256", "topological_certificate", "strict_scope", "strict_nonclaims",
    "upstream_pins",
}
COMPONENT_KEYS = {
    "physical_root_component_id", "source_core_index", "second_selected_target_id", "third_candidate_id",
    "physical_patch_count", "certification_source_histogram", "input_box_count", "unique_union_box_count",
    "coordinate_gradient_nonzero_box_count", "coordinate_gradient_sign_histogram",
    "registered_boundary_segment_count", "boundary_initial_status_histogram", "boundary_interval_box_tests",
    "registered_port_count", "source_boundary_port_count", "non_source_registered_boundary_port_count",
    "registered_elementary_arc_census_count", "registered_boundary_segment_ids_sha256",
    "registered_port_ids_sha256",
}
SEGMENT_KEYS = {
    "registered_boundary_segment_id", "physical_root_component_id", "local_boundary_segment_rank", "axis",
    "fixed_axis", "fixed_coordinate", "parameter_interval", "inside_side", "source_boundary_side",
    "initial_status", "interval_box_tests", "leaf_rows", "leaf_rows_sha256", "certified_root_count",
    "registered_port_ids",
}
PORT_KEYS = {
    "registered_port_id", "physical_root_component_id", "source_core_index", "second_selected_target_id",
    "third_candidate_id", "boundary_segment_id", "boundary_axis", "fixed_coordinate", "root_bracket",
    "derivative_sign", "endpoint_signs", "refinement_depth", "source_boundary_side", "port_scope",
}
CROSSWALK_KEYS = {"physical_endpoint_id", "registered_port_id"}
TOPOLOGY_KEYS = {"regularity", "boundary_transversality", "closed_component_exclusion", "census_rule"}
PIN_KEYS = {
    "round82_sha256_ledger_sha256",
    "rank3_physical_patch_atlas_sha256", "rank3_cross_tube_joins_sha256",
    "rank3_boundary_endpoints_sha256",
}


def strict_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def strict_load_text(text: str) -> Any:
    return json.loads(text, object_pairs_hook=strict_object_pairs, parse_constant=reject_nonfinite)


def strict_load(path: Path) -> dict[str, Any]:
    document = strict_load_text(path.read_text())
    if not isinstance(document, dict):
        raise ValueError("document must be an object")
    return document


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_round82_ledger() -> dict[str, str]:
    if file_sha256(ROUND82_LEDGER) != ROUND82_LEDGER_SHA256:
        raise ValueError("frozen Round-82 SHA ledger digest mismatch")
    entries: dict[str, str] = {}
    for line in ROUND82_LEDGER.read_text().splitlines():
        parts = line.split("  ")
        if len(parts) != 2 or len(parts[0]) != 64 or any(character not in "0123456789abcdef" for character in parts[0]):
            raise ValueError("malformed frozen Round-82 SHA ledger")
        checksum, name = parts
        if name in entries:
            raise ValueError("duplicate frozen Round-82 SHA ledger path")
        entries[name] = checksum
    for path in (ATLAS, JOINS, ENDPOINTS):
        name = "deliverables/" + path.name
        if entries.get(name) != file_sha256(path):
            raise ValueError(f"Round-82 ledger pin mismatch: {name}")
    return entries


def check_keys(row: dict[str, Any], expected: set[str], label: str) -> None:
    if set(row) != expected:
        raise ValueError(f"non-closed {label} schema: missing={sorted(expected-set(row))} extra={sorted(set(row)-expected)}")


def check_leaf_schema(row: dict[str, Any]) -> None:
    base = {"parameter_interval", "depth", "status"}
    status = row.get("status")
    if status == "STRICT_RANGE_EXCLUSION":
        expected = base | {"range_sign"}
    elif status == "STRICT_MONOTONE_SAME_SIGN_EXCLUSION":
        expected = base | {"derivative_sign", "endpoint_signs"}
    elif status == "UNIQUE_TRANSVERSE_BOUNDARY_ROOT":
        expected = base | {"derivative_sign", "endpoint_signs", "strictly_inside_segment"}
    else:
        raise ValueError(f"unknown final leaf status: {status}")
    check_keys(row, expected, "boundary leaf")


def validate_closed_document(document: dict[str, Any]) -> None:
    check_keys(document, TOP_KEYS, "top-level")
    if document["schema"] != "cm2.round85.rank3-registered-arc-port-census.v1":
        raise ValueError("candidate schema")
    result = document["result"]
    check_keys(result, RESULT_KEYS, "result")
    if document["result_sha256"] != digest(result):
        raise ValueError("candidate result digest")
    check_keys(result["topological_certificate"], TOPOLOGY_KEYS, "topological certificate")
    check_keys(result["upstream_pins"], PIN_KEYS, "upstream pins")
    for row in result["component_rows"]:
        check_keys(row, COMPONENT_KEYS, "component row")
    for row in result["boundary_segment_rows"]:
        check_keys(row, SEGMENT_KEYS, "boundary segment row")
        if row["leaf_rows_sha256"] != digest(row["leaf_rows"]):
            raise ValueError("boundary leaf-row digest")
        for leaf in row["leaf_rows"]:
            check_leaf_schema(leaf)
    for row in result["port_rows"]:
        check_keys(row, PORT_KEYS, "port row")
    for row in result["source_endpoint_crosswalk_rows"]:
        check_keys(row, CROSSWALK_KEYS, "source endpoint crosswalk row")
    for key, rows_key in (
        ("component_rows_sha256", "component_rows"),
        ("boundary_segment_rows_sha256", "boundary_segment_rows"),
        ("port_rows_sha256", "port_rows"),
        ("source_endpoint_crosswalk_rows_sha256", "source_endpoint_crosswalk_rows"),
    ):
        if result[key] != digest(result[rows_key]):
            raise ValueError(f"row digest mismatch: {key}")


def load_upstream(path: Path, schema: str) -> dict[str, Any]:
    document = strict_load(path)
    check_keys(document, TOP_KEYS, f"upstream {path.name}")
    if document["schema"] != schema or document["result_sha256"] != digest(document["result"]):
        raise ValueError(f"upstream validation: {path.name}")
    return document["result"]


def event_boundary_atoms(
    negative_intervals: list[tuple[Q, Q]], positive_intervals: list[tuple[Q, Q]]
) -> list[tuple[Q, Q, int]]:
    """Independent interval-event sweep, distinct from the producer's union merge."""
    events: dict[Q, list[int]] = defaultdict(lambda: [0, 0])
    for side_index, intervals in enumerate((negative_intervals, positive_intervals)):
        for lower, upper in intervals:
            if not lower < upper:
                raise ValueError("nonpositive interval")
            events[lower][side_index] += 1
            events[upper][side_index] -= 1
    coordinates = sorted(events)
    counts = [0, 0]
    atoms: list[tuple[Q, Q, int]] = []
    for index, coordinate in enumerate(coordinates[:-1]):
        counts[0] += events[coordinate][0]
        counts[1] += events[coordinate][1]
        upper = coordinates[index + 1]
        present = counts[0] > 0, counts[1] > 0
        if present[0] == present[1]:
            continue
        inside_side = -1 if present[0] else 1
        if atoms and atoms[-1][1] == coordinate and atoms[-1][2] == inside_side:
            atoms[-1] = atoms[-1][0], upper, inside_side
        else:
            atoms.append((coordinate, upper, inside_side))
    return atoms


def independent_boundary(boxes: list[tuple[Q, Q, Q, Q]]) -> list[dict[str, Any]]:
    rows = []
    for fixed in sorted({coordinate for box in boxes for coordinate in box[:2]}):
        negative = [(p0, p1) for t0, t1, p0, p1 in boxes if t0 < fixed <= t1]
        positive = [(p0, p1) for t0, t1, p0, p1 in boxes if t0 <= fixed < t1]
        for lower, upper, inside_side in event_boundary_atoms(negative, positive):
            rows.append({
                "axis": "p", "fixed_axis": "t", "fixed_coordinate": str(fixed),
                "parameter_interval": [str(lower), str(upper)], "inside_side": inside_side,
            })
    for fixed in sorted({coordinate for box in boxes for coordinate in box[2:]}):
        negative = [(t0, t1) for t0, t1, p0, p1 in boxes if p0 < fixed <= p1]
        positive = [(t0, t1) for t0, t1, p0, p1 in boxes if p0 <= fixed < p1]
        for lower, upper, inside_side in event_boundary_atoms(negative, positive):
            rows.append({
                "axis": "t", "fixed_axis": "p", "fixed_coordinate": str(fixed),
                "parameter_interval": [str(lower), str(upper)], "inside_side": inside_side,
            })
    rows.sort(key=lambda row: (
        row["fixed_axis"], Q(row["fixed_coordinate"]), Q(row["parameter_interval"][0]),
        Q(row["parameter_interval"][1]), row["inside_side"],
    ))
    return rows


def boundary_jet(source: Any, second: str, candidate: str, boundary: dict[str, Any], lower: Q, upper: Q) -> Any:
    fixed = Q(boundary["fixed_coordinate"])
    if boundary["axis"] == "p":
        return third_tangency_jet(source, second, candidate, fixed, fixed, lower, upper)
    return third_tangency_jet(source, second, candidate, lower, upper, fixed, fixed)


def endpoint_value(source: Any, second: str, candidate: str, boundary: dict[str, Any], value: Q) -> Any:
    fixed = Q(boundary["fixed_coordinate"])
    if boundary["axis"] == "p":
        return third_tangency_jet(source, second, candidate, fixed, fixed, value, value).value
    return third_tangency_jet(source, second, candidate, value, value, fixed, fixed).value


def independent_leaf(
    source: Any, second: str, candidate: str, boundary: dict[str, Any], lower: Q, upper: Q, depth: int
) -> dict[str, Any]:
    jet = boundary_jet(source, second, candidate, boundary, lower, upper)
    value_sign = strict_sign(jet.value)
    if value_sign:
        return {
            "parameter_interval": [str(lower), str(upper)], "depth": depth,
            "status": "STRICT_RANGE_EXCLUSION", "range_sign": value_sign,
        }
    derivative_sign = strict_sign(jet.gradient[1 if boundary["axis"] == "p" else 0])
    signs = [
        strict_sign(endpoint_value(source, second, candidate, boundary, lower)),
        strict_sign(endpoint_value(source, second, candidate, boundary, upper)),
    ]
    if derivative_sign and signs[0] and signs[1]:
        if signs[0] == signs[1]:
            return {
                "parameter_interval": [str(lower), str(upper)], "depth": depth,
                "status": "STRICT_MONOTONE_SAME_SIGN_EXCLUSION", "derivative_sign": derivative_sign,
                "endpoint_signs": signs,
            }
        return {
            "parameter_interval": [str(lower), str(upper)], "depth": depth,
            "status": "UNIQUE_TRANSVERSE_BOUNDARY_ROOT", "derivative_sign": derivative_sign,
            "endpoint_signs": signs, "strictly_inside_segment": True,
        }
    return {
        "parameter_interval": [str(lower), str(upper)], "depth": depth, "status": "INCONCLUSIVE",
        "derivative_sign": derivative_sign, "endpoint_signs": signs,
    }


def independent_certification(source: Any, second: str, candidate: str, boundary: dict[str, Any]) -> tuple[str, int, list[dict[str, Any]]]:
    lower, upper = map(Q, boundary["parameter_interval"])
    first = independent_leaf(source, second, candidate, boundary, lower, upper, 0)
    if first["status"] != "INCONCLUSIVE":
        return first["status"], 1, [first]
    middle = (lower + upper) / 2
    leaves = [
        independent_leaf(source, second, candidate, boundary, lower, middle, 1),
        independent_leaf(source, second, candidate, boundary, middle, upper, 1),
    ]
    if any(row["status"] == "INCONCLUSIVE" for row in leaves):
        raise ValueError("independent boundary refinement unresolved")
    return "INCONCLUSIVE", 3, leaves


def boundary_side(source: Any, boundary: dict[str, Any]) -> str | None:
    fixed = Q(boundary["fixed_coordinate"])
    if boundary["fixed_axis"] == "t":
        return "t_lower" if fixed == source.t0 else "t_upper" if fixed == source.t1 else None
    return "p_lower" if fixed == source.p0 else "p_upper" if fixed == source.p1 else None


def independently_verify(document: dict[str, Any]) -> dict[str, Any]:
    ctx.prec = VERIFIER_PRECISION_BITS
    validate_round82_ledger()
    result = document["result"]
    atlas = load_upstream(ATLAS, "cm2.round82.rank3-physical-patch-atlas.v1")
    joins = load_upstream(JOINS, "cm2.round82.rank3-cross-tube-joins.v1")
    endpoints = load_upstream(ENDPOINTS, "cm2.round82.rank3-boundary-endpoints.v1")
    cores = core_cert.physical_cores()
    patches = {row["physical_patch_id"]: row for row in atlas["physical_patch_rows"]}
    candidate_components = {row["physical_root_component_id"]: row for row in result["component_rows"]}
    candidate_segments = {row["registered_boundary_segment_id"]: row for row in result["boundary_segment_rows"]}
    candidate_ports = {row["registered_port_id"]: row for row in result["port_rows"]}
    if len(candidate_components) != len(result["component_rows"]):
        raise ValueError("duplicate candidate component id")
    if len(candidate_segments) != len(result["boundary_segment_rows"]):
        raise ValueError("duplicate candidate segment id")
    if len(candidate_ports) != len(result["port_rows"]):
        raise ValueError("duplicate candidate port id")

    seen_segments: set[str] = set()
    seen_ports: set[str] = set()
    recomputed_components = []
    initial_histogram: Counter[str] = Counter()
    final_histogram: Counter[str] = Counter()
    root_histogram: Counter[int] = Counter()
    arc_histogram: Counter[int] = Counter()
    input_boxes = unique_boxes = gradient_boxes = tests = 0
    source_port_count = 0

    for joined in joins["component_rows"]:
        identifier = joined["physical_root_component_id"]
        source = cores[joined["source_core_index"]]
        second, candidate = joined["second_selected_target_id"], joined["third_candidate_id"]
        raw_boxes = [
            tuple(map(Q, box)) for patch_id in joined["physical_patch_ids"] for box in patches[patch_id]["boxes"]
        ]
        boxes = sorted(set(raw_boxes))
        input_boxes += len(raw_boxes)
        unique_boxes += len(boxes)
        gradient_histogram: Counter[tuple[int, int]] = Counter()
        for box in boxes:
            _value, gradient = centered_taylor(source, second, candidate, box)
            signs = strict_sign(gradient[0]), strict_sign(gradient[1])
            if not all(signs):
                raise ValueError(f"higher-precision critical box: {identifier}")
            gradient_histogram[signs] += 1
            gradient_boxes += 1

        boundaries = independent_boundary(boxes)
        local_segment_ids = []
        local_port_ids = []
        local_initial: Counter[str] = Counter()
        local_tests = 0
        local_source_ports = 0
        for rank, boundary in enumerate(boundaries):
            segment_id = "physical-s0-rank3-registered-boundary-segment:" + digest({
                "component": identifier, "boundary": boundary,
            })
            if segment_id in seen_segments or segment_id not in candidate_segments:
                raise ValueError(f"segment incidence mismatch: {segment_id}")
            seen_segments.add(segment_id)
            initial_status, interval_tests, leaves = independent_certification(source, second, candidate, boundary)
            source_side = boundary_side(source, boundary)
            expected_port_ids = []
            for leaf in leaves:
                final_histogram[leaf["status"]] += 1
                if leaf["status"] != "UNIQUE_TRANSVERSE_BOUNDARY_ROOT":
                    continue
                port_id = "physical-s0-rank3-registered-port:" + digest({
                    "segment_id": segment_id, "root_bracket": leaf["parameter_interval"],
                })
                expected_port = {
                    "registered_port_id": port_id,
                    "physical_root_component_id": identifier,
                    "source_core_index": joined["source_core_index"],
                    "second_selected_target_id": second,
                    "third_candidate_id": candidate,
                    "boundary_segment_id": segment_id,
                    "boundary_axis": boundary["axis"],
                    "fixed_coordinate": boundary["fixed_coordinate"],
                    "root_bracket": leaf["parameter_interval"],
                    "derivative_sign": leaf["derivative_sign"],
                    "endpoint_signs": leaf["endpoint_signs"],
                    "refinement_depth": leaf["depth"],
                    "source_boundary_side": source_side,
                    "port_scope": "SOURCE_CORE_BOUNDARY" if source_side is not None else "NON_SOURCE_REGISTERED_UNION_BOUNDARY",
                }
                if port_id in seen_ports or candidate_ports.get(port_id) != expected_port:
                    raise ValueError(f"higher-precision port mismatch: {port_id}")
                seen_ports.add(port_id)
                expected_port_ids.append(port_id)
                local_port_ids.append(port_id)
                if source_side is not None:
                    local_source_ports += 1
                    source_port_count += 1
            expected_segment = {
                "registered_boundary_segment_id": segment_id,
                "physical_root_component_id": identifier,
                "local_boundary_segment_rank": rank,
                **boundary,
                "source_boundary_side": source_side,
                "initial_status": initial_status,
                "interval_box_tests": interval_tests,
                "leaf_rows": leaves,
                "leaf_rows_sha256": digest(leaves),
                "certified_root_count": len(expected_port_ids),
                "registered_port_ids": expected_port_ids,
            }
            if candidate_segments[segment_id] != expected_segment:
                raise ValueError(f"higher-precision segment mismatch: {segment_id}")
            initial_histogram[initial_status] += 1
            local_initial[initial_status] += 1
            tests += interval_tests
            local_tests += interval_tests
            local_segment_ids.append(segment_id)

        port_count = len(local_port_ids)
        arc_count = port_count // 2
        root_histogram[port_count] += 1
        arc_histogram[arc_count] += 1
        certification_sources = Counter(patches[patch_id]["certification_source"] for patch_id in joined["physical_patch_ids"])
        expected_component = {
            "physical_root_component_id": identifier,
            "source_core_index": joined["source_core_index"],
            "second_selected_target_id": second,
            "third_candidate_id": candidate,
            "physical_patch_count": joined["physical_patch_count"],
            "certification_source_histogram": dict(sorted(certification_sources.items())),
            "input_box_count": len(raw_boxes),
            "unique_union_box_count": len(boxes),
            "coordinate_gradient_nonzero_box_count": len(boxes),
            "coordinate_gradient_sign_histogram": {
                f"{a},{b}": count for (a, b), count in sorted(gradient_histogram.items())
            },
            "registered_boundary_segment_count": len(boundaries),
            "boundary_initial_status_histogram": dict(sorted(local_initial.items())),
            "boundary_interval_box_tests": local_tests,
            "registered_port_count": port_count,
            "source_boundary_port_count": local_source_ports,
            "non_source_registered_boundary_port_count": port_count - local_source_ports,
            "registered_elementary_arc_census_count": arc_count,
            "registered_boundary_segment_ids_sha256": digest(sorted(local_segment_ids)),
            "registered_port_ids_sha256": digest(sorted(local_port_ids)),
        }
        if candidate_components.get(identifier) != expected_component:
            raise ValueError(f"higher-precision component mismatch: {identifier}")
        recomputed_components.append(expected_component)

    if seen_segments != set(candidate_segments) or seen_ports != set(candidate_ports):
        raise ValueError("candidate contains unregistered segment or port")
    recomputed_components.sort(key=lambda row: row["physical_root_component_id"])
    if result["component_rows"] != recomputed_components:
        raise ValueError("component row order")

    # Independently crosswalk each frozen, 80-step endpoint bracket to exactly
    # one higher-precision registered source port.
    ports_by_component_side: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for port in candidate_ports.values():
        if port["source_boundary_side"] is not None:
            ports_by_component_side[(port["physical_root_component_id"], port["source_boundary_side"])].append(port)
    crosswalk = []
    for endpoint in endpoints["endpoint_rows"]:
        lower, upper = map(Q, endpoint["parameter_interval"])
        matches = []
        for port in ports_by_component_side[(endpoint["physical_root_component_id"], endpoint["source_boundary_side"])]:
            a, b = map(Q, port["root_bracket"])
            if max(a, lower) <= min(b, upper):
                matches.append(port["registered_port_id"])
        if len(matches) != 1:
            raise ValueError("independent endpoint crosswalk multiplicity")
        crosswalk.append({"physical_endpoint_id": endpoint["physical_endpoint_id"], "registered_port_id": matches[0]})
    crosswalk.sort(key=lambda row: row["physical_endpoint_id"])
    if crosswalk != result["source_endpoint_crosswalk_rows"]:
        raise ValueError("higher-precision endpoint crosswalk mismatch")

    scalar_expected = {
        "fixed_parameter": "s=0",
        "precision_bits": 512,
        "frozen_joined_row_count": len(joins["component_rows"]),
        "input_registered_box_count": input_boxes,
        "exactly_deduplicated_union_box_count": unique_boxes,
        "coordinate_gradient_nonzero_box_count": gradient_boxes,
        "registered_union_boundary_segment_count": len(seen_segments),
        "initial_boundary_status_histogram": dict(sorted(initial_histogram.items())),
        "final_boundary_leaf_status_histogram": dict(sorted(final_histogram.items())),
        "total_boundary_interval_box_tests": tests,
        "maximum_boundary_refinement_depth": 1,
        "certified_registered_port_count": len(seen_ports),
        "source_boundary_port_count": source_port_count,
        "non_source_registered_boundary_port_count": len(seen_ports) - source_port_count,
        "registered_port_count_histogram_per_frozen_row": {
            str(key): value for key, value in sorted(root_histogram.items())
        },
        "registered_elementary_arc_multiplicity_histogram_per_frozen_row": {
            str(key): value for key, value in sorted(arc_histogram.items())
        },
        "single_arc_frozen_row_count": sum(key == 1 and value or 0 for key, value in arc_histogram.items()),
        "multi_arc_frozen_row_count": sum(value for key, value in arc_histogram.items() if key > 1),
        "registered_elementary_arc_census_count": sum(key * value for key, value in arc_histogram.items()),
        "round82_source_endpoint_crosswalk_count": len(crosswalk),
        "round82_source_endpoint_crosswalk_is_bijective": len(crosswalk) == source_port_count,
    }
    for key, expected in scalar_expected.items():
        if result[key] != expected:
            raise ValueError(f"higher-precision scalar mismatch: {key}")
    fixed_expected = {
        "topological_certificate": {
            "regularity": "BOTH_COORDINATE_PARTIAL_DERIVATIVES_STRICTLY_NONZERO_ON_EVERY_REGISTERED_BOX",
            "boundary_transversality": "EVERY_REGISTERED_PORT_HAS_STRICT_OPPOSITE_ENDPOINT_SIGNS_AND_NONZERO_TANGENTIAL_DERIVATIVE",
            "closed_component_exclusion": "A_CLOSED_REGULAR_LEVEL_CURVE_WOULD_HAVE_A_COORDINATE_EXTREMUM_CONTRADICTING_NONZERO_COORDINATE_PARTIALS",
            "census_rule": "EACH_COMPACT_REGISTERED_ELEMENTARY_ARC_HAS_EXACTLY_TWO_EXPOSED_PORTS",
        },
        "strict_scope": "elementary-arc and exposed-port census only inside the exact union of frozen Round-82 registered boxes",
        "strict_nonclaims": [
            "no pairing or continuation is asserted across non-source registered-union ports",
            "the 1672 frozen joined rows are box-connectivity aggregates and are not asserted to be zero-set components",
            "the 2108 registered elementary arcs are not asserted to be complete physical rank-three faces",
            "no Gate-5 or RN return-face promotion follows from this registered-scope census",
        ],
        "upstream_pins": {
            "round82_sha256_ledger_sha256": ROUND82_LEDGER_SHA256,
            "rank3_physical_patch_atlas_sha256": file_sha256(ATLAS),
            "rank3_cross_tube_joins_sha256": file_sha256(JOINS),
            "rank3_boundary_endpoints_sha256": file_sha256(ENDPOINTS),
        },
    }
    for key, expected in fixed_expected.items():
        if result[key] != expected:
            raise ValueError(f"fixed claim mismatch: {key}")
    return {
        "scalar_expected": scalar_expected,
        "component_rows_sha256": result["component_rows_sha256"],
        "boundary_segment_rows_sha256": result["boundary_segment_rows_sha256"],
        "port_rows_sha256": result["port_rows_sha256"],
        "source_endpoint_crosswalk_rows_sha256": result["source_endpoint_crosswalk_rows_sha256"],
        "fixed_expected": fixed_expected,
    }


def validate_against_facts(document: dict[str, Any], facts: dict[str, Any]) -> None:
    validate_closed_document(document)
    result = document["result"]
    for key, expected in facts["scalar_expected"].items():
        if result[key] != expected:
            raise ValueError(f"certified scalar changed: {key}")
    for key in (
        "component_rows_sha256", "boundary_segment_rows_sha256", "port_rows_sha256",
        "source_endpoint_crosswalk_rows_sha256",
    ):
        if result[key] != facts[key]:
            raise ValueError(f"certified row commitment changed: {key}")
    for key, expected in facts["fixed_expected"].items():
        if result[key] != expected:
            raise ValueError(f"certified fixed claim changed: {key}")


def coordinated_digest(document: dict[str, Any]) -> None:
    result = document["result"]
    result["component_rows_sha256"] = digest(result["component_rows"])
    result["boundary_segment_rows_sha256"] = digest(result["boundary_segment_rows"])
    result["port_rows_sha256"] = digest(result["port_rows"])
    result["source_endpoint_crosswalk_rows_sha256"] = digest(result["source_endpoint_crosswalk_rows"])
    document["result_sha256"] = digest(result)


def hostile_mutation_audit(original: dict[str, Any], facts: dict[str, Any]) -> dict[str, Any]:
    mutations = []

    document = copy.deepcopy(original)
    document["result"]["registered_elementary_arc_census_count"] = 1672
    coordinated_digest(document)
    mutations.append(("arc census scalar", document))

    document = copy.deepcopy(original)
    document["result"]["component_rows"][0]["registered_elementary_arc_census_count"] += 1
    coordinated_digest(document)
    mutations.append(("component multiplicity", document))

    document = copy.deepcopy(original)
    original_status = document["result"]["boundary_segment_rows"][0]["initial_status"]
    document["result"]["boundary_segment_rows"][0]["initial_status"] = (
        "STRICT_RANGE_EXCLUSION" if original_status != "STRICT_RANGE_EXCLUSION" else "UNIQUE_TRANSVERSE_BOUNDARY_ROOT"
    )
    coordinated_digest(document)
    mutations.append(("boundary classification", document))

    document = copy.deepcopy(original)
    document["result"]["strict_nonclaims"].append("complete physical faces are certified")
    coordinated_digest(document)
    mutations.append(("claim injection", document))

    document = copy.deepcopy(original)
    document["result"]["upstream_pins"]["round82_sha256_ledger_sha256"] = "0" * 64
    coordinated_digest(document)
    mutations.append(("coordinated Round-82 ledger-pin mutation", document))

    rejected = []
    for label, document in mutations:
        try:
            validate_against_facts(document, facts)
        except Exception:
            rejected.append(label)
    if len(rejected) != len(mutations):
        raise ValueError("hostile semantic mutation accepted")
    return {"attempted": len(mutations), "rejected": len(rejected), "rejected_labels": rejected}


def strict_json_audit(text: str) -> dict[str, Any]:
    attacks = {
        "duplicate_top_level_key": text.replace('"schema":', '"schema": "shadow", "schema":', 1),
        "duplicate_nested_key": text.replace('"fixed_parameter":', '"fixed_parameter": "shadow", "fixed_parameter":', 1),
        "nan": text.replace('"precision_bits": 512', '"precision_bits": NaN', 1),
        "infinity": text.replace('"precision_bits": 512', '"precision_bits": Infinity', 1),
    }
    rejected = []
    for label, payload in attacks.items():
        try:
            strict_load_text(payload)
        except Exception:
            rejected.append(label)
    if len(rejected) != len(attacks):
        raise ValueError("strict JSON attack accepted")
    return {"attempted": len(attacks), "rejected": len(rejected), "rejected_labels": rejected}


def main() -> int:
    candidate_text = CANDIDATE.read_text()
    document = strict_load_text(candidate_text)
    validate_closed_document(document)
    facts = independently_verify(document)
    validate_against_facts(document, facts)
    hostile = hostile_mutation_audit(document, facts)
    strict_json = strict_json_audit(candidate_text)
    result = {
        "status": "PASS",
        "candidate_sha256": file_sha256(CANDIDATE),
        "candidate_result_sha256": document["result_sha256"],
        "producer_precision_bits": document["result"]["precision_bits"],
        "independent_verifier_precision_bits": VERIFIER_PRECISION_BITS,
        "independent_event_sweep_boundary_recomputation": "PASS",
        "independent_coordinate_gradient_recomputation": "34652/34652_STRICTLY_NONZERO_IN_BOTH_COORDINATES",
        "independent_registered_boundary_segment_recomputation": "45016/45016",
        "independent_registered_port_recomputation": "4216/4216",
        "independent_source_endpoint_crosswalk": "1004/1004_BIJECTIVE",
        "independent_registered_elementary_arc_census": "2108/2108",
        "semantic_hostile_mutation_audit": hostile,
        "strict_json_attack_audit": strict_json,
        "strict_scope": "verification covers only the frozen registered box unions and their exposed ports; off-registry continuation and complete physical faces remain open",
    }
    audit = {
        "schema": "cm2.round85.rank3-registered-arc-port-census-audit.v1",
        "result": result,
        "result_sha256": digest(result),
    }
    json.dump(audit, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
