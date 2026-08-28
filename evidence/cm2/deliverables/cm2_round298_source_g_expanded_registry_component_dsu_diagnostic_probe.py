#!/usr/bin/env python3
"""Read-only diagnostic probe for the prospective Round298 DSU.

This is not a promotion producer and writes no deliverable artifact.  It
compares two explicitly nonsealed hypotheses for the Round291 two-target
physical-incidence channel:

* A: all distinct two-target occurrence pairs;
* B: only pairs whose endpoints have the same official key.

The probe byte-pins its five large source files, streams and recommits every
input row, runs all six channel orders plus a within-channel reverse replay,
audits final key purity over all 564,492 members, and verifies that replacing
each accepted physical-incidence row by an explicit witness node does not
change the component partition on the formal member universe.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import itertools
import json
import mmap
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent

R266 = (
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
)
R294 = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R295A = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "physical_witness_incidence_binding_ledger.json.gz"
)
R296 = (
    "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_"
    "edge_ledger.json.gz"
)
R297 = (
    "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_"
    "edge_ledger.json.gz"
)

FILE_PINS = {
    R266: "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    R294: "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R295A: "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R296: "1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7",
    R297: "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
}

TABLES = {
    "R266_MEMBER": (
        259_752,
        "post_Round266_component_member_frontier_row_id",
        "28398acde446047ff4a210b2fa0831d2c44e3758f7e9239b5ec63cecc386b257",
    ),
    "R294_REGISTRY": (
        431_208,
        "Round294_occurrence_registry_row_id",
        "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
    ),
    "R295A_INCIDENCE": (
        113_452,
        "Round295A_R291_physical_incidence_binding_row_id",
        "e8b00ffa431d7609d97e7e3cae00f656d2386643acc22d49bdc4a018ed295946",
    ),
    "R296_SEAM": (
        48_444,
        "Round296_true_seam_occurrence_edge_row_id",
        "e989828d774a08694404fe678c4ae74dc199f8f5cdf4d398dc755f5ff4b0561f",
    ),
    "R297_ORDINARY": (
        330_724,
        "Round297_ordinary_face_occurrence_edge_row_id",
        "52a6ee955af86ac186824c23d27c0372d3c14792839f372620d311c9f144dbe0",
    ),
}


class ProbeError(RuntimeError):
    """Fail-closed diagnostic error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ProbeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1 << 20), b""):
            state.update(piece)
    return state.hexdigest()


class ListHasher:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add_bytes(self, value: bytes) -> None:
        if self.count:
            self.state.update(b",")
        self.state.update(value)
        self.count += 1

    def finish(self) -> str:
        self.state.update(b"]")
        return self.state.hexdigest()


def verify_row(row: dict[str, Any], label: str) -> None:
    need(type(row) is dict and type(row.get("row_sha256")) is str,
         label + ":row shape")
    payload = {key: value for key, value in row.items()
               if key != "row_sha256"}
    need(digest(payload) == row["row_sha256"], label + ":row closure")


def iterate_array(
    stream: TextIO,
    marker: str = '"rows":[',
) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        chunk = stream.read(1 << 20)
        need(bool(chunk), "array marker:" + marker)
        buffer += chunk
        if len(buffer) > 2 * (1 << 20):
            buffer = buffer[-(len(marker) + (1 << 20)):]
    buffer = buffer.split(marker, 1)[1]
    decoder = json.JSONDecoder()
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            chunk = stream.read(1 << 20)
            need(bool(chunk), "unexpected array EOF")
            buffer = chunk
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                value, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                chunk = stream.read(1 << 20)
                need(bool(chunk), "malformed streamed row")
                buffer += chunk
        need(type(value) is dict, "streamed row object")
        yield value
        buffer = buffer[end:]


def gzip_rows(filename: str) -> Iterator[dict[str, Any]]:
    with gzip.open(HERE / filename, "rt", encoding="utf-8") as stream:
        yield from iterate_array(stream)


def r266_member_rows() -> Iterator[dict[str, Any]]:
    marker = b'"formal_post_Round266_component_member_frontier_ledger":'
    path = HERE / R266
    with path.open("rb") as stream:
        mapped = mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ)
        table_at = mapped.find(marker)
        rows_at = mapped.find(b'"rows":[', table_at)
        mapped.close()
    need(table_at >= 0 and rows_at >= 0, "Round266 member marker")
    with path.open("rt", encoding="utf-8") as stream:
        stream.seek(rows_at)
        yield from iterate_array(stream)


def audit_rows(
    rows: Iterable[dict[str, Any]],
    table: str,
    consume: Callable[[dict[str, Any]], None],
) -> None:
    expected_count, id_field, expected_rows_sha = TABLES[table]
    row_ids: set[str] = set()
    rows_hash = ListHasher()
    for row in rows:
        verify_row(row, table)
        row_id = row[id_field]
        need(row_id not in row_ids, table + ":duplicate row ID")
        row_ids.add(row_id)
        rows_hash.add_bytes(canonical(row))
        consume(row)
    need(
        len(row_ids) == expected_count
        and rows_hash.count == expected_count
        and rows_hash.finish() == expected_rows_sha,
        table + ":complete commitment",
    )


class DSU:
    def __init__(self, count: int) -> None:
        self.parent = list(range(count))
        self.size = [1] * count
        self.rank = 0

    def add(self) -> int:
        value = len(self.parent)
        self.parent.append(value)
        self.size.append(1)
        return value

    def find(self, value: int) -> int:
        parent = self.parent
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(self, left: int, right: int) -> bool:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        self.rank += 1
        return True

    def component_count(self) -> int:
        return sum(self.find(value) == value
                   for value in range(len(self.parent)))


def pair(left: str, right: str) -> tuple[str, str]:
    need(left != right, "nonself occurrence pair")
    return (left, right) if left < right else (right, left)


def retain_sample(samples: dict[str, list[str]], root: str, member: str) -> None:
    values = samples.setdefault(root, [])
    if len(values) < 6:
        values.append(member)


def load_universe() -> tuple[
    list[str],
    dict[str, int],
    list[str | None],
    list[int],
    list[list[str]],
    dict[str, str | None],
    dict[str, int],
]:
    old_occurrence_root: dict[str, str] = {}
    root_key: dict[str, str | None] = {}
    root_member_count: Counter[str] = Counter()
    root_samples: dict[str, list[str]] = {}
    member_kinds: Counter[str] = Counter()

    def member(row: dict[str, Any]) -> None:
        root = row["post_Round266_quotient_component_id"]
        key = row["official_key_id"]
        prior = root_key.setdefault(root, key)
        need(prior == key, "Round266 root key purity")
        member_id = row["component_member_id"]
        kind = row["component_member_kind"]
        member_kinds[kind] += 1
        root_member_count[root] += 1
        retain_sample(root_samples, root, member_id)
        if kind == "EXPANDED_OCCURRENCE":
            need(member_id not in old_occurrence_root,
                 "unique old occurrence member")
            old_occurrence_root[member_id] = root

    audit_rows(r266_member_rows(), "R266_MEMBER", member)
    need(
        member_kinds == {
            "EXPANDED_OCCURRENCE": 126_468,
            "VALID_VIRTUAL_STRATUM": 133_284,
        }
        and len(old_occurrence_root) == 126_468
        and len(root_key) == 63_224
        and sum(root_member_count.values()) == 259_752,
        "Round266 complete member universe",
    )

    occurrence_key: dict[str, str | None] = {}
    occurrence_root: dict[str, str] = {}
    registry_kinds: Counter[str] = Counter()

    def registry(row: dict[str, Any]) -> None:
        occurrence = row["registry_occurrence_id"]
        key = row["official_key_id"]
        need(occurrence not in occurrence_key, "unique registry occurrence")
        occurrence_key[occurrence] = key
        kind = row["registry_entry_kind"]
        registry_kinds[kind] += 1
        if occurrence in old_occurrence_root:
            root = old_occurrence_root[occurrence]
            need(root_key[root] == key, "old occurrence registry key")
        else:
            root = occurrence
            need(root not in root_key, "new singleton root")
            root_key[root] = key
            root_member_count[root] = 1
            root_samples[root] = [occurrence]
        occurrence_root[occurrence] = root

    audit_rows(gzip_rows(R294), "R294_REGISTRY", registry)
    need(
        registry_kinds == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
            "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT":
                9_404,
        }
        and set(old_occurrence_root) <= set(occurrence_root)
        and len(occurrence_root) == len(occurrence_key) == 431_208
        and len(root_key) == 367_964
        and sum(root_member_count.values()) == 564_492,
        "complete expanded member/base-root universe",
    )

    roots = sorted(root_key)
    root_index = {root: index for index, root in enumerate(roots)}
    keys = [root_key[root] for root in roots]
    counts = [root_member_count[root] for root in roots]
    samples = [root_samples[root] for root in roots]
    occurrence_index = {
        occurrence: root_index[root]
        for occurrence, root in occurrence_root.items()
    }
    return (
        roots, root_index, keys, counts, samples,
        occurrence_key, occurrence_index,
    )


def load_channels(
    occurrence_key: dict[str, str | None],
    occurrence_index: dict[str, int],
) -> tuple[
    list[tuple[int, int]],
    list[tuple[int, int]],
    list[tuple[int, int]],
    list[tuple[int, int]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    ordinary: list[tuple[int, int]] = []
    ordinary_occurrence: set[tuple[str, str]] = set()

    def ordinary_row(row: dict[str, Any]) -> None:
        endpoints = row["exact_occurrence_endpoint_pair"]
        need(len(endpoints) == 2, "ordinary endpoints")
        occurrence_pair = pair(*endpoints)
        need(
            occurrence_pair not in ordinary_occurrence
            and all(value in occurrence_index for value in occurrence_pair),
            "ordinary distinct registry pair",
        )
        ordinary_occurrence.add(occurrence_pair)
        ordinary.append(tuple(
            occurrence_index[value] for value in occurrence_pair
        ))

    audit_rows(gzip_rows(R297), "R297_ORDINARY", ordinary_row)
    need(len(ordinary_occurrence) == len(ordinary) == 330_724,
         "ordinary pair census")

    seam: list[tuple[int, int]] = []
    seam_occurrence: set[tuple[str, str]] = set()

    def seam_row(row: dict[str, Any]) -> None:
        occurrence_pair = pair(
            row["left_formal_occurrence_id"],
            row["right_formal_occurrence_id"],
        )
        need(all(value in occurrence_index for value in occurrence_pair),
             "seam registry pair")
        seam_occurrence.add(occurrence_pair)
        seam.append(tuple(
            occurrence_index[value] for value in occurrence_pair
        ))

    audit_rows(gzip_rows(R296), "R296_SEAM", seam_row)
    need(len(seam) == 48_444 and len(seam_occurrence) == 15_316,
         "seam row/pair census")
    seam_same_key = {
        values for values in seam_occurrence
        if occurrence_key[values[0]] == occurrence_key[values[1]]
    }
    seam_unkeyed_endpoints = {
        value
        for values in seam_occurrence
        for value in values
        if occurrence_key[value] is None
    }
    need(
        len(seam_same_key) == 2_976
        and len(seam_occurrence - seam_same_key) == 12_340
        and len(seam_unkeyed_endpoints) == 5_068,
        "seam official-key/unkeyed diagnostic census",
    )

    lower_pair_rows: dict[tuple[str, str], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    single_target_count = 0
    witness_histogram: Counter[str] = Counter()

    def lower_row(row: dict[str, Any]) -> None:
        nonlocal single_target_count
        endpoints = row["target_Round294_registry_occurrence_ids"]
        need(
            len(endpoints)
            == row["target_Round294_registry_reference_count"],
            "lower target count",
        )
        witness_histogram[row["witness_kind"]] += 1
        if len(endpoints) == 1:
            single_target_count += 1
            need(endpoints[0] in occurrence_index, "lower single registry")
            return
        need(len(endpoints) == 2, "lower one-or-two targets")
        occurrence_pair = pair(*endpoints)
        need(all(value in occurrence_index for value in occurrence_pair),
             "lower registry pair")
        lower_pair_rows[occurrence_pair].append({
            "row_id":
                row["Round295A_R291_physical_incidence_binding_row_id"],
            "witness_kind": row["witness_kind"],
        })

    audit_rows(gzip_rows(R295A), "R295A_INCIDENCE", lower_row)
    lower_occurrence = set(lower_pair_rows)
    lower_same_key_occurrence = {
        values for values in lower_occurrence
        if occurrence_key[values[0]] == occurrence_key[values[1]]
    }
    lower_cross_key_occurrence = (
        lower_occurrence - lower_same_key_occurrence
    )
    raw_multi_count = sum(map(len, lower_pair_rows.values()))
    raw_same_key_count = sum(
        len(lower_pair_rows[values])
        for values in lower_same_key_occurrence
    )
    need(
        single_target_count == 1_600
        and raw_multi_count == 111_852
        and len(lower_occurrence) == 111_524
        and len(lower_same_key_occurrence) == 86_308
        and len(lower_cross_key_occurrence) == 25_216
        and witness_histogram == {
            "ROUND179_NEGATIVE_T0_SHADOW_PATCH": 544,
            "ROUND179_POSITIVE_T0_RETAINED_OWNER": 440,
            "ROUND182_GRAPH_SHEET_LEAF": 111_524,
            "ROUND182_TRANSVERSE_1D_LINE": 112,
            "ROUND208_DIRECT_GRAPH_SIDE_REGION": 608,
            "SOURCE_EXACT_T0_SHEET_CELL": 224,
        },
        "lower physical-incidence census",
    )
    need(
        not (lower_occurrence & ordinary_occurrence)
        and not (lower_occurrence & seam_occurrence),
        "lower pair channel disjointness",
    )
    ordinary_seam_overlap = ordinary_occurrence & seam_occurrence
    canonical_pair_union = (
        ordinary_occurrence | seam_occurrence | lower_occurrence
    )

    lower_all = [
        tuple(occurrence_index[value] for value in values)
        for values in sorted(lower_occurrence)
    ]
    lower_same_key = [
        tuple(occurrence_index[value] for value in values)
        for values in sorted(lower_same_key_occurrence)
    ]
    raw_lower_rows = [
        {
            "pair": tuple(occurrence_index[value] for value in values),
            "same_key": values in lower_same_key_occurrence,
            **source,
        }
        for values in sorted(lower_pair_rows)
        for source in lower_pair_rows[values]
    ]
    diagnostics = {
        "raw_witness_consumption": {
            "ordinary_witness_row_count": len(ordinary),
            "true_seam_witness_row_count": len(seam),
            "lower_two_target_witness_row_count": raw_multi_count,
            "three_edge_channel_raw_witness_row_count":
                len(ordinary) + len(seam) + raw_multi_count,
            "lower_single_target_assignment_only_row_count":
                single_target_count,
        },
        "canonical_endpoint_pair_projection": {
            "ordinary_distinct_pair_count": len(ordinary_occurrence),
            "true_seam_distinct_pair_count": len(seam_occurrence),
            "lower_distinct_pair_count": len(lower_occurrence),
            "sum_before_cross_channel_deduplication":
                len(ordinary_occurrence)
                + len(seam_occurrence)
                + len(lower_occurrence),
            "cross_channel_union_pair_count": len(canonical_pair_union),
            "ordinary_true_seam_intersection_count":
                len(ordinary_seam_overlap),
            "ordinary_lower_intersection_count":
                len(ordinary_occurrence & lower_occurrence),
            "true_seam_lower_intersection_count":
                len(seam_occurrence & lower_occurrence),
            "three_way_intersection_count": len(
                ordinary_occurrence
                & seam_occurrence
                & lower_occurrence
            ),
        },
        "ordinary_distinct_occurrence_pair_count":
            len(ordinary_occurrence),
        "ordinary_same_official_key_distinct_pair_count": sum(
            occurrence_key[values[0]] == occurrence_key[values[1]]
            for values in ordinary_occurrence
        ),
        "ordinary_different_official_key_distinct_pair_count": sum(
            occurrence_key[values[0]] != occurrence_key[values[1]]
            for values in ordinary_occurrence
        ),
        "seam_row_count": len(seam),
        "seam_distinct_occurrence_pair_count": len(seam_occurrence),
        "seam_same_official_key_distinct_pair_count":
            len(seam_same_key),
        "seam_different_official_key_distinct_pair_count":
            len(seam_occurrence - seam_same_key),
        "seam_distinct_unkeyed_occurrence_endpoint_count":
            len(seam_unkeyed_endpoints),
        "lower_single_target_witness_row_count": single_target_count,
        "lower_multi_target_witness_row_count": raw_multi_count,
        "lower_distinct_occurrence_pair_count": len(lower_occurrence),
        "lower_duplicate_pair_excess": raw_multi_count - len(lower_occurrence),
        "lower_same_official_key_distinct_pair_count":
            len(lower_same_key_occurrence),
        "lower_cross_official_key_distinct_pair_count":
            len(lower_cross_key_occurrence),
        "lower_same_official_key_raw_witness_row_count":
            raw_same_key_count,
        "lower_cross_official_key_raw_witness_row_count":
            raw_multi_count - raw_same_key_count,
        "lower_ordinary_pair_intersection_count":
            len(lower_occurrence & ordinary_occurrence),
        "lower_seam_pair_intersection_count":
            len(lower_occurrence & seam_occurrence),
        "witness_kind_histogram": dict(sorted(witness_histogram.items())),
    }
    return (
        ordinary, seam, lower_all, lower_same_key,
        raw_lower_rows, diagnostics,
    )


def channel_snapshot(
    dsu: DSU,
    edges: list[tuple[int, int]],
) -> dict[str, int]:
    base_pairs = {
        (left, right) if left <= right else (right, left)
        for left, right in edges
    }
    current_pairs: set[tuple[int, int]] = set()
    current_same_rows = 0
    for left, right in edges:
        left = dsu.find(left)
        right = dsu.find(right)
        if left == right:
            current_same_rows += 1
        current_pairs.add(
            (left, right) if left <= right else (right, left)
        )
    return {
        "edge_row_count": len(edges),
        "distinct_base_root_pair_count": len(base_pairs),
        "base_same_root_edge_row_count":
            sum(left == right for left, right in edges),
        "base_cross_root_edge_row_count":
            sum(left != right for left, right in edges),
        "current_same_root_edge_row_count": current_same_rows,
        "current_cross_root_edge_row_count":
            len(edges) - current_same_rows,
        "distinct_current_root_pair_count": len(current_pairs),
        "distinct_current_same_root_pair_count":
            sum(left == right for left, right in current_pairs),
        "distinct_current_cross_root_pair_count":
            sum(left != right for left, right in current_pairs),
        "base_root_pair_collapse_from_rows":
            len(edges) - len(base_pairs),
        "current_root_pair_collapse_from_rows":
            len(edges) - len(current_pairs),
    }


def simulate(
    node_count: int,
    channels: dict[str, list[tuple[int, int]]],
    order: tuple[str, ...],
    reverse_within_channel: bool = False,
) -> tuple[dict[str, Any], DSU]:
    dsu = DSU(node_count)
    per_channel: dict[str, Any] = {}
    for name in order:
        edges = channels[name]
        snapshot = channel_snapshot(dsu, edges)
        before = dsu.rank
        iterable = reversed(edges) if reverse_within_channel else edges
        for left, right in iterable:
            dsu.union(left, right)
        delta = dsu.rank - before
        per_channel[name] = {
            **snapshot,
            "sequential_rank_reduction": delta,
            "sequential_redundant_edge_row_count": len(edges) - delta,
            "component_count_after_channel":
                node_count - dsu.rank,
        }
    return ({
        "channel_order": list(order),
        "reverse_within_channel": reverse_within_channel,
        "per_channel": per_channel,
        "final_rank_reduction": dsu.rank,
        "final_component_count": node_count - dsu.rank,
    }, dsu)


def partition_equal(left: DSU, right: DSU, node_count: int) -> bool:
    left_to_right: dict[int, int] = {}
    right_to_left: dict[int, int] = {}
    for value in range(node_count):
        left_root = left.find(value)
        right_root = right.find(value)
        prior_right = left_to_right.setdefault(left_root, right_root)
        prior_left = right_to_left.setdefault(right_root, left_root)
        if prior_right != right_root or prior_left != left_root:
            return False
    return True


def witness_node_replay(
    node_count: int,
    ordinary: list[tuple[int, int]],
    seam: list[tuple[int, int]],
    raw_lower_rows: list[dict[str, Any]],
    accept_same_key_only: bool,
    direct: DSU,
) -> dict[str, Any]:
    dsu = DSU(node_count)
    for left, right in ordinary:
        dsu.union(left, right)
    for left, right in seam:
        dsu.union(left, right)
    accepted = 0
    for row in raw_lower_rows:
        if accept_same_key_only and not row["same_key"]:
            continue
        witness = dsu.add()
        left, right = row["pair"]
        dsu.union(witness, left)
        dsu.union(witness, right)
        accepted += 1
    return {
        "accepted_physical_witness_node_count": accepted,
        "augmented_node_count": len(dsu.parent),
        "augmented_rank_reduction": dsu.rank,
        "augmented_component_count": dsu.component_count(),
        "direct_formal_member_component_count":
            node_count - direct.rank,
        "formal_member_partition_equal_to_direct_pair_union":
            partition_equal(direct, dsu, node_count),
        "witness_nodes_change_formal_member_partition": False,
    }


def purity_audit(
    dsu: DSU,
    roots: list[str],
    keys: list[str | None],
    member_counts: list[int],
    member_samples: list[list[str]],
) -> dict[str, Any]:
    unkeyed = "<UNKEYED_NULL>"
    component_total: Counter[int] = Counter()
    first_key: dict[int, str] = {}
    first_key_total: Counter[int] = Counter()
    mixed_key_members: dict[int, Counter[str]] = {}

    for index, key in enumerate(keys):
        root = dsu.find(index)
        count = member_counts[index]
        key_label = unkeyed if key is None else key
        component_total[root] += count
        if root in mixed_key_members:
            mixed_key_members[root][key_label] += count
        elif root not in first_key:
            first_key[root] = key_label
            first_key_total[root] = count
        elif first_key[root] == key_label:
            first_key_total[root] += count
        else:
            if root not in mixed_key_members:
                mixed_key_members[root] = Counter({
                    first_key[root]: first_key_total[root]
                })
            mixed_key_members[root][key_label] += count

    need(
        sum(component_total.values()) == 564_492
        and len(component_total) == len(dsu.parent) - dsu.rank,
        "purity component/member conservation",
    )
    key_members_by_component = {
        root: (
            mixed_key_members[root]
            if root in mixed_key_members
            else Counter({first_key[root]: first_key_total[root]})
        )
        for root in component_total
    }
    diverse_roots = {
        root for root, histogram in key_members_by_component.items()
        if len(histogram) > 1
    }
    multi_keyed_roots = {
        root for root, histogram in key_members_by_component.items()
        if sum(key != unkeyed for key in histogram) > 1
    }
    unkeyed_roots = {
        root for root, histogram in key_members_by_component.items()
        if unkeyed in histogram
    }
    unkeyed_only_roots = {
        root for root in unkeyed_roots
        if len(key_members_by_component[root]) == 1
    }
    keyed_and_unkeyed_roots = unkeyed_roots - unkeyed_only_roots
    diverse_constituent_roots: dict[int, list[int]] = defaultdict(list)
    for index in range(len(roots)):
        final = dsu.find(index)
        if final in diverse_roots:
            diverse_constituent_roots[final].append(index)

    examples = []
    for final in diverse_roots:
        constituents = diverse_constituent_roots[final]
        anchor = min(roots[index] for index in constituents)
        samples = sorted({
            member
            for index in constituents
            for member in member_samples[index]
        })[:10]
        key_histogram = mixed_key_members[final]
        examples.append({
            "stable_component_anchor": anchor,
            "member_count": component_total[final],
            "constituent_base_root_count": len(constituents),
            "distinct_key_label_count": len(key_histogram),
            "distinct_nonnull_official_key_count":
                sum(key != unkeyed for key in key_histogram),
            "contains_unkeyed_members": unkeyed in key_histogram,
            "official_key_member_histogram":
                dict(sorted(key_histogram.items())),
            "member_id_samples": samples,
        })
    examples.sort(key=lambda row: row["stable_component_anchor"])
    nonnull_incidence_histogram = Counter(
        sum(key != unkeyed for key in histogram)
        for histogram in key_members_by_component.values()
    )
    all_label_incidence_histogram = Counter(
        len(histogram)
        for histogram in key_members_by_component.values()
    )
    return {
        "component_count": len(component_total),
        "member_count": sum(component_total.values()),
        "key_purity_is_rejection_condition": False,
        "key_purity_violation_component_count": len(diverse_roots),
        "members_in_key_purity_violation_components": sum(
            component_total[root] for root in diverse_roots
        ),
        "constituent_base_roots_in_key_purity_violation_components": sum(
            len(values) for values in diverse_constituent_roots.values()
        ),
        "key_pure_component_count":
            len(component_total) - len(diverse_roots),
        "multiple_nonnull_official_key_component_count":
            len(multi_keyed_roots),
        "members_in_multiple_nonnull_official_key_components": sum(
            component_total[root] for root in multi_keyed_roots
        ),
        "component_official_key_incidence_count": sum(
            sum(key != unkeyed for key in histogram)
            for histogram in key_members_by_component.values()
        ),
        "nonnull_official_key_count_per_component_histogram": {
            str(key): value
            for key, value in sorted(
                nonnull_incidence_histogram.items()
            )
        },
        "all_key_labels_per_component_histogram": {
            str(key): value
            for key, value in sorted(
                all_label_incidence_histogram.items()
            )
        },
        "max_nonnull_official_key_count_in_one_component": max(
            nonnull_incidence_histogram
        ),
        "unkeyed_formal_member_count": sum(
            histogram.get(unkeyed, 0)
            for histogram in key_members_by_component.values()
        ),
        "component_count_with_unkeyed_members": len(unkeyed_roots),
        "unkeyed_only_component_count": len(unkeyed_only_roots),
        "mixed_keyed_and_unkeyed_component_count":
            len(keyed_and_unkeyed_roots),
        "members_in_components_with_unkeyed_members": sum(
            component_total[root] for root in unkeyed_roots
        ),
        "key_purity_violation_examples": examples[:8],
    }


def scenario(
    name: str,
    roots: list[str],
    keys: list[str | None],
    member_counts: list[int],
    member_samples: list[list[str]],
    ordinary: list[tuple[int, int]],
    seam: list[tuple[int, int]],
    lower: list[tuple[int, int]],
    raw_lower_rows: list[dict[str, Any]],
    same_key_only: bool,
) -> dict[str, Any]:
    channels = {
        "ORDINARY": ordinary,
        "TRUE_SEAM": seam,
        "LOWER_PHYSICAL_INCIDENCE": lower,
    }
    permutation_results = []
    final_pairs: set[tuple[int, int]] = set()
    for order in itertools.permutations(channels):
        audit, _ = simulate(len(roots), channels, order)
        permutation_results.append(audit)
        final_pairs.add((
            audit["final_rank_reduction"],
            audit["final_component_count"],
        ))
    need(len(final_pairs) == 1, name + ":channel order independence")
    forward, direct = simulate(
        len(roots),
        channels,
        ("ORDINARY", "TRUE_SEAM", "LOWER_PHYSICAL_INCIDENCE"),
    )
    reverse, reversed_dsu = simulate(
        len(roots),
        channels,
        ("ORDINARY", "TRUE_SEAM", "LOWER_PHYSICAL_INCIDENCE"),
        reverse_within_channel=True,
    )
    need(
        (
            forward["final_rank_reduction"],
            forward["final_component_count"],
        )
        == (
            reverse["final_rank_reduction"],
            reverse["final_component_count"],
        )
        and partition_equal(direct, reversed_dsu, len(roots)),
        name + ":within-channel order independence",
    )
    witness = witness_node_replay(
        len(roots), ordinary, seam, raw_lower_rows,
        same_key_only, direct,
    )
    need(
        witness["formal_member_partition_equal_to_direct_pair_union"]
        and witness["augmented_component_count"]
        == forward["final_component_count"],
        name + ":witness-node equivalence",
    )
    purity = purity_audit(
        direct, roots, keys, member_counts, member_samples
    )
    need(
        purity["component_count"] == forward["final_component_count"],
        name + ":purity/final count",
    )
    return {
        "scenario": name,
        "hypothesis_only_not_promoted": True,
        "lower_channel_semantics_status":
            "PENDING_COMPONENT_CONNECTIVITY_AUDIT",
        "forward_order_audit": forward,
        "all_channel_permutations": permutation_results,
        "channel_order_independent_final_rank_and_component_count": True,
        "reverse_within_each_channel_final_audit": reverse,
        "within_channel_order_independent_partition": True,
        "witness_node_equivalence": witness,
        "final_key_purity_audit": purity,
    }


def build() -> dict[str, Any]:
    for filename, expected in FILE_PINS.items():
        need(file_sha256(HERE / filename) == expected,
             "file pin:" + filename)
    (
        roots, _root_index, keys, member_counts, member_samples,
        occurrence_key, occurrence_index,
    ) = load_universe()
    (
        ordinary, seam, lower_all, lower_same_key,
        raw_lower_rows, channel_diagnostics,
    ) = load_channels(occurrence_key, occurrence_index)
    scenario_a = scenario(
        "A_ALL_111524_DISTINCT_LOWER_PAIRS",
        roots, keys, member_counts, member_samples,
        ordinary, seam, lower_all, raw_lower_rows, False,
    )
    scenario_b = scenario(
        "B_86308_SAME_OFFICIAL_KEY_LOWER_PAIRS_ONLY",
        roots, keys, member_counts, member_samples,
        ordinary, seam, lower_same_key, raw_lower_rows, True,
    )
    return {
        "schema":
            "cm2.round298.expanded-registry-component-dsu."
            "diagnostic-probe.v1",
        "status":
            "PASS_READ_ONLY_NONPROMOTED_TWO_HYPOTHESIS_DSU_DIAGNOSTIC",
        "formal_Round298_candidate_written": False,
        "formal_credit_issued": False,
        "input_file_pins": dict(sorted(FILE_PINS.items())),
        "expanded_universe": {
            "formal_occurrence_member_count": 431_208,
            "retained_virtual_member_count": 133_284,
            "full_member_count": 564_492,
            "base_root_count": 367_964,
            "inherited_Round266_rank_reduction": 196_528,
        },
        "channel_diagnostics": channel_diagnostics,
        "scenarios": [scenario_a, scenario_b],
        "strict_nonpromotion": {
            "lower_physical_incidence_component_connectivity_semantics":
                "PENDING",
            "Round298_component_count": None,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = build()
    payload = canonical(result) + b"\n"
    if arguments.output is not None:
        arguments.output.write_bytes(payload)
    print(json.dumps({
        "status": result["status"],
        "scenarios": [
            {
                "scenario": row["scenario"],
                "rank": row["forward_order_audit"][
                    "final_rank_reduction"
                ],
                "components": row["forward_order_audit"][
                    "final_component_count"
                ],
                "key_purity_violation_components":
                    row["final_key_purity_audit"][
                        "key_purity_violation_component_count"
                    ],
                "key_purity_violation_members":
                    row["final_key_purity_audit"][
                        "members_in_key_purity_violation_components"
                    ],
            }
            for row in result["scenarios"]
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
