#!/usr/bin/env python3
"""Cross-implementation verifier and coherent mutation attacks for P0-A 192+24."""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import gzip
import json
from pathlib import Path
from typing import Any


GRAPH1_ROUTE = "EXACT_NONINCIDENCE_CROSS_CHART_T0_GLOBAL_PHASE_MISMATCH"
GRAPH2_ROUTE = "EXACT_NONINCIDENCE__T0_GLOBAL_PHASE_POSITION_MISMATCH"
LOWER2_ROUTE = (
    "EXACT_NONEDGE__TARGET_OPEN_SUPPORT_EXCLUDES_CONTACT__"
    "COMPLETE_T0_OWNER_COVER_HAS_SOURCE_SHEET_COMPONENT"
)


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def load(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream]


def normal(chart: str) -> tuple[Fraction, Fraction]:
    need(chart.startswith("G:"), "source-G chart")
    cell = chart.split(":", 1)[1]
    need(cell in {"E", "W", "N", "S"}, "four charts")
    return {
        "E": (Fraction(1), Fraction(0)), "W": (Fraction(-1), Fraction(0)),
        "N": (Fraction(0), Fraction(1)), "S": (Fraction(0), Fraction(-1)),
    }[cell]


def graph1(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        if row.get("route") != GRAPH1_ROUTE:
            continue
        evidence = row["support_evidence"]["exact_global_phase_equation"]
        output.append({
            "sheet_member_id": row["sheet_member_id"], "side_member_id": row["side_member_id"],
            "sheet_chart": row["support_evidence"]["sheet_chart"], "side_chart": row["support_evidence"]["side_chart"],
            "sheet_normal": evidence["sheet_primitive_normal"], "side_normal": evidence["side_primitive_normal"],
            "sheet_position": evidence["sheet_primitive_position"], "side_position": evidence["side_primitive_position"],
        })
    return output


def graph2(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{key: row[key] for key in (
        "sheet_member_id", "side_member_id", "sheet_chart", "side_chart",
        "sheet_normal", "side_normal", "sheet_position", "side_position",
    )} for row in rows if row.get("route") == GRAPH2_ROUTE]


def verify_graph(rows: list[dict[str, Any]]) -> None:
    need(len(rows) == 192, "192 rows")
    keys = [(row["sheet_member_id"], row["side_member_id"]) for row in rows]
    need(len(set(keys)) == 192, "unique graph pairs")
    radius = Fraction(9, 25)
    for row in rows:
        sc, tc = row["sheet_chart"], row["side_chart"]
        need(sc != tc, "cross chart")
        sn, tn = normal(sc), normal(tc)
        need(sn != tn, "normal mismatch")
        need(row["sheet_normal"] == [str(x) for x in sn], "sheet normal equation")
        need(row["side_normal"] == [str(x) for x in tn], "side normal equation")
        need(row["sheet_position"] == [str(radius*x) for x in sn], "sheet position equation")
        need(row["side_position"] == [str(radius*x) for x in tn], "side position equation")
        need(row["sheet_position"] != row["side_position"], "position nonincidence")


def lower1(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        handoff = row["layer_B_lower_owner_physical_support_component_handoff"]
        output.append({
            "key": [row["source_sheet_member_id"], row["target_registry_occurrence_id"], row["R291_disposition_row_id"], row["R291_physical_witness_cell_index"]],
            "chart": row["chart"], "point": row["contact_locus"]["representative_t_p_s"],
            "target_bounds": row["target_normalized_support_ast"]["bounds"],
            "covering_members": handoff["covering_member_ids"],
            "covering_member_count": handoff["covering_member_count"],
            "owner_component": handoff["unique_C15_component_id"],
            "source_component": row["source_sheet_component_id"], "target_component": row["target_component_id"],
            "witness": bool(handoff["cross_component_same_physical_point_witness"]),
        })
    return output


def lower2(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        if row.get("route") != LOWER2_ROUTE:
            continue
        output.append({
            "key": [row["sheet_member_id"], row["target_registry_occurrence_id"], row["R291_disposition_row_id"], row["physical_witness_cell_index"]],
            "chart": row["sheet_chart"], "point": row["closure_contact_point_t_p_s"],
            "target_bounds": row["target_normalized_support_ast"]["bounds"],
            "covering_members": row["complete_t0_owner_covering_member_ids"],
            "covering_member_count": row["complete_t0_owner_covering_member_count"],
            "owner_component": row["complete_t0_owner_unique_component_id"],
            "source_component": row["sheet_component_id"], "target_component": row["target_component_id"],
            "witness": False,
        })
    return output


def verify_lower(rows: list[dict[str, Any]]) -> None:
    need(len(rows) == 24, "24 lower rows")
    need(len({tuple(row["key"]) for row in rows}) == 24, "unique lower keys")
    cover_census = {1: 0, 2: 0}
    for row in rows:
        need(row["point"][0] == "0", "contact exact t0")
        p = Fraction(row["point"][1]); bounds = [Fraction(x) for x in row["target_bounds"]]
        need(bounds[0] == 0 < bounds[1], "target positive-open t interval")
        need(p in {bounds[2], bounds[3]}, "contact on strict p endpoint")
        need(row["covering_member_count"] == len(row["covering_members"]), "cover count")
        need(len(set(row["covering_members"])) == row["covering_member_count"], "unique cover members")
        need(row["covering_member_count"] in {1, 2}, "one/two sheet cover")
        cover_census[row["covering_member_count"]] += 1
        need(row["owner_component"] == row["source_component"], "owner is source component")
        need(row["owner_component"] != row["target_component"], "target is not t0 owner")
        need(row["witness"] is False, "no cross-component witness")
    need(cover_census == {1: 8, 2: 16}, "lower cover census")


def rejected(fn, rows: list[dict[str, Any]]) -> bool:
    try:
        fn(rows)
    except (Reject, KeyError, ValueError, TypeError):
        return True
    return False


def attack_suite(graph: list[dict[str, Any]], lower: list[dict[str, Any]]) -> dict[str, bool]:
    attacks: dict[str, bool] = {}
    attacks["graph_row_omission"] = rejected(verify_graph, graph[:-1])
    attacks["graph_row_duplication"] = rejected(verify_graph, graph[:-1] + [graph[0]])
    mutant = copy.deepcopy(graph); mutant[0]["side_chart"] = mutant[0]["sheet_chart"]
    attacks["graph_cross_chart_mutation"] = rejected(verify_graph, mutant)
    mutant = copy.deepcopy(graph); mutant[0]["side_normal"] = mutant[0]["sheet_normal"]
    attacks["graph_normal_mutation"] = rejected(verify_graph, mutant)
    mutant = copy.deepcopy(graph); mutant[0]["side_position"] = mutant[0]["sheet_position"]
    attacks["graph_position_mutation"] = rejected(verify_graph, mutant)
    attacks["lower_row_omission"] = rejected(verify_lower, lower[:-1])
    attacks["lower_row_duplication"] = rejected(verify_lower, lower[:-1] + [lower[0]])
    mutant = copy.deepcopy(lower); mutant[0]["target_bounds"][0] = "-1/1000"
    attacks["lower_open_t_endpoint_mutation"] = rejected(verify_lower, mutant)
    mutant = copy.deepcopy(lower); mutant[0]["point"][1] = "0"
    attacks["lower_p_endpoint_mutation"] = rejected(verify_lower, mutant)
    mutant = copy.deepcopy(lower); mutant[0]["covering_member_count"] += 1
    attacks["lower_owner_cover_omission_or_count_mutation"] = rejected(verify_lower, mutant)
    mutant = copy.deepcopy(lower); mutant[0]["owner_component"] = mutant[0]["target_component"]
    attacks["lower_C15_component_mutation"] = rejected(verify_lower, mutant)
    mutant = copy.deepcopy(lower); mutant[0]["witness"] = True
    attacks["lower_witness_flip"] = rejected(verify_lower, mutant)
    need(all(attacks.values()), "all attacks rejected")
    return attacks


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in ("graph1", "graph2", "lower1", "lower2"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    g1, g2 = graph1(load(args.graph1)), graph2(load(args.graph2))
    verify_graph(g1); verify_graph(g2)
    need(sorted(g1, key=lambda r: r["sheet_member_id"]+r["side_member_id"]) ==
         sorted(g2, key=lambda r: r["sheet_member_id"]+r["side_member_id"]), "graph implementations exact")
    l1, l2 = lower1(load(args.lower1)), lower2(load(args.lower2))
    verify_lower(l1); verify_lower(l2)
    need(sorted(l1, key=lambda r: tuple(r["key"])) == sorted(l2, key=lambda r: tuple(r["key"])), "lower implementations exact")
    attacks = attack_suite(g2, l2)
    print(json.dumps({
        "status": "PASS_P0A_192_24_DUAL_IMPLEMENTATION_AND_COHERENT_ATTACKS_ZERO_CREDIT",
        "graph_count": 192, "lower_count": 24, "unresolved_count": 0,
        "attack_count": len(attacks), "attacks": attacks,
        "formal_credit": 0, "C27_C28_C29": "REJECT_PENDING_20_FAMILY_GATE",
    }, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
