#!/usr/bin/env python3
"""Independent verifier for the C27R2 fresh-primitive preflight.

This verifier does not import the producer.  It independently hashes and
parses the frozen C15, strict-volume, lower-dimensional and G2B authorities,
replays the known edge topology with adjacency-list connected components, and
checks that an incomplete future input surface is represented as rejection.
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
import gzip
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
C15 = ROOT / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
STRICT = WORKSPACE / ".cm2-runtime/audit/c27-same-chart-strict-volume-v1-seed-30632101-run3/candidate/cm2_c27_same_chart_strict_volume_totality_v1_component_edges.jsonl.gz"
G2B = WORKSPACE / ".cm2-runtime/audit/c27-c24a-priority-rank-closure-v2-seed-30635101/payload/C24A_cross_positive_unique_component_edges.jsonl.gz"
G2A_RECEIPT = ROOT / "cm2_c27_g2a_relative2d_primitive_totality_v2_terminal_receipt.json"
CURRENT_RECEIPT = ROOT / "cm2_c27_three_terminal_current_support_91672_v4_terminal_receipt.json"
FORBIDDEN = [
    "OLD_C27_FAMILIES",
    "OLD_C27_TRANSITION_CANDIDATE_LEDGER",
    "OLD_C27_TRANSITION_FAMILY_COVERAGE_LEDGER",
    "OLD_C28_PAIR_ROUTING",
    "OLD_C29_PHYSICAL_MAXIMALITY",
    "HISTORICAL_EDGE_LEDGER_AS_CANDIDATE_UNIVERSE",
]
PINS = {
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    STRICT: "64cb62aa3b5ae298699ef5809e075ce6c2314baad1f589965e675c82deaa4632",
    G2B: "d922bbf6d8f487df1e826271b0d65d2d9765432f6d4a02919fe1157b94c117ef",
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            payload = line[:-1]
            row = json.loads(payload)
            need(type(row) is dict and canonical(row) == payload,
                 f"canonical:{path.name}:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == digest(body),
                 f"closure:{path.name}:{ordinal}")
            yield row


def verify_document(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    claimed = body.pop("preflight_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "preflight closure")
    need(value.get("schema") == "cm2.round306c27r2.source-g-fresh-primitive-rebuild-preflight.v1", "schema")
    need(value.get("formal_credit") == 0 and value.get("manifest_authorized") is False,
         "nonpromotion")
    need(value.get("C27_transition_totality") == "UNAUTHORIZED"
         and value.get("C28_pair_routing") == "UNAUTHORIZED"
         and value.get("C29_physical_maximality") == "UNAUTHORIZED",
         "C27-C29 unauthorized")
    need(value.get("Source_W_transition_authorized") is False
         and value.get("CM2") == "NO-GO_FOR_CLAIM", "global nonpromotion")
    need(value.get("forbidden_dependency_open_count") == 0, "forbidden dependencies")
    need(value.get("forbidden_dependencies") == FORBIDDEN, "exact forbidden list")
    contract = value.get("input_contract", {})
    need(contract.get("frozen_C15_members") == 502_204
         and contract.get("frozen_old_C15_components") == 57_876
         and contract.get("strict_volume_component_edges") == 14_772
         and contract.get("same_chart_lower_edge_contribution") == 0
         and contract.get("G2B_unique_component_edges") == 144
         and contract.get("G2B_edges_subset_of_strict_volume") is True,
         "exact known input contract")
    future_contracts = contract.get("future_terminal_contracts")
    need(type(future_contracts) is dict
         and set(future_contracts) == {"G2A", "CURRENT_SUPPORT_91672"},
         "exact future contract names")
    need(future_contracts["G2A"].get("path") ==
         "deliverables/cm2_c27_g2a_relative2d_primitive_totality_v2_terminal_receipt.json",
         "G2A contract path")
    need(future_contracts["CURRENT_SUPPORT_91672"].get("path") ==
         "deliverables/cm2_c27_three_terminal_current_support_91672_v4_terminal_receipt.json",
         "91672 contract path")
    topo = value.get("edge_topology_preflight", {})
    need(topo.get("strict_volume_rank") == 14_104
         and topo.get("strict_volume_component_count") == 43_772,
         "strict topology")
    need(topo.get("G2B_incremental_rank_after_strict_volume") == 0,
         "G2B duplicate topology")
    need(topo.get("may_assert_final_component_count_43772") is False,
         "no premature 43772 assertion")
    missing = value.get("missing_required_authority")
    invalid = value.get("invalid_required_authority")
    need(type(missing) is list and type(invalid) is list, "authority lists")
    expected_missing = []
    if not G2A_RECEIPT.exists():
        expected_missing.append("G2A_TERMINAL_RECEIPT")
    if not CURRENT_RECEIPT.exists():
        expected_missing.append("CURRENT_SUPPORT_91672_TERMINAL_RECEIPT")
    need(missing == expected_missing, "filesystem-bound missing authority list")
    complete = not missing and not invalid
    need(value.get("producer_authorization") is complete, "authorization iff complete")
    if complete:
        need(value.get("status", "").startswith("PASS_INPUT_COMPLETE_"), "complete status")
    else:
        need(value.get("status", "").startswith("REJECT_INCOMPLETE_"), "reject status")
        need(topo.get("component_count_conclusion") ==
             "UNAUTHORIZED__43772_IS_STRICT_VOLUME_UPPER_BOUND_ONLY__FUTURE_EDGE_RANK_UNKNOWN",
             "incomplete component conclusion")
    return {"complete": complete, "preflight_sha256": claimed}


def independent_known_topology() -> dict[str, int | bool]:
    for path, pin in PINS.items():
        need(fsha(path) == pin, "file pin:" + path.name)
    components = set()
    for ordinal, row in enumerate(rows(C15)):
        need(row.get("member_ordinal") == ordinal, "C15 ordinal")
        components.add(row["fresh_component_id"])
    need(len(components) == 57_876, "C15 components")
    adjacency: dict[str, set[str]] = defaultdict(set)
    strict_pairs = set()
    for row in rows(STRICT):
        pair = tuple(row["component_pair"])
        need(len(pair) == 2 and tuple(sorted(pair)) == pair and pair[0] != pair[1],
             "strict pair")
        need(pair[0] in components and pair[1] in components and pair not in strict_pairs,
             "strict C15 unique")
        strict_pairs.add(pair)
        adjacency[pair[0]].add(pair[1])
        adjacency[pair[1]].add(pair[0])
    need(len(strict_pairs) == 14_772, "strict edge count")
    visited = set()
    connected = 0
    for start in sorted(components):
        if start in visited:
            continue
        connected += 1
        visited.add(start)
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in adjacency[node]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
    need(connected == 43_772, "adjacency-list component count")
    g2b_pairs = set()
    for row in rows(G2B):
        pair = tuple(row["ordered_C15_component_pair"])
        need(pair not in g2b_pairs, "G2B unique")
        g2b_pairs.add(pair)
    need(len(g2b_pairs) == 144 and g2b_pairs <= strict_pairs, "G2B subset")
    return {
        "old_C15_components": len(components),
        "strict_edges": len(strict_pairs),
        "strict_adjacency_components": connected,
        "G2B_edges": len(g2b_pairs),
        "G2B_subset_strict": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        raw = Path(args.preflight).read_bytes()
        need(raw.endswith(b"\n") and b"\n" not in raw[:-1], "single preflight object")
        value = json.loads(raw[:-1])
        need(type(value) is dict and canonical(value) == raw[:-1], "canonical preflight")
        verified = verify_document(value)
        topology = independent_known_topology()
        result = {
            "schema": "cm2.round306c27r2.source-g-fresh-primitive-rebuild-preflight-independent-verification.v1",
            "status": "PASS_INDEPENDENT_PREFLIGHT_VERIFICATION__ZERO_CREDIT",
            "preflight": verified,
            "independent_algorithm": "ADJACENCY_LIST_BFS__NO_PRODUCER_IMPORT__NO_DSU_REUSE",
            "known_topology": topology,
            "formal_credit": 0,
        }
        result["verification_sha256"] = digest(result)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = canonical(result) + b"\n"
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                     | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            os.write(fd, payload)
            os.fsync(fd)
        finally:
            os.close(fd)
    except (Reject, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "verification_sha256": result["verification_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
