#!/usr/bin/env python3
"""Round290: close the 21,160 Round288 isolated-atom inner-support residuals.

This is deliberately a zero-credit producer.  Every accepted row contains a
strictly positive-volume rational box, strictly inside its Round279 atom
envelope.  The complete return signature is dynamically recomputed on the
whole box, and the source signed-region factor/graph side is independently
re-evaluated.  Point witnesses and whole-leaf envelopes are never accepted as
inner supports.
"""
from __future__ import annotations

import argparse
import collections
import gc
import gzip
import hashlib
import io
import json
import multiprocessing as mp
import os
import stat
import sys
import tempfile
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from typing import Any

from flint import ctx

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement_verifier as r179wall
import cm2_round270_source_g_outgoing_g_factor_signature_materialization as r270


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round290_source_g_isolated_atom_inner_support_closure"
OUTPUT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_inner_support_ledger.json.gz"
SCHEMA = "cm2.round290.source-g-isolated-atom-inner-support-closure.v1"
FIELDS = {
    "official_key_id",
    "official_key_ordinal",
    "official_key_row",
    "ordered_integer_wall_events",
    "outgoing_cell",
    "roof",
    "signed_wall_word",
    "source_chart",
    "target_chart",
    "target_lift",
}
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}

R174_ROWS = (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
)
R179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R182_ROWS = "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R204_CERT = (
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
)
R208_CERT = (
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
)
R269_CERT = (
    "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json"
)
R270_CERT = (
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json"
)
R271_CERT = (
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json"
)
R272_CERT = (
    "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json"
)
R279_ATOMS = "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
R288_RESULT = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_result.json"
)
R288_DISPOSITIONS = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "atom_dispositions.json.gz"
)

PINS = {
    R174_ROWS:
        "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R179_ROWS:
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R182_ROWS:
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    R204_CERT:
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R208_CERT:
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    R269_CERT:
        "472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3",
    R270_CERT:
        "72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea",
    R271_CERT:
        "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",
    R272_CERT:
        "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",
    R279_ATOMS:
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    R288_RESULT:
        "9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569",
    R288_DISPOSITIONS:
        "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
}

SOURCE_PINS = {
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py":
        "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    "cm2_round179_source_g_residual_tube_arrangement_verifier.py":
        "292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679",
    "cm2_round270_source_g_outgoing_g_factor_signature_materialization.py":
        "0ed0df9e4873e93b03ba11e8ad8ce6274d3b9de01875363c1a1818fdbc8867df",
}

SOURCE_SPECS = {
    269: (R269_CERT, "formal_direct_side_signature_ledger", "signed_region_row_id"),
    270: (R270_CERT, "formal_direct_side_signature_ledger", "signed_region_row_id"),
    271: (R271_CERT, "formal_side_signature_ledger", "signed_region_row_id"),
    272: (R272_CERT, "formal_side_signature_ledger", "signed_region_row_id"),
}

# The order is part of the finite deterministic search contract.  It starts
# with the exact extreme grid already used by Rounds271/272, then adds quarters.
SEARCH_FRACTIONS = (
    Q(1, 1_048_576),
    Q(1_048_575, 1_048_576),
    Q(1, 4_096),
    Q(4_095, 4_096),
    Q(1, 64),
    Q(63, 64),
    Q(1, 2),
    Q(1, 8),
    Q(7, 8),
    Q(1, 4),
    Q(3, 4),
)
SEARCH_CATALOGUE_SIZE = len(SEARCH_FRACTIONS) ** 3
UNRESOLVED_STATE = (
    "NEW_DISJOINT_CANDIDATE__"
    "POSITIVE_VOLUME_RATIONAL_INNER_SUPPORT_NOT_MATERIALIZED"
)


class ClosureError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ClosureError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def canonical(value: Any) -> bytes:
    return ENCODER.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def secure_raw(name: str, maximum: int = 1_200_000_000) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        path.parent == HERE
        and stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        f"regular pinned input:{name}",
    )
    payload = path.read_bytes()
    need(hashlib.sha256(payload).hexdigest() == PINS[name], f"file pin:{name}")
    return payload


def closed_json(name: str) -> dict[str, Any]:
    document = json.loads(secure_raw(name))
    need(
        isinstance(document, dict)
        and "result" in document
        and document.get("result_sha256") == digest(document["result"]),
        f"closed document:{name}",
    )
    return document["result"]


def direct_result(name: str) -> dict[str, Any]:
    result = json.loads(secure_raw(name))
    claimed = result.pop("result_sha256")
    need(claimed == digest(result), f"direct result digest:{name}")
    result["result_sha256"] = claimed
    return result


def gzip_json(name: str) -> dict[str, Any]:
    raw = secure_raw(name)
    with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as handle:
        decoded = handle.read(1_200_000_001)
    need(len(decoded) <= 1_200_000_000, f"gzip size:{name}")
    return json.loads(decoded)


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    rows = result[table]
    columns = result["row_column_schemas"][table]
    census = result["table_census_and_sha256"][table]
    need(
        len(rows) == census["row_count"] and digest(rows) == census["rows_sha256"],
        f"packed table:{table}",
    )
    return [dict(zip(columns, row, strict=True)) for row in rows]


def qbox(values: list[str] | tuple[str, ...]) -> tuple[Q, ...]:
    result = tuple(Q(value) for value in values)
    need(
        len(result) == 6
        and all(result[2 * axis] < result[2 * axis + 1] for axis in range(3)),
        "positive rational box",
    )
    return result


def box_text(box: tuple[Q, ...]) -> list[str]:
    return [str(value) for value in box]


def volume(box: tuple[Q, ...]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def strict_inside(inner: tuple[Q, ...], outer: tuple[Q, ...]) -> bool:
    return all(
        outer[2 * axis] < inner[2 * axis]
        < inner[2 * axis + 1] < outer[2 * axis + 1]
        for axis in range(3)
    )


def positive_overlap(left: tuple[Q, ...], right: tuple[Q, ...]) -> bool:
    return all(
        max(left[2 * axis], right[2 * axis])
        < min(left[2 * axis + 1], right[2 * axis + 1])
        for axis in range(3)
    )


def signature_payload(signature: dict[str, Any], chart: str) -> dict[str, Any]:
    result = {
        "official_key_id": signature["key"]["identifier"],
        "official_key_ordinal": signature["key"]["ordinal"],
        "official_key_row": signature["key"]["row"],
        "ordered_integer_wall_events": signature["events"],
        "outgoing_cell": signature["outgoing_cell"],
        "roof": signature["roof"],
        "signed_wall_word": list(signature["pattern"]),
        "source_chart": chart,
        "target_chart": signature["target_chart"],
        "target_lift": signature["target"],
    }
    need(set(result) == FIELDS, "dynamic ten-field signature")
    return result


def signature_from_geometry(row: dict[str, Any]) -> dict[str, Any]:
    result = {
        "official_key_id": row["official_key_id"],
        "official_key_ordinal": row["official_key_ordinal"],
        "official_key_row": row["official_key_row"],
        "ordered_integer_wall_events": row["ordered_integer_wall_events"],
        "outgoing_cell": row["outgoing_cell"],
        "roof": row["roof"],
        "signed_wall_word": row["signed_wall_word"],
        "source_chart": row["chart"],
        "target_chart": row["target_chart"],
        "target_lift": row["owner_target"],
    }
    need(set(result) == FIELDS, "geometry ten-field signature")
    return result


def close(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    need("row_sha256" not in result, "unclosed row")
    result["row_sha256"] = digest(result)
    return result


def ledger(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "cm2.round290.isolated-atom-inner-support-ledger.v1",
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest(
            [row["Round290_inner_support_row_id"] for row in rows]
        ),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
        "rows": rows,
    }


def gzip_bytes(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as handle:
        handle.write(canonical(value) + b"\n")
    return buffer.getvalue()


def atomic(path: Path, payload: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class IntervalNode:
    """Exact one-dimensional interval index for 3D overlap shortlisting."""

    __slots__ = ("center", "cross_lower", "cross_upper", "left", "right")

    def __init__(self, rows: list[tuple[Any, ...]]):
        midpoints = sorted((row[4][0] + row[4][1]) / 2 for row in rows)
        self.center = midpoints[len(midpoints) // 2]
        left: list[tuple[Any, ...]] = []
        right: list[tuple[Any, ...]] = []
        cross: list[tuple[Any, ...]] = []
        for row in rows:
            if row[4][1] <= self.center:
                left.append(row)
            elif row[4][0] >= self.center:
                right.append(row)
            else:
                cross.append(row)
        if not cross:
            ordered = sorted(rows, key=lambda row: (row[4][0], row[4][1], row[0]))
            middle = len(ordered) // 2
            cross = [ordered[middle]]
            left = ordered[:middle]
            right = ordered[middle + 1 :]
            self.center = (cross[0][4][0] + cross[0][4][1]) / 2
        self.cross_lower = sorted(cross, key=lambda row: row[4][0])
        self.cross_upper = sorted(cross, key=lambda row: row[4][1], reverse=True)
        self.left = IntervalNode(left) if left else None
        self.right = IntervalNode(right) if right else None

    def query(self, lower: Q, upper: Q, output: list[tuple[Any, ...]]) -> None:
        if upper <= self.center:
            for row in self.cross_lower:
                if row[4][0] >= upper:
                    break
                output.append(row)
            if self.left is not None:
                self.left.query(lower, upper, output)
        elif lower >= self.center:
            for row in self.cross_upper:
                if row[4][1] <= lower:
                    break
                output.append(row)
            if self.right is not None:
                self.right.query(lower, upper, output)
        else:
            output.extend(self.cross_lower)
            if self.left is not None:
                self.left.query(lower, upper, output)
            if self.right is not None:
                self.right.query(lower, upper, output)


# Initialized once before the fork pool.
TABLES: Any = None
TASKS: list[dict[str, Any]] = []
R198: Any = None
R195: Any = None
R186: Any = None
W_FACTOR_GEOMETRY: Any = None


def atlas_box(values: tuple[Q, ...], label: str) -> Any:
    return r174.atlas.AtlasBox(*values, 0, label)


def dynamic_signature(
    task: dict[str, Any], values: tuple[Q, ...], label: str
) -> dict[str, Any] | None:
    box = atlas_box(values, label)
    if r174.chart_domain_status(box) != "STRICT_INSIDE_TRUE_SOURCE_CHART":
        return None
    signature, _rejected = r174.dynamic_signature(
        task["source_chart"],
        box,
        task["owner_target"],
        TABLES,
    )
    if signature is None:
        return None
    payload = signature_payload(signature, task["source_chart"])
    if (
        payload != task["expected_signature"]
        or digest(payload) != task["expected_signature_sha256"]
        or payload["source_chart"] != task["source_chart"]
        or payload["target_lift"] != task["owner_target"]
        or payload["official_key_id"] != task["official_key_id"]
        or payload["official_key_ordinal"] != task["official_key_ordinal"]
        or payload["official_key_row"] != task["official_key_row"]
    ):
        return None
    return payload


def factor_side(
    task: dict[str, Any], values: tuple[Q, ...], label: str
) -> dict[str, Any] | None:
    """Independently validate the source signed-region factor/graph side."""

    round_number = task["source_round"]
    box = atlas_box(values, label)
    source = task["source_row"]
    if round_number in {269, 270}:
        R186.factor_geometry = (
            W_FACTOR_GEOMETRY if round_number == 269 else r270.factor_geometry_g
        )
        profiles = R198.selected_factor_profiles(task["collar"], box)
        hplus = profiles["HPLUS"]["selected_sign"]
        hminus = profiles["HMINUS"]["selected_sign"]
        if (
            hplus != source["HPLUS_sign"]
            or hminus != source["HMINUS_sign"]
            or hplus not in STRICT_SIGNS
            or hminus not in STRICT_SIGNS
        ):
            return None
        product_sign = R195.multiply_signs(hplus, hminus)
        if product_sign != source["region_factor_sign"]:
            return None
        return {
            "factor_model": (
                "PINNED_ROUND269_W_FACTOR_GEOMETRY"
                if round_number == 269
                else "PINNED_ROUND270_EXACT_G_FACTOR_GEOMETRY"
            ),
            "HPLUS_sign": hplus,
            "HMINUS_sign": hminus,
            "region_product_sign": product_sign,
            "graph_classification": source["graph_classification"],
            "active_factor_or_graph_side_strict_on_whole_inner_box": True,
        }

    collar = task["collar"]
    geometry = r179wall.independent_geometry(
        collar["chart"], collar["owner_target"], box
    )
    _, axis, wall_text = collar["reason_label"].split(":")
    wall = int(wall_text)
    source_value = geometry["source_x" if axis == "X" else "source_y"][0] - wall
    target_value = geometry["hit_x" if axis == "X" else "hit_y"][0] - wall
    source_sign = r179wall.arb_sign(source_value)
    target_sign = r179wall.arb_sign(target_value)
    if (
        source_sign != source["witness_source_factor_sign"]
        or target_sign != source["witness_target_factor_sign"]
        or source_sign not in STRICT_SIGNS
        or target_sign not in STRICT_SIGNS
    ):
        return None
    product_sign = R195.multiply_signs(source_sign, target_sign)
    if product_sign != source["region_product_sign"]:
        return None
    return {
        "factor_model": "PINNED_ROUND179_INDEPENDENT_WALL_FACTOR_GEOMETRY",
        "wall_axis": axis,
        "wall_coordinate": wall,
        "source_factor_sign": source_sign,
        "target_factor_sign": target_sign,
        "region_product_sign": product_sign,
        "graph_classification": source["graph_classification"],
        "active_factor_or_graph_side_strict_on_whole_inner_box": True,
    }


def centered_box(
    envelope: tuple[Q, ...],
    fractions: tuple[Q, Q, Q],
) -> tuple[Q, ...]:
    values: list[Q] = []
    for axis, fraction in enumerate(fractions):
        lower, upper = envelope[2 * axis : 2 * axis + 2]
        width = upper - lower
        center = lower + width * fraction
        # Strictly interior even for the 2^-20 extreme candidate.
        radius = min(center - lower, upper - center, width / (2**20)) / 4
        need(radius > 0, "positive catalogue radius")
        values.extend((center - radius, center + radius))
    result = tuple(values)
    need(strict_inside(result, envelope), "catalogue chart-guard interior")
    return result


def witness_expansion_box(
    envelope: tuple[Q, ...],
    point: tuple[Q, Q, Q],
    depth: int,
) -> tuple[Q, ...]:
    values: list[Q] = []
    for axis, center in enumerate(point):
        lower, upper = envelope[2 * axis : 2 * axis + 2]
        need(lower < center < upper, "point witness strictly interior")
        margin = min(center - lower, upper - center)
        radius = margin / (2 ** (depth + 1))
        need(radius > 0, "positive witness expansion radius")
        values.extend((center - radius, center + radius))
    result = tuple(values)
    need(strict_inside(result, envelope), "witness chart-guard interior")
    return result


def worker(index: int) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    task = TASKS[index]
    envelope = tuple(Q(value) for value in task["envelope"])
    found: tuple[
        tuple[Q, ...], dict[str, Any], dict[str, Any], dict[str, Any]
    ] | None = None

    if task["source_round"] in {271, 272}:
        point = tuple(Q(value) for value in task["source_row"]["witness_point"])
        need(len(point) == 3, "wall witness point")
        # Nested dyadic expansions are tried from largest to smallest.  The
        # first success is therefore the largest certified box in this family.
        for depth in range(0, 61):
            values = witness_expansion_box(envelope, point, depth)
            signature = dynamic_signature(
                task, values, f"round290-wall-signature:{index}:{depth}"
            )
            if signature is None:
                continue
            side = factor_side(task, values, f"round290-wall-side:{index}:{depth}")
            if side is None:
                continue
            found = (
                values,
                signature,
                side,
                {
                    "search_method": "NESTED_DYADIC_EXPANSION_AROUND_PINNED_STRICT_WITNESS",
                    "largest_successful_dyadic_box_depth": depth,
                    "maximum_permitted_dyadic_depth": 60,
                    "point_witness_used_only_as_search_center": True,
                    "point_witness_itself_used_as_inner_support": False,
                    "witness_generation_path":
                        (
                            f"{task['source_signature_row_id']}:"
                            f"nested-dyadic-depth:{depth}"
                        ),
                },
            )
            break
    else:
        ordinal = 0
        for fractions in product(SEARCH_FRACTIONS, repeat=3):
            values = centered_box(envelope, fractions)
            signature = dynamic_signature(
                task, values, f"round290-factor-signature:{index}:{ordinal}"
            )
            if signature is not None:
                side = factor_side(
                    task, values, f"round290-factor-side:{index}:{ordinal}"
                )
                if side is not None:
                    found = (
                        values,
                        signature,
                        side,
                        {
                            "search_method":
                                "FINITE_ORDERED_RATIONAL_FACTOR_SIDE_CATALOGUE",
                            "catalogue_size": SEARCH_CATALOGUE_SIZE,
                            "selected_catalogue_ordinal_zero_based": ordinal,
                            "selected_relative_center_fractions":
                                [str(value) for value in fractions],
                            "catalogue_order_sha256":
                                digest([str(value) for value in SEARCH_FRACTIONS]),
                            "failure_requires_complete_catalogue_exhaustion": True,
                            "witness_generation_path":
                                (
                                    f"{task['source_signature_row_id']}:"
                                    f"ordered-rational-catalogue-ordinal:{ordinal}"
                                ),
                        },
                    )
                    break
            ordinal += 1

    if found is None:
        return None, close(
            {
                "Round290_failure_row_id":
                    "round290-inner-support-failure:"
                    + digest(task["canonical_atom_id"]),
                "canonical_atom_id": task["canonical_atom_id"],
                "Round182_leaf_row_id": task["Round182_leaf_row_id"],
                "source_round": task["source_round"],
                "source_signature_row_id": task["source_signature_row_id"],
                "reason": (
                    "ALL_61_NESTED_DYADIC_WITNESS_EXPANSIONS_FAILED"
                    if task["source_round"] in {271, 272}
                    else
                    f"ALL_{SEARCH_CATALOGUE_SIZE}_ORDERED_RATIONAL_CANDIDATES_FAILED"
                ),
                "formal_occurrence_credit": 0,
                "formal_component_credit": 0,
                "formal_maximality_credit": 0,
            }
        )

    values, actual_signature, side_proof, search_proof = found
    need(
        volume(values) > 0
        and strict_inside(values, envelope)
        and r174.chart_domain_status(
            atlas_box(values, f"round290-final-chart-guard:{index}")
        )
        == "STRICT_INSIDE_TRUE_SOURCE_CHART"
        and actual_signature == task["expected_signature"]
        and digest(actual_signature) == task["expected_signature_sha256"],
        "accepted inner support",
    )
    row = close(
        {
            "Round290_inner_support_row_id":
                "round290-isolated-inner-support:"
                + digest(
                    [
                        task["canonical_atom_id"],
                        box_text(values),
                        task["expected_signature_sha256"],
                    ]
                ),
            "canonical_atom_id": task["canonical_atom_id"],
            "Round288_atom_disposition_row_id":
                task["Round288_atom_disposition_row_id"],
            "Round182_leaf_row_id": task["Round182_leaf_row_id"],
            "source_signature_row_id": task["source_signature_row_id"],
            "source_round": task["source_round"],
            "source_chart": task["source_chart"],
            "owner_target": task["owner_target"],
            "canonical_atom_frozen_support_envelope": task["envelope"],
            "Round182_leaf_exact_box": task["Round182_leaf_exact_box"],
            "exact_positive_volume_rational_inner_support_box": box_text(values),
            "exact_inner_support_volume": str(volume(values)),
            "strictly_inside_canonical_atom_frozen_support_envelope": True,
            "strictly_inside_original_Round182_leaf": True,
            "strictly_inside_true_source_chart_guard": True,
            "touches_half_open_or_excluded_face": False,
            "expected_complete_10_field_return_signature":
                task["expected_signature"],
            "dynamically_recomputed_complete_10_field_return_signature":
                actual_signature,
            "complete_10_field_return_signature_sha256":
                task["expected_signature_sha256"],
            "official_key_id": actual_signature["official_key_id"],
            "official_key_ordinal": actual_signature["official_key_ordinal"],
            "official_key_row": actual_signature["official_key_row"],
            "dynamic_signature_constant_on_whole_inner_box": True,
            "independent_source_signed_region_side_proof": side_proof,
            "deterministic_inner_support_search_proof": search_proof,
            "whole_leaf_envelope_used_as_inner_support": False,
            "point_witness_used_as_inner_support": False,
            "formal_new_occurrence_credit": 0,
            "formal_component_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
        }
    )
    return row, None


def existing_occurrences() -> list[tuple[Any, ...]]:
    rows: list[tuple[Any, ...]] = []
    round174 = closed_json(R174_ROWS)
    for row in unpack(round174, "resolved_3d_occurrence_rows"):
        signature = signature_from_geometry(row)
        box = qbox(row["box"])
        need(
            row["ambient_dimension"] == 3
            and row["physical_open_subset_positive"] is True
            and Q(row["coordinate_volume"]) == volume(box) > 0,
            "Round174 occurrence geometry",
        )
        rows.append(
            (
                row["row_id"],
                "ROUND174_RESOLVED",
                row["chart"],
                digest(signature),
                box,
            )
        )
    del round174

    round179 = closed_json(R179_ROWS)
    for row in unpack(round179, "resolved_3d_child_rows"):
        signature = signature_from_geometry(row)
        box = qbox(row["box"])
        need(
            row["ambient_dimension"] == 3
            and row["credit_kind"] == "LOCAL_POSITIVE_3D_OCCURRENCE_ONLY"
            and Q(row["coordinate_volume"]) == volume(box) > 0,
            "Round179 occurrence geometry",
        )
        rows.append(
            (
                row["row_id"],
                "ROUND179_RESOLVED",
                row["chart"],
                digest(signature),
                box,
            )
        )
    del round179

    round204 = closed_json(R204_CERT)
    rows204 = round204["formal_local_open_3D_region_ledger"]["rows"]
    for row in rows204:
        signature = signature_from_geometry(row)
        box = qbox(row["leaf_exact_box"])
        need(
            row["ambient_dimension"] == 3
            and row["strict_open_region"] is True
            and row["positive_coordinate_volume"] is True
            and row["formal_local_signature_credit"] == 1,
            "Round204 occurrence geometry",
        )
        rows.append(
            (
                row["region_row_id"],
                "ROUND204_REGION",
                row["chart"],
                digest(signature),
                box,
            )
        )
    del round204

    round208 = closed_json(R208_CERT)
    rows208 = round208["formal_local_open_3D_signature_ledger"]["rows"]
    for row in rows208:
        signature = row["local_return_signature"]
        box = qbox(row["Round182_leaf_box"])
        need(
            row["strict_open_3D_region_exists"] is True
            and row["formal_local_open_3D_signature_credit"] == 1,
            "Round208 occurrence geometry",
        )
        rows.append(
            (
                row["region_row_id"],
                "ROUND208_REGION",
                signature["source_chart"],
                digest(signature),
                box,
            )
        )
    need(
        collections.Counter(row[1] for row in rows)
        == {
            "ROUND174_RESOLVED": 72_500,
            "ROUND179_RESOLVED": 17_192,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36_040,
        },
        "complete existing occurrence frontier",
    )
    return rows


def build(seed: int, processes: int) -> tuple[dict[str, Any], dict[str, Any]]:
    global TABLES, TASKS, R198, R195, R186, W_FACTOR_GEOMETRY
    del seed
    need(1 <= processes <= 64, "process count")
    for name in PINS:
        need(file_sha256(HERE / name) == PINS[name], f"input pin:{name}")
    for name, expected in SOURCE_PINS.items():
        need(file_sha256(HERE / name) == expected, f"source pin:{name}")
    ctx.prec = 256
    need(ctx.prec == 256, "fixed FLINT precision")

    chain = r270.r207.check_inputs()
    R198 = r270.r207.r203.r198
    R195 = R198.r195
    R186 = R195.r191.r189.r188.r186
    W_FACTOR_GEOMETRY = R186.factor_geometry
    factor_r174 = R186.r179.r174
    need(
        factor_r174.__name__
        == "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier",
        "pinned factor evaluator Round174 module",
    )
    r270.R174 = factor_r174
    r270.R195 = R195
    TABLES = r174.registry_tables(r174.load_inputs()["gate5"])

    r288 = direct_result(R288_RESULT)
    need(
        r288["status"].startswith("PASS_ROUND288_CACHELESS_ATOM_IDENTITY_GATE_AUDIT")
        and r288["census"]["isolated_new_candidate_inner_support_residual_count"]
        == 21_160
        and r288["census"]["conditional_occurrence_total_if_all_inner_supports_later_pass"]
        == 421_804
        and r288["strict_nonpromotion"]["formal_new_expanded_occurrence_credit"] == 0,
        "Round288 frozen residual baseline",
    )

    atom_document = gzip_json(R279_ATOMS)
    atoms = atom_document["rows"]
    need(
        len(atoms) == atom_document["row_count"] == 332_016
        and digest(atoms) == atom_document["rows_sha256"],
        "Round279 atom ledger",
    )
    atom_by_id = {row["canonical_atom_id"]: row for row in atoms}
    need(len(atom_by_id) == 332_016, "unique Round279 atoms")

    disposition_document = gzip_json(R288_DISPOSITIONS)
    dispositions = disposition_document["rows"]
    need(
        len(dispositions) == disposition_document["row_count"] == 332_016
        and digest(dispositions) == disposition_document["rows_sha256"],
        "Round288 disposition ledger",
    )
    unresolved = [
        row
        for row in dispositions
        if row["occurrence_identity_disposition"] == UNRESOLVED_STATE
    ]
    need(len(unresolved) == 21_160, "Round288 unresolved disposition census")

    round182 = closed_json(R182_ROWS)
    leaves = {row["row_id"]: row for row in unpack(round182, "collar_leaf_rows")}
    collars = {
        row["Round179_occurrence_row_id"]: row
        for row in unpack(round182, "collar_occurrence_rows")
    }
    need(len(leaves) == 202_840 and len(collars) == 54_220, "Round182 census")
    del round182

    source_maps: dict[int, dict[str, dict[str, Any]]] = {}
    for round_number, (name, ledger_name, id_field) in SOURCE_SPECS.items():
        result = closed_json(name)
        rows = result[ledger_name]["rows"]
        need(
            len(rows) == result[ledger_name]["row_count"]
            and digest(rows) == result[ledger_name]["rows_sha256"],
            f"source ledger:{round_number}",
        )
        source_maps[round_number] = {row[id_field]: row for row in rows}
        need(len(source_maps[round_number]) == len(rows), f"unique source:{round_number}")

    TASKS = []
    source_round_histogram: collections.Counter[int] = collections.Counter()
    for disposition in unresolved:
        stored = dict(disposition)
        row_hash = stored.pop("row_sha256")
        need(digest(stored) == row_hash, "Round288 disposition row closure")
        atom = atom_by_id[disposition["canonical_atom_id"]]
        need(
            atom["source_rounds"] == disposition["source_rounds"]
            and len(atom["source_rounds"]) == 1
            and len(atom["source_signature_row_ids"]) == 1
            and len(atom["frozen_true_support_boxes"]) == 1,
            "isolated atom singleton provenance",
        )
        round_number = atom["source_rounds"][0]
        source_id = atom["source_signature_row_ids"][0]
        source = source_maps[round_number][source_id]
        leaf = leaves[atom["Round182_leaf_row_id"]]
        collar = collars[leaf["occurrence_row_id"]]
        signature = atom["complete_10_field_return_signature"]
        envelope = qbox(atom["frozen_true_support_boxes"][0])
        need(
            round_number in SOURCE_SPECS
            and source["Round182_leaf_row_id"] == leaf["row_id"]
            and source["local_return_signature"] == signature
            and digest(signature) == atom["complete_10_field_return_signature_sha256"]
            and disposition["source_chart"] == atom["source_chart"]
            == collar["chart"] == signature["source_chart"]
            and disposition["owner_target"] == atom["owner_target"]
            == collar["owner_target"] == signature["target_lift"]
            and envelope == qbox(leaf["box"])
            and volume(envelope) > 0,
            "isolated source/leaf/atom binding",
        )
        TASKS.append(
            {
                "canonical_atom_id": atom["canonical_atom_id"],
                "Round288_atom_disposition_row_id":
                    disposition["Round288_atom_disposition_row_id"],
                "Round182_leaf_row_id": leaf["row_id"],
                "source_round": round_number,
                "source_signature_row_id": source_id,
                "source_row": source,
                "collar": collar,
                "source_chart": atom["source_chart"],
                "owner_target": atom["owner_target"],
                "envelope": atom["frozen_true_support_boxes"][0],
                "Round182_leaf_exact_box": leaf["box"],
                "expected_signature": signature,
                "expected_signature_sha256":
                    atom["complete_10_field_return_signature_sha256"],
                "official_key_id": signature["official_key_id"],
                "official_key_ordinal": signature["official_key_ordinal"],
                "official_key_row": signature["official_key_row"],
            }
        )
        source_round_histogram[round_number] += 1
    need(
        source_round_histogram == {269: 3_968, 270: 6_728, 271: 10_448, 272: 16},
        "isolated source-round census",
    )
    del dispositions, unresolved, atoms, atom_by_id, leaves, collars, source_maps
    gc.collect()

    rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    with mp.get_context("fork").Pool(processes) as pool:
        for accepted, failed in pool.imap_unordered(
            worker, range(len(TASKS)), chunksize=8
        ):
            if accepted is not None:
                rows.append(accepted)
            if failed is not None:
                failures.append(failed)
            done = len(rows) + len(failures)
            if done and done % 2_000 == 0:
                print(
                    json.dumps(
                        {
                            "round290_progress": done,
                            "accepted": len(rows),
                            "failed": len(failures),
                            "total": len(TASKS),
                        },
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                    flush=True,
                )
    rows.sort(key=lambda row: row["Round290_inner_support_row_id"])
    failures.sort(key=lambda row: row["Round290_failure_row_id"])
    need(len(rows) + len(failures) == 21_160, "worker partition")

    # Re-audit the full pre-existing frontier on the newly materialized boxes.
    existing = existing_occurrences()
    existing_by_chart: dict[str, list[tuple[Any, ...]]] = collections.defaultdict(list)
    for item in existing:
        existing_by_chart[item[2]].append(item)
    existing_trees = {
        chart: IntervalNode(items) for chart, items in existing_by_chart.items()
    }
    existing_shortlist = 0
    existing_overlaps: list[tuple[str, str, str, str]] = []
    row_boxes: list[tuple[str, str, str, str, tuple[Q, ...]]] = []
    for row in rows:
        box = qbox(row["exact_positive_volume_rational_inner_support_box"])
        row_boxes.append(
            (
                row["canonical_atom_id"],
                "ROUND290_INNER_SUPPORT",
                row["source_chart"],
                row["complete_10_field_return_signature_sha256"],
                box,
            )
        )
        candidates: list[tuple[Any, ...]] = []
        existing_trees[row["source_chart"]].query(box[0], box[1], candidates)
        existing_shortlist += len(candidates)
        for item in candidates:
            if positive_overlap(box, item[4]):
                existing_overlaps.append(
                    (
                        row["canonical_atom_id"],
                        item[0],
                        row["complete_10_field_return_signature_sha256"],
                        item[3],
                    )
                )
    need(not existing_overlaps, "Round290 box/existing-frontier positive overlap")

    # Exact same-chart, same-signature pairwise duplicate audit.
    groups: dict[tuple[str, str], list[tuple[Any, ...]]] = collections.defaultdict(list)
    for item in row_boxes:
        groups[(item[2], item[3])].append(item)
    pair_shortlist = 0
    duplicate_pairs: list[tuple[str, str]] = []
    for items in groups.values():
        ordered = sorted(items, key=lambda item: (item[4][0], item[4][1], item[0]))
        active: list[tuple[Any, ...]] = []
        for item in ordered:
            active = [other for other in active if other[4][1] > item[4][0]]
            for other in active:
                pair_shortlist += 1
                if positive_overlap(item[4], other[4]):
                    duplicate_pairs.append((other[0], item[0]))
            active.append(item)
    need(not duplicate_pairs, "Round290 pairwise positive-volume duplicate")

    method_histogram: collections.Counter[str] = collections.Counter()
    factor_model_histogram: collections.Counter[str] = collections.Counter()
    selected_ordinal_histogram: collections.Counter[int] = collections.Counter()
    wall_depth_histogram: collections.Counter[int] = collections.Counter()
    for row in rows:
        method = row["deterministic_inner_support_search_proof"]["search_method"]
        method_histogram[method] += 1
        model = row["independent_source_signed_region_side_proof"]["factor_model"]
        factor_model_histogram[model] += 1
        proof = row["deterministic_inner_support_search_proof"]
        if "selected_catalogue_ordinal_zero_based" in proof:
            selected_ordinal_histogram[proof["selected_catalogue_ordinal_zero_based"]] += 1
        if "largest_successful_dyadic_box_depth" in proof:
            wall_depth_histogram[proof["largest_successful_dyadic_box_depth"]] += 1

    attachment = ledger(rows)
    factor_failure_count = sum(
        row["source_round"] in {269, 270} for row in failures
    )
    wall_failure_count = sum(
        row["source_round"] in {271, 272} for row in failures
    )
    result = {
        "schema": SCHEMA,
        "status": (
            (
                "PASS_ROUND290_ALL_21160_ISOLATED_ATOMS_HAVE_STRICT_"
                "POSITIVE_VOLUME_RATIONAL_INNER_SUPPORTS__"
                "FULL_DYNAMIC_SIGNATURE_AND_ACTIVE_SIDE_RECHECK__"
                "EXISTING_AND_PAIRWISE_OVERLAP_RESIDUAL_ZERO__ZERO_CREDIT"
            )
            if not failures
            else (
                "FAIL_CLOSED_ROUND290_ISOLATED_INNER_SUPPORT_RESIDUAL_"
                f"{len(failures)}__ZERO_CREDIT"
            )
        ),
        "input_file_pins": dict(sorted(PINS.items())),
        "input_source_pins": dict(sorted(SOURCE_PINS.items())),
        "census": {
            "Round288_isolated_inner_support_residual_input_count": 21_160,
            "strict_positive_volume_inner_support_count": len(rows),
            "failure_residual_count": len(failures),
            "source_round_histogram": {
                str(key): value for key, value in sorted(source_round_histogram.items())
            },
            "search_method_histogram": dict(sorted(method_histogram.items())),
            "factor_model_histogram": dict(sorted(factor_model_histogram.items())),
            "largest_successful_wall_dyadic_depth_histogram": {
                str(key): value for key, value in sorted(wall_depth_histogram.items())
            },
            "factor_catalogue_selected_ordinal_histogram_sha256":
                digest(sorted(selected_ordinal_histogram.items())),
            "factor_catalogue_size_per_task": SEARCH_CATALOGUE_SIZE,
            "factor_catalogue_failure_residual_count": factor_failure_count,
            "wall_dyadic_expansion_failure_residual_count": wall_failure_count,
            "dynamic_signature_constant_whole_box_count": len(rows),
            "independent_active_factor_or_graph_side_whole_box_count": len(rows),
            "strict_chart_guard_interior_count": len(rows),
            "half_open_or_excluded_face_touch_count": 0,
            "existing_Round266_occurrence_count": len(existing),
            "existing_frontier_interval_shortlist_comparison_count":
                existing_shortlist,
            "existing_frontier_positive_volume_overlap_count": 0,
            "same_chart_same_signature_pairwise_shortlist_comparison_count":
                pair_shortlist,
            "same_chart_same_signature_positive_volume_duplicate_pair_count": 0,
            "conditional_distinct_new_atom_total": 295_336,
            "conditional_occurrence_total_if_Round288_and_Round290_later_promoted":
                421_804,
        },
        "support_contract": {
            "every_inner_box_has_strictly_positive_exact_rational_volume": True,
            "every_inner_box_is_strictly_inside_its_atom_envelope": True,
            "every_inner_box_is_strictly_inside_the_chart_guard": True,
            "no_inner_box_touches_a_half_open_or_excluded_face": True,
            "complete_ten_field_signature_recomputed_on_every_whole_box": True,
            "official_exact_key_recomputed_on_every_whole_box": True,
            "owner_target_and_source_chart_recomputed_and_equal": True,
            "source_signed_region_active_factor_or_graph_side_rechecked_separately":
                True,
            "return_signature_coincidence_alone_never_proves_signed_region_side":
                True,
            "whole_leaf_envelope_never_used_as_inner_support": True,
            "point_witness_never_used_as_inner_support": True,
            "Round269_Round270_search_is_finite_ordered_and_seed_inert": True,
            "Round271_Round272_nested_dyadic_expansion_records_largest_successful_box_depth":
                True,
            "existing_frontier_overlap_reaudited": True,
            "same_chart_same_signature_pairwise_duplicate_reaudited": True,
            "any_search_failure_is_preserved_verbatim_and_receives_zero_credit":
                True,
        },
        "strict_nonpromotion": {
            "formal_new_expanded_occurrence_credit": 0,
            "formal_occurrence_alias_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "maximality_credit": 0,
            "fibre_credit": 0,
            "global_disposition_credit": 0,
            "true_seam_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "expanded_occurrences": 126_468,
            "quotient_components": 63_224,
            "maximality": "0/63224",
            "exact_key_fibres": "0/116",
            "global_dispositions": "0/224580",
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": [
            "Run a standalone cacheless Round290 verifier without importing or executing this producer.",
            "Keep the 21,160 rows zero-credit until that verifier independently rebuilds every inner box, dynamic signature, signed-region side and overlap audit.",
            "Combine a verified Round288 corridor partition and verified Round290 isolated partition only in a later explicit occurrence-promotion round.",
            "The 152 true seams, final DSU, maximality, 116 fibres and 224,580 dispositions remain downstream gates.",
        ],
        "inner_support_ledger": {
            "filename": LEDGER.name,
            "row_count": attachment["row_count"],
            "rows_sha256": attachment["rows_sha256"],
            "row_ids_sha256": attachment["row_ids_sha256"],
            "row_hashes_sha256": attachment["row_hashes_sha256"],
        },
        "failure_residual_ledger": {
            "row_count": len(failures),
            "rows_sha256": digest(failures),
            "row_ids_sha256": digest(
                [row["Round290_failure_row_id"] for row in failures]
            ),
            "row_hashes_sha256": digest(
                [row["row_sha256"] for row in failures]
            ),
            "every_row_closed_by_own_SHA256": True,
            "rows": failures,
        },
        "provenance": {
            "producer_sha256": file_sha256(Path(__file__).resolve()),
            "python_version": sys.version.split()[0],
            "python_flint_version": str(ctx),
            "precision_bits": ctx.prec,
            "process_count": processes,
            "seed_affects_output": False,
            "cache_or_pickle_input_used": False,
            "pinned_evaluator_chain": chain,
        },
    }
    return result, attachment


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=290071)
    parser.add_argument("--processes", type=int, default=min(40, mp.cpu_count()))
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    args = parser.parse_args()
    result, attachment = build(args.seed, args.processes)
    payload = gzip_bytes(attachment)
    result["inner_support_ledger"]["file_sha256"] = hashlib.sha256(payload).hexdigest()
    result["result_sha256"] = digest(result)
    atomic(args.ledger, payload)
    atomic(args.output, canonical(result) + b"\n")
    print(result["status"])
    print("result_sha256=" + result["result_sha256"])
    print("inner_support_ledger_sha256=" + hashlib.sha256(payload).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
