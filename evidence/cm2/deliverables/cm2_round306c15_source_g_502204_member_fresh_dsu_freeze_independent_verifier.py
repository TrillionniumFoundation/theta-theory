#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze"
SCHEMA = "cm2.round306c15.source-g-502204-member-fresh-dsu-freeze.v1"
FILES = [PREFIX + suffix for suffix in ("_edge_application_ledger.jsonl.gz", "_member_component_ledger.jsonl.gz", "_base_root_component_ledger.jsonl.gz", "_component_census_ledger.jsonl.gz", "_cross_component_pair_denominator.json", "_result.json")]
SOURCE = {
    "C6_MEMBER": "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_member_component_ledger.jsonl.gz",
    "C6_EDGE": "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze_edge_application_ledger.jsonl.gz",
    "C14C_ADMISSION": "cm2_round306c14c_source_g_registry_official_key_family_and_self_root_admission_new_exact_sheet_admission_ledger.jsonl.gz",
    "C14D_EDGE": "cm2_round306c14d_source_g_exact_sheet_to_side_edge_promotion_edge_promotion_ledger.jsonl.gz",
}


class Rejected(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def obj(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1048576): digest.update(block)
    return digest.hexdigest()


def rows(path: Path):
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), "newline:" + path.name); raw = line[:-1]; row = json.loads(raw)
            need(canonical(row) == raw, "canonical:" + path.name); body = dict(row)
            need(body.pop("row_sha256", None) == obj(body), "closure:" + path.name)
            yield ordinal, row, hashlib.sha256(raw).hexdigest()


class DSU:
    def __init__(self, roots: set[str]):
        self.items = sorted(roots); self.index = {root: i for i, root in enumerate(self.items)}
        self.parent = list(range(len(self.items))); self.size = [1] * len(self.items); self.reduction = 0
    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]; item = self.parent[item]
        return item
    def union(self, left: str, right: str) -> int:
        a = self.find(self.index[left]); b = self.find(self.index[right])
        if a == b: return 0
        if self.size[a] < self.size[b] or (self.size[a] == self.size[b] and self.items[a] > self.items[b]): a, b = b, a
        self.parent[b] = a; self.size[a] += self.size[b]; self.reduction += 1; return 1
    def partition(self):
        groups = defaultdict(list)
        for ordinal, root in enumerate(self.items): groups[self.find(ordinal)].append(root)
        return sorted(sorted(group) for group in groups.values())


def verify(candidate: Path) -> dict[str, Any]:
    result_raw = (candidate / FILES[-1]).read_bytes(); result = json.loads(result_raw)
    need(canonical(result) == result_raw, "result canonical"); body = dict(result); claimed = body.pop("result_sha256")
    need(claimed == obj(body), "result closure")
    need(result["status"] == "PASS_502204_MEMBER_484982_EDGE_FRESH_DSU_SEALED__C7_C14_REPLAY_REQUIRED", "result status")
    need(result["fresh_universe_census"] == {"members": 502204, "base_roots": 339036, "old_C6_members": 497772, "new_C14c_members": 4432}, "result universe census")
    need(result["edge_application_census"] == {"applied_edges": 484982, "old_C6_retained_edges": 476118, "new_C14d_edges": 8864, "forward_rank_reduction": 281160, "reverse_rank_reduction": 281160}, "result edge census")
    need(result["fresh_DSU_census"]["components"] == 57876 and result["fresh_DSU_census"]["cross_component_pair_denominator"] == 125616475670, "result DSU census")
    need(result["strict_invalidation"] == {"all_pre_C15_component_ids": "INVALIDATED", "C6_through_C14_component_bound_outputs": "REPLAY_REQUIRED"}, "result invalidation")
    need(result["strict_nonpromotion"] == {"representation_pullback": 0, "normalized_support": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": "NO-GO_FOR_CLAIM"}, "result nonpromotion")
    for name, desc in result["output_files"].items():
        path = candidate / name; need(path.stat().st_size == desc["size"] and fsha(path) == desc["sha256"], "output descriptor:" + name)

    members: dict[str, tuple[str, str, str, list[Any]]] = {}; root_count = defaultdict(int); root_key = {}
    for ordinal, row, wire in rows(ROOT / SOURCE["C6_MEMBER"]):
        member = row["registry_member_id"]; root = row["new_base_root_id"]
        members[member] = (root, row["official_key_id"], "C6_RETAINED", [ordinal, row["row_id"], wire, row["row_sha256"]])
        root_count[root] += 1; root_key.setdefault(root, row["official_key_id"])
    need(len(members) == 497772 and len(root_count) == 334604, "C6 member exhaustion")
    for ordinal, row, wire in rows(ROOT / SOURCE["C14C_ADMISSION"]):
        member = row["new_exact_sheet_member_id"]; root = row["self_base_root_id"]
        need(member not in members and root not in root_count, "admission collision")
        members[member] = (root, row["official_key_id"], "C14C_NEW_EXACT_SHEET", [ordinal, row["row_id"], wire, row["row_sha256"]])
        root_count[root] = 1; root_key[root] = row["official_key_id"]
    need(len(members) == 502204 and len(root_count) == 339036, "universe exhaustion")

    edges = []
    for ordinal, row, wire in rows(ROOT / SOURCE["C6_EDGE"]):
        if row["fed_to_new_empty_DSU"]:
            edges.append(("C6_RETAINED", row["new_projected_base_root_pair"], ordinal, row["row_id"], wire, row["row_sha256"]))
    need(len(edges) == 476118, "C6 edge exhaustion")
    for ordinal, row, wire in rows(ROOT / SOURCE["C14D_EDGE"]):
        edges.append(("C14D_NEW_EXACT_SHEET_TO_SIDE", row["projected_base_root_pair"], ordinal, row["row_id"], wire, row["row_sha256"]))
    need(len(edges) == 484982, "all edge exhaustion")
    roots = set(root_count); forward = DSU(roots); ff = [forward.union(*edge[1]) for edge in edges]
    reverse = DSU(roots); rf = [0] * len(edges)
    for ordinal in range(len(edges) - 1, -1, -1): rf[ordinal] = reverse.union(*edges[ordinal][1])
    partition = forward.partition(); need(partition == reverse.partition() and forward.reduction == reverse.reduction == 281160 and len(partition) == 57876, "independent DSU")
    component_by_root = {}; roots_by_component = {}
    for group in partition:
        component = "round306c15-source-g-component:" + obj(group); roots_by_component[component] = group
        for root in group: component_by_root[root] = component

    edge_path = candidate / FILES[0]
    count = 0
    for ordinal, row, _ in rows(edge_path):
        channel, pair, source_ordinal, source_row_id, wire, row_sha = edges[ordinal]
        need(row["application_ordinal"] == ordinal and row["channel"] == channel and row["pair"] == pair and row["source_ordinal"] == source_ordinal and row["source_row_id"] == source_row_id and row["source_wire_sha256"] == wire and row["source_row_sha256"] == row_sha and row["forward_rank_reduction"] == ff[ordinal] and row["reverse_rank_reduction"] == rf[ordinal] and row["fresh_DSU_edge_application_credit"] == 1, "edge row")
        count += 1
    need(count == 484982, "candidate edge count")

    sorted_members = sorted(members)
    for expected_ordinal, (ordinal, row, _) in enumerate(rows(candidate / FILES[1])):
        member = sorted_members[expected_ordinal]; root, key, source, ref = members[member]
        need(ordinal == expected_ordinal and row["member_ordinal"] == ordinal and row["registry_member_id"] == member and row["base_root_id"] == root and row["fresh_component_id"] == component_by_root[root] and row["official_key_id"] == key and row["admission_source"] == source and row["source_row_ref"] == ref and row["fresh_member_and_component_credit"] == 1, "member row")
    need(expected_ordinal + 1 == 502204, "candidate member count")

    sorted_roots = sorted(roots)
    for expected_ordinal, (ordinal, row, _) in enumerate(rows(candidate / FILES[2])):
        root = sorted_roots[expected_ordinal]
        need(ordinal == expected_ordinal and row["base_root_ordinal"] == ordinal and row["base_root_id"] == root and row["fresh_component_id"] == component_by_root[root] and row["official_key_id"] == root_key[root] and row["member_count"] == root_count[root] and row["fresh_root_component_credit"] == 1, "root row")
    need(expected_ordinal + 1 == 339036, "candidate root count")

    component_members = {component: sum(root_count[root] for root in group) for component, group in roots_by_component.items()}; sorted_components = sorted(roots_by_component)
    for expected_ordinal, (ordinal, row, _) in enumerate(rows(candidate / FILES[3])):
        component = sorted_components[expected_ordinal]; group = roots_by_component[component]
        need(row["component_ordinal"] == ordinal == expected_ordinal and row["fresh_component_id"] == component and row["base_root_count"] == len(group) and row["base_root_ids_sha256"] == obj(group) and row["member_count"] == component_members[component] and row["fresh_component_credit"] == 1, "component row")
    need(expected_ordinal + 1 == 57876, "candidate component count")
    sizes = sorted(component_members.values()); all_pairs = 502204 * 502203 // 2; within = sum(size * (size - 1) // 2 for size in sizes); cross = all_pairs - within
    cross_raw = (candidate / FILES[4]).read_bytes(); cross_obj = json.loads(cross_raw); need(canonical(cross_obj) == cross_raw and cross_obj["cross_component_pair_denominator"] == cross == 125616475670 and cross_obj["component_member_size_vector_sha256"] == obj(sizes), "cross object")
    need(result["fresh_DSU_census"]["partition_sha256"] == obj(partition) and result["formal_credit"] == {"fresh_member_universe": 502204, "fresh_base_roots": 339036, "fresh_edge_applications": 484982, "fresh_components": 57876, "cross_denominator": 125616475670}, "result formal credit")
    return {"status": "PASS_INDEPENDENT_C15_FRESH_DSU_VERIFICATION", "result_sha256": claimed, "members": 502204, "roots": 339036, "edges": 484982, "components": 57876, "cross_denominator": cross}


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "python -I -B")
    parser = argparse.ArgumentParser(); parser.add_argument("--candidate-dir"); args = parser.parse_args()
    candidate = ROOT if args.candidate_dir is None else Path(args.candidate_dir).resolve()
    print(json.dumps(verify(candidate), sort_keys=True, separators=(",", ":"))); return 0


if __name__ == "__main__": raise SystemExit(main())
