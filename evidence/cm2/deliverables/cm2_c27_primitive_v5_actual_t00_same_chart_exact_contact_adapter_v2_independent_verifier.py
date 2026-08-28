#!/usr/bin/env python3
"""No-producer-import inverse/completeness verifier for T00 corrected-v2.

It reconstructs every emitted authority/candidate/proof row from direct
primitive inputs and then independently re-enumerates the four-chart closure
intersection set.  The independent enumeration deletes keys from a strict
observed-key table; exact exhaustion proves no omitted or invented pair.
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
import sqlite3
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
PRODUCER = ROOT / "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2.py"
PRODUCER_SHA = "27b1a0e0eef9d71070a5925a40b3a2d4e33608437545fde2e4ec2ad9013f4e66"
RUNNER = ROOT / "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2_runner.py"
RUNNER_SHA = "38af3747bed3f8800972847c104328b7aa870c1c63bfb8232282ec533fe041fd"
T00 = "SAME_CHART_RELATIVE_CELLS"
SLOT = "T00_SAME_CHART_RELATIVE_CELLS"
AUTHORITY_SCHEMA = "cm2.c27-independent.primitive-v5-actual.t00-same-chart-exact-contact-authority.row.v2"
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
PAIR_PREFIX = "round306c27-v5-same-chart-exact-contact:"
PROOF_PREFIX = "round306c27-v5-physical-proof:"
EDGE_PREFIX = "round306c27r2-v5-component-edge:"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
AXES = ("t", "p", "s")
BITS = ("t_lower_closed", "t_upper_closed", "p_lower_closed",
        "p_upper_closed", "s_lower_closed", "s_upper_closed")
CHARTS = ("G:E", "G:N", "G:S", "G:W")
COUNTS = {"C19A": 5596, "C19B": 12232, "C19C": 33344,
          "C20A": 126468, "C22A": 295340, "C23A": 10252}
OPEN_KINDS = {"C19A": "OPEN_RATIONAL_BOX", "C19B": "OPEN_RATIONAL_BOX",
              "C20A": "OPEN_RATIONAL_BOX", "C22A": "OPEN_RATIONAL_BOX",
              "C23A": "T2PS_BRANCH_OPEN_RATIONAL_BOX"}
EXPECTED_DIMENSIONS = {0: 807_104, 1: 2_611_136,
                       2: 2_365_468, 3: 187_132}
EXPECTED_RELATIONS = {
    (0, "CROSS_C15_COMPONENT"): 431_473,
    (0, "SAME_C15_COMPONENT"): 375_631,
    (1, "CROSS_C15_COMPONENT"): 1_239_209,
    (1, "SAME_C15_COMPONENT"): 1_371_927,
    (2, "CROSS_C15_COMPONENT"): 927_984,
    (2, "SAME_C15_COMPONENT"): 1_437_484,
    (3, "CROSS_C15_COMPONENT"): 32_240,
    (3, "SAME_C15_COMPONENT"): 154_892,
}
C26_RECEIPT_OBJECT = "4689da7fb3e4c339419e74a2fc603ec3e5ff595e6c940ef442b306198f10efcd"
G2A_RECEIPT_OBJECT = "b9cefd8474b6cd45b9d0afc6667024369d9461db559bbef5cee9c1c368f6d556"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def byte_identical(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    with left.open("rb") as a, right.open("rb") as b:
        while True:
            x, y = a.read(4 << 20), b.read(4 << 20)
            if x != y:
                return False
            if not x:
                return True


def root_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    need(ROOT in path.parents, "path inside workspace")
    return path


def document(path: Path, closure: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claim = body.pop(closure, None)
    need(type(claim) is str and claim == digest(body),
         "document closure:" + path.name)
    return value


def raw_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            payload = line[:-1]
            row = json.loads(payload)
            need(type(row) is dict and canonical(row) == payload,
                 f"canonical:{path.name}:{ordinal}")
            body = dict(row)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and claim == digest(body),
                 f"closure:{path.name}:{ordinal}")
            yield row


class DescriptorReader:
    def __init__(self, desc: dict[str, Any]):
        self.desc = desc
        self.path = root_path(desc["path"])
        need(self.path.is_file() and self.path.stat().st_size == desc["size"]
             and fsha(self.path) == desc["sha256"],
             "descriptor file:" + self.path.name)
        self.iterator = raw_rows(self.path)
        self.count = 0
        self.sequence = hashlib.sha256()

    def next(self) -> dict[str, Any]:
        try:
            row = next(self.iterator)
        except StopIteration as error:
            raise Failure("early EOF:" + self.path.name) from error
        need(row["schema"] == self.desc["row_schema"],
             "descriptor row schema:" + self.path.name)
        self.sequence.update(row["row_sha256"].encode("ascii") + b"\n")
        self.count += 1
        return row

    def finish(self) -> None:
        try:
            next(self.iterator)
        except StopIteration:
            pass
        else:
            raise Failure("extra row:" + self.path.name)
        need(self.count == self.desc["row_count"]
             and self.sequence.hexdigest() == self.desc["row_sequence_sha256"],
             "descriptor count/sequence:" + self.path.name)


Endpoint = tuple[Any, ...]


def q_endpoint(value: str) -> Endpoint:
    return (0, Fraction(value))


def sqrt_endpoint(value: str, sign: int) -> Endpoint:
    q = Fraction(value)
    need(q >= 0 and sign in {-1, 1}, "sqrt domain")
    a, b = math.isqrt(q.numerator), math.isqrt(q.denominator)
    if a * a == q.numerator and b * b == q.denominator:
        return (0, Fraction(sign * a, b))
    return (1, q, sign)


def compare_endpoint(left: Endpoint, right: Endpoint) -> int:
    if left == right:
        return 0
    if left[0] == right[0] == 0:
        return -1 if left[1] < right[1] else 1
    if left[0] == right[0] == 1:
        if left[2] != right[2]:
            return -1 if left[2] < right[2] else 1
        result = -1 if left[1] < right[1] else 1
        return result if left[2] == 1 else -result
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


def qwire(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def endpoint_wire(value: Endpoint) -> dict[str, Any]:
    if value[0] == 0:
        return {"kind": "Q", "value": qwire(value[1])}
    return {"kind": "SIGNED_SQRT_Q", "radicand": qwire(value[1]),
            "sign": value[2]}


def bounds_for(source: str, support: dict[str, Any]) -> tuple[Endpoint, ...]:
    raw = support["bounds"]
    need(type(raw) is list and len(raw) == 6, "six bounds")
    if source != "C23A":
        result = tuple(q_endpoint(value) for value in raw)
    else:
        sign = support["physical_t_sign"]
        t0, t1 = ((sqrt_endpoint(raw[0], 1), sqrt_endpoint(raw[1], 1))
                  if sign == 1 else
                  (sqrt_endpoint(raw[1], -1), sqrt_endpoint(raw[0], -1)))
        result = (t0, t1, q_endpoint(raw[2]), q_endpoint(raw[3]),
                  q_endpoint(raw[4]), q_endpoint(raw[5]))
    need(all(compare_endpoint(result[2 * axis], result[2 * axis + 1]) < 0
             for axis in range(3)), "positive box")
    return result


def atom_key(source: str, row: dict[str, Any]) -> str:
    if source == "C22A":
        return row["predicate_cell_row_id"]
    if source == "C23A":
        return row["R292_refinement_cell_id"]
    return f"{source.lower()}-support-atom:{row['row_sha256']}"


def endpoint_bit(atom: dict[str, Any], axis: int,
                 coordinate: Endpoint) -> tuple[str, bool]:
    lower, upper = atom["bounds"][2 * axis:2 * axis + 2]
    if compare_endpoint(coordinate, lower) == 0:
        return "LOWER", atom["bits"][2 * axis]
    need(compare_endpoint(coordinate, upper) == 0, "endpoint contact")
    return "UPPER", atom["bits"][2 * axis + 1]


def manifest_bytes(receipt_path: Path, receipt: dict[str, Any]) -> bytes:
    adapter = receipt["terminal_adapter"]
    lines = []
    for key in ("candidate_ownership_ledger",
                "materialized_physical_proof_fragment_ledger",
                "primitive_authority_ledger"):
        desc = adapter[key]
        lines.append(f"{desc['sha256']}  {desc['path']}\n")
    for item in receipt["root_input_capture"]["attestations"].values():
        lines.append(f"{item['sha256']}  {item['path']}\n")
    lines.extend((f"{PRODUCER_SHA}  {PRODUCER.relative_to(ROOT)}\n",
                  f"{fsha(receipt_path)}  {receipt_path.relative_to(ROOT)}\n"))
    return "".join(sorted(set(lines))).encode("ascii")


def verify_receipt_shell(path: Path) -> dict[str, Any]:
    receipt = document(path, "receipt_sha256")
    need(receipt["schema"] == "cm2.c27-independent.primitive-v5-actual-t00-same-chart-exact-contact-adapter.v2"
         and receipt["producer_source_sha256"] == PRODUCER_SHA
         and fsha(PRODUCER) == PRODUCER_SHA
         and receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False,
         "receipt source/governance")
    adapter = receipt["terminal_adapter"]
    need((adapter["terminal_ordinal"], adapter["terminal"],
          adapter["authority_slot"]) == (0, T00, SLOT), "T00 slot")
    exact = receipt["exact_census"]
    need(exact["primitive_support_atom_count"] == 483_232
         and exact["candidate_count"] == 5_970_840
         and exact["strict_dimension3_candidate_count"] == 187_132
         and exact["lower_dimension0_1_2_candidate_count"] == 5_783_708
         and exact["lower_cross_component_candidate_count"] == 2_598_666
         and exact["lower_same_component_candidate_count"] == 3_185_042
         and exact["lower_fully_open_rejection_count"] == 5_707_708
         and exact["lower_C19C_endpoint_dependent_rejection_count"] == 76_000
         and exact["lower_legal_witness_count"] == 0
         and exact["strict_cross_component_physical_proof_count"] == 32_240
         and exact["strict_same_component_no_edge_count"] == 154_892
         and exact["unique_component_edge_count"] == 14_772,
         "receipt exact census")
    need(exact["candidate_component_disposition_census"] == {
        "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 32_240,
        "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 5_783_708,
        "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 154_892},
         "receipt disposition census")
    need(all(value is True for value in receipt["authority_closures"].values())
         and all(value is False
                 for value in receipt["forbidden_input_governance"].values()),
         "receipt closures/forbidden")
    descriptions = (("primitive_authority_ledger", AUTHORITY_SCHEMA, 5_970_840),
                    ("candidate_ownership_ledger", CANDIDATE_SCHEMA, 5_970_840),
                    ("materialized_physical_proof_fragment_ledger", PROOF_SCHEMA, 32_240))
    for key, schema, count in descriptions:
        desc = adapter[key]
        need(desc["row_schema"] == schema and desc["row_count"] == count
             and desc["ordering"] == ["candidate_key"],
             "descriptor contract:" + key)
    manifest = path.parent / "manifest.sha256"
    need(manifest.is_file() and manifest.read_bytes() == manifest_bytes(path, receipt),
         "exact manifest")
    for label, item in receipt["root_input_capture"]["attestations"].items():
        input_path = root_path(item["path"])
        info = input_path.stat()
        observed = [info.st_dev, info.st_ino, info.st_size,
                    info.st_mtime_ns, info.st_ctime_ns, info.st_mode,
                    info.st_uid, info.st_gid]
        need(fsha(input_path) == item["sha256"]
             and info.st_size == item["size"]
             and observed == item["stat_fingerprint"],
             "root input attestation:" + label)
    return receipt


def verify_run_attestation(path: Path, receipt_path: Path,
                           receipt: dict[str, Any]) -> dict[str, Any]:
    row = document(path, "run_attestation_sha256")
    run = row["run"]
    need(row["status"].startswith("PASS_NUMERIC_EXIT0_SIGNAL_NULL_STDERR_EMPTY")
         and row["runner_source_sha256"] == RUNNER_SHA
         and fsha(RUNNER) == RUNNER_SHA
         and run["numeric_exit_code"] == 0 and run["signal"] is None
         and run["stderr_empty"] is True
         and run["pre_post_sha256_identical"] is True
         and run["pre_post_stat_identical"] is True
         and run["receipt_file_sha256"] == fsha(receipt_path)
         and run["receipt_object_sha256"] == receipt["receipt_sha256"]
         and row["input_pre"] == row["input_post"],
         "run attestation")
    return row


def load_chart_maps(attest: dict[str, dict[str, Any]]) -> tuple[dict[str, str], ...]:
    r179 = json.loads(root_path(attest["R179"]["path"]).read_bytes())
    map179 = {row[0]: row[3]
              for row in r179["result"]["retained_3d_child_rows"]}
    r234 = json.loads(root_path(attest["R234"]["path"]).read_bytes())
    map234 = {row["materialized_row_id"]: row["chart"]
              for row in r234["result"]["resolved_descendant_rows"]}
    r236 = json.loads(root_path(attest["R236"]["path"]).read_bytes())
    map236 = {row["crossing_dependency_discharge_row_id"]:
              row["local_return_signature"]["source_chart"]
              for row in r236["result"]["crossing_dependency_discharge_rows"]}
    map5 = {}
    for row in raw_rows(root_path(attest["C5"]["path"])):
        semantic = row["semantic_classification"]
        if semantic["classification"] == "EMPTY_GRAPH":
            map5[row["row_sha256"]] = semantic["kernel_parameters"]["source_chart"]
    need(len(map5) == 33_344, "C5 chart census")
    return map179, map234, map236, map5


def chart_for(source: str, row: dict[str, Any],
              maps: tuple[dict[str, str], ...]) -> str:
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
    need(chart in CHARTS, "chart")
    return chart


def load_atoms(receipt: dict[str, Any]) -> list[dict[str, Any]]:
    attest = receipt["root_input_capture"]["attestations"]
    endpoint_authority = {}
    for row in raw_rows(root_path(attest["C19C_authority"]["path"])):
        endpoint_authority[row["member_id"]] = {
            "bits": tuple(row["endpoint_inclusion_bits"][name] for name in BITS),
            "sha": row["row_sha256"], "source_sha": row["C19C_row_sha256"],
            "bounds": row["bounds"], "chart": row["chart"]}
    need(len(endpoint_authority) == 33_344, "C19C endpoint authority")
    maps = load_chart_maps(attest)
    atoms = []
    owners: dict[str, set[str]] = defaultdict(set)
    endpoint_sets = [set(), set(), set()]
    for source in COUNTS:
        count = 0
        for row in raw_rows(root_path(attest[source]["path"])):
            count += 1
            owner = row.get("member_id") or row["owner_member_id"]
            embedded = (row.get("fresh_component_id")
                        or row["owner_fresh_component_id"])
            bounds = bounds_for(source, row["support_ast"])
            chart = chart_for(source, row, maps)
            if source == "C19C":
                endpoint = endpoint_authority[owner]
                need(endpoint["source_sha"] == row["row_sha256"]
                     and endpoint["bounds"] == row["support_ast"]["bounds"]
                     and endpoint["chart"] == chart, "C19C binding")
                bits, endpoint_sha = endpoint["bits"], endpoint["sha"]
            else:
                need(row["support_ast"]["kind"] == OPEN_KINDS[source],
                     "open kernel")
                bits, endpoint_sha = (False,) * 6, None
            for axis in range(3):
                endpoint_sets[axis].update(bounds[2 * axis:2 * axis + 2])
            owners[owner].add(source)
            atoms.append({"key": atom_key(source, row), "source": source,
                          "source_sha": row["row_sha256"], "owner": owner,
                          "embedded": embedded, "bounds": bounds,
                          "chart": chart, "bits": bits,
                          "endpoint_sha": endpoint_sha})
        need(count == COUNTS[source], "kernel census:" + source)
    need(len(atoms) == 483_232 and len(owners) == 482_380,
         "atom/owner census")
    c15 = {}
    components = set()
    for ordinal, row in enumerate(raw_rows(root_path(attest["C15"]["path"]))):
        need(row["member_ordinal"] == ordinal, "C15 ordinal")
        components.add(row["fresh_component_id"])
        if row["registry_member_id"] in owners:
            c15[row["registry_member_id"]] = (
                row["fresh_component_id"], row["row_sha256"])
    need(ordinal + 1 == 502_204 and len(components) == 57_876
         and set(c15) == set(owners), "C15 join")
    c25 = {}
    for ordinal, row in enumerate(raw_rows(root_path(attest["C25"]["path"]))):
        if row["member_id"] in owners:
            c25[row["member_id"]] = (row["fresh_component_id"],
                                      row["row_sha256"],
                                      row["source_bindings"]["C15_member_row_sha256"])
    need(ordinal + 1 == 502_204 and set(c25) == set(owners), "C25 join")
    atoms.sort(key=lambda atom: atom["key"])
    for atom in atoms:
        owner = atom["owner"]
        need(atom["embedded"] == c15[owner][0] == c25[owner][0]
             and c15[owner][1] == c25[owner][2], "C15/C25 binding")
        atom["component"], atom["C15_sha"] = c15[owner]
        atom["C25_sha"] = c25[owner][1]
    ranks = []
    for values in endpoint_sets:
        ordered = sorted(values, key=cmp_to_key(compare_endpoint))
        ranks.append({value: index + 1 for index, value in enumerate(ordered)})
    need([len(value) for value in ranks] == [6433, 1201, 257],
         "endpoint ranks")
    for atom in atoms:
        ranked = []
        for axis in range(3):
            ranked.extend((ranks[axis][atom["bounds"][2 * axis]],
                           ranks[axis][atom["bounds"][2 * axis + 1]]))
        atom["rank"] = tuple(ranked)
    return atoms


def exact_intersection(left: dict[str, Any], right: dict[str, Any]) -> tuple[int, list[Any], list[str], list[dict[str, Any]]]:
    dimension = 0
    wires = []
    zero_axes = []
    checks = []
    for axis in range(3):
        lower = (left["bounds"][2 * axis]
                 if compare_endpoint(left["bounds"][2 * axis],
                                     right["bounds"][2 * axis]) >= 0
                 else right["bounds"][2 * axis])
        upper = (left["bounds"][2 * axis + 1]
                 if compare_endpoint(left["bounds"][2 * axis + 1],
                                     right["bounds"][2 * axis + 1]) <= 0
                 else right["bounds"][2 * axis + 1])
        relation = compare_endpoint(lower, upper)
        need(relation <= 0, "candidate is closure contact")
        dimension += int(relation < 0)
        wires.extend((endpoint_wire(lower), endpoint_wire(upper)))
        if relation == 0:
            zero_axes.append(AXES[axis])
            if left["source"] == right["source"] == "C19C":
                lb, lc = endpoint_bit(left, axis, lower)
                rb, rc = endpoint_bit(right, axis, lower)
                checks.append({"axis": AXES[axis], "left_boundary": lb,
                               "right_boundary": rb, "left_closed": lc,
                               "right_closed": rc,
                               "both_closed": lc and rc})
    return dimension, wires, zero_axes, checks


def verify_rows(receipt: dict[str, Any], atoms: list[dict[str, Any]],
                db: sqlite3.Connection) -> dict[str, Any]:
    by_key = {atom["key"]: atom for atom in atoms}
    adapter = receipt["terminal_adapter"]
    authority = DescriptorReader(adapter["primitive_authority_ledger"])
    candidates = DescriptorReader(adapter["candidate_ownership_ledger"])
    proofs = DescriptorReader(adapter["materialized_physical_proof_fragment_ledger"])
    db.execute("CREATE TABLE remaining(key BLOB PRIMARY KEY,dimension INTEGER NOT NULL,seen INTEGER NOT NULL DEFAULT 0) WITHOUT ROWID")
    batch = []
    dimensions = Counter()
    relations = Counter()
    dispositions = Counter()
    lower_open = lower_c19c = lower_legal = 0
    proof_count = 0
    edges = set()
    previous = None
    for ordinal in range(5_970_840):
        observed_authority = authority.next()
        observed_candidate = candidates.next()
        key = observed_authority["candidate_key"]
        need(key == observed_candidate["candidate_key"]
             and (previous is None or previous < key)
             and key.startswith(PAIR_PREFIX), "joint candidate ordering")
        previous = key
        atom_keys = observed_authority["ordered_primitive_support_atom_keys"]
        need(type(atom_keys) is list and len(atom_keys) == 2
             and atom_keys[0] < atom_keys[1]
             and all(item in by_key for item in atom_keys), "authority atom pair")
        left, right = by_key[atom_keys[0]], by_key[atom_keys[1]]
        key_digest = hashlib.sha256(canonical(atom_keys)).digest()
        need(key == PAIR_PREFIX + key_digest.hex(), "candidate key recomputation")
        dimension, wires, zero_axes, checks = exact_intersection(left, right)
        member_pair = sorted((left["owner"], right["owner"]))
        component_pair = sorted((left["component"], right["component"]))
        component_relation = ("SAME_C15_COMPONENT"
                              if component_pair[0] == component_pair[1]
                              else "CROSS_C15_COMPONENT")
        source_pair = sorted((left["source"], right["source"]))
        witness_sha = digest(wires)
        if dimension == 3:
            endpoint_policy = "STRICT_POSITIVE_WIDTH_IN_ALL_THREE_AXES__ENDPOINT_BITS_IRRELEVANT"
            lower_disposition = None
        elif source_pair == ["C19C", "C19C"]:
            lower_c19c += 1
            legal = all(check["both_closed"] for check in checks)
            lower_legal += int(legal and component_relation == "CROSS_C15_COMPONENT")
            need(not legal, "C19C lower rejection")
            endpoint_policy = "C19C_V3_PRODUCT_ENDPOINT_AUTHORITY__AT_LEAST_ONE_ZERO_AXIS_NOT_DOUBLE_INCLUDED"
            lower_disposition = "REJECT_ZERO_WIDTH_C19C_PRODUCT_ENDPOINT_POLICY"
        else:
            lower_open += 1
            endpoint_policy = "AT_LEAST_ONE_FULLY_OPEN_PRIMITIVE_KERNEL_REJECTS_ZERO_WIDTH_CONTACT"
            lower_disposition = "REJECT_ZERO_WIDTH_FULLY_OPEN_KERNEL"
        expected_authority = close({
            "schema": AUTHORITY_SCHEMA, "ordinal": ordinal,
            "candidate_key": key,
            "ordered_primitive_support_atom_keys": atom_keys,
            "ordered_primitive_source_row_sha256": [left["source_sha"],
                                                     right["source_sha"]],
            "ordered_C15_member_pair": member_pair,
            "ordered_C15_component_pair": component_pair,
            "ordered_C15_member_row_sha256": sorted((left["C15_sha"],
                                                       right["C15_sha"])),
            "ordered_C25_member_row_sha256": sorted((left["C25_sha"],
                                                       right["C25_sha"])),
            "chart": left["chart"], "source_pair": source_pair,
            "intersection_dimension": dimension,
            "component_relation": component_relation,
            "zero_width_axes": zero_axes,
            "exact_intersection_witness_sha256": witness_sha,
            "endpoint_contact_policy": endpoint_policy,
            "C19C_endpoint_authority_row_sha256": sorted(
                item for item in (left["endpoint_sha"], right["endpoint_sha"])
                if item is not None),
            "C19C_zero_axis_endpoint_checks": checks,
            "lower_dimensional_disposition_or_null": lower_disposition,
            "C26_no_new_geometry_receipt_sha256": C26_RECEIPT_OBJECT,
            "G2A_scoped_alias_receipt_sha256": G2A_RECEIPT_OBJECT,
            "formal_credit": 0,
        })
        need(observed_authority == expected_authority,
             "inverse primitive authority row")
        is_cross_strict = dimension == 3 and component_relation == "CROSS_C15_COMPONENT"
        proof_sequence = EMPTY_SHA
        if is_cross_strict:
            witness_key = "same-chart-strict-volume:" + digest([
                key, atom_keys, witness_sha])
            edge_key = EDGE_PREFIX + digest(component_pair)
            proof_key = PROOF_PREFIX + digest([
                key, witness_key, member_pair, component_pair])
            expected_proof = close({
                "schema": PROOF_SCHEMA, "ordinal": proof_count,
                "proof_row_key": proof_key, "candidate_key": key,
                "atom_pair_incidence_key_or_null": None,
                "terminal": T00, "authority_slot": SLOT,
                "primitive_authority_row_sha256":
                    expected_authority["row_sha256"],
                "ordered_C15_member_pair": member_pair,
                "ordered_C15_component_pair": component_pair,
                "component_edge_key": edge_key,
                "physical_witness_key": witness_key, "formal_credit": 0})
            need(proofs.next() == expected_proof, "inverse physical proof row")
            proof_sequence = hashlib.sha256(
                expected_proof["row_sha256"].encode("ascii") + b"\n").hexdigest()
            proof_count += 1
            edges.add(edge_key)
            disposition = "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED"
        elif dimension < 3:
            disposition = "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"
        else:
            disposition = "SAME_FROZEN_C15_COMPONENT__NO_EDGE"
        expected_candidate = close({
            "schema": CANDIDATE_SCHEMA, "ordinal": ordinal,
            "candidate_key": key,
            "candidate_kind": "SAME_CHART_EXACT_CONTACT_CANDIDATE",
            "candidate_pair_key_or_null": key,
            "terminal_ordinal": 0, "terminal": T00,
            "authority_slot": SLOT,
            "primitive_authority_row_sha256": expected_authority["row_sha256"],
            "component_relation_disposition": disposition,
            "physical_proof_row_count": int(is_cross_strict),
            "physical_proof_row_sequence_sha256": proof_sequence,
            "formal_credit": 0})
        need(observed_candidate == expected_candidate,
             "inverse candidate ownership row")
        dimensions[dimension] += 1
        relations[(dimension, component_relation)] += 1
        dispositions[disposition] += 1
        batch.append((key_digest, dimension))
        if len(batch) >= 20_000:
            db.executemany("INSERT INTO remaining(key,dimension) VALUES(?,?)", batch)
            batch.clear()
    if batch:
        db.executemany("INSERT INTO remaining(key,dimension) VALUES(?,?)", batch)
    db.commit()
    authority.finish()
    candidates.finish()
    proofs.finish()
    need(dict(dimensions) == EXPECTED_DIMENSIONS
         and dict(relations) == EXPECTED_RELATIONS,
         "inverse dimension/relation census")
    need(lower_open == 5_707_708 and lower_c19c == 76_000
         and lower_legal == 0 and proof_count == 32_240
         and len(edges) == 14_772,
         "inverse endpoint/proof census")
    need(dispositions == {
        "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 32_240,
        "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 5_783_708,
        "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 154_892},
         "inverse disposition census")
    return {"dimensions": dimensions, "relations": relations,
            "proof_count": proof_count, "edges": len(edges)}


def independent_exhaustion(atoms: list[dict[str, Any]],
                           db: sqlite3.Connection) -> dict[str, Any]:
    tables = {chart: "verify_box_" + chart[-1].lower() for chart in CHARTS}
    for table in tables.values():
        db.execute(f"CREATE VIRTUAL TABLE {table} USING rtree_i32(id,t0,t1,p0,p1,s0,s1)")
    query = "SELECT id FROM {table} WHERE t0<=? AND t1>=? AND p0<=? AND p1>=? AND s0<=? AND s1>=?"
    cursor = db.cursor()
    counts = Counter()
    relations = Counter()
    deletion_batch = []
    # Reverse atom order is independent of both producer random permutations.
    for atom_index in range(len(atoms) - 1, -1, -1):
        atom = atoms[atom_index]
        rb = atom["rank"]
        table = tables[atom["chart"]]
        for (other_id,) in cursor.execute(query.format(table=table),
                                          (rb[1], rb[0], rb[3], rb[2],
                                           rb[5], rb[4])):
            other = atoms[other_id - 1]
            left, right = sorted((atom, other), key=lambda item: item["key"])
            dimension, _, _, _ = exact_intersection(left, right)
            key = hashlib.sha256(canonical([left["key"], right["key"]])).digest()
            component_relation = ("SAME_C15_COMPONENT"
                                  if left["component"] == right["component"]
                                  else "CROSS_C15_COMPONENT")
            counts[dimension] += 1
            relations[(dimension, component_relation)] += 1
            deletion_batch.append((key, dimension))
            if len(deletion_batch) >= 20_000:
                before = db.total_changes
                db.executemany("UPDATE remaining SET seen=1 WHERE key=? AND dimension=? AND seen=0",
                               deletion_batch)
                need(db.total_changes - before == len(deletion_batch),
                     "independent candidate exact membership")
                deletion_batch.clear()
        cursor.execute(f"INSERT INTO {table} VALUES(?,?,?,?,?,?,?)",
                       (atom_index + 1, *rb))
    if deletion_batch:
        before = db.total_changes
        db.executemany("UPDATE remaining SET seen=1 WHERE key=? AND dimension=? AND seen=0",
                       deletion_batch)
        need(db.total_changes - before == len(deletion_batch),
             "final independent membership")
    db.commit()
    remaining = db.execute("SELECT count(*) FROM remaining WHERE seen=0").fetchone()[0]
    total = db.execute("SELECT count(*) FROM remaining").fetchone()[0]
    need(total == 5_970_840 and remaining == 0
         and dict(counts) == EXPECTED_DIMENSIONS
         and dict(relations) == EXPECTED_RELATIONS,
         "independent complete exhaustion")
    return {"independently_enumerated_candidate_count": sum(counts.values()),
            "observed_unmatched_candidate_count": remaining,
            "dimension_census": {str(key): counts[key] for key in sorted(counts)}}


def verify(receipt_path: Path, second_path: Path,
           run_path: Path, second_run_path: Path,
           temporary_db: Path) -> dict[str, Any]:
    first = verify_receipt_shell(receipt_path)
    second = verify_receipt_shell(second_path)
    run1 = verify_run_attestation(run_path, receipt_path, first)
    run2 = verify_run_attestation(second_run_path, second_path, second)
    need(first["execution_seed"] != second["execution_seed"]
         and first["exact_census"] == second["exact_census"],
         "distinct dual seeds")
    dual_count = 0
    for key in ("primitive_authority_ledger", "candidate_ownership_ledger",
                "materialized_physical_proof_fragment_ledger"):
        a, b = first["terminal_adapter"][key], second["terminal_adapter"][key]
        need(a["sha256"] == b["sha256"]
             and byte_identical(root_path(a["path"]), root_path(b["path"])),
             "dual-seed ledger byte identity:" + key)
        dual_count += 1
    need(not temporary_db.exists(), "fresh verifier database")
    temporary_db.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(temporary_db)
    try:
        db.execute("PRAGMA journal_mode=OFF")
        db.execute("PRAGMA synchronous=OFF")
        db.execute("PRAGMA temp_store=FILE")
        db.execute("PRAGMA cache_size=-262144")
        atoms = load_atoms(first)
        inverse = verify_rows(first, atoms, db)
        exhaustive = independent_exhaustion(atoms, db)
    finally:
        db.close()
    temporary_db.unlink()
    stable = {
        "candidate_count": 5_970_840,
        "lower_cross_component_candidate_count": 2_598_666,
        "lower_same_component_candidate_count": 3_185_042,
        "physical_proof_count": inverse["proof_count"],
        "unique_component_edge_count": inverse["edges"],
        "dual_seed_byte_identical_ledger_count": dual_count,
        **exhaustive,
    }
    body = {
        "schema": "cm2.c27-independent.primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-independent-verification.v1",
        "status": "PASS_NO_PRODUCER_IMPORT_ROW_INVERSE_AND_INDEPENDENT_COMPLETE_ENUMERATION__DUAL_SEED_BYTE_IDENTICAL__ZERO_CREDIT",
        "receipt_file_sha256": fsha(receipt_path),
        "receipt_object_sha256": first["receipt_sha256"],
        "second_receipt_file_sha256": fsha(second_path),
        "second_receipt_object_sha256": second["receipt_sha256"],
        "run_attestation_objects": [run1["run_attestation_sha256"],
                                    run2["run_attestation_sha256"]],
        "producer_imported": False,
        "verification_method": {
            "all_authority_candidate_and_proof_rows_reconstructed": True,
            "independent_reverse_order_Rtree_enumeration": True,
            "observed_key_table_exactly_exhausted": True,
            "C26_and_G2A_add_no_candidate": True,
        },
        "exact_census": stable,
        "formal_credit": 0, "manifest_authorized": False,
        "C27_C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        "verifier_source_sha256": fsha(Path(__file__).resolve()),
    }
    result = dict(body)
    result["verification_sha256"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--second-receipt", required=True)
    parser.add_argument("--run-attestation", required=True)
    parser.add_argument("--second-run-attestation", required=True)
    parser.add_argument("--temporary-db", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    try:
        need(not output.exists(), "fresh verification output")
        result = verify(Path(args.receipt).resolve(),
                        Path(args.second_receipt).resolve(),
                        Path(args.run_attestation).resolve(),
                        Path(args.second_run_attestation).resolve(),
                        Path(args.temporary_db).resolve())
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(canonical(result) + b"\n")
    except (Failure, KeyError, TypeError, ValueError, OSError,
            sqlite3.Error, json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "exact_census": result["exact_census"],
                     "verification_sha256": result["verification_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
