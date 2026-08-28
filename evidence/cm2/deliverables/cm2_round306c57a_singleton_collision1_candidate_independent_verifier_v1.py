#!/usr/bin/env python3
"""Independent, no-producer audit of the frozen C57s1 candidate."""

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
SCHEMA = "cm2.round306c57a.singleton-collision1-candidate-independent-verifier.v1"
S1_SCHEMA = "cm2.round306c57s1.singleton-collision1-common-refinement.v1"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
PAIRS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)

PRODUCER = OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_v1.py"
RESULT = OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_result_v1.json"
LEAVES = OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_leaf_ledger_v1.jsonl.gz"
OWNERS = OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_face_corner_owner_ledger_v1.jsonl.gz"
PARENTS = OUT / "cm2_round306c57s1_singleton_collision1_common_refinement_parent_ledger_v1.jsonl.gz"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C38 = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C39 = ROOT / ".cm2-runtime/candidates/c39-h1-c1-graph-router-20260810T185014Z-e004fadaadcd5559"
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C41 = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"

PINS = {
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
}


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def bytes_sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def close(value: dict[str, Any], key: str = "object_sha256") -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need(key not in answer, "open object")
    answer[key] = digest(answer)
    return answer


def duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for key, value in pairs:
        if key in answer:
            raise Rejected("duplicate key:" + key)
        answer[key] = value
    return answer


def parse(raw: bytes, label: str, canonical_required: bool = False) -> Any:
    need(bool(raw) and not raw.startswith(b"\xef\xbb\xbf"), label + " strict bytes")
    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=duplicate_guard,
                           parse_constant=lambda token: (_ for _ in ()).throw(Rejected(label + ":" + token)))
    except Rejected:
        raise
    except Exception as exc:
        raise Rejected(label + " JSON:" + str(exc)) from exc
    if canonical_required:
        need(raw == canonical(value) + b"\n", label + " canonical bytes")
    return value


def fp(item: os.stat_result) -> tuple[int, ...]:
    return (item.st_dev, item.st_ino, item.st_mode, item.st_nlink, item.st_size, item.st_mtime_ns, item.st_ctime_ns)


def stable_bundle(paths: Iterable[Path], maximum: int = 128 << 20,
                  hook: Callable[[], None] | None = None) -> dict[Path, bytes]:
    ordered = tuple(paths)
    fds: dict[Path, int] = {}
    before: dict[Path, os.stat_result] = {}
    try:
        for path in ordered:
            fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
            state = os.fstat(fd)
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and 0 < state.st_size <= maximum,
                 "single-link regular input")
            fds[path] = fd; before[path] = state
        raws: dict[Path, bytes] = {}
        for path in ordered:
            pieces: list[bytes] = []
            while block := os.read(fds[path], 4 << 20):
                pieces.append(block)
            raws[path] = b"".join(pieces)
        if hook:
            hook()
        for path in ordered:
            need(fp(before[path]) == fp(os.fstat(fds[path])) == fp(os.stat(path, follow_symlinks=False)),
                 "bundle TOCTOU/freeze stability")
        return raws
    finally:
        for fd in fds.values():
            os.close(fd)


def closed_result(raw: bytes, file_pin: str, object_pin: str, label: str) -> dict[str, Any]:
    need(bytes_sha(raw) == file_pin, label + " file pin")
    value = parse(raw, label)
    need(type(value) is dict and value.get("object_sha256") == object_pin, label + " object claim")
    body = copy.deepcopy(value); body.pop("object_sha256")
    need(digest(body) == object_pin, label + " object reconstruction")
    return value


def rows(raw: bytes, descriptor: dict[str, Any], file_pin: str, label: str) -> list[dict[str, Any]]:
    need(bytes_sha(raw) == file_pin == descriptor["sha256"], label + " file pin")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        expanded = decoder.decompress(raw, 768 << 20) + decoder.flush()
    except zlib.error as exc:
        raise Rejected(label + " gzip:" + str(exc)) from exc
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail, label + " one gzip member")
    lines = expanded.splitlines(keepends=True)
    need(len(lines) == descriptor["row_count"], label + " row count")
    answer: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for line in lines:
        row = parse(line, label + " row", canonical_required=True)
        claim = row.get("row_sha256")
        need(type(claim) is str and HEX64.fullmatch(claim) is not None, label + " row claim")
        body = copy.deepcopy(row); body.pop("row_sha256")
        need(digest(body) == claim, label + " row closure")
        sequence.update((claim + "\n").encode("ascii"))
        answer.append(row)
    need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], label + " row sequence")
    return answer


def q(value: str) -> Fraction:
    return Fraction(value)


def prefix_free(paths: list[str]) -> bool:
    ordered = sorted(paths, key=lambda item: (len(item), item))
    return all(not later.startswith(first) for index, first in enumerate(ordered)
               for later in ordered[index + 1:])


def box_key(box: dict[str, Any]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return q(box["t"][0]), q(box["t"][1]), q(box["p"][0]), q(box["p"][1])


def expected_face_atoms(leaf: dict[str, Any]) -> list[tuple[int, str, Fraction, Fraction, Fraction, str]]:
    pair = leaf["pair_index"]
    t0, t1, p0, p1 = box_key(leaf["exact_representative_box"])
    return [(pair, "t", t0, p0, p1, "T_MINUS"), (pair, "t", t1, p0, p1, "T_PLUS"),
            (pair, "p", p0, t0, t1, "P_MINUS"), (pair, "p", p1, t0, t1, "P_PLUS")]


def independence() -> dict[str, Any]:
    source = stable_bundle((PRODUCER,))[PRODUCER]
    need(bytes_sha(source) == PINS["producer_file"], "producer file pin")
    tree = ast.parse(source.decode("utf-8"), filename=PRODUCER.name)
    imported: list[str] = []
    dynamic: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import): imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom): imported.append(node.module or "")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval", "compile", "__import__"}:
            dynamic.append(node.func.id)
    need(not any("cm2_round306c57s1" in item for item in imported) and not dynamic,
         "producer not imported/executed")
    need(not any("cm2_round306c57s1" in name for name in sys.modules), "producer absent sys.modules")
    return {"producer_imported": False, "producer_executed": False,
            "producer_consumed_as_inert_AST_and_bytes_only": True}


def verify() -> dict[str, Any]:
    source_paths = (PRODUCER, RESULT, LEAVES, OWNERS, PARENTS,
                    C38 / "result.json", C39 / "result.json", C40 / "result.json", C41 / "result.json")
    raw = stable_bundle(source_paths)
    need(bytes_sha(raw[PRODUCER]) == PINS["producer_file"], "producer pin")
    result = closed_result(raw[RESULT], PINS["result_file"], PINS["result_object"], "C57s1 result")
    c38 = closed_result(raw[C38 / "result.json"], PINS["C38_file"], PINS["C38_object"], "C38")
    c39 = closed_result(raw[C39 / "result.json"], PINS["C39_file"], PINS["C39_object"], "C39")
    c40 = closed_result(raw[C40 / "result.json"], PINS["C40_file"], PINS["C40_object"], "C40")
    c41 = closed_result(raw[C41 / "result.json"], PINS["C41_file"], PINS["C41_object"], "C41")
    need(result["authority_objects"]["C38"] == PINS["C38_object"]
         and result["authority_objects"]["C39"] == PINS["C39_object"]
         and result["authority_objects"]["C40"] == PINS["C40_object"]
         and result["authority_objects"]["C41"] == PINS["C41_object"], "C38-C41 result pins")

    leaves = rows(raw[LEAVES], result["ledgers"]["leaves"], PINS["leaf_file"], "C57s1 leaves")
    owners = rows(raw[OWNERS], result["ledgers"]["face_corner_owners"], PINS["owner_file"], "C57s1 owners")
    parents = rows(raw[PARENTS], result["ledgers"]["parents"], PINS["parent_file"], "C57s1 parents")
    need(len(leaves) == 781 and len(owners) == 3141 and len(parents) == 12, "candidate row census")
    need(tuple(parent["pair_index"] for parent in parents) == PAIRS, "parent pair order")

    # Upstream ledgers needed to independently validate every chain.
    upstream_paths: list[Path] = []
    for directory, value, names in (
        (C38, c38, ("collision1_2_child_pairs", "representative_parent_conservation")),
        (C39, c39, ("routed_child_pairs", "parent_conservation")),
        (C40, c40, ("routed_leaf_cells", "parent_conservation")),
        (C41, c41, ("routed_ambient_cells", "parent_conservation", "c1_h1_surface_outers", "boundary_corner_outers", "split_face_adjacency")),
    ):
        upstream_paths.extend(directory / value["ledgers"][name]["filename"] for name in names)
    upstream_raw = stable_bundle(upstream_paths, maximum=768 << 20)
    def get(directory: Path, value: dict[str, Any], name: str) -> list[dict[str, Any]]:
        path = directory / value["ledgers"][name]["filename"]
        return rows(upstream_raw[path], value["ledgers"][name], value["ledgers"][name]["sha256"], name)
    c38_children = {item["row_sha256"]: item for item in get(C38, c38, "collision1_2_child_pairs") if item["pair_index"] in PAIRS}
    c38_parents = {item["pair_index"]: item for item in get(C38, c38, "representative_parent_conservation") if item["pair_index"] in PAIRS}
    c39_children = {item["row_sha256"]: item for item in get(C39, c39, "routed_child_pairs") if item["pair_index"] in PAIRS}
    c39_by_c38 = {item["c38_child_row_sha256"]: item for item in c39_children.values()}
    c39_parents = {item["pair_index"]: item for item in get(C39, c39, "parent_conservation") if item["pair_index"] in PAIRS}
    c40_leaves = {item["row_sha256"]: item for item in get(C40, c40, "routed_leaf_cells") if item["pair_index"] in PAIRS}
    c40_parents = {item["pair_index"]: item for item in get(C40, c40, "parent_conservation") if item["pair_index"] in PAIRS}
    c41_ambient = {item["row_sha256"]: item for item in get(C41, c41, "routed_ambient_cells") if item["pair_index"] in PAIRS}
    c41_parents = {item["pair_index"]: item for item in get(C41, c41, "parent_conservation") if item["pair_index"] in PAIRS}
    c41_outers = {(item["pair_index"], item["descendant_path"]): item for item in get(C41, c41, "c1_h1_surface_outers") if item["pair_index"] in PAIRS}
    c41_boundaries = {(item["pair_index"], item["descendant_path"]): item for item in get(C41, c41, "boundary_corner_outers") if item["pair_index"] in PAIRS}
    split_count = sum(item["pair_index"] in PAIRS for item in get(C41, c41, "split_face_adjacency"))
    need(len(c38_children) == 164 and len(c39_by_c38) == 164 and len(c40_leaves) == 299
         and len(c41_ambient) == 781 and len(c41_outers) == len(c41_boundaries) == 319
         and split_count == 482, "C38-C41 target coverage")

    # C35 collision-one history is read independently.
    c35_raw = stable_bundle((C35 / "result.json",))[C35 / "result.json"]
    c35_value = parse(c35_raw, "C35")
    body = copy.deepcopy(c35_value); claim = body.pop("object_sha256")
    need(claim == PINS["C35_object"] and digest(body) == claim, "C35 object")
    history_path = C35 / c35_value["ledgers"]["path_occurrences"]["filename"]
    history_raw = stable_bundle((history_path,))[history_path]
    history_rows = rows(history_raw, c35_value["ledgers"]["path_occurrences"],
                        c35_value["ledgers"]["path_occurrences"]["sha256"], "C35 history")
    history = history_rows[0]
    need(history["collision_index"] == 1, "collision-one history")

    leaf_by_hash = {leaf["row_sha256"]: leaf for leaf in leaves}
    owner_by_hash = {owner["row_sha256"]: owner for owner in owners}
    ambient_to_leaf = {leaf["C41_ambient_row_sha256"]: leaf for leaf in leaves}
    need(len(leaf_by_hash) == len(ambient_to_leaf) == len(leaves), "unique leaf identities")
    terminal = handoff = 0
    by_pair: dict[int, list[dict[str, Any]]] = {pair: [] for pair in PAIRS}
    for leaf in leaves:
        pair, path = leaf["pair_index"], leaf["path"]
        need(pair in by_pair and set(path) <= {"0", "1"}, "leaf pair/path")
        ambient = c41_ambient[leaf["C41_ambient_row_sha256"]]
        c40_leaf = c40_leaves[leaf["C40_leaf_row_sha256"]]
        c38_child = c38_children[leaf["C38_child_row_sha256"]]
        c39_child = c39_children[leaf["C39_routed_row_sha256"]]
        need(ambient["path"] == path and ambient["pair_index"] == pair
             and ambient["row_sha256"] == leaf["C41_ambient_row_sha256"], "C41 leaf chain")
        need(ambient["c40_source_row_sha256"] == c40_leaf["row_sha256"], "C40-C41 chain")
        need(c40_leaf["c38_source_row_sha256"] == c38_child["row_sha256"]
             and c40_leaf["c39_source_row_sha256"] == c39_child["row_sha256"]
             and c39_by_c38[c38_child["row_sha256"]]["row_sha256"] == c39_child["row_sha256"],
             "C38-C39-C40 chain")
        need(leaf["exact_representative_box"] == ambient["closed_representative_box"]
             and leaf["exact_reflected_box"] == ambient["closed_reflected_box"]
             and leaf["parent_volume_fraction"] == ambient["parent_volume_fraction"],
             "exact leaf geometry/volume")
        need(leaf["whole_parent_credit"] == leaf["D02_gate_credit"] == 0
             and leaf["event_order_bound_to_C35_collision1"] is True, "leaf zero-credit/event lock")
        hashes = leaf["face_corner_owner_row_sha256s"]
        need(type(hashes) is list and hashes == sorted(set(hashes))
             and all(item in owner_by_hash for item in hashes), "leaf owner refs")
        actual_face = [owner_by_hash[item] for item in hashes if owner_by_hash[item]["atom_kind"] == "FACE"]
        actual_corner = [owner_by_hash[item] for item in hashes if owner_by_hash[item]["atom_kind"] == "CORNER"]
        need(len(actual_face) == leaf["face_owner_count"] >= 4
             and len(actual_corner) == leaf["corner_owner_count"] == 4
             and leaf["owner_rows_complete"] is True, "leaf owner coverage")
        if leaf["leaf_disposition"] == "STRICT_TERMINAL":
            terminal += 1
            need(ambient["disposition_family"] == "TERMINAL_EXCLUDED"
                 and leaf["strict_terminal_class"] == "EARLIEST_PREFIX_EXCLUDED"
                 and leaf["collision2_handoff"] is None
                 and leaf["local_terminal_credit"] == 1, "terminal classification")
        else:
            handoff += 1
            need(leaf["leaf_disposition"] == "COLLISION2_HANDOFF"
                 and ambient["disposition_family"] == "RESIDUAL_OUTER"
                 and leaf["strict_terminal_class"] is None
                 and leaf["local_terminal_credit"] == 0, "handoff classification")
            value = leaf["collision2_handoff"]
            need(type(value) is dict, "handoff object")
            open_value = copy.deepcopy(value); object_hash = open_value.pop("handoff_object_sha256")
            need(digest(open_value) == object_hash and value["next_collision_index"] == 2
                 and value["collision1_history_row_sha256"] == history["row_sha256"]
                 and value["collision1_original_owner"] == history["selected_absolute_owner_id"]
                 and value["exact_representative_box"] == leaf["exact_representative_box"]
                 and value["exact_reflected_box"] == leaf["exact_reflected_box"], "exact C2 handoff")
            outer = c41_outers[(pair, path)]; boundary = c41_boundaries[(pair, path)]
            need(value["C41_outer_row_sha256"] == outer["row_sha256"]
                 and value["C41_boundary_corner_row_sha256"] == boundary["row_sha256"]
                 and value["normalized_surface_ids"] == [item["normalized_surface_id"] for item in outer["normalized_surfaces"]],
                 "C2 lower-strata binding")
        by_pair[pair].append(leaf)
    need(terminal == 462 and handoff == 319, "terminal/handoff census")

    # Recompute global owner incidence and deterministic lexicographic owners.
    leaf_id_to_leaf = {
        c41_ambient[leaf["C41_ambient_row_sha256"]]["c41_ambient_cell_id"]: leaf
        for leaf in leaves
    }
    need(len(leaf_id_to_leaf) == len(leaves), "unique C41 ambient leaf ids")
    path_by_leaf_id = {leaf_id: leaf["path"] for leaf_id, leaf in leaf_id_to_leaf.items()}

    # Independently atomize every exact box boundary.  A face atom is one open
    # interval between consecutive exact endpoints on a common boundary line;
    # corners are exact endpoint pairs.  This reconstruction neither trusts the
    # candidate owner census nor merely echoes the leaf-provided owner hashes.
    line_segments: dict[tuple[int, str, Fraction], list[tuple[Fraction, Fraction, str]]] = {}
    corner_incidence: dict[tuple[int, str, Fraction, Fraction], set[str]] = {}
    for leaf_id, leaf in leaf_id_to_leaf.items():
        pair = leaf["pair_index"]
        t0, t1, p0, p1 = box_key(leaf["exact_representative_box"])
        need(t0 < t1 and p0 < p1, "positive exact leaf box")
        for axis, coordinate, low, high in (("t", t0, p0, p1), ("t", t1, p0, p1),
                                            ("p", p0, t0, t1), ("p", p1, t0, t1)):
            line_segments.setdefault((pair, axis, coordinate), []).append((low, high, leaf_id))
        for t_value in (t0, t1):
            for p_value in (p0, p1):
                corner_incidence.setdefault((pair, "CORNER", t_value, p_value), set()).add(leaf_id)

    face_incidence: dict[tuple[int, str, str, Fraction, Fraction, Fraction], set[str]] = {}
    for (pair, axis, coordinate), segments in line_segments.items():
        endpoints = sorted({value for low, high, _leaf_id in segments for value in (low, high)})
        for low, high in zip(endpoints, endpoints[1:]):
            if low == high:
                continue
            incident = {leaf_id for start, stop, leaf_id in segments if start <= low and high <= stop}
            if incident:
                face_incidence[(pair, "FACE", axis, coordinate, low, high)] = incident

    owner_by_geometry: dict[tuple[Any, ...], dict[str, Any]] = {}
    for owner in owners:
        if owner["atom_kind"] == "FACE":
            geometry: tuple[Any, ...] = (owner["pair_index"], "FACE", owner["axis"],
                                         q(owner["coordinate"]), q(owner["span"][0]), q(owner["span"][1]))
        else:
            need(owner["atom_kind"] == "CORNER", "closed owner atom kind")
            geometry = (owner["pair_index"], "CORNER", q(owner["t"]), q(owner["p"]))
        need(geometry not in owner_by_geometry, "unique owner geometry")
        owner_by_geometry[geometry] = owner
    expected_incidence: dict[tuple[Any, ...], set[str]] = {}
    expected_incidence.update(face_incidence)
    expected_incidence.update(corner_incidence)
    need(set(owner_by_geometry) == set(expected_incidence), "complete exact atomic face/corner geometry")

    owner_refs: dict[str, set[str]] = {claim: set() for claim in owner_by_hash}
    for leaf in leaves:
        leaf_id = c41_ambient[leaf["C41_ambient_row_sha256"]]["c41_ambient_cell_id"]
        for claim in leaf["face_corner_owner_row_sha256s"]:
            owner_refs[claim].add(leaf_id)
    need(all(owner_refs.values()), "every owner row consumed")
    expected_claims_by_leaf: dict[str, set[str]] = {leaf_id: set() for leaf_id in leaf_id_to_leaf}
    for geometry, incident in expected_incidence.items():
        owner = owner_by_geometry[geometry]
        claim = owner["row_sha256"]
        need(set(owner["incident_leaf_ids"]) == incident, "owner exact geometric incidence")
        for leaf_id in incident:
            expected_claims_by_leaf[leaf_id].add(claim)
    for leaf_id, leaf in leaf_id_to_leaf.items():
        need(set(leaf["face_corner_owner_row_sha256s"]) == expected_claims_by_leaf[leaf_id],
             "leaf complete exact atomic owner references")
    for claim, owner in owner_by_hash.items():
        need(owner["incident_leaf_ids"] == sorted(owner_refs[claim])
             and owner["incident_leaf_count"] == len(owner_refs[claim])
             and owner["owner_unique"] is True
             and owner["owner_rule"] == "LEXICOGRAPHIC_MINIMUM_PATH_THEN_LEAF_ID"
             and owner["owner_credit"] == owner["D02_gate_credit"] == 0,
             "owner incidence/zero-credit")
        expected_owner = min(owner["incident_leaf_ids"], key=lambda leaf_id: (path_by_leaf_id[leaf_id], leaf_id))
        need(owner["owner_leaf_id"] == expected_owner, "owner deterministic rule")

    # Parent rows are derived, never trusted.
    for parent in parents:
        pair = parent["pair_index"]
        pair_leaves = by_pair[pair]
        paths = [leaf["path"] for leaf in pair_leaves]
        kraft = sum(Fraction(leaf["parent_volume_fraction"]) for leaf in pair_leaves)
        terminal_count = sum(leaf["leaf_disposition"] == "STRICT_TERMINAL" for leaf in pair_leaves)
        need(prefix_free(paths) and kraft == 1 and parent["path_prefix_free"] is True
             and parent["parent_Kraft_conservation"] == "1", "parent prefix/Kraft")
        need(parent["leaf_count"] == len(pair_leaves)
             and parent["terminal_leaf_count"] == terminal_count
             and parent["collision2_handoff_leaf_count"] == len(pair_leaves) - terminal_count,
             "parent census")
        need(parent["C38_parent_row_sha256"] == c38_parents[pair]["row_sha256"]
             and parent["C39_parent_row_sha256"] == c39_parents[pair]["row_sha256"]
             and parent["C40_parent_row_sha256"] == c40_parents[pair]["row_sha256"]
             and parent["C41_parent_row_sha256"] == c41_parents[pair]["row_sha256"], "parent upstream chain")
        need(parent["whole_representative_parent_terminal"] is False
             and parent["whole_reflected_parent_terminal"] is False
             and parent["whole_pair_credit"] == parent["D02_gate_credit"] == 0,
             "parent strict nonpromotion")

    need(result["terminal_census"] == {
        "exact_collision2_handoff_leaves": 319, "strict_terminal_leaves": 462,
        "whole_pairs_closed": 0, "whole_singletons_closed": 0,
        "whole_singletons_remaining": 24,
    }, "result terminal census")
    need(result["strict_nonpromotion"]["formal_credit"] == 0
         and result["strict_nonpromotion"]["D02_gate_credit"] == 0
         and result["strict_nonpromotion"]["whole_parent_credit"] == 0,
         "result zero-credit")
    return close({
        "schema": SCHEMA + ".verification",
        "status": "PASS_INDEPENDENT_C57S1_12_PARENT_781_LEAF_3141_OWNER_AND_C2_HANDOFF_AUDIT__ZERO_FORMAL_CREDIT",
        "frozen_candidate": {
            "producer_file_sha256": PINS["producer_file"],
            "result_file_sha256": PINS["result_file"], "result_object_sha256": PINS["result_object"],
            "leaf_file_sha256": PINS["leaf_file"], "owner_file_sha256": PINS["owner_file"],
            "parent_file_sha256": PINS["parent_file"],
        },
        "freeze_race_observed_before_final_snapshot": {
            "observed": True,
            "disposition": "EXCLUDED_PRE_FREEZE_BYTES_NOT_CONSUMED",
            "final_snapshot_stable_and_exactly_pinned": True,
        },
        "upstream_objects": {key: PINS[key] for key in ("C38_object", "C39_object", "C40_object", "C41_object")},
        "coverage": {"parent_rows": 12, "leaf_rows": 781, "strict_terminal_leaves": 462,
                     "exact_collision2_handoffs": 319, "atomic_owner_rows": 3141,
                     "C38_child_rows": 164, "C39_routed_rows": 164,
                     "C40_leaf_rows": 299, "C41_split_face_rows": 482},
        "invariants": {"all_12_prefix_free": True, "all_12_Kraft_one": True,
                       "all_3141_atomic_face_corner_geometries_reconstructed": True,
                       "all_owner_incidence_and_unique_rules_reconstructed": True,
                       "all_319_C2_handoffs_exactly_bound": True,
                       "all_C38_C39_C40_C41_chains_reconstructed": True},
        "whole_singletons_closed": 0, "whole_singletons_remaining": 24,
        "candidate_is_authority": False, "formal_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
        "independence": independence(),
    })


def reclose(value: dict[str, Any], mutation: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    answer = copy.deepcopy(value); answer.pop("object_sha256", None); mutation(answer); return close(answer)


def validate_synthetic(value: dict[str, Any]) -> None:
    need(type(value) is dict and set(value) == {
        "schema", "formal_credit", "D02_gate_credit", "terminal", "handoff",
        "owners", "prefix_free", "Kraft", "whole_closed", "object_sha256",
    }, "synthetic closed schema")
    body = copy.deepcopy(value); claim = body.pop("object_sha256")
    need(digest(body) == claim, "synthetic object closure")
    need(value["schema"] == "synthetic" and value["formal_credit"] == 0
         and value["D02_gate_credit"] == 0 and value["terminal"] == 462
         and value["handoff"] == 319 and value["owners"] == 3141
         and value["prefix_free"] is True and value["Kraft"] == "1"
         and value["whole_closed"] == 0, "synthetic invariant set")


def self_test() -> dict[str, Any]:
    tests: dict[str, bool] = {}
    baseline = close({"schema": "synthetic", "formal_credit": 0, "D02_gate_credit": 0,
                      "terminal": 462, "handoff": 319, "owners": 3141,
                      "prefix_free": True, "Kraft": "1", "whole_closed": 0})
    validate_synthetic(baseline)
    tests["synthetic_baseline_valid"] = True
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("formal_credit", lambda x: x.__setitem__("formal_credit", 1)),
        ("D02_credit", lambda x: x.__setitem__("D02_gate_credit", 1)),
        ("terminal_census", lambda x: x.__setitem__("terminal", 463)),
        ("handoff_census", lambda x: x.__setitem__("handoff", 318)),
        ("owner_census", lambda x: x.__setitem__("owners", 3142)),
        ("prefix", lambda x: x.__setitem__("prefix_free", False)),
        ("Kraft", lambda x: x.__setitem__("Kraft", "255/256")),
        ("whole_closed", lambda x: x.__setitem__("whole_closed", 1)),
    ]
    for name, mutation in attacks:
        attacked = reclose(baseline, mutation)
        try:
            validate_synthetic(attacked)
        except Rejected:
            tests["coherent_" + name + "_rejected"] = True
    for name, raw in (("duplicate_JSON", b'{"a":1,"a":2}\n'), ("NaN", b'{"a":NaN}\n'),
                      ("BOM", b'\xef\xbb\xbf{"a":1}\n')):
        try: parse(raw, name)
        except Rejected: tests[name + "_rejected"] = True
    with tempfile.TemporaryDirectory(prefix="cm2-c57a-") as temporary:
        root = Path(temporary); target = root / "x"; target.write_bytes(canonical(baseline) + b"\n")
        link = root / "link"; link.symlink_to(target.name)
        try: stable_bundle((link,))
        except OSError: tests["symlink_rejected"] = True
        hard = root / "hard"; os.link(target, hard)
        try: stable_bundle((target,))
        except Rejected: tests["hardlink_rejected"] = True
        hard.unlink(); replacement = root / "new"; replacement.write_bytes(canonical(baseline) + b"\n")
        try: stable_bundle((target,), hook=lambda: os.replace(replacement, target))
        except Rejected: tests["TOCTOU_rejected"] = True
    tests["producer_not_imported_or_executed"] = not independence()["producer_imported"]
    need(all(tests.values()) and len(tests) == 16, "16 executed tests")
    return close({"schema": SCHEMA + ".self-test", "status": "PASS_16_OF_16_EXECUTED_HOSTILE_TESTS",
                  "tests": tests, "test_count": len(tests), "synthetic_is_authority": False,
                  "formal_credit": 0, "D02_gate_credit": 0,
                  "runtime_canonical_pointer_or_seal_writes": False})


def main() -> int:
    parser = argparse.ArgumentParser(); group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify", action="store_true"); group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        output = verify() if args.verify else self_test()
        sys.stdout.buffer.write(canonical(output) + b"\n"); return 0
    except (Rejected, OSError, zlib.error, KeyError, ValueError) as exc:
        failure = close({"schema": SCHEMA + ".fail-closed", "status": "FAIL_CLOSED_REJECTED",
                         "reason": str(exc), "formal_credit": 0, "D02_gate_credit": 0,
                         "runtime_canonical_pointer_or_seal_writes": False})
        sys.stdout.buffer.write(canonical(failure) + b"\n"); return 1


if __name__ == "__main__":
    raise SystemExit(main())
