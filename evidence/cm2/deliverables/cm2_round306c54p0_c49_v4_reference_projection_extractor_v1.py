#!/usr/bin/env python3
"""Extract the frozen semantic comparison hashes from C49-v4 JSON on stdin.

This is a reference-data reducer, not the independent verifier.  It imports
no C49 module and performs no numeric work.  Its small output is compared with
the separately recomputed C54p0 projection and frozen as an audit binding.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from typing import Any


C49_OBJECT = "9a39a43907651235a216977a097615aad098be10989617088a6295043857fb17"
NUMERIC_KEYS = (
    "status", "collision_index", "collision_index_derivation",
    "exact_owner", "discriminant", "root_order", "official_word",
    "chart", "wall", "homogeneity", "incidence", "core",
    "structured_terminal_decision_margin", "full_candidate_table",
    "global_oracle_available", "formal_credit", "D02_credit",
    "history_replay", "blocker", "next_decision",
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise RuntimeError(label)


def normalize_replay(value: Any) -> Any:
    if type(value) is not dict:
        return copy.deepcopy(value)
    answer = copy.deepcopy(value)
    answer.pop("history_sha256", None)
    answer.pop("replay_rows_sha256", None)
    for row in answer.get("replay_rows", []):
        row.pop("evidence_sha256", None)
    return answer


def numeric_step(step: dict[str, Any]) -> dict[str, Any]:
    answer = {key: copy.deepcopy(step[key]) for key in NUMERIC_KEYS if key in step}
    if "history_replay" in answer:
        answer["history_replay"] = normalize_replay(answer["history_replay"])
    return answer


def tree_projection(tree: dict[str, Any]) -> dict[str, Any]:
    performed: dict[str, dict[str, Any]] = {}
    bits: dict[str, set[str]] = {}
    leaves = []
    for leaf in tree["leaves"]:
        step = leaf["step"]
        for row in step["original_box"]["refinement_decision_chain"]:
            path = row["parent_adaptive_suffix"]
            decision = copy.deepcopy(row["split_decision"])
            if path in performed:
                need(performed[path] == decision, "coherent repeated split:" + path)
            else:
                performed[path] = decision
                bits[path] = set()
            bit = row["selected_child_bit"]
            need(bit in {"0", "1"}, "selected child bit enum")
            bits[path].add(bit)
        leaves.append({
            "path": leaf["adaptive_suffix"],
            "relative_Kraft_fraction": leaf["relative_Kraft_fraction"],
            "regression_status": leaf["regression_status"],
            "step": numeric_step(step),
        })
    decisions = [{"parent_path": path, "performed": True,
                  "selected_child_bit_enum": sorted(bits[path]),
                  "decision": decision}
                 for path, decision in performed.items()]
    for leaf in tree["leaves"]:
        if leaf["regression_status"] == "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION":
            decisions.append({"parent_path": leaf["adaptive_suffix"],
                              "performed": False,
                              "selected_child_bit_enum": [],
                              "decision": copy.deepcopy(leaf["step"]["next_decision"])})
    need(len({row["parent_path"] for row in decisions}) == len(decisions),
         "unique decision paths")
    need(all((row["selected_child_bit_enum"] == ["0", "1"])
             if row["performed"] else not row["selected_child_bit_enum"]
             for row in decisions), "both child enums on performed split")
    paths = [leaf["adaptive_suffix"] for leaf in tree["leaves"]]
    root_path = paths[0]
    for path in paths[1:]:
        while not path.startswith(root_path):
            root_path = root_path[:-1]
    return {
        "collision_index": tree["collision_index"],
        "root_path": root_path,
        "maximum_additional_depth": tree["maximum_additional_depth"],
        "maximum_nodes": tree["maximum_nodes"],
        "node_count": tree["node_count"], "split_count": tree["split_count"],
        "leaf_count": tree["leaf_count"],
        "leaf_status_census": tree["leaf_status_census"],
        "relative_Kraft_sum": tree["relative_Kraft_sum"],
        "decisions": sorted(decisions, key=lambda row: row["parent_path"]),
        "leaves": sorted(leaves, key=lambda row: row["path"]),
    }


def main() -> int:
    raw = sys.stdin.buffer.read()
    value = json.loads(raw)
    body = copy.deepcopy(value)
    claimed = body.pop("object_sha256")
    need(claimed == C49_OBJECT == digest(body), "C49 regression object pin")
    sides = {row["side"]: row["adaptive_result"]
             for row in value["collision3_both_physical_sides"]}
    projections = {
        "collision3_reflected": tree_projection(sides["REFLECTED"]),
        "collision3_representative": tree_projection(sides["REPRESENTATIVE"]),
        "collision4": tree_projection(value["collision4_adaptive_result"]),
    }
    hashes = {key: digest(projection) for key, projection in projections.items()}
    hashes["collision5_step"] = digest(numeric_step(
        value["collision5_first_live_child_step"]))
    hashes["combined"] = digest(hashes)
    output = {
        "schema": "cm2.round306c54p0.c49-v4-reference-semantic-projection.v1",
        "C49_regression_object_sha256": C49_OBJECT,
        "C49_regression_file_sha256": hashlib.sha256(raw).hexdigest(),
        "semantic_projection_sha256": hashes,
        "projection_counts": {
            key: {"decisions": len(projection["decisions"]),
                  "leaves": len(projection["leaves"])}
            for key, projection in projections.items()
        },
        "formal_credit": 0, "D02_credit": 0,
    }
    output["object_sha256"] = digest(output)
    sys.stdout.buffer.write(canonical(output) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
