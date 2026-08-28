#!/usr/bin/env python3
"""Independent verifier for the Round-87 finite-root seam obstruction."""
from __future__ import annotations

import copy
import json
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as cores_cert
import cm2_round85_gate3_s0_two_sided_material_window_cert as old
import cm2_round87_gate3_finite_root_seam_recut_obstruction_cert as cert


HERE = Path(__file__).resolve().parent
INPUT = HERE / "cm2-round87-gate3-finite-root-seam-recut-obstruction-2026-07-22.json"


def strict_load(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result
    value = json.loads(
        path.read_text(), object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError("top-level object")
    return value


def validate(value: dict[str, Any], expected: dict[str, Any]) -> None:
    if set(value) != {"schema", "pins", "result", "result_sha256"}:
        raise ValueError("closed top-level schema")
    if value["schema"] != cert.SCHEMA or set(value["pins"]) != set(cert.PINS):
        raise ValueError("schema or pin keys")
    if value["result_sha256"] != cert.digest(value["result"]):
        raise ValueError("result digest")
    if value["result"]["evidence_sha256"] != cert.digest(value["result"]["evidence"]):
        raise ValueError("evidence digest")
    if value != expected:
        raise ValueError("fresh producer mismatch")


def independent_recompute() -> dict[str, Any]:
    full = old.strict_load(old.FULL_CORE)
    previous = old.strict_load(cert.ROUND85_MANIFEST)
    rows: list[dict[str, Any]] = []
    old.collect(full, rows)
    positive = [row for row in rows if Q(row["source_box"]["s"][0]) == 0]
    negative = [row for row in rows if Q(row["source_box"]["s"][1]) == 0]
    up = {row["positive_atom_id"] for row in previous["result"]["evidence"]["unmatched_rows"]}
    un = {row["negative_atom_id"] for row in previous["result"]["evidence"]["negative_unmatched_rows"]}
    selected = [
        ("POSITIVE", row, negative) for row in positive if row["atom_id"] in up
    ] + [
        ("NEGATIVE", row, positive) for row in negative if row["atom_id"] in un
    ]
    contacts: Counter[str] = Counter()
    kinds: Counter[str] = Counter()
    orientations: Counter[str] = Counter()
    tangential_widths: Counter[str] = Counter()
    for _side, row, opposite in selected:
        local = []
        for other in opposite:
            if old.edge(row) != old.edge(other):
                continue
            status, dt, dp = old.relation(row, other)
            if dt > 0 and dp > 0:
                raise ValueError("positive-area intersection discovered")
            if status in {"EDGE_CONTACT_ONLY", "CORNER_CONTACT_ONLY"}:
                contacts[status] += 1
                local.append(status)
                if status == "EDGE_CONTACT_ONLY":
                    orientations["T_NORMAL" if dt == 0 else "P_NORMAL"] += 1
                    tangential_widths[str(dp if dt == 0 else dt)] += 1
        if not local:
            raise ValueError("no closure contact")
        kinds["EDGE_SEAM" if "EDGE_CONTACT_ONLY" in local else "CORNER_ONLY"] += 1

    ctx.prec = 768
    cores = cores_cert.physical_cores()
    replayed = 0
    for _side, row, _opposite in selected:
        result = cert.replay(row, cores)
        if not result["matches_frozen_row"]:
            raise ValueError("768-bit replay")
        replayed += 1
    return {
        "positive": len(positive), "negative": len(negative),
        "unmatched_positive": len(up), "unmatched_negative": len(un),
        "contacts": dict(sorted(contacts.items())),
        "kinds": dict(sorted(kinds.items())),
        "orientations": dict(sorted(orientations.items())),
        "tangential_widths": dict(sorted(tangential_widths.items())),
        "replayed_at_768_bits": replayed,
    }


def rejected(hostile: dict[str, Any], expected: dict[str, Any]) -> bool:
    try:
        validate(hostile, expected)
    except (ValueError, KeyError, TypeError, IndexError):
        return True
    return False


def main(argv: list[str]) -> int:
    path = Path(argv[1]).resolve() if len(argv) > 1 else INPUT
    value = strict_load(path)
    expected = cert.build()
    validate(value, expected)
    independent = independent_recompute()
    target = {
        "positive": 176, "negative": 176,
        "unmatched_positive": 24, "unmatched_negative": 24,
        "contacts": {"CORNER_CONTACT_ONLY": 48, "EDGE_CONTACT_ONLY": 64},
        "kinds": {"CORNER_ONLY": 8, "EDGE_SEAM": 40},
        "orientations": {"P_NORMAL": 24, "T_NORMAL": 40},
        "tangential_widths": {"1/3200": 24, "1/800": 40},
        "replayed_at_768_bits": 48,
    }
    if independent != target:
        raise ValueError("independent recomputation")

    mutations = (
        lambda x: x["result"].__setitem__("exact_repartition_can_close_remaining_rows", True),
        lambda x: x["result"].__setitem__("finite_root_local_two_sided_material_windows", "176/176"),
        lambda x: x["result"].__setitem__("Gate3", "CERTIFIED"),
        lambda x: x["result"]["minimal_required_enlargement"].__setitem__("corner_only_rows_per_side", 0),
        lambda x: x["result"]["evidence"].__setitem__("unmatched_row_total", 0),
        lambda x: x["result"]["evidence"]["positive_rows"][0].__setitem__("opposite_union_positive_area_intersection", True),
    )
    attacks = []
    for mutation in mutations:
        hostile = copy.deepcopy(value)
        mutation(hostile)
        hostile["result"]["evidence_sha256"] = cert.digest(hostile["result"]["evidence"])
        hostile["result_sha256"] = cert.digest(hostile["result"])
        attacks.append(rejected(hostile, expected))
    pin_attacks = []
    for key in value["pins"]:
        hostile = copy.deepcopy(value)
        hostile["pins"][key] = "0" * 64
        hostile["result_sha256"] = cert.digest(hostile["result"])
        pin_attacks.append(rejected(hostile, expected))
    if not all(attacks) or not all(pin_attacks):
        raise ValueError("hostile mutation accepted")

    strict_rejected = 0
    temporary = HERE / ".round87-gate3-invalid-json.tmp"
    for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e9999}'):
        try:
            temporary.write_text(raw)
            strict_load(temporary)
        except ValueError:
            strict_rejected += 1
        finally:
            temporary.unlink(missing_ok=True)
    if strict_rejected != 4:
        raise ValueError("strict JSON suite")
    result = {
        "independent_768_bit_recomputation": independent,
        "fresh_producer_reconstruction": "EXACT_EQUALITY_VERIFIED",
        "hostile_mutations_rejected": f"{sum(attacks)}/{len(attacks)}",
        "coordinated_pin_mutations_rejected": f"{sum(pin_attacks)}/{len(pin_attacks)}",
        "strict_json_attacks_rejected": f"{strict_rejected}/4",
        "verdict": "PASS",
    }
    audit = {
        "schema": "cm2.round87.gate3-finite-root-seam-recut-obstruction-audit.v1",
        "result": result,
        "result_sha256": cert.digest(result),
    }
    json.dump(audit, sys.stdout, sort_keys=True, indent=2, allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
