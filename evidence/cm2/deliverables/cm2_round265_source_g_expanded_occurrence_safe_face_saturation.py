#!/usr/bin/env python3
"""Expand the Source-G occurrence universe and saturate its safe box faces.

Round264 freezes a corrected 68,312-component quotient carrying 53,968
local occurrences and 133,284 valid virtual strata.  Round174 independently
materializes 72,500 further positive-open 3D occurrences.  This producer
adds those rows as initially separate seeds, reconstructs the resulting
126,468-occurrence universe, and exhaustively enumerates every positive-area
same-key, same-source-chart box-face contact involving a Round174 row.

A physical face edge is admitted only when all ten fields of the local
return signature agree.  This is strictly stronger than key equality.
Resolved Round174--Round174 and Round174--Round179 box contacts then have
an exact positive-area common patch with strict open 3D corridors on both
sides.  The 169,064 such faces supply 77,000 rank reductions.  Contacts
involving Round204/Round208 graph-side regions remain fail-closed until an
exact curved two-sided corridor proof is supplied.  Same-key contacts whose
ten-field signatures differ are explicit non-edges.

The producer rebuilds the complete component, occurrence, exact-key, seed,
and valid-virtual-node frontiers.  It does not import or execute an upstream
producer and grants no maximality, fibre-exhaustion, global-disposition,
Gate5, D02, Jx/Jy same-point-glue, or CM2 credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
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
PREFIX = "cm2_round265_source_g_expanded_occurrence_safe_face_saturation"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round265.source-g-expanded-occurrence-safe-face-saturation.v1"

ROUND174_CERTIFICATE = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_"
    "materialization_certificate.json"
)
ROUND174_ROWS = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_"
    "materialization_rows.json"
)
ROUND179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
ROUND204_CERTIFICATE = (
    "cm2_round204_source_g_wall_return_signature_local_replacement_"
    "certificate.json"
)
ROUND208_CERTIFICATE = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization_"
    "certificate.json"
)
ROUND264_CERTIFICATE = (
    "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_"
    "glue_closure_certificate.json"
)

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
    ROUND179_ROWS: (
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
        "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb",
        "cm2.round179.source-g-residual-tube-arrangement-rows.v1",
    ),
    ROUND204_CERTIFICATE: (
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
        "ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd",
        "cm2.round204.source-g-wall-return-signature-local-replacement.v1",
    ),
    ROUND208_CERTIFICATE: (
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
        "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8",
        "cm2.round208.source-g-outgoing-direct-signature-materialization.v1",
    ),
    ROUND264_CERTIFICATE: (
        "ac9e9451e12621fd236fea39bc686e13b41ade62e5255de9c9cd98230763236f",
        "712a4eeae512e6370c642635a6d80090c15789612cb1745d0844282cc02f9ae1",
        "cm2.round264.source-g-lower-dimensional-endpoint-correction-and-glue-closure.v1",
    ),
}

SIGNATURE_FIELDS = (
    "official_key_id",
    "official_key_ordinal",
    "official_key_row",
    "ordered_integer_wall_events",
    "outgoing_cell",
    "roof",
    "signed_wall_word",
    "source_chart",
    "target_chart",
    "target_lift",
)
AXIS_NAMES = ("t", "p", "s")
EXPECTED_SOURCE_COUNTS = {
    "ROUND174_RESOLVED": 72_500,
    "ROUND179_RESOLVED": 17_192,
    "ROUND204_REGION": 736,
    "ROUND208_REGION": 36_040,
}
EXPECTED_FULL_SIGNATURE_FACE_HISTOGRAM = {
    "ROUND174_RESOLVED|ROUND174_RESOLVED": 138_412,
    "ROUND174_RESOLVED|ROUND179_RESOLVED": 30_652,
    "ROUND174_RESOLVED|ROUND204_REGION": 96,
    "ROUND174_RESOLVED|ROUND208_REGION": 2_556,
}
EXPECTED_SAFE_AXIS_HISTOGRAM = {
    "p:ROUND174_RESOLVED|ROUND174_RESOLVED": 60_200,
    "p:ROUND174_RESOLVED|ROUND179_RESOLVED": 13_080,
    "s:ROUND174_RESOLVED|ROUND174_RESOLVED": 16_152,
    "s:ROUND174_RESOLVED|ROUND179_RESOLVED": 3_220,
    "t:ROUND174_RESOLVED|ROUND174_RESOLVED": 62_060,
    "t:ROUND174_RESOLVED|ROUND179_RESOLVED": 14_352,
}
EXPECTED_CURVED_AXIS_HISTOGRAM = {
    "p:ROUND174_RESOLVED|ROUND204_REGION": 32,
    "p:ROUND174_RESOLVED|ROUND208_REGION": 1_796,
    "t:ROUND174_RESOLVED|ROUND204_REGION": 64,
    "t:ROUND174_RESOLVED|ROUND208_REGION": 760,
}


class Round265Error(RuntimeError):
    """A fail-closed Round265 contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round265Error(label)


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


def qtext(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


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
        raise Round265Error(f"non-integral JSON number:{label}:{token}")

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_float=reject,
            parse_constant=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Round265Error(f"strict JSON:{label}") from error
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
) -> Iterable[tuple[dict[str, Any], str]]:
    census = result["table_census_and_sha256"][table]
    rows = result[table]
    columns = result["row_column_schemas"][table]
    need(
        census["row_count"] == len(rows) == expected_count
        and census["rows_sha256"] == digest(rows)
        and len(columns) == len(set(columns)),
        f"packed table contract:{table}",
    )
    for packed in rows:
        need(len(packed) == len(columns), f"packed row width:{table}")
        yield dict(zip(columns, packed, strict=True)), digest(packed)


def input_binding() -> dict[str, Any]:
    return {
        name: {
            "file_sha256": values[0],
            "result_sha256": values[1],
            "schema": values[2],
        }
        for name, values in sorted(INPUTS.items())
    }


def exact_box(values: Any, label: str) -> tuple[Fraction, ...]:
    need(
        isinstance(values, list)
        and len(values) == 6
        and all(isinstance(value, str) for value in values),
        f"exact box:{label}",
    )
    try:
        box = tuple(Fraction(value) for value in values)
    except (ValueError, ZeroDivisionError) as error:
        raise Round265Error(f"exact rational box:{label}") from error
    need(
        all(box[2 * axis] < box[2 * axis + 1] for axis in range(3)),
        f"positive box:{label}",
    )
    return box


def make_signature(
    *,
    official_key_id: str,
    official_key_ordinal: int,
    official_key_row: Any,
    ordered_integer_wall_events: Any,
    outgoing_cell: str,
    roof: int,
    signed_wall_word: Any,
    source_chart: str,
    target_chart: str,
    target_lift: str,
) -> dict[str, Any]:
    signature = {
        "official_key_id": official_key_id,
        "official_key_ordinal": official_key_ordinal,
        "official_key_row": official_key_row,
        "ordered_integer_wall_events": ordered_integer_wall_events,
        "outgoing_cell": outgoing_cell,
        "roof": roof,
        "signed_wall_word": signed_wall_word,
        "source_chart": source_chart,
        "target_chart": target_chart,
        "target_lift": target_lift,
    }
    need(tuple(sorted(signature)) == tuple(sorted(SIGNATURE_FIELDS)), "signature fields")
    return signature


def add_occurrence(
    occurrences: list[dict[str, Any]],
    occurrence_ids: set[str],
    *,
    occurrence_id: str,
    source: str,
    signature: dict[str, Any],
    box_values: list[str],
    vertex: str,
    source_row_id: str,
    source_row_sha256: str,
    round264_row: dict[str, Any] | None,
) -> None:
    need(occurrence_id not in occurrence_ids, f"unique occurrence:{occurrence_id}")
    need(set(signature) == set(SIGNATURE_FIELDS), f"complete signature:{occurrence_id}")
    need(
        signature["source_chart"] in {"G:E", "G:N", "G:S", "G:W"}
        and isinstance(signature["official_key_id"], str)
        and isinstance(signature["official_key_ordinal"], int)
        and not isinstance(signature["official_key_ordinal"], bool),
        f"signature types:{occurrence_id}",
    )
    box = exact_box(box_values, occurrence_id)
    signature_bytes = canonical(signature)
    occurrence_ids.add(occurrence_id)
    occurrences.append({
        "id": occurrence_id,
        "source": source,
        "signature": signature,
        "signature_bytes": signature_bytes,
        "signature_sha256": hashlib.sha256(signature_bytes).hexdigest(),
        "key_id": signature["official_key_id"],
        "key_ordinal": signature["official_key_ordinal"],
        "chart": signature["source_chart"],
        "box": box,
        "box_text": list(box_values),
        "vertex": vertex,
        "source_row_id": source_row_id,
        "source_row_sha256": source_row_sha256,
        "round264_row": round264_row,
    })


class DSU:
    def __init__(self, members: Iterable[str]) -> None:
        values = list(members)
        self.parent = {value: value for value in values}
        self.size = {value: 1 for value in values}

    def find(self, value: str) -> str:
        need(value in self.parent, f"DSU member:{value}")
        root = value
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[value] != value:
            parent = self.parent[value]
            self.parent[value] = root
            value = parent
        return root

    def union(self, left: str, right: str) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        if (
            self.size[left_root] < self.size[right_root]
            or (
                self.size[left_root] == self.size[right_root]
                and left_root > right_root
            )
        ):
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        self.size[left_root] += self.size[right_root]
        return True


def common_face_geometry(
    negative: dict[str, Any],
    positive: dict[str, Any],
    axis: int,
    coordinate: Fraction,
) -> dict[str, Any]:
    negative_box = negative["box"]
    positive_box = positive["box"]
    need(
        negative_box[2 * axis + 1] == coordinate
        and positive_box[2 * axis] == coordinate,
        "opposite face orientation",
    )
    tangential_axes = [value for value in range(3) if value != axis]
    rectangle: list[Fraction] = []
    exact_equal = True
    area = Fraction(1)
    for tangent in tangential_axes:
        negative_interval = negative_box[2 * tangent:2 * tangent + 2]
        positive_interval = positive_box[2 * tangent:2 * tangent + 2]
        lower = max(negative_interval[0], positive_interval[0])
        upper = min(negative_interval[1], positive_interval[1])
        need(lower < upper, "positive tangential face width")
        rectangle.extend((lower, upper))
        area *= upper - lower
        exact_equal = exact_equal and negative_interval == positive_interval
    negative_volume = area * (coordinate - negative_box[2 * axis])
    positive_volume = area * (positive_box[2 * axis + 1] - coordinate)
    need(
        area > 0 and negative_volume > 0 and positive_volume > 0,
        "strict two-sided box corridors",
    )
    return {
        "face_axis": AXIS_NAMES[axis],
        "shared_face_coordinate": qtext(coordinate),
        "tangential_axes": [AXIS_NAMES[value] for value in tangential_axes],
        "exact_positive_2D_common_face_rectangle":
            [qtext(value) for value in rectangle],
        "exact_positive_2D_common_face_area": qtext(area),
        "negative_side_strict_3D_corridor_volume": qtext(negative_volume),
        "positive_side_strict_3D_corridor_volume": qtext(positive_volume),
        "face_relation":
            "EXACT_EQUAL_FACE" if exact_equal else "POSITIVE_AREA_PARTIAL_REFINEMENT",
        "_area": area,
        "_negative_volume": negative_volume,
        "_positive_volume": positive_volume,
    }


def build(producer_sha256: str) -> dict[str, Any]:
    # The Round174 summary pins the complete rows attachment and preserves its
    # deliberately bounded, non-maximal scope.
    round174_certificate = load_result(ROUND174_CERTIFICATE)
    materialization = round174_certificate["materialization_census"]
    attachment = round174_certificate["row_attachment"]
    need(
        materialization["resolved_3d_occurrence_row_count"] == 72_500
        and materialization["observed_exact_key_count"] == 116
        and materialization["volume_conservation_exact"] is True
        and attachment["file_sha256"] == INPUTS[ROUND174_ROWS][0]
        and attachment["result_sha256"] == INPUTS[ROUND174_ROWS][1]
        and attachment["full_attachment_rows_materialized"] is True
        and round174_certificate["scope"]["all_unique_first_parents_fully_materialized"] is False
        and round174_certificate["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round174 bounded materialization precondition",
    )
    del round174_certificate
    gc.collect()

    # Extract the complete corrected Round264 frontier, including all valid
    # virtual nodes, before loading geometry-heavy occurrence tables.
    round264 = load_result(ROUND264_CERTIFICATE)
    need(
        round264["census"]["post_Round264_component_count"] == 68_312
        and round264["census"]["complete_occurrence_frontier_count"] == 53_968
        and round264["census"]["complete_exact_key_frontier_count"] == 116
        and round264["census"]["complete_valid_virtual_node_frontier_count"] == 133_284
        and round264["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round264 corrected frontier precondition",
    )
    component_rows264 = check_closed_rows(
        round264["formal_post_Round264_component_frontier_ledger"],
        "post_Round264_component_frontier_row_id",
        68_312,
    )
    base_components = {
        row["post_Round264_quotient_component_id"]: {
            "official_key_id": row["official_key_id"],
            "official_key_ordinal": row["official_key_ordinal"],
            "source_row_id": row["post_Round264_component_frontier_row_id"],
            "source_row_sha256": row["row_sha256"],
        }
        for row in component_rows264
    }
    need(len(base_components) == 68_312, "unique Round264 components")
    occurrence_rows264 = check_closed_rows(
        round264["formal_post_Round264_occurrence_frontier_ledger"],
        "post_Round264_occurrence_frontier_row_id",
        53_968,
    )
    base_occurrences = {
        row["local_occurrence_row_id"]: {
            "official_key_id": row["official_key_id"],
            "official_key_ordinal": row["official_key_ordinal"],
            "current_component_id": row["post_Round264_quotient_component_id"],
            "source_row_id": row["post_Round264_occurrence_frontier_row_id"],
            "source_row_sha256": row["row_sha256"],
        }
        for row in occurrence_rows264
    }
    need(len(base_occurrences) == 53_968, "unique Round264 occurrence frontier")
    key_rows264 = check_closed_rows(
        round264["formal_post_Round264_key_frontier_ledger"],
        "post_Round264_key_frontier_row_id",
        116,
    )
    base_keys = {
        row["official_key_id"]: {
            "official_key_ordinal": row["official_key_ordinal"],
            "component_count": row["post_Round264_quotient_component_count"],
            "occurrence_count": row["local_occurrence_count"],
            "valid_virtual_count": row["valid_virtual_stratum_node_count"],
            "source_row_id": row["post_Round264_key_frontier_row_id"],
            "source_row_sha256": row["row_sha256"],
        }
        for row in key_rows264
    }
    need(len(base_keys) == 116, "unique Round264 key frontier")
    virtual_rows264 = check_closed_rows(
        round264["formal_post_Round264_valid_virtual_node_frontier_ledger"],
        "post_Round264_valid_virtual_node_frontier_row_id",
        133_284,
    )
    base_virtual = [
        {
            "node_id": row["valid_virtual_stratum_node_id"],
            "kind": row["virtual_node_kind"],
            "current_component_id": row["post_Round264_quotient_component_id"],
            "official_key_id": row["official_key_id"],
            "source_row_id":
                row["post_Round264_valid_virtual_node_frontier_row_id"],
            "source_row_sha256": row["row_sha256"],
        }
        for row in virtual_rows264
    ]
    need(
        len({row["node_id"] for row in base_virtual}) == 133_284,
        "unique Round264 valid virtual nodes",
    )
    del (
        round264,
        component_rows264,
        occurrence_rows264,
        key_rows264,
        virtual_rows264,
    )
    gc.collect()

    occurrences: list[dict[str, Any]] = []
    occurrence_ids: set[str] = set()

    # Add all 72,500 newly admitted Round174 positive-open 3D rows.
    round174_rows = load_result(ROUND174_ROWS)
    for row, row_sha256 in packed_rows(
        round174_rows,
        "resolved_3d_occurrence_rows",
        72_500,
    ):
        need(
            row["ambient_dimension"] == 3
            and row["physical_open_subset_positive"] is True
            and Fraction(row["coordinate_volume"]) > 0,
            f"Round174 positive-open row:{row['row_id']}",
        )
        signature = make_signature(
            official_key_id=row["official_key_id"],
            official_key_ordinal=row["official_key_ordinal"],
            official_key_row=row["official_key_row"],
            ordered_integer_wall_events=row["ordered_integer_wall_events"],
            outgoing_cell=row["outgoing_cell"],
            roof=row["roof"],
            signed_wall_word=row["signed_wall_word"],
            source_chart=row["chart"],
            target_chart=row["target_chart"],
            target_lift=row["owner_target"],
        )
        add_occurrence(
            occurrences,
            occurrence_ids,
            occurrence_id=row["row_id"],
            source="ROUND174_RESOLVED",
            signature=signature,
            box_values=row["box"],
            vertex=row["row_id"],
            source_row_id=row["row_id"],
            source_row_sha256=row_sha256,
            round264_row=None,
        )
    del round174_rows
    gc.collect()

    # Reconstruct every prior occurrence's exact box and ten-field signature.
    round179 = load_result(ROUND179_ROWS)
    for row, row_sha256 in packed_rows(
        round179,
        "resolved_3d_child_rows",
        17_192,
    ):
        need(row["row_id"] in base_occurrences, f"Round179 Round264 binding:{row['row_id']}")
        binding = base_occurrences[row["row_id"]]
        signature = make_signature(
            official_key_id=row["official_key_id"],
            official_key_ordinal=row["official_key_ordinal"],
            official_key_row=row["official_key_row"],
            ordered_integer_wall_events=row["ordered_integer_wall_events"],
            outgoing_cell=row["outgoing_cell"],
            roof=row["roof"],
            signed_wall_word=row["signed_wall_word"],
            source_chart=row["chart"],
            target_chart=row["target_chart"],
            target_lift=row["owner_target"],
        )
        need(
            binding["official_key_id"] == signature["official_key_id"]
            and binding["official_key_ordinal"] == signature["official_key_ordinal"],
            f"Round179 exact-key cross-binding:{row['row_id']}",
        )
        add_occurrence(
            occurrences,
            occurrence_ids,
            occurrence_id=row["row_id"],
            source="ROUND179_RESOLVED",
            signature=signature,
            box_values=row["box"],
            vertex=binding["current_component_id"],
            source_row_id=row["row_id"],
            source_row_sha256=row_sha256,
            round264_row=binding,
        )
    del round179
    gc.collect()

    round204 = load_result(ROUND204_CERTIFICATE)
    rows204 = check_closed_rows(
        round204["formal_local_open_3D_region_ledger"],
        "region_row_id",
        736,
    )
    for row in rows204:
        occurrence_id = row["region_row_id"]
        need(
            occurrence_id in base_occurrences
            and row["ambient_dimension"] == 3
            and row["strict_open_region"] is True
            and row["positive_coordinate_volume"] is True,
            f"Round204 positive-open binding:{occurrence_id}",
        )
        binding = base_occurrences[occurrence_id]
        signature = make_signature(
            official_key_id=row["official_key_id"],
            official_key_ordinal=row["official_key_ordinal"],
            official_key_row=row["official_key_row"],
            ordered_integer_wall_events=row["ordered_integer_wall_events"],
            outgoing_cell=row["outgoing_cell"],
            roof=row["roof"],
            signed_wall_word=row["signed_wall_word"],
            source_chart=row["chart"],
            target_chart=row["target_chart"],
            target_lift=row["owner_target"],
        )
        need(
            binding["official_key_id"] == signature["official_key_id"]
            and binding["official_key_ordinal"] == signature["official_key_ordinal"],
            f"Round204 exact-key cross-binding:{occurrence_id}",
        )
        add_occurrence(
            occurrences,
            occurrence_ids,
            occurrence_id=occurrence_id,
            source="ROUND204_REGION",
            signature=signature,
            box_values=row["leaf_exact_box"],
            vertex=binding["current_component_id"],
            source_row_id=occurrence_id,
            source_row_sha256=row["row_sha256"],
            round264_row=binding,
        )
    del round204, rows204
    gc.collect()

    round208 = load_result(ROUND208_CERTIFICATE)
    rows208 = check_closed_rows(
        round208["formal_local_open_3D_signature_ledger"],
        "region_row_id",
        36_040,
    )
    for row in rows208:
        occurrence_id = row["region_row_id"]
        signature = row["local_return_signature"]
        need(
            occurrence_id in base_occurrences
            and row["strict_open_3D_region_exists"] is True
            and row["formal_local_open_3D_signature_credit"] == 1
            and set(signature) == set(SIGNATURE_FIELDS),
            f"Round208 positive-open binding:{occurrence_id}",
        )
        binding = base_occurrences[occurrence_id]
        need(
            binding["official_key_id"] == signature["official_key_id"]
            and binding["official_key_ordinal"] == signature["official_key_ordinal"],
            f"Round208 exact-key cross-binding:{occurrence_id}",
        )
        add_occurrence(
            occurrences,
            occurrence_ids,
            occurrence_id=occurrence_id,
            source="ROUND208_REGION",
            signature=signature,
            box_values=row["Round182_leaf_box"],
            vertex=binding["current_component_id"],
            source_row_id=occurrence_id,
            source_row_sha256=row["row_sha256"],
            round264_row=binding,
        )
    del round208, rows208
    gc.collect()

    source_counts = Counter(row["source"] for row in occurrences)
    need(dict(sorted(source_counts.items())) == EXPECTED_SOURCE_COUNTS, "occurrence source census")
    need(len(occurrences) == 126_468, "expanded occurrence universe")
    prior_occurrence_ids = {
        row["id"] for row in occurrences if row["source"] != "ROUND174_RESOLVED"
    }
    need(prior_occurrence_ids == set(base_occurrences), "complete Round264 occurrence reconstruction")
    need(
        {row["key_id"] for row in occurrences} == set(base_keys),
        "complete exact-key universe",
    )

    # Exhaustively enumerate same-key, same-chart positive-area box faces.
    # Each group carries positive-side boxes by LOWER face and negative-side
    # boxes by UPPER face.
    face_groups: dict[
        tuple[str, str, int, Fraction],
        list[list[int]],
    ] = defaultdict(lambda: [[], []])
    for index, row in enumerate(occurrences):
        box = row["box"]
        for axis in range(3):
            face_groups[(row["key_id"], row["chart"], axis, box[2 * axis])][0].append(index)
            face_groups[(row["key_id"], row["chart"], axis, box[2 * axis + 1])][1].append(index)

    safe_raw: list[dict[str, Any]] = []
    curved_raw: list[dict[str, Any]] = []
    mismatch_raw: list[dict[str, Any]] = []
    same_key_pair_histogram: Counter[str] = Counter()
    full_signature_pair_histogram: Counter[str] = Counter()
    safe_axis_histogram: Counter[str] = Counter()
    curved_axis_histogram: Counter[str] = Counter()
    mismatch_axis_histogram: Counter[str] = Counter()
    relation_histogram: Counter[str] = Counter()
    safe_area_sum = Fraction(0)
    safe_negative_volume_sum = Fraction(0)
    safe_positive_volume_sum = Fraction(0)
    curved_area_sum = Fraction(0)
    mismatch_area_sum = Fraction(0)

    for (key_id, chart, axis, coordinate), groups in face_groups.items():
        positive_indices, negative_indices = groups
        if not positive_indices or not negative_indices:
            continue
        for positive_index in positive_indices:
            positive = occurrences[positive_index]
            for negative_index in negative_indices:
                negative = occurrences[negative_index]
                if positive["id"] == negative["id"]:
                    continue
                if (
                    positive["source"] != "ROUND174_RESOLVED"
                    and negative["source"] != "ROUND174_RESOLVED"
                ):
                    continue
                tangential_axes = [value for value in range(3) if value != axis]
                if any(
                    min(
                        positive["box"][2 * tangent + 1],
                        negative["box"][2 * tangent + 1],
                    )
                    <= max(
                        positive["box"][2 * tangent],
                        negative["box"][2 * tangent],
                    )
                    for tangent in tangential_axes
                ):
                    continue
                need(
                    positive["key_id"] == negative["key_id"] == key_id
                    and positive["chart"] == negative["chart"] == chart,
                    "same-key/chart face group",
                )
                pair_type = "|".join(sorted((positive["source"], negative["source"])))
                same_key_pair_histogram[pair_type] += 1
                geometry = common_face_geometry(negative, positive, axis, coordinate)
                base = {
                    "negative": negative,
                    "positive": positive,
                    "pair_type": pair_type,
                    "key_id": key_id,
                    "chart": chart,
                    "axis": axis,
                    "geometry": geometry,
                }
                if positive["signature_bytes"] != negative["signature_bytes"]:
                    differing = [
                        field
                        for field in SIGNATURE_FIELDS
                        if positive["signature"][field] != negative["signature"][field]
                    ]
                    need(differing, "nonempty signature mismatch fields")
                    row_id = "round265-signature-mismatch-nonedge:" + digest([
                        negative["id"],
                        positive["id"],
                        AXIS_NAMES[axis],
                        qtext(coordinate),
                        geometry["exact_positive_2D_common_face_rectangle"],
                    ])
                    base["row_id"] = row_id
                    base["differing_fields"] = differing
                    mismatch_raw.append(base)
                    mismatch_axis_histogram[f"{AXIS_NAMES[axis]}:{pair_type}"] += 1
                    mismatch_area_sum += geometry["_area"]
                    continue

                need(
                    positive["signature"] == negative["signature"],
                    "byte-equal signature object",
                )
                full_signature_pair_histogram[pair_type] += 1
                if pair_type in {
                    "ROUND174_RESOLVED|ROUND174_RESOLVED",
                    "ROUND174_RESOLVED|ROUND179_RESOLVED",
                }:
                    row_id = "round265-safe-full-signature-face-edge:" + digest([
                        negative["id"],
                        positive["id"],
                        AXIS_NAMES[axis],
                        qtext(coordinate),
                        geometry["exact_positive_2D_common_face_rectangle"],
                    ])
                    base["row_id"] = row_id
                    base["vertex_pair"] = tuple(sorted((
                        negative["vertex"],
                        positive["vertex"],
                    )))
                    need(base["vertex_pair"][0] != base["vertex_pair"][1], f"distinct safe seeds:{row_id}")
                    safe_raw.append(base)
                    safe_axis_histogram[f"{AXIS_NAMES[axis]}:{pair_type}"] += 1
                    relation_histogram[geometry["face_relation"]] += 1
                    safe_area_sum += geometry["_area"]
                    safe_negative_volume_sum += geometry["_negative_volume"]
                    safe_positive_volume_sum += geometry["_positive_volume"]
                else:
                    need(
                        pair_type in {
                            "ROUND174_RESOLVED|ROUND204_REGION",
                            "ROUND174_RESOLVED|ROUND208_REGION",
                        },
                        f"known curved pair class:{pair_type}",
                    )
                    row_id = "round265-curved-face-failclosed:" + digest([
                        negative["id"],
                        positive["id"],
                        AXIS_NAMES[axis],
                        qtext(coordinate),
                        geometry["exact_positive_2D_common_face_rectangle"],
                    ])
                    base["row_id"] = row_id
                    base["vertex_pair"] = tuple(sorted((
                        negative["vertex"],
                        positive["vertex"],
                    )))
                    curved_raw.append(base)
                    curved_axis_histogram[f"{AXIS_NAMES[axis]}:{pair_type}"] += 1
                    curved_area_sum += geometry["_area"]

    safe_raw.sort(key=lambda row: row["row_id"])
    curved_raw.sort(key=lambda row: row["row_id"])
    mismatch_raw.sort(key=lambda row: row["row_id"])
    all_ids = (
        [row["row_id"] for row in safe_raw]
        + [row["row_id"] for row in curved_raw]
        + [row["row_id"] for row in mismatch_raw]
    )
    need(len(all_ids) == len(set(all_ids)) == 174_108, "complete same-key face disposition IDs")
    need(
        dict(sorted(full_signature_pair_histogram.items()))
        == EXPECTED_FULL_SIGNATURE_FACE_HISTOGRAM,
        "full-signature face histogram",
    )
    need(
        len(safe_raw) == 169_064
        and len(curved_raw) == 2_652
        and len(mismatch_raw) == 2_392,
        "safe/curved/mismatch partition",
    )
    need(
        dict(sorted(safe_axis_histogram.items())) == EXPECTED_SAFE_AXIS_HISTOGRAM,
        "safe axis histogram",
    )
    need(
        dict(sorted(curved_axis_histogram.items())) == EXPECTED_CURVED_AXIS_HISTOGRAM,
        "curved axis histogram",
    )
    need(
        set(same_key_pair_histogram)
        == {
            "ROUND174_RESOLVED|ROUND174_RESOLVED",
            "ROUND174_RESOLVED|ROUND179_RESOLVED",
            "ROUND174_RESOLVED|ROUND204_REGION",
            "ROUND174_RESOLVED|ROUND208_REGION",
        }
        and same_key_pair_histogram["ROUND174_RESOLVED|ROUND208_REGION"] == 4_948
        and all(
            row["pair_type"] == "ROUND174_RESOLVED|ROUND208_REGION"
            for row in mismatch_raw
        ),
        "same-key mismatch confined to R174/R208",
    )
    need(
        dict(sorted(relation_histogram.items()))
        == {
            "EXACT_EQUAL_FACE": 67_100,
            "POSITIVE_AREA_PARTIAL_REFINEMENT": 101_964,
        },
        "safe exact/partial face relation",
    )

    # Saturate only the two exact resolved-box channels.
    round174_ids = {
        row["id"] for row in occurrences if row["source"] == "ROUND174_RESOLVED"
    }
    seed_ids = sorted(set(base_components) | round174_ids)
    need(len(seed_ids) == 140_812, "expanded seed universe")
    dsu = DSU(seed_ids)
    for row in safe_raw:
        row["rank_reducing"] = dsu.union(*row["vertex_pair"])
    rank_reduction_count = sum(row["rank_reducing"] for row in safe_raw)
    need(
        rank_reduction_count == 77_000
        and len(safe_raw) - rank_reduction_count == 92_064
        and len({row["vertex_pair"] for row in safe_raw}) == 162_424,
        "safe face DSU census",
    )
    classes: dict[str, list[str]] = defaultdict(list)
    for seed_id in seed_ids:
        classes[dsu.find(seed_id)].append(seed_id)
    need(len(classes) == 63_812, "post-safe-face quotient")

    occurrence_by_id = {row["id"]: row for row in occurrences}
    seed_descriptors: dict[str, dict[str, Any]] = {}
    seed_key: dict[str, tuple[str, int]] = {}
    for component_id, item in base_components.items():
        seed_descriptors[component_id] = {
            "seed_kind": "ROUND264_CORRECTED_COMPONENT",
            "seed_id": component_id,
            "source_row_id": item["source_row_id"],
            "source_row_sha256": item["source_row_sha256"],
        }
        seed_key[component_id] = (
            item["official_key_id"],
            item["official_key_ordinal"],
        )
    for occurrence_id in round174_ids:
        item = occurrence_by_id[occurrence_id]
        seed_descriptors[occurrence_id] = {
            "seed_kind": "ROUND174_RESOLVED_OCCURRENCE",
            "seed_id": occurrence_id,
            "source_row_id": item["source_row_id"],
            "source_row_sha256": item["source_row_sha256"],
        }
        seed_key[occurrence_id] = (item["key_id"], item["key_ordinal"])
    need(set(seed_descriptors) == set(seed_ids), "complete seed descriptors")

    post_id_by_seed: dict[str, str] = {}
    post_class_seeds: dict[str, list[str]] = {}
    post_descriptor_hash: dict[str, str] = {}
    for members in classes.values():
        members.sort()
        descriptors = [seed_descriptors[value] for value in members]
        keys = {seed_key[value] for value in members}
        need(len(keys) == 1, "exact-key-pure expanded component")
        post_id = "round265-expanded-face-component:" + digest(descriptors)
        need(post_id not in post_class_seeds, f"unique post component:{post_id}")
        post_class_seeds[post_id] = members
        post_descriptor_hash[post_id] = digest(descriptors)
        for value in members:
            post_id_by_seed[value] = post_id

    # Edge ledgers are closed only after their post-quotient assignment is
    # known.
    safe_edge_rows: list[dict[str, Any]] = []
    safe_edge_count_by_post: Counter[str] = Counter()
    safe_rank_count_by_post: Counter[str] = Counter()
    safe_edge_count_by_key: Counter[str] = Counter()
    safe_rank_count_by_key: Counter[str] = Counter()
    for item in safe_raw:
        negative = item["negative"]
        positive = item["positive"]
        geometry = item["geometry"]
        post_id = post_id_by_seed[item["vertex_pair"][0]]
        need(post_id == post_id_by_seed[item["vertex_pair"][1]], "safe edge post assignment")
        safe_edge_count_by_post[post_id] += 1
        safe_rank_count_by_post[post_id] += int(item["rank_reducing"])
        safe_edge_count_by_key[item["key_id"]] += 1
        safe_rank_count_by_key[item["key_id"]] += int(item["rank_reducing"])
        safe_edge_rows.append(closed({
            "safe_full_signature_face_edge_row_id": item["row_id"],
            "negative_side_occurrence_id": negative["id"],
            "positive_side_occurrence_id": positive["id"],
            "negative_side_occurrence_source": negative["source"],
            "positive_side_occurrence_source": positive["source"],
            "occurrence_source_pair": item["pair_type"],
            "official_key_id": item["key_id"],
            "official_key_ordinal": negative["key_ordinal"],
            "source_chart": item["chart"],
            "complete_10_field_return_signature_sha256":
                negative["signature_sha256"],
            "complete_10_field_return_signature_equal": True,
            "signature_field_order": list(SIGNATURE_FIELDS),
            "face_axis": geometry["face_axis"],
            "shared_face_coordinate": geometry["shared_face_coordinate"],
            "tangential_axes": geometry["tangential_axes"],
            "exact_positive_2D_common_face_rectangle":
                geometry["exact_positive_2D_common_face_rectangle"],
            "exact_positive_2D_common_face_area":
                geometry["exact_positive_2D_common_face_area"],
            "face_relation": geometry["face_relation"],
            "negative_side_strict_3D_corridor_volume":
                geometry["negative_side_strict_3D_corridor_volume"],
            "positive_side_strict_3D_corridor_volume":
                geometry["positive_side_strict_3D_corridor_volume"],
            "pre_Round265_seed_pair": list(item["vertex_pair"]),
            "post_Round265_quotient_component_id": post_id,
            "proof_kind":
                "EXACT_POSITIVE_AREA_RESOLVED_BOX_FACE_WITH_STRICT_TWO_SIDED_3D_CORRIDORS",
            "rank_reducing_edge": item["rank_reducing"],
            "component_union_credit": 1 if item["rank_reducing"] else 0,
            "maximality_credit": 0,
        }))

    curved_rows: list[dict[str, Any]] = []
    curved_internal_count = 0
    for item in curved_raw:
        negative = item["negative"]
        positive = item["positive"]
        geometry = item["geometry"]
        post_pair = tuple(sorted((
            post_id_by_seed[negative["vertex"]],
            post_id_by_seed[positive["vertex"]],
        )))
        internal = post_pair[0] == post_pair[1]
        curved_internal_count += int(internal)
        curved_rows.append(closed({
            "curved_face_failclosed_row_id": item["row_id"],
            "negative_side_occurrence_id": negative["id"],
            "positive_side_occurrence_id": positive["id"],
            "negative_side_occurrence_source": negative["source"],
            "positive_side_occurrence_source": positive["source"],
            "occurrence_source_pair": item["pair_type"],
            "official_key_id": item["key_id"],
            "official_key_ordinal": negative["key_ordinal"],
            "source_chart": item["chart"],
            "complete_10_field_return_signature_sha256":
                negative["signature_sha256"],
            "complete_10_field_return_signature_equal": True,
            "face_axis": geometry["face_axis"],
            "shared_face_coordinate": geometry["shared_face_coordinate"],
            "tangential_axes": geometry["tangential_axes"],
            "exact_positive_2D_enclosing_box_face_rectangle":
                geometry["exact_positive_2D_common_face_rectangle"],
            "exact_positive_2D_enclosing_box_face_area":
                geometry["exact_positive_2D_common_face_area"],
            "pre_Round265_seed_pair": list(item["vertex_pair"]),
            "post_safe_face_component_pair": list(post_pair),
            "post_safe_face_pair_internal": internal,
            "disposition":
                "FAIL_CLOSED_CURVED_GRAPH_SIDE_REQUIRES_STRICT_TWO_SIDED_CORRIDOR_OR_EXACT_SEPARATION",
            "physical_glue_credit": 0,
            "component_union_credit": 0,
            "maximality_credit": 0,
        }))

    mismatch_rows: list[dict[str, Any]] = []
    mismatch_internal_count = 0
    for item in mismatch_raw:
        negative = item["negative"]
        positive = item["positive"]
        geometry = item["geometry"]
        vertex_pair = tuple(sorted((negative["vertex"], positive["vertex"])))
        post_pair = tuple(sorted((
            post_id_by_seed[vertex_pair[0]],
            post_id_by_seed[vertex_pair[1]],
        )))
        internal = post_pair[0] == post_pair[1]
        mismatch_internal_count += int(internal)
        mismatch_rows.append(closed({
            "same_key_signature_mismatch_nonedge_row_id": item["row_id"],
            "negative_side_occurrence_id": negative["id"],
            "positive_side_occurrence_id": positive["id"],
            "negative_side_occurrence_source": negative["source"],
            "positive_side_occurrence_source": positive["source"],
            "occurrence_source_pair": item["pair_type"],
            "official_key_id": item["key_id"],
            "official_key_ordinal": negative["key_ordinal"],
            "source_chart": item["chart"],
            "negative_complete_10_field_return_signature_sha256":
                negative["signature_sha256"],
            "positive_complete_10_field_return_signature_sha256":
                positive["signature_sha256"],
            "differing_signature_fields": item["differing_fields"],
            "complete_10_field_return_signature_equal": False,
            "face_axis": geometry["face_axis"],
            "shared_face_coordinate": geometry["shared_face_coordinate"],
            "tangential_axes": geometry["tangential_axes"],
            "exact_positive_2D_enclosing_box_face_rectangle":
                geometry["exact_positive_2D_common_face_rectangle"],
            "exact_positive_2D_enclosing_box_face_area":
                geometry["exact_positive_2D_common_face_area"],
            "pre_Round265_seed_pair": list(vertex_pair),
            "post_safe_face_component_pair": list(post_pair),
            "post_safe_face_pair_internal": internal,
            "disposition":
                "EXPLICIT_NONEDGE__SAME_KEY_IS_INSUFFICIENT__COMPLETE_RETURN_SIGNATURE_MISMATCH",
            "physical_glue_credit": 0,
            "component_union_credit": 0,
            "maximality_credit": 0,
        }))

    # Complete seed map.
    seed_map_rows: list[dict[str, Any]] = []
    for seed_id in seed_ids:
        descriptor = seed_descriptors[seed_id]
        key_id, ordinal = seed_key[seed_id]
        seed_map_rows.append(closed({
            "expanded_seed_to_Round265_component_map_row_id":
                "round265-seed-map:" + digest([seed_id]),
            "seed_id": seed_id,
            "seed_kind": descriptor["seed_kind"],
            "official_key_id": key_id,
            "official_key_ordinal": ordinal,
            "source_row_id": descriptor["source_row_id"],
            "source_row_sha256": descriptor["source_row_sha256"],
            "seed_descriptor_sha256": digest(descriptor),
            "post_Round265_quotient_component_id": post_id_by_seed[seed_id],
            "maximality_credit": 0,
        }))

    # Complete expanded occurrence frontier.
    occurrence_rows: list[dict[str, Any]] = []
    occurrence_count_by_post: Counter[str] = Counter()
    occurrence_count_by_key: Counter[str] = Counter()
    R174_count_by_post: Counter[str] = Counter()
    R174_count_by_key: Counter[str] = Counter()
    for item in sorted(occurrences, key=lambda row: row["id"]):
        post_id = post_id_by_seed[item["vertex"]]
        occurrence_count_by_post[post_id] += 1
        occurrence_count_by_key[item["key_id"]] += 1
        if item["source"] == "ROUND174_RESOLVED":
            R174_count_by_post[post_id] += 1
            R174_count_by_key[item["key_id"]] += 1
        binding = item["round264_row"]
        occurrence_rows.append(closed({
            "post_Round265_expanded_occurrence_frontier_row_id":
                "round265-expanded-occurrence:" + digest([item["id"]]),
            "local_occurrence_row_id": item["id"],
            "occurrence_source": item["source"],
            "official_key_id": item["key_id"],
            "official_key_ordinal": item["key_ordinal"],
            "source_chart": item["chart"],
            "complete_10_field_return_signature_sha256":
                item["signature_sha256"],
            "exact_box_sha256": digest(item["box_text"]),
            "source_geometry_row_id": item["source_row_id"],
            "source_geometry_row_sha256": item["source_row_sha256"],
            "source_Round264_occurrence_frontier_row_id":
                None if binding is None else binding["source_row_id"],
            "source_Round264_occurrence_frontier_row_sha256":
                None if binding is None else binding["source_row_sha256"],
            "pre_Round265_seed_id": item["vertex"],
            "post_Round265_quotient_component_id": post_id,
            "expanded_quotient_assignment_credit": 1,
            "maximal_physical_component_assignment_credit": 0,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    need(len(occurrence_rows) == 126_468, "complete expanded occurrence frontier")

    # Complete valid virtual frontier, reassigned through the safe quotient.
    virtual_rows: list[dict[str, Any]] = []
    virtual_count_by_post: Counter[str] = Counter()
    virtual_count_by_key: Counter[str] = Counter()
    for item in sorted(base_virtual, key=lambda row: row["node_id"]):
        current_id = item["current_component_id"]
        post_id = post_id_by_seed[current_id]
        need(
            item["official_key_id"] == base_components[current_id]["official_key_id"],
            f"virtual key purity:{item['node_id']}",
        )
        virtual_count_by_post[post_id] += 1
        virtual_count_by_key[item["official_key_id"]] += 1
        virtual_rows.append(closed({
            "post_Round265_valid_virtual_node_frontier_row_id":
                "round265-valid-virtual-node:" + digest([item["node_id"]]),
            "valid_virtual_stratum_node_id": item["node_id"],
            "virtual_node_kind": item["kind"],
            "official_key_id": item["official_key_id"],
            "source_Round264_valid_virtual_node_frontier_row_id":
                item["source_row_id"],
            "source_Round264_valid_virtual_node_frontier_row_sha256":
                item["source_row_sha256"],
            "post_Round264_quotient_component_id": current_id,
            "post_Round265_quotient_component_id": post_id,
            "valid_virtual_node_identity_preserved": True,
            "maximality_credit": 0,
        }))
    need(len(virtual_rows) == 133_284, "complete valid virtual frontier")

    classes_with_old: set[str] = set()
    for post_id, members in post_class_seeds.items():
        if any(value in base_components for value in members):
            classes_with_old.add(post_id)
    R174_attached_count = sum(
        R174_count_by_post[post_id] for post_id in classes_with_old
    )
    R174_only_classes = set(post_class_seeds) - classes_with_old
    need(
        R174_attached_count == 67_620
        and len(R174_only_classes) == 1_948,
        "R174 attachment and R174-only class census",
    )

    # Complete component frontier.
    component_rows: list[dict[str, Any]] = []
    component_count_by_key: Counter[str] = Counter()
    R174_only_count_by_key: Counter[str] = Counter()
    expanded_member_sum = 0
    seed_class_size_histogram: Counter[int] = Counter()
    for post_id in sorted(post_class_seeds):
        members = post_class_seeds[post_id]
        keys = {seed_key[value] for value in members}
        need(len(keys) == 1, f"component key purity:{post_id}")
        key_id, ordinal = next(iter(keys))
        old_count = sum(value in base_components for value in members)
        R174_seed_count = len(members) - old_count
        occurrence_count = occurrence_count_by_post[post_id]
        virtual_count = virtual_count_by_post[post_id]
        member_count = occurrence_count + virtual_count
        need(member_count > 0, f"nonempty expanded component:{post_id}")
        expanded_member_sum += member_count
        component_count_by_key[key_id] += 1
        if old_count == 0:
            R174_only_count_by_key[key_id] += 1
        seed_class_size_histogram[len(members)] += 1
        component_rows.append(closed({
            "post_Round265_component_frontier_row_id":
                "round265-component-row:" + digest([post_id]),
            "post_Round265_quotient_component_id": post_id,
            "official_key_id": key_id,
            "official_key_ordinal": ordinal,
            "constituent_seed_count": len(members),
            "constituent_seed_ids": members,
            "constituent_seed_ids_sha256": digest(members),
            "constituent_seed_descriptors_sha256":
                post_descriptor_hash[post_id],
            "constituent_Round264_component_count": old_count,
            "constituent_Round174_occurrence_seed_count": R174_seed_count,
            "safe_full_signature_face_edge_count":
                safe_edge_count_by_post[post_id],
            "safe_full_signature_rank_reduction_count":
                safe_rank_count_by_post[post_id],
            "expanded_occurrence_member_count": occurrence_count,
            "Round174_occurrence_member_count": R174_count_by_post[post_id],
            "valid_virtual_stratum_node_count": virtual_count,
            "expanded_member_count": member_count,
            "component_class":
                "R174_ONLY" if old_count == 0 else "ATTACHED_TO_ROUND264",
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
        }))
    need(
        len(component_rows) == 63_812
        and expanded_member_sum == 259_752,
        "complete expanded component/member frontier",
    )

    # Complete exact-key frontier.
    key_rows: list[dict[str, Any]] = []
    R174_seed_count_by_key: Counter[str] = Counter(
        occurrence_by_id[value]["key_id"] for value in round174_ids
    )
    old_seed_count_by_key: Counter[str] = Counter(
        item["official_key_id"] for item in base_components.values()
    )
    for key_id in sorted(base_keys):
        item = base_keys[key_id]
        pre_seed_count = (
            old_seed_count_by_key[key_id] + R174_seed_count_by_key[key_id]
        )
        post_count = component_count_by_key[key_id]
        rank_reduction = pre_seed_count - post_count
        need(
            occurrence_count_by_key[key_id]
            == item["occurrence_count"] + R174_count_by_key[key_id]
            and virtual_count_by_key[key_id] == item["valid_virtual_count"]
            and rank_reduction == safe_rank_count_by_key[key_id],
            f"expanded key conservation:{key_id}",
        )
        key_rows.append(closed({
            "post_Round265_key_frontier_row_id":
                "round265-key-frontier:" + digest([key_id]),
            "official_key_id": key_id,
            "official_key_ordinal": item["official_key_ordinal"],
            "source_Round264_key_frontier_row_id": item["source_row_id"],
            "source_Round264_key_frontier_row_sha256": item["source_row_sha256"],
            "pre_Round265_Round264_component_seed_count":
                old_seed_count_by_key[key_id],
            "pre_Round265_Round174_occurrence_seed_count":
                R174_seed_count_by_key[key_id],
            "pre_Round265_expanded_seed_count": pre_seed_count,
            "safe_full_signature_face_edge_count":
                safe_edge_count_by_key[key_id],
            "safe_full_signature_rank_reduction_count": rank_reduction,
            "post_Round265_quotient_component_count": post_count,
            "post_Round265_R174_only_component_count":
                R174_only_count_by_key[key_id],
            "expanded_occurrence_count": occurrence_count_by_key[key_id],
            "Round174_occurrence_count": R174_count_by_key[key_id],
            "valid_virtual_stratum_node_count": virtual_count_by_key[key_id],
            "expanded_member_count":
                occurrence_count_by_key[key_id] + virtual_count_by_key[key_id],
            "occurrence_quotient_assignment_complete": True,
            "all_quotient_components_proved_maximal": False,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    need(
        len(key_rows) == 116
        and sum(component_count_by_key.values()) == 63_812
        and sum(occurrence_count_by_key.values()) == 126_468
        and sum(virtual_count_by_key.values()) == 133_284,
        "complete expanded key frontier",
    )

    disposition_commitment_row = closed({
        "complete_same_key_face_disposition_commitment_row_id":
            "round265-complete-same-key-face-disposition",
        "enumeration_scope":
            "ALL_POSITIVE_AREA_SAME_KEY_SAME_SOURCE_CHART_BOX_FACES_INVOLVING_AT_LEAST_ONE_ROUND174_OCCURRENCE",
        "complete_10_field_signature_field_order": list(SIGNATURE_FIELDS),
        "same_key_positive_area_face_candidate_count": 174_108,
        "safe_full_signature_resolved_box_edge_count": 169_064,
        "curved_graph_side_failclosed_count": 2_652,
        "same_key_complete_signature_mismatch_nonedge_count": 2_392,
        "disposition_partition_complete": True,
        "safe_edge_row_ids_sha256":
            digest([row["safe_full_signature_face_edge_row_id"] for row in safe_edge_rows]),
        "curved_failclosed_row_ids_sha256":
            digest([row["curved_face_failclosed_row_id"] for row in curved_rows]),
        "signature_mismatch_nonedge_row_ids_sha256":
            digest([
                row["same_key_signature_mismatch_nonedge_row_id"]
                for row in mismatch_rows
            ]),
        "all_disposition_row_ids_sha256": digest(sorted(all_ids)),
        "key_equality_alone_authorizes_physical_edge": False,
        "physical_edge_requires_complete_signature_equality": True,
    })

    census = {
        "Round264_corrected_component_seed_count": 68_312,
        "new_Round174_resolved_occurrence_seed_count": 72_500,
        "pre_Round265_expanded_seed_count": 140_812,
        "expanded_occurrence_source_histogram": dict(sorted(source_counts.items())),
        "expanded_occurrence_count": 126_468,
        "valid_virtual_stratum_node_count": 133_284,
        "expanded_member_count": 259_752,
        "exact_key_count": 116,
        "same_key_same_chart_face_carrier_group_count": len(face_groups),
        "same_key_positive_area_face_candidate_count": 174_108,
        "same_key_positive_area_face_pair_histogram":
            dict(sorted(same_key_pair_histogram.items())),
        "full_10_field_signature_equal_face_histogram":
            dict(sorted(full_signature_pair_histogram.items())),
        "safe_full_signature_resolved_box_face_edge_count": 169_064,
        "safe_full_signature_face_axis_histogram":
            dict(sorted(safe_axis_histogram.items())),
        "safe_exact_equal_face_count": 67_100,
        "safe_positive_area_partial_refinement_face_count": 101_964,
        "safe_distinct_pre_seed_pair_count": 162_424,
        "safe_rank_reducing_edge_count": 77_000,
        "safe_redundant_edge_count": 92_064,
        "safe_exact_positive_2D_common_face_area_sum": qtext(safe_area_sum),
        "safe_negative_side_strict_3D_corridor_volume_sum":
            qtext(safe_negative_volume_sum),
        "safe_positive_side_strict_3D_corridor_volume_sum":
            qtext(safe_positive_volume_sum),
        "curved_graph_side_failclosed_face_count": 2_652,
        "curved_graph_side_face_axis_histogram":
            dict(sorted(curved_axis_histogram.items())),
        "curved_enclosing_box_positive_face_area_sum": qtext(curved_area_sum),
        "curved_post_safe_face_internal_pair_count": curved_internal_count,
        "curved_post_safe_face_cross_component_pair_count":
            2_652 - curved_internal_count,
        "same_key_complete_signature_mismatch_nonedge_count": 2_392,
        "signature_mismatch_axis_histogram":
            dict(sorted(mismatch_axis_histogram.items())),
        "signature_mismatch_enclosing_box_positive_face_area_sum":
            qtext(mismatch_area_sum),
        "signature_mismatch_post_safe_face_internal_pair_count":
            mismatch_internal_count,
        "signature_mismatch_post_safe_face_cross_component_pair_count":
            2_392 - mismatch_internal_count,
        "post_Round265_component_count": 63_812,
        "post_Round265_component_seed_class_size_histogram": {
            str(key): value
            for key, value in sorted(seed_class_size_histogram.items())
        },
        "Round174_occurrence_count_attached_to_preexisting_Round264_class":
            67_620,
        "Round174_occurrence_count_not_attached_to_preexisting_Round264_class":
            4_880,
        "Round174_only_post_Round265_component_count": 1_948,
        "post_Round265_component_count_with_Round264_constituent":
            len(classes_with_old),
        "maximal_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }

    return {
        "status": (
            "CERTIFIED_EXPANDED_126468_OCCURRENCE_SAFE_FULL_SIGNATURE_FACE_"
            "SATURATION__169064_SAFE_EDGES__77000_RANK_REDUCTIONS__"
            "POST_ROUND265_COMPONENTS_63812__2652_CURVED_FACES_FAIL_CLOSED"
        ),
        "formal_input_binding": input_binding(),
        "formal_complete_same_key_face_disposition_commitment_ledger": ledger(
            [disposition_commitment_row],
            "complete_same_key_face_disposition_commitment_row_id",
        ),
        "formal_safe_full_signature_resolved_box_face_edge_ledger": ledger(
            safe_edge_rows,
            "safe_full_signature_face_edge_row_id",
        ),
        "formal_curved_graph_side_face_failclosed_ledger": ledger(
            curved_rows,
            "curved_face_failclosed_row_id",
        ),
        "formal_same_key_complete_signature_mismatch_nonedge_ledger": ledger(
            mismatch_rows,
            "same_key_signature_mismatch_nonedge_row_id",
        ),
        "formal_expanded_seed_to_Round265_component_map_ledger": ledger(
            seed_map_rows,
            "expanded_seed_to_Round265_component_map_row_id",
        ),
        "formal_post_Round265_component_frontier_ledger": ledger(
            component_rows,
            "post_Round265_component_frontier_row_id",
        ),
        "formal_post_Round265_expanded_occurrence_frontier_ledger": ledger(
            occurrence_rows,
            "post_Round265_expanded_occurrence_frontier_row_id",
        ),
        "formal_post_Round265_key_frontier_ledger": ledger(
            key_rows,
            "post_Round265_key_frontier_row_id",
        ),
        "formal_post_Round265_valid_virtual_node_frontier_ledger": ledger(
            virtual_rows,
            "post_Round265_valid_virtual_node_frontier_row_id",
        ),
        "census": census,
        "scope_contract": {
            "all_72500_Round174_resolved_positive_open_3D_occurrences_admitted":
                True,
            "expanded_126468_occurrence_universe_independently_reconstructed":
                True,
            "all_positive_area_same_key_same_chart_box_faces_involving_Round174_enumerated":
                True,
            "same_key_is_not_used_as_a_physical_glue_rule": True,
            "safe_face_edge_requires_equality_of_all_10_return_signature_fields":
                True,
            "safe_resolved_box_faces_have_exact_positive_area_and_strict_two_sided_3D_corridors":
                True,
            "all_Round174_Round204_and_Round174_Round208_full_signature_faces_remain_fail_closed":
                True,
            "all_same_key_signature_mismatch_faces_are_explicit_nonedges":
                True,
            "complete_seed_component_occurrence_key_and_valid_virtual_frontiers_rebuilt":
                True,
            "valid_virtual_node_identity_and_count_preserved": True,
            "Round174_lower_dimensional_and_residual_strata_not_closed_by_this_round":
                True,
            "component_maximality_not_proved": True,
            "exact_key_fibre_exhaustion_not_proved": True,
            "Jx_Jy_are_not_same_point_glue_generators": True,
        },
        "strict_nonpromotion": {
            "safe_full_signature_physical_face_edge_count": 169_064,
            "new_component_union_credit": 77_000,
            "remaining_fail_closed_curved_face_count": 2_652,
            "same_key_signature_mismatch_physical_edge_credit": 0,
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
            "close or exactly separate all 2,652 Round174--Round204/Round208 "
            "curved graph-side face candidates, then audit the expanded "
            "63,812-component frontier for maximality and exhaust all 116 "
            "exact-key fibres"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "upstream_producer_imported_or_executed": False,
            "arithmetic": "fractions.Fraction exact rational",
            "seed_affects_output": False,
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=265_071)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    need(
        isinstance(arguments.seed, int) and not isinstance(arguments.seed, bool),
        "integral seed",
    )
    producer_sha256 = hashlib.sha256(
        regular_bytes(Path(__file__).resolve(), 5_000_000)
    ).hexdigest()
    result = build(producer_sha256)
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    encoded = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(encoded)
    print(result["status"])
    print(f"producer_sha256={producer_sha256}")
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(
        "same_key_faces=174108 safe=169064 curved_failclosed=2652 "
        "signature_mismatch_nonedge=2392"
    )
    print(
        "pre_seeds=140812 rank=77000 post_components=63812 "
        "frontiers=126468/116/133284 members=259752"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
