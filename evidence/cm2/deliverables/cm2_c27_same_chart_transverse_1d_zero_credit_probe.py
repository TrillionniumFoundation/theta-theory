#!/usr/bin/env python3
"""Counterexample-first zero-credit gate for 448 same-chart transverse lines.

The candidate denominator is generated as the Cartesian product of the 112
R291 transverse one-dimensional physical cells with the four current source
double sheets in the same chart.  No Round306C27 source, FAMILIES registry,
or edge ledger is imported or used as a candidate filter.

The decisive test is deliberately elementary and exact.  Each transverse
curve is joined to its R182 pair-arrangement row and R179 containing box.
Its full physical support is contained in the exact interval-Newton p-domain
of that box.  That closed p-domain is compared to each source sheet's exact
closed p-interval.  A strictly positive rational gap proves nonincidence
without assuming that identifiers, partitions, or components imply it.

All input files are opened once with O_NOFOLLOW.  Hashing and parsing consume
the identical captured bytes.  PASS remains diagnostic and awards no credit.
"""

from __future__ import annotations

import argparse
from collections import Counter
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
PREFIX = "cm2_c27_same_chart_transverse_1d_zero_credit_v1"
LEDGER = PREFIX + "_exact_partition_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
MANIFEST = PREFIX + "_manifest.json"

R182_CERT = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_certificate.json"
R182_ROWS = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R182_VERIFY = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json"
R182_MANIFEST = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256"
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

INPUT_PINS = {
    R182_CERT: "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08",
    R182_ROWS: "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    R182_VERIFY: "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    R182_MANIFEST: "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5",
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
}

CHARTS = ("G:E", "G:W", "G:N", "G:S")
EXPECTED_R291_KIND_CENSUS = {
    "ROUND182_GRAPH_SHEET_LEAF": 111_524,
    "ROUND208_DIRECT_GRAPH_SIDE_REGION": 608,
    "ROUND179_NEGATIVE_T0_SHADOW_PATCH": 544,
    "ROUND179_POSITIVE_T0_RETAINED_OWNER": 440,
    "SOURCE_EXACT_T0_SHEET_CELL": 224,
    "ROUND182_TRANSVERSE_1D_LINE": 112,
}

PAIR_COLUMNS = (
    "row_id", "Round179_pair_row_id", "origin_row_id", "parent_id", "chart",
    "owner_target", "reason_labels", "source_graph_equation",
    "source_graph_exact_factorization", "second_graph_equation",
    "source_graph_t_boundary_face", "existence_classification", "p_lower_sign",
    "p_upper_sign", "p_lower_value_interval", "p_upper_value_interval",
    "strict_p_derivative_sign", "strict_p_derivative_interval",
    "strict_source_t_derivative_sign", "strict_source_t_derivative_interval",
    "strict_2x2_Jacobian_minor_sign", "strict_2x2_Jacobian_minor_interval",
    "first_empty_source_factor_interval", "first_empty_target_factor_interval",
    "interval_newton_domain", "interval_newton_interior", "interval_newton_image",
    "actual_intersection_dimension", "actual_1D_intersection_component_count",
    "actual_boundary_0D_corner_incidence_count",
    "containing_Round179_retained_child_row_id",
    "integer_wall_endpoint_owner_status", "whole_original_tube_credit",
    "global_exact_key_disposition_credit", "provenance",
)
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
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


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
        need(len(payload) == opened.st_size, "captured input size:" + name)
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
    stream: TextIO,
    *,
    marker: str,
    nested_rows: bool,
    expected_type: type = dict,
) -> Iterator[Any]:
    buffer = ""
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing marker:" + marker)
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
    payload: bytes | bytearray,
    marker: str,
    *,
    nested_rows: bool = False,
    expected_type: type = dict,
) -> Iterator[Any]:
    with io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8", errors="strict", newline="") as stream:
        yield from stream_array(
            stream,
            marker=marker,
            nested_rows=nested_rows,
            expected_type=expected_type,
        )


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


def capture_manifests_and_r182_authority() -> dict[str, Any]:
    for manifest_name in (
        R182_MANIFEST, R179_MANIFEST, R236_MANIFEST, R248_MANIFEST,
        R291_MANIFEST, R295A_MANIFEST, C15_MANIFEST,
    ):
        payload = capture_input(manifest_name)
        text = bytes(payload).decode("ascii", "strict")
        need(text.endswith("\n") and "  " in text, "manifest syntax:" + manifest_name)
        del payload

    certificate_bytes = capture_input(R182_CERT)
    certificate = closed_wrapper(certificate_bytes, R182_CERT)
    del certificate_bytes
    pair = certificate["dimension_safe_ledger"]["pair_1D_intersections"]
    need(
        certificate["status"]
        == "CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_CLIPPED_GRAPH_AND_PAIR_ARRANGEMENT__NO_GLOBAL_EXACT_KEY_DISPOSITION_OR_D02_PROMOTION"
        and pair["actual_component_count"] == 112
        and pair["existence_by_p_face_bracket_and_interval_Newton"] is True
        and pair["transversality_by_strict_2x2_Jacobian_minor"] is True
        and certificate["row_attachment"]["file_sha256"] == INPUT_PINS[R182_ROWS],
        "R182 authority contract",
    )
    verification_bytes = capture_input(R182_VERIFY)
    verification = closed_wrapper(verification_bytes, R182_VERIFY)
    del verification_bytes
    need(
        verification["status"] == "PASS"
        and verification["certificate_result_sha256"] == digest(certificate),
        "R182 verification binding",
    )
    return {
        "R182_certificate_sha256": INPUT_PINS[R182_CERT],
        "R182_rows_sha256": INPUT_PINS[R182_ROWS],
        "R182_verification_sha256": INPUT_PINS[R182_VERIFY],
        "R182_certified_transverse_component_count": 112,
        "R182_interval_Newton_existence_bound": True,
        "R182_strict_Jacobian_transversality_bound": True,
    }


def reconstruct_source_sheets() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    r236_bytes = capture_input(R236_CERT)
    r236 = closed_wrapper(r236_bytes, R236_CERT)
    del r236_bytes
    partitions = r236["double_endpoint_partition_rows"]
    need(len(partitions) == 16, "R236 double partition count")
    partition_charts: dict[str, str] = {}
    for row in partitions:
        pid = row["double_endpoint_partition_row_id"]
        signatures = (
            row["negative_to_positive_signature"],
            row["positive_to_negative_signature"],
            row["same_sign_event_absent_signature"],
        )
        charts = {signature["source_chart"] for signature in signatures}
        need(len(charts) == 1 and next(iter(charts)) in CHARTS, "R236 source chart")
        need(pid not in partition_charts, "R236 partition uniqueness")
        partition_charts[pid] = next(iter(charts))

    r248_bytes = capture_input(R248_CERT)
    sheets: list[dict[str, Any]] = []
    kind_census: Counter[str] = Counter()
    for row in plain_array(
        r248_bytes,
        '"formal_wall_half_open_sheet_owner_ledger":',
        nested_rows=True,
    ):
        kind_census[row["source_partition_kind"]] += 1
        if (
            row["source_partition_kind"] == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET"
            and row["endpoint_factor"] == "source"
        ):
            check_row(row, "R248 source double sheet")
            pid = row["source_partition_row_id"]
            need(pid in partition_charts, "R248/R236 partition join")
            base = [str(Fraction(value)) for value in row["exact_closed_base_rectangle"]]
            need(len(base) == 4, "R248 sheet p/s rectangle")
            sheets.append({
                "member_id": row["wall_sheet_node_id"],
                "partition_row_id": pid,
                "chart": partition_charts[pid],
                "exact_closed_p_s_rectangle": base,
                "owner_official_key_id": row["owner_official_key_id"],
                "owner_signature_sha256": row["owner_signature_sha256"],
                "R248_row_sha256": row["row_sha256"],
            })
    del r248_bytes
    need(
        kind_census
        == {
            "ROUND235_SINGLE_ENDPOINT_GRAPH_SHEET": 38_328,
            "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET": 32,
        },
        "R248 sheet census",
    )
    need(len(sheets) == 16 and len({row["member_id"] for row in sheets}) == 16, "16 source sheets")
    need(Counter(row["chart"] for row in sheets) == {chart: 4 for chart in CHARTS}, "four source sheets per chart")
    sheets.sort(key=canonical)
    return sheets, {
        "source_sheet_count": 16,
        "source_sheet_chart_census": dict(sorted(Counter(row["chart"] for row in sheets).items())),
        "source_sheet_rows_sha256": digest(sheets),
    }


def load_transverse_cells() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    r291_bytes = capture_input(R291_LEDGER)
    selected: list[dict[str, Any]] = []
    kind_census: Counter[str] = Counter()
    disposition_count = 0
    physical_count = 0
    physical_keys: set[tuple[str, int]] = set()
    for disposition in gzip_array(r291_bytes):
        check_row(disposition, "R291 disposition")
        disposition_count += 1
        disposition_id = disposition["complete_lower_stratum_local_disposition_row_id"]
        chart = disposition["source_chart"]
        need(chart in CHARTS, "R291 chart")
        for index, cell in enumerate(disposition["physical_witness_cells"]):
            key = (disposition_id, index)
            need(key not in physical_keys, "R291 physical key uniqueness")
            physical_keys.add(key)
            physical_count += 1
            kind = cell["witness_kind"]
            kind_census[kind] += 1
            if kind == "ROUND182_TRANSVERSE_1D_LINE":
                selected.append({
                    "key": key,
                    "disposition_row_id": disposition_id,
                    "physical_witness_cell_index": index,
                    "chart": chart,
                    "pair_row_id": cell["pair_row_id"],
                    "retained_child_row_id": cell["containing_retained_child_row_id"],
                    "interval_newton_domain": [str(Fraction(value)) for value in cell["interval_newton_domain"]],
                    "interval_newton_image": cell["interval_newton_image"],
                    "strict_2x2_Jacobian_minor_sign": cell["strict_2x2_Jacobian_minor_sign"],
                    "cell_sha256": digest(cell),
                    "R291_disposition_row_sha256": disposition["row_sha256"],
                })
    del r291_bytes
    need(disposition_count == 55_428 and physical_count == 113_452, "R291 complete physical census")
    need(kind_census == EXPECTED_R291_KIND_CENSUS, "R291 witness-kind census")
    need(len(selected) == 112, "R291 transverse count")
    need(len({row["pair_row_id"] for row in selected}) == 112, "R291 transverse pair uniqueness")
    need(len({row["retained_child_row_id"] for row in selected}) == 112, "R291 transverse retained uniqueness")
    return selected, {
        "R291_disposition_count": disposition_count,
        "R291_physical_cell_count": physical_count,
        "R291_witness_kind_census": dict(sorted(kind_census.items())),
        "selected_transverse_cell_count": len(selected),
        "selected_transverse_cells_sha256": digest(sorted(selected, key=canonical)),
    }


def bind_pair_rows(cells: list[dict[str, Any]]) -> dict[str, Any]:
    selected_ids = {row["pair_row_id"] for row in cells}
    r182_bytes = capture_input(R182_ROWS)
    selected: dict[str, dict[str, Any]] = {}
    count = 0
    classification_census: Counter[str] = Counter()
    for packed in plain_array(
        r182_bytes,
        '"pair_intersection_rows":',
        expected_type=list,
    ):
        count += 1
        need(len(packed) == len(PAIR_COLUMNS), "R182 pair packed width")
        row = dict(zip(PAIR_COLUMNS, packed, strict=True))
        classification_census[row["existence_classification"]] += 1
        if row["row_id"] in selected_ids:
            need(row["row_id"] not in selected, "selected R182 pair uniqueness")
            need(
                row["existence_classification"]
                == "UNIQUE_TRANSVERSE_1D_INTERSECTION_LINE__P_BRACKET_AND_INTERVAL_NEWTON"
                and row["source_graph_equation"] == "t=0"
                and row["interval_newton_interior"] is True
                and row["actual_intersection_dimension"] == "EXACT_DIMENSION_1"
                and row["actual_1D_intersection_component_count"] == 1
                and row["strict_2x2_Jacobian_minor_sign"] in {"STRICT_POSITIVE", "STRICT_NEGATIVE"}
                and row["strict_p_derivative_sign"] in {"STRICT_POSITIVE", "STRICT_NEGATIVE"},
                "R182 selected transverse semantics",
            )
            selected[row["row_id"]] = row
    del r182_bytes
    need(count == 336, "R182 pair row count")
    need(
        classification_census
        == {
            "EMPTY__ONE_PREDICATE_HAS_EMPTY_ZERO_SET": 8,
            "EMPTY__STRICT_SAME_SIGN_P_FACES": 216,
            "UNIQUE_TRANSVERSE_1D_INTERSECTION_LINE__P_BRACKET_AND_INTERVAL_NEWTON": 112,
        },
        "R182 pair classification census",
    )
    need(set(selected) == selected_ids, "R182/R291 selected pair cover")
    for cell in cells:
        pair = selected[cell["pair_row_id"]]
        need(
            pair["chart"] == cell["chart"]
            and pair["containing_Round179_retained_child_row_id"] == cell["retained_child_row_id"]
            and [str(Fraction(value)) for value in pair["interval_newton_domain"]] == cell["interval_newton_domain"]
            and pair["interval_newton_image"] == cell["interval_newton_image"]
            and pair["strict_2x2_Jacobian_minor_sign"] == cell["strict_2x2_Jacobian_minor_sign"],
            "R182/R291 exact transverse binding",
        )
        cell["pair"] = pair
        cell["R182_pair_row_sha256"] = digest(pair)
    return {
        "R182_pair_row_count": count,
        "R182_pair_classification_census": dict(sorted(classification_census.items())),
        "R182_selected_pair_count": len(selected),
        "R182_selected_pair_rows_sha256": digest(sorted(selected.values(), key=canonical)),
    }


def bind_retained_boxes(cells: list[dict[str, Any]]) -> dict[str, Any]:
    retained_ids = {row["retained_child_row_id"] for row in cells}
    r179_bytes = capture_input(R179_ROWS)
    selected: dict[str, dict[str, Any]] = {}
    count = 0
    for packed in plain_array(
        r179_bytes,
        '"retained_3d_child_rows":',
        expected_type=list,
    ):
        count += 1
        need(len(packed) == len(R179_COLUMNS), "R179 retained packed width")
        if packed[0] in retained_ids:
            need(packed[0] not in selected, "selected R179 retained uniqueness")
            selected[packed[0]] = dict(zip(R179_COLUMNS, packed, strict=True))
    del r179_bytes
    need(count == 106_680 and set(selected) == retained_ids, "R179 selected retained cover")
    for cell in cells:
        retained = selected[cell["retained_child_row_id"]]
        bounds = [str(Fraction(value)) for value in retained["box"]]
        need(
            retained["chart"] == cell["chart"]
            and len(bounds) == 6
            and bounds[2:4] == cell["interval_newton_domain"],
            "R179/R182/R291 exact containing box",
        )
        t0, t1 = Fraction(bounds[0]), Fraction(bounds[1])
        need(t0 == 0 or t1 == 0, "transverse source graph lies on t=0 box face")
        cell["exact_containing_t_p_s_bounds"] = bounds
        cell["R179_retained_row_sha256"] = digest(retained)
    return {
        "R179_retained_row_count": count,
        "R179_selected_retained_count": len(selected),
        "R179_selected_retained_rows_sha256": digest(sorted(selected.values(), key=canonical)),
    }


def bind_registry_targets(cells: list[dict[str, Any]]) -> tuple[set[str], dict[str, Any]]:
    selected_keys = {row["key"] for row in cells}
    by_key = {row["key"]: row for row in cells}
    r295_bytes = capture_input(R295A_LEDGER)
    count = 0
    selected_count = 0
    target_ids: set[str] = set()
    reference_census: Counter[int] = Counter()
    for binding in gzip_array(r295_bytes):
        check_row(binding, "R295A binding")
        count += 1
        key = (
            binding["Round291_local_disposition_row_id"],
            binding["physical_witness_cell_index"],
        )
        if key not in selected_keys:
            continue
        selected_count += 1
        cell = by_key[key]
        need("binding" not in cell, "selected R295A key uniqueness")
        targets = binding["target_Round294_registry_rows"]
        ids = binding["target_Round294_registry_occurrence_ids"]
        need(
            binding["witness_kind"] == "ROUND182_TRANSVERSE_1D_LINE"
            and binding["source_chart"] == cell["chart"]
            and ids == [row["registry_occurrence_id"] for row in targets]
            and len(ids) == binding["target_Round294_registry_reference_count"]
            and len(ids) > 0,
            "selected R295A transverse binding",
        )
        reduced_targets = []
        for target in targets:
            need(target["physical_support_chart"] == cell["chart"], "R295A target chart")
            reduced_targets.append({
                "registry_occurrence_id": target["registry_occurrence_id"],
                "official_key_id": target["official_key_id"],
                "complete_10_field_return_signature_sha256": target["complete_10_field_return_signature_sha256"],
                "physical_support_chart": target["physical_support_chart"],
                "Round294_occurrence_registry_row_sha256": target["Round294_occurrence_registry_row_sha256"],
            })
            target_ids.add(target["registry_occurrence_id"])
        cell["binding"] = {
            "row_id": binding["Round295A_R291_physical_incidence_binding_row_id"],
            "row_sha256": binding["row_sha256"],
            "classification": binding["Round295A_binding_classification"],
            "targets": reduced_targets,
        }
        reference_census[len(ids)] += 1
    del r295_bytes
    need(count == 113_452 and selected_count == 112, "R295A complete/selected counts")
    need(all("binding" in row for row in cells), "all transverse cells R295A-bound")
    return target_ids, {
        "R295A_binding_count": count,
        "R295A_selected_transverse_binding_count": selected_count,
        "R295A_selected_target_occurrence_count": len(target_ids),
        "R295A_selected_reference_count_census": {
            str(key): value for key, value in sorted(reference_census.items())
        },
    }


def load_components(selected_ids: set[str]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    c15_bytes = capture_input(C15_LEDGER)
    selected: dict[str, dict[str, Any]] = {}
    count = 0
    for row in gzip_jsonl(c15_bytes):
        count += 1
        member = row["registry_member_id"]
        if member in selected_ids:
            check_row(row, "selected C15 member")
            need(member not in selected, "selected C15 uniqueness")
            selected[member] = {
                "component_id": row["fresh_component_id"],
                "official_key_id": row["official_key_id"],
                "C15_row_sha256": row["row_sha256"],
            }
    del c15_bytes
    need(count == 502_204 and set(selected) == selected_ids, "C15 selected exact cover")
    return selected, {
        "C15_member_count": count,
        "C15_selected_member_count": len(selected),
        "C15_selected_component_count": len({row["component_id"] for row in selected.values()}),
    }


def interval_relation(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> tuple[str, Fraction]:
    overlap = min(left[1], right[1]) - max(left[0], right[0])
    if overlap > 0:
        return "STRICT_POSITIVE_OVERLAP", overlap
    if overlap == 0:
        return "CLOSED_ENDPOINT_TOUCH", overlap
    return "STRICTLY_DISJOINT", -overlap


def component_relation(source: str, targets: list[dict[str, Any]]) -> str:
    same = sum(target["component_id"] == source for target in targets)
    if same == len(targets):
        return "ALL_TARGETS_SAME_C15_COMPONENT"
    if same == 0:
        return "ALL_TARGETS_CROSS_C15_COMPONENT"
    return "MIXED_SAME_AND_CROSS_C15_COMPONENT_TARGETS"


def owner_relation(sheet: dict[str, Any], targets: list[dict[str, Any]]) -> str:
    keys = [target for target in targets if target["official_key_id"] == sheet["owner_official_key_id"]]
    exact = [
        target for target in keys
        if target["complete_10_field_return_signature_sha256"] == sheet["owner_signature_sha256"]
    ]
    if exact:
        return "AT_LEAST_ONE_EXACT_OFFICIAL_KEY_AND_SIGNATURE_MATCH"
    if keys:
        return "OFFICIAL_KEY_MATCH_WITH_SIGNATURE_MISMATCH"
    return "NO_OFFICIAL_KEY_MATCH"


def closed_row(body: dict[str, Any]) -> dict[str, Any]:
    row = dict(body)
    row["row_sha256"] = digest(row)
    return row


def build_partition(
    sheets: list[dict[str, Any]],
    cells: list[dict[str, Any]],
    components: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    for sheet in sheets:
        member = sheet["member_id"]
        need(member in components, "sheet C15 binding")
        need(components[member]["official_key_id"] == sheet["owner_official_key_id"], "sheet C15 key")
        sheet["component_id"] = components[member]["component_id"]
        sheet["C15_row_sha256"] = components[member]["C15_row_sha256"]

    states: dict[tuple[Any, ...], dict[str, Any]] = {}
    p_order_census: Counter[str] = Counter()
    s_relation_census: Counter[str] = Counter()
    component_census: Counter[str] = Counter()
    owner_census: Counter[str] = Counter()
    priority_count = 0
    cross_component_candidate_count = 0
    direct_candidate_count = 0
    minimum_p_gap: Fraction | None = None
    pair_count = 0

    for cell in cells:
        pair = cell["pair"]
        bounds = [Fraction(value) for value in cell["exact_containing_t_p_s_bounds"]]
        pair_p = (bounds[2], bounds[3])
        pair_s = (bounds[4], bounds[5])
        need([str(value) for value in pair_p] == cell["interval_newton_domain"], "pair p domain")
        raw_targets = cell["binding"]["targets"]
        targets = []
        for target in raw_targets:
            member = target["registry_occurrence_id"]
            need(member in components, "target C15 binding")
            need(components[member]["official_key_id"] == target["official_key_id"], "target C15 key")
            targets.append({**target, **components[member]})

        matching_sheets = [sheet for sheet in sheets if sheet["chart"] == cell["chart"]]
        need(len(matching_sheets) == 4, "four same-chart sheets")
        for sheet in matching_sheets:
            pair_count += 1
            base = [Fraction(value) for value in sheet["exact_closed_p_s_rectangle"]]
            sheet_p = (base[0], base[1])
            sheet_s = (base[2], base[3])
            p_relation, p_measure = interval_relation(sheet_p, pair_p)
            s_relation, s_measure = interval_relation(sheet_s, pair_s)
            need(p_relation == "STRICTLY_DISJOINT" and p_measure > 0, "strict transverse/sheet p gap")
            if sheet_p[1] < pair_p[0]:
                p_order = "SOURCE_SHEET_P_INTERVAL_STRICTLY_LEFT_OF_TRANSVERSE_NEWTON_DOMAIN"
                exact_gap = pair_p[0] - sheet_p[1]
            else:
                need(pair_p[1] < sheet_p[0], "strict p ordering")
                p_order = "TRANSVERSE_NEWTON_DOMAIN_STRICTLY_LEFT_OF_SOURCE_SHEET_P_INTERVAL"
                exact_gap = sheet_p[0] - pair_p[1]
            need(exact_gap == p_measure, "p gap identity")
            minimum_p_gap = exact_gap if minimum_p_gap is None else min(minimum_p_gap, exact_gap)

            comp = component_relation(sheet["component_id"], targets)
            own = owner_relation(sheet, targets)
            any_cross = any(target["component_id"] != sheet["component_id"] for target in targets)
            priority = any(
                target["component_id"] != sheet["component_id"]
                and target["official_key_id"] == sheet["owner_official_key_id"]
                and target["complete_10_field_return_signature_sha256"] == sheet["owner_signature_sha256"]
                for target in targets
            )
            cross_component_candidate_count += int(any_cross)
            priority_count += int(priority)
            representative = {
                "source_sheet_member_id": sheet["member_id"],
                "source_sheet_component_id": sheet["component_id"],
                "source_sheet_chart": sheet["chart"],
                "source_sheet_exact_closed_p_s_rectangle": sheet["exact_closed_p_s_rectangle"],
                "R182_pair_row_id": pair["row_id"],
                "R182_pair_row_sha256": cell["R182_pair_row_sha256"],
                "R291_disposition_row_id": cell["disposition_row_id"],
                "R291_physical_witness_cell_index": cell["physical_witness_cell_index"],
                "R291_physical_witness_cell_sha256": cell["cell_sha256"],
                "transverse_exact_containing_t_p_s_bounds": cell["exact_containing_t_p_s_bounds"],
                "transverse_interval_newton_p_domain": cell["interval_newton_domain"],
                "target_registry_occurrence_ids": [target["registry_occurrence_id"] for target in targets],
                "target_component_ids": [target["component_id"] for target in targets],
                "exact_p_gap": str(exact_gap),
                "priority_exact_owner_match_cross_component": priority,
            }
            key = (
                sheet["chart"], p_order, s_relation, comp, own, priority,
                len(targets), cell["binding"]["classification"],
                pair["source_graph_t_boundary_face"],
                pair["strict_2x2_Jacobian_minor_sign"],
            )
            state = states.get(key)
            if state is None:
                state = {
                    "multiplicity": 0,
                    "representative": representative,
                    "representative_bytes": canonical(representative),
                    "minimum_p_gap": exact_gap,
                    "maximum_p_gap": exact_gap,
                    "s_measure_minimum": s_measure,
                    "s_measure_maximum": s_measure,
                }
                states[key] = state
            else:
                encoded = canonical(representative)
                if encoded < state["representative_bytes"]:
                    state["representative"] = representative
                    state["representative_bytes"] = encoded
                state["minimum_p_gap"] = min(state["minimum_p_gap"], exact_gap)
                state["maximum_p_gap"] = max(state["maximum_p_gap"], exact_gap)
                state["s_measure_minimum"] = min(state["s_measure_minimum"], s_measure)
                state["s_measure_maximum"] = max(state["s_measure_maximum"], s_measure)
            state["multiplicity"] += 1
            p_order_census[p_order] += 1
            s_relation_census[s_relation] += 1
            component_census[comp] += 1
            owner_census[own] += 1

    need(pair_count == 448, "same-chart transverse denominator")
    need(minimum_p_gap == Fraction(35, 64), "minimum exact p gap")
    need(direct_candidate_count == 0, "direct support-intersection candidate zero")
    need(
        s_relation_census
        == {
            "STRICT_POSITIVE_OVERLAP": 224,
            "CLOSED_ENDPOINT_TOUCH": 128,
            "STRICTLY_DISJOINT": 96,
        },
        "s relation census",
    )

    rows: list[dict[str, Any]] = []
    for key, state in states.items():
        body = {
            "schema": "cm2.c27-semantic-counterexample-gate.same-chart-transverse-1d.zero-credit.v1.cohort-row.v1",
            "cohort_id": "c27-same-chart-transverse-cohort:" + digest(list(key)),
            "chart": key[0],
            "p_order": key[1],
            "s_interval_relation": key[2],
            "C15_component_relation": key[3],
            "half_open_owner_relation": key[4],
            "priority_exact_owner_match_cross_component": key[5],
            "target_reference_count": key[6],
            "R295A_binding_classification": key[7],
            "R182_source_graph_t_boundary_face": key[8],
            "R182_strict_2x2_Jacobian_minor_sign": key[9],
            "multiplicity": state["multiplicity"],
            "minimum_exact_p_gap": str(state["minimum_p_gap"]),
            "maximum_exact_p_gap": str(state["maximum_p_gap"]),
            "s_relation_measure_minimum": str(state["s_measure_minimum"]),
            "s_relation_measure_maximum": str(state["s_measure_maximum"]),
            "canonical_representative": state["representative"],
            "route": "EXACT_NONINCIDENCE__TRANSVERSE_CURVE_CONTAINING_NEWTON_P_DOMAIN_STRICTLY_DISJOINT_FROM_SOURCE_SHEET_P_INTERVAL",
            "same_physical_point_witness_count": 0,
            "formal_component_edge_credit": 0,
            "formal_maximality_credit": 0,
        }
        rows.append(closed_row(body))
    rows.sort(key=canonical)
    need(sum(row["multiplicity"] for row in rows) == 448, "cohort exact cover")
    return rows, {
        "same_chart_transverse_pair_count": pair_count,
        "candidate_denominator_identity": "112 R291 transverse cells * 4 current source sheets in the identical chart",
        "exact_route_census": {
            "EXACT_NONINCIDENCE__TRANSVERSE_CURVE_CONTAINING_NEWTON_P_DOMAIN_STRICTLY_DISJOINT_FROM_SOURCE_SHEET_P_INTERVAL": 448,
        },
        "p_order_census": dict(sorted(p_order_census.items())),
        "s_interval_relation_census": dict(sorted(s_relation_census.items())),
        "C15_component_relation_census": dict(sorted(component_census.items())),
        "half_open_owner_relation_census": dict(sorted(owner_census.items())),
        "cross_component_candidate_pair_count_before_geometry_test": cross_component_candidate_count,
        "priority_exact_owner_match_cross_component_pair_count": priority_count,
        "minimum_exact_p_gap": str(minimum_p_gap),
        "direct_same_physical_support_candidate_count_after_exact_p_test": direct_candidate_count,
        "confirmed_cross_component_same_physical_point_witness_count": 0,
        "unresolved_same_chart_transverse_pair_count": 0,
        "cohort_count": len(rows),
        "cohort_multiplicity_sum": sum(row["multiplicity"] for row in rows),
        "cohort_rows_sha256": digest(rows),
        "each_pair_has_exactly_one_route": True,
    }


def reconstruct() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    authority = capture_manifests_and_r182_authority()
    sheets, sheet_audit = reconstruct_source_sheets()
    cells, r291_audit = load_transverse_cells()
    r182_audit = bind_pair_rows(cells)
    r179_audit = bind_retained_boxes(cells)
    target_ids, r295_audit = bind_registry_targets(cells)
    selected_ids = target_ids | {sheet["member_id"] for sheet in sheets}
    components, c15_audit = load_components(selected_ids)
    rows, partition = build_partition(sheets, cells, components)

    result = {
        "schema": "cm2.c27-semantic-counterexample-gate.same-chart-transverse-1d.zero-credit.v1",
        "status": "PASS_ZERO_CREDIT__448_SAME_CHART_TRANSVERSE_1D_PAIRS_EXACTLY_NONINCIDENT_BY_STRICT_RATIONAL_P_GAP__C27_C28_C29_REJECT_UNCHANGED",
        "subgate_decision": "PASS_DIAGNOSTIC_ZERO_CREDIT__NO_SAME_PHYSICAL_POINT_WITNESS",
        "unconditional_C27_C28_C29_decision": "REJECT_REMAINS_IN_FORCE",
        "scope_contract": {
            "semantic_family": "SAME_CHART_TRANSVERSE_1D",
            "candidate_universe": "COMPLETE_112_R291_TRANSVERSE_CELLS_X_FOUR_CURRENT_SOURCE_DOUBLE_SHEETS_IN_THE_IDENTICAL_CHART",
            "Round306C27_imported_or_executed": False,
            "Round306C27_FAMILIES_copied": False,
            "edge_ledger_used_as_candidate_universe": False,
            "same_retained_child_or_partition_used_as_incidence_filter": False,
            "all_inputs_O_NOFOLLOW_single_byte_capture": True,
            "input_hashing_and_parsing_use_identical_captured_bytes": True,
            "input_path_content_reread_count": 0,
        },
        "R182_authority_binding": authority,
        "source_sheet_reconstruction": sheet_audit,
        "transverse_support_reconstruction": {
            **r291_audit, **r182_audit, **r179_audit,
        },
        "registry_component_binding": {**r295_audit, **c15_audit},
        "exact_partition_certificate": partition,
        "counterexample_gate": {
            "counterexample_first": True,
            "cross_component_candidates_prioritized_before_geometry_disposition": True,
            "cross_component_candidate_pair_count_before_geometry_test": partition["cross_component_candidate_pair_count_before_geometry_test"],
            "direct_same_physical_support_candidate_count": 0,
            "confirmed_legal_cross_component_witness_count": 0,
            "verdict": "NO_WITNESS_IN_THIS_EXACT_448_PAIR_DENOMINATOR",
        },
        "diagnostic_composition_only": {
            "alias_rechart_v1_cross_chart_pairs_closed_by_one_implementation": 1_361_424,
            "same_chart_transverse_pairs_closed_here": 448,
            "remaining_cross_component_lower_owner_contacts": 24,
            "remaining_current_graph_side_cross_chart_pairs": 192,
            "diagnostic_residual_sum": 216,
            "not_formal_authority": True,
            "alias_v1_double_seed_is_not_an_independent_semantic_proof": True,
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
            "build an independent alias/rechart implementation that explicitly acts Jx/Jy/JxJy on coordinates, normals, and positions and solves the same-point equations",
            "independently route the 192 current-graph-side cross-chart pairs",
            "resolve the 24 codimension-two lower-owner contacts from original lower-dimensional support ownership",
            "extend the counterexample-first gate to the remaining C27 families",
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
        "schema": "cm2.c27-semantic-counterexample-gate.same-chart-transverse-1d.zero-credit.v1.wrapper.v1",
    }) + b"\n"


def manifest_bytes(ledger: bytes, result: bytes) -> bytes:
    members = [
        {"name": LEDGER, "sha256": hashlib.sha256(ledger).hexdigest(), "size": len(ledger)},
        {"name": RESULT, "sha256": hashlib.sha256(result).hexdigest(), "size": len(result)},
    ]
    body = {
        "schema": "cm2.c27-semantic-counterexample-gate.same-chart-transverse-1d.zero-credit.v1.manifest.v1",
        "member_count": 2,
        "members": members,
        "members_sha256": digest(members),
        "formal_credit": 0,
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
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        need(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
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
        need(
            member["size"] == len(payload)
            and member["sha256"] == hashlib.sha256(payload).hexdigest(),
            "manifest member:" + member["name"],
        )


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
            "cohort_count": len(rows),
            "same_chart_transverse_pair_count": 448,
            "unresolved_pair_count": 0,
            "formal_credit": 0,
            "output": str(output),
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
