#!/usr/bin/env python3
"""Materialize an inert B-side 76,832-row projection for the strict decider.

No upstream producer is imported or executed.  The implementation consumes
only frozen JSON/JSONL bytes and publishes only new round306c56c files.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any
import zlib


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
OUT = SELF.parent
SCHEMA = "cm2.round306c56c.b-side-full-per-origin-projection.v1"
ROW_SCHEMA = SCHEMA + ".row"
RESULT_SCHEMA = SCHEMA + ".result"
PREFIX = "cm2_round306c56c_b_side_full_per_origin_projection"
LEDGER_NAME = PREFIX + "_ledger_v1.jsonl.gz"
RESULT_NAME = PREFIX + "_result_v1.json"
LEDGER_PATH = OUT / LEDGER_NAME
RESULT_PATH = OUT / RESULT_NAME
UNIVERSE = 76_832
UNRESOLVED = "UNRESOLVED_R1648_CONTINUATION"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

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


class FailClosed(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise FailClosed(label)


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
            raise FailClosed("duplicate JSON key:" + key)
        answer[key] = value
    return answer


def parse(raw: bytes, label: str) -> Any:
    need(not raw.startswith(b"\xef\xbb\xbf") and bool(raw), label + " strict bytes")
    try:
        return json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=duplicate_guard,
            parse_constant=lambda token: (_ for _ in ()).throw(FailClosed(label + ":" + token)),
        )
    except FailClosed:
        raise
    except Exception as exc:
        raise FailClosed(label + " strict JSON:" + str(exc)) from exc


def stable_read(path: Path, maximum: int = 64 << 20) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and 0 < before.st_size <= maximum,
             "stable regular single-link input:" + path.name)
        chunks: list[bytes] = []
        while block := os.read(fd, 4 << 20):
            chunks.append(block)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        named = os.stat(path, follow_symlinks=False)
        fp = lambda item: (item.st_dev, item.st_ino, item.st_mode, item.st_nlink, item.st_size, item.st_mtime_ns)
        need(fp(before) == fp(after) == fp(named), "stable input TOCTOU:" + path.name)
        return raw
    finally:
        os.close(fd)


def closed_result(path: Path, file_pin: str, object_pin: str, hash_key: str = "object_sha256") -> dict[str, Any]:
    raw = stable_read(path)
    need(bytes_sha(raw) == file_pin, "result file pin:" + path.name)
    value = parse(raw, path.name)
    need(type(value) is dict and value.get(hash_key) == object_pin, "result object claim:" + path.name)
    body = copy.deepcopy(value)
    body.pop(hash_key)
    need(digest(body) == object_pin, "result object hash:" + path.name)
    return value


def gzip_rows(path: Path, file_pin: str, descriptor: dict[str, Any], label: str) -> list[dict[str, Any]]:
    raw = stable_read(path)
    need(bytes_sha(raw) == file_pin == descriptor["sha256"], label + " file pin")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    expanded = decoder.decompress(raw, 512 << 20) + decoder.flush()
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail, label + " one complete gzip member")
    lines = expanded.splitlines(keepends=True)
    need(len(lines) == descriptor["row_count"] and all(line.endswith(b"\n") for line in lines), label + " row count")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    for line in lines:
        row = parse(line, label + " row")
        need(type(row) is dict and line == canonical(row) + b"\n", label + " canonical row")
        claim = row.get("row_sha256")
        need(type(claim) is str and HEX64.fullmatch(claim) is not None, label + " row claim")
        body = copy.deepcopy(row)
        body.pop("row_sha256")
        need(digest(body) == claim, label + " row hash")
        sequence.update((claim + "\n").encode("ascii"))
        rows.append(row)
    need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], label + " row sequence")
    return rows


def publish_noreplace(path: Path, raw: bytes) -> None:
    if path.exists():
        need(stable_read(path, maximum=max(64 << 20, len(raw) + 1)) == raw, "existing output byte exact:" + path.name)
        return
    fd, name = tempfile.mkstemp(prefix=path.name + ".tmp-", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
        os.chmod(path, 0o444)
    finally:
        temporary.unlink(missing_ok=True)


def build() -> dict[str, Any]:
    c32 = closed_result(C32_DIR / "result.json", PINS["C32_RESULT_FILE"], PINS["C32_RESULT_OBJECT"])
    c33 = closed_result(C33_DIR / "result.json", PINS["C33_RESULT_FILE"], PINS["C33_RESULT_OBJECT"])
    c34 = closed_result(C34_DIR / "result.json", PINS["C34_RESULT_FILE"], PINS["C34_RESULT_OBJECT"])
    head = closed_result(C53_HEAD, PINS["C53_HEAD_FILE"], PINS["C53_HEAD_OBJECT"], "authority_seal_object_sha256")
    b_result = closed_result(B_RESULT, PINS["B_RESULT_FILE"], PINS["B_RESULT_OBJECT"])
    s_result = closed_result(S_RESULT, PINS["S_RESULT_FILE"], PINS["S_RESULT_OBJECT"])
    need(head["post_seal_effective_checkpoint_object_sha256"] == CHECKPOINT, "C53 checkpoint")

    c32_rows = gzip_rows(C32_DIR / c32["ledgers"]["cells"]["filename"], PINS["C32_CELLS_FILE"], c32["ledgers"]["cells"], "C32 cells")
    c33_rows = gzip_rows(C33_DIR / c33["row_level_crosswalk"]["filename"], PINS["C33_CROSSWALK_FILE"], c33["row_level_crosswalk"], "C33 crosswalk")
    typed_rows = gzip_rows(C34_DIR / c34["ledgers"]["typed_first_event_bindings"]["filename"], PINS["C34_TYPED_FILE"], c34["ledgers"]["typed_first_event_bindings"], "C34 typed")
    b_cells = gzip_rows(B_CELLS, PINS["B_CELLS_FILE"], b_result["ledgers"]["cell_component_crosswalk"], "C55B cells")
    b_edges = gzip_rows(B_EDGES, PINS["B_EDGES_FILE"], b_result["ledgers"]["component_edges_and_glue"], "C55B edges")
    b_components = gzip_rows(B_COMPONENTS, PINS["B_COMPONENTS_FILE"], b_result["ledgers"]["ordinary_components"], "C55B components")
    s_rows = gzip_rows(S_LEDGER, PINS["S_LEDGER_FILE"], s_result["ledgers"]["singletons"], "C56s singletons")

    need(len(c32_rows) == len(c33_rows) == UNIVERSE, "full row universe")
    typed = {row["cell_id"]: row for row in typed_rows}
    ordinary = {row["cell_id"]: row for row in b_cells}
    components = {row["component_index"]: row for row in b_components}
    singletons = {row["cell_id"]: row for row in s_rows}
    need(len(typed) == 296 and len(ordinary) == 1_724 and not set(typed) & set(ordinary), "typed/ordinary partition")
    need(len(components) == 26 and len(singletons) == 24, "component/singleton census")

    incident: dict[str, list[str]] = {cell_id: [] for cell_id in ordinary}
    for edge in b_edges:
        for cell_id in (edge["left_cell_id"], edge["right_cell_id"]):
            if cell_id in incident:
                incident[cell_id].append(edge["row_sha256"])
    for hashes in incident.values():
        hashes.sort()

    census = {"EARLIEST_PREFIX_EXCLUDED": 0, "TYPED_EVENT_GRAPH": 0,
              "CONNECTED_TO_KNOWN": 0, "SOURCE_GRAZING_OR_CEMETERY": 0,
              UNRESOLVED: 0, "total": 0}
    sequence = hashlib.sha256()
    row_count = 0
    fd, temporary_name = tempfile.mkstemp(prefix=LEDGER_NAME + ".tmp-", dir=OUT)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as raw_stream:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw_stream, mtime=0) as stream:
                previous_origin = None
                seen: set[str] = set()
                for ordinal, (cell, cross) in enumerate(zip(c32_rows, c33_rows, strict=True)):
                    need(cell["cell_id"] == cross["cell_id"] and cell["origin_key"] == cross["origin_key"], "C32/C33 ordered bijection")
                    need(cell["cell_id"] not in seen and (previous_origin is None or previous_origin < cell["origin_key"]), "unique lexicographic origin order")
                    seen.add(cell["cell_id"])
                    previous_origin = cell["origin_key"]
                    cell_id = cell["cell_id"]
                    typed_row = typed.get(cell_id)
                    ordinary_row = ordinary.get(cell_id)
                    ordinary_binding = None
                    if ordinary_row is not None:
                        component = components[ordinary_row["component_index"]]
                        singleton = singletons.get(cell_id)
                        hashes = incident[cell_id]
                        ordinary_binding = {
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
                            terminal, unresolved_reason, proof_kind = "EARLIEST_PREFIX_EXCLUDED", None, "C55B_C53_WHOLE_PARENT_STRICT_EXCLUSION"
                        else:
                            terminal, unresolved_reason, proof_kind = None, component["unresolved_reason"], "C55B_ORDINARY_COMPONENT_EXPLICITLY_UNRESOLVED"
                    elif typed_row is not None:
                        terminal, unresolved_reason, proof_kind = "TYPED_EVENT_GRAPH", None, "C34_TYPED_FIRST_EVENT_BINDING"
                    else:
                        need(cross["formal_source_W_disposition"] == "EXCLUDED" and cross["round144_terminal_class"] == "EARLIEST_PREFIX_EXCLUDED", "C33 strict excluded complement")
                        terminal, unresolved_reason, proof_kind = "EARLIEST_PREFIX_EXCLUDED", None, "C33_FORMAL_EARLIEST_PREFIX_EXCLUSION"
                    census_class = terminal if terminal is not None else UNRESOLVED
                    row = {
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
                        "proof_kind": proof_kind,
                        "terminal_disposition": terminal,
                        "unresolved_reason": unresolved_reason,
                        "census_class": census_class,
                        "ordinary_binding": ordinary_binding,
                        "formal_credit": 0,
                        "D02_credit": 0,
                    }
                    complete = close(row, "row_sha256")
                    stream.write(canonical(complete) + b"\n")
                    sequence.update((complete["row_sha256"] + "\n").encode("ascii"))
                    census[census_class] += 1
                    census["total"] += 1
                    row_count += 1
            raw_stream.flush()
            os.fsync(raw_stream.fileno())
        need(row_count == UNIVERSE and census == {
            "EARLIEST_PREFIX_EXCLUDED": 75_388, "TYPED_EVENT_GRAPH": 296,
            "CONNECTED_TO_KNOWN": 0, "SOURCE_GRAZING_OR_CEMETERY": 0,
            UNRESOLVED: 1_148, "total": UNIVERSE,
        }, "exact current census")
        ledger_raw = stable_read(temporary, maximum=128 << 20)
        publish_noreplace(LEDGER_PATH, ledger_raw)
    finally:
        temporary.unlink(missing_ok=True)

    ledger_raw = stable_read(LEDGER_PATH, maximum=128 << 20)
    result = close({
        "schema": RESULT_SCHEMA,
        "status": "PASS_INERT_B_SIDE_76832_PER_ORIGIN_PROJECTION__FAIL_CLOSED_1148_UNRESOLVED",
        "verifier_boundary": "NO_UPSTREAM_PRODUCER_IMPORTED_OR_EXECUTED",
        "C53_effective_checkpoint_object_sha256": CHECKPOINT,
        "source_pins": PINS,
        "projection_ledger": {
            "filename": LEDGER_NAME,
            "order": "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
            "row_count": row_count,
            "row_hash_line_sequence_sha256": sequence.hexdigest(),
            "sha256": bytes_sha(ledger_raw),
            "size": len(ledger_raw),
        },
        "census": census,
        "ordinary_binding": {
            "ordinary_row_count": len(ordinary),
            "component_count": len(components),
            "singleton_C56s_row_count": len(singletons),
            "every_ordinary_row_binds_C55B_cell_component_and_incident_glue": True,
        },
        "B_second_full_per_origin_projection_materialized": True,
        "unresolved_zero": False,
        "strict_decider_eligible": False,
        "positive_terminal_enabled": False,
        "formal_credit": 0,
        "D02_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })
    result_raw = canonical(result) + b"\n"
    publish_noreplace(RESULT_PATH, result_raw)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    if not args.build:
        parser.error("--build required")
    try:
        result = build()
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 0
    except (FailClosed, OSError, zlib.error) as exc:
        failure = close({
            "schema": SCHEMA + ".fail-closed",
            "status": "FAIL_CLOSED_REJECTED",
            "reason": str(exc),
            "positive_terminal_enabled": False,
            "formal_credit": 0,
            "D02_credit": 0,
            "runtime_canonical_pointer_or_seal_writes": False,
        })
        sys.stdout.buffer.write(canonical(failure) + b"\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
