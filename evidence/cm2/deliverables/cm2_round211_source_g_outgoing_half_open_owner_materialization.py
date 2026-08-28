#!/usr/bin/env python3
"""Formal local half-open owner materialization for source-G outgoing-W.

The producer pins the final Round209 feasibility probe and report, then uses
that probe as a producer-side evaluator over the pinned Round173 and Round208
producer/certificate trust boundary.  It materializes one local half-open
owner row for every nonempty factor sheet and for every clipping-curve and
endpoint incidence carried by that sheet.

These rows are local dimensional incidences.  They are deliberately not
deduplicated into global components and issue no whole-origin, whole-tube, or
global exact-key disposition credit.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round211_source_g_outgoing_half_open_owner_materialization"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round211.source-g-outgoing-half-open-owner-materialization.v1"
STATUS = (
    "CERTIFIED_LOCAL_SOURCE_G_OUTGOING_W_HALF_OPEN_OWNER_LINEAGES__"
    "NO_GLOBAL_COMPONENT_OR_EXACT_KEY_DISPOSITION"
)
MAX_INPUT_BYTES = 300 * 1024 * 1024

R209_SOURCE = "cm2_round209_source_g_outgoing_half_open_owner_probe.py"
R209_REPORT = "cm2_round209_source_g_outgoing_half_open_owner_spike_report.md"
R209_SOURCE_SHA256 = (
    "dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f"
)
R209_REPORT_SHA256 = (
    "7501e73fdad0c3721ed70b73226a4c3a4f7288f9b8429a553a50dde725812524"
)
R209_RESULT_SHA256 = (
    "7bb2117148571c23432ab8bbee86107fdadc3198c61628b2f8a46760be91a120"
)
R209_DOCUMENT_SHA256 = (
    "d561ad855ff22b067f5ac997941a0cc96ba53d368ba6dcaa303c6d6d5672471d"
)
R208_SOURCE_SHA256 = (
    "c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913"
)
R208_CERTIFICATE_SHA256 = (
    "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938"
)
R208_RESULT_SHA256 = (
    "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8"
)

EXPECTED_SHEETS = 17_716
EXPECTED_CURVES = 20_456
EXPECTED_ENDPOINTS = 40_912
EXPECTED_EMPTY_LEAVES = 608
EXPECTED_STRICT_REGIONS = 36_040
EXPECTED_SOURCE_G_EXACT_KEYS = 224_580

EXPECTED_FORMAL_SHEET_ROWS_SHA256 = (
    "ed26068a92d4ed74f54cd724680da5bc9cafa811d553415380999ae69ea7fdeb"
)
EXPECTED_FORMAL_CURVE_ROWS_SHA256 = (
    "3d93dd7860c1025bb68acf3568a0b4b66e3106189776aae4bafa12d3902a8522"
)
EXPECTED_FORMAL_ENDPOINT_ROWS_SHA256 = (
    "e5466d386b45ea8ab473a8483b5a90a244592491cdb9ecbcdf01b7a40c87d712"
)


class Round211Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round211Error(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def regular_bytes(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(before.st_nlink == 1, f"hardlink:{path.name}")
    require(0 < before.st_size <= maximum, f"size:{path.name}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            )
            == (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ),
            f"stable-open:{path.name}",
        )
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            require(total <= maximum, f"bounded-read:{path.name}")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
            == (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            ),
            f"stable-read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def pinned_bytes(path: Path, expected: str, maximum: int) -> bytes:
    raw = regular_bytes(path, maximum)
    require(
        hashlib.sha256(raw).hexdigest() == expected,
        f"SHA256:{path.name}",
    )
    return raw


def import_round209() -> Any:
    source_path = HERE / R209_SOURCE
    pinned_bytes(source_path, R209_SOURCE_SHA256, 5_000_000)
    pinned_bytes(HERE / R209_REPORT, R209_REPORT_SHA256, 5_000_000)
    spec = importlib.util.spec_from_file_location(
        "cm2_round209_frozen_for_round211",
        source_path,
    )
    require(spec is not None and spec.loader is not None, "Round209 import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def formal_id(kind: str, probe_id: str, probe_sha256: str) -> str:
    return (
        f"round211-{kind}:"
        f"{digest({'probe_id': probe_id, 'probe_row_sha256': probe_sha256})}"
    )


def without(
    row: dict[str, Any],
    removed: set[str],
) -> dict[str, Any]:
    return {key: copy.deepcopy(value) for key, value in row.items()
            if key not in removed}


def formalize_lineages(
    probe_sheets: list[dict[str, Any]],
    probe_curves: list[dict[str, Any]],
    probe_endpoints: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    sheet_map: dict[str, dict[str, Any]] = {}
    formal_sheets: list[dict[str, Any]] = []
    for probe in probe_sheets:
        sheet_id = formal_id(
            "half-open-sheet-owner",
            probe["sheet_row_id"],
            probe["row_sha256"],
        )
        payload = without(
            probe,
            {
                "sheet_row_id",
                "row_sha256",
                "formal_half_open_owner_credit",
                "whole_original_tube_credit",
                "global_exact_key_disposition_credit",
            },
        )
        row = closed_row({
            "sheet_row_id": sheet_id,
            "probe_sheet_row_id": probe["sheet_row_id"],
            "probe_sheet_row_sha256": probe["row_sha256"],
            **payload,
            "local_dimensional_owner_materialized": True,
            "formal_half_open_owner_credit": 1,
            "component_deduplication_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        sheet_map[probe["sheet_row_id"]] = row
        formal_sheets.append(row)

    curve_map: dict[str, dict[str, Any]] = {}
    formal_curves: list[dict[str, Any]] = []
    for probe in probe_curves:
        parent = sheet_map[probe["sheet_row_id"]]
        curve_id = formal_id(
            "half-open-curve-incidence-owner",
            probe["curve_row_id"],
            probe["row_sha256"],
        )
        payload = without(
            probe,
            {
                "curve_row_id",
                "sheet_row_id",
                "sheet_row_sha256",
                "row_sha256",
                "formal_half_open_owner_credit",
                "whole_original_tube_credit",
                "global_exact_key_disposition_credit",
            },
        )
        row = closed_row({
            "curve_row_id": curve_id,
            "probe_curve_row_id": probe["curve_row_id"],
            "probe_curve_row_sha256": probe["row_sha256"],
            "sheet_row_id": parent["sheet_row_id"],
            "sheet_row_sha256": parent["row_sha256"],
            **payload,
            "local_dimensional_owner_materialized": True,
            "formal_half_open_owner_credit": 1,
            "component_deduplication_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        curve_map[probe["curve_row_id"]] = row
        formal_curves.append(row)

    formal_endpoints: list[dict[str, Any]] = []
    for probe in probe_endpoints:
        parent_curve = curve_map[probe["curve_row_id"]]
        parent_sheet = sheet_map[probe["sheet_row_id"]]
        endpoint_id = formal_id(
            "half-open-endpoint-incidence-owner",
            probe["endpoint_row_id"],
            probe["row_sha256"],
        )
        payload = without(
            probe,
            {
                "endpoint_row_id",
                "curve_row_id",
                "curve_row_sha256",
                "sheet_row_id",
                "row_sha256",
                "formal_half_open_owner_credit",
                "whole_original_tube_credit",
                "global_exact_key_disposition_credit",
            },
        )
        row = closed_row({
            "endpoint_row_id": endpoint_id,
            "probe_endpoint_row_id": probe["endpoint_row_id"],
            "probe_endpoint_row_sha256": probe["row_sha256"],
            "curve_row_id": parent_curve["curve_row_id"],
            "curve_row_sha256": parent_curve["row_sha256"],
            "sheet_row_id": parent_sheet["sheet_row_id"],
            "sheet_row_sha256": parent_sheet["row_sha256"],
            **payload,
            "local_dimensional_owner_materialized": True,
            "formal_half_open_owner_credit": 1,
            "component_deduplication_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        formal_endpoints.append(row)

    formal_sheets.sort(key=lambda row: row["sheet_row_id"])
    formal_curves.sort(key=lambda row: row["curve_row_id"])
    formal_endpoints.sort(key=lambda row: row["endpoint_row_id"])
    return formal_sheets, formal_curves, formal_endpoints


def validate_formal_rows(
    sheets: list[dict[str, Any]],
    curves: list[dict[str, Any]],
    endpoints: list[dict[str, Any]],
) -> None:
    require(
        len(sheets) == EXPECTED_SHEETS
        and len(curves) == EXPECTED_CURVES
        and len(endpoints) == EXPECTED_ENDPOINTS,
        "formal dimensional counts",
    )
    require(
        len({row["sheet_row_id"] for row in sheets}) == EXPECTED_SHEETS
        and len({row["curve_row_id"] for row in curves}) == EXPECTED_CURVES
        and len({row["endpoint_row_id"] for row in endpoints})
        == EXPECTED_ENDPOINTS,
        "formal dimensional unique IDs",
    )
    sheet_by_id = {row["sheet_row_id"]: row for row in sheets}
    curve_by_id = {row["curve_row_id"]: row for row in curves}
    require(
        all(
            row["sheet_row_id"] in sheet_by_id
            and row["sheet_row_sha256"]
            == sheet_by_id[row["sheet_row_id"]]["row_sha256"]
            for row in curves
        )
        and all(
            row["sheet_row_id"] in sheet_by_id
            and row["curve_row_id"] in curve_by_id
            and row["sheet_row_sha256"]
            == sheet_by_id[row["sheet_row_id"]]["row_sha256"]
            and row["curve_row_sha256"]
            == curve_by_id[row["curve_row_id"]]["row_sha256"]
            for row in endpoints
        ),
        "formal exact lineage joins",
    )
    for row in sheets + curves + endpoints:
        copy_row = dict(row)
        row_sha256 = copy_row.pop("row_sha256")
        require(digest(copy_row) == row_sha256, "formal row closure")
        require(
            row["local_dimensional_owner_materialized"] is True
            and row["formal_half_open_owner_credit"] == 1
            and row["incidence_is_not_a_global_component"] is True
            and row["component_deduplication_credit"] == 0
            and row["whole_leaf_credit"] == 0
            and row["whole_origin_credit"] == 0
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            "formal local-only credit boundary",
        )
    pins = (
        (EXPECTED_FORMAL_SHEET_ROWS_SHA256, digest(sheets), "sheet"),
        (EXPECTED_FORMAL_CURVE_ROWS_SHA256, digest(curves), "curve"),
        (EXPECTED_FORMAL_ENDPOINT_ROWS_SHA256, digest(endpoints), "endpoint"),
    )
    for expected, actual, label in pins:
        if expected is not None:
            require(actual == expected, f"formal {label} rows pin")


def ledger(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def build_result(producer_sha256: str) -> dict[str, Any]:
    r209 = import_round209()
    _r173, r208, input_hashes = r209.validate_inputs()
    require(
        input_hashes["Round208_producer_source_sha256"] == R208_SOURCE_SHA256
        and input_hashes["Round208_certificate_sha256"]
        == R208_CERTIFICATE_SHA256
        and input_hashes["Round208_result_sha256"] == R208_RESULT_SHA256,
        "Round208 producer/certificate boundary",
    )
    leaves, regions, _faces, u2_rows = r209.validate_round195_geometry(r208)
    probe_sheets, probe_curves, probe_endpoints, owner_audit = (
        r209.build_lineages(leaves, regions)
    )
    u2_audit = r209.audit_u2(
        u2_rows,
        probe_sheets,
        probe_curves,
        probe_endpoints,
    )
    sheets, curves, endpoints = formalize_lineages(
        probe_sheets,
        probe_curves,
        probe_endpoints,
    )
    validate_formal_rows(sheets, curves, endpoints)
    origin_count = len({row["origin_row_id"] for row in sheets})
    occurrence_count = len({row["occurrence_row_id"] for row in sheets})
    retained_child_count = len({
        row["retained_child_row_id"] for row in sheets
    })
    return {
        "status": STATUS,
        "formal_input_binding": {
            "Round209_probe_source_sha256": R209_SOURCE_SHA256,
            "Round209_spike_report_sha256": R209_REPORT_SHA256,
            "Round209_probe_result_sha256": R209_RESULT_SHA256,
            "Round209_probe_document_sha256": R209_DOCUMENT_SHA256,
            "Round208_producer_source_sha256": R208_SOURCE_SHA256,
            "Round208_certificate_sha256": R208_CERTIFICATE_SHA256,
            "Round208_result_sha256": R208_RESULT_SHA256,
            "Round208_verifier_or_manifest_used": False,
            "Round209_used_as_pinned_producer_side_evaluator": True,
        },
        "formal_scope_and_conservation": {
            "input_leaf_count": len(leaves),
            "empty_leaf_count": EXPECTED_EMPTY_LEAVES,
            "nonempty_sheet_leaf_count": EXPECTED_SHEETS,
            "strict_open_3D_region_count": EXPECTED_STRICT_REGIONS,
            "strict_region_identity": "36040=608+2*17716",
            "2D_sheet_owner_row_count": EXPECTED_SHEETS,
            "1D_curve_incidence_owner_row_count": EXPECTED_CURVES,
            "0D_endpoint_incidence_owner_row_count": EXPECTED_ENDPOINTS,
            "endpoint_identity": "40912=2*20456",
            "covered_origin_count_without_whole_origin_credit": origin_count,
            "covered_occurrence_count_without_global_component_credit":
                occurrence_count,
            "covered_retained_child_count": retained_child_count,
            "all_nonempty_sheets_have_exactly_one_E_or_W_owner": True,
            "all_sheet_signature_pairs_match_except_outgoing_chart_fields":
                True,
            "incidence_rows_are_not_deduplicated_global_components": True,
            "owner_audit": owner_audit,
            "U_pipe_U_audit": u2_audit,
        },
        "formal_2D_sheet_owner_ledger":
            ledger(sheets, "sheet_row_id"),
        "formal_1D_curve_incidence_owner_ledger":
            ledger(curves, "curve_row_id"),
        "formal_0D_endpoint_incidence_owner_ledger":
            ledger(endpoints, "endpoint_row_id"),
        "formal_credit_contract": {
            "formal_2D_half_open_owner_credits": EXPECTED_SHEETS,
            "formal_1D_incidence_owner_credits": EXPECTED_CURVES,
            "formal_0D_incidence_owner_credits": EXPECTED_ENDPOINTS,
            "formal_local_dimensional_owner_credit_total":
                EXPECTED_SHEETS + EXPECTED_CURVES + EXPECTED_ENDPOINTS,
            "local_lower_dimensional_ownership_materialized": True,
            "global_component_deduplication_complete": False,
            "global_component_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator":
                EXPECTED_SOURCE_G_EXACT_KEYS,
            "D02": "BLOCKED",
            "Gate5": "10/18",
            "complete_global_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "join and deduplicate local sheet/curve/endpoint incidences into "
            "true physical components, then combine Round208 open-region "
            "rows and the separate wall-G replacement by immutable exact "
            "key; no fibre may be disposed until every occurrence and every "
            "owned lower-dimensional component in that fibre is exhausted"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "producer_imported_or_executed_by_independent_verifier": False,
        },
    }


def validate_output(path: Path) -> Path:
    absolute = path.resolve(strict=False)
    require(absolute.parent == HERE.resolve(), "output parent")
    official = absolute.name == OUTPUT.name
    replay = (
        absolute.name.startswith(f".{PREFIX}_replay_")
        and absolute.name.endswith(".json")
        and absolute.name.count("/") == 0
    )
    require(official or replay, "output filename")
    require(not absolute.is_symlink(), "output symlink")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1,
            "output existing regular unique",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{PREFIX}.tmp.",
        dir=HERE,
    )
    temp_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, destination)
        directory = os.open(HERE, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temp_path.exists():
            temp_path.unlink()


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
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
