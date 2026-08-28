#!/usr/bin/env python3
"""Saturate strict positive-volume occurrence-fibre overlaps."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation_certificate.json"
SCHEMA = "cm2.round257.source-g-occurrence-fibre-volume-overlap-saturation.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round256_source_g_local_occurrence_carrier_completion_certificate.json":
        "b72ed5f3c4d28a9ea9fea1eda1e7259db08c3a2bdda40d0959aaee6bf0482772",
}


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read_pinned(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode) and not path.is_symlink()
        and 0 < info.st_size <= 500_000_000,
        f"regular:{name}",
    )
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINS[name], f"pin:{name}")
    return raw


def load_result(name: str) -> dict[str, Any]:
    document = json.loads(read_pinned(name))
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        f"envelope:{name}",
    )
    return document["result"]


def closed(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def ledger(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    need(len(rows) == len({row[id_field] for row in rows}), f"unique:{id_field}")
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def fraction_box(values: list[str]) -> tuple[Fraction, ...]:
    need(len(values) == 6, "box dimension")
    box = tuple(Fraction(value) for value in values)
    need(box[0] < box[1] and box[2] < box[3] and box[4] < box[5], "positive box")
    return box


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def load_occurrence_geometry() -> dict[str, tuple[str, list[str], str]]:
    rows179 = load_result("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    columns = rows179["row_column_schemas"]["resolved_3d_child_rows"]
    geometry: dict[str, tuple[str, list[str], str]] = {}
    for packed in rows179["resolved_3d_child_rows"]:
        row = dict(zip(columns, packed))
        geometry[row["row_id"]] = (row["chart"], row["box"], "ROUND179_RESOLVED_CHILD")

    round204 = load_result(
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )
    for row in round204["formal_local_open_3D_region_ledger"]["rows"]:
        geometry[row["region_row_id"]] = (
            row["chart"], row["leaf_exact_box"], "ROUND204_STRICT_OPEN_REGION"
        )

    round208 = load_result(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )
    for row in round208["formal_local_open_3D_signature_ledger"]["rows"]:
        geometry[row["region_row_id"]] = (
            row["local_return_signature"]["source_chart"],
            row["Round182_leaf_box"],
            "ROUND208_STRICT_OPEN_REGION",
        )
    need(len(geometry) == 53_968, "geometry census")
    return geometry


def build() -> dict[str, Any]:
    round256 = load_result(
        "cm2_round256_source_g_local_occurrence_carrier_completion_certificate.json"
    )
    frontier = round256[
        "formal_post_Round256_complete_occurrence_quotient_frontier_ledger"
    ]["rows"]
    key_frontier = round256[
        "formal_post_Round256_complete_key_quotient_frontier_ledger"
    ]["rows"]
    geometry = load_occurrence_geometry()
    need(len(frontier) == 53_968 and len(key_frontier) == 116, "frontier census")
    need(
        len({row["local_occurrence_row_id"] for row in frontier}) == 53_968
        and {row["local_occurrence_row_id"] for row in frontier} == set(geometry),
        "geometry/frontier bijection",
    )

    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    gauge_histogram: Counter[str] = Counter()
    component_ids: set[str] = set()
    for row in frontier:
        occurrence_id = row["local_occurrence_row_id"]
        chart, box_values, geometry_gauge = geometry[occurrence_id]
        need(geometry_gauge == row["local_occurrence_gauge"], f"gauge:{occurrence_id}")
        component_id = row["post_Round256_quotient_component_id"]
        component_ids.add(component_id)
        gauge_histogram[geometry_gauge] += 1
        groups[(row["official_key_id"], chart)].append({
            "occurrence_id": occurrence_id,
            "component_id": component_id,
            "box": fraction_box(box_values),
            "box_values": box_values,
            "gauge": geometry_gauge,
            "official_key_ordinal": row["official_key_ordinal"],
        })
    need(len(groups) == 116, "group census")

    positive_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    global_dispositions: list[list[Any]] = []
    totals: Counter[str] = Counter()
    for (key_id, chart), rows in sorted(groups.items()):
        rows.sort(key=lambda row: (row["box"][0], row["occurrence_id"]))
        active: list[dict[str, Any]] = []
        dispositions: list[list[Any]] = []
        counts: Counter[str] = Counter()
        for current in rows:
            active = [row for row in active if row["box"][1] > current["box"][0]]
            for other in active:
                pair_ids = sorted([other["occurrence_id"], current["occurrence_id"]])
                pair_id = "round257-overlap-candidate:" + digest(pair_ids)
                counts["strict_x_overlap_candidate_count"] += 1
                y_width = min(other["box"][3], current["box"][3]) - max(
                    other["box"][2], current["box"][2]
                )
                if y_width <= 0:
                    disposition = "REJECT_NONPOSITIVE_Y_INTERSECTION"
                    counts["nonpositive_y_intersection_count"] += 1
                    overlap_widths: list[str] = []
                else:
                    z_width = min(other["box"][5], current["box"][5]) - max(
                        other["box"][4], current["box"][4]
                    )
                    if z_width <= 0:
                        disposition = "REJECT_NONPOSITIVE_Z_INTERSECTION"
                        counts["nonpositive_z_intersection_count"] += 1
                        overlap_widths = []
                    else:
                        x_width = min(other["box"][1], current["box"][1]) - max(
                            other["box"][0], current["box"][0]
                        )
                        need(x_width > 0, f"sweep x:{pair_id}")
                        overlap_widths = [
                            fraction_text(x_width), fraction_text(y_width), fraction_text(z_width)
                        ]
                        same_component = other["component_id"] == current["component_id"]
                        disposition = (
                            "ACCEPT_ALREADY_INTERNAL_TO_COMPONENT" if same_component
                            else "ACCEPT_CROSS_COMPONENT_PHYSICAL_GLUE"
                        )
                        counts["positive_volume_overlap_count"] += 1
                        counts[
                            "same_component_positive_volume_overlap_count"
                            if same_component
                            else "cross_component_positive_volume_overlap_count"
                        ] += 1
                        positive_rows.append(closed({
                            "positive_overlap_row_id": pair_id,
                            "official_key_id": key_id,
                            "official_key_ordinal": current["official_key_ordinal"],
                            "source_chart": chart,
                            "occurrence_row_ids": pair_ids,
                            "post_Round256_quotient_component_id": (
                                current["component_id"] if same_component else None
                            ),
                            "strict_intersection_widths": overlap_widths,
                            "strict_intersection_volume": fraction_text(
                                x_width * y_width * z_width
                            ),
                            "disposition": disposition,
                            "new_rank_reducing_edge_credit": 0 if same_component else 1,
                        }))
                record = [pair_id, disposition, overlap_widths]
                dispositions.append(record)
                global_dispositions.append(record)
            active.append(current)
        totals.update(counts)
        key_rows.append(closed({
            "key_volume_overlap_audit_row_id": "round257-key-volume-audit:" + digest([key_id, chart]),
            "official_key_id": key_id,
            "official_key_ordinal": rows[0]["official_key_ordinal"],
            "source_chart": chart,
            "occurrence_count": len(rows),
            "post_Round256_quotient_component_count": len({row["component_id"] for row in rows}),
            "strict_x_overlap_candidate_count": counts["strict_x_overlap_candidate_count"],
            "nonpositive_y_intersection_count": counts["nonpositive_y_intersection_count"],
            "nonpositive_z_intersection_count": counts["nonpositive_z_intersection_count"],
            "positive_volume_overlap_count": counts["positive_volume_overlap_count"],
            "same_component_positive_volume_overlap_count": counts[
                "same_component_positive_volume_overlap_count"
            ],
            "cross_component_positive_volume_overlap_count": counts[
                "cross_component_positive_volume_overlap_count"
            ],
            "candidate_disposition_sha256": digest(dispositions),
            "same_chart_same_key_positive_volume_channel_exhausted": True,
        }))

    positive_rows.sort(key=lambda row: row["positive_overlap_row_id"])
    key_rows.sort(key=lambda row: row["official_key_ordinal"])
    need(
        totals == {
            "strict_x_overlap_candidate_count": 729_700,
            "nonpositive_y_intersection_count": 581_592,
            "nonpositive_z_intersection_count": 130_392,
            "positive_volume_overlap_count": 17_716,
            "same_component_positive_volume_overlap_count": 17_716,
        },
        "overlap census",
    )
    need(len(positive_rows) == 17_716 and len(key_rows) == 116, "ledger census")

    census = {
        "local_occurrence_count": 53_968,
        "observed_exact_key_count": 116,
        "post_Round256_unified_quotient_component_count": 74_012,
        "post_Round257_unified_quotient_component_count": 74_012,
        "occurrence_bearing_quotient_component_count": len(component_ids),
        "occurrence_geometry_gauge_histogram": dict(sorted(gauge_histogram.items())),
        "strict_x_overlap_candidate_count": totals["strict_x_overlap_candidate_count"],
        "nonpositive_y_intersection_count": totals["nonpositive_y_intersection_count"],
        "nonpositive_z_intersection_count": totals["nonpositive_z_intersection_count"],
        "positive_volume_overlap_count": totals["positive_volume_overlap_count"],
        "same_component_positive_volume_overlap_count": totals[
            "same_component_positive_volume_overlap_count"
        ],
        "cross_component_positive_volume_overlap_count": 0,
        "new_rank_reducing_physical_edge_count": 0,
        "maximal_physical_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
        "global_candidate_disposition_sha256": digest(global_dispositions),
    }
    return {
        "status": (
            "CERTIFIED_53968_OCCURRENCE_GEOMETRIES__729700_X_SWEEP_CANDIDATES__"
            "17716_INTERNAL_POSITIVE_VOLUME_OVERLAPS__ZERO_CROSS_COMPONENT_OVERLAPS"
        ),
        "census": census,
        "formal_input_binding": {name: PINS[name] for name in sorted(PINS)},
        "formal_internal_positive_volume_overlap_ledger": ledger(
            positive_rows, "positive_overlap_row_id"
        ),
        "formal_exact_key_volume_overlap_exhaustion_ledger": ledger(
            key_rows, "key_volume_overlap_audit_row_id"
        ),
        "scope_contract": {
            "all_53968_occurrences_have_exact_rational_open_boxes": True,
            "all_pairs_with_strict_x_overlap_are_deterministically_reconciled": True,
            "all_positive_volume_overlaps_are_internal_to_existing_components": True,
            "same_chart_same_key_positive_volume_overlap_channel_is_exhausted": True,
            "zero_volume_face_contacts_are_not_promoted_by_this_round": True,
            "cross_chart_contacts_are_not_promoted_by_this_round": True,
            "volume_overlap_exhaustion_is_not_full_component_maximality": True,
        },
        "strict_nonpromotion": {
            "new_physical_glue_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "exhaust strict two-sided same-chart boundary-face contacts between distinct "
            "Round257 components, then audit pinned same-point cross-chart transitions"
        ),
    }


def safe_write(raw: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", dir=OUTPUT.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = build()
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    raw = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(raw)
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
