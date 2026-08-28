#!/usr/bin/env python3
"""Cold verifier for the C50a generic codimension owner oracle.

The candidate and request are consumed strictly as data.  This verifier never
imports or executes the C50a producer (or any C41/C32 producer).  It directly
parses the two frozen ledgers, independently replays the versioned history and
binary partitions, then rebuilds face incidence with boundary indexes and
corner germs with a separate point-query pass.  It writes nothing.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable


sys.dont_write_bytecode = True
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
SCHEMA = "cm2.round306c50a.global-codimension-owner-oracle.independent-verifier.v1"
CANDIDATE_SCHEMA = "cm2.round306c50a.global-codimension-owner-oracle.v1"
REQUEST_SCHEMA = CANDIDATE_SCHEMA + ".request"
FACE_SCHEMA = CANDIDATE_SCHEMA + ".face-atom-owner"
CORNER_SCHEMA = CANDIDATE_SCHEMA + ".corner-owner"
PRODUCER_REL = "deliverables/cm2_round306c50a_global_codimension_owner_oracle_v1.py"
PRODUCER = ROOT / PRODUCER_REL

VERSIONS = {
    "occurrence": "CM2_C41_ACTIVE_OVERLAY_OCCURRENCE_V1",
    "split": "CM2_EXACT_TWO_SIDE_BINARY_SPLIT_DECISION_V1",
    "history": "CM2_HASH_CHAINED_ACTIVE_OVERLAY_HISTORY_V1",
    "owner": "CM2_FULL_UNIVERSE_FACE_CORNER_OWNER_V1",
}
OWNER_RULE = "UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH"

C32_REL = ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
C41_REL = ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C32_DIR, C41_DIR = ROOT / C32_REL, ROOT / C41_REL
C32_LEDGER, C41_LEDGER = C32_DIR / "compact_cells.jsonl.gz", C41_DIR / "routed_ambient_cells.jsonl.gz"
C32_RESULT, C41_RESULT = C32_DIR / "result.json", C41_DIR / "result.json"
C32_MANIFEST, C41_MANIFEST = C32_DIR / "root_manifest.sha256", C41_DIR / "root_manifest.sha256"

C32_OBJECT = "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474"
C41_OBJECT = "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
C32_RESULT_HASH = "c2abba977fa21ea965a9d77478df391db496d0e03f60320b9a4adf9005f1a0a4"
C41_RESULT_HASH = "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f"
C32_MANIFEST_HASH = "4af827cfec996f62443b9ef38ea71cd341873de58b9b04cedfcd8faaca70a8e1"
C41_MANIFEST_HASH = "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba"
C32_LEDGER_HASH = "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8"
C41_LEDGER_HASH = "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8"
C32_COUNT, C41_COUNT = 76_832, 91_879
C32_SEQUENCE = "e2f33100491adadda1045c37be735a80cc8bc7e914132b5647e3df13913ac726"
C41_SEQUENCE = "934d5ca55ee2deb33a066d948af9e3f0a85e09088d97254a579a06c3f62b8045"


class Deny(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Deny(label)


def encoded(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def h(value: Any) -> str:
    return hashlib.sha256(encoded(value)).hexdigest()


def seq(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        require(type(value) is str, "digest sequence string")
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


ACTIVE = {
    "schema": CANDIDATE_SCHEMA + ".active-universe-binding",
    "C32": {
        "authority_object_sha256": C32_OBJECT,
        "result_path": C32_REL + "/result.json",
        "result_file_sha256": C32_RESULT_HASH,
        "root_manifest_path": C32_REL + "/root_manifest.sha256",
        "root_manifest_file_sha256": C32_MANIFEST_HASH,
        "cell_ledger_path": C32_REL + "/compact_cells.jsonl.gz",
        "cell_ledger_file_sha256": C32_LEDGER_HASH,
        "cell_row_count": C32_COUNT,
        "cell_row_sequence_sha256": C32_SEQUENCE,
    },
    "C41": {
        "authority_object_sha256": C41_OBJECT,
        "result_path": C41_REL + "/result.json",
        "result_file_sha256": C41_RESULT_HASH,
        "root_manifest_path": C41_REL + "/root_manifest.sha256",
        "root_manifest_file_sha256": C41_MANIFEST_HASH,
        "ambient_ledger_path": C41_REL + "/routed_ambient_cells.jsonl.gz",
        "ambient_ledger_file_sha256": C41_LEDGER_HASH,
        "ambient_row_count": C41_COUNT,
        "ambient_row_sequence_sha256": C41_SEQUENCE,
    },
}
ACTIVE_HASH = h(ACTIVE)
GENESIS = {
    "schema": CANDIDATE_SCHEMA + ".history-genesis",
    "history_protocol_version": VERSIONS["history"],
    "active_universe_binding_sha256": ACTIVE_HASH,
    "genesis_kind": "FROZEN_C41_91879_ROW_TWO_SIDE_ACTIVE_UNIVERSE",
}
GENESIS_HASH = h(GENESIS)


def hash_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def read_stable(path: Path, label: str, maximum: int = 512 << 20) -> tuple[bytes, tuple[int, ...]]:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                 | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
                "regular singleton:" + label)
        require(0 < before.st_size <= maximum, "bounded file:" + label)
        pieces, remaining = [], before.st_size
        while remaining:
            piece = os.read(fd, min(2 << 20, remaining))
            require(bool(piece), "short read:" + label)
            pieces.append(piece)
            remaining -= len(piece)
        require(os.read(fd, 1) == b"", "EOF:" + label)
        after = os.fstat(fd)
    finally:
        os.close(fd)
    identity = lambda row: (row.st_dev, row.st_ino, row.st_mode, row.st_nlink,
                            row.st_uid, row.st_gid, row.st_size, row.st_mtime_ns,
                            row.st_ctime_ns)
    require(identity(before) == identity(after), "TOCTOU:" + label)
    return b"".join(pieces), identity(after)


def parse(raw: bytes, label: str, *, canonical_line: bool = False) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
            "JSON bytes:" + label)

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            require(key not in output, "duplicate key:" + label + ":" + key)
            output[key] = value
        return output

    def reject_number(token: str) -> Any:
        raise Deny("noninteger JSON number:" + token)

    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs,
                       parse_float=reject_number, parse_constant=reject_number)
    require(type(value) is dict, "JSON object:" + label)
    if canonical_line:
        require(raw == encoded(value) + b"\n", "canonical JSON line:" + label)
    return value


def self_hash(value: dict[str, Any], key: str, label: str) -> None:
    require(type(value.get(key)) is str, "self hash field:" + label)
    require(value[key] == h({name: item for name, item in value.items() if name != key}),
            "self hash:" + label)


def keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    require(type(value) is dict and set(value) == expected, "exact keys:" + label)


def fraction(text: str, label: str) -> Q:
    require(type(text) is str and 0 < len(text) <= 256, "rational text:" + label)
    value = Q(text)
    require(str(value) == text, "canonical rational:" + label)
    return value


def span(raw: list[str], label: str, positive: bool = False) -> tuple[Q, Q]:
    require(type(raw) is list and len(raw) == 2, "span shape:" + label)
    low, high = fraction(raw[0], label + " low"), fraction(raw[1], label + " high")
    require(low < high if positive else low <= high, "span order:" + label)
    return low, high


def box(raw: dict[str, Any], label: str) -> tuple[Q, Q, Q, Q]:
    keys(raw, {"compact_chart", "t", "p", "s"}, label)
    require(raw["compact_chart"] in {"E", "W", "N", "S"}, "box chart")
    t0, t1 = span(raw["t"], label + " t", True)
    p0, p1 = span(raw["p"], label + " p", True)
    s0, s1 = span(raw["s"], label + " s")
    require(s0 == s1 == 0, "box slice")
    return t0, t1, p0, p1


def frozen_files() -> list[dict[str, Any]]:
    pins = ((C32_RESULT, C32_RESULT_HASH), (C41_RESULT, C41_RESULT_HASH),
            (C32_MANIFEST, C32_MANIFEST_HASH), (C41_MANIFEST, C41_MANIFEST_HASH),
            (C32_LEDGER, C32_LEDGER_HASH), (C41_LEDGER, C41_LEDGER_HASH),
            (PRODUCER, None))
    snapshot = []
    for path, expected in pins:
        raw, identity = read_stable(path, str(path.relative_to(ROOT)))
        observed = hashlib.sha256(raw).hexdigest()
        if expected is not None:
            require(observed == expected, "frozen hash:" + str(path.relative_to(ROOT)))
        snapshot.append({"path": str(path.relative_to(ROOT)), "sha256": observed,
                         "identity": list(identity)})
    for path, expected in ((C32_RESULT, C32_OBJECT), (C41_RESULT, C41_OBJECT)):
        raw, _ = read_stable(path, "authority result")
        value = parse(raw, "authority result")
        self_hash(value, "object_sha256", "authority result")
        require(value["object_sha256"] == expected, "authority object")
    return snapshot


def rows(path: Path, file_hash: str, count: int, sequence: str,
         label: str) -> list[dict[str, Any]]:
    compressed, _ = read_stable(path, label)
    require(hashlib.sha256(compressed).hexdigest() == file_hash, "ledger hash:" + label)
    output, row_hashes = [], []
    with gzip.GzipFile(fileobj=io.BytesIO(compressed), mode="rb") as stream:
        for ordinal, line in enumerate(stream):
            row = parse(line, f"{label}[{ordinal}]", canonical_line=True)
            require(type(row.get("row_sha256")) is str, "row hash:" + label)
            output.append(row)
            row_hashes.append(row["row_sha256"])
    require(len(output) == count and seq(row_hashes) == sequence,
            "ledger census/sequence:" + label)
    return output


def make_occurrence(body: dict[str, Any]) -> dict[str, Any]:
    binding = h(body)
    output = {**body, "occurrence_binding_sha256": binding,
              "physical_occurrence_id": "c50a-occurrence:" + binding}
    raw_box = body["exact_closed_box"]
    if raw_box is None:
        env = body["nonrational_exclusion_envelope"]
        t0, t1 = span(env["t"], "unknown t", True)
        p0, p1 = span(env["p"], "unknown p", True)
        output.update({"rational": False, "t0": None, "t1": None,
                       "p0": None, "p1": None, "env_t0": t0, "env_t1": t1,
                       "env_p0": p0, "env_p1": p1})
    else:
        t0, t1, p0, p1 = box(raw_box, "occurrence")
        output.update({"rational": True, "t0": t0, "t1": t1,
                       "p0": p0, "p1": p1})
    return output


def reconstruct_base() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    cell_rows = rows(C32_LEDGER, C32_LEDGER_HASH, C32_COUNT, C32_SEQUENCE, "C32 ledger")
    cells: dict[str, dict[str, Any]] = {}
    for row in cell_rows:
        require(row["schema"] == "cm2.round306c32.d02-four-chart-compact-atlas-cell.v1",
                "C32 schema")
        cell_id, chart = row["cell_id"], row["compact_chart"]
        require(cell_id not in cells and chart in {"E", "W", "N", "S"},
                "C32 identity/chart")
        t0, t1 = span(row["gate3_product_box"]["t"], "C32 envelope t", True)
        p0, p1 = span(row["gate3_product_box"]["p"], "C32 envelope p", True)
        cells[cell_id] = {"chart": chart, "envelope": {
            "compact_chart": chart, "t": [str(t0), str(t1)],
            "p": [str(p0), str(p1)]}}
    ambient_rows = rows(C41_LEDGER, C41_LEDGER_HASH, C41_COUNT, C41_SEQUENCE, "C41 ledger")
    ambient_index, output = {}, []
    for ambient in ambient_rows:
        require(ambient["schema"] == "cm2.round306c41.d02-lower-strata-depth3-closure.v1.routed-ambient-cell",
                "C41 schema")
        ambient_id = ambient["c41_ambient_cell_id"]
        require(ambient_id not in ambient_index, "ambient uniqueness")
        ambient_index[ambient_id] = ambient
        for side, cell_key, box_key in (
            ("REPRESENTATIVE", "representative_cell_id", "closed_representative_box"),
            ("REFLECTED", "reflected_cell_id", "closed_reflected_box"),
        ):
            cell_id = ambient[cell_key]
            require(cell_id in cells, "ambient cell foreign key")
            chart = cells[cell_id]["chart"]
            raw_box = ambient[box_key]
            if raw_box is None:
                normalized, env = None, cells[cell_id]["envelope"]
            else:
                normalized = dict(raw_box)
                if side == "REPRESENTATIVE":
                    normalized = {"compact_chart": chart, **normalized}
                require(normalized["compact_chart"] == chart, "ambient chart")
                box(normalized, "ambient box")
                env = None
            body = {
                "occurrence_protocol_version": VERSIONS["occurrence"],
                "active_universe_binding_sha256": ACTIVE_HASH,
                "history_parent_sha256": GENESIS_HASH,
                "transaction_binding_sha256": None,
                "source_kind": "C41_BASELINE", "side": side,
                "pair_index": ambient["pair_index"], "semantic_path": ambient["path"],
                "physical_route_path": None, "physical_cell_id": cell_id,
                "compact_chart": chart, "exact_closed_box": normalized,
                "nonrational_exclusion_envelope": env,
                "upstream_ambient_cell_id": ambient_id,
                "upstream_ambient_row_sha256": ambient["row_sha256"],
                "upstream_split_axis_history": ambient["split_axis_history"],
                "upstream_disposition_family": ambient["disposition_family"],
                "upstream_task_binding_sha256": None, "relative_path": None,
                "source_evidence": None,
            }
            output.append(make_occurrence(body))
    require(len(output) == 183_758 and sum(row["rational"] for row in output) == 183_700,
            "baseline occurrence census")
    require(len({row["physical_occurrence_id"] for row in output}) == len(output),
            "baseline identity uniqueness")
    replay = {
        "C32_cell_count": len(cells), "C41_ambient_row_count": len(ambient_index),
        "baseline_physical_occurrence_count": len(output),
        "baseline_exact_rational_occurrence_count": sum(row["rational"] for row in output),
        "baseline_nonrational_enveloped_occurrence_count": sum(not row["rational"] for row in output),
        "baseline_occurrence_binding_sequence_sha256": seq(sorted(
            row["occurrence_binding_sha256"] for row in output)),
        "full_pinned_active_universe_scanned": True,
    }
    return output, ambient_index, replay


def extent(items: list[dict[str, Any]]) -> tuple[Q, Q, Q, Q]:
    require(bool(items), "nonempty extent")
    return (min(row["t0"] for row in items), max(row["t1"] for row in items),
            min(row["p0"] for row in items), max(row["p1"] for row in items))


def measure(value: tuple[Q, Q, Q, Q]) -> Q:
    return (value[1] - value[0]) * (value[3] - value[2])


def internal_prefixes(frontier: list[str]) -> set[str]:
    return {path[:depth] for path in frontier for depth in range(len(path))}


def validate_partition(task: dict[str, Any], tx: dict[str, Any],
                       predecessors: dict[str, dict[str, Any]]) -> str:
    frontier = tx["relative_frontier"]
    require(type(frontier) is list and frontier == sorted(set(frontier)) and bool(frontier),
            "frontier ordering")
    require(all(type(path) is str and path and set(path) <= {"0", "1"} for path in frontier),
            "binary frontier")
    require(not any(b.startswith(a) for a in frontier for b in frontier if a != b),
            "prefix-free frontier")
    require(sum((Q(1, 2 ** len(path)) for path in frontier), Q(0)) == 1, "Kraft one")
    internals = internal_prefixes(frontier)
    require(all(any(path.startswith(prefix + "0") for path in frontier)
                and any(path.startswith(prefix + "1") for path in frontier)
                for prefix in internals), "full binary frontier")
    replacement = tx["replacements"]
    require(type(replacement) is list and len(replacement) == 2 * len(frontier),
            "replacement census")
    maps: dict[str, dict[str, dict[str, Any]]] = {}
    for side in ("REPRESENTATIVE", "REFLECTED"):
        chosen = [row for row in replacement if row.get("side") == side]
        require(sorted(row["relative_path"] for row in chosen) == frontier,
                "side frontier:" + side)
        mapping = {}
        for row in chosen:
            rel = row["relative_path"]
            require(row["semantic_path"] == task["root_semantic_path"] + rel,
                    "semantic path binding")
            require(row["physical_cell_id"] == predecessors[side]["physical_cell_id"],
                    "physical cell binding")
            require(row["exact_closed_box"]["compact_chart"] == predecessors[side]["compact_chart"],
                    "chart binding")
            t0, t1, p0, p1 = box(row["exact_closed_box"], "replacement")
            require(fraction(row["relative_parent_fraction"], "relative fraction")
                    == Q(1, 2 ** len(rel)), "relative fraction")
            require(type(row["source_evidence"]) is dict
                    and row["source_evidence"].get("formal_credit") == 0,
                    "zero-credit evidence")
            mapping[rel] = {**row, "t0": t0, "t1": t1, "p0": p0, "p1": p1}
        values = list(mapping.values())
        for index, left in enumerate(values):
            for right in values[index + 1:]:
                dt = min(left["t1"], right["t1"]) - max(left["t0"], right["t0"])
                dp = min(left["p1"], right["p1"]) - max(left["p0"], right["p0"])
                require(dt <= 0 or dp <= 0, "replacement interior overlap")
        root = extent(values)
        require(predecessors[side]["exact_closed_box"] is not None
                and root == box(predecessors[side]["exact_closed_box"], "predecessor"),
                "root box conservation")
        require(sum(measure((row["t0"], row["t1"], row["p0"], row["p1"]))
                    for row in values) == measure(root), "root area conservation")
        maps[side] = mapping
    events = tx["split_decisions"]
    require(type(events) is list and len(events) == 2 * len(internals),
            "split event census")
    event_map = {}
    for event in events:
        self_hash(event, "split_decision_sha256", "split event")
        require(event["split_protocol_version"] == VERSIONS["split"], "split version")
        side, parent = event["side"], event["logical_parent_prefix"]
        require(side in maps and parent in internals and (side, parent) not in event_map,
                "event side/parent")
        children = {parent + "0", parent + "1"}
        lower, upper = (event["lower_coordinate_logical_child_prefix"],
                        event["upper_coordinate_logical_child_prefix"])
        require({lower, upper} == children, "logical children")
        physical_parent = event["physical_parent_path"]
        require({event["lower_coordinate_physical_child_path"],
                 event["upper_coordinate_physical_child_path"]}
                == {physical_parent + "0", physical_parent + "1"}, "physical children")
        require(event["half_open_owner_logical_child_prefix"] in children,
                "half-open child")
        event_map[(side, parent)] = event
    event_hashes = []
    for side, mapping in maps.items():
        physical = {"": event_map[(side, "")]["physical_parent_path"]}
        for parent in sorted(internals, key=lambda item: (len(item), item)):
            event = event_map[(side, parent)]
            require(event["physical_parent_path"] == physical[parent], "physical history")
            low_key = event["lower_coordinate_logical_child_prefix"]
            high_key = event["upper_coordinate_logical_child_prefix"]
            physical[low_key] = event["lower_coordinate_physical_child_path"]
            physical[high_key] = event["upper_coordinate_physical_child_path"]
            low_rows = [row for rel, row in mapping.items() if rel.startswith(low_key)]
            high_rows = [row for rel, row in mapping.items() if rel.startswith(high_key)]
            low_box, high_box = extent(low_rows), extent(high_rows)
            coordinate = fraction(event["coordinate"], "split coordinate")
            if event["axis"] == "t":
                require(low_box[1] == high_box[0] == coordinate
                        and low_box[2:] == high_box[2:], "t split")
            elif event["axis"] == "p":
                require(low_box[3] == high_box[2] == coordinate
                        and low_box[:2] == high_box[:2], "p split")
            else:
                raise Deny("split axis")
            parent_rows = low_rows + high_rows
            require(measure(extent(parent_rows)) == sum(
                measure((row["t0"], row["t1"], row["p0"], row["p1"]))
                for row in parent_rows), "subtree conservation")
            event_hashes.append(event["split_decision_sha256"])
        for rel, row in mapping.items():
            require(row["physical_route_path"] == physical[rel], "physical leaf history")
    return seq(sorted(event_hashes))


def find_predecessor(locator: dict[str, Any], side: str,
                     active: dict[str, dict[str, Any]]) -> dict[str, Any]:
    require(locator["side"] == side, "locator side")
    if locator["locator_kind"] == "C41_AMBIENT_SIDE":
        selected = [row for row in active.values()
                    if row["source_kind"] == "C41_BASELINE" and row["side"] == side
                    and row["upstream_ambient_cell_id"] == locator["upstream_ambient_cell_id"]
                    and row["upstream_ambient_row_sha256"] == locator["upstream_ambient_row_sha256"]]
    elif locator["locator_kind"] == "ACTIVE_OCCURRENCE_ID":
        row = active.get(locator["physical_occurrence_id"])
        selected = [] if row is None or row["side"] != side else [row]
    else:
        raise Deny("locator kind")
    require(len(selected) == 1, "unique active predecessor")
    return selected[0]


def replay_request(request: dict[str, Any], baseline: list[dict[str, Any]]) \
        -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], str]:
    self_hash(request, "request_object_sha256", "request")
    require(request["schema"] == REQUEST_SCHEMA and request["protocol_versions"] == VERSIONS,
            "request schema/versions")
    require(request["active_universe"] == ACTIVE
            and request["active_universe_binding_sha256"] == ACTIVE_HASH,
            "request universe")
    require(request["history_genesis"] == GENESIS
            and request["history_genesis_sha256"] == GENESIS_HASH,
            "request genesis")
    require(request["formal_credit"] == 0, "request credit")
    transactions = request["transactions"]
    require(type(transactions) is list and 0 < len(transactions) <= 1000,
            "transaction history bound")
    active = {row["physical_occurrence_id"]: row for row in baseline}
    head, history, inserted_by_tx = GENESIS_HASH, [], {}
    for index, tx in enumerate(transactions):
        self_hash(tx, "transaction_binding_sha256", "transaction")
        require(tx["transaction_index"] == index and tx["parent_history_sha256"] == head,
                "transaction index/parent")
        task = tx["task"]
        self_hash(task, "oracle_task_binding_sha256", "task")
        require(type(task["pair_index"]) is int and task["pair_index"] >= 0,
                "pair index")
        locators = task["predecessors"]
        require(type(locators) is list and len(locators) == 2
                and {row["side"] for row in locators} == {"REPRESENTATIVE", "REFLECTED"},
                "two locator sides")
        predecessor = {side: find_predecessor(
            next(row for row in locators if row["side"] == side), side, active)
            for side in ("REPRESENTATIVE", "REFLECTED")}
        require(all(row["pair_index"] == task["pair_index"]
                    and row["semantic_path"] == task["root_semantic_path"]
                    for row in predecessor.values()), "task predecessor binding")
        split_sequence = validate_partition(task, tx, predecessor)
        removed = sorted(row["physical_occurrence_id"] for row in predecessor.values())
        require(len(set(removed)) == 2, "distinct predecessor pair")
        for occurrence_id in removed:
            del active[occurrence_id]
        inserted = []
        for spec in tx["replacements"]:
            source = predecessor[spec["side"]]
            body = {
                "occurrence_protocol_version": VERSIONS["occurrence"],
                "active_universe_binding_sha256": ACTIVE_HASH,
                "history_parent_sha256": head,
                "transaction_binding_sha256": tx["transaction_binding_sha256"],
                "source_kind": "HISTORY_REPLACEMENT", "side": spec["side"],
                "pair_index": task["pair_index"], "semantic_path": spec["semantic_path"],
                "physical_route_path": spec["physical_route_path"],
                "physical_cell_id": spec["physical_cell_id"],
                "compact_chart": spec["exact_closed_box"]["compact_chart"],
                "exact_closed_box": spec["exact_closed_box"],
                "nonrational_exclusion_envelope": None,
                "upstream_ambient_cell_id": source["upstream_ambient_cell_id"],
                "upstream_ambient_row_sha256": source["upstream_ambient_row_sha256"],
                "upstream_split_axis_history": None, "upstream_disposition_family": None,
                "upstream_task_binding_sha256": task["upstream_task_binding_sha256"],
                "relative_path": spec["relative_path"],
                "source_evidence": spec["source_evidence"],
            }
            row = make_occurrence(body)
            require(row["physical_occurrence_id"] not in active, "insert identity")
            active[row["physical_occurrence_id"]] = row
            inserted.append(row)
        overlay_hash = seq(sorted(row["occurrence_binding_sha256"] for row in active.values()))
        node_body = {
            "schema": CANDIDATE_SCHEMA + ".history-node",
            "history_protocol_version": VERSIONS["history"],
            "active_universe_binding_sha256": ACTIVE_HASH,
            "transaction_index": index, "parent_history_sha256": head,
            "transaction_binding_sha256": tx["transaction_binding_sha256"],
            "oracle_task_binding_sha256": task["oracle_task_binding_sha256"],
            "split_decision_sequence_sha256": split_sequence,
            "removed_occurrence_id_sequence_sha256": seq(removed),
            "inserted_occurrence_id_sequence_sha256": seq(sorted(
                row["physical_occurrence_id"] for row in inserted)),
            "resulting_overlay_occurrence_binding_sequence_sha256": overlay_hash,
            "resulting_overlay_occurrence_count": len(active),
        }
        next_head = h(node_body)
        history.append({**node_body, "history_node_sha256": next_head,
                        "removed_occurrence_ids": removed,
                        "inserted_occurrence_ids": sorted(
                            row["physical_occurrence_id"] for row in inserted)})
        inserted_by_tx[index] = inserted
        head = next_head
    target_indices = request["target_transaction_indices"]
    require(type(target_indices) is list and target_indices == sorted(set(target_indices))
            and all(index in inserted_by_tx for index in target_indices),
            "target transaction indices")
    mode = request["target_mode"]
    require(mode in {"TRANSACTION_INSERTIONS_STILL_ACTIVE",
                     "ALL_ACTIVE_HISTORY_REPLACEMENTS"}, "target mode")
    require((mode == "TRANSACTION_INSERTIONS_STILL_ACTIVE" and bool(target_indices))
            or (mode == "ALL_ACTIVE_HISTORY_REPLACEMENTS" and target_indices == []),
            "target mode/index contract")
    if mode == "ALL_ACTIVE_HISTORY_REPLACEMENTS":
        target = [row for row in active.values()
                  if row["source_kind"] == "HISTORY_REPLACEMENT"]
        target.sort(key=lambda row: row["physical_occurrence_id"])
    else:
        target = [row for index in target_indices for row in inserted_by_tx[index]]
    require(all(row["physical_occurrence_id"] in active for row in target),
            "active targets")
    return list(active.values()), history, target, head


def positive_overlap(a0: Q, a1: Q, b0: Q, b1: Q) -> tuple[Q, Q] | None:
    low, high = max(a0, b0), min(a1, b1)
    return (low, high) if low < high else None


def compact(row: dict[str, Any], *, side: str | None = None,
            occupied: list[str] | None = None) -> dict[str, Any]:
    output = {
        "physical_occurrence_id": row["physical_occurrence_id"],
        "occurrence_binding_sha256": row["occurrence_binding_sha256"],
        "occurrence_protocol_version": row["occurrence_protocol_version"],
        "history_parent_sha256": row["history_parent_sha256"],
        "transaction_binding_sha256": row["transaction_binding_sha256"],
        "source_kind": row["source_kind"], "side": row["side"],
        "pair_index": row["pair_index"], "semantic_path": row["semantic_path"],
        "physical_route_path": row["physical_route_path"],
        "physical_cell_id": row["physical_cell_id"],
        "upstream_task_binding_sha256": row["upstream_task_binding_sha256"],
        "relative_path": row["relative_path"],
    }
    if side is not None:
        output["geometric_side"] = side
    if occupied is not None:
        output["occupied_quadrants"] = sorted(occupied)
    return output


def unique_owner(incidents: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, bool]:
    require(bool(incidents), "nonempty incidents")
    minimum = min(row["semantic_path"] for row in incidents)
    selected = [row for row in incidents if row["semantic_path"] == minimum]
    return (selected[0], True) if len(selected) == 1 else (None, False)


def boundary_indexes(overlay: list[dict[str, Any]]) -> tuple[dict[tuple[str, str, Q, str], list[dict[str, Any]]], list[dict[str, Any]]]:
    index: dict[tuple[str, str, Q, str], list[dict[str, Any]]] = {}
    unknown = []
    for row in overlay:
        if not row["rational"]:
            unknown.append(row)
            continue
        chart = row["compact_chart"]
        for key in ((chart, "t", row["t1"], "LOWER_COORDINATE_SIDE"),
                    (chart, "t", row["t0"], "UPPER_COORDINATE_SIDE"),
                    (chart, "p", row["p1"], "LOWER_COORDINATE_SIDE"),
                    (chart, "p", row["p0"], "UPPER_COORDINATE_SIDE")):
            index.setdefault(key, []).append(row)
    return index, unknown


def target_boundaries(targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in targets:
        for name, axis, fixed, low, high in (
            ("t_lower", "t", row["t0"], row["p0"], row["p1"]),
            ("t_upper", "t", row["t1"], row["p0"], row["p1"]),
            ("p_lower", "p", row["p0"], row["t0"], row["t1"]),
            ("p_upper", "p", row["p1"], row["t0"], row["t1"]),
        ):
            output.append({"target_occurrence_id": row["physical_occurrence_id"],
                           "face": name, "chart": row["compact_chart"],
                           "axis": axis, "fixed": fixed, "low": low, "high": high})
    return output


def incident_extent(row: dict[str, Any], axis: str, low: Q, high: Q) -> tuple[Q, Q] | None:
    return (positive_overlap(low, high, row["p0"], row["p1"])
            if axis == "t" else positive_overlap(low, high, row["t0"], row["t1"]))


def unknown_face_safe(row: dict[str, Any], chart: str, axis: str,
                      fixed: Q, low: Q, high: Q) -> bool:
    if row["compact_chart"] != chart:
        return True
    if axis == "t":
        possible = row["env_t0"] <= fixed <= row["env_t1"] and positive_overlap(
            low, high, row["env_p0"], row["env_p1"]) is not None
    else:
        possible = row["env_p0"] <= fixed <= row["env_p1"] and positive_overlap(
            low, high, row["env_t0"], row["env_t1"]) is not None
    return not possible


def rebuild_faces(overlay: list[dict[str, Any]], targets: list[dict[str, Any]]) \
        -> tuple[list[dict[str, Any]], int]:
    index, unknown = boundary_indexes(overlay)
    atom_targets: dict[tuple[str, str, Q, Q, Q], list[dict[str, Any]]] = {}
    target_count = 0
    for target in target_boundaries(targets):
        breaks = {target["low"], target["high"]}
        for geometric_side in ("LOWER_COORDINATE_SIDE", "UPPER_COORDINATE_SIDE"):
            for row in index.get((target["chart"], target["axis"],
                                  target["fixed"], geometric_side), []):
                found = incident_extent(row, target["axis"], target["low"], target["high"])
                if found is not None:
                    breaks.update(found)
        ordered = sorted(breaks)
        for low, high in zip(ordered, ordered[1:]):
            if low == high:
                continue
            key = (target["chart"], target["axis"], target["fixed"], low, high)
            reference = {"target_occurrence_id": target["target_occurrence_id"],
                         "face": target["face"]}
            atom_targets.setdefault(key, [])
            if reference not in atom_targets[key]:
                atom_targets[key].append(reference)
            target_count += 1
    result = []
    for key in sorted(atom_targets, key=lambda item: tuple(map(str, item))):
        chart, axis, fixed, low, high = key
        pairs = []
        side_rows = {}
        for geometric_side in ("LOWER_COORDINATE_SIDE", "UPPER_COORDINATE_SIDE"):
            selected = []
            for row in index.get((chart, axis, fixed, geometric_side), []):
                found = incident_extent(row, axis, low, high)
                if found is not None and found[0] <= low and high <= found[1]:
                    selected.append(row)
                    pairs.append((row, geometric_side))
            side_rows[geometric_side] = selected
        pairs.sort(key=lambda item: item[0]["physical_occurrence_id"])
        compact_rows = [compact(row, side=geometric_side) for row, geometric_side in pairs]
        selected_owner, owner_unique = unique_owner(compact_rows)
        unknown_safe = all(unknown_face_safe(row, chart, axis, fixed, low, high)
                           for row in unknown)
        complete = unknown_safe and all(len(value) == 1 for value in side_rows.values())
        geometry = {"compact_chart": chart,
                    "t": [str(fixed), str(fixed)] if axis == "t" else [str(low), str(high)],
                    "p": [str(low), str(high)] if axis == "t" else [str(fixed), str(fixed)],
                    "s": ["0", "0"]}
        body = {
            "schema": FACE_SCHEMA, "owner_protocol_version": VERSIONS["owner"],
            "active_universe_binding_sha256": ACTIVE_HASH,
            "canonical_entity_key": {"compact_chart": chart,
                                     "exact_closed_face_box": geometry},
            "axis": axis,
            "target_occurrence_face_references": sorted(
                atom_targets[key], key=lambda row: (row["target_occurrence_id"], row["face"])),
            "positive_length_face_overlap_only": True,
            "incident_occurrence_count": len(compact_rows),
            "incident_occurrences": compact_rows,
            "incident_occurrence_binding_sequence_sha256": seq(
                row["occurrence_binding_sha256"] for row in compact_rows),
            "geometric_side_counts": {name: len(value) for name, value in side_rows.items()},
            "nonrational_envelope_exclusion_count": len(unknown),
            "all_nonrational_occurrences_proven_disjoint": unknown_safe,
            "incident_set_complete": complete, "owner_rule": OWNER_RULE,
            "owner_unique": owner_unique, "owner": selected_owner, "formal_credit": 0,
        }
        result.append({**body, "face_atom_id": "c50a-face:" + h(body)})
    return result, target_count


QUADRANTS = (("t-_p-", -1, -1), ("t-_p+", -1, 1),
             ("t+_p-", 1, -1), ("t+_p+", 1, 1))


def point_quadrants(row: dict[str, Any], t: Q, p: Q) -> list[str]:
    if not row["rational"]:
        return []
    output = []
    for name, tsign, psign in QUADRANTS:
        t_ok = row["t0"] < t <= row["t1"] if tsign < 0 else row["t0"] <= t < row["t1"]
        p_ok = row["p0"] < p <= row["p1"] if psign < 0 else row["p0"] <= p < row["p1"]
        if t_ok and p_ok:
            output.append(name)
    return output


def rebuild_corners(overlay: list[dict[str, Any]], targets: list[dict[str, Any]],
                    faces: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    points: set[tuple[str, Q, Q]] = set()
    for face in faces:
        raw = face["canonical_entity_key"]["exact_closed_face_box"]
        chart = raw["compact_chart"]
        if face["axis"] == "t":
            points.add((chart, Q(raw["t"][0]), Q(raw["p"][0])))
            points.add((chart, Q(raw["t"][0]), Q(raw["p"][1])))
        else:
            points.add((chart, Q(raw["t"][0]), Q(raw["p"][0])))
            points.add((chart, Q(raw["t"][1]), Q(raw["p"][0])))
    unknown = [row for row in overlay if not row["rational"]]
    output, target_corner_count = [], 0
    for chart, t, p in sorted(points, key=lambda item: tuple(map(str, item))):
        boundary, target_corners = [], []
        for target in targets:
            if target["compact_chart"] != chart:
                continue
            if target["t0"] <= t <= target["t1"] and target["p0"] <= p <= target["p1"] \
                    and (t in {target["t0"], target["t1"]}
                         or p in {target["p0"], target["p1"]}):
                boundary.append(target["physical_occurrence_id"])
            if t in {target["t0"], target["t1"]} and p in {target["p0"], target["p1"]}:
                target_corners.append(target["physical_occurrence_id"])
                target_corner_count += 1
        pairs, qmap = [], {name: [] for name, _t, _p in QUADRANTS}
        for row in overlay:
            if row["compact_chart"] != chart:
                continue
            occupied = point_quadrants(row, t, p)
            if occupied:
                pairs.append((row, occupied))
                for quadrant in occupied:
                    qmap[quadrant].append(row["physical_occurrence_id"])
        pairs.sort(key=lambda item: item[0]["physical_occurrence_id"])
        incidents = [compact(row, occupied=occupied) for row, occupied in pairs]
        selected_owner, owner_unique = unique_owner(incidents)
        unknown_safe = all(row["compact_chart"] != chart
                           or not (row["env_t0"] <= t <= row["env_t1"]
                                   and row["env_p0"] <= p <= row["env_p1"])
                           for row in unknown)
        complete = unknown_safe and all(len(value) == 1 for value in qmap.values())
        count = len(incidents)
        kind = {1: "SINGLE_CELL_CORNER", 2: "TWO_CELL_FACE_VERTEX",
                3: "THREE_WAY_T_JUNCTION", 4: "FOUR_WAY_CROSS_JUNCTION"}.get(
                    count, "OTHER_INCIDENT_CENSUS")
        body = {
            "schema": CORNER_SCHEMA, "owner_protocol_version": VERSIONS["owner"],
            "active_universe_binding_sha256": ACTIVE_HASH,
            "canonical_entity_key": {"compact_chart": chart,
                "exact_closed_corner_box": {"compact_chart": chart,
                    "t": [str(t), str(t)], "p": [str(p), str(p)], "s": ["0", "0"]}},
            "junction_kind": kind,
            "target_boundary_occurrence_ids": sorted(boundary),
            "target_corner_occurrence_ids": sorted(target_corners),
            "incident_occurrence_count": count, "incident_occurrences": incidents,
            "incident_occurrence_binding_sequence_sha256": seq(
                row["occurrence_binding_sha256"] for row in incidents),
            "quadrant_incident_occurrence_ids": {
                key: sorted(value) for key, value in sorted(qmap.items())},
            "nonrational_envelope_exclusion_count": len(unknown),
            "all_nonrational_occurrences_proven_disjoint": unknown_safe,
            "four_quadrant_germ_complete": complete, "incident_set_complete": complete,
            "owner_rule": OWNER_RULE, "owner_unique": owner_unique,
            "owner": selected_owner, "formal_credit": 0,
        }
        output.append({**body, "corner_entity_id": "c50a-corner:" + h(body)})
    return output, target_corner_count


def expected_owner(overlay: list[dict[str, Any]], targets: list[dict[str, Any]]) -> dict[str, Any]:
    faces, target_face_count = rebuild_faces(overlay, targets)
    corners, target_corner_count = rebuild_corners(overlay, targets, faces)
    face_complete = all(row["incident_set_complete"] and row["owner_unique"]
                        and row["incident_occurrence_count"] == 2 for row in faces)
    corner_complete = all(row["incident_set_complete"] and row["owner_unique"]
                          for row in corners)
    require(face_complete and corner_complete, "independent owner closure")
    return {
        "owner_protocol_version": VERSIONS["owner"],
        "face_atom_count": len(faces), "face_atoms": faces,
        "face_atom_id_sequence_sha256": seq(row["face_atom_id"] for row in faces),
        "target_face_atom_occurrence_count": target_face_count,
        "all_face_atoms_degree_two": all(row["incident_occurrence_count"] == 2
                                         for row in faces),
        "all_face_incident_sets_complete": face_complete,
        "corner_entity_count": len(corners), "corner_entities": corners,
        "corner_entity_id_sequence_sha256": seq(row["corner_entity_id"] for row in corners),
        "target_corner_occurrence_count": target_corner_count,
        "all_corner_four_quadrant_germs_complete": corner_complete,
        "all_codimension_owners_unique": face_complete and corner_complete,
        "formal_credit": 0,
    }


def audit(candidate: dict[str, Any], producer_hash: str) -> dict[str, Any]:
    keys(candidate, {"schema", "status", "producer", "request", "request_object_sha256",
                     "active_universe_replay", "history_replay", "target_replay",
                     "owner_ledger", "independence_and_scope", "strict_nonpromotion",
                     "formal_credit", "object_sha256"}, "candidate")
    self_hash(candidate, "object_sha256", "candidate")
    require(candidate["schema"] == CANDIDATE_SCHEMA, "candidate schema")
    require(candidate["status"] == "PASS_C50A_GENERIC_TWO_SIDE_HISTORY_BOUND_FULL_UNIVERSE_OWNER_ORACLE__ZERO_FORMAL_CREDIT",
            "candidate status")
    require(candidate["producer"] == {"path": PRODUCER_REL, "sha256": producer_hash},
            "producer byte binding")
    require(candidate["formal_credit"] == 0, "candidate formal credit")
    baseline, _ambient, base_replay = reconstruct_base()
    overlay, nodes, targets, head = replay_request(candidate["request"], baseline)
    require(candidate["request_object_sha256"] == candidate["request"]["request_object_sha256"],
            "candidate request binding")
    expected_active = {
        **base_replay, "active_universe_binding_sha256": ACTIVE_HASH,
        "final_overlay_occurrence_count": len(overlay),
        "final_overlay_occurrence_binding_sequence_sha256": seq(sorted(
            row["occurrence_binding_sha256"] for row in overlay)),
    }
    require(candidate["active_universe_replay"] == expected_active,
            "active universe replay equality")
    expected_history = {"history_protocol_version": VERSIONS["history"],
                        "genesis_sha256": GENESIS_HASH,
                        "transaction_count": len(nodes), "history_nodes": nodes,
                        "history_head_sha256": head}
    require(candidate["history_replay"] == expected_history, "history replay equality")
    expected_target = {
        "target_mode": candidate["request"]["target_mode"],
        "target_transaction_indices": candidate["request"]["target_transaction_indices"],
        "target_occurrence_count": len(targets),
        "target_occurrence_id_sequence_sha256": seq(sorted(
            row["physical_occurrence_id"] for row in targets)),
    }
    require(candidate["target_replay"] == expected_target, "target replay equality")
    owner_forward = expected_owner(overlay, targets)
    owner_reverse = expected_owner(list(reversed(overlay)), targets)
    require(encoded(owner_forward) == encoded(owner_reverse), "dual traversal owner replay")
    require(candidate["owner_ledger"] == owner_forward, "owner ledger equality")
    require(candidate["independence_and_scope"] == {
        "C48_producer_imported_or_executed": False,
        "C41_or_C32_producer_imported_or_executed": False,
        "frozen_ledgers_consumed_as_data_only": True,
        "arbitrary_task_and_history_request_supported": True,
        "nonrational_occurrences_require_conservative_C32_envelope_disjointness": True,
        "cross_chart_or_unknown_envelope_contact_rejects_fail_closed": True,
    }, "candidate scope flags")
    require(candidate["strict_nonpromotion"] == {
        "runtime_writes_performed": False, "authority_or_pointer_modified": False,
        "seal_or_receipt_created": False, "D02_gate_credit": 0,
        "D02_A_complete": False, "D02_B_complete": False,
        "D02_C_started": False, "D03_started": False,
        "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
    }, "strict nonpromotion flags")
    return {"overlay": overlay, "targets": targets, "history": nodes,
            "head": head, "owner": owner_forward, "base": base_replay}


def self_test() -> dict[str, Any]:
    checks = []
    require(h({"z": 0, "a": 1}) == h({"a": 1, "z": 0}), "canonical hash")
    checks.append("canonical JSON hashing")
    require(ACTIVE_HASH == h(ACTIVE) and GENESIS_HASH == h(GENESIS), "root bindings")
    checks.append("universe and history root bindings")
    require(positive_overlap(Q(0), Q(1), Q(1), Q(2)) is None, "point contact")
    checks.append("positive face overlap excludes point contact")
    body = {"schema": SCHEMA + ".self-test",
            "status": "PASS_C50A_INDEPENDENT_VERIFIER_SELF_TEST__NO_FULL_REPLAY__ZERO_CREDIT",
            "test_count": len(checks), "tests": checks,
            "producer_imported_or_executed": False,
            "runtime_writes_performed": False, "formal_credit": 0}
    return {**body, "object_sha256": h(body)}


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(encoded(value) + b"\n")
    sys.stdout.buffer.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        if arguments.self_test:
            emit(self_test())
            return 0
        require(arguments.candidate is not None, "candidate argument")
        before = frozen_files()
        candidate_raw, candidate_identity = read_stable(arguments.candidate.absolute(), "candidate")
        candidate = parse(candidate_raw, "candidate", canonical_line=True)
        producer_hash = next(row["sha256"] for row in before if row["path"] == PRODUCER_REL)
        result = audit(candidate, producer_hash)
        candidate_after, identity_after = read_stable(arguments.candidate.absolute(), "candidate replay")
        require(candidate_after == candidate_raw and identity_after == candidate_identity,
                "candidate terminal-byte/identity replay")
        after = frozen_files()
        require(after == before, "frozen source/input immutability")
        body = {
            "schema": SCHEMA,
            "status": "PASS_INDEPENDENT_C50A_GENERIC_HISTORY_BOUND_FULL_UNIVERSE_OWNER_ORACLE__ZERO_FORMAL_CREDIT",
            "verifier": {"path": str(SELF.relative_to(ROOT)), "sha256": hash_file(SELF)},
            "candidate": {"path": str(arguments.candidate.absolute()),
                          "file_sha256": hashlib.sha256(candidate_raw).hexdigest(),
                          "object_sha256": candidate["object_sha256"],
                          "request_object_sha256": candidate["request_object_sha256"]},
            "independence_boundary": {
                "C50a_producer_imported_or_executed": False,
                "C48_C41_C32_producers_imported_or_executed": False,
                "producer_read_only_for_terminal_byte_hash": True,
                "frozen_ledgers_parsed_directly": True,
                "boundary_index_face_implementation": True,
                "separate_point_query_corner_implementation": True,
                "full_universe_reconstructed_twice_in_opposite_traversal_orders": True,
            },
            "replay": {
                "C32_cell_count": result["base"]["C32_cell_count"],
                "C41_ambient_row_count": result["base"]["C41_ambient_row_count"],
                "baseline_physical_occurrence_count": result["base"]["baseline_physical_occurrence_count"],
                "final_overlay_occurrence_count": len(result["overlay"]),
                "transaction_count": len(result["history"]),
                "history_head_sha256": result["head"],
                "target_occurrence_count": len(result["targets"]),
                "face_atom_count": result["owner"]["face_atom_count"],
                "corner_entity_count": result["owner"]["corner_entity_count"],
                "all_codimension_owners_unique": result["owner"]["all_codimension_owners_unique"],
            },
            "immutability": {"frozen_file_count": len(before),
                             "pre_post_snapshot_equal": True,
                             "snapshot_sha256": h(before),
                             "candidate_terminal_byte_replay_equal": True,
                             "candidate_identity_replay_equal": True},
            "strict_nonpromotion": {"runtime_writes_performed": False,
                                    "seal_or_authority_created": False,
                                    "D02_gate_credit": 0,
                                    "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0},
            "formal_credit": 0,
        }
        emit({**body, "object_sha256": h(body)})
        return 0
    except (Deny, OSError, ValueError, KeyError, TypeError, StopIteration,
            gzip.BadGzipFile, json.JSONDecodeError) as error:
        body = {"schema": SCHEMA + ".fail-closed", "status": "REJECTED",
                "error_class": type(error).__name__, "reason": str(error),
                "producer_imported_or_executed": False,
                "runtime_writes_performed": False, "formal_credit": 0}
        emit({**body, "object_sha256": h(body)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
