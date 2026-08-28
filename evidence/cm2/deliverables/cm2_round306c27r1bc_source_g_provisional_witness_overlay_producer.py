#!/usr/bin/env python3
"""Build the append-only C27R1-B/C witness-only provisional overlay.

This program does not read or modify Round306C27/C28/C29.  It consumes only
the independently reconstructed seed-bearing witness ledger and the frozen
C15 member/component authorities.  The result is deliberately an upper-bound
partition with zero formal credit; it is not a maximality certificate.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import random
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
WITNESS_DEFAULT = ROOT.parent / ".cm2-runtime/audit/c27-same-chart-exact-equal-sqlite-seed-30629101/cm2_c27_same_chart_exact_equal_cross_component_witness_groups.jsonl.gz"
INPUTS = {
    "witness": (161323, "70e588cf83942c243cdac0c634ad348bc78ce7090ae01e2e36cd6d6b84717644"),
    "member": (142025813, "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    "census": (7599313, "eedeae91c8986440b41e5e5e1a1e65bf74e9c37add2d858b1d6b9b55e99a142c"),
}
PREFIX = "cm2_round306c27r1bc_source_g_provisional_witness_overlay"
PROMOTIONS = PREFIX + "_192_edge_promotion_ledger.jsonl.gz"
ASSIGNMENTS = PREFIX + "_502204_member_assignment_ledger.jsonl.gz"
COMPONENTS = PREFIX + "_57684_component_census_ledger.jsonl.gz"
CLUSTERS = PREFIX + "_120_affected_cluster_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
NEW_NS = "round306c27r1-provisional-source-g-component:"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def check_file(path: Path, expected: tuple[int, str], label: str) -> None:
    info = path.stat()
    need(path.is_file() and not path.is_symlink() and info.st_nlink == 1, "regular pinned input:" + label)
    need(info.st_size == expected[0] and file_hash(path) == expected[1], "size/hash pin:" + label)


def closed_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"canonical:{path.name}:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", body.pop("group_row_sha256", None))
            need(type(claimed) is str and claimed == digest(body), f"row closure:{path.name}:{ordinal}")
            yield row


def rational_volume(bounds: list[dict[str, Any]]) -> Fraction:
    need(type(bounds) is list and len(bounds) == 6, "six bounds")
    values: list[Fraction] = []
    for endpoint in bounds:
        need(type(endpoint) is dict and endpoint.get("kind") == "Q" and type(endpoint.get("value")) is str, "rational endpoint")
        values.append(Fraction(endpoint["value"]))
    widths = [values[1] - values[0], values[3] - values[2], values[5] - values[4]]
    need(all(width > 0 for width in widths), "strict positive widths")
    return widths[0] * widths[1] * widths[2]


def qwire(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def component_identity(old_ids: list[str]) -> dict[str, Any]:
    return {
        "schema": "cm2.round306c27r1.provisional-component-identity.v1",
        "ordered_round306c15_component_ids": old_ids,
        "qualification": "WITNESS_ONLY_PROVISIONAL_EQUIVALENCE_CLASS",
    }


def provisional_id(old_ids: list[str]) -> str:
    return NEW_NS + digest(component_identity(old_ids))


def closed(body: dict[str, Any]) -> bytes:
    return canonical({**body, "row_sha256": digest(body)}) + b"\n"


class DSU:
    def __init__(self, items: list[str]):
        self.items = sorted(items)
        self.index = {item: ordinal for ordinal, item in enumerate(self.items)}
        self.parent = list(range(len(self.items)))
        self.weight = [1] * len(self.items)

    def find(self, ordinal: int) -> int:
        while self.parent[ordinal] != ordinal:
            self.parent[ordinal] = self.parent[self.parent[ordinal]]
            ordinal = self.parent[ordinal]
        return ordinal

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
        out: dict[int, list[str]] = defaultdict(list)
        for ordinal, item in enumerate(self.items):
            out[self.find(ordinal)].append(item)
        return sorted((sorted(group) for group in out.values()), key=lambda group: provisional_id(group))


def write_gzip_exclusive(path: Path, rows: Iterator[bytes]) -> dict[str, Any]:
    need(not path.exists(), "no clobber:" + path.name)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=False) as raw:
            with gzip.GzipFile(filename="", fileobj=raw, mode="wb", compresslevel=9, mtime=0) as stream:
                for row in rows:
                    stream.write(row)
            raw.flush()
            os.fsync(raw.fileno())
    finally:
        os.close(fd)
    return {"filename": path.name, "size": path.stat().st_size, "sha256": file_hash(path)}


def write_json_exclusive(path: Path, value: dict[str, Any]) -> dict[str, Any]:
    payload = canonical(value) + b"\n"
    need(not path.exists(), "no clobber:" + path.name)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    return {"filename": path.name, "size": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def load_authorities(witness_path: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, int]]:
    member_path = ROOT / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
    census_path = ROOT / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_component_census_ledger.jsonl.gz"
    check_file(witness_path, INPUTS["witness"], "witness")
    check_file(member_path, INPUTS["member"], "C15 member")
    check_file(census_path, INPUTS["census"], "C15 census")

    members: dict[str, dict[str, Any]] = {}
    for row in closed_rows(member_path):
        member = row["registry_member_id"]
        need(member not in members, "unique C15 member")
        members[member] = row
    need(len(members) == 502_204, "C15 member census")

    sizes: dict[str, int] = {}
    for row in closed_rows(census_path):
        component = row["fresh_component_id"]
        need(component not in sizes and row["member_count"] > 0, "unique positive C15 component")
        sizes[component] = row["member_count"]
    need(len(sizes) == 57_876 and sum(sizes.values()) == 502_204, "C15 component census")
    need(set(row["fresh_component_id"] for row in members.values()) == set(sizes), "member/component exhaustion")

    witnesses: list[dict[str, Any]] = []
    group_ids: set[str] = set()
    for row in closed_rows(witness_path):
        need(row.get("schema") == "cm2.c27.same-chart-exact-equal-cross-component-witness-group.v1", "witness schema")
        need(row.get("legal_cross_component_physical_witness") is True, "legal witness assertion")
        need(row.get("member_count") == 2 and row.get("component_count") == 2 and row.get("cross_component_member_pair_count") == 1, "binary cross-component group")
        need(row.get("witness_reason") == "DISTINCT_C15_COMPONENTS_SHARE_THE_SAME_NONEMPTY_OPEN_3D_INTERIOR_IN_ONE_CHART", "open rational box witness reason")
        need(type(row.get("group_id")) is str and row["group_id"] not in group_ids, "unique witness group")
        group_ids.add(row["group_id"])
        group_volume = rational_volume(row["physical_bounds"])
        proof = row.get("strict_positive_volume_proof")
        need(type(proof) is dict and proof.get("common_open_interior_nonempty") is True and proof.get("endpoint_inclusion_bits_irrelevant_to_open_interior_intersection") is True, "open-interior proof")
        need(proof.get("exact_positive_rational_volume") == qwire(group_volume), "exact volume")
        observed_components: list[str] = []
        for member in row["members"]:
            member_id = member["owner_member_id"]
            need(member_id in members, "witness member in C15")
            source = members[member_id]
            need(member["fresh_component_id"] == source["fresh_component_id"], "witness component binding")
            need(member["C15_member_row_sha256"] == source["row_sha256"], "witness C15 row binding")
            need(member["chart"] == row["chart"] and member["support_kind"] == "OPEN_RATIONAL_BOX" and member["physical_bounds"] == row["physical_bounds"], "identical physical support")
            need(member["source_kernel"] == "C22A" and member["source_row_sha256"] == member["atom_id"].rsplit(":", 1)[-1], "primitive atom binding")
            observed_components.append(member["fresh_component_id"])
        need(sorted(observed_components) == row["fresh_component_ids"] and len(set(observed_components)) == 2, "component pair binding")
        witnesses.append(row)
    need(len(witnesses) == 228, "witness group census")
    return witnesses, members, sizes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--witness", type=Path, default=WITNESS_DEFAULT)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)

    witnesses, members, sizes = load_authorities(args.witness)
    insertion = list(witnesses)
    random.Random(args.seed).shuffle(insertion)
    edge_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in insertion:
        edge_groups[tuple(row["fresh_component_ids"])].append(row)
    need(len(edge_groups) == 192, "unique component edge census")

    dsu = DSU(list(sizes))
    reduction = 0
    for edge in sorted(edge_groups, key=lambda pair: digest({"pair": pair, "seed_rank": insertion.index(edge_groups[pair][0])})):
        reduction += dsu.union(*edge)
    need(reduction == 192, "forced rank reduction")
    groups = dsu.groups()
    need(len(groups) == 57_684, "provisional component census")
    group_by_old = {old: group for group in groups for old in group}
    new_by_old = {old: provisional_id(group_by_old[old]) for old in sizes}

    affected = [group for group in groups if len(group) > 1]
    need(len(affected) == 120 and sum(len(group) for group in affected) == 312, "affected cluster census")
    incident: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for edge in edge_groups:
        incident[new_by_old[edge[0]]].append(edge)

    promotion_bodies: list[dict[str, Any]] = []
    for edge in sorted(edge_groups):
        rows = sorted(edge_groups[edge], key=lambda row: row["group_id"])
        body = {
            "schema": "cm2.round306c27r1-b.provisional-certain-edge-promotion-row.v1",
            "provisional_edge_id": "round306c27r1-provisional-certain-edge:" + digest({"ordered_C15_component_pair": list(edge)}),
            "ordered_C15_component_pair": list(edge),
            "witness_group_count": len(rows),
            "witness_group_ids": [row["group_id"] for row in rows],
            "witness_group_ids_sha256": digest([row["group_id"] for row in rows]),
            "strict_positive_rational_volumes": [row["strict_positive_volume_proof"]["exact_positive_rational_volume"] for row in rows],
            "all_witnesses_strict_positive_open_interior": True,
            "logical_edge_status": "CERTAIN_LEGAL_PHYSICAL_EDGE",
            "overlay_qualification": "PROVISIONAL_UPPER_BOUND_ONLY",
            "formal_credit": 0,
        }
        promotion_bodies.append(body)

    promotion_meta = write_gzip_exclusive(args.out / PROMOTIONS, iter(closed(body) for body in promotion_bodies))

    cluster_bodies: list[dict[str, Any]] = []
    for group in sorted(affected, key=provisional_id):
        pid = provisional_id(group)
        edges = sorted(incident[pid])
        body = {
            "schema": "cm2.round306c27r1-c.provisional-affected-cluster-row.v1",
            "provisional_component_id": pid,
            "identity_preimage": component_identity(group),
            "old_C15_component_count": len(group),
            "old_C15_component_ids_sha256": digest(group),
            "certain_edge_count": len(edges),
            "certain_edge_ids_sha256": digest(["round306c27r1-provisional-certain-edge:" + digest({"ordered_C15_component_pair": list(edge)}) for edge in edges]),
            "member_count": sum(sizes[old] for old in group),
            "overlay_qualification": "PROVISIONAL_UPPER_BOUND_ONLY",
            "formal_credit": 0,
        }
        cluster_bodies.append(body)
    cluster_meta = write_gzip_exclusive(args.out / CLUSTERS, iter(closed(body) for body in cluster_bodies))

    component_bodies: list[dict[str, Any]] = []
    for ordinal, group in enumerate(groups):
        pid = provisional_id(group)
        body = {
            "schema": "cm2.round306c27r1-c.provisional-component-census-row.v1",
            "component_ordinal": ordinal,
            "provisional_component_id": pid,
            "identity_preimage": component_identity(group),
            "old_C15_component_count": len(group),
            "old_C15_component_ids_sha256": digest(group),
            "member_count": sum(sizes[old] for old in group),
            "affected_by_same_chart_witness_promotion": len(group) > 1,
            "overlay_qualification": "PROVISIONAL_UPPER_BOUND_ONLY",
            "formal_credit": 0,
        }
        component_bodies.append(body)
    component_meta = write_gzip_exclusive(args.out / COMPONENTS, iter(closed(body) for body in component_bodies))

    def assignment_rows() -> Iterator[bytes]:
        for row in sorted(members.values(), key=lambda source: source["member_ordinal"]):
            body = {
                "schema": "cm2.round306c27r1-c.provisional-member-assignment-row.v1",
                "member_ordinal": row["member_ordinal"],
                "registry_member_id": row["registry_member_id"],
                "round306c15_component_id": row["fresh_component_id"],
                "provisional_component_id": new_by_old[row["fresh_component_id"]],
                "round306c15_source_row_id": row["row_id"],
                "round306c15_source_row_sha256": row["row_sha256"],
                "overlay_qualification": "PROVISIONAL_UPPER_BOUND_ONLY",
                "formal_credit": 0,
            }
            yield closed(body)
    assignment_meta = write_gzip_exclusive(args.out / ASSIGNMENTS, assignment_rows())

    old_within = sum(count * (count - 1) // 2 for count in sizes.values())
    new_sizes = [sum(sizes[old] for old in group) for group in groups]
    new_within = sum(count * (count - 1) // 2 for count in new_sizes)
    total_pairs = 502_204 * 502_203 // 2
    newly_internalized = new_within - old_within
    cross = total_pairs - new_within
    need(old_within == 487_702_036 and newly_internalized == 691_416 and cross == 125_615_784_254, "pair arithmetic")

    result = {
        "schema": "cm2.round306c27r1-bc.provisional-witness-overlay-result.v1",
        "status": "PASS_PROVISIONAL_UPPER_BOUND_ONLY__ZERO_FORMAL_CREDIT",
        "formal_credit": 0,
        "authority": "APPEND_ONLY_WITNESS_ONLY_OVERLAY__NOT_A_FORMAL_SUCCESSOR_SEAL",
        "old_C27_C28_C29": "REJECT__NOT_READ_NOT_MODIFIED_NOT_REUSED",
        "input_sha256": {key: value[1] for key, value in INPUTS.items()},
        "witness_census": {"groups": 228, "unique_component_edges": 192, "all_edges_strictly_witnessed": True},
        "partition_census": {
            "members": 502_204,
            "old_C15_components": 57_876,
            "provisional_components": 57_684,
            "affected_old_component_vertices": 312,
            "affected_connected_clusters": 120,
            "forced_rank_reduction": 192,
            "newly_internalized_member_pairs": 691_416,
            "provisional_cross_component_pair_denominator": 125_615_784_254,
        },
        "qualification": {
            "component_count": "UPPER_BOUND_ON_ANY_EVENTUAL_COMPONENT_COUNT",
            "rank_reduction": "LOWER_BOUND_ON_EVENTUAL_RANK_REDUCTION",
            "not_closed": [
                "SAME_CHART_RELATIVE_CELLS_TOTALITY",
                "SIGNED_BOUNDARY_FACES",
                "COMPLETE_BOUNDARY_FACES",
                "POSITIVE_VOLUME_CARRIERS",
                "TWENTY_FAMILY_PHYSICAL_TOTALITY_AND_UNIQUE_ASSIGNMENT",
                "C28R1_MAXIMALITY",
                "C29R1_GLOBAL_DISPOSITIONS",
            ],
            "C28": "REJECT",
            "C29": "REJECT",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "outputs": {
            "promotion_ledger": promotion_meta,
            "affected_cluster_ledger": cluster_meta,
            "component_census_ledger": component_meta,
            "member_assignment_ledger": assignment_meta,
        },
    }
    result["result_object_sha256"] = digest(result)
    result_meta = write_json_exclusive(args.out / RESULT, result)
    print(json.dumps({"status": "PASS", "execution_seed": args.seed, "result": result_meta, "outputs": result["outputs"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "error": str(error)}, sort_keys=True), file=os.sys.stderr)
        raise SystemExit(2)
