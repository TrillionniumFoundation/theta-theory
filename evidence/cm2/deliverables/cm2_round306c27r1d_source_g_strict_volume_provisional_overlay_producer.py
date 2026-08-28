#!/usr/bin/env python3
"""Append-only C27R1D strict-volume provisional overlay producer.

Inputs are exactly the sealed 14,772 strict-volume component-edge ledger and
the frozen C15 502,204-member assignment ledger.  The edge application order
is controlled by a real seed; every output is canonicalized independently of
that order.  No C27/C28/C29 artifact or previous overlay is read or modified.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
import gzip
import hashlib
import json
import os
from pathlib import Path
import random
import stat
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
EDGE_DEFAULT = WORKSPACE / ".cm2-runtime/audit/c27-same-chart-strict-volume-v1-seed-30632101-run3/candidate/cm2_c27_same_chart_strict_volume_totality_v1_component_edges.jsonl.gz"
C15 = ROOT / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
PINS = {
    "strict_volume_edges": (2_157_061, "64cb62aa3b5ae298699ef5809e075ce6c2314baad1f589965e675c82deaa4632"),
    "C15_members": (142_025_813, "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
}
PREFIX = "cm2_round306c27r1d_source_g_strict_volume_provisional_overlay"
PROMOTIONS = PREFIX + "_14772_edge_application_ledger.jsonl.gz"
ASSIGNMENTS = PREFIX + "_502204_member_assignment_ledger.jsonl.gz"
COMPONENTS = PREFIX + "_43772_component_census_ledger.jsonl.gz"
CLUSTERS = PREFIX + "_305_affected_cluster_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
NEW_NS = "round306c27r1d-strict-volume-provisional-source-g-component:"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


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
    """Hash and consume one immutable open-file capture, never a reopened path."""
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


def rows(stream: Any, label: str) -> Iterator[dict[str, Any]]:
    with gzip.GzipFile(filename="", fileobj=stream, mode="rb") as packed:
        for ordinal, line in enumerate(packed):
            need(line.endswith(b"\n"), f"newline:{label}:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"canonical:{label}:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == digest(body), f"row closure:{label}:{ordinal}")
            yield row


def identity(old_ids: list[str]) -> dict[str, Any]:
    return {
        "schema": "cm2.round306c27r1d.strict-volume-provisional-component-identity.v1",
        "ordered_round306c15_component_ids": old_ids,
        "qualification": "STRICT_VOLUME_EDGES_ONLY__PROVISIONAL_UPPER_BOUND",
    }


def provisional_id(old_ids: list[str]) -> str:
    return NEW_NS + digest(identity(old_ids))


def edge_application_id(pair: tuple[str, str]) -> str:
    return "round306c27r1d-strict-volume-provisional-edge:" + digest({"ordered_C15_component_pair": list(pair)})


def closed(body: dict[str, Any]) -> bytes:
    return canonical({**body, "row_sha256": digest(body)}) + b"\n"


def write_gzip(path: Path, values: Iterable[bytes]) -> dict[str, Any]:
    need(not path.exists(), "no clobber:" + path.name)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=False) as raw:
            with gzip.GzipFile(filename="", fileobj=raw, mode="wb", compresslevel=9, mtime=0) as packed:
                for value in values:
                    packed.write(value)
            raw.flush()
            os.fsync(raw.fileno())
    finally:
        os.close(fd)
    return {"filename": path.name, "size": path.stat().st_size, "sha256": fsha(path)}


def write_json(path: Path, value: dict[str, Any]) -> dict[str, Any]:
    payload = canonical(value) + b"\n"
    need(not path.exists(), "no clobber:" + path.name)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    return {"filename": path.name, "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


class DSU:
    def __init__(self, items: Iterable[str]) -> None:
        self.items = sorted(items)
        self.index = {item: ordinal for ordinal, item in enumerate(self.items)}
        self.parent = list(range(len(self.items)))
        self.weight = [1] * len(self.items)

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: str, right: str) -> int:
        a, b = self.find(self.index[left]), self.find(self.index[right])
        if a == b:
            return 0
        if self.weight[a] < self.weight[b] or (self.weight[a] == self.weight[b] and self.items[a] > self.items[b]):
            a, b = b, a
        self.parent[b] = a
        self.weight[a] += self.weight[b]
        return 1

    def groups(self) -> list[list[str]]:
        grouped: dict[int, list[str]] = defaultdict(list)
        for ordinal, item in enumerate(self.items):
            grouped[self.find(ordinal)].append(item)
        return sorted((sorted(group) for group in grouped.values()), key=provisional_id)


def load_edges(path: Path, components: set[str]) -> list[dict[str, Any]]:
    output = []
    pairs = set()
    source_pairs = Counter()
    baseline_occurrences = incremental_occurrences = 0
    baseline_edges = incremental_edges = 0
    with pinned_input(path, PINS["strict_volume_edges"], "strict-volume edge ledger") as stream:
        for ordinal, row in enumerate(rows(stream, path.name)):
            need(row.get("schema") == "cm2.c27.same-chart-strict-volume-totality.v1.component-edge-row.v1", "edge schema")
            need(row.get("ordinal") == ordinal, "edge ordinal")
            pair = row.get("component_pair")
            need(type(pair) is list and len(pair) == 2 and pair == sorted(pair) and pair[0] != pair[1], "ordered nonself edge")
            pair_tuple = tuple(pair)
            need(pair_tuple not in pairs and all(value in components for value in pair), "unique C15-bound edge")
            pairs.add(pair_tuple)
            need(row.get("component_edge_id") == "same-chart-strict-volume-component-edge:" + digest(pair), "source edge identity")
            total = row.get("witness_occurrence_count")
            base, increment = row.get("baseline_occurrence_count"), row.get("incremental_occurrence_count")
            need(type(total) is int and total > 0 and type(base) is int and type(increment) is int and base + increment == total, "witness count split")
            census = row.get("source_pair_census")
            need(type(census) is dict and sum(census.values()) == total and set(census) <= {"C19B__C22A", "C19C__C22A", "C22A__C22A"}, "source pair census")
            source_pairs.update(census)
            need(row.get("edge_in_known_228_baseline") is bool(base), "baseline flag")
            need(row.get("edge_has_incremental_nonidentical_overlap") is bool(increment), "incremental flag")
            need(row.get("edge_novel_beyond_known_228_baseline") is (bool(increment) and not bool(base)), "novel flag")
            need(row.get("unique_member_pair_count") > 0 and row.get("unique_member_pair_count") <= total, "member-pair witness count")
            need(row.get("provisional_only") is True and row.get("formal_credit") == 0, "source edge zero-credit authority")
            baseline_occurrences += base
            incremental_occurrences += increment
            baseline_edges += int(bool(base))
            incremental_edges += int(bool(increment))
            output.append(row)
    need(len(output) == 14_772, "edge row census")
    need(source_pairs == Counter({"C19B__C22A": 3668, "C19C__C22A": 28344, "C22A__C22A": 228}), "edge source totals")
    need((baseline_occurrences, incremental_occurrences, baseline_edges, incremental_edges) == (228, 32012, 192, 14620), "edge baseline/incremental totals")
    return output


def build(out: Path, edge_path: Path, seed: int) -> dict[str, Any]:
    need(type(seed) is int and seed > 0, "real positive seed")
    out.mkdir(parents=True, exist_ok=False)
    members = []
    sizes = Counter()
    member_ids = set()
    with pinned_input(C15, PINS["C15_members"], "C15 member ledger") as stream:
        for ordinal, row in enumerate(rows(stream, C15.name)):
            need(row.get("member_ordinal") == ordinal, "C15 contiguous member ordinal")
            member = row["registry_member_id"]
            need(member not in member_ids, "unique C15 member")
            member_ids.add(member)
            component = row["fresh_component_id"]
            sizes[component] += 1
            members.append({
                "ordinal": ordinal, "member_id": member, "old_component": component,
                "source_row_id": row["row_id"], "source_row_sha256": row["row_sha256"],
            })
    need(len(members) == 502_204 and len(sizes) == 57_876 and sum(sizes.values()) == 502_204, "C15 partition census")
    need(sum(count * (count - 1) // 2 for count in sizes.values()) == 487_702_036, "old within-pair census")

    edge_rows = load_edges(edge_path, set(sizes))
    application_order = list(edge_rows)
    random.Random(seed).shuffle(application_order)
    dsu = DSU(sizes)
    rank = sum(dsu.union(*row["component_pair"]) for row in application_order)
    need(rank == 14_104, "DSU rank reduction")
    groups = dsu.groups()
    need(len(groups) == 43_772, "provisional component count")
    home = {old: group for group in groups for old in group}
    new_id = {old: provisional_id(home[old]) for old in sizes}
    affected = [group for group in groups if len(group) > 1]
    need(len(affected) == 305 and sum(map(len, affected)) == 14_409, "affected cluster/vertex census")

    edge_by_pair = {tuple(row["component_pair"]): row for row in edge_rows}
    incident: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for pair in edge_by_pair:
        pid = new_id[pair[0]]
        need(pid == new_id[pair[1]], "every source edge internalized")
        incident[pid].append(pair)

    promotion_bodies = []
    for pair in sorted(edge_by_pair):
        source = edge_by_pair[pair]
        promotion_bodies.append({
            "schema": "cm2.round306c27r1d.strict-volume-provisional-edge-application-row.v1",
            "edge_application_id": edge_application_id(pair),
            "ordered_round306c15_component_pair": list(pair),
            "source_component_edge_id": source["component_edge_id"],
            "source_component_edge_row_sha256": source["row_sha256"],
            "witness_occurrence_count": source["witness_occurrence_count"],
            "unique_member_pair_count": source["unique_member_pair_count"],
            "source_pair_census": source["source_pair_census"],
            "baseline_occurrence_count": source["baseline_occurrence_count"],
            "incremental_occurrence_count": source["incremental_occurrence_count"],
            "sealed_edge_authority": "SAME_CHART_STRICT_POSITIVE_VOLUME_INTERIOR_INTERSECTION",
            "both_endpoints_bound_to_C15": True,
            "application_status": "CERTAIN_EDGE_INTERNALIZED_IN_PROVISIONAL_PARTITION",
            "overlay_qualification": "STRICT_VOLUME_ONLY__PROVISIONAL_UPPER_BOUND",
            "formal_credit": 0,
        })
    promotion_meta = write_gzip(out / PROMOTIONS, (closed(body) for body in promotion_bodies))

    cluster_bodies = []
    for group in sorted(affected, key=provisional_id):
        pid = provisional_id(group)
        pairs = sorted(incident[pid])
        cluster_bodies.append({
            "schema": "cm2.round306c27r1d.strict-volume-provisional-affected-cluster-row.v1",
            "provisional_component_id": pid,
            "identity_preimage": identity(group),
            "old_C15_component_count": len(group),
            "old_C15_component_ids_sha256": digest(group),
            "strict_volume_edge_count": len(pairs),
            "strict_volume_edge_application_ids_sha256": digest([edge_application_id(pair) for pair in pairs]),
            "member_count": sum(sizes[old] for old in group),
            "overlay_qualification": "STRICT_VOLUME_ONLY__PROVISIONAL_UPPER_BOUND",
            "formal_credit": 0,
        })
    cluster_meta = write_gzip(out / CLUSTERS, (closed(body) for body in cluster_bodies))

    component_bodies = []
    for ordinal, group in enumerate(groups):
        component_bodies.append({
            "schema": "cm2.round306c27r1d.strict-volume-provisional-component-census-row.v1",
            "component_ordinal": ordinal,
            "provisional_component_id": provisional_id(group),
            "identity_preimage": identity(group),
            "old_C15_component_count": len(group),
            "old_C15_component_ids_sha256": digest(group),
            "member_count": sum(sizes[old] for old in group),
            "affected_by_strict_volume_edge": len(group) > 1,
            "overlay_qualification": "STRICT_VOLUME_ONLY__PROVISIONAL_UPPER_BOUND",
            "formal_credit": 0,
        })
    component_meta = write_gzip(out / COMPONENTS, (closed(body) for body in component_bodies))

    def assignment_values() -> Iterator[bytes]:
        for row in members:
            body = {
                "schema": "cm2.round306c27r1d.strict-volume-provisional-member-assignment-row.v1",
                "member_ordinal": row["ordinal"],
                "registry_member_id": row["member_id"],
                "round306c15_component_id": row["old_component"],
                "provisional_component_id": new_id[row["old_component"]],
                "round306c15_source_row_id": row["source_row_id"],
                "round306c15_source_row_sha256": row["source_row_sha256"],
                "unique_assignment": True,
                "overlay_qualification": "STRICT_VOLUME_ONLY__PROVISIONAL_UPPER_BOUND",
                "formal_credit": 0,
            }
            yield closed(body)
    assignment_meta = write_gzip(out / ASSIGNMENTS, assignment_values())

    old_within = sum(count * (count - 1) // 2 for count in sizes.values())
    new_sizes = [sum(sizes[old] for old in group) for group in groups]
    new_within = sum(count * (count - 1) // 2 for count in new_sizes)
    total_pairs = 502_204 * 502_203 // 2
    newly_internalized = new_within - old_within
    cross_denominator = total_pairs - new_within
    need((newly_internalized, cross_denominator) == (24_956_788, 125_591_518_882), "pair arithmetic")

    result = {
        "schema": "cm2.round306c27r1d.strict-volume-provisional-overlay-result.v1",
        "status": "PASS_APPEND_ONLY_STRICT_VOLUME_PROVISIONAL_UPPER_BOUND__ZERO_FORMAL_CREDIT",
        "authority": "STRICT_VOLUME_EDGES_ONLY__NOT_A_FORMAL_C27R1_C28R1_OR_C29R1_SUCCESSOR",
        "formal_credit": 0,
        "input_sha256": {"strict_volume_component_edges": PINS["strict_volume_edges"][1], "C15_member_assignments": PINS["C15_members"][1]},
        "edge_census": {"strict_volume_component_edges": 14_772, "all_endpoints_bound_to_C15": True, "all_edges_internalized": True},
        "partition_census": {
            "members": 502_204, "old_C15_components": 57_876, "provisional_components": 43_772,
            "affected_old_component_vertices": 14_409, "affected_connected_clusters": 305,
            "forced_rank_reduction": 14_104, "newly_internalized_unordered_member_pairs": 24_956_788,
            "provisional_cross_component_pair_denominator": 125_591_518_882,
        },
        "qualification": {
            "component_count": "UPPER_BOUND_ONLY__MORE_UNCOVERED_TRANSITIONS_CAN_ONLY_LOWER_IT",
            "rank_reduction": "LOWER_BOUND_ONLY__MORE_LEGAL_EDGES_CAN_ONLY_RAISE_IT",
            "open_obligations": [
                "SAME_CHART_DIM1_DIM2_CLOSURE_CONTACT_TOTALITY", "C19C_ENDPOINT_OWNERSHIP",
                "C26_TRANSITION_HANDLE_ROUTING", "OTHER_OPEN_SUPPORT_TERMINALS",
                "TWENTY_FAMILY_PHYSICAL_TOTALITY_AND_UNIQUE_ASSIGNMENT", "C28R1_MAXIMALITY", "C29R1_GLOBAL_DISPOSITIONS",
            ],
            "C27": "UNAUTHORIZED", "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        },
        "forbidden_inputs_or_mutations": {
            "old_C27_C28_C29_read_or_reused": False, "old_C27R1BC_overlay_read_or_modified": False,
            "formal_seal_published": False, "C30c_touched": False,
        },
        "outputs": {
            "edge_application_ledger": promotion_meta, "affected_cluster_ledger": cluster_meta,
            "component_census_ledger": component_meta, "member_assignment_ledger": assignment_meta,
        },
    }
    result["result_object_sha256"] = digest(result)
    result_meta = write_json(out / RESULT, result)
    return {"execution_seed": seed, "result": result_meta, "outputs": result["outputs"], "result_object_sha256": result["result_object_sha256"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--edges", type=Path, default=EDGE_DEFAULT)
    args = parser.parse_args()
    value = build(args.out.resolve(), args.edges.resolve(), args.seed)
    print(canonical({"status": "PASS", **value}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "error": str(error)}, sort_keys=True), file=os.sys.stderr)
        raise SystemExit(2)
