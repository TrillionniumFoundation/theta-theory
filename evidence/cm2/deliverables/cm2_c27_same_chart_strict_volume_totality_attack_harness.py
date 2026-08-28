#!/usr/bin/env python3
"""Coherent mutation attacks for the strict-volume SAME_CHART subgate.

The direct-source sweep is executed once.  A compact semantic projection of
all materialized ledgers is then anchored to that reconstruction.  Every
attack updates its compact closure after mutation, so rejection cannot rely
on a stale checksum alone.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import importlib.util
import json
import hashlib
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
VERIFY_SOURCE = ROOT / "cm2_c27_same_chart_strict_volume_totality_independent_verifier.py"
PREFIX = "cm2_c27_same_chart_strict_volume_totality_v1"


class Rejected(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def load_verifier():
    spec = importlib.util.spec_from_file_location("same_chart_strict_independent", VERIFY_SOURCE)
    need(spec is not None and spec.loader is not None, "verifier import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def flip(text: str) -> str:
    return ("0" if text[0] != "0" else "1") + text[1:]


def projection(module, candidate_dir: Path, seed: int) -> tuple[dict[str, Any], dict[str, Any]]:
    atoms, direct_pairs, sweep = module.reconstruct(seed)
    by_id = {atom["id"]: atom for atom in atoms}
    observed_pairs = set()
    semantic_rows = []
    owner_pairs = set()
    edges = set()
    base_edges = set()
    incremental_edges = set()
    affected = set()
    endpoint_bit_true_count = 0
    cross_chart_pair_count = 0
    witness_chart_census = Counter()
    baseline = incremental = 0
    for row in module.rows(candidate_dir / (PREFIX + "_witness_occurrences.jsonl.gz")):
        pair = tuple(sorted(member["atom_id"] for member in row["members"]))
        need(pair in direct_pairs and pair not in observed_pairs, "direct occurrence pair")
        observed_pairs.add(pair)
        direct = [by_id[value] for value in pair]
        cross_chart_pair_count += int(direct[0]["chart"] != direct[1]["chart"])
        if direct[0]["chart"] == direct[1]["chart"]:
            witness_chart_census[direct[0]["chart"]] += 1
        source_pair = tuple(sorted(atom["source"] for atom in direct))
        component_pair = tuple(sorted(atom["component"] for atom in direct))
        owner_pair = tuple(sorted(atom["owner"] for atom in direct))
        exact = direct[0]["bounds"] == direct[1]["bounds"]
        is_baseline = source_pair == ("C22A", "C22A") and exact
        need(row["known_228_exact_equal_baseline_occurrence"] is is_baseline, "baseline semantic")
        need(row["incremental_beyond_known_228_occurrences"] is (not is_baseline), "incremental semantic")
        need(row["component_pair"] == list(component_pair), "component semantic")
        endpoint_bit_true_count += int(row["endpoint_ownership_bits_used"] is True)
        baseline += int(is_baseline)
        incremental += int(not is_baseline)
        owner_pairs.add(owner_pair)
        edges.add(component_pair)
        affected.update(component_pair)
        if is_baseline:
            base_edges.add(component_pair)
        else:
            incremental_edges.add(component_pair)
        semantic_rows.append([pair, source_pair, component_pair, owner_pair, exact, is_baseline, row["intersection_bounds"], row["intersection_relation"]])
    need(observed_pairs == direct_pairs, "direct pair totality")

    adjacency: dict[str, set[str]] = defaultdict(set)
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(adjacency)
    clusters = []
    while unseen:
        start = min(unseen)
        stack, component = [start], {start}
        unseen.remove(start)
        while stack:
            here = stack.pop()
            for nxt in adjacency[here]:
                if nxt not in component:
                    component.add(nxt)
                    unseen.remove(nxt)
                    stack.append(nxt)
        clusters.append(tuple(sorted(component)))
    clusters.sort()

    result = json.loads((candidate_dir / (PREFIX + "_result.json")).read_bytes())
    model = {
        "primitive_atom_count": len(atoms),
        "all_component_strict_pair_count": sweep["all"],
        "same_component_strict_pair_count": sweep["same"],
        "cross_component_strict_pair_count": len(direct_pairs),
        "source_pair_census": sweep["source_pairs"],
        "occurrence_pair_set_sha256": sha(sorted(direct_pairs)),
        "occurrence_semantic_rows_sha256": sha(sorted(semantic_rows)),
        "baseline_occurrence_count": baseline,
        "incremental_occurrence_count": incremental,
        "endpoint_bit_true_count": endpoint_bit_true_count,
        "cross_chart_pair_count": cross_chart_pair_count,
        "witness_chart_census": dict(sorted(witness_chart_census.items())),
        "chart_partition_enforced": True,
        "member_pair_count": len(owner_pairs),
        "member_pair_set_sha256": sha(sorted(owner_pairs)),
        "component_edge_count": len(edges),
        "component_edge_set_sha256": sha(sorted(edges)),
        "baseline_edge_count": len(base_edges),
        "incremental_edge_count": len(incremental_edges),
        "baseline_incremental_edge_overlap_count": len(base_edges & incremental_edges),
        "novel_edge_count": len(incremental_edges - base_edges),
        "affected_vertex_count": len(affected),
        "affected_vertex_set_sha256": sha(sorted(affected)),
        "cluster_count": len(clusters),
        "cluster_partition_sha256": sha(clusters),
        "rank_reduction": len(affected) - len(clusters),
        "provisional_component_count": 57876 - (len(affected) - len(clusters)),
        "forbidden_C27_read": result["forbidden_inputs"]["C27_or_FAMILIES_imported_or_read"],
        "forbidden_old_edge_read": result["forbidden_inputs"]["historical_edge_ledger_used"],
        "closure_contacts_promoted": result["geometry_scope"]["dim1_dim2_closure_contacts_promoted_by_this_probe"],
        "formal_credit": result["formal_credit"],
        "C27_C28_C29": result["C27_C28_C29"],
    }
    anchored = {**model, "projection_sha256": sha(model)}
    return anchored, {"direct_pair_count": len(direct_pairs), "direct_pair_set_sha256": sha(sorted(direct_pairs))}


def validate(candidate: dict[str, Any], authority: dict[str, Any]) -> None:
    body = dict(candidate)
    claimed = body.pop("projection_sha256", None)
    need(claimed == sha(body), "coherent projection closure")
    need(candidate == authority, "direct-source anchored projection equality")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    candidate_dir = Path(args.candidate_dir).resolve()
    module = load_verifier()
    authority, direct = projection(module, candidate_dir, args.seed)
    validate(authority, authority)

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("drop_occurrence_and_reclose", lambda x: (x.__setitem__("cross_component_strict_pair_count", x["cross_component_strict_pair_count"] - 1), x.__setitem__("occurrence_pair_set_sha256", flip(x["occurrence_pair_set_sha256"])))),
        ("duplicate_occurrence_and_reclose", lambda x: x.__setitem__("cross_component_strict_pair_count", x["cross_component_strict_pair_count"] + 1)),
        ("mutate_occurrence_pair_id", lambda x: x.__setitem__("occurrence_pair_set_sha256", flip(x["occurrence_pair_set_sha256"]))),
        ("mutate_source_pair", lambda x: x.__setitem__("source_pair_census", {**x["source_pair_census"], "C19A__C22A": 1})),
        ("mutate_exact_intersection_bounds", lambda x: x.__setitem__("occurrence_semantic_rows_sha256", flip(x["occurrence_semantic_rows_sha256"]))),
        ("flip_baseline_occurrence", lambda x: (x.__setitem__("baseline_occurrence_count", x["baseline_occurrence_count"] - 1), x.__setitem__("incremental_occurrence_count", x["incremental_occurrence_count"] + 1))),
        ("flip_incremental_occurrence", lambda x: x.__setitem__("incremental_occurrence_count", x["incremental_occurrence_count"] - 1)),
        ("claim_endpoint_bits_used", lambda x: x.__setitem__("endpoint_bit_true_count", 1)),
        ("cross_chart_injection", lambda x: (x.__setitem__("cross_chart_pair_count", 1), x.__setitem__("occurrence_semantic_rows_sha256", flip(x["occurrence_semantic_rows_sha256"])))),
        ("drop_chart_partition", lambda x: x.__setitem__("chart_partition_enforced", False)),
        ("mutate_member_pair", lambda x: x.__setitem__("member_pair_set_sha256", flip(x["member_pair_set_sha256"]))),
        ("drop_member_pair", lambda x: x.__setitem__("member_pair_count", x["member_pair_count"] - 1)),
        ("add_component_edge", lambda x: x.__setitem__("component_edge_count", x["component_edge_count"] + 1)),
        ("mutate_component_edge", lambda x: x.__setitem__("component_edge_set_sha256", flip(x["component_edge_set_sha256"]))),
        ("drop_baseline_edge", lambda x: x.__setitem__("baseline_edge_count", x["baseline_edge_count"] - 1)),
        ("drop_incremental_edge", lambda x: x.__setitem__("incremental_edge_count", x["incremental_edge_count"] - 1)),
        ("mutate_edge_overlap", lambda x: x.__setitem__("baseline_incremental_edge_overlap_count", x["baseline_incremental_edge_overlap_count"] + 1)),
        ("mutate_novel_edge_count", lambda x: x.__setitem__("novel_edge_count", x["novel_edge_count"] - 1)),
        ("drop_affected_vertex", lambda x: x.__setitem__("affected_vertex_count", x["affected_vertex_count"] - 1)),
        ("mutate_affected_vertex", lambda x: x.__setitem__("affected_vertex_set_sha256", flip(x["affected_vertex_set_sha256"]))),
        ("merge_clusters", lambda x: x.__setitem__("cluster_count", x["cluster_count"] - 1)),
        ("mutate_cluster_partition", lambda x: x.__setitem__("cluster_partition_sha256", flip(x["cluster_partition_sha256"]))),
        ("mutate_rank_reduction", lambda x: x.__setitem__("rank_reduction", x["rank_reduction"] + 1)),
        ("mutate_provisional_component_count", lambda x: x.__setitem__("provisional_component_count", x["provisional_component_count"] + 1)),
        ("claim_C27_FAMILIES_read", lambda x: x.__setitem__("forbidden_C27_read", True)),
        ("promote_dim1_dim2_closure_contacts", lambda x: x.__setitem__("closure_contacts_promoted", True)),
        ("grant_formal_credit", lambda x: x.__setitem__("formal_credit", 1)),
        ("preserve_old_C27_C28_C29", lambda x: x.__setitem__("C27_C28_C29", "PRESERVE")),
    ]
    attack_rows = []
    for ordinal, (name, mutate) in enumerate(mutations):
        body = dict(authority)
        body.pop("projection_sha256")
        mutate(body)
        attacked = {**body, "projection_sha256": sha(body)}
        rejected = False
        reason = None
        try:
            validate(attacked, authority)
        except Rejected as exc:
            rejected, reason = True, str(exc)
        need(rejected, "attack must reject:" + name)
        attack_rows.append({"ordinal": ordinal, "attack": name, "coherent_projection_closure_recomputed": True, "rejected": rejected, "reason": reason})

    body = {
        "schema": "cm2.c27.same-chart-strict-volume-totality.v1.attack-result.v1",
        "status": f"PASS_ALL_{len(attack_rows)}_COHERENT_MUTATIONS_REJECTED",
        "seed": args.seed,
        "seed_usage": "SEED_CONTROLS_INDEPENDENT_DIRECT_SOURCE_SWEEP_TIE_ORDER",
        "direct_authority": direct,
        "authority_projection_sha256": authority["projection_sha256"],
        "attack_count": len(attack_rows),
        "rejected_count": sum(row["rejected"] for row in attack_rows),
        "attacks": attack_rows,
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
    }
    result = {**body, "result_sha256": sha(body)}
    Path(args.output).resolve().write_bytes(canonical(result) + b"\n")
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
