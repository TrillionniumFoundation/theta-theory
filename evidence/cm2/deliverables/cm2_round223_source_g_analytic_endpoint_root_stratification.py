#!/usr/bin/env python3
"""Formal symbolic endpoint-root stratification of the Round219 frontier.

No numerical approximation is used as an exact coordinate.  Each promoted
root is represented by the identity of an analytic endpoint-edge function,
an exact rational isolating interval, opposite strict endpoint signs, and a
strict full-interval transverse derivative.  The root identity is shared by
the two open 2D sides, the 1D root slice, and the 0D endpoint join.
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
import cm2_round219_source_g_partial_face_common_refinement_glue as r219


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round223_source_g_analytic_endpoint_root_stratification"
OUTPUT = HERE / f"{PREFIX}_certificate.json"
SCHEMA = (
    "cm2.round223.source-g-analytic-endpoint-root-stratification.v1"
)
STATUS = (
    "CERTIFIED_FULL_EXACT_P_S_CONTACT_SYMBOLIC_ANALYTIC_ROOT_"
    "STRATIFICATION__PHYSICAL_COMPONENT_CLOSURE_STILL_INCOMPLETE"
)
VERDICT = (
    "FORMAL_ALL_7932_EXACT_P_S_CONTACTS_COMPLETE_BY_RATIONAL_AND_"
    "SYMBOLIC_ANALYTIC_ROOT_STRATA__236_PARTIAL_CONTACTS_AND_"
    "PHYSICAL_COMPONENT_QUOTIENT_REMAIN"
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
R186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
R186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)

STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
R219_UNRESOLVED_SUBFACES = 7_236
R219_INCOMPLETE_CONTACTS = 7_016
DIRECT_ROOT_PARTITIONS = 6_980
DIRECT_ABSENCE_PARTITIONS = 4
ADAPTIVE_ROOT_PARTITIONS = 252
ANALYTIC_ROOTS = 7_232
EDGE_PARTITIONS = 7_236
EDGE_TERMINAL_SEGMENTS = 8_000
EDGE_ABSENCE_SEGMENTS = 768
STRATA = 28_932
ROOT_SIDE_STRATA = 14_464
ROOT_SLICE_STRATA = 7_232
ROOT_POINT_STRATA = 7_232
ENDPOINT_JOINS = 7_232
NEW_COMPLETE_CONTACTS = 7_016
CUMULATIVE_EXACT_CONTACTS = 7_932
PARTIAL_REMAINING = 236
SOURCE_G_KEYS = 224_580
MAX_ADAPTIVE_EDGE_DEPTH = 5
MAX_INPUT_BYTES = 180_000_000


class Round223Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round223Error(label)


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
    return f"round223-{kind}:{digest(identity)}"


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


def strict_json(raw: bytes) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf"), "JSON BOM")
    require(len(raw) <= MAX_INPUT_BYTES, "JSON size")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise Round223Error("JSON UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_pairs,
            parse_constant=lambda token: (
                (_ for _ in ()).throw(
                    Round223Error(f"JSON constant:{token}")
                )
            ),
        )
    except json.JSONDecodeError as error:
        raise Round223Error("strict JSON parse") from error
    require(isinstance(value, dict), "JSON top object")
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


def edge_box(
    fixed_axis: str,
    graph_coordinate: Q,
    fixed_coordinate: Q,
    lower: Q,
    upper: Q,
    label: str,
) -> tuple[Any, int]:
    atlas = r186.r179.r174.atlas.AtlasBox
    if fixed_axis == "p":
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
    require(fixed_axis == "s", "fixed p/s face")
    return (
        atlas(
            graph_coordinate,
            graph_coordinate,
            lower,
            upper,
            fixed_coordinate,
            fixed_coordinate,
            0,
            label,
        ),
        1,
    )


def endpoint_value_proof(
    chart: str,
    target: str,
    active: str,
    box: Any,
) -> dict[str, str]:
    direct_value = r186.factor_geometry(
        chart, target, box
    )[active][0]
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


def edge_interval_proof(
    row: dict[str, Any],
    frontier: dict[str, Any],
    path: str,
    depth: int,
    interval: tuple[Q, Q],
) -> dict[str, Any]:
    graph_signs = row["selected_lower_upper_derivative_signs"]
    require(
        graph_signs[2] in STRICT_SIGNS
        and (
            (graph_signs[0] in STRICT_SIGNS)
            ^ (graph_signs[1] in STRICT_SIGNS)
        ),
        "one ambiguous graph endpoint and strict graph derivative",
    )
    graph_endpoint = (
        "LOWER" if graph_signs[0] not in STRICT_SIGNS else "UPPER"
    )
    graph_coordinate = Q(
        row["graph_interval"][0 if graph_endpoint == "LOWER" else 1]
    )
    lower, upper = interval
    full_box, derivative_index = edge_box(
        row["fixed_axis"],
        graph_coordinate,
        Q(row["shared_coordinate"]),
        lower,
        upper,
        f"round223-edge-full:{row['terminal_subface_row_id']}:{path}",
    )
    lower_box, _ = edge_box(
        row["fixed_axis"],
        graph_coordinate,
        Q(row["shared_coordinate"]),
        lower,
        lower,
        f"round223-edge-lower:{row['terminal_subface_row_id']}:{path}",
    )
    upper_box, _ = edge_box(
        row["fixed_axis"],
        graph_coordinate,
        Q(row["shared_coordinate"]),
        upper,
        upper,
        f"round223-edge-upper:{row['terminal_subface_row_id']}:{path}",
    )
    chart = frontier["source_chart"]
    target = frontier["target_lift"]
    active = frontier["active_factor"]
    full = r186.factor_geometry(chart, target, full_box)[active]
    full_value_sign = r186.r179.arb_sign(full[0])
    derivative = full[1][derivative_index]
    derivative_sign = (
        "DERIVATIVE_UNAVAILABLE"
        if derivative is None
        else r186.r179.arb_sign(derivative)
    )
    lower_proof = endpoint_value_proof(
        chart, target, active, lower_box
    )
    upper_proof = endpoint_value_proof(
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
        "Round219_terminal_subface_row_id":
            row["terminal_subface_row_id"],
        "edge_dyadic_path": path,
        "edge_depth": depth,
        "edge_interval": [str(lower), str(upper)],
    }
    return closed({
        "edge_terminal_segment_row_id":
            identifier("edge-terminal-segment", identity),
        **identity,
        "Round219_terminal_subface_row_sha256": row["row_sha256"],
        "contact_row_id": row["contact_row_id"],
        "fixed_axis": row["fixed_axis"],
        "shared_coordinate": row["shared_coordinate"],
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
        "formal_edge_unique_root_credit":
            int(classification == "UNIQUE_INTERIOR_ROOT"),
        "formal_edge_zero_absence_credit":
            int(classification.endswith("ZERO_ABSENT")),
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def edge_partition(
    row: dict[str, Any],
    frontier: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    original = tuple(
        Q(value) for value in row["transverse_interval"]
    )
    direct = edge_interval_proof(row, frontier, "", 0, original)
    if direct["classification"] != "UNRESOLVED":
        terminals = [direct]
        method = "DIRECT_FULL_EDGE_MONOTONE_OR_INTERVAL"
        completion_depth = 0
    else:
        active = [("", original)]
        terminals = []
        completion_depth = None
        for depth in range(1, MAX_ADAPTIVE_EDGE_DEPTH + 1):
            following: list[tuple[str, tuple[Q, Q]]] = []
            for path, (lower, upper) in active:
                midpoint = (lower + upper) / 2
                for suffix, interval in (
                    ("L", (lower, midpoint)),
                    ("R", (midpoint, upper)),
                ):
                    child = edge_interval_proof(
                        row,
                        frontier,
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
        require(not active and completion_depth is not None,
                "adaptive edge partition closes by depth five")
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
        "edge terminal exact union",
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
        counts["UNIQUE_INTERIOR_ROOT"] in {0, 1}
        and counts["UNRESOLVED"] == 0,
        "edge partition at most one root and no unresolved",
    )
    partition_identity = {
        "Round219_terminal_subface_row_id":
            row["terminal_subface_row_id"],
        "Round219_terminal_subface_row_sha256": row["row_sha256"],
    }
    partition_id = identifier("endpoint-edge-partition", partition_identity)
    root_terminal = next(
        (
            terminal for terminal in terminals
            if terminal["classification"] == "UNIQUE_INTERIOR_ROOT"
        ),
        None,
    )
    partition = closed({
        "endpoint_edge_partition_row_id": partition_id,
        **partition_identity,
        "contact_row_id": row["contact_row_id"],
        "fixed_axis": row["fixed_axis"],
        "shared_coordinate": row["shared_coordinate"],
        "graph_interval": copy.deepcopy(row["graph_interval"]),
        "original_transverse_interval":
            copy.deepcopy(row["transverse_interval"]),
        "partition_method": method,
        "adaptive_completion_depth": completion_depth,
        "terminal_edge_segment_count": len(terminals),
        "unique_interior_root_terminal_count":
            counts["UNIQUE_INTERIOR_ROOT"],
        "zero_absence_terminal_count":
            len(terminals) - counts["UNIQUE_INTERIOR_ROOT"],
        "root_edge_terminal_segment_row_id":
            None if root_terminal is None
            else root_terminal["edge_terminal_segment_row_id"],
        "root_edge_terminal_segment_row_sha256":
            None if root_terminal is None
            else root_terminal["row_sha256"],
        "terminal_edge_segments_sha256": digest([
            [
                terminal["edge_terminal_segment_row_id"],
                terminal["row_sha256"],
            ]
            for terminal in terminals
        ]),
        "terminal_partition_exact_union_of_original_edge": True,
        "terminal_partition_has_no_gap": True,
        "terminal_partition_has_no_owned_overlap": True,
        "edge_root_set_complete": True,
        "formal_edge_partition_complete_credit": 1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })
    return partition, terminals


def analytic_root_row(
    r219_row: dict[str, Any],
    frontier: dict[str, Any],
    partition: dict[str, Any],
    terminal: dict[str, Any],
) -> dict[str, Any]:
    require(
        terminal["classification"] == "UNIQUE_INTERIOR_ROOT"
        and terminal["lower_transverse_endpoint_sign"]
        != terminal["upper_transverse_endpoint_sign"]
        and terminal["full_transverse_derivative_sign"]
        in STRICT_SIGNS,
        "analytic root proof",
    )
    function_identity = {
        "source_chart": frontier["source_chart"],
        "target_lift": frontier["target_lift"],
        "active_factor": frontier["active_factor"],
        "fixed_axis": r219_row["fixed_axis"],
        "fixed_coordinate": r219_row["shared_coordinate"],
        "graph_endpoint": terminal["graph_endpoint"],
        "graph_endpoint_coordinate":
            terminal["graph_endpoint_coordinate"],
    }
    identity = {
        "analytic_function_identity_sha256": digest(function_identity),
        "edge_carrier_Round219_terminal_subface_row_id":
            r219_row["terminal_subface_row_id"],
        "isolating_rational_interval":
            copy.deepcopy(terminal["edge_interval"]),
        "isolating_edge_terminal_segment_row_id":
            terminal["edge_terminal_segment_row_id"],
    }
    root_id = identifier("analytic-endpoint-root", identity)
    return closed({
        "analytic_root_row_id": root_id,
        **identity,
        "endpoint_edge_partition_row_id":
            partition["endpoint_edge_partition_row_id"],
        "Round219_terminal_subface_row_sha256": r219_row["row_sha256"],
        "contact_row_id": r219_row["contact_row_id"],
        "source_chart": frontier["source_chart"],
        "target_lift": frontier["target_lift"],
        "active_factor": frontier["active_factor"],
        "fixed_axis": r219_row["fixed_axis"],
        "fixed_coordinate": r219_row["shared_coordinate"],
        "graph_endpoint": terminal["graph_endpoint"],
        "graph_endpoint_coordinate":
            terminal["graph_endpoint_coordinate"],
        "edge_free_axis":
            "s" if r219_row["fixed_axis"] == "p" else "p",
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
            "THE_UNIQUE_ZERO_OF_THE_PINNED_ANALYTIC_ENDPOINT_EDGE_"
            "FUNCTION_ON_THE_CLOSED_RATIONAL_ISOLATING_INTERVAL",
        "root_is_strictly_inside_isolating_interval": True,
        "root_is_simple_by_strict_full_transverse_derivative": True,
        "root_set_on_original_edge_is_complete_by_exact_terminal_"
        "partition": True,
        "formal_analytic_root_credit": 1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def trace_ids(
    stratum_id: str,
    r219_row: dict[str, Any],
) -> tuple[str, str, str, str]:
    curve = identifier(
        "symbolic-open-strip-zero-curve",
        {"stratum_row_id": stratum_id},
    )
    negative = identifier(
        "negative-open-strip-incidence",
        {
            "zero_curve_row_id": curve,
            "leaf_row_id": r219_row["negative_side_leaf_row_id"],
        },
    )
    positive = identifier(
        "positive-open-strip-incidence",
        {
            "zero_curve_row_id": curve,
            "leaf_row_id": r219_row["positive_side_leaf_row_id"],
        },
    )
    glue = identifier(
        "symbolic-open-strip-glue",
        {
            "zero_curve_row_id": curve,
            "negative_incidence_row_id": negative,
            "positive_incidence_row_id": positive,
        },
    )
    return curve, negative, positive, glue


def root_strata(
    r219_row: dict[str, Any],
    root: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root_id = root["analytic_root_row_id"]
    graph_endpoint = root["graph_endpoint"]
    derivative_sign = root[
        "strict_full_transverse_derivative_sign"
    ]
    lower_edge_sign = root["lower_isolating_endpoint_sign"]
    upper_edge_sign = root["upper_isolating_endpoint_sign"]
    require(
        (
            derivative_sign == "STRICT_POSITIVE"
            and lower_edge_sign == "STRICT_NEGATIVE"
            and upper_edge_sign == "STRICT_POSITIVE"
        )
        or (
            derivative_sign == "STRICT_NEGATIVE"
            and lower_edge_sign == "STRICT_POSITIVE"
            and upper_edge_sign == "STRICT_NEGATIVE"
        ),
        "root side signs agree with strict monotonicity",
    )
    old_graph_signs = r219_row[
        "selected_lower_upper_derivative_signs"
    ]
    other_graph_sign = (
        old_graph_signs[1]
        if graph_endpoint == "LOWER"
        else old_graph_signs[0]
    )
    graph_derivative_sign = old_graph_signs[2]
    require(
        other_graph_sign in STRICT_SIGNS
        and graph_derivative_sign in STRICT_SIGNS,
        "other graph endpoint and graph derivative strict",
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
        graph_signs = (
            [edge_sign, other_graph_sign, graph_derivative_sign]
            if graph_endpoint == "LOWER"
            else [other_graph_sign, edge_sign, graph_derivative_sign]
        )
        classification = (
            "TRACE" if graph_signs[0] != graph_signs[1] else "ABSENT"
        )
        identity = {
            "analytic_root_row_id": root_id,
            "stratum_kind": "TWO_DIMENSIONAL_OPEN_ROOT_SIDE",
            "root_side": side,
        }
        stratum_id = identifier("symbolic-stratum", identity)
        if classification == "TRACE":
            curve, negative, positive, glue = trace_ids(
                stratum_id, r219_row
            )
        else:
            curve = negative = positive = glue = None
        stratum = closed({
            "symbolic_stratum_row_id": stratum_id,
            **identity,
            "Round219_terminal_subface_row_id":
                r219_row["terminal_subface_row_id"],
            "contact_row_id": r219_row["contact_row_id"],
            "topological_dimension": 2,
            "graph_interval":
                copy.deepcopy(r219_row["graph_interval"]),
            "transverse_domain_relation": relation,
            "root_boundary_coordinate_representation":
                "EXACT_ANALYTIC_ROOT_ID",
            "selected_lower_upper_graph_derivative_signs":
                graph_signs,
            "classification": classification,
            "classification_derived_from_strict_root_monotonicity": True,
            "restricted_zero_curve_row_id": curve,
            "negative_side_incidence_row_id": negative,
            "negative_side_leaf_row_id":
                r219_row["negative_side_leaf_row_id"],
            "positive_side_incidence_row_id": positive,
            "positive_side_leaf_row_id":
                r219_row["positive_side_leaf_row_id"],
            "exact_common_refinement_glue_row_id": glue,
            "formal_two_dimensional_trace_stratum_credit":
                int(classification == "TRACE"),
            "formal_two_dimensional_zero_absence_stratum_credit":
                int(classification == "ABSENT"),
            "formal_local_incidence_credit":
                2 * int(classification == "TRACE"),
            "formal_local_glue_credit":
                int(classification == "TRACE"),
            "formal_component_deduplication_credit": 0,
            "whole_origin_credit": 0,
            "global_component_credit": 0,
            "global_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
        })
        strata.append(stratum)
        if classification == "TRACE":
            require(trace_stratum is None, "one TRACE side per root")
            trace_stratum = stratum
    require(trace_stratum is not None, "root has one TRACE side")

    interior_sign = (
        graph_derivative_sign
        if graph_endpoint == "LOWER"
        else opposite(graph_derivative_sign)
    )
    slice_identity = {
        "analytic_root_row_id": root_id,
        "stratum_kind": "ONE_DIMENSIONAL_ROOT_SLICE_WITH_ROOT_POINT_REMOVED",
    }
    slice_id = identifier("symbolic-stratum", slice_identity)
    strata.append(closed({
        "symbolic_stratum_row_id": slice_id,
        **slice_identity,
        "Round219_terminal_subface_row_id":
            r219_row["terminal_subface_row_id"],
        "contact_row_id": r219_row["contact_row_id"],
        "topological_dimension": 1,
        "transverse_coordinate": "ANALYTIC_ROOT",
        "graph_domain":
            "GRAPH_INTERVAL_WITH_THE_ROOT_ENDPOINT_REMOVED",
        "strict_interior_active_factor_sign": interior_sign,
        "strict_graph_derivative_sign": graph_derivative_sign,
        "classification": "ROOT_SLICE_ZERO_ABSENT_AWAY_FROM_ROOT_POINT",
        "formal_one_dimensional_root_slice_zero_absence_credit": 1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    }))

    point_identity = {
        "analytic_root_row_id": root_id,
        "stratum_kind": "ZERO_DIMENSIONAL_ENDPOINT_ROOT_POINT",
    }
    point_id = identifier("symbolic-stratum", point_identity)
    join_identity = {
        "analytic_root_row_id": root_id,
        "root_point_stratum_row_id": point_id,
        "trace_stratum_row_id":
            trace_stratum["symbolic_stratum_row_id"],
        "restricted_zero_curve_row_id":
            trace_stratum["restricted_zero_curve_row_id"],
    }
    join_id = identifier("endpoint-to-curve-join", join_identity)
    point = closed({
        "symbolic_stratum_row_id": point_id,
        **point_identity,
        "Round219_terminal_subface_row_id":
            r219_row["terminal_subface_row_id"],
        "contact_row_id": r219_row["contact_row_id"],
        "topological_dimension": 0,
        "graph_coordinate": root["graph_endpoint_coordinate"],
        "transverse_coordinate": "ANALYTIC_ROOT",
        "active_factor_is_exactly_zero_by_root_definition": True,
        "endpoint_to_curve_join_row_id": join_id,
        "formal_zero_dimensional_root_point_credit": 1,
        "formal_endpoint_to_curve_join_credit": 1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })
    strata.append(point)
    join = closed({
        "endpoint_to_curve_join_row_id": join_id,
        **join_identity,
        "root_point_stratum_row_sha256": point["row_sha256"],
        "trace_stratum_row_sha256": trace_stratum["row_sha256"],
        "contact_row_id": r219_row["contact_row_id"],
        "negative_side_leaf_row_id":
            r219_row["negative_side_leaf_row_id"],
        "positive_side_leaf_row_id":
            r219_row["positive_side_leaf_row_id"],
        "exact_restricted_evaluator_identity": True,
        "joined_from_numeric_root_approximation": False,
        "formal_endpoint_to_curve_join_credit": 1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })
    return strata, join


def zero_root_whole_stratum(
    r219_row: dict[str, Any],
    terminal: dict[str, Any],
) -> dict[str, Any]:
    require(
        terminal["classification"].endswith("ZERO_ABSENT"),
        "zero-root edge partition",
    )
    edge_sign = terminal["lower_transverse_endpoint_sign"]
    require(
        edge_sign == terminal["upper_transverse_endpoint_sign"]
        and edge_sign in STRICT_SIGNS,
        "whole edge strict sign",
    )
    old_signs = r219_row["selected_lower_upper_derivative_signs"]
    graph_endpoint = terminal["graph_endpoint"]
    graph_signs = (
        [edge_sign, old_signs[1], old_signs[2]]
        if graph_endpoint == "LOWER"
        else [old_signs[0], edge_sign, old_signs[2]]
    )
    require(all(sign in STRICT_SIGNS for sign in graph_signs),
            "whole strip strict graph signs")
    classification = (
        "TRACE" if graph_signs[0] != graph_signs[1] else "ABSENT"
    )
    identity = {
        "Round219_terminal_subface_row_id":
            r219_row["terminal_subface_row_id"],
        "stratum_kind": "TWO_DIMENSIONAL_WHOLE_RATIONAL_STRIP",
    }
    stratum_id = identifier("symbolic-stratum", identity)
    if classification == "TRACE":
        curve, negative, positive, glue = trace_ids(
            stratum_id, r219_row
        )
    else:
        curve = negative = positive = glue = None
    return closed({
        "symbolic_stratum_row_id": stratum_id,
        **identity,
        "contact_row_id": r219_row["contact_row_id"],
        "topological_dimension": 2,
        "graph_interval": copy.deepcopy(r219_row["graph_interval"]),
        "transverse_interval":
            copy.deepcopy(r219_row["transverse_interval"]),
        "selected_lower_upper_graph_derivative_signs": graph_signs,
        "classification": classification,
        "classification_derived_from_complete_zero-free_endpoint_edge":
            True,
        "restricted_zero_curve_row_id": curve,
        "negative_side_incidence_row_id": negative,
        "negative_side_leaf_row_id":
            r219_row["negative_side_leaf_row_id"],
        "positive_side_incidence_row_id": positive,
        "positive_side_leaf_row_id":
            r219_row["positive_side_leaf_row_id"],
        "exact_common_refinement_glue_row_id": glue,
        "formal_two_dimensional_trace_stratum_credit":
            int(classification == "TRACE"),
        "formal_two_dimensional_zero_absence_stratum_credit":
            int(classification == "ABSENT"),
        "formal_local_incidence_credit":
            2 * int(classification == "TRACE"),
        "formal_local_glue_credit":
            int(classification == "TRACE"),
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def contact_completion_row(
    r219_contact: dict[str, Any],
    old_rows: list[dict[str, Any]],
    partitions: list[dict[str, Any]],
    replacement_strata: list[dict[str, Any]],
) -> dict[str, Any]:
    require(
        len(old_rows)
        == r219_contact["UNRESOLVED_terminal_subface_count"]
        == len(partitions)
        and all(
            partition["formal_edge_partition_complete_credit"] == 1
            and partition["edge_root_set_complete"] is True
            for partition in partitions
        ),
        "contact exact unresolved replacement",
    )
    identity = {
        "Round219_exact_contact_row_id":
            r219_contact["exact_contact_row_id"],
        "Round219_exact_contact_row_sha256":
            r219_contact["row_sha256"],
    }
    return closed({
        "completed_contact_row_id":
            identifier("completed-exact-contact", identity),
        **identity,
        "official_key_ordinal":
            r219_contact["official_key_ordinal"],
        "fixed_axis": r219_contact["fixed_axis"],
        "Round219_inherited_resolved_terminal_subface_count":
            r219_contact["terminal_subface_count"]
            - r219_contact["UNRESOLVED_terminal_subface_count"],
        "replaced_Round219_UNRESOLVED_terminal_subface_count":
            len(old_rows),
        "old_UNRESOLVED_terminal_subface_rows_sha256": digest([
            [row["terminal_subface_row_id"], row["row_sha256"]]
            for row in sorted(
                old_rows,
                key=lambda item: item["terminal_subface_row_id"],
            )
        ]),
        "endpoint_edge_partition_rows_sha256": digest([
            [
                row["endpoint_edge_partition_row_id"],
                row["row_sha256"],
            ]
            for row in sorted(
                partitions,
                key=lambda item: item["endpoint_edge_partition_row_id"],
            )
        ]),
        "replacement_symbolic_stratum_count":
            len(replacement_strata),
        "replacement_symbolic_strata_sha256": digest([
            [
                row["symbolic_stratum_row_id"],
                row["row_sha256"],
            ]
            for row in sorted(
                replacement_strata,
                key=lambda item: item["symbolic_stratum_row_id"],
            )
        ]),
        "all_old_UNRESOLVED_subfaces_exactly_replaced": True,
        "replacement_partition_exact_union_of_old_subfaces": True,
        "replacement_partition_has_no_gap": True,
        "replacement_partition_has_no_owned_overlap": True,
        "complete_TRACE_ABSENT_root_slice_and_root_point_stratification":
            True,
        "formal_exact_contact_symbolic_stratification_complete_credit": 1,
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
    pinned(HERE / R219_SOURCE, R219_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R219_MANIFEST, R219_MANIFEST_SHA256, 10_000)
    pinned(HERE / R186_SOURCE, R186_SOURCE_SHA256, 5_000_000)
    raw219 = pinned(
        HERE / R219_CERTIFICATE,
        R219_CERTIFICATE_SHA256,
        MAX_INPUT_BYTES,
    )
    envelope219 = strict_json(raw219)
    require(
        set(envelope219) == {"schema", "result", "result_sha256"}
        and envelope219["result_sha256"] == R219_RESULT_SHA256
        and digest(envelope219["result"]) == R219_RESULT_SHA256,
        "Round219 result closure",
    )
    result219 = envelope219["result"]
    terminal219 = validate_ledger(
        result219["formal_terminal_subface_ledger"],
        "terminal_subface_row_id",
    )
    contacts219 = validate_ledger(
        result219["formal_exact_contact_partition_ledger"],
        "exact_contact_row_id",
    )
    unresolved219 = [
        row for row in terminal219
        if row["classification"] == "UNRESOLVED"
    ]
    incomplete219 = [
        row for row in contacts219
        if row[
            "formal_exact_contact_common_refinement_complete_credit"
        ] == 0
    ]
    require(
        len(unresolved219) == R219_UNRESOLVED_SUBFACES
        and len(incomplete219) == R219_INCOMPLETE_CONTACTS,
        "Round219 exact frontier",
    )

    (
        _result217,
        exact_frontier,
        _partial_frontier,
        _evaluators,
        upstream_hashes,
    ) = r219.load_boundary()
    ctx.prec = 256
    frontier_by_id = {
        row["frontier_row_id"]: row for row in exact_frontier
    }
    contact_by_id = {
        row["exact_contact_row_id"]: row for row in contacts219
    }

    edge_partitions: list[dict[str, Any]] = []
    edge_terminals: list[dict[str, Any]] = []
    analytic_roots: list[dict[str, Any]] = []
    symbolic_strata: list[dict[str, Any]] = []
    endpoint_joins: list[dict[str, Any]] = []
    partitions_by_contact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    old_rows_by_contact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    strata_by_contact: dict[str, list[dict[str, Any]]] = defaultdict(list)

    print(
        "Round223 building 7236 endpoint-edge partitions",
        file=sys.stderr,
    )
    for index, old_row in enumerate(unresolved219, 1):
        frontier = frontier_by_id[
            old_row["Round217_frontier_row_id"]
        ]
        partition, terminals = edge_partition(old_row, frontier)
        edge_partitions.append(partition)
        edge_terminals.extend(terminals)
        partitions_by_contact[old_row["contact_row_id"]].append(partition)
        old_rows_by_contact[old_row["contact_row_id"]].append(old_row)
        root_terminal = next(
            (
                terminal for terminal in terminals
                if terminal["classification"] == "UNIQUE_INTERIOR_ROOT"
            ),
            None,
        )
        if root_terminal is None:
            require(len(terminals) == 1, "direct whole-edge absence")
            stratum = zero_root_whole_stratum(old_row, terminals[0])
            symbolic_strata.append(stratum)
            strata_by_contact[old_row["contact_row_id"]].append(stratum)
        else:
            root = analytic_root_row(
                old_row, frontier, partition, root_terminal
            )
            strata, join = root_strata(old_row, root)
            analytic_roots.append(root)
            symbolic_strata.extend(strata)
            endpoint_joins.append(join)
            strata_by_contact[old_row["contact_row_id"]].extend(strata)
        if index % 1000 == 0:
            print(
                f"Round223 endpoint edges {index}/{len(unresolved219)}",
                file=sys.stderr,
            )

    completed_contacts = [
        contact_completion_row(
            contact_by_id[contact_id],
            old_rows_by_contact[contact_id],
            partitions_by_contact[contact_id],
            strata_by_contact[contact_id],
        )
        for contact_id in sorted(old_rows_by_contact)
    ]
    for rows, key in (
        (edge_partitions, "endpoint_edge_partition_row_id"),
        (edge_terminals, "edge_terminal_segment_row_id"),
        (analytic_roots, "analytic_root_row_id"),
        (symbolic_strata, "symbolic_stratum_row_id"),
        (endpoint_joins, "endpoint_to_curve_join_row_id"),
        (completed_contacts, "completed_contact_row_id"),
    ):
        rows.sort(key=lambda row, key=key: row[key])
        validate_rows(rows, key)

    partition_methods = Counter(
        row["partition_method"] for row in edge_partitions
    )
    partition_root_counts = Counter(
        row["unique_interior_root_terminal_count"]
        for row in edge_partitions
    )
    terminal_classes = Counter(
        row["classification"] for row in edge_terminals
    )
    adaptive_completion_depths = Counter(
        row["adaptive_completion_depth"]
        for row in edge_partitions
        if row["partition_method"] == "ADAPTIVE_RATIONAL_EDGE_PARTITION"
    )
    stratum_kinds = Counter(
        row["stratum_kind"] for row in symbolic_strata
    )
    dimensional_counts = Counter(
        row["topological_dimension"] for row in symbolic_strata
    )
    two_dimensional_classes = Counter(
        row["classification"] for row in symbolic_strata
        if row["topological_dimension"] == 2
    )
    require(
        len(edge_partitions) == EDGE_PARTITIONS
        and len(edge_terminals) == EDGE_TERMINAL_SEGMENTS
        and len(analytic_roots) == ANALYTIC_ROOTS
        and len(symbolic_strata) == STRATA
        and len(endpoint_joins) == ENDPOINT_JOINS
        and len(completed_contacts) == NEW_COMPLETE_CONTACTS
        and partition_methods
        == Counter({
            "DIRECT_FULL_EDGE_MONOTONE_OR_INTERVAL":
                DIRECT_ROOT_PARTITIONS + DIRECT_ABSENCE_PARTITIONS,
            "ADAPTIVE_RATIONAL_EDGE_PARTITION":
                ADAPTIVE_ROOT_PARTITIONS,
        })
        and partition_root_counts
        == Counter({1: ANALYTIC_ROOTS, 0: DIRECT_ABSENCE_PARTITIONS})
        and terminal_classes["UNIQUE_INTERIOR_ROOT"] == ANALYTIC_ROOTS
        and sum(
            value for key, value in terminal_classes.items()
            if key.endswith("ZERO_ABSENT")
        ) == EDGE_ABSENCE_SEGMENTS
        and adaptive_completion_depths
        == Counter({2: 88, 3: 84, 4: 64, 5: 16})
        and stratum_kinds[
            "TWO_DIMENSIONAL_OPEN_ROOT_SIDE"
        ] == ROOT_SIDE_STRATA
        and stratum_kinds[
            "ONE_DIMENSIONAL_ROOT_SLICE_WITH_ROOT_POINT_REMOVED"
        ] == ROOT_SLICE_STRATA
        and stratum_kinds[
            "ZERO_DIMENSIONAL_ENDPOINT_ROOT_POINT"
        ] == ROOT_POINT_STRATA
        and dimensional_counts[2] == ROOT_SIDE_STRATA + 4
        and dimensional_counts[1] == ROOT_SLICE_STRATA
        and dimensional_counts[0] == ROOT_POINT_STRATA,
        "Round223 formal census",
    )
    require(
        all(
            row[
                "formal_exact_contact_symbolic_stratification_complete_credit"
            ] == 1
            for row in completed_contacts
        )
        and len(old_rows_by_contact) == R219_INCOMPLETE_CONTACTS,
        "all Round219 incomplete contacts complete",
    )
    completion_ordinals = Counter(
        row["official_key_ordinal"] for row in completed_contacts
    )
    whole_strata = [
        row for row in symbolic_strata
        if row["stratum_kind"]
        == "TWO_DIMENSIONAL_WHOLE_RATIONAL_STRIP"
    ]
    whole_classes = Counter(
        row["classification"] for row in whole_strata
    )

    return {
        "status": STATUS,
        "verdict": VERDICT,
        "formal_input_binding": {
            "Round219_source_sha256": R219_SOURCE_SHA256,
            "Round219_certificate_sha256": R219_CERTIFICATE_SHA256,
            "Round219_result_sha256": R219_RESULT_SHA256,
            "Round219_manifest_sha256": R219_MANIFEST_SHA256,
            "Round186_factor_evaluator_source_sha256":
                R186_SOURCE_SHA256,
            **upstream_hashes,
            "Round219_exact_UNRESOLVED_terminal_subface_count":
                len(unresolved219),
            "Round219_incomplete_exact_contact_count":
                len(incomplete219),
            "Round219_producer_imported_as_pinned_predicate_dependency":
                True,
            "Round221_probe_imported_or_executed": False,
        },
        "formal_analytic_root_contract": {
            "coordinate_representation":
                "EXACT_ANALYTIC_UNIQUE_ROOT_NOT_NUMERIC_APPROXIMATION",
            "root_identity_binds_analytic_function_edge_carrier_and_"
            "rational_isolating_interval": True,
            "unique_root_requires_opposite_strict_endpoint_signs": True,
            "simple_root_requires_strict_full_transverse_derivative": True,
            "adaptive_partition_splits_only_UNRESOLVED_children": True,
            "adaptive_partition_maximum_depth":
                MAX_ADAPTIVE_EDGE_DEPTH,
            "edge_terminal_owner_rule":
                "LEFT_CLOSED_RIGHT_OPEN_EXCEPT_FINAL_RIGHT_CLOSED",
            "root_is_shared_by_both_open_sides_root_slice_and_root_point":
                True,
            "numeric_root_approximation_used_as_exact_coordinate": False,
        },
        "formal_endpoint_edge_scope": {
            "endpoint_edge_partition_count": len(edge_partitions),
            "direct_unique_root_partition_count":
                DIRECT_ROOT_PARTITIONS,
            "direct_zero_absence_partition_count":
                DIRECT_ABSENCE_PARTITIONS,
            "adaptive_unique_root_partition_count":
                ADAPTIVE_ROOT_PARTITIONS,
            "analytic_unique_root_count": len(analytic_roots),
            "terminal_edge_segment_count": len(edge_terminals),
            "terminal_unique_root_segment_count":
                terminal_classes["UNIQUE_INTERIOR_ROOT"],
            "terminal_zero_absence_segment_count":
                EDGE_ABSENCE_SEGMENTS,
            "adaptive_completion_depth_histogram": {
                str(key): value
                for key, value in sorted(
                    adaptive_completion_depths.items()
                )
            },
            "all_endpoint_edge_root_sets_complete": True,
            "remaining_UNRESOLVED_endpoint_edge_segment_count": 0,
        },
        "formal_symbolic_stratum_scope": {
            "symbolic_stratum_count": len(symbolic_strata),
            "two_dimensional_open_root_side_count":
                ROOT_SIDE_STRATA,
            "one_dimensional_root_slice_count":
                ROOT_SLICE_STRATA,
            "zero_dimensional_root_point_count":
                ROOT_POINT_STRATA,
            "two_dimensional_whole_rational_strip_count":
                len(whole_strata),
            "two_dimensional_TRACE_count":
                two_dimensional_classes["TRACE"],
            "two_dimensional_ABSENT_count":
                two_dimensional_classes["ABSENT"],
            "whole_rational_strip_classification_count":
                dict(sorted(whole_classes.items())),
            "endpoint_to_curve_join_count": len(endpoint_joins),
            "every_root_partition_is_left_open_side_plus_root_slice_"
            "plus_right_open_side": True,
            "root_point_is_separate_from_two_dimensional_strips": True,
            "every_old_UNRESOLVED_subface_exactly_partitioned": True,
        },
        "formal_exact_contact_scope": {
            "Round219_direct_complete_contact_count":
                result219["formal_exact_contact_scope"][
                    "cumulative_complete_contact_count"
                ],
            "new_symbolic_stratification_complete_contact_count":
                len(completed_contacts),
            "cumulative_complete_exact_p_s_contact_count":
                CUMULATIVE_EXACT_CONTACTS,
            "total_exact_p_s_contact_count":
                CUMULATIVE_EXACT_CONTACTS,
            "remaining_incomplete_exact_p_s_contact_count": 0,
            "cumulative_identity": "916+7016=7932",
            "new_complete_official_key_ordinal_count":
                len(completion_ordinals),
            "new_complete_contacts_per_official_key_ordinal": {
                str(key): value
                for key, value in sorted(completion_ordinals.items())
            },
            "new_complete_contacts_per_official_key_ordinal_sha256":
                digest(dict(sorted(completion_ordinals.items()))),
            "physical_component_equivalence_relation_complete": False,
        },
        "formal_endpoint_edge_partition_ledger":
            ledger(
                edge_partitions,
                "endpoint_edge_partition_row_id",
            ),
        "formal_edge_terminal_segment_ledger":
            ledger(edge_terminals, "edge_terminal_segment_row_id"),
        "formal_analytic_root_ledger":
            ledger(analytic_roots, "analytic_root_row_id"),
        "formal_symbolic_stratum_ledger":
            ledger(symbolic_strata, "symbolic_stratum_row_id"),
        "formal_endpoint_to_curve_join_ledger":
            ledger(endpoint_joins, "endpoint_to_curve_join_row_id"),
        "formal_completed_exact_contact_ledger":
            ledger(completed_contacts, "completed_contact_row_id"),
        "first_missing_frontier": {
            "remaining_incomplete_exact_p_s_contact_count": 0,
            "remaining_partial_contact_count": PARTIAL_REMAINING,
            "partial_contact_symbolic_root_stratification_missing": True,
            "complete_physical_component_equivalence_closure_missing":
                True,
            "global_occurrence_fibre_exhaustion_missing": True,
        },
        "formal_credit_contract": {
            "formal_analytic_root_credits": len(analytic_roots),
            "formal_endpoint_to_curve_join_credits":
                len(endpoint_joins),
            "formal_two_dimensional_trace_stratum_credits":
                two_dimensional_classes["TRACE"],
            "formal_two_dimensional_zero_absence_stratum_credits":
                two_dimensional_classes["ABSENT"],
            "formal_one_dimensional_root_slice_zero_absence_credits":
                ROOT_SLICE_STRATA,
            "formal_zero_dimensional_root_point_credits":
                ROOT_POINT_STRATA,
            "formal_exact_contact_symbolic_stratification_complete_"
            "credits": len(completed_contacts),
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
            "apply the same exact analytic-root stratification to the "
            "236 partial contacts, then use only proved local glue and "
            "endpoint-join edges to close the physical-component "
            "equivalence relation and global occurrence fibres"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "python_flint_version":
                getattr(__import__("flint"), "__version__", "unknown"),
            "effective_Arb_precision_bits": ctx.prec,
            "Round221_probe_imported_or_executed": False,
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
