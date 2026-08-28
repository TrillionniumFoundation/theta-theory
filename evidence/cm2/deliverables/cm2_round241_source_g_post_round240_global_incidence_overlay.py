#!/usr/bin/env python3
"""Apply the Round240 delta to the full 53,968-occurrence frontier."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round241_source_g_post_round240_global_incidence_overlay_certificate.json"
)
SCHEMA = "cm2.round241.source-g-post-round240-global-incidence-overlay.v1"
PINS = {
    "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json":
        "88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73",
    "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json":
        "65285cd08662006015c388f8dbf1eb077ca2434d80b715dbdc99c332de629359",
}


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def read_pinned(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= 200_000_000,
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


def safe_write(data: bytes) -> None:
    descriptor, name = tempfile.mkstemp(
        prefix=".round241.",
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
    finally:
        if temporary.exists():
            temporary.unlink()


def build() -> dict[str, Any]:
    round230 = load_result(
        "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json"
    )
    round240 = load_result(
        "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json"
    )
    source_rows = round230[
        "formal_post_Round230_occurrence_known_block_frontier_ledger"
    ]["rows"]
    delta_rows = round240[
        "formal_occurrence_known_block_incidence_delta_ledger"
    ]["rows"]
    deltas = {
        row["local_occurrence_row_id"]: row for row in delta_rows
    }
    need(
        len(source_rows) == 53_968
        and len(deltas) == 12
        and round240["census"][
            "post_Round240_occurrences_with_known_block_incidence"
        ] == 35_908,
        "input census",
    )

    post_rows: list[dict[str, Any]] = []
    changed_ids: list[str] = []
    for source in source_rows:
        occurrence_id = source["local_occurrence_row_id"]
        delta = deltas.get(occurrence_id)
        base = {
            key: value
            for key, value in source.items()
            if key not in {"post_frontier_row_id", "row_sha256"}
        }
        if delta is not None:
            need(
                source["known_block_incidence_attachment_credit"] == 0
                and source["Round225_known_connectivity_block_id"] is None
                and source["incidence_source"] == "NONE"
                and source["official_key_id"] == delta["official_key_id"]
                and source["official_key_ordinal"]
                == delta["official_key_ordinal"],
                f"strict delta precondition:{occurrence_id}",
            )
            base["Round225_known_connectivity_block_id"] = delta[
                "Round225_known_connectivity_block_id"
            ]
            base["known_block_incidence_attachment_credit"] = 1
            base["incidence_source"] = (
                "ROUND240_STRICT_SHEET_INTERFACE_CORRIDOR"
            )
            changed_ids.append(occurrence_id)
        row_id = (
            "round241-post-known-block-frontier:"
            + digest([
                occurrence_id,
                base["Round225_known_connectivity_block_id"],
                base["incidence_source"],
                base["known_block_incidence_attachment_credit"],
            ])
        )
        post_rows.append(closed({
            "post_frontier_row_id": row_id,
            **base,
        }))
    post_rows.sort(key=lambda row: row["post_frontier_row_id"])
    need(
        sorted(changed_ids) == sorted(deltas)
        and len(post_rows) == len({
            row["local_occurrence_row_id"] for row in post_rows
        }) == 53_968,
        "exact overlay",
    )

    key_metadata = {
        row["official_key_ordinal"]: {
            "official_key_id": row["official_key_id"],
            "official_key_row": row["official_key_row"],
        }
        for row in round230[
            "formal_post_Round230_key_frontier_ledger"
        ]["rows"]
    }
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in post_rows:
        grouped[row["official_key_ordinal"]].append(row)
    delta_by_key = Counter(
        row["official_key_ordinal"] for row in delta_rows
    )
    key_rows: list[dict[str, Any]] = []
    for ordinal in sorted(grouped):
        occurrences = grouped[ordinal]
        metadata = key_metadata[ordinal]
        attached = sum(
            row["known_block_incidence_attachment_credit"]
            for row in occurrences
        )
        total = len(occurrences)
        need(
            all(
                row["official_key_id"] == metadata["official_key_id"]
                for row in occurrences
            ),
            f"key identity:{ordinal}",
        )
        key_rows.append(closed({
            "key_frontier_row_id":
                "round241-key-frontier:"
                + digest([
                    ordinal,
                    metadata["official_key_id"],
                    attached,
                    total,
                ]),
            "official_key_ordinal": ordinal,
            "official_key_id": metadata["official_key_id"],
            "official_key_row": metadata["official_key_row"],
            "local_occurrence_count": total,
            "occurrences_with_known_block_incidence": attached,
            "occurrences_without_known_block_incidence": total - attached,
            "new_Round240_known_block_incidences":
                delta_by_key[ordinal],
            "cumulative_known_block_incidences": attached,
            "maximal_physical_component_assignment_count": 0,
            "global_exact_key_fibre_exhausted": False,
            "global_exact_key_disposition_credit": 0,
        }))
    key_rows.sort(key=lambda row: row["key_frontier_row_id"])

    attached_count = sum(
        row["known_block_incidence_attachment_credit"]
        for row in post_rows
    )
    gauge_histogram = Counter(
        row["local_occurrence_gauge"] for row in post_rows
    )
    source_histogram = Counter(
        row["incidence_source"] for row in post_rows
        if row["known_block_incidence_attachment_credit"] == 1
    )
    need(
        len(key_rows) == 116
        and attached_count == 35_908
        and sum(
            row["occurrences_without_known_block_incidence"]
            for row in key_rows
        ) == 18_060
        and sum(
            row["new_Round240_known_block_incidences"]
            for row in key_rows
        ) == 12,
        "post overlay census",
    )
    return {
        "status": (
            "CERTIFIED_POST_ROUND240_GLOBAL_OCCURRENCE_FRONTIER__"
            "35908_OF_53968_KNOWN_BLOCK_INCIDENCES__18060_UNATTACHED__"
            "ZERO_COMPONENT_MAXIMAL_OR_GLOBAL_FIBRE_PROMOTION"
        ),
        "census": {
            "local_occurrence_count": len(post_rows),
            "observed_exact_key_count": len(key_rows),
            "pre_Round240_occurrences_with_known_block_incidence": 35_896,
            "Round240_new_occurrence_known_block_incidences": 12,
            "post_Round240_occurrences_with_known_block_incidence":
                attached_count,
            "post_Round240_occurrences_without_known_block_incidence":
                len(post_rows) - attached_count,
            "keys_touched_by_Round240": len(delta_by_key),
            "global_exact_key_fibre_exhausted_count": 0,
            "maximal_physical_component_assignment_count": 0,
            "local_occurrence_gauge_histogram":
                dict(sorted(gauge_histogram.items())),
            "attached_incidence_source_histogram":
                dict(sorted(source_histogram.items())),
        },
        "formal_post_Round241_occurrence_known_block_frontier_ledger":
            ledger(post_rows, "post_frontier_row_id"),
        "formal_post_Round241_key_frontier_ledger":
            ledger(key_rows, "key_frontier_row_id"),
        "Round240_changed_local_occurrence_ids_sha256":
            digest(sorted(changed_ids)),
        "scope_contract": {
            "Round230_frontier_rows_preserved_except_exact_Round240_delta":
                True,
            "all_53968_occurrences_rebuilt": True,
            "all_116_observed_keys_reaggregated": True,
            "known_block_incidence_is_not_component_membership": True,
            "no_key_fibre_is_globally_exhausted": True,
        },
        "strict_nonpromotion": {
            "known_block_membership_assignment_credit": 0,
            "physical_component_credit": 0,
            "maximal_physical_component_credit": 0,
            "global_exact_key_fibre_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "materialize event-bearing retained/common-refinement strata "
            "for the 8500 Round239 interfaces lacking any Round225 block "
            "reference"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = build()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    data = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(data)
    print(result["status"])
    print(json.dumps(result["census"], sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"certificate_sha256={hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
