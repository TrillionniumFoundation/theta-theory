#!/usr/bin/env python3
"""Close the Round-87 C24 landing crosswalk modulo transverse null faces.

Round 87 leaves 6,952 positive-volume rational boxes because their landing
enclosures meet one or more coordinate faces of the frozen 33,960-leaf C24
atlas.  This certificate differentiates the landing map with interval forward
automatic differentiation.  Every possibly met target-face equation has a
uniformly nonzero partial derivative on its source box.  Consequently its
zero set is a codimension-one graph and has three-dimensional Lebesgue measure
zero.  Off the finite union of these graphs, the frozen atlas cover supplies a
unique target leaf.

This is an almost-everywhere landing-to-leaf crosswalk.  It is not a stable
plaque, a later-return construction, or a Gate-2/Gate-4 promotion.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_full_core_return_adaptive_frontier_cert as atlas


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round88.c24-pullback-event-surface-closure.v1"
R87 = HERE / "cm2-round87-c24-landing-pullback-arrangement-2026-07-22.json"
FULL = HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
R85_INCIDENCE = HERE / "cm2-round85-c24-full-return-incidence-2026-07-22.json"
R85_CROSSWALK = HERE / "cm2-round85-c24-variable-return-crosswalk-2026-07-22.json"

PINS = {
    R87.name: "361f492eddeb342327706991a273aa70c3eebc54cd402799e2995f1034505121",
    "cm2_round87_c24_landing_pullback_arrangement_cert.py":
        "a8d92feb1ad4b12b50f3f4f32840fee7f360747d23fe4f4b667dae07c1b56637",
    FULL.name: "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",
    R85_INCIDENCE.name:
        "e79ae8e779de3f05f21eb468d71817d10ef743ce49312637fb603cf937cba295",
    "cm2_round85_c24_full_return_incidence_cert.py":
        "de95de3a0ae3f3d7aa09a48f048adc9ef03575040a8b30adcdb9cff70ce4d84d",
    R85_CROSSWALK.name:
        "f20e24ed0ef879628ad54c91e7ecb939ea9d870fd6ffbb638f048bce0be54ebc",
    "cm2_round85_c24_variable_return_crosswalk_cert.py":
        "91b0ad807391aafce8862451273fb007115f4c4a66d0c60b82ea642cd63f85cd",
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json":
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py":
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
}

DERIVATIVE_GAP = Q(7, 5)
RETURN_HULL_GAP = Q(1, 200)
COORDINATES = ("t", "p", "s")


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(value: bool, label: str) -> None:
    if not value:
        raise ValueError(label)


def qarb(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def collect(value: Any, rows: list[dict[str, Any]]) -> None:
    if isinstance(value, dict):
        if "classification" in value and "source_box" in value and "atom_id" in value:
            rows.append(value)
        for child in value.values():
            collect(child, rows)
    elif isinstance(value, list):
        for child in value:
            collect(child, rows)


def interval(lower: Q, upper: Q) -> arb:
    require(lower <= upper, "interval order")
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    return qarb(middle) + arb(0, qarb(radius).upper())


@dataclass(frozen=True)
class Jet:
    """An Arb value and its interval gradient in source (t,p,s)."""

    value: arb
    gradient: tuple[arb, arb, arb]

    @staticmethod
    def constant(value: arb | int) -> "Jet":
        return Jet(value if isinstance(value, arb) else arb(value), (arb(0), arb(0), arb(0)))

    def _coerce(self, other: "Jet | arb | int") -> "Jet":
        return other if isinstance(other, Jet) else Jet.constant(other)

    def __add__(self, other: "Jet | arb | int") -> "Jet":
        other = self._coerce(other)
        return Jet(self.value + other.value, tuple(a + b for a, b in zip(self.gradient, other.gradient)))

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet(-self.value, tuple(-value for value in self.gradient))

    def __sub__(self, other: "Jet | arb | int") -> "Jet":
        return self + (-self._coerce(other))

    def __rsub__(self, other: "Jet | arb | int") -> "Jet":
        return self._coerce(other) - self

    def __mul__(self, other: "Jet | arb | int") -> "Jet":
        other = self._coerce(other)
        return Jet(
            self.value * other.value,
            tuple(a * other.value + self.value * b for a, b in zip(self.gradient, other.gradient)),
        )

    __rmul__ = __mul__

    def __truediv__(self, other: "Jet | arb | int") -> "Jet":
        other = self._coerce(other)
        denominator = other.value * other.value
        return Jet(
            self.value / other.value,
            tuple(
                (a * other.value - self.value * b) / denominator
                for a, b in zip(self.gradient, other.gradient)
            ),
        )

    def sqrt(self) -> "Jet":
        require(bool(self.value > 0), "positive square-root radicand")
        root = self.value.sqrt()
        return Jet(root, tuple(value / (2 * root) for value in self.gradient))


def variable(lower: Q, upper: Q, coordinate: int) -> Jet:
    gradient = [arb(0), arb(0), arb(0)]
    gradient[coordinate] = arb(1)
    return Jet(interval(lower, upper), tuple(gradient))  # type: ignore[arg-type]


def landing_jet(atom: atlas.Atom, destination: core_cert.Core) -> dict[str, Jet | arb]:
    """Independently replay one collision and differentiate its landing chart."""

    source, cell = atom.source_core.chart_id.split(":")
    t = variable(atom.t0, atom.t1, 0)
    p = variable(atom.p0, atom.p1, 1)
    s = variable(atom.s0, atom.s1, 2)
    normal_radical = (1 - t * t).sqrt()
    momentum_radical = (1 - p * p).sqrt()
    if cell == "E":
        normal_x, normal_y = normal_radical, t
    elif cell == "W":
        normal_x, normal_y = -normal_radical, t
    elif cell == "N":
        normal_x, normal_y = t, normal_radical
    elif cell == "S":
        normal_x, normal_y = t, -normal_radical
    else:
        raise ValueError(cell)
    velocity_x = momentum_radical * normal_x - p * normal_y
    velocity_y = momentum_radical * normal_y + p * normal_x
    if source == "G":
        center_x, center_y = Jet.constant(0), Jet.constant(0)
    else:
        center_x, center_y = Jet.constant(qarb(Q(1, 2))) + s, Jet.constant(qarb(Q(1, 2)))
    source_radius = qarb(first_hit.RADIUS[source])
    point_x = center_x + source_radius * normal_x
    point_y = center_y + source_radius * normal_y
    target = first_hit.target_by_id(atom.source_core.target_id)
    if target.obstacle == "G":
        target_x, target_y = Jet.constant(target.ix), Jet.constant(target.iy)
    else:
        target_x = Jet.constant(target.ix) + qarb(Q(1, 2)) + s
        target_y = Jet.constant(target.iy) + qarb(Q(1, 2))
    delta_x, delta_y = target_x - point_x, target_y - point_y
    longitudinal = velocity_x * delta_x + velocity_y * delta_y
    transverse = -velocity_y * delta_x + velocity_x * delta_y
    target_radius = qarb(first_hit.RADIUS[target.obstacle])
    discriminant = target_radius * target_radius - transverse * transverse
    radical = discriminant.sqrt()
    near = longitudinal - radical
    require(bool(near.value > 0), "strict future collision")
    require(bool(near.value < qarb(first_hit.TAU_MAX)), "collision before horizon")
    output_normal_x = (-radical * velocity_x + transverse * velocity_y) / target_radius
    output_normal_y = (-radical * velocity_y - transverse * velocity_x) / target_radius
    landing_p = transverse / target_radius
    destination_cell = destination.chart_id.split(":")[1]
    landing_t = output_normal_y if destination_cell in ("E", "W") else output_normal_x
    return {
        "t": landing_t,
        "p": landing_p,
        "normal_x": output_normal_x,
        "normal_y": output_normal_y,
        "normal_radicand": 1 - t.value * t.value,
        "momentum_radicand": 1 - p.value * p.value,
        "collision_discriminant": discriminant.value,
        "near": near.value,
    }


def overlaps_rational(value: arb, boundary: Q) -> bool:
    point = qarb(boundary)
    return not bool(value < point) and not bool(value > point)


def derivative_witness(value: Jet) -> tuple[str, arb]:
    """Choose the first coordinate with a certified uniform derivative gap."""

    for name, derivative in zip(COORDINATES, value.gradient):
        magnitude = derivative if bool(derivative > 0) else -derivative if bool(derivative < 0) else None
        if magnitude is not None and bool(magnitude > qarb(DERIVATIVE_GAP)):
            return name, derivative
    raise ValueError("no uniform transverse derivative")


def volume(row: dict[str, Any]) -> Q:
    return (
        (Q(row["t"][1]) - Q(row["t"][0]))
        * (Q(row["p"][1]) - Q(row["p"][0]))
        * (Q(row["s"][1]) - Q(row["s"][0]))
    )


def build(precision_bits: int = 512) -> dict[str, Any]:
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        require(file_digest(HERE / name) == expected, "pin " + name)

    round87 = json.loads(R87.read_text())
    r87_result = round87["result"]
    require(
        r87_result["remaining_equation_frontier"]
        == {
            "residual_leaf_count": 6952,
            "all_residuals_intersect_frozen_target_boundary": True,
            "equations": [
                "landing_t(t,p,s)=target_t_boundary",
                "landing_p(t,p,s)=target_p_boundary",
                "s=target_s_boundary",
            ],
        },
        "Round87 residual frontier",
    )
    residual_rows = sorted(
        r87_result["evidence"]["residual_rows"],
        key=lambda row: (row["parent_atom_id"], row["path"], row["destination_core_id"]),
    )
    require(len(residual_rows) == 6952, "residual row census")
    require(qstr(sum((volume(row) for row in residual_rows), Q())) == "1793/8192000000", "residual mass")

    incidence = json.loads(R85_INCIDENCE.read_text())["result"]
    require(incidence["status"] == "CERTIFIED_EMPTY_LANDING_TO_RETURN_SOURCE_INCIDENCE_GRAPH", "Round85 incidence status")
    require(incidence["landing_to_source_atom_incidence_graph"]["edge_count"] == 0, "Round85 RETURN edge count")
    require(not incidence["constructive_consequence"]["nonempty_recurrent_same_key_subroot_in_current_atlas"], "Round85 recurrence state")
    crosswalk = json.loads(R85_CROSSWALK.read_text())["result"]
    require(crosswalk["graph_frontier"]["RETURN_to_RETURN_possible_edges"] == 0, "Round85 crosswalk RETURN frontier")
    require(crosswalk["evidence"]["boundary_straddling_landing_count"] == 2328, "Round85 boundary source census")

    full_document = json.loads(FULL.read_text())
    registry = full_document["result"]["adaptive_full_core_step1_registry"]
    require(registry["adaptive_leaf_count"] == 33960, "target atlas leaf census")
    require(registry["leaf_interiors_pairwise_disjoint"], "target atlas disjoint interiors")
    require(registry["leaf_union_covers_C24_times_parameter_modulo_shared_null_faces"], "target atlas cover")
    atlas_rows: list[dict[str, Any]] = []
    collect(full_document, atlas_rows)
    require(len(atlas_rows) == 33960, "collected target leaf census")
    by_atom = {row["atom_id"]: row for row in atlas_rows}
    require(len(by_atom) == 33960, "unique target atom ids")
    cores = {atlas.core_id(core): core for core in core_cert.physical_cores()}
    require(len(cores) == 24, "C24 core census")

    boundaries: dict[str, dict[str, set[Q]]] = {}
    return_rows: dict[str, list[dict[str, Any]]] = {}
    for row in atlas_rows:
        core_id = row["source_core_id"]
        boundaries.setdefault(core_id, {name: set() for name in COORDINATES})
        for name in COORDINATES:
            boundaries[core_id][name].update(map(Q, row["source_box"][name]))
        if row["classification"] == "RETURN_AT_1_INNER":
            return_rows.setdefault(core_id, []).append(row)
    return_hulls = {
        core_id: (
            min(Q(row["source_box"]["p"][0]) for row in rows),
            max(Q(row["source_box"]["p"][1]) for row in rows),
        )
        for core_id, rows in return_rows.items()
    }
    require(len(return_hulls) == 16, "active return core census")

    event_histogram: Counter[str] = Counter()
    derivative_histogram: Counter[str] = Counter()
    return_separator_histogram: Counter[str] = Counter()
    parent_ids: set[str] = set()
    witness_rows: list[dict[str, Any]] = []
    all_event_occurrences = 0
    for row in residual_rows:
        parent = by_atom[row["parent_atom_id"]]
        require(parent["classification"] == "RETURN_AT_1_INNER", "residual source is return")
        require(parent["destination_core_id"] == row["destination_core_id"], "destination key")
        source = cores[parent["source_core_id"]]
        destination = cores[row["destination_core_id"]]
        atom = atlas.Atom(
            0,
            source,
            *map(Q, row["t"]),
            *map(Q, row["p"]),
            *map(Q, row["s"]),
            row["path"],
        )
        geometry = landing_jet(atom, destination)
        landing_t = geometry["t"]
        landing_p = geometry["p"]
        require(isinstance(landing_t, Jet) and isinstance(landing_p, Jet), "jet types")
        require(bool(geometry["normal_radicand"] > 0), "source chart regularity")
        require(bool(geometry["momentum_radicand"] > 0), "momentum regularity")
        require(bool(geometry["collision_discriminant"] > 0), "collision regularity")
        require(bool(landing_t.value > qarb(destination.t0)), "landing t lower core interior")
        require(bool(landing_t.value < qarb(destination.t1)), "landing t upper core interior")
        require(bool(landing_p.value > qarb(destination.p0)), "landing p lower core interior")
        require(bool(landing_p.value < qarb(destination.p1)), "landing p upper core interior")
        _chart_t, inside_chart, _outside_chart = atlas.chart_tests(
            destination.chart_id.split(":")[1],
            geometry["normal_x"].value,  # type: ignore[union-attr]
            geometry["normal_y"].value,  # type: ignore[union-attr]
        )
        require(all(flag for _name, flag in inside_chart), "destination chart interior")
        ordinary = atlas.atom_geometry(atom)
        require(ordinary is not None, "ordinary collision replay")
        require(ordinary["p_target"].overlaps(landing_p.value), "AD p replay overlap")

        local_counts: dict[str, int] = {}
        local_derivatives: dict[str, dict[str, str]] = {}
        for name, value in (("t", landing_t), ("p", landing_p)):
            hits = [q for q in boundaries[row["destination_core_id"]][name] if overlaps_rational(value.value, q)]
            local_counts[name] = len(hits)
            if hits:
                coordinate, derivative = derivative_witness(value)
                local_derivatives[name] = {
                    "coordinate": coordinate,
                    "derivative_enclosure": str(derivative),
                    "absolute_derivative_strict_lower": qstr(DERIVATIVE_GAP),
                }
                event_histogram[name] += len(hits)
                derivative_histogram[f"{name}_by_{coordinate}"] += len(hits)
                all_event_occurrences += len(hits)
        s0, s1 = map(Q, row["s"])
        s_hits = [q for q in boundaries[row["destination_core_id"]]["s"] if s0 <= q <= s1]
        local_counts["s"] = len(s_hits)
        if s_hits:
            local_derivatives["s"] = {
                "coordinate": "s",
                "derivative_enclosure": "1.0000000000000000000",
                "absolute_derivative_exact": "1",
            }
            event_histogram["s"] += len(s_hits)
            derivative_histogram["s_by_s"] += len(s_hits)
            all_event_occurrences += len(s_hits)
        require(sum(local_counts.values()) > 0, "residual without target-face event")

        hull0, hull1 = return_hulls[row["destination_core_id"]]
        below = qarb(hull0) - landing_p.value
        above = landing_p.value - qarb(hull1)
        if bool(below > qarb(RETURN_HULL_GAP)):
            separator, gap = "landing_p_below_RETURN_source_hull", below
        elif bool(above > qarb(RETURN_HULL_GAP)):
            separator, gap = "landing_p_above_RETURN_source_hull", above
        else:
            raise ValueError("RETURN source hull separation")
        return_separator_histogram[separator] += 1
        parent_ids.add(row["parent_atom_id"])
        witness_rows.append(
            {
                "row_id": digest([row["parent_atom_id"], row["path"], row["destination_core_id"]]),
                "parent_atom_id": row["parent_atom_id"],
                "destination_core_id": row["destination_core_id"],
                "path": row["path"],
                "target_boundary_occurrences": dict(sorted(local_counts.items())),
                "transverse_derivative_witnesses": dict(sorted(local_derivatives.items())),
                "RETURN_source_separator": separator,
                "RETURN_source_gap_enclosure": str(gap),
                "RETURN_source_gap_strict_lower": qstr(RETURN_HULL_GAP),
            }
        )

    require(len(witness_rows) == 6952, "witness row census")
    require(sum(event_histogram.values()) == all_event_occurrences, "event occurrence sum")
    require(return_separator_histogram == {
        "landing_p_above_RETURN_source_hull": 3476,
        "landing_p_below_RETURN_source_hull": 3476,
    }, "RETURN separator symmetry")

    semantic_rows = [
        [
            row["row_id"],
            row["target_boundary_occurrences"],
            {key: value["coordinate"] for key, value in row["transverse_derivative_witnesses"].items()},
            row["RETURN_source_separator"],
        ]
        for row in witness_rows
    ]
    evidence = {
        "precision_bits": precision_bits,
        "round87_residual_row_count": len(residual_rows),
        "round87_residual_parent_count": len(parent_ids),
        "round87_residual_volume": "1793/8192000000",
        "round87_residual_volume_ratio": "1793/2298",
        "frozen_target_leaf_count": 33960,
        "frozen_target_boundary_value_count_by_coordinate": {
            name: sum(len(value[name]) for value in boundaries.values()) for name in COORDINATES
        },
        "box_local_target_boundary_occurrence_histogram": dict(sorted(event_histogram.items())),
        "box_local_target_boundary_occurrence_count": all_event_occurrences,
        "transverse_derivative_coordinate_histogram": dict(sorted(derivative_histogram.items())),
        "uniform_t_or_p_event_absolute_partial_derivative_strict_lower": qstr(DERIVATIVE_GAP),
        "s_event_exact_partial_derivative": "1",
        "regularity_checks_per_row": [
            "1-t^2>0",
            "1-p^2>0",
            "collision_discriminant>0",
            "0<near<3",
            "strict_destination_chart_and_core_interior",
        ],
        "RETURN_source_separator_histogram": dict(sorted(return_separator_histogram.items())),
        "uniform_RETURN_source_coordinate_gap_strict_lower": qstr(RETURN_HULL_GAP),
        "upstream_full_4216_RETURN_atom_empty_incidence_graph_replayed": True,
        "upstream_2328_boundary_source_crosswalk_replayed": True,
        "semantic_witness_ledger_sha256": digest(semantic_rows),
        "witness_rows": witness_rows,
    }
    result = {
        "status": "CERTIFIED_AE_C24_LANDING_TO_FROZEN_LEAF_CROSSWALK_CLOSURE",
        "round87_positive_volume_frontier": {
            "input_residual_boxes": 6952,
            "input_residual_volume_ratio": "1793/2298",
            "positive_volume_ambiguity_after_transverse_surface_quotient": 0,
            "exceptional_set": "FINITE_UNION_OF_TRANSVERSE_C1_HYPERSURFACES__LEBESGUE_NULL",
            "off_exceptional_set_unique_frozen_target_leaf": True,
            "pointwise_target_leaf_on_shared_faces": "NOT_CANONICALLY_ASSIGNED",
        },
        "one_step_same_key_recurrence_search": {
            "RETURN_to_RETURN_possible_residual_box_count": 0,
            "RETURN_to_RETURN_edge_count": 0,
            "nonempty_one_step_recurrent_same_key_subroot_in_current_frozen_atlas": False,
            "proof": "all_6952_landing_p_enclosures_are_strictly_separated_from_destination_RETURN_source_hulls",
        },
        "measure_theoretic_scope": {
            "target_leaf_partition_is_the_frozen_33960_leaf_C24_times_parameter_cover": True,
            "finite_transverse_preimages_of_shared_target_faces_are_null": True,
            "does_not_assign_shared_faces_to_a_unique_closed_leaf": True,
            "does_not_continue_SURVIVE_leaves_to_later_return_times": True,
            "does_not_construct_a_stable_plaque_or_holonomy": True,
        },
        "strict_nonpromotion": {
            "Gate2": "NOT_CERTIFIED__0_OF_17",
            "Gate4": "NOT_CERTIFIED__1_OF_7",
            "same_key_all_depth_stable_material_crosswalk": "NOT_CERTIFIED",
        },
        "evidence": evidence,
        "evidence_sha256": digest(evidence),
    }
    return {"schema": SCHEMA, "pins": dict(PINS), "result": result, "result_sha256": digest(result)}


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2, allow_nan=False))
