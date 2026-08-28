#!/usr/bin/env python3
"""Certify that the frozen Round-69 C24 base root is not same-key invariant.

This narrow Gate-4 frontier certificate recomputes the one-step image of each
of the 176 ``s=0`` owner atoms and compares it with every owner atom in its
declared destination C24 core.  It proves escape from the registered base
root, not escape from C24 itself.
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
SCHEMA = "cm2.round84.c24-base-root-same-key-escape.v1"
FULL_CORE = HERE / "cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json"
ROUND69 = HERE / "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json"
PINS = {
    FULL_CORE.name: "f79010c757e687cec2e8d7a8d617f3d94a3814731c58e960195c69107c446ad0",
    ROUND69.name: "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json":
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py":
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
}
SEPARATION = Q(1, 100)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ValueError(label)


def collect(value: Any, output: list[dict[str, Any]]) -> None:
    if isinstance(value, dict):
        if value.get("classification") == "RETURN_AT_1_INNER" and "source_box" in value:
            output.append(value)
        for child in value.values():
            collect(child, output)
    elif isinstance(value, list):
        for child in value:
            collect(child, output)


def qarb(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def build(precision_bits: int = 512) -> dict[str, Any]:
    ctx.prec = precision_bits
    for name, expected in PINS.items():
        require(file_digest(HERE / name) == expected, f"pin: {name}")
    full = json.loads(FULL_CORE.read_text())
    round69 = json.loads(ROUND69.read_text())
    rows: list[dict[str, Any]] = []
    collect(full, rows)
    owner = [row for row in rows if Q(row["source_box"]["s"][0]) == 0]
    require(len(rows) == 4216 and len(owner) == 176, "frozen atom census")
    require(round69["result"]["actual_base_s_return_root"]["owned_by_lower_closed_upper_open_rule"] == 176,
            "Round69 owner count")

    cores = {return_cert.core_id(core): core for core in core_cert.physical_cores()}
    by_source: dict[str, list[dict[str, Any]]] = {}
    for row in owner:
        by_source.setdefault(row["source_core_id"], []).append(row)

    comparison_rows: list[dict[str, Any]] = []
    landing_rows: list[dict[str, Any]] = []
    for row in sorted(owner, key=lambda item: item["atom_id"]):
        source = cores[row["source_core_id"]]
        box = row["source_box"]
        atom = return_cert.Atom(
            0, source, *map(Q, box["t"]), *map(Q, box["p"]), *map(Q, box["s"]), "",
        )
        geometry = return_cert.atom_geometry(atom)
        require(geometry is not None, "one-step collision geometry")
        destination = cores[row["destination_core_id"]]
        landing_t = return_cert.chart_tests(
            destination.chart_id.split(":")[1], geometry["normal_x"], geometry["normal_y"]
        )[0]
        landing_p = geometry["p_target"]
        require(destination.source == source.target_id[0], "destination obstacle")
        require(
            bool(landing_t > qarb(destination.t0))
            and bool(landing_t < qarb(destination.t1))
            and bool(landing_p > qarb(destination.p0))
            and bool(landing_p < qarb(destination.p1)),
            "strict destination-core interior",
        )
        local_rows: list[dict[str, Any]] = []
        for target in sorted(by_source[row["destination_core_id"]], key=lambda item: item["atom_id"]):
            p0, p1 = map(Q, target["source_box"]["p"])
            below = qarb(p0) - landing_p
            above = landing_p - qarb(p1)
            if bool(below > qarb(SEPARATION)):
                separator, gap = "landing_p_below_target_p0", below
            elif bool(above > qarb(SEPARATION)):
                separator, gap = "landing_p_above_target_p1", above
            else:
                raise ValueError("same-key depth2 separation")
            witness = {
                "landing_atom_id": row["atom_id"],
                "target_atom_id": target["atom_id"],
                "destination_core_id": row["destination_core_id"],
                "separator": separator,
                "gap_enclosure": str(gap),
                "gap_strict_lower": "1/100",
            }
            local_rows.append(witness)
            comparison_rows.append(witness)
        require(local_rows, "destination owner rows")
        landing_rows.append({
            "landing_atom_id": row["atom_id"],
            "source_core_id": row["source_core_id"],
            "destination_core_id": row["destination_core_id"],
            "landing_t_enclosure": str(landing_t),
            "landing_p_enclosure": str(landing_p),
            "compared_destination_owner_atoms": len(local_rows),
            "all_destination_owner_atoms_strictly_separated": True,
        })

    histogram = Counter(item["separator"] for item in comparison_rows)
    require(len(landing_rows) == 176 and len(comparison_rows) == 1360, "comparison census")
    require(histogram == {
        "landing_p_above_target_p1": 680,
        "landing_p_below_target_p0": 680,
    }, "separator histogram")
    evidence = {
        "precision_bits": precision_bits,
        "registered_base_owner_atom_count": 176,
        "registered_directed_core_edge_count": 16,
        "landing_atom_count": len(landing_rows),
        "same_destination_core_atom_comparison_count": len(comparison_rows),
        "separator_histogram": dict(sorted(histogram.items())),
        "uniform_coordinate_gap_strict_lower": "1/100",
        "landing_rows": landing_rows,
        "comparison_rows": comparison_rows,
    }
    result = {
        "status": "CERTIFIED_ROUND69_BASE_ROOT_ESCAPES_ITS_SAME_KEY_OWNER_UNION_AT_DEPTH2",
        "scope": "the 176 lower-closed s=0 owner atoms frozen in Round69",
        "registered_base_root_depth2_self_intersection_count": 0,
        "same_key_all_depth_stable_material_crosswalk_on_round69_root": "IMPOSSIBLE_WITHOUT_RESELECTING_OR_ENLARGING_THE_BASE_ROOT",
        "gate4_field_progress": {
            "field_1_all_depth_positive_stable_base": "NOT_CERTIFIED__CURRENT_BASE_ROOT_PROVED_NONINVARIANT_AT_DEPTH2",
            "field_4_same_branch_commuting_square_family": "PARTIAL_FIXED_DEPTH_ONLY",
            "complete_fields": "1/7",
            "Gate4": "NOT_CERTIFIED",
        },
        "strict_nonclaims": {
            "no_claim_that_all_C24_points_escape": True,
            "no_claim_that_no_other_C24_subroot_is_invariant": True,
            "no_stable_holonomy_or_marker_law_constructed": True,
        },
        "evidence": evidence,
        "evidence_sha256": digest(evidence),
    }
    return {"schema": SCHEMA, "pins": dict(PINS), "result": result, "result_sha256": digest(result)}


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, indent=2, allow_nan=False))
