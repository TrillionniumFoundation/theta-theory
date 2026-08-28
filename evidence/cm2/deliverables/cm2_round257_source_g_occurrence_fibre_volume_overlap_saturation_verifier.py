#!/usr/bin/env python3
"""Independently verify Round257 without importing or executing its producer."""

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
OUTPUT = HERE / "cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation_verification.json"
CANDIDATE = HERE / "cm2_round257_source_g_occurrence_fibre_volume_overlap_saturation_certificate.json"
CANDIDATE_SHA256 = "320d8221dcc11d227f667a9e7efbd64c5e40f1de214b22ddd5264079b93504fb"
SCHEMA = "cm2.round257.source-g-occurrence-fibre-volume-overlap-saturation-verification.v1"
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


def load_envelope(path: Path, expected_sha256: str) -> dict[str, Any]:
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode) and not path.is_symlink()
        and 0 < info.st_size <= 500_000_000,
        f"regular:{path.name}",
    )
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected_sha256, f"pin:{path.name}")
    document = json.loads(raw)
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        f"envelope:{path.name}",
    )
    return document


def load_input(name: str) -> dict[str, Any]:
    return load_envelope(HERE / name, PINS[name])["result"]


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


def box(values: list[str]) -> tuple[Fraction, ...]:
    need(len(values) == 6, "box dimension")
    result = tuple(Fraction(value) for value in values)
    need(result[0] < result[1] and result[2] < result[3] and result[4] < result[5], "box")
    return result


def text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def reconstruct() -> dict[str, Any]:
    rows179 = load_input("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    round204 = load_input(
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )
    round208 = load_input(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )
    round256 = load_input(
        "cm2_round256_source_g_local_occurrence_carrier_completion_certificate.json"
    )

    geometry: dict[str, tuple[str, list[str], str]] = {}
    columns = rows179["row_column_schemas"]["resolved_3d_child_rows"]
    for packed in rows179["resolved_3d_child_rows"]:
        row = dict(zip(columns, packed))
        geometry[row["row_id"]] = (row["chart"], row["box"], "ROUND179_RESOLVED_CHILD")
    for row in round204["formal_local_open_3D_region_ledger"]["rows"]:
        geometry[row["region_row_id"]] = (
            row["chart"], row["leaf_exact_box"], "ROUND204_STRICT_OPEN_REGION"
        )
    for row in round208["formal_local_open_3D_signature_ledger"]["rows"]:
        geometry[row["region_row_id"]] = (
            row["local_return_signature"]["source_chart"],
            row["Round182_leaf_box"],
            "ROUND208_STRICT_OPEN_REGION",
        )
    frontier = round256[
        "formal_post_Round256_complete_occurrence_quotient_frontier_ledger"
    ]["rows"]
    need(
        len(geometry) == len(frontier) == 53_968
        and set(geometry) == {row["local_occurrence_row_id"] for row in frontier},
        "geometry/frontier bijection",
    )

    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    gauges: Counter[str] = Counter()
    components: set[str] = set()
    for occurrence in frontier:
        occurrence_id = occurrence["local_occurrence_row_id"]
        chart, values, gauge = geometry[occurrence_id]
        need(gauge == occurrence["local_occurrence_gauge"], f"gauge:{occurrence_id}")
        component_id = occurrence["post_Round256_quotient_component_id"]
        gauges[gauge] += 1
        components.add(component_id)
        groups[(occurrence["official_key_id"], chart)].append({
            "occurrence_id": occurrence_id,
            "component_id": component_id,
            "box": box(values),
            "ordinal": occurrence["official_key_ordinal"],
        })
    need(len(groups) == 116, "key/chart groups")

    positive_rows: list[dict[str, Any]] = []
    key_rows: list[dict[str, Any]] = []
    global_records: list[list[Any]] = []
    totals: Counter[str] = Counter()
    for (key_id, chart), rows in sorted(groups.items()):
        rows.sort(key=lambda row: (row["box"][0], row["occurrence_id"]))
        active: list[dict[str, Any]] = []
        records: list[list[Any]] = []
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
                widths: list[str] = []
                if y_width <= 0:
                    disposition = "REJECT_NONPOSITIVE_Y_INTERSECTION"
                    counts["nonpositive_y_intersection_count"] += 1
                else:
                    z_width = min(other["box"][5], current["box"][5]) - max(
                        other["box"][4], current["box"][4]
                    )
                    if z_width <= 0:
                        disposition = "REJECT_NONPOSITIVE_Z_INTERSECTION"
                        counts["nonpositive_z_intersection_count"] += 1
                    else:
                        x_width = min(other["box"][1], current["box"][1]) - max(
                            other["box"][0], current["box"][0]
                        )
                        need(x_width > 0, f"x width:{pair_id}")
                        widths = [text(x_width), text(y_width), text(z_width)]
                        same = other["component_id"] == current["component_id"]
                        disposition = (
                            "ACCEPT_ALREADY_INTERNAL_TO_COMPONENT" if same
                            else "ACCEPT_CROSS_COMPONENT_PHYSICAL_GLUE"
                        )
                        counts["positive_volume_overlap_count"] += 1
                        counts[
                            "same_component_positive_volume_overlap_count"
                            if same else "cross_component_positive_volume_overlap_count"
                        ] += 1
                        positive_rows.append(closed({
                            "positive_overlap_row_id": pair_id,
                            "official_key_id": key_id,
                            "official_key_ordinal": current["ordinal"],
                            "source_chart": chart,
                            "occurrence_row_ids": pair_ids,
                            "post_Round256_quotient_component_id": current["component_id"] if same else None,
                            "strict_intersection_widths": widths,
                            "strict_intersection_volume": text(x_width * y_width * z_width),
                            "disposition": disposition,
                            "new_rank_reducing_edge_credit": 0 if same else 1,
                        }))
                record = [pair_id, disposition, widths]
                records.append(record)
                global_records.append(record)
            active.append(current)
        totals.update(counts)
        key_rows.append(closed({
            "key_volume_overlap_audit_row_id": "round257-key-volume-audit:" + digest([key_id, chart]),
            "official_key_id": key_id,
            "official_key_ordinal": rows[0]["ordinal"],
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
            "candidate_disposition_sha256": digest(records),
            "same_chart_same_key_positive_volume_channel_exhausted": True,
        }))
    positive_rows.sort(key=lambda row: row["positive_overlap_row_id"])
    key_rows.sort(key=lambda row: row["official_key_ordinal"])
    need(
        totals["strict_x_overlap_candidate_count"] == 729_700
        and totals["nonpositive_y_intersection_count"] == 581_592
        and totals["nonpositive_z_intersection_count"] == 130_392
        and totals["positive_volume_overlap_count"] == 17_716
        and totals["same_component_positive_volume_overlap_count"] == 17_716
        and totals["cross_component_positive_volume_overlap_count"] == 0,
        "census",
    )
    census = {
        "local_occurrence_count": 53_968,
        "observed_exact_key_count": 116,
        "post_Round256_unified_quotient_component_count": 74_012,
        "post_Round257_unified_quotient_component_count": 74_012,
        "occurrence_bearing_quotient_component_count": len(components),
        "occurrence_geometry_gauge_histogram": dict(sorted(gauges.items())),
        "strict_x_overlap_candidate_count": 729_700,
        "nonpositive_y_intersection_count": 581_592,
        "nonpositive_z_intersection_count": 130_392,
        "positive_volume_overlap_count": 17_716,
        "same_component_positive_volume_overlap_count": 17_716,
        "cross_component_positive_volume_overlap_count": 0,
        "new_rank_reducing_physical_edge_count": 0,
        "maximal_physical_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
        "global_candidate_disposition_sha256": digest(global_records),
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
    candidate_document = load_envelope(CANDIDATE, CANDIDATE_SHA256)
    need(
        candidate_document["schema"]
        == "cm2.round257.source-g-occurrence-fibre-volume-overlap-saturation.v1",
        "candidate schema",
    )
    reconstructed = reconstruct()
    need(reconstructed == candidate_document["result"], "independent reconstruction")
    census = reconstructed["census"]
    result = {
        "status": "PASS_INDEPENDENT_ROUND257",
        "producer_imported_or_executed": False,
        "candidate_result_sha256": candidate_document["result_sha256"],
        "verified_occurrence_geometry_count": census["local_occurrence_count"],
        "verified_x_overlap_candidate_count": census["strict_x_overlap_candidate_count"],
        "verified_internal_positive_volume_overlap_count": census[
            "same_component_positive_volume_overlap_count"
        ],
        "verified_cross_component_positive_volume_overlap_count": census[
            "cross_component_positive_volume_overlap_count"
        ],
        "verified_post_component_count": census[
            "post_Round257_unified_quotient_component_count"
        ],
        "verified_maximal_component_assignment_count": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    raw = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(raw)
    print(result["status"])
    print(json.dumps(result, sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"verification_sha256={hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
