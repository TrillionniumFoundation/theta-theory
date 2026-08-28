#!/usr/bin/env python3
"""Independent fail-closed verifier for the formal Round213 local union.

The producer is pinned and parsed only as inert source bytes.  The complete
expected certificate is rebuilt from the four accepted package manifests and
their formal documents before the candidate certificate is opened.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round213_source_g_round182_residual_dimensional_union"
PRODUCER = HERE / f"{PREFIX}.py"
CERTIFICATE = HERE / f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
REPORT = f"{PREFIX}_report.md"
COLD = f"{PREFIX}_cold_replay.md"
MANIFEST = f"{PREFIX}_manifest.sha256"
SCHEMA = "cm2.round213.source-g-round182-residual-dimensional-union.v1"
VERIFICATION_SCHEMA = (
    "cm2.round213.source-g-round182-residual-dimensional-union."
    "verification.v1"
)
STATUS = (
    "CERTIFIED_LOCAL_SOURCE_G_ROUND182_RESIDUAL_DIMENSIONAL_UNION__"
    "NO_PHYSICAL_COMPONENT_WHOLE_TUBE_OR_GLOBAL_FIBRE_DISPOSITION"
)
MAX_INPUT_BYTES = 500 * 1024 * 1024

EXPECTED_PRODUCER_SHA256 = (
    "b90ea2c23d9296f2fe6f40d20d2b9655f98501014719e2b1d6ccbd647fde9b31"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "5ba025aa9e28d34fa913d51025ee90833632e9bca3d1f4ed4d0fa2a67efcbe05"
)
EXPECTED_CERTIFICATE_SIZE = 10_584_916
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "1b2e74eedc449e2d27b8e6c92fa8d6d4e3eae1021a0b581f8f799845e3d9d13a"
)

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


class Round213VerificationError(RuntimeError):
    pass


def ensure(condition: bool, label: str) -> None:
    if not condition:
        raise Round213VerificationError(label)


def encoded(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def object_sha256(value: Any) -> str:
    return hashlib.sha256(encoded(value)).hexdigest()


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = object_sha256(row)
    return row


def secure_read(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    metadata = path.lstat()
    ensure(
        stat.S_ISREG(metadata.st_mode)
        and not path.is_symlink()
        and metadata.st_nlink == 1
        and 0 < metadata.st_size <= maximum,
        f"secure input type/size:{path.name}",
    )
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        fingerprint = (
            opened.st_dev,
            opened.st_ino,
            opened.st_size,
            opened.st_mtime_ns,
        )
        ensure(
            fingerprint == (
                metadata.st_dev,
                metadata.st_ino,
                metadata.st_size,
                metadata.st_mtime_ns,
            ),
            f"stable input open:{path.name}",
        )
        output = bytearray()
        while len(output) <= maximum:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            output.extend(chunk)
        ensure(len(output) <= maximum, f"bounded input read:{path.name}")
        after = os.fstat(descriptor)
        ensure(
            fingerprint == (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            ),
            f"stable input read:{path.name}",
        )
        return bytes(output)
    finally:
        os.close(descriptor)


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        ensure(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def no_nonintegers(token: str) -> None:
    raise Round213VerificationError(f"noninteger JSON number:{token}")


def audit_json_types(value: Any, location: str = "$") -> None:
    ensure(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{location}",
    )
    if type(value) is dict:
        for key, child in value.items():
            ensure(
                type(key) is str
                and "\x00" not in key
                and not any(0xD800 <= ord(char) <= 0xDFFF for char in key),
                f"JSON key:{location}",
            )
            audit_json_types(child, f"{location}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            audit_json_types(child, f"{location}[{index}]")
    elif type(value) is str:
        ensure(
            "\x00" not in value
            and not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            f"JSON string:{location}",
        )


def decode_canonical(raw: bytes, label: str) -> dict[str, Any]:
    ensure(
        raw
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        f"JSON encoding:{label}",
    )
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=no_duplicate_pairs,
            parse_float=no_nonintegers,
            parse_constant=no_nonintegers,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Round213VerificationError(
            f"JSON decode:{label}:{exc}"
        ) from exc
    audit_json_types(value)
    ensure(type(value) is dict, f"JSON top object:{label}")
    ensure(raw == encoded(value) + b"\n", f"canonical JSON:{label}")
    return value


def manifest_map(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise Round213VerificationError("manifest ASCII") from exc
    ensure(text.endswith("\n"), "manifest trailing newline")
    result: dict[str, str] = {}
    for line in text.splitlines():
        pieces = line.split("  ", 1)
        ensure(len(pieces) == 2, "manifest line")
        value, name = pieces
        ensure(
            len(value) == 64
            and all(char in "0123456789abcdef" for char in value)
            and name not in result
            and name not in {"", ".", ".."}
            and "/" not in name
            and "\\" not in name,
            f"manifest entry:{name}",
        )
        result[name] = value
    return result


def replay_manifest(prefix: str) -> dict[str, str]:
    filename, expected_sha256, expected_count = PACKAGE_MANIFESTS[prefix]
    raw = secure_read(HERE / filename, 10_000)
    ensure(
        hashlib.sha256(raw).hexdigest() == expected_sha256,
        f"manifest hash:{prefix}",
    )
    entries = manifest_map(raw)
    ensure(len(entries) == expected_count, f"manifest count:{prefix}")
    for name, expected in entries.items():
        ensure(
            hashlib.sha256(secure_read(HERE / name)).hexdigest() == expected,
            f"manifest replay:{prefix}:{name}",
        )
    return entries


def manifest_document(
    entries: dict[str, str],
    filename: str,
) -> dict[str, Any]:
    ensure(filename in entries, f"manifest document:{filename}")
    raw = secure_read(HERE / filename)
    ensure(
        hashlib.sha256(raw).hexdigest() == entries[filename],
        f"document hash:{filename}",
    )
    return decode_canonical(raw, filename)


def result_payload(
    document: dict[str, Any],
    expected: str,
    label: str,
) -> dict[str, Any]:
    ensure(
        set(document) == {"schema", "result", "result_sha256"}
        and document["result_sha256"] == expected
        and object_sha256(document["result"]) == expected,
        f"formal wrapper:{label}",
    )
    return document["result"]


def accepted_inputs() -> dict[str, Any]:
    entries = {
        prefix: replay_manifest(prefix) for prefix in PACKAGE_MANIFESTS
    }
    r182 = result_payload(
        manifest_document(entries[R182], f"{R182}_rows.json"),
        EXPECTED_RESULT_DIGESTS["Round182_attachment"],
        "Round182 attachment",
    )
    result_payload(
        manifest_document(entries[R182], f"{R182}_verification.json"),
        EXPECTED_RESULT_DIGESTS["Round182_verification"],
        "Round182 verification",
    )
    r204 = result_payload(
        manifest_document(entries[R204], f"{R204}_certificate.json"),
        EXPECTED_RESULT_DIGESTS["Round204_certificate"],
        "Round204 certificate",
    )
    result_payload(
        manifest_document(entries[R204], f"{R204}_verification.json"),
        EXPECTED_RESULT_DIGESTS["Round204_verification"],
        "Round204 verification",
    )
    r208 = result_payload(
        manifest_document(entries[R208], f"{R208}_certificate.json"),
        EXPECTED_RESULT_DIGESTS["Round208_certificate"],
        "Round208 certificate",
    )
    result_payload(
        manifest_document(entries[R208], f"{R208}_verification.json"),
        EXPECTED_RESULT_DIGESTS["Round208_verification"],
        "Round208 verification",
    )
    r211 = result_payload(
        manifest_document(entries[R211], f"{R211}_certificate.json"),
        EXPECTED_RESULT_DIGESTS["Round211_certificate"],
        "Round211 certificate",
    )
    verification211 = manifest_document(
        entries[R211], f"{R211}_verification.json"
    )
    ensure(
        set(verification211)
        == {"schema", "verification", "verification_result_sha256"}
        and verification211["verification_result_sha256"]
        == EXPECTED_RESULT_DIGESTS["Round211_verification"]
        and object_sha256(verification211["verification"])
        == EXPECTED_RESULT_DIGESTS["Round211_verification"],
        "Round211 verification wrapper",
    )
    return {
        "entries": entries,
        "r182": r182,
        "r204": r204,
        "r208": r208,
        "r211": r211,
    }


def closed_ledger(
    ledger: dict[str, Any],
    *,
    identifier: str,
    expected_count: int,
    label: str,
) -> tuple[list[dict[str, Any]], set[str]]:
    rows = ledger["rows"]
    ensure(
        type(rows) is list
        and len(rows) == ledger["row_count"] == expected_count
        and object_sha256(rows) == ledger["rows_sha256"],
        f"ledger summary:{label}",
    )
    identifiers: set[str] = set()
    for row in rows:
        row_id = row[identifier]
        body = {
            key: value for key, value in row.items()
            if key != "row_sha256"
        }
        ensure(
            type(row_id) is str
            and row_id not in identifiers
            and set(row) == {*body, "row_sha256"}
            and row["row_sha256"] == object_sha256(body),
            f"closed formal row:{label}",
        )
        identifiers.add(row_id)
    return rows, identifiers


def reconstruct_expected(producer_sha256: str) -> dict[str, Any]:
    source = accepted_inputs()
    r182, r204, r208, r211 = (
        source["r182"],
        source["r204"],
        source["r208"],
        source["r211"],
    )

    columns = r182["row_column_schemas"]["origin_replacement_rows"]
    unpacked = [
        dict(zip(columns, packed, strict=True))
        for packed in r182["origin_replacement_rows"]
    ]
    ensure(
        len(unpacked) == 57_896
        and len({
            row["Round179_origin_row_id"] for row in unpacked
        }) == 57_896,
        "independent Round182 origin registry",
    )
    residual = {
        row["Round179_origin_row_id"]: row
        for row in unpacked
        if row["fully_geometrically_replaced_original_tube"] is False
    }
    ensure(len(residual) == 8_332, "independent residual registry")

    rows204, ids204 = closed_ledger(
        r204["origin_local_completion_ledger"],
        identifier="origin_row_id",
        expected_count=64,
        label="Round204 origins",
    )
    rows208, ids208 = closed_ledger(
        r208["formal_origin_local_completion_ledger"],
        identifier="origin_row_id",
        expected_count=8_268,
        label="Round208 origins",
    )
    by_origin204 = {row["origin_row_id"]: row for row in rows204}
    by_origin208 = {row["origin_row_id"]: row for row in rows208}
    ensure(
        ids204.isdisjoint(ids208)
        and ids204 | ids208 == set(residual)
        and object_sha256(sorted(ids204))
        == EXPECTED_R204_ORIGIN_IDS_SHA256
        and object_sha256(sorted(ids208))
        == EXPECTED_R208_ORIGIN_IDS_SHA256
        and object_sha256(sorted(residual))
        == EXPECTED_ORIGIN_UNION_SHA256,
        "independent exact origin partition",
    )

    region_rows204, region_ids204 = closed_ledger(
        r204["formal_local_open_3D_region_ledger"],
        identifier="region_row_id",
        expected_count=736,
        label="Round204 regions",
    )
    region_rows208, region_ids208 = closed_ledger(
        r208["formal_local_open_3D_signature_ledger"],
        identifier="region_row_id",
        expected_count=36_040,
        label="Round208 regions",
    )
    ensure(
        region_ids204.isdisjoint(region_ids208)
        and len(region_ids204 | region_ids208) == 36_776
        and object_sha256(sorted(region_ids204 | region_ids208))
        == EXPECTED_REGION_UNION_SHA256,
        "independent region partition",
    )

    key_rows204, _ = closed_ledger(
        r204["exact_key_local_join_ledger"],
        identifier="official_key_id",
        expected_count=12,
        label="Round204 key joins",
    )
    key_rows208, _ = closed_ledger(
        r208["formal_exact_key_local_join_ledger"],
        identifier="official_key_id",
        expected_count=24,
        label="Round208 key joins",
    )
    keys204 = {
        row["official_key_ordinal"] for row in key_rows204
    }
    keys208 = {
        row["official_key_ordinal"] for row in key_rows208
    }
    ensure(
        len(keys204) == 12
        and len(keys208) == 24
        and keys204.isdisjoint(keys208)
        and len(keys204 | keys208) == 36
        and object_sha256(sorted(keys204 | keys208))
        == EXPECTED_KEY_ORDINAL_UNION_SHA256,
        "independent key ordinal partition",
    )

    sheets, _ = closed_ledger(
        r211["formal_2D_sheet_owner_ledger"],
        identifier="sheet_row_id",
        expected_count=17_716,
        label="Round211 sheets",
    )
    curves, _ = closed_ledger(
        r211["formal_1D_curve_incidence_owner_ledger"],
        identifier="curve_row_id",
        expected_count=20_456,
        label="Round211 curves",
    )
    endpoints, _ = closed_ledger(
        r211["formal_0D_endpoint_incidence_owner_ledger"],
        identifier="endpoint_row_id",
        expected_count=40_912,
        label="Round211 endpoints",
    )
    sheet_to_origin: dict[str, str] = {}
    sheet_count: Counter[str] = Counter()
    for row in sheets:
        sheet_to_origin[row["sheet_row_id"]] = row["origin_row_id"]
        sheet_count[row["origin_row_id"]] += 1
        ensure(
            row["local_dimensional_owner_materialized"] is True
            and row["formal_half_open_owner_credit"] == 1
            and row["component_deduplication_credit"] == 0
            and row["whole_origin_credit"] == 0
            and row["whole_original_tube_credit"] == 0
            and row["global_exact_key_disposition_credit"] == 0,
            "independent sheet credit boundary",
        )
    curve_count: Counter[str] = Counter()
    for row in curves:
        ensure(row["sheet_row_id"] in sheet_to_origin, "curve sheet join")
        curve_count[sheet_to_origin[row["sheet_row_id"]]] += 1
    endpoint_count: Counter[str] = Counter()
    for row in endpoints:
        ensure(row["sheet_row_id"] in sheet_to_origin, "endpoint sheet join")
        endpoint_count[sheet_to_origin[row["sheet_row_id"]]] += 1
    nonempty_origins = set(sheet_count)
    empty_origins = ids208 - nonempty_origins
    ensure(
        nonempty_origins <= ids208
        and len(nonempty_origins) == 8_264
        and len(empty_origins) == 4
        and object_sha256(sorted(nonempty_origins))
        == EXPECTED_R211_SHEET_ORIGIN_IDS_SHA256
        and object_sha256(sorted(empty_origins))
        == EXPECTED_EMPTY_ONLY_ORIGIN_IDS_SHA256
        and sum(sheet_count.values()) == 17_716
        and sum(curve_count.values()) == 20_456
        and sum(endpoint_count.values()) == 40_912,
        "independent dimensional incidence census",
    )
    for origin_id in empty_origins:
        row = by_origin208[origin_id]
        ensure(
            row["leaf_classification_count"] == {"EMPTY": 9}
            and row["leaf_row_count"] == 9
            and row["strict_open_3D_signature_region_count"] == 9
            and sheet_count[origin_id] == 0
            and curve_count[origin_id] == 0
            and endpoint_count[origin_id] == 0,
            f"independent EMPTY-only proof:{origin_id}",
        )

    parent204 = {row["parent_id"] for row in rows204}
    parent208 = {row["parent_id"] for row in rows208}
    ensure(
        len(parent204) == 16
        and len(parent208) == 912
        and parent204.isdisjoint(parent208)
        and len(parent204 | parent208) == 928
        and object_sha256(sorted(parent204 | parent208))
        == EXPECTED_PARENT_UNION_SHA256,
        "independent parent partition",
    )

    union_rows: list[dict[str, Any]] = []
    for origin_id, frozen in sorted(residual.items()):
        if origin_id in by_origin204:
            formal = by_origin204[origin_id]
            ensure(
                formal["parent_id"] == frozen["parent_id"]
                and formal[
                    "Round182_fully_geometrically_replaced_original_tube"
                ] is False
                and formal["Round204_fully_locally_signature_replaced"]
                is True
                and formal[
                    "all_dimensions_have_deterministic_half_open_lineage"
                ] is True,
                f"independent Round204 binding:{origin_id}",
            )
            branch = "ROUND204_WALL_G"
            status = "ROUND204_COMPLETE_LOCAL_3D_2D_1D_0D_LINEAGE"
            strict_count = formal["strict_open_3D_region_count"]
            two_d = (
                formal["source_t0_2D_sheet_cell_count"]
                + formal["target_graph_2D_sheet_cell_count"]
            )
            one_d = len(formal["incident_1D_stratum_row_ids"])
            zero_d = len(formal["incident_0D_stratum_row_ids"])
            empty_only = False
        else:
            formal = by_origin208[origin_id]
            ensure(
                formal["parent_id"] == frozen["parent_id"]
                and formal["all_leaves_have_direct_signature_bases"] is True
                and formal[
                    "all_strict_open_3D_regions_have_formal_signatures"
                ] is True,
                f"independent Round208 binding:{origin_id}",
            )
            branch = "ROUND208_OUTGOING_W"
            strict_count = formal[
                "strict_open_3D_signature_region_count"
            ]
            two_d = sheet_count[origin_id]
            one_d = curve_count[origin_id]
            zero_d = endpoint_count[origin_id]
            empty_only = origin_id in empty_origins
            status = (
                "ROUND208_EMPTY_ONLY_OPEN_3D__"
                "NO_FACTOR_SHEET_EXISTS_OR_IS_REQUIRED"
                if empty_only
                else
                "ROUND208_OPEN_3D_PLUS_ROUND211_LOCAL_INCIDENCE_OWNER_LINEAGE"
            )
        union_rows.append(seal({
            "origin_row_id": origin_id,
            "parent_id": frozen["parent_id"],
            "Round182_origin_record_sha256": object_sha256(frozen),
            "Round182_fully_geometrically_replaced_original_tube": False,
            "partition_member": branch,
            "source_package_origin_row_sha256": formal["row_sha256"],
            "local_dimensional_completion_status": status,
            "strict_open_3D_region_count": strict_count,
            "local_2D_sheet_or_sheet_incidence_count": two_d,
            "local_1D_stratum_or_curve_incidence_count": one_d,
            "local_0D_stratum_or_endpoint_incidence_count": zero_d,
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
    ensure(
        len(union_rows) == 8_332
        and len({row["origin_row_id"] for row in union_rows}) == 8_332
        and Counter(
            row["partition_member"] for row in union_rows
        ) == {
            "ROUND204_WALL_G": 64,
            "ROUND208_OUTGOING_W": 8_268,
        },
        "independent formal union rows",
    )
    ordinal_rows = [
        seal({
            "official_key_ordinal": ordinal,
            "local_package": (
                "ROUND204_WALL_G"
                if ordinal in keys204
                else "ROUND208_OUTGOING_W"
            ),
            "local_join_materialized": True,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        })
        for ordinal in sorted(keys204 | keys208)
    ]

    scope204 = r204["formal_scope_contract"]
    lineage204 = r204["formal_2D_sheet_lineage"]
    scope208 = r208["formal_scope_contract"]
    scope211 = r211["formal_scope_and_conservation"]
    ensure(
        scope204["strict_open_3D_region_count"] == 736
        and scope204["tail_open_3D_region_count"] == 96
        and lineage204["source_sheet_row_count"] == 224
        and lineage204["target_sheet_row_count"] == 224
        and r204["formal_1D_boundary_and_intersection_lineage"]["row_count"]
        == 1_024
        and r204["formal_0D_endpoint_and_corner_lineage"]["row_count"] == 580
        and r204["tail_pair_signature_glue_ledger"]["row_count"] == 32
        and scope208["strict_open_3D_candidate_region_count"] == 36_040
        and scope211["2D_sheet_owner_row_count"] == 17_716
        and scope211["1D_curve_incidence_owner_row_count"] == 20_456
        and scope211["0D_endpoint_incidence_owner_row_count"] == 40_912,
        "independent separate census",
    )

    entries = source["entries"]
    return {
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
            "rows_sha256": object_sha256(union_rows),
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
            "Round204_origin_ids_sha256": object_sha256(sorted(ids204)),
            "Round208_origin_count": 8_268,
            "Round208_origin_ids_sha256": object_sha256(sorted(ids208)),
            "Round204_Round208_origin_intersection_count": 0,
            "Round204_Round208_origin_union_count": 8_332,
            "Round204_Round208_origin_union_sha256":
                object_sha256(sorted(ids204 | ids208)),
            "union_equals_exact_Round182_residual_origin_registry": True,
            "Round204_parent_count": 16,
            "Round208_parent_count": 912,
            "parent_intersection_count": 0,
            "parent_union_count": 928,
            "parent_union_sha256":
                object_sha256(sorted(parent204 | parent208)),
            "Round211_nonempty_sheet_origin_count": 8_264,
            "Round211_nonempty_sheet_origin_ids_sha256":
                object_sha256(sorted(nonempty_origins)),
            "Round208_EMPTY_only_origin_count": 4,
            "Round208_EMPTY_only_origin_ids": sorted(empty_origins),
            "Round208_EMPTY_only_origin_ids_sha256":
                object_sha256(sorted(empty_origins)),
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
                object_sha256(sorted(region_ids204 | region_ids208)),
            "coordinate_volume_cross_gauge_sum_performed": False,
            "coordinate_volume_union_claimed": False,
        },
        "formal_local_exact_key_ordinal_union": {
            "row_count": len(ordinal_rows),
            "rows_sha256": object_sha256(ordinal_rows),
            "rows": ordinal_rows,
            "Round204_ordinal_count": 12,
            "Round204_ordinals": sorted(keys204),
            "Round208_ordinal_count": 24,
            "Round208_ordinals": sorted(keys208),
            "ordinal_intersection_count": 0,
            "ordinal_union_count": 36,
            "ordinal_union_sha256":
                object_sha256(sorted(keys204 | keys208)),
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


def verify_sealed_rows(
    rows: list[dict[str, Any]],
    id_key: str,
    label: str,
) -> set[Any]:
    ids: set[Any] = set()
    for row in rows:
        identifier = row[id_key]
        body = {
            key: value for key, value in row.items()
            if key != "row_sha256"
        }
        ensure(
            identifier not in ids
            and set(row) == {*body, "row_sha256"}
            and row["row_sha256"] == object_sha256(body),
            f"candidate sealed row:{label}",
        )
        ids.add(identifier)
    return ids


def recursive_exact(value: Any, key: str, expected: Any) -> int:
    count = 0
    if type(value) is dict:
        for child_key, child in value.items():
            if child_key == key:
                ensure(
                    type(child) is type(expected) and child == expected,
                    f"recursive exact field:{key}",
                )
                count += 1
            count += recursive_exact(child, key, expected)
    elif type(value) is list:
        for child in value:
            count += recursive_exact(child, key, expected)
    return count


def audit_expected(result: dict[str, Any]) -> dict[str, int]:
    ensure(
        set(result) == {
            "status",
            "formal_input_binding",
            "formal_Round182_residual_origin_union_ledger",
            "exact_origin_and_parent_partition_proof",
            "separate_dimensional_census_without_cross_gauge_measure_sum",
            "formal_local_exact_key_ordinal_union",
            "formal_local_union_and_strict_nonpromotion",
            "next_core_gate",
            "provenance",
        }
        and result["status"] == STATUS,
        "expected top-level contract",
    )
    union = result["formal_Round182_residual_origin_union_ledger"]
    rows = union["rows"]
    origin_ids = verify_sealed_rows(rows, "origin_row_id", "origin union")
    ensure(
        len(rows) == union["row_count"] == len(origin_ids) == 8_332
        and union["rows_sha256"] == object_sha256(rows)
        and union["formal_local_residual_origin_completion_credit"] == 8_332
        and Counter(row["partition_member"] for row in rows)
        == {"ROUND204_WALL_G": 64, "ROUND208_OUTGOING_W": 8_268}
        and sum(
            row["Round208_EMPTY_only_origin_without_invented_sheet"]
            for row in rows
        ) == 4
        and all(
            row["all_required_local_dimensions_materialized_for_this_origin"]
            is True
            and row[
                "separate_incidences_deduplicated_as_physical_components"
            ] is False
            and row["formal_local_residual_origin_completion_credit"] == 1
            for row in rows
        ),
        "candidate origin union ledger",
    )
    partition = result["exact_origin_and_parent_partition_proof"]
    ensure(
        partition["Round182_residual_origin_count"] == 8_332
        and partition["Round204_origin_count"] == 64
        and partition["Round208_origin_count"] == 8_268
        and partition["Round204_Round208_origin_intersection_count"] == 0
        and partition["Round204_Round208_origin_union_count"] == 8_332
        and partition["Round204_Round208_origin_union_sha256"]
        == EXPECTED_ORIGIN_UNION_SHA256
        and partition[
            "union_equals_exact_Round182_residual_origin_registry"
        ] is True
        and partition["Round204_parent_count"] == 16
        and partition["Round208_parent_count"] == 912
        and partition["parent_intersection_count"] == 0
        and partition["parent_union_count"] == 928
        and partition["parent_union_sha256"] == EXPECTED_PARENT_UNION_SHA256
        and partition["Round211_nonempty_sheet_origin_count"] == 8_264
        and partition["Round208_EMPTY_only_origin_count"] == 4
        and partition["Round208_EMPTY_only_origin_ids_sha256"]
        == EXPECTED_EMPTY_ONLY_ORIGIN_IDS_SHA256
        and partition["no_2D_sheet_fabricated_for_EMPTY_only_origins"]
        is True,
        "candidate exact partition",
    )
    dimensional = result[
        "separate_dimensional_census_without_cross_gauge_measure_sum"
    ]
    ensure(
        dimensional["Round204"] == {
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
        }
        and dimensional["Round208"] == {
            "origin_count": 8_268,
            "strict_open_3D_region_count": 36_040,
            "coordinate_volume_gauge":
                "ROUND208_OUTGOING_W_LOCAL_MATERIALIZATION",
            "input_and_output_coordinate_volume":
                "861459/419430400000",
        }
        and dimensional["Round211"] == {
            "nonempty_sheet_origin_count": 8_264,
            "EMPTY_only_origin_count": 4,
            "two_D_sheet_owner_incidence_count": 17_716,
            "one_D_curve_owner_incidence_count": 20_456,
            "zero_D_endpoint_owner_incidence_count": 40_912,
            "incidences_deduplicated_as_physical_components": False,
        }
        and dimensional["strict_open_3D_region_disjoint_union_count"]
        == 36_776
        and dimensional["strict_open_3D_region_union_ids_sha256"]
        == EXPECTED_REGION_UNION_SHA256
        and dimensional["coordinate_volume_cross_gauge_sum_performed"]
        is False
        and dimensional["coordinate_volume_union_claimed"] is False,
        "candidate separate dimensional census",
    )
    key_union = result["formal_local_exact_key_ordinal_union"]
    ordinal_ids = verify_sealed_rows(
        key_union["rows"], "official_key_ordinal", "key ordinal union"
    )
    ensure(
        len(ordinal_ids) == key_union["row_count"] == 36
        and key_union["rows_sha256"] == object_sha256(key_union["rows"])
        and key_union["Round204_ordinal_count"] == 12
        and key_union["Round208_ordinal_count"] == 24
        and key_union["ordinal_intersection_count"] == 0
        and key_union["ordinal_union_count"] == 36
        and key_union["ordinal_union_sha256"]
        == EXPECTED_KEY_ORDINAL_UNION_SHA256
        and key_union["global_exact_key_fibre_exhausted"] is False
        and key_union["global_exact_key_disposition_credit"] == 0,
        "candidate local key ordinal union",
    )
    nonpromotion = result["formal_local_union_and_strict_nonpromotion"]
    ensure(
        nonpromotion[
            "Round182_residual_origins_locally_dimensionally_completed"
        ] == 8_332
        and nonpromotion["physical_component_deduplication_complete"] is False
        and nonpromotion["physical_component_credit"] == 0
        and nonpromotion["whole_origin_credit"] == 0
        and nonpromotion["whole_original_tube_credit"] == 0
        and nonpromotion["global_exact_key_fibre_exhausted"] is False
        and nonpromotion["global_exact_key_disposition_credit"] == 0
        and nonpromotion["source_G_global_exact_key_dispositions"]
        == "0/224580"
        and nonpromotion["D02"] == "BLOCKED"
        and nonpromotion["global_Gate5_fields"] == "10/18"
        and nonpromotion["global_complete_18_field_blocks"] == 0
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "candidate strict nonpromotion",
    )
    ensure(
        result["provenance"]["producer_sha256"]
        == EXPECTED_PRODUCER_SHA256
        and result["provenance"]["schema"] == SCHEMA
        and result["provenance"]["formal_input_files_modified"] is False,
        "candidate provenance",
    )
    counts = {
        "physical_component_credit_zero_occurrences": recursive_exact(
            result, "physical_component_credit", 0
        ),
        "whole_origin_credit_zero_occurrences": recursive_exact(
            result, "whole_origin_credit", 0
        ),
        "whole_original_tube_credit_zero_occurrences": recursive_exact(
            result, "whole_original_tube_credit", 0
        ),
        "global_disposition_credit_zero_occurrences": recursive_exact(
            result, "global_exact_key_disposition_credit", 0
        ),
        "global_fibre_exhaustion_false_occurrences": recursive_exact(
            result, "global_exact_key_fibre_exhausted", False
        ),
    }
    ensure(
        all(value > 0 for value in counts.values()),
        "recursive nonpromotion census",
    )
    return {
        "Round182_residual_origin_count": len(origin_ids),
        "Round204_origin_count": 64,
        "Round208_origin_count": 8_268,
        "Round211_nonempty_sheet_origin_count": 8_264,
        "Round208_EMPTY_only_origin_count": 4,
        "parent_union_count": 928,
        "strict_open_3D_region_union_count": 36_776,
        "local_exact_key_ordinal_union_count": len(ordinal_ids),
        **counts,
    }


def exact_directory_read(
    path: Path,
    maximum: int = MAX_INPUT_BYTES,
) -> bytes:
    ensure(
        not any(part == ".." for part in path.parts),
        "input parent alias",
    )
    absolute = Path(os.path.abspath(os.fspath(path)))
    ensure(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "input exact directory",
    )
    return secure_read(absolute, maximum)


def duplicate_literal_key_count(tree: ast.AST) -> int:
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: set[tuple[type, Any]] = set()
        for key in node.keys:
            if isinstance(key, ast.Constant):
                marker = (type(key.value), key.value)
                if marker in seen:
                    count += 1
                seen.add(marker)
    return count


def inert_boundary_audit() -> dict[str, Any]:
    producer_raw = exact_directory_read(PRODUCER, 5_000_000)
    ensure(
        hashlib.sha256(producer_raw).hexdigest()
        == EXPECTED_PRODUCER_SHA256,
        "inert producer pin",
    )
    verifier_raw = exact_directory_read(Path(__file__), 5_000_000)
    producer_tree = ast.parse(
        producer_raw.decode("utf-8", "strict"),
        filename=PRODUCER.name,
    )
    verifier_tree = ast.parse(
        verifier_raw.decode("utf-8", "strict"),
        filename=Path(__file__).name,
    )
    imports: list[str] = []
    for node in ast.walk(verifier_tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    ensure(
        PRODUCER.stem not in imports
        and not any(name.startswith(PREFIX) for name in imports)
        and PRODUCER.stem not in sys.modules,
        "producer import boundary",
    )
    dangerous = {
        node.func.id
        for node in ast.walk(verifier_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in {"exec", "eval", "compile"}
    }
    ensure(not dangerous, "dynamic execution boundary")

    def bodies(tree: ast.Module) -> dict[str, str]:
        output: dict[str, str] = {}
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                module = ast.Module(body=node.body, type_ignores=[])
                output[node.name] = hashlib.sha256(
                    ast.dump(
                        module,
                        annotate_fields=True,
                        include_attributes=False,
                    ).encode()
                ).hexdigest()
        return output

    producer_bodies = bodies(producer_tree)
    verifier_bodies = bodies(verifier_tree)
    reverse: defaultdict[str, list[str]] = defaultdict(list)
    for name, value in producer_bodies.items():
        reverse[value].append(name)
    overlap = sorted(
        (producer_name, verifier_name)
        for verifier_name, value in verifier_bodies.items()
        for producer_name in reverse.get(value, [])
    )
    producer_duplicates = duplicate_literal_key_count(producer_tree)
    verifier_duplicates = duplicate_literal_key_count(verifier_tree)
    ensure(
        producer_duplicates == verifier_duplicates == 0,
        "duplicate literal dictionary keys",
    )
    return {
        "producer_treated_as_inert_bytes": True,
        "producer_imported_or_executed": False,
        "producer_sha256": EXPECTED_PRODUCER_SHA256,
        "verifier_sha256": hashlib.sha256(verifier_raw).hexdigest(),
        "producer_AST_duplicate_literal_key_count": producer_duplicates,
        "verifier_AST_duplicate_literal_key_count": verifier_duplicates,
        "exact_AST_body_overlap_pair_count": len(overlap),
        "exact_AST_body_overlap_pairs": [
            {
                "producer_function": producer_name,
                "verifier_function": verifier_name,
            }
            for producer_name, verifier_name in overlap
        ],
        "implementation_diverse_second_derivation_claimed": False,
        "shared_generic_algorithm_risk_disclosed": True,
    }


def resign_union_row(result: dict[str, Any], index: int) -> None:
    ledger = result["formal_Round182_residual_origin_union_ledger"]
    row = ledger["rows"][index]
    row["row_sha256"] = object_sha256({
        key: value for key, value in row.items()
        if key != "row_sha256"
    })
    ledger["rows_sha256"] = object_sha256(ledger["rows"])


def resign_ordinal_row(result: dict[str, Any], index: int) -> None:
    ledger = result["formal_local_exact_key_ordinal_union"]
    row = ledger["rows"][index]
    row["row_sha256"] = object_sha256({
        key: value for key, value in row.items()
        if key != "row_sha256"
    })
    ledger["rows_sha256"] = object_sha256(ledger["rows"])


def assign(root: Any, path: tuple[Any, ...], value: Any) -> Any:
    cursor = root
    for component in path[:-1]:
        cursor = cursor[component]
    old = cursor[path[-1]]
    cursor[path[-1]] = value
    return old


def validate_candidate(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    ensure(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == SCHEMA
        and document["result_sha256"] == object_sha256(document["result"]),
        "candidate self-consistent wrapper",
    )
    audit_expected(document["result"])
    ensure(document["result"] == expected, "complete expected result equality")


def semantic_attack_suite(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    empty_index = next(
        index
        for index, row in enumerate(
            candidate["result"][
                "formal_Round182_residual_origin_union_ledger"
            ]["rows"]
        )
        if row["Round208_EMPTY_only_origin_without_invented_sheet"]
    )
    attacks: list[
        tuple[str, tuple[Any, ...], Any, tuple[str, int] | None]
    ] = [
        (
            "invented parent",
            ("result", "formal_Round182_residual_origin_union_ledger",
             "rows", 0, "parent_id"),
            "invented-parent",
            ("origin", 0),
        ),
        (
            "invented whole-tube credit",
            ("result", "formal_Round182_residual_origin_union_ledger",
             "rows", 0, "whole_original_tube_credit"),
            1,
            ("origin", 0),
        ),
        (
            "invented global disposition credit",
            ("result", "formal_Round182_residual_origin_union_ledger",
             "rows", 0, "global_exact_key_disposition_credit"),
            1,
            ("origin", 0),
        ),
        (
            "invented physical component credit",
            ("result", "formal_Round182_residual_origin_union_ledger",
             "rows", 0, "physical_component_credit"),
            1,
            ("origin", 0),
        ),
        (
            "origin overlap",
            ("result", "exact_origin_and_parent_partition_proof",
             "Round204_Round208_origin_intersection_count"),
            1,
            None,
        ),
        (
            "origin omission",
            ("result", "exact_origin_and_parent_partition_proof",
             "Round204_Round208_origin_union_count"),
            8_331,
            None,
        ),
        (
            "parent overlap",
            ("result", "exact_origin_and_parent_partition_proof",
             "parent_intersection_count"),
            1,
            None,
        ),
        (
            "fabricated EMPTY-only sheet",
            ("result", "formal_Round182_residual_origin_union_ledger",
             "rows", empty_index,
             "local_2D_sheet_or_sheet_incidence_count"),
            1,
            ("origin", empty_index),
        ),
        (
            "false EMPTY-only census",
            ("result", "exact_origin_and_parent_partition_proof",
             "Round208_EMPTY_only_origin_count"),
            3,
            None,
        ),
        (
            "key ordinal overlap",
            ("result", "formal_local_exact_key_ordinal_union",
             "ordinal_intersection_count"),
            1,
            None,
        ),
        (
            "invented global key exhaustion",
            ("result", "formal_local_exact_key_ordinal_union",
             "rows", 0, "global_exact_key_fibre_exhausted"),
            True,
            ("ordinal", 0),
        ),
        (
            "tampered official key ordinal",
            ("result", "formal_local_exact_key_ordinal_union",
             "rows", 0, "official_key_ordinal"),
            -1,
            ("ordinal", 0),
        ),
        (
            "tail regions falsely added to strict-open total",
            ("result",
             "separate_dimensional_census_without_cross_gauge_measure_sum",
             "strict_open_3D_region_disjoint_union_count"),
            36_872,
            None,
        ),
        (
            "forbidden cross-gauge volume sum",
            ("result",
             "separate_dimensional_census_without_cross_gauge_measure_sum",
             "coordinate_volume_cross_gauge_sum_performed"),
            True,
            None,
        ),
        (
            "false component deduplication",
            ("result", "formal_local_union_and_strict_nonpromotion",
             "physical_component_deduplication_complete"),
            True,
            None,
        ),
        (
            "false D02 promotion",
            ("result", "formal_local_union_and_strict_nonpromotion", "D02"),
            "OPEN",
            None,
        ),
        (
            "false CM2 promotion",
            ("result", "formal_local_union_and_strict_nonpromotion", "CM2"),
            "GO",
            None,
        ),
        (
            "producer provenance forgery",
            ("result", "provenance", "producer_sha256"),
            "0" * 64,
            None,
        ),
    ]
    rejected: list[str] = []
    for name, path, replacement, row_repair in attacks:
        original = assign(candidate, path, replacement)
        ensure(original != replacement, f"attack collision:{name}")
        try:
            if row_repair is not None:
                if row_repair[0] == "origin":
                    resign_union_row(candidate["result"], row_repair[1])
                else:
                    resign_ordinal_row(candidate["result"], row_repair[1])
            candidate["result_sha256"] = object_sha256(candidate["result"])
            ensure(
                candidate["result_sha256"]
                != EXPECTED_CERTIFICATE_RESULT_SHA256,
                f"attack changed result digest:{name}",
            )
            try:
                validate_candidate(candidate, expected)
            except Exception:
                rejected.append(name)
            else:
                raise Round213VerificationError(
                    f"semantic attack accepted:{name}"
                )
        finally:
            assign(candidate, path, original)
            if row_repair is not None:
                if row_repair[0] == "origin":
                    resign_union_row(candidate["result"], row_repair[1])
                else:
                    resign_ordinal_row(candidate["result"], row_repair[1])
            candidate["result_sha256"] = object_sha256(candidate["result"])

    union_ledger = candidate["result"][
        "formal_Round182_residual_origin_union_ledger"
    ]
    local_credit_key = "formal_local_residual_origin_completion_credit"
    transfer_targets = (
        ("steal local credit into whole-origin credit",
         "whole_origin_credit"),
        ("steal local credit into whole-original-tube credit",
         "whole_original_tube_credit"),
    )
    for name, target_key in transfer_targets:
        original_local_credit = union_ledger[local_credit_key]
        original_target_credit = union_ledger[target_key]
        union_ledger[local_credit_key] = 0
        union_ledger[target_key] = 8_332
        candidate["result_sha256"] = object_sha256(candidate["result"])
        try:
            ensure(
                candidate["result_sha256"]
                != EXPECTED_CERTIFICATE_RESULT_SHA256,
                f"attack changed result digest:{name}",
            )
            try:
                validate_candidate(candidate, expected)
            except Exception:
                rejected.append(name)
            else:
                raise Round213VerificationError(
                    f"semantic attack accepted:{name}"
                )
        finally:
            union_ledger[local_credit_key] = original_local_credit
            union_ledger[target_key] = original_target_credit
            candidate["result_sha256"] = object_sha256(
                candidate["result"]
            )

    rows = union_ledger["rows"]
    original_row_count = union_ledger["row_count"]
    original_rows_sha256 = union_ledger["rows_sha256"]
    original_local_credit = union_ledger[local_credit_key]

    omitted_row = rows.pop()
    union_ledger["row_count"] = len(rows)
    union_ledger["rows_sha256"] = object_sha256(rows)
    union_ledger[local_credit_key] = len(rows)
    candidate["result_sha256"] = object_sha256(candidate["result"])
    try:
        try:
            validate_candidate(candidate, expected)
        except Exception:
            rejected.append("omitted union row with recomputed ledger")
        else:
            raise Round213VerificationError(
                "semantic attack accepted:omitted union row"
            )
    finally:
        rows.append(omitted_row)
        union_ledger["row_count"] = original_row_count
        union_ledger["rows_sha256"] = original_rows_sha256
        union_ledger[local_credit_key] = original_local_credit
        candidate["result_sha256"] = object_sha256(candidate["result"])

    rows.append(copy.deepcopy(rows[0]))
    union_ledger["row_count"] = len(rows)
    union_ledger["rows_sha256"] = object_sha256(rows)
    union_ledger[local_credit_key] = len(rows)
    candidate["result_sha256"] = object_sha256(candidate["result"])
    try:
        try:
            validate_candidate(candidate, expected)
        except Exception:
            rejected.append("duplicated union row with recomputed ledger")
        else:
            raise Round213VerificationError(
                "semantic attack accepted:duplicated union row"
            )
    finally:
        rows.pop()
        union_ledger["row_count"] = original_row_count
        union_ledger["rows_sha256"] = original_rows_sha256
        union_ledger[local_credit_key] = original_local_credit
        candidate["result_sha256"] = object_sha256(candidate["result"])

    ensure(
        len(rejected) == len(attacks) + len(transfer_targets) + 2
        and candidate["result"] == expected
        and candidate["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "semantic attack restoration",
    )
    return {
        "attack_count": len(attacks) + len(transfer_targets) + 2,
        "rejected_count": len(rejected),
        "all_rejected": True,
        "attack_names": rejected,
        "every_attack_result_digest_recomputed": True,
        "affected_row_and_ledger_digests_recomputed": True,
    }


def reject_case(name: str, operation: Callable[[], Any]) -> str:
    try:
        operation()
    except Exception:
        return name
    raise Round213VerificationError(f"attack accepted:{name}")


def strict_json_attack_suite() -> dict[str, Any]:
    cases = [
        ("duplicate key", b'{"a":1,"a":2}'),
        ("float", b'{"a":1.0}'),
        ("NaN", b'{"a":NaN}'),
        ("Infinity", b'{"a":Infinity}'),
        ("negative Infinity", b'{"a":-Infinity}'),
        ("BOM", b'\xef\xbb\xbf{"a":1}\n'),
        ("NUL", b'{"a":"x\\u0000"}\x00\n'),
        ("invalid UTF-8", b'{"a":"\xff"}\n'),
        ("surrogate value", b'{"a":"\\ud800"}\n'),
        ("surrogate key", b'{"\\udfff":1}\n'),
        ("trailing JSON", b'{"a":1}{}\n'),
        ("top array", b'[]\n'),
        ("empty", b''),
        ("noncanonical whitespace", b'{ "a": 1 }\n'),
    ]
    rejected = [
        reject_case(
            name,
            lambda raw=raw, name=name: decode_canonical(
                raw, f"attack:{name}"
            ),
        )
        for name, raw in cases
    ]
    oversized = HERE / f".cm2_round213_{os.getpid()}_oversize.json"
    try:
        with oversized.open("wb") as handle:
            handle.truncate(65)
        rejected.append(reject_case(
            "oversize",
            lambda: exact_directory_read(oversized, 64),
        ))
    finally:
        if oversized.exists() or oversized.is_symlink():
            oversized.unlink()
    ensure(len(rejected) == 15, "JSON attack count")
    return {
        "attack_count": len(rejected),
        "rejected_count": len(rejected),
        "all_rejected": True,
        "attack_names": rejected,
    }


def protected_outputs() -> set[Path]:
    protected = {
        Path(__file__).resolve(),
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        (HERE / REPORT).resolve(),
        (HERE / COLD).resolve(),
        (HERE / MANIFEST).resolve(),
    }
    for prefix, values in PACKAGE_MANIFESTS.items():
        protected.add((HERE / values[0]).resolve())
        raw = secure_read(HERE / values[0], 10_000)
        protected.update(
            (HERE / name).resolve() for name in manifest_map(raw)
        )
    return protected


def validate_output(path: Path) -> Path:
    ensure(
        not any(part == ".." for part in path.parts),
        "output parent alias",
    )
    absolute = Path(os.path.abspath(os.fspath(path)))
    ensure(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "output exact directory",
    )
    ensure(
        absolute.name == OUTPUT.name
        or (
            absolute.name.startswith(".cm2_round213_")
            and absolute.name.endswith("_verification.json")
        ),
        "verification output allowlist",
    )
    ensure(
        absolute.resolve(strict=False) not in protected_outputs(),
        "protected output",
    )
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        ensure(
            stat.S_ISREG(metadata.st_mode)
            and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "existing output type",
        )
    return absolute


def atomic_write(path: Path, data: bytes) -> None:
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
        metadata = temporary.lstat()
        ensure(
            stat.S_ISREG(metadata.st_mode)
            and not temporary.is_symlink()
            and metadata.st_nlink == 1,
            "atomic temporary type",
        )
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


def path_type_output_attack_suite() -> dict[str, Any]:
    pid = os.getpid()
    scratch = Path(tempfile.mkdtemp(
        prefix=".cm2_round213_attack.",
        dir=HERE,
    ))
    source = scratch / "source"
    victim = scratch / "victim"
    source.write_bytes(b"SAFE\n")
    victim.write_bytes(b"SAFE\n")
    input_symlink = HERE / f".cm2_round213_{pid}_input_symlink"
    input_hardlink = HERE / f".cm2_round213_{pid}_input_hardlink"
    input_fifo = HERE / f".cm2_round213_{pid}_input_fifo"
    output_symlink = (
        HERE / f".cm2_round213_{pid}_symlink_verification.json"
    )
    output_hard_base = (
        HERE / f".cm2_round213_{pid}_base_verification.json"
    )
    output_hardlink = (
        HERE / f".cm2_round213_{pid}_hard_verification.json"
    )
    output_fifo = (
        HERE / f".cm2_round213_{pid}_fifo_verification.json"
    )
    outside = (
        HERE.parent / f".cm2_round213_{pid}_escape_verification.json"
    )
    parent_alias = HERE / f".cm2_round213_parent_alias_{pid}"
    safe_target = HERE / f".cm2_round213_{pid}_safe_verification.json"
    prepositioned = HERE / f".{safe_target.name}.prepositioned.tmp"
    created = [
        input_symlink,
        input_hardlink,
        input_fifo,
        output_symlink,
        output_hard_base,
        output_hardlink,
        output_fifo,
        outside,
        parent_alias,
        safe_target,
        prepositioned,
    ]
    rejected: list[str] = []
    try:
        input_symlink.symlink_to(source)
        os.link(source, input_hardlink)
        os.mkfifo(input_fifo)
        rejected.extend([
            reject_case(
                "input symlink",
                lambda: exact_directory_read(input_symlink, 64),
            ),
            reject_case(
                "input hardlink",
                lambda: exact_directory_read(input_hardlink, 64),
            ),
            reject_case(
                "input FIFO",
                lambda: exact_directory_read(input_fifo, 64),
            ),
            reject_case(
                "input directory",
                lambda: exact_directory_read(scratch, 64),
            ),
            reject_case(
                "input parent escape",
                lambda: exact_directory_read(HERE.parent / "outside", 64),
            ),
            reject_case(
                "input parent-dot-dot alias",
                lambda: exact_directory_read(
                    HERE / ".." / HERE.name / PRODUCER.name, 5_000_000
                ),
            ),
        ])
        parent_alias.symlink_to(HERE, target_is_directory=True)
        rejected.append(reject_case(
            "input symlink parent alias",
            lambda: exact_directory_read(
                parent_alias / PRODUCER.name, 5_000_000
            ),
        ))

        output_symlink.symlink_to(victim)
        output_hard_base.write_bytes(b"SAFE\n")
        os.link(output_hard_base, output_hardlink)
        os.mkfifo(output_fifo)
        rejected.extend([
            reject_case(
                "output symlink",
                lambda: atomic_write(output_symlink, b"x"),
            ),
            reject_case(
                "output hardlink",
                lambda: atomic_write(output_hardlink, b"x"),
            ),
            reject_case(
                "output FIFO",
                lambda: atomic_write(output_fifo, b"x"),
            ),
            reject_case(
                "output parent escape",
                lambda: atomic_write(outside, b"x"),
            ),
            reject_case(
                "nested output",
                lambda: atomic_write(
                    scratch
                    / f".cm2_round213_{pid}_nested_verification.json",
                    b"x",
                ),
            ),
            reject_case(
                "output symlink parent alias",
                lambda: atomic_write(
                    parent_alias
                    / f".cm2_round213_{pid}_alias_verification.json",
                    b"x",
                ),
            ),
            reject_case(
                "output parent-dot-dot alias",
                lambda: atomic_write(
                    HERE / ".." / HERE.name
                    / f".cm2_round213_{pid}_dotdot_verification.json",
                    b"x",
                ),
            ),
            reject_case(
                "unallowlisted output",
                lambda: atomic_write(
                    HERE / f"cm2_round213_{pid}_unlisted.json", b"x"
                ),
            ),
            reject_case(
                "certificate-shaped hidden output",
                lambda: atomic_write(
                    HERE / f".cm2_round213_{pid}_certificate.json", b"x"
                ),
            ),
            reject_case(
                "producer alias",
                lambda: atomic_write(PRODUCER, b"x"),
            ),
            reject_case(
                "certificate alias",
                lambda: atomic_write(CERTIFICATE, b"x"),
            ),
            reject_case(
                "verifier alias",
                lambda: atomic_write(Path(__file__), b"x"),
            ),
            reject_case(
                "existing output directory",
                lambda: atomic_write(scratch, b"x"),
            ),
        ])
        prepositioned.symlink_to(victim)
        atomic_write(safe_target, b"NEW\n")
        ensure(
            victim.read_bytes() == b"SAFE\n"
            and safe_target.read_bytes() == b"NEW\n"
            and prepositioned.is_symlink(),
            "prepositioned temporary untouched",
        )
        rejected.append("prepositioned temporary symlink not followed")
    finally:
        for path in created:
            if path.exists() or path.is_symlink():
                if path.is_dir() and not path.is_symlink():
                    shutil.rmtree(path)
                else:
                    path.unlink()
        if scratch.exists():
            shutil.rmtree(scratch)
    ensure(len(rejected) == 21, "path/type/output attack count")
    return {
        "attack_count": len(rejected),
        "rejected_or_safely_bypassed_count": len(rejected),
        "all_rejected_or_safely_bypassed": True,
        "attack_names": rejected,
        "protected_files_modified": False,
        "prepositioned_temporary_symlink_not_followed": True,
    }


def load_candidate() -> tuple[dict[str, Any], bytes]:
    raw = exact_directory_read(
        CERTIFICATE, EXPECTED_CERTIFICATE_SIZE
    )
    ensure(
        len(raw) == EXPECTED_CERTIFICATE_SIZE
        and hashlib.sha256(raw).hexdigest()
        == EXPECTED_CERTIFICATE_SHA256,
        "candidate byte pin",
    )
    return decode_canonical(raw, CERTIFICATE.name), raw


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--expect-result")
    arguments = parser.parse_args()

    boundary = inert_boundary_audit()
    expected_result = reconstruct_expected(EXPECTED_PRODUCER_SHA256)
    expected_result_sha256 = object_sha256(expected_result)
    ensure(
        expected_result_sha256 == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "independent expected result digest",
    )
    census = audit_expected(expected_result)

    # The candidate is opened only after full independent reconstruction.
    candidate, candidate_raw = load_candidate()
    expected_document = {
        "schema": SCHEMA,
        "result": expected_result,
        "result_sha256": expected_result_sha256,
    }
    validate_candidate(candidate, expected_result)
    expected_raw = encoded(expected_document) + b"\n"
    ensure(
        candidate == expected_document
        and candidate_raw == expected_raw
        and hashlib.sha256(expected_raw).hexdigest()
        == EXPECTED_CERTIFICATE_SHA256,
        "full expected object and canonical-byte equality",
    )
    del candidate_raw, expected_raw

    semantic_attacks = semantic_attack_suite(candidate, expected_result)
    json_attacks = strict_json_attack_suite()
    path_attacks = path_type_output_attack_suite()
    ensure(
        PRODUCER.stem not in sys.modules,
        "producer never imported or executed",
    )

    verification_result = {
        "status": "PASS_PARTIAL_FORMAL_ROUND213",
        "verdict": "PASS",
        "verifier_filename": Path(__file__).name,
        "verifier_sha256": boundary["verifier_sha256"],
        "producer_filename": PRODUCER.name,
        "producer_sha256": EXPECTED_PRODUCER_SHA256,
        "certificate_filename": CERTIFICATE.name,
        "certificate_file_sha256": EXPECTED_CERTIFICATE_SHA256,
        "certificate_size_bytes": EXPECTED_CERTIFICATE_SIZE,
        "certificate_result_sha256":
            EXPECTED_CERTIFICATE_RESULT_SHA256,
        "reconstructed_result_sha256": expected_result_sha256,
        "complete_expected_result_rebuilt_before_candidate_load": True,
        "full_expected_python_object_equality": True,
        "full_expected_canonical_byte_equality": True,
        "verified_census": census,
        "verified_set_identities": {
            "Round204_Round208_origin_intersection_count": 0,
            "Round204_Round208_origin_union_count": 8_332,
            "origin_union_sha256": EXPECTED_ORIGIN_UNION_SHA256,
            "union_equals_Round182_residual_registry": True,
            "parent_intersection_count": 0,
            "parent_union_count": 928,
            "parent_union_sha256": EXPECTED_PARENT_UNION_SHA256,
            "local_key_ordinal_intersection_count": 0,
            "local_key_ordinal_union_count": 36,
            "local_key_ordinal_union_sha256":
                EXPECTED_KEY_ORDINAL_UNION_SHA256,
        },
        "strict_nonpromotion": {
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
        "independence_contract": {
            **boundary,
            "all_four_manifests_and_25_entries_replayed": True,
            "candidate_loaded_only_after_expected_rebuilt": True,
            "implementation_diverse_second_derivation_claimed": False,
        },
        "semantic_resigned_attack_suite": semantic_attacks,
        "strict_JSON_and_oversize_attack_suite": json_attacks,
        "path_type_and_output_attack_suite": path_attacks,
        "output_safety": {
            "strict_verification_only_allowlist": True,
            "parent_aliases_rejected": True,
            "single_link_regular_existing_output_required": True,
            "unpredictable_same_directory_temporary": True,
            "file_fsync_before_replace": True,
            "parent_directory_fsync_after_replace": True,
        },
    }
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "result": verification_result,
        "result_sha256": object_sha256(verification_result),
    }
    if arguments.expect_result is not None:
        ensure(
            verification["result_sha256"] == arguments.expect_result,
            "expected verification result",
        )
    atomic_write(arguments.output, encoded(verification) + b"\n")
    print(verification["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
