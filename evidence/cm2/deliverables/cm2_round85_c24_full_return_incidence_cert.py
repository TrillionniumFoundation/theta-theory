#!/usr/bin/env python3
"""Full 4,216-atom C24 landing-to-source incidence frontier.

The frozen 384-bit landing enclosures leave 460 aggregate-hull comparisons
ambiguous.  Re-evaluation of the same rational atom boxes at 512 bits resolves
all of them.  Every one-step return atom lands inside its declared C24 core,
but outside the union of all one-step return source atoms in that core.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as return_cert


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round85.c24-full-return-incidence.v1"
FULL = HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
PINS = {
    FULL.name: "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",
    "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json":
        "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json":
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py":
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
}
GAP = Q(1, 200)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(value: bool, label: str) -> None:
    if not value:
        raise ValueError(label)


def qarb(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def collect(value: Any, rows: list[dict[str, Any]]) -> None:
    if isinstance(value, dict):
        if value.get("classification") == "RETURN_AT_1_INNER" and "source_box" in value:
            rows.append(value)
        for child in value.values():
            collect(child, rows)
    elif isinstance(value, list):
        for child in value:
            collect(child, rows)


def build(precision_bits: int = 512) -> dict[str, Any]:
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        require(file_digest(HERE / name) == expected, f"pin: {name}")
    document = json.loads(FULL.read_text())
    rows: list[dict[str, Any]] = []
    collect(document, rows)
    require(len(rows) == 4216 and len({row["atom_id"] for row in rows}) == 4216,
            "return atom census")
    cores = {return_cert.core_id(core): core for core in core_cert.physical_cores()}
    by_source: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_source.setdefault(row["source_core_id"], []).append(row)
    require(len(by_source) == 16, "active source core census")

    core_hulls: dict[str, dict[str, str]] = {}
    for identifier, members in by_source.items():
        core_hulls[identifier] = {
            "t0": str(min(Q(row["source_box"]["t"][0]) for row in members)),
            "t1": str(max(Q(row["source_box"]["t"][1]) for row in members)),
            "p0": str(min(Q(row["source_box"]["p"][0]) for row in members)),
            "p1": str(max(Q(row["source_box"]["p"][1]) for row in members)),
            "source_atom_count": str(len(members)),
        }

    frozen_ambiguous = 0
    replay_overlap_count = 0
    evidence_rows: list[dict[str, Any]] = []
    histogram: Counter[str] = Counter()
    for row in sorted(rows, key=lambda item: item["atom_id"]):
        source = cores[row["source_core_id"]]
        box = row["source_box"]
        atom = return_cert.Atom(
            0, source, *map(Q, box["t"]), *map(Q, box["p"]), *map(Q, box["s"]), "",
        )
        geometry = return_cert.atom_geometry(atom)
        require(geometry is not None, "collision geometry")
        destination = cores[row["destination_core_id"]]
        landing_t = return_cert.chart_tests(
            destination.chart_id.split(":")[1], geometry["normal_x"], geometry["normal_y"]
        )[0]
        landing_p = geometry["p_target"]
        require(destination.source == source.target_id[0], "destination obstacle")
        require(bool(landing_t > qarb(destination.t0)) and bool(landing_t < qarb(destination.t1))
                and bool(landing_p > qarb(destination.p0)) and bool(landing_p < qarb(destination.p1)),
                "destination core interior")
        frozen = row["output_enclosures"]
        require(arb(frozen["normal_x"]).overlaps(geometry["normal_x"])
                and arb(frozen["normal_y"]).overlaps(geometry["normal_y"])
                and arb(frozen["p_target"]).overlaps(landing_p), "frozen replay overlap")
        replay_overlap_count += 1

        hull = core_hulls[row["destination_core_id"]]
        t0, t1 = Q(hull["t0"]), Q(hull["t1"])
        p0, p1 = Q(hull["p0"]), Q(hull["p1"])
        frozen_p = arb(frozen["p_target"])
        frozen_t = return_cert.chart_tests(
            destination.chart_id.split(":")[1], arb(frozen["normal_x"]), arb(frozen["normal_y"])
        )[0]
        frozen_separated = (
            bool(qarb(t0) - frozen_t > 0) or bool(frozen_t - qarb(t1) > 0)
            or bool(qarb(p0) - frozen_p > 0) or bool(frozen_p - qarb(p1) > 0)
        )
        if not frozen_separated:
            frozen_ambiguous += 1
        below = qarb(p0) - landing_p
        above = landing_p - qarb(p1)
        if bool(below > qarb(GAP)):
            separator, gap = "landing_p_below_destination_return_hull", below
        elif bool(above > qarb(GAP)):
            separator, gap = "landing_p_above_destination_return_hull", above
        else:
            raise ValueError("destination return hull separation")
        histogram[separator] += 1
        evidence_rows.append({
            "atom_id": row["atom_id"],
            "source_core_id": row["source_core_id"],
            "destination_core_id": row["destination_core_id"],
            "separator": separator,
            "gap_enclosure": str(gap),
            "gap_strict_lower": "1/200",
        })

    require(frozen_ambiguous == 460, "frozen ambiguity count")
    require(replay_overlap_count == 4216, "frozen replay count")
    require(histogram == {
        "landing_p_above_destination_return_hull": 2108,
        "landing_p_below_destination_return_hull": 2108,
    }, "separator histogram")
    evidence = {
        "precision_bits": precision_bits,
        "return_atom_count": 4216,
        "physical_C24_core_universe_count": 24,
        "active_source_core_count": 16,
        "empty_return_source_core_count": 8,
        "destination_core_count": 16,
        "frozen_384bit_landing_replay_overlap_count": replay_overlap_count,
        "frozen_384bit_aggregate_hull_ambiguous_count": frozen_ambiguous,
        "recomputed_separator_histogram": dict(sorted(histogram.items())),
        "uniform_coordinate_gap_strict_lower": "1/200",
        "core_return_source_hulls": core_hulls,
        "atom_rows": evidence_rows,
    }
    result = {
        "status": "CERTIFIED_EMPTY_LANDING_TO_RETURN_SOURCE_INCIDENCE_GRAPH",
        "landing_to_source_atom_incidence_graph": {
            "node_count": 4216,
            "edge_count": 0,
            "strongly_connected_component_count": 4216,
            "nontrivial_or_self_loop_SCC_count": 0,
            "recurrent_node_count": 0,
            "maximum_directed_path_edge_length": 0,
        },
        "constructive_consequence": {
            "nonempty_recurrent_same_key_subroot_in_current_atlas": False,
            "required_repair": "enlarge to survivor atoms and variable return times, or select a different base registry",
            "graph_connectivity_is_not_called_a_stable_plaque": True,
        },
        "strict_scope": {
            "only_the_frozen_4216_one_step_RETURN_AT_1_INNER_atoms": True,
            "does_not_exclude_later_return_via_SURVIVE_THROUGH_1_INNER": True,
            "does_not_exclude_another_C24_subroot": True,
            "Gate2": "NOT_CERTIFIED__0_OF_17",
            "Gate4": "NOT_CERTIFIED__1_OF_7",
        },
        "evidence": evidence,
        "evidence_sha256": digest(evidence),
    }
    return {"schema": SCHEMA, "pins": dict(PINS), "result": result, "result_sha256": digest(result)}


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2, allow_nan=False))
