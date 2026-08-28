#!/usr/bin/env python3
"""Freeze the first off-registry continuation stage for all non-source ports."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round76_r2_numeric_fields_generator import Jet, center, collision, normal
from cm2_round79_tangency_intersection_generator import aq, digest, interval, strict_sign
from cm2_round80_time3_adaptive_carrier_resolver import third_tangency_jet


HERE = Path(__file__).resolve().parent
ARC_PORTS = HERE / "cm2-round85-rank3-registered-arc-port-census-2026-07-22.json"
ATLAS = HERE / "cm2-round82-rank3-physical-patch-atlas-2026-07-21.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
GEOMETRY = HERE / "cm2-round80-time3-carrier-geometry-2026-07-21.json"
ROUND82_LEDGER = HERE / "cm2-eighty-second-direct-assault-manifest-2026-07-21.sha256"
ROUND80_LEDGER = HERE / "cm2-eightieth-direct-assault-manifest-2026-07-21.sha256"
ARC_PORTS_SHA256 = "11feee98133d133ecc20654389dd559fa1fbd06f9210ef10d52ec6d86f479f2d"
ROUND82_LEDGER_SHA256 = "ba6856a54f5a112fb349d3a8d3961b7c6e21f021529bb86af521b1d3293ec93d"
ROUND80_LEDGER_SHA256 = "11d6a17fbf7aca0855cf9792ea3b3e4c810992cfa84009b016b767545cea22e6"
PRECISION_BITS = 384
GRID = 64


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def load_document(path: Path, schema: str) -> dict[str, Any]:
    document = json.loads(path.read_text(), object_pairs_hook=strict_pairs, parse_constant=reject_nonfinite)
    if set(document) != {"schema", "result", "result_sha256"}:
        raise RuntimeError(f"non-closed upstream document: {path.name}")
    if document["schema"] != schema or document["result_sha256"] != digest(document["result"]):
        raise RuntimeError(f"upstream validation failed: {path.name}")
    return document


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ledger_entries(path: Path, expected: str) -> dict[str, str]:
    if file_sha256(path) != expected:
        raise RuntimeError(f"frozen ledger digest mismatch: {path.name}")
    entries: dict[str, str] = {}
    for line in path.read_text().splitlines():
        parts = line.split("  ")
        if len(parts) != 2 or len(parts[0]) != 64 or any(c not in "0123456789abcdef" for c in parts[0]):
            raise RuntimeError(f"malformed ledger: {path.name}")
        checksum, name = parts
        if name in entries:
            raise RuntimeError(f"duplicate ledger path: {name}")
        entries[name] = checksum
    return entries


def require_pin(entries: dict[str, str], path: Path) -> None:
    matches = [checksum for name, checksum in entries.items() if Path(name).name == path.name]
    if matches != [file_sha256(path)]:
        raise RuntimeError(f"ledger pin mismatch: {path.name}")


def coordinate(core: Any, axis: str, index: int) -> Q:
    lower, upper = (core.t0, core.t1) if axis == "t" else (core.p0, core.p1)
    return lower + (upper - lower) * Q(index, GRID)


def grid_cell(path: str) -> tuple[int, int]:
    prefix, base_i, tail = path.split(":")
    base_j, suffix = tail[:-2], tail[-2:]
    if prefix != "g32" or len(suffix) != 2 or any(bit not in "01" for bit in suffix):
        raise RuntimeError(f"unexpected seed path: {path}")
    return 2 * int(base_i) + int(suffix[0]), 2 * int(base_j) + int(suffix[1])


def dyadic_path(cell: tuple[int, int]) -> str:
    i, j = cell
    return f"g32:{i // 2}:{j // 2}{i % 2}{j % 2}"


def point_value(source: Any, second: str, candidate: str, axis: str, fixed: Q, value: Q) -> Any:
    if axis == "p":
        return third_tangency_jet(source, second, candidate, fixed, fixed, value, value).value
    return third_tangency_jet(source, second, candidate, value, value, fixed, fixed).value


def isolate_grid_cell(
    source: Any, second: str, candidate: str, axis: str, fixed: Q,
    bracket: tuple[Q, Q], endpoint_signs: tuple[int, int],
) -> dict[str, Any]:
    lower, upper = bracket
    lower_sign, upper_sign = endpoint_signs
    if lower_sign * upper_sign != -1:
        raise RuntimeError("port bracket lacks opposite endpoint signs")
    coordinates = [coordinate(source, axis, index) for index in range(GRID + 1)]
    cuts = [value for value in coordinates[1:-1] if lower < value < upper]
    trace = []
    while cuts:
        cut = cuts[len(cuts) // 2]
        cut_sign = strict_sign(point_value(source, second, candidate, axis, fixed, cut))
        if cut_sign == 0:
            raise RuntimeError("port root unresolved on a physical grid line")
        trace.append({"cut_coordinate": str(cut), "cut_sign": cut_sign})
        if cut_sign == lower_sign:
            lower, lower_sign = cut, cut_sign
        else:
            upper, upper_sign = cut, cut_sign
        cuts = [value for value in cuts if lower < value < upper]
    cells = [index for index in range(GRID) if coordinates[index] <= lower < upper <= coordinates[index + 1]]
    if len(cells) != 1:
        raise RuntimeError("root not isolated inside one physical grid cell")
    return {
        "parameter_axis": axis,
        "input_root_bracket": [str(bracket[0]), str(bracket[1])],
        "isolated_root_bracket": [str(lower), str(upper)],
        "isolated_endpoint_signs": [lower_sign, upper_sign],
        "parameter_grid_cell_index": cells[0],
        "strict_grid_cut_test_count": len(trace),
        "grid_cut_rows": trace,
        "grid_cut_rows_sha256": digest(trace),
    }


def outgoing_transverse_jet(
    source: Any, second_target: str, candidate: str,
    t0: Q, t1: Q, p0: Q, p1: Q,
) -> tuple[Jet, Jet, Jet]:
    t = Jet.variable(interval(t0, t1), 0)
    p = Jet.variable(interval(p0, p1), 1)
    parameter = Jet(arb(0))
    normal_x, normal_y = normal(source.chart_id.split(":")[1], t)
    radial = (arb(1) - p * p).sqrt()
    velocity_x = radial * normal_x - p * normal_y
    velocity_y = radial * normal_y + p * normal_x
    source_x, source_y = center(f"{source.source}[0,0]", parameter)
    source_radius = Q(9, 25) if source.source == "G" else Q(4, 25)
    point_x, point_y = source_x + aq(source_radius) * normal_x, source_y + aq(source_radius) * normal_y
    first_x, first_y = center(source.target_id, parameter)
    first_radius = Q(9, 25) if source.target_id[0] == "G" else Q(4, 25)
    hit1_x, hit1_y, normal1_x, normal1_y, first_p = collision(
        point_x, point_y, velocity_x, velocity_y, first_x, first_y, first_radius
    )
    radial1 = (arb(1) - first_p * first_p).sqrt()
    outgoing1_x = radial1 * normal1_x - first_p * normal1_y
    outgoing1_y = radial1 * normal1_y + first_p * normal1_x
    second_x, second_y = center(second_target, parameter)
    second_radius = Q(9, 25) if second_target[0] == "G" else Q(4, 25)
    hit2_x, hit2_y, normal2_x, normal2_y, second_p = collision(
        hit1_x, hit1_y, outgoing1_x, outgoing1_y, second_x, second_y, second_radius
    )
    radial2 = (arb(1) - second_p * second_p).sqrt()
    outgoing2_x = radial2 * normal2_x - second_p * normal2_y
    outgoing2_y = radial2 * normal2_y + second_p * normal2_x
    candidate_x, candidate_y = center(candidate, parameter)
    dx, dy = candidate_x - hit2_x, candidate_y - hit2_y
    transverse = -outgoing2_y * dx + outgoing2_x * dy
    return outgoing2_x, outgoing2_y, transverse


def reverse_labels(
    source: Any, second: str, candidate: str, axis: str, fixed: Q, bracket: tuple[Q, Q]
) -> dict[str, Any]:
    lower, upper = bracket
    if axis == "p":
        ux, uy, transverse = outgoing_transverse_jet(source, second, candidate, fixed, fixed, lower, upper)
    else:
        ux, uy, transverse = outgoing_transverse_jet(source, second, candidate, lower, upper, fixed, fixed)
    transverse_sign = strict_sign(transverse.value)
    if transverse_sign == 0:
        raise RuntimeError("tangency factor sign unresolved")
    plus_sign = strict_sign((Jet(arb(1)) + ux).value)
    minus_sign = strict_sign((Jet(arb(1)) - ux).value)
    if plus_sign == 1:
        chart, denominator = "Q_TAN_HALF_EQUALS_UY_OVER_ONE_PLUS_UX", "1+u_x"
    elif minus_sign == 1:
        chart, denominator = "R_RECIPROCAL_EQUALS_UY_OVER_ONE_MINUS_UX", "1-u_x"
    else:
        raise RuntimeError("no strict projective direction chart")
    return {
        "signed_transverse_tangency_factor": "POSITIVE_RADIUS_FACTOR" if transverse_sign > 0 else "NEGATIVE_RADIUS_FACTOR",
        "signed_transverse_sign": transverse_sign,
        "oriented_line_projective_chart": chart,
        "projective_chart_denominator": denominator,
        "projective_chart_denominator_strictly_positive": True,
    }


def classify(rows: list[dict[str, Any]], carrier: str, second: str, chart: str) -> tuple[str, str, str | None]:
    if not rows:
        return "NO_UNRESOLVED_SEED_REGISTERED", "REVERSE_TANGENT_OR_STRICT_OUTWARD_CELL_RECLASSIFICATION_REQUIRED", None
    blockers = [row for row in rows if row["carrier"] == "SECOND_OUTGOING_CHART_OR_GEOMETRY"]
    physical = [row for row in rows if row["carrier"].startswith("THIRD_CANDIDATE:")]
    if len(blockers) == len(rows):
        return "SECOND_OUTGOING_CHART_OR_GEOMETRY_BLOCKER_ONLY", "RESOLVE_SECOND_OUTGOING_CHART_OR_GEOMETRY_THEN_CONTINUE", "SECOND_OUTGOING_CHART_OR_GEOMETRY"
    same = [row for row in physical if row["carrier"] == carrier]
    if same:
        if any(row["second_selected_target_id"] == second and row["second_outgoing_chart"] == chart for row in same):
            return "SAME_CANDIDATE_SAME_SECOND_BRANCH_SEED", "CROSSWALK_TO_SAME_BRANCH_INTERVAL", None
        return "SAME_CANDIDATE_DIFFERENT_SECOND_BRANCH_SEED", "CERTIFY_SECOND_OWNER_OR_CHART_SEAM_THEN_CROSSWALK", "SECOND_OWNER_OR_OUTGOING_CHART_SEAM"
    if physical and len(physical) == len(rows):
        return "OTHER_THIRD_CANDIDATE_SEEDS_ONLY", "CERTIFY_OWNER_OR_CANDIDATE_SEAM_WITH_REVERSE_TANGENT_CROSSWALK", "THIRD_CANDIDATE_OR_OWNER_SEAM"
    return "MIXED_OR_OTHER_BLOCKER_SEEDS", "RESOLVE_MIXED_OUTWARD_CELL_TAXONOMY", "MIXED_UNRESOLVED_BLOCKER"


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    ctx.prec = precision_bits
    if file_sha256(ARC_PORTS) != ARC_PORTS_SHA256:
        raise RuntimeError("frozen arc/port byte pin mismatch")
    round82 = ledger_entries(ROUND82_LEDGER, ROUND82_LEDGER_SHA256)
    require_pin(round82, ATLAS)
    require_pin(round82, JOINS)
    round80 = ledger_entries(ROUND80_LEDGER, ROUND80_LEDGER_SHA256)
    require_pin(round80, GEOMETRY)
    arc = load_document(ARC_PORTS, "cm2.round85.rank3-registered-arc-port-census.v1")["result"]
    atlas = load_document(ATLAS, "cm2.round82.rank3-physical-patch-atlas.v1")["result"]
    joins = load_document(JOINS, "cm2.round82.rank3-cross-tube-joins.v1")["result"]
    geometry = load_document(GEOMETRY, "cm2.round80.time3-carrier-geometry.v1")["result"]
    cores = core_cert.physical_cores()
    segments = {row["registered_boundary_segment_id"]: row for row in arc["boundary_segment_rows"]}
    patches = {row["physical_patch_id"]: row for row in atlas["physical_patch_rows"]}
    components = {row["physical_root_component_id"]: row for row in joins["component_rows"]}
    component_chart = {}
    for identifier, component in components.items():
        charts = {patches[patch_id]["second_outgoing_chart"] for patch_id in component["physical_patch_ids"]}
        if len(charts) != 1:
            raise RuntimeError(f"nonunique component chart: {identifier}")
        component_chart[identifier] = next(iter(charts))
    seeds: dict[tuple[int, tuple[int, int]], list[dict[str, Any]]] = defaultdict(list)
    for seed in geometry["seed_rows"]:
        seeds[(seed["source_core_index"], grid_cell(seed["dyadic_path"]))].append(seed)
    for rows in seeds.values():
        rows.sort(key=lambda row: (row["carrier"], row["dyadic_path"]))

    frontier_rows = []
    classes: Counter[str] = Counter()
    actions: Counter[str] = Counter()
    factors: Counter[str] = Counter()
    projective_charts: Counter[str] = Counter()
    grid_tests = 0
    for port in arc["port_rows"]:
        if port["source_boundary_side"] is not None:
            continue
        source = cores[port["source_core_index"]]
        segment = segments[port["boundary_segment_id"]]
        axis, fixed_axis = port["boundary_axis"], segment["fixed_axis"]
        fixed = Q(port["fixed_coordinate"])
        isolation = isolate_grid_cell(
            source, port["second_selected_target_id"], port["third_candidate_id"], axis, fixed,
            tuple(map(Q, port["root_bracket"])), tuple(port["endpoint_signs"]),
        )
        grid_tests += isolation["strict_grid_cut_test_count"]
        fixed_indices = [i for i in range(GRID + 1) if coordinate(source, fixed_axis, i) == fixed]
        if len(fixed_indices) != 1:
            raise RuntimeError("sub-grid exposed edge")
        fixed_index = fixed_indices[0]
        parameter_index = isolation["parameter_grid_cell_index"]
        if fixed_axis == "t":
            outward = (fixed_index if segment["inside_side"] == -1 else fixed_index - 1, parameter_index)
        else:
            outward = (parameter_index, fixed_index if segment["inside_side"] == -1 else fixed_index - 1)
        if not (0 <= outward[0] < GRID and 0 <= outward[1] < GRID):
            raise RuntimeError("non-source port leaves source core")
        expected_path = dyadic_path(outward)
        outward_seeds = seeds.get((port["source_core_index"], outward), [])
        expected_box = {
            "t": [str(coordinate(source, "t", outward[0])), str(coordinate(source, "t", outward[0] + 1))],
            "p": [str(coordinate(source, "p", outward[1])), str(coordinate(source, "p", outward[1] + 1))],
        }
        if any(seed["dyadic_path"] != expected_path or seed["source_box"] != expected_box for seed in outward_seeds):
            raise RuntimeError("outward seed geometry mismatch")
        chart = component_chart[port["physical_root_component_id"]]
        carrier = f"THIRD_CANDIDATE:{port['third_candidate_id']}:unresolved_discriminant"
        classification, action, event_type = classify(outward_seeds, carrier, port["second_selected_target_id"], chart)
        labels = reverse_labels(
            source, port["second_selected_target_id"], port["third_candidate_id"], axis, fixed,
            tuple(map(Q, isolation["isolated_root_bracket"])),
        )
        classes[classification] += 1
        actions[action] += 1
        factors[labels["signed_transverse_tangency_factor"]] += 1
        projective_charts[labels["oriented_line_projective_chart"]] += 1
        evidence = [{key: seed[key] for key in (
            "dyadic_path", "source_box", "blocker", "carrier",
            "second_selected_target_id", "second_outgoing_chart",
        )} for seed in outward_seeds]
        frontier_rows.append({
            "continuation_frontier_id": "physical-s0-rank3-outward-port-frontier:" + digest({"port": port["registered_port_id"], "outward": list(outward)}),
            "registered_port_id": port["registered_port_id"],
            "physical_root_component_id": port["physical_root_component_id"],
            "source_core_index": port["source_core_index"],
            "second_selected_target_id": port["second_selected_target_id"],
            "second_outgoing_chart": chart,
            "third_candidate_id": port["third_candidate_id"],
            "boundary_axis": axis,
            "fixed_coordinate": port["fixed_coordinate"],
            "inside_side": segment["inside_side"],
            "fixed_grid_line_index": fixed_index,
            "root_grid_isolation": isolation,
            "outward_grid_cell": list(outward),
            "outward_dyadic_path": expected_path,
            "outward_cell_box": expected_box,
            "outward_seed_count": len(evidence),
            "outward_seed_rows": evidence,
            "outward_seed_rows_sha256": digest(evidence),
            "outward_cell_classification": classification,
            "typed_physical_event_frontier": event_type,
            "next_certification_action": action,
            "reverse_tangent_continuation_input": {
                "source_core_index": port["source_core_index"],
                "second_selected_target_id": port["second_selected_target_id"],
                "second_outgoing_chart": chart,
                "third_candidate_id": port["third_candidate_id"],
                "source_coordinate_box": {
                    "fixed_axis": fixed_axis,
                    "fixed_coordinate": port["fixed_coordinate"],
                    "parameter_axis": axis,
                    "parameter_interval": isolation["isolated_root_bracket"],
                },
                **labels,
            },
        })
    frontier_rows.sort(key=lambda row: row["registered_port_id"])
    expected = {
        "NO_UNRESOLVED_SEED_REGISTERED": 2696,
        "SECOND_OUTGOING_CHART_OR_GEOMETRY_BLOCKER_ONLY": 516,
    }
    if len(frontier_rows) != 3212 or dict(classes) != expected:
        raise RuntimeError(f"outward partition mismatch: {len(frontier_rows)} {dict(classes)}")
    result = {
        "fixed_parameter": "s=0",
        "precision_bits": precision_bits,
        "input_registered_port_count": arc["certified_registered_port_count"],
        "input_source_boundary_port_count": arc["source_boundary_port_count"],
        "input_non_source_registered_port_count": arc["non_source_registered_boundary_port_count"],
        "classified_non_source_port_count": len(frontier_rows),
        "outward_cell_lookup_definition": "isolate the unique root in one physical 64x64 parameter atom, cross the exposed rectilinear segment opposite its exact union inside_side, then index the complete frozen Round80 geometry seed_rows by source_core_index and grid_cell(dyadic_path)",
        "outward_cell_classification_histogram": dict(sorted(classes.items())),
        "preliminary_read_only_partition_2588_428_196_reproduced": False,
        "preliminary_partition_status": "REJECTED_BY_EXACT_FROZEN_REPLAY__REPLACED_BY_2696_NO_SEED_516_SECOND_BLOCKER_0_CANDIDATE",
        "same_candidate_same_second_branch_seed_count": classes["SAME_CANDIDATE_SAME_SECOND_BRANCH_SEED"],
        "same_candidate_different_second_branch_seed_count": classes["SAME_CANDIDATE_DIFFERENT_SECOND_BRANCH_SEED"],
        "subgrid_exposed_edge_count": 0,
        "root_on_physical_grid_line_count": 0,
        "strict_grid_cut_test_count": grid_tests,
        "reverse_tangent_action_histogram": dict(sorted(actions.items())),
        "signed_transverse_tangency_factor_histogram": dict(sorted(factors.items())),
        "oriented_line_projective_chart_histogram": dict(sorted(projective_charts.items())),
        "continuation_frontier_rows": frontier_rows,
        "continuation_frontier_rows_sha256": digest(frontier_rows),
        "strict_scope": "exact outward-cell and executable reverse-tangent input ledger for all 3212 non-source registered ports",
        "strict_nonclaims": [
            "outward seed absence is not a genuine physical termination event",
            "chart, owner and candidate seams remain continuation frontiers until separately resolved",
            "ports are not paired and 3212/2=1606 is not asserted to be a gap count",
            "registered elementary arcs are not promoted to complete physical faces",
        ],
        "upstream_pins": {
            "round85_registered_arc_port_manifest_sha256": ARC_PORTS_SHA256,
            "round82_sha256_ledger_sha256": ROUND82_LEDGER_SHA256,
            "round80_sha256_ledger_sha256": ROUND80_LEDGER_SHA256,
            "rank3_physical_patch_atlas_sha256": file_sha256(ATLAS),
            "rank3_cross_tube_joins_sha256": file_sha256(JOINS),
            "time3_carrier_geometry_sha256": file_sha256(GEOMETRY),
        },
    }
    return {"schema": "cm2.round85.rank3-outward-port-continuation-frontier.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
