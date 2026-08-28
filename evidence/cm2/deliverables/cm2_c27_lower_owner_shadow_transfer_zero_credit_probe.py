#!/usr/bin/env python3
"""Fail-closed audit of the 24 DOUBLE_GRAPHS lower-owner contacts.

This probe deliberately separates two statements which must never be
conflated:

1. the contact locus is outside the target occurrence's OPEN_RATIONAL_BOX;
2. the contact locus has a unique lower-dimensional physical owner whose
   support and C15 component lineage are known.

The first statement is proved exactly for all 24 contacts.  The second is
resolved independently of the positive-t retained child: the complete R248
source endpoint-sheet ledger is itself the physical t=0 owner cover.  Every
contact locus is covered by one or two current source sheets, and every such
sheet is in the same unique C15 component as the discovered source sheet.
Thus the target occurrence is absent at the contact and the complete t=0
owner component is known.  This remains a zero-credit diagnostic until a
second semantic implementation and attacks pass.

Candidates are reconstructed from R236/R248 sheets and the complete R291
physical-cell frontier.  No Round306C27 source, FAMILIES table, or edge
ledger is imported.  Every input is opened once with O_NOFOLLOW; hashing and
parsing consume the same captured bytes, whose descriptors remain open until
after no-replace publication and metadata recheck.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import ctypes
import errno
from fractions import Fraction
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import secrets
import stat
import sys
from typing import Any, Iterator, TextIO


ROOT = Path(__file__).resolve().parent
AUDIT_ROOT = ROOT.parent / ".cm2-runtime" / "audit"
PREFIX = "cm2_c27_lower_owner_shadow_transfer_zero_credit_v1"
LEDGER = PREFIX + "_contact_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
MANIFEST = PREFIX + "_manifest.json"

R236 = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R248 = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R291 = "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz"
R295A = "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_physical_witness_incidence_binding_ledger.json.gz"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C22B = "cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_ledger.jsonl.gz"
R281_RESULT = "cm2_round281_source_g_lower_stratum_tail_closure_result.json"
R281_LEDGER = "cm2_round281_source_g_lower_stratum_tail_closure_ledger.json.gz"
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R204 = "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
R267 = "cm2_round267_source_g_lower_stratum_terminal_lineage_certificate.json"

INPUT_PINS = {
    R236: "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    R248: "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    R291: "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    R295A: "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C22B: "c0f3d3a9fc6002f0af23271f7483aeff7eac0b0cc92399fc3785b0a5b9291f97",
    R281_RESULT: "84ea62964c4199bdec66f7a82cfdee964b8b2b610f9c8c1c6298cc6fbaf1942c",
    R281_LEDGER: "ffa333f040551d583c6afd34a1b466fbc67fe0628683782d80f905329b800fc7",
    R179: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R204: "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R267: "66879215e0250a4a462fea9837c24bccf49a936ce3c5e66da2707e1a66fafc8f",
}

CHARTS = ("G:E", "G:W", "G:N", "G:S")
EXPECTED_R291_KINDS = {
    "ROUND182_GRAPH_SHEET_LEAF": 111_524,
    "ROUND208_DIRECT_GRAPH_SIDE_REGION": 608,
    "ROUND179_NEGATIVE_T0_SHADOW_PATCH": 544,
    "ROUND179_POSITIVE_T0_RETAINED_OWNER": 440,
    "SOURCE_EXACT_T0_SHEET_CELL": 224,
    "ROUND182_TRANSVERSE_1D_LINE": 112,
}
R179_COLUMNS = (
    "row_id", "origin_row_id", "parent_id", "chart", "child_index",
    "refinement_path", "box", "coordinate_volume", "reason_labels",
    "ambient_dimension", "whole_origin_credit",
    "global_geometric_disposition_credit", "provenance",
)


class GateFailure(RuntimeError):
    pass


CAPTURE_RECORDS: dict[str, dict[str, Any]] = {}
CAPTURE_FDS: dict[str, int] = {}


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise GateFailure(label)


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate JSON key:" + key)
        output[key] = value
    return output


def reject_float(token: str) -> Any:
    raise GateFailure("JSON float forbidden:" + token)


def reject_constant(token: str) -> Any:
    raise GateFailure("JSON constant forbidden:" + token)


DECODER = json.JSONDecoder(
    object_pairs_hook=strict_pairs,
    parse_float=reject_float,
    parse_constant=reject_constant,
)


def strict_loads(payload: bytes | bytearray) -> Any:
    need(bytes(payload[:3]) != b"\xef\xbb\xbf", "JSON BOM forbidden")
    text = bytes(payload).decode("utf-8", "strict")
    value, end = DECODER.raw_decode(text)
    need(not text[end:].strip(), "trailing JSON content")
    return value


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def metadata_tuple(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev, info.st_ino, stat.S_IFMT(info.st_mode),
        stat.S_IMODE(info.st_mode), info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns,
    )


def capture_input(name: str) -> bytearray:
    need(name in INPUT_PINS and name not in CAPTURE_RECORDS, "unique input capture:" + name)
    path = ROOT / name
    need(path.parent == ROOT and path.parent.resolve(strict=True) == ROOT.resolve(strict=True), "direct input:" + name)
    before = os.lstat(path)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and (opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino),
            "nofollow regular input:" + name,
        )
        payload = bytearray()
        state = hashlib.sha256()
        while True:
            block = os.read(descriptor, 8 << 20)
            if not block:
                break
            payload.extend(block)
            state.update(block)
        after = os.fstat(descriptor)
        need(metadata_tuple(opened) == metadata_tuple(after), "stable input capture:" + name)
        need(len(payload) == opened.st_size, "captured size:" + name)
        actual = state.hexdigest()
        need(actual == INPUT_PINS[name], "captured byte pin:" + name)
        CAPTURE_RECORDS[name] = {
            "device": opened.st_dev,
            "inode": opened.st_ino,
            "mode": stat.S_IMODE(opened.st_mode),
            "nlink": opened.st_nlink,
            "size": opened.st_size,
            "mtime_ns": opened.st_mtime_ns,
            "ctime_ns": opened.st_ctime_ns,
            "sha256": actual,
            "open_count": 1,
            "content_read_count": 1,
            "hash_and_parse_source": "SAME_CAPTURED_BYTES",
        }
        CAPTURE_FDS[name] = descriptor
        return payload
    except BaseException:
        os.close(descriptor)
        raise


def recheck_capture_metadata() -> None:
    need(set(CAPTURE_RECORDS) == set(INPUT_PINS), "complete input capture set")
    for name in sorted(INPUT_PINS):
        opened = os.fstat(CAPTURE_FDS[name])
        path_info = os.lstat(ROOT / name)
        expected = CAPTURE_RECORDS[name]
        for field, actual in (
            ("device", opened.st_dev), ("inode", opened.st_ino),
            ("mode", stat.S_IMODE(opened.st_mode)), ("nlink", opened.st_nlink),
            ("size", opened.st_size), ("mtime_ns", opened.st_mtime_ns),
            ("ctime_ns", opened.st_ctime_ns),
        ):
            need(expected[field] == actual, "stable open input metadata:" + name + ":" + field)
        need(metadata_tuple(path_info) == metadata_tuple(opened), "stable path/fd identity:" + name)


def close_capture_fds() -> None:
    for descriptor in CAPTURE_FDS.values():
        try:
            os.close(descriptor)
        except OSError:
            pass
    CAPTURE_FDS.clear()


def check_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "row closure:" + label)


def closed_wrapper(payload: bytes | bytearray, name: str) -> dict[str, Any]:
    document = strict_loads(payload)
    need(type(document) is dict and type(document.get("result")) is dict, "closed wrapper:" + name)
    need(document.get("result_sha256") == digest(document["result"]), "wrapper closure:" + name)
    return document["result"]


def stream_array(
    stream: TextIO, *, marker: str, nested_rows: bool,
    expected_type: type = dict,
) -> Iterator[Any]:
    buffer = ""
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing marker:" + marker)
        buffer = (buffer + block)[-(len(marker) + (2 << 20)):]
    buffer = buffer.split(marker, 1)[1]
    if nested_rows:
        while '"rows":[' not in buffer:
            block = stream.read(1 << 20)
            need(bool(block), "missing nested rows:" + marker)
            buffer += block
        buffer = buffer.split('"rows":[', 1)[1]
    else:
        while not buffer.lstrip().startswith("["):
            block = stream.read(1 << 20)
            need(bool(block), "missing array opener:" + marker)
            buffer += block
        buffer = buffer.lstrip()[1:]
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated array:" + marker)
            buffer = block
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                value, end = DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated array row:" + marker)
                buffer += block
        need(type(value) is expected_type, "array row type:" + marker)
        yield value
        buffer = buffer[end:]


def plain_array(
    payload: bytes | bytearray, marker: str, *, nested_rows: bool = False,
    expected_type: type = dict,
) -> Iterator[Any]:
    with io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8", errors="strict", newline="") as stream:
        yield from stream_array(stream, marker=marker, nested_rows=nested_rows, expected_type=expected_type)


def gzip_array(payload: bytes | bytearray) -> Iterator[dict[str, Any]]:
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as compressed:
        with io.TextIOWrapper(compressed, encoding="utf-8", errors="strict", newline="") as stream:
            yield from stream_array(stream, marker='"rows":', nested_rows=False)


def gzip_jsonl(payload: bytes | bytearray) -> Iterator[dict[str, Any]]:
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
        for raw in stream:
            need(raw.endswith(b"\n"), "JSONL newline")
            row = strict_loads(raw[:-1])
            need(type(row) is dict, "JSONL object")
            yield row


def load_source_sheets() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    r236_bytes = capture_input(R236)
    r236 = closed_wrapper(r236_bytes, R236)
    del r236_bytes
    partitions = r236["double_endpoint_partition_rows"]
    need(len(partitions) == 16, "R236 double partition count")
    partition_charts: dict[str, str] = {}
    for row in partitions:
        pid = row["double_endpoint_partition_row_id"]
        charts = {
            row[name]["source_chart"]
            for name in (
                "negative_to_positive_signature", "positive_to_negative_signature",
                "same_sign_event_absent_signature",
            )
        }
        need(len(charts) == 1 and next(iter(charts)) in CHARTS, "R236 chart")
        need(pid not in partition_charts, "R236 partition uniqueness")
        partition_charts[pid] = next(iter(charts))

    r248_bytes = capture_input(R248)
    sheets: list[dict[str, Any]] = []
    kinds: Counter[str] = Counter()
    for row in plain_array(
        r248_bytes, '"formal_wall_half_open_sheet_owner_ledger":', nested_rows=True,
    ):
        kinds[row["source_partition_kind"]] += 1
        if (
            row["source_partition_kind"] == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET"
            and row["endpoint_factor"] == "source"
        ):
            check_row(row, "R248 source double sheet")
            pid = row["source_partition_row_id"]
            need(pid in partition_charts, "R248/R236 partition join")
            base = [str(Fraction(value)) for value in row["exact_closed_base_rectangle"]]
            need(len(base) == 4, "source sheet base")
            sheets.append({
                "member_id": row["wall_sheet_node_id"],
                "partition_row_id": pid,
                "chart": partition_charts[pid],
                "closed_p_s_rectangle": base,
                "owner_official_key_id": row["owner_official_key_id"],
                "owner_signature_sha256": row["owner_signature_sha256"],
                "R248_row_sha256": row["row_sha256"],
            })
    del r248_bytes
    need(kinds == {
        "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328,
        "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32,
    }, "R248 sheet census")
    need(len(sheets) == 16 and len({row["member_id"] for row in sheets}) == 16, "16 source sheets")
    need(Counter(row["chart"] for row in sheets) == {chart: 4 for chart in CHARTS}, "four source sheets per chart")
    sheets.sort(key=canonical)
    return sheets, {
        "source_sheet_count": 16,
        "source_sheet_chart_census": dict(sorted(Counter(row["chart"] for row in sheets).items())),
        "source_sheet_rows_sha256": digest(sheets),
    }


def interval_overlap(a0: Fraction, a1: Fraction, b0: Fraction, b1: Fraction) -> Fraction:
    return min(a1, b1) - max(a0, b0)


def discover_contacts(
    sheets: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], set[str], dict[str, Any]]:
    r291_bytes = capture_input(R291)
    contacts: list[dict[str, Any]] = []
    by_key: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    kinds: Counter[str] = Counter()
    disposition_count = 0
    physical_count = 0
    physical_keys: set[tuple[str, int]] = set()
    for disposition in gzip_array(r291_bytes):
        check_row(disposition, "R291 disposition")
        disposition_count += 1
        did = disposition["complete_lower_stratum_local_disposition_row_id"]
        chart = disposition["source_chart"]
        need(chart in CHARTS, "R291 chart")
        for index, cell in enumerate(disposition["physical_witness_cells"]):
            key = (did, index)
            need(key not in physical_keys, "R291 physical-key uniqueness")
            physical_keys.add(key)
            physical_count += 1
            kind = cell["witness_kind"]
            kinds[kind] += 1
            if kind != "ROUND179_NEGATIVE_T0_SHADOW_PATCH":
                continue
            bounds = tuple(Fraction(value) for value in cell["exact_bounds"])
            need(len(bounds) == 6 and bounds[0] == bounds[1] == 0, "negative shadow t0 patch")
            for sheet in sheets:
                if sheet["chart"] != chart:
                    continue
                base = tuple(Fraction(value) for value in sheet["closed_p_s_rectangle"])
                overlap_p = interval_overlap(base[0], base[1], bounds[2], bounds[3])
                overlap_s = interval_overlap(base[2], base[3], bounds[4], bounds[5])
                if overlap_p < 0 or overlap_s < 0:
                    continue
                contact = {
                    "key": key,
                    "sheet": sheet,
                    "R291_disposition_row_id": did,
                    "R291_disposition_row_sha256": disposition["row_sha256"],
                    "R291_canonical_support_kind": disposition["canonical_support_kind"],
                    "R291_canonical_support_row_id": disposition["canonical_support_row_id"],
                    "R291_local_disposition": disposition["local_disposition"],
                    "R291_evidence_basis": disposition["evidence_basis"],
                    "R291_predicate_equation": disposition["predicate_equation"],
                    "physical_witness_cell_index": index,
                    "cell": cell,
                    "overlap_p": str(overlap_p),
                    "overlap_s": str(overlap_s),
                }
                contacts.append(contact)
                by_key[key].append(contact)
    del r291_bytes
    need(disposition_count == 55_428 and physical_count == 113_452, "R291 complete frontier")
    need(kinds == EXPECTED_R291_KINDS, "R291 witness-kind census")
    need(len(contacts) == 24 and len(by_key) == 16, "24 contacts on 16 shadow patches")
    need(Counter((row["overlap_p"], row["overlap_s"]) for row in contacts) == {
        ("0", "0"): 8, ("0", "1/800"): 16,
    }, "contact overlap census")

    r295_bytes = capture_input(R295A)
    binding_count = 0
    selected_binding_count = 0
    target_ids: set[str] = set()
    for binding in gzip_array(r295_bytes):
        check_row(binding, "R295A binding")
        binding_count += 1
        key = (
            binding["Round291_local_disposition_row_id"],
            binding["physical_witness_cell_index"],
        )
        if key not in by_key:
            continue
        selected_binding_count += 1
        targets = binding["target_Round294_registry_rows"]
        ids = binding["target_Round294_registry_occurrence_ids"]
        need(
            binding["witness_kind"] == "ROUND179_NEGATIVE_T0_SHADOW_PATCH"
            and len(targets) == len(ids) == 1
            and ids == [targets[0]["registry_occurrence_id"]]
            and binding["exact_witness_covered_by_named_registry_supports"] is True,
            "R295A selected shadow binding",
        )
        target = targets[0]
        target_ids.add(ids[0])
        reduced = {
            "binding_row_id": binding["Round295A_R291_physical_incidence_binding_row_id"],
            "binding_row_sha256": binding["row_sha256"],
            "classification": binding["Round295A_binding_classification"],
            "source_binding_classification": binding["source_Round293_binding_classification"],
            "target": {
                "registry_occurrence_id": target["registry_occurrence_id"],
                "official_key_id": target["official_key_id"],
                "complete_10_field_return_signature_sha256": target["complete_10_field_return_signature_sha256"],
                "physical_support_chart": target["physical_support_chart"],
                "Round294_occurrence_registry_row_sha256": target["Round294_occurrence_registry_row_sha256"],
            },
        }
        for contact in by_key[key]:
            contact["binding"] = reduced
    del r295_bytes
    need(binding_count == 113_452 and selected_binding_count == 16, "R295A complete/selected census")
    need(all("binding" in row for row in contacts), "all contacts registry-bound")
    return contacts, target_ids, {
        "R291_disposition_count": disposition_count,
        "R291_physical_cell_count": physical_count,
        "R291_witness_kind_census": dict(sorted(kinds.items())),
        "negative_shadow_contact_count": len(contacts),
        "negative_shadow_patch_count": len(by_key),
        "R295A_binding_count": binding_count,
        "R295A_selected_binding_count": selected_binding_count,
        "selected_target_occurrence_count": len(target_ids),
    }


def bind_current_supports(
    contacts: list[dict[str, Any]], target_ids: set[str], sheets: list[dict[str, Any]],
) -> dict[str, Any]:
    selected_ids = target_ids | {row["member_id"] for row in sheets}
    c15_bytes = capture_input(C15)
    components: dict[str, dict[str, Any]] = {}
    count = 0
    for row in gzip_jsonl(c15_bytes):
        count += 1
        member = row["registry_member_id"]
        if member in selected_ids:
            check_row(row, "selected C15 member")
            need(member not in components, "C15 selected uniqueness")
            components[member] = {
                "component_id": row["fresh_component_id"],
                "official_key_id": row["official_key_id"],
                "row_sha256": row["row_sha256"],
            }
    del c15_bytes
    need(count == 502_204 and set(components) == selected_ids, "C15 selected exact cover")

    c25_bytes = capture_input(C25)
    c25: dict[str, dict[str, Any]] = {}
    count25 = 0
    for row in gzip_jsonl(c25_bytes):
        count25 += 1
        member = row["member_id"]
        if member in target_ids:
            check_row(row, "selected C25 target")
            need(member not in c25, "C25 selected uniqueness")
            c25[member] = row
    del c25_bytes
    need(count25 == 502_204 and set(c25) == target_ids, "C25 selected exact cover")

    c22b_bytes = capture_input(C22B)
    c22b: dict[str, dict[str, Any]] = {}
    count22 = 0
    for row in gzip_jsonl(c22b_bytes):
        count22 += 1
        member = row["member_id"]
        if member in target_ids:
            check_row(row, "selected C22B support")
            need(member not in c22b, "C22B selected uniqueness")
            c22b[member] = row
    del c22b_bytes
    need(count22 == 302_624 and set(c22b) == target_ids, "C22B selected exact cover")

    for contact in contacts:
        sheet = contact["sheet"]
        target = contact["binding"]["target"]
        sid, tid = sheet["member_id"], target["registry_occurrence_id"]
        need(
            components[sid]["official_key_id"] == sheet["owner_official_key_id"]
            and components[tid]["official_key_id"] == target["official_key_id"],
            "C15 exact-key joins",
        )
        need(components[sid]["component_id"] != components[tid]["component_id"], "contact is cross C15 component")
        need(
            c25[tid]["fresh_component_id"] == components[tid]["component_id"]
            and c25[tid]["source_bindings"]["C15_member_row_sha256"] == components[tid]["row_sha256"]
            and c25[tid]["source_bindings"]["support_kernel"] == "C22B"
            and c25[tid]["source_bindings"]["support_kernel_row_sha256"] == c22b[tid]["row_sha256"],
            "C15/C25/C22B support join",
        )
        ast = c22b[tid]["normalized_support_ast"]
        need(
            ast.get("kind") == "OPEN_RATIONAL_BOX"
            and ast.get("coordinates") == ["t", "p", "s"]
            and ast.get("coordinate_chart") == sheet["chart"],
            "target open support AST",
        )
        contact["sheet_component_id"] = components[sid]["component_id"]
        contact["target_component_id"] = components[tid]["component_id"]
        contact["sheet_C15_row_sha256"] = components[sid]["row_sha256"]
        contact["target_C15_row_sha256"] = components[tid]["row_sha256"]
        contact["target_C25_row_sha256"] = c25[tid]["row_sha256"]
        contact["target_C22B_row_sha256"] = c22b[tid]["row_sha256"]
        contact["target_support_ast"] = ast
    for sheet in sheets:
        member = sheet["member_id"]
        sheet["component_id"] = components[member]["component_id"]
        sheet["C15_row_sha256"] = components[member]["row_sha256"]
    return {
        "C15_member_count": count,
        "C15_selected_member_count": len(components),
        "C25_member_count": count25,
        "C25_selected_target_count": len(c25),
        "C22B_representation_count": count22,
        "C22B_selected_target_count": len(c22b),
        "all_24_contacts_cross_C15_component": True,
    }


def evaluate_open_support(contacts: list[dict[str, Any]]) -> dict[str, Any]:
    contact_dimension_census: Counter[int] = Counter()
    for contact in contacts:
        sheet = tuple(Fraction(value) for value in contact["sheet"]["closed_p_s_rectangle"])
        cell = tuple(Fraction(value) for value in contact["cell"]["exact_bounds"])
        target = tuple(Fraction(value) for value in contact["target_support_ast"]["bounds"])
        need(target[0] == 0 < target[1] and target[2:] == cell[2:], "target open box equals positive-owner interior bounds")
        p0, p1 = max(sheet[0], cell[2]), min(sheet[1], cell[3])
        s0, s1 = max(sheet[2], cell[4]), min(sheet[3], cell[5])
        need(p0 == p1 and s0 <= s1, "codimension-two contact locus")
        need(p0 in {target[2], target[3]}, "contact p is target endpoint")
        representative_s = s0 if s0 == s1 else (s0 + s1) / 2
        representative = (Fraction(0), p0, representative_s)
        open_contains = all(target[2 * axis] < representative[axis] < target[2 * axis + 1] for axis in range(3))
        need(not open_contains, "target open support excludes contact")
        dimension = int(s0 < s1)
        contact_dimension_census[dimension] += 1
        contact["contact_locus"] = {
            "t": "0",
            "p": str(p0),
            "s_closed_interval": [str(s0), str(s1)],
            "dimension": dimension,
            "representative_t_p_s": [str(value) for value in representative],
        }
        contact["open_support_evaluation"] = {
            "target_OPEN_RATIONAL_BOX_contains_representative": False,
            "entire_contact_locus_excluded_by_axes": ["t", "p"],
            "t_equals_strict_lower_endpoint": True,
            "p_equals_one_strict_endpoint": True,
            "closure_exclusion_does_not_imply_physical_nonincidence": True,
        }
    need(contact_dimension_census == {0: 8, 1: 16}, "contact dimension census")
    return {
        "layer_A_decision": "PASS__24_OF_24_CONTACT_LOCI_EXCLUDED_FROM_TARGET_OPEN_SUPPORT",
        "target_open_exclusion_count": 24,
        "zero_dimensional_contact_count": 8,
        "one_dimensional_contact_count": 16,
        "every_contact_excluded_by_t_and_p_strict_endpoint_semantics": True,
        "physical_edge_or_lower_owner_conclusion_from_layer_A": "NONE",
    }


def resolve_t0_owner_components(
    contacts: list[dict[str, Any]], sheets: list[dict[str, Any]],
) -> dict[str, Any]:
    """Bind every contact locus to the complete current R248 t=0 sheet cover.

    Member-level overlap at an s endpoint is allowed, but the physical owner
    component must be unique.  This is the exact component-level statement
    needed by the counterexample gate and does not rely on R204 covering the
    unrelated positive-t retained child.
    """
    member_cover_census: Counter[int] = Counter()
    component_cover_census: Counter[int] = Counter()
    for contact in contacts:
        locus = contact["contact_locus"]
        p = Fraction(locus["p"])
        s0, s1 = (Fraction(value) for value in locus["s_closed_interval"])
        candidates: list[dict[str, Any]] = []
        covered_intervals: list[tuple[Fraction, Fraction]] = []
        for sheet in sheets:
            if sheet["chart"] != contact["sheet"]["chart"]:
                continue
            p0, p1, q0, q1 = (
                Fraction(value) for value in sheet["closed_p_s_rectangle"]
            )
            if not (p0 <= p <= p1):
                continue
            lower, upper = max(s0, q0), min(s1, q1)
            if lower > upper:
                continue
            candidates.append(sheet)
            covered_intervals.append((lower, upper))
        need(
            bool(candidates),
            "nonempty complete t0 source-sheet owner cover:"
            + contact["sheet"]["chart"] + ":" + str(p) + ":" + str(s0) + ":" + str(s1),
        )
        covered_intervals.sort()
        merged: list[list[Fraction]] = []
        for lower, upper in covered_intervals:
            if not merged or lower > merged[-1][1]:
                merged.append([lower, upper])
            else:
                merged[-1][1] = max(merged[-1][1], upper)
        need(merged == [[s0, s1]], "entire contact locus covered by t0 sheets")
        components = {sheet["component_id"] for sheet in candidates}
        need(
            components == {contact["sheet_component_id"]},
            "unique lower-owner C15 component equals source-sheet component",
        )
        member_cover_census[len(candidates)] += 1
        component_cover_census[len(components)] += 1
        contact["t0_owner_component_handoff"] = {
            "owner_basis": "COMPLETE_R248_SOURCE_ENDPOINT_SHEET_COVER_AT_EXACT_T0",
            "covering_member_count": len(candidates),
            "covering_member_ids": sorted(sheet["member_id"] for sheet in candidates),
            "covering_member_C15_row_sha256s": sorted(
                sheet["C15_row_sha256"] for sheet in candidates
            ),
            "covering_closed_s_intervals_on_contact": [
                [str(lower), str(upper)] for lower, upper in covered_intervals
            ],
            "contact_locus_fully_covered": True,
            "unique_C15_component_count": 1,
            "unique_C15_component_id": contact["sheet_component_id"],
            "target_component_is_owner_component": False,
            "cross_component_same_physical_point_witness": False,
        }
    need(member_cover_census == {1: 8, 2: 16}, "t0 owner member-cover census")
    need(component_cover_census == {1: 24}, "unique t0 owner component census")
    return {
        "decision": "PASS__24_OF_24_COMPLETE_T0_OWNER_COMPONENT_HANDOFFS",
        "contact_count": 24,
        "single_covering_member_count": 8,
        "two_same_component_covering_members_count": 16,
        "unique_owner_component_count_per_contact": 1,
        "owner_component_equals_source_sheet_component_count": 24,
        "owner_component_equals_target_component_count": 0,
        "confirmed_cross_component_same_point_witness_count": 0,
    }


def bind_round281(contacts: list[dict[str, Any]]) -> dict[str, Any]:
    result_bytes = capture_input(R281_RESULT)
    authority = strict_loads(result_bytes)
    del result_bytes
    claimed = authority.get("result_sha256")
    body = dict(authority)
    body.pop("result_sha256", None)
    need(claimed == digest(body), "R281 result closure")
    need(
        authority["status"] == "PASS_ROUND281_LOWER_STRATUM_TAIL_CLOSURE__ZERO_CREDIT"
        and authority["ledger_attachment"]["file_sha256"] == INPUT_PINS[R281_LEDGER]
        and authority["census"]["shadow_owner_patch_count"] == 544,
        "R281 authority contract",
    )

    shadow_ids = {row["cell"]["negative_shadow_origin_row_id"] for row in contacts}
    ledger_bytes = capture_input(R281_LEDGER)
    selected: dict[str, dict[str, Any]] = {}
    row_count = 0
    for row in gzip_array(ledger_bytes):
        check_row(row, "R281 ledger row")
        row_count += 1
        origin = row["containing_Round174_residual_row_id"]
        if origin in shadow_ids:
            need(origin not in selected, "R281 selected shadow uniqueness")
            selected[origin] = row
    del ledger_bytes
    need(row_count == 1_276 and set(selected) == shadow_ids and len(selected) == 8, "R281 selected shadow cover")

    owner_children: set[str] = set()
    owner_origins: set[str] = set()
    for contact in contacts:
        cell = contact["cell"]
        row = selected[cell["negative_shadow_origin_row_id"]]
        need(
            row["decision_family"] == "EXACT_SOURCE_T0_HALF_OPEN_OWNER"
            and row["physical_disposition"] == "CERTIFIED_PHYSICAL_SUPPORT_EXISTS__NEGATIVE_T_SHADOW_TO_POSITIVE_OWNER"
            and row["evidence_basis"] == "ROUND204_POSITIVE_T_OWNER_POLICY__EXACT_POSITIVE_RETAINED_CHILD_PATCH_COVER",
            "R281 selected owner semantics",
        )
        matches = []
        for patch in row["owner_patches"]:
            if (
                patch["negative_shadow_origin_row_id"] == cell["negative_shadow_origin_row_id"]
                and patch["positive_owner_origin_row_id"] == cell["positive_owner_origin_row_id"]
                and patch["positive_owner_parent_id"] == cell["positive_owner_parent_id"]
                and patch["positive_owner_retained_child_row_id"] == cell["positive_owner_retained_child_row_id"]
                and patch["patch_exact_bounds"] == cell["exact_bounds"]
                and patch["patch_area"] == cell["cell_area"]
                and patch["owner_policy"] == cell["owner_policy"]
            ):
                matches.append(patch)
        need(len(matches) == 1, "R281 exact owner-patch join")
        owner_children.add(cell["positive_owner_retained_child_row_id"])
        owner_origins.add(cell["positive_owner_origin_row_id"])
        contact["R281_binding"] = {
            "row_id": row["round281_lower_tail_closure_row_id"],
            "row_sha256": row["row_sha256"],
            "Round267_lineage_row_id": row["Round267_lower_stratum_terminal_lineage_row_id"],
            "t_side_owner_policy": cell["owner_policy"],
            "positive_owner_origin_row_id": cell["positive_owner_origin_row_id"],
            "positive_owner_parent_id": cell["positive_owner_parent_id"],
            "positive_owner_retained_child_row_id": cell["positive_owner_retained_child_row_id"],
            "patch_exact_bounds": cell["exact_bounds"],
            "scope_limit": "T_SIDE_OWNER_PATCH_ONLY__P_S_BOUNDARY_OWNER_NOT_MATERIALIZED_HERE",
        }
    need(len(owner_children) == len(owner_origins) == 16, "16 positive owner children/origins")
    return {
        "R281_ledger_row_count": row_count,
        "selected_negative_shadow_origin_count": len(selected),
        "selected_positive_owner_patch_count": len(owner_children),
        "selected_positive_owner_origin_count": len(owner_origins),
        "t_side_owner_transfer_bound_count": 24,
        "p_s_lower_owner_transfer_bound_count": 0,
    }


def bind_round179(contacts: list[dict[str, Any]]) -> dict[str, Any]:
    child_ids = {row["R281_binding"]["positive_owner_retained_child_row_id"] for row in contacts}
    payload = capture_input(R179)
    selected: dict[str, dict[str, Any]] = {}
    row_count = 0
    for packed in plain_array(payload, '"retained_3d_child_rows":', expected_type=list):
        row_count += 1
        need(len(packed) == len(R179_COLUMNS), "R179 retained packed width")
        if packed[0] in child_ids:
            need(packed[0] not in selected, "R179 selected child uniqueness")
            selected[packed[0]] = dict(zip(R179_COLUMNS, packed, strict=True))
    del payload
    need(row_count == 106_680 and set(selected) == child_ids, "R179 positive-owner child cover")
    for contact in contacts:
        binding = contact["R281_binding"]
        row = selected[binding["positive_owner_retained_child_row_id"]]
        box = [str(Fraction(value)) for value in row["box"]]
        patch = [str(Fraction(value)) for value in binding["patch_exact_bounds"]]
        need(
            row["origin_row_id"] == binding["positive_owner_origin_row_id"]
            and row["parent_id"] == binding["positive_owner_parent_id"]
            and row["chart"] == contact["sheet"]["chart"]
            and box[0] == "0" and Fraction(box[1]) > 0
            and patch == ["0", "0", *box[2:]],
            "R179 positive-t child/t0-face exact join",
        )
        contact["R179_positive_owner"] = {
            "retained_child_row_sha256": digest(row),
            "exact_closed_box": box,
            "t0_face_equals_R281_patch": True,
            "ambient_dimension": row["ambient_dimension"],
        }
    return {
        "R179_retained_child_count": row_count,
        "selected_positive_owner_retained_child_count": len(selected),
        "all_selected_R281_patches_equal_the_R179_positive_child_t0_face": True,
    }


def bind_round267(contacts: list[dict[str, Any]]) -> dict[str, Any]:
    lineage_ids = {row["R281_binding"]["Round267_lineage_row_id"] for row in contacts}
    payload = capture_input(R267)
    selected: dict[str, dict[str, Any]] = {}
    row_count = 0
    for row in plain_array(
        payload, '"formal_Round174_lower_stratum_terminal_lineage_ledger":', nested_rows=True,
    ):
        check_row(row, "R267 lineage row")
        row_count += 1
        rid = row["lower_stratum_terminal_lineage_row_id"]
        if rid in lineage_ids:
            need(rid not in selected, "R267 selected uniqueness")
            selected[rid] = row
    del payload
    need(row_count == 62_696 and set(selected) == lineage_ids and len(selected) == 8, "R267 selected lineage cover")
    for contact in contacts:
        rid = contact["R281_binding"]["Round267_lineage_row_id"]
        row = selected[rid]
        need(
            row["canonical_support_or_absence_row_id"] == contact["R291_canonical_support_row_id"]
            and row["containing_Round174_residual_row_id"] == contact["cell"]["negative_shadow_origin_row_id"]
            and row["terminal_lineage_status"] == "MATERIALIZED_AS_CANONICAL_SUPPORT"
            and row["nominal_support_only"] is True
            and row["physical_existence_credit"] == 0
            and row["quotient_component_edge_credit"] == 0,
            "R267 nominal-only selected lineage",
        )
        contact["R267_binding"] = {
            "lineage_row_id": rid,
            "row_sha256": row["row_sha256"],
            "nominal_support_only": True,
            "physical_existence_credit": 0,
            "quotient_component_edge_credit": 0,
        }
    return {
        "R267_lineage_row_count": row_count,
        "selected_lineage_row_count": len(selected),
        "selected_nominal_support_only_count": len(selected),
        "selected_physical_existence_credit_sum": 0,
        "selected_quotient_component_edge_credit_sum": 0,
    }


def overlaps(a0: Fraction, a1: Fraction, b0: Fraction, b1: Fraction) -> bool:
    return min(a1, b1) >= max(a0, b0)


def r204_edge_matches(row: dict[str, Any], chart: str, p: Fraction, s0: Fraction, s1: Fraction) -> bool:
    key, kind = row["geometry_key"], row["geometry_kind"]
    if key[1] != chart:
        return False
    if kind in {"EXACT_SOURCE_T0_P_FIXED_S_SEGMENT", "TARGET_GRAPH_P_FIXED_S_CURVE"}:
        return Fraction(key[5]) == p and overlaps(Fraction(key[6]), Fraction(key[7]), s0, s1)
    if kind in {"EXACT_SOURCE_T0_S_FIXED_P_SEGMENT", "TARGET_GRAPH_S_FIXED_P_CURVE"}:
        return s0 <= Fraction(key[5]) <= s1 and Fraction(key[6]) <= p <= Fraction(key[7])
    if kind == "EXACT_T0_P0_S_SEGMENT":
        return p == 0 and overlaps(Fraction(key[6]), Fraction(key[7]), s0, s1)
    raise GateFailure("unknown R204 1D geometry kind:" + kind)


def audit_round204(contacts: list[dict[str, Any]]) -> dict[str, Any]:
    payload = capture_input(R204)
    result = closed_wrapper(payload, R204)
    del payload
    regions = result["formal_local_open_3D_region_ledger"]["rows"]
    sheets = result["formal_2D_sheet_lineage"]["source_sheet_rows"]
    edges = result["formal_1D_boundary_and_intersection_lineage"]["rows"]
    points = result["formal_0D_endpoint_and_corner_lineage"]["rows"]
    need(len(regions) == 736 and len(sheets) == 224 and len(edges) == 1_024 and len(points) == 580, "R204 dimensional census")
    owner_children = {row["R281_binding"]["positive_owner_retained_child_row_id"] for row in contacts}
    owner_origins = {row["R281_binding"]["positive_owner_origin_row_id"] for row in contacts}
    identity_hits = [
        row for row in regions
        if row["retained_child_row_id"] in owner_children or row["origin_row_id"] in owner_origins
    ]
    need(not identity_hits, "selected retained children absent from R204 open-region domain")
    source_identity_hits = [row for row in sheets if row["positive_t_origin_row_id"] in owner_origins]
    need(not source_identity_hits, "selected origins absent from R204 source-sheet domain")

    two_d_hits = one_d_hits = zero_d_hits = 0
    for contact in contacts:
        locus = contact["contact_locus"]
        chart = contact["sheet"]["chart"]
        p = Fraction(locus["p"])
        s0, s1 = map(Fraction, locus["s_closed_interval"])
        hit2 = sum(
            row["chart"] == chart
            and Fraction(row["base_p_s_exact_bounds"][0]) <= p <= Fraction(row["base_p_s_exact_bounds"][1])
            and overlaps(
                Fraction(row["base_p_s_exact_bounds"][2]),
                Fraction(row["base_p_s_exact_bounds"][3]), s0, s1,
            )
            for row in sheets
        )
        hit1 = sum(r204_edge_matches(row, chart, p, s0, s1) for row in edges)
        hit0 = sum(
            row["geometry_key"][1] == chart
            and Fraction(row["geometry_key"][5]) == p
            and s0 <= Fraction(row["geometry_key"][6]) <= s1
            for row in points
        )
        need(hit2 == hit1 == hit0 == 0, "R204 contact locus absent from dimensional lineage")
        two_d_hits += hit2
        one_d_hits += hit1
        zero_d_hits += hit0
        contact["R204_scope_audit"] = {
            "positive_owner_child_or_origin_identity_match_count": 0,
            "contact_locus_2D_source_sheet_match_count": 0,
            "contact_locus_1D_lineage_match_count": 0,
            "contact_locus_0D_lineage_match_count": 0,
            "interpretation": "ROUND204_COMPLETE_DIMENSIONAL_LINEAGE_DOES_NOT_COVER_THIS_RETAINED_CHILD_CONTACT_LOCUS",
        }
    return {
        "R204_open_region_count": len(regions),
        "R204_source_2D_sheet_count": len(sheets),
        "R204_1D_lineage_count": len(edges),
        "R204_0D_lineage_count": len(points),
        "selected_positive_owner_identity_match_count": len(identity_hits) + len(source_identity_hits),
        "contact_locus_2D_match_count": two_d_hits,
        "contact_locus_1D_match_count": one_d_hits,
        "contact_locus_0D_match_count": zero_d_hits,
        "scope_conclusion": "NO_R204_2D_1D_0D_OWNER_LINEAGE_FOR_THE_24_CONTACTS",
    }


def closed_row(body: dict[str, Any]) -> dict[str, Any]:
    row = dict(body)
    row["row_sha256"] = digest(row)
    return row


def finalize_rows(contacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for contact in contacts:
        sheet = contact["sheet"]
        target = contact["binding"]["target"]
        body = {
            "schema": "cm2.c27-semantic-counterexample-gate.lower-owner-shadow-transfer.zero-credit.v1.contact-row.v1",
            "contact_id": "c27-lower-owner-contact:" + digest([
                sheet["member_id"], contact["R291_disposition_row_id"],
                contact["physical_witness_cell_index"], target["registry_occurrence_id"],
            ]),
            "chart": sheet["chart"],
            "source_sheet_member_id": sheet["member_id"],
            "source_sheet_component_id": contact["sheet_component_id"],
            "source_sheet_closed_p_s_rectangle": sheet["closed_p_s_rectangle"],
            "target_registry_occurrence_id": target["registry_occurrence_id"],
            "target_component_id": contact["target_component_id"],
            "cross_C15_component": True,
            "R291_disposition_row_id": contact["R291_disposition_row_id"],
            "R291_disposition_row_sha256": contact["R291_disposition_row_sha256"],
            "R291_physical_witness_cell_index": contact["physical_witness_cell_index"],
            "R291_physical_witness_cell_sha256": digest(contact["cell"]),
            "R295A_binding": contact["binding"],
            "target_C15_row_sha256": contact["target_C15_row_sha256"],
            "target_C25_row_sha256": contact["target_C25_row_sha256"],
            "target_C22B_row_sha256": contact["target_C22B_row_sha256"],
            "target_normalized_support_ast": contact["target_support_ast"],
            "contact_locus": contact["contact_locus"],
            "layer_A_target_open_membership": {
                **contact["open_support_evaluation"],
                "decision": "EXCLUDED_FROM_TARGET_OPEN_SUPPORT",
            },
            "R281_t_side_binding": contact["R281_binding"],
            "R179_positive_owner_binding": contact["R179_positive_owner"],
            "R267_nominal_lineage_binding": contact["R267_binding"],
            "R204_dimensional_scope_audit": contact["R204_scope_audit"],
            "layer_B_lower_owner_physical_support_component_handoff": {
                **contact["t0_owner_component_handoff"],
                "decision": "PASS__COMPLETE_T0_SHEET_COVER_HAS_UNIQUE_C15_COMPONENT",
                "unique_named_p_s_lower_owner_component_count": 1,
                "lower_owner_physical_existence_to_current_occurrence_proven": True,
                "lower_owner_to_C15_component_lineage_proven": True,
                "closure_contact_promoted_to_physical_edge": False,
            },
            "confirmed_cross_component_same_physical_point_witness_count": 0,
            "formal_component_edge_credit": 0,
            "formal_maximality_credit": 0,
            "verdict": "PASS_ZERO_CREDIT__TARGET_OPEN_SUPPORT_EXCLUDES_CONTACT__T0_OWNER_COMPONENT_IS_SOURCE_COMPONENT",
        }
        rows.append(closed_row(body))
    rows.sort(key=canonical)
    need(len(rows) == 24 and len({row["contact_id"] for row in rows}) == 24, "24 injective result rows")
    return rows


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    sheets, sheet_audit = load_source_sheets()
    contacts, target_ids, frontier_audit = discover_contacts(sheets)
    current_audit = bind_current_supports(contacts, target_ids, sheets)
    layer_a = evaluate_open_support(contacts)
    layer_b = resolve_t0_owner_components(contacts, sheets)
    r281_audit = bind_round281(contacts)
    r179_audit = bind_round179(contacts)
    r267_audit = bind_round267(contacts)
    r204_audit = audit_round204(contacts)
    rows = finalize_rows(contacts)
    result = {
        "schema": "cm2.c27-semantic-counterexample-gate.lower-owner-shadow-transfer.zero-credit.v1",
        "status": "PASS_ZERO_CREDIT__24_TARGET_OPEN_SUPPORT_EXCLUSIONS__24_COMPLETE_T0_OWNER_COMPONENT_HANDOFFS__ZERO_CROSS_COMPONENT_WITNESSES",
        "subgate_decision": "PASS_DIAGNOSTIC_ZERO_CREDIT__SECOND_IMPLEMENTATION_AND_ATTACKS_REQUIRED",
        "unconditional_C27_C28_C29_decision": "REJECT_REMAINS_IN_FORCE",
        "scope_contract": {
            "semantic_family": "LOWER_OWNER_SHADOW_TRANSFER",
            "candidate_universe": "ALL_SAME_CHART_CLOSED_CONTACTS_BETWEEN_16_CURRENT_SOURCE_DOUBLE_SHEETS_AND_COMPLETE_544_R291_NEGATIVE_T0_SHADOW_PATCHES",
            "Round306C27_imported_or_executed": False,
            "Round306C27_FAMILIES_copied": False,
            "edge_ledger_used_as_candidate_universe": False,
            "existing_DOUBLE_GRAPHS_probe_output_used_as_input": False,
            "all_inputs_O_NOFOLLOW_single_byte_capture": True,
            "input_hashing_and_parsing_use_identical_captured_bytes": True,
            "input_path_content_reread_count": 0,
            "single_semantic_implementation_only": True,
        },
        "source_sheet_reconstruction": sheet_audit,
        "complete_frontier_reconstruction": frontier_audit,
        "current_support_and_component_binding": current_audit,
        "two_layer_decision": {
            "layer_A": layer_a,
            "layer_B": {
                **layer_b,
                "family_empty_theorem": True,
            },
            "composition_rule": "LAYER_A_OPEN_EXCLUSION_MUST_NOT_BE_PROMOTED_TO_PHYSICAL_NONINCIDENCE_WITHOUT_LAYER_B",
        },
        "Round281_t_side_owner_audit": r281_audit,
        "Round179_positive_owner_child_audit": r179_audit,
        "Round267_nominal_lineage_audit": r267_audit,
        "Round204_dimensional_scope_audit": r204_audit,
        "contact_ledger": {
            "row_count": len(rows),
            "rows_sha256": digest(rows),
            "all_rows_layer_A_excluded": True,
            "all_rows_layer_B_unresolved": False,
            "all_rows_layer_B_unique_component_handoff": True,
            "all_rows_formal_credit_zero": True,
        },
        "counterexample_gate": {
            "counterexample_first": True,
            "confirmed_legal_cross_component_witness_count": 0,
            "no_witness_is_not_a_family_empty_theorem": False,
            "verdict": "NO_CONFIRMED_WITNESS__COMPLETE_T0_OWNER_COMPONENT_COVER_PROVES_SUBGATE_EMPTY",
        },
        "formal_credit": {
            "whole_origin_credit": 0,
            "component_edge_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "maximality_credit": 0,
            "C27_credit": 0,
            "C28_credit": 0,
            "C29_credit": 0,
        },
        "strict_nonpromotion": {
            "CM2": "NO-GO_FOR_CLAIM",
            "D02": "BLOCKED",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "complete_18_field_global_blocks": 0,
        },
        "independence_boundary": {
            "double_seed_byte_identity_tests_hash_order_determinism_only": True,
            "double_seed_does_not_supply_independent_semantic_implementation": True,
            "required_before_any_FORMAL_PROMOTION": "A_SEPARATE_IMPLEMENTATION_MUST_RECONSTRUCT_THE_T0_OWNER_COMPONENT_COVER_WITHOUT_REUSING_THIS_IMPLEMENTATION_AND_COHERENT_ATTACKS_MUST_PASS",
        },
        "required_next": [
            "run a second independent reconstruction of the complete R248 t0 owner-component cover",
            "attack member omission, chart mutation, interval endpoint mutation, and C15 component mutation",
            "retain zero formal credit until the full 20-family semantic gate closes",
        ],
        "input_capture_records": {name: CAPTURE_RECORDS[name] for name in sorted(CAPTURE_RECORDS)},
    }
    return rows, result


def gzip_rows(rows: list[dict[str, Any]]) -> bytes:
    raw = b"".join(canonical(row) + b"\n" for row in rows)
    target = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=target, mtime=0) as stream:
        stream.write(raw)
    return target.getvalue()


def result_bytes(result: dict[str, Any]) -> bytes:
    return canonical({
        "result": result,
        "result_sha256": digest(result),
        "schema": "cm2.c27-semantic-counterexample-gate.lower-owner-shadow-transfer.zero-credit.v1.wrapper.v1",
    }) + b"\n"


def manifest_bytes(ledger: bytes, result: bytes) -> bytes:
    members = [
        {"name": LEDGER, "sha256": hashlib.sha256(ledger).hexdigest(), "size": len(ledger)},
        {"name": RESULT, "sha256": hashlib.sha256(result).hexdigest(), "size": len(result)},
    ]
    body = {
        "schema": "cm2.c27-semantic-counterexample-gate.lower-owner-shadow-transfer.zero-credit.v1.manifest.v1",
        "member_count": 2,
        "members": members,
        "members_sha256": digest(members),
        "formal_credit": 0,
        "subgate_decision": "REJECT_FAIL_CLOSED",
    }
    return canonical({"manifest": body, "manifest_sha256": digest(body)}) + b"\n"


def exclusive_write(path: Path, payload: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            need(written > 0, "write progress:" + path.name)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def read_output(path: Path) -> bytes:
    before = os.lstat(path)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode) and opened.st_nlink == 1
            and (opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino),
            "nofollow output:" + path.name,
        )
        chunks = []
        while True:
            block = os.read(descriptor, 8 << 20)
            if not block:
                break
            chunks.append(block)
        data = b"".join(chunks)
        need(len(data) == opened.st_size, "output size:" + path.name)
        return data
    finally:
        os.close(descriptor)


def verify_directory(directory: Path, expected: dict[str, bytes]) -> None:
    info = os.lstat(directory)
    need(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode), "output directory")
    need(sorted(path.name for path in directory.iterdir()) == sorted(expected), "exact output graph")
    for name, payload in expected.items():
        need(read_output(directory / name) == payload, "output bytes:" + name)
    wrapper = strict_loads(expected[RESULT])
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "result closure")
    wrapper = strict_loads(expected[MANIFEST])
    manifest = wrapper["manifest"]
    need(wrapper["manifest_sha256"] == digest(manifest), "manifest closure")
    need(manifest["members_sha256"] == digest(manifest["members"]), "manifest member closure")
    for member in manifest["members"]:
        payload = expected[member["name"]]
        need(member["size"] == len(payload) and member["sha256"] == hashlib.sha256(payload).hexdigest(), "manifest member:" + member["name"])


def rename_noreplace(source: Path, destination: Path) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    need(function is not None, "renameat2 available")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    rc = function(-100, os.fsencode(source), -100, os.fsencode(destination), 1)
    if rc != 0:
        code = ctypes.get_errno()
        if code == errno.EEXIST:
            raise GateFailure("output exists:" + destination.name)
        raise OSError(code, os.strerror(code), str(destination))


def cleanup_staging(directory: Path) -> None:
    if not directory.exists():
        return
    for name in (LEDGER, RESULT, MANIFEST):
        path = directory / name
        try:
            if path.exists() or path.is_symlink():
                os.chmod(path, 0o600, follow_symlinks=False)
                os.unlink(path)
        except OSError:
            pass
    try:
        os.chmod(directory, 0o700)
        os.rmdir(directory)
    except OSError:
        pass


def publish(output: Path, rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
    ledger = gzip_rows(rows)
    result_payload = result_bytes(result)
    manifest_payload = manifest_bytes(ledger, result_payload)
    expected = {LEDGER: ledger, RESULT: result_payload, MANIFEST: manifest_payload}
    staging = AUDIT_ROOT / f".{PREFIX}.staging-{os.getpid()}-{secrets.token_hex(8)}"
    need(not staging.exists() and staging.parent == AUDIT_ROOT, "fresh direct staging")
    os.mkdir(staging, 0o700)
    try:
        for name, payload in expected.items():
            exclusive_write(staging / name, payload)
        verify_directory(staging, expected)
        recheck_capture_metadata()
        for name in expected:
            os.chmod(staging / name, 0o444, follow_symlinks=False)
        os.chmod(staging, 0o555)
        rename_noreplace(staging, output)
    except BaseException:
        cleanup_staging(staging)
        raise
    verify_directory(output, expected)
    recheck_capture_metadata()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-tag", required=True)
    args = parser.parse_args()
    need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,126}[a-z0-9]", args.output_tag) is not None, "safe output tag")
    AUDIT_ROOT.mkdir(parents=True, exist_ok=True)
    need(AUDIT_ROOT.is_dir() and not AUDIT_ROOT.is_symlink(), "audit root")
    output = AUDIT_ROOT / args.output_tag
    need(output.parent == AUDIT_ROOT and output.resolve(strict=False).parent == AUDIT_ROOT.resolve(strict=True), "direct output")
    need(not output.exists() and not output.is_symlink(), "fresh output")
    try:
        rows, result = reconstruct()
        recheck_capture_metadata()
        publish(output, rows, result)
        print(canonical({
            "status": result["status"],
            "result_sha256": digest(result),
            "contact_count": len(rows),
            "layer_A_excluded_count": 24,
            "layer_B_unresolved_count": 0,
            "layer_B_unique_component_handoff_count": 24,
            "confirmed_witness_count": 0,
            "formal_credit": 0,
            "process_exit_is_fail_closed": 0,
        }).decode("ascii"))
        return 0
    finally:
        close_capture_fds()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateFailure as error:
        close_capture_fds()
        print("GATE_FAILURE:" + str(error), file=sys.stderr)
        raise SystemExit(2)
