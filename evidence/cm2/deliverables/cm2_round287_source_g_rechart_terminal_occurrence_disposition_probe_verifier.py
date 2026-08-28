#!/usr/bin/env python3
"""Independent, cacheless verifier for the Round287 terminal disposition probe.

The Round287 producer is never imported or executed.  It is treated only as a
pinned inert byte string.  Expected Round287 rows are reconstructed from the
frozen Round174/179 guard data, the Round274 active-factor convention, the
Round275 region atlas, the Round279 atom ledger, the Round280 incidence and
identity contracts, the Round283 analytic-tail guard, the Round284 overlap
ledger, and an independently rebuilt Round286 common refinement.

All arithmetic used for coordinate boxes, t-square recharting, containment,
faces, and overlap sweeps is exact ``fractions.Fraction`` arithmetic.  Active
factor range signs are replayed with the pinned interval evaluator at the
strict monotone extrema.  This verifier issues no occurrence/component/seam/
maximality/fibre/disposition/Jx-Jy credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import importlib
import importlib.util
import io
import json
import os
from pathlib import Path
import random
import sys
import tempfile
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe"
PRODUCER = HERE / f"{PREFIX}.py"
RESULT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
OUTPUT = HERE / f"{PREFIX}_verification.json"

R174_PRODUCER = HERE / (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py"
)
R174_ROWS = HERE / (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
)
R179_PRODUCER = HERE / "cm2_round179_source_g_residual_tube_arrangement.py"
R179_ROWS = HERE / "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R274_PRODUCER = HERE / "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py"
R275 = HERE / (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
)
R279_ATOMS = HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
R280_IDENTITY = HERE / (
    "cm2_round280_source_g_expanded_occurrence_identity_contract_audit_result.json"
)
R280_BINDINGS = HERE / (
    "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_"
    "region_bindings.json.gz"
)
R283_RESULT = HERE / "cm2_round283_source_g_outgoing_seam_tail_independent_probe_result.json"
R283_LEDGER = HERE / "cm2_round283_source_g_outgoing_seam_tail_independent_probe_ledger.json.gz"
R284_RESULT = HERE / "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_result.json"
R284_LEDGER = HERE / "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_ledger.json.gz"
R284_VERIFICATION = HERE / (
    "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_verification.json"
)
R286_RESULT = HERE / "cm2_round286_source_g_partial_overlap_exact_refinement_probe_result.json"
R286_LEDGER = HERE / "cm2_round286_source_g_partial_overlap_exact_refinement_probe_ledger.json.gz"
R286_VERIFIER = HERE / "cm2_round286_source_g_partial_overlap_exact_refinement_probe_verifier.py"
R286_VERIFICATION = HERE / (
    "cm2_round286_source_g_partial_overlap_exact_refinement_probe_verification.json"
)

VERIFICATION_SCHEMA = (
    "cm2.round287.source-g-rechart-terminal-occurrence-disposition-probe."
    "verification.v1"
)
RESULT_SCHEMA = (
    "cm2.round287.source-g-rechart-terminal-occurrence-disposition-probe.v1"
)
LEDGER_SCHEMA = (
    "cm2.round287.source-g-rechart-terminal-occurrence-disposition.ledger.v1"
)

INPUT_PINS = {
    R174_PRODUCER.name:
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    R174_ROWS.name:
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R179_PRODUCER.name:
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R179_ROWS.name:
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R274_PRODUCER.name:
        "677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
    R275.name:
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R279_ATOMS.name:
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    R280_IDENTITY.name:
        "873974c8b343961f9e7c1674a946681749a3c0267bc57a1ccc147ccd21b3bdfc",
    R280_BINDINGS.name:
        "8354eb042455e6d3ed591ee1620c9fc9def1af916a9bfbc0bf42e473e3e6e58b",
    R283_RESULT.name:
        "29a1a48140136f105c2454771afa642794de10c61afc18bfbbefe88f0df70eca",
    R283_LEDGER.name:
        "2643a17cd325a16fabe8508a06b8666811641f837e8c2a2ea8a4a71ab982b786",
    R284_RESULT.name:
        "e25dd7b494ad2c2ccddc17601d28136c1919a3b16e41f008669bd6c14a513692",
    R284_LEDGER.name:
        "39b69e0c5d249454c7ff13da99b260d3a7fabfa03c8ad6866035cbcaa883eb92",
    R284_VERIFICATION.name:
        "f1b3c6f3b9ccb8525fdf29379a7369c958a80ce278f3e5afb7232f5bbd842aa6",
    R286_RESULT.name:
        "a3b705c489eff9df4e1129bcdf960c6ea9de435e326c1d7e040e01d63352d29e",
    R286_LEDGER.name:
        "bb7e28cbe029e2bb414313ec4a08f6366acbbad88a519926ec2a3a424e679eda",
    R286_VERIFIER.name:
        "4861302c8f3bb85ab32ddb8fecd54603a894c110ad8dfe88dcb47c7528facc65",
    R286_VERIFICATION.name:
        "817a212eeac8d855927a617dd07462747c636127e4f4b15ec709f9975a74698e",
}

ROUND287_CANDIDATE_INPUT_PINS = {
    name: value
    for name, value in INPUT_PINS.items()
    if name != R286_VERIFIER.name
}

CANDIDATE_PINS = {
    PRODUCER.name:
        "b39849e3aee21688ccf3eb5443984e9e0e8d7a88ed2d61e059ed3485d84c780d",
    RESULT.name:
        "1265475e5d27f99eda35b16f13ba342e0d270ca1bc064df215a018d3ffae89f9",
    LEDGER.name:
        "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
}

PARTIAL = "PARTIAL_OVERLAP__EXACT_REFINEMENT_REQUIRED"
CONTAINED = "CONTAINED_ALIAS_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED"
DISJOINT = "NEW_DISJOINT_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED"
FULL = "FULL_DESIRED_SIDE_SUPPORT"
CLIPPED = "CLIPPED_DESIRED_SIDE_SUPPORT"
EMPTY = "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL"

TABLES = (
    (
        "region_rows",
        "region_row_count",
        "region_rows_sha256",
        "Round287_region_disposition_row_id",
        13788,
    ),
    (
        "refinement_cell_rows",
        "refinement_cell_row_count",
        "refinement_cell_rows_sha256",
        "Round287_refinement_cell_disposition_row_id",
        7616,
    ),
    (
        "potential_new_support_union_rows",
        "potential_new_support_union_row_count",
        "potential_new_support_union_rows_sha256",
        "Round287_potential_new_support_union_id",
        10020,
    ),
    (
        "valid_internal_physical_face_rows",
        "valid_internal_physical_face_row_count",
        "valid_internal_physical_face_rows_sha256",
        "Round287_internal_physical_face_row_id",
        648,
    ),
    (
        "mutually_exclusive_outer_overlap_pair_rows",
        "mutually_exclusive_outer_overlap_pair_row_count",
        "mutually_exclusive_outer_overlap_pair_rows_sha256",
        "Round287_mutually_exclusive_outer_overlap_pair_row_id",
        3488,
    ),
)

REPLAY_SEEDS = (287071, 287929)

ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


class VerificationError(RuntimeError):
    """Raised for every fail-closed verification rejection."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"{path.name}:top-level object")
    return value


def read_gzip_json(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), f"{path.name}:top-level object")
    return value


def deterministic_gzip_bytes(value: Any) -> bytes:
    stream = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=stream, mtime=0) as handle:
        handle.write(canonical(value))
    return stream.getvalue()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def boxq(values: list[str] | tuple[str, ...]) -> tuple[Q, ...]:
    box = tuple(map(Q, values))
    need(len(box) == 6, "box arity")
    need(
        all(box[2 * axis] < box[2 * axis + 1] for axis in range(3)),
        "positive box",
    )
    return box


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    need("row_sha256" not in row, "row not preclosed")
    row["row_sha256"] = digest(row)
    return row


def verify_closed_rows(
    label: str,
    rows: list[dict[str, Any]],
    id_field: str,
    expected_count: int,
    stored_digest: str | None = None,
) -> list[dict[str, Any]]:
    need(len(rows) == expected_count, f"{label}:count")
    if stored_digest is not None:
        need(digest(rows) == stored_digest, f"{label}:rows digest")
    ids: list[str] = []
    for row in rows:
        payload = dict(row)
        stored = payload.pop("row_sha256")
        need(stored == digest(payload), f"{label}:row closure")
        ids.append(row[id_field])
    need(len(ids) == len(set(ids)), f"{label}:unique ids")
    return rows


def verify_standard_ledger(
    label: str,
    ledger: dict[str, Any],
    id_field: str,
    expected_count: int,
) -> list[dict[str, Any]]:
    rows = verify_closed_rows(
        label,
        ledger["rows"],
        id_field,
        expected_count,
        ledger["rows_sha256"],
    )
    ids = [row[id_field] for row in rows]
    need(ledger["row_count"] == expected_count, f"{label}:header count")
    need(ledger["row_ids_sha256"] == digest(ids), f"{label}:ids digest")
    need(
        ledger["row_hashes_sha256"] == digest([row["row_sha256"] for row in rows]),
        f"{label}:hash digest",
    )
    return rows


def validate_verification_document(
    label: str,
    document: dict[str, Any],
    minimum_attacks: int,
) -> None:
    payload = dict(document)
    stored = payload.pop("verification_sha256")
    need(stored == digest(payload), f"{label}:verification digest")
    attacks = document["attacks"]
    need(
        attacks["attack_count"] >= minimum_attacks
        and attacks["rejected_count"] == attacks["attack_count"]
        and attacks["all_attacks_rejected"] is True,
        f"{label}:attacks",
    )


def unpack_attachment(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    need(document["result_sha256"] == digest(document["result"]), "attachment digest")
    result = document["result"]
    rows = result[table]
    expected = result["table_census_and_sha256"][table]
    need(len(rows) == expected["row_count"], f"{table}:count")
    need(digest(rows) == expected["rows_sha256"], f"{table}:digest")
    columns = result["row_column_schemas"][table]
    return [dict(zip(columns, row, strict=True)) for row in rows]


def square_interval(lo: Q, hi: Q) -> tuple[Q, Q]:
    need(lo * hi > 0, "strict signed t interval")
    return (lo * lo, hi * hi) if lo > 0 else (hi * hi, lo * lo)


def physical_t_square_interval(
    coordinate_box: tuple[Q, ...],
    guard_box: tuple[Q, ...],
) -> tuple[Q, Q]:
    adjacent = square_interval(coordinate_box[0], coordinate_box[1])
    source = square_interval(guard_box[0], guard_box[1])
    image = (1 - source[1], 1 - source[0])
    overlap = (max(adjacent[0], image[0]), min(adjacent[1], image[1]))
    need(overlap[0] < overlap[1], "positive rechart t-square interval")
    return overlap


def signed_t_contains(
    outer: tuple[Q, ...],
    inner_square: tuple[Q, Q],
    inner_sign: int,
) -> bool:
    if (1 if outer[0] > 0 else -1) != inner_sign:
        return False
    outer_square = square_interval(outer[0], outer[1])
    return (
        outer_square[0] <= inner_square[0]
        and inner_square[1] <= outer_square[1]
    )


def strict_outer_contains(outer: tuple[Q, ...], inner: tuple[Q, ...]) -> bool:
    return (
        outer != inner
        and all(
            outer[2 * axis] <= inner[2 * axis]
            and inner[2 * axis + 1] <= outer[2 * axis + 1]
            for axis in range(3)
        )
    )


def common_face(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[Q, ...] | None:
    for axis in range(3):
        value = (
            left[2 * axis + 1]
            if left[2 * axis + 1] == right[2 * axis]
            else right[2 * axis + 1]
            if right[2 * axis + 1] == left[2 * axis]
            else None
        )
        if value is None:
            continue
        intervals: list[tuple[Q, Q]] = []
        for other in range(3):
            if other != axis:
                intervals.append(
                    (
                        max(left[2 * other], right[2 * other]),
                        min(left[2 * other + 1], right[2 * other + 1]),
                    )
                )
        if not all(lo < hi for lo, hi in intervals):
            continue
        result: list[Q] = []
        iterator = iter(intervals)
        for other in range(3):
            result.extend((value, value) if other == axis else next(iterator))
        return tuple(result)
    return None


def load_module_from_path(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    need(spec is not None and spec.loader is not None, f"module spec:{path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_frozen_inputs() -> dict[str, Any]:
    """Load and independently validate all pre-Round287 material."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    basis = load_module_from_path("round286_independent_basis", R286_VERIFIER)
    need(PRODUCER.stem not in sys.modules, "Round287 producer not imported")

    regions = basis.load_round275_regions()
    partial_ids, round284_result_from_basis = basis.load_round284_partial_ids(regions)
    partial_bindings, partial_atom_ids = basis.load_round280_bindings(
        regions, partial_ids
    )

    r284_result = read_json(R284_RESULT)
    r284_ledger = read_gzip_json(R284_LEDGER)
    r284_rows_list = verify_standard_ledger(
        "Round284 overlap ledger",
        r284_ledger,
        "Round284_region_overlap_row_id",
        13788,
    )
    r284_rows = {row["Round275_region_id"]: row for row in r284_rows_list}
    need(len(r284_rows) == len(regions) == 13788, "Round284 region universe")
    need(
        round284_result_from_basis["result_sha256"] == r284_result["result_sha256"],
        "Round284 basis/result agreement",
    )
    contained_atom_ids: set[str] = set()
    for region_id, row in r284_rows.items():
        need(region_id in regions, f"Round284 known region:{region_id}")
        if row["classification"] == CONTAINED:
            relations = [
                relation
                for relation in row["relations"]
                if relation["relation"] == "REGION_STRICTLY_CONTAINED_IN_ATOM"
            ]
            need(len(relations) == 1, f"Round284 unique containment:{region_id}")
            contained_atom_ids.add(relations[0]["canonical_atom_id"])
    need(len(contained_atom_ids) == 176, "Round284 contained target atom census")

    wanted_atoms = set(partial_atom_ids) | contained_atom_ids
    atoms, support_box_count = basis.load_referenced_round279_atoms(wanted_atoms)

    r286_rows_a, r286_summary_a = basis.reconstruct(
        regions, partial_ids, partial_bindings, atoms, REPLAY_SEEDS[0]
    )
    r286_rows_b, r286_summary_b = basis.reconstruct(
        regions, partial_ids, partial_bindings, atoms, REPLAY_SEEDS[1]
    )
    need(r286_rows_a == r286_rows_b, "Round286 cacheless dual-seed rows")
    need(r286_summary_a == r286_summary_b, "Round286 cacheless dual-seed summary")
    r286_ledger = read_gzip_json(R286_LEDGER)
    r286_result = read_json(R286_RESULT)
    basis.audit_candidate(
        r286_ledger,
        r286_result,
        r286_rows_a,
        r286_summary_a,
    )

    guards: dict[str, dict[str, Any]] = {}
    r174_attachment = read_json(R174_ROWS)
    r179_attachment = read_json(R179_ROWS)
    guard_rows = unpack_attachment(
        r174_attachment, "chart_guard_rejection_rows"
    ) + unpack_attachment(r179_attachment, "chart_guard_child_rows")
    need(len(guard_rows) == 880, "Round174/179 guard census")
    for row in guard_rows:
        need(row["row_id"] not in guards, f"unique guard:{row['row_id']}")
        boxq(row["box"])
        guards[row["row_id"]] = row
    need(
        all(row["source_guard_row_id"] in guards for row in regions.values()),
        "Round275 guard coverage",
    )

    identity_wrapper = read_json(R280_IDENTITY)
    need(
        identity_wrapper["result_sha256"] == digest(identity_wrapper["result"]),
        "Round280 identity digest",
    )
    identity_rule = identity_wrapper["result"]["deterministic_identity_rule"]
    need(
        identity_rule["identity_alias_rule"].startswith(
            "Collapse identities only under an explicit exact same-positive-open-region"
        ),
        "Round280 exact identity rule",
    )
    need(
        identity_wrapper["result"]["strict_nonpromotion"][
            "new_expanded_occurrence_credit"
        ] == 0,
        "Round280 zero identity credit",
    )

    r283_result = read_json(R283_RESULT)
    payload283 = {k: v for k, v in r283_result.items() if k != "result_sha256"}
    need(r283_result["result_sha256"] == digest(payload283), "Round283 result digest")
    r283_ledger = read_gzip_json(R283_LEDGER)
    verify_standard_ledger(
        "Round283 endpoint ledger",
        r283_ledger,
        "Round283_endpoint_row_id",
        40,
    )
    need(
        r283_result["census"]["analytic_partition_child_count"] == 64
        and r283_result["census"]["remaining_analytic_tail_endpoint_count"] == 0
        and r283_result["strict_nonpromotion"]["expanded_occurrence_credit"] == 0,
        "Round283 nonoccurrence guard",
    )

    verify284 = read_json(R284_VERIFICATION)
    verify286 = read_json(R286_VERIFICATION)
    validate_verification_document("Round284", verify284, 15)
    validate_verification_document("Round286", verify286, 13)

    return {
        "basis": basis,
        "regions": regions,
        "partial_ids": partial_ids,
        "partial_bindings": partial_bindings,
        "atoms": atoms,
        "support_box_count": support_box_count,
        "r284_rows": r284_rows,
        "r286_rows": r286_rows_a,
        "r286_summary": r286_summary_a,
        "guards": guards,
        "r283_result": r283_result,
        "identity_rule": identity_rule,
    }


def extremal_coordinates(
    values: tuple[Q, ...],
    derivative_signs: list[str | None],
    want_maximum: bool,
) -> tuple[Q, Q, Q]:
    """Choose the exact monotone endpoint without using Round274 code."""
    coordinates: list[Q] = []
    for (lower, upper), sign in zip(
        (
            (values[0], values[1]),
            (values[2], values[3]),
            (values[4], values[5]),
        ),
        derivative_signs,
        strict=True,
    ):
        if sign == "STRICT_POSITIVE":
            coordinates.append(upper if want_maximum else lower)
        elif sign == "STRICT_NEGATIVE":
            coordinates.append(lower if want_maximum else upper)
        else:
            coordinates.append((lower + upper) / 2)
    return coordinates[0], coordinates[1], coordinates[2]


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
    return (
        (value[0] * scalar, value[1] * scalar)
        if scalar >= 0
        else (value[1] * scalar, value[0] * scalar)
    )


def iv_square(value: Interval) -> Interval:
    if value[0] <= 0 <= value[1]:
        return Q(0), max(value[0] * value[0], value[1] * value[1])
    squares = value[0] * value[0], value[1] * value[1]
    return min(squares), max(squares)


def sqrt_fraction_bounds(value: Q, bits: int) -> Interval:
    """Exact dyadic outward enclosure for sqrt(nonnegative rational)."""
    need(value >= 0, "sqrt nonnegative")
    if value == 0:
        return Q(0), Q(0)
    scale = 1 << bits
    scaled_floor = (value.numerator << (2 * bits)) // value.denominator
    root_floor = __import__("math").isqrt(scaled_floor)
    lower = Q(root_floor, scale)
    if lower * lower == value:
        return lower, lower
    return lower, Q(root_floor + 1, scale)


def iv_sqrt(value: Interval, bits: int) -> Interval:
    need(value[0] > 0, "strict positive radical interval")
    return (
        sqrt_fraction_bounds(value[0], bits)[0],
        sqrt_fraction_bounds(value[1], bits)[1],
    )


def parse_target(target_id: str) -> tuple[str, int, int]:
    need(
        len(target_id) >= 6
        and target_id[0] in {"G", "W"}
        and target_id[1] == "["
        and target_id[-1] == "]",
        "target syntax",
    )
    coordinates = target_id[2:-1].split(",")
    need(len(coordinates) == 2, "target coordinate arity")
    return target_id[0], int(coordinates[0]), int(coordinates[1])


def exact_active_interval(
    chart: str,
    target_id: str,
    point: tuple[Q, Q, Q],
    reason: str,
    bits: int,
) -> Interval:
    """Independent rational outward evaluation of the pinned geometry formula."""
    t_value, p_value, s_value = point
    t = iv(t_value)
    p = iv(p_value)
    s = iv(s_value)
    rn = sqrt_fraction_bounds(1 - t_value * t_value, bits)
    rp = sqrt_fraction_bounds(1 - p_value * p_value, bits)
    cell = chart.split(":")[1]
    need(cell in {"E", "W", "N", "S"}, "adjacent chart cell")
    if cell == "E":
        nx, ny = rn, t
    elif cell == "W":
        nx, ny = iv_neg(rn), t
    elif cell == "N":
        nx, ny = t, rn
    else:
        nx, ny = t, iv_neg(rn)

    ux = iv_sub(iv_mul(rp, nx), iv_mul(p, ny))
    uy = iv_add(iv_mul(rp, ny), iv_mul(p, nx))
    source_x = iv_scale(nx, Q(9, 25))
    source_y = iv_scale(ny, Q(9, 25))
    obstacle, ix, iy = parse_target(target_id)
    if obstacle == "G":
        center_x, center_y = iv(Q(ix)), iv(Q(iy))
        target_radius = Q(9, 25)
    else:
        center_x = iv_add(iv(Q(ix) + Q(1, 2)), s)
        center_y = iv(Q(iy) + Q(1, 2))
        target_radius = Q(4, 25)
    dx = iv_sub(center_x, source_x)
    dy = iv_sub(center_y, source_y)
    transverse = iv_add(iv_neg(iv_mul(uy, dx)), iv_mul(ux, dy))
    discriminant = iv_sub(iv(target_radius * target_radius), iv_square(transverse))
    radical = iv_sqrt(discriminant, bits)
    outgoing_x = iv_scale(
        iv_add(iv_neg(iv_mul(radical, ux)), iv_mul(transverse, uy)),
        1 / target_radius,
    )
    outgoing_y = iv_scale(
        iv_sub(iv_neg(iv_mul(radical, uy)), iv_mul(transverse, ux)),
        1 / target_radius,
    )
    hit_x = iv_add(center_x, iv_scale(outgoing_x, target_radius))
    hit_y = iv_add(center_y, iv_scale(outgoing_y, target_radius))
    if reason == "outgoing_chart_seam":
        return iv_sub(iv_square(outgoing_x), iv_square(outgoing_y))
    kind, axis, wall = reason.split(":")
    need(kind == "wall_endpoint_or_count_transition", "active reason kind")
    return iv_sub(hit_x if axis == "X" else hit_y, iv(Q(int(wall))))


def exact_active_sign(
    chart: str,
    target_id: str,
    point: tuple[Q, Q, Q],
    reason: str,
) -> str:
    for bits in (160, 224, 320, 448, 640):
        value = exact_active_interval(chart, target_id, point, reason, bits)
        if value[0] > 0:
            return "STRICT_POSITIVE"
        if value[1] < 0:
            return "STRICT_NEGATIVE"
    raise VerificationError("active factor remains overwrapped at 640 bits")


def signed_cell_state(
    region: dict[str, Any],
    values: tuple[Q, ...],
) -> tuple[str, list[str]]:
    if region.get("arrangement_classification") != "REGULAR_GRAPH_CROSSING":
        return FULL, []
    signs: list[str] = []
    for want_maximum in (False, True):
        point = extremal_coordinates(
            values,
            region["strict_derivative_signs_t_p_s"],
            want_maximum,
        )
        signs.append(
            exact_active_sign(
                region["adjacent_chart"],
                region["owner_target"],
                point,
                region["active_reason"],
            )
        )
    need(
        all(sign in {"STRICT_NEGATIVE", "STRICT_POSITIVE"} for sign in signs),
        "strict active-factor extrema",
    )
    if signs[0] != signs[1]:
        return CLIPPED, signs
    if signs[0] == region["active_factor_side_sign"]:
        return FULL, signs
    return EMPTY, signs


def exact_alias_checks(
    region: dict[str, Any],
    atom: dict[str, Any],
    outer_box: tuple[Q, ...],
    inner_box: tuple[Q, ...],
    inner_square: tuple[Q, Q],
    inner_sign: int,
    label: str,
) -> None:
    """Enforce the non-weakening clauses of the inclusion-alias lemma."""
    need(strict_outer_contains(outer_box, inner_box), f"{label}:strict containment")
    need(region["adjacent_chart"] == atom["source_chart"], f"{label}:physical chart")
    need(region["owner_target"] == atom["owner_target"], f"{label}:owner")
    need(
        region["local_return_signature"]
        == atom["complete_10_field_return_signature"],
        f"{label}:complete ten-field signature",
    )
    need(
        region["complete_10_field_return_signature_sha256"]
        == atom["complete_10_field_return_signature_sha256"]
        == digest(region["local_return_signature"]),
        f"{label}:signature closure",
    )
    for exact_key_field in (
        "official_key_id",
        "official_key_ordinal",
        "official_key_row",
    ):
        need(
            region["local_return_signature"][exact_key_field]
            == atom["complete_10_field_return_signature"][exact_key_field],
            f"{label}:exact key:{exact_key_field}",
        )
    need(
        signed_t_contains(outer_box, inner_square, inner_sign),
        f"{label}:exact physical t inclusion",
    )


def reconstruct_round287(
    frozen: dict[str, Any],
    replay_seed: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Rebuild every Round287 semantic row before reading its candidate."""
    regions: dict[str, dict[str, Any]] = frozen["regions"]
    atoms: dict[str, dict[str, Any]] = frozen["atoms"]
    r284_rows: dict[str, dict[str, Any]] = frozen["r284_rows"]
    r286_rows: list[dict[str, Any]] = frozen["r286_rows"]
    guards: dict[str, dict[str, Any]] = frozen["guards"]

    region_boxes = {
        region_id: boxq(region["adjacent_rational_region_box"])
        for region_id, region in regions.items()
    }
    physical_square: dict[str, tuple[Q, Q]] = {}
    physical_sign: dict[str, int] = {}
    for region_id, region in regions.items():
        guard_box = boxq(guards[region["source_guard_row_id"]]["box"])
        physical_square[region_id] = physical_t_square_interval(
            region_boxes[region_id], guard_box
        )
        physical_sign[region_id] = 1 if region_boxes[region_id][0] > 0 else -1

    shuffled_cells = list(r286_rows)
    random.Random(replay_seed).shuffle(shuffled_cells)
    cell_rows: list[dict[str, Any]] = []
    cell_states: dict[str, str] = {}
    cell_boxes: dict[str, tuple[Q, ...]] = {}
    cells_by_region: dict[str, list[dict[str, Any]]] = defaultdict(list)
    corrected_cells_by_region: dict[str, list[dict[str, Any]]] = defaultdict(list)
    cell_hist: Counter[str] = Counter()
    alias_anchor_hist: Counter[str] = Counter()

    for source in shuffled_cells:
        cell_id = source["Round286_refinement_cell_id"]
        region_id = source["Round275_region_id"]
        region = regions[region_id]
        values = boxq(source["cell_exact_box"])
        guard_box = boxq(guards[region["source_guard_row_id"]]["box"])
        cell_square = physical_t_square_interval(values, guard_box)
        state, extrema = signed_cell_state(region, values)
        occupied = source["atom_occupancy_count"] == 1
        need(source["atom_occupancy_count"] in {0, 1}, "Round286 occupancy")
        alias_atom_id = source["unique_alias_atom_id"] if occupied else None
        alias_ok = False
        alias_status: str | None = None
        if occupied:
            need(alias_atom_id in atoms, f"known alias atom:{cell_id}")
            atom = atoms[alias_atom_id]
            containing = [
                boxq(box)
                for box in atom["frozen_true_support_boxes"]
                if strict_outer_contains(boxq(box), values)
            ]
            need(len(containing) == 1, f"one containing atom box:{cell_id}")
            exact_alias_checks(
                region,
                atom,
                containing[0],
                values,
                cell_square,
                physical_sign[region_id],
                f"cell alias:{cell_id}",
            )
            alias_ok = state != EMPTY
            anchors = atom["existing_Round208_occurrence_row_ids"]
            need(len(anchors) in {0, 1}, f"atom anchor multiplicity:{alias_atom_id}")
            alias_status = (
                "PRESERVE_EXISTING_ROUND208_OCCURRENCE_ID"
                if anchors
                else
                "CONDITIONAL_ON_UNBACKED_ATOM_PROMOTION_OR_LATER_EXACT_ANCHOR"
            )
            alias_anchor_hist[
                ("NONEMPTY" if alias_ok else "EMPTY")
                + ("_R208_ANCHORED" if anchors else "_UNBACKED")
            ] += 1

        if state == EMPTY:
            disposition = "EMPTY_FOR_THIS_R275_SIGNED_REGION__NO_ALIAS_OR_NEW_SUPPORT"
        elif occupied:
            disposition = (
                "EXACT_INCLUSION_ALIAS_REPRESENTATION_SUBCOVER__"
                "CONDITIONAL_ON_CONTAINING_ATOM_IDENTITY"
            )
        else:
            disposition = (
                "NONEMPTY_UNCOVERED_SLICE__MEMBER_OF_ONE_PARENT_LOCAL_NEW_SUPPORT_UNION"
            )
        row = closed(
            {
                "Round287_refinement_cell_disposition_row_id":
                    "round287-cell-disposition:" + digest(cell_id),
                "Round286_refinement_cell_id": cell_id,
                "Round275_region_id": region_id,
                "source_chart": region["source_chart"],
                "adjacent_chart": region["adjacent_chart"],
                "owner_target": region["owner_target"],
                "complete_10_field_return_signature_sha256":
                    region["complete_10_field_return_signature_sha256"],
                "coordinate_box": source["cell_exact_box"],
                "physical_t_sign": physical_sign[region_id],
                "physical_t_square_open_interval": list(map(qstr, cell_square)),
                "signed_region_cell_state": state,
                "active_factor_extremal_signs": extrema,
                "Round286_coordinate_occupancy_count":
                    source["atom_occupancy_count"],
                "containing_atom_id": alias_atom_id,
                "exact_inclusion_alias_lemma_satisfied": alias_ok,
                "containing_atom_identity_status": alias_status,
                "disposition": disposition,
                "formal_occurrence_credit": 0,
                "formal_component_credit": 0,
                "formal_seam_credit": 0,
                "formal_maximality_credit": 0,
                "Jx_Jy_same_point_glue_credit": 0,
            }
        )
        cell_rows.append(row)
        cell_states[cell_id] = state
        cell_boxes[cell_id] = values
        cells_by_region[region_id].append(source)
        corrected_cells_by_region[region_id].append(row)
        cell_hist[
            ("OCCUPIED" if occupied else "UNCOVERED") + "|" + state
        ] += 1

    expected_cell_hist = {
        f"OCCUPIED|{FULL}": 3484,
        f"OCCUPIED|{CLIPPED}": 2048,
        f"OCCUPIED|{EMPTY}": 168,
        f"UNCOVERED|{FULL}": 1108,
        f"UNCOVERED|{CLIPPED}": 432,
        f"UNCOVERED|{EMPTY}": 376,
    }
    need(dict(cell_hist) == expected_cell_hist, "physical-side corrected cell census")

    union_rows: list[dict[str, Any]] = []
    internal_face_rows: list[dict[str, Any]] = []
    union_by_region: dict[str, str] = {}
    partial_hist: Counter[str] = Counter()
    partial_order = list(cells_by_region)
    random.Random(replay_seed ^ 0x287).shuffle(partial_order)
    for region_id in partial_order:
        region = regions[region_id]
        source_cells = cells_by_region[region_id]
        nonempty_uncovered = [
            cell
            for cell in source_cells
            if cell["atom_occupancy_count"] == 0
            and cell_states[cell["Round286_refinement_cell_id"]] != EMPTY
        ]
        nonempty_alias = [
            cell
            for cell in source_cells
            if cell["atom_occupancy_count"] == 1
            and cell_states[cell["Round286_refinement_cell_id"]] != EMPTY
        ]
        empty_cells = [
            cell
            for cell in source_cells
            if cell_states[cell["Round286_refinement_cell_id"]] == EMPTY
        ]
        partial_hist[
            "MIXED_WITH_ONE_NEW_SUPPORT"
            if nonempty_uncovered
            else "FULLY_COVERED_NO_NEW_SUPPORT"
        ] += 1
        if not nonempty_uncovered:
            continue

        parent = list(range(len(nonempty_uncovered)))

        def find(index: int) -> int:
            while parent[index] != index:
                parent[index] = parent[parent[index]]
                index = parent[index]
            return index

        face_ids: list[str] = []
        for left_index in range(len(nonempty_uncovered)):
            for right_index in range(left_index):
                left = nonempty_uncovered[left_index]
                right = nonempty_uncovered[right_index]
                left_id = left["Round286_refinement_cell_id"]
                right_id = right["Round286_refinement_cell_id"]
                face = common_face(cell_boxes[left_id], cell_boxes[right_id])
                if face is None:
                    continue
                face_state, face_signs = signed_cell_state(region, face)
                if face_state == EMPTY:
                    continue
                edge = closed(
                    {
                        "Round287_internal_physical_face_row_id":
                            "round287-internal-physical-face:"
                            + digest([region_id, sorted([left_id, right_id])]),
                        "Round275_region_id": region_id,
                        "left_Round286_cell_id": min(left_id, right_id),
                        "right_Round286_cell_id": max(left_id, right_id),
                        "face_box": list(map(qstr, face)),
                        "signed_region_face_state": face_state,
                        "active_factor_extremal_signs": face_signs,
                        "artificial_refinement_face_only": True,
                        "preserves_one_parent_local_occurrence_identity": True,
                        "formal_component_edge_credit": 0,
                    }
                )
                internal_face_rows.append(edge)
                face_ids.append(edge["Round287_internal_physical_face_row_id"])
                left_root = find(left_index)
                right_root = find(right_index)
                if left_root != right_root:
                    parent[right_root] = left_root
        need(
            len({find(index) for index in range(len(nonempty_uncovered))}) == 1,
            f"one connected uncovered union:{region_id}",
        )
        members = sorted(
            cell["Round286_refinement_cell_id"]
            for cell in nonempty_uncovered
        )
        union_id = "round287-potential-new-support-union:" + digest(
            ["R286_UNCOVERED_PARENT_UNION", region_id, members]
        )
        union_by_region[region_id] = union_id
        union_rows.append(
            closed(
                {
                    "Round287_potential_new_support_union_id": union_id,
                    "source_kind": "R286_NONEMPTY_UNCOVERED_PARENT_UNION",
                    "Round275_region_id": region_id,
                    "source_chart": region["source_chart"],
                    "adjacent_chart": region["adjacent_chart"],
                    "owner_target": region["owner_target"],
                    "complete_10_field_return_signature_sha256":
                        region["complete_10_field_return_signature_sha256"],
                    "nonempty_uncovered_member_cell_count": len(members),
                    "nonempty_uncovered_member_cell_ids": members,
                    "valid_internal_physical_face_count": len(face_ids),
                    "valid_internal_physical_face_ids": sorted(face_ids),
                    "nonempty_alias_slice_count": len(nonempty_alias),
                    "empty_coordinate_cell_count": len(empty_cells),
                    "one_connected_positive_open_support": True,
                    "strictly_disjoint_from_matching_atom_supports": True,
                    "conditional_new_occurrence_count": 1,
                    "formal_occurrence_credit": 0,
                    "formal_component_credit": 0,
                    "formal_seam_credit": 0,
                }
            )
        )

    need(
        dict(partial_hist)
        == {
            "FULLY_COVERED_NO_NEW_SUPPORT": 1292,
            "MIXED_WITH_ONE_NEW_SUPPORT": 892,
        },
        "physical partial-parent census",
    )
    need(len(internal_face_rows) == 648, "valid internal physical faces")
    need(len(union_rows) == 892, "partial-parent support unions")

    region_rows: list[dict[str, Any]] = []
    region_hist: Counter[str] = Counter()
    contained_alias_targets: set[str] = set()
    region_order = list(regions)
    random.Random(replay_seed ^ 0x275).shuffle(region_order)
    for region_id in region_order:
        region = regions[region_id]
        overlap_audit = r284_rows[region_id]
        classification = overlap_audit["classification"]
        alias_atom_id: str | None = None
        inclusion_alias = False
        potential_union_id: str | None = None
        if classification == CONTAINED:
            relations = [
                relation
                for relation in overlap_audit["relations"]
                if relation["relation"] == "REGION_STRICTLY_CONTAINED_IN_ATOM"
            ]
            need(len(relations) == 1, f"unique region containment:{region_id}")
            relation = relations[0]
            alias_atom_id = relation["canonical_atom_id"]
            atom = atoms[alias_atom_id]
            atom_box = boxq(
                atom["frozen_true_support_boxes"][
                    relation["atom_support_box_index"]
                ]
            )
            exact_alias_checks(
                region,
                atom,
                atom_box,
                region_boxes[region_id],
                physical_square[region_id],
                physical_sign[region_id],
                f"region alias:{region_id}",
            )
            inclusion_alias = True
            contained_alias_targets.add(alias_atom_id)
            disposition = (
                "EXACT_INCLUSION_ALIAS_REPRESENTATION_SUBCOVER__"
                "CONDITIONAL_ON_CONTAINING_ATOM_IDENTITY"
            )
        elif classification == DISJOINT:
            need(
                not any(
                    relation["relation"]
                    in {
                        "REGION_STRICTLY_CONTAINED_IN_ATOM",
                        "PARTIAL_POSITIVE_VOLUME_OVERLAP",
                    }
                    for relation in overlap_audit["relations"]
                ),
                f"whole disjoint relation:{region_id}",
            )
            potential_union_id = "round287-potential-new-support-union:" + digest(
                ["WHOLE_R275_REGION", region_id]
            )
            union_by_region[region_id] = potential_union_id
            union_rows.append(
                closed(
                    {
                        "Round287_potential_new_support_union_id":
                            potential_union_id,
                        "source_kind": "WHOLE_R275_DISJOINT_REGION",
                        "Round275_region_id": region_id,
                        "source_chart": region["source_chart"],
                        "adjacent_chart": region["adjacent_chart"],
                        "owner_target": region["owner_target"],
                        "complete_10_field_return_signature_sha256":
                            region["complete_10_field_return_signature_sha256"],
                        "nonempty_uncovered_member_cell_count": 0,
                        "nonempty_uncovered_member_cell_ids": [],
                        "valid_internal_physical_face_count": 0,
                        "valid_internal_physical_face_ids": [],
                        "nonempty_alias_slice_count": 0,
                        "empty_coordinate_cell_count": 0,
                        "one_connected_positive_open_support":
                            region["connected_open_region"],
                        "strictly_disjoint_from_matching_atom_supports": True,
                        "conditional_new_occurrence_count": 1,
                        "formal_occurrence_credit": 0,
                        "formal_component_credit": 0,
                        "formal_seam_credit": 0,
                    }
                )
            )
            disposition = "ONE_STRICTLY_NEW_DISJOINT_SUPPORT_CANDIDATE__ZERO_CREDIT"
        else:
            need(classification == PARTIAL, f"known R284 classification:{region_id}")
            physical_cells = corrected_cells_by_region[region_id]
            nonempty_new = sum(
                row["Round286_coordinate_occupancy_count"] == 0
                and row["signed_region_cell_state"] != EMPTY
                for row in physical_cells
            )
            if nonempty_new:
                potential_union_id = union_by_region[region_id]
                disposition = (
                    "EXACT_REFINEMENT_MIXED__ONE_CONNECTED_STRICTLY_NEW_SUPPORT_"
                    "CANDIDATE_PLUS_INCLUSION_ALIAS_SLICES__ZERO_CREDIT"
                )
            else:
                disposition = (
                    "EXACT_REFINEMENT_PHYSICALLY_FULLY_ATOM_COVERED__"
                    "NO_PARENT_ALIAS_AND_NO_NEW_SUPPORT"
                )
        region_hist[disposition] += 1
        region_rows.append(
            closed(
                {
                    "Round287_region_disposition_row_id":
                        "round287-region-disposition:" + digest(region_id),
                    "Round275_region_id": region_id,
                    "source_guard_row_id": region["source_guard_row_id"],
                    "source_chart": region["source_chart"],
                    "adjacent_chart": region["adjacent_chart"],
                    "owner_target": region["owner_target"],
                    "complete_10_field_return_signature_sha256":
                        region["complete_10_field_return_signature_sha256"],
                    "R275_region_kind": region.get(
                        "region_classification",
                        region.get("arrangement_classification"),
                    ),
                    "physical_t_sign": physical_sign[region_id],
                    "physical_t_square_open_interval":
                        list(map(qstr, physical_square[region_id])),
                    "Round284_classification": classification,
                    "exact_inclusion_alias_lemma_satisfied": inclusion_alias,
                    "containing_atom_id": alias_atom_id,
                    "Round286_refinement_cell_count":
                        len(cells_by_region.get(region_id, [])),
                    "Round287_potential_new_support_union_id":
                        potential_union_id,
                    "disposition": disposition,
                    "formal_occurrence_credit": 0,
                    "formal_component_credit": 0,
                    "formal_seam_credit": 0,
                    "formal_maximality_credit": 0,
                    "Jx_Jy_same_point_glue_credit": 0,
                }
            )
        )

    expected_region_hist = {
        "EXACT_INCLUSION_ALIAS_REPRESENTATION_SUBCOVER__"
        "CONDITIONAL_ON_CONTAINING_ATOM_IDENTITY": 2476,
        "ONE_STRICTLY_NEW_DISJOINT_SUPPORT_CANDIDATE__ZERO_CREDIT": 9128,
        "EXACT_REFINEMENT_PHYSICALLY_FULLY_ATOM_COVERED__"
        "NO_PARENT_ALIAS_AND_NO_NEW_SUPPORT": 1292,
        "EXACT_REFINEMENT_MIXED__ONE_CONNECTED_STRICTLY_NEW_SUPPORT_"
        "CANDIDATE_PLUS_INCLUSION_ALIAS_SLICES__ZERO_CREDIT": 892,
    }
    need(dict(region_hist) == expected_region_hist, "terminal region census")
    need(len(union_rows) == 10020, "conditional new support census")

    # Exhaust all R275 rational/physical-t outer overlaps.  This sweep uses
    # only exact intervals and then validates the mutually exclusive graph
    # sides; it does not consult the Round287 candidate pair table.
    overlap_pairs: list[dict[str, Any]] = []
    by_chart: dict[str, list[tuple[tuple[Q, ...], dict[str, Any]]]] = defaultdict(list)
    for region_id, region in regions.items():
        by_chart[region["adjacent_chart"]].append(
            (region_boxes[region_id], region)
        )
    for chart in sorted(by_chart):
        candidates = sorted(by_chart[chart], key=lambda item: item[0][0])
        for left_index, (left_box, left) in enumerate(candidates):
            left_id = left["reverse_rechart_region_row_id"]
            for right_box, right in candidates[left_index + 1:]:
                if right_box[0] >= left_box[1]:
                    break
                right_id = right["reverse_rechart_region_row_id"]
                if not (
                    max(
                        physical_square[left_id][0],
                        physical_square[right_id][0],
                    )
                    < min(
                        physical_square[left_id][1],
                        physical_square[right_id][1],
                    )
                    and max(left_box[2], right_box[2])
                    < min(left_box[3], right_box[3])
                    and max(left_box[4], right_box[4])
                    < min(left_box[5], right_box[5])
                ):
                    continue
                need(
                    left.get("arrangement_classification")
                    == right.get("arrangement_classification")
                    == "REGULAR_GRAPH_CROSSING",
                    "only regular-graph outer overlaps",
                )
                need(
                    left["source_guard_row_id"] == right["source_guard_row_id"],
                    "outer pair same guard",
                )
                need(left_box == right_box, "outer pair same coordinate cell")
                need(
                    left["active_reason"] == right["active_reason"],
                    "outer pair same factor",
                )
                need(
                    {
                        left["active_factor_side_sign"],
                        right["active_factor_side_sign"],
                    }
                    == {"STRICT_NEGATIVE", "STRICT_POSITIVE"},
                    "outer pair opposite factor sides",
                )
                need(
                    left["complete_10_field_return_signature_sha256"]
                    != right["complete_10_field_return_signature_sha256"],
                    "outer pair distinct complete signatures",
                )
                overlap_pairs.append(
                    closed(
                        {
                            "Round287_mutually_exclusive_outer_overlap_pair_row_id":
                                "round287-mutually-exclusive-pair:"
                                + digest(sorted([left_id, right_id])),
                            "left_Round275_region_id": min(left_id, right_id),
                            "right_Round275_region_id": max(left_id, right_id),
                            "adjacent_chart": chart,
                            "source_guard_row_id": left["source_guard_row_id"],
                            "active_reason": left["active_reason"],
                            "active_factor_side_signs": sorted(
                                [
                                    left["active_factor_side_sign"],
                                    right["active_factor_side_sign"],
                                ]
                            ),
                            "exact_positive_physical_overlap": False,
                            "reason":
                                "SAME_REGULAR_GRAPH_CELL_OPPOSITE_OPEN_FACTOR_SIDES",
                            "occurrence_identity_collapse_credit": 0,
                            "component_edge_credit": 0,
                        }
                    )
                )
    need(len(overlap_pairs) == 3488, "outer-overlap pair census")

    expected_tables: dict[str, list[dict[str, Any]]] = {
        "region_rows": region_rows,
        "refinement_cell_rows": cell_rows,
        "potential_new_support_union_rows": union_rows,
        "valid_internal_physical_face_rows": internal_face_rows,
        "mutually_exclusive_outer_overlap_pair_rows": overlap_pairs,
    }
    for rows_name, _count_name, _digest_name, id_field, expected_count in TABLES:
        rows = expected_tables[rows_name]
        rows.sort(key=lambda row: row[id_field])
        need(len(rows) == expected_count, f"expected {rows_name}:count")
        ids = [row[id_field] for row in rows]
        need(len(ids) == len(set(ids)), f"expected {rows_name}:unique ids")

    expected_ledger: dict[str, Any] = {"schema": LEDGER_SCHEMA}
    for rows_name, count_name, digest_name, _id_field, _expected_count in TABLES:
        expected_ledger[count_name] = len(expected_tables[rows_name])
        expected_ledger[digest_name] = digest(expected_tables[rows_name])
        expected_ledger[rows_name] = expected_tables[rows_name]

    nonempty_alias_count = sum(
        row["exact_inclusion_alias_lemma_satisfied"] for row in cell_rows
    )
    empty_count = sum(row["signed_region_cell_state"] == EMPTY for row in cell_rows)
    uncovered_count = sum(
        row["Round286_coordinate_occupancy_count"] == 0
        and row["signed_region_cell_state"] != EMPTY
        for row in cell_rows
    )
    need(
        (nonempty_alias_count, empty_count, uncovered_count) == (5532, 544, 1540),
        "corrected alias/empty/uncovered census",
    )
    summary = {
        "Round275_region_count": len(region_rows),
        "Round286_coordinate_refinement_cell_count": len(cell_rows),
        "Round284_contained_region_inclusion_alias_witness_count": 2476,
        "Round286_nonempty_inclusion_alias_slice_count": nonempty_alias_count,
        "Round286_empty_opposite_side_coordinate_cell_count": empty_count,
        "Round286_nonempty_uncovered_slice_count": uncovered_count,
        "Round286_physically_fully_atom_covered_parent_count": 1292,
        "Round286_mixed_parent_count": 892,
        "valid_internal_artificial_physical_face_count": len(internal_face_rows),
        "connected_new_support_union_from_partial_parents": 892,
        "whole_Round275_disjoint_new_support_candidate_count": 9128,
        "total_conditional_new_Round275_support_count": len(union_rows),
        "R275_pairwise_outer_positive_overlap_pair_count": len(overlap_pairs),
        "R275_pairwise_actual_positive_overlap_pair_count": 0,
        "R283_logical_analytic_child_count_not_occurrence_nodes": 64,
        "cell_state_histogram": dict(sorted(cell_hist.items())),
        "region_disposition_histogram": dict(sorted(region_hist.items())),
        "alias_anchor_histogram": dict(sorted(alias_anchor_hist.items())),
        "contained_alias_target_unique_atom_count": len(contained_alias_targets),
        "table_sha256": {
            rows_name: expected_ledger[digest_name]
            for rows_name, _count_name, digest_name, _id_field, _count in TABLES
        },
        "ledger_object_sha256": digest(expected_ledger),
    }
    return expected_ledger, summary


def expected_strict_nonpromotion() -> dict[str, Any]:
    return {
        "new_expanded_occurrence_credit": 0,
        "occurrence_identity_collapse_credit": 0,
        "component_edge_credit": 0,
        "seam_edge_credit": 0,
        "maximality_credit": 0,
        "fibre_credit": 0,
        "global_disposition_credit": 0,
        "Jx_Jy_same_point_glue_credit": 0,
        "expanded_occurrences": 126468,
        "quotient": 63224,
        "Gate5": "10/18",
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def audit_candidate(
    ledger: dict[str, Any],
    result: dict[str, Any],
    expected_ledger: dict[str, Any],
    summary: dict[str, Any],
    check_file_bytes: bool = False,
) -> None:
    need(ledger["schema"] == LEDGER_SCHEMA, "candidate ledger schema")
    need(set(ledger) == set(expected_ledger), "candidate ledger field universe")
    for rows_name, count_name, digest_name, id_field, expected_count in TABLES:
        rows = verify_closed_rows(
            f"candidate {rows_name}",
            ledger[rows_name],
            id_field,
            expected_count,
            ledger[digest_name],
        )
        need(ledger[count_name] == expected_count, f"candidate {count_name}")
        need(
            [row[id_field] for row in rows]
            == sorted(row[id_field] for row in rows),
            f"candidate {rows_name}:canonical order",
        )
        need(rows == expected_ledger[rows_name], f"independent match:{rows_name}")
    need(ledger == expected_ledger, "complete expected ledger equality")

    need(result["schema"] == RESULT_SCHEMA, "candidate result schema")
    need(
        result["status"]
        == "PASS_ROUND287_PHYSICAL_SIDE_CORRECTED_TERMINAL_DISPOSITION_CONTRACT__"
        "10020_CONDITIONAL_NEW_SUPPORTS__ZERO_CREDIT",
        "candidate result status",
    )
    need(
        result["result_sha256"]
        == digest({key: value for key, value in result.items() if key != "result_sha256"}),
        "candidate result object digest",
    )
    need(
        result["pins"] == ROUND287_CANDIDATE_INPUT_PINS,
        "candidate input pins",
    )
    expected_census = {
        key: value for key, value in summary.items()
        if key not in {"table_sha256", "ledger_object_sha256"}
    }
    need(result["census"] == expected_census, "candidate exact census")

    lemma = result["inclusion_alias_lemma"]
    need(
        lemma
        == {
            "name": "EXACT_SAME_POSITIVE_OPEN_REGION_INCLUSION_ALIAS_V1",
            "rule":
                "If a nonempty R275 signed open support or R286 signed support slice "
                "is strictly included in one certified connected positive-open "
                "Round279 atom support under the same physical chart coordinates, "
                "and the complete ten-field signature, exact key, and owner agree, "
                "the smaller row is an exact representation-subcover witness for "
                "that atom occurrence identity and receives no new occurrence ID.",
            "box_containment_alone_is_never_sufficient": True,
            "signature_only_is_never_sufficient": True,
            "face_only_is_never_sufficient": True,
            "partial_overlap_is_never_sufficient": True,
            "does_not_collapse_two_existing_occurrence_ids": True,
            "conditional_on_containing_atom_identity_being_preserved_or_promoted":
                True,
        },
        "candidate inclusion-alias lemma",
    )
    need(
        result["physical_side_correction"]
        == {
            "Round286_coordinate_cells_do_not_by_themselves_prove_signed_support":
                True,
            "active_factor_extrema_replayed_for_every_graph_parent_cell": True,
            "coordinate_empty_rows_removed_from_alias_and_new_support_censuses": 544,
            "old_coordinate_uncovered_count": 1916,
            "corrected_nonempty_uncovered_count": 1540,
            "old_coordinate_mixed_parent_count": 1224,
            "corrected_physical_mixed_parent_count": 892,
            "old_coordinate_internal_face_count": 692,
            "corrected_valid_physical_internal_face_count": 648,
        },
        "candidate physical-side correction",
    )
    need(
        result["pairwise_uniqueness_contract"]
        == {
            "all_R275_outer_positive_overlap_pairs_exhausted": True,
            "only_opposite_sides_of_one_regular_graph_cell_survive_outer_test":
                True,
            "opposite_factor_sides_are_physically_disjoint": True,
            "no_cross_guard_or_return_branch_positive_volume_duplicate_found": True,
            "nonmatching_strict_complete_signatures_exclude_physical_open_overlap":
                True,
        },
        "candidate pairwise contract",
    )
    need(
        result["Round283_nonoccurrence_guard"]
        == {
            "logical_children": 64,
            "materialized_child_identity_ledger_present": False,
            "children_may_overlap_across_return_branches": True,
            "children_are_only_refinement_witnesses_to_be_bound_to_R275_regions":
                True,
            "occurrence_credit": 0,
        },
        "candidate Round283 guard",
    )
    dependency = result["Round288_dependency"]
    need(
        dependency["Round288_artifact_pinned_here"] is False
        and dependency["arithmetic_is_informational_and_not_credited"] is True
        and dependency["reported_additional_R204_exact_atom_alias_count"] == 640
        and dependency["reported_conditional_new_Round279_atom_count"] == 295336
        and dependency[
            "reported_combined_conditional_expanded_occurrence_total_if_Round288_freezes"
        ] == 431824,
        "candidate Round288 dependency",
    )
    need(
        len(result["issuance_blockers"]) == 5
        and all(isinstance(item, str) and item for item in result["issuance_blockers"]),
        "candidate issuance blockers",
    )
    need(
        result["strict_nonpromotion"] == expected_strict_nonpromotion(),
        "candidate strict nonpromotion",
    )
    need(
        result["ledger"]
        == {
            "filename": LEDGER.name,
            "region_row_count": 13788,
            "refinement_cell_row_count": 7616,
            "potential_new_support_union_row_count": 10020,
            "valid_internal_physical_face_row_count": 648,
            "mutually_exclusive_outer_overlap_pair_row_count": 3488,
            "ledger_object_sha256": summary["ledger_object_sha256"],
            "file_sha256": hashlib.sha256(
                deterministic_gzip_bytes(ledger)
            ).hexdigest(),
        },
        "candidate ledger/result binding",
    )
    if check_file_bytes:
        need(
            deterministic_gzip_bytes(ledger) == LEDGER.read_bytes(),
            "candidate deterministic gzip bytes",
        )
        need(
            canonical(result) + b"\n" == RESULT.read_bytes(),
            "candidate canonical result bytes",
        )


def reclose_candidate(ledger: dict[str, Any], result: dict[str, Any]) -> None:
    for rows_name, count_name, digest_name, _id_field, _expected_count in TABLES:
        for row in ledger[rows_name]:
            payload = dict(row)
            payload.pop("row_sha256", None)
            row["row_sha256"] = digest(payload)
        ledger[count_name] = len(ledger[rows_name])
        ledger[digest_name] = digest(ledger[rows_name])
    result["ledger"]["region_row_count"] = ledger["region_row_count"]
    result["ledger"]["refinement_cell_row_count"] = ledger[
        "refinement_cell_row_count"
    ]
    result["ledger"]["potential_new_support_union_row_count"] = ledger[
        "potential_new_support_union_row_count"
    ]
    result["ledger"]["valid_internal_physical_face_row_count"] = ledger[
        "valid_internal_physical_face_row_count"
    ]
    result["ledger"]["mutually_exclusive_outer_overlap_pair_row_count"] = ledger[
        "mutually_exclusive_outer_overlap_pair_row_count"
    ]
    result["ledger"]["ledger_object_sha256"] = digest(ledger)
    result["ledger"]["file_sha256"] = hashlib.sha256(
        deterministic_gzip_bytes(ledger)
    ).hexdigest()
    result["result_sha256"] = digest(
        {key: value for key, value in result.items() if key != "result_sha256"}
    )


def run_attacks(
    stored_ledger: dict[str, Any],
    stored_result: dict[str, Any],
    expected_ledger: dict[str, Any],
    summary: dict[str, Any],
) -> dict[str, Any]:
    def first_cell(state: str | None = None) -> dict[str, Any]:
        for row in attack_ledger["refinement_cell_rows"]:
            if state is None or row["signed_region_cell_state"] == state:
                return row
        raise VerificationError("attack cell selection")

    def first_region(disposition_fragment: str) -> dict[str, Any]:
        for row in attack_ledger["region_rows"]:
            if disposition_fragment in row["disposition"]:
                return row
        raise VerificationError("attack region selection")

    def mutate_empty_as_alias(_l: dict[str, Any], _r: dict[str, Any]) -> None:
        row = first_cell(EMPTY)
        row["exact_inclusion_alias_lemma_satisfied"] = True
        row["disposition"] = (
            "EXACT_INCLUSION_ALIAS_REPRESENTATION_SUBCOVER__"
            "CONDITIONAL_ON_CONTAINING_ATOM_IDENTITY"
        )

    def mutate_box_only_alias(_l: dict[str, Any], _r: dict[str, Any]) -> None:
        row = first_cell(FULL)
        row["complete_10_field_return_signature_sha256"] = "0" * 64

    def mutate_partial_as_whole_alias(_l: dict[str, Any], _r: dict[str, Any]) -> None:
        row = first_region("EXACT_REFINEMENT_MIXED")
        row["exact_inclusion_alias_lemma_satisfied"] = True
        row["Round284_classification"] = CONTAINED

    def mutate_invalid_face(_l: dict[str, Any], _r: dict[str, Any]) -> None:
        row = _l["valid_internal_physical_face_rows"][0]
        row["signed_region_face_state"] = EMPTY
        row["preserves_one_parent_local_occurrence_identity"] = False

    def mutate_round283_credit(_l: dict[str, Any], _r: dict[str, Any]) -> None:
        _r["Round283_nonoccurrence_guard"]["occurrence_credit"] = 1

    def mutate_weak_lemma(_l: dict[str, Any], _r: dict[str, Any]) -> None:
        _r["inclusion_alias_lemma"][
            "box_containment_alone_is_never_sufficient"
        ] = False

    attacks: list[
        tuple[
            str,
            Callable[[dict[str, Any], dict[str, Any]], None],
            bool,
        ]
    ] = [
        (
            "DROP_REGION_ROW",
            lambda l, r: l["region_rows"].pop(),
            True,
        ),
        (
            "DUPLICATE_REFINEMENT_CELL",
            lambda l, r: l["refinement_cell_rows"].append(
                deepcopy(l["refinement_cell_rows"][0])
            ),
            True,
        ),
        ("EMPTY_CELL_FORGED_AS_ALIAS", mutate_empty_as_alias, True),
        ("BOX_ONLY_ALIAS_WITH_WRONG_SIGNATURE", mutate_box_only_alias, True),
        ("PARTIAL_PARENT_FORGED_AS_WHOLE_ALIAS", mutate_partial_as_whole_alias, True),
        (
            "PROMOTE_CELL_OCCURRENCE_CREDIT",
            lambda l, r: first_cell().__setitem__("formal_occurrence_credit", 1),
            True,
        ),
        (
            "PROMOTE_UNION_COMPONENT_CREDIT",
            lambda l, r: l["potential_new_support_union_rows"][0].__setitem__(
                "formal_component_credit", 1
            ),
            True,
        ),
        ("FACE_ONLY_FALSE_CONNECTIVITY", mutate_invalid_face, True),
        (
            "DROP_MUTUALLY_EXCLUSIVE_PAIR",
            lambda l, r: l["mutually_exclusive_outer_overlap_pair_rows"].pop(),
            True,
        ),
        (
            "FORGE_ACTUAL_PAIR_OVERLAP",
            lambda l, r: l["mutually_exclusive_outer_overlap_pair_rows"][0].__setitem__(
                "exact_positive_physical_overlap", True
            ),
            True,
        ),
        (
            "FORGE_CONDITIONAL_NEW_SUPPORT_COUNT",
            lambda l, r: r["census"].__setitem__(
                "total_conditional_new_Round275_support_count", 10019
            ),
            True,
        ),
        (
            "FORGE_EMPTY_CELL_COUNT",
            lambda l, r: r["census"].__setitem__(
                "Round286_empty_opposite_side_coordinate_cell_count", 543
            ),
            True,
        ),
        ("ISSUE_ROUND283_CHILD_OCCURRENCE", mutate_round283_credit, True),
        ("WEAKEN_ALIAS_LEMMA_TO_BOX_ONLY", mutate_weak_lemma, True),
        (
            "PROMOTE_JX_JY_GLUE",
            lambda l, r: r["strict_nonpromotion"].__setitem__(
                "Jx_Jy_same_point_glue_credit", 1
            ),
            True,
        ),
        (
            "TAMPER_INPUT_PIN",
            lambda l, r: r["pins"].__setitem__(R275.name, "0" * 64),
            True,
        ),
        (
            "FORGE_LEDGER_ROW_HASH",
            lambda l, r: l["region_rows"][0].__setitem__("row_sha256", "0" * 64),
            False,
        ),
        (
            "FORGE_TABLE_DIGEST",
            lambda l, r: l.__setitem__("region_rows_sha256", "0" * 64),
            False,
        ),
        (
            "FORGE_RESULT_DIGEST",
            lambda l, r: r.__setitem__("result_sha256", "0" * 64),
            False,
        ),
        (
            "FORGE_UNCONDITIONAL_CM2_GO",
            lambda l, r: r.__setitem__("status", "PASS_UNCONDITIONAL_CM2_GO"),
            True,
        ),
    ]

    rejected: list[str] = []
    reclosed_ids: list[str] = []
    global attack_ledger
    for attack_id, mutate, should_reclose in attacks:
        attack_ledger = deepcopy(stored_ledger)
        attack_result = deepcopy(stored_result)
        mutate(attack_ledger, attack_result)
        if should_reclose:
            reclose_candidate(attack_ledger, attack_result)
            reclosed_ids.append(attack_id)
        try:
            audit_candidate(
                attack_ledger,
                attack_result,
                expected_ledger,
                summary,
                check_file_bytes=False,
            )
        except (
            VerificationError,
            KeyError,
            IndexError,
            StopIteration,
            TypeError,
            ValueError,
            ZeroDivisionError,
        ):
            rejected.append(attack_id)
        else:
            raise VerificationError(f"attack accepted:{attack_id}")
        del attack_ledger, attack_result
        gc.collect()
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_attacks_rejected": len(rejected) == len(attacks),
        "reclosed_attack_count": len(reclosed_ids),
        "reclosed_attack_ids": reclosed_ids,
        "rejected_attack_ids": rejected,
    }


def verify() -> dict[str, Any]:
    for name, expected in {**INPUT_PINS, **CANDIDATE_PINS}.items():
        need(file_sha256(HERE / name) == expected, f"pin:{name}")
    need(PRODUCER.stem not in sys.modules, "Round287 producer not preimported")

    frozen = load_frozen_inputs()
    ledger_a, summary_a = reconstruct_round287(frozen, REPLAY_SEEDS[0])
    ledger_b, summary_b = reconstruct_round287(frozen, REPLAY_SEEDS[1])
    need(ledger_a == ledger_b, "Round287 dual-seed reconstructed ledger")
    need(summary_a == summary_b, "Round287 dual-seed reconstruction summary")
    del ledger_b
    gc.collect()

    stored_ledger = read_gzip_json(LEDGER)
    stored_result = read_json(RESULT)
    audit_candidate(
        stored_ledger,
        stored_result,
        ledger_a,
        summary_a,
        check_file_bytes=True,
    )
    attacks = run_attacks(
        stored_ledger,
        stored_result,
        ledger_a,
        summary_a,
    )

    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status":
            "PASS_INDEPENDENT_ROUND287_TERMINAL_OCCURRENCE_DISPOSITION__"
            "13788_REGIONS__7616_SIGNED_CELLS__544_EMPTY__5532_ALIAS_SLICES__"
            "1540_UNCOVERED_SLICES__648_FACES__892_PARTIAL_UNIONS__"
            "10020_CONDITIONAL_NEW_SUPPORTS__3488_MUTUALLY_EXCLUSIVE_PAIRS__"
            "ZERO_CREDIT",
        "pins": {**INPUT_PINS, **CANDIDATE_PINS},
        "independence_contract": {
            "Round287_producer_imported_or_executed": False,
            "producer_treated_only_as_pinned_inert_bytes": True,
            "Round286_coordinate_refinement_rebuilt_from_R275_R279_R280_R284":
                True,
            "Round287_candidate_ledger_read_only_after_expected_rows_built": True,
            "active_factor_selector_and_extremal_rule_independently_spelled":
                True,
            "exact_coordinate_arithmetic": "fractions.Fraction",
            "pinned_interval_evaluator_sources": [
                R174_PRODUCER.name,
                R179_PRODUCER.name,
                R274_PRODUCER.name,
            ],
        },
        "reconstruction": {
            "Round174_Round179_guard_count": len(frozen["guards"]),
            "Round275_region_count": len(frozen["regions"]),
            "Round279_total_atom_count": 332016,
            "Round279_total_support_box_count": frozen["support_box_count"],
            "Round279_selected_atom_count": len(frozen["atoms"]),
            "Round284_partial_region_count": len(frozen["partial_ids"]),
            "Round286_cacheless_reconstruction":
                frozen["r286_summary"],
            **summary_a,
        },
        "dual_seed_replay": {
            "replay_seeds": list(REPLAY_SEEDS),
            "Round286_partial_region_order_independently_permuted": True,
            "Round287_cell_and_region_orders_independently_permuted": True,
            "canonical_reconstructed_ledgers_identical": True,
            "ledger_object_sha256_by_seed": {
                str(seed): summary_a["ledger_object_sha256"]
                for seed in REPLAY_SEEDS
            },
            "PYTHONHASHSEED_independent_output_contract": True,
        },
        "inclusion_alias_rejection_contract": {
            "box_only_aliases_accepted": 0,
            "signature_only_aliases_accepted": 0,
            "face_only_aliases_accepted": 0,
            "partial_overlap_aliases_accepted": 0,
            "complete_signature_exact_key_owner_chart_and_physical_t_required":
                True,
            "conditional_alias_credit_issued": 0,
        },
        "attacks": attacks,
        "zero_credit_contract": {
            "Round275_region_rows_zero_credit": True,
            "Round279_atom_rows_zero_credit": True,
            "Round280_binding_and_identity_rows_zero_credit": True,
            "Round283_children_occurrence_credit": 0,
            "Round284_overlap_disposition_credit": 0,
            "Round286_coordinate_refinement_credit": 0,
            "Round287_occurrence_ids_issued": 0,
            "Round287_component_edges_issued": 0,
            "Round287_seam_edges_issued": 0,
            "frozen_expanded_occurrences": 126468,
            "frozen_quotient_components": 63224,
        },
        "strict_nonpromotion": stored_result["strict_nonpromotion"],
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def atomic_write(path: Path, payload: bytes) -> None:
    target = path.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + target.name + ".", dir=target.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--seed",
        default="287071",
        help=(
            "Accepted for external PYTHONHASHSEED cold replay.  The verification "
            "itself performs both frozen reconstruction seeds."
        ),
    )
    args = parser.parse_args()
    value = verify()
    atomic_write(args.output, canonical(value) + b"\n")


if __name__ == "__main__":
    main()
