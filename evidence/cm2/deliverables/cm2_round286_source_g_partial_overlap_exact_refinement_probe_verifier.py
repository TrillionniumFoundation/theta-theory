#!/usr/bin/env python3
"""Independent verifier for the Round286 exact-refinement probe.

The Round286 producer is pinned and treated only as inert bytes.  This verifier
starts from the frozen Round275 region boxes, Round279 atom support boxes,
Round280 region/atom incidences, and the Round284 partial-overlap disposition.
It independently reconstructs the exact rational common refinement of all
2,184 partial regions and then compares the complete 7,616-row candidate
ledger byte-for-byte at the semantic-object level.

This remains a ZERO-CREDIT verification.  A uniquely covered subcell is only
an alias candidate, and an uncovered subcell is only a new-disjoint candidate.
No occurrence, component, maximality, fibre, disposition, seam, or Jx/Jy
credit is issued here.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
import gc
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import random
import sys
import tempfile
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round286_source_g_partial_overlap_exact_refinement_probe"
PRODUCER = HERE / f"{PREFIX}.py"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"

R275 = HERE / (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "certificate.json"
)
R279_ATOMS = HERE / (
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
)
R280_BINDINGS = HERE / (
    "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_"
    "region_bindings.json.gz"
)
R284_RESULT = HERE / (
    "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_result.json"
)
R284_LEDGER = HERE / (
    "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe_"
    "ledger.json.gz"
)

VERIFICATION_SCHEMA = (
    "cm2.round286.source-g-partial-overlap-exact-refinement-probe."
    "verification.v1"
)
RESULT_SCHEMA = (
    "cm2.round286.source-g-partial-overlap-exact-refinement-probe.v1"
)
LEDGER_SCHEMA = (
    "cm2.round286.source-g-partial-overlap-exact-refinement.ledger.v1"
)

INPUT_PINS = {
    R275.name:
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R279_ATOMS.name:
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    R280_BINDINGS.name:
        "8354eb042455e6d3ed591ee1620c9fc9def1af916a9bfbc0bf42e473e3e6e58b",
    R284_RESULT.name:
        "e25dd7b494ad2c2ccddc17601d28136c1919a3b16e41f008669bd6c14a513692",
    R284_LEDGER.name:
        "39b69e0c5d249454c7ff13da99b260d3a7fabfa03c8ad6866035cbcaa883eb92",
}

ARTIFACT_PINS = {
    **INPUT_PINS,
    PRODUCER.name:
        "2fa6a547f3bad0432f77b5fba75069c3599fcef2234b0f9d19547297ea670088",
    LEDGER.name:
        "bb7e28cbe029e2bb414313ec4a08f6366acbbad88a519926ec2a3a424e679eda",
    RESULT.name:
        "a3b705c489eff9df4e1129bcdf960c6ea9de435e326c1d7e040e01d63352d29e",
}

PARTIAL = "PARTIAL_OVERLAP__EXACT_REFINEMENT_REQUIRED"
ALIAS = "UNIQUE_ATOM_ALIAS_SUBCELL__OCCURRENCE_ID_NOT_YET_ISSUED"
NEW = "NEW_DISJOINT_SUBCELL__OCCURRENCE_ID_NOT_YET_ISSUED"
EXPECTED_CELL_HISTOGRAM = {ALIAS: 5700, NEW: 1916}
EXPECTED_REGION_HISTOGRAM = {
    "2|1|1": 976,
    "2|2|0": 416,
    "3|2|1": 8,
    "4|1|3": 8,
    "4|3|1": 64,
    "4|4|0": 312,
    "5|5|0": 144,
    "6|2|4": 8,
    "8|4|4": 68,
    "10|5|5": 76,
    "10|10|0": 88,
    "20|10|10": 16,
}
EXPECTED_COVERED_VOLUME = Q(
    3348196627739797762204307008167731394283,
    2787593149816327892691964784081045188247552000,
)
EXPECTED_UNCOVERED_VOLUME = Q(
    2978688554474657606787381925998666783467,
    2787593149816327892691964784081045188247552000,
)
ROW_ZERO_FIELDS = (
    "formal_occurrence_credit",
    "formal_component_credit",
    "formal_maximality_credit",
    "Jx_Jy_same_point_glue_credit",
)
RESULT_ZERO_FIELDS = (
    "occurrence_credit",
    "component_credit",
    "maximality_credit",
    "fibre_credit",
    "global_disposition_credit",
    "Jx_Jy_same_point_glue_credit",
)
DUAL_REPLAY_SEEDS = (286071, 286929)

ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


class VerificationError(RuntimeError):
    """Raised on any frozen-input or candidate-contract failure."""


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
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=stream, mtime=0
    ) as handle:
        handle.write(canonical(value))
    return stream.getvalue()


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def box_volume(box: tuple[Q, Q, Q, Q, Q, Q]) -> Q:
    return (
        (box[1] - box[0])
        * (box[3] - box[2])
        * (box[5] - box[4])
    )


def positive_box(box: tuple[Q, ...]) -> bool:
    return (
        len(box) == 6
        and all(box[2 * axis] < box[2 * axis + 1] for axis in range(3))
    )


def positive_interior_overlap(
    left: tuple[Q, Q, Q, Q, Q, Q],
    right: tuple[Q, Q, Q, Q, Q, Q],
) -> bool:
    return all(
        max(left[2 * axis], right[2 * axis])
        < min(left[2 * axis + 1], right[2 * axis + 1])
        for axis in range(3)
    )


def intersection_box(
    left: tuple[Q, Q, Q, Q, Q, Q],
    right: tuple[Q, Q, Q, Q, Q, Q],
) -> tuple[Q, Q, Q, Q, Q, Q] | None:
    value = tuple(
        endpoint
        for axis in range(3)
        for endpoint in (
            max(left[2 * axis], right[2 * axis]),
            min(left[2 * axis + 1], right[2 * axis + 1]),
        )
    )
    return value if positive_box(value) else None


def verify_closed_ledger(
    label: str,
    ledger: dict[str, Any],
    id_field: str,
    expected_count: int,
) -> list[dict[str, Any]]:
    rows = ledger["rows"]
    need(isinstance(rows, list), f"{label}:rows list")
    need(ledger["row_count"] == len(rows) == expected_count, f"{label}:row count")
    need(ledger["rows_sha256"] == digest(rows), f"{label}:rows digest")
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), f"{label}:unique ids")
    need(ledger["row_ids_sha256"] == digest(ids), f"{label}:id digest")
    hashes: list[str] = []
    for row in rows:
        payload = dict(row)
        stored = payload.pop("row_sha256")
        need(stored == digest(payload), f"{label}:row closure:{row[id_field]}")
        hashes.append(stored)
    need(ledger["row_hashes_sha256"] == digest(hashes), f"{label}:hash digest")
    return rows


def load_round275_regions() -> dict[str, dict[str, Any]]:
    wrapper = read_json(R275)
    need(set(wrapper) == {"result", "result_sha256"}, "Round275 wrapper")
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "Round275 digest")
    result = wrapper["result"]
    need(
        result["schema"]
        == "cm2.round275.source-g-complete-reverse-rechart-materialization.v1",
        "Round275 schema",
    )
    strict = verify_closed_ledger(
        "Round275 strict regions",
        result["strict_region_ledger"],
        "reverse_rechart_region_row_id",
        5288,
    )
    arranged = verify_closed_ledger(
        "Round275 arrangement regions",
        result["arrangement_region_ledger"],
        "reverse_rechart_region_row_id",
        8500,
    )
    rows = [*strict, *arranged]
    need(
        result["census"]["total_materialized_connected_region_count"] == 13788,
        "Round275 census",
    )
    for row in rows:
        region_id = row["reverse_rechart_region_row_id"]
        need(
            row["connected_open_region"] is True
            and row["occurrence_credit"] == 0
            and row["component_credit"] == 0
            and row["maximality_credit"] == 0,
            f"Round275 zero credit:{region_id}",
        )
        need(
            row["complete_10_field_return_signature_sha256"]
            == digest(row["local_return_signature"]),
            f"Round275 signature closure:{region_id}",
        )
        need(
            positive_box(tuple(map(Q, row["adjacent_rational_region_box"]))),
            f"Round275 positive box:{region_id}",
        )
    regions = {row["reverse_rechart_region_row_id"]: row for row in rows}
    need(len(regions) == 13788, "Round275 region universe")
    return regions


def load_round284_partial_ids(
    regions: dict[str, dict[str, Any]],
) -> tuple[list[str], dict[str, Any]]:
    result = read_json(R284_RESULT)
    need(
        result["schema"]
        == "cm2.round284.source-g-rechart-occurrence-overlap-contract-probe.v1",
        "Round284 result schema",
    )
    need(
        result["result_sha256"]
        == digest({key: value for key, value in result.items() if key != "result_sha256"}),
        "Round284 result object digest",
    )
    need(result["pins"][R275.name] == INPUT_PINS[R275.name], "Round284 R275 pin")
    need(
        result["pins"][R279_ATOMS.name] == INPUT_PINS[R279_ATOMS.name],
        "Round284 R279 pin",
    )
    need(
        result["pins"][R280_BINDINGS.name] == INPUT_PINS[R280_BINDINGS.name],
        "Round284 R280 pin",
    )
    need(
        result["census"]["classification_histogram"][PARTIAL] == 2184
        and result["census"]["Round275_region_count"] == 13788,
        "Round284 partial census",
    )
    ledger = read_gzip_json(R284_LEDGER)
    need(
        ledger["schema"]
        == "cm2.round284.source-g-rechart-occurrence-overlap-contract.ledger.v1",
        "Round284 ledger schema",
    )
    rows = verify_closed_ledger(
        "Round284 overlap ledger",
        ledger,
        "Round284_region_overlap_row_id",
        13788,
    )
    need(
        result["ledger"]["rows_sha256"] == ledger["rows_sha256"]
        and result["ledger"]["row_count"] == 13788
        and result["ledger"]["file_sha256"] == file_sha256(R284_LEDGER),
        "Round284 result/ledger binding",
    )
    partial_ids: list[str] = []
    seen_regions: set[str] = set()
    for row in rows:
        region_id = row["Round275_region_id"]
        need(region_id in regions, f"Round284 known region:{region_id}")
        need(region_id not in seen_regions, f"Round284 duplicate region:{region_id}")
        seen_regions.add(region_id)
        need(
            all(row[field] == 0 for field in ROW_ZERO_FIELDS),
            f"Round284 zero credit:{region_id}",
        )
        if row["classification"] == PARTIAL:
            need(
                any(
                    relation["relation"] == "PARTIAL_POSITIVE_VOLUME_OVERLAP"
                    for relation in row["relations"]
                ),
                f"Round284 partial evidence:{region_id}",
            )
            partial_ids.append(region_id)
    need(seen_regions == set(regions), "Round284 complete region universe")
    need(len(partial_ids) == len(set(partial_ids)) == 2184, "Round284 partial ids")
    return partial_ids, result


def load_round280_bindings(
    regions: dict[str, dict[str, Any]],
    partial_ids: list[str],
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    ledger = read_gzip_json(R280_BINDINGS)
    need(
        ledger["schema"] == "cm2.round280.rechart-region-incidence.zero-credit.v1",
        "Round280 schema",
    )
    rows = verify_closed_ledger(
        "Round280 region bindings",
        ledger,
        "Round275_region_incidence_row_id",
        13788,
    )
    wanted_regions = set(partial_ids)
    selected: dict[str, dict[str, Any]] = {}
    wanted_atoms: set[str] = set()
    seen_regions: set[str] = set()
    for row in rows:
        region_id = row["Round275_reverse_rechart_region_row_id"]
        need(region_id in regions, f"Round280 known region:{region_id}")
        need(region_id not in seen_regions, f"Round280 duplicate region:{region_id}")
        seen_regions.add(region_id)
        need(
            row["matching_atom_count"] == len(row["matching_atom_ids"])
            and len(row["matching_atom_ids"]) == len(set(row["matching_atom_ids"])),
            f"Round280 atom count:{region_id}",
        )
        need(
            row["formal_component_union_credit"] == 0
            and row["formal_expanded_occurrence_credit"] == 0
            and row["formal_maximality_credit"] == 0,
            f"Round280 zero credit:{region_id}",
        )
        if region_id in wanted_regions:
            region = regions[region_id]
            need(
                row["source_chart"] == region["source_chart"]
                and row["adjacent_chart"] == region["adjacent_chart"]
                and row["owner_target"] == region["owner_target"]
                and row["complete_10_field_return_signature_sha256"]
                == region["complete_10_field_return_signature_sha256"],
                f"Round280 provenance:{region_id}",
            )
            selected[region_id] = row
            wanted_atoms.update(row["matching_atom_ids"])
    need(seen_regions == set(regions), "Round280 complete region universe")
    need(set(selected) == wanted_regions, "Round280 partial binding coverage")
    return selected, wanted_atoms


def load_referenced_round279_atoms(
    wanted_atoms: set[str],
) -> tuple[dict[str, dict[str, Any]], int]:
    ledger = read_gzip_json(R279_ATOMS)
    need(
        ledger["schema"] == "cm2.round279.canonical-collar-atom-ledger.v1",
        "Round279 schema",
    )
    expected_header = {
        "row_count": 332016,
        "source_signature_row_count": 332020,
        "artificial_alias_contraction_count": 4,
        "existing_Round208_occurrence_backed_atom_count": 36040,
        "new_occurrence_region_atom_candidate_count": 295976,
        "strict_subbox_atom_count": 4,
        "rows_sha256":
            "d2680baed100e4e1a236aa929999c7d93be5eeddabb2cc0660fca5e756882105",
        "row_ids_sha256":
            "a685a017d5ae1a4d735a84142b3a2f2c3ed1b3cd2be3c41ad3dca3297f0acbe3",
        "row_hashes_sha256":
            "52aed35a8b1b423da27c7b6f05bc6f6721398c606ebe7ec3239770ada9f8887f",
    }
    need(
        all(ledger[key] == value for key, value in expected_header.items()),
        "Round279 frozen header",
    )
    need(
        ledger["strict_nonpromotion"]
        == {
            "component_credit": 0,
            "expanded_occurrence_credit": 0,
            "maximality_credit": 0,
        },
        "Round279 strict nonpromotion",
    )
    rows = ledger["rows"]
    need(len(rows) == 332016, "Round279 row count")
    seen: set[str] = set()
    selected: dict[str, dict[str, Any]] = {}
    support_box_count = 0
    for row in rows:
        atom_id = row["canonical_atom_id"]
        need(atom_id not in seen, f"Round279 duplicate atom:{atom_id}")
        seen.add(atom_id)
        need(
            row["expanded_occurrence_credit"] == 0
            and row["component_credit"] == 0
            and row["maximality_credit"] == 0,
            f"Round279 zero credit:{atom_id}",
        )
        boxes = row["frozen_true_support_boxes"]
        need(boxes and all(len(box) == 6 for box in boxes), f"Round279 boxes:{atom_id}")
        support_box_count += len(boxes)
        if atom_id in wanted_atoms:
            payload = dict(row)
            stored = payload.pop("row_sha256")
            need(stored == digest(payload), f"Round279 row closure:{atom_id}")
            need(
                row["complete_10_field_return_signature_sha256"]
                == digest(row["complete_10_field_return_signature"]),
                f"Round279 signature closure:{atom_id}",
            )
            need(
                all(positive_box(tuple(map(Q, box))) for box in boxes),
                f"Round279 positive boxes:{atom_id}",
            )
            selected[atom_id] = row
    need(len(seen) == 332016, "Round279 atom universe")
    need(set(selected) == wanted_atoms, "Round279 referenced atom coverage")
    del rows, ledger, seen
    gc.collect()
    return selected, support_box_count


def reconstruct(
    regions: dict[str, dict[str, Any]],
    partial_ids: list[str],
    bindings: dict[str, dict[str, Any]],
    atoms: dict[str, dict[str, Any]],
    replay_seed: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    order = list(partial_ids)
    random.Random(replay_seed).shuffle(order)
    rows: list[dict[str, Any]] = []
    cell_histogram: Counter[str] = Counter()
    region_histogram: Counter[str] = Counter()
    covered_volume = Q(0)
    uncovered_volume = Q(0)
    clip_count = 0
    pairwise_comparisons = 0

    for region_id in order:
        region = regions[region_id]
        region_box = tuple(map(Q, region["adjacent_rational_region_box"]))
        binding = bindings[region_id]
        clips: list[tuple[str, int, tuple[Q, Q, Q, Q, Q, Q]]] = []
        genuine_partial = False
        for atom_id in binding["matching_atom_ids"]:
            atom = atoms[atom_id]
            need(
                atom["source_chart"] == region["adjacent_chart"]
                and atom["owner_target"] == region["owner_target"]
                and atom["complete_10_field_return_signature_sha256"]
                == region["complete_10_field_return_signature_sha256"],
                f"Round279/Round275 provenance:{region_id}:{atom_id}",
            )
            for box_index, values in enumerate(atom["frozen_true_support_boxes"]):
                atom_box = tuple(map(Q, values))
                clip = intersection_box(region_box, atom_box)
                if clip is not None:
                    clips.append((atom_id, box_index, clip))
                    genuine_partial |= clip != region_box
        need(clips and genuine_partial, f"Round286 genuine partial:{region_id}")
        clip_count += len(clips)

        axes = [
            sorted(
                {
                    region_box[2 * axis],
                    region_box[2 * axis + 1],
                    *(
                        endpoint
                        for _atom_id, _box_index, clip in clips
                        for endpoint in clip[2 * axis:2 * axis + 2]
                    ),
                }
            )
            for axis in range(3)
        ]
        region_rows: list[dict[str, Any]] = []
        local_histogram: Counter[str] = Counter()
        for t0, t1 in zip(axes[0], axes[0][1:]):
            for p0, p1 in zip(axes[1], axes[1][1:]):
                for s0, s1 in zip(axes[2], axes[2][1:]):
                    cell = (t0, t1, p0, p1, s0, s1)
                    need(positive_box(cell), f"Round286 positive cell:{region_id}")
                    owners = sorted(
                        {
                            atom_id
                            for atom_id, _box_index, clip in clips
                            if clip[0] <= t0 <= t1 <= clip[1]
                            and clip[2] <= p0 <= p1 <= clip[3]
                            and clip[4] <= s0 <= s1 <= clip[5]
                        }
                    )
                    need(len(owners) <= 1, f"Round286 multi-atom cell:{region_id}")
                    classification = ALIAS if owners else NEW
                    volume = box_volume(cell)
                    local_histogram[classification] += 1
                    cell_histogram[classification] += 1
                    if owners:
                        covered_volume += volume
                    else:
                        uncovered_volume += volume
                    payload = {
                        "Round286_refinement_cell_id":
                            "round286-refinement-cell:"
                            + digest([region_id, [qstr(value) for value in cell]]),
                        "Round275_region_id": region_id,
                        "source_chart": region["source_chart"],
                        "adjacent_chart": region["adjacent_chart"],
                        "parent_id": region["parent_id"],
                        "owner_target": region["owner_target"],
                        "complete_10_field_return_signature_sha256":
                            region["complete_10_field_return_signature_sha256"],
                        "cell_exact_box": [qstr(value) for value in cell],
                        "cell_coordinate_volume": qstr(volume),
                        "classification": classification,
                        "unique_alias_atom_id": owners[0] if owners else None,
                        "atom_occupancy_count": len(owners),
                        "formal_occurrence_credit": 0,
                        "formal_component_credit": 0,
                        "formal_maximality_credit": 0,
                        "Jx_Jy_same_point_glue_credit": 0,
                    }
                    row = dict(payload)
                    row["row_sha256"] = digest(payload)
                    region_rows.append(row)

        need(
            sum(Q(row["cell_coordinate_volume"]) for row in region_rows)
            == box_volume(region_box),
            f"Round286 exact volume cover:{region_id}",
        )
        for left_index, left in enumerate(region_rows):
            left_box = tuple(map(Q, left["cell_exact_box"]))
            need(
                all(
                    region_box[2 * axis] <= left_box[2 * axis]
                    < left_box[2 * axis + 1] <= region_box[2 * axis + 1]
                    for axis in range(3)
                ),
                f"Round286 cell inside region:{region_id}",
            )
            for right in region_rows[left_index + 1:]:
                pairwise_comparisons += 1
                need(
                    not positive_interior_overlap(
                        left_box, tuple(map(Q, right["cell_exact_box"]))
                    ),
                    f"Round286 pairwise disjoint:{region_id}",
                )
        region_histogram[
            (
                len(region_rows),
                local_histogram[ALIAS],
                local_histogram[NEW],
            )
        ] += 1
        rows.extend(region_rows)

    rows.sort(key=lambda row: row["Round286_refinement_cell_id"])
    normalized_region_histogram = {
        "|".join(map(str, key)): value
        for key, value in sorted(region_histogram.items())
    }
    need(len(rows) == 7616, "Round286 reconstructed cell count")
    need(dict(cell_histogram) == EXPECTED_CELL_HISTOGRAM, "Round286 cell census")
    need(
        normalized_region_histogram == EXPECTED_REGION_HISTOGRAM,
        "Round286 region partition census",
    )
    need(covered_volume == EXPECTED_COVERED_VOLUME, "Round286 covered volume")
    need(uncovered_volume == EXPECTED_UNCOVERED_VOLUME, "Round286 uncovered volume")

    reconstruction = {
        "input_partial_region_count": len(partial_ids),
        "output_refinement_cell_count": len(rows),
        "cell_classification_histogram": dict(sorted(cell_histogram.items())),
        "region_partition_histogram": normalized_region_histogram,
        "region_with_uncovered_new_subcells_count":
            sum(value for (count, aliases, new), value in region_histogram.items() if new),
        "region_fully_covered_by_multiple_unique_atom_subcells_count":
            sum(
                value
                for (count, aliases, new), value in region_histogram.items()
                if not new
            ),
        "multi_atom_occupancy_cell_count": 0,
        "covered_alias_coordinate_volume": qstr(covered_volume),
        "uncovered_new_coordinate_volume": qstr(uncovered_volume),
        "positive_atom_clip_count": clip_count,
        "pairwise_interior_disjointness_comparison_count": pairwise_comparisons,
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest(
            [row["Round286_refinement_cell_id"] for row in rows]
        ),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
    }
    return rows, reconstruction


def expected_strict_nonpromotion() -> dict[str, Any]:
    return {
        "occurrence_credit": 0,
        "component_credit": 0,
        "maximality_credit": 0,
        "fibre_credit": 0,
        "global_disposition_credit": 0,
        "Jx_Jy_same_point_glue_credit": 0,
        "quotient": 63224,
        "expanded_occurrences": 126468,
        "Gate5": "10/18",
        "D02": "BLOCKED",
        "CM2": "NO-GO_FOR_CLAIM",
    }


def audit_candidate(
    ledger: dict[str, Any],
    result: dict[str, Any],
    expected_rows: list[dict[str, Any]],
    reconstruction: dict[str, Any],
) -> None:
    need(ledger["schema"] == LEDGER_SCHEMA, "Round286 ledger schema")
    rows = verify_closed_ledger(
        "Round286 candidate ledger",
        ledger,
        "Round286_refinement_cell_id",
        7616,
    )
    need(
        [row["Round286_refinement_cell_id"] for row in rows]
        == sorted(row["Round286_refinement_cell_id"] for row in rows),
        "Round286 canonical order",
    )
    need(rows == expected_rows, "Round286 exact independent row reconstruction")
    for row in rows:
        need(
            all(row[field] == 0 for field in ROW_ZERO_FIELDS),
            f"Round286 row zero credit:{row['Round286_refinement_cell_id']}",
        )
        owners = row["atom_occupancy_count"]
        if row["classification"] == ALIAS:
            need(
                owners == 1 and row["unique_alias_atom_id"] is not None,
                "Round286 alias semantics",
            )
        else:
            need(
                row["classification"] == NEW
                and owners == 0
                and row["unique_alias_atom_id"] is None,
                "Round286 new semantics",
            )
        need(
            Q(row["cell_coordinate_volume"])
            == box_volume(tuple(map(Q, row["cell_exact_box"]))),
            "Round286 cell volume closure",
        )

    need(result["schema"] == RESULT_SCHEMA, "Round286 result schema")
    need(
        result["status"]
        == "PASS_ROUND286_PARTIAL_OVERLAP_EXACT_REFINEMENT__ZERO_CREDIT",
        "Round286 result status",
    )
    need(
        result["result_sha256"]
        == digest({key: value for key, value in result.items() if key != "result_sha256"}),
        "Round286 result object digest",
    )
    need(result["pins"] == INPUT_PINS, "Round286 input pins")
    expected_census = {
        key: value
        for key, value in reconstruction.items()
        if key
        in {
            "input_partial_region_count",
            "output_refinement_cell_count",
            "cell_classification_histogram",
            "region_partition_histogram",
            "region_with_uncovered_new_subcells_count",
            "region_fully_covered_by_multiple_unique_atom_subcells_count",
            "multi_atom_occupancy_cell_count",
            "covered_alias_coordinate_volume",
            "uncovered_new_coordinate_volume",
        }
    }
    need(result["census"] == expected_census, "Round286 result census")
    need(
        result["semantic_contract"]
        == {
            "cells_are_pairwise_interior_disjoint_within_each_region": True,
            "each_cell_has_zero_or_one_atom_owner": True,
            "unique_atom_subcell_is_relative_alias_candidate": True,
            "uncovered_subcell_is_relative_new_candidate": True,
            "cells_of_one_connected_region_retain_internal_component_frontier": True,
        },
        "Round286 semantic contract",
    )
    need(
        result["strict_nonpromotion"] == expected_strict_nonpromotion(),
        "Round286 strict nonpromotion",
    )
    need(
        all(result["strict_nonpromotion"][field] == 0 for field in RESULT_ZERO_FIELDS),
        "Round286 zero result credit",
    )
    need(
        result["ledger"]
        == {
            "filename": LEDGER.name,
            "row_count": 7616,
            "rows_sha256": ledger["rows_sha256"],
            "file_sha256": hashlib.sha256(
                deterministic_gzip_bytes(ledger)
            ).hexdigest(),
        },
        "Round286 result/ledger binding",
    )


def reclose(ledger: dict[str, Any], result: dict[str, Any]) -> None:
    for row in ledger["rows"]:
        payload = dict(row)
        payload.pop("row_sha256", None)
        row["row_sha256"] = digest(payload)
    ledger["row_count"] = len(ledger["rows"])
    ledger["rows_sha256"] = digest(ledger["rows"])
    ledger["row_ids_sha256"] = digest(
        [row["Round286_refinement_cell_id"] for row in ledger["rows"]]
    )
    ledger["row_hashes_sha256"] = digest(
        [row["row_sha256"] for row in ledger["rows"]]
    )
    result["ledger"]["row_count"] = ledger["row_count"]
    result["ledger"]["rows_sha256"] = ledger["rows_sha256"]
    result["ledger"]["file_sha256"] = hashlib.sha256(
        deterministic_gzip_bytes(ledger)
    ).hexdigest()
    result["result_sha256"] = digest(
        {key: value for key, value in result.items() if key != "result_sha256"}
    )


def run_attacks(
    ledger: dict[str, Any],
    result: dict[str, Any],
    expected_rows: list[dict[str, Any]],
    reconstruction: dict[str, Any],
) -> dict[str, Any]:
    def alias_row(candidate: dict[str, Any]) -> dict[str, Any]:
        return next(row for row in candidate["rows"] if row["classification"] == ALIAS)

    def new_row(candidate: dict[str, Any]) -> dict[str, Any]:
        return next(row for row in candidate["rows"] if row["classification"] == NEW)

    def forge_ledger_file_digest(
        candidate_ledger: dict[str, Any],
        candidate_result: dict[str, Any],
    ) -> None:
        candidate_result["ledger"]["file_sha256"] = "0" * 64
        candidate_result["result_sha256"] = digest(
            {
                key: value
                for key, value in candidate_result.items()
                if key != "result_sha256"
            }
        )

    attacks: list[
        tuple[
            str,
            Callable[[dict[str, Any], dict[str, Any]], None],
            bool,
        ]
    ] = [
        ("DROP_CELL", lambda l, r: l["rows"].pop(), True),
        (
            "DUPLICATE_CELL",
            lambda l, r: l["rows"].append(deepcopy(l["rows"][0])),
            True,
        ),
        (
            "TAMPER_CELL_BOUNDS",
            lambda l, r: l["rows"][0]["cell_exact_box"].__setitem__(0, "0"),
            True,
        ),
        (
            "TAMPER_ALIAS_OWNER",
            lambda l, r: alias_row(l).__setitem__(
                "unique_alias_atom_id", "round279-collar-atom:" + "0" * 64
            ),
            True,
        ),
        (
            "FORGE_NEW_AS_ALIAS",
            lambda l, r: new_row(l).__setitem__("classification", ALIAS),
            True,
        ),
        (
            "TAMPER_CELL_VOLUME",
            lambda l, r: l["rows"][0].__setitem__("cell_coordinate_volume", "1"),
            True,
        ),
        (
            "TAMPER_INPUT_PIN",
            lambda l, r: r["pins"].__setitem__(R275.name, "0" * 64),
            True,
        ),
        (
            "PROMOTE_OCCURRENCE_CREDIT",
            lambda l, r: l["rows"][0].__setitem__("formal_occurrence_credit", 1),
            True,
        ),
        (
            "FORGE_LEDGER_FILE_DIGEST",
            forge_ledger_file_digest,
            False,
        ),
        (
            "FORGE_ROW_HASH",
            lambda l, r: l["rows"][0].__setitem__("row_sha256", "0" * 64),
            False,
        ),
        (
            "FORGE_LEDGER_ROWS_HASH",
            lambda l, r: l.__setitem__("rows_sha256", "0" * 64),
            False,
        ),
        (
            "FORGE_RESULT_OBJECT_DIGEST",
            lambda l, r: r.__setitem__("result_sha256", "0" * 64),
            False,
        ),
        (
            "FORGE_CM2_GO",
            lambda l, r: r.__setitem__("status", "PASS_UNCONDITIONAL_CM2_GO"),
            True,
        ),
    ]
    rejected: list[str] = []
    reclosed: list[str] = []
    for attack_id, mutate, should_reclose in attacks:
        attacked_ledger = deepcopy(ledger)
        attacked_result = deepcopy(result)
        mutate(attacked_ledger, attacked_result)
        if should_reclose:
            reclose(attacked_ledger, attacked_result)
            reclosed.append(attack_id)
        try:
            audit_candidate(
                attacked_ledger,
                attacked_result,
                expected_rows,
                reconstruction,
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
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_attacks_rejected": len(rejected) == len(attacks),
        "reclosed_attack_count": len(reclosed),
        "reclosed_attack_ids": reclosed,
        "rejected_attack_ids": rejected,
    }


def verify() -> dict[str, Any]:
    for name, expected in ARTIFACT_PINS.items():
        need(file_sha256(HERE / name) == expected, f"pin:{name}")
    need(PRODUCER.stem not in sys.modules, "Round286 producer imported")

    regions = load_round275_regions()
    partial_ids, round284_result = load_round284_partial_ids(regions)
    bindings, wanted_atoms = load_round280_bindings(regions, partial_ids)
    atoms, frozen_support_box_count = load_referenced_round279_atoms(wanted_atoms)

    first_rows, first_reconstruction = reconstruct(
        regions,
        partial_ids,
        bindings,
        atoms,
        DUAL_REPLAY_SEEDS[0],
    )
    second_rows, second_reconstruction = reconstruct(
        regions,
        partial_ids,
        bindings,
        atoms,
        DUAL_REPLAY_SEEDS[1],
    )
    need(first_rows == second_rows, "Round286 dual-seed rows")
    need(
        first_reconstruction == second_reconstruction,
        "Round286 dual-seed reconstruction",
    )
    del second_rows
    gc.collect()

    stored_ledger = read_gzip_json(LEDGER)
    stored_result = read_json(RESULT)
    need(
        deterministic_gzip_bytes(stored_ledger) == LEDGER.read_bytes(),
        "Round286 deterministic gzip",
    )
    need(
        canonical(stored_result) + b"\n" == RESULT.read_bytes(),
        "Round286 canonical result bytes",
    )
    audit_candidate(
        stored_ledger,
        stored_result,
        first_rows,
        first_reconstruction,
    )
    attacks = run_attacks(
        stored_ledger,
        stored_result,
        first_rows,
        first_reconstruction,
    )

    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_ROUND286_EXACT_REFINEMENT__"
            "2184_PARTIAL_REGIONS__7616_CELLS__5700_ALIAS_SUBCELLS__"
            "1916_NEW_SUBCELLS__ZERO_MULTI_ATOM__ZERO_CREDIT"
        ),
        "pins": ARTIFACT_PINS,
        "independence_contract": {
            "Round286_producer_imported_or_executed": False,
            "producer_treated_only_as_pinned_inert_bytes": True,
            "exact_arithmetic": "fractions.Fraction",
            "expected_rows_reconstructed_from_R275_R279_R280_R284_before_candidate_audit":
                True,
            "Round284_result_object_sha256":
                round284_result["result_sha256"],
        },
        "reconstruction": {
            "Round275_region_count": len(regions),
            "Round284_partial_region_count": len(partial_ids),
            "Round279_frozen_atom_count": 332016,
            "Round279_frozen_support_box_count": frozen_support_box_count,
            "Round279_referenced_atom_count": len(atoms),
            "Round280_selected_binding_count": len(bindings),
            **first_reconstruction,
        },
        "dual_seed_replay": {
            "replay_seeds": list(DUAL_REPLAY_SEEDS),
            "partial_region_order_independently_permuted_for_each_seed": True,
            "reconstructed_rows_identical": True,
            "reconstructed_rows_sha256_by_seed": {
                str(seed): first_reconstruction["rows_sha256"]
                for seed in DUAL_REPLAY_SEEDS
            },
            "verification_replay_is_PYTHONHASHSEED_independent": True,
        },
        "attacks": attacks,
        "zero_credit_contract": {
            "Round275_region_rows_zero_credit": True,
            "Round279_atom_rows_zero_credit": True,
            "Round280_binding_rows_zero_credit": True,
            "Round284_partial_disposition_zero_credit": True,
            "Round286_rows_zero_credit": True,
            "alias_subcells_are_candidates_only": True,
            "uncovered_subcells_are_candidates_only": True,
            "occurrence_ids_issued": 0,
            "seam_edges_issued": 0,
            "frozen_expanded_occurrences": 126468,
            "frozen_quotient_components": 63224,
        },
        "strict_nonpromotion": stored_result["strict_nonpromotion"],
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def atomic_write(path: Path, payload: bytes) -> None:
    target = path if path.is_absolute() else (Path.cwd() / path)
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
        default="286071",
        help=(
            "Accepted for external cold-replay symmetry; output is deliberately "
            "seed-independent."
        ),
    )
    args = parser.parse_args()
    value = verify()
    atomic_write(args.output, canonical(value) + b"\n")


if __name__ == "__main__":
    main()
