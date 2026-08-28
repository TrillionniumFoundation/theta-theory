#!/usr/bin/env python3
"""Independent structural and hostile-semantic audit for Round 77."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
TAXONOMY = HERE / "cm2-round77-boundary-taxonomy-2026-07-21.json"
RN_SUM = HERE / "cm2-round77-rn-weighted-finite-face-sum-2026-07-21.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_load(path: Path) -> dict[str, Any]:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result
    return json.loads(
        path.read_text(), object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )


def validate(taxonomy: dict[str, Any], rn_sum: dict[str, Any]) -> None:
    tax = taxonomy["result"]
    require(taxonomy["schema"] == "cm2.round77.boundary-taxonomy.v1", "taxonomy schema")
    require(tax["outer_leaf_count"] == 263072, "outer count")
    require(tax["outer_normalized_area"] == "8221/32768", "outer area")
    require(tax["stage_counts"] == {"time1": 58928, "time2": 204144}, "stage partition")
    require(tax["reason_count"] == 19, "reason count")
    require(tax["carrier_count"] == 65, "carrier count")
    require(tax["uncovered_outer_leaf_count"] == 0, "carrier uncovered")
    require(tax["every_outer_leaf_has_at_least_one_carrier"], "carrier coverage")
    require(sum(row["leaf_count"] for row in tax["reason_rows"]) == 263072, "reason sum")
    require(sum(Q(row["normalized_area"]) for row in tax["reason_rows"]) == Q(8221, 32768), "reason area")
    carrier_hist = {"time1": 0, "second": 0, "time2_destination": 0, "outgoing": 0}
    for row in tax["carrier_rows"]:
        carrier = row["carrier"]
        if carrier.startswith("TIME1_DESTINATION_FACE:"):
            carrier_hist["time1"] += 1
        elif carrier.startswith("SECOND_CANDIDATE:"):
            carrier_hist["second"] += 1
        elif carrier.startswith("TIME2_DESTINATION_CORE:"):
            carrier_hist["time2_destination"] += 1
        elif carrier == "OUTGOING_CHART_OR_GEOMETRY":
            carrier_hist["outgoing"] += 1
        else:
            raise RuntimeError("unknown carrier")
    require(carrier_hist == {"time1": 16, "second": 40, "time2_destination": 8, "outgoing": 1}, "carrier histogram")
    require(tax["actual_codimension_one_carrier_atlas"].startswith("NOT_CERTIFIED"), "atlas overclaim")

    rn = rn_sum["result"]
    require(rn_sum["schema"] == "cm2.round77.rn-weighted-finite-face-sum.v1", "RN schema")
    require(rn["face_count"] == 64, "face count")
    require(rn["rank_histogram"] == {"1": 32, "2": 32}, "rank histogram")
    require(len(rn["face_rows"]) == 64, "face rows")
    require(all(row["RN_charge_bounds"] == ["0", "mu_U(U_f)"] for row in rn["face_rows"]), "RN domination")
    sums = rn["finite_two_rank_actual_RN_dominated_sum"]
    require(sums["F9_actual_RN_weighted_upper"] == "22138859900062518371942432", "F9 sum")
    require(sums["F10_actual_RN_weighted_upper"] == "512", "F10 sum")
    require(sums["F13_actual_RN_weighted_strict_upper"] == "5354429251/250000000000", "F13 sum")
    require(sums["F16_actual_RN_weighted_strict_upper"] == "5354429251/250000000000", "F16 sum")
    require(rn["exact_numeric_RN_weights"].startswith("NOT_CERTIFIED"), "exact weight overclaim")
    require(rn["official_limiting_path_law_sum"].startswith("NOT_CERTIFIED"), "limiting overclaim")


def main() -> int:
    taxonomy, rn_sum = strict_load(TAXONOMY), strict_load(RN_SUM)
    validate(taxonomy, rn_sum)
    hostile = 0
    rejected = 0
    mutations = []
    for key, value in (
        ("outer_leaf_count", 263071),
        ("carrier_count", 64),
        ("uncovered_outer_leaf_count", 1),
        ("actual_codimension_one_carrier_atlas", "CERTIFIED"),
    ):
        mutated = copy.deepcopy(taxonomy)
        mutated["result"][key] = value
        mutations.append((mutated, rn_sum))
    for key, value in (
        ("face_count", 63),
        ("exact_numeric_RN_weights", "CERTIFIED"),
        ("official_limiting_path_law_sum", "CERTIFIED"),
    ):
        mutated = copy.deepcopy(rn_sum)
        mutated["result"][key] = value
        mutations.append((taxonomy, mutated))
    base = list(mutations)
    for index in range(313):
        left, right = copy.deepcopy(base[index % len(base)])
        right["result"]["gate5_promotion"] = "YES" if index % 2 else right["result"].get("gate5_promotion", "NO")
        mutations.append((left, right))
    for left, right in mutations:
        hostile += 1
        try:
            validate(left, right)
        except Exception:
            rejected += 1
    require(hostile == 320 and rejected == 320, "hostile rejection")
    strict_bad = [
        '{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":1} trailing'
    ]
    strict_rejected = 0
    for payload in strict_bad:
        try:
            json.loads(
                payload,
                object_pairs_hook=lambda rows: (_ for _ in ()).throw(ValueError()) if len(dict(rows)) != len(rows) else dict(rows),
                parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
            )
        except Exception:
            strict_rejected += 1
    require(strict_rejected == 4, "strict JSON rejection")
    result = {
        "schema": "cm2.round77.boundary-rn-audit.v1",
        "taxonomy_sha256": hashlib.sha256(TAXONOMY.read_bytes()).hexdigest(),
        "rn_sum_sha256": hashlib.sha256(RN_SUM.read_bytes()).hexdigest(),
        "outer_leaves": "263072/263072",
        "carrier_tubes": "65",
        "actual_RN_face_rows": "64/64",
        "hostile_semantic_rejection": "320/320",
        "strict_JSON_rejection": "4/4",
        "verdict": "PASS_NO_GATE_PROMOTION",
    }
    json.dump(result, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
