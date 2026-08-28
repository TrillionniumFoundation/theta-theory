#!/usr/bin/env python3
"""Build the exact zero-credit C65-child structural-obligation atlas.

This program is deliberately not a structural decider.  It freezes the exact
input domain on which the five missing deciders must operate.  It joins the
published C65 v3 aggregate to the independently closed C68/C69c source
partition and materializes every still-live C65 ``COLLISION2_HANDOFF`` child
whose source is not one of C69c's full-face decisions.

The program never imports or executes any upstream producer.  Every input is
opened no-follow, required to be a regular single-link file, hashed from the
opened descriptor, parsed with duplicate-key and canonical-byte checks, and
recaptured after the full scan.  Outputs are deterministic, zero-credit, and
created with no-replace semantics in a caller-supplied empty directory.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterable, Iterator, Mapping
import zlib


SELF = Path(__file__).resolve()
OUT = SELF.parent
SCHEMA = "cm2.round306c72.structural-child-obligation-atlas.v1"
PREFIX = "cm2_round306c72_structural_child_obligation_atlas_v1"
LEDGER_NAME = PREFIX + ".jsonl.gz"
RESULT_NAME = PREFIX + "_result.json"
REPORT_NAME = PREFIX + "_report.md"

FILES = {
    "C65_RESULT": "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json",
    "C65_LEAVES": "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz",
    "C65_SOURCES": "cm2_round306c65s18_depth18_64shard_aggregate_source_summary_v1.jsonl.gz",
    "C65_VERIFY": "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v9.json",
    "C65_SELFTEST": "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v9.json",
    "C65_REPLAY": "cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v9.json",
    "C65_MANIFEST": "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v9.sha256",
    "C65_OUTER": "cm2_round306c65s18_64shard_aggregate_independent_cold_outer_receipt_v9.json",
    "C68_RESULT": "cm2_round306c68l_blocker_crosswalk_result_v1.json",
    "C68_TASKS": "cm2_round306c68l_blocker_crosswalk_singleton_structural_tasks_v1.jsonl.gz",
    "C68_VERIFY": "cm2_round306c68l_blocker_crosswalk_independent_verification_v1.json",
    "C68_MANIFEST": "cm2_round306c68l_blocker_crosswalk_manifest_v1.sha256",
    "C69_RESULT": "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json",
    "C69_DECISIONS": "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_decisions.jsonl.gz",
    "C69_BLOCKERS": "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz",
    "C69_VERIFY": "cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json",
    "C69_MANIFEST": "cm2_round306c69c_descriptor_repair_supersession_independent_manifest_v1.sha256",
    "C69_OUTER": "cm2_round306c69c_descriptor_repair_supersession_independent_outer_publication_receipt_v1.json",
}

PINS = {
    "C65_RESULT": "1ca46fb81cc104b727b31d3bb0adbb439ab8dae9123b8cbe05d3c60de0e75457",
    "C65_LEAVES": "4ff1c36a0a6331510da3afb988738f128a3cada04ddd297ac58584579115437d",
    "C65_SOURCES": "de8fa908cbe46e379ff05564c5d8ed0ea97de2875eca05792ad3abf63287f432",
    "C65_VERIFY": "7d4e97bd641da7c5ccc64e8c2ad3d59f21ba3ebd73eb0e4d55c88ad617ee23b4",
    "C65_SELFTEST": "f0609dc4835346e078b5299007b1b31210d28cbf772ac41bb0f390f7047ad274",
    "C65_REPLAY": "c7d99ba4fea05fbd7a3b478f025323c77e5335951e4ff08743ad37ba47fa8e85",
    "C65_MANIFEST": "96b0f082688f16f821104402bc9aba1b7778df36f084a300d978dac95faf43c5",
    "C65_OUTER": "20a52a4c16c84ffd524833c0ee872edfeb6fdec538a1368f619244199814fb1d",
    "C68_RESULT": "81cf9b6e3fbf2330f747af6430410026406cad8a1a2eb862be974235b2b60f37",
    "C68_TASKS": "c2d174d9a7e076a52474cde03e02ecdc11172251fe70a5b0273b4aa57c480b8b",
    "C68_VERIFY": "037dae421cd04132fef64aee95ae47b1a159c8d133b2b050039669afd682f818",
    "C68_MANIFEST": "487b7644abc07634d8290efa689b068f7a1f94c770f43c144b5afb2140dd8958",
    "C69_RESULT": "607fc73ebe3333ca172eb15c0831b8c3d98192c86e20eec7a59a69c4ae4737d4",
    "C69_DECISIONS": "b9bc1cd359c77ee6a5246011925090e5d5557cd88e90d1f5c67fa70a452d1eba",
    "C69_BLOCKERS": "69b3ec294f95cb5ce377e553ae875daab10a5bdb33e860363f6bae122022e606",
    "C69_VERIFY": "b0490ed50de8d615039d864db1071792df0809b928a663fcd4a89981eaf326b6",
    "C69_MANIFEST": "c231941ca4f5f76a95faa81e8390e3f11b5d1af84b645605c52245e6ff214749",
    "C69_OUTER": "2baac1cf22ca8be0163f9027d0365e948107b535df917a25334626110bf2916c",
}

OBJECT_PINS = {
    "C65_RESULT": "79185dbca48f0d228977a006583eb545525cff2d9418160fb190c1f9c5b6c393",
    "C65_VERIFY": "8b8c1c64adf5485709b68e904bfb935f552539c53771ff5dd7b5a5f3ac1987ba",
    "C65_SELFTEST": "540654f9f959f13a25d664e404655fa2570c67a7e1e9e4e6e0022c601a7007d1",
    "C65_REPLAY": "9bd2c1c378066f5e4fb5c86bc83caee721962001c666c7187c9e39693fed7327",
    "C65_OUTER": "5e7e21d9be14fa52ec5e3663bd9863ac023e8beffe8e80dc28925aaeb3ed074d",
    "C68_RESULT": "551c28d03ee59e3fadc2b593dc2575acf911545ce0e6527f9ef0270dfc08d3b2",
    "C68_VERIFY": "214d7294637aaa9140997a1ec1a0e3f11932f3f169647ae1e78f993ea23c39cc",
    "C69_RESULT": "e52904a7d8ba73c855e69e390cd3cf29c233ffe492e6fae74efdf0b6d4d0a6a5",
    "C69_VERIFY": "fd25accfd8c5669d13a09b5f335ae265a751a1fb7f069ac21c64e069a0fc2b29",
    "C69_OUTER": "921a5b16d4102b356f1e2e903a71df5e872c869caa668903bb210fe0dbfed1f3",
}

CATEGORY_CHILD_CENSUS = {
    "COLLISION1_OUTGOING_STATE": 423,
    "REGULAR_BOUNDARY_ARRANGEMENT": 83_759,
    "REGULAR_MULTI_GRAPH_FIRST_TANGENCY": 9_476,
    "REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED": 40_478,
    "SOURCE_GRAZING_ENDPOINT_CHART": 19,
}

CATEGORY_SOURCE_CENSUS = {
    "COLLISION1_OUTGOING_STATE": 3_222,
    "REGULAR_BOUNDARY_ARRANGEMENT": 9_053,
    "REGULAR_FULL_FACE_GRAPH_CELL": 2_356,
    "REGULAR_MULTI_GRAPH_FIRST_TANGENCY": 737,
    "REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED": 5_364,
    "SOURCE_GRAZING_ENDPOINT_CHART": 147,
}

DECIDER_FOR_CATEGORY = {
    "COLLISION1_OUTGOING_STATE": "EXACT_OUTGOING_STATE_ORACLE",
    "REGULAR_BOUNDARY_ARRANGEMENT": "EXACT_BOUNDARY_ARRANGEMENT_ORACLE",
    "REGULAR_MULTI_GRAPH_FIRST_TANGENCY": "EXACT_FIRST_TANGENCY_ORACLE",
    "REGULAR_MULTI_GRAPH_INHERITED_INTERVAL_ORDER_OR_BOUNDARY_UNISOLATED":
        "EXACT_MULTI_GRAPH_ORDER_ORACLE",
    "SOURCE_GRAZING_ENDPOINT_CHART": "EXACT_SOURCE_GRAZING_ENDPOINT_ORACLE",
}

ALLOWED_EXIT_CLASSES = (
    "STRICT_EXCLUSION",
    "KNOWN_COMPONENT_CONNECTION",
    "CEMETERY_OR_SOURCE_GRAZING_TERMINAL",
    "SEALED_COLLISION3_HANDOFF",
)


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


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        need(key not in value, "duplicate JSON key:" + key)
        value[key] = item
    return value


def parse_line(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         label + ": framing")
    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=no_duplicates,
                       parse_constant=lambda token: (_ for _ in ()).throw(Reject(token)))
    need(type(value) is dict and canonical(value) == raw, label + ": canonical")
    return value


def close_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ": row closure")


def close_object(value: Mapping[str, Any], expected: str, label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(claim == expected and claim == digest(body), label + ": object closure")


@dataclass(frozen=True)
class Identity:
    dev: int
    ino: int
    mode: int
    nlink: int
    size: int
    mtime_ns: int
    ctime_ns: int


def identity(value: os.stat_result) -> Identity:
    return Identity(value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                    value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def open_regular(path: Path) -> tuple[int, Identity]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    first = os.fstat(descriptor)
    need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1,
         "regular single-link:" + path.name)
    return descriptor, identity(first)


def finish_read(path: Path, descriptor: int, first: Identity, observed_sha: str,
                expected_sha: str) -> None:
    second = identity(os.fstat(descriptor))
    current = identity(os.stat(path, follow_symlinks=False))
    need(first == second == current, "TOCTOU:" + path.name)
    need(observed_sha == expected_sha, "file pin:" + path.name)


def secure_bytes(path: Path, expected_sha: str, maximum: int = 8 << 20) -> bytes:
    descriptor, first = open_regular(path)
    try:
        raw = bytearray()
        hasher = hashlib.sha256()
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
            raw.extend(block)
            need(len(raw) <= maximum, "bounded read:" + path.name)
        finish_read(path, descriptor, first, hasher.hexdigest(), expected_sha)
        return bytes(raw)
    finally:
        os.close(descriptor)


def secure_json(path: Path, expected_sha: str, object_sha: str) -> dict[str, Any]:
    raw = secure_bytes(path, expected_sha)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "JSON newline:" + path.name)
    value = parse_line(raw[:-1], path.name)
    close_object(value, object_sha, path.name)
    return value


def iter_secure_jsonl(path: Path, expected_sha: str, expected_rows: int,
                      maximum_uncompressed: int = 1 << 30) -> Iterator[dict[str, Any]]:
    descriptor, first = open_regular(path)
    hasher = hashlib.sha256()
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    pending = bytearray()
    count = 0
    expanded = 0
    try:
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
            decoded = decoder.decompress(block)
            expanded += len(decoded)
            need(expanded <= maximum_uncompressed, "gzip expansion bound:" + path.name)
            pending.extend(decoded)
            while True:
                newline = pending.find(b"\n")
                if newline < 0:
                    break
                line = bytes(pending[:newline])
                del pending[:newline + 1]
                value = parse_line(line, path.name + ":" + str(count + 1))
                close_row(value, path.name + ":" + str(count + 1))
                count += 1
                yield value
        tail = decoder.flush()
        expanded += len(tail)
        pending.extend(tail)
        need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
             "single complete gzip member:" + path.name)
        need(not pending, "JSONL terminal newline:" + path.name)
        need(count == expected_rows, "JSONL row count:" + path.name)
        finish_read(path, descriptor, first, hasher.hexdigest(), expected_sha)
    finally:
        os.close(descriptor)


def secure_manifest(path: Path, expected_sha: str) -> dict[str, str]:
    raw = secure_bytes(path, expected_sha, 2 << 20)
    need(raw.endswith(b"\n") and b"\x00" not in raw, "manifest framing:" + path.name)
    result: dict[str, str] = {}
    for line in raw.decode("utf-8", "strict").splitlines():
        sha, separator, name = line.partition("  ")
        need(separator == "  " and len(sha) == 64 and
             all(char in "0123456789abcdef" for char in sha), "manifest line")
        need(name not in result, "manifest duplicate alias")
        result[name] = sha
    return result


def snapshot_identities() -> dict[str, Identity]:
    return {key: identity(os.stat(OUT / name, follow_symlinks=False))
            for key, name in FILES.items()}


def recapture_pins(before: Mapping[str, Identity]) -> None:
    for key, name in FILES.items():
        path = OUT / name
        need(identity(os.stat(path, follow_symlinks=False)) == before[key],
             "post-scan identity:" + name)
        descriptor, first = open_regular(path)
        try:
            hasher = hashlib.sha256()
            while block := os.read(descriptor, 1 << 20):
                hasher.update(block)
            finish_read(path, descriptor, first, hasher.hexdigest(), PINS[key])
        finally:
            os.close(descriptor)


def validate_bundles() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    c65 = secure_json(OUT / FILES["C65_RESULT"], PINS["C65_RESULT"],
                      OBJECT_PINS["C65_RESULT"])
    c65v = secure_json(OUT / FILES["C65_VERIFY"], PINS["C65_VERIFY"],
                       OBJECT_PINS["C65_VERIFY"])
    c65t = secure_json(OUT / FILES["C65_SELFTEST"], PINS["C65_SELFTEST"],
                       OBJECT_PINS["C65_SELFTEST"])
    c65r = secure_json(OUT / FILES["C65_REPLAY"], PINS["C65_REPLAY"],
                       OBJECT_PINS["C65_REPLAY"])
    c65o = secure_json(OUT / FILES["C65_OUTER"], PINS["C65_OUTER"],
                       OBJECT_PINS["C65_OUTER"])
    m65 = secure_manifest(OUT / FILES["C65_MANIFEST"], PINS["C65_MANIFEST"])
    need(c65["status"] == "PASS_COMPLETE_64_SHARD_DEPTH18_REPLACEMENT_AGGREGATE__ZERO_CREDIT",
         "C65 aggregate status")
    need(c65v["status"].startswith("PASS_DUAL_EXTERNAL_PROCESS_COLD_VERIFICATION_V9") and
         c65t["status"].startswith("PASS_134_OF_134_") and len(c65t["tests"]) == 134 and
         all(value is True for value in c65t["tests"].values()), "C65 cold closure")
    need(c65r["status"].startswith("PASS_FULL_RELEASE_VALIDATION") and
         c65o["outer_receipt_published_last"] is True and
         c65o["manifest_members_recaptured_after_publication"] is True,
         "C65 postpublication order")
    for key in ("C65_RESULT", "C65_VERIFY", "C65_SELFTEST", "C65_REPLAY"):
        name = FILES[key]
        need(m65.get("deliverables__" + name) == PINS[key] or
             m65.get("deliverables/" + name) == PINS[key], "C65 manifest member:" + key)
    need(c65["formal_credit"] == c65["whole_parent_credit"] == c65["D02_gate_credit"] ==
         c65v["formal_credit"] == c65v["whole_parent_credit"] == c65v["D02_gate_credit"] == 0,
         "C65 zero credit")

    c68 = secure_json(OUT / FILES["C68_RESULT"], PINS["C68_RESULT"],
                      OBJECT_PINS["C68_RESULT"])
    c68v = secure_json(OUT / FILES["C68_VERIFY"], PINS["C68_VERIFY"],
                       OBJECT_PINS["C68_VERIFY"])
    secure_manifest(OUT / FILES["C68_MANIFEST"], PINS["C68_MANIFEST"])
    need(c68["scope"]["C61_singleton_structural_task_count"] == 20_879 and
         c68["strict_boundary"]["formal_credit"] == 0 and
         c68v["formal_credit"] == 0, "C68 boundary")

    c69 = secure_json(OUT / FILES["C69_RESULT"], PINS["C69_RESULT"],
                      OBJECT_PINS["C69_RESULT"])
    c69v = secure_json(OUT / FILES["C69_VERIFY"], PINS["C69_VERIFY"],
                       OBJECT_PINS["C69_VERIFY"])
    c69o = secure_json(OUT / FILES["C69_OUTER"], PINS["C69_OUTER"],
                       OBJECT_PINS["C69_OUTER"])
    m69 = secure_manifest(OUT / FILES["C69_MANIFEST"], PINS["C69_MANIFEST"])
    need(c69["scope"]["input_task_count"] == 20_879 and
         c69["scope"]["decision_count"] == 2_356 and
         c69["scope"]["total_blocker_count"] == 18_523, "C69 source partition")
    need(c69v["status"].startswith("PASS_COLD_NO_C69_PRODUCER") and
         c69o["formal_credit"] == c69v["formal_credit"] == 0, "C69 cold boundary")
    for key in ("C69_RESULT", "C69_VERIFY"):
        name = FILES[key]
        need(m69.get("deliverables/" + name) == PINS[key] or
             m69.get("deliverables__" + name) == PINS[key], "C69 manifest member:" + key)
    return c65, c68, c69


def exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0),
                         0o644)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "output write:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


class LedgerWriter:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.open("xb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def __enter__(self) -> "LedgerWriter":
        return self

    def write(self, body: dict[str, Any]) -> None:
        body = copy.deepcopy(body)
        body["row_sha256"] = digest(body)
        raw = canonical(body) + b"\n"
        self.gz.write(raw)
        self.sequence.update(body["row_sha256"].encode("ascii") + b"\n")
        self.count += 1

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        raw_sha = hashlib.sha256(self.path.read_bytes()).hexdigest()
        return {
            "filename": self.path.name,
            "order": "C65_AGGREGATE_LEAF_ORDER_FILTERED_TO_C69C_BLOCKER_SOURCES_AND_COLLISION2",
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": raw_sha,
            "size": self.path.stat().st_size,
        }


def validate_result_shape(value: Mapping[str, Any]) -> None:
    partition = value["child_partition"]
    need(partition["C69C_DECISION_SOURCE_CHILDREN"] == 33_100, "decision children")
    need(partition["C69C_BLOCKER_SOURCE_CHILDREN"] == 134_155, "blocker children")
    need(partition["TOTAL_C65_COLLISION2_HANDOFF_CHILDREN"] == 167_255, "total children")
    need(partition["C69C_DECISION_SOURCE_CHILDREN"] +
         partition["C69C_BLOCKER_SOURCE_CHILDREN"] ==
         partition["TOTAL_C65_COLLISION2_HANDOFF_CHILDREN"], "partition sum")
    need(value["blocker_child_category_census"] == CATEGORY_CHILD_CENSUS,
         "category child census")
    need(sum(value["blocker_child_category_census"].values()) == 134_155,
         "category child sum")
    need(value["source_category_census"] == CATEGORY_SOURCE_CENSUS,
         "source category census")
    need(value["allowed_exit_classes"] == list(ALLOWED_EXIT_CLASSES), "exit classes")
    need(set(value["required_deciders"]) == set(DECIDER_FOR_CATEGORY.values()), "deciders")
    boundary = value["strict_boundary"]
    need(boundary == {
        "candidate_is_authority": False,
        "decider_execution_performed": False,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
        "global_consumption_ready": False,
        "runtime_canonical_pointer_or_seal_writes": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }, "strict boundary")


def coherent_self_test(base: dict[str, Any]) -> dict[str, Any]:
    tests: dict[str, bool] = {}

    def attacked(name: str, mutation: Any) -> None:
        candidate = copy.deepcopy(base)
        mutation(candidate)
        try:
            validate_result_shape(candidate)
        except (Reject, KeyError, TypeError, ValueError):
            tests[name] = True
        else:
            tests[name] = False

    attacked("decision_child_count", lambda v: v["child_partition"].__setitem__(
        "C69C_DECISION_SOURCE_CHILDREN", 33_101))
    attacked("blocker_child_count", lambda v: v["child_partition"].__setitem__(
        "C69C_BLOCKER_SOURCE_CHILDREN", 134_154))
    attacked("total_child_count", lambda v: v["child_partition"].__setitem__(
        "TOTAL_C65_COLLISION2_HANDOFF_CHILDREN", 167_254))
    for index, category in enumerate(CATEGORY_CHILD_CENSUS):
        attacked("category_" + str(index), lambda v, key=category:
                 v["blocker_child_category_census"].__setitem__(
                     key, v["blocker_child_category_census"][key] + 1))
    attacked("unknown_category", lambda v: v["blocker_child_category_census"].__setitem__(
        "UNKNOWN", 0))
    attacked("source_census", lambda v: v["source_category_census"].__setitem__(
        "REGULAR_FULL_FACE_GRAPH_CELL", 2_355))
    attacked("exit_class", lambda v: v["allowed_exit_classes"].append("LOCAL_TERMINAL"))
    attacked("decider_missing", lambda v: v["required_deciders"].pop())
    for field in ("candidate_is_authority", "decider_execution_performed",
                  "global_consumption_ready", "runtime_canonical_pointer_or_seal_writes"):
        attacked("boundary_" + field,
                 lambda v, key=field: v["strict_boundary"].__setitem__(key, True))
    for field in ("formal_credit", "whole_parent_credit", "D02_gate_credit"):
        attacked("credit_" + field,
                 lambda v, key=field: v["strict_boundary"].__setitem__(key, 1))
    attacked("CM2", lambda v: v["strict_boundary"].__setitem__("CM2", "CLAIM"))
    need(all(tests.values()), "coherent self-test")
    return {
        "status": "PASS_%d_OF_%d_COHERENT_PARTITION_AND_CREDIT_ATTACKS_FAIL_CLOSED" %
                  (len(tests), len(tests)),
        "attack_count": len(tests),
        "attacks": dict(sorted(tests.items())),
    }


def build(stage: Path) -> dict[str, Any]:
    need(stage.is_dir() and not any(stage.iterdir()), "empty build directory")
    before = snapshot_identities()
    c65, c68, c69 = validate_bundles()

    c68_tasks: dict[str, dict[str, Any]] = {}
    source_categories = Counter()
    for row in iter_secure_jsonl(OUT / FILES["C68_TASKS"], PINS["C68_TASKS"], 20_879):
        source = row["C61_aggregate_leaf_row_sha256"]
        need(source not in c68_tasks, "duplicate C68 source")
        need(row["formal_credit"] == row["whole_parent_credit"] ==
             row["D02_gate_credit"] == 0, "C68 row credit")
        c68_tasks[source] = row
        source_categories[row["structural_graph_kind"]] += 1
    need(dict(source_categories) == CATEGORY_SOURCE_CENSUS, "C68 category census")

    source_partition: dict[str, dict[str, Any]] = {}
    for row in iter_secure_jsonl(OUT / FILES["C69_DECISIONS"], PINS["C69_DECISIONS"], 2_356):
        source = row["C61_aggregate_leaf_row_sha256"]
        task = c68_tasks[source]
        need(task["structural_graph_kind"] == "REGULAR_FULL_FACE_GRAPH_CELL" and
             row["C68_structural_task_row_sha256"] == task["row_sha256"],
             "C69 decision lineage")
        need(source not in source_partition, "duplicate C69 decision source")
        source_partition[source] = {"kind": "DECISION", "row": row, "task": task}
    for row in iter_secure_jsonl(OUT / FILES["C69_BLOCKERS"], PINS["C69_BLOCKERS"], 18_523):
        source = row["C61_aggregate_leaf_row_sha256"]
        task = c68_tasks[source]
        need(task["structural_graph_kind"] == row["structural_graph_kind"] and
             row["C68_structural_task_row_sha256"] == task["row_sha256"],
             "C69 blocker lineage")
        need(source not in source_partition, "duplicate C69 blocker source")
        source_partition[source] = {"kind": "BLOCKER", "row": row, "task": task}
    need(len(source_partition) == len(c68_tasks) == 20_879, "complete source partition")

    summaries: dict[str, dict[str, Any]] = {}
    for row in iter_secure_jsonl(OUT / FILES["C65_SOURCES"], PINS["C65_SOURCES"], 20_879):
        source = row["source_C61_aggregate_leaf_row_sha256"]
        need(source in source_partition and source not in summaries, "C65 source summary join")
        need(row["formal_credit"] == row["whole_parent_credit"] == row["D02_gate_credit"] == 0,
             "C65 source credit")
        summaries[source] = row

    observed_source = defaultdict(Counter)
    all_dispositions = Counter()
    blocker_children = Counter()
    decision_children = 0
    total_rows = 0
    ledger_path = stage / LEDGER_NAME
    with LedgerWriter(ledger_path) as writer:
        for child in iter_secure_jsonl(OUT / FILES["C65_LEAVES"], PINS["C65_LEAVES"], 358_919):
            total_rows += 1
            source = child["source_C61_aggregate_leaf_row_sha256"]
            need(source in source_partition, "C65 leaf source join")
            entry = source_partition[source]
            task = entry["task"]
            need(child["pair_index"] == task["pair_index"] and
                 child["source_path"] == task["path"] and
                 child["path"].startswith(task["path"]), "C65 child lineage")
            need(child["formal_credit"] == child["whole_parent_credit"] ==
                 child["D02_gate_credit"] == 0, "C65 child credit")
            disposition = child["disposition"]
            need(disposition in {"STRICT_TERMINAL", "COLLISION2_HANDOFF"},
                 "C65 disposition")
            all_dispositions[disposition] += 1
            observed_source[source][disposition] += 1
            observed_source[source]["ALL"] += 1
            if disposition != "COLLISION2_HANDOFF":
                continue
            if entry["kind"] == "DECISION":
                decision_children += 1
                continue
            category = task["structural_graph_kind"]
            blocker_children[category] += 1
            blocker = entry["row"]
            writer.write({
                "schema": SCHEMA + ".obligation-row",
                "C65_aggregate_child_row_sha256": child["row_sha256"],
                "C65_source_shard_row_sha256": child["source_C65_shard_row_sha256"],
                "C61_aggregate_leaf_row_sha256": source,
                "C68_structural_task_row_sha256": task["row_sha256"],
                "C69c_blocker_row_sha256": blocker["row_sha256"],
                "pair_index": child["pair_index"],
                "source_path": child["source_path"],
                "child_path": child["path"],
                "parent_volume_fraction": child["parent_volume_fraction"],
                "exact_representative_box": child["exact_representative_box"],
                "exact_reflected_box": child["exact_reflected_box"],
                "structural_category": category,
                "required_decider": DECIDER_FOR_CATEGORY[category],
                "source_route_classification": task["residual_classification"],
                "source_route_witness": task["route_witness"],
                "child_route_classification": child["route_classification"],
                "child_route_witness": child["route_witness"],
                "source_grazing": task["source_grazing"],
                "blocker_codes": blocker["blocker_codes"],
                "allowed_exit_classes": list(ALLOWED_EXIT_CLASSES),
                "current_disposition": "FAIL_CLOSED_STRUCTURAL_OBLIGATION",
                "formal_credit": 0,
                "whole_parent_credit": 0,
                "D02_gate_credit": 0,
            })
    descriptor = writer.descriptor()
    need(total_rows == 358_919 and all_dispositions == Counter({
        "STRICT_TERMINAL": 191_664, "COLLISION2_HANDOFF": 167_255}),
         "C65 aggregate leaf census")
    need(decision_children == 33_100 and dict(blocker_children) == CATEGORY_CHILD_CENSUS and
         descriptor["row_count"] == 134_155, "child obligation partition")
    for source, summary in summaries.items():
        observed = observed_source[source]
        need(observed["ALL"] == summary["output_leaf_count"] and
             observed["STRICT_TERMINAL"] == summary["strict_terminal_leaf_count"] and
             observed["COLLISION2_HANDOFF"] == summary["collision2_handoff_leaf_count"],
             "C65 per-source census")

    result: dict[str, Any] = {
        "schema": SCHEMA + ".result",
        "status": "PASS_EXACT_C65_V3_CHILD_OBLIGATION_PARTITION__33100_C71_ELIGIBLE__134155_FIVE_STRUCTURAL_DECIDERS__ZERO_CREDIT",
        "producer_file_sha256": hashlib.sha256(SELF.read_bytes()).hexdigest(),
        "input_file_sha256": dict(PINS),
        "input_object_sha256": dict(OBJECT_PINS),
        "upstream_bundle_status": {
            "C65": c65["status"],
            "C68": c68["status"],
            "C69c": c69["status"],
        },
        "source_partition": {"C69C_DECISIONS": 2_356, "C69C_BLOCKERS": 18_523,
                             "TOTAL": 20_879},
        "source_category_census": dict(source_categories),
        "child_partition": {
            "C69C_DECISION_SOURCE_CHILDREN": decision_children,
            "C69C_BLOCKER_SOURCE_CHILDREN": descriptor["row_count"],
            "TOTAL_C65_COLLISION2_HANDOFF_CHILDREN": all_dispositions["COLLISION2_HANDOFF"],
        },
        "blocker_child_category_census": dict(blocker_children),
        "required_deciders": sorted(DECIDER_FOR_CATEGORY.values()),
        "allowed_exit_classes": list(ALLOWED_EXIT_CLASSES),
        "ledger": descriptor,
        "global_contract": {
            "additional_dyadic_depth_is_not_a_structural_decider": True,
            "every_child_requires_exact_full_box_or_exact_glued_stratum_proof": True,
            "partial_local_decisions_are_not_formal_credit": True,
            "only_a_later_no_producer_global_consumer_may_set_unresolved_zero": True,
        },
        "strict_boundary": {
            "candidate_is_authority": False,
            "decider_execution_performed": False,
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
            "global_consumption_ready": False,
            "runtime_canonical_pointer_or_seal_writes": False,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    validate_result_shape(result)
    result["producer_self_test"] = coherent_self_test(result)
    result["object_sha256"] = digest(result)
    exclusive(stage / RESULT_NAME, canonical(result) + b"\n")
    report = (
        "# C72 exact structural child-obligation atlas v1\n\n"
        f"Status: `{result['status']}`\n\n"
        "The frozen C65 v3 collision-2 child domain closes exactly as "
        "`167,255 = 33,100 + 134,155`.  The 134,155 fail-closed children are "
        "partitioned into boundary arrangement 83,759; inherited multi-graph order "
        "40,478; first tangency 9,476; outgoing state 423; source grazing 19.\n\n"
        "This atlas performs no structural decision and grants no credit.  Each row "
        "is bound to its C65 child, C61 source, C68 task, and C69c blocker, and may "
        "exit only through strict exclusion, known-component connection, cemetery/"
        "source-grazing terminal, or a complete sealed collision-3 handoff.\n\n"
        f"Ledger SHA256: `{descriptor['sha256']}`; rows: `{descriptor['row_count']}`.\n"
        f"Result object: `{result['object_sha256']}`.\n"
    )
    exclusive(stage / REPORT_NAME, report.encode("utf-8"))
    recapture_pins(before)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-dir", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        result = build(arguments.build_dir.resolve())
    except (Reject, OSError, ValueError, KeyError, TypeError, zlib.error) as error:
        print("REJECT_C72:" + str(error))
        return 2
    print(result["status"])
    print(result["object_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
