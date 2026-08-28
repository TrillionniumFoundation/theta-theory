#!/usr/bin/env python3
"""Independently verify Round258 without importing or executing its producer."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round258_source_g_whole_box_boundary_face_saturation_verification.json"
CANDIDATE = HERE / "cm2_round258_source_g_whole_box_boundary_face_saturation_certificate.json"
CANDIDATE_SHA256 = "11d546a00cf27ae1fe5e146a18a64436676ec73214cd15dd294bb03bfb0359bb"
SCHEMA = "cm2.round258.source-g-whole-box-boundary-face-saturation-verification.v1"
PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_rows.json":
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    "cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json":
        "e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818",
    "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json":
        "4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938",
    "cm2_round254_source_g_seed_block_quotient_closure_certificate.json":
        "b3823b57ba6112c37b63fa1eab85507659038170277634853eb0453f418c47cf",
    "cm2_round255_source_g_block_carrier_quotient_augmentation_certificate.json":
        "d7a2ad5175d1671ca4000e287c0c201826e41e4da718fa5af3c840a80417db0d",
    "cm2_round256_source_g_local_occurrence_carrier_completion_certificate.json":
        "b72ed5f3c4d28a9ea9fea1eda1e7259db08c3a2bdda40d0959aaee6bf0482772",
}


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


def envelope(path: Path, expected: str) -> dict[str, Any]:
    info = path.lstat()
    need(
        stat.S_ISREG(info.st_mode) and not path.is_symlink()
        and 0 < info.st_size <= 500_000_000,
        f"regular:{path.name}",
    )
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected, f"pin:{path.name}")
    document = json.loads(raw)
    need(
        set(document) == {"schema", "result", "result_sha256"}
        and digest(document["result"]) == document["result_sha256"],
        f"envelope:{path.name}",
    )
    return document


def load(name: str) -> dict[str, Any]:
    return envelope(HERE / name, PINS[name])["result"]


def text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def sig(value: dict[str, Any]) -> tuple[Any, ...]:
    return (
        value["source_chart"], value["target_lift"],
        tuple(tuple(event) for event in value["ordered_integer_wall_events"]),
        tuple(value["signed_wall_word"]), value["roof"], value["outgoing_cell"],
        value["target_chart"], tuple(value["official_key_row"]),
        value["official_key_ordinal"], value["official_key_id"],
    )


def check_ledger(value: dict[str, Any], id_field: str) -> None:
    rows = value["rows"]
    need(value["row_count"] == len(rows), f"count:{id_field}")
    need(len({row[id_field] for row in rows}) == len(rows), f"unique:{id_field}")
    need(all(digest({key: item for key, item in row.items() if key != "row_sha256"}) == row["row_sha256"] for row in rows), f"row hashes:{id_field}")
    need(value["rows_sha256"] == digest(rows), f"rows hash:{id_field}")
    need(value["row_ids_sha256"] == digest([row[id_field] for row in rows]), f"ids hash:{id_field}")
    need(value["row_hashes_sha256"] == digest([row["row_sha256"] for row in rows]), f"hashes hash:{id_field}")


class DSU:
    def __init__(self, values: set[str]) -> None:
        self.parent = {value: value for value in values}

    def find(self, value: str) -> str:
        if self.parent[value] != value:
            self.parent[value] = self.find(self.parent[value])
        return self.parent[value]

    def union(self, left: str, right: str) -> bool:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        if left > right:
            left, right = right, left
        self.parent[right] = left
        return True


def metadata() -> dict[str, dict[str, Any]]:
    rows179 = load("cm2_round179_source_g_residual_tube_arrangement_rows.json")
    round204 = load("cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json")
    round208 = load("cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json")
    result: dict[str, dict[str, Any]] = {}
    columns = rows179["row_column_schemas"]["resolved_3d_child_rows"]
    for packed in rows179["resolved_3d_child_rows"]:
        row = dict(zip(columns, packed))
        signature = {
            "source_chart": row["chart"], "target_lift": row["owner_target"],
            "ordered_integer_wall_events": row["ordered_integer_wall_events"],
            "signed_wall_word": row["signed_wall_word"], "roof": row["roof"],
            "outgoing_cell": row["outgoing_cell"], "target_chart": row["target_chart"],
            "official_key_row": row["official_key_row"],
            "official_key_ordinal": row["official_key_ordinal"],
            "official_key_id": row["official_key_id"],
        }
        result[row["row_id"]] = {
            "chart": row["chart"], "box": tuple(Fraction(item) for item in row["box"]),
            "class": "ROUND179_RESOLVED_WHOLE_BOX", "whole": True,
            "signature": signature, "signature_tuple": sig(signature),
        }
    rows204 = round204["formal_local_open_3D_region_ledger"]["rows"]
    count204 = Counter(row["leaf_row_id"] for row in rows204)
    for row in rows204:
        signature = {
            "source_chart": row["chart"], "target_lift": row["owner_target"],
            "ordered_integer_wall_events": row["ordered_integer_wall_events"],
            "signed_wall_word": row["signed_wall_word"], "roof": row["roof"],
            "outgoing_cell": row["outgoing_cell"], "target_chart": row["target_chart"],
            "official_key_row": row["official_key_row"],
            "official_key_ordinal": row["official_key_ordinal"],
            "official_key_id": row["official_key_id"],
        }
        result[row["region_row_id"]] = {
            "chart": row["chart"],
            "box": tuple(Fraction(item) for item in row["leaf_exact_box"]),
            "class": f"ROUND204_{row['graph_classification']}_{row['region_kind']}",
            "whole": row["graph_classification"] == "EMPTY"
            and row["region_kind"] == "NO_TARGET_SHEET_REGION"
            and count204[row["leaf_row_id"]] == 1,
            "signature": signature, "signature_tuple": sig(signature),
        }
    rows208 = round208["formal_local_open_3D_signature_ledger"]["rows"]
    count208 = Counter(row["leaf_row_id"] for row in rows208)
    for row in rows208:
        signature = row["local_return_signature"]
        result[row["region_row_id"]] = {
            "chart": signature["source_chart"],
            "box": tuple(Fraction(item) for item in row["Round182_leaf_box"]),
            "class": f"ROUND208_{row['F_sign']}_{row['leaf_classification']}",
            "whole": row["leaf_classification"] == "EMPTY"
            and count208[row["leaf_row_id"]] == 1,
            "signature": signature, "signature_tuple": sig(signature),
        }
    need(len(result) == 53_968, "metadata")
    return result


def verify(candidate: dict[str, Any]) -> dict[str, int]:
    round254 = load("cm2_round254_source_g_seed_block_quotient_closure_certificate.json")
    round255 = load("cm2_round255_source_g_block_carrier_quotient_augmentation_certificate.json")
    round256 = load("cm2_round256_source_g_local_occurrence_carrier_completion_certificate.json")
    occurrence_meta = metadata()
    frontier = round256["formal_post_Round256_complete_occurrence_quotient_frontier_ledger"]["rows"]
    by_occurrence = {row["local_occurrence_row_id"]: row for row in frontier}
    need(set(by_occurrence) == set(occurrence_meta), "frontier metadata")

    component_keys: dict[str, tuple[str, int]] = {}
    for row in round254["formal_post_Round254_component_commitment_ledger"]["rows"]:
        component_keys[row["post_Round254_mixed_sheet_quotient_component_id"]] = (row["official_key_id"], row["official_key_ordinal"])
    for row in round255["formal_new_known_block_carrier_component_ledger"]["rows"]:
        component_keys[row["post_Round255_quotient_component_id"]] = (row["official_key_id"], row["official_key_ordinal"])
    for row in round256["formal_new_local_occurrence_carrier_ledger"]["rows"]:
        component_keys[row["post_Round256_quotient_component_id"]] = (row["official_key_id"], row["official_key_ordinal"])
    need(len(component_keys) == 74_012, "component universe")

    accepted_ledger = candidate["formal_accepted_whole_box_boundary_face_ledger"]
    rejected_ledger = candidate["formal_rejected_or_deferred_boundary_face_ledger"]
    check_ledger(accepted_ledger, "accepted_face_row_id")
    check_ledger(rejected_ledger, "rejected_face_row_id")
    actual_accepted = {row["accepted_face_row_id"]: row for row in accepted_ledger["rows"]}
    actual_rejected = {row["rejected_face_row_id"]: row for row in rejected_ledger["rows"]}

    groups: dict[tuple[str, str], list[tuple[str, str, dict[str, Any]]]] = defaultdict(list)
    for occurrence_id, source in by_occurrence.items():
        item = occurrence_meta[occurrence_id]
        groups[(source["official_key_id"], item["chart"])].append((
            occurrence_id, source["post_Round256_quotient_component_id"], item
        ))
    expected_ids: set[str] = set()
    accepted_pairs: set[tuple[str, str]] = set()
    counts: Counter[str] = Counter()
    for (key_id, chart), rows in groups.items():
        for axis in range(3):
            lower: dict[Fraction, list[tuple[str, str, dict[str, Any]]]] = defaultdict(list)
            upper: dict[Fraction, list[tuple[str, str, dict[str, Any]]]] = defaultdict(list)
            for row in rows:
                lower[row[2]["box"][2 * axis]].append(row)
                upper[row[2]["box"][2 * axis + 1]].append(row)
            for coordinate in set(lower) & set(upper):
                for left in upper[coordinate]:
                    for right in lower[coordinate]:
                        if left[0] == right[0] or left[1] == right[1]:
                            continue
                        transverse = [candidate_axis for candidate_axis in range(3) if candidate_axis != axis]
                        widths = [
                            min(left[2]["box"][2 * candidate_axis + 1], right[2]["box"][2 * candidate_axis + 1])
                            - max(left[2]["box"][2 * candidate_axis], right[2]["box"][2 * candidate_axis])
                            for candidate_axis in transverse
                        ]
                        if min(widths) <= 0:
                            continue
                        occurrence_ids = sorted([left[0], right[0]])
                        candidate_id = "round258-boundary-face-candidate:" + digest(
                            [key_id, chart, axis, text(coordinate), occurrence_ids]
                        )
                        need(candidate_id not in expected_ids, f"duplicate candidate:{candidate_id}")
                        expected_ids.add(candidate_id)
                        signature_equal = left[2]["signature_tuple"] == right[2]["signature_tuple"]
                        both_whole = left[2]["whole"] and right[2]["whole"]
                        if signature_equal and both_whole:
                            row = actual_accepted[candidate_id]
                            need(
                                row["occurrence_row_ids"] == occurrence_ids
                                and row["source_chart"] == chart
                                and row["face_axis"] == axis
                                and row["face_coordinate"] == text(coordinate)
                                and row["exact_common_face_widths"] == [text(width) for width in widths]
                                and row["exact_common_face_area"] == text(widths[0] * widths[1])
                                and row["complete_ten_field_return_signature"] == left[2]["signature"]
                                and row["physical_glue_credit"] == 1,
                                f"accepted row:{candidate_id}",
                            )
                            pair = tuple(sorted([left[1], right[1]]))
                            accepted_pairs.add(pair)
                            counts["accepted"] += 1
                        else:
                            row = actual_rejected[candidate_id]
                            expected_disposition = (
                                "REJECT_FULL_RETURN_SIGNATURE_MISMATCH" if not signature_equal
                                else "DEFER_CURVED_REGION_FACE_OCCUPANCY_UNPROVED"
                            )
                            need(
                                row["disposition"] == expected_disposition
                                and row["complete_ten_field_return_signature_equal"] == signature_equal
                                and row["both_regions_certified_whole_box"] == both_whole
                                and row["physical_glue_credit"] == 0,
                                f"rejected row:{candidate_id}",
                            )
                            counts[
                                "mismatch" if not signature_equal else "deferred"
                            ] += 1
    need(
        expected_ids == set(actual_accepted) | set(actual_rejected)
        and not (set(actual_accepted) & set(actual_rejected))
        and counts == {"accepted": 904, "mismatch": 12_548, "deferred": 13_836}
        and len(accepted_pairs) == 852,
        "candidate reconciliation",
    )

    dsu = DSU(set(component_keys))
    reductions = sum(int(dsu.union(*pair)) for pair in sorted(accepted_pairs))
    need(reductions == 468, "rank reductions")
    members: dict[str, list[str]] = defaultdict(list)
    for component_id in sorted(component_keys):
        members[dsu.find(component_id)].append(component_id)
    need(len(members) == 73_544, "post components")

    map_ledger = candidate["formal_Round257_to_Round258_component_map_ledger"]
    component_ledger = candidate["formal_post_Round258_component_commitment_ledger"]
    occurrence_ledger = candidate["formal_post_Round258_occurrence_quotient_frontier_ledger"]
    key_ledger = candidate["formal_post_Round258_key_quotient_frontier_ledger"]
    check_ledger(map_ledger, "Round257_to_Round258_component_map_row_id")
    check_ledger(component_ledger, "post_Round258_component_row_id")
    check_ledger(occurrence_ledger, "post_frontier_row_id")
    check_ledger(key_ledger, "post_Round258_key_frontier_row_id")
    actual_map = {
        row["Round257_quotient_component_id"]: row["post_Round258_quotient_component_id"]
        for row in map_ledger["rows"]
    }
    need(set(actual_map) == set(component_keys), "map universe")
    for values in members.values():
        expected_post = values[0] if len(values) == 1 else "round258-whole-box-face-component:" + digest(values)
        need(all(actual_map[value] == expected_post for value in values), "map reconstruction")
    actual_components = {
        row["post_Round258_quotient_component_id"]: row
        for row in component_ledger["rows"]
    }
    need(len(actual_components) == len(members), "component rows")
    for values in members.values():
        expected_post = actual_map[values[0]]
        row = actual_components[expected_post]
        need(
            row["constituent_Round257_component_ids"] == values
            and row["constituent_Round257_component_count"] == len(values)
            and len({component_keys[value] for value in values}) == 1,
            f"component commitment:{expected_post}",
        )
    actual_occurrence = {row["local_occurrence_row_id"]: row for row in occurrence_ledger["rows"]}
    need(set(actual_occurrence) == set(by_occurrence), "occurrence frontier")
    for occurrence_id, source in by_occurrence.items():
        need(
            actual_occurrence[occurrence_id]["post_Round258_quotient_component_id"]
            == actual_map[source["post_Round256_quotient_component_id"]],
            f"occurrence map:{occurrence_id}",
        )
    need(len(key_ledger["rows"]) == 116, "key frontier")
    component_count_by_key = Counter(row["official_key_id"] for row in component_ledger["rows"])
    for row in key_ledger["rows"]:
        need(
            row["post_Round258_quotient_component_count"] == component_count_by_key[row["official_key_id"]]
            and row["occurrence_quotient_assignment_complete"] is True
            and row["all_quotient_components_proved_maximal"] is False,
            f"key row:{row['official_key_id']}",
        )
    return {
        "candidate_count": len(expected_ids),
        "accepted_count": counts["accepted"],
        "mismatch_count": counts["mismatch"],
        "deferred_count": counts["deferred"],
        "rank_reductions": reductions,
        "post_components": len(members),
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
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    candidate_document = envelope(CANDIDATE, CANDIDATE_SHA256)
    need(
        candidate_document["schema"]
        == "cm2.round258.source-g-whole-box-boundary-face-saturation.v1",
        "candidate schema",
    )
    verified = verify(candidate_document["result"])
    result = {
        "status": "PASS_INDEPENDENT_ROUND258",
        "producer_imported_or_executed": False,
        "candidate_result_sha256": candidate_document["result_sha256"],
        "verified_boundary_face_candidate_count": verified["candidate_count"],
        "verified_accepted_whole_box_face_count": verified["accepted_count"],
        "verified_signature_mismatch_face_count": verified["mismatch_count"],
        "verified_curved_region_deferred_face_count": verified["deferred_count"],
        "verified_rank_reduction_count": verified["rank_reductions"],
        "verified_post_component_count": verified["post_components"],
        "verified_maximal_component_assignment_count": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    document = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    raw = canonical(document) + b"\n"
    if not arguments.no_write:
        safe_write(raw)
    print(result["status"])
    print(json.dumps(result, sort_keys=True))
    print(f"result_sha256={document['result_sha256']}")
    print(f"verification_sha256={hashlib.sha256(raw).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
