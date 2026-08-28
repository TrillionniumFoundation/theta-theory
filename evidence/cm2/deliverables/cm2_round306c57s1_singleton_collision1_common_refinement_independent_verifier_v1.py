#!/usr/bin/env python3
"""Second cold verifier for the frozen C57s1 collision-one refinement.

The C57s1 producer is never imported or executed.  This verifier consumes its
source only as pinned inert bytes, then independently reconstructs the exact
C35/C38/C39/C40/C41 row chains, the 781-leaf prefix/Kraft partitions, all 319
collision-two handoffs, and the globally atomized face/corner owner ledger.
"""

from __future__ import annotations

import argparse
import ast
import copy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Callable, Iterable
import zlib


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
OUT = SELF.parent
BASE = "cm2_round306c57s1_singleton_collision1_common_refinement"
SCHEMA = "cm2.round306c57s1.singleton-collision1-common-refinement-independent-verifier.v1"
CORE_SCHEMA = "cm2.round306c57s1.singleton-collision1-common-refinement.v1"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
PAIRS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)

PRODUCER = OUT / (BASE + "_v1.py")
RESULT = OUT / (BASE + "_result_v1.json")
LEAVES = OUT / (BASE + "_leaf_ledger_v1.jsonl.gz")
OWNERS = OUT / (BASE + "_face_corner_owner_ledger_v1.jsonl.gz")
PARENTS = OUT / (BASE + "_parent_ledger_v1.jsonl.gz")

C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C38 = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C39 = ROOT / ".cm2-runtime/candidates/c39-h1-c1-graph-router-20260810T185014Z-e004fadaadcd5559"
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C41 = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"

C57A_AUDIT = OUT / "cm2_round306c57a_singleton_collision1_candidate_independent_audit_v1.json"
C57A_REPORT = OUT / "cm2_round306c57a_singleton_collision1_candidate_independent_report_v1.md"
C57A_SELFTEST = OUT / "cm2_round306c57a_singleton_collision1_candidate_independent_self_test_v1.json"
C57A_VERIFIER = OUT / "cm2_round306c57a_singleton_collision1_candidate_independent_verifier_v1.py"
C57A_MANIFEST = OUT / "cm2_round306c57a_singleton_collision1_candidate_independent_manifest_v1.sha256"

PIN = {
    "producer_file": "52184b7211176dcd8b3321d77ac33143457e0be912769d0486d822a57eef0b13",
    "result_file": "9881c22ac4a8630b90b8eb16d81c1670bb6f544e5f4666197d0e6047771d8c4c",
    "result_object": "8cda7681bcbe93c065f1f336842e9fffa6bd3ea67268e96d95fcb3d1f8cbbb58",
    "leaf_file": "918899a914ad4fbb05c1095cac9f42f6c46d02f0acdad366538a395021aeaee6",
    "owner_file": "72d4dd688378166bfd8dbf9ded56ef091014803f80777ea21847a831b4c3f884",
    "parent_file": "8817069967798042bd87315f57e7c3cea279c6564c0e50a5ac927ca4f765e510",
    "C35_object": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C38_file": "094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    "C38_object": "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434",
    "C39_file": "f9bfacbdaaf5263ba16397e70fe56b4f31149087c2434b7c163ff284b40cfd7e",
    "C39_object": "821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02",
    "C40_file": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C40_object": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "C41_file": "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    "C41_object": "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    "C57a_audit_file": "9fdbb28605e81de75949486416851f4d2bb233c4953650fcbadd024c12dccbdc",
    "C57a_audit_object": "f7984162bdb64c7cbb828e9d3733103637898007c91c89292b64717145b818c0",
    "C57a_report_file": "08d7e495393ab07b3aa363d6aa53d6ba0fffc905d5ba7b93c1b811e9d883aa28",
    "C57a_selftest_file": "171d67782e0de1822bf7e069a614c2783ccad08d82a0b353d13e4d96b45111fb",
    "C57a_verifier_file": "afa648cc29a1ba627b2e41f7cd45f2d62d1135df212d6483c2c5f7da6e203d1e",
    "C57a_manifest_file": "669377fd362a5c66dd36c75d27685c2f76a0e5661c400dd99494455940d15db5",
}


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def bytes_sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def close(value: dict[str, Any], key: str = "object_sha256") -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need(key not in answer, "object already closed")
    answer[key] = digest(answer)
    return answer


def duplicate_guard(items: list[tuple[str, Any]]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for key, value in items:
        if key in answer:
            raise Rejected("duplicate JSON key:" + key)
        answer[key] = value
    return answer


def parse(raw: bytes, label: str, canonical_required: bool = False) -> Any:
    need(bool(raw) and not raw.startswith(b"\xef\xbb\xbf"), label + " strict bytes")
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=duplicate_guard,
            parse_constant=lambda token: (_ for _ in ()).throw(Rejected(label + ":" + token)),
        )
    except Rejected:
        raise
    except Exception as exc:
        raise Rejected(label + " JSON:" + str(exc)) from exc
    if canonical_required:
        need(raw == canonical(value) + b"\n", label + " canonical bytes")
    return value


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns)


def capture(paths: Iterable[Path], maximum: int = 256 << 20,
            hook: Callable[[], None] | None = None) -> dict[Path, bytes]:
    ordered = tuple(paths)
    need(len(set(ordered)) == len(ordered), "duplicate capture path")
    descriptors: dict[Path, int] = {}
    before: dict[Path, os.stat_result] = {}
    try:
        for path in ordered:
            descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                                 getattr(os, "O_NOFOLLOW", 0))
            state = os.fstat(descriptor)
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
                 0 < state.st_size <= maximum, "single-link regular frozen input:" + str(path))
            descriptors[path] = descriptor
            before[path] = state
        raw: dict[Path, bytes] = {}
        for path in ordered:
            pieces: list[bytes] = []
            while block := os.read(descriptors[path], 4 << 20):
                pieces.append(block)
            raw[path] = b"".join(pieces)
        if hook is not None:
            hook()
        for path in ordered:
            need(fingerprint(before[path]) == fingerprint(os.fstat(descriptors[path])) ==
                 fingerprint(os.stat(path, follow_symlinks=False)), "TOCTOU:" + str(path))
        return raw
    finally:
        for descriptor in descriptors.values():
            os.close(descriptor)


def closed_result(raw: bytes, file_pin: str | None, object_pin: str, label: str) -> dict[str, Any]:
    if file_pin is not None:
        need(bytes_sha(raw) == file_pin, label + " file pin")
    value = parse(raw, label)
    need(type(value) is dict and value.get("object_sha256") == object_pin, label + " object claim")
    body = copy.deepcopy(value)
    body.pop("object_sha256")
    need(digest(body) == object_pin, label + " object reconstruction")
    return value


def ledger_rows(raw: bytes, descriptor: dict[str, Any], file_pin: str, label: str) -> list[dict[str, Any]]:
    need(bytes_sha(raw) == descriptor["sha256"] == file_pin, label + " file pin")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        expanded = decoder.decompress(raw, 768 << 20) + decoder.flush()
    except zlib.error as exc:
        raise Rejected(label + " gzip:" + str(exc)) from exc
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
         label + " exactly one gzip member")
    lines = expanded.splitlines(keepends=True)
    need(len(lines) == descriptor["row_count"], label + " row count")
    sequence = hashlib.sha256()
    answer: list[dict[str, Any]] = []
    for line in lines:
        row = parse(line, label + " row", canonical_required=True)
        need(type(row) is dict and type(row.get("row_sha256")) is str and
             HEX64.fullmatch(row["row_sha256"]) is not None, label + " row claim")
        body = copy.deepcopy(row)
        claim = body.pop("row_sha256")
        need(digest(body) == claim, label + " row closure")
        sequence.update((claim + "\n").encode("ascii"))
        answer.append(row)
    need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         label + " row sequence")
    return answer


def q(value: Any) -> Fraction:
    return Fraction(str(value))


def box_key(box: dict[str, Any]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return q(box["t"][0]), q(box["t"][1]), q(box["p"][0]), q(box["p"][1])


def prefix_free(paths: list[str]) -> bool:
    ordered = sorted(paths, key=lambda value: (len(value), value))
    return all(not later.startswith(first) for index, first in enumerate(ordered)
               for later in ordered[index + 1:])


def producer_independence(raw: bytes) -> dict[str, Any]:
    need(bytes_sha(raw) == PIN["producer_file"], "producer source pin")
    tree = ast.parse(raw.decode("utf-8", "strict"), filename=PRODUCER.name)
    imports: list[str] = []
    dynamic: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {
            "exec", "eval", "compile", "__import__",
        }:
            dynamic.append(node.func.id)
    need(not dynamic and not any("cm2_round306c57s1" in item for item in imports),
         "producer dynamic/import path")
    need(not any("cm2_round306c57s1_singleton_collision1_common_refinement_v1" in key
                 for key in sys.modules), "producer absent from modules")
    return {
        "producer_imported": False,
        "producer_executed": False,
        "producer_source_consumed_as_pinned_inert_bytes_and_AST_only": True,
    }


def frozen_manifest_check(raws: dict[Path, bytes]) -> dict[str, Any]:
    expected = {
        C57A_AUDIT.name: PIN["C57a_audit_file"],
        C57A_REPORT.name: PIN["C57a_report_file"],
        C57A_SELFTEST.name: PIN["C57a_selftest_file"],
        C57A_VERIFIER.name: PIN["C57a_verifier_file"],
    }
    need(bytes_sha(raws[C57A_MANIFEST]) == PIN["C57a_manifest_file"], "C57a manifest pin")
    parsed: dict[str, str] = {}
    for line in raws[C57A_MANIFEST].decode("ascii", "strict").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and HEX64.fullmatch(parts[0]) is not None, "C57a manifest line")
        parsed[parts[1]] = parts[0]
    need(parsed == expected, "C57a manifest exact membership")
    for path in (C57A_AUDIT, C57A_REPORT, C57A_SELFTEST, C57A_VERIFIER):
        need(bytes_sha(raws[path]) == expected[path.name], "C57a member pin:" + path.name)
    audit = closed_result(raws[C57A_AUDIT], PIN["C57a_audit_file"],
                          PIN["C57a_audit_object"], "C57a audit")
    need(audit["status"].startswith("PASS_INDEPENDENT_C57S1_") and
         audit["candidate_is_authority"] is False and audit["formal_credit"] == 0 and
         audit["D02_gate_credit"] == 0, "C57a audit boundary")
    return {"manifest_sha256": PIN["C57a_manifest_file"],
            "audit_object_sha256": PIN["C57a_audit_object"], "manifest_entries": 4}


def verify() -> dict[str, Any]:
    first_paths = (
        PRODUCER, RESULT, LEAVES, OWNERS, PARENTS,
        C35 / "result.json", C38 / "result.json", C39 / "result.json",
        C40 / "result.json", C41 / "result.json",
        C57A_AUDIT, C57A_REPORT, C57A_SELFTEST, C57A_VERIFIER, C57A_MANIFEST,
    )
    raw = capture(first_paths)
    independence = producer_independence(raw[PRODUCER])
    c57a = frozen_manifest_check(raw)
    result = closed_result(raw[RESULT], PIN["result_file"], PIN["result_object"], "C57s1")
    c35 = closed_result(raw[C35 / "result.json"], None, PIN["C35_object"], "C35")
    c38 = closed_result(raw[C38 / "result.json"], PIN["C38_file"], PIN["C38_object"], "C38")
    c39 = closed_result(raw[C39 / "result.json"], PIN["C39_file"], PIN["C39_object"], "C39")
    c40 = closed_result(raw[C40 / "result.json"], PIN["C40_file"], PIN["C40_object"], "C40")
    c41 = closed_result(raw[C41 / "result.json"], PIN["C41_file"], PIN["C41_object"], "C41")
    need(result["schema"] == CORE_SCHEMA and result["object_sha256"] == PIN["result_object"],
         "C57s1 schema/object")
    need(result["status"] ==
         "PASS_COLLISION1_COMMON_REFINEMENT__12_PAIRS_24_SINGLETONS__781_LEAVES__462_TERMINAL__319_EXACT_COLLISION2_HANDOFFS__ZERO_WHOLE_CLOSED",
         "C57s1 status")
    need(result["authority_objects"] == {
        "C35": PIN["C35_object"], "C38": PIN["C38_object"], "C39": PIN["C39_object"],
        "C40": PIN["C40_object"], "C41": PIN["C41_object"],
        "C56s": "c0e90419a49ca4054897b0985933478bea5d6893ae33048176c4c46194e1f6da",
    }, "C57s1 authority pins")

    leaves = ledger_rows(raw[LEAVES], result["ledgers"]["leaves"], PIN["leaf_file"], "C57 leaves")
    owners = ledger_rows(raw[OWNERS], result["ledgers"]["face_corner_owners"], PIN["owner_file"], "C57 owners")
    parents = ledger_rows(raw[PARENTS], result["ledgers"]["parents"], PIN["parent_file"], "C57 parents")
    need(len(leaves) == 781 and len(owners) == 3141 and len(parents) == 12,
         "C57 core row census")
    need(tuple(row["pair_index"] for row in parents) == PAIRS, "parent order")

    ledger_specs = (
        (C35, c35, ("path_occurrences",)),
        (C38, c38, ("collision1_2_child_pairs", "representative_parent_conservation")),
        (C39, c39, ("routed_child_pairs", "parent_conservation")),
        (C40, c40, ("routed_leaf_cells", "parent_conservation")),
        (C41, c41, ("routed_ambient_cells", "parent_conservation", "c1_h1_surface_outers",
                     "boundary_corner_outers", "split_face_adjacency")),
    )
    upstream_paths: list[Path] = []
    for directory, value, names in ledger_specs:
        upstream_paths.extend(directory / value["ledgers"][name]["filename"] for name in names)
    upstream_raw = capture(upstream_paths, maximum=768 << 20)

    def upstream(directory: Path, value: dict[str, Any], name: str) -> list[dict[str, Any]]:
        descriptor = value["ledgers"][name]
        path = directory / descriptor["filename"]
        return ledger_rows(upstream_raw[path], descriptor, descriptor["sha256"], name)

    histories = upstream(C35, c35, "path_occurrences")
    need(len(histories) == 1648 and histories[0]["collision_index"] == 1, "C35 history census")
    history = histories[0]
    c38_children = {row["row_sha256"]: row for row in upstream(C38, c38, "collision1_2_child_pairs")
                    if row["pair_index"] in PAIRS}
    c38_parents = {row["pair_index"]: row for row in upstream(C38, c38, "representative_parent_conservation")
                   if row["pair_index"] in PAIRS}
    c39_rows = {row["row_sha256"]: row for row in upstream(C39, c39, "routed_child_pairs")
                if row["pair_index"] in PAIRS}
    c39_by_c38 = {row["c38_child_row_sha256"]: row for row in c39_rows.values()}
    c39_parents = {row["pair_index"]: row for row in upstream(C39, c39, "parent_conservation")
                   if row["pair_index"] in PAIRS}
    c40_rows = {row["row_sha256"]: row for row in upstream(C40, c40, "routed_leaf_cells")
                if row["pair_index"] in PAIRS}
    c40_parents = {row["pair_index"]: row for row in upstream(C40, c40, "parent_conservation")
                   if row["pair_index"] in PAIRS}
    c41_rows = {row["row_sha256"]: row for row in upstream(C41, c41, "routed_ambient_cells")
                if row["pair_index"] in PAIRS}
    c41_parents = {row["pair_index"]: row for row in upstream(C41, c41, "parent_conservation")
                   if row["pair_index"] in PAIRS}
    c41_outers = {(row["pair_index"], row["descendant_path"]): row
                  for row in upstream(C41, c41, "c1_h1_surface_outers") if row["pair_index"] in PAIRS}
    c41_boundaries = {(row["pair_index"], row["descendant_path"]): row
                      for row in upstream(C41, c41, "boundary_corner_outers") if row["pair_index"] in PAIRS}
    split_count = sum(row["pair_index"] in PAIRS for row in upstream(C41, c41, "split_face_adjacency"))
    need((len(c38_children), len(c39_by_c38), len(c40_rows), len(c41_rows),
          len(c41_outers), len(c41_boundaries), split_count) == (164, 164, 299, 781, 319, 319, 482),
         "exact upstream indexed coverage")

    owner_by_hash = {row["row_sha256"]: row for row in owners}
    need(len(owner_by_hash) == 3141, "owner hash uniqueness")
    by_pair: dict[int, list[dict[str, Any]]] = {pair: [] for pair in PAIRS}
    ambient_id_by_leaf_hash: dict[str, str] = {}
    path_by_id: dict[str, str] = {}
    terminal = handoff_count = 0
    for leaf in leaves:
        pair, path = leaf["pair_index"], leaf["path"]
        need(pair in by_pair and type(path) is str and path and set(path) <= {"0", "1"}, "leaf pair/path")
        ambient = c41_rows[leaf["C41_ambient_row_sha256"]]
        c40_row = c40_rows[leaf["C40_leaf_row_sha256"]]
        c38_row = c38_children[leaf["C38_child_row_sha256"]]
        c39_row = c39_rows[leaf["C39_routed_row_sha256"]]
        need((ambient["pair_index"], ambient["path"]) == (pair, path), "C41 pair/path")
        need(ambient["c40_source_row_sha256"] == c40_row["row_sha256"], "C40-C41 link")
        need(c40_row["c38_source_row_sha256"] == c38_row["row_sha256"] and
             c40_row["c39_source_row_sha256"] == c39_row["row_sha256"] and
             c39_by_c38[c38_row["row_sha256"]]["row_sha256"] == c39_row["row_sha256"],
             "C38-C39-C40 chain")
        need(c38_row["representative_cell_id"] == leaf["representative_cell_id"] and
             c38_row["reflected_cell_id"] == leaf["reflected_cell_id"], "leaf cell chain")
        need(leaf["exact_representative_box"] == ambient["closed_representative_box"] and
             leaf["exact_reflected_box"] == ambient["closed_reflected_box"] and
             leaf["parent_volume_fraction"] == ambient["parent_volume_fraction"],
             "leaf exact geometry/volume")
        need(leaf["event_order_bound_to_C35_collision1"] is True and
             leaf["whole_parent_credit"] == leaf["D02_gate_credit"] == 0, "leaf event/credit lock")
        references = leaf["face_corner_owner_row_sha256s"]
        need(references == sorted(set(references)) and all(item in owner_by_hash for item in references),
             "leaf owner references")
        face_count = sum(owner_by_hash[item]["atom_kind"] == "FACE" for item in references)
        corner_count = sum(owner_by_hash[item]["atom_kind"] == "CORNER" for item in references)
        need(face_count == leaf["face_owner_count"] >= 4 and corner_count == leaf["corner_owner_count"] == 4
             and leaf["owner_rows_complete"] is True, "leaf owner census")
        leaf_id = ambient["c41_ambient_cell_id"]
        need(leaf_id not in path_by_id, "unique ambient leaf id")
        ambient_id_by_leaf_hash[leaf["row_sha256"]] = leaf_id
        path_by_id[leaf_id] = path
        if leaf["leaf_disposition"] == "STRICT_TERMINAL":
            terminal += 1
            need(ambient["disposition_family"] == "TERMINAL_EXCLUDED" and
                 leaf["strict_terminal_class"] == "EARLIEST_PREFIX_EXCLUDED" and
                 leaf["collision2_handoff"] is None and leaf["local_terminal_credit"] == 1,
                 "strict terminal leaf")
        else:
            handoff_count += 1
            need(leaf["leaf_disposition"] == "COLLISION2_HANDOFF" and
                 ambient["disposition_family"] == "RESIDUAL_OUTER" and
                 leaf["strict_terminal_class"] is None and leaf["local_terminal_credit"] == 0,
                 "collision-two handoff leaf")
            handoff = leaf["collision2_handoff"]
            need(type(handoff) is dict, "handoff object")
            open_handoff = copy.deepcopy(handoff)
            claim = open_handoff.pop("handoff_object_sha256", None)
            need(type(claim) is str and digest(open_handoff) == claim, "handoff object closure")
            outer = c41_outers[(pair, path)]
            boundary = c41_boundaries[(pair, path)]
            expected_event_order = {key: history[key] for key in (
                "official_word_key_id", "official_word_variant_id", "incoming_chart", "outgoing_chart")}
            need(handoff["next_collision_index"] == 2 and handoff["collision1_history_row_sha256"] ==
                 history["row_sha256"] and handoff["collision1_original_owner"] ==
                 history["selected_absolute_owner_id"] and handoff["collision1_event_order"] ==
                 expected_event_order, "collision-one history/event binding")
            need(handoff["exact_representative_box"] == leaf["exact_representative_box"] and
                 handoff["exact_reflected_box"] == leaf["exact_reflected_box"] and
                 handoff["C41_outer_row_sha256"] == outer["row_sha256"] and
                 handoff["C41_boundary_corner_row_sha256"] == boundary["row_sha256"],
                 "handoff exact geometry/lower-strata pins")
            need(handoff["residual_classification"] == ambient["residual_classification"] and
                 handoff["normalized_surface_ids"] ==
                 [item["normalized_surface_id"] for item in outer["normalized_surfaces"]] and
                 handoff["face_owner_rows_complete"] is True and
                 handoff["corner_owner_rows_complete"] is True and handoff["handoff_credit"] == 0,
                 "handoff residual/owner/credit")
        by_pair[pair].append(leaf)
    need((terminal, handoff_count) == (462, 319), "leaf disposition census")

    # Reconstruct the closed exact boundary complex independently from boxes.
    line_segments: dict[tuple[int, str, Fraction], list[tuple[Fraction, Fraction, str]]] = {}
    corner_incidence: dict[tuple[Any, ...], set[str]] = {}
    leaf_by_id = {ambient_id_by_leaf_hash[leaf["row_sha256"]]: leaf for leaf in leaves}
    for leaf_id, leaf in leaf_by_id.items():
        pair = leaf["pair_index"]
        t0, t1, p0, p1 = box_key(leaf["exact_representative_box"])
        need(t0 < t1 and p0 < p1, "positive leaf box")
        for axis, coordinate, low, high in (("t", t0, p0, p1), ("t", t1, p0, p1),
                                            ("p", p0, t0, t1), ("p", p1, t0, t1)):
            line_segments.setdefault((pair, axis, coordinate), []).append((low, high, leaf_id))
        for t in (t0, t1):
            for p in (p0, p1):
                corner_incidence.setdefault((pair, "CORNER", t, p), set()).add(leaf_id)
    face_incidence: dict[tuple[Any, ...], set[str]] = {}
    for (pair, axis, coordinate), segments in line_segments.items():
        endpoints = sorted({point for low, high, _leaf in segments for point in (low, high)})
        for low, high in zip(endpoints, endpoints[1:]):
            incident = {leaf_id for start, stop, leaf_id in segments if start <= low and high <= stop}
            if incident:
                face_incidence[(pair, "FACE", axis, coordinate, low, high)] = incident
    expected_incidence: dict[tuple[Any, ...], set[str]] = {**face_incidence, **corner_incidence}
    owners_by_geometry: dict[tuple[Any, ...], dict[str, Any]] = {}
    for owner in owners:
        need(owner["schema"] == CORE_SCHEMA + ".owner-row" and owner["owner_unique"] is True and
             owner["owner_rule"] == "LEXICOGRAPHIC_MINIMUM_PATH_THEN_LEAF_ID" and
             owner["owner_credit"] == owner["D02_gate_credit"] == 0, "owner schema/rule/credit")
        if owner["atom_kind"] == "FACE":
            geometry = (owner["pair_index"], "FACE", owner["axis"], q(owner["coordinate"]),
                        q(owner["span"][0]), q(owner["span"][1]))
        else:
            need(owner["atom_kind"] == "CORNER", "owner atom kind")
            geometry = (owner["pair_index"], "CORNER", q(owner["t"]), q(owner["p"]))
        need(geometry not in owners_by_geometry, "unique owner geometry")
        owners_by_geometry[geometry] = owner
    need(set(owners_by_geometry) == set(expected_incidence), "complete atomized boundary geometry")
    expected_refs: dict[str, set[str]] = {leaf_id: set() for leaf_id in leaf_by_id}
    for geometry, incident in expected_incidence.items():
        owner = owners_by_geometry[geometry]
        need(owner["incident_leaf_ids"] == sorted(incident) and
             owner["incident_leaf_count"] == len(incident), "owner exact incidence")
        expected_owner = min(incident, key=lambda leaf_id: (path_by_id[leaf_id], leaf_id))
        need(owner["owner_leaf_id"] == expected_owner, "deterministic owner")
        for leaf_id in incident:
            expected_refs[leaf_id].add(owner["row_sha256"])
    for leaf_id, leaf in leaf_by_id.items():
        need(set(leaf["face_corner_owner_row_sha256s"]) == expected_refs[leaf_id],
             "leaf complete owner incidence")

    # Derive parent proofs instead of trusting aggregate booleans.
    parent_by_pair = {row["pair_index"]: row for row in parents}
    need(len(parent_by_pair) == 12, "unique parent rows")
    for pair, pair_leaves in by_pair.items():
        parent = parent_by_pair[pair]
        paths = [leaf["path"] for leaf in pair_leaves]
        kraft = sum(Fraction(leaf["parent_volume_fraction"]) for leaf in pair_leaves)
        terminal_count = sum(leaf["leaf_disposition"] == "STRICT_TERMINAL" for leaf in pair_leaves)
        need(prefix_free(paths) and kraft == 1 and parent["path_prefix_free"] is True and
             parent["parent_Kraft_conservation"] == "1", "parent prefix/Kraft")
        need(parent["leaf_count"] == len(pair_leaves) and
             parent["terminal_leaf_count"] == terminal_count and
             parent["collision2_handoff_leaf_count"] == len(pair_leaves) - terminal_count,
             "parent leaf census")
        need(parent["C38_parent_row_sha256"] == c38_parents[pair]["row_sha256"] and
             parent["C39_parent_row_sha256"] == c39_parents[pair]["row_sha256"] and
             parent["C40_parent_row_sha256"] == c40_parents[pair]["row_sha256"] and
             parent["C41_parent_row_sha256"] == c41_parents[pair]["row_sha256"],
             "parent upstream chain")
        need(parent["representative_cell_id"] == c38_parents[pair]["representative_cell_id"] and
             parent["reflected_cell_id"] == c38_parents[pair]["reflected_cell_id"], "parent cell ids")
        need(parent["face_corner_owner_complete"] is True and
             parent["collision1_event_order_complete"] is True and
             parent["whole_representative_parent_terminal"] is False and
             parent["whole_reflected_parent_terminal"] is False and
             parent["whole_pair_credit"] == parent["D02_gate_credit"] == 0,
             "parent strict nonpromotion")

    need(result["terminal_census"] == {
        "strict_terminal_leaves": 462, "exact_collision2_handoff_leaves": 319,
        "whole_pairs_closed": 0, "whole_singletons_closed": 0, "whole_singletons_remaining": 24,
    }, "result terminal census")
    need(result["strict_nonpromotion"] == {
        "C41_partial_outers_promoted_to_terminal": False, "D02_gate_credit": 0,
        "canonical_writes_performed": False, "formal_credit": 0,
        "runtime_writes_performed": False, "whole_parent_credit": 0,
    }, "result strict nonpromotion")
    return close({
        "schema": SCHEMA + ".verification",
        "status": "PASS_SECOND_COLD_NO_PRODUCER_RECONSTRUCTION__12_PARENTS__781_LEAVES__462_TERMINAL__319_C2_HANDOFF__3141_ATOMIC_OWNERS__ZERO_CREDIT",
        "frozen_core": {
            "producer_file_sha256": PIN["producer_file"],
            "result_file_sha256": PIN["result_file"],
            "result_object_sha256": PIN["result_object"],
            "leaf_ledger_sha256": PIN["leaf_file"],
            "owner_ledger_sha256": PIN["owner_file"],
            "parent_ledger_sha256": PIN["parent_file"],
        },
        "independent_C57a_cosign": c57a,
        "coverage": {
            "reflection_pairs": 12, "singleton_cells": 24, "parent_rows": 12,
            "leaf_rows": 781, "strict_terminal_leaves": 462,
            "exact_collision2_handoffs": 319, "atomic_face_corner_owner_rows": 3141,
            "C38_child_rows": 164, "C39_routed_rows": 164,
            "C40_leaf_rows": 299, "C41_ambient_rows": 781, "C41_split_face_rows": 482,
        },
        "reconstructed_invariants": {
            "all_parent_paths_prefix_free": True,
            "all_parent_Kraft_sums_exactly_one": True,
            "all_C38_C39_C40_C41_leaf_and_parent_chains_exact": True,
            "all_319_handoff_objects_and_C35_event_orders_exact": True,
            "all_3141_atomic_geometries_incidence_sets_and_owners_exact": True,
            "hanging_node_faces_resegmented_at_all_exact_endpoints": True,
        },
        "whole_singletons_closed": 0,
        "whole_singletons_remaining": 24,
        "candidate_is_authority": False,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
        "independence": independence,
    })


def synthetic_validate(value: dict[str, Any]) -> None:
    required = {
        "schema", "parents", "leaves", "terminal", "handoff", "owners", "next_collision",
        "event_bound", "face_complete", "corner_complete", "prefix_free", "Kraft",
        "whole_closed", "formal_credit", "whole_parent_credit", "owner_credit",
        "D02_gate_credit", "object_sha256",
    }
    need(type(value) is dict and set(value) == required, "synthetic closed schema")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256")
    need(digest(body) == claim, "synthetic closure")
    need(value == close({
        "schema": "synthetic.c57s1", "parents": 12, "leaves": 781, "terminal": 462,
        "handoff": 319, "owners": 3141, "next_collision": 2, "event_bound": True,
        "face_complete": True, "corner_complete": True, "prefix_free": True, "Kraft": "1",
        "whole_closed": 0, "formal_credit": 0, "whole_parent_credit": 0,
        "owner_credit": 0, "D02_gate_credit": 0,
    }), "synthetic invariants")


def self_test() -> dict[str, Any]:
    baseline = close({
        "schema": "synthetic.c57s1", "parents": 12, "leaves": 781, "terminal": 462,
        "handoff": 319, "owners": 3141, "next_collision": 2, "event_bound": True,
        "face_complete": True, "corner_complete": True, "prefix_free": True, "Kraft": "1",
        "whole_closed": 0, "formal_credit": 0, "whole_parent_credit": 0,
        "owner_credit": 0, "D02_gate_credit": 0,
    })
    synthetic_validate(baseline)
    tests: dict[str, bool] = {"baseline_valid": True}
    attacks: list[tuple[str, str, Any]] = [
        ("parents", "parents", 11), ("leaves", "leaves", 780),
        ("terminal", "terminal", 463), ("handoff", "handoff", 318),
        ("owners", "owners", 3140), ("collision_index", "next_collision", 3),
        ("event_order", "event_bound", False), ("face_coverage", "face_complete", False),
        ("corner_coverage", "corner_complete", False), ("prefix", "prefix_free", False),
        ("Kraft_gap", "Kraft", "1023/1024"), ("whole_closure", "whole_closed", 1),
        ("formal_credit", "formal_credit", 1), ("whole_parent_credit", "whole_parent_credit", 1),
        ("owner_credit", "owner_credit", 1), ("D02_credit", "D02_gate_credit", 1),
    ]
    for name, field, replacement in attacks:
        attacked = copy.deepcopy(baseline)
        attacked.pop("object_sha256")
        attacked[field] = replacement
        attacked = close(attacked)
        try:
            synthetic_validate(attacked)
        except Rejected:
            tests["coherent_" + name + "_rejected"] = True
    malformed = (
        ("duplicate_key", b'{"a":1,"a":2}\n'),
        ("NaN", b'{"a":NaN}\n'),
        ("BOM", b'\xef\xbb\xbf{"a":1}\n'),
        ("trailing_bytes", b'{"a":1}\nX'),
    )
    for name, raw in malformed:
        try:
            parse(raw, name, canonical_required=True)
        except Rejected:
            tests[name + "_rejected"] = True
    with tempfile.TemporaryDirectory(prefix="cm2-c57s1-cold-") as temporary:
        root = Path(temporary)
        target = root / "target"
        target.write_bytes(canonical(baseline) + b"\n")
        link = root / "link"
        link.symlink_to(target.name)
        try:
            capture((link,))
        except OSError:
            tests["symlink_rejected"] = True
        hard = root / "hard"
        os.link(target, hard)
        try:
            capture((target,))
        except Rejected:
            tests["hardlink_rejected"] = True
        hard.unlink()
        replacement = root / "replacement"
        replacement.write_bytes(canonical(baseline) + b"\n")
        try:
            capture((target,), hook=lambda: os.replace(replacement, target))
        except Rejected:
            tests["TOCTOU_replacement_rejected"] = True
    source = capture((PRODUCER,))[PRODUCER]
    tests["producer_not_imported_or_executed"] = not producer_independence(source)["producer_imported"]
    need(len(tests) == 25 and all(tests.values()), "25/25 hostile tests")
    return close({
        "schema": SCHEMA + ".self-test",
        "status": "PASS_25_OF_25_EXECUTED_HOSTILE_TESTS",
        "tests": tests,
        "test_count": 25,
        "synthetic_is_authority": False,
        "formal_credit": 0,
        "whole_parent_credit": 0,
        "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        value = verify() if args.verify else self_test()
        sys.stdout.buffer.write(canonical(value) + b"\n")
        return 0
    except (Rejected, OSError, KeyError, ValueError, zlib.error) as exc:
        failure = close({
            "schema": SCHEMA + ".fail-closed",
            "status": "FAIL_CLOSED_REJECTED",
            "reason": str(exc),
            "formal_credit": 0,
            "whole_parent_credit": 0,
            "D02_gate_credit": 0,
            "runtime_canonical_pointer_or_seal_writes": False,
        })
        sys.stdout.buffer.write(canonical(failure) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
