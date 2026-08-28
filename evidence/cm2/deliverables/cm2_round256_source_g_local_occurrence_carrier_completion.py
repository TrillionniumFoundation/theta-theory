#!/usr/bin/env python3
"""Complete quotient assignment with certified local occurrence carriers."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round256_source_g_local_occurrence_carrier_completion_certificate.json"
SCHEMA = "cm2.round256.source-g-local-occurrence-carrier-completion.v1"
PINS = {
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round255_source_g_block_carrier_quotient_augmentation_certificate.json":
        "d7a2ad5175d1671ca4000e287c0c201826e41e4da718fa5af3c840a80417db0d",
}


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read_pinned(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode) and not path.is_symlink()
        and 0 < info.st_size <= 400_000_000,
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


def build() -> dict[str, Any]:
    round204 = load_result(
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )
    round208 = load_result(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )
    round255 = load_result(
        "cm2_round255_source_g_block_carrier_quotient_augmentation_certificate.json"
    )
    regions204 = {
        row["region_row_id"]: row
        for row in round204["formal_local_open_3D_region_ledger"]["rows"]
    }
    regions208 = {
        row["region_row_id"]: row
        for row in round208[
            "formal_local_open_3D_signature_ledger"
        ]["rows"]
    }
    source_frontier = round255[
        "formal_post_Round255_unified_occurrence_quotient_frontier_ledger"
    ]["rows"]
    source_keys = {
        row["official_key_id"]: row
        for row in round255[
            "formal_post_Round255_key_unified_quotient_frontier_ledger"
        ]["rows"]
    }
    need(
        len(regions204) == 736
        and len(regions208) == 36_040
        and len(source_frontier) == 53_968
        and len(source_keys) == 116,
        "input census",
    )

    unassigned = [
        row for row in source_frontier
        if row["quotient_component_assignment_credit"] == 0
    ]
    need(
        len(unassigned) == 1_324
        and Counter(row["local_occurrence_gauge"] for row in unassigned)
        == {
            "ROUND204_STRICT_OPEN_REGION": 736,
            "ROUND208_STRICT_OPEN_REGION": 588,
        },
        "unassigned partition",
    )

    carrier_rows: list[dict[str, Any]] = []
    carrier_by_occurrence: dict[str, dict[str, Any]] = {}
    carrier_count_by_key: Counter[str] = Counter()
    gauge_histogram: Counter[str] = Counter()
    source_kind_histogram: Counter[str] = Counter()
    for occurrence in unassigned:
        occurrence_id = occurrence["local_occurrence_row_id"]
        gauge = occurrence["local_occurrence_gauge"]
        if gauge == "ROUND204_STRICT_OPEN_REGION":
            source = regions204[occurrence_id]
            need(
                source["strict_open_region"] is True
                and source["positive_coordinate_volume"] is True
                and source["ambient_dimension"] == 3
                and source["formal_local_signature_credit"] == 1
                and source["official_key_id"] == occurrence["official_key_id"],
                f"Round204 carrier:{occurrence_id}",
            )
            geometry_box = source["leaf_exact_box"]
            geometry_volume = source["leaf_exact_coordinate_volume"]
            source_kind = f"ROUND204_{source['region_kind']}"
            source_row_sha256 = source["row_sha256"]
        else:
            source = regions208[occurrence_id]
            signature = source["local_return_signature"]
            need(
                source["strict_open_3D_region_exists"] is True
                and source["formal_local_open_3D_signature_credit"] == 1
                and signature["official_key_id"] == occurrence["official_key_id"],
                f"Round208 carrier:{occurrence_id}",
            )
            geometry_box = source["Round182_leaf_box"]
            geometry_volume = source["Round182_leaf_coordinate_volume"]
            source_kind = f"ROUND208_{source['F_sign']}"
            source_row_sha256 = source["row_sha256"]
        component_id = (
            "round256-local-occurrence-carrier-component:"
            + digest([gauge, occurrence_id])
        )
        row = closed({
            "local_occurrence_carrier_row_id":
                "round256-local-occurrence-carrier:" + digest(component_id),
            "post_Round256_quotient_component_id": component_id,
            "component_origin": source_kind,
            "local_occurrence_row_id": occurrence_id,
            "local_occurrence_gauge": gauge,
            "official_key_ordinal": occurrence["official_key_ordinal"],
            "official_key_id": occurrence["official_key_id"],
            "source_certificate_row_sha256": source_row_sha256,
            "certified_local_open_3D_geometry_box": geometry_box,
            "certified_positive_coordinate_volume": geometry_volume,
            "member_occurrence_count": 1,
            "quotient_component_assignment_credit": 1,
            "known_block_incidence_attachment_credit": 0,
            "certified_known_connectivity_only": True,
            "new_physical_bridge_to_existing_component_credit": 0,
            "maximal_physical_component_claimed": False,
            "global_exact_key_fibre_credit": 0,
        })
        carrier_rows.append(row)
        carrier_by_occurrence[occurrence_id] = row
        carrier_count_by_key[occurrence["official_key_id"]] += 1
        gauge_histogram[gauge] += 1
        source_kind_histogram[source_kind] += 1
    carrier_rows.sort(key=lambda row: row["local_occurrence_carrier_row_id"])
    need(
        len(carrier_rows) == len(carrier_by_occurrence) == 1_324
        and gauge_histogram == {
            "ROUND204_STRICT_OPEN_REGION": 736,
            "ROUND208_STRICT_OPEN_REGION": 588,
        },
        "carrier census",
    )

    post_rows: list[dict[str, Any]] = []
    post_gauge_histogram: Counter[str] = Counter()
    for source in source_frontier:
        occurrence_id = source["local_occurrence_row_id"]
        base = {
            key: value
            for key, value in source.items()
            if key not in {"post_frontier_row_id", "row_sha256"}
        }
        component_id = source["post_Round255_quotient_component_id"]
        carrier = carrier_by_occurrence.get(occurrence_id)
        if carrier is not None:
            component_id = carrier["post_Round256_quotient_component_id"]
        base["post_Round256_quotient_component_id"] = component_id
        base["quotient_component_assignment_credit"] = 1
        base["quotient_component_maximality_credit"] = 0
        post_gauge_histogram[source["local_occurrence_gauge"]] += 1
        post_rows.append(closed({
            "post_frontier_row_id":
                "round256-post-complete-quotient-frontier:"
                + digest([occurrence_id, component_id]),
            **base,
        }))
    post_rows.sort(key=lambda row: row["post_frontier_row_id"])
    need(
        len(post_rows) == 53_968
        and all(row["quotient_component_assignment_credit"] == 1 for row in post_rows)
        and dict(post_gauge_histogram) == {
            "ROUND179_RESOLVED_CHILD": 17_192,
            "ROUND204_STRICT_OPEN_REGION": 736,
            "ROUND208_STRICT_OPEN_REGION": 36_040,
        },
        "complete occurrence frontier",
    )

    rows_by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in post_rows:
        rows_by_key[row["official_key_id"]].append(row)
    key_rows: list[dict[str, Any]] = []
    for key_id, rows in rows_by_key.items():
        source = source_keys[key_id]
        key_rows.append(closed({
            "key_frontier_row_id":
                "round256-key-complete-quotient-frontier:" + digest(key_id),
            "official_key_ordinal": source["official_key_ordinal"],
            "official_key_id": key_id,
            "official_key_row": source["official_key_row"],
            "local_occurrence_count": len(rows),
            "post_Round256_quotient_component_count":
                source["post_Round255_quotient_component_count"]
                + carrier_count_by_key[key_id],
            "new_local_occurrence_carrier_count": carrier_count_by_key[key_id],
            "occurrence_quotient_assignment_count": len(rows),
            "occurrences_without_quotient_assignment": 0,
            "occurrence_quotient_assignment_complete": True,
            "occurrences_with_known_block_incidence": sum(
                row["known_block_incidence_attachment_credit"] for row in rows
            ),
            "occurrences_without_known_block_incidence": sum(
                1 - row["known_block_incidence_attachment_credit"] for row in rows
            ),
            "all_quotient_components_proved_maximal": False,
            "global_exact_key_fibre_exhausted": False,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
        }))
    key_rows.sort(key=lambda row: row["key_frontier_row_id"])
    need(
        len(key_rows) == 116
        and all(row["occurrence_quotient_assignment_complete"] for row in key_rows)
        and sum(row["occurrence_quotient_assignment_count"] for row in key_rows)
        == 53_968,
        "complete key frontier",
    )

    census = {
        "Round255_unified_quotient_component_count": 72_688,
        "new_local_occurrence_carrier_component_count": 1_324,
        "post_Round256_unified_quotient_component_count": 74_012,
        "new_Round204_occurrence_assignment_count": 736,
        "new_Round208_occurrence_assignment_count": 588,
        "cumulative_occurrence_quotient_assignment_count": 53_968,
        "occurrences_without_quotient_assignment": 0,
        "keys_with_complete_all_gauge_occurrence_quotient_assignment": 116,
        "post_Round256_occurrences_with_known_block_incidence": 36_200,
        "post_Round256_occurrences_without_known_block_incidence": 17_768,
        "new_occurrence_known_block_incidence_count": 0,
        "local_carrier_source_kind_histogram": dict(sorted(source_kind_histogram.items())),
        "maximal_physical_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }
    return {
        "status": (
            "CERTIFIED_1324_LOCAL_OCCURRENCE_CARRIERS__"
            "53968_OF_53968_QUOTIENT_ASSIGNMENTS__116_OF_116_KEY_FRONTIERS"
        ),
        "census": census,
        "formal_input_binding": {
            name: PINS[name] for name in sorted(PINS)
        },
        "formal_new_local_occurrence_carrier_ledger": ledger(
            carrier_rows, "local_occurrence_carrier_row_id"
        ),
        "formal_post_Round256_complete_occurrence_quotient_frontier_ledger": ledger(
            post_rows, "post_frontier_row_id"
        ),
        "formal_post_Round256_complete_key_quotient_frontier_ledger": ledger(
            key_rows, "key_frontier_row_id"
        ),
        "scope_contract": {
            "all_53968_occurrences_have_unique_quotient_assignments": True,
            "all_116_observed_keys_have_complete_occurrence_assignment": True,
            "all_1324_new_carriers_have_certified_local_open_3D_geometry": True,
            "local_occurrence_carrier_is_not_known_block_membership": True,
            "local_occurrence_carrier_is_not_component_maximality": True,
            "maximal_component_exhaustion_remains_the_next_gate": True,
        },
        "strict_nonpromotion": {
            "new_occurrence_known_block_incidence_credit": 0,
            "known_block_membership_assignment_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "Gate5_filled_field_slot_count": 10,
            "Gate5_total_field_slot_count": 18,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "begin P3 maximal-component exhaustion over the 74012-component "
            "unified lower-bound quotient; quotient assignment completeness "
            "does not imply maximality"
        ),
    }


def safe_write(raw: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{OUTPUT.name}.", dir=OUTPUT.parent
    )
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
