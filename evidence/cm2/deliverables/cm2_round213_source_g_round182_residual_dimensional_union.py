#!/usr/bin/env python3
"""Formal local-dimensional union over every Round182 residual source-G origin.

This producer joins the independently accepted Round204, Round208, and
Round211 local packages back to the frozen Round182 residual-origin registry.
It does not deduplicate physical components, promote a whole original tube,
exhaust a global exact-key fibre, or create a source-G disposition.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round213_source_g_round182_residual_dimensional_union"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round213.source-g-round182-residual-dimensional-union.v1"
STATUS = (
    "CERTIFIED_LOCAL_SOURCE_G_ROUND182_RESIDUAL_DIMENSIONAL_UNION__"
    "NO_PHYSICAL_COMPONENT_WHOLE_TUBE_OR_GLOBAL_FIBRE_DISPOSITION"
)
MAX_INPUT_BYTES = 500 * 1024 * 1024

R182 = "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
R204 = "cm2_round204_source_g_wall_return_signature_local_replacement"
R208 = "cm2_round208_source_g_outgoing_direct_signature_materialization"
R211 = "cm2_round211_source_g_outgoing_half_open_owner_materialization"

PACKAGE_MANIFESTS = {
    R182: (
        f"{R182}_manifest.sha256",
        "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5",
        7,
    ),
    R204: (
        f"{R204}_manifest.sha256",
        "ae3310f8ae0a4c565a39153e268c09fcb983aa04cccce6e3d7dd72fb7803c213",
        6,
    ),
    R208: (
        f"{R208}_manifest.sha256",
        "f35c1d00bb1e5c6fc35465ffa29fc66e5648c009d07069ea09b6332c657c1c83",
        6,
    ),
    R211: (
        f"{R211}_manifest.sha256",
        "c0cf8b70de6dd147fd1009c97d28549ec4571f9d6c82b8bf46dba023e3fe943c",
        6,
    ),
}
EXPECTED_RESULT_DIGESTS = {
    "Round182_attachment":
        "9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269",
    "Round182_verification":
        "61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797",
    "Round204_certificate":
        "ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd",
    "Round204_verification":
        "bd523e7c288e8b6830a7e94d78d06039b324bc8d2fdcfd38dab2ec85b532b1fd",
    "Round208_certificate":
        "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8",
    "Round208_verification":
        "2f902656d553bea37640120a1c73ae8085f23f6a0c5fe091ecd6c45ed545117b",
    "Round211_certificate":
        "3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b",
    "Round211_verification":
        "eed5687f736c6244421ec432a4d1fc283d84386147293825a19837173cbb819d",
}

EXPECTED_R204_ORIGIN_IDS_SHA256 = (
    "5ead6a0c6f0d84f257ca43d4c3388feb1736201789e0c8d0b92ccfde829ae71e"
)
EXPECTED_R208_ORIGIN_IDS_SHA256 = (
    "10dd4db3aad3063bf848908eb19de2e7363b7e280d24420ec50723688eed3947"
)
EXPECTED_ORIGIN_UNION_SHA256 = (
    "5799c69f51d4dbdfd890fffc4b4fa260bc76f022ee37dc0c3bf036e477fc8156"
)
EXPECTED_PARENT_UNION_SHA256 = (
    "96aa885986f7ece9487d2ccd9b3ab291e663d11f93f2c08fa7f45ff1e243ba3d"
)
EXPECTED_KEY_ORDINAL_UNION_SHA256 = (
    "5ba4d5186ddb7ddb1868957f83af9d5224dbddaa619ecfedf1cdc51f7bc03763"
)
EXPECTED_R211_SHEET_ORIGIN_IDS_SHA256 = (
    "54d30278aba3b3383a6cfe8762c8f5dc6851e333f595fb0d7dadbf8bd127410f"
)
EXPECTED_EMPTY_ONLY_ORIGIN_IDS_SHA256 = (
    "d19114798c695281bd7f9e8edeeffec77a703ac9a893aace4419bb6a60b0a4a3"
)
EXPECTED_REGION_UNION_SHA256 = (
    "f6913be76b7fe9ab6bf8d16eab9228303101b9cd07de672dd025f6de69598b78"
)


class Round213Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round213Error(label)


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
    require(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1,
        f"single-link regular input:{path.name}",
    )
    require(0 < before.st_size <= maximum, f"bounded input:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
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
            f"stable open:{path.name}",
        )
        chunks: list[bytes] = []
        size = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            require(size <= maximum, f"bounded read:{path.name}")
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
            f"stable read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in output, f"duplicate JSON key:{key}")
        output[key] = value
    return output


def reject_noninteger(token: str) -> None:
    raise Round213Error(f"noninteger JSON number:{token}")


def validate_json_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON value type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(
                type(key) is str
                and "\x00" not in key
                and not any(0xD800 <= ord(char) <= 0xDFFF for char in key),
                f"JSON key:{path}",
            )
            validate_json_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_json_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require(
            "\x00" not in value
            and not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            f"JSON string:{path}",
        )


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(
        raw
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        f"JSON encoding:{label}",
    )
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique_pairs,
            parse_float=reject_noninteger,
            parse_constant=reject_noninteger,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Round213Error(f"JSON parse:{label}:{exc}") from exc
    validate_json_tree(value)
    require(type(value) is dict, f"JSON top object:{label}")
    require(
        raw == canonical_bytes(value) + b"\n",
        f"canonical JSON:{label}",
    )
    return value


def parse_manifest(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise Round213Error("manifest ASCII") from exc
    require(text.endswith("\n"), "manifest newline")
    entries: dict[str, str] = {}
    for line in text.splitlines():
        parts = line.split("  ", 1)
        require(len(parts) == 2, "manifest line")
        value, name = parts
        require(
            len(value) == 64
            and all(char in "0123456789abcdef" for char in value),
            f"manifest digest:{name}",
        )
        require(
            name not in entries
            and name not in {"", ".", ".."}
            and "/" not in name
            and "\\" not in name,
            f"manifest filename:{name}",
        )
        entries[name] = value
    return entries


def pin_package(prefix: str) -> dict[str, str]:
    manifest_name, manifest_sha256, entry_count = PACKAGE_MANIFESTS[prefix]
    manifest_raw = regular_bytes(HERE / manifest_name, 10_000)
    require(
        hashlib.sha256(manifest_raw).hexdigest() == manifest_sha256,
        f"manifest pin:{prefix}",
    )
    entries = parse_manifest(manifest_raw)
    require(len(entries) == entry_count, f"manifest entry count:{prefix}")
    observed = {
        name: hashlib.sha256(regular_bytes(HERE / name)).hexdigest()
        for name in entries
    }
    require(observed == entries, f"manifest replay:{prefix}")
    return entries


def load_manifest_json(
    entries: dict[str, str],
    name: str,
) -> dict[str, Any]:
    require(name in entries, f"manifest-bound JSON:{name}")
    raw = regular_bytes(HERE / name)
    require(
        hashlib.sha256(raw).hexdigest() == entries[name],
        f"JSON file pin:{name}",
    )
    return strict_json(raw, name)


def require_result_wrapper(
    document: dict[str, Any],
    expected_result_sha256: str,
    label: str,
) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["result_sha256"] == expected_result_sha256
        and digest(document["result"]) == expected_result_sha256,
        f"result wrapper:{label}",
    )
    return document["result"]


def audit_rows(
    ledger: dict[str, Any],
    *,
    id_key: str,
    count: int,
    label: str,
) -> tuple[list[dict[str, Any]], set[str]]:
    rows = ledger["rows"]
    identifiers: set[str] = set()
    require(
        type(rows) is list
        and len(rows) == count
        and ledger["row_count"] == count
        and ledger["rows_sha256"] == digest(rows),
        f"ledger summary:{label}",
    )
    for row in rows:
        identifier = row[id_key]
        payload = {
            key: value
            for key, value in row.items()
            if key != "row_sha256"
        }
        require(
            type(identifier) is str
            and identifier not in identifiers
            and set(row) == {*payload, "row_sha256"}
            and row["row_sha256"] == digest(payload),
            f"closed row:{label}",
        )
        identifiers.add(identifier)
    return rows, identifiers


def load_formal_packages() -> dict[str, dict[str, Any]]:
    package_entries = {
        prefix: pin_package(prefix) for prefix in PACKAGE_MANIFESTS
    }
    attachment182 = require_result_wrapper(
        load_manifest_json(
            package_entries[R182],
            f"{R182}_rows.json",
        ),
        EXPECTED_RESULT_DIGESTS["Round182_attachment"],
        "Round182 attachment",
    )
    require_result_wrapper(
        load_manifest_json(
            package_entries[R182],
            f"{R182}_verification.json",
        ),
        EXPECTED_RESULT_DIGESTS["Round182_verification"],
        "Round182 verification",
    )
    certificate204 = require_result_wrapper(
        load_manifest_json(
            package_entries[R204],
            f"{R204}_certificate.json",
        ),
        EXPECTED_RESULT_DIGESTS["Round204_certificate"],
        "Round204 certificate",
    )
    require_result_wrapper(
        load_manifest_json(
            package_entries[R204],
            f"{R204}_verification.json",
        ),
        EXPECTED_RESULT_DIGESTS["Round204_verification"],
        "Round204 verification",
    )
    certificate208 = require_result_wrapper(
        load_manifest_json(
            package_entries[R208],
            f"{R208}_certificate.json",
        ),
        EXPECTED_RESULT_DIGESTS["Round208_certificate"],
        "Round208 certificate",
    )
    require_result_wrapper(
        load_manifest_json(
            package_entries[R208],
            f"{R208}_verification.json",
        ),
        EXPECTED_RESULT_DIGESTS["Round208_verification"],
        "Round208 verification",
    )
    certificate211 = require_result_wrapper(
        load_manifest_json(
            package_entries[R211],
            f"{R211}_certificate.json",
        ),
        EXPECTED_RESULT_DIGESTS["Round211_certificate"],
        "Round211 certificate",
    )
    verification211 = load_manifest_json(
        package_entries[R211],
        f"{R211}_verification.json",
    )
    require(
        set(verification211)
        == {"schema", "verification", "verification_result_sha256"}
        and verification211["verification_result_sha256"]
        == EXPECTED_RESULT_DIGESTS["Round211_verification"]
        and digest(verification211["verification"])
        == EXPECTED_RESULT_DIGESTS["Round211_verification"],
        "Round211 verification wrapper",
    )
    return {
        "entries": package_entries,
        "r182": attachment182,
        "r204": certificate204,
        "r208": certificate208,
        "r211": certificate211,
    }


def build_result(producer_sha256: str) -> dict[str, Any]:
    packages = load_formal_packages()
    r182 = packages["r182"]
    r204 = packages["r204"]
    r208 = packages["r208"]
    r211 = packages["r211"]

    origin_schema = r182["row_column_schemas"]["origin_replacement_rows"]
    packed_origin_rows = r182["origin_replacement_rows"]
    origin_rows = [
        dict(zip(origin_schema, packed, strict=True))
        for packed in packed_origin_rows
    ]
    require(
        len(origin_rows) == 57_896
        and len({
            row["Round179_origin_row_id"] for row in origin_rows
        }) == 57_896,
        "Round182 origin registry",
    )
    residual182 = {
        row["Round179_origin_row_id"]: row
        for row in origin_rows
        if row["fully_geometrically_replaced_original_tube"] is False
    }
    require(len(residual182) == 8_332, "Round182 residual origin count")

    origin_rows204, origin_ids204 = audit_rows(
        r204["origin_local_completion_ledger"],
        id_key="origin_row_id",
        count=64,
        label="Round204 origin completion",
    )
    origin_rows208, origin_ids208 = audit_rows(
        r208["formal_origin_local_completion_ledger"],
        id_key="origin_row_id",
        count=8_268,
        label="Round208 origin completion",
    )
    origins204 = {row["origin_row_id"]: row for row in origin_rows204}
    origins208 = {row["origin_row_id"]: row for row in origin_rows208}
    require(
        not (origin_ids204 & origin_ids208)
        and origin_ids204 | origin_ids208 == set(residual182)
        and digest(sorted(origin_ids204)) == EXPECTED_R204_ORIGIN_IDS_SHA256
        and digest(sorted(origin_ids208)) == EXPECTED_R208_ORIGIN_IDS_SHA256
        and digest(sorted(residual182)) == EXPECTED_ORIGIN_UNION_SHA256,
        "exact residual-origin partition",
    )

    regions204, region_ids204 = audit_rows(
        r204["formal_local_open_3D_region_ledger"],
        id_key="region_row_id",
        count=736,
        label="Round204 strict 3D regions",
    )
    regions208, region_ids208 = audit_rows(
        r208["formal_local_open_3D_signature_ledger"],
        id_key="region_row_id",
        count=36_040,
        label="Round208 strict 3D regions",
    )
    require(
        not (region_ids204 & region_ids208)
        and len(region_ids204 | region_ids208) == 36_776
        and digest(sorted(region_ids204 | region_ids208))
        == EXPECTED_REGION_UNION_SHA256,
        "strict-open region disjoint union",
    )

    joins204, _ = audit_rows(
        r204["exact_key_local_join_ledger"],
        id_key="official_key_id",
        count=12,
        label="Round204 exact-key joins",
    )
    joins208, _ = audit_rows(
        r208["formal_exact_key_local_join_ledger"],
        id_key="official_key_id",
        count=24,
        label="Round208 exact-key joins",
    )
    ordinals204 = {
        row["official_key_ordinal"] for row in joins204
    }
    ordinals208 = {
        row["official_key_ordinal"] for row in joins208
    }
    require(
        len(ordinals204) == 12
        and len(ordinals208) == 24
        and not (ordinals204 & ordinals208)
        and len(ordinals204 | ordinals208) == 36
        and digest(sorted(ordinals204 | ordinals208))
        == EXPECTED_KEY_ORDINAL_UNION_SHA256,
        "local exact-key ordinal union",
    )

    sheet_rows, _ = audit_rows(
        r211["formal_2D_sheet_owner_ledger"],
        id_key="sheet_row_id",
        count=17_716,
        label="Round211 2D owner incidences",
    )
    curve_rows, _ = audit_rows(
        r211["formal_1D_curve_incidence_owner_ledger"],
        id_key="curve_row_id",
        count=20_456,
        label="Round211 1D owner incidences",
    )
    endpoint_rows, _ = audit_rows(
        r211["formal_0D_endpoint_incidence_owner_ledger"],
        id_key="endpoint_row_id",
        count=40_912,
        label="Round211 0D owner incidences",
    )
    sheet_origin: dict[str, str] = {}
    sheets_per_origin: Counter[str] = Counter()
    for row in sheet_rows:
        sheet_origin[row["sheet_row_id"]] = row["origin_row_id"]
        sheets_per_origin[row["origin_row_id"]] += 1
        require(
            row["local_dimensional_owner_materialized"] is True
            and row["formal_half_open_owner_credit"] == 1
            and row["component_deduplication_credit"] == 0
            and row["whole_origin_credit"] == 0
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            "Round211 sheet strict local credit",
        )
    curves_per_origin: Counter[str] = Counter()
    for row in curve_rows:
        require(row["sheet_row_id"] in sheet_origin, "curve-sheet join")
        curves_per_origin[sheet_origin[row["sheet_row_id"]]] += 1
    endpoints_per_origin: Counter[str] = Counter()
    for row in endpoint_rows:
        require(row["sheet_row_id"] in sheet_origin, "endpoint-sheet join")
        endpoints_per_origin[sheet_origin[row["sheet_row_id"]]] += 1
    sheet_origins = set(sheets_per_origin)
    empty_only_origins = origin_ids208 - sheet_origins
    require(
        sheet_origins <= origin_ids208
        and len(sheet_origins) == 8_264
        and len(empty_only_origins) == 4
        and digest(sorted(sheet_origins))
        == EXPECTED_R211_SHEET_ORIGIN_IDS_SHA256
        and digest(sorted(empty_only_origins))
        == EXPECTED_EMPTY_ONLY_ORIGIN_IDS_SHA256
        and sum(sheets_per_origin.values()) == 17_716
        and sum(curves_per_origin.values()) == 20_456
        and sum(endpoints_per_origin.values()) == 40_912,
        "Round211 origin incidence partition",
    )
    for origin_id in empty_only_origins:
        row = origins208[origin_id]
        require(
            row["leaf_classification_count"] == {"EMPTY": 9}
            and row["leaf_row_count"] == 9
            and row["strict_open_3D_signature_region_count"] == 9
            and sheets_per_origin[origin_id] == 0
            and curves_per_origin[origin_id] == 0
            and endpoints_per_origin[origin_id] == 0,
            f"empty-only origin:{origin_id}",
        )

    parents204 = {row["parent_id"] for row in origin_rows204}
    parents208 = {row["parent_id"] for row in origin_rows208}
    require(
        len(parents204) == 16
        and len(parents208) == 912
        and not (parents204 & parents208)
        and len(parents204 | parents208) == 928
        and digest(sorted(parents204 | parents208))
        == EXPECTED_PARENT_UNION_SHA256,
        "parent partition",
    )

    union_rows: list[dict[str, Any]] = []
    for origin_id in sorted(residual182):
        frozen = residual182[origin_id]
        if origin_id in origins204:
            local = origins204[origin_id]
            require(
                local["parent_id"] == frozen["parent_id"]
                and local[
                    "Round182_fully_geometrically_replaced_original_tube"
                ] is False
                and local["Round204_fully_locally_signature_replaced"] is True
                and local["all_dimensions_have_deterministic_half_open_lineage"]
                is True,
                f"Round204 origin binding:{origin_id}",
            )
            branch = "ROUND204_WALL_G"
            dimensional_status = (
                "ROUND204_COMPLETE_LOCAL_3D_2D_1D_0D_LINEAGE"
            )
            strict_regions = local["strict_open_3D_region_count"]
            sheet_count = (
                local["source_t0_2D_sheet_cell_count"]
                + local["target_graph_2D_sheet_cell_count"]
            )
            curve_count = len(local["incident_1D_stratum_row_ids"])
            endpoint_count = len(local["incident_0D_stratum_row_ids"])
            empty_only = False
        else:
            local = origins208[origin_id]
            require(
                local["parent_id"] == frozen["parent_id"]
                and local["all_leaves_have_direct_signature_bases"] is True
                and local[
                    "all_strict_open_3D_regions_have_formal_signatures"
                ] is True,
                f"Round208 origin binding:{origin_id}",
            )
            branch = "ROUND208_OUTGOING_W"
            strict_regions = local[
                "strict_open_3D_signature_region_count"
            ]
            sheet_count = sheets_per_origin[origin_id]
            curve_count = curves_per_origin[origin_id]
            endpoint_count = endpoints_per_origin[origin_id]
            empty_only = origin_id in empty_only_origins
            dimensional_status = (
                "ROUND208_EMPTY_ONLY_OPEN_3D__"
                "NO_FACTOR_SHEET_EXISTS_OR_IS_REQUIRED"
                if empty_only
                else
                "ROUND208_OPEN_3D_PLUS_ROUND211_LOCAL_INCIDENCE_OWNER_LINEAGE"
            )
        union_rows.append(closed_row({
            "origin_row_id": origin_id,
            "parent_id": frozen["parent_id"],
            "Round182_origin_record_sha256": digest(frozen),
            "Round182_fully_geometrically_replaced_original_tube": False,
            "partition_member": branch,
            "source_package_origin_row_sha256": local["row_sha256"],
            "local_dimensional_completion_status": dimensional_status,
            "strict_open_3D_region_count": strict_regions,
            "local_2D_sheet_or_sheet_incidence_count": sheet_count,
            "local_1D_stratum_or_curve_incidence_count": curve_count,
            "local_0D_stratum_or_endpoint_incidence_count": endpoint_count,
            "Round211_nonempty_sheet_origin":
                branch == "ROUND208_OUTGOING_W" and not empty_only,
            "Round208_EMPTY_only_origin_without_invented_sheet": empty_only,
            "all_required_local_dimensions_materialized_for_this_origin": True,
            "separate_incidences_deduplicated_as_physical_components": False,
            "formal_local_residual_origin_completion_credit": 1,
            "physical_component_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    require(
        len(union_rows) == 8_332
        and len({row["origin_row_id"] for row in union_rows}) == 8_332
        and Counter(
            row["partition_member"] for row in union_rows
        ) == {
            "ROUND204_WALL_G": 64,
            "ROUND208_OUTGOING_W": 8_268,
        }
        and sum(
            row["formal_local_residual_origin_completion_credit"]
            for row in union_rows
        ) == 8_332
        and all(
            row["physical_component_credit"] == 0
            and row["whole_origin_credit"] == 0
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0
            for row in union_rows
        ),
        "formal residual-origin union rows",
    )

    ordinal_rows = [
        closed_row({
            "official_key_ordinal": ordinal,
            "local_package": (
                "ROUND204_WALL_G"
                if ordinal in ordinals204
                else "ROUND208_OUTGOING_W"
            ),
            "local_join_materialized": True,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        })
        for ordinal in sorted(ordinals204 | ordinals208)
    ]

    scope204 = r204["formal_scope_contract"]
    sheets204 = r204["formal_2D_sheet_lineage"]
    scope208 = r208["formal_scope_contract"]
    scope211 = r211["formal_scope_and_conservation"]
    require(
        scope204["strict_open_3D_region_count"] == 736
        and scope204["tail_open_3D_region_count"] == 96
        and sheets204["source_sheet_row_count"] == 224
        and sheets204["target_sheet_row_count"] == 224
        and r204["formal_1D_boundary_and_intersection_lineage"]["row_count"]
        == 1_024
        and r204["formal_0D_endpoint_and_corner_lineage"]["row_count"] == 580
        and r204["tail_pair_signature_glue_ledger"]["row_count"] == 32
        and scope208["strict_open_3D_candidate_region_count"] == 36_040
        and scope211["2D_sheet_owner_row_count"] == 17_716
        and scope211["1D_curve_incidence_owner_row_count"] == 20_456
        and scope211["0D_endpoint_incidence_owner_row_count"] == 40_912,
        "separate dimensional census",
    )

    entries = packages["entries"]
    result = {
        "status": STATUS,
        "formal_input_binding": {
            "Round182_manifest_sha256": PACKAGE_MANIFESTS[R182][1],
            "Round182_manifest_entries":
                dict(sorted(entries[R182].items())),
            "Round182_attachment_result_sha256":
                EXPECTED_RESULT_DIGESTS["Round182_attachment"],
            "Round182_verification_result_sha256":
                EXPECTED_RESULT_DIGESTS["Round182_verification"],
            "Round204_manifest_sha256": PACKAGE_MANIFESTS[R204][1],
            "Round204_manifest_entries":
                dict(sorted(entries[R204].items())),
            "Round204_certificate_result_sha256":
                EXPECTED_RESULT_DIGESTS["Round204_certificate"],
            "Round204_verification_result_sha256":
                EXPECTED_RESULT_DIGESTS["Round204_verification"],
            "Round208_manifest_sha256": PACKAGE_MANIFESTS[R208][1],
            "Round208_manifest_entries":
                dict(sorted(entries[R208].items())),
            "Round208_certificate_result_sha256":
                EXPECTED_RESULT_DIGESTS["Round208_certificate"],
            "Round208_verification_result_sha256":
                EXPECTED_RESULT_DIGESTS["Round208_verification"],
            "Round211_manifest_sha256": PACKAGE_MANIFESTS[R211][1],
            "Round211_manifest_entries":
                dict(sorted(entries[R211].items())),
            "Round211_certificate_result_sha256":
                EXPECTED_RESULT_DIGESTS["Round211_certificate"],
            "Round211_verification_result_sha256":
                EXPECTED_RESULT_DIGESTS["Round211_verification"],
            "all_four_manifests_and_25_entries_replayed": True,
        },
        "formal_Round182_residual_origin_union_ledger": {
            "row_count": len(union_rows),
            "rows_sha256": digest(union_rows),
            "rows": union_rows,
            "formal_local_residual_origin_completion_credit": 8_332,
            "physical_component_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "exact_origin_and_parent_partition_proof": {
            "Round182_origin_registry_count": 57_896,
            "Round182_fully_replaced_origin_count": 49_564,
            "Round182_residual_origin_count": 8_332,
            "Round204_origin_count": 64,
            "Round204_origin_ids_sha256":
                digest(sorted(origin_ids204)),
            "Round208_origin_count": 8_268,
            "Round208_origin_ids_sha256":
                digest(sorted(origin_ids208)),
            "Round204_Round208_origin_intersection_count": 0,
            "Round204_Round208_origin_union_count": 8_332,
            "Round204_Round208_origin_union_sha256":
                digest(sorted(origin_ids204 | origin_ids208)),
            "union_equals_exact_Round182_residual_origin_registry": True,
            "Round204_parent_count": 16,
            "Round208_parent_count": 912,
            "parent_intersection_count": 0,
            "parent_union_count": 928,
            "parent_union_sha256":
                digest(sorted(parents204 | parents208)),
            "Round211_nonempty_sheet_origin_count": 8_264,
            "Round211_nonempty_sheet_origin_ids_sha256":
                digest(sorted(sheet_origins)),
            "Round208_EMPTY_only_origin_count": 4,
            "Round208_EMPTY_only_origin_ids":
                sorted(empty_only_origins),
            "Round208_EMPTY_only_origin_ids_sha256":
                digest(sorted(empty_only_origins)),
            "no_2D_sheet_fabricated_for_EMPTY_only_origins": True,
        },
        "separate_dimensional_census_without_cross_gauge_measure_sum": {
            "Round204": {
                "origin_count": 64,
                "strict_open_3D_region_count": 736,
                "tail_open_3D_region_count": 96,
                "source_2D_sheet_count": 224,
                "target_2D_sheet_count": 224,
                "one_D_stratum_count": 1_024,
                "zero_D_stratum_count": 580,
                "tail_signature_glue_count": 32,
                "coordinate_volume_gauge":
                    "ROUND204_WALL_G_LOCAL_REPLACEMENT",
                "input_and_output_coordinate_volume": "177/1600000",
            },
            "Round208": {
                "origin_count": 8_268,
                "strict_open_3D_region_count": 36_040,
                "coordinate_volume_gauge":
                    "ROUND208_OUTGOING_W_LOCAL_MATERIALIZATION",
                "input_and_output_coordinate_volume":
                    "861459/419430400000",
            },
            "Round211": {
                "nonempty_sheet_origin_count": 8_264,
                "EMPTY_only_origin_count": 4,
                "two_D_sheet_owner_incidence_count": 17_716,
                "one_D_curve_owner_incidence_count": 20_456,
                "zero_D_endpoint_owner_incidence_count": 40_912,
                "incidences_deduplicated_as_physical_components": False,
            },
            "strict_open_3D_region_disjoint_union_count": 36_776,
            "strict_open_3D_region_union_ids_sha256":
                digest(sorted(region_ids204 | region_ids208)),
            "coordinate_volume_cross_gauge_sum_performed": False,
            "coordinate_volume_union_claimed": False,
        },
        "formal_local_exact_key_ordinal_union": {
            "row_count": len(ordinal_rows),
            "rows_sha256": digest(ordinal_rows),
            "rows": ordinal_rows,
            "Round204_ordinal_count": 12,
            "Round204_ordinals": sorted(ordinals204),
            "Round208_ordinal_count": 24,
            "Round208_ordinals": sorted(ordinals208),
            "ordinal_intersection_count": 0,
            "ordinal_union_count": 36,
            "ordinal_union_sha256":
                digest(sorted(ordinals204 | ordinals208)),
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        },
        "formal_local_union_and_strict_nonpromotion": {
            "Round182_residual_origins_locally_dimensionally_completed":
                8_332,
            "physical_component_deduplication_complete": False,
            "physical_component_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "deduplicate the formal local 2D/1D/0D incidence ledgers into "
            "physical components and independently close complete global "
            "exact-key fibres before any whole-tube or source-G disposition"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "formal_input_files_modified": False,
        },
    }
    return result


def validate_output(path: Path) -> Path:
    require(
        not any(part == ".." for part in path.parts),
        "output parent alias",
    )
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "output exact directory",
    )
    require(
        absolute.name == OUTPUT.name
        or (
            absolute.name.startswith(".cm2_round213_")
            and absolute.name.endswith("_certificate.json")
        ),
        "output allowlist",
    )
    protected = {
        Path(__file__).resolve(),
        *((HERE / values[0]).resolve()
          for values in PACKAGE_MANIFESTS.values()),
    }
    require(
        absolute.resolve(strict=False) not in protected,
        "protected output",
    )
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "existing output type",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    absolute = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.",
        suffix=".tmp",
        dir=absolute.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, absolute)
        directory_descriptor = os.open(
            os.fspath(absolute.parent),
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
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
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
