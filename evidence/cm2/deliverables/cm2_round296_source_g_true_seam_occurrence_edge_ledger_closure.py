#!/usr/bin/env python3
"""Freeze the formal Source-G true-seam occurrence-edge ledger.

Round296 reconstructs every seam cell from frozen geometry and incidence
sources.  It promotes edge evidence only.  It does not run a DSU, assign
component rank, compute a quotient, or promote maximality/fibre/disposition.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import tempfile
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure"
DEFAULT_EDGE = HERE / f"{PREFIX}_edge_ledger.json.gz"
DEFAULT_CELL = HERE / f"{PREFIX}_cell_coverage_ledger.json.gz"
DEFAULT_RESULT = HERE / f"{PREFIX}_result.json"

SCHEMA = "cm2.round296.source-g-true-seam-occurrence-edge-ledger-closure.v1"
EDGE_SCHEMA = "cm2.round296.source-g-true-seam-occurrence-edge-ledger.v1"
CELL_SCHEMA = (
    "cm2.round296.source-g-true-seam-exact-cell-coverage-ledger.v1"
)

MANIFEST_PINS = {
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_manifest.sha256":
        "d2d4c0c34cc25dd92626a656e3a08abb031190f168f4acfe11cd451d886a538f",
    "cm2_round275_source_g_complete_reverse_rechart_materialization_manifest.sha256":
        "a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669",
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_manifest.sha256":
        "c93d7982b036126ea4fcae761316d86863051d19c9fa9a3008b82ef9c6d44081",
    "cm2_round285_source_g_true_seam_safe_pairing_contract_probe_manifest.sha256":
        "260065c2a0253516ebda73ba68db8bd76cd3d6e68fade0535d81b77e1471b952",
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_manifest.sha256":
        "85a9d4fcf9d9931a0e352eeef7582347b12325b92ffc78f2ee40c77c58093751",
    "cm2_round289_source_g_outgoing_seam_tail_child_materialization_manifest.sha256":
        "4786efc0d7f0f060de0702e324176a8e6ea0634288cc71d78c86d7913640036d",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_manifest.sha256":
        "09cec800efc3c7dd21bebab4a226d384f51ec1273040c548bfa54834a25c8331",
}

R268_CERT = (
    "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_"
    "certificate.json"
)
R275_CERT = (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "certificate.json"
)
R282_LEDGER = (
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_"
    "ledger.json.gz"
)
R285_LEDGER = (
    "cm2_round285_source_g_true_seam_safe_pairing_contract_probe_"
    "ledger.json.gz"
)
R287_LEDGER = (
    "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_"
    "ledger.json.gz"
)
R289_LEDGER = (
    "cm2_round289_source_g_outgoing_seam_tail_child_materialization_"
    "ledger.json.gz"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R294_BINDINGS = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "representation_binding_ledger.json.gz"
)
R295B_LEDGER = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_ledger.json.gz"
)
R295B_RESULT = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_result.json"
)

EXPECTED_PREVIEW = {
    "exact_cell_count": 3_444,
    "full_patch_exact_cell_count": 148,
    "tail_patch_exact_cell_count": 3_296,
    "formal_true_seam_edge_count": 48_444,
    "full_patch_edge_count": 504,
    "tail_patch_edge_count": 47_940,
    "distinct_unordered_endpoint_pair_count": 15_316,
    "distinct_occurrence_target_count": 5_784,
    "self_edge_count": 0,
    "common_payload_count_per_cell_histogram": {"1": 2_880, "2": 564},
    "tail_patch_cell_count_histogram": {"8": 8, "104": 8, "300": 8},
}

ZERO_FIELDS = (
    "formal_component_union_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)


class Round296Error(RuntimeError):
    """Fail-closed Round296 contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round296Error(label)


ENCODER = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for piece in chunks(value):
        state.update(piece)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1024 * 1024), b""):
            state.update(piece)
    return state.hexdigest()


def read_json(name: str) -> dict[str, Any]:
    with (HERE / name).open("rb") as stream:
        value = json.load(stream)
    need(isinstance(value, dict), f"JSON object:{name}")
    return value


def read_gzip(name: str) -> dict[str, Any]:
    with gzip.open(HERE / name, "rb") as stream:
        value = json.load(stream)
    need(isinstance(value, dict), f"gzip JSON object:{name}")
    return value


def parse_manifest(name: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in (HERE / name).read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, f"manifest syntax:{name}")
        sha256, filename = match.groups()
        need(filename not in rows, f"manifest duplicate:{name}:{filename}")
        rows[filename] = sha256
    need(rows, f"nonempty manifest:{name}")
    return rows


def verify_packages() -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for manifest, manifest_sha in sorted(MANIFEST_PINS.items()):
        need(
            file_sha256(HERE / manifest) == manifest_sha,
            f"manifest byte pin:{manifest}",
        )
        entries = parse_manifest(manifest)
        for filename, expected in entries.items():
            need(
                file_sha256(HERE / filename) == expected,
                f"package byte pin:{manifest}:{filename}",
            )
        output[manifest] = entries
    return output


def closed(row: dict[str, Any], label: str) -> None:
    payload = dict(row)
    row_sha = payload.pop("row_sha256", None)
    need(row_sha == digest(payload), f"closed row:{label}")


def validate_table(
    table: dict[str, Any],
    *,
    count: int,
    id_field: str,
    label: str,
) -> list[dict[str, Any]]:
    rows = table.get("rows")
    need(
        table.get("row_count") == count
        and isinstance(rows, list)
        and len(rows) == count,
        f"table envelope:{label}",
    )
    ids = [row[id_field] for row in rows]
    hashes = [row["row_sha256"] for row in rows]
    need(
        len(set(ids)) == count
        and table.get("row_ids_sha256") == digest(ids)
        and table.get("row_hashes_sha256") == digest(hashes)
        and table.get("rows_sha256") == digest(rows),
        f"table commitments:{label}",
    )
    for row in rows:
        closed(row, f"{label}:{row[id_field]}")
    return rows


def fraction_box(values: list[str], label: str) -> tuple[Fraction, ...]:
    box = tuple(map(Fraction, values))
    need(
        len(box) == 4 and box[0] < box[1] and box[2] < box[3],
        f"positive p-s box:{label}",
    )
    return box


def box_strings(box: tuple[Fraction, ...]) -> list[str]:
    return [str(value) for value in box]


def intersection(
    left: tuple[Fraction, ...],
    right: tuple[Fraction, ...],
) -> tuple[Fraction, ...] | None:
    box = (
        max(left[0], right[0]),
        min(left[1], right[1]),
        max(left[2], right[2]),
        min(left[3], right[3]),
    )
    return box if box[0] < box[1] and box[2] < box[3] else None


def contains(
    outer: tuple[Fraction, ...],
    inner: tuple[Fraction, ...],
) -> bool:
    return (
        outer[0] <= inner[0] <= inner[1] <= outer[1]
        and outer[2] <= inner[2] <= inner[3] <= outer[3]
    )


def box_area(box: tuple[Fraction, ...]) -> Fraction:
    return (box[1] - box[0]) * (box[3] - box[2])


def physical_payload(region: dict[str, Any]) -> dict[str, Any]:
    signature = region["local_return_signature"]
    payload = {
        "target_chart": signature["target_chart"],
        "target_lift": signature["target_lift"],
        "outgoing_cell": signature["outgoing_cell"],
        "ordered_integer_wall_events":
            signature["ordered_integer_wall_events"],
        "roof": signature["roof"],
        "signed_wall_word": signature["signed_wall_word"],
    }
    need(
        set(payload) == {
            "target_chart", "target_lift", "outgoing_cell",
            "ordered_integer_wall_events", "roof", "signed_wall_word",
        },
        "complete transported physical payload",
    )
    return payload


def interval_distance(
    point: Fraction,
    lower: Fraction,
    upper: Fraction,
) -> Fraction:
    if lower <= point <= upper:
        return Fraction(0)
    return min(abs(point - lower), abs(point - upper))


def ledger(
    rows: list[dict[str, Any]],
    *,
    schema: str,
    status: str,
    id_field: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), f"unique output IDs:{id_field}")
    return {
        "schema": schema,
        "status": status,
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def attachment(value: dict[str, Any], filename: str) -> dict[str, Any]:
    return {
        "filename": filename,
        "schema": value["schema"],
        "row_count": value["row_count"],
        "row_ids_sha256": value["row_ids_sha256"],
        "row_hashes_sha256": value["row_hashes_sha256"],
        "rows_sha256": value["rows_sha256"],
    }


def build(
    producer_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    package_entries = verify_packages()

    r268_doc = read_json(R268_CERT)
    r268 = r268_doc["result"]
    patch_rows = validate_table(
        r268["formal_true_source_seam_positive_patch_ledger"],
        count=152,
        id_field="true_seam_patch_row_id",
        label="Round268 patches",
    )
    patch_by_id = {row["true_seam_patch_row_id"]: row for row in patch_rows}

    r275 = read_json(R275_CERT)["result"]
    strict_regions = validate_table(
        r275["strict_region_ledger"],
        count=5_288,
        id_field="reverse_rechart_region_row_id",
        label="Round275 strict regions",
    )
    arrangement_regions = validate_table(
        r275["arrangement_region_ledger"],
        count=8_500,
        id_field="reverse_rechart_region_row_id",
        label="Round275 arrangement regions",
    )
    region_by_id = {
        row["reverse_rechart_region_row_id"]: row
        for row in strict_regions + arrangement_regions
    }
    need(len(region_by_id) == 13_788, "Round275 region injectivity")

    r282_doc = read_gzip(R282_LEDGER)
    need(
        r282_doc.get("schema")
        == "cm2.round282.source-g-strict-true-seam-normal-corridor-probe."
        "v1.ledger",
        "Round282 schema",
    )
    r282_rows = validate_table(
        r282_doc,
        count=152,
        id_field="Round282_seam_corridor_row_id",
        label="Round282 corridors",
    )
    r282_by_patch = {
        row["Round268_true_seam_patch_row_id"]: row for row in r282_rows
    }
    need(set(r282_by_patch) == set(patch_by_id), "Round282 patch exhaustion")

    r285_doc = read_gzip(R285_LEDGER)
    need(
        r285_doc.get("schema")
        == "cm2.round285.source-g-true-seam-safe-pairing-contract-probe."
        "v1.ledger",
        "Round285 schema",
    )
    r285_rows = validate_table(
        r285_doc,
        count=152,
        id_field="Round285_safe_pairing_row_id",
        label="Round285 pairing",
    )
    r285_by_patch = {
        row["Round268_true_seam_patch_row_id"]: row for row in r285_rows
    }
    need(set(r285_by_patch) == set(patch_by_id), "Round285 patch exhaustion")
    r285_cell_class_histogram: Counter[str] = Counter()
    r285_cell_class_areas: Counter[str] = Counter()
    for patch_id in sorted(patch_by_id):
        patch = patch_by_id[patch_id]
        corridor = r282_by_patch[patch_id]
        safe_pairing = r285_by_patch[patch_id]
        patch_box = fraction_box([
            *patch["exact_common_p_interval"],
            *patch["exact_common_s_interval"],
        ], f"Round268 patch:{patch_id}")
        safe_cells = [
            fraction_box(
                cell["exact_p_s_box"],
                f"Round285 safe cell:{patch_id}:{cell['cell_index']}",
            )
            for cell in safe_pairing["exact_cells"]
        ]
        for cell_row, cell_box in zip(
            safe_pairing["exact_cells"], safe_cells
        ):
            r285_cell_class_histogram[cell_row["classification"]] += 1
            r285_cell_class_areas[cell_row["classification"]] += (
                box_area(cell_box)
            )
        need(
            patch["same_physical_source_point"] is True
            and patch["Round171_normal_position_velocity_identity"] is True
            and patch["owner_shadow_half_open_pair"] is True
            and safe_pairing["same_physical_source_point"] is True
            and safe_pairing[
                "Round171_normal_position_velocity_identity"
            ] is True
            and safe_pairing["transported_owner_target_sets_equal"] is True
            and safe_pairing["owner_shadow_half_open_pair"] is True
            and safe_pairing["cyclic_transition_identity"]
            == patch["cyclic_transition_identity"]
            and safe_pairing["Round282_geometry_classification"]
            == corridor["classification"]
            and safe_pairing["exact_common_p_interval"]
            == patch["exact_common_p_interval"]
            and safe_pairing["exact_common_s_interval"]
            == patch["exact_common_s_interval"]
            and Fraction(safe_pairing["exact_positive_common_area"])
            == Fraction(patch["exact_positive_common_area"])
            == box_area(patch_box)
            and safe_pairing["exact_cell_count"] == len(safe_cells)
            and all(contains(patch_box, cell) for cell in safe_cells)
            and all(
                Fraction(cell_row["exact_positive_area"])
                == box_area(cell_box) > 0
                and (
                    (
                        cell_row["classification"]
                        == "GEOMETRIC_PAIR_PRESENT__"
                        "OCCURRENCE_IDENTITIES_UNISSUED"
                        and cell_row[
                            "transported_physical_payload_"
                            "intersection_nonempty"
                        ] is True
                    )
                    or (
                        cell_row["classification"]
                        == "UNCOVERED_SIDE__"
                        "ARRANGEMENT_REFINEMENT_REQUIRED"
                        and cell_row[
                            "transported_physical_payload_"
                            "intersection_nonempty"
                        ] is False
                    )
                )
                for cell_row, cell_box in zip(
                    safe_pairing["exact_cells"], safe_cells
                )
            )
            and sum(map(box_area, safe_cells), Fraction(0))
            == box_area(patch_box)
            and all(
                intersection(left, right) is None
                for left_index, left in enumerate(safe_cells)
                for right in safe_cells[left_index + 1:]
            )
            and safe_pairing["left_Round182_source_seam_row_id"]
            == patch["left_Round182_source_seam_row_id"]
            and safe_pairing["right_Round182_source_seam_row_id"]
            == patch["right_Round182_source_seam_row_id"]
            and safe_pairing["left_chart"] == patch["left_chart"]
            and safe_pairing["right_chart"] == patch["right_chart"]
            and safe_pairing["left_local_t_root"]
            == patch["left_local_t_root"]
            and safe_pairing["right_local_t_root"]
            == patch["right_local_t_root"],
            f"Round285 semantic safe-pairing contract:{patch_id}",
        )
    need(
        r285_cell_class_histogram == {
            "GEOMETRIC_PAIR_PRESENT__OCCURRENCE_IDENTITIES_UNISSUED":
                464,
            "UNCOVERED_SIDE__ARRANGEMENT_REFINEMENT_REQUIRED": 876,
        }
        and r285_cell_class_areas == {
            "GEOMETRIC_PAIR_PRESENT__OCCURRENCE_IDENTITIES_UNISSUED":
                Fraction(1139, 102400),
            "UNCOVERED_SIDE__ARRANGEMENT_REFINEMENT_REQUIRED":
                Fraction(141, 102400),
        }
        and sum(r285_cell_class_histogram.values()) == 1_340
        and sum(r285_cell_class_areas.values(), Fraction(0))
        == Fraction(1, 80),
        "Round285 exact-cell exhaustive class and area partition",
    )

    r287_doc = read_gzip(R287_LEDGER)
    need(
        r287_doc.get("schema")
        == "cm2.round287.source-g-rechart-terminal-occurrence-disposition."
        "ledger.v1",
        "Round287 schema",
    )
    r287_regions = r287_doc["region_rows"]
    need(
        len(r287_regions) == 13_788
        and r287_doc["region_rows_sha256"] == digest(r287_regions),
        "Round287 region table",
    )
    r287_by_region = {row["Round275_region_id"]: row for row in r287_regions}
    need(len(r287_by_region) == 13_788, "Round287 region injectivity")
    for row in r287_regions:
        closed(row, row["Round287_region_disposition_row_id"])

    r289_doc = read_gzip(R289_LEDGER)
    need(
        r289_doc.get("schema")
        == "cm2.round289.source-g-outgoing-seam-tail-child-materialization."
        "v1.ledger",
        "Round289 schema",
    )
    r289_relations = validate_table(
        r289_doc["region_cell_relation_ledger"],
        count=9_528,
        id_field="Round289_region_cell_relation_id",
        label="Round289 relations",
    )
    r289_by_id = {
        row["Round289_region_cell_relation_id"]: row
        for row in r289_relations
    }

    r294_registry_doc = read_gzip(R294_REGISTRY)
    need(
        r294_registry_doc.get("schema")
        == "cm2.round294.source-g-occurrence-registry-ledger.v1",
        "Round294 registry schema",
    )
    r294_registry = validate_table(
        r294_registry_doc,
        count=431_208,
        id_field="Round294_occurrence_registry_row_id",
        label="Round294 registry",
    )
    formal_occurrence_ids = {
        row["registry_occurrence_id"] for row in r294_registry
    }
    need(len(formal_occurrence_ids) == 431_208, "formal occurrence injectivity")
    registry_source_reference_to_occurrence: dict[str, str] = {}
    for row in r294_registry:
        source_reference = row["source_row_id"]
        need(
            source_reference not in registry_source_reference_to_occurrence,
            f"unique Round294 source-row reference:{source_reference}",
        )
        registry_source_reference_to_occurrence[source_reference] = (
            row["registry_occurrence_id"]
        )

    r294_binding_doc = read_gzip(R294_BINDINGS)
    need(
        r294_binding_doc.get("schema")
        == "cm2.round294.source-g-occurrence-representation-binding-ledger.v1",
        "Round294 binding schema",
    )
    r294_bindings = validate_table(
        r294_binding_doc,
        count=46_288,
        id_field="Round294_occurrence_representation_binding_row_id",
        label="Round294 bindings",
    )

    r295_result = read_json(R295B_RESULT)
    need(
        r295_result.get("status", "").startswith(
            "PASS_ROUND295B_R289_TERMINAL_FACE_ABSENCE_CLOSURE"
        )
        and r295_result["corrected_relation_census"][
            "remaining_R289_terminal_face_frontier_count"
        ] == 0,
        "Round295B sealed closure",
    )
    r295_doc = read_gzip(R295B_LEDGER)
    need(
        r295_doc.get("schema")
        == "cm2.round295b.source-g-r289-terminal-face-absence-closure."
        "v1.ledger.v1",
        "Round295B schema",
    )
    physical_rows = validate_table(
        r295_doc["physical_incidence_binding_ledger"],
        count=11_448,
        id_field="Round295B_physical_incidence_binding_row_id",
        label="Round295B physical incidence",
    )
    wrong_rows = validate_table(
        r295_doc["wrong_signed_empty_no_binding_ledger"],
        count=468,
        id_field="Round295B_wrong_signed_empty_no_binding_row_id",
        label="Round295B wrong-sign no-bind",
    )
    graph_rows = validate_table(
        r295_doc["graph_separated_no_binding_ledger"],
        count=288,
        id_field="Round295B_graph_separated_no_binding_row_id",
        label="Round295B graph no-bind",
    )

    # Build the formal occurrence mapping carried by Round294.  The t^2
    # interval remains present because the terminal face is selected per
    # corridor by nearest exact closure, not by a global region extremum.
    region_mappings: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in r294_registry:
        if (
            row["registry_entry_kind"]
            != "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
        ):
            continue
        for member in row["member_refinement_cells"]:
            region_mappings[row["Round275_region_id"]].append({
                "box": tuple(map(
                    Fraction, member["exact_transformed_open_cell"]
                )),
                "occurrence_id": row["registry_occurrence_id"],
                "source_kind": "ROUND294_REFINED_COMPONENT_MEMBER",
                "source_row_id": row["Round294_occurrence_registry_row_id"],
                "source_row_sha256": row["row_sha256"],
                "source_subrow_id": member["Round292_refinement_cell_id"],
            })
    for row in r294_bindings:
        kind = row["alias_source_kind"]
        if kind == "ROUND287_R275_REGION_INCLUSION_SUBCOVER":
            box: tuple[Fraction, ...] | None = None
        elif kind == "ROUND287_R286_SIGNED_CELL_INCLUSION_SUBCOVER":
            box = tuple(map(Fraction, row["exact_support_representation_box"]))
        elif kind == "ROUND292_R287_EXACT_REFINED_EXISTING_SUBCOVER_CELL":
            box = tuple(map(Fraction, row["exact_transformed_open_cell"]))
        else:
            continue
        region_mappings[row["Round275_region_id"]].append({
            "box": box,
            "occurrence_id": row["target_registry_occurrence_id"],
            "source_kind": kind,
            "source_row_id":
                row["Round294_occurrence_representation_binding_row_id"],
            "source_row_sha256": row["row_sha256"],
            "source_subrow_id": row["source_representation_id"],
        })

    fragments: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    relevant_regions: set[str] = set()
    for patch_id in sorted(patch_by_id):
        corridor_row = r282_by_patch[patch_id]
        patch = patch_by_id[patch_id]
        need(
            corridor_row["exact_common_p_interval"]
            == patch["exact_common_p_interval"]
            and corridor_row["exact_common_s_interval"]
            == patch["exact_common_s_interval"],
            f"Round268/Round282 patch geometry:{patch_id}",
        )
        for side in corridor_row["side_corridors"]:
            side_index = 0 if side["side"] == "left" else 1
            need(side["side"] in {"left", "right"}, f"side:{patch_id}")
            for corridor_index, corridor in enumerate(
                side["accepted_strict_corridors"]
            ):
                region_id = corridor["Round275_region_id"]
                relevant_regions.add(region_id)
                region = region_by_id[region_id]
                disposition = r287_by_region[region_id]
                need(
                    region["complete_10_field_return_signature_sha256"]
                    == corridor["complete_10_field_return_signature_sha256"]
                    == disposition[
                        "complete_10_field_return_signature_sha256"
                    ],
                    f"corridor signature provenance:{region_id}",
                )
                entries = region_mappings.get(region_id, [])
                need(entries, f"formal region occurrence mapping:{region_id}")
                whole = [entry for entry in entries if entry["box"] is None]
                seam_t = Fraction(corridor["seam_dyadic_outer_endpoint"])
                seam_t_square = seam_t * seam_t
                if whole:
                    need(
                        len(whole) == len(entries) == 1,
                        f"unique whole-region mapping:{region_id}",
                    )
                    selected = whole
                    minimum_distance = None
                else:
                    distances = [
                        interval_distance(
                            seam_t_square, entry["box"][0], entry["box"][1]
                        )
                        for entry in entries
                    ]
                    minimum_distance = min(distances)
                    selected = [
                        entry for entry, distance in zip(entries, distances)
                        if distance == minimum_distance
                    ]
                footprint = fraction_box(
                    corridor["positive_ps_footprint"],
                    f"corridor:{patch_id}:{side_index}:{corridor_index}",
                )
                for entry in selected:
                    mapping_ps = (
                        footprint if entry["box"] is None
                        else entry["box"][2:]
                    )
                    exact_box = intersection(footprint, mapping_ps)
                    if exact_box is None:
                        continue
                    occurrence_id = entry["occurrence_id"]
                    need(
                        occurrence_id in formal_occurrence_ids,
                        f"strict fragment formal target:{occurrence_id}",
                    )
                    payload = physical_payload(region)
                    fragment_payload = {
                        "patch_id": patch_id,
                        "side_index": side_index,
                        "source_kind":
                            "ROUND282_STRICT_CORRIDOR_TERMINAL_SLICE",
                        "Round282_seam_corridor_row_id":
                            corridor_row["Round282_seam_corridor_row_id"],
                        "corridor_index": corridor_index,
                        "Round275_region_id": region_id,
                        "Round275_region_row_sha256": region["row_sha256"],
                        "seam_dyadic_endpoint":
                            corridor["seam_dyadic_outer_endpoint"],
                        "seam_dyadic_endpoint_t_square": str(seam_t_square),
                        "terminal_interval_selection_rule":
                            "EXACT_NEAREST_T2_INTERVAL_CLOSURE",
                        "minimum_terminal_interval_distance":
                            (
                                None if minimum_distance is None
                                else str(minimum_distance)
                            ),
                        "mapping_source_kind": entry["source_kind"],
                        "mapping_source_row_id": entry["source_row_id"],
                        "mapping_source_row_sha256":
                            entry["source_row_sha256"],
                        "mapping_source_subrow_id": entry["source_subrow_id"],
                        "mapping_t_square_interval":
                            (
                                None if entry["box"] is None
                                else [
                                    str(entry["box"][0]),
                                    str(entry["box"][1]),
                                ]
                            ),
                        "exact_ps_box": box_strings(exact_box),
                        "physical_payload_sha256": digest(payload),
                        "formal_occurrence_id": occurrence_id,
                    }
                    fragment_id = "round296-seam-fragment:" + digest([
                        "ROUND296_STRICT_TERMINAL_FRAGMENT_V1",
                        fragment_payload,
                    ])
                    fragments[(patch_id, side_index)].append({
                        **fragment_payload,
                        "fragment_id": fragment_id,
                        "box": exact_box,
                        "payload": payload,
                        "occurrence_id": occurrence_id,
                    })

    canonicalized_R295B_reference_count = 0
    already_canonical_R295B_reference_count = 0
    for row in physical_rows:
        relation = r289_by_id[row["Round289_region_cell_relation_id"]]
        region_id = row["Round275_region_id"]
        region = region_by_id[region_id]
        raw_target_reference = row["formal_Round294_occurrence_id"]
        if raw_target_reference in formal_occurrence_ids:
            occurrence_id = raw_target_reference
            target_reference_resolution = (
                "ALREADY_CANONICAL_ROUND294_REGISTRY_OCCURRENCE_ID"
            )
            already_canonical_R295B_reference_count += 1
        else:
            occurrence_id = registry_source_reference_to_occurrence.get(
                raw_target_reference
            )
            need(
                occurrence_id is not None,
                f"Round295B target reference resolves uniquely:"
                f"{raw_target_reference}",
            )
            target_reference_resolution = (
                "CANONICALIZED_ROUND294_SOURCE_ROW_ID_TO_REGISTRY_"
                "OCCURRENCE_ID"
            )
            canonicalized_R295B_reference_count += 1
        need(
            relation["actual_seam_incidence"] is True
            and relation["Round268_true_seam_patch_row_id"]
            == row["Round268_true_seam_patch_row_id"]
            and relation["Round275_region_id"] == region_id
            and occurrence_id in formal_occurrence_ids
            and row["binding_classification"]
            == "FORMAL_EXISTING_ROUND294_OCCURRENCE_PHYSICAL_TERMINAL_FACE_INCIDENCE"
            and row["formal_existing_physical_incidence_binding_credit"] == 1
            and row["formal_seam_edge_credit"] == 0,
            f"Round295B physical source:{row['Round295B_physical_incidence_binding_row_id']}",
        )
        exact_box = fraction_box(
            row["exact_physical_ps_subcell"],
            row["Round295B_physical_incidence_binding_row_id"],
        )
        payload = physical_payload(region)
        fragment_payload = {
            "patch_id": row["Round268_true_seam_patch_row_id"],
            "side_index": row["side_index"],
            "source_kind": "ROUND295B_PHYSICAL_TERMINAL_FACE_INCIDENCE",
            "Round295B_physical_incidence_binding_row_id":
                row["Round295B_physical_incidence_binding_row_id"],
            "Round295B_row_sha256": row["row_sha256"],
            "Round289_region_cell_relation_id":
                row["Round289_region_cell_relation_id"],
            "Round289_relation_row_sha256": relation["row_sha256"],
            "Round275_region_id": region_id,
            "Round275_region_row_sha256": region["row_sha256"],
            "terminal_face_physical_t_square":
                row["terminal_face_physical_t_square"],
            "raw_Round295B_formal_Round294_occurrence_id_field":
                raw_target_reference,
            "Round294_target_reference_resolution":
                target_reference_resolution,
            "exact_ps_box": box_strings(exact_box),
            "physical_payload_sha256": digest(payload),
            "formal_occurrence_id": occurrence_id,
        }
        fragment_id = "round296-seam-fragment:" + digest([
            "ROUND296_R295B_PHYSICAL_FRAGMENT_V1", fragment_payload
        ])
        fragments[(
            row["Round268_true_seam_patch_row_id"], row["side_index"]
        )].append({
            **fragment_payload,
            "fragment_id": fragment_id,
            "box": exact_box,
            "payload": payload,
            "occurrence_id": occurrence_id,
        })

    # No-bind sources remain explicit negative evidence.  They never enter
    # `fragments`, hence can never supply an edge endpoint.
    no_bind: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for rows, id_field, box_field in (
        (
            wrong_rows,
            "Round295B_wrong_signed_empty_no_binding_row_id",
            "exact_empty_intersection_ps_rectangle",
        ),
        (
            graph_rows,
            "Round295B_graph_separated_no_binding_row_id",
            "exact_relation_ps_rectangle",
        ),
    ):
        for row in rows:
            need(
                row["terminal_registry_target_reference_count"] == 0
                and not row["terminal_registry_target_references"]
                and row["formal_existing_physical_incidence_binding_credit"]
                == 0
                and row["formal_seam_edge_credit"] == 0,
                f"strict no-bind:{row[id_field]}",
            )
            no_bind[(
                row["Round268_true_seam_patch_row_id"], row["side_index"]
            )].append({
                "row_id": row[id_field],
                "row_sha256": row["row_sha256"],
                "classification": row["no_binding_classification"],
                "box": fraction_box(row[box_field], row[id_field]),
            })

    fragment_sources = (
        "ROUND282_STRICT_CORRIDOR_TERMINAL_SLICE",
        "ROUND295B_PHYSICAL_TERMINAL_FACE_INCIDENCE",
    )
    source_raw_counts: Counter[str] = Counter()
    source_key_multiplicities: dict[
        str, Counter[tuple[Any, ...]]
    ] = {source: Counter() for source in fragment_sources}
    union_key_multiplicities: Counter[tuple[Any, ...]] = Counter()
    union_key_source_multiplicities: dict[
        tuple[Any, ...], Counter[str]
    ] = defaultdict(Counter)
    all_fragment_ids: set[str] = set()
    for patch_side, rows in fragments.items():
        for fragment in rows:
            source = fragment["source_kind"]
            need(source in fragment_sources, f"fragment source:{source}")
            formal_atom_key = (
                patch_side[0],
                patch_side[1],
                tuple(fragment["exact_ps_box"]),
                fragment["physical_payload_sha256"],
                fragment["occurrence_id"],
            )
            source_raw_counts[source] += 1
            source_key_multiplicities[source][formal_atom_key] += 1
            union_key_multiplicities[formal_atom_key] += 1
            union_key_source_multiplicities[formal_atom_key][source] += 1
            need(
                fragment["fragment_id"] not in all_fragment_ids,
                f"unique raw fragment evidence:{fragment['fragment_id']}",
            )
            all_fragment_ids.add(fragment["fragment_id"])

    def multiplicity_histogram(
        counter: Counter[tuple[Any, ...]],
    ) -> dict[str, int]:
        return {
            str(multiplicity): count
            for multiplicity, count in sorted(
                Counter(counter.values()).items()
            )
        }

    source_fragment_dedup: dict[str, dict[str, Any]] = {}
    for source in fragment_sources:
        multiplicities = source_key_multiplicities[source]
        raw_count = source_raw_counts[source]
        distinct_count = len(multiplicities)
        source_fragment_dedup[source] = {
            "raw_evidence_fragment_count": raw_count,
            "distinct_formal_endpoint_atom_count": distinct_count,
            "duplicate_evidence_excess_count":
                raw_count - distinct_count,
            "formal_atom_evidence_multiplicity_histogram":
                multiplicity_histogram(multiplicities),
        }

    reason_audit: dict[str, Counter[str]] = defaultdict(Counter)
    for key, multiplicity in union_key_multiplicities.items():
        source_counts = union_key_source_multiplicities[key]
        if len(source_counts) == 2:
            reason = (
                "CROSS_ROUND282_ROUND295B_EVIDENCE_FOR_SAME_"
                "OCCURRENCE_BOX_PAYLOAD"
            )
        elif multiplicity == 1:
            reason = "UNIQUE_FORMAL_ENDPOINT_ATOM_EVIDENCE"
        elif fragment_sources[0] in source_counts:
            reason = (
                "MULTIPLE_ROUND282_CORRIDOR_OR_MAPPING_EVIDENCE_FOR_"
                "SAME_OCCURRENCE_BOX_PAYLOAD"
            )
        else:
            reason = (
                "MULTIPLE_ROUND295B_INCIDENCE_ROWS_FOR_SAME_"
                "OCCURRENCE_BOX_PAYLOAD"
            )
        reason_audit[reason]["formal_endpoint_atom_count"] += 1
        reason_audit[reason]["raw_evidence_fragment_count"] += multiplicity
        reason_audit[reason]["duplicate_evidence_excess_count"] += (
            multiplicity - 1
        )

    fragment_dedup_audit = {
        "formal_endpoint_atom_key_fields": [
            "Round268_true_seam_patch_row_id",
            "side_index",
            "exact_ps_box",
            "complete_physical_payload_sha256",
            "actual_Round294_registry_occurrence_id",
        ],
        "raw_evidence_fragment_count": sum(source_raw_counts.values()),
        "distinct_formal_endpoint_atom_count":
            len(union_key_multiplicities),
        "duplicate_evidence_excess_count":
            sum(source_raw_counts.values()) - len(union_key_multiplicities),
        "formal_atom_evidence_multiplicity_histogram":
            multiplicity_histogram(union_key_multiplicities),
        "by_fragment_source": source_fragment_dedup,
        "same_occurrence_box_payload_reason_strata": {
            reason: dict(sorted(counts.items()))
            for reason, counts in sorted(reason_audit.items())
        },
        "raw_evidence_is_retained_only_as_provenance": True,
        "cell_payload_occurrence_maps_deduplicate_formal_atoms": True,
        "edge_keys_derive_from_deduplicated_cell_payload_occurrence_maps":
            True,
    }
    need(
        len(relevant_regions) == 2_636
        and len(fragments) == 304
        and source_raw_counts[fragment_sources[0]] == 3_532
        and source_raw_counts[fragment_sources[1]] == 11_448
        and sum(source_raw_counts.values()) == 14_980,
        "complete strict-plus-tail raw fragment reconstruction:"
        f"regions={len(relevant_regions)};"
        f"patch-sides={len(fragments)};"
        f"sources={dict(source_raw_counts)}",
    )
    need(
        canonicalized_R295B_reference_count == 5_292
        and already_canonical_R295B_reference_count == 6_156,
        "Round295B canonical target-reference census",
    )

    edge_rows: list[dict[str, Any]] = []
    cell_rows: list[dict[str, Any]] = []
    edge_kind_histogram: Counter[str] = Counter()
    common_payload_histogram: Counter[int] = Counter()
    tail_patch_cell_histogram: Counter[int] = Counter()
    endpoint_pair_multiplicity: Counter[tuple[str, str]] = Counter()
    occurrence_targets: set[str] = set()
    self_edge_count = 0

    for patch_id in sorted(patch_by_id):
        patch = patch_by_id[patch_id]
        geometry_class = r282_by_patch[patch_id]["classification"]
        patch_class = (
            "FULL" if geometry_class
            == "FULL_BIDIRECTIONAL_STRICT_NORMAL_CORRIDOR_COVER"
            else "TAIL"
        )
        patch_box = fraction_box([
            *patch["exact_common_p_interval"],
            *patch["exact_common_s_interval"],
        ], patch_id)
        p_cuts = {patch_box[0], patch_box[1]}
        s_cuts = {patch_box[2], patch_box[3]}
        for side_index in (0, 1):
            for fragment in fragments[(patch_id, side_index)]:
                need(
                    contains(patch_box, fragment["box"]),
                    f"fragment inside patch:{fragment['fragment_id']}",
                )
                p_cuts.update(fragment["box"][:2])
                s_cuts.update(fragment["box"][2:])
        p_values = sorted(p_cuts)
        s_values = sorted(s_cuts)
        patch_cells: list[tuple[Fraction, ...]] = [
            (p0, p1, s0, s1)
            for p0, p1 in zip(p_values, p_values[1:])
            for s0, s1 in zip(s_values, s_values[1:])
        ]
        need(
            sum(map(box_area, patch_cells), Fraction(0))
            == box_area(patch_box),
            f"exact patch cell area conservation:{patch_id}",
        )
        if patch_class == "TAIL":
            tail_patch_cell_histogram[len(patch_cells)] += 1

        for cell_index, cell_box in enumerate(patch_cells):
            cell_id = "round296-true-seam-cell:" + digest([
                "ROUND296_TRUE_SEAM_EXACT_HALF_OPEN_PS_CELL_V1",
                patch_id,
                cell_index,
                box_strings(cell_box),
            ])
            side_maps: list[
                dict[str, dict[str, Any]]
            ] = []
            for side_index in (0, 1):
                payload_map: dict[str, dict[str, Any]] = {}
                for fragment in fragments[(patch_id, side_index)]:
                    if not contains(fragment["box"], cell_box):
                        continue
                    payload_sha = fragment["physical_payload_sha256"]
                    binding = payload_map.setdefault(payload_sha, {
                        "physical_payload": fragment["payload"],
                        "occurrence_evidence": defaultdict(set),
                    })
                    need(
                        binding["physical_payload"] == fragment["payload"],
                        f"payload SHA collision:{payload_sha}",
                    )
                    binding["occurrence_evidence"][
                        fragment["occurrence_id"]
                    ].add(fragment["fragment_id"])
                normalized: dict[str, dict[str, Any]] = {}
                for payload_sha, binding in payload_map.items():
                    normalized[payload_sha] = {
                        "physical_payload": binding["physical_payload"],
                        "occurrence_evidence": {
                            occurrence_id: sorted(evidence)
                            for occurrence_id, evidence in sorted(
                                binding["occurrence_evidence"].items()
                            )
                        },
                    }
                side_maps.append(normalized)
            common_payloads = sorted(set(side_maps[0]) & set(side_maps[1]))
            common_payload_histogram[len(common_payloads)] += 1
            need(
                len(common_payloads) in {1, 2},
                f"one-or-two common payloads:{cell_id}",
            )

            cell_edge_ids: list[str] = []
            for payload_sha in common_payloads:
                payload = side_maps[0][payload_sha]["physical_payload"]
                need(
                    payload == side_maps[1][payload_sha]["physical_payload"],
                    f"complete payload equality:{cell_id}:{payload_sha}",
                )
                left = side_maps[0][payload_sha]["occurrence_evidence"]
                right = side_maps[1][payload_sha]["occurrence_evidence"]
                for left_occurrence in sorted(left):
                    for right_occurrence in sorted(right):
                        if left_occurrence == right_occurrence:
                            self_edge_count += 1
                            continue
                        pair = tuple(sorted((
                            left_occurrence, right_occurrence
                        )))
                        edge_payload = {
                            "Round268_true_seam_patch_row_id": patch_id,
                            "Round296_true_seam_cell_id": cell_id,
                            "cell_index": cell_index,
                            "exact_half_open_ps_cell": box_strings(cell_box),
                            "physical_payload": payload,
                            "physical_payload_sha256": payload_sha,
                            "left_formal_occurrence_id": left_occurrence,
                            "right_formal_occurrence_id": right_occurrence,
                            "unordered_formal_occurrence_endpoint_pair":
                                list(pair),
                        }
                        edge_id = "round296-true-seam-occurrence-edge:" + digest([
                            "ROUND296_TRUE_SEAM_OCCURRENCE_EDGE_KEY_V1",
                            edge_payload,
                        ])
                        row = {
                            "Round296_true_seam_occurrence_edge_row_id":
                                edge_id,
                            **edge_payload,
                            "patch_class": patch_class,
                            "cyclic_transition_identity":
                                patch["cyclic_transition_identity"],
                            "left_endpoint_evidence_fragment_ids":
                                left[left_occurrence],
                            "right_endpoint_evidence_fragment_ids":
                                right[right_occurrence],
                            "repeated_endpoint_pair_across_cells_preserved":
                                True,
                            "occurrence_identity_collapsed": False,
                            "formal_true_seam_edge_credit": 1,
                            **{field: 0 for field in ZERO_FIELDS},
                        }
                        row["row_sha256"] = digest(row)
                        edge_rows.append(row)
                        cell_edge_ids.append(edge_id)
                        edge_kind_histogram[patch_class] += 1
                        endpoint_pair_multiplicity[pair] += 1
                        occurrence_targets.update(pair)

            def side_document(side_index: int) -> list[dict[str, Any]]:
                output: list[dict[str, Any]] = []
                for payload_sha, binding in sorted(
                    side_maps[side_index].items()
                ):
                    output.append({
                        "physical_payload_sha256": payload_sha,
                        "physical_payload": binding["physical_payload"],
                        "formal_occurrence_ids":
                            sorted(binding["occurrence_evidence"]),
                        "occurrence_evidence_fragment_ids": {
                            key: value for key, value in sorted(
                                binding["occurrence_evidence"].items()
                            )
                        },
                    })
                return output

            no_bind_rows: list[dict[str, Any]] = []
            for side_index in (0, 1):
                for evidence in no_bind[(patch_id, side_index)]:
                    if contains(evidence["box"], cell_box):
                        no_bind_rows.append({
                            "side_index": side_index,
                            "source_row_id": evidence["row_id"],
                            "source_row_sha256": evidence["row_sha256"],
                            "classification": evidence["classification"],
                        })
            common_document = [{
                "physical_payload_sha256": payload_sha,
                "physical_payload":
                    side_maps[0][payload_sha]["physical_payload"],
                "left_formal_occurrence_ids": sorted(
                    side_maps[0][payload_sha]["occurrence_evidence"]
                ),
                "right_formal_occurrence_ids": sorted(
                    side_maps[1][payload_sha]["occurrence_evidence"]
                ),
            } for payload_sha in common_payloads]
            cell_row = {
                "Round296_true_seam_cell_coverage_row_id": cell_id,
                "Round268_true_seam_patch_row_id": patch_id,
                "Round268_patch_row_sha256": patch["row_sha256"],
                "Round282_seam_corridor_row_id":
                    r282_by_patch[patch_id]["Round282_seam_corridor_row_id"],
                "Round285_safe_pairing_row_id":
                    r285_by_patch[patch_id]["Round285_safe_pairing_row_id"],
                "patch_class": patch_class,
                "cell_index": cell_index,
                "exact_half_open_ps_cell": box_strings(cell_box),
                "exact_positive_cell_area": str(box_area(cell_box)),
                "half_open_p_upper_included":
                    cell_box[1] == patch_box[1],
                "half_open_s_upper_included":
                    cell_box[3] == patch_box[3],
                "left_payload_occurrence_bindings": side_document(0),
                "right_payload_occurrence_bindings": side_document(1),
                "common_physical_payload_count": len(common_payloads),
                "common_physical_payload_bindings": common_document,
                "formal_edge_row_count": len(cell_edge_ids),
                "formal_edge_row_ids": sorted(cell_edge_ids),
                "wrong_sign_or_graph_separated_no_bind_evidence":
                    sorted(no_bind_rows, key=lambda item: (
                        item["side_index"], item["source_row_id"]
                    )),
                "wrong_sign_or_graph_separated_rows_used_as_endpoints": 0,
                "formal_true_seam_edge_credit": 0,
                **{field: 0 for field in ZERO_FIELDS},
            }
            cell_row["row_sha256"] = digest(cell_row)
            cell_rows.append(cell_row)

    edge_rows.sort(
        key=lambda row: row["Round296_true_seam_occurrence_edge_row_id"]
    )
    cell_rows.sort(
        key=lambda row: row["Round296_true_seam_cell_coverage_row_id"]
    )
    edge_ids = [
        row["Round296_true_seam_occurrence_edge_row_id"] for row in edge_rows
    ]
    need(
        len(edge_rows) == len(set(edge_ids))
        and sum(
            row["formal_true_seam_edge_credit"] for row in edge_rows
        ) == len(edge_rows)
        and all(
            row[field] == 0
            for row in edge_rows + cell_rows
            for field in ZERO_FIELDS
        ),
        "formal edge-only credit partition",
    )
    multiplicity_histogram = Counter(endpoint_pair_multiplicity.values())
    computed_preview = {
        "exact_cell_count": len(cell_rows),
        "full_patch_exact_cell_count": sum(
            row["patch_class"] == "FULL" for row in cell_rows
        ),
        "tail_patch_exact_cell_count": sum(
            row["patch_class"] == "TAIL" for row in cell_rows
        ),
        "formal_true_seam_edge_count": len(edge_rows),
        "full_patch_edge_count": edge_kind_histogram["FULL"],
        "tail_patch_edge_count": edge_kind_histogram["TAIL"],
        "distinct_unordered_endpoint_pair_count":
            len(endpoint_pair_multiplicity),
        "distinct_occurrence_target_count": len(occurrence_targets),
        "self_edge_count": self_edge_count,
        "common_payload_count_per_cell_histogram": {
            str(key): value
            for key, value in sorted(common_payload_histogram.items())
        },
        "tail_patch_cell_count_histogram": {
            str(key): value
            for key, value in sorted(tail_patch_cell_histogram.items())
        },
    }
    # These constants are consulted only after complete source reconstruction.
    # They are a post-hoc counterevidence check, never an input to construction.
    need(
        computed_preview == EXPECTED_PREVIEW,
        f"post-reconstruction preview countercheck:{computed_preview}",
    )

    edge_ledger = ledger(
        edge_rows,
        schema=EDGE_SCHEMA,
        status=(
            "FORMAL_48444_TRUE_SEAM_OCCURRENCE_EDGE_ROWS__"
            "NO_DSU_OR_QUOTIENT_EXECUTED"
        ),
        id_field="Round296_true_seam_occurrence_edge_row_id",
    )
    cell_ledger = ledger(
        cell_rows,
        schema=CELL_SCHEMA,
        status=(
            "EXACT_3444_HALF_OPEN_PS_COMMON_REFINEMENT_CELLS__"
            "ALL_152_TRUE_SEAM_PATCHES_COVERED"
        ),
        id_field="Round296_true_seam_cell_coverage_row_id",
    )
    result = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND296_FORMAL_TRUE_SEAM_OCCURRENCE_EDGE_LEDGER__"
            "152_PATCHES__3444_EXACT_CELLS__48444_FORMAL_EDGES__"
            "DSU_NOT_RUN__QUOTIENT_NOT_COMPUTED"
        ),
        "input_package_manifest_pins":
            dict(sorted(MANIFEST_PINS.items())),
        "input_package_entry_count": sum(map(len, package_entries.values())),
        "source_reconstruction_contract": {
            "preview_used_as_construction_oracle": False,
            "preview_consulted_only_after_complete_reconstruction": True,
            "Round282_strict_corridor_terminal_mapping_rule":
                "per-corridor exact nearest t^2 interval closure to the "
                "dyadic seam endpoint",
            "Round295B_physical_incidence_rows_consumed": 11_448,
            "total_terminal_endpoint_evidence_fragment_count": 14_980,
            "Round282_strict_terminal_evidence_fragment_count": 3_532,
            "fragment_raw_vs_formal_atom_dedup_audit":
                fragment_dedup_audit,
            "Round295B_target_references_canonicalized_from_Round294_"
            "source_row_id": canonicalized_R295B_reference_count,
            "Round295B_target_references_already_canonical_occurrence_ID":
                already_canonical_R295B_reference_count,
            "every_edge_endpoint_is_actual_Round294_registry_occurrence_ID":
                True,
            "Round295B_wrong_signed_empty_rows_excluded": 468,
            "Round295B_graph_separated_rows_excluded": 288,
            "wrong_sign_or_graph_separated_row_ever_used_as_endpoint": False,
            "complete_transported_physical_payload_fields": [
                "target_chart", "target_lift", "outgoing_cell",
                "ordered_integer_wall_events", "roof", "signed_wall_word",
            ],
            "pair_only_payloads_common_to_both_sides": True,
            "Round285_safe_pairing_semantics_validated_for_all_152_"
            "patches": True,
            "Round285_validated_semantic_fields": [
                "same_physical_source_point",
                "Round171_normal_position_velocity_identity",
                "transported_owner_target_sets_equal",
                "owner_shadow_half_open_pair",
                "cyclic_transition_identity_matches_Round268",
                "Round282_geometry_classification_matches_Round282",
                "exact_cells_positive_disjoint_and_area_conservative",
            ],
            "Round285_exact_cell_class_histogram": {
                key: value for key, value in sorted(
                    r285_cell_class_histogram.items()
                )
            },
            "Round285_exact_cell_class_area_partition": {
                key: str(value) for key, value in sorted(
                    r285_cell_class_areas.items()
                )
            },
            "Round285_uncovered_negative_cells_used_as_edge_endpoints": 0,
        },
        "census": {
            **computed_preview,
            "true_seam_patch_count": 152,
            "formal_edge_row_count": len(edge_rows),
            "edge_key_count": len(edge_ids),
            "edge_key_collision_count": 0,
            "unordered_endpoint_pair_edge_multiplicity_histogram": {
                str(key): value
                for key, value in sorted(multiplicity_histogram.items())
            },
            "repeated_endpoint_pairs_across_cells_preserved": True,
        },
        "preview_counterevidence_crosscheck": {
            "source_reconstruction_completed_before_comparison": True,
            "computed_values": computed_preview,
            "preview_values": EXPECTED_PREVIEW,
            "exact_match": True,
        },
        "edge_ledger": attachment(edge_ledger, DEFAULT_EDGE.name),
        "cell_coverage_ledger": attachment(
            cell_ledger, DEFAULT_CELL.name
        ),
        "formal_credit_transition": {
            "formal_true_seam_edge_credit": len(edge_rows),
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "strict_nonpromotion": {
            "component_DSU_executed": False,
            "quotient_computed": False,
            "quotient_component_count": None,
            "ordinary_face_edges_consumed_or_promoted": False,
            "maximality_status": "WAITING_FUTURE_EXPLICIT_DSU_ROUND",
            "fibre_status": "WAITING_FUTURE_EXPLICIT_DSU_ROUND",
            "global_disposition_status":
                "WAITING_FUTURE_EXPLICIT_DSU_ROUND",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "scope_contract": {
            "registry_scope":
                "ROUND294_FORMAL_STAGE_A_OCCURRENCE_REGISTRY",
            "true_seam_scope":
                "ALL_152_FROZEN_ROUND268_POSITIVE_AREA_PATCHES",
            "edge_evidence_frozen_without_connectivity_claim": True,
            "future_DSU_must_consume_all_48444_edge_rows": True,
        },
        "provenance": {
            "producer_sha256": producer_sha256,
            "seed_affects_output": False,
            "upstream_producer_imported_or_executed": False,
        },
        "required_next": [
            "Independently reconstruct both ledgers cachelessly without "
            "importing or executing this producer.",
            "Only a later explicit DSU round may turn edge evidence into "
            "rank reduction or a quotient-component census.",
        ],
    }
    return edge_ledger, cell_ledger, result


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=buffer, mtime=0, compresslevel=9
    ) as stream:
        for piece in chunks(value):
            stream.write(piece)
    return buffer.getvalue()


def safe_write(path: Path, payload: bytes) -> None:
    need(path.parent.resolve() == HERE.resolve(), f"output parent:{path}")
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=HERE, prefix=f".{path.name}.", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edge-ledger", type=Path, default=DEFAULT_EDGE)
    parser.add_argument(
        "--cell-coverage-ledger", type=Path, default=DEFAULT_CELL
    )
    parser.add_argument("--result", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--seed", default="296071")
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()

    producer_sha256 = file_sha256(Path(__file__).resolve())
    edges, cells, result = build(producer_sha256)
    edge_bytes = deterministic_gzip(edges)
    cell_bytes = deterministic_gzip(cells)
    result["edge_ledger"]["file_sha256"] = hashlib.sha256(
        edge_bytes
    ).hexdigest()
    result["cell_coverage_ledger"]["file_sha256"] = hashlib.sha256(
        cell_bytes
    ).hexdigest()
    result["seed_affects_output"] = False
    result["result_sha256"] = digest(result)
    result_bytes = canonical(result)
    if not arguments.no_write:
        safe_write(arguments.edge_ledger, edge_bytes)
        safe_write(arguments.cell_coverage_ledger, cell_bytes)
        safe_write(arguments.result, result_bytes)
    print(json.dumps({
        "status": result["status"],
        "seed": arguments.seed,
        "seed_affects_output": False,
        "edge_ledger_file_sha256":
            result["edge_ledger"]["file_sha256"],
        "cell_coverage_ledger_file_sha256":
            result["cell_coverage_ledger"]["file_sha256"],
        "result_file_sha256": hashlib.sha256(result_bytes).hexdigest(),
        "result_sha256": result["result_sha256"],
        "census": result["census"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
