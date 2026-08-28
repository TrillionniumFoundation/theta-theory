#!/usr/bin/env python3
"""Round299D complete zero-credit Round275 region common-face frontier.

Round280 explicitly did not construct a complete region-to-region frontier.
Rounds292/299A only saw the 10,020 Round287 potential-new-support unions, so
they cannot cover Round275 regions which were wholly aliased or partitioned
among several existing registry supports.

This diagnostic:

1. enumerates every positive-area common coordinate face among all 13,788
   Round275 regions after imposing the exact physical ``t^2`` interval;
2. replays every graph-constrained face with the Round299B rational-sqrt/Arb
   diagnostic;
3. binds every region to all formal Round294 occurrence endpoints represented
   by its Round292 cells and Round294 representation bindings;
4. expands accepted region faces to a deduplicated occurrence-pair frontier;
5. compares that frontier with ordinary, seam, lower, and Round299A/B/C pairs.

The signed-factor witness is still diagnostic evidence, not the final guided
positive patch/corridor required for formal promotion.  Every formal credit is
therefore zero.

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
import cm2_round299b_source_g_r292_signed_support_face_replay_diagnostic as r299b


PREFIX = "cm2_round299d_source_g_complete_r275_region_face_frontier_diagnostic"
OUTPUT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"

R275 = "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
R287 = "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe_ledger.json.gz"
R292 = "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_ledger.json.gz"
R294R = "cm2_round294_source_g_occurrence_registry_atomic_promotion_registry_ledger.json.gz"
R294B = "cm2_round294_source_g_occurrence_registry_atomic_promotion_representation_binding_ledger.json.gz"
R299AL = "cm2_round299_source_g_r292_complete_common_face_frontier_diagnostic_probe_ledger.json.gz"
R299BL = "cm2_round299b_source_g_r292_signed_support_face_replay_diagnostic_ledger.json.gz"
R299CL = "cm2_round299c_source_g_r292_registry_support_boundary_face_diagnostic_ledger.json.gz"
R295A = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "physical_witness_incidence_binding_ledger.json.gz"
)
R296 = "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_edge_ledger.json.gz"
R297 = "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_edge_ledger.json.gz"

PINS = {
    R275: "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R287: "29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a",
    R292: "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    R294R: "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R294B: "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",
    R299AL: "b9de98c7ccb3051ea7af3070e1eb62ce059d21f0b22b9b3f5007c1847c667845",
    R299BL: "f7973edfe005435e162527d8eb3be98284963718146bd99812c243702d2e6e50",
    R299CL: "8bd0d36cd48319a9930d43f35536ce4d59697a28f09235ae373bfacf9c0d1acc",
    R295A: "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R296: "1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7",
    R297: "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
}

SCHEMA = "cm2.round299d.source-g-complete-r275-region-face-frontier-diagnostic.v1"
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


def read_json(name: str) -> dict[str, Any]:
    path = HERE / name
    need(file_sha256(path) == PINS[name], f"pin:{name}")
    return json.loads(path.read_bytes())


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
    need(left != right, "nonself occurrence pair")
    return tuple(sorted((left, right)))


def load_regions() -> dict[str, dict[str, Any]]:
    wrapper = read_json(R275)
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "R275 result")
    result = wrapper["result"]
    rows = [
        row
        for table in ("strict_region_ledger", "arrangement_region_ledger")
        for row in result[table]["rows"]
    ]
    need(len(rows) == 13_788, "R275 region census")
    return {row["reverse_rechart_region_row_id"]: row for row in rows}


def load_region_dispositions() -> dict[str, dict[str, Any]]:
    document = read_gzip(R287)
    rows = document["region_rows"]
    need(
        len(rows) == document["region_row_count"] == 13_788
        and digest(rows) == document["region_rows_sha256"],
        "R287 region disposition table",
    )
    return {row["Round275_region_id"]: row for row in rows}


def transformed_region_rows(
    regions: dict[str, dict[str, Any]],
    dispositions: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    result = []
    for region_id, region in regions.items():
        disposition = dispositions[region_id]
        coordinate = tuple(map(Q, region["adjacent_rational_region_box"]))
        box = (
            Q(disposition["physical_t_square_open_interval"][0]),
            Q(disposition["physical_t_square_open_interval"][1]),
            coordinate[2],
            coordinate[3],
            coordinate[4],
            coordinate[5],
        )
        result.append(
            {
                "region_id": region_id,
                "region": region,
                "disposition": disposition,
                "source_chart": region["adjacent_chart"],
                "physical_t_sign": disposition["physical_t_sign"],
                "box": box,
                "signature_sha256":
                    region["complete_10_field_return_signature_sha256"],
                "support_class": (
                    "SIGNED_REGULAR_GRAPH_CONSTRAINED_SUPPORT"
                    if region.get("arrangement_classification")
                    == "REGULAR_GRAPH_CROSSING"
                    else "FULL_SIGNED_SUPPORT"
                ),
            }
        )
    result.sort(key=lambda row: row["region_id"])
    need(len(result) == 13_788, "transformed region census")
    return result


def region_endpoint_map(
    regions: dict[str, dict[str, Any]],
) -> dict[str, set[str]]:
    registry = read_gzip(R294R)["rows"]
    refined_component = {
        row["source_row_id"]: row["registry_occurrence_id"]
        for row in registry
        if row["registry_entry_kind"]
        == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
    }
    need(len(refined_component) == 9_404, "refined component map")

    result: dict[str, set[str]] = defaultdict(set)
    for row in read_gzip(R292)["rows"]:
        disposition = row.get("disposition")
        if disposition == (
            "EXACT_UNCOVERED_POSITIVE_OPEN_SLICE__"
            "MEMBER_OF_REFINED_PARENT_LOCAL_NEW_SUPPORT"
        ):
            result[row["Round275_region_id"]].add(
                refined_component[row["Round292_refined_new_support_component_id"]]
            )
        elif disposition == (
            "EXACT_EXISTING_OCCURRENCE_REPRESENTATION_SUBCOVER__"
            "NO_NEW_OCCURRENCE_ID"
        ):
            result[row["Round275_region_id"]].update(
                row["existing_occurrence_ids"]
            )
    for row in read_gzip(R294B)["rows"]:
        region_id = row.get("Round275_region_id")
        if region_id is not None:
            result[region_id].add(row["target_registry_occurrence_id"])

    need(set(result) == set(regions), "every R275 region has registry endpoint")
    histogram = Counter(len(result[region_id]) for region_id in regions)
    need(
        histogram
        == {1: 11_208, 2: 1_680, 3: 268, 4: 232,
            5: 220, 6: 76, 10: 88, 11: 16}
        and sum(map(len, result.values())) == 18_912,
        "region endpoint incidence census",
    )
    return result


def exact_face(
    left: tuple[Q, ...],
    right: tuple[Q, ...],
    axis: int,
) -> tuple[Q, ...] | None:
    if left[2 * axis + 1] != right[2 * axis]:
        return None
    result: list[Q] = []
    for current in range(3):
        if current == axis:
            value = left[2 * current + 1]
            result.extend((value, value))
            continue
        lower = max(left[2 * current], right[2 * current])
        upper = min(left[2 * current + 1], right[2 * current + 1])
        if not lower < upper:
            return None
        result.extend((lower, upper))
    return tuple(result)


def graph_metadata(row: dict[str, Any]) -> dict[str, Any] | None:
    region = row["region"]
    if row["support_class"] != "SIGNED_REGULAR_GRAPH_CONSTRAINED_SUPPORT":
        return None
    return {
        "region": region,
        "factor_identity": (
            region["adjacent_chart"],
            region["owner_target"],
            region["active_reason"],
        ),
        "desired_sign": region["active_factor_side_sign"],
    }


def classify_face(
    left: dict[str, Any],
    right: dict[str, Any],
    face: tuple[Q, ...],
    axis: int,
) -> tuple[str, str, list[dict[str, Any]], dict[str, Any] | None]:
    graphs = [
        graph for graph in (graph_metadata(left), graph_metadata(right))
        if graph is not None
    ]
    if not graphs:
        return (
            "NO_GRAPH_ENDPOINT",
            "ACCEPTED_FULL_SIGNED_SUPPORT_COORDINATE_FACE",
            [],
            None,
        )
    same_factor = (
        len(graphs) == 2
        and graphs[0]["factor_identity"] == graphs[1]["factor_identity"]
    )
    if (
        same_factor
        and graphs[0]["desired_sign"] != graphs[1]["desired_sign"]
    ):
        return (
            "SAME_ACTIVE_FACTOR__OPPOSITE_STRICT_DESIRED_SIDES",
            "EXCLUDED_NO_POSITIVE_AREA_FACE__COMMON_ZERO_SET_ONLY",
            [],
            None,
        )
    factor_relation = (
        "SAME_ACTIVE_FACTOR__SAME_STRICT_DESIRED_SIDE"
        if same_factor
        else "ONE_GRAPH_ENDPOINT__OTHER_ENDPOINT_FULL_SIGNED_SUPPORT"
    )
    region = graphs[0]["region"]
    replays = []
    for bits in r299b.REPLAY_BITS:
        state, extrema, enclosure = r299b.signed_state(
            region, face, left["physical_t_sign"], bits
        )
        replays.append(
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
    states = {replay["signed_region_face_state"] for replay in replays}
    extrema = {
        tuple(replay["active_factor_extremal_signs"]) for replay in replays
    }
    need(len(states) == len(extrema) == 1, "precision-stable region face")
    state = replays[-1]["signed_region_face_state"]
    if state == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL":
        return (
            factor_relation,
            "EXCLUDED_SIGNED_SUPPORT_EMPTY_ON_FACE",
            replays,
            None,
        )
    need(
        state in {"FULL_DESIRED_SIDE_SUPPORT", "CLIPPED_DESIRED_SIDE_SUPPORT"},
        "decisive region signed state",
    )
    witness = r299b.strict_desired_witness(
        region, face, axis, left["physical_t_sign"]
    )
    return (
        factor_relation,
        "ACCEPTED_SIGNED_SUPPORT_POSITIVE_AREA_FACE_DIAGNOSTIC",
        replays,
        witness,
    )


def enumerate_region_faces(
    regions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    lower: dict[tuple[str, int, int, Q], list[int]] = defaultdict(list)
    for index, row in enumerate(regions):
        for axis in range(3):
            lower[
                (
                    row["source_chart"],
                    row["physical_t_sign"],
                    axis,
                    row["box"][2 * axis],
                )
            ].append(index)
    rows = []
    for left_index, left in enumerate(regions):
        for axis in range(3):
            key = (
                left["source_chart"],
                left["physical_t_sign"],
                axis,
                left["box"][2 * axis + 1],
            )
            for right_index in lower.get(key, []):
                right = regions[right_index]
                face = exact_face(left["box"], right["box"], axis)
                if face is None:
                    continue
                relation, disposition, replays, witness = classify_face(
                    left, right, face, axis
                )
                payload = {
                    "Round299D_R275_region_common_face_row_id":
                        "round299d-r275-region-common-face:"
                        + digest(
                            [
                                left["region_id"],
                                right["region_id"],
                                axis,
                                list(map(qstr, face)),
                            ]
                        ),
                    "left_Round275_region_id": left["region_id"],
                    "right_Round275_region_id": right["region_id"],
                    "source_chart": left["source_chart"],
                    "physical_t_sign": left["physical_t_sign"],
                    "common_face_axis": axis,
                    "exact_positive_area_coordinate_face_t2_p_s": [
                        qstr(value) for value in face
                    ],
                    "left_support_class": left["support_class"],
                    "right_support_class": right["support_class"],
                    "same_complete_10_field_return_signature":
                        left["signature_sha256"] == right["signature_sha256"],
                    "left_complete_10_field_return_signature_sha256":
                        left["signature_sha256"],
                    "right_complete_10_field_return_signature_sha256":
                        right["signature_sha256"],
                    "active_factor_relation": relation,
                    "signed_support_face_disposition": disposition,
                    "signed_support_precision_replays": replays,
                    "strict_desired_side_face_witness": witness,
                    "formal_occurrence_identity_collapse_credit": 0,
                    "formal_component_edge_credit": 0,
                    "formal_DSU_rank_reduction_credit": 0,
                    "formal_maximality_credit": 0,
                }
                rows.append(closed(payload))
    rows.sort(key=lambda row: row["Round299D_R275_region_common_face_row_id"])
    need(len(rows) == 55_932, "complete region face census")
    return rows


def prior_pair_sets() -> dict[str, set[tuple[str, str]]]:
    ordinary = {
        tuple(row["exact_occurrence_endpoint_pair"])
        for row in read_gzip(R297)["rows"]
    }
    seam = {
        tuple(row["unordered_formal_occurrence_endpoint_pair"])
        for row in read_gzip(R296)["rows"]
    }
    lower = {
        tuple(row["target_Round294_registry_occurrence_ids"])
        for row in read_gzip(R295A)["rows"]
        if row["target_Round294_registry_reference_count"] == 2
    }
    a_rows = read_gzip(R299AL)["rows"]
    r299ab = {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in a_rows
        if row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
        and row["coordinate_face_physical_replay_status"].startswith(
            "BOTH_ENDPOINT_CELLS_FULL"
        )
    }
    r299ab |= {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in read_gzip(R299BL)["rows"]
        if row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
        and row["signed_support_face_disposition"].startswith(
            "POSITIVE_AREA_SIGNED_SUPPORT_COMMON_FACE_CERTIFIED"
        )
    }
    r299c = {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in read_gzip(R299CL)["rows"]
        if row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
        and not row["signed_support_face_disposition"].endswith("__EXCLUDED")
    }
    need(
        len(ordinary) == 330_724
        and len(seam) == 15_316
        and len(lower) == 111_524
        and len(r299ab) == 25_452
        and len(r299c) == 4_288,
        "prior pair census",
    )
    return {
        "R297_ORDINARY": ordinary,
        "R296_TRUE_SEAM": seam,
        "R295A_LOWER": lower,
        "R299AB_ACCEPTED": r299ab,
        "R299C_ACCEPTED": r299c,
        "R299ABC_ACCEPTED": r299ab | r299c,
    }


def expand_occurrence_pairs(
    faces: list[dict[str, Any]],
    endpoints: dict[str, set[str]],
    prior: dict[str, set[tuple[str, str]]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    evidence: dict[tuple[str, str], list[str]] = defaultdict(list)
    self_incidence = 0
    accepted_faces = 0
    accepted_kind = Counter()
    excluded_kind = Counter()
    for face in faces:
        relation = face["active_factor_relation"]
        accepted = face["signed_support_face_disposition"].startswith("ACCEPTED")
        if not accepted:
            excluded_kind[relation] += 1
            continue
        accepted_faces += 1
        accepted_kind[relation] += 1
        face_id = face["Round299D_R275_region_common_face_row_id"]
        for left in endpoints[face["left_Round275_region_id"]]:
            for right in endpoints[face["right_Round275_region_id"]]:
                if left == right:
                    self_incidence += 1
                    continue
                evidence[pair(left, right)].append(face_id)

    rows = []
    for occurrence_pair in sorted(evidence):
        face_ids = sorted(set(evidence[occurrence_pair]))
        payload = {
            "Round299D_occurrence_pair_candidate_row_id":
                "round299d-occurrence-pair-candidate:"
                + digest(list(occurrence_pair)),
            "unordered_formal_occurrence_endpoint_pair":
                list(occurrence_pair),
            "accepted_R275_region_face_witness_count": len(face_ids),
            "accepted_R275_region_face_witness_ids": face_ids,
            "accepted_R275_region_face_witness_ids_sha256": digest(face_ids),
            "R297_ordinary_pair_already_present":
                occurrence_pair in prior["R297_ORDINARY"],
            "R296_true_seam_pair_already_present":
                occurrence_pair in prior["R296_TRUE_SEAM"],
            "R295A_lower_pair_already_present":
                occurrence_pair in prior["R295A_LOWER"],
            "R299AB_accepted_pair_already_present":
                occurrence_pair in prior["R299AB_ACCEPTED"],
            "R299C_accepted_pair_already_present":
                occurrence_pair in prior["R299C_ACCEPTED"],
            "R299ABC_accepted_pair_already_present":
                occurrence_pair in prior["R299ABC_ACCEPTED"],
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
        }
        rows.append(closed(payload))
    pairs = set(evidence)
    need(
        accepted_faces == 36_140
        and len(rows) == len(pairs) == 34_628
        and accepted_kind
        == {
            "NO_GRAPH_ENDPOINT": 16_396,
            "ONE_GRAPH_ENDPOINT__OTHER_ENDPOINT_FULL_SIGNED_SUPPORT": 7_160,
            "SAME_ACTIVE_FACTOR__SAME_STRICT_DESIRED_SIDE": 12_584,
        }
        and excluded_kind
        == {
            "SAME_ACTIVE_FACTOR__OPPOSITE_STRICT_DESIRED_SIDES": 12_608,
            "ONE_GRAPH_ENDPOINT__OTHER_ENDPOINT_FULL_SIGNED_SUPPORT": 7_160,
            "SAME_ACTIVE_FACTOR__SAME_STRICT_DESIRED_SIDE": 24,
        },
        "accepted/excluded region face census",
    )
    need(
        len(pairs & prior["R299AB_ACCEPTED"]) == 25_204
        and len(pairs & prior["R299C_ACCEPTED"]) == 2_776
        and len(pairs & prior["R299ABC_ACCEPTED"]) == 26_764
        and len(pairs & prior["R297_ORDINARY"]) == 272
        and not pairs & prior["R296_TRUE_SEAM"]
        and not pairs & prior["R295A_LOWER"],
        "prior channel intersection census",
    )
    prior_union = (
        prior["R297_ORDINARY"]
        | prior["R296_TRUE_SEAM"]
        | prior["R295A_LOWER"]
        | prior["R299ABC_ACCEPTED"]
    )
    need(len(pairs - prior_union) == 7_592, "new R275 frontier pair census")
    return rows, {
        "accepted_region_face_count": accepted_faces,
        "excluded_region_face_count": len(faces) - accepted_faces,
        "accepted_active_factor_relation_histogram":
            dict(sorted(accepted_kind.items())),
        "excluded_active_factor_relation_histogram":
            dict(sorted(excluded_kind.items())),
        "self_occurrence_endpoint_incidence_count": self_incidence,
        "accepted_distinct_occurrence_pair_count": len(pairs),
        "accepted_pair_R299AB_intersection_count":
            len(pairs & prior["R299AB_ACCEPTED"]),
        "accepted_pair_R299C_intersection_count":
            len(pairs & prior["R299C_ACCEPTED"]),
        "accepted_pair_R299ABC_intersection_count":
            len(pairs & prior["R299ABC_ACCEPTED"]),
        "accepted_pair_R297_ordinary_intersection_count":
            len(pairs & prior["R297_ORDINARY"]),
        "accepted_pair_R296_true_seam_intersection_count":
            len(pairs & prior["R296_TRUE_SEAM"]),
        "accepted_pair_R295A_lower_intersection_count":
            len(pairs & prior["R295A_LOWER"]),
        "accepted_pair_new_beyond_all_prior_channels_count":
            len(pairs - prior_union),
    }


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    regions = load_regions()
    dispositions = load_region_dispositions()
    transformed = transformed_region_rows(regions, dispositions)
    endpoints = region_endpoint_map(regions)
    faces = enumerate_region_faces(transformed)
    prior = prior_pair_sets()
    occurrence_rows, frontier_census = expand_occurrence_pairs(
        faces, endpoints, prior
    )

    face_disposition = Counter(
        row["signed_support_face_disposition"] for row in faces
    )
    signature_outcome = Counter(
        (
            "ACCEPTED"
            if row["signed_support_face_disposition"].startswith("ACCEPTED")
            else "EXCLUDED",
            "SAME_SIGNATURE"
            if row["same_complete_10_field_return_signature"]
            else "DIFFERENT_SIGNATURE",
        )
        for row in faces
    )
    need(
        signature_outcome
        == {
            ("ACCEPTED", "SAME_SIGNATURE"): 36_140,
            ("EXCLUDED", "DIFFERENT_SIGNATURE"): 19_768,
            ("EXCLUDED", "SAME_SIGNATURE"): 24,
        },
        "signature/outcome census",
    )
    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": "PASS_ZERO_CREDIT__COMPLETE_R275_REGION_FACE_FRONTIER_ENUMERATED",
        "region_face_row_count": len(faces),
        "region_face_rows": faces,
        "region_face_rows_sha256": digest(faces),
        "occurrence_pair_candidate_row_count": len(occurrence_rows),
        "occurrence_pair_candidate_rows": occurrence_rows,
        "occurrence_pair_candidate_rows_sha256": digest(occurrence_rows),
        "every_row_closed_by_own_SHA256": True,
    }
    result = {
        "schema": SCHEMA,
        "status": "PASS_ZERO_CREDIT__R275_REGION_FRONTIER_GAP_EXPOSED",
        "input_file_pins": PINS,
        "census": {
            "Round275_region_count": len(regions),
            "Round275_region_endpoint_incidence_count":
                sum(len(values) for values in endpoints.values()),
            "Round275_region_endpoint_multiplicity_histogram": dict(
                sorted(Counter(len(values) for values in endpoints.values()).items())
            ),
            "raw_region_common_face_count": len(faces),
            "raw_region_face_disposition_histogram":
                dict(sorted(face_disposition.items())),
            "raw_region_face_signature_outcome_histogram": {
                "|".join(key): value
                for key, value in sorted(signature_outcome.items())
            },
            **frontier_census,
            "signed_point_witness_is_not_final_guided_positive_patch": True,
            "coordinate_region_face_is_not_automatically_component_edge": True,
        },
        "ledger": {
            "filename": LEDGER.name,
            "region_face_row_count": len(faces),
            "region_face_rows_sha256": ledger["region_face_rows_sha256"],
            "occurrence_pair_candidate_row_count": len(occurrence_rows),
            "occurrence_pair_candidate_rows_sha256":
                ledger["occurrence_pair_candidate_rows_sha256"],
        },
        "strict_nonpromotion": {
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "CM2": "NO_GO_COMPLETE_R275_FRONTIER_NOT_FORMALLY_PROMOTED",
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
