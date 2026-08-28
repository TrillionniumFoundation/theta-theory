#!/usr/bin/env python3
"""Outcome-blind depth 7--10 probe of the frozen Round219 exact frontier.

This is a read-only feasibility/cost probe.  It imports the frozen Round219
producer solely to reuse the pinned interval predicate, continues only the
terminal rows that Round219 left UNRESOLVED, and emits no formal credit.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import sys
import time
from typing import Any

from flint import ctx

import cm2_round219_source_g_partial_face_common_refinement_glue as r219


HERE = Path(__file__).resolve().parent
R219_SOURCE = (
    "cm2_round219_source_g_partial_face_common_refinement_glue.py"
)
R219_CERTIFICATE = (
    "cm2_round219_source_g_partial_face_common_refinement_glue"
    "_certificate.json"
)
R219_SOURCE_SHA256 = (
    "8b670ffbcabd5a9796fb67580cbb9e3318b8eb2ee1cd65c5e71f7f1f360b3019"
)
R219_CERTIFICATE_SHA256 = (
    "8341a8b08a0abd5c7a16c61b918b7b47db4d05c3c4e6fae8615892e3aafaf096"
)
R219_RESULT_SHA256 = (
    "f8d46a9a220b6b7e0e6f86430ad6d537d5358cd610f064417ab3e8b4c125744e"
)
START_DEPTH = 6
FINAL_DEPTH = 10


class ProbeError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ProbeError(label)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    require(
        Path(r219.__file__).resolve() == (HERE / R219_SOURCE).resolve(),
        "Round219 module identity",
    )
    require(
        sha256(HERE / R219_SOURCE) == R219_SOURCE_SHA256,
        "Round219 source pin",
    )
    raw = (HERE / R219_CERTIFICATE).read_bytes()
    require(
        hashlib.sha256(raw).hexdigest() == R219_CERTIFICATE_SHA256,
        "Round219 certificate pin",
    )
    envelope = json.loads(raw)
    require(
        envelope["result_sha256"] == R219_RESULT_SHA256
        and r219.digest(envelope["result"]) == R219_RESULT_SHA256,
        "Round219 result closure",
    )
    result = envelope["result"]
    terminal_ledger = result["formal_terminal_subface_ledger"]
    terminal_rows = terminal_ledger["rows"]
    require(
        terminal_ledger["row_count"] == len(terminal_rows)
        and terminal_ledger["rows_sha256"] == r219.digest(terminal_rows),
        "Round219 terminal ledger closure",
    )
    unresolved_rows = [
        row for row in terminal_rows
        if row["classification"] == "UNRESOLVED"
    ]
    require(
        unresolved_rows
        and all(row["depth"] == START_DEPTH for row in unresolved_rows),
        "Round219 depth-six unresolved boundary",
    )

    (
        _result217,
        exact_frontier,
        _partial_frontier,
        _evaluators,
        _hashes,
    ) = r219.load_boundary()
    ctx.prec = 256
    frontier_by_id = {
        row["frontier_row_id"]: row for row in exact_frontier
    }
    require(
        all(
            row["Round217_frontier_row_id"] in frontier_by_id
            for row in unresolved_rows
        ),
        "unresolved frontier identity",
    )

    # Each active item is (contact ID, Round217 frontier, path, interval).
    active: list[
        tuple[str, dict[str, Any], str, tuple[Q, Q]]
    ] = [
        (
            row["contact_row_id"],
            frontier_by_id[row["Round217_frontier_row_id"]],
            row["dyadic_path"],
            tuple(Q(value) for value in row["transverse_interval"]),
        )
        for row in unresolved_rows
    ]
    starting_by_contact = Counter(item[0] for item in active)
    require(
        len(starting_by_contact)
        == result["formal_exact_contact_scope"][
            "remaining_incomplete_contact_count"
        ],
        "Round219 unresolved contact boundary",
    )
    still_unresolved_by_contact = dict(starting_by_contact)
    cumulative_complete = result["formal_exact_contact_scope"][
        "cumulative_complete_contact_count"
    ]
    per_depth: list[dict[str, Any]] = []

    for depth in range(START_DEPTH + 1, FINAL_DEPTH + 1):
        started = time.perf_counter()
        following: list[
            tuple[str, dict[str, Any], str, tuple[Q, Q]]
        ] = []
        classifications = Counter()
        resolved_parent_children: dict[str, int] = defaultdict(int)
        for contact_id, frontier, path, (lower, upper) in active:
            midpoint = (lower + upper) / 2
            for suffix, interval in (
                ("L", (lower, midpoint)),
                ("R", (midpoint, upper)),
            ):
                proof = r219.interval_proof(
                    frontier["source_chart"],
                    frontier["target_lift"],
                    frontier["active_factor"],
                    frontier["fixed_axis"],
                    Q(frontier["shared_coordinate"]),
                    "t",
                    tuple(Q(value) for value in frontier["t_interval"]),
                    interval,
                )
                classification = proof["classification"]
                classifications[classification] += 1
                if classification == "UNRESOLVED":
                    following.append(
                        (contact_id, frontier, path + suffix, interval)
                    )
                else:
                    resolved_parent_children[contact_id] += 1

        remaining_by_contact = Counter(item[0] for item in following)
        newly_complete_contacts = sum(
            contact_id not in remaining_by_contact
            for contact_id in still_unresolved_by_contact
        )
        cumulative_complete += newly_complete_contacts
        still_unresolved_by_contact = dict(remaining_by_contact)
        elapsed = time.perf_counter() - started
        row = {
            "depth": depth,
            "strict_child_interval_evaluations": 2 * len(active),
            "TRACE_children": classifications["TRACE"],
            "ABSENT_children": classifications["ABSENT"],
            "UNRESOLVED_children": classifications["UNRESOLVED"],
            "remaining_incomplete_contact_count":
                len(remaining_by_contact),
            "newly_complete_contact_count": newly_complete_contacts,
            "cumulative_complete_contact_count": cumulative_complete,
            "elapsed_seconds": round(elapsed, 6),
        }
        per_depth.append(row)
        print(json.dumps(row, sort_keys=True), file=sys.stderr, flush=True)
        active = following

    output = {
        "status": "OUTCOME_BLIND_READ_ONLY_PROBE_NO_FORMAL_CREDIT",
        "Round219_source_sha256": R219_SOURCE_SHA256,
        "Round219_certificate_sha256": R219_CERTIFICATE_SHA256,
        "Round219_result_sha256": R219_RESULT_SHA256,
        "Round219_producer_imported_for_predicate_reuse": True,
        "effective_Arb_precision_bits": ctx.prec,
        "start_depth": START_DEPTH,
        "final_depth": FINAL_DEPTH,
        "starting_UNRESOLVED_terminal_subface_count":
            len(unresolved_rows),
        "starting_incomplete_contact_count": len(starting_by_contact),
        "starting_unresolved_subfaces_per_contact_histogram": dict(
            sorted(Counter(starting_by_contact.values()).items())
        ),
        "per_depth": per_depth,
        "final_UNRESOLVED_terminal_subface_count": len(active),
        "final_incomplete_contact_count":
            len({item[0] for item in active}),
        "formal_credit_granted": False,
        "component_or_global_credit_granted": False,
    }
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
