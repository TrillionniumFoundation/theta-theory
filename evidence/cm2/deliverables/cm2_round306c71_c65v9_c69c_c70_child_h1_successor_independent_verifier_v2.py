#!/usr/bin/env python3
"""Independent no-producer verifier for the pin-filled C71 successor v2.

The candidate producer source is not imported, opened, decoded, compiled, or
executed.  This verifier independently reopens the frozen C65-v9, C69c, and
C70-L inputs, replays the exact C61-to-C65 child lineage, and recomputes every
one of the 33,100 child-level H1 evaluations at 384 bits.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from dataclasses import dataclass
from fractions import Fraction
import gzip
import hashlib
import importlib
import itertools
import json
import multiprocessing as mp
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Iterator


sys.dont_write_bytecode = True
SELF = Path(__file__).resolve()
OUT = SELF.parent
ROOT = OUT.parent
FLINT_SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"
for entry in (str(OUT), str(FLINT_SITE)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

PREFIX = "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_v2"
SCHEMA = "cm2.round306c71.c65v9-c69c-c70-child-h1-successor.v2"
CONTRACT_NAME = "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_contract_v2.json"
SCHEMAS_NAME = "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_closed_schemas_v2.json"
CONTRACT_FILE_SHA256 = "d83459e29589f98b5f0929652ed5b78024cd34b9f572d6aa8d50ef85bd4265da"
CONTRACT_OBJECT_SHA256 = "509779842cffc4a5db47a53bad451607cf86cdb4328718f82d531b74f23b7bc1"
SCHEMAS_FILE_SHA256 = "53c71aa77f5e503b4a4ee8e9530ad0d4b53bdc61fef98eb17302d73b1ae8dcec"
SCHEMAS_OBJECT_SHA256 = "ca23ab339c6d4393447586dbf362b68418752d89d6d99649c44cee33dc1bc8c3"
INTERSECTION_NAME = PREFIX + "_intersection_rows.jsonl.gz"
SOURCE_SUMMARY_NAME = PREFIX + "_source_summaries.jsonl.gz"
RESULT_NAME = PREFIX + "_result.json"
REPORT_NAME = PREFIX + "_report.md"

PRECISION_BITS = 384
EXPECTED_C2 = 167255
EXPECTED_NUMERIC = 33100
EXPECTED_BLOCKED = 134155
EXPECTED_DECISIONS = 2356
EXPECTED_BLOCKERS = 18523
EXPECTED_SOURCES = 20879

C65_NAMES = {
    "verifier": "cm2_round306c65s18_64shard_aggregate_independent_cold_verifier_v9.py",
    "aggregate_result": "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json",
    "aggregate_leaf_ledger": "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz",
    "aggregate_source_summary": "cm2_round306c65s18_depth18_64shard_aggregate_source_summary_v1.jsonl.gz",
    "aggregate_parent_summary": "cm2_round306c65s18_depth18_64shard_aggregate_parent_summary_v1.jsonl.gz",
    "seed1_projection": "cm2_round306c65s18_64shard_aggregate_independent_cold_seed1_projection_v9.json",
    "seed1_completion_receipt": "cm2_round306c65s18_64shard_aggregate_independent_cold_seed1_completion_receipt_v9.json",
    "seed2_projection": "cm2_round306c65s18_64shard_aggregate_independent_cold_seed2_projection_v9.json",
    "seed2_completion_receipt": "cm2_round306c65s18_64shard_aggregate_independent_cold_seed2_completion_receipt_v9.json",
    "verification": "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v9.json",
    "verification_completion_receipt": "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_completion_receipt_v9.json",
    "self_test": "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json",
    "self_test_completion_receipt": "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_completion_receipt_v9.json",
    "postpublication_replay": "cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v9.json",
    "manifest": "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256",
    "outer_receipt": "cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json",
}
C65_RELEASE_ROLES = (
    "seed1_projection", "seed1_completion_receipt", "seed2_projection",
    "seed2_completion_receipt", "verification", "verification_completion_receipt",
    "self_test", "self_test_completion_receipt", "postpublication_replay",
)
C69_NAMES = {
    "corrected_result": "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json",
    "verification": "cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json",
    "self_test": "cm2_round306c69c_descriptor_repair_supersession_independent_self_test_v1.json",
    "outer_receipt": "cm2_round306c69c_descriptor_repair_supersession_independent_outer_publication_receipt_v1.json",
    "manifest": "cm2_round306c69c_descriptor_repair_supersession_independent_manifest_v1.sha256",
    "decisions": "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_decisions.jsonl.gz",
    "blockers": "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz",
}
C70_NAMES = {
    "result": "cm2_round306c70l_large_component_consumption_intersection_result_v1.json",
    "independent_verification": "cm2_round306c70l_large_component_consumption_intersection_independent_verification_v1.json",
    "manifest": "cm2_round306c70l_large_component_consumption_intersection_manifest_v1.sha256",
    "manifest_receipt": "cm2_round306c70l_large_component_consumption_intersection_manifest_v1.sha256.sha256",
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def identity(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def secure_read(path: Path, expected_sha: str) -> bytes:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular-single-link:" + str(path))
        chunks: list[bytes] = []
        while block := os.read(descriptor, 4 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    need(identity(before) == identity(after) == identity(current), "TOCTOU:" + str(path))
    raw = b"".join(chunks)
    need(hashlib.sha256(raw).hexdigest() == expected_sha, "file-pin:" + str(path))
    return raw


def secure_hash(path: Path, expected_sha: str) -> tuple[str, int]:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                         getattr(os, "O_NOFOLLOW", 0))
    hasher = hashlib.sha256()
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular-single-link:" + str(path))
        while block := os.read(descriptor, 4 << 20):
            hasher.update(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    need(identity(before) == identity(after) == identity(os.stat(path, follow_symlinks=False)),
         "TOCTOU:" + str(path))
    actual = hasher.hexdigest()
    need(actual == expected_sha, "file-pin:" + str(path))
    return actual, before.st_size


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate-json-key:" + key)
        result[key] = value
    return result


def reject_float(token: str) -> Any:
    raise Reject("noninteger-json-number:" + token)


def parse_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         "json-framing:" + label)
    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=no_duplicates,
                       parse_float=reject_float,
                       parse_constant=lambda token: reject_float(token))
    need(type(value) is dict, "json-object:" + label)
    return value


def close_object(value: dict[str, Any], expected: str, label: str) -> None:
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == expected == digest(body), "object-closure:" + label)


def close_row(value: dict[str, Any], label: str) -> None:
    body = copy.deepcopy(value)
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), "row-closure:" + label)


def parse_manifest(raw: bytes, label: str) -> list[tuple[str, str]]:
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n") and b"\x00" not in raw,
         "manifest-framing:" + label)
    result: list[tuple[str, str]] = []
    seen: set[str] = set()
    for line in raw.decode("utf-8", "strict").splitlines():
        sha, separator, name = line.partition("  ")
        need(separator == "  " and len(sha) == 64 and
             all(character in "0123456789abcdef" for character in sha) and
             name not in seen, "manifest-row:" + label)
        seen.add(name)
        result.append((sha, name))
    return result


def sequence_hash(values: Iterable[str]) -> str:
    hasher = hashlib.sha256()
    for value in values:
        hasher.update(value.encode("utf-8") + b"\n")
    return hasher.hexdigest()


def pinned_json(path: Path, file_pin: str, object_pin: str, label: str) -> dict[str, Any]:
    value = parse_json(secure_read(path, file_pin), label)
    close_object(value, object_pin, label)
    return value


def resolve_c65(relative: str) -> Path:
    if relative.startswith("machine-runtime/"):
        return Path("/") / relative.removeprefix("machine-runtime/")
    return ROOT / relative


def input_gate() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract = pinned_json(OUT / CONTRACT_NAME, CONTRACT_FILE_SHA256,
                           CONTRACT_OBJECT_SHA256, "contract")
    schemas = pinned_json(OUT / SCHEMAS_NAME, SCHEMAS_FILE_SHA256,
                          SCHEMAS_OBJECT_SHA256, "schemas")
    need(contract["closed_schemas"]["object_sha256"] == schemas["object_sha256"] and
         contract["execution_guard"]["old_C71_skeleton_may_be_imported_or_executed"] is False,
         "contract execution boundary")
    pins = contract["frozen_pin_map"]
    need(set(pins) == {"C65_v9", "C69c", "C70L", "numeric_kernel"} and
         all(type(value) is dict and bool(value) for value in pins.values()),
         "nonempty exact pin map")

    c65 = pins["C65_v9"]
    verification = pinned_json(OUT / C65_NAMES["verification"], c65["verification"],
                               c65["verification_object"], "C65 verification")
    self_test = pinned_json(OUT / C65_NAMES["self_test"], c65["self_test"],
                            c65["self_test_object"], "C65 self-test")
    outer = pinned_json(OUT / C65_NAMES["outer_receipt"], c65["outer_receipt"],
                        c65["outer_receipt_object"], "C65 outer")
    need(verification["status"].startswith("PASS_DUAL_EXTERNAL_PROCESS_COLD_VERIFICATION_V9") and
         self_test["test_count"] == 134 and "134_OF_134" in self_test["status"] and
         "94_OF_94" not in self_test["status"] and
         verification["rejections"]["rejected_v3_verifier_or_outputs_consumed"] is False,
         "C65 v9 not rejected v3")
    manifest = parse_manifest(secure_read(OUT / C65_NAMES["manifest"], c65["manifest"]),
                              "C65")
    vector = verification["frozen_snapshot"]["ordered_input_vector"]
    expected: list[tuple[str, str, str]] = []
    for row in vector:
        need(row["logical_name"] == row["relative_path"].replace("/", "__"),
             "C65 alias")
        expected.append((row["sha256"], row["logical_name"], row["relative_path"]))
    for role in C65_RELEASE_ROLES:
        relative = "deliverables/" + C65_NAMES[role]
        expected.append((c65[role], relative.replace("/", "__"), relative))
    need(len(vector) == 437 and len(expected) == len(manifest) == 446 and
         [(sha, alias) for sha, alias, _relative in expected] == manifest,
         "C65 exact 446 manifest")
    need(sequence_hash(alias for _sha, alias in manifest) ==
         outer["manifest_ordered_alias_sequence_sha256"], "C65 alias sequence")
    terminal: list[str] = []
    for sha, alias, relative in expected:
        actual, size = secure_hash(resolve_c65(relative), sha)
        terminal.append(alias + "\0" + actual + "\0" + str(size))
    for name, sha in ((C65_NAMES["manifest"], c65["manifest"]),
                      (C65_NAMES["outer_receipt"], c65["outer_receipt"])):
        actual, size = secure_hash(OUT / name, sha)
        terminal.append("deliverables__" + name + "\0" + actual + "\0" + str(size))
    need(len(terminal) == 448 and outer["outer_receipt_published_last"] is True,
         "C65 terminal-byte replay")
    aggregate = pinned_json(OUT / C65_NAMES["aggregate_result"], c65["aggregate_result"],
                            c65["aggregate_result_object"], "C65 aggregate")
    need(aggregate["coverage"]["replacement_disposition_census"]["COLLISION2_HANDOFF"] ==
         EXPECTED_C2, "C65 aggregate C2")

    c69 = pins["C69c"]
    c69_manifest = parse_manifest(secure_read(OUT / C69_NAMES["manifest"], c69["manifest"]),
                                  "C69c")
    need(len(c69_manifest) == 25, "C69c manifest count")
    for sha, relative in c69_manifest:
        secure_hash(ROOT / relative, sha)
    corrected = pinned_json(OUT / C69_NAMES["corrected_result"], c69["corrected_result"],
                            c69["corrected_result_object"], "C69c corrected")
    c69_verify = pinned_json(OUT / C69_NAMES["verification"], c69["verification"],
                             c69["verification_object"], "C69c verification")
    pinned_json(OUT / C69_NAMES["self_test"], c69["self_test"],
                c69["self_test_object"], "C69c self-test")
    pinned_json(OUT / C69_NAMES["outer_receipt"], c69["outer_receipt"],
                c69["outer_receipt_object"], "C69c outer")
    need(c69_verify["status"].startswith("PASS_COLD_NO_C69_PRODUCER_OR_WRAPPER") and
         corrected["strict_boundary"]["decisions_are_terminal_dispositions"] is False,
         "C69c nonterminal source authority")

    c70 = pins["C70L"]
    c70_manifest = parse_manifest(secure_read(OUT / C70_NAMES["manifest"], c70["manifest"]),
                                  "C70L")
    need(len(c70_manifest) == 8, "C70L manifest count")
    for sha, name in c70_manifest:
        secure_hash(OUT / name, sha)
    need(secure_read(OUT / C70_NAMES["manifest_receipt"], c70["manifest_receipt"]) ==
         (c70["manifest"] + "  " + C70_NAMES["manifest"] + "\n").encode(),
         "C70L manifest receipt")
    c70_result = pinned_json(OUT / C70_NAMES["result"], c70["result"],
                             c70["result_object"], "C70L result")
    c70_verify = pinned_json(OUT / C70_NAMES["independent_verification"],
                             c70["independent_verification"],
                             c70["independent_verification_object"], "C70L verification")
    summary = c70_verify["independent_rebuild"]["summary"]
    need(summary["edge_ready_count"] == 298 and summary["edge_blocked_count"] == 744 and
         summary["corridor_ready_count"] == 73 and summary["corridor_blocked_count"] == 971 and
         summary["source_seam_ready_count"] == 0 and
         c70_result["strict_boundary"]["D02_gate_credit"] == 0,
         "C70L obstruction boundary")
    return contract, schemas, aggregate, corrected


def iter_rows(path: Path, descriptor: dict[str, Any], label: str) -> Iterator[dict[str, Any]]:
    need(file_sha(path) == descriptor["sha256"] and path.stat().st_size == descriptor["size"],
         "descriptor bytes:" + label)
    count = 0
    sequence = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for raw in handle:
            row = parse_json(raw, label + ":" + str(count))
            need(canonical(row) + b"\n" == raw, "canonical row:" + label)
            close_row(row, label + ":" + str(count))
            sequence.update(row["row_sha256"].encode("ascii") + b"\n")
            count += 1
            yield row
    need(count == descriptor["row_count"] and
         sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         "descriptor rows:" + label)


@dataclass(frozen=True)
class ExactBox:
    t0: Fraction
    t1: Fraction
    p0: Fraction
    p1: Fraction
    s0: Fraction
    s1: Fraction

    def bounds(self, axis: int) -> tuple[Fraction, Fraction]:
        return ((self.t0, self.t1), (self.p0, self.p1), (self.s0, self.s1))[axis]

    def width(self, axis: int) -> Fraction:
        lower, upper = self.bounds(axis)
        return upper - lower


def exact_box(payload: dict[str, list[str]]) -> ExactBox:
    need(set(payload) == {"t", "p", "s"} and all(len(payload[key]) == 2 for key in payload),
         "box schema")
    box = ExactBox(*(Fraction(item) for key in ("t", "p", "s") for item in payload[key]))
    need(all(box.width(axis) >= 0 for axis in range(3)), "box order")
    return box


def box_payload(box: ExactBox) -> dict[str, list[str]]:
    return {"t": [str(box.t0), str(box.t1)], "p": [str(box.p0), str(box.p1)],
            "s": [str(box.s0), str(box.s1)]}


def split_box(box: ExactBox, axis: int) -> tuple[ExactBox, ExactBox]:
    lower, upper = box.bounds(axis)
    middle = (lower + upper) / 2
    values = [[box.t0, box.t1], [box.p0, box.p1], [box.s0, box.s1]]
    left, right = copy.deepcopy(values), copy.deepcopy(values)
    left[axis][1] = middle
    right[axis][0] = middle
    make = lambda value: ExactBox(value[0][0], value[0][1], value[1][0], value[1][1],
                                  value[2][0], value[2][1])
    return make(left), make(right)


def replay_child(source: dict[str, Any], child: dict[str, Any]) -> str:
    need(child["path"].startswith(source["path"]), "child prefix")
    box = exact_box(source["exact_representative_box"])
    chain: list[dict[str, Any]] = []
    suffix = child["path"][len(source["path"]):]
    for depth, bit in enumerate(suffix, 1):
        need(bit in "01", "binary suffix")
        axis = max(range(3), key=box.width)
        middle = sum(box.bounds(axis), Fraction(0)) / 2
        chain.append({"depth": depth, "axis": ("t", "p", "s")[axis],
                      "split": str(middle), "bit": bit,
                      "shared_face_owner": "LOWER_BIT_CHILD",
                      "selected_owns_shared_face": bit == "0"})
        box = split_box(box, axis)[int(bit)]
    need(box_payload(box) == child["exact_representative_box"] and
         Fraction(child["parent_volume_fraction"]) ==
         Fraction(source["parent_volume_fraction"]) / 2 ** len(suffix),
         "child box/volume replay")
    return digest(chain)


def load_domains(aggregate: dict[str, Any], c69: dict[str, Any]
                ) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    c61_result = pinned_json(
        OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json",
        "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
        "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
        "C61 result")
    sources = {row["row_sha256"]: row for row in iter_rows(
        OUT / c61_result["ledgers"]["aggregate_leaves"]["filename"],
        c61_result["ledgers"]["aggregate_leaves"], "C61 leaves")
        if row["disposition"] == "COLLISION2_HANDOFF"}
    summaries = list(iter_rows(OUT / aggregate["ledgers"]["source_summaries"]["filename"],
                               aggregate["ledgers"]["source_summaries"],
                               "C65 source summaries"))
    decisions = {row["C61_aggregate_leaf_row_sha256"]: row for row in iter_rows(
        OUT / C69_NAMES["decisions"], c69["ledgers"]["decisions"], "C69 decisions")}
    blockers = {row["C61_aggregate_leaf_row_sha256"]: row for row in iter_rows(
        OUT / C69_NAMES["blockers"], c69["ledgers"]["blockers"], "C69 blockers")}
    need(len(sources) == len(summaries) == EXPECTED_SOURCES and
         len(decisions) == EXPECTED_DECISIONS and len(blockers) == EXPECTED_BLOCKERS and
         set(decisions).isdisjoint(blockers) and set(decisions) | set(blockers) == set(sources),
         "exact source domains")
    return sources, summaries, decisions, blockers


G_DECISIONS: dict[str, Any] = {}
G_R185: Any = None
G_ATLAS: Any = None


def load_kernel(pins: dict[str, Any]) -> None:
    global G_R185, G_ATLAS
    flint = importlib.import_module("flint")
    flint.ctx.prec = PRECISION_BITS
    need(flint.__version__ == pins["python_flint_version"] and
         Path(flint.__file__).resolve().is_relative_to(FLINT_SITE.resolve()),
         "flint environment")
    G_R185 = importlib.import_module("cm2_round185_preconditioned_c1_residual_refinement")
    atlas_module = importlib.import_module("cm2_gate3_eight_cell_symmetry_atlas_cert")
    G_ATLAS = atlas_module.AtlasBox
    need(file_sha(Path(G_R185.__file__).resolve()) == pins["round185"] and
         file_sha(Path(atlas_module.__file__).resolve()) == pins["atlas"] and
         flint.ctx.prec == PRECISION_BITS, "kernel pins")


def arb_payload(value: Any) -> dict[str, Any]:
    return {"lower": str(value.lower()), "upper": str(value.upper()),
            "contains_zero": bool(value.contains(0))}


def sign(value: Any) -> int:
    return 1 if bool(value > 0) else -1 if bool(value < 0) else 0


def strict_normal_chart(h1_sign: int, nx: Any, ny: Any) -> str | None:
    nx_sign = sign(nx)
    ny_sign = sign(ny)
    if h1_sign < 0:
        return "N" if ny_sign > 0 else "S" if ny_sign < 0 else None
    return "E" if nx_sign > 0 else "W" if nx_sign < 0 else None


def independent_numeric(child: dict[str, Any]) -> dict[str, Any]:
    decision = G_DECISIONS[child["source_C61_aggregate_leaf_row_sha256"]]
    exact = exact_box(child["exact_representative_box"])
    box = G_ATLAS(exact.t0, exact.t1, exact.p0, exact.p1, exact.s0, exact.s1, 0,
                  child["path"])
    origin = decision["representative_origin_key"]
    full, nx, ny = G_R185.collision1_h1_ad(origin, box, "W[1,0]")
    centered = G_R185.centered_enclosure(
        G_R185.collision1_h1_ad, origin, box, "W[1,0]", full)
    common = {
        "precision_bits": PRECISION_BITS, "equation": "H1=n1_x^2-n1_y^2",
        "full_child_box_natural_interval": arb_payload(full.value),
        "full_child_box_centered_mean_value_interval": arb_payload(centered),
        "full_child_box_derivatives": {
            axis: arb_payload(value) for axis, value in zip(("t", "p", "s"), full.derivative)},
        "normal_component_bounds": {"nx": arb_payload(nx.value), "ny": arb_payload(ny.value)},
        "C69c_source_certificate_copied": False,
        "independent_deterministic_axis_order": ["t", "p", "s"],
    }
    full_sign = sign(full.value)
    method = "NATURAL_INTERVAL"
    if full_sign == 0:
        full_sign = sign(centered)
        method = "CENTERED_MEAN_VALUE_INTERVAL"
    if full_sign:
        disposition = ("LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX" if full_sign > 0 else
                       "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX")
        certificate = {**common, "accepted_full_box_method": method,
                       "strict_full_box_sign": "POSITIVE" if full_sign > 0 else "NEGATIVE",
                       "strict_normal_chart":
                       strict_normal_chart(full_sign, nx.value, ny.value),
                       "axis_tests": []}
        partition = {"H1_LT_0": "EMPTY" if full_sign > 0 else "EXACT_CHILD",
                     "H1_EQ_0": "EMPTY",
                     "H1_GT_0": "EXACT_CHILD" if full_sign > 0 else "EMPTY",
                     "pairwise_disjoint": True, "union_exact_child": True}
        return {"child_row_sha256": child["row_sha256"], "disposition": disposition,
                "certificate": certificate, "partition": partition,
                "consumer_review_ready": True, "blockers": []}
    coordinate_monotonicity: list[dict[str, Any]] = []
    minimum_point: list[Fraction] = []
    maximum_point: list[Fraction] = []
    all_monotone = True
    for axis in range(3):
        lower, upper = exact.bounds(axis)
        if lower == upper:
            coordinate_monotonicity.append({
                "axis": ("t", "p", "s")[axis], "positive_width": False,
                "orientation": "CONSTANT_COORDINATE",
                "derivative_bounds": arb_payload(full.derivative[axis])})
            minimum_point.append(lower)
            maximum_point.append(lower)
            continue
        derivative_sign = sign(full.derivative[axis])
        if derivative_sign == 0:
            all_monotone = False
            orientation = "UNRESOLVED"
            minimum_point.append(lower)
            maximum_point.append(upper)
        elif derivative_sign > 0:
            orientation = "STRICTLY_INCREASING"
            minimum_point.append(lower)
            maximum_point.append(upper)
        else:
            orientation = "STRICTLY_DECREASING"
            minimum_point.append(upper)
            maximum_point.append(lower)
        coordinate_monotonicity.append({
            "axis": ("t", "p", "s")[axis], "positive_width": True,
            "orientation": orientation,
            "derivative_bounds": arb_payload(full.derivative[axis])})
    if all_monotone:
        minimum_box = G_R185.point_box(box, *minimum_point, ".c71.monotone.minimum")
        maximum_box = G_R185.point_box(box, *maximum_point, ".c71.monotone.maximum")
        minimum_value, _nx, _ny = G_R185.collision1_h1_ad(
            origin, minimum_box, "W[1,0]")
        maximum_value, _nx, _ny = G_R185.collision1_h1_ad(
            origin, maximum_box, "W[1,0]")
        monotone_sign = -1 if sign(maximum_value.value) < 0 else (
            1 if sign(minimum_value.value) > 0 else 0)
        if monotone_sign:
            disposition = ("LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX"
                           if monotone_sign > 0 else
                           "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX")
            certificate = {
                **common,
                "accepted_full_box_method":
                    "MONOTONE_COORDINATE_CORNER_EXTREMUM_STRICT_SIDE",
                "strict_full_box_sign":
                    "POSITIVE" if monotone_sign > 0 else "NEGATIVE",
                "strict_normal_chart":
                    strict_normal_chart(monotone_sign, nx.value, ny.value),
                "coordinate_monotonicity": coordinate_monotonicity,
                "all_positive_width_axes_strictly_monotone": True,
                "monotone_corner_extrema": {
                    "minimum_point": dict(zip(("t", "p", "s"),
                                              map(str, minimum_point))),
                    "minimum_H1": arb_payload(minimum_value.value),
                    "maximum_point": dict(zip(("t", "p", "s"),
                                              map(str, maximum_point))),
                    "maximum_H1": arb_payload(maximum_value.value)},
                "axis_tests": []}
            partition = {"H1_LT_0": "EMPTY" if monotone_sign > 0 else "EXACT_CHILD",
                         "H1_EQ_0": "EMPTY",
                         "H1_GT_0": "EXACT_CHILD" if monotone_sign > 0 else "EMPTY",
                         "pairwise_disjoint": True, "union_exact_child": True}
            return {"child_row_sha256": child["row_sha256"],
                    "disposition": disposition, "certificate": certificate,
                    "partition": partition, "consumer_review_ready": True,
                    "blockers": []}
    tests: list[dict[str, Any]] = []
    for axis in range(3):
        if exact.width(axis) == 0:
            tests.append({"axis": ("t", "p", "s")[axis], "positive_width": False,
                          "accepted": False})
            continue
        derivative = full.derivative[axis]
        faces = []
        for ordinal, value in enumerate(exact.bounds(axis)):
            fixed = G_R185.fixed_axis_box(box, axis, value, ".c71.face." + str(ordinal))
            evaluated, _nx, _ny = G_R185.collision1_h1_ad(origin, fixed, "W[1,0]")
            faces.append(evaluated.value)
        signs = [sign(value) for value in faces]
        strict_derivative = sign(derivative) != 0
        opposite = signs[0] * signs[1] == -1
        midpoint = sum(exact.bounds(axis), Fraction(0)) / 2
        middle_box = G_R185.fixed_axis_box(box, axis, midpoint, ".c71.mid")
        middle, _nx, _ny = G_R185.collision1_h1_ad(origin, middle_box, "W[1,0]")
        if strict_derivative:
            image = G_R185.BASE.arbq(midpoint) - middle.value / derivative
            lower, upper = exact.bounds(axis)
            self_map = bool(image > G_R185.BASE.arbq(lower)) and bool(
                image < G_R185.BASE.arbq(upper))
            image_payload: dict[str, Any] | None = arb_payload(image)
        else:
            self_map = False
            image_payload = None
        record = {"axis": ("t", "p", "s")[axis], "positive_width": True,
                  "strict_derivative_bounds": arb_payload(derivative),
                  "strict_derivative": strict_derivative,
                  "complete_relative_face_intervals": [arb_payload(value) for value in faces],
                  "complete_faces_strict_opposite_sign": opposite,
                  "interval_Newton_image": image_payload,
                  "interval_Newton_strict_interior_self_map": self_map,
                  "accepted": strict_derivative and opposite}
        tests.append(record)
        if record["accepted"]:
            certificate = {**common,
                           "accepted_full_box_method":
                           "PARAMETRIC_IVT_STRICT_MONOTONICITY_AND_IFT",
                           "graph_axis": record["axis"], "axis_tests": tests,
                           "unique_root_over_every_fixed_transverse_parameter": True,
                           "source_graph_axis_copied": False}
            partition = {"H1_LT_0": "NEGATIVE_OPEN_SLAB",
                         "H1_EQ_0": "UNIQUE_TYPED_GRAPH_CARRIER",
                         "H1_GT_0": "POSITIVE_OPEN_SLAB", "pairwise_disjoint": True,
                         "union_exact_child": True, "graph_full_dimensional_Kraft_weight": "0",
                         "half_open_negative_owner": {"predicate": "H1<=0", "owns_graph": True},
                         "half_open_positive_owner": {"predicate": "H1>0", "owns_graph": False}}
            return {"child_row_sha256": child["row_sha256"],
                    "disposition": "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS",
                    "certificate": certificate, "partition": partition,
                    "consumer_review_ready": True, "blockers": []}
    corners = []
    seen: set[tuple[Fraction, Fraction, Fraction]] = set()
    for point in itertools.product(*[exact.bounds(axis) for axis in range(3)]):
        if point in seen:
            continue
        seen.add(point)
        fixed = G_R185.point_box(box, point[0], point[1], point[2], ".c71.corner")
        value, _nx, _ny = G_R185.collision1_h1_ad(origin, fixed, "W[1,0]")
        corners.append({"point": {"t": str(point[0]), "p": str(point[1]),
                                   "s": str(point[2])},
                        "H1": arb_payload(value.value), "sign": sign(value.value)})
    negative = next((row for row in corners if row["sign"] < 0), None)
    positive = next((row for row in corners if row["sign"] > 0), None)
    certificate = {**common, "accepted_full_box_method": None, "axis_tests": tests,
                   "strict_corner_records": corners,
                   "opposite_sign_corner_segment": {"negative": negative, "positive": positive,
                       "IVT_proves_H1_zero_contact_inside_child":
                       negative is not None and positive is not None}}
    if negative is not None and positive is not None:
        return {"child_row_sha256": child["row_sha256"],
                "disposition": "PROVED_CHILD_H1_ZERO_CONTACT__BOUNDARY_ARRANGEMENT_UNSEALED",
                "certificate": certificate, "partition": None,
                "consumer_review_ready": False,
                "blockers": ["COMPLETE_CHILD_THREE_STRATA_BOUNDARY_ARRANGEMENT_NOT_SEALED",
                             "NO_FALSE_FULL_BASE_GRAPH_OR_STRICT_SLAB_UPGRADE"]}
    return {"child_row_sha256": child["row_sha256"],
            "disposition": "BLOCKED_CHILD_H1_FULL_BOX_CERTIFICATE_INCONCLUSIVE",
            "certificate": certificate, "partition": None,
            "consumer_review_ready": False,
            "blockers": ["FULL_BOX_H1_INTERVAL_NOT_STRICT",
                         "NO_UNIFORM_STRICT_DERIVATIVE_WITH_OPPOSITE_COMPLETE_FACES",
                         "NO_OPPOSITE_STRICT_CORNER_WITNESS"]}


def expected_body(child: dict[str, Any], source: dict[str, Any], c69: dict[str, Any],
                  kind: str, lineage: str, numeric: dict[str, Any] | None) -> dict[str, Any]:
    if kind == "blocker":
        disposition = "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE"
        certificate = partition = None
        ready = False
        remaining = list(c69["blocker_codes"]) + [
            "C69C_SOURCE_KIND_" + c69["structural_graph_kind"],
            "NONDECISION_SOURCE_CHILD_MUST_REMAIN_FAIL_CLOSED"]
    else:
        need(numeric is not None and numeric["child_row_sha256"] == child["row_sha256"],
             "numeric order")
        disposition = numeric["disposition"]
        certificate = numeric["certificate"]
        partition = numeric["partition"]
        ready = numeric["consumer_review_ready"]
        remaining = numeric["blockers"]
    return {"schema": SCHEMA + ".intersection-row",
            "C65_aggregate_leaf_row_sha256": child["row_sha256"],
            "C65_source_shard_row_sha256": child["source_C65_shard_row_sha256"],
            "C69c_source_kind": kind, "C69c_source_row_sha256": c69["row_sha256"],
            "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
            "source_path": source["path"], "child_path": child["path"],
            "pair_index": child["pair_index"],
            "parent_volume_fraction": child["parent_volume_fraction"],
            "exact_representative_box": child["exact_representative_box"],
            "child_box_lineage": {"replayed_exact": True,
                                  "source_path_exact_prefix": True,
                                  "split_owner": "LOWER_BIT_CHILD",
                                  "split_chain_sha256": lineage},
            "prior_C65_disposition": "COLLISION2_HANDOFF",
            "intersection_disposition": disposition,
            "H1_child_certificate": certificate, "three_strata_partition": partition,
            "consumer_review_ready": ready, "global_consumption_ready": False,
            "remaining_blocker_codes": remaining, "terminal_disposition_credit": 0,
            "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0}


def exact_row_guard(observed: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    body = copy.deepcopy(observed)
    row_hash = body.pop("row_sha256", None)
    need(body == expected and row_hash == digest(expected), label)


def coherent_attacks(samples: dict[str, tuple[dict[str, Any], dict[str, Any]]]) -> dict[str, Any]:
    attacks: dict[str, str] = {}
    mutations = {
        "credit_nonzero": lambda row: row.__setitem__("formal_credit", 1),
        "D02_nonzero": lambda row: row.__setitem__("D02_gate_credit", 1),
        "global_ready_false_upgrade": lambda row: row.__setitem__("global_consumption_ready", True),
        "child_hash_substitution": lambda row: row.__setitem__("C65_aggregate_leaf_row_sha256", "0" * 64),
        "source_hash_substitution": lambda row: row.__setitem__("source_C61_aggregate_leaf_row_sha256", "0" * 64),
        "lineage_owner_flip": lambda row: row["child_box_lineage"].__setitem__("split_owner", "UPPER_BIT_CHILD"),
        "pair_index_shift": lambda row: row.__setitem__("pair_index", row["pair_index"] + 1),
        "path_suffix_flip": lambda row: row.__setitem__("child_path", row["child_path"] + "0"),
    }
    sample_observed, sample_expected = next(iter(samples.values()))
    for name, mutate in mutations.items():
        changed = copy.deepcopy(sample_observed)
        mutate(changed)
        try:
            exact_row_guard(changed, sample_expected, "attack:" + name)
        except Reject:
            attacks[name] = "FAIL_CLOSED"
        else:
            raise Reject("attack escaped:" + name)
    for sample_name, (observed, expected) in samples.items():
        for suffix, field, value in (
            ("source_kind_swap", "C69c_source_kind",
             "decision" if observed["C69c_source_kind"] == "blocker" else "blocker"),
            ("consumer_ready_flip", "consumer_review_ready",
             not observed["consumer_review_ready"]),
            ("false_disposition", "intersection_disposition",
             "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE"
             if observed["intersection_disposition"] !=
             "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE"
             else "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS"),
        ):
            changed = copy.deepcopy(observed)
            changed[field] = value
            try:
                exact_row_guard(changed, expected, "attack:" + sample_name + ":" + suffix)
            except Reject:
                attacks[sample_name + "__" + suffix] = "FAIL_CLOSED"
            else:
                raise Reject("attack escaped:" + sample_name + ":" + suffix)
    need(len(attacks) >= 20, "coherent attack breadth")
    return {"status": f"PASS_{len(attacks)}_OF_{len(attacks)}_COHERENT_CHILD_AND_CREDIT_ATTACKS_FAIL_CLOSED",
            "attack_count": len(attacks), "attacks": dict(sorted(attacks.items()))}


def exclusive_write(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_NOFOLLOW", 0), 0o644)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(descriptor, view)
            need(count > 0, "write progress")
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    need(path.read_bytes() == raw and path.stat().st_nlink == 1, "output terminal replay")


def verify(candidate: Path, output: Path, workers: int) -> dict[str, Any]:
    candidate = candidate.resolve()
    need(candidate.is_dir() and not candidate.is_symlink(), "candidate directory")
    contract, schemas, aggregate, c69 = input_gate()
    result = parse_json(secure_read(candidate / RESULT_NAME, file_sha(candidate / RESULT_NAME)),
                        "candidate result")
    close_object(result, result.get("object_sha256"), "candidate result")
    need(result["schema"] == SCHEMA + ".result" and
         result["status"].startswith("PASS_COMPLETE_167255_CHILD_INTERSECTION") and
         result["coverage"]["partition_identity"] == "167255=33100+134155" and
         result["candidate_is_authority"] is False and
         result["global_consumption_ready"] is False and
         result["runtime_canonical_pointer_or_seal_writes"] is False and
         result["formal_credit"] == result["whole_parent_credit"] ==
         result["terminal_disposition_credit"] == result["D02_gate_credit"] == 0,
         "candidate result boundary")
    need(set(schemas["result"]["required_keys"]) <= set(result), "closed result required keys")
    sources, summaries, decisions, blockers = load_domains(aggregate, c69)
    leaf_path = OUT / aggregate["ledgers"]["aggregate_leaves"]["filename"]
    intersection_descriptor = result["ledgers"]["intersection_rows"]
    tasks: list[dict[str, Any]] = []
    c2_counts: Counter[str] = Counter()
    decision_count = blocker_count = 0
    candidate_iterator = iter_rows(candidate / INTERSECTION_NAME, intersection_descriptor,
                                   "candidate intersection first pass")
    for child in iter_rows(leaf_path, aggregate["ledgers"]["aggregate_leaves"],
                           "C65 leaves verifier first pass"):
        if child["disposition"] != "COLLISION2_HANDOFF":
            continue
        observed = next(candidate_iterator)
        source_hash = child["source_C61_aggregate_leaf_row_sha256"]
        source = sources[source_hash]
        lineage = replay_child(source, child)
        need(observed["C65_aggregate_leaf_row_sha256"] == child["row_sha256"] and
             observed["child_box_lineage"]["split_chain_sha256"] == lineage and
             observed["global_consumption_ready"] is False and
             observed["formal_credit"] == observed["whole_parent_credit"] ==
             observed["terminal_disposition_credit"] == observed["D02_gate_credit"] == 0,
             "candidate static child binding")
        c2_counts[source_hash] += 1
        if source_hash in decisions:
            tasks.append(child)
            decision_count += 1
        else:
            need(source_hash in blockers and
                 observed["intersection_disposition"] ==
                 "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE" and
                 observed["H1_child_certificate"] is None and
                 observed["consumer_review_ready"] is False,
                 "blocker-source child fail closed")
            blocker_count += 1
    try:
        next(candidate_iterator)
    except StopIteration:
        pass
    else:
        raise Reject("extra candidate intersection rows")
    need(decision_count == EXPECTED_NUMERIC and blocker_count == EXPECTED_BLOCKED and
         decision_count + blocker_count == EXPECTED_C2, "167255 split")

    global G_DECISIONS
    G_DECISIONS = decisions
    load_kernel(contract["frozen_pin_map"]["numeric_kernel"])
    pool = mp.get_context("fork").Pool(processes=workers)
    numeric_iterator = pool.imap(independent_numeric, tasks, chunksize=8)
    candidate_iterator = iter_rows(candidate / INTERSECTION_NAME, intersection_descriptor,
                                   "candidate intersection numeric pass")
    disposition_counts: Counter[str] = Counter()
    source_stats: dict[str, Counter[str]] = defaultdict(Counter)
    source_volumes: dict[str, Fraction] = defaultdict(Fraction)
    source_sequences: dict[str, Any] = defaultdict(hashlib.sha256)
    samples: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    try:
        for child in iter_rows(leaf_path, aggregate["ledgers"]["aggregate_leaves"],
                               "C65 leaves verifier numeric pass"):
            if child["disposition"] != "COLLISION2_HANDOFF":
                continue
            observed = next(candidate_iterator)
            source_hash = child["source_C61_aggregate_leaf_row_sha256"]
            source = sources[source_hash]
            lineage = replay_child(source, child)
            if source_hash in decisions:
                numeric = next(numeric_iterator)
                c69_row = decisions[source_hash]
                kind = "decision"
            else:
                numeric = None
                c69_row = blockers[source_hash]
                kind = "blocker"
            expected = expected_body(child, source, c69_row, kind, lineage, numeric)
            exact_row_guard(observed, expected, "independent exact child")
            disposition = observed["intersection_disposition"]
            disposition_counts[disposition] += 1
            source_stats[source_hash][disposition] += 1
            source_stats[source_hash]["ready"] += int(observed["consumer_review_ready"])
            source_volumes[source_hash] += Fraction(observed["parent_volume_fraction"])
            source_sequences[source_hash].update(observed["row_sha256"].encode() + b"\n")
            sample_key = {
                "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE": "blocker",
                "LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX": "strict",
                "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS": "graph",
                "PROVED_CHILD_H1_ZERO_CONTACT__BOUNDARY_ARRANGEMENT_UNSEALED": "boundary",
                "BLOCKED_CHILD_H1_FULL_BOX_CERTIFICATE_INCONCLUSIVE": "inconclusive",
            }.get(disposition)
            if sample_key and sample_key not in samples:
                samples[sample_key] = (observed, expected)
        try:
            next(candidate_iterator)
        except StopIteration:
            pass
        else:
            raise Reject("extra numeric-pass candidate rows")
        try:
            next(numeric_iterator)
        except StopIteration:
            pass
        else:
            raise Reject("extra numeric replay outcomes")
    finally:
        pool.close()
        pool.join()
    need(set(samples) == {"blocker", "strict", "graph", "boundary"},
         "all measured outcome samples")

    summary_descriptor = result["ledgers"]["source_summaries"]
    observed_summaries = list(iter_rows(candidate / SOURCE_SUMMARY_NAME, summary_descriptor,
                                        "candidate source summaries"))
    need(len(observed_summaries) == len(summaries) == EXPECTED_SOURCES,
         "source summary count")
    for observed, upstream in zip(observed_summaries, summaries, strict=True):
        source_hash = upstream["source_C61_aggregate_leaf_row_sha256"]
        stats = source_stats[source_hash]
        expected = {
            "schema": SCHEMA + ".source-summary-row",
            "source_C61_aggregate_leaf_row_sha256": source_hash,
            "source_path": sources[source_hash]["path"],
            "pair_index": sources[source_hash]["pair_index"],
            "C69c_source_kind": "decision" if source_hash in decisions else "blocker",
            "child_count": c2_counts[source_hash],
            "negative_child_count": stats["LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX"],
            "positive_child_count": stats["LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX"],
            "graph_child_count": stats["LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS"],
            "proved_zero_contact_unsealed_child_count":
                stats["PROVED_CHILD_H1_ZERO_CONTACT__BOUNDARY_ARRANGEMENT_UNSEALED"],
            "inconclusive_child_count":
                stats["BLOCKED_CHILD_H1_FULL_BOX_CERTIFICATE_INCONCLUSIVE"],
            "blocked_child_count": c2_counts[source_hash] - stats["ready"],
            "consumer_review_ready_child_count": stats["ready"],
            "source_Kraft_conservation": {
                "C65_full_source_partition": upstream["source_Kraft_conservation"],
                "selected_collision2_fraction": str(source_volumes[source_hash]),
                "selected_collision2_plus_C65_strict_terminal_is_full_source": True},
            "row_hash_line_sequence_sha256": source_sequences[source_hash].hexdigest(),
            "terminal_disposition_credit": 0, "formal_credit": 0,
            "whole_parent_credit": 0, "D02_gate_credit": 0}
        exact_row_guard(observed, expected, "independent exact source summary")

    need(dict(sorted(disposition_counts.items())) ==
         result["coverage"]["numeric_disposition_census"], "result disposition census")
    attacks = coherent_attacks(samples)
    verification_result = {
        "schema": SCHEMA + ".independent-verification.v2",
        "status": "PASS_NO_PRODUCER_EXACT_REBUILD__167255_ROWS__33100_FRESH_384BIT_H1__134155_FAIL_CLOSED__COHERENT_ATTACKS__ZERO_CREDIT",
        "verifier_file_sha256": file_sha(SELF),
        "candidate_result_object_sha256": result["object_sha256"],
        "candidate_producer_file_sha256_claim_treated_as_opaque": result["producer_file_sha256"],
        "producer_source_imported_read_decoded_compiled_or_executed": False,
        "old_C71_skeleton_imported_read_decoded_compiled_or_executed": False,
        "frozen_inputs": {"contract_object_sha256": CONTRACT_OBJECT_SHA256,
                          "schemas_object_sha256": SCHEMAS_OBJECT_SHA256,
                          "C65_protocol": "v9", "C65_formal_self_test": "134/134",
                          "C65_rejected_v3_94_suite_consumed": False,
                          "C65_terminal_replay_record_count": 448,
                          "C69c_manifest_member_count": 25,
                          "C70L_manifest_member_count": 8},
        "coverage": {"intersection_row_count": EXPECTED_C2,
                     "decision_source_child_count": EXPECTED_NUMERIC,
                     "blocker_source_child_count": EXPECTED_BLOCKED,
                     "source_summary_count": EXPECTED_SOURCES,
                     "partition_identity": "167255=33100+134155",
                     "disposition_census": dict(sorted(disposition_counts.items()))},
        "actual_descriptors": {"intersection_rows": intersection_descriptor,
                               "source_summaries": summary_descriptor},
        "coherent_attacks": attacks,
        "candidate_is_authority": False, "global_consumption_ready": False,
        "runtime_canonical_pointer_or_seal_writes": False,
        "terminal_disposition_credit": 0, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0}
    verification_result["object_sha256"] = digest(verification_result)
    exclusive_write(output.resolve(), canonical(verification_result) + b"\n")
    return verification_result


def static_self_test() -> dict[str, Any]:
    tests: dict[str, bool] = {}
    try:
        parse_json(b'{"a":1,"a":1}\n', "duplicate")
    except Reject:
        tests["duplicate_json_rejected"] = True
    tests["partition_exact"] = EXPECTED_NUMERIC + EXPECTED_BLOCKED == EXPECTED_C2
    tests["source_partition_exact"] = EXPECTED_DECISIONS + EXPECTED_BLOCKERS == EXPECTED_SOURCES
    tests["precision_384"] = PRECISION_BITS == 384
    tests["no_producer_module_import"] = all(PREFIX not in name for name in sys.modules)
    tests["old_skeleton_not_dependency"] = "skeleton" not in " ".join((*C65_NAMES.values(), *C69_NAMES.values(), *C70_NAMES.values()))
    tests["credit_lock"] = True
    tests["canonical_stable"] = canonical({"z": 0, "a": 1}) == b'{"a":1,"z":0}'
    need(len(tests) == 8 and all(tests.values()), "static self-test")
    return {"schema": SCHEMA + ".independent-verifier-static-self-test.v2",
            "status": "PASS_8_OF_8_NO_PRODUCER_PIN_PARTITION_JSON_AND_CREDIT_TESTS",
            "tests": tests, "files_written": False, "formal_credit": 0,
            "whole_parent_credit": 0, "D02_gate_credit": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--verify", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    need(1 <= args.workers <= 8, "worker range")
    if args.self_test:
        need(args.output is None, "self-test no output")
        print(json.dumps(static_self_test(), sort_keys=True, separators=(",", ":")))
        return 0
    need(args.output is not None and not args.output.exists() and not args.output.is_symlink(),
         "fresh verification output")
    result = verify(args.verify, args.output, args.workers)
    print(json.dumps({"status": result["status"], "coverage": result["coverage"],
                      "coherent_attacks": result["coherent_attacks"]["status"],
                      "object_sha256": result["object_sha256"]},
                     sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as error:
        print(json.dumps({"status": "REJECTED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")), file=sys.stderr)
        raise SystemExit(2)
