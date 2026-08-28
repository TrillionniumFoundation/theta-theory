#!/usr/bin/env python3
"""Independent non-SQLite verifier for the SAME_CHART lower-contact subgate.

The candidate universe is reconstructed directly from the primitive sources.
Completeness is recomputed with a chart-local exact-rank t sweep; this file
does not import the producer and never opens a C27 family/edge/census ledger.
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
PREFIX = "cm2_c27_same_chart_lower_dimensional_exact_contact_v1"
RESULT = PREFIX + "_result.json"
BUCKET_LEDGER = PREFIX + "_complete_candidate_bucket_commitments.jsonl.gz"
C19C_LEDGER = PREFIX + "_c19c_endpoint_dependent_contacts.jsonl.gz"

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
OPEN_KINDS = {"C19A": "OPEN_RATIONAL_BOX", "C19B": "OPEN_RATIONAL_BOX", "C20A": "OPEN_RATIONAL_BOX", "C22A": "OPEN_RATIONAL_BOX", "C23A": "T2PS_BRANCH_OPEN_RATIONAL_BOX"}
CHARTS = ("G:E", "G:N", "G:S", "G:W")
AXES = ("t", "p", "s")
BIT_NAMES = ("t_lower_closed", "t_upper_closed", "p_lower_closed", "p_upper_closed", "s_lower_closed", "s_upper_closed")
EXPECTED_DIMS = {0: 807104, 1: 2611136, 2: 2365468, 3: 187132}
EXPECTED_RELATIONS = {
    (0, "CROSS_C15_COMPONENT"): 431473, (0, "SAME_C15_COMPONENT"): 375631,
    (1, "CROSS_C15_COMPONENT"): 1239209, (1, "SAME_C15_COMPONENT"): 1371927,
    (2, "CROSS_C15_COMPONENT"): 927984, (2, "SAME_C15_COMPONENT"): 1437484,
    (3, "CROSS_C15_COMPONENT"): 32240, (3, "SAME_C15_COMPONENT"): 154892,
}


class Reject(RuntimeError):
    pass


def require(flag: bool, label: str) -> None:
    if type(flag) is not bool or not flag:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def hash_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            require(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            raw = line[:-1]
            value = json.loads(raw)
            require(type(value) is dict and encode(value) == raw, f"canonical:{path.name}:{ordinal}")
            body = dict(value)
            claimed = body.pop("row_sha256", None)
            require(claimed == digest(body), f"row closure:{path.name}:{ordinal}")
            yield value


def closed_json(path: Path, closure: str) -> dict[str, Any]:
    raw = path.read_bytes()
    value = json.loads(raw)
    require(type(value) is dict and encode(value) == raw, "canonical JSON:" + path.name)
    body = dict(value)
    claimed = body.pop(closure, None)
    require(claimed == digest(body), "JSON closure:" + path.name)
    return value


Number = tuple[Any, ...]


def rational(text: str) -> Number:
    return ("Q", Fraction(text))


def radical(text: str, sign: int) -> Number:
    q = Fraction(text)
    require(q >= 0 and sign in {-1, 1}, "radical domain")
    a, b = math.isqrt(q.numerator), math.isqrt(q.denominator)
    if a * a == q.numerator and b * b == q.denominator:
        return ("Q", Fraction(sign * a, b))
    return ("SQ", sign, q)


def order(left: Number, right: Number) -> int:
    if left == right:
        return 0
    if left[0] == right[0] == "Q":
        return -1 if left[1] < right[1] else 1
    if left[0] == right[0] == "SQ":
        ls, lq, rs, rq = left[1], left[2], right[1], right[2]
        if ls != rs:
            return -1 if ls < rs else 1
        direction = -1 if lq < rq else 1
        return direction if ls == 1 else -direction
    if left[0] == "Q":
        x, sign, q = left[1], right[1], right[2]
        if sign == 1:
            if x < 0:
                return -1
            delta = x * x - q
            return 0 if delta == 0 else (-1 if delta < 0 else 1)
        if x >= 0:
            return 1
        delta = x * x - q
        return 0 if delta == 0 else (-1 if delta > 0 else 1)
    return -order(right, left)


def qtext(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def wire(value: Number) -> dict[str, Any]:
    if value[0] == "Q":
        return {"kind": "Q", "value": qtext(value[1])}
    return {"kind": "SIGNED_SQRT_Q", "radicand": qtext(value[2]), "sign": value[1]}


def physical_bounds(source: str, ast: dict[str, Any]) -> tuple[Number, ...]:
    raw = ast.get("bounds")
    require(type(raw) is list and len(raw) == 6 and all(type(x) is str for x in raw), "six exact bounds:" + source)
    if source != "C23A":
        require(ast.get("coordinates") == ["t", "p", "s"], "physical coordinates:" + source)
        result = tuple(rational(x) for x in raw)
    else:
        require(ast.get("kind") == "T2PS_BRANCH_OPEN_RATIONAL_BOX", "C23 kind")
        sign = ast.get("physical_t_sign")
        require(sign in {-1, 1}, "C23 sign")
        t0, t1 = (radical(raw[0], 1), radical(raw[1], 1)) if sign == 1 else (radical(raw[1], -1), radical(raw[0], -1))
        result = (t0, t1, rational(raw[2]), rational(raw[3]), rational(raw[4]), rational(raw[5]))
    require(all(order(result[2 * axis], result[2 * axis + 1]) < 0 for axis in range(3)), "positive widths:" + source)
    return result


def chart_maps() -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]:
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
    require(len(c5) == 33344, "C5 empty-graph chart census")
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
        chart = row["support_ast"]["recharted_target_chart"]
    require(chart in CHARTS, "four-chart atom")
    return chart


def atom_id(source: str, row: dict[str, Any]) -> str:
    if source == "C22A":
        return row["predicate_cell_row_id"]
    if source == "C23A":
        return row["R292_refinement_cell_id"]
    return f"{source.lower()}-support-atom:{row['row_sha256']}"


def pair_hash(left: str, right: str) -> bytes:
    return hashlib.sha256(encode(sorted((left, right)))).digest()


def endpoint_bit(atom: dict[str, Any], axis: int, coordinate: Number) -> tuple[str, bool]:
    lower, upper = atom["bounds"][2 * axis:2 * axis + 2]
    if order(coordinate, lower) == 0:
        return "LOWER", atom["bits"][2 * axis]
    require(order(coordinate, upper) == 0, "contact coordinate is endpoint")
    return "UPPER", atom["bits"][2 * axis + 1]


def rebuild(seed: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    require(type(seed) is int and seed > 0, "positive verification seed")
    for role, (filename, expected) in FILES.items():
        require(hash_file(ROOT / filename) == expected, "input pin:" + role)
    cold = closed_json(ROOT / FILES["V3_COLD_RECEIPT"][0], "receipt_sha256")
    require(cold["status"] == "PASS_COLD_POSTPUBLICATION_REPLAY_PRE_POST_SHA_STAT_IDENTICAL__ZERO_FORMAL_CREDIT", "cold status")
    require(cold["pre_post_sha256_identical"] is True and cold["pre_post_stat_identical"] is True, "cold TOCTOU identity")
    require(cold["formal_credit"] == 0 and cold["C27_C28_C29"] == "UNAUTHORIZED_PENDING_REBUILD", "cold nonpromotion")

    authority = {}
    for row in rows(ROOT / FILES["V3_AUTHORITY"][0]):
        require(row["member_id"] not in authority, "v3 authority uniqueness")
        require(set(row["endpoint_inclusion_bits"]) == set(BIT_NAMES), "v3 exact bit names")
        require(all(type(row["endpoint_inclusion_bits"][name]) is bool for name in BIT_NAMES), "v3 bool bits")
        authority[row["member_id"]] = row
    require(len(authority) == 33344, "v3 authority census")

    maps = chart_maps()
    atoms = []
    owners_to_sources: dict[str, set[str]] = defaultdict(set)
    endpoints = [set(), set(), set()]
    seen_ids = set()
    source_counts = Counter()
    for source in COUNTS:
        for row in rows(ROOT / FILES[source][0]):
            source_counts[source] += 1
            owner = row.get("member_id") or row["owner_member_id"]
            embedded = row.get("fresh_component_id") or row["owner_fresh_component_id"]
            identity = atom_id(source, row)
            require(identity not in seen_ids, "primitive atom id uniqueness")
            seen_ids.add(identity)
            box = physical_bounds(source, row["support_ast"])
            chart = chart_for(source, row, maps)
            if source == "C19C":
                auth = authority[owner]
                require(auth["C19C_row_sha256"] == row["row_sha256"] and auth["chart"] == chart, "v3 row/chart binding")
                require(auth["bounds"] == row["support_ast"]["bounds"], "v3 bounds binding")
                bits = tuple(auth["endpoint_inclusion_bits"][name] for name in BIT_NAMES)
                auth_row = auth["row_sha256"]
            else:
                require(row["support_ast"]["kind"] == OPEN_KINDS[source], "fully-open kernel:" + source)
                bits = (False,) * 6
                auth_row = None
            for axis in range(3):
                endpoints[axis].update(box[2 * axis:2 * axis + 2])
            owners_to_sources[owner].add(source)
            atoms.append({"id": identity, "source": source, "source_row": row["row_sha256"], "owner": owner, "embedded": embedded, "chart": chart, "bounds": box, "bits": bits, "authority_row": auth_row})
        require(source_counts[source] == COUNTS[source], "source census:" + source)
    require(len(atoms) == 483232 and len(owners_to_sources) == 482380, "primitive atom/owner census")
    atoms.sort(key=lambda atom: atom["id"])
    owners = set(owners_to_sources)

    c15 = {}
    all_components = set()
    c15_rows = 0
    for row in rows(ROOT / FILES["C15"][0]):
        c15_rows += 1
        all_components.add(row["fresh_component_id"])
        member = row["registry_member_id"]
        if member in owners:
            require(member not in c15, "C15 unique owner")
            c15[member] = (row["fresh_component_id"], row["row_sha256"])
    require(c15_rows == 502204 and len(all_components) == 57876 and set(c15) == owners, "complete C15 join")
    c25 = {}
    c25_rows = 0
    for row in rows(ROOT / FILES["C25"][0]):
        c25_rows += 1
        member = row["member_id"]
        if member in owners:
            bind = row["source_bindings"]
            require(member not in c25, "C25 unique owner")
            c25[member] = (row["fresh_component_id"], row["row_sha256"], bind["support_kernel"], bind["C15_member_row_sha256"])
    require(c25_rows == 502204 and set(c25) == owners, "complete C25 join")
    for atom in atoms:
        owner = atom["owner"]
        expected_kernel = {KERNEL[source] for source in owners_to_sources[owner]}
        require(len(expected_kernel) == 1, "one C25 kernel per owner")
        require(atom["embedded"] == c15[owner][0] == c25[owner][0], "primitive/C15/C25 component")
        require(c15[owner][1] == c25[owner][3] and c25[owner][2] == next(iter(expected_kernel)), "C25 exact source binding")
        atom["component"] = c15[owner][0]
        atom["c15"] = c15[owner][1]
        atom["c25"] = c25[owner][1]

    rank_maps = []
    for values in endpoints:
        ordered = sorted(values, key=cmp_to_key(order))
        require(all(order(a, b) < 0 for a, b in zip(ordered, ordered[1:])), "strict endpoint ranks")
        rank_maps.append({value: ordinal + 1 for ordinal, value in enumerate(ordered)})
    require([len(mapping) for mapping in rank_maps] == [6433, 1201, 257], "endpoint rank census")
    for atom in atoms:
        rank = []
        for axis in range(3):
            rank.extend((rank_maps[axis][atom["bounds"][2 * axis]], rank_maps[axis][atom["bounds"][2 * axis + 1]]))
        atom["rank"] = tuple(rank)

    rng = random.Random(seed)
    ties = [rng.getrandbits(64) for _ in atoms]
    traversal = sorted(range(len(atoms)), key=lambda index: (atoms[index]["chart"], atoms[index]["rank"][0], ties[index], atoms[index]["id"]))
    dimension_counts = Counter()
    relation_counts = Counter()
    source_dimension_counts = Counter()
    buckets: dict[tuple[int, str, str], list[bytes]] = defaultdict(list)
    c19c_contacts = []
    patterns = Counter()
    contact_owners = set()
    legal_count = 0
    for chart in CHARTS:
        active: set[int] = set()
        expiry: list[tuple[int, int]] = []
        for index in (value for value in traversal if atoms[value]["chart"] == chart):
            current = atoms[index]
            cr = current["rank"]
            # Closed-contact sweep: equality at t is retained.
            while expiry and expiry[0][0] < cr[0]:
                _, old = heapq.heappop(expiry)
                active.discard(old)
            for old in active:
                other = atoms[old]
                rr = other["rank"]
                if not (rr[2] <= cr[3] and rr[3] >= cr[2] and rr[4] <= cr[5] and rr[5] >= cr[4]):
                    continue
                intersections = []
                relations = []
                for axis in range(3):
                    lower = current["bounds"][2 * axis] if order(current["bounds"][2 * axis], other["bounds"][2 * axis]) >= 0 else other["bounds"][2 * axis]
                    upper = current["bounds"][2 * axis + 1] if order(current["bounds"][2 * axis + 1], other["bounds"][2 * axis + 1]) <= 0 else other["bounds"][2 * axis + 1]
                    relation = order(lower, upper)
                    require(relation <= 0, "sweep closure false positive")
                    intersections.append((lower, upper))
                    relations.append(relation)
                dimension = sum(value < 0 for value in relations)
                component_relation = "SAME_C15_COMPONENT" if current["component"] == other["component"] else "CROSS_C15_COMPONENT"
                source_pair = "__".join(sorted((current["source"], other["source"])))
                dimension_counts[dimension] += 1
                relation_counts[(dimension, component_relation)] += 1
                source_dimension_counts[(dimension, source_pair, component_relation)] += 1
                if dimension == 3:
                    continue
                contact_owners.update((current["owner"], other["owner"]))
                ph = pair_hash(current["id"], other["id"])
                buckets[(dimension, source_pair, component_relation)].append(ph)
                if source_pair != "C19C__C19C":
                    continue
                left, right = sorted((current, other), key=lambda atom: atom["id"])
                checks = []
                positives = []
                for axis, relation in enumerate(relations):
                    lower, upper = intersections[axis]
                    if relation < 0:
                        positives.append({"axis": AXES[axis], "intersection_lower": wire(lower), "intersection_upper": wire(upper)})
                    else:
                        lb, lc = endpoint_bit(left, axis, lower)
                        rb, rc = endpoint_bit(right, axis, lower)
                        checks.append({"axis": AXES[axis], "common_endpoint": wire(lower), "left_boundary": lb, "right_boundary": rb, "left_closed": lc, "right_closed": rc, "both_closed": lc and rc})
                double = all(check["both_closed"] for check in checks)
                require(not double, "v3 product authority excludes double inclusion")
                legal = component_relation == "CROSS_C15_COMPONENT" and double
                legal_count += int(legal)
                patterns[(dimension, tuple((check["left_closed"], check["right_closed"]) for check in checks))] += 1
                members = []
                for atom in (left, right):
                    members.append({
                        "atom_id": atom["id"], "owner_member_id": atom["owner"], "C15_component_id": atom["component"],
                        "source_row_sha256": atom["source_row"], "C15_row_sha256": atom["c15"], "C25_row_sha256": atom["c25"],
                        "v3_endpoint_authority_row_sha256": atom["authority_row"],
                        "endpoint_inclusion_bits": {name: atom["bits"][position] for position, name in enumerate(BIT_NAMES)},
                    })
                c19c_contacts.append({
                    "schema": "cm2.c27.same-chart-lower-dimensional-exact-contact.v1.c19c-contact-row.v1",
                    "contact_pair_id": "same-chart-lower-contact:" + ph.hex(), "contact_pair_digest": ph.hex(), "chart": left["chart"],
                    "intersection_dimension": dimension, "component_relation": component_relation, "members": members,
                    "positive_width_axes": positives, "zero_width_axis_endpoint_checks": checks,
                    "all_zero_axes_double_included": double, "legal_cross_component_lower_dimensional_witness": legal,
                    "disposition": "REJECT_C19C_PRODUCT_AUTHORITY_EXACTLY_ONE_OWNER_NOT_DOUBLE_INCLUDED", "formal_credit": 0,
                })
            active.add(index)
            heapq.heappush(expiry, (cr[1], index))
    require(dict(dimension_counts) == EXPECTED_DIMS, "complete dimension census")
    require(dict(relation_counts) == EXPECTED_RELATIONS, "complete relation census")
    require(sum(dimension_counts[d] for d in (0, 1, 2)) == 5783708, "lower total")
    require(len(c19c_contacts) == 76000 and legal_count == 0, "C19C endpoint-dependent zero-witness census")
    require(sum(row["intersection_dimension"] == 1 for row in c19c_contacts) == 29040, "C19C dim1")
    require(sum(row["intersection_dimension"] == 2 for row in c19c_contacts) == 46960, "C19C dim2")
    require(sum(row["component_relation"] == "CROSS_C15_COMPONENT" for row in c19c_contacts) == 49256, "C19C cross")

    c26_rows = 0
    c26_on_contact = 0
    c26_covered = set()
    for row in rows(ROOT / FILES["C26"][0]):
        c26_rows += 1
        owner = row["owner_member_id"]
        if owner in contact_owners:
            c26_on_contact += 1
            c26_covered.add(owner)
    require(c26_rows == 691424, "C26 full census")
    return atoms, {
        "dimension_counts": dimension_counts, "relation_counts": relation_counts,
        "source_dimension_counts": source_dimension_counts, "buckets": buckets,
        "c19c_contacts": c19c_contacts, "patterns": patterns, "legal_count": legal_count,
        "contact_owners": contact_owners, "c26_rows": c26_rows,
        "c26_on_contact": c26_on_contact, "c26_covered": c26_covered,
        "all_components": all_components, "cold": cold,
    }


def expected_row(body: dict[str, Any], ordinal: int) -> dict[str, Any]:
    row = {**body, "ordinal": ordinal}
    row["row_sha256"] = digest(row)
    return row


def verify(candidate_dir: Path, output: Path, seed: int) -> dict[str, Any]:
    result = closed_json(candidate_dir / RESULT, "result_sha256")
    require(result["status"] == "PASS_COMPLETE_SAME_CHART_LOWER_DIMENSIONAL_EXACT_CONTACT_SUBGATE__ZERO_LEGAL_WITNESSES__ZERO_FORMAL_CREDIT", "candidate PASS status")
    require(result["forbidden_inputs"] == {"C27_FAMILIES_read": False, "historical_edge_universe_read": False, "older_same_chart_candidate_ledger_read": False}, "forbidden inputs")
    require(result["formal_credit"] == 0 and result["C27_C28_C29"] == "REBUILD_REQUIRED_AND_NOT_AUTHORIZED", "candidate zero-credit governance")
    require(result["CM2"] == "NO-GO_FOR_CLAIM" and result["source_W_transition_authorized"] is False, "candidate fail closed")
    require(result["input_pins"] == {filename: pin for filename, pin in (value for value in FILES.values())}, "candidate input pins")

    atoms, audit = rebuild(seed)
    buckets = audit["buckets"]
    bucket_bodies = []
    for key in sorted(buckets):
        dimension, source_pair, relation = key
        values = sorted(buckets[key])
        buckets[key] = values
        bucket_bodies.append({
            "schema": "cm2.c27.same-chart-lower-dimensional-exact-contact.v1.candidate-bucket-commitment-row.v1",
            "intersection_dimension": dimension, "source_pair": source_pair.split("__"), "component_relation": relation,
            "candidate_pair_count": len(values), "canonical_sorted_pair_digest_sequence_sha256": hashlib.sha256(b"".join(values)).hexdigest(),
            "endpoint_policy": "C19C_V3_PRODUCT_AUTHORITY_ROW_MATERIALIZATION" if source_pair == "C19C__C19C" else "AT_LEAST_ONE_FULLY_OPEN_PRIMITIVE_KERNEL_REJECTS_EVERY_ZERO_WIDTH_CONTACT",
            "materialized_C19C_contact_row_count": len(values) if source_pair == "C19C__C19C" else 0,
            "legal_witness_count": 0, "formal_credit": 0,
        })
    actual_bucket_rows = list(rows(candidate_dir / BUCKET_LEDGER))
    expected_bucket_rows = [expected_row(body, ordinal) for ordinal, body in enumerate(bucket_bodies)]
    require(actual_bucket_rows == expected_bucket_rows, "complete bucket ledger exact match")

    contacts = sorted(audit["c19c_contacts"], key=lambda row: row["contact_pair_digest"])
    actual_contact_rows = list(rows(candidate_dir / C19C_LEDGER))
    expected_contact_rows = [expected_row(body, ordinal) for ordinal, body in enumerate(contacts)]
    require(actual_contact_rows == expected_contact_rows, "all 76000 C19C contact rows exact match")

    def ledger_meta(path: Path, observed: list[dict[str, Any]]) -> dict[str, Any]:
        sequence = hashlib.sha256()
        for row in observed:
            sequence.update(bytes.fromhex(row["row_sha256"]))
        return {"filename": path.name, "row_count": len(observed), "row_sequence_sha256": sequence.hexdigest(), "sha256": hash_file(path), "size": path.stat().st_size}

    bucket_meta = ledger_meta(candidate_dir / BUCKET_LEDGER, actual_bucket_rows)
    contact_meta = ledger_meta(candidate_dir / C19C_LEDGER, actual_contact_rows)
    require(result["census"]["ledgers"] == {"candidate_buckets": bucket_meta, "C19C_contacts": contact_meta}, "candidate ledger metadata")

    global_state = hashlib.sha256()
    for value in heapq.merge(*(buckets[key] for key in sorted(buckets))):
        global_state.update(value)
    dims = audit["dimension_counts"]
    relations = audit["relation_counts"]
    sources = audit["source_dimension_counts"]
    patterns = audit["patterns"]
    stable = {
        "primitive_atom_count": len(atoms), "primitive_owner_count": len({atom["owner"] for atom in atoms}),
        "endpoint_rank_census_t_p_s": [6433, 1201, 257],
        "all_closure_intersection_pair_count": sum(dims.values()), "strict_dimension3_pair_count_crosscheck": dims[3],
        "lower_dimensional_candidate_pair_count": sum(dims[d] for d in (0, 1, 2)),
        "dimension_census": {str(key): dims[key] for key in sorted(dims)},
        "component_relation_census": {f"dim{dimension}__{relation}": count for (dimension, relation), count in sorted(relations.items())},
        "source_dimension_component_census": {f"dim{dimension}__{source_pair}__{relation}": count for (dimension, source_pair, relation), count in sorted(sources.items())},
        "global_canonical_sorted_pair_digest_sequence_sha256": global_state.hexdigest(),
        "candidate_bucket_count": len(bucket_bodies), "C19C_endpoint_dependent_contact_count": len(contacts),
        "C19C_dim1_count": 29040, "C19C_dim2_count": 46960, "C19C_cross_component_count": 49256, "C19C_same_component_count": 26744,
        "open_kernel_uniform_rejection_candidate_count": 5707708, "legal_cross_component_lower_dimensional_witness_count": audit["legal_count"],
        "C19C_endpoint_pattern_census": {f"dim{dimension}__{pattern}": count for (dimension, pattern), count in sorted(patterns.items(), key=lambda item: str(item[0]))},
        "contact_owner_count": len(audit["contact_owners"]), "C26_contact_owner_coverage_count": len(audit["c26_covered"]),
        "C26_contact_owner_gap_count": len(audit["contact_owners"] - audit["c26_covered"]), "C26_rows_on_contact_owners": audit["c26_on_contact"],
        "ledgers": {"candidate_buckets": bucket_meta, "C19C_contacts": contact_meta},
    }
    require(result["census"] == stable, "complete result census")
    require(result["semantic_projection_sha256"] == digest(stable), "semantic projection")
    require(result["authority_joins"] == {"C15_full_rows": 502204, "C25_full_rows": 502204, "C26_full_rows": 691424, "C15_C25_primitive_join_gap": 0, "C19C_v3_endpoint_authority_join_gap": 0, "C26_absence_used_as_negative_geometry_theorem": False}, "authority joins")
    require(result["endpoint_authority"]["five_non_C19C_kernels_fully_open"] is True and result["endpoint_authority"]["C19C_product_rule_consumed_row_by_row"] is True, "endpoint authority statement")

    body = {
        "schema": "cm2.c27.same-chart-lower-dimensional-exact-contact.v1.independent-verification.v1",
        "status": "PASS_INDEPENDENT_NONSQLITE_EXACT_T_SWEEP_MATCHES_ALL_5783708_LOWER_CONTACTS_AND_76000_ENDPOINT_ROWS__ZERO_FORMAL_CREDIT",
        "verification_seed": seed,
        "algorithm": "CHART_LOCAL_EXACT_ENDPOINT_RANK_T_SWEEP_WITH_CLOSED_EQUALITY_RETENTION_AND_EXACT_P_S_COMPARISONS",
        "candidate_result_sha256": result["result_sha256"], "candidate_semantic_projection_sha256": result["semantic_projection_sha256"],
        "complete_closure_pair_count": sum(dims.values()), "lower_dimensional_candidate_pair_count": 5783708,
        "strict_dimension3_pair_count_crosscheck": 187132, "C19C_endpoint_dependent_contact_count": 76000,
        "other_fully_open_rejection_count": 5707708, "legal_cross_component_lower_dimensional_witness_count": 0,
        "global_pair_commitment": global_state.hexdigest(), "bucket_ledger_sha256": bucket_meta["sha256"], "C19C_ledger_sha256": contact_meta["sha256"],
        "formal_credit": 0, "C27_C28_C29": "REBUILD_REQUIRED_AND_NOT_AUTHORIZED", "CM2": "NO-GO_FOR_CLAIM", "source_W_transition_authorized": False,
    }
    verification = {**body, "verification_sha256": digest(body)}
    output.write_bytes(encode(verification))
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
