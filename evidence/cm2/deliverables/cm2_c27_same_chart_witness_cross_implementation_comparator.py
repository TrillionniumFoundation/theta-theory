#!/usr/bin/env python3
"""Cross-implementation comparator for the SAME_CHART exact-box witnesses.

Implementation A is the independently materialized SAME_CHART census atom
ledger.  This program does not query or reuse implementation B's SQLite
database.  Instead it validates every canonical closure in A and in the C15
member authority, builds a bounded-memory Python external merge sort keyed by
``[chart, physical_bounds]``, and reconstructs all equal-box groups whose
members lie in distinct C15 components.  It then compares those groups with
both seed runs of implementation B at the exact group/projection level.

This is deliberately a zero-credit counterexample comparator.  It does not
establish totality for SAME_CHART_RELATIVE_CELLS or any 20-family gate.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import hashlib
import heapq
import json
import os
from pathlib import Path
import shutil
import stat
import sys
from typing import Any, BinaryIO, Iterator


LEDGER_NAME = "cm2_c27_same_chart_witness_cross_implementation_comparison_groups.jsonl.gz"
RESULT_NAME = "cm2_c27_same_chart_witness_cross_implementation_comparator_result.json"
EXPECTED_CENSUS_LEDGER_SHA256 = "6e3aacd47d1331634f5b9d5c89f21fae62695203deb81acd4009deca81b4d069"
EXPECTED_C15_LEDGER_SHA256 = "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"
EXPECTED_SEEDS = (30_629_101, 30_629_901)


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


@dataclass(frozen=True)
class FilePin:
    path: str
    sha256: str
    size: int
    device: int
    inode: int
    mtime_ns: int

    def as_json(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "sha256": self.sha256,
            "size": self.size,
            "device": self.device,
            "inode": self.inode,
            "mtime_ns": self.mtime_ns,
        }


def pin_file(path: Path) -> FilePin:
    path = path.resolve(strict=True)
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), f"regular input:{path}")
    observed = file_hash(path)
    after = path.lstat()
    need(
        (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
        f"stable input while hashing:{path}",
    )
    return FilePin(
        str(path), observed, after.st_size, after.st_dev, after.st_ino,
        after.st_mtime_ns,
    )


def repin_exact(pin: FilePin) -> None:
    path = Path(pin.path)
    observed = pin_file(path)
    need(observed == pin, f"input changed during comparison:{path}")


def closed_object(path: Path, field: str = "result_sha256") -> dict[str, Any]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and b"\n" not in raw[:-1], f"single canonical object:{path}")
    value = json.loads(raw[:-1])
    need(type(value) is dict and canonical(value) + b"\n" == raw, f"canonical object:{path}")
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body), f"object closure:{path}")
    return value


def closed_gzip_rows(path: Path, field: str) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"canonical:{path.name}:{ordinal}")
            body = dict(row)
            claimed = body.pop(field, None)
            need(type(claimed) is str and claimed == digest(body), f"closure:{path.name}:{ordinal}")
            yield row


def load_c15(path: Path) -> tuple[dict[str, tuple[str, str]], int]:
    output: dict[str, tuple[str, str]] = {}
    count = 0
    for ordinal, row in enumerate(closed_gzip_rows(path, "row_sha256")):
        need(row.get("member_ordinal") == ordinal, f"C15 member ordinal:{ordinal}")
        member = row.get("registry_member_id")
        component = row.get("fresh_component_id")
        need(type(member) is str and type(component) is str, f"C15 member/component types:{ordinal}")
        need(member not in output, f"C15 unique member:{member}")
        output[member] = (component, row["row_sha256"])
        count += 1
    need(count == len(output) == 502_204, "complete C15 502204-member authority")
    return output, count


def projection(member: dict[str, Any]) -> dict[str, str]:
    fields = (
        "owner_member_id",
        "fresh_component_id",
        "source_kernel",
        "source_row_sha256",
        "support_kind",
    )
    output: dict[str, str] = {}
    for field in fields:
        value = member.get(field)
        need(type(value) is str and value != "", f"projection field:{field}")
        output[field] = value
    return output


def projection_sort_key(value: dict[str, str]) -> bytes:
    return canonical(value)


def validate_second_group(row: dict[str, Any], ordinal: int) -> tuple[str, dict[str, Any]]:
    need(row.get("ordinal") == ordinal, f"implementation B ordinal:{ordinal}")
    chart = row.get("chart")
    bounds = row.get("physical_bounds")
    need(chart in {"G:E", "G:N", "G:W", "G:S"}, f"implementation B chart:{ordinal}")
    need(type(bounds) is list and len(bounds) == 6, f"implementation B six bounds:{ordinal}")
    derived_group = "same-chart-exact-equal-positive-volume:" + digest([chart, bounds])
    need(row.get("group_id") == derived_group, f"implementation B derived group id:{ordinal}")
    members = row.get("members")
    need(type(members) is list and len(members) == row.get("member_count") == 2, f"implementation B two members:{ordinal}")
    values: list[dict[str, str]] = []
    for member_ordinal, member in enumerate(members):
        need(type(member) is dict, f"implementation B member object:{ordinal}:{member_ordinal}")
        body = dict(member)
        claimed = body.pop("member_row_sha256", None)
        need(type(claimed) is str and claimed == digest(body), f"implementation B member closure:{ordinal}:{member_ordinal}")
        need(
            member.get("chart") == chart
            and member.get("physical_bounds") == bounds,
            f"implementation B group geometry binding:{ordinal}:{member_ordinal}",
        )
        values.append(projection(member))
    values.sort(key=projection_sort_key)
    components = {value["fresh_component_id"] for value in values}
    need(
        len(components) == row.get("component_count") == 2
        and row.get("cross_component_member_pair_count") == 1
        and row.get("legal_cross_component_physical_witness") is True
        and row.get("formal_credit") == 0,
        f"implementation B cross-component witness semantics:{ordinal}",
    )
    need(
        all(value["source_kernel"] == "C22A" and value["support_kind"] == "OPEN_RATIONAL_BOX" for value in values),
        f"implementation B observed C22A open-box structure:{ordinal}",
    )
    proof = row.get("strict_positive_volume_proof")
    need(
        type(proof) is dict
        and proof.get("common_open_interior_nonempty") is True
        and proof.get("endpoint_inclusion_bits_irrelevant_to_open_interior_intersection") is True,
        f"implementation B positive open interior:{ordinal}",
    )
    return derived_group, {
        "chart": chart,
        "physical_bounds": bounds,
        "projections": values,
    }


def load_second_ledger(path: Path) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    group_rows = hashlib.sha256()
    flattened = hashlib.sha256()
    count = 0
    for ordinal, row in enumerate(closed_gzip_rows(path, "group_row_sha256")):
        group_id, value = validate_second_group(row, ordinal)
        need(group_id not in groups, f"implementation B unique group:{group_id}")
        groups[group_id] = value
        group_rows.update(bytes.fromhex(row["group_row_sha256"]))
        for member in row["members"]:
            flattened.update(bytes.fromhex(member["member_row_sha256"]))
        count += 1
    need(count == len(groups) == 228, "implementation B 228 groups")
    ids = sorted(groups, key=lambda value: value.encode("ascii"))
    return groups, {
        "row_count": count,
        "group_ids_sha256": digest(ids),
        "group_row_sequence_sha256": group_rows.hexdigest(),
        "flattened_member_row_sequence_sha256": flattened.hexdigest(),
    }


def validate_second_result(
    result: dict[str, Any],
    result_path: Path,
    ledger_path: Path,
    seed: int,
    ledger_stats: dict[str, Any],
) -> None:
    need(result.get("declared_seed") == seed, f"implementation B declared seed:{seed}")
    need(result.get("declared_seed_used_for_pre_sort_sqlite_insertion_order") is True, f"implementation B seed used:{seed}")
    need(result.get("formal_credit") == 0, f"implementation B zero credit:{seed}")
    need(result.get("legal_cross_component_witness_found") is True, f"implementation B witness:{seed}")
    need(result.get("C27_C28_C29") == "REJECT_AND_REBUILD_REQUIRED", f"implementation B governance:{seed}")
    need(result.get("CM2") == "NO-GO_FOR_CLAIM", f"implementation B CM2 status:{seed}")
    census = result.get("witness_census")
    need(
        type(census) is dict
        and census.get("witness_group_count") == 228
        and census.get("witness_member_count") == 456
        and census.get("witness_component_occurrence_count") == 456
        and census.get("cross_component_member_pair_count") == 228,
        f"implementation B 228/456 census:{seed}",
    )
    ledger = result.get("ledger")
    need(type(ledger) is dict, f"implementation B ledger object:{seed}")
    need(
        ledger.get("row_count") == 228
        and ledger.get("sha256") == file_hash(ledger_path)
        and ledger.get("size") == ledger_path.stat().st_size
        and ledger.get("group_row_sequence_sha256") == ledger_stats["group_row_sequence_sha256"]
        and ledger.get("flattened_member_row_sequence_sha256") == ledger_stats["flattened_member_row_sequence_sha256"],
        f"implementation B ledger commitments:{seed}",
    )
    need(result.get("group_ids_sha256") == ledger_stats["group_ids_sha256"], f"implementation B group id commitment:{seed}")
    invocation = result.get("invocation")
    need(
        type(invocation) is dict
        and invocation.get("isolated_runtime") is True
        and invocation.get("dont_write_bytecode") is True
        and type(invocation.get("command_argv")) is list
        and str(seed) in invocation["command_argv"],
        f"implementation B seed-bearing invocation:{seed}",
    )
    need(result_path.read_bytes().endswith(b"\n"), f"implementation B result newline:{seed}")


def semantic_projection_for_seed_result(result: dict[str, Any]) -> dict[str, Any]:
    drop = {
        "declared_seed",
        "invocation",
        "result_sha256",
    }
    return {key: value for key, value in result.items() if key not in drop}


def flush_chunk(chunk_dir: Path, ordinal: int, rows: list[bytes]) -> Path:
    rows.sort()
    path = chunk_dir / f"chunk-{ordinal:04d}.jsonl"
    with path.open("xb") as stream:
        for row in rows:
            stream.write(row)
    return path


def materialize_sorted_chunks(
    census_path: Path,
    c15: dict[str, tuple[str, str]],
    chunk_dir: Path,
    chunk_size: int,
) -> tuple[list[Path], dict[str, Any]]:
    need(chunk_size >= 1_000, "chunk size at least 1000")
    chunk_dir.mkdir(parents=False, exist_ok=False)
    chunk: list[bytes] = []
    paths: list[Path] = []
    source_census: dict[str, int] = {}
    owner_set: set[str] = set()
    atom_ids: set[str] = set()
    count = 0
    for ordinal, row in enumerate(closed_gzip_rows(census_path, "row_sha256")):
        need(row.get("ordinal") == ordinal, f"implementation A atom ordinal:{ordinal}")
        owner = row.get("owner_member_id")
        need(type(owner) is str and owner in c15, f"implementation A C15 owner join:{ordinal}")
        component, _c15_row_sha = c15[owner]
        atom_id = row.get("atom_id")
        need(type(atom_id) is str and atom_id not in atom_ids, f"implementation A unique atom:{ordinal}")
        atom_ids.add(atom_id)
        chart = row.get("chart")
        bounds = row.get("physical_bounds")
        source = row.get("source_kernel")
        source_sha = row.get("source_row_sha256")
        support_kind = row.get("support_kind")
        need(chart in {"G:E", "G:N", "G:W", "G:S"}, f"implementation A chart:{ordinal}")
        need(type(bounds) is list and len(bounds) == 6, f"implementation A six bounds:{ordinal}")
        need(type(source) is str and type(source_sha) is str and type(support_kind) is str, f"implementation A projection types:{ordinal}")
        group_id = "same-chart-exact-equal-positive-volume:" + digest([chart, bounds])
        record = [
            group_id,
            chart,
            bounds,
            owner,
            component,
            source,
            source_sha,
            support_kind,
        ]
        chunk.append(canonical(record) + b"\n")
        source_census[source] = source_census.get(source, 0) + 1
        owner_set.add(owner)
        count += 1
        if len(chunk) >= chunk_size:
            paths.append(flush_chunk(chunk_dir, len(paths), chunk))
            chunk = []
    if chunk:
        paths.append(flush_chunk(chunk_dir, len(paths), chunk))
    need(count == 483_232, "implementation A complete 483232 atoms")
    need(len(owner_set) == 482_380, "implementation A distinct 482380 owners")
    need(len(atom_ids) == count, "implementation A unique atom ids")
    need(source_census == {
        "C19A": 5_596,
        "C19B": 12_232,
        "C19C": 33_344,
        "C20A": 126_468,
        "C22A": 295_340,
        "C23A": 10_252,
    }, "implementation A primitive source census")
    return paths, {
        "atom_count": count,
        "distinct_owner_count": len(owner_set),
        "source_census": source_census,
        "chunk_count": len(paths),
        "chunk_size": chunk_size,
    }


def merge_chunk_records(paths: list[Path]) -> Iterator[list[Any]]:
    streams: list[BinaryIO] = [path.open("rb") for path in paths]
    try:
        for line in heapq.merge(*streams):
            need(line.endswith(b"\n"), "temporary chunk newline")
            value = json.loads(line[:-1])
            need(type(value) is list and len(value) == 8 and canonical(value) + b"\n" == line, "canonical temporary record")
            yield value
    finally:
        for stream in streams:
            stream.close()


def dsu_summary(edges: list[list[str]]) -> dict[str, Any]:
    vertices = sorted({vertex for edge in edges for vertex in edge}, key=lambda value: value.encode("ascii"))
    parent = {vertex: vertex for vertex in vertices}

    def find(value: str) -> str:
        root = value
        while parent[root] != root:
            root = parent[root]
        while parent[value] != value:
            next_value = parent[value]
            parent[value] = root
            value = next_value
        return root

    rank = 0
    for left, right in edges:
        root_left, root_right = find(left), find(right)
        if root_left != root_right:
            if root_right.encode("ascii") < root_left.encode("ascii"):
                root_left, root_right = root_right, root_left
            parent[root_right] = root_left
            rank += 1
    connected_components = len({find(vertex) for vertex in vertices})
    return {
        "unique_component_edge_count": len(edges),
        "affected_component_vertex_count": len(vertices),
        "DSU_rank_reduction": rank,
        "connected_component_count_on_affected_vertices": connected_components,
        "unique_component_edges_sha256": digest(edges),
        "affected_component_vertices_sha256": digest(vertices),
    }


def close_comparison_row(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "comparison_row_sha256": digest(body)}


def validate_comparison_groups(groups: list[dict[str, Any]], expected: dict[str, Any]) -> dict[str, Any]:
    need(type(groups) is list, "comparison groups list")
    group_ids: list[str] = []
    flattened: list[dict[str, str]] = []
    edges_set: set[tuple[str, str]] = set()
    row_hashes: list[str] = []
    for ordinal, row in enumerate(groups):
        need(type(row) is dict, f"comparison row object:{ordinal}")
        body = dict(row)
        claimed = body.pop("comparison_row_sha256", None)
        need(type(claimed) is str and claimed == digest(body), f"comparison row closure:{ordinal}")
        need(row.get("ordinal") == ordinal, f"comparison ordinal:{ordinal}")
        chart, bounds = row.get("chart"), row.get("physical_bounds")
        derived = "same-chart-exact-equal-positive-volume:" + digest([chart, bounds])
        need(row.get("group_id") == derived, f"comparison derived group id:{ordinal}")
        values = row.get("projections")
        need(type(values) is list and len(values) == row.get("projection_count") == 2, f"comparison two projections:{ordinal}")
        need(values == sorted(values, key=projection_sort_key), f"comparison sorted projections:{ordinal}")
        for value in values:
            need(type(value) is dict and projection(value) == value, f"comparison projection shape:{ordinal}")
            need(value["source_kernel"] == "C22A" and value["support_kind"] == "OPEN_RATIONAL_BOX", f"comparison observed witness structure:{ordinal}")
        need(len({value["owner_member_id"] for value in values}) == 2, f"comparison distinct owners:{ordinal}")
        components = sorted({value["fresh_component_id"] for value in values}, key=lambda value: value.encode("ascii"))
        need(len(components) == 2 and row.get("component_edge") == components, f"comparison component edge:{ordinal}")
        need(
            row.get("implementation_A_equals_implementation_B_seed_A") is True
            and row.get("formal_credit") == 0,
            f"comparison equality/credit:{ordinal}",
        )
        group_ids.append(derived)
        flattened.extend(values)
        edges_set.add((components[0], components[1]))
        row_hashes.append(claimed)
    need(len(group_ids) == len(set(group_ids)), "unique comparison group ids")
    edges = [list(edge) for edge in sorted(edges_set, key=lambda edge: canonical(edge))]
    dsu = dsu_summary(edges)
    summary = {
        "witness_group_count": len(groups),
        "witness_projection_count": len(flattened),
        "group_ids_sha256": digest(group_ids),
        "flattened_projection_sha256": digest(flattened),
        "comparison_row_hashes_sha256": digest(row_hashes),
        **dsu,
    }
    for field, expected_value in expected.items():
        need(summary.get(field) == expected_value, f"comparison commitment:{field}")
    return summary


def reconstruct_and_compare(
    chunk_paths: list[Path],
    second_groups: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    output: list[dict[str, Any]] = []
    duplicate_group_count = 0
    current_group: str | None = None
    current_records: list[list[Any]] = []
    seen_second: set[str] = set()

    def consume(group_id: str, records: list[list[Any]]) -> None:
        nonlocal duplicate_group_count
        if len(records) > 1:
            duplicate_group_count += 1
        chart = records[0][1]
        bounds = records[0][2]
        need(all(row[0] == group_id and row[1] == chart and row[2] == bounds for row in records), f"full key equality/no digest collision:{group_id}")
        values = [
            {
                "owner_member_id": row[3],
                "fresh_component_id": row[4],
                "source_kernel": row[5],
                "source_row_sha256": row[6],
                "support_kind": row[7],
            }
            for row in records
        ]
        components = sorted({value["fresh_component_id"] for value in values}, key=lambda value: value.encode("ascii"))
        if len(components) <= 1:
            return
        values.sort(key=projection_sort_key)
        need(len(values) == 2 and len(components) == 2, f"implementation A observed two-by-two witness:{group_id}")
        need(group_id in second_groups, f"implementation A group absent in implementation B:{group_id}")
        other = second_groups[group_id]
        need(other["chart"] == chart and other["physical_bounds"] == bounds, f"cross-implementation exact geometry:{group_id}")
        need(other["projections"] == values, f"cross-implementation exact five-field projections:{group_id}")
        body = {
            "schema": "cm2.c27.same-chart-witness-cross-implementation-comparison-group.v1",
            "ordinal": len(output),
            "group_id": group_id,
            "chart": chart,
            "physical_bounds": bounds,
            "projection_count": len(values),
            "projections": values,
            "component_edge": components,
            "implementation_A_equals_implementation_B_seed_A": True,
            "formal_credit": 0,
        }
        output.append(close_comparison_row(body))
        seen_second.add(group_id)

    for record in merge_chunk_records(chunk_paths):
        group_id = record[0]
        if current_group is None:
            current_group = group_id
        if group_id != current_group:
            consume(current_group, current_records)
            current_group = group_id
            current_records = []
        current_records.append(record)
    if current_group is not None:
        consume(current_group, current_records)
    need(len(output) == 228, "implementation A independently reconstructs 228 groups")
    need(seen_second == set(second_groups), "cross-implementation group id set exact identity")
    output.sort(key=lambda row: row["group_id"].encode("ascii"))
    for ordinal, row in enumerate(output):
        if row["ordinal"] != ordinal:
            body = dict(row)
            body.pop("comparison_row_sha256")
            body["ordinal"] = ordinal
            output[ordinal] = close_comparison_row(body)
    expected = {
        "witness_group_count": 228,
        "witness_projection_count": 456,
        "unique_component_edge_count": 192,
        "affected_component_vertex_count": 312,
        "DSU_rank_reduction": 192,
        "connected_component_count_on_affected_vertices": 120,
    }
    summary = validate_comparison_groups(output, expected)
    summary["duplicate_exact_box_group_count_in_implementation_A"] = duplicate_group_count
    need(duplicate_group_count == 134_968, "implementation A 134968 exact-box duplicate groups")
    return output, summary


def write_comparison_ledger(path: Path, groups: list[dict[str, Any]]) -> dict[str, Any]:
    sequence = hashlib.sha256()
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as packed:
            for row in groups:
                packed.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["comparison_row_sha256"]))
    return {
        "filename": path.name,
        "row_count": len(groups),
        "sha256": file_hash(path),
        "size": path.stat().st_size,
        "comparison_row_sequence_sha256": sequence.hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census-result", required=True)
    parser.add_argument("--census-ledger", required=True)
    parser.add_argument("--c15-ledger", required=True)
    parser.add_argument("--seed-a-result", required=True)
    parser.add_argument("--seed-a-ledger", required=True)
    parser.add_argument("--seed-b-result", required=True)
    parser.add_argument("--seed-b-ledger", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--chunk-size", type=int, default=40_000)
    args = parser.parse_args()
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated -I -B runtime")

    paths = {
        key: Path(value).resolve(strict=True)
        for key, value in {
            "census_result": args.census_result,
            "census_ledger": args.census_ledger,
            "C15_ledger": args.c15_ledger,
            "seed_A_result": args.seed_a_result,
            "seed_A_ledger": args.seed_a_ledger,
            "seed_B_result": args.seed_b_result,
            "seed_B_ledger": args.seed_b_ledger,
        }.items()
    }
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    input_pins = {key: pin_file(path) for key, path in paths.items()}
    need(input_pins["census_ledger"].sha256 == EXPECTED_CENSUS_LEDGER_SHA256, "pinned implementation A census ledger")
    need(input_pins["C15_ledger"].sha256 == EXPECTED_C15_LEDGER_SHA256, "pinned C15 authority")
    need(
        paths["seed_A_ledger"].read_bytes() == paths["seed_B_ledger"].read_bytes(),
        "implementation B double-seed ledger byte identity",
    )

    census_result = closed_object(paths["census_result"])
    need(census_result.get("formal_credit") == 0 and census_result.get("C27_C28_C29") == "REJECT", "truthful implementation A result")
    need(census_result.get("ledger", {}).get("sha256") == EXPECTED_CENSUS_LEDGER_SHA256, "implementation A result binds ledger")
    need(census_result.get("fresh_candidate_universe", {}).get("atom_count") == 483_232, "implementation A result atom count")

    seed_a_result = closed_object(paths["seed_A_result"])
    seed_b_result = closed_object(paths["seed_B_result"])
    need(paths["seed_A_result"].read_bytes() != paths["seed_B_result"].read_bytes(), "implementation B seed-bearing result files distinct")
    second_groups, second_stats = load_second_ledger(paths["seed_A_ledger"])
    validate_second_result(seed_a_result, paths["seed_A_result"], paths["seed_A_ledger"], EXPECTED_SEEDS[0], second_stats)
    validate_second_result(seed_b_result, paths["seed_B_result"], paths["seed_B_ledger"], EXPECTED_SEEDS[1], second_stats)
    need(
        seed_a_result.get("semantic_projection_sha256") == seed_b_result.get("semantic_projection_sha256")
        and semantic_projection_for_seed_result(seed_a_result) == semantic_projection_for_seed_result(seed_b_result),
        "implementation B cross-seed exact semantic equality",
    )

    c15, c15_count = load_c15(paths["C15_ledger"])
    chunk_dir = output_dir / "external-sort-chunks"
    chunk_paths, first_census = materialize_sorted_chunks(
        paths["census_ledger"], c15, chunk_dir, args.chunk_size,
    )
    groups, comparison = reconstruct_and_compare(chunk_paths, second_groups)
    for chunk_path in chunk_paths:
        chunk_path.unlink()
    chunk_dir.rmdir()

    ledger = write_comparison_ledger(output_dir / LEDGER_NAME, groups)
    expected = {
        key: comparison[key]
        for key in (
            "witness_group_count",
            "witness_projection_count",
            "group_ids_sha256",
            "flattened_projection_sha256",
            "comparison_row_hashes_sha256",
            "unique_component_edge_count",
            "affected_component_vertex_count",
            "DSU_rank_reduction",
            "connected_component_count_on_affected_vertices",
            "unique_component_edges_sha256",
            "affected_component_vertices_sha256",
        )
    }
    validate_comparison_groups(groups, expected)
    need(second_stats["group_ids_sha256"] == comparison["group_ids_sha256"], "cross-implementation group id commitment equality")

    for pin in input_pins.values():
        repin_exact(pin)

    body = {
        "schema": "cm2.c27.same-chart-witness-cross-implementation-comparator.v1",
        "status": "PASS_ZERO_CREDIT__PYTHON_EXTERNAL_SORT_AND_SQLITE_IMPLEMENTATIONS_EXACTLY_MATCH_228_GROUPS_456_PROJECTIONS__C27_C28_C29_REBUILD_REQUIRED",
        "implementation_A": "CANONICAL_CENSUS_ATOM_LEDGER_PLUS_C15_JOIN_AND_PYTHON_BOUNDED_MEMORY_EXTERNAL_MERGE_SORT",
        "implementation_B": "INDEPENDENT_DIRECT_PRIMITIVE_SQLITE_EXTERNAL_GROUPING__TWO_DISTINCT_INSERTION_SEEDS",
        "forbidden_reuse": {
            "implementation_B_scratch_SQLite_opened_or_queried_by_comparator": False,
            "C27_FAMILIES_or_old_edge_ledger_used": False,
        },
        "canonical_row_closures_validated": {
            "implementation_A_atom_rows": 483_232,
            "C15_member_rows": c15_count,
            "implementation_B_seed_A_group_rows": 228,
            "implementation_B_seed_A_member_rows": 456,
            "implementation_B_seed_B_ledger_byte_identical_to_A": True,
        },
        "implementation_A_census": first_census,
        "implementation_B_cross_seed": {
            "seeds": list(EXPECTED_SEEDS),
            "seed_bearing_result_files_distinct": True,
            "semantic_projection_exact_identical": True,
            "ledger_byte_identical": True,
            "group_ids_sha256": second_stats["group_ids_sha256"],
        },
        "cross_implementation_exact_comparison": comparison,
        "comparison_ledger": ledger,
        "input_pins": {key: pin.as_json() for key, pin in input_pins.items()},
        "legal_cross_component_witness_found": True,
        "required_governance_action": "REBUILD_C27_THROUGH_C29__PATCHING_OR_PRESERVING_C29_UNCONDITIONAL_AUTHORITY_IS_FORBIDDEN",
        "limitations": {
            "same_chart_relative_cells_totality_proved": False,
            "twenty_family_totality_proved": False,
            "half_open_endpoint_ownership_gap_resolved": False,
            "C26_absence_negative_theorem_proved": False,
            "scope": "EXACT_EQUAL_POSITIVE_VOLUME_SAME_CHART_GROUP_CROSS_IMPLEMENTATION_COMPARISON_ONLY",
        },
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
        "invocation": {
            "command_argv": list(sys.argv),
            "isolated_runtime": True,
            "dont_write_bytecode": True,
            "python_external_sort_chunk_size": args.chunk_size,
        },
    }
    result = {**body, "result_sha256": digest(body)}
    (output_dir / RESULT_NAME).write_bytes(canonical(result) + b"\n")
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        Failure,
        KeyError,
        OSError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        print("REJECT_SAME_CHART_CROSS_IMPLEMENTATION_COMPARATOR:" + str(error), file=sys.stderr)
        raise SystemExit(2)
