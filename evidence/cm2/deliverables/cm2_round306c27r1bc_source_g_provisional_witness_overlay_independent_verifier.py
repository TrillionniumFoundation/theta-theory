#!/usr/bin/env python3
"""Independent graph/BFS verifier for the C27R1-B/C provisional overlay.

The producer's DSU implementation is not imported.  This verifier rebuilds
the witness graph as adjacency lists, computes connected components by BFS,
and checks every materialized row against pinned primitive/C15 authority.
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
WITNESS = WORKSPACE / ".cm2-runtime/audit/c27-same-chart-exact-equal-sqlite-seed-30629101/cm2_c27_same_chart_exact_equal_cross_component_witness_groups.jsonl.gz"
MEMBER = ROOT / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
CENSUS = ROOT / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_component_census_ledger.jsonl.gz"
PINS = {
    WITNESS: (161323, "70e588cf83942c243cdac0c634ad348bc78ce7090ae01e2e36cd6d6b84717644"),
    MEMBER: (142025813, "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    CENSUS: (7599313, "eedeae91c8986440b41e5e5e1a1e65bf74e9c37add2d858b1d6b9b55e99a142c"),
}
PREFIX = "cm2_round306c27r1bc_source_g_provisional_witness_overlay"
PROMOTIONS = PREFIX + "_192_edge_promotion_ledger.jsonl.gz"
ASSIGNMENTS = PREFIX + "_502204_member_assignment_ledger.jsonl.gz"
COMPONENTS = PREFIX + "_57684_component_census_ledger.jsonl.gz"
CLUSTERS = PREFIX + "_120_affected_cluster_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
NEW_NS = "round306c27r1-provisional-source-g-component:"


class Reject(RuntimeError): pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value: raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024): state.update(block)
    return state.hexdigest()


def rows(path: Path, group: bool = False) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            raw = line[:-1]; row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"canonical:{path.name}:{ordinal}")
            body = dict(row); claimed = body.pop("group_row_sha256" if group else "row_sha256", None)
            need(type(claimed) is str and claimed == digest(body), f"closure:{path.name}:{ordinal}")
            yield row


def identity(group: list[str]) -> dict[str, Any]:
    return {"schema": "cm2.round306c27r1.provisional-component-identity.v1", "ordered_round306c15_component_ids": group, "qualification": "WITNESS_ONLY_PROVISIONAL_EQUIVALENCE_CLASS"}


def pid(group: list[str]) -> str: return NEW_NS + digest(identity(group))


def qvolume(bounds: list[dict[str, Any]]) -> str:
    need(type(bounds) is list and len(bounds) == 6, "six witness bounds")
    values = []
    for endpoint in bounds:
        need(type(endpoint) is dict and endpoint.get("kind") == "Q" and type(endpoint.get("value")) is str, "rational witness endpoint")
        values.append(Fraction(endpoint["value"]))
    widths = [values[1] - values[0], values[3] - values[2], values[5] - values[4]]
    need(all(width > 0 for width in widths), "strict positive witness widths")
    volume = widths[0] * widths[1] * widths[2]
    return str(volume.numerator) if volume.denominator == 1 else f"{volume.numerator}/{volume.denominator}"


def exact_body(row: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    body = dict(row); body.pop("row_sha256", None)
    need(body == expected, label)


def compact_expected(authority: dict[str, Any]) -> dict[str, Any]:
    """Independent small-model oracle used by the coherent attack harness."""
    sizes = authority.get("old_component_sizes")
    witnesses = authority.get("witnesses")
    need(type(sizes) is dict and sizes and all(type(k) is str and type(v) is int and v > 0 for k, v in sizes.items()), "compact authority sizes")
    need(type(witnesses) is list and len(witnesses) > 0, "compact authority witnesses")
    edge_groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    for witness in witnesses:
        pair = witness.get("pair"); need(type(pair) is list and len(pair) == 2 and pair == sorted(pair) and pair[0] != pair[1], "compact witness pair")
        need(all(item in sizes for item in pair), "compact witness endpoints")
        need(Fraction(witness.get("volume")) > 0 and type(witness.get("group_id")) is str, "compact strict witness")
        edge_groups[tuple(pair)].append(witness["group_id"])
    adjacency: dict[str, set[str]] = defaultdict(set)
    for left, right in edge_groups: adjacency[left].add(right); adjacency[right].add(left)
    seen: set[str] = set(); groups = []
    for start in sorted(sizes):
        if start in seen: continue
        queue = deque([start]); seen.add(start); group = []
        while queue:
            current = queue.popleft(); group.append(current)
            for neighbor in sorted(adjacency[current]):
                if neighbor not in seen: seen.add(neighbor); queue.append(neighbor)
        groups.append(sorted(group))
    groups.sort(key=pid); home = {old: pid(group) for group in groups for old in group}
    assignments = sorted(authority.get("members", []), key=lambda row: row["member_id"])
    need(len({row["member_id"] for row in assignments}) == sum(sizes.values()), "compact member universe")
    observed = defaultdict(int)
    for row in assignments:
        need(row["old_component_id"] in sizes, "compact member old home"); observed[row["old_component_id"]] += 1
    need(dict(observed) == sizes, "compact member size binding")
    total_members = sum(sizes.values()); old_within = sum(v * (v - 1) // 2 for v in sizes.values())
    new_sizes = [sum(sizes[old] for old in group) for group in groups]; new_within = sum(v * (v - 1) // 2 for v in new_sizes)
    return {
        "promotion_edges": [{"pair": list(pair), "group_ids": sorted(ids)} for pair, ids in sorted(edge_groups.items())],
        "components": [{"id": pid(group), "old_ids": group, "member_count": sum(sizes[old] for old in group)} for group in groups],
        "member_assignments": [{"member_id": row["member_id"], "old_component_id": row["old_component_id"], "provisional_component_id": home[row["old_component_id"]]} for row in assignments],
        "summary": {"formal_credit": 0, "qualification": "PROVISIONAL_UPPER_BOUND_ONLY", "old_C27_C28_C29": "REJECT", "members": total_members, "edges": len(edge_groups), "components": len(groups), "rank_reduction": len(sizes) - len(groups), "newly_internalized_pairs": new_within - old_within, "cross_denominator": total_members * (total_members - 1) // 2 - new_within},
    }


def validate_compact_attack_model(authority: dict[str, Any], candidate: dict[str, Any]) -> None:
    need(candidate == compact_expected(authority), "compact candidate exact semantic reconstruction")


def verify(candidate: Path) -> dict[str, Any]:
    for path, (size, sha) in PINS.items():
        info = path.stat(); need(path.is_file() and not path.is_symlink() and info.st_nlink == 1 and info.st_size == size and fsha(path) == sha, "input pin:" + path.name)
    expected_files = [PROMOTIONS, ASSIGNMENTS, COMPONENTS, CLUSTERS, RESULT]
    need(set(item.name for item in candidate.iterdir()) == set(expected_files), "exclusive candidate file set")
    for name in expected_files:
        path = candidate / name; info = path.stat()
        need(path.is_file() and not path.is_symlink() and info.st_nlink == 1, "regular candidate:" + name)

    witness_rows = list(rows(WITNESS, group=True))
    need(len(witness_rows) == 228, "228 witness rows")
    witness_members = {member["owner_member_id"] for row in witness_rows for member in row["members"]}
    bindings: dict[str, tuple[str, str]] = {}
    member_count = 0
    for source in rows(MEMBER):
        member_count += 1
        if source["registry_member_id"] in witness_members:
            bindings[source["registry_member_id"]] = (source["fresh_component_id"], source["row_sha256"])
    need(member_count == 502_204 and len(bindings) == len(witness_members) == 456, "C15 witness bindings")

    edge_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for witness in witness_rows:
        need(witness.get("legal_cross_component_physical_witness") is True and witness.get("witness_reason") == "DISTINCT_C15_COMPONENTS_SHARE_THE_SAME_NONEMPTY_OPEN_3D_INTERIOR_IN_ONE_CHART", "legal open-box witness")
        need(witness.get("member_count") == witness.get("component_count") == 2, "binary witness")
        volume = qvolume(witness["physical_bounds"])
        proof = witness.get("strict_positive_volume_proof")
        need(type(proof) is dict and proof.get("exact_positive_rational_volume") == volume and proof.get("common_open_interior_nonempty") is True, "independent volume proof")
        comps = []
        for member in witness["members"]:
            need(member["owner_member_id"] in bindings, "bound witness member")
            comp, row_sha = bindings[member["owner_member_id"]]
            need(member["fresh_component_id"] == comp and member["C15_member_row_sha256"] == row_sha, "C15 binding exact")
            need(member["chart"] == witness["chart"] and member["physical_bounds"] == witness["physical_bounds"] and member["source_kernel"] == "C22A", "support equality")
            comps.append(comp)
        pair = tuple(sorted(comps)); need(pair[0] != pair[1] and list(pair) == witness["fresh_component_ids"], "strict cross-component pair")
        edge_groups[pair].append(witness)
    need(len(edge_groups) == 192, "192 independently deduplicated edges")

    sizes: dict[str, int] = {}
    for source in rows(CENSUS):
        need(source["fresh_component_id"] not in sizes and source["member_count"] > 0, "unique old component")
        sizes[source["fresh_component_id"]] = source["member_count"]
    need(len(sizes) == 57_876 and sum(sizes.values()) == 502_204, "old partition census")

    adjacency: dict[str, set[str]] = defaultdict(set)
    for left, right in edge_groups:
        need(left in sizes and right in sizes, "edge endpoints in old partition")
        adjacency[left].add(right); adjacency[right].add(left)
    seen: set[str] = set(); groups: list[list[str]] = []
    for start in sorted(sizes):
        if start in seen: continue
        queue = deque([start]); seen.add(start); group = []
        while queue:
            current = queue.popleft(); group.append(current)
            for neighbor in sorted(adjacency[current]):
                if neighbor not in seen: seen.add(neighbor); queue.append(neighbor)
        groups.append(sorted(group))
    groups.sort(key=pid)
    need(len(groups) == 57_684 and sum(len(group) - 1 for group in groups) == 192, "BFS partition and rank")
    affected = [group for group in groups if len(group) > 1]
    need(len(affected) == 120 and sum(map(len, affected)) == 312, "affected clusters")
    group_of = {old: group for group in groups for old in group}; pid_of = {old: pid(group_of[old]) for old in sizes}

    promotion_rows = list(rows(candidate / PROMOTIONS))
    need(len(promotion_rows) == 192, "promotion row census")
    for candidate_row, pair in zip(promotion_rows, sorted(edge_groups)):
        supporting = sorted(edge_groups[pair], key=lambda row: row["group_id"])
        expected = {
            "schema": "cm2.round306c27r1-b.provisional-certain-edge-promotion-row.v1",
            "provisional_edge_id": "round306c27r1-provisional-certain-edge:" + digest({"ordered_C15_component_pair": list(pair)}),
            "ordered_C15_component_pair": list(pair),
            "witness_group_count": len(supporting),
            "witness_group_ids": [row["group_id"] for row in supporting],
            "witness_group_ids_sha256": digest([row["group_id"] for row in supporting]),
            "strict_positive_rational_volumes": [row["strict_positive_volume_proof"]["exact_positive_rational_volume"] for row in supporting],
            "all_witnesses_strict_positive_open_interior": True,
            "logical_edge_status": "CERTAIN_LEGAL_PHYSICAL_EDGE",
            "overlay_qualification": "PROVISIONAL_UPPER_BOUND_ONLY",
            "formal_credit": 0,
        }
        exact_body(candidate_row, expected, "exact promotion row")

    incident: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for pair in edge_groups: incident[pid_of[pair[0]]].append(pair)
    cluster_rows = list(rows(candidate / CLUSTERS)); need(len(cluster_rows) == 120, "cluster row census")
    for candidate_row, group in zip(cluster_rows, sorted(affected, key=pid)):
        component_id = pid(group); pairs = sorted(incident[component_id])
        expected = {
            "schema": "cm2.round306c27r1-c.provisional-affected-cluster-row.v1", "provisional_component_id": component_id,
            "identity_preimage": identity(group), "old_C15_component_count": len(group), "old_C15_component_ids_sha256": digest(group),
            "certain_edge_count": len(pairs),
            "certain_edge_ids_sha256": digest(["round306c27r1-provisional-certain-edge:" + digest({"ordered_C15_component_pair": list(pair)}) for pair in pairs]),
            "member_count": sum(sizes[old] for old in group), "overlay_qualification": "PROVISIONAL_UPPER_BOUND_ONLY", "formal_credit": 0,
        }
        exact_body(candidate_row, expected, "exact cluster row")

    component_rows = rows(candidate / COMPONENTS)
    observed_components = 0
    for ordinal, (candidate_row, group) in enumerate(zip(component_rows, groups)):
        expected = {
            "schema": "cm2.round306c27r1-c.provisional-component-census-row.v1", "component_ordinal": ordinal,
            "provisional_component_id": pid(group), "identity_preimage": identity(group), "old_C15_component_count": len(group),
            "old_C15_component_ids_sha256": digest(group), "member_count": sum(sizes[old] for old in group),
            "affected_by_same_chart_witness_promotion": len(group) > 1, "overlay_qualification": "PROVISIONAL_UPPER_BOUND_ONLY", "formal_credit": 0,
        }
        exact_body(candidate_row, expected, "exact component row"); observed_components += 1
    need(observed_components == len(groups) and next(component_rows, None) is None, "component exhaustion")

    candidate_assignments = rows(candidate / ASSIGNMENTS)
    assignment_count = 0
    for source, candidate_row in zip(rows(MEMBER), candidate_assignments):
        expected = {
            "schema": "cm2.round306c27r1-c.provisional-member-assignment-row.v1", "member_ordinal": source["member_ordinal"],
            "registry_member_id": source["registry_member_id"], "round306c15_component_id": source["fresh_component_id"],
            "provisional_component_id": pid_of[source["fresh_component_id"]], "round306c15_source_row_id": source["row_id"],
            "round306c15_source_row_sha256": source["row_sha256"], "overlay_qualification": "PROVISIONAL_UPPER_BOUND_ONLY", "formal_credit": 0,
        }
        exact_body(candidate_row, expected, "exact member assignment"); assignment_count += 1
    need(assignment_count == 502_204 and next(candidate_assignments, None) is None, "member assignment exhaustion")

    new_sizes = [sum(sizes[old] for old in group) for group in groups]
    old_within = sum(count * (count - 1) // 2 for count in sizes.values())
    new_within = sum(count * (count - 1) // 2 for count in new_sizes)
    total = 502_204 * 502_203 // 2
    need(new_within - old_within == 691_416 and total - new_within == 125_615_784_254, "pair denominator arithmetic")

    result_path = candidate / RESULT
    result = json.loads(result_path.read_bytes()); need(canonical(result) + b"\n" == result_path.read_bytes(), "canonical result")
    claimed = result.pop("result_object_sha256", None); need(claimed == digest(result), "result object closure")
    need(result.get("status") == "PASS_PROVISIONAL_UPPER_BOUND_ONLY__ZERO_FORMAL_CREDIT" and result.get("formal_credit") == 0, "zero-credit result")
    need(result.get("authority") == "APPEND_ONLY_WITNESS_ONLY_OVERLAY__NOT_A_FORMAL_SUCCESSOR_SEAL", "provisional authority limit")
    need(result.get("old_C27_C28_C29") == "REJECT__NOT_READ_NOT_MODIFIED_NOT_REUSED", "old chain rejection")
    need(result.get("input_sha256") == {"witness": PINS[WITNESS][1], "member": PINS[MEMBER][1], "census": PINS[CENSUS][1]}, "result input pins")
    need(result.get("witness_census") == {"groups": 228, "unique_component_edges": 192, "all_edges_strictly_witnessed": True}, "result witness census")
    need(result["partition_census"] == {"members": 502204, "old_C15_components": 57876, "provisional_components": 57684, "affected_old_component_vertices": 312, "affected_connected_clusters": 120, "forced_rank_reduction": 192, "newly_internalized_member_pairs": 691416, "provisional_cross_component_pair_denominator": 125615784254}, "result census")
    need(result.get("qualification") == {"component_count": "UPPER_BOUND_ON_ANY_EVENTUAL_COMPONENT_COUNT", "rank_reduction": "LOWER_BOUND_ON_EVENTUAL_RANK_REDUCTION", "not_closed": ["SAME_CHART_RELATIVE_CELLS_TOTALITY", "SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES", "POSITIVE_VOLUME_CARRIERS", "TWENTY_FAMILY_PHYSICAL_TOTALITY_AND_UNIQUE_ASSIGNMENT", "C28R1_MAXIMALITY", "C29R1_GLOBAL_DISPOSITIONS"], "C28": "REJECT", "C29": "REJECT", "CM2": "NO-GO_FOR_CLAIM"}, "open-gate qualification")
    need(set(result.get("outputs", {})) == {"promotion_ledger", "affected_cluster_ledger", "component_census_ledger", "member_assignment_ledger"}, "result output roles")
    for role, meta in result["outputs"].items():
        path = candidate / meta["filename"]
        need(path.stat().st_size == meta["size"] and fsha(path) == meta["sha256"], "output hash pin:" + role)
    return {
        "schema": "cm2.round306c27r1-bc.provisional-witness-overlay-independent-verification.v1",
        "status": "PASS_INDEPENDENT_GRAPH_BFS_VERIFICATION__PROVISIONAL_UPPER_BOUND_ONLY",
        "formal_credit": 0, "witness_groups": 228, "unique_component_edges": 192, "members": 502204,
        "provisional_components": 57684, "affected_clusters": 120, "rank_reduction": 192,
        "newly_internalized_member_pairs": 691416, "provisional_cross_component_pair_denominator": 125615784254,
        "C28": "REJECT", "C29": "REJECT", "CM2": "NO-GO_FOR_CLAIM",
        "candidate_files_sha256": {name: fsha(candidate / name) for name in expected_files},
    }


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--candidate", type=Path, required=True); parser.add_argument("--out", type=Path)
    args = parser.parse_args(); result = verify(args.candidate); result["verification_object_sha256"] = digest(result)
    payload = canonical(result) + b"\n"
    if args.out:
        need(not args.out.exists(), "no-clobber verifier output")
        args.out.write_bytes(payload)
    os.sys.stdout.buffer.write(payload); return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except (Reject, OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "REJECT", "error": str(error)}, sort_keys=True), file=os.sys.stderr); raise SystemExit(2)
