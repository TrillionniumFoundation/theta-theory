#!/usr/bin/env python3
"""Primitive-only SAME_CHART lower-dimensional exact-contact producer.

The candidate universe is rebuilt from the six normalized support kernels,
C15, C25, C26, primitive chart lineage, and the cold-replayed published C19C
v3 endpoint authority.  It never reads C27 FAMILIES, a historical edge
universe, or an older same-chart candidate ledger.

All 5,783,708 closure contacts are enumerated.  The complete set is committed
by canonical pair-digest sequences per exact dimension/source/component bucket.
All 76,000 endpoint-dependent C19C x C19C contacts are additionally
materialized row by row.  The other five kernels are proved fully open, so a
zero-width contact involving any of them is uniformly rejected.
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
import sqlite3
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_c27_same_chart_lower_dimensional_exact_contact_v1"
BUCKET_LEDGER = PREFIX + "_complete_candidate_bucket_commitments.jsonl.gz"
C19C_LEDGER = PREFIX + "_c19c_endpoint_dependent_contacts.jsonl.gz"
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
    "V3_MANIFEST": ("cm2_c19c_endpoint_ownership_v3_manifest.sha256", "14643e303aee7a3bac27342204ee92f2420ae855a5df66916307680721c82929"),
    "V3_RECEIPT": ("cm2_c19c_endpoint_ownership_v3_terminal_receipt.json", "c620034783676f20d99e3f9a600cfe9b3e22a48129cd2f0555479d5b6c25e63b"),
    "V3_AUTHORITY": ("cm2_c19c_endpoint_ownership_v3_authority_ledger.jsonl.gz", "77b220d803b64066a09a0172e06f53f0ddc7a229d208cb7248c2293f493f3166"),
    "V3_COLD_MANIFEST": ("cm2_c19c_endpoint_ownership_v3_postpublication_cold_replay_manifest.sha256", "76af00fbb2c69bf2aa4f01a68a3da33fffd947d325f27e78b68bcf1ccc4c0cfb"),
    "V3_COLD_RECEIPT": ("cm2_c19c_endpoint_ownership_v3_postpublication_cold_replay_receipt.json", "17236dac0b9cf04d0d4e50bba1072fc90b2e87f732cdfa6d802f411facc6930d"),
}
COUNTS = {"C19A": 5596, "C19B": 12232, "C19C": 33344, "C20A": 126468, "C22A": 295340, "C23A": 10252}
KERNEL = {"C19A": "C19A", "C19B": "C19B", "C19C": "C19C", "C20A": "C20A", "C22A": "C22B", "C23A": "C23B"}
OPEN_KINDS = {
    "C19A": "OPEN_RATIONAL_BOX",
    "C19B": "OPEN_RATIONAL_BOX",
    "C20A": "OPEN_RATIONAL_BOX",
    "C22A": "OPEN_RATIONAL_BOX",
    "C23A": "T2PS_BRANCH_OPEN_RATIONAL_BOX",
}
AXES = ("t", "p", "s")
BIT_NAMES = (
    "t_lower_closed", "t_upper_closed", "p_lower_closed",
    "p_upper_closed", "s_lower_closed", "s_upper_closed",
)
CHARTS = ("G:E", "G:N", "G:S", "G:W")
EXPECTED_DIMENSION_COUNTS = {0: 807_104, 1: 2_611_136, 2: 2_365_468, 3: 187_132}
EXPECTED_RELATION_COUNTS = {
    (0, "CROSS_C15_COMPONENT"): 431_473,
    (0, "SAME_C15_COMPONENT"): 375_631,
    (1, "CROSS_C15_COMPONENT"): 1_239_209,
    (1, "SAME_C15_COMPONENT"): 1_371_927,
    (2, "CROSS_C15_COMPONENT"): 927_984,
    (2, "SAME_C15_COMPONENT"): 1_437_484,
    (3, "CROSS_C15_COMPONENT"): 32_240,
    (3, "SAME_C15_COMPONENT"): 154_892,
}


class Failure(RuntimeError):
    pass


def need(flag: bool, label: str) -> None:
    if type(flag) is not bool or not flag:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
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
            need(claimed == object_sha(body), f"closure:{path.name}:{ordinal}")
            yield row


def closed_json(path: Path, closure: str) -> dict[str, Any]:
    raw = path.read_bytes()
    row = json.loads(raw)
    need(canonical(row) == raw, "canonical JSON:" + path.name)
    body = dict(row)
    claimed = body.pop(closure, None)
    need(claimed == object_sha(body), "JSON closure:" + path.name)
    return row


def qwire(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


# Endpoint is rational Q or a signed square-root of Q.
Endpoint = tuple[Any, ...]


def q_endpoint(text: str) -> Endpoint:
    return (0, Fraction(text))


def sqrt_endpoint(text: str, sign: int) -> Endpoint:
    value = Fraction(text)
    need(value >= 0 and sign in {-1, 1}, "signed sqrt domain")
    a, b = math.isqrt(value.numerator), math.isqrt(value.denominator)
    if a * a == value.numerator and b * b == value.denominator:
        return (0, Fraction(sign * a, b))
    return (1, value, sign)


def compare_endpoint(left: Endpoint, right: Endpoint) -> int:
    if left == right:
        return 0
    if left[0] == right[0] == 0:
        return -1 if left[1] < right[1] else 1
    if left[0] == right[0] == 1:
        lq, ls, rq, rs = left[1], left[2], right[1], right[2]
        if ls != rs:
            return -1 if ls < rs else 1
        direction = -1 if lq < rq else 1
        return direction if ls == 1 else -direction
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


def endpoint_wire(value: Endpoint) -> dict[str, Any]:
    if value[0] == 0:
        return {"kind": "Q", "value": qwire(value[1])}
    return {"kind": "SIGNED_SQRT_Q", "radicand": qwire(value[1]), "sign": value[2]}


def normalized_bounds(source: str, support: dict[str, Any]) -> tuple[Endpoint, ...]:
    raw = support.get("bounds")
    need(type(raw) is list and len(raw) == 6 and all(type(x) is str for x in raw), "six exact bounds:" + source)
    if source != "C23A":
        need(support.get("coordinates") == ["t", "p", "s"], "physical coordinates:" + source)
        bounds = tuple(q_endpoint(value) for value in raw)
    else:
        need(support.get("kind") == "T2PS_BRANCH_OPEN_RATIONAL_BOX", "C23 support kind")
        sign = support.get("physical_t_sign")
        need(sign in {-1, 1}, "C23 physical sign")
        if sign == 1:
            t0, t1 = sqrt_endpoint(raw[0], 1), sqrt_endpoint(raw[1], 1)
        else:
            t0, t1 = sqrt_endpoint(raw[1], -1), sqrt_endpoint(raw[0], -1)
        bounds = (t0, t1, q_endpoint(raw[2]), q_endpoint(raw[3]), q_endpoint(raw[4]), q_endpoint(raw[5]))
    need(all(compare_endpoint(bounds[2 * axis], bounds[2 * axis + 1]) < 0 for axis in range(3)), "positive primitive widths:" + source)
    return bounds


def load_chart_maps() -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]:
    r179_doc = json.loads((ROOT / FILES["R179"][0]).read_bytes())
    r179 = {row[0]: row[3] for row in r179_doc["result"]["retained_3d_child_rows"]}
    r234_doc = json.loads((ROOT / FILES["R234"][0]).read_bytes())
    r234 = {row["materialized_row_id"]: row["chart"] for row in r234_doc["result"]["resolved_descendant_rows"]}
    r236_doc = json.loads((ROOT / FILES["R236"][0]).read_bytes())
    r236 = {row["crossing_dependency_discharge_row_id"]: row["local_return_signature"]["source_chart"] for row in r236_doc["result"]["crossing_dependency_discharge_rows"]}
    c5 = {}
    for row in closed_rows(ROOT / FILES["C5"][0]):
        semantic = row["semantic_classification"]
        if semantic["classification"] == "EMPTY_GRAPH":
            c5[row["row_sha256"]] = semantic["kernel_parameters"]["source_chart"]
    need(len(c5) == 33_344, "C5 empty graph chart census")
    return r179, r234, r236, c5


def chart_for(source: str, row: dict[str, Any], maps: tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]) -> str:
    r179, r234, r236, c5 = maps
    if source == "C19A":
        chart = r179[row["construction_certificate"]["retained_child_row_id"]]
    elif source == "C19B":
        key = row["construction_certificate"]["source_partition_row_id"]
        chart = r234[key] if key.startswith("round234-resolved:") else r236[key]
    elif source == "C19C":
        chart = c5[row["construction_certificate"]["C5_row_sha256"]]
    elif source in {"C20A", "C22A"}:
        chart = row["support_ast"]["coordinate_chart"]
    else:
        need(source == "C23A", "known source")
        chart = row["support_ast"]["recharted_target_chart"]
    need(chart in CHARTS, "four-chart atom")
    return chart


def atom_id_for(source: str, row: dict[str, Any]) -> str:
    if source == "C22A":
        return row["predicate_cell_row_id"]
    if source == "C23A":
        return row["R292_refinement_cell_id"]
    return f"{source.lower()}-support-atom:{row['row_sha256']}"


def write_rows(path: Path, bodies: Iterable[dict[str, Any]]) -> dict[str, Any]:
    count = 0
    sequence = hashlib.sha256()
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as packed:
            for ordinal, body in enumerate(bodies):
                row = {**body, "ordinal": ordinal}
                row["row_sha256"] = object_sha(row)
                sequence.update(bytes.fromhex(row["row_sha256"]))
                packed.write(canonical(row) + b"\n")
                count += 1
    return {
        "filename": path.name,
        "row_count": count,
        "row_sequence_sha256": sequence.hexdigest(),
        "sha256": file_sha(path),
        "size": path.stat().st_size,
    }


def pair_digest(left: str, right: str) -> bytes:
    a, b = sorted((left, right))
    return hashlib.sha256(canonical([a, b])).digest()


def endpoint_bit(atom: dict[str, Any], axis: int, coordinate: Endpoint) -> tuple[str, bool]:
    lower, upper = atom["bounds"][2 * axis:2 * axis + 2]
    if compare_endpoint(coordinate, lower) == 0:
        return "LOWER", atom["bits"][2 * axis]
    need(compare_endpoint(coordinate, upper) == 0, "zero contact lies on endpoint")
    return "UPPER", atom["bits"][2 * axis + 1]


def build(candidate_dir: Path, seed: int) -> dict[str, Any]:
    need(type(seed) is int and seed > 0, "positive execution seed")
    need(not candidate_dir.exists(), "new candidate directory")
    candidate_dir.mkdir(parents=True)
    for role, (filename, pin) in FILES.items():
        need(file_sha(ROOT / filename) == pin, "input pin:" + role)
    cold = closed_json(ROOT / FILES["V3_COLD_RECEIPT"][0], "receipt_sha256")
    need(cold["status"] == "PASS_COLD_POSTPUBLICATION_REPLAY_PRE_POST_SHA_STAT_IDENTICAL__ZERO_FORMAL_CREDIT", "cold authority status")
    need(cold["pre_post_sha256_identical"] is True and cold["pre_post_stat_identical"] is True, "cold pre/post identity")
    need(cold["formal_credit"] == 0 and cold["C27_C28_C29"] == "UNAUTHORIZED_PENDING_REBUILD", "cold nonpromotion")

    authority: dict[str, dict[str, Any]] = {}
    for row in closed_rows(ROOT / FILES["V3_AUTHORITY"][0]):
        need(row["member_id"] not in authority, "v3 authority member uniqueness")
        # Canonical JSON sorts object keys, so this authority is a named-bit
        # map; insertion order is intentionally not semantic.
        need(set(row["endpoint_inclusion_bits"]) == set(BIT_NAMES), "v3 exact bit names")
        need(all(type(row["endpoint_inclusion_bits"][name]) is bool for name in BIT_NAMES), "v3 bool bits")
        authority[row["member_id"]] = row
    need(len(authority) == 33_344, "v3 authority census")

    maps = load_chart_maps()
    atoms: list[dict[str, Any]] = []
    owner_sources: dict[str, set[str]] = defaultdict(set)
    endpoints = [set(), set(), set()]
    source_counts = Counter()
    atom_ids: set[str] = set()
    for source in COUNTS:
        for row in closed_rows(ROOT / FILES[source][0]):
            source_counts[source] += 1
            owner = row.get("member_id") or row["owner_member_id"]
            component = row.get("fresh_component_id") or row["owner_fresh_component_id"]
            atom_id = atom_id_for(source, row)
            need(atom_id not in atom_ids, "unique primitive atom id")
            atom_ids.add(atom_id)
            bounds = normalized_bounds(source, row["support_ast"])
            chart = chart_for(source, row, maps)
            if source == "C19C":
                auth = authority[owner]
                need(auth["C19C_row_sha256"] == row["row_sha256"] and auth["chart"] == chart, "C19C v3 row/chart binding")
                need(auth["bounds"] == row["support_ast"]["bounds"], "C19C v3 bounds binding")
                bits = tuple(auth["endpoint_inclusion_bits"][name] for name in BIT_NAMES)
                authority_row_sha256 = auth["row_sha256"]
            else:
                need(row["support_ast"]["kind"] == OPEN_KINDS[source], "fully open primitive kernel:" + source)
                bits = (False,) * 6
                authority_row_sha256 = None
            owner_sources[owner].add(source)
            for axis in range(3):
                endpoints[axis].update(bounds[2 * axis:2 * axis + 2])
            atoms.append({
                "atom_id": atom_id,
                "source": source,
                "source_row_sha256": row["row_sha256"],
                "owner": owner,
                "embedded_component": component,
                "chart": chart,
                "bounds": bounds,
                "support_kind": row["support_ast"]["kind"],
                "bits": bits,
                "authority_row_sha256": authority_row_sha256,
            })
        need(source_counts[source] == COUNTS[source], "primitive source census:" + source)
    need(len(atoms) == 483_232 and len(owner_sources) == 482_380, "primitive atom/owner census")
    atoms.sort(key=lambda atom: atom["atom_id"])
    owners = set(owner_sources)

    c15: dict[str, tuple[str, str]] = {}
    all_components: set[str] = set()
    c15_rows = 0
    for row in closed_rows(ROOT / FILES["C15"][0]):
        c15_rows += 1
        all_components.add(row["fresh_component_id"])
        member = row["registry_member_id"]
        if member in owners:
            need(member not in c15, "C15 unique owner")
            c15[member] = (row["fresh_component_id"], row["row_sha256"])
    need(c15_rows == 502_204 and len(all_components) == 57_876 and set(c15) == owners, "complete C15 join")
    c25: dict[str, tuple[str, str, str, str]] = {}
    c25_rows = 0
    for row in closed_rows(ROOT / FILES["C25"][0]):
        c25_rows += 1
        member = row["member_id"]
        if member in owners:
            bind = row["source_bindings"]
            need(member not in c25, "C25 unique owner")
            c25[member] = (row["fresh_component_id"], row["row_sha256"], bind["support_kernel"], bind["C15_member_row_sha256"])
    need(c25_rows == 502_204 and set(c25) == owners, "complete C25 join")
    for atom in atoms:
        owner = atom["owner"]
        expected_kernel = {KERNEL[source] for source in owner_sources[owner]}
        need(len(expected_kernel) == 1, "one C25 support kernel per owner")
        need(atom["embedded_component"] == c15[owner][0] == c25[owner][0], "primitive/C15/C25 component")
        need(c15[owner][1] == c25[owner][3] and c25[owner][2] == next(iter(expected_kernel)), "C25 exact source binding")
        atom["component"] = c15[owner][0]
        atom["C15_row_sha256"] = c15[owner][1]
        atom["C25_row_sha256"] = c25[owner][1]
        atom["C25_support_kernel"] = c25[owner][2]

    rank_maps: list[dict[Endpoint, int]] = []
    for values in endpoints:
        ordered = sorted(values, key=cmp_to_key(compare_endpoint))
        need(all(compare_endpoint(a, b) < 0 for a, b in zip(ordered, ordered[1:])), "strict endpoint ranking")
        rank_maps.append({value: ordinal + 1 for ordinal, value in enumerate(ordered)})
    need([len(mapping) for mapping in rank_maps] == [6433, 1201, 257], "endpoint rank census")
    for atom in atoms:
        ranked = []
        for axis in range(3):
            ranked.extend((rank_maps[axis][atom["bounds"][2 * axis]], rank_maps[axis][atom["bounds"][2 * axis + 1]]))
        atom["rank"] = tuple(ranked)

    db_path = candidate_dir / "temporary-contact-index.sqlite"
    db = sqlite3.connect(db_path)
    db.execute("PRAGMA journal_mode=OFF")
    db.execute("PRAGMA synchronous=OFF")
    db.execute("PRAGMA temp_store=MEMORY")
    tables = {"G:E": "box_e", "G:N": "box_n", "G:S": "box_s", "G:W": "box_w"}
    for table in tables.values():
        db.execute(f"CREATE VIRTUAL TABLE {table} USING rtree_i32(id,t0,t1,p0,p1,s0,s1)")
    query = "SELECT id FROM {table} WHERE t0<=? AND t1>=? AND p0<=? AND p1>=? AND s0<=? AND s1>=?"
    insertion_order = list(range(len(atoms)))
    random.Random(seed).shuffle(insertion_order)
    cursor = db.cursor()
    dimension_counts = Counter()
    relation_counts = Counter()
    source_dimension_counts = Counter()
    bucket_digests: dict[tuple[int, str, str], list[bytes]] = defaultdict(list)
    c19c_rows: list[dict[str, Any]] = []
    c19c_pattern_counts = Counter()
    contact_owners: set[str] = set()
    legal_witness_count = 0
    for atom_index in insertion_order:
        atom = atoms[atom_index]
        rb = atom["rank"]
        table = tables[atom["chart"]]
        for (old_id,) in cursor.execute(query.format(table=table), (rb[1], rb[0], rb[3], rb[2], rb[5], rb[4])):
            other = atoms[old_id - 1]
            relations = []
            intersections = []
            for axis in range(3):
                lower = atom["bounds"][2 * axis] if compare_endpoint(atom["bounds"][2 * axis], other["bounds"][2 * axis]) >= 0 else other["bounds"][2 * axis]
                upper = atom["bounds"][2 * axis + 1] if compare_endpoint(atom["bounds"][2 * axis + 1], other["bounds"][2 * axis + 1]) <= 0 else other["bounds"][2 * axis + 1]
                relation = compare_endpoint(lower, upper)
                need(relation <= 0, "R-tree closure false positive")
                relations.append(relation)
                intersections.append((lower, upper))
            dimension = sum(relation < 0 for relation in relations)
            component_relation = "SAME_C15_COMPONENT" if atom["component"] == other["component"] else "CROSS_C15_COMPONENT"
            source_pair = "__".join(sorted((atom["source"], other["source"])))
            dimension_counts[dimension] += 1
            relation_counts[(dimension, component_relation)] += 1
            source_dimension_counts[(dimension, source_pair, component_relation)] += 1
            if dimension == 3:
                continue
            contact_owners.update((atom["owner"], other["owner"]))
            digest = pair_digest(atom["atom_id"], other["atom_id"])
            bucket_digests[(dimension, source_pair, component_relation)].append(digest)
            if source_pair != "C19C__C19C":
                continue
            left, right = sorted((atom, other), key=lambda value: value["atom_id"])
            zero_checks = []
            positive_axes = []
            for axis, relation in enumerate(relations):
                lower, upper = intersections[axis]
                if relation < 0:
                    positive_axes.append({
                        "axis": AXES[axis],
                        "intersection_lower": endpoint_wire(lower),
                        "intersection_upper": endpoint_wire(upper),
                    })
                    continue
                left_boundary, left_closed = endpoint_bit(left, axis, lower)
                right_boundary, right_closed = endpoint_bit(right, axis, lower)
                zero_checks.append({
                    "axis": AXES[axis],
                    "common_endpoint": endpoint_wire(lower),
                    "left_boundary": left_boundary,
                    "right_boundary": right_boundary,
                    "left_closed": left_closed,
                    "right_closed": right_closed,
                    "both_closed": left_closed and right_closed,
                })
            all_zero_axes_double_included = all(check["both_closed"] for check in zero_checks)
            need(not all_zero_axes_double_included, "C19C product authority forbids double-included lower contact")
            legal = component_relation == "CROSS_C15_COMPONENT" and all_zero_axes_double_included
            legal_witness_count += int(legal)
            pattern = tuple((check["left_closed"], check["right_closed"]) for check in zero_checks)
            c19c_pattern_counts[(dimension, pattern)] += 1
            members = []
            for value in (left, right):
                members.append({
                    "atom_id": value["atom_id"],
                    "owner_member_id": value["owner"],
                    "C15_component_id": value["component"],
                    "source_row_sha256": value["source_row_sha256"],
                    "C15_row_sha256": value["C15_row_sha256"],
                    "C25_row_sha256": value["C25_row_sha256"],
                    "v3_endpoint_authority_row_sha256": value["authority_row_sha256"],
                    "endpoint_inclusion_bits": {name: value["bits"][index] for index, name in enumerate(BIT_NAMES)},
                })
            c19c_rows.append({
                "schema": "cm2.c27.same-chart-lower-dimensional-exact-contact.v1.c19c-contact-row.v1",
                "contact_pair_id": "same-chart-lower-contact:" + digest.hex(),
                "contact_pair_digest": digest.hex(),
                "chart": left["chart"],
                "intersection_dimension": dimension,
                "component_relation": component_relation,
                "members": members,
                "positive_width_axes": positive_axes,
                "zero_width_axis_endpoint_checks": zero_checks,
                "all_zero_axes_double_included": all_zero_axes_double_included,
                "legal_cross_component_lower_dimensional_witness": legal,
                "disposition": "REJECT_C19C_PRODUCT_AUTHORITY_EXACTLY_ONE_OWNER_NOT_DOUBLE_INCLUDED",
                "formal_credit": 0,
            })
        cursor.execute(f"INSERT INTO {table} VALUES(?,?,?,?,?,?,?)", (atom_index + 1, *rb))
    db.commit()
    db.close()
    db_path.unlink()

    need(dict(dimension_counts) == EXPECTED_DIMENSION_COUNTS, "complete dimension census")
    need(dict(relation_counts) == EXPECTED_RELATION_COUNTS, "complete component-relation census")
    need(sum(dimension_counts[d] for d in (0, 1, 2)) == 5_783_708, "lower contact total")
    need(len(c19c_rows) == 76_000, "C19C endpoint-dependent contact census")
    need(sum(row["intersection_dimension"] == 1 for row in c19c_rows) == 29_040, "C19C dim1 census")
    need(sum(row["intersection_dimension"] == 2 for row in c19c_rows) == 46_960, "C19C dim2 census")
    need(sum(row["component_relation"] == "CROSS_C15_COMPONENT" for row in c19c_rows) == 49_256, "C19C cross-component census")
    need(legal_witness_count == 0, "zero legal lower-dimensional witnesses")

    bucket_bodies = []
    for key in sorted(bucket_digests):
        dimension, source_pair, component_relation = key
        values = bucket_digests[key]
        values.sort()
        sequence = hashlib.sha256(b"".join(values)).hexdigest()
        bucket_bodies.append({
            "schema": "cm2.c27.same-chart-lower-dimensional-exact-contact.v1.candidate-bucket-commitment-row.v1",
            "intersection_dimension": dimension,
            "source_pair": source_pair.split("__"),
            "component_relation": component_relation,
            "candidate_pair_count": len(values),
            "canonical_sorted_pair_digest_sequence_sha256": sequence,
            "endpoint_policy": "C19C_V3_PRODUCT_AUTHORITY_ROW_MATERIALIZATION" if source_pair == "C19C__C19C" else "AT_LEAST_ONE_FULLY_OPEN_PRIMITIVE_KERNEL_REJECTS_EVERY_ZERO_WIDTH_CONTACT",
            "materialized_C19C_contact_row_count": len(values) if source_pair == "C19C__C19C" else 0,
            "legal_witness_count": 0,
            "formal_credit": 0,
        })
    global_sequence = hashlib.sha256()
    for value in heapq.merge(*(bucket_digests[key] for key in sorted(bucket_digests))):
        global_sequence.update(value)
    global_pair_commitment = global_sequence.hexdigest()

    c19c_rows.sort(key=lambda row: row["contact_pair_digest"])
    bucket_meta = write_rows(candidate_dir / BUCKET_LEDGER, bucket_bodies)
    c19c_meta = write_rows(candidate_dir / C19C_LEDGER, c19c_rows)
    ledgers = {"candidate_buckets": bucket_meta, "C19C_contacts": c19c_meta}

    c26_rows = 0
    c26_rows_on_contact_owners = 0
    c26_covered_contact_owners: set[str] = set()
    for row in closed_rows(ROOT / FILES["C26"][0]):
        c26_rows += 1
        owner = row["owner_member_id"]
        if owner in contact_owners:
            c26_rows_on_contact_owners += 1
            c26_covered_contact_owners.add(owner)
    need(c26_rows == 691_424, "C26 full feature-obligation census")

    stable = {
        "primitive_atom_count": len(atoms),
        "primitive_owner_count": len(owners),
        "endpoint_rank_census_t_p_s": [len(mapping) for mapping in rank_maps],
        "all_closure_intersection_pair_count": sum(dimension_counts.values()),
        "strict_dimension3_pair_count_crosscheck": dimension_counts[3],
        "lower_dimensional_candidate_pair_count": sum(dimension_counts[d] for d in (0, 1, 2)),
        "dimension_census": {str(key): dimension_counts[key] for key in sorted(dimension_counts)},
        "component_relation_census": {f"dim{dimension}__{relation}": count for (dimension, relation), count in sorted(relation_counts.items())},
        "source_dimension_component_census": {f"dim{dimension}__{source_pair}__{relation}": count for (dimension, source_pair, relation), count in sorted(source_dimension_counts.items())},
        "global_canonical_sorted_pair_digest_sequence_sha256": global_pair_commitment,
        "candidate_bucket_count": len(bucket_bodies),
        "C19C_endpoint_dependent_contact_count": len(c19c_rows),
        "C19C_dim1_count": 29_040,
        "C19C_dim2_count": 46_960,
        "C19C_cross_component_count": 49_256,
        "C19C_same_component_count": 26_744,
        "open_kernel_uniform_rejection_candidate_count": 5_783_708 - 76_000,
        "legal_cross_component_lower_dimensional_witness_count": legal_witness_count,
        "C19C_endpoint_pattern_census": {f"dim{dimension}__{pattern}": count for (dimension, pattern), count in sorted(c19c_pattern_counts.items(), key=lambda item: str(item[0]))},
        "contact_owner_count": len(contact_owners),
        "C26_contact_owner_coverage_count": len(c26_covered_contact_owners),
        "C26_contact_owner_gap_count": len(contact_owners - c26_covered_contact_owners),
        "C26_rows_on_contact_owners": c26_rows_on_contact_owners,
        "ledgers": ledgers,
    }
    semantic = {
        "schema": "cm2.c27.same-chart-lower-dimensional-exact-contact.v1.result.v1",
        "status": "PASS_COMPLETE_SAME_CHART_LOWER_DIMENSIONAL_EXACT_CONTACT_SUBGATE__ZERO_LEGAL_WITNESSES__ZERO_FORMAL_CREDIT",
        "execution_seed": seed,
        "execution_order_attestation": object_sha([atoms[index]["atom_id"] for index in insertion_order]),
        "algorithm": "RANDOMIZED_FOUR_CHART_EXACT_INTEGER_ENDPOINT_RANK_RTREE_CLOSURE_ENUMERATION",
        "forbidden_inputs": {
            "C27_FAMILIES_read": False,
            "historical_edge_universe_read": False,
            "older_same_chart_candidate_ledger_read": False,
        },
        "endpoint_authority": {
            "published_v3_manifest_sha256": FILES["V3_MANIFEST"][1],
            "published_v3_authority_ledger_sha256": FILES["V3_AUTHORITY"][1],
            "cold_replay_receipt_sha256": cold["receipt_sha256"],
            "cold_pre_post_SHA_stat_identical": True,
            "five_non_C19C_kernels_fully_open": True,
            "C19C_product_rule_consumed_row_by_row": True,
        },
        "authority_joins": {
            "C15_full_rows": c15_rows,
            "C25_full_rows": c25_rows,
            "C26_full_rows": c26_rows,
            "C15_C25_primitive_join_gap": 0,
            "C19C_v3_endpoint_authority_join_gap": 0,
            "C26_absence_used_as_negative_geometry_theorem": False,
        },
        "census": stable,
        "semantic_projection_sha256": object_sha(stable),
        "input_pins": {filename: pin for filename, pin in (value for value in FILES.values())},
        "formal_credit": 0,
        "C27_C28_C29": "REBUILD_REQUIRED_AND_NOT_AUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
        "source_W_transition_authorized": False,
        "required_next": "INTEGRATE_WITH_ALL_OTHER_PRIMITIVE_FAMILY_TOTALITY_SUBGATES_BEFORE_ANY_C27_REBUILD",
    }
    result = {**semantic, "result_sha256": object_sha(semantic)}
    (candidate_dir / RESULT).write_bytes(canonical(result))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    result = build(Path(args.candidate_dir).resolve(), args.seed)
    print(canonical({
        "status": result["status"],
        "execution_seed": result["execution_seed"],
        "lower_dimensional_candidate_pair_count": result["census"]["lower_dimensional_candidate_pair_count"],
        "legal_witness_count": result["census"]["legal_cross_component_lower_dimensional_witness_count"],
        "semantic_projection_sha256": result["semantic_projection_sha256"],
        "result_sha256": result["result_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
