#!/usr/bin/env python3
"""Exhaust true same-point source-chart transitions on all Source-G occurrences.

Round171 proves that the four genuine Source-G chart transitions occur on
the exact seam ``2*t^2-1=0``.  This producer independently reconstructs the
complete 53,968-occurrence exact-box universe from the pinned Round179,
Round204, and Round208 geometry, binds it to the future frozen Round262
frontier, and proves for every box that

    1/2 - max(abs(t_lower), abs(t_upper))^2 > 0.

Consequently none of the retained occurrence boxes meets a true source-chart
seam.  Round227's Jx/Jy maps are nonidentity physical symmetries, not
same-point coordinate transitions, and therefore add no union-find edge.
The post-Round262 quotient and all of its frontiers are preserved verbatim
by digest commitment.  This is a transition-channel exhaustion only: it
does not prove component maximality, exact-key fibre exhaustion, a global
disposition, Gate5 completion, D02, or CM2.

The Round262 certificate and result pins below bind this transition audit to
the independently verified, byte-reproducible Round262 freeze.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
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
PREFIX = "cm2_round263_source_g_complete_occurrence_cross_chart_transition_exhaustion"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = (
    "cm2.round263.source-g-complete-occurrence-cross-chart-"
    "transition-exhaustion.v1"
)

ROUND171_CERTIFICATE = (
    "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
)
ROUND227_CERTIFICATE = (
    "cm2_round227_source_g_sheet_symmetry_non_glue_audit_certificate.json"
)
ROUND228_CERTIFICATE = (
    "cm2_round228_source_g_sheet_atlas_overlap_exhaustion_certificate.json"
)
ROUND179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
ROUND204_CERTIFICATE = (
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
)
ROUND208_CERTIFICATE = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
)
ROUND262_CERTIFICATE = (
    "cm2_round262_source_g_monotone_deep_common_face_closure_certificate.json"
)

ROUND262_CERTIFICATE_SHA256 = (
    "d9cac69017dd3247428492bdee6402da9868a7d97db3574f41ba25a1b49005de"
)
ROUND262_RESULT_SHA256 = (
    "33d54f038b066d66119bb401c98a0a34b308743ba81932b5693e7a9e69238d6e"
)

INPUTS = {
    ROUND171_CERTIFICATE: {
        "file_sha256": "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5",
        "result_sha256": "ffac0e2e16829c1a3ffc4783af2c224288265d02cf53c1d041aaf02013b52957",
        "schema": "cm2.round171.compact-gate3-source-g-coordinate-bridge.v1",
        "maximum_bytes": 1_000_000,
    },
    ROUND227_CERTIFICATE: {
        "file_sha256": "fa8d518239d2f2d4eb993ac58c66ffe2b7d222fa8efd4d916689cebd05201461",
        "result_sha256": "fe134a35a2bb601f79ed4b712eba0cdb9a01db696bf854a24678a006ab2036ba",
        "schema": "cm2.round227.source-g-sheet-symmetry-non-glue-audit.v1",
        "maximum_bytes": 50_000_000,
    },
    ROUND228_CERTIFICATE: {
        "file_sha256": "03bd2bf3d4a6f9c6694062c1f7409058a537a5d4e4742df4e67d485032615cd0",
        "result_sha256": "8c220de4122ccdc9673f45a5cd82b5da28c64e47b87af01ee04723f971923550",
        "schema": "cm2.round228.source-g-sheet-atlas-overlap-exhaustion.v1",
        "maximum_bytes": 25_000_000,
    },
    ROUND179_ROWS: {
        "file_sha256": "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
        "result_sha256": "a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb",
        "schema": "cm2.round179.source-g-residual-tube-arrangement-rows.v1",
        "maximum_bytes": 150_000_000,
    },
    ROUND204_CERTIFICATE: {
        "file_sha256": "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
        "result_sha256": "ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd",
        "schema": "cm2.round204.source-g-wall-return-signature-local-replacement.v1",
        "maximum_bytes": 10_000_000,
    },
    ROUND208_CERTIFICATE: {
        "file_sha256": "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
        "result_sha256": "d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8",
        "schema": "cm2.round208.source-g-outgoing-direct-signature-materialization.v1",
        "maximum_bytes": 225_000_000,
    },
    ROUND262_CERTIFICATE: {
        "file_sha256": ROUND262_CERTIFICATE_SHA256,
        "result_sha256": ROUND262_RESULT_SHA256,
        "schema": "cm2.round262.source-g-monotone-deep-common-face-closure.v1",
        "maximum_bytes": 700_000_000,
    },
}

EXPECTED_GEOMETRY_SOURCE_COUNTS = {
    "ROUND179_RESOLVED_3D_CHILD": 17_192,
    "ROUND204_LOCAL_OPEN_3D_REGION": 736,
    "ROUND208_LOCAL_OPEN_3D_SIGNATURE": 36_040,
}
EXPECTED_SOURCE_CHART_COUNTS = {
    "G:E": 16_346,
    "G:N": 10_638,
    "G:S": 10_638,
    "G:W": 16_346,
}
EXPECTED_MAXIMUM_ABSOLUTE_T = Fraction(1_448_037, 2_048_000)
EXPECTED_MINIMUM_SEAM_SQUARE_GAP = Fraction(340_846_631, 4_194_304_000_000)


class Round263Error(RuntimeError):
    """A fail-closed Round263 contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round263Error(label)


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
    need("row_sha256" not in output, "row already carries closure")
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


def regular_bytes(path: Path, maximum: int) -> bytes:
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
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, f"duplicate JSON key:{label}:{key}")
            result[key] = value
        return result

    def reject(token: str) -> None:
        raise Round263Error(f"non-integral JSON number:{label}:{token}")

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_float=reject,
            parse_constant=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Round263Error(f"strict JSON:{label}") from error
    need(isinstance(value, dict), f"top-level JSON object:{label}")
    return value


def load_result(name: str) -> dict[str, Any]:
    specification = INPUTS[name]
    if name == ROUND262_CERTIFICATE:
        need(
            all(
                isinstance(specification[field], str)
                and len(specification[field]) == 64
                and all(character in "0123456789abcdef"
                        for character in specification[field])
                for field in ("file_sha256", "result_sha256")
            ),
            "Round262 pins must be frozen lowercase SHA256 values",
        )
    raw = regular_bytes(HERE / name, specification["maximum_bytes"])
    need(
        hashlib.sha256(raw).hexdigest() == specification["file_sha256"],
        f"file pin:{name}",
    )
    document = strict_json(raw, name)
    need(
        set(document) == {"schema", "result", "result_sha256"},
        f"envelope keys:{name}",
    )
    need(document["schema"] == specification["schema"], f"schema pin:{name}")
    need(
        document["result_sha256"] == specification["result_sha256"]
        and digest(document["result"]) == specification["result_sha256"],
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
        f"ledger unique ids:{id_field}",
    )
    need(value["rows_sha256"] == digest(rows), f"ledger rows digest:{id_field}")
    for row in rows:
        expected = row["row_sha256"]
        body = dict(row)
        body.pop("row_sha256")
        need(expected == digest(body), f"row closure:{id_field}")
    if "row_ids_sha256" in value:
        need(
            value["row_ids_sha256"] == digest([row[id_field] for row in rows]),
            f"ledger id digest:{id_field}",
        )
    if "row_hashes_sha256" in value:
        need(
            value["row_hashes_sha256"]
            == digest([row["row_sha256"] for row in rows]),
            f"ledger row-hash digest:{id_field}",
        )
    if "every_row_closed_by_own_SHA256" in value:
        need(
            value["every_row_closed_by_own_SHA256"] is True,
            f"ledger closure flag:{id_field}",
        )
    return rows


def exact_box(values: Any, label: str) -> tuple[Fraction, ...]:
    need(
        isinstance(values, list)
        and len(values) == 6
        and all(isinstance(value, str) for value in values),
        f"exact six-coordinate box:{label}",
    )
    try:
        box = tuple(Fraction(value) for value in values)
    except (ValueError, ZeroDivisionError) as error:
        raise Round263Error(f"exact rational box:{label}") from error
    need(
        all(box[2 * axis] < box[2 * axis + 1] for axis in range(3)),
        f"positive exact box:{label}",
    )
    return box


def add_geometry(
    geometry: dict[str, dict[str, Any]],
    occurrence_id: str,
    chart: str,
    box_values: list[str],
    official_key_id: str,
    official_key_ordinal: int,
    source: str,
) -> None:
    need(occurrence_id not in geometry, f"unique geometry id:{occurrence_id}")
    need(chart in {"G:E", "G:N", "G:W", "G:S"}, f"source chart:{occurrence_id}")
    need(
        isinstance(official_key_id, str)
        and isinstance(official_key_ordinal, int)
        and not isinstance(official_key_ordinal, bool),
        f"official key binding:{occurrence_id}",
    )
    box = exact_box(box_values, occurrence_id)
    geometry[occurrence_id] = {
        "source_chart": chart,
        "box": box,
        "box_text": list(box_values),
        "official_key_id": official_key_id,
        "official_key_ordinal": official_key_ordinal,
        "geometry_source": source,
    }


def reconstruct_geometry(
    round179: dict[str, Any],
    round204: dict[str, Any],
    round208: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    geometry: dict[str, dict[str, Any]] = {}

    census179 = round179["table_census_and_sha256"]
    columns = round179["row_column_schemas"]["resolved_3d_child_rows"]
    packed_rows = round179["resolved_3d_child_rows"]
    need(
        census179["resolved_3d_child_rows"]["row_count"] == 17_192
        and len(packed_rows) == 17_192,
        "Round179 resolved-child census",
    )
    need(
        census179["resolved_3d_child_rows"]["rows_sha256"]
        == digest(packed_rows),
        "Round179 resolved-child rows digest",
    )
    need(
        len(columns) == len(set(columns))
        and {
            "row_id",
            "chart",
            "box",
            "official_key_id",
            "official_key_ordinal",
        }.issubset(columns),
        "Round179 resolved-child columns",
    )
    for packed in packed_rows:
        need(len(packed) == len(columns), "Round179 packed row width")
        row = dict(zip(columns, packed, strict=True))
        add_geometry(
            geometry,
            row["row_id"],
            row["chart"],
            row["box"],
            row["official_key_id"],
            row["official_key_ordinal"],
            "ROUND179_RESOLVED_3D_CHILD",
        )

    rows204 = check_closed_rows(
        round204["formal_local_open_3D_region_ledger"],
        "region_row_id",
        736,
    )
    for row in rows204:
        need(
            row["strict_open_region"] is True
            and row["ambient_dimension"] == 3
            and row["positive_coordinate_volume"] is True,
            f"Round204 strict 3D occurrence:{row['region_row_id']}",
        )
        add_geometry(
            geometry,
            row["region_row_id"],
            row["chart"],
            row["leaf_exact_box"],
            row["official_key_id"],
            row["official_key_ordinal"],
            "ROUND204_LOCAL_OPEN_3D_REGION",
        )

    rows208 = check_closed_rows(
        round208["formal_local_open_3D_signature_ledger"],
        "region_row_id",
        36_040,
    )
    for row in rows208:
        signature = row["local_return_signature"]
        need(
            row["strict_open_3D_region_exists"] is True
            and row["formal_local_open_3D_signature_credit"] == 1,
            f"Round208 strict 3D occurrence:{row['region_row_id']}",
        )
        add_geometry(
            geometry,
            row["region_row_id"],
            signature["source_chart"],
            row["Round182_leaf_box"],
            signature["official_key_id"],
            signature["official_key_ordinal"],
            "ROUND208_LOCAL_OPEN_3D_SIGNATURE",
        )

    need(len(geometry) == 53_968, "complete 53,968-occurrence geometry")
    source_counts = Counter(
        row["geometry_source"] for row in geometry.values()
    )
    chart_counts = Counter(row["source_chart"] for row in geometry.values())
    need(
        dict(sorted(source_counts.items())) == EXPECTED_GEOMETRY_SOURCE_COUNTS,
        "geometry-source census",
    )
    need(
        dict(sorted(chart_counts.items())) == EXPECTED_SOURCE_CHART_COUNTS,
        "source-chart census",
    )
    return geometry


def input_binding() -> dict[str, Any]:
    return {
        name: {
            "file_sha256": specification["file_sha256"],
            "result_sha256": specification["result_sha256"],
            "schema": specification["schema"],
        }
        for name, specification in sorted(INPUTS.items())
    }


def ledger_identity_row(
    label: str,
    value: dict[str, Any],
    id_field: str,
) -> dict[str, Any]:
    rows = check_closed_rows(value, id_field)
    metadata = {key: item for key, item in value.items() if key != "rows"}
    return closed({
        "frontier_identity_commitment_row_id":
            f"round263-frontier-identity:{label.lower()}",
        "logical_object": label,
        "source_round": 262,
        "post_round": 263,
        "row_count": len(rows),
        "source_rows_sha256": value["rows_sha256"],
        "post_Round263_rows_sha256": value["rows_sha256"],
        "source_ledger_metadata_sha256": digest(metadata),
        "post_Round263_is_exact_alias_of_post_Round262": True,
        "new_row_or_component_assignment_count": 0,
    })


def build(producer_sha256: str) -> dict[str, Any]:
    round171 = load_result(ROUND171_CERTIFICATE)
    round227 = load_result(ROUND227_CERTIFICATE)
    round228 = load_result(ROUND228_CERTIFICATE)
    round179 = load_result(ROUND179_ROWS)
    round204 = load_result(ROUND204_CERTIFICATE)
    round208 = load_result(ROUND208_CERTIFICATE)
    round262 = load_result(ROUND262_CERTIFICATE)

    bridge = round171["exact_source_G_coordinate_bridge"]
    need(
        bridge["all_four_source_G_seams_glue_exactly"] is True
        and bridge["t_map_absolute_endpoint"] == "1/sqrt(2)"
        and len(bridge["seam_rows"]) == 4
        and all(
            row["normal_glues_exactly"] is True
            and row["quarter_turn_and_velocity_glue_for_every_q"] is True
            and row["source_G_position_glues_exactly"] is True
            for row in bridge["seam_rows"]
        ),
        "Round171 exact true-source-seam bridge",
    )

    symmetry = round227["map_contract"]
    need(
        symmetry["Jx_physical_reflection"]
        == "(x,y,s,p)->(-x,y,-s,-p)"
        and symmetry["Jy_physical_reflection"]
        == "(x,y,s,p)->(x,-y,s,-p)"
        and symmetry["both_maps_nonidentity_on_physical_space"] is True
        and symmetry[
            "symmetry_partner_is_same_physical_point_atlas_transition"
        ] is False
        and symmetry["equivariance_does_not_authorize_union_find_edge"] is True
        and round227["census"]["physical_glue_credit"] == 0
        and round227["census"]["component_union_credit"] == 0,
        "Round227 Jx/Jy non-glue contract",
    )

    precedent = round228["scope_contract"]
    need(
        precedent["true_source_chart_seams_exist_and_glue_exactly"] is True
        and precedent[
            "materialized_Round211_sheet_leaves_meet_true_source_chart_seams"
        ] is False
        and precedent["claim_applies_only_to_materialized_Round211_sheet_pool"]
        is True
        and precedent["all_future_retained_strata_exhausted"] is False
        and round228["census"]["Round211_sheet_count"] == 17_716
        and round228["census"]["source_chart_seam_overlap_candidate_count"]
        == 0,
        "Round228 bounded-scope precedent",
    )

    need(
        round262["census"]["occurrence_assignment_count"] == 53_968
        and round262["census"]["exact_key_count"] == 116
        and round262["census"]["remaining_fail_closed_face_count"] == 0,
        "Round262 closure and complete frontier precondition",
    )
    need(
        round262["strict_nonpromotion"]["maximal_physical_component_credit"]
        == 0
        and round262["strict_nonpromotion"]["global_exact_key_fibre_credit"]
        == 0
        and round262["strict_nonpromotion"][
            "global_exact_key_disposition_credit"
        ] == 0
        and round262["strict_nonpromotion"]["Gate5_filled_field_slot_count"]
        == 10
        and round262["strict_nonpromotion"]["Gate5_total_field_slot_count"]
        == 18
        and round262["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "Round262 strict nonpromotion",
    )

    occurrence_frontier = check_closed_rows(
        round262["formal_post_Round262_occurrence_frontier_ledger"],
        "post_frontier_row_id",
        53_968,
    )
    component_frontier = check_closed_rows(
        round262["formal_post_Round262_component_commitment_ledger"],
        "post_Round262_component_row_id",
        round262["census"]["post_Round262_component_count"],
    )
    key_frontier = check_closed_rows(
        round262["formal_post_Round262_key_frontier_ledger"],
        "post_Round262_key_frontier_row_id",
        116,
    )

    geometry = reconstruct_geometry(round179, round204, round208)
    occurrence_by_id = {
        row["local_occurrence_row_id"]: row for row in occurrence_frontier
    }
    need(
        len(occurrence_by_id) == 53_968
        and set(occurrence_by_id) == set(geometry),
        "Round262 frontier equals reconstructed occurrence universe",
    )

    component_by_id = {
        row["post_Round262_quotient_component_id"]: row
        for row in component_frontier
    }
    need(
        len(component_by_id) == len(component_frontier),
        "unique post-Round262 components",
    )
    occurrences_by_key: Counter[str] = Counter()
    components_by_key: Counter[str] = Counter(
        row["official_key_id"] for row in component_frontier
    )

    disposition_rows: list[dict[str, Any]] = []
    maximum_absolute_t = Fraction(0)
    minimum_gap: Fraction | None = None
    source_counts: Counter[str] = Counter()
    source_charts: Counter[str] = Counter()
    for occurrence_id in sorted(geometry):
        item = geometry[occurrence_id]
        frontier = occurrence_by_id[occurrence_id]
        component_id = frontier["post_Round262_quotient_component_id"]
        need(component_id in component_by_id, f"component assignment:{occurrence_id}")
        need(
            frontier["official_key_id"] == item["official_key_id"]
            and frontier["official_key_ordinal"] == item["official_key_ordinal"]
            and component_by_id[component_id]["official_key_id"]
            == item["official_key_id"],
            f"exact-key-pure occurrence binding:{occurrence_id}",
        )
        t_lower, t_upper = item["box"][0], item["box"][1]
        max_absolute_t = max(abs(t_lower), abs(t_upper))
        seam_square_gap = Fraction(1, 2) - max_absolute_t * max_absolute_t
        need(seam_square_gap > 0, f"strict source-chart interior:{occurrence_id}")
        maximum_absolute_t = max(maximum_absolute_t, max_absolute_t)
        minimum_gap = (
            seam_square_gap
            if minimum_gap is None
            else min(minimum_gap, seam_square_gap)
        )
        source_counts[item["geometry_source"]] += 1
        source_charts[item["source_chart"]] += 1
        occurrences_by_key[item["official_key_id"]] += 1
        disposition_rows.append(closed({
            "cross_chart_transition_disposition_row_id":
                "round263-cross-chart-transition:" + digest([occurrence_id]),
            "local_occurrence_row_id": occurrence_id,
            "geometry_source": item["geometry_source"],
            "source_chart": item["source_chart"],
            "official_key_id": item["official_key_id"],
            "official_key_ordinal": item["official_key_ordinal"],
            "post_Round262_quotient_component_id": component_id,
            "post_Round263_quotient_component_id": component_id,
            "exact_box_sha256": digest(item["box_text"]),
            "exact_t_interval": item["box_text"][0:2],
            "maximum_absolute_t_endpoint": qtext(max_absolute_t),
            "exact_true_source_seam_square_gap":
                qtext(seam_square_gap),
            "true_source_chart_seam_equation": "2*t^2-1=0",
            "true_same_point_source_chart_seam_candidate": False,
            "disposition":
                "STRICT_TRUE_SOURCE_CHART_INTERIOR__NO_SEAM_INTERSECTION",
            "physical_glue_credit": 0,
            "component_union_credit": 0,
            "maximality_credit": 0,
        }))
    disposition_rows.sort(
        key=lambda row: row["cross_chart_transition_disposition_row_id"]
    )

    need(
        maximum_absolute_t == EXPECTED_MAXIMUM_ABSOLUTE_T
        and minimum_gap == EXPECTED_MINIMUM_SEAM_SQUARE_GAP,
        "global exact source-seam margin",
    )
    need(
        dict(sorted(source_counts.items())) == EXPECTED_GEOMETRY_SOURCE_COUNTS
        and dict(sorted(source_charts.items())) == EXPECTED_SOURCE_CHART_COUNTS,
        "complete occurrence partition",
    )

    key_by_id = {row["official_key_id"]: row for row in key_frontier}
    need(len(key_by_id) == 116, "unique post-Round262 exact keys")
    for key_id, row in key_by_id.items():
        need(
            row["local_occurrence_count"] == occurrences_by_key[key_id]
            and row["post_Round262_quotient_component_count"]
            == components_by_key[key_id],
            f"post-Round262 key-frontier conservation:{key_id}",
        )

    symmetry_rows = [
        closed({
            "physical_symmetry_non_glue_row_id":
                f"round263-physical-symmetry-non-glue:{generator}",
            "generator": generator,
            "physical_map": symmetry[f"{generator}_physical_reflection"],
            "map_kind": "NONIDENTITY_PHYSICAL_SYMMETRY",
            "same_physical_point_atlas_transition": False,
            "may_supply_source_chart_union_find_edge": False,
            "equivariance_credit_preserved": True,
            "physical_glue_credit": 0,
            "component_union_credit": 0,
        })
        for generator in ("Jx", "Jy")
    ]

    frontier_identity_rows = [
        ledger_identity_row(
            "POST_ROUND262_COMPONENT_COMMITMENT",
            round262["formal_post_Round262_component_commitment_ledger"],
            "post_Round262_component_row_id",
        ),
        ledger_identity_row(
            "POST_ROUND262_OCCURRENCE_FRONTIER",
            round262["formal_post_Round262_occurrence_frontier_ledger"],
            "post_frontier_row_id",
        ),
        ledger_identity_row(
            "POST_ROUND262_KEY_FRONTIER",
            round262["formal_post_Round262_key_frontier_ledger"],
            "post_Round262_key_frontier_row_id",
        ),
    ]

    post_component_count = len(component_frontier)
    census = {
        "complete_occurrence_count": 53_968,
        "Round179_resolved_3D_child_occurrence_count": 17_192,
        "Round204_local_open_3D_occurrence_count": 736,
        "Round208_local_open_3D_occurrence_count": 36_040,
        "source_chart_histogram": dict(sorted(source_charts.items())),
        "maximum_absolute_t_over_all_occurrence_exact_boxes":
            qtext(maximum_absolute_t),
        "minimum_exact_gap_1_over_2_minus_max_absolute_t_squared":
            qtext(minimum_gap),
        "strict_positive_source_seam_gap_count": 53_968,
        "nonpositive_source_seam_gap_count": 0,
        "true_source_chart_seam_candidate_count": 0,
        "Jx_Jy_physical_symmetry_generator_count": 2,
        "Jx_Jy_same_point_glue_generator_count": 0,
        "new_cross_chart_transition_edge_count": 0,
        "new_component_union_credit": 0,
        "post_Round262_component_count": post_component_count,
        "post_Round263_component_count": post_component_count,
        "occurrence_frontier_count": 53_968,
        "exact_key_frontier_count": 116,
        "maximal_component_assignment_count": 0,
        "exhausted_fibre_count": 0,
        "global_disposition_count": 0,
    }

    return {
        "status": (
            "CERTIFIED_COMPLETE_53968_OCCURRENCE_TRUE_SOURCE_CHART_SEAM_"
            "EXHAUSTION__ZERO_SAME_POINT_CANDIDATES__JX_JY_NON_GLUE__"
            "POST_ROUND262_QUOTIENT_AND_FRONTIERS_UNCHANGED"
        ),
        "formal_input_binding": input_binding(),
        "formal_complete_occurrence_cross_chart_transition_disposition_ledger":
            ledger(
                disposition_rows,
                "cross_chart_transition_disposition_row_id",
            ),
        "formal_physical_symmetry_non_glue_ledger": ledger(
            symmetry_rows,
            "physical_symmetry_non_glue_row_id",
        ),
        "formal_post_Round262_quotient_and_frontier_identity_ledger": ledger(
            frontier_identity_rows,
            "frontier_identity_commitment_row_id",
        ),
        "census": census,
        "scope_contract": {
            "Round171_true_source_chart_seams_are_exactly_pinned": True,
            "true_source_chart_seam_equation": "2*t^2-1=0",
            "all_53968_occurrence_exact_boxes_independently_reconstructed":
                True,
            "all_53968_occurrence_exact_boxes_are_strictly_inside_their_"
            "true_source_chart": True,
            "complete_occurrence_true_same_point_source_chart_transition_"
            "candidate_count": 0,
            "Round228_materialized_sheet_scope_precedent_is_strictly_"
            "extended_to_the_complete_occurrence_universe": True,
            "Jx_and_Jy_are_physical_symmetries_not_same_point_chart_"
            "transitions": True,
            "physical_symmetry_equivariance_does_not_authorize_a_component_"
            "edge": True,
            "post_Round262_component_ids_and_assignments_are_unchanged": True,
            "post_Round262_occurrence_and_key_frontiers_are_unchanged": True,
            "cross_chart_transition_exhaustion_is_not_component_maximality":
            True,
        },
        "strict_nonpromotion": {
            "new_physical_glue_credit": 0,
            "new_component_union_credit": 0,
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
            "prove maximality of the frozen post-Round262 physical "
            "components and exhaust all 116 exact-key fibres; retain zero "
            "Jx/Jy component credit"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "upstream_producer_imported_or_executed": False,
            "arithmetic": "fractions.Fraction exact rational",
            "Round262_pin_state":
                "FROZEN_EXACT_PIN_REQUIRED_BEFORE_EXECUTION",
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
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
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
        "occurrences=53968 true_source_seam_candidates=0 "
        "Jx_Jy_same_point_glue=0 new_edges=0"
    )
    print(
        "post_Round263_components="
        f"{result['census']['post_Round263_component_count']} "
        "frontiers=53968/116 unchanged=true"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
