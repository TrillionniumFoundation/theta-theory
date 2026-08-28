#!/usr/bin/env python3
"""Verifier for the Round-85 finite-root Gate-5 field frontier."""
from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path
from typing import Any

import cm2_round85_gate5_finite_root_operator_field_frontier_cert as cert


HERE = Path(__file__).resolve().parent
INPUT = HERE / "cm2-round85-gate5-finite-root-operator-field-frontier-2026-07-22.json"


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result: raise ValueError("duplicate key")
        result[key] = value
    return result


def loads_strict(raw: str) -> Any:
    value = json.loads(raw, object_pairs_hook=unique,
                       parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    def walk(item: Any) -> None:
        if isinstance(item, float) and not math.isfinite(item): raise ValueError("nonfinite")
        if isinstance(item, dict):
            for child in item.values(): walk(child)
        elif isinstance(item, list):
            for child in item: walk(child)
    walk(value); return value


def validate(value: Any, expected: dict[str, Any]) -> None:
    if not isinstance(value, dict) or set(value) != {"schema", "pins", "result", "result_sha256"}:
        raise ValueError("closed schema")
    if value["result_sha256"] != cert.digest(value["result"]): raise ValueError("result digest")
    if value["result"]["evidence_sha256"] != cert.digest(value["result"]["evidence"]):
        raise ValueError("evidence digest")
    if value != expected: raise ValueError("fresh exact reconstruction")


def rejected(hostile: dict[str, Any], expected: dict[str, Any]) -> bool:
    try: validate(hostile, expected)
    except (ValueError, KeyError, TypeError, IndexError): return True
    return False


def main(argv: list[str]) -> int:
    path = Path(argv[1]).resolve() if len(argv) > 1 else INPUT
    value = loads_strict(path.read_text())
    expected = cert.build(); validate(value, expected)
    evidence = value["result"]["evidence"]
    if len(evidence["attachment_rows"]) != 152 or len({row["atom_id"] for row in evidence["attachment_rows"]}) != 152:
        raise ValueError("attachment key census")
    if any(row["candidate_local_maturity"] != "13/18" for row in evidence["attachment_rows"]):
        raise ValueError("packet maturity")
    if [row["same_key_slot_count"] for row in evidence["field_rows"]] != [0] * 5:
        raise ValueError("F14--F18 frontier")

    mutations = (
        lambda x: x["result"].__setitem__("candidate_local_maturity_after", "18/18"),
        lambda x: x["result"].__setitem__("complete_18_field_operator_blocks", 1),
        lambda x: x["result"].__setitem__("global_Gate5", "CERTIFIED"),
        lambda x: x["result"]["evidence"]["same_key_F14_through_F18_slot_counts"].__setitem__("F16", 152),
        lambda x: x["result"]["evidence"]["attachment_rows"][0].__setitem__("F13_trace_pair_count", 2),
        lambda x: x["result"]["evidence"]["field_rows"][0].__setitem__("status", "CERTIFIED"),
        lambda x: x.__setitem__("extra_claim", "CERTIFIED"),
    )
    attacks = []
    for mutation in mutations:
        hostile = copy.deepcopy(value); mutation(hostile)
        hostile["result"]["evidence_sha256"] = cert.digest(hostile["result"]["evidence"])
        hostile["result_sha256"] = cert.digest(hostile["result"])
        attacks.append(rejected(hostile, expected))
    pin_attacks = []
    for key in value["pins"]:
        hostile = copy.deepcopy(value); hostile["pins"][key] = "0" * 64
        pin_attacks.append(rejected(hostile, expected))
    if not all(attacks) or not all(pin_attacks): raise ValueError("hostile mutation")
    strict_rejected = 0
    for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e9999}'):
        try: loads_strict(raw)
        except ValueError: strict_rejected += 1
    if strict_rejected != 4: raise ValueError("strict JSON")

    audit_result = {
        "fresh_producer_reconstruction": "EXACT_EQUALITY_VERIFIED",
        "same_key_material_packet_count": 152,
        "same_key_F10_F13_empty_slot_counts": {"F10": 152, "F13": 152},
        "same_key_F14_through_F18_slot_counts": {f"F{index}": 0 for index in range(14, 19)},
        "candidate_local_maturity": "13/18_UNCHANGED",
        "hostile_mutations_rejected": f"{sum(attacks)}/{len(attacks)}",
        "coordinated_pin_mutations_rejected": f"{sum(pin_attacks)}/{len(pin_attacks)}",
        "strict_json_attacks_rejected": f"{strict_rejected}/4",
        "verdict": "PASS",
    }
    audit = {"schema": "cm2.round85.gate5-finite-root-operator-field-frontier-audit.v1",
             "result": audit_result, "result_sha256": cert.digest(audit_result)}
    json.dump(audit, sys.stdout, sort_keys=True, indent=2, allow_nan=False); sys.stdout.write("\n")
    return 0


if __name__ == "__main__": raise SystemExit(main(sys.argv))
