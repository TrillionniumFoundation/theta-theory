#!/usr/bin/env python3
"""Fail-closed logical/phase audit for the CM2 section-to-full bridge.

This checker never promotes literature citations or algebraic identities into
analytic witnesses.  A clause is certified only when the manifest says so.
If a separate finite phase tower is used, the checker also requires a strongly
connected weighted graph with cycle gcd one.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import deque
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cm2_gate5_transfer_manifest.json"


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def weighted_cycle_gcd(graph: dict[str, Any], failures: list[str]) -> int | None:
    states = graph.get("states")
    edges = graph.get("edges")
    if not isinstance(states, list) or not states or len(set(states)) != len(states):
        failures.append("phase_graph.states must be a nonempty duplicate-free list")
        return None
    if not isinstance(edges, list) or not edges:
        failures.append("phase_graph.edges must be a nonempty list")
        return None

    state_set = set(states)
    outgoing: dict[str, list[tuple[str, int]]] = {s: [] for s in states}
    incoming: dict[str, list[str]] = {s: [] for s in states}
    clean_edges: list[tuple[str, str, int]] = []
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            failures.append(f"phase edge {index} is not an object")
            continue
        u, v, weight = edge.get("source"), edge.get("target"), edge.get("weight")
        if u not in state_set or v not in state_set:
            failures.append(f"phase edge {index} has an unknown endpoint")
            continue
        if not isinstance(weight, int) or isinstance(weight, bool) or weight <= 0:
            failures.append(f"phase edge {index} has no positive integer weight")
            continue
        outgoing[u].append((v, weight))
        incoming[v].append(u)
        clean_edges.append((u, v, weight))
    if failures:
        return None

    def reachable(reverse: bool = False) -> set[str]:
        root = states[0]
        seen = {root}
        queue = deque([root])
        while queue:
            u = queue.popleft()
            neighbors = incoming[u] if reverse else [v for v, _ in outgoing[u]]
            for v in neighbors:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        return seen

    require(reachable() == state_set and reachable(True) == state_set,
            "phase graph is not strongly connected", failures)
    if failures:
        return None

    # For a strongly connected integer-weighted graph, the gcd of
    # d[u] + weight - d[v] over all edges equals the gcd of cycle weights.
    distance: dict[str, int] = {states[0]: 0}
    queue = deque([states[0]])
    while queue:
        u = queue.popleft()
        for v, weight in outgoing[u]:
            if v not in distance:
                distance[v] = distance[u] + weight
                queue.append(v)
    period = 0
    for u, v, weight in clean_edges:
        period = math.gcd(period, abs(distance[u] + weight - distance[v]))
    require(period == 1,
            f"phase graph has weighted cycle gcd {period}, not 1", failures)
    return period


def audit(data: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    require(data.get("schema_version") == 1, "unsupported schema_version", failures)
    require(isinstance(data.get("model_id"), str) and bool(data["model_id"]),
            "missing model_id", failures)
    require(data.get("route") in {"fixed_to_full", "direct_standard_N"},
            "route must be fixed_to_full or direct_standard_N", failures)

    sf1 = data.get("sf1_common_refinement", {})
    require(sf1.get("certified") is True, "SF1 common refinement is not certified", failures)
    require(set(sf1.get("sections", [])) == {"M", "N"},
            "SF1 does not contain exactly sections M and N", failures)

    sf2 = data.get("sf2_return_block_dq", {})
    for field in ("certified", "complete_return_word_manifest",
                  "all_boundary_currents_typed", "exact_occurrence_source_matching"):
        require(sf2.get(field) is True, f"SF2 missing {field}", failures)

    sf3 = data.get("sf3_kac_centering", {})
    require(sf3.get("algebra_certified") is True, "SF3 Kac algebra is not certified", failures)
    require(sf3.get("four_terms_separately_typed") is True,
            "SF3 four differentiated Kac terms are not separately typed", failures)

    sf4 = data.get("sf4_wiener_aperiodicity", {})
    require(sf4.get("target_standard_N_certified") is True,
            "SF4 target standard-N Wiener layer is not certified", failures)
    phase_period = None
    if sf4.get("uses_separate_phase_tower") is True:
        graph = sf4.get("phase_graph")
        if not isinstance(graph, dict):
            failures.append("SF4 uses a phase tower but has no phase_graph")
        else:
            phase_period = weighted_cycle_gcd(graph, failures)

    sf5 = data.get("sf5_phase_test_norm_lift", {})
    for field in ("regular_density_subspace_certified",
                  "singular_curve_source_certified",
                  "singular_face_current_certified",
                  "physical_test_lift_certified",
                  "both_cm2_norms_intertwined"):
        require(sf5.get(field) is True, f"SF5 missing {field}", failures)

    summary = {
        "model_id": data.get("model_id"),
        "route": data.get("route"),
        "phase_cycle_gcd": phase_period,
        "gate5_certified": not failures,
        "failure_count": len(failures),
    }
    return failures, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    failures, summary = audit(data)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if failures:
        print("GATE5: NOT_CERTIFIED")
        for failure in failures:
            print(f"- {failure}")
        return 2
    print("GATE5: CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
