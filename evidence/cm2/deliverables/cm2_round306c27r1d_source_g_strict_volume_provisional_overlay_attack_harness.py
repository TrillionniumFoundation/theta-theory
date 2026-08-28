#!/usr/bin/env python3
"""Coherent fail-closed attacks for the C27R1D provisional overlay verifier."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
VERIFIER = ROOT / "cm2_round306c27r1d_source_g_strict_volume_provisional_overlay_independent_verifier.py"


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load_verifier() -> Any:
    spec = importlib.util.spec_from_file_location("c27r1d_overlay_independent_verifier_for_attacks", VERIFIER)
    if spec is None or spec.loader is None:
        raise RuntimeError("verifier import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def authority(module: Any) -> dict[str, Any]:
    sizes = {"C15-A": 3, "C15-B": 2, "C15-C": 4, "C15-D": 1, "C15-E": 2, "C15-F": 3}
    pairs = [["C15-A", "C15-B"], ["C15-B", "C15-C"], ["C15-D", "C15-E"]]
    members = []
    for component, count in sizes.items():
        for ordinal in range(count):
            members.append({"member_id": f"member:{component}:{ordinal}", "old_component_id": component})
    return {
        "old_component_sizes": sizes,
        "edges": [
            {"pair": pair, "edge_id": "sealed-edge:" + module.digest(pair), "authority": "SAME_CHART_STRICT_POSITIVE_VOLUME_INTERIOR_INTERSECTION"}
            for pair in pairs
        ],
        "members": members,
    }


def mutate(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
    def apply(target: dict[str, Any]) -> None:
        node: Any = target
        for step in path[:-1]:
            node = node[step]
        node[path[-1]] = value
    return apply


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    if args.seed <= 0:
        raise RuntimeError("real positive attack seed")
    module = load_verifier()
    original = authority(module)
    pristine = module.compact_expected(original, args.seed)

    attacks: list[tuple[str, str, Callable[[dict[str, Any], dict[str, Any]], None]]] = []

    def authority_attack(name: str, edit: Callable[[dict[str, Any]], None]) -> None:
        attacks.append((name, "AUTHORITY_RECONSTRUCTION", lambda source, candidate: edit(source)))

    def candidate_attack(name: str, edit: Callable[[dict[str, Any]], None]) -> None:
        attacks.append((name, "DOWNSTREAM_LEDGER_OR_SUMMARY", lambda source, candidate: edit(candidate)))

    def swap_component_ids(candidate: dict[str, Any]) -> None:
        left = candidate["components"][0]["id"]
        right = candidate["components"][1]["id"]
        candidate["components"][0]["id"] = right
        candidate["components"][1]["id"] = left

    authority_attack("delete_authoritative_edge", lambda x: x["edges"].pop(1))
    authority_attack("add_fake_edge", lambda x: x["edges"].append({"pair": ["C15-C", "C15-D"], "edge_id": "sealed-edge:" + module.digest(["C15-C", "C15-D"]), "authority": "SAME_CHART_STRICT_POSITIVE_VOLUME_INTERIOR_INTERSECTION"}))
    authority_attack("cross_chart_injection", mutate(("edges", 0, "authority"), "CROSS_CHART_UNSEALED_INJECTION"))
    authority_attack("duplicate_edge", lambda x: x["edges"].append(copy.deepcopy(x["edges"][0])))
    authority_attack("endpoint_tamper", mutate(("edges", 1, "pair", 1), "C15-D"))
    authority_attack("edge_id_tamper", mutate(("edges", 1, "edge_id"), "sealed-edge:" + "0" * 64))
    authority_attack("missing_member", lambda x: x["members"].pop())
    authority_attack("duplicate_member", lambda x: x["members"].append(copy.deepcopy(x["members"][0])))
    authority_attack("member_old_component_tamper", mutate(("members", 0, "old_component_id"), "C15-F"))
    authority_attack("old_component_size_tamper", mutate(("old_component_sizes", "C15-A"), 4))

    candidate_attack("component_id_permutation", swap_component_ids)
    candidate_attack("missing_member_assignment", lambda x: x["member_assignments"].pop())
    candidate_attack("duplicate_member_assignment", lambda x: x["member_assignments"].append(copy.deepcopy(x["member_assignments"][0])))
    candidate_attack("assignment_reroute", mutate(("member_assignments", 0, "provisional_component_id"), "round306c27r1d-strict-volume-provisional-source-g-component:" + "f" * 64))
    candidate_attack("denominator_off_by_one", lambda x: x["summary"].__setitem__("cross_denominator", x["summary"]["cross_denominator"] + 1))
    candidate_attack("rank_tamper", lambda x: x["summary"].__setitem__("rank_reduction", x["summary"]["rank_reduction"] - 1))
    candidate_attack("component_census_tamper", lambda x: x["summary"].__setitem__("provisional_components", x["summary"]["provisional_components"] + 1))
    candidate_attack("newly_internalized_pair_tamper", lambda x: x["summary"].__setitem__("newly_internalized_pairs", x["summary"]["newly_internalized_pairs"] + 1))
    candidate_attack("component_member_count_tamper", lambda x: x["components"][0].__setitem__("member_count", x["components"][0]["member_count"] + 1))
    candidate_attack("component_old_id_drop", lambda x: x["components"][0]["old_ids"].pop())
    candidate_attack("edge_application_drop", lambda x: x["edge_applications"].pop())
    candidate_attack("edge_application_duplicate", lambda x: x["edge_applications"].append(copy.deepcopy(x["edge_applications"][0])))
    candidate_attack("formal_credit_escalation", mutate(("summary", "formal_credit"), 1))
    candidate_attack("authorize_C27_C28_C29", mutate(("summary", "C27_C28_C29"), "AUTHORIZED"))
    candidate_attack("upper_bound_promoted_to_maximality", mutate(("summary", "qualification"), "FORMAL_PHYSICAL_MAXIMALITY"))
    candidate_attack("member_census_tamper", lambda x: x["summary"].__setitem__("members", x["summary"]["members"] + 1))

    results = []
    for name, layer, edit in attacks:
        source = copy.deepcopy(original)
        candidate = copy.deepcopy(pristine)
        rejected = False
        reason = None
        try:
            edit(source, candidate)
            module.validate_compact(source, candidate, args.seed ^ 0x5A5A5A5A)
        except Exception as error:  # the rejection class is deliberately verifier-owned
            rejected = True
            reason = f"{type(error).__name__}:{error}"
        if not rejected:
            raise RuntimeError("attack accepted:" + name)
        results.append({"attack": name, "layer": layer, "status": "REJECTED", "reason": reason})

    required = {
        "delete_authoritative_edge", "add_fake_edge", "cross_chart_injection", "duplicate_edge", "endpoint_tamper",
        "component_id_permutation", "missing_member_assignment", "duplicate_member_assignment", "denominator_off_by_one",
        "rank_tamper", "component_census_tamper",
    }
    names = {row["attack"] for row in results}
    if not required <= names or len(names) != len(results):
        raise RuntimeError("required/unique attack labels")
    value = {
        "schema": "cm2.round306c27r1d.strict-volume-provisional-overlay-coherent-attacks.v1",
        "status": "PASS_ALL_COHERENT_ATTACKS_REJECTED",
        "implementation_under_attack": "INDEPENDENT_ADJACENCY_BFS_COMPACT_SEMANTIC_RECONSTRUCTION",
        "attack_seed": args.seed,
        "attack_count": len(results), "rejected_count": len(results), "accepted_count": 0,
        "required_attack_labels_present": True, "formal_credit": 0,
        "C27": "UNAUTHORIZED", "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        "attacks": results,
    }
    value["attack_result_object_sha256"] = digest(value)
    payload = canonical(value) + b"\n"
    if args.out.exists():
        raise RuntimeError("no clobber attack result")
    args.out.write_bytes(payload)
    sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({"status": "FAIL_CLOSED", "error": str(error)}, sort_keys=True), file=sys.stderr)
        raise SystemExit(2)
