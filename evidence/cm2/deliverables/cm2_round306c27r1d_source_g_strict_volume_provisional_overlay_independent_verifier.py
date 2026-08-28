#!/usr/bin/env python3
"""Independent adjacency/BFS verifier for the append-only C27R1D overlay.

The producer's DSU code is never imported.  A real seed controls graph-edge,
component-start, and neighbor traversal order; all verified outputs remain
canonical and seed-independent.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from contextlib import contextmanager
import gzip
import hashlib
import json
import os
from pathlib import Path
import random
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
EDGE = WORKSPACE / ".cm2-runtime/audit/c27-same-chart-strict-volume-v1-seed-30632101-run3/candidate/cm2_c27_same_chart_strict_volume_totality_v1_component_edges.jsonl.gz"
C15 = ROOT / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
STRICT_RECEIPT = ROOT / "cm2_c27_same_chart_strict_volume_totality_subgate_receipt.json"
PINS = {
    EDGE: (2_157_061, "64cb62aa3b5ae298699ef5809e075ce6c2314baad1f589965e675c82deaa4632"),
    C15: (142_025_813, "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    STRICT_RECEIPT: (4_234, "22f8f8f6635a6083254311f5ee776e9ebe82b3192b0aadac6dc9585a0b0db3a4"),
}
STRICT_RECEIPT_OBJECT = "34277fdcb593186e9177e60d1c9fcef9969b732200231895d6c0b3a699621002"
PREFIX = "cm2_round306c27r1d_source_g_strict_volume_provisional_overlay"
PROMOTIONS = PREFIX + "_14772_edge_application_ledger.jsonl.gz"
ASSIGNMENTS = PREFIX + "_502204_member_assignment_ledger.jsonl.gz"
COMPONENTS = PREFIX + "_43772_component_census_ledger.jsonl.gz"
CLUSTERS = PREFIX + "_305_affected_cluster_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
EXPECTED_FILES = [PROMOTIONS, ASSIGNMENTS, COMPONENTS, CLUSTERS, RESULT]
NEW_NS = "round306c27r1d-strict-volume-provisional-source-g-component:"


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def stable_identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


@contextmanager
def pinned_input(path: Path, pin: tuple[int, str], label: str) -> Iterator[Any]:
    """Consume a pinned input from one stable O_NOFOLLOW file descriptor."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular single-link input:" + label)
        need(before.st_size == pin[0], "input size pin:" + label)
        state = hashlib.sha256()
        while block := stream.read(4 << 20):
            state.update(block)
        after_hash = os.fstat(stream.fileno())
        need(stable_identity(before) == stable_identity(after_hash), "input changed during hash:" + label)
        need(state.hexdigest() == pin[1], "input sha pin:" + label)
        stream.seek(0)
        yield stream
        after_parse = os.fstat(stream.fileno())
        need(stable_identity(before) == stable_identity(after_parse), "input changed during parse:" + label)


def rows_handle(stream: Any, label: str) -> Iterator[dict[str, Any]]:
    with gzip.GzipFile(filename="", fileobj=stream, mode="rb") as packed:
        for ordinal, line in enumerate(packed):
            need(line.endswith(b"\n"), f"newline:{label}:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"canonical:{label}:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(claimed == digest(body), f"closure:{label}:{ordinal}")
            yield row


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"canonical:{path.name}:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(claimed == digest(body), f"closure:{path.name}:{ordinal}")
            yield row


def identity(group: list[str]) -> dict[str, Any]:
    return {
        "schema": "cm2.round306c27r1d.strict-volume-provisional-component-identity.v1",
        "ordered_round306c15_component_ids": group,
        "qualification": "STRICT_VOLUME_EDGES_ONLY__PROVISIONAL_UPPER_BOUND",
    }


def pid(group: list[str]) -> str:
    return NEW_NS + digest(identity(group))


def edge_id(pair: tuple[str, str]) -> str:
    return "round306c27r1d-strict-volume-provisional-edge:" + digest({"ordered_C15_component_pair": list(pair)})


def exact(row: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    body = dict(row)
    body.pop("row_sha256", None)
    need(body == expected, label)


def strict_receipt_authority() -> dict[str, Any]:
    with pinned_input(STRICT_RECEIPT, PINS[STRICT_RECEIPT], "strict-volume subgate receipt") as stream:
        raw = stream.read()
    receipt = json.loads(raw)
    need(canonical(receipt) + b"\n" == raw, "canonical strict-volume receipt")
    body = dict(receipt)
    claimed = body.pop("receipt_sha256", None)
    need(claimed == STRICT_RECEIPT_OBJECT and claimed == digest(body), "strict-volume receipt object closure")
    need(receipt.get("schema") == "cm2.c27.same-chart-strict-volume-totality.v1.final-zero-credit-receipt.v1", "strict-volume receipt schema")
    need(receipt.get("formal_credit") == 0 and receipt.get("C27_C28_C29") == "REJECT_AND_REBUILD_REQUIRED", "strict-volume zero-credit qualification")
    census = receipt.get("exact_census")
    need(type(census) is dict and census.get("union_component_edge_count") == 14_772 and census.get("provisional_component_count_after_strict_volume_edges_only") == 43_772, "strict-volume receipt census")
    edge_meta = receipt.get("producer_replay", {}).get("ledgers", {}).get("cm2_c27_same_chart_strict_volume_totality_v1_component_edges.jsonl.gz")
    need(type(edge_meta) is dict and edge_meta.get("row_count") == 14_772 and edge_meta.get("sha256") == PINS[EDGE][1] and edge_meta.get("byte_identical_across_producer_seeds") is True, "sealed ledger authority binding")
    return receipt


def edge_authority(components: set[str], stream: Any) -> list[dict[str, Any]]:
    edge_rows = []
    seen = set()
    source_pairs = Counter()
    baseline = incremental = 0
    for ordinal, row in enumerate(rows_handle(stream, EDGE.name)):
        need(row.get("schema") == "cm2.c27.same-chart-strict-volume-totality.v1.component-edge-row.v1" and row.get("ordinal") == ordinal, "source edge schema/ordinal")
        pair = row.get("component_pair")
        need(type(pair) is list and len(pair) == 2 and pair == sorted(pair) and pair[0] != pair[1], "ordered edge")
        key = tuple(pair)
        need(key not in seen and all(value in components for value in pair), "unique C15-bound edge")
        seen.add(key)
        need(row.get("component_edge_id") == "same-chart-strict-volume-component-edge:" + digest(pair), "source edge identity")
        total, base, add = row["witness_occurrence_count"], row["baseline_occurrence_count"], row["incremental_occurrence_count"]
        need(type(total) is int and total > 0 and base + add == total, "source witness split")
        need(sum(row["source_pair_census"].values()) == total, "source pair total")
        source_pairs.update(row["source_pair_census"])
        need(row["edge_in_known_228_baseline"] is bool(base), "baseline flag")
        need(row["edge_has_incremental_nonidentical_overlap"] is bool(add), "incremental flag")
        need(row["edge_novel_beyond_known_228_baseline"] is (bool(add) and not bool(base)), "novel flag")
        need(row["provisional_only"] is True and row["formal_credit"] == 0, "zero-credit source edge")
        baseline += base
        incremental += add
        edge_rows.append(row)
    need(len(edge_rows) == 14_772 and baseline == 228 and incremental == 32_012, "source edge census")
    need(source_pairs == Counter({"C19B__C22A": 3668, "C19C__C22A": 28344, "C22A__C22A": 228}), "source pair census")
    return edge_rows


def bfs_groups(sizes: dict[str, int], edges: list[dict[str, Any]], seed: int) -> tuple[list[list[str]], dict[str, set[str]]]:
    rng = random.Random(seed)
    insertion = list(edges)
    rng.shuffle(insertion)
    adjacency: dict[str, set[str]] = {component: set() for component in sizes}
    for row in insertion:
        left, right = row["component_pair"]
        adjacency[left].add(right)
        adjacency[right].add(left)
    starts = list(sizes)
    rng.shuffle(starts)
    seen = set()
    groups = []
    for start in starts:
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        group = []
        while queue:
            current = queue.popleft()
            group.append(current)
            neighbors = list(adjacency[current])
            rng.shuffle(neighbors)
            for neighbor in neighbors:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        groups.append(sorted(group))
    need(len(seen) == len(sizes), "BFS vertex exhaustion")
    groups.sort(key=pid)
    return groups, adjacency


def compact_expected(authority: dict[str, Any], seed: int = 1) -> dict[str, Any]:
    sizes = authority.get("old_component_sizes")
    edge_rows = authority.get("edges")
    members = authority.get("members")
    need(type(sizes) is dict and sizes and all(type(value) is int and value > 0 for value in sizes.values()), "compact sizes")
    need(type(edge_rows) is list and len(edge_rows) > 0, "compact edges")
    normalized = []
    pairs = set()
    for row in edge_rows:
        pair = row.get("pair")
        need(type(pair) is list and len(pair) == 2 and pair == sorted(pair) and pair[0] != pair[1], "compact pair")
        need(all(value in sizes for value in pair), "compact endpoints")
        need(row.get("edge_id") == "sealed-edge:" + digest(pair), "compact edge id")
        need(row.get("authority") == "SAME_CHART_STRICT_POSITIVE_VOLUME_INTERIOR_INTERSECTION", "compact same-chart authority")
        need(tuple(pair) not in pairs, "compact unique edge")
        pairs.add(tuple(pair))
        normalized.append({"component_pair": pair})
    groups, _ = bfs_groups(sizes, normalized, seed)
    home = {old: pid(group) for group in groups for old in group}
    need(type(members) is list and len({row["member_id"] for row in members}) == sum(sizes.values()), "compact member universe")
    observed = Counter(row["old_component_id"] for row in members)
    need(dict(observed) == sizes, "compact member size binding")
    old_within = sum(value * (value - 1) // 2 for value in sizes.values())
    new_sizes = [sum(sizes[old] for old in group) for group in groups]
    new_within = sum(value * (value - 1) // 2 for value in new_sizes)
    total = sum(sizes.values())
    return {
        "edge_applications": [{"pair": list(pair), "edge_id": "sealed-edge:" + digest(list(pair)), "authority": "SAME_CHART_STRICT_POSITIVE_VOLUME_INTERIOR_INTERSECTION"} for pair in sorted(pairs)],
        "components": [{"id": pid(group), "old_ids": group, "member_count": sum(sizes[old] for old in group)} for group in groups],
        "member_assignments": [{"member_id": row["member_id"], "old_component_id": row["old_component_id"], "provisional_component_id": home[row["old_component_id"]]} for row in sorted(members, key=lambda row: row["member_id"])],
        "summary": {
            "members": total, "edges": len(pairs), "old_components": len(sizes), "provisional_components": len(groups),
            "rank_reduction": len(sizes) - len(groups), "newly_internalized_pairs": new_within - old_within,
            "cross_denominator": total * (total - 1) // 2 - new_within,
            "formal_credit": 0, "qualification": "STRICT_VOLUME_ONLY__PROVISIONAL_UPPER_BOUND",
            "C27_C28_C29": "UNAUTHORIZED",
        },
    }


def validate_compact(authority: dict[str, Any], candidate: dict[str, Any], seed: int = 1) -> None:
    need(candidate == compact_expected(authority, seed), "compact exact reconstruction")


def verify(candidate: Path, seed: int) -> dict[str, Any]:
    need(type(seed) is int and seed > 0, "real positive verifier seed")
    strict_receipt = strict_receipt_authority()
    need(candidate.is_dir() and not candidate.is_symlink(), "candidate directory")
    need(set(item.name for item in candidate.iterdir()) == set(EXPECTED_FILES), "exclusive candidate files")

    members = []
    sizes = Counter()
    member_ids = set()
    with pinned_input(C15, PINS[C15], "C15 member ledger") as stream:
        for ordinal, row in enumerate(rows_handle(stream, C15.name)):
            need(row["member_ordinal"] == ordinal, "C15 member ordinal")
            member = row["registry_member_id"]
            need(member not in member_ids, "unique member")
            member_ids.add(member)
            sizes[row["fresh_component_id"]] += 1
            members.append({"ordinal": ordinal, "member_id": member, "old_component": row["fresh_component_id"], "source_row_id": row["row_id"], "source_row_sha256": row["row_sha256"]})
    need(len(members) == 502_204 and len(sizes) == 57_876, "C15 census")
    with pinned_input(EDGE, PINS[EDGE], "strict-volume edge ledger") as stream:
        edges = edge_authority(set(sizes), stream)
    groups, adjacency = bfs_groups(dict(sizes), edges, seed)
    need(len(groups) == 43_772 and sum(len(group) - 1 for group in groups) == 14_104, "BFS component/rank census")
    affected = [group for group in groups if len(group) > 1]
    need(len(affected) == 305 and sum(map(len, affected)) == 14_409, "BFS affected census")
    home = {old: group for group in groups for old in group}
    new_id = {old: pid(home[old]) for old in sizes}
    edge_by_pair = {tuple(row["component_pair"]): row for row in edges}
    incident: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for pair in edge_by_pair:
        need(new_id[pair[0]] == new_id[pair[1]], "edge internalization")
        incident[new_id[pair[0]]].append(pair)

    promotion_rows = rows(candidate / PROMOTIONS)
    count = 0
    for source, candidate_row in zip((edge_by_pair[pair] for pair in sorted(edge_by_pair)), promotion_rows):
        pair = tuple(source["component_pair"])
        expected = {
            "schema": "cm2.round306c27r1d.strict-volume-provisional-edge-application-row.v1",
            "edge_application_id": edge_id(pair), "ordered_round306c15_component_pair": list(pair),
            "source_component_edge_id": source["component_edge_id"], "source_component_edge_row_sha256": source["row_sha256"],
            "witness_occurrence_count": source["witness_occurrence_count"], "unique_member_pair_count": source["unique_member_pair_count"],
            "source_pair_census": source["source_pair_census"], "baseline_occurrence_count": source["baseline_occurrence_count"],
            "incremental_occurrence_count": source["incremental_occurrence_count"],
            "sealed_edge_authority": "SAME_CHART_STRICT_POSITIVE_VOLUME_INTERIOR_INTERSECTION",
            "both_endpoints_bound_to_C15": True, "application_status": "CERTAIN_EDGE_INTERNALIZED_IN_PROVISIONAL_PARTITION",
            "overlay_qualification": "STRICT_VOLUME_ONLY__PROVISIONAL_UPPER_BOUND", "formal_credit": 0,
        }
        exact(candidate_row, expected, "exact promotion row")
        count += 1
    need(count == 14_772 and next(promotion_rows, None) is None, "promotion exhaustion")

    cluster_rows = rows(candidate / CLUSTERS)
    count = 0
    for group, candidate_row in zip(sorted(affected, key=pid), cluster_rows):
        component = pid(group)
        pairs = sorted(incident[component])
        expected = {
            "schema": "cm2.round306c27r1d.strict-volume-provisional-affected-cluster-row.v1",
            "provisional_component_id": component, "identity_preimage": identity(group), "old_C15_component_count": len(group),
            "old_C15_component_ids_sha256": digest(group), "strict_volume_edge_count": len(pairs),
            "strict_volume_edge_application_ids_sha256": digest([edge_id(pair) for pair in pairs]),
            "member_count": sum(sizes[old] for old in group),
            "overlay_qualification": "STRICT_VOLUME_ONLY__PROVISIONAL_UPPER_BOUND", "formal_credit": 0,
        }
        exact(candidate_row, expected, "exact cluster row")
        count += 1
    need(count == 305 and next(cluster_rows, None) is None, "cluster exhaustion")

    component_rows = rows(candidate / COMPONENTS)
    count = 0
    for ordinal, (group, candidate_row) in enumerate(zip(groups, component_rows)):
        expected = {
            "schema": "cm2.round306c27r1d.strict-volume-provisional-component-census-row.v1",
            "component_ordinal": ordinal, "provisional_component_id": pid(group), "identity_preimage": identity(group),
            "old_C15_component_count": len(group), "old_C15_component_ids_sha256": digest(group),
            "member_count": sum(sizes[old] for old in group), "affected_by_strict_volume_edge": len(group) > 1,
            "overlay_qualification": "STRICT_VOLUME_ONLY__PROVISIONAL_UPPER_BOUND", "formal_credit": 0,
        }
        exact(candidate_row, expected, "exact component row")
        count += 1
    need(count == 43_772 and next(component_rows, None) is None, "component exhaustion")

    assignment_rows = rows(candidate / ASSIGNMENTS)
    count = 0
    for source, candidate_row in zip(members, assignment_rows):
        expected = {
            "schema": "cm2.round306c27r1d.strict-volume-provisional-member-assignment-row.v1",
            "member_ordinal": source["ordinal"], "registry_member_id": source["member_id"],
            "round306c15_component_id": source["old_component"], "provisional_component_id": new_id[source["old_component"]],
            "round306c15_source_row_id": source["source_row_id"], "round306c15_source_row_sha256": source["source_row_sha256"],
            "unique_assignment": True, "overlay_qualification": "STRICT_VOLUME_ONLY__PROVISIONAL_UPPER_BOUND", "formal_credit": 0,
        }
        exact(candidate_row, expected, "exact assignment row")
        count += 1
    need(count == 502_204 and next(assignment_rows, None) is None, "assignment exhaustion")

    old_within = sum(value * (value - 1) // 2 for value in sizes.values())
    new_sizes = [sum(sizes[old] for old in group) for group in groups]
    new_within = sum(value * (value - 1) // 2 for value in new_sizes)
    total = 502_204 * 502_203 // 2
    need((new_within - old_within, total - new_within) == (24_956_788, 125_591_518_882), "denominator arithmetic")

    result_path = candidate / RESULT
    raw = result_path.read_bytes()
    result = json.loads(raw)
    need(canonical(result) + b"\n" == raw, "canonical result")
    body = dict(result)
    claimed = body.pop("result_object_sha256", None)
    need(claimed == digest(body), "result closure")
    need(result["status"] == "PASS_APPEND_ONLY_STRICT_VOLUME_PROVISIONAL_UPPER_BOUND__ZERO_FORMAL_CREDIT" and result["formal_credit"] == 0, "result status")
    need(result["input_sha256"] == {"strict_volume_component_edges": PINS[EDGE][1], "C15_member_assignments": PINS[C15][1]}, "result inputs")
    need(result["partition_census"] == {"members": 502204, "old_C15_components": 57876, "provisional_components": 43772, "affected_old_component_vertices": 14409, "affected_connected_clusters": 305, "forced_rank_reduction": 14104, "newly_internalized_unordered_member_pairs": 24956788, "provisional_cross_component_pair_denominator": 125591518882}, "result partition census")
    need(result["qualification"]["C27"] == result["qualification"]["C28"] == result["qualification"]["C29"] == "UNAUTHORIZED", "chain unauthorized")
    need(set(result["outputs"]) == {"edge_application_ledger", "affected_cluster_ledger", "component_census_ledger", "member_assignment_ledger"}, "output roles")
    for meta in result["outputs"].values():
        path = candidate / meta["filename"]
        need(path.stat().st_size == meta["size"] and fsha(path) == meta["sha256"], "result output pin")

    verification = {
        "schema": "cm2.round306c27r1d.strict-volume-provisional-overlay-independent-verification.v1",
        "status": "PASS_INDEPENDENT_ADJACENCY_BFS__PROVISIONAL_UPPER_BOUND_ONLY",
        "implementation": "ADJACENCY_LIST_AND_RANDOMIZED_BFS__NO_DSU_IMPORT_OR_REUSE",
        "formal_credit": 0, "members": 502204, "strict_volume_edges": 14772,
        "old_components": 57876, "provisional_components": 43772, "affected_vertices": 14409,
        "affected_clusters": 305, "rank_reduction": 14104,
        "newly_internalized_unordered_member_pairs": 24956788,
        "provisional_cross_component_pair_denominator": 125591518882,
        "strict_volume_subgate_receipt": {
            "file_sha256": PINS[STRICT_RECEIPT][1], "object_sha256": strict_receipt["receipt_sha256"],
            "sealed_component_edge_ledger_sha256": PINS[EDGE][1], "sealed_component_edge_row_count": 14772,
            "authority_inherited": True,
        },
        "C27": "UNAUTHORIZED", "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        "candidate_files_sha256": {name: fsha(candidate / name) for name in EXPECTED_FILES},
    }
    verification["verification_object_sha256"] = digest(verification)
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    value = verify(args.candidate.resolve(), args.seed)
    payload = canonical(value) + b"\n"
    need(not args.out.exists(), "no-clobber verification")
    args.out.write_bytes(payload)
    os.sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "REJECT", "error": str(error)}, sort_keys=True), file=os.sys.stderr)
        raise SystemExit(2)
