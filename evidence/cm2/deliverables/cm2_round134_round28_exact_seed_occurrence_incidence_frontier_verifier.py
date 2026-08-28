#!/usr/bin/env python3
"""Independent verifier for the Round134 occurrence-incidence frontier.

The verifier never imports or executes the Round134 producer.  It rebuilds
the 64-record typed crosswalk from the pinned Round132 certificate, performs
a genuine 2048-bit Arb *whole-box* evaluation of all twelve source-G target
discriminants, and independently audits the Round122 4056-check empty ledger.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = HERE / "cm2_round134_round28_exact_seed_occurrence_incidence_frontier.py"
CERTIFICATE = (
    HERE
    / "cm2-round134-round28-exact-seed-occurrence-incidence-frontier-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round134-round28-exact-seed-occurrence-incidence-frontier-verification-2026-07-24.json"
)

CERTIFICATE_SCHEMA = (
    "cm2.round134.round28-exact-seed-occurrence-incidence-frontier.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round134.round28-exact-seed-occurrence-incidence-frontier-verification.v1"
)
PRODUCER_SHA256 = (
    "6bcac3d0b74f974fe0b07cd22aa8e407221ff4da94242ca28c746c31a97b7b1e"
)
CERTIFICATE_SHA256 = (
    "1d09f4371d72e2d63dc3398d82b45f515a29f8a3db33009e5c6212e53fcb7e6e"
)
CERTIFICATE_RESULT_SHA256 = (
    "263a5215ecbeae30cd858af2e3b18131a759103480ea58f000975b92d5ef2704"
)
PRECISION_BITS = 2048
MAX_JSON_BYTES = 64_000_000
MAX_CERTIFICATE_BYTES = 2_000_000

FIRST_HIT_P = "cm2_gate3_candidate_first_hit_cert.py"
R75P = "cm2_round75_r2_physical_curve_generator.py"
R75 = "cm2-round75-r2-physical-curves-2026-07-21.json"
R75QP = "cm2_round75_r2_physical_subquotient_cert.py"
R75Q = "cm2-round75-r2-physical-subquotient-manifest-2026-07-21.json"
R113P = "cm2_round113_rank3_endpoint_sheet_owner_ordering.py"
R113 = "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
R122P = "cm2_round122_rank3_exact_seed_physical_face_field_bridge.py"
R122 = "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
R132P = "cm2_round132_round28_occurrence_record_materialization.py"
R132 = "cm2-round132-round28-occurrence-record-materialization-2026-07-24.json"
R133P = "cm2_round133_round132_owner_map_realizability_audit.py"
R133 = "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json"

INPUT_NAMES = (
    FIRST_HIT_P,
    R75P,
    R75,
    R75QP,
    R75Q,
    R113P,
    R113,
    R122P,
    R122,
    R132P,
    R132,
    R133P,
    R133,
)
BYTE_PINS = {
    FIRST_HIT_P: "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    R75P: "60cbbd4e433c0c7aef15ce500af428e19041f281fcf235d55e7413b6f7b5b026",
    R75: "ef3005c3306e321966daf6cf10db04a9ea54b5f10b1de0cd7bb4194b8eaa85cb",
    R75QP: "22c39c5d693cb04a50a2a801a6b510a3ca2877f31c85b4c54376ad7c980a1191",
    R75Q: "460f32ffd650b14c5f9c4688b8cc01cfd08778751ee4d3dd73ca0d63151a0580",
    R113P: "249e30c6410bf77e2c81aec346461fd4c0d4d4c8448e74894f73f0b8ccd0bfd3",
    R113: "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    R122P: "44a64789635b8adfb597376d25afcbf8cb39dbaf0c2a19c4031bcbe78b3848f4",
    R122: "a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028",
    R132P: "88a12779148a49f111380c0560b0cb490a4e87f00d7ba7671878eec858f87d53",
    R132: "b5d09c7398dae4b77a6f011430286f88539e0f13ca449e50eb84fc3712d67d31",
    R133P: "3607bf2a3b2498c13d4bab27113dd151577e050cb83e68535ee32aaadbd79722",
    R133: "a020ce376c1398384e5f304aff320aa214721f5f8d8bcc1e35bfa31eadd54c91",
}
SCHEMA_PINS = {
    R75: "cm2.round75.r2-physical-curves.v1",
    R75Q: "cm2.round75.r2-physical-subquotient.v1",
    R113: "cm2.round113.rank3-endpoint-sheet-owner-ordering.v1",
    R122: "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1",
    R132: "cm2.round132.round28-occurrence-record-materialization.v1",
    R133: "cm2.round133.round132-owner-map-realizability-audit.v1",
}
RESULT_PINS = {
    R75: "94208887c3364995e5a781b8d57c60741fef33b14441343d6a3f71a459aa94b4",
    R75Q: "104c7935465ee53d749381628e00e0f85f079a6b284ea70095e4167bae833bca",
    R113: "33f564bd6afea1ba346ed0048a4bc61fa1a1bf91ebbbac546a32b051643bda67",
    R122: "e8bc4e02635b70dda7cee0485811ae68d42ee595c37a03a5b2aa94ecf170f6cb",
    R132: "3a5b4450d838ac39e0e7f596344589b520a8060bb0131bd88fb8f2c77af4d624",
    R133: "0e8e446fc81b1432dac31a9e7fc407b74bd6948dbd72451c67ffc43034f05ed2",
}

PARENT_CELL_ID = (
    "round113-cell:08b7ca8449af5f6e8d4e3abce98803656664ed7ec957aba62406763b68b2fea6"
)
EXACT_PARENT_ID = (
    "round121-exact-parent-W:41462c4f6815ad00fd5d4456e5c13885feeab5e8343b009b8872b72d15cf18c8"
)
TARGET_LIFTS_SHA256 = (
    "221eddd881ca4a82729a7842e0d89a8b71a1307d63ecb550f7545b931dabf769"
)
SIGNED_SHEETS_SHA256 = (
    "5ed98afe90cd8bd8504260edce1623efa1795a1075faff793bd15c08d600f6c5"
)
OCCURRENCE_MAP_SHA256 = (
    "91e5495bc44057296f883261027505786a79855b1042cdecd96a8408d9279f12"
)
ROUND122_AUDIT_SHA256 = (
    "840a2c470df61e399d2ff89daf3875610602daeb431f24b5c8a5c1300b0c81c3"
)
ROUND122_CHILD_ROWS_SHA256 = (
    "c340715887d737ffea966f99ab341474cef8248811397964e88646cb6c178522"
)


class VerificationError(RuntimeError):
    """Fail-closed file, JSON, reconstruction, or semantic error."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        require(key not in value, f"duplicate JSON key:{key}")
        value[key] = child
    return value


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON token:{token}")


def reject_float(token: str) -> None:
    raise VerificationError(f"floating-point JSON token:{token}")


def parse_integer(token: str) -> int:
    require(len(token.lstrip("-")) <= 1024, "oversized JSON integer")
    return int(token)


def validate_json_tree(value: Any) -> None:
    if value is None or isinstance(value, (bool, int)):
        return
    if isinstance(value, str):
        require(
            all(not 0xD800 <= ord(character) <= 0xDFFF for character in value),
            "unpaired JSON surrogate",
        )
        return
    if isinstance(value, list):
        for child in value:
            validate_json_tree(child)
        return
    require(isinstance(value, dict), "JSON tree type")
    for key, child in value.items():
        validate_json_tree(key)
        validate_json_tree(child)


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(len(raw) <= MAX_JSON_BYTES, f"oversized JSON:{label}")
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{label}")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
            parse_float=reject_float,
            parse_int=parse_integer,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise VerificationError(f"strict JSON:{label}") from exc
    require(isinstance(value, dict), f"top-level object:{label}")
    validate_json_tree(value)
    return value


def strict_json_path(path: Path) -> dict[str, Any]:
    return strict_json_bytes(path.read_bytes(), path.name)


def exact_dyadic(point: Any) -> Q:
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def arb_pair(value: arb) -> tuple[Q, Q]:
    return exact_dyadic(value.lower()), exact_dyadic(value.upper())


def aq(value: Q | int) -> arb:
    rational = Q(value)
    return arb(rational.numerator) / rational.denominator


def arb_interval(lower: Q, upper: Q) -> arb:
    require(lower <= upper, "ordered Arb interval")
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    # Build the midpoint plus an explicitly outward radius ball.  This
    # reproduces the pinned interval convention without importing its helper.
    return aq(middle) + arb(0, aq(radius).upper())


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def outward_decimal_enclosure(
    lower: Q,
    upper: Q,
    decimal_places: int = 12,
) -> tuple[Q, Q]:
    """Round an exact Arb endpoint pair outward to compact decimal rationals."""

    require(lower <= upper, "ordered enclosure endpoints")
    scale = 10 ** decimal_places
    lower_integer = (lower * scale).numerator // (lower * scale).denominator
    scaled_upper = upper * scale
    upper_integer = -(
        (-scaled_upper.numerator) // scaled_upper.denominator
    )
    return Q(lower_integer, scale), Q(upper_integer, scale)


def closed_row(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already closed")
    return {**row, "row_sha256": digest(row)}


def regular_single_link(path: Path, label: str) -> None:
    require(path.is_file(), f"missing file:{label}")
    require(not path.is_symlink(), f"symlink file:{label}")
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"regular file:{label}")
    require(metadata.st_nlink == 1, f"hardlinked file:{label}")


def load_inputs(check_files: bool = True) -> dict[str, dict[str, Any]]:
    documents: dict[str, dict[str, Any]] = {}
    for name in INPUT_NAMES:
        path = HERE / name
        if check_files:
            regular_single_link(path, name)
            require(path.resolve().parent == HERE, f"input parent:{name}")
            require(sha256_path(path) == BYTE_PINS[name], f"byte pin:{name}")
        if name.endswith(".json"):
            document = strict_json_path(path)
            require(document.get("schema") == SCHEMA_PINS[name], f"schema:{name}")
            result = document.get("result")
            require(isinstance(result, dict), f"result object:{name}")
            require(digest(result) == RESULT_PINS[name], f"result pin:{name}")
            if "result_sha256" in document:
                require(
                    document["result_sha256"] == RESULT_PINS[name],
                    f"stored result pin:{name}",
                )
            documents[name] = document
    return documents


def selected_cell(r113: dict[str, Any]) -> dict[str, Any]:
    matches = [
        cell
        for sheet in r113["sheet_rows"]
        for cell in sheet.get("certified_cells", [])
        if cell["cell_id"] == PARENT_CELL_ID
    ]
    require(len(matches) == 1, "unique selected Round113 cell")
    cell = matches[0]
    require(cell["source_chart"] == "W", "selected source chart")
    require(
        cell["parameter_box"]
        == {
            "b3": ["1/32768", "1/16384"],
            "c0": ["3/65536", "1/16384"],
        },
        "selected parameter box",
    )
    require(cell["official_path_regular_on_parameter_relative_interior_only"], "path scope")
    return cell


def typed_occurrence_crosswalk(
    r132: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[list[Any]], list[str]]:
    source_rows = r132["occurrence_face_record_rows"]
    require(isinstance(source_rows, list) and len(source_rows) == 64, "64 sources")
    require(
        r132["occurrence_face_record_rows_sha256"] == digest(source_rows),
        "Round132 source group digest",
    )
    mapping: list[dict[str, Any]] = []
    for row in source_rows:
        copy_row = dict(row)
        row_hash = copy_row.pop("row_sha256", None)
        require(row_hash == digest(copy_row), "Round132 source row closure")
        require(
            row["physical_carrier_type"]
            == "moving_first_event_grazing_occurrence_face",
            "Round132 moving carrier",
        )
        mapping.append(
            {
                "occurrence_record_id": row["occurrence_record_id"],
                "source": row["source"],
                "target": row["tangent_target"],
                "epsilon": row["epsilon"],
            }
        )
    require(digest(mapping) == OCCURRENCE_MAP_SHA256, "64-record typed map")
    source_g = [row for row in mapping if row["source"] == "G"]
    source_w = [row for row in mapping if row["source"] == "W"]
    require(len(source_g) == 44 and len(source_w) == 20, "44/20 source split")
    require({row["source"] for row in mapping} == {"G", "W"}, "source universe")
    signed = sorted({(row["target"], row["epsilon"]) for row in source_g})
    signed_rows = [[target, epsilon] for target, epsilon in signed]
    targets = sorted({target for target, _epsilon in signed})
    require(len(signed_rows) == 16 and len(targets) == 12, "16/12 sheet census")
    require(digest(signed_rows) == SIGNED_SHEETS_SHA256, "signed sheet digest")
    require(digest(targets) == TARGET_LIFTS_SHA256, "target lift digest")
    return mapping, signed_rows, targets


def parse_white_target(target: str) -> tuple[int, int]:
    require(target.startswith("W[") and target.endswith("]"), "white target")
    fields = target[2:-1].split(",")
    require(len(fields) == 2, "white target coordinate pair")
    try:
        ix, iy = int(fields[0]), int(fields[1])
    except ValueError as exc:
        raise VerificationError("white target integer coordinates") from exc
    require(target == f"W[{ix},{iy}]", "canonical white target")
    return ix, iy


def whole_box_delta(
    t_bounds: tuple[Q, Q],
    c_bounds: tuple[Q, Q],
    s_bounds: tuple[Q, Q],
    target: str,
) -> arb:
    """Evaluate Delta_T on the full product box, not only at its corners."""

    ix, iy = parse_white_target(target)
    t = arb_interval(*t_bounds)
    c0 = arb_interval(*c_bounds)
    system_s = arb_interval(*s_bounds)
    nx = -(arb(1) - t * t).sqrt()
    ny = t
    p = (arb(1) - c0 * c0).sqrt()
    ux = c0 * nx - p * ny
    uy = c0 * ny + p * nx
    qx = aq(Q(9, 25)) * nx
    qy = aq(Q(9, 25)) * ny
    dx = arb(ix) + aq(Q(1, 2)) + system_s - qx
    dy = arb(iy) + aq(Q(1, 2)) - qy
    transverse = -uy * dx + ux * dy
    return aq(Q(16, 625)) - transverse * transverse


def discriminant_rows(
    cell: dict[str, Any],
    signed_rows: list[list[Any]],
    targets: list[str],
) -> tuple[list[dict[str, Any]], dict[str, list[str]], Q]:
    ctx.prec = PRECISION_BITS
    t_bounds = tuple(Q(value) for value in cell["implicit_t_root_enclosure"])
    c_bounds = tuple(Q(value) for value in cell["parameter_box"]["c0"])
    s_bounds = (Q(-1, 400), Q(1, 400))
    require(len(t_bounds) == len(c_bounds) == 2, "two-sided parent bounds")
    signed_counts = {
        target: sum(sheet[0] == target for sheet in signed_rows)
        for target in targets
    }

    rows: list[dict[str, Any]] = []
    enclosures: dict[str, list[str]] = {}
    margins: list[Q] = []
    for target in targets:
        delta = whole_box_delta(t_bounds, c_bounds, s_bounds, target)
        lower, upper = arb_pair(delta)
        require(lower > 0 or upper < 0, f"whole-box zero exclusion:{target}")
        sign = 1 if lower > 0 else -1
        margin = lower if sign == 1 else -upper
        require(margin > Q(1, 100), f"uniform whole-box gap:{target}")
        margins.append(margin)
        outward_lower, outward_upper = outward_decimal_enclosure(lower, upper)
        require(
            outward_lower <= lower <= upper <= outward_upper,
            f"outward whole-box enclosure:{target}",
        )
        enclosures[target] = [qstr(lower), qstr(upper)]

        corner_values = [
            whole_box_delta((t, t), (c0, c0), (system_s, system_s), target)
            for t in t_bounds
            for c0 in c_bounds
            for system_s in s_bounds
        ]
        corner_lower = min(arb_pair(value)[0] for value in corner_values)
        corner_upper = max(arb_pair(value)[1] for value in corner_values)
        require(
            corner_lower > 0 or corner_upper < 0,
            f"auxiliary corner zero exclusion:{target}",
        )
        corner_sign = 1 if corner_lower > 0 else -1
        require(corner_sign == sign, f"corner/whole-box sign agreement:{target}")
        rows.append(
            closed_row(
                {
                    "target_lift": target,
                    "Round28_signed_sheet_count": signed_counts[target],
                    "whole_rectangle_interval_check": True,
                    "whole_rectangle_discriminant_enclosure": [
                        qstr(outward_lower),
                        qstr(outward_upper),
                    ],
                    "whole_rectangle_interval_sign": sign,
                    "whole_rectangle_status":
                        "STRICT_POSITIVE_TWO_LINE_INTERSECTIONS"
                        if sign == 1
                        else "STRICT_NEGATIVE_WHOLE_LINE_MISS",
                    "zero_tangency_root_count": 0,
                    "corner_auxiliary_evaluation_count": len(corner_values),
                    "corner_auxiliary_sign": corner_sign,
                    "corner_auxiliary_sign_agrees": True,
                }
            )
        )
    require(len(rows) == 12, "twelve discriminant rows")
    positive = [
        row["target_lift"]
        for row in rows
        if row["whole_rectangle_interval_sign"] == 1
    ]
    require(positive == ["W[-1,-1]", "W[-1,-2]"], "positive target identities")
    require(
        sum(row["whole_rectangle_interval_sign"] == -1 for row in rows) == 10,
        "ten misses",
    )
    require(sum(row["Round28_signed_sheet_count"] for row in rows) == 16, "16 sheets")
    return rows, enclosures, min(margins)


def validate_round122(r122: dict[str, Any]) -> dict[str, Any]:
    empty = r122["physical_face_typed_empty_audit"]
    ledger = r122["count_ledger"]
    require(
        r122["round121_contract"]["exact_parent_W_seed_id"] == EXACT_PARENT_ID,
        "Round122 exact parent",
    )
    physical_digest = digest(
        {
            "core": empty["core_clearance_rows_sha256"],
            "child_stage": empty["child_stage_boundary_rows_sha256"],
            "five": digest(r122["physical_five_face_grammar_rows"]),
            "seven": digest(r122["physical_seven_boundary_kind_rows"]),
        }
    )
    require(
        r122["physical_face_typed_empty_audit_sha256"]
        == physical_digest
        == ROUND122_AUDIT_SHA256,
        "Round122 physical audit closure",
    )
    child_rows = empty["child_stage_boundary_rows"]
    require(len(child_rows) == 72, "Round122 72 child-stage rows")
    require(
        empty["child_stage_boundary_rows_sha256"]
        == digest(child_rows)
        == ROUND122_CHILD_ROWS_SHA256,
        "Round122 child-stage digest",
    )
    total_candidates = 0
    for row in child_rows:
        copy_row = dict(row)
        row_hash = copy_row.pop("row_sha256", None)
        require(row_hash == digest(copy_row), "Round122 child row closure")
        require(row["physical_boundary_incidence_count"] == 0, "empty child row")
        total_candidates += row["candidate_check_count"]
    for common_rank in range(24):
        rank_rows = sorted(
            (row for row in child_rows if row["common_rank"] == common_rank),
            key=lambda row: row["stage"],
        )
        require(len(rank_rows) == 3, "three stages per child")
        require(
            [row["candidate_check_count"] for row in rank_rows] == [57, 55, 57],
            "57/55/57 candidate census",
        )
    require(total_candidates == 4056, "independent 4056 sum")
    require(
        empty["rank3_candidate_occurrence_stage_counts"] == [57, 55, 57]
        and empty["rank3_candidate_occurrence_count_per_common_child"] == 169
        and empty["rank3_candidate_occurrence_total_check_count"] == 4056,
        "Round122 stored candidate census",
    )
    require(
        ledger["common_refinement_actual_child_count"] == 24
        and ledger["child_stage_physical_audit_row_count"] == 72
        and ledger["physical_face_instance_count"] == 0
        and empty["residual_physical_face_count"] == 0,
        "Round122 empty ledger",
    )
    moving = [
        row
        for row in r122["physical_five_face_grammar_rows"]
        if row["kind"] == "moving_occurrence_face"
    ]
    require(len(moving) == 1, "one moving occurrence grammar")
    require(
        moving[0]["actual_instance_count"] == 0
        and moving[0]["rank3_candidate_occurrence_total_check_count"] == 4056,
        "Round122 moving grammar empty",
    )
    stage_zero_margins = [
        Q(row["typed_boundary_actual_interval_lower_minima"]["candidate_tangency"])
        for row in child_rows
        if row["stage"] == 0
    ]
    require(len(stage_zero_margins) == 24, "24 stage-zero margins")
    require(min(stage_zero_margins) > Q(1, 1000), "stage-zero gap above 1/1000")
    return {
        "total_candidates": total_candidates,
        "stage_zero_minimum": qstr(min(stage_zero_margins)),
    }


def validate_round75(r75: dict[str, Any], r75q: dict[str, Any]) -> None:
    require(
        r75["physical_R2_component_count"] == 16
        and r75["physical_R2_curve_count"] == 32,
        "Round75 census",
    )
    curves = r75["curve_rows"]
    require(len(curves) == 32, "Round75 curve rows")
    require(r75["curve_rows_sha256"] == digest(curves), "Round75 curve digest")
    require(
        all(
            row["active_side"] in {"t_lower", "t_upper", "p_lower", "p_upper"}
            and row["source_stationary_sides"]
            for row in curves
        ),
        "Round75 stationary side levels",
    )
    require(
        r75q["scope"].startswith("actual fixed s=0 depth-two physical subquotient"),
        "Round75 fixed-s scope",
    )
    require(
        r75q["physical_R2_curve_atlas"]["physical_curves"] == 32,
        "Round75 subquotient count",
    )


def build_expected(
    check_files: bool = True,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if check_files:
        regular_single_link(PRODUCER, PRODUCER.name)
        require(sha256_path(PRODUCER) == PRODUCER_SHA256, "producer pin")
    documents = load_inputs(check_files)
    r75 = documents[R75]["result"]
    r75q = documents[R75Q]["result"]
    r113 = documents[R113]["result"]
    r122 = documents[R122]["result"]
    r132 = documents[R132]["result"]
    r133 = documents[R133]["result"]
    validate_round75(r75, r75q)
    cell = selected_cell(r113)
    mapping, signed_rows, targets = typed_occurrence_crosswalk(r132)
    delta_rows, enclosures, whole_box_minimum = discriminant_rows(
        cell, signed_rows, targets
    )
    round122_replay = validate_round122(r122)
    require(
        r133["count_ledger"][
            "certified_or_materialized_Round67_owned_Omega_j_record_count"
        ]
        == 0
        and r133["count_ledger"]["owner_key_count"] == 0
        and r133["count_ledger"]["q_j_recordwise_output_count"] == 0,
        "Round133 owner frontier",
    )
    empty = r122["physical_face_typed_empty_audit"]
    ledger = r122["count_ledger"]

    result = {
        "provenance": {
            "producer_sha256_filled_after_write": True,
            "dependency_sha256": dict(BYTE_PINS),
            "old_artifacts_modified": False,
            "precision_bits": PRECISION_BITS,
        },
        "Round132_to_Round113_typed_crosswalk": {
            "Round132_occurrence_record_count": len(mapping),
            "Round132_occurrence_record_source_target_epsilon_map_sha256":
                OCCURRENCE_MAP_SHA256,
            "source_G_compatible_record_count": 44,
            "source_W_type_mismatch_record_count": 20,
            "source_G_unique_signed_target_sheet_count": len(signed_rows),
            "source_G_unique_signed_target_sheets": signed_rows,
            "source_G_unique_signed_target_sheets_sha256": SIGNED_SHEETS_SHA256,
            "source_G_unique_target_lift_count": len(targets),
            "source_G_unique_target_lifts": targets,
            "source_G_unique_target_lifts_sha256": TARGET_LIFTS_SHA256,
            "Round122_itself_typed_joined_Round28_occurrence_IDs": False,
            "Round134_installs_the_missing_Round28_ID_to_exact_seed_target_crosswalk":
                True,
        },
        "whole_Round113_rectangle_discriminant_audit": {
            "parent_round113_cell_id": PARENT_CELL_ID,
            "exact_parent_W_seed_id": EXACT_PARENT_ID,
            "source_type": "G",
            "source_normal_chart": "W",
            "parameter_box": cell["parameter_box"],
            "implicit_t_root_enclosure": cell["implicit_t_root_enclosure"],
            "system_parameter_interval": ["-1/400", "1/400"],
            "precision_bits": PRECISION_BITS,
            "target_lift_row_count": len(delta_rows),
            "target_lift_rows": delta_rows,
            "target_lift_rows_sha256": digest(delta_rows),
            "strict_positive_discriminant_target_count": 2,
            "strict_negative_discriminant_target_count": 10,
            "zero_discriminant_target_count": 0,
            "uniform_absolute_discriminant_strict_lower": "1/100",
            "tightest_target_lift": "W[-1,0]",
            "tightest_outward_discriminant_enclosure":
                ["-374189179/25000000000", "-101296291/7812500000"],
            "interpretation":
                "positive means two transverse line intersections and negative means whole-line miss; neither is a tangency root",
            "exact_seed_Round28_moving_occurrence_root_count": 0,
            "status": "CERTIFIED_EMPTY",
        },
        "Round122_crosscheck": {
            "strict_scope": r122["strict_scope"],
            "common_child_count": ledger["common_refinement_actual_child_count"],
            "child_stage_physical_audit_row_count":
                ledger["child_stage_physical_audit_row_count"],
            "candidate_occurrence_stage_counts":
                empty["rank3_candidate_occurrence_stage_counts"],
            "candidate_occurrence_count_per_common_child":
                empty["rank3_candidate_occurrence_count_per_common_child"],
            "candidate_occurrence_total_check_count":
                empty["rank3_candidate_occurrence_total_check_count"],
            "seven_physical_boundary_kinds_all_checked":
                ledger["physical_seven_boundary_kind_count"] == 7,
            "physical_face_instance_count": ledger["physical_face_instance_count"],
            "residual_physical_face_count": empty["residual_physical_face_count"],
            "physical_face_empty_audit_sha256":
                r122["physical_face_typed_empty_audit_sha256"],
            "status": "CERTIFIED_EMPTY",
        },
        "Round75_type_check": {
            "physical_R2_component_count": r75["physical_R2_component_count"],
            "physical_R2_curve_count": r75["physical_R2_curve_count"],
            "actual_carrier_type":
                "stationary destination-core t/p boundary preimage crosscuts",
            "requested_carrier_type":
                "moving occurrence pullback family at an active transverse tangency root",
            "carrier_types_match": False,
            "stationary_terminal_preimage_may_replace_occurrence_pullback": False,
            "status": "REJECTED_TYPE_MISMATCH",
        },
        "feasibility_frontier": {
            "Round121_exact_seed_Round28_occurrence_incidence":
                "CERTIFIED_EMPTY",
            "Round75_as_Round28_occurrence_parent":
                "REJECTED_TYPE_MISMATCH",
            "actual_nonempty_n_ge_2_occurrence_pullback_elsewhere":
                "UNKNOWN_NOT_CERTIFIED",
            "first_unpaid_construction_elsewhere":
                "materialize a genuine fixed-s n>=2 parent-W/path component crossing one Round28 moving-occurrence graph, then enumerate the complete primitive-free active fibre",
            "tailored_analytic_leaf_through_a_face_witness_is_by_itself_a_component":
                False,
            "parameter-s hit/miss germ_may_replace_fixed-s_plaque-side_path_proof":
                False,
            "stationary_terminal_preimage_curve_may_replace_occurrence_pullback":
                False,
        },
        "materialization_ledger": {
            "new_nonempty_occurrence_pullback_return_component_count": 0,
            "new_rank_zero_occurrence_component_count": 0,
            "new_complete_active_primitive_fibre_count": 0,
            "new_owner_key_count": 0,
            "new_q_j_recordwise_output_count": 0,
            "new_Round67_owned_Omega_j_record_count": 0,
            "new_global_complete_18_field_block_count": 0,
        },
        "global_safety": {
            "gate5_global_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "the exact-seed empty result is not a global absence theorem",
            "actual n>=2 occurrence incidence elsewhere is UNKNOWN_NOT_CERTIFIED, not empty",
            "the 32 Round75 stationary terminal-preimage curves are not occurrence pullbacks",
            "a positive line discriminant is not a tangency root",
            "no Round67 owner key, q_j output, positive owner law or Gate5 field is promoted",
        ],
    }
    replay = {
        "whole_box_enclosures": enclosures,
        "whole_box_uniform_margin_exact": qstr(whole_box_minimum),
        "whole_box_uniform_margin_above_one_hundredth": True,
        "Round122_stage_zero_minimum_exact":
            round122_replay["stage_zero_minimum"],
        "Round122_stage_zero_minimum_above_one_thousandth": True,
    }
    return result, replay


def validate_result_closures(result: dict[str, Any]) -> None:
    audit = result["whole_Round113_rectangle_discriminant_audit"]
    rows = audit["target_lift_rows"]
    require(isinstance(rows, list) and len(rows) == 12, "12 target rows")
    require(audit["target_lift_rows_sha256"] == digest(rows), "target group digest")
    for row in rows:
        copy_row = dict(row)
        row_hash = copy_row.pop("row_sha256", None)
        require(row_hash == digest(copy_row), "target row closure")
    require(
        audit["strict_positive_discriminant_target_count"] == 2
        and audit["strict_negative_discriminant_target_count"] == 10
        and audit["zero_discriminant_target_count"] == 0
        and audit["exact_seed_Round28_moving_occurrence_root_count"] == 0,
        "empty discriminant ledger",
    )
    crosswalk = result["Round132_to_Round113_typed_crosswalk"]
    require(
        crosswalk["Round132_occurrence_record_count"] == 64
        and crosswalk["source_G_compatible_record_count"] == 44
        and crosswalk["source_W_type_mismatch_record_count"] == 20
        and crosswalk["source_G_unique_signed_target_sheet_count"] == 16
        and crosswalk["source_G_unique_target_lift_count"] == 12,
        "crosswalk census",
    )
    require(
        all(value == 0 for value in result["materialization_ledger"].values()),
        "zero materialization ledger",
    )


def evaluate_document(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(isinstance(result, dict), "certificate result object")
    require(document["result_sha256"] == digest(result), "outer result digest")
    validate_result_closures(result)
    require(result == expected, "independent expected result equality")
    require(
        document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
        "frozen result digest",
    )


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def reclose_target_row(result: dict[str, Any], index: int) -> None:
    audit = result["whole_Round113_rectangle_discriminant_audit"]
    row = audit["target_lift_rows"][index]
    row.pop("row_sha256", None)
    row["row_sha256"] = digest(row)
    audit["target_lift_rows_sha256"] = digest(audit["target_lift_rows"])


def semantic_mutations(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def simple(path: tuple[Any, ...], value: Any) -> Callable[[dict[str, Any]], None]:
        def mutate(document: dict[str, Any]) -> None:
            target: Any = document
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            resign(document)
        return mutate

    def mutate_target(
        index: int,
        operation: Callable[[dict[str, Any]], None],
    ) -> Callable[[dict[str, Any]], None]:
        def mutate(document: dict[str, Any]) -> None:
            result = document["result"]
            operation(
                result["whole_Round113_rectangle_discriminant_audit"][
                    "target_lift_rows"
                ][index]
            )
            reclose_target_row(result, index)
            resign(document)
        return mutate

    mutations.extend(
        [
            (
                "certificate schema altered",
                lambda d: (d.__setitem__("schema", "bad"), resign(d)),
            ),
            (
                "producer provenance altered",
                simple(
                    ("result", "provenance", "producer_sha256_filled_after_write"),
                    False,
                ),
            ),
            (
                "precision altered",
                simple(("result", "provenance", "precision_bits"), 1024),
            ),
            (
                "Round132 pin altered",
                simple(("result", "provenance", "dependency_sha256", R132), "0" * 64),
            ),
            (
                "first-hit interval helper pin altered",
                simple(
                    ("result", "provenance", "dependency_sha256", FIRST_HIT_P),
                    "0" * 64,
                ),
            ),
            (
                "old artifacts modified",
                simple(("result", "provenance", "old_artifacts_modified"), True),
            ),
            (
                "occurrence count reduced",
                simple(
                    (
                        "result",
                        "Round132_to_Round113_typed_crosswalk",
                        "Round132_occurrence_record_count",
                    ),
                    63,
                ),
            ),
            (
                "source G count altered",
                simple(
                    (
                        "result",
                        "Round132_to_Round113_typed_crosswalk",
                        "source_G_compatible_record_count",
                    ),
                    43,
                ),
            ),
            (
                "source W mismatch erased",
                simple(
                    (
                        "result",
                        "Round132_to_Round113_typed_crosswalk",
                        "source_W_type_mismatch_record_count",
                    ),
                    0,
                ),
            ),
            (
                "signed sheet count altered",
                simple(
                    (
                        "result",
                        "Round132_to_Round113_typed_crosswalk",
                        "source_G_unique_signed_target_sheet_count",
                    ),
                    15,
                ),
            ),
            (
                "target count altered",
                simple(
                    (
                        "result",
                        "Round132_to_Round113_typed_crosswalk",
                        "source_G_unique_target_lift_count",
                    ),
                    11,
                ),
            ),
            (
                "signed sheet digest altered",
                simple(
                    (
                        "result",
                        "Round132_to_Round113_typed_crosswalk",
                        "source_G_unique_signed_target_sheets_sha256",
                    ),
                    "0" * 64,
                ),
            ),
            (
                "target digest altered",
                simple(
                    (
                        "result",
                        "Round132_to_Round113_typed_crosswalk",
                        "source_G_unique_target_lifts_sha256",
                    ),
                    "0" * 64,
                ),
            ),
            (
                "Round122 falsely claimed to have typed ID join",
                simple(
                    (
                        "result",
                        "Round132_to_Round113_typed_crosswalk",
                        "Round122_itself_typed_joined_Round28_occurrence_IDs",
                    ),
                    True,
                ),
            ),
            (
                "Round134 crosswalk disabled",
                simple(
                    (
                        "result",
                        "Round132_to_Round113_typed_crosswalk",
                        "Round134_installs_the_missing_Round28_ID_to_exact_seed_target_crosswalk",
                    ),
                    False,
                ),
            ),
            (
                "parent cell altered",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "parent_round113_cell_id",
                    ),
                    "round113-cell:" + "0" * 64,
                ),
            ),
            (
                "system parameter interval narrowed",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "system_parameter_interval",
                    ),
                    ["0", "0"],
                ),
            ),
            (
                "target row count altered",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "target_lift_row_count",
                    ),
                    11,
                ),
            ),
            (
                "positive count altered",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "strict_positive_discriminant_target_count",
                    ),
                    1,
                ),
            ),
            (
                "negative count altered",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "strict_negative_discriminant_target_count",
                    ),
                    9,
                ),
            ),
            (
                "zero discriminant count promoted",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "zero_discriminant_target_count",
                    ),
                    1,
                ),
            ),
            (
                "uniform gap weakened",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "uniform_absolute_discriminant_strict_lower",
                    ),
                    "0",
                ),
            ),
            (
                "tightest target altered",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "tightest_target_lift",
                    ),
                    "W[-1,-1]",
                ),
            ),
            (
                "tightest enclosure crosses zero",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "tightest_outward_discriminant_enclosure",
                    ),
                    ["-1/100", "1/100"],
                ),
            ),
            (
                "exact-seed root invented",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "exact_seed_Round28_moving_occurrence_root_count",
                    ),
                    1,
                ),
            ),
            (
                "empty status promoted to intersection",
                simple(
                    (
                        "result",
                        "whole_Round113_rectangle_discriminant_audit",
                        "status",
                    ),
                    "CERTIFIED_NONEMPTY",
                ),
            ),
            (
                "Round122 child count altered",
                simple(("result", "Round122_crosscheck", "common_child_count"), 23),
            ),
            (
                "Round122 child-stage count altered",
                simple(
                    ("result", "Round122_crosscheck", "child_stage_physical_audit_row_count"),
                    71,
                ),
            ),
            (
                "Round122 stage census altered",
                simple(
                    ("result", "Round122_crosscheck", "candidate_occurrence_stage_counts"),
                    [57, 55, 56],
                ),
            ),
            (
                "Round122 total altered",
                simple(
                    ("result", "Round122_crosscheck", "candidate_occurrence_total_check_count"),
                    4055,
                ),
            ),
            (
                "Round122 physical face invented",
                simple(("result", "Round122_crosscheck", "physical_face_instance_count"), 1),
            ),
            (
                "Round122 residual invented",
                simple(("result", "Round122_crosscheck", "residual_physical_face_count"), 1),
            ),
            (
                "Round122 audit digest altered",
                simple(
                    ("result", "Round122_crosscheck", "physical_face_empty_audit_sha256"),
                    "0" * 64,
                ),
            ),
            (
                "Round75 carrier types conflated",
                simple(("result", "Round75_type_check", "carrier_types_match"), True),
            ),
            (
                "Round75 substitution allowed",
                simple(
                    (
                        "result",
                        "Round75_type_check",
                        "stationary_terminal_preimage_may_replace_occurrence_pullback",
                    ),
                    True,
                ),
            ),
            (
                "Round75 status promoted",
                simple(("result", "Round75_type_check", "status"), "CERTIFIED_MATCH"),
            ),
            (
                "elsewhere unknown changed to empty",
                simple(
                    (
                        "result",
                        "feasibility_frontier",
                        "actual_nonempty_n_ge_2_occurrence_pullback_elsewhere",
                    ),
                    "CERTIFIED_EMPTY",
                ),
            ),
            (
                "tailored leaf promoted to component",
                simple(
                    (
                        "result",
                        "feasibility_frontier",
                        "tailored_analytic_leaf_through_a_face_witness_is_by_itself_a_component",
                    ),
                    True,
                ),
            ),
            (
                "parameter germ promoted to plaque proof",
                simple(
                    (
                        "result",
                        "feasibility_frontier",
                        "parameter-s hit/miss germ_may_replace_fixed-s_plaque-side_path_proof",
                    ),
                    True,
                ),
            ),
            (
                "stationary curve promoted to occurrence pullback",
                simple(
                    (
                        "result",
                        "feasibility_frontier",
                        "stationary_terminal_preimage_curve_may_replace_occurrence_pullback",
                    ),
                    True,
                ),
            ),
            (
                "Gate5 maturity promoted",
                simple(("result", "global_safety", "gate5_global_maturity"), "18/18"),
            ),
            (
                "global complete block invented",
                simple(
                    ("result", "global_safety", "global_complete_18_field_block_count"),
                    1,
                ),
            ),
            (
                "Gate5 promoted",
                simple(("result", "global_safety", "Gate5"), "CERTIFIED"),
            ),
            (
                "CM2 promoted",
                simple(("result", "global_safety", "CM2"), "GO_FOR_CLAIM"),
            ),
            (
                "strict nonclaim deleted",
                lambda d: (d["result"]["strict_nonclaims"].pop(), resign(d)),
            ),
            (
                "unknown result key added",
                lambda d: (d["result"].__setitem__("unknown", True), resign(d)),
            ),
        ]
    )

    for field in expected["materialization_ledger"]:
        mutations.append(
            (
                f"materialization promoted:{field}",
                simple(("result", "materialization_ledger", field), 1),
            )
        )
    for index, row in enumerate(
        expected["whole_Round113_rectangle_discriminant_audit"]["target_lift_rows"]
    ):
        mutations.append(
            (
                f"target {row['target_lift']} root invented",
                mutate_target(
                    index,
                    lambda target_row: target_row.__setitem__(
                        "zero_tangency_root_count", 1
                    ),
                ),
            )
        )
    mutations.extend(
        [
            (
                "whole-box interval check disabled",
                mutate_target(
                    2,
                    lambda row: row.__setitem__(
                        "whole_rectangle_interval_check", False
                    ),
                ),
            ),
            (
                "whole-box outward enclosure crosses zero",
                mutate_target(
                    2,
                    lambda row: row.__setitem__(
                        "whole_rectangle_discriminant_enclosure",
                        ["-1/100", "1/100"],
                    ),
                ),
            ),
            (
                "whole-box interval sign flipped",
                mutate_target(
                    2,
                    lambda row: row.__setitem__(
                        "whole_rectangle_interval_sign", 1
                    ),
                ),
            ),
            (
                "corner auxiliary agreement disabled",
                mutate_target(
                    2,
                    lambda row: row.__setitem__(
                        "corner_auxiliary_sign_agrees", False
                    ),
                ),
            ),
        ]
    )

    rejected: list[str] = []
    for label, mutation in mutations:
        candidate = copy.deepcopy(certificate)
        mutation(candidate)
        try:
            evaluate_document(candidate, expected)
        except (
            VerificationError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            rejected.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    require(len(rejected) == len(mutations), "all semantic mutations rejected")
    return rejected


def strict_json_attacks(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    canonical_raw = (
        json.dumps(
            certificate,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")

    def doc_raw(document: dict[str, Any]) -> bytes:
        return (
            json.dumps(
                document,
                sort_keys=True,
                indent=2,
                ensure_ascii=False,
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")

    attacks: list[tuple[str, bytes]] = []
    attacks.append(
        (
            "duplicate top-level schema key",
            canonical_raw.replace(
                b'  "schema": ',
                b'  "schema": "duplicate",\\n  "schema": ',
                1,
            ),
        )
    )
    attacks.append(
        (
            "duplicate nested status key",
            canonical_raw.replace(
                b'      "status": ',
                b'      "status": "duplicate",\\n      "status": ',
                1,
            ),
        )
    )
    attacks.append(
        (
            "floating-point count",
            canonical_raw.replace(
                b'"Round132_occurrence_record_count": 64',
                b'"Round132_occurrence_record_count": 64.0',
                1,
            ),
        )
    )
    attacks.append(
        (
            "NaN constant",
            canonical_raw.replace(
                b'"Round132_occurrence_record_count": 64',
                b'"Round132_occurrence_record_count": NaN',
                1,
            ),
        )
    )
    attacks.append(
        (
            "positive Infinity",
            canonical_raw.replace(
                b'"Round132_occurrence_record_count": 64',
                b'"Round132_occurrence_record_count": Infinity',
                1,
            ),
        )
    )
    attacks.append(
        (
            "negative Infinity",
            canonical_raw.replace(
                b'"Round132_occurrence_record_count": 64',
                b'"Round132_occurrence_record_count": -Infinity',
                1,
            ),
        )
    )
    attacks.append(("UTF-8 BOM", b"\xef\xbb\xbf" + canonical_raw))
    attacks.append(("invalid UTF-8", canonical_raw[:-2] + b"\xff\n"))
    attacks.append(("top-level array", b"[]\n"))
    attacks.append(("top-level null", b"null\n"))
    attacks.append(("trailing second document", canonical_raw + b"{}\n"))
    attacks.append(
        (
            "oversized integer",
            canonical_raw.replace(
                b'"Round132_occurrence_record_count": 64',
                b'"Round132_occurrence_record_count": ' + b"9" * 1025,
                1,
            ),
        )
    )
    attacks.append(
        (
            "negative zero",
            canonical_raw.replace(
                b'"Round132_occurrence_record_count": 64',
                b'"Round132_occurrence_record_count": -0',
                1,
            ),
        )
    )
    attacks.append(
        (
            "leading-zero integer",
            canonical_raw.replace(
                b'"Round132_occurrence_record_count": 64',
                b'"Round132_occurrence_record_count": 064',
                1,
            ),
        )
    )
    attacks.append(
        (
            "unpaired surrogate",
            canonical_raw.replace(
                b'"CERTIFIED_EMPTY"',
                b'"\\ud800"',
                1,
            ),
        )
    )
    envelope_extra = copy.deepcopy(certificate)
    envelope_extra["unknown"] = True
    attacks.append(("closed envelope extra key", doc_raw(envelope_extra)))
    result_extra = copy.deepcopy(certificate)
    result_extra["result"]["unknown"] = True
    resign(result_extra)
    attacks.append(("closed result extra key", doc_raw(result_extra)))
    stale = copy.deepcopy(certificate)
    stale["result"]["global_safety"]["CM2"] = "GO_FOR_CLAIM"
    attacks.append(("stale outer result digest", doc_raw(stale)))

    rejected: list[str] = []
    for label, raw in attacks:
        try:
            document = strict_json_bytes(raw, label)
            evaluate_document(document, expected)
        except (
            VerificationError,
            UnicodeError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    require(len(rejected) == len(attacks) == 18, "18 strict attacks rejected")
    return rejected


def build_verification(
    replay: dict[str, Any],
    mutations: list[str],
    strict_attacks: list[str],
) -> dict[str, Any]:
    return {
        "status": "PASS",
        "verifier_sha256": sha256_path(VERIFIER),
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "independence_contract": {
            "Round134_producer_imported": False,
            "Round134_producer_executed": False,
            "Round132_64_record_crosswalk_independently_rebuilt": True,
            "all_12_target_discriminants_evaluated_on_full_Arb_product_box": True,
            "corner_auxiliary_values_not_used_as_whole_box_proof": True,
            "Round122_72_rows_and_4056_checks_independently_recounted": True,
        },
        "replay_audit": {
            "Round132_occurrence_record_count": 64,
            "source_G_compatible_record_count": 44,
            "source_W_type_mismatch_record_count": 20,
            "source_G_signed_sheet_count": 16,
            "source_G_target_lift_count": 12,
            "strict_positive_discriminant_target_count": 2,
            "strict_negative_discriminant_target_count": 10,
            "zero_discriminant_target_count": 0,
            "whole_box_enclosures": replay["whole_box_enclosures"],
            "whole_box_uniform_margin_exact":
                replay["whole_box_uniform_margin_exact"],
            "whole_box_uniform_margin_above_one_hundredth": True,
            "Round122_common_child_count": 24,
            "Round122_child_stage_row_count": 72,
            "Round122_candidate_check_count": 4056,
            "Round122_stage_zero_minimum_exact":
                replay["Round122_stage_zero_minimum_exact"],
            "Round122_stage_zero_minimum_above_one_thousandth": True,
            "Round122_physical_face_instance_count": 0,
            "Round122_residual_physical_face_count": 0,
            "Round75_stationary_curve_substitution_rejected": True,
            "new_Round67_owned_record_count": 0,
        },
        "semantic_mutation_test_count": len(mutations),
        "semantic_mutation_rejection_labels": mutations,
        "strict_json_attack_count": len(strict_attacks),
        "strict_json_attack_rejection_labels": strict_attacks,
        "determinism_contract": {
            "canonical_JSON_sort_keys": True,
            "no_hash_iteration_controls_output": True,
            "verification_replay_is_PYTHONHASHSEED_independent": True,
        },
        "path_safety_contract": {
            "input_must_be_regular_single_link_non_symlink": True,
            "output_must_be_regular_single_link_or_absent": True,
            "input_output_alias_rejected": True,
            "producer_verifier_certificate_and_upstreams_protected": True,
            "atomic_replace_after_fsync": True,
        },
        "safety": {
            "actual_nonempty_n_ge_2_occurrence_pullback_elsewhere":
                "UNKNOWN_NOT_CERTIFIED",
            "Round67_owned_record_count": 0,
            "global_complete_18_field_block_count": 0,
            "gate5_global_maturity": "10/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def safe_input_path(path: Path) -> Path:
    expanded = path.expanduser()
    regular_single_link(expanded, "certificate")
    require(expanded.stat().st_size <= MAX_CERTIFICATE_BYTES, "certificate size")
    resolved = expanded.resolve()
    require(sha256_path(resolved) == CERTIFICATE_SHA256, "certificate byte pin")
    return resolved


def safe_output_path(path: Path, certificate_path: Path) -> Path:
    expanded = path.expanduser()
    protected = {
        PRODUCER.resolve(),
        VERIFIER.resolve(),
        CERTIFICATE.resolve(),
        certificate_path.resolve(),
        *((HERE / name).resolve() for name in INPUT_NAMES),
    }
    require(not expanded.is_symlink(), "output symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(stat.S_ISREG(metadata.st_mode), "existing output regular")
        require(metadata.st_nlink == 1, "existing output single link")
        for item in protected:
            try:
                require(not os.path.samefile(expanded, item), "output aliases protected")
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(resolved not in protected, "output overwrites protected")
    require(resolved.parent.is_dir(), "output parent directory")
    require(not resolved.parent.is_symlink(), "output parent symlink")
    return resolved


def write_document(path: Path, document: dict[str, Any]) -> None:
    payload = (
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        certificate_path = safe_input_path(args.certificate)
        certificate = strict_json_path(certificate_path)
        expected, replay = build_expected()
        evaluate_document(certificate, expected)
        mutations = semantic_mutations(certificate, expected)
        strict_attacks = strict_json_attacks(certificate, expected)
        result = build_verification(replay, mutations, strict_attacks)
        document = {
            "schema": VERIFICATION_SCHEMA,
            "result": result,
            "result_sha256": digest(result),
        }
        output = safe_output_path(args.output, certificate_path)
        write_document(output, document)
        print(
            canonical(
                {
                    "output": str(output),
                    "result_sha256": document["result_sha256"],
                    "semantic_mutations": len(mutations),
                    "strict_json_attacks": len(strict_attacks),
                    "status": "PASS",
                }
            )
        )
        return 0
    except (
        OSError,
        UnicodeError,
        VerificationError,
        ValueError,
    ) as exc:
        print(f"{type(exc).__name__}: {exc}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
