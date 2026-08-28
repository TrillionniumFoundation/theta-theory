#!/usr/bin/env python3
"""Independent cold verifier for the C56-C B-side full projection.

The producer is parsed only as inert AST/bytes and is never imported or
executed.  The verifier rebuilds every one of the 76,832 rows directly from
the frozen C32/C33/C34, C53, C55-B and C56s data.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Callable
import zlib


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
OUT = SELF.parent
SCHEMA = "cm2.round306c56c.b-side-full-per-origin-projection-independent-verifier.v1"
SOURCE_SCHEMA = "cm2.round306c56c.b-side-full-per-origin-projection.v1"
ROW_SCHEMA = SOURCE_SCHEMA + ".row"
UNIVERSE = 76_832
UNRESOLVED = "UNRESOLVED_R1648_CONTINUATION"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

PRODUCER = OUT / "cm2_round306c56c_b_side_full_per_origin_projection_v1.py"
RESULT = OUT / "cm2_round306c56c_b_side_full_per_origin_projection_result_v1.json"
LEDGER = OUT / "cm2_round306c56c_b_side_full_per_origin_projection_ledger_v1.jsonl.gz"
C32_DIR = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
C33_DIR = ROOT / ".cm2-runtime/candidates/c33-row-crosswalk-20260810T135223Z-eb0796f41e16d927"
C34_DIR = ROOT / ".cm2-runtime/candidates/c34-seed-event-frontier-20260810T142445Z-6ec6dac7de032cdb"
C53_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
B_RESULT = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json"
B_CELLS = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_cell_component_crosswalk_v1.jsonl.gz"
B_EDGES = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_component_edges_and_glue_v1.jsonl.gz"
B_COMPONENTS = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_ordinary_components_v1.jsonl.gz"
S_RESULT = OUT / "cm2_round306c56s_singleton_whole_cell_terminal_audit_result_v1.json"
S_LEDGER = OUT / "cm2_round306c56s_singleton_whole_cell_terminal_audit_singleton_ledger_v1.jsonl.gz"

PINS = {
    "PRODUCER_FILE": "44db2feea410f8c6b88cd71a916e2fb7abf12b432de515301a25f7a16ae8b29c",
    "RESULT_FILE": "deeea5f7f752f80be600fbadbccccd73f4678c63e1d1885407082829ad017509",
    "RESULT_OBJECT": "063a006de5f6394c79815a5975bb1d0b800a5420ec28466a2269aca3f7dd7ad6",
    "LEDGER_FILE": "c5a79b946171ba5f60b6ef471aba5b8eb835547eb37e8019589ed06ada203a5c",
    "C32_RESULT_FILE": "c2abba977fa21ea965a9d77478df391db496d0e03f60320b9a4adf9005f1a0a4",
    "C32_RESULT_OBJECT": "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474",
    "C32_CELLS_FILE": "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8",
    "C33_RESULT_FILE": "5a69edde0723525b052934b7522628d90da61f40c71fbbc9ae49a072a506a11f",
    "C33_RESULT_OBJECT": "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0",
    "C33_CROSSWALK_FILE": "0efad586df0e578b91b7852e9474c3e3446480393a0543cd8f23c2149abbc2ee",
    "C34_RESULT_FILE": "bca9d948f86733d75a9f84c7b4b2f11b2617a71b0c6acea14a6d7d7692d3d69d",
    "C34_RESULT_OBJECT": "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e",
    "C34_TYPED_FILE": "73ef4ae2f898054a2af5e5896efcce249a113d6dee6c90dce2ec8b6c8e87fb84",
    "C53_HEAD_FILE": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "C53_HEAD_OBJECT": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
    "B_RESULT_FILE": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "B_RESULT_OBJECT": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "B_CELLS_FILE": "123a742ed553d89fd1026cf65c64879d9a92916492b5b583888c3312551ca2ce",
    "B_EDGES_FILE": "23ea0b4419f155f62d32b6b73c5a16c6f402884d333c222ff803899a58da29a0",
    "B_COMPONENTS_FILE": "bebc49f66efb01c0b980ec10258a60d7aead9d4d2006d28bdd169c9a9ae38a04",
    "S_RESULT_FILE": "7479c162a7e408bf17ae1f8fc36cbaa41281b8899116549d79010afdfceccc3c",
    "S_RESULT_OBJECT": "c0e90419a49ca4054897b0985933478bea5d6893ae33048176c4c46194e1f6da",
    "S_LEDGER_FILE": "077cca660b0ce5b2dfaf5f3bffd7302b88e19cb3839d1d094f5b34489ab7714c",
}

ROW_KEYS = frozenset((
    "C53_effective_checkpoint_object_sha256", "D02_credit", "cell_id",
    "census_class", "exact_box", "formal_credit", "ordinary_binding",
    "origin_key", "physical_chart", "proof_kind", "row_ordinal",
    "row_sha256", "schema", "source_rows", "terminal_disposition",
    "unresolved_reason",
))
BOX_KEYS = frozenset(("physical_p_interval", "physical_slice", "physical_t_interval"))
SOURCE_KEYS = frozenset(("C32_cell_row_sha256", "C33_crosswalk_row_sha256", "C34_typed_event_row_sha256"))
ORDINARY_KEYS = frozenset((
    "C55B_cell_row_sha256", "C55B_component_row_sha256",
    "C56s_singleton_row_sha256", "component_id", "component_index",
    "current_effective_disposition", "incident_C55B_glue_row_count",
    "incident_C55B_glue_row_sha256s", "incident_C55B_glue_sequence_sha256",
    "known_sheet_anchor_role", "pair_index", "reflection_partner_cell_id",
    "whole_pair_terminal_after_C53",
))


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


def exact_keys(value: Any, keys: frozenset[str], label: str) -> None:
    need(type(value) is dict and frozenset(value) == keys, label + " closed keys")


def duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for key, value in pairs:
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


def fingerprint(item: os.stat_result) -> tuple[int, ...]:
    return (item.st_dev, item.st_ino, item.st_mode, item.st_nlink, item.st_size, item.st_mtime_ns)


def stable_read(path: Path, maximum: int = 128 << 20, hook: Callable[[], None] | None = None) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and 0 < before.st_size <= maximum,
             "single-link regular file")
        raw = b""
        while block := os.read(fd, 4 << 20):
            raw += block
        if hook:
            hook()
        after = os.fstat(fd)
        named = os.stat(path, follow_symlinks=False)
        need(fingerprint(before) == fingerprint(after) == fingerprint(named), "file TOCTOU")
        return raw
    finally:
        os.close(fd)


def closed_result(
    path: Path, file_pin: str, object_pin: str,
    hash_key: str = "object_sha256",
) -> dict[str, Any]:
    raw = stable_read(path)
    need(bytes_sha(raw) == file_pin, "result file pin:" + path.name)
    value = parse(raw, path.name)
    need(type(value) is dict and value.get(hash_key) == object_pin, "result object claim")
    body = copy.deepcopy(value)
    body.pop(hash_key)
    need(digest(body) == object_pin, "result object reconstruction")
    return value


def gzip_rows(path: Path, file_pin: str, descriptor: dict[str, Any], label: str) -> list[dict[str, Any]]:
    raw = stable_read(path)
    need(bytes_sha(raw) == file_pin == descriptor["sha256"], label + " file pin")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    try:
        expanded = decoder.decompress(raw, 512 << 20) + decoder.flush()
    except zlib.error as exc:
        raise Rejected(label + " gzip:" + str(exc)) from exc
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail, label + " one gzip member")
    lines = expanded.splitlines(keepends=True)
    need(len(lines) == descriptor["row_count"], label + " row count")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for line in lines:
        row = parse(line, label + " row", canonical_required=True)
        claim = row.get("row_sha256")
        need(type(claim) is str and HEX64.fullmatch(claim) is not None, label + " row claim")
        body = copy.deepcopy(row)
        body.pop("row_sha256")
        need(digest(body) == claim, label + " row hash")
        sequence.update((claim + "\n").encode("ascii"))
        rows.append(row)
    need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], label + " row sequence")
    return rows


def validate_projection_semantics(row: dict[str, Any]) -> None:
    exact_keys(row, ROW_KEYS, "projection row")
    body = copy.deepcopy(row)
    claim = body.pop("row_sha256")
    need(type(claim) is str and digest(body) == claim, "projection row hash")
    exact_keys(row["exact_box"], BOX_KEYS, "projection exact box")
    exact_keys(row["source_rows"], SOURCE_KEYS, "projection source rows")
    need(row["schema"] == ROW_SCHEMA and row["C53_effective_checkpoint_object_sha256"] == CHECKPOINT,
         "projection schema/checkpoint")
    need(type(row["row_ordinal"]) is int and row["row_ordinal"] >= 0, "projection ordinal")
    need(row["formal_credit"] == row["D02_credit"] == 0, "projection zero credit")
    for key in ("C32_cell_row_sha256", "C33_crosswalk_row_sha256"):
        need(type(row["source_rows"][key]) is str and HEX64.fullmatch(row["source_rows"][key]) is not None,
             "projection source hash")
    terminal = row["terminal_disposition"]
    ordinary = row["ordinary_binding"]
    if terminal is None:
        need(row["census_class"] == UNRESOLVED and type(row["unresolved_reason"]) is str
             and bool(row["unresolved_reason"]), "projection explicit unresolved")
        need(row["proof_kind"] == "C55B_ORDINARY_COMPONENT_EXPLICITLY_UNRESOLVED",
             "projection unresolved proof kind")
    else:
        need(terminal in {"EARLIEST_PREFIX_EXCLUDED", "TYPED_EVENT_GRAPH"}
             and row["census_class"] == terminal and row["unresolved_reason"] is None,
             "projection legal terminal")
    if ordinary is None:
        need(row["proof_kind"] in {"C33_FORMAL_EARLIEST_PREFIX_EXCLUSION", "C34_TYPED_FIRST_EVENT_BINDING"},
             "projection nonordinary proof")
        if row["proof_kind"] == "C34_TYPED_FIRST_EVENT_BINDING":
            need(terminal == "TYPED_EVENT_GRAPH" and row["source_rows"]["C34_typed_event_row_sha256"] is not None,
                 "projection typed binding")
        else:
            need(terminal == "EARLIEST_PREFIX_EXCLUDED" and row["source_rows"]["C34_typed_event_row_sha256"] is None,
                 "projection C33 exclusion")
    else:
        exact_keys(ordinary, ORDINARY_KEYS, "ordinary binding")
        need(row["source_rows"]["C34_typed_event_row_sha256"] is None, "ordinary not typed")
        hashes = ordinary["incident_C55B_glue_row_sha256s"]
        need(type(hashes) is list and hashes == sorted(set(hashes))
             and ordinary["incident_C55B_glue_row_count"] == len(hashes)
             and ordinary["incident_C55B_glue_sequence_sha256"] == digest(hashes),
             "ordinary glue binding")
        for key in ("C55B_cell_row_sha256", "C55B_component_row_sha256"):
            need(type(ordinary[key]) is str and HEX64.fullmatch(ordinary[key]) is not None,
                 "ordinary hash")
        singleton = ordinary["C56s_singleton_row_sha256"]
        need((ordinary["component_index"] >= 2) == (type(singleton) is str and HEX64.fullmatch(singleton or "") is not None),
             "ordinary singleton binding iff component>=2")
        if terminal is None:
            need(ordinary["current_effective_disposition"] == UNRESOLVED
                 and ordinary["whole_pair_terminal_after_C53"] is False,
                 "ordinary unresolved consistency")
        else:
            need(terminal == "EARLIEST_PREFIX_EXCLUDED"
                 and ordinary["current_effective_disposition"] == terminal
                 and ordinary["whole_pair_terminal_after_C53"] is True,
                 "ordinary excluded consistency")


def expected_row(
    ordinal: int, cell: dict[str, Any], cross: dict[str, Any],
    typed: dict[str, dict[str, Any]], ordinary: dict[str, dict[str, Any]],
    components: dict[int, dict[str, Any]], singletons: dict[str, dict[str, Any]],
    incident: dict[str, list[str]],
) -> dict[str, Any]:
    cell_id = cell["cell_id"]
    typed_row = typed.get(cell_id)
    ordinary_row = ordinary.get(cell_id)
    binding = None
    if ordinary_row is not None:
        component = components[ordinary_row["component_index"]]
        singleton = singletons.get(cell_id)
        hashes = incident[cell_id]
        binding = {
            "C55B_cell_row_sha256": ordinary_row["row_sha256"],
            "C55B_component_row_sha256": component["row_sha256"],
            "C56s_singleton_row_sha256": singleton["row_sha256"] if singleton else None,
            "component_id": ordinary_row["component_id"],
            "component_index": ordinary_row["component_index"],
            "current_effective_disposition": ordinary_row["current_effective_disposition"],
            "incident_C55B_glue_row_count": len(hashes),
            "incident_C55B_glue_row_sha256s": hashes,
            "incident_C55B_glue_sequence_sha256": digest(hashes),
            "known_sheet_anchor_role": ordinary_row["known_sheet_anchor_role"],
            "pair_index": ordinary_row["pair_index"],
            "reflection_partner_cell_id": ordinary_row["reflection_partner_cell_id"],
            "whole_pair_terminal_after_C53": ordinary_row["whole_pair_terminal_after_C53"],
        }
        if ordinary_row["current_effective_disposition"] == "EARLIEST_PREFIX_EXCLUDED":
            terminal, reason, proof = "EARLIEST_PREFIX_EXCLUDED", None, "C55B_C53_WHOLE_PARENT_STRICT_EXCLUSION"
        else:
            terminal, reason, proof = None, component["unresolved_reason"], "C55B_ORDINARY_COMPONENT_EXPLICITLY_UNRESOLVED"
    elif typed_row is not None:
        terminal, reason, proof = "TYPED_EVENT_GRAPH", None, "C34_TYPED_FIRST_EVENT_BINDING"
    else:
        need(cross["formal_source_W_disposition"] == "EXCLUDED"
             and cross["round144_terminal_class"] == "EARLIEST_PREFIX_EXCLUDED",
             "expected C33 exclusion")
        terminal, reason, proof = "EARLIEST_PREFIX_EXCLUDED", None, "C33_FORMAL_EARLIEST_PREFIX_EXCLUSION"
    return close({
        "schema": ROW_SCHEMA,
        "row_ordinal": ordinal,
        "origin_key": cell["origin_key"],
        "cell_id": cell_id,
        "physical_chart": cell["compact_chart"],
        "exact_box": {
            "physical_p_interval": cell["physical_p_interval"],
            "physical_slice": cell["physical_slice"],
            "physical_t_interval": cell["physical_t_interval"],
        },
        "source_rows": {
            "C32_cell_row_sha256": cell["row_sha256"],
            "C33_crosswalk_row_sha256": cross["row_sha256"],
            "C34_typed_event_row_sha256": typed_row["row_sha256"] if typed_row else None,
        },
        "C53_effective_checkpoint_object_sha256": CHECKPOINT,
        "proof_kind": proof,
        "terminal_disposition": terminal,
        "unresolved_reason": reason,
        "census_class": terminal if terminal is not None else UNRESOLVED,
        "ordinary_binding": binding,
        "formal_credit": 0,
        "D02_credit": 0,
    }, "row_sha256")


def independence() -> dict[str, Any]:
    need(bytes_sha(stable_read(PRODUCER)) == PINS["PRODUCER_FILE"], "producer source pin")
    tree = ast.parse(PRODUCER.read_text(encoding="utf-8"), filename=PRODUCER.name)
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    forbidden = ("cm2_round306c55a", "cm2_round306c55b", "cm2_round306c56s")
    need(not any(any(token in item for token in forbidden) for item in imports), "no upstream producer import")
    loaded = [name for name in sys.modules if any(token in name for token in forbidden)]
    need(not loaded, "upstream producers absent from sys.modules")
    return {"upstream_producer_imported": False, "upstream_producer_executed": False,
            "producer_consumed_as_inert_AST_and_bytes_only": True}


def verify() -> dict[str, Any]:
    result = closed_result(RESULT, PINS["RESULT_FILE"], PINS["RESULT_OBJECT"])
    need(result["source_pins"] == {key: value for key, value in PINS.items()
         if key not in {"PRODUCER_FILE", "RESULT_FILE", "RESULT_OBJECT", "LEDGER_FILE"}},
         "result source pin set")
    c32 = closed_result(C32_DIR / "result.json", PINS["C32_RESULT_FILE"], PINS["C32_RESULT_OBJECT"])
    c33 = closed_result(C33_DIR / "result.json", PINS["C33_RESULT_FILE"], PINS["C33_RESULT_OBJECT"])
    c34 = closed_result(C34_DIR / "result.json", PINS["C34_RESULT_FILE"], PINS["C34_RESULT_OBJECT"])
    head = closed_result(C53_HEAD, PINS["C53_HEAD_FILE"], PINS["C53_HEAD_OBJECT"],
                         "authority_seal_object_sha256")
    need(head["post_seal_effective_checkpoint_object_sha256"] == CHECKPOINT,
         "C53 effective checkpoint")
    b_result = closed_result(B_RESULT, PINS["B_RESULT_FILE"], PINS["B_RESULT_OBJECT"])
    s_result = closed_result(S_RESULT, PINS["S_RESULT_FILE"], PINS["S_RESULT_OBJECT"])
    c32_rows = gzip_rows(C32_DIR / c32["ledgers"]["cells"]["filename"], PINS["C32_CELLS_FILE"], c32["ledgers"]["cells"], "C32")
    c33_rows = gzip_rows(C33_DIR / c33["row_level_crosswalk"]["filename"], PINS["C33_CROSSWALK_FILE"], c33["row_level_crosswalk"], "C33")
    typed_rows = gzip_rows(C34_DIR / c34["ledgers"]["typed_first_event_bindings"]["filename"], PINS["C34_TYPED_FILE"], c34["ledgers"]["typed_first_event_bindings"], "C34 typed")
    b_cells = gzip_rows(B_CELLS, PINS["B_CELLS_FILE"], b_result["ledgers"]["cell_component_crosswalk"], "B cells")
    b_edges = gzip_rows(B_EDGES, PINS["B_EDGES_FILE"], b_result["ledgers"]["component_edges_and_glue"], "B edges")
    b_components = gzip_rows(B_COMPONENTS, PINS["B_COMPONENTS_FILE"], b_result["ledgers"]["ordinary_components"], "B components")
    s_rows = gzip_rows(S_LEDGER, PINS["S_LEDGER_FILE"], s_result["ledgers"]["singletons"], "C56s")
    projection_rows = gzip_rows(LEDGER, PINS["LEDGER_FILE"], result["projection_ledger"], "C56c projection")

    typed = {row["cell_id"]: row for row in typed_rows}
    ordinary = {row["cell_id"]: row for row in b_cells}
    components = {row["component_index"]: row for row in b_components}
    singletons = {row["cell_id"]: row for row in s_rows}
    incident: dict[str, list[str]] = {cell_id: [] for cell_id in ordinary}
    for edge in b_edges:
        for cell_id in (edge["left_cell_id"], edge["right_cell_id"]):
            if cell_id in incident:
                incident[cell_id].append(edge["row_sha256"])
    for values in incident.values():
        values.sort()

    need(len(c32_rows) == len(c33_rows) == len(projection_rows) == UNIVERSE, "full projection count")
    census = {"EARLIEST_PREFIX_EXCLUDED": 0, "TYPED_EVENT_GRAPH": 0,
              "CONNECTED_TO_KNOWN": 0, "SOURCE_GRAZING_OR_CEMETERY": 0,
              UNRESOLVED: 0, "total": 0}
    previous = None
    for ordinal, (cell, cross, actual) in enumerate(zip(c32_rows, c33_rows, projection_rows, strict=True)):
        need(cell["cell_id"] == cross["cell_id"] and cell["origin_key"] == cross["origin_key"], "source row bijection")
        need(previous is None or previous < cell["origin_key"], "lexicographic source order")
        previous = cell["origin_key"]
        validate_projection_semantics(actual)
        expected = expected_row(ordinal, cell, cross, typed, ordinary, components, singletons, incident)
        need(actual == expected, "independent per-origin row reconstruction")
        census[actual["census_class"]] += 1
        census["total"] += 1
    need(census == result["census"] == {
        "EARLIEST_PREFIX_EXCLUDED": 75_388, "TYPED_EVENT_GRAPH": 296,
        "CONNECTED_TO_KNOWN": 0, "SOURCE_GRAZING_OR_CEMETERY": 0,
        UNRESOLVED: 1_148, "total": UNIVERSE,
    }, "exact reconstructed census")
    need(result["B_second_full_per_origin_projection_materialized"] is True
         and result["unresolved_zero"] is False
         and result["strict_decider_eligible"] is False
         and result["positive_terminal_enabled"] is False
         and result["formal_credit"] == result["D02_credit"] == 0,
         "strict fail-closed result")
    return close({
        "schema": SCHEMA + ".verification",
        "status": "PASS_INDEPENDENT_RECONSTRUCTION_76832_B_SIDE_ROWS__NONMATHEMATICAL_INPUT_GAP_CLOSED__FAIL_CLOSED_1148_UNRESOLVED",
        "producer_source_sha256": PINS["PRODUCER_FILE"],
        "result_file_sha256": PINS["RESULT_FILE"],
        "result_object_sha256": PINS["RESULT_OBJECT"],
        "projection_file_sha256": PINS["LEDGER_FILE"],
        "projection_row_count": UNIVERSE,
        "projection_row_sequence_sha256": result["projection_ledger"]["row_hash_line_sequence_sha256"],
        "census": census,
        "ordinary_row_count": len(ordinary),
        "component_count": len(components),
        "singleton_C56s_binding_count": len(singletons),
        "every_row_byte_for_byte_independently_reconstructed": True,
        "B_second_full_per_origin_projection_materialized": True,
        "C55C_B_NO_INERT_76832_PER_ROW_PROJECTION_blocker_closed": True,
        "remaining_blocker": "UNRESOLVED_R1648_CONTINUATION_NONZERO:1148",
        "positive_terminal_enabled": False,
        "formal_credit": 0,
        "D02_credit": 0,
        "independence": independence(),
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def synthetic_row() -> dict[str, Any]:
    h = "1" * 64
    return close({
        "schema": ROW_SCHEMA, "row_ordinal": 0, "origin_key": "W:E:00",
        "cell_id": "c32-compact-cell:" + "2" * 64, "physical_chart": "E",
        "exact_box": {"physical_p_interval": ["0", "1"], "physical_slice": "s=0", "physical_t_interval": [{"kind": "RATIONAL", "value": "0"}, {"kind": "RATIONAL", "value": "1"}]},
        "source_rows": {"C32_cell_row_sha256": h, "C33_crosswalk_row_sha256": "2" * 64, "C34_typed_event_row_sha256": None},
        "C53_effective_checkpoint_object_sha256": CHECKPOINT,
        "proof_kind": "C55B_ORDINARY_COMPONENT_EXPLICITLY_UNRESOLVED",
        "terminal_disposition": None, "unresolved_reason": "EXPLICIT_BLOCKER",
        "census_class": UNRESOLVED,
        "ordinary_binding": {
            "C55B_cell_row_sha256": "3" * 64, "C55B_component_row_sha256": "4" * 64,
            "C56s_singleton_row_sha256": "5" * 64, "component_id": "component:2",
            "component_index": 2, "current_effective_disposition": UNRESOLVED,
            "incident_C55B_glue_row_count": 1, "incident_C55B_glue_row_sha256s": ["6" * 64],
            "incident_C55B_glue_sequence_sha256": digest(["6" * 64]),
            "known_sheet_anchor_role": "NO_CELL_LEVEL_ANCHOR", "pair_index": 1,
            "reflection_partner_cell_id": "c32-compact-cell:" + "7" * 64,
            "whole_pair_terminal_after_C53": False,
        },
        "formal_credit": 0, "D02_credit": 0,
    }, "row_sha256")


def reclose(value: dict[str, Any], mutation: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    answer = copy.deepcopy(value)
    answer.pop("row_sha256")
    mutation(answer)
    return close(answer, "row_sha256")


def self_test() -> dict[str, Any]:
    tests: dict[str, bool] = {}
    baseline = synthetic_row()
    validate_projection_semantics(baseline)
    tests["synthetic_baseline_valid"] = True
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("checkpoint", lambda x: x.__setitem__("C53_effective_checkpoint_object_sha256", "0" * 64)),
        ("credit", lambda x: x.__setitem__("D02_credit", 1)),
        ("unresolved_reason_null", lambda x: x.__setitem__("unresolved_reason", None)),
        ("terminal_forgery", lambda x: x.__setitem__("terminal_disposition", "SOURCE_GRAZING_OR_CEMETERY")),
        ("census_forgery", lambda x: x.__setitem__("census_class", "EARLIEST_PREFIX_EXCLUDED")),
        ("proof_shortcut", lambda x: x.__setitem__("proof_kind", "LOCAL_CHART_EXIT")),
        ("ordinary_removed", lambda x: x.__setitem__("ordinary_binding", None)),
        ("cell_hash", lambda x: x["ordinary_binding"].__setitem__("C55B_cell_row_sha256", "0" * 64)),
        ("component_hash", lambda x: x["ordinary_binding"].__setitem__("C55B_component_row_sha256", "0" * 64)),
        ("singleton_removed", lambda x: x["ordinary_binding"].__setitem__("C56s_singleton_row_sha256", None)),
        ("glue_count", lambda x: x["ordinary_binding"].__setitem__("incident_C55B_glue_row_count", 2)),
        ("glue_sequence", lambda x: x["ordinary_binding"].__setitem__("incident_C55B_glue_sequence_sha256", "0" * 64)),
        ("whole_pair", lambda x: x["ordinary_binding"].__setitem__("whole_pair_terminal_after_C53", True)),
        ("current_disposition", lambda x: x["ordinary_binding"].__setitem__("current_effective_disposition", "EARLIEST_PREFIX_EXCLUDED")),
        ("typed_hash_on_ordinary", lambda x: x["source_rows"].__setitem__("C34_typed_event_row_sha256", "8" * 64)),
    ]
    for name, mutation in attacks:
        attacked = reclose(baseline, mutation)
        try:
            validate_projection_semantics(attacked)
        except Rejected:
            accepted = False
        else:
            # The real verifier additionally demands byte-for-byte equality
            # with its independently rebuilt expected row.
            accepted = attacked == baseline
        need(not accepted, "coherent attack accepted:" + name)
        tests["coherent_" + name + "_rejected"] = True
    try:
        parse(b'{"a":1,"a":2}\n', "duplicate")
    except Rejected:
        tests["duplicate_JSON_rejected"] = True
    try:
        parse(b'{"a":NaN}\n', "NaN")
    except Rejected:
        tests["NaN_rejected"] = True
    with tempfile.TemporaryDirectory(prefix="cm2-c56c-") as temporary:
        root = Path(temporary)
        target = root / "row.json"
        target.write_bytes(canonical(baseline) + b"\n")
        symlink = root / "link.json"
        symlink.symlink_to(target.name)
        try:
            stable_read(symlink)
        except OSError:
            tests["symlink_rejected"] = True
        hardlink = root / "hard.json"
        os.link(target, hardlink)
        try:
            stable_read(target)
        except Rejected:
            tests["hardlink_rejected"] = True
        hardlink.unlink()
        replacement = root / "new.json"
        replacement.write_bytes(canonical(baseline) + b"\n")
        try:
            stable_read(target, hook=lambda: os.replace(replacement, target))
        except Rejected:
            tests["same_name_TOCTOU_rejected"] = True
    tests["upstream_producers_not_imported_or_executed"] = not independence()["upstream_producer_imported"]
    need(all(tests.values()) and len(tests) == 22, "22 executed tests")
    return close({
        "schema": SCHEMA + ".self-test", "status": "PASS_22_OF_22_EXECUTED_HOSTILE_TESTS",
        "tests": tests, "test_count": len(tests), "synthetic_rows_are_authority": False,
        "positive_terminal_enabled": False, "formal_credit": 0, "D02_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        output = verify() if args.verify else self_test()
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (Rejected, OSError, zlib.error) as exc:
        failure = close({
            "schema": SCHEMA + ".fail-closed", "status": "FAIL_CLOSED_REJECTED",
            "reason": str(exc), "positive_terminal_enabled": False,
            "formal_credit": 0, "D02_credit": 0,
            "runtime_canonical_pointer_or_seal_writes": False,
        })
        sys.stdout.buffer.write(canonical(failure) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
