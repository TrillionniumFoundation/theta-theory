#!/usr/bin/env python3
"""Adaptive exact-subface common-refinement materialization for source-G.

Round219 consumes exactly the Round217 fail-closed exact and partial face
frontiers.  For each of the 7,484 exact p/s contacts it constructs a
deterministic depth-six dyadic transverse partition.  Every child subface is
classified only from full-child endpoint C0 enclosures and a strict derivative
on the whole child.  Certified TRACE children receive canonical restricted
zero-curve, two-sided incidence, and glue IDs; ABSENT children receive local
zero-absence credit; unresolved children remain fail-closed.

A contact is complete only when TRACE+ABSENT owned children partition its
entire transverse interval with no gap, overlap, or unresolved child.  Local
subface/contact credits are not physical-component, whole-origin/tube,
global-fibre, or exact-key disposition credits.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable

from flint import ctx

import cm2_round186_source_g_factor_face_probe as r186
import cm2_round209_source_g_outgoing_half_open_owner_probe as r209


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round219_source_g_partial_face_common_refinement_glue"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = "cm2.round219.source-g-partial-face-common-refinement-glue.v1"
STATUS = (
    "CERTIFIED_ADAPTIVE_EXACT_SUBFACE_TRACE_ABSENCE_AND_GLUE_PREFIX__"
    "ENDPOINT_TO_INTERIOR_AND_PHYSICAL_COMPONENT_CLOSURE_INCOMPLETE"
)
MAX_INPUT_BYTES = 300 * 1024 * 1024
MAX_DEPTH = 6

R217_SOURCE = (
    "cm2_round217_source_g_internal_face_trace_glue_materialization.py"
)
R217_CERTIFICATE = (
    "cm2_round217_source_g_internal_face_trace_glue_materialization"
    "_certificate.json"
)
R217_SOURCE_SHA256 = (
    "687fd48134e204a99c807e1fd18954cef7633879396db5f4d291ece1568dfa66"
)
R217_CERTIFICATE_SHA256 = (
    "1ccf9b4bf65bb4f45603594ea19f47e3b2103ea682bebfff0b023234308938fd"
)
R217_RESULT_SHA256 = (
    "fb4519a43f76cbc765e24b3cb0a0e25267d9664091e22139913f3899fd1e2286"
)
R209_SOURCE = "cm2_round209_source_g_outgoing_half_open_owner_probe.py"
R209_SOURCE_SHA256 = (
    "dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f"
)
R186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
R186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)

EXPECTED_ROUND217_DIRECT_ACCEPTED = 448
EXPECTED_EXACT_FRONTIER = 7_484
EXPECTED_EXACT_P_S_TOTAL = 7_932
EXPECTED_TRACE_SUBFACES = 22_960
EXPECTED_ABSENT_SUBFACES = 22_096
EXPECTED_UNRESOLVED_SUBFACES = 7_236
EXPECTED_TERMINAL_SUBFACES = 52_292
EXPECTED_COMPLETE_CONTACTS = 468
EXPECTED_REMAINING_CONTACTS = 7_016
EXPECTED_CUMULATIVE_COMPLETE = 916
EXPECTED_PARTIAL_FRONTIER = 264
EXPECTED_PARTIAL_ABSENT = 28
EXPECTED_PARTIAL_REMAINING = 236
EXPECTED_SOURCE_G_KEYS = 224_580
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


class Round219Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round219Error(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def encoded_chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode()


def canonical_bytes(value: Any) -> bytes:
    return b"".join(encoded_chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in encoded_chunks(value):
        state.update(chunk)
    return state.hexdigest()


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(payload)
    value["row_sha256"] = digest(value)
    return value


def row_id(kind: str, identity: dict[str, Any]) -> str:
    return f"round219-{kind}:{digest(identity)}"


def histogram(values: Iterable[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


def ledger(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def regular_bytes(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(before.st_nlink == 1, f"hardlink:{path.name}")
    require(0 < before.st_size <= maximum, f"size:{path.name}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        require(
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
            f"stable-open:{path.name}",
        )
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            require(total <= maximum, f"bounded-read:{path.name}")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        require(
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
            f"stable-read:{path.name}",
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def pinned(path: Path, expected: str, maximum: int) -> bytes:
    raw = regular_bytes(path, maximum)
    require(hashlib.sha256(raw).hexdigest() == expected,
            f"SHA256:{path.name}")
    return raw


def validate_row_ledger(
    ledger_value: dict[str, Any],
    id_key: str,
) -> list[dict[str, Any]]:
    rows = ledger_value["rows"]
    require(
        ledger_value["row_count"] == len(rows)
        and ledger_value["rows_sha256"] == digest(rows)
        and ledger_value["row_ids_sha256"]
        == digest([row[id_key] for row in rows])
        and ledger_value["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows]),
        f"input ledger closure:{id_key}",
    )
    for row in rows:
        payload = dict(row)
        row_hash = payload.pop("row_sha256")
        require(digest(payload) == row_hash, f"input row closure:{id_key}")
    return rows


def load_boundary() -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, tuple[str, str, str]],
    dict[str, str],
]:
    require(
        Path(r209.__file__).resolve() == (HERE / R209_SOURCE).resolve()
        and Path(r186.__file__).resolve() == (HERE / R186_SOURCE).resolve(),
        "pinned module identity",
    )
    pinned(HERE / R217_SOURCE, R217_SOURCE_SHA256, 5_000_000)
    raw217 = pinned(
        HERE / R217_CERTIFICATE,
        R217_CERTIFICATE_SHA256,
        50_000_000,
    )
    pinned(HERE / R209_SOURCE, R209_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R186_SOURCE, R186_SOURCE_SHA256, 5_000_000)
    certificate = json.loads(raw217)
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["result_sha256"] == R217_RESULT_SHA256
        and digest(certificate["result"]) == R217_RESULT_SHA256,
        "Round217 result closure",
    )
    result217 = certificate["result"]
    traces217 = validate_row_ledger(
        result217["formal_internal_face_zero_trace_ledger"],
        "trace_row_id",
    )
    incidences217 = validate_row_ledger(
        result217["formal_internal_face_incidence_ledger"],
        "incidence_row_id",
    )
    glues217 = validate_row_ledger(
        result217["formal_exact_common_refinement_glue_ledger"],
        "glue_row_id",
    )
    del traces217, incidences217
    exact_frontier = result217[
        "exact_face_endpoint_to_interior_frontier"
    ]["rows"]
    partial_frontier = result217["partial_face_frontier"]["rows"]
    require(
        len(glues217) == EXPECTED_ROUND217_DIRECT_ACCEPTED
        and len(exact_frontier) == EXPECTED_EXACT_FRONTIER
        and len(partial_frontier) == EXPECTED_PARTIAL_FRONTIER
        and digest(exact_frontier)
        == result217["exact_face_endpoint_to_interior_frontier"][
            "rows_sha256"
        ]
        and digest(partial_frontier)
        == result217["partial_face_frontier"]["rows_sha256"],
        "exact Round217 frontier boundary",
    )
    for rows in (exact_frontier, partial_frontier):
        for row in rows:
            payload = dict(row)
            row_hash = payload.pop("row_sha256")
            require(digest(payload) == row_hash, "Round217 frontier row closure")

    accepted_pairs = {
        (
            row["negative_side_leaf_row_id"],
            row["positive_side_leaf_row_id"],
        )
        for row in glues217
    }
    frontier_pairs = {
        (
            row["negative_leaf_row_id"],
            row["positive_leaf_row_id"],
        )
        for row in exact_frontier
    }
    require(
        len(accepted_pairs) == EXPECTED_ROUND217_DIRECT_ACCEPTED
        and len(frontier_pairs) == EXPECTED_EXACT_FRONTIER
        and accepted_pairs.isdisjoint(frontier_pairs)
        and len(accepted_pairs | frontier_pairs) == EXPECTED_EXACT_P_S_TOTAL,
        "Round217 accepted/frontier exact disjoint union",
    )

    _r173, result208, hashes209 = r209.validate_inputs()
    leaves, regions, _faces, _u2 = r209.validate_round195_geometry(result208)
    sheets, _curves, _endpoints, _audit = r209.build_lineages(leaves, regions)
    region_by_id = {row["region_row_id"]: row for row in regions}
    sheet_by_leaf = {row["leaf_row_id"]: row for row in sheets}
    evaluators: dict[str, tuple[str, str, str]] = {}
    for leaf_id, sheet in sheet_by_leaf.items():
        signature = region_by_id[
            sheet["owner_region_row_id"]
        ]["local_return_signature"]
        evaluators[leaf_id] = (
            signature["source_chart"],
            signature["target_lift"],
            sheet["active_factor"],
        )
    for row in exact_frontier:
        require(
            evaluators[row["negative_leaf_row_id"]]
            == (
                row["source_chart"],
                row["target_lift"],
                row["active_factor"],
            )
            == evaluators[row["positive_leaf_row_id"]],
            "Round217 exact frontier evaluator identity",
        )
    hashes = {
        "Round217_source_sha256": R217_SOURCE_SHA256,
        "Round217_certificate_sha256": R217_CERTIFICATE_SHA256,
        "Round217_result_sha256": R217_RESULT_SHA256,
        "Round209_probe_source_sha256": R209_SOURCE_SHA256,
        "Round186_factor_evaluator_source_sha256": R186_SOURCE_SHA256,
        "Round208_certificate_sha256":
            hashes209["Round208_certificate_sha256"],
        "Round208_result_sha256": hashes209["Round208_result_sha256"],
    }
    return (
        result217,
        exact_frontier,
        partial_frontier,
        evaluators,
        hashes,
    )


def interval_proof(
    chart: str,
    target: str,
    active: str,
    fixed_axis: str,
    fixed_coordinate: Q,
    graph_axis: str,
    graph_interval: tuple[Q, Q],
    transverse_interval: tuple[Q, Q],
) -> dict[str, Any]:
    atlas_box = r186.r179.r174.atlas.AtlasBox
    arb_sign = r186.r179.arb_sign
    g0, g1 = graph_interval
    u0, u1 = transverse_interval

    if fixed_axis == "p" and graph_axis == "t":
        def make(a: Q, b: Q) -> Any:
            return atlas_box(
                a, b, fixed_coordinate, fixed_coordinate,
                u0, u1, 0, "round219"
            )
        derivative_index = 0
    elif fixed_axis == "s" and graph_axis == "t":
        def make(a: Q, b: Q) -> Any:
            return atlas_box(
                a, b, u0, u1,
                fixed_coordinate, fixed_coordinate, 0, "round219"
            )
        derivative_index = 0
    elif fixed_axis == "t" and graph_axis == "p":
        def make(a: Q, b: Q) -> Any:
            return atlas_box(
                fixed_coordinate, fixed_coordinate, a, b,
                u0, u1, 0, "round219"
            )
        derivative_index = 1
    elif fixed_axis == "t" and graph_axis == "s":
        def make(a: Q, b: Q) -> Any:
            return atlas_box(
                fixed_coordinate, fixed_coordinate, u0, u1,
                a, b, 0, "round219"
            )
        derivative_index = 2
    else:
        raise Round219Error("unsupported restricted graph axes")

    lower_box = make(g0, g0)
    upper_box = make(g1, g1)
    full_box = make(g0, g1)
    lower = r186.factor_geometry(chart, target, lower_box)[active]
    upper = r186.factor_geometry(chart, target, upper_box)[active]
    full = r186.factor_geometry(chart, target, full_box)[active]
    lower_centered = r186.centered_value(
        chart, target, lower_box, active
    )
    upper_centered = r186.centered_value(
        chart, target, upper_box, active
    )
    direct_signs = (
        arb_sign(lower[0]),
        arb_sign(upper[0]),
        arb_sign(full[1][derivative_index]),
    )
    centered_signs = (
        arb_sign(lower_centered),
        arb_sign(upper_centered),
    )
    selected_signs = (
        (
            direct_signs[0]
            if direct_signs[0] in STRICT_SIGNS
            else centered_signs[0]
        ),
        (
            direct_signs[1]
            if direct_signs[1] in STRICT_SIGNS
            else centered_signs[1]
        ),
        direct_signs[2],
    )
    if (
        selected_signs[2] in STRICT_SIGNS
        and selected_signs[0] in STRICT_SIGNS
        and selected_signs[1] in STRICT_SIGNS
    ):
        classification = (
            "TRACE" if selected_signs[0] != selected_signs[1] else "ABSENT"
        )
    else:
        classification = "UNRESOLVED"
    witness = {
        "direct_signs": list(direct_signs),
        "centered_endpoint_signs": list(centered_signs),
        "selected_signs": list(selected_signs),
        "direct_lower_C0": str(lower[0]),
        "centered_lower_C0": str(lower_centered),
        "direct_upper_C0": str(upper[0]),
        "centered_upper_C0": str(upper_centered),
        "full_graph_axis_derivative": str(
            full[1][derivative_index]
        ),
    }
    return {
        "classification": classification,
        "selected_lower_upper_derivative_signs": list(selected_signs),
        "interval_witness_sha256": digest(witness),
        "proof_rule": (
            "FULL_CHILD_ENDPOINT_C0_AND_FULL_CHILD_STRICT_GRAPH_AXIS_"
            "DERIVATIVE"
        ),
    }


def segment_row(
    contact_id: str,
    frontier: dict[str, Any],
    path: str,
    depth: int,
    interval: tuple[Q, Q],
    proof: dict[str, Any],
) -> dict[str, Any]:
    axis = frontier["fixed_axis"]
    classification = proof["classification"]
    identity = {
        "contact_row_id": contact_id,
        "dyadic_path": path,
        "depth": depth,
        "transverse_interval": [str(value) for value in interval],
    }
    segment_id = row_id("terminal-subface", identity)
    trace_id = (
        row_id("restricted-zero-curve", {"terminal_subface_row_id": segment_id})
        if classification == "TRACE"
        else None
    )
    negative_incidence = (
        row_id("negative-side-incidence", {
            "trace_row_id": trace_id,
            "leaf_row_id": frontier["negative_leaf_row_id"],
            "orientation": "POSITIVE_" + axis.upper(),
        })
        if trace_id else None
    )
    positive_incidence = (
        row_id("positive-side-incidence", {
            "trace_row_id": trace_id,
            "leaf_row_id": frontier["positive_leaf_row_id"],
            "orientation": "NEGATIVE_" + axis.upper(),
        })
        if trace_id else None
    )
    glue_id = (
        row_id("restricted-common-refinement-glue", {
            "trace_row_id": trace_id,
            "negative_incidence_row_id": negative_incidence,
            "positive_incidence_row_id": positive_incidence,
        })
        if trace_id else None
    )
    return closed_row({
        "terminal_subface_row_id": segment_id,
        **identity,
        "Round217_frontier_row_id": frontier["frontier_row_id"],
        "Round217_frontier_row_sha256": frontier["row_sha256"],
        "fixed_axis": axis,
        "shared_coordinate": frontier["shared_coordinate"],
        "graph_axis": "t",
        "graph_interval": copy.deepcopy(frontier["t_interval"]),
        "half_open_partition_owner_rule":
            "LEFT_CLOSED_RIGHT_OPEN_EXCEPT_FINAL_RIGHT_CLOSED",
        "classification": classification,
        **proof,
        "restricted_zero_curve_row_id": trace_id,
        "negative_side_incidence_row_id": negative_incidence,
        "negative_side_leaf_row_id": frontier["negative_leaf_row_id"],
        "negative_side_outward_orientation":
            "POSITIVE_" + axis.upper() if trace_id else None,
        "positive_side_incidence_row_id": positive_incidence,
        "positive_side_leaf_row_id": frontier["positive_leaf_row_id"],
        "positive_side_outward_orientation":
            "NEGATIVE_" + axis.upper() if trace_id else None,
        "exact_subface_common_refinement_glue_row_id": glue_id,
        "exact_restricted_evaluator_identity": (
            True if trace_id else None
        ),
        "joined_from_box_touch_or_signature_hash_alone": False,
        "formal_restricted_zero_curve_credit":
            int(classification == "TRACE"),
        "formal_local_subface_incidence_credit":
            2 * int(classification == "TRACE"),
        "formal_local_subface_glue_credit":
            int(classification == "TRACE"),
        "formal_local_zero_absence_credit":
            int(classification == "ABSENT"),
        "formal_component_deduplication_credit": 0,
        "whole_leaf_credit": 0,
        "whole_origin_credit": 0,
        "whole_original_tube_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def exact_contact_partition(
    frontier: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    contact_identity = {
        "Round217_frontier_row_id": frontier["frontier_row_id"],
        "Round217_frontier_row_sha256": frontier["row_sha256"],
    }
    contact_id = row_id("exact-contact", contact_identity)
    chart = frontier["source_chart"]
    target = frontier["target_lift"]
    active_factor = frontier["active_factor"]
    fixed_axis = frontier["fixed_axis"]
    coordinate = Q(frontier["shared_coordinate"])
    graph_interval = tuple(Q(value) for value in frontier["t_interval"])
    original = tuple(
        Q(value) for value in frontier["transverse_interval"]
    )

    active_segments = [("", 0, original)]
    terminal: list[tuple[str, int, tuple[Q, Q], dict[str, Any]]] = []
    for depth in range(1, MAX_DEPTH + 1):
        following: list[tuple[str, int, tuple[Q, Q]]] = []
        for path, _old_depth, (lower, upper) in active_segments:
            midpoint = (lower + upper) / 2
            for suffix, interval in (
                ("L", (lower, midpoint)),
                ("R", (midpoint, upper)),
            ):
                proof = interval_proof(
                    chart,
                    target,
                    active_factor,
                    fixed_axis,
                    coordinate,
                    "t",
                    graph_interval,
                    interval,
                )
                child_path = path + suffix
                if proof["classification"] == "UNRESOLVED":
                    following.append((child_path, depth, interval))
                else:
                    terminal.append((child_path, depth, interval, proof))
        active_segments = following
    for path, depth, interval in active_segments:
        proof = interval_proof(
            chart,
            target,
            active_factor,
            fixed_axis,
            coordinate,
            "t",
            graph_interval,
            interval,
        )
        require(proof["classification"] == "UNRESOLVED",
                "depth-six residual remains unresolved")
        terminal.append((path, depth, interval, proof))

    terminal.sort(key=lambda item: (item[2][0], item[2][1], item[0]))
    require(
        terminal[0][2][0] == original[0]
        and terminal[-1][2][1] == original[1]
        and all(
            terminal[index][2][1] == terminal[index + 1][2][0]
            for index in range(len(terminal) - 1)
        ),
        "terminal exact no-gap/no-overlap partition",
    )
    rows = [
        segment_row(contact_id, frontier, path, depth, interval, proof)
        for path, depth, interval, proof in terminal
    ]
    for ordinal, row in enumerate(rows, 1):
        row.pop("row_sha256")
        row["terminal_partition_ordinal"] = ordinal
        row["terminal_partition_count"] = len(rows)
        row["owned_lower_closed"] = True
        row["owned_upper_closed"] = ordinal == len(rows)
        row["row_sha256"] = digest(row)
    counts = Counter(row["classification"] for row in rows)
    unresolved = counts["UNRESOLVED"]
    complete = unresolved == 0
    resolution_depth = (
        max(row["depth"] for row in rows) if complete else None
    )
    require(
        (complete and counts["TRACE"] + counts["ABSENT"] == len(rows))
        or (
            not complete
            and counts["TRACE"] + counts["ABSENT"] + unresolved == len(rows)
        ),
        "complete/incomplete partition conservation",
    )
    contact = closed_row({
        "exact_contact_row_id": contact_id,
        **contact_identity,
        "fixed_axis": fixed_axis,
        "shared_coordinate": frontier["shared_coordinate"],
        "negative_leaf_row_id": frontier["negative_leaf_row_id"],
        "positive_leaf_row_id": frontier["positive_leaf_row_id"],
        "official_key_ordinal": frontier["official_key_ordinal"],
        "original_transverse_interval":
            copy.deepcopy(frontier["transverse_interval"]),
        "maximum_adaptive_depth": MAX_DEPTH,
        "complete_contact_resolution_depth": resolution_depth,
        "terminal_subface_count": len(rows),
        "TRACE_terminal_subface_count": counts["TRACE"],
        "ABSENT_terminal_subface_count": counts["ABSENT"],
        "UNRESOLVED_terminal_subface_count": unresolved,
        "terminal_subface_rows_sha256": digest([
            [row["terminal_subface_row_id"], row["row_sha256"]]
            for row in rows
        ]),
        "terminal_partition_exact_union_of_original_face": True,
        "terminal_partition_has_no_gap": True,
        "terminal_partition_has_no_owned_overlap": True,
        "complete_TRACE_plus_ABSENT_union_of_whole_common_face": complete,
        "formal_exact_contact_common_refinement_complete_credit":
            int(complete),
        "formal_component_deduplication_credit": 0,
        "whole_leaf_credit": 0,
        "whole_origin_credit": 0,
        "whole_original_tube_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })
    return contact, rows


def partial_row(
    frontier: dict[str, Any],
    evaluator: tuple[str, str, str],
) -> dict[str, Any]:
    chart, target, active = evaluator
    fixed_axis = frontier["axis"]
    coordinate = Q(frontier["shared_coordinate"])
    overlaps = [
        tuple(Q(value) for value in interval)
        for interval in frontier["overlaps"]
    ]
    if fixed_axis == "p":
        attempts = [(
            "t",
            overlaps[0],
            overlaps[1],
        )]
    else:
        require(fixed_axis == "t", "Round217 partial p/t frontier")
        attempts = [
            ("p", overlaps[0], overlaps[1]),
            ("s", overlaps[1], overlaps[0]),
        ]
    proofs: list[dict[str, Any]] = []
    accepted: tuple[str, dict[str, Any]] | None = None
    for graph_axis, graph_interval, transverse_interval in attempts:
        proof = interval_proof(
            chart,
            target,
            active,
            fixed_axis,
            coordinate,
            graph_axis,
            graph_interval,
            transverse_interval,
        )
        proofs.append({"graph_axis": graph_axis, **proof})
        if (
            accepted is None
            and proof["classification"] in {"TRACE", "ABSENT"}
        ):
            accepted = (graph_axis, proof)
    if accepted is None:
        classification = "UNRESOLVED"
        accepted_axis = None
        witness_sha = None
    else:
        accepted_axis, accepted_proof = accepted
        classification = accepted_proof["classification"]
        witness_sha = accepted_proof["interval_witness_sha256"]
    require(classification != "TRACE",
            "no unsupported partial trace promotion at depth zero")
    identity = {
        "Round217_frontier_row_id": frontier["frontier_row_id"],
        "Round217_frontier_row_sha256": frontier["row_sha256"],
    }
    return closed_row({
        "partial_contact_row_id": row_id("partial-contact", identity),
        **identity,
        "fixed_axis": fixed_axis,
        "shared_coordinate": frontier["shared_coordinate"],
        "negative_leaf_row_id": frontier["negative_leaf_row_id"],
        "positive_leaf_row_id": frontier["positive_leaf_row_id"],
        "positive_overlap_intervals": copy.deepcopy(frontier["overlaps"]),
        "graph_axis_attempts": proofs,
        "classification": classification,
        "accepted_graph_axis": accepted_axis,
        "accepted_interval_witness_sha256": witness_sha,
        "formal_partial_subface_zero_absence_credit":
            int(classification == "ABSENT"),
        "formal_partial_subface_trace_credit": 0,
        "formal_partial_subface_glue_credit": 0,
        "formal_component_deduplication_credit": 0,
        "whole_leaf_credit": 0,
        "whole_origin_credit": 0,
        "whole_original_tube_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def validate_closed_output_rows(
    rows: list[dict[str, Any]],
    id_key: str,
) -> None:
    require(len({row[id_key] for row in rows}) == len(rows),
            f"unique output IDs:{id_key}")
    for row in rows:
        payload = dict(row)
        row_hash = payload.pop("row_sha256")
        require(digest(payload) == row_hash, f"closed output row:{id_key}")


def build_result(producer_sha256: str) -> dict[str, Any]:
    print("Round219 loading exact Round217 frontier", file=sys.stderr)
    (
        result217,
        exact_frontier,
        partial_frontier,
        evaluators,
        input_hashes,
    ) = load_boundary()
    ctx.prec = 256

    contact_rows: list[dict[str, Any]] = []
    terminal_rows: list[dict[str, Any]] = []
    print("Round219 building depth-six exact subface partitions",
          file=sys.stderr)
    for index, frontier in enumerate(exact_frontier, 1):
        contact, segments = exact_contact_partition(frontier)
        contact_rows.append(contact)
        terminal_rows.extend(segments)
        if index % 1000 == 0:
            print(f"Round219 exact contacts {index}/{len(exact_frontier)}",
                  file=sys.stderr)
    contact_rows.sort(key=lambda row: row["exact_contact_row_id"])
    terminal_rows.sort(key=lambda row: row["terminal_subface_row_id"])
    partial_rows = sorted(
        (
            partial_row(
                frontier,
                evaluators[frontier["negative_leaf_row_id"]],
            )
            for frontier in partial_frontier
        ),
        key=lambda row: row["partial_contact_row_id"],
    )
    validate_closed_output_rows(
        contact_rows, "exact_contact_row_id"
    )
    validate_closed_output_rows(
        terminal_rows, "terminal_subface_row_id"
    )
    validate_closed_output_rows(
        partial_rows, "partial_contact_row_id"
    )

    subface_counts = Counter(row["classification"] for row in terminal_rows)
    complete_contacts = [
        row for row in contact_rows
        if row[
            "formal_exact_contact_common_refinement_complete_credit"
        ] == 1
    ]
    incomplete_contacts = [
        row for row in contact_rows
        if row[
            "formal_exact_contact_common_refinement_complete_credit"
        ] == 0
    ]
    partial_counts = Counter(row["classification"] for row in partial_rows)
    require(
        len(contact_rows) == EXPECTED_EXACT_FRONTIER
        and len(terminal_rows) == EXPECTED_TERMINAL_SUBFACES
        and subface_counts
        == Counter({
            "TRACE": EXPECTED_TRACE_SUBFACES,
            "ABSENT": EXPECTED_ABSENT_SUBFACES,
            "UNRESOLVED": EXPECTED_UNRESOLVED_SUBFACES,
        })
        and len(complete_contacts) == EXPECTED_COMPLETE_CONTACTS
        and len(incomplete_contacts) == EXPECTED_REMAINING_CONTACTS,
        "exact adaptive partition census",
    )
    require(
        len(partial_rows) == EXPECTED_PARTIAL_FRONTIER
        and partial_counts
        == Counter({
            "ABSENT": EXPECTED_PARTIAL_ABSENT,
            "UNRESOLVED": EXPECTED_PARTIAL_REMAINING,
        }),
        "partial contact depth-zero census",
    )
    require(
        all(
            row["UNRESOLVED_terminal_subface_count"] == 0
            and row[
                "complete_TRACE_plus_ABSENT_union_of_whole_common_face"
            ] is True
            for row in complete_contacts
        )
        and all(
            row["UNRESOLVED_terminal_subface_count"] > 0
            and row[
                "complete_TRACE_plus_ABSENT_union_of_whole_common_face"
            ] is False
            for row in incomplete_contacts
        ),
        "complete contact exact-equivalence boundary",
    )

    complete_ordinals = Counter(
        row["official_key_ordinal"] for row in complete_contacts
    )
    terminal_depths = Counter(row["depth"] for row in terminal_rows)
    complete_max_depths = Counter(
        row["complete_contact_resolution_depth"] for row in complete_contacts
    )
    partial_absent_axis = Counter(
        row["fixed_axis"] for row in partial_rows
        if row["classification"] == "ABSENT"
    )
    partial_remaining_axis = Counter(
        row["fixed_axis"] for row in partial_rows
        if row["classification"] == "UNRESOLVED"
    )

    return {
        "status": STATUS,
        "verdict": (
            "FORMAL_ADAPTIVE_EXACT_SUBFACE_PREFIX__468_NEW_EXACT_CONTACT_"
            "COMMON_REFINEMENTS_COMPLETE__7016_EXACT_AND_236_PARTIAL_"
            "CONTACTS_REMAIN_FAIL_CLOSED"
        ),
        "formal_input_binding": {
            **input_hashes,
            "input_is_exactly_Round217_exact_frontier_row_count":
                len(exact_frontier),
            "input_is_exactly_Round217_partial_frontier_row_count":
                len(partial_frontier),
            "Round217_direct_accepted_contact_count":
                EXPECTED_ROUND217_DIRECT_ACCEPTED,
            "Round217_direct_accepted_and_exact_frontier_disjoint": True,
            "Round217_direct_plus_exact_frontier_identity":
                "448+7484=7932",
            "Round217_producer_imported_or_executed": False,
            "Round186_used_as_pinned_interval_factor_evaluator": True,
        },
        "adaptive_partition_contract": {
            "maximum_dyadic_depth": MAX_DEPTH,
            "split_only_UNRESOLVED_children": True,
            "terminal_owner_rule":
                "LEFT_CLOSED_RIGHT_OPEN_EXCEPT_FINAL_RIGHT_CLOSED",
            "every_contact_terminal_partition_exact_union_of_original_face":
                True,
            "every_contact_terminal_partition_no_gap": True,
            "every_contact_terminal_partition_no_owned_overlap": True,
            "complete_contact_requires_zero_UNRESOLVED_children": True,
            "TRACE_acceptance_requires_strict_opposite_full_child_endpoint_"
            "C0_and_strict_full_child_derivative": True,
            "ABSENT_acceptance_requires_same_strict_full_child_endpoint_C0_"
            "and_strict_full_child_derivative": True,
            "midpoint_or_box_touch_alone_never_accepted": True,
        },
        "formal_terminal_subface_scope": {
            "terminal_subface_count": len(terminal_rows),
            "TRACE_terminal_subface_count": subface_counts["TRACE"],
            "ABSENT_terminal_subface_count": subface_counts["ABSENT"],
            "UNRESOLVED_terminal_subface_count":
                subface_counts["UNRESOLVED"],
            "UNRESOLVED_count_is_subfaces_not_contacts": True,
            "terminal_depth_histogram":
                dict(sorted(terminal_depths.items())),
            "formal_restricted_zero_curve_credits":
                subface_counts["TRACE"],
            "formal_two_sided_incidence_credits":
                2 * subface_counts["TRACE"],
            "formal_exact_subface_glue_credits":
                subface_counts["TRACE"],
            "formal_zero_absence_credits":
                subface_counts["ABSENT"],
        },
        "formal_exact_contact_scope": {
            "Round217_frontier_contact_count": len(contact_rows),
            "new_complete_common_refinement_contact_count":
                len(complete_contacts),
            "remaining_incomplete_contact_count": len(incomplete_contacts),
            "Round217_direct_complete_contact_count":
                EXPECTED_ROUND217_DIRECT_ACCEPTED,
            "cumulative_complete_contact_count":
                EXPECTED_CUMULATIVE_COMPLETE,
            "cumulative_complete_identity": "448+468=916",
            "cumulative_remaining_identity": "7932-916=7016",
            "complete_contact_resolution_depth_histogram":
                dict(sorted(complete_max_depths.items())),
            "new_complete_official_key_ordinal_count":
                len(complete_ordinals),
            "new_complete_contacts_per_official_key_ordinal": {
                str(key): value
                for key, value in sorted(complete_ordinals.items())
            },
            "new_complete_contacts_per_official_key_ordinal_sha256":
                digest(dict(sorted(complete_ordinals.items()))),
            "physical_component_equivalence_relation_complete": False,
        },
        "formal_partial_contact_scope": {
            "Round217_partial_frontier_count": len(partial_rows),
            "new_formal_partial_zero_absence_count":
                partial_counts["ABSENT"],
            "remaining_partial_contact_count":
                partial_counts["UNRESOLVED"],
            "new_absence_axis_count":
                dict(sorted(partial_absent_axis.items())),
            "remaining_axis_count":
                dict(sorted(partial_remaining_axis.items())),
            "partial_restricted_zero_curve_count": 0,
            "partial_endpoint_to_curve_interior_join_count": 0,
        },
        "formal_terminal_subface_ledger":
            ledger(terminal_rows, "terminal_subface_row_id"),
        "formal_exact_contact_partition_ledger":
            ledger(contact_rows, "exact_contact_row_id"),
        "formal_partial_contact_probe_ledger":
            ledger(partial_rows, "partial_contact_row_id"),
        "first_missing_frontier": {
            "remaining_exact_contact_count": len(incomplete_contacts),
            "remaining_UNRESOLVED_exact_terminal_subface_count":
                subface_counts["UNRESOLVED"],
            "remaining_partial_contact_count":
                partial_counts["UNRESOLVED"],
            "Round211_endpoint_rows_missing_exact_root_coordinate": True,
            "endpoint_to_curve_interior_join_count": 0,
            "exact_root_isolation_or_symbolic_coordinate_required": True,
            "depth_seven_or_deeper_not_claimed": True,
            "complete_physical_component_equivalence_closure_missing": True,
        },
        "formal_credit_contract": {
            "formal_exact_contact_common_refinement_complete_credits":
                len(complete_contacts),
            "formal_partial_zero_absence_credits":
                partial_counts["ABSENT"],
            "formal_component_deduplication_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_component_credit": 0,
            "global_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator":
                EXPECTED_SOURCE_G_KEYS,
            "D02": "UNCHANGED_BLOCKED",
            "Gate5": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
        },
        "required_next": (
            "isolate or symbolically represent the exact t-boundary root "
            "coordinates inside the remaining 7236 unresolved exact "
            "terminal subfaces, then materialize endpoint-to-curve-interior "
            "joins and close the physical-component equivalence relation; "
            "the 236 partial contacts require the same restricted-curve "
            "treatment"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "python_flint_version":
                getattr(__import__("flint"), "__version__", "unknown"),
            "effective_Arb_precision_bits": ctx.prec,
            "producer_imported_or_executed_by_independent_verifier": False,
            "formal_upstream_files_modified": False,
        },
    }


def validate_output(path: Path) -> Path:
    absolute = path.resolve(strict=False)
    require(absolute.parent == HERE.resolve(), "output parent")
    official = absolute.name == OUTPUT.name
    replay = (
        absolute.name.startswith(f".{PREFIX}_replay_")
        and absolute.name.endswith(".json")
    )
    require(official or replay, "output filename")
    require(not absolute.is_symlink(), "output symlink")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "output existing regular unique",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{PREFIX}.tmp.", dir=HERE
    )
    temp_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, destination)
        directory = os.open(HERE, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    source_sha256 = hashlib.sha256(
        regular_bytes(Path(__file__), 5_000_000)
    ).hexdigest()
    result = build_result(source_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical_bytes(envelope) + b"\n")
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
