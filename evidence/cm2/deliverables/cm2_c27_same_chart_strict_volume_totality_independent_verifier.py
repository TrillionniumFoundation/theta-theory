#!/usr/bin/env python3
"""Independent sweep-line verifier for SAME_CHART strict-volume witnesses.

This verifier reconstructs all six primitive sources, chart lineage, C15 and
C25 joins itself.  It does not import the producer and does not use SQLite or
an R-tree.  Completeness is checked by a strict-t sweep with an active set,
followed by exact p/s rank comparisons.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import cmp_to_key
import gzip
import hashlib
import heapq
import json
import math
from pathlib import Path
import random
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_c27_same_chart_strict_volume_totality_v1"
RESULT = PREFIX + "_result.json"
OCCURRENCES = PREFIX + "_witness_occurrences.jsonl.gz"
MEMBERS = PREFIX + "_member_pairs.jsonl.gz"
EDGES = PREFIX + "_component_edges.jsonl.gz"
CLUSTERS = PREFIX + "_affected_clusters.jsonl.gz"

FILES = {
    "C15": ("cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz", "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    "C25": ("cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz", "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6"),
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
COUNTS = {"C19A": 5596, "C19B": 12232, "C19C": 33344, "C20A": 126468, "C22A": 295340, "C23A": 10252}
KERNEL = {"C19A": "C19A", "C19B": "C19B", "C19C": "C19C", "C20A": "C20A", "C22A": "C22B", "C23A": "C23B"}


class Reject(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(2 << 20):
            h.update(block)
    return h.hexdigest()


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            require(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            raw = line[:-1]
            value = json.loads(raw)
            require(type(value) is dict and encode(value) == raw, f"canonical:{path.name}:{ordinal}")
            body = dict(value)
            claimed = body.pop("row_sha256", None)
            require(claimed == digest(body), f"row hash:{path.name}:{ordinal}")
            yield value


Number = tuple[Any, ...]


def rational(text: str) -> Number:
    return ("r", Fraction(text))


def radical(text: str, sign: int) -> Number:
    q = Fraction(text)
    require(q >= 0 and sign in {-1, 1}, "radical domain")
    a, b = math.isqrt(q.numerator), math.isqrt(q.denominator)
    if a * a == q.numerator and b * b == q.denominator:
        return ("r", Fraction(sign * a, b))
    return ("s", sign, q)


def order(a: Number, b: Number) -> int:
    if a == b:
        return 0
    if a[0] == b[0] == "r":
        return -1 if a[1] < b[1] else 1
    if a[0] == b[0] == "s":
        sa, qa, sb, qb = a[1], a[2], b[1], b[2]
        if sa != sb:
            return -1 if sa < sb else 1
        direction = -1 if qa < qb else 1
        return direction if sa == 1 else -direction
    if a[0] == "r":
        x, sign, q = a[1], b[1], b[2]
        if sign == 1:
            if x < 0:
                return -1
            d = x * x - q
            return 0 if d == 0 else (-1 if d < 0 else 1)
        if x >= 0:
            return 1
        d = x * x - q
        return 0 if d == 0 else (-1 if d > 0 else 1)
    return -order(b, a)


def wire(number: Number) -> dict[str, Any]:
    def qtext(q: Fraction) -> str:
        return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"
    if number[0] == "r":
        return {"kind": "Q", "value": qtext(number[1])}
    return {"kind": "SIGNED_SQRT_Q", "radicand": qtext(number[2]), "sign": number[1]}


def from_wire(value: dict[str, Any]) -> Number:
    if value.get("kind") == "Q":
        return rational(value["value"])
    require(value.get("kind") == "SIGNED_SQRT_Q", "known endpoint wire")
    return radical(value["radicand"], value["sign"])


def bounds_for(source: str, ast: dict[str, Any]) -> tuple[Number, ...]:
    raw = ast["bounds"]
    require(type(raw) is list and len(raw) == 6, "six bounds")
    if source != "C23A":
        output = tuple(rational(x) for x in raw)
    else:
        sign = ast["physical_t_sign"]
        t0, t1 = (radical(raw[0], 1), radical(raw[1], 1)) if sign == 1 else (radical(raw[1], -1), radical(raw[0], -1))
        output = (t0, t1, rational(raw[2]), rational(raw[3]), rational(raw[4]), rational(raw[5]))
    require(all(order(output[2 * i], output[2 * i + 1]) < 0 for i in range(3)), "primitive positive widths")
    return output


def chart_authorities() -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]:
    doc = json.loads((ROOT / FILES["R179"][0]).read_bytes())
    r179 = {row[0]: row[3] for row in doc["result"]["retained_3d_child_rows"]}
    doc = json.loads((ROOT / FILES["R234"][0]).read_bytes())
    r234 = {row["materialized_row_id"]: row["chart"] for row in doc["result"]["resolved_descendant_rows"]}
    doc = json.loads((ROOT / FILES["R236"][0]).read_bytes())
    r236 = {row["crossing_dependency_discharge_row_id"]: row["local_return_signature"]["source_chart"] for row in doc["result"]["crossing_dependency_discharge_rows"]}
    c5 = {}
    for row in rows(ROOT / FILES["C5"][0]):
        semantic = row["semantic_classification"]
        if semantic["classification"] == "EMPTY_GRAPH":
            c5[row["row_sha256"]] = semantic["kernel_parameters"]["source_chart"]
    require(len(c5) == 33344, "C5 chart count")
    return r179, r234, r236, c5


def derive_chart(source: str, row: dict[str, Any], maps: tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]) -> str:
    a, b, c, d = maps
    if source == "C19A":
        return a[row["construction_certificate"]["retained_child_row_id"]]
    if source == "C19B":
        key = row["construction_certificate"]["source_partition_row_id"]
        return b[key] if key.startswith("round234-resolved:") else c[key]
    if source == "C19C":
        return d[row["construction_certificate"]["C5_row_sha256"]]
    if source in {"C20A", "C22A"}:
        return row["support_ast"]["coordinate_chart"]
    return row["support_ast"]["recharted_target_chart"]


def source_atom_id(source: str, row: dict[str, Any]) -> str:
    if source == "C22A":
        return row["predicate_cell_row_id"]
    if source == "C23A":
        return row["R292_refinement_cell_id"]
    return f"{source.lower()}-support-atom:{row['row_sha256']}"


def reconstruct(seed: int) -> tuple[list[dict[str, Any]], set[tuple[str, str]], dict[str, Any]]:
    require(type(seed) is int and seed > 0, "verification seed")
    for role, (filename, expected) in FILES.items():
        require(hash_file(ROOT / filename) == expected, "input pin:" + role)
    maps = chart_authorities()
    atoms = []
    endpoints = [set(), set(), set()]
    owner_sources: dict[str, set[str]] = defaultdict(set)
    source_count = Counter()
    for source in COUNTS:
        for row in rows(ROOT / FILES[source][0]):
            source_count[source] += 1
            owner = row.get("member_id") or row["owner_member_id"]
            embedded = row.get("fresh_component_id") or row["owner_fresh_component_id"]
            box = bounds_for(source, row["support_ast"])
            for axis in range(3):
                endpoints[axis].update(box[2 * axis:2 * axis + 2])
            owner_sources[owner].add(source)
            atoms.append({"id": source_atom_id(source, row), "owner": owner, "embedded": embedded, "source": source, "source_row": row["row_sha256"], "chart": derive_chart(source, row, maps), "bounds": box, "kind": row["support_ast"]["kind"]})
        require(source_count[source] == COUNTS[source], "source count:" + source)
    require(len(atoms) == 483232 and len(owner_sources) == 482380, "atom owner totals")
    atoms.sort(key=lambda x: x["id"])
    owners = set(owner_sources)
    c15 = {}
    all_components = set()
    for row in rows(ROOT / FILES["C15"][0]):
        all_components.add(row["fresh_component_id"])
        member = row["registry_member_id"]
        if member in owners:
            require(member not in c15, "C15 unique")
            c15[member] = (row["fresh_component_id"], row["row_sha256"])
    require(set(c15) == owners and len(all_components) == 57876, "C15 full join")
    c25 = {}
    for row in rows(ROOT / FILES["C25"][0]):
        member = row["member_id"]
        if member in owners:
            bind = row["source_bindings"]
            require(member not in c25, "C25 unique")
            c25[member] = (row["fresh_component_id"], row["row_sha256"], bind["support_kernel"], bind["C15_member_row_sha256"])
    require(set(c25) == owners, "C25 full join")
    for atom in atoms:
        owner = atom["owner"]
        expected = {KERNEL[source] for source in owner_sources[owner]}
        require(len(expected) == 1, "single owner kernel")
        require(atom["embedded"] == c15[owner][0] == c25[owner][0], "component binding")
        require(c15[owner][1] == c25[owner][3] and c25[owner][2] == next(iter(expected)), "C25 exact binding")
        atom["component"] = c15[owner][0]
        atom["c15"] = c15[owner][1]
        atom["c25"] = c25[owner][1]
        atom["c25_kernel"] = c25[owner][2]
    rank_maps = []
    for values in endpoints:
        ordered = sorted(values, key=cmp_to_key(order))
        rank_maps.append({value: index + 1 for index, value in enumerate(ordered)})
    require([len(x) for x in rank_maps] == [6433, 1201, 257], "rank totals")
    for atom in atoms:
        ranked = []
        for axis in range(3):
            ranked.extend([rank_maps[axis][atom["bounds"][2 * axis]], rank_maps[axis][atom["bounds"][2 * axis + 1]]])
        atom["rank"] = tuple(ranked)

    rng = random.Random(seed)
    tie = [rng.getrandbits(64) for _ in atoms]
    traversal = sorted(range(len(atoms)), key=lambda i: (atoms[i]["chart"], atoms[i]["rank"][0], tie[i], atoms[i]["id"]))
    expected: set[tuple[str, str]] = set()
    all_pairs = 0
    same_pairs = 0
    source_pairs = Counter()
    for chart in ("G:E", "G:N", "G:S", "G:W"):
        active: set[int] = set()
        expiry: list[tuple[int, int]] = []
        for index in (i for i in traversal if atoms[i]["chart"] == chart):
            current = atoms[index]
            rb = current["rank"]
            while expiry and expiry[0][0] <= rb[0]:
                _, old = heapq.heappop(expiry)
                active.discard(old)
            for old in active:
                other = atoms[old]
                ob = other["rank"]
                if ob[2] < rb[3] and ob[3] > rb[2] and ob[4] < rb[5] and ob[5] > rb[4]:
                    all_pairs += 1
                    if other["component"] == current["component"]:
                        same_pairs += 1
                    else:
                        pair = tuple(sorted((other["id"], current["id"])))
                        require(pair not in expected, "unique sweep pair")
                        expected.add(pair)
                        source_pairs["__".join(sorted((other["source"], current["source"])))] += 1
            active.add(index)
            heapq.heappush(expiry, (rb[1], index))
    require(all_pairs == 187132 and same_pairs == 154892 and len(expected) == 32240, "sweep census")
    require(source_pairs == Counter({"C19B__C22A": 3668, "C19C__C22A": 28344, "C22A__C22A": 228}), "sweep source split")
    return atoms, expected, {"all": all_pairs, "same": same_pairs, "source_pairs": dict(sorted(source_pairs.items())), "component_count": len(all_components)}


def verify(candidate_dir: Path, output: Path, seed: int) -> dict[str, Any]:
    raw = (candidate_dir / RESULT).read_bytes()
    require(raw.endswith(b"\n"), "result newline")
    result = json.loads(raw)
    require(encode(result) + b"\n" == raw, "result canonical")
    result_body = dict(result)
    claimed = result_body.pop("result_sha256", None)
    require(claimed == digest(result_body), "result closure")
    require(result["forbidden_inputs"] == {"C27_or_FAMILIES_imported_or_read": False, "historical_edge_ledger_used": False, "older_same_chart_census_ledger_imported_or_read": False}, "forbidden-input declaration")
    for filename, meta in result["census"]["ledgers"].items():
        require(hash_file(candidate_dir / filename) == meta["sha256"], "ledger file pin:" + filename)

    atoms, expected_pairs, sweep = reconstruct(seed)
    by_id = {atom["id"]: atom for atom in atoms}
    observed_pairs = set()
    member_counts = Counter()
    edge_counts = Counter()
    edge_baseline = Counter()
    edge_incremental = Counter()
    baseline = incremental = 0
    for row in rows(candidate_dir / OCCURRENCES):
        members = row["members"]
        require(type(members) is list and len(members) == 2, "two witness members")
        pair = tuple(sorted(member["atom_id"] for member in members))
        require(pair not in observed_pairs and pair in expected_pairs, "occurrence exact pair")
        observed_pairs.add(pair)
        direct = [by_id[value] for value in pair]
        direct.sort(key=lambda x: x["id"])
        members.sort(key=lambda x: x["atom_id"])
        require(row["chart"] == direct[0]["chart"] == direct[1]["chart"], "witness chart")
        require(row["source_pair"] == sorted((direct[0]["source"], direct[1]["source"])), "witness sources")
        for claimed_member, atom in zip(members, direct):
            require(claimed_member["source_kernel"] == atom["source"] and claimed_member["source_row_sha256"] == atom["source_row"], "source binding")
            require(claimed_member["owner_member_id"] == atom["owner"] and claimed_member["C15_component_id"] == atom["component"], "owner component")
            require(claimed_member["C15_member_row_sha256"] == atom["c15"] and claimed_member["C25_member_row_sha256"] == atom["c25"], "C15/C25 rows")
            require(claimed_member["C25_support_kernel"] == atom["c25_kernel"] and claimed_member["support_kind"] == atom["kind"], "kernel kind")
            require(tuple(from_wire(x) for x in claimed_member["physical_bounds"]) == atom["bounds"], "exact physical bounds")
        intersection = []
        for axis in range(3):
            lower = direct[0]["bounds"][2 * axis] if order(direct[0]["bounds"][2 * axis], direct[1]["bounds"][2 * axis]) >= 0 else direct[1]["bounds"][2 * axis]
            upper = direct[0]["bounds"][2 * axis + 1] if order(direct[0]["bounds"][2 * axis + 1], direct[1]["bounds"][2 * axis + 1]) <= 0 else direct[1]["bounds"][2 * axis + 1]
            require(order(lower, upper) < 0, "strict exact intersection")
            intersection.extend([lower, upper])
        require(tuple(from_wire(x) for x in row["intersection_bounds"]) == tuple(intersection), "intersection bounds")
        exact = direct[0]["bounds"] == direct[1]["bounds"]
        is_baseline = row["source_pair"] == ["C22A", "C22A"] and exact
        require(row["exact_equal_support_boxes"] is exact and row["known_228_exact_equal_baseline_occurrence"] is is_baseline, "baseline classification")
        require(row["incremental_beyond_known_228_occurrences"] is (not is_baseline), "incremental classification")
        require(row["endpoint_ownership_bits_used"] is False and row["intersection_relation"] == "STRICT_POSITIVE_VOLUME_INTERIOR_INTERSECTION", "strict relation")
        baseline += int(is_baseline)
        incremental += int(not is_baseline)
        owner_pair = tuple(sorted(atom["owner"] for atom in direct))
        edge = tuple(sorted(atom["component"] for atom in direct))
        require(len(set(edge)) == 2, "cross component witness")
        member_counts[owner_pair] += 1
        edge_counts[edge] += 1
        edge_baseline[edge] += int(is_baseline)
        edge_incremental[edge] += int(not is_baseline)
    require(observed_pairs == expected_pairs and baseline == 228 and incremental == 32012, "complete occurrence ledger")

    observed_member_pairs = set()
    for row in rows(candidate_dir / MEMBERS):
        pair = tuple(row["member_pair"])
        require(pair in member_counts and pair not in observed_member_pairs, "member aggregate key")
        observed_member_pairs.add(pair)
        require(row["witness_occurrence_count"] == member_counts[pair], "member aggregate count")
    require(observed_member_pairs == set(member_counts), "member aggregate totality")

    observed_edges = set()
    for row in rows(candidate_dir / EDGES):
        edge = tuple(row["component_pair"])
        require(edge in edge_counts and edge not in observed_edges, "edge aggregate key")
        observed_edges.add(edge)
        require(row["witness_occurrence_count"] == edge_counts[edge], "edge occurrence count")
        require(row["baseline_occurrence_count"] == edge_baseline[edge] and row["incremental_occurrence_count"] == edge_incremental[edge], "edge split")
        require(row["edge_in_known_228_baseline"] is bool(edge_baseline[edge]), "edge baseline flag")
        require(row["edge_has_incremental_nonidentical_overlap"] is bool(edge_incremental[edge]), "edge incremental flag")
        require(row["edge_novel_beyond_known_228_baseline"] is (bool(edge_incremental[edge]) and not bool(edge_baseline[edge])), "edge novel flag")
    require(observed_edges == set(edge_counts) and len(observed_edges) == 14772, "edge totality")
    base_edges = {edge for edge in edge_counts if edge_baseline[edge]}
    added_edges = {edge for edge in edge_counts if edge_incremental[edge]}
    require((len(base_edges), len(added_edges), len(base_edges & added_edges), len(added_edges - base_edges)) == (192, 14620, 40, 14580), "edge census")

    adjacency: dict[str, set[str]] = defaultdict(set)
    for left, right in edge_counts:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(adjacency)
    expected_clusters: set[tuple[str, ...]] = set()
    while unseen:
        start = min(unseen)
        stack = [start]
        seen = {start}
        unseen.remove(start)
        while stack:
            here = stack.pop()
            for nxt in adjacency[here]:
                if nxt not in seen:
                    seen.add(nxt)
                    unseen.remove(nxt)
                    stack.append(nxt)
        expected_clusters.add(tuple(sorted(seen)))
    observed_clusters = set()
    for row in rows(candidate_dir / CLUSTERS):
        cluster = tuple(row["component_ids"])
        require(cluster not in observed_clusters and cluster in expected_clusters, "cluster exact")
        require(row["component_count"] == len(cluster), "cluster size")
        observed_clusters.add(cluster)
    require(observed_clusters == expected_clusters, "cluster totality")

    census = result["census"]
    require(census["all_component_strict_intersection_pair_count"] == sweep["all"], "result all census")
    require(census["same_C15_component_strict_intersection_pair_count"] == sweep["same"], "result same census")
    require(census["cross_C15_component_strict_intersection_pair_count"] == len(expected_pairs), "result cross census")
    require(census["cross_component_source_pair_census"] == sweep["source_pairs"], "result source census")
    require(census["unique_cross_component_member_pair_count"] == len(member_counts), "result member census")
    require(census["union_component_edge_count"] == len(edge_counts), "result edge census")
    require(census["affected_old_C15_component_vertex_count"] == len(adjacency), "result vertex census")
    require(census["affected_cluster_count"] == len(expected_clusters), "result cluster census")
    require(census["forced_DSU_rank_reduction"] == len(adjacency) - len(expected_clusters), "result rank")
    stable = dict(census)
    require(result["semantic_projection_sha256"] == digest(stable), "semantic projection")
    require(result["formal_credit"] == 0 and result["C27_C28_C29"] == "REJECT_AND_REBUILD_REQUIRED", "zero-credit governance")

    body = {
        "schema": "cm2.c27.same-chart-strict-volume-totality.v1.independent-verification.v1",
        "status": "PASS_INDEPENDENT_DIRECT_SOURCE_SWEEP_EXACTLY_MATCHES_ALL_32240_CROSS_COMPONENT_STRICT_VOLUME_OCCURRENCES",
        "verification_seed": seed,
        "seed_usage": "SEED_CONTROLS_TIE_ORDER_WITHIN_EQUAL_CHART_AND_T_LOWER_SWEEP_KEYS",
        "candidate_result_sha256": result["result_sha256"],
        "candidate_semantic_projection_sha256": result["semantic_projection_sha256"],
        "all_component_strict_pair_count": sweep["all"],
        "same_component_strict_pair_count": sweep["same"],
        "cross_component_strict_pair_count": len(expected_pairs),
        "incremental_nonidentical_occurrence_count": incremental,
        "unique_member_pair_count": len(member_counts),
        "component_edge_count": len(edge_counts),
        "novel_component_edge_count_beyond_known_228": len(added_edges - base_edges),
        "affected_vertex_count": len(adjacency),
        "affected_cluster_count": len(expected_clusters),
        "forced_rank_reduction": len(adjacency) - len(expected_clusters),
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
    }
    verification = {**body, "verification_sha256": digest(body)}
    output.write_bytes(encode(verification) + b"\n")
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    value = verify(Path(args.candidate_dir).resolve(), Path(args.output).resolve(), args.seed)
    print(encode(value).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
