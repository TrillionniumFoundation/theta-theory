#!/usr/bin/env python3
"""C57s1: materialize collision-one common refinements for 24 singletons.

The exact C38--C41 collision-one routing is consumed as frozen inert bytes.
C41 ambient leaves already form a prefix-free/Kraft-one partition.  This
round closes their face/corner ownership globally, binds the collision-one
event-order history, and turns every nonterminal ambient leaf into an exact
collision-two handoff.  No unresolved outer is promoted to a terminal.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c57s1_singleton_collision1_common_refinement"
LEAF_FILE = PREFIX + "_leaf_ledger_v1.jsonl.gz"
OWNER_FILE = PREFIX + "_face_corner_owner_ledger_v1.jsonl.gz"
PARENT_FILE = PREFIX + "_parent_ledger_v1.jsonl.gz"
RESULT_FILE = PREFIX + "_result_v1.json"
SCHEMA = "cm2.round306c57s1.singleton-collision1-common-refinement.v1"

C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C38 = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C39 = ROOT / ".cm2-runtime/candidates/c39-h1-c1-graph-router-20260810T185014Z-e004fadaadcd5559"
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C41 = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C56 = OUT / "cm2_round306c56s_singleton_whole_cell_terminal_audit_result_v1.json"
C56_SINGLETONS = OUT / "cm2_round306c56s_singleton_whole_cell_terminal_audit_singleton_ledger_v1.jsonl.gz"

OBJECT = {
    "C35": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C38": "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434",
    "C39": "821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02",
    "C40": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "C41": "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    "C56": "c0e90419a49ca4054897b0985933478bea5d6893ae33048176c4c46194e1f6da",
}
FILE = {
    "C38": "094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    "C39": "f9bfacbdaaf5263ba16397e70fe56b4f31149087c2434b7c163ff284b40cfd7e",
    "C40": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C41": "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    "C56": "7479c162a7e408bf17ae1f8fc36cbaa41281b8899116549d79010afdfceccc3c",
}
PAIRS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)


class FailClosed(RuntimeError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise FailClosed(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in out, f"duplicate key:{path}:{key}")
            out[key] = value
        return out
    value = json.loads(path.read_text(), object_pairs_hook=hook)
    require(isinstance(value, dict), f"object:{path}")
    return value


def validate_result(directory: Path, label: str) -> dict[str, Any]:
    path = directory / "result.json"
    require(file_sha(path) == FILE.get(label, file_sha(path)), f"file pin:{label}")
    value = strict_json(path)
    body = dict(value)
    claim = body.pop("object_sha256")
    require(claim == OBJECT[label] and digest(body) == claim, f"object pin:{label}")
    return value


def read_ledger(path: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    require(file_sha(path) == descriptor["sha256"], f"ledger file:{path}")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt") as stream:
        for line in stream:
            row = json.loads(line)
            claim = row.pop("row_sha256")
            require(digest(row) == claim, f"row closure:{path}")
            row["row_sha256"] = claim
            sequence.update((claim + "\n").encode())
            rows.append(row)
    require(len(rows) == descriptor["row_count"] and sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], f"ledger descriptor:{path}")
    return rows


class Writer:
    def __init__(self, path: Path, order: str):
        self.path, self.order = path, order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.gz: Any = None

    def __enter__(self) -> "Writer":
        self.raw = self.path.open("wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, row: dict[str, Any]) -> dict[str, Any]:
        claim = digest(row)
        closed = {**row, "row_sha256": claim}
        self.gz.write(canonical(closed) + b"\n")
        self.sequence.update((claim + "\n").encode())
        self.count += 1
        return closed

    def __exit__(self, *_: Any) -> None:
        self.gz.close(); self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {"filename": self.path.name, "order": self.order, "row_count": self.count, "row_hash_line_sequence_sha256": self.sequence.hexdigest(), "sha256": file_sha(self.path), "size": self.path.stat().st_size}


def q(value: str) -> Fraction:
    return Fraction(value)


def box_key(box: dict[str, Any]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return q(box["t"][0]), q(box["t"][1]), q(box["p"][0]), q(box["p"][1])


def atom_key(axis: str, coordinate: str, span: list[str]) -> tuple[str, Fraction, Fraction, Fraction]:
    lo, hi = sorted((q(span[0]), q(span[1])))
    return axis, q(coordinate), lo, hi


def boundary_atoms(leaf: dict[str, Any]) -> list[dict[str, Any]]:
    box = leaf["closed_representative_box"]
    t0, t1, p0, p1 = box_key(box)
    return [
        {"kind": "FACE", "axis": "t", "coordinate": str(t0), "span": [str(p0), str(p1)], "side": "T_MINUS"},
        {"kind": "FACE", "axis": "t", "coordinate": str(t1), "span": [str(p0), str(p1)], "side": "T_PLUS"},
        {"kind": "FACE", "axis": "p", "coordinate": str(p0), "span": [str(t0), str(t1)], "side": "P_MINUS"},
        {"kind": "FACE", "axis": "p", "coordinate": str(p1), "span": [str(t0), str(t1)], "side": "P_PLUS"},
    ]


def corner_atoms(leaf: dict[str, Any]) -> list[dict[str, Any]]:
    t0, t1, p0, p1 = box_key(leaf["closed_representative_box"])
    return [{"kind": "CORNER", "t": str(t), "p": str(p), "corner": name} for t, p, name in ((t0,p0,"T0P0"),(t0,p1,"T0P1"),(t1,p0,"T1P0"),(t1,p1,"T1P1"))]


def prefix_free(paths: list[str]) -> bool:
    ordered = sorted(paths, key=lambda x: (len(x), x))
    return all(not later.startswith(first) for i, first in enumerate(ordered) for later in ordered[i+1:])


def build() -> dict[str, Any]:
    c35 = strict_json(C35 / "result.json")
    body = dict(c35); claim = body.pop("object_sha256")
    require(claim == OBJECT["C35"] and digest(body) == claim, "C35 object")
    c38, c39, c40, c41 = (validate_result(C38, "C38"), validate_result(C39, "C39"), validate_result(C40, "C40"), validate_result(C41, "C41"))
    require(file_sha(C56) == FILE["C56"], "C56 file")
    c56 = strict_json(C56); body = dict(c56); claim = body.pop("object_sha256")
    require(claim == OBJECT["C56"] and digest(body) == claim, "C56 object")
    singletons = read_ledger(C56_SINGLETONS, c56["ledgers"]["singletons"])
    require(tuple(sorted({x["reflection_pair"]["pair_index"] for x in singletons})) == PAIRS, "12 singleton pairs")

    c35_history = read_ledger(C35 / c35["ledgers"]["path_occurrences"]["filename"], c35["ledgers"]["path_occurrences"])[0]
    require(c35_history["collision_index"] == 1, "collision1 history")
    c38_children = read_ledger(C38 / c38["ledgers"]["collision1_2_child_pairs"]["filename"], c38["ledgers"]["collision1_2_child_pairs"])
    c38_parents = read_ledger(C38 / c38["ledgers"]["representative_parent_conservation"]["filename"], c38["ledgers"]["representative_parent_conservation"])
    c39_children = read_ledger(C39 / c39["ledgers"]["routed_child_pairs"]["filename"], c39["ledgers"]["routed_child_pairs"])
    c39_parents = read_ledger(C39 / c39["ledgers"]["parent_conservation"]["filename"], c39["ledgers"]["parent_conservation"])
    c40_leaves = read_ledger(C40 / c40["ledgers"]["routed_leaf_cells"]["filename"], c40["ledgers"]["routed_leaf_cells"])
    c40_parents = read_ledger(C40 / c40["ledgers"]["parent_conservation"]["filename"], c40["ledgers"]["parent_conservation"])
    c41_leaves = read_ledger(C41 / c41["ledgers"]["routed_ambient_cells"]["filename"], c41["ledgers"]["routed_ambient_cells"])
    c41_parents = read_ledger(C41 / c41["ledgers"]["parent_conservation"]["filename"], c41["ledgers"]["parent_conservation"])
    c41_faces = read_ledger(C41 / c41["ledgers"]["split_face_adjacency"]["filename"], c41["ledgers"]["split_face_adjacency"])
    c41_outers = read_ledger(C41 / c41["ledgers"]["c1_h1_surface_outers"]["filename"], c41["ledgers"]["c1_h1_surface_outers"])
    c41_boundaries = read_ledger(C41 / c41["ledgers"]["boundary_corner_outers"]["filename"], c41["ledgers"]["boundary_corner_outers"])

    by_pair = lambda rows: {row["pair_index"]: row for row in rows if row["pair_index"] in PAIRS}
    parents38, parents39, parents40, parents41 = map(by_pair, (c38_parents, c39_parents, c40_parents, c41_parents))
    require(all(len(x) == 12 for x in (parents38, parents39, parents40, parents41)), "parent joins")
    children38 = {row["row_sha256"]: row for row in c38_children if row["pair_index"] in PAIRS}
    children39 = {row["c38_child_row_sha256"]: row for row in c39_children if row["pair_index"] in PAIRS}
    leaves40 = {row["row_sha256"]: row for row in c40_leaves if row["pair_index"] in PAIRS}
    leaves41 = sorted((row for row in c41_leaves if row["pair_index"] in PAIRS), key=lambda r: (r["pair_index"], r["path"]))
    require(len(children38) == len(children39) == 164 and len(leaves40) == 299 and len(leaves41) == 781, "exact indexed coverage")
    outers = {(r["pair_index"], r["descendant_path"]): r for r in c41_outers if r["pair_index"] in PAIRS}
    boundaries = {(r["pair_index"], r["descendant_path"]): r for r in c41_boundaries if r["pair_index"] in PAIRS}
    split_rows = [r for r in c41_faces if r["pair_index"] in PAIRS]
    require(len(outers) == len(boundaries) == 319 and len(split_rows) == 482, "C41 lower strata coverage")

    # Compute exact global ownership from the closed leaf partition.
    face_incidence: dict[tuple[int, str, Fraction], list[tuple[Fraction, Fraction, str, str]]] = defaultdict(list)
    corner_incidence: dict[tuple[int, Fraction, Fraction], list[str]] = defaultdict(list)
    leaf_by_id: dict[str, dict[str, Any]] = {}
    for source in leaves41:
        leaf_id = source["c41_ambient_cell_id"]
        leaf_by_id[leaf_id] = source
        for atom in boundary_atoms(source):
            axis, coordinate, lo, hi = atom_key(atom["axis"], atom["coordinate"], atom["span"])
            face_incidence[(source["pair_index"], axis, coordinate)].append((lo, hi, source["path"], leaf_id))
        for atom in corner_atoms(source):
            corner_incidence[(source["pair_index"], q(atom["t"]), q(atom["p"]))].append(leaf_id)

    owner_writer = Writer(OUT / OWNER_FILE, "PAIR_INDEX_THEN_ATOM_KIND_THEN_EXACT_GEOMETRY")
    owner_hash_by_leaf: dict[str, list[str]] = defaultdict(list)
    face_hash_by_leaf: dict[str, list[str]] = defaultdict(list)
    corner_hash_by_leaf: dict[str, list[str]] = defaultdict(list)
    with owner_writer:
        for (pair, axis, coordinate), faces in sorted(face_incidence.items(), key=str):
            endpoints = sorted({value for lo, hi, _path, _leaf in faces for value in (lo, hi)})
            for lo, hi in zip(endpoints, endpoints[1:]):
                incident = [(path, leaf_id) for face_lo, face_hi, path, leaf_id in faces if face_lo <= lo and hi <= face_hi]
                if not incident:
                    continue
                incident_ids = sorted({x[1] for x in incident})
                owner = min(incident, key=lambda x: (x[0], x[1]))[1]
                row = {"schema": SCHEMA + ".owner-row", "pair_index": pair, "atom_kind": "FACE", "axis": axis, "coordinate": str(coordinate), "span": [str(lo), str(hi)], "incident_leaf_ids": incident_ids, "incident_leaf_count": len(incident_ids), "owner_rule": "LEXICOGRAPHIC_MINIMUM_PATH_THEN_LEAF_ID", "owner_leaf_id": owner, "owner_unique": True, "owner_credit": 0, "D02_gate_credit": 0}
                closed = owner_writer.write(row)
                for leaf_id in incident_ids:
                    owner_hash_by_leaf[leaf_id].append(closed["row_sha256"])
                    face_hash_by_leaf[leaf_id].append(closed["row_sha256"])
        for (pair, t, p), incident in sorted(corner_incidence.items(), key=str):
            incident_ids = sorted(set(incident))
            owner = min(incident_ids, key=lambda leaf_id: (leaf_by_id[leaf_id]["path"], leaf_id))
            row = {"schema": SCHEMA + ".owner-row", "pair_index": pair, "atom_kind": "CORNER", "t": str(t), "p": str(p), "incident_leaf_ids": incident_ids, "incident_leaf_count": len(incident_ids), "owner_rule": "LEXICOGRAPHIC_MINIMUM_PATH_THEN_LEAF_ID", "owner_leaf_id": owner, "owner_unique": True, "owner_credit": 0, "D02_gate_credit": 0}
            closed = owner_writer.write(row)
            for leaf_id in incident_ids:
                owner_hash_by_leaf[leaf_id].append(closed["row_sha256"])
                corner_hash_by_leaf[leaf_id].append(closed["row_sha256"])

    leaf_writer = Writer(OUT / LEAF_FILE, "PAIR_INDEX_THEN_PATH")
    terminal = handoffs = 0
    leaf_rows_by_pair: dict[int, list[dict[str, Any]]] = defaultdict(list)
    with leaf_writer:
        for source in leaves41:
            pair, path = source["pair_index"], source["path"]
            c40_source = leaves40[source["c40_source_row_sha256"]]
            c38_source = children38[c40_source["c38_source_row_sha256"]]
            c39_source = children39[c40_source["c38_source_row_sha256"]]
            require(c39_source["row_sha256"] == c40_source["c39_source_row_sha256"], "C38-C39-C40 leaf chain")
            require(c38_source["representative_cell_id"] == source["representative_cell_id"] and c38_source["reflected_cell_id"] == source["reflected_cell_id"], "cell chain")
            is_terminal = source["disposition_family"] == "TERMINAL_EXCLUDED"
            if is_terminal:
                terminal += 1
                disposition = "STRICT_TERMINAL"
                terminal_class = "EARLIEST_PREFIX_EXCLUDED"
                handoff = None
            else:
                require(source["disposition_family"] == "RESIDUAL_OUTER" and (pair, path) in outers and (pair, path) in boundaries, "nonterminal outer bindings")
                handoffs += 1
                disposition = "COLLISION2_HANDOFF"
                terminal_class = None
                outer = outers[(pair, path)]
                boundary = boundaries[(pair, path)]
                handoff = {"next_collision_index": 2, "collision1_history_row_sha256": c35_history["row_sha256"], "collision1_original_owner": c35_history["selected_absolute_owner_id"], "collision1_event_order": {"official_word_key_id": c35_history["official_word_key_id"], "official_word_variant_id": c35_history["official_word_variant_id"], "incoming_chart": c35_history["incoming_chart"], "outgoing_chart": c35_history["outgoing_chart"]}, "exact_representative_box": source["closed_representative_box"], "exact_reflected_box": source["closed_reflected_box"], "C41_outer_row_sha256": outer["row_sha256"], "C41_boundary_corner_row_sha256": boundary["row_sha256"], "residual_classification": source["residual_classification"], "normalized_surface_ids": [x["normalized_surface_id"] for x in outer["normalized_surfaces"]], "face_owner_rows_complete": True, "corner_owner_rows_complete": True, "handoff_credit": 0}
                handoff["handoff_object_sha256"] = digest(handoff)
            leaf_id = source["c41_ambient_cell_id"]
            require(len(corner_hash_by_leaf[leaf_id]) == 4 and len(face_hash_by_leaf[leaf_id]) >= 4, "leaf atomic owner coverage")
            row = {"schema": SCHEMA + ".leaf-row", "pair_index": pair, "path": path, "parent_volume_fraction": source["parent_volume_fraction"], "representative_cell_id": source["representative_cell_id"], "reflected_cell_id": source["reflected_cell_id"], "exact_representative_box": source["closed_representative_box"], "exact_reflected_box": source["closed_reflected_box"], "C38_child_row_sha256": c38_source["row_sha256"], "C39_routed_row_sha256": c39_source["row_sha256"], "C40_leaf_row_sha256": c40_source["row_sha256"], "C41_ambient_row_sha256": source["row_sha256"], "face_corner_owner_row_sha256s": sorted(owner_hash_by_leaf[leaf_id]), "face_owner_count": len(face_hash_by_leaf[leaf_id]), "corner_owner_count": len(corner_hash_by_leaf[leaf_id]), "owner_rows_complete": True, "event_order_bound_to_C35_collision1": True, "leaf_disposition": disposition, "strict_terminal_class": terminal_class, "collision2_handoff": handoff, "local_terminal_credit": 1 if is_terminal else 0, "whole_parent_credit": 0, "D02_gate_credit": 0}
            leaf_rows_by_pair[pair].append(leaf_writer.write(row))

    parent_writer = Writer(OUT / PARENT_FILE, "PAIR_INDEX_ASCENDING")
    whole_closed = 0
    with parent_writer:
        for pair in PAIRS:
            rows = leaf_rows_by_pair[pair]
            paths = [r["path"] for r in rows]
            kraft = sum(Fraction(r["parent_volume_fraction"]) for r in rows)
            require(prefix_free(paths) and kraft == 1, f"prefix/Kraft:{pair}")
            terminal_count = sum(r["leaf_disposition"] == "STRICT_TERMINAL" for r in rows)
            handoff_count = len(rows) - terminal_count
            whole = handoff_count == 0
            whole_closed += int(whole)
            row = {"schema": SCHEMA + ".parent-row", "pair_index": pair, "representative_cell_id": parents38[pair]["representative_cell_id"], "reflected_cell_id": parents38[pair]["reflected_cell_id"], "C38_parent_row_sha256": parents38[pair]["row_sha256"], "C39_parent_row_sha256": parents39[pair]["row_sha256"], "C40_parent_row_sha256": parents40[pair]["row_sha256"], "C41_parent_row_sha256": parents41[pair]["row_sha256"], "leaf_count": len(rows), "terminal_leaf_count": terminal_count, "collision2_handoff_leaf_count": handoff_count, "path_prefix_free": True, "parent_Kraft_conservation": "1", "face_corner_owner_complete": True, "collision1_event_order_complete": True, "whole_representative_parent_terminal": whole, "whole_reflected_parent_terminal": whole, "whole_pair_credit": 0, "D02_gate_credit": 0}
            parent_writer.write(row)

    require(terminal == 462 and handoffs == 319 and whole_closed == 0, "strict expected census")
    result: dict[str, Any] = {"schema": SCHEMA, "status": "PASS_COLLISION1_COMMON_REFINEMENT__12_PAIRS_24_SINGLETONS__781_LEAVES__462_TERMINAL__319_EXACT_COLLISION2_HANDOFFS__ZERO_WHOLE_CLOSED", "authority_objects": {"C35": OBJECT["C35"], "C38": OBJECT["C38"], "C39": OBJECT["C39"], "C40": OBJECT["C40"], "C41": OBJECT["C41"], "C56s": OBJECT["C56"]}, "coverage": {"singleton_cells": 24, "reflection_pairs": 12, "C38_child_rows": 164, "C39_routed_rows": 164, "C40_leaf_rows": 299, "C41_leaf_rows": 781, "C41_terminal_rows": 462, "C41_residual_outer_rows": 319, "C41_split_face_rows": len(split_rows)}, "ledgers": {"leaves": leaf_writer.descriptor(), "face_corner_owners": owner_writer.descriptor(), "parents": parent_writer.descriptor()}, "terminal_census": {"strict_terminal_leaves": terminal, "exact_collision2_handoff_leaves": handoffs, "whole_pairs_closed": whole_closed, "whole_singletons_closed": whole_closed * 2, "whole_singletons_remaining": 24}, "invariants": {"all_12_parent_path_sets_prefix_free": True, "all_12_parent_Kraft_sums_equal_one": True, "all_leaf_face_owner_rows_complete": True, "all_leaf_corner_owner_rows_complete": True, "all_nonterminal_leaves_have_exact_collision2_handoff": True, "collision1_history_and_event_order_bound": True}, "strict_nonpromotion": {"C41_partial_outers_promoted_to_terminal": False, "whole_parent_credit": 0, "formal_credit": 0, "D02_gate_credit": 0, "runtime_writes_performed": False, "canonical_writes_performed": False}, "required_next": "consume the 319 sealed collision2 handoffs with a dimension-complete collision2 decider; do not infer whole-cell closure from partial terminal volume"}
    result["object_sha256"] = digest(result)
    (OUT / RESULT_FILE).write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--build", action="store_true"); args = parser.parse_args(); require(args.build, "use --build")
    result = build(); print(json.dumps({"status": result["status"], "object_sha256": result["object_sha256"], "ledgers": result["ledgers"]}, sort_keys=True, separators=(",", ":"))); return 0


if __name__ == "__main__":
    try: raise SystemExit(main())
    except FailClosed as error: print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)}, sort_keys=True, separators=(",", ":"))); raise SystemExit(1)
