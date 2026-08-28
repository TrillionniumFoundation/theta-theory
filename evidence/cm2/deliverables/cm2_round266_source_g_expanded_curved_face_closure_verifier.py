#!/usr/bin/env python3
"""Independent verifier for expanded Round266 curved-face closure.

The producer is pinned as inert bytes and is never imported or executed.
This verifier independently reconstructs all 2,652 candidates, reruns the
fixed-precision geometry and corridor tests, rebuilds the quotient/frontiers,
and completes the expected object before opening the candidate.

Round265 freezes a 63,812-component quotient on 126,468 positive-open
occurrences and 133,284 valid virtual strata.  It leaves exactly 2,652
full-signature-equal R174--R204/R208 positive-area box-face candidates
fail-closed.  This producer independently reconstructs those candidates
from the frozen R174/R204/R208 geometry, imports only the hash-pinned
R259/R260 evaluator chain, and evaluates every complete common face with
fixed 256-bit Arb arithmetic.

All 2,652 complete faces are strict MATCH cells at canonical depth zero.
Every match also carries one strict inward 3D corridor for each incident
occurrence.  The resulting 2,652 certified edges induce 588 rank reductions
and rebuild the quotient from 63,812 to 63,224 components.

Complete component, occurrence, exact-key, valid-virtual-node, and unified
259,752-row member frontiers are rebuilt.  No maximality, exact-key-fibre,
global-disposition, Jx/Jy same-point glue, Gate5, D02, or CM2 credit is
granted.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gc
import hashlib
import importlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable

from flint import ctx, __version__ as FLINT_VERSION


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round266_source_g_expanded_curved_face_closure"
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE = HERE / f"{PREFIX}_certificate.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"
SCHEMA = "cm2.round266.source-g-expanded-curved-face-closure.v1"
VERIFICATION_SCHEMA = (
    "cm2.round266.source-g-expanded-curved-face-closure-verification.v1"
)
PRODUCER_SHA256 = (
    "22c2fa3555a69681f724088ad01d080e5f8925ae974f5e69307d72badd08a999"
)
CANDIDATE_SHA256 = (
    "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"
)
CANDIDATE_RESULT_SHA256 = (
    "39bc6d46bc7b83e73af0cc3466b79196defa4a2518e1db704b7a3f61f2e2173b"
)
CANDIDATE_SIZE = 934_776_249

ROUND174_SOURCE = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py"
)
ROUND174_ROWS = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_"
    "materialization_rows.json"
)
ROUND204_SOURCE = (
    "cm2_round204_source_g_wall_return_signature_local_replacement.py"
)
ROUND204_CERTIFICATE = (
    "cm2_round204_source_g_wall_return_signature_local_replacement_"
    "certificate.json"
)
ROUND208_SOURCE = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization.py"
)
ROUND208_CERTIFICATE = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization_"
    "certificate.json"
)
ROUND259_SOURCE = (
    "cm2_round259_source_g_curved_region_full_face_saturation.py"
)
ROUND259_CERTIFICATE = (
    "cm2_round259_source_g_curved_region_full_face_saturation_certificate.json"
)
ROUND260_SOURCE = (
    "cm2_round260_source_g_curved_region_common_face_refinement.py"
)
ROUND260_CERTIFICATE = (
    "cm2_round260_source_g_curved_region_common_face_refinement_certificate.json"
)
ROUND265_SOURCE = (
    "cm2_round265_source_g_expanded_occurrence_safe_face_saturation.py"
)
ROUND265_CERTIFICATE = (
    "cm2_round265_source_g_expanded_occurrence_safe_face_saturation_"
    "certificate.json"
)

SOURCE_PINS = {
    ROUND174_SOURCE:
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    ROUND204_SOURCE:
        "7e4b81846155c1edad0807362c7086a290702da7ce6680d7c449b7193635da77",
    ROUND208_SOURCE:
        "c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913",
    ROUND259_SOURCE:
        "4a465317d05ef3f1497876b052131cbbd889d67fbcc88e28362248935cfc5310",
    ROUND260_SOURCE:
        "7edc6e5978e2c0570522d90314be2945187ffa279fa85f345c66fa126b60552f",
    ROUND265_SOURCE:
        "ff32b033486d236d67532e7eef771983b32c8ca556d3fce06ddf3313ffb3f84d",
}
JSON_INPUTS = {
    ROUND174_ROWS: (
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
        "002ca6631edd39c2325c63a1e8f9717d111f4d10c6d2585077d665a0ff128d18",
        "cm2.round174.source-g-unique-first-dynamic-occurrence-rows.v1",
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
    ROUND259_CERTIFICATE: (
        "799dc36d6a5a9da351c0d006939feb6fc69eaad7ac30aa42b781f925c637d039",
        "03f3542ba4d51e6938d098b6822ea76a8ec6225e9bf590e1a96a7c5c67f8eba3",
        "cm2.round259.source-g-curved-region-full-face-saturation.v1",
    ),
    ROUND260_CERTIFICATE: (
        "a86ec032c3acbb708fd606ea0aa340f9ad650b9a8ac5e77299fefb8fdd1a765b",
        "5b3d3ec045c5ef5baa9cab9838b019a583ec4077b0867cce2a5c151131ba2f09",
        "cm2.round260.source-g-curved-region-common-face-refinement.v1",
    ),
    ROUND265_CERTIFICATE: (
        "78ec778a0521580991f18b9a5ef5d2ea9065283d5efb49a920c7469526735d18",
        "8289c4ee4d6d9698fcb0e7caff3d803e81122b06278c246cd20ab47298f682d4",
        "cm2.round265.source-g-expanded-occurrence-safe-face-saturation.v1",
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
OPPOSITE = {
    "STRICT_NEGATIVE": "STRICT_POSITIVE",
    "STRICT_POSITIVE": "STRICT_NEGATIVE",
}
EXPECTED_AXIS_HISTOGRAM = {
    "p:ROUND174_RESOLVED|ROUND204_REGION": 32,
    "p:ROUND174_RESOLVED|ROUND208_REGION": 1_796,
    "t:ROUND174_RESOLVED|ROUND204_REGION": 64,
    "t:ROUND174_RESOLVED|ROUND208_REGION": 760,
}
G: dict[str, Any] = {}


class Round266Error(RuntimeError):
    """A fail-closed Round266 contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round266Error(label)


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
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


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


def regular_bytes(path: Path, maximum: int = 2_000_000_000) -> bytes:
    need(path.parent == HERE, f"unexpected input parent:{path.name}")
    before = path.lstat()
    need(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1
        and 0 < before.st_size <= maximum,
        f"regular bounded input:{path.name}",
    )
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
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, f"strict encoding:{label}")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in items:
            need(key not in output, f"duplicate JSON key:{label}:{key}")
            output[key] = value
        return output

    def reject(token: str) -> None:
        raise Round266Error(f"non-integral JSON number:{label}:{token}")

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_float=reject,
            parse_constant=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Round266Error(f"strict JSON:{label}") from error
    need(isinstance(value, dict), f"top-level JSON object:{label}")
    return value


def load_result(name: str) -> dict[str, Any]:
    expected_file, expected_result, expected_schema = JSON_INPUTS[name]
    raw = regular_bytes(HERE / name)
    need(hashlib.sha256(raw).hexdigest() == expected_file, f"file pin:{name}")
    document = json.loads(raw)
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == expected_schema
        and document["result_sha256"] == expected_result
        and digest(document["result"]) == expected_result,
        f"envelope:{name}",
    )
    return document["result"]


def check_ledger(
    table: dict[str, Any],
    id_field: str,
    count: int,
) -> list[dict[str, Any]]:
    rows = table["rows"]
    need(
        table["row_count"] == len(rows) == count
        and table["rows_sha256"] == digest(rows)
        and len({row[id_field] for row in rows}) == count,
        f"ledger envelope:{id_field}",
    )
    if "row_ids_sha256" in table:
        need(
            table["row_ids_sha256"] == digest(
                [row[id_field] for row in rows]
            ),
            f"ledger row ids:{id_field}",
        )
    if "row_hashes_sha256" in table:
        need(
            table["row_hashes_sha256"] == digest(
                [row["row_sha256"] for row in rows]
            ),
            f"ledger row hashes:{id_field}",
        )
    if "every_row_closed_by_own_SHA256" in table:
        need(
            table["every_row_closed_by_own_SHA256"] is True,
            f"ledger closed flag:{id_field}",
        )
    for row in rows:
        raw = dict(row)
        row_hash = raw.pop("row_sha256")
        need(row_hash == digest(raw), f"closed row:{row[id_field]}")
    return rows


def packed_rows(
    result: dict[str, Any],
    table: str,
    count: int,
) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][table]
    rows = result[table]
    need(len(rows) == count, f"packed count:{table}")
    return [
        dict(zip(columns, packed, strict=True))
        for packed in rows
    ]


def input_binding() -> dict[str, Any]:
    result = {
        name: {"file_sha256": value}
        for name, value in SOURCE_PINS.items()
    }
    result.update({
        name: {
            "file_sha256": value[0],
            "result_sha256": value[1],
            "schema": value[2],
        }
        for name, value in JSON_INPUTS.items()
    })
    return dict(sorted(result.items()))


def exact_box(values: list[str], label: str) -> tuple[Fraction, ...]:
    need(
        isinstance(values, list)
        and len(values) == 6
        and all(isinstance(value, str) for value in values),
        f"box schema:{label}",
    )
    box = tuple(Fraction(value) for value in values)
    need(
        all(box[2 * axis] < box[2 * axis + 1] for axis in range(3)),
        f"positive box:{label}",
    )
    return box


def signature174(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "official_key_id": row["official_key_id"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_row": row["official_key_row"],
        "ordered_integer_wall_events": row["ordered_integer_wall_events"],
        "outgoing_cell": row["outgoing_cell"],
        "roof": row["roof"],
        "signed_wall_word": row["signed_wall_word"],
        "source_chart": row["chart"],
        "target_chart": row["target_chart"],
        "target_lift": row["owner_target"],
    }


def signature204(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "official_key_id": row["official_key_id"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_row": row["official_key_row"],
        "ordered_integer_wall_events": row["ordered_integer_wall_events"],
        "outgoing_cell": row["outgoing_cell"],
        "roof": row["roof"],
        "signed_wall_word": row["signed_wall_word"],
        "source_chart": row["chart"],
        "target_chart": row["target_chart"],
        "target_lift": row["owner_target"],
    }


def add_geometry_row(
    rows: list[dict[str, Any]],
    *,
    row_id: str,
    source: str,
    signature: dict[str, Any],
    box_values: list[str],
    evaluation_row: dict[str, Any],
) -> None:
    need(set(signature) == set(SIGNATURE_FIELDS), f"signature:{row_id}")
    signature_bytes = canonical(signature)
    rows.append({
        "id": row_id,
        "source": source,
        "signature": signature,
        "signature_bytes": signature_bytes,
        "signature_sha256": hashlib.sha256(signature_bytes).hexdigest(),
        "key_id": signature["official_key_id"],
        "key_ordinal": signature["official_key_ordinal"],
        "chart": signature["source_chart"],
        "box": exact_box(box_values, row_id),
        "box_text": list(box_values),
        "evaluation_row": evaluation_row,
    })


def common_face(
    negative: dict[str, Any],
    positive: dict[str, Any],
    axis: int,
    coordinate: Fraction,
) -> dict[str, Any]:
    need(
        negative["box"][2 * axis + 1] == coordinate
        and positive["box"][2 * axis] == coordinate,
        "opposite face incidence",
    )
    face: list[Fraction] = []
    rectangle: list[str] = []
    tangential_axes = [value for value in range(3) if value != axis]
    area = Fraction(1)
    for candidate_axis in range(3):
        if candidate_axis == axis:
            face.extend((coordinate, coordinate))
            continue
        lower = max(
            negative["box"][2 * candidate_axis],
            positive["box"][2 * candidate_axis],
        )
        upper = min(
            negative["box"][2 * candidate_axis + 1],
            positive["box"][2 * candidate_axis + 1],
        )
        need(lower < upper, "positive common face")
        face.extend((lower, upper))
        rectangle.extend((qtext(lower), qtext(upper)))
        area *= upper - lower
    need(area > 0, "positive common face area")
    return {
        "axis": axis,
        "axis_name": AXIS_NAMES[axis],
        "coordinate": coordinate,
        "face": face,
        "face_text": [qtext(value) for value in face],
        "tangential_axes": [AXIS_NAMES[value] for value in tangential_axes],
        "rectangle": rectangle,
        "area": area,
        "area_text": qtext(area),
    }


def reconstruct_candidates(
    failclosed_rows: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, tuple[Fraction, ...]],
]:
    raw174 = load_result(ROUND174_ROWS)
    round204 = load_result(ROUND204_CERTIFICATE)
    round208 = load_result(ROUND208_CERTIFICATE)
    rows: list[dict[str, Any]] = []
    for row in packed_rows(
        raw174,
        "resolved_3d_occurrence_rows",
        72_500,
    ):
        add_geometry_row(
            rows,
            row_id=row["row_id"],
            source="ROUND174_RESOLVED",
            signature=signature174(row),
            box_values=row["box"],
            evaluation_row=row,
        )
    for row in check_ledger(
        round204["formal_local_open_3D_region_ledger"],
        "region_row_id",
        736,
    ):
        add_geometry_row(
            rows,
            row_id=row["region_row_id"],
            source="ROUND204_REGION",
            signature=signature204(row),
            box_values=row["leaf_exact_box"],
            evaluation_row=row,
        )
    for row in check_ledger(
        round208["formal_local_open_3D_signature_ledger"],
        "region_row_id",
        36_040,
    ):
        add_geometry_row(
            rows,
            row_id=row["region_row_id"],
            source="ROUND208_REGION",
            signature=row["local_return_signature"],
            box_values=row["Round182_leaf_box"],
            evaluation_row=row,
        )
    need(
        Counter(row["source"] for row in rows)
        == Counter({
            "ROUND174_RESOLVED": 72_500,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36_040,
        }),
        "geometry source census",
    )
    meta = {row["id"]: row for row in rows}
    boxes = {row["id"]: row["box"] for row in rows}
    groups: dict[
        tuple[bytes, int, Fraction],
        list[list[int]],
    ] = defaultdict(lambda: [[], []])
    for index, row in enumerate(rows):
        for axis in range(3):
            groups[(row["signature_bytes"], axis, row["box"][2 * axis])][0].append(index)
            groups[(row["signature_bytes"], axis, row["box"][2 * axis + 1])][1].append(index)

    candidates: list[dict[str, Any]] = []
    for (signature_bytes, axis, coordinate), sides in groups.items():
        positive_indices, negative_indices = sides
        for positive_index in positive_indices:
            positive = rows[positive_index]
            for negative_index in negative_indices:
                negative = rows[negative_index]
                sources = {positive["source"], negative["source"]}
                if "ROUND174_RESOLVED" not in sources:
                    continue
                if not (
                    "ROUND204_REGION" in sources
                    or "ROUND208_REGION" in sources
                ):
                    continue
                tangential = [value for value in range(3) if value != axis]
                if any(
                    min(
                        positive["box"][2 * value + 1],
                        negative["box"][2 * value + 1],
                    )
                    <= max(
                        positive["box"][2 * value],
                        negative["box"][2 * value],
                    )
                    for value in tangential
                ):
                    continue
                need(
                    positive["signature_bytes"] == negative["signature_bytes"]
                    == signature_bytes,
                    "complete signature equality",
                )
                geometry = common_face(negative, positive, axis, coordinate)
                source_pair = "|".join(sorted((
                    negative["source"],
                    positive["source"],
                )))
                row_id = "round265-curved-face-failclosed:" + digest([
                    negative["id"],
                    positive["id"],
                    AXIS_NAMES[axis],
                    qtext(coordinate),
                    geometry["rectangle"],
                ])
                candidates.append({
                    "Round265_curved_face_failclosed_row_id": row_id,
                    "negative_id": negative["id"],
                    "positive_id": positive["id"],
                    "negative_source": negative["source"],
                    "positive_source": positive["source"],
                    "source_pair": source_pair,
                    "official_key_id": negative["key_id"],
                    "official_key_ordinal": negative["key_ordinal"],
                    "source_chart": negative["chart"],
                    "signature_sha256": negative["signature_sha256"],
                    "geometry": geometry,
                })
    candidates.sort(
        key=lambda row: row["Round265_curved_face_failclosed_row_id"]
    )
    need(
        len(candidates) == 2_652
        and len({
            row["Round265_curved_face_failclosed_row_id"]
            for row in candidates
        }) == 2_652,
        "independent curved candidate census",
    )
    axis_histogram = Counter(
        f"{row['geometry']['axis_name']}:{row['source_pair']}"
        for row in candidates
    )
    need(
        dict(sorted(axis_histogram.items())) == EXPECTED_AXIS_HISTOGRAM,
        "independent curved axis census",
    )

    frozen_by_id = {
        row["curved_face_failclosed_row_id"]: row
        for row in failclosed_rows
    }
    need(
        set(frozen_by_id)
        == {
            row["Round265_curved_face_failclosed_row_id"]
            for row in candidates
        },
        "Round265 failclosed candidate identity cross-binding",
    )
    for candidate in candidates:
        source = frozen_by_id[
            candidate["Round265_curved_face_failclosed_row_id"]
        ]
        geometry = candidate["geometry"]
        need(
            source["negative_side_occurrence_id"] == candidate["negative_id"]
            and source["positive_side_occurrence_id"] == candidate["positive_id"]
            and source["occurrence_source_pair"] == candidate["source_pair"]
            and source["official_key_id"] == candidate["official_key_id"]
            and source["official_key_ordinal"] == candidate["official_key_ordinal"]
            and source["source_chart"] == candidate["source_chart"]
            and source["complete_10_field_return_signature_sha256"]
            == candidate["signature_sha256"]
            and source["face_axis"] == geometry["axis_name"]
            and source["shared_face_coordinate"] == qtext(geometry["coordinate"])
            and source["tangential_axes"] == geometry["tangential_axes"]
            and source["exact_positive_2D_enclosing_box_face_rectangle"]
            == geometry["rectangle"]
            and source["exact_positive_2D_enclosing_box_face_area"]
            == geometry["area_text"]
            and source["complete_10_field_return_signature_equal"] is True
            and source["physical_glue_credit"] == 0,
            f"Round265 candidate geometry cross-binding:{source['curved_face_failclosed_row_id']}",
        )
        candidate["Round265_row_sha256"] = source["row_sha256"]
        candidate["pre_component_pair"] = source[
            "post_safe_face_component_pair"
        ]
        candidate["pre_pair_internal"] = source[
            "post_safe_face_pair_internal"
        ]
    del raw174, round204, round208, rows, groups
    gc.collect()
    return candidates, meta, boxes


def load_evaluators(
    meta: dict[str, dict[str, Any]],
    boxes: dict[str, tuple[Fraction, ...]],
) -> None:
    need(FLINT_VERSION == "0.9.0", "python-flint version")
    for name, expected in SOURCE_PINS.items():
        raw = regular_bytes(HERE / name, 5_000_000)
        need(hashlib.sha256(raw).hexdigest() == expected, f"source pin:{name}")
    round259 = load_result(ROUND259_CERTIFICATE)
    round260_certificate = load_result(ROUND260_CERTIFICATE)
    need(
        round259["census"]["accepted_curved_full_face_count"] == 1_988
        and round259["census"]["remaining_common_face_refinement_count"] == 11_848
        and round260_certificate["census"]["accepted_common_face_patch_count"] == 6_728
        and round260_certificate["census"]["remaining_deeper_common_face_refinement_count"] == 5_120,
        "R259/R260 evaluator-chain certified baseline",
    )
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    round260 = importlib.import_module(
        "cm2_round260_source_g_curved_region_common_face_refinement"
    )
    round260.load_geometry()
    round174 = importlib.import_module(
        "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization"
    )
    inputs174 = round174.load_inputs()
    tables174 = round174.registry_tables(inputs174["gate5"])
    ctx.prec = 256
    G.update({
        "round260": round260,
        "round174": round174,
        "tables174": tables174,
        "meta": meta,
        "boxes": boxes,
    })


def evaluate_r174(
    row_id: str,
    values: list[Fraction],
    label: str,
) -> dict[str, Any]:
    row = G["meta"][row_id]["evaluation_row"]
    round174 = G["round174"]
    signature, reasons = round174.dynamic_signature(
        row["chart"],
        round174.atlas.AtlasBox(*values, 0, label),
        row["owner_target"],
        G["tables174"],
    )
    need(signature is not None and not reasons, f"R174 unresolved:{label}")
    matches = (
        signature["target"] == row["owner_target"]
        and signature["events"] == row["ordered_integer_wall_events"]
        and list(signature["pattern"]) == row["signed_wall_word"]
        and signature["roof"] == row["roof"]
        and signature["outgoing_cell"] == row["outgoing_cell"]
        and signature["target_chart"] == row["target_chart"]
        and signature["key"]["row"] == row["official_key_row"]
        and signature["key"]["ordinal"] == row["official_key_ordinal"]
        and signature["key"]["identifier"] == row["official_key_id"]
    )
    need(matches, f"R174 full signature mismatch:{label}")
    observed = {
        "official_key_id": signature["key"]["identifier"],
        "official_key_ordinal": signature["key"]["ordinal"],
        "official_key_row": signature["key"]["row"],
        "ordered_integer_wall_events": signature["events"],
        "outgoing_cell": signature["outgoing_cell"],
        "roof": signature["roof"],
        "signed_wall_word": list(signature["pattern"]),
        "source_chart": row["chart"],
        "target_chart": signature["target_chart"],
        "target_lift": signature["target"],
    }
    return {
        "state": "MATCH",
        "proof_kind": "ROUND174_FULL_DYNAMIC_SIGNATURE_MATCH",
        "observed_complete_10_field_signature_sha256": digest(observed),
        "expected_complete_10_field_signature_sha256":
            G["meta"][row_id]["signature_sha256"],
    }


def evaluate_r204(
    row_id: str,
    values: list[Fraction],
    label: str,
) -> dict[str, Any]:
    round260 = G["round260"]
    region = round260.G["reg204"][row_id]
    collar = round260.G["scope182"]["collars"][region["occurrence_row_id"]]
    wall = round260.G["scope179"]["walls"][region["occurrence_row_id"]]
    r179 = round260.G["r179"]
    geometry = r179.independent_geometry(
        collar["chart"],
        collar["owner_target"],
        round260.G["r174_204"].atlas.AtlasBox(*values, 0, label),
    )
    source_factor = round260.G["r204"].CHART_CONTRACT[collar["chart"]][2]
    target_factor = "hit_x" if wall["axis"] == "X" else "hit_y"
    source_value = r179.subtract_wall(geometry[source_factor], 0)[0]
    target_value = r179.subtract_wall(
        geometry[target_factor],
        wall["integer_wall"],
    )[0]
    observed_source = r179.arb_sign(source_value)
    observed_target = r179.arb_sign(target_value)
    expected_source = "STRICT_" + region["source_sign"]
    expected_target = "STRICT_" + region["target_factor_sign"]
    need(
        observed_source == expected_source
        and observed_target == expected_target,
        f"R204 strict region mismatch:{label}",
    )
    return {
        "state": "MATCH",
        "proof_kind": "ROUND204_SOURCE_AND_TARGET_FACTOR_SIGNS_MATCH",
        "source_factor": source_factor,
        "target_factor": target_factor,
        "observed_source_sign": observed_source,
        "observed_target_sign": observed_target,
        "expected_source_sign": expected_source,
        "expected_target_sign": expected_target,
        "source_Arb_repr": repr(source_value),
        "target_Arb_repr": repr(target_value),
    }


def evaluate_r208(
    row_id: str,
    values: list[Fraction],
    label: str,
) -> dict[str, Any]:
    round260 = G["round260"]
    region = round260.G["reg208"][row_id]
    profiles = round260.G["r198"].selected_factor_profiles(
        round260.G["collars208"][region["occurrence_row_id"]],
        round260.G["r174"].atlas.AtlasBox(*values, 0, label),
    )
    observed = {
        factor: profiles[factor]["selected_sign"]
        for factor in ("HPLUS", "HMINUS")
    }
    expected = {
        "HPLUS": region["HPLUS_sign"],
        "HMINUS": region["HMINUS_sign"],
    }
    need(observed == expected, f"R208 factor-sign mismatch:{label}")
    return {
        "state": "MATCH",
        "proof_kind": "ROUND208_BOTH_SELECTED_FACTOR_SIGNS_MATCH",
        "HPLUS_direct_sign": profiles["HPLUS"]["direct_sign"],
        "HPLUS_centered_sign": profiles["HPLUS"]["centered_sign"],
        "HPLUS_selected_sign": profiles["HPLUS"]["selected_sign"],
        "HPLUS_expected_sign": expected["HPLUS"],
        "HMINUS_direct_sign": profiles["HMINUS"]["direct_sign"],
        "HMINUS_centered_sign": profiles["HMINUS"]["centered_sign"],
        "HMINUS_selected_sign": profiles["HMINUS"]["selected_sign"],
        "HMINUS_expected_sign": expected["HMINUS"],
    }


def evaluate(
    row_id: str,
    values: list[Fraction],
    label: str,
) -> dict[str, Any]:
    source = G["meta"][row_id]["source"]
    if source == "ROUND174_RESOLVED":
        return evaluate_r174(row_id, values, label)
    if source == "ROUND204_REGION":
        return evaluate_r204(row_id, values, label)
    if source == "ROUND208_REGION":
        return evaluate_r208(row_id, values, label)
    raise Round266Error(f"unknown evaluator source:{source}")


def corridor(
    candidate: dict[str, Any],
    row_id: str,
    ordinal: int,
) -> dict[str, Any]:
    geometry = candidate["geometry"]
    axis = geometry["axis"]
    coordinate = geometry["coordinate"]
    source_box = G["boxes"][row_id]
    span = source_box[2 * axis + 1] - source_box[2 * axis]
    for depth in range(1, 25):
        width = span / (2 ** depth)
        values = list(geometry["face"])
        if source_box[2 * axis + 1] == coordinate:
            values[2 * axis:2 * axis + 2] = [
                coordinate - width,
                coordinate,
            ]
            side = "NEGATIVE_SIDE_INWARD_CORRIDOR"
        elif source_box[2 * axis] == coordinate:
            values[2 * axis:2 * axis + 2] = [
                coordinate,
                coordinate + width,
            ]
            side = "POSITIVE_SIDE_INWARD_CORRIDOR"
        else:
            raise Round266Error(f"face incidence:{row_id}")
        try:
            proof = evaluate(
                row_id,
                values,
                f"round266:{ordinal}:corridor:{row_id}:{depth}",
            )
        except (Round266Error, RuntimeError):
            continue
        return {
            "occurrence_row_id": row_id,
            "occurrence_source": G["meta"][row_id]["source"],
            "corridor_side": side,
            "dyadic_normal_depth": depth,
            "exact_normal_width": qtext(width),
            "exact_corridor_box": [qtext(value) for value in values],
            "strict_match_evaluation": proof,
        }
    raise Round266Error(f"corridor depth 24:{row_id}")


def evaluate_candidate(
    task: tuple[int, dict[str, Any]],
) -> dict[str, Any]:
    ordinal, candidate = task
    geometry = candidate["geometry"]
    face = list(geometry["face"])
    face_evaluations = [
        {
            "occurrence_row_id": row_id,
            "occurrence_source": G["meta"][row_id]["source"],
            "strict_match_evaluation": evaluate(
                row_id,
                face,
                f"round266:{ordinal}:full-face:{row_id}",
            ),
        }
        for row_id in (candidate["negative_id"], candidate["positive_id"])
    ]
    corridor_rows = [
        corridor(candidate, row_id, ordinal)
        for row_id in (candidate["negative_id"], candidate["positive_id"])
    ]
    return {
        "Round265_curved_face_failclosed_row_id":
            candidate["Round265_curved_face_failclosed_row_id"],
        "full_face_evaluations": face_evaluations,
        "corridors": corridor_rows,
    }


class DSU:
    def __init__(self, values: Iterable[str]) -> None:
        self.parent = {value: value for value in values}
        self.size = {value: 1 for value in self.parent}

    def find(self, value: str) -> str:
        need(value in self.parent, f"DSU value:{value}")
        root = value
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[value] != value:
            parent = self.parent[value]
            self.parent[value] = root
            value = parent
        return root

    def union(self, left: str, right: str) -> bool:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        if (
            self.size[left] < self.size[right]
            or (self.size[left] == self.size[right] and left > right)
        ):
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True


def build(producer_sha256: str, processes: int) -> dict[str, Any]:
    round265 = load_result(ROUND265_CERTIFICATE)
    census265 = round265["census"]
    need(
        census265["post_Round265_component_count"] == 63_812
        and census265["expanded_occurrence_count"] == 126_468
        and census265["exact_key_count"] == 116
        and census265["valid_virtual_stratum_node_count"] == 133_284
        and census265["expanded_member_count"] == 259_752
        and census265["curved_graph_side_failclosed_face_count"] == 2_652
        and census265["curved_post_safe_face_internal_pair_count"] == 1_476
        and census265["curved_post_safe_face_cross_component_pair_count"] == 1_176
        and round265["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round265 frozen baseline",
    )
    component_rows265 = check_ledger(
        round265["formal_post_Round265_component_frontier_ledger"],
        "post_Round265_component_frontier_row_id",
        63_812,
    )
    occurrence_rows265 = check_ledger(
        round265["formal_post_Round265_expanded_occurrence_frontier_ledger"],
        "post_Round265_expanded_occurrence_frontier_row_id",
        126_468,
    )
    key_rows265 = check_ledger(
        round265["formal_post_Round265_key_frontier_ledger"],
        "post_Round265_key_frontier_row_id",
        116,
    )
    virtual_rows265 = check_ledger(
        round265["formal_post_Round265_valid_virtual_node_frontier_ledger"],
        "post_Round265_valid_virtual_node_frontier_row_id",
        133_284,
    )
    failclosed_rows = check_ledger(
        round265["formal_curved_graph_side_face_failclosed_ledger"],
        "curved_face_failclosed_row_id",
        2_652,
    )
    base_components = {
        row["post_Round265_quotient_component_id"]: row
        for row in component_rows265
    }
    base_occurrences = {
        row["local_occurrence_row_id"]: row
        for row in occurrence_rows265
    }
    base_keys = {
        row["official_key_id"]: row
        for row in key_rows265
    }
    need(
        len(base_components) == 63_812
        and len(base_occurrences) == 126_468
        and len(base_keys) == 116,
        "unique Round265 frontiers",
    )
    del round265
    gc.collect()

    candidates, meta, boxes = reconstruct_candidates(failclosed_rows)
    candidate_by_id = {
        row["Round265_curved_face_failclosed_row_id"]: row
        for row in candidates
    }
    load_evaluators(meta, boxes)
    tasks = list(enumerate(candidates, 1))
    evaluated: list[dict[str, Any]] = []
    with mp.get_context("fork").Pool(processes=processes) as pool:
        for result in pool.imap_unordered(
            evaluate_candidate,
            tasks,
            chunksize=1,
        ):
            evaluated.append(result)
    evaluated.sort(
        key=lambda row: row["Round265_curved_face_failclosed_row_id"]
    )
    need(len(evaluated) == 2_652, "complete evaluator result census")
    evaluated_by_id = {
        row["Round265_curved_face_failclosed_row_id"]: row
        for row in evaluated
    }
    need(set(evaluated_by_id) == set(candidate_by_id), "complete evaluation")

    accepted_rows: list[dict[str, Any]] = []
    area_sum = Fraction(0)
    corridor_volume_sum = Fraction(0)
    corridor_depth_histogram: Counter[int] = Counter()
    for candidate in candidates:
        source_id = candidate["Round265_curved_face_failclosed_row_id"]
        result = evaluated_by_id[source_id]
        geometry = candidate["geometry"]
        area_sum += geometry["area"]
        for proof in result["corridors"]:
            corridor_depth_histogram[proof["dyadic_normal_depth"]] += 1
            corridor_volume_sum += (
                geometry["area"] * Fraction(proof["exact_normal_width"])
            )
        accepted_id = "round266-accepted-curved-full-face:" + digest([
            source_id
        ])
        accepted_rows.append(closed({
            "accepted_curved_full_face_row_id": accepted_id,
            "Round265_curved_face_failclosed_row_id": source_id,
            "Round265_curved_face_failclosed_row_sha256":
                candidate["Round265_row_sha256"],
            "negative_side_occurrence_id": candidate["negative_id"],
            "positive_side_occurrence_id": candidate["positive_id"],
            "negative_side_occurrence_source": candidate["negative_source"],
            "positive_side_occurrence_source": candidate["positive_source"],
            "occurrence_source_pair": candidate["source_pair"],
            "official_key_id": candidate["official_key_id"],
            "official_key_ordinal": candidate["official_key_ordinal"],
            "source_chart": candidate["source_chart"],
            "complete_10_field_return_signature_sha256":
                candidate["signature_sha256"],
            "face_axis": geometry["axis_name"],
            "shared_face_coordinate": qtext(geometry["coordinate"]),
            "tangential_axes": geometry["tangential_axes"],
            "exact_positive_2D_common_face_box": geometry["face_text"],
            "exact_positive_2D_common_face_rectangle":
                geometry["rectangle"],
            "exact_positive_2D_common_face_area": geometry["area_text"],
            "canonical_dyadic_face_refinement_depth": 0,
            "canonical_quadtree_checkpoint_states": {
                "0": "MATCH",
                "4": "MATCH",
                "8": "MATCH",
                "12": "MATCH",
            },
            "full_face_strict_MATCH_evaluations":
                result["full_face_evaluations"],
            "strict_two_sided_inward_3D_corridors": result["corridors"],
            "pre_Round266_component_pair":
                candidate["pre_component_pair"],
            "pre_Round266_pair_internal":
                candidate["pre_pair_internal"],
            "disposition":
                "ACCEPT_COMPLETE_CURVED_FULL_FACE_WITH_TWO_STRICT_INWARD_CORRIDORS",
            "physical_glue_credit": 1,
            "component_union_credit": 0,
            "maximality_credit": 0,
        }))
    need(
        area_sum == Fraction(5_728_631, 1_638_400_000)
        and corridor_volume_sum
        == Fraction(302_487_513, 3_355_443_200_000)
        and corridor_depth_histogram == Counter({1: 5_224, 2: 80}),
        "exact accepted geometry census",
    )
    accepted_rows.sort(
        key=lambda row: row["accepted_curved_full_face_row_id"]
    )

    # Quotient the complete Round265 component frontier.
    dsu = DSU(base_components)
    distinct_nontrivial_pairs: set[tuple[str, str]] = set()
    raw_internal_count = 0
    accepted_edge_count_by_key: Counter[str] = Counter()
    internal_edge_count_by_key: Counter[str] = Counter()
    rank_count_by_key: Counter[str] = Counter()
    for row in accepted_rows:
        left, right = row["pre_Round266_component_pair"]
        need(
            left in base_components
            and right in base_components
            and base_components[left]["official_key_id"]
            == base_components[right]["official_key_id"]
            == row["official_key_id"],
            f"accepted edge key purity:{row['accepted_curved_full_face_row_id']}",
        )
        accepted_edge_count_by_key[row["official_key_id"]] += 1
        if left == right:
            raw_internal_count += 1
            internal_edge_count_by_key[row["official_key_id"]] += 1
        else:
            distinct_nontrivial_pairs.add(tuple(sorted((left, right))))
    need(
        raw_internal_count == 1_476
        and len(distinct_nontrivial_pairs) == 604,
        "post-Round265 component-pair census",
    )

    rank_pairs: set[tuple[str, str]] = set()
    for pair in sorted(distinct_nontrivial_pairs):
        if dsu.union(*pair):
            rank_pairs.add(pair)
            key_id = base_components[pair[0]]["official_key_id"]
            rank_count_by_key[key_id] += 1
    need(
        len(rank_pairs) == 588
        and len(distinct_nontrivial_pairs - rank_pairs) == 16,
        "curved-face rank census",
    )
    classes: dict[str, list[str]] = defaultdict(list)
    for component_id in sorted(base_components):
        classes[dsu.find(component_id)].append(component_id)
    need(len(classes) == 63_224, "post-Round266 quotient count")

    descriptors_by_component = {
        component_id: {
            "Round265_component_id": component_id,
            "source_row_id":
                row["post_Round265_component_frontier_row_id"],
            "source_row_sha256": row["row_sha256"],
        }
        for component_id, row in base_components.items()
    }
    post_by_old: dict[str, str] = {}
    members_by_post: dict[str, list[str]] = {}
    descriptors_sha_by_post: dict[str, str] = {}
    for members in classes.values():
        members.sort()
        descriptors = [
            descriptors_by_component[value] for value in members
        ]
        post_id = "round266-curved-face-component:" + digest(descriptors)
        need(post_id not in members_by_post, f"unique post component:{post_id}")
        members_by_post[post_id] = members
        descriptors_sha_by_post[post_id] = digest(descriptors)
        for value in members:
            post_by_old[value] = post_id
    need(len(post_by_old) == 63_812, "complete component map")

    rank_edge_count_by_post: Counter[str] = Counter()
    distinct_pair_count_by_post: Counter[str] = Counter()
    raw_edge_count_by_post: Counter[str] = Counter()
    for pair in distinct_nontrivial_pairs:
        post_id = post_by_old[pair[0]]
        need(post_id == post_by_old[pair[1]], "pair post assignment")
        distinct_pair_count_by_post[post_id] += 1
        rank_edge_count_by_post[post_id] += int(pair in rank_pairs)
    credited_rank_pairs: set[tuple[str, str]] = set()
    for row in accepted_rows:
        left, right = row["pre_Round266_component_pair"]
        post_id = post_by_old[left]
        need(post_id == post_by_old[right], "edge post assignment")
        raw_edge_count_by_post[post_id] += 1
        row_without_hash = dict(row)
        row_without_hash.pop("row_sha256")
        pair = tuple(sorted((left, right)))
        rank_credit = (
            pair in rank_pairs and pair not in credited_rank_pairs
        )
        if rank_credit:
            credited_rank_pairs.add(pair)
        row_without_hash["post_Round266_quotient_component_id"] = post_id
        row_without_hash["rank_reducing_distinct_component_pair"] = (
            rank_credit
        )
        row_without_hash["component_union_credit"] = int(rank_credit)
        row.clear()
        row.update(closed(row_without_hash))
    need(credited_rank_pairs == rank_pairs, "canonical rank-credit rows")

    component_map_rows: list[dict[str, Any]] = []
    for old_id in sorted(base_components):
        source = base_components[old_id]
        component_map_rows.append(closed({
            "Round265_to_Round266_component_map_row_id":
                "round266-component-map:" + digest([old_id]),
            "Round265_quotient_component_id": old_id,
            "source_Round265_component_frontier_row_id":
                source["post_Round265_component_frontier_row_id"],
            "source_Round265_component_frontier_row_sha256":
                source["row_sha256"],
            "official_key_id": source["official_key_id"],
            "official_key_ordinal": source["official_key_ordinal"],
            "post_Round266_quotient_component_id": post_by_old[old_id],
            "Round266_component_remap_indicator":
                int(post_by_old[old_id] != old_id),
            "maximality_credit": 0,
        }))

    occurrence_count_by_post: Counter[str] = Counter()
    occurrence_count_by_key: Counter[str] = Counter()
    R174_count_by_post: Counter[str] = Counter()
    occurrence_frontier_rows: list[dict[str, Any]] = []
    for source in sorted(
        occurrence_rows265,
        key=lambda row: row["local_occurrence_row_id"],
    ):
        old_id = source["post_Round265_quotient_component_id"]
        post_id = post_by_old[old_id]
        key_id = source["official_key_id"]
        need(
            base_components[old_id]["official_key_id"] == key_id,
            f"occurrence key purity:{source['local_occurrence_row_id']}",
        )
        occurrence_count_by_post[post_id] += 1
        occurrence_count_by_key[key_id] += 1
        if source["occurrence_source"] == "ROUND174_RESOLVED":
            R174_count_by_post[post_id] += 1
        output = dict(source)
        output.pop("row_sha256")
        output["source_Round265_expanded_occurrence_frontier_row_id"] = (
            source["post_Round265_expanded_occurrence_frontier_row_id"]
        )
        output["source_Round265_expanded_occurrence_frontier_row_sha256"] = (
            source["row_sha256"]
        )
        output["post_Round266_expanded_occurrence_frontier_row_id"] = (
            "round266-expanded-occurrence:"
            + digest([source["local_occurrence_row_id"]])
        )
        output["post_Round266_quotient_component_id"] = post_id
        output["Round266_curved_face_attachment_credit"] = int(
            post_id != old_id
        )
        occurrence_frontier_rows.append(closed(output))
    need(
        len(occurrence_frontier_rows) == 126_468,
        "complete occurrence frontier",
    )

    virtual_count_by_post: Counter[str] = Counter()
    virtual_count_by_key: Counter[str] = Counter()
    virtual_frontier_rows: list[dict[str, Any]] = []
    for source in sorted(
        virtual_rows265,
        key=lambda row: row["valid_virtual_stratum_node_id"],
    ):
        old_id = source["post_Round265_quotient_component_id"]
        post_id = post_by_old[old_id]
        key_id = source["official_key_id"]
        need(
            base_components[old_id]["official_key_id"] == key_id,
            f"virtual key purity:{source['valid_virtual_stratum_node_id']}",
        )
        virtual_count_by_post[post_id] += 1
        virtual_count_by_key[key_id] += 1
        output = dict(source)
        output.pop("row_sha256")
        output["source_Round265_valid_virtual_node_frontier_row_id"] = (
            source["post_Round265_valid_virtual_node_frontier_row_id"]
        )
        output["source_Round265_valid_virtual_node_frontier_row_sha256"] = (
            source["row_sha256"]
        )
        output["post_Round266_valid_virtual_node_frontier_row_id"] = (
            "round266-valid-virtual-node:"
            + digest([source["valid_virtual_stratum_node_id"]])
        )
        output["post_Round266_quotient_component_id"] = post_id
        output["Round266_curved_face_attachment_credit"] = int(
            post_id != old_id
        )
        virtual_frontier_rows.append(closed(output))
    need(
        len(virtual_frontier_rows) == 133_284,
        "complete virtual frontier",
    )

    component_count_by_key: Counter[str] = Counter()
    member_count_sum = 0
    component_frontier_rows: list[dict[str, Any]] = []
    for post_id in sorted(members_by_post):
        members = members_by_post[post_id]
        keys = {
            (
                base_components[value]["official_key_id"],
                base_components[value]["official_key_ordinal"],
            )
            for value in members
        }
        need(len(keys) == 1, f"component key purity:{post_id}")
        key_id, ordinal = next(iter(keys))
        occurrence_count = occurrence_count_by_post[post_id]
        virtual_count = virtual_count_by_post[post_id]
        member_count = occurrence_count + virtual_count
        need(member_count > 0, f"nonempty component:{post_id}")
        member_count_sum += member_count
        component_count_by_key[key_id] += 1
        component_frontier_rows.append(closed({
            "post_Round266_component_frontier_row_id":
                "round266-component-row:" + digest([post_id]),
            "post_Round266_quotient_component_id": post_id,
            "official_key_id": key_id,
            "official_key_ordinal": ordinal,
            "constituent_Round265_component_count": len(members),
            "constituent_Round265_component_ids": members,
            "constituent_Round265_component_ids_sha256": digest(members),
            "constituent_Round265_component_descriptors_sha256":
                descriptors_sha_by_post[post_id],
            "accepted_curved_full_face_edge_count":
                raw_edge_count_by_post[post_id],
            "distinct_nontrivial_curved_component_pair_count":
                distinct_pair_count_by_post[post_id],
            "curved_face_rank_reduction_count":
                rank_edge_count_by_post[post_id],
            "expanded_occurrence_member_count": occurrence_count,
            "Round174_occurrence_member_count": R174_count_by_post[post_id],
            "valid_virtual_stratum_node_count": virtual_count,
            "expanded_member_count": member_count,
            "certified_known_connectivity_only": True,
            "maximal_physical_component_claimed": False,
        }))
    need(
        len(component_frontier_rows) == 63_224
        and member_count_sum == 259_752,
        "complete component/member frontier",
    )

    key_frontier_rows: list[dict[str, Any]] = []
    for key_id in sorted(base_keys):
        source = base_keys[key_id]
        pre_count = source["post_Round265_quotient_component_count"]
        post_count = component_count_by_key[key_id]
        need(
            pre_count - post_count == rank_count_by_key[key_id]
            and occurrence_count_by_key[key_id]
            == source["expanded_occurrence_count"]
            and virtual_count_by_key[key_id]
            == source["valid_virtual_stratum_node_count"],
            f"key conservation:{key_id}",
        )
        key_frontier_rows.append(closed({
            "post_Round266_key_frontier_row_id":
                "round266-key-frontier:" + digest([key_id]),
            "official_key_id": key_id,
            "official_key_ordinal": source["official_key_ordinal"],
            "source_Round265_key_frontier_row_id":
                source["post_Round265_key_frontier_row_id"],
            "source_Round265_key_frontier_row_sha256": source["row_sha256"],
            "pre_Round266_quotient_component_count": pre_count,
            "accepted_curved_full_face_edge_count":
                accepted_edge_count_by_key[key_id],
            "already_internal_curved_full_face_edge_count":
                internal_edge_count_by_key[key_id],
            "curved_face_rank_reduction_count":
                rank_count_by_key[key_id],
            "post_Round266_quotient_component_count": post_count,
            "expanded_occurrence_count": occurrence_count_by_key[key_id],
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
        len(key_frontier_rows) == 116
        and sum(component_count_by_key.values()) == 63_224
        and sum(occurrence_count_by_key.values()) == 126_468
        and sum(virtual_count_by_key.values()) == 133_284,
        "complete exact-key frontier",
    )

    # Explicit unified member frontier.
    member_frontier_rows: list[dict[str, Any]] = []
    for row in occurrence_frontier_rows:
        member_id = row["local_occurrence_row_id"]
        member_frontier_rows.append(closed({
            "post_Round266_component_member_frontier_row_id":
                "round266-component-member:"
                + digest(["EXPANDED_OCCURRENCE", member_id]),
            "component_member_id": member_id,
            "component_member_kind": "EXPANDED_OCCURRENCE",
            "component_member_source_kind": row["occurrence_source"],
            "official_key_id": row["official_key_id"],
            "source_Round266_frontier_row_id":
                row["post_Round266_expanded_occurrence_frontier_row_id"],
            "source_Round266_frontier_row_sha256": row["row_sha256"],
            "post_Round265_quotient_component_id":
                row["post_Round265_quotient_component_id"],
            "post_Round266_quotient_component_id":
                row["post_Round266_quotient_component_id"],
            "member_identity_preserved": True,
            "maximality_credit": 0,
        }))
    for row in virtual_frontier_rows:
        member_id = row["valid_virtual_stratum_node_id"]
        member_frontier_rows.append(closed({
            "post_Round266_component_member_frontier_row_id":
                "round266-component-member:"
                + digest(["VALID_VIRTUAL_STRATUM", member_id]),
            "component_member_id": member_id,
            "component_member_kind": "VALID_VIRTUAL_STRATUM",
            "component_member_source_kind": row["virtual_node_kind"],
            "official_key_id": row["official_key_id"],
            "source_Round266_frontier_row_id":
                row["post_Round266_valid_virtual_node_frontier_row_id"],
            "source_Round266_frontier_row_sha256": row["row_sha256"],
            "post_Round265_quotient_component_id":
                row["post_Round265_quotient_component_id"],
            "post_Round266_quotient_component_id":
                row["post_Round266_quotient_component_id"],
            "member_identity_preserved": True,
            "maximality_credit": 0,
        }))
    member_frontier_rows.sort(
        key=lambda row: row["post_Round266_component_member_frontier_row_id"]
    )
    need(
        len(member_frontier_rows) == 259_752
        and len({
            (
                row["component_member_kind"],
                row["component_member_id"],
            )
            for row in member_frontier_rows
        }) == 259_752,
        "complete explicit member frontier",
    )

    checkpoint_census = {
        depth: {"MATCH": 2_652, "EXCLUDE": 0, "UNRESOLVED": 0}
        for depth in ("0", "4", "8", "12")
    }
    census = {
        "Round265_curved_face_candidate_count": 2_652,
        "independently_rebuilt_R174_R204_candidate_count": 96,
        "independently_rebuilt_R174_R208_candidate_count": 2_556,
        "curved_face_axis_histogram": EXPECTED_AXIS_HISTOGRAM,
        "canonical_checkpoint_candidate_state_census": checkpoint_census,
        "accepted_complete_curved_full_face_count": 2_652,
        "strictly_excluded_curved_face_count": 0,
        "remaining_unresolved_curved_face_count": 0,
        "accepted_face_refinement_depth_histogram": {"0": 2_652},
        "strict_inward_corridor_count": 5_304,
        "strict_inward_corridor_normal_depth_histogram": {
            "1": 5_224,
            "2": 80,
        },
        "exact_accepted_curved_full_face_area_sum": qtext(area_sum),
        "exact_strict_inward_corridor_volume_sum":
            qtext(corridor_volume_sum),
        "accepted_edge_row_count": 2_652,
        "already_internal_edge_row_count": 1_476,
        "cross_component_edge_row_count": 1_176,
        "distinct_nontrivial_post_Round265_component_pair_count": 604,
        "rank_reducing_distinct_component_pair_count": 588,
        "redundant_distinct_component_pair_count": 16,
        "redundant_accepted_edge_row_count": 2_064,
        "pre_Round266_component_count": 63_812,
        "post_Round266_component_count": 63_224,
        "complete_occurrence_frontier_count": 126_468,
        "complete_exact_key_frontier_count": 116,
        "complete_valid_virtual_node_frontier_count": 133_284,
        "complete_explicit_component_member_frontier_count": 259_752,
        "known_remaining_Round182_closed_leaf_count_without_side_specific_signature_materialization":
            184_452,
        "known_remaining_positive_volume_chart_guard_count_requiring_reverse_rechart":
            880,
        "known_remaining_Round174_positive_volume_chart_guard_count": 728,
        "known_remaining_Round179_positive_volume_chart_guard_count": 152,
        "known_remaining_Round182_positive_area_seam_owner_shadow_candidate_count":
            152,
        "maximal_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    return {
        "status":
            "CERTIFIED_2652_EXPANDED_CURVED_FULL_FACES__"
            "5304_STRICT_INWARD_CORRIDORS__"
            "588_RANK_REDUCTIONS__QUOTIENT_63812_TO_63224",
        "census": census,
        "formal_input_binding": input_binding(),
        "formal_accepted_expanded_curved_full_face_ledger": ledger(
            accepted_rows,
            "accepted_curved_full_face_row_id",
        ),
        "formal_Round265_to_Round266_component_map_ledger": ledger(
            component_map_rows,
            "Round265_to_Round266_component_map_row_id",
        ),
        "formal_post_Round266_component_frontier_ledger": ledger(
            component_frontier_rows,
            "post_Round266_component_frontier_row_id",
        ),
        "formal_post_Round266_expanded_occurrence_frontier_ledger": ledger(
            occurrence_frontier_rows,
            "post_Round266_expanded_occurrence_frontier_row_id",
        ),
        "formal_post_Round266_key_frontier_ledger": ledger(
            key_frontier_rows,
            "post_Round266_key_frontier_row_id",
        ),
        "formal_post_Round266_valid_virtual_node_frontier_ledger": ledger(
            virtual_frontier_rows,
            "post_Round266_valid_virtual_node_frontier_row_id",
        ),
        "formal_post_Round266_component_member_frontier_ledger": ledger(
            member_frontier_rows,
            "post_Round266_component_member_frontier_row_id",
        ),
        "scope_contract": {
            "Round265_failclosed_rows_reconstructed_from_R174_R204_R208_geometry":
                True,
            "Round259_Round260_hash_pinned_evaluator_chain_replayed":
                True,
            "fixed_Arb_precision_bits": 256,
            "all_candidates_strict_MATCH_on_the_complete_common_face": True,
            "all_matches_have_explicit_strict_two_sided_inward_3D_corridors":
                True,
            "canonical_checkpoint_states_0_4_8_12_preserved": True,
            "all_input_component_occurrence_key_virtual_and_member_rows_conserved":
                True,
            "Round182_closed_leaf_side_specific_signatures_complete": False,
            "positive_volume_chart_guards_reverse_recharted": False,
            "Round182_positive_area_seam_owner_shadow_candidates_closed": False,
            "complete_occurrence_universe_claimed": False,
            "complete_full_signature_face_is_glue_but_not_maximality": True,
            "Jx_Jy_same_point_glue_credit": 0,
        },
        "strict_nonpromotion": {
            "maximal_physical_component_assignments": "0/63224",
            "globally_exhausted_exact_key_fibres": "0/116",
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "materialize side-specific return signatures on the remaining "
            "184,452 Round182 closed leaves, reverse-rechart the 728 Round174 "
            "and 152 Round179 positive-volume chart guards, close the 152 "
            "Round182 positive-area seam owner/shadow candidates, complete "
            "the omitted Round174 lower-dimensional boundary atlas, and only "
            "then prove "
            "maximality of all 63,224 expanded quotient components and "
            "exhaust all 116 exact-key fibres without Jx/Jy same-point glue "
            "credit"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "python_flint_version": FLINT_VERSION,
            "effective_Arb_precision_bits": ctx.prec,
            "imported_pinned_R259_R260_evaluator_chain": True,
            "upstream_producer_build_or_main_executed": False,
            "temporary_probe_consumed": False,
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


def semantic_attack_suite(candidate: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    attacks = [
        ("promote_maximality", "maximal_component_assignment_count", 1),
        ("promote_fibre", "globally_exhausted_exact_key_fibre_count", 1),
        ("promote_disposition", "global_exact_key_disposition_count", 1),
        ("alter_candidate_count", "Round265_curved_face_candidate_count", 2651),
        ("alter_accepted_count", "accepted_complete_curved_full_face_count", 2651),
        ("alter_corridor_count", "strict_inward_corridor_count", 5303),
        ("alter_rank", "rank_reducing_distinct_component_pair_count", 587),
        ("alter_quotient", "post_Round266_component_count", 63225),
    ]
    rejected = []
    census = candidate["census"]
    for label, key, replacement in attacks:
        original = census[key]
        census[key] = replacement
        need(candidate != expected, f"semantic attack rejected:{label}")
        census[key] = original
        need(candidate == expected, f"semantic attack restored:{label}")
        rejected.append(label)
    extra = [
        ("grant_jx_jy", "Jx_Jy_same_point_glue_credit", 1),
        ("promote_cm2", "CM2", "GO_FOR_CLAIM"),
    ]
    for label, key, replacement in extra:
        target = candidate["scope_contract"] if key.startswith("Jx") else candidate["strict_nonpromotion"]
        original = target[key]
        target[key] = replacement
        need(candidate != expected, f"semantic attack rejected:{label}")
        target[key] = original
        need(candidate == expected, f"semantic attack restored:{label}")
        rejected.append(label)
    return {
        "attack_count": len(rejected),
        "rejected_count": len(rejected),
        "all_semantic_attacks_rejected": True,
        "attack_labels": rejected,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=266_929)
    parser.add_argument("--processes", type=int, default=40)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    need(
        isinstance(arguments.seed, int)
        and not isinstance(arguments.seed, bool)
        and 1 <= arguments.processes <= 64,
        "arguments",
    )
    producer_raw = regular_bytes(PRODUCER, 5_000_000)
    need(hashlib.sha256(producer_raw).hexdigest() == PRODUCER_SHA256, "producer pin")
    expected = build(PRODUCER_SHA256, arguments.processes)
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
        "status": "PASS_INDEPENDENT_ROUND266",
        "candidate_sha256": CANDIDATE_SHA256,
        "candidate_result_sha256": CANDIDATE_RESULT_SHA256,
        "producer_sha256": PRODUCER_SHA256,
        "independence_contract": {
            "producer_imported_or_executed": False,
            "complete_candidate_geometry_rebuilt": True,
            "complete_expected_object_built_before_candidate_open": True,
            "fixed_Arb_precision_bits": 256,
            "seed_affects_output": False,
        },
        "verified_census": expected["census"],
        "semantic_attack_suite": attacks,
        "strict_nonpromotion": expected["strict_nonpromotion"],
    }
    encoded = canonical(verification) + b"\n"
    if not arguments.no_write:
        safe_write(encoded)
    print(verification["status"])
    print(f"verification_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"attacks_rejected={attacks['rejected_count']}/{attacks['attack_count']}")
    print("curved_faces=2652 corridors=5304 rank=588 components=63812->63224")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
