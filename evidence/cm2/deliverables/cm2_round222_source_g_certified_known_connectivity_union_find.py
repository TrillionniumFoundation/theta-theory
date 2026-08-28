#!/usr/bin/env python3
"""Formal outcome-blind source-G known-connectivity lower-bound quotient.

Only the Round214 safe same-occurrence carriers and the exact TRACE glues
materialized by Round217/Round219 are union edges.  Round219 ABSENT or
UNRESOLVED rows and every Round220 coordinate adjacency remain non-edges.
The resulting blocks are not claimed to be maximal physical components.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import gc
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable

import cm2_round214_source_g_physical_component_join_dedup_feasibility_probe as r214


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round222_source_g_certified_known_connectivity_union_find"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round222.source-g-certified-known-connectivity-union-find.v1"
STATUS = (
    "CERTIFIED_KNOWN_CONNECTIVITY_LOWER_BOUND__"
    "NOT_MAXIMAL_PHYSICAL_COMPONENTS__ZERO_PROMOTION"
)
MAX_INPUT_BYTES = 800 * 1024 * 1024
SOURCE_G_KEYS = 224_580

R211 = "cm2_round211_source_g_outgoing_half_open_owner_materialization"
R216 = "cm2_round216_source_g_global_key_occurrence_exhaustion_frontier"
R217 = "cm2_round217_source_g_internal_face_trace_glue_materialization"
R219 = "cm2_round219_source_g_partial_face_common_refinement_glue"
R220 = "cm2_round220_source_g_round179_resolved_child_boundary_atlas"
MANIFESTS = {
    R211: ("c0cf8b70de6dd147fd1009c97d28549ec4571f9d6c82b8bf46dba023e3fe943c", 6),
    R216: ("54f9f270a6bad485691fa1db12a46052fcd91615b01461ce40ad55b66475b58b", 6),
    R217: ("2b6df0e791e62743ee7a27e8556292166f07d8873a41e8de854b27787981b8c5", 6),
    R219: ("67470c6f9503bc5707135901a878fefc7086ac33caae4b578280dd0e6b5c2b9f", 6),
    R220: ("f6c4f748ca3a98fd214342d264006b5c2e71755174daf686556ff4926160c385", 6),
}
RESULTS = {
    R211: "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b",
    R216: "267a4b9aaaab6a576e1c1866cc2fa0b9dc9bf4fc6a3b08a210ed3821e45dd658",
    R217: "fb4519a43f76cbc765e24b3cb0a0e25267d9664091e22139913f3899fd1e2286",
    R219: "f8d46a9a220b6b7e0e6f86430ad6d537d5358cd610f064417ab3e8b4c125744e",
    f"{R220}_verification":
        "d753d748b344205ecdaa611b37b4adcc82868c82cf1ea008c92ba88688330ed6",
}
R214_SOURCE_SHA256 = "d074aa045637ce1bb31768fa551bdb73ceda6a58c760cafe3dbf92faa7c922fe"
R214_REPORT_SHA256 = "aa48c012fa8c57df89b2bea4123467fc2c74821a03525095976cb61c709fe952"
R214_RESULT_SHA256 = "ddc12c8e625a5a65cc8e445d97ee89e64429a6c729efe32778a092f7e6521d09"
R214_SHEET_HASH = "7a679aca24e025463e0739485e2b0b5f6b4b11746d343f91b0743060623f56f8"
R214_CURVE_HASH = "388cf14fb2103fe8149411fb37de9ee0be7618c73831e22d805d87f7cd74f891"
R214_ENDPOINT_HASH = "e810a52cd88248490d60ebc0f6715a87c7aed78bfd816c765fd905e7dbf19cc5"


class Round222Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round222Error(label)


ENCODER = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode()


def canonical_bytes(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


def make_id(label: str, value: Any) -> str:
    return f"round222-{label}:{digest(value)}"


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def verify_row(row: dict[str, Any], label: str) -> None:
    require(
        row.get("row_sha256")
        == digest({key: value for key, value in row.items() if key != "row_sha256"}),
        f"row closure:{label}",
    )


def histogram(values: Iterable[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


def regular_bytes(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    before = path.lstat()
    require(
        stat.S_ISREG(before.st_mode) and not path.is_symlink()
        and before.st_nlink == 1,
        f"single-link regular:{path.name}",
    )
    require(0 < before.st_size <= maximum, f"bounded:{path.name}")
    descriptor = os.open(
        path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns)
            == (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns),
            f"stable open:{path.name}",
        )
        parts: list[bytes] = []
        size = 0
        while True:
            part = os.read(descriptor, 1024 * 1024)
            if not part:
                break
            size += len(part)
            require(size <= maximum, f"bounded read:{path.name}")
            parts.append(part)
        after = os.fstat(descriptor)
        require(
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns),
            f"stable read:{path.name}",
        )
        return b"".join(parts)
    finally:
        os.close(descriptor)


def pinned(path: Path, expected: str, maximum: int = MAX_INPUT_BYTES) -> bytes:
    raw = regular_bytes(path, maximum)
    require(hashlib.sha256(raw).hexdigest() == expected, f"SHA256:{path.name}")
    return raw


def parse_manifest(prefix: str) -> tuple[str, dict[str, str]]:
    expected, count = MANIFESTS[prefix]
    name = f"{prefix}_manifest.sha256"
    raw = pinned(HERE / name, expected, 100_000)
    entries: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        fields = line.split()
        require(len(fields) == 2, f"manifest line:{name}")
        sha, entry = fields
        entry = entry.lstrip("*")
        require(
            len(sha) == 64 and entry == Path(entry).name
            and entry.startswith(prefix) and entry not in entries,
            f"manifest entry:{name}",
        )
        entries[entry] = sha
    require(len(entries) == count, f"manifest count:{name}")
    for entry, sha in entries.items():
        pinned(HERE / entry, sha)
    return expected, dict(sorted(entries.items()))


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, f"duplicate key:{label}:{key}")
            result[key] = value
        return result

    def reject(token: str) -> None:
        raise Round222Error(f"nonfinite:{label}:{token}")

    result = json.loads(raw, object_pairs_hook=pairs, parse_constant=reject)
    require(isinstance(result, dict), f"object:{label}")
    return result


def load_envelope(name: str, file_sha: str, result_sha: str) -> dict[str, Any]:
    envelope = strict_json(pinned(HERE / name, file_sha), name)
    require(
        envelope.get("result_sha256") == result_sha
        and digest(envelope.get("result")) == result_sha,
        f"result closure:{name}",
    )
    return envelope


def verify_ledger(value: dict[str, Any], id_key: str, label: str) -> list[dict[str, Any]]:
    rows = value["rows"]
    require(value["row_count"] == len(rows), f"count:{label}")
    require(value["rows_sha256"] == digest(rows), f"rows:{label}")
    require(
        value["row_ids_sha256"] == digest([row[id_key] for row in rows]),
        f"ids:{label}",
    )
    if "row_hashes_sha256" in value:
        require(
            value["row_hashes_sha256"]
            == digest([row["row_sha256"] for row in rows]),
            f"hashes:{label}",
        )
    for row in rows:
        verify_row(row, f"{label}:{row[id_key]}")
    return rows


def ledger(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    require(len({row[id_key] for row in rows}) == len(rows), f"unique:{id_key}")
    return {
        "row_count": len(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows": rows,
    }


class UF:
    def __init__(self, nodes: Iterable[str]) -> None:
        self.parent = {node: node for node in nodes}
        self.size = {node: 1 for node in self.parent}

    def find(self, node: str) -> str:
        root = node
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[node] != node:
            following = self.parent[node]
            self.parent[node] = root
            node = following
        return root

    def join(self, left: str, right: str) -> bool:
        left, right = self.find(left), self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right] or (
            self.size[left] == self.size[right] and left > right
        ):
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True

    def groups(self) -> list[list[str]]:
        groups: dict[str, list[str]] = defaultdict(list)
        for node in self.parent:
            groups[self.find(node)].append(node)
        return sorted(sorted(group) for group in groups.values())


def baseline_from_round214() -> tuple[
    set[tuple[str, str]], dict[str, int], dict[str, Any]
]:
    """Rebuild the safe quotient; return leaf pairs, probe counts, audit."""
    print("Round222 reconstructing the Round214 baseline", file=sys.stderr)
    leaves, regions, _u2, sheets, curves, endpoints, _wall, _hashes = (
        r214.validate_inputs()
    )
    leaf_by_id = {row["leaf_row_id"]: row for row in leaves}
    region_by_id = {row["region_row_id"]: row for row in regions}
    sheet_by_leaf = {row["leaf_row_id"]: row for row in sheets}
    boxes = {
        leaf_id: tuple(Q(value) for value in leaf_by_id[leaf_id]["box"])
        for leaf_id in sheet_by_leaf
    }
    parent = {
        row["leaf_row_id"]: row["parent_id"] for row in regions
        if row["leaf_row_id"] in sheet_by_leaf
    }
    occurrence = {
        leaf_id: row["occurrence_row_id"]
        for leaf_id, row in sheet_by_leaf.items()
    }
    identity: dict[str, tuple[Any, ...]] = {}
    for leaf_id, sheet in sheet_by_leaf.items():
        signature = region_by_id[sheet["owner_region_row_id"]][
            "local_return_signature"
        ]
        identity[leaf_id] = (
            parent[leaf_id], signature["source_chart"],
            signature["target_lift"], tuple(signature["signed_wall_word"]),
            signature["roof"], sheet["active_factor"],
            sheet["owner_outgoing_cell"], sheet["owner_signature_core_sha256"],
        )

    def curve_carrier(row: dict[str, Any]) -> tuple[Any, ...]:
        box = boxes[row["leaf_row_id"]]
        t = box[0] if row["face_side"] == "LOWER" else box[1]
        return identity[row["leaf_row_id"]] + (t, box[2], box[3], box[4], box[5])

    def endpoint_carrier(row: dict[str, Any]) -> tuple[Any, ...]:
        box = boxes[row["leaf_row_id"]]
        t = box[0] if row["face_side"] == "LOWER" else box[1]
        edge = row["boundary_edge"]
        geometry = (
            ("s", box[4], box[2], box[3]) if edge == "S"
            else ("s", box[5], box[2], box[3]) if edge == "N"
            else ("p", box[2], box[4], box[5]) if edge == "W"
            else ("p", box[3], box[4], box[5])
        )
        require(edge in {"S", "N", "W", "E"}, "endpoint edge")
        return identity[row["leaf_row_id"]] + (t,) + geometry

    curve_groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    endpoint_groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in curves:
        curve_groups[
            curve_carrier(row) + (occurrence[row["leaf_row_id"]],)
        ].append(row)
    for row in endpoints:
        endpoint_groups[
            endpoint_carrier(row) + (occurrence[row["leaf_row_id"]],)
        ].append(row)

    sheet_uf = UF(sheet_by_leaf)
    curve_uf = UF(row["curve_row_id"] for row in curves)
    endpoint_uf = UF(row["endpoint_row_id"] for row in endpoints)
    pairs: set[tuple[str, str]] = set()
    counts = {"curve_evidence": 0, "endpoint_evidence": 0}
    for rows in curve_groups.values():
        rows = sorted(rows, key=lambda row: row["leaf_row_id"])
        first = rows[0]
        for row in rows[1:]:
            sheet_uf.join(first["leaf_row_id"], row["leaf_row_id"])
            curve_uf.join(first["curve_row_id"], row["curve_row_id"])
            pairs.add(tuple(sorted((first["leaf_row_id"], row["leaf_row_id"]))))
            counts["curve_evidence"] += 1
    for rows in endpoint_groups.values():
        rows = sorted(rows, key=lambda row: row["leaf_row_id"])
        first = rows[0]
        for row in rows[1:]:
            sheet_uf.join(first["leaf_row_id"], row["leaf_row_id"])
            curve_uf.join(first["curve_row_id"], row["curve_row_id"])
            endpoint_uf.join(first["endpoint_row_id"], row["endpoint_row_id"])
            pairs.add(tuple(sorted((first["leaf_row_id"], row["leaf_row_id"]))))
            counts["endpoint_evidence"] += 1
    sheet_groups, curve_groups_out, endpoint_groups_out = (
        sheet_uf.groups(), curve_uf.groups(), endpoint_uf.groups()
    )
    require(
        counts == {"curve_evidence": 4_260, "endpoint_evidence": 10_036}
        and len(pairs) == 5_935 and len(sheet_groups) == 12_156
        and digest(sheet_groups) == R214_SHEET_HASH
        and len(curve_groups_out) == 14_680
        and digest(curve_groups_out) == R214_CURVE_HASH
        and len(endpoint_groups_out) == 30_876
        and digest(endpoint_groups_out) == R214_ENDPOINT_HASH,
        "Round214 independent baseline",
    )
    audit = {
        "evidence_row_count": 14_296,
        "curve_carrier_evidence_row_count": 4_260,
        "endpoint_carrier_evidence_row_count": 10_036,
        "unique_sheet_pair_count": len(pairs),
        "union_rank_reduction": 17_716 - len(sheet_groups),
        "sheet_block_count": len(sheet_groups),
        "sheet_block_size_histogram":
            histogram(len(group) for group in sheet_groups),
        "sheet_block_membership_sha256": digest(sheet_groups),
        "curve_block_count": len(curve_groups_out),
        "curve_block_membership_sha256": digest(curve_groups_out),
        "endpoint_block_count": len(endpoint_groups_out),
        "endpoint_block_membership_sha256": digest(endpoint_groups_out),
        "physical_component_count_claimed": False,
    }
    del (
        leaves, regions, sheets, curves, endpoints, leaf_by_id, region_by_id,
        sheet_by_leaf, boxes, parent, occurrence, identity, curve_groups,
        endpoint_groups,
    )
    gc.collect()
    return pairs, counts, audit


def build_result(producer_sha256: str) -> dict[str, Any]:
    print("Round222 validating five frozen manifests", file=sys.stderr)
    manifest_entries: dict[str, dict[str, str]] = {}
    manifest_hashes: dict[str, str] = {}
    for prefix in MANIFESTS:
        manifest_hashes[f"{prefix}_manifest_sha256"], entries = (
            parse_manifest(prefix)
        )
        manifest_entries[prefix] = entries
    pinned(
        HERE / "cm2_round214_source_g_physical_component_join_dedup_feasibility_probe.py",
        R214_SOURCE_SHA256,
        5_000_000,
    )
    pinned(
        HERE / "cm2_round214_source_g_physical_component_join_dedup_spike_report.md",
        R214_REPORT_SHA256,
        5_000_000,
    )
    require(
        Path(r214.__file__).resolve()
        == (
            HERE
            / "cm2_round214_source_g_physical_component_join_dedup_feasibility_probe.py"
        ).resolve(),
        "Round214 module identity",
    )
    baseline_leaf_pairs, _baseline_counts, baseline_audit = (
        baseline_from_round214()
    )

    round211 = load_envelope(
        f"{R211}_certificate.json",
        manifest_entries[R211][f"{R211}_certificate.json"],
        RESULTS[R211],
    )
    sheet_rows = verify_ledger(
        round211["result"]["formal_2D_sheet_owner_ledger"],
        "sheet_row_id",
        "Round211 sheets",
    )
    require(len(sheet_rows) == 17_716, "Round211 sheet census")
    sheet_rows = sorted(sheet_rows, key=lambda row: row["sheet_row_id"])
    sheet_by_id = {row["sheet_row_id"]: row for row in sheet_rows}
    sheet_by_leaf = {row["leaf_row_id"]: row for row in sheet_rows}
    require(len(sheet_by_id) == len(sheet_by_leaf) == 17_716, "leaf/sheet bijection")
    baseline_pairs = {
        tuple(sorted((
            sheet_by_leaf[left]["sheet_row_id"],
            sheet_by_leaf[right]["sheet_row_id"],
        )))
        for left, right in baseline_leaf_pairs
    }
    require(len(baseline_pairs) == 5_935, "formal baseline pair census")
    del round211, baseline_leaf_pairs
    gc.collect()

    round217 = load_envelope(
        f"{R217}_certificate.json",
        manifest_entries[R217][f"{R217}_certificate.json"],
        RESULTS[R217],
    )["result"]
    incidences217 = verify_ledger(
        round217["formal_internal_face_incidence_ledger"],
        "incidence_row_id",
        "Round217 incidences",
    )
    glues217 = verify_ledger(
        round217["formal_exact_common_refinement_glue_ledger"],
        "glue_row_id",
        "Round217 glues",
    )
    incidence217_by_id = {
        row["incidence_row_id"]: row for row in incidences217
    }
    exact_frontier217 = round217[
        "exact_face_endpoint_to_interior_frontier"
    ]["rows"]
    require(
        len(exact_frontier217) == 7_484
        and round217["exact_face_endpoint_to_interior_frontier"]["rows_sha256"]
        == digest(exact_frontier217),
        "Round217 frontier closure",
    )
    frontier217_by_id: dict[str, dict[str, Any]] = {}
    for row in exact_frontier217:
        verify_row(row, f"Round217 frontier:{row['frontier_row_id']}")
        require(
            row["negative_leaf_row_id"] in sheet_by_leaf
            and row["positive_leaf_row_id"] in sheet_by_leaf,
            "Round217 frontier leaf mapping",
        )
        frontier217_by_id[row["frontier_row_id"]] = row

    pair_evidence217: dict[tuple[str, str], list[str]] = defaultdict(list)
    trace_blocks217: list[list[str]] = []
    mapping_failure217 = 0
    relation217: Counter[str] = Counter()
    for glue in glues217:
        require(
            glue["formal_local_common_refinement_glue_credit"] == 1
            and glue["common_refinement_is_the_exact_shared_face"] is True
            and glue["exact_parent_atlas_identity"] is True
            and glue["exact_restricted_evaluator_identity"] is True
            and glue["joined_from_box_touch_or_signature_hash_alone"] is False
            and glue["component_deduplication_credit"] == 0
            and glue["global_component_credit"] == 0
            and glue["global_exact_key_disposition_credit"] == 0,
            "Round217 edge predicate",
        )
        negative = incidence217_by_id.get(
            glue["negative_side_incidence_row_id"]
        )
        positive = incidence217_by_id.get(
            glue["positive_side_incidence_row_id"]
        )
        if negative is None or positive is None:
            mapping_failure217 += 1
            continue
        left = sheet_by_id.get(negative["formal_Round211_sheet_row_id"])
        right = sheet_by_id.get(positive["formal_Round211_sheet_row_id"])
        if (
            left is None or right is None
            or left["leaf_row_id"] != glue["negative_side_leaf_row_id"]
            or right["leaf_row_id"] != glue["positive_side_leaf_row_id"]
            or negative["formal_Round211_sheet_row_sha256"] != left["row_sha256"]
            or positive["formal_Round211_sheet_row_sha256"] != right["row_sha256"]
            or left["active_factor"] != right["active_factor"]
            or left["owner_signature_core_sha256"]
            != right["owner_signature_core_sha256"]
        ):
            mapping_failure217 += 1
            continue
        pair = tuple(sorted((left["sheet_row_id"], right["sheet_row_id"])))
        require(pair[0] != pair[1], "Round217 self-loop")
        pair_evidence217[pair].append(glue["glue_row_id"])
        trace_blocks217.append(sorted([
            negative["incidence_row_id"], positive["incidence_row_id"]
        ]))
        relation217[glue["relation"]] += 1
    require(
        mapping_failure217 == 0 and len(glues217) == 448
        and len(pair_evidence217) == 448
        and relation217 == Counter({"CROSS_ORIGIN": 416, "SAME_OCCURRENCE": 32}),
        "Round217 mapping/pair census",
    )
    del incidences217, glues217, incidence217_by_id, exact_frontier217
    gc.collect()

    round219 = load_envelope(
        f"{R219}_certificate.json",
        manifest_entries[R219][f"{R219}_certificate.json"],
        RESULTS[R219],
    )["result"]
    terminal219 = verify_ledger(
        round219["formal_terminal_subface_ledger"],
        "terminal_subface_row_id",
        "Round219 terminal subfaces",
    )
    contacts219 = verify_ledger(
        round219["formal_exact_contact_partition_ledger"],
        "exact_contact_row_id",
        "Round219 contact partitions",
    )
    partial219 = verify_ledger(
        round219["formal_partial_contact_probe_ledger"],
        "partial_contact_row_id",
        "Round219 partial probes",
    )
    pair_evidence219: dict[tuple[str, str], list[str]] = defaultdict(list)
    trace_blocks219: list[list[str]] = []
    trace_axis219: Counter[str] = Counter()
    mapping_failure219 = 0
    trace_row_ids219: list[str] = []
    for terminal in terminal219:
        if terminal["classification"] != "TRACE":
            require(
                terminal["formal_local_subface_glue_credit"] == 0,
                "Round219 non-TRACE nonedge",
            )
            continue
        require(
            terminal["formal_restricted_zero_curve_credit"] == 1
            and terminal["formal_local_subface_incidence_credit"] == 2
            and terminal["formal_local_subface_glue_credit"] == 1
            and terminal["exact_restricted_evaluator_identity"] is True
            and terminal[
                "joined_from_box_touch_or_signature_hash_alone"
            ] is False
            and terminal["formal_component_deduplication_credit"] == 0
            and terminal["global_component_credit"] == 0
            and terminal["global_exact_key_disposition_credit"] == 0,
            "Round219 TRACE edge predicate",
        )
        frontier = frontier217_by_id.get(
            terminal["Round217_frontier_row_id"]
        )
        left = sheet_by_leaf.get(terminal["negative_side_leaf_row_id"])
        right = sheet_by_leaf.get(terminal["positive_side_leaf_row_id"])
        if (
            frontier is None or left is None or right is None
            or terminal["Round217_frontier_row_sha256"]
            != frontier["row_sha256"]
            or frontier["negative_leaf_row_id"] != left["leaf_row_id"]
            or frontier["positive_leaf_row_id"] != right["leaf_row_id"]
            or left["active_factor"] != right["active_factor"]
            or left["active_factor"] != frontier["active_factor"]
            or left["owner_signature_core_sha256"]
            != right["owner_signature_core_sha256"]
            or left["owner_signature_core_sha256"]
            != frontier["owner_signature_core_sha256"]
        ):
            mapping_failure219 += 1
            continue
        pair = tuple(sorted((left["sheet_row_id"], right["sheet_row_id"])))
        require(pair[0] != pair[1], "Round219 self-loop")
        pair_evidence219[pair].append(terminal["terminal_subface_row_id"])
        trace_blocks219.append(sorted([
            terminal["negative_side_incidence_row_id"],
            terminal["positive_side_incidence_row_id"],
        ]))
        trace_axis219[terminal["fixed_axis"]] += 1
        trace_row_ids219.append(terminal["terminal_subface_row_id"])
    require(
        mapping_failure219 == 0 and len(trace_row_ids219) == 22_960
        and len(pair_evidence219) == 6_588
        and trace_axis219 == Counter({"p": 16_312, "s": 6_648})
        and not (set(pair_evidence217) & set(pair_evidence219)),
        "Round219 mapping/pair census",
    )
    new_pairs = set(pair_evidence217) | set(pair_evidence219)
    require(len(new_pairs) == 7_036, "new pair census")
    del terminal219, round219, frontier217_by_id
    gc.collect()

    print("Round222 applying fixed-source union-find", file=sys.stderr)
    uf = UF(sheet_by_id)
    source_audit: dict[str, dict[str, int]] = {}
    for source, pairs, evidence_count in (
        ("ROUND214_SAFE_CARRIER_BASELINE", baseline_pairs, 14_296),
        ("ROUND217_EXACT_FULL_FACE_TRACE_GLUE", set(pair_evidence217), 448),
        ("ROUND219_TRACE_TERMINAL_SUBFACE_GLUE", set(pair_evidence219), 22_960),
    ):
        merges = sum(uf.join(*pair) for pair in sorted(pairs))
        source_audit[source] = {
            "evidence_row_count": evidence_count,
            "unique_sheet_pair_count": len(pairs),
            "union_rank_reduction": merges,
            "rank_redundant_unique_pair_count": len(pairs) - merges,
            "known_connectivity_block_count_after_source": len(uf.groups()),
        }
    require(
        source_audit["ROUND214_SAFE_CARRIER_BASELINE"]["union_rank_reduction"]
        == 5_560
        and source_audit["ROUND217_EXACT_FULL_FACE_TRACE_GLUE"][
            "union_rank_reduction"
        ] == 448
        and source_audit["ROUND219_TRACE_TERMINAL_SUBFACE_GLUE"][
            "union_rank_reduction"
        ] == 4_068
        and len(uf.groups()) == 7_640,
        "union rank census",
    )

    edge_rows: list[dict[str, Any]] = []
    for source, evidence in (
        ("ROUND217_EXACT_FULL_FACE_TRACE_GLUE", pair_evidence217),
        ("ROUND219_TRACE_TERMINAL_SUBFACE_GLUE", pair_evidence219),
    ):
        for pair in sorted(evidence):
            ids = sorted(evidence[pair])
            edge_rows.append(closed({
                "current_quotient_edge_row_id":
                    make_id("current-quotient-edge", [source, *pair]),
                "source_layer": source,
                "left_Round211_sheet_row_id": pair[0],
                "right_Round211_sheet_row_id": pair[1],
                "left_leaf_row_id": sheet_by_id[pair[0]]["leaf_row_id"],
                "right_leaf_row_id": sheet_by_id[pair[1]]["leaf_row_id"],
                "upstream_evidence_row_count": len(ids),
                "upstream_evidence_row_ids_sha256": digest(ids),
                "mapping_failure_count": 0,
                "self_loop": False,
                "accepted_from_signature_hash_or_box_touch_alone": False,
                "current_quotient_lower_bound_edge_credit": 1,
                "maximal_physical_component_edge_credit": 0,
                "global_exact_key_disposition_credit": 0,
            }))
    edge_rows.sort(key=lambda row: row["current_quotient_edge_row_id"])
    require(len(edge_rows) == 7_036, "formal new edge ledger count")

    final_groups = uf.groups()
    all_pairs = baseline_pairs | new_pairs
    incident_pairs: Counter[str] = Counter()
    for left, right in all_pairs:
        incident_pairs[left] += 1
        incident_pairs[right] += 1
    require(
        sum(value > 0 for value in incident_pairs.values()) == 15_248,
        "incident sheet census",
    )

    sheet_to_block: dict[str, str] = {}
    block_rows: list[dict[str, Any]] = []
    for members in final_groups:
        block_id = make_id("known-connectivity-block", members)
        for member in members:
            sheet_to_block[member] = block_id
        block_rows.append(closed({
            "known_connectivity_block_id": block_id,
            "canonical_member_Round211_sheet_row_id": members[0],
            "member_Round211_sheet_row_count": len(members),
            "member_Round211_sheet_row_ids": members,
            "member_Round211_sheet_row_ids_sha256": digest(members),
            "member_leaf_row_ids_sha256": digest(sorted(
                sheet_by_id[member]["leaf_row_id"] for member in members
            )),
            "certified_known_connectivity": True,
            "maximal_physical_component_claimed": False,
            "component_exhaustion_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    block_rows.sort(key=lambda row: row["known_connectivity_block_id"])
    formal_membership = sorted(
        row["member_Round211_sheet_row_ids"] for row in block_rows
    )
    require(
        digest(formal_membership)
        == "715008789165502798276611bd763a8f6cf3160d9c74d8559a63c3cf7e467cd9",
        "final formal membership",
    )

    assignment_rows: list[dict[str, Any]] = []
    for sheet in sheet_rows:
        sheet_id = sheet["sheet_row_id"]
        assignment_rows.append(closed({
            "sheet_assignment_row_id": make_id("sheet-assignment", sheet_id),
            "Round211_sheet_row_id": sheet_id,
            "Round211_sheet_row_sha256": sheet["row_sha256"],
            "leaf_row_id": sheet["leaf_row_id"],
            "known_connectivity_block_id": sheet_to_block[sheet_id],
            "current_unique_proved_edge_incidence_count":
                incident_pairs[sheet_id],
            "isolated_under_current_proved_edge_set":
                incident_pairs[sheet_id] == 0,
            "maximal_physical_component_assignment_claimed": False,
            "global_exact_key_disposition_credit": 0,
        }))
    require(
        sum(row["isolated_under_current_proved_edge_set"]
            for row in assignment_rows) == 2_468,
        "isolated sheet census",
    )

    frontier_rows: list[dict[str, Any]] = []
    incomplete_exact_direct = 0
    incomplete_exact_indirect = 0
    incomplete_exact = 0
    for contact in contacts219:
        if contact[
            "formal_exact_contact_common_refinement_complete_credit"
        ] == 1:
            continue
        incomplete_exact += 1
        pair = tuple(sorted((
            sheet_by_leaf[contact["negative_leaf_row_id"]]["sheet_row_id"],
            sheet_by_leaf[contact["positive_leaf_row_id"]]["sheet_row_id"],
        )))
        direct = pair in pair_evidence219
        same = sheet_to_block[pair[0]] == sheet_to_block[pair[1]]
        incomplete_exact_direct += direct
        incomplete_exact_indirect += (not direct and same)
        frontier_rows.append(closed({
            "frontier_account_row_id": make_id(
                "frontier-account",
                ["ROUND219_INCOMPLETE_EXACT_CONTACT",
                 contact["exact_contact_row_id"]],
            ),
            "frontier_kind": "ROUND219_INCOMPLETE_EXACT_CONTACT",
            "upstream_row_id": contact["exact_contact_row_id"],
            "upstream_row_sha256": contact["row_sha256"],
            "left_Round211_sheet_row_id": pair[0],
            "right_Round211_sheet_row_id": pair[1],
            "TRACE_edge_already_materialized_on_a_terminal_subface": direct,
            "same_current_known_connectivity_block": same,
            "UNRESOLVED_terminal_subface_count":
                contact["UNRESOLVED_terminal_subface_count"],
            "contact_partition_complete": False,
            "same_current_block_does_not_replace_contact_partition": True,
            "current_quotient_lower_bound_edge_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))

    partial_counts: Counter[str] = Counter()
    separating_unresolved: list[dict[str, Any]] = []
    for partial in partial219:
        pair = tuple(sorted((
            sheet_by_leaf[partial["negative_leaf_row_id"]]["sheet_row_id"],
            sheet_by_leaf[partial["positive_leaf_row_id"]]["sheet_row_id"],
        )))
        same = sheet_to_block[pair[0]] == sheet_to_block[pair[1]]
        classification = partial["classification"]
        partial_counts[classification] += 1
        account = closed({
            "frontier_account_row_id": make_id(
                "frontier-account",
                [f"ROUND219_PARTIAL_{classification}",
                 partial["partial_contact_row_id"]],
            ),
            "frontier_kind": f"ROUND219_PARTIAL_{classification}",
            "upstream_row_id": partial["partial_contact_row_id"],
            "upstream_row_sha256": partial["row_sha256"],
            "left_Round211_sheet_row_id": pair[0],
            "right_Round211_sheet_row_id": pair[1],
            "same_current_known_connectivity_block": same,
            "partial_TRACE_edge_materialized": False,
            "formal_partial_zero_absence_credit":
                partial["formal_partial_subface_zero_absence_credit"],
            "exact_trace_or_absence_proof_missing":
                classification == "UNRESOLVED",
            "potential_future_sheet_block_merge_under_missing_proof":
                classification == "UNRESOLVED" and not same,
            "current_quotient_lower_bound_edge_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        frontier_rows.append(account)
        if classification == "UNRESOLVED" and not same:
            separating_unresolved.append(account)
    frontier_rows.sort(key=lambda row: row["frontier_account_row_id"])
    separating_unresolved.sort(key=lambda row: row["upstream_row_id"])
    require(
        incomplete_exact == 7_016 and incomplete_exact_direct == 6_120
        and incomplete_exact_indirect == 896
        and partial_counts == Counter({"UNRESOLVED": 236, "ABSENT": 28})
        and len(separating_unresolved) == 236,
        "frontier connectivity census",
    )

    trace_blocks = sorted(trace_blocks217 + trace_blocks219)
    trace_incidences = [incidence for block in trace_blocks for incidence in block]
    require(
        len(trace_blocks) == 23_408 and len(trace_incidences) == 46_816
        and len(set(trace_incidences)) == 46_816,
        "trace-incidence quotient census",
    )

    round216 = load_envelope(
        f"{R216}_certificate.json",
        manifest_entries[R216][f"{R216}_certificate.json"],
        RESULTS[R216],
    )["result"]
    require(
        round216["formal_key_occurrence_exhaustion_frontier_ledger"][
            "row_count"
        ] == 116
        and round216["strict_nonpromotion"][
            "global_exact_key_fibre_exhausted_count"
        ] == 0,
        "Round216 global frontier",
    )
    verification220 = load_envelope(
        f"{R220}_verification.json",
        manifest_entries[R220][f"{R220}_verification.json"],
        RESULTS[f"{R220}_verification"],
    )["result"]
    require(
        verification220["status"] == "PASS_FORMAL_ROUND220"
        and verification220["independent_reconstruction"][
            "coordinate_adjacencies"
        ] == 10_384
        and verification220["independent_reconstruction"][
            "rejected_coordinate_coincidences"
        ] == 9_830
        and verification220["strict_nonpromotion_reconfirmed"][
            "physical_component_credit"
        ] == 0,
        "Round220 coordinate nonedges",
    )

    first_missing = separating_unresolved[0]
    return {
        "status": STATUS,
        "verdict": (
            "OUTCOME_BLIND_CURRENT_QUOTIENT_LOWER_BOUND_MATERIALIZED__"
            "UNRESOLVED_AND_COORDINATE_ONLY_FRONTIERS_EXCLUDED__"
            "NO_MAXIMAL_PHYSICAL_COMPONENT_OR_GLOBAL_CLAIM"
        ),
        "formal_input_binding": {
            **manifest_hashes,
            "manifest_entries": manifest_entries,
            "Round214_probe_source_sha256": R214_SOURCE_SHA256,
            "Round214_probe_report_sha256": R214_REPORT_SHA256,
            "Round214_probe_result_sha256": R214_RESULT_SHA256,
            "Round214_conclusion_trusted_without_reconstruction": False,
            "Round214_baseline_reconstructed_from_Round211_lineages": True,
            "Round211_leaf_to_sheet_mapping_failure_count": 0,
            "Round217_incidence_to_Round211_sheet_mapping_failure_count":
                mapping_failure217,
            "Round219_leaf_to_Round211_sheet_mapping_failure_count":
                mapping_failure219,
            "producer_outcome_or_oracle_dependency": False,
        },
        "terminology_and_scope_contract": {
            "allowed_block_term": "CERTIFIED_KNOWN_CONNECTIVITY_BLOCK",
            "allowed_edge_term": "CURRENT_QUOTIENT_LOWER_BOUND_EDGE",
            "known_connectivity_block_count_is_not_a_component_count": True,
            "maximal_physical_component_term_forbidden": True,
            "same_current_block_does_not_complete_an_unresolved_contact": True,
            "coordinate_adjacency_is_not_event_glue": True,
            "UNRESOLVED_or_ABSENT_row_is_not_an_edge": True,
        },
        "Round214_old_safe_quotient_baseline": baseline_audit,
        "source_layered_edge_audit": {
            "fixed_source_precedence": [
                "ROUND214_SAFE_CARRIER_BASELINE",
                "ROUND217_EXACT_FULL_FACE_TRACE_GLUE",
                "ROUND219_TRACE_TERMINAL_SUBFACE_GLUE",
            ],
            "source_layers": source_audit,
            "Round214_unique_sheet_pairs_sha256":
                digest(sorted([list(pair) for pair in baseline_pairs])),
            "Round217_unique_sheet_pairs_sha256":
                digest(sorted([list(pair) for pair in pair_evidence217])),
            "Round219_unique_sheet_pairs_sha256":
                digest(sorted([list(pair) for pair in pair_evidence219])),
            "Round217_plus_Round219_unique_sheet_pairs_sha256":
                digest(sorted([list(pair) for pair in new_pairs])),
            "Round217_plus_Round219_evidence_row_count": 23_408,
            "Round217_plus_Round219_unique_sheet_pair_count": 7_036,
            "Round217_plus_Round219_pair_overlap_count": 0,
            "Round214_vs_Round217_Round219_literal_pair_overlap_count":
                len(baseline_pairs & new_pairs),
            "Round214_vs_Round217_literal_pair_overlap_count":
                len(baseline_pairs & set(pair_evidence217)),
            "Round214_vs_Round219_literal_pair_overlap_count":
                len(baseline_pairs & set(pair_evidence219)),
            "Round219_TRACE_evidence_multiplicity_histogram":
                histogram(len(rows) for rows in pair_evidence219.values()),
            "Round219_TRACE_evidence_row_ids_sha256":
                digest(sorted(trace_row_ids219)),
            "total_unique_current_quotient_pair_count": len(all_pairs),
            "total_union_rank_reduction": 17_716 - len(final_groups),
        },
        "old_vs_new_known_connectivity_delta": {
            "raw_Round211_sheet_rows": 17_716,
            "Round214_old_safe_block_count": 12_156,
            "Round217_rank_reduction": 448,
            "block_count_after_Round217": 11_708,
            "Round219_rank_reduction": 4_068,
            "Round219_rank_redundant_unique_pair_count": 2_520,
            "current_known_connectivity_block_count": len(final_groups),
            "current_known_connectivity_block_size_histogram":
                histogram(len(group) for group in final_groups),
            "current_known_connectivity_member_sheet_rows_sha256":
                digest(formal_membership),
            "current_edge_incident_sheet_count": 15_248,
            "current_edge_isolated_sheet_count": 2_468,
            "maximal_physical_component_count_claimed": False,
            "component_exhaustion_credit": 0,
        },
        "legacy_curve_endpoint_and_new_trace_strata_audit": {
            "legacy_Round211_curve_rows": 20_456,
            "legacy_Round214_curve_block_count": 14_680,
            "legacy_Round214_curve_block_membership_sha256": R214_CURVE_HASH,
            "new_proved_equality_edges_between_legacy_Round211_curve_rows": 0,
            "legacy_Round211_endpoint_rows": 40_912,
            "legacy_Round214_endpoint_block_count": 30_876,
            "legacy_Round214_endpoint_block_membership_sha256":
                R214_ENDPOINT_HASH,
            "new_proved_equality_edges_between_legacy_Round211_endpoint_rows":
                0,
            "new_p_s_local_trace_incidence_row_count": 46_816,
            "new_p_s_two_sided_local_trace_block_count": 23_408,
            "new_p_s_local_trace_block_size_histogram": {"2": 23_408},
            "new_p_s_local_trace_block_membership_sha256":
                digest(trace_blocks),
            "endpoint_to_curve_interior_join_count": 0,
            "p_s_trace_blocks_are_not_maximal_physical_components": True,
        },
        "formal_Round217_Round219_current_quotient_edge_ledger":
            ledger(edge_rows, "current_quotient_edge_row_id"),
        "formal_certified_known_connectivity_block_ledger":
            ledger(block_rows, "known_connectivity_block_id"),
        "formal_Round211_sheet_assignment_ledger":
            ledger(assignment_rows, "sheet_assignment_row_id"),
        "formal_unresolved_and_nonedge_frontier_account_ledger":
            ledger(frontier_rows, "frontier_account_row_id"),
        "frontier_connectivity_audit": {
            "Round219_incomplete_exact_contact_count": incomplete_exact,
            "incomplete_exact_with_direct_TRACE_edge_count":
                incomplete_exact_direct,
            "incomplete_exact_without_direct_edge_but_same_current_block_count":
                incomplete_exact_indirect,
            "incomplete_exact_contact_partition_still_required": True,
            "Round219_partial_ABSENT_nonedge_count": partial_counts["ABSENT"],
            "Round219_partial_UNRESOLVED_nonedge_count":
                partial_counts["UNRESOLVED"],
            "partial_UNRESOLVED_pair_in_distinct_current_blocks_count":
                len(separating_unresolved),
            "first_missing_frontier": {
                "upstream_partial_contact_row_id":
                    first_missing["upstream_row_id"],
                "upstream_partial_contact_row_sha256":
                    first_missing["upstream_row_sha256"],
                "left_Round211_sheet_row_id":
                    first_missing["left_Round211_sheet_row_id"],
                "right_Round211_sheet_row_id":
                    first_missing["right_Round211_sheet_row_id"],
                "first_missing_proof":
                    "EXACT_PARTIAL_FACE_TRACE_OR_ABSENCE_AND_ENDPOINT_TO_"
                    "CURVE_INTERIOR_COMMON_REFINEMENT",
            },
        },
        "Round216_Round220_boundary_and_nonedge_audit": {
            "Round216_exact_key_frontier_row_count": 116,
            "Round216_resolved_children_missing_coordinate_atlas": 17_192,
            "Round220_resolved_children_with_coordinate_atlas": 17_192,
            "Round220_remaining_unatlased_resolved_children": 0,
            "Round220_coordinate_adjacency_nonedge_count": 10_384,
            "Round220_rejected_coordinate_coincidence_nonedge_count": 9_830,
            "Round220_coordinate_adjacency_union_edge_count": 0,
            "Round220_cross_parent_cross_chart_physical_glue_missing": True,
            "Round220_coordinate_atlas_blocker_closed": True,
            "Round220_physical_glue_blocker_closed": False,
            "all_116_global_exact_key_fibres_exhausted": False,
        },
        "strict_nonpromotion": {
            "formal_component_deduplication_credit": 0,
            "maximal_physical_component_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_component_credit": 0,
            "global_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator": SOURCE_G_KEYS,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "materialize exact partial-face trace/absence restrictions and "
            "endpoint-to-curve-interior joins for the 236 separating "
            "Round219 contacts; separately prove cross-parent/cross-chart "
            "transition glues for Round220.  Rebuild after every new proved "
            "edge; current blocks remain connectivity lower bounds."
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "producer_outcome_blind": True,
            "formal_upstream_files_modified": False,
            "independent_verifier_must_not_import_or_execute_producer": True,
        },
    }


def validate_output(path: Path) -> Path:
    require(not any(part == ".." for part in path.parts), "output parent alias")
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE and absolute.parent.resolve() == HERE
        and (
            absolute.name == OUTPUT.name
            or (
                absolute.name.startswith(f".{PREFIX}_replay_")
                and absolute.name.endswith(".json")
            )
        ),
        "output directory/allowlist",
    )
    protected = {
        Path(__file__).resolve(),
        *((HERE / f"{prefix}_manifest.sha256").resolve()
          for prefix in MANIFESTS),
    }
    require(
        absolute.resolve(strict=False) not in protected, "protected output"
    )
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "existing output type",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        directory = os.open(
            os.fspath(destination.parent),
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        raise
    finally:
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    producer_sha256 = hashlib.sha256(
        regular_bytes(Path(__file__), 5_000_000)
    ).hexdigest()
    result = build_result(producer_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical_bytes(envelope) + b"\n")
    print(STATUS)
    print(f"result_sha256={envelope['result_sha256']}")
    print(f"output={validate_output(arguments.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
