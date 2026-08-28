#!/usr/bin/env python3
"""Formal analytic-root stratification of all remaining partial contacts.

Round224 consumes the exact 236 Round219 partial contacts that remain
UNRESOLVED after the 28 certified zero-absence contacts.  For each remaining
overlap rectangle it selects the pinned strict graph-axis attempt, isolates
the unique zero on the ambiguous graph-endpoint edge, and replaces the old
partial rectangle by two open two-dimensional root sides, one one-dimensional
root slice, and one zero-dimensional root point.

An analytic root is never represented by a floating approximation.  Its exact
identity is the unique zero of a pinned analytic edge function on a closed
rational isolating interval with opposite strict endpoint signs and a strict
full-interval transverse derivative.
"""

from __future__ import annotations

import argparse
from collections import Counter
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
import cm2_round219_source_g_partial_face_common_refinement_glue as r219


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round224_source_g_partial_face_analytic_root_stratification"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = (
    "cm2.round224.source-g-partial-face-analytic-root-stratification.v1"
)
STATUS = (
    "CERTIFIED_ALL_236_REMAINING_PARTIAL_CONTACTS_BY_EXACT_ANALYTIC_"
    "BOUNDARY_ROOT_STRATIFICATION__PHYSICAL_COMPONENT_QUOTIENT_INCOMPLETE"
)
VERDICT = (
    "FORMAL_ALL_264_PARTIAL_FACE_CONTACTS_COMPLETE__28_INHERITED_ZERO_"
    "ABSENCES_PLUS_236_SYMBOLIC_ROOT_STRATIFICATIONS__NO_PARTIAL_CONTACT_"
    "REMAINS"
)

R186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
R186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)
R219_SOURCE = (
    "cm2_round219_source_g_partial_face_common_refinement_glue.py"
)
R219_CERTIFICATE = (
    "cm2_round219_source_g_partial_face_common_refinement_glue"
    "_certificate.json"
)
R219_MANIFEST = (
    "cm2_round219_source_g_partial_face_common_refinement_glue"
    "_manifest.sha256"
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
R219_MANIFEST_SHA256 = (
    "67470c6f9503bc5707135901a878fefc7086ac33caae4b578280dd0e6b5c2b9f"
)
R223_SOURCE = (
    "cm2_round223_source_g_analytic_endpoint_root_stratification.py"
)
R223_CERTIFICATE = (
    "cm2_round223_source_g_analytic_endpoint_root_stratification"
    "_certificate.json"
)
R223_MANIFEST = (
    "cm2_round223_source_g_analytic_endpoint_root_stratification"
    "_manifest.sha256"
)
R223_SOURCE_SHA256 = (
    "fb5d46a31857cb09c2606747d4fbec996eecffdf65702431a17624a2260ad970"
)
R223_CERTIFICATE_SHA256 = (
    "3d28f097419e11bde6733462736fcb70cd0164b18ac06a793a34b5dc26113168"
)
R223_RESULT_SHA256 = (
    "db012bb2e68176c8a5c144455bac9ff780521bbfa3c03110694390c70a3343d9"
)
R223_MANIFEST_SHA256 = (
    "24e27aee7ffe90cfe41fb3a1589849b8258f63dc62c5a7e5a1ba7ac05526f1d2"
)

STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
ROUND219_PARTIAL_CONTACTS = 264
INHERITED_PARTIAL_ABSENCES = 28
REMAINING_PARTIAL_CONTACTS = 236
FIXED_P_CONTACTS = 128
FIXED_T_CONTACTS = 108
PARTITIONS = 236
TERMINALS = 236
ROOTS = 236
STRATA = 944
TWO_DIMENSIONAL_STRATA = 472
TRACE_STRATA = 236
ABSENT_STRATA = 236
ROOT_SLICES = 236
ROOT_POINTS = 236
JOINS = 236
COMPLETED_CONTACTS = 236
MAX_ADAPTIVE_DEPTH = 5
SOURCE_G_KEYS = 224_580
MAX_INPUT_BYTES = 180_000_000


class Round224Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round224Error(label)


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
    result = copy.deepcopy(payload)
    result["row_sha256"] = digest(result)
    return result


def identifier(kind: str, identity: dict[str, Any]) -> str:
    return f"round224-{kind}:{digest(identity)}"


def ledger(rows: list[dict[str, Any]], id_key: str) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def secure_read(path: Path, maximum: int, name: str) -> bytes:
    require(
        not any(part == ".." for part in path.parts),
        "input parent alias",
    )
    require(
        path.is_absolute() and path.parent == HERE and path.name == name,
        "input raw path",
    )
    path = Path(os.path.abspath(os.fspath(path)))
    require(
        path.parent == HERE and path.parent.resolve() == HERE,
        "input exact parent",
    )
    before = path.lstat()
    require(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1,
        f"single-link regular input:{name}",
    )
    require(0 < before.st_size <= maximum, f"bounded input:{name}")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
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
            f"stable input open:{name}",
        )
        parts: list[bytes] = []
        total = 0
        while True:
            part = os.read(descriptor, 1024 * 1024)
            if not part:
                break
            total += len(part)
            require(total <= maximum, f"bounded input read:{name}")
            parts.append(part)
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
            f"stable input read:{name}",
        )
        return b"".join(parts)
    finally:
        os.close(descriptor)


def pinned(path: Path, expected: str, maximum: int) -> bytes:
    raw = secure_read(path, maximum, path.name)
    require(
        hashlib.sha256(raw).hexdigest() == expected,
        f"SHA256:{path.name}",
    )
    return raw


def reject_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def validate_scalars(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            require(
                all(ord(character) >= 0x20 for character in key),
                "JSON key control character",
            )
            validate_scalars(item)
    elif isinstance(value, list):
        for item in value:
            validate_scalars(item)
    elif isinstance(value, str):
        require(
            all(ord(character) >= 0x20 for character in value),
            "JSON string control character",
        )


def strict_json(raw: bytes) -> dict[str, Any]:
    require(0 < len(raw) <= MAX_INPUT_BYTES, "JSON bounded size")
    require(not raw.startswith(b"\xef\xbb\xbf"), "JSON BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Round224Error("JSON UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_pairs,
            parse_constant=lambda token: (
                (_ for _ in ()).throw(
                    Round224Error(f"JSON constant:{token}")
                )
            ),
        )
    except json.JSONDecodeError as error:
        raise Round224Error("strict JSON parse") from error
    require(isinstance(value, dict), "JSON top object")
    validate_scalars(value)
    require(raw == canonical(value) + b"\n", "canonical JSON bytes")
    return value


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
        f"ledger closure:{id_key}",
    )
    for row in rows:
        payload = dict(row)
        row_hash = payload.pop("row_sha256")
        require(digest(payload) == row_hash, f"row closure:{id_key}")
    return rows


def opposite(sign: str) -> str:
    require(sign in STRICT_SIGNS, "strict sign")
    return (
        "STRICT_POSITIVE"
        if sign == "STRICT_NEGATIVE"
        else "STRICT_NEGATIVE"
    )


def selected_value_proof(
    chart: str,
    target: str,
    active: str,
    box: Any,
) -> dict[str, str]:
    direct_value = r186.factor_geometry(chart, target, box)[active][0]
    centered_value = r186.centered_value(
        chart, target, box, active
    )
    direct_sign = r186.r179.arb_sign(direct_value)
    centered_sign = r186.r179.arb_sign(centered_value)
    selected_sign = (
        direct_sign if direct_sign in STRICT_SIGNS else centered_sign
    )
    return {
        "direct_value": str(direct_value),
        "centered_value": str(centered_value),
        "direct_sign": direct_sign,
        "centered_sign": centered_sign,
        "selected_sign": selected_sign,
    }


def graph_contract(
    partial_row: dict[str, Any],
) -> tuple[str, str, tuple[Q, Q], tuple[Q, Q], list[str]]:
    fixed_axis = partial_row["fixed_axis"]
    attempts = partial_row["graph_axis_attempts"]
    if fixed_axis == "p":
        graph_axis = "t"
        transverse_axis = "s"
    else:
        require(fixed_axis == "t", "partial fixed p/t axis")
        graph_axis = "p"
        transverse_axis = "s"
    attempt = attempts[0]
    signs = attempt["selected_lower_upper_derivative_signs"]
    require(
        attempt["graph_axis"] == graph_axis
        and signs[2] in STRICT_SIGNS
        and (
            (signs[0] in STRICT_SIGNS)
            ^ (signs[1] in STRICT_SIGNS)
        ),
        "one ambiguous graph endpoint and strict graph derivative",
    )
    overlaps = partial_row["positive_overlap_intervals"]
    graph_interval = tuple(Q(value) for value in overlaps[0])
    transverse_interval = tuple(Q(value) for value in overlaps[1])
    return (
        graph_axis,
        transverse_axis,
        graph_interval,
        transverse_interval,
        signs,
    )


def edge_box(
    partial_row: dict[str, Any],
    graph_coordinate: Q,
    lower: Q,
    upper: Q,
    label: str,
) -> tuple[Any, int]:
    atlas = r186.r179.r174.atlas.AtlasBox
    fixed_coordinate = Q(partial_row["shared_coordinate"])
    if partial_row["fixed_axis"] == "p":
        return (
            atlas(
                graph_coordinate,
                graph_coordinate,
                fixed_coordinate,
                fixed_coordinate,
                lower,
                upper,
                0,
                label,
            ),
            2,
        )
    require(partial_row["fixed_axis"] == "t", "partial fixed t edge")
    return (
        atlas(
            fixed_coordinate,
            fixed_coordinate,
            graph_coordinate,
            graph_coordinate,
            lower,
            upper,
            0,
            label,
        ),
        2,
    )


def edge_interval_proof(
    partial_row: dict[str, Any],
    frontier: dict[str, Any],
    evaluator: tuple[str, str, str],
    path: str,
    depth: int,
    interval: tuple[Q, Q],
) -> dict[str, Any]:
    (
        graph_axis,
        transverse_axis,
        graph_interval,
        _original_transverse,
        graph_signs,
    ) = graph_contract(partial_row)
    graph_endpoint = (
        "LOWER" if graph_signs[0] not in STRICT_SIGNS else "UPPER"
    )
    graph_coordinate = graph_interval[
        0 if graph_endpoint == "LOWER" else 1
    ]
    lower, upper = interval
    full_box, derivative_index = edge_box(
        partial_row,
        graph_coordinate,
        lower,
        upper,
        f"round224-edge-full:{partial_row['partial_contact_row_id']}:{path}",
    )
    lower_box, _ = edge_box(
        partial_row,
        graph_coordinate,
        lower,
        lower,
        f"round224-edge-lower:{partial_row['partial_contact_row_id']}:{path}",
    )
    upper_box, _ = edge_box(
        partial_row,
        graph_coordinate,
        upper,
        upper,
        f"round224-edge-upper:{partial_row['partial_contact_row_id']}:{path}",
    )
    chart, target, active = evaluator
    full = r186.factor_geometry(chart, target, full_box)[active]
    full_value_sign = r186.r179.arb_sign(full[0])
    derivative = full[1][derivative_index]
    derivative_sign = (
        "DERIVATIVE_UNAVAILABLE"
        if derivative is None
        else r186.r179.arb_sign(derivative)
    )
    lower_proof = selected_value_proof(
        chart, target, active, lower_box
    )
    upper_proof = selected_value_proof(
        chart, target, active, upper_box
    )
    lower_sign = lower_proof["selected_sign"]
    upper_sign = upper_proof["selected_sign"]
    if full_value_sign in STRICT_SIGNS:
        classification = "STRICT_INTERVAL_ZERO_ABSENT"
    elif (
        derivative_sign in STRICT_SIGNS
        and lower_sign in STRICT_SIGNS
        and upper_sign in STRICT_SIGNS
    ):
        classification = (
            "UNIQUE_INTERIOR_ROOT"
            if lower_sign != upper_sign
            else "STRICT_MONOTONE_ZERO_ABSENT"
        )
    else:
        classification = "UNRESOLVED"
    witness = {
        "full_edge_value": str(full[0]),
        "full_edge_value_sign": full_value_sign,
        "full_transverse_derivative":
            None if derivative is None else str(derivative),
        "full_transverse_derivative_sign": derivative_sign,
        "lower_endpoint": lower_proof,
        "upper_endpoint": upper_proof,
    }
    identity = {
        "Round219_partial_contact_row_id":
            partial_row["partial_contact_row_id"],
        "edge_dyadic_path": path,
        "edge_depth": depth,
        "edge_interval": [str(lower), str(upper)],
    }
    return closed({
        "partial_edge_terminal_segment_row_id":
            identifier("partial-edge-terminal-segment", identity),
        **identity,
        "Round219_partial_contact_row_sha256":
            partial_row["row_sha256"],
        "Round217_frontier_row_id":
            partial_row["Round217_frontier_row_id"],
        "Round217_frontier_row_sha256":
            partial_row["Round217_frontier_row_sha256"],
        "fixed_axis": partial_row["fixed_axis"],
        "fixed_coordinate": partial_row["shared_coordinate"],
        "graph_axis": graph_axis,
        "transverse_axis": transverse_axis,
        "graph_interval": [str(value) for value in graph_interval],
        "graph_endpoint": graph_endpoint,
        "graph_endpoint_coordinate": str(graph_coordinate),
        "source_chart": chart,
        "target_lift": target,
        "active_factor": active,
        "classification": classification,
        "full_edge_value_sign": full_value_sign,
        "full_transverse_derivative_sign": derivative_sign,
        "lower_transverse_endpoint_sign": lower_sign,
        "upper_transverse_endpoint_sign": upper_sign,
        "proof_witness_sha256": digest(witness),
        "unique_root_requires_opposite_strict_endpoint_signs_and_"
        "strict_full_transverse_derivative": True,
        "formal_partial_edge_unique_root_credit":
            int(classification == "UNIQUE_INTERIOR_ROOT"),
        "formal_partial_edge_zero_absence_credit":
            int(classification.endswith("ZERO_ABSENT")),
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def edge_partition(
    partial_row: dict[str, Any],
    frontier: dict[str, Any],
    evaluator: tuple[str, str, str],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    (
        graph_axis,
        transverse_axis,
        graph_interval,
        original,
        _graph_signs,
    ) = graph_contract(partial_row)
    direct = edge_interval_proof(
        partial_row, frontier, evaluator, "", 0, original
    )
    if direct["classification"] != "UNRESOLVED":
        terminals = [direct]
        method = "DIRECT_FULL_EDGE_MONOTONE_OR_INTERVAL"
        completion_depth = 0
    else:
        active = [("", original)]
        terminals: list[dict[str, Any]] = []
        completion_depth: int | None = None
        for depth in range(1, MAX_ADAPTIVE_DEPTH + 1):
            following: list[tuple[str, tuple[Q, Q]]] = []
            for path, (lower, upper) in active:
                midpoint = (lower + upper) / 2
                for suffix, interval in (
                    ("L", (lower, midpoint)),
                    ("R", (midpoint, upper)),
                ):
                    child = edge_interval_proof(
                        partial_row,
                        frontier,
                        evaluator,
                        path + suffix,
                        depth,
                        interval,
                    )
                    if child["classification"] == "UNRESOLVED":
                        following.append((path + suffix, interval))
                    else:
                        terminals.append(child)
            active = following
            if not active:
                completion_depth = depth
                break
        require(
            not active and completion_depth is not None,
            "adaptive partial edge partition closes",
        )
        method = "ADAPTIVE_RATIONAL_EDGE_PARTITION"

    terminals.sort(
        key=lambda item: (
            Q(item["edge_interval"][0]),
            Q(item["edge_interval"][1]),
            item["edge_dyadic_path"],
        )
    )
    require(
        terminals[0]["edge_interval"][0] == str(original[0])
        and terminals[-1]["edge_interval"][1] == str(original[1])
        and all(
            terminals[index]["edge_interval"][1]
            == terminals[index + 1]["edge_interval"][0]
            for index in range(len(terminals) - 1)
        ),
        "partial edge terminal exact union",
    )
    for ordinal, terminal in enumerate(terminals, 1):
        terminal.pop("row_sha256")
        terminal["terminal_partition_ordinal"] = ordinal
        terminal["terminal_partition_count"] = len(terminals)
        terminal["owned_lower_closed"] = True
        terminal["owned_upper_closed"] = ordinal == len(terminals)
        terminal["row_sha256"] = digest(terminal)
    counts = Counter(
        terminal["classification"] for terminal in terminals
    )
    require(
        counts["UNIQUE_INTERIOR_ROOT"] == 1
        and counts["UNRESOLVED"] == 0,
        "one partial boundary root and no unresolved",
    )
    root_terminal = next(
        terminal
        for terminal in terminals
        if terminal["classification"] == "UNIQUE_INTERIOR_ROOT"
    )
    identity = {
        "Round219_partial_contact_row_id":
            partial_row["partial_contact_row_id"],
        "Round219_partial_contact_row_sha256":
            partial_row["row_sha256"],
    }
    return closed({
        "partial_endpoint_edge_partition_row_id":
            identifier("partial-endpoint-edge-partition", identity),
        **identity,
        "Round217_frontier_row_id":
            partial_row["Round217_frontier_row_id"],
        "fixed_axis": partial_row["fixed_axis"],
        "fixed_coordinate": partial_row["shared_coordinate"],
        "graph_axis": graph_axis,
        "transverse_axis": transverse_axis,
        "graph_interval": [str(value) for value in graph_interval],
        "original_transverse_interval": [
            str(value) for value in original
        ],
        "partition_method": method,
        "adaptive_completion_depth": completion_depth,
        "terminal_edge_segment_count": len(terminals),
        "unique_interior_root_terminal_count":
            counts["UNIQUE_INTERIOR_ROOT"],
        "zero_absence_terminal_count":
            len(terminals) - counts["UNIQUE_INTERIOR_ROOT"],
        "root_edge_terminal_segment_row_id":
            root_terminal["partial_edge_terminal_segment_row_id"],
        "root_edge_terminal_segment_row_sha256":
            root_terminal["row_sha256"],
        "terminal_edge_segments_sha256": digest([
            [
                terminal["partial_edge_terminal_segment_row_id"],
                terminal["row_sha256"],
            ]
            for terminal in terminals
        ]),
        "terminal_partition_exact_union_of_original_edge": True,
        "terminal_partition_has_no_gap": True,
        "terminal_partition_has_no_owned_overlap": True,
        "edge_root_set_complete": True,
        "formal_partial_edge_partition_complete_credit": 1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }), terminals


def analytic_root_row(
    partial_row: dict[str, Any],
    frontier: dict[str, Any],
    evaluator: tuple[str, str, str],
    partition: dict[str, Any],
    terminal: dict[str, Any],
) -> dict[str, Any]:
    require(
        terminal["classification"] == "UNIQUE_INTERIOR_ROOT"
        and terminal["lower_transverse_endpoint_sign"]
        != terminal["upper_transverse_endpoint_sign"]
        and terminal["full_transverse_derivative_sign"] in STRICT_SIGNS,
        "partial analytic root proof",
    )
    chart, target, active = evaluator
    function_identity = {
        "source_chart": chart,
        "target_lift": target,
        "active_factor": active,
        "fixed_axis": partial_row["fixed_axis"],
        "fixed_coordinate": partial_row["shared_coordinate"],
        "graph_axis": partition["graph_axis"],
        "graph_endpoint": terminal["graph_endpoint"],
        "graph_endpoint_coordinate":
            terminal["graph_endpoint_coordinate"],
        "transverse_axis": partition["transverse_axis"],
    }
    identity = {
        "analytic_function_identity_sha256": digest(function_identity),
        "carrier_Round219_partial_contact_row_id":
            partial_row["partial_contact_row_id"],
        "isolating_rational_interval":
            copy.deepcopy(terminal["edge_interval"]),
        "isolating_edge_terminal_segment_row_id":
            terminal["partial_edge_terminal_segment_row_id"],
    }
    return closed({
        "partial_analytic_root_row_id":
            identifier("partial-analytic-boundary-root", identity),
        **identity,
        "partial_endpoint_edge_partition_row_id":
            partition["partial_endpoint_edge_partition_row_id"],
        "Round219_partial_contact_row_sha256":
            partial_row["row_sha256"],
        "Round217_frontier_row_id":
            partial_row["Round217_frontier_row_id"],
        "source_chart": chart,
        "target_lift": target,
        "active_factor": active,
        "fixed_axis": partial_row["fixed_axis"],
        "fixed_coordinate": partial_row["shared_coordinate"],
        "graph_axis": partition["graph_axis"],
        "graph_endpoint": terminal["graph_endpoint"],
        "graph_endpoint_coordinate":
            terminal["graph_endpoint_coordinate"],
        "transverse_axis": partition["transverse_axis"],
        "isolating_edge_dyadic_path":
            terminal["edge_dyadic_path"],
        "isolating_edge_depth": terminal["edge_depth"],
        "lower_isolating_endpoint_sign":
            terminal["lower_transverse_endpoint_sign"],
        "upper_isolating_endpoint_sign":
            terminal["upper_transverse_endpoint_sign"],
        "strict_full_transverse_derivative_sign":
            terminal["full_transverse_derivative_sign"],
        "proof_witness_sha256": terminal["proof_witness_sha256"],
        "coordinate_representation":
            "EXACT_ANALYTIC_UNIQUE_ROOT_NOT_NUMERIC_APPROXIMATION",
        "exact_definition":
            "THE_UNIQUE_ZERO_OF_THE_PINNED_ANALYTIC_PARTIAL_BOUNDARY_"
            "EDGE_FUNCTION_ON_THE_CLOSED_RATIONAL_ISOLATING_INTERVAL",
        "root_is_strictly_inside_isolating_interval": True,
        "root_is_simple_by_strict_full_transverse_derivative": True,
        "root_set_on_original_edge_is_complete_by_exact_terminal_"
        "partition": True,
        "formal_partial_analytic_root_credit": 1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def trace_ids(
    stratum_id: str,
    partial_row: dict[str, Any],
) -> tuple[str, str, str, str]:
    curve = identifier(
        "partial-open-strip-zero-curve",
        {"stratum_row_id": stratum_id},
    )
    negative = identifier(
        "negative-partial-open-strip-incidence",
        {
            "zero_curve_row_id": curve,
            "leaf_row_id": partial_row["negative_leaf_row_id"],
        },
    )
    positive = identifier(
        "positive-partial-open-strip-incidence",
        {
            "zero_curve_row_id": curve,
            "leaf_row_id": partial_row["positive_leaf_row_id"],
        },
    )
    glue = identifier(
        "partial-open-strip-glue",
        {
            "zero_curve_row_id": curve,
            "negative_incidence_row_id": negative,
            "positive_incidence_row_id": positive,
        },
    )
    return curve, negative, positive, glue


def root_point_coordinates(
    partial_row: dict[str, Any],
    root: dict[str, Any],
) -> dict[str, str]:
    if partial_row["fixed_axis"] == "p":
        return {
            "t": root["graph_endpoint_coordinate"],
            "p": partial_row["shared_coordinate"],
            "s": "ANALYTIC_ROOT",
        }
    return {
        "t": partial_row["shared_coordinate"],
        "p": root["graph_endpoint_coordinate"],
        "s": "ANALYTIC_ROOT",
    }


def root_strata(
    partial_row: dict[str, Any],
    root: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root_id = root["partial_analytic_root_row_id"]
    graph_endpoint = root["graph_endpoint"]
    transverse_derivative_sign = root[
        "strict_full_transverse_derivative_sign"
    ]
    lower_edge_sign = root["lower_isolating_endpoint_sign"]
    upper_edge_sign = root["upper_isolating_endpoint_sign"]
    require(
        (
            transverse_derivative_sign == "STRICT_POSITIVE"
            and lower_edge_sign == "STRICT_NEGATIVE"
            and upper_edge_sign == "STRICT_POSITIVE"
        )
        or (
            transverse_derivative_sign == "STRICT_NEGATIVE"
            and lower_edge_sign == "STRICT_POSITIVE"
            and upper_edge_sign == "STRICT_NEGATIVE"
        ),
        "partial root side signs agree with monotonicity",
    )
    graph_signs = partial_row["graph_axis_attempts"][0][
        "selected_lower_upper_derivative_signs"
    ]
    other_graph_sign = (
        graph_signs[1]
        if graph_endpoint == "LOWER"
        else graph_signs[0]
    )
    graph_derivative_sign = graph_signs[2]
    require(
        other_graph_sign in STRICT_SIGNS
        and graph_derivative_sign in STRICT_SIGNS,
        "partial other graph endpoint and derivative strict",
    )
    strata: list[dict[str, Any]] = []
    trace_stratum: dict[str, Any] | None = None
    for side, edge_sign, relation in (
        (
            "LOWER_ROOT_SIDE",
            lower_edge_sign,
            "TRANSVERSE_COORDINATE_STRICTLY_LESS_THAN_ANALYTIC_ROOT",
        ),
        (
            "UPPER_ROOT_SIDE",
            upper_edge_sign,
            "TRANSVERSE_COORDINATE_STRICTLY_GREATER_THAN_ANALYTIC_ROOT",
        ),
    ):
        selected_graph_signs = (
            [edge_sign, other_graph_sign, graph_derivative_sign]
            if graph_endpoint == "LOWER"
            else [other_graph_sign, edge_sign, graph_derivative_sign]
        )
        classification = (
            "TRACE"
            if selected_graph_signs[0] != selected_graph_signs[1]
            else "ABSENT"
        )
        identity = {
            "partial_analytic_root_row_id": root_id,
            "stratum_kind":
                "TWO_DIMENSIONAL_PARTIAL_OPEN_ROOT_SIDE",
            "root_side": side,
        }
        stratum_id = identifier("partial-symbolic-stratum", identity)
        if classification == "TRACE":
            curve, negative, positive, glue = trace_ids(
                stratum_id, partial_row
            )
        else:
            curve = negative = positive = glue = None
        stratum = closed({
            "partial_symbolic_stratum_row_id": stratum_id,
            **identity,
            "Round219_partial_contact_row_id":
                partial_row["partial_contact_row_id"],
            "Round219_partial_contact_row_sha256":
                partial_row["row_sha256"],
            "Round217_frontier_row_id":
                partial_row["Round217_frontier_row_id"],
            "topological_dimension": 2,
            "fixed_axis": partial_row["fixed_axis"],
            "fixed_coordinate": partial_row["shared_coordinate"],
            "graph_axis": root["graph_axis"],
            "graph_interval":
                copy.deepcopy(partial_row["positive_overlap_intervals"][0]),
            "transverse_axis": root["transverse_axis"],
            "transverse_domain_relation": relation,
            "root_boundary_coordinate_representation":
                "EXACT_ANALYTIC_ROOT_ID",
            "selected_lower_upper_graph_derivative_signs":
                selected_graph_signs,
            "classification": classification,
            "classification_derived_from_strict_root_monotonicity": True,
            "restricted_zero_curve_row_id": curve,
            "negative_side_incidence_row_id": negative,
            "negative_side_leaf_row_id":
                partial_row["negative_leaf_row_id"],
            "positive_side_incidence_row_id": positive,
            "positive_side_leaf_row_id":
                partial_row["positive_leaf_row_id"],
            "exact_partial_common_refinement_glue_row_id": glue,
            "formal_two_dimensional_partial_trace_stratum_credit":
                int(classification == "TRACE"),
            "formal_two_dimensional_partial_zero_absence_stratum_credit":
                int(classification == "ABSENT"),
            "formal_local_partial_incidence_credit":
                2 * int(classification == "TRACE"),
            "formal_local_partial_glue_credit":
                int(classification == "TRACE"),
            "formal_component_deduplication_credit": 0,
            "whole_origin_credit": 0,
            "global_component_credit": 0,
            "global_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        strata.append(stratum)
        if classification == "TRACE":
            require(
                trace_stratum is None,
                "one partial TRACE side per root",
            )
            trace_stratum = stratum
    require(trace_stratum is not None, "partial root has one TRACE side")

    interior_sign = (
        graph_derivative_sign
        if graph_endpoint == "LOWER"
        else opposite(graph_derivative_sign)
    )
    slice_identity = {
        "partial_analytic_root_row_id": root_id,
        "stratum_kind":
            "ONE_DIMENSIONAL_PARTIAL_ROOT_SLICE_WITH_ROOT_POINT_REMOVED",
    }
    slice_id = identifier("partial-symbolic-stratum", slice_identity)
    strata.append(closed({
        "partial_symbolic_stratum_row_id": slice_id,
        **slice_identity,
        "Round219_partial_contact_row_id":
            partial_row["partial_contact_row_id"],
        "Round219_partial_contact_row_sha256":
            partial_row["row_sha256"],
        "Round217_frontier_row_id":
            partial_row["Round217_frontier_row_id"],
        "topological_dimension": 1,
        "fixed_axis": partial_row["fixed_axis"],
        "fixed_coordinate": partial_row["shared_coordinate"],
        "transverse_axis": root["transverse_axis"],
        "transverse_coordinate": "ANALYTIC_ROOT",
        "graph_axis": root["graph_axis"],
        "graph_domain":
            "GRAPH_INTERVAL_WITH_THE_ROOT_ENDPOINT_REMOVED",
        "strict_interior_active_factor_sign": interior_sign,
        "strict_graph_derivative_sign": graph_derivative_sign,
        "classification":
            "PARTIAL_ROOT_SLICE_ZERO_ABSENT_AWAY_FROM_ROOT_POINT",
        "formal_one_dimensional_partial_root_slice_zero_absence_credit":
            1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }))

    point_identity = {
        "partial_analytic_root_row_id": root_id,
        "stratum_kind":
            "ZERO_DIMENSIONAL_PARTIAL_BOUNDARY_ROOT_POINT",
    }
    point_id = identifier("partial-symbolic-stratum", point_identity)
    join_identity = {
        "partial_analytic_root_row_id": root_id,
        "root_point_stratum_row_id": point_id,
        "trace_stratum_row_id":
            trace_stratum["partial_symbolic_stratum_row_id"],
        "restricted_zero_curve_row_id":
            trace_stratum["restricted_zero_curve_row_id"],
    }
    join_id = identifier(
        "partial-endpoint-to-curve-join", join_identity
    )
    point = closed({
        "partial_symbolic_stratum_row_id": point_id,
        **point_identity,
        "Round219_partial_contact_row_id":
            partial_row["partial_contact_row_id"],
        "Round219_partial_contact_row_sha256":
            partial_row["row_sha256"],
        "Round217_frontier_row_id":
            partial_row["Round217_frontier_row_id"],
        "topological_dimension": 0,
        "exact_coordinate_map":
            root_point_coordinates(partial_row, root),
        "active_factor_is_exactly_zero_by_root_definition": True,
        "partial_endpoint_to_curve_join_row_id": join_id,
        "formal_zero_dimensional_partial_root_point_credit": 1,
        "formal_partial_endpoint_to_curve_join_credit": 1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })
    strata.append(point)
    join = closed({
        "partial_endpoint_to_curve_join_row_id": join_id,
        **join_identity,
        "root_point_stratum_row_sha256": point["row_sha256"],
        "trace_stratum_row_sha256": trace_stratum["row_sha256"],
        "Round219_partial_contact_row_id":
            partial_row["partial_contact_row_id"],
        "negative_side_leaf_row_id":
            partial_row["negative_leaf_row_id"],
        "positive_side_leaf_row_id":
            partial_row["positive_leaf_row_id"],
        "exact_restricted_evaluator_identity": True,
        "joined_from_numeric_root_approximation": False,
        "formal_partial_endpoint_to_curve_join_credit": 1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })
    return strata, join


def completion_row(
    partial_row: dict[str, Any],
    partition: dict[str, Any],
    root: dict[str, Any],
    strata: list[dict[str, Any]],
    join: dict[str, Any],
) -> dict[str, Any]:
    require(
        partition["formal_partial_edge_partition_complete_credit"] == 1
        and partition["edge_root_set_complete"] is True
        and len(strata) == 4
        and len(
            [
                row for row in strata
                if row["topological_dimension"] == 2
                and row["classification"] == "TRACE"
            ]
        ) == 1
        and len(
            [
                row for row in strata
                if row["topological_dimension"] == 2
                and row["classification"] == "ABSENT"
            ]
        ) == 1,
        "partial contact exact replacement",
    )
    identity = {
        "Round219_partial_contact_row_id":
            partial_row["partial_contact_row_id"],
        "Round219_partial_contact_row_sha256":
            partial_row["row_sha256"],
    }
    return closed({
        "completed_partial_contact_row_id":
            identifier("completed-partial-contact", identity),
        **identity,
        "Round217_frontier_row_id":
            partial_row["Round217_frontier_row_id"],
        "fixed_axis": partial_row["fixed_axis"],
        "fixed_coordinate": partial_row["shared_coordinate"],
        "negative_leaf_row_id":
            partial_row["negative_leaf_row_id"],
        "positive_leaf_row_id":
            partial_row["positive_leaf_row_id"],
        "partial_endpoint_edge_partition_row_id":
            partition["partial_endpoint_edge_partition_row_id"],
        "partial_endpoint_edge_partition_row_sha256":
            partition["row_sha256"],
        "partial_analytic_root_row_id":
            root["partial_analytic_root_row_id"],
        "partial_analytic_root_row_sha256": root["row_sha256"],
        "replacement_partial_symbolic_stratum_count": len(strata),
        "replacement_partial_symbolic_strata_sha256": digest([
            [
                row["partial_symbolic_stratum_row_id"],
                row["row_sha256"],
            ]
            for row in sorted(
                strata,
                key=lambda item:
                    item["partial_symbolic_stratum_row_id"],
            )
        ]),
        "partial_endpoint_to_curve_join_row_id":
            join["partial_endpoint_to_curve_join_row_id"],
        "partial_endpoint_to_curve_join_row_sha256":
            join["row_sha256"],
        "old_UNRESOLVED_partial_contact_exactly_replaced": True,
        "replacement_partition_exact_union_of_old_partial_overlap": True,
        "replacement_partition_has_no_gap": True,
        "replacement_partition_has_no_owned_overlap": True,
        "complete_TRACE_ABSENT_root_slice_and_root_point_stratification":
            True,
        "formal_partial_contact_symbolic_stratification_complete_credit":
            1,
        "formal_component_deduplication_credit": 0,
        "whole_leaf_credit": 0,
        "whole_origin_credit": 0,
        "whole_original_tube_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def validate_rows(
    rows: list[dict[str, Any]],
    id_key: str,
) -> None:
    require(
        len({row[id_key] for row in rows}) == len(rows),
        f"unique rows:{id_key}",
    )
    for row in rows:
        payload = dict(row)
        row_hash = payload.pop("row_sha256")
        require(digest(payload) == row_hash, f"closed row:{id_key}")


def build_result(producer_sha256: str) -> dict[str, Any]:
    require(
        Path(r219.__file__).resolve() == (HERE / R219_SOURCE).resolve()
        and Path(r186.__file__).resolve() == (HERE / R186_SOURCE).resolve(),
        "pinned module identity",
    )
    pinned(HERE / R186_SOURCE, R186_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R219_SOURCE, R219_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R219_MANIFEST, R219_MANIFEST_SHA256, 10_000)
    pinned(HERE / R223_SOURCE, R223_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R223_MANIFEST, R223_MANIFEST_SHA256, 10_000)
    raw219 = pinned(
        HERE / R219_CERTIFICATE,
        R219_CERTIFICATE_SHA256,
        MAX_INPUT_BYTES,
    )
    raw223 = pinned(
        HERE / R223_CERTIFICATE,
        R223_CERTIFICATE_SHA256,
        MAX_INPUT_BYTES,
    )
    envelope219 = strict_json(raw219)
    envelope223 = strict_json(raw223)
    require(
        set(envelope219) == {"schema", "result", "result_sha256"}
        and envelope219["result_sha256"] == R219_RESULT_SHA256
        and digest(envelope219["result"]) == R219_RESULT_SHA256,
        "Round219 result closure",
    )
    require(
        set(envelope223) == {"schema", "result", "result_sha256"}
        and envelope223["result_sha256"] == R223_RESULT_SHA256
        and digest(envelope223["result"]) == R223_RESULT_SHA256,
        "Round223 result closure",
    )
    result219 = envelope219["result"]
    result223 = envelope223["result"]
    partial219 = validate_ledger(
        result219["formal_partial_contact_probe_ledger"],
        "partial_contact_row_id",
    )
    unresolved219 = [
        row for row in partial219
        if row["classification"] == "UNRESOLVED"
    ]
    inherited_absent = [
        row for row in partial219
        if row["classification"] == "ABSENT"
    ]
    require(
        len(partial219) == ROUND219_PARTIAL_CONTACTS
        and len(inherited_absent) == INHERITED_PARTIAL_ABSENCES
        and len(unresolved219) == REMAINING_PARTIAL_CONTACTS,
        "Round219 partial frontier",
    )
    require(
        result223["formal_exact_contact_scope"][
            "cumulative_complete_exact_p_s_contact_count"
        ] == 7_932
        and result223["formal_exact_contact_scope"][
            "remaining_incomplete_exact_p_s_contact_count"
        ] == 0
        and result223["first_missing_frontier"][
            "remaining_partial_contact_count"
        ] == REMAINING_PARTIAL_CONTACTS
        and result223["first_missing_frontier"][
            "partial_contact_symbolic_root_stratification_missing"
        ] is True,
        "Round223 exact-complete partial-frontier boundary",
    )

    (
        _result217,
        _exact_frontier,
        partial_frontier,
        evaluators,
        upstream_hashes,
    ) = r219.load_boundary()
    ctx.prec = 256
    frontier_by_id = {
        row["frontier_row_id"]: row for row in partial_frontier
    }
    require(
        len(frontier_by_id) == ROUND219_PARTIAL_CONTACTS
        and all(
            row["Round217_frontier_row_id"] in frontier_by_id
            for row in unresolved219
        ),
        "Round217 partial frontier identity",
    )

    partitions: list[dict[str, Any]] = []
    terminals: list[dict[str, Any]] = []
    roots: list[dict[str, Any]] = []
    strata: list[dict[str, Any]] = []
    joins: list[dict[str, Any]] = []
    completed: list[dict[str, Any]] = []
    print(
        "Round224 building 236 partial boundary root partitions",
        file=sys.stderr,
    )
    for partial_row in unresolved219:
        frontier = frontier_by_id[
            partial_row["Round217_frontier_row_id"]
        ]
        evaluator = evaluators[partial_row["negative_leaf_row_id"]]
        require(
            evaluator == evaluators[partial_row["positive_leaf_row_id"]],
            "partial evaluator identity",
        )
        partition, child_rows = edge_partition(
            partial_row, frontier, evaluator
        )
        root_terminal = next(
            row
            for row in child_rows
            if row["classification"] == "UNIQUE_INTERIOR_ROOT"
        )
        root = analytic_root_row(
            partial_row,
            frontier,
            evaluator,
            partition,
            root_terminal,
        )
        root_side_rows, join = root_strata(partial_row, root)
        contact = completion_row(
            partial_row,
            partition,
            root,
            root_side_rows,
            join,
        )
        partitions.append(partition)
        terminals.extend(child_rows)
        roots.append(root)
        strata.extend(root_side_rows)
        joins.append(join)
        completed.append(contact)

    for rows, key in (
        (partitions, "partial_endpoint_edge_partition_row_id"),
        (terminals, "partial_edge_terminal_segment_row_id"),
        (roots, "partial_analytic_root_row_id"),
        (strata, "partial_symbolic_stratum_row_id"),
        (joins, "partial_endpoint_to_curve_join_row_id"),
        (completed, "completed_partial_contact_row_id"),
    ):
        rows.sort(key=lambda row, key=key: row[key])
        validate_rows(rows, key)

    methods = Counter(row["partition_method"] for row in partitions)
    depths = Counter(row["adaptive_completion_depth"] for row in partitions)
    terminal_classes = Counter(row["classification"] for row in terminals)
    fixed_axes = Counter(row["fixed_axis"] for row in completed)
    graph_endpoints = Counter(row["graph_endpoint"] for row in roots)
    stratum_kinds = Counter(row["stratum_kind"] for row in strata)
    dimensions = Counter(row["topological_dimension"] for row in strata)
    two_dimensional_classes = Counter(
        row["classification"]
        for row in strata
        if row["topological_dimension"] == 2
    )
    require(
        len(partitions) == PARTITIONS
        and len(terminals) == TERMINALS
        and len(roots) == ROOTS
        and len(strata) == STRATA
        and len(joins) == JOINS
        and len(completed) == COMPLETED_CONTACTS
        and methods
        == Counter({"DIRECT_FULL_EDGE_MONOTONE_OR_INTERVAL": 236})
        and depths == Counter({0: 236})
        and terminal_classes == Counter({"UNIQUE_INTERIOR_ROOT": 236})
        and fixed_axes == Counter({"p": FIXED_P_CONTACTS, "t": FIXED_T_CONTACTS})
        and graph_endpoints == Counter({"LOWER": 118, "UPPER": 118})
        and stratum_kinds[
            "TWO_DIMENSIONAL_PARTIAL_OPEN_ROOT_SIDE"
        ] == TWO_DIMENSIONAL_STRATA
        and stratum_kinds[
            "ONE_DIMENSIONAL_PARTIAL_ROOT_SLICE_WITH_ROOT_POINT_REMOVED"
        ] == ROOT_SLICES
        and stratum_kinds[
            "ZERO_DIMENSIONAL_PARTIAL_BOUNDARY_ROOT_POINT"
        ] == ROOT_POINTS
        and dimensions
        == Counter({2: 472, 1: 236, 0: 236})
        and two_dimensional_classes
        == Counter({"TRACE": TRACE_STRATA, "ABSENT": ABSENT_STRATA}),
        "Round224 formal census",
    )
    require(
        all(
            row[
                "formal_partial_contact_symbolic_stratification_complete_credit"
            ] == 1
            for row in completed
        ),
        "all remaining partial contacts complete",
    )

    return {
        "status": STATUS,
        "verdict": VERDICT,
        "formal_input_binding": {
            "Round186_factor_evaluator_source_sha256":
                R186_SOURCE_SHA256,
            "Round219_source_sha256": R219_SOURCE_SHA256,
            "Round219_certificate_sha256": R219_CERTIFICATE_SHA256,
            "Round219_result_sha256": R219_RESULT_SHA256,
            "Round219_manifest_sha256": R219_MANIFEST_SHA256,
            "Round223_source_sha256": R223_SOURCE_SHA256,
            "Round223_certificate_sha256": R223_CERTIFICATE_SHA256,
            "Round223_result_sha256": R223_RESULT_SHA256,
            "Round223_manifest_sha256": R223_MANIFEST_SHA256,
            **upstream_hashes,
            "Round223_cumulative_complete_exact_p_s_contact_count":
                7_932,
            "Round223_remaining_incomplete_exact_p_s_contact_count": 0,
            "Round219_inherited_partial_zero_absence_count":
                len(inherited_absent),
            "Round219_remaining_partial_UNRESOLVED_contact_count":
                len(unresolved219),
            "Round224_producer_outcome_or_oracle_dependency": False,
            "Round221_probe_imported_or_executed": False,
        },
        "formal_partial_analytic_root_contract": {
            "coordinate_representation":
                "EXACT_ANALYTIC_UNIQUE_ROOT_NOT_NUMERIC_APPROXIMATION",
            "root_identity_binds_analytic_function_edge_carrier_and_"
            "rational_isolating_interval": True,
            "unique_root_requires_opposite_strict_endpoint_signs": True,
            "simple_root_requires_strict_full_transverse_derivative": True,
            "adaptive_partition_splits_only_UNRESOLVED_children": True,
            "adaptive_partition_maximum_depth": MAX_ADAPTIVE_DEPTH,
            "edge_terminal_owner_rule":
                "LEFT_CLOSED_RIGHT_OPEN_EXCEPT_FINAL_RIGHT_CLOSED",
            "root_is_shared_by_both_open_sides_root_slice_and_root_point":
                True,
            "numeric_root_approximation_used_as_exact_coordinate": False,
        },
        "formal_partial_endpoint_edge_scope": {
            "partial_endpoint_edge_partition_count": len(partitions),
            "direct_unique_root_partition_count": methods[
                "DIRECT_FULL_EDGE_MONOTONE_OR_INTERVAL"
            ],
            "adaptive_unique_root_partition_count": methods[
                "ADAPTIVE_RATIONAL_EDGE_PARTITION"
            ],
            "partial_analytic_unique_root_count": len(roots),
            "terminal_partial_edge_segment_count": len(terminals),
            "terminal_unique_root_segment_count":
                terminal_classes["UNIQUE_INTERIOR_ROOT"],
            "terminal_zero_absence_segment_count": sum(
                value
                for key, value in terminal_classes.items()
                if key.endswith("ZERO_ABSENT")
            ),
            "adaptive_completion_depth_histogram": {
                str(key): value for key, value in sorted(depths.items())
            },
            "fixed_axis_count": dict(sorted(fixed_axes.items())),
            "graph_endpoint_count":
                dict(sorted(graph_endpoints.items())),
            "all_partial_endpoint_edge_root_sets_complete": True,
            "remaining_UNRESOLVED_partial_edge_segment_count": 0,
        },
        "formal_partial_symbolic_stratum_scope": {
            "partial_symbolic_stratum_count": len(strata),
            "two_dimensional_partial_open_root_side_count":
                TWO_DIMENSIONAL_STRATA,
            "two_dimensional_partial_TRACE_count":
                two_dimensional_classes["TRACE"],
            "two_dimensional_partial_ABSENT_count":
                two_dimensional_classes["ABSENT"],
            "one_dimensional_partial_root_slice_count": ROOT_SLICES,
            "zero_dimensional_partial_root_point_count": ROOT_POINTS,
            "partial_endpoint_to_curve_join_count": len(joins),
            "every_root_partition_is_left_open_side_plus_root_slice_"
            "plus_right_open_side": True,
            "root_point_is_separate_from_two_dimensional_strips": True,
            "every_old_UNRESOLVED_partial_contact_exactly_partitioned":
                True,
        },
        "formal_partial_contact_scope": {
            "Round219_partial_frontier_contact_count":
                ROUND219_PARTIAL_CONTACTS,
            "Round219_inherited_complete_zero_absence_contact_count":
                INHERITED_PARTIAL_ABSENCES,
            "new_symbolic_stratification_complete_partial_contact_count":
                len(completed),
            "cumulative_complete_partial_contact_count":
                ROUND219_PARTIAL_CONTACTS,
            "total_partial_contact_count": ROUND219_PARTIAL_CONTACTS,
            "remaining_incomplete_partial_contact_count": 0,
            "cumulative_identity": "28+236=264",
            "new_complete_fixed_axis_count":
                dict(sorted(fixed_axes.items())),
            "physical_component_equivalence_relation_complete": False,
        },
        "formal_partial_endpoint_edge_partition_ledger":
            ledger(
                partitions,
                "partial_endpoint_edge_partition_row_id",
            ),
        "formal_partial_edge_terminal_segment_ledger":
            ledger(
                terminals,
                "partial_edge_terminal_segment_row_id",
            ),
        "formal_partial_analytic_root_ledger":
            ledger(roots, "partial_analytic_root_row_id"),
        "formal_partial_symbolic_stratum_ledger":
            ledger(strata, "partial_symbolic_stratum_row_id"),
        "formal_partial_endpoint_to_curve_join_ledger":
            ledger(
                joins,
                "partial_endpoint_to_curve_join_row_id",
            ),
        "formal_completed_partial_contact_ledger":
            ledger(completed, "completed_partial_contact_row_id"),
        "first_missing_frontier": {
            "remaining_incomplete_exact_p_s_contact_count": 0,
            "remaining_partial_contact_count": 0,
            "complete_physical_component_equivalence_closure_missing":
                True,
            "Round220_cross_parent_cross_chart_transition_glues_missing":
                True,
            "global_occurrence_fibre_exhaustion_missing": True,
        },
        "formal_credit_contract": {
            "formal_partial_analytic_root_credits": len(roots),
            "formal_two_dimensional_partial_trace_stratum_credits":
                TRACE_STRATA,
            "formal_two_dimensional_partial_zero_absence_stratum_credits":
                ABSENT_STRATA,
            "formal_one_dimensional_partial_root_slice_zero_absence_credits":
                ROOT_SLICES,
            "formal_zero_dimensional_partial_root_point_credits":
                ROOT_POINTS,
            "formal_partial_endpoint_to_curve_join_credits": len(joins),
            "formal_partial_contact_symbolic_stratification_complete_credits":
                len(completed),
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
            "rebuild the certified connectivity quotient with these 236 "
            "new exact partial-contact glues, then prove the remaining "
            "Round220 cross-parent/cross-chart transition glues before "
            "claiming physical-component or global occurrence-fibre credit"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "python_flint_version":
                getattr(__import__("flint"), "__version__", "unknown"),
            "effective_Arb_precision_bits": ctx.prec,
            "producer_imported_or_executed_by_independent_verifier":
                False,
            "formal_upstream_files_modified": False,
        },
    }


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
    official = absolute.name == OUTPUT.name
    replay = (
        absolute.name.startswith(f".{PREFIX}_replay_")
        and absolute.name.endswith(".json")
    )
    require(official or replay, "output filename")
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "existing output type",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{PREFIX}.tmp.",
        suffix=".json",
        dir=HERE,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        metadata = temporary.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and not temporary.is_symlink()
            and metadata.st_nlink == 1,
            "atomic temporary type",
        )
        os.replace(temporary, destination)
        directory = os.open(
            HERE,
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        raise
    finally:
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    source_sha256 = hashlib.sha256(
        secure_read(
            HERE / Path(__file__).name,
            5_000_000,
            Path(__file__).name,
        )
    ).hexdigest()
    result = build_result(source_sha256)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical(envelope) + b"\n")
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
