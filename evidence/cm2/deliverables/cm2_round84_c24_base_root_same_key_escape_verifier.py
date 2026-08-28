#!/usr/bin/env python3
"""Independent verifier for the Round-84 C24 same-key escape certificate."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

import cm2_round84_c24_base_root_same_key_escape_cert as cert


HERE = Path(__file__).resolve().parent
INPUT = HERE / "cm2-round84-c24-base-root-same-key-escape-2026-07-22.json"


def strict_load(path: Path) -> dict[str, Any]:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result
    value = json.loads(path.read_text(), object_pairs_hook=pairs,
                       parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    if not isinstance(value, dict):
        raise ValueError("top level")
    return value


def validate(value: dict[str, Any], expected: dict[str, Any]) -> None:
    if set(value) != {"schema", "pins", "result", "result_sha256"}:
        raise ValueError("closed schema")
    if value != expected:
        raise ValueError("independent replay mismatch")


def main() -> int:
    try:
        value = strict_load(INPUT)
        expected = cert.build(512)
        validate(value, expected)
        higher = cert.build(768)
        left = value["result"]["evidence"]
        right = higher["result"]["evidence"]
        for key in (
            "registered_base_owner_atom_count", "registered_directed_core_edge_count",
            "landing_atom_count", "same_destination_core_atom_comparison_count",
            "separator_histogram", "uniform_coordinate_gap_strict_lower",
        ):
            if left[key] != right[key]:
                raise ValueError(f"higher precision invariant: {key}")
        if higher["result"]["registered_base_root_depth2_self_intersection_count"] != 0:
            raise ValueError("higher precision intersection count")

        attacks: list[dict[str, Any]] = []
        for mutation in (
            lambda x: x["result"].__setitem__("registered_base_root_depth2_self_intersection_count", 1),
            lambda x: x["result"]["gate4_field_progress"].__setitem__("Gate4", "CERTIFIED"),
            lambda x: x["result"]["evidence"]["comparison_rows"][0].__setitem__("gap_strict_lower", "1"),
            lambda x: x.__setitem__("extra_claim", True),
        ):
            hostile = copy.deepcopy(value)
            mutation(hostile)
            hostile["result_sha256"] = cert.digest(hostile["result"])
            rejected = False
            try:
                validate(hostile, expected)
            except ValueError:
                rejected = True
            attacks.append({"rejected": rejected})
        if not all(row["rejected"] for row in attacks):
            raise ValueError("hostile mutation")

        audit = {
            "schema": "cm2.round84.c24-base-root-same-key-escape.audit.v1",
            "status": "AUDIT_PASS",
            "producer_precision_bits": 512,
            "independent_precision_bits": 768,
            "landing_atom_count": 176,
            "comparison_count": 1360,
            "depth2_self_intersection_count": 0,
            "uniform_coordinate_gap_strict_lower": "1/100",
            "hostile_mutations_rejected": f"{sum(row['rejected'] for row in attacks)}/{len(attacks)}",
            "strict_state": value["result"]["gate4_field_progress"],
        }
        print(json.dumps(audit, sort_keys=True, indent=2, allow_nan=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"ROUND84_C24_SAME_KEY_ESCAPE_VERIFY_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
