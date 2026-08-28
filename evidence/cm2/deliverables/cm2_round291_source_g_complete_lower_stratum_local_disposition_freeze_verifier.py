#!/usr/bin/env python3
"""Cacheless independent verifier for the Round291 lower-stratum freeze.

The Round291 producer is pinned as inert bytes and is never imported or
executed.  Before opening either candidate output, this verifier independently
rebuilds all 55,428 rows from the pinned Round174, Round179, Round182,
Round204, Round208, and Round267 artifacts.  Round280 and Round281 producers
and outputs are neither read nor trusted.

The expected ledger is compared with the candidate row-for-row, as canonical
JSON, and as a deterministic gzip byte stream.  The complete candidate result
is then compared with an independently rebuilt result object.  A separate
fully-resigned mutation suite checks row, ledger, gzip, result, and
strict-nonpromotion attack families.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import sys
import tempfile
from typing import Any, Iterable


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round291_source_g_complete_lower_stratum_local_disposition_freeze"
DEFAULT_LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
DEFAULT_RESULT = HERE / f"{PREFIX}_result.json"
PRODUCER = HERE / f"{PREFIX}.py"
DEFAULT_OUTPUT = HERE / f"{PREFIX}_verification.json"
SCHEMA = "cm2.round291.source-g-complete-lower-stratum-local-disposition-freeze.v1"
LEDGER_SCHEMA = (
    "cm2.round291.source-g-complete-lower-stratum-local-disposition-ledger.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round291.source-g-complete-lower-stratum-local-disposition-freeze."
    "verification.v1"
)

PRODUCER_SHA256 = (
    "1f485f0add666eecb83e73b5cd498b490d0f8895726717bccb4c8727600838c7"
)
CANDIDATE_LEDGER_SHA256 = (
    "412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab"
)
CANDIDATE_RESULT_FILE_SHA256 = (
    "f07aae7d12b9d33aea0313737b7dafa51b22c1c8b1e5526ecf87ad53c5a8f705"
)
CANDIDATE_RESULT_SHA256 = (
    "2397c4d1e83155fdf1c8cd625fb772be0a5c39e1b758d6f7e5ae7bb8131dbc77"
)

INPUT_SHA256 = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json":
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json":
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round267_source_g_lower_stratum_terminal_lineage_certificate.json":
        "66879215e0250a4a462fea9837c24bccf49a936ce3c5e66da2707e1a66fafc8f",
}

WHOLE_PHYSICAL = "WHOLE_PHYSICAL_SUPPORT"
WHOLE_ABSENT = "WHOLE_SUPPORT_ABSENT"
PARTITIONED = "PARTITIONED_PHYSICAL_AND_ABSENT"
PENDING_BINDING = "PENDING_FINAL_OCCURRENCE_REGISTRY"
NO_OCCURRENCE = "NO_OCCURRENCE__LOCAL_ABSENCE"

ZERO_FIELDS = (
    "expanded_occurrence_credit",
    "component_edge_credit",
    "maximality_credit",
    "exact_key_fibre_credit",
    "global_exact_key_disposition_credit",
    "Jx_Jy_same_point_glue_credit",
)

EXPECTED_BASIS = {
    "ROUND182_EXPLICIT_FULL_OR_CLIPPED_2D_GRAPH_SHEET": 38_244,
    "ROUND182_EXHAUSTIVE_CLOSED_COLLAR_ALL_GRAPH_LEAVES_EMPTY": 15_492,
    "ROUND182_STRICT_INTERIOR_INTERVAL_NEWTON_TRANSVERSE_1D_LINE": 112,
    "ROUND182_PAIR_STRICT_SAME_SIGN_P_FACES": 216,
    "ROUND204_EXPLICIT_SOURCE_OR_TARGET_2D_SHEET_WITH_HALF_OPEN_LINEAGE": 32,
    "ROUND208_EXPLICIT_RESIDUAL_OUTGOING_GRAPH_SHEET_AND_SIDES": 52,
    "ROUND208_EXHAUSTIVE_RESIDUAL_OUTGOING_ROWS_ALL_EMPTY": 4,
    "ROUND179_TWO_RESOLVED_P_CHILDREN__STRICT_PREDICATE_SIGNS__EXACT_VOLUME_COVER":
        396,
    "ROUND204_POSITIVE_T_OWNER_POLICY__ROUND179_EXACT_T0_RETAINED_OWNER_CHILD":
        440,
    "ROUND204_POSITIVE_T_OWNER_POLICY__EXACT_POSITIVE_RETAINED_CHILD_PATCH_COVER":
        372,
    "ROUND204_POSITIVE_T_ONLY_OWNER_POLICY__COMPLETE_ROUND174_UNIQUE_FIRST_PARENT_UNIVERSE_HAS_NO_POSITIVE_T_OWNER":
        60,
    "ROUND204_POSITIVE_T_OWNER_POLICY__EXACT_POSITIVE_RETAINED_CHILD_PATCH_COVER_PLUS_COMPLETE_ROUND174_COMPLEMENT_ABSENCE":
        8,
}


class Round291Error(RuntimeError):
    """Fail-closed contract violation."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Round291Error(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            state.update(chunk)
    return state.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        value = json.load(stream)
    need(isinstance(value, dict), f"JSON object:{path.name}")
    return value


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = result["row_column_schemas"][table]
    packed = result[table]
    need(
        all(isinstance(row, list) and len(row) == len(columns) for row in packed),
        f"packed width:{table}",
    )
    return [dict(zip(columns, row, strict=True)) for row in packed]


def closed(row: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in row, "row already closed")
    output = dict(row)
    output["row_sha256"] = digest(output)
    return output


def zero_credit(disposition: str) -> dict[str, Any]:
    return {
        **{field: 0 for field in ZERO_FIELDS},
        "nominal_lineage_promoted_to_occurrence": False,
        "requires_final_DSU_to_decide_local_physical_support": False,
        "occurrence_binding_status": (
            NO_OCCURRENCE if disposition == WHOLE_ABSENT else PENDING_BINDING
        ),
    }


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def qbox(values: list[str]) -> tuple[Q, Q, Q, Q, Q, Q]:
    need(len(values) == 6, "box width")
    return tuple(map(Q, values))  # type: ignore[return-value]


Interval = tuple[Q, Q]


def iv(value: Q) -> Interval:
    return value, value


def iv_add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def iv_neg(value: Interval) -> Interval:
    return -value[1], -value[0]


def iv_sub(left: Interval, right: Interval) -> Interval:
    return iv_add(left, iv_neg(right))


def iv_mul(left: Interval, right: Interval) -> Interval:
    products = (
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    )
    return min(products), max(products)


def iv_scale(value: Interval, scalar: Q) -> Interval:
    if scalar >= 0:
        return value[0] * scalar, value[1] * scalar
    return value[1] * scalar, value[0] * scalar


def iv_square(value: Interval) -> Interval:
    if value[0] <= 0 <= value[1]:
        return Q(0), max(value[0] * value[0], value[1] * value[1])
    squares = value[0] * value[0], value[1] * value[1]
    return min(squares), max(squares)


def sqrt_fraction_bounds(value: Q, bits: int) -> Interval:
    """Return an exact outward dyadic enclosure of sqrt(value)."""
    need(value >= 0 and bits >= 64, "nonnegative rational square root")
    if value == 0:
        return Q(0), Q(0)
    scale = 1 << bits
    scaled_floor = (value.numerator << (2 * bits)) // value.denominator
    root_floor = math.isqrt(scaled_floor)
    lower = Q(root_floor, scale)
    upper = lower if lower * lower == value else Q(root_floor + 1, scale)
    need(lower * lower <= value <= upper * upper, "dyadic sqrt enclosure")
    return lower, upper


def iv_sqrt(value: Interval, bits: int) -> Interval:
    need(value[0] > 0, "strictly positive interval radical")
    return (
        sqrt_fraction_bounds(value[0], bits)[0],
        sqrt_fraction_bounds(value[1], bits)[1],
    )


def parse_target_id(target_id: str) -> tuple[str, int, int]:
    need(
        len(target_id) >= 6
        and target_id[0] in {"G", "W"}
        and target_id[1] == "["
        and target_id[-1] == "]",
        "target syntax",
    )
    coordinates = target_id[2:-1].split(",")
    need(len(coordinates) == 2, "target coordinate arity")
    obstacle = target_id[0]
    ix, iy = int(coordinates[0]), int(coordinates[1])
    need(
        -4 <= ix <= 4
        and -4 <= iy <= 4
        and target_id == f"{obstacle}[{ix},{iy}]",
        "target finite registry syntax",
    )
    return obstacle, ix, iy


def exact_fraction_geometry(
    chart: str,
    target_id: str,
    values: list[str],
    bits: int = 256,
) -> dict[str, Interval]:
    """Rebuild source and hit coordinates on a whole rational box.

    All arithmetic is exact rational interval arithmetic.  The only
    irrational operations are square roots, each enclosed outward by exact
    dyadic rationals at ``bits`` precision.
    """
    t0, t1, p0, p1, s0, s1 = qbox(values)
    t = (t0, t1)
    p = (p0, p1)
    s = (s0, s1)
    one = iv(Q(1))
    rt = iv_sqrt(iv_sub(one, iv_square(t)), bits)
    rp = iv_sqrt(iv_sub(one, iv_square(p)), bits)
    cell = chart.split(":", 1)[1]
    need(cell in {"E", "W", "N", "S"}, "source chart cell")
    if cell == "E":
        nx, ny = rt, t
    elif cell == "W":
        nx, ny = iv_neg(rt), t
    elif cell == "N":
        nx, ny = t, rt
    else:
        nx, ny = t, iv_neg(rt)
    ux = iv_sub(iv_mul(rp, nx), iv_mul(p, ny))
    uy = iv_add(iv_mul(rp, ny), iv_mul(p, nx))
    source_x = iv_scale(nx, Q(9, 25))
    source_y = iv_scale(ny, Q(9, 25))
    obstacle, ix, iy = parse_target_id(target_id)
    if obstacle == "G":
        center_x = iv(Q(ix))
        center_y = iv(Q(iy))
        target_radius = Q(9, 25)
    else:
        center_x = iv_add(iv(Q(ix) + Q(1, 2)), s)
        center_y = iv(Q(iy) + Q(1, 2))
        target_radius = Q(4, 25)
    dx = iv_sub(center_x, source_x)
    dy = iv_sub(center_y, source_y)
    transverse = iv_add(iv_neg(iv_mul(uy, dx)), iv_mul(ux, dy))
    discriminant = iv_sub(
        iv(target_radius * target_radius),
        iv_square(transverse),
    )
    radical = iv_sqrt(discriminant, bits)
    outgoing_x = iv_scale(
        iv_add(
            iv_neg(iv_mul(radical, ux)),
            iv_mul(transverse, uy),
        ),
        Q(1, 1) / target_radius,
    )
    outgoing_y = iv_scale(
        iv_sub(
            iv_neg(iv_mul(radical, uy)),
            iv_mul(transverse, ux),
        ),
        Q(1, 1) / target_radius,
    )
    return {
        "source_x": source_x,
        "source_y": source_y,
        "hit_x": iv_add(center_x, iv_scale(outgoing_x, target_radius)),
        "hit_y": iv_add(center_y, iv_scale(outgoing_y, target_radius)),
        "discriminant": discriminant,
    }


def strict_interval_sign(value: Interval) -> str:
    if value[0] > 0:
        return "STRICT_POSITIVE"
    if value[1] < 0:
        return "STRICT_NEGATIVE"
    return "OVERWRAP"


def interval_payload(value: Interval) -> list[str]:
    return [qstr(value[0]), qstr(value[1])]


def face_rect(values: list[str]) -> tuple[Q, Q, Q, Q]:
    box = qbox(values)
    return box[2], box[3], box[4], box[5]


def rect_payload(rect: tuple[Q, Q, Q, Q]) -> list[str]:
    return ["0", "0", *(qstr(value) for value in rect)]


def area(rect: tuple[Q, Q, Q, Q]) -> Q:
    return (rect[1] - rect[0]) * (rect[3] - rect[2])


def intersection(
    left: tuple[Q, Q, Q, Q],
    right: tuple[Q, Q, Q, Q],
) -> tuple[Q, Q, Q, Q] | None:
    hit = (
        max(left[0], right[0]),
        min(left[1], right[1]),
        max(left[2], right[2]),
        min(left[3], right[3]),
    )
    return None if hit[0] >= hit[1] or hit[2] >= hit[3] else hit


def union_area_disjoint(
    rectangles: list[tuple[Q, Q, Q, Q]],
) -> tuple[Q, bool]:
    if not rectangles:
        return Q(0), True
    p_values = sorted({value for rect in rectangles for value in rect[:2]})
    s_values = sorted({value for rect in rectangles for value in rect[2:]})
    total = Q(0)
    disjoint = True
    for p0, p1 in zip(p_values, p_values[1:]):
        for s0, s1 in zip(s_values, s_values[1:]):
            multiplicity = sum(
                rect[0] <= p0 and p1 <= rect[1]
                and rect[2] <= s0 and s1 <= rect[3]
                for rect in rectangles
            )
            if multiplicity:
                total += (p1 - p0) * (s1 - s0)
            if multiplicity > 1:
                disjoint = False
    return total, disjoint


def exact_rect_complement(
    container: tuple[Q, Q, Q, Q],
    covered: list[tuple[Q, Q, Q, Q]],
) -> list[tuple[Q, Q, Q, Q]]:
    clipped = [
        hit for rectangle in covered
        if (hit := intersection(container, rectangle)) is not None
    ]
    p_values = sorted({
        container[0], container[1],
        *(value for rectangle in clipped for value in rectangle[:2]),
    })
    s_values = sorted({
        container[2], container[3],
        *(value for rectangle in clipped for value in rectangle[2:]),
    })
    output: list[tuple[Q, Q, Q, Q]] = []
    for p0, p1 in zip(p_values, p_values[1:]):
        for s0, s1 in zip(s_values, s_values[1:]):
            cell = (p0, p1, s0, s1)
            if not any(
                rectangle[0] <= p0 and p1 <= rectangle[1]
                and rectangle[2] <= s0 and s1 <= rectangle[3]
                for rectangle in clipped
            ):
                output.append(cell)
    return sorted(output)


def make_id(lineage_id: str, support_id: str) -> str:
    return "round291-lower-local-disposition:" + digest([lineage_id, support_id])


def base_row(
    lineage: dict[str, Any],
    disposition: str,
    role: str,
    basis: str,
    evidence_row_ids: list[str],
    physical_cells: list[dict[str, Any]],
    absence_cells: list[dict[str, Any]],
) -> dict[str, Any]:
    support_id = lineage["canonical_support_or_absence_row_id"]
    return closed({
        "complete_lower_stratum_local_disposition_row_id": make_id(
            lineage["lower_stratum_terminal_lineage_row_id"],
            support_id,
        ),
        "Round267_lower_stratum_terminal_lineage_row_id":
            lineage["lower_stratum_terminal_lineage_row_id"],
        "Round174_stratum_id": lineage["Round174_stratum_id"],
        "canonical_support_row_id": support_id,
        "canonical_support_kind": lineage["canonical_support_kind"],
        "containing_Round174_residual_row_id":
            lineage["containing_Round174_residual_row_id"],
        "parent_id": lineage["parent_id"],
        "source_chart": lineage["source_chart"],
        "predicate_label": lineage["predicate_label"],
        "predicate_equation": lineage["predicate_equation"],
        "local_disposition": disposition,
        "representation_role": role,
        "evidence_basis": basis,
        "evidence_row_ids": evidence_row_ids,
        "physical_witness_cell_count": len(physical_cells),
        "physical_witness_cells": physical_cells,
        "absence_witness_cell_count": len(absence_cells),
        "absence_witness_cells": absence_cells,
        "physical_witness_cells_sha256": digest(physical_cells),
        "absence_witness_cells_sha256": digest(absence_cells),
        **zero_credit(disposition),
    })


def audit_rows(rows: list[dict[str, Any]], expected_digest: str | None = None) -> None:
    need(len(rows) == 55_428, "complete output census")
    ids = [row["complete_lower_stratum_local_disposition_row_id"] for row in rows]
    need(len(ids) == len(set(ids)), "unique disposition ids")
    for row in rows:
        payload = {key: value for key, value in row.items() if key != "row_sha256"}
        need(digest(payload) == row["row_sha256"], "closed output row")
        need(all(row[field] == 0 for field in ZERO_FIELDS), "zero credit")
        expected_binding = (
            NO_OCCURRENCE
            if row["local_disposition"] == WHOLE_ABSENT
            else PENDING_BINDING
        )
        need(
            row["occurrence_binding_status"] == expected_binding
            and not row["nominal_lineage_promoted_to_occurrence"]
            and not row["requires_final_DSU_to_decide_local_physical_support"],
            "strict local-only scope",
        )
        need(
            row["physical_witness_cell_count"]
            == len(row["physical_witness_cells"])
            and row["absence_witness_cell_count"]
            == len(row["absence_witness_cells"])
            and row["physical_witness_cells_sha256"]
            == digest(row["physical_witness_cells"])
            and row["absence_witness_cells_sha256"]
            == digest(row["absence_witness_cells"]),
            "witness attachment closure",
        )
        if row["local_disposition"] == WHOLE_PHYSICAL:
            need(
                row["physical_witness_cell_count"] > 0
                and row["absence_witness_cell_count"] == 0,
                "whole physical witnesses",
            )
        elif row["local_disposition"] == WHOLE_ABSENT:
            need(
                row["physical_witness_cell_count"] == 0
                and row["absence_witness_cell_count"] > 0,
                "whole absence witnesses",
            )
        else:
            need(
                row["local_disposition"] == PARTITIONED
                and row["representation_role"] == "MIXED_SHADOW_AND_ABSENCE"
                and row["physical_witness_cell_count"] > 0
                and row["absence_witness_cell_count"] > 0,
                "partitioned witnesses",
            )
    histogram = Counter(row["local_disposition"] for row in rows)
    need(
        histogram == {
            WHOLE_PHYSICAL: 39_252,
            WHOLE_ABSENT: 16_168,
            PARTITIONED: 8,
        },
        "final disposition histogram",
    )
    need(
        Counter(row["evidence_basis"] for row in rows) == EXPECTED_BASIS,
        "evidence basis histogram",
    )
    if expected_digest is not None:
        need(digest(rows) == expected_digest, "expected complete rows digest")


def run_attacks(rows: list[dict[str, Any]]) -> dict[str, Any]:
    expected = digest(rows)
    physical_index = next(
        index for index, row in enumerate(rows)
        if row["local_disposition"] == WHOLE_PHYSICAL
    )
    absent_index = next(
        index for index, row in enumerate(rows)
        if row["local_disposition"] == WHOLE_ABSENT
    )
    mixed_index = next(
        index for index, row in enumerate(rows)
        if row["local_disposition"] == PARTITIONED
    )

    attacks: list[tuple[str, Any]] = [
        ("grant_occurrence_credit", (physical_index, "expanded_occurrence_credit", 1)),
        ("grant_component_credit", (physical_index, "component_edge_credit", 1)),
        ("grant_maximality_credit", (physical_index, "maximality_credit", 1)),
        ("grant_fibre_credit", (physical_index, "exact_key_fibre_credit", 1)),
        ("grant_global_disposition", (physical_index, "global_exact_key_disposition_credit", 1)),
        ("grant_JxJy_glue", (physical_index, "Jx_Jy_same_point_glue_credit", 1)),
        ("forge_lineage_id", (physical_index, "Round267_lower_stratum_terminal_lineage_row_id", "forged")),
        ("forge_support_id", (physical_index, "canonical_support_row_id", "forged")),
        ("forge_evidence_basis", (physical_index, "evidence_basis", "forged")),
        ("forge_evidence_reference", (physical_index, "evidence_row_ids", ["forged"])),
        ("physical_to_absent", (physical_index, "local_disposition", WHOLE_ABSENT)),
        ("absent_to_physical", (absent_index, "local_disposition", WHOLE_PHYSICAL)),
        ("partition_to_whole", (mixed_index, "local_disposition", WHOLE_PHYSICAL)),
        ("shadow_to_owner", (mixed_index, "representation_role", "HALF_OPEN_OWNER")),
        ("bind_occurrence_early", (physical_index, "occurrence_binding_status", "BOUND")),
        ("bind_absence_to_registry", (absent_index, "occurrence_binding_status", "BOUND")),
        ("mark_absence_pending", (absent_index, "occurrence_binding_status", PENDING_BINDING)),
        ("claim_lineage_promotion", (physical_index, "nominal_lineage_promoted_to_occurrence", True)),
        ("forge_DSU_dependency", (physical_index, "requires_final_DSU_to_decide_local_physical_support", True)),
        ("forge_physical_cell_count", (physical_index, "physical_witness_cell_count", 0)),
        ("forge_absence_cell_count", (absent_index, "absence_witness_cell_count", 0)),
        ("erase_partition_absence", (mixed_index, "absence_witness_cells", [])),
        ("erase_partition_physical", (mixed_index, "physical_witness_cells", [])),
        ("forge_physical_cell_digest", (physical_index, "physical_witness_cells_sha256", "0" * 64)),
        ("forge_absence_cell_digest", (absent_index, "absence_witness_cells_sha256", "0" * 64)),
        ("duplicate_disposition_id", (1, "complete_lower_stratum_local_disposition_row_id", rows[0]["complete_lower_stratum_local_disposition_row_id"])),
    ]
    rejected = 0
    labels: list[str] = []
    for label, (index, field, value) in attacks:
        candidate = list(rows)
        changed = dict(candidate[index])
        changed[field] = value
        changed.pop("row_sha256", None)
        candidate[index] = closed(changed)
        try:
            audit_rows(candidate, expected)
        except Round291Error:
            rejected += 1
            labels.append(label)
        else:
            raise Round291Error(f"attack accepted:{label}")

    for label, candidate in (
        ("drop_row", rows[:-1]),
        ("append_duplicate_row", [*rows, rows[-1]]),
    ):
        try:
            audit_rows(candidate, expected)
        except Round291Error:
            rejected += 1
            labels.append(label)
        else:
            raise Round291Error(f"attack accepted:{label}")

    need(rejected == len(attacks) + 2 and rejected >= 19, "attack census")
    return {
        "attack_count": rejected,
        "rejected_count": rejected,
        "attack_labels": labels,
        "all_targeted_resigned_attacks_rejected": True,
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    for filename, expected in INPUT_SHA256.items():
        need(file_sha256(HERE / filename) == expected, f"pinned input:{filename}")

    # Round267 is used only to define the complete nominal universe and its
    # immutable provenance keys.  It never supplies physical existence.
    round267 = read_json(
        HERE / "cm2_round267_source_g_lower_stratum_terminal_lineage_certificate.json"
    )
    lineage_ledger = round267["result"][
        "formal_Round174_lower_stratum_terminal_lineage_ledger"
    ]
    lineage_rows = lineage_ledger["rows"]
    need(
        len(lineage_rows) == 62_696
        and digest(lineage_rows) == lineage_ledger["rows_sha256"],
        "Round267 ledger closure",
    )
    nominal: dict[str, dict[str, Any]] = {}
    for row in lineage_rows:
        payload = {key: value for key, value in row.items() if key != "row_sha256"}
        need(digest(payload) == row["row_sha256"], "Round267 row closure")
        if not row["nominal_support_only"]:
            continue
        need(
            row["terminal_lineage_status"] == "MATERIALIZED_AS_CANONICAL_SUPPORT"
            and row["physical_existence_credit"] == 0
            and row["descendant_wide_absence_credit"] == 0,
            "Round267 nominal provenance only",
        )
        support_id = row["canonical_support_or_absence_row_id"]
        need(support_id not in nominal, "unique nominal support id")
        nominal[support_id] = {
            key: row[key]
            for key in (
                "lower_stratum_terminal_lineage_row_id",
                "Round174_stratum_id",
                "canonical_support_or_absence_row_id",
                "canonical_support_kind",
                "containing_Round174_residual_row_id",
                "parent_id",
                "source_chart",
                "predicate_label",
                "predicate_equation",
            )
        }
    need(
        len(nominal) == 55_428
        and Counter(row["canonical_support_kind"] for row in nominal.values())
        == {
            "NOMINAL_REGULAR_ZERO_SET_IF_PRESENT": 30_444,
            "NOMINAL_REGULAR_FACTOR_UNION_IF_PRESENT": 24_656,
            "NOMINAL_PAIR_CANDIDATE_IF_TRANSVERSE": 328,
        },
        "complete Round267 nominal universe",
    )
    del round267, lineage_rows
    gc.collect()

    round179 = read_json(
        HERE / "cm2_round179_source_g_residual_tube_arrangement_rows.json"
    )["result"]
    origins = unpack(round179, "origin_tube_rows")
    outgoing = unpack(round179, "outgoing_normal_form_rows")
    walls = unpack(round179, "wall_normal_form_rows")
    resolved = unpack(round179, "resolved_3d_child_rows")
    retained = unpack(round179, "retained_3d_child_rows")
    guards = unpack(round179, "chart_guard_child_rows")
    del round179
    gc.collect()
    need(len(origins) == 62_012, "Round179 origin census")
    origin_by_id = {row["origin_row_id"]: row for row in origins}
    outgoing_by_id = {row["row_id"]: row for row in outgoing}
    wall_by_id = {row["row_id"]: row for row in walls}
    children_by_origin: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for kind, table in (
        ("RESOLVED", resolved),
        ("RETAINED", retained),
        ("GUARD", guards),
    ):
        for row in table:
            children_by_origin[row["origin_row_id"]].append((kind, row))

    round182 = read_json(
        HERE / "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
    )["result"]
    collars = unpack(round182, "collar_occurrence_rows")
    leaves = unpack(round182, "collar_leaf_rows")
    pairs = unpack(round182, "pair_intersection_rows")
    del round182
    gc.collect()
    leaves_by_occurrence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for leaf in leaves:
        leaves_by_occurrence[leaf["occurrence_row_id"]].append(leaf)

    decisions: dict[str, dict[str, Any]] = {}
    replaced_supports: set[str] = set()
    residual_outgoing: set[str] = set()
    residual_wall: set[str] = set()

    for collar in collars:
        support_id = collar["Round179_occurrence_row_id"]
        need(support_id in nominal, f"Round182 nominal collar:{support_id}")
        support_leaves = sorted(
            leaves_by_occurrence[support_id],
            key=lambda row: row["row_id"],
        )
        classification = Counter(
            row["graph_classification"] for row in support_leaves
        )
        need(
            len(support_leaves)
            == collar["closed_leaf_count"] + collar["residual_leaf_count"]
            and classification["FULL_2D"] == collar["full_base_graph_leaf_count"]
            and classification["CLIPPED_2D_BOUNDARY_1D"]
            == collar["clipped_graph_leaf_count"]
            and classification["EMPTY"] == collar["absent_graph_leaf_count"]
            and classification["RESIDUAL_3D"] == collar["residual_leaf_count"]
            and classification["FULL_2D"]
            + classification["CLIPPED_2D_BOUNDARY_1D"]
            == collar["two_dimensional_graph_sheet_count"]
            and sum(Q(row["coordinate_volume"]) for row in support_leaves)
            == Q(collar["Round179_retained_coordinate_volume"]),
            f"Round182 exact collar conservation:{support_id}",
        )
        if collar["Round179_origin_already_fully_replaced"]:
            need(not support_leaves, f"fully replaced has no collar:{support_id}")
            replaced_supports.add(support_id)
            continue
        if collar["two_dimensional_graph_sheet_count"]:
            physical = [
                {
                    "witness_kind": "ROUND182_GRAPH_SHEET_LEAF",
                    "leaf_row_id": leaf["row_id"],
                    "retained_child_row_id": leaf["retained_child_row_id"],
                    "graph_classification": leaf["graph_classification"],
                    "exact_box": leaf["box"],
                    "base_coordinate_area": leaf["base_coordinate_area"],
                }
                for leaf in support_leaves
                if leaf["graph_classification"]
                in {"FULL_2D", "CLIPPED_2D_BOUNDARY_1D"}
            ]
            need(physical, f"physical collar witness:{support_id}")
            decisions[support_id] = {
                "disposition": WHOLE_PHYSICAL,
                "role": "DIRECT_GRAPH_SHEET_WITNESS",
                "basis": "ROUND182_EXPLICIT_FULL_OR_CLIPPED_2D_GRAPH_SHEET",
                "evidence": [collar["row_id"], *(row["leaf_row_id"] for row in physical)],
                "physical": physical,
                "absence": [],
            }
        elif collar["residual_leaf_count"]:
            need(
                collar["kind"] in {"OUTGOING", "WALL"},
                f"pure residual collar:{support_id}",
            )
            (residual_outgoing if collar["kind"] == "OUTGOING" else residual_wall).add(
                support_id
            )
            continue
        else:
            need(
                collar["fully_clipped_over_Round179_retained_children"],
                f"closed collar cover:{support_id}",
            )
            need(
                support_leaves
                and all(row["graph_classification"] == "EMPTY" for row in support_leaves),
                f"exhaustive empty collar:{support_id}",
            )
            absence = [
                {
                    "witness_kind": "ROUND182_EMPTY_GRAPH_LEAF",
                    "leaf_row_id": leaf["row_id"],
                    "retained_child_row_id": leaf["retained_child_row_id"],
                    "exact_box": leaf["box"],
                }
                for leaf in support_leaves
            ]
            decisions[support_id] = {
                "disposition": WHOLE_ABSENT,
                "role": "NO_PHYSICAL_SUPPORT",
                "basis": "ROUND182_EXHAUSTIVE_CLOSED_COLLAR_ALL_GRAPH_LEAVES_EMPTY",
                "evidence": [collar["row_id"], *(row["leaf_row_id"] for row in absence)],
                "physical": [],
                "absence": absence,
            }

    need(
        len(collars) == 54_220
        and len(replaced_supports) == 396
        and len(residual_outgoing) == 56
        and len(residual_wall) == 32,
        "Round182 collar routing census",
    )

    pair_join_count = 0
    for pair in pairs:
        support_id = pair["Round179_pair_row_id"]
        if support_id not in nominal:
            continue
        pair_join_count += 1
        classification = pair["existence_classification"]
        if classification == (
            "UNIQUE_TRANSVERSE_1D_INTERSECTION_LINE__"
            "P_BRACKET_AND_INTERVAL_NEWTON"
        ):
            need(
                pair["actual_intersection_dimension"] == "EXACT_DIMENSION_1"
                and pair["actual_1D_intersection_component_count"] == 1
                and pair["interval_newton_interior"],
                f"strict pair witness:{support_id}",
            )
            decisions[support_id] = {
                "disposition": WHOLE_PHYSICAL,
                "role": "DIRECT_TRANSVERSE_LINE_WITNESS",
                "basis": "ROUND182_STRICT_INTERIOR_INTERVAL_NEWTON_TRANSVERSE_1D_LINE",
                "evidence": [pair["row_id"]],
                "physical": [{
                    "witness_kind": "ROUND182_TRANSVERSE_1D_LINE",
                    "pair_row_id": pair["row_id"],
                    "containing_retained_child_row_id":
                        pair["containing_Round179_retained_child_row_id"],
                    "interval_newton_domain": pair["interval_newton_domain"],
                    "interval_newton_image": pair["interval_newton_image"],
                    "strict_2x2_Jacobian_minor_sign":
                        pair["strict_2x2_Jacobian_minor_sign"],
                }],
                "absence": [],
            }
        else:
            need(
                classification == "EMPTY__STRICT_SAME_SIGN_P_FACES"
                and pair["actual_1D_intersection_component_count"] == 0,
                f"strict pair absence:{support_id}",
            )
            decisions[support_id] = {
                "disposition": WHOLE_ABSENT,
                "role": "NO_PHYSICAL_SUPPORT",
                "basis": "ROUND182_PAIR_STRICT_SAME_SIGN_P_FACES",
                "evidence": [pair["row_id"]],
                "physical": [],
                "absence": [{
                    "witness_kind": "ROUND182_STRICT_SAME_SIGN_PAIR",
                    "pair_row_id": pair["row_id"],
                    "p_lower_sign": pair["p_lower_sign"],
                    "p_upper_sign": pair["p_upper_sign"],
                    "p_lower_value_interval": pair["p_lower_value_interval"],
                    "p_upper_value_interval": pair["p_upper_value_interval"],
                }],
            }
    need(pair_join_count == 328, "nominal pair census")
    del collars, leaves, pairs, leaves_by_occurrence
    gc.collect()

    round204 = read_json(
        HERE / "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )["result"]
    completion_by_origin = {
        row["origin_row_id"]: row
        for row in round204["origin_local_completion_ledger"]["rows"]
    }
    lineage204 = round204["formal_2D_sheet_lineage"]
    need(
        lineage204["source_sheet_row_count"] == 224
        and lineage204["all_source_sheets_have_positive_t_half_open_owner"],
        "Round204 source owner policy",
    )
    sheets204 = {
        row["sheet_row_id"]: row
        for row in (
            lineage204["source_sheet_rows"] + lineage204["target_sheet_rows"]
        )
    }
    for support_id in sorted(residual_wall):
        wall = wall_by_id[support_id]
        completion = completion_by_origin[wall["origin_row_id"]]
        sheet_rows = [
            sheets204[row_id]
            for row_id in completion["incident_2D_sheet_row_ids"]
        ]
        need(
            completion["Round204_fully_locally_signature_replaced"]
            and sheet_rows
            and all(
                row["ambient_dimension"] == 2
                and row["local_dimension_lineage_materialized"]
                and row["wall_axis"] == wall["axis"]
                and row["integer_wall"] == wall["integer_wall"]
                for row in sheet_rows
            ),
            f"Round204 wall sheet witness:{support_id}",
        )
        physical = [
            {
                "witness_kind": row["sheet_kind"],
                "sheet_row_id": row["sheet_row_id"],
                "exact_ambient_bounds": row["exact_ambient_bounds"],
                "half_open_owner_policy": row["half_open_owner_policy"],
                "half_open_owner_region_row_id":
                    row.get("half_open_owner_region_row_id"),
                "wall_axis": row["wall_axis"],
                "integer_wall": row["integer_wall"],
            }
            for row in sorted(sheet_rows, key=lambda item: item["sheet_row_id"])
        ]
        decisions[support_id] = {
            "disposition": WHOLE_PHYSICAL,
            "role": "HALF_OPEN_2D_SHEET_OWNER_LINEAGE",
            "basis": "ROUND204_EXPLICIT_SOURCE_OR_TARGET_2D_SHEET_WITH_HALF_OPEN_LINEAGE",
            "evidence": [row["sheet_row_id"] for row in physical],
            "physical": physical,
            "absence": [],
        }

    # Round208 proves existence or exhaustive leaf emptiness but does not by
    # itself promote a lower-dimensional occurrence.
    round208 = read_json(
        HERE / "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )["result"]
    signature_rows = round208["formal_local_open_3D_signature_ledger"]["rows"]
    signatures_by_occurrence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in signature_rows:
        if row["occurrence_row_id"] in residual_outgoing:
            signatures_by_occurrence[row["occurrence_row_id"]].append(row)
    need(
        set(signatures_by_occurrence) == residual_outgoing,
        "Round208 residual occurrence join",
    )
    for support_id in sorted(residual_outgoing):
        rows208 = sorted(
            signatures_by_occurrence[support_id],
            key=lambda row: row["region_row_id"],
        )
        residual_leaf_ids = {
            row["leaf_row_id"]
            for row in rows208
        }
        need(
            rows208
            and all(
                row["formal_local_open_3D_signature_credit"] == 1
                and row["leaf_classification"]
                in {"FULL_2D", "CLIPPED_2D_BOUNDARY_1D", "EMPTY"}
                for row in rows208
            ),
            f"Round208 direct signature rows:{support_id}",
        )
        nonempty = [
            row for row in rows208
            if row["leaf_classification"] != "EMPTY"
        ]
        need(
            all(
                sum(other["leaf_row_id"] == leaf_id for other in rows208)
                == (1 if classification == "EMPTY" else 2)
                for leaf_id, classification in {
                    row["leaf_row_id"]: row["leaf_classification"]
                    for row in rows208
                }.items()
            ),
            f"Round208 side multiplicity:{support_id}",
        )
        if nonempty:
            physical = [
                {
                    "witness_kind": "ROUND208_DIRECT_GRAPH_SIDE_REGION",
                    "region_row_id": row["region_row_id"],
                    "leaf_row_id": row["leaf_row_id"],
                    "leaf_classification": row["leaf_classification"],
                    "exact_leaf_box": row["Round182_leaf_box"],
                    "local_return_signature": row["local_return_signature"],
                    "strict_open_3D_region_exists":
                        row["strict_open_3D_region_exists"],
                }
                for row in nonempty
            ]
            decisions[support_id] = {
                "disposition": WHOLE_PHYSICAL,
                "role": "GRAPH_EXISTS__OWNER_BINDING_STILL_PENDING",
                "basis": "ROUND208_EXPLICIT_RESIDUAL_OUTGOING_GRAPH_SHEET_AND_SIDES",
                "evidence": [row["region_row_id"] for row in physical],
                "physical": physical,
                "absence": [],
            }
        else:
            absence = [
                {
                    "witness_kind": "ROUND208_DIRECT_EMPTY_GRAPH_REGION",
                    "region_row_id": row["region_row_id"],
                    "leaf_row_id": row["leaf_row_id"],
                    "exact_leaf_box": row["Round182_leaf_box"],
                }
                for row in rows208
            ]
            need(len(residual_leaf_ids) == len(rows208), "Round208 empty leaf cover")
            decisions[support_id] = {
                "disposition": WHOLE_ABSENT,
                "role": "NO_PHYSICAL_SUPPORT",
                "basis": "ROUND208_EXHAUSTIVE_RESIDUAL_OUTGOING_ROWS_ALL_EMPTY",
                "evidence": [row["region_row_id"] for row in absence],
                "physical": [],
                "absence": absence,
            }
    del round208, signature_rows, signatures_by_occurrence
    gc.collect()

    # The 396 missing collars are not absence merely because they are
    # missing.  Rebuild the exact two-child cover and strict signs with an
    # independent pure-Fraction interval evaluator.
    replaced_kind_histogram = Counter(
        "OUTGOING" if support_id in outgoing_by_id else "WALL"
        for support_id in replaced_supports
    )
    need(
        replaced_kind_histogram == {"OUTGOING": 284, "WALL": 112},
        "fully replaced support-kind census",
    )
    wall_sign_pair_histogram: Counter[str] = Counter()
    for support_id in sorted(replaced_supports):
        normal = outgoing_by_id.get(support_id) or wall_by_id.get(support_id)
        need(normal is not None, f"fully replaced normal form:{support_id}")
        origin = origin_by_id[normal["origin_row_id"]]
        entries = children_by_origin[origin["origin_row_id"]]
        resolved_children = sorted(
            [row for kind, row in entries if kind == "RESOLVED"],
            key=lambda row: row["child_index"],
        )
        retained_children = [row for kind, row in entries if kind == "RETAINED"]
        guard_children = [row for kind, row in entries if kind == "GUARD"]
        need(
            origin["fully_replaced_by_bounded_children"]
            and origin["chosen_split_axis"] == "p"
            and len(resolved_children) == 2
            and not retained_children
            and not guard_children
            and sum(Q(row["coordinate_volume"]) for row in resolved_children)
            == Q(origin["original_coordinate_volume"]),
            f"fully replaced exact cover:{support_id}",
        )
        absence: list[dict[str, Any]] = []
        if support_id in outgoing_by_id:
            signs: list[str] = []
            for child in resolved_children:
                cell = child["outgoing_cell"]
                need(cell in {"E", "W", "N", "S"}, "resolved outgoing cell")
                sign = (
                    "STRICT_POSITIVE" if cell in {"E", "W"}
                    else "STRICT_NEGATIVE"
                )
                signs.append(sign)
                absence.append({
                    "witness_kind": "ROUND179_RESOLVED_OUTGOING_CHILD",
                    "resolved_child_row_id": child["row_id"],
                    "child_index": child["child_index"],
                    "exact_box": child["box"],
                    "outgoing_cell": cell,
                    "predicate_sign": sign,
                })
            need(len(set(signs)) == 1, f"outgoing strict sign cover:{support_id}")
        else:
            wall = wall_by_id[support_id]
            source_name = "source_x" if wall["axis"] == "X" else "source_y"
            target_name = "hit_x" if wall["axis"] == "X" else "hit_y"
            sign_pairs: list[tuple[str, str]] = []
            for child in resolved_children:
                geometry = exact_fraction_geometry(
                    child["chart"],
                    origin["owner_target"],
                    child["box"],
                )
                source_interval = iv_sub(
                    geometry[source_name],
                    iv(Q(wall["integer_wall"])),
                )
                target_interval = iv_sub(
                    geometry[target_name],
                    iv(Q(wall["integer_wall"])),
                )
                source_sign = strict_interval_sign(source_interval)
                target_sign = strict_interval_sign(target_interval)
                need(
                    source_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
                    and target_sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
                    f"wall resolved strict factors:{child['row_id']}",
                )
                sign_pairs.append((source_sign, target_sign))
                absence.append({
                    "witness_kind": "ROUND179_RESOLVED_WALL_CHILD",
                    "resolved_child_row_id": child["row_id"],
                    "child_index": child["child_index"],
                    "exact_box": child["box"],
                    "source_endpoint_factor_sign": source_sign,
                    "target_endpoint_factor_sign": target_sign,
                    "source_endpoint_factor_interval":
                        interval_payload(source_interval),
                    "target_endpoint_factor_interval":
                        interval_payload(target_interval),
                    "discriminant_interval":
                        interval_payload(geometry["discriminant"]),
                    "exact_dyadic_sqrt_enclosure_bits": 256,
                })
            need(
                len(set(sign_pairs)) == 1,
                f"wall strict factor-pair cover:{support_id}",
            )
            source_sign, target_sign = sign_pairs[0]
            wall_sign_pair_histogram[
                f"{source_sign}|{target_sign}"
            ] += 1
        decisions[support_id] = {
            "disposition": WHOLE_ABSENT,
            "role": "NO_PHYSICAL_SUPPORT",
            "basis":
                "ROUND179_TWO_RESOLVED_P_CHILDREN__STRICT_PREDICATE_SIGNS__"
                "EXACT_VOLUME_COVER",
            "evidence": [row["resolved_child_row_id"] for row in absence],
            "physical": [],
            "absence": absence,
        }
    need(
        wall_sign_pair_histogram == {
            "STRICT_POSITIVE|STRICT_POSITIVE": 48,
            "STRICT_NEGATIVE|STRICT_NEGATIVE": 48,
            "STRICT_NEGATIVE|STRICT_POSITIVE": 8,
            "STRICT_POSITIVE|STRICT_NEGATIVE": 8,
        },
        "fully replaced wall sign-pair census",
    )

    # The remaining 880 rows are exact source t=0 factor sheets.  Apply the
    # frozen outcome-blind positive-t owner policy and exact rational face
    # partitions over the complete Round174 parent universe.
    undecided = set(nominal) - set(decisions)
    need(len(undecided) == 880, "exact t0 tail universe")
    round174 = read_json(
        HERE / "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
    )["result"]
    parents = unpack(round174, "parent_rows")
    del round174
    gc.collect()
    need(len(parents) == 21_232, "complete Round174 parent universe")

    positive_origins_by_chart: dict[
        str, list[tuple[dict[str, Any], dict[str, Any], tuple[Q, Q, Q, Q]]]
    ] = defaultdict(list)
    for origin in origins:
        box = qbox(origin["original_box"])
        if not (box[0] == 0 and box[1] > 0):
            continue
        adjacent = [
            (kind, child)
            for kind, child in children_by_origin[origin["origin_row_id"]]
            if qbox(child["box"])[0] == 0
        ]
        need(
            len(adjacent) == 1 and adjacent[0][0] == "RETAINED"
            and face_rect(adjacent[0][1]["box"])
            == face_rect(origin["original_box"]),
            f"positive t0 retained owner:{origin['origin_row_id']}",
        )
        positive_origins_by_chart[origin["chart"]].append(
            (origin, adjacent[0][1], face_rect(origin["original_box"]))
        )
    positive_parents_by_chart: dict[
        str, list[tuple[dict[str, Any], tuple[Q, Q, Q, Q]]]
    ] = defaultdict(list)
    for parent in parents:
        box = qbox(parent["box"])
        if box[0] == 0 and box[1] > 0:
            positive_parents_by_chart[parent["chart"]].append(
                (parent, face_rect(parent["box"]))
            )

    total_t0_area = Q(0)
    physical_t0_area = Q(0)
    absent_t0_area = Q(0)
    for support_id in sorted(undecided):
        lineage = nominal[support_id]
        wall = wall_by_id[support_id]
        origin = origin_by_id[wall["origin_row_id"]]
        box = qbox(origin["original_box"])
        rectangle = face_rect(origin["original_box"])
        rectangle_area = area(rectangle)
        total_t0_area += rectangle_area
        need(
            lineage["canonical_support_kind"]
            == "NOMINAL_REGULAR_FACTOR_UNION_IF_PRESENT"
            and wall["source_factor_classification"] == "REGULAR_GRAPH"
            and wall["source_gradient_axis"] == "t"
            and wall["integer_wall"] == 0
            and wall["target_face_classification"] == "STRICT_ZERO_ABSENT"
            and ((box[0] == 0) ^ (box[1] == 0)),
            f"exact t0 symbolic contract:{support_id}",
        )
        physical_cells: list[dict[str, Any]] = []
        absence_cells: list[dict[str, Any]] = []
        evidence: list[str] = [support_id]
        if box[0] == 0:
            adjacent = [
                child for kind, child
                in children_by_origin[origin["origin_row_id"]]
                if kind == "RETAINED" and qbox(child["box"])[0] == 0
            ]
            need(len(adjacent) == 1, f"self positive owner:{support_id}")
            physical_cells = [{
                "witness_kind": "ROUND179_POSITIVE_T0_RETAINED_OWNER",
                "exact_bounds": rect_payload(rectangle),
                "cell_area": qstr(rectangle_area),
                "positive_owner_origin_row_id": origin["origin_row_id"],
                "positive_owner_retained_child_row_id": adjacent[0]["row_id"],
                "positive_owner_parent_id": origin["parent_id"],
                "owner_target": origin["owner_target"],
                "owner_policy":
                    "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
                    "NEGATIVE_T_SIDE_IS_SHADOW",
            }]
            evidence.append(adjacent[0]["row_id"])
            basis = (
                "ROUND204_POSITIVE_T_OWNER_POLICY__ROUND179_EXACT_T0_"
                "RETAINED_OWNER_CHILD"
            )
            disposition = WHOLE_PHYSICAL
            role = "HALF_OPEN_OWNER"
            physical_t0_area += rectangle_area
        else:
            patches: list[tuple[Q, Q, Q, Q]] = []
            for owner, child, owner_rect in (
                positive_origins_by_chart[origin["chart"]]
            ):
                hit = intersection(rectangle, owner_rect)
                if hit is None:
                    continue
                # This strengthening is true for the frozen universe and
                # prevents a merely same-chart but different-target alias.
                need(
                    owner["owner_target"] == origin["owner_target"],
                    f"shadow owner target identity:{support_id}",
                )
                patches.append(hit)
                physical_cells.append({
                    "witness_kind": "ROUND179_NEGATIVE_T0_SHADOW_PATCH",
                    "exact_bounds": rect_payload(hit),
                    "cell_area": qstr(area(hit)),
                    "negative_shadow_origin_row_id": origin["origin_row_id"],
                    "positive_owner_origin_row_id": owner["origin_row_id"],
                    "positive_owner_retained_child_row_id": child["row_id"],
                    "positive_owner_parent_id": owner["parent_id"],
                    "owner_target": owner["owner_target"],
                    "owner_policy":
                        "OUTCOME_BLIND_POSITIVE_T_SIDE_OWNS__"
                        "NEGATIVE_T_SIDE_IS_SHADOW",
                })
                evidence.extend((owner["origin_row_id"], child["row_id"]))
            union, disjoint = union_area_disjoint(patches)
            need(disjoint, f"shadow patch disjointness:{support_id}")
            if union == rectangle_area:
                disposition = WHOLE_PHYSICAL
                role = "SHADOW_ALIAS_TO_POSITIVE_OWNER"
                basis = (
                    "ROUND204_POSITIVE_T_OWNER_POLICY__EXACT_POSITIVE_"
                    "RETAINED_CHILD_PATCH_COVER"
                )
                physical_t0_area += union
            elif union > 0:
                complements = exact_rect_complement(rectangle, patches)
                complement_area, complement_disjoint = union_area_disjoint(
                    complements
                )
                need(
                    union < rectangle_area
                    and complement_disjoint
                    and union + complement_area == rectangle_area,
                    f"partial exact t0 partition:{support_id}",
                )
                for cell in complements:
                    need(
                        not any(
                            intersection(cell, parent_rect) is not None
                            for _parent, parent_rect
                            in positive_parents_by_chart[origin["chart"]]
                        ),
                        f"partial complement positive parent:{support_id}",
                    )
                    absence_cells.append({
                        "witness_kind": "COMPLETE_ROUND174_POSITIVE_PARENT_ABSENCE",
                        "exact_bounds": rect_payload(cell),
                        "cell_area": qstr(area(cell)),
                        "complete_positive_parent_overlap_absent": True,
                    })
                disposition = PARTITIONED
                role = "MIXED_SHADOW_AND_ABSENCE"
                basis = (
                    "ROUND204_POSITIVE_T_OWNER_POLICY__EXACT_POSITIVE_"
                    "RETAINED_CHILD_PATCH_COVER_PLUS_COMPLETE_ROUND174_"
                    "COMPLEMENT_ABSENCE"
                )
                physical_t0_area += union
                absent_t0_area += complement_area
            else:
                need(
                    not any(
                        intersection(rectangle, parent_rect) is not None
                        for _parent, parent_rect
                        in positive_parents_by_chart[origin["chart"]]
                    )
                    and Q(-1) == 2 * Q(0) * Q(0) - 1,
                    f"complete negative t0 absence:{support_id}",
                )
                absence_cells = [{
                    "witness_kind": "COMPLETE_ROUND174_POSITIVE_PARENT_ABSENCE",
                    "exact_bounds": rect_payload(rectangle),
                    "cell_area": qstr(rectangle_area),
                    "complete_positive_parent_overlap_absent": True,
                }]
                disposition = WHOLE_ABSENT
                role = "NO_PHYSICAL_SUPPORT"
                basis = (
                    "ROUND204_POSITIVE_T_ONLY_OWNER_POLICY__COMPLETE_"
                    "ROUND174_UNIQUE_FIRST_PARENT_UNIVERSE_HAS_NO_"
                    "POSITIVE_T_OWNER"
                )
                absent_t0_area += rectangle_area
        decisions[support_id] = {
            "disposition": disposition,
            "role": role,
            "basis": basis,
            "evidence": sorted(set(evidence)),
            "physical": physical_cells,
            "absence": absence_cells,
        }

    need(
        total_t0_area == Q(31, 640)
        and physical_t0_area == Q(59, 1280)
        and absent_t0_area == Q(3, 1280)
        and total_t0_area == physical_t0_area + absent_t0_area,
        "global exact t0 area conservation",
    )
    need(set(decisions) == set(nominal), "complete nominal decision join")

    rows = [
        base_row(
            nominal[support_id],
            decision["disposition"],
            decision["role"],
            decision["basis"],
            decision["evidence"],
            decision["physical"],
            decision["absence"],
        )
        for support_id, decision in sorted(decisions.items())
    ]
    rows.sort(
        key=lambda row: row["complete_lower_stratum_local_disposition_row_id"]
    )
    audit_rows(rows)
    attacks = run_attacks(rows)

    disposition_histogram = Counter(row["local_disposition"] for row in rows)
    role_histogram = Counter(row["representation_role"] for row in rows)
    support_kind_by_disposition: dict[str, Counter[str]] = defaultdict(Counter)
    chart_by_disposition: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        support_kind_by_disposition[row["canonical_support_kind"]][
            row["local_disposition"]
        ] += 1
        chart_by_disposition[row["source_chart"]][row["local_disposition"]] += 1

    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": (
            "COMPLETE_55428_NOMINAL_LOWER_STRATUM_LOCAL_DISPOSITION_FREEZE__"
            "39252_WHOLE_PHYSICAL__16168_WHOLE_ABSENT__8_PARTITIONED__"
            "ZERO_UNRESOLVED__ZERO_GLOBAL_CREDIT"
        ),
        "row_count": len(rows),
        "row_ids_sha256": digest([
            row["complete_lower_stratum_local_disposition_row_id"]
            for row in rows
        ]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "rows": rows,
    }
    result = {
        "schema": SCHEMA,
        "status": (
            "ROUND291_COMPLETE_LOWER_STRATUM_LOCAL_DISPOSITION_CANDIDATE__"
            "AWAITING_INDEPENDENT_VERIFIER__ZERO_CREDIT"
        ),
        "pins": INPUT_SHA256,
        "independence_contract": {
            "Round280_producer_imported_or_executed": False,
            "Round281_producer_imported_or_executed": False,
            "Round280_or_Round281_output_used_as_truth": False,
            "Round179_verifier_imported_or_executed": False,
            "python_flint_required": False,
            "complete_Round267_nominal_universe_reopened": 55_428,
            "complete_upstream_geometry_reconstructed_cachelessly": True,
            "shared_lower_level_evaluator": "NONE",
            "fully_replaced_wall_geometry_method":
                "PURE_FRACTION_INTERVAL_ARITHMETIC_WITH_EXACT_256_BIT_"
                "DYADIC_OUTWARD_SQRT_ENCLOSURES",
        },
        "census": {
            "Round267_nominal_support_count": 55_428,
            "local_disposition_histogram":
                dict(sorted(disposition_histogram.items())),
            "representation_role_histogram": dict(sorted(role_histogram.items())),
            "evidence_basis_histogram": dict(sorted(
                Counter(row["evidence_basis"] for row in rows).items()
            )),
            "support_kind_by_disposition": {
                kind: dict(sorted(counter.items()))
                for kind, counter in sorted(support_kind_by_disposition.items())
            },
            "source_chart_by_disposition": {
                chart: dict(sorted(counter.items()))
                for chart, counter in sorted(chart_by_disposition.items())
            },
            "whole_physical_support_count": disposition_histogram[WHOLE_PHYSICAL],
            "whole_absent_support_count": disposition_histogram[WHOLE_ABSENT],
            "partitioned_physical_and_absent_support_count":
                disposition_histogram[PARTITIONED],
            "unresolved_local_decision_count": 0,
            "fully_replaced_support_kind_histogram":
                dict(sorted(replaced_kind_histogram.items())),
            "fully_replaced_wall_sign_pair_histogram":
                dict(sorted(wall_sign_pair_histogram.items())),
            "total_t0_face_area": qstr(total_t0_area),
            "physical_t0_face_area": qstr(physical_t0_area),
            "absent_t0_face_area": qstr(absent_t0_area),
            "t0_area_partition_delta":
                qstr(total_t0_area - physical_t0_area - absent_t0_area),
        },
        "attack_suite": attacks,
        "ledger_attachment": {
            "filename": DEFAULT_LEDGER.name,
            "schema": LEDGER_SCHEMA,
            "row_count": ledger["row_count"],
            "row_ids_sha256": ledger["row_ids_sha256"],
            "row_hashes_sha256": ledger["row_hashes_sha256"],
            "rows_sha256": ledger["rows_sha256"],
        },
        "strict_nonpromotion": {
            **{field: 0 for field in ZERO_FIELDS},
            "physical_and_partitioned_occurrence_bindings": PENDING_BINDING,
            "whole_absent_occurrence_binding": NO_OCCURRENCE,
            "physical_local_support_is_not_expanded_occurrence": True,
            "absence_is_not_an_occurrence": True,
            "shadow_alias_does_not_create_an_occurrence": True,
            "partitioned_parent_does_not_receive_whole_row_credit": True,
            "quotient": 63_224,
            "expanded_occurrences": 126_468,
            "maximality": "0/63224",
            "exact_key_fibres": "0/116",
            "global_dispositions": "0/224580",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_gate": (
            "bind every physical witness or shadow patch to the independently "
            "frozen final occurrence registry using exact provenance, exact "
            "geometry, complete signature, and exact-key identity; absence "
            "rows bind to no occurrence and the eight partitioned rows bind "
            "only their physical child cells"
        ),
    }
    return ledger, result


def gzip_payload(value: Any) -> bytes:
    return gzip_payload_at_mtime(value, 0)


def gzip_payload_at_mtime(value: Any, mtime: int) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=buffer,
        mtime=mtime,
    ) as stream:
        for chunk in chunks(value):
            stream.write(chunk)
    return buffer.getvalue()


def close_result(value: dict[str, Any]) -> dict[str, Any]:
    output = deepcopy(value)
    output.pop("result_sha256", None)
    output["result_sha256"] = digest(output)
    return output


def rebuilt_ledger(
    rows: list[dict[str, Any]],
    template: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema": template["schema"],
        "status": template["status"],
        "row_count": len(rows),
        "row_ids_sha256": digest([
            row["complete_lower_stratum_local_disposition_row_id"]
            for row in rows
        ]),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
        "rows": rows,
    }


def resign_layers(
    rows: list[dict[str, Any]],
    expected_ledger: dict[str, Any],
    expected_result: dict[str, Any],
    *,
    mtime: int = 0,
) -> tuple[bytes, dict[str, Any], bytes, dict[str, Any]]:
    ledger = rebuilt_ledger(rows, expected_ledger)
    ledger_raw = gzip_payload_at_mtime(ledger, mtime)
    result = deepcopy(expected_result)
    result.pop("result_sha256", None)
    result["ledger_attachment"].update({
        "row_count": ledger["row_count"],
        "row_ids_sha256": ledger["row_ids_sha256"],
        "row_hashes_sha256": ledger["row_hashes_sha256"],
        "rows_sha256": ledger["rows_sha256"],
        "file_sha256": hashlib.sha256(ledger_raw).hexdigest(),
    })
    result = close_result(result)
    return ledger_raw, ledger, canonical(result), result


def validate_candidate_layers(
    ledger_raw: bytes,
    ledger: dict[str, Any],
    result_raw: bytes,
    result: dict[str, Any],
    expected_ledger_raw: bytes,
    expected_ledger: dict[str, Any],
    expected_result_raw: bytes,
    expected_result: dict[str, Any],
) -> None:
    need(ledger_raw == expected_ledger_raw, "complete deterministic gzip equality")
    need(ledger == expected_ledger, "complete ledger object equality")
    need(result_raw == expected_result_raw, "complete result byte equality")
    need(result == expected_result, "complete result object equality")


def set_path(root: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    cursor: dict[str, Any] = root
    for key in path[:-1]:
        child = cursor[key]
        need(isinstance(child, dict), f"attack path:{'.'.join(path)}")
        cursor = child
    cursor[path[-1]] = value


def independent_attack_suite(
    expected_ledger_raw: bytes,
    expected_ledger: dict[str, Any],
    expected_result_raw: bytes,
    expected_result: dict[str, Any],
) -> dict[str, Any]:
    """Reject mutations after all affected envelopes have been re-signed."""
    rows = expected_ledger["rows"]
    physical_index = next(
        index for index, row in enumerate(rows)
        if row["local_disposition"] == WHOLE_PHYSICAL
    )
    absent_index = next(
        index for index, row in enumerate(rows)
        if row["local_disposition"] == WHOLE_ABSENT
    )
    partition_index = next(
        index for index, row in enumerate(rows)
        if row["local_disposition"] == PARTITIONED
    )
    shadow_index = next(
        index for index, row in enumerate(rows)
        if row["representation_role"] == "SHADOW_ALIAS_TO_POSITIVE_OWNER"
    )

    rejected: list[str] = []

    def reject(
        label: str,
        layers: tuple[bytes, dict[str, Any], bytes, dict[str, Any]],
    ) -> None:
        try:
            validate_candidate_layers(
                *layers,
                expected_ledger_raw,
                expected_ledger,
                expected_result_raw,
                expected_result,
            )
        except Round291Error:
            rejected.append(label)
        else:
            raise Round291Error(f"attack accepted:{label}")

    def resigned_row_attack(
        label: str,
        index: int,
        mutator: Any,
    ) -> None:
        changed_rows = list(rows)
        changed = deepcopy(changed_rows[index])
        changed.pop("row_sha256")
        mutator(changed)
        changed_rows[index] = closed(changed)
        reject(
            label,
            resign_layers(changed_rows, expected_ledger, expected_result),
        )

    resigned_row_attack(
        "ROW_GRANT_ALL_FORMAL_CREDITS",
        physical_index,
        lambda row: row.update({field: 1 for field in ZERO_FIELDS}),
    )

    def forge_provenance(row: dict[str, Any]) -> None:
        row["Round267_lower_stratum_terminal_lineage_row_id"] = "forged-lineage"
        row["canonical_support_row_id"] = "forged-support"
        row["evidence_basis"] = "FORGED_EVIDENCE"
        row["evidence_row_ids"] = ["forged-evidence-row"]
        row["physical_witness_cells"][0]["witness_kind"] = "FORGED_WITNESS"
        row["physical_witness_cells_sha256"] = digest(
            row["physical_witness_cells"]
        )

    resigned_row_attack(
        "ROW_FORGE_LINEAGE_EVIDENCE_AND_GEOMETRY",
        physical_index,
        forge_provenance,
    )

    def physical_to_absent(row: dict[str, Any]) -> None:
        row["local_disposition"] = WHOLE_ABSENT
        row["occurrence_binding_status"] = NO_OCCURRENCE

    resigned_row_attack(
        "ROW_PHYSICAL_TO_ABSENT",
        physical_index,
        physical_to_absent,
    )

    def partition_to_whole(row: dict[str, Any]) -> None:
        row["local_disposition"] = WHOLE_PHYSICAL
        row["representation_role"] = "HALF_OPEN_OWNER"
        row["absence_witness_cells"] = []
        row["absence_witness_cell_count"] = 0
        row["absence_witness_cells_sha256"] = digest([])

    resigned_row_attack(
        "ROW_PARTITION_TO_WHOLE_AND_ERASE_COMPLEMENT",
        partition_index,
        partition_to_whole,
    )

    def shadow_to_owner(row: dict[str, Any]) -> None:
        row["representation_role"] = "HALF_OPEN_OWNER"
        cell = row["physical_witness_cells"][0]
        cell["positive_owner_origin_row_id"] = "forged-owner"
        row["physical_witness_cells_sha256"] = digest(
            row["physical_witness_cells"]
        )

    resigned_row_attack(
        "ROW_SHADOW_TO_FORGED_OWNER",
        shadow_index,
        shadow_to_owner,
    )

    def promote_local_scope(row: dict[str, Any]) -> None:
        row["occurrence_binding_status"] = "BOUND"
        row["nominal_lineage_promoted_to_occurrence"] = True
        row["requires_final_DSU_to_decide_local_physical_support"] = True

    resigned_row_attack(
        "ROW_BIND_PROMOTE_AND_FORGE_DSU_DEPENDENCE",
        physical_index,
        promote_local_scope,
    )

    reject(
        "LEDGER_DROP_ROW",
        resign_layers(rows[:-1], expected_ledger, expected_result),
    )
    reject(
        "LEDGER_DUPLICATE_ROW",
        resign_layers([*rows, rows[-1]], expected_ledger, expected_result),
    )
    reordered = list(rows)
    reordered[0], reordered[1] = reordered[1], reordered[0]
    reject(
        "LEDGER_REORDER_ROWS",
        resign_layers(reordered, expected_ledger, expected_result),
    )

    def result_attack(
        label: str,
        path: tuple[str, ...],
        value: Any,
    ) -> None:
        result = deepcopy(expected_result)
        result.pop("result_sha256")
        set_path(result, path, value)
        result = close_result(result)
        reject(
            label,
            (
                expected_ledger_raw,
                expected_ledger,
                canonical(result),
                result,
            ),
        )

    result_attacks = (
        (
            "RESULT_ALTER_55428_CENSUS",
            ("census", "Round267_nominal_support_count"),
            55_427,
        ),
        (
            "RESULT_ALTER_T0_AREA",
            ("census", "total_t0_face_area"),
            "0",
        ),
        (
            "RESULT_PROMOTE_QUOTIENT",
            ("strict_nonpromotion", "quotient"),
            63_223,
        ),
        (
            "RESULT_PROMOTE_MAXIMALITY",
            ("strict_nonpromotion", "maximality"),
            "1/63224",
        ),
        (
            "RESULT_PROMOTE_EXACT_KEY_FIBRE",
            ("strict_nonpromotion", "exact_key_fibres"),
            "1/116",
        ),
        (
            "RESULT_PROMOTE_GLOBAL_DISPOSITION",
            ("strict_nonpromotion", "global_dispositions"),
            "1/224580",
        ),
        (
            "RESULT_PROMOTE_GATE5",
            ("strict_nonpromotion", "Gate5"),
            "18/18",
        ),
        (
            "RESULT_PROMOTE_D02",
            ("strict_nonpromotion", "D02"),
            "UNBLOCKED",
        ),
        (
            "RESULT_PROMOTE_CM2",
            ("strict_nonpromotion", "CM2"),
            "GO_FOR_CLAIM",
        ),
        (
            "RESULT_FORGE_STATUS",
            ("status",),
            "PASS_WITHOUT_VERIFIER",
        ),
        (
            "RESULT_CLAIM_ROUND280_281_TRUTH",
            ("independence_contract", "Round280_or_Round281_output_used_as_truth"),
            True,
        ),
        (
            "RESULT_FORGE_INPUT_PIN",
            (
                "pins",
                "cm2_round267_source_g_lower_stratum_terminal_lineage_certificate.json",
            ),
            "0" * 64,
        ),
        (
            "RESULT_FORGE_LEDGER_DIGEST",
            ("ledger_attachment", "rows_sha256"),
            "0" * 64,
        ),
    )
    for label, path, value in result_attacks:
        result_attack(label, path, value)

    gzip_attack_raw = gzip_payload_at_mtime(expected_ledger, 1)
    gzip_attack_result = deepcopy(expected_result)
    gzip_attack_result.pop("result_sha256")
    gzip_attack_result["ledger_attachment"]["file_sha256"] = hashlib.sha256(
        gzip_attack_raw
    ).hexdigest()
    gzip_attack_result = close_result(gzip_attack_result)
    reject(
        "LEDGER_NONDETERMINISTIC_GZIP_HEADER",
        (
            gzip_attack_raw,
            expected_ledger,
            canonical(gzip_attack_result),
            gzip_attack_result,
        ),
    )

    need(len(rejected) == 23, "independent attack census")
    return {
        "attack_count": len(rejected),
        "rejected_count": len(rejected),
        "all_row_ledger_gzip_result_resigned_attacks_rejected": True,
        "attack_labels": rejected,
    }


def safe_write(path: Path, payload: bytes) -> None:
    need(path.parent.resolve() == HERE.resolve(), "output parent")
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=HERE,
        prefix=f".{path.name}.",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    # Critical ordering: finish the independent expected reconstruction before
    # opening the producer or either candidate output.
    expected_ledger, expected_result = build()
    expected_ledger_raw = gzip_payload(expected_ledger)
    expected_result["ledger_attachment"]["file_sha256"] = hashlib.sha256(
        expected_ledger_raw
    ).hexdigest()
    expected_result["seed_affects_output"] = False
    expected_result = close_result(expected_result)
    expected_result_raw = canonical(expected_result)

    need(file_sha256(PRODUCER) == PRODUCER_SHA256, "inert producer pin")
    need(
        file_sha256(DEFAULT_LEDGER) == CANDIDATE_LEDGER_SHA256,
        "candidate ledger file pin",
    )
    need(
        file_sha256(DEFAULT_RESULT) == CANDIDATE_RESULT_FILE_SHA256,
        "candidate result file pin",
    )

    candidate_ledger_raw = DEFAULT_LEDGER.read_bytes()
    with gzip.GzipFile(fileobj=io.BytesIO(candidate_ledger_raw), mode="rb") as stream:
        candidate_ledger_decoded = stream.read()
    candidate_ledger = json.loads(candidate_ledger_decoded)
    need(isinstance(candidate_ledger, dict), "candidate ledger object")

    candidate_result_raw = DEFAULT_RESULT.read_bytes()
    candidate_result = json.loads(candidate_result_raw)
    need(isinstance(candidate_result, dict), "candidate result object")
    need(
        candidate_result["result_sha256"] == CANDIDATE_RESULT_SHA256,
        "candidate result self-digest pin",
    )
    unsigned_candidate_result = dict(candidate_result)
    unsigned_digest = unsigned_candidate_result.pop("result_sha256")
    need(digest(unsigned_candidate_result) == unsigned_digest, "result closure")

    validate_candidate_layers(
        candidate_ledger_raw,
        candidate_ledger,
        candidate_result_raw,
        candidate_result,
        expected_ledger_raw,
        expected_ledger,
        expected_result_raw,
        expected_result,
    )
    audit_rows(candidate_ledger["rows"], expected_ledger["rows_sha256"])

    attacks = independent_attack_suite(
        expected_ledger_raw,
        expected_ledger,
        expected_result_raw,
        expected_result,
    )
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_ROUND291_COMPLETE_LOWER_STRATUM_LOCAL_"
            "DISPOSITION_FREEZE__ZERO_CREDIT"
        ),
        "pins": {
            **INPUT_SHA256,
            PRODUCER.name: PRODUCER_SHA256,
            DEFAULT_LEDGER.name: CANDIDATE_LEDGER_SHA256,
            DEFAULT_RESULT.name: CANDIDATE_RESULT_FILE_SHA256,
        },
        "independence_contract": {
            "Round291_producer_imported_or_executed": False,
            "Round280_or_Round281_artifact_read": False,
            "expected_reconstruction_completed_before_candidate_open": True,
            "complete_Round267_nominal_universe_reopened": 55_428,
            "exact_arithmetic":
                "fractions.Fraction_with_exact_outward_dyadic_sqrt_bounds",
            "candidate_used_only_after_expected_freeze": True,
        },
        "reconstruction": {
            "row_count": expected_ledger["row_count"],
            "row_ids_sha256": expected_ledger["row_ids_sha256"],
            "row_hashes_sha256": expected_ledger["row_hashes_sha256"],
            "rows_sha256": expected_ledger["rows_sha256"],
            "deterministic_gzip_sha256":
                hashlib.sha256(expected_ledger_raw).hexdigest(),
            "result_sha256": expected_result["result_sha256"],
            "complete_row_ledger_result_equality": True,
            "deterministic_gzip_byte_equality": True,
            "local_disposition_histogram":
                expected_result["census"]["local_disposition_histogram"],
            "evidence_basis_histogram":
                expected_result["census"]["evidence_basis_histogram"],
            "total_t0_face_area":
                expected_result["census"]["total_t0_face_area"],
            "physical_t0_face_area":
                expected_result["census"]["physical_t0_face_area"],
            "absent_t0_face_area":
                expected_result["census"]["absent_t0_face_area"],
            "t0_area_partition_delta":
                expected_result["census"]["t0_area_partition_delta"],
        },
        "semantic_attack_suite": attacks,
        "strict_nonpromotion": expected_result["strict_nonpromotion"],
    }
    verification["verification_sha256"] = digest(verification)
    safe_write(args.output, canonical(verification) + b"\n")
    print(verification["status"])
    print(f"verification_sha256={verification['verification_sha256']}")
    print(f"attacks_rejected={attacks['rejected_count']}/{attacks['attack_count']}")


if __name__ == "__main__":
    main()
