#!/usr/bin/env python3
"""Certify the elementary-arc/port census inside the frozen rank-three registry.

This generator deliberately stops at the boundary of the Round-82 registered
box unions.  It removes internal rectangle sides exactly, certifies every zero
of the physical discriminant on the exposed rectilinear boundary, and uses
strict nonvanishing of both coordinate derivatives on every registered box to
turn the boundary-root count into an elementary-arc census.  It does *not*
pair the non-source ports across uncovered carrier gaps and therefore does not
claim a global physical-face count.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import digest
from cm2_round80_time3_adaptive_carrier_resolver import centered_taylor, strict_sign, third_tangency_jet


HERE = Path(__file__).resolve().parent
ATLAS = HERE / "cm2-round82-rank3-physical-patch-atlas-2026-07-21.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
ENDPOINTS = HERE / "cm2-round82-rank3-boundary-endpoints-2026-07-21.json"
ROUND82_LEDGER = HERE / "cm2-eighty-second-direct-assault-manifest-2026-07-21.sha256"
ROUND82_LEDGER_SHA256 = "ba6856a54f5a112fb349d3a8d3961b7c6e21f021529bb86af521b1d3293ec93d"
PRECISION_BITS = 512
MAXIMUM_BOUNDARY_REFINEMENT_DEPTH = 1


def strict_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def load_document(path: Path, schema: str) -> dict[str, Any]:
    document = json.loads(
        path.read_text(), object_pairs_hook=strict_object_pairs, parse_constant=reject_nonfinite
    )
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError(f"non-closed upstream top-level schema: {path.name}")
    if document["schema"] != schema:
        raise RuntimeError(f"upstream schema mismatch: {path.name}")
    if document["result_sha256"] != digest(document["result"]):
        raise RuntimeError(f"upstream result digest mismatch: {path.name}")
    return document


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validated_round82_ledger() -> dict[str, str]:
    if file_sha256(ROUND82_LEDGER) != ROUND82_LEDGER_SHA256:
        raise RuntimeError("frozen Round-82 SHA ledger digest mismatch")
    entries: dict[str, str] = {}
    for line in ROUND82_LEDGER.read_text().splitlines():
        parts = line.split("  ")
        if len(parts) != 2 or len(parts[0]) != 64 or any(character not in "0123456789abcdef" for character in parts[0]):
            raise RuntimeError("malformed frozen Round-82 SHA ledger")
        checksum, name = parts
        if name in entries:
            raise RuntimeError("duplicate frozen Round-82 SHA ledger path")
        entries[name] = checksum
    required = {
        "deliverables/" + ATLAS.name: ATLAS,
        "deliverables/" + JOINS.name: JOINS,
        "deliverables/" + ENDPOINTS.name: ENDPOINTS,
    }
    for name, path in required.items():
        if entries.get(name) != file_sha256(path):
            raise RuntimeError(f"Round-82 ledger pin mismatch: {name}")
    return entries


def merge_open_intervals(intervals: Iterable[tuple[Q, Q]]) -> list[tuple[Q, Q]]:
    merged: list[tuple[Q, Q]] = []
    for lower, upper in sorted(set(intervals)):
        if not lower < upper:
            raise RuntimeError("nonpositive registered box side")
        if merged and lower <= merged[-1][1]:
            merged[-1] = merged[-1][0], max(merged[-1][1], upper)
        else:
            merged.append((lower, upper))
    return merged


def contains_open(intervals: list[tuple[Q, Q]], point: Q) -> bool:
    return any(lower < point < upper for lower, upper in intervals)


def symmetric_boundary_atoms(
    negative_side: list[tuple[Q, Q]], positive_side: list[tuple[Q, Q]]
) -> list[tuple[Q, Q, int]]:
    """Return maximal boundary atoms; inside_side is -1 or +1."""
    negative = merge_open_intervals(negative_side) if negative_side else []
    positive = merge_open_intervals(positive_side) if positive_side else []
    coordinates = sorted({value for interval in negative + positive for value in interval})
    atoms: list[tuple[Q, Q, int]] = []
    for lower, upper in zip(coordinates, coordinates[1:]):
        if lower == upper:
            continue
        middle = (lower + upper) / 2
        has_negative = contains_open(negative, middle)
        has_positive = contains_open(positive, middle)
        if has_negative == has_positive:
            continue
        inside_side = -1 if has_negative else 1
        if atoms and atoms[-1][1] == lower and atoms[-1][2] == inside_side:
            atoms[-1] = atoms[-1][0], upper, inside_side
        else:
            atoms.append((lower, upper, inside_side))
    return atoms


def union_boundary_segments(boxes: list[tuple[Q, Q, Q, Q]]) -> list[dict[str, Any]]:
    """Cancel all internal rectangle sides before emitting exposed segments."""
    vertical_coordinates = sorted({value for box in boxes for value in box[:2]})
    horizontal_coordinates = sorted({value for box in boxes for value in box[2:]})
    rows: list[dict[str, Any]] = []
    for fixed in vertical_coordinates:
        negative = [(p0, p1) for t0, t1, p0, p1 in boxes if t0 < fixed <= t1]
        positive = [(p0, p1) for t0, t1, p0, p1 in boxes if t0 <= fixed < t1]
        for lower, upper, inside_side in symmetric_boundary_atoms(negative, positive):
            rows.append({
                "axis": "p",
                "fixed_axis": "t",
                "fixed_coordinate": str(fixed),
                "parameter_interval": [str(lower), str(upper)],
                "inside_side": inside_side,
            })
    for fixed in horizontal_coordinates:
        negative = [(t0, t1) for t0, t1, p0, p1 in boxes if p0 < fixed <= p1]
        positive = [(t0, t1) for t0, t1, p0, p1 in boxes if p0 <= fixed < p1]
        for lower, upper, inside_side in symmetric_boundary_atoms(negative, positive):
            rows.append({
                "axis": "t",
                "fixed_axis": "p",
                "fixed_coordinate": str(fixed),
                "parameter_interval": [str(lower), str(upper)],
                "inside_side": inside_side,
            })
    rows.sort(key=lambda row: (
        row["fixed_axis"], Q(row["fixed_coordinate"]),
        Q(row["parameter_interval"][0]), Q(row["parameter_interval"][1]), row["inside_side"],
    ))
    return rows


def interval_jet(source: Any, second: str, candidate: str, segment: dict[str, Any], lower: Q, upper: Q) -> Any:
    fixed = Q(segment["fixed_coordinate"])
    if segment["axis"] == "p":
        return third_tangency_jet(source, second, candidate, fixed, fixed, lower, upper)
    return third_tangency_jet(source, second, candidate, lower, upper, fixed, fixed)


def point_value(source: Any, second: str, candidate: str, segment: dict[str, Any], value: Q) -> Any:
    fixed = Q(segment["fixed_coordinate"])
    if segment["axis"] == "p":
        return third_tangency_jet(source, second, candidate, fixed, fixed, value, value).value
    return third_tangency_jet(source, second, candidate, value, value, fixed, fixed).value


def classify_interval(
    source: Any,
    second: str,
    candidate: str,
    segment: dict[str, Any],
    lower: Q,
    upper: Q,
    depth: int,
) -> dict[str, Any]:
    jet = interval_jet(source, second, candidate, segment, lower, upper)
    range_sign = strict_sign(jet.value)
    if range_sign:
        return {
            "parameter_interval": [str(lower), str(upper)],
            "depth": depth,
            "status": "STRICT_RANGE_EXCLUSION",
            "range_sign": range_sign,
        }
    derivative_index = 1 if segment["axis"] == "p" else 0
    derivative_sign = strict_sign(jet.gradient[derivative_index])
    lower_sign = strict_sign(point_value(source, second, candidate, segment, lower))
    upper_sign = strict_sign(point_value(source, second, candidate, segment, upper))
    if derivative_sign and lower_sign and upper_sign:
        if lower_sign == upper_sign:
            return {
                "parameter_interval": [str(lower), str(upper)],
                "depth": depth,
                "status": "STRICT_MONOTONE_SAME_SIGN_EXCLUSION",
                "derivative_sign": derivative_sign,
                "endpoint_signs": [lower_sign, upper_sign],
            }
        return {
            "parameter_interval": [str(lower), str(upper)],
            "depth": depth,
            "status": "UNIQUE_TRANSVERSE_BOUNDARY_ROOT",
            "derivative_sign": derivative_sign,
            "endpoint_signs": [lower_sign, upper_sign],
            "strictly_inside_segment": True,
        }
    return {
        "parameter_interval": [str(lower), str(upper)],
        "depth": depth,
        "status": "INCONCLUSIVE",
        "derivative_sign": derivative_sign,
        "endpoint_signs": [lower_sign, upper_sign],
    }


def certify_segment(source: Any, second: str, candidate: str, segment: dict[str, Any]) -> dict[str, Any]:
    lower, upper = map(Q, segment["parameter_interval"])
    initial = classify_interval(source, second, candidate, segment, lower, upper, 0)
    tests = 1
    if initial["status"] != "INCONCLUSIVE":
        return {"initial_status": initial["status"], "tests": tests, "leaf_rows": [initial]}
    middle = (lower + upper) / 2
    leaves = [
        classify_interval(source, second, candidate, segment, lower, middle, 1),
        classify_interval(source, second, candidate, segment, middle, upper, 1),
    ]
    tests += 2
    if any(row["status"] == "INCONCLUSIVE" for row in leaves):
        raise RuntimeError("boundary classifier unresolved after the pinned depth-one refinement")
    return {"initial_status": "INCONCLUSIVE", "tests": tests, "leaf_rows": leaves}


def source_boundary_side(source: Any, segment: dict[str, Any]) -> str | None:
    fixed = Q(segment["fixed_coordinate"])
    if segment["fixed_axis"] == "t":
        if fixed == source.t0:
            return "t_lower"
        if fixed == source.t1:
            return "t_upper"
    else:
        if fixed == source.p0:
            return "p_lower"
        if fixed == source.p1:
            return "p_upper"
    return None


def endpoint_crosswalk(
    frozen_rows: list[dict[str, Any]], port_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    by_component_side: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for port in port_rows:
        if port["source_boundary_side"] is not None:
            by_component_side[(port["physical_root_component_id"], port["source_boundary_side"])].append(port)
    result = []
    for endpoint in frozen_rows:
        key = (endpoint["physical_root_component_id"], endpoint["source_boundary_side"])
        frozen_lower, frozen_upper = map(Q, endpoint["parameter_interval"])
        matches = []
        for port in by_component_side[key]:
            lower, upper = map(Q, port["root_bracket"])
            if max(lower, frozen_lower) <= min(upper, frozen_upper):
                matches.append(port)
        if len(matches) != 1:
            raise RuntimeError(f"source endpoint crosswalk multiplicity {len(matches)} for {endpoint['physical_endpoint_id']}")
        result.append({
            "physical_endpoint_id": endpoint["physical_endpoint_id"],
            "registered_port_id": matches[0]["registered_port_id"],
        })
    result.sort(key=lambda row: row["physical_endpoint_id"])
    if len({row["registered_port_id"] for row in result}) != len(result):
        raise RuntimeError("source endpoint crosswalk is not injective")
    return result


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    ctx.prec = precision_bits
    validated_round82_ledger()
    atlas_document = load_document(ATLAS, "cm2.round82.rank3-physical-patch-atlas.v1")
    join_document = load_document(JOINS, "cm2.round82.rank3-cross-tube-joins.v1")
    endpoint_document = load_document(ENDPOINTS, "cm2.round82.rank3-boundary-endpoints.v1")
    atlas = atlas_document["result"]
    joins = join_document["result"]
    endpoints = endpoint_document["result"]
    cores = core_cert.physical_cores()
    if atlas["physical_patch_count"] != 1780 or joins["joined_physical_root_component_count"] != 1672:
        raise RuntimeError("unexpected frozen Round-82 registry size")
    patch_by_id = {row["physical_patch_id"]: row for row in atlas["physical_patch_rows"]}
    if len(patch_by_id) != 1780:
        raise RuntimeError("duplicate physical patch identifier")

    segment_rows: list[dict[str, Any]] = []
    port_rows: list[dict[str, Any]] = []
    component_rows: list[dict[str, Any]] = []
    input_box_count = 0
    unique_box_count = 0
    gradient_box_count = 0
    total_tests = 0
    initial_histogram: Counter[str] = Counter()
    final_leaf_histogram: Counter[str] = Counter()

    for component in joins["component_rows"]:
        source = cores[component["source_core_index"]]
        second = component["second_selected_target_id"]
        candidate = component["third_candidate_id"]
        raw_boxes = [
            tuple(map(Q, raw_box))
            for patch_id in component["physical_patch_ids"]
            for raw_box in patch_by_id[patch_id]["boxes"]
        ]
        input_box_count += len(raw_boxes)
        boxes = sorted(set(raw_boxes))
        unique_box_count += len(boxes)
        if any(not (box[0] < box[1] and box[2] < box[3]) for box in boxes):
            raise RuntimeError("degenerate registered box")
        gradient_sign_histogram: Counter[tuple[int, int]] = Counter()
        for box in boxes:
            _value, gradient = centered_taylor(source, second, candidate, box)
            signs = strict_sign(gradient[0]), strict_sign(gradient[1])
            if not all(signs):
                raise RuntimeError(f"coordinate criticality unresolved in {component['physical_root_component_id']}")
            gradient_sign_histogram[signs] += 1
            gradient_box_count += 1

        boundaries = union_boundary_segments(boxes)
        local_ports = []
        local_segment_ids = []
        local_initial: Counter[str] = Counter()
        local_tests = 0
        for local_rank, boundary in enumerate(boundaries):
            identity = {
                "component": component["physical_root_component_id"],
                "boundary": boundary,
            }
            segment_id = "physical-s0-rank3-registered-boundary-segment:" + digest(identity)
            certification = certify_segment(source, second, candidate, boundary)
            initial_histogram[certification["initial_status"]] += 1
            local_initial[certification["initial_status"]] += 1
            total_tests += certification["tests"]
            local_tests += certification["tests"]
            leaf_histogram = Counter(row["status"] for row in certification["leaf_rows"])
            final_leaf_histogram.update(leaf_histogram)
            source_side = source_boundary_side(source, boundary)
            segment_port_ids = []
            for leaf_rank, leaf in enumerate(certification["leaf_rows"]):
                if leaf["status"] != "UNIQUE_TRANSVERSE_BOUNDARY_ROOT":
                    continue
                port_identity = {"segment_id": segment_id, "root_bracket": leaf["parameter_interval"]}
                port = {
                    "registered_port_id": "physical-s0-rank3-registered-port:" + digest(port_identity),
                    "physical_root_component_id": component["physical_root_component_id"],
                    "source_core_index": component["source_core_index"],
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
                port_rows.append(port)
                local_ports.append(port)
                segment_port_ids.append(port["registered_port_id"])
            segment_row = {
                "registered_boundary_segment_id": segment_id,
                "physical_root_component_id": component["physical_root_component_id"],
                "local_boundary_segment_rank": local_rank,
                **boundary,
                "source_boundary_side": source_side,
                "initial_status": certification["initial_status"],
                "interval_box_tests": certification["tests"],
                "leaf_rows": certification["leaf_rows"],
                "leaf_rows_sha256": digest(certification["leaf_rows"]),
                "certified_root_count": len(segment_port_ids),
                "registered_port_ids": segment_port_ids,
            }
            segment_rows.append(segment_row)
            local_segment_ids.append(segment_id)

        root_count = len(local_ports)
        if root_count % 2:
            raise RuntimeError(f"odd registered boundary root count in {component['physical_root_component_id']}")
        source_count = sum(port["source_boundary_side"] is not None for port in local_ports)
        certification_sources = Counter(patch_by_id[identifier]["certification_source"] for identifier in component["physical_patch_ids"])
        component_rows.append({
            "physical_root_component_id": component["physical_root_component_id"],
            "source_core_index": component["source_core_index"],
            "second_selected_target_id": second,
            "third_candidate_id": candidate,
            "physical_patch_count": component["physical_patch_count"],
            "certification_source_histogram": dict(sorted(certification_sources.items())),
            "input_box_count": len(raw_boxes),
            "unique_union_box_count": len(boxes),
            "coordinate_gradient_nonzero_box_count": len(boxes),
            "coordinate_gradient_sign_histogram": {
                f"{dt_sign},{dp_sign}": count
                for (dt_sign, dp_sign), count in sorted(gradient_sign_histogram.items())
            },
            "registered_boundary_segment_count": len(boundaries),
            "boundary_initial_status_histogram": dict(sorted(local_initial.items())),
            "boundary_interval_box_tests": local_tests,
            "registered_port_count": root_count,
            "source_boundary_port_count": source_count,
            "non_source_registered_boundary_port_count": root_count - source_count,
            "registered_elementary_arc_census_count": root_count // 2,
            "registered_boundary_segment_ids_sha256": digest(sorted(local_segment_ids)),
            "registered_port_ids_sha256": digest(sorted(port["registered_port_id"] for port in local_ports)),
        })

    segment_rows.sort(key=lambda row: row["registered_boundary_segment_id"])
    port_rows.sort(key=lambda row: row["registered_port_id"])
    component_rows.sort(key=lambda row: row["physical_root_component_id"])
    crosswalk_rows = endpoint_crosswalk(endpoints["endpoint_rows"], port_rows)
    root_histogram = Counter(row["registered_port_count"] for row in component_rows)
    arc_histogram = Counter(row["registered_elementary_arc_census_count"] for row in component_rows)
    source_ports = sum(row["source_boundary_side"] is not None for row in port_rows)
    non_source_ports = len(port_rows) - source_ports
    total_arcs = sum(row["registered_elementary_arc_census_count"] for row in component_rows)
    multi_arc_rows = sum(row["registered_elementary_arc_census_count"] > 1 for row in component_rows)

    result = {
        "fixed_parameter": "s=0",
        "precision_bits": precision_bits,
        "frozen_joined_row_count": len(component_rows),
        "input_registered_box_count": input_box_count,
        "exactly_deduplicated_union_box_count": unique_box_count,
        "coordinate_gradient_nonzero_box_count": gradient_box_count,
        "registered_union_boundary_segment_count": len(segment_rows),
        "initial_boundary_status_histogram": dict(sorted(initial_histogram.items())),
        "final_boundary_leaf_status_histogram": dict(sorted(final_leaf_histogram.items())),
        "total_boundary_interval_box_tests": total_tests,
        "maximum_boundary_refinement_depth": MAXIMUM_BOUNDARY_REFINEMENT_DEPTH,
        "certified_registered_port_count": len(port_rows),
        "source_boundary_port_count": source_ports,
        "non_source_registered_boundary_port_count": non_source_ports,
        "registered_port_count_histogram_per_frozen_row": {
            str(key): value for key, value in sorted(root_histogram.items())
        },
        "registered_elementary_arc_multiplicity_histogram_per_frozen_row": {
            str(key): value for key, value in sorted(arc_histogram.items())
        },
        "single_arc_frozen_row_count": len(component_rows) - multi_arc_rows,
        "multi_arc_frozen_row_count": multi_arc_rows,
        "registered_elementary_arc_census_count": total_arcs,
        "round82_source_endpoint_crosswalk_count": len(crosswalk_rows),
        "round82_source_endpoint_crosswalk_is_bijective": len(crosswalk_rows) == source_ports,
        "component_rows": component_rows,
        "component_rows_sha256": digest(component_rows),
        "boundary_segment_rows": segment_rows,
        "boundary_segment_rows_sha256": digest(segment_rows),
        "port_rows": port_rows,
        "port_rows_sha256": digest(port_rows),
        "source_endpoint_crosswalk_rows": crosswalk_rows,
        "source_endpoint_crosswalk_rows_sha256": digest(crosswalk_rows),
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

    expected_initial = {
        "INCONCLUSIVE": 348,
        "STRICT_MONOTONE_SAME_SIGN_EXCLUSION": 27184,
        "STRICT_RANGE_EXCLUSION": 13356,
        "UNIQUE_TRANSVERSE_BOUNDARY_ROOT": 4128,
    }
    expected_root_histogram = {2: 1568, 4: 12, 6: 40, 8: 16, 10: 8, 14: 8, 16: 4, 18: 4, 22: 4, 24: 4, 38: 4}
    expected_arc_histogram = {key // 2: value for key, value in expected_root_histogram.items()}
    invariants = [
        input_box_count == unique_box_count == gradient_box_count == 34652,
        len(component_rows) == 1672,
        len(segment_rows) == 45016,
        dict(initial_histogram) == expected_initial,
        total_tests == 45712,
        len(port_rows) == 4216,
        source_ports == len(crosswalk_rows) == endpoints["certified_source_boundary_endpoint_count"] == 1004,
        non_source_ports == 3212,
        dict(root_histogram) == expected_root_histogram,
        dict(arc_histogram) == expected_arc_histogram,
        multi_arc_rows == 104,
        total_arcs == 2108,
        result["round82_source_endpoint_crosswalk_is_bijective"],
    ]
    if not all(invariants):
        diagnostic = {
            "boxes": [input_box_count, unique_box_count, gradient_box_count],
            "components": len(component_rows),
            "segments": len(segment_rows),
            "initial": dict(initial_histogram),
            "tests": total_tests,
            "ports": [len(port_rows), source_ports, non_source_ports],
            "root_histogram": dict(root_histogram),
            "arc_histogram": dict(arc_histogram),
            "multi_arc_rows": multi_arc_rows,
            "arcs": total_arcs,
        }
        raise RuntimeError(f"registered arc/port invariant mismatch: {diagnostic}")
    return {
        "schema": "cm2.round85.rank3-registered-arc-port-census.v1",
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
