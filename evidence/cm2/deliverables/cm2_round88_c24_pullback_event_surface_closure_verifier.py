#!/usr/bin/env python3
"""Independent 1024-bit verifier for the Round-88 pullback closure."""
from __future__ import annotations

import copy
import json
import sys
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_full_core_return_adaptive_frontier_cert as atlas
import cm2_round88_c24_pullback_event_surface_closure_cert as cert


HERE = Path(__file__).resolve().parent
INPUT = HERE / "cm2-round88-c24-pullback-event-surface-closure-2026-07-22.json"
INDEPENDENT_BITS = 1024


def require(value: bool, label: str) -> None:
    if not value:
        raise ValueError(label)


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate JSON key " + key)
        result[key] = value
    return result


def strict_load(text: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError("nonfinite " + token)),
    )
    if not isinstance(value, dict):
        raise ValueError("root object required")
    return value


def qarb(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def interval(lower: Q, upper: Q) -> arb:
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    return qarb(middle) + arb(0, qarb(radius).upper())


@dataclass(frozen=True)
class IndependentJet:
    value: arb
    derivative: tuple[arb, arb, arb]

    @staticmethod
    def constant(value: arb | int) -> "IndependentJet":
        return IndependentJet(value if isinstance(value, arb) else arb(value), (arb(0), arb(0), arb(0)))

    def cast(self, other: "IndependentJet | arb | int") -> "IndependentJet":
        return other if isinstance(other, IndependentJet) else IndependentJet.constant(other)

    def __add__(self, other: "IndependentJet | arb | int") -> "IndependentJet":
        other = self.cast(other)
        return IndependentJet(self.value + other.value, tuple(x + y for x, y in zip(self.derivative, other.derivative)))

    __radd__ = __add__

    def __neg__(self) -> "IndependentJet":
        return IndependentJet(-self.value, tuple(-x for x in self.derivative))

    def __sub__(self, other: "IndependentJet | arb | int") -> "IndependentJet":
        return self + (-self.cast(other))

    def __rsub__(self, other: "IndependentJet | arb | int") -> "IndependentJet":
        return self.cast(other) - self

    def __mul__(self, other: "IndependentJet | arb | int") -> "IndependentJet":
        other = self.cast(other)
        return IndependentJet(
            self.value * other.value,
            tuple(x * other.value + self.value * y for x, y in zip(self.derivative, other.derivative)),
        )

    __rmul__ = __mul__

    def __truediv__(self, other: "IndependentJet | arb | int") -> "IndependentJet":
        other = self.cast(other)
        square = other.value * other.value
        return IndependentJet(
            self.value / other.value,
            tuple(
                (x * other.value - self.value * y) / square
                for x, y in zip(self.derivative, other.derivative)
            ),
        )

    def square_root(self) -> "IndependentJet":
        require(bool(self.value > 0), "independent radicand")
        root = self.value.sqrt()
        return IndependentJet(root, tuple(x / (2 * root) for x in self.derivative))


def independent_variable(lower: Q, upper: Q, coordinate: int) -> IndependentJet:
    derivatives = [arb(0), arb(0), arb(0)]
    derivatives[coordinate] = arb(1)
    return IndependentJet(interval(lower, upper), tuple(derivatives))  # type: ignore[arg-type]


def independent_landing(atom: atlas.Atom, destination: core_cert.Core) -> dict[str, Any]:
    """Separate implementation of the line-circle collision derivative."""

    source, chart = atom.source_core.chart_id.split(":")
    source_t = independent_variable(atom.t0, atom.t1, 0)
    source_p = independent_variable(atom.p0, atom.p1, 1)
    parameter = independent_variable(atom.s0, atom.s1, 2)
    rt = (1 - source_t * source_t).square_root()
    rp = (1 - source_p * source_p).square_root()
    chart_normals = {
        "E": (rt, source_t),
        "W": (-rt, source_t),
        "N": (source_t, rt),
        "S": (source_t, -rt),
    }
    nx, ny = chart_normals[chart]
    ux, uy = rp * nx - source_p * ny, rp * ny + source_p * nx
    if source == "G":
        cx, cy = IndependentJet.constant(0), IndependentJet.constant(0)
    else:
        cx, cy = IndependentJet.constant(qarb(Q(1, 2))) + parameter, IndependentJet.constant(qarb(Q(1, 2)))
    radius0 = qarb(first_hit.RADIUS[source])
    point_x, point_y = cx + radius0 * nx, cy + radius0 * ny
    target = first_hit.target_by_id(atom.source_core.target_id)
    if target.obstacle == "G":
        center_x, center_y = IndependentJet.constant(target.ix), IndependentJet.constant(target.iy)
    else:
        center_x = IndependentJet.constant(target.ix) + qarb(Q(1, 2)) + parameter
        center_y = IndependentJet.constant(target.iy) + qarb(Q(1, 2))
    dx, dy = center_x - point_x, center_y - point_y
    ell = ux * dx + uy * dy
    signed_distance = -uy * dx + ux * dy
    radius1 = qarb(first_hit.RADIUS[target.obstacle])
    discriminant = radius1 * radius1 - signed_distance * signed_distance
    radical = discriminant.square_root()
    collision_time = ell - radical
    require(bool(collision_time.value > 0) and bool(collision_time.value < qarb(3)), "independent flight order")
    out_x = (-radical * ux + signed_distance * uy) / radius1
    out_y = (-radical * uy - signed_distance * ux) / radius1
    landing_p = signed_distance / radius1
    target_chart = destination.chart_id.split(":")[1]
    landing_t = out_y if target_chart in ("E", "W") else out_x
    return {
        "t": landing_t,
        "p": landing_p,
        "normal_x": out_x.value,
        "normal_y": out_y.value,
        "normal_radicand": 1 - source_t.value * source_t.value,
        "momentum_radicand": 1 - source_p.value * source_p.value,
        "discriminant": discriminant.value,
    }


def independent_sweep(frozen: dict[str, Any]) -> dict[str, Any]:
    ctx.prec = INDEPENDENT_BITS
    round87 = strict_load(cert.R87.read_text())
    residual_rows = sorted(
        round87["result"]["evidence"]["residual_rows"],
        key=lambda row: (row["parent_atom_id"], row["path"], row["destination_core_id"]),
    )
    full = strict_load(cert.FULL.read_text())
    atlas_rows: list[dict[str, Any]] = []
    cert.collect(full, atlas_rows)
    by_atom = {row["atom_id"]: row for row in atlas_rows}
    cores = {atlas.core_id(core): core for core in core_cert.physical_cores()}
    boundaries: dict[str, dict[str, set[Q]]] = {}
    return_rows: dict[str, list[dict[str, Any]]] = {}
    for row in atlas_rows:
        identifier = row["source_core_id"]
        boundaries.setdefault(identifier, {name: set() for name in cert.COORDINATES})
        for name in cert.COORDINATES:
            boundaries[identifier][name].update(map(Q, row["source_box"][name]))
        if row["classification"] == "RETURN_AT_1_INNER":
            return_rows.setdefault(identifier, []).append(row)
    return_hulls = {
        identifier: (
            min(Q(row["source_box"]["p"][0]) for row in rows),
            max(Q(row["source_box"]["p"][1]) for row in rows),
        )
        for identifier, rows in return_rows.items()
    }
    frozen_rows = frozen["result"]["evidence"]["witness_rows"]
    require(len(frozen_rows) == len(residual_rows) == 6952, "independent row census")
    event_histogram: Counter[str] = Counter()
    derivative_histogram: Counter[str] = Counter()
    separator_histogram: Counter[str] = Counter()
    semantic_rows: list[list[Any]] = []
    residual_volume = Q()
    coordinate_index = {"t": 0, "p": 1, "s": 2}
    for source_row, recorded in zip(residual_rows, frozen_rows):
        parent = by_atom[source_row["parent_atom_id"]]
        source = cores[parent["source_core_id"]]
        destination = cores[source_row["destination_core_id"]]
        atom = atlas.Atom(
            0,
            source,
            *map(Q, source_row["t"]),
            *map(Q, source_row["p"]),
            *map(Q, source_row["s"]),
            source_row["path"],
        )
        residual_volume += cert.volume(source_row)
        landing = independent_landing(atom, destination)
        require(bool(landing["normal_radicand"] > 0), "independent source regularity")
        require(bool(landing["momentum_radicand"] > 0), "independent momentum regularity")
        require(bool(landing["discriminant"] > 0), "independent collision regularity")
        require(bool(landing["t"].value > qarb(destination.t0)) and bool(landing["t"].value < qarb(destination.t1)), "independent t interior")
        require(bool(landing["p"].value > qarb(destination.p0)) and bool(landing["p"].value < qarb(destination.p1)), "independent p interior")
        _coordinate, chart_inside, _outside = atlas.chart_tests(
            destination.chart_id.split(":")[1], landing["normal_x"], landing["normal_y"]
        )
        require(all(flag for _name, flag in chart_inside), "independent chart interior")

        counts: dict[str, int] = {}
        derivative_coordinates: dict[str, str] = {}
        for name in ("t", "p"):
            value: IndependentJet = landing[name]
            hits = sum(
                1
                for boundary in boundaries[source_row["destination_core_id"]][name]
                if not bool(value.value < qarb(boundary)) and not bool(value.value > qarb(boundary))
            )
            counts[name] = hits
            if hits:
                selected = recorded["transverse_derivative_witnesses"][name]["coordinate"]
                derivative = value.derivative[coordinate_index[selected]]
                magnitude = derivative if bool(derivative > 0) else -derivative if bool(derivative < 0) else arb(0)
                require(bool(magnitude > qarb(cert.DERIVATIVE_GAP)), "independent derivative gap")
                derivative_coordinates[name] = selected
                event_histogram[name] += hits
                derivative_histogram[f"{name}_by_{selected}"] += hits
        s0, s1 = map(Q, source_row["s"])
        counts["s"] = sum(
            1 for boundary in boundaries[source_row["destination_core_id"]]["s"] if s0 <= boundary <= s1
        )
        if counts["s"]:
            derivative_coordinates["s"] = "s"
            event_histogram["s"] += counts["s"]
            derivative_histogram["s_by_s"] += counts["s"]
        require(counts == recorded["target_boundary_occurrences"], "independent target event counts")

        hull0, hull1 = return_hulls[source_row["destination_core_id"]]
        below = qarb(hull0) - landing["p"].value
        above = landing["p"].value - qarb(hull1)
        if bool(below > qarb(cert.RETURN_HULL_GAP)):
            separator = "landing_p_below_RETURN_source_hull"
        elif bool(above > qarb(cert.RETURN_HULL_GAP)):
            separator = "landing_p_above_RETURN_source_hull"
        else:
            raise ValueError("independent RETURN hull separation")
        require(separator == recorded["RETURN_source_separator"], "independent RETURN separator label")
        separator_histogram[separator] += 1
        row_id = cert.digest([source_row["parent_atom_id"], source_row["path"], source_row["destination_core_id"]])
        require(row_id == recorded["row_id"], "independent row id")
        semantic_rows.append([row_id, counts, derivative_coordinates, separator])

    evidence = frozen["result"]["evidence"]
    require(cert.qstr(residual_volume) == evidence["round87_residual_volume"], "independent residual volume")
    require(dict(sorted(event_histogram.items())) == evidence["box_local_target_boundary_occurrence_histogram"], "independent event histogram")
    require(dict(sorted(derivative_histogram.items())) == evidence["transverse_derivative_coordinate_histogram"], "independent derivative histogram")
    require(dict(sorted(separator_histogram.items())) == evidence["RETURN_source_separator_histogram"], "independent separator histogram")
    require(cert.digest(semantic_rows) == evidence["semantic_witness_ledger_sha256"], "independent semantic ledger")
    return {
        "residual_rows": len(residual_rows),
        "event_occurrences": sum(event_histogram.values()),
        "event_histogram": dict(sorted(event_histogram.items())),
        "derivative_histogram": dict(sorted(derivative_histogram.items())),
        "separator_histogram": dict(sorted(separator_histogram.items())),
        "semantic_ledger_sha256": cert.digest(semantic_rows),
    }


def main() -> int:
    try:
        frozen = strict_load(INPUT.read_text())
        fresh = cert.build(512)
        require(frozen == fresh, "512-bit byte-semantic replay / closed schema")
        independent = independent_sweep(frozen)

        semantic_attacks = []
        mutations = (
            lambda value: value["result"].__setitem__("status", "CERTIFIED_GATE2"),
            lambda value: value["result"]["round87_positive_volume_frontier"].__setitem__("input_residual_boxes", 0),
            lambda value: value["result"]["round87_positive_volume_frontier"].__setitem__("off_exceptional_set_unique_frozen_target_leaf", False),
            lambda value: value["result"]["one_step_same_key_recurrence_search"].__setitem__("RETURN_to_RETURN_edge_count", 1),
            lambda value: value["result"]["evidence"].__setitem__("uniform_t_or_p_event_absolute_partial_derivative_strict_lower", "100"),
            lambda value: value["result"]["evidence"]["witness_rows"][0].__setitem__("RETURN_source_separator", "NONE"),
            lambda value: value["result"]["strict_nonpromotion"].__setitem__("Gate4", "CERTIFIED"),
            lambda value: value.__setitem__("extra", 1),
        )
        for mutate in mutations:
            attacked = copy.deepcopy(frozen)
            mutate(attacked)
            attacked["result"]["evidence_sha256"] = cert.digest(attacked["result"]["evidence"])
            attacked["result_sha256"] = cert.digest(attacked["result"])
            semantic_attacks.append(attacked != fresh)
        require(all(semantic_attacks), "semantic mutation accepted")

        pin_attacks = []
        for name in cert.PINS:
            attacked = copy.deepcopy(frozen)
            attacked["pins"][name] = "0" * 64
            attacked["result_sha256"] = cert.digest(attacked["result"])
            pin_attacks.append(attacked != fresh)
        require(all(pin_attacks), "pin mutation accepted")

        strict_attacks = []
        for text in ('{"a":1,"a":2}', "NaN", "[]", '{"x":Infinity}'):
            try:
                strict_load(text)
                strict_attacks.append(False)
            except Exception:
                strict_attacks.append(True)
        require(all(strict_attacks), "strict JSON attack accepted")

        result = frozen["result"]
        audit = {
            "schema": "cm2.round88.c24-pullback-event-surface-closure.audit.v1",
            "status": "AUDIT_PASS",
            "producer_precision_bits": 512,
            "independent_precision_bits": INDEPENDENT_BITS,
            "closed_schema_exact_replay": True,
            "independent_residual_rows_recomputed": independent["residual_rows"],
            "independent_box_local_event_occurrences": independent["event_occurrences"],
            "independent_event_histogram": independent["event_histogram"],
            "independent_derivative_histogram": independent["derivative_histogram"],
            "independent_RETURN_separator_histogram": independent["separator_histogram"],
            "independent_semantic_ledger_sha256": independent["semantic_ledger_sha256"],
            "positive_volume_ambiguity_after_surface_quotient":
                result["round87_positive_volume_frontier"]["positive_volume_ambiguity_after_transverse_surface_quotient"],
            "RETURN_to_RETURN_edges": result["one_step_same_key_recurrence_search"]["RETURN_to_RETURN_edge_count"],
            "semantic_mutations_rejected": f"{sum(semantic_attacks)}/{len(semantic_attacks)}",
            "pin_mutations_rejected": f"{sum(pin_attacks)}/{len(pin_attacks)}",
            "strict_json_attacks_rejected": f"{sum(strict_attacks)}/{len(strict_attacks)}",
            "strict_gate_state": result["strict_nonpromotion"],
        }
        print(json.dumps(audit, sort_keys=True, indent=2, allow_nan=False))
        return 0
    except Exception as error:
        print("ROUND88_PULLBACK_VERIFY_ERROR", error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
