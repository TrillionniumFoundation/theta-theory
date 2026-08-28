#!/usr/bin/env python3
"""Fresh independent verifier for Round223 symbolic endpoint-root strata."""

from __future__ import annotations

import argparse
import ast
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
from typing import Any, Callable, Iterable

from flint import ctx

import cm2_round186_source_g_factor_face_probe as r186
import cm2_round219_source_g_partial_face_common_refinement_glue as r219


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round223_source_g_analytic_endpoint_root_stratification"
PRODUCER = f"{PREFIX}.py"
CERTIFICATE = f"{PREFIX}_certificate.json"
VERIFICATION = f"{PREFIX}_verification.json"
SCHEMA = (
    "cm2.round223.source-g-analytic-endpoint-root-stratification.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round223.source-g-analytic-endpoint-root-stratification-"
    "verification.v1"
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
PRODUCER_SHA256 = (
    "fb5d46a31857cb09c2606747d4fbec996eecffdf65702431a17624a2260ad970"
)
CERTIFICATE_SHA256 = (
    "3d28f097419e11bde6733462736fcb70cd0164b18ac06a793a34b5dc26113168"
)
RESULT_SHA256 = (
    "db012bb2e68176c8a5c144455bac9ff780521bbfa3c03110694390c70a3343d9"
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

STRICT = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
UNRESOLVED_ROWS = 7_236
INCOMPLETE_CONTACTS = 7_016
ROOTS = 7_232
PARTITIONS = 7_236
TERMINALS = 8_000
ABSENCE_TERMINALS = 768
STRATA = 28_932
JOINS = 7_232
COMPLETED = 7_016
MAX_EDGE_DEPTH = 5
MAX_BYTES = 180_000_000


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


def pieces(value: Any) -> Iterable[bytes]:
    for piece in ENCODER.iterencode(value):
        yield piece.encode()


def canonical(value: Any) -> bytes:
    return b"".join(pieces(value))


def object_hash(value: Any) -> str:
    state = hashlib.sha256()
    for piece in pieces(value):
        state.update(piece)
    return state.hexdigest()


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = object_hash(row)
    return row


def key_id(kind: str, identity: dict[str, Any]) -> str:
    return f"round223-{kind}:{object_hash(identity)}"


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
        text = raw.decode()
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
    try:
        encoded = canonical(value) + b"\n"
    except UnicodeEncodeError as error:
        raise VerificationError("JSON scalar") from error
    ensure(raw == encoded, "canonical JSON bytes")
    return value


def inspect_ledger(
    ledger: dict[str, Any],
    id_key: str,
) -> list[dict[str, Any]]:
    rows = ledger["rows"]
    ensure(
        ledger["row_count"] == len(rows)
        and ledger["rows_sha256"] == object_hash(rows)
        and ledger["row_ids_sha256"]
        == object_hash([row[id_key] for row in rows])
        and ledger["row_hashes_sha256"]
        == object_hash([row["row_sha256"] for row in rows])
        and ledger["every_row_closed_by_own_SHA256"] is True
        and len({row[id_key] for row in rows}) == len(rows),
        f"ledger closure:{id_key}",
    )
    for row in rows:
        payload = dict(row)
        row_hash = payload.pop("row_sha256")
        ensure(object_hash(payload) == row_hash, f"row closure:{id_key}")
    return rows


def sign_opposite(sign: str) -> str:
    ensure(sign in STRICT, "strict sign")
    return (
        "STRICT_POSITIVE"
        if sign == "STRICT_NEGATIVE"
        else "STRICT_NEGATIVE"
    )


def make_edge_box(
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
    ensure(fixed_axis == "s", "fixed p/s")
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


def point_proof(
    chart: str,
    target: str,
    active: str,
    box: Any,
) -> dict[str, str]:
    direct = r186.factor_geometry(chart, target, box)[active][0]
    centered = r186.centered_value(chart, target, box, active)
    direct_sign = r186.r179.arb_sign(direct)
    centered_sign = r186.r179.arb_sign(centered)
    return {
        "direct_value": str(direct),
        "centered_value": str(centered),
        "direct_sign": direct_sign,
        "centered_sign": centered_sign,
        "selected_sign":
            direct_sign if direct_sign in STRICT else centered_sign,
    }


def expected_edge_segment(
    old: dict[str, Any],
    frontier: dict[str, Any],
    path: str,
    depth: int,
    interval: tuple[Q, Q],
) -> dict[str, Any]:
    graph_signs = old["selected_lower_upper_derivative_signs"]
    ensure(
        graph_signs[2] in STRICT
        and (
            (graph_signs[0] in STRICT)
            ^ (graph_signs[1] in STRICT)
        ),
        "one graph endpoint ambiguous",
    )
    endpoint = "LOWER" if graph_signs[0] not in STRICT else "UPPER"
    graph_coordinate = Q(
        old["graph_interval"][0 if endpoint == "LOWER" else 1]
    )
    lower, upper = interval
    full_box, derivative_index = make_edge_box(
        old["fixed_axis"],
        graph_coordinate,
        Q(old["shared_coordinate"]),
        lower,
        upper,
        f"round223-edge-full:{old['terminal_subface_row_id']}:{path}",
    )
    lower_box, _ = make_edge_box(
        old["fixed_axis"],
        graph_coordinate,
        Q(old["shared_coordinate"]),
        lower,
        lower,
        f"round223-edge-lower:{old['terminal_subface_row_id']}:{path}",
    )
    upper_box, _ = make_edge_box(
        old["fixed_axis"],
        graph_coordinate,
        Q(old["shared_coordinate"]),
        upper,
        upper,
        f"round223-edge-upper:{old['terminal_subface_row_id']}:{path}",
    )
    chart = frontier["source_chart"]
    target = frontier["target_lift"]
    active = frontier["active_factor"]
    full = r186.factor_geometry(chart, target, full_box)[active]
    value_sign = r186.r179.arb_sign(full[0])
    derivative = full[1][derivative_index]
    derivative_sign = (
        "DERIVATIVE_UNAVAILABLE"
        if derivative is None
        else r186.r179.arb_sign(derivative)
    )
    lower_proof = point_proof(chart, target, active, lower_box)
    upper_proof = point_proof(chart, target, active, upper_box)
    lower_sign = lower_proof["selected_sign"]
    upper_sign = upper_proof["selected_sign"]
    if value_sign in STRICT:
        classification = "STRICT_INTERVAL_ZERO_ABSENT"
    elif (
        derivative_sign in STRICT
        and lower_sign in STRICT
        and upper_sign in STRICT
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
        "full_edge_value_sign": value_sign,
        "full_transverse_derivative":
            None if derivative is None else str(derivative),
        "full_transverse_derivative_sign": derivative_sign,
        "lower_endpoint": lower_proof,
        "upper_endpoint": upper_proof,
    }
    identity = {
        "Round219_terminal_subface_row_id":
            old["terminal_subface_row_id"],
        "edge_dyadic_path": path,
        "edge_depth": depth,
        "edge_interval": [str(lower), str(upper)],
    }
    return seal({
        "edge_terminal_segment_row_id":
            key_id("edge-terminal-segment", identity),
        **identity,
        "Round219_terminal_subface_row_sha256": old["row_sha256"],
        "contact_row_id": old["contact_row_id"],
        "fixed_axis": old["fixed_axis"],
        "shared_coordinate": old["shared_coordinate"],
        "graph_endpoint": endpoint,
        "graph_endpoint_coordinate": str(graph_coordinate),
        "source_chart": chart,
        "target_lift": target,
        "active_factor": active,
        "classification": classification,
        "full_edge_value_sign": value_sign,
        "full_transverse_derivative_sign": derivative_sign,
        "lower_transverse_endpoint_sign": lower_sign,
        "upper_transverse_endpoint_sign": upper_sign,
        "proof_witness_sha256": object_hash(witness),
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


def expected_partition(
    old: dict[str, Any],
    frontier: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    original = tuple(Q(value) for value in old["transverse_interval"])
    direct = expected_edge_segment(old, frontier, "", 0, original)
    if direct["classification"] != "UNRESOLVED":
        terminals = [direct]
        method = "DIRECT_FULL_EDGE_MONOTONE_OR_INTERVAL"
        completion_depth = 0
    else:
        active = [("", original)]
        terminals: list[dict[str, Any]] = []
        completion_depth = None
        for depth in range(1, MAX_EDGE_DEPTH + 1):
            following: list[tuple[str, tuple[Q, Q]]] = []
            for path, (lower, upper) in active:
                middle = (lower + upper) / 2
                for suffix, interval in (
                    ("L", (lower, middle)),
                    ("R", (middle, upper)),
                ):
                    child = expected_edge_segment(
                        old, frontier, path + suffix, depth, interval
                    )
                    if child["classification"] == "UNRESOLVED":
                        following.append((path + suffix, interval))
                    else:
                        terminals.append(child)
            active = following
            if not active:
                completion_depth = depth
                break
        ensure(not active and completion_depth is not None,
               "adaptive edge closes")
        method = "ADAPTIVE_RATIONAL_EDGE_PARTITION"
    terminals.sort(
        key=lambda row: (
            Q(row["edge_interval"][0]),
            Q(row["edge_interval"][1]),
            row["edge_dyadic_path"],
        )
    )
    ensure(
        terminals[0]["edge_interval"][0] == str(original[0])
        and terminals[-1]["edge_interval"][1] == str(original[1])
        and all(
            terminals[index]["edge_interval"][1]
            == terminals[index + 1]["edge_interval"][0]
            for index in range(len(terminals) - 1)
        ),
        "terminal edge exact union",
    )
    for ordinal, terminal in enumerate(terminals, 1):
        terminal.pop("row_sha256")
        terminal["terminal_partition_ordinal"] = ordinal
        terminal["terminal_partition_count"] = len(terminals)
        terminal["owned_lower_closed"] = True
        terminal["owned_upper_closed"] = ordinal == len(terminals)
        terminal["row_sha256"] = object_hash(terminal)
    counts = Counter(row["classification"] for row in terminals)
    ensure(
        counts["UNIQUE_INTERIOR_ROOT"] in {0, 1}
        and counts["UNRESOLVED"] == 0,
        "edge root completeness",
    )
    identity = {
        "Round219_terminal_subface_row_id":
            old["terminal_subface_row_id"],
        "Round219_terminal_subface_row_sha256": old["row_sha256"],
    }
    root_terminal = next(
        (
            row for row in terminals
            if row["classification"] == "UNIQUE_INTERIOR_ROOT"
        ),
        None,
    )
    partition = seal({
        "endpoint_edge_partition_row_id":
            key_id("endpoint-edge-partition", identity),
        **identity,
        "contact_row_id": old["contact_row_id"],
        "fixed_axis": old["fixed_axis"],
        "shared_coordinate": old["shared_coordinate"],
        "graph_interval": copy.deepcopy(old["graph_interval"]),
        "original_transverse_interval":
            copy.deepcopy(old["transverse_interval"]),
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
        "terminal_edge_segments_sha256": object_hash([
            [
                row["edge_terminal_segment_row_id"],
                row["row_sha256"],
            ]
            for row in terminals
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


def expected_root(
    old: dict[str, Any],
    frontier: dict[str, Any],
    partition: dict[str, Any],
    terminal: dict[str, Any],
) -> dict[str, Any]:
    ensure(
        terminal["classification"] == "UNIQUE_INTERIOR_ROOT"
        and terminal["lower_transverse_endpoint_sign"]
        != terminal["upper_transverse_endpoint_sign"]
        and terminal["full_transverse_derivative_sign"] in STRICT,
        "root proof",
    )
    function_identity = {
        "source_chart": frontier["source_chart"],
        "target_lift": frontier["target_lift"],
        "active_factor": frontier["active_factor"],
        "fixed_axis": old["fixed_axis"],
        "fixed_coordinate": old["shared_coordinate"],
        "graph_endpoint": terminal["graph_endpoint"],
        "graph_endpoint_coordinate":
            terminal["graph_endpoint_coordinate"],
    }
    identity = {
        "analytic_function_identity_sha256":
            object_hash(function_identity),
        "edge_carrier_Round219_terminal_subface_row_id":
            old["terminal_subface_row_id"],
        "isolating_rational_interval":
            copy.deepcopy(terminal["edge_interval"]),
        "isolating_edge_terminal_segment_row_id":
            terminal["edge_terminal_segment_row_id"],
    }
    root_id = key_id("analytic-endpoint-root", identity)
    return seal({
        "analytic_root_row_id": root_id,
        **identity,
        "endpoint_edge_partition_row_id":
            partition["endpoint_edge_partition_row_id"],
        "Round219_terminal_subface_row_sha256": old["row_sha256"],
        "contact_row_id": old["contact_row_id"],
        "source_chart": frontier["source_chart"],
        "target_lift": frontier["target_lift"],
        "active_factor": frontier["active_factor"],
        "fixed_axis": old["fixed_axis"],
        "fixed_coordinate": old["shared_coordinate"],
        "graph_endpoint": terminal["graph_endpoint"],
        "graph_endpoint_coordinate":
            terminal["graph_endpoint_coordinate"],
        "edge_free_axis": "s" if old["fixed_axis"] == "p" else "p",
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


def expected_trace_ids(
    stratum_id: str,
    old: dict[str, Any],
) -> tuple[str, str, str, str]:
    curve = key_id(
        "symbolic-open-strip-zero-curve",
        {"stratum_row_id": stratum_id},
    )
    negative = key_id(
        "negative-open-strip-incidence",
        {
            "zero_curve_row_id": curve,
            "leaf_row_id": old["negative_side_leaf_row_id"],
        },
    )
    positive = key_id(
        "positive-open-strip-incidence",
        {
            "zero_curve_row_id": curve,
            "leaf_row_id": old["positive_side_leaf_row_id"],
        },
    )
    glue = key_id(
        "symbolic-open-strip-glue",
        {
            "zero_curve_row_id": curve,
            "negative_incidence_row_id": negative,
            "positive_incidence_row_id": positive,
        },
    )
    return curve, negative, positive, glue


def expected_root_strata(
    old: dict[str, Any],
    root: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root_id = root["analytic_root_row_id"]
    endpoint = root["graph_endpoint"]
    derivative_sign = root[
        "strict_full_transverse_derivative_sign"
    ]
    lower_edge_sign = root["lower_isolating_endpoint_sign"]
    upper_edge_sign = root["upper_isolating_endpoint_sign"]
    ensure(
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
        "root monotonicity orientation",
    )
    old_signs = old["selected_lower_upper_derivative_signs"]
    other_sign = old_signs[1] if endpoint == "LOWER" else old_signs[0]
    graph_derivative = old_signs[2]
    ensure(other_sign in STRICT and graph_derivative in STRICT,
           "strict other graph data")
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
            [edge_sign, other_sign, graph_derivative]
            if endpoint == "LOWER"
            else [other_sign, edge_sign, graph_derivative]
        )
        classification = (
            "TRACE" if graph_signs[0] != graph_signs[1] else "ABSENT"
        )
        identity = {
            "analytic_root_row_id": root_id,
            "stratum_kind": "TWO_DIMENSIONAL_OPEN_ROOT_SIDE",
            "root_side": side,
        }
        stratum_id = key_id("symbolic-stratum", identity)
        if classification == "TRACE":
            curve, negative, positive, glue = expected_trace_ids(
                stratum_id, old
            )
        else:
            curve = negative = positive = glue = None
        stratum = seal({
            "symbolic_stratum_row_id": stratum_id,
            **identity,
            "Round219_terminal_subface_row_id":
                old["terminal_subface_row_id"],
            "contact_row_id": old["contact_row_id"],
            "topological_dimension": 2,
            "graph_interval": copy.deepcopy(old["graph_interval"]),
            "transverse_domain_relation": relation,
            "root_boundary_coordinate_representation":
                "EXACT_ANALYTIC_ROOT_ID",
            "selected_lower_upper_graph_derivative_signs":
                graph_signs,
            "classification": classification,
            "classification_derived_from_strict_root_monotonicity":
                True,
            "restricted_zero_curve_row_id": curve,
            "negative_side_incidence_row_id": negative,
            "negative_side_leaf_row_id":
                old["negative_side_leaf_row_id"],
            "positive_side_incidence_row_id": positive,
            "positive_side_leaf_row_id":
                old["positive_side_leaf_row_id"],
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
            ensure(trace_stratum is None, "one TRACE side")
            trace_stratum = stratum
    ensure(trace_stratum is not None, "TRACE side exists")

    interior_sign = (
        graph_derivative
        if endpoint == "LOWER"
        else sign_opposite(graph_derivative)
    )
    slice_identity = {
        "analytic_root_row_id": root_id,
        "stratum_kind":
            "ONE_DIMENSIONAL_ROOT_SLICE_WITH_ROOT_POINT_REMOVED",
    }
    slice_id = key_id("symbolic-stratum", slice_identity)
    strata.append(seal({
        "symbolic_stratum_row_id": slice_id,
        **slice_identity,
        "Round219_terminal_subface_row_id":
            old["terminal_subface_row_id"],
        "contact_row_id": old["contact_row_id"],
        "topological_dimension": 1,
        "transverse_coordinate": "ANALYTIC_ROOT",
        "graph_domain":
            "GRAPH_INTERVAL_WITH_THE_ROOT_ENDPOINT_REMOVED",
        "strict_interior_active_factor_sign": interior_sign,
        "strict_graph_derivative_sign": graph_derivative,
        "classification":
            "ROOT_SLICE_ZERO_ABSENT_AWAY_FROM_ROOT_POINT",
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
    point_id = key_id("symbolic-stratum", point_identity)
    join_identity = {
        "analytic_root_row_id": root_id,
        "root_point_stratum_row_id": point_id,
        "trace_stratum_row_id":
            trace_stratum["symbolic_stratum_row_id"],
        "restricted_zero_curve_row_id":
            trace_stratum["restricted_zero_curve_row_id"],
    }
    join_id = key_id("endpoint-to-curve-join", join_identity)
    point = seal({
        "symbolic_stratum_row_id": point_id,
        **point_identity,
        "Round219_terminal_subface_row_id":
            old["terminal_subface_row_id"],
        "contact_row_id": old["contact_row_id"],
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
    join = seal({
        "endpoint_to_curve_join_row_id": join_id,
        **join_identity,
        "root_point_stratum_row_sha256": point["row_sha256"],
        "trace_stratum_row_sha256": trace_stratum["row_sha256"],
        "contact_row_id": old["contact_row_id"],
        "negative_side_leaf_row_id":
            old["negative_side_leaf_row_id"],
        "positive_side_leaf_row_id":
            old["positive_side_leaf_row_id"],
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


def expected_whole_stratum(
    old: dict[str, Any],
    terminal: dict[str, Any],
) -> dict[str, Any]:
    ensure(
        terminal["classification"].endswith("ZERO_ABSENT"),
        "whole edge no root",
    )
    edge_sign = terminal["lower_transverse_endpoint_sign"]
    ensure(
        edge_sign == terminal["upper_transverse_endpoint_sign"]
        and edge_sign in STRICT,
        "whole edge sign",
    )
    old_signs = old["selected_lower_upper_derivative_signs"]
    graph_signs = (
        [edge_sign, old_signs[1], old_signs[2]]
        if terminal["graph_endpoint"] == "LOWER"
        else [old_signs[0], edge_sign, old_signs[2]]
    )
    ensure(all(sign in STRICT for sign in graph_signs),
           "whole strip strict signs")
    classification = (
        "TRACE" if graph_signs[0] != graph_signs[1] else "ABSENT"
    )
    identity = {
        "Round219_terminal_subface_row_id":
            old["terminal_subface_row_id"],
        "stratum_kind": "TWO_DIMENSIONAL_WHOLE_RATIONAL_STRIP",
    }
    stratum_id = key_id("symbolic-stratum", identity)
    if classification == "TRACE":
        curve, negative, positive, glue = expected_trace_ids(
            stratum_id, old
        )
    else:
        curve = negative = positive = glue = None
    return seal({
        "symbolic_stratum_row_id": stratum_id,
        **identity,
        "contact_row_id": old["contact_row_id"],
        "topological_dimension": 2,
        "graph_interval": copy.deepcopy(old["graph_interval"]),
        "transverse_interval": copy.deepcopy(old["transverse_interval"]),
        "selected_lower_upper_graph_derivative_signs": graph_signs,
        "classification": classification,
        "classification_derived_from_complete_zero-free_endpoint_edge":
            True,
        "restricted_zero_curve_row_id": curve,
        "negative_side_incidence_row_id": negative,
        "negative_side_leaf_row_id":
            old["negative_side_leaf_row_id"],
        "positive_side_incidence_row_id": positive,
        "positive_side_leaf_row_id":
            old["positive_side_leaf_row_id"],
        "exact_common_refinement_glue_row_id": glue,
        "formal_two_dimensional_trace_stratum_credit":
            int(classification == "TRACE"),
        "formal_two_dimensional_zero_absence_stratum_credit":
            int(classification == "ABSENT"),
        "formal_local_incidence_credit":
            2 * int(classification == "TRACE"),
        "formal_local_glue_credit": int(classification == "TRACE"),
        "formal_component_deduplication_credit": 0,
        "whole_origin_credit": 0,
        "global_component_credit": 0,
        "global_fibre_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })


def expected_contact_completion(
    contact: dict[str, Any],
    old_rows: list[dict[str, Any]],
    partitions: list[dict[str, Any]],
    strata: list[dict[str, Any]],
) -> dict[str, Any]:
    ensure(
        len(old_rows)
        == contact["UNRESOLVED_terminal_subface_count"]
        == len(partitions)
        and all(
            row["formal_edge_partition_complete_credit"] == 1
            and row["edge_root_set_complete"] is True
            for row in partitions
        ),
        "contact replacement",
    )
    identity = {
        "Round219_exact_contact_row_id": contact["exact_contact_row_id"],
        "Round219_exact_contact_row_sha256": contact["row_sha256"],
    }
    return seal({
        "completed_contact_row_id":
            key_id("completed-exact-contact", identity),
        **identity,
        "official_key_ordinal": contact["official_key_ordinal"],
        "fixed_axis": contact["fixed_axis"],
        "Round219_inherited_resolved_terminal_subface_count":
            contact["terminal_subface_count"]
            - contact["UNRESOLVED_terminal_subface_count"],
        "replaced_Round219_UNRESOLVED_terminal_subface_count":
            len(old_rows),
        "old_UNRESOLVED_terminal_subface_rows_sha256": object_hash([
            [row["terminal_subface_row_id"], row["row_sha256"]]
            for row in sorted(
                old_rows,
                key=lambda item: item["terminal_subface_row_id"],
            )
        ]),
        "endpoint_edge_partition_rows_sha256": object_hash([
            [
                row["endpoint_edge_partition_row_id"],
                row["row_sha256"],
            ]
            for row in sorted(
                partitions,
                key=lambda item: item["endpoint_edge_partition_row_id"],
            )
        ]),
        "replacement_symbolic_stratum_count": len(strata),
        "replacement_symbolic_strata_sha256": object_hash([
            [row["symbolic_stratum_row_id"], row["row_sha256"]]
            for row in sorted(
                strata,
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


def expected_result() -> dict[str, Any]:
    ensure(
        Path(r219.__file__).resolve() == (HERE / R219_SOURCE).resolve()
        and Path(r186.__file__).resolve() == (HERE / R186_SOURCE).resolve(),
        "dependency module identity",
    )
    pin(HERE / PRODUCER, PRODUCER_SHA256, 5_000_000)
    pin(HERE / R219_SOURCE, R219_SOURCE_SHA256, 5_000_000)
    pin(HERE / R219_MANIFEST, R219_MANIFEST_SHA256, 10_000)
    pin(HERE / R186_SOURCE, R186_SOURCE_SHA256, 5_000_000)
    raw219 = pin(
        HERE / R219_CERTIFICATE,
        R219_CERTIFICATE_SHA256,
        MAX_BYTES,
    )
    envelope219 = strict_decode(raw219)
    ensure(
        set(envelope219) == {"schema", "result", "result_sha256"}
        and envelope219["result_sha256"] == R219_RESULT_SHA256
        and object_hash(envelope219["result"]) == R219_RESULT_SHA256,
        "Round219 result closure",
    )
    result219 = envelope219["result"]
    terminal219 = inspect_ledger(
        result219["formal_terminal_subface_ledger"],
        "terminal_subface_row_id",
    )
    contacts219 = inspect_ledger(
        result219["formal_exact_contact_partition_ledger"],
        "exact_contact_row_id",
    )
    unresolved = [
        row for row in terminal219
        if row["classification"] == "UNRESOLVED"
    ]
    incomplete = [
        row for row in contacts219
        if row[
            "formal_exact_contact_common_refinement_complete_credit"
        ] == 0
    ]
    ensure(
        len(unresolved) == UNRESOLVED_ROWS
        and len(incomplete) == INCOMPLETE_CONTACTS,
        "Round219 exact boundary",
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

    partitions: list[dict[str, Any]] = []
    terminals: list[dict[str, Any]] = []
    roots: list[dict[str, Any]] = []
    strata: list[dict[str, Any]] = []
    joins: list[dict[str, Any]] = []
    partitions_by_contact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    old_by_contact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    strata_by_contact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    print(
        "Round223 verifier rebuilding 7236 endpoint-edge partitions",
        file=sys.stderr,
    )
    for index, old in enumerate(unresolved, 1):
        frontier = frontier_by_id[old["Round217_frontier_row_id"]]
        partition, child_rows = expected_partition(old, frontier)
        partitions.append(partition)
        terminals.extend(child_rows)
        partitions_by_contact[old["contact_row_id"]].append(partition)
        old_by_contact[old["contact_row_id"]].append(old)
        root_terminal = next(
            (
                row for row in child_rows
                if row["classification"] == "UNIQUE_INTERIOR_ROOT"
            ),
            None,
        )
        if root_terminal is None:
            ensure(len(child_rows) == 1, "direct no-root edge")
            stratum = expected_whole_stratum(old, child_rows[0])
            strata.append(stratum)
            strata_by_contact[old["contact_row_id"]].append(stratum)
        else:
            root = expected_root(
                old, frontier, partition, root_terminal
            )
            root_strata, join = expected_root_strata(old, root)
            roots.append(root)
            strata.extend(root_strata)
            joins.append(join)
            strata_by_contact[old["contact_row_id"]].extend(root_strata)
        if index % 1000 == 0:
            print(
                f"Round223 verifier endpoint edges {index}/{len(unresolved)}",
                file=sys.stderr,
            )
    completed = [
        expected_contact_completion(
            contact_by_id[contact_id],
            old_by_contact[contact_id],
            partitions_by_contact[contact_id],
            strata_by_contact[contact_id],
        )
        for contact_id in sorted(old_by_contact)
    ]
    for rows, id_key in (
        (partitions, "endpoint_edge_partition_row_id"),
        (terminals, "edge_terminal_segment_row_id"),
        (roots, "analytic_root_row_id"),
        (strata, "symbolic_stratum_row_id"),
        (joins, "endpoint_to_curve_join_row_id"),
        (completed, "completed_contact_row_id"),
    ):
        rows.sort(key=lambda row, id_key=id_key: row[id_key])
        ensure(
            len({row[id_key] for row in rows}) == len(rows),
            f"unique expected:{id_key}",
        )
        for row in rows:
            payload = dict(row)
            row_hash = payload.pop("row_sha256")
            ensure(object_hash(payload) == row_hash,
                   f"closed expected:{id_key}")

    methods = Counter(row["partition_method"] for row in partitions)
    root_counts = Counter(
        row["unique_interior_root_terminal_count"]
        for row in partitions
    )
    terminal_classes = Counter(row["classification"] for row in terminals)
    depth_counts = Counter(
        row["adaptive_completion_depth"]
        for row in partitions
        if row["partition_method"] == "ADAPTIVE_RATIONAL_EDGE_PARTITION"
    )
    kind_counts = Counter(row["stratum_kind"] for row in strata)
    dimension_counts = Counter(
        row["topological_dimension"] for row in strata
    )
    two_classes = Counter(
        row["classification"] for row in strata
        if row["topological_dimension"] == 2
    )
    whole = [
        row for row in strata
        if row["stratum_kind"]
        == "TWO_DIMENSIONAL_WHOLE_RATIONAL_STRIP"
    ]
    whole_classes = Counter(row["classification"] for row in whole)
    ensure(
        len(partitions) == PARTITIONS
        and len(terminals) == TERMINALS
        and len(roots) == ROOTS
        and len(strata) == STRATA
        and len(joins) == JOINS
        and len(completed) == COMPLETED
        and methods
        == Counter({
            "DIRECT_FULL_EDGE_MONOTONE_OR_INTERVAL": 6_984,
            "ADAPTIVE_RATIONAL_EDGE_PARTITION": 252,
        })
        and root_counts == Counter({1: ROOTS, 0: 4})
        and terminal_classes["UNIQUE_INTERIOR_ROOT"] == ROOTS
        and sum(
            value for key, value in terminal_classes.items()
            if key.endswith("ZERO_ABSENT")
        ) == ABSENCE_TERMINALS
        and depth_counts == Counter({2: 88, 3: 84, 4: 64, 5: 16})
        and kind_counts["TWO_DIMENSIONAL_OPEN_ROOT_SIDE"] == 14_464
        and kind_counts[
            "ONE_DIMENSIONAL_ROOT_SLICE_WITH_ROOT_POINT_REMOVED"
        ] == ROOTS
        and kind_counts[
            "ZERO_DIMENSIONAL_ENDPOINT_ROOT_POINT"
        ] == ROOTS
        and dimension_counts[2] == 14_468
        and dimension_counts[1] == ROOTS
        and dimension_counts[0] == ROOTS,
        "independent Round223 census",
    )
    ordinals = Counter(row["official_key_ordinal"] for row in completed)
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
                len(unresolved),
            "Round219_incomplete_exact_contact_count":
                len(incomplete),
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
            "adaptive_partition_maximum_depth": MAX_EDGE_DEPTH,
            "edge_terminal_owner_rule":
                "LEFT_CLOSED_RIGHT_OPEN_EXCEPT_FINAL_RIGHT_CLOSED",
            "root_is_shared_by_both_open_sides_root_slice_and_root_point":
                True,
            "numeric_root_approximation_used_as_exact_coordinate": False,
        },
        "formal_endpoint_edge_scope": {
            "endpoint_edge_partition_count": len(partitions),
            "direct_unique_root_partition_count": 6_980,
            "direct_zero_absence_partition_count": 4,
            "adaptive_unique_root_partition_count": 252,
            "analytic_unique_root_count": len(roots),
            "terminal_edge_segment_count": len(terminals),
            "terminal_unique_root_segment_count":
                terminal_classes["UNIQUE_INTERIOR_ROOT"],
            "terminal_zero_absence_segment_count": ABSENCE_TERMINALS,
            "adaptive_completion_depth_histogram": {
                str(key): value
                for key, value in sorted(depth_counts.items())
            },
            "all_endpoint_edge_root_sets_complete": True,
            "remaining_UNRESOLVED_endpoint_edge_segment_count": 0,
        },
        "formal_symbolic_stratum_scope": {
            "symbolic_stratum_count": len(strata),
            "two_dimensional_open_root_side_count": 14_464,
            "one_dimensional_root_slice_count": ROOTS,
            "zero_dimensional_root_point_count": ROOTS,
            "two_dimensional_whole_rational_strip_count": len(whole),
            "two_dimensional_TRACE_count": two_classes["TRACE"],
            "two_dimensional_ABSENT_count": two_classes["ABSENT"],
            "whole_rational_strip_classification_count":
                dict(sorted(whole_classes.items())),
            "endpoint_to_curve_join_count": len(joins),
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
                len(completed),
            "cumulative_complete_exact_p_s_contact_count": 7_932,
            "total_exact_p_s_contact_count": 7_932,
            "remaining_incomplete_exact_p_s_contact_count": 0,
            "cumulative_identity": "916+7016=7932",
            "new_complete_official_key_ordinal_count": len(ordinals),
            "new_complete_contacts_per_official_key_ordinal": {
                str(key): value for key, value in sorted(ordinals.items())
            },
            "new_complete_contacts_per_official_key_ordinal_sha256":
                object_hash(dict(sorted(ordinals.items()))),
            "physical_component_equivalence_relation_complete": False,
        },
        "formal_endpoint_edge_partition_ledger":
            make_ledger(partitions, "endpoint_edge_partition_row_id"),
        "formal_edge_terminal_segment_ledger":
            make_ledger(terminals, "edge_terminal_segment_row_id"),
        "formal_analytic_root_ledger":
            make_ledger(roots, "analytic_root_row_id"),
        "formal_symbolic_stratum_ledger":
            make_ledger(strata, "symbolic_stratum_row_id"),
        "formal_endpoint_to_curve_join_ledger":
            make_ledger(joins, "endpoint_to_curve_join_row_id"),
        "formal_completed_exact_contact_ledger":
            make_ledger(completed, "completed_contact_row_id"),
        "first_missing_frontier": {
            "remaining_incomplete_exact_p_s_contact_count": 0,
            "remaining_partial_contact_count": 236,
            "partial_contact_symbolic_root_stratification_missing": True,
            "complete_physical_component_equivalence_closure_missing":
                True,
            "global_occurrence_fibre_exhaustion_missing": True,
        },
        "formal_credit_contract": {
            "formal_analytic_root_credits": len(roots),
            "formal_endpoint_to_curve_join_credits": len(joins),
            "formal_two_dimensional_trace_stratum_credits":
                two_classes["TRACE"],
            "formal_two_dimensional_zero_absence_stratum_credits":
                two_classes["ABSENT"],
            "formal_one_dimensional_root_slice_zero_absence_credits":
                ROOTS,
            "formal_zero_dimensional_root_point_credits": ROOTS,
            "formal_exact_contact_symbolic_stratification_complete_"
            "credits": len(completed),
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
            "apply the same exact analytic-root stratification to the "
            "236 partial contacts, then use only proved local glue and "
            "endpoint-join edges to close the physical-component "
            "equivalence relation and global occurrence fibres"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": PRODUCER_SHA256,
            "python_version": sys.version.split()[0],
            "python_flint_version":
                getattr(__import__("flint"), "__version__", "unknown"),
            "effective_Arb_precision_bits": ctx.prec,
            "Round221_probe_imported_or_executed": False,
            "formal_upstream_files_modified": False,
        },
    }


LEDGERS = (
    (
        "formal_endpoint_edge_partition_ledger",
        "endpoint_edge_partition_row_id",
    ),
    (
        "formal_edge_terminal_segment_ledger",
        "edge_terminal_segment_row_id",
    ),
    ("formal_analytic_root_ledger", "analytic_root_row_id"),
    ("formal_symbolic_stratum_ledger", "symbolic_stratum_row_id"),
    (
        "formal_endpoint_to_curve_join_ledger",
        "endpoint_to_curve_join_row_id",
    ),
    (
        "formal_completed_exact_contact_ledger",
        "completed_contact_row_id",
    ),
)


def verify_envelope(
    envelope: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    ensure(
        set(envelope) == {"schema", "result", "result_sha256"}
        and envelope["schema"] == SCHEMA
        and envelope["result_sha256"] == object_hash(envelope["result"]),
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
    root_key = "formal_analytic_root_ledger"
    partition_key = "formal_endpoint_edge_partition_ledger"
    terminal_key = "formal_edge_terminal_segment_ledger"
    stratum_key = "formal_symbolic_stratum_ledger"
    join_key = "formal_endpoint_to_curve_join_ledger"
    contact_key = "formal_completed_exact_contact_ledger"

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
        row["strict_full_transverse_derivative_sign"] = sign_opposite(
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
            == "ZERO_DIMENSIONAL_ENDPOINT_ROOT_POINT"
        )
        rows.pop(index)
        return {stratum_key}

    def drop_root_slice(result: dict[str, Any]) -> set[str]:
        rows = result[stratum_key]["rows"]
        index = next(
            index for index, row in enumerate(rows)
            if row["stratum_kind"]
            == "ONE_DIMENSIONAL_ROOT_SLICE_WITH_ROOT_POINT_REMOVED"
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

    def change_terminal(result: dict[str, Any]) -> set[str]:
        row = next(
            row for row in result[terminal_key]["rows"]
            if row["classification"] == "UNIQUE_INTERIOR_ROOT"
        )
        row["classification"] = "STRICT_INTERVAL_ZERO_ABSENT"
        row["formal_edge_unique_root_credit"] = 0
        row["formal_edge_zero_absence_credit"] = 1
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
        result["formal_exact_contact_scope"][
            "remaining_incomplete_exact_p_s_contact_count"
        ] = 1
        return set()

    def root_embedded_in_strip(result: dict[str, Any]) -> set[str]:
        result["formal_symbolic_stratum_scope"][
            "root_point_is_separate_from_two_dimensional_strips"
        ] = False
        return set()

    def numeric_contract(result: dict[str, Any]) -> set[str]:
        result["formal_analytic_root_contract"][
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
        change_terminal,
        false_contact,
        drop_contact,
        summary_remaining,
        root_embedded_in_strip,
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
    # One candidate-sized duplicate-key attack confirms nested duplicates.
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
        prefix=".round223_path_", dir=HERE
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
        wrong = HERE / f".round223_wrong_{token}.json"
        wrong.write_bytes(b"{}\n")
        cleanup.append(wrong)
        reject_output(wrong)
        output_dir = HERE / (
            f".{PREFIX}_verification_replay_directory_{token}.json"
        )
        output_dir.mkdir()
        cleanup.append(output_dir)
        reject_output(output_dir)
        # Three additional protected-formal-name attacks.
        reject_output(HERE / PRODUCER)
        reject_output(HERE / CERTIFICATE)
        reject_output(HERE / Path(__file__).name)
        for path in reversed(cleanup):
            if path.is_symlink() or path.is_file() or stat.S_ISFIFO(
                path.lstat().st_mode
            ):
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

    # The full expected object is complete before candidate loading.
    expected = expected_result()
    print("Round223 verifier now loading candidate", file=sys.stderr)
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
        f"Round223 hostile semantic={semantic_rejected}/"
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
        "status": "PASS_PARTIAL_FORMAL_ROUND223",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": RESULT_SHA256,
        "verifier_sha256": verifier_sha,
        "full_expected_Python_object_equality": True,
        "full_expected_canonical_equality": True,
        "endpoint_edge_partition_rows_verified": PARTITIONS,
        "edge_terminal_segment_rows_verified": TERMINALS,
        "analytic_root_rows_verified": ROOTS,
        "symbolic_stratum_rows_verified": STRATA,
        "endpoint_to_curve_join_rows_verified": JOINS,
        "completed_exact_contact_rows_verified": COMPLETED,
        "cumulative_exact_p_s_contact_count_verified": 7_932,
        "remaining_incomplete_exact_p_s_contact_count_verified": 0,
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
