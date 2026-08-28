#!/usr/bin/env python3
"""Independently rebuild and verify the Round241 global overlay."""

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
    / "cm2_round241_source_g_post_round240_global_incidence_overlay_verification.json"
)
PINS = {
    "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json":
        "88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73",
    "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json":
        "65285cd08662006015c388f8dbf1eb077ca2434d80b715dbdc99c332de629359",
    "cm2_round241_source_g_post_round240_global_incidence_overlay.py":
        "290e3b7be9d0aee9713e77f140c25b7cf7a5b1571254e7b452341d41fbff9d4c",
    "cm2_round241_source_g_post_round240_global_incidence_overlay_certificate.json":
        "7fd00a654965d223cc9ae88de4f0456f9c743dbfa38b06d22879519a5ad79bcc",
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
        prefix=".round241-verifier.",
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


def verify() -> dict[str, Any]:
    for name in PINS:
        read_pinned(name)
    round230 = load_result(
        "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json"
    )
    round240 = load_result(
        "cm2_round240_source_g_remote_sheet_interface_corridor_incidence_certificate.json"
    )
    candidate = load_result(
        "cm2_round241_source_g_post_round240_global_incidence_overlay_certificate.json"
    )
    deltas = {
        row["local_occurrence_row_id"]: row
        for row in round240[
            "formal_occurrence_known_block_incidence_delta_ledger"
        ]["rows"]
    }
    need(len(deltas) == 12, "delta count")

    rebuilt: list[dict[str, Any]] = []
    changed: list[str] = []
    for source in round230[
        "formal_post_Round230_occurrence_known_block_frontier_ledger"
    ]["rows"]:
        occurrence_id = source["local_occurrence_row_id"]
        base = {
            key: value
            for key, value in source.items()
            if key not in {"post_frontier_row_id", "row_sha256"}
        }
        delta = deltas.get(occurrence_id)
        if delta is not None:
            need(
                base["known_block_incidence_attachment_credit"] == 0
                and base["Round225_known_connectivity_block_id"] is None
                and base["incidence_source"] == "NONE"
                and base["official_key_id"] == delta["official_key_id"]
                and base["official_key_ordinal"]
                == delta["official_key_ordinal"],
                f"delta precondition:{occurrence_id}",
            )
            base["Round225_known_connectivity_block_id"] = delta[
                "Round225_known_connectivity_block_id"
            ]
            base["known_block_incidence_attachment_credit"] = 1
            base["incidence_source"] = (
                "ROUND240_STRICT_SHEET_INTERFACE_CORRIDOR"
            )
            changed.append(occurrence_id)
        rebuilt.append(closed({
            "post_frontier_row_id":
                "round241-post-known-block-frontier:"
                + digest([
                    occurrence_id,
                    base["Round225_known_connectivity_block_id"],
                    base["incidence_source"],
                    base["known_block_incidence_attachment_credit"],
                ]),
            **base,
        }))
    rebuilt.sort(key=lambda row: row["post_frontier_row_id"])
    need(
        len(rebuilt) == 53_968
        and sorted(changed) == sorted(deltas),
        "rebuilt occurrence frontier",
    )

    metadata = {
        row["official_key_ordinal"]: (
            row["official_key_id"],
            row["official_key_row"],
        )
        for row in round230[
            "formal_post_Round230_key_frontier_ledger"
        ]["rows"]
    }
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rebuilt:
        grouped[row["official_key_ordinal"]].append(row)
    delta_by_key = Counter(
        row["official_key_ordinal"] for row in deltas.values()
    )
    key_rows: list[dict[str, Any]] = []
    for ordinal, occurrences in sorted(grouped.items()):
        key_id, key_row = metadata[ordinal]
        attached = sum(
            row["known_block_incidence_attachment_credit"]
            for row in occurrences
        )
        total = len(occurrences)
        key_rows.append(closed({
            "key_frontier_row_id":
                "round241-key-frontier:"
                + digest([ordinal, key_id, attached, total]),
            "official_key_ordinal": ordinal,
            "official_key_id": key_id,
            "official_key_row": key_row,
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

    attached = sum(
        row["known_block_incidence_attachment_credit"] for row in rebuilt
    )
    gauge_histogram = Counter(
        row["local_occurrence_gauge"] for row in rebuilt
    )
    source_histogram = Counter(
        row["incidence_source"] for row in rebuilt
        if row["known_block_incidence_attachment_credit"] == 1
    )
    expected_census = {
        "local_occurrence_count": 53_968,
        "observed_exact_key_count": 116,
        "pre_Round240_occurrences_with_known_block_incidence": 35_896,
        "Round240_new_occurrence_known_block_incidences": 12,
        "post_Round240_occurrences_with_known_block_incidence": 35_908,
        "post_Round240_occurrences_without_known_block_incidence": 18_060,
        "keys_touched_by_Round240": len(delta_by_key),
        "global_exact_key_fibre_exhausted_count": 0,
        "maximal_physical_component_assignment_count": 0,
        "local_occurrence_gauge_histogram":
            dict(sorted(gauge_histogram.items())),
        "attached_incidence_source_histogram":
            dict(sorted(source_histogram.items())),
    }
    need(
        attached == 35_908
        and candidate[
            "formal_post_Round241_occurrence_known_block_frontier_ledger"
        ] == ledger(rebuilt, "post_frontier_row_id")
        and candidate[
            "formal_post_Round241_key_frontier_ledger"
        ] == ledger(key_rows, "key_frontier_row_id")
        and candidate["census"] == expected_census
        and candidate["Round240_changed_local_occurrence_ids_sha256"]
        == digest(sorted(changed))
        and candidate["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "candidate overlay",
    )
    return {
        "status": "PASS_INDEPENDENT_ROUND241",
        "candidate_sha256": PINS[
            "cm2_round241_source_g_post_round240_global_incidence_overlay_certificate.json"
        ],
        "candidate_result_sha256": digest(candidate),
        "producer_imported_or_executed": False,
        "independently_rebuilt_occurrence_count": len(rebuilt),
        "independently_rebuilt_key_count": len(key_rows),
        "independently_applied_Round240_delta_count": len(changed),
        "post_Round240_occurrences_with_known_block_incidence": attached,
        "post_Round240_occurrences_without_known_block_incidence":
            len(rebuilt) - attached,
        "strict_nonpromotion_reconfirmed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = verify()
    document = {
        "schema": (
            "cm2.round241.source-g-post-round240-global-incidence-"
            "overlay.verification.v1"
        ),
        "result": result,
        "result_sha256": digest(result),
    }
    data = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(data)
    print(result["status"])
    print(json.dumps(result, sort_keys=True))
    print(f"verification_result_sha256={document['result_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
