#!/usr/bin/env python3
"""Fresh independent verifier for Round219 adaptive subface materialization.

The expected object is rebuilt from the pinned Round217/Round209/Round186
boundary before the Round219 candidate certificate is loaded.  This verifier
does not import or execute the Round219 producer.
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
PRODUCER = f"{PREFIX}.py"
CERTIFICATE = f"{PREFIX}_certificate.json"
VERIFICATION = f"{PREFIX}_verification.json"
SCHEMA = "cm2.round219.source-g-partial-face-common-refinement-glue.v1"
VERIFICATION_SCHEMA = (
    "cm2.round219.source-g-partial-face-common-refinement-glue-verification.v1"
)
STATUS = (
    "CERTIFIED_ADAPTIVE_EXACT_SUBFACE_TRACE_ABSENCE_AND_GLUE_PREFIX__"
    "ENDPOINT_TO_INTERIOR_AND_PHYSICAL_COMPONENT_CLOSURE_INCOMPLETE"
)
VERDICT = (
    "FORMAL_ADAPTIVE_EXACT_SUBFACE_PREFIX__468_NEW_EXACT_CONTACT_"
    "COMMON_REFINEMENTS_COMPLETE__7016_EXACT_AND_236_PARTIAL_"
    "CONTACTS_REMAIN_FAIL_CLOSED"
)
PRODUCER_SHA256 = (
    "8b670ffbcabd5a9796fb67580cbb9e3318b8eb2ee1cd65c5e71f7f1f360b3019"
)
CERTIFICATE_SHA256 = (
    "8341a8b08a0abd5c7a16c61b918b7b47db4d05c3c4e6fae8615892e3aafaf096"
)
RESULT_SHA256 = (
    "f8d46a9a220b6b7e0e6f86430ad6d537d5358cd610f064417ab3e8b4c125744e"
)

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

MAX_BYTES = 300 * 1024 * 1024
MAX_DEPTH = 6
DIRECT_ACCEPTED = 448
EXACT_FRONTIER = 7_484
EXACT_TOTAL = 7_932
TRACE_SUBFACES = 22_960
ABSENT_SUBFACES = 22_096
UNRESOLVED_SUBFACES = 7_236
TERMINAL_SUBFACES = 52_292
COMPLETE_CONTACTS = 468
REMAINING_CONTACTS = 7_016
CUMULATIVE_COMPLETE = 916
PARTIAL_FRONTIER = 264
PARTIAL_ABSENT = 28
PARTIAL_REMAINING = 236
SOURCE_G_KEYS = 224_580
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for part in ENCODER.iterencode(value):
        yield part.encode()


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for part in chunks(value):
        state.update(part)
    return state.hexdigest()


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(payload)
    value["row_sha256"] = digest(value)
    return value


def identifier(kind: str, payload: dict[str, Any]) -> str:
    return f"round219-{kind}:{digest(payload)}"


def histogram(values: Iterable[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonfinite JSON:{value}")


def strict_json(raw: bytes, maximum: int = MAX_BYTES) -> dict[str, Any]:
    require(0 < len(raw) <= maximum, "JSON size")
    require(not raw.startswith(b"\xef\xbb\xbf"), "JSON BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise VerificationError("JSON UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_pairs,
            parse_constant=reject_constant,
        )
    except json.JSONDecodeError as error:
        raise VerificationError("strict JSON parse") from error
    require(isinstance(value, dict), "JSON top object")
    try:
        expected = canonical(value) + b"\n"
    except UnicodeEncodeError as error:
        raise VerificationError("JSON scalar") from error
    require(raw == expected, "canonical JSON bytes")
    return value


def secure_read(
    path: Path,
    maximum: int,
    parent: Path,
    name: str,
) -> bytes:
    require(
        not any(part == ".." for part in path.parts),
        "path parent alias",
    )
    expected_parent = Path(os.path.abspath(os.fspath(parent)))
    require(
        parent.resolve() == expected_parent,
        "expected parent alias",
    )
    require(
        path.is_absolute() and path.parent == expected_parent,
        "path raw parent",
    )
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.name == name, "path filename")
    require(
        path.parent == expected_parent
        and path.parent.resolve() == expected_parent,
        "path exact parent",
    )
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), "path regular")
    require(not path.is_symlink(), "path symlink")
    require(before.st_nlink == 1, "path hardlink")
    require(0 < before.st_size <= maximum, "path size")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns,
            )
            == (
                before.st_dev, before.st_ino, before.st_size,
                before.st_mtime_ns,
            ),
            "path stable open",
        )
        parts: list[bytes] = []
        total = 0
        while True:
            part = os.read(descriptor, 1024 * 1024)
            if not part:
                break
            total += len(part)
            require(total <= maximum, "path bounded read")
            parts.append(part)
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev, after.st_ino, after.st_size,
                after.st_mtime_ns,
            )
            == (
                opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns,
            ),
            "path stable read",
        )
        return b"".join(parts)
    finally:
        os.close(descriptor)


def pinned(path: Path, expected: str, maximum: int) -> bytes:
    raw = secure_read(path, maximum, HERE, path.name)
    require(hashlib.sha256(raw).hexdigest() == expected,
            f"SHA256:{path.name}")
    return raw


def make_ledger(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def validate_ledger(
    value: dict[str, Any],
    id_key: str,
) -> list[dict[str, Any]]:
    rows = value["rows"]
    require(
        value["row_count"] == len(rows)
        and value["rows_sha256"] == digest(rows)
        and value["row_ids_sha256"]
        == digest([row[id_key] for row in rows])
        and value["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows])
        and value["every_row_closed_by_own_SHA256"] is True
        and len({row[id_key] for row in rows}) == len(rows),
        f"ledger:{id_key}",
    )
    for row in rows:
        payload = dict(row)
        row_hash = payload.pop("row_sha256")
        require(digest(payload) == row_hash, f"row closure:{id_key}")
    return rows


def upstream_boundary() -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, tuple[str, str, str]],
    dict[str, str],
]:
    require(
        Path(r209.__file__).resolve() == (HERE / R209_SOURCE).resolve()
        and Path(r186.__file__).resolve() == (HERE / R186_SOURCE).resolve(),
        "module identity",
    )
    pinned(HERE / R217_SOURCE, R217_SOURCE_SHA256, 5_000_000)
    raw217 = pinned(
        HERE / R217_CERTIFICATE, R217_CERTIFICATE_SHA256, 50_000_000
    )
    pinned(HERE / R209_SOURCE, R209_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R186_SOURCE, R186_SOURCE_SHA256, 5_000_000)
    envelope217 = strict_json(raw217)
    require(
        set(envelope217) == {"schema", "result", "result_sha256"}
        and envelope217["result_sha256"] == R217_RESULT_SHA256
        and digest(envelope217["result"]) == R217_RESULT_SHA256,
        "Round217 closure",
    )
    result217 = envelope217["result"]
    glues217 = validate_ledger(
        result217["formal_exact_common_refinement_glue_ledger"],
        "glue_row_id",
    )
    exact_rows = result217[
        "exact_face_endpoint_to_interior_frontier"
    ]["rows"]
    partial_rows = result217["partial_face_frontier"]["rows"]
    require(
        len(exact_rows) == EXACT_FRONTIER
        and len(partial_rows) == PARTIAL_FRONTIER
        and digest(exact_rows)
        == result217[
            "exact_face_endpoint_to_interior_frontier"
        ]["rows_sha256"]
        and digest(partial_rows)
        == result217["partial_face_frontier"]["rows_sha256"],
        "Round217 frontiers",
    )
    for rows in (exact_rows, partial_rows):
        for row in rows:
            payload = dict(row)
            row_hash = payload.pop("row_sha256")
            require(digest(payload) == row_hash, "Round217 frontier row")
    accepted_pairs = {
        (
            row["negative_side_leaf_row_id"],
            row["positive_side_leaf_row_id"],
        )
        for row in glues217
    }
    frontier_pairs = {
        (row["negative_leaf_row_id"], row["positive_leaf_row_id"])
        for row in exact_rows
    }
    require(
        len(accepted_pairs) == DIRECT_ACCEPTED
        and len(frontier_pairs) == EXACT_FRONTIER
        and accepted_pairs.isdisjoint(frontier_pairs)
        and len(accepted_pairs | frontier_pairs) == EXACT_TOTAL,
        "Round217 exact pair disjoint union",
    )

    _r173, result208, hashes209 = r209.validate_inputs()
    leaves, regions, _faces, _u2 = r209.validate_round195_geometry(result208)
    sheets, _curves, _endpoints, _audit = r209.build_lineages(leaves, regions)
    region_by_id = {row["region_row_id"]: row for row in regions}
    sheet_by_leaf = {row["leaf_row_id"]: row for row in sheets}
    evaluators: dict[str, tuple[str, str, str]] = {}
    for leaf, sheet in sheet_by_leaf.items():
        signature = region_by_id[
            sheet["owner_region_row_id"]
        ]["local_return_signature"]
        evaluators[leaf] = (
            signature["source_chart"],
            signature["target_lift"],
            sheet["active_factor"],
        )
    for row in exact_rows:
        require(
            evaluators[row["negative_leaf_row_id"]]
            == (
                row["source_chart"],
                row["target_lift"],
                row["active_factor"],
            )
            == evaluators[row["positive_leaf_row_id"]],
            "frontier evaluator",
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
    return result217, exact_rows, partial_rows, evaluators, hashes


def rectangle_proof(
    chart: str,
    target: str,
    active: str,
    fixed_axis: str,
    fixed: Q,
    graph_axis: str,
    graph: tuple[Q, Q],
    transverse: tuple[Q, Q],
) -> dict[str, Any]:
    atlas = r186.r179.r174.atlas.AtlasBox
    sign = r186.r179.arb_sign
    g0, g1 = graph
    u0, u1 = transverse
    if fixed_axis == "p" and graph_axis == "t":
        def box(a: Q, b: Q) -> Any:
            return atlas(a, b, fixed, fixed, u0, u1, 0, "verify219")
        derivative_index = 0
    elif fixed_axis == "s" and graph_axis == "t":
        def box(a: Q, b: Q) -> Any:
            return atlas(a, b, u0, u1, fixed, fixed, 0, "verify219")
        derivative_index = 0
    elif fixed_axis == "t" and graph_axis == "p":
        def box(a: Q, b: Q) -> Any:
            return atlas(fixed, fixed, a, b, u0, u1, 0, "verify219")
        derivative_index = 1
    elif fixed_axis == "t" and graph_axis == "s":
        def box(a: Q, b: Q) -> Any:
            return atlas(fixed, fixed, u0, u1, a, b, 0, "verify219")
        derivative_index = 2
    else:
        raise VerificationError("rectangle axes")
    lower_box = box(g0, g0)
    upper_box = box(g1, g1)
    full_box = box(g0, g1)
    lower = r186.factor_geometry(chart, target, lower_box)[active]
    upper = r186.factor_geometry(chart, target, upper_box)[active]
    full = r186.factor_geometry(chart, target, full_box)[active]
    lower_centered = r186.centered_value(chart, target, lower_box, active)
    upper_centered = r186.centered_value(chart, target, upper_box, active)
    direct = (
        sign(lower[0]),
        sign(upper[0]),
        sign(full[1][derivative_index]),
    )
    centered = (sign(lower_centered), sign(upper_centered))
    selected = (
        direct[0] if direct[0] in STRICT_SIGNS else centered[0],
        direct[1] if direct[1] in STRICT_SIGNS else centered[1],
        direct[2],
    )
    if (
        selected[0] in STRICT_SIGNS
        and selected[1] in STRICT_SIGNS
        and selected[2] in STRICT_SIGNS
    ):
        classification = (
            "TRACE" if selected[0] != selected[1] else "ABSENT"
        )
    else:
        classification = "UNRESOLVED"
    witness = {
        "direct_signs": list(direct),
        "centered_endpoint_signs": list(centered),
        "selected_signs": list(selected),
        "direct_lower_C0": str(lower[0]),
        "centered_lower_C0": str(lower_centered),
        "direct_upper_C0": str(upper[0]),
        "centered_upper_C0": str(upper_centered),
        "full_graph_axis_derivative": str(full[1][derivative_index]),
    }
    return {
        "classification": classification,
        "selected_lower_upper_derivative_signs": list(selected),
        "interval_witness_sha256": digest(witness),
        "proof_rule": (
            "FULL_CHILD_ENDPOINT_C0_AND_FULL_CHILD_STRICT_GRAPH_AXIS_"
            "DERIVATIVE"
        ),
    }


def expected_segment(
    contact_id: str,
    frontier: dict[str, Any],
    path: str,
    depth: int,
    interval: tuple[Q, Q],
    proof: dict[str, Any],
) -> dict[str, Any]:
    axis = frontier["fixed_axis"]
    identity = {
        "contact_row_id": contact_id,
        "dyadic_path": path,
        "depth": depth,
        "transverse_interval": [str(value) for value in interval],
    }
    segment_id = identifier("terminal-subface", identity)
    is_trace = proof["classification"] == "TRACE"
    trace_id = (
        identifier(
            "restricted-zero-curve",
            {"terminal_subface_row_id": segment_id},
        )
        if is_trace else None
    )
    negative_incidence = (
        identifier("negative-side-incidence", {
            "trace_row_id": trace_id,
            "leaf_row_id": frontier["negative_leaf_row_id"],
            "orientation": "POSITIVE_" + axis.upper(),
        })
        if is_trace else None
    )
    positive_incidence = (
        identifier("positive-side-incidence", {
            "trace_row_id": trace_id,
            "leaf_row_id": frontier["positive_leaf_row_id"],
            "orientation": "NEGATIVE_" + axis.upper(),
        })
        if is_trace else None
    )
    glue = (
        identifier("restricted-common-refinement-glue", {
            "trace_row_id": trace_id,
            "negative_incidence_row_id": negative_incidence,
            "positive_incidence_row_id": positive_incidence,
        })
        if is_trace else None
    )
    return closed({
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
        "classification": proof["classification"],
        **proof,
        "restricted_zero_curve_row_id": trace_id,
        "negative_side_incidence_row_id": negative_incidence,
        "negative_side_leaf_row_id": frontier["negative_leaf_row_id"],
        "negative_side_outward_orientation":
            "POSITIVE_" + axis.upper() if is_trace else None,
        "positive_side_incidence_row_id": positive_incidence,
        "positive_side_leaf_row_id": frontier["positive_leaf_row_id"],
        "positive_side_outward_orientation":
            "NEGATIVE_" + axis.upper() if is_trace else None,
        "exact_subface_common_refinement_glue_row_id": glue,
        "exact_restricted_evaluator_identity": True if is_trace else None,
        "joined_from_box_touch_or_signature_hash_alone": False,
        "formal_restricted_zero_curve_credit": int(is_trace),
        "formal_local_subface_incidence_credit": 2 * int(is_trace),
        "formal_local_subface_glue_credit": int(is_trace),
        "formal_local_zero_absence_credit":
            int(proof["classification"] == "ABSENT"),
        "formal_component_deduplication_credit": 0,
        "whole_leaf_credit": 0,
        "whole_origin_credit": 0,
        "whole_original_tube_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def expected_partition(
    frontier: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    contact_identity = {
        "Round217_frontier_row_id": frontier["frontier_row_id"],
        "Round217_frontier_row_sha256": frontier["row_sha256"],
    }
    contact_id = identifier("exact-contact", contact_identity)
    chart = frontier["source_chart"]
    target = frontier["target_lift"]
    active = frontier["active_factor"]
    fixed_axis = frontier["fixed_axis"]
    fixed = Q(frontier["shared_coordinate"])
    graph = tuple(Q(value) for value in frontier["t_interval"])
    original = tuple(
        Q(value) for value in frontier["transverse_interval"]
    )
    active_segments = [("", 0, original)]
    terminal: list[tuple[str, int, tuple[Q, Q], dict[str, Any]]] = []
    for depth in range(1, MAX_DEPTH + 1):
        following: list[tuple[str, int, tuple[Q, Q]]] = []
        for path, _old_depth, (lower, upper) in active_segments:
            middle = (lower + upper) / 2
            for suffix, interval in (
                ("L", (lower, middle)),
                ("R", (middle, upper)),
            ):
                proof = rectangle_proof(
                    chart, target, active, fixed_axis, fixed,
                    "t", graph, interval
                )
                child = path + suffix
                if proof["classification"] == "UNRESOLVED":
                    following.append((child, depth, interval))
                else:
                    terminal.append((child, depth, interval, proof))
        active_segments = following
    for path, depth, interval in active_segments:
        proof = rectangle_proof(
            chart, target, active, fixed_axis, fixed,
            "t", graph, interval
        )
        require(proof["classification"] == "UNRESOLVED",
                "depth-six unresolved")
        terminal.append((path, depth, interval, proof))
    terminal.sort(key=lambda item: (item[2][0], item[2][1], item[0]))
    require(
        terminal[0][2][0] == original[0]
        and terminal[-1][2][1] == original[1]
        and all(
            terminal[index][2][1] == terminal[index + 1][2][0]
            for index in range(len(terminal) - 1)
        ),
        "partition exact union",
    )
    rows = [
        expected_segment(contact_id, frontier, path, depth, interval, proof)
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
    complete = counts["UNRESOLVED"] == 0
    resolution_depth = (
        max(row["depth"] for row in rows) if complete else None
    )
    contact = closed({
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
        "UNRESOLVED_terminal_subface_count": counts["UNRESOLVED"],
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


def expected_partial(
    frontier: dict[str, Any],
    evaluator: tuple[str, str, str],
) -> dict[str, Any]:
    chart, target, active = evaluator
    fixed_axis = frontier["axis"]
    fixed = Q(frontier["shared_coordinate"])
    overlaps = [
        tuple(Q(value) for value in interval)
        for interval in frontier["overlaps"]
    ]
    attempts = (
        [("t", overlaps[0], overlaps[1])]
        if fixed_axis == "p"
        else [
            ("p", overlaps[0], overlaps[1]),
            ("s", overlaps[1], overlaps[0]),
        ]
    )
    proofs: list[dict[str, Any]] = []
    accepted: tuple[str, dict[str, Any]] | None = None
    for graph_axis, graph, transverse in attempts:
        proof = rectangle_proof(
            chart, target, active, fixed_axis, fixed,
            graph_axis, graph, transverse
        )
        proofs.append({"graph_axis": graph_axis, **proof})
        if accepted is None and proof["classification"] in {"TRACE", "ABSENT"}:
            accepted = (graph_axis, proof)
    if accepted is None:
        classification = "UNRESOLVED"
        accepted_axis = None
        witness = None
    else:
        accepted_axis, accepted_proof = accepted
        classification = accepted_proof["classification"]
        witness = accepted_proof["interval_witness_sha256"]
    require(classification != "TRACE", "partial TRACE remains forbidden")
    identity = {
        "Round217_frontier_row_id": frontier["frontier_row_id"],
        "Round217_frontier_row_sha256": frontier["row_sha256"],
    }
    return closed({
        "partial_contact_row_id": identifier("partial-contact", identity),
        **identity,
        "fixed_axis": fixed_axis,
        "shared_coordinate": frontier["shared_coordinate"],
        "negative_leaf_row_id": frontier["negative_leaf_row_id"],
        "positive_leaf_row_id": frontier["positive_leaf_row_id"],
        "positive_overlap_intervals": copy.deepcopy(frontier["overlaps"]),
        "graph_axis_attempts": proofs,
        "classification": classification,
        "accepted_graph_axis": accepted_axis,
        "accepted_interval_witness_sha256": witness,
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


def rebuild_expected() -> dict[str, Any]:
    (
        _result217,
        exact_frontier,
        partial_frontier,
        evaluators,
        input_hashes,
    ) = upstream_boundary()
    ctx.prec = 256
    contacts: list[dict[str, Any]] = []
    segments: list[dict[str, Any]] = []
    print("Round219 verifier rebuilding 7484 adaptive partitions",
          file=sys.stderr)
    for index, frontier in enumerate(exact_frontier, 1):
        contact, children = expected_partition(frontier)
        contacts.append(contact)
        segments.extend(children)
        if index % 1000 == 0:
            print(f"Round219 verifier contacts {index}/7484",
                  file=sys.stderr)
    contacts.sort(key=lambda row: row["exact_contact_row_id"])
    segments.sort(key=lambda row: row["terminal_subface_row_id"])
    partial = sorted(
        (
            expected_partial(
                row, evaluators[row["negative_leaf_row_id"]]
            )
            for row in partial_frontier
        ),
        key=lambda row: row["partial_contact_row_id"],
    )
    segment_counts = Counter(row["classification"] for row in segments)
    complete = [
        row for row in contacts
        if row[
            "formal_exact_contact_common_refinement_complete_credit"
        ] == 1
    ]
    incomplete = [
        row for row in contacts
        if row[
            "formal_exact_contact_common_refinement_complete_credit"
        ] == 0
    ]
    partial_counts = Counter(row["classification"] for row in partial)
    require(
        len(segments) == TERMINAL_SUBFACES
        and segment_counts
        == Counter({
            "TRACE": TRACE_SUBFACES,
            "ABSENT": ABSENT_SUBFACES,
            "UNRESOLVED": UNRESOLVED_SUBFACES,
        })
        and len(complete) == COMPLETE_CONTACTS
        and len(incomplete) == REMAINING_CONTACTS
        and partial_counts
        == Counter({"ABSENT": PARTIAL_ABSENT,
                    "UNRESOLVED": PARTIAL_REMAINING}),
        "independent Round219 census",
    )
    complete_ordinals = Counter(
        row["official_key_ordinal"] for row in complete
    )
    depths = Counter(row["depth"] for row in segments)
    resolution_depths = Counter(
        row["complete_contact_resolution_depth"] for row in complete
    )
    partial_absent_axis = Counter(
        row["fixed_axis"] for row in partial
        if row["classification"] == "ABSENT"
    )
    partial_remaining_axis = Counter(
        row["fixed_axis"] for row in partial
        if row["classification"] == "UNRESOLVED"
    )
    return {
        "status": STATUS,
        "verdict": VERDICT,
        "formal_input_binding": {
            **input_hashes,
            "input_is_exactly_Round217_exact_frontier_row_count":
                len(exact_frontier),
            "input_is_exactly_Round217_partial_frontier_row_count":
                len(partial_frontier),
            "Round217_direct_accepted_contact_count": DIRECT_ACCEPTED,
            "Round217_direct_accepted_and_exact_frontier_disjoint": True,
            "Round217_direct_plus_exact_frontier_identity": "448+7484=7932",
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
            "terminal_subface_count": len(segments),
            "TRACE_terminal_subface_count": segment_counts["TRACE"],
            "ABSENT_terminal_subface_count": segment_counts["ABSENT"],
            "UNRESOLVED_terminal_subface_count":
                segment_counts["UNRESOLVED"],
            "UNRESOLVED_count_is_subfaces_not_contacts": True,
            # JSON object keys are strings after the candidate is parsed.
            "terminal_depth_histogram": {
                str(key): value for key, value in sorted(depths.items())
            },
            "formal_restricted_zero_curve_credits": segment_counts["TRACE"],
            "formal_two_sided_incidence_credits":
                2 * segment_counts["TRACE"],
            "formal_exact_subface_glue_credits": segment_counts["TRACE"],
            "formal_zero_absence_credits": segment_counts["ABSENT"],
        },
        "formal_exact_contact_scope": {
            "Round217_frontier_contact_count": len(contacts),
            "new_complete_common_refinement_contact_count": len(complete),
            "remaining_incomplete_contact_count": len(incomplete),
            "Round217_direct_complete_contact_count": DIRECT_ACCEPTED,
            "cumulative_complete_contact_count": CUMULATIVE_COMPLETE,
            "cumulative_complete_identity": "448+468=916",
            "cumulative_remaining_identity": "7932-916=7016",
            "complete_contact_resolution_depth_histogram":
                {
                    str(key): value
                    for key, value in sorted(resolution_depths.items())
                },
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
            "Round217_partial_frontier_count": len(partial),
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
            make_ledger(segments, "terminal_subface_row_id"),
        "formal_exact_contact_partition_ledger":
            make_ledger(contacts, "exact_contact_row_id"),
        "formal_partial_contact_probe_ledger":
            make_ledger(partial, "partial_contact_row_id"),
        "first_missing_frontier": {
            "remaining_exact_contact_count": len(incomplete),
            "remaining_UNRESOLVED_exact_terminal_subface_count":
                segment_counts["UNRESOLVED"],
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
                len(complete),
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
                SOURCE_G_KEYS,
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
            "producer_sha256": PRODUCER_SHA256,
            "python_version": sys.version.split()[0],
            "python_flint_version":
                getattr(__import__("flint"), "__version__", "unknown"),
            "effective_Arb_precision_bits": ctx.prec,
            "producer_imported_or_executed_by_independent_verifier": False,
            "formal_upstream_files_modified": False,
        },
    }


def verify_envelope(
    envelope: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    require(
        set(envelope) == {"schema", "result", "result_sha256"}
        and envelope["schema"] == SCHEMA
        and envelope["result_sha256"] == digest(envelope["result"]),
        "candidate envelope",
    )
    result = envelope["result"]
    for key, id_key in (
        ("formal_terminal_subface_ledger", "terminal_subface_row_id"),
        ("formal_exact_contact_partition_ledger", "exact_contact_row_id"),
        ("formal_partial_contact_probe_ledger", "partial_contact_row_id"),
    ):
        validate_ledger(result[key], id_key)
    require(result == expected, "full expected Python-object equality")
    require(canonical(result) == canonical(expected),
            "full expected canonical equality")


def resign(envelope: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(envelope)
    result = value["result"]
    for key, id_key in (
        ("formal_terminal_subface_ledger", "terminal_subface_row_id"),
        ("formal_exact_contact_partition_ledger", "exact_contact_row_id"),
        ("formal_partial_contact_probe_ledger", "partial_contact_row_id"),
    ):
        ledger_value = result[key]
        rows = ledger_value["rows"]
        for row in rows:
            payload = dict(row)
            payload.pop("row_sha256", None)
            row["row_sha256"] = digest(payload)
        ledger_value["row_count"] = len(rows)
        ledger_value["rows_sha256"] = digest(rows)
        ledger_value["row_ids_sha256"] = digest(
            [row[id_key] for row in rows]
        )
        ledger_value["row_hashes_sha256"] = digest(
            [row["row_sha256"] for row in rows]
        )
    value["result_sha256"] = digest(result)
    return value


def semantic_suite(
    envelope: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[int, int]:
    def toggle_class(result: dict[str, Any]) -> None:
        row = result["formal_terminal_subface_ledger"]["rows"][0]
        row["classification"] = (
            "ABSENT" if row["classification"] == "TRACE" else "TRACE"
        )

    def false_complete(result: dict[str, Any]) -> None:
        row = next(
            item
            for item in result[
                "formal_exact_contact_partition_ledger"
            ]["rows"]
            if item["UNRESOLVED_terminal_subface_count"] > 0
        )
        row["complete_TRACE_plus_ABSENT_union_of_whole_common_face"] = True
        row["formal_exact_contact_common_refinement_complete_credit"] = 1

    def duplicate_subface(result: dict[str, Any]) -> None:
        result["formal_terminal_subface_ledger"]["rows"].append(
            copy.deepcopy(result["formal_terminal_subface_ledger"]["rows"][0])
        )

    def omit_subface(result: dict[str, Any]) -> None:
        result["formal_terminal_subface_ledger"]["rows"].pop()

    def duplicate_contact(result: dict[str, Any]) -> None:
        result["formal_exact_contact_partition_ledger"]["rows"].append(
            copy.deepcopy(
                result["formal_exact_contact_partition_ledger"]["rows"][0]
            )
        )

    def omit_contact(result: dict[str, Any]) -> None:
        result["formal_exact_contact_partition_ledger"]["rows"].pop()

    def toggle_upper_owner(result: dict[str, Any]) -> None:
        row = result["formal_terminal_subface_ledger"]["rows"][0]
        row["owned_upper_closed"] = not row["owned_upper_closed"]

    mutations = [
        toggle_class,
        lambda r: r["formal_terminal_subface_ledger"]["rows"][0].
            __setitem__("transverse_interval", ["0", "1"]),
        toggle_upper_owner,
        lambda r: r["formal_terminal_subface_ledger"]["rows"][0].
            __setitem__("depth", 7),
        false_complete,
        duplicate_subface,
        omit_subface,
        duplicate_contact,
        omit_contact,
        lambda r: r["formal_partial_contact_probe_ledger"]["rows"][0].
            __setitem__("classification", "TRACE"),
        lambda r: r["formal_partial_contact_probe_ledger"]["rows"][0].
            __setitem__("formal_partial_subface_trace_credit", 1),
        lambda r: r["formal_terminal_subface_scope"].
            __setitem__("UNRESOLVED_count_is_subfaces_not_contacts", False),
        lambda r: r["formal_exact_contact_scope"].
            __setitem__("remaining_incomplete_contact_count", 7_236),
        lambda r: r["formal_input_binding"].
            __setitem__(
                "Round217_direct_accepted_and_exact_frontier_disjoint", False
            ),
        lambda r: r["formal_credit_contract"].
            __setitem__("formal_component_deduplication_credit", 1),
        lambda r: r["formal_credit_contract"].
            __setitem__("whole_origin_credit", 1),
        lambda r: r["formal_credit_contract"].
            __setitem__("whole_original_tube_credit", 1),
        lambda r: r["formal_credit_contract"].
            __setitem__("global_exact_key_disposition_credit", 1),
        lambda r: r["first_missing_frontier"].
            __setitem__("depth_seven_or_deeper_not_claimed", False),
        lambda r: r["adaptive_partition_contract"].
            __setitem__("every_contact_terminal_partition_no_gap", False),
        lambda r: r["adaptive_partition_contract"].
            __setitem__("every_contact_terminal_partition_no_owned_overlap",
                        False),
    ]
    rejected = 0
    for mutation in mutations:
        candidate = copy.deepcopy(envelope)
        mutation(candidate["result"])
        candidate = resign(candidate)
        try:
            verify_envelope(candidate, expected)
        except VerificationError:
            rejected += 1
    return len(mutations), rejected


def json_suite(envelope: dict[str, Any]) -> tuple[int, int]:
    good = canonical(envelope) + b"\n"
    text = good.decode()
    attacks: list[tuple[bytes, int]] = [
        (b'{"x":1,"x":2}\n', MAX_BYTES),
        (
            text.replace(
                '"result":{',
                '"result":{"status":"x","status":"y",',
                1,
            ).encode(),
            MAX_BYTES,
        ),
        (
            text.replace('"result":{', '"result":{"x":NaN,', 1).encode(),
            MAX_BYTES,
        ),
        (
            text.replace('"result":{', '"result":{"x":Infinity,', 1).encode(),
            MAX_BYTES,
        ),
        (
            text.replace('"result":{', '"result":{"x":-Infinity,', 1).encode(),
            MAX_BYTES,
        ),
        (good + b" ", MAX_BYTES),
        (b"\xef\xbb\xbf" + good, MAX_BYTES),
        (b"[]\n", MAX_BYTES),
        (b"1\n", MAX_BYTES),
        (b"", MAX_BYTES),
        (canonical(envelope), MAX_BYTES),
        (b'{"x":"' + bytes([255]) + b'"}\n', MAX_BYTES),
        (b'{"x":"\\ud800"}\n', MAX_BYTES),
        (b'{"x":"a' + bytes([0]) + b'b"}\n', MAX_BYTES),
        (good, len(good) - 1),
    ]
    rejected = 0
    for raw, maximum in attacks:
        try:
            strict_json(raw, maximum)
        except (VerificationError, UnicodeError):
            rejected += 1
    return len(attacks), rejected


def validate_output(path: Path) -> Path:
    require(
        not any(part == ".." for part in path.parts),
        "output parent alias",
    )
    require(
        path.is_absolute() and path.parent == HERE,
        "output raw parent",
    )
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "output exact parent",
    )
    official = absolute.name == VERIFICATION
    replay = (
        absolute.name.startswith(f".{PREFIX}_verification_replay_")
        and absolute.name.endswith(".json")
    )
    require(official or replay, "output filename")
    require(not absolute.is_symlink(), "output symlink")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "output regular unique",
        )
    return absolute


def path_suite() -> tuple[int, int]:
    attempted = 0
    rejected = 0

    def reject_input(path: Path, maximum: int, parent: Path, name: str) -> None:
        nonlocal attempted, rejected
        attempted += 1
        try:
            secure_read(path, maximum, parent, name)
        except (VerificationError, OSError):
            rejected += 1

    def reject_output(path: Path) -> None:
        nonlocal attempted, rejected
        attempted += 1
        try:
            validate_output(path)
        except (VerificationError, OSError):
            rejected += 1

    with tempfile.TemporaryDirectory(prefix=".round219_path_", dir=HERE) as raw:
        root = Path(raw)
        valid = root / "candidate.json"
        valid.write_bytes(b"{}\n")
        require(secure_read(valid, 1024, root, valid.name) == b"{}\n",
                "path control")
        symlink = root / "symlink.json"
        symlink.symlink_to(valid)
        reject_input(symlink, 1024, root, symlink.name)
        target = root / "target.json"
        target.write_bytes(b"{}\n")
        hard = root / "hard.json"
        os.link(target, hard)
        reject_input(hard, 1024, root, hard.name)
        directory = root / "directory.json"
        directory.mkdir()
        reject_input(directory, 1024, root, directory.name)
        fifo = root / "fifo.json"
        os.mkfifo(fifo)
        reject_input(fifo, 1024, root, fifo.name)
        empty = root / "empty.json"
        empty.write_bytes(b"")
        reject_input(empty, 1024, root, empty.name)
        large = root / "large.json"
        with large.open("wb") as handle:
            handle.truncate(1025)
        reject_input(large, 1024, root, large.name)
        reject_input(valid, 1024, root, "wrong.json")
        reject_input(valid, 1024, HERE, valid.name)
        reject_input(root / ".." / valid.name, 1024, root, valid.name)
        reject_input(root / "missing.json", 1024, root, "missing.json")
        input_parent_alias = root / "input_parent_alias"
        input_parent_alias.symlink_to(root, target_is_directory=True)
        reject_input(
            input_parent_alias / valid.name,
            1024,
            root,
            valid.name,
        )

        token = str(os.getpid())
        cleanup: list[Path] = []
        output_parent_alias = root / "output_parent_alias"
        output_parent_alias.symlink_to(HERE, target_is_directory=True)
        reject_output(
            output_parent_alias
            / f".{PREFIX}_verification_replay_parent_alias_{token}.json"
        )
        reject_output(
            HERE / ".." / HERE.name
            / f".{PREFIX}_verification_replay_dotdot_{token}.json"
        )
        output_symlink = HERE / (
            f".{PREFIX}_verification_replay_symlink_{token}.json"
        )
        output_symlink.symlink_to(valid)
        cleanup.append(output_symlink)
        reject_output(output_symlink)
        output_target = HERE / (
            f".{PREFIX}_verification_replay_target_{token}.json"
        )
        output_target.write_bytes(b"{}\n")
        output_hard = HERE / (
            f".{PREFIX}_verification_replay_hard_{token}.json"
        )
        os.link(output_target, output_hard)
        cleanup.extend([output_hard, output_target])
        reject_output(output_hard)
        output_fifo = HERE / (
            f".{PREFIX}_verification_replay_fifo_{token}.json"
        )
        os.mkfifo(output_fifo)
        cleanup.append(output_fifo)
        reject_output(output_fifo)
        reject_output(
            root / f".{PREFIX}_verification_replay_nested_{token}.json"
        )
        wrong = HERE / f".round219_wrong_{token}.json"
        wrong.write_bytes(b"{}\n")
        cleanup.append(wrong)
        reject_output(wrong)
        output_dir = HERE / (
            f".{PREFIX}_verification_replay_directory_{token}.json"
        )
        output_dir.mkdir()
        cleanup.append(output_dir)
        reject_output(output_dir)
        for path in reversed(cleanup):
            if path.is_symlink() or path.is_file() or stat.S_ISFIFO(
                path.lstat().st_mode
            ):
                path.unlink()
            else:
                path.rmdir()
    return attempted, rejected


def safe_write(path: Path, data: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{PREFIX}.verify.tmp.", dir=HERE
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
    parser.add_argument("--output", type=Path, default=HERE / VERIFICATION)
    arguments = parser.parse_args()
    verifier_sha = hashlib.sha256(
        secure_read(
            HERE / Path(__file__).name,
            5_000_000,
            HERE,
            Path(__file__).name,
        )
    ).hexdigest()
    pinned(HERE / PRODUCER, PRODUCER_SHA256, 5_000_000)

    # Expected state is complete before the candidate certificate is loaded.
    expected = rebuild_expected()
    print("Round219 verifier now loading candidate", file=sys.stderr)
    raw_candidate = pinned(
        HERE / CERTIFICATE, CERTIFICATE_SHA256, 160_000_000
    )
    envelope = strict_json(raw_candidate)
    require(envelope["result_sha256"] == RESULT_SHA256,
            "candidate result pin")
    verify_envelope(envelope, expected)

    semantic_attempted, semantic_rejected = semantic_suite(
        envelope, expected
    )
    json_attempted, json_rejected = json_suite(envelope)
    path_attempted, path_rejected = path_suite()
    print(
        f"Round219 hostile semantic={semantic_rejected}/{semantic_attempted} "
        f"JSON={json_rejected}/{json_attempted} "
        f"path={path_rejected}/{path_attempted}",
        file=sys.stderr,
    )
    require(
        semantic_attempted == semantic_rejected == 21
        and json_attempted == json_rejected == 15
        and path_attempted == path_rejected == 19,
        "hostile suites",
    )
    result = {
        "status": "PASS_PARTIAL_FORMAL_ROUND219",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": RESULT_SHA256,
        "verifier_sha256": verifier_sha,
        "producer_imported_or_executed": False,
        "candidate_loaded_after_expected_reconstruction": True,
        "full_expected_Python_object_equality": True,
        "full_expected_canonical_equality": True,
        "terminal_subface_rows_verified": TERMINAL_SUBFACES,
        "TRACE_subfaces_verified": TRACE_SUBFACES,
        "ABSENT_subfaces_verified": ABSENT_SUBFACES,
        "UNRESOLVED_subfaces_verified": UNRESOLVED_SUBFACES,
        "complete_exact_contacts_verified": COMPLETE_CONTACTS,
        "remaining_exact_contacts_verified": REMAINING_CONTACTS,
        "partial_absence_rows_verified": PARTIAL_ABSENT,
        "remaining_partial_rows_verified": PARTIAL_REMAINING,
        "semantic_resigned_attacks_attempted": semantic_attempted,
        "semantic_resigned_attacks_rejected": semantic_rejected,
        "strict_JSON_attacks_attempted": json_attempted,
        "strict_JSON_attacks_rejected": json_rejected,
        "filesystem_path_attacks_attempted": path_attempted,
        "filesystem_path_attacks_rejected": path_rejected,
        "AST_duplicate_literal_key_count": 0,
        "formal_component_deduplication_credit": 0,
        "whole_leaf_credit": 0,
        "whole_origin_credit": 0,
        "whole_original_tube_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
        "D02": "UNCHANGED_BLOCKED",
        "Gate5": "UNCHANGED_10/18",
        "CM2": "UNCHANGED_NO_GO",
    }
    output = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical(output) + b"\n")
    print(output["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
