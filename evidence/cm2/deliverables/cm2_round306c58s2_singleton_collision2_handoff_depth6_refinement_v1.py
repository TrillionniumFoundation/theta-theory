#!/usr/bin/env python3
"""C58s2: exact depth-six continuation of the 319 C57s1 C2 handoffs.

Every frozen C57s1 handoff is replayed on its exact C41 box through the pinned
C38--C41 strict router.  Residual leaves are bisected by the router's exact
longest-axis rule up to six further levels.  Leaves are emitted only as strict
exclusions, genuine collision-three-ready rows, or exact still-collision-two
handoffs.  In particular, C1 equality carriers are never relabelled C3-ready.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


SELF = Path(__file__).resolve()
ROOT = SELF.parent.parent
OUT = SELF.parent
sys.path.insert(0, str(OUT))

import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41  # noqa: E402


BASE = "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement"
SCHEMA = "cm2.round306c58s2.singleton-collision2-handoff-depth6-refinement.v1"
MAX_ADDITIONAL_DEPTH = 6
PAIRS = (31, 188, 200, 270, 321, 410, 471, 474, 631, 711, 787, 853)

C57_BASE = "cm2_round306c57s1_singleton_collision1_common_refinement"
C57_RESULT = OUT / (C57_BASE + "_result_v1.json")
C57_LEAVES = OUT / (C57_BASE + "_leaf_ledger_v1.jsonl.gz")
C57_OWNERS = OUT / (C57_BASE + "_face_corner_owner_ledger_v1.jsonl.gz")
C57_PARENTS = OUT / (C57_BASE + "_parent_ledger_v1.jsonl.gz")
C57_MANIFEST = OUT / (C57_BASE + "_manifest_v1.sha256")
C57A_AUDIT = OUT / "cm2_round306c57a_singleton_collision1_candidate_independent_audit_v1.json"
C57A_MANIFEST = OUT / "cm2_round306c57a_singleton_collision1_candidate_independent_manifest_v1.sha256"
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"

LEAF_FILE = BASE + "_leaf_ledger_v1.jsonl.gz"
OWNER_FILE = BASE + "_face_corner_owner_ledger_v1.jsonl.gz"
HANDOFF_FILE = BASE + "_handoff_summary_v1.jsonl.gz"
PARENT_FILE = BASE + "_parent_summary_v1.jsonl.gz"
RESULT_FILE = BASE + "_result_v1.json"

PIN = {
    "C57_result_file": "9881c22ac4a8630b90b8eb16d81c1670bb6f544e5f4666197d0e6047771d8c4c",
    "C57_result_object": "8cda7681bcbe93c065f1f336842e9fffa6bd3ea67268e96d95fcb3d1f8cbbb58",
    "C57_leaf_file": "918899a914ad4fbb05c1095cac9f42f6c46d02f0acdad366538a395021aeaee6",
    "C57_owner_file": "72d4dd688378166bfd8dbf9ded56ef091014803f80777ea21847a831b4c3f884",
    "C57_parent_file": "8817069967798042bd87315f57e7c3cea279c6564c0e50a5ac927ca4f765e510",
    "C57_manifest_file": "4427e1376811454ad3b6ec5478c1687064cea81f5d33ebd0c13284952928ced0",
    "C57_verify_object": "cec8d9bbe3345552b7cb1734c84ed3c1026dc02276780cb6fca9f502118953d6",
    "C57a_audit_file": "9fdbb28605e81de75949486416851f4d2bb233c4953650fcbadd024c12dccbdc",
    "C57a_audit_object": "f7984162bdb64c7cbb828e9d3733103637898007c91c89292b64717145b818c0",
    "C57a_manifest_file": "669377fd362a5c66dd36c75d27685c2f76a0e5661c400dd99494455940d15db5",
    "C40_object": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
}


class FailClosed(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if not value:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        answer: dict[str, Any] = {}
        for key, value in items:
            need(key not in answer, "duplicate key:" + key)
            answer[key] = value
        return answer
    value = json.loads(path.read_text(), object_pairs_hook=hook)
    need(isinstance(value, dict), "JSON object:" + str(path))
    return value


def closed_object(path: Path, file_pin: str, object_pin: str) -> dict[str, Any]:
    need(file_sha(path) == file_pin, "file pin:" + path.name)
    value = strict_json(path)
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == object_pin and digest(body) == object_pin, "object pin:" + path.name)
    return value


def read_rows(path: Path, descriptor: dict[str, Any], pin: str) -> list[dict[str, Any]]:
    need(file_sha(path) == descriptor["sha256"] == pin, "ledger pin:" + path.name)
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            body = copy.deepcopy(row)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and digest(body) == claim, "row closure:" + path.name)
            sequence.update((claim + "\n").encode("ascii"))
            rows.append(row)
    need(len(rows) == descriptor["row_count"] and
         sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         "ledger descriptor:" + path.name)
    return rows


class Writer:
    def __init__(self, path: Path, order: str):
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.stream: Any = None

    def __enter__(self) -> "Writer":
        need(not self.path.exists(), "no-replace:" + self.path.name)
        self.raw = self.path.open("xb")
        self.stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, row: dict[str, Any]) -> dict[str, Any]:
        claim = digest(row)
        closed = {**row, "row_sha256": claim}
        self.stream.write(canonical(closed) + b"\n")
        self.sequence.update((claim + "\n").encode("ascii"))
        self.count += 1
        return closed

    def __exit__(self, *_args: Any) -> None:
        self.stream.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name, "order": self.order, "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha(self.path), "size": self.path.stat().st_size,
        }


def q(value: Any) -> Fraction:
    return Fraction(str(value))


def box_key(box: dict[str, Any]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return q(box["t"][0]), q(box["t"][1]), q(box["p"][0]), q(box["p"][1])


def prefix_free(paths: list[str]) -> bool:
    ordered = sorted(paths, key=lambda value: (len(value), value))
    return all(not later.startswith(first) for index, first in enumerate(ordered)
               for later in ordered[index + 1:])


def frozen_context() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    result = closed_object(C57_RESULT, PIN["C57_result_file"], PIN["C57_result_object"])
    need(file_sha(C57_MANIFEST) == PIN["C57_manifest_file"], "C57 final manifest")
    need(file_sha(C57A_MANIFEST) == PIN["C57a_manifest_file"], "C57a final manifest")
    c57a = closed_object(C57A_AUDIT, PIN["C57a_audit_file"], PIN["C57a_audit_object"])
    need(c57a["status"].startswith("PASS_INDEPENDENT_C57S1_") and
         c57a["candidate_is_authority"] is False, "C57a audit status")
    leaves = read_rows(C57_LEAVES, result["ledgers"]["leaves"], PIN["C57_leaf_file"])
    owners = read_rows(C57_OWNERS, result["ledgers"]["face_corner_owners"], PIN["C57_owner_file"])
    parents = read_rows(C57_PARENTS, result["ledgers"]["parents"], PIN["C57_parent_file"])
    need((len(leaves), len(owners), len(parents)) == (781, 3141, 12), "C57 frozen census")
    return result, leaves, parents, c57a


def build() -> dict[str, Any]:
    c57_result, c57_leaves, c57_parents, c57a = frozen_context()
    context = c41.load_context(C40, None, formal=False)
    need(context["result"]["object_sha256"] == PIN["C40_object"], "C40 context object")
    c41.install_complete_immutable_cache()
    config = c41.decode_worker_config(context["config"])

    c40_result = context["result"]
    c40_rows = c41.c38.read_ledger(C40, c40_result["ledgers"]["routed_leaf_cells"])
    sources = {row["row_sha256"]: (ordinal, row) for ordinal, row in enumerate(c40_rows)}
    need(len(sources) == 35009, "C40 source uniqueness")

    selected = [row for row in c57_leaves if row["leaf_disposition"] == "COLLISION2_HANDOFF"]
    carried_terminal = [row for row in c57_leaves if row["leaf_disposition"] == "STRICT_TERMINAL"]
    need(len(selected) == 319 and len(carried_terminal) == 462, "C57 selected census")
    need(len({row["C40_leaf_row_sha256"] for row in selected}) == 97, "97 C40 source rows")

    route_cache: dict[tuple[str, str], dict[str, Any]] = {}
    route_evaluations = 0
    leaves_by_handoff: dict[str, list[dict[str, Any]]] = {}
    all_open_rows: list[dict[str, Any]] = []
    handoff_summaries: list[dict[str, Any]] = []
    raw_census: dict[str, int] = {}
    disposition_census = {"STRICT_TERMINAL": 0, "COLLISION3_READY": 0, "COLLISION2_HANDOFF": 0}

    for ordinal, source_handoff in enumerate(selected):
        c57_handoff = source_handoff["collision2_handoff"]
        source_ordinal, source = sources[source_handoff["C40_leaf_row_sha256"]]
        task = c41.task_for_row(source_ordinal, source, context)
        key = source_handoff["row_sha256"]
        stack: list[tuple[str, int, Fraction, str | None]] = [
            (source_handoff["path"], 0, q(source_handoff["parent_volume_fraction"]), None)
        ]
        final_rows: list[dict[str, Any]] = []
        while stack:
            path, depth, volume, parent_path = stack.pop()
            cache_key = (source["row_sha256"], path)
            route = route_cache.get(cache_key)
            if route is None:
                route = c41.route_at_path(task, path, config)
                route_cache[cache_key] = route
                route_evaluations += 1
            need(c41.box_payload(route["box"]) is not None, "rational route box")
            family = c41.disposition_family(route["classification"])
            if family == "RESIDUAL_OUTER" and depth < MAX_ADDITIONAL_DEPTH:
                stack.append((path + "1", depth + 1, volume / 2, path))
                stack.append((path + "0", depth + 1, volume / 2, path))
                continue
            if family == "TERMINAL_EXCLUDED":
                disposition = "STRICT_TERMINAL"
                strict_class = "EARLIEST_PREFIX_EXCLUDED"
                next_handoff = None
                c3_ready = None
            elif family == "COLLISION3_READY":
                disposition = "COLLISION3_READY"
                strict_class = None
                next_handoff = None
                c3_ready = {
                    "next_collision_index": 3,
                    "route_classification": route["classification"],
                    "route_witness": route["witness"],
                    "exact_representative_box": c41.box_payload(route["box"]),
                    "exact_reflected_box": c41.reflected_box(
                        task["c38_source"]["representative_origin_key"], route["box"]),
                    "collision3_ready_credit": 0,
                }
                c3_ready["collision3_ready_object_sha256"] = digest(c3_ready)
            else:
                disposition = "COLLISION2_HANDOFF"
                strict_class = None
                c3_ready = None
                residual = c41.residual_classification(route["classification"])
                next_handoff = {
                    "next_collision_index": 2,
                    "prior_C57_leaf_row_sha256": source_handoff["row_sha256"],
                    "prior_C57_handoff_object_sha256": c57_handoff["handoff_object_sha256"],
                    "collision1_history_row_sha256": c57_handoff["collision1_history_row_sha256"],
                    "collision1_original_owner": c57_handoff["collision1_original_owner"],
                    "collision1_event_order": c57_handoff["collision1_event_order"],
                    "exact_representative_box": c41.box_payload(route["box"]),
                    "exact_reflected_box": c41.reflected_box(
                        task["c38_source"]["representative_origin_key"], route["box"]),
                    "route_classification": route["classification"],
                    "route_witness": route["witness"],
                    "route_method": route["route_method"],
                    "residual_classification": residual,
                    "c2_status": route["c2_status"],
                    "c2_baseline": route["c2_baseline"],
                    "handoff_credit": 0,
                }
                next_handoff["handoff_object_sha256"] = digest(next_handoff)
            raw_census[route["classification"]] = raw_census.get(route["classification"], 0) + 1
            disposition_census[disposition] += 1
            open_row = {
                "schema": SCHEMA + ".leaf-row",
                "source_handoff_ordinal": ordinal,
                "source_C57_leaf_row_sha256": source_handoff["row_sha256"],
                "source_C57_handoff_object_sha256": c57_handoff["handoff_object_sha256"],
                "pair_index": source_handoff["pair_index"],
                "path": path,
                "additional_depth": depth,
                "parent_path": parent_path,
                "parent_volume_fraction": str(volume),
                "representative_cell_id": source_handoff["representative_cell_id"],
                "reflected_cell_id": source_handoff["reflected_cell_id"],
                "exact_representative_box": c41.box_payload(route["box"]),
                "exact_reflected_box": c41.reflected_box(
                    task["c38_source"]["representative_origin_key"], route["box"]),
                "C40_source_row_sha256": source["row_sha256"],
                "route_classification": route["classification"],
                "route_witness": route["witness"],
                "route_method": route["route_method"],
                "disposition": disposition,
                "strict_terminal_class": strict_class,
                "collision2_handoff": next_handoff,
                "collision3_ready": c3_ready,
                "face_corner_owner_row_sha256s": [],
                "face_owner_count": 0,
                "corner_owner_count": 0,
                "owner_rows_complete": False,
                "local_terminal_credit": 1 if disposition == "STRICT_TERMINAL" else 0,
                "collision3_ready_credit": 0,
                "whole_parent_credit": 0,
                "D02_gate_credit": 0,
            }
            final_rows.append(open_row)
            all_open_rows.append(open_row)
        final_rows.sort(key=lambda row: row["path"])
        paths = [row["path"] for row in final_rows]
        need(prefix_free(paths) and sum(q(row["parent_volume_fraction"]) for row in final_rows) ==
             q(source_handoff["parent_volume_fraction"]), "handoff prefix/Kraft")
        leaves_by_handoff[key] = final_rows

    # Atomize the final exact leaf boundaries at every rational endpoint.
    line_segments: dict[tuple[int, str, Fraction], list[tuple[Fraction, Fraction, str]]] = {}
    corners: dict[tuple[int, Fraction, Fraction], set[str]] = {}
    row_id: dict[int, str] = {}
    path_by_id: dict[str, str] = {}
    row_by_id: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(all_open_rows):
        leaf_id = "c58s2-leaf:" + digest({"source": row["source_C57_leaf_row_sha256"], "path": row["path"]})
        row_id[id(row)] = leaf_id
        path_by_id[leaf_id] = row["path"]
        row_by_id[leaf_id] = row
        t0, t1, p0, p1 = box_key(row["exact_representative_box"])
        for axis, coordinate, low, high in (("t", t0, p0, p1), ("t", t1, p0, p1),
                                            ("p", p0, t0, t1), ("p", p1, t0, t1)):
            line_segments.setdefault((row["pair_index"], axis, coordinate), []).append((low, high, leaf_id))
        for t in (t0, t1):
            for p in (p0, p1):
                corners.setdefault((row["pair_index"], t, p), set()).add(leaf_id)

    owner_refs: dict[str, list[str]] = {leaf_id: [] for leaf_id in row_by_id}
    face_refs: dict[str, list[str]] = {leaf_id: [] for leaf_id in row_by_id}
    corner_refs: dict[str, list[str]] = {leaf_id: [] for leaf_id in row_by_id}
    owner_writer = Writer(OUT / OWNER_FILE, "PAIR_THEN_ATOMIZED_EXACT_GEOMETRY")
    with owner_writer:
        for (pair, axis, coordinate), segments in sorted(line_segments.items(), key=str):
            endpoints = sorted({point for low, high, _leaf in segments for point in (low, high)})
            for low, high in zip(endpoints, endpoints[1:]):
                incident = sorted({leaf_id for start, stop, leaf_id in segments if start <= low and high <= stop})
                if not incident:
                    continue
                owner = min(incident, key=lambda leaf_id: (path_by_id[leaf_id], leaf_id))
                closed = owner_writer.write({
                    "schema": SCHEMA + ".owner-row", "pair_index": pair, "atom_kind": "FACE",
                    "axis": axis, "coordinate": str(coordinate), "span": [str(low), str(high)],
                    "incident_leaf_ids": incident, "incident_leaf_count": len(incident),
                    "owner_rule": "LEXICOGRAPHIC_MINIMUM_PATH_THEN_LEAF_ID",
                    "owner_leaf_id": owner, "owner_unique": True,
                    "owner_credit": 0, "D02_gate_credit": 0,
                })
                for leaf_id in incident:
                    owner_refs[leaf_id].append(closed["row_sha256"])
                    face_refs[leaf_id].append(closed["row_sha256"])
        for (pair, t, p), incident_set in sorted(corners.items(), key=str):
            incident = sorted(incident_set)
            owner = min(incident, key=lambda leaf_id: (path_by_id[leaf_id], leaf_id))
            closed = owner_writer.write({
                "schema": SCHEMA + ".owner-row", "pair_index": pair, "atom_kind": "CORNER",
                "t": str(t), "p": str(p), "incident_leaf_ids": incident,
                "incident_leaf_count": len(incident),
                "owner_rule": "LEXICOGRAPHIC_MINIMUM_PATH_THEN_LEAF_ID",
                "owner_leaf_id": owner, "owner_unique": True,
                "owner_credit": 0, "D02_gate_credit": 0,
            })
            for leaf_id in incident:
                owner_refs[leaf_id].append(closed["row_sha256"])
                corner_refs[leaf_id].append(closed["row_sha256"])

    leaf_writer = Writer(OUT / LEAF_FILE, "SOURCE_HANDOFF_ORDINAL_THEN_PATH")
    closed_by_source: dict[str, list[dict[str, Any]]] = {}
    with leaf_writer:
        for row in sorted(all_open_rows, key=lambda item: (item["source_handoff_ordinal"], item["path"])):
            leaf_id = row_id[id(row)]
            need(len(face_refs[leaf_id]) >= 4 and len(corner_refs[leaf_id]) == 4, "owner completeness")
            row["face_corner_owner_row_sha256s"] = sorted(owner_refs[leaf_id])
            row["face_owner_count"] = len(face_refs[leaf_id])
            row["corner_owner_count"] = len(corner_refs[leaf_id])
            row["owner_rows_complete"] = True
            row["leaf_id"] = leaf_id
            closed = leaf_writer.write(row)
            closed_by_source.setdefault(row["source_C57_leaf_row_sha256"], []).append(closed)

    handoff_writer = Writer(OUT / HANDOFF_FILE, "SOURCE_HANDOFF_ORDINAL_ASCENDING")
    whole_handoffs_terminal = 0
    whole_handoffs_c3_or_terminal = 0
    with handoff_writer:
        for ordinal, source_handoff in enumerate(selected):
            rows = closed_by_source[source_handoff["row_sha256"]]
            paths = [row["path"] for row in rows]
            kraft = sum(q(row["parent_volume_fraction"]) for row in rows)
            terminal_count = sum(row["disposition"] == "STRICT_TERMINAL" for row in rows)
            c3_count = sum(row["disposition"] == "COLLISION3_READY" for row in rows)
            residual_count = len(rows) - terminal_count - c3_count
            whole_terminal = terminal_count == len(rows)
            whole_c3 = residual_count == 0
            whole_handoffs_terminal += int(whole_terminal)
            whole_handoffs_c3_or_terminal += int(whole_c3)
            need(prefix_free(paths) and kraft == q(source_handoff["parent_volume_fraction"]),
                 "closed handoff Kraft")
            handoff_writer.write({
                "schema": SCHEMA + ".handoff-summary-row", "source_handoff_ordinal": ordinal,
                "source_C57_leaf_row_sha256": source_handoff["row_sha256"],
                "pair_index": source_handoff["pair_index"], "source_path": source_handoff["path"],
                "source_parent_volume_fraction": source_handoff["parent_volume_fraction"],
                "refined_leaf_count": len(rows), "strict_terminal_leaf_count": terminal_count,
                "collision3_ready_leaf_count": c3_count, "collision2_handoff_leaf_count": residual_count,
                "path_prefix_free": True, "Kraft_conservation": source_handoff["parent_volume_fraction"],
                "whole_source_handoff_terminal": whole_terminal,
                "whole_source_handoff_terminal_or_collision3_ready": whole_c3,
                "whole_handoff_credit": 0, "D02_gate_credit": 0,
            })

    # Parent summaries combine the 462 carried terminals and the refined 319 leaves.
    c57_by_pair: dict[int, list[dict[str, Any]]] = {pair: [] for pair in PAIRS}
    for row in carried_terminal:
        c57_by_pair[row["pair_index"]].append(row)
    for source, rows in closed_by_source.items():
        pair = rows[0]["pair_index"]
        c57_by_pair[pair].extend(rows)
    parent_writer = Writer(OUT / PARENT_FILE, "PAIR_INDEX_ASCENDING")
    whole_pairs_closed = 0
    with parent_writer:
        for pair in PAIRS:
            rows = c57_by_pair[pair]
            paths = [row["path"] for row in rows]
            kraft = sum(q(row["parent_volume_fraction"]) for row in rows)
            residual = sum(row.get("disposition") == "COLLISION2_HANDOFF" for row in rows)
            c3 = sum(row.get("disposition") == "COLLISION3_READY" for row in rows)
            terminal = len(rows) - residual - c3
            whole = residual == 0 and c3 == 0
            whole_pairs_closed += int(whole)
            need(prefix_free(paths) and kraft == 1, "parent combined prefix/Kraft")
            parent_writer.write({
                "schema": SCHEMA + ".parent-summary-row", "pair_index": pair,
                "combined_leaf_count": len(rows), "strict_terminal_leaf_count": terminal,
                "collision3_ready_leaf_count": c3, "collision2_handoff_leaf_count": residual,
                "path_prefix_free": True, "parent_Kraft_conservation": "1",
                "whole_representative_parent_terminal": whole,
                "whole_reflected_parent_terminal": whole,
                "whole_pair_credit": 0, "D02_gate_credit": 0,
            })

    need(route_evaluations == 10777, "deterministic route-evaluation count")
    need(disposition_census == {"STRICT_TERMINAL": 2949, "COLLISION3_READY": 0,
                                "COLLISION2_HANDOFF": 2599}, "depth-six disposition census")
    need(whole_handoffs_terminal == 38 and whole_handoffs_c3_or_terminal == 38,
         "depth-six whole handoff census")
    need(whole_pairs_closed == 0, "no whole singleton pair closure")
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PASS_EXACT_DEPTH6_CONTINUATION__319_INPUT_HANDOFFS__5548_LEAVES__2949_TERMINAL__0_C3_READY__2599_EXACT_C2_HANDOFFS__ZERO_WHOLE_SINGLETON_CLOSED",
        "frozen_inputs": {
            "C57_result_object_sha256": PIN["C57_result_object"],
            "C57_result_file_sha256": PIN["C57_result_file"],
            "C57_leaf_file_sha256": PIN["C57_leaf_file"],
            "C57_owner_file_sha256": PIN["C57_owner_file"],
            "C57_parent_file_sha256": PIN["C57_parent_file"],
            "C57_manifest_sha256": PIN["C57_manifest_file"],
            "C57_independent_verification_object_sha256": PIN["C57_verify_object"],
            "C57a_audit_object_sha256": c57a["object_sha256"],
            "C57a_manifest_sha256": PIN["C57a_manifest_file"],
            "C40_object_sha256": PIN["C40_object"],
        },
        "routing": {
            "maximum_additional_dyadic_depth": MAX_ADDITIONAL_DEPTH,
            "exact_route_evaluations": route_evaluations,
            "input_C57_handoffs": 319, "unique_C40_source_rows": 97,
            "refined_leaf_count": len(all_open_rows),
            "raw_classification_census": dict(sorted(raw_census.items())),
            "disposition_census": disposition_census,
            "whole_input_handoffs_terminal": whole_handoffs_terminal,
            "whole_input_handoffs_terminal_or_collision3_ready": whole_handoffs_c3_or_terminal,
        },
        "ledgers": {
            "leaves": leaf_writer.descriptor(), "face_corner_owners": owner_writer.descriptor(),
            "handoff_summaries": handoff_writer.descriptor(), "parent_summaries": parent_writer.descriptor(),
        },
        "strict_boundary": {
            "C1_equality_carriers_relabelled_C3_ready": False,
            "unrelated_C40_C2_rows_imported": False,
            "whole_pairs_closed": whole_pairs_closed, "whole_singletons_closed": 0,
            "whole_singletons_remaining": 24, "formal_credit": 0,
            "whole_parent_credit": 0, "D02_gate_credit": 0,
            "runtime_writes_performed": False, "canonical_writes_performed": False,
        },
        "required_next": "continue the 2599 exact collision-two handoffs with an equality-carrier-aware strict decider; no C3-ready credit exists in this checkpoint",
    }
    result["object_sha256"] = digest(result)
    path = OUT / RESULT_FILE
    need(not path.exists(), "result no-replace")
    path.write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    need(args.build, "use --build")
    result = build()
    print(json.dumps({"status": result["status"], "object_sha256": result["object_sha256"],
                      "ledgers": result["ledgers"]}, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FailClosed as error:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(error)},
                         sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
