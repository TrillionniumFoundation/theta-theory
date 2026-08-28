#!/usr/bin/env python3
"""Fresh corrected-v2 T00 SAME_CHART exact-contact authority adapter.

The 5,970,840 candidate-pair universe is freshly enumerated from the six
primitive support kernels in four charts.  It is the disjoint union of
187,132 strict three-dimensional intersections and 5,783,708 lower-
dimensional closure contacts.  C26's sealed no-new-geometry theorem and the
sealed G2A alias scope are consumed as theorems; neither adds a candidate.

Only the 32,240 strict cross-C15-component candidates emit physical proofs.
All 5,783,708 lower-dimensional candidates emit no edge: 5,707,708 involve a
fully open kernel, while all 76,000 C19C/C19C endpoint-dependent contacts are
rejected by the row-level endpoint ownership product rule.

No C27 FAMILIES, transition ledger, C28, C29, or historical edge ledger is
opened.  A seed randomizes R-tree insertion only; SQLite key ordering makes
all emitted ledgers deterministic across seeds.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from functools import cmp_to_key
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import random
import sqlite3
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
T00 = "SAME_CHART_RELATIVE_CELLS"
SLOT = "T00_SAME_CHART_RELATIVE_CELLS"
CANDIDATE_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
PROOF_SCHEMA = "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2"
AUTHORITY_SCHEMA = "cm2.c27-independent.primitive-v5-actual.t00-same-chart-exact-contact-authority.row.v2"
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
KERNEL = {"C19A": "C19A", "C19B": "C19B", "C19C": "C19C",
          "C20A": "C20A", "C22A": "C22B", "C23A": "C23B"}
OPEN_KINDS = {
    "C19A": "OPEN_RATIONAL_BOX", "C19B": "OPEN_RATIONAL_BOX",
    "C20A": "OPEN_RATIONAL_BOX", "C22A": "OPEN_RATIONAL_BOX",
    "C23A": "T2PS_BRANCH_OPEN_RATIONAL_BOX",
}
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

FILES = {
    "interface_v2": (".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json", "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6"),
    "C15": ("deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz", "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    "C25": ("deliverables/cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz", "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6"),
    "C19A": ("deliverables/cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz", "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3"),
    "C19B": ("deliverables/cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz", "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798"),
    "C19C": ("deliverables/cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz", "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84"),
    "C20A": ("deliverables/cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz", "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922"),
    "C22A": ("deliverables/cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz", "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb"),
    "C23A": ("deliverables/cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz", "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528"),
    "R179": ("deliverables/cm2_round179_source_g_residual_tube_arrangement_rows.json", "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),
    "R234": ("deliverables/cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    "R236": ("deliverables/cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    "C5": ("deliverables/cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz", "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
    "C19C_manifest": ("deliverables/cm2_c19c_endpoint_ownership_v3_manifest.sha256", "14643e303aee7a3bac27342204ee92f2420ae855a5df66916307680721c82929"),
    "C19C_receipt": ("deliverables/cm2_c19c_endpoint_ownership_v3_terminal_receipt.json", "c620034783676f20d99e3f9a600cfe9b3e22a48129cd2f0555479d5b6c25e63b"),
    "C19C_authority": ("deliverables/cm2_c19c_endpoint_ownership_v3_authority_ledger.jsonl.gz", "77b220d803b64066a09a0172e06f53f0ddc7a229d208cb7248c2293f493f3166"),
    "C19C_cold": ("deliverables/cm2_c19c_endpoint_ownership_v3_postpublication_cold_replay_receipt.json", "17236dac0b9cf04d0d4e50bba1072fc90b2e87f732cdfa6d802f411facc6930d"),
    "C26_receipt": (".cm2-runtime/audit/c26-no-new-geometry-from-feature-rows-v1-zero-credit-seal-final/receipt.json", "be0cc715427bd9ee4792ad536a1bfab1f23db8de204ddf9fb9a24c745aa05cb7"),
    "C26_replay": (".cm2-runtime/audit/c26-no-new-geometry-from-feature-rows-v1-zero-credit-seal-final-terminal-replay/terminal_replay.json", "94bdcb59bbeba4d894a80c00345a27e9cf236354905ca40505336498726b4ad2"),
    "G2A_receipt": (".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2/receipt.json", "acb9b25d309efbf52026bacbb5208aa2775b4e4c5c98fcca30c7ed7ce42585b5"),
    "G2A_replay": (".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2-terminal-replay/terminal_replay.json", "aa95ca037c16d444a3e51e815afb9028489266b444da0582405029dc43cce2d7"),
}


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
    need("row_sha256" not in body, "fresh row")
    return {**body, "row_sha256": digest(body)}


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def fp(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid)


@dataclass
class Capture:
    label: str
    path: Path
    fd: int
    initial: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, relative: str, expected: str) -> "Capture":
        path = (ROOT / relative).resolve()
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                     | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            need(observed == expected, label + ":sha256")
            need(fp(os.fstat(fd)) == fp(before), label + ":hash-fstat")
            return cls(label, path, fd, fp(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def stable(self, phase: str) -> None:
        need(fp(os.fstat(self.fd)) == self.initial,
             self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        self.stable("raw")
        return b"".join(pieces)

    def json(self) -> dict[str, Any]:
        value = json.loads(self.raw())
        need(type(value) is dict, self.label + ":JSON object")
        return value

    def document(self, closure: str) -> dict[str, Any]:
        value = self.json()
        body = dict(value)
        claim = body.pop(closure, None)
        need(type(claim) is str and claim == digest(body),
             self.label + ":closure")
        return value

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"),
                         f"{self.label}:{ordinal}:newline")
                    payload = line[:-1]
                    row = json.loads(payload)
                    need(type(row) is dict and canonical(row) == payload,
                         f"{self.label}:{ordinal}:canonical")
                    body = dict(row)
                    claim = body.pop("row_sha256", None)
                    need(type(claim) is str and claim == digest(body),
                         f"{self.label}:{ordinal}:closure")
                    yield row
        self.stable("rows")

    def attestation(self) -> dict[str, Any]:
        self.stable("attestation")
        return {"path": str(self.path.relative_to(ROOT)),
                "size": self.initial[2], "sha256": self.sha256,
                "stat_fingerprint": list(self.initial), "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


class RowWriter:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.open("xb")
        self.stream = gzip.GzipFile(filename="", fileobj=self.raw,
                                    mode="wb", mtime=0, compresslevel=1)
        self.count = 0
        self.sequence = hashlib.sha256()

    def write(self, row: dict[str, Any]) -> None:
        # ``close`` computes the closure immediately before this call.  Avoid
        # a second full canonicalization/hash for each of 11,973,920 emitted
        # rows; the independent verifier replays every closure from bytes.
        claim = row.get("row_sha256")
        need(type(claim) is str and len(claim) == 64,
             self.path.name + ":closed row")
        self.stream.write(canonical(row) + b"\n")
        self.sequence.update(claim.encode("ascii") + b"\n")
        self.count += 1

    def finish(self, schema: str, unique_key: str,
               ordering: list[str]) -> dict[str, Any]:
        self.stream.close()
        self.raw.close()
        return {"path": str(self.path.relative_to(ROOT)),
                "size": self.path.stat().st_size,
                "sha256": file_sha(self.path), "row_count": self.count,
                "row_sequence_sha256": self.sequence.hexdigest(),
                "row_schema": schema, "unique_key": unique_key,
                "ordering": ordering}


Endpoint = tuple[Any, ...]


def q_endpoint(value: str) -> Endpoint:
    return (0, Fraction(value))


def sqrt_endpoint(value: str, sign: int) -> Endpoint:
    radicand = Fraction(value)
    need(radicand >= 0 and sign in {-1, 1}, "signed sqrt domain")
    a, b = math.isqrt(radicand.numerator), math.isqrt(radicand.denominator)
    if a * a == radicand.numerator and b * b == radicand.denominator:
        return (0, Fraction(sign * a, b))
    return (1, radicand, sign)


def compare_endpoint(left: Endpoint, right: Endpoint) -> int:
    if left == right:
        return 0
    if left[0] == right[0] == 0:
        return -1 if left[1] < right[1] else 1
    if left[0] == right[0] == 1:
        lq, ls, rq, rs = left[1], left[2], right[1], right[2]
        if ls != rs:
            return -1 if ls < rs else 1
        result = -1 if lq < rq else 1
        return result if ls == 1 else -result
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


def normalized_bounds(source: str, support: dict[str, Any]) -> tuple[Endpoint, ...]:
    raw = support.get("bounds")
    need(type(raw) is list and len(raw) == 6
         and all(type(item) is str for item in raw), "six bounds:" + source)
    if source != "C23A":
        need(support.get("coordinates") == ["t", "p", "s"],
             "physical coordinates:" + source)
        result = tuple(q_endpoint(item) for item in raw)
    else:
        need(support.get("kind") == "T2PS_BRANCH_OPEN_RATIONAL_BOX",
             "C23 support kind")
        sign = support.get("physical_t_sign")
        need(sign in {-1, 1}, "C23 sign")
        t0, t1 = ((sqrt_endpoint(raw[0], 1), sqrt_endpoint(raw[1], 1))
                  if sign == 1 else
                  (sqrt_endpoint(raw[1], -1), sqrt_endpoint(raw[0], -1)))
        result = (t0, t1, q_endpoint(raw[2]), q_endpoint(raw[3]),
                  q_endpoint(raw[4]), q_endpoint(raw[5]))
    need(all(compare_endpoint(result[2 * axis], result[2 * axis + 1]) < 0
             for axis in range(3)), "positive widths:" + source)
    return result


def atom_id(source: str, row: dict[str, Any]) -> str:
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
    need(compare_endpoint(coordinate, upper) == 0,
         "zero contact at endpoint")
    return "UPPER", atom["bits"][2 * axis + 1]


def load_chart_maps(captures: dict[str, Capture]) -> tuple[dict[str, str], ...]:
    r179_doc = captures["R179"].json()
    r179 = {row[0]: row[3]
            for row in r179_doc["result"]["retained_3d_child_rows"]}
    r234_doc = captures["R234"].json()
    r234 = {row["materialized_row_id"]: row["chart"]
            for row in r234_doc["result"]["resolved_descendant_rows"]}
    r236_doc = captures["R236"].json()
    r236 = {row["crossing_dependency_discharge_row_id"]:
            row["local_return_signature"]["source_chart"]
            for row in r236_doc["result"]["crossing_dependency_discharge_rows"]}
    c5 = {}
    for row in captures["C5"].rows():
        semantic = row["semantic_classification"]
        if semantic["classification"] == "EMPTY_GRAPH":
            c5[row["row_sha256"]] = semantic["kernel_parameters"]["source_chart"]
    need(len(c5) == 33_344, "C5 chart census")
    return r179, r234, r236, c5


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
        need(source == "C23A", "known source")
        chart = row["support_ast"]["recharted_target_chart"]
    need(chart in CHARTS, "four charts")
    return chart


def validate_formal_receipts(captures: dict[str, Capture]) -> tuple[str, str, str]:
    interface = captures["interface_v2"].document("preflight_sha256")
    need(interface["corrected_interface"]["terminal_order"][0] == T00
         and interface["corrected_interface"]["authority_slot_order"][0] == SLOT,
         "corrected T00 terminal/slot")
    t00 = interface["corrected_interface"]["candidate_ownership_ledger"]["T00_rule"]
    need(t00["candidate_count"] == 5_970_840
         and t00["strict_volume_candidates"] == 187_132
         and t00["lower_dimensional_candidates"] == 5_783_708
         and t00["strict_and_lower_disjoint_complete_union"] is True
         and t00["C26_691424_is_absence_coverage_theorem_not_candidate_rows"] is True
         and t00["G2A_G2B_alias_adds_T00_candidate"] is False,
         "corrected T00 interface")
    c19 = captures["C19C_receipt"].document("receipt_sha256")
    cold = captures["C19C_cold"].document("receipt_sha256")
    need(c19["formal_credit"] == 0
         and c19["authority"]["closed_physical_outer_rule"]
            == "both p endpoints and both s endpoints included"
         and cold["pre_post_sha256_identical"] is True
         and cold["pre_post_stat_identical"] is True
         and cold["formal_credit"] == 0
         and cold["base_manifest"]["sha256"]
            == captures["C19C_manifest"].sha256
         and cold["base_manifest"]["members"][
             "cm2_c19c_endpoint_ownership_v3_authority_ledger.jsonl.gz"]
            == captures["C19C_authority"].sha256,
         "C19C sealed endpoint authority")
    c26 = captures["C26_receipt"].document("receipt_sha256")
    c26_replay = captures["C26_replay"].document("result_sha256")
    need(c26["schema"] == "cm2.c26-independent.no-new-geometry-from-c26-feature-rows-zero-credit-receipt.v1"
         and c26["headline"]["C26_feature_rows"] == 691_424
         and c26["headline"]["C26_direct_support_carriers"] == 0
         and c26["headline"]["same_chart_lower_dim012_pairs"] == 5_783_708
         and c26["headline"]["same_chart_lower_legal_witnesses"] == 0
         and c26["authority_scope"]["NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS"] is True
         and c26["authority_scope"]["fills_v5_C26_absence_slot"] is True
         and c26["authority_scope"]["C26_absence_used_as_negative_geometry_theorem"] is False
         and c26["formal_credit"] == 0 and c26["manifest_authorized"] is False
         and c26_replay["receipt_file_sha256"] == captures["C26_receipt"].sha256
         and c26_replay["receipt_sha256"] == c26["receipt_sha256"]
         and c26_replay["formal_credit"] == 0,
         "C26 no-new-geometry formal authority")
    g2a = captures["G2A_receipt"].document("result_sha256")
    g2a_replay = captures["G2A_replay"].document("result_sha256")
    need(g2a["schema"] == "cm2.c27-independent.g2a-relative2d-primitive-totality-zero-credit-receipt.v2"
         and g2a["headline"]["contact_aliases"] == 9_408
         and g2a["headline"]["scoped_unique_routes"] == 5_264
         and g2a["authority_scope"]["scoped_G2A_route_assignment"] is True
         and g2a["authority_scope"]["global_three_terminal_unique_assignment"] is False
         and g2a["formal_credit"] == 0 and g2a["manifest_authorized"] is False
         and g2a_replay["payload_manifest_file_sha256"]
            == g2a["payload_manifest"]["file_sha256"]
         and g2a_replay["formal_credit"] == 0,
         "G2A scoped alias authority")
    return c26["receipt_sha256"], g2a["result_sha256"], interface["preflight_sha256"]


def build(out_dir: Path, seed: int) -> dict[str, Any]:
    need(type(seed) is int and seed > 0, "positive seed")
    need(not out_dir.exists(), "fresh output")
    captures: dict[str, Capture] = {}
    writers: list[RowWriter] = []
    db: sqlite3.Connection | None = None
    db_path = out_dir / "temporary_exact_contact_sort.sqlite"
    try:
        for label, (path, pin) in FILES.items():
            captures[label] = Capture.open(label, path, pin)
        c26_receipt_sha, g2a_receipt_sha, interface_sha = validate_formal_receipts(captures)
        authority: dict[str, dict[str, Any]] = {}
        for row in captures["C19C_authority"].rows():
            member = row["member_id"]
            need(member not in authority and set(row["endpoint_inclusion_bits"]) == set(BITS),
                 "C19C endpoint row")
            authority[member] = {
                "bits": tuple(row["endpoint_inclusion_bits"][name]
                              for name in BITS),
                "row_sha256": row["row_sha256"],
                "C19C_row_sha256": row["C19C_row_sha256"],
                "bounds": row["bounds"], "chart": row["chart"],
            }
        need(len(authority) == 33_344, "C19C authority census")

        maps = load_chart_maps(captures)
        atoms: list[dict[str, Any]] = []
        owners: dict[str, set[str]] = defaultdict(set)
        endpoints = [set(), set(), set()]
        atom_keys = set()
        for source in COUNTS:
            count = 0
            for row in captures[source].rows():
                count += 1
                owner = row.get("member_id") or row["owner_member_id"]
                embedded_component = (row.get("fresh_component_id")
                                      or row["owner_fresh_component_id"])
                key = atom_id(source, row)
                need(key not in atom_keys, "atom key uniqueness")
                atom_keys.add(key)
                bounds = normalized_bounds(source, row["support_ast"])
                chart = chart_for(source, row, maps)
                if source == "C19C":
                    endpoint = authority[owner]
                    need(endpoint["C19C_row_sha256"] == row["row_sha256"]
                         and endpoint["bounds"] == row["support_ast"]["bounds"]
                         and endpoint["chart"] == chart,
                         "C19C endpoint/source/chart binding")
                    bits = endpoint["bits"]
                    endpoint_sha = endpoint["row_sha256"]
                else:
                    need(row["support_ast"]["kind"] == OPEN_KINDS[source],
                         "fully open kernel:" + source)
                    bits, endpoint_sha = (False,) * 6, None
                for axis in range(3):
                    endpoints[axis].update(bounds[2 * axis:2 * axis + 2])
                owners[owner].add(source)
                atoms.append({"key": key, "source": source,
                              "source_sha": row["row_sha256"],
                              "owner": owner,
                              "embedded_component": embedded_component,
                              "chart": chart, "bounds": bounds,
                              "bits": bits, "endpoint_sha": endpoint_sha})
            need(count == COUNTS[source], "source census:" + source)
        need(len(atoms) == 483_232 and len(owners) == 482_380,
             "atom/owner census")
        atoms.sort(key=lambda atom: atom["key"])

        c15 = {}
        component_set = set()
        for ordinal, row in enumerate(captures["C15"].rows()):
            need(row["member_ordinal"] == ordinal, "C15 ordinal")
            component_set.add(row["fresh_component_id"])
            member = row["registry_member_id"]
            if member in owners:
                need(member not in c15, "C15 owner uniqueness")
                c15[member] = (row["fresh_component_id"], row["row_sha256"])
        need(ordinal + 1 == 502_204 and len(component_set) == 57_876
             and set(c15) == set(owners), "C15 complete join")
        c25 = {}
        for ordinal, row in enumerate(captures["C25"].rows()):
            member = row["member_id"]
            if member in owners:
                need(member not in c25, "C25 owner uniqueness")
                bindings = row["source_bindings"]
                c25[member] = (row["fresh_component_id"], row["row_sha256"],
                               bindings["support_kernel"],
                               bindings["C15_member_row_sha256"])
        need(ordinal + 1 == 502_204 and set(c25) == set(owners),
             "C25 complete join")
        for atom in atoms:
            owner = atom["owner"]
            expected = {KERNEL[source] for source in owners[owner]}
            need(len(expected) == 1
                 and atom["embedded_component"] == c15[owner][0] == c25[owner][0]
                 and c15[owner][1] == c25[owner][3]
                 and c25[owner][2] == next(iter(expected)),
                 "primitive/C15/C25 exact join")
            atom["component"], atom["C15_sha"] = c15[owner]
            atom["C25_sha"] = c25[owner][1]

        ranks = []
        for values in endpoints:
            ordered = sorted(values, key=cmp_to_key(compare_endpoint))
            need(all(compare_endpoint(a, b) < 0
                     for a, b in zip(ordered, ordered[1:])),
                 "endpoint strict ranking")
            ranks.append({value: index + 1 for index, value in enumerate(ordered)})
        need([len(value) for value in ranks] == [6433, 1201, 257],
             "endpoint rank census")
        for atom in atoms:
            ranked = []
            for axis in range(3):
                ranked.extend((ranks[axis][atom["bounds"][2 * axis]],
                               ranks[axis][atom["bounds"][2 * axis + 1]]))
            atom["rank"] = tuple(ranked)

        out_dir.mkdir(parents=True)
        db = sqlite3.connect(db_path)
        db.execute("PRAGMA journal_mode=OFF")
        db.execute("PRAGMA synchronous=OFF")
        db.execute("PRAGMA temp_store=FILE")
        db.execute("PRAGMA cache_size=-262144")
        tables = {chart: "box_" + chart[-1].lower() for chart in CHARTS}
        for table in tables.values():
            db.execute(f"CREATE VIRTUAL TABLE {table} USING rtree_i32(id,t0,t1,p0,p1,s0,s1)")
        db.execute("CREATE TABLE candidates(key BLOB PRIMARY KEY,left_id INTEGER NOT NULL,right_id INTEGER NOT NULL,dimension INTEGER NOT NULL) WITHOUT ROWID")
        query = "SELECT id FROM {table} WHERE t0<=? AND t1>=? AND p0<=? AND p1>=? AND s0<=? AND s1>=?"
        order = list(range(len(atoms)))
        random.Random(seed).shuffle(order)
        cursor = db.cursor()
        dimensions = Counter()
        relations = Counter()
        source_dimension = Counter()
        batch = []
        for processed, atom_index in enumerate(order, 1):
            atom = atoms[atom_index]
            rb = atom["rank"]
            table = tables[atom["chart"]]
            for (old_id,) in cursor.execute(query.format(table=table),
                                            (rb[1], rb[0], rb[3], rb[2],
                                             rb[5], rb[4])):
                other_index = old_id - 1
                other = atoms[other_index]
                dimension = 0
                for axis in range(3):
                    lower = (atom["bounds"][2 * axis]
                             if compare_endpoint(atom["bounds"][2 * axis],
                                                 other["bounds"][2 * axis]) >= 0
                             else other["bounds"][2 * axis])
                    upper = (atom["bounds"][2 * axis + 1]
                             if compare_endpoint(atom["bounds"][2 * axis + 1],
                                                 other["bounds"][2 * axis + 1]) <= 0
                             else other["bounds"][2 * axis + 1])
                    relation = compare_endpoint(lower, upper)
                    need(relation <= 0, "Rtree closure false positive")
                    dimension += int(relation < 0)
                left_id, right_id = sorted((atom_index, other_index))
                left, right = atoms[left_id], atoms[right_id]
                key = hashlib.sha256(canonical([left["key"], right["key"]])).digest()
                component_relation = ("SAME_C15_COMPONENT"
                                      if left["component"] == right["component"]
                                      else "CROSS_C15_COMPONENT")
                source_pair = "__".join(sorted((left["source"], right["source"])))
                dimensions[dimension] += 1
                relations[(dimension, component_relation)] += 1
                source_dimension[(dimension, source_pair, component_relation)] += 1
                batch.append((key, left_id, right_id, dimension))
                if len(batch) >= 20_000:
                    db.executemany("INSERT INTO candidates VALUES(?,?,?,?)", batch)
                    batch.clear()
            cursor.execute(f"INSERT INTO {table} VALUES(?,?,?,?,?,?,?)",
                           (atom_index + 1, *rb))
            if processed % 100_000 == 0:
                if batch:
                    db.executemany("INSERT INTO candidates VALUES(?,?,?,?)", batch)
                    batch.clear()
                db.commit()
        if batch:
            db.executemany("INSERT INTO candidates VALUES(?,?,?,?)", batch)
        db.commit()
        need(dict(dimensions) == EXPECTED_DIMENSIONS,
             "complete dimension census")
        need(dict(relations) == EXPECTED_RELATIONS,
             "complete dimension/component census")
        need(sum(dimensions.values()) == 5_970_840
             and sum(dimensions[d] for d in (0, 1, 2)) == 5_783_708,
             "T00 totality census")

        authority_writer = RowWriter(out_dir / "T00_same_chart_exact_contact_primitive_authority.jsonl.gz")
        candidate_writer = RowWriter(out_dir / "T00_SAME_CHART_RELATIVE_CELLS_candidate_ownership.jsonl.gz")
        proof_writer = RowWriter(out_dir / "T00_SAME_CHART_RELATIVE_CELLS_physical_proof_fragment.jsonl.gz")
        writers.extend((authority_writer, candidate_writer, proof_writer))
        lower_open = lower_c19c = lower_legal = 0
        disposition_census = Counter()
        proof_edges = set()
        proof_count = 0
        previous_key = None
        select = db.execute("SELECT key,left_id,right_id,dimension FROM candidates ORDER BY key")
        for ordinal, (key_bytes, left_id, right_id, stored_dimension) in enumerate(select):
            need(previous_key is None or previous_key < key_bytes,
                 "candidate key strict ordering")
            previous_key = key_bytes
            left, right = atoms[left_id], atoms[right_id]
            candidate_key = PAIR_PREFIX + bytes(key_bytes).hex()
            intersections = []
            zero_axes = []
            endpoint_checks = []
            dimension = 0
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
                need(relation <= 0, "exact intersection")
                dimension += int(relation < 0)
                intersections.extend((endpoint_wire(lower), endpoint_wire(upper)))
                if relation == 0:
                    zero_axes.append(AXES[axis])
                    if left["source"] == right["source"] == "C19C":
                        lb, lc = endpoint_bit(left, axis, lower)
                        rbnd, rc = endpoint_bit(right, axis, lower)
                        endpoint_checks.append({"axis": AXES[axis],
                                                "left_boundary": lb,
                                                "right_boundary": rbnd,
                                                "left_closed": lc,
                                                "right_closed": rc,
                                                "both_closed": lc and rc})
            need(dimension == stored_dimension, "stored dimension")
            pair_sources = sorted((left["source"], right["source"]))
            member_pair = sorted((left["owner"], right["owner"]))
            component_pair = sorted((left["component"], right["component"]))
            component_relation = ("SAME_C15_COMPONENT"
                                  if component_pair[0] == component_pair[1]
                                  else "CROSS_C15_COMPONENT")
            intersection_sha = digest(intersections)
            if dimension == 3:
                endpoint_policy = "STRICT_POSITIVE_WIDTH_IN_ALL_THREE_AXES__ENDPOINT_BITS_IRRELEVANT"
                lower_disposition = None
            elif pair_sources == ["C19C", "C19C"]:
                lower_c19c += 1
                legal = all(check["both_closed"] for check in endpoint_checks)
                lower_legal += int(legal and component_relation == "CROSS_C15_COMPONENT")
                need(not legal, "C19C lower product must reject")
                endpoint_policy = "C19C_V3_PRODUCT_ENDPOINT_AUTHORITY__AT_LEAST_ONE_ZERO_AXIS_NOT_DOUBLE_INCLUDED"
                lower_disposition = "REJECT_ZERO_WIDTH_C19C_PRODUCT_ENDPOINT_POLICY"
            else:
                lower_open += 1
                endpoint_policy = "AT_LEAST_ONE_FULLY_OPEN_PRIMITIVE_KERNEL_REJECTS_ZERO_WIDTH_CONTACT"
                lower_disposition = "REJECT_ZERO_WIDTH_FULLY_OPEN_KERNEL"
            authority_row = close({
                "schema": AUTHORITY_SCHEMA, "ordinal": ordinal,
                "candidate_key": candidate_key,
                "ordered_primitive_support_atom_keys": [left["key"], right["key"]],
                "ordered_primitive_source_row_sha256": [left["source_sha"], right["source_sha"]],
                "ordered_C15_member_pair": member_pair,
                "ordered_C15_component_pair": component_pair,
                "ordered_C15_member_row_sha256": sorted((left["C15_sha"], right["C15_sha"])),
                "ordered_C25_member_row_sha256": sorted((left["C25_sha"], right["C25_sha"])),
                "chart": left["chart"], "source_pair": pair_sources,
                "intersection_dimension": dimension,
                "component_relation": component_relation,
                "zero_width_axes": zero_axes,
                "exact_intersection_witness_sha256": intersection_sha,
                "endpoint_contact_policy": endpoint_policy,
                "C19C_endpoint_authority_row_sha256": sorted(
                    value for value in (left["endpoint_sha"], right["endpoint_sha"])
                    if value is not None),
                "C19C_zero_axis_endpoint_checks": endpoint_checks,
                "lower_dimensional_disposition_or_null": lower_disposition,
                "C26_no_new_geometry_receipt_sha256": c26_receipt_sha,
                "G2A_scoped_alias_receipt_sha256": g2a_receipt_sha,
                "formal_credit": 0,
            })
            authority_writer.write(authority_row)
            is_cross_strict = (dimension == 3
                               and component_relation == "CROSS_C15_COMPONENT")
            proof_sequence = EMPTY_SHA
            if is_cross_strict:
                witness_key = "same-chart-strict-volume:" + digest([
                    candidate_key, [left["key"], right["key"]], intersection_sha])
                edge_key = EDGE_PREFIX + digest(component_pair)
                proof_key = PROOF_PREFIX + digest([
                    candidate_key, witness_key, member_pair, component_pair])
                proof = close({
                    "schema": PROOF_SCHEMA, "ordinal": proof_count,
                    "proof_row_key": proof_key,
                    "candidate_key": candidate_key,
                    "atom_pair_incidence_key_or_null": None,
                    "terminal": T00, "authority_slot": SLOT,
                    "primitive_authority_row_sha256": authority_row["row_sha256"],
                    "ordered_C15_member_pair": member_pair,
                    "ordered_C15_component_pair": component_pair,
                    "component_edge_key": edge_key,
                    "physical_witness_key": witness_key,
                    "formal_credit": 0,
                })
                proof_writer.write(proof)
                proof_sequence = hashlib.sha256(
                    proof["row_sha256"].encode("ascii") + b"\n").hexdigest()
                proof_edges.add(edge_key)
                proof_count += 1
                component_disposition = "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED"
            elif dimension < 3:
                component_disposition = "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS"
            else:
                component_disposition = "SAME_FROZEN_C15_COMPONENT__NO_EDGE"
            disposition_census[component_disposition] += 1
            candidate = close({
                "schema": CANDIDATE_SCHEMA, "ordinal": ordinal,
                "candidate_key": candidate_key,
                "candidate_kind": "SAME_CHART_EXACT_CONTACT_CANDIDATE",
                "candidate_pair_key_or_null": candidate_key,
                "terminal_ordinal": 0, "terminal": T00,
                "authority_slot": SLOT,
                "primitive_authority_row_sha256": authority_row["row_sha256"],
                "component_relation_disposition": component_disposition,
                "physical_proof_row_count": int(is_cross_strict),
                "physical_proof_row_sequence_sha256": proof_sequence,
                "formal_credit": 0,
            })
            candidate_writer.write(candidate)
        need(authority_writer.count == candidate_writer.count == 5_970_840
             and proof_count == 32_240 and len(proof_edges) == 14_772,
             "emitted T00 census")
        need(lower_open == 5_707_708 and lower_c19c == 76_000
             and lower_legal == 0, "lower endpoint policy census")
        need(disposition_census == {
            "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 32_240,
            "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 154_892,
            "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 5_783_708,
        }, "candidate disposition census")
        authority_desc = authority_writer.finish(
            AUTHORITY_SCHEMA, "candidate_key", ["candidate_key"])
        candidate_desc = candidate_writer.finish(
            CANDIDATE_SCHEMA, "candidate_key", ["candidate_key"])
        proof_desc = proof_writer.finish(
            PROOF_SCHEMA, "proof_row_key", ["candidate_key"])
        writers.clear()
        db.close()
        db = None
        db_path.unlink()

        stable = {
            "primitive_support_atom_count": len(atoms),
            "primitive_owner_count": len(owners),
            "candidate_count": candidate_desc["row_count"],
            "strict_dimension3_candidate_count": dimensions[3],
            "lower_dimension0_1_2_candidate_count":
                sum(dimensions[d] for d in (0, 1, 2)),
            "dimension_census": {str(key): dimensions[key]
                                 for key in sorted(dimensions)},
            "dimension_component_relation_census": {
                f"dim{dimension}__{relation}": count
                for (dimension, relation), count in sorted(relations.items())},
            "lower_cross_component_candidate_count": 2_598_666,
            "lower_same_component_candidate_count": 3_185_042,
            "lower_fully_open_rejection_count": lower_open,
            "lower_C19C_endpoint_dependent_rejection_count": lower_c19c,
            "lower_legal_witness_count": lower_legal,
            "strict_cross_component_physical_proof_count": proof_count,
            "strict_same_component_no_edge_count": 154_892,
            "unique_component_edge_count": len(proof_edges),
            "candidate_component_disposition_census":
                dict(sorted(disposition_census.items())),
            "source_dimension_component_census": {
                f"dim{dimension}__{sources}__{relation}": count
                for (dimension, sources, relation), count
                in sorted(source_dimension.items())},
        }
        source = Path(__file__).resolve()
        body = {
            "schema": "cm2.c27-independent.primitive-v5-actual-t00-same-chart-exact-contact-adapter.v2",
            "status": "PASS_FRESH_T00_5970840_EXACT_CONTACT_CANDIDATES__LOWER_ZERO_EDGE__STRICT_32240_PROOFS__ZERO_CREDIT",
            "execution_seed": seed,
            "seed_usage": "RANDOMIZES_ONLY_RTREE_INSERTION__EMISSION_SORTED_BY_CANDIDATE_KEY",
            "interface_v2_object_sha256": interface_sha,
            "terminal_adapter": {
                "terminal_ordinal": 0, "terminal": T00,
                "authority_slot": SLOT,
                "primitive_authority_ledger": authority_desc,
                "candidate_ownership_ledger": candidate_desc,
                "materialized_physical_proof_fragment_ledger": proof_desc,
            },
            "exact_census": stable,
            "authority_closures": {
                "fresh_six_kernel_four_chart_enumeration": True,
                "strict_and_lower_candidate_union_disjoint_complete": True,
                "C26_691424_is_absence_coverage_theorem_not_candidate_rows": True,
                "G2A_G2B_alias_adds_no_T00_candidate": True,
                "all_lower_dimensional_candidates_have_no_component_edge": True,
                "every_strict_cross_component_candidate_has_one_physical_proof": True,
                "strict_same_component_candidates_have_no_edge": True,
                "proof_edges_derived_only_from_materialized_member_pairs_via_C15": True,
            },
            "forbidden_input_governance": {
                "old_C27_FAMILIES_imported_or_read": False,
                "old_transition_ledger_imported_or_read": False,
                "C28_imported_or_read": False, "C29_imported_or_read": False,
                "historical_edge_ledger_used_as_candidate_universe": False,
                "older_same_chart_candidate_ledger_imported_or_read": False,
                "strict_14772_used_as_candidate_universe": False,
            },
            "formal_credit": 0, "manifest_authorized": False,
            "Source_W_transition_authorized": False,
            "strict_nonpromotion": {"C27_transition_totality": 0,
                                    "C28_pair_routing": 0,
                                    "C29_physical_maximality": 0,
                                    "CM2": "NO-GO_FOR_CLAIM"},
            "producer_source_sha256": file_sha(source),
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {label: capture.attestation()
                                 for label, capture in sorted(captures.items())},
            },
        }
        receipt = dict(body)
        receipt["receipt_sha256"] = digest(receipt)
        receipt_path = out_dir / "adapter_receipt.json"
        receipt_path.write_bytes(canonical(receipt) + b"\n")
        manifest = []
        for desc in (authority_desc, candidate_desc, proof_desc):
            manifest.append(f"{desc['sha256']}  {desc['path']}\n")
        for capture in captures.values():
            item = capture.attestation()
            manifest.append(f"{item['sha256']}  {item['path']}\n")
        manifest.extend((f"{file_sha(source)}  {source.relative_to(ROOT)}\n",
                         f"{file_sha(receipt_path)}  {receipt_path.relative_to(ROOT)}\n"))
        (out_dir / "manifest.sha256").write_text(
            "".join(sorted(set(manifest))), encoding="ascii")
        return receipt
    finally:
        if db is not None:
            db.close()
        for writer in writers:
            if not writer.raw.closed:
                writer.stream.close()
                writer.raw.close()
        for capture in captures.values():
            capture.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    try:
        receipt = build(Path(args.out_dir).resolve(), args.seed)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            sqlite3.Error, json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(canonical({"status": receipt["status"],
                     "execution_seed": receipt["execution_seed"],
                     "exact_census": receipt["exact_census"],
                     "receipt_sha256": receipt["receipt_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
