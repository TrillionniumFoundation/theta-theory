#!/usr/bin/env python3
"""Formal source-G global exact-key occurrence exhaustion frontier.

This producer reconstructs all 116 Round179 observed exact-key ordinals and
joins their local 3D occurrence censuses to the accepted Round204, Round208,
Round211, and Round213 local packages.  It enumerates the first missing
lower-dimensional and physical-glue frontier.  It does not identify physical
components, exhaust a global exact-key fibre, or create a disposition.
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
PREFIX = "cm2_round216_source_g_global_key_occurrence_exhaustion_frontier"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = (
    "cm2.round216.source-g-global-key-occurrence-exhaustion-frontier.v1"
)
STATUS = (
    "CERTIFIED_FORMAL_SOURCE_G_GLOBAL_KEY_OCCURRENCE_EXHAUSTION_FRONTIER__"
    "NO_GLOBAL_FIBRE_OR_DISPOSITION"
)
MAX_INPUT_BYTES = 500 * 1024 * 1024

R179 = "cm2_round179_source_g_residual_tube_arrangement"
R182 = "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
R204 = "cm2_round204_source_g_wall_return_signature_local_replacement"
R208 = "cm2_round208_source_g_outgoing_direct_signature_materialization"
R211 = "cm2_round211_source_g_outgoing_half_open_owner_materialization"
R213 = "cm2_round213_source_g_round182_residual_dimensional_union"

PACKAGE_MANIFESTS = {
    R179: (
        f"{R179}_manifest.sha256",
        "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76",
        7,
    ),
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
    R213: (
        f"{R213}_manifest.sha256",
        "85fa3bb452c88e4c4aec12a3744fab1c206dd9ca7086ab64cee96448d24d9673",
        6,
    ),
}

EXPECTED_RESULTS = {
    "Round179_certificate":
        "0f57284c11c617349fe66877552c401f426efafbc75faa08948f099166e9cde3",
    "Round179_attachment":
        "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb",
    "Round179_verification":
        "ca2ec32d84edf55919a26f556fd8e9dfc39566ad876b0cb5537168fee2b28229",
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
    "Round213_certificate":
        "1b2e74eedc449e2d27b8e6c92fa8d6d4e3eae1021a0b581f8f799845e3d9d13a",
    "Round213_verification":
        "5e21201a1c8741fa0d33bd83d3e284ff927fcf6589e7666fcf865d74093eb5a1",
}

ROUND214_PROBE = (
    "cm2_round214_source_g_physical_component_join_dedup_feasibility_probe.py"
)
ROUND214_REPORT = (
    "cm2_round214_source_g_physical_component_join_dedup_spike_report.md"
)
ROUND214_PROBE_SHA256 = (
    "d074aa045637ce1bb31768fa551bdb73ceda6a58c760cafe3dbf92faa7c922fe"
)
ROUND214_REPORT_SHA256 = (
    "aa48c012fa8c57df89b2bea4123467fc2c74821a03525095976cb61c709fe952"
)
ROUND213_ERRATUM = (
    "cm2_round213_source_g_round182_residual_dimensional_union_"
    "report_erratum.md"
)
ROUND213_ERRATUM_SHA256 = (
    "a18c1641e739e01fa178fa0aafbc2956e58e27e0bf4ca087154bc47cf183a721"
)
ROUND213_ERRATUM_MANIFEST = (
    "cm2_round213_source_g_round182_residual_dimensional_union_"
    "report_erratum_manifest.sha256"
)
ROUND213_ERRATUM_MANIFEST_SHA256 = (
    "0a2d39ad8c80f5c39cd5e6b3d3917e40df6e12eaa5fcaa075fce089708b8ccc8"
)
LEGACY_PRETTY_JSON = {
    f"{R179}_certificate.json",
    f"{R179}_verification.json",
}

EXPECTED_ALL_KEYS_SHA256 = (
    "405ffd84f2a5a432d5dbbf2e0a1f1f3c4f8ed477f0408fd07e4d4c369ec27fdb"
)
EXPECTED_FULLY_REPLACED_KEYS_SHA256 = (
    "68e5124cc0e3ac64b34dd48c470553ca60ce9f9e53d159e5fd581a55786238db"
)
EXPECTED_RESIDUAL_KEYS_SHA256 = (
    "5ba4d5186ddb7ddb1868957f83af9d5224dbddaa619ecfedf1cdc51f7bc03763"
)
EXPECTED_CLASS_KEY_SHA256 = {
    "BOTH_FULLY_REPLACED_AND_RESIDUAL":
        "45d580bedb669875f90101d98013ba44da40e56aa6688f052dbccc1f8499efe4",
    "RESIDUAL_ONLY":
        "0e36044c42c8c6dfd072bda521f4d6a4f146b35c1d68cb88f7915dd43b588eb9",
    "FULLY_REPLACED_ONLY":
        "95868ce1cf24d57530143a73fdf95db8da3e39cad70197b09664cb9afacefa68",
    "RESOLVED_CHILD_ONLY":
        "5d1cf0b2165bbf8611cba5c3810a5dc1cfcbc5d5fb5faa7be23be312bd691a8b",
}


class Round216Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round216Error(label)


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
    raise Round216Error(f"noninteger JSON number:{token}")


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
        raise Round216Error(f"JSON parse:{label}:{exc}") from exc
    validate_json_tree(value)
    require(type(value) is dict, f"JSON top object:{label}")
    canonical = canonical_bytes(value) + b"\n"
    legacy_pretty = (
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        ).encode() + b"\n"
    )
    require(
        raw == canonical
        or (label in LEGACY_PRETTY_JSON and raw == legacy_pretty),
        f"canonical or pinned legacy-pretty JSON:{label}",
    )
    return value


def parse_manifest(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise Round216Error("manifest ASCII") from exc
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


def load_json(entries: dict[str, str], name: str) -> dict[str, Any]:
    require(name in entries, f"manifest-bound JSON:{name}")
    raw = regular_bytes(HERE / name)
    require(
        hashlib.sha256(raw).hexdigest() == entries[name],
        f"JSON file pin:{name}",
    )
    return strict_json(raw, name)


def result_wrapper(
    document: dict[str, Any],
    expected: str,
    label: str,
) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"}
        and document["result_sha256"] == expected
        and digest(document["result"]) == expected,
        f"result wrapper:{label}",
    )
    return document["result"]


def verification211_wrapper(
    document: dict[str, Any],
    expected: str,
) -> None:
    require(
        set(document)
        == {"schema", "verification", "verification_result_sha256"}
        and document["verification_result_sha256"] == expected
        and digest(document["verification"]) == expected,
        "Round211 verification wrapper",
    )


def audit_closed_rows(
    ledger: dict[str, Any],
    *,
    id_key: str,
    count: int,
    label: str,
) -> list[dict[str, Any]]:
    rows = ledger["rows"]
    require(
        type(rows) is list
        and len(rows) == count
        and ledger["row_count"] == count
        and ledger["rows_sha256"] == digest(rows),
        f"ledger summary:{label}",
    )
    identifiers: set[Any] = set()
    for row in rows:
        identifier = row[id_key]
        payload = {
            key: value for key, value in row.items()
            if key != "row_sha256"
        }
        require(
            identifier not in identifiers
            and set(row) == {*payload, "row_sha256"}
            and row["row_sha256"] == digest(payload),
            f"closed row:{label}",
        )
        identifiers.add(identifier)
    return rows


def classify(
    ordinal: int,
    fully_replaced: set[int],
    residual: set[int],
) -> str:
    if ordinal in fully_replaced and ordinal in residual:
        return "BOTH_FULLY_REPLACED_AND_RESIDUAL"
    if ordinal in residual:
        return "RESIDUAL_ONLY"
    if ordinal in fully_replaced:
        return "FULLY_REPLACED_ONLY"
    return "RESOLVED_CHILD_ONLY"


def build_result(producer_sha256: str) -> dict[str, Any]:
    entries = {
        prefix: pin_package(prefix) for prefix in PACKAGE_MANIFESTS
    }

    # Accepted verification wrappers are replayed before their data are used.
    result_wrapper(
        load_json(entries[R179], f"{R179}_certificate.json"),
        EXPECTED_RESULTS["Round179_certificate"],
        "Round179 certificate",
    )
    result_wrapper(
        load_json(entries[R179], f"{R179}_verification.json"),
        EXPECTED_RESULTS["Round179_verification"],
        "Round179 verification",
    )
    result_wrapper(
        load_json(entries[R182], f"{R182}_verification.json"),
        EXPECTED_RESULTS["Round182_verification"],
        "Round182 verification",
    )

    attachment179 = result_wrapper(
        load_json(entries[R179], f"{R179}_rows.json"),
        EXPECTED_RESULTS["Round179_attachment"],
        "Round179 attachment",
    )
    schemas179 = attachment179["row_column_schemas"]
    resolved_schema = schemas179["resolved_3d_child_rows"]
    resolved_index = {
        name: index for index, name in enumerate(resolved_schema)
    }
    resolved_rows = attachment179["resolved_3d_child_rows"]
    cluster_rows = attachment179["fully_replaced_key_cluster_rows"]
    table_census = attachment179["table_census_and_sha256"]
    require(
        len(resolved_rows) == 17_192
        and table_census["resolved_3d_child_rows"]["row_count"] == 17_192
        and table_census["resolved_3d_child_rows"]["rows_sha256"]
        == digest(resolved_rows)
        and len(cluster_rows) == 96
        and table_census["fully_replaced_key_cluster_rows"]["row_count"]
        == 96
        and table_census["fully_replaced_key_cluster_rows"]["rows_sha256"]
        == digest(cluster_rows),
        "Round179 table closures",
    )
    r179_counts: Counter[int] = Counter()
    key_metadata: dict[int, tuple[str, list[Any]]] = {}
    resolved_ids: set[str] = set()
    for packed in resolved_rows:
        row_id = packed[resolved_index["row_id"]]
        ordinal = packed[resolved_index["official_key_ordinal"]]
        metadata = (
            packed[resolved_index["official_key_id"]],
            packed[resolved_index["official_key_row"]],
        )
        require(
            type(row_id) is str
            and row_id not in resolved_ids
            and type(ordinal) is int
            and packed[resolved_index["ambient_dimension"]] == 3
            and packed[resolved_index["credit_kind"]]
            == "LOCAL_POSITIVE_3D_OCCURRENCE_ONLY"
            and packed[
                resolved_index["global_geometric_disposition_credit"]
            ] == 0,
            "Round179 resolved occurrence",
        )
        resolved_ids.add(row_id)
        if ordinal in key_metadata:
            require(
                key_metadata[ordinal] == metadata,
                "Round179 key metadata consistency",
            )
        else:
            key_metadata[ordinal] = metadata
        r179_counts[ordinal] += 1
    fully_replaced: set[int] = set()
    cluster_ids: set[str] = set()
    fully_replaced_origin_count = 0
    for packed in cluster_rows:
        cluster_id, ordinals, ordinals_sha, origin_count, credit = packed
        require(
            type(cluster_id) is str
            and cluster_id not in cluster_ids
            and ordinals_sha == digest(ordinals)
            and all(type(value) is int for value in ordinals)
            and credit == 0,
            "Round179 fully-replaced cluster",
        )
        cluster_ids.add(cluster_id)
        fully_replaced.update(ordinals)
        fully_replaced_origin_count += origin_count
    all_keys = set(r179_counts)
    require(
        len(resolved_ids) == 17_192
        and len(all_keys) == 116
        and sum(r179_counts.values()) == 17_192
        and digest(sorted(all_keys)) == EXPECTED_ALL_KEYS_SHA256
        and len(fully_replaced) == 96
        and fully_replaced <= all_keys
        and fully_replaced_origin_count == 4_116
        and digest(sorted(fully_replaced))
        == EXPECTED_FULLY_REPLACED_KEYS_SHA256,
        "Round179 key sets",
    )
    del attachment179, resolved_rows, cluster_rows

    r204 = result_wrapper(
        load_json(entries[R204], f"{R204}_certificate.json"),
        EXPECTED_RESULTS["Round204_certificate"],
        "Round204 certificate",
    )
    result_wrapper(
        load_json(entries[R204], f"{R204}_verification.json"),
        EXPECTED_RESULTS["Round204_verification"],
        "Round204 verification",
    )
    regions204 = audit_closed_rows(
        r204["formal_local_open_3D_region_ledger"],
        id_key="region_row_id",
        count=736,
        label="Round204 strict regions",
    )
    joins204 = audit_closed_rows(
        r204["exact_key_local_join_ledger"],
        id_key="official_key_ordinal",
        count=12,
        label="Round204 key joins",
    )
    r204_counts: Counter[int] = Counter()
    for row in regions204:
        ordinal = row["official_key_ordinal"]
        require(
            ordinal in all_keys
            and (
                row["official_key_id"],
                row["official_key_row"],
            ) == key_metadata[ordinal]
            and row["strict_open_region"] is True
            and row["formal_local_signature_credit"] == 1
            and row["global_exact_key_disposition_credit"] == 0,
            "Round204 strict-key join",
        )
        r204_counts[ordinal] += 1
    r204_tail: Counter[int] = Counter()
    for row in joins204:
        ordinal = row["official_key_ordinal"]
        require(
            ordinal in r204_counts
            and (
                row["official_key_id"],
                row["official_key_row"],
            ) == key_metadata[ordinal]
            and row["global_exact_key_fibre_exhausted"] is False
            and row["global_exact_key_disposition_credit"] == 0,
            "Round204 local join",
        )
        r204_tail[ordinal] = row["tail_region_occurrence_count"]
    keys204 = set(r204_counts)
    require(
        len(keys204) == 12
        and sum(r204_counts.values()) == 736
        and sum(r204_tail.values()) == 96
        and digest(sorted(keys204))
        == "b6a4be44c82676bbef4e07ce1125ab862b1b8dd794e06dd45394a2e2a87cf855",
        "Round204 key census",
    )
    scope204 = r204["formal_scope_contract"]
    r204_lower_dimensional_gauge = {
        "source_2D_sheet_count":
            r204["formal_2D_sheet_lineage"]["source_sheet_row_count"],
        "target_2D_sheet_count":
            r204["formal_2D_sheet_lineage"]["target_sheet_row_count"],
        "one_D_stratum_count":
            r204["formal_1D_boundary_and_intersection_lineage"]["row_count"],
        "zero_D_stratum_count":
            r204["formal_0D_endpoint_and_corner_lineage"]["row_count"],
        "tail_signature_glue_count":
            r204["tail_pair_signature_glue_ledger"]["row_count"],
    }
    require(
        scope204["strict_open_3D_region_count"] == 736
        and scope204["tail_open_3D_region_count"] == 96
        and r204_lower_dimensional_gauge == {
            "source_2D_sheet_count": 224,
            "target_2D_sheet_count": 224,
            "one_D_stratum_count": 1_024,
            "zero_D_stratum_count": 580,
            "tail_signature_glue_count": 32,
        },
        "Round204 separate dimensional gauge",
    )
    del r204, regions204, joins204

    r208 = result_wrapper(
        load_json(entries[R208], f"{R208}_certificate.json"),
        EXPECTED_RESULTS["Round208_certificate"],
        "Round208 certificate",
    )
    result_wrapper(
        load_json(entries[R208], f"{R208}_verification.json"),
        EXPECTED_RESULTS["Round208_verification"],
        "Round208 verification",
    )
    regions208 = audit_closed_rows(
        r208["formal_local_open_3D_signature_ledger"],
        id_key="region_row_id",
        count=36_040,
        label="Round208 strict regions",
    )
    joins208 = audit_closed_rows(
        r208["formal_exact_key_local_join_ledger"],
        id_key="official_key_ordinal",
        count=24,
        label="Round208 key joins",
    )
    r208_counts: Counter[int] = Counter()
    region_to_key: dict[str, int] = {}
    for row in regions208:
        signature = row["local_return_signature"]
        ordinal = signature["official_key_ordinal"]
        require(
            ordinal in all_keys
            and (
                signature["official_key_id"],
                signature["official_key_row"],
            ) == key_metadata[ordinal]
            and row["formal_local_open_3D_signature_credit"] == 1
            and row["global_exact_key_disposition_credit"] == 0
            and row["region_row_id"] not in region_to_key,
            "Round208 strict-key join",
        )
        region_to_key[row["region_row_id"]] = ordinal
        r208_counts[ordinal] += 1
    keys208 = set(r208_counts)
    require(
        len(keys208) == 24
        and sum(r208_counts.values()) == 36_040
        and len(region_to_key) == 36_040
        and digest(sorted(keys208))
        == "7b9394fd0da52793cb900cb82a26f7456d4097159b00f6fcf7a09bf14dc1f58c",
        "Round208 key census",
    )
    for row in joins208:
        require(
            row["official_key_ordinal"] in keys208
            and row["global_exact_key_fibre_exhausted"] is False
            and row["global_exact_key_disposition_credit"] == 0,
            "Round208 local join",
        )
    require(
        not (keys204 & keys208),
        "Round204/Round208 ordinal disjointness",
    )
    del r208, regions208, joins208

    r211 = result_wrapper(
        load_json(entries[R211], f"{R211}_certificate.json"),
        EXPECTED_RESULTS["Round211_certificate"],
        "Round211 certificate",
    )
    verification211_wrapper(
        load_json(entries[R211], f"{R211}_verification.json"),
        EXPECTED_RESULTS["Round211_verification"],
    )
    lower_counts: dict[str, Counter[int]] = {}
    for name, ledger_name, row_id_key, count in (
        ("two_D_sheet_owner_incidence_count",
         "formal_2D_sheet_owner_ledger", "sheet_row_id", 17_716),
        ("one_D_curve_owner_incidence_count",
         "formal_1D_curve_incidence_owner_ledger", "curve_row_id", 20_456),
        ("zero_D_endpoint_owner_incidence_count",
         "formal_0D_endpoint_incidence_owner_ledger",
         "endpoint_row_id", 40_912),
    ):
        rows = audit_closed_rows(
            r211[ledger_name],
            id_key=row_id_key,
            count=count,
            label=f"Round211 {name}",
        )
        key_counts: Counter[int] = Counter()
        for row in rows:
            owner = row["owner_region_row_id"]
            require(
                owner in region_to_key
                and row["local_dimensional_owner_materialized"] is True
                and row["formal_half_open_owner_credit"] == 1
                and row["component_deduplication_credit"] == 0
                and row["global_exact_key_disposition_credit"] == 0,
                f"Round211 owner-region key join:{name}",
            )
            key_counts[region_to_key[owner]] += 1
        require(
            set(key_counts) == keys208
            and sum(key_counts.values()) == count,
            f"Round211 keywise census:{name}",
        )
        lower_counts[name] = key_counts
    del r211, region_to_key

    r213 = result_wrapper(
        load_json(entries[R213], f"{R213}_certificate.json"),
        EXPECTED_RESULTS["Round213_certificate"],
        "Round213 certificate",
    )
    result_wrapper(
        load_json(entries[R213], f"{R213}_verification.json"),
        EXPECTED_RESULTS["Round213_verification"],
        "Round213 verification",
    )
    ordinal213 = r213["formal_local_exact_key_ordinal_union"]
    rows213 = audit_closed_rows(
        ordinal213,
        id_key="official_key_ordinal",
        count=36,
        label="Round213 residual ordinals",
    )
    residual = {row["official_key_ordinal"] for row in rows213}
    require(
        residual == keys204 | keys208
        and len(residual) == 36
        and ordinal213["Round204_ordinals"] == sorted(keys204)
        and ordinal213["Round208_ordinals"] == sorted(keys208)
        and ordinal213["ordinal_intersection_count"] == 0
        and ordinal213["global_exact_key_fibre_exhausted"] is False
        and ordinal213["global_exact_key_disposition_credit"] == 0
        and digest(sorted(residual)) == EXPECTED_RESIDUAL_KEYS_SHA256,
        "Round213 residual-key identity",
    )
    del r213, rows213

    classes: defaultdict[str, list[int]] = defaultdict(list)
    for ordinal in sorted(all_keys):
        classes[classify(ordinal, fully_replaced, residual)].append(ordinal)
    expected_class_counts = {
        "BOTH_FULLY_REPLACED_AND_RESIDUAL": 32,
        "RESIDUAL_ONLY": 4,
        "FULLY_REPLACED_ONLY": 64,
        "RESOLVED_CHILD_ONLY": 16,
    }
    require(
        {key: len(classes[key]) for key in expected_class_counts}
        == expected_class_counts
        and set().union(*(set(values) for values in classes.values()))
        == all_keys
        and sum(len(values) for values in classes.values()) == 116
        and all(
            digest(classes[key]) == EXPECTED_CLASS_KEY_SHA256[key]
            for key in expected_class_counts
        ),
        "116-key classification partition",
    )

    class_census: dict[str, dict[str, Any]] = {}
    expected_class_census = {
        "BOTH_FULLY_REPLACED_AND_RESIDUAL":
            (13_612, 736, 35_900, 50_248, 194, 6_206,
             17_664, 20_384, 40_768),
        "RESIDUAL_ONLY":
            (60, 0, 140, 200, 50, 50, 52, 72, 144),
        "FULLY_REPLACED_ONLY":
            (3_432, 0, 0, 3_432, 24, 102, 0, 0, 0),
        "RESOLVED_CHILD_ONLY":
            (88, 0, 0, 88, 3, 8, 0, 0, 0),
    }
    for class_name in expected_class_counts:
        ordinals = classes[class_name]
        totals = [
            r179_counts[value] + r204_counts[value] + r208_counts[value]
            for value in ordinals
        ]
        observed = (
            sum(r179_counts[value] for value in ordinals),
            sum(r204_counts[value] for value in ordinals),
            sum(r208_counts[value] for value in ordinals),
            sum(totals),
            min(totals),
            max(totals),
            sum(lower_counts[
                "two_D_sheet_owner_incidence_count"
            ][value] for value in ordinals),
            sum(lower_counts[
                "one_D_curve_owner_incidence_count"
            ][value] for value in ordinals),
            sum(lower_counts[
                "zero_D_endpoint_owner_incidence_count"
            ][value] for value in ordinals),
        )
        require(
            observed == expected_class_census[class_name],
            f"class census:{class_name}",
        )
        class_census[class_name] = {
            "key_count": len(ordinals),
            "key_ordinals_sha256": digest(ordinals),
            "Round179_resolved_child_occurrence_count": observed[0],
            "Round204_strict_local_region_occurrence_count": observed[1],
            "Round208_strict_local_region_occurrence_count": observed[2],
            "local_3D_occurrence_count": observed[3],
            "per_key_local_3D_occurrence_minimum": observed[4],
            "per_key_local_3D_occurrence_maximum": observed[5],
            "Round211_2D_sheet_owner_incidence_count": observed[6],
            "Round211_1D_curve_owner_incidence_count": observed[7],
            "Round211_0D_endpoint_owner_incidence_count": observed[8],
        }

    key_rows: list[dict[str, Any]] = []
    for ordinal in sorted(all_keys):
        class_name = classify(ordinal, fully_replaced, residual)
        if ordinal in keys204:
            lower_source = "ROUND204_SEPARATE_FORMAL_DIMENSIONAL_GAUGE"
        elif ordinal in keys208:
            lower_source = "ROUND211_KEYWISE_OWNER_INCIDENCE_LEDGER"
        else:
            lower_source = "NONE"
        local_3d = (
            r179_counts[ordinal]
            + r204_counts[ordinal]
            + r208_counts[ordinal]
        )
        key_id, key_row = key_metadata[ordinal]
        key_rows.append(closed_row({
            "official_key_ordinal": ordinal,
            "official_key_id": key_id,
            "official_key_row": key_row,
            "classification": class_name,
            "observed_in_Round179_resolved_children": True,
            "in_Round179_fully_replaced_cluster": ordinal in fully_replaced,
            "in_Round213_residual_36_key_union": ordinal in residual,
            "Round179_resolved_child_occurrence_count":
                r179_counts[ordinal],
            "Round204_strict_local_region_occurrence_count":
                r204_counts[ordinal],
            "Round204_tail_open_region_count_separately_tagged_nonadditive":
                r204_tail[ordinal],
            "Round208_strict_local_region_occurrence_count":
                r208_counts[ordinal],
            "local_3D_occurrence_count": local_3d,
            "local_3D_occurrence_is_not_a_physical_component_count": True,
            "residual_local_lower_dimensional_atlas_present":
                ordinal in residual,
            "local_lower_dimensional_atlas_source": lower_source,
            "Round204_lower_dimensional_rows_preserved_in_separate_gauge":
                ordinal in keys204,
            "Round204_lower_dimensional_rows_not_allocated_keywise":
                ordinal in keys204,
            "Round211_2D_sheet_owner_incidence_count":
                lower_counts[
                    "two_D_sheet_owner_incidence_count"
                ][ordinal],
            "Round211_1D_curve_owner_incidence_count":
                lower_counts[
                    "one_D_curve_owner_incidence_count"
                ][ordinal],
            "Round211_0D_endpoint_owner_incidence_count":
                lower_counts[
                    "zero_D_endpoint_owner_incidence_count"
                ][ordinal],
            "Round179_resolved_child_lower_dimensional_boundary_atlas_materialized":
                False,
            "cross_occurrence_physical_glue_materialized": False,
            "physical_component_credit": 0,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    require(
        len(key_rows) == 116
        and len({row["official_key_ordinal"] for row in key_rows}) == 116
        and sum(row["local_3D_occurrence_count"] for row in key_rows)
        == 53_968
        and sum(
            row["residual_local_lower_dimensional_atlas_present"]
            for row in key_rows
        ) == 36
        and all(
            row["global_exact_key_fibre_exhausted"] is False
            and row["global_exact_key_disposition_credit"] == 0
            and row["physical_component_credit"] == 0
            for row in key_rows
        ),
        "formal key frontier rows",
    )

    round214_probe_raw = regular_bytes(HERE / ROUND214_PROBE, 100_000)
    round214_report_raw = regular_bytes(HERE / ROUND214_REPORT, 100_000)
    require(
        hashlib.sha256(round214_probe_raw).hexdigest()
        == ROUND214_PROBE_SHA256
        and hashlib.sha256(round214_report_raw).hexdigest()
        == ROUND214_REPORT_SHA256,
        "optional Round214 read-only evidence pins",
    )
    erratum_manifest_raw = regular_bytes(
        HERE / ROUND213_ERRATUM_MANIFEST, 10_000
    )
    require(
        hashlib.sha256(erratum_manifest_raw).hexdigest()
        == ROUND213_ERRATUM_MANIFEST_SHA256,
        "Round213 immutable erratum manifest pin",
    )
    erratum_entries = parse_manifest(erratum_manifest_raw)
    require(
        erratum_entries == {
            ROUND213_ERRATUM: ROUND213_ERRATUM_SHA256
        }
        and hashlib.sha256(
            regular_bytes(HERE / ROUND213_ERRATUM, 10_000)
        ).hexdigest() == ROUND213_ERRATUM_SHA256,
        "Round213 immutable erratum replay",
    )
    boundary_blocker = {
        "Round179_resolved_child_occurrence_count_missing_explicit_lower_dimensional_boundary_atlas":
            17_192,
        "explicit_Round179_resolved_child_boundary_atlas_row_count": 0,
        "missing_boundary_cell_count":
            "NOT_ENUMERABLE_BEFORE_EXPLICIT_BOUNDARY_MATERIALIZATION",
    }
    physical_glue_blocker = {
        "positive_area_p_or_s_face_contact_count": 8_256,
        "exact_p_face_contact_count": 5_840,
        "partial_p_face_contact_count": 324,
        "exact_s_face_contact_count": 2_092,
        "explicit_p_or_s_internal_face_zero_trace_incidence_id_count_in_pinned_pre_Round217_boundary":
            0,
        "concurrent_Round217_not_pinned_or_included": True,
        "no_claim_about_post_boundary_Round217_trace_or_incidence_rows": True,
        "strict_Arb_active_factor_zero_witness_count": 4_648,
        "cross_occurrence_positive_area_contact_count": 9_200,
        "cross_occurrence_exact_t_face_contact_count": 2_704,
        "cross_occurrence_partial_t_face_contact_count": 320,
        "cross_occurrence_exact_p_face_contact_count": 5_840,
        "cross_occurrence_partial_p_face_contact_count": 324,
        "cross_occurrence_exact_s_face_contact_count": 12,
        "explicit_cross_occurrence_common_refinement_glue_row_count": 0,
        "cross_occurrence_exact_curve_carrier_candidate_count": 2_704,
        "cross_occurrence_exact_endpoint_carrier_candidate_count": 6_684,
        "same_occurrence_exact_t_face_safe_duplicate_join_count": 4_260,
        "unresolved_partial_positive_area_contact_count": 264,
        "unresolved_partial_p_face_contact_count": 144,
        "unresolved_partial_t_face_contact_count": 120,
    }
    obstruction = {
        "independent_blocker_count": 2,
        "Round179_resolved_child_lower_dimensional_boundary_blocker":
            boundary_blocker,
        "physical_glue_and_internal_face_trace_blocker":
            physical_glue_blocker,
        "blockers_are_logically_independent_and_both_required": True,
        "first_obstruction_order": [
            "ROUND179_RESOLVED_CHILD_LOWER_DIMENSIONAL_BOUNDARY_ATLAS",
            "P_OR_S_INTERNAL_FACE_ZERO_TRACE_INCIDENCE_IDS",
            "CROSS_OCCURRENCE_COMMON_REFINEMENT_GLUE_IDS",
            "PARTIAL_FACE_CURVE_RESTRICTIONS_AND_ENDPOINT_TO_INTERIOR_JOINS",
        ],
    }
    require(
        physical_glue_blocker["positive_area_p_or_s_face_contact_count"]
        == (
            physical_glue_blocker["exact_p_face_contact_count"]
            + physical_glue_blocker["partial_p_face_contact_count"]
            + physical_glue_blocker["exact_s_face_contact_count"]
        )
        and physical_glue_blocker[
            "cross_occurrence_positive_area_contact_count"
        ]
        == sum((
            physical_glue_blocker[
                "cross_occurrence_exact_t_face_contact_count"
            ],
            physical_glue_blocker[
                "cross_occurrence_partial_t_face_contact_count"
            ],
            physical_glue_blocker[
                "cross_occurrence_exact_p_face_contact_count"
            ],
            physical_glue_blocker[
                "cross_occurrence_partial_p_face_contact_count"
            ],
            physical_glue_blocker[
                "cross_occurrence_exact_s_face_contact_count"
            ],
        ))
        and physical_glue_blocker[
            "unresolved_partial_positive_area_contact_count"
        ]
        == (
            physical_glue_blocker[
                "unresolved_partial_p_face_contact_count"
            ]
            + physical_glue_blocker[
                "unresolved_partial_t_face_contact_count"
            ]
        ),
        "obstruction arithmetic",
    )

    formal_entries = sum(len(value) for value in entries.values())
    require(formal_entries == 38, "six-package entry census")
    result = {
        "status": STATUS,
        "formal_input_binding": {
            **{
                f"{prefix}_manifest_sha256":
                    PACKAGE_MANIFESTS[prefix][1]
                for prefix in PACKAGE_MANIFESTS
            },
            **{
                f"{prefix}_manifest_entries":
                    dict(sorted(entries[prefix].items()))
                for prefix in PACKAGE_MANIFESTS
            },
            "all_six_manifests_and_38_entries_replayed": True,
            "accepted_result_sha256": dict(sorted(EXPECTED_RESULTS.items())),
            "optional_Round214_probe_filename": ROUND214_PROBE,
            "optional_Round214_probe_sha256": ROUND214_PROBE_SHA256,
            "optional_Round214_report_filename": ROUND214_REPORT,
            "optional_Round214_report_sha256": ROUND214_REPORT_SHA256,
            "Round214_used_as_read_only_nonpromotional_obstruction_evidence":
                True,
            "Round213_immutable_report_erratum_manifest_filename":
                ROUND213_ERRATUM_MANIFEST,
            "Round213_immutable_report_erratum_manifest_sha256":
                ROUND213_ERRATUM_MANIFEST_SHA256,
            "Round213_immutable_report_erratum_filename": ROUND213_ERRATUM,
            "Round213_immutable_report_erratum_sha256":
                ROUND213_ERRATUM_SHA256,
            "Round213_frozen_six_artifact_manifest_unchanged": True,
        },
        "exact_116_key_set_and_classification": {
            "Round179_resolved_3D_child_row_count": 17_192,
            "Round179_observed_official_key_ordinal_count": 116,
            "Round179_observed_official_key_ordinals_sha256":
                digest(sorted(all_keys)),
            "Round179_fully_replaced_cluster_key_count": 96,
            "Round179_fully_replaced_cluster_keys_sha256":
                digest(sorted(fully_replaced)),
            "Round213_residual_key_count": 36,
            "Round213_residual_keys_sha256": digest(sorted(residual)),
            "fully_replaced_and_residual_intersection_count": 32,
            "classification_count": dict(sorted(expected_class_counts.items())),
            "classification_key_ordinals_sha256":
                dict(sorted(EXPECTED_CLASS_KEY_SHA256.items())),
            "classification_is_disjoint_complete_partition": True,
            "Round204_12_plus_Round208_Round211_24_equals_Round213_36":
                True,
        },
        "formal_key_occurrence_exhaustion_frontier_ledger": {
            "row_count": len(key_rows),
            "rows_sha256": digest(key_rows),
            "rows": key_rows,
            "global_exact_key_fibre_exhausted_count": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "local_3D_occurrence_census_without_physical_promotion": {
            "Round179_resolved_child_occurrence_count": 17_192,
            "Round204_strict_local_region_occurrence_count": 736,
            "Round204_tail_open_region_count_not_added_again_to_strict_total":
                96,
            "Round204_96_tail_regions_are_a_tagged_subset_of_the_736_strict_open_regions":
                True,
            "Round208_strict_local_region_occurrence_count": 36_040,
            "local_3D_occurrence_count": 53_968,
            "classification_census": dict(sorted(class_census.items())),
            "coordinate_volume_or_measure_sum_across_gauges_performed": False,
            "local_occurrence_count_promoted_to_physical_component_count":
                False,
            "local_occurrence_count_promoted_to_global_fibre_exhaustion":
                False,
        },
        "residual_lower_dimensional_coverage_frontier": {
            "residual_key_count_with_local_lower_dimensional_atlas": 36,
            "BOTH_class_key_count_with_local_lower_dimensional_atlas": 32,
            "RESIDUAL_ONLY_class_key_count_with_local_lower_dimensional_atlas":
                4,
            "nonresidual_key_count_without_Round204_Round211_atlas": 80,
            "FULLY_REPLACED_ONLY_without_local_atlas": 64,
            "RESOLVED_CHILD_ONLY_without_local_atlas": 16,
            "Round204_key_count_with_separate_formal_gauge": 12,
            "Round204_lower_dimensional_gauge":
                r204_lower_dimensional_gauge,
            "Round208_Round211_key_count_with_keywise_owner_incidences": 24,
            "Round211_2D_sheet_owner_incidence_count": 17_716,
            "Round211_1D_curve_owner_incidence_count": 20_456,
            "Round211_0D_endpoint_owner_incidence_count": 40_912,
            "Round211_owner_region_to_Round208_signature_key_join_complete":
                True,
            "local_lower_dimensional_materialization_does_not_exhaust_fibre":
                True,
        },
        "formal_missing_exhaustion_frontier": obstruction,
        "strict_nonpromotion": {
            "all_116_global_exact_key_fibres_exhausted": False,
            "global_exact_key_fibre_exhausted_count": 0,
            "physical_component_deduplication_complete": False,
            "physical_component_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "materialize all Round179 resolved-child lower-dimensional "
            "boundary atlases, p/s zero-trace incidences, cross-occurrence "
            "common-refinement glue, and partial-face restrictions before "
            "independent physical-component or global-fibre closure"
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
            absolute.name.startswith(".cm2_round216_")
            and absolute.name.endswith("_certificate.json")
        ),
        "output allowlist",
    )
    protected = {
        Path(__file__).resolve(),
        *((HERE / values[0]).resolve()
          for values in PACKAGE_MANIFESTS.values()),
        (HERE / ROUND214_PROBE).resolve(),
        (HERE / ROUND214_REPORT).resolve(),
        (HERE / ROUND213_ERRATUM_MANIFEST).resolve(),
        (HERE / ROUND213_ERRATUM).resolve(),
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
    source_sha256 = hashlib.sha256(regular_bytes(Path(__file__))).hexdigest()
    result = build_result(source_sha256)
    certificate = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical_bytes(certificate) + b"\n")
    print(certificate["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
