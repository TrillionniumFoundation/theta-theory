#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round216 source-G frontier.

The producer is parsed only as pinned inert source.  The complete expected
certificate is rebuilt from six accepted manifests plus the immutable
Round213 report erratum before candidate bytes are opened.
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
PREFIX = "cm2_round216_source_g_global_key_occurrence_exhaustion_frontier"
PRODUCER = HERE / f"{PREFIX}.py"
CERTIFICATE = HERE / f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
REPORT = HERE / f"{PREFIX}_report.md"
COLD = HERE / f"{PREFIX}_cold_replay.md"
MANIFEST = HERE / f"{PREFIX}_manifest.sha256"
SCHEMA = (
    "cm2.round216.source-g-global-key-occurrence-exhaustion-frontier.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round216.source-g-global-key-occurrence-exhaustion-frontier."
    "verification.v1"
)
STATUS = (
    "CERTIFIED_FORMAL_SOURCE_G_GLOBAL_KEY_OCCURRENCE_EXHAUSTION_FRONTIER__"
    "NO_GLOBAL_FIBRE_OR_DISPOSITION"
)
MAX_INPUT_BYTES = 500 * 1024 * 1024

EXPECTED_PRODUCER_SHA256 = (
    "9da9d11ec0aa16e8dcbd22c0add51f373194008afa507da0432d3fee417c68fa"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "fa4cfb3b209518308c61ccdfa95834dd8e6899e6232fc40a569cbab4d6ecbe34"
)
EXPECTED_CERTIFICATE_SIZE = 174_708
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "267a4b9aaaab6a576e1c1866cc2fa0b9dc9bf4fc6a3b08a210ed3821e45dd658"
)

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
CLASS_KEY_SHA256 = {
    "BOTH_FULLY_REPLACED_AND_RESIDUAL":
        "45d580bedb669875f90101d98013ba44da40e56aa6688f052dbccc1f8499efe4",
    "RESIDUAL_ONLY":
        "0e36044c42c8c6dfd072bda521f4d6a4f146b35c1d68cb88f7915dd43b588eb9",
    "FULLY_REPLACED_ONLY":
        "95868ce1cf24d57530143a73fdf95db8da3e39cad70197b09664cb9afacefa68",
    "RESOLVED_CHILD_ONLY":
        "5d1cf0b2165bbf8611cba5c3810a5dc1cfcbc5d5fb5faa7be23be312bd691a8b",
}


class Round216VerificationError(RuntimeError):
    pass


def ensure(condition: bool, label: str) -> None:
    if not condition:
        raise Round216VerificationError(label)


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


def close(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = object_sha256(row)
    return row


def exact_read(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    ensure(
        not any(part == ".." for part in path.parts),
        "input parent alias",
    )
    path = Path(os.path.abspath(os.fspath(path)))
    ensure(
        path.parent == HERE and path.parent.resolve() == HERE,
        "input exact directory",
    )
    before = path.lstat()
    ensure(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1,
        f"single-link regular input:{path.name}",
    )
    ensure(0 < before.st_size <= maximum, f"bounded input:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        ensure(
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
        total = 0
        while True:
            block = os.read(descriptor, 1024 * 1024)
            if not block:
                break
            total += len(block)
            ensure(total <= maximum, f"bounded read:{path.name}")
            chunks.append(block)
        after = os.fstat(descriptor)
        ensure(
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


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        ensure(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_number(token: str) -> None:
    raise Round216VerificationError(f"noninteger JSON number:{token}")


def audit_tree(value: Any, path: str = "$") -> None:
    ensure(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            ensure(
                type(key) is str
                and "\x00" not in key
                and not any(0xD800 <= ord(char) <= 0xDFFF for char in key),
                f"JSON key:{path}",
            )
            audit_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            audit_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        ensure(
            "\x00" not in value
            and not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            f"JSON string:{path}",
        )


def decode(
    raw: bytes,
    label: str,
    *,
    allow_legacy: bool = False,
    maximum: int = MAX_INPUT_BYTES,
) -> dict[str, Any]:
    ensure(
        raw
        and len(raw) <= maximum
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        f"JSON encoding:{label}",
    )
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique_object,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Round216VerificationError(
            f"JSON parse:{label}:{exc}"
        ) from exc
    audit_tree(value)
    ensure(type(value) is dict, f"JSON top object:{label}")
    compact = encoded(value) + b"\n"
    pretty = json.dumps(
        value,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ).encode() + b"\n"
    ensure(
        raw == compact
        or (allow_legacy and label in LEGACY_PRETTY_JSON and raw == pretty),
        f"canonical JSON:{label}",
    )
    return value


def parse_manifest(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise Round216VerificationError("manifest ASCII") from exc
    ensure(text.endswith("\n"), "manifest newline")
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


def replay_packages() -> dict[str, dict[str, str]]:
    packages: dict[str, dict[str, str]] = {}
    for prefix, (manifest_name, manifest_sha, count) in (
        PACKAGE_MANIFESTS.items()
    ):
        raw = exact_read(HERE / manifest_name, 10_000)
        ensure(
            hashlib.sha256(raw).hexdigest() == manifest_sha,
            f"manifest pin:{prefix}",
        )
        entries = parse_manifest(raw)
        ensure(len(entries) == count, f"manifest count:{prefix}")
        for name, expected in entries.items():
            ensure(
                hashlib.sha256(exact_read(HERE / name)).hexdigest()
                == expected,
                f"manifest entry replay:{name}",
            )
        packages[prefix] = entries
    ensure(
        sum(len(value) for value in packages.values()) == 38,
        "six manifests and 38 entries",
    )
    return packages


def package_json(
    entries: dict[str, str],
    filename: str,
) -> dict[str, Any]:
    ensure(filename in entries, f"manifest JSON:{filename}")
    raw = exact_read(HERE / filename)
    ensure(
        hashlib.sha256(raw).hexdigest() == entries[filename],
        f"file pin:{filename}",
    )
    return decode(
        raw,
        filename,
        allow_legacy=filename in LEGACY_PRETTY_JSON,
    )


def unwrap(
    document: dict[str, Any],
    expected_sha: str,
    label: str,
) -> dict[str, Any]:
    ensure(
        set(document) == {"schema", "result", "result_sha256"}
        and document["result_sha256"] == expected_sha
        and object_sha256(document["result"]) == expected_sha,
        f"wrapper:{label}",
    )
    return document["result"]


def audit_ledger(
    ledger: dict[str, Any],
    id_key: str,
    count: int,
    label: str,
) -> list[dict[str, Any]]:
    rows = ledger["rows"]
    ensure(
        len(rows) == count
        and ledger["row_count"] == count
        and ledger["rows_sha256"] == object_sha256(rows),
        f"ledger:{label}",
    )
    seen: set[Any] = set()
    for row in rows:
        payload = {
            key: value for key, value in row.items()
            if key != "row_sha256"
        }
        ensure(
            row[id_key] not in seen
            and row["row_sha256"] == object_sha256(payload),
            f"row:{label}",
        )
        seen.add(row[id_key])
    return rows


def category(
    ordinal: int,
    fully: set[int],
    residual: set[int],
) -> str:
    if ordinal in fully and ordinal in residual:
        return "BOTH_FULLY_REPLACED_AND_RESIDUAL"
    if ordinal in residual:
        return "RESIDUAL_ONLY"
    if ordinal in fully:
        return "FULLY_REPLACED_ONLY"
    return "RESOLVED_CHILD_ONLY"


def reconstruct_expected(producer_sha256: str) -> dict[str, Any]:
    packages = replay_packages()
    unwrap(
        package_json(packages[R179], f"{R179}_certificate.json"),
        EXPECTED_RESULTS["Round179_certificate"],
        "Round179 certificate",
    )
    unwrap(
        package_json(packages[R179], f"{R179}_verification.json"),
        EXPECTED_RESULTS["Round179_verification"],
        "Round179 verification",
    )
    unwrap(
        package_json(packages[R182], f"{R182}_verification.json"),
        EXPECTED_RESULTS["Round182_verification"],
        "Round182 verification",
    )

    source179 = unwrap(
        package_json(packages[R179], f"{R179}_rows.json"),
        EXPECTED_RESULTS["Round179_attachment"],
        "Round179 attachment",
    )
    columns = source179["row_column_schemas"]["resolved_3d_child_rows"]
    position = {name: index for index, name in enumerate(columns)}
    packed_resolved = source179["resolved_3d_child_rows"]
    packed_clusters = source179["fully_replaced_key_cluster_rows"]
    table = source179["table_census_and_sha256"]
    ensure(
        len(packed_resolved) == 17_192
        and table["resolved_3d_child_rows"]["row_count"] == 17_192
        and table["resolved_3d_child_rows"]["rows_sha256"]
        == object_sha256(packed_resolved)
        and len(packed_clusters) == 96
        and table["fully_replaced_key_cluster_rows"]["rows_sha256"]
        == object_sha256(packed_clusters),
        "Round179 attachment tables",
    )
    counts179: Counter[int] = Counter()
    metadata: dict[int, tuple[str, list[Any]]] = {}
    occurrence_ids: set[str] = set()
    for packed in packed_resolved:
        row_id = packed[position["row_id"]]
        ordinal = packed[position["official_key_ordinal"]]
        key_data = (
            packed[position["official_key_id"]],
            packed[position["official_key_row"]],
        )
        ensure(
            row_id not in occurrence_ids
            and packed[position["ambient_dimension"]] == 3
            and packed[position["credit_kind"]]
            == "LOCAL_POSITIVE_3D_OCCURRENCE_ONLY"
            and packed[position["global_geometric_disposition_credit"]]
            == 0,
            "Round179 resolved occurrence",
        )
        occurrence_ids.add(row_id)
        ensure(
            ordinal not in metadata or metadata[ordinal] == key_data,
            "Round179 key metadata",
        )
        metadata[ordinal] = key_data
        counts179[ordinal] += 1
    fully: set[int] = set()
    cluster_ids: set[str] = set()
    released_origins = 0
    for cluster in packed_clusters:
        cluster_id, ordinals, ordinals_sha, origin_count, credit = cluster
        ensure(
            cluster_id not in cluster_ids
            and ordinals_sha == object_sha256(ordinals)
            and credit == 0,
            "Round179 key cluster",
        )
        cluster_ids.add(cluster_id)
        fully.update(ordinals)
        released_origins += origin_count
    all_keys = set(counts179)
    ensure(
        len(occurrence_ids) == 17_192
        and len(all_keys) == 116
        and len(fully) == 96
        and fully <= all_keys
        and released_origins == 4_116
        and object_sha256(sorted(all_keys))
        == "405ffd84f2a5a432d5dbbf2e0a1f1f3c4f8ed477f0408fd07e4d4c369ec27fdb"
        and object_sha256(sorted(fully))
        == "68e5124cc0e3ac64b34dd48c470553ca60ce9f9e53d159e5fd581a55786238db",
        "Round179 key sets",
    )
    del source179, packed_resolved, packed_clusters

    source204 = unwrap(
        package_json(packages[R204], f"{R204}_certificate.json"),
        EXPECTED_RESULTS["Round204_certificate"],
        "Round204 certificate",
    )
    unwrap(
        package_json(packages[R204], f"{R204}_verification.json"),
        EXPECTED_RESULTS["Round204_verification"],
        "Round204 verification",
    )
    strict204 = audit_ledger(
        source204["formal_local_open_3D_region_ledger"],
        "region_row_id",
        736,
        "Round204 strict",
    )
    joins204 = audit_ledger(
        source204["exact_key_local_join_ledger"],
        "official_key_ordinal",
        12,
        "Round204 keys",
    )
    counts204: Counter[int] = Counter()
    for row in strict204:
        ordinal = row["official_key_ordinal"]
        ensure(
            ordinal in all_keys
            and (row["official_key_id"], row["official_key_row"])
            == metadata[ordinal]
            and row["strict_open_region"] is True
            and row["formal_local_signature_credit"] == 1
            and row["global_exact_key_disposition_credit"] == 0,
            "Round204 region-key mapping",
        )
        counts204[ordinal] += 1
    tails204: Counter[int] = Counter()
    for row in joins204:
        ordinal = row["official_key_ordinal"]
        ensure(
            ordinal in counts204
            and row["global_exact_key_fibre_exhausted"] is False
            and row["global_exact_key_disposition_credit"] == 0,
            "Round204 key join",
        )
        tails204[ordinal] = row["tail_region_occurrence_count"]
    keys204 = set(counts204)
    gauge204 = {
        "source_2D_sheet_count":
            source204["formal_2D_sheet_lineage"]["source_sheet_row_count"],
        "target_2D_sheet_count":
            source204["formal_2D_sheet_lineage"]["target_sheet_row_count"],
        "one_D_stratum_count":
            source204[
                "formal_1D_boundary_and_intersection_lineage"
            ]["row_count"],
        "zero_D_stratum_count":
            source204[
                "formal_0D_endpoint_and_corner_lineage"
            ]["row_count"],
        "tail_signature_glue_count":
            source204["tail_pair_signature_glue_ledger"]["row_count"],
    }
    ensure(
        len(keys204) == 12
        and sum(counts204.values()) == 736
        and sum(tails204.values()) == 96
        and gauge204 == {
            "source_2D_sheet_count": 224,
            "target_2D_sheet_count": 224,
            "one_D_stratum_count": 1_024,
            "zero_D_stratum_count": 580,
            "tail_signature_glue_count": 32,
        },
        "Round204 censuses",
    )
    del source204, strict204, joins204

    source208 = unwrap(
        package_json(packages[R208], f"{R208}_certificate.json"),
        EXPECTED_RESULTS["Round208_certificate"],
        "Round208 certificate",
    )
    unwrap(
        package_json(packages[R208], f"{R208}_verification.json"),
        EXPECTED_RESULTS["Round208_verification"],
        "Round208 verification",
    )
    strict208 = audit_ledger(
        source208["formal_local_open_3D_signature_ledger"],
        "region_row_id",
        36_040,
        "Round208 strict",
    )
    joins208 = audit_ledger(
        source208["formal_exact_key_local_join_ledger"],
        "official_key_ordinal",
        24,
        "Round208 keys",
    )
    counts208: Counter[int] = Counter()
    region_key: dict[str, int] = {}
    for row in strict208:
        signature = row["local_return_signature"]
        ordinal = signature["official_key_ordinal"]
        ensure(
            ordinal in all_keys
            and (
                signature["official_key_id"],
                signature["official_key_row"],
            ) == metadata[ordinal]
            and row["formal_local_open_3D_signature_credit"] == 1
            and row["global_exact_key_disposition_credit"] == 0
            and row["region_row_id"] not in region_key,
            "Round208 region-key mapping",
        )
        region_key[row["region_row_id"]] = ordinal
        counts208[ordinal] += 1
    keys208 = set(counts208)
    ensure(
        len(keys208) == 24
        and sum(counts208.values()) == 36_040
        and not (keys204 & keys208)
        and all(
            row["official_key_ordinal"] in keys208
            and row["global_exact_key_fibre_exhausted"] is False
            and row["global_exact_key_disposition_credit"] == 0
            for row in joins208
        ),
        "Round208 censuses",
    )
    del source208, strict208, joins208

    source211 = unwrap(
        package_json(packages[R211], f"{R211}_certificate.json"),
        EXPECTED_RESULTS["Round211_certificate"],
        "Round211 certificate",
    )
    verification211 = package_json(
        packages[R211], f"{R211}_verification.json"
    )
    ensure(
        set(verification211)
        == {"schema", "verification", "verification_result_sha256"}
        and verification211["verification_result_sha256"]
        == EXPECTED_RESULTS["Round211_verification"]
        and object_sha256(verification211["verification"])
        == EXPECTED_RESULTS["Round211_verification"],
        "Round211 verification",
    )
    lower: dict[str, Counter[int]] = {}
    for output_name, ledger_name, row_id, expected_count in (
        (
            "two_D_sheet_owner_incidence_count",
            "formal_2D_sheet_owner_ledger",
            "sheet_row_id",
            17_716,
        ),
        (
            "one_D_curve_owner_incidence_count",
            "formal_1D_curve_incidence_owner_ledger",
            "curve_row_id",
            20_456,
        ),
        (
            "zero_D_endpoint_owner_incidence_count",
            "formal_0D_endpoint_incidence_owner_ledger",
            "endpoint_row_id",
            40_912,
        ),
    ):
        rows = audit_ledger(
            source211[ledger_name],
            row_id,
            expected_count,
            output_name,
        )
        by_key: Counter[int] = Counter()
        for row in rows:
            ensure(
                row["owner_region_row_id"] in region_key
                and row["local_dimensional_owner_materialized"] is True
                and row["formal_half_open_owner_credit"] == 1
                and row["component_deduplication_credit"] == 0
                and row["global_exact_key_disposition_credit"] == 0,
                f"Round211 owner join:{output_name}",
            )
            by_key[region_key[row["owner_region_row_id"]]] += 1
        ensure(
            set(by_key) == keys208
            and sum(by_key.values()) == expected_count,
            f"Round211 key count:{output_name}",
        )
        lower[output_name] = by_key
    del source211, region_key

    source213 = unwrap(
        package_json(packages[R213], f"{R213}_certificate.json"),
        EXPECTED_RESULTS["Round213_certificate"],
        "Round213 certificate",
    )
    unwrap(
        package_json(packages[R213], f"{R213}_verification.json"),
        EXPECTED_RESULTS["Round213_verification"],
        "Round213 verification",
    )
    ordinal_union = source213["formal_local_exact_key_ordinal_union"]
    residual_rows = audit_ledger(
        ordinal_union,
        "official_key_ordinal",
        36,
        "Round213 ordinals",
    )
    residual = {row["official_key_ordinal"] for row in residual_rows}
    ensure(
        residual == keys204 | keys208
        and ordinal_union["Round204_ordinals"] == sorted(keys204)
        and ordinal_union["Round208_ordinals"] == sorted(keys208)
        and ordinal_union["global_exact_key_fibre_exhausted"] is False
        and ordinal_union["global_exact_key_disposition_credit"] == 0
        and object_sha256(sorted(residual))
        == "5ba4d5186ddb7ddb1868957f83af9d5224dbddaa619ecfedf1cdc51f7bc03763",
        "Round213 residual key union",
    )
    del source213, residual_rows

    class_keys: defaultdict[str, list[int]] = defaultdict(list)
    for ordinal in sorted(all_keys):
        class_keys[category(ordinal, fully, residual)].append(ordinal)
    class_counts = {
        "BOTH_FULLY_REPLACED_AND_RESIDUAL": 32,
        "RESIDUAL_ONLY": 4,
        "FULLY_REPLACED_ONLY": 64,
        "RESOLVED_CHILD_ONLY": 16,
    }
    ensure(
        {
            name: len(class_keys[name]) for name in class_counts
        } == class_counts
        and all(
            object_sha256(class_keys[name]) == CLASS_KEY_SHA256[name]
            for name in class_counts
        ),
        "classification",
    )
    expected_class_values = {
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
    class_census: dict[str, dict[str, Any]] = {}
    for name in class_counts:
        ordinals = class_keys[name]
        totals = [
            counts179[value] + counts204[value] + counts208[value]
            for value in ordinals
        ]
        values = (
            sum(counts179[value] for value in ordinals),
            sum(counts204[value] for value in ordinals),
            sum(counts208[value] for value in ordinals),
            sum(totals),
            min(totals),
            max(totals),
            sum(lower["two_D_sheet_owner_incidence_count"][value]
                for value in ordinals),
            sum(lower["one_D_curve_owner_incidence_count"][value]
                for value in ordinals),
            sum(lower["zero_D_endpoint_owner_incidence_count"][value]
                for value in ordinals),
        )
        ensure(values == expected_class_values[name], f"class values:{name}")
        class_census[name] = {
            "key_count": len(ordinals),
            "key_ordinals_sha256": object_sha256(ordinals),
            "Round179_resolved_child_occurrence_count": values[0],
            "Round204_strict_local_region_occurrence_count": values[1],
            "Round208_strict_local_region_occurrence_count": values[2],
            "local_3D_occurrence_count": values[3],
            "per_key_local_3D_occurrence_minimum": values[4],
            "per_key_local_3D_occurrence_maximum": values[5],
            "Round211_2D_sheet_owner_incidence_count": values[6],
            "Round211_1D_curve_owner_incidence_count": values[7],
            "Round211_0D_endpoint_owner_incidence_count": values[8],
        }

    key_rows: list[dict[str, Any]] = []
    for ordinal in sorted(all_keys):
        if ordinal in keys204:
            lower_source = "ROUND204_SEPARATE_FORMAL_DIMENSIONAL_GAUGE"
        elif ordinal in keys208:
            lower_source = "ROUND211_KEYWISE_OWNER_INCIDENCE_LEDGER"
        else:
            lower_source = "NONE"
        key_id, key_row = metadata[ordinal]
        key_rows.append(close({
            "official_key_ordinal": ordinal,
            "official_key_id": key_id,
            "official_key_row": key_row,
            "classification": category(ordinal, fully, residual),
            "observed_in_Round179_resolved_children": True,
            "in_Round179_fully_replaced_cluster": ordinal in fully,
            "in_Round213_residual_36_key_union": ordinal in residual,
            "Round179_resolved_child_occurrence_count":
                counts179[ordinal],
            "Round204_strict_local_region_occurrence_count":
                counts204[ordinal],
            "Round204_tail_open_region_count_separately_tagged_nonadditive":
                tails204[ordinal],
            "Round208_strict_local_region_occurrence_count":
                counts208[ordinal],
            "local_3D_occurrence_count": (
                counts179[ordinal]
                + counts204[ordinal]
                + counts208[ordinal]
            ),
            "local_3D_occurrence_is_not_a_physical_component_count": True,
            "residual_local_lower_dimensional_atlas_present":
                ordinal in residual,
            "local_lower_dimensional_atlas_source": lower_source,
            "Round204_lower_dimensional_rows_preserved_in_separate_gauge":
                ordinal in keys204,
            "Round204_lower_dimensional_rows_not_allocated_keywise":
                ordinal in keys204,
            "Round211_2D_sheet_owner_incidence_count":
                lower["two_D_sheet_owner_incidence_count"][ordinal],
            "Round211_1D_curve_owner_incidence_count":
                lower["one_D_curve_owner_incidence_count"][ordinal],
            "Round211_0D_endpoint_owner_incidence_count":
                lower["zero_D_endpoint_owner_incidence_count"][ordinal],
            "Round179_resolved_child_lower_dimensional_boundary_atlas_materialized":
                False,
            "cross_occurrence_physical_glue_materialized": False,
            "physical_component_credit": 0,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    ensure(
        len(key_rows) == 116
        and sum(row["local_3D_occurrence_count"] for row in key_rows)
        == 53_968,
        "expected key rows",
    )

    probe_raw = exact_read(HERE / ROUND214_PROBE, 100_000)
    report_raw = exact_read(HERE / ROUND214_REPORT, 100_000)
    ensure(
        hashlib.sha256(probe_raw).hexdigest() == ROUND214_PROBE_SHA256
        and hashlib.sha256(report_raw).hexdigest() == ROUND214_REPORT_SHA256,
        "Round214 read-only pins",
    )
    erratum_manifest_raw = exact_read(
        HERE / ROUND213_ERRATUM_MANIFEST, 10_000
    )
    ensure(
        hashlib.sha256(erratum_manifest_raw).hexdigest()
        == ROUND213_ERRATUM_MANIFEST_SHA256
        and parse_manifest(erratum_manifest_raw)
        == {ROUND213_ERRATUM: ROUND213_ERRATUM_SHA256}
        and hashlib.sha256(
            exact_read(HERE / ROUND213_ERRATUM, 10_000)
        ).hexdigest() == ROUND213_ERRATUM_SHA256,
        "Round213 immutable erratum pin",
    )

    boundary_blocker = {
        "Round179_resolved_child_occurrence_count_missing_explicit_lower_dimensional_boundary_atlas":
            17_192,
        "explicit_Round179_resolved_child_boundary_atlas_row_count": 0,
        "missing_boundary_cell_count":
            "NOT_ENUMERABLE_BEFORE_EXPLICIT_BOUNDARY_MATERIALIZATION",
    }
    glue_blocker = {
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
    blockers = {
        "independent_blocker_count": 2,
        "Round179_resolved_child_lower_dimensional_boundary_blocker":
            boundary_blocker,
        "physical_glue_and_internal_face_trace_blocker": glue_blocker,
        "blockers_are_logically_independent_and_both_required": True,
        "first_obstruction_order": [
            "ROUND179_RESOLVED_CHILD_LOWER_DIMENSIONAL_BOUNDARY_ATLAS",
            "P_OR_S_INTERNAL_FACE_ZERO_TRACE_INCIDENCE_IDS",
            "CROSS_OCCURRENCE_COMMON_REFINEMENT_GLUE_IDS",
            "PARTIAL_FACE_CURVE_RESTRICTIONS_AND_ENDPOINT_TO_INTERIOR_JOINS",
        ],
    }

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
                    dict(sorted(packages[prefix].items()))
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
                object_sha256(sorted(all_keys)),
            "Round179_fully_replaced_cluster_key_count": 96,
            "Round179_fully_replaced_cluster_keys_sha256":
                object_sha256(sorted(fully)),
            "Round213_residual_key_count": 36,
            "Round213_residual_keys_sha256":
                object_sha256(sorted(residual)),
            "fully_replaced_and_residual_intersection_count": 32,
            "classification_count": dict(sorted(class_counts.items())),
            "classification_key_ordinals_sha256":
                dict(sorted(CLASS_KEY_SHA256.items())),
            "classification_is_disjoint_complete_partition": True,
            "Round204_12_plus_Round208_Round211_24_equals_Round213_36":
                True,
        },
        "formal_key_occurrence_exhaustion_frontier_ledger": {
            "row_count": 116,
            "rows_sha256": object_sha256(key_rows),
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
            "Round204_lower_dimensional_gauge": gauge204,
            "Round208_Round211_key_count_with_keywise_owner_incidences": 24,
            "Round211_2D_sheet_owner_incidence_count": 17_716,
            "Round211_1D_curve_owner_incidence_count": 20_456,
            "Round211_0D_endpoint_owner_incidence_count": 40_912,
            "Round211_owner_region_to_Round208_signature_key_join_complete":
                True,
            "local_lower_dimensional_materialization_does_not_exhaust_fibre":
                True,
        },
        "formal_missing_exhaustion_frontier": blockers,
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


def audit_expected(result: dict[str, Any]) -> dict[str, Any]:
    ensure(result["status"] == STATUS, "status")
    ledger = result["formal_key_occurrence_exhaustion_frontier_ledger"]
    rows = ledger["rows"]
    ensure(
        ledger["row_count"] == len(rows) == 116
        and ledger["rows_sha256"] == object_sha256(rows)
        and len({row["official_key_ordinal"] for row in rows}) == 116,
        "frontier ledger",
    )
    for row in rows:
        ensure(
            row["row_sha256"] == object_sha256({
                key: value for key, value in row.items()
                if key != "row_sha256"
            })
            and row[
                "Round179_resolved_child_lower_dimensional_boundary_atlas_materialized"
            ] is False
            and row["cross_occurrence_physical_glue_materialized"] is False
            and row["physical_component_credit"] == 0
            and row["global_exact_key_fibre_exhausted"] is False
            and row["global_exact_key_disposition_credit"] == 0,
            "frontier closed row",
        )
    classes = Counter(row["classification"] for row in rows)
    atlas = Counter(
        row["classification"]
        for row in rows
        if row["residual_local_lower_dimensional_atlas_present"]
    )
    local_total = sum(row["local_3D_occurrence_count"] for row in rows)
    census = result[
        "local_3D_occurrence_census_without_physical_promotion"
    ]
    blockers = result["formal_missing_exhaustion_frontier"]
    nonpromotion = result["strict_nonpromotion"]
    ensure(
        classes == {
            "BOTH_FULLY_REPLACED_AND_RESIDUAL": 32,
            "RESIDUAL_ONLY": 4,
            "FULLY_REPLACED_ONLY": 64,
            "RESOLVED_CHILD_ONLY": 16,
        }
        and atlas == {
            "BOTH_FULLY_REPLACED_AND_RESIDUAL": 32,
            "RESIDUAL_ONLY": 4,
        }
        and local_total == census["local_3D_occurrence_count"] == 53_968
        and census[
            "Round204_96_tail_regions_are_a_tagged_subset_of_the_736_strict_open_regions"
        ] is True
        and blockers["independent_blocker_count"] == 2
        and blockers[
            "Round179_resolved_child_lower_dimensional_boundary_blocker"
        ][
            "Round179_resolved_child_occurrence_count_missing_explicit_lower_dimensional_boundary_atlas"
        ] == 17_192
        and blockers[
            "physical_glue_and_internal_face_trace_blocker"
        ]["explicit_cross_occurrence_common_refinement_glue_row_count"] == 0
        and blockers[
            "physical_glue_and_internal_face_trace_blocker"
        ]["concurrent_Round217_not_pinned_or_included"] is True
        and nonpromotion["all_116_global_exact_key_fibres_exhausted"]
        is False
        and nonpromotion["global_exact_key_fibre_exhausted_count"] == 0
        and nonpromotion["physical_component_credit"] == 0
        and nonpromotion["whole_origin_credit"] == 0
        and nonpromotion["whole_original_tube_credit"] == 0
        and nonpromotion["global_exact_key_disposition_credit"] == 0
        and nonpromotion["D02"] == "BLOCKED"
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "strict frontier audit",
    )
    binding = result["formal_input_binding"]
    ensure(
        binding["all_six_manifests_and_38_entries_replayed"] is True
        and binding["Round213_immutable_report_erratum_sha256"]
        == ROUND213_ERRATUM_SHA256
        and binding[
            "Round213_immutable_report_erratum_manifest_sha256"
        ] == ROUND213_ERRATUM_MANIFEST_SHA256
        and binding["Round213_frozen_six_artifact_manifest_unchanged"]
        is True,
        "erratum binding",
    )
    return {
        "key_count": 116,
        "Round179_resolved_child_occurrence_count": 17_192,
        "fully_replaced_cluster_key_count": 96,
        "residual_key_count": 36,
        "fully_replaced_residual_intersection_count": 32,
        "classification_count": dict(sorted(classes.items())),
        "local_3D_occurrence_count": local_total,
        "lower_dimensional_atlas_covered_key_count": sum(atlas.values()),
        "lower_dimensional_atlas_missing_key_count": 80,
        "independent_missing_blocker_count": 2,
        "global_exact_key_fibre_exhausted_count": 0,
        "global_exact_key_disposition_credit": 0,
    }


def duplicate_literal_key_count(tree: ast.AST) -> int:
    duplicates = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: set[Any] = set()
        for key in node.keys:
            if (
                isinstance(key, ast.Constant)
                and type(key.value) in {str, int, bool, type(None)}
            ):
                if key.value in seen:
                    duplicates += 1
                seen.add(key.value)
    return duplicates


def inert_boundary_audit() -> dict[str, Any]:
    producer_raw = exact_read(PRODUCER, 1_000_000)
    verifier_raw = exact_read(Path(__file__), 1_000_000)
    ensure(
        hashlib.sha256(producer_raw).hexdigest()
        == EXPECTED_PRODUCER_SHA256,
        "producer inert-byte pin",
    )
    producer_tree = ast.parse(producer_raw, filename=PRODUCER.name)
    verifier_tree = ast.parse(verifier_raw, filename=Path(__file__).name)
    producer_duplicates = duplicate_literal_key_count(producer_tree)
    verifier_duplicates = duplicate_literal_key_count(verifier_tree)
    ensure(
        producer_duplicates == verifier_duplicates == 0,
        "duplicate literal dictionary keys",
    )

    def bodies(tree: ast.AST) -> dict[str, str]:
        output: dict[str, str] = {}
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                output[node.name] = hashlib.sha256(
                    ast.dump(
                        ast.Module(body=node.body, type_ignores=[]),
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
    overlaps = sorted(
        (producer_name, verifier_name)
        for verifier_name, value in verifier_bodies.items()
        for producer_name in reverse.get(value, [])
    )
    return {
        "producer_treated_as_inert_bytes": True,
        "producer_imported_or_executed": False,
        "producer_sha256": EXPECTED_PRODUCER_SHA256,
        "verifier_sha256": hashlib.sha256(verifier_raw).hexdigest(),
        "producer_AST_duplicate_literal_key_count": producer_duplicates,
        "verifier_AST_duplicate_literal_key_count": verifier_duplicates,
        "exact_AST_body_overlap_pair_count": len(overlaps),
        "exact_AST_body_overlap_pairs": [
            {
                "producer_function": producer,
                "verifier_function": verifier,
            }
            for producer, verifier in overlaps
        ],
        "implementation_diverse_second_derivation_claimed": False,
        "shared_generic_algorithm_risk_disclosed": True,
    }


def resign_frontier_row(result: dict[str, Any], index: int) -> None:
    ledger = result["formal_key_occurrence_exhaustion_frontier_ledger"]
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
        and document["result_sha256"]
        == object_sha256(document["result"]),
        "candidate wrapper",
    )
    audit_expected(document["result"])
    ensure(document["result"] == expected, "complete expected equality")


def semantic_attack_suite(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    rows = candidate["result"][
        "formal_key_occurrence_exhaustion_frontier_ledger"
    ]["rows"]
    nonresidual_index = next(
        index for index, row in enumerate(rows)
        if not row["in_Round213_residual_36_key_union"]
    )
    residual_index = next(
        index for index, row in enumerate(rows)
        if row["in_Round213_residual_36_key_union"]
    )
    attacks: list[tuple[str, tuple[Any, ...], Any, int | None]] = [
        (
            "official key ordinal tamper",
            ("result", "formal_key_occurrence_exhaustion_frontier_ledger",
             "rows", 0, "official_key_ordinal"),
            -1,
            0,
        ),
        (
            "classification tamper",
            ("result", "formal_key_occurrence_exhaustion_frontier_ledger",
             "rows", 0, "classification"),
            "RESIDUAL_ONLY",
            0,
        ),
        (
            "steal one of 80 missing keys into 36-key atlas",
            ("result", "formal_key_occurrence_exhaustion_frontier_ledger",
             "rows", nonresidual_index,
             "residual_local_lower_dimensional_atlas_present"),
            True,
            nonresidual_index,
        ),
        (
            "remove one of 36 covered keys into 80-key missing set",
            ("result", "formal_key_occurrence_exhaustion_frontier_ledger",
             "rows", residual_index,
             "residual_local_lower_dimensional_atlas_present"),
            False,
            residual_index,
        ),
        (
            "fabricated Round179 resolved-child boundary atlas",
            ("result", "formal_key_occurrence_exhaustion_frontier_ledger",
             "rows", 0,
             "Round179_resolved_child_lower_dimensional_boundary_atlas_materialized"),
            True,
            0,
        ),
        (
            "invented cross-occurrence physical glue",
            ("result", "formal_key_occurrence_exhaustion_frontier_ledger",
             "rows", 0, "cross_occurrence_physical_glue_materialized"),
            True,
            0,
        ),
        (
            "incidence promoted to physical component",
            ("result", "formal_key_occurrence_exhaustion_frontier_ledger",
             "rows", 0, "physical_component_credit"),
            1,
            0,
        ),
        (
            "local key promoted to global fibre exhaustion",
            ("result", "formal_key_occurrence_exhaustion_frontier_ledger",
             "rows", 0, "global_exact_key_fibre_exhausted"),
            True,
            0,
        ),
        (
            "invented global disposition",
            ("result", "formal_key_occurrence_exhaustion_frontier_ledger",
             "rows", 0, "global_exact_key_disposition_credit"),
            1,
            0,
        ),
        (
            "false missing boundary occurrence count zero",
            ("result", "formal_missing_exhaustion_frontier",
             "Round179_resolved_child_lower_dimensional_boundary_blocker",
             "Round179_resolved_child_occurrence_count_missing_explicit_lower_dimensional_boundary_atlas"),
            0,
            None,
        ),
        (
            "fabricated boundary atlas row",
            ("result", "formal_missing_exhaustion_frontier",
             "Round179_resolved_child_lower_dimensional_boundary_blocker",
             "explicit_Round179_resolved_child_boundary_atlas_row_count"),
            1,
            None,
        ),
        (
            "96 tagged tail rows double counted",
            ("result",
             "local_3D_occurrence_census_without_physical_promotion",
             "local_3D_occurrence_count"),
            54_064,
            None,
        ),
        (
            "concurrent Round217 falsely treated as pinned",
            ("result", "formal_missing_exhaustion_frontier",
             "physical_glue_and_internal_face_trace_blocker",
             "concurrent_Round217_not_pinned_or_included"),
            False,
            None,
        ),
        (
            "fabricated cross-occurrence glue census",
            ("result", "formal_missing_exhaustion_frontier",
             "physical_glue_and_internal_face_trace_blocker",
             "explicit_cross_occurrence_common_refinement_glue_row_count"),
            9_200,
            None,
        ),
        (
            "erratum digest tamper",
            ("result", "formal_input_binding",
             "Round213_immutable_report_erratum_sha256"),
            "0" * 64,
            None,
        ),
        (
            "erratum omission",
            ("result", "formal_input_binding",
             "Round213_immutable_report_erratum_filename"),
            "",
            None,
        ),
        (
            "116 fibres falsely exhausted",
            ("result", "strict_nonpromotion",
             "all_116_global_exact_key_fibres_exhausted"),
            True,
            None,
        ),
        (
            "global fibre exhausted count 116",
            ("result", "strict_nonpromotion",
             "global_exact_key_fibre_exhausted_count"),
            116,
            None,
        ),
        (
            "component credit theft",
            ("result", "strict_nonpromotion", "physical_component_credit"),
            53_968,
            None,
        ),
        (
            "whole origin credit theft",
            ("result", "strict_nonpromotion", "whole_origin_credit"),
            116,
            None,
        ),
        (
            "whole tube credit theft",
            ("result", "strict_nonpromotion",
             "whole_original_tube_credit"),
            116,
            None,
        ),
        (
            "global disposition credit theft",
            ("result", "strict_nonpromotion",
             "global_exact_key_disposition_credit"),
            116,
            None,
        ),
        (
            "D02 promotion",
            ("result", "strict_nonpromotion", "D02"),
            "OPEN",
            None,
        ),
        (
            "CM2 promotion",
            ("result", "strict_nonpromotion", "CM2"),
            "GO",
            None,
        ),
        (
            "producer provenance forgery",
            ("result", "provenance", "producer_sha256"),
            "f" * 64,
            None,
        ),
    ]
    rejected: list[str] = []
    for name, path, replacement, row_index in attacks:
        old = assign(candidate, path, replacement)
        ensure(old != replacement, f"attack collision:{name}")
        try:
            if row_index is not None:
                resign_frontier_row(candidate["result"], row_index)
            candidate["result_sha256"] = object_sha256(candidate["result"])
            try:
                validate_candidate(candidate, expected)
            except Exception:
                rejected.append(name)
            else:
                raise Round216VerificationError(
                    f"semantic attack accepted:{name}"
                )
        finally:
            assign(candidate, path, old)
            if row_index is not None:
                resign_frontier_row(candidate["result"], row_index)
            candidate["result_sha256"] = object_sha256(candidate["result"])

    ledger = candidate["result"][
        "formal_key_occurrence_exhaustion_frontier_ledger"
    ]
    first = ledger["rows"][0]
    for delta, name in (
        (-1, "per-key occurrence omitted with recomputed digest"),
        (1, "per-key occurrence duplicated with recomputed digest"),
    ):
        old_source = first["Round179_resolved_child_occurrence_count"]
        old_total = first["local_3D_occurrence_count"]
        first["Round179_resolved_child_occurrence_count"] += delta
        first["local_3D_occurrence_count"] += delta
        resign_frontier_row(candidate["result"], 0)
        candidate["result_sha256"] = object_sha256(candidate["result"])
        try:
            try:
                validate_candidate(candidate, expected)
            except Exception:
                rejected.append(name)
            else:
                raise Round216VerificationError(
                    f"semantic attack accepted:{name}"
                )
        finally:
            first["Round179_resolved_child_occurrence_count"] = old_source
            first["local_3D_occurrence_count"] = old_total
            resign_frontier_row(candidate["result"], 0)
            candidate["result_sha256"] = object_sha256(candidate["result"])

    original_count = ledger["row_count"]
    original_sha = ledger["rows_sha256"]
    removed = ledger["rows"].pop()
    ledger["row_count"] = len(ledger["rows"])
    ledger["rows_sha256"] = object_sha256(ledger["rows"])
    candidate["result_sha256"] = object_sha256(candidate["result"])
    try:
        try:
            validate_candidate(candidate, expected)
        except Exception:
            rejected.append("key row omitted with recomputed ledger")
        else:
            raise Round216VerificationError("key-row omission accepted")
    finally:
        ledger["rows"].append(removed)
        ledger["row_count"] = original_count
        ledger["rows_sha256"] = original_sha
        candidate["result_sha256"] = object_sha256(candidate["result"])

    ledger["rows"].append(copy.deepcopy(ledger["rows"][0]))
    ledger["row_count"] = len(ledger["rows"])
    ledger["rows_sha256"] = object_sha256(ledger["rows"])
    candidate["result_sha256"] = object_sha256(candidate["result"])
    try:
        try:
            validate_candidate(candidate, expected)
        except Exception:
            rejected.append("key row duplicated with recomputed ledger")
        else:
            raise Round216VerificationError("key-row duplicate accepted")
    finally:
        ledger["rows"].pop()
        ledger["row_count"] = original_count
        ledger["rows_sha256"] = original_sha
        candidate["result_sha256"] = object_sha256(candidate["result"])

    expected_count = len(attacks) + 4
    ensure(
        len(rejected) == expected_count
        and candidate["result"] == expected
        and candidate["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "semantic restoration",
    )
    return {
        "attack_count": expected_count,
        "rejected_count": len(rejected),
        "all_rejected": True,
        "attack_names": rejected,
        "affected_row_ledger_and_result_digests_recomputed": True,
    }


def reject_case(name: str, operation: Callable[[], Any]) -> str:
    try:
        operation()
    except Exception:
        return name
    raise Round216VerificationError(f"attack accepted:{name}")


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
            lambda raw=raw, name=name: decode(raw, f"attack:{name}"),
        )
        for name, raw in cases
    ]
    rejected.append(reject_case(
        "oversize",
        lambda: decode(b"{}\n", "attack:oversize", maximum=2),
    ))
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
        REPORT.resolve(),
        COLD.resolve(),
        MANIFEST.resolve(),
        (HERE / ROUND214_PROBE).resolve(),
        (HERE / ROUND214_REPORT).resolve(),
        (HERE / ROUND213_ERRATUM).resolve(),
        (HERE / ROUND213_ERRATUM_MANIFEST).resolve(),
    }
    for _, (manifest_name, _, _) in PACKAGE_MANIFESTS.items():
        manifest_path = HERE / manifest_name
        protected.add(manifest_path.resolve())
        entries = parse_manifest(exact_read(manifest_path, 10_000))
        protected.update((HERE / name).resolve() for name in entries)
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
            absolute.name.startswith(".cm2_round216_")
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
        prefix=".cm2_round216_attack.",
        dir=HERE,
    ))
    source = scratch / "source"
    victim = scratch / "victim"
    source.write_bytes(b"SAFE\n")
    victim.write_bytes(b"SAFE\n")
    input_symlink = HERE / f".cm2_round216_{pid}_input_symlink"
    input_hardlink = HERE / f".cm2_round216_{pid}_input_hardlink"
    input_fifo = HERE / f".cm2_round216_{pid}_input_fifo"
    output_symlink = (
        HERE / f".cm2_round216_{pid}_symlink_verification.json"
    )
    output_hard_base = (
        HERE / f".cm2_round216_{pid}_base_verification.json"
    )
    output_hardlink = (
        HERE / f".cm2_round216_{pid}_hard_verification.json"
    )
    output_fifo = (
        HERE / f".cm2_round216_{pid}_fifo_verification.json"
    )
    outside = (
        HERE.parent / f".cm2_round216_{pid}_escape_verification.json"
    )
    parent_alias = HERE / f".cm2_round216_parent_alias_{pid}"
    safe_target = (
        HERE / f".cm2_round216_{pid}_safe_verification.json"
    )
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
                lambda: exact_read(input_symlink, 64),
            ),
            reject_case(
                "input hardlink",
                lambda: exact_read(input_hardlink, 64),
            ),
            reject_case(
                "input FIFO",
                lambda: exact_read(input_fifo, 64),
            ),
            reject_case(
                "input directory",
                lambda: exact_read(scratch, 64),
            ),
            reject_case(
                "input parent escape",
                lambda: exact_read(HERE.parent / "outside", 64),
            ),
        ])
        parent_alias.symlink_to(HERE, target_is_directory=True)
        rejected.append(reject_case(
            "input symlink parent alias",
            lambda: exact_read(parent_alias / PRODUCER.name, 1_000_000),
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
                    / f".cm2_round216_{pid}_nested_verification.json",
                    b"x",
                ),
            ),
            reject_case(
                "output symlink parent alias",
                lambda: atomic_write(
                    parent_alias
                    / f".cm2_round216_{pid}_alias_verification.json",
                    b"x",
                ),
            ),
            reject_case(
                "output parent-dot-dot alias",
                lambda: atomic_write(
                    HERE / ".." / HERE.name
                    / f".cm2_round216_{pid}_dotdot_verification.json",
                    b"x",
                ),
            ),
            reject_case(
                "unallowlisted output",
                lambda: atomic_write(
                    HERE / f"cm2_round216_{pid}_unlisted.json",
                    b"x",
                ),
            ),
            reject_case(
                "certificate-shaped hidden output",
                lambda: atomic_write(
                    HERE / f".cm2_round216_{pid}_certificate.json",
                    b"x",
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
    ensure(len(rejected) == 20, "path/type/output attack count")
    return {
        "attack_count": len(rejected),
        "rejected_or_safely_bypassed_count": len(rejected),
        "all_rejected_or_safely_bypassed": True,
        "attack_names": rejected,
        "protected_files_modified": False,
        "prepositioned_temporary_symlink_not_followed": True,
    }


def load_candidate() -> tuple[dict[str, Any], bytes]:
    raw = exact_read(CERTIFICATE, EXPECTED_CERTIFICATE_SIZE)
    ensure(
        len(raw) == EXPECTED_CERTIFICATE_SIZE
        and hashlib.sha256(raw).hexdigest()
        == EXPECTED_CERTIFICATE_SHA256,
        "candidate byte pin",
    )
    return decode(raw, CERTIFICATE.name), raw


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

    # Candidate bytes are unavailable to all preceding reconstruction steps.
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

    semantic = semantic_attack_suite(candidate, expected_result)
    json_attacks = strict_json_attack_suite()
    path_attacks = path_type_output_attack_suite()
    ensure(PRODUCER.stem not in sys.modules, "producer not imported")

    verification_result = {
        "status": "PASS_PARTIAL_FORMAL_ROUND216",
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
        "strict_nonpromotion": {
            "all_116_global_exact_key_fibres_exhausted": False,
            "global_exact_key_fibre_exhausted_count": 0,
            "physical_component_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "independence_contract": {
            **boundary,
            "all_six_manifests_and_38_entries_replayed": True,
            "Round213_immutable_erratum_replayed": True,
            "candidate_loaded_only_after_expected_rebuilt": True,
            "concurrent_Round217_not_pinned_or_included": True,
            "implementation_diverse_second_derivation_claimed": False,
        },
        "semantic_resigned_attack_suite": semantic,
        "strict_JSON_and_oversize_attack_suite": json_attacks,
        "path_type_and_output_attack_suite": path_attacks,
        "output_safety": {
            "strict_verification_only_allowlist": True,
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
