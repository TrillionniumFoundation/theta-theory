#!/usr/bin/env python3
"""Request-driven, full-active-universe codimension owner oracle.

This is a zero-credit capability artifact.  It turns the narrow C48 owner
ledger construction into a versioned overlay-history protocol.  Every
transaction replaces exactly one representative/reflected predecessor pair,
binds the task, occurrence, split, and history versions, and recomputes face
and corner owners against the complete frozen 91,879-row C41 universe.

The default regression fixture is adapted from C48 *data*; no C48 producer is
imported or executed.  Arbitrary callers can supply the same request schema
with ``--request``.  Output is canonical JSON on stdout and no runtime state is
written.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
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
RUNTIME = ROOT / ".cm2-runtime"
DELIVERABLES = ROOT / "deliverables"

SCHEMA = "cm2.round306c50a.global-codimension-owner-oracle.v1"
REQUEST_SCHEMA = SCHEMA + ".request"
FACE_SCHEMA = SCHEMA + ".face-atom-owner"
CORNER_SCHEMA = SCHEMA + ".corner-owner"

PROTOCOLS = {
    "occurrence": "CM2_C41_ACTIVE_OVERLAY_OCCURRENCE_V1",
    "split": "CM2_EXACT_TWO_SIDE_BINARY_SPLIT_DECISION_V1",
    "history": "CM2_HASH_CHAINED_ACTIVE_OVERLAY_HISTORY_V1",
    "owner": "CM2_FULL_UNIVERSE_FACE_CORNER_OWNER_V1",
}
OWNER_RULE = "UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH"

C32_REL = ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
C41_REL = ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C32_DIR = ROOT / C32_REL
C41_DIR = ROOT / C41_REL
C32_LEDGER = C32_DIR / "compact_cells.jsonl.gz"
C41_LEDGER = C41_DIR / "routed_ambient_cells.jsonl.gz"
C32_RESULT = C32_DIR / "result.json"
C41_RESULT = C41_DIR / "result.json"
C32_MANIFEST = C32_DIR / "root_manifest.sha256"
C41_MANIFEST = C41_DIR / "root_manifest.sha256"

C32_OBJECT = "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474"
C41_OBJECT = "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
C32_RESULT_SHA256 = "c2abba977fa21ea965a9d77478df391db496d0e03f60320b9a4adf9005f1a0a4"
C41_RESULT_SHA256 = "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f"
C32_MANIFEST_SHA256 = "4af827cfec996f62443b9ef38ea71cd341873de58b9b04cedfcd8faaca70a8e1"
C41_MANIFEST_SHA256 = "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba"
C32_LEDGER_SHA256 = "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8"
C41_LEDGER_SHA256 = "ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8"
C32_ROW_COUNT = 76_832
C41_ROW_COUNT = 91_879
C32_ROW_SEQUENCE_SHA256 = "e2f33100491adadda1045c37be735a80cc8bc7e914132b5647e3df13913ac726"
C41_ROW_SEQUENCE_SHA256 = "934d5ca55ee2deb33a066d948af9e3f0a85e09088d97254a579a06c3f62b8045"

C48_RESULT = DELIVERABLES / "cm2_round306c48_d02a_pair668_two_side_owner_closure_result_v1.json"
C48_RESULT_SHA256 = "5f356dd0b1bb9ded56548a8b046f2401ad59bf706c253d44dd151649035d283e"
C48_OBJECT = "61de17d0a8122a4a03af34cf832cd717fdb715cd9c4cd2fac4162bdab8ddceab"
C48_AMBIENT_ID = "c41-ambient:a828b4c95611e3e12ab8b3131f19f801ce8e1f1541106010ea94f34ba981a351"
C48_AMBIENT_ROW = "195145d6d5fb6a2bfc78d3f0fd97dcb6af75ef4eb3d0c0c0efb116feaeba4bdd"
C48_TASK_BINDING = "64400932860d6f224a90204e56a5614bf982eb3a1b87f37f04b86ba112a3ff9f"

ACTIVE_UNIVERSE = {
    "schema": SCHEMA + ".active-universe-binding",
    "C32": {
        "authority_object_sha256": C32_OBJECT,
        "result_path": C32_REL + "/result.json",
        "result_file_sha256": C32_RESULT_SHA256,
        "root_manifest_path": C32_REL + "/root_manifest.sha256",
        "root_manifest_file_sha256": C32_MANIFEST_SHA256,
        "cell_ledger_path": C32_REL + "/compact_cells.jsonl.gz",
        "cell_ledger_file_sha256": C32_LEDGER_SHA256,
        "cell_row_count": C32_ROW_COUNT,
        "cell_row_sequence_sha256": C32_ROW_SEQUENCE_SHA256,
    },
    "C41": {
        "authority_object_sha256": C41_OBJECT,
        "result_path": C41_REL + "/result.json",
        "result_file_sha256": C41_RESULT_SHA256,
        "root_manifest_path": C41_REL + "/root_manifest.sha256",
        "root_manifest_file_sha256": C41_MANIFEST_SHA256,
        "ambient_ledger_path": C41_REL + "/routed_ambient_cells.jsonl.gz",
        "ambient_ledger_file_sha256": C41_LEDGER_SHA256,
        "ambient_row_count": C41_ROW_COUNT,
        "ambient_row_sequence_sha256": C41_ROW_SEQUENCE_SHA256,
    },
}


class Reject(RuntimeError):
    """A fail-closed protocol, input, geometry, or incidence rejection."""


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sequence_digest(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        need(type(value) is str, "sequence digest string")
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


ACTIVE_UNIVERSE_SHA256 = digest(ACTIVE_UNIVERSE)
GENESIS_BODY = {
    "schema": SCHEMA + ".history-genesis",
    "history_protocol_version": PROTOCOLS["history"],
    "active_universe_binding_sha256": ACTIVE_UNIVERSE_SHA256,
    "genesis_kind": "FROZEN_C41_91879_ROW_TWO_SIDE_ACTIVE_UNIVERSE",
}
GENESIS_SHA256 = digest(GENESIS_BODY)


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def stable_read(path: Path, label: str, maximum: int = 512 << 20) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode), "regular file:" + label)
        need(before.st_nlink == 1 and 0 < before.st_size <= maximum,
             "singleton bounded file:" + label)
        chunks: list[bytes] = []
        remaining = before.st_size
        while remaining:
            block = os.read(fd, min(4 << 20, remaining))
            need(bool(block), "short read:" + label)
            chunks.append(block)
            remaining -= len(block)
        need(os.read(fd, 1) == b"", "stable EOF:" + label)
        after = os.fstat(fd)
    finally:
        os.close(fd)
    identity = lambda row: (
        row.st_dev, row.st_ino, row.st_mode, row.st_nlink, row.st_uid,
        row.st_gid, row.st_size, row.st_mtime_ns, row.st_ctime_ns,
    )
    need(identity(before) == identity(after), "TOCTOU:" + label)
    return b"".join(chunks)


def json_value(raw: bytes, label: str, *, canonical_line: bool = False) -> dict[str, Any]:
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         "JSON byte hygiene:" + label)

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + label + ":" + key)
            result[key] = value
        return result

    def no_float(token: str) -> Any:
        raise Reject("noninteger JSON number:" + label + ":" + token)

    value = json.loads(
        raw.decode("utf-8", "strict"), object_pairs_hook=pairs,
        parse_float=no_float, parse_constant=no_float,
    )
    need(type(value) is dict, "JSON object:" + label)
    if canonical_line:
        need(raw == canonical(value) + b"\n", "canonical JSON line:" + label)
    return value


def closed(value: dict[str, Any], hash_key: str, label: str) -> None:
    need(type(value) is dict and type(value.get(hash_key)) is str,
         "self-hash field:" + label)
    body = {key: item for key, item in value.items() if key != hash_key}
    need(value[hash_key] == digest(body), "self-hash:" + label)


def exact_keys(value: dict[str, Any], keys: set[str], label: str) -> None:
    need(type(value) is dict and set(value) == keys, "exact keys:" + label)


def q(value: str, label: str) -> F:
    need(type(value) is str and 0 < len(value) <= 256, "rational string:" + label)
    result = F(value)
    need(str(result) == value, "canonical rational:" + label)
    return result


def interval(value: list[str], label: str, *, positive: bool = False) -> tuple[F, F]:
    need(type(value) is list and len(value) == 2, "interval shape:" + label)
    low, high = q(value[0], label + ".low"), q(value[1], label + ".high")
    need(low < high if positive else low <= high, "interval order:" + label)
    return low, high


def exact_box(value: dict[str, Any], label: str) -> tuple[F, F, F, F]:
    exact_keys(value, {"compact_chart", "t", "p", "s"}, label)
    need(value["compact_chart"] in {"E", "W", "N", "S"}, "chart:" + label)
    t0, t1 = interval(value["t"], label + ".t", positive=True)
    p0, p1 = interval(value["p"], label + ".p", positive=True)
    s0, s1 = interval(value["s"], label + ".s")
    need(s0 == s1 == 0, "s=0 box:" + label)
    return t0, t1, p0, p1


def envelope(value: dict[str, Any], chart: str, label: str) -> dict[str, Any]:
    need(type(value) is dict, "cell envelope:" + label)
    t0, t1 = interval(value["t"], label + ".t", positive=True)
    p0, p1 = interval(value["p"], label + ".p", positive=True)
    return {
        "compact_chart": chart,
        "t": [str(t0), str(t1)],
        "p": [str(p0), str(p1)],
    }


def verify_authority_files() -> None:
    pins = {
        C32_RESULT: C32_RESULT_SHA256, C41_RESULT: C41_RESULT_SHA256,
        C32_MANIFEST: C32_MANIFEST_SHA256, C41_MANIFEST: C41_MANIFEST_SHA256,
    }
    for path, expected in pins.items():
        raw = stable_read(path, str(path.relative_to(ROOT)))
        need(hashlib.sha256(raw).hexdigest() == expected,
             "frozen file SHA-256:" + str(path.relative_to(ROOT)))
    for path, expected in ((C32_RESULT, C32_OBJECT), (C41_RESULT, C41_OBJECT)):
        value = json_value(stable_read(path, "authority result"), "authority result")
        closed(value, "object_sha256", str(path.relative_to(ROOT)))
        need(value["object_sha256"] == expected, "authority object pin")


def ledger_rows(path: Path, expected_sha: str, expected_count: int,
                expected_sequence: str, label: str) -> list[dict[str, Any]]:
    raw = stable_read(path, label)
    need(hashlib.sha256(raw).hexdigest() == expected_sha, "ledger file SHA-256:" + label)
    output: list[dict[str, Any]] = []
    hashes: list[str] = []
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
        for ordinal, line in enumerate(stream):
            row = json_value(line, f"{label}[{ordinal}]", canonical_line=True)
            need(type(row.get("row_sha256")) is str, "ledger row hash field:" + label)
            output.append(row)
            hashes.append(row["row_sha256"])
    need(len(output) == expected_count, "ledger row census:" + label)
    need(sequence_digest(hashes) == expected_sequence, "ledger row sequence:" + label)
    return output


def occurrence(body: dict[str, Any]) -> dict[str, Any]:
    binding = digest(body)
    result = {
        **body,
        "occurrence_binding_sha256": binding,
        "physical_occurrence_id": "c50a-occurrence:" + binding,
    }
    box = body["exact_closed_box"]
    if box is None:
        env = body["nonrational_exclusion_envelope"]
        t0, t1 = interval(env["t"], "nonrational envelope t", positive=True)
        p0, p1 = interval(env["p"], "nonrational envelope p", positive=True)
        result.update({
            "rational": False, "t0": None, "t1": None,
            "p0": None, "p1": None,
            "env_t0": t0, "env_t1": t1, "env_p0": p0, "env_p1": p1,
        })
    else:
        t0, t1, p0, p1 = exact_box(box, "occurrence box")
        result.update({
            "rational": True, "t0": t0, "t1": t1,
            "p0": p0, "p1": p1,
        })
    return result


def load_active_universe() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    verify_authority_files()
    cells = ledger_rows(
        C32_LEDGER, C32_LEDGER_SHA256, C32_ROW_COUNT,
        C32_ROW_SEQUENCE_SHA256, "C32 compact cells",
    )
    cell_map: dict[str, dict[str, Any]] = {}
    for row in cells:
        need(row["schema"] == "cm2.round306c32.d02-four-chart-compact-atlas-cell.v1",
             "C32 cell schema")
        cell_id = row["cell_id"]
        need(type(cell_id) is str and cell_id not in cell_map, "C32 cell identity uniqueness")
        chart = row["compact_chart"]
        need(chart in {"E", "W", "N", "S"} and row["gate3_chart"].endswith(":" + chart),
             "C32 compact chart binding")
        cell_map[cell_id] = {
            "compact_chart": chart,
            "row_sha256": row["row_sha256"],
            "envelope": envelope(row["gate3_product_box"], chart, "C32 cell envelope"),
        }
    ambient = ledger_rows(
        C41_LEDGER, C41_LEDGER_SHA256, C41_ROW_COUNT,
        C41_ROW_SEQUENCE_SHA256, "C41 routed ambient cells",
    )
    overlay: list[dict[str, Any]] = []
    ambient_index: dict[str, dict[str, Any]] = {}
    for row in ambient:
        need(row["schema"] == "cm2.round306c41.d02-lower-strata-depth3-closure.v1.routed-ambient-cell",
             "C41 ambient schema")
        ambient_id = row["c41_ambient_cell_id"]
        need(type(ambient_id) is str and ambient_id not in ambient_index,
             "C41 ambient identity uniqueness")
        ambient_index[ambient_id] = row
        for side in ("REPRESENTATIVE", "REFLECTED"):
            cell_key = "representative_cell_id" if side == "REPRESENTATIVE" else "reflected_cell_id"
            box_key = "closed_representative_box" if side == "REPRESENTATIVE" else "closed_reflected_box"
            cell_id = row[cell_key]
            need(cell_id in cell_map, "C41 to C32 cell foreign key")
            chart = cell_map[cell_id]["compact_chart"]
            raw_box = row[box_key]
            if raw_box is None:
                box = None
                env = cell_map[cell_id]["envelope"]
            else:
                box = dict(raw_box)
                if side == "REPRESENTATIVE":
                    box = {"compact_chart": chart, **box}
                need(box["compact_chart"] == chart, "C41 box to C32 chart binding")
                exact_box(box, "C41 exact box")
                env = None
            body = {
                "occurrence_protocol_version": PROTOCOLS["occurrence"],
                "active_universe_binding_sha256": ACTIVE_UNIVERSE_SHA256,
                "history_parent_sha256": GENESIS_SHA256,
                "transaction_binding_sha256": None,
                "source_kind": "C41_BASELINE",
                "side": side,
                "pair_index": row["pair_index"],
                "semantic_path": row["path"],
                "physical_route_path": None,
                "physical_cell_id": cell_id,
                "compact_chart": chart,
                "exact_closed_box": box,
                "nonrational_exclusion_envelope": env,
                "upstream_ambient_cell_id": ambient_id,
                "upstream_ambient_row_sha256": row["row_sha256"],
                "upstream_split_axis_history": row["split_axis_history"],
                "upstream_disposition_family": row["disposition_family"],
                "upstream_task_binding_sha256": None,
                "relative_path": None,
                "source_evidence": None,
            }
            overlay.append(occurrence(body))
    need(len(overlay) == 183_758, "two-side baseline occurrence census")
    rational_count = sum(row["rational"] for row in overlay)
    need(rational_count == 183_700, "exact-rational baseline occurrence census")
    ids = [row["physical_occurrence_id"] for row in overlay]
    need(len(set(ids)) == len(ids), "baseline occurrence identity uniqueness")
    replay = {
        "C32_cell_count": len(cell_map),
        "C41_ambient_row_count": len(ambient_index),
        "baseline_physical_occurrence_count": len(overlay),
        "baseline_exact_rational_occurrence_count": rational_count,
        "baseline_nonrational_enveloped_occurrence_count": len(overlay) - rational_count,
        "baseline_occurrence_binding_sequence_sha256": sequence_digest(sorted(
            row["occurrence_binding_sha256"] for row in overlay
        )),
        "full_pinned_active_universe_scanned": True,
    }
    return overlay, ambient_index, replay


def common_prefix(values: list[str]) -> str:
    need(bool(values) and all(type(value) is str for value in values), "common prefix inputs")
    prefix = values[0]
    for value in values[1:]:
        while not value.startswith(prefix):
            prefix = prefix[:-1]
    return prefix


def split_decision(side: str, logical_parent: str, physical_parent: str,
                   axis: str, coordinate: str, lower_logical: str,
                   lower_physical: str, upper_logical: str,
                   upper_physical: str) -> dict[str, Any]:
    body = {
        "split_protocol_version": PROTOCOLS["split"],
        "side": side,
        "logical_parent_prefix": logical_parent,
        "physical_parent_path": physical_parent,
        "axis": axis,
        "coordinate": coordinate,
        "lower_coordinate_logical_child_prefix": lower_logical,
        "lower_coordinate_physical_child_path": lower_physical,
        "upper_coordinate_logical_child_prefix": upper_logical,
        "upper_coordinate_physical_child_path": upper_physical,
        "half_open_owner_logical_child_prefix": lower_logical,
    }
    return {**body, "split_decision_sha256": digest(body)}


def build_c48_request() -> dict[str, Any]:
    raw = stable_read(C48_RESULT, "C48 installed task result")
    need(hashlib.sha256(raw).hexdigest() == C48_RESULT_SHA256, "C48 result file pin")
    source = json_value(raw, "C48 result", canonical_line=True)
    closed(source, "object_sha256", "C48 result")
    need(source["object_sha256"] == C48_OBJECT, "C48 result object pin")
    selection = source["selection"]
    need(selection["ambient_cell_id"] == C48_AMBIENT_ID,
         "C48 ambient fixture pin")
    need(selection["task_binding_sha256"] == C48_TASK_BINDING,
         "C48 task fixture pin")
    raw_rows = source["two_side_route_materialization"]["route_and_margin_rows"]
    need(type(raw_rows) is list and len(raw_rows) == 6, "C48 physical leaf fixture census")
    replacements = []
    for row in raw_rows:
        need(row["formal_credit"] == 0 and row["terminal_candidate_closed"] is True,
             "C48 leaf evidence remains candidate/zero-credit")
        evidence = {
            "source_schema": row["schema"],
            "source_physical_leaf_id": row["physical_leaf_id"],
            "source_route_row_sha256": digest(row),
            "terminal_classification": row["terminal_classification"],
            "terminal_candidate_closed": True,
            "formal_credit": 0,
        }
        replacements.append({
            "side": row["side"], "relative_path": row["relative_path"],
            "semantic_path": row["semantic_path"],
            "physical_route_path": row["physical_route_path"],
            "physical_cell_id": row["physical_cell_id"],
            "exact_closed_box": row["exact_closed_box"],
            "relative_parent_fraction": row["relative_parent_fraction"],
            "source_evidence": evidence,
        })
    replacements.sort(key=lambda row: (row["side"], row["relative_path"]))
    rep_paths = [row["physical_route_path"] for row in replacements
                 if row["side"] == "REPRESENTATIVE"]
    ref_paths = [row["physical_route_path"] for row in replacements
                 if row["side"] == "REFLECTED"]
    rep_root, ref_root = common_prefix(rep_paths), common_prefix(ref_paths)
    need(rep_root == "010111011" and ref_root == "101000100", "C48 physical roots")
    decisions = [
        split_decision("REPRESENTATIVE", "", rep_root, "t", "31683/102400",
                       "0", rep_root + "0", "1", rep_root + "1"),
        split_decision("REPRESENTATIVE", "1", rep_root + "1", "p", "-1653/4096",
                       "10", rep_root + "10", "11", rep_root + "11"),
        split_decision("REFLECTED", "", ref_root, "t", "-31683/102400",
                       "1", ref_root + "0", "0", ref_root + "1"),
        split_decision("REFLECTED", "1", ref_root + "0", "p", "1653/4096",
                       "11", ref_root + "00", "10", ref_root + "01"),
    ]
    decisions.sort(key=lambda row: (row["side"], row["logical_parent_prefix"]))
    task_body = {
        "task_id": selection["task_id"],
        "upstream_task_binding_sha256": C48_TASK_BINDING,
        "pair_index": 668,
        "root_semantic_path": "010111011",
        "predecessors": [
            {
                "side": side, "locator_kind": "C41_AMBIENT_SIDE",
                "upstream_ambient_cell_id": C48_AMBIENT_ID,
                "upstream_ambient_row_sha256": C48_AMBIENT_ROW,
            } for side in ("REPRESENTATIVE", "REFLECTED")
        ],
    }
    task = {**task_body, "oracle_task_binding_sha256": digest(task_body)}
    tx_body = {
        "transaction_index": 0,
        "parent_history_sha256": GENESIS_SHA256,
        "task": task,
        "relative_frontier": ["0", "10", "11"],
        "split_decisions": decisions,
        "replacements": replacements,
    }
    tx = {**tx_body, "transaction_binding_sha256": digest(tx_body)}
    body = {
        "schema": REQUEST_SCHEMA,
        "protocol_versions": PROTOCOLS,
        "active_universe": ACTIVE_UNIVERSE,
        "active_universe_binding_sha256": ACTIVE_UNIVERSE_SHA256,
        "history_genesis": GENESIS_BODY,
        "history_genesis_sha256": GENESIS_SHA256,
        "transactions": [tx],
        "target_mode": "TRANSACTION_INSERTIONS_STILL_ACTIVE",
        "target_transaction_indices": [0],
        "request_purpose": "C48_INSTALLED_TASK_GENERIC_ORACLE_REGRESSION__ZERO_CREDIT",
        "formal_credit": 0,
    }
    return {**body, "request_object_sha256": digest(body)}


def prefixes(frontier: list[str]) -> set[str]:
    return {value[:depth] for value in frontier for depth in range(len(value))}


def bound(rows: list[dict[str, Any]]) -> tuple[F, F, F, F]:
    need(bool(rows), "nonempty box bound")
    return (
        min(row["t0"] for row in rows), max(row["t1"] for row in rows),
        min(row["p0"] for row in rows), max(row["p1"] for row in rows),
    )


def area(box: tuple[F, F, F, F]) -> F:
    return (box[1] - box[0]) * (box[3] - box[2])


def nonoverlap(rows: list[dict[str, Any]], label: str) -> None:
    for index, left in enumerate(rows):
        for right in rows[index + 1:]:
            t = min(left["t1"], right["t1"]) - max(left["t0"], right["t0"])
            p = min(left["p1"], right["p1"]) - max(left["p0"], right["p0"])
            need(t <= 0 or p <= 0, "interior-disjoint leaf boxes:" + label)


def validate_split_tree(task: dict[str, Any], frontier: list[str],
                        replacements: list[dict[str, Any]],
                        decisions: list[dict[str, Any]],
                        predecessors: dict[str, dict[str, Any]]) -> str:
    need(bool(frontier) and len(frontier) <= 4096, "bounded nonempty frontier")
    need(frontier == sorted(set(frontier)), "sorted unique frontier")
    need(all(type(path) is str and path and set(path) <= {"0", "1"}
             for path in frontier), "binary nonempty relative paths")
    need(not any(right.startswith(left) for left in frontier for right in frontier
                 if left != right), "prefix-free frontier")
    need(sum((F(1, 2 ** len(path)) for path in frontier), F(0)) == 1,
         "exact Kraft-one frontier")
    internals = prefixes(frontier)
    need(all(any(path.startswith(prefix + "0") for path in frontier)
             and any(path.startswith(prefix + "1") for path in frontier)
             for prefix in internals), "complete binary prefix tree")
    need(len(replacements) == 2 * len(frontier), "two-side replacement census")
    by_side: dict[str, dict[str, dict[str, Any]]] = {}
    for side in ("REPRESENTATIVE", "REFLECTED"):
        side_rows = [row for row in replacements if row.get("side") == side]
        need(sorted(row.get("relative_path") for row in side_rows) == frontier,
             "two-side identical frontier:" + side)
        mapping: dict[str, dict[str, Any]] = {}
        for row in side_rows:
            exact_keys(row, {
                "side", "relative_path", "semantic_path", "physical_route_path",
                "physical_cell_id", "exact_closed_box", "relative_parent_fraction",
                "source_evidence",
            }, "replacement")
            rel = row["relative_path"]
            need(row["semantic_path"] == task["root_semantic_path"] + rel,
                 "semantic root/history binding")
            need(type(row["physical_route_path"]) is str
                 and set(row["physical_route_path"]) <= {"0", "1"},
                 "physical route path")
            need(row["physical_cell_id"] == predecessors[side]["physical_cell_id"],
                 "replacement predecessor physical cell binding")
            need(row["exact_closed_box"]["compact_chart"] == predecessors[side]["compact_chart"],
                 "replacement predecessor chart binding")
            t0, t1, p0, p1 = exact_box(row["exact_closed_box"], "replacement box")
            need(q(row["relative_parent_fraction"], "relative fraction")
                 == F(1, 2 ** len(rel)), "relative fraction/path binding")
            evidence = row["source_evidence"]
            need(type(evidence) is dict and evidence.get("formal_credit") == 0,
                 "replacement zero-credit evidence")
            mapping[rel] = {**row, "t0": t0, "t1": t1, "p0": p0, "p1": p1}
        nonoverlap(list(mapping.values()), side)
        root_bound = bound(list(mapping.values()))
        predecessor_box = predecessors[side]["exact_closed_box"]
        need(predecessor_box is not None, "exact predecessor required for split oracle")
        need(root_bound == exact_box(predecessor_box, "predecessor exact box"),
             "replacement union equals predecessor box")
        need(sum(area((row["t0"], row["t1"], row["p0"], row["p1"]))
                 for row in mapping.values()) == area(root_bound),
             "replacement exact area conservation")
        by_side[side] = mapping
    need(len(decisions) == 2 * len(internals), "complete two-side split-decision census")
    event_map: dict[tuple[str, str], dict[str, Any]] = {}
    for event in decisions:
        exact_keys(event, {
            "split_protocol_version", "side", "logical_parent_prefix",
            "physical_parent_path", "axis", "coordinate",
            "lower_coordinate_logical_child_prefix",
            "lower_coordinate_physical_child_path",
            "upper_coordinate_logical_child_prefix",
            "upper_coordinate_physical_child_path",
            "half_open_owner_logical_child_prefix", "split_decision_sha256",
        }, "split decision")
        closed(event, "split_decision_sha256", "split decision")
        need(event["split_protocol_version"] == PROTOCOLS["split"],
             "split protocol version")
        side, parent = event["side"], event["logical_parent_prefix"]
        need(side in by_side and parent in internals and (side, parent) not in event_map,
             "split side/parent uniqueness")
        children = {parent + "0", parent + "1"}
        lower = event["lower_coordinate_logical_child_prefix"]
        upper = event["upper_coordinate_logical_child_prefix"]
        need({lower, upper} == children, "logical binary child binding")
        physical_parent = event["physical_parent_path"]
        need({event["lower_coordinate_physical_child_path"],
              event["upper_coordinate_physical_child_path"]}
             == {physical_parent + "0", physical_parent + "1"},
             "physical binary child binding")
        need(event["half_open_owner_logical_child_prefix"] in children,
             "half-open owner child binding")
        event_map[(side, parent)] = event
    split_hashes: list[str] = []
    for side, mapping in by_side.items():
        physical_prefix = {"": event_map[(side, "")]["physical_parent_path"]}
        for parent in sorted(internals, key=lambda item: (len(item), item)):
            event = event_map[(side, parent)]
            need(physical_prefix[parent] == event["physical_parent_path"],
                 "physical split-history continuity")
            lower = event["lower_coordinate_logical_child_prefix"]
            upper = event["upper_coordinate_logical_child_prefix"]
            physical_prefix[lower] = event["lower_coordinate_physical_child_path"]
            physical_prefix[upper] = event["upper_coordinate_physical_child_path"]
            lower_rows = [row for rel, row in mapping.items() if rel.startswith(lower)]
            upper_rows = [row for rel, row in mapping.items() if rel.startswith(upper)]
            lower_box, upper_box = bound(lower_rows), bound(upper_rows)
            axis = event["axis"]
            coordinate = q(event["coordinate"], "split coordinate")
            if axis == "t":
                need(lower_box[1] == upper_box[0] == coordinate,
                     "t split coordinate adjacency")
                need(lower_box[2:] == upper_box[2:], "t split transverse interval")
            elif axis == "p":
                need(lower_box[3] == upper_box[2] == coordinate,
                     "p split coordinate adjacency")
                need(lower_box[:2] == upper_box[:2], "p split transverse interval")
            else:
                raise Reject("split axis enum")
            parent_rows = lower_rows + upper_rows
            parent_box = bound(parent_rows)
            need(area(parent_box) == sum(area((row["t0"], row["t1"], row["p0"], row["p1"]))
                                              for row in parent_rows),
                 "split subtree exact rectangular conservation")
            split_hashes.append(event["split_decision_sha256"])
        for rel, row in mapping.items():
            need(physical_prefix[rel] == row["physical_route_path"],
                 "leaf physical route/split-history binding")
    return sequence_digest(sorted(split_hashes))


def request_check(request: dict[str, Any]) -> None:
    exact_keys(request, {
        "schema", "protocol_versions", "active_universe",
        "active_universe_binding_sha256", "history_genesis",
        "history_genesis_sha256", "transactions", "target_transaction_indices",
        "target_mode", "request_purpose", "formal_credit", "request_object_sha256",
    }, "request")
    closed(request, "request_object_sha256", "request")
    need(request["schema"] == REQUEST_SCHEMA and request["protocol_versions"] == PROTOCOLS,
         "request schema/protocol versions")
    need(request["active_universe"] == ACTIVE_UNIVERSE
         and request["active_universe_binding_sha256"] == ACTIVE_UNIVERSE_SHA256,
         "active universe binding")
    need(request["history_genesis"] == GENESIS_BODY
         and request["history_genesis_sha256"] == GENESIS_SHA256,
         "history genesis binding")
    need(request["formal_credit"] == 0, "request formal credit zero")
    need(type(request["transactions"]) is list and 0 < len(request["transactions"]) <= 1000,
         "bounded transaction history")
    targets = request["target_transaction_indices"]
    need(type(targets) is list and targets == sorted(set(targets)),
         "sorted unique target transaction indices")
    mode = request["target_mode"]
    need(mode in {"TRANSACTION_INSERTIONS_STILL_ACTIVE",
                  "ALL_ACTIVE_HISTORY_REPLACEMENTS"}, "target mode")
    need((mode == "TRANSACTION_INSERTIONS_STILL_ACTIVE" and bool(targets))
         or (mode == "ALL_ACTIVE_HISTORY_REPLACEMENTS" and targets == []),
         "target mode/index contract")


def locate_predecessor(locator: dict[str, Any], side: str,
                       active: dict[str, dict[str, Any]]) -> dict[str, Any]:
    need(locator.get("side") == side, "predecessor side binding")
    kind = locator.get("locator_kind")
    if kind == "C41_AMBIENT_SIDE":
        exact_keys(locator, {"side", "locator_kind", "upstream_ambient_cell_id",
                             "upstream_ambient_row_sha256"}, "C41 predecessor locator")
        found = [row for row in active.values()
                 if row["source_kind"] == "C41_BASELINE" and row["side"] == side
                 and row["upstream_ambient_cell_id"] == locator["upstream_ambient_cell_id"]
                 and row["upstream_ambient_row_sha256"] == locator["upstream_ambient_row_sha256"]]
    elif kind == "ACTIVE_OCCURRENCE_ID":
        exact_keys(locator, {"side", "locator_kind", "physical_occurrence_id"},
                   "active predecessor locator")
        row = active.get(locator["physical_occurrence_id"])
        found = [] if row is None or row["side"] != side else [row]
    else:
        raise Reject("predecessor locator kind")
    need(len(found) == 1, "exactly one active predecessor occurrence")
    return found[0]


def apply_history(request: dict[str, Any], baseline: list[dict[str, Any]]) \
        -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], str]:
    active = {row["physical_occurrence_id"]: row for row in baseline}
    need(len(active) == len(baseline), "active baseline identity uniqueness")
    head = GENESIS_SHA256
    replay: list[dict[str, Any]] = []
    inserted_by_tx: dict[int, list[dict[str, Any]]] = {}
    for expected_index, tx in enumerate(request["transactions"]):
        exact_keys(tx, {
            "transaction_index", "parent_history_sha256", "task",
            "relative_frontier", "split_decisions", "replacements",
            "transaction_binding_sha256",
        }, "transaction")
        closed(tx, "transaction_binding_sha256", "transaction")
        need(tx["transaction_index"] == expected_index, "transaction contiguous index")
        need(tx["parent_history_sha256"] == head, "transaction parent history binding")
        task = tx["task"]
        exact_keys(task, {
            "task_id", "upstream_task_binding_sha256", "pair_index",
            "root_semantic_path", "predecessors", "oracle_task_binding_sha256",
        }, "task")
        closed(task, "oracle_task_binding_sha256", "oracle task")
        need(type(task["task_id"]) is str and type(task["upstream_task_binding_sha256"]) is str,
             "task identity strings")
        need(type(task["pair_index"]) is int and task["pair_index"] >= 0,
             "task pair index")
        need(type(task["root_semantic_path"]) is str
             and set(task["root_semantic_path"]) <= {"0", "1"}, "task semantic root")
        locators = task["predecessors"]
        need(type(locators) is list and len(locators) == 2, "two task predecessors")
        predecessor = {
            side: locate_predecessor(next(item for item in locators if item.get("side") == side),
                                     side, active)
            for side in ("REPRESENTATIVE", "REFLECTED")
        }
        need(all(row["pair_index"] == task["pair_index"] for row in predecessor.values()),
             "task pair/predecessor binding")
        need(all(row["semantic_path"] == task["root_semantic_path"]
                 for row in predecessor.values()), "task root/predecessor semantic binding")
        split_sequence = validate_split_tree(
            task, tx["relative_frontier"], tx["replacements"],
            tx["split_decisions"], predecessor,
        )
        removed = sorted(row["physical_occurrence_id"] for row in predecessor.values())
        need(len(set(removed)) == 2, "two distinct predecessor occurrences")
        for occurrence_id in removed:
            del active[occurrence_id]
        inserted: list[dict[str, Any]] = []
        for spec in tx["replacements"]:
            body = {
                "occurrence_protocol_version": PROTOCOLS["occurrence"],
                "active_universe_binding_sha256": ACTIVE_UNIVERSE_SHA256,
                "history_parent_sha256": head,
                "transaction_binding_sha256": tx["transaction_binding_sha256"],
                "source_kind": "HISTORY_REPLACEMENT",
                "side": spec["side"], "pair_index": task["pair_index"],
                "semantic_path": spec["semantic_path"],
                "physical_route_path": spec["physical_route_path"],
                "physical_cell_id": spec["physical_cell_id"],
                "compact_chart": spec["exact_closed_box"]["compact_chart"],
                "exact_closed_box": spec["exact_closed_box"],
                "nonrational_exclusion_envelope": None,
                "upstream_ambient_cell_id": predecessor[spec["side"]]["upstream_ambient_cell_id"],
                "upstream_ambient_row_sha256": predecessor[spec["side"]]["upstream_ambient_row_sha256"],
                "upstream_split_axis_history": None,
                "upstream_disposition_family": None,
                "upstream_task_binding_sha256": task["upstream_task_binding_sha256"],
                "relative_path": spec["relative_path"],
                "source_evidence": spec["source_evidence"],
            }
            row = occurrence(body)
            need(row["physical_occurrence_id"] not in active, "replacement occurrence uniqueness")
            active[row["physical_occurrence_id"]] = row
            inserted.append(row)
        overlay_sequence = sequence_digest(sorted(row["occurrence_binding_sha256"]
                                                  for row in active.values()))
        history_body = {
            "schema": SCHEMA + ".history-node",
            "history_protocol_version": PROTOCOLS["history"],
            "active_universe_binding_sha256": ACTIVE_UNIVERSE_SHA256,
            "transaction_index": expected_index,
            "parent_history_sha256": head,
            "transaction_binding_sha256": tx["transaction_binding_sha256"],
            "oracle_task_binding_sha256": task["oracle_task_binding_sha256"],
            "split_decision_sequence_sha256": split_sequence,
            "removed_occurrence_id_sequence_sha256": sequence_digest(removed),
            "inserted_occurrence_id_sequence_sha256": sequence_digest(sorted(
                row["physical_occurrence_id"] for row in inserted
            )),
            "resulting_overlay_occurrence_binding_sequence_sha256": overlay_sequence,
            "resulting_overlay_occurrence_count": len(active),
        }
        next_head = digest(history_body)
        replay.append({
            **history_body, "history_node_sha256": next_head,
            "removed_occurrence_ids": removed,
            "inserted_occurrence_ids": sorted(row["physical_occurrence_id"] for row in inserted),
        })
        inserted_by_tx[expected_index] = inserted
        head = next_head
    target_indices = request["target_transaction_indices"]
    need(all(type(index) is int and index in inserted_by_tx for index in target_indices),
         "target transaction index exists")
    if request["target_mode"] == "ALL_ACTIVE_HISTORY_REPLACEMENTS":
        # This mode is the nested-endpoint-history contract: siblings installed
        # by earlier transactions remain targets after the endpoint child is
        # refined again, so the oracle audits the complete current frontier.
        target = [row for row in active.values()
                  if row["source_kind"] == "HISTORY_REPLACEMENT"]
        target.sort(key=lambda row: row["physical_occurrence_id"])
    else:
        target = [row for index in target_indices for row in inserted_by_tx[index]]
    need(all(row["physical_occurrence_id"] in active for row in target),
         "target replacement remains active at history head")
    return list(active.values()), replay, target, head


def overlap(a0: F, a1: F, b0: F, b1: F) -> tuple[F, F] | None:
    low, high = max(a0, b0), min(a1, b1)
    return (low, high) if low < high else None


def face_incident(row: dict[str, Any], chart: str, axis: str, fixed: F,
                  low: F, high: F) -> tuple[str, tuple[F, F]] | None:
    if not row["rational"] or row["compact_chart"] != chart:
        return None
    if axis == "t":
        extent = overlap(low, high, row["p0"], row["p1"])
        sides = (("LOWER_COORDINATE_SIDE", row["t1"] == fixed),
                 ("UPPER_COORDINATE_SIDE", row["t0"] == fixed))
    else:
        extent = overlap(low, high, row["t0"], row["t1"])
        sides = (("LOWER_COORDINATE_SIDE", row["p1"] == fixed),
                 ("UPPER_COORDINATE_SIDE", row["p0"] == fixed))
    if extent is None:
        return None
    found = [name for name, condition in sides if condition]
    need(len(found) <= 1, "positive occurrence has at most one incident face side")
    return None if not found else (found[0], extent)


def unknown_face_disjoint(row: dict[str, Any], chart: str, axis: str,
                          fixed: F, low: F, high: F) -> bool:
    if row["rational"] or row["compact_chart"] != chart:
        return True
    if axis == "t":
        possible = (row["env_t0"] <= fixed <= row["env_t1"]
                    and overlap(low, high, row["env_p0"], row["env_p1"]) is not None)
    else:
        possible = (row["env_p0"] <= fixed <= row["env_p1"]
                    and overlap(low, high, row["env_t0"], row["env_t1"]) is not None)
    return not possible


def compact_occurrence(row: dict[str, Any], geometric_side: str | None = None,
                       quadrants: list[str] | None = None) -> dict[str, Any]:
    result = {
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
    if geometric_side is not None:
        result["geometric_side"] = geometric_side
    if quadrants is not None:
        result["occupied_quadrants"] = sorted(quadrants)
    return result


def owner(rows: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, bool]:
    need(bool(rows), "nonempty owner incident set")
    minimum = min(row["semantic_path"] for row in rows)
    winners = [row for row in rows if row["semantic_path"] == minimum]
    return (winners[0], True) if len(winners) == 1 else (None, False)


def target_faces(targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in targets:
        t0, t1, p0, p1 = row["t0"], row["t1"], row["p0"], row["p1"]
        for name, axis, fixed, low, high in (
            ("t_lower", "t", t0, p0, p1), ("t_upper", "t", t1, p0, p1),
            ("p_lower", "p", p0, t0, t1), ("p_upper", "p", p1, t0, t1),
        ):
            output.append({
                "target_occurrence_id": row["physical_occurrence_id"],
                "face": name, "chart": row["compact_chart"], "axis": axis,
                "fixed": fixed, "low": low, "high": high,
            })
    return output


def face_ledger(overlay: list[dict[str, Any]], targets: list[dict[str, Any]]) \
        -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    atom_targets: dict[tuple[str, str, F, F, F], list[dict[str, Any]]] = {}
    occurrences: list[dict[str, Any]] = []
    for target in target_faces(targets):
        breaks = {target["low"], target["high"]}
        for row in overlay:
            found = face_incident(row, target["chart"], target["axis"],
                                  target["fixed"], target["low"], target["high"])
            if found is not None:
                breaks.update(found[1])
        ordered = sorted(breaks)
        for low, high in zip(ordered, ordered[1:]):
            if low == high:
                continue
            key = (target["chart"], target["axis"], target["fixed"], low, high)
            ref = {"target_occurrence_id": target["target_occurrence_id"],
                   "face": target["face"]}
            atom_targets.setdefault(key, [])
            if ref not in atom_targets[key]:
                atom_targets[key].append(ref)
            occurrences.append({"key": key, **ref})
    rows: list[dict[str, Any]] = []
    for key in sorted(atom_targets, key=lambda item: tuple(map(str, item))):
        chart, axis, fixed, low, high = key
        incidents: list[tuple[dict[str, Any], str]] = []
        for row in overlay:
            found = face_incident(row, chart, axis, fixed, low, high)
            if found is not None and found[1][0] <= low and high <= found[1][1]:
                incidents.append((row, found[0]))
        incidents.sort(key=lambda item: item[0]["physical_occurrence_id"])
        by_side = {name: [row for row, side in incidents if side == name]
                   for name in ("LOWER_COORDINATE_SIDE", "UPPER_COORDINATE_SIDE")}
        unknown_safe = all(unknown_face_disjoint(row, chart, axis, fixed, low, high)
                           for row in overlay if not row["rational"])
        compact = [compact_occurrence(row, side) for row, side in incidents]
        selected, unique = owner(compact)
        complete = unknown_safe and all(len(value) == 1 for value in by_side.values())
        geometry = {
            "compact_chart": chart,
            "t": [str(fixed), str(fixed)] if axis == "t" else [str(low), str(high)],
            "p": [str(low), str(high)] if axis == "t" else [str(fixed), str(fixed)],
            "s": ["0", "0"],
        }
        body = {
            "schema": FACE_SCHEMA, "owner_protocol_version": PROTOCOLS["owner"],
            "active_universe_binding_sha256": ACTIVE_UNIVERSE_SHA256,
            "canonical_entity_key": {"compact_chart": chart,
                                     "exact_closed_face_box": geometry},
            "axis": axis,
            "target_occurrence_face_references": sorted(
                atom_targets[key], key=lambda item: (item["target_occurrence_id"], item["face"])),
            "positive_length_face_overlap_only": True,
            "incident_occurrence_count": len(compact),
            "incident_occurrences": compact,
            "incident_occurrence_binding_sequence_sha256": sequence_digest(
                row["occurrence_binding_sha256"] for row in compact),
            "geometric_side_counts": {name: len(value) for name, value in by_side.items()},
            "nonrational_envelope_exclusion_count": sum(not row["rational"] for row in overlay),
            "all_nonrational_occurrences_proven_disjoint": unknown_safe,
            "incident_set_complete": complete,
            "owner_rule": OWNER_RULE, "owner_unique": unique, "owner": selected,
            "formal_credit": 0,
        }
        rows.append({**body, "face_atom_id": "c50a-face:" + digest(body)})
    return rows, occurrences


QUADRANTS = (
    ("t-_p-", -1, -1), ("t-_p+", -1, 1),
    ("t+_p-", 1, -1), ("t+_p+", 1, 1),
)


def quadrants(row: dict[str, Any], t: F, p: F) -> list[str]:
    if not row["rational"]:
        return []
    found = []
    for name, tsign, psign in QUADRANTS:
        t_ok = row["t0"] < t <= row["t1"] if tsign < 0 else row["t0"] <= t < row["t1"]
        p_ok = row["p0"] < p <= row["p1"] if psign < 0 else row["p0"] <= p < row["p1"]
        if t_ok and p_ok:
            found.append(name)
    return found


def unknown_corner_disjoint(row: dict[str, Any], chart: str, t: F, p: F) -> bool:
    return (row["rational"] or row["compact_chart"] != chart
            or not (row["env_t0"] <= t <= row["env_t1"]
                    and row["env_p0"] <= p <= row["env_p1"]))


def corner_ledger(overlay: list[dict[str, Any]], targets: list[dict[str, Any]],
                  faces: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    points: set[tuple[str, F, F]] = set()
    for face in faces:
        box = face["canonical_entity_key"]["exact_closed_face_box"]
        chart = box["compact_chart"]
        if face["axis"] == "t":
            points.add((chart, F(box["t"][0]), F(box["p"][0])))
            points.add((chart, F(box["t"][0]), F(box["p"][1])))
        else:
            points.add((chart, F(box["t"][0]), F(box["p"][0])))
            points.add((chart, F(box["t"][1]), F(box["p"][0])))
    rows = []
    target_corner_count = 0
    for chart, t, p in sorted(points, key=lambda item: tuple(map(str, item))):
        boundary, corners = [], []
        for target in targets:
            if target["compact_chart"] != chart:
                continue
            if target["t0"] <= t <= target["t1"] and target["p0"] <= p <= target["p1"] \
                    and (t in {target["t0"], target["t1"]}
                         or p in {target["p0"], target["p1"]}):
                boundary.append(target["physical_occurrence_id"])
            if t in {target["t0"], target["t1"]} and p in {target["p0"], target["p1"]}:
                corners.append(target["physical_occurrence_id"])
                target_corner_count += 1
        incident_pairs = []
        qmap: dict[str, list[str]] = {name: [] for name, _t, _p in QUADRANTS}
        for occurrence_row in overlay:
            if occurrence_row["compact_chart"] != chart:
                continue
            occupied = quadrants(occurrence_row, t, p)
            if occupied:
                incident_pairs.append((occurrence_row, occupied))
                for quadrant in occupied:
                    qmap[quadrant].append(occurrence_row["physical_occurrence_id"])
        incident_pairs.sort(key=lambda item: item[0]["physical_occurrence_id"])
        compact = [compact_occurrence(row, quadrants=occupied)
                   for row, occupied in incident_pairs]
        selected, unique = owner(compact)
        unknown_safe = all(unknown_corner_disjoint(row, chart, t, p)
                           for row in overlay if not row["rational"])
        complete = unknown_safe and all(len(value) == 1 for value in qmap.values())
        count = len(compact)
        kind = {1: "SINGLE_CELL_CORNER", 2: "TWO_CELL_FACE_VERTEX",
                3: "THREE_WAY_T_JUNCTION", 4: "FOUR_WAY_CROSS_JUNCTION"}.get(
                    count, "OTHER_INCIDENT_CENSUS")
        body = {
            "schema": CORNER_SCHEMA, "owner_protocol_version": PROTOCOLS["owner"],
            "active_universe_binding_sha256": ACTIVE_UNIVERSE_SHA256,
            "canonical_entity_key": {
                "compact_chart": chart,
                "exact_closed_corner_box": {
                    "compact_chart": chart, "t": [str(t), str(t)],
                    "p": [str(p), str(p)], "s": ["0", "0"],
                },
            },
            "junction_kind": kind,
            "target_boundary_occurrence_ids": sorted(boundary),
            "target_corner_occurrence_ids": sorted(corners),
            "incident_occurrence_count": count, "incident_occurrences": compact,
            "incident_occurrence_binding_sequence_sha256": sequence_digest(
                row["occurrence_binding_sha256"] for row in compact),
            "quadrant_incident_occurrence_ids": {
                key: sorted(value) for key, value in sorted(qmap.items())},
            "nonrational_envelope_exclusion_count": sum(not row["rational"] for row in overlay),
            "all_nonrational_occurrences_proven_disjoint": unknown_safe,
            "four_quadrant_germ_complete": complete, "incident_set_complete": complete,
            "owner_rule": OWNER_RULE, "owner_unique": unique, "owner": selected,
            "formal_credit": 0,
        }
        rows.append({**body, "corner_entity_id": "c50a-corner:" + digest(body)})
    return rows, target_corner_count


def build(request: dict[str, Any]) -> dict[str, Any]:
    request_check(request)
    baseline, _ambient, universe_replay = load_active_universe()
    overlay, history_replay, targets, head = apply_history(request, baseline)
    faces, face_occurrences = face_ledger(overlay, targets)
    corners, target_corner_count = corner_ledger(overlay, targets, faces)
    faces_complete = all(row["incident_set_complete"] and row["owner_unique"]
                         and row["incident_occurrence_count"] == 2 for row in faces)
    corners_complete = all(row["incident_set_complete"] and row["owner_unique"]
                           for row in corners)
    need(faces_complete, "all target face atoms have complete degree-two owners")
    need(corners_complete, "all target corners have complete four-quadrant owners")
    body = {
        "schema": SCHEMA,
        "status": "PASS_C50A_GENERIC_TWO_SIDE_HISTORY_BOUND_FULL_UNIVERSE_OWNER_ORACLE__ZERO_FORMAL_CREDIT",
        "producer": {"path": str(SELF.relative_to(ROOT)), "sha256": file_sha256(SELF)},
        "request": request,
        "request_object_sha256": request["request_object_sha256"],
        "active_universe_replay": {
            **universe_replay,
            "active_universe_binding_sha256": ACTIVE_UNIVERSE_SHA256,
            "final_overlay_occurrence_count": len(overlay),
            "final_overlay_occurrence_binding_sequence_sha256": sequence_digest(sorted(
                row["occurrence_binding_sha256"] for row in overlay)),
        },
        "history_replay": {
            "history_protocol_version": PROTOCOLS["history"],
            "genesis_sha256": GENESIS_SHA256, "transaction_count": len(history_replay),
            "history_nodes": history_replay, "history_head_sha256": head,
        },
        "target_replay": {
            "target_mode": request["target_mode"],
            "target_transaction_indices": request["target_transaction_indices"],
            "target_occurrence_count": len(targets),
            "target_occurrence_id_sequence_sha256": sequence_digest(sorted(
                row["physical_occurrence_id"] for row in targets)),
        },
        "owner_ledger": {
            "owner_protocol_version": PROTOCOLS["owner"],
            "face_atom_count": len(faces), "face_atoms": faces,
            "face_atom_id_sequence_sha256": sequence_digest(
                row["face_atom_id"] for row in faces),
            "target_face_atom_occurrence_count": len(face_occurrences),
            "all_face_atoms_degree_two": all(row["incident_occurrence_count"] == 2
                                             for row in faces),
            "all_face_incident_sets_complete": faces_complete,
            "corner_entity_count": len(corners), "corner_entities": corners,
            "corner_entity_id_sequence_sha256": sequence_digest(
                row["corner_entity_id"] for row in corners),
            "target_corner_occurrence_count": target_corner_count,
            "all_corner_four_quadrant_germs_complete": corners_complete,
            "all_codimension_owners_unique": faces_complete and corners_complete,
            "formal_credit": 0,
        },
        "independence_and_scope": {
            "C48_producer_imported_or_executed": False,
            "C41_or_C32_producer_imported_or_executed": False,
            "frozen_ledgers_consumed_as_data_only": True,
            "arbitrary_task_and_history_request_supported": True,
            "nonrational_occurrences_require_conservative_C32_envelope_disjointness": True,
            "cross_chart_or_unknown_envelope_contact_rejects_fail_closed": True,
        },
        "strict_nonpromotion": {
            "runtime_writes_performed": False, "authority_or_pointer_modified": False,
            "seal_or_receipt_created": False, "D02_gate_credit": 0,
            "D02_A_complete": False, "D02_B_complete": False,
            "D02_C_started": False, "D03_started": False,
            "CM2": "NO-GO_FOR_CLAIM", "formal_credit": 0,
        },
        "formal_credit": 0,
    }
    return {**body, "object_sha256": digest(body)}


def self_test() -> dict[str, Any]:
    tests = []
    need(digest({"b": 1, "a": 2}) == digest({"a": 2, "b": 1}), "canonical keys")
    tests.append("canonical JSON key ordering")
    need(ACTIVE_UNIVERSE_SHA256 == digest(ACTIVE_UNIVERSE), "universe binding")
    tests.append("active-universe version binding")
    need(GENESIS_SHA256 == digest(GENESIS_BODY), "genesis binding")
    tests.append("history genesis binding")
    frontier = ["0", "10", "11"]
    need(sum((F(1, 2 ** len(path)) for path in frontier), F(0)) == 1,
         "Kraft self-test")
    tests.append("exact prefix-free Kraft one")
    need(overlap(F(0), F(1), F(1), F(2)) is None, "corner-only overlap")
    tests.append("face overlap excludes corner-only contact")
    body = {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_C50A_PURE_PROTOCOL_SELF_TEST__NO_FULL_REPLAY__ZERO_CREDIT",
        "test_count": len(tests), "tests": tests,
        "full_universe_read": False, "runtime_writes_performed": False,
        "formal_credit": 0,
    }
    return {**body, "object_sha256": digest(body)}


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")
    sys.stdout.buffer.flush()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--emit-c48-request", action="store_true")
    modes.add_argument("--materialize-c48-fixture", action="store_true")
    modes.add_argument("--request", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            result = self_test()
        elif args.emit_c48_request:
            result = build_c48_request()
        else:
            if args.materialize_c48_fixture:
                request = build_c48_request()
            else:
                raw = stable_read(args.request.absolute(), "external owner-oracle request")
                request = json_value(raw, "external owner-oracle request")
            result = build(request)
        emit(result)
        return 0
    except (Reject, OSError, ValueError, KeyError, TypeError, StopIteration,
            gzip.BadGzipFile, json.JSONDecodeError) as error:
        body = {
            "schema": SCHEMA + ".fail-closed", "status": "REJECTED",
            "error_class": type(error).__name__, "reason": str(error),
            "runtime_writes_performed": False, "formal_credit": 0,
        }
        emit({**body, "object_sha256": digest(body)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
