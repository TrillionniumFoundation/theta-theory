#!/usr/bin/env python3
"""Independent verifier for the Round222 known-connectivity quotient.

The verifier never imports or executes the Round222 producer.  It rebuilds
the Round214 baseline and the Round217/Round219 exact TRACE sheet pairs from
the pinned upstream rows, recomputes union-find membership, and validates
every formal Round222 edge, block, assignment, and frontier-account row.
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
from typing import Any, Callable, Iterable

import cm2_round214_source_g_physical_component_join_dedup_feasibility_probe as r214


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round222_source_g_certified_known_connectivity_union_find"
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE = HERE / f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
SCHEMA = "cm2.round222.source-g-certified-known-connectivity-union-find.v1"
VERIFICATION_SCHEMA = f"{SCHEMA}.verification.v1"
PRODUCER_SHA256 = "58b5b63dc25a44c7d2279d54b1eb842d88cc61e3abd6c31f889688d3d2801a22"
CANDIDATE_SHA256 = "700174fc3bdfa57805ce8a2a97630fd9e6183ce5aee443c430f14db6184e9e9e"
CANDIDATE_RESULT_SHA256 = "1b80b806fa6716135480a500ff1248cc8dfabb37af7b3802ba50ba1bf62b493e"
MAX_INPUT_BYTES = 800 * 1024 * 1024

R211 = "cm2_round211_source_g_outgoing_half_open_owner_materialization"
R216 = "cm2_round216_source_g_global_key_occurrence_exhaustion_frontier"
R217 = "cm2_round217_source_g_internal_face_trace_glue_materialization"
R219 = "cm2_round219_source_g_partial_face_common_refinement_glue"
R220 = "cm2_round220_source_g_round179_resolved_child_boundary_atlas"
MANIFESTS = {
    R211: "c0cf8b70de6dd147fd1009c97d28549ec4571f9d6c82b8bf46dba023e3fe943c",
    R216: "54f9f270a6bad485691fa1db12a46052fcd91615b01461ce40ad55b66475b58b",
    R217: "2b6df0e791e62743ee7a27e8556292166f07d8873a41e8de854b27787981b8c5",
    R219: "67470c6f9503bc5707135901a878fefc7086ac33caae4b578280dd0e6b5c2b9f",
    R220: "f6c4f748ca3a98fd214342d264006b5c2e71755174daf686556ff4926160c385",
}
RESULTS = {
    R211: "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b",
    R217: "fb4519a43f76cbc765e24b3cb0a0e25267d9664091e22139913f3899fd1e2286",
    R219: "f8d46a9a220b6b7e0e6f86430ad6d537d5358cd610f064417ab3e8b4c125744e",
}
R214_SOURCE_SHA256 = "d074aa045637ce1bb31768fa551bdb73ceda6a58c760cafe3dbf92faa7c922fe"
R214_SHEET_HASH = "7a679aca24e025463e0739485e2b0b5f6b4b11746d343f91b0743060623f56f8"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


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


def verify_row(row: dict[str, Any], label: str) -> None:
    require(
        row.get("row_sha256")
        == digest({key: value for key, value in row.items() if key != "row_sha256"}),
        f"row closure:{label}",
    )


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
        total = 0
        while True:
            part = os.read(descriptor, 1024 * 1024)
            if not part:
                break
            total += len(part)
            require(total <= maximum, f"bounded read:{path.name}")
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


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf"), f"BOM:{label}")
    require(b"\x00" not in raw, f"NUL:{label}")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, f"duplicate key:{label}:{key}")
            result[key] = value
        return result

    def reject(token: str) -> None:
        raise VerificationError(f"non-integral-or-nonfinite:{label}:{token}")

    value = json.loads(
        raw,
        object_pairs_hook=pairs,
        parse_float=reject,
        parse_constant=reject,
    )
    require(isinstance(value, dict), f"object:{label}")
    try:
        canonical_bytes(value)
    except UnicodeEncodeError as error:
        raise VerificationError(f"invalid Unicode scalar:{label}") from error
    return value


def parse_manifest(prefix: str) -> dict[str, str]:
    raw = pinned(
        HERE / f"{prefix}_manifest.sha256", MANIFESTS[prefix], 100_000
    )
    entries: dict[str, str] = {}
    for line in raw.decode("ascii").splitlines():
        sha, entry = line.split()
        entry = entry.lstrip("*")
        require(
            entry == Path(entry).name and entry.startswith(prefix)
            and entry not in entries,
            f"manifest entry:{prefix}",
        )
        entries[entry] = sha
    require(len(entries) == 6, f"manifest count:{prefix}")
    for entry, sha in entries.items():
        pinned(HERE / entry, sha)
    return entries


def envelope(name: str, file_sha: str, result_sha: str) -> dict[str, Any]:
    value = strict_json(pinned(HERE / name, file_sha), name)
    require(
        value.get("result_sha256") == result_sha
        and digest(value.get("result")) == result_sha,
        f"result closure:{name}",
    )
    return value


def ledger_rows(
    value: dict[str, Any], id_key: str, label: str
) -> list[dict[str, Any]]:
    rows = value["rows"]
    require(value["row_count"] == len(rows), f"ledger count:{label}")
    require(value["rows_sha256"] == digest(rows), f"ledger rows:{label}")
    require(
        value["row_ids_sha256"] == digest([row[id_key] for row in rows]),
        f"ledger IDs:{label}",
    )
    if "row_hashes_sha256" in value:
        require(
            value["row_hashes_sha256"]
            == digest([row["row_sha256"] for row in rows]),
            f"ledger hashes:{label}",
        )
    require(len({row[id_key] for row in rows}) == len(rows), f"unique:{label}")
    for row in rows:
        verify_row(row, f"{label}:{row[id_key]}")
    return rows


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


def reconstruct_baseline_leaf_pairs() -> set[tuple[str, str]]:
    """Independent carrier grouping; no Round222 producer code is used."""
    leaves, regions, _u2, sheets, curves, endpoints, _wall, _hashes = (
        r214.validate_inputs()
    )
    leaf_by_id = {row["leaf_row_id"]: row for row in leaves}
    region_by_id = {row["region_row_id"]: row for row in regions}
    sheet_by_leaf = {row["leaf_row_id"]: row for row in sheets}
    boxes = {
        leaf: tuple(Q(value) for value in leaf_by_id[leaf]["box"])
        for leaf in sheet_by_leaf
    }
    parent = {
        row["leaf_row_id"]: row["parent_id"] for row in regions
        if row["leaf_row_id"] in sheet_by_leaf
    }
    occurrence = {
        leaf: row["occurrence_row_id"] for leaf, row in sheet_by_leaf.items()
    }
    identity: dict[str, tuple[Any, ...]] = {}
    for leaf, sheet in sheet_by_leaf.items():
        signature = region_by_id[sheet["owner_region_row_id"]][
            "local_return_signature"
        ]
        identity[leaf] = (
            parent[leaf], signature["source_chart"], signature["target_lift"],
            tuple(signature["signed_wall_word"]), signature["roof"],
            sheet["active_factor"], sheet["owner_outgoing_cell"],
            sheet["owner_signature_core_sha256"],
        )

    def curve_key(row: dict[str, Any]) -> tuple[Any, ...]:
        box = boxes[row["leaf_row_id"]]
        t = box[0] if row["face_side"] == "LOWER" else box[1]
        return identity[row["leaf_row_id"]] + (
            t, box[2], box[3], box[4], box[5],
            occurrence[row["leaf_row_id"]],
        )

    def endpoint_key(row: dict[str, Any]) -> tuple[Any, ...]:
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
        return identity[row["leaf_row_id"]] + (
            t, *geometry, occurrence[row["leaf_row_id"]],
        )

    curve_groups: dict[tuple[Any, ...], list[str]] = defaultdict(list)
    endpoint_groups: dict[tuple[Any, ...], list[str]] = defaultdict(list)
    for row in curves:
        curve_groups[curve_key(row)].append(row["leaf_row_id"])
    for row in endpoints:
        endpoint_groups[endpoint_key(row)].append(row["leaf_row_id"])
    uf = UF(sheet_by_leaf)
    pairs: set[tuple[str, str]] = set()
    curve_evidence = endpoint_evidence = 0
    for rows in curve_groups.values():
        rows = sorted(rows)
        for leaf in rows[1:]:
            uf.join(rows[0], leaf)
            pairs.add(tuple(sorted((rows[0], leaf))))
            curve_evidence += 1
    for rows in endpoint_groups.values():
        rows = sorted(rows)
        for leaf in rows[1:]:
            uf.join(rows[0], leaf)
            pairs.add(tuple(sorted((rows[0], leaf))))
            endpoint_evidence += 1
    require(
        curve_evidence == 4_260 and endpoint_evidence == 10_036
        and len(pairs) == 5_935 and len(uf.groups()) == 12_156
        and digest(uf.groups()) == R214_SHEET_HASH,
        "independent Round214 baseline",
    )
    del (
        leaves, regions, sheets, curves, endpoints, leaf_by_id, region_by_id,
        sheet_by_leaf, boxes, parent, occurrence, identity, curve_groups,
        endpoint_groups,
    )
    gc.collect()
    return pairs


def independent_reconstruction() -> dict[str, Any]:
    entries = {prefix: parse_manifest(prefix) for prefix in MANIFESTS}
    baseline_leaf_pairs = reconstruct_baseline_leaf_pairs()
    r211 = envelope(
        f"{R211}_certificate.json",
        entries[R211][f"{R211}_certificate.json"],
        RESULTS[R211],
    )["result"]
    sheets = ledger_rows(
        r211["formal_2D_sheet_owner_ledger"],
        "sheet_row_id",
        "Round211 sheets",
    )
    sheet_by_id = {row["sheet_row_id"]: row for row in sheets}
    sheet_by_leaf = {row["leaf_row_id"]: row for row in sheets}
    require(len(sheet_by_id) == len(sheet_by_leaf) == 17_716, "sheet bijection")
    baseline_pairs = {
        tuple(sorted((
            sheet_by_leaf[left]["sheet_row_id"],
            sheet_by_leaf[right]["sheet_row_id"],
        )))
        for left, right in baseline_leaf_pairs
    }
    require(len(baseline_pairs) == 5_935, "formal baseline pairs")
    del r211, baseline_leaf_pairs
    gc.collect()

    r217 = envelope(
        f"{R217}_certificate.json",
        entries[R217][f"{R217}_certificate.json"],
        RESULTS[R217],
    )["result"]
    incidences = ledger_rows(
        r217["formal_internal_face_incidence_ledger"],
        "incidence_row_id",
        "Round217 incidences",
    )
    glues = ledger_rows(
        r217["formal_exact_common_refinement_glue_ledger"],
        "glue_row_id",
        "Round217 glues",
    )
    incidence_by_id = {row["incidence_row_id"]: row for row in incidences}
    frontier217 = r217["exact_face_endpoint_to_interior_frontier"]["rows"]
    require(
        len(frontier217) == 7_484
        and r217["exact_face_endpoint_to_interior_frontier"]["rows_sha256"]
        == digest(frontier217),
        "Round217 frontier",
    )
    frontier217_by_id = {}
    for row in frontier217:
        verify_row(row, f"Round217 frontier:{row['frontier_row_id']}")
        frontier217_by_id[row["frontier_row_id"]] = row
    evidence217: dict[tuple[str, str], list[str]] = defaultdict(list)
    trace_blocks217: list[list[str]] = []
    failures217 = self_loops217 = false_edges217 = 0
    for glue in glues:
        if not (
            glue["formal_local_common_refinement_glue_credit"] == 1
            and glue["common_refinement_is_the_exact_shared_face"] is True
            and glue["exact_parent_atlas_identity"] is True
            and glue["exact_restricted_evaluator_identity"] is True
            and glue["joined_from_box_touch_or_signature_hash_alone"] is False
            and glue["component_deduplication_credit"] == 0
            and glue["global_component_credit"] == 0
        ):
            false_edges217 += 1
            continue
        negative = incidence_by_id.get(glue["negative_side_incidence_row_id"])
        positive = incidence_by_id.get(glue["positive_side_incidence_row_id"])
        if negative is None or positive is None:
            failures217 += 1
            continue
        left = sheet_by_id.get(negative["formal_Round211_sheet_row_id"])
        right = sheet_by_id.get(positive["formal_Round211_sheet_row_id"])
        if (
            left is None or right is None
            or left["leaf_row_id"] != glue["negative_side_leaf_row_id"]
            or right["leaf_row_id"] != glue["positive_side_leaf_row_id"]
            or negative["formal_Round211_sheet_row_sha256"] != left["row_sha256"]
            or positive["formal_Round211_sheet_row_sha256"] != right["row_sha256"]
        ):
            failures217 += 1
            continue
        pair = tuple(sorted((left["sheet_row_id"], right["sheet_row_id"])))
        if pair[0] == pair[1]:
            self_loops217 += 1
            continue
        evidence217[pair].append(glue["glue_row_id"])
        trace_blocks217.append(sorted([
            negative["incidence_row_id"], positive["incidence_row_id"]
        ]))
    require(
        failures217 == self_loops217 == false_edges217 == 0
        and len(glues) == len(evidence217) == 448,
        "Round217 exact edge reconstruction",
    )
    del incidences, glues, incidence_by_id, frontier217, r217
    gc.collect()

    r219 = envelope(
        f"{R219}_certificate.json",
        entries[R219][f"{R219}_certificate.json"],
        RESULTS[R219],
    )["result"]
    terminals = ledger_rows(
        r219["formal_terminal_subface_ledger"],
        "terminal_subface_row_id",
        "Round219 terminal subfaces",
    )
    contacts = ledger_rows(
        r219["formal_exact_contact_partition_ledger"],
        "exact_contact_row_id",
        "Round219 contacts",
    )
    partial = ledger_rows(
        r219["formal_partial_contact_probe_ledger"],
        "partial_contact_row_id",
        "Round219 partial",
    )
    evidence219: dict[tuple[str, str], list[str]] = defaultdict(list)
    trace_blocks219: list[list[str]] = []
    failures219 = self_loops219 = false_edges219 = 0
    trace_rows = 0
    for terminal in terminals:
        if terminal["classification"] != "TRACE":
            if terminal["formal_local_subface_glue_credit"] != 0:
                false_edges219 += 1
            continue
        trace_rows += 1
        if not (
            terminal["formal_restricted_zero_curve_credit"] == 1
            and terminal["formal_local_subface_incidence_credit"] == 2
            and terminal["formal_local_subface_glue_credit"] == 1
            and terminal["exact_restricted_evaluator_identity"] is True
            and terminal[
                "joined_from_box_touch_or_signature_hash_alone"
            ] is False
            and terminal["formal_component_deduplication_credit"] == 0
            and terminal["global_component_credit"] == 0
        ):
            false_edges219 += 1
            continue
        frontier = frontier217_by_id.get(terminal["Round217_frontier_row_id"])
        left = sheet_by_leaf.get(terminal["negative_side_leaf_row_id"])
        right = sheet_by_leaf.get(terminal["positive_side_leaf_row_id"])
        if (
            frontier is None or left is None or right is None
            or terminal["Round217_frontier_row_sha256"] != frontier["row_sha256"]
            or frontier["negative_leaf_row_id"] != left["leaf_row_id"]
            or frontier["positive_leaf_row_id"] != right["leaf_row_id"]
            or left["active_factor"] != right["active_factor"]
            or left["owner_signature_core_sha256"]
            != right["owner_signature_core_sha256"]
        ):
            failures219 += 1
            continue
        pair = tuple(sorted((left["sheet_row_id"], right["sheet_row_id"])))
        if pair[0] == pair[1]:
            self_loops219 += 1
            continue
        evidence219[pair].append(terminal["terminal_subface_row_id"])
        trace_blocks219.append(sorted([
            terminal["negative_side_incidence_row_id"],
            terminal["positive_side_incidence_row_id"],
        ]))
    require(
        failures219 == self_loops219 == false_edges219 == 0
        and trace_rows == 22_960 and len(evidence219) == 6_588
        and not (set(evidence217) & set(evidence219)),
        "Round219 exact edge reconstruction",
    )

    uf = UF(sheet_by_id)
    rank = {}
    for label, pairs in (
        ("Round214", baseline_pairs),
        ("Round217", set(evidence217)),
        ("Round219", set(evidence219)),
    ):
        rank[label] = sum(uf.join(*pair) for pair in sorted(pairs))
    groups = uf.groups()
    require(
        rank == {"Round214": 5_560, "Round217": 448, "Round219": 4_068}
        and len(groups) == 7_640,
        "independent union rank",
    )
    sheet_to_block = {}
    block_by_id = {}
    for members in groups:
        block_id = make_id("known-connectivity-block", members)
        block_by_id[block_id] = members
        for member in members:
            sheet_to_block[member] = block_id

    all_pairs = baseline_pairs | set(evidence217) | set(evidence219)
    incident: Counter[str] = Counter()
    for left, right in all_pairs:
        incident[left] += 1
        incident[right] += 1
    require(
        sum(value > 0 for value in incident.values()) == 15_248,
        "independent incident census",
    )

    frontier_expected: dict[str, dict[str, Any]] = {}
    direct_exact = indirect_exact = incomplete_exact = 0
    for contact in contacts:
        if contact[
            "formal_exact_contact_common_refinement_complete_credit"
        ] == 1:
            continue
        incomplete_exact += 1
        pair = tuple(sorted((
            sheet_by_leaf[contact["negative_leaf_row_id"]]["sheet_row_id"],
            sheet_by_leaf[contact["positive_leaf_row_id"]]["sheet_row_id"],
        )))
        direct = pair in evidence219
        same = sheet_to_block[pair[0]] == sheet_to_block[pair[1]]
        direct_exact += direct
        indirect_exact += (not direct and same)
        frontier_expected[contact["exact_contact_row_id"]] = {
            "kind": "ROUND219_INCOMPLETE_EXACT_CONTACT",
            "pair": pair,
            "direct": direct,
            "same": same,
            "unresolved":
                contact["UNRESOLVED_terminal_subface_count"],
            "row_sha256": contact["row_sha256"],
        }
    partial_counts: Counter[str] = Counter()
    first_missing = None
    for row in partial:
        pair = tuple(sorted((
            sheet_by_leaf[row["negative_leaf_row_id"]]["sheet_row_id"],
            sheet_by_leaf[row["positive_leaf_row_id"]]["sheet_row_id"],
        )))
        same = sheet_to_block[pair[0]] == sheet_to_block[pair[1]]
        partial_counts[row["classification"]] += 1
        frontier_expected[row["partial_contact_row_id"]] = {
            "kind": f"ROUND219_PARTIAL_{row['classification']}",
            "pair": pair,
            "same": same,
            "classification": row["classification"],
            "row_sha256": row["row_sha256"],
        }
        if row["classification"] == "UNRESOLVED" and not same:
            candidate = (row["partial_contact_row_id"], pair, row["row_sha256"])
            if first_missing is None or candidate < first_missing:
                first_missing = candidate
    require(
        incomplete_exact == 7_016 and direct_exact == 6_120
        and indirect_exact == 896
        and partial_counts == Counter({"UNRESOLVED": 236, "ABSENT": 28})
        and first_missing is not None,
        "independent frontier census",
    )

    trace_blocks = sorted(trace_blocks217 + trace_blocks219)
    trace_ids = [item for block in trace_blocks for item in block]
    require(
        len(trace_blocks) == 23_408 and len(set(trace_ids)) == 46_816,
        "independent trace block census",
    )
    del terminals, r219, frontier217_by_id
    gc.collect()
    return {
        "entries": entries,
        "sheets": sheets,
        "sheet_by_id": sheet_by_id,
        "sheet_by_leaf": sheet_by_leaf,
        "baseline_pairs": baseline_pairs,
        "evidence217": evidence217,
        "evidence219": evidence219,
        "groups": groups,
        "block_by_id": block_by_id,
        "sheet_to_block": sheet_to_block,
        "incident": incident,
        "frontier_expected": frontier_expected,
        "first_missing": first_missing,
        "trace_blocks": trace_blocks,
        "rank": rank,
        "all_pairs": all_pairs,
        "mapping_failures": failures217 + failures219,
        "self_loops": self_loops217 + self_loops219,
        "false_edges": false_edges217 + false_edges219,
    }


def validate_candidate_semantics(
    candidate: dict[str, Any],
    truth: dict[str, Any],
) -> None:
    require(candidate.get("schema") == SCHEMA, "candidate schema")
    result = candidate.get("result")
    require(isinstance(result, dict), "candidate result object")
    require(
        candidate.get("result_sha256") == digest(result),
        "candidate result closure",
    )
    require(
        result["status"]
        == "CERTIFIED_KNOWN_CONNECTIVITY_LOWER_BOUND__"
           "NOT_MAXIMAL_PHYSICAL_COMPONENTS__ZERO_PROMOTION",
        "candidate status",
    )
    require(
        result["provenance"]["producer_sha256"] == PRODUCER_SHA256
        and result["provenance"]["producer_outcome_blind"] is True,
        "producer binding/outcome blindness",
    )
    input_binding = result["formal_input_binding"]
    require(
        input_binding["producer_outcome_or_oracle_dependency"] is False
        and input_binding[
            "Round214_baseline_reconstructed_from_Round211_lineages"
        ] is True
        and input_binding[
            "Round214_conclusion_trusted_without_reconstruction"
        ] is False
        and input_binding["Round211_leaf_to_sheet_mapping_failure_count"] == 0
        and input_binding[
            "Round217_incidence_to_Round211_sheet_mapping_failure_count"
        ] == 0
        and input_binding[
            "Round219_leaf_to_Round211_sheet_mapping_failure_count"
        ] == 0,
        "claimed mapping census",
    )
    terminology = result["terminology_and_scope_contract"]
    require(
        terminology["known_connectivity_block_count_is_not_a_component_count"]
        is True
        and terminology["maximal_physical_component_term_forbidden"] is True
        and terminology["coordinate_adjacency_is_not_event_glue"] is True
        and terminology["UNRESOLVED_or_ABSENT_row_is_not_an_edge"] is True,
        "terminology/nonedge contract",
    )

    audit = result["source_layered_edge_audit"]
    require(
        audit["Round217_plus_Round219_unique_sheet_pair_count"] == 7_036
        and audit["Round217_plus_Round219_evidence_row_count"] == 23_408
        and audit["Round217_plus_Round219_pair_overlap_count"] == 0
        and audit[
            "Round214_vs_Round217_Round219_literal_pair_overlap_count"
        ] == 665
        and audit["total_unique_current_quotient_pair_count"] == 12_306
        and audit["total_union_rank_reduction"] == 10_076,
        "source audit census",
    )
    require(
        audit["Round214_unique_sheet_pairs_sha256"]
        == digest(sorted([list(pair) for pair in truth["baseline_pairs"]]))
        and audit["Round217_unique_sheet_pairs_sha256"]
        == digest(sorted([list(pair) for pair in truth["evidence217"]]))
        and audit["Round219_unique_sheet_pairs_sha256"]
        == digest(sorted([list(pair) for pair in truth["evidence219"]])),
        "source pair hashes",
    )

    expected_edges = {}
    for source, mapping in (
        ("ROUND217_EXACT_FULL_FACE_TRACE_GLUE", truth["evidence217"]),
        ("ROUND219_TRACE_TERMINAL_SUBFACE_GLUE", truth["evidence219"]),
    ):
        for pair, evidence_ids in mapping.items():
            expected_edges[(source, pair)] = sorted(evidence_ids)
    edge_rows = ledger_rows(
        result["formal_Round217_Round219_current_quotient_edge_ledger"],
        "current_quotient_edge_row_id",
        "candidate edge ledger",
    )
    require(len(edge_rows) == len(expected_edges) == 7_036, "edge ledger count")
    seen_edges = set()
    for row in edge_rows:
        source = row["source_layer"]
        pair = (
            row["left_Round211_sheet_row_id"],
            row["right_Round211_sheet_row_id"],
        )
        require(
            source in {
                "ROUND217_EXACT_FULL_FACE_TRACE_GLUE",
                "ROUND219_TRACE_TERMINAL_SUBFACE_GLUE",
            },
            "edge source whitelist/Round220 nonedge",
        )
        expected_ids = expected_edges.get((source, pair))
        require(
            expected_ids is not None and pair[0] < pair[1]
            and row["current_quotient_edge_row_id"]
            == make_id("current-quotient-edge", [source, *pair])
            and row["upstream_evidence_row_count"] == len(expected_ids)
            and row["upstream_evidence_row_ids_sha256"] == digest(expected_ids)
            and row["mapping_failure_count"] == 0 and row["self_loop"] is False
            and row["accepted_from_signature_hash_or_box_touch_alone"] is False
            and row["current_quotient_lower_bound_edge_credit"] == 1
            and row["maximal_physical_component_edge_credit"] == 0,
            "edge row semantics",
        )
        seen_edges.add((source, pair))
    require(seen_edges == set(expected_edges), "edge set equality")

    block_rows = ledger_rows(
        result["formal_certified_known_connectivity_block_ledger"],
        "known_connectivity_block_id",
        "candidate blocks",
    )
    require(len(block_rows) == 7_640, "block count")
    seen_blocks = {}
    for row in block_rows:
        members = row["member_Round211_sheet_row_ids"]
        block_id = make_id("known-connectivity-block", members)
        require(
            row["known_connectivity_block_id"] == block_id
            and truth["block_by_id"].get(block_id) == members
            and row["member_Round211_sheet_row_count"] == len(members)
            and row["member_Round211_sheet_row_ids_sha256"] == digest(members)
            and row["maximal_physical_component_claimed"] is False
            and row["component_exhaustion_credit"] == 0,
            "block row semantics",
        )
        seen_blocks[block_id] = members
    require(seen_blocks == truth["block_by_id"], "block membership equality")

    assignments = ledger_rows(
        result["formal_Round211_sheet_assignment_ledger"],
        "sheet_assignment_row_id",
        "candidate assignments",
    )
    require(len(assignments) == 17_716, "assignment count")
    seen_sheets = set()
    for row in assignments:
        sheet_id = row["Round211_sheet_row_id"]
        sheet = truth["sheet_by_id"].get(sheet_id)
        require(
            sheet is not None
            and row["sheet_assignment_row_id"]
            == make_id("sheet-assignment", sheet_id)
            and row["Round211_sheet_row_sha256"] == sheet["row_sha256"]
            and row["leaf_row_id"] == sheet["leaf_row_id"]
            and row["known_connectivity_block_id"]
            == truth["sheet_to_block"][sheet_id]
            and row["current_unique_proved_edge_incidence_count"]
            == truth["incident"][sheet_id]
            and row["isolated_under_current_proved_edge_set"]
            == (truth["incident"][sheet_id] == 0)
            and row["maximal_physical_component_assignment_claimed"] is False,
            "assignment semantics",
        )
        seen_sheets.add(sheet_id)
    require(seen_sheets == set(truth["sheet_by_id"]), "assignment coverage")

    frontier_rows = ledger_rows(
        result["formal_unresolved_and_nonedge_frontier_account_ledger"],
        "frontier_account_row_id",
        "candidate frontier accounts",
    )
    require(len(frontier_rows) == len(truth["frontier_expected"]) == 7_280,
            "frontier count")
    seen_frontier = set()
    for row in frontier_rows:
        expected = truth["frontier_expected"].get(row["upstream_row_id"])
        require(
            expected is not None
            and row["frontier_kind"] == expected["kind"]
            and (
                row["left_Round211_sheet_row_id"],
                row["right_Round211_sheet_row_id"],
            ) == expected["pair"]
            and row["upstream_row_sha256"] == expected["row_sha256"]
            and row["same_current_known_connectivity_block"]
            == expected["same"]
            and row["current_quotient_lower_bound_edge_credit"] == 0
            and row["maximal_physical_component_credit"] == 0,
            "frontier row common semantics",
        )
        if expected["kind"] == "ROUND219_INCOMPLETE_EXACT_CONTACT":
            require(
                row["TRACE_edge_already_materialized_on_a_terminal_subface"]
                == expected["direct"]
                and row["UNRESOLVED_terminal_subface_count"]
                == expected["unresolved"]
                and row["contact_partition_complete"] is False
                and row[
                    "same_current_block_does_not_replace_contact_partition"
                ] is True,
                "exact frontier semantics",
            )
        else:
            classification = expected["classification"]
            require(
                row["partial_TRACE_edge_materialized"] is False
                and row["exact_trace_or_absence_proof_missing"]
                == (classification == "UNRESOLVED")
                and row[
                    "potential_future_sheet_block_merge_under_missing_proof"
                ] == (classification == "UNRESOLVED" and not expected["same"]),
                "partial frontier semantics",
            )
        seen_frontier.add(row["upstream_row_id"])
    require(seen_frontier == set(truth["frontier_expected"]),
            "frontier coverage")

    delta = result["old_vs_new_known_connectivity_delta"]
    require(
        delta["raw_Round211_sheet_rows"] == 17_716
        and delta["Round214_old_safe_block_count"] == 12_156
        and delta["Round217_rank_reduction"] == truth["rank"]["Round217"]
        and delta["Round219_rank_reduction"] == truth["rank"]["Round219"]
        and delta["current_known_connectivity_block_count"] == 7_640
        and delta["current_edge_incident_sheet_count"] == 15_248
        and delta["current_edge_isolated_sheet_count"] == 2_468
        and delta["current_known_connectivity_member_sheet_rows_sha256"]
        == digest(sorted(truth["groups"]))
        and delta["maximal_physical_component_count_claimed"] is False
        and delta["component_exhaustion_credit"] == 0,
        "old/new delta",
    )
    trace = result["legacy_curve_endpoint_and_new_trace_strata_audit"]
    require(
        trace["new_p_s_local_trace_incidence_row_count"] == 46_816
        and trace["new_p_s_two_sided_local_trace_block_count"] == 23_408
        and trace["new_p_s_local_trace_block_membership_sha256"]
        == digest(truth["trace_blocks"])
        and trace["endpoint_to_curve_interior_join_count"] == 0
        and trace["p_s_trace_blocks_are_not_maximal_physical_components"]
        is True,
        "trace incidence quotient",
    )
    first = truth["first_missing"]
    frontier_audit = result["frontier_connectivity_audit"]
    claimed_first = frontier_audit["first_missing_frontier"]
    require(
        frontier_audit["Round219_incomplete_exact_contact_count"] == 7_016
        and frontier_audit["Round219_partial_ABSENT_nonedge_count"] == 28
        and frontier_audit["Round219_partial_UNRESOLVED_nonedge_count"] == 236
        and frontier_audit[
            "incomplete_exact_contact_partition_still_required"
        ] is True
        and frontier_audit[
            "incomplete_exact_with_direct_TRACE_edge_count"
        ] == 6_120
        and frontier_audit[
            "incomplete_exact_without_direct_edge_but_same_current_block_count"
        ] == 896
        and frontier_audit[
            "partial_UNRESOLVED_pair_in_distinct_current_blocks_count"
        ] == 236
        and claimed_first["upstream_partial_contact_row_id"] == first[0]
        and (
            claimed_first["left_Round211_sheet_row_id"],
            claimed_first["right_Round211_sheet_row_id"],
        ) == first[1]
        and claimed_first["upstream_partial_contact_row_sha256"] == first[2],
        "first missing frontier",
    )
    nonedge = result["Round216_Round220_boundary_and_nonedge_audit"]
    require(
        nonedge["Round216_exact_key_frontier_row_count"] == 116
        and nonedge["Round220_coordinate_adjacency_nonedge_count"] == 10_384
        and nonedge[
            "Round220_rejected_coordinate_coincidence_nonedge_count"
        ] == 9_830
        and nonedge["Round220_coordinate_adjacency_union_edge_count"] == 0
        and nonedge["Round220_physical_glue_blocker_closed"] is False,
        "Round220 all-coordinate-row nonedge boundary",
    )
    nonpromotion = result["strict_nonpromotion"]
    for key in (
        "formal_component_deduplication_credit",
        "maximal_physical_component_credit",
        "whole_leaf_credit",
        "whole_origin_credit",
        "whole_original_tube_credit",
        "global_component_credit",
        "global_fibre_credit",
        "global_exact_key_disposition_credit",
        "official_source_G_global_disposition_count",
        "global_complete_18_field_blocks",
    ):
        require(nonpromotion[key] == 0, f"zero promotion:{key}")
    require(
        nonpromotion["D02"] == "BLOCKED"
        and nonpromotion["D03_negative_oracle"] == "UNAUTHORIZED"
        and nonpromotion["global_Gate5_fields"] == "10/18"
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "global nonpromotion status",
    )


def reclose_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = digest(row)


def reclose_ledger(value: dict[str, Any], id_key: str) -> None:
    rows = value["rows"]
    value["row_count"] = len(rows)
    value["rows_sha256"] = digest(rows)
    value["row_ids_sha256"] = digest([row[id_key] for row in rows])
    value["row_hashes_sha256"] = digest([row["row_sha256"] for row in rows])


def resign(candidate: dict[str, Any]) -> None:
    candidate["result_sha256"] = digest(candidate["result"])


def semantic_attack_suite(
    candidate: dict[str, Any], truth: dict[str, Any]
) -> dict[str, Any]:
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = []
    edge_key = "formal_Round217_Round219_current_quotient_edge_ledger"
    block_key = "formal_certified_known_connectivity_block_ledger"
    assign_key = "formal_Round211_sheet_assignment_ledger"
    frontier_key = "formal_unresolved_and_nonedge_frontier_account_ledger"

    def mutate_edge_source(value: dict[str, Any]) -> None:
        ledger = value["result"][edge_key]
        ledger["rows"][0]["source_layer"] = "ROUND220_COORDINATE_ADJACENCY"
        reclose_row(ledger["rows"][0]); reclose_ledger(
            ledger, "current_quotient_edge_row_id"
        )

    def mutate_edge_self_loop(value: dict[str, Any]) -> None:
        ledger = value["result"][edge_key]
        row = ledger["rows"][0]
        row["right_Round211_sheet_row_id"] = row["left_Round211_sheet_row_id"]
        row["self_loop"] = True
        reclose_row(row); reclose_ledger(ledger, "current_quotient_edge_row_id")

    def mutate_edge_box_touch(value: dict[str, Any]) -> None:
        ledger = value["result"][edge_key]
        ledger["rows"][0][
            "accepted_from_signature_hash_or_box_touch_alone"
        ] = True
        reclose_row(ledger["rows"][0]); reclose_ledger(
            ledger, "current_quotient_edge_row_id"
        )

    def delete_edge(value: dict[str, Any]) -> None:
        ledger = value["result"][edge_key]
        ledger["rows"].pop(); reclose_ledger(
            ledger, "current_quotient_edge_row_id"
        )

    def duplicate_edge(value: dict[str, Any]) -> None:
        ledger = value["result"][edge_key]
        ledger["rows"].append(copy.deepcopy(ledger["rows"][0]))
        reclose_ledger(ledger, "current_quotient_edge_row_id")

    def mutate_block(value: dict[str, Any]) -> None:
        ledger = value["result"][block_key]
        row = next(row for row in ledger["rows"]
                   if row["member_Round211_sheet_row_count"] > 1)
        row["member_Round211_sheet_row_ids"].pop()
        row["member_Round211_sheet_row_count"] -= 1
        row["member_Round211_sheet_row_ids_sha256"] = digest(
            row["member_Round211_sheet_row_ids"]
        )
        reclose_row(row); reclose_ledger(ledger, "known_connectivity_block_id")

    def mutate_assignment(value: dict[str, Any]) -> None:
        ledger = value["result"][assign_key]
        ledger["rows"][0]["known_connectivity_block_id"] = "forged"
        reclose_row(ledger["rows"][0]); reclose_ledger(
            ledger, "sheet_assignment_row_id"
        )

    def promote_frontier(value: dict[str, Any]) -> None:
        ledger = value["result"][frontier_key]
        row = next(row for row in ledger["rows"]
                   if row["frontier_kind"] == "ROUND219_PARTIAL_UNRESOLVED")
        row["current_quotient_lower_bound_edge_credit"] = 1
        reclose_row(row); reclose_ledger(ledger, "frontier_account_row_id")

    attacks.extend([
        ("ROUND220_COORDINATE_ROW_AS_EDGE", mutate_edge_source),
        ("SELF_LOOP_EDGE", mutate_edge_self_loop),
        ("BOX_TOUCH_FALSE_EDGE", mutate_edge_box_touch),
        ("DELETE_PROVED_EDGE", delete_edge),
        ("DUPLICATE_PROVED_EDGE", duplicate_edge),
        ("ALTER_BLOCK_MEMBERSHIP", mutate_block),
        ("ALTER_SHEET_ASSIGNMENT", mutate_assignment),
        ("PROMOTE_UNRESOLVED_FRONTIER", promote_frontier),
        ("MAPPING_FAILURE_FORGERY", lambda value:
            value["result"]["formal_input_binding"].__setitem__(
                "Round219_leaf_to_Round211_sheet_mapping_failure_count", 1
            )),
        ("MAXIMAL_COMPONENT_CLAIM", lambda value:
            value["result"]["old_vs_new_known_connectivity_delta"].__setitem__(
                "maximal_physical_component_count_claimed", True
            )),
        ("COORDINATE_ADJACENCY_UNION_CREDIT", lambda value:
            value["result"]["Round216_Round220_boundary_and_nonedge_audit"].
            __setitem__("Round220_coordinate_adjacency_union_edge_count", 1)),
        ("GLOBAL_DISPOSITION_CREDIT", lambda value:
            value["result"]["strict_nonpromotion"].__setitem__(
                "global_exact_key_disposition_credit", 1
            )),
        ("WHOLE_ORIGIN_CREDIT", lambda value:
            value["result"]["strict_nonpromotion"].__setitem__(
                "whole_origin_credit", 1
            )),
        ("FALSE_CONTACT_COMPLETION", lambda value:
            value["result"]["frontier_connectivity_audit"].__setitem__(
                "incomplete_exact_contact_partition_still_required", False
            )),
        ("OUTCOME_DEPENDENCY", lambda value:
            value["result"]["formal_input_binding"].__setitem__(
                "producer_outcome_or_oracle_dependency", True
            )),
    ])
    rejected = 0
    for name, mutate in attacks:
        attacked = copy.deepcopy(candidate)
        mutate(attacked)
        resign(attacked)
        require(
            attacked["result_sha256"] == digest(attacked["result"]),
            f"attack truly resigned:{name}",
        )
        try:
            validate_candidate_semantics(attacked, truth)
        except Exception:
            rejected += 1
        else:
            raise VerificationError(f"semantic attack accepted:{name}")
        del attacked
        gc.collect()
    return {
        "attempted": len(attacks),
        "rejected": rejected,
        "old_result_signature_was_not_the_rejection_reason": True,
        "affected_ledger_summaries_recomputed_where_applicable": True,
        "classes": [name for name, _mutate in attacks],
    }


def json_attack_suite(raw: bytes) -> dict[str, int]:
    attacks = [
        b"",
        b"[]\n",
        b"null\n",
        b"\xef\xbb\xbf" + raw,
        raw.replace(b"{", b"{\"schema\":\"duplicate\",", 1),
        raw[:-1] + b" trailing",
        raw.replace(b"false", b"NaN", 1),
        raw + b"\x00",
        b"\xff" + raw,
        b"{\"x\":\"\\ud800\"}\n",
        b"{\"x\":Infinity}\n",
        b"{\"x\":-Infinity}\n",
        b"{\"x\":1,\"x\":2}\n",
        b"{\"x\":1.5}\n",
        b"{}\n{}",
        raw[:-2],
    ]
    rejected = 0
    for index, attack in enumerate(attacks):
        try:
            strict_json(attack, f"attack-{index}")
        except Exception:
            rejected += 1
    require(rejected == len(attacks), "JSON attacks")
    return {"attempted": len(attacks), "rejected": rejected}


def validate_candidate_path(path: Path) -> Path:
    require(not any(part == ".." for part in path.parts), "candidate parent alias")
    absolute = Path(os.path.abspath(os.fspath(path)))
    allowed = (
        absolute.name == CANDIDATE.name
        or (
            absolute.name.startswith(f".{PREFIX}_candidate_replay_")
            and absolute.name.endswith(".json")
        )
    )
    require(
        absolute.parent == HERE and absolute.parent.resolve() == HERE and allowed,
        "candidate directory/allowlist",
    )
    return absolute


def validate_output(path: Path) -> Path:
    require(not any(part == ".." for part in path.parts), "output parent alias")
    absolute = Path(os.path.abspath(os.fspath(path)))
    allowed = (
        absolute.name == OUTPUT.name
        or (
            absolute.name.startswith(f".{PREFIX}_verification_replay_")
            and absolute.name.endswith(".json")
        )
    )
    require(
        absolute.parent == HERE and absolute.parent.resolve() == HERE and allowed,
        "output directory/allowlist",
    )
    protected = {PRODUCER.resolve(), CANDIDATE.resolve(), Path(__file__).resolve()}
    require(absolute.resolve(strict=False) not in protected, "protected output")
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "existing output type",
        )
    return absolute


def safe_write(path: Path, raw: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(raw)
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


def path_attack_suite() -> dict[str, Any]:
    token = str(os.getpid())
    base = HERE / f".{PREFIX}_candidate_replay_attack_{token}.json"
    hard = HERE / f".{PREFIX}_candidate_replay_hard_{token}.json"
    fifo = HERE / f".{PREFIX}_candidate_replay_fifo_{token}.json"
    directory = HERE / f".{PREFIX}_candidate_replay_dir_{token}.json"
    symlink = HERE / f".{PREFIX}_candidate_replay_symlink_{token}.json"
    bad_name = HERE / f".round222_bad_{token}.json"
    output_symlink = HERE / f"{PREFIX}_verification_replay_symlink_{token}.json"
    attempted = rejected = 0

    def expect_reject(action: Callable[[], Any]) -> None:
        nonlocal attempted, rejected
        attempted += 1
        try:
            action()
        except Exception:
            rejected += 1
        else:
            raise VerificationError("path attack accepted")

    try:
        with open(base, "wb") as handle:
            handle.write(b"{}\n")
        os.link(base, hard)
        os.mkfifo(fifo)
        directory.mkdir()
        symlink.symlink_to(CANDIDATE.name)
        bad_name.write_bytes(b"{}\n")
        output_symlink.symlink_to(OUTPUT.name)
        expect_reject(lambda: regular_bytes(symlink))
        expect_reject(lambda: regular_bytes(hard))
        expect_reject(lambda: regular_bytes(fifo))
        expect_reject(lambda: regular_bytes(directory))
        expect_reject(lambda: validate_candidate_path(bad_name))
        expect_reject(
            lambda: validate_candidate_path(HERE / ".." / CANDIDATE.name)
        )
        expect_reject(lambda: validate_output(output_symlink))
        expect_reject(lambda: validate_output(PRODUCER))
        expect_reject(lambda: regular_bytes(base, 1))
        missing = HERE / f".{PREFIX}_candidate_replay_missing_{token}.json"
        expect_reject(lambda: regular_bytes(missing))
    finally:
        for path in (output_symlink, bad_name, symlink, fifo, hard, base):
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        try:
            directory.rmdir()
        except FileNotFoundError:
            pass
    require(attempted == rejected == 10, "path attacks")
    return {
        "attempted": attempted,
        "rejected": rejected,
        "actual_file_object_classes": [
            "symlink", "hardlink", "FIFO", "directory", "missing",
            "bounded-size", "misnamed", "parent-alias",
            "output-symlink", "protected-output",
        ],
    }


def duplicate_literal_key_count(path: Path) -> int:
    import ast

    tree = ast.parse(regular_bytes(path, 5_000_000), filename=str(path))
    duplicates = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        keys = []
        for key in node.keys:
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                keys.append(key.value)
        duplicates += len(keys) - len(set(keys))
    return duplicates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, default=CANDIDATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    pinned(PRODUCER, PRODUCER_SHA256, 5_000_000)
    candidate_path = validate_candidate_path(arguments.candidate)
    raw = regular_bytes(candidate_path, 100 * 1024 * 1024)
    require(
        hashlib.sha256(raw).hexdigest() == CANDIDATE_SHA256,
        "candidate file hash",
    )
    candidate = strict_json(raw, candidate_path.name)
    require(
        candidate.get("result_sha256") == CANDIDATE_RESULT_SHA256,
        "candidate result signature",
    )
    print("Round222 verifier independently reconstructing inputs", file=sys.stderr)
    truth = independent_reconstruction()
    validate_candidate_semantics(candidate, truth)
    semantic_attacks = semantic_attack_suite(candidate, truth)
    json_attacks = json_attack_suite(raw)
    path_attacks = path_attack_suite()
    verifier_sha256 = hashlib.sha256(
        regular_bytes(Path(__file__), 5_000_000)
    ).hexdigest()
    duplicate_keys = {
        "producer": duplicate_literal_key_count(PRODUCER),
        "verifier": duplicate_literal_key_count(Path(__file__)),
    }
    require(duplicate_keys == {"producer": 0, "verifier": 0},
            "duplicate literal keys")
    result = {
        "status": "PASS_PARTIAL_FORMAL_ROUND222",
        "candidate_schema": candidate["schema"],
        "producer_sha256": PRODUCER_SHA256,
        "candidate_file_sha256": CANDIDATE_SHA256,
        "candidate_result_sha256": CANDIDATE_RESULT_SHA256,
        "verifier_sha256": verifier_sha256,
        "producer_imported_or_executed": False,
        "independent_reconstruction": {
            "Round211_sheet_rows": len(truth["sheets"]),
            "Round214_unique_safe_pairs": len(truth["baseline_pairs"]),
            "Round217_unique_TRACE_pairs": len(truth["evidence217"]),
            "Round219_unique_TRACE_pairs": len(truth["evidence219"]),
            "Round217_plus_Round219_unique_TRACE_pairs":
                len(set(truth["evidence217"]) | set(truth["evidence219"])),
            "mapping_failure_count": truth["mapping_failures"],
            "self_loop_count": truth["self_loops"],
            "false_edge_count": truth["false_edges"],
            "known_connectivity_block_count": len(truth["groups"]),
            "known_connectivity_membership_sha256":
                digest(sorted(truth["groups"])),
            "edge_incident_sheet_count":
                sum(value > 0 for value in truth["incident"].values()),
            "isolated_sheet_count":
                17_716 - sum(
                    value > 0 for value in truth["incident"].values()
                ),
            "formal_edge_rows_checked": 7_036,
            "formal_block_rows_checked": 7_640,
            "formal_assignment_rows_checked": 17_716,
            "formal_frontier_rows_checked": 7_280,
            "all_semantically_material_fields_and_formal_rows_checked": True,
        },
        "attack_suite": {
            "truly_resigned_semantic": semantic_attacks,
            "strict_JSON": json_attacks,
            "path_and_file_object": path_attacks,
        },
        "AST_duplicate_literal_dictionary_keys": duplicate_keys,
        "strict_nonpromotion_reconfirmed": {
            "known_connectivity_blocks_are_maximal_physical_components":
                False,
            "physical_component_credit": 0,
            "whole_origin_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical_bytes(verification) + b"\n")
    print(result["status"])
    print(f"result_sha256={verification['result_sha256']}")
    print(f"output={validate_output(arguments.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
