#!/usr/bin/env python3
"""Verifier for the exact Round-85 finite-root two-sided material audit."""
from __future__ import annotations

import copy
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_round85_gate3_s0_two_sided_material_window_cert as cert


HERE = Path(__file__).resolve().parent
INPUT = HERE / "cm2-round85-gate3-s0-two-sided-material-window-2026-07-22.json"


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def strict_load(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(), object_pairs_hook=unique,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError("top-level object")
    def walk(item: Any) -> None:
        if isinstance(item, float) and not math.isfinite(item):
            raise ValueError("nonfinite JSON")
        if isinstance(item, dict):
            for child in item.values(): walk(child)
        elif isinstance(item, list):
            for child in item: walk(child)
    walk(value)
    return value


def validate(value: Any, expected: dict[str, Any]) -> None:
    if not isinstance(value, dict) or set(value) != {"schema", "pins", "result", "result_sha256"}:
        raise ValueError("closed schema")
    if value["result_sha256"] != cert.digest(value["result"]):
        raise ValueError("result digest")
    if value["result"]["evidence_sha256"] != cert.digest(value["result"]["evidence"]):
        raise ValueError("evidence digest")
    if value != expected:
        raise ValueError("fresh exact reconstruction")


def independent_counts() -> dict[str, Any]:
    full = cert.strict_load(cert.FULL_CORE)
    rows: list[dict[str, Any]] = []
    cert.collect(full, rows)
    positive = [row for row in rows if Q(row["source_box"]["s"][0]) == 0]
    negative = [row for row in rows if Q(row["source_box"]["s"][1]) == 0]
    neg_by_edge: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in negative:
        neg_by_edge[cert.edge(row)].append(row)
    relations: Counter[str] = Counter()
    covered = exact = partial = unmatched = 0
    negative_covered = 0
    minimum_radius: Q | None = None
    for pos in positive:
        local = []
        for neg in neg_by_edge[cert.edge(pos)]:
            status, dt, dp = cert.relation(pos, neg)
            relations[status] += 1
            if dt > 0 and dp > 0:
                radius = min(
                    dt / 2, dp / 2,
                    Q(pos["source_box"]["s"][1]), -Q(neg["source_box"]["s"][0]),
                )
                local.append((radius, status))
        if not local:
            unmatched += 1
            continue
        covered += 1
        if any(status == "EXACT_BOX" for _, status in local): exact += 1
        else: partial += 1
        best = max(radius for radius, _ in local)
        minimum_radius = best if minimum_radius is None else min(minimum_radius, best)
    for neg in negative:
        if any(
            cert.relation(pos, neg)[1] > 0 and cert.relation(pos, neg)[2] > 0
            for pos in positive if cert.edge(pos) == cert.edge(neg)
        ):
            negative_covered += 1
    return {
        "positive": len(positive), "negative": len(negative),
        "comparisons": sum(relations.values()),
        "relations": dict(sorted(relations.items())),
        "covered": covered, "exact": exact, "partial": partial,
        "unmatched": unmatched, "minimum_radius": str(minimum_radius),
        "negative_covered": negative_covered,
        "negative_unmatched": len(negative) - negative_covered,
    }


def rejected(hostile: dict[str, Any], expected: dict[str, Any]) -> bool:
    try: validate(hostile, expected)
    except (ValueError, KeyError, TypeError, IndexError): return True
    return False


def main(argv: list[str]) -> int:
    path = Path(argv[1]).resolve() if len(argv) > 1 else INPUT
    value = strict_load(path)
    expected = cert.build()
    validate(value, expected)
    independent = independent_counts()
    if independent != {
        "positive": 176, "negative": 176, "comparisons": 2504,
        "relations": {
            "CORNER_CONTACT_ONLY": 320, "DISJOINT": 1640,
            "EDGE_CONTACT_ONLY": 376, "EXACT_BOX": 104,
            "PARTIAL_POSITIVE_AREA": 64,
        },
        "covered": 152, "exact": 104, "partial": 48,
        "unmatched": 24, "minimum_radius": "1/6400",
        "negative_covered": 152, "negative_unmatched": 24,
    }:
        raise ValueError("independent rational recomputation")

    attacks = []
    mutations = (
        lambda x: x["result"].__setitem__("full_176_owner_row_two_sided_cover", "CERTIFIED"),
        lambda x: x["result"].__setitem__("Gate3", "CERTIFIED"),
        lambda x: x["result"]["evidence"].__setitem__("unmatched_positive_owner_row_count", 0),
        lambda x: x["result"]["evidence"]["window_rows"][0].__setitem__("certified_L_infinity_radius", "1"),
        lambda x: x["result"]["evidence"]["unmatched_rows"][0].__setitem__("positive_area_counterpart_count", 1),
        lambda x: x.__setitem__("extra_claim", "CERTIFIED"),
    )
    for mutation in mutations:
        hostile = copy.deepcopy(value); mutation(hostile)
        hostile["result"]["evidence_sha256"] = cert.digest(hostile["result"]["evidence"])
        hostile["result_sha256"] = cert.digest(hostile["result"])
        attacks.append(rejected(hostile, expected))
    pin_attacks = []
    for key in value["pins"]:
        hostile = copy.deepcopy(value)
        hostile["pins"][key] = "0" * 64
        # Rehashing the result cannot mask a coordinated provenance change.
        hostile["result_sha256"] = cert.digest(hostile["result"])
        pin_attacks.append(rejected(hostile, expected))
    if not all(pin_attacks):
        raise ValueError("coordinated pin mutation accepted")
    if not all(attacks):
        raise ValueError("hostile mutation accepted")

    strict_rejected = 0
    for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e9999}'):
        temporary = HERE / ".round85-invalid-json.tmp"
        try:
            temporary.write_text(raw)
            strict_load(temporary)
        except ValueError:
            strict_rejected += 1
        finally:
            temporary.unlink(missing_ok=True)
    if strict_rejected != 4:
        raise ValueError("strict JSON suite")

    audit_result = {
        "exact_rational_recomputation": independent,
        "fresh_producer_reconstruction": "EXACT_EQUALITY_VERIFIED",
        "hostile_mutations_rejected": f"{sum(attacks)}/{len(attacks)}",
        "coordinated_pin_mutations_rejected": f"{sum(pin_attacks)}/{len(pin_attacks)}",
        "strict_json_attacks_rejected": f"{strict_rejected}/4",
        "verdict": "PASS",
    }
    audit = {
        "schema": "cm2.round85.gate3-s0-two-sided-material-window-audit.v1",
        "result": audit_result,
        "result_sha256": cert.digest(audit_result),
    }
    json.dump(audit, sys.stdout, sort_keys=True, indent=2, allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
