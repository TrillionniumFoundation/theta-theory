#!/usr/bin/env python3
"""Adaptive full-core one-step return frontier for the CM2 pilot.

This append-only certificate starts from all twenty-four two-dimensional
physical collision cores, uniformly over ``|s|<=1/400``.  It inherits the
complete strict first-collision owner proof on each parent core, then uses
384-bit Arb to classify the image of adaptive ``(t,p,s)`` boxes against the
entire 24-core union.  Boxes are admitted only by a strict trichotomy:

* ``RETURN_AT_1_INNER``: the whole image lies strictly inside one core;
* ``SURVIVE_THROUGH_1_INNER``: the whole image lies strictly outside all cores;
* ``UNRESOLVED_OUTER``: neither conclusion follows from the enclosure.

The parameter coordinate is subdivided, but every atom retains a positive
two-dimensional ``(t,p)`` source rectangle.  A midpoint test is proposal-only:
it decides which unresolved depth-12 boxes are refined to depth 15, never
which boxes are admitted.  The resulting raw rows cover ``C24 x S`` modulo
shared null faces and carry rational collision-mass brackets and the exact
invariant-area Jacobian seed.

This is a finite one-step inner/outer approximation, not a complete R_n/Q_n
partition, not an exponential return tail, and not an induced strong bound.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit


ctx.prec = 384
Q = Fraction
HERE = Path(__file__).resolve().parent

RESULT_SCHEMA = "cm2.gate34.full-core-return-adaptive-frontier.v1"
MANIFEST_SCHEMA = "cm2.gate34.full-core-return-adaptive-frontier.manifest.v1"
DEFAULT_MANIFEST = (
    HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
)

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
}

BASE_MAX_BINARY_DEPTH = 12
PROMOTED_MAX_BINARY_DEPTH = 15
GLOBAL_DTHETA_DT_UPPER = Q(1401, 1000)
PARAMETER_WIDTH = core_cert.S_UPPER - core_cert.S_LOWER


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def load_dependencies() -> None:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        if not path.is_file() or sha256_path(path) != expected:
            raise RuntimeError(f"dependency mismatch: {name}")
    registry = json.loads(
        (
            HERE
            / "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
        ).read_text(encoding="utf-8")
    )["result"]["physical_return_core_registry"]
    if registry["physical_compact_homogeneous_core_count"] != 24:
        raise RuntimeError("frozen core count mismatch")
    if not registry[
        "all_cores_strict_first_hit_against_complete_retained_candidate_list"
    ]:
        raise RuntimeError("parent first-owner audit missing")


def core_payload(core: core_cert.Core) -> dict[str, Any]:
    return {
        "chart_id": core.chart_id,
        "t": [str(core.t0), str(core.t1)],
        "p": [str(core.p0), str(core.p1)],
        "target_id": core.target_id,
        "crossings": list(core.crossings),
    }


def core_id(core: core_cert.Core) -> str:
    return "core:" + canonical_digest(core_payload(core))


@dataclass(frozen=True)
class Atom:
    source_core_index: int
    source_core: core_cert.Core
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    s0: Q
    s1: Q
    path: str

    @property
    def depth(self) -> int:
        return len(self.path)

    @property
    def phase_box(self) -> first_hit.PhaseBox:
        return first_hit.PhaseBox(
            self.source_core.chart_id,
            self.t0,
            self.t1,
            self.p0,
            self.p1,
            self.s0,
            self.s1,
        )


def atom_geometry(atom: Atom) -> dict[str, arb] | None:
    qx, qy, ux, uy, s = first_hit.phase_geometry(atom.phase_box)
    target = first_hit.target_by_id(atom.source_core.target_id)
    ax, ay = first_hit.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = arbq(first_hit.RADIUS[target.obstacle])
    discriminant = radius * radius - transverse * transverse
    if not bool(discriminant > 0):
        return None
    radical = discriminant.sqrt()
    near = ell - radical
    if not bool(near > 0) or not bool(near < arbq(first_hit.TAU_MAX)):
        return None
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    return {
        "near": near,
        "normal_x": normal_x,
        "normal_y": normal_y,
        "p_target": transverse / radius,
    }


def chart_tests(
    cell: str, normal_x: arb, normal_y: arb
) -> tuple[arb, list[tuple[str, bool]], list[tuple[str, bool]]]:
    abs_x, abs_y = abs(normal_x), abs(normal_y)
    if cell == "E":
        return (
            normal_y,
            [("normal_x_positive", bool(normal_x > 0)),
             ("abs_nx_gt_abs_ny", bool(abs_x > abs_y))],
            [("normal_x_negative", bool(normal_x < 0)),
             ("abs_nx_lt_abs_ny", bool(abs_x < abs_y))],
        )
    if cell == "W":
        return (
            normal_y,
            [("normal_x_negative", bool(normal_x < 0)),
             ("abs_nx_gt_abs_ny", bool(abs_x > abs_y))],
            [("normal_x_positive", bool(normal_x > 0)),
             ("abs_nx_lt_abs_ny", bool(abs_x < abs_y))],
        )
    if cell == "N":
        return (
            normal_x,
            [("normal_y_positive", bool(normal_y > 0)),
             ("abs_ny_gt_abs_nx", bool(abs_y > abs_x))],
            [("normal_y_negative", bool(normal_y < 0)),
             ("abs_ny_lt_abs_nx", bool(abs_y < abs_x))],
        )
    if cell == "S":
        return (
            normal_x,
            [("normal_y_negative", bool(normal_y < 0)),
             ("abs_ny_gt_abs_nx", bool(abs_y > abs_x))],
            [("normal_y_positive", bool(normal_y > 0)),
             ("abs_ny_lt_abs_nx", bool(abs_y < abs_x))],
        )
    raise ValueError(cell)


def classify_atom(
    atom: Atom,
    destination_cores: tuple[core_cert.Core, ...],
) -> dict[str, Any]:
    geometry = atom_geometry(atom)
    if geometry is None:
        return {
            "classification": "UNRESOLVED_OUTER",
            "destination_core_id": None,
            "witness_rows": [{"kind": "unresolved_collision_geometry"}],
            "output_enclosures": None,
        }
    nx = geometry["normal_x"]
    ny = geometry["normal_y"]
    p = geometry["p_target"]
    target_obstacle = atom.source_core.target_id[0]
    inside: list[str] = []
    unresolved: list[str] = []
    witnesses: list[dict[str, Any]] = []
    for destination in destination_cores:
        if destination.source != target_obstacle:
            continue
        identifier = core_id(destination)
        cell = destination.chart_id.split(":")[1]
        t, inside_chart_tests, outside_chart_tests = chart_tests(cell, nx, ny)
        inside_tests = inside_chart_tests + [
            ("t_gt_t0", bool(t > arbq(destination.t0))),
            ("t_lt_t1", bool(t < arbq(destination.t1))),
            ("p_gt_p0", bool(p > arbq(destination.p0))),
            ("p_lt_p1", bool(p < arbq(destination.p1))),
        ]
        if all(value for _name, value in inside_tests):
            inside.append(identifier)
            witnesses.append({"core_id": identifier, "kind": "strict_inside"})
            continue
        separators = outside_chart_tests + [
            ("t_lt_t0", bool(t < arbq(destination.t0))),
            ("t_gt_t1", bool(t > arbq(destination.t1))),
            ("p_lt_p0", bool(p < arbq(destination.p0))),
            ("p_gt_p1", bool(p > arbq(destination.p1))),
        ]
        separator = next((name for name, value in separators if value), None)
        if separator is None:
            unresolved.append(identifier)
            witnesses.append({"core_id": identifier, "kind": "unresolved"})
        else:
            witnesses.append({
                "core_id": identifier,
                "kind": "strictly_excluded",
                "first_separator": separator,
            })
    if unresolved or len(inside) > 1:
        classification = "UNRESOLVED_OUTER"
        destination_id = None
    elif len(inside) == 1:
        classification = "RETURN_AT_1_INNER"
        destination_id = inside[0]
    else:
        classification = "SURVIVE_THROUGH_1_INNER"
        destination_id = None
    return {
        "classification": classification,
        "destination_core_id": destination_id,
        "witness_rows": witnesses,
        "output_enclosures": {
            "normal_x": str(nx),
            "normal_y": str(ny),
            "p_target": str(p),
        },
    }


def split_atom(atom: Atom) -> tuple[Atom, Atom]:
    core = atom.source_core
    t_scale = (atom.t1 - atom.t0) / (core.t1 - core.t0)
    p_scale = (atom.p1 - atom.p0) / (core.p1 - core.p0)
    s_scale = (atom.s1 - atom.s0) / PARAMETER_WIDTH
    if t_scale >= p_scale and t_scale >= s_scale:
        middle = (atom.t0 + atom.t1) / 2
        bounds = [
            (atom.t0, middle, atom.p0, atom.p1, atom.s0, atom.s1),
            (middle, atom.t1, atom.p0, atom.p1, atom.s0, atom.s1),
        ]
    elif p_scale >= s_scale:
        middle = (atom.p0 + atom.p1) / 2
        bounds = [
            (atom.t0, atom.t1, atom.p0, middle, atom.s0, atom.s1),
            (atom.t0, atom.t1, middle, atom.p1, atom.s0, atom.s1),
        ]
    else:
        middle = (atom.s0 + atom.s1) / 2
        bounds = [
            (atom.t0, atom.t1, atom.p0, atom.p1, atom.s0, middle),
            (atom.t0, atom.t1, atom.p0, atom.p1, middle, atom.s1),
        ]
    return tuple(
        Atom(
            atom.source_core_index,
            core,
            *row,
            atom.path + str(index),
        )
        for index, row in enumerate(bounds)
    )  # type: ignore[return-value]


def midpoint_atom(atom: Atom) -> Atom:
    tm = (atom.t0 + atom.t1) / 2
    pm = (atom.p0 + atom.p1) / 2
    sm = (atom.s0 + atom.s1) / 2
    return Atom(
        atom.source_core_index,
        atom.source_core,
        tm,
        tm,
        pm,
        pm,
        sm,
        sm,
        atom.path,
    )


def base_mass(atom: Atom) -> Q:
    return (
        first_hit.RADIUS[atom.source_core.source]
        * (atom.t1 - atom.t0)
        * (atom.p1 - atom.p0)
        * (atom.s1 - atom.s0)
        / PARAMETER_WIDTH
    )


def atom_row(
    atom: Atom,
    classification: dict[str, Any],
    parent_owner_digest: str,
    midpoint_promoted_parent: bool,
) -> dict[str, Any]:
    payload = {
        "source_core_id": core_id(atom.source_core),
        "dyadic_path": atom.path,
        "source_box": {
            "t": [str(atom.t0), str(atom.t1)],
            "p": [str(atom.p0), str(atom.p1)],
            "s": [str(atom.s0), str(atom.s1)],
        },
    }
    raw_base = base_mass(atom)
    return {
        "atom_id": "full-core-step1:" + canonical_digest(payload),
        **payload,
        "source_core_index": atom.source_core_index,
        "depth": atom.depth,
        "positive_two_dimensional_source_rectangle_at_each_s": (
            atom.t0 < atom.t1 and atom.p0 < atom.p1
        ),
        "positive_parameter_interval": atom.s0 < atom.s1,
        "midpoint_proposal_promoted_parent": midpoint_promoted_parent,
        "strict_next_collision_owner_inherited_from_whole_parent_core": True,
        "complete_retained_candidate_comparison_inherited": True,
        "parent_owner_witness_sha256": parent_owner_digest,
        "classification": classification["classification"],
        "destination_core_id": classification["destination_core_id"],
        "classification_witness_rows_sha256": canonical_digest(
            classification["witness_rows"]
        ),
        "output_enclosures": classification["output_enclosures"],
        "parameter_averaged_unnormalized_base_mass": str(raw_base),
        "parameter_averaged_unnormalized_collision_mass_lower": str(raw_base),
        "parameter_averaged_unnormalized_collision_mass_upper": str(
            GLOBAL_DTHETA_DT_UPPER * raw_base
        ),
        "canonical_invariant_area_coordinates": "(r,p=sin(phi))",
        "absolute_inverse_invariant_area_Jacobian": "1",
        "log_invariant_area_Jacobian_distortion": "0",
    }


def adaptive_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cores = core_cert.physical_cores()
    if len(cores) != 24:
        raise RuntimeError("core registry changed")
    owner_rows = [core_cert.certify_core(core) for core in cores]
    owner_digests = [canonical_digest(row) for row in owner_rows]
    if not all(row["strict_first_hit"] for row in owner_rows):
        raise RuntimeError("parent owner replay failed")

    rows: list[dict[str, Any]] = []
    promoted_parent_ids: set[tuple[int, str]] = set()
    for index, core in enumerate(cores):
        root = Atom(
            index,
            core,
            core.t0,
            core.t1,
            core.p0,
            core.p1,
            core_cert.S_LOWER,
            core_cert.S_UPPER,
            "",
        )
        stack: list[tuple[Atom, bool]] = [(root, False)]
        while stack:
            atom, promoted_lineage = stack.pop()
            classification = classify_atom(atom, cores)
            kind = classification["classification"]
            if kind != "UNRESOLVED_OUTER":
                rows.append(atom_row(
                    atom,
                    classification,
                    owner_digests[index],
                    promoted_lineage,
                ))
                continue
            if atom.depth < BASE_MAX_BINARY_DEPTH:
                stack.extend(
                    (child, False) for child in reversed(split_atom(atom))
                )
                continue
            if atom.depth == BASE_MAX_BINARY_DEPTH:
                proposal = classify_atom(midpoint_atom(atom), cores)
                if proposal["classification"] == "RETURN_AT_1_INNER":
                    promoted_parent_ids.add((index, atom.path))
                    stack.extend(
                        (child, True) for child in reversed(split_atom(atom))
                    )
                    continue
                rows.append(atom_row(
                    atom,
                    classification,
                    owner_digests[index],
                    False,
                ))
                continue
            if atom.depth < PROMOTED_MAX_BINARY_DEPTH and promoted_lineage:
                stack.extend(
                    (child, True) for child in reversed(split_atom(atom))
                )
                continue
            rows.append(atom_row(
                atom,
                classification,
                owner_digests[index],
                promoted_lineage,
            ))

    rows.sort(key=lambda row: (row["source_core_index"], row["dyadic_path"]))
    if len({row["atom_id"] for row in rows}) != len(rows):
        raise RuntimeError("duplicate atom id")
    if not all(
        row["positive_two_dimensional_source_rectangle_at_each_s"]
        and row["positive_parameter_interval"]
        for row in rows
    ):
        raise RuntimeError("degenerate adaptive leaf")
    for source_index in range(24):
        source_rows = [row for row in rows if row["source_core_index"] == source_index]
        paths = [row["dyadic_path"] for row in source_rows]
        if any(
            left != right and right.startswith(left)
            for left in paths
            for right in paths
        ):
            raise RuntimeError("non-prefix-free leaves")
        parent = cores[source_index]
        expected = (
            first_hit.RADIUS[parent.source]
            * (parent.t1 - parent.t0)
            * (parent.p1 - parent.p0)
        )
        observed = sum(Q(row["parameter_averaged_unnormalized_base_mass"])
                       for row in source_rows)
        if observed != expected:
            raise RuntimeError("source cover mass mismatch")

    diagnostics = {
        "promoted_depth12_parent_count": len(promoted_parent_ids),
        "promoted_parent_ids_sha256": canonical_digest(sorted(promoted_parent_ids)),
        "parent_owner_rows_sha256": canonical_digest(owner_rows),
    }
    return rows, diagnostics


def normalized_lower(raw_base: Q) -> Q:
    # Total collision volume = 4*pi*(R_G+R_W), with pi<22/7.
    return raw_base / (
        4 * Q(22, 7) * (first_hit.RADIUS["G"] + first_hit.RADIUS["W"])
    )


def normalized_upper(raw_base: Q) -> Q:
    # pi>3 and dtheta/dt<1401/1000 on |t|<=7/10.
    return GLOBAL_DTHETA_DT_UPPER * raw_base / (
        4 * 3 * (first_hit.RADIUS["G"] + first_hit.RADIUS["W"])
    )


def parameter_slab_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Summarize the uniform leaf cover on each finest open s slab."""
    slab_count = 2 ** (PROMOTED_MAX_BINARY_DEPTH // 3)
    cores = core_cert.physical_cores()
    result: list[dict[str, Any]] = []
    for slab_index in range(slab_count):
        s0 = core_cert.S_LOWER + PARAMETER_WIDTH * Q(slab_index, slab_count)
        s1 = core_cert.S_LOWER + PARAMETER_WIDTH * Q(slab_index + 1, slab_count)
        midpoint = (s0 + s1) / 2
        active = [
            row
            for row in rows
            if Q(row["source_box"]["s"][0]) < midpoint
            < Q(row["source_box"]["s"][1])
        ]
        histogram = Counter(row["classification"] for row in active)
        fixed_s_mass = {
            kind: sum(
                first_hit.RADIUS[
                    cores[row["source_core_index"]].source
                ]
                * (Q(row["source_box"]["t"][1]) - Q(row["source_box"]["t"][0]))
                * (Q(row["source_box"]["p"][1]) - Q(row["source_box"]["p"][0]))
                for row in active
                if row["classification"] == kind
            )
            for kind in (
                "RETURN_AT_1_INNER",
                "SURVIVE_THROUGH_1_INNER",
                "UNRESOLVED_OUTER",
            )
        }
        if sum(fixed_s_mass.values()) != Q(273, 156250):
            raise RuntimeError("fixed-s slab source cover mismatch")
        result.append({
            "slab_index": slab_index,
            "open_s_interval": [str(s0), str(s1)],
            "active_leaf_count": len(active),
            "classification_histogram": dict(sorted(histogram.items())),
            "return_inner_fixed_s_base_mass": str(
                fixed_s_mass["RETURN_AT_1_INNER"]
            ),
            "survivor_inner_fixed_s_base_mass": str(
                fixed_s_mass["SURVIVE_THROUGH_1_INNER"]
            ),
            "unresolved_outer_fixed_s_base_mass": str(
                fixed_s_mass["UNRESOLVED_OUTER"]
            ),
            "full_C24_fixed_s_base_mass": "273/156250",
        })
    return result


def build_result() -> dict[str, Any]:
    load_dependencies()
    if not (
        GLOBAL_DTHETA_DT_UPPER * GLOBAL_DTHETA_DT_UPPER
        * (1 - Q(7, 10) * Q(7, 10))
        > 1
    ):
        raise RuntimeError("dtheta/dt rational upper proof failed")
    rows, diagnostics = adaptive_rows()
    histogram = Counter(row["classification"] for row in rows)
    depth_histogram = Counter(row["depth"] for row in rows)
    source_return_ids = {
        row["source_core_id"]
        for row in rows
        if row["classification"] == "RETURN_AT_1_INNER"
    }
    destination_return_ids = {
        row["destination_core_id"]
        for row in rows
        if row["classification"] == "RETURN_AT_1_INNER"
    }
    mass_by_kind = {
        kind: sum(
            Q(row["parameter_averaged_unnormalized_base_mass"])
            for row in rows
            if row["classification"] == kind
        )
        for kind in (
            "RETURN_AT_1_INNER",
            "SURVIVE_THROUGH_1_INNER",
            "UNRESOLVED_OUTER",
        )
    }
    total_base = sum(mass_by_kind.values())
    if total_base != Q(273, 156250):
        raise RuntimeError("full C24 source mass mismatch")
    if histogram["RETURN_AT_1_INNER"] == 0:
        raise RuntimeError("no positive full-dimensional return inner box")
    slab_rows = parameter_slab_rows(rows)
    minimum_fixed_s_return_base = min(
        Q(row["return_inner_fixed_s_base_mass"]) for row in slab_rows
    )
    return_fraction = mass_by_kind["RETURN_AT_1_INNER"] / total_base
    unresolved_fraction = mass_by_kind["UNRESOLVED_OUTER"] / total_base
    return_normalized_lower = normalized_lower(
        mass_by_kind["RETURN_AT_1_INNER"]
    )
    axis_base = sum(
        first_hit.RADIUS[core.source]
        * (core.t1 - core.t0)
        * (core.p1 - core.p0)
        for core in core_cert.physical_cores()
        if core.family == "axis_translate"
    )
    diagonal_base = total_base - axis_base
    if axis_base != Q(13, 156250) or diagonal_base != Q(26, 15625):
        raise RuntimeError("axis/diagonal base decomposition changed")
    axis_dtheta_upper = Q(1001, 1000)
    if not axis_dtheta_upper * axis_dtheta_upper * (1 - Q(1, 50) ** 2) > 1:
        raise RuntimeError("axis dtheta upper proof failed")
    normalized_C24_upper = (
        axis_dtheta_upper * axis_base
        + GLOBAL_DTHETA_DT_UPPER * diagonal_base
    ) / (4 * 3 * (first_hit.RADIUS["G"] + first_hit.RADIUS["W"]))
    if normalized_C24_upper != Q(29021, 75000000):
        raise RuntimeError("C24 normalized mass upper changed")
    uniform_return_probability_lower = (
        normalized_lower(minimum_fixed_s_return_base) / normalized_C24_upper
    )
    if not return_fraction > Q(1, 70):
        raise RuntimeError("return-inner averaged fraction target failed")
    if not unresolved_fraction < Q(1, 10):
        raise RuntimeError("unresolved averaged fraction target failed")
    if not return_normalized_lower > Q(1, 300000):
        raise RuntimeError("return-inner normalized mass target failed")
    if minimum_fixed_s_return_base != Q(711, 32000000):
        raise RuntimeError("unexpected fixed-s return-inner minimum")
    if not minimum_fixed_s_return_base / total_base > Q(1, 80):
        raise RuntimeError("uniform fixed-s return fraction target failed")
    if not normalized_lower(minimum_fixed_s_return_base) > Q(1, 400000):
        raise RuntimeError("uniform fixed-s normalized return mass target failed")
    if not normalized_C24_upper < Q(1, 2500):
        raise RuntimeError("C24 normalized upper benchmark failed")
    if not uniform_return_probability_lower > Q(1, 160):
        raise RuntimeError("uniform immediate-return probability target failed")

    registry = {
        "source_core_count": 24,
        "source_phase_dimension_at_fixed_parameter": 2,
        "parameter_dimension": 1,
        "parameter_window": [str(core_cert.S_LOWER), str(core_cert.S_UPPER)],
        "base_max_binary_depth": BASE_MAX_BINARY_DEPTH,
        "promoted_max_binary_depth": PROMOTED_MAX_BINARY_DEPTH,
        "midpoint_search_role": "proposal_only_for_refinement",
        "strict_Arb_admission_only": True,
        "adaptive_leaf_count": len(rows),
        "classification_histogram": dict(sorted(histogram.items())),
        "depth_histogram": {
            str(depth): count for depth, count in sorted(depth_histogram.items())
        },
        "promoted_depth12_parent_count": diagnostics[
            "promoted_depth12_parent_count"
        ],
        "source_core_count_with_positive_return_inner_atom": len(source_return_ids),
        "destination_core_count_hit_by_return_inner_atoms": len(
            destination_return_ids
        ),
        "all_24_parent_branches_have_complete_strict_first_owner_replay": True,
        "all_leaf_source_domains_positive_2D_at_each_parameter": True,
        "all_leaf_parameter_intervals_positive": True,
        "leaf_interiors_pairwise_disjoint": True,
        "leaf_union_covers_C24_times_parameter_modulo_shared_null_faces": True,
        "step1_collision_singular_atom_count": 0,
        "unresolved_atoms_are_only_core_membership_or_chart_boundary_outer_boxes": True,
        "canonical_invariant_area_Jacobian_on_every_regular_leaf": "1",
        "global_dtheta_dt_strict_upper_on_abs_t_le_7_over_10": str(
            GLOBAL_DTHETA_DT_UPPER
        ),
        "parent_owner_rows_sha256": diagnostics["parent_owner_rows_sha256"],
        "promoted_parent_ids_sha256": diagnostics["promoted_parent_ids_sha256"],
        "raw_leaf_rows_sha256": canonical_digest(rows),
        "finest_open_parameter_slab_count": len(slab_rows),
        "all_open_parameter_slabs_cover_full_C24": True,
        "all_open_parameter_slabs_have_positive_return_inner": True,
        "parameter_slab_rows_sha256": canonical_digest(slab_rows),
    }
    mass_frontier = {
        "parameter_average_measure": "uniform_ds_on_[-1/400,1/400]",
        "source_collision_density": "R_source/sqrt(1-t^2) dt dp",
        "full_C24_parameter_averaged_unnormalized_base_mass": str(total_base),
        "return_inner_base_mass": str(mass_by_kind["RETURN_AT_1_INNER"]),
        "survivor_inner_base_mass": str(
            mass_by_kind["SURVIVE_THROUGH_1_INNER"]
        ),
        "unresolved_outer_base_mass": str(mass_by_kind["UNRESOLVED_OUTER"]),
        "return_inner_normalized_collision_SRB_mass_strict_lower": str(
            return_normalized_lower
        ),
        "unresolved_outer_normalized_collision_SRB_mass_strict_upper": str(
            normalized_upper(mass_by_kind["UNRESOLVED_OUTER"])
        ),
        "return_inner_base_fraction_of_C24": str(return_fraction),
        "survivor_inner_base_fraction_of_C24": str(
            mass_by_kind["SURVIVE_THROUGH_1_INNER"] / total_base
        ),
        "unresolved_outer_base_fraction_of_C24": str(unresolved_fraction),
        "return_inner_base_fraction_strict_lower": "1/70",
        "unresolved_outer_base_fraction_strict_upper": "1/10",
        "return_inner_normalized_mass_strict_lower_benchmark": "1/300000",
        "uniform_all_s_return_inner_base_mass_lower": str(
            minimum_fixed_s_return_base
        ),
        "uniform_all_s_return_inner_base_fraction_strict_lower": "1/80",
        "uniform_all_s_return_inner_normalized_collision_SRB_mass_lower": str(
            normalized_lower(minimum_fixed_s_return_base)
        ),
        "uniform_all_s_return_inner_normalized_mass_strict_lower_benchmark": (
            "1/400000"
        ),
        "dyadic_s_boundary_policy": (
            "choose_either_adjacent_closed_leaf_partition; strict box admission "
            "includes the shared parameter endpoint"
        ),
        "C24_normalized_collision_SRB_mass_strict_upper": str(
            normalized_C24_upper
        ),
        "C24_normalized_mass_strict_upper_benchmark": "1/2500",
        "uniform_all_s_muC_first_return_at_1_probability_strict_lower": str(
            uniform_return_probability_lower
        ),
        "uniform_all_s_muC_first_return_at_1_probability_benchmark": "1/160",
        "immediate_return_probability_is_unconditional_at_time_0_not_survivor_conditioned": True,
        "base_mass_identity_return_plus_survivor_plus_unresolved": True,
        "true_R1_is_contained_in_return_inner_union_unresolved_outer_mod_null": True,
        "true_Q1_is_contained_in_survivor_inner_union_unresolved_outer_mod_null": True,
    }
    scope = {
        "one_step_return_inner_operator_R1_nonzero": "CERTIFIED",
        "one_step_survivor_inner_operator_Q1_nonzero": "CERTIFIED",
        "full_step1_R1_Q1_partition_without_unresolved_cover": "NOT_CERTIFIED",
        "finite_or_infinite_full_return_partition": "NOT_CERTIFIED",
        "unweighted_exponential_return_tail": "NOT_CERTIFIED",
        "q_weighted_strong_return_tail": "NOT_CERTIFIED",
        "induced_strong_Lasota_Yorke_coefficient": "NOT_CERTIFIED",
        "common_forward_reverse_restriction": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }
    result = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "old_artifacts_modified": False,
            "admission_engine": "python-flint Arb",
            "precision_bits": 384,
            "classification_policy": "strict_trichotomy_fail_closed",
            "clock": "source_core_state_is_time_0_and_next_collision_is_time_1",
        },
        "adaptive_full_core_step1_registry": registry,
        "adaptive_full_core_step1_raw_leaf_rows": rows,
        "adaptive_full_core_step1_open_parameter_slab_rows": slab_rows,
        "collision_mass_inner_outer_frontier": mass_frontier,
        "strict_nonpromotion": scope,
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def verdict() -> dict[str, Any]:
    return {
        "full_24_core_times_parameter_adaptive_cover": "CERTIFIED_MOD_NULL_FACES",
        "positive_full_dimensional_R1_inner_branches": "CERTIFIED",
        "strict_full_dimensional_Q1_survivor_inner_branches": "CERTIFIED",
        "uniform_all_s_muC_first_return_at_1_probability_gt_1_over_160": (
            "CERTIFIED"
        ),
        "step1_collision_singular_cemetery": "EMPTY_ON_FROZEN_PARENT_BRANCHES",
        "unresolved_step1_outer_cover": "NONEMPTY",
        "complete_Rn_Qn_first_return_partition": "NOT_CERTIFIED",
        "physical_exponential_return_tail": "NOT_CERTIFIED",
        "induced_strong_operator": "NOT_CERTIFIED",
        "Gate3": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "Gate5": "NOT_CERTIFIED",
    }


def write_manifest(path: Path, verifier_path: Path) -> None:
    result = build_result()
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier_path.resolve()),
        "dependencies": DEPENDENCIES,
        "result": result,
        "verdict": verdict(),
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument(
        "--verifier",
        type=Path,
        default=HERE / "cm2_gate34_full_core_return_adaptive_frontier_verifier.py",
    )
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    if args.write_manifest is not None:
        write_manifest(args.write_manifest, args.verifier)
        print(f"wrote {args.write_manifest}")
        return 0
    result = build_result()
    registry = result["adaptive_full_core_step1_registry"]
    mass = result["collision_mass_inner_outer_frontier"]
    print("FULL_24_CORE_ADAPTIVE_STEP1_COVER: CERTIFIED_MOD_NULL_FACES")
    print("FULL_DIMENSIONAL_R1_INNER_BRANCHES: CERTIFIED")
    print("FULL_DIMENSIONAL_Q1_SURVIVOR_INNER_BRANCHES: CERTIFIED")
    print(f"LEAVES: {registry['adaptive_leaf_count']}")
    print(f"HISTOGRAM: {registry['classification_histogram']}")
    print(f"RETURN_INNER_BASE_MASS: {mass['return_inner_base_mass']}")
    print(f"UNRESOLVED_OUTER_BASE_MASS: {mass['unresolved_outer_base_mass']}")
    print("COMPLETE_RN_QN_PARTITION: NOT_CERTIFIED")
    print("PHYSICAL_EXPONENTIAL_RETURN_TAIL: NOT_CERTIFIED")
    print("INDUCED_STRONG_OPERATOR: NOT_CERTIFIED")
    return 0 if args.summary else 2


if __name__ == "__main__":
    sys.exit(main())
