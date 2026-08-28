#!/usr/bin/env python3
"""Formal local absence refinement of the Round185 H2 factor residual.

The frozen Round185 certificate contains 592
``H2_FACTOR_EXISTENCE_RESIDUAL`` boxes.  In every such box exactly one signed
factor of

    H2 = HPLUS * HMINUS

is strictly absent, while the other factor has strict full-box ``dt`` and
``dp`` derivatives.  This producer does not infer absence from regularity.
It reconstructs a complete centered-C0 atlas on both t-endpoint faces,
using exact rational p-bisection to depth at most two, and requires both
complete faces to have the same strict sign.  Strict full-box monotonicity in
t then excludes an active-factor zero throughout the box.

All 592 results are materialized as local exact-key rows.  Complete interval
evidence for all 1,568 terminal face cells is embedded in the certificate.
No whole-parent, stratum, or global exact-key disposition is issued.

Round199 is not imported and is not a mathematical dependency.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any

import flint


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round202_h2_factor_t_face_c0_absence_certificate.json"
SCHEMA = "cm2.round202.h2-factor-t-face-c0-absence.v1"
MAX_INPUT_BYTES = 160 * 1024 * 1024

R185_PREFIX = "cm2_round185_preconditioned_c1_residual_refinement"
R185_PRODUCER = f"{R185_PREFIX}.py"
R185_CERTIFICATE = f"{R185_PREFIX}_certificate.json"
R185_VERIFIER = f"{R185_PREFIX}_verifier.py"
R185_VERIFICATION = f"{R185_PREFIX}_verification.json"
R185_REPORT = f"{R185_PREFIX}_report.md"
R185_COLD_REPLAY = f"{R185_PREFIX}_cold_replay.md"
R185_MANIFEST = f"{R185_PREFIX}_manifest.sha256"
R185_PINS = {
    R185_PRODUCER:
        "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    R185_CERTIFICATE:
        "2034e939a6046cd36f749546ab8dc2c0a004b3325c803b5335a3f5e34831fff1",
    R185_VERIFIER:
        "88d5b72c68ba216a1c807b868156c8e0da7e9e63db968eda5b5a66dd86d5651f",
    R185_VERIFICATION:
        "bda1286ec582f17724b6478e3af98973280f482bf9192235f96842c55513642e",
    R185_REPORT:
        "77e29b55ff4be771fce34e3032b92ed52e94ab0833e20a069f491ad227ae7619",
    R185_COLD_REPLAY:
        "c14d3908a42746c7ff8a60f5f07319e0bd86b2f94d27154a3126b8f895447a7d",
}
R185_MANIFEST_SHA256 = (
    "ec018e261e866b48039d1cf775e972c6a9b1a9558a1ecf043665c6340ad3dc26"
)
R185_CERTIFICATE_SCHEMA = (
    "cm2.round185.preconditioned-c1-residual-refinement.v1"
)
R185_VERIFICATION_SCHEMA = (
    "cm2.round185.preconditioned-c1-residual-refinement-verification.v1"
)
R185_RESULT_SHA256 = (
    "ae5af298b9d19b99863af600dca7f73fad4ff76f9db661ccfdf9b0e03afbeddf"
)
R185_VERIFICATION_RESULT_SHA256 = (
    "b63c15eabc468192c113d7221c7adfd37fec94aa38f4b02c97acb25598962cf6"
)
R185_DYNAMIC_EXACT_ROWS_SHA256 = (
    "14e3ac9a008978668a8f6088cf7124f776e4f44186ed34d9f6d197727e76933e"
)
R185_DYNAMIC_RESIDUAL_ROWS_SHA256 = (
    "707577c77ef26050b331c3be4e657431dcfade82a4caec51d3a65a26e37d0f73"
)
R185_H2_ARRANGEMENT_ROWS_SHA256 = (
    "be0ac77b64583af7b8e61d648a67a514de0c003e2111783c30412b1785b67422"
)
R185_INHERITED_RESIDUAL_ROWS_SHA256 = (
    "1a08ae404c36d211206d5b1616c3266cdf629ee6b294d5a1f444330061ef3df2"
)

EXPECTED_INPUT_COUNT = 592
EXPECTED_TERMINAL_FACE_CELL_COUNT = 1568
EXPECTED_INPUT_VOLUME = Q(2301, 2684354560000)
EXPECTED_PARENT_COUNTS = {
    "W:E:00.14.01101": 264,
    "W:E:02.11.110": 32,
    "W:E:05.04.001": 32,
    "W:E:07.01.10010": 264,
}
EXPECTED_ACTIVE_FACTOR_COUNTS = {"HMINUS": 296, "HPLUS": 296}
EXPECTED_CHART_COUNTS = {"N": 160, "S": 160, "W": 272}
EXPECTED_ACTIVE_SIGN_COUNTS = {"NEGATIVE": 272, "POSITIVE": 320}
EXPECTED_UPDATED_DYNAMIC_EXACT_COUNT = 19642
EXPECTED_UPDATED_DYNAMIC_RESIDUAL_COUNT = 15238
EXPECTED_UPDATED_COMBINED_RESIDUAL_COUNT = 16128
EXPECTED_UPDATED_DYNAMIC_EXACT_VOLUME = Q(139653, 1677721600000)
EXPECTED_UPDATED_DYNAMIC_RESIDUAL_VOLUME = Q(108147, 1677721600000)
EXPECTED_UPDATED_COMBINED_RESIDUAL_VOLUME = Q(
    35451507, 1677721600000
)
T_FACE_P_ATLAS_MAX_DEPTH = 2
AXES = ("t", "p", "s")
SIGNS = {"NEGATIVE", "POSITIVE"}
NEW_LOCAL_STATUS = "LOCAL_EXACT_KEY_FACTORIZED_T_FACE_C0_ATLAS"


class Round202Error(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise Round202Error(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def closed_row(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result["row_sha256"] = digest(result)
    return result


def file_sha256(path: Path, maximum: int = MAX_INPUT_BYTES) -> str:
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(metadata.st_nlink == 1, f"hardlink:{path.name}")
    require(metadata.st_size <= maximum, f"oversized:{path.name}")
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def read_regular(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(metadata.st_nlink == 1, f"hardlink:{path.name}")
    require(metadata.st_size <= maximum, f"oversized:{path.name}")
    data = path.read_bytes()
    require(len(data) == metadata.st_size, f"stable-size:{path.name}")
    return data


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_number(value: str) -> None:
    raise Round202Error(f"noninteger JSON number:{value}")


def validate_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(
                type(key) is str and "\x00" not in key,
                f"JSON key:{path}",
            )
            validate_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require("\x00" not in value, f"JSON NUL:{path}")


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"JSON encoding:{label}",
    )
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique_pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Round202Error(f"JSON parse:{label}:{exc}") from exc
    validate_tree(value)
    require(type(value) is dict, f"JSON top object:{label}")
    require(
        raw == canonical_bytes(value) + b"\n",
        f"canonical JSON:{label}",
    )
    return value


def manifest_entries(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise Round202Error("manifest ASCII") from exc
    require(text.endswith("\n"), "manifest final newline")
    result: dict[str, str] = {}
    for line in text.splitlines():
        pieces = line.split("  ", 1)
        require(len(pieces) == 2, "manifest line shape")
        value, name = pieces
        require(
            len(value) == 64
            and all(character in "0123456789abcdef" for character in value),
            f"manifest digest:{name}",
        )
        require(
            name not in result
            and "/" not in name
            and "\\" not in name
            and name not in {".", ".."},
            f"manifest name:{name}",
        )
        result[name] = value
    return result


def pin_round185_files() -> None:
    for name, expected in R185_PINS.items():
        require(
            file_sha256(HERE / name) == expected,
            f"Round185 file pin:{name}",
        )
    require(
        file_sha256(HERE / R185_MANIFEST) == R185_MANIFEST_SHA256,
        "Round185 manifest pin",
    )
    require(
        manifest_entries(read_regular(HERE / R185_MANIFEST)) == R185_PINS,
        "Round185 exact manifest entries",
    )


def load_round185() -> tuple[dict[str, Any], dict[str, Any]]:
    pin_round185_files()
    certificate = strict_json(
        read_regular(HERE / R185_CERTIFICATE),
        R185_CERTIFICATE,
    )
    verification = strict_json(
        read_regular(HERE / R185_VERIFICATION),
        R185_VERIFICATION,
    )
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["schema"] == R185_CERTIFICATE_SCHEMA
        and certificate["result_sha256"] == R185_RESULT_SHA256
        and digest(certificate["result"]) == R185_RESULT_SHA256,
        "Round185 certificate",
    )
    require(
        set(verification) == {"schema", "result", "result_sha256"}
        and verification["schema"] == R185_VERIFICATION_SCHEMA
        and verification["result_sha256"]
        == R185_VERIFICATION_RESULT_SHA256
        and digest(verification["result"])
        == R185_VERIFICATION_RESULT_SHA256,
        "Round185 verification wrapper",
    )
    checked = verification["result"]
    require(
        checked["status"] == "PASS"
        and checked["certificate_result_sha256"] == R185_RESULT_SHA256
        and checked["independently_rebuilt_result_sha256"]
        == R185_RESULT_SHA256
        and checked["full_expected_result_canonical_equality"] is True
        and checked["producer_imported_or_executed"] is False
        and checked["re_signed_semantic_attacks"]["rejected"] == 32
        and checked["re_signed_semantic_attacks"]["total"] == 32
        and checked["strict_JSON_attacks"]["rejected"] == 9
        and checked["strict_JSON_attacks"]["total"] == 9
        and checked["path_attacks"]["rejected"] == 11
        and checked["path_attacks"]["total"] == 11,
        "Round185 formal acceptance",
    )
    return certificate["result"], checked


def bounds(box: Any) -> tuple[tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]]:
    return (
        (box.t0, box.t1),
        (box.p0, box.p1),
        (box.s0, box.s1),
    )


def sign_name(value: int) -> str:
    return "POSITIVE" if value > 0 else "NEGATIVE" if value < 0 else "UNRESOLVED"


def factor_function(module: Any, factor: str) -> Any:
    require(factor in {"HPLUS", "HMINUS"}, "factor name")
    return (
        module.outgoing_hplus_ad
        if factor == "HPLUS"
        else module.outgoing_hminus_ad
    )


def factor_chart(hplus: str, hminus: str) -> str:
    require(hplus in SIGNS and hminus in SIGNS, "strict factor signs")
    if hplus == hminus:
        return "E" if hplus == "POSITIVE" else "W"
    return "N" if hplus == "POSITIVE" else "S"


def exact_box_payload(box: Any) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "volume": str(
            (box.t1 - box.t0)
            * (box.p1 - box.p0)
            * (box.s1 - box.s0)
        ),
    }


def cell_interval_record(
    module: Any,
    parent_key: str,
    box: Any,
    identifier: str,
    factor: str,
    face: str,
    p_path: str,
    depth: int,
) -> dict[str, Any]:
    function = factor_function(module, factor)
    full = function(parent_key, box, identifier)[0]
    center = tuple((low + high) / 2 for low, high in bounds(box))
    center_box = module.point_box(
        box,
        *center,
        ".round202-centered-C0",
    )
    center_value = function(parent_key, center_box, identifier)[0].value
    centered = center_value
    exact_half_widths = []
    for derivative, (low, high) in zip(full.derivative, bounds(box)):
        width = (high - low) / 2
        exact_half_widths.append(str(width))
        centered += derivative * module.BASE.arb_interval(-width, width)
    direct_sign = module.strict_sign(full.value)
    centered_sign = module.strict_sign(centered)
    require(
        not (
            direct_sign != 0
            and centered_sign != 0
            and direct_sign != centered_sign
        ),
        f"cell direct/centered sign:{parent_key}:{face}:{p_path}",
    )
    area = (box.p1 - box.p0) * (box.s1 - box.s0)
    record = {
        "face": face,
        "p_refinement_path": p_path,
        "relative_depth": depth,
        "factor": factor,
        "identifier": identifier,
        "cell_box": exact_box_payload(box),
        "exact_face_area": str(area),
        "exact_center_point": {
            axis: str(value) for axis, value in zip(AXES, center)
        },
        "exact_half_widths_t_p_s": exact_half_widths,
        "center_point_value": module.arb_bounds(center_value),
        "direct_C0_enclosure": module.arb_bounds(full.value),
        "direct_C0_sign": sign_name(direct_sign),
        "full_cell_C1_derivatives": {
            axis: {
                **module.arb_bounds(value),
                "strict_sign": sign_name(module.strict_sign(value)),
            }
            for axis, value in zip(AXES, full.derivative)
        },
        "centered_mean_value_C0_enclosure": module.arb_bounds(centered),
        "centered_C0_sign": sign_name(centered_sign),
        "centered_C0_formula":
            "h(center)+sum_i d_i(cell)*[-half_width_i,+half_width_i]",
        "regularity_is_not_existence": True,
    }
    return closed_row(record)


def t_face_atlas(
    module: Any,
    parent_key: str,
    parent: Any,
    identifier: str,
    factor: str,
    bit: int,
) -> dict[str, Any]:
    coordinate = (parent.t0, parent.t1)[bit]
    face = module.fixed_axis_box(
        parent,
        0,
        coordinate,
        ".round202-t-face",
    )
    face_name = "t-" if bit == 0 else "t+"
    face_area = (face.p1 - face.p0) * (face.s1 - face.s0)
    pending = [(face, 0, "")]
    terminals: list[dict[str, Any]] = []
    split_rows: list[dict[str, Any]] = []
    while pending:
        cell, depth, path = pending.pop()
        record = cell_interval_record(
            module,
            parent_key,
            cell,
            identifier,
            factor,
            face_name,
            path,
            depth,
        )
        if record["centered_C0_sign"] in SIGNS:
            terminals.append(record)
            continue
        require(
            depth < T_FACE_P_ATLAS_MAX_DEPTH,
            f"unresolved terminal face cell:{parent_key}:{face_name}:{path}",
        )
        left, right = module.split_axis(cell, 1)
        require(
            left.p0 == cell.p0
            and left.p1 == right.p0
            and right.p1 == cell.p1
            and left.t0 == left.t1 == coordinate
            and right.t0 == right.t1 == coordinate,
            "exact p-bisection",
        )
        split_rows.append(closed_row({
            "face": face_name,
            "parent_p_refinement_path": path,
            "relative_depth": depth,
            "axis": "p",
            "coordinate": str(left.p1),
            "left_child_path": path + "0",
            "right_child_path": path + "1",
            "half_open_owner": "LEFT",
            "right_child_excludes_common_split_face": True,
            "dimension": 1,
            "credit": 0,
        }))
        pending.extend(((right, depth + 1, path + "1"),
                        (left, depth + 1, path + "0")))
    terminals.sort(key=lambda row: row["p_refinement_path"])
    split_rows.sort(key=lambda row: row["parent_p_refinement_path"])
    signs = {row["centered_C0_sign"] for row in terminals}
    terminal_area = sum(
        (Q(row["exact_face_area"]) for row in terminals),
        Q(0),
    )
    require(
        signs <= SIGNS
        and len(signs) == 1
        and terminal_area == face_area,
        f"complete strict t-face atlas:{parent_key}:{face_name}",
    )
    return closed_row({
        "face": face_name,
        "t_coordinate": str(coordinate),
        "factor": factor,
        "identifier": identifier,
        "exact_face_area": str(face_area),
        "refinement_axis": "p",
        "maximum_allowed_relative_depth": T_FACE_P_ATLAS_MAX_DEPTH,
        "observed_maximum_relative_depth": max(
            row["relative_depth"] for row in terminals
        ),
        "split_count": len(split_rows),
        "split_rows": split_rows,
        "split_rows_sha256": digest(split_rows),
        "terminal_cell_count": len(terminals),
        "terminal_cell_rows": terminals,
        "terminal_cell_rows_sha256": digest(terminals),
        "resolved_face_sign": next(iter(signs)),
        "all_terminal_centered_C0_enclosures_strict": True,
        "all_terminal_signs_identical": True,
        "exact_face_area_conserved": True,
        "complete_centered_C0_atlas": True,
        "lower_dimensional_credit": 0,
        "whole_parent_or_stratum_credit": 0,
    })


def source_row_index(upstream183: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    rows = upstream183["dynamic_residual_ledger"]["rows"]
    result = {
        (row["origin_parent_key"], row["terminal_path"]): row
        for row in rows
    }
    require(len(result) == len(rows), "Round183 dynamic row uniqueness")
    return result


def reconstruct_one(
    module: Any,
    row: dict[str, Any],
    source: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    require(
        digest({
            key: value for key, value in row.items()
            if key != "row_sha256"
        }) == row["row_sha256"],
        f"Round185 input row hash:{row['terminal_path']}",
    )
    require(
        source["status"] == "OUTGOING_H2"
        and source["terminal_path"] == row["origin_terminal_path"]
        and source["origin_parent_key"] == row["origin_parent_key"]
        and source["detail"]["point_owner"] == row["detail"]["point_owner"]
        and digest({
            key: value for key, value in source.items()
            if key != "row_sha256"
        }) == source["row_sha256"],
        f"Round183 source binding:{row['terminal_path']}",
    )
    official = source["detail"]["official_gate5_key"]
    require(
        official["row_sha256"] == digest(official["row"])
        and official["word_key_id"]
        == (
            f"gate5-word:{official['ordinal_zero_based']}:"
            f"{official['row_sha256']}"
        )
        and source["detail"]["point_owner"]
        == row["detail"]["point_owner"],
        f"official Gate5 key binding:{row['terminal_path']}",
    )
    parent_key = row["origin_parent_key"]
    identifier = row["detail"]["point_owner"]
    box = module.box_from_payload(row["box"], row["terminal_path"])
    require(
        module.volume(box) == Q(row["box"]["volume"]),
        f"input volume:{row['terminal_path']}",
    )
    records = module.hfactor_records(parent_key, box, identifier)
    evidence = [records["HPLUS"], records["HMINUS"]]
    summaries = [
        module.compact_surface_summary(records["HPLUS"]),
        module.compact_surface_summary(records["HMINUS"]),
    ]
    require(
        summaries == row["surface_summaries"]
        and digest(evidence) == row["surface_evidence_rows_sha256"],
        f"Round185 factor evidence:{row['terminal_path']}",
    )
    by_kind = {
        summary["kind"]: summary for summary in summaries
    }
    active = [
        kind for kind in ("HPLUS", "HMINUS")
        if by_kind[kind]["centered_C0_sign"] == "UNRESOLVED"
    ]
    fixed = [
        kind for kind in ("HPLUS", "HMINUS")
        if by_kind[kind]["centered_C0_sign"] in SIGNS
    ]
    require(
        len(active) == len(fixed) == 1
        and by_kind[fixed[0]]["centered_C0_sign"] == "NEGATIVE"
        and by_kind[active[0]]["strict_derivative_axes"] == ["dt", "dp"]
        and by_kind[fixed[0]]["strict_derivative_axes"] == [],
        f"one active factor:{row['terminal_path']}",
    )
    active_kind, fixed_kind = active[0], fixed[0]
    active_record = records[active_kind]
    require(
        not active_record["full_box_C1_derivatives"]["dt"][
            "contains_zero"
        ],
        f"official strict dt:{row['terminal_path']}",
    )
    function = factor_function(module, active_kind)
    active_full = function(parent_key, box, identifier)[0]
    dt_sign = sign_name(module.strict_sign(active_full.derivative[0]))
    dp_sign = sign_name(module.strict_sign(active_full.derivative[1]))
    require(
        dt_sign in SIGNS and dp_sign in SIGNS,
        f"strict dt/dp:{row['terminal_path']}",
    )
    faces = [
        t_face_atlas(
            module,
            parent_key,
            box,
            identifier,
            active_kind,
            bit,
        )
        for bit in (0, 1)
    ]
    face_signs = [face["resolved_face_sign"] for face in faces]
    require(
        face_signs[0] == face_signs[1]
        and face_signs[0] in SIGNS,
        f"same-sign endpoint faces:{row['terminal_path']}",
    )
    active_sign = face_signs[0]
    hplus = active_sign if active_kind == "HPLUS" else "NEGATIVE"
    hminus = active_sign if active_kind == "HMINUS" else "NEGATIVE"
    chart = factor_chart(hplus, hminus)
    proof = {
        "theorem":
            "strict full-box dt plus two complete same-sign endpoint-face "
            "centered-C0 atlases excludes every active-factor zero",
        "active_factor": active_kind,
        "fixed_absent_factor": fixed_kind,
        "fixed_factor_sign": "NEGATIVE",
        "active_full_box_dt_sign": dt_sign,
        "active_full_box_dp_sign": dp_sign,
        "t_endpoint_face_signs": face_signs,
        "t_endpoint_face_signs_identical": True,
        "active_factor_zero_absent": True,
        "regularity_alone_used_as_existence": False,
        "factor_signs": {
            "h_plus": hplus,
            "h_minus": hminus,
        },
        "collision2_outgoing_chart": chart,
        "local_only": True,
        "whole_parent_or_stratum_credit": 0,
        "global_credit": 0,
    }
    evidence_row = closed_row({
        "Round185_input_row_sha256": row["row_sha256"],
        "Round183_source_row_sha256": source["row_sha256"],
        "origin_parent_key": parent_key,
        "origin_terminal_path": row["origin_terminal_path"],
        "terminal_path": row["terminal_path"],
        "box": row["box"],
        "point_owner": identifier,
        "active_factor": active_kind,
        "fixed_absent_factor": fixed_kind,
        "Round185_full_box_factor_records": evidence,
        "Round185_full_box_factor_records_sha256": digest(evidence),
        "t_endpoint_face_C0_atlases": faces,
        "t_endpoint_face_C0_atlases_sha256": digest(faces),
        "absence_proof": proof,
        "absence_proof_sha256": digest(proof),
        "formal_local_exact_key_credit": 1,
        "whole_parent_or_stratum_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })
    detail = {
        **copy.deepcopy(source["detail"]),
        "collision2_outgoing_chart": chart,
        "factor_signs": {
            "h_plus": hplus,
            "h_minus": hminus,
        },
        "exact_factorization_resolution": True,
        "active_factor": active_kind,
        "fixed_absent_factor": fixed_kind,
        "fixed_factor_sign": "NEGATIVE",
        "strict_dependent_axis": "t",
        "active_factor_full_box_dt_sign": dt_sign,
        "active_factor_full_box_dp_sign": dp_sign,
        "endpoint_face_C0_sign": active_sign,
        "complete_endpoint_face_centered_C0_atlas": True,
        "Round202_absence_evidence_row_sha256":
            evidence_row["row_sha256"],
        "local_exact_key_is_global_disposition": False,
    }
    require(
        all(detail[key] == value for key, value in source["detail"].items())
        and detail["official_gate5_key"] == official,
        f"source detail preservation:{row['terminal_path']}",
    )
    local_row = closed_row({
        "source_kind": row["source_kind"],
        "origin_parent_key": parent_key,
        "origin_terminal_path": row["origin_terminal_path"],
        "origin_status": row["origin_status"],
        "terminal_path": row["terminal_path"],
        "Round185_relative_depth": row["Round185_relative_depth"],
        "box": row["box"],
        "baseline_child_status": row["baseline_child_status"],
        "status": NEW_LOCAL_STATUS,
        "detail": detail,
        "surface_summaries": row["surface_summaries"],
        "surface_evidence_rows_sha256":
            row["surface_evidence_rows_sha256"],
        "Round202_absence_evidence_row_sha256":
            evidence_row["row_sha256"],
        "Round183_source_detail_sha256": digest(source["detail"]),
        "conditional_rank2_record": row["conditional_rank2_record"],
        "formal_local_exact_key_credit": 1,
        "global_credit": 0,
        "whole_parent_or_stratum_credit": 0,
    })
    return evidence_row, local_row


def status_volume(rows: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, str]]:
    counts: Counter[str] = Counter()
    volumes: Counter[str] = Counter()
    for row in rows:
        counts[row["status"]] += 1
        volumes[row["status"]] += Q(row["box"]["volume"])
    return (
        dict(sorted(counts.items())),
        {
            key: str(value)
            for key, value in sorted(volumes.items())
        },
    )


def updated_parent_rows(
    round185: dict[str, Any],
    new_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    new_by_parent = Counter(
        row["origin_parent_key"] for row in new_rows
    )
    output = []
    for old in round185["per_parent_partial_ledger"]["rows"]:
        key = old["parent_key"]
        delta = new_by_parent[key]
        require(
            old["Round185_residual_outer_count"] >= delta,
            f"parent residual delta:{key}",
        )
        output.append(closed_row({
            "parent_key": key,
            "Round183_combined_local_exact_key_box_count":
                old["Round183_combined_local_exact_key_box_count"],
            "Round185_dimensionally_arranged_H2_outer_count":
                old["Round185_dimensionally_arranged_H2_outer_count"],
            "Round185_local_exact_or_excluded_cell_count":
                old["Round185_local_exact_or_excluded_cell_count"],
            "Round185_residual_outer_count":
                old["Round185_residual_outer_count"],
            "Round202_new_local_H2_absence_count": delta,
            "Round202_local_exact_or_excluded_cell_count":
                old["Round185_local_exact_or_excluded_cell_count"] + delta,
            "Round202_residual_outer_count":
                old["Round185_residual_outer_count"] - delta,
            "all_dimensions_under_same_exact_key_closed": False,
            "status": "PARTIAL",
            "whole_parent_or_stratum_credit": 0,
        }))
    require(
        len(output) == 16
        and sum(
            row["Round202_new_local_H2_absence_count"]
            for row in output
        ) == EXPECTED_INPUT_COUNT
        and all(row["status"] == "PARTIAL" for row in output),
        "updated partial parent ledger",
    )
    return output


def build_result(producer_sha256: str) -> dict[str, Any]:
    round185, verification = load_round185()
    flint.ctx.prec = 384
    module = importlib.import_module(
        "cm2_round185_preconditioned_c1_residual_refinement_verifier"
    )
    require(
        Path(module.__file__).resolve() == (HERE / R185_VERIFIER).resolve()
        and file_sha256(Path(module.__file__).resolve())
        == R185_PINS[R185_VERIFIER]
        and flint.__version__ == "0.9.0"
        and module.atlas.ctx.prec == 384,
        "Round185 evaluator identity",
    )
    # Detect any import-time mutation of every frozen Round185 delivery item.
    pin_round185_files()
    upstream183, _upstream181, _upstream178 = module.load_chain()
    sources = source_row_index(upstream183)

    old_exact = round185["dynamic_local_exact_key_ledger"]["rows"]
    old_residual = round185["dynamic_residual_ledger"]["rows"]
    arrangements = round185[
        "dimensionally_arranged_H2_factor_seams"
    ]["rows"]
    inherited_residual = round185["inherited_residual_ledger"]["rows"]
    require(
        digest(old_exact) == R185_DYNAMIC_EXACT_ROWS_SHA256
        and digest(old_residual) == R185_DYNAMIC_RESIDUAL_ROWS_SHA256
        and digest(arrangements) == R185_H2_ARRANGEMENT_ROWS_SHA256
        and digest(inherited_residual)
        == R185_INHERITED_RESIDUAL_ROWS_SHA256,
        "Round185 principal row ledgers",
    )
    selected = [
        row for row in old_residual
        if row["status"] == "H2_FACTOR_EXISTENCE_RESIDUAL"
    ]
    selected.sort(key=lambda row: (
        row["origin_parent_key"], row["terminal_path"]
    ))
    require(
        len(selected) == EXPECTED_INPUT_COUNT
        and Counter(
            row["origin_parent_key"] for row in selected
        ) == EXPECTED_PARENT_COUNTS
        and sum(
            (Q(row["box"]["volume"]) for row in selected),
            Q(0),
        ) == EXPECTED_INPUT_VOLUME,
        "Round185 selected H2 cohort",
    )

    evidence_rows = []
    new_local_rows = []
    for index, row in enumerate(selected, 1):
        source_key = (
            row["origin_parent_key"],
            row["origin_terminal_path"],
        )
        require(
            source_key in sources,
            f"Round183 source exists:{row['terminal_path']}",
        )
        evidence, local = reconstruct_one(
            module,
            row,
            sources[source_key],
        )
        evidence_rows.append(evidence)
        new_local_rows.append(local)
        if index % 64 == 0 or index == len(selected):
            print(
                f"Round202 formal H2 absence {index}/{len(selected)}",
                file=sys.stderr,
                flush=True,
            )
    evidence_rows.sort(key=lambda row: (
        row["origin_parent_key"], row["terminal_path"]
    ))
    new_local_rows.sort(key=lambda row: (
        row["origin_parent_key"], row["terminal_path"]
    ))
    require(
        len({row["row_sha256"] for row in evidence_rows})
        == EXPECTED_INPUT_COUNT
        and len({row["row_sha256"] for row in new_local_rows})
        == EXPECTED_INPUT_COUNT,
        "new row uniqueness",
    )
    terminal_cell_count = sum(
        face["terminal_cell_count"]
        for row in evidence_rows
        for face in row["t_endpoint_face_C0_atlases"]
    )
    require(
        terminal_cell_count == EXPECTED_TERMINAL_FACE_CELL_COUNT,
        "terminal face-cell census",
    )
    retained_residual = [
        row for row in old_residual
        if row["status"] != "H2_FACTOR_EXISTENCE_RESIDUAL"
    ]
    old_residual_keys = {
        (row["origin_parent_key"], row["terminal_path"])
        for row in old_residual
    }
    selected_keys = {
        (row["origin_parent_key"], row["terminal_path"])
        for row in selected
    }
    retained_keys = {
        (row["origin_parent_key"], row["terminal_path"])
        for row in retained_residual
    }
    new_local_keys = {
        (row["origin_parent_key"], row["terminal_path"])
        for row in new_local_rows
    }
    require(
        len(old_residual_keys) == len(old_residual)
        and selected_keys.isdisjoint(retained_keys)
        and selected_keys | retained_keys == old_residual_keys
        and new_local_keys == selected_keys
        and len(new_local_keys) == EXPECTED_INPUT_COUNT,
        "selected/retained/new-local exact key-set partition",
    )
    updated_exact = sorted(
        old_exact + new_local_rows,
        key=lambda row: (
            row["origin_parent_key"],
            row["terminal_path"],
        ),
    )
    retained_residual.sort(key=lambda row: (
        row["origin_parent_key"], row["terminal_path"]
    ))
    require(
        len(updated_exact) == EXPECTED_UPDATED_DYNAMIC_EXACT_COUNT
        and len(retained_residual)
        == EXPECTED_UPDATED_DYNAMIC_RESIDUAL_COUNT
        and len({
            (row["origin_parent_key"], row["terminal_path"])
            for row in updated_exact
        }) == len(updated_exact)
        and len({
            (row["origin_parent_key"], row["terminal_path"])
            for row in retained_residual
        }) == len(retained_residual),
        "updated dynamic row census",
    )

    new_counts, new_volumes = status_volume(new_local_rows)
    exact_counts, exact_volumes = status_volume(updated_exact)
    residual_counts, residual_volumes = status_volume(retained_residual)
    updated_exact_volume = sum(
        (Q(row["box"]["volume"]) for row in updated_exact),
        Q(0),
    )
    updated_residual_volume = sum(
        (Q(row["box"]["volume"]) for row in retained_residual),
        Q(0),
    )
    arrangement_volume = sum(
        (Q(row["box"]["volume"]) for row in arrangements),
        Q(0),
    )
    inherited_residual_volume = sum(
        (Q(row["box"]["volume"]) for row in inherited_residual),
        Q(0),
    )
    combined_residual_volume = (
        updated_residual_volume + inherited_residual_volume
    )
    old_dynamic_output_volume = (
        Q(round185["dynamic_local_exact_key_ledger"][
            "exact_coordinate_volume"
        ])
        + Q(round185["dimensionally_arranged_H2_factor_seams"][
            "support_outer_exact_coordinate_volume"
        ])
        + Q(round185["dynamic_residual_ledger"][
            "exact_coordinate_outer_volume"
        ])
    )
    require(
        updated_exact_volume == EXPECTED_UPDATED_DYNAMIC_EXACT_VOLUME
        and updated_residual_volume
        == EXPECTED_UPDATED_DYNAMIC_RESIDUAL_VOLUME
        and combined_residual_volume
        == EXPECTED_UPDATED_COMBINED_RESIDUAL_VOLUME
        and updated_exact_volume
        + arrangement_volume
        + updated_residual_volume
        == old_dynamic_output_volume
        and len(retained_residual) + len(inherited_residual)
        == EXPECTED_UPDATED_COMBINED_RESIDUAL_COUNT,
        "updated exact conservation",
    )

    active_counts = Counter(
        row["active_factor"] for row in evidence_rows
    )
    chart_counts = Counter(
        row["absence_proof"]["collision2_outgoing_chart"]
        for row in evidence_rows
    )
    active_sign_counts = Counter(
        row["absence_proof"]["t_endpoint_face_signs"][0]
        for row in evidence_rows
    )
    depth_counts = Counter(
        face["observed_maximum_relative_depth"]
        for row in evidence_rows
        for face in row["t_endpoint_face_C0_atlases"]
    )
    require(
        active_counts == EXPECTED_ACTIVE_FACTOR_COUNTS
        and chart_counts == EXPECTED_CHART_COUNTS
        and active_sign_counts == EXPECTED_ACTIVE_SIGN_COUNTS
        and depth_counts == {0: 928, 1: 128, 2: 128},
        "formal H2 absence census",
    )
    local_key_ids = sorted({
        row["detail"]["official_gate5_key"]["word_key_id"]
        for row in updated_exact
    })
    local_ordinals = sorted({
        row["detail"]["official_gate5_key"]["ordinal_zero_based"]
        for row in updated_exact
    })
    require(
        local_key_ids
        == round185["dynamic_local_exact_key_ledger"][
            "local_gate5_key_ids"
        ]
        and local_ordinals
        == round185["dynamic_local_exact_key_ledger"][
            "local_gate5_ordinals_zero_based"
        ],
        "no new official Gate5 key identity",
    )
    parent_rows = updated_parent_rows(round185, new_local_rows)
    first_residual = retained_residual[0]

    return {
        "status":
            "PARTIAL_FORMAL_H2_FACTOR_T_FACE_C0_ABSENCE"
            "__NO_WHOLE_PARENT_PROMOTION",
        "Round185_binding": {
            "manifest_sha256": R185_MANIFEST_SHA256,
            "producer_sha256": R185_PINS[R185_PRODUCER],
            "certificate_file_sha256": R185_PINS[R185_CERTIFICATE],
            "certificate_result_sha256": R185_RESULT_SHA256,
            "verifier_sha256": R185_PINS[R185_VERIFIER],
            "verification_file_sha256": R185_PINS[R185_VERIFICATION],
            "verification_result_sha256":
                R185_VERIFICATION_RESULT_SHA256,
            "verification_status": verification["status"],
            "full_expected_result_canonical_equality":
                verification["full_expected_result_canonical_equality"],
            "formal_files_modified": False,
        },
        "formal_absence_contract": {
            "factorization": "H2=HPLUS*HMINUS",
            "selected_full_box_graph_axis": "t",
            "existence_and_regularity_separated": True,
            "absence_rule":
                "one strict full-box dt sign plus complete strict "
                "same-sign centered-C0 atlases on t- and t+",
            "endpoint_face_refinement_axis": "p",
            "maximum_endpoint_face_refinement_depth":
                T_FACE_P_ATLAS_MAX_DEPTH,
            "strict_derivative_alone_never_certifies_existence_or_absence":
                True,
            "factor_simultaneous_zero_excluded_by_fixed_factor_C0": True,
            "local_only": True,
            "whole_parent_or_stratum_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "H2_factor_t_face_C0_absence_evidence_ledger": {
            "row_count": len(evidence_rows),
            "rows_sha256": digest(evidence_rows),
            "rows": evidence_rows,
            "terminal_t_face_count": 2 * len(evidence_rows),
            "terminal_face_cell_count": terminal_cell_count,
            "active_factor_counts":
                dict(sorted(active_counts.items())),
            "active_factor_sign_counts":
                dict(sorted(active_sign_counts.items())),
            "outgoing_chart_counts":
                dict(sorted(chart_counts.items())),
            "endpoint_face_maximum_depth_counts": {
                str(key): value
                for key, value in sorted(depth_counts.items())
            },
            "input_exact_coordinate_volume": str(EXPECTED_INPUT_VOLUME),
            "every_cell_centered_C0_strict": True,
            "every_face_exact_area_conserved": True,
            "every_box_has_two_complete_same-sign_faces": True,
            "every_box_has_one_strict_full_box_dt_sign": True,
            "counterexample_count": 0,
        },
        "new_dynamic_local_exact_key_delta_ledger": {
            "row_count": len(new_local_rows),
            "rows_sha256": digest(new_local_rows),
            "rows": new_local_rows,
            "status_counts": new_counts,
            "status_volumes": new_volumes,
            "exact_coordinate_volume": str(EXPECTED_INPUT_VOLUME),
            "formal_local_exact_key_credit": len(new_local_rows),
            "whole_parent_or_stratum_credit": 0,
            "global_credit": 0,
        },
        "updated_dynamic_local_exact_key_ledger": {
            "Round185_prefix_row_count": len(old_exact),
            "Round185_prefix_rows_sha256":
                R185_DYNAMIC_EXACT_ROWS_SHA256,
            "Round202_delta_row_count": len(new_local_rows),
            "Round202_delta_rows_sha256": digest(new_local_rows),
            "row_count": len(updated_exact),
            "rows_sha256": digest(updated_exact),
            "row_sha256_ledger": [
                row["row_sha256"] for row in updated_exact
            ],
            "row_sha256_ledger_sha256": digest([
                row["row_sha256"] for row in updated_exact
            ]),
            "rows_materialized_by_Round185_binding_plus_Round202_delta":
                True,
            "status_counts": exact_counts,
            "status_volumes": exact_volumes,
            "exact_coordinate_volume": str(updated_exact_volume),
            "local_gate5_key_ids": local_key_ids,
            "local_gate5_ordinals_zero_based": local_ordinals,
            "whole_parent_or_stratum_credit": 0,
            "global_credit": 0,
        },
        "updated_dynamic_residual_ledger": {
            "Round185_input_row_count": len(old_residual),
            "Round185_input_rows_sha256":
                R185_DYNAMIC_RESIDUAL_ROWS_SHA256,
            "removed_H2_factor_existence_row_count": len(selected),
            "removed_rows_sha256": digest(selected),
            "row_count": len(retained_residual),
            "rows_sha256": digest(retained_residual),
            "row_sha256_ledger": [
                row["row_sha256"] for row in retained_residual
            ],
            "row_sha256_ledger_sha256": digest([
                row["row_sha256"] for row in retained_residual
            ]),
            "rows_materialized_by_Round185_order_preserving_filter":
                True,
            "status_counts": residual_counts,
            "status_volumes": residual_volumes,
            "exact_coordinate_outer_volume":
                str(updated_residual_volume),
            "H2_FACTOR_EXISTENCE_RESIDUAL_count": 0,
            "whole_parent_or_stratum_credit": 0,
            "global_credit": 0,
        },
        "unchanged_dimension_and_inherited_bindings": {
            "dimensionally_arranged_H2_row_count": len(arrangements),
            "dimensionally_arranged_H2_rows_sha256":
                R185_H2_ARRANGEMENT_ROWS_SHA256,
            "dimensionally_arranged_H2_support_outer_volume":
                str(arrangement_volume),
            "inherited_residual_row_count": len(inherited_residual),
            "inherited_residual_rows_sha256":
                R185_INHERITED_RESIDUAL_ROWS_SHA256,
            "inherited_residual_exact_coordinate_outer_volume":
                str(inherited_residual_volume),
            "unchanged": True,
        },
        "exact_conservation": {
            "Round185_dynamic_output_row_count":
                len(old_exact) + len(arrangements) + len(old_residual),
            "Round202_dynamic_output_row_count":
                len(updated_exact)
                + len(arrangements)
                + len(retained_residual),
            "Round185_dynamic_output_exact_coordinate_volume":
                str(old_dynamic_output_volume),
            "Round202_dynamic_exact_coordinate_volume":
                str(updated_exact_volume),
            "unchanged_H2_arrangement_support_outer_volume":
                str(arrangement_volume),
            "Round202_dynamic_residual_exact_coordinate_volume":
                str(updated_residual_volume),
            "Round202_dynamic_output_exact_coordinate_volume":
                str(
                    updated_exact_volume
                    + arrangement_volume
                    + updated_residual_volume
                ),
            "moved_H2_absence_exact_coordinate_volume":
                str(EXPECTED_INPUT_VOLUME),
            "integer_delta": 0,
            "exact_volume_delta": "0",
        },
        "exact_residual_census": {
            "Round185_dynamic_local_exact_key_count": len(old_exact),
            "Round202_new_dynamic_local_exact_key_count":
                len(new_local_rows),
            "Round202_dynamic_local_exact_key_count":
                len(updated_exact),
            "Round185_dynamic_residual_outer_count": len(old_residual),
            "Round202_dynamic_residual_outer_count":
                len(retained_residual),
            "Round185_inherited_residual_outer_count":
                len(inherited_residual),
            "Round202_combined_remaining_residual_outer_count":
                len(retained_residual) + len(inherited_residual),
            "Round202_combined_remaining_exact_coordinate_outer_volume":
                str(combined_residual_volume),
            "removed_H2_factor_existence_residual_count": len(selected),
            "removed_H2_factor_existence_exact_coordinate_volume":
                str(EXPECTED_INPUT_VOLUME),
            "integer_census_delta": 0,
        },
        "per_parent_partial_ledger": {
            "parent_count": len(parent_rows),
            "rows_sha256": digest(parent_rows),
            "rows": parent_rows,
            "fully_closed_live_strata": 0,
            "partial_live_strata": len(parent_rows),
            "whole_parent_or_stratum_promotions": 0,
        },
        "first_analytic_hard_blocker": {
            "first_residual_status": first_residual["status"],
            "first_residual_parent_key":
                first_residual["origin_parent_key"],
            "first_residual_terminal_path":
                first_residual["terminal_path"],
            "reason":
                "remaining Delta/root-order, point-winner, wall-endpoint, "
                "and inherited collision1/source carriers still lack their "
                "required complete local certificates",
        },
        "strict_nonpromotion": {
            "all_592_new_exact_keys_are_local": True,
            "all_other_Round185_dimensions_unchanged": True,
            "whole_parent_or_stratum_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "observed_point_289591_global_credit": 0,
            "inner_or_refined_box_290575_global_credit": 0,
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate":
            "centered/Krawczyk treatment of the remaining Delta/root-order "
            "and inherited collision1/source carriers; no whole-parent "
            "promotion until every dimension under the same exact key closes",
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(R185_PINS.items())),
            "Round185_manifest_sha256": R185_MANIFEST_SHA256,
            "python_flint_version": flint.__version__,
            "effective_Arb_precision_bits": module.atlas.ctx.prec,
            "Round199_imported_or_used_as_dependency": False,
            "Round185_files_modified": False,
        },
    }


def safe_write(path: Path, data: bytes) -> None:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent.resolve() == HERE, "output directory")
    allowed_name = (
        absolute.name == OUTPUT.name
        or (
            absolute.name.startswith(".cm2_round202_")
            and absolute.name.endswith("_certificate.json")
        )
    )
    require(allowed_name, "output allowlist")
    protected = {(HERE / name).resolve() for name in R185_PINS}
    protected.add((HERE / R185_MANIFEST).resolve())
    protected.add(Path(__file__).resolve())
    require(
        absolute.resolve(strict=False) not in protected,
        "protected output",
    )
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "output type",
        )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.",
        suffix=".tmp",
        dir=absolute.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, absolute)
        directory_descriptor = os.open(
            os.fspath(absolute.parent),
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    producer_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = build_result(producer_sha256)
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
