#!/usr/bin/env python3
"""Cold no-producer verifier for the C72 structural child-obligation atlas.

The C72 producer is outside this verifier's runtime input set: this program
does not open, import, execute, parse, or decode it.  Instead it independently
rebuilds every candidate obligation row from the pinned C65-v9, C68, and C69c
publication bytes and compares the rebuild to the candidate stream in exact
C65 aggregate-leaf order.

Both isolated candidate directories are required.  Their three candidate
members must be byte-identical, regular single-link files.  All JSON and JSONL
is duplicate-key-free, canonical, hash-closed, bounded, and read through held
O_NOFOLLOW descriptors with pre/post identity checks.  Every input byte pin is
recaptured after the full rebuild.  The only permitted write is an O_EXCL
independent-verification object in the selected candidate staging directory.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterator, Mapping
import zlib


sys.dont_write_bytecode = True

SELF = Path(__file__).absolute()
ROOT = SELF.parents[1]
OUT = ROOT / "deliverables"
SCHEMA = "cm2.round306c72.structural-child-obligation-atlas.v1"
VERIFY_SCHEMA = SCHEMA + ".independent-verification.v1"
PREFIX = "cm2_round306c72_structural_child_obligation_atlas_v1"
LEDGER_NAME = PREFIX + ".jsonl.gz"
RESULT_NAME = PREFIX + "_result.json"
REPORT_NAME = PREFIX + "_report.md"
VERIFY_NAME = "cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json"

# Declaration-only binding.  There is deliberately no producer path constant.
C72_PRODUCER_FILE_SHA256 = "327e10072639db30075576f317d5171d3d4d7e49b385d4d3367341979bdd5ca4"
CANDIDATE_PINS = {
    "ledger": "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370",
    "result": "55318b7c3ee778cb8a0e41d612c9c2caa44790e6fff816a6104116268258f01e",
    "report": "bd28ef086f3ab607bc1b12ee5eb71d89263805c4e04e16316b8a05332282fae1",
}
CANDIDATE_OBJECT_SHA256 = "a6aa0cfd8e1ee1b7a02d92af066acb23abffb22b0b7276b7e233d2ff7d92f9f4"
CANDIDATE_LEDGER_SIZE = 23_266_147
CANDIDATE_LEDGER_SEQUENCE = "2cd348f1821c5d2158008bc8fda4c500388902e385a31e87e281cd6a69be587b"

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

LEDGER_SPECS = {
    "C65_LEAVES": (358_919, "800e0c412b83aef7a2d5eb05a80e8d39c3b83dfe1e9bf57a3543ca9c8b55fe9c"),
    "C65_SOURCES": (20_879, "8d978e31d34f8a467c9cfc6df953608775c9cc3a797c2e859ab55b6f093da9f4"),
    "C68_TASKS": (20_879, "ddfc6e3c51a9794a1970e8d7d230cbbadf05c2c4009f686887c4219a1baa72b8"),
    "C69_DECISIONS": (2_356, "706e6d15b3cf5a9f010c20e77974528399696dd2df18f4c65ceabfe1c4a4c040"),
    "C69_BLOCKERS": (18_523, "7b14e43030218bb448a3192e1e27a03e48ebf0a1627f8cd59a6167c7fb39e7e7"),
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

C68_TASK_KEYS = {
    "schema", "C61_aggregate_leaf_row_sha256", "C61_continuation_object_sha256",
    "C65_assignment_row_sha256", "C65_shard_id", "pair_index", "path",
    "parent_volume_fraction", "exact_representative_box_object_sha256",
    "exact_reflected_box_object_sha256", "residual_classification", "route_witness",
    "structural_graph_kind", "owner_candidate", "incoming_chart",
    "outgoing_factor_candidate", "official_word_key_id", "official_word_variant_id",
    "source_grazing", "C65_capability_for_this_task", "structural_decider_available",
    "required_next", "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "row_sha256",
}
C69_BLOCKER_KEYS = {
    "schema", "C61_aggregate_leaf_row_sha256", "C68_structural_task_row_sha256",
    "pair_index", "path", "parent_volume_fraction",
    "exact_representative_box_object_sha256", "route_classification", "route_witness",
    "structural_graph_kind", "additional_dyadic_source_depth_recommended",
    "capability_decision_available", "blocker_codes", "formal_credit",
    "whole_parent_credit", "D02_gate_credit", "row_sha256",
}
OBLIGATION_KEYS = {
    "schema", "C65_aggregate_child_row_sha256", "C65_source_shard_row_sha256",
    "C61_aggregate_leaf_row_sha256", "C68_structural_task_row_sha256",
    "C69c_blocker_row_sha256", "pair_index", "source_path", "child_path",
    "parent_volume_fraction", "exact_representative_box", "exact_reflected_box",
    "structural_category", "required_decider", "source_route_classification",
    "source_route_witness", "child_route_classification", "child_route_witness",
    "source_grazing", "blocker_codes", "allowed_exit_classes",
    "current_disposition", "formal_credit", "whole_parent_credit", "D02_gate_credit",
    "row_sha256",
}


class Reject(RuntimeError):
    """Fail-closed verification rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


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
         label + ":framing")
    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=no_duplicates,
        parse_constant=lambda token: (_ for _ in ()).throw(Reject("constant:" + token)),
    )
    need(type(value) is dict and canonical(value) == raw, label + ":canonical")
    return value


def close_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row-closure")


def close_object(value: Mapping[str, Any], expected: str, label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(type(claim) is str and claim == expected == digest(body), label + ":object-closure")


def close_object_self(value: Mapping[str, Any], label: str) -> None:
    claim = value.get("object_sha256")
    need(type(claim) is str, label + ":object-claim")
    close_object(value, claim, label)


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


def require_directory(path: Path, label: str) -> None:
    observed = os.lstat(path)
    need(stat.S_ISDIR(observed.st_mode) and not stat.S_ISLNK(observed.st_mode),
         label + ":real-directory")


def open_regular(path: Path) -> tuple[int, Identity]:
    before = identity(os.lstat(path))
    need(stat.S_ISREG(before.mode) and before.nlink == 1,
         "regular-single-link:" + path.name)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    opened = identity(os.fstat(descriptor))
    need(before == opened, "path-fd-identity:" + path.name)
    return descriptor, opened


def finish_read(path: Path, descriptor: int, first: Identity, observed_sha: str,
                expected_sha: str) -> None:
    need(identity(os.fstat(descriptor)) == first, "fd-post-identity:" + path.name)
    need(identity(os.lstat(path)) == first, "path-post-identity:" + path.name)
    need(observed_sha == expected_sha, "file-pin:" + path.name)


def secure_bytes(path: Path, expected_sha: str, maximum: int = 8 << 20) -> bytes:
    descriptor, first = open_regular(path)
    output = bytearray()
    hasher = hashlib.sha256()
    try:
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
            output.extend(block)
            need(len(output) <= maximum, "bounded-read:" + path.name)
        finish_read(path, descriptor, first, hasher.hexdigest(), expected_sha)
        return bytes(output)
    finally:
        os.close(descriptor)


def secure_unpinned_bytes(path: Path, maximum: int = 8 << 20) -> tuple[bytes, str]:
    descriptor, first = open_regular(path)
    output = bytearray()
    hasher = hashlib.sha256()
    try:
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
            output.extend(block)
            need(len(output) <= maximum, "bounded-unpinned-read:" + path.name)
        observed = hasher.hexdigest()
        finish_read(path, descriptor, first, observed, observed)
        return bytes(output), observed
    finally:
        os.close(descriptor)


def secure_json(path: Path, expected_sha: str, object_sha: str) -> dict[str, Any]:
    raw = secure_bytes(path, expected_sha)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "JSON-newline:" + path.name)
    value = parse_line(raw[:-1], path.name)
    close_object(value, object_sha, path.name)
    return value


def iter_secure_jsonl(path: Path, expected_sha: str, expected_rows: int,
                      expected_sequence: str, maximum_uncompressed: int) -> Iterator[dict[str, Any]]:
    descriptor, first = open_regular(path)
    hasher = hashlib.sha256()
    sequence = hashlib.sha256()
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    pending = b""
    count = 0
    expanded = 0
    try:
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            need(not decoder.eof, "gzip-trailing-member:" + path.name)
            hasher.update(block)
            decoded = decoder.decompress(block)
            need(not decoder.unused_data and not decoder.unconsumed_tail,
                 "single-gzip-member:" + path.name)
            expanded += len(decoded)
            need(expanded <= maximum_uncompressed, "gzip-expansion-bound:" + path.name)
            parts = (pending + decoded).split(b"\n")
            pending = parts.pop()
            for raw in parts:
                count += 1
                value = parse_line(raw, path.name + ":" + str(count))
                close_row(value, path.name + ":" + str(count))
                sequence.update(value["row_sha256"].encode("ascii") + b"\n")
                yield value
        tail = decoder.flush()
        expanded += len(tail)
        need(expanded <= maximum_uncompressed, "gzip-flush-bound:" + path.name)
        parts = (pending + tail).split(b"\n")
        pending = parts.pop()
        for raw in parts:
            count += 1
            value = parse_line(raw, path.name + ":" + str(count))
            close_row(value, path.name + ":" + str(count))
            sequence.update(value["row_sha256"].encode("ascii") + b"\n")
            yield value
        need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
             "complete-single-gzip-member:" + path.name)
        need(not pending, "JSONL-terminal-newline:" + path.name)
        need(count == expected_rows, "JSONL-row-count:" + path.name)
        need(sequence.hexdigest() == expected_sequence, "JSONL-row-sequence:" + path.name)
        finish_read(path, descriptor, first, hasher.hexdigest(), expected_sha)
    finally:
        os.close(descriptor)


def secure_manifest(path: Path, expected_sha: str) -> tuple[dict[str, str], list[str]]:
    raw = secure_bytes(path, expected_sha, 4 << 20)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n") and b"\x00" not in raw,
         "manifest-framing:" + path.name)
    entries: dict[str, str] = {}
    order: list[str] = []
    for index, line in enumerate(raw.decode("utf-8", "strict").splitlines(), 1):
        sha, separator, name = line.partition("  ")
        need(separator == "  " and len(sha) == 64 and
             all(char in "0123456789abcdef" for char in sha) and bool(name),
             "manifest-line:" + path.name + ":" + str(index))
        need(name not in entries, "manifest-duplicate-alias:" + name)
        entries[name] = sha
        order.append(name)
    return entries, order


def sequence_hash(values: Iterator[str] | list[str]) -> str:
    value = hashlib.sha256()
    for item in values:
        value.update(item.encode("utf-8") + b"\n")
    return value.hexdigest()


def compare_secure_files(left: Path, right: Path, expected_sha: str) -> None:
    left_fd, left_id = open_regular(left)
    right_fd, right_id = open_regular(right)
    left_hash = hashlib.sha256()
    right_hash = hashlib.sha256()
    try:
        while True:
            left_block = os.read(left_fd, 1 << 20)
            right_block = os.read(right_fd, 1 << 20)
            need(left_block == right_block, "dual-build-byte-mismatch:" + left.name)
            if not left_block:
                break
            left_hash.update(left_block)
            right_hash.update(right_block)
        finish_read(left, left_fd, left_id, left_hash.hexdigest(), expected_sha)
        finish_read(right, right_fd, right_id, right_hash.hexdigest(), expected_sha)
    finally:
        os.close(left_fd)
        os.close(right_fd)


def input_paths(primary: Path, peer: Path) -> tuple[dict[str, Path], dict[str, str]]:
    paths = {"upstream:" + key: OUT / name for key, name in FILES.items()}
    pins = {"upstream:" + key: PINS[key] for key in FILES}
    for label, directory in (("primary", primary), ("peer", peer)):
        for member, name in (("ledger", LEDGER_NAME), ("result", RESULT_NAME),
                             ("report", REPORT_NAME)):
            paths[label + ":" + member] = directory / name
            pins[label + ":" + member] = CANDIDATE_PINS[member]
    return paths, pins


def snapshot_inputs(paths: Mapping[str, Path]) -> dict[str, Identity]:
    result: dict[str, Identity] = {}
    for key, path in paths.items():
        observed = identity(os.lstat(path))
        need(stat.S_ISREG(observed.mode) and observed.nlink == 1,
             "snapshot-regular-single-link:" + key)
        result[key] = observed
    return result


def recapture_inputs(paths: Mapping[str, Path], pins: Mapping[str, str],
                     before: Mapping[str, Identity]) -> None:
    for key, path in paths.items():
        need(identity(os.lstat(path)) == before[key], "full-scan-identity:" + key)
        descriptor, first = open_regular(path)
        hasher = hashlib.sha256()
        try:
            while True:
                block = os.read(descriptor, 1 << 20)
                if not block:
                    break
                hasher.update(block)
            finish_read(path, descriptor, first, hasher.hexdigest(), pins[key])
        finally:
            os.close(descriptor)


def manifest_member(entries: Mapping[str, str], name: str, expected: str,
                    prefixes: tuple[str, ...]) -> None:
    matches = [entries.get(prefix + name) for prefix in prefixes]
    need(expected in matches, "manifest-member:" + name)


def zero_credit(value: Mapping[str, Any], label: str,
                runtime_key: str = "runtime_canonical_pointer_or_seal_writes") -> None:
    need(value["formal_credit"] == value["whole_parent_credit"] ==
         value["D02_gate_credit"] == 0, label + ":zero-credit")
    need(value.get("candidate_is_authority", value.get("candidate_is_installed_authority", False))
         is False, label + ":non-authority")
    need(value[runtime_key] is False, label + ":no-runtime-write")


def require_descriptor(value: Mapping[str, Any], filename: str, order: str,
                       row_count: int, sequence: str, sha: str) -> None:
    need(value == {
        "filename": filename,
        "order": order,
        "row_count": row_count,
        "row_hash_line_sequence_sha256": sequence,
        "sha256": sha,
        "size": (OUT / filename).stat().st_size,
    }, "upstream-ledger-descriptor:" + filename)


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
    m65, m65_order = secure_manifest(OUT / FILES["C65_MANIFEST"], PINS["C65_MANIFEST"])
    need(c65["status"] ==
         "PASS_COMPLETE_64_SHARD_DEPTH18_REPLACEMENT_AGGREGATE__ZERO_CREDIT",
         "C65-result-status")
    zero_credit(c65, "C65-result")
    need(c65["coverage"]["replacement_output_leaf_count"] == 358_919 and
         c65["coverage"]["replacement_disposition_census"] == {
             "STRICT_TERMINAL": 191_664, "COLLISION2_HANDOFF": 167_255,
             "COLLISION3_READY": 0,
         } and c65["coverage"]["C61_full_base_collision2_sources_replaced"] == 20_879,
         "C65-result-domain")
    require_descriptor(c65["ledgers"]["aggregate_leaves"], FILES["C65_LEAVES"],
                       "C61_V4_FILTERED_C2_ORDER_THEN_CHILD_PATH", *LEDGER_SPECS["C65_LEAVES"],
                       PINS["C65_LEAVES"])
    require_descriptor(c65["ledgers"]["source_summaries"], FILES["C65_SOURCES"],
                       "C61_V4_FILTERED_C2_ORDER", *LEDGER_SPECS["C65_SOURCES"],
                       PINS["C65_SOURCES"])
    need(c65v["status"] ==
         "PASS_DUAL_EXTERNAL_PROCESS_COLD_VERIFICATION_V9__DISTINCT_STARTTICKS__EXACT_FROZEN_VECTOR__ZERO_CREDIT",
         "C65-v9-status")
    zero_credit(c65v, "C65-v9")
    dual = c65v["dual_process_evidence"]
    need(dual["byte_identical"] is True and dual["different_pid_and_startticks"] is True and
         len(set(dual["worker_pids"])) == len(set(dual["worker_startticks"])) == 2 and
         dual["projection_file_sha256"] ==
         "133bffae1b0244714fb7b752040e157dd7d0b9de2111d7e2b5c10298478e5cbd",
         "C65-v9-dual-isolation")
    need(c65v["invariants"]["sealed_python_flint_runtime_and_384bit_context_replayed"] is True and
         c65v["invariants"]["all_20879_depth6_numeric_DFS_rows_recomputed"] is True and
         c65v["invariants"]["all_frozen_inputs_identity_and_bytes_recaptured_after_long_run"] is True and
         c65v["independence"]["C65_programs_imported_or_executed"] is False,
         "C65-v9-cold-invariants")
    need(c65t["status"] ==
         "PASS_134_OF_134_PROTOCOL_FILESYSTEM_SCHEMA_LOADER_PROVENANCE_MANIFEST_WORKER_TRANSPORT_AND_C61_BASELINE_ATTACKS" and
         c65t["test_count"] == len(c65t["tests"]) == 134 and
         all(value is True for value in c65t["tests"].values()), "C65-v9-134-selftest")
    zero_credit(c65t, "C65-v9-selftest")
    need(c65r["status"] ==
         "PASS_FULL_RELEASE_VALIDATION_AND_POSTPUBLICATION_RECAPTURE__ZERO_CREDIT" and
         c65r["verification_file_sha256"] == PINS["C65_VERIFY"] and
         c65r["verification_object_sha256"] == OBJECT_PINS["C65_VERIFY"] and
         c65r["self_test_file_sha256"] == PINS["C65_SELFTEST"] and
         c65r["self_test_object_sha256"] == OBJECT_PINS["C65_SELFTEST"] and
         c65r["manifest_and_outer_receipt_published_after_this_result"] is True,
         "C65-v9-replay")
    zero_credit(c65r, "C65-v9-replay")
    need(len(m65) == len(m65_order) == 446, "C65-one-global-manifest-count")
    for key in ("C65_RESULT", "C65_LEAVES", "C65_SOURCES", "C65_VERIFY",
                "C65_SELFTEST", "C65_REPLAY"):
        manifest_member(m65, FILES[key], PINS[key], ("deliverables__", "deliverables/"))
    need(c65o["status"] ==
         "PASS_ONE_GLOBAL_FROZEN_MANIFEST_AND_FULL_POSTPUBLICATION_RECAPTURE__ZERO_CREDIT" and
         c65o["manifest_file_sha256"] == PINS["C65_MANIFEST"] and
         c65o["manifest_member_count"] == 446 and
         c65o["manifest_ordered_alias_sequence_sha256"] == sequence_hash(m65_order) and
         c65o["manifest_recaptured_and_parsed_after_publication"] is True and
         c65o["manifest_members_recaptured_after_publication"] is True and
         c65o["manifest_member_bytes_and_identities_unchanged"] is True and
         c65o["outer_receipt_published_last"] is True, "C65-v9-outer-last")
    zero_credit(c65o, "C65-v9-outer")

    c68 = secure_json(OUT / FILES["C68_RESULT"], PINS["C68_RESULT"],
                      OBJECT_PINS["C68_RESULT"])
    c68v = secure_json(OUT / FILES["C68_VERIFY"], PINS["C68_VERIFY"],
                       OBJECT_PINS["C68_VERIFY"])
    m68, _ = secure_manifest(OUT / FILES["C68_MANIFEST"], PINS["C68_MANIFEST"])
    need(c68["status"] ==
         "PASS_FAIL_CLOSED_BLOCKER_CROSSWALK__OWNER_1042_HISTORY_1042__DIRECT_C41_LOCAL_350_WHOLE_89__MARGIN_PENDING__20879_SINGLETON_STRUCTURAL_TASKS__ZERO_CREDIT" and
         c68["scope"]["C61_singleton_structural_task_count"] == 20_879 and
         c68["strict_boundary"]["formal_credit"] ==
         c68["strict_boundary"]["D02_gate_credit"] == 0 and
         c68["strict_boundary"]["runtime_or_canonical_written"] is False,
         "C68-zero-credit-domain")
    require_descriptor(c68["ledgers"]["singleton_structural_tasks"], FILES["C68_TASKS"],
                       "C61_FILTERED_COLLISION2_HANDOFF_ORDER", *LEDGER_SPECS["C68_TASKS"],
                       PINS["C68_TASKS"])
    need(c68v["status"].startswith("PASS_COLD_NO_PRODUCER_IMPORT_OR_EXECUTION") and
         c68v["producer_imported"] is c68v["producer_executed"] is False and
         c68v["formal_credit"] == c68v["D02_gate_credit"] == 0 and
         c68v["runtime_or_canonical_written"] is False and c68v["CM2"] == "NO-GO_FOR_CLAIM",
         "C68-independent-closure")
    for key in ("C68_RESULT", "C68_TASKS", "C68_VERIFY"):
        manifest_member(m68, FILES[key], PINS[key], ("", "deliverables/", "deliverables__"))

    c69 = secure_json(OUT / FILES["C69_RESULT"], PINS["C69_RESULT"],
                      OBJECT_PINS["C69_RESULT"])
    c69v = secure_json(OUT / FILES["C69_VERIFY"], PINS["C69_VERIFY"],
                       OBJECT_PINS["C69_VERIFY"])
    c69o = secure_json(OUT / FILES["C69_OUTER"], PINS["C69_OUTER"],
                       OBJECT_PINS["C69_OUTER"])
    m69, _ = secure_manifest(OUT / FILES["C69_MANIFEST"], PINS["C69_MANIFEST"])
    need(c69["status"] ==
         "PASS_C69B_SEALED_LEDGER_DESCRIPTOR_REPAIR_SUPERSESSION__ZERO_CREDIT" and
         c69["scope"]["input_task_count"] == 20_879 and
         c69["scope"]["decision_count"] == 2_356 and
         c69["scope"]["total_blocker_count"] == 18_523 and
         c69["strict_boundary"] == {
             "CM2": "NO-GO_FOR_CLAIM", "D02_gate_credit": 0,
             "candidate_is_installed_authority": False,
             "decisions_are_terminal_dispositions": False, "formal_credit": 0,
             "runtime_or_canonical_written": False, "whole_parent_credit": 0,
         }, "C69c-zero-credit-partition")
    require_descriptor(c69["ledgers"]["decisions"], FILES["C69_DECISIONS"],
                       "C68_C61_FILTERED_ORDER", *LEDGER_SPECS["C69_DECISIONS"],
                       PINS["C69_DECISIONS"])
    require_descriptor(c69["ledgers"]["blockers"], FILES["C69_BLOCKERS"],
                       "C68_C61_FILTERED_ORDER", *LEDGER_SPECS["C69_BLOCKERS"],
                       PINS["C69_BLOCKERS"])
    need(c69v["status"].startswith("PASS_COLD_NO_C69_PRODUCER_OR_WRAPPER_IMPORT_EXECUTION_READ_OR_DECODE") and
         c69v["producer_imported"] is c69v["producer_executed"] is False and
         c69v["producer_or_wrapper_source_read_or_decoded"] is False and
         c69v["formal_credit"] == c69v["whole_parent_credit"] ==
         c69v["D02_gate_credit"] == 0 and c69v["runtime_or_canonical_written"] is False and
         c69v["CM2"] == "NO-GO_FOR_CLAIM", "C69c-independent-closure")
    need(c69o["formal_credit"] == c69o["whole_parent_credit"] ==
         c69o["D02_gate_credit"] == 0 and c69o["runtime_or_canonical_written"] is False and
         c69o["publication_O_EXCL_no_replace"] is True,
         "C69c-outer-publication")
    for key in ("C69_RESULT", "C69_DECISIONS", "C69_BLOCKERS", "C69_VERIFY"):
        manifest_member(m69, FILES[key], PINS[key], ("deliverables/", "deliverables__", ""))
    return c65, c68, c69


def validate_result_shape(value: Mapping[str, Any]) -> None:
    partition = value["child_partition"]
    need(partition == {
        "C69C_BLOCKER_SOURCE_CHILDREN": 134_155,
        "C69C_DECISION_SOURCE_CHILDREN": 33_100,
        "TOTAL_C65_COLLISION2_HANDOFF_CHILDREN": 167_255,
    }, "result-child-partition")
    need(value["blocker_child_category_census"] == CATEGORY_CHILD_CENSUS and
         sum(value["blocker_child_category_census"].values()) == 134_155,
         "result-child-category-census")
    need(value["source_category_census"] == CATEGORY_SOURCE_CENSUS,
         "result-source-category-census")
    need(value["source_partition"] == {
        "C69C_BLOCKERS": 18_523, "C69C_DECISIONS": 2_356, "TOTAL": 20_879,
    }, "result-source-partition")
    need(value["allowed_exit_classes"] == list(ALLOWED_EXIT_CLASSES),
         "result-exit-classes")
    need(value["required_deciders"] == sorted(DECIDER_FOR_CATEGORY.values()),
         "result-deciders")
    need(value["global_contract"] == {
        "additional_dyadic_depth_is_not_a_structural_decider": True,
        "every_child_requires_exact_full_box_or_exact_glued_stratum_proof": True,
        "only_a_later_no_producer_global_consumer_may_set_unresolved_zero": True,
        "partial_local_decisions_are_not_formal_credit": True,
    }, "result-global-contract")
    need(value["strict_boundary"] == {
        "candidate_is_authority": False,
        "decider_execution_performed": False,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
        "global_consumption_ready": False,
        "runtime_canonical_pointer_or_seal_writes": False,
        "CM2": "NO-GO_FOR_CLAIM",
    }, "result-strict-boundary")


def producer_shape_self_test(base: dict[str, Any]) -> dict[str, Any]:
    attacks: dict[str, bool] = {}

    def attacked(name: str, mutation: Any) -> None:
        candidate = copy.deepcopy(base)
        mutation(candidate)
        try:
            validate_result_shape(candidate)
        except (Reject, KeyError, TypeError, ValueError):
            attacks[name] = True
        else:
            attacks[name] = False

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
    need(len(attacks) == 20 and all(attacks.values()), "producer-shape-selftest")
    return {
        "status": "PASS_20_OF_20_COHERENT_PARTITION_AND_CREDIT_ATTACKS_FAIL_CLOSED",
        "attack_count": 20,
        "attacks": dict(sorted(attacks.items())),
    }


def expected_obligation(child: Mapping[str, Any], task: Mapping[str, Any],
                        blocker: Mapping[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": SCHEMA + ".obligation-row",
        "C65_aggregate_child_row_sha256": child["row_sha256"],
        "C65_source_shard_row_sha256": child["source_C65_shard_row_sha256"],
        "C61_aggregate_leaf_row_sha256": child["source_C61_aggregate_leaf_row_sha256"],
        "C68_structural_task_row_sha256": task["row_sha256"],
        "C69c_blocker_row_sha256": blocker["row_sha256"],
        "pair_index": child["pair_index"],
        "source_path": child["source_path"],
        "child_path": child["path"],
        "parent_volume_fraction": child["parent_volume_fraction"],
        "exact_representative_box": copy.deepcopy(child["exact_representative_box"]),
        "exact_reflected_box": copy.deepcopy(child["exact_reflected_box"]),
        "structural_category": task["structural_graph_kind"],
        "required_decider": DECIDER_FOR_CATEGORY[task["structural_graph_kind"]],
        "source_route_classification": task["residual_classification"],
        "source_route_witness": task["route_witness"],
        "child_route_classification": child["route_classification"],
        "child_route_witness": child["route_witness"],
        "source_grazing": task["source_grazing"],
        "blocker_codes": copy.deepcopy(blocker["blocker_codes"]),
        "allowed_exit_classes": list(ALLOWED_EXIT_CLASSES),
        "current_disposition": "FAIL_CLOSED_STRUCTURAL_OBLIGATION",
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    body["row_sha256"] = digest(body)
    return body


def validate_candidate_row(value: Mapping[str, Any], expected: Mapping[str, Any],
                           label: str) -> None:
    need(set(value) == OBLIGATION_KEYS, label + ":closed-schema")
    close_row(value, label)
    need(value["formal_credit"] == value["whole_parent_credit"] ==
         value["D02_gate_credit"] == 0, label + ":zero-credit")
    need(value["current_disposition"] == "FAIL_CLOSED_STRUCTURAL_OBLIGATION",
         label + ":fail-closed-disposition")
    need(value == expected, label + ":exact-independent-rebuild")


def build_expected_result(c65: Mapping[str, Any], c68: Mapping[str, Any],
                          c69: Mapping[str, Any], source_categories: Counter[str],
                          decision_children: int, blocker_children: Counter[str],
                          collision2_children: int, row_count: int,
                          row_sequence: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": SCHEMA + ".result",
        "status": "PASS_EXACT_C65_V3_CHILD_OBLIGATION_PARTITION__33100_C71_ELIGIBLE__134155_FIVE_STRUCTURAL_DECIDERS__ZERO_CREDIT",
        "producer_file_sha256": C72_PRODUCER_FILE_SHA256,
        "input_file_sha256": dict(PINS),
        "input_object_sha256": dict(OBJECT_PINS),
        "upstream_bundle_status": {
            "C65": c65["status"], "C68": c68["status"], "C69c": c69["status"],
        },
        "source_partition": {"C69C_DECISIONS": 2_356, "C69C_BLOCKERS": 18_523,
                             "TOTAL": 20_879},
        "source_category_census": dict(source_categories),
        "child_partition": {
            "C69C_DECISION_SOURCE_CHILDREN": decision_children,
            "C69C_BLOCKER_SOURCE_CHILDREN": row_count,
            "TOTAL_C65_COLLISION2_HANDOFF_CHILDREN": collision2_children,
        },
        "blocker_child_category_census": dict(blocker_children),
        "required_deciders": sorted(DECIDER_FOR_CATEGORY.values()),
        "allowed_exit_classes": list(ALLOWED_EXIT_CLASSES),
        "ledger": {
            "filename": LEDGER_NAME,
            "order": "C65_AGGREGATE_LEAF_ORDER_FILTERED_TO_C69C_BLOCKER_SOURCES_AND_COLLISION2",
            "row_count": row_count,
            "row_hash_line_sequence_sha256": row_sequence,
            "sha256": CANDIDATE_PINS["ledger"],
            "size": CANDIDATE_LEDGER_SIZE,
        },
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
    result["producer_self_test"] = producer_shape_self_test(result)
    result["object_sha256"] = digest(result)
    return result


def expected_report(result: Mapping[str, Any]) -> bytes:
    text = (
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
        f"Ledger SHA256: `{CANDIDATE_PINS['ledger']}`; rows: `134155`.\n"
        f"Result object: `{result['object_sha256']}`.\n"
    )
    return text.encode("utf-8")


def mutate_value(value: Any) -> Any:
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "__ATTACK"
    if type(value) is list:
        return copy.deepcopy(value) + ["__ATTACK"]
    if type(value) is dict:
        altered = copy.deepcopy(value)
        altered["__attack__"] = True
        return altered
    return "__ATTACK"


def independent_coherent_attacks(sample_row: dict[str, Any],
                                 expected_result: dict[str, Any]) -> dict[str, Any]:
    attacks: dict[str, bool] = {}

    def rejected(name: str, callback: Any) -> None:
        try:
            callback()
        except (Reject, KeyError, TypeError, ValueError, UnicodeError, json.JSONDecodeError):
            attacks[name] = True
        else:
            attacks[name] = False

    for field in sorted(set(sample_row) - {"row_sha256"}):
        altered = copy.deepcopy(sample_row)
        altered[field] = mutate_value(altered[field])
        altered["row_sha256"] = digest({key: value for key, value in altered.items()
                                        if key != "row_sha256"})
        rejected("coherent_row_field__" + field,
                 lambda value=altered: validate_candidate_row(value, sample_row, "attack-row"))
    altered_hash = copy.deepcopy(sample_row)
    altered_hash["row_sha256"] = "0" * 64
    rejected("row_closure", lambda: validate_candidate_row(altered_hash, sample_row, "attack-row"))

    def validate_attacked_result(value: dict[str, Any]) -> None:
        close_object_self(value, "attack-result")
        validate_result_shape(value)
        need(value == expected_result, "attack-result:exact-rebuild")
        need(value["object_sha256"] == CANDIDATE_OBJECT_SHA256,
             "attack-result:published-object-pin")

    for field in sorted(set(expected_result) - {"object_sha256"}):
        altered = copy.deepcopy(expected_result)
        altered[field] = mutate_value(altered[field])
        altered["object_sha256"] = digest({key: value for key, value in altered.items()
                                           if key != "object_sha256"})
        rejected("coherent_result_field__" + field,
                 lambda value=altered: validate_attacked_result(value))

    targeted: list[tuple[str, tuple[str, ...], Any]] = [
        ("partition_decision", ("child_partition", "C69C_DECISION_SOURCE_CHILDREN"), 33_101),
        ("partition_blocker", ("child_partition", "C69C_BLOCKER_SOURCE_CHILDREN"), 134_154),
        ("partition_total", ("child_partition", "TOTAL_C65_COLLISION2_HANDOFF_CHILDREN"), 167_254),
        ("ledger_rows", ("ledger", "row_count"), 134_154),
        ("ledger_sequence", ("ledger", "row_hash_line_sequence_sha256"), "0" * 64),
        ("ledger_pin", ("ledger", "sha256"), "0" * 64),
        ("ledger_size", ("ledger", "size"), CANDIDATE_LEDGER_SIZE + 1),
        ("ledger_order", ("ledger", "order"), "ATTACK_ORDER"),
        ("boundary_authority", ("strict_boundary", "candidate_is_authority"), True),
        ("boundary_decider", ("strict_boundary", "decider_execution_performed"), True),
        ("boundary_ready", ("strict_boundary", "global_consumption_ready"), True),
        ("boundary_write", ("strict_boundary", "runtime_canonical_pointer_or_seal_writes"), True),
        ("boundary_formal", ("strict_boundary", "formal_credit"), 1),
        ("boundary_parent", ("strict_boundary", "whole_parent_credit"), 1),
        ("boundary_D02", ("strict_boundary", "D02_gate_credit"), 1),
        ("boundary_CM2", ("strict_boundary", "CM2"), "GO"),
        ("contract_depth", ("global_contract", "additional_dyadic_depth_is_not_a_structural_decider"), False),
        ("contract_exact", ("global_contract", "every_child_requires_exact_full_box_or_exact_glued_stratum_proof"), False),
        ("contract_partial", ("global_contract", "partial_local_decisions_are_not_formal_credit"), False),
        ("contract_consumer", ("global_contract", "only_a_later_no_producer_global_consumer_may_set_unresolved_zero"), False),
    ]
    for name, path, replacement in targeted:
        altered = copy.deepcopy(expected_result)
        cursor: dict[str, Any] = altered
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        altered["object_sha256"] = digest({key: value for key, value in altered.items()
                                           if key != "object_sha256"})
        rejected("coherent_nested__" + name,
                 lambda value=altered: validate_attacked_result(value))

    rejected("framing_duplicate_key", lambda: parse_line(b'{"a":1,"a":2}', "attack"))
    rejected("framing_noncanonical_space", lambda: parse_line(b'{"a": 1}', "attack"))
    rejected("framing_BOM", lambda: parse_line(b'\xef\xbb\xbf{"a":1}', "attack"))
    rejected("framing_NUL", lambda: parse_line(b'{"a":"\x00"}', "attack"))
    rejected("framing_NaN", lambda: parse_line(b'{"a":NaN}', "attack"))
    rejected("framing_empty", lambda: parse_line(b"", "attack"))
    need(len(attacks) >= 60 and all(attacks.values()), "independent-coherent-attacks")
    return {
        "status": "PASS_%d_OF_%d_COHERENT_ROW_RESULT_CREDIT_AND_FRAMING_ATTACKS_FAIL_CLOSED" %
                  (len(attacks), len(attacks)),
        "attack_count": len(attacks),
        "attacks": dict(sorted(attacks.items())),
    }


def exclusive(path: Path, raw: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0)
    descriptor = os.open(path, flags, 0o644)
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "verification-write:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def verify(primary: Path, peer: Path, publish: bool) -> tuple[dict[str, Any], bytes]:
    require_directory(primary, "primary-candidate")
    require_directory(peer, "peer-candidate")
    need(primary != peer, "distinct-candidate-directories")
    paths, pins = input_paths(primary, peer)
    before = snapshot_inputs(paths)

    for member, name in (("ledger", LEDGER_NAME), ("result", RESULT_NAME),
                         ("report", REPORT_NAME)):
        compare_secure_files(primary / name, peer / name, CANDIDATE_PINS[member])

    candidate_result = secure_json(primary / RESULT_NAME, CANDIDATE_PINS["result"],
                                   CANDIDATE_OBJECT_SHA256)
    candidate_report = secure_bytes(primary / REPORT_NAME, CANDIDATE_PINS["report"], 1 << 20)
    need(candidate_result["producer_file_sha256"] == C72_PRODUCER_FILE_SHA256,
         "declaration-only-producer-byte-binding")
    need(candidate_result["input_file_sha256"] == PINS and
         candidate_result["input_object_sha256"] == OBJECT_PINS,
         "candidate-upstream-pin-maps")
    validate_result_shape(candidate_result)
    c65, c68, c69 = validate_bundles()

    c68_tasks: dict[str, dict[str, Any]] = {}
    source_categories: Counter[str] = Counter()
    task_rows, task_sequence = LEDGER_SPECS["C68_TASKS"]
    for row in iter_secure_jsonl(OUT / FILES["C68_TASKS"], PINS["C68_TASKS"],
                                 task_rows, task_sequence, 64 << 20):
        need(set(row) == C68_TASK_KEYS, "C68-task-closed-schema")
        source = row["C61_aggregate_leaf_row_sha256"]
        need(source not in c68_tasks, "duplicate-C68-source")
        need(row["formal_credit"] == row["whole_parent_credit"] ==
             row["D02_gate_credit"] == 0 and row["structural_decider_available"] is False,
             "C68-task-zero-credit")
        c68_tasks[source] = row
        source_categories[row["structural_graph_kind"]] += 1
    need(len(c68_tasks) == 20_879 and dict(source_categories) == CATEGORY_SOURCE_CENSUS,
         "C68-exact-source-domain")

    source_partition: dict[str, dict[str, Any]] = {}
    decision_rows, decision_sequence = LEDGER_SPECS["C69_DECISIONS"]
    for row in iter_secure_jsonl(OUT / FILES["C69_DECISIONS"], PINS["C69_DECISIONS"],
                                 decision_rows, decision_sequence, 32 << 20):
        source = row["C61_aggregate_leaf_row_sha256"]
        need(source in c68_tasks and source not in source_partition,
             "C69-decision-source-partition")
        task = c68_tasks[source]
        need(task["structural_graph_kind"] == "REGULAR_FULL_FACE_GRAPH_CELL" and
             row["C68_structural_task_row_sha256"] == task["row_sha256"] and
             row["pair_index"] == task["pair_index"] and row["path"] == task["path"] and
             row["parent_volume_fraction"] == task["parent_volume_fraction"] and
             row["decision"] == "STRICT_UNIQUE_H1_GRAPH_AND_TWO_OFF_GRAPH_SLABS_AVAILABLE" and
             row["capability_consumption_ready"] is True and
             row["formal_credit"] == row["whole_parent_credit"] ==
             row["D02_gate_credit"] == row["collision2_handoff_credit"] ==
             row["terminal_disposition_credit"] == 0,
             "C69-decision-lineage-zero-credit")
        source_partition[source] = {"kind": "DECISION", "task": task, "row": row}

    blocker_rows, blocker_sequence = LEDGER_SPECS["C69_BLOCKERS"]
    for row in iter_secure_jsonl(OUT / FILES["C69_BLOCKERS"], PINS["C69_BLOCKERS"],
                                 blocker_rows, blocker_sequence, 32 << 20):
        need(set(row) == C69_BLOCKER_KEYS, "C69-blocker-closed-schema")
        source = row["C61_aggregate_leaf_row_sha256"]
        need(source in c68_tasks and source not in source_partition,
             "C69-blocker-source-partition")
        task = c68_tasks[source]
        need(row["C68_structural_task_row_sha256"] == task["row_sha256"] and
             row["pair_index"] == task["pair_index"] and row["path"] == task["path"] and
             row["parent_volume_fraction"] == task["parent_volume_fraction"] and
             row["exact_representative_box_object_sha256"] ==
             task["exact_representative_box_object_sha256"] and
             row["route_classification"] == task["residual_classification"] and
             row["route_witness"] == task["route_witness"] and
             row["structural_graph_kind"] == task["structural_graph_kind"] and
             row["additional_dyadic_source_depth_recommended"] is False and
             row["capability_decision_available"] is False and
             row["formal_credit"] == row["whole_parent_credit"] == row["D02_gate_credit"] == 0 and
             type(row["blocker_codes"]) is list and len(row["blocker_codes"]) > 0,
             "C69-blocker-lineage-zero-credit")
        source_partition[source] = {"kind": "BLOCKER", "task": task, "row": row}
    need(len(source_partition) == len(c68_tasks) == 20_879,
         "complete-C69c-source-partition")

    summaries: dict[str, dict[str, Any]] = {}
    source_rows, source_sequence = LEDGER_SPECS["C65_SOURCES"]
    for row in iter_secure_jsonl(OUT / FILES["C65_SOURCES"], PINS["C65_SOURCES"],
                                 source_rows, source_sequence, 64 << 20):
        source = row["source_C61_aggregate_leaf_row_sha256"]
        need(source in source_partition and source not in summaries,
             "C65-source-summary-join")
        need(row["formal_credit"] == row["whole_parent_credit"] == row["D02_gate_credit"] == 0 and
             row["path_prefix_free"] is True and
             type(row["source_Kraft_conservation"]) is str and
             len(row["source_Kraft_conservation"]) > 0,
             "C65-source-summary-boundary")
        summaries[source] = row
    need(len(summaries) == 20_879, "C65-source-summary-domain")

    candidate_rows = iter_secure_jsonl(
        primary / LEDGER_NAME, CANDIDATE_PINS["ledger"], 134_155,
        CANDIDATE_LEDGER_SEQUENCE, 384 << 20,
    )
    observed_source: defaultdict[str, Counter[str]] = defaultdict(Counter)
    dispositions: Counter[str] = Counter()
    blocker_children: Counter[str] = Counter()
    decision_children = 0
    rebuilt_count = 0
    rebuilt_sequence = hashlib.sha256()
    sample_row: dict[str, Any] | None = None
    leaf_rows, leaf_sequence = LEDGER_SPECS["C65_LEAVES"]
    for child in iter_secure_jsonl(OUT / FILES["C65_LEAVES"], PINS["C65_LEAVES"],
                                   leaf_rows, leaf_sequence, 1_100 << 20):
        source = child["source_C61_aggregate_leaf_row_sha256"]
        need(source in source_partition, "C65-child-source-join")
        entry = source_partition[source]
        task = entry["task"]
        need(child["pair_index"] == task["pair_index"] and
             child["source_path"] == task["path"] and
             child["path"].startswith(task["path"]) and
             child["formal_credit"] == child["whole_parent_credit"] ==
             child["D02_gate_credit"] == 0, "C65-child-lineage-zero-credit")
        disposition = child["disposition"]
        need(disposition in {"STRICT_TERMINAL", "COLLISION2_HANDOFF"},
             "C65-child-disposition")
        dispositions[disposition] += 1
        observed_source[source]["ALL"] += 1
        observed_source[source][disposition] += 1
        if disposition != "COLLISION2_HANDOFF":
            continue
        if entry["kind"] == "DECISION":
            decision_children += 1
            continue
        category = task["structural_graph_kind"]
        need(category in DECIDER_FOR_CATEGORY, "blocker-child-known-category")
        expected = expected_obligation(child, task, entry["row"])
        try:
            observed = next(candidate_rows)
        except StopIteration as error:
            raise Reject("candidate-ledger-premature-EOF") from error
        validate_candidate_row(observed, expected, "candidate-row:" + str(rebuilt_count + 1))
        rebuilt_count += 1
        rebuilt_sequence.update(expected["row_sha256"].encode("ascii") + b"\n")
        blocker_children[category] += 1
        if sample_row is None:
            sample_row = copy.deepcopy(expected)
    try:
        next(candidate_rows)
    except StopIteration:
        pass
    else:
        raise Reject("candidate-ledger-trailing-row")

    need(dispositions == Counter({"STRICT_TERMINAL": 191_664,
                                  "COLLISION2_HANDOFF": 167_255}),
         "C65-independent-child-census")
    need(decision_children == 33_100 and rebuilt_count == 134_155 and
         dict(blocker_children) == CATEGORY_CHILD_CENSUS and
         rebuilt_sequence.hexdigest() == CANDIDATE_LEDGER_SEQUENCE,
         "exact-167255-equals-33100-plus-134155-partition")
    need(sample_row is not None, "nonempty-candidate-ledger")
    for source, summary in summaries.items():
        observed = observed_source[source]
        need(observed["ALL"] == summary["output_leaf_count"] and
             observed["STRICT_TERMINAL"] == summary["strict_terminal_leaf_count"] and
             observed["COLLISION2_HANDOFF"] == summary["collision2_handoff_leaf_count"],
             "C65-per-source-summary:" + source)

    expected_result = build_expected_result(
        c65, c68, c69, source_categories, decision_children, blocker_children,
        dispositions["COLLISION2_HANDOFF"], rebuilt_count, rebuilt_sequence.hexdigest(),
    )
    need(expected_result["object_sha256"] == CANDIDATE_OBJECT_SHA256,
         "independently-rebuilt-result-object-pin")
    close_object_self(candidate_result, "candidate-result")
    need(candidate_result == expected_result, "exact-independent-result-rebuild")
    need(candidate_report == expected_report(expected_result), "exact-report-rebuild")
    attacks = independent_coherent_attacks(sample_row, expected_result)

    recapture_inputs(paths, pins, before)
    _, verifier_sha = secure_unpinned_bytes(SELF)
    verification: dict[str, Any] = {
        "schema": VERIFY_SCHEMA,
        "status": "PASS_COLD_NO_C72_PRODUCER_READ_IMPORT_EXECUTION_OR_DECODE__DUAL_ISOLATED_CANDIDATES_BYTE_IDENTICAL__EXACT_REBUILD_134155_ROWS__167255_EQUALS_33100_PLUS_134155__FIVE_CATEGORY_CENSUS__ZERO_CREDIT",
        "verifier_file_sha256": verifier_sha,
        "producer_file_sha256": C72_PRODUCER_FILE_SHA256,
        "producer_source_policy": {
            "producer_path_in_runtime_input_set": False,
            "producer_source_opened": False,
            "producer_source_read_or_decoded": False,
            "producer_imported": False,
            "producer_executed": False,
            "producer_hash_consumed_as_declaration_only_binding": True,
        },
        "dual_isolated_candidate_byte_identity": {
            "ledger": True, "result": True, "report": True,
        },
        "candidate_file_sha256": dict(CANDIDATE_PINS),
        "candidate_object_sha256": CANDIDATE_OBJECT_SHA256,
        "upstream_file_sha256": dict(PINS),
        "upstream_object_sha256": dict(OBJECT_PINS),
        "upstream_bundle_closure": {
            "C65_v9_formal_self_test": "134/134",
            "C65_one_global_manifest_member_count": 446,
            "C65_outer_receipt_published_last": True,
            "C68_independent_zero_credit_closure": True,
            "C69c_independent_no_producer_zero_credit_closure": True,
        },
        "recomputed_source_partition": {
            "C69C_DECISIONS": 2_356, "C69C_BLOCKERS": 18_523, "TOTAL": 20_879,
        },
        "recomputed_source_category_census": dict(source_categories),
        "recomputed_child_partition": {
            "C69C_DECISION_SOURCE_CHILDREN": decision_children,
            "C69C_BLOCKER_SOURCE_CHILDREN": rebuilt_count,
            "TOTAL_C65_COLLISION2_HANDOFF_CHILDREN": dispositions["COLLISION2_HANDOFF"],
        },
        "recomputed_blocker_child_category_census": dict(blocker_children),
        "recomputed_ledger_row_hash_line_sequence_sha256": rebuilt_sequence.hexdigest(),
        "all_134155_rows_exactly_rebuilt": True,
        "candidate_ledger_gzip_single_member_canonical_closed": True,
        "candidate_result_canonical_closed_and_exactly_rebuilt": True,
        "candidate_report_exactly_rebuilt": True,
        "all_inputs_regular_single_link_nofollow_TOCTOU_closed": True,
        "all_input_byte_pins_recaptured_after_full_scan": True,
        "coherent_attacks": attacks,
        "strict_boundary": {
            "candidate_is_authority": False,
            "decider_execution_performed": False,
            "global_consumption_ready": False,
            "runtime_canonical_pointer_or_seal_writes": False,
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    verification["object_sha256"] = digest(verification)
    raw_verification = canonical(verification) + b"\n"
    if publish:
        output = primary / VERIFY_NAME
        exclusive(output, raw_verification)
        replayed = secure_bytes(output, hashlib.sha256(raw_verification).hexdigest(), 4 << 20)
        need(replayed == raw_verification, "verification-terminal-byte-replay")
        replayed_object = parse_line(replayed[:-1], VERIFY_NAME)
        close_object(replayed_object, verification["object_sha256"], VERIFY_NAME)
    return verification, raw_verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", type=Path, required=True)
    parser.add_argument("--peer-candidate-dir", type=Path, required=True)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    primary = arguments.candidate_dir.absolute()
    peer = arguments.peer_candidate_dir.absolute()
    verification, raw = verify(primary, peer, not arguments.no_write)
    print(json.dumps({
        "status": verification["status"],
        "object_sha256": verification["object_sha256"],
        "file_sha256": hashlib.sha256(raw).hexdigest(),
        "attacks": verification["coherent_attacks"]["attack_count"],
        "published": not arguments.no_write,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, ValueError, KeyError, TypeError, IndexError,
            UnicodeError, zlib.error) as error:
        print("REJECT_C72_INDEPENDENT:%s:%s" % (type(error).__name__, error), file=sys.stderr)
        raise SystemExit(2)
