#!/usr/bin/env python3
"""Independent fail-closed verifier for the formal Round202 H2 absence atlas.

The Round202 producer is accepted only as pinned inert bytes.  It is never
imported or executed here.  This verifier starts from the frozen Round185
package, imports only the pinned Round185 verifier as a low-level interval-AD
evaluator, and independently reconstructs every selected box, terminal face
cell, local exact row, retained residual row, parent row, census, and exact
conservation field.  Acceptance is full canonical expected-result equality.
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
from typing import Any, Callable

import flint


HERE = Path(__file__).resolve().parent
PRODUCER_NAME = "cm2_round202_h2_factor_t_face_c0_absence.py"
PRODUCER = HERE / PRODUCER_NAME
CERTIFICATE_NAME = (
    "cm2_round202_h2_factor_t_face_c0_absence_certificate.json"
)
CERTIFICATE = HERE / CERTIFICATE_NAME
OUTPUT_NAME = "cm2_round202_h2_factor_t_face_c0_absence_verification.json"
OUTPUT = HERE / OUTPUT_NAME
SCHEMA = "cm2.round202.h2-factor-t-face-c0-absence.v1"
VERIFICATION_SCHEMA = (
    "cm2.round202.h2-factor-t-face-c0-absence-verification.v1"
)
PRODUCER_SHA256 = (
    "630f0e9177807499eda3a75de368d1fff3c8c3454532558703d08f0f80d33786"
)
CERTIFICATE_FILE_SHA256 = (
    "d33bf83615b3e5917c02e42e71e5f0cbb8da8eebd2a0b52af38042e1793cfe1c"
)
MAX_INPUT_BYTES = 160 * 1024 * 1024

R185_PREFIX = "cm2_round185_preconditioned_c1_residual_refinement"
R185_PRODUCER = f"{R185_PREFIX}.py"
R185_CERTIFICATE = f"{R185_PREFIX}_certificate.json"
R185_VERIFIER = f"{R185_PREFIX}_verifier.py"
R185_VERIFICATION = f"{R185_PREFIX}_verification.json"
R185_REPORT = f"{R185_PREFIX}_report.md"
R185_COLD = f"{R185_PREFIX}_cold_replay.md"
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
    R185_COLD:
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

SELECTED_COUNT = 592
TERMINAL_CELL_COUNT = 1568
SELECTED_VOLUME = Q(2301, 2684354560000)
PARENT_COUNTS = {
    "W:E:00.14.01101": 264,
    "W:E:02.11.110": 32,
    "W:E:05.04.001": 32,
    "W:E:07.01.10010": 264,
}
FACTOR_COUNTS = {"HMINUS": 296, "HPLUS": 296}
CHART_COUNTS = {"N": 160, "S": 160, "W": 272}
ACTIVE_SIGN_COUNTS = {"NEGATIVE": 272, "POSITIVE": 320}
FACE_DEPTH_COUNTS = {0: 928, 1: 128, 2: 128}
UPDATED_EXACT_COUNT = 19642
UPDATED_RESIDUAL_COUNT = 15238
COMBINED_RESIDUAL_COUNT = 16128
UPDATED_EXACT_VOLUME = Q(139653, 1677721600000)
UPDATED_RESIDUAL_VOLUME = Q(108147, 1677721600000)
COMBINED_RESIDUAL_VOLUME = Q(35451507, 1677721600000)
MAX_FACE_DEPTH = 2
AXES = ("t", "p", "s")
STRICT_SIGNS = {"NEGATIVE", "POSITIVE"}
LOCAL_STATUS = "LOCAL_EXACT_KEY_FACTORIZED_T_FACE_C0_ATLAS"


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


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


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def verify_row_hash(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items()
               if key != "row_sha256"}
    require(set(row) == set(payload) | {"row_sha256"}, f"row shape:{label}")
    require(row["row_sha256"] == digest(payload), f"row hash:{label}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_noninteger(token: str) -> None:
    raise VerificationError(f"noninteger JSON number:{token}")


def validate_json_tree(value: Any, path: str = "$") -> None:
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
            validate_json_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_json_tree(child, f"{path}[{index}]")
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
            object_pairs_hook=unique_object,
            parse_float=reject_noninteger,
            parse_constant=reject_noninteger,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"JSON parse:{label}:{exc}") from exc
    validate_json_tree(value)
    require(type(value) is dict, f"JSON top object:{label}")
    require(raw == canonical_bytes(value) + b"\n",
            f"canonical JSON:{label}")
    return value


def read_regular(
    path: Path,
    expected: str | None = None,
    maximum: int = MAX_INPUT_BYTES,
) -> bytes:
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(metadata.st_nlink == 1, f"hardlink:{path.name}")
    require(metadata.st_size <= maximum, f"oversized:{path.name}")
    with path.open("rb") as handle:
        data = handle.read(maximum + 1)
        require(len(data) <= maximum, f"oversized-read:{path.name}")
        require(handle.read(1) == b"", f"stable EOF:{path.name}")
    require(len(data) == metadata.st_size, f"stable size:{path.name}")
    if expected is not None:
        require(sha256_bytes(data) == expected, f"pin:{path.name}")
    return data


def parse_manifest(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise VerificationError("manifest ASCII") from exc
    require(text.endswith("\n"), "manifest newline")
    entries: dict[str, str] = {}
    for line in text.splitlines():
        parts = line.split("  ", 1)
        require(len(parts) == 2, "manifest line")
        value, name = parts
        require(
            len(value) == 64
            and all(character in "0123456789abcdef" for character in value),
            f"manifest digest:{name}",
        )
        require(
            name not in entries
            and name not in {"", ".", ".."}
            and "/" not in name
            and "\\" not in name,
            f"manifest name:{name}",
        )
        entries[name] = value
    return entries


def pin_round185_snapshot() -> dict[str, str]:
    observed = {
        name: sha256_bytes(read_regular(HERE / name))
        for name in R185_PINS
    }
    require(observed == R185_PINS, "Round185 six-file pins")
    manifest_raw = read_regular(
        HERE / R185_MANIFEST,
        R185_MANIFEST_SHA256,
    )
    require(parse_manifest(manifest_raw) == R185_PINS,
            "Round185 exact manifest")
    return observed


def producer_absent_from_modules() -> bool:
    producer_stem = Path(PRODUCER_NAME).stem
    if producer_stem in sys.modules:
        return False
    for loaded in tuple(sys.modules.values()):
        filename = getattr(loaded, "__file__", None)
        if filename and Path(filename).name == PRODUCER_NAME:
            return False
    return True


def load_frozen_inputs() -> tuple[
    dict[str, Any], dict[str, Any], Any, dict[str, Any]
]:
    require(producer_absent_from_modules(), "producer pre-import absence")
    read_regular(PRODUCER, PRODUCER_SHA256)
    pin_round185_snapshot()

    round185_certificate = strict_json(
        read_regular(HERE / R185_CERTIFICATE, R185_PINS[R185_CERTIFICATE]),
        R185_CERTIFICATE,
    )
    round185_verification = strict_json(
        read_regular(HERE / R185_VERIFICATION, R185_PINS[R185_VERIFICATION]),
        R185_VERIFICATION,
    )
    require(
        set(round185_certificate) == {"schema", "result", "result_sha256"}
        and round185_certificate["schema"] == R185_CERTIFICATE_SCHEMA
        and round185_certificate["result_sha256"] == R185_RESULT_SHA256
        and digest(round185_certificate["result"]) == R185_RESULT_SHA256,
        "Round185 certificate wrapper",
    )
    require(
        set(round185_verification) == {"schema", "result", "result_sha256"}
        and round185_verification["schema"] == R185_VERIFICATION_SCHEMA
        and round185_verification["result_sha256"]
        == R185_VERIFICATION_RESULT_SHA256
        and digest(round185_verification["result"])
        == R185_VERIFICATION_RESULT_SHA256,
        "Round185 verification wrapper",
    )
    accepted185 = round185_verification["result"]
    require(
        accepted185["status"] == "PASS"
        and accepted185["certificate_result_sha256"] == R185_RESULT_SHA256
        and accepted185["independently_rebuilt_result_sha256"]
        == R185_RESULT_SHA256
        and accepted185["full_expected_result_canonical_equality"] is True
        and accepted185["producer_imported_or_executed"] is False
        and accepted185["re_signed_semantic_attacks"]["rejected"] == 32
        and accepted185["re_signed_semantic_attacks"]["total"] == 32
        and accepted185["strict_JSON_attacks"]["rejected"] == 9
        and accepted185["strict_JSON_attacks"]["total"] == 9
        and accepted185["path_attacks"]["rejected"] == 11
        and accepted185["path_attacks"]["total"] == 11,
        "Round185 formal acceptance",
    )

    # The import boundary is deliberately after the complete byte snapshot.
    evaluator = importlib.import_module(
        "cm2_round185_preconditioned_c1_residual_refinement_verifier"
    )
    require(
        Path(evaluator.__file__).resolve() == (HERE / R185_VERIFIER).resolve()
        and sha256_bytes(read_regular(Path(evaluator.__file__)))
        == R185_PINS[R185_VERIFIER],
        "Round185 evaluator identity",
    )
    pin_round185_snapshot()
    require(
        flint.__version__ == "0.9.0"
        and evaluator.atlas.ctx.prec == 384,
        "frozen numeric environment",
    )
    upstream183, _upstream181, _upstream178 = evaluator.load_chain()
    pin_round185_snapshot()
    read_regular(PRODUCER, PRODUCER_SHA256)
    require(producer_absent_from_modules(), "producer post-evaluation absence")
    return (
        round185_certificate["result"],
        accepted185,
        evaluator,
        upstream183,
    )


def coordinate_bounds(box: Any) -> tuple[
    tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]
]:
    return (
        (box.t0, box.t1),
        (box.p0, box.p1),
        (box.s0, box.s1),
    )


def sign_label(sign: int) -> str:
    if sign > 0:
        return "POSITIVE"
    if sign < 0:
        return "NEGATIVE"
    return "UNRESOLVED"


def factor_evaluator(evaluator: Any, factor: str) -> Callable[..., Any]:
    require(factor in {"HPLUS", "HMINUS"}, "factor selector")
    if factor == "HPLUS":
        return evaluator.outgoing_hplus_ad
    return evaluator.outgoing_hminus_ad


def chart_for_signs(hplus: str, hminus: str) -> str:
    require(
        hplus in STRICT_SIGNS and hminus in STRICT_SIGNS,
        "strict chart inputs",
    )
    if hplus == hminus:
        return "E" if hplus == "POSITIVE" else "W"
    return "N" if hplus == "POSITIVE" else "S"


def exact_box(box: Any) -> dict[str, Any]:
    extents = coordinate_bounds(box)
    exact_volume = Q(1)
    for low, high in extents:
        exact_volume *= high - low
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "volume": str(exact_volume),
    }


def independently_evaluate_face_cell(
    evaluator: Any,
    *,
    parent_key: str,
    cell: Any,
    point_owner: str,
    active_factor: str,
    face_name: str,
    refinement_path: str,
    relative_depth: int,
) -> dict[str, Any]:
    function = factor_evaluator(evaluator, active_factor)
    full_ad = function(parent_key, cell, point_owner)[0]
    extents = coordinate_bounds(cell)
    center = tuple((low + high) / 2 for low, high in extents)
    point = evaluator.point_box(
        cell,
        *center,
        ".round202-centered-C0",
    )
    point_value = function(parent_key, point, point_owner)[0].value

    centered_enclosure = point_value
    half_widths: list[str] = []
    for derivative, (low, high) in zip(full_ad.derivative, extents):
        half_width = (high - low) / 2
        half_widths.append(str(half_width))
        centered_enclosure += (
            derivative
            * evaluator.BASE.arb_interval(-half_width, half_width)
        )

    direct_sign = evaluator.strict_sign(full_ad.value)
    centered_sign = evaluator.strict_sign(centered_enclosure)
    require(
        not (
            direct_sign != 0
            and centered_sign != 0
            and direct_sign != centered_sign
        ),
        f"direct/centered contradiction:"
        f"{parent_key}:{face_name}:{refinement_path}",
    )
    exact_area = (cell.p1 - cell.p0) * (cell.s1 - cell.s0)
    derivative_records = {}
    for axis, derivative in zip(AXES, full_ad.derivative):
        derivative_records[axis] = {
            **evaluator.arb_bounds(derivative),
            "strict_sign": sign_label(evaluator.strict_sign(derivative)),
        }
    return close_row({
        "face": face_name,
        "p_refinement_path": refinement_path,
        "relative_depth": relative_depth,
        "factor": active_factor,
        "identifier": point_owner,
        "cell_box": exact_box(cell),
        "exact_face_area": str(exact_area),
        "exact_center_point": {
            axis: str(value) for axis, value in zip(AXES, center)
        },
        "exact_half_widths_t_p_s": half_widths,
        "center_point_value": evaluator.arb_bounds(point_value),
        "direct_C0_enclosure": evaluator.arb_bounds(full_ad.value),
        "direct_C0_sign": sign_label(direct_sign),
        "full_cell_C1_derivatives": derivative_records,
        "centered_mean_value_C0_enclosure":
            evaluator.arb_bounds(centered_enclosure),
        "centered_C0_sign": sign_label(centered_sign),
        "centered_C0_formula":
            "h(center)+sum_i d_i(cell)*[-half_width_i,+half_width_i]",
        "regularity_is_not_existence": True,
    })


def independently_rebuild_face(
    evaluator: Any,
    *,
    parent_key: str,
    parent_box: Any,
    point_owner: str,
    active_factor: str,
    endpoint: int,
) -> dict[str, Any]:
    require(endpoint in {0, 1}, "endpoint bit")
    t_coordinate = (parent_box.t0, parent_box.t1)[endpoint]
    face_box = evaluator.fixed_axis_box(
        parent_box,
        0,
        t_coordinate,
        ".round202-t-face",
    )
    face_name = "t-" if endpoint == 0 else "t+"
    face_area = (
        (face_box.p1 - face_box.p0)
        * (face_box.s1 - face_box.s0)
    )
    terminals: list[dict[str, Any]] = []
    splits: list[dict[str, Any]] = []

    def visit(cell: Any, depth: int, path: str) -> None:
        record = independently_evaluate_face_cell(
            evaluator,
            parent_key=parent_key,
            cell=cell,
            point_owner=point_owner,
            active_factor=active_factor,
            face_name=face_name,
            refinement_path=path,
            relative_depth=depth,
        )
        if record["centered_C0_sign"] in STRICT_SIGNS:
            terminals.append(record)
            return
        require(
            depth < MAX_FACE_DEPTH,
            f"unresolved terminal:{parent_key}:{face_name}:{path}",
        )
        left, right = evaluator.split_axis(cell, 1)
        require(
            left.p0 == cell.p0
            and left.p1 == right.p0
            and right.p1 == cell.p1
            and left.t0 == left.t1 == t_coordinate
            and right.t0 == right.t1 == t_coordinate,
            f"exact p split:{parent_key}:{face_name}:{path}",
        )
        splits.append(close_row({
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
        visit(left, depth + 1, path + "0")
        visit(right, depth + 1, path + "1")

    visit(face_box, 0, "")
    terminals.sort(key=lambda item: item["p_refinement_path"])
    splits.sort(key=lambda item: item["parent_p_refinement_path"])
    for index, terminal in enumerate(terminals):
        verify_row_hash(
            terminal,
            f"rebuilt terminal:{parent_key}:{face_name}:{index}",
        )
    for index, split in enumerate(splits):
        verify_row_hash(
            split,
            f"rebuilt split:{parent_key}:{face_name}:{index}",
        )
    signs = {item["centered_C0_sign"] for item in terminals}
    conserved_area = sum(
        (Q(item["exact_face_area"]) for item in terminals),
        Q(0),
    )
    require(
        len(signs) == 1
        and signs <= STRICT_SIGNS
        and conserved_area == face_area,
        f"complete face atlas:{parent_key}:{face_name}",
    )
    return close_row({
        "face": face_name,
        "t_coordinate": str(t_coordinate),
        "factor": active_factor,
        "identifier": point_owner,
        "exact_face_area": str(face_area),
        "refinement_axis": "p",
        "maximum_allowed_relative_depth": MAX_FACE_DEPTH,
        "observed_maximum_relative_depth": max(
            item["relative_depth"] for item in terminals
        ),
        "split_count": len(splits),
        "split_rows": splits,
        "split_rows_sha256": digest(splits),
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


def index_round183_sources(
    upstream183: dict[str, Any],
) -> dict[tuple[str, str], dict[str, Any]]:
    source_rows = upstream183["dynamic_residual_ledger"]["rows"]
    source_index: dict[tuple[str, str], dict[str, Any]] = {}
    for row in source_rows:
        key = (row["origin_parent_key"], row["terminal_path"])
        require(key not in source_index, f"Round183 source duplicate:{key}")
        source_index[key] = row
    require(len(source_index) == len(source_rows),
            "Round183 source index census")
    return source_index


def independently_rebuild_selected_row(
    evaluator: Any,
    round185_row: dict[str, Any],
    source183: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    terminal_path = round185_row["terminal_path"]
    verify_row_hash(round185_row, f"Round185 selected:{terminal_path}")
    verify_row_hash(source183, f"Round183 source:{terminal_path}")
    require(
        source183["status"] == "OUTGOING_H2"
        and source183["origin_parent_key"]
        == round185_row["origin_parent_key"]
        and source183["terminal_path"]
        == round185_row["origin_terminal_path"]
        and source183["detail"]["point_owner"]
        == round185_row["detail"]["point_owner"],
        f"Round183/185 binding:{terminal_path}",
    )
    official_key = source183["detail"]["official_gate5_key"]
    require(
        official_key["row_sha256"] == digest(official_key["row"])
        and official_key["word_key_id"]
        == (
            f"gate5-word:{official_key['ordinal_zero_based']}:"
            f"{official_key['row_sha256']}"
        ),
        f"official Gate5 identity:{terminal_path}",
    )

    parent_key = round185_row["origin_parent_key"]
    point_owner = round185_row["detail"]["point_owner"]
    parent_box = evaluator.box_from_payload(
        round185_row["box"],
        terminal_path,
    )
    require(
        evaluator.volume(parent_box) == Q(round185_row["box"]["volume"]),
        f"selected exact volume:{terminal_path}",
    )
    records_by_factor = evaluator.hfactor_records(
        parent_key,
        parent_box,
        point_owner,
    )
    full_factor_records = [
        records_by_factor["HPLUS"],
        records_by_factor["HMINUS"],
    ]
    summaries = [
        evaluator.compact_surface_summary(records_by_factor["HPLUS"]),
        evaluator.compact_surface_summary(records_by_factor["HMINUS"]),
    ]
    require(
        summaries == round185_row["surface_summaries"]
        and digest(full_factor_records)
        == round185_row["surface_evidence_rows_sha256"],
        f"Round185 factor evidence binding:{terminal_path}",
    )
    summary_by_factor = {item["kind"]: item for item in summaries}
    active_factors = [
        factor for factor in ("HPLUS", "HMINUS")
        if summary_by_factor[factor]["centered_C0_sign"] == "UNRESOLVED"
    ]
    fixed_factors = [
        factor for factor in ("HPLUS", "HMINUS")
        if summary_by_factor[factor]["centered_C0_sign"] in STRICT_SIGNS
    ]
    require(
        len(active_factors) == 1
        and len(fixed_factors) == 1,
        f"unique active/fixed factor:{terminal_path}",
    )
    active_factor = active_factors[0]
    fixed_factor = fixed_factors[0]
    require(
        summary_by_factor[fixed_factor]["centered_C0_sign"] == "NEGATIVE"
        and summary_by_factor[active_factor]["strict_derivative_axes"]
        == ["dt", "dp"]
        and summary_by_factor[fixed_factor]["strict_derivative_axes"] == [],
        f"factor roles:{terminal_path}",
    )
    require(
        records_by_factor[active_factor][
            "full_box_C1_derivatives"
        ]["dt"]["contains_zero"] is False,
        f"official strict dt:{terminal_path}",
    )
    active_ad = factor_evaluator(
        evaluator,
        active_factor,
    )(parent_key, parent_box, point_owner)[0]
    dt_sign = sign_label(evaluator.strict_sign(active_ad.derivative[0]))
    dp_sign = sign_label(evaluator.strict_sign(active_ad.derivative[1]))
    require(
        dt_sign in STRICT_SIGNS and dp_sign in STRICT_SIGNS,
        f"independent strict dt/dp:{terminal_path}",
    )

    face_rows = [
        independently_rebuild_face(
            evaluator,
            parent_key=parent_key,
            parent_box=parent_box,
            point_owner=point_owner,
            active_factor=active_factor,
            endpoint=endpoint,
        )
        for endpoint in (0, 1)
    ]
    face_signs = [row["resolved_face_sign"] for row in face_rows]
    require(
        face_signs[0] == face_signs[1]
        and face_signs[0] in STRICT_SIGNS,
        f"same-sign endpoint faces:{terminal_path}",
    )
    active_sign = face_signs[0]
    hplus_sign = (
        active_sign if active_factor == "HPLUS" else "NEGATIVE"
    )
    hminus_sign = (
        active_sign if active_factor == "HMINUS" else "NEGATIVE"
    )
    outgoing_chart = chart_for_signs(hplus_sign, hminus_sign)

    proof = {
        "theorem":
            "strict full-box dt plus two complete same-sign endpoint-face "
            "centered-C0 atlases excludes every active-factor zero",
        "active_factor": active_factor,
        "fixed_absent_factor": fixed_factor,
        "fixed_factor_sign": "NEGATIVE",
        "active_full_box_dt_sign": dt_sign,
        "active_full_box_dp_sign": dp_sign,
        "t_endpoint_face_signs": face_signs,
        "t_endpoint_face_signs_identical": True,
        "active_factor_zero_absent": True,
        "regularity_alone_used_as_existence": False,
        "factor_signs": {
            "h_plus": hplus_sign,
            "h_minus": hminus_sign,
        },
        "collision2_outgoing_chart": outgoing_chart,
        "local_only": True,
        "whole_parent_or_stratum_credit": 0,
        "global_credit": 0,
    }
    evidence_row = close_row({
        "Round185_input_row_sha256": round185_row["row_sha256"],
        "Round183_source_row_sha256": source183["row_sha256"],
        "origin_parent_key": parent_key,
        "origin_terminal_path": round185_row["origin_terminal_path"],
        "terminal_path": terminal_path,
        "box": round185_row["box"],
        "point_owner": point_owner,
        "active_factor": active_factor,
        "fixed_absent_factor": fixed_factor,
        "Round185_full_box_factor_records": full_factor_records,
        "Round185_full_box_factor_records_sha256":
            digest(full_factor_records),
        "t_endpoint_face_C0_atlases": face_rows,
        "t_endpoint_face_C0_atlases_sha256": digest(face_rows),
        "absence_proof": proof,
        "absence_proof_sha256": digest(proof),
        "formal_local_exact_key_credit": 1,
        "whole_parent_or_stratum_credit": 0,
        "global_exact_key_disposition_credit": 0,
    })

    local_detail = copy.deepcopy(source183["detail"])
    local_detail.update({
        "collision2_outgoing_chart": outgoing_chart,
        "factor_signs": {
            "h_plus": hplus_sign,
            "h_minus": hminus_sign,
        },
        "exact_factorization_resolution": True,
        "active_factor": active_factor,
        "fixed_absent_factor": fixed_factor,
        "fixed_factor_sign": "NEGATIVE",
        "strict_dependent_axis": "t",
        "active_factor_full_box_dt_sign": dt_sign,
        "active_factor_full_box_dp_sign": dp_sign,
        "endpoint_face_C0_sign": active_sign,
        "complete_endpoint_face_centered_C0_atlas": True,
        "Round202_absence_evidence_row_sha256":
            evidence_row["row_sha256"],
        "local_exact_key_is_global_disposition": False,
    })
    require(
        all(
            local_detail[key] == value
            for key, value in source183["detail"].items()
        )
        and local_detail["official_gate5_key"] == official_key,
        f"source detail preservation:{terminal_path}",
    )
    local_row = close_row({
        "source_kind": round185_row["source_kind"],
        "origin_parent_key": parent_key,
        "origin_terminal_path": round185_row["origin_terminal_path"],
        "origin_status": round185_row["origin_status"],
        "terminal_path": terminal_path,
        "Round185_relative_depth": round185_row["Round185_relative_depth"],
        "box": round185_row["box"],
        "baseline_child_status": round185_row["baseline_child_status"],
        "status": LOCAL_STATUS,
        "detail": local_detail,
        "surface_summaries": round185_row["surface_summaries"],
        "surface_evidence_rows_sha256":
            round185_row["surface_evidence_rows_sha256"],
        "Round202_absence_evidence_row_sha256":
            evidence_row["row_sha256"],
        "Round183_source_detail_sha256": digest(source183["detail"]),
        "conditional_rank2_record":
            round185_row["conditional_rank2_record"],
        "formal_local_exact_key_credit": 1,
        "global_credit": 0,
        "whole_parent_or_stratum_credit": 0,
    })
    verify_row_hash(evidence_row, f"new evidence:{terminal_path}")
    verify_row_hash(local_row, f"new local:{terminal_path}")
    return evidence_row, local_row


def status_census(
    rows: list[dict[str, Any]],
) -> tuple[dict[str, int], dict[str, str]]:
    counts: Counter[str] = Counter()
    volumes: Counter[str] = Counter()
    for row in rows:
        counts[row["status"]] += 1
        volumes[row["status"]] += Q(row["box"]["volume"])
    return (
        dict(sorted(counts.items())),
        {
            status: str(volume)
            for status, volume in sorted(volumes.items())
        },
    )


def independently_update_parent_rows(
    round185: dict[str, Any],
    local_delta: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    delta_by_parent = Counter(
        row["origin_parent_key"] for row in local_delta
    )
    rebuilt: list[dict[str, Any]] = []
    for prior in round185["per_parent_partial_ledger"]["rows"]:
        parent_key = prior["parent_key"]
        moved = delta_by_parent[parent_key]
        require(
            0 <= moved <= prior["Round185_residual_outer_count"],
            f"parent residual movement:{parent_key}",
        )
        rebuilt.append(close_row({
            "parent_key": parent_key,
            "Round183_combined_local_exact_key_box_count":
                prior["Round183_combined_local_exact_key_box_count"],
            "Round185_dimensionally_arranged_H2_outer_count":
                prior["Round185_dimensionally_arranged_H2_outer_count"],
            "Round185_local_exact_or_excluded_cell_count":
                prior["Round185_local_exact_or_excluded_cell_count"],
            "Round185_residual_outer_count":
                prior["Round185_residual_outer_count"],
            "Round202_new_local_H2_absence_count": moved,
            "Round202_local_exact_or_excluded_cell_count":
                prior["Round185_local_exact_or_excluded_cell_count"]
                + moved,
            "Round202_residual_outer_count":
                prior["Round185_residual_outer_count"] - moved,
            "all_dimensions_under_same_exact_key_closed": False,
            "status": "PARTIAL",
            "whole_parent_or_stratum_credit": 0,
        }))
    require(
        len(rebuilt) == 16
        and sum(
            row["Round202_new_local_H2_absence_count"]
            for row in rebuilt
        ) == SELECTED_COUNT
        and all(
            row["status"] == "PARTIAL"
            and row["whole_parent_or_stratum_credit"] == 0
            for row in rebuilt
        ),
        "parent partial ledger",
    )
    return rebuilt


def independently_reconstruct() -> tuple[dict[str, Any], dict[str, Any]]:
    round185, accepted185, evaluator, upstream183 = load_frozen_inputs()
    flint.ctx.prec = 384
    require(evaluator.atlas.ctx.prec == 384, "effective precision")

    old_exact = round185["dynamic_local_exact_key_ledger"]["rows"]
    old_residual = round185["dynamic_residual_ledger"]["rows"]
    h2_arrangements = round185[
        "dimensionally_arranged_H2_factor_seams"
    ]["rows"]
    inherited_residual = round185["inherited_residual_ledger"]["rows"]
    require(
        digest(old_exact) == R185_DYNAMIC_EXACT_ROWS_SHA256
        and digest(old_residual) == R185_DYNAMIC_RESIDUAL_ROWS_SHA256
        and digest(h2_arrangements) == R185_H2_ARRANGEMENT_ROWS_SHA256
        and digest(inherited_residual)
        == R185_INHERITED_RESIDUAL_ROWS_SHA256,
        "Round185 ledger pins",
    )

    selected = sorted(
        (
            row for row in old_residual
            if row["status"] == "H2_FACTOR_EXISTENCE_RESIDUAL"
        ),
        key=lambda row: (
            row["origin_parent_key"],
            row["terminal_path"],
        ),
    )
    selected_key_set = {
        (row["origin_parent_key"], row["terminal_path"])
        for row in selected
    }
    require(
        len(selected) == SELECTED_COUNT
        and len(selected_key_set) == SELECTED_COUNT
        and Counter(
            row["origin_parent_key"] for row in selected
        ) == PARENT_COUNTS
        and sum(
            (Q(row["box"]["volume"]) for row in selected),
            Q(0),
        ) == SELECTED_VOLUME,
        "independent selected cohort",
    )
    source_index = index_round183_sources(upstream183)

    evidence_delta: list[dict[str, Any]] = []
    local_delta: list[dict[str, Any]] = []
    for ordinal, selected_row in enumerate(selected, 1):
        source_key = (
            selected_row["origin_parent_key"],
            selected_row["origin_terminal_path"],
        )
        require(
            source_key in source_index,
            f"Round183 source present:{selected_row['terminal_path']}",
        )
        evidence_row, local_row = independently_rebuild_selected_row(
            evaluator,
            selected_row,
            source_index[source_key],
        )
        evidence_delta.append(evidence_row)
        local_delta.append(local_row)
        if ordinal % 64 == 0 or ordinal == SELECTED_COUNT:
            print(
                f"Round202 independent reconstruction "
                f"{ordinal}/{SELECTED_COUNT}",
                file=sys.stderr,
                flush=True,
            )
    evidence_delta.sort(
        key=lambda row: (
            row["origin_parent_key"],
            row["terminal_path"],
        )
    )
    local_delta.sort(
        key=lambda row: (
            row["origin_parent_key"],
            row["terminal_path"],
        )
    )
    require(
        len({row["row_sha256"] for row in evidence_delta})
        == SELECTED_COUNT
        and len({row["row_sha256"] for row in local_delta})
        == SELECTED_COUNT,
        "new row digest uniqueness",
    )

    rebuilt_cell_count = 0
    for evidence_row in evidence_delta:
        verify_row_hash(
            evidence_row,
            f"evidence closure:{evidence_row['terminal_path']}",
        )
        faces = evidence_row["t_endpoint_face_C0_atlases"]
        require(
            len(faces) == 2
            and [face["face"] for face in faces] == ["t-", "t+"]
            and faces[0]["resolved_face_sign"]
            == faces[1]["resolved_face_sign"],
            f"two same-sign faces:{evidence_row['terminal_path']}",
        )
        for face in faces:
            verify_row_hash(
                face,
                f"face closure:{evidence_row['terminal_path']}:"
                f"{face['face']}",
            )
            require(
                face["terminal_cell_rows_sha256"]
                == digest(face["terminal_cell_rows"])
                and face["split_rows_sha256"]
                == digest(face["split_rows"])
                and face["terminal_cell_count"]
                == len(face["terminal_cell_rows"])
                and face["split_count"] == len(face["split_rows"]),
                f"face inner ledgers:{evidence_row['terminal_path']}:"
                f"{face['face']}",
            )
            rebuilt_cell_count += face["terminal_cell_count"]
    require(rebuilt_cell_count == TERMINAL_CELL_COUNT,
            "independent terminal cell census")

    retained_residual = sorted(
        (
            row for row in old_residual
            if row["status"] != "H2_FACTOR_EXISTENCE_RESIDUAL"
        ),
        key=lambda row: (
            row["origin_parent_key"],
            row["terminal_path"],
        ),
    )
    old_key_set = {
        (row["origin_parent_key"], row["terminal_path"])
        for row in old_residual
    }
    retained_key_set = {
        (row["origin_parent_key"], row["terminal_path"])
        for row in retained_residual
    }
    local_key_set = {
        (row["origin_parent_key"], row["terminal_path"])
        for row in local_delta
    }
    require(
        len(old_key_set) == len(old_residual)
        and selected_key_set.isdisjoint(retained_key_set)
        and selected_key_set | retained_key_set == old_key_set
        and local_key_set == selected_key_set,
        "exact selected/retained/local partition",
    )
    updated_exact = sorted(
        [*old_exact, *local_delta],
        key=lambda row: (
            row["origin_parent_key"],
            row["terminal_path"],
        ),
    )
    require(
        len(updated_exact) == UPDATED_EXACT_COUNT
        and len(retained_residual) == UPDATED_RESIDUAL_COUNT
        and len({
            (row["origin_parent_key"], row["terminal_path"])
            for row in updated_exact
        }) == UPDATED_EXACT_COUNT
        and len(retained_key_set) == UPDATED_RESIDUAL_COUNT,
        "updated row census and key uniqueness",
    )

    delta_counts, delta_volumes = status_census(local_delta)
    exact_counts, exact_volumes = status_census(updated_exact)
    residual_counts, residual_volumes = status_census(retained_residual)
    updated_exact_volume = sum(
        (Q(row["box"]["volume"]) for row in updated_exact),
        Q(0),
    )
    updated_residual_volume = sum(
        (Q(row["box"]["volume"]) for row in retained_residual),
        Q(0),
    )
    arrangement_volume = sum(
        (Q(row["box"]["volume"]) for row in h2_arrangements),
        Q(0),
    )
    inherited_residual_volume = sum(
        (Q(row["box"]["volume"]) for row in inherited_residual),
        Q(0),
    )
    combined_residual_volume = (
        updated_residual_volume + inherited_residual_volume
    )
    old_dynamic_volume = (
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
        updated_exact_volume == UPDATED_EXACT_VOLUME
        and updated_residual_volume == UPDATED_RESIDUAL_VOLUME
        and combined_residual_volume == COMBINED_RESIDUAL_VOLUME
        and updated_exact_volume
        + arrangement_volume
        + updated_residual_volume
        == old_dynamic_volume
        and len(retained_residual) + len(inherited_residual)
        == COMBINED_RESIDUAL_COUNT,
        "independent exact conservation",
    )

    active_counts = Counter(
        row["active_factor"] for row in evidence_delta
    )
    active_sign_counts = Counter(
        row["absence_proof"]["t_endpoint_face_signs"][0]
        for row in evidence_delta
    )
    chart_counts = Counter(
        row["absence_proof"]["collision2_outgoing_chart"]
        for row in evidence_delta
    )
    depth_counts = Counter(
        face["observed_maximum_relative_depth"]
        for row in evidence_delta
        for face in row["t_endpoint_face_C0_atlases"]
    )
    require(
        active_counts == FACTOR_COUNTS
        and active_sign_counts == ACTIVE_SIGN_COUNTS
        and chart_counts == CHART_COUNTS
        and depth_counts == FACE_DEPTH_COUNTS,
        "independent factor/sign/chart/depth census",
    )

    local_gate5_ids = sorted({
        row["detail"]["official_gate5_key"]["word_key_id"]
        for row in updated_exact
    })
    local_gate5_ordinals = sorted({
        row["detail"]["official_gate5_key"]["ordinal_zero_based"]
        for row in updated_exact
    })
    require(
        local_gate5_ids
        == round185["dynamic_local_exact_key_ledger"][
            "local_gate5_key_ids"
        ]
        and local_gate5_ordinals
        == round185["dynamic_local_exact_key_ledger"][
            "local_gate5_ordinals_zero_based"
        ],
        "no Gate5 identity promotion",
    )
    parent_rows = independently_update_parent_rows(round185, local_delta)
    first_residual = retained_residual[0]
    exact_row_hashes = [row["row_sha256"] for row in updated_exact]
    residual_row_hashes = [
        row["row_sha256"] for row in retained_residual
    ]

    expected = {
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
            "verification_status": accepted185["status"],
            "full_expected_result_canonical_equality":
                accepted185["full_expected_result_canonical_equality"],
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
            "maximum_endpoint_face_refinement_depth": MAX_FACE_DEPTH,
            "strict_derivative_alone_never_certifies_existence_or_absence":
                True,
            "factor_simultaneous_zero_excluded_by_fixed_factor_C0": True,
            "local_only": True,
            "whole_parent_or_stratum_credit": 0,
            "global_exact_key_disposition_credit": 0,
        },
        "H2_factor_t_face_C0_absence_evidence_ledger": {
            "row_count": len(evidence_delta),
            "rows_sha256": digest(evidence_delta),
            "rows": evidence_delta,
            "terminal_t_face_count": 2 * len(evidence_delta),
            "terminal_face_cell_count": rebuilt_cell_count,
            "active_factor_counts": dict(sorted(active_counts.items())),
            "active_factor_sign_counts":
                dict(sorted(active_sign_counts.items())),
            "outgoing_chart_counts": dict(sorted(chart_counts.items())),
            "endpoint_face_maximum_depth_counts": {
                str(depth): count
                for depth, count in sorted(depth_counts.items())
            },
            "input_exact_coordinate_volume": str(SELECTED_VOLUME),
            "every_cell_centered_C0_strict": True,
            "every_face_exact_area_conserved": True,
            "every_box_has_two_complete_same-sign_faces": True,
            "every_box_has_one_strict_full_box_dt_sign": True,
            "counterexample_count": 0,
        },
        "new_dynamic_local_exact_key_delta_ledger": {
            "row_count": len(local_delta),
            "rows_sha256": digest(local_delta),
            "rows": local_delta,
            "status_counts": delta_counts,
            "status_volumes": delta_volumes,
            "exact_coordinate_volume": str(SELECTED_VOLUME),
            "formal_local_exact_key_credit": len(local_delta),
            "whole_parent_or_stratum_credit": 0,
            "global_credit": 0,
        },
        "updated_dynamic_local_exact_key_ledger": {
            "Round185_prefix_row_count": len(old_exact),
            "Round185_prefix_rows_sha256":
                R185_DYNAMIC_EXACT_ROWS_SHA256,
            "Round202_delta_row_count": len(local_delta),
            "Round202_delta_rows_sha256": digest(local_delta),
            "row_count": len(updated_exact),
            "rows_sha256": digest(updated_exact),
            "row_sha256_ledger": exact_row_hashes,
            "row_sha256_ledger_sha256": digest(exact_row_hashes),
            "rows_materialized_by_Round185_binding_plus_Round202_delta":
                True,
            "status_counts": exact_counts,
            "status_volumes": exact_volumes,
            "exact_coordinate_volume": str(updated_exact_volume),
            "local_gate5_key_ids": local_gate5_ids,
            "local_gate5_ordinals_zero_based": local_gate5_ordinals,
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
            "row_sha256_ledger": residual_row_hashes,
            "row_sha256_ledger_sha256": digest(residual_row_hashes),
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
            "dimensionally_arranged_H2_row_count": len(h2_arrangements),
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
                len(old_exact) + len(h2_arrangements) + len(old_residual),
            "Round202_dynamic_output_row_count":
                len(updated_exact)
                + len(h2_arrangements)
                + len(retained_residual),
            "Round185_dynamic_output_exact_coordinate_volume":
                str(old_dynamic_volume),
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
                str(SELECTED_VOLUME),
            "integer_delta": 0,
            "exact_volume_delta": "0",
        },
        "exact_residual_census": {
            "Round185_dynamic_local_exact_key_count": len(old_exact),
            "Round202_new_dynamic_local_exact_key_count":
                len(local_delta),
            "Round202_dynamic_local_exact_key_count": len(updated_exact),
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
                str(SELECTED_VOLUME),
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
            "producer_sha256": PRODUCER_SHA256,
            "dependency_sha256": dict(sorted(R185_PINS.items())),
            "Round185_manifest_sha256": R185_MANIFEST_SHA256,
            "python_flint_version": flint.__version__,
            "effective_Arb_precision_bits": evaluator.atlas.ctx.prec,
            "Round199_imported_or_used_as_dependency": False,
            "Round185_files_modified": False,
        },
    }
    pin_round185_snapshot()
    read_regular(PRODUCER, PRODUCER_SHA256)
    require(producer_absent_from_modules(), "producer final absence")
    reconstruction_summary = {
        "Round185_dynamic_exact_input_count": len(old_exact),
        "Round185_dynamic_residual_input_count": len(old_residual),
        "selected_H2_factor_existence_count": len(selected),
        "selected_exact_coordinate_volume": str(SELECTED_VOLUME),
        "rebuilt_evidence_row_count": len(evidence_delta),
        "rebuilt_terminal_face_count": 2 * len(evidence_delta),
        "rebuilt_centered_C0_terminal_cell_count": rebuilt_cell_count,
        "rebuilt_local_exact_delta_count": len(local_delta),
        "updated_dynamic_exact_count": len(updated_exact),
        "updated_dynamic_residual_count": len(retained_residual),
        "combined_remaining_residual_count":
            len(retained_residual) + len(inherited_residual),
        "active_factor_counts": dict(sorted(active_counts.items())),
        "active_factor_sign_counts":
            dict(sorted(active_sign_counts.items())),
        "outgoing_chart_counts": dict(sorted(chart_counts.items())),
        "face_maximum_depth_counts": {
            str(depth): count
            for depth, count in sorted(depth_counts.items())
        },
        "updated_dynamic_exact_volume": str(updated_exact_volume),
        "updated_dynamic_residual_volume": str(updated_residual_volume),
        "combined_remaining_residual_volume":
            str(combined_residual_volume),
        "fully_closed_live_strata": 0,
        "whole_parent_or_stratum_credit": 0,
        "global_exact_key_disposition_credit": 0,
        "D02": "BLOCKED",
        "global_Gate5_fields": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return expected, reconstruction_summary


def validate_candidate(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    require(
        set(candidate) == {"schema", "result", "result_sha256"},
        "certificate envelope shape",
    )
    require(candidate["schema"] == SCHEMA, "certificate schema")
    require(
        candidate["result_sha256"] == digest(candidate["result"]),
        "certificate self digest",
    )
    require(
        candidate["result"] == expected,
        "full independently rebuilt expected canonical equality",
    )


def resign_envelope(candidate: dict[str, Any]) -> None:
    candidate["result_sha256"] = digest(candidate["result"])


def resign_closed_row(row: dict[str, Any]) -> None:
    payload = copy.deepcopy(row)
    payload.pop("row_sha256", None)
    row["row_sha256"] = digest(payload)


def refresh_evidence_row(
    result: dict[str, Any],
    evidence_index: int,
    face_index: int | None = None,
) -> None:
    ledger = result["H2_factor_t_face_C0_absence_evidence_ledger"]
    evidence = ledger["rows"][evidence_index]
    if face_index is not None:
        face = evidence["t_endpoint_face_C0_atlases"][face_index]
        face["terminal_cell_rows_sha256"] = digest(
            face["terminal_cell_rows"]
        )
        face["split_rows_sha256"] = digest(face["split_rows"])
        resign_closed_row(face)
    evidence["t_endpoint_face_C0_atlases_sha256"] = digest(
        evidence["t_endpoint_face_C0_atlases"]
    )
    evidence["absence_proof_sha256"] = digest(evidence["absence_proof"])
    evidence["Round185_full_box_factor_records_sha256"] = digest(
        evidence["Round185_full_box_factor_records"]
    )
    resign_closed_row(evidence)
    ledger["rows_sha256"] = digest(ledger["rows"])


def refresh_delta_row(result: dict[str, Any], index: int) -> None:
    ledger = result["new_dynamic_local_exact_key_delta_ledger"]
    resign_closed_row(ledger["rows"][index])
    ledger["rows_sha256"] = digest(ledger["rows"])


def refresh_parent_row(result: dict[str, Any], index: int) -> None:
    ledger = result["per_parent_partial_ledger"]
    resign_closed_row(ledger["rows"][index])
    ledger["rows_sha256"] = digest(ledger["rows"])


def semantic_resigning_attacks(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    Mutation = Callable[[dict[str, Any]], None]
    attacks: list[tuple[str, Mutation]] = []

    def evidence(result: dict[str, Any], index: int = 0) -> dict[str, Any]:
        return result[
            "H2_factor_t_face_C0_absence_evidence_ledger"
        ]["rows"][index]

    def mutate_active_factor(result: dict[str, Any]) -> None:
        row = evidence(result)
        row["active_factor"], row["fixed_absent_factor"] = (
            row["fixed_absent_factor"],
            row["active_factor"],
        )
        refresh_evidence_row(result, 0)

    def mutate_proof_active_factor(result: dict[str, Any]) -> None:
        row = evidence(result)
        current = row["absence_proof"]["active_factor"]
        row["absence_proof"]["active_factor"] = (
            "HMINUS" if current == "HPLUS" else "HPLUS"
        )
        refresh_evidence_row(result, 0)

    def mutate_fixed_factor_sign(result: dict[str, Any]) -> None:
        evidence(result)["absence_proof"]["fixed_factor_sign"] = "POSITIVE"
        refresh_evidence_row(result, 0)

    def mutate_dt_sign(result: dict[str, Any]) -> None:
        proof = evidence(result)["absence_proof"]
        proof["active_full_box_dt_sign"] = (
            "NEGATIVE"
            if proof["active_full_box_dt_sign"] == "POSITIVE"
            else "POSITIVE"
        )
        refresh_evidence_row(result, 0)

    def mutate_dp_sign(result: dict[str, Any]) -> None:
        proof = evidence(result)["absence_proof"]
        proof["active_full_box_dp_sign"] = (
            "NEGATIVE"
            if proof["active_full_box_dp_sign"] == "POSITIVE"
            else "POSITIVE"
        )
        refresh_evidence_row(result, 0)

    def mutate_endpoint_agreement(result: dict[str, Any]) -> None:
        proof = evidence(result)["absence_proof"]
        proof["t_endpoint_face_signs"][1] = (
            "NEGATIVE"
            if proof["t_endpoint_face_signs"][0] == "POSITIVE"
            else "POSITIVE"
        )
        refresh_evidence_row(result, 0)

    def mutate_face_sign(result: dict[str, Any]) -> None:
        row = evidence(result)
        face = row["t_endpoint_face_C0_atlases"][1]
        face["resolved_face_sign"] = (
            "NEGATIVE"
            if face["resolved_face_sign"] == "POSITIVE"
            else "POSITIVE"
        )
        refresh_evidence_row(result, 0, 1)

    def mutate_terminal_sign(result: dict[str, Any]) -> None:
        row = evidence(result)
        cell = row["t_endpoint_face_C0_atlases"][0][
            "terminal_cell_rows"
        ][0]
        cell["centered_C0_sign"] = "UNRESOLVED"
        resign_closed_row(cell)
        refresh_evidence_row(result, 0, 0)

    def mutate_terminal_enclosure(result: dict[str, Any]) -> None:
        row = evidence(result)
        cell = row["t_endpoint_face_C0_atlases"][0][
            "terminal_cell_rows"
        ][0]
        cell["centered_mean_value_C0_enclosure"]["contains_zero"] = True
        resign_closed_row(cell)
        refresh_evidence_row(result, 0, 0)

    def corrupt_terminal_row_hash(result: dict[str, Any]) -> None:
        cell = evidence(result)["t_endpoint_face_C0_atlases"][0][
            "terminal_cell_rows"
        ][0]
        cell["row_sha256"] = "0" * 64
        refresh_evidence_row(result, 0, 0)

    def mutate_cell_area(result: dict[str, Any]) -> None:
        cell = evidence(result)["t_endpoint_face_C0_atlases"][0][
            "terminal_cell_rows"
        ][0]
        cell["exact_face_area"] = "0"
        resign_closed_row(cell)
        refresh_evidence_row(result, 0, 0)

    def mutate_face_area(result: dict[str, Any]) -> None:
        evidence(result)["t_endpoint_face_C0_atlases"][0][
            "exact_face_area"
        ] = "0"
        refresh_evidence_row(result, 0, 0)

    def split_location(
        result: dict[str, Any],
    ) -> tuple[int, int, dict[str, Any]]:
        rows = result[
            "H2_factor_t_face_C0_absence_evidence_ledger"
        ]["rows"]
        for row_index, row in enumerate(rows):
            for face_index, face in enumerate(
                row["t_endpoint_face_C0_atlases"]
            ):
                if face["split_rows"]:
                    return row_index, face_index, face["split_rows"][0]
        raise VerificationError("attack split witness missing")

    def mutate_split_lineage(result: dict[str, Any]) -> None:
        row_index, face_index, split = split_location(result)
        split["left_child_path"] = split["right_child_path"]
        resign_closed_row(split)
        refresh_evidence_row(result, row_index, face_index)

    def mutate_split_coordinate(result: dict[str, Any]) -> None:
        row_index, face_index, split = split_location(result)
        split["coordinate"] = "0"
        resign_closed_row(split)
        refresh_evidence_row(result, row_index, face_index)

    def mutate_split_owner(result: dict[str, Any]) -> None:
        row_index, face_index, split = split_location(result)
        split["half_open_owner"] = "RIGHT"
        resign_closed_row(split)
        refresh_evidence_row(result, row_index, face_index)

    def mutate_local_global_flag(result: dict[str, Any]) -> None:
        row = result["new_dynamic_local_exact_key_delta_ledger"]["rows"][0]
        row["detail"]["local_exact_key_is_global_disposition"] = True
        refresh_delta_row(result, 0)

    def mutate_local_global_credit(result: dict[str, Any]) -> None:
        row = result["new_dynamic_local_exact_key_delta_ledger"]["rows"][0]
        row["global_credit"] = 1
        refresh_delta_row(result, 0)

    def mutate_local_whole_credit(result: dict[str, Any]) -> None:
        row = result["new_dynamic_local_exact_key_delta_ledger"]["rows"][0]
        row["whole_parent_or_stratum_credit"] = 1
        refresh_delta_row(result, 0)

    def corrupt_local_row_hash(result: dict[str, Any]) -> None:
        ledger = result["new_dynamic_local_exact_key_delta_ledger"]
        ledger["rows"][0]["row_sha256"] = "f" * 64
        ledger["rows_sha256"] = digest(ledger["rows"])

    def mutate_parent_full(result: dict[str, Any]) -> None:
        row = result["per_parent_partial_ledger"]["rows"][0]
        row["status"] = "FULL"
        row["all_dimensions_under_same_exact_key_closed"] = True
        row["whole_parent_or_stratum_credit"] = 1
        refresh_parent_row(result, 0)

    attacks.extend([
        (
            "active_fixed_factor_roles_swapped_and_resigned",
            mutate_active_factor,
        ),
        (
            "absence_proof_active_factor_changed_and_resigned",
            mutate_proof_active_factor,
        ),
        (
            "fixed_absent_factor_sign_forged_positive",
            mutate_fixed_factor_sign,
        ),
        ("active_full_box_dt_sign_reversed", mutate_dt_sign),
        ("active_full_box_dp_sign_reversed", mutate_dp_sign),
        ("two_endpoint_faces_forged_opposite_sign", mutate_endpoint_agreement),
        ("terminal_face_resolved_sign_changed", mutate_face_sign),
        ("terminal_cell_centered_sign_unresolved", mutate_terminal_sign),
        (
            "terminal_cell_centered_enclosure_contains_zero",
            mutate_terminal_enclosure,
        ),
        ("terminal_cell_row_hash_corrupted", corrupt_terminal_row_hash),
        ("terminal_cell_exact_area_zeroed", mutate_cell_area),
        ("complete_face_exact_area_zeroed", mutate_face_area),
        ("split_child_lineage_collapsed", mutate_split_lineage),
        ("split_exact_coordinate_changed", mutate_split_coordinate),
        ("split_half_open_owner_changed", mutate_split_owner),
        (
            "Round185_manifest_binding_changed",
            lambda result: result["Round185_binding"].__setitem__(
                "manifest_sha256", "0" * 64
            ),
        ),
        (
            "Round185_verifier_binding_changed",
            lambda result: result["Round185_binding"].__setitem__(
                "verifier_sha256", "0" * 64
            ),
        ),
        (
            "Round185_formal_files_forged_modified",
            lambda result: result["Round185_binding"].__setitem__(
                "formal_files_modified", True
            ),
        ),
        (
            "evidence_ledger_rows_sha256_changed",
            lambda result: result[
                "H2_factor_t_face_C0_absence_evidence_ledger"
            ].__setitem__("rows_sha256", "0" * 64),
        ),
        (
            "evidence_row_count_changed",
            lambda result: result[
                "H2_factor_t_face_C0_absence_evidence_ledger"
            ].__setitem__("row_count", SELECTED_COUNT - 1),
        ),
        (
            "terminal_face_cell_census_changed",
            lambda result: result[
                "H2_factor_t_face_C0_absence_evidence_ledger"
            ].__setitem__("terminal_face_cell_count", TERMINAL_CELL_COUNT - 1),
        ),
        (
            "active_factor_census_changed",
            lambda result: result[
                "H2_factor_t_face_C0_absence_evidence_ledger"
            ]["active_factor_counts"].__setitem__("HPLUS", 295),
        ),
        (
            "outgoing_chart_census_changed",
            lambda result: result[
                "H2_factor_t_face_C0_absence_evidence_ledger"
            ]["outgoing_chart_counts"].__setitem__("W", 271),
        ),
        (
            "input_selected_exact_volume_changed",
            lambda result: result[
                "H2_factor_t_face_C0_absence_evidence_ledger"
            ].__setitem__("input_exact_coordinate_volume", "0"),
        ),
        ("local_row_promoted_to_global", mutate_local_global_flag),
        ("local_row_global_credit_forged", mutate_local_global_credit),
        ("local_row_whole_parent_credit_forged", mutate_local_whole_credit),
        ("local_row_hash_corrupted", corrupt_local_row_hash),
        (
            "local_delta_count_changed",
            lambda result: result[
                "new_dynamic_local_exact_key_delta_ledger"
            ].__setitem__("row_count", SELECTED_COUNT - 1),
        ),
        (
            "updated_exact_count_changed",
            lambda result: result[
                "updated_dynamic_local_exact_key_ledger"
            ].__setitem__("row_count", UPDATED_EXACT_COUNT - 1),
        ),
        (
            "updated_exact_rows_hash_changed",
            lambda result: result[
                "updated_dynamic_local_exact_key_ledger"
            ].__setitem__("rows_sha256", "0" * 64),
        ),
        (
            "updated_exact_row_hash_ledger_resigned_wrong",
            lambda result: (
                result["updated_dynamic_local_exact_key_ledger"][
                    "row_sha256_ledger"
                ].__setitem__(0, "0" * 64),
                result["updated_dynamic_local_exact_key_ledger"].__setitem__(
                    "row_sha256_ledger_sha256",
                    digest(result[
                        "updated_dynamic_local_exact_key_ledger"
                    ]["row_sha256_ledger"]),
                ),
            ),
        ),
        (
            "updated_exact_volume_changed",
            lambda result: result[
                "updated_dynamic_local_exact_key_ledger"
            ].__setitem__("exact_coordinate_volume", "0"),
        ),
        (
            "retained_residual_count_changed",
            lambda result: result[
                "updated_dynamic_residual_ledger"
            ].__setitem__("row_count", UPDATED_RESIDUAL_COUNT - 1),
        ),
        (
            "retained_residual_rows_hash_changed",
            lambda result: result[
                "updated_dynamic_residual_ledger"
            ].__setitem__("rows_sha256", "0" * 64),
        ),
        (
            "removed_H2_residual_count_changed",
            lambda result: result[
                "updated_dynamic_residual_ledger"
            ].__setitem__(
                "removed_H2_factor_existence_row_count",
                SELECTED_COUNT - 1,
            ),
        ),
        (
            "H2_residual_forged_remaining",
            lambda result: result[
                "updated_dynamic_residual_ledger"
            ].__setitem__("H2_FACTOR_EXISTENCE_RESIDUAL_count", 1),
        ),
        (
            "retained_residual_volume_changed",
            lambda result: result[
                "updated_dynamic_residual_ledger"
            ].__setitem__("exact_coordinate_outer_volume", "0"),
        ),
        (
            "combined_residual_census_changed",
            lambda result: result["exact_residual_census"].__setitem__(
                "Round202_combined_remaining_residual_outer_count",
                COMBINED_RESIDUAL_COUNT - 1,
            ),
        ),
        (
            "combined_residual_volume_changed",
            lambda result: result["exact_residual_census"].__setitem__(
                "Round202_combined_remaining_exact_coordinate_outer_volume",
                "0",
            ),
        ),
        (
            "conservation_integer_delta_changed",
            lambda result: result["exact_conservation"].__setitem__(
                "integer_delta", 1
            ),
        ),
        (
            "conservation_exact_volume_delta_changed",
            lambda result: result["exact_conservation"].__setitem__(
                "exact_volume_delta", "1"
            ),
        ),
        ("one_parent_forged_full", mutate_parent_full),
        (
            "all_parents_forged_full",
            lambda result: (
                result["per_parent_partial_ledger"].__setitem__(
                    "fully_closed_live_strata", 16
                ),
                result["per_parent_partial_ledger"].__setitem__(
                    "partial_live_strata", 0
                ),
                result["per_parent_partial_ledger"].__setitem__(
                    "whole_parent_or_stratum_promotions", 16
                ),
            ),
        ),
        (
            "first_residual_status_changed",
            lambda result: result["first_analytic_hard_blocker"].__setitem__(
                "first_residual_status", "H2_FACTOR_EXISTENCE_RESIDUAL"
            ),
        ),
        (
            "first_residual_path_changed",
            lambda result: result["first_analytic_hard_blocker"].__setitem__(
                "first_residual_terminal_path", "forged"
            ),
        ),
        (
            "unchanged_dimension_binding_forged_changed",
            lambda result: result[
                "unchanged_dimension_and_inherited_bindings"
            ].__setitem__("unchanged", False),
        ),
        (
            "D02_forged_pass",
            lambda result: result["strict_nonpromotion"].__setitem__(
                "D02", "PASS"
            ),
        ),
        (
            "Gate5_forged_18_of_18",
            lambda result: result["strict_nonpromotion"].__setitem__(
                "global_Gate5_fields", "18/18"
            ),
        ),
        (
            "global_complete_block_forged",
            lambda result: result["strict_nonpromotion"].__setitem__(
                "global_complete_18_field_blocks", 1
            ),
        ),
        (
            "CM2_forged_go",
            lambda result: result["strict_nonpromotion"].__setitem__(
                "CM2", "GO"
            ),
        ),
        (
            "partial_status_forged_full",
            lambda result: result.__setitem__(
                "status", "FULL_FORMAL_GLOBAL_PROMOTION"
            ),
        ),
    ])

    rejected: list[str] = []
    for label, mutate in attacks:
        forged = copy.deepcopy(certificate)
        before = canonical_bytes(forged["result"])
        mutate(forged["result"])
        require(
            canonical_bytes(forged["result"]) != before,
            f"attack made no change:{label}",
        )
        resign_envelope(forged)
        require(
            forged["result_sha256"] == digest(forged["result"]),
            f"attack top-level resign:{label}",
        )
        try:
            validate_candidate(forged, expected)
        except VerificationError:
            rejected.append(label)
        else:
            raise VerificationError(f"semantic attack accepted:{label}")
    return rejected


def strict_json_attacks(certificate: dict[str, Any]) -> list[str]:
    canonical = canonical_bytes(certificate) + b"\n"
    cases = {
        "duplicate_key": b'{"x":1,"x":2}\n',
        "floating_point": b'{"x":1.25}\n',
        "floating_exponent": b'{"x":1e2}\n',
        "NaN_constant": b'{"x":NaN}\n',
        "Infinity_constant": b'{"x":Infinity}\n',
        "UTF8_BOM": b"\xef\xbb\xbf" + canonical,
        "embedded_NUL": b'{"x":"a\x00b"}\n',
        "invalid_UTF8": b'{"x":"\xff"}\n',
        "leading_whitespace": b" " + canonical,
        "trailing_document": canonical + b"{}\n",
        "top_level_list": b"[]\n",
        "missing_final_newline": canonical[:-1],
        "CRLF_noncanonical": canonical[:-1] + b"\r\n",
    }
    rejected: list[str] = []
    for label, raw in cases.items():
        try:
            strict_json(raw, f"attack:{label}")
        except VerificationError:
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    return rejected


def has_parent_alias(path: Path) -> bool:
    return any(part == ".." for part in path.parts)


def validate_certificate_path(path: Path) -> Path:
    require(not has_parent_alias(path), "certificate parent alias")
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute == CERTIFICATE, "certificate exact path")
    require(absolute.parent.resolve() == HERE, "certificate directory")
    require(absolute.name == CERTIFICATE_NAME, "certificate exact name")
    return absolute


def validate_output_path(path: Path) -> Path:
    require(not has_parent_alias(path), "output parent alias")
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE and absolute.parent.resolve() == HERE,
        "output exact directory",
    )
    allowed_name = (
        absolute.name == OUTPUT_NAME
        or (
            absolute.name.startswith(".cm2_round202_")
            and absolute.name.endswith("_verification.json")
        )
    )
    require(allowed_name, "output allowlist")
    protected = {
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        Path(__file__).resolve(),
        (HERE / R185_MANIFEST).resolve(),
    }
    protected.update((HERE / name).resolve() for name in R185_PINS)
    require(
        absolute.resolve(strict=False) not in protected,
        "protected output",
    )
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode),
            f"output regular:{absolute.name}",
        )
        require(not absolute.is_symlink(),
                f"output symlink:{absolute.name}")
        require(metadata.st_nlink == 1,
                f"output hardlink:{absolute.name}")
    return absolute


def filesystem_path_attacks() -> list[str]:
    rejected: list[str] = []
    with tempfile.TemporaryDirectory(
        dir=HERE,
        prefix=".round202-verifier-path-",
    ) as temporary_name:
        root = Path(temporary_name)
        regular = root / "regular"
        regular.write_bytes(b"x")
        symlink = root / "symlink"
        symlink.symlink_to(regular)
        hardlink = root / "hardlink"
        os.link(regular, hardlink)
        directory = root / "directory"
        directory.mkdir()
        fifo = root / "fifo"
        os.mkfifo(fifo)
        oversized = root / "oversized"
        oversized.write_bytes(b"xx")

        output_symlink = (
            HERE / f".cm2_round202_{root.name}_symlink_verification.json"
        )
        output_hardlink = (
            HERE / f".cm2_round202_{root.name}_hardlink_verification.json"
        )
        output_fifo = (
            HERE / f".cm2_round202_{root.name}_fifo_verification.json"
        )
        output_directory = (
            HERE / f".cm2_round202_{root.name}_directory_verification.json"
        )
        output_symlink.symlink_to(regular)
        os.link(regular, output_hardlink)
        os.mkfifo(output_fifo)
        output_directory.mkdir()
        certificate_parent_alias = (
            HERE / ".." / HERE.name / CERTIFICATE_NAME
        )
        output_parent_alias = (
            HERE / ".." / HERE.name
            / ".cm2_round202_alias_verification.json"
        )
        symlink_parent_alias = root / "deliverables-alias"
        symlink_parent_alias.symlink_to(HERE, target_is_directory=True)
        output_symlink_parent_alias = (
            symlink_parent_alias
            / ".cm2_round202_symlink_parent_verification.json"
        )
        cases: list[tuple[str, Callable[[], Any]]] = [
            ("input_symlink", lambda: read_regular(symlink)),
            ("input_hardlink", lambda: read_regular(hardlink)),
            ("input_directory", lambda: read_regular(directory)),
            ("input_FIFO", lambda: read_regular(fifo)),
            (
                "input_oversized",
                lambda: read_regular(oversized, maximum=1),
            ),
            (
                "certificate_parent_alias",
                lambda: validate_certificate_path(certificate_parent_alias),
            ),
            (
                "certificate_wrong_name",
                lambda: validate_certificate_path(regular),
            ),
            (
                "output_escape",
                lambda: validate_output_path(root / OUTPUT_NAME),
            ),
            (
                "output_parent_alias",
                lambda: validate_output_path(output_parent_alias),
            ),
            (
                "output_symlink_parent_alias",
                lambda: validate_output_path(output_symlink_parent_alias),
            ),
            (
                "output_producer",
                lambda: validate_output_path(PRODUCER),
            ),
            (
                "output_certificate",
                lambda: validate_output_path(CERTIFICATE),
            ),
            (
                "output_verifier",
                lambda: validate_output_path(Path(__file__)),
            ),
            (
                "output_Round185_alias",
                lambda: validate_output_path(HERE / R185_VERIFICATION),
            ),
            (
                "output_symlink",
                lambda: validate_output_path(output_symlink),
            ),
            (
                "output_hardlink",
                lambda: validate_output_path(output_hardlink),
            ),
            (
                "output_FIFO",
                lambda: validate_output_path(output_fifo),
            ),
            (
                "output_directory",
                lambda: validate_output_path(output_directory),
            ),
        ]
        try:
            for label, operation in cases:
                try:
                    operation()
                except (VerificationError, OSError):
                    rejected.append(label)
                else:
                    raise VerificationError(
                        f"filesystem/path attack accepted:{label}"
                    )
        finally:
            output_symlink.unlink(missing_ok=True)
            output_hardlink.unlink(missing_ok=True)
            output_fifo.unlink(missing_ok=True)
            output_directory.rmdir()
    return rejected


def safe_write(path: Path, data: bytes) -> None:
    absolute = validate_output_path(path)
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
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    certificate_path = validate_certificate_path(arguments.certificate)
    certificate_raw = read_regular(
        certificate_path,
        CERTIFICATE_FILE_SHA256,
    )
    certificate = strict_json(certificate_raw, CERTIFICATE_NAME)
    expected, reconstruction = independently_reconstruct()
    validate_candidate(certificate, expected)
    semantic_rejected = semantic_resigning_attacks(
        certificate,
        expected,
    )
    json_rejected = strict_json_attacks(certificate)
    path_rejected = filesystem_path_attacks()
    pin_round185_snapshot()
    read_regular(PRODUCER, PRODUCER_SHA256)
    require(producer_absent_from_modules(), "producer final module audit")

    verifier_sha256 = sha256_bytes(read_regular(Path(__file__)))
    result = {
        "status": "PASS",
        "certificate_file_sha256": sha256_bytes(certificate_raw),
        "certificate_result_sha256": certificate["result_sha256"],
        "independently_rebuilt_result_sha256": digest(expected),
        "full_expected_result_canonical_equality": True,
        "frozen_expected_result_digest_used_for_semantic_rejection": False,
        "certificate_file_pin_used_for_initial_identity": True,
        "producer_imported_or_executed": False,
        "producer_bytes_treated_as_inert": True,
        "producer_sha256": PRODUCER_SHA256,
        "Round185_evaluator_boundary": {
            "only_pinned_Round185_verifier_imported_as_evaluator": True,
            "Round185_six_files_and_manifest_pinned_before_import": True,
            "Round185_six_files_and_manifest_pinned_after_import": True,
            "Round185_six_files_and_manifest_pinned_after_evaluation": True,
            "Round185_manifest_sha256": R185_MANIFEST_SHA256,
            "Round185_verifier_sha256": R185_PINS[R185_VERIFIER],
            "Round185_files_modified": False,
        },
        "independent_reconstruction": reconstruction,
        "re_signed_semantic_attacks": {
            "rejected": len(semantic_rejected),
            "total": len(semantic_rejected),
            "labels": semantic_rejected,
            "all_result_digests_recomputed_after_mutation": True,
            "full_expected_equality_used_for_rejection": True,
        },
        "strict_JSON_encoding_attacks": {
            "rejected": len(json_rejected),
            "total": len(json_rejected),
            "labels": json_rejected,
        },
        "filesystem_path_output_attacks": {
            "rejected": len(path_rejected),
            "total": len(path_rejected),
            "labels": path_rejected,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "verifier_provenance": {
            "schema": VERIFICATION_SCHEMA,
            "verifier_sha256": verifier_sha256,
            "python_flint_version": flint.__version__,
            "effective_Arb_precision_bits": 384,
            "precision_source":
                "pinned Round185 verifier low-level interval-AD evaluator",
        },
    }
    require(
        result["certificate_result_sha256"]
        == result["independently_rebuilt_result_sha256"],
        "result digest agreement",
    )
    envelope = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    safe_write(arguments.output, canonical_bytes(envelope) + b"\n")
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
