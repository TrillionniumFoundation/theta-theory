#!/usr/bin/env python3
"""Coherent semantic attacks for the append-only C27R1-B/C overlay."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
VERIFIER = ROOT / "cm2_round306c27r1bc_source_g_provisional_witness_overlay_independent_verifier.py"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


spec = importlib.util.spec_from_file_location("c27r1bc_verifier", VERIFIER)
if spec is None or spec.loader is None: raise RuntimeError("verifier import")
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


OLD = ["round306c15-source-g-component:" + hashlib.sha256(label.encode()).hexdigest() for label in "ABCD"]
SIZES = dict(zip(OLD, (2, 3, 5, 7)))
AUTHORITY = {
    "old_component_sizes": SIZES,
    "witnesses": [
        {"group_id": "witness:g1", "pair": sorted(OLD[:2]), "volume": "1/13"},
        {"group_id": "witness:g2", "pair": sorted(OLD[:2]), "volume": "2/13"},
        {"group_id": "witness:g3", "pair": sorted(OLD[2:]), "volume": "3/13"},
    ],
    "members": [{"member_id": f"member:{component[-8:]}:{ordinal}", "old_component_id": component} for component, count in SIZES.items() for ordinal in range(count)],
}
PRISTINE = module.compact_expected(AUTHORITY)


def coherent_from(mutator: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    alternate = copy.deepcopy(AUTHORITY); mutator(alternate); return module.compact_expected(alternate)


def attacks() -> list[tuple[str, Callable[[], dict[str, Any]]]]:
    def missing_witness(authority): authority["witnesses"].pop()
    def fake_edge(authority): authority["witnesses"].append({"group_id": "witness:fake", "pair": sorted([OLD[1], OLD[2]]), "volume": "1/17"})
    def reroute_edge(authority): authority["witnesses"][0]["pair"] = sorted([OLD[0], OLD[2]])
    def merge_old_components(authority):
        moved = OLD[1]; authority["old_component_sizes"][OLD[0]] += authority["old_component_sizes"].pop(moved)
        for witness in authority["witnesses"]:
            witness["pair"] = sorted(OLD[2:]) if moved in witness["pair"] else witness["pair"]
        authority["witnesses"] = [row for row in authority["witnesses"] if row["pair"][0] != row["pair"][1]]
        for member in authority["members"]:
            if member["old_component_id"] == moved: member["old_component_id"] = OLD[0]
    rows: list[tuple[str, Callable[[], dict[str, Any]]]] = [
        ("coherent_missing_authoritative_witness_and_downstream_split", lambda: coherent_from(missing_witness)),
        ("coherent_fake_edge_and_downstream_merge", lambda: coherent_from(fake_edge)),
        ("coherent_rerouted_witness_edge_and_partition", lambda: coherent_from(reroute_edge)),
        ("coherent_rewritten_old_partition", lambda: coherent_from(merge_old_components)),
    ]
    def mutate(name: str, fn: Callable[[dict[str, Any]], None]):
        def build():
            value = copy.deepcopy(PRISTINE); fn(value); return value
        rows.append((name, build))
    mutate("omit_promotion_edge", lambda value: value["promotion_edges"].pop())
    mutate("duplicate_promotion_edge", lambda value: value["promotion_edges"].append(copy.deepcopy(value["promotion_edges"][0])))
    mutate("substitute_witness_group", lambda value: value["promotion_edges"][0]["group_ids"].__setitem__(0, "witness:substitute"))
    mutate("reverse_unsorted_edge", lambda value: value["promotion_edges"][0]["pair"].reverse())
    mutate("omit_component", lambda value: value["components"].pop())
    mutate("reuse_old_component_id", lambda value: value["components"][0].__setitem__("id", value["components"][0]["old_ids"][0]))
    mutate("forge_content_address", lambda value: value["components"][0].__setitem__("id", module.NEW_NS + "0" * 64))
    mutate("change_component_member_count", lambda value: value["components"][0].__setitem__("member_count", value["components"][0]["member_count"] + 1))
    mutate("omit_member_assignment", lambda value: value["member_assignments"].pop())
    mutate("duplicate_member_assignment", lambda value: value["member_assignments"].append(copy.deepcopy(value["member_assignments"][0])))
    mutate("reroute_member_assignment", lambda value: value["member_assignments"][0].__setitem__("provisional_component_id", value["components"][-1]["id"]))
    mutate("upgrade_formal_credit", lambda value: value["summary"].__setitem__("formal_credit", 1))
    mutate("upgrade_qualification", lambda value: value["summary"].__setitem__("qualification", "FORMAL_MAXIMAL_COMPONENT_PARTITION"))
    mutate("preserve_old_chain", lambda value: value["summary"].__setitem__("old_C27_C28_C29", "PASS"))
    mutate("inflate_rank_reduction", lambda value: value["summary"].__setitem__("rank_reduction", value["summary"]["rank_reduction"] + 1))
    mutate("alter_internalized_pair_count", lambda value: value["summary"].__setitem__("newly_internalized_pairs", value["summary"]["newly_internalized_pairs"] + 1))
    mutate("alter_cross_denominator", lambda value: value["summary"].__setitem__("cross_denominator", value["summary"]["cross_denominator"] - 1))
    return rows


def main() -> int:
    module.validate_compact_attack_model(AUTHORITY, PRISTINE)
    receipts = []
    for name, build in attacks():
        candidate = build(); rejected = False; reason = None
        try: module.validate_compact_attack_model(AUTHORITY, candidate)
        except module.Reject as error: rejected = True; reason = str(error)
        if not rejected: raise RuntimeError("attack accepted:" + name)
        receipts.append({"attack": name, "expected": "REJECT", "observed": "REJECT", "reason": reason})
    result = {
        "schema": "cm2.round306c27r1-bc.provisional-witness-overlay-coherent-attacks.v1",
        "status": "PASS_ALL_COHERENT_ATTACKS_REJECTED", "formal_credit": 0,
        "attack_count": len(receipts), "receipts": receipts,
    }
    result["result_object_sha256"] = hashlib.sha256(canonical(result)).hexdigest()
    sys.stdout.buffer.write(canonical(result) + b"\n"); return 0


if __name__ == "__main__": raise SystemExit(main())
