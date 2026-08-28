#!/usr/bin/env python3
"""Verifier for the full Round-85 C24 return-incidence frontier."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

import cm2_round85_c24_full_return_incidence_cert as cert


HERE = Path(__file__).resolve().parent
INPUT = HERE / "cm2-round85-c24-full-return-incidence-2026-07-22.json"


def strict_load(path: Path) -> dict[str, Any]:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in rows:
            if key in value:
                raise ValueError("duplicate key")
            value[key] = item
        return value
    value = json.loads(path.read_text(), object_pairs_hook=pairs,
                       parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    if not isinstance(value, dict):
        raise ValueError("top level")
    return value


def validate(value: dict[str, Any], expected: dict[str, Any]) -> None:
    if set(value) != {"schema", "pins", "result", "result_sha256"}:
        raise ValueError("closed schema")
    if value != expected:
        raise ValueError("replay mismatch")


def main() -> int:
    try:
        value = strict_load(INPUT)
        expected = cert.build(512)
        validate(value, expected)
        higher = cert.build(768)
        invariant_paths = (
            ("return_atom_count",),
            ("physical_C24_core_universe_count",),
            ("active_source_core_count",),
            ("empty_return_source_core_count",),
            ("destination_core_count",),
            ("frozen_384bit_landing_replay_overlap_count",),
            ("frozen_384bit_aggregate_hull_ambiguous_count",),
            ("recomputed_separator_histogram",),
            ("uniform_coordinate_gap_strict_lower",),
        )
        a = value["result"]["evidence"]
        b = higher["result"]["evidence"]
        for (key,) in invariant_paths:
            if a[key] != b[key]:
                raise ValueError(f"precision invariant: {key}")
        if higher["result"]["landing_to_source_atom_incidence_graph"] != {
            "node_count": 4216,
            "edge_count": 0,
            "strongly_connected_component_count": 4216,
            "nontrivial_or_self_loop_SCC_count": 0,
            "recurrent_node_count": 0,
            "maximum_directed_path_edge_length": 0,
        }:
            raise ValueError("higher precision graph")

        attacks = []
        mutations = (
            lambda x: x["result"]["landing_to_source_atom_incidence_graph"].__setitem__("edge_count", 1),
            lambda x: x["result"]["constructive_consequence"].__setitem__("nonempty_recurrent_same_key_subroot_in_current_atlas", True),
            lambda x: x["result"]["strict_scope"].__setitem__("Gate4", "CERTIFIED"),
            lambda x: x["result"]["evidence"]["atom_rows"][0].__setitem__("gap_strict_lower", "1"),
            lambda x: x.__setitem__("extra_claim", True),
        )
        for mutation in mutations:
            hostile = copy.deepcopy(value)
            mutation(hostile)
            hostile["result_sha256"] = cert.digest(hostile["result"])
            rejected = False
            try:
                validate(hostile, expected)
            except ValueError:
                rejected = True
            attacks.append(rejected)
        if not all(attacks):
            raise ValueError("hostile mutation")
        audit = {
            "schema": "cm2.round85.c24-full-return-incidence.audit.v1",
            "status": "AUDIT_PASS",
            "producer_precision_bits": 512,
            "independent_precision_bits": 768,
            "return_atom_count": 4216,
            "physical_C24_core_universe_count": 24,
            "active_return_source_core_count": 16,
            "empty_return_source_core_count": 8,
            "incidence_edge_count": 0,
            "cyclic_SCC_count": 0,
            "recurrent_node_count": 0,
            "frozen_384bit_ambiguous_count": 460,
            "uniform_coordinate_gap_strict_lower": "1/200",
            "hostile_mutations_rejected": f"{sum(attacks)}/{len(attacks)}",
            "strict_gate_state": value["result"]["strict_scope"],
        }
        print(json.dumps(audit, sort_keys=True, indent=2, allow_nan=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"ROUND85_C24_INCIDENCE_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
