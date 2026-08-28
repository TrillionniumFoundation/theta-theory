#!/usr/bin/env python3
"""Independent zero-credit ALIAS_RECHART_HANDOFF semantic subgate.

This probe closes only the 1,361,424 cross-source-chart pairs left open by
the additive DOUBLE_GRAPHS v2 probe.  It does not import Round306C27, copy
its FAMILIES registry, or use an existing edge ledger as a candidate
universe.  Instead it rebuilds the four source-normal chart formulae from a
pinned primitive geometry source, reconstructs the sixteen current
double-endpoint source sheets, and scans the complete R291 physical-cell
frontier.  The 112 transverse one-dimensional cells receive their exact
containing t-bounds from the packed Round179 table.

Every input is opened exactly once with O_NOFOLLOW.  Hashing and parsing use
only the captured bytes from that descriptor; paths are never reopened for
content.  Descriptors remain open and their metadata/path identity is
rechecked before and after atomic no-replace publication.

This is a development/audit subgate.  A PASS gives exactly zero formal
credit and does not upgrade C27/C28/C29.  The 448 same-chart transverse-1D
pairs, 24 lower-owner contacts, and 192 current-graph-side cross-chart pairs
remain outside this subgate.
"""

from __future__ import annotations

import argparse
import ast
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
PREFIX = "cm2_c27_alias_rechart_handoff_zero_credit_v1"
LEDGER = PREFIX + "_transport_cohort_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
MANIFEST = PREFIX + "_manifest.json"

R173_CERT = "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
R173_VERIFY = "cm2_round173_source_g_exact_return_signature_transport_verification.json"
R179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R179_MANIFEST = "cm2_round179_source_g_residual_tube_arrangement_manifest.sha256"
R236_CERT = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json"
R236_MANIFEST = "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_manifest.sha256"
R248_CERT = "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json"
R248_MANIFEST = "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256"
R291_LEDGER = "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_ledger.json.gz"
R291_MANIFEST = "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze_manifest.sha256"
R295A_LEDGER = "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_physical_witness_incidence_binding_ledger.json.gz"
R295A_MANIFEST = "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_manifest.sha256"
C15_LEDGER = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C15_MANIFEST = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_manifest.sha256"
PRIMITIVE_GEOMETRY = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"

INPUT_PINS = {
    R173_CERT: "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",
    R173_VERIFY: "e205367506bc02aa982de074253e5806f07b4358dd3738fb4a0e14476e44ce99",
    R179_ROWS: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R179_MANIFEST: "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76",
    R236_CERT: "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217",
    R236_MANIFEST: "28f6f6d2f5b0f10edba5cd473b4126a8fed098874849c2f579eadd92b30d324c",
    R248_CERT: "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311",
    R248_MANIFEST: "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07",
    R291_LEDGER: "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab",
    R291_MANIFEST: "d655907a45cfb7b47ebdc822d35a0e604fc27fa38547c300139c116d7a2191ce",
    R295A_LEDGER: "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R295A_MANIFEST: "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    C15_LEDGER: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C15_MANIFEST: "a1eea2c41123d2ff7f7d3e1f35f1deabc5bae9d93b24f825b4831f6324c1e2c4",
    PRIMITIVE_GEOMETRY: "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
}

CHARTS = ("G:E", "G:W", "G:N", "G:S")
CELLS = ("E", "W", "N", "S")
SOURCE_RADIUS = Fraction(9, 25)
EXPECTED_KIND_CENSUS = {
    "ROUND182_GRAPH_SHEET_LEAF": 111_524,
    "ROUND208_DIRECT_GRAPH_SIDE_REGION": 608,
    "ROUND179_NEGATIVE_T0_SHADOW_PATCH": 544,
    "ROUND179_POSITIVE_T0_RETAINED_OWNER": 440,
    "SOURCE_EXACT_T0_SHEET_CELL": 224,
    "ROUND182_TRANSVERSE_1D_LINE": 112,
}


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


STRICT_DECODER = json.JSONDecoder(
    object_pairs_hook=strict_pairs,
    parse_float=reject_float,
    parse_constant=reject_constant,
)


def strict_loads(payload: bytes | bytearray) -> Any:
    need(not bytes(payload[:3]) == b"\xef\xbb\xbf", "JSON BOM forbidden")
    text = bytes(payload).decode("utf-8", "strict")
    value, end = STRICT_DECODER.raw_decode(text)
    need(not text[end:].strip(), "trailing JSON content")
    return value


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def metadata_tuple(info: os.stat_result) -> tuple[int, ...]:
    return (
        info.st_dev,
        info.st_ino,
        stat.S_IFMT(info.st_mode),
        stat.S_IMODE(info.st_mode),
        info.st_nlink,
        info.st_size,
        info.st_mtime_ns,
        info.st_ctime_ns,
    )


def capture_input(name: str) -> bytearray:
    """Open one direct-child input once and return exactly those captured bytes."""
    need(name in INPUT_PINS and name not in CAPTURE_RECORDS, "unique pinned capture:" + name)
    path = ROOT / name
    root_resolved = ROOT.resolve(strict=True)
    need(path.parent == ROOT and path.parent.resolve(strict=True) == root_resolved, "direct input parent:" + name)
    before = os.lstat(path)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size > 0
            and (before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino),
            "nofollow regular input:" + name,
        )
        data = bytearray()
        state = hashlib.sha256()
        while True:
            block = os.read(descriptor, 8 << 20)
            if not block:
                break
            data.extend(block)
            state.update(block)
        after = os.fstat(descriptor)
        need(metadata_tuple(opened) == metadata_tuple(after), "stable during capture:" + name)
        need(len(data) == opened.st_size, "captured size:" + name)
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
        return data
    except BaseException:
        os.close(descriptor)
        raise


def recheck_capture_metadata() -> None:
    need(set(CAPTURE_RECORDS) == set(INPUT_PINS), "complete captured input set")
    for name in sorted(INPUT_PINS):
        descriptor = CAPTURE_FDS[name]
        opened = os.fstat(descriptor)
        path_info = os.lstat(ROOT / name)
        expected = CAPTURE_RECORDS[name]
        current = {
            "device": opened.st_dev,
            "inode": opened.st_ino,
            "mode": stat.S_IMODE(opened.st_mode),
            "nlink": opened.st_nlink,
            "size": opened.st_size,
            "mtime_ns": opened.st_mtime_ns,
            "ctime_ns": opened.st_ctime_ns,
        }
        need(all(current[key] == expected[key] for key in current), "stable open fd metadata:" + name)
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


def text_stream(payload: bytes | bytearray) -> TextIO:
    return io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8", errors="strict", newline="")


def stream_array(
    stream: TextIO,
    *,
    marker: str,
    nested_rows: bool,
    expected_type: type = dict,
) -> Iterator[Any]:
    buffer = ""
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing array marker:" + marker)
        buffer = (buffer + block)[-(len(marker) + (2 << 20)) :]
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
                value, end = STRICT_DECODER.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated array row:" + marker)
                buffer += block
        need(type(value) is expected_type, "array row type:" + marker)
        yield value
        buffer = buffer[end:]


def plain_array(
    payload: bytes | bytearray,
    marker: str,
    *,
    nested_rows: bool = False,
    expected_type: type = dict,
) -> Iterator[Any]:
    with text_stream(payload) as stream:
        yield from stream_array(
            stream,
            marker=marker,
            nested_rows=nested_rows,
            expected_type=expected_type,
        )


def gzip_array(payload: bytes | bytearray, marker: str = '"rows":') -> Iterator[dict[str, Any]]:
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as compressed:
        with io.TextIOWrapper(compressed, encoding="utf-8", errors="strict", newline="") as stream:
            yield from stream_array(stream, marker=marker, nested_rows=False)


def gzip_jsonl(payload: bytes | bytearray) -> Iterator[dict[str, Any]]:
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
        for raw in stream:
            need(raw.endswith(b"\n"), "JSONL newline")
            value = strict_loads(raw[:-1])
            need(type(value) is dict, "JSONL object row")
            yield value


def validate_small_authorities() -> dict[str, Any]:
    primitive_bytes = capture_input(PRIMITIVE_GEOMETRY)
    primitive_text = bytes(primitive_bytes).decode("utf-8", "strict")
    ast.parse(primitive_text, filename=PRIMITIVE_GEOMETRY)
    exact_fragments = [
        'if cell == "E":\n        nx, ny = radical_n, t',
        'elif cell == "W":\n        nx, ny = -radical_n, t',
        'elif cell == "N":\n        nx, ny = t, radical_n',
        'elif cell == "S":\n        nx, ny = t, -radical_n',
        'if source == "G":\n        cx, cy = arb(0), arb(0)',
    ]
    need(all(fragment in primitive_text for fragment in exact_fragments), "primitive chart formula fragments")
    del primitive_bytes

    r173_bytes = capture_input(R173_CERT)
    r173 = closed_wrapper(r173_bytes, R173_CERT)
    del r173_bytes
    need(
        r173["status"]
        == "CERTIFIED_SOURCE_G_JX_JY_EXACT_RETURN_SIGNATURE_TRANSPORT_DICTIONARY__NO_DYNAMIC_ROW_OR_D02_PROMOTION",
        "R173 transport status",
    )
    generators = {row["generator"]: row for row in r173["exact_transport_generators"]}
    need(set(generators) == {"Jx", "Jy"}, "R173 generator set")
    expected_chart_maps = {
        "Jx": {"G:E": "G:W", "G:W": "G:E", "G:N": "G:N", "G:S": "G:S"},
        "Jy": {"G:E": "G:E", "G:W": "G:W", "G:N": "G:S", "G:S": "G:N"},
    }
    need(
        generators["Jx"]["physical_reflection"] == "(x,y,s,p)->(-x,y,-s,-p)"
        and generators["Jy"]["physical_reflection"] == "(x,y,s,p)->(x,-y,s,-p)",
        "R173 physical reflections",
    )
    for generator, expected in expected_chart_maps.items():
        row = generators[generator]
        need(row["source_chart_dictionary"] == expected, "R173 chart dictionary:" + generator)
        need(
            row["half_open_owner_rule_equivariant"] is True
            and row["half_open_owner_set_image"] == ["E", "W"],
            "R173 half-open equivariance:" + generator,
        )
    need(
        r173["Klein_four_action"]["relations_checked_on_every_source_G_ordinal"] is True,
        "R173 Klein relation audit",
    )

    verify_bytes = capture_input(R173_VERIFY)
    verify = closed_wrapper(verify_bytes, R173_VERIFY)
    del verify_bytes
    need(
        verify["status"] == "PASS"
        and verify["certificate_sha256"] == INPUT_PINS[R173_CERT]
        and verify["source_chart_and_target_lift_permutations_independently_rebuilt"] is True,
        "R173 independent verification",
    )

    for manifest_name in (
        R179_MANIFEST,
        R236_MANIFEST,
        R248_MANIFEST,
        R291_MANIFEST,
        R295A_MANIFEST,
        C15_MANIFEST,
    ):
        manifest_bytes = capture_input(manifest_name)
        text = bytes(manifest_bytes).decode("ascii", "strict")
        need("  " in text and text.endswith("\n"), "manifest syntax:" + manifest_name)
        del manifest_bytes

    return {
        "primitive_source_sha256": INPUT_PINS[PRIMITIVE_GEOMETRY],
        "primitive_formulae": {
            "G:E": "n_E(t)=(+sqrt(1-t^2),t)",
            "G:W": "n_W(t)=(-sqrt(1-t^2),t)",
            "G:N": "n_N(t)=(t,+sqrt(1-t^2))",
            "G:S": "n_S(t)=(t,-sqrt(1-t^2))",
            "source_G_center": "(0,0)",
            "source_G_radius": "9/25",
        },
        "R173_certificate_sha256": INPUT_PINS[R173_CERT],
        "R173_verification_sha256": INPUT_PINS[R173_VERIFY],
        "generator_chart_maps": expected_chart_maps,
        "generator_physical_reflections": {
            "Jx": generators["Jx"]["physical_reflection"],
            "Jy": generators["Jy"]["physical_reflection"],
        },
        "Klein_chart_orbits_recomputed": [["G:E", "G:W"], ["G:N", "G:S"]],
    }


def reconstruct_source_sheets() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    r236_bytes = capture_input(R236_CERT)
    r236 = closed_wrapper(r236_bytes, R236_CERT)
    del r236_bytes
    partitions = r236["double_endpoint_partition_rows"]
    need(len(partitions) == 16, "R236 double partition count")
    partition_map: dict[str, dict[str, Any]] = {}
    chart_census: Counter[str] = Counter()
    source_factor_rows: list[dict[str, Any]] = []
    for row in partitions:
        pid = row["double_endpoint_partition_row_id"]
        need(pid not in partition_map, "unique R236 partition")
        signatures = [
            row["negative_to_positive_signature"],
            row["positive_to_negative_signature"],
            row["same_sign_event_absent_signature"],
        ]
        charts = {item["source_chart"] for item in signatures}
        need(len(charts) == 1, "R236 source chart agreement")
        chart = next(iter(charts))
        need(chart in CHARTS and row["wall"] == 0, "R236 source-G wall-zero partition")
        cell = chart.split(":", 1)[1]
        expected_axis = "Y" if cell in {"E", "W"} else "X"
        need(
            row["axis"] == expected_axis
            and row["source_factor_strict_t_derivative_sign"] == "STRICT_POSITIVE",
            "R236 primitive source factor derivation",
        )
        chart_census[chart] += 1
        partition_map[pid] = {"row": row, "chart": chart}
        source_factor_rows.append({
            "partition_row_id": pid,
            "chart": chart,
            "axis": row["axis"],
            "wall": row["wall"],
            "primitive_source_factor": "(9/25)*t",
            "unique_zero": "t=0",
        })
    need(chart_census == {chart: 4 for chart in CHARTS}, "R236 chart-balanced source partitions")

    r248_bytes = capture_input(R248_CERT)
    selected: list[dict[str, Any]] = []
    full_kind_census: Counter[str] = Counter()
    for row in plain_array(
        r248_bytes,
        '"formal_wall_half_open_sheet_owner_ledger":',
        nested_rows=True,
    ):
        kind = row["source_partition_kind"]
        full_kind_census[kind] += 1
        if kind == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET":
            check_row(row, "R248 double sheet")
            if row["endpoint_factor"] == "source":
                selected.append(row)
    del r248_bytes
    need(
        full_kind_census
        == {
            "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328,
            "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32,
        },
        "R248 full sheet-kind census",
    )
    need(len(selected) == 16, "R248 source double sheet count")
    sheets: list[dict[str, Any]] = []
    for row in selected:
        pid = row["source_partition_row_id"]
        need(pid in partition_map, "R248/R236 partition join")
        chart = partition_map[pid]["chart"]
        base = [str(Fraction(value)) for value in row["exact_closed_base_rectangle"]]
        need(len(base) == 4, "R248 source sheet base rectangle")
        cell = chart.split(":", 1)[1]
        fixed_axis = "x" if cell in {"E", "W"} else "y"
        fixed_sign = 1 if cell in {"E", "N"} else -1
        sheets.append({
            "member_id": row["wall_sheet_node_id"],
            "partition_row_id": pid,
            "partition_row_sha256": digest(partition_map[pid]["row"]),
            "R248_row_sha256": row["row_sha256"],
            "chart": chart,
            "source_t": "0",
            "source_normal": {
                "E": ["1", "0"],
                "W": ["-1", "0"],
                "N": ["0", "1"],
                "S": ["0", "-1"],
            }[cell],
            "source_position_fixed_axis": fixed_axis,
            "source_position_fixed_coordinate": str(fixed_sign * SOURCE_RADIUS),
            "exact_closed_p_s_rectangle": base,
            "owner_official_key_id": row["owner_official_key_id"],
            "owner_signature_sha256": row["owner_signature_sha256"],
        })
    need(len({row["member_id"] for row in sheets}) == 16, "source sheet member uniqueness")
    need(Counter(row["chart"] for row in sheets) == {chart: 4 for chart in CHARTS}, "source sheet chart census")
    sheets.sort(key=canonical)
    return sheets, {
        "R236_partition_count": len(partitions),
        "R248_source_sheet_count": len(sheets),
        "source_sheet_chart_census": dict(sorted(Counter(row["chart"] for row in sheets).items())),
        "source_factor_rows_sha256": digest(sorted(source_factor_rows, key=canonical)),
        "all_source_sheets_have_primitive_factor_9_over_25_times_t": True,
        "all_source_sheets_have_unique_source_t_zero": True,
        "source_sheet_rows_sha256": digest(sheets),
    }


def extract_cell_bounds(cell: dict[str, Any]) -> tuple[list[str] | None, str | None]:
    kind = cell["witness_kind"]
    if kind == "ROUND182_GRAPH_SHEET_LEAF":
        return cell.get("exact_box"), None
    if kind == "ROUND208_DIRECT_GRAPH_SIDE_REGION":
        return cell.get("exact_leaf_box"), None
    if kind in {
        "ROUND179_NEGATIVE_T0_SHADOW_PATCH",
        "ROUND179_POSITIVE_T0_RETAINED_OWNER",
        "SOURCE_EXACT_T0_SHEET_CELL",
    }:
        return cell.get("exact_ambient_bounds", cell.get("exact_bounds")), None
    need(kind == "ROUND182_TRANSVERSE_1D_LINE", "known R291 physical witness kind")
    retained = cell.get("containing_retained_child_row_id")
    need(type(retained) is str, "transverse retained child id")
    return None, retained


def load_physical_cells() -> tuple[list[dict[str, Any]], dict[str, Any], set[str]]:
    r291_bytes = capture_input(R291_LEDGER)
    cells: list[dict[str, Any]] = []
    physical_keys: set[tuple[str, int]] = set()
    transverse_ids: set[str] = set()
    kind_census: Counter[str] = Counter()
    chart_census: Counter[str] = Counter()
    disposition_count = 0
    sequence = hashlib.sha256()
    for disposition in gzip_array(r291_bytes):
        check_row(disposition, "R291 disposition")
        disposition_count += 1
        row_id = disposition["complete_lower_stratum_local_disposition_row_id"]
        chart = disposition["source_chart"]
        need(chart in CHARTS, "R291 source-G chart")
        for index, cell in enumerate(disposition["physical_witness_cells"]):
            key = (row_id, index)
            need(key not in physical_keys, "R291 physical key uniqueness")
            physical_keys.add(key)
            bounds, retained = extract_cell_bounds(cell)
            if bounds is not None:
                need(type(bounds) is list and len(bounds) == 6, "R291 exact t/p/s bounds")
                normalized = [str(Fraction(value)) for value in bounds]
            else:
                normalized = None
                need(retained not in transverse_ids, "transverse retained child uniqueness")
                transverse_ids.add(retained)
            kind = cell["witness_kind"]
            kind_census[kind] += 1
            chart_census[chart] += 1
            cell_hash = digest(cell)
            sequence.update(canonical([row_id, index, cell_hash]))
            cells.append({
                "key": key,
                "disposition_row_id": row_id,
                "disposition_row_sha256": disposition["row_sha256"],
                "physical_witness_cell_index": index,
                "chart": chart,
                "witness_kind": kind,
                "cell_sha256": cell_hash,
                "exact_containing_t_p_s_bounds": normalized,
                "transverse_containing_retained_child_row_id": retained,
            })
    del r291_bytes
    need(disposition_count == 55_428, "R291 disposition count")
    need(len(cells) == 113_452 and len(physical_keys) == 113_452, "R291 physical-cell count")
    need(kind_census == EXPECTED_KIND_CENSUS, "R291 witness-kind census")
    need(len(transverse_ids) == 112, "R291 transverse retained-child count")
    return cells, {
        "R291_disposition_count": disposition_count,
        "R291_physical_cell_count": len(cells),
        "R291_witness_kind_census": dict(sorted(kind_census.items())),
        "R291_source_chart_census": dict(sorted(chart_census.items())),
        "R291_reduced_cell_sequence_sha256": sequence.hexdigest(),
    }, transverse_ids


def bind_transverse_boxes(cells: list[dict[str, Any]], transverse_ids: set[str]) -> dict[str, Any]:
    r179_bytes = capture_input(R179_ROWS)
    columns = (
        "row_id", "origin_row_id", "parent_id", "chart", "child_index",
        "refinement_path", "box", "coordinate_volume", "reason_labels",
        "ambient_dimension", "whole_origin_credit",
        "global_geometric_disposition_credit", "provenance",
    )
    selected: dict[str, dict[str, Any]] = {}
    count = 0
    for packed in plain_array(
        r179_bytes,
        '"retained_3d_child_rows":',
        expected_type=list,
    ):
        count += 1
        need(len(packed) == len(columns), "R179 retained packed row width")
        row_id = packed[0]
        if row_id in transverse_ids:
            need(row_id not in selected, "selected R179 retained row uniqueness")
            selected[row_id] = dict(zip(columns, packed, strict=True))
    del r179_bytes
    need(count == 106_680, "R179 retained row count")
    need(set(selected) == transverse_ids, "R179 transverse exact cover")
    for cell in cells:
        retained = cell["transverse_containing_retained_child_row_id"]
        if retained is None:
            continue
        row = selected[retained]
        need(row["chart"] == cell["chart"], "R179/R291 transverse chart")
        box = [str(Fraction(value)) for value in row["box"]]
        need(len(box) == 6, "R179 transverse containing box")
        cell["exact_containing_t_p_s_bounds"] = box
        cell["R179_retained_row_sha256"] = digest(row)
    return {
        "R179_retained_row_count": count,
        "selected_transverse_retained_row_count": len(selected),
        "selected_transverse_rows_sha256": digest(sorted(selected.values(), key=canonical)),
        "all_112_transverse_cells_bound_to_exact_containing_boxes": True,
    }


def load_bindings(
    physical_keys: set[tuple[str, int]],
) -> tuple[dict[tuple[str, int], dict[str, Any]], set[str], dict[str, Any]]:
    r295_bytes = capture_input(R295A_LEDGER)
    bindings: dict[tuple[str, int], dict[str, Any]] = {}
    target_ids: set[str] = set()
    target_reference_census: Counter[int] = Counter()
    classification_census: Counter[str] = Counter()
    for binding in gzip_array(r295_bytes):
        check_row(binding, "R295A binding")
        key = (
            binding["Round291_local_disposition_row_id"],
            binding["physical_witness_cell_index"],
        )
        need(key in physical_keys and key not in bindings, "R295A/R291 unique physical-key join")
        targets = binding["target_Round294_registry_rows"]
        ids = binding["target_Round294_registry_occurrence_ids"]
        need(
            type(targets) is list
            and type(ids) is list
            and ids == [row["registry_occurrence_id"] for row in targets]
            and len(ids) == binding["target_Round294_registry_reference_count"]
            and len(ids) > 0,
            "R295A target-row closure",
        )
        reduced_targets = []
        for row in targets:
            need(row["physical_support_chart"] in CHARTS, "R295A target source chart")
            reduced_targets.append({
                "registry_occurrence_id": row["registry_occurrence_id"],
                "official_key_id": row["official_key_id"],
                "complete_10_field_return_signature_sha256": row["complete_10_field_return_signature_sha256"],
                "physical_support_chart": row["physical_support_chart"],
                "Round294_occurrence_registry_row_sha256": row["Round294_occurrence_registry_row_sha256"],
            })
            target_ids.add(row["registry_occurrence_id"])
        bindings[key] = {
            "binding_row_id": binding["Round295A_R291_physical_incidence_binding_row_id"],
            "binding_row_sha256": binding["row_sha256"],
            "binding_classification": binding["Round295A_binding_classification"],
            "source_binding_classification": binding["source_Round293_binding_classification"],
            "witness_kind": binding["witness_kind"],
            "source_chart": binding["source_chart"],
            "targets": reduced_targets,
        }
        target_reference_census[len(ids)] += 1
        classification_census[binding["Round295A_binding_classification"]] += 1
    del r295_bytes
    need(len(bindings) == 113_452 and set(bindings) == physical_keys, "R295A complete R291 bijection")
    return bindings, target_ids, {
        "R295A_binding_count": len(bindings),
        "R295A_distinct_target_occurrence_count": len(target_ids),
        "target_reference_count_per_cell_census": {
            str(key): value for key, value in sorted(target_reference_census.items())
        },
        "binding_classification_census": dict(sorted(classification_census.items())),
    }


def load_components(selected_ids: set[str]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    c15_bytes = capture_input(C15_LEDGER)
    selected: dict[str, dict[str, Any]] = {}
    row_count = 0
    for row in gzip_jsonl(c15_bytes):
        row_count += 1
        member = row["registry_member_id"]
        if member in selected_ids:
            check_row(row, "selected C15 member")
            need(member not in selected, "selected C15 member uniqueness")
            selected[member] = {
                "component_id": row["fresh_component_id"],
                "official_key_id": row["official_key_id"],
                "C15_row_sha256": row["row_sha256"],
            }
    del c15_bytes
    need(row_count == 502_204, "C15 member row count")
    need(set(selected) == selected_ids, "C15 selected member exact cover")
    return selected, {
        "C15_member_row_count": row_count,
        "C15_selected_member_count": len(selected),
        "C15_selected_component_count": len({row["component_id"] for row in selected.values()}),
        "C15_selected_rows_sha256": digest(sorted(
            ({"member_id": member, **row} for member, row in selected.items()),
            key=canonical,
        )),
    }


def chart_cell(chart: str) -> str:
    need(chart in CHARTS, "known source chart")
    return chart.split(":", 1)[1]


def chart_relation(source: str, target: str) -> dict[str, Any]:
    need(source != target, "cross-chart relation")
    s_cell, t_cell = chart_cell(source), chart_cell(target)
    opposite = {"E": "W", "W": "E", "N": "S", "S": "N"}[s_cell]
    if t_cell == opposite:
        words = ["Jx", "JxJy"] if s_cell in {"E", "W"} else ["Jy", "JxJy"]
        fixed_axis = "x" if s_cell in {"E", "W"} else "y"
        fixed_coordinate = SOURCE_RADIUS * (1 if s_cell in {"E", "N"} else -1)
        return {
            "relation": "OPPOSITE_DOMINANT_CHART",
            "direct_normal_equation_disposition": "NO_SOLUTION__DOMINANT_COMPONENT_HAS_OPPOSITE_STRICT_SIGN",
            "required_target_t": None,
            "endpoint_exclusion": "NOT_APPLICABLE__SIGN_CONTRADICTION",
            "Klein_chart_transport_words": words,
            "Klein_transport_is_same_point_rechart": False,
            "physical_reflection_fixed_point_axis": fixed_axis,
            "source_fixed_axis_coordinate": str(fixed_coordinate),
            "fixed_point_excluded_by_nonzero_source_radius": fixed_coordinate != 0,
        }
    required = 1 if s_cell in {"E", "N"} else -1
    return {
        "relation": "PERPENDICULAR_DOMINANT_CHART",
        "direct_normal_equation_disposition": "ONLY_SOLUTION_REQUIRES_TARGET_LOCAL_T_AT_UNIT_ENDPOINT",
        "required_target_t": str(required),
        "endpoint_exclusion": (
            "REQUIRED_PLUS_ONE_EXCLUDED_BY_STRICT_UPPER_BOUND"
            if required == 1
            else "REQUIRED_MINUS_ONE_EXCLUDED_BY_STRICT_LOWER_BOUND"
        ),
        "Klein_chart_transport_words": [],
        "Klein_transport_is_same_point_rechart": False,
        "Klein_orbit_obstruction": "EW_AND_NS_CHART_ORBITS_ARE_DISJOINT",
    }


def component_relation(source_component: str, targets: list[dict[str, Any]]) -> str:
    same = sum(target["component_id"] == source_component for target in targets)
    if same == len(targets):
        return "ALL_TARGETS_SAME_C15_COMPONENT"
    if same == 0:
        return "ALL_TARGETS_CROSS_C15_COMPONENT"
    return "MIXED_SAME_AND_CROSS_C15_COMPONENT_TARGETS"


def owner_relation(sheet: dict[str, Any], targets: list[dict[str, Any]]) -> str:
    key_matches = [target for target in targets if target["official_key_id"] == sheet["owner_official_key_id"]]
    exact = [
        target for target in key_matches
        if target["complete_10_field_return_signature_sha256"] == sheet["owner_signature_sha256"]
    ]
    if exact:
        return "AT_LEAST_ONE_EXACT_OFFICIAL_KEY_AND_SIGNATURE_MATCH"
    if key_matches:
        return "OFFICIAL_KEY_MATCH_WITH_SIGNATURE_MISMATCH"
    return "NO_OFFICIAL_KEY_MATCH"


def cohort_row(body: dict[str, Any]) -> dict[str, Any]:
    row = dict(body)
    row["row_sha256"] = digest(row)
    return row


def build_cohorts(
    sheets: list[dict[str, Any]],
    cells: list[dict[str, Any]],
    bindings: dict[tuple[str, int], dict[str, Any]],
    components: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    for sheet in sheets:
        member = sheet["member_id"]
        need(member in components, "source sheet C15 binding")
        need(
            components[member]["official_key_id"] == sheet["owner_official_key_id"],
            "source sheet C15 official key",
        )
        sheet["component_id"] = components[member]["component_id"]
        sheet["C15_row_sha256"] = components[member]["C15_row_sha256"]

    cohort_states: dict[tuple[Any, ...], dict[str, Any]] = {}
    route_census: Counter[str] = Counter()
    relation_census: Counter[str] = Counter()
    component_census: Counter[str] = Counter()
    owner_census: Counter[str] = Counter()
    priority_count = 0
    priority_representatives: list[dict[str, Any]] = []
    same_chart_transverse = 0
    cross_chart_count = 0
    endpoint_candidate_count = 0
    global_t_lower: Fraction | None = None
    global_t_upper: Fraction | None = None

    for cell in cells:
        bounds = cell["exact_containing_t_p_s_bounds"]
        need(type(bounds) is list and len(bounds) == 6, "all physical cells exact containing bounds")
        t_lower, t_upper = Fraction(bounds[0]), Fraction(bounds[1])
        need(-1 < t_lower <= t_upper < 1, "physical cell t support strictly inside unit endpoints")
        global_t_lower = t_lower if global_t_lower is None else min(global_t_lower, t_lower)
        global_t_upper = t_upper if global_t_upper is None else max(global_t_upper, t_upper)
        binding = bindings[cell["key"]]
        need(
            binding["source_chart"] == cell["chart"]
            and binding["witness_kind"] == cell["witness_kind"],
            "R291/R295A cell semantics",
        )
        targets: list[dict[str, Any]] = []
        for target in binding["targets"]:
            member = target["registry_occurrence_id"]
            need(member in components, "R295A target C15 binding")
            need(
                target["physical_support_chart"] == cell["chart"]
                and components[member]["official_key_id"] == target["official_key_id"],
                "R295A target chart/key C15 consistency",
            )
            targets.append({**target, **components[member]})

        same_chart_sheets = [sheet for sheet in sheets if sheet["chart"] == cell["chart"]]
        need(len(same_chart_sheets) == 4, "four source sheets per cell chart")
        if cell["witness_kind"] == "ROUND182_TRANSVERSE_1D_LINE":
            same_chart_transverse += len(same_chart_sheets)

        for sheet in sheets:
            if sheet["chart"] == cell["chart"]:
                continue
            cross_chart_count += 1
            relation = chart_relation(sheet["chart"], cell["chart"])
            required = relation["required_target_t"]
            if required is None:
                same_normal_possible = False
                endpoint_gap = None
                route = "EXACT_NONINCIDENCE__OPPOSITE_DOMINANT_COMPONENT_STRICT_SIGN"
            else:
                endpoint = Fraction(required)
                same_normal_possible = t_lower <= endpoint <= t_upper
                endpoint_gap_fraction = (
                    endpoint - t_upper if endpoint == 1 else t_lower - endpoint
                )
                need(endpoint_gap_fraction > 0, "unit endpoint strict exclusion")
                endpoint_gap = str(endpoint_gap_fraction)
                route = "EXACT_NONINCIDENCE__PERPENDICULAR_RECHART_REQUIRES_EXCLUDED_UNIT_T_ENDPOINT"
            if same_normal_possible:
                endpoint_candidate_count += 1

            comp_relation = component_relation(sheet["component_id"], targets)
            own_relation = owner_relation(sheet, targets)
            exact_owner_cross = any(
                target["official_key_id"] == sheet["owner_official_key_id"]
                and target["complete_10_field_return_signature_sha256"] == sheet["owner_signature_sha256"]
                and target["component_id"] != sheet["component_id"]
                for target in targets
            )
            representative = {
                "source_sheet_member_id": sheet["member_id"],
                "source_sheet_chart": sheet["chart"],
                "source_sheet_component_id": sheet["component_id"],
                "source_sheet_owner_official_key_id": sheet["owner_official_key_id"],
                "source_sheet_owner_signature_sha256": sheet["owner_signature_sha256"],
                "R291_disposition_row_id": cell["disposition_row_id"],
                "physical_witness_cell_index": cell["physical_witness_cell_index"],
                "physical_witness_cell_sha256": cell["cell_sha256"],
                "target_cell_chart": cell["chart"],
                "target_cell_witness_kind": cell["witness_kind"],
                "target_exact_containing_t_p_s_bounds": bounds,
                "R295A_binding_row_id": binding["binding_row_id"],
                "target_registry_occurrence_ids": [target["registry_occurrence_id"] for target in targets],
                "target_component_ids": [target["component_id"] for target in targets],
                "direct_same_normal_possible": same_normal_possible,
                "priority_exact_owner_match_cross_component": exact_owner_cross,
            }
            if exact_owner_cross:
                priority_count += 1
                if len(priority_representatives) < 32:
                    priority_representatives.append(representative)

            cohort_key = (
                sheet["chart"],
                cell["chart"],
                cell["witness_kind"],
                relation["relation"],
                route,
                comp_relation,
                own_relation,
                exact_owner_cross,
                len(targets),
                binding["binding_classification"],
            )
            state = cohort_states.get(cohort_key)
            if state is None:
                state = {
                    "key": cohort_key,
                    "multiplicity": 0,
                    "representative": representative,
                    "representative_bytes": canonical(representative),
                    "min_t_lower": t_lower,
                    "max_t_upper": t_upper,
                    "minimum_endpoint_gap": Fraction(endpoint_gap) if endpoint_gap is not None else None,
                    "relation_proof": relation,
                }
                cohort_states[cohort_key] = state
            else:
                encoded = canonical(representative)
                if encoded < state["representative_bytes"]:
                    state["representative"] = representative
                    state["representative_bytes"] = encoded
                state["min_t_lower"] = min(state["min_t_lower"], t_lower)
                state["max_t_upper"] = max(state["max_t_upper"], t_upper)
                if endpoint_gap is not None:
                    gap = Fraction(endpoint_gap)
                    current = state["minimum_endpoint_gap"]
                    state["minimum_endpoint_gap"] = gap if current is None else min(current, gap)
            state["multiplicity"] += 1
            route_census[route] += 1
            relation_census[relation["relation"]] += 1
            component_census[comp_relation] += 1
            owner_census[own_relation] += 1

    need(cross_chart_count == 1_361_424, "cross-chart denominator")
    need(same_chart_transverse == 448, "same-chart transverse isolated denominator")
    need(endpoint_candidate_count == 0, "zero direct same-normal endpoint candidates")
    need(sum(route_census.values()) == cross_chart_count, "route exact cover")
    need(global_t_lower is not None and global_t_upper is not None, "global t enclosure")

    rows: list[dict[str, Any]] = []
    for state in cohort_states.values():
        key = state["key"]
        body = {
            "schema": "cm2.c27-semantic-counterexample-gate.alias-rechart-handoff.zero-credit.v1.transport-cohort-row.v1",
            "cohort_id": "c27-alias-rechart-cohort:" + digest(list(key)),
            "source_sheet_chart": key[0],
            "target_cell_chart": key[1],
            "target_cell_witness_kind": key[2],
            "chart_relation": key[3],
            "route": key[4],
            "C15_component_relation": key[5],
            "half_open_owner_relation": key[6],
            "priority_exact_owner_match_cross_component": key[7],
            "target_reference_count": key[8],
            "R295A_binding_classification": key[9],
            "multiplicity": state["multiplicity"],
            "cohort_t_lower_minimum": str(state["min_t_lower"]),
            "cohort_t_upper_maximum": str(state["max_t_upper"]),
            "minimum_exact_gap_from_required_unit_endpoint": (
                None
                if state["minimum_endpoint_gap"] is None
                else str(state["minimum_endpoint_gap"])
            ),
            "relation_proof": state["relation_proof"],
            "canonical_representative": state["representative"],
            "all_pairs_in_cohort_have_direct_same_normal_possible": False,
            "same_physical_point_witness_count": 0,
            "formal_component_edge_credit": 0,
            "formal_maximality_credit": 0,
        }
        rows.append(cohort_row(body))
    rows.sort(key=canonical)
    need(sum(row["multiplicity"] for row in rows) == cross_chart_count, "cohort multiplicity exact cover")
    need(len({row["cohort_id"] for row in rows}) == len(rows), "cohort id injectivity")

    priority_representatives.sort(key=canonical)
    return rows, {
        "complete_source_sheet_by_R291_physical_cell_product": 16 * 113_452,
        "same_chart_pair_count": 4 * 113_452,
        "cross_chart_pair_count": cross_chart_count,
        "cross_chart_expected_identity": "113452 physical cells * 12 nonmatching-chart source sheets",
        "cross_chart_route_census": dict(sorted(route_census.items())),
        "chart_relation_census": dict(sorted(relation_census.items())),
        "C15_component_relation_census": dict(sorted(component_census.items())),
        "half_open_owner_relation_census": dict(sorted(owner_census.items())),
        "priority_exact_owner_match_cross_component_pair_count": priority_count,
        "priority_representative_count": len(priority_representatives),
        "priority_representatives_sha256": digest(priority_representatives),
        "priority_representatives": priority_representatives,
        "direct_same_normal_candidate_count": endpoint_candidate_count,
        "confirmed_same_physical_point_cross_component_witness_count": 0,
        "unresolved_cross_chart_pair_count": 0,
        "global_exact_containing_t_lower_minimum": str(global_t_lower),
        "global_exact_containing_t_upper_maximum": str(global_t_upper),
        "all_target_t_supports_strictly_inside_minus_one_plus_one": True,
        "transport_cohort_count": len(rows),
        "transport_cohort_multiplicity_sum": sum(row["multiplicity"] for row in rows),
        "transport_cohort_rows_sha256": digest(rows),
        "each_cross_chart_pair_has_exactly_one_cohort": True,
        "same_chart_transverse_1D_pair_count_kept_separate": same_chart_transverse,
    }


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    authority = validate_small_authorities()
    sheets, sheet_audit = reconstruct_source_sheets()
    cells, cell_audit, transverse_ids = load_physical_cells()
    transverse_audit = bind_transverse_boxes(cells, transverse_ids)
    physical_keys = {cell["key"] for cell in cells}
    bindings, target_ids, binding_audit = load_bindings(physical_keys)
    selected_ids = target_ids | {sheet["member_id"] for sheet in sheets}
    components, component_audit = load_components(selected_ids)
    rows, cohort_audit = build_cohorts(sheets, cells, bindings, components)

    need(cohort_audit["cross_chart_pair_count"] == 1_361_424, "final cross-chart count")
    need(cohort_audit["unresolved_cross_chart_pair_count"] == 0, "final cross-chart unresolved zero")
    need(cohort_audit["confirmed_same_physical_point_cross_component_witness_count"] == 0, "final witness zero")
    result = {
        "schema": "cm2.c27-semantic-counterexample-gate.alias-rechart-handoff.zero-credit.v1",
        "status": "PASS_ZERO_CREDIT__ALIAS_RECHART_CROSS_CHART_DENOMINATOR_EXACTLY_EXHAUSTED__C27_C28_C29_UNCONDITIONAL_STATUS_UNCHANGED",
        "subgate_decision": "PASS_DIAGNOSTIC_ZERO_CREDIT__NO_CROSS_CHART_SAME_PHYSICAL_POINT_WITNESS",
        "unconditional_C27_C28_C29_decision": "REJECT_REMAINS_IN_FORCE",
        "scope_contract": {
            "semantic_family": "ALIAS_RECHART_HANDOFF",
            "candidate_universe": "COMPLETE_16_CURRENT_SOURCE_DOUBLE_SHEETS_X_COMPLETE_113452_R291_PHYSICAL_CELLS_FILTERED_ONLY_BY_CHART_INEQUALITY",
            "Round306C27_imported_or_executed": False,
            "Round306C27_FAMILIES_copied": False,
            "C6_C14D_or_other_edge_ledger_used_as_candidate_universe": False,
            "primitive_chart_formula_reconstructed_independently": True,
            "all_inputs_O_NOFOLLOW_single_byte_capture": True,
            "input_hashing_and_parsing_use_identical_captured_bytes": True,
            "input_path_content_reread_count": 0,
            "same_chart_transverse_1D_pairs_in_scope": False,
            "current_graph_side_cross_chart_pairs_in_scope": False,
            "lower_owner_codimension_two_contacts_in_scope": False,
        },
        "authority_and_primitive_geometry": authority,
        "source_sheet_reconstruction": sheet_audit,
        "physical_cell_reconstruction": {**cell_audit, **transverse_audit},
        "registry_and_component_binding": {**binding_audit, **component_audit},
        "exact_transport_cohort_certificate": cohort_audit,
        "counterexample_gate": {
            "counterexample_first": True,
            "minimal_witness_would_be_preserved_if_direct_normal_equality_survived": True,
            "direct_same_normal_candidate_count": 0,
            "confirmed_legal_cross_component_witness_count": 0,
            "verdict": "NO_WITNESS_IN_THIS_EXACT_CROSS_CHART_DENOMINATOR",
        },
        "residual_not_closed_by_this_subgate": {
            "same_chart_transverse_1D_pairs": 448,
            "cross_component_codimension_two_lower_owner_contacts": 24,
            "current_graph_side_cross_chart_pairs": 192,
            "diagnostic_residual_sum_if_composed_with_DOUBLE_GRAPHS_v2": 664,
            "composition_is_not_formal_authority": True,
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
        "required_next": [
            "materialize exact TPS support and owner transfer for the 448 same-chart transverse-1D pairs",
            "resolve the 24 codimension-two lower-owner contacts without treating closure as open-support membership",
            "independently route the 192 current-graph-side cross-chart pairs",
            "extend the counterexample-first reconstruction to the remaining high-risk C27 families",
        ],
        "input_capture_records": {name: CAPTURE_RECORDS[name] for name in sorted(CAPTURE_RECORDS)},
    }
    return rows, result


def deterministic_gzip_jsonl(rows: list[dict[str, Any]]) -> bytes:
    raw = b"".join(canonical(row) + b"\n" for row in rows)
    target = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=target, mtime=0) as stream:
        stream.write(raw)
    return target.getvalue()


def result_document(result: dict[str, Any]) -> bytes:
    return canonical({
        "result": result,
        "result_sha256": digest(result),
        "schema": "cm2.c27-semantic-counterexample-gate.alias-rechart-handoff.zero-credit.v1.wrapper.v1",
    }) + b"\n"


def file_bytes_nofollow(path: Path) -> bytes:
    before = os.lstat(path)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and (before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino),
            "nofollow output file:" + path.name,
        )
        blocks: list[bytes] = []
        while True:
            block = os.read(descriptor, 8 << 20)
            if not block:
                break
            blocks.append(block)
        payload = b"".join(blocks)
        need(len(payload) == opened.st_size, "output size:" + path.name)
        return payload
    finally:
        os.close(descriptor)


def exclusive_write(path: Path, payload: bytes) -> None:
    flags = (
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(payload)
        while view:
            count = os.write(descriptor, view)
            need(count > 0, "output write progress:" + path.name)
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def make_manifest(ledger_bytes: bytes, result_bytes: bytes) -> bytes:
    members = [
        {"name": LEDGER, "sha256": hashlib.sha256(ledger_bytes).hexdigest(), "size": len(ledger_bytes)},
        {"name": RESULT, "sha256": hashlib.sha256(result_bytes).hexdigest(), "size": len(result_bytes)},
    ]
    body = {
        "schema": "cm2.c27-semantic-counterexample-gate.alias-rechart-handoff.zero-credit.v1.manifest.v1",
        "member_count": 2,
        "members": members,
        "members_sha256": digest(members),
        "formal_credit": 0,
    }
    return canonical({"manifest": body, "manifest_sha256": digest(body)}) + b"\n"


def verify_output_directory(directory: Path, expected: dict[str, bytes]) -> None:
    info = os.lstat(directory)
    need(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode), "regular output directory")
    need(sorted(item.name for item in directory.iterdir()) == sorted(expected), "exact output member graph")
    for name, payload in expected.items():
        need(file_bytes_nofollow(directory / name) == payload, "published output bytes:" + name)
    document = strict_loads(expected[RESULT])
    need(document["result_sha256"] == digest(document["result"]), "published result closure")
    manifest_document = strict_loads(expected[MANIFEST])
    manifest = manifest_document["manifest"]
    need(manifest_document["manifest_sha256"] == digest(manifest), "published manifest closure")
    need(manifest["member_count"] == 2 and manifest["members_sha256"] == digest(manifest["members"]), "manifest member closure")
    for member in manifest["members"]:
        payload = expected[member["name"]]
        need(
            member["size"] == len(payload)
            and member["sha256"] == hashlib.sha256(payload).hexdigest(),
            "manifest member binding:" + member["name"],
        )


def rename_noreplace(source: Path, destination: Path) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    need(function is not None, "Linux renameat2 available")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    rc = function(
        -100,
        os.fsencode(source),
        -100,
        os.fsencode(destination),
        1,
    )
    if rc != 0:
        code = ctypes.get_errno()
        if code == errno.EEXIST:
            raise GateFailure("output already exists:" + destination.name)
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


def publish(output_dir: Path, rows: list[dict[str, Any]], result: dict[str, Any]) -> None:
    ledger_bytes = deterministic_gzip_jsonl(rows)
    result_bytes = result_document(result)
    manifest_bytes = make_manifest(ledger_bytes, result_bytes)
    expected = {LEDGER: ledger_bytes, RESULT: result_bytes, MANIFEST: manifest_bytes}

    staging = AUDIT_ROOT / f".{PREFIX}.staging-{os.getpid()}-{secrets.token_hex(8)}"
    need(staging.parent == AUDIT_ROOT and not staging.exists(), "fresh direct-child staging")
    os.mkdir(staging, 0o700)
    try:
        exclusive_write(staging / LEDGER, ledger_bytes)
        exclusive_write(staging / RESULT, result_bytes)
        exclusive_write(staging / MANIFEST, manifest_bytes)
        verify_output_directory(staging, expected)
        recheck_capture_metadata()
        for name in expected:
            os.chmod(staging / name, 0o444, follow_symlinks=False)
        os.chmod(staging, 0o555)
        rename_noreplace(staging, output_dir)
    except BaseException:
        cleanup_staging(staging)
        raise
    verify_output_directory(output_dir, expected)
    recheck_capture_metadata()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-tag", required=True)
    arguments = parser.parse_args()
    need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,126}[a-z0-9]", arguments.output_tag) is not None, "safe output tag")
    AUDIT_ROOT.mkdir(parents=True, exist_ok=True)
    need(AUDIT_ROOT.is_dir() and not AUDIT_ROOT.is_symlink(), "audit root directory")
    output_dir = AUDIT_ROOT / arguments.output_tag
    need(output_dir.parent == AUDIT_ROOT, "direct-child output")
    need(output_dir.resolve(strict=False).parent == AUDIT_ROOT.resolve(strict=True), "resolved output parent")
    need(not output_dir.exists() and not output_dir.is_symlink(), "fresh output directory")

    try:
        rows, result = reconstruct()
        recheck_capture_metadata()
        publish(output_dir, rows, result)
        print(canonical({
            "status": result["status"],
            "result_sha256": digest(result),
            "transport_cohort_count": len(rows),
            "cross_chart_pair_count": result["exact_transport_cohort_certificate"]["cross_chart_pair_count"],
            "unresolved_cross_chart_pair_count": 0,
            "formal_credit": 0,
            "output": str(output_dir),
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
