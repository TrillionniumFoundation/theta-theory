#!/usr/bin/env python3
"""Independent verifier for Round224 partial analytic-root strata.

The verifier pins the Round224 producer as inert source bytes but never
imports or executes it.  Before loading the candidate certificate it rebuilds
the complete expected Python object from the frozen Round219, Round223, and
factor-evaluator boundary.
"""

from __future__ import annotations

import argparse
import ast
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
from typing import Any, Callable, Iterable

from flint import ctx

import cm2_round186_source_g_factor_face_probe as r186
import cm2_round219_source_g_partial_face_common_refinement_glue as r219


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round224_source_g_partial_face_analytic_root_stratification"
PRODUCER = f"{PREFIX}.py"
CERTIFICATE = f"{PREFIX}_certificate.json"
VERIFICATION = f"{PREFIX}_verification.json"
SCHEMA = (
    "cm2.round224.source-g-partial-face-analytic-root-stratification.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round224.source-g-partial-face-analytic-root-stratification"
    ".verification.v1"
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

PRODUCER_SHA256 = (
    "8bb6bd227be21d2c2c6e34394e4f83257f502bb9ab621355a306d5a20757336b"
)
CERTIFICATE_SHA256 = (
    "9ff49f0a55c0048f8dc7b636b1ddcc7291e01545e9775d95cb9738f4b3f237c7"
)
RESULT_SHA256 = (
    "2015369b8f5eef92da2245981157bf4dbacc55a69939b087d893f954f3374ab8"
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
PARTITIONS = 236
TERMINALS = 236
ROOTS = 236
STRATA = 944
JOINS = 236
COMPLETED = 236
MAX_ADAPTIVE_DEPTH = 5
MAX_BYTES = 180_000_000

LEDGERS = (
    (
        "formal_partial_endpoint_edge_partition_ledger",
        "partial_endpoint_edge_partition_row_id",
    ),
    (
        "formal_partial_edge_terminal_segment_ledger",
        "partial_edge_terminal_segment_row_id",
    ),
    (
        "formal_partial_analytic_root_ledger",
        "partial_analytic_root_row_id",
    ),
    (
        "formal_partial_symbolic_stratum_ledger",
        "partial_symbolic_stratum_row_id",
    ),
    (
        "formal_partial_endpoint_to_curve_join_ledger",
        "partial_endpoint_to_curve_join_row_id",
    ),
    (
        "formal_completed_partial_contact_ledger",
        "completed_partial_contact_row_id",
    ),
)


class VerificationError(RuntimeError):
    pass


def ensure(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def encoded(value: Any) -> Iterable[bytes]:
    for part in ENCODER.iterencode(value):
        yield part.encode()


def canonical(value: Any) -> bytes:
    return b"".join(encoded(value))


def object_hash(value: Any) -> str:
    state = hashlib.sha256()
    for part in encoded(value):
        state.update(part)
    return state.hexdigest()


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result["row_sha256"] = object_hash(result)
    return result


def row_id(kind: str, identity: dict[str, Any]) -> str:
    return f"round224-{kind}:{object_hash(identity)}"


def make_ledger(
    rows: list[dict[str, Any]],
    id_key: str,
) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "rows_sha256": object_hash(rows),
        "row_ids_sha256": object_hash([row[id_key] for row in rows]),
        "row_hashes_sha256":
            object_hash([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def exact_read(
    path: Path,
    maximum: int,
    parent: Path = HERE,
) -> bytes:
    ensure(
        not any(part == ".." for part in path.parts),
        "input parent alias",
    )
    expected_parent = Path(os.path.abspath(os.fspath(parent)))
    ensure(parent.resolve() == expected_parent, "expected parent alias")
    ensure(
        path.is_absolute() and path.parent == expected_parent,
        "input raw parent",
    )
    path = Path(os.path.abspath(os.fspath(path)))
    ensure(
        path.parent == expected_parent
        and path.parent.resolve() == expected_parent,
        "input exact parent",
    )
    before = path.lstat()
    ensure(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1
        and 0 < before.st_size <= maximum,
        f"bounded unique regular input:{path.name}",
    )
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        ensure(
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
            "stable input open",
        )
        output: list[bytes] = []
        total = 0
        while True:
            part = os.read(descriptor, 1024 * 1024)
            if not part:
                break
            total += len(part)
            ensure(total <= maximum, "bounded input read")
            output.append(part)
        after = os.fstat(descriptor)
        ensure(
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
            "stable input read",
        )
        return b"".join(output)
    finally:
        os.close(descriptor)


def pin(path: Path, expected: str, maximum: int) -> bytes:
    raw = exact_read(path, maximum)
    ensure(
        hashlib.sha256(raw).hexdigest() == expected,
        f"SHA256:{path.name}",
    )
    return raw


def pair_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        ensure(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def validate_scalars(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            ensure(
                all(ord(character) >= 0x20 for character in key),
                "JSON key control character",
            )
            validate_scalars(item)
    elif isinstance(value, list):
        for item in value:
            validate_scalars(item)
    elif isinstance(value, str):
        ensure(
            all(ord(character) >= 0x20 for character in value),
            "JSON string control character",
        )


def strict_decode(raw: bytes, maximum: int = MAX_BYTES) -> dict[str, Any]:
    ensure(0 < len(raw) <= maximum, "JSON bounded size")
    ensure(not raw.startswith(b"\xef\xbb\xbf"), "JSON BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise VerificationError("JSON UTF-8") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=pair_hook,
            parse_constant=lambda token: (
                (_ for _ in ()).throw(
                    VerificationError(f"JSON constant:{token}")
                )
            ),
        )
    except json.JSONDecodeError as error:
        raise VerificationError("strict JSON parse") from error
    ensure(isinstance(value, dict), "JSON top object")
    validate_scalars(value)
    ensure(raw == canonical(value) + b"\n", "canonical JSON bytes")
    return value


def inspect_ledger(
    value: dict[str, Any],
    id_key: str,
) -> list[dict[str, Any]]:
    rows = value["rows"]
    ensure(
        value["row_count"] == len(rows)
        and value["rows_sha256"] == object_hash(rows)
        and value["row_ids_sha256"]
        == object_hash([row[id_key] for row in rows])
        and value["row_hashes_sha256"]
        == object_hash([row["row_sha256"] for row in rows])
        and value["every_row_closed_by_own_SHA256"] is True
        and len({row[id_key] for row in rows}) == len(rows),
        f"ledger closure:{id_key}",
    )
    for row in rows:
        payload = dict(row)
        row_hash = payload.pop("row_sha256")
        ensure(object_hash(payload) == row_hash, f"row closure:{id_key}")
    return rows


def opposite(sign: str) -> str:
    ensure(sign in STRICT_SIGNS, "strict sign")
    return (
        "STRICT_POSITIVE"
        if sign == "STRICT_NEGATIVE"
        else "STRICT_NEGATIVE"
    )


def selected_value(
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
    return {
        "direct_value": str(direct_value),
        "centered_value": str(centered_value),
        "direct_sign": direct_sign,
        "centered_sign": centered_sign,
        "selected_sign": (
            direct_sign
            if direct_sign in STRICT_SIGNS
            else centered_sign
        ),
    }


def graph_data(
    partial: dict[str, Any],
) -> tuple[str, str, tuple[Q, Q], tuple[Q, Q], list[str]]:
    if partial["fixed_axis"] == "p":
        graph_axis, transverse_axis = "t", "s"
    else:
        ensure(partial["fixed_axis"] == "t", "fixed p/t")
        graph_axis, transverse_axis = "p", "s"
    attempt = partial["graph_axis_attempts"][0]
    signs = attempt["selected_lower_upper_derivative_signs"]
    ensure(
        attempt["graph_axis"] == graph_axis
        and signs[2] in STRICT_SIGNS
        and (
            (signs[0] in STRICT_SIGNS)
            ^ (signs[1] in STRICT_SIGNS)
        ),
        "strict graph attempt",
    )
    return (
        graph_axis,
        transverse_axis,
        tuple(Q(value) for value in partial["positive_overlap_intervals"][0]),
        tuple(Q(value) for value in partial["positive_overlap_intervals"][1]),
        signs,
    )


def boundary_box(
    partial: dict[str, Any],
    graph_coordinate: Q,
    lower: Q,
    upper: Q,
    label: str,
) -> tuple[Any, int]:
    atlas = r186.r179.r174.atlas.AtlasBox
    fixed = Q(partial["shared_coordinate"])
    if partial["fixed_axis"] == "p":
        return (
            atlas(
                graph_coordinate,
                graph_coordinate,
                fixed,
                fixed,
                lower,
                upper,
                0,
                label,
            ),
            2,
        )
    return (
        atlas(
            fixed,
            fixed,
            graph_coordinate,
            graph_coordinate,
            lower,
            upper,
            0,
            label,
        ),
        2,
    )


def expected_terminal(
    partial: dict[str, Any],
    evaluator: tuple[str, str, str],
) -> dict[str, Any]:
    (
        graph_axis,
        transverse_axis,
        graph_interval,
        edge_interval,
        graph_signs,
    ) = graph_data(partial)
    graph_endpoint = (
        "LOWER" if graph_signs[0] not in STRICT_SIGNS else "UPPER"
    )
    graph_coordinate = graph_interval[
        0 if graph_endpoint == "LOWER" else 1
    ]
    lower, upper = edge_interval
    full_box, derivative_index = boundary_box(
        partial,
        graph_coordinate,
        lower,
        upper,
        f"round224-edge-full:{partial['partial_contact_row_id']}:",
    )
    lower_box, _ = boundary_box(
        partial,
        graph_coordinate,
        lower,
        lower,
        f"round224-edge-lower:{partial['partial_contact_row_id']}:",
    )
    upper_box, _ = boundary_box(
        partial,
        graph_coordinate,
        upper,
        upper,
        f"round224-edge-upper:{partial['partial_contact_row_id']}:",
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
    lower_proof = selected_value(
        chart, target, active, lower_box
    )
    upper_proof = selected_value(
        chart, target, active, upper_box
    )
    lower_sign = lower_proof["selected_sign"]
    upper_sign = upper_proof["selected_sign"]
    ensure(
        full_value_sign not in STRICT_SIGNS
        and derivative_sign in STRICT_SIGNS
        and lower_sign in STRICT_SIGNS
        and upper_sign in STRICT_SIGNS
        and lower_sign != upper_sign,
        "direct unique partial root",
    )
    witness = {
        "full_edge_value": str(full[0]),
        "full_edge_value_sign": full_value_sign,
        "full_transverse_derivative": str(derivative),
        "full_transverse_derivative_sign": derivative_sign,
        "lower_endpoint": lower_proof,
        "upper_endpoint": upper_proof,
    }
    identity = {
        "Round219_partial_contact_row_id":
            partial["partial_contact_row_id"],
        "edge_dyadic_path": "",
        "edge_depth": 0,
        "edge_interval": [str(lower), str(upper)],
    }
    row = seal({
        "partial_edge_terminal_segment_row_id":
            row_id("partial-edge-terminal-segment", identity),
        **identity,
        "Round219_partial_contact_row_sha256": partial["row_sha256"],
        "Round217_frontier_row_id":
            partial["Round217_frontier_row_id"],
        "Round217_frontier_row_sha256":
            partial["Round217_frontier_row_sha256"],
        "fixed_axis": partial["fixed_axis"],
        "fixed_coordinate": partial["shared_coordinate"],
        "graph_axis": graph_axis,
        "transverse_axis": transverse_axis,
        "graph_interval": [str(value) for value in graph_interval],
        "graph_endpoint": graph_endpoint,
        "graph_endpoint_coordinate": str(graph_coordinate),
        "source_chart": chart,
        "target_lift": target,
        "active_factor": active,
        "classification": "UNIQUE_INTERIOR_ROOT",
        "full_edge_value_sign": full_value_sign,
        "full_transverse_derivative_sign": derivative_sign,
        "lower_transverse_endpoint_sign": lower_sign,
        "upper_transverse_endpoint_sign": upper_sign,
        "proof_witness_sha256": object_hash(witness),
        "unique_root_requires_opposite_strict_endpoint_signs_and_"
        "strict_full_transverse_derivative": True,
        "formal_partial_edge_unique_root_credit": 1,
        "formal_partial_edge_zero_absence_credit": 0,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })
    row.pop("row_sha256")
    row["terminal_partition_ordinal"] = 1
    row["terminal_partition_count"] = 1
    row["owned_lower_closed"] = True
    row["owned_upper_closed"] = True
    row["row_sha256"] = object_hash(row)
    return row


def expected_partition(
    partial: dict[str, Any],
    terminal: dict[str, Any],
) -> dict[str, Any]:
    (
        graph_axis,
        transverse_axis,
        graph_interval,
        transverse_interval,
        _graph_signs,
    ) = graph_data(partial)
    identity = {
        "Round219_partial_contact_row_id":
            partial["partial_contact_row_id"],
        "Round219_partial_contact_row_sha256": partial["row_sha256"],
    }
    return seal({
        "partial_endpoint_edge_partition_row_id":
            row_id("partial-endpoint-edge-partition", identity),
        **identity,
        "Round217_frontier_row_id":
            partial["Round217_frontier_row_id"],
        "fixed_axis": partial["fixed_axis"],
        "fixed_coordinate": partial["shared_coordinate"],
        "graph_axis": graph_axis,
        "transverse_axis": transverse_axis,
        "graph_interval": [str(value) for value in graph_interval],
        "original_transverse_interval": [
            str(value) for value in transverse_interval
        ],
        "partition_method": "DIRECT_FULL_EDGE_MONOTONE_OR_INTERVAL",
        "adaptive_completion_depth": 0,
        "terminal_edge_segment_count": 1,
        "unique_interior_root_terminal_count": 1,
        "zero_absence_terminal_count": 0,
        "root_edge_terminal_segment_row_id":
            terminal["partial_edge_terminal_segment_row_id"],
        "root_edge_terminal_segment_row_sha256":
            terminal["row_sha256"],
        "terminal_edge_segments_sha256": object_hash([[
            terminal["partial_edge_terminal_segment_row_id"],
            terminal["row_sha256"],
        ]]),
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
    })


def expected_root(
    partial: dict[str, Any],
    evaluator: tuple[str, str, str],
    partition: dict[str, Any],
    terminal: dict[str, Any],
) -> dict[str, Any]:
    chart, target, active = evaluator
    function_identity = {
        "source_chart": chart,
        "target_lift": target,
        "active_factor": active,
        "fixed_axis": partial["fixed_axis"],
        "fixed_coordinate": partial["shared_coordinate"],
        "graph_axis": partition["graph_axis"],
        "graph_endpoint": terminal["graph_endpoint"],
        "graph_endpoint_coordinate":
            terminal["graph_endpoint_coordinate"],
        "transverse_axis": partition["transverse_axis"],
    }
    identity = {
        "analytic_function_identity_sha256":
            object_hash(function_identity),
        "carrier_Round219_partial_contact_row_id":
            partial["partial_contact_row_id"],
        "isolating_rational_interval":
            copy.deepcopy(terminal["edge_interval"]),
        "isolating_edge_terminal_segment_row_id":
            terminal["partial_edge_terminal_segment_row_id"],
    }
    return seal({
        "partial_analytic_root_row_id":
            row_id("partial-analytic-boundary-root", identity),
        **identity,
        "partial_endpoint_edge_partition_row_id":
            partition["partial_endpoint_edge_partition_row_id"],
        "Round219_partial_contact_row_sha256": partial["row_sha256"],
        "Round217_frontier_row_id":
            partial["Round217_frontier_row_id"],
        "source_chart": chart,
        "target_lift": target,
        "active_factor": active,
        "fixed_axis": partial["fixed_axis"],
        "fixed_coordinate": partial["shared_coordinate"],
        "graph_axis": partition["graph_axis"],
        "graph_endpoint": terminal["graph_endpoint"],
        "graph_endpoint_coordinate":
            terminal["graph_endpoint_coordinate"],
        "transverse_axis": partition["transverse_axis"],
        "isolating_edge_dyadic_path": terminal["edge_dyadic_path"],
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


def trace_identifiers(
    stratum_id: str,
    partial: dict[str, Any],
) -> tuple[str, str, str, str]:
    curve = row_id(
        "partial-open-strip-zero-curve",
        {"stratum_row_id": stratum_id},
    )
    negative = row_id(
        "negative-partial-open-strip-incidence",
        {
            "zero_curve_row_id": curve,
            "leaf_row_id": partial["negative_leaf_row_id"],
        },
    )
    positive = row_id(
        "positive-partial-open-strip-incidence",
        {
            "zero_curve_row_id": curve,
            "leaf_row_id": partial["positive_leaf_row_id"],
        },
    )
    glue = row_id(
        "partial-open-strip-glue",
        {
            "zero_curve_row_id": curve,
            "negative_incidence_row_id": negative,
            "positive_incidence_row_id": positive,
        },
    )
    return curve, negative, positive, glue


def point_coordinates(
    partial: dict[str, Any],
    root: dict[str, Any],
) -> dict[str, str]:
    if partial["fixed_axis"] == "p":
        return {
            "t": root["graph_endpoint_coordinate"],
            "p": partial["shared_coordinate"],
            "s": "ANALYTIC_ROOT",
        }
    return {
        "t": partial["shared_coordinate"],
        "p": root["graph_endpoint_coordinate"],
        "s": "ANALYTIC_ROOT",
    }


def expected_strata(
    partial: dict[str, Any],
    root: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root_id_value = root["partial_analytic_root_row_id"]
    graph_endpoint = root["graph_endpoint"]
    transverse_derivative = root[
        "strict_full_transverse_derivative_sign"
    ]
    lower_edge_sign = root["lower_isolating_endpoint_sign"]
    upper_edge_sign = root["upper_isolating_endpoint_sign"]
    ensure(
        (
            transverse_derivative == "STRICT_POSITIVE"
            and lower_edge_sign == "STRICT_NEGATIVE"
            and upper_edge_sign == "STRICT_POSITIVE"
        )
        or (
            transverse_derivative == "STRICT_NEGATIVE"
            and lower_edge_sign == "STRICT_POSITIVE"
            and upper_edge_sign == "STRICT_NEGATIVE"
        ),
        "root monotonicity",
    )
    graph_signs = partial["graph_axis_attempts"][0][
        "selected_lower_upper_derivative_signs"
    ]
    other_graph_sign = (
        graph_signs[1]
        if graph_endpoint == "LOWER"
        else graph_signs[0]
    )
    graph_derivative = graph_signs[2]
    output: list[dict[str, Any]] = []
    trace: dict[str, Any] | None = None
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
        signs = (
            [edge_sign, other_graph_sign, graph_derivative]
            if graph_endpoint == "LOWER"
            else [other_graph_sign, edge_sign, graph_derivative]
        )
        classification = (
            "TRACE" if signs[0] != signs[1] else "ABSENT"
        )
        identity = {
            "partial_analytic_root_row_id": root_id_value,
            "stratum_kind":
                "TWO_DIMENSIONAL_PARTIAL_OPEN_ROOT_SIDE",
            "root_side": side,
        }
        stratum_id = row_id("partial-symbolic-stratum", identity)
        if classification == "TRACE":
            curve, negative, positive, glue = trace_identifiers(
                stratum_id, partial
            )
        else:
            curve = negative = positive = glue = None
        stratum = seal({
            "partial_symbolic_stratum_row_id": stratum_id,
            **identity,
            "Round219_partial_contact_row_id":
                partial["partial_contact_row_id"],
            "Round219_partial_contact_row_sha256":
                partial["row_sha256"],
            "Round217_frontier_row_id":
                partial["Round217_frontier_row_id"],
            "topological_dimension": 2,
            "fixed_axis": partial["fixed_axis"],
            "fixed_coordinate": partial["shared_coordinate"],
            "graph_axis": root["graph_axis"],
            "graph_interval":
                copy.deepcopy(partial["positive_overlap_intervals"][0]),
            "transverse_axis": root["transverse_axis"],
            "transverse_domain_relation": relation,
            "root_boundary_coordinate_representation":
                "EXACT_ANALYTIC_ROOT_ID",
            "selected_lower_upper_graph_derivative_signs": signs,
            "classification": classification,
            "classification_derived_from_strict_root_monotonicity":
                True,
            "restricted_zero_curve_row_id": curve,
            "negative_side_incidence_row_id": negative,
            "negative_side_leaf_row_id":
                partial["negative_leaf_row_id"],
            "positive_side_incidence_row_id": positive,
            "positive_side_leaf_row_id":
                partial["positive_leaf_row_id"],
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
        output.append(stratum)
        if classification == "TRACE":
            ensure(trace is None, "one trace side")
            trace = stratum
    ensure(trace is not None, "trace side exists")

    interior_sign = (
        graph_derivative
        if graph_endpoint == "LOWER"
        else opposite(graph_derivative)
    )
    slice_identity = {
        "partial_analytic_root_row_id": root_id_value,
        "stratum_kind":
            "ONE_DIMENSIONAL_PARTIAL_ROOT_SLICE_WITH_ROOT_POINT_REMOVED",
    }
    slice_id = row_id("partial-symbolic-stratum", slice_identity)
    output.append(seal({
        "partial_symbolic_stratum_row_id": slice_id,
        **slice_identity,
        "Round219_partial_contact_row_id":
            partial["partial_contact_row_id"],
        "Round219_partial_contact_row_sha256": partial["row_sha256"],
        "Round217_frontier_row_id":
            partial["Round217_frontier_row_id"],
        "topological_dimension": 1,
        "fixed_axis": partial["fixed_axis"],
        "fixed_coordinate": partial["shared_coordinate"],
        "transverse_axis": root["transverse_axis"],
        "transverse_coordinate": "ANALYTIC_ROOT",
        "graph_axis": root["graph_axis"],
        "graph_domain":
            "GRAPH_INTERVAL_WITH_THE_ROOT_ENDPOINT_REMOVED",
        "strict_interior_active_factor_sign": interior_sign,
        "strict_graph_derivative_sign": graph_derivative,
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
        "partial_analytic_root_row_id": root_id_value,
        "stratum_kind":
            "ZERO_DIMENSIONAL_PARTIAL_BOUNDARY_ROOT_POINT",
    }
    point_id = row_id("partial-symbolic-stratum", point_identity)
    join_identity = {
        "partial_analytic_root_row_id": root_id_value,
        "root_point_stratum_row_id": point_id,
        "trace_stratum_row_id":
            trace["partial_symbolic_stratum_row_id"],
        "restricted_zero_curve_row_id":
            trace["restricted_zero_curve_row_id"],
    }
    join_id = row_id("partial-endpoint-to-curve-join", join_identity)
    point = seal({
        "partial_symbolic_stratum_row_id": point_id,
        **point_identity,
        "Round219_partial_contact_row_id":
            partial["partial_contact_row_id"],
        "Round219_partial_contact_row_sha256": partial["row_sha256"],
        "Round217_frontier_row_id":
            partial["Round217_frontier_row_id"],
        "topological_dimension": 0,
        "exact_coordinate_map": point_coordinates(partial, root),
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
    output.append(point)
    join = seal({
        "partial_endpoint_to_curve_join_row_id": join_id,
        **join_identity,
        "root_point_stratum_row_sha256": point["row_sha256"],
        "trace_stratum_row_sha256": trace["row_sha256"],
        "Round219_partial_contact_row_id":
            partial["partial_contact_row_id"],
        "negative_side_leaf_row_id":
            partial["negative_leaf_row_id"],
        "positive_side_leaf_row_id":
            partial["positive_leaf_row_id"],
        "exact_restricted_evaluator_identity": True,
        "joined_from_numeric_root_approximation": False,
        "formal_partial_endpoint_to_curve_join_credit": 1,
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })
    return output, join


def expected_completion(
    partial: dict[str, Any],
    partition: dict[str, Any],
    root: dict[str, Any],
    strata: list[dict[str, Any]],
    join: dict[str, Any],
) -> dict[str, Any]:
    identity = {
        "Round219_partial_contact_row_id":
            partial["partial_contact_row_id"],
        "Round219_partial_contact_row_sha256": partial["row_sha256"],
    }
    return seal({
        "completed_partial_contact_row_id":
            row_id("completed-partial-contact", identity),
        **identity,
        "Round217_frontier_row_id":
            partial["Round217_frontier_row_id"],
        "fixed_axis": partial["fixed_axis"],
        "fixed_coordinate": partial["shared_coordinate"],
        "negative_leaf_row_id": partial["negative_leaf_row_id"],
        "positive_leaf_row_id": partial["positive_leaf_row_id"],
        "partial_endpoint_edge_partition_row_id":
            partition["partial_endpoint_edge_partition_row_id"],
        "partial_endpoint_edge_partition_row_sha256":
            partition["row_sha256"],
        "partial_analytic_root_row_id":
            root["partial_analytic_root_row_id"],
        "partial_analytic_root_row_sha256": root["row_sha256"],
        "replacement_partial_symbolic_stratum_count": len(strata),
        "replacement_partial_symbolic_strata_sha256": object_hash([
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
        "partial_endpoint_to_curve_join_row_sha256": join["row_sha256"],
        "old_UNRESOLVED_partial_contact_exactly_replaced": True,
        "replacement_partition_exact_union_of_old_partial_overlap":
            True,
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


def expected_result() -> dict[str, Any]:
    ensure(
        Path(r219.__file__).resolve() == (HERE / R219_SOURCE).resolve()
        and Path(r186.__file__).resolve() == (HERE / R186_SOURCE).resolve(),
        "pinned module identity",
    )
    pin(HERE / PRODUCER, PRODUCER_SHA256, 5_000_000)
    pin(HERE / R186_SOURCE, R186_SOURCE_SHA256, 5_000_000)
    pin(HERE / R219_SOURCE, R219_SOURCE_SHA256, 5_000_000)
    pin(HERE / R219_MANIFEST, R219_MANIFEST_SHA256, 10_000)
    pin(HERE / R223_SOURCE, R223_SOURCE_SHA256, 5_000_000)
    pin(HERE / R223_MANIFEST, R223_MANIFEST_SHA256, 10_000)
    envelope219 = strict_decode(pin(
        HERE / R219_CERTIFICATE,
        R219_CERTIFICATE_SHA256,
        MAX_BYTES,
    ))
    envelope223 = strict_decode(pin(
        HERE / R223_CERTIFICATE,
        R223_CERTIFICATE_SHA256,
        MAX_BYTES,
    ))
    ensure(
        envelope219["result_sha256"] == R219_RESULT_SHA256
        and object_hash(envelope219["result"]) == R219_RESULT_SHA256,
        "Round219 closure",
    )
    ensure(
        envelope223["result_sha256"] == R223_RESULT_SHA256
        and object_hash(envelope223["result"]) == R223_RESULT_SHA256,
        "Round223 closure",
    )
    result219 = envelope219["result"]
    result223 = envelope223["result"]
    partial_rows = inspect_ledger(
        result219["formal_partial_contact_probe_ledger"],
        "partial_contact_row_id",
    )
    unresolved = [
        row for row in partial_rows
        if row["classification"] == "UNRESOLVED"
    ]
    inherited_absent = [
        row for row in partial_rows
        if row["classification"] == "ABSENT"
    ]
    ensure(
        len(partial_rows) == ROUND219_PARTIAL_CONTACTS
        and len(inherited_absent) == INHERITED_PARTIAL_ABSENCES
        and len(unresolved) == REMAINING_PARTIAL_CONTACTS,
        "partial frontier census",
    )
    ensure(
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
        "Round223 boundary",
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

    partitions: list[dict[str, Any]] = []
    terminals: list[dict[str, Any]] = []
    roots: list[dict[str, Any]] = []
    strata: list[dict[str, Any]] = []
    joins: list[dict[str, Any]] = []
    completed: list[dict[str, Any]] = []
    print(
        "Round224 verifier rebuilding 236 partial contacts",
        file=sys.stderr,
    )
    for partial in unresolved:
        ensure(
            partial["Round217_frontier_row_id"] in frontier_by_id,
            "Round217 partial identity",
        )
        evaluator = evaluators[partial["negative_leaf_row_id"]]
        ensure(
            evaluator == evaluators[partial["positive_leaf_row_id"]],
            "partial evaluator identity",
        )
        terminal = expected_terminal(partial, evaluator)
        partition = expected_partition(partial, terminal)
        root = expected_root(
            partial, evaluator, partition, terminal
        )
        root_strata, join = expected_strata(partial, root)
        contact = expected_completion(
            partial, partition, root, root_strata, join
        )
        terminals.append(terminal)
        partitions.append(partition)
        roots.append(root)
        strata.extend(root_strata)
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
        ensure(
            len({row[key] for row in rows}) == len(rows),
            f"expected unique:{key}",
        )

    methods = Counter(row["partition_method"] for row in partitions)
    depths = Counter(row["adaptive_completion_depth"] for row in partitions)
    terminal_classes = Counter(row["classification"] for row in terminals)
    fixed_axes = Counter(row["fixed_axis"] for row in completed)
    graph_endpoints = Counter(row["graph_endpoint"] for row in roots)
    stratum_kinds = Counter(row["stratum_kind"] for row in strata)
    dimensions = Counter(row["topological_dimension"] for row in strata)
    two_classes = Counter(
        row["classification"]
        for row in strata
        if row["topological_dimension"] == 2
    )
    ensure(
        len(partitions) == PARTITIONS
        and len(terminals) == TERMINALS
        and len(roots) == ROOTS
        and len(strata) == STRATA
        and len(joins) == JOINS
        and len(completed) == COMPLETED
        and methods
        == Counter({"DIRECT_FULL_EDGE_MONOTONE_OR_INTERVAL": 236})
        and depths == Counter({0: 236})
        and terminal_classes == Counter({"UNIQUE_INTERIOR_ROOT": 236})
        and fixed_axes == Counter({"p": 128, "t": 108})
        and graph_endpoints == Counter({"LOWER": 118, "UPPER": 118})
        and stratum_kinds[
            "TWO_DIMENSIONAL_PARTIAL_OPEN_ROOT_SIDE"
        ] == 472
        and stratum_kinds[
            "ONE_DIMENSIONAL_PARTIAL_ROOT_SLICE_WITH_ROOT_POINT_REMOVED"
        ] == 236
        and stratum_kinds[
            "ZERO_DIMENSIONAL_PARTIAL_BOUNDARY_ROOT_POINT"
        ] == 236
        and dimensions == Counter({2: 472, 1: 236, 0: 236})
        and two_classes == Counter({"TRACE": 236, "ABSENT": 236}),
        "expected census",
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
                len(unresolved),
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
            "two_dimensional_partial_open_root_side_count": 472,
            "two_dimensional_partial_TRACE_count": two_classes["TRACE"],
            "two_dimensional_partial_ABSENT_count":
                two_classes["ABSENT"],
            "one_dimensional_partial_root_slice_count": 236,
            "zero_dimensional_partial_root_point_count": 236,
            "partial_endpoint_to_curve_join_count": len(joins),
            "every_root_partition_is_left_open_side_plus_root_slice_"
            "plus_right_open_side": True,
            "root_point_is_separate_from_two_dimensional_strips": True,
            "every_old_UNRESOLVED_partial_contact_exactly_partitioned":
                True,
        },
        "formal_partial_contact_scope": {
            "Round219_partial_frontier_contact_count": 264,
            "Round219_inherited_complete_zero_absence_contact_count": 28,
            "new_symbolic_stratification_complete_partial_contact_count":
                len(completed),
            "cumulative_complete_partial_contact_count": 264,
            "total_partial_contact_count": 264,
            "remaining_incomplete_partial_contact_count": 0,
            "cumulative_identity": "28+236=264",
            "new_complete_fixed_axis_count":
                dict(sorted(fixed_axes.items())),
            "physical_component_equivalence_relation_complete": False,
        },
        "formal_partial_endpoint_edge_partition_ledger":
            make_ledger(
                partitions,
                "partial_endpoint_edge_partition_row_id",
            ),
        "formal_partial_edge_terminal_segment_ledger":
            make_ledger(
                terminals,
                "partial_edge_terminal_segment_row_id",
            ),
        "formal_partial_analytic_root_ledger":
            make_ledger(roots, "partial_analytic_root_row_id"),
        "formal_partial_symbolic_stratum_ledger":
            make_ledger(strata, "partial_symbolic_stratum_row_id"),
        "formal_partial_endpoint_to_curve_join_ledger":
            make_ledger(
                joins,
                "partial_endpoint_to_curve_join_row_id",
            ),
        "formal_completed_partial_contact_ledger":
            make_ledger(completed, "completed_partial_contact_row_id"),
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
            "formal_two_dimensional_partial_trace_stratum_credits": 236,
            "formal_two_dimensional_partial_zero_absence_stratum_credits":
                236,
            "formal_one_dimensional_partial_root_slice_zero_absence_credits":
                236,
            "formal_zero_dimensional_partial_root_point_credits": 236,
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
            "official_source_G_global_disposition_denominator": 224_580,
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
            "producer_sha256": PRODUCER_SHA256,
            "python_version": sys.version.split()[0],
            "python_flint_version":
                getattr(__import__("flint"), "__version__", "unknown"),
            "effective_Arb_precision_bits": ctx.prec,
            "producer_imported_or_executed_by_independent_verifier":
                False,
            "formal_upstream_files_modified": False,
        },
    }


def verify_envelope(
    envelope: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    ensure(
        set(envelope) == {"schema", "result", "result_sha256"}
        and envelope["schema"] == SCHEMA
        and envelope["result_sha256"]
        == object_hash(envelope["result"]),
        "candidate envelope",
    )
    for ledger_key, id_key in LEDGERS:
        inspect_ledger(envelope["result"][ledger_key], id_key)
    ensure(
        envelope["result"] == expected,
        "full expected Python-object equality",
    )
    ensure(
        canonical(envelope["result"]) == canonical(expected),
        "full expected canonical equality",
    )


def reclose_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = object_hash(row)


def reclose_ledger(
    result: dict[str, Any],
    ledger_key: str,
) -> None:
    id_key = dict(LEDGERS)[ledger_key]
    value = result[ledger_key]
    rows = value["rows"]
    value["row_count"] = len(rows)
    value["rows_sha256"] = object_hash(rows)
    value["row_ids_sha256"] = object_hash(
        [row[id_key] for row in rows]
    )
    value["row_hashes_sha256"] = object_hash(
        [row["row_sha256"] for row in rows]
    )


Mutation = Callable[[dict[str, Any]], set[str]]


def semantic_suite(
    envelope: dict[str, Any],
    expected: dict[str, Any],
) -> tuple[int, int]:
    root_key = "formal_partial_analytic_root_ledger"
    partition_key = "formal_partial_endpoint_edge_partition_ledger"
    terminal_key = "formal_partial_edge_terminal_segment_ledger"
    stratum_key = "formal_partial_symbolic_stratum_ledger"
    join_key = "formal_partial_endpoint_to_curve_join_ledger"
    contact_key = "formal_completed_partial_contact_ledger"

    def drop_root(result: dict[str, Any]) -> set[str]:
        result[root_key]["rows"].pop()
        return {root_key}

    def change_root_interval(result: dict[str, Any]) -> set[str]:
        row = result[root_key]["rows"][0]
        row["isolating_rational_interval"] = ["0", "1"]
        reclose_row(row)
        return {root_key}

    def change_root_derivative(result: dict[str, Any]) -> set[str]:
        row = result[root_key]["rows"][0]
        row["strict_full_transverse_derivative_sign"] = opposite(
            row["strict_full_transverse_derivative_sign"]
        )
        reclose_row(row)
        return {root_key}

    def numeric_root(result: dict[str, Any]) -> set[str]:
        row = result[root_key]["rows"][0]
        row["coordinate_representation"] = "FLOAT_APPROXIMATION"
        reclose_row(row)
        return {root_key}

    def drop_root_point(result: dict[str, Any]) -> set[str]:
        rows = result[stratum_key]["rows"]
        index = next(
            index for index, row in enumerate(rows)
            if row["stratum_kind"]
            == "ZERO_DIMENSIONAL_PARTIAL_BOUNDARY_ROOT_POINT"
        )
        rows.pop(index)
        return {stratum_key}

    def drop_root_slice(result: dict[str, Any]) -> set[str]:
        rows = result[stratum_key]["rows"]
        index = next(
            index for index, row in enumerate(rows)
            if row["stratum_kind"]
            == (
                "ONE_DIMENSIONAL_PARTIAL_ROOT_SLICE_WITH_"
                "ROOT_POINT_REMOVED"
            )
        )
        rows.pop(index)
        return {stratum_key}

    def drop_join(result: dict[str, Any]) -> set[str]:
        result[join_key]["rows"].pop()
        return {join_key}

    def partition_gap(result: dict[str, Any]) -> set[str]:
        row = result[partition_key]["rows"][0]
        row["terminal_partition_has_no_gap"] = False
        reclose_row(row)
        return {partition_key}

    def partition_overlap(result: dict[str, Any]) -> set[str]:
        row = result[partition_key]["rows"][0]
        row["terminal_partition_has_no_owned_overlap"] = False
        reclose_row(row)
        return {partition_key}

    def false_terminal(result: dict[str, Any]) -> set[str]:
        row = result[terminal_key]["rows"][0]
        row["classification"] = "STRICT_INTERVAL_ZERO_ABSENT"
        row["formal_partial_edge_unique_root_credit"] = 0
        row["formal_partial_edge_zero_absence_credit"] = 1
        reclose_row(row)
        return {terminal_key}

    def false_contact(result: dict[str, Any]) -> set[str]:
        row = result[contact_key]["rows"][0]
        row[
            "complete_TRACE_ABSENT_root_slice_and_root_point_stratification"
        ] = False
        reclose_row(row)
        return {contact_key}

    def drop_contact(result: dict[str, Any]) -> set[str]:
        result[contact_key]["rows"].pop()
        return {contact_key}

    def summary_remaining(result: dict[str, Any]) -> set[str]:
        result["formal_partial_contact_scope"][
            "remaining_incomplete_partial_contact_count"
        ] = 1
        return set()

    def root_embedded(result: dict[str, Any]) -> set[str]:
        result["formal_partial_symbolic_stratum_scope"][
            "root_point_is_separate_from_two_dimensional_strips"
        ] = False
        return set()

    def numeric_contract(result: dict[str, Any]) -> set[str]:
        result["formal_partial_analytic_root_contract"][
            "numeric_root_approximation_used_as_exact_coordinate"
        ] = True
        return set()

    def component_theft(result: dict[str, Any]) -> set[str]:
        result["formal_credit_contract"][
            "formal_component_deduplication_credit"
        ] = 1
        return set()

    def whole_theft(result: dict[str, Any]) -> set[str]:
        result["formal_credit_contract"]["whole_origin_credit"] = 1
        return set()

    def global_theft(result: dict[str, Any]) -> set[str]:
        result["formal_credit_contract"][
            "global_exact_key_disposition_credit"
        ] = 1
        return set()

    mutations: list[Mutation] = [
        drop_root,
        change_root_interval,
        change_root_derivative,
        numeric_root,
        drop_root_point,
        drop_root_slice,
        drop_join,
        partition_gap,
        partition_overlap,
        false_terminal,
        false_contact,
        drop_contact,
        summary_remaining,
        root_embedded,
        numeric_contract,
        component_theft,
        whole_theft,
        global_theft,
    ]
    rejected = 0
    for mutation in mutations:
        candidate = copy.deepcopy(envelope)
        dirty = mutation(candidate["result"])
        for ledger_key in dirty:
            reclose_ledger(candidate["result"], ledger_key)
        candidate["result_sha256"] = object_hash(candidate["result"])
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
        (b'{"x":NaN}\n', MAX_BYTES),
        (b'{"x":Infinity}\n', MAX_BYTES),
        (b'{"x":-Infinity}\n', MAX_BYTES),
        (b"\xef\xbb\xbf" + good, MAX_BYTES),
        (b'{"x":"\\u0000"}\n', MAX_BYTES),
        (b"\xff\n", MAX_BYTES),
        (b'{"x":"\\ud800"}\n', MAX_BYTES),
        (good + b"x", MAX_BYTES),
        (good[:-1], MAX_BYTES),
        (b"[]\n", MAX_BYTES),
        (b"1\n", MAX_BYTES),
        (b'""\n', MAX_BYTES),
        (b"", MAX_BYTES),
        (good, len(good) - 1),
    ]
    attacks[0] = (
        text.replace(
            '"result":{',
            '"result":{"status":"x","status":"y",',
            1,
        ).encode(),
        MAX_BYTES,
    )
    rejected = 0
    for raw, maximum in attacks:
        try:
            strict_decode(raw, maximum)
        except (VerificationError, UnicodeError):
            rejected += 1
    return len(attacks), rejected


def validate_output(path: Path) -> Path:
    ensure(
        not any(part == ".." for part in path.parts),
        "output parent alias",
    )
    ensure(
        path.is_absolute() and path.parent == HERE,
        "output raw parent",
    )
    absolute = Path(os.path.abspath(os.fspath(path)))
    ensure(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "output exact parent",
    )
    official = absolute.name == VERIFICATION
    replay = (
        absolute.name.startswith(f".{PREFIX}_verification_replay_")
        and absolute.name.endswith(".json")
    )
    ensure(official or replay, "output filename")
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        ensure(
            stat.S_ISREG(metadata.st_mode)
            and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "existing output type",
        )
    return absolute


def path_suite() -> tuple[int, int]:
    attempted = 0
    rejected = 0

    def reject_input(
        path: Path,
        maximum: int,
        parent: Path,
    ) -> None:
        nonlocal attempted, rejected
        attempted += 1
        try:
            exact_read(path, maximum, parent)
        except (VerificationError, OSError):
            rejected += 1

    def reject_output(path: Path) -> None:
        nonlocal attempted, rejected
        attempted += 1
        try:
            validate_output(path)
        except (VerificationError, OSError):
            rejected += 1

    with tempfile.TemporaryDirectory(
        prefix=".round224_path_", dir=HERE
    ) as raw:
        root = Path(raw)
        valid = root / "candidate.json"
        valid.write_bytes(b"{}\n")
        ensure(
            exact_read(valid, 1024, root) == b"{}\n",
            "path control",
        )
        symlink = root / "symlink.json"
        symlink.symlink_to(valid)
        reject_input(symlink, 1024, root)
        target = root / "target.json"
        target.write_bytes(b"{}\n")
        hard = root / "hard.json"
        os.link(target, hard)
        reject_input(hard, 1024, root)
        directory = root / "directory.json"
        directory.mkdir()
        reject_input(directory, 1024, root)
        fifo = root / "fifo.json"
        os.mkfifo(fifo)
        reject_input(fifo, 1024, root)
        empty = root / "empty.json"
        empty.write_bytes(b"")
        reject_input(empty, 1024, root)
        large = root / "large.json"
        with large.open("wb") as handle:
            handle.truncate(1025)
        reject_input(large, 1024, root)
        reject_input(valid, 1024, HERE)
        reject_input(root / ".." / valid.name, 1024, root)
        reject_input(root / "missing.json", 1024, root)
        input_parent_alias = root / "input_parent_alias"
        input_parent_alias.symlink_to(root, target_is_directory=True)
        reject_input(input_parent_alias / valid.name, 1024, root)

        token = str(os.getpid())
        output_parent_alias = root / "output_parent_alias"
        output_parent_alias.symlink_to(HERE, target_is_directory=True)
        reject_output(
            output_parent_alias
            / f".{PREFIX}_verification_replay_alias_{token}.json"
        )
        reject_output(
            HERE / ".." / HERE.name
            / f".{PREFIX}_verification_replay_dotdot_{token}.json"
        )
        cleanup: list[Path] = []
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
        wrong = HERE / f".round224_wrong_{token}.json"
        wrong.write_bytes(b"{}\n")
        cleanup.append(wrong)
        reject_output(wrong)
        output_dir = HERE / (
            f".{PREFIX}_verification_replay_directory_{token}.json"
        )
        output_dir.mkdir()
        cleanup.append(output_dir)
        reject_output(output_dir)
        reject_output(HERE / PRODUCER)
        reject_output(HERE / CERTIFICATE)
        reject_output(HERE / Path(__file__).name)
        for path in reversed(cleanup):
            mode = path.lstat().st_mode
            if path.is_symlink() or path.is_file() or stat.S_ISFIFO(mode):
                path.unlink()
            else:
                path.rmdir()
    return attempted, rejected


def ast_duplicates(path: Path) -> int:
    tree = ast.parse(exact_read(path, 5_000_000).decode())
    duplicates = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: set[tuple[str, str]] = set()
        for key in node.keys:
            if isinstance(key, ast.Constant):
                token = (type(key.value).__name__, repr(key.value))
                if token in seen:
                    duplicates += 1
                seen.add(token)
    return duplicates


def safe_write(path: Path, data: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{PREFIX}.verify.tmp.",
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
        ensure(
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
    parser.add_argument(
        "--output",
        type=Path,
        default=HERE / VERIFICATION,
    )
    arguments = parser.parse_args()
    verifier_sha = hashlib.sha256(
        exact_read(HERE / Path(__file__).name, 5_000_000)
    ).hexdigest()

    expected = expected_result()
    print("Round224 verifier now loading candidate", file=sys.stderr)
    raw_candidate = pin(
        HERE / CERTIFICATE,
        CERTIFICATE_SHA256,
        MAX_BYTES,
    )
    envelope = strict_decode(raw_candidate)
    ensure(
        envelope["result_sha256"] == RESULT_SHA256,
        "candidate result pin",
    )
    verify_envelope(envelope, expected)
    semantic_attempted, semantic_rejected = semantic_suite(
        envelope, expected
    )
    json_attempted, json_rejected = json_suite(envelope)
    path_attempted, path_rejected = path_suite()
    print(
        f"Round224 hostile semantic={semantic_rejected}/"
        f"{semantic_attempted} JSON={json_rejected}/{json_attempted} "
        f"path={path_rejected}/{path_attempted}",
        file=sys.stderr,
    )
    ensure(
        semantic_attempted == semantic_rejected == 18
        and json_attempted == json_rejected == 15
        and path_attempted == path_rejected == 21,
        "hostile suites",
    )
    producer_duplicate_keys = ast_duplicates(HERE / PRODUCER)
    verifier_duplicate_keys = ast_duplicates(
        HERE / Path(__file__).name
    )
    ensure(
        producer_duplicate_keys == verifier_duplicate_keys == 0,
        "AST duplicate literal keys",
    )
    result = {
        "status": "PASS_PARTIAL_FORMAL_ROUND224",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": RESULT_SHA256,
        "verifier_sha256": verifier_sha,
        "full_expected_Python_object_equality": True,
        "full_expected_canonical_equality": True,
        "partial_endpoint_edge_partition_rows_verified": PARTITIONS,
        "partial_edge_terminal_segment_rows_verified": TERMINALS,
        "partial_analytic_root_rows_verified": ROOTS,
        "partial_symbolic_stratum_rows_verified": STRATA,
        "partial_endpoint_to_curve_join_rows_verified": JOINS,
        "completed_partial_contact_rows_verified": COMPLETED,
        "cumulative_partial_contact_count_verified": 264,
        "remaining_incomplete_partial_contact_count_verified": 0,
        "semantic_resigned_attacks_attempted": semantic_attempted,
        "semantic_resigned_attacks_rejected": semantic_rejected,
        "strict_JSON_attacks_attempted": json_attempted,
        "strict_JSON_attacks_rejected": json_rejected,
        "filesystem_path_attacks_attempted": path_attempted,
        "filesystem_path_attacks_rejected": path_rejected,
        "producer_AST_duplicate_literal_key_count":
            producer_duplicate_keys,
        "verifier_AST_duplicate_literal_key_count":
            verifier_duplicate_keys,
        "producer_imported_or_executed": False,
        "Round221_probe_imported_or_executed": False,
        "formal_component_or_global_credit_granted": False,
    }
    output = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": object_hash(result),
    }
    safe_write(arguments.output, canonical(output) + b"\n")
    print(output["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
