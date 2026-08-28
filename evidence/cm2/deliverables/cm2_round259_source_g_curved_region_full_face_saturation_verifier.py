#!/usr/bin/env python3
"""Independent verifier for Round259 curved-region full-face saturation."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_CANDIDATE = HERE / "cm2_round259_source_g_curved_region_full_face_saturation_certificate.json"
OUTPUT = HERE / "cm2_round259_source_g_curved_region_full_face_saturation_verification.json"
SCHEMA = "cm2.round259.source-g-curved-region-full-face-saturation.verification.v1"
CANDIDATE_SCHEMA = "cm2.round259.source-g-curved-region-full-face-saturation.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round204_source_g_wall_return_signature_local_replacement_verifier.py":
        "6bcfbb794005e5a92590b7bb60ffceda34db3441ced143a15ceb23e15d5c035e",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_verifier.py":
        "718c731004fe2125511a9a52c84f45c77eab842d4c042942e91cc5881b64ee36",
    "cm2_round258_source_g_whole_box_boundary_face_saturation_certificate.json":
        "11d546a00cf27ae1fe5e146a18a64436676ec73214cd15dd294bb03bfb0359bb",
    "cm2_round259_source_g_curved_region_full_face_saturation.py":
        "4a465317d05ef3f1497876b052131cbbd889d67fbcc88e28362248935cfc5310",
}
EXPECTED_CANDIDATE_SHA256 = "799dc36d6a5a9da351c0d006939feb6fc69eaad7ac30aa42b781f925c637d039"


def need(value: bool, label: str) -> None:
    if not value:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def pinned(name: str) -> bytes:
    path = HERE / name
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode) and not path.is_symlink()
        and 0 < info.st_size <= 500_000_000,
        f"regular:{name}",
    )
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINS[name], f"pin:{name}")
    return raw


def load_result(name: str) -> dict[str, Any]:
    document = json.loads(pinned(name))
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        f"envelope:{name}",
    )
    return document["result"]


def check_ledger(value: dict[str, Any], id_field: str) -> None:
    rows = value["rows"]
    need(
        value["row_count"] == len(rows)
        and len(rows) == len({row[id_field] for row in rows})
        and value["rows_sha256"] == digest(rows)
        and value["row_ids_sha256"] == digest([row[id_field] for row in rows])
        and value["row_hashes_sha256"] == digest([row["row_sha256"] for row in rows])
        and value["every_row_closed_by_own_SHA256"] is True,
        f"ledger:{id_field}",
    )
    for row in rows:
        body = dict(row)
        actual = body.pop("row_sha256")
        need(actual == digest(body), f"row:{id_field}:{row[id_field]}")


class DSU:
    def __init__(self, values: list[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find(parent)
        return self.parent[value]

    def union(self, left: str, right: str) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        if left_root > right_root:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        return True


def boxes(round204: dict[str, Any], round208: dict[str, Any]) -> dict[str, tuple[Fraction, ...]]:
    rows179 = load_result("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    columns = rows179["row_column_schemas"]["resolved_3d_child_rows"]
    result: dict[str, tuple[Fraction, ...]] = {}
    for packed in rows179["resolved_3d_child_rows"]:
        row = dict(zip(columns, packed))
        result[row["row_id"]] = tuple(Fraction(value) for value in row["box"])
    for row in round204["formal_local_open_3D_region_ledger"]["rows"]:
        result[row["region_row_id"]] = tuple(Fraction(value) for value in row["leaf_exact_box"])
    for row in round208["formal_local_open_3D_signature_ledger"]["rows"]:
        result[row["region_row_id"]] = tuple(Fraction(value) for value in row["Round182_leaf_box"])
    need(len(result) == 53_968, "box census")
    return result


def face_values(row: dict[str, Any], all_boxes: dict[str, tuple[Fraction, ...]]) -> list[Fraction]:
    left, right = (all_boxes[value] for value in row["occurrence_row_ids"])
    axis = row["face_axis"]
    coordinate = Fraction(row["face_coordinate"])
    result: list[Fraction] = []
    for candidate in range(3):
        result.extend(
            (coordinate, coordinate) if candidate == axis else (
                max(left[2 * candidate], right[2 * candidate]),
                min(left[2 * candidate + 1], right[2 * candidate + 1]),
            )
        )
    return result


def corridor(
    occurrence_id: str, face: list[Fraction], axis: int, coordinate: Fraction,
    depth: int, all_boxes: dict[str, tuple[Fraction, ...]],
) -> tuple[list[Fraction], Fraction]:
    source = all_boxes[occurrence_id]
    result = list(face)
    exact_depth = (source[2 * axis + 1] - source[2 * axis]) / (2 ** depth)
    if source[2 * axis + 1] == coordinate:
        result[2 * axis:2 * axis + 2] = [coordinate - exact_depth, coordinate]
    elif source[2 * axis] == coordinate:
        result[2 * axis:2 * axis + 2] = [coordinate, coordinate + exact_depth]
    else:
        raise RuntimeError(f"incidence:{occurrence_id}")
    return result, exact_depth


def verify(candidate: dict[str, Any]) -> dict[str, Any]:
    for value, id_field in (
        (candidate["formal_accepted_curved_region_full_face_ledger"], "accepted_curved_face_row_id"),
        (candidate["formal_deferred_common_face_refinement_ledger"], "Round259_deferred_face_row_id"),
        (candidate["formal_Round258_to_Round259_component_map_ledger"], "Round258_to_Round259_component_map_row_id"),
        (candidate["formal_post_Round259_component_commitment_ledger"], "post_Round259_component_row_id"),
        (candidate["formal_post_Round259_occurrence_quotient_frontier_ledger"], "post_frontier_row_id"),
        (candidate["formal_post_Round259_key_quotient_frontier_ledger"], "post_Round259_key_frontier_row_id"),
    ):
        check_ledger(value, id_field)

    round204 = load_result(
        "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json"
    )
    round208 = load_result(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json"
    )
    round258 = load_result(
        "cm2_round258_source_g_whole_box_boundary_face_saturation_certificate.json"
    )
    pinned("cm2_round204_source_g_wall_return_signature_local_replacement_verifier.py")
    pinned("cm2_round208_source_g_outgoing_direct_signature_materialization_verifier.py")
    pinned("cm2_round259_source_g_curved_region_full_face_saturation.py")
    need(
        "cm2_round259_source_g_curved_region_full_face_saturation" not in sys.modules,
        "producer not imported",
    )
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    verifier208 = importlib.import_module(
        "cm2_round208_source_g_outgoing_direct_signature_materialization_verifier"
    )
    verifier204 = importlib.import_module(
        "cm2_round204_source_g_wall_return_signature_local_replacement_verifier"
    )
    _r195, round198, round174_208, _registry, _outgoing, collars208, _chain = (
        verifier208.load_evaluator()
    )
    formal204 = verifier204.load_formal_inputs()
    round179_204 = formal204["evaluator"].r179
    round174_204 = round179_204.r174
    scope182 = verifier204.extract_round182_scope(formal204["attachment182"])
    scope179 = verifier204.extract_round179_scope(
        formal204["source179"], scope182["occurrence_ids"], scope182["origin_ids"]
    )
    regions204 = {
        row["region_row_id"]: row
        for row in round204["formal_local_open_3D_region_ledger"]["rows"]
    }
    regions208 = {
        row["region_row_id"]: row
        for row in round208["formal_local_open_3D_signature_ledger"]["rows"]
    }
    all_boxes = boxes(round204, round208)

    def eval204(region: dict[str, Any], values: list[Fraction], label: str) -> bool:
        collar = scope182["collars"][region["occurrence_row_id"]]
        wall = scope179["walls"][region["occurrence_row_id"]]
        box = round174_204.atlas.AtlasBox(*values, 0, label)
        geometry = round179_204.independent_geometry(
            collar["chart"], collar["owner_target"], box
        )
        source_name = verifier204.CHART_CONTRACT[collar["chart"]][2]
        target_name = "hit_x" if wall["axis"] == "X" else "hit_y"
        source_sign = round179_204.arb_sign(
            round179_204.subtract_wall(geometry[source_name], 0)[0]
        )
        target_sign = round179_204.arb_sign(round179_204.subtract_wall(
            geometry[target_name], wall["integer_wall"]
        )[0])
        return (
            source_sign == "STRICT_" + region["source_sign"]
            and target_sign == "STRICT_" + region["target_factor_sign"]
        )

    accepted_actual = {
        row["Round258_boundary_face_candidate_id"]: row
        for row in candidate["formal_accepted_curved_region_full_face_ledger"]["rows"]
    }
    deferred_actual = {
        row["Round258_boundary_face_candidate_id"]: row
        for row in candidate["formal_deferred_common_face_refinement_ledger"]["rows"]
    }
    source_rows = [
        row for row in round258["formal_rejected_or_deferred_boundary_face_ledger"]["rows"]
        if row["disposition"] == "DEFER_CURVED_REGION_FACE_OCCUPANCY_UNPROVED"
    ]
    map258 = {
        row["Round257_quotient_component_id"]: row["post_Round258_quotient_component_id"]
        for row in round258["formal_Round257_to_Round258_component_map_ledger"]["rows"]
    }
    expected_accepted: set[str] = set()
    expected_deferred: dict[str, str] = {}
    accepted_pairs: set[tuple[str, str]] = set()
    counts: Counter[str] = Counter()
    depths: Counter[int] = Counter()
    area_sum = Fraction(0)
    volume_sum = Fraction(0)
    for index, source in enumerate(source_rows, 1):
        occurrence_ids = source["occurrence_row_ids"]
        axis = source["face_axis"]
        coordinate = Fraction(source["face_coordinate"])
        face = face_values(source, all_boxes)
        kinds = [
            "208" if value in regions208 else "204" if value in regions204 else "179"
            for value in occurrence_ids
        ]
        face_pass = False
        if kinds.count("208") == 1:
            curved_id = occurrence_ids[kinds.index("208")]
            region = regions208[curved_id]
            proof = round198.compatible_strict_cell_patch(
                collars208[region["occurrence_row_id"]],
                {
                    "axis": ("t", "p", "s")[axis],
                    "candidate_side": "UPPER", "anchor_side": "LOWER",
                    "box": [str(value) for value in face],
                },
                region["HPLUS_sign"], region["HMINUS_sign"],
                f"verify-round259-face:{index}:{curved_id}",
            )
            face_pass = proof["compatible_nonempty_relative_open_cell_patch"]
            channel = "r208"
        elif all(kind == "204" for kind in kinds):
            face_pass = all(
                eval204(regions204[value], face, f"verify-face:{index}:{value}")
                for value in occurrence_ids
            )
            channel = "r204"
        else:
            channel = "r208-refine"
        corridor_pass = face_pass
        local_depths: list[tuple[int, Fraction]] = []
        if face_pass:
            for occurrence_id, kind in zip(occurrence_ids, kinds):
                found = None
                for depth in range(1, 9):
                    values, exact_depth = corridor(
                        occurrence_id, face, axis, coordinate, depth, all_boxes
                    )
                    if kind == "208":
                        region = regions208[occurrence_id]
                        profiles = round198.selected_factor_profiles(
                            collars208[region["occurrence_row_id"]],
                            round174_208.atlas.AtlasBox(
                                *values, 0, f"verify-corridor:{index}:{occurrence_id}:{depth}"
                            ),
                        )
                        matched = (
                            profiles["HPLUS"]["selected_sign"] == region["HPLUS_sign"]
                            and profiles["HMINUS"]["selected_sign"] == region["HMINUS_sign"]
                        )
                    elif kind == "204":
                        matched = eval204(
                            regions204[occurrence_id], values,
                            f"verify-corridor:{index}:{occurrence_id}:{depth}",
                        )
                    else:
                        matched = True
                    if matched:
                        found = (depth, exact_depth)
                        break
                if found is None:
                    corridor_pass = False
                    break
                local_depths.append(found)
        source_id = source["rejected_face_row_id"]
        if face_pass and corridor_pass:
            expected_accepted.add(source_id)
            counts[f"accepted-{channel}"] += 1
            counts[f"axis-{axis}"] += 1
            current_pair = tuple(sorted(
                map258[value] for value in source["pre_Round258_component_ids"]
            ))
            if current_pair[0] != current_pair[1]:
                accepted_pairs.add(current_pair)
            face_area = Fraction(source["exact_common_face_area"])
            area_sum += face_area
            for depth, exact_depth in local_depths:
                depths[depth] += 1
                volume_sum += face_area * exact_depth
        else:
            expected_deferred[source_id] = (
                "DEFER_R204_COMMON_FACE_REFINEMENT_REQUIRED"
                if channel == "r204" else "DEFER_R208_COMMON_FACE_REFINEMENT_REQUIRED"
            )

    need(
        set(accepted_actual) == expected_accepted
        and set(deferred_actual) == set(expected_deferred)
        and all(
            deferred_actual[source_id]["disposition"] == disposition
            for source_id, disposition in expected_deferred.items()
        ),
        "independent accepted/deferred partition",
    )
    need(
        len(expected_accepted) == 1_988
        and counts == Counter({
            "accepted-r208": 1_764, "axis-1": 1_068, "axis-0": 904,
            "accepted-r204": 224, "axis-2": 16,
        })
        and depths == Counter({1: 3_548, 2: 424, 3: 4})
        and area_sum == Fraction(2_374_447, 3_276_800_000)
        and volume_sum == Fraction(19_879_047, 1_677_721_600_000)
        and len(accepted_pairs) == 1_504,
        "independent geometric census",
    )

    source_components = round258["formal_post_Round258_component_commitment_ledger"]["rows"]
    component_keys = {
        row["post_Round258_quotient_component_id"]: (
            row["official_key_id"], row["official_key_ordinal"]
        ) for row in source_components
    }
    dsu = DSU(sorted(component_keys))
    rank = 0
    for left, right in sorted(accepted_pairs):
        need(component_keys[left] == component_keys[right], "independent key purity")
        rank += int(dsu.union(left, right))
    members: dict[str, list[str]] = defaultdict(list)
    for component_id in sorted(component_keys):
        members[dsu.find(component_id)].append(component_id)
    need(rank == 1_480 and len(members) == 72_064, "independent DSU census")
    expected_post: dict[str, str] = {}
    expected_members: dict[str, list[str]] = {}
    for values in members.values():
        post_id = values[0] if len(values) == 1 else (
            "round259-curved-full-face-component:" + digest(values)
        )
        expected_members[post_id] = values
        for value in values:
            expected_post[value] = post_id

    map_rows = candidate["formal_Round258_to_Round259_component_map_ledger"]["rows"]
    actual_map = {
        row["Round258_quotient_component_id"]: row["post_Round259_quotient_component_id"]
        for row in map_rows
    }
    need(actual_map == expected_post, "independent component map")
    component_rows = candidate["formal_post_Round259_component_commitment_ledger"]["rows"]
    actual_members = {
        row["post_Round259_quotient_component_id"]: row["constituent_Round258_component_ids"]
        for row in component_rows
    }
    need(actual_members == expected_members, "independent component commitments")
    for row in candidate["formal_post_Round259_occurrence_quotient_frontier_ledger"]["rows"]:
        need(
            row["post_Round259_quotient_component_id"]
            == expected_post[row["post_Round258_quotient_component_id"]],
            f"frontier map:{row['local_occurrence_row_id']}",
        )
    component_count_by_key = Counter(row["official_key_id"] for row in component_rows)
    for row in candidate["formal_post_Round259_key_quotient_frontier_ledger"]["rows"]:
        need(
            row["post_Round259_quotient_component_count"]
            == component_count_by_key[row["official_key_id"]]
            and row["all_quotient_components_proved_maximal"] is False
            and row["global_exact_key_fibre_exhausted"] is False,
            f"key frontier:{row['official_key_id']}",
        )

    need(candidate["census"] == {
        "Round258_curved_region_deferred_face_count": 13_836,
        "accepted_curved_full_face_count": 1_988,
        "accepted_Round208_factor_region_vs_whole_box_face_count": 1_764,
        "accepted_Round204_target_graph_face_count": 224,
        "accepted_curved_full_face_count_by_axis": {"x": 904, "y": 1_068, "z": 16},
        "remaining_common_face_refinement_count": 11_848,
        "remaining_Round208_common_face_refinement_count": 10_784,
        "remaining_Round204_common_face_refinement_count": 1_064,
        "strict_corridor_dyadic_normal_depth_histogram": {"1": 3_548, "2": 424, "3": 4},
        "accepted_distinct_current_component_pair_count": 1_504,
        "rank_reducing_component_pair_count": 1_480,
        "redundant_certified_component_pair_count": 24,
        "post_Round258_unified_quotient_component_count": 73_544,
        "post_Round259_unified_quotient_component_count": 72_064,
        "exact_accepted_face_area_sum": "2374447/3276800000",
        "exact_two_sided_corridor_volume_sum": "19879047/1677721600000",
        "accepted_Round258_candidate_ids_sha256":
            "974458059739191f495b73d8a88bca32797c6c9d79a21e85cce3b4f1d41dccdc",
        "occurrence_quotient_assignment_count": 53_968,
        "observed_exact_key_count": 116,
        "maximal_physical_component_assignment_count": 0,
        "globally_exhausted_exact_key_fibre_count": 0,
        "global_exact_key_disposition_count": 0,
    }, "candidate census")
    need(
        candidate["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM"
        and candidate["strict_nonpromotion"]["Gate5_filled_field_slot_count"] == 10,
        "strict nonpromotion",
    )
    return {
        "status": "PASS_INDEPENDENT_ROUND259",
        "independent_geometry_recomputed": True,
        "producer_imported_or_executed": False,
        "accepted_face_count": 1_988,
        "remaining_fail_closed_face_count": 11_848,
        "rank_reduction_count": 1_480,
        "post_component_count": 72_064,
        "occurrence_frontier_count": 53_968,
        "exact_key_frontier_count": 116,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def safe_write(raw: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", dir=OUTPUT.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUTPUT)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", nargs="?", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    raw = arguments.candidate.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == EXPECTED_CANDIDATE_SHA256, "candidate SHA256")
    document = json.loads(raw)
    need(
        document["schema"] == CANDIDATE_SCHEMA
        and digest(document["result"]) == document["result_sha256"],
        "candidate envelope",
    )
    result = verify(document["result"])
    verification = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    verification_raw = canonical(verification) + b"\n"
    if not arguments.no_write:
        safe_write(verification_raw)
    print(result["status"])
    print(json.dumps(result, sort_keys=True))
    print(f"result_sha256={verification['result_sha256']}")
    print(f"verification_sha256={hashlib.sha256(verification_raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
