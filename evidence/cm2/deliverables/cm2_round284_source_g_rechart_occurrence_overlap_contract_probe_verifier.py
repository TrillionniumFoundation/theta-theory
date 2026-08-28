#!/usr/bin/env python3
"""Independent verifier for the Round284 rechart/atom overlap contract.

The Round284 producer is pinned as inert source bytes and is never imported or
executed.  This verifier starts from the frozen Round275 rational rechart
regions, the Round279 canonical atom support boxes, the Round280 region/atom
bindings, and the Round280 occurrence-identity contract.  It independently
recomputes every selected region-box versus atom-box relation with exact
``fractions.Fraction`` arithmetic, reconstructs all 13,788 Round284 rows, and
checks the complete candidate ledger and summary result.

The result is deliberately ZERO-CREDIT.  Containment is only an alias
candidate, partial positive-volume overlap remains refinement-required, and
positive-area face contact never creates occurrence identity or component
credit.
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
PREFIX = "cm2_round284_source_g_rechart_occurrence_overlap_contract_probe"
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
R280_IDENTITY = HERE / (
    "cm2_round280_source_g_expanded_occurrence_identity_contract_audit_"
    "result.json"
)

VERIFICATION_SCHEMA = (
    "cm2.round284.source-g-rechart-occurrence-overlap-contract-probe."
    "verification.v1"
)
LEDGER_SCHEMA = "cm2.round284.source-g-rechart-occurrence-overlap-contract.ledger.v1"
RESULT_SCHEMA = (
    "cm2.round284.source-g-rechart-occurrence-overlap-contract-probe.v1"
)

INPUT_PINS = {
    R275.name:
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R279_ATOMS.name:
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    R280_BINDINGS.name:
        "8354eb042455e6d3ed591ee1620c9fc9def1af916a9bfbc0bf42e473e3e6e58b",
    R280_IDENTITY.name:
        "873974c8b343961f9e7c1674a946681749a3c0267bc57a1ccc147ccd21b3bdfc",
}

ARTIFACT_PINS = {
    **INPUT_PINS,
    PRODUCER.name:
        "fea66702762eb6031c11a591e4f63000aa84645d3b1a471e92fd34c8c0e9ac35",
    LEDGER.name:
        "39b69e0c5d249454c7ff13da99b260d3a7fabfa03c8ad6866035cbcaa883eb92",
    RESULT.name:
        "e25dd7b494ad2c2ccddc17601d28136c1919a3b16e41f008669bd6c14a513692",
}

CLASS_CONTAINED = (
    "CONTAINED_ALIAS_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED"
)
CLASS_PARTIAL = "PARTIAL_OVERLAP__EXACT_REFINEMENT_REQUIRED"
CLASS_DISJOINT = (
    "NEW_DISJOINT_CANDIDATE__OCCURRENCE_ID_NOT_YET_ISSUED"
)
EXPECTED_CLASSIFICATION_HISTOGRAM = {
    CLASS_CONTAINED: 2476,
    CLASS_DISJOINT: 9128,
    CLASS_PARTIAL: 2184,
}
EXPECTED_RELATION_HISTOGRAM = {
    "PARTIAL_POSITIVE_VOLUME_OVERLAP": 5572,
    "POSITIVE_AREA_COMMON_FACE_ONLY": 5544,
    "REGION_STRICTLY_CONTAINED_IN_ATOM": 2476,
}

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
DUAL_REPLAY_SEEDS = (284071, 284072)

ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


class VerificationError(RuntimeError):
    """Raised when any frozen or candidate contract fails."""


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
    hashes = []
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
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "Round275 result digest")
    result = wrapper["result"]
    need(
        result["schema"]
        == "cm2.round275.source-g-complete-reverse-rechart-materialization.v1",
        "Round275 schema",
    )
    need(
        result["census"]["total_materialized_connected_region_count"] == 13788
        and result["census"]["strict_cover_region_count"] == 5288
        and result["census"]["arrangement_region_count"] == 8500,
        "Round275 census",
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
    for row in rows:
        need(
            row["connected_open_region"]
            and row["occurrence_credit"] == 0
            and row["component_credit"] == 0
            and row["maximality_credit"] == 0,
            f"Round275 zero credit:{row['reverse_rechart_region_row_id']}",
        )
        need(
            row["complete_10_field_return_signature_sha256"]
            == digest(row["local_return_signature"]),
            f"Round275 signature closure:{row['reverse_rechart_region_row_id']}",
        )
        box = tuple(map(Q, row["adjacent_rational_region_box"]))
        need(
            len(box) == 6
            and all(box[2 * axis] < box[2 * axis + 1] for axis in range(3)),
            f"Round275 positive box:{row['reverse_rechart_region_row_id']}",
        )
    regions = {row["reverse_rechart_region_row_id"]: row for row in rows}
    need(len(regions) == 13788, "Round275 region id universe")
    return regions


def load_round280_bindings(
    regions: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], set[str]]:
    ledger = read_gzip_json(R280_BINDINGS)
    need(
        ledger["schema"] == "cm2.round280.rechart-region-incidence.zero-credit.v1",
        "Round280 binding schema",
    )
    need(
        ledger["status"] == "ROUND280_RECHART_REGION_INCIDENCE_PROBE__ZERO_CREDIT"
        and ledger["strict_nonpromotion"] is True,
        "Round280 binding status",
    )
    rows = verify_closed_ledger(
        "Round280 region bindings",
        ledger,
        "Round275_region_incidence_row_id",
        13788,
    )
    seen_regions: set[str] = set()
    wanted_atoms: set[str] = set()
    for binding in rows:
        region_id = binding["Round275_reverse_rechart_region_row_id"]
        need(region_id in regions, f"Round280 known region:{region_id}")
        need(region_id not in seen_regions, f"Round280 duplicate region:{region_id}")
        seen_regions.add(region_id)
        region = regions[region_id]
        atom_ids = binding["matching_atom_ids"]
        need(
            binding["matching_atom_count"] == len(atom_ids)
            and len(atom_ids) == len(set(atom_ids)),
            f"Round280 atom binding count:{region_id}",
        )
        need(
            binding["adjacent_chart"] == region["adjacent_chart"]
            and binding["source_chart"] == region["source_chart"]
            and binding["owner_target"] == region["owner_target"]
            and binding["source_guard_row_id"] == region["source_guard_row_id"]
            and binding["source_round"] == region["source_round"]
            and binding["complete_10_field_return_signature_sha256"]
            == region["complete_10_field_return_signature_sha256"],
            f"Round280/Round275 provenance:{region_id}",
        )
        need(
            binding["exact_coordinate_identity_verified"] is True
            and binding["exact_algebraic_image_intersection_positive"] is True,
            f"Round280 exact binding evidence:{region_id}",
        )
        need(
            binding["formal_component_union_credit"] == 0
            and binding["formal_expanded_occurrence_credit"] == 0
            and binding["formal_maximality_credit"] == 0,
            f"Round280 binding zero credit:{region_id}",
        )
        wanted_atoms.update(atom_ids)
    need(seen_regions == set(regions), "Round280 complete Round275 binding universe")
    return rows, wanted_atoms


def load_referenced_round279_atoms(
    wanted_atoms: set[str],
) -> tuple[dict[str, dict[str, Any]], int]:
    """Validate the frozen atom census while retaining only referenced rows."""

    ledger = read_gzip_json(R279_ATOMS)
    need(
        ledger["schema"] == "cm2.round279.canonical-collar-atom-ledger.v1",
        "Round279 atom schema",
    )
    need(
        ledger["status"] == "ROUND279_CANONICAL_COLLAR_ATOMS_FROZEN__ZERO_CREDIT",
        "Round279 atom status",
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
        "Round279 frozen atom header",
    )
    need(
        ledger["strict_nonpromotion"]
        == {
            "component_credit": 0,
            "expanded_occurrence_credit": 0,
            "maximality_credit": 0,
        },
        "Round279 atom zero-credit summary",
    )
    rows = ledger["rows"]
    need(len(rows) == 332016, "Round279 atom row count")
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
            f"Round279 atom zero credit:{atom_id}",
        )
        boxes = row["frozen_true_support_boxes"]
        need(boxes and all(len(box) == 6 for box in boxes), f"Round279 atom boxes:{atom_id}")
        support_box_count += len(boxes)
        if atom_id in wanted_atoms:
            payload = dict(row)
            stored_hash = payload.pop("row_sha256")
            need(stored_hash == digest(payload), f"Round279 selected row closure:{atom_id}")
            need(
                row["complete_10_field_return_signature_sha256"]
                == digest(row["complete_10_field_return_signature"]),
                f"Round279 selected signature closure:{atom_id}",
            )
            selected[atom_id] = row
    need(len(seen) == 332016, "Round279 atom id universe")
    need(set(selected) == wanted_atoms, "Round279 referenced atom coverage")
    del rows, ledger, seen
    gc.collect()
    return selected, support_box_count


def verify_round280_identity_contract() -> dict[str, Any]:
    wrapper = read_json(R280_IDENTITY)
    need(set(wrapper) == {"result", "result_sha256"}, "Round280 identity wrapper")
    need(
        wrapper["result_sha256"] == digest(wrapper["result"]),
        "Round280 identity digest",
    )
    result = wrapper["result"]
    need(
        result["schema"]
        == "cm2.round280.source-g-expanded-occurrence-identity-contract-audit.v1",
        "Round280 identity schema",
    )
    need(
        result["status"]
        == (
            "PASS_ZERO_CREDIT_IDENTITY_CONTRACT_AUDIT__"
            "ROUND280_CLASS_AS_OCCURRENCE_SEMANTICS_REJECTED"
        ),
        "Round280 identity status",
    )
    disposition = result["Round275_reverse_rechart_disposition"]
    need(
        disposition["raw_connected_region_rows"] == 13788
        and disposition["raw_new_occurrence_seed_count_authorized"] == 0
        and disposition["candidate_total_436232_authorized"] is False
        and len(disposition["required_three_way_disposition_per_positive_open_piece"])
        == 3,
        "Round280 three-way disposition contract",
    )
    nonpromotion = result["strict_nonpromotion"]
    zero_fields = (
        "DSU_rank_reduction_credit",
        "Jx_Jy_same_point_glue_credit",
        "component_edge_credit",
        "exact_key_fibre_credit",
        "global_disposition_credit",
        "maximality_credit",
        "new_expanded_occurrence_credit",
        "occurrence_identity_collapse_credit",
    )
    need(all(nonpromotion[field] == 0 for field in zero_fields), "Round280 zero credit")
    need(
        nonpromotion["expanded_occurrences"] == 126468
        and nonpromotion["quotient_components"] == 63224
        and nonpromotion["Gate5"] == "10/18"
        and nonpromotion["D02"] == "BLOCKED"
        and nonpromotion["CM2"] == "NO-GO_FOR_CLAIM",
        "Round280 frozen baseline",
    )
    return result


def exact_box_relation(
    region: tuple[Q, Q, Q, Q, Q, Q],
    atom: tuple[Q, Q, Q, Q, Q, Q],
) -> str | None:
    """Classify one closed outer-box pair by positive-open intersection."""

    intersections = [
        (
            max(region[2 * axis], atom[2 * axis]),
            min(region[2 * axis + 1], atom[2 * axis + 1]),
        )
        for axis in range(3)
    ]
    positive_axes = [upper > lower for lower, upper in intersections]
    if all(positive_axes):
        if region == atom:
            return "EXACT_EQUAL_BOX"
        region_in_atom = all(
            atom[2 * axis] <= region[2 * axis]
            and region[2 * axis + 1] <= atom[2 * axis + 1]
            for axis in range(3)
        )
        atom_in_region = all(
            region[2 * axis] <= atom[2 * axis]
            and atom[2 * axis + 1] <= region[2 * axis + 1]
            for axis in range(3)
        )
        if region_in_atom:
            return "REGION_STRICTLY_CONTAINED_IN_ATOM"
        if atom_in_region:
            return "ATOM_STRICTLY_CONTAINED_IN_REGION"
        return "PARTIAL_POSITIVE_VOLUME_OVERLAP"
    zero_axes = sum(upper == lower for lower, upper in intersections)
    if sum(positive_axes) == 2 and zero_axes == 1:
        return "POSITIVE_AREA_COMMON_FACE_ONLY"
    return None


def reconstruct(
    regions: dict[str, dict[str, Any]],
    bindings: list[dict[str, Any]],
    atoms: dict[str, dict[str, Any]],
    replay_seed: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    ordered_bindings = list(bindings)
    random.Random(replay_seed).shuffle(ordered_bindings)
    rows: list[dict[str, Any]] = []
    classifications: Counter[str] = Counter()
    relation_histogram: Counter[str] = Counter()
    face_contact_regions = 0
    region_atom_box_comparisons = 0

    for binding in ordered_bindings:
        region_id = binding["Round275_reverse_rechart_region_row_id"]
        region = regions[region_id]
        region_box = tuple(map(Q, region["adjacent_rational_region_box"]))
        relations: list[dict[str, Any]] = []
        for atom_id in binding["matching_atom_ids"]:
            atom = atoms[atom_id]
            need(
                atom["source_chart"] == region["adjacent_chart"]
                and atom["owner_target"] == region["owner_target"]
                and atom["complete_10_field_return_signature_sha256"]
                == region["complete_10_field_return_signature_sha256"],
                f"Round279/Round275 signature provenance:{region_id}:{atom_id}",
            )
            for box_index, stored_box in enumerate(atom["frozen_true_support_boxes"]):
                atom_box = tuple(map(Q, stored_box))
                need(
                    all(atom_box[2 * axis] < atom_box[2 * axis + 1] for axis in range(3)),
                    f"Round279 positive support box:{atom_id}:{box_index}",
                )
                region_atom_box_comparisons += 1
                relation = exact_box_relation(region_box, atom_box)
                if relation is not None:
                    relation_histogram[relation] += 1
                    relations.append(
                        {
                            "canonical_atom_id": atom_id,
                            "atom_support_box_index": box_index,
                            "relation": relation,
                        }
                    )

        relations.sort(
            key=lambda item: (
                item["canonical_atom_id"],
                item["atom_support_box_index"],
                item["relation"],
            )
        )
        kinds = {item["relation"] for item in relations}
        need(
            "EXACT_EQUAL_BOX" not in kinds
            and "ATOM_STRICTLY_CONTAINED_IN_REGION" not in kinds,
            f"Round284 forbidden identity direction:{region_id}",
        )
        if "PARTIAL_POSITIVE_VOLUME_OVERLAP" in kinds:
            classification = CLASS_PARTIAL
        elif "REGION_STRICTLY_CONTAINED_IN_ATOM" in kinds:
            classification = CLASS_CONTAINED
        else:
            classification = CLASS_DISJOINT
        has_face_contact = "POSITIVE_AREA_COMMON_FACE_ONLY" in kinds
        classifications[classification] += 1
        face_contact_regions += int(has_face_contact)

        payload = {
            "Round284_region_overlap_row_id":
                "round284-region-overlap:" + digest(region_id),
            "Round275_region_id": region_id,
            "source_chart": region["source_chart"],
            "adjacent_chart": region["adjacent_chart"],
            "parent_id": region["parent_id"],
            "owner_target": region["owner_target"],
            "complete_10_field_return_signature_sha256":
                region["complete_10_field_return_signature_sha256"],
            "classification": classification,
            "positive_area_face_contact_present": has_face_contact,
            "relation_count": len(relations),
            "relations": relations,
            "formal_occurrence_credit": 0,
            "formal_component_credit": 0,
            "formal_maximality_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
        }
        row = dict(payload)
        row["row_sha256"] = digest(payload)
        rows.append(row)

    rows.sort(key=lambda row: row["Round284_region_overlap_row_id"])
    census = {
        "Round275_region_count": len(rows),
        "classification_histogram": dict(sorted(classifications.items())),
        "relation_histogram": dict(sorted(relation_histogram.items())),
        "region_with_any_face_contact_count": face_contact_regions,
        "exact_equal_box_count": relation_histogram["EXACT_EQUAL_BOX"],
        "atom_contained_in_region_count":
            relation_histogram["ATOM_STRICTLY_CONTAINED_IN_REGION"],
    }
    need(len(rows) == 13788, "Round284 reconstructed region count")
    need(
        census["classification_histogram"] == EXPECTED_CLASSIFICATION_HISTOGRAM,
        "Round284 reconstructed three-way census",
    )
    need(
        census["relation_histogram"] == EXPECTED_RELATION_HISTOGRAM
        and face_contact_regions == 3036
        and census["exact_equal_box_count"] == 0
        and census["atom_contained_in_region_count"] == 0,
        "Round284 reconstructed relation census",
    )
    reconstruction = {
        "census": census,
        "region_atom_support_box_comparison_count": region_atom_box_comparisons,
        "positive_relation_row_count": sum(relation_histogram.values()),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest(
            [row["Round284_region_overlap_row_id"] for row in rows]
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
    need(ledger["schema"] == LEDGER_SCHEMA, "Round284 ledger schema")
    rows = verify_closed_ledger(
        "Round284 candidate ledger",
        ledger,
        "Round284_region_overlap_row_id",
        13788,
    )
    need(
        [row["Round284_region_overlap_row_id"] for row in rows]
        == sorted(row["Round284_region_overlap_row_id"] for row in rows),
        "Round284 canonical row order",
    )
    need(rows == expected_rows, "Round284 exact independent row reconstruction")

    need(result["schema"] == RESULT_SCHEMA, "Round284 result schema")
    need(
        result["status"]
        == "PASS_ROUND284_RECHART_OCCURRENCE_OVERLAP_CONTRACT_PROBE__ZERO_CREDIT",
        "Round284 result status",
    )
    need(
        result["result_sha256"]
        == digest({key: value for key, value in result.items() if key != "result_sha256"}),
        "Round284 result closure",
    )
    need(result["pins"] == INPUT_PINS, "Round284 producer input pins")
    need(result["census"] == reconstruction["census"], "Round284 result census")
    need(
        result["semantic_contract"]
        == {
            "contained_region_is_alias_candidate_not_new_occurrence": True,
            "partial_positive_volume_overlap_requires_exact_refinement": True,
            "face_contact_never_implies_occurrence_identity": True,
            "disjoint_region_is_only_a_new_occurrence_candidate_until_seam_and_frontier_closure":
                True,
        },
        "Round284 semantic contract",
    )
    need(
        result["strict_nonpromotion"] == expected_strict_nonpromotion(),
        "Round284 strict nonpromotion",
    )
    need(
        all(result["strict_nonpromotion"][field] == 0 for field in RESULT_ZERO_FIELDS),
        "Round284 zero result credit",
    )
    need(
        result["ledger"]
        == {
            "filename": LEDGER.name,
            "row_count": 13788,
            "rows_sha256": ledger["rows_sha256"],
            "file_sha256": hashlib.sha256(deterministic_gzip_bytes(ledger)).hexdigest(),
        },
        "Round284 result/ledger binding",
    )
    for row in rows:
        need(
            all(row[field] == 0 for field in ROW_ZERO_FIELDS),
            f"Round284 row zero credit:{row['Round284_region_overlap_row_id']}",
        )
        kinds = {relation["relation"] for relation in row["relations"]}
        if row["classification"] == CLASS_CONTAINED:
            need(
                "REGION_STRICTLY_CONTAINED_IN_ATOM" in kinds
                and "PARTIAL_POSITIVE_VOLUME_OVERLAP" not in kinds,
                "Round284 contained semantics",
            )
        elif row["classification"] == CLASS_PARTIAL:
            need(
                "PARTIAL_POSITIVE_VOLUME_OVERLAP" in kinds,
                "Round284 partial semantics",
            )
        else:
            need(
                row["classification"] == CLASS_DISJOINT
                and not kinds.intersection(
                    {
                        "EXACT_EQUAL_BOX",
                        "REGION_STRICTLY_CONTAINED_IN_ATOM",
                        "ATOM_STRICTLY_CONTAINED_IN_REGION",
                        "PARTIAL_POSITIVE_VOLUME_OVERLAP",
                    }
                ),
                "Round284 disjoint semantics",
            )
        need(
            row["positive_area_face_contact_present"]
            == ("POSITIVE_AREA_COMMON_FACE_ONLY" in kinds),
            "Round284 face-contact flag",
        )


def reclose(ledger: dict[str, Any], result: dict[str, Any]) -> None:
    for row in ledger["rows"]:
        payload = dict(row)
        payload.pop("row_sha256", None)
        row["row_sha256"] = digest(payload)
    ledger["row_count"] = len(ledger["rows"])
    ledger["rows_sha256"] = digest(ledger["rows"])
    ledger["row_ids_sha256"] = digest(
        [row["Round284_region_overlap_row_id"] for row in ledger["rows"]]
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
    def first_relation_row(candidate: dict[str, Any]) -> dict[str, Any]:
        return next(row for row in candidate["rows"] if row["relations"])

    def first_face_only_row(candidate: dict[str, Any]) -> dict[str, Any]:
        return next(
            row
            for row in candidate["rows"]
            if row["positive_area_face_contact_present"]
            and row["classification"] == CLASS_DISJOINT
        )

    attacks: list[
        tuple[str, Callable[[dict[str, Any], dict[str, Any]], None]]
    ] = [
        ("DROP_REGION_ROW", lambda l, r: l["rows"].pop()),
        (
            "DUPLICATE_REGION_ROW",
            lambda l, r: l["rows"].append(deepcopy(l["rows"][0])),
        ),
        (
            "FORGE_CONTAINED_AS_DISJOINT",
            lambda l, r: next(
                row for row in l["rows"] if row["classification"] == CLASS_CONTAINED
            ).__setitem__("classification", CLASS_DISJOINT),
        ),
        (
            "FORGE_PARTIAL_AS_ALIAS",
            lambda l, r: next(
                row for row in l["rows"] if row["classification"] == CLASS_PARTIAL
            ).__setitem__("classification", CLASS_CONTAINED),
        ),
        (
            "PROMOTE_FACE_CONTACT_TO_ALIAS",
            lambda l, r: first_face_only_row(l).__setitem__(
                "classification", CLASS_CONTAINED
            ),
        ),
        (
            "FORGE_RELATION_KIND",
            lambda l, r: first_relation_row(l)["relations"][0].__setitem__(
                "relation", "EXACT_EQUAL_BOX"
            ),
        ),
        (
            "FORGE_RELATION_ATOM",
            lambda l, r: first_relation_row(l)["relations"][0].__setitem__(
                "canonical_atom_id", "round279-collar-atom:" + "0" * 64
            ),
        ),
        (
            "FORGE_RELATION_BOX_INDEX",
            lambda l, r: first_relation_row(l)["relations"][0].__setitem__(
                "atom_support_box_index", 999
            ),
        ),
        (
            "PROMOTE_ROW_OCCURRENCE_CREDIT",
            lambda l, r: l["rows"][0].__setitem__("formal_occurrence_credit", 1),
        ),
        (
            "PROMOTE_ROW_COMPONENT_CREDIT",
            lambda l, r: l["rows"][0].__setitem__("formal_component_credit", 1),
        ),
        (
            "PROMOTE_ROW_MAXIMALITY_CREDIT",
            lambda l, r: l["rows"][0].__setitem__("formal_maximality_credit", 1),
        ),
        (
            "PROMOTE_ROW_JX_JY_GLUE",
            lambda l, r: l["rows"][0].__setitem__(
                "Jx_Jy_same_point_glue_credit", 1
            ),
        ),
        (
            "FORGE_THREE_WAY_CENSUS",
            lambda l, r: r["census"]["classification_histogram"].__setitem__(
                CLASS_DISJOINT, 9127
            ),
        ),
        (
            "FORGE_SEMANTIC_CONTRACT",
            lambda l, r: r["semantic_contract"].__setitem__(
                "face_contact_never_implies_occurrence_identity", False
            ),
        ),
        (
            "PROMOTE_RESULT_OCCURRENCE_CREDIT",
            lambda l, r: r["strict_nonpromotion"].__setitem__(
                "occurrence_credit", 1
            ),
        ),
        (
            "FORGE_QUOTIENT",
            lambda l, r: r["strict_nonpromotion"].__setitem__("quotient", 63223),
        ),
        (
            "FORGE_CM2_GO",
            lambda l, r: r.__setitem__("status", "PASS_UNCONDITIONAL_CM2_GO"),
        ),
    ]
    rejected: list[str] = []
    for attack_id, mutate in attacks:
        attacked_ledger = deepcopy(ledger)
        attacked_result = deepcopy(result)
        mutate(attacked_ledger, attacked_result)
        reclose(attacked_ledger, attacked_result)
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
        ):
            rejected.append(attack_id)
        else:
            raise VerificationError(f"attack accepted:{attack_id}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_attacks_rejected": len(rejected) == len(attacks),
        "all_attacks_reclosed_at_row_ledger_and_result_levels": True,
        "rejected_attack_ids": rejected,
    }


def verify() -> dict[str, Any]:
    for name, expected in ARTIFACT_PINS.items():
        need(file_sha256(HERE / name) == expected, f"pin:{name}")
    need(PRODUCER.stem not in sys.modules, "Round284 producer imported")

    identity_contract = verify_round280_identity_contract()
    regions = load_round275_regions()
    bindings, wanted_atoms = load_round280_bindings(regions)
    atoms, frozen_support_box_count = load_referenced_round279_atoms(wanted_atoms)

    first_rows, first_reconstruction = reconstruct(
        regions, bindings, atoms, DUAL_REPLAY_SEEDS[0]
    )
    second_rows, second_reconstruction = reconstruct(
        regions, bindings, atoms, DUAL_REPLAY_SEEDS[1]
    )
    need(first_rows == second_rows, "dual-seed reconstructed rows differ")
    need(
        first_reconstruction == second_reconstruction,
        "dual-seed reconstructed census differs",
    )
    del second_rows
    gc.collect()

    stored_ledger = read_gzip_json(LEDGER)
    stored_result = read_json(RESULT)
    need(
        deterministic_gzip_bytes(stored_ledger) == LEDGER.read_bytes(),
        "Round284 deterministic GZIP bytes",
    )
    need(
        canonical(stored_result) + b"\n" == RESULT.read_bytes(),
        "Round284 canonical result bytes",
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

    audit_nonpromotion = identity_contract["strict_nonpromotion"]
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_INDEPENDENT_ROUND284_RECHART_OCCURRENCE_OVERLAP_CONTRACT_"
            "PROBE__2476_ALIAS_CANDIDATES__2184_REFINEMENTS__"
            "9128_DISJOINT_CANDIDATES__ZERO_CREDIT"
        ),
        "pins": ARTIFACT_PINS,
        "independence_contract": {
            "Round284_producer_imported_or_executed": False,
            "producer_treated_only_as_pinned_inert_bytes": True,
            "exact_arithmetic": "fractions.Fraction",
            "expected_rows_reconstructed_from_R275_R279_R280_before_candidate_audit":
                True,
        },
        "reconstruction": {
            "Round275_region_count": len(regions),
            "Round279_frozen_atom_count": 332016,
            "Round279_frozen_support_box_count": frozen_support_box_count,
            "Round279_referenced_atom_count": len(atoms),
            "Round280_region_binding_count": len(bindings),
            "region_atom_support_box_comparison_count":
                first_reconstruction["region_atom_support_box_comparison_count"],
            "positive_relation_count":
                first_reconstruction["positive_relation_row_count"],
            "classification_histogram":
                first_reconstruction["census"]["classification_histogram"],
            "relation_histogram":
                first_reconstruction["census"]["relation_histogram"],
            "region_with_any_face_contact_count":
                first_reconstruction["census"][
                    "region_with_any_face_contact_count"
                ],
            "rows_sha256": first_reconstruction["rows_sha256"],
            "row_ids_sha256": first_reconstruction["row_ids_sha256"],
            "row_hashes_sha256": first_reconstruction["row_hashes_sha256"],
        },
        "dual_seed_replay": {
            "replay_seeds": list(DUAL_REPLAY_SEEDS),
            "binding_order_independently_permuted_for_each_seed": True,
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
            "Round280_new_occurrence_seed_count_authorized":
                identity_contract["Round275_reverse_rechart_disposition"][
                    "raw_new_occurrence_seed_count_authorized"
                ],
            "Round284_rows_zero_credit": True,
            "contained_rows_are_alias_candidates_only": True,
            "partial_overlap_rows_remain_refinement_required": True,
            "face_contact_has_no_identity_or_component_credit": True,
            "disjoint_rows_have_no_issued_occurrence_ids": True,
            "frozen_expanded_occurrences":
                audit_nonpromotion["expanded_occurrences"],
            "frozen_quotient_components":
                audit_nonpromotion["quotient_components"],
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
        default="284071",
        help=(
            "Accepted for external PYTHONHASHSEED cold-replay symmetry; "
            "verification bytes are deliberately seed-independent."
        ),
    )
    args = parser.parse_args()
    value = verify()
    atomic_write(args.output, canonical(value) + b"\n")


if __name__ == "__main__":
    main()
