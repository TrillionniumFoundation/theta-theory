#!/usr/bin/env python3
"""Round299C zero-credit R292-to-registry support boundary sweep.

This diagnostic compares every one of the 11,852 exact Round292 cells with
the true rational support box of each non-Round292 registry entry:

* 126,468 preserved Round174/Round179/Round204/Round208 occurrences;
* 295,336 promoted Round288 atom occurrences.

The 9,404 Round292 occurrences are represented by their 10,252 uncovered
cells; the 1,600 occupied Round292 cells are retained as representation cells
of preserved occurrences.  Round292-to-Round292 faces are deliberately not
re-enumerated here; they are pinned from Round299A/B.

Boundary joins use exact ``Fraction`` endpoint keys and a per-boundary exact
interval tree on one tangential axis.  This avoids a quadratic scan inside
large dyadic boundary buckets.  A graph-constrained Round292 endpoint is
replayed with the Round299B signed-factor procedure.  All outputs remain
diagnostic candidates with zero formal credit.

Run with python-flint, for example:

    uv run --with python-flint python <this-file>
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import sys
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import ctx


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cm2_round292_source_g_r287_registry_overlap_exhaustion_probe as r292
import cm2_round299_source_g_r292_complete_common_face_frontier_diagnostic_probe as r299a
import cm2_round299b_source_g_r292_signed_support_face_replay_diagnostic as r299b


PREFIX = "cm2_round299c_source_g_r292_registry_support_boundary_face_diagnostic"
OUTPUT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"

R174 = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
R179 = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R204 = "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
R208 = "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
R288 = "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_atom_dispositions.json.gz"
R292P = "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe.py"
R299AP = "cm2_round299_source_g_r292_complete_common_face_frontier_diagnostic_probe.py"
R299AL = "cm2_round299_source_g_r292_complete_common_face_frontier_diagnostic_probe_ledger.json.gz"
R299BP = "cm2_round299b_source_g_r292_signed_support_face_replay_diagnostic.py"
R299BL = "cm2_round299b_source_g_r292_signed_support_face_replay_diagnostic_ledger.json.gz"
R295A = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "physical_witness_incidence_binding_ledger.json.gz"
)
R296 = "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_edge_ledger.json.gz"
R297 = "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_edge_ledger.json.gz"

PINS = {
    R174: "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R179: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R204: "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    R208: "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    R288: "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    R292P: "69078405b39dff3e924630ffbc9fbe35c14e4114e1e33c946b9ab44fe26e8c4c",
    R299AP: "058c00d41e9bc7f8656fe7f03740ecc3e27e844d0abb70ca9f9bfb09cbbac113",
    R299AL: "b9de98c7ccb3051ea7af3070e1eb62ce059d21f0b22b9b3f5007c1847c667845",
    R299BP: "5d6ad6df836a58c6761d2be7c8b1fb65af051ce0203dd071ea5c18e09fa86cfc",
    R299BL: "f7973edfe005435e162527d8eb3be98284963718146bd99812c243702d2e6e50",
    R295A: "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R296: "1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7",
    R297: "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
}

SCHEMA = "cm2.round299c.source-g-r292-registry-support-boundary-face-diagnostic.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
ENC = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
)
ctx.prec = 768


def canonical(value: Any) -> bytes:
    return ENC.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            result.update(chunk)
    return result.hexdigest()


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def read_gzip(name: str) -> dict[str, Any]:
    path = HERE / name
    need(file_sha256(path) == PINS[name], f"pin:{name}")
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    result = dict(payload)
    result["row_sha256"] = digest(result)
    return result


def deterministic_gzip_bytes(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=buffer, compresslevel=9, mtime=0
    ) as handle:
        handle.write(canonical(value))
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


def pair(left: str, right: str) -> tuple[str, str]:
    need(left != right, "nonself pair")
    return tuple(sorted((left, right)))


def load_r292_cells() -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    regions = r299a.load_regions()
    r287_regions, r287_cells = r299a.load_r287()
    refined_occurrence = r299a.load_r294_refined_occurrence_map()
    cells = r299a.load_r292_cells(
        regions,
        r287_regions,
        r287_cells,
        refined_occurrence,
    )
    return cells, regions


def load_base_registry_supports() -> list[dict[str, Any]]:
    rows = r292.load_preserved_occurrences() + r292.load_new_atoms()
    need(
        len(rows) == 421_804
        and Counter(row["occurrence_source"] for row in rows)
        == {
            "ROUND174_RESOLVED": 72_500,
            "ROUND179_RESOLVED": 17_192,
            "ROUND204_REGION": 736,
            "ROUND208_REGION": 36_040,
            "ROUND288_NEW_ATOM_CANDIDATE": 295_336,
        },
        "base registry support census",
    )
    need(
        all(len(row["support_boxes"]) == 1 for row in rows),
        "one pinned true support box per base registry entry",
    )
    return rows


def query_key(
    cell: dict[str, Any],
    axis: int,
    base_endpoint: str,
) -> tuple[str, int, int, Q, str]:
    need(base_endpoint in {"LOW", "HIGH"}, "base endpoint direction")
    value = (
        cell["box"][2 * axis + 1]
        if base_endpoint == "LOW"
        else cell["box"][2 * axis]
    )
    return (
        cell["source_chart"],
        cell["physical_t_sign"],
        axis,
        value,
        base_endpoint,
    )


def tangent_rectangle(
    box: tuple[Q, ...], axis: int
) -> tuple[Q, Q, Q, Q]:
    others = [current for current in range(3) if current != axis]
    return (
        box[2 * others[0]],
        box[2 * others[0] + 1],
        box[2 * others[1]],
        box[2 * others[1] + 1],
    )


def pseudo_box(rectangle: tuple[Q, Q, Q, Q]) -> tuple[Q, ...]:
    # PIntervalNode indexes positions 2:4.  The leading interval is unused.
    return (
        Q(0),
        Q(1),
        rectangle[0],
        rectangle[1],
        rectangle[2],
        rectangle[3],
    )


def build_boundary_buckets(
    cells: list[dict[str, Any]],
    base_rows: list[dict[str, Any]],
) -> tuple[
    dict[tuple[str, int, int, Q, str], list[int]],
    dict[tuple[str, int, int, Q, str], list[tuple[tuple[Q, ...], dict[str, Any]]]],
    dict[str, Any],
]:
    queries: dict[tuple[str, int, int, Q, str], list[int]] = defaultdict(list)
    for cell_index, cell in enumerate(cells):
        for axis in range(3):
            queries[query_key(cell, axis, "LOW")].append(cell_index)
            queries[query_key(cell, axis, "HIGH")].append(cell_index)

    buckets: dict[
        tuple[str, int, int, Q, str],
        list[tuple[tuple[Q, ...], dict[str, Any]]],
    ] = defaultdict(list)
    transformed_box_count = 0
    shortlisted_endpoint_count = 0
    source_histogram: Counter[str] = Counter()
    for source in base_rows:
        rational_box = source["support_boxes"][0]
        for sign in (-1, 1):
            transformed = r292.transformed_registry_box(rational_box, sign)
            if transformed is None:
                continue
            transformed_box_count += 1
            source_histogram[source["occurrence_source"]] += 1
            for axis in range(3):
                for base_endpoint, coordinate_index in (
                    ("LOW", 2 * axis),
                    ("HIGH", 2 * axis + 1),
                ):
                    key = (
                        source["source_chart"],
                        sign,
                        axis,
                        transformed[coordinate_index],
                        base_endpoint,
                    )
                    if key not in queries:
                        continue
                    shortlisted_endpoint_count += 1
                    rectangle = tangent_rectangle(transformed, axis)
                    buckets[key].append(
                        (
                            pseudo_box(rectangle),
                            {
                                "occurrence_id": source["occurrence_id"],
                                "occurrence_source": source["occurrence_source"],
                                "signature_sha256": source["signature_sha256"],
                                "transformed_support_box": transformed,
                                "rational_support_box": rational_box,
                                "tangent_rectangle": rectangle,
                            },
                        )
                    )
    need(
        transformed_box_count == 421_804,
        "one signed transformed support per base occurrence",
    )
    return queries, buckets, {
        "base_registry_occurrence_count": len(base_rows),
        "base_registry_transformed_support_box_count": transformed_box_count,
        "base_support_source_histogram": dict(sorted(source_histogram.items())),
        "Round292_boundary_query_bucket_count": len(queries),
        "nonempty_base_boundary_bucket_count": len(buckets),
        "shortlisted_base_support_endpoint_count": shortlisted_endpoint_count,
    }


def exact_face(
    cell_box: tuple[Q, ...],
    base_box: tuple[Q, ...],
    axis: int,
    base_endpoint: str,
) -> tuple[Q, ...] | None:
    if base_endpoint == "LOW":
        if cell_box[2 * axis + 1] != base_box[2 * axis]:
            return None
        value = cell_box[2 * axis + 1]
    else:
        if base_box[2 * axis + 1] != cell_box[2 * axis]:
            return None
        value = cell_box[2 * axis]
    result: list[Q] = []
    for current in range(3):
        if current == axis:
            result.extend((value, value))
            continue
        lower = max(cell_box[2 * current], base_box[2 * current])
        upper = min(cell_box[2 * current + 1], base_box[2 * current + 1])
        if not lower < upper:
            return None
        result.extend((lower, upper))
    return tuple(result)


def signed_face_disposition(
    cell: dict[str, Any],
    face: tuple[Q, ...],
    axis: int,
    regions: dict[str, dict[str, Any]],
) -> tuple[str, list[dict[str, Any]], dict[str, Any] | None]:
    if "REGULAR_GRAPH_CONSTRAINED" not in cell[
        "inherited_signed_support_state"
    ]:
        return (
            "FULL_ROUND292_SUPPORT__COORDINATE_FACE_CANDIDATE",
            [],
            None,
        )
    region = regions[cell["region_id"]]
    precision_replays = []
    for bits in r299b.REPLAY_BITS:
        state, extrema, enclosure = r299b.signed_state(
            region, face, cell["physical_t_sign"], bits
        )
        precision_replays.append(
            {
                "dyadic_sqrt_outer_enclosure_bits": bits,
                "signed_t_rational_outer_enclosure": [
                    qstr(enclosure[0]),
                    qstr(enclosure[1]),
                ],
                "signed_region_face_state": state,
                "active_factor_extremal_signs": extrema,
            }
        )
    states = {
        replay["signed_region_face_state"] for replay in precision_replays
    }
    extrema = {
        tuple(replay["active_factor_extremal_signs"])
        for replay in precision_replays
    }
    need(len(states) == len(extrema) == 1, "precision-stable registry face")
    state = precision_replays[-1]["signed_region_face_state"]
    if state == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL":
        return (
            "GRAPH_CONSTRAINED_ROUND292_SUPPORT_EMPTY_ON_FACE__EXCLUDED",
            precision_replays,
            None,
        )
    need(
        state in {"FULL_DESIRED_SIDE_SUPPORT", "CLIPPED_DESIRED_SIDE_SUPPORT"},
        "decisive graph face state",
    )
    witness = r299b.strict_desired_witness(
        region, face, axis, cell["physical_t_sign"]
    )
    return (
        "GRAPH_CONSTRAINED_ROUND292_SUPPORT_POSITIVE_AREA_FACE_CERTIFIED",
        precision_replays,
        witness,
    )


def enumerate_faces(
    cells: list[dict[str, Any]],
    regions: dict[str, dict[str, Any]],
    queries: dict[tuple[str, int, int, Q, str], list[int]],
    buckets: dict[
        tuple[str, int, int, Q, str],
        list[tuple[tuple[Q, ...], dict[str, Any]]],
    ],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    interval_tree_query_count = 0
    interval_tree_candidate_count = 0
    for key in sorted(buckets):
        _chart, _sign, axis, _boundary, base_endpoint = key
        tree = r292.PIntervalNode(buckets[key])
        for cell_index in queries[key]:
            cell = cells[cell_index]
            rectangle = tangent_rectangle(cell["box"], axis)
            candidates: list[tuple[tuple[Q, ...], dict[str, Any]]] = []
            tree.query(rectangle[0], rectangle[1], candidates)
            interval_tree_query_count += 1
            interval_tree_candidate_count += len(candidates)
            for _pseudo, base in candidates:
                base_rectangle = base["tangent_rectangle"]
                if not (
                    max(rectangle[2], base_rectangle[2])
                    < min(rectangle[3], base_rectangle[3])
                ):
                    continue
                face = exact_face(
                    cell["box"],
                    base["transformed_support_box"],
                    axis,
                    base_endpoint,
                )
                need(face is not None, "interval shortlist exact face")
                self_endpoint = (
                    cell["endpoint_occurrence_id"] == base["occurrence_id"]
                )
                endpoint_pair = (
                    None
                    if self_endpoint
                    else list(
                        pair(
                            cell["endpoint_occurrence_id"],
                            base["occurrence_id"],
                        )
                    )
                )
                disposition, replays, witness = signed_face_disposition(
                    cell, face, axis, regions
                )
                payload = {
                    "Round299C_registry_support_boundary_face_row_id":
                        "round299c-registry-support-boundary-face:"
                        + digest(
                            [
                                cell["cell_id"],
                                base["occurrence_id"],
                                axis,
                                base_endpoint,
                                list(map(qstr, face)),
                            ]
                        ),
                    "Round292_refinement_cell_id": cell["cell_id"],
                    "Round292_endpoint_kind": cell["endpoint_kind"],
                    "Round292_formal_occurrence_id":
                        cell["endpoint_occurrence_id"],
                    "Round292_Round275_region_id": cell["region_id"],
                    "Round292_inherited_signed_support_state":
                        cell["inherited_signed_support_state"],
                    "base_registry_occurrence_id": base["occurrence_id"],
                    "base_registry_occurrence_source":
                        base["occurrence_source"],
                    "base_registry_rational_support_box": [
                        qstr(value) for value in base["rational_support_box"]
                    ],
                    "base_registry_transformed_support_box_t2_p_s": [
                        qstr(value) for value in base["transformed_support_box"]
                    ],
                    "source_chart": cell["source_chart"],
                    "physical_t_sign": cell["physical_t_sign"],
                    "common_face_axis": axis,
                    "base_support_touching_endpoint": base_endpoint,
                    "exact_positive_area_coordinate_face_t2_p_s": [
                        qstr(value) for value in face
                    ],
                    "same_complete_10_field_return_signature":
                        cell["signature_sha256"] == base["signature_sha256"],
                    "Round292_complete_10_field_return_signature_sha256":
                        cell["signature_sha256"],
                    "base_complete_10_field_return_signature_sha256":
                        base["signature_sha256"],
                    "same_formal_occurrence_endpoint": self_endpoint,
                    "unordered_nonself_formal_occurrence_endpoint_pair":
                        endpoint_pair,
                    "signed_support_face_disposition": disposition,
                    "signed_support_precision_replays": replays,
                    "strict_desired_side_face_witness": witness,
                    "formal_occurrence_identity_collapse_credit": 0,
                    "formal_component_edge_credit": 0,
                    "formal_DSU_rank_reduction_credit": 0,
                    "formal_maximality_credit": 0,
                }
                rows.append(closed(payload))
    rows.sort(key=lambda row: row["Round299C_registry_support_boundary_face_row_id"])
    return rows, {
        "interval_tree_query_count": interval_tree_query_count,
        "interval_tree_tangent1_candidate_count":
            interval_tree_candidate_count,
    }


def prior_pair_sets() -> dict[str, set[tuple[str, str]]]:
    ordinary_document = read_gzip(R297)
    ordinary = {
        tuple(row["exact_occurrence_endpoint_pair"])
        for row in ordinary_document["rows"]
    }
    seam_document = read_gzip(R296)
    seam = {
        tuple(row["unordered_formal_occurrence_endpoint_pair"])
        for row in seam_document["rows"]
    }
    lower_document = read_gzip(R295A)
    lower = {
        tuple(row["target_Round294_registry_occurrence_ids"])
        for row in lower_document["rows"]
        if row["target_Round294_registry_reference_count"] == 2
    }
    a_document = read_gzip(R299AL)
    r299_all = {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in a_document["rows"]
        if row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
    }
    r299_full = {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in a_document["rows"]
        if row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
        and row["coordinate_face_physical_replay_status"].startswith(
            "BOTH_ENDPOINT_CELLS_FULL"
        )
    }
    b_document = read_gzip(R299BL)
    r299_graph_accepted = {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in b_document["rows"]
        if row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
        and row["signed_support_face_disposition"].startswith(
            "POSITIVE_AREA_SIGNED_SUPPORT_COMMON_FACE_CERTIFIED"
        )
    }
    need(
        len(ordinary) == 330_724
        and len(seam) == 15_316
        and len(lower) == 111_524
        and len(r299_all) == 38_204
        and len(r299_full | r299_graph_accepted) == 25_452,
        "prior pair universe census",
    )
    return {
        "R297_ORDINARY": ordinary,
        "R296_TRUE_SEAM": seam,
        "R295A_LOWER": lower,
        "R299_ALL_COORDINATE": r299_all,
        "R299_ACCEPTED_SIGNED_SUPPORT": r299_full | r299_graph_accepted,
    }


def census(
    rows: list[dict[str, Any]],
    search: dict[str, Any],
    prior: dict[str, set[tuple[str, str]]],
) -> dict[str, Any]:
    raw_source_kind = Counter()
    raw_disposition = Counter()
    raw_signature = Counter()
    raw_axis = Counter()
    self_source_kind = Counter()
    accepted_pairs: set[tuple[str, str]] = set()
    excluded_pairs: set[tuple[str, str]] = set()
    distinct_by_source_kind: dict[str, set[tuple[str, str]]] = defaultdict(set)
    raw_accepted_nonself = 0
    raw_excluded_nonself = 0

    for row in rows:
        cell_kind = (
            "U" if row["Round292_endpoint_kind"].startswith("UNCOVERED") else "O"
        )
        source_kind = cell_kind + "|" + row["base_registry_occurrence_source"]
        raw_source_kind[source_kind] += 1
        raw_disposition[row["signed_support_face_disposition"]] += 1
        raw_signature[
            source_kind
            + "|"
            + ("SAME_SIGNATURE" if row[
                "same_complete_10_field_return_signature"
            ] else "DIFFERENT_SIGNATURE")
        ] += 1
        raw_axis[str(row["common_face_axis"])] += 1
        endpoint_pair = row[
            "unordered_nonself_formal_occurrence_endpoint_pair"
        ]
        if endpoint_pair is None:
            self_source_kind[source_kind] += 1
            continue
        exact_pair = tuple(endpoint_pair)
        distinct_by_source_kind[source_kind].add(exact_pair)
        accepted = not row["signed_support_face_disposition"].endswith(
            "__EXCLUDED"
        )
        if accepted:
            raw_accepted_nonself += 1
            accepted_pairs.add(exact_pair)
        else:
            raw_excluded_nonself += 1
            excluded_pairs.add(exact_pair)

    # Edge existence is existential: a rejected local face cannot overwrite a
    # separate accepted face for the same occurrence pair.
    accepted_exists_pairs = set(accepted_pairs)
    mixed_pairs = accepted_pairs & excluded_pairs
    intersection = {
        name: len(accepted_exists_pairs & pairs)
        for name, pairs in prior.items()
    }
    return {
        **search,
        "raw_registry_support_boundary_face_count": len(rows),
        "raw_Round292_kind_base_source_histogram":
            dict(sorted(raw_source_kind.items())),
        "raw_signed_support_face_disposition_histogram":
            dict(sorted(raw_disposition.items())),
        "raw_Round292_kind_base_source_signature_histogram":
            dict(sorted(raw_signature.items())),
        "raw_common_face_axis_histogram": dict(sorted(raw_axis.items())),
        "self_endpoint_source_histogram": dict(sorted(self_source_kind.items())),
        "raw_accepted_nonself_face_count": raw_accepted_nonself,
        "raw_excluded_nonself_face_count": raw_excluded_nonself,
        "accepted_distinct_nonself_pair_count": len(accepted_exists_pairs),
        "excluded_distinct_nonself_pair_count": len(excluded_pairs),
        "distinct_pair_with_both_accept_and_reject_face_count":
            len(mixed_pairs),
        "accepted_distinct_pair_by_Round292_kind_base_source": dict(
            sorted(
                (key, len(values & accepted_exists_pairs))
                for key, values in distinct_by_source_kind.items()
            )
        ),
        "accepted_pair_prior_channel_intersection_count": intersection,
        "accepted_pair_new_beyond_all_prior_accepted_channels_count": len(
            accepted_exists_pairs
            - set().union(
                prior["R297_ORDINARY"],
                prior["R296_TRUE_SEAM"],
                prior["R295A_LOWER"],
                prior["R299_ACCEPTED_SIGNED_SUPPORT"],
            )
        ),
        "coordinate_support_box_face_is_not_automatically_component_edge":
            True,
        "formal_credit_remains_zero": True,
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    for name, expected in PINS.items():
        need(file_sha256(HERE / name) == expected, f"pin:{name}")
    cells, regions = load_r292_cells()
    base_rows = load_base_registry_supports()
    queries, buckets, search = build_boundary_buckets(cells, base_rows)
    rows, query_diagnostics = enumerate_faces(
        cells, regions, queries, buckets
    )
    prior = prior_pair_sets()
    result_census = census(
        rows, {**search, **query_diagnostics}, prior
    )
    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": "PASS_ZERO_CREDIT__R292_TO_BASE_REGISTRY_BOUNDARY_SWEEP_COMPLETE",
        "row_count": len(rows),
        "rows": rows,
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest(
            [row["Round299C_registry_support_boundary_face_row_id"] for row in rows]
        ),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
    }
    result = {
        "schema": SCHEMA,
        "status": "PASS_ZERO_CREDIT__REGISTRY_BOUNDARY_CANDIDATES_ENUMERATED",
        "input_file_pins": PINS,
        "census": result_census,
        "ledger": {
            "filename": LEDGER.name,
            "row_count": len(rows),
            "rows_sha256": ledger["rows_sha256"],
        },
        "strict_nonpromotion": {
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "CM2": "NO_GO_PENDING_SUPPORT_FACE_SEMANTICS_AND_GLOBAL_COVERAGE",
        },
    }
    result["result_sha256"] = digest(result)
    return ledger, result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    ledger, result = build()
    ledger_bytes = deterministic_gzip_bytes(ledger)
    result["ledger"]["file_sha256"] = hashlib.sha256(ledger_bytes).hexdigest()
    result["result_sha256"] = digest(
        {key: value for key, value in result.items() if key != "result_sha256"}
    )
    atomic(arguments.ledger, ledger_bytes)
    atomic(arguments.output, canonical(result) + b"\n")


if __name__ == "__main__":
    main()
