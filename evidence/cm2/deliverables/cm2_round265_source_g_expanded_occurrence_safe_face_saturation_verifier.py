#!/usr/bin/env python3
"""Independent verifier for the CM2 Round265 expanded face saturation.

The Round265 producer is treated only as a pinned inert byte string.  This
program reconstructs the complete expanded occurrence universe, exhaustively
classifies every in-scope face, recomputes the quotient and every published
frontier, and finishes that expected object before opening the candidate.
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
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE = HERE / f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
PRODUCER_SHA256 = (
    "ff32b033486d236d67532e7eef771983b32c8ca556d3fce06ddf3313ffb3f84d"
)
CANDIDATE_SHA256 = (
    "78ec778a0521580991f18b9a5ef5d2ea9065283d5efb49a920c7469526735d18"
)
CANDIDATE_RESULT_SHA256 = (
    "8289c4ee4d6d9698fcb0e7caff3d803e81122b06278c246cd20ab47298f682d4"
)
CANDIDATE_SIZE = 915_077_047
CANDIDATE_SCHEMA = (
    "cm2.round265.source-g-expanded-occurrence-safe-face-saturation.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round265.source-g-expanded-occurrence-safe-face-saturation-"
    "verification.v1"
)

R174_CERT = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_"
    "materialization_certificate.json"
)
R174_ROWS = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_"
    "materialization_rows.json"
)
R179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R204 = (
    "cm2_round204_source_g_wall_return_signature_local_replacement_"
    "certificate.json"
)
R208 = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization_"
    "certificate.json"
)
R264 = (
    "cm2_round264_source_g_lower_dimensional_endpoint_correction_and_"
    "glue_closure_certificate.json"
)

UPSTREAM = {
    R174_CERT: (
        "10221141c58c044b42e43009beb34ae4705995925a88deaa70ff2eba2ea852c7",
        "d45f05458c42189cf0ebc51e258356d13278ba40845cce80b6a072ffbc8cf09b",
        "cm2.round174.source-g-unique-first-dynamic-occurrence-materialization.v1",
    ),
    R174_ROWS: (
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
        "002ca6631edd39c2325c63a1e8f9717d111f4d10c6d2585077d665a0ff128d18",
        "cm2.round174.source-g-unique-first-dynamic-occurrence-rows.v1",
    ),
    R179_ROWS: (
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
        "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb",
        "cm2.round179.source-g-residual-tube-arrangement-rows.v1",
    ),
    R204: (
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
        "ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd",
        "cm2.round204.source-g-wall-return-signature-local-replacement.v1",
    ),
    R208: (
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
        "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8",
        "cm2.round208.source-g-outgoing-direct-signature-materialization.v1",
    ),
    R264: (
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
AXES = ("t", "p", "s")
SOURCE_COUNTS = {
    "ROUND174_RESOLVED": 72_500,
    "ROUND179_RESOLVED": 17_192,
    "ROUND204_REGION": 736,
    "ROUND208_REGION": 36_040,
}
FULL_FACE_HISTOGRAM = {
    "ROUND174_RESOLVED|ROUND174_RESOLVED": 138_412,
    "ROUND174_RESOLVED|ROUND179_RESOLVED": 30_652,
    "ROUND174_RESOLVED|ROUND204_REGION": 96,
    "ROUND174_RESOLVED|ROUND208_REGION": 2_556,
}
SAFE_AXIS_HISTOGRAM = {
    "p:ROUND174_RESOLVED|ROUND174_RESOLVED": 60_200,
    "p:ROUND174_RESOLVED|ROUND179_RESOLVED": 13_080,
    "s:ROUND174_RESOLVED|ROUND174_RESOLVED": 16_152,
    "s:ROUND174_RESOLVED|ROUND179_RESOLVED": 3_220,
    "t:ROUND174_RESOLVED|ROUND174_RESOLVED": 62_060,
    "t:ROUND174_RESOLVED|ROUND179_RESOLVED": 14_352,
}
CURVED_AXIS_HISTOGRAM = {
    "p:ROUND174_RESOLVED|ROUND204_REGION": 32,
    "p:ROUND174_RESOLVED|ROUND208_REGION": 1_796,
    "t:ROUND174_RESOLVED|ROUND204_REGION": 64,
    "t:ROUND174_RESOLVED|ROUND208_REGION": 760,
}


class VerificationFailure(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationFailure(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def encoded_chunks(value: Any) -> Iterable[bytes]:
    for piece in ENCODER.iterencode(value):
        yield piece.encode("utf-8")


def encoded(value: Any) -> bytes:
    return b"".join(encoded_chunks(value))


def fingerprint(value: Any) -> str:
    state = hashlib.sha256()
    for piece in encoded_chunks(value):
        state.update(piece)
    return state.hexdigest()


def fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def seal(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    require("row_sha256" not in result, "fresh row closure")
    result["row_sha256"] = fingerprint(result)
    return result


def make_ledger(rows: list[dict[str, Any]], identity: str) -> dict[str, Any]:
    require(
        len(rows) == len({row[identity] for row in rows}),
        f"unique output ids:{identity}",
    )
    return {
        "row_count": len(rows),
        "rows_sha256": fingerprint(rows),
        "row_ids_sha256": fingerprint([row[identity] for row in rows]),
        "row_hashes_sha256": fingerprint([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def guarded_read(
    path: Path,
    maximum: int,
    required_parent: Path | None = HERE,
    expected_size: int | None = None,
) -> bytes:
    if required_parent is not None:
        require(path.parent == required_parent, f"input parent:{path.name}")
    before = path.lstat()
    require(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1,
        f"regular nonlinked input:{path.name}",
    )
    require(0 < before.st_size <= maximum, f"bounded input:{path.name}")
    if expected_size is not None:
        require(before.st_size == expected_size, f"exact input size:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns)
            == (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns),
            f"stable open:{path.name}",
        )
        pieces: list[bytes] = []
        total = 0
        while True:
            piece = os.read(descriptor, 1024 * 1024)
            if not piece:
                break
            total += len(piece)
            require(total <= maximum, f"bounded read:{path.name}")
            pieces.append(piece)
        after = os.fstat(descriptor)
        require(
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns),
            f"stable read:{path.name}",
        )
        return b"".join(pieces)
    finally:
        os.close(descriptor)


def parse_strict(raw: bytes, label: str) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"strict encoding:{label}",
    )

    def unique_pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, f"duplicate JSON key:{label}:{key}")
            result[key] = value
        return result

    def reject_number(token: str) -> None:
        raise VerificationFailure(f"non-integral JSON number:{label}:{token}")

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique_pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationFailure(f"strict JSON:{label}") from error
    require(isinstance(value, dict), f"top-level object:{label}")
    return value


def load_upstream(name: str) -> dict[str, Any]:
    file_hash, result_hash, schema = UPSTREAM[name]
    raw = guarded_read(HERE / name, 1_200_000_000)
    require(hashlib.sha256(raw).hexdigest() == file_hash, f"file pin:{name}")
    document = parse_strict(raw, name)
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"envelope:{name}",
    )
    require(document["schema"] == schema, f"schema pin:{name}")
    require(
        document["result_sha256"] == result_hash
        and fingerprint(document["result"]) == result_hash,
        f"result pin:{name}",
    )
    require(isinstance(document["result"], dict), f"result object:{name}")
    return document["result"]


def closed_rows(
    table: dict[str, Any],
    identity: str,
    expected: int | None = None,
) -> list[dict[str, Any]]:
    rows = table["rows"]
    require(isinstance(rows, list), f"ledger rows:{identity}")
    require(table["row_count"] == len(rows), f"ledger count:{identity}")
    if expected is not None:
        require(len(rows) == expected, f"expected ledger count:{identity}")
    require(
        len(rows) == len({row[identity] for row in rows}),
        f"unique ledger identity:{identity}",
    )
    require(table["rows_sha256"] == fingerprint(rows), f"ledger digest:{identity}")
    for row in rows:
        body = dict(row)
        closure = body.pop("row_sha256")
        require(closure == fingerprint(body), f"row closure:{identity}")
    return rows


def unpacked_rows(
    result: dict[str, Any],
    table: str,
    expected: int,
) -> Iterable[tuple[dict[str, Any], str]]:
    packed = result[table]
    census = result["table_census_and_sha256"][table]
    columns = result["row_column_schemas"][table]
    require(
        isinstance(packed, list)
        and census["row_count"] == len(packed) == expected
        and census["rows_sha256"] == fingerprint(packed)
        and len(columns) == len(set(columns)),
        f"packed table:{table}",
    )
    for values in packed:
        require(len(values) == len(columns), f"packed width:{table}")
        yield dict(zip(columns, values, strict=True)), fingerprint(values)


def expected_input_binding() -> dict[str, Any]:
    return {
        name: {
            "file_sha256": values[0],
            "result_sha256": values[1],
            "schema": values[2],
        }
        for name, values in sorted(UPSTREAM.items())
    }


def parse_box(values: Any, label: str) -> tuple[Fraction, ...]:
    require(
        isinstance(values, list)
        and len(values) == 6
        and all(isinstance(value, str) for value in values),
        f"box syntax:{label}",
    )
    try:
        box = tuple(Fraction(value) for value in values)
    except (ValueError, ZeroDivisionError) as error:
        raise VerificationFailure(f"exact box:{label}") from error
    require(
        all(box[2 * axis] < box[2 * axis + 1] for axis in range(3)),
        f"positive box:{label}",
    )
    return box


def signature(
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
    result = {
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
    require(set(result) == set(SIGNATURE_FIELDS), "signature field set")
    return result


def append_occurrence(
    rows: list[dict[str, Any]],
    identities: set[str],
    *,
    occurrence_id: str,
    source: str,
    local_signature: dict[str, Any],
    box_values: list[str],
    vertex: str,
    source_row_id: str,
    source_row_sha256: str,
    round264_binding: dict[str, Any] | None,
) -> None:
    require(occurrence_id not in identities, f"unique occurrence:{occurrence_id}")
    require(set(local_signature) == set(SIGNATURE_FIELDS), "complete signature")
    require(
        local_signature["source_chart"] in {"G:E", "G:N", "G:S", "G:W"}
        and isinstance(local_signature["official_key_id"], str)
        and isinstance(local_signature["official_key_ordinal"], int)
        and not isinstance(local_signature["official_key_ordinal"], bool),
        f"signature types:{occurrence_id}",
    )
    box = parse_box(box_values, occurrence_id)
    signature_bytes = encoded(local_signature)
    identities.add(occurrence_id)
    rows.append({
        "id": occurrence_id,
        "source": source,
        "signature": local_signature,
        "signature_bytes": signature_bytes,
        "signature_sha256": hashlib.sha256(signature_bytes).hexdigest(),
        "key_id": local_signature["official_key_id"],
        "key_ordinal": local_signature["official_key_ordinal"],
        "chart": local_signature["source_chart"],
        "box": box,
        "box_text": list(box_values),
        "vertex": vertex,
        "source_row_id": source_row_id,
        "source_row_sha256": source_row_sha256,
        "round264_row": round264_binding,
    })


class UnionFind:
    def __init__(self, values: Iterable[str]) -> None:
        members = list(values)
        self.parent = {value: value for value in members}
        self.weight = {value: 1 for value in members}

    def root(self, value: str) -> str:
        require(value in self.parent, f"union member:{value}")
        root = value
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[value] != value:
            following = self.parent[value]
            self.parent[value] = root
            value = following
        return root

    def merge(self, left: str, right: str) -> bool:
        a = self.root(left)
        b = self.root(right)
        if a == b:
            return False
        if self.weight[a] < self.weight[b] or (
            self.weight[a] == self.weight[b] and a > b
        ):
            a, b = b, a
        self.parent[b] = a
        self.weight[a] += self.weight[b]
        return True


def face_geometry(
    negative: dict[str, Any],
    positive: dict[str, Any],
    axis: int,
    coordinate: Fraction,
) -> dict[str, Any]:
    a = negative["box"]
    b = positive["box"]
    require(
        a[2 * axis + 1] == coordinate and b[2 * axis] == coordinate,
        "oriented common face",
    )
    tangents = [value for value in range(3) if value != axis]
    rectangle: list[Fraction] = []
    equal_face = True
    area = Fraction(1)
    for tangent in tangents:
        left = a[2 * tangent:2 * tangent + 2]
        right = b[2 * tangent:2 * tangent + 2]
        lower, upper = max(left[0], right[0]), min(left[1], right[1])
        require(lower < upper, "positive tangential width")
        rectangle.extend((lower, upper))
        area *= upper - lower
        equal_face = equal_face and left == right
    negative_volume = area * (coordinate - a[2 * axis])
    positive_volume = area * (b[2 * axis + 1] - coordinate)
    require(
        area > 0 and negative_volume > 0 and positive_volume > 0,
        "strict two-sided box corridor",
    )
    return {
        "face_axis": AXES[axis],
        "shared_face_coordinate": fraction_text(coordinate),
        "tangential_axes": [AXES[value] for value in tangents],
        "exact_positive_2D_common_face_rectangle":
            [fraction_text(value) for value in rectangle],
        "exact_positive_2D_common_face_area": fraction_text(area),
        "negative_side_strict_3D_corridor_volume": fraction_text(negative_volume),
        "positive_side_strict_3D_corridor_volume": fraction_text(positive_volume),
        "face_relation": (
            "EXACT_EQUAL_FACE"
            if equal_face
            else "POSITIVE_AREA_PARTIAL_REFINEMENT"
        ),
        "_area": area,
        "_negative_volume": negative_volume,
        "_positive_volume": positive_volume,
    }


def reconstruct_expected() -> dict[str, Any]:
    # First bind the bounded Round174 attachment declaration.
    summary174 = load_upstream(R174_CERT)
    materialization = summary174["materialization_census"]
    attachment = summary174["row_attachment"]
    require(
        materialization["resolved_3d_occurrence_row_count"] == 72_500
        and materialization["observed_exact_key_count"] == 116
        and materialization["volume_conservation_exact"] is True
        and attachment["file_sha256"] == UPSTREAM[R174_ROWS][0]
        and attachment["result_sha256"] == UPSTREAM[R174_ROWS][1]
        and attachment["full_attachment_rows_materialized"] is True
        and summary174["scope"]["all_unique_first_parents_fully_materialized"] is False
        and summary174["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round174 materialization contract",
    )
    del summary174
    gc.collect()

    # Decode and authenticate every complete Round264 frontier independently.
    result264 = load_upstream(R264)
    require(
        result264["census"]["post_Round264_component_count"] == 68_312
        and result264["census"]["complete_occurrence_frontier_count"] == 53_968
        and result264["census"]["complete_exact_key_frontier_count"] == 116
        and result264["census"]["complete_valid_virtual_node_frontier_count"] == 133_284
        and result264["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round264 frontier contract",
    )
    component264_rows = closed_rows(
        result264["formal_post_Round264_component_frontier_ledger"],
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
        for row in component264_rows
    }
    require(len(base_components) == 68_312, "Round264 component uniqueness")
    occurrence264_rows = closed_rows(
        result264["formal_post_Round264_occurrence_frontier_ledger"],
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
        for row in occurrence264_rows
    }
    require(len(base_occurrences) == 53_968, "Round264 occurrence uniqueness")
    key264_rows = closed_rows(
        result264["formal_post_Round264_key_frontier_ledger"],
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
        for row in key264_rows
    }
    require(len(base_keys) == 116, "Round264 key uniqueness")
    virtual264_rows = closed_rows(
        result264["formal_post_Round264_valid_virtual_node_frontier_ledger"],
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
        for row in virtual264_rows
    ]
    require(
        len({item["node_id"] for item in base_virtual}) == 133_284,
        "Round264 virtual uniqueness",
    )
    del (
        result264,
        component264_rows,
        occurrence264_rows,
        key264_rows,
        virtual264_rows,
    )
    gc.collect()

    occurrences: list[dict[str, Any]] = []
    occurrence_ids: set[str] = set()

    rows174 = load_upstream(R174_ROWS)
    for row, row_sha256 in unpacked_rows(
        rows174,
        "resolved_3d_occurrence_rows",
        72_500,
    ):
        require(
            row["ambient_dimension"] == 3
            and row["physical_open_subset_positive"] is True
            and Fraction(row["coordinate_volume"]) > 0,
            f"Round174 positive occurrence:{row['row_id']}",
        )
        local_signature = signature(
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
        append_occurrence(
            occurrences,
            occurrence_ids,
            occurrence_id=row["row_id"],
            source="ROUND174_RESOLVED",
            local_signature=local_signature,
            box_values=row["box"],
            vertex=row["row_id"],
            source_row_id=row["row_id"],
            source_row_sha256=row_sha256,
            round264_binding=None,
        )
    del rows174
    gc.collect()

    rows179 = load_upstream(R179_ROWS)
    for row, row_sha256 in unpacked_rows(
        rows179,
        "resolved_3d_child_rows",
        17_192,
    ):
        require(row["row_id"] in base_occurrences, "Round179 occurrence binding")
        binding = base_occurrences[row["row_id"]]
        local_signature = signature(
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
        require(
            (
                binding["official_key_id"],
                binding["official_key_ordinal"],
            )
            == (
                local_signature["official_key_id"],
                local_signature["official_key_ordinal"],
            ),
            f"Round179 key binding:{row['row_id']}",
        )
        append_occurrence(
            occurrences,
            occurrence_ids,
            occurrence_id=row["row_id"],
            source="ROUND179_RESOLVED",
            local_signature=local_signature,
            box_values=row["box"],
            vertex=binding["current_component_id"],
            source_row_id=row["row_id"],
            source_row_sha256=row_sha256,
            round264_binding=binding,
        )
    del rows179
    gc.collect()

    result204 = load_upstream(R204)
    rows204 = closed_rows(
        result204["formal_local_open_3D_region_ledger"],
        "region_row_id",
        736,
    )
    for row in rows204:
        occurrence_id = row["region_row_id"]
        require(
            occurrence_id in base_occurrences
            and row["ambient_dimension"] == 3
            and row["strict_open_region"] is True
            and row["positive_coordinate_volume"] is True,
            f"Round204 positive occurrence:{occurrence_id}",
        )
        binding = base_occurrences[occurrence_id]
        local_signature = signature(
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
        require(
            (
                binding["official_key_id"],
                binding["official_key_ordinal"],
            )
            == (
                local_signature["official_key_id"],
                local_signature["official_key_ordinal"],
            ),
            f"Round204 key binding:{occurrence_id}",
        )
        append_occurrence(
            occurrences,
            occurrence_ids,
            occurrence_id=occurrence_id,
            source="ROUND204_REGION",
            local_signature=local_signature,
            box_values=row["leaf_exact_box"],
            vertex=binding["current_component_id"],
            source_row_id=occurrence_id,
            source_row_sha256=row["row_sha256"],
            round264_binding=binding,
        )
    del result204, rows204
    gc.collect()

    result208 = load_upstream(R208)
    rows208 = closed_rows(
        result208["formal_local_open_3D_signature_ledger"],
        "region_row_id",
        36_040,
    )
    for row in rows208:
        occurrence_id = row["region_row_id"]
        local_signature = row["local_return_signature"]
        require(
            occurrence_id in base_occurrences
            and row["strict_open_3D_region_exists"] is True
            and row["formal_local_open_3D_signature_credit"] == 1
            and set(local_signature) == set(SIGNATURE_FIELDS),
            f"Round208 positive occurrence:{occurrence_id}",
        )
        binding = base_occurrences[occurrence_id]
        require(
            (
                binding["official_key_id"],
                binding["official_key_ordinal"],
            )
            == (
                local_signature["official_key_id"],
                local_signature["official_key_ordinal"],
            ),
            f"Round208 key binding:{occurrence_id}",
        )
        append_occurrence(
            occurrences,
            occurrence_ids,
            occurrence_id=occurrence_id,
            source="ROUND208_REGION",
            local_signature=local_signature,
            box_values=row["Round182_leaf_box"],
            vertex=binding["current_component_id"],
            source_row_id=occurrence_id,
            source_row_sha256=row["row_sha256"],
            round264_binding=binding,
        )
    del result208, rows208
    gc.collect()

    source_counts = Counter(item["source"] for item in occurrences)
    require(
        dict(sorted(source_counts.items())) == SOURCE_COUNTS,
        "expanded occurrence source census",
    )
    require(len(occurrences) == 126_468, "expanded occurrence universe")
    require(
        {
            item["id"]
            for item in occurrences
            if item["source"] != "ROUND174_RESOLVED"
        }
        == set(base_occurrences),
        "complete prior occurrence reconstruction",
    )
    require(
        {item["key_id"] for item in occurrences} == set(base_keys),
        "complete exact-key universe",
    )

    # Build lower/upper incidence buckets for every exact carrier plane.  The
    # Cartesian products below are the complete candidate universe; no
    # candidate list from Round265 is consulted.
    plane_incidence: dict[
        tuple[str, str, int, Fraction],
        tuple[list[int], list[int]],
    ] = {}
    for index, item in enumerate(occurrences):
        for axis in range(3):
            lower_key = (
                item["key_id"],
                item["chart"],
                axis,
                item["box"][2 * axis],
            )
            upper_key = (
                item["key_id"],
                item["chart"],
                axis,
                item["box"][2 * axis + 1],
            )
            if lower_key not in plane_incidence:
                plane_incidence[lower_key] = ([], [])
            if upper_key not in plane_incidence:
                plane_incidence[upper_key] = ([], [])
            plane_incidence[lower_key][0].append(index)
            plane_incidence[upper_key][1].append(index)

    safe_faces: list[dict[str, Any]] = []
    curved_faces: list[dict[str, Any]] = []
    mismatch_faces: list[dict[str, Any]] = []
    same_key_histogram: Counter[str] = Counter()
    full_signature_histogram: Counter[str] = Counter()
    safe_axis_histogram: Counter[str] = Counter()
    curved_axis_histogram: Counter[str] = Counter()
    mismatch_axis_histogram: Counter[str] = Counter()
    face_relation_histogram: Counter[str] = Counter()
    safe_area = Fraction(0)
    safe_negative_volume = Fraction(0)
    safe_positive_volume = Fraction(0)
    curved_area = Fraction(0)
    mismatch_area = Fraction(0)

    for (key_id, chart, axis, coordinate), (
        positive_indices,
        negative_indices,
    ) in plane_incidence.items():
        if not positive_indices or not negative_indices:
            continue
        tangents = [value for value in range(3) if value != axis]
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
                if any(
                    min(
                        positive["box"][2 * tangent + 1],
                        negative["box"][2 * tangent + 1],
                    )
                    <= max(
                        positive["box"][2 * tangent],
                        negative["box"][2 * tangent],
                    )
                    for tangent in tangents
                ):
                    continue
                require(
                    positive["key_id"] == negative["key_id"] == key_id
                    and positive["chart"] == negative["chart"] == chart,
                    "plane incidence key/chart purity",
                )
                pair_type = "|".join(
                    sorted((positive["source"], negative["source"]))
                )
                same_key_histogram[pair_type] += 1
                geometry = face_geometry(negative, positive, axis, coordinate)
                common = {
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
                        if positive["signature"][field]
                        != negative["signature"][field]
                    ]
                    require(differing, "nonempty signature mismatch")
                    common["row_id"] = (
                        "round265-signature-mismatch-nonedge:"
                        + fingerprint([
                            negative["id"],
                            positive["id"],
                            AXES[axis],
                            fraction_text(coordinate),
                            geometry[
                                "exact_positive_2D_common_face_rectangle"
                            ],
                        ])
                    )
                    common["differing_fields"] = differing
                    mismatch_faces.append(common)
                    mismatch_axis_histogram[f"{AXES[axis]}:{pair_type}"] += 1
                    mismatch_area += geometry["_area"]
                    continue

                require(
                    positive["signature"] == negative["signature"],
                    "signature byte/object agreement",
                )
                full_signature_histogram[pair_type] += 1
                if pair_type in {
                    "ROUND174_RESOLVED|ROUND174_RESOLVED",
                    "ROUND174_RESOLVED|ROUND179_RESOLVED",
                }:
                    common["row_id"] = (
                        "round265-safe-full-signature-face-edge:"
                        + fingerprint([
                            negative["id"],
                            positive["id"],
                            AXES[axis],
                            fraction_text(coordinate),
                            geometry[
                                "exact_positive_2D_common_face_rectangle"
                            ],
                        ])
                    )
                    common["vertex_pair"] = tuple(sorted((
                        negative["vertex"],
                        positive["vertex"],
                    )))
                    require(
                        common["vertex_pair"][0] != common["vertex_pair"][1],
                        f"distinct safe seeds:{common['row_id']}",
                    )
                    safe_faces.append(common)
                    safe_axis_histogram[f"{AXES[axis]}:{pair_type}"] += 1
                    face_relation_histogram[geometry["face_relation"]] += 1
                    safe_area += geometry["_area"]
                    safe_negative_volume += geometry["_negative_volume"]
                    safe_positive_volume += geometry["_positive_volume"]
                else:
                    require(
                        pair_type in {
                            "ROUND174_RESOLVED|ROUND204_REGION",
                            "ROUND174_RESOLVED|ROUND208_REGION",
                        },
                        f"curved pair class:{pair_type}",
                    )
                    common["row_id"] = (
                        "round265-curved-face-failclosed:"
                        + fingerprint([
                            negative["id"],
                            positive["id"],
                            AXES[axis],
                            fraction_text(coordinate),
                            geometry[
                                "exact_positive_2D_common_face_rectangle"
                            ],
                        ])
                    )
                    common["vertex_pair"] = tuple(sorted((
                        negative["vertex"],
                        positive["vertex"],
                    )))
                    curved_faces.append(common)
                    curved_axis_histogram[f"{AXES[axis]}:{pair_type}"] += 1
                    curved_area += geometry["_area"]

    safe_faces.sort(key=lambda item: item["row_id"])
    curved_faces.sort(key=lambda item: item["row_id"])
    mismatch_faces.sort(key=lambda item: item["row_id"])
    all_disposition_ids = (
        [item["row_id"] for item in safe_faces]
        + [item["row_id"] for item in curved_faces]
        + [item["row_id"] for item in mismatch_faces]
    )
    require(
        len(all_disposition_ids)
        == len(set(all_disposition_ids))
        == 174_108,
        "complete disposition identity partition",
    )
    require(
        dict(sorted(full_signature_histogram.items())) == FULL_FACE_HISTOGRAM,
        "full-signature face histogram",
    )
    require(
        (len(safe_faces), len(curved_faces), len(mismatch_faces))
        == (169_064, 2_652, 2_392),
        "face disposition partition",
    )
    require(
        dict(sorted(safe_axis_histogram.items())) == SAFE_AXIS_HISTOGRAM,
        "safe face axis histogram",
    )
    require(
        dict(sorted(curved_axis_histogram.items())) == CURVED_AXIS_HISTOGRAM,
        "curved face axis histogram",
    )
    require(
        set(same_key_histogram)
        == {
            "ROUND174_RESOLVED|ROUND174_RESOLVED",
            "ROUND174_RESOLVED|ROUND179_RESOLVED",
            "ROUND174_RESOLVED|ROUND204_REGION",
            "ROUND174_RESOLVED|ROUND208_REGION",
        }
        and same_key_histogram["ROUND174_RESOLVED|ROUND208_REGION"] == 4_948
        and all(
            item["pair_type"] == "ROUND174_RESOLVED|ROUND208_REGION"
            for item in mismatch_faces
        ),
        "signature mismatch channel confinement",
    )
    require(
        dict(sorted(face_relation_histogram.items()))
        == {
            "EXACT_EQUAL_FACE": 67_100,
            "POSITIVE_AREA_PARTIAL_REFINEMENT": 101_964,
        },
        "safe face relation histogram",
    )

    # Saturate in the deterministic closed-row order.  Rank flags are thus
    # independently fixed, including every redundant edge.
    round174_ids = {
        item["id"]
        for item in occurrences
        if item["source"] == "ROUND174_RESOLVED"
    }
    seed_ids = sorted(set(base_components) | round174_ids)
    require(len(seed_ids) == 140_812, "expanded seed universe")
    union = UnionFind(seed_ids)
    for item in safe_faces:
        item["rank_reducing"] = union.merge(*item["vertex_pair"])
    rank_reductions = sum(item["rank_reducing"] for item in safe_faces)
    require(
        rank_reductions == 77_000
        and len(safe_faces) - rank_reductions == 92_064
        and len({item["vertex_pair"] for item in safe_faces}) == 162_424,
        "safe face union census",
    )
    classes: dict[str, list[str]] = defaultdict(list)
    for seed_id in seed_ids:
        classes[union.root(seed_id)].append(seed_id)
    require(len(classes) == 63_812, "post-face quotient count")

    occurrence_by_id = {item["id"]: item for item in occurrences}
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
    require(set(seed_descriptors) == set(seed_ids), "complete seed descriptors")

    post_id_by_seed: dict[str, str] = {}
    post_class_seeds: dict[str, list[str]] = {}
    post_descriptor_hash: dict[str, str] = {}
    for members in classes.values():
        members.sort()
        descriptors = [seed_descriptors[value] for value in members]
        keys = {seed_key[value] for value in members}
        require(len(keys) == 1, "exact-key-pure expanded component")
        post_id = "round265-expanded-face-component:" + fingerprint(descriptors)
        require(post_id not in post_class_seeds, f"unique component:{post_id}")
        post_class_seeds[post_id] = members
        post_descriptor_hash[post_id] = fingerprint(descriptors)
        for value in members:
            post_id_by_seed[value] = post_id

    safe_rows: list[dict[str, Any]] = []
    safe_edge_count_by_post: Counter[str] = Counter()
    safe_rank_count_by_post: Counter[str] = Counter()
    safe_edge_count_by_key: Counter[str] = Counter()
    safe_rank_count_by_key: Counter[str] = Counter()
    for item in safe_faces:
        negative = item["negative"]
        positive = item["positive"]
        geometry = item["geometry"]
        post_id = post_id_by_seed[item["vertex_pair"][0]]
        require(
            post_id == post_id_by_seed[item["vertex_pair"][1]],
            "safe edge post assignment",
        )
        safe_edge_count_by_post[post_id] += 1
        safe_rank_count_by_post[post_id] += int(item["rank_reducing"])
        safe_edge_count_by_key[item["key_id"]] += 1
        safe_rank_count_by_key[item["key_id"]] += int(item["rank_reducing"])
        safe_rows.append(seal({
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
    for item in curved_faces:
        negative = item["negative"]
        positive = item["positive"]
        geometry = item["geometry"]
        post_pair = tuple(sorted((
            post_id_by_seed[negative["vertex"]],
            post_id_by_seed[positive["vertex"]],
        )))
        internal = post_pair[0] == post_pair[1]
        curved_internal_count += int(internal)
        curved_rows.append(seal({
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
    for item in mismatch_faces:
        negative = item["negative"]
        positive = item["positive"]
        geometry = item["geometry"]
        vertex_pair = tuple(sorted((
            negative["vertex"],
            positive["vertex"],
        )))
        post_pair = tuple(sorted((
            post_id_by_seed[vertex_pair[0]],
            post_id_by_seed[vertex_pair[1]],
        )))
        internal = post_pair[0] == post_pair[1]
        mismatch_internal_count += int(internal)
        mismatch_rows.append(seal({
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

    seed_map_rows: list[dict[str, Any]] = []
    for seed_id in seed_ids:
        descriptor = seed_descriptors[seed_id]
        key_id, ordinal = seed_key[seed_id]
        seed_map_rows.append(seal({
            "expanded_seed_to_Round265_component_map_row_id":
                "round265-seed-map:" + fingerprint([seed_id]),
            "seed_id": seed_id,
            "seed_kind": descriptor["seed_kind"],
            "official_key_id": key_id,
            "official_key_ordinal": ordinal,
            "source_row_id": descriptor["source_row_id"],
            "source_row_sha256": descriptor["source_row_sha256"],
            "seed_descriptor_sha256": fingerprint(descriptor),
            "post_Round265_quotient_component_id": post_id_by_seed[seed_id],
            "maximality_credit": 0,
        }))

    occurrence_rows: list[dict[str, Any]] = []
    occurrence_count_by_post: Counter[str] = Counter()
    occurrence_count_by_key: Counter[str] = Counter()
    round174_count_by_post: Counter[str] = Counter()
    round174_count_by_key: Counter[str] = Counter()
    for item in sorted(occurrences, key=lambda value: value["id"]):
        post_id = post_id_by_seed[item["vertex"]]
        occurrence_count_by_post[post_id] += 1
        occurrence_count_by_key[item["key_id"]] += 1
        if item["source"] == "ROUND174_RESOLVED":
            round174_count_by_post[post_id] += 1
            round174_count_by_key[item["key_id"]] += 1
        binding = item["round264_row"]
        occurrence_rows.append(seal({
            "post_Round265_expanded_occurrence_frontier_row_id":
                "round265-expanded-occurrence:" + fingerprint([item["id"]]),
            "local_occurrence_row_id": item["id"],
            "occurrence_source": item["source"],
            "official_key_id": item["key_id"],
            "official_key_ordinal": item["key_ordinal"],
            "source_chart": item["chart"],
            "complete_10_field_return_signature_sha256":
                item["signature_sha256"],
            "exact_box_sha256": fingerprint(item["box_text"]),
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
    require(len(occurrence_rows) == 126_468, "occurrence frontier count")

    virtual_rows: list[dict[str, Any]] = []
    virtual_count_by_post: Counter[str] = Counter()
    virtual_count_by_key: Counter[str] = Counter()
    for item in sorted(base_virtual, key=lambda value: value["node_id"]):
        old_component = item["current_component_id"]
        post_id = post_id_by_seed[old_component]
        require(
            item["official_key_id"]
            == base_components[old_component]["official_key_id"],
            f"virtual node key purity:{item['node_id']}",
        )
        virtual_count_by_post[post_id] += 1
        virtual_count_by_key[item["official_key_id"]] += 1
        virtual_rows.append(seal({
            "post_Round265_valid_virtual_node_frontier_row_id":
                "round265-valid-virtual-node:" + fingerprint([item["node_id"]]),
            "valid_virtual_stratum_node_id": item["node_id"],
            "virtual_node_kind": item["kind"],
            "official_key_id": item["official_key_id"],
            "source_Round264_valid_virtual_node_frontier_row_id":
                item["source_row_id"],
            "source_Round264_valid_virtual_node_frontier_row_sha256":
                item["source_row_sha256"],
            "post_Round264_quotient_component_id": old_component,
            "post_Round265_quotient_component_id": post_id,
            "valid_virtual_node_identity_preserved": True,
            "maximality_credit": 0,
        }))
    require(len(virtual_rows) == 133_284, "valid virtual frontier count")

    classes_with_old = {
        post_id
        for post_id, members in post_class_seeds.items()
        if any(value in base_components for value in members)
    }
    round174_attached_count = sum(
        round174_count_by_post[post_id]
        for post_id in classes_with_old
    )
    round174_only_classes = set(post_class_seeds) - classes_with_old
    require(
        round174_attached_count == 67_620
        and len(round174_only_classes) == 1_948,
        "Round174 attachment census",
    )

    component_rows: list[dict[str, Any]] = []
    component_count_by_key: Counter[str] = Counter()
    round174_only_count_by_key: Counter[str] = Counter()
    expanded_member_sum = 0
    seed_class_size_histogram: Counter[int] = Counter()
    for post_id in sorted(post_class_seeds):
        members = post_class_seeds[post_id]
        keys = {seed_key[value] for value in members}
        require(len(keys) == 1, f"component key purity:{post_id}")
        key_id, ordinal = next(iter(keys))
        old_count = sum(value in base_components for value in members)
        round174_seed_count = len(members) - old_count
        occurrence_count = occurrence_count_by_post[post_id]
        virtual_count = virtual_count_by_post[post_id]
        member_count = occurrence_count + virtual_count
        require(member_count > 0, f"nonempty component:{post_id}")
        expanded_member_sum += member_count
        component_count_by_key[key_id] += 1
        if old_count == 0:
            round174_only_count_by_key[key_id] += 1
        seed_class_size_histogram[len(members)] += 1
        component_rows.append(seal({
            "post_Round265_component_frontier_row_id":
                "round265-component-row:" + fingerprint([post_id]),
            "post_Round265_quotient_component_id": post_id,
            "official_key_id": key_id,
            "official_key_ordinal": ordinal,
            "constituent_seed_count": len(members),
            "constituent_seed_ids": members,
            "constituent_seed_ids_sha256": fingerprint(members),
            "constituent_seed_descriptors_sha256":
                post_descriptor_hash[post_id],
            "constituent_Round264_component_count": old_count,
            "constituent_Round174_occurrence_seed_count": round174_seed_count,
            "safe_full_signature_face_edge_count":
                safe_edge_count_by_post[post_id],
            "safe_full_signature_rank_reduction_count":
                safe_rank_count_by_post[post_id],
            "expanded_occurrence_member_count": occurrence_count,
            "Round174_occurrence_member_count":
                round174_count_by_post[post_id],
            "valid_virtual_stratum_node_count": virtual_count,
            "expanded_member_count": member_count,
            "component_class":
                "R174_ONLY" if old_count == 0 else "ATTACHED_TO_ROUND264",
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
        }))
    require(
        len(component_rows) == 63_812
        and expanded_member_sum == 259_752,
        "component/member frontier conservation",
    )

    key_rows: list[dict[str, Any]] = []
    round174_seed_count_by_key: Counter[str] = Counter(
        occurrence_by_id[value]["key_id"] for value in round174_ids
    )
    old_seed_count_by_key: Counter[str] = Counter(
        item["official_key_id"] for item in base_components.values()
    )
    for key_id in sorted(base_keys):
        item = base_keys[key_id]
        pre_seed_count = (
            old_seed_count_by_key[key_id]
            + round174_seed_count_by_key[key_id]
        )
        post_count = component_count_by_key[key_id]
        rank_reduction = pre_seed_count - post_count
        require(
            occurrence_count_by_key[key_id]
            == item["occurrence_count"] + round174_count_by_key[key_id]
            and virtual_count_by_key[key_id] == item["valid_virtual_count"]
            and rank_reduction == safe_rank_count_by_key[key_id],
            f"key conservation:{key_id}",
        )
        key_rows.append(seal({
            "post_Round265_key_frontier_row_id":
                "round265-key-frontier:" + fingerprint([key_id]),
            "official_key_id": key_id,
            "official_key_ordinal": item["official_key_ordinal"],
            "source_Round264_key_frontier_row_id": item["source_row_id"],
            "source_Round264_key_frontier_row_sha256": item["source_row_sha256"],
            "pre_Round265_Round264_component_seed_count":
                old_seed_count_by_key[key_id],
            "pre_Round265_Round174_occurrence_seed_count":
                round174_seed_count_by_key[key_id],
            "pre_Round265_expanded_seed_count": pre_seed_count,
            "safe_full_signature_face_edge_count":
                safe_edge_count_by_key[key_id],
            "safe_full_signature_rank_reduction_count": rank_reduction,
            "post_Round265_quotient_component_count": post_count,
            "post_Round265_R174_only_component_count":
                round174_only_count_by_key[key_id],
            "expanded_occurrence_count": occurrence_count_by_key[key_id],
            "Round174_occurrence_count": round174_count_by_key[key_id],
            "valid_virtual_stratum_node_count": virtual_count_by_key[key_id],
            "expanded_member_count":
                occurrence_count_by_key[key_id]
                + virtual_count_by_key[key_id],
            "occurrence_quotient_assignment_complete": True,
            "all_quotient_components_proved_maximal": False,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
        }))
    require(
        len(key_rows) == 116
        and sum(component_count_by_key.values()) == 63_812
        and sum(occurrence_count_by_key.values()) == 126_468
        and sum(virtual_count_by_key.values()) == 133_284,
        "complete key frontier",
    )

    disposition_commitment = seal({
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
        "safe_edge_row_ids_sha256": fingerprint([
            row["safe_full_signature_face_edge_row_id"]
            for row in safe_rows
        ]),
        "curved_failclosed_row_ids_sha256": fingerprint([
            row["curved_face_failclosed_row_id"]
            for row in curved_rows
        ]),
        "signature_mismatch_nonedge_row_ids_sha256": fingerprint([
            row["same_key_signature_mismatch_nonedge_row_id"]
            for row in mismatch_rows
        ]),
        "all_disposition_row_ids_sha256":
            fingerprint(sorted(all_disposition_ids)),
        "key_equality_alone_authorizes_physical_edge": False,
        "physical_edge_requires_complete_signature_equality": True,
    })

    census = {
        "Round264_corrected_component_seed_count": 68_312,
        "new_Round174_resolved_occurrence_seed_count": 72_500,
        "pre_Round265_expanded_seed_count": 140_812,
        "expanded_occurrence_source_histogram":
            dict(sorted(source_counts.items())),
        "expanded_occurrence_count": 126_468,
        "valid_virtual_stratum_node_count": 133_284,
        "expanded_member_count": 259_752,
        "exact_key_count": 116,
        "same_key_same_chart_face_carrier_group_count": len(plane_incidence),
        "same_key_positive_area_face_candidate_count": 174_108,
        "same_key_positive_area_face_pair_histogram":
            dict(sorted(same_key_histogram.items())),
        "full_10_field_signature_equal_face_histogram":
            dict(sorted(full_signature_histogram.items())),
        "safe_full_signature_resolved_box_face_edge_count": 169_064,
        "safe_full_signature_face_axis_histogram":
            dict(sorted(safe_axis_histogram.items())),
        "safe_exact_equal_face_count": 67_100,
        "safe_positive_area_partial_refinement_face_count": 101_964,
        "safe_distinct_pre_seed_pair_count": 162_424,
        "safe_rank_reducing_edge_count": 77_000,
        "safe_redundant_edge_count": 92_064,
        "safe_exact_positive_2D_common_face_area_sum":
            fraction_text(safe_area),
        "safe_negative_side_strict_3D_corridor_volume_sum":
            fraction_text(safe_negative_volume),
        "safe_positive_side_strict_3D_corridor_volume_sum":
            fraction_text(safe_positive_volume),
        "curved_graph_side_failclosed_face_count": 2_652,
        "curved_graph_side_face_axis_histogram":
            dict(sorted(curved_axis_histogram.items())),
        "curved_enclosing_box_positive_face_area_sum":
            fraction_text(curved_area),
        "curved_post_safe_face_internal_pair_count": curved_internal_count,
        "curved_post_safe_face_cross_component_pair_count":
            2_652 - curved_internal_count,
        "same_key_complete_signature_mismatch_nonedge_count": 2_392,
        "signature_mismatch_axis_histogram":
            dict(sorted(mismatch_axis_histogram.items())),
        "signature_mismatch_enclosing_box_positive_face_area_sum":
            fraction_text(mismatch_area),
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
        "formal_input_binding": expected_input_binding(),
        "formal_complete_same_key_face_disposition_commitment_ledger":
            make_ledger(
                [disposition_commitment],
                "complete_same_key_face_disposition_commitment_row_id",
            ),
        "formal_safe_full_signature_resolved_box_face_edge_ledger":
            make_ledger(
                safe_rows,
                "safe_full_signature_face_edge_row_id",
            ),
        "formal_curved_graph_side_face_failclosed_ledger":
            make_ledger(curved_rows, "curved_face_failclosed_row_id"),
        "formal_same_key_complete_signature_mismatch_nonedge_ledger":
            make_ledger(
                mismatch_rows,
                "same_key_signature_mismatch_nonedge_row_id",
            ),
        "formal_expanded_seed_to_Round265_component_map_ledger":
            make_ledger(
                seed_map_rows,
                "expanded_seed_to_Round265_component_map_row_id",
            ),
        "formal_post_Round265_component_frontier_ledger":
            make_ledger(
                component_rows,
                "post_Round265_component_frontier_row_id",
            ),
        "formal_post_Round265_expanded_occurrence_frontier_ledger":
            make_ledger(
                occurrence_rows,
                "post_Round265_expanded_occurrence_frontier_row_id",
            ),
        "formal_post_Round265_key_frontier_ledger":
            make_ledger(key_rows, "post_Round265_key_frontier_row_id"),
        "formal_post_Round265_valid_virtual_node_frontier_ledger":
            make_ledger(
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
            "schema": CANDIDATE_SCHEMA,
            "producer_sha256": PRODUCER_SHA256,
            "python_version": sys.version.split()[0],
            "upstream_producer_imported_or_executed": False,
            "arithmetic": "fractions.Fraction exact rational",
            "seed_affects_output": False,
        },
    }


def canonical_line(raw: bytes, value: Any) -> bool:
    offset = 0
    for piece in encoded_chunks(value):
        following = offset + len(piece)
        if raw[offset:following] != piece:
            return False
        offset = following
    return raw[offset:] == b"\n"


def candidate_matches(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> bool:
    try:
        require(
            set(document) == {"schema", "result", "result_sha256"},
            "candidate envelope",
        )
        require(document["schema"] == CANDIDATE_SCHEMA, "candidate schema")
        require(isinstance(document["result"], dict), "candidate result object")
        require(
            document["result_sha256"] == CANDIDATE_RESULT_SHA256,
            "candidate fixed result pin",
        )
        require(
            fingerprint(document["result"]) == CANDIDATE_RESULT_SHA256,
            "candidate result closure",
        )
        require(document["result"] == expected, "complete expected equality")
        return True
    except (VerificationFailure, KeyError, TypeError, ValueError):
        return False


def assign_path(root: Any, path: tuple[Any, ...], replacement: Any) -> Any:
    target = root
    for part in path[:-1]:
        target = target[part]
    old = target[path[-1]]
    target[path[-1]] = replacement
    return old


def reclose_ledger(ledger: dict[str, Any]) -> None:
    rows = ledger["rows"]
    for row in rows:
        body = dict(row)
        body.pop("row_sha256")
        row["row_sha256"] = fingerprint(body)
    ledger["rows_sha256"] = fingerprint(rows)
    ledger["row_hashes_sha256"] = fingerprint(
        [row["row_sha256"] for row in rows]
    )


def semantic_attack_suite(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    attacks: list[tuple[str, tuple[Any, ...], Any, str | None]] = [
        (
            "invent_component",
            ("result", "census", "post_Round265_component_count"),
            63_813,
            None,
        ),
        (
            "promote_maximality",
            (
                "result",
                "strict_nonpromotion",
                "maximal_physical_component_credit",
            ),
            1,
            None,
        ),
        (
            "authorize_same_key_glue",
            (
                "result",
                "scope_contract",
                "same_key_is_not_used_as_a_physical_glue_rule",
            ),
            False,
            None,
        ),
        (
            "forge_producer_pin",
            ("result", "provenance", "producer_sha256"),
            "0" * 64,
            None,
        ),
        (
            "erase_disposition",
            (
                "result",
                "formal_complete_same_key_face_disposition_commitment_ledger",
                "rows",
                0,
                "same_key_positive_area_face_candidate_count",
            ),
            174_107,
            "formal_complete_same_key_face_disposition_commitment_ledger",
        ),
        (
            "invent_safe_rank_credit",
            (
                "result",
                "formal_safe_full_signature_resolved_box_face_edge_ledger",
                "rows",
                0,
                "component_union_credit",
            ),
            7,
            None,
        ),
        (
            "promote_curved_face",
            (
                "result",
                "formal_curved_graph_side_face_failclosed_ledger",
                "rows",
                0,
                "physical_glue_credit",
            ),
            1,
            "formal_curved_graph_side_face_failclosed_ledger",
        ),
        (
            "promote_signature_mismatch",
            (
                "result",
                "formal_same_key_complete_signature_mismatch_nonedge_ledger",
                "rows",
                0,
                "complete_10_field_return_signature_equal",
            ),
            True,
            "formal_same_key_complete_signature_mismatch_nonedge_ledger",
        ),
        (
            "promote_component_row",
            (
                "result",
                "formal_post_Round265_component_frontier_ledger",
                "rows",
                0,
                "maximal_physical_component_claimed",
            ),
            True,
            None,
        ),
        (
            "redirect_occurrence",
            (
                "result",
                "formal_post_Round265_expanded_occurrence_frontier_ledger",
                "rows",
                0,
                "post_Round265_quotient_component_id",
            ),
            "round265-expanded-face-component:forged",
            None,
        ),
        (
            "exhaust_key",
            (
                "result",
                "formal_post_Round265_key_frontier_ledger",
                "rows",
                0,
                "global_exact_key_fibre_exhausted",
            ),
            True,
            "formal_post_Round265_key_frontier_ledger",
        ),
        (
            "promote_virtual_node",
            (
                "result",
                "formal_post_Round265_valid_virtual_node_frontier_ledger",
                "rows",
                0,
                "maximality_credit",
            ),
            1,
            None,
        ),
    ]
    rejected = 0
    reclosed_count = 0
    for label, path, replacement, ledger_name in attacks:
        old = assign_path(candidate, path, replacement)
        if ledger_name is not None:
            reclose_ledger(candidate["result"][ledger_name])
            reclosed_count += 1
        candidate["result_sha256"] = fingerprint(candidate["result"])
        rejected += int(not candidate_matches(candidate, expected))
        assign_path(candidate, path, old)
        if ledger_name is not None:
            reclose_ledger(candidate["result"][ledger_name])
        candidate["result_sha256"] = CANDIDATE_RESULT_SHA256
    require(candidate_matches(candidate, expected), "candidate attack restoration")
    return {
        "attack_count": len(attacks),
        "rejected_count": rejected,
        "all_attacks_resigned_at_result_level": True,
        "small_ledger_attacks_reclosed_at_row_and_ledger_levels":
            reclosed_count,
        "attack_labels": [label for label, *_rest in attacks],
    }


def strict_json_attack_suite() -> dict[str, Any]:
    attacks: list[tuple[str, bytes]] = [
        ("duplicate_key", b'{"a":1,"a":2}'),
        ("float", b'{"a":1.5}'),
        ("exponent", b'{"a":1e2}'),
        ("nan", b'{"a":NaN}'),
        ("infinity", b'{"a":Infinity}'),
        ("negative_infinity", b'{"a":-Infinity}'),
        ("bom", b'\xef\xbb\xbf{"a":1}'),
        ("nul", b'{"a":"\\u0000"}\x00'),
        ("trailing", b'{"a":1} x'),
        ("two_documents", b'{"a":1}{"b":2}'),
        ("top_array", b"[]"),
        ("top_string", b'"x"'),
        ("top_integer", b"1"),
        ("invalid_utf8", b'{"a":"\xff"}'),
        ("truncated", b'{"a":'),
        ("unquoted_key", b"{a:1}"),
        ("comment", b'{"a":1/*x*/}'),
    ]
    rejected = 0
    for label, raw in attacks:
        try:
            parse_strict(raw, f"attack:{label}")
        except VerificationFailure:
            rejected += 1
    return {
        "attack_count": len(attacks),
        "rejected_count": rejected,
        "attack_labels": [label for label, _raw in attacks],
    }


def file_attack_suite() -> dict[str, Any]:
    rejected = 0
    labels: list[str] = []
    with tempfile.TemporaryDirectory(prefix="round265-verifier-files-") as name:
        root = Path(name)
        regular = root / "regular"
        regular.write_bytes(b"x")
        cases: list[tuple[str, Path, int, Path | None, int | None]] = [
            ("wrong_parent", regular, 100, HERE, None),
        ]
        empty = root / "empty"
        empty.write_bytes(b"")
        cases.append(("empty", empty, 100, None, None))
        directory = root / "directory"
        directory.mkdir()
        cases.append(("directory", directory, 100, None, None))
        cases.append(("missing", root / "missing", 100, None, None))
        symlink = root / "symlink"
        symlink.symlink_to(regular)
        cases.append(("symlink", symlink, 100, None, None))
        hardlink = root / "hardlink"
        os.link(regular, hardlink)
        cases.append(("hardlink", hardlink, 100, None, None))
        oversized = root / "oversized"
        oversized.write_bytes(b"xx")
        cases.append(("oversized", oversized, 1, None, None))
        wrong_size = root / "wrong-size"
        wrong_size.write_bytes(b"x")
        cases.append(("wrong_exact_size", wrong_size, 100, None, 2))
        fifo = root / "fifo"
        os.mkfifo(fifo)
        cases.append(("fifo", fifo, 100, None, None))
        for label, path, maximum, parent, exact_size in cases:
            labels.append(label)
            try:
                guarded_read(path, maximum, parent, exact_size)
            except (VerificationFailure, FileNotFoundError):
                rejected += 1
    return {
        "attack_count": len(labels),
        "rejected_count": rejected,
        "attack_labels": labels,
    }


def atomic_write(raw: bytes) -> None:
    require(OUTPUT.parent == HERE, "output parent")
    if OUTPUT.exists() or OUTPUT.is_symlink():
        information = OUTPUT.lstat()
        require(
            stat.S_ISREG(information.st_mode)
            and not OUTPUT.is_symlink()
            and information.st_nlink == 1,
            "safe existing output",
        )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.",
        suffix=".tmp",
        dir=HERE,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=265_071)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    require(
        isinstance(arguments.seed, int) and not isinstance(arguments.seed, bool),
        "integral seed",
    )

    # Producer is never compiled, imported, evaluated, or used as data.
    producer_raw = guarded_read(PRODUCER, 5_000_000)
    require(
        hashlib.sha256(producer_raw).hexdigest() == PRODUCER_SHA256,
        "producer inert-byte pin",
    )
    del producer_raw

    # This is the key ordering invariant: the entire expected result, including
    # every row of every ledger, exists and is pinned before candidate lstat.
    expected = reconstruct_expected()
    expected_result_sha256 = fingerprint(expected)
    require(
        expected_result_sha256 == CANDIDATE_RESULT_SHA256,
        "independently reconstructed result pin",
    )

    candidate_raw = guarded_read(
        CANDIDATE,
        1_000_000_000,
        HERE,
        CANDIDATE_SIZE,
    )
    require(
        hashlib.sha256(candidate_raw).hexdigest() == CANDIDATE_SHA256,
        "candidate file pin",
    )
    candidate = parse_strict(candidate_raw, CANDIDATE.name)
    require(canonical_line(candidate_raw, candidate), "canonical candidate bytes")
    require(candidate_matches(candidate, expected), "complete candidate equality")
    del candidate_raw
    gc.collect()

    semantic = semantic_attack_suite(candidate, expected)
    require(
        semantic["rejected_count"] == semantic["attack_count"],
        "semantic attacks",
    )
    strict_attacks = strict_json_attack_suite()
    require(
        strict_attacks["rejected_count"] == strict_attacks["attack_count"],
        "strict JSON attacks",
    )
    file_attacks = file_attack_suite()
    require(
        file_attacks["rejected_count"] == file_attacks["attack_count"],
        "file attacks",
    )

    census = expected["census"]
    verification = {
        "status": "PASS_INDEPENDENT_ROUND265",
        "producer_file_sha256": PRODUCER_SHA256,
        "candidate_file_sha256": CANDIDATE_SHA256,
        "candidate_file_size": CANDIDATE_SIZE,
        "candidate_result_sha256": CANDIDATE_RESULT_SHA256,
        "independently_reconstructed_result_sha256":
            expected_result_sha256,
        "verified_census": {
            "expanded_seed_count":
                census["pre_Round265_expanded_seed_count"],
            "expanded_occurrence_count":
                census["expanded_occurrence_count"],
            "same_key_positive_area_face_candidate_count":
                census["same_key_positive_area_face_candidate_count"],
            "safe_face_edge_count":
                census[
                    "safe_full_signature_resolved_box_face_edge_count"
                ],
            "safe_rank_reducing_edge_count":
                census["safe_rank_reducing_edge_count"],
            "curved_failclosed_face_count":
                census["curved_graph_side_failclosed_face_count"],
            "signature_mismatch_nonedge_count":
                census[
                    "same_key_complete_signature_mismatch_nonedge_count"
                ],
            "post_Round265_component_count":
                census["post_Round265_component_count"],
            "exact_key_count": census["exact_key_count"],
            "valid_virtual_node_count":
                census["valid_virtual_stratum_node_count"],
            "expanded_member_count": census["expanded_member_count"],
        },
        "verified_ledger_row_counts": {
            key: value["row_count"]
            for key, value in expected.items()
            if isinstance(value, dict) and "rows" in value
        },
        "semantic_attack_suite": semantic,
        "strict_json_attack_suite": strict_attacks,
        "file_attack_suite": file_attacks,
        "independence_contract": {
            "Round265_producer_imported_or_executed": False,
            "expected_object_completed_before_candidate_open": True,
            "complete_expected_object_equality_required": True,
            "complete_candidate_canonical_bytes_required": True,
            "candidate_exact_byte_size_required": True,
            "all_upstream_files_schema_result_and_file_pinned": True,
            "exact_arithmetic": "fractions.Fraction",
            "seed_affects_output": False,
        },
    }
    envelope = {
        "schema": VERIFICATION_SCHEMA,
        "result": verification,
        "result_sha256": fingerprint(verification),
    }
    raw = encoded(envelope) + b"\n"
    if not arguments.no_write:
        atomic_write(raw)
    print(verification["status"])
    print(
        "occurrences=126468 dispositions=174108 "
        "safe=169064 curved=2652 mismatch=2392"
    )
    print(
        "seeds=140812 rank=77000 components=63812 "
        "frontiers=126468/116/133284 members=259752"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        VerificationFailure,
        OSError,
        KeyError,
        TypeError,
        ValueError,
    ) as error:
        print(f"FAIL_CLOSED_ROUND265_VERIFIER:{error}", file=sys.stderr)
        raise SystemExit(1)
