#!/usr/bin/env python3
"""C40: dimension-safe H1/endpoint/collision-two arrangement over C39.

This producer performs up to two adaptive dyadic refinements of every rational
C39 residual leaf, replays the collision-one router, and applies the pinned
Round185 centered-C1 collision-two machinery only after collision one and its
outgoing W chart are strict.  H1 carriers, source/algebraic endpoint charts,
and multi-Delta carriers are materialized in separate ledgers.  A graph,
endpoint, or incidence outer never earns ambient or whole-parent credit.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import itertools
import json
import math
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import flint
from flint import ctx

import cm2_round185_preconditioned_c1_residual_refinement as round185
import cm2_round306c38_d02_collision1_2_representative_child_atlas_v1 as c38
import cm2_round306c39_d02_h1_c1_graph_cell_router_v1 as c39


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

SCHEMA = "cm2.round306c40.d02-h1-endpoint-collision2-arrangement.v1"
LEAF_SCHEMA = "cm2.round306c40.routed-leaf-cell.v1"
H1_SCHEMA = "cm2.round306c40.h1-graph-cell.v1"
ENDPOINT_SCHEMA = "cm2.round306c40.endpoint-chart.v1"
C2_SCHEMA = "cm2.round306c40.collision2-multi-delta-cell.v1"
C2_SOURCE_SCHEMA = "cm2.round306c40.collision2-source-candidate-census.v1"
PARENT_SCHEMA = "cm2.round306c40.parent-conservation.v1"
RECEIPT_SCHEMA = "cm2.round306c40.execution-receipt.v1"

PRECISION_BITS = 384
EXTRA_DEPTH = 2
FROZEN_OWNER = "W[1,0]"
EXPECTED_C39_OBJECT = "821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02"
EXPECTED_C39_AUDIT_OBJECT = (
    "5eccca7db5a473db6fbd67f7f0eda0f582a52b51b3aab5895316e83777358182"
)
EXPECTED_C39_SOURCE = "873a84cb150efc5649ffb5822457c510ab45c32f3e16a48914c8674dc93c0aae"
EXPECTED_ROUND185_SOURCE = (
    "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2"
)
EXPECTED_BOUNDARY_SEPARATION_OBJECT = (
    "4b0ce3d81b7a4957f35bb233d46c1f332ca2e60a00751396c6b3d97b8e8db7cc"
)
EXPECTED_C38_OBJECT = c39.EXPECTED_C38_OBJECT
INVOCATION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{15,127}\Z")
C39_COLLISION2_TARGETS = {
    "UNRESOLVED_COLLISION2_OWNER",
    "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION2_OWNER",
    "UNRESOLVED_C39_H1_W_SIDE_COLLISION2_OWNER",
}
EXPECTED_C39_COLLISION2_RAW_CENSUS = {
    "INTERSECTION_BEHIND": 5881,
    "NO_REAL_INTERSECTION": 285281,
    "STRICT_FUTURE": 10589,
    "UNRESOLVED_DELTA": 40875,
    "UNRESOLVED_ROOT_SIGN": 134,
}
EXPECTED_ROUTE_EXCEPTION_EVIDENCE_CENSUS = {
    (
        "UNRESOLVED_C40_SOURCE_RADICAL_ENDPOINT_ROUTE_EVALUATION_FAILURE_OUTER",
        "Round185Error",
        "AD sqrt domain",
    ): 200,
    (
        "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER",
        "KeyError",
        "'uncached chart:W:W'",
    ): 19,
}


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def strict_json(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key:{path}:{key}")
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=unique,
        parse_float=lambda item: (_ for _ in ()).throw(ValueError(item)),
        parse_constant=lambda item: (_ for _ in ()).throw(ValueError(item)),
    )
    require(type(value) is dict, f"top object:{path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical(value) + b"\n")


def validate_object(
    value: dict[str, Any], field: str, expected: str, label: str,
) -> None:
    semantic = dict(value)
    recorded = semantic.pop(field, None)
    require(recorded == expected == digest(semantic), f"object:{label}")


def validate_manifest(directory: Path) -> None:
    rows = (directory / "root_manifest.sha256").read_text(
        encoding="utf-8"
    ).splitlines()
    names: list[str] = []
    for row in rows:
        expected, name = row.split("  ", 1)
        require(name not in names, f"manifest duplicate:{name}")
        names.append(name)
        path = directory / name
        require(path.is_file() and file_sha256(path) == expected, f"manifest:{path}")
    require(names == sorted(names), f"manifest order:{directory}")


def write_manifest(directory: Path) -> None:
    members = sorted(
        path for path in directory.iterdir() if path.name != "root_manifest.sha256"
    )
    (directory / "root_manifest.sha256").write_text(
        "".join(f"{file_sha256(path)}  {path.name}\n" for path in members),
        encoding="utf-8",
    )


class LedgerWriter:
    def __init__(self, path: Path, order: str) -> None:
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.stream: Any = None

    def __enter__(self) -> "LedgerWriter":
        self.raw = self.path.open("wb")
        self.stream = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, row: dict[str, Any]) -> None:
        require("row_sha256" not in row, "writer row open")
        row_sha = digest(row)
        self.stream.write(canonical({**row, "row_sha256": row_sha}) + b"\n")
        self.sequence.update((row_sha + "\n").encode("ascii"))
        self.count += 1

    def __exit__(self, *_args: Any) -> None:
        self.stream.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha256(self.path),
            "size": self.path.stat().st_size,
        }


def source_pins() -> dict[str, str]:
    values = {
        "C39": file_sha256(Path(c39.__file__).resolve()),
        "Round185": file_sha256(Path(round185.__file__).resolve()),
        "C38": file_sha256(Path(c38.__file__).resolve()),
    }
    require(values["C39"] == EXPECTED_C39_SOURCE, "C39 source pin")
    require(values["Round185"] == EXPECTED_ROUND185_SOURCE, "Round185 source pin")
    require(values["C38"] == c39.EXPECTED_C38_SOURCE, "C38 source pin")
    c39.source_pins()
    require(flint.__version__ == "0.9.0", "python-flint version")
    separation = round185.r181.boundary_separation_registry()
    require(
        digest(separation) == EXPECTED_BOUNDARY_SEPARATION_OBJECT
        and separation["candidate_count"] == 55
        and separation["pair_count"] == 1485
        and separation["minimum_strict_squared_margin"] == "36337/160000"
        and separation["pair_rows_sha256"]
        == "36b22055587a22a003fa57a4c29c5cd6cc730af567e1354f5c72f317991a1ce2",
        "candidate boundary separation registry",
    )
    tuple_codec_self_test()
    return values


def source_identifier(row: dict[str, Any]) -> str:
    return row.get("c39_routed_child_pair_id", "c39-row:" + row["row_sha256"])


def box_payload(box: Any) -> dict[str, Any]:
    return {
        "t": [qstr(box.t0), qstr(box.t1)],
        "p": [qstr(box.p0), qstr(box.p1)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def reflected_payload(chart: str, box: Any) -> dict[str, Any]:
    if chart in {"E", "W"}:
        reflected_chart = chart
        t_interval = (-box.t1, -box.t0)
    else:
        reflected_chart = {"N": "S", "S": "N"}[chart]
        t_interval = (box.t0, box.t1)
    return {
        "compact_chart": reflected_chart,
        "t": [qstr(value) for value in t_interval],
        "p": [qstr(-box.p1), qstr(-box.p0)],
        "s": [qstr(box.s0), qstr(box.s1)],
    }


def encoded_tuple_map(value: dict[tuple[str, ...], int]) -> dict[str, int]:
    require(type(value) is dict, "tuple codec encode map")
    encoded: dict[str, int] = {}
    for key, item in value.items():
        require(
            type(key) is tuple
            and all(type(part) is str for part in key)
            and type(item) is int,
            "tuple codec encode domain",
        )
        canonical_key = canonical(list(key)).decode("utf-8")
        require(canonical_key not in encoded, "tuple codec encoded collision")
        encoded[canonical_key] = item
    require(len(encoded) == len(value), "tuple codec encode cardinality")
    return encoded


def decoded_tuple_map(value: dict[str, int]) -> dict[tuple[str, ...], int]:
    require(type(value) is dict, "tuple codec decode map")
    decoded: dict[tuple[str, ...], int] = {}
    for encoded_key, item in value.items():
        require(
            type(encoded_key) is str and type(item) is int,
            "tuple codec decode domain",
        )
        try:
            parts = json.loads(
                encoded_key,
                parse_float=lambda token: (_ for _ in ()).throw(
                    ValueError(token)
                ),
                parse_constant=lambda token: (_ for _ in ()).throw(
                    ValueError(token)
                ),
            )
        except Exception as error:
            raise RuntimeError("tuple codec key is not strict JSON") from error
        require(
            type(parts) is list
            and all(type(part) is str for part in parts),
            "tuple codec decoded string list",
        )
        require(
            canonical(parts).decode("utf-8") == encoded_key,
            "tuple codec noncanonical key",
        )
        key = tuple(parts)
        require(key not in decoded, "tuple codec duplicate decoded key")
        decoded[key] = item
    require(len(decoded) == len(value), "tuple codec decode cardinality")
    return decoded


def tuple_codec_self_test() -> None:
    probe = {
        (): 0,
        ("",): 1,
        ("\u001f",): 2,
        ("a", "b"): 3,
        ("a\u001fb",): 4,
        ('["', '","'): 5,
        ("雪",): 6,
        ("", ""): 7,
    }
    encoded = encoded_tuple_map(probe)
    require(
        decoded_tuple_map(encoded) == probe
        and encoded["[]"] == 0
        and encoded['[""]'] == 1,
        "tuple codec complete round trip",
    )
    hostile = [
        {"": 0},
        {"[ ]": 0},
        {"{}": 0},
        {"[1]": 0},
        {'["a",]': 0},
        {'["a"]': True},
        {'["a"]': 0, '["\\u0061"]': 1},
    ]
    for attack in hostile:
        try:
            decoded_tuple_map(attack)
        except Exception:
            continue
        raise RuntimeError("tuple codec hostile input accepted")


def compact_surface(evidence: dict[str, Any]) -> dict[str, Any]:
    derivatives = evidence.get("full_box_C1_derivatives", {})
    return {
        "kind": evidence.get("kind"),
        "identifier": evidence.get("identifier"),
        "equation": evidence.get("equation"),
        "centered_C0_sign": evidence.get("centered_C0_sign"),
        "centered_mean_value_C0_enclosure": evidence.get(
            "centered_mean_value_C0_enclosure"
        ),
        "full_box_C1_derivatives": derivatives,
        "strict_derivative_axes": [
            axis for axis in ("dt", "dp")
            if axis in derivatives and not derivatives[axis]["contains_zero"]
        ],
        "axis_full_face_brackets_t_p_s": evidence.get(
            "axis_full_face_brackets_t_p_s", []
        ),
        "axis_interval_Newton": evidence.get("axis_interval_Newton", []),
        "strict_corner_segment_bracket": evidence.get(
            "strict_corner_segment_bracket"
        ),
        "independently_certified_nonempty": evidence.get(
            "independently_certified_nonempty", False
        ),
        "evidence_sha256": digest(evidence),
    }


def certified_nonempty_regular_graph(
    evidence: dict[str, Any] | None,
) -> bool:
    """Require both existence and a strict in-slice derivative for graph credit."""
    if evidence is None:
        return False
    compact = compact_surface(evidence)
    return bool(
        compact["independently_certified_nonempty"]
        and compact["strict_derivative_axes"]
    )


def endpoint_phase(box: Any) -> str | None:
    if box.p0 == -1 or box.p1 == 1:
        return "SOURCE_RADICAL_1_MINUS_P2_ENDPOINT"
    return None


def source_radical_failure_replay(
    parent_key: str,
    box: Any,
    caught: Exception,
) -> dict[str, Any]:
    """Bind a router failure to an independent initial-geometry replay."""
    semantic: dict[str, Any] = {
        "attempted": endpoint_phase(box) is not None,
        "matched_caught_exception": False,
        "replay_is_source_sqrt_domain_failure": False,
        "source_radical_causal_match": False,
        "replay_exception_type": None,
        "replay_exception_module": None,
        "replay_exception_message": None,
    }
    if not semantic["attempted"]:
        return semantic
    try:
        round185.ad_initial_geometry(parent_key, box)
    except Exception as replay:
        matched = (
            type(replay).__module__ == type(caught).__module__
            and type(replay).__name__ == type(caught).__name__
            and str(replay) == str(caught)
        )
        source_sqrt = (
            type(replay).__name__ == "Round185Error"
            and str(replay) == "AD sqrt domain"
        )
        semantic.update({
            "matched_caught_exception": matched,
            "replay_is_source_sqrt_domain_failure": source_sqrt,
            "source_radical_causal_match": matched and source_sqrt,
            "replay_exception_type": type(replay).__name__,
            "replay_exception_module": type(replay).__module__,
            "replay_exception_message": str(replay),
        })
    return semantic


def endpoint_exception(parent_key: str, box: Any) -> tuple[str, str, str]:
    if box.p0 == -1 or box.p1 == 1:
        return (
            "SOURCE_RADICAL_1_MINUS_P2_ENDPOINT",
            "EXACT_SOURCE_RADICAL_BOUNDARY",
            "q_source^2=1-p^2 and q_source=0 at p=+/-1",
        )
    try:
        initial = round185.ad_initial_geometry(parent_key, box)
    except Exception as error:
        raise RuntimeError(
            "interior initial-geometry evaluation failure:"
            + type(error).__name__ + ":" + str(error)
        ) from error
    try:
        round185.collision1_h1_ad(parent_key, box, FROZEN_OWNER)
    except Exception as error:
        raw = round185.ad_root(initial, FROZEN_OWNER)
        require(
            box.p0 > -1 and box.p1 < 1
            and bool(raw["Delta"].value.contains(0)),
            "Delta1/H1 exception invariant",
        )
        return (
            "COLLISION1_DELTA1_H1_EVALUATION_FAILURE_OUTER",
            type(error).__name__,
            str(error),
        )
    return "NONE", "NONE", ""


def endpoint_row(
    leaf_id: str,
    source: dict[str, Any],
    c38_source: dict[str, Any],
    cell: dict[str, Any],
    box: Any | None,
    classification: str,
    seams: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if box is None:
        algebraic = [
            value for value in cell["physical_t_interval"]
            if value["kind"] == "ALGEBRAIC"
        ]
        require(len(algebraic) == 1, "single algebraic endpoint")
        endpoint = algebraic[0]
        require(seams is not None and bool(seams),
                "algebraic adjacent-chart seam incidence rows")
        phase = "ALGEBRAIC_SOURCE_CHART_H0_ENDPOINT"
        exception_type, exception_message = "NOT_EVALUATED", "exact endpoint chart"
        equations = [endpoint["minimal_polynomial"], "H0=2*t^2-1=0"]
        endpoint_index = next(
            index for index, value in enumerate(cell["physical_t_interval"])
            if value["kind"] == "ALGEBRAIC"
        )
        endpoint_payload: dict[str, Any] = {
            **endpoint,
            "exact_sign": (
                "NEGATIVE" if endpoint["value"].startswith("-") else "POSITIVE"
            ),
            "physical_interval_side": (
                "INTERIOR_ABOVE_ALGEBRAIC_ENDPOINT"
                if endpoint_index == 0 else "INTERIOR_BELOW_ALGEBRAIC_ENDPOINT"
            ),
            "horizontal_reflection_partner_cell_id": c38_source[
                "reflected_cell_id"
            ],
            "horizontal_reflection_partner_origin_key": c38_source[
                "reflected_origin_key"
            ],
            "horizontal_reflection_rule": (
                "(t,p)->(-t,-p)"
                if cell["compact_chart"] in {"E", "W"}
                else "(t,p)->(t,-p)"
            ),
            "horizontal_reflection_materialized_in_rational_box": False,
            "adjacent_chart_seam_incidence_count": len(seams),
            "adjacent_chart_seam_incidence": [
                {
                    "seam_segment_ordinal": segment_ordinal,
                    "seam_id": seam["seam_id"],
                    "face_id": seam["face_id"],
                    "seam_row_sha256": seam["row_sha256"],
                    "orientation": (
                        "RIGHT_TO_LEFT"
                        if seam["right_cell_id"] == cell["cell_id"]
                        else "LEFT_TO_RIGHT"
                    ),
                    "adjacent_cell_id": (
                        seam["left_cell_id"]
                        if seam["right_cell_id"] == cell["cell_id"]
                        else seam["right_cell_id"]
                    ),
                    "adjacent_chart": (
                        seam["left_chart"]
                        if seam["right_cell_id"] == cell["cell_id"]
                        else seam["right_chart"]
                    ),
                    "exact_physical_p_span": seam["physical_p_span"],
                    "exact_state_gluing_inherited_from_round162": seam[
                        "exact_state_gluing_inherited_from_round162"
                    ],
                }
                for segment_ordinal, seam in enumerate(seams)
            ],
        }
        expected_dimension = 1
        certified_dimension: int | None = 1
        existence_status = "CERTIFIED_EXACT_ALGEBRAIC_SOURCE_CHART_ENDPOINT"
        rank_status = "NOT_APPLICABLE_EXACT_CHART_BOUNDARY"
    else:
        phase, exception_type, exception_message = endpoint_exception(
            c38_source["representative_origin_key"], box
        )
        require(phase != "NONE", "endpoint exception phase")
        if phase == "SOURCE_RADICAL_1_MINUS_P2_ENDPOINT":
            equations = ["q_source^2=1-p^2", "q_source=0"]
            endpoint_payload = {
                "p_endpoint": "-1" if box.p0 == -1 else "1",
                "p_interval": [qstr(box.p0), qstr(box.p1)],
                "q_chart_orientation": "NONNEGATIVE_SQUARE_ROOT",
            }
            expected_dimension = 1
            certified_dimension = 1
            existence_status = "CERTIFIED_EXACT_SOURCE_RADICAL_ENDPOINT"
            rank_status = "NOT_APPLICABLE_EXACT_SOURCE_BOUNDARY"
        else:
            equations = [
                "candidate:Delta1=0",
                "candidate:H1=n1_x^2-n1_y^2=0",
            ]
            endpoint_payload = {
                "p_interval": [qstr(box.p0), qstr(box.p1)],
                "t_interval": [qstr(box.t0), qstr(box.t1)],
            }
            expected_dimension = 0
            certified_dimension = None
            existence_status = "UNRESOLVED_EVALUATION_FAILURE_OUTER"
            rank_status = "UNRESOLVED"
    semantic = {
        "schema": ENDPOINT_SCHEMA,
        "c40_leaf_id": leaf_id,
        "pair_index": source["pair_index"],
        "c39_source_row_sha256": source["row_sha256"],
        "c38_source_row_sha256": c38_source["row_sha256"],
        "classification": classification,
        "failure_phase": phase,
        "exception_target": "source sqrt" if phase.startswith("SOURCE_") else (
            "collision-one sqrt" if phase.startswith("COLLISION1_") else "exact algebraic H0"
        ),
        "exception_type": exception_type,
        "exception_message": exception_message,
        "chart_equations": equations,
        "endpoint": endpoint_payload,
        "ambient_slice_dimension": 2,
        "candidate_carrier_expected_dimension": expected_dimension,
        "certified_carrier_dimension": certified_dimension,
        "carrier_existence_status": existence_status,
        "candidate_intersection_rank_status": rank_status,
        "arrangement_status": (
            "EVALUATION_FAILURE_OUTER__EXISTENCE_AND_RANK_PENDING"
            if certified_dimension is None
            else "ENDPOINT_OUTER__SEAM_CONTINUATION_PENDING"
        ),
        "boundary_and_corner_inventory_complete": False,
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["endpoint_chart_id"] = "c40-endpoint:" + digest(semantic)
    return semantic


def h1_graph_row(
    leaf_id: str,
    source: dict[str, Any],
    c38_source: dict[str, Any],
    box: Any,
) -> dict[str, Any]:
    parent_key = c38_source["representative_origin_key"]
    try:
        evidence = round185.surface_evidence(
            "H1", parent_key, box, FROZEN_OWNER, include_axis_tests=True
        )
        compact = compact_surface(evidence)
        certified_graph = certified_nonempty_regular_graph(evidence)
        phase = (
            "H1_CERTIFIED_NONEMPTY_REGULAR_GRAPH"
            if certified_graph else "H1_POTENTIAL_SURFACE_OUTER"
        )
        exception_type = None
        exception_message = None
        brackets = compact["axis_full_face_brackets_t_p_s"]
        interior_axis_brackets = sum(bool(value) for value in brackets[:2])
    except Exception as error:
        phase, exception_type, exception_message = endpoint_exception(parent_key, box)
        if phase == "NONE":
            phase = "H1_SURFACE_EVIDENCE_EVALUATION_EXCEPTION"
            exception_type = type(error).__name__
            exception_message = str(error)
        compact = None
        certified_graph = False
        interior_axis_brackets = 0
    semantic = {
        "schema": H1_SCHEMA,
        "c40_leaf_id": leaf_id,
        "pair_index": source["pair_index"],
        "c39_source_row_sha256": source["row_sha256"],
        "c38_source_row_sha256": c38_source["row_sha256"],
        "surface_id": "H1:" + digest({
            "leaf": leaf_id,
            "parent": parent_key,
            "box": box_payload(box),
        }),
        "equation": "H1=n1_x^2-n1_y^2=0",
        "failure_phase": phase,
        "exception_type": exception_type,
        "exception_message": exception_message,
        "surface_evidence": compact,
        "ambient_slice_dimension": 2,
        "candidate_surface_expected_dimension": 1,
        "certified_carrier_dimension": 1 if certified_graph else None,
        "carrier_existence_status": (
            "CERTIFIED_NONEMPTY_REGULAR_GRAPH"
            if certified_graph else "UNRESOLVED_POTENTIAL_SURFACE_OUTER"
        ),
        "certified_nonempty_regular_graph": certified_graph,
        "open_chamber_signs": ["H1<0", "H1>0"],
        "boundary_face_family": ["t_lower", "t_upper", "p_lower", "p_upper"],
        "interior_axis_full_face_bracket_count": interior_axis_brackets,
        "boundary_intersection_outer_count": 4,
        "boundary_intersection_rows": [
            {"face": face, "status": "UNRESOLVED_OUTER", "credit": 0}
            for face in ("t_lower", "t_upper", "p_lower", "p_upper")
        ],
        "corner_family_count": 4,
        "half_open_policy": "strict sides disjoint; H1=0 retained once as event graph",
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["h1_graph_cell_id"] = "c40-h1:" + digest(semantic)
    return semantic


def expected_collision2(
    detail: dict[str, Any], config: dict[str, Any]
) -> tuple[str, str]:
    selected = detail["absolute_collision2_owner"]
    expected_by_owner = {
        config["original_path"][1]["selected_absolute_owner_id"]:
            config["original_path"][1],
        config["reflected_path"][1]["selected_absolute_owner_id"]:
            config["reflected_path"][1],
    }
    expected = expected_by_owner.get(selected)
    if expected is None:
        return "EXCLUDED_C40_COLLISION2_OWNER_MISMATCH", selected
    outgoing = detail.get("collision2_outgoing_chart")
    if outgoing != expected["outgoing_chart"]:
        return "EXCLUDED_C40_COLLISION2_CHART_MISMATCH", str(outgoing)
    word_id = detail["official_gate5_key"]["word_key_id"]
    if word_id != expected["official_word_key_id"]:
        return "EXCLUDED_C40_COLLISION2_WORD_MISMATCH", word_id
    branch = (
        "ORIGINAL"
        if selected == config["original_path"][1]["selected_absolute_owner_id"]
        else "REFLECTED"
    )
    return (
        f"UNRESOLVED_C40_LIVE_COLLISION2_{branch}_MATCH_NEEDS_COLLISION3_1648",
        selected,
    )


def candidate_disposition_inventory(
    parent_key: str,
    box: Any,
    leaf_id: str,
    include_surface_evidence: bool,
) -> dict[str, Any]:
    state = round185.r181.collision1_state_direct(parent_key, box)
    geometry = round185.r183.collision2_geometry(state)
    candidate_rows: list[dict[str, Any]] = []
    future: list[tuple[str, dict[str, Any]]] = []
    active: list[tuple[str, str, dict[str, Any] | None]] = []
    raw_census: Counter[str] = Counter()
    for identifier in round185.CANDIDATES:
        raw = round185.r181.raw_candidate(geometry, identifier)
        kind, data = round185.r178.root_record(*geometry, identifier)
        raw_census[kind] += 1
        near_bounds = None
        if data is not None and data.get("near") is not None:
            near_bounds = round185.arb_bounds(data["near"])
        surface: dict[str, Any] | None = None
        surface_error: dict[str, str] | None = None
        if kind in {"UNRESOLVED_DELTA", "UNRESOLVED_ROOT_SIGN"}:
            if include_surface_evidence and kind == "UNRESOLVED_DELTA":
                try:
                    surface = round185.surface_evidence(
                        "DELTA",
                        parent_key,
                        box,
                        identifier,
                        include_axis_tests=True,
                    )
                except Exception as error:
                    surface_error = {
                        "error_type": type(error).__name__,
                        "error_message": str(error),
                    }
            elif include_surface_evidence:
                surface_error = {
                    "error_type": "ROOT_SIGN_SURFACE_EVIDENCE_NOT_MATERIALIZED",
                    "error_message": (
                        "near=0 requires its own ell^2-Delta equivalence and "
                        "C0/C1 face proof; Delta=0 evidence is not substituted"
                    ),
                }
            active.append((identifier, kind, surface))
        if kind == "STRICT_FUTURE" and data is not None:
            future.append((identifier, data))
        candidate_rows.append({
            "candidate_ordinal": len(candidate_rows),
            "target_id": identifier,
            "raw_classification": kind,
            "ell": round185.arb_bounds(raw["ell"]),
            "Delta": round185.arb_bounds(raw["Delta"]),
            "transverse": round185.arb_bounds(raw["transverse"]),
            "near": near_bounds,
            "active_surface_kind": (
                "DELTA_ZERO" if kind == "UNRESOLVED_DELTA"
                else "NEAR_ROOT_ZERO" if kind == "UNRESOLVED_ROOT_SIGN"
                else None
            ),
            "surface_evidence": compact_surface(surface) if surface else None,
            "surface_evidence_error": surface_error,
        })
    require(
        tuple(row["target_id"] for row in candidate_rows)
        == tuple(round185.CANDIDATES),
        "ordered 55-candidate universe",
    )
    require(len(candidate_rows) == 55 and sum(raw_census.values()) == 55,
            "candidate census 55")

    future_pairs: list[dict[str, Any]] = []
    center_box = round185.point_box(
        box,
        (box.t0 + box.t1) / 2,
        (box.p0 + box.p1) / 2,
        (box.s0 + box.s1) / 2,
        ".c40-root-order-center",
    )
    center_state = round185.r181.collision1_state_direct(parent_key, center_box)
    center_geometry = round185.r183.collision2_geometry(center_state)
    for (left_id, left), (right_id, right) in itertools.combinations(future, 2):
        if bool(left["near"] < right["near"]):
            relation = "LEFT_STRICTLY_BEFORE_RIGHT"
        elif bool(right["near"] < left["near"]):
            relation = "RIGHT_STRICTLY_BEFORE_LEFT"
        else:
            left_kind, left_center = round185.r178.root_record(
                *center_geometry, left_id
            )
            right_kind, right_center = round185.r178.root_record(
                *center_geometry, right_id
            )
            require(
                left_kind == right_kind == "STRICT_FUTURE"
                and left_center is not None and right_center is not None,
                "strict center future pair",
            )
            if bool(left_center["near"] < right_center["near"]):
                relation = "LEFT_BEFORE_BY_CENTER_AND_SEPARATION"
            elif bool(right_center["near"] < left_center["near"]):
                relation = "RIGHT_BEFORE_BY_CENTER_AND_SEPARATION"
            else:
                raise RuntimeError("center root equality contradicts separation")
        future_pairs.append({
            "left_target_id": left_id,
            "right_target_id": right_id,
            "root_order_relation": relation,
            "root_equality_carrier": (
                "EMPTY_BY_PINNED_DISJOINT_BOUNDARY_SEPARATION"
            ),
            "equality_carrier_empty_by_boundary_registry": True,
            "boundary_separation_registry_sha256": (
                EXPECTED_BOUNDARY_SEPARATION_OBJECT
            ),
            "wall_or_order_credit": 0,
        })

    active_rows: list[dict[str, Any]] = []
    for identifier, kind, surface in active:
        surface_id = "c40-c2-surface:" + digest({
            "leaf": leaf_id,
            "target": identifier,
            "kind": kind,
        })
        compact = compact_surface(surface) if surface else None
        certified_graph = certified_nonempty_regular_graph(surface)
        active_rows.append({
            "surface_id": surface_id,
            "target_id": identifier,
            "surface_kind": (
                "DELTA_ZERO" if kind == "UNRESOLVED_DELTA"
                else "NEAR_ROOT_ZERO"
            ),
            "equation": (
                f"Delta_{identifier}=0" if kind == "UNRESOLVED_DELTA"
                else f"near_{identifier}=0"
            ),
            "surface_evidence_sha256": digest(surface) if surface else None,
            "surface_evidence": compact,
            "candidate_surface_expected_dimension": 1,
            "certified_carrier_dimension": 1 if certified_graph else None,
            "carrier_existence_status": (
                "CERTIFIED_NONEMPTY_REGULAR_GRAPH"
                if certified_graph else "UNRESOLVED_POTENTIAL_SURFACE_OUTER"
            ),
            "certified_nonempty_regular_graph": certified_graph,
            "interior_axis_crossing_brackets_t_p": (
                surface["axis_full_face_brackets_t_p_s"][:2]
                if surface else []
            ),
            "boundary_face_rows": (
                [
                    {
                        "face": face,
                        "intersection_status": (
                            "FACE_RESTRICTED_INTERSECTION_UNRESOLVED_OUTER"
                        ),
                        "credit": 0,
                    }
                    for _axis, faces in enumerate((
                        ("t_lower", "t_upper"),
                        ("p_lower", "p_upper"),
                    ))
                    for face in faces
                ] if surface else []
            ),
            "corner_rows": [
                {"corner": corner, "status": "RETAINED_OUTER", "credit": 0}
                for corner in ("t0p0", "t0p1", "t1p0", "t1p1")
            ],
            "ambient_or_whole_parent_credit": 0,
        })

    incidence_rows: list[dict[str, Any]] = []
    active_by_id = {row["target_id"]: row for row in active_rows}
    surface_by_id = {identifier: surface for identifier, _kind, surface in active}
    for left_id, right_id in itertools.combinations(active_by_id, 2):
        rank_status = "RANK_NOT_CERTIFIED"
        left_surface = surface_by_id[left_id]
        right_surface = surface_by_id[right_id]
        if left_surface is not None and right_surface is not None:
            left_full = round185.delta_ad(parent_key, box, left_id)
            right_full = round185.delta_ad(parent_key, box, right_id)
            determinant = (
                left_full.derivative[0] * right_full.derivative[1]
                - left_full.derivative[1] * right_full.derivative[0]
            )
            rank_status = (
                "STRICT_RANK2_IF_INTERSECTION"
                if round185.strict_sign(determinant) != 0
                else "RANK_NOT_CERTIFIED"
            )
            determinant_bounds: dict[str, Any] | None = round185.arb_bounds(
                determinant
            )
        else:
            determinant_bounds = None
        incidence_rows.append({
            "left_surface_id": active_by_id[left_id]["surface_id"],
            "right_surface_id": active_by_id[right_id]["surface_id"],
            "candidate_incidence_expected_dimension_in_s0_slice": 0,
            "certified_intersection_dimension": None,
            "rank_status": rank_status,
            "Jacobian_determinant": determinant_bounds,
            "intersection_existence": "UNRESOLVED_OUTER",
            "ambient_or_whole_parent_credit": 0,
        })
    return {
        "candidate_universe": list(round185.CANDIDATES),
        "candidate_universe_sha256": digest(list(round185.CANDIDATES)),
        "candidate_dispositions": candidate_rows,
        "raw_classification_census": dict(sorted(raw_census.items())),
        "strict_future_pair_order_rows": future_pairs,
        "active_surface_rows": active_rows,
        "pairwise_incidence_rows": incidence_rows,
    }


def source_candidate_census_row(
    source: dict[str, Any],
    c38_source: dict[str, Any],
    box: Any,
) -> dict[str, Any]:
    identity = "c40-c2-source:" + digest({
        "source": source["row_sha256"],
        "box": box_payload(box),
    })
    inventory = candidate_disposition_inventory(
        c38_source["representative_origin_key"], box, identity, False
    )
    semantic = {
        "schema": C2_SOURCE_SCHEMA,
        "source_candidate_census_id": identity,
        "pair_index": source["pair_index"],
        "c39_source_id": source_identifier(source),
        "c39_source_row_sha256": source["row_sha256"],
        "c38_source_row_sha256": c38_source["row_sha256"],
        "representative_box": box_payload(box),
        "candidate_universe": inventory["candidate_universe"],
        "candidate_universe_sha256": inventory["candidate_universe_sha256"],
        "candidate_dispositions": inventory["candidate_dispositions"],
        "raw_classification_census": inventory["raw_classification_census"],
        "strict_future_pair_order_rows": inventory[
            "strict_future_pair_order_rows"
        ],
        "raw_candidate_count": 55,
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    return semantic


def collision2_record(
    leaf_id: str,
    source: dict[str, Any],
    c38_source: dict[str, Any],
    box: Any,
    config: dict[str, Any],
) -> tuple[dict[str, Any], str, str]:
    parent_key = c38_source["representative_origin_key"]
    inventory = candidate_disposition_inventory(
        parent_key, box, leaf_id, True
    )
    try:
        status, detail, evidence, baseline = round185.resolve_dynamic_box(
            parent_key,
            box,
            config["pair_index"],
            config["pattern_index"],
        )
    except Exception as error:
        status = "EVALUATION_EXCEPTION"
        baseline = "ROUND185_FAIL_CLOSED"
        evidence = []
        detail = {
            "point_owner": None,
            "error_type": type(error).__name__,
            "error_message": str(error),
        }
    if status.startswith("LOCAL_EXACT_KEY"):
        classification, witness = expected_collision2(detail, config)
    else:
        classification = "UNRESOLVED_C40_COLLISION2_" + status
        witness = baseline
    count = len(inventory["active_surface_rows"])
    certified_count = sum(
        bool(row["certified_nonempty_regular_graph"])
        for row in inventory["active_surface_rows"]
    )
    semantic = {
        "schema": C2_SCHEMA,
        "c40_leaf_id": leaf_id,
        "pair_index": source["pair_index"],
        "c39_source_row_sha256": source["row_sha256"],
        "c38_source_row_sha256": c38_source["row_sha256"],
        "baseline_status": baseline,
        "enhanced_status": status,
        "route_classification": classification,
        "route_witness": witness,
        "detail_sha256": digest(detail),
        "point_owner": detail.get("point_owner") or detail.get(
            "absolute_collision2_owner"
        ),
        "candidate_universe": inventory["candidate_universe"],
        "candidate_universe_sha256": inventory["candidate_universe_sha256"],
        "candidate_dispositions": inventory["candidate_dispositions"],
        "raw_classification_census": inventory["raw_classification_census"],
        "strict_future_pair_order_rows": inventory[
            "strict_future_pair_order_rows"
        ],
        "active_surface_rows": inventory["active_surface_rows"],
        "pairwise_incidence_rows": inventory["pairwise_incidence_rows"],
        "raw_candidate_count": 55,
        "active_surface_count": count,
        "ambient_slice_dimension": 2,
        "candidate_surface_outer_count": count,
        "certified_nonempty_regular_graph_count": certified_count,
        "pairwise_potential_incidence_outer_count": len(
            inventory["pairwise_incidence_rows"]
        ),
        "certified_zero_dimensional_intersection_count": 0,
        "boundary_face_family": ["t_lower", "t_upper", "p_lower", "p_upper"],
        "corner_family_count": 4,
        "arrangement_status": (
            "FULL_55_CANDIDATE_OUTER_CATALOG__OPEN_CHAMBERS_NOT_MATERIALIZED"
        ),
        "open_chambers_materialized": False,
        "half_open_policy_required_before_promotion": (
            "each strict Delta sign vector owns one open chamber; every equality "
            "carrier and incidence is retained once in its own dimension"
        ),
        "ambient_or_whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }
    semantic["multi_delta_cell_id"] = "c40-multi-delta:" + digest(semantic)
    return semantic, classification, witness


def route_child(
    source: dict[str, Any],
    c38_source: dict[str, Any],
    cell: dict[str, Any],
    combined_path: str,
    config: dict[str, Any],
) -> tuple[dict[str, Any], Any]:
    pseudo = copy.deepcopy(c38_source)
    pseudo["path"] = combined_path
    task = {
        "task_id": source_identifier(source) + ":" + combined_path,
        "kind": "C1",
        "row": pseudo,
        "cell": cell,
    }
    result = c39.route_c1_task(task, config)
    box, _active = c39.reconstruct_box(cell, combined_path)
    return result, box


def needs_h1_graph(classification: str, result: dict[str, Any]) -> bool:
    if classification.startswith("EXCLUDED_"):
        return False
    evidence = result.get("surface_evidence") or {}
    h1 = evidence.get("H1")
    if h1 is not None:
        return h1.get("kind") not in {None, "STRICT_SIDE"}
    return bool(
        not classification.startswith("EXCLUDED_")
        and any(token in classification for token in (
            "H1_BOUNDARY", "H1_GRAPH", "H1_REGULAR_FULL_FACE"
        ))
    )


def collision2_safe(result: dict[str, Any], classification: str) -> bool:
    if classification.startswith("EXCLUDED_") or "COLLISION2" not in classification:
        return False
    evidence = result.get("surface_evidence") or {}
    h1 = evidence.get("H1")
    return bool(
        evidence.get("remaining_unresolved_record_count") == 0
        and h1
        and h1.get("kind") == "STRICT_SIDE"
        and h1.get("chart") == "W"
    )


def make_leaf(
    source: dict[str, Any],
    c38_source: dict[str, Any],
    box: Any | None,
    path: str,
    extra_depth: int,
    fraction: Q,
    classification: str,
    route_method: str,
    witness: str,
    h1_id: str | None,
    endpoint_id: str | None,
    c2_id: str | None,
    route_failure: dict[str, Any] | None = None,
) -> dict[str, Any]:
    identity = {
        "pair_index": source["pair_index"],
        "c39_source_row_sha256": source["row_sha256"],
        "path": path,
        "parent_volume_fraction": qstr(fraction),
    }
    leaf_id = "c40-leaf:" + digest(identity)
    terminal = classification.startswith("EXCLUDED_")
    chart = ":".join(c38_source["representative_origin_key"].split(":")[:2])
    semantic = {
        "schema": LEAF_SCHEMA,
        "c40_leaf_id": leaf_id,
        "pair_index": source["pair_index"],
        "c39_source_id": source_identifier(source),
        "c39_source_row_sha256": source["row_sha256"],
        "c38_source_row_sha256": c38_source["row_sha256"],
        "representative_cell_id": source["representative_cell_id"],
        "reflected_cell_id": source["reflected_cell_id"],
        "source_path": source["path"],
        "path": path,
        "extra_depth": extra_depth,
        "parent_volume_fraction": qstr(fraction),
        "representative_box": box_payload(box) if box is not None else None,
        "reflected_box": (
            reflected_payload(chart.split(":")[1], box) if box is not None else None
        ),
        "source_classification": source["classification"],
        "classification": classification,
        "route_method": route_method,
        "witness": witness,
        "h1_graph_cell_id": h1_id,
        "endpoint_chart_id": endpoint_id,
        "multi_delta_cell_id": c2_id,
        "route_failure": route_failure,
        "route_exception_phase": (
            route_failure["phase"] if route_failure is not None else None
        ),
        "route_exception_type": (
            route_failure["exception_type"] if route_failure is not None else None
        ),
        "route_exception_message": (
            route_failure["exception_message"]
            if route_failure is not None else None
        ),
        "reflection_transport_materialized": box is not None,
        "round144_terminal_class": (
            "EARLIEST_PREFIX_EXCLUDED"
            if terminal else "UNRESOLVED_R1648_CONTINUATION"
        ),
        "local_round144_terminal_credit": 1 if terminal else 0,
        "C34_common_refinement_credit": 0,
        "D02_gate_credit": 0,
    }
    require(semantic["c40_leaf_id"] == leaf_id, "leaf identity")
    return semantic


def process_source(
    source: dict[str, Any],
    c38_source: dict[str, Any],
    cell: dict[str, Any],
    seams: list[dict[str, Any]] | None,
    config: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    leaves: list[dict[str, Any]] = []
    h1_rows: list[dict[str, Any]] = []
    endpoint_rows: list[dict[str, Any]] = []
    c2_rows: list[dict[str, Any]] = []
    c2_source_rows: list[dict[str, Any]] = []
    source_fraction = Q(source["parent_volume_fraction"])

    if source["classification"].startswith("EXCLUDED_") or (
        "NEEDS_COLLISION3_1648" in source["classification"]
    ):
        box = c39.box_from_child(c38_source) if source["representative_box"] else None
        leaves.append(make_leaf(
            source,
            c38_source,
            box,
            source["path"],
            0,
            source_fraction,
            source["classification"],
            "C39_TERMINAL_OR_LIVE_CARRY",
            source["witness"],
            None,
            None,
            None,
        ))
        return {
            "leaves": leaves, "h1": h1_rows, "endpoint": endpoint_rows,
            "c2": c2_rows, "c2_source": c2_source_rows,
        }

    if source["representative_box"] is None:
        identity = {
            "pair_index": source["pair_index"],
            "c39_source_row_sha256": source["row_sha256"],
            "path": source["path"],
            "parent_volume_fraction": qstr(source_fraction),
        }
        leaf_id = "c40-leaf:" + digest(identity)
        endpoint = endpoint_row(
            leaf_id,
            source,
            c38_source,
            cell,
            None,
            "UNRESOLVED_C40_ALGEBRAIC_ENDPOINT_GRAPH_CELL",
            seams,
        )
        endpoint_rows.append(endpoint)
        leaves.append(make_leaf(
            source,
            c38_source,
            None,
            source["path"],
            0,
            source_fraction,
            "UNRESOLVED_C40_ALGEBRAIC_ENDPOINT_GRAPH_CELL",
            "EXACT_ALGEBRAIC_H0_ENDPOINT_CHART",
            source["witness"],
            None,
            endpoint["endpoint_chart_id"],
            None,
        ))
        return {
            "leaves": leaves, "h1": h1_rows, "endpoint": endpoint_rows,
            "c2": c2_rows, "c2_source": c2_source_rows,
        }

    root_box = c39.box_from_child(c38_source)
    if source["classification"] in C39_COLLISION2_TARGETS:
        c2_source_rows.append(source_candidate_census_row(
            source, c38_source, root_box
        ))

    pending: list[tuple[Any, str, int]] = []
    first_axis = c38.round166.longest_axis(root_box)
    for bit, child in reversed(list(enumerate(
        c38.round166.split_axis(root_box, first_axis)
    ))):
        pending.append((child, source["path"] + str(bit), 1))
    while pending:
        child, path, depth = pending.pop()
        try:
            result, reconstructed = route_child(
                source, c38_source, cell, path, config
            )
        except Exception as error:
            # C39's AD router can legitimately be undefined on a source-radical
            # endpoint box.  The dyadic cell still exists: retain it once as a
            # nonterminal, zero-credit outer instead of aborting or promoting it.
            reconstructed, _active = c39.reconstruct_box(cell, path)
            require(
                box_payload(child) == box_payload(reconstructed),
                "exception child reconstruction equality",
            )
            fraction = source_fraction / (2 ** depth)
            identity = {
                "pair_index": source["pair_index"],
                "c39_source_row_sha256": source["row_sha256"],
                "path": path,
                "parent_volume_fraction": qstr(fraction),
            }
            leaf_id = "c40-leaf:" + digest(identity)
            endpoint: dict[str, Any] | None = None
            h1: dict[str, Any] | None = None
            replay = source_radical_failure_replay(
                c38_source["representative_origin_key"], reconstructed, error
            )
            route_failure = {
                "phase": "C39_ROUTE_C1_TASK",
                "exception_type": type(error).__name__,
                "exception_module": type(error).__module__,
                "exception_message": str(error),
                "exact_box_endpoint_phase": endpoint_phase(reconstructed),
                "source_radical_initial_geometry_replay": replay,
            }
            if replay["source_radical_causal_match"]:
                classification = (
                    "UNRESOLVED_C40_SOURCE_RADICAL_ENDPOINT_ROUTE_"
                    "EVALUATION_FAILURE_OUTER"
                )
            else:
                classification = (
                    "UNRESOLVED_C40_P_ENDPOINT_BOX_ROUTE_EVALUATION_"
                    "FAILURE_OUTER"
                    if endpoint_phase(reconstructed) is not None
                    else "UNRESOLVED_C40_C1_ROUTE_EVALUATION_EXCEPTION_OUTER"
                )
                # A router exception alone says nothing about H1.  Retain an H1
                # row only when a separate full-box proof certifies a nonempty
                # regular graph; all weaker/evaluation-failure evidence is omitted.
                try:
                    independent_h1 = h1_graph_row(
                        leaf_id, source, c38_source, reconstructed
                    )
                except Exception:
                    independent_h1 = None
                if (
                    independent_h1 is not None
                    and independent_h1["certified_nonempty_regular_graph"]
                ):
                    h1 = independent_h1
                    h1_rows.append(h1)
            if endpoint_phase(reconstructed) is not None:
                # The exact endpoint carrier exists independently of why the
                # router failed, so always retain its chart once.  Its route
                # classification must exactly match the owning leaf.
                endpoint = endpoint_row(
                    leaf_id,
                    source,
                    c38_source,
                    cell,
                    reconstructed,
                    classification,
                )
                require(
                    endpoint["failure_phase"]
                    == "SOURCE_RADICAL_1_MINUS_P2_ENDPOINT"
                    and endpoint["certified_carrier_dimension"] == 1
                    and endpoint["classification"] == classification,
                    "exact source-radical endpoint exception chart",
                )
                endpoint_rows.append(endpoint)
            leaves.append(make_leaf(
                source,
                c38_source,
                reconstructed,
                path,
                depth,
                fraction,
                classification,
                "C39_ROUTE_EXCEPTION_FAIL_CLOSED",
                type(error).__name__ + ":" + str(error),
                h1["h1_graph_cell_id"] if h1 else None,
                endpoint["endpoint_chart_id"] if endpoint else None,
                None,
                route_failure,
            ))
            continue
        require(
            box_payload(child) == box_payload(reconstructed),
            "child reconstruction equality",
        )
        classification = result["classification"]
        witness = result["witness"]
        route_method = result["route_method"]
        terminal_or_live = (
            classification.startswith("EXCLUDED_")
            or "NEEDS_COLLISION3_1648" in classification
        )
        if not terminal_or_live and depth < EXTRA_DEPTH:
            axis = c38.round166.longest_axis(reconstructed)
            grandchildren = c38.round166.split_axis(reconstructed, axis)
            for bit, grandchild in reversed(list(enumerate(grandchildren))):
                pending.append((grandchild, path + str(bit), depth + 1))
            continue
        fraction = source_fraction / (2 ** depth)
        identity = {
            "pair_index": source["pair_index"],
            "c39_source_row_sha256": source["row_sha256"],
            "path": path,
            "parent_volume_fraction": qstr(fraction),
        }
        leaf_id = "c40-leaf:" + digest(identity)
        endpoint: dict[str, Any] | None = None
        h1: dict[str, Any] | None = None
        c2: dict[str, Any] | None = None
        endpoint_kind = endpoint_phase(reconstructed)
        if not classification.startswith("EXCLUDED_") and (
            endpoint_kind is not None
            or classification.endswith("SOURCE_GRAZING_ENDPOINT_CHART")
        ):
            endpoint = endpoint_row(
                leaf_id, source, c38_source, cell, reconstructed, classification
            )
            endpoint_rows.append(endpoint)
        if needs_h1_graph(classification, result):
            h1 = h1_graph_row(leaf_id, source, c38_source, reconstructed)
            h1_rows.append(h1)
            if (
                h1["failure_phase"]
                == "COLLISION1_DELTA1_H1_EVALUATION_FAILURE_OUTER"
                and endpoint is None
            ):
                endpoint = endpoint_row(
                    leaf_id, source, c38_source, cell, reconstructed, classification
                )
                endpoint_rows.append(endpoint)
        if collision2_safe(result, classification):
            try:
                c2, enhanced_classification, enhanced_witness = collision2_record(
                    leaf_id, source, c38_source, reconstructed, config
                )
                c2_rows.append(c2)
                classification = enhanced_classification
                witness = enhanced_witness
                route_method = "ROUND185_ENHANCED_COLLISION2_ARRANGEMENT"
            except Exception as error:
                classification = "UNRESOLVED_C40_COLLISION2_EVALUATION_EXCEPTION"
                witness = type(error).__name__ + ":" + str(error)
                route_method = "ROUND185_FAIL_CLOSED"
        leaves.append(make_leaf(
            source,
            c38_source,
            reconstructed,
            path,
            depth,
            fraction,
            classification,
            route_method,
            witness,
            h1["h1_graph_cell_id"] if h1 else None,
            endpoint["endpoint_chart_id"] if endpoint else None,
            c2["multi_delta_cell_id"] if c2 else None,
        ))
    require(sum(Q(row["parent_volume_fraction"]) for row in leaves) == source_fraction,
            "source Kraft conservation")
    return {
        "leaves": leaves, "h1": h1_rows, "endpoint": endpoint_rows,
        "c2": c2_rows, "c2_source": c2_source_rows,
    }


def worker(input_path: Path, output_path: Path) -> None:
    source_pins()
    ctx.prec = PRECISION_BITS
    payload = strict_json(input_path)
    config = payload["config"]
    config["pair_index"] = decoded_tuple_map(config["pair_index"])
    config["pattern_index"] = decoded_tuple_map(config["pattern_index"])
    official_pair_index, official_pattern_index, official_registry_sha = (
        c38.round139.lower.component_cert.key_index_tables()
    )
    require(
        config["pair_index"] == official_pair_index
        and config["pattern_index"] == official_pattern_index
        and config["official_registry_sha256"] == official_registry_sha
        and config["pattern_index"].get(()) == 0,
        "worker decoded official registry exact equality",
    )
    config["cores"] = tuple(c38.round139.lower.core_cert.physical_cores())
    c38.round166.install_fast_readonly_replay()
    rows = []
    for task in payload["tasks"]:
        rows.append({
            "source_ordinal": task["source_ordinal"],
            **process_source(
                task["source"], task["c38_source"], task["cell"],
                task.get("seams"), config
            ),
        })
    write_json(output_path, {"schema": SCHEMA + ".worker", "rows": rows})


def run_workers(
    stage: Path,
    tasks: list[dict[str, Any]],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    worker_dir = stage / ".worker"
    worker_dir.mkdir()
    shard_count = min(8, max(1, len(tasks)))
    shards = [tasks[index::shard_count] for index in range(shard_count)]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(DELIVERABLES) + (
        os.pathsep + environment["PYTHONPATH"]
        if environment.get("PYTHONPATH") else ""
    )
    processes: list[tuple[Any, Path, Any, Any]] = []
    for index, shard in enumerate(shards):
        input_path = worker_dir / f"input-{index}.json"
        output_path = worker_dir / f"output-{index}.json"
        stdout_path = worker_dir / f"stdout-{index}.log"
        stderr_path = worker_dir / f"stderr-{index}.log"
        write_json(input_path, {
            "schema": SCHEMA + ".worker-input",
            "config": config,
            "tasks": shard,
        })
        stdout = stdout_path.open("wb")
        stderr = stderr_path.open("wb")
        process = __import__("subprocess").Popen(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--worker-input", str(input_path),
                "--worker-output", str(output_path),
            ],
            cwd=ROOT,
            env=environment,
            stdout=stdout,
            stderr=stderr,
        )
        processes.append((process, output_path, stdout, stderr))
    results: dict[int, dict[str, Any]] = {}
    for index, (process, output_path, stdout, stderr) in enumerate(processes):
        code = process.wait()
        stdout.close()
        stderr.close()
        require(
            code == 0,
            "worker failure:" + str(index) + ":" + (
                worker_dir / f"stderr-{index}.log"
            ).read_text(encoding="utf-8", errors="replace")[-4000:],
        )
        output = strict_json(output_path)
        for row in output["rows"]:
            ordinal = row["source_ordinal"]
            require(ordinal not in results, "duplicate worker ordinal")
            results[ordinal] = row
    require(len(results) == len(tasks), "worker result census")
    ordered = [results[index] for index in range(len(tasks))]
    shutil.rmtree(worker_dir)
    return ordered


def build(output: Path, candidate: Path, audit_path: Path) -> dict[str, Any]:
    require(not output.exists(), f"output exists:{output}")
    pins = source_pins()
    validate_manifest(candidate)
    c39_result = strict_json(candidate / "result.json")
    validate_object(c39_result, "object_sha256", EXPECTED_C39_OBJECT, "C39")
    audit = strict_json(audit_path)
    validate_object(audit, "object_sha256", EXPECTED_C39_AUDIT_OBJECT, "C39 audit")
    require(
        audit["candidate_object_sha256"] == EXPECTED_C39_OBJECT
        and audit["status"]
        == "PASS_INDEPENDENT_C39_FORMAL_CREDIT_RECONSTRUCTION__320_NEW_TERMINAL_ROUTES__18_OF_18_ATTACKS_FAIL_CLOSED",
        "C39 audit binding",
    )
    c39_leaves = c38.read_ledger(candidate, c39_result["ledgers"]["routed_child_pairs"])
    c39_parents = c38.read_ledger(candidate, c39_result["ledgers"]["parent_conservation"])
    require(len(c39_leaves) == 10486 and len(c39_parents) == 862, "C39 census")

    c38_dir = (ROOT / c39_result["C38_authority"]["path"]).resolve()
    validate_manifest(c38_dir)
    c38_result = strict_json(c38_dir / "result.json")
    validate_object(c38_result, "object_sha256", EXPECTED_C38_OBJECT, "C38")
    c38_leaves = c38.read_ledger(
        c38_dir, c38_result["ledgers"]["collision1_2_child_pairs"]
    )
    c38_index = {row["row_sha256"]: row for row in c38_leaves}
    require(len(c38_index) == len(c38_leaves), "C38 row uniqueness")

    c37 = (ROOT / c38_result["C37_authority"]["path"]).resolve()
    c37_result = strict_json(c37 / "result.json")
    c36 = (ROOT / c37_result["C36_authority"]["path"]).resolve()
    c36_result = strict_json(c36 / "result.json")
    c35 = (ROOT / c36_result["C35_authority"]["path"]).resolve()
    c34 = (ROOT / c36_result["C34_authority"]["path"]).resolve()
    c35_result = strict_json(c35 / "result.json")
    c34_result = strict_json(c34 / "result.json")
    c32 = (ROOT / c34_result["C32_authority"]["path"]).resolve()
    c32_result = strict_json(c32 / "result.json")
    required_cell_ids = {row["representative_cell_id"] for row in c39_leaves}
    cells = {
        row["cell_id"]: row
        for row in c38.read_ledger(c32, c32_result["ledgers"]["cells"])
        if row["cell_id"] in required_cell_ids
    }
    require(set(cells) == required_cell_ids, "C32 cell inventory")
    seam_rows = c38.read_ledger(
        c32, c32_result["ledgers"]["source_chart_seams"]
    )
    seams_by_cell: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for seam in seam_rows:
        seams_by_cell[seam["left_cell_id"]].append(seam)
        seams_by_cell[seam["right_cell_id"]].append(seam)
    original_path = c38.read_ledger(
        c35, c35_result["ledgers"]["path_occurrences"]
    )[:2]
    reflected_path = c38.read_ledger(
        c37, c37_result["ledgers"]["reflected_r1648_occurrences"]
    )[:2]
    pair_index, pattern_index, registry_sha = (
        c38.round139.lower.component_cert.key_index_tables()
    )
    worker_config = {
        "original_path": original_path,
        "reflected_path": reflected_path,
        "pair_index": encoded_tuple_map(pair_index),
        "pattern_index": encoded_tuple_map(pattern_index),
        "official_registry_sha256": registry_sha,
    }
    tasks = []
    for ordinal, source in enumerate(c39_leaves):
        c38_source = c38_index.get(source["c38_child_row_sha256"])
        require(c38_source is not None, "C39 to C38 row binding")
        cell = cells[source["representative_cell_id"]]
        algebraic_seams: list[dict[str, Any]] | None = None
        if source["representative_box"] is None:
            algebraic_seams = sorted(
                seams_by_cell[cell["cell_id"]],
                key=lambda row: Q(row["physical_p_span"][0]["value"]),
            )
            require(bool(algebraic_seams), "algebraic seam incidence nonempty")
            spans = [
                tuple(Q(value["value"]) for value in row["physical_p_span"])
                for row in algebraic_seams
            ]
            require(
                spans[0][0] == Q(cell["physical_p_interval"][0])
                and spans[-1][1] == Q(cell["physical_p_interval"][1])
                and all(left[1] == right[0]
                        for left, right in zip(spans, spans[1:])),
                "algebraic seam exact p-span exhaustion",
            )
        tasks.append({
            "source_ordinal": ordinal,
            "source": source,
            "c38_source": c38_source,
            "cell": cell,
            "seams": algebraic_seams,
        })

    output.parent.mkdir(parents=True, exist_ok=True)
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require(not stage.exists(), f"stage exists:{stage}")
    stage.mkdir()
    try:
        routed_writer = LedgerWriter(
            stage / "routed_leaf_cells.jsonl.gz", "C39_ROW_ORDER_THEN_PATH"
        )
        h1_writer = LedgerWriter(
            stage / "h1_graph_cells.jsonl.gz", "C39_ROW_ORDER_THEN_PATH"
        )
        endpoint_writer = LedgerWriter(
            stage / "endpoint_charts.jsonl.gz", "C39_ROW_ORDER_THEN_PATH"
        )
        c2_writer = LedgerWriter(
            stage / "collision2_multi_delta_cells.jsonl.gz",
            "C39_ROW_ORDER_THEN_PATH",
        )
        c2_source_writer = LedgerWriter(
            stage / "collision2_source_candidate_census.jsonl.gz",
            "C39_ROW_ORDER",
        )
        parent_writer = LedgerWriter(
            stage / "parent_conservation.jsonl.gz", "PAIR_INDEX_ASCENDING"
        )
        processed = run_workers(stage, tasks, worker_config)
        rows_by_pair: dict[int, list[dict[str, Any]]] = defaultdict(list)
        classifications: Counter[str] = Counter()
        route_exception_outer_census: Counter[str] = Counter()
        route_exception_evidence_census: Counter[
            tuple[str, str, str]
        ] = Counter()
        source_raw_census: Counter[str] = Counter()
        source_strict_future_pair_count = 0
        h1_certified_graph_count = 0
        endpoint_phase_census: Counter[str] = Counter()
        algebraic_seam_segment_census: Counter[int] = Counter()
        algebraic_seam_incidence_count = 0
        c2_candidate_surface_outer_count = 0
        c2_certified_graph_count = 0
        c2_potential_incidence_outer_count = 0
        with routed_writer, h1_writer, endpoint_writer, c2_writer, c2_source_writer:
            for row in processed:
                for leaf in row["leaves"]:
                    routed_writer.write(leaf)
                    rows_by_pair[leaf["pair_index"]].append(leaf)
                    classifications[leaf["classification"]] += 1
                    if leaf["route_method"] == "C39_ROUTE_EXCEPTION_FAIL_CLOSED":
                        failure = leaf["route_failure"]
                        require(
                            not leaf["classification"].startswith("EXCLUDED_")
                            and leaf["local_round144_terminal_credit"] == 0
                            and leaf["D02_gate_credit"] == 0
                            and leaf["multi_delta_cell_id"] is None,
                            "route exception retained as zero-credit outer",
                        )
                        require(
                            type(failure) is dict
                            and failure["phase"] == "C39_ROUTE_C1_TASK"
                            and type(failure["exception_type"]) is str
                            and type(failure["exception_message"]) is str,
                            "structured route exception evidence",
                        )
                        require(
                            leaf["route_exception_phase"] == failure["phase"]
                            and leaf["route_exception_type"]
                            == failure["exception_type"]
                            and leaf["route_exception_message"]
                            == failure["exception_message"],
                            "flat structured route exception fields",
                        )
                        if "SOURCE_RADICAL_ENDPOINT" in leaf["classification"]:
                            require(
                                leaf["endpoint_chart_id"] is not None,
                                "source-radical exception endpoint chart binding",
                            )
                            require(
                                failure[
                                    "source_radical_initial_geometry_replay"
                                ]["source_radical_causal_match"],
                                "source-radical causal exception replay binding",
                            )
                        elif "P_ENDPOINT_BOX" in leaf["classification"]:
                            require(
                                leaf["endpoint_chart_id"] is not None
                                and not failure[
                                    "source_radical_initial_geometry_replay"
                                ]["source_radical_causal_match"],
                                "p-endpoint generic exception separation",
                            )
                        route_exception_outer_census[leaf["classification"]] += 1
                        route_exception_evidence_census.update([(
                            leaf["classification"],
                            leaf["route_exception_type"],
                            leaf["route_exception_message"],
                        )])
                    else:
                        require(
                            leaf["route_failure"] is None
                            and leaf["route_exception_phase"] is None
                            and leaf["route_exception_type"] is None
                            and leaf["route_exception_message"] is None,
                            "nonexception leaf has null route exception fields",
                        )
                for h1 in row["h1"]:
                    h1_writer.write(h1)
                    h1_certified_graph_count += int(
                        h1["certified_nonempty_regular_graph"]
                    )
                for endpoint in row["endpoint"]:
                    endpoint_writer.write(endpoint)
                    endpoint_phase_census[endpoint["failure_phase"]] += 1
                    if endpoint["failure_phase"] == (
                        "ALGEBRAIC_SOURCE_CHART_H0_ENDPOINT"
                    ):
                        segment_count = endpoint["endpoint"][
                            "adjacent_chart_seam_incidence_count"
                        ]
                        algebraic_seam_segment_census[segment_count] += 1
                        algebraic_seam_incidence_count += segment_count
                for c2 in row["c2"]:
                    c2_writer.write(c2)
                    c2_candidate_surface_outer_count += c2[
                        "candidate_surface_outer_count"
                    ]
                    c2_certified_graph_count += c2[
                        "certified_nonempty_regular_graph_count"
                    ]
                    c2_potential_incidence_outer_count += c2[
                        "pairwise_potential_incidence_outer_count"
                    ]
                for c2_source in row["c2_source"]:
                    c2_source_writer.write(c2_source)
                    source_raw_census.update(
                        c2_source["raw_classification_census"]
                    )
                    source_strict_future_pair_count += len(
                        c2_source["strict_future_pair_order_rows"]
                    )
        require(c2_source_writer.count == 6232, "C39 source C2 row census")
        require(
            dict(sorted(source_raw_census.items()))
            == EXPECTED_C39_COLLISION2_RAW_CENSUS,
            "C39 source 6232x55 raw candidate census",
        )
        require(source_strict_future_pair_count == 5708,
                "C39 source strict-future pair census")
        require(
            sum(route_exception_outer_census.values()) == 219
            and route_exception_evidence_census
            == Counter(EXPECTED_ROUTE_EXCEPTION_EVIDENCE_CENSUS),
            "exact fail-closed C1 route exception evidence census",
        )
        require(
            endpoint_phase_census["ALGEBRAIC_SOURCE_CHART_H0_ENDPOINT"] == 29
            and dict(sorted(algebraic_seam_segment_census.items()))
            == {1: 26, 2: 2, 3: 1}
            and algebraic_seam_incidence_count == 33,
            "algebraic chart-seam complete incidence census",
        )
        require(
            h1_certified_graph_count <= h1_writer.count
            and c2_certified_graph_count <= c2_candidate_surface_outer_count,
            "certified graph counts bounded by candidate outers",
        )

        c39_parent_index = {row["pair_index"]: row for row in c39_parents}
        full_count = partial_count = zero_count = newly_full = 0
        terminal_equivalent = Q(0)
        unresolved_equivalent = Q(0)
        with parent_writer:
            for pair_number in range(862):
                rows = rows_by_pair[pair_number]
                require(bool(rows), f"pair rows:{pair_number}")
                paths = [row["path"] for row in rows]
                require(len(paths) == len(set(paths)), "unique paths")
                require(not any(
                    left != right and right.startswith(left)
                    for left, right in itertools.product(paths, repeat=2)
                ), "prefix-free paths")
                total = sum(Q(row["parent_volume_fraction"]) for row in rows)
                require(total == 1, f"parent Kraft:{pair_number}:{total}")
                terminal = sum(
                    Q(row["parent_volume_fraction"])
                    for row in rows if row["classification"].startswith("EXCLUDED_")
                )
                unresolved = 1 - terminal
                prior = c39_parent_index[pair_number]
                prior_terminal = Q(prior["terminal_excluded_parent_volume"])
                require(terminal >= prior_terminal, "monotone terminal volume")
                whole = terminal == 1
                if whole:
                    full_count += 1
                elif terminal == 0:
                    zero_count += 1
                else:
                    partial_count += 1
                if whole and not prior["whole_representative_parent_terminal"]:
                    newly_full += 1
                terminal_equivalent += terminal
                unresolved_equivalent += unresolved
                parent_writer.write({
                    "schema": PARENT_SCHEMA,
                    "pair_index": pair_number,
                    "c39_parent_row_sha256": prior["row_sha256"],
                    "leaf_count": len(rows),
                    "path_prefix_free": True,
                    "terminal_excluded_parent_volume": qstr(terminal),
                    "unresolved_parent_volume": qstr(unresolved),
                    "parent_Kraft_conservation": "1",
                    "whole_representative_parent_terminal": whole,
                    "whole_reflected_parent_terminal": whole,
                    "newly_whole_terminal_vs_C39": (
                        whole and not prior["whole_representative_parent_terminal"]
                    ),
                    "C34_common_refinement_credit": 2 if whole else 0,
                    "D02_gate_credit": 0,
                })
        require(
            full_count + partial_count + zero_count == 862
            and terminal_equivalent + unresolved_equivalent == 862,
            "global conservation",
        )
        require(full_count >= 161 and newly_full == full_count - 161,
                "monotone whole credit")
        formal_excluded = 74812 + 2 * full_count
        formal_unresolved = 1724 - 2 * full_count
        (stage / "PARTIAL_ARRANGEMENT_ONLY.lock").write_text(
            "C40 materializes two-level rational off-graph slabs, H1 graph cells, "
            "source/algebraic endpoint charts, and collision-two multi-Delta "
            "incidence outers. Only exact excluded leaf volume participates in "
            "parent Kraft conservation. No graph, boundary, endpoint, incidence, "
            "local exact key, or surviving collision-two branch earns ambient, "
            "D02, D03, D04, Gate5, or CM2 credit. Collisions 3--1648 remain.\n",
            encoding="utf-8",
        )
        result: dict[str, Any] = {
            "schema": SCHEMA,
            "status": (
                f"PASS_C40_DIMENSION_SAFE_ARRANGEMENT_OUTER_FRONTIER__"
                f"{routed_writer.count}_LEAVES__"
                f"{2 * full_count}_WHOLE_CELLS_TERMINAL__"
                f"{formal_unresolved}_FORMAL_UNRESOLVED"
            ),
            "C39_authority": {
                "path": str(candidate.resolve().relative_to(ROOT)),
                "object_sha256": c39_result["object_sha256"],
                "independent_audit_path": str(audit_path.resolve().relative_to(ROOT)),
                "independent_audit_object_sha256": audit["object_sha256"],
            },
            "numeric_authority": {
                "source_sha256": pins,
                "flint_version": flint.__version__,
                "precision_bits": PRECISION_BITS,
                "extra_dyadic_depth": EXTRA_DEPTH,
                "official_registry_sha256": registry_sha,
                "candidate_boundary_separation_registry": (
                    round185.r181.boundary_separation_registry()
                ),
                "candidate_boundary_separation_registry_object_sha256": (
                    EXPECTED_BOUNDARY_SEPARATION_OBJECT
                ),
                "source_slice": "s=0",
            },
            "arrangement_census": {
                "C39_source_leaf_count": len(c39_leaves),
                "C39_nonwhole_representative_parent_count": 701,
                "routed_leaf_count": routed_writer.count,
                "classification_census": dict(sorted(classifications.items())),
                "route_evaluation_failure_outer_count": sum(
                    route_exception_outer_census.values()
                ),
                "route_evaluation_failure_outer_census": dict(
                    sorted(route_exception_outer_census.items())
                ),
                "route_evaluation_failure_evidence_census": {
                    "\u001f".join(key): value
                    for key, value in sorted(
                        route_exception_evidence_census.items()
                    )
                },
                "h1_candidate_surface_outer_count": h1_writer.count,
                "h1_certified_nonempty_regular_graph_count": (
                    h1_certified_graph_count
                ),
                "endpoint_chart_count": endpoint_writer.count,
                "endpoint_failure_phase_census": dict(
                    sorted(endpoint_phase_census.items())
                ),
                "algebraic_endpoint_chart_count": 29,
                "algebraic_chart_seam_incidence_count": (
                    algebraic_seam_incidence_count
                ),
                "algebraic_chart_seam_segment_count_census": {
                    str(key): value
                    for key, value in sorted(algebraic_seam_segment_census.items())
                },
                "collision2_multi_delta_cell_count": c2_writer.count,
                "collision2_candidate_surface_outer_count": (
                    c2_candidate_surface_outer_count
                ),
                "collision2_certified_nonempty_regular_graph_count": (
                    c2_certified_graph_count
                ),
                "collision2_pairwise_potential_incidence_outer_count": (
                    c2_potential_incidence_outer_count
                ),
                "collision2_certified_zero_dimensional_intersection_count": 0,
                "collision2_source_candidate_census_row_count": (
                    c2_source_writer.count
                ),
                "collision2_source_raw_candidate_count": (
                    55 * c2_source_writer.count
                ),
                "collision2_source_raw_classification_census": dict(
                    sorted(source_raw_census.items())
                ),
                "collision2_source_strict_future_pair_row_count": (
                    source_strict_future_pair_count
                ),
                "whole_terminal_representative_parent_count": full_count,
                "whole_terminal_paired_coarse_cell_count": 2 * full_count,
                "newly_whole_terminal_representative_parent_count": newly_full,
                "newly_whole_terminal_paired_coarse_cell_count": 2 * newly_full,
                "partial_representative_parent_count": partial_count,
                "zero_progress_representative_parent_count": zero_count,
                "representative_terminal_parent_equivalent": qstr(terminal_equivalent),
                "representative_unresolved_parent_equivalent": qstr(unresolved_equivalent),
            },
            "ledgers": {
                "routed_leaf_cells": routed_writer.descriptor(),
                "h1_graph_cells": h1_writer.descriptor(),
                "endpoint_charts": endpoint_writer.descriptor(),
                "collision2_multi_delta_cells": c2_writer.descriptor(),
                "collision2_source_candidate_census": (
                    c2_source_writer.descriptor()
                ),
                "parent_conservation": parent_writer.descriptor(),
            },
            "round144_terminal_census": {
                "CONNECTED_TO_KNOWN": 0,
                "EARLIEST_PREFIX_EXCLUDED": formal_excluded,
                "SOURCE_GRAZING_OR_CEMETERY": 0,
                "TYPED_EVENT_GRAPH": 296,
                "UNRESOLVED_R1648_CONTINUATION": formal_unresolved,
                "terminal_total": 76832,
                "unresolved_zero": False,
            },
            "strict_nonpromotion": {
                "lower_dimensional_graph_credit": 0,
                "endpoint_or_incidence_ambient_credit": 0,
                "four_class_terminal_census_unresolved_zero": False,
                "D02": f"BLOCKED_BY_{formal_unresolved}_COMPLETE_R1648_CONTINUATIONS",
                "D03": "UNAUTHORIZED",
                "D04": "NOT_MINTED",
                "Gate5": "10/18",
                "complete_global_18_field_blocks": 0,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "execution_receipt_policy": (
                "out-of-band self-hashed receipt binds InvocationID/PID to this "
                "deterministic object and root manifest without polluting replay bytes"
            ),
            "required_next": (
                "resolve the remaining C1/H1/endpoint/multi-Delta carriers, then "
                "continue every surviving exact collision-two branch through "
                "collisions 3--1648 before any D02 promotion"
            ),
        }
        result["object_sha256"] = digest(result)
        write_json(stage / "result.json", result)
        write_manifest(stage)
        require(
            sorted(path.name for path in stage.iterdir()) == sorted([
                "PARTIAL_ARRANGEMENT_ONLY.lock",
                "collision2_multi_delta_cells.jsonl.gz",
                "collision2_source_candidate_census.jsonl.gz",
                "endpoint_charts.jsonl.gz",
                "h1_graph_cells.jsonl.gz",
                "parent_conservation.jsonl.gz",
                "result.json",
                "root_manifest.sha256",
                "routed_leaf_cells.jsonl.gz",
            ]),
            "exact nine-file candidate inventory",
        )
        stage.rename(output)
        return result
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def process_start_ticks(pid: int) -> int:
    fields = (Path("/proc") / str(pid) / "stat").read_text(
        encoding="ascii"
    ).split()
    value = int(fields[21])
    require(value > 0, "process start ticks")
    return value


def write_receipt(
    path: Path,
    invocation_id: str,
    pid: int,
    start_ticks: int,
    output: Path,
    result: dict[str, Any],
) -> dict[str, Any]:
    require(INVOCATION.fullmatch(invocation_id) is not None, "InvocationID syntax")
    require(not path.exists(), f"receipt exists:{path}")
    require(pid == os.getpid() and process_start_ticks(pid) == start_ticks,
            "live PID/start binding")
    semantic = {
        "schema": RECEIPT_SCHEMA,
        "status": "PASS_LIVE_PID_INVOCATION_BOUND_TO_C40_OBJECT",
        "InvocationID": invocation_id,
        "producer_pid": pid,
        "producer_parent_pid": os.getppid(),
        "producer_proc_start_ticks": start_ticks,
        "producer_executable": str(Path(sys.executable).resolve()),
        "producer_source_sha256": file_sha256(Path(__file__).resolve()),
        "candidate_path": str(output.resolve().relative_to(ROOT)),
        "candidate_object_sha256": result["object_sha256"],
        "root_manifest_sha256": file_sha256(output / "root_manifest.sha256"),
        "candidate_inventory_count": 9,
    }
    semantic["receipt_object_sha256"] = digest(semantic)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(descriptor, canonical(semantic) + b"\n")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return semantic


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--invocation-id")
    parser.add_argument("--worker-input", type=Path)
    parser.add_argument("--worker-output", type=Path)
    arguments = parser.parse_args()
    if arguments.worker_input is not None:
        require(arguments.worker_output is not None, "worker output")
        worker(arguments.worker_input.resolve(), arguments.worker_output.resolve())
        return 0
    require(arguments.output is not None, "output")
    require(arguments.receipt is not None, "receipt")
    require(arguments.invocation_id is not None, "InvocationID")
    pid = os.getpid()
    start_ticks = process_start_ticks(pid)
    candidate = arguments.candidate or (
        RUNTIME / "candidates" /
        (RUNTIME / "c39-current-token").read_text(encoding="utf-8").strip()
    )
    audit_path = arguments.audit or (
        RUNTIME / "audit" /
        (RUNTIME / "c39-current-audit-token").read_text(encoding="utf-8").strip() /
        "independent_audit.json"
    )
    result = build(arguments.output.resolve(), candidate.resolve(), audit_path.resolve())
    receipt = write_receipt(
        arguments.receipt.resolve(),
        arguments.invocation_id,
        pid,
        start_ticks,
        arguments.output.resolve(),
        result,
    )
    print(canonical({"result": result, "execution_receipt": receipt}).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
