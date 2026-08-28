#!/usr/bin/env python3
"""Independent verifier for the Round267 terminal-lineage certificate.

The producer is pinned and treated as inert bytes.  This verifier contains
its own reconstruction path from the Round174, Round179, and frozen Round266
inputs; it never imports or executes the producer.  It first completes the
expected result, only then opens the candidate, compares the complete object,
and finally checks resigned semantic corruptions.

Round174 records 62,696 lower-dimensional rows, many with deliberately
nominal ``regular if present`` or ``candidate if transverse`` status.
Round179 later replaces every containing residual tube by a pinned normal
form.  This producer independently matches every Round174 stratum to exactly
one terminal Round179 normal form, exact source-chart seam graph, certified
Round174 physical grazing face, or strict descendant-wide absence
certificate.

``MATERIALIZED_AS_CANONICAL_SUPPORT`` is a lineage status, not automatically
a physical-existence claim.  Only the twelve Round174 grazing boundary
faces, 472 exact full-base source-chart seam graphs, and 344 exact full-base
outgoing graphs receive physical-existence credit.  A further 320 Round179
wall normal forms carry an explicit target ``FULL_BASE_UNIQUE_GRAPH`` and
also receive physical-existence credit.  Source-factor regular graphs that
only overwrap a base remain nominal, as do all nominal pair supports.

Round267 is quotient-neutral.  Once the Round266 freeze is pinned below, its
component, occurrence, exact-key, and valid-virtual-node frontiers are
preserved by exact digest identity.  No maximality, fibre, global
disposition, Jx/Jy same-point glue, Gate5, D02, or CM2 credit is awarded.

The Round266 input and frontier names are intentionally centralized in the
marked pending block so the already complete lineage reconstruction can be
bound byte-for-byte as soon as Round266 freezes.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gc
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round267_source_g_lower_stratum_terminal_lineage"
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE = HERE / f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
SCHEMA = "cm2.round267.source-g-lower-stratum-terminal-lineage.v1"
VERIFICATION_SCHEMA = (
    "cm2.round267.source-g-lower-stratum-terminal-lineage-verification.v1"
)
PRODUCER_SHA256 = (
    "5ad12bc7b6fe6b1fc7210150a493ef99e73dcf7b0605f674513454f3caeb20b1"
)
CANDIDATE_SHA256 = (
    "66879215e0250a4a462fea9837c24bccf49a936ce3c5e66da2707e1a66fafc8f"
)
CANDIDATE_RESULT_SHA256 = (
    "deaee59586be2f324fbedfe7a97d8ee54b7962f818a3d12ff1d4935d881b0c35"
)
CANDIDATE_SIZE = 116_140_190

ROUND174_CERTIFICATE = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_"
    "materialization_certificate.json"
)
ROUND174_ROWS = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_"
    "materialization_rows.json"
)
ROUND179_CERTIFICATE = (
    "cm2_round179_source_g_residual_tube_arrangement_certificate.json"
)
ROUND179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"

# BEGIN ROUND266 FREEZE ADAPTER -- replace only this block after freeze.
ROUND266_CERTIFICATE = (
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
)
ROUND266_FILE_SHA256 = (
    "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"
)
ROUND266_RESULT_SHA256 = (
    "39bc6d46bc7b83e73af0cc3466b79196defa4a2518e1db704b7a3f61f2e2173b"
)
ROUND266_SCHEMA = "cm2.round266.source-g-expanded-curved-face-closure.v1"
ROUND266_FRONTIERS = (
    (
        "COMPONENT",
        "formal_post_Round266_component_frontier_ledger",
        "post_Round266_component_frontier_row_id",
        63_224,
    ),
    (
        "OCCURRENCE",
        "formal_post_Round266_expanded_occurrence_frontier_ledger",
        "post_Round266_expanded_occurrence_frontier_row_id",
        126_468,
    ),
    (
        "EXACT_KEY",
        "formal_post_Round266_key_frontier_ledger",
        "post_Round266_key_frontier_row_id",
        116,
    ),
    (
        "VALID_VIRTUAL_NODE",
        "formal_post_Round266_valid_virtual_node_frontier_ledger",
        "post_Round266_valid_virtual_node_frontier_row_id",
        133_284,
    ),
    (
        "EXPLICIT_COMPONENT_MEMBER",
        "formal_post_Round266_component_member_frontier_ledger",
        "post_Round266_component_member_frontier_row_id",
        259_752,
    ),
)
# END ROUND266 FREEZE ADAPTER.

INPUTS = {
    ROUND174_CERTIFICATE: (
        "10221141c58c044b42e43009beb34ae4705995925a88deaa70ff2eba2ea852c7",
        "d45f05458c42189cf0ebc51e258356d13278ba40845cce80b6a072ffbc8cf09b",
        "cm2.round174.source-g-unique-first-dynamic-occurrence-materialization.v1",
    ),
    ROUND174_ROWS: (
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
        "002ca6631edd39c2325c63a1e8f9717d111f4d10c6d2585077d665a0ff128d18",
        "cm2.round174.source-g-unique-first-dynamic-occurrence-rows.v1",
    ),
    ROUND179_CERTIFICATE: (
        "edc2c538dc04a93c2b873f53e07b5c97c6b395a1d107e7ed2de4cf2c4bd35111",
        "0f57284c11c617349fe66877552c401f426efafbc75faa08948f099166e9cde3",
        "cm2.round179.source-g-residual-tube-arrangement.v1",
    ),
    ROUND179_ROWS: (
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
        "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb",
        "cm2.round179.source-g-residual-tube-arrangement-rows.v1",
    ),
    ROUND266_CERTIFICATE: (
        ROUND266_FILE_SHA256,
        ROUND266_RESULT_SHA256,
        ROUND266_SCHEMA,
    ),
}

EXPECTED_PREDICATE_HISTOGRAM = {
    "candidate_pair_intersection": 336,
    "integer_wall_crossing_endpoint": 480,
    "integer_wall_endpoint": 27_208,
    "outgoing_chart_seam": 34_188,
    "source_chart_seam": 472,
    "source_grazing": 12,
}
EXPECTED_TERMINAL_HISTOGRAM = {
    "ABSENT_ON_ALL_DESCENDANTS": 6_120,
    "MATERIALIZED_AS_CANONICAL_SUPPORT": 56_576,
}
EXPECTED_DETAIL_HISTOGRAM = {
    "CONSTITUENT_NORMAL_FORM_STRICTLY_ABSENT": 8,
    "ROUND174_CERTIFIED_PHYSICAL_BOUNDARY_FACE": 12,
    "ROUND179_BOTH_FACTORS_STRICTLY_ZERO_ABSENT": 2_712,
    "ROUND179_FACE_OVERWRAP_REGULAR_ZERO_SET_IF_PRESENT": 30_444,
    "ROUND179_FULL_BASE_UNIQUE_GRAPH": 344,
    "ROUND179_FULL_BASE_UNIQUE_SOURCE_SEAM_GRAPH": 472,
    "ROUND179_NOMINAL_PAIR_ARRANGEMENT_CANDIDATE": 328,
    "ROUND179_STRICT_ZERO_ABSENT": 3_400,
    "ROUND179_UNION_OF_CERTIFIED_REGULAR_DIMENSION_2_FACTORS": 24_976,
}
EXPECTED_PROBE_PROJECTION_SHA256 = (
    "439c2e7cf39f239c5b01e3c727326f545a67333f15ebf45301299769f5800c91"
)


class Round267Error(RuntimeError):
    """A fail-closed Round267 contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round267Error(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


def closed(row: dict[str, Any]) -> dict[str, Any]:
    output = dict(row)
    need("row_sha256" not in output, "row already closed")
    output["row_sha256"] = digest(output)
    return output


def ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    need(
        len(rows) == len({row[id_field] for row in rows}),
        f"unique ledger ids:{id_field}",
    )
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def regular_bytes(path: Path, maximum: int = 1_200_000_000) -> bytes:
    need(path.parent == HERE, f"unexpected input parent:{path.name}")
    before = path.lstat()
    need(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1,
        f"regular nonlinked input:{path.name}",
    )
    need(0 < before.st_size <= maximum, f"bounded input:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        need(
            (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns)
            == (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns),
            f"stable input open:{path.name}",
        )
        pieces: list[bytes] = []
        total = 0
        while True:
            piece = os.read(descriptor, 1024 * 1024)
            if not piece:
                break
            total += len(piece)
            need(total <= maximum, f"bounded input read:{path.name}")
            pieces.append(piece)
        after = os.fstat(descriptor)
        need(
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns),
            f"stable input read:{path.name}",
        )
        return b"".join(pieces)
    finally:
        os.close(descriptor)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"strict encoding:{label}",
    )

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, f"duplicate JSON key:{label}:{key}")
            output[key] = value
        return output

    def reject(token: str) -> None:
        raise Round267Error(f"non-integral JSON number:{label}:{token}")

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_float=reject,
            parse_constant=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Round267Error(f"strict JSON:{label}") from error
    need(isinstance(value, dict), f"top-level JSON object:{label}")
    return value


def load_result(name: str) -> dict[str, Any]:
    file_sha256, result_sha256, schema = INPUTS[name]
    raw = regular_bytes(HERE / name)
    need(hashlib.sha256(raw).hexdigest() == file_sha256, f"file pin:{name}")
    document = strict_json(raw, name)
    need(set(document) == {"schema", "result", "result_sha256"}, f"envelope:{name}")
    need(document["schema"] == schema, f"schema pin:{name}")
    need(
        document["result_sha256"] == result_sha256
        and digest(document["result"]) == result_sha256,
        f"result pin:{name}",
    )
    need(isinstance(document["result"], dict), f"result object:{name}")
    return document["result"]


def check_closed_rows(
    value: dict[str, Any],
    id_field: str,
    expected_count: int | None = None,
) -> list[dict[str, Any]]:
    rows = value["rows"]
    need(isinstance(rows, list), f"ledger rows:{id_field}")
    need(value["row_count"] == len(rows), f"ledger count:{id_field}")
    if expected_count is not None:
        need(len(rows) == expected_count, f"expected ledger count:{id_field}")
    need(
        len({row[id_field] for row in rows}) == len(rows),
        f"unique ledger ids:{id_field}",
    )
    need(value["rows_sha256"] == digest(rows), f"ledger digest:{id_field}")
    for row in rows:
        body = dict(row)
        expected = body.pop("row_sha256")
        need(expected == digest(body), f"row closure:{id_field}")
    return rows


def packed_rows(
    result: dict[str, Any],
    table: str,
    expected_count: int,
) -> list[tuple[dict[str, Any], str]]:
    census = result["table_census_and_sha256"][table]
    rows = result[table]
    columns = result["row_column_schemas"][table]
    need(
        census["row_count"] == len(rows) == expected_count
        and census["rows_sha256"] == digest(rows)
        and len(columns) == len(set(columns)),
        f"packed table contract:{table}",
    )
    output: list[tuple[dict[str, Any], str]] = []
    for packed in rows:
        need(len(packed) == len(columns), f"packed row width:{table}")
        output.append((dict(zip(columns, packed, strict=True)), digest(packed)))
    return output


def input_binding() -> dict[str, Any]:
    return {
        name: {
            "file_sha256": values[0],
            "result_sha256": values[1],
            "schema": values[2],
        }
        for name, values in sorted(INPUTS.items())
    }


def frontier_identity_row(
    round266: dict[str, Any],
    logical_object: str,
    ledger_name: str,
    id_field: str,
    expected_count: int,
) -> dict[str, Any]:
    value = round266[ledger_name]
    rows = check_closed_rows(value, id_field, expected_count)
    metadata = {key: item for key, item in value.items() if key != "rows"}
    return closed({
        "Round266_to_Round267_frontier_identity_row_id":
            f"round267-frontier-identity:{logical_object.lower()}",
        "logical_object": logical_object,
        "source_round": 266,
        "post_round": 267,
        "row_count": len(rows),
        "source_Round266_rows_sha256": value["rows_sha256"],
        "post_Round267_rows_sha256": value["rows_sha256"],
        "source_ledger_metadata_sha256": digest(metadata),
        "post_Round267_is_exact_alias_of_post_Round266": True,
        "new_assignment_or_component_count": 0,
    })


def build(producer_sha256: str) -> dict[str, Any]:
    round174_certificate = load_result(ROUND174_CERTIFICATE)
    need(
        round174_certificate["materialization_census"][
            "lower_dimensional_stratum_row_count"
        ] == 62_696
        and round174_certificate["materialization_census"][
            "chart_guard_rejection_row_count"
        ] == 728
        and round174_certificate["row_attachment"]["file_sha256"]
        == INPUTS[ROUND174_ROWS][0]
        and round174_certificate["row_attachment"]["result_sha256"]
        == INPUTS[ROUND174_ROWS][1]
        and round174_certificate["scope"]["all_unique_first_parents_fully_materialized"]
        is False
        and round174_certificate["scope"]["CM2_exterior_sheet_exclusions_added"]
        == 0
        and round174_certificate["strict_nonpromotion"]["CM2"]
        == "NO-GO_FOR_CLAIM",
        "Round174 bounded lower-stratum precondition",
    )
    del round174_certificate
    gc.collect()

    round179_certificate = load_result(ROUND179_CERTIFICATE)
    need(
        round179_certificate["row_attachment"]["file_sha256"]
        == INPUTS[ROUND179_ROWS][0]
        and round179_certificate["row_attachment"]["result_sha256"]
        == INPUTS[ROUND179_ROWS][1]
        and round179_certificate["dimension_safe_ledger"][
            "outgoing_and_wall_regular_zero_set_dimension_if_present"
        ] == 2
        and round179_certificate["dimension_safe_ledger"][
            "pair_intersection_nominal_dimension_if_transverse"
        ] == 1
        and round179_certificate["row_attachment"]["table_census_and_sha256"][
            "chart_guard_child_rows"
        ]["row_count"] == 152
        and round179_certificate["dimension_safe_ledger"][
            "chart_guard_is_not_CM2_exterior_sheet_exclusion"
        ] is True
        and round179_certificate["dimension_safe_ledger"][
            "chart_guard_is_not_Gate5_geometric_disposition"
        ] is True
        and round179_certificate["strict_nonpromotion"]["CM2"]
        == "NO-GO_FOR_CLAIM",
        "Round179 normal-form and dimension-safe precondition",
    )
    del round179_certificate
    gc.collect()

    round174 = load_result(ROUND174_ROWS)
    residual_pairs = packed_rows(
        round174,
        "residual_3d_tube_rows",
        62_012,
    )
    stratum_pairs = packed_rows(
        round174,
        "lower_dimensional_stratum_rows",
        62_696,
    )
    residual_by_id = {
        row["row_id"]: (row, row_sha256)
        for row, row_sha256 in residual_pairs
    }
    need(len(residual_by_id) == 62_012, "unique Round174 residuals")
    del round174, residual_pairs
    gc.collect()

    round179 = load_result(ROUND179_ROWS)
    origin_pairs = packed_rows(round179, "origin_tube_rows", 62_012)
    outgoing_pairs = packed_rows(
        round179,
        "outgoing_normal_form_rows",
        34_188,
    )
    wall_pairs = packed_rows(
        round179,
        "wall_normal_form_rows",
        27_688,
    )
    seam_pairs = packed_rows(
        round179,
        "source_chart_seam_rows",
        472,
    )
    pair_pairs = packed_rows(
        round179,
        "pair_arrangement_candidate_rows",
        336,
    )

    origin_by_id = {
        row["origin_row_id"]: (row, row_sha256)
        for row, row_sha256 in origin_pairs
    }
    need(
        len(origin_by_id) == len(residual_by_id) == 62_012
        and set(origin_by_id) == set(residual_by_id),
        "Round174 residuals equal Round179 origins",
    )
    for row_id, (residual, _) in residual_by_id.items():
        origin, _ = origin_by_id[row_id]
        need(
            residual["parent_id"] == origin["parent_id"]
            and residual["chart"] == origin["chart"]
            and residual["box"] == origin["original_box"]
            and residual["reason_labels"] == origin["original_reason_labels"],
            f"exact origin identity:{row_id}",
        )

    outgoing_by_origin = {
        row["origin_row_id"]: (row, row_sha256)
        for row, row_sha256 in outgoing_pairs
    }
    wall_by_origin_reason = {
        (row["origin_row_id"], row["reason_label"]): (row, row_sha256)
        for row, row_sha256 in wall_pairs
    }
    seam_by_parent_chart: dict[
        tuple[str, str],
        tuple[dict[str, Any], str],
    ] = {}
    for row, row_sha256 in seam_pairs:
        key = (row["parent_id"], row["chart"])
        need(key not in seam_by_parent_chart, f"unique source seam:{key}")
        seam_by_parent_chart[key] = (row, row_sha256)
    pair_by_origin = {
        row["origin_row_id"]: (row, row_sha256)
        for row, row_sha256 in pair_pairs
    }
    need(
        len(outgoing_by_origin) == 34_188
        and len(wall_by_origin_reason) == 27_688
        and len(seam_by_parent_chart) == 472
        and len(pair_by_origin) == 336,
        "Round179 unique normal-form census",
    )

    absence_by_origin_reason: set[tuple[str, str]] = set()
    for row, _ in outgoing_pairs:
        if row["face_classification"] == "STRICT_ZERO_ABSENT":
            absence_by_origin_reason.add((
                row["origin_row_id"],
                "outgoing_chart_seam",
            ))
    for row, _ in wall_pairs:
        target_absent = (
            row["target_factor_classification"] == "STRICT_NONZERO"
            or row["target_face_classification"] == "STRICT_ZERO_ABSENT"
        )
        if (
            row["source_factor_classification"] == "STRICT_NONZERO"
            and target_absent
        ):
            absence_by_origin_reason.add((
                row["origin_row_id"],
                row["reason_label"],
            ))

    predicate_histogram: Counter[str] = Counter()
    terminal_histogram: Counter[str] = Counter()
    detail_histogram: Counter[str] = Counter()
    support_kind_histogram: Counter[str] = Counter()
    projection_rows: list[dict[str, Any]] = []
    lineage_rows: list[dict[str, Any]] = []

    for stratum, stratum_sha256 in sorted(
        stratum_pairs,
        key=lambda item: item[0]["stratum_id"],
    ):
        stratum_id = stratum["stratum_id"]
        label = stratum["predicate_label"]
        residual_id = stratum["containing_residual_row_id"]
        predicate_histogram[label] += 1
        later_row: dict[str, Any]
        later_row_sha256: str
        later_table: str
        terminal: str
        detail: str
        support_kind: str
        explicit_physical_support = 0

        if label == "source_grazing":
            need(
                residual_id is None
                and stratum["dimension_certification"] == "CERTIFIED"
                and stratum["existence_certification"] == "CERTIFIED_PRESENT"
                and stratum["half_open_owner_status"] == "PHYSICAL_BOUNDARY_FACE",
                f"physical grazing:{stratum_id}",
            )
            terminal = "MATERIALIZED_AS_CANONICAL_SUPPORT"
            detail = "ROUND174_CERTIFIED_PHYSICAL_BOUNDARY_FACE"
            support_kind = "CERTIFIED_PHYSICAL_BOUNDARY_FACE"
            later_row = stratum
            later_row_sha256 = stratum_sha256
            later_table = "ROUND174_LOWER_DIMENSIONAL_STRATUM"
            explicit_physical_support = 1

        elif label == "source_chart_seam":
            need(residual_id is None, f"source seam parent carrier:{stratum_id}")
            later_row, later_row_sha256 = seam_by_parent_chart[
                (stratum["parent_id"], stratum["chart"])
            ]
            need(
                later_row["equation"] == "2*t^2-1=0"
                and later_row["face_classification"] == "FULL_BASE_UNIQUE_GRAPH"
                and later_row["exact_dimension"] == 2,
                f"exact source seam graph:{stratum_id}",
            )
            terminal = "MATERIALIZED_AS_CANONICAL_SUPPORT"
            detail = "ROUND179_FULL_BASE_UNIQUE_SOURCE_SEAM_GRAPH"
            support_kind = "CERTIFIED_PHYSICAL_FULL_BASE_UNIQUE_GRAPH"
            later_table = "ROUND179_SOURCE_CHART_SEAM"
            explicit_physical_support = 1

        elif label == "outgoing_chart_seam":
            need(residual_id in residual_by_id, f"outgoing origin:{stratum_id}")
            residual, _ = residual_by_id[residual_id]
            later_row, later_row_sha256 = outgoing_by_origin[residual_id]
            need(
                "outgoing_chart_seam" in residual["reason_labels"]
                and later_row["gradient_axis"] == "t"
                and later_row["regularity_certification"]
                == "CERTIFIED_STRICT_INTERVAL_DERIVATIVE",
                f"outgoing normal form:{stratum_id}",
            )
            later_table = "ROUND179_OUTGOING_NORMAL_FORM"
            if (residual_id, "outgoing_chart_seam") in absence_by_origin_reason:
                terminal = "ABSENT_ON_ALL_DESCENDANTS"
                detail = "ROUND179_STRICT_ZERO_ABSENT"
                support_kind = "STRICT_DESCENDANT_WIDE_ABSENCE"
            else:
                terminal = "MATERIALIZED_AS_CANONICAL_SUPPORT"
                detail = "ROUND179_" + later_row["face_classification"]
                support_kind = (
                    "CERTIFIED_PHYSICAL_FULL_BASE_UNIQUE_GRAPH"
                    if later_row["face_classification"]
                    == "FULL_BASE_UNIQUE_GRAPH"
                    else "NOMINAL_REGULAR_ZERO_SET_IF_PRESENT"
                )
                explicit_physical_support = int(
                    later_row["face_classification"]
                    == "FULL_BASE_UNIQUE_GRAPH"
                )

        elif label in {
            "integer_wall_endpoint",
            "integer_wall_crossing_endpoint",
        }:
            need(residual_id in residual_by_id, f"wall origin:{stratum_id}")
            residual, _ = residual_by_id[residual_id]
            prefix = (
                "wall_endpoint_or_count_transition:"
                if label == "integer_wall_endpoint"
                else "wall_crossing_time_not_strict:"
            )
            reasons: list[str] = []
            for reason in residual["reason_labels"]:
                if not reason.startswith(prefix):
                    continue
                _kind, axis, wall = reason.split(":")
                equation = (
                    f"(source_{axis.lower()}-{wall})*"
                    f"(target_{axis.lower()}-{wall})=0"
                    if label == "integer_wall_endpoint"
                    else f"alpha_{axis}_{wall}*(1-alpha_{axis}_{wall})=0"
                )
                if equation == stratum["equation"]:
                    reasons.append(reason)
            need(len(reasons) == 1, f"unique wall reason:{stratum_id}")
            reason = reasons[0]
            later_row, later_row_sha256 = wall_by_origin_reason[
                (residual_id, reason)
            ]
            _kind, axis, wall = reason.split(":")
            need(
                later_row["zero_equation"]
                == f"(source_{axis.lower()}-{wall})*"
                f"(target_{axis.lower()}-{wall})=0",
                f"Round179 wall factorization:{stratum_id}",
            )
            later_table = "ROUND179_WALL_NORMAL_FORM"
            if (residual_id, reason) in absence_by_origin_reason:
                terminal = "ABSENT_ON_ALL_DESCENDANTS"
                detail = "ROUND179_BOTH_FACTORS_STRICTLY_ZERO_ABSENT"
                support_kind = "STRICT_DESCENDANT_WIDE_ABSENCE"
            else:
                terminal = "MATERIALIZED_AS_CANONICAL_SUPPORT"
                detail = "ROUND179_" + later_row[
                    "zero_set_dimension_account"
                ]
                explicit_physical_support = int(
                    later_row["target_face_classification"]
                    == "FULL_BASE_UNIQUE_GRAPH"
                )
                support_kind = (
                    "CERTIFIED_PHYSICAL_TARGET_FULL_BASE_UNIQUE_GRAPH"
                    if explicit_physical_support
                    else "NOMINAL_REGULAR_FACTOR_UNION_IF_PRESENT"
                )

        elif label == "candidate_pair_intersection":
            need(residual_id in residual_by_id, f"pair origin:{stratum_id}")
            residual, _ = residual_by_id[residual_id]
            later_row, later_row_sha256 = pair_by_origin[residual_id]
            need(
                later_row["reason_labels"] == residual["reason_labels"]
                and later_row["predicate_count"] == 2
                and later_row["existence_certification"] == "NOT_CERTIFIED",
                f"pair arrangement candidate:{stratum_id}",
            )
            later_table = "ROUND179_PAIR_ARRANGEMENT_CANDIDATE"
            if any(
                (residual_id, reason) in absence_by_origin_reason
                for reason in residual["reason_labels"]
            ):
                terminal = "ABSENT_ON_ALL_DESCENDANTS"
                detail = "CONSTITUENT_NORMAL_FORM_STRICTLY_ABSENT"
                support_kind = "STRICT_CONSTITUENT_ABSENCE"
            else:
                terminal = "MATERIALIZED_AS_CANONICAL_SUPPORT"
                detail = "ROUND179_NOMINAL_PAIR_ARRANGEMENT_CANDIDATE"
                support_kind = "NOMINAL_PAIR_CANDIDATE_IF_TRANSVERSE"

        else:
            raise Round267Error(f"unknown stratum predicate:{label}")

        physical_existence_credit = explicit_physical_support
        nominal_support_only = (
            terminal == "MATERIALIZED_AS_CANONICAL_SUPPORT"
            and physical_existence_credit == 0
        )
        later_row_id = (
            later_row["row_id"]
            if "row_id" in later_row
            else later_row["stratum_id"]
        )
        terminal_histogram[terminal] += 1
        detail_histogram[detail] += 1
        support_kind_histogram[support_kind] += 1
        projection = {
            "Round174_stratum_id": stratum_id,
            "predicate_label": label,
            "terminal_lineage_status": terminal,
            "canonical_support_or_absence_row_id": later_row_id,
            "support_or_absence_detail": detail,
            "physical_existence_credit": physical_existence_credit,
            "maximality_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }
        projection_rows.append(projection)
        lineage_rows.append(closed({
            "lower_stratum_terminal_lineage_row_id":
                "round267-lower-stratum-lineage:" + digest([stratum_id]),
            "Round174_stratum_id": stratum_id,
            "Round174_stratum_packed_row_sha256": stratum_sha256,
            "source_chart": stratum["chart"],
            "parent_id": stratum["parent_id"],
            "containing_Round174_residual_row_id": residual_id,
            "predicate_label": label,
            "predicate_equation": stratum["equation"],
            "Round174_dimension_account": stratum["dimension_account"],
            "Round174_dimension_certification":
                stratum["dimension_certification"],
            "Round174_existence_certification":
                stratum["existence_certification"],
            "Round174_half_open_owner_status":
                stratum["half_open_owner_status"],
            "terminal_lineage_status": terminal,
            "canonical_support_or_absence_source_table": later_table,
            "canonical_support_or_absence_row_id": later_row_id,
            "canonical_support_or_absence_packed_row_sha256":
                later_row_sha256,
            "support_or_absence_detail": detail,
            "canonical_support_kind": support_kind,
            "nominal_support_only": nominal_support_only,
            "physical_existence_credit": physical_existence_credit,
            "descendant_wide_absence_credit":
                int(terminal == "ABSENT_ON_ALL_DESCENDANTS"),
            "three_dimensional_volume_credit": 0,
            "quotient_component_edge_credit": 0,
            "maximality_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))

    need(
        len(lineage_rows)
        == len({row["Round174_stratum_id"] for row in lineage_rows})
        == 62_696,
        "complete unique lower-stratum lineage",
    )
    need(
        dict(sorted(predicate_histogram.items()))
        == EXPECTED_PREDICATE_HISTOGRAM,
        "predicate histogram",
    )
    need(
        dict(sorted(terminal_histogram.items()))
        == EXPECTED_TERMINAL_HISTOGRAM,
        "terminal histogram",
    )
    need(
        dict(sorted(detail_histogram.items())) == EXPECTED_DETAIL_HISTOGRAM,
        "support/absence detail histogram",
    )
    need(
        digest(projection_rows) == EXPECTED_PROBE_PROJECTION_SHA256,
        "independent probe projection digest:" + digest(projection_rows),
    )
    need(
        sum(row["physical_existence_credit"] for row in projection_rows)
        == 1_148
        and sum(
            row["terminal_lineage_status"]
            == "MATERIALIZED_AS_CANONICAL_SUPPORT"
            and row["physical_existence_credit"] == 0
            for row in projection_rows
        ) == 55_428,
        "physical versus nominal support census",
    )

    del (
        round179,
        residual_by_id,
        origin_by_id,
        outgoing_by_origin,
        wall_by_origin_reason,
        seam_by_parent_chart,
        pair_by_origin,
        stratum_pairs,
        origin_pairs,
        outgoing_pairs,
        wall_pairs,
        seam_pairs,
        pair_pairs,
    )
    gc.collect()

    # The lineage audit above is independently executable while Round266 is
    # being frozen.  Formal certificate production remains fail-closed here
    # until the centralized adapter carries real immutable pins.
    need(
        ROUND266_FILE_SHA256 != "0" * 64
        and ROUND266_RESULT_SHA256 != "0" * 64
        and ROUND266_SCHEMA
        == "cm2.round266.source-g-expanded-curved-face-closure.v1",
        "Round266 freeze adapter is still pending",
    )
    round266 = load_result(ROUND266_CERTIFICATE)
    need(
        round266["census"]["post_Round266_component_count"] == 63_224
        and round266["census"]["complete_occurrence_frontier_count"] == 126_468
        and round266["census"]["complete_valid_virtual_node_frontier_count"]
        == 133_284
        and round266["census"]["complete_exact_key_frontier_count"] == 116
        and round266["census"][
            "complete_explicit_component_member_frontier_count"
        ] == 259_752
        and round266["strict_nonpromotion"][
            "maximal_physical_component_assignments"
        ] == "0/63224"
        and round266["strict_nonpromotion"][
            "globally_exhausted_exact_key_fibres"
        ] == "0/116"
        and round266["strict_nonpromotion"][
            "source_G_global_exact_key_dispositions"
        ] == "0/224580"
        and round266["scope_contract"]["Jx_Jy_same_point_glue_credit"] == 0
        and round266["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round266 frozen quotient and strict nonpromotion",
    )
    identity_rows = [
        frontier_identity_row(round266, *specification)
        for specification in ROUND266_FRONTIERS
    ]

    census = {
        "Round174_lower_dimensional_stratum_count": 62_696,
        "predicate_histogram": dict(sorted(predicate_histogram.items())),
        "terminal_lineage_status_histogram":
            dict(sorted(terminal_histogram.items())),
        "support_or_absence_detail_histogram":
            dict(sorted(detail_histogram.items())),
        "canonical_support_kind_histogram":
            dict(sorted(support_kind_histogram.items())),
        "descendant_wide_absent_stratum_count": 6_120,
        "canonical_support_lineage_count": 56_576,
        "certified_physical_existence_count": 1_148,
        "nominal_support_without_physical_existence_credit_count": 55_428,
        "canonical_support_exact_key_occurrence_credit": 0,
        "positive_volume_chart_guard_rows_still_requiring_reverse_rechart": 880,
        "probe_projection_rows_sha256": digest(projection_rows),
        "post_Round266_component_count": 63_224,
        "post_Round267_component_count": 63_224,
        "expanded_occurrence_frontier_count": 126_468,
        "exact_key_frontier_count": 116,
        "valid_virtual_node_frontier_count": 133_284,
        "explicit_component_member_frontier_count": 259_752,
        "quotient_component_edge_credit": 0,
        "maximal_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }

    return {
        "status": (
            "CERTIFIED_COMPLETE_62696_ROUND174_LOWER_STRATUM_TERMINAL_"
            "LINEAGE__6120_DESCENDANT_WIDE_ABSENT__56576_CANONICAL_"
            "SUPPORTS_WITHOUT_NOMINAL_EXISTENCE_PROMOTION__ROUND266_"
            "QUOTIENT_AND_FRONTIERS_UNCHANGED"
        ),
        "formal_input_binding": input_binding(),
        "formal_Round174_lower_stratum_terminal_lineage_ledger": ledger(
            lineage_rows,
            "lower_stratum_terminal_lineage_row_id",
        ),
        "formal_Round266_to_Round267_quotient_and_frontier_identity_ledger":
            ledger(
                identity_rows,
                "Round266_to_Round267_frontier_identity_row_id",
            ),
        "census": census,
        "scope_contract": {
            "all_62696_Round174_lower_dimensional_rows_have_unique_terminal_lineage":
                True,
            "all_62012_Round174_residual_tubes_match_Round179_origins_exactly":
                True,
            "all_terminal_lineages_are_canonical_support_or_descendant_wide_absence":
                True,
            "nominal_regular_if_present_support_is_not_physical_existence":
                True,
            "nominal_pair_candidate_if_transverse_is_not_physical_existence":
                True,
            "only_Round174_certified_grazing_faces_and_Round179_explicit_full_base_graphs_receive_physical_existence_credit":
                True,
            "Round179_source_factor_regular_graph_overwrap_without_full_base_existence_remains_nominal":
                True,
            "all_56576_canonical_support_lineages_are_not_by_themselves_exact_key_occurrences":
                True,
            "Round174_Round179_positive_volume_chart_guards_are_not_outside_or_global_dispositions":
                True,
            "lower_stratum_lineage_is_quotient_neutral": True,
            "Round266_component_occurrence_key_and_virtual_frontiers_preserved":
                True,
            "component_maximality_not_proved": True,
            "exact_key_fibre_exhaustion_not_proved": True,
            "Jx_Jy_are_not_same_point_glue_generators": True,
        },
        "strict_nonpromotion": {
            "new_physical_glue_credit": 0,
            "new_component_union_credit": 0,
            "nominal_support_physical_existence_credit": 0,
            "canonical_support_exact_key_occurrence_credit": 0,
            "positive_volume_chart_guard_global_disposition_credit": 0,
            "Round182_source_seam_owner_shadow_candidate_global_disposition_credit":
                0,
            "Jx_Jy_same_point_glue_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "audit the Round182 closed-collar descendant materialization of "
            "these terminal supports, including 152 positive-area source-"
            "seam owner/shadow candidates; reverse-rechart all 880 positive-"
            "volume Round174/Round179 chart guards before any outside or "
            "global-disposition credit; only then consider exact-key "
            "occurrence/maximality promotion and exhaust all 116 fibres"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "upstream_producer_imported_or_executed": False,
            "arithmetic": "exact symbolic row identity and canonical SHA256",
            "seed_affects_output": False,
            "Round266_freeze_adapter_pending_at_initial_skeleton_creation":
                False,
        },
    }


def safe_write(data: bytes) -> None:
    need(OUTPUT.parent == HERE, "output parent")
    if OUTPUT.exists() or OUTPUT.is_symlink():
        information = OUTPUT.lstat()
        need(
            stat.S_ISREG(information.st_mode)
            and not OUTPUT.is_symlink()
            and information.st_nlink == 1,
            "safe existing output",
        )
    descriptor, name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.",
        suffix=".tmp",
        dir=HERE,
    )
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
        directory_descriptor = os.open(
            HERE,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def value_at(root: Any, path: tuple[Any, ...]) -> Any:
    value = root
    for key in path:
        value = value[key]
    return value


def replace_at(root: Any, path: tuple[Any, ...], replacement: Any) -> None:
    value = root
    for key in path[:-1]:
        value = value[key]
    value[path[-1]] = replacement


def semantic_attack_suite(candidate: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    """Reject result-level-resigned corruptions without copying huge ledgers."""
    attacks: list[tuple[str, tuple[Any, ...], Any]] = [
        ("promote_maximality", ("census", "maximal_component_assignment_count"), 1),
        ("promote_fibre", ("census", "globally_exhausted_exact_key_fibre_count"), 1),
        ("promote_disposition", ("census", "global_exact_key_disposition_count"), 1),
        ("grant_component_edge", ("census", "quotient_component_edge_credit"), 1),
        ("alter_absence_census", ("census", "descendant_wide_absent_stratum_count"), 6119),
        ("alter_support_census", ("census", "canonical_support_lineage_count"), 56575),
        ("alter_physical_existence", ("census", "certified_physical_existence_count"), 1149),
        ("grant_nominal_existence", ("strict_nonpromotion", "nominal_support_physical_existence_credit"), 1),
        ("grant_key_occurrence", ("strict_nonpromotion", "canonical_support_exact_key_occurrence_credit"), 1),
        ("grant_jx_jy_glue", ("strict_nonpromotion", "Jx_Jy_same_point_glue_credit"), 1),
        ("promote_cm2", ("strict_nonpromotion", "CM2"), "GO_FOR_CLAIM"),
        ("forge_probe_digest", ("census", "probe_projection_rows_sha256"), "0" * 64),
        ("change_required_next", ("required_next",), "done"),
        ("forge_status", ("status",), "CERTIFIED_MAXIMAL"),
        ("forge_producer_pin", ("provenance", "producer_sha256"), "0" * 64),
        ("claim_seed_dependence", ("provenance", "seed_affects_output"), True),
    ]
    rejected: list[str] = []
    for label, path, replacement in attacks:
        original = value_at(candidate, path)
        replace_at(candidate, path, replacement)
        resigned = digest(candidate)
        need(resigned != CANDIDATE_RESULT_SHA256, f"attack changes digest:{label}")
        need(candidate != expected, f"attack rejected:{label}")
        replace_at(candidate, path, original)
        need(candidate == expected, f"attack restoration:{label}")
        rejected.append(label)
    return {
        "attack_count": len(rejected),
        "all_result_level_resigned_semantic_attacks_rejected": True,
        "attack_labels": rejected,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=267_929)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    need(isinstance(arguments.seed, int) and not isinstance(arguments.seed, bool), "integral seed")

    producer_raw = regular_bytes(PRODUCER, 5_000_000)
    need(hashlib.sha256(producer_raw).hexdigest() == PRODUCER_SHA256, "producer pin")
    expected = build(PRODUCER_SHA256)
    need(digest(expected) == CANDIDATE_RESULT_SHA256, "independent expected result pin")

    candidate_raw = regular_bytes(CANDIDATE)
    need(len(candidate_raw) == CANDIDATE_SIZE, "candidate size pin")
    need(hashlib.sha256(candidate_raw).hexdigest() == CANDIDATE_SHA256, "candidate file pin")
    candidate = strict_json(candidate_raw, CANDIDATE.name)
    need(set(candidate) == {"schema", "result", "result_sha256"}, "candidate envelope")
    need(candidate["schema"] == SCHEMA, "candidate schema")
    need(candidate["result_sha256"] == CANDIDATE_RESULT_SHA256, "candidate result pin")
    need(digest(candidate["result"]) == CANDIDATE_RESULT_SHA256, "candidate result closure")
    need(candidate["result"] == expected, "complete independent result equality")

    attacks = semantic_attack_suite(candidate["result"], expected)
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": "PASS_INDEPENDENT_ROUND267",
        "candidate_sha256": CANDIDATE_SHA256,
        "candidate_result_sha256": CANDIDATE_RESULT_SHA256,
        "producer_sha256": PRODUCER_SHA256,
        "independent_reconstruction": {
            "producer_imported_or_executed": False,
            "complete_Round174_lower_stratum_rows_rebuilt": 62_696,
            "complete_terminal_lineage_rows_rebuilt": 62_696,
            "complete_Round266_frontier_identity_rows_rebuilt": 582_844,
            "post_Round267_component_count": 63_224,
            "expanded_occurrence_frontier_count": 126_468,
            "exact_key_frontier_count": 116,
            "valid_virtual_node_frontier_count": 133_284,
            "quotient_and_frontiers_unchanged": True,
        },
        "semantic_attack_suite": attacks,
        "strict_nonpromotion": expected["strict_nonpromotion"],
        "seed_affects_output": False,
    }
    encoded = canonical(verification) + b"\n"
    if not arguments.no_write:
        safe_write(encoded)
    print(verification["status"])
    print(f"verification_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"attacks_rejected={attacks['attack_count']}/{attacks['attack_count']}")
    print("producer_imported_or_executed=false quotient_unchanged=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
