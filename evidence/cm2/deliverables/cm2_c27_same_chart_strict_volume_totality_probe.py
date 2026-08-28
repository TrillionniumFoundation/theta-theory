#!/usr/bin/env python3
"""Direct-source totality probe for strict same-chart volume intersections.

The candidate universe is rebuilt from the six primitive support kernels and
is joined independently to C15 and C25.  C26 is read only as a feature-cover
audit: absence of a C26 node is never interpreted as a negative geometric
theorem.  Round306C27, its FAMILIES table, historical edge ledgers, and the
older SAME_CHART census ledger are forbidden inputs.

Only strict intersection in all three physical coordinates is promoted by
this probe.  Lower-dimensional closure contacts are deliberately outside this
subgate because C19C endpoint ownership is a separate fail-closed obligation.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import cmp_to_key
import gzip
import hashlib
import json
import math
from pathlib import Path
import random
import sqlite3
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_c27_same_chart_strict_volume_totality_v1"
OCCURRENCE_LEDGER = PREFIX + "_witness_occurrences.jsonl.gz"
MEMBER_PAIR_LEDGER = PREFIX + "_member_pairs.jsonl.gz"
COMPONENT_EDGE_LEDGER = PREFIX + "_component_edges.jsonl.gz"
CLUSTER_LEDGER = PREFIX + "_affected_clusters.jsonl.gz"
RESULT = PREFIX + "_result.json"

FILES = {
    "C15": ("cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz", "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    "C25": ("cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz", "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6"),
    "C26": ("cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz", "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e"),
    "C19A": ("cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz", "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3"),
    "C19B": ("cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz", "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798"),
    "C19C": ("cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz", "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84"),
    "C20A": ("cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz", "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922"),
    "C22A": ("cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz", "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb"),
    "C23A": ("cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz", "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528"),
    "R179": ("cm2_round179_source_g_residual_tube_arrangement_rows.json", "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),
    "R234": ("cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    "R236": ("cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    "C5": ("cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz", "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
}
SOURCE_COUNTS = {"C19A": 5596, "C19B": 12232, "C19C": 33344, "C20A": 126468, "C22A": 295340, "C23A": 10252}
SOURCE_KERNEL = {"C19A": "C19A", "C19B": "C19B", "C19C": "C19C", "C20A": "C20A", "C22A": "C22B", "C23A": "C23B"}
CHARTS = {"G:E", "G:N", "G:W", "G:S"}


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def closed_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"canonical:{path.name}:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == object_sha(body), f"closure:{path.name}:{ordinal}")
            yield row


def qwire(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


# Internal endpoint: (0, Fraction) for Q; (1, Fraction radicand, +/-1) for signed sqrt.
Endpoint = tuple[Any, ...]


def q_endpoint(value: str) -> Endpoint:
    return (0, Fraction(value))


def sqrt_endpoint(value: str, sign: int) -> Endpoint:
    radicand = Fraction(value)
    need(radicand >= 0 and sign in {-1, 1}, "signed sqrt domain")
    rn, rd = math.isqrt(radicand.numerator), math.isqrt(radicand.denominator)
    if rn * rn == radicand.numerator and rd * rd == radicand.denominator:
        return (0, Fraction(sign * rn, rd))
    return (1, radicand, sign)


def endpoint_wire(value: Endpoint) -> dict[str, Any]:
    if value[0] == 0:
        return {"kind": "Q", "value": qwire(value[1])}
    return {"kind": "SIGNED_SQRT_Q", "radicand": qwire(value[1]), "sign": value[2]}


def compare_endpoint(left: Endpoint, right: Endpoint) -> int:
    if left == right:
        return 0
    if left[0] == right[0] == 0:
        return -1 if left[1] < right[1] else 1
    if left[0] == right[0] == 1:
        lq, ls, rq, rs = left[1], left[2], right[1], right[2]
        if ls != rs:
            return -1 if ls < rs else 1
        if lq == rq:
            return 0
        order = -1 if lq < rq else 1
        return order if ls == 1 else -order
    if left[0] == 0:
        rational, radicand, sign = left[1], right[1], right[2]
        if sign == 1:
            if rational < 0:
                return -1
            delta = rational * rational - radicand
            return 0 if delta == 0 else (-1 if delta < 0 else 1)
        if rational >= 0:
            return 1
        delta = rational * rational - radicand
        return 0 if delta == 0 else (-1 if delta > 0 else 1)
    return -compare_endpoint(right, left)


def max_endpoint(left: Endpoint, right: Endpoint) -> Endpoint:
    return right if compare_endpoint(left, right) < 0 else left


def min_endpoint(left: Endpoint, right: Endpoint) -> Endpoint:
    return left if compare_endpoint(left, right) < 0 else right


def width_proof(lower: Endpoint, upper: Endpoint, axis: str) -> dict[str, Any]:
    need(compare_endpoint(lower, upper) < 0, "strict intersection width:" + axis)
    body = {"axis": axis, "lower": endpoint_wire(lower), "upper": endpoint_wire(upper)}
    if lower[0] == upper[0] == 0:
        body.update({"relation": "UPPER_MINUS_LOWER_IS_POSITIVE_RATIONAL", "exact_positive_difference": qwire(upper[1] - lower[1])})
    else:
        body.update({"relation": "EXACT_ALGEBRAIC_ENDPOINT_COMPARATOR_IS_STRICT", "comparator_result": -1})
    return body


def normalized_bounds(source: str, support: dict[str, Any]) -> tuple[Endpoint, ...]:
    raw = support.get("bounds")
    need(type(raw) is list and len(raw) == 6 and all(type(x) is str for x in raw), "six exact bounds:" + source)
    if source != "C23A":
        need(support.get("coordinates") == ["t", "p", "s"], "physical coordinates:" + source)
        bounds = tuple(q_endpoint(value) for value in raw)
    else:
        need(support.get("kind") == "T2PS_BRANCH_OPEN_RATIONAL_BOX" and support.get("coordinates") == ["t_squared", "p", "s"], "C23 t2ps AST")
        sign = support.get("physical_t_sign")
        need(sign in {-1, 1}, "C23 physical sign")
        if sign == 1:
            t0, t1 = sqrt_endpoint(raw[0], 1), sqrt_endpoint(raw[1], 1)
        else:
            t0, t1 = sqrt_endpoint(raw[1], -1), sqrt_endpoint(raw[0], -1)
        bounds = (t0, t1, q_endpoint(raw[2]), q_endpoint(raw[3]), q_endpoint(raw[4]), q_endpoint(raw[5]))
    for axis in range(3):
        need(compare_endpoint(bounds[2 * axis], bounds[2 * axis + 1]) < 0, f"positive primitive width:{source}:{axis}")
    return bounds


def load_chart_maps() -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]:
    r179 = json.loads((ROOT / FILES["R179"][0]).read_bytes())
    packed = r179["result"]["retained_3d_child_rows"]
    r179_chart = {row[0]: row[3] for row in packed}
    need(len(r179_chart) == len(packed), "R179 unique")
    r234 = json.loads((ROOT / FILES["R234"][0]).read_bytes())
    rows = r234["result"]["resolved_descendant_rows"]
    r234_chart = {row["materialized_row_id"]: row["chart"] for row in rows}
    need(len(r234_chart) == len(rows), "R234 unique")
    r236 = json.loads((ROOT / FILES["R236"][0]).read_bytes())
    rows = r236["result"]["crossing_dependency_discharge_rows"]
    r236_chart = {row["crossing_dependency_discharge_row_id"]: row["local_return_signature"]["source_chart"] for row in rows}
    need(len(r236_chart) == len(rows) == 32, "R236 unique")
    c5_chart: dict[str, str] = {}
    for row in closed_rows(ROOT / FILES["C5"][0]):
        semantic = row["semantic_classification"]
        if semantic["classification"] == "EMPTY_GRAPH":
            c5_chart[row["row_sha256"]] = semantic["kernel_parameters"]["source_chart"]
    need(len(c5_chart) == 33344, "C5 empty graph chart census")
    return r179_chart, r234_chart, r236_chart, c5_chart


def chart_for(source: str, row: dict[str, Any], maps: tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]) -> str:
    r179, r234, r236, c5 = maps
    if source == "C19A":
        chart = r179[row["construction_certificate"]["retained_child_row_id"]]
    elif source == "C19B":
        row_id = row["construction_certificate"]["source_partition_row_id"]
        chart = r234[row_id] if row_id.startswith("round234-resolved:") else r236[row_id]
    elif source == "C19C":
        chart = c5[row["construction_certificate"]["C5_row_sha256"]]
    elif source in {"C20A", "C22A"}:
        chart = row["support_ast"]["coordinate_chart"]
    else:
        need(source == "C23A", "known source")
        chart = row["support_ast"]["recharted_target_chart"]
    need(chart in CHARTS, "four-chart atom")
    return chart


def owner_for(row: dict[str, Any]) -> str:
    return row.get("member_id") or row["owner_member_id"]


def component_for(row: dict[str, Any]) -> str:
    return row.get("fresh_component_id") or row["owner_fresh_component_id"]


def atom_id_for(source: str, row: dict[str, Any]) -> str:
    if source == "C22A":
        return row["predicate_cell_row_id"]
    if source == "C23A":
        return row["R292_refinement_cell_id"]
    return f"{source.lower()}-support-atom:{row['row_sha256']}"


def write_rows(path: Path, rows: Iterable[dict[str, Any]]) -> tuple[int, str]:
    count = 0
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as packed:
            for ordinal, body in enumerate(rows):
                closed = {**body, "ordinal": ordinal}
                closed["row_sha256"] = object_sha(closed)
                sequence.update(bytes.fromhex(closed["row_sha256"]))
                packed.write(canonical(closed) + b"\n")
                count += 1
    return count, sequence.hexdigest()


class DSU:
    def __init__(self, values: Iterable[str]) -> None:
        self.parent = {value: value for value in values}
        self.size = {value: 1 for value in self.parent}

    def find(self, value: str) -> str:
        root = value
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[value] != value:
            nxt = self.parent[value]
            self.parent[value] = root
            value = nxt
        return root

    def union(self, left: str, right: str) -> None:
        a, b = self.find(left), self.find(right)
        if a == b:
            return
        if self.size[a] < self.size[b] or (self.size[a] == self.size[b] and a > b):
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]


def build(candidate_dir: Path, seed: int) -> dict[str, Any]:
    need(type(seed) is int and seed > 0, "real positive seed")
    need(not candidate_dir.exists() or not any(candidate_dir.iterdir()), "candidate dir must be new or empty")
    candidate_dir.mkdir(parents=True, exist_ok=True)
    for role, (filename, expected) in FILES.items():
        need(file_sha(ROOT / filename) == expected, "input pin:" + role)

    maps = load_chart_maps()
    atoms: list[dict[str, Any]] = []
    owner_sources: dict[str, set[str]] = defaultdict(set)
    source_counts = Counter()
    endpoint_sets = [set(), set(), set()]
    atom_ids: set[str] = set()
    for source in SOURCE_COUNTS:
        for row in closed_rows(ROOT / FILES[source][0]):
            source_counts[source] += 1
            owner = owner_for(row)
            embedded_component = component_for(row)
            aid = atom_id_for(source, row)
            need(aid not in atom_ids, "unique atom id")
            atom_ids.add(aid)
            bounds = normalized_bounds(source, row["support_ast"])
            chart = chart_for(source, row, maps)
            support_kind = row["support_ast"]["kind"]
            owner_sources[owner].add(source)
            for axis in range(3):
                endpoint_sets[axis].update(bounds[2 * axis:2 * axis + 2])
            atoms.append({
                "atom_id": aid,
                "source": source,
                "source_row_sha256": row["row_sha256"],
                "owner": owner,
                "embedded_component": embedded_component,
                "chart": chart,
                "bounds": bounds,
                "support_kind": support_kind,
            })
        need(source_counts[source] == SOURCE_COUNTS[source], "source census:" + source)
    need(len(atoms) == 483232 and len(owner_sources) == 482380, "primitive atom/owner census")
    atoms.sort(key=lambda row: row["atom_id"].encode("ascii"))

    owners = set(owner_sources)
    c15: dict[str, dict[str, Any]] = {}
    all_c15_components: set[str] = set()
    c15_rows = 0
    for row in closed_rows(ROOT / FILES["C15"][0]):
        c15_rows += 1
        all_c15_components.add(row["fresh_component_id"])
        member = row["registry_member_id"]
        if member in owners:
            need(member not in c15, "C15 unique owner")
            c15[member] = {"component": row["fresh_component_id"], "row_sha256": row["row_sha256"]}
    need(c15_rows == 502204 and len(all_c15_components) == 57876 and set(c15) == owners, "complete C15 join")

    c25: dict[str, dict[str, Any]] = {}
    c25_rows = 0
    for row in closed_rows(ROOT / FILES["C25"][0]):
        c25_rows += 1
        member = row["member_id"]
        if member in owners:
            need(member not in c25, "C25 unique owner")
            c25[member] = {
                "component": row["fresh_component_id"],
                "kernel": row["source_bindings"]["support_kernel"],
                "row_sha256": row["row_sha256"],
                "C15_member_row_sha256": row["source_bindings"]["C15_member_row_sha256"],
            }
    need(c25_rows == 502204 and set(c25) == owners, "complete C25 join")
    for owner, sources in owner_sources.items():
        expected_kernels = {SOURCE_KERNEL[source] for source in sources}
        need(len(expected_kernels) == 1, "one support kernel per owner")
        need(c15[owner]["component"] == c25[owner]["component"], "C15/C25 component")
        need(c15[owner]["row_sha256"] == c25[owner]["C15_member_row_sha256"], "C25 binds exact C15 row")
        need(c25[owner]["kernel"] == next(iter(expected_kernels)), "C25 support kernel")
    for atom in atoms:
        owner = atom["owner"]
        need(atom["embedded_component"] == c15[owner]["component"], "primitive/C15 component")
        atom["component"] = c15[owner]["component"]
        atom["C15_row_sha256"] = c15[owner]["row_sha256"]
        atom["C25_row_sha256"] = c25[owner]["row_sha256"]
        atom["C25_support_kernel"] = c25[owner]["kernel"]

    ranks: list[dict[Endpoint, int]] = []
    endpoint_rank_census = []
    for values in endpoint_sets:
        ordered = sorted(values, key=cmp_to_key(compare_endpoint))
        for left, right in zip(ordered, ordered[1:]):
            need(compare_endpoint(left, right) < 0, "strict endpoint rank")
        ranks.append({value: ordinal + 1 for ordinal, value in enumerate(ordered)})
        endpoint_rank_census.append(len(ordered))
    need(endpoint_rank_census == [6433, 1201, 257], "endpoint rank census")
    for atom in atoms:
        rank_bounds: list[int] = []
        for axis in range(3):
            rank_bounds.extend([ranks[axis][atom["bounds"][2 * axis]], ranks[axis][atom["bounds"][2 * axis + 1]]])
        atom["rank_bounds"] = tuple(rank_bounds)

    index_path = candidate_dir / (PREFIX + ".rtree.sqlite")
    connection = sqlite3.connect(index_path)
    connection.execute("PRAGMA journal_mode=OFF")
    connection.execute("PRAGMA synchronous=OFF")
    connection.execute("PRAGMA temp_store=MEMORY")
    chart_tables = {"G:E": "boxes_e", "G:N": "boxes_n", "G:W": "boxes_w", "G:S": "boxes_s"}
    for table in chart_tables.values():
        connection.execute(f"CREATE VIRTUAL TABLE {table} USING rtree_i32(id,t0,t1,p0,p1,s0,s1)")
    order = list(range(len(atoms)))
    random.Random(seed).shuffle(order)
    cursor = connection.cursor()
    query = "SELECT id FROM {table} WHERE t0<? AND t1>? AND p0<? AND p1>? AND s0<? AND s1>?"
    all_strict_pair_count = 0
    same_component_pair_count = 0
    all_source_pairs = Counter()
    cross_source_pairs = Counter()
    witness_rows: list[dict[str, Any]] = []
    witness_owners: set[str] = set()
    for atom_index in order:
        atom = atoms[atom_index]
        rb = atom["rank_bounds"]
        table = chart_tables[atom["chart"]]
        for (old_id,) in cursor.execute(query.format(table=table), (rb[1], rb[0], rb[3], rb[2], rb[5], rb[4])):
            other = atoms[old_id - 1]
            all_strict_pair_count += 1
            source_pair = tuple(sorted((atom["source"], other["source"])))
            all_source_pairs["__".join(source_pair)] += 1
            if atom["component"] == other["component"]:
                same_component_pair_count += 1
                continue
            cross_source_pairs["__".join(source_pair)] += 1
            left, right = sorted((atom, other), key=lambda row: row["atom_id"].encode("ascii"))
            intersection: list[Endpoint] = []
            proofs = []
            for axis, axis_name in enumerate(("t", "p", "s")):
                lower = max_endpoint(left["bounds"][2 * axis], right["bounds"][2 * axis])
                upper = min_endpoint(left["bounds"][2 * axis + 1], right["bounds"][2 * axis + 1])
                proofs.append(width_proof(lower, upper, axis_name))
                intersection.extend([lower, upper])
            exact_equal = left["bounds"] == right["bounds"]
            baseline = source_pair == ("C22A", "C22A") and exact_equal
            witness_id = "same-chart-strict-volume:" + object_sha([left["atom_id"], right["atom_id"]])
            members = []
            for value in (left, right):
                members.append({
                    "atom_id": value["atom_id"],
                    "source_kernel": value["source"],
                    "source_row_sha256": value["source_row_sha256"],
                    "owner_member_id": value["owner"],
                    "C15_component_id": value["component"],
                    "C15_member_row_sha256": value["C15_row_sha256"],
                    "C25_member_row_sha256": value["C25_row_sha256"],
                    "C25_support_kernel": value["C25_support_kernel"],
                    "support_kind": value["support_kind"],
                    "physical_bounds": [endpoint_wire(endpoint) for endpoint in value["bounds"]],
                })
            body = {
                "schema": "cm2.c27.same-chart-strict-volume-totality.v1.witness-occurrence-row.v1",
                "witness_occurrence_id": witness_id,
                "chart": left["chart"],
                "source_pair": list(source_pair),
                "members": members,
                "component_pair": sorted((left["component"], right["component"])),
                "exact_equal_support_boxes": exact_equal,
                "intersection_bounds": [endpoint_wire(endpoint) for endpoint in intersection],
                "strict_positive_width_proofs": proofs,
                "intersection_relation": "STRICT_POSITIVE_VOLUME_INTERIOR_INTERSECTION",
                "endpoint_ownership_bits_used": False,
                "known_228_exact_equal_baseline_occurrence": baseline,
                "incremental_beyond_known_228_occurrences": not baseline,
                "provisional_transition_witness": True,
                "formal_credit": 0,
            }
            witness_rows.append(body)
            witness_owners.update((left["owner"], right["owner"]))
        cursor.execute(f"INSERT INTO {table} VALUES(?,?,?,?,?,?,?)", (atom_index + 1, *rb))
    connection.commit()
    connection.close()
    index_path.unlink()

    need(all_strict_pair_count == 187132, "all-component strict pair census")
    need(same_component_pair_count == 154892, "same-component strict pair census")
    need(len(witness_rows) == 32240, "cross-component strict pair census")
    need(cross_source_pairs == Counter({"C19B__C22A": 3668, "C19C__C22A": 28344, "C22A__C22A": 228}), "cross source pair census")
    baseline_rows = [row for row in witness_rows if row["known_228_exact_equal_baseline_occurrence"]]
    incremental_rows = [row for row in witness_rows if row["incremental_beyond_known_228_occurrences"]]
    need(len(baseline_rows) == 228 and len(incremental_rows) == 32012, "baseline/incremental split")
    need(all(row["exact_equal_support_boxes"] for row in baseline_rows), "baseline exact equal")
    need(all(not row["exact_equal_support_boxes"] for row in incremental_rows), "incremental nonidentical overlaps")

    c26_candidate_owners: set[str] = set()
    c26_witness_nodes: dict[str, set[str]] = defaultdict(set)
    c26_rows_on_candidate_owners = 0
    c26_rows_total = 0
    for row in closed_rows(ROOT / FILES["C26"][0]):
        c26_rows_total += 1
        owner = row["owner_member_id"]
        if owner in owners:
            c26_rows_on_candidate_owners += 1
            c26_candidate_owners.add(owner)
            if owner in witness_owners:
                c26_witness_nodes[owner].add(row["node_id"])
    need(c26_rows_total == 691424, "C26 full row census")

    witness_rows.sort(key=lambda row: row["witness_occurrence_id"].encode("ascii"))
    occurrence_count, occurrence_sequence = write_rows(candidate_dir / OCCURRENCE_LEDGER, witness_rows)
    need(occurrence_count == 32240, "occurrence ledger count")

    member_aggregates: dict[tuple[str, str], dict[str, Any]] = {}
    edge_aggregates: dict[tuple[str, str], dict[str, Any]] = {}
    for row in witness_rows:
        owners_pair = tuple(sorted(member["owner_member_id"] for member in row["members"]))
        component_pair = tuple(row["component_pair"])
        for store, key in ((member_aggregates, owners_pair), (edge_aggregates, component_pair)):
            value = store.setdefault(key, {"occurrences": 0, "baseline": 0, "incremental": 0, "source_pairs": Counter(), "member_pairs": set()})
            value["occurrences"] += 1
            value["baseline"] += int(row["known_228_exact_equal_baseline_occurrence"])
            value["incremental"] += int(row["incremental_beyond_known_228_occurrences"])
            value["source_pairs"]["__".join(row["source_pair"])] += 1
            value["member_pairs"].add(owners_pair)

    baseline_edges = {key for key, value in edge_aggregates.items() if value["baseline"]}
    incremental_edges = {key for key, value in edge_aggregates.items() if value["incremental"]}
    need(len(baseline_edges) == 192 and len(incremental_edges) == 14620, "edge baseline/incremental census")
    need(len(baseline_edges & incremental_edges) == 40 and len(incremental_edges - baseline_edges) == 14580, "novel edge census")
    need(len(edge_aggregates) == 14772, "union edge census")

    member_rows = []
    for pair, value in sorted(member_aggregates.items()):
        components = sorted({c15[owner]["component"] for owner in pair})
        need(len(components) == 2, "member pair crosses C15")
        member_rows.append({
            "schema": "cm2.c27.same-chart-strict-volume-totality.v1.member-pair-row.v1",
            "member_pair_id": "same-chart-strict-volume-member-pair:" + object_sha(list(pair)),
            "member_pair": list(pair),
            "component_pair": components,
            "witness_occurrence_count": value["occurrences"],
            "baseline_occurrence_count": value["baseline"],
            "incremental_occurrence_count": value["incremental"],
            "source_pair_census": dict(sorted(value["source_pairs"].items())),
            "formal_credit": 0,
        })
    member_count, member_sequence = write_rows(candidate_dir / MEMBER_PAIR_LEDGER, member_rows)

    edge_rows = []
    for pair, value in sorted(edge_aggregates.items()):
        edge_rows.append({
            "schema": "cm2.c27.same-chart-strict-volume-totality.v1.component-edge-row.v1",
            "component_edge_id": "same-chart-strict-volume-component-edge:" + object_sha(list(pair)),
            "component_pair": list(pair),
            "witness_occurrence_count": value["occurrences"],
            "unique_member_pair_count": len(value["member_pairs"]),
            "baseline_occurrence_count": value["baseline"],
            "incremental_occurrence_count": value["incremental"],
            "source_pair_census": dict(sorted(value["source_pairs"].items())),
            "edge_in_known_228_baseline": pair in baseline_edges,
            "edge_has_incremental_nonidentical_overlap": pair in incremental_edges,
            "edge_novel_beyond_known_228_baseline": pair in incremental_edges - baseline_edges,
            "provisional_only": True,
            "formal_credit": 0,
        })
    edge_count, edge_sequence = write_rows(candidate_dir / COMPONENT_EDGE_LEDGER, edge_rows)

    affected_vertices = sorted({component for edge in edge_aggregates for component in edge})
    dsu = DSU(affected_vertices)
    for left, right in edge_aggregates:
        dsu.union(left, right)
    clusters: dict[str, list[str]] = defaultdict(list)
    for vertex in affected_vertices:
        clusters[dsu.find(vertex)].append(vertex)
    cluster_rows = []
    for members in sorted((sorted(values) for values in clusters.values()), key=lambda values: values[0]):
        cluster_rows.append({
            "schema": "cm2.c27.same-chart-strict-volume-totality.v1.affected-cluster-row.v1",
            "cluster_id": "same-chart-strict-volume-cluster:" + object_sha(members),
            "component_count": len(members),
            "component_ids": members,
            "formal_credit": 0,
        })
    cluster_count, cluster_sequence = write_rows(candidate_dir / CLUSTER_LEDGER, cluster_rows)
    rank_reduction = len(affected_vertices) - cluster_count
    need(rank_reduction > 192, "strict volume extends old rank reduction")

    ledgers = {}
    for filename, row_count, sequence in (
        (OCCURRENCE_LEDGER, occurrence_count, occurrence_sequence),
        (MEMBER_PAIR_LEDGER, member_count, member_sequence),
        (COMPONENT_EDGE_LEDGER, edge_count, edge_sequence),
        (CLUSTER_LEDGER, cluster_count, cluster_sequence),
    ):
        path = candidate_dir / filename
        ledgers[filename] = {"row_count": row_count, "row_sequence_sha256": sequence, "sha256": file_sha(path), "size": path.stat().st_size}

    stable = {
        "primitive_atom_count": len(atoms),
        "candidate_owner_count": len(owners),
        "endpoint_rank_census_t_p_s": endpoint_rank_census,
        "all_component_strict_intersection_pair_count": all_strict_pair_count,
        "same_C15_component_strict_intersection_pair_count": same_component_pair_count,
        "cross_C15_component_strict_intersection_pair_count": len(witness_rows),
        "cross_component_source_pair_census": dict(sorted(cross_source_pairs.items())),
        "known_exact_equal_baseline_occurrence_count": len(baseline_rows),
        "incremental_nonidentical_overlap_occurrence_count": len(incremental_rows),
        "unique_cross_component_member_pair_count": member_count,
        "union_component_edge_count": edge_count,
        "known_baseline_component_edge_count": len(baseline_edges),
        "incremental_component_edge_count": len(incremental_edges),
        "baseline_and_incremental_edge_overlap_count": len(baseline_edges & incremental_edges),
        "novel_component_edge_count_beyond_known_228": len(incremental_edges - baseline_edges),
        "affected_old_C15_component_vertex_count": len(affected_vertices),
        "affected_cluster_count": cluster_count,
        "forced_DSU_rank_reduction": rank_reduction,
        "provisional_component_count_after_strict_volume_edges_only": len(all_c15_components) - rank_reduction,
        "C26_candidate_owner_coverage_count": len(c26_candidate_owners),
        "C26_candidate_owner_gap_count": len(owners - c26_candidate_owners),
        "C26_witness_owner_coverage_count": len(set(c26_witness_nodes)),
        "C26_witness_owner_gap_count": len(witness_owners - set(c26_witness_nodes)),
        "ledgers": ledgers,
    }
    body = {
        "schema": "cm2.c27.same-chart-strict-volume-totality.v1.result.v1",
        "status": "PASS_COMPLETE_STRICT_VOLUME_SUBGATE__32012_INCREMENTAL_NONIDENTICAL_OCCURRENCES__LOWER_DIMENSIONAL_CLOSURE_CONTACTS_REMAIN_SEPARATE__ZERO_CREDIT",
        "seed": seed,
        "seed_usage": "SEED_CONTROLS_FULL_RTREE_INSERTION_ORDER_OVER_ALL_483232_ATOMS",
        "forbidden_inputs": {
            "C27_or_FAMILIES_imported_or_read": False,
            "historical_edge_ledger_used": False,
            "older_same_chart_census_ledger_imported_or_read": False,
        },
        "geometry_scope": {
            "proved_complete": "STRICT_INTERIOR_INTERSECTION_IN_ALL_THREE_PHYSICAL_COORDINATES",
            "strict_volume_witnesses_do_not_depend_on_endpoint_ownership_bits": True,
            "dim1_dim2_closure_contacts_promoted_by_this_probe": False,
            "dim1_dim2_closure_contacts_state": "OPEN_SEPARATE_ENDPOINT_OWNERSHIP_SUBGATE",
        },
        "authority_joins": {
            "C15_full_row_count": c15_rows,
            "C15_component_count": len(all_c15_components),
            "C15_candidate_owner_join_count": len(c15),
            "C15_candidate_owner_join_gap": 0,
            "C25_full_row_count": c25_rows,
            "C25_candidate_owner_join_count": len(c25),
            "C25_candidate_owner_join_gap": 0,
            "C15_C25_component_or_row_binding_mismatch_count": 0,
            "primitive_embedded_component_C15_mismatch_count": 0,
            "C26_full_row_count": c26_rows_total,
            "C26_rows_on_candidate_owners": c26_rows_on_candidate_owners,
            "C26_absence_used_as_negative_geometry_theorem": False,
        },
        "census": stable,
        "semantic_projection_sha256": object_sha(stable),
        "input_pins": {filename: expected for filename, expected in (value for value in FILES.values())},
        "authority": "PROVISIONAL_WITNESS_EVIDENCE_REQUIRING_C27_TO_C29_REBUILD__NOT_C28_MAXIMALITY__NOT_A_SEAL",
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = {**body, "result_sha256": object_sha(body)}
    (candidate_dir / RESULT).write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    result = build(Path(args.candidate_dir).resolve(), args.seed)
    print(canonical({
        "status": result["status"],
        "seed": result["seed"],
        "cross_C15_component_strict_intersection_pair_count": result["census"]["cross_C15_component_strict_intersection_pair_count"],
        "incremental_nonidentical_overlap_occurrence_count": result["census"]["incremental_nonidentical_overlap_occurrence_count"],
        "novel_component_edge_count_beyond_known_228": result["census"]["novel_component_edge_count_beyond_known_228"],
        "semantic_projection_sha256": result["semantic_projection_sha256"],
        "result_sha256": result["result_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
