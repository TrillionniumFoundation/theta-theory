#!/usr/bin/env python3
"""Rigorous reverse-billiard closure of the Round-83 common-tangent frontier."""
from __future__ import annotations

import json
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
from cm2_round79_tangency_intersection_generator import aq, digest, strict_sign
from cm2_round83_common_tangent_line_krawczyk import common_tangent_targets, outgoing_line


HERE = Path(__file__).resolve().parent
PRIMARY = HERE / "cm2-round83-common-tangent-line-krawczyk-2026-07-22.json"
CENTERED = HERE / "cm2-round83-centered-line-refinement-2026-07-22.json"
JOINS = HERE / "cm2-round82-rank3-cross-tube-joins-2026-07-21.json"
PRECISION_BITS = 512
UNIFORM_COORDINATE_SEPARATION = Q(87, 4000)
UNIFORM_CORE_COORDINATE_SEPARATION = Q(83, 4000)


def center(identifier: str) -> tuple[arb, arb]:
    obstacle = identifier[0]
    i, j = map(int, identifier[2:-1].split(","))
    offset = Q(0) if obstacle == "G" else Q(1, 2)
    return aq(Q(i) + offset), aq(Q(j) + offset)


def radius(identifier: str) -> Q:
    return Q(9, 25) if identifier[0] == "G" else Q(4, 25)


def add(left: tuple[arb, arb], right: tuple[arb, arb]) -> tuple[arb, arb]:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: tuple[arb, arb], right: tuple[arb, arb]) -> tuple[arb, arb]:
    return left[0] - right[0], left[1] - right[1]


def scale(value: arb, vector: tuple[arb, arb]) -> tuple[arb, arb]:
    return value * vector[0], value * vector[1]


def dot(left: tuple[arb, arb], right: tuple[arb, arb]) -> arb:
    return left[0] * right[0] + left[1] * right[1]


def cross(left: tuple[arb, arb], right: tuple[arb, arb]) -> arb:
    return left[0] * right[1] - left[1] * right[0]


def reflect(velocity: tuple[arb, arb], normal: tuple[arb, arb]) -> tuple[arb, arb]:
    return subtract(velocity, scale(2 * dot(velocity, normal), normal))


def line_circle_outgoing_branches(
    normal: tuple[arb, arb],
    offset: arb,
    direction: tuple[arb, arb],
    obstacle: str,
) -> tuple[list[tuple[tuple[arb, arb], tuple[arb, arb]]], bool, str | None]:
    obstacle_center = center(obstacle)
    obstacle_radius = aq(radius(obstacle))
    signed_distance = offset - dot(normal, obstacle_center)
    radicand = obstacle_radius * obstacle_radius - signed_distance * signed_distance
    radicand_sign = strict_sign(radicand)
    if radicand_sign < 0:
        return [], False, "MISS_SECOND"
    if radicand_sign == 0:
        return [], True, None
    root = radicand.sqrt()
    foot = add(obstacle_center, scale(signed_distance, normal))
    branches = []
    uncertain = False
    for sign in (-1, 1):
        hit = add(foot, scale(sign * root, direction))
        hit_normal = scale(1 / obstacle_radius, subtract(hit, obstacle_center))
        outgoing_sign = strict_sign(dot(direction, hit_normal))
        if outgoing_sign > 0:
            branches.append((hit, hit_normal))
        elif outgoing_sign == 0:
            uncertain = True
    return branches, uncertain, None


def ray_circle_incoming_branches(
    point: tuple[arb, arb],
    direction: tuple[arb, arb],
    obstacle: str,
) -> tuple[list[tuple[tuple[arb, arb], tuple[arb, arb]]], bool]:
    obstacle_center = center(obstacle)
    obstacle_radius = aq(radius(obstacle))
    delta = subtract(obstacle_center, point)
    longitudinal = dot(direction, delta)
    transverse = cross(direction, delta)
    radicand = obstacle_radius * obstacle_radius - transverse * transverse
    radicand_sign = strict_sign(radicand)
    if radicand_sign < 0:
        return [], False
    if radicand_sign == 0:
        return [], True
    root = radicand.sqrt()
    branches = []
    uncertain = False
    for sign in (-1, 1):
        flight = longitudinal + sign * root
        flight_sign = strict_sign(flight)
        if flight_sign < 0:
            continue
        if flight_sign == 0:
            uncertain = True
            continue
        hit = add(point, scale(flight, direction))
        hit_normal = scale(1 / obstacle_radius, subtract(hit, obstacle_center))
        incidence_sign = strict_sign(dot(direction, hit_normal))
        if incidence_sign < 0:
            branches.append((hit, hit_normal))
        elif incidence_sign == 0:
            uncertain = True
    return branches, uncertain


def chart_coordinate(side: str, normal: tuple[arb, arb]) -> tuple[arb | None, bool]:
    radial = normal[0] if side in ("E", "W") else normal[1]
    expected = 1 if side in ("E", "N") else -1
    radial_sign = strict_sign(radial)
    if radial_sign == expected:
        return normal[1] if side in ("E", "W") else normal[0], False
    if radial_sign == -expected:
        return None, False
    return None, True


def reverse_target(
    source: Any,
    second: str,
    target: dict[str, Any],
) -> tuple[str, list[tuple[arb, arb]], dict[str, int]]:
    normal = target["nx"], target["ny"]
    direction = target["ny"], -target["nx"]
    second_branches, uncertain, immediate = line_circle_outgoing_branches(
        normal, target["h"], direction, second
    )
    counts = {
        "physical_second_branch_count": len(second_branches),
        "physical_first_branch_count": 0,
        "physical_source_branch_count": 0,
    }
    if immediate is not None:
        return immediate, [], counts
    if uncertain:
        return "UNRESOLVED_BRANCH_SIGN", [], counts
    if not second_branches:
        return "MISS_SECOND", [], counts

    first_rows: list[tuple[tuple[arb, arb], tuple[arb, arb]]] = []
    first_uncertain = False
    for hit2, normal2 in second_branches:
        incoming2 = reflect(direction, normal2)
        reverse_direction = scale(arb(-1), incoming2)
        branches, branch_uncertain = ray_circle_incoming_branches(
            hit2, reverse_direction, source.target_id
        )
        first_uncertain = first_uncertain or branch_uncertain
        for hit1, normal1 in branches:
            first_rows.append((hit1, reflect(incoming2, normal1)))
    counts["physical_first_branch_count"] = len(first_rows)
    if first_uncertain:
        return "UNRESOLVED_BRANCH_SIGN", [], counts
    if not first_rows:
        return "MISS_FIRST", [], counts

    inverse_rows: list[tuple[arb, arb]] = []
    source_uncertain = False
    source_id = f"{source.source}[0,0]"
    side = source.chart_id.split(":")[1]
    for hit1, initial_velocity in first_rows:
        reverse_direction = scale(arb(-1), initial_velocity)
        branches, branch_uncertain = ray_circle_incoming_branches(
            hit1, reverse_direction, source_id
        )
        source_uncertain = source_uncertain or branch_uncertain
        for _hit0, normal0 in branches:
            t_value, chart_uncertain = chart_coordinate(side, normal0)
            source_uncertain = source_uncertain or chart_uncertain
            if t_value is None:
                continue
            tangent = -normal0[1], normal0[0]
            p_value = dot(initial_velocity, tangent)
            inverse_rows.append((t_value, p_value))
    counts["physical_source_branch_count"] = len(inverse_rows)
    if source_uncertain:
        return "UNRESOLVED_BRANCH_SIGN", inverse_rows, counts
    if not inverse_rows:
        return "MISS_SOURCE", [], counts
    return "INVERSE_PRESENT", inverse_rows, counts


def coordinate_separation(
    point: tuple[arb, arb],
    raw_box: list[str],
) -> tuple[str, arb] | None:
    t0, t1, p0, p1 = map(Q, raw_box)
    candidates = (
        ("t_below", aq(t0) - point[0]),
        ("t_above", point[0] - aq(t1)),
        ("p_below", aq(p0) - point[1]),
        ("p_above", point[1] - aq(p1)),
    )
    strict = [(label, gap) for label, gap in candidates if strict_sign(gap) > 0]
    if not strict:
        return None
    return max(strict, key=lambda item: float(item[1].mid()))


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    ctx.prec = precision_bits
    primary = json.loads(PRIMARY.read_text())["result"]
    centered = json.loads(CENTERED.read_text())["result"]
    joins = json.loads(JOINS.read_text())["result"]
    components = {row["physical_root_component_id"]: row for row in joins["component_rows"]}
    cores = core_cert.physical_cores()
    hard_rows = [row for row in primary["pair_rows"] if row["unresolved_initial_box_count"]]
    centered_rows = {
        (row["left_physical_root_component_id"], row["right_physical_root_component_id"]): row
        for row in centered["pair_rows"]
    }

    target_rows = []
    pair_rows = []
    status_histogram: Counter[str] = Counter()
    total_branch_counts: Counter[str] = Counter()
    inverse_count = replay_count = box_comparisons = uniformly_separated = 0
    core_comparisons = uniformly_core_separated = 0
    unit_identity_overlaps = signed_distance_identity_overlaps = 0
    unresolved_target_count = 0
    post_centered_live_pair_count = 0
    for pair_rank, pair in enumerate(hard_rows):
        left_id = pair["left_physical_root_component_id"]
        right_id = pair["right_physical_root_component_id"]
        left, right = components[left_id], components[right_id]
        source = cores[left["source_core_index"]]
        targets = common_tangent_targets(left["third_candidate_id"], right["third_candidate_id"])
        pair_histogram: Counter[str] = Counter()
        pair_inverse_count = pair_comparisons = pair_uniform = 0
        centered_row = centered_rows[(left_id, right_id)]
        if centered_row["unresolved_leaf_count"]:
            post_centered_live_pair_count += 1
        for target_rank, target in enumerate(targets):
            target_normal = target["nx"], target["ny"]
            unit_identity = dot(target_normal, target_normal).overlaps(arb(1))
            left_distance_identity = (
                dot(target_normal, center(left["third_candidate_id"])) - target["h"]
            ).overlaps(aq(target["left_signed_distance"] * radius(left["third_candidate_id"])))
            right_distance_identity = (
                dot(target_normal, center(right["third_candidate_id"])) - target["h"]
            ).overlaps(aq(target["right_signed_distance"] * radius(right["third_candidate_id"])))
            unit_identity_overlaps += int(unit_identity)
            signed_distance_identity_overlaps += int(left_distance_identity) + int(right_distance_identity)
            status, inverse_rows, branch_counts = reverse_target(
                source, left["second_selected_target_id"], target
            )
            total_branch_counts.update(branch_counts)
            row = {
                "pair_rank": pair_rank,
                "target_rank": target_rank,
                "left_signed_distance": target["left_signed_distance"],
                "right_signed_distance": target["right_signed_distance"],
                "normal_branch": target["normal_branch"],
                "unit_normal_identity_overlap": unit_identity,
                "left_signed_distance_identity_overlap": left_distance_identity,
                "right_signed_distance_identity_overlap": right_distance_identity,
                **branch_counts,
            }
            if status == "INVERSE_PRESENT":
                separated = True
                replayed = 0
                target_box_comparisons = 0
                target_uniform = 0
                target_core_uniform = 0
                inverse_enclosures = []
                for t_value, p_value in inverse_rows:
                    inverse_count += 1
                    pair_inverse_count += 1
                    core_comparisons += 1
                    core_box = [str(source.t0), str(source.t1), str(source.p0), str(source.p1)]
                    core_separation = coordinate_separation((t_value, p_value), core_box)
                    core_separation_certified = (
                        core_separation is not None
                        and bool(core_separation[1] > aq(UNIFORM_CORE_COORDINATE_SEPARATION))
                    )
                    if core_separation_certified:
                        uniformly_core_separated += 1
                        target_core_uniform += 1
                    else:
                        separated = False
                    replay = outgoing_line(
                        source, left["second_selected_target_id"], t_value, p_value
                    )
                    if all(replay[index].value.overlaps(target[key]) for index, key in enumerate(("nx", "ny", "h"))):
                        replay_count += 1
                        replayed += 1
                    else:
                        separated = False
                    inverse_enclosures.append([str(t_value), str(p_value)])
                    for raw_box in pair["unresolved_initial_boxes"]:
                        box_comparisons += 1
                        pair_comparisons += 1
                        target_box_comparisons += 1
                        separation = coordinate_separation((t_value, p_value), raw_box)
                        if separation is None:
                            separated = False
                            continue
                        if bool(separation[1] > aq(UNIFORM_COORDINATE_SEPARATION)):
                            uniformly_separated += 1
                            pair_uniform += 1
                            target_uniform += 1
                row.update({
                    "inverse_enclosures": inverse_enclosures,
                    "source_core_uniform_separation_count": target_core_uniform,
                    "forward_replay_overlap_count": replayed,
                    "hard_box_comparison_count": target_box_comparisons,
                    "uniformly_separated_box_comparison_count": target_uniform,
                })
                status = "INVERSE_STRICTLY_SEPARATED" if separated else "UNRESOLVED_INVERSE_OVERLAP"
            row["status"] = status
            target_rows.append(row)
            status_histogram[status] += 1
            pair_histogram[status] += 1
            if status.startswith("UNRESOLVED"):
                unresolved_target_count += 1
        pair_rows.append({
            "pair_rank": pair_rank,
            "left_physical_root_component_id": left_id,
            "right_physical_root_component_id": right_id,
            "input_hard_box_count": pair["unresolved_initial_box_count"],
            "post_centered_unresolved_leaf_count": centered_row["unresolved_leaf_count"],
            "target_status_histogram": dict(sorted(pair_histogram.items())),
            "inverse_count": pair_inverse_count,
            "inverse_box_comparison_count": pair_comparisons,
            "uniformly_separated_box_comparison_count": pair_uniform,
        })

    hard_box_count = sum(row["unresolved_initial_box_count"] for row in hard_rows)
    result = {
        "fixed_parameter": "s=0",
        "precision_bits": precision_bits,
        "input_hard_component_pair_count": len(hard_rows),
        "post_centered_live_component_pair_count": post_centered_live_pair_count,
        "post_centered_closed_component_pair_count": len(hard_rows) - post_centered_live_pair_count,
        "input_hard_box_count": hard_box_count,
        "oriented_common_tangent_target_count": len(target_rows),
        "unit_normal_identity_overlap_count": unit_identity_overlaps,
        "candidate_signed_distance_identity_overlap_count": signed_distance_identity_overlaps,
        "target_status_histogram": dict(sorted(status_histogram.items())),
        "physical_reverse_branch_totals": dict(sorted(total_branch_counts.items())),
        "inverse_enclosure_count": inverse_count,
        "forward_replay_overlap_count": replay_count,
        "inverse_hard_box_comparison_count": box_comparisons,
        "inverse_source_core_comparison_count": core_comparisons,
        "uniform_core_coordinate_separation_lower": str(UNIFORM_CORE_COORDINATE_SEPARATION),
        "uniformly_source_core_separated_inverse_count": uniformly_core_separated,
        "uniform_coordinate_separation_lower": str(UNIFORM_COORDINATE_SEPARATION),
        "uniformly_separated_box_comparison_count": uniformly_separated,
        "unresolved_target_count": unresolved_target_count,
        "certified_disjoint_hard_box_count": hard_box_count if unresolved_target_count == 0 else 0,
        "remaining_hard_box_count": 0 if unresolved_target_count == 0 else hard_box_count,
        "pair_rows": pair_rows,
        "pair_rows_sha256": digest(pair_rows),
        "target_rows": target_rows,
        "target_rows_sha256": digest(target_rows),
        "strict_scope": "finite reverse-billiard preimage certificate for all 614 Round-83 hard positive-area boxes",
        "strict_nonclaims": [
            "reverse-line closure of the overlap boxes does not itself construct rank-three return-face RN rows",
            "completion of the fixed-s=0 intersection atlas is not an all-depth Gate-4 stable/material crosswalk",
            "finite rank-three intersection closure is not a uniform physical rank-transition tail contraction",
        ],
    }
    expected_histogram = {
        "INVERSE_STRICTLY_SEPARATED": 42,
        "MISS_FIRST": 114,
        "MISS_SECOND": 176,
        "MISS_SOURCE": 4,
    }
    if len(hard_rows) != 42 or post_centered_live_pair_count != 40:
        raise RuntimeError("hard-pair accounting")
    if hard_box_count != 614 or len(target_rows) != 336:
        raise RuntimeError("hard-box/target accounting")
    if unit_identity_overlaps != 336 or signed_distance_identity_overlaps != 672:
        raise RuntimeError("common-tangent target identities")
    if dict(status_histogram) != expected_histogram:
        raise RuntimeError(f"unexpected reverse status histogram: {dict(status_histogram)}")
    if inverse_count != 42 or replay_count != 42:
        raise RuntimeError("reverse/forward replay accounting")
    if core_comparisons != 42 or uniformly_core_separated != 42:
        raise RuntimeError("uniform inverse/source-core separation failed")
    if box_comparisons != 614 or uniformly_separated != 614:
        raise RuntimeError("uniform inverse/box separation failed")
    if unresolved_target_count != 0:
        raise RuntimeError("reverse frontier remains unresolved")
    return {"schema": "cm2.round84.reverse-common-tangent-closure.v1", "result": result, "result_sha256": digest(result)}


def main() -> int:
    json.dump(build(), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
