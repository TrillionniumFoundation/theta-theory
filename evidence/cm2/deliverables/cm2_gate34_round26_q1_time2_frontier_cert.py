#!/usr/bin/env python3
"""Round-26 strict propagation of the frozen Q1-inner atoms to time two.

The round-25 adaptive cover contains 2,868 whole source boxes whose time-one
images lie strictly outside the complete 24-core union.  This append-only
certificate starts from exactly those boxes.  It recomputes the first
collision with 384-bit Arb, reconstructs the physical outgoing state, reduces
the next-collision search by the complete translated eight-chart candidate
table, and proves a unique next owner before testing the time-two image
against every core.

Unresolved boxes are bisected in their original (t,p,s) coordinates through
total dyadic depth 16.  Admission is whole-box and strict.  Consequently a
RETURN_AT_2_INNER leaf is a genuine first-return-at-two cylinder and a
SURVIVE_THROUGH_2_INNER leaf is a genuine Q2-inner cylinder.  The remaining
outer boxes are retained explicitly; this file does not claim a complete
R2/Q2 partition or an arbitrary-n return construction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

RESULT_SCHEMA = "cm2.gate34.round26-q1-time2-frontier.v1"
MANIFEST_SCHEMA = "cm2.gate34.round26-q1-time2-frontier.manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-round26-q1-time2-frontier-manifest-2026-07-18.json"
)
MAX_TOTAL_BINARY_DEPTH = 16

DEPENDENCIES = {
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate3_candidate_first_hit_cert.py": (
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"
    ),
    "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json": (
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4"
    ),
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py": (
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24"
    ),
    "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json": (
        "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0"
    ),
}

TARGET_PATTERN = re.compile(r"([GW])\[(-?\d+),(-?\d+)\]")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_step1_manifest() -> dict[str, Any]:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency: {name}")
        require(not path.is_symlink(), f"symlink dependency: {name}")
        require(sha256_path(path) == expected, f"dependency mismatch: {name}")
    manifest = json.loads(
        (
            HERE
            / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
        ).read_text(encoding="utf-8")
    )
    result = manifest["result"]
    require(
        result["adaptive_full_core_step1_registry"]["adaptive_leaf_count"]
        == 33960,
        "step1 leaf count",
    )
    require(
        result["adaptive_full_core_step1_registry"]["classification_histogram"]
        ["SURVIVE_THROUGH_1_INNER"]
        == 2868,
        "frozen Q1 count",
    )
    return manifest


def parse_target(target_id: str) -> tuple[str, int, int]:
    match = TARGET_PATTERN.fullmatch(target_id)
    require(match is not None, f"bad target id: {target_id}")
    assert match is not None
    return match.group(1), int(match.group(2)), int(match.group(3))


def target_id(obstacle: str, ix: int, iy: int) -> str:
    return f"{obstacle}[{ix},{iy}]"


def target_center(target: str, s: arb) -> tuple[arb, arb]:
    obstacle, ix, iy = parse_target(target)
    if obstacle == "G":
        return arb(ix), arb(iy)
    return (
        arb(ix) + step1.arbq(Q(1, 2)) + s,
        arb(iy) + step1.arbq(Q(1, 2)),
    )


@lru_cache(maxsize=8)
def relative_candidate_ids(source: str, cell: str) -> tuple[str, ...]:
    return tuple(first_hit.candidate_ids(f"{source}:{cell}"))


def translated_candidate_ids(current_target: str, cell: str) -> Iterable[str]:
    source, ix, iy = parse_target(current_target)
    for relative_id in relative_candidate_ids(source, cell):
        obstacle, jx, jy = parse_target(relative_id)
        yield target_id(obstacle, ix + jx, iy + jy)


def strict_chart(normal_x: arb, normal_y: arb) -> str | None:
    abs_x, abs_y = abs(normal_x), abs(normal_y)
    if bool(abs_x > abs_y):
        if bool(normal_x > 0):
            return "E"
        if bool(normal_x < 0):
            return "W"
    if bool(abs_y > abs_x):
        if bool(normal_y > 0):
            return "N"
        if bool(normal_y < 0):
            return "S"
    return None


def first_collision_outgoing(
    atom: step1.Atom,
) -> dict[str, arb | str] | None:
    qx, qy, ux, uy, s = first_hit.phase_geometry(atom.phase_box)
    ax, ay = target_center(atom.source_core.target_id, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = step1.arbq(first_hit.RADIUS[atom.source_core.target_id[0]])
    discriminant = radius * radius - transverse * transverse
    if not bool(discriminant > 0):
        return None
    radical = discriminant.sqrt()
    root = ell - radical
    if not bool(root > 0) or not bool(root < step1.arbq(first_hit.TAU_MAX)):
        return None
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    p = transverse / radius
    radial_square = 1 - p * p
    if not bool(radial_square > 0):
        return None
    radial = radial_square.sqrt()
    outgoing_x = radial * normal_x - p * normal_y
    outgoing_y = radial * normal_y + p * normal_x
    contact_x = ax + radius * normal_x
    contact_y = ay + radius * normal_y
    chart = strict_chart(normal_x, normal_y)
    if chart is None:
        return None
    return {
        "contact_x": contact_x,
        "contact_y": contact_y,
        "outgoing_x": outgoing_x,
        "outgoing_y": outgoing_y,
        "s": s,
        "chart": chart,
        "normal_x": normal_x,
        "normal_y": normal_y,
        "p": p,
        "root": root,
    }


def candidate_root(
    qx: arb,
    qy: arb,
    ux: arb,
    uy: arb,
    s: arb,
    candidate_id: str,
) -> dict[str, Any]:
    ax, ay = target_center(candidate_id, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = step1.arbq(first_hit.RADIUS[candidate_id[0]])
    discriminant = radius * radius - transverse * transverse
    if bool(discriminant < 0):
        return {"classification": "no_real_intersection"}
    if not bool(discriminant > 0):
        return {"classification": "unresolved_discriminant"}
    radical = discriminant.sqrt()
    near = ell - radical
    far = ell + radical
    if bool(far < 0):
        return {"classification": "intersection_strictly_behind"}
    if not bool(near > 0):
        return {"classification": "unresolved_root_sign"}
    return {
        "classification": "strict_future_near_root",
        "near": near,
        "radical": radical,
        "transverse": transverse,
        "radius": radius,
    }


def strict_second_owner(
    atom: step1.Atom,
) -> tuple[dict[str, Any] | None, str]:
    state = first_collision_outgoing(atom)
    if state is None:
        return None, "unresolved_time1_outgoing_chart_or_geometry"
    qx = state["contact_x"]
    qy = state["contact_y"]
    ux = state["outgoing_x"]
    uy = state["outgoing_y"]
    s = state["s"]
    chart = state["chart"]
    assert isinstance(qx, arb) and isinstance(qy, arb)
    assert isinstance(ux, arb) and isinstance(uy, arb) and isinstance(s, arb)
    assert isinstance(chart, str)
    rows: list[tuple[str, dict[str, Any]]] = []
    missed = 0
    behind = 0
    for candidate_id in translated_candidate_ids(atom.source_core.target_id, chart):
        row = candidate_root(qx, qy, ux, uy, s, candidate_id)
        kind = row["classification"]
        if kind == "no_real_intersection":
            missed += 1
        elif kind == "intersection_strictly_behind":
            behind += 1
        elif kind == "strict_future_near_root":
            rows.append((candidate_id, row))
        else:
            return None, f"unresolved_competitor:{kind}"
    winners: list[tuple[str, dict[str, Any]]] = []
    for candidate_id, row in rows:
        near = row["near"]
        assert isinstance(near, arb)
        if all(
            candidate_id == other_id
            or bool(near < other_row["near"])
            for other_id, other_row in rows
        ):
            winners.append((candidate_id, row))
    if len(winners) != 1:
        return None, "unresolved_strict_root_order"
    selected_id, selected = winners[0]
    root = selected["near"]
    if not bool(root < step1.arbq(first_hit.TAU_MAX)):
        return None, "selected_root_not_strictly_below_tau_max"
    radical = selected["radical"]
    transverse = selected["transverse"]
    radius = selected["radius"]
    assert all(isinstance(value, arb) for value in (root, radical, transverse, radius))
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    p = transverse / radius
    return {
        "time1_chart_id": f"{atom.source_core.target_id[0]}:{chart}",
        "selected_target_id": selected_id,
        "selected_root": root,
        "normal_x": normal_x,
        "normal_y": normal_y,
        "p": p,
        "retained_candidate_count": missed + behind + len(rows),
        "missed_candidate_count": missed,
        "behind_candidate_count": behind,
        "strict_future_candidate_count": len(rows),
    }, "strict_unique_second_collision_owner"


def classify_time2(
    atom: step1.Atom,
    cores: tuple[core_cert.Core, ...],
) -> dict[str, Any]:
    owner, owner_status = strict_second_owner(atom)
    if owner is None:
        return {
            "classification": "UNRESOLVED_TIME2_OUTER",
            "owner_status": owner_status,
            "selected_target_id": None,
            "destination_core_id": None,
            "witness_digest": canonical_digest({"owner_status": owner_status}),
        }
    normal_x = owner["normal_x"]
    normal_y = owner["normal_y"]
    p = owner["p"]
    assert isinstance(normal_x, arb) and isinstance(normal_y, arb)
    assert isinstance(p, arb)
    inside: list[str] = []
    unresolved: list[str] = []
    witness_rows: list[dict[str, Any]] = []
    for destination in cores:
        if destination.source != owner["selected_target_id"][0]:
            continue
        identifier = step1.core_id(destination)
        cell = destination.chart_id.split(":")[1]
        t, inside_chart_tests, outside_chart_tests = step1.chart_tests(
            cell, normal_x, normal_y
        )
        inside_tests = inside_chart_tests + [
            ("t_gt_t0", bool(t > step1.arbq(destination.t0))),
            ("t_lt_t1", bool(t < step1.arbq(destination.t1))),
            ("p_gt_p0", bool(p > step1.arbq(destination.p0))),
            ("p_lt_p1", bool(p < step1.arbq(destination.p1))),
        ]
        if all(value for _name, value in inside_tests):
            inside.append(identifier)
            witness_rows.append({"core_id": identifier, "kind": "strict_inside"})
            continue
        separators = outside_chart_tests + [
            ("t_lt_t0", bool(t < step1.arbq(destination.t0))),
            ("t_gt_t1", bool(t > step1.arbq(destination.t1))),
            ("p_lt_p0", bool(p < step1.arbq(destination.p0))),
            ("p_gt_p1", bool(p > step1.arbq(destination.p1))),
        ]
        separator = next((name for name, value in separators if value), None)
        if separator is None:
            unresolved.append(identifier)
            witness_rows.append({"core_id": identifier, "kind": "unresolved"})
        else:
            witness_rows.append({
                "core_id": identifier,
                "kind": "strictly_excluded",
                "first_separator": separator,
            })
    if unresolved or len(inside) > 1:
        classification = "UNRESOLVED_TIME2_OUTER"
        destination_id = None
    elif len(inside) == 1:
        classification = "RETURN_AT_2_INNER"
        destination_id = inside[0]
    else:
        classification = "SURVIVE_THROUGH_2_INNER"
        destination_id = None
    public_owner = {
        key: (str(value) if isinstance(value, arb) else value)
        for key, value in owner.items()
        if key not in {"normal_x", "normal_y", "p"}
    }
    witness_payload = {
        "owner": public_owner,
        "normal_x": str(normal_x),
        "normal_y": str(normal_y),
        "p": str(p),
        "core_tests": witness_rows,
    }
    return {
        "classification": classification,
        "owner_status": owner_status,
        "selected_target_id": owner["selected_target_id"],
        "destination_core_id": destination_id,
        "witness_digest": canonical_digest(witness_payload),
    }


def atom_from_step1_row(
    row: dict[str, Any], cores: tuple[core_cert.Core, ...]
) -> step1.Atom:
    box = row["source_box"]
    index = row["source_core_index"]
    return step1.Atom(
        index,
        cores[index],
        Q(box["t"][0]),
        Q(box["t"][1]),
        Q(box["p"][0]),
        Q(box["p"][1]),
        Q(box["s"][0]),
        Q(box["s"][1]),
        row["dyadic_path"],
    )


def compact_row(
    parent_row: dict[str, Any],
    atom: step1.Atom,
    classification: dict[str, Any],
) -> dict[str, Any]:
    suffix = atom.path[len(parent_row["dyadic_path"]):]
    mass = step1.base_mass(atom)
    payload = {
        "Q1_parent_atom_id": parent_row["atom_id"],
        "refinement_suffix": suffix,
        "source_box": {
            "t": [str(atom.t0), str(atom.t1)],
            "p": [str(atom.p0), str(atom.p1)],
            "s": [str(atom.s0), str(atom.s1)],
        },
    }
    return {
        "time2_atom_id": "full-core-time2:" + canonical_digest(payload),
        **payload,
        "source_core_index": atom.source_core_index,
        "total_depth": atom.depth,
        "classification": classification["classification"],
        "owner_status": classification["owner_status"],
        "selected_second_target_id": classification["selected_target_id"],
        "destination_core_id": classification["destination_core_id"],
        "whole_box_Arb_witness_sha256": classification["witness_digest"],
        "parameter_averaged_unnormalized_base_mass": str(mass),
        "time1_strict_outside_all_24_cores_inherited_from_Q1_parent": True,
        "first_return_clock_starts_at_source_core_time0": True,
        "canonical_invariant_area_Jacobian_per_regular_collision": "1",
    }


def adaptive_time2_rows(
    q1_rows: list[dict[str, Any]],
    cores: tuple[core_cert.Core, ...],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for parent_row in q1_rows:
        root = atom_from_step1_row(parent_row, cores)
        stack = [root]
        while stack:
            atom = stack.pop()
            classification = classify_time2(atom, cores)
            if (
                classification["classification"] == "UNRESOLVED_TIME2_OUTER"
                and atom.depth < MAX_TOTAL_BINARY_DEPTH
            ):
                left, right = step1.split_atom(atom)
                stack.append(right)
                stack.append(left)
                continue
            result.append(compact_row(parent_row, atom, classification))
    result.sort(key=lambda row: (
        row["Q1_parent_atom_id"], row["refinement_suffix"]
    ))
    require(
        len({row["time2_atom_id"] for row in result}) == len(result),
        "duplicate time2 atom id",
    )
    return result


def verify_prefix_and_mass(
    q1_rows: list[dict[str, Any]], rows: list[dict[str, Any]]
) -> None:
    children: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        children.setdefault(row["Q1_parent_atom_id"], []).append(row)
    require(len(children) == len(q1_rows), "Q1 parent coverage")
    for parent in q1_rows:
        family = children[parent["atom_id"]]
        paths = sorted(row["refinement_suffix"] for row in family)
        require(
            not any(
                right.startswith(left)
                for left, right in zip(paths, paths[1:])
            ),
            f"non-prefix-free time2 family: {parent['atom_id']}",
        )
        observed = sum(
            Q(row["parameter_averaged_unnormalized_base_mass"])
            for row in family
        )
        expected = Q(parent["parameter_averaged_unnormalized_base_mass"])
        require(observed == expected, f"time2 family mass: {parent['atom_id']}")


def build_result() -> dict[str, Any]:
    manifest = load_step1_manifest()
    cores = core_cert.physical_cores()
    require(len(cores) == 24, "core count")
    q1_rows = [
        row
        for row in manifest["result"]["adaptive_full_core_step1_raw_leaf_rows"]
        if row["classification"] == "SURVIVE_THROUGH_1_INNER"
    ]
    require(len(q1_rows) == 2868, "Q1 row count")
    rows = adaptive_time2_rows(q1_rows, cores)
    verify_prefix_and_mass(q1_rows, rows)
    histogram = Counter(row["classification"] for row in rows)
    depth_histogram = Counter(row["total_depth"] for row in rows)
    owner_status_histogram = Counter(row["owner_status"] for row in rows)
    mass_by_kind = {
        kind: sum(
            Q(row["parameter_averaged_unnormalized_base_mass"])
            for row in rows
            if row["classification"] == kind
        )
        for kind in (
            "RETURN_AT_2_INNER",
            "SURVIVE_THROUGH_2_INNER",
            "UNRESOLVED_TIME2_OUTER",
        )
    }
    q1_mass = sum(
        Q(row["parameter_averaged_unnormalized_base_mass"])
        for row in q1_rows
    )
    require(sum(mass_by_kind.values()) == q1_mass, "global Q1 mass conservation")
    return_rows = [row for row in rows if row["classification"] == "RETURN_AT_2_INNER"]
    survivor_rows = [
        row for row in rows if row["classification"] == "SURVIVE_THROUGH_2_INNER"
    ]
    require(len(survivor_rows) > 0, "no Q2 inner atom")
    result = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "admission_engine": "python-flint Arb",
            "precision_bits": 384,
            "clock": "source_core_time0_then_time1_Q1_then_time2",
            "candidate_search": "complete_translated_eight_chart_retained_table",
        },
        "Q1_time2_adaptive_registry": {
            "frozen_Q1_parent_atom_count": len(q1_rows),
            "maximum_total_binary_depth": MAX_TOTAL_BINARY_DEPTH,
            "time2_leaf_count": len(rows),
            "classification_histogram": dict(sorted(histogram.items())),
            "depth_histogram": {
                str(depth): count for depth, count in sorted(depth_histogram.items())
            },
            "owner_status_histogram": dict(sorted(owner_status_histogram.items())),
            "strict_R2_inner_atom_count": len(return_rows),
            "strict_Q2_inner_atom_count": len(survivor_rows),
            "time2_leaf_rows_sha256": canonical_digest(rows),
            "time2_atom_ids_sha256": canonical_digest(
                [row["time2_atom_id"] for row in rows]
            ),
            "Q1_parent_atom_ids_sha256": canonical_digest(
                [row["atom_id"] for row in q1_rows]
            ),
            "representative_rows": (
                return_rows[:1] + survivor_rows[:1]
                + [row for row in rows if row["classification"] == "UNRESOLVED_TIME2_OUTER"][:1]
            ),
        },
        "Q1_time2_mass_frontier": {
            "parameter_averaged_Q1_inner_base_mass": str(q1_mass),
            "R2_inner_base_mass": str(mass_by_kind["RETURN_AT_2_INNER"]),
            "Q2_inner_base_mass": str(mass_by_kind["SURVIVE_THROUGH_2_INNER"]),
            "time2_unresolved_outer_base_mass": str(
                mass_by_kind["UNRESOLVED_TIME2_OUTER"]
            ),
            "mass_identity_R2_plus_Q2_plus_unresolved_equals_Q1": True,
            "every_R2_inner_leaf_is_first_return_at_exact_time2": True,
            "every_Q2_inner_leaf_avoids_C24_at_times1_and2": True,
        },
        "strict_nonpromotion": {
            "complete_R2_Q2_partition": "NOT_CERTIFIED",
            "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
            "q_weighted_return_tail": "NOT_CERTIFIED",
            "induced_strong_Lasota_Yorke": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    payload = dict(result)
    result["internal_replay_digest"] = canonical_digest(payload)
    return result


def verdict(result: dict[str, Any]) -> dict[str, Any]:
    registry = result["Q1_time2_adaptive_registry"]
    return {
        "strict_R2_inner_atoms": f"CERTIFIED_{registry['strict_R2_inner_atom_count']}",
        "strict_Q2_inner_atoms": f"CERTIFIED_{registry['strict_Q2_inner_atom_count']}",
        "Q1_time2_mass_conservation": "CERTIFIED",
        "complete_R2_Q2_partition": "NOT_CERTIFIED",
        "arbitrary_n_Rn_Qn_partition": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def write_manifest(path: Path, verifier_path: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": verdict(result),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_round26_q1_time2_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    registry = result["Q1_time2_adaptive_registry"]
    mass = result["Q1_time2_mass_frontier"]
    print("Q1_TIME2_ADAPTIVE_FRONTIER: CERTIFIED")
    print(f"LEAVES: {registry['time2_leaf_count']}")
    print(f"HISTOGRAM: {registry['classification_histogram']}")
    print(f"R2_INNER_BASE_MASS: {mass['R2_inner_base_mass']}")
    print(f"Q2_INNER_BASE_MASS: {mass['Q2_inner_base_mass']}")
    print(f"UNRESOLVED_BASE_MASS: {mass['time2_unresolved_outer_base_mass']}")
    print("COMPLETE_R2_Q2_PARTITION: NOT_CERTIFIED")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
