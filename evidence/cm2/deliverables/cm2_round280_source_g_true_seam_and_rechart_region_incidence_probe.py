#!/usr/bin/env python3
"""Round280 exact zero-credit seam/rechart incidence audit.

This probe answers two deliberately separate questions.

1. Which of the 13,788 frozen Round275 reverse-rechart regions have an exact
   positive-volume overlap or a complete positive-area common face with a
   Round279 canonical collar atom carrying the *same complete signature*?
2. Which Round275 guard channels project over each of the 152 Round268 seam
   patches, and what DSU rank change would follow *conditionally* if a missing
   seam-normal corridor were later certified?

The second question is intentionally fail-closed.  Every Round275 region is
strictly inside an adjacent chart and hence has a positive exact gap from the
irrational source-chart seam.  Positive p/s overlap is not promoted to seam
incidence.  Conditional rank arithmetic is emitted only to size the next
gate.  No occurrence, component, maximality, fibre, disposition, or Jx/Jy
credit is awarded.
"""
from __future__ import annotations

import collections
import gzip
import hashlib
import json
import os
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe"

R174 = HERE / "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
R179 = HERE / "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R182 = HERE / "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
R268 = HERE / "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json"
R268V = HERE / "cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_verification.json"
R275 = HERE / "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
R275V = HERE / "cm2_round275_source_g_complete_reverse_rechart_materialization_verification.json"
R279A = HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
R279V = HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_verification.json"
R280 = HERE / "cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe_result.json"
R280C = HERE / "cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe_atom_graph_classes.json.gz"
R280P = HERE / "cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe_provisional_components.json.gz"

PINS = {
    R174.name: "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54",
    R179.name: "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R182.name: "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    R268.name: "10d5e42f4353e981e7e8d5aacc002bed119453ee14a13398c524d5cb4ac2f7b9",
    R268V.name: "a1b43f9f81555a1f48d0593c941c6c5741b99b473649834635ee0ccabc8a53b6",
    R275.name: "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R275V.name: "130d61804d1251ac84e14546034331d8a071d13910b28f7f46b46f5ebe4c3f65",
    R279A.name: "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    R279V.name: "a4cd7a96a43a9011e223d230c9f604f567fa56f1b095403cf802261daab5de21",
    R280.name: "93b0fc0ce798284120adb78e08f9c78ad33c67607dd40870483a5a1031388541",
    R280C.name: "a7333eb0f025c5e42a5e84fe4bf795a11ca1517cf34d34d0415e941fbaef4402",
    R280P.name: "08127f4f528f76f41577cc5a8c510fab34ed0eb284dd58a924e3614f6ef56d4d",
}

RESULT = HERE / f"{PREFIX}_result.json"
REGION_LEDGER = HERE / f"{PREFIX}_region_bindings.json.gz"
PATCH_LEDGER = HERE / f"{PREFIX}_patch_channels.json.gz"


class ProbeError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise ProbeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qtext(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def boxq(values: list[str]) -> tuple[Q, ...]:
    result = tuple(Q(value) for value in values)
    need(len(result) == 6, "six box coordinates")
    need(all(result[2 * i] < result[2 * i + 1] for i in range(3)), "positive widths")
    return result


def closed(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    need("row_sha256" not in result, "row not already closed")
    result["row_sha256"] = digest(result)
    return result


def ledger(rows: list[dict[str, Any]], row_id: str, **extra: Any) -> dict[str, Any]:
    rows.sort(key=lambda row: row[row_id])
    ids = [row[row_id] for row in rows]
    need(len(ids) == len(set(ids)), f"unique ledger ids:{row_id}")
    return {
        **extra,
        "row_count": len(rows),
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows": rows,
    }


def atomic_write(path: Path, payload: bytes) -> None:
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def gzip_write(path: Path, payload: dict[str, Any]) -> None:
    atomic_write(path, gzip.compress(canonical(payload) + b"\n", compresslevel=9, mtime=0))


def pinned_json(path: Path) -> dict[str, Any]:
    need(file_sha256(path) == PINS[path.name], f"input pin:{path.name}")
    return json.loads(path.read_bytes())


def pinned_gzip_json(path: Path) -> dict[str, Any]:
    need(file_sha256(path) == PINS[path.name], f"input pin:{path.name}")
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def packed_result(path: Path) -> dict[str, Any]:
    document = pinned_json(path)
    need(set(document) >= {"result", "result_sha256"}, f"result envelope:{path.name}")
    need(document["result_sha256"] == digest(document["result"]), f"result digest:{path.name}")
    return document["result"]


def unpack(result: dict[str, Any], table: str) -> list[dict[str, Any]]:
    rows = result[table]
    columns = result["row_column_schemas"][table]
    expected = result["table_census_and_sha256"][table]
    need(len(rows) == expected["row_count"], f"packed count:{table}")
    need(digest(rows) == expected["rows_sha256"], f"packed digest:{table}")
    return [dict(zip(columns, row, strict=True)) for row in rows]


def positive_overlap(a0: Q, a1: Q, b0: Q, b1: Q) -> bool:
    return max(a0, b0) < min(a1, b1)


def floorq(value: Q) -> int:
    return value.numerator // value.denominator


def bins(lo: Q, hi: Q, scale: int) -> range:
    # Inclusive endpoint bins form a safe superset; exact tests reject mere
    # endpoint contact later.
    return range(floorq(lo * scale), floorq(hi * scale) + 1)


def square_range(lo: Q, hi: Q) -> tuple[Q, Q]:
    need(lo * hi > 0, "strict signed t interval")
    return (lo * lo, hi * hi) if lo > 0 else (hi * hi, lo * lo)


def actual_t_positive(lo: Q, hi: Q, image_square: tuple[Q, Q]) -> bool:
    if not (lo < hi and lo * hi > 0):
        return False
    square = square_range(lo, hi)
    return max(square[0], image_square[0]) < min(square[1], image_square[1])


def exact_relation(
    region: tuple[Q, ...],
    atom: tuple[Q, ...],
    image_square: tuple[Q, Q],
) -> str | None:
    overlaps = [
        (max(region[2 * axis], atom[2 * axis]), min(region[2 * axis + 1], atom[2 * axis + 1]))
        for axis in range(3)
    ]
    if all(lo < hi for lo, hi in overlaps) and actual_t_positive(
        overlaps[0][0], overlaps[0][1], image_square
    ):
        return "EXACT_POSITIVE_PHYSICAL_VOLUME_OVERLAP"
    for axis, name in enumerate(("T", "P", "S")):
        face = None
        if region[2 * axis + 1] == atom[2 * axis]:
            face = region[2 * axis + 1]
        elif atom[2 * axis + 1] == region[2 * axis]:
            face = atom[2 * axis + 1]
        if face is None:
            continue
        other = [index for index in range(3) if index != axis]
        if not all(
            positive_overlap(
                region[2 * index],
                region[2 * index + 1],
                atom[2 * index],
                atom[2 * index + 1],
            )
            for index in other
        ):
            continue
        if axis == 0:
            if image_square[0] < face * face < image_square[1]:
                return f"EXACT_POSITIVE_AREA_COMMON_{name}_FACE"
        else:
            lo, hi = max(region[0], atom[0]), min(region[1], atom[1])
            if actual_t_positive(lo, hi, image_square):
                return f"EXACT_POSITIVE_AREA_COMMON_{name}_FACE"
    return None


def adjacent_chart(chart: str, root: str) -> str:
    destination = {
        ("E", True): "N",
        ("E", False): "S",
        ("N", True): "E",
        ("N", False): "W",
        ("W", True): "N",
        ("W", False): "S",
        ("S", True): "E",
        ("S", False): "W",
    }[(chart.split(":", 1)[1], root == "+")]
    return f"G:{destination}"


class DSU:
    def __init__(self, values: list[str]):
        self.parent = {value: value for value in values}
        self.size = {value: 1 for value in values}

    def find(self, value: str) -> str:
        need(value in self.parent, f"DSU value:{value}")
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: str, right: str) -> bool:
        left, right = self.find(left), self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right] or (
            self.size[left] == self.size[right] and left > right
        ):
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True


def main() -> int:
    producer_sha256 = file_sha256(Path(__file__))
    r174 = packed_result(R174)
    r179 = packed_result(R179)
    r182 = packed_result(R182)
    r268_document = pinned_json(R268)
    need(r268_document["result_sha256"] == digest(r268_document["result"]), "Round268 digest")
    r268 = r268_document["result"]
    r268v = pinned_json(R268V)
    need(r268v["status"] == "PASS_INDEPENDENT_ROUND268", "Round268 verification")
    r275_document = pinned_json(R275)
    need(r275_document["result_sha256"] == digest(r275_document["result"]), "Round275 digest")
    r275 = r275_document["result"]
    r275v = pinned_json(R275V)
    need(r275v["status"] == "PASS_INDEPENDENT_ROUND275", "Round275 verification")
    r279v = pinned_json(R279V)
    need(r279v["status"] == "PASS_INDEPENDENT_ROUND279", "Round279 verification")
    r280_document = pinned_json(R280)
    need(r280_document["result_sha256"] == digest(r280_document["result"]), "Round280 digest")
    r280 = r280_document["result"]
    need(
        r280["status"] == "PASS_ROUND280_ZERO_CREDIT_SCHEMA_AND_DSU_PREVIEW"
        and r280["round279_readiness"]["round279_fully_frozen"],
        "Round280 zero-credit readiness",
    )

    guard_rows = unpack(r174, "chart_guard_rejection_rows") + unpack(
        r179, "chart_guard_child_rows"
    )
    need(len(guard_rows) == 880, "complete guard universe")
    guards = {row["row_id"]: row for row in guard_rows}
    guard_boxes = {row["row_id"]: boxq(row["box"]) for row in guard_rows}
    guards_by_parent_chart: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for row in guard_rows:
        guards_by_parent_chart[(row["parent_id"], row["chart"])].append(row)

    seam_rows = unpack(r182, "source_chart_seam_owner_rows")
    seams = {row["row_id"]: row for row in seam_rows}
    need(len(seams) == 472, "complete seam owner universe")
    patches = r268["formal_true_source_seam_positive_patch_ledger"]["rows"]
    need(len(patches) == 152, "complete true seam patch universe")

    region_rows = r275["strict_region_ledger"]["rows"] + r275["arrangement_region_ledger"]["rows"]
    need(len(region_rows) == 13_788, "complete reverse-rechart region universe")
    regions: dict[str, dict[str, Any]] = {}
    regions_by_guard: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    region_boxes: dict[str, tuple[Q, ...]] = {}
    for row in region_rows:
        row_id = row["reverse_rechart_region_row_id"]
        need(row_id not in regions, "unique Round275 region id")
        need(row["source_guard_row_id"] in guards, "Round275 guard endpoint")
        need(
            row["exact_coordinate_identity"] == "image_t^2=1-source_t^2; p'=p; s'=s",
            "Round275 coordinate identity",
        )
        need(
            row["occurrence_credit"] == row["component_credit"] == row["maximality_credit"] == 0,
            "Round275 strict nonpromotion",
        )
        box = boxq(row["adjacent_rational_region_box"])
        guard = guard_boxes[row["source_guard_row_id"]]
        image_square = (
            1 - max(guard[0] * guard[0], guard[1] * guard[1]),
            1 - min(guard[0] * guard[0], guard[1] * guard[1]),
        )
        need(actual_t_positive(box[0], box[1], image_square), "nonempty exact Round275 image")
        regions[row_id] = row
        regions_by_guard[row["source_guard_row_id"]].append(row)
        region_boxes[row_id] = box

    atoms_payload = pinned_gzip_json(R279A)
    atoms = atoms_payload["rows"]
    need(atoms_payload["row_count"] == len(atoms) == 332_016, "Round279 atom count")
    seam_origin_ids = {row["origin_row_id"] for row in seam_rows}
    direct_source_seam_origin_atom_count = sum(
        atom["origin_row_id"] in seam_origin_ids for atom in atoms
    )
    need(
        direct_source_seam_origin_atom_count == 0,
        "Round268 seam origins remain disjoint from Round279 collar atoms",
    )
    classes_payload = pinned_gzip_json(R280C)
    class_rows = classes_payload["rows"]
    need(classes_payload["row_count"] == len(class_rows) == 92_120, "Round280 class count")
    need(
        r280["attachments"]["atom_graph_class_ledger"]["file_sha256"] == PINS[R280C.name],
        "Round280 class attachment pin",
    )
    components_payload = pinned_gzip_json(R280P)
    component_rows = components_payload["rows"]
    need(
        components_payload["row_count"] == len(component_rows) == 136_740,
        "Round280 provisional component count",
    )
    need(
        r280["attachments"]["provisional_component_ledger"]["file_sha256"]
        == PINS[R280P.name],
        "Round280 provisional component attachment pin",
    )
    atom_to_class: dict[str, dict[str, Any]] = {}
    class_by_id: dict[str, dict[str, Any]] = {}
    for row in class_rows:
        class_by_id[row["atom_graph_class_id"]] = row
        for atom_id in row["canonical_atom_ids"]:
            need(atom_id not in atom_to_class, "one Round280 class per atom")
            atom_to_class[atom_id] = row
    need(len(atom_to_class) == 332_016, "Round280 complete atom-class mapping")

    atom_by_id = {row["canonical_atom_id"]: row for row in atoms}
    need(len(atom_by_id) == 332_016, "unique atom ids")
    atom_index: dict[tuple[str, str, int, int], list[tuple[str, int, tuple[Q, ...]]]] = (
        collections.defaultdict(list)
    )
    for atom in atoms:
        for box_index, values in enumerate(atom["frozen_true_support_boxes"]):
            box = boxq(values)
            record = (atom["canonical_atom_id"], box_index, box)
            for t_bin in bins(box[0], box[1], 256):
                for p_bin in bins(box[2], box[3], 64):
                    atom_index[
                        (
                            atom["source_chart"],
                            atom["complete_10_field_return_signature_sha256"],
                            t_bin,
                            p_bin,
                        )
                    ].append(record)

    relation_histogram: collections.Counter[str] = collections.Counter()
    class_count_histogram: collections.Counter[int] = collections.Counter()
    old_occurrence_count_histogram: collections.Counter[int] = collections.Counter()
    old_component_count_histogram: collections.Counter[int] = collections.Counter()
    source_round_classification: collections.Counter[str] = collections.Counter()
    region_ledger_rows: list[dict[str, Any]] = []
    region_binding: dict[str, dict[str, Any]] = {}
    base_component_ids = sorted(
        {row["provisional_component_id"] for row in component_rows}
    )
    need(len(base_component_ids) == 136_740, "Round280 provisional component universe")
    region_node_ids = {
        row_id: "round280-r275-region-node:" + digest(row_id)
        for row_id in regions
    }
    preview_dsu = DSU(base_component_ids + sorted(region_node_ids.values()))
    region_binding_requested = 0
    region_binding_rank = 0

    for row_id in sorted(regions):
        row = regions[row_id]
        box = region_boxes[row_id]
        guard = guard_boxes[row["source_guard_row_id"]]
        image_square = (
            1 - max(guard[0] * guard[0], guard[1] * guard[1]),
            1 - min(guard[0] * guard[0], guard[1] * guard[1]),
        )
        candidate_records: dict[tuple[str, int], tuple[str, int, tuple[Q, ...]]] = {}
        for t_bin in bins(box[0], box[1], 256):
            for p_bin in bins(box[2], box[3], 64):
                for record in atom_index.get(
                    (
                        row["adjacent_chart"],
                        row["complete_10_field_return_signature_sha256"],
                        t_bin,
                        p_bin,
                    ),
                    [],
                ):
                    candidate_records[(record[0], record[1])] = record
        relation_rows = []
        for atom_id, box_index, atom_box in candidate_records.values():
            atom = atom_by_id[atom_id]
            # Full object equality and owner equality are mandatory.  Hash
            # equality above is only a spatial-index key.
            if (
                atom["complete_10_field_return_signature"] != row["local_return_signature"]
                or atom["owner_target"] != row["owner_target"]
            ):
                continue
            relation = exact_relation(box, atom_box, image_square)
            if relation is None:
                continue
            relation_histogram[relation] += 1
            relation_rows.append(
                {
                    "canonical_atom_id": atom_id,
                    "atom_support_box_index": box_index,
                    "exact_relation": relation,
                    "atom_graph_class_id": atom_to_class[atom_id]["atom_graph_class_id"],
                }
            )
        atom_ids = sorted({item["canonical_atom_id"] for item in relation_rows})
        class_ids = sorted({item["atom_graph_class_id"] for item in relation_rows})
        class_components = sorted(
            {class_by_id[class_id]["provisional_component_id"] for class_id in class_ids}
        )
        old_occurrences = sorted(
            {
                occurrence
                for class_id in class_ids
                for occurrence in class_by_id[class_id]["existing_Round208_occurrence_ids"]
            }
        )
        old_components = sorted(
            {
                component
                for class_id in class_ids
                for component in class_by_id[class_id]["existing_Round266_component_ids"]
            }
        )
        class_count_histogram[len(class_ids)] += 1
        old_occurrence_count_histogram[len(old_occurrences)] += 1
        old_component_count_histogram[len(old_components)] += 1
        if not class_ids:
            classification = "NO_EXACT_ATOM_CLASS_BINDING__PROVISIONAL_R275_REGION_SEED"
        elif len(class_components) == 1:
            classification = "UNIQUE_ROUND280_PROVISIONAL_COMPONENT_BINDING__ZERO_CREDIT"
        else:
            classification = "MULTIPLE_ROUND280_PROVISIONAL_COMPONENT_BINDINGS__ZERO_CREDIT"
        source_round_classification[f"{row['source_round']}:{classification}"] += 1
        region_binding_requested += len(class_components)
        for component_id in class_components:
            region_binding_rank += preview_dsu.union(region_node_ids[row_id], component_id)
        binding_row = closed(
            {
                "Round275_region_incidence_row_id": "round280-r275-region-incidence:"
                + digest(row_id),
                "Round275_reverse_rechart_region_row_id": row_id,
                "source_round": row["source_round"],
                "source_guard_row_id": row["source_guard_row_id"],
                "source_chart": row["source_chart"],
                "adjacent_chart": row["adjacent_chart"],
                "owner_target": row["owner_target"],
                "official_key_id": row["local_return_signature"]["official_key_id"],
                "complete_10_field_return_signature_sha256": row[
                    "complete_10_field_return_signature_sha256"
                ],
                "exact_coordinate_identity_verified": True,
                "exact_algebraic_image_intersection_positive": True,
                "matching_atom_count": len(atom_ids),
                "matching_atom_ids": atom_ids,
                "matching_atom_graph_class_count": len(class_ids),
                "matching_atom_graph_class_ids": class_ids,
                "matching_Round280_provisional_component_count": len(class_components),
                "matching_Round280_provisional_component_ids": class_components,
                "matching_existing_Round208_occurrence_count": len(old_occurrences),
                "matching_existing_Round208_occurrence_ids": old_occurrences,
                "matching_existing_Round266_component_count": len(old_components),
                "matching_existing_Round266_component_ids": old_components,
                "exact_relation_rows_sha256": digest(
                    sorted(
                        relation_rows,
                        key=lambda item: (
                            item["canonical_atom_id"],
                            item["atom_support_box_index"],
                            item["exact_relation"],
                        ),
                    )
                ),
                "binding_classification": classification,
                "provisional_Round275_region_node_id": region_node_ids[row_id],
                "formal_expanded_occurrence_credit": 0,
                "formal_component_union_credit": 0,
                "formal_maximality_credit": 0,
            }
        )
        region_ledger_rows.append(binding_row)
        region_binding[row_id] = binding_row

    patch_rows: list[dict[str, Any]] = []
    patch_guard_histogram: collections.Counter[int] = collections.Counter()
    patch_region_histogram: collections.Counter[int] = collections.Counter()
    patch_conditional_edge_histogram: collections.Counter[int] = collections.Counter()
    patch_conditional_atom_join_histogram: collections.Counter[str] = collections.Counter()
    endpoint_conditional_atom_join_histogram: collections.Counter[str] = collections.Counter()
    orphan_endpoint_direction_histogram: collections.Counter[str] = collections.Counter()
    endpoint_pair_classification_histogram: collections.Counter[str] = collections.Counter()
    conditional_seam_requested = 0
    conditional_seam_rank = 0
    direct_seam_incident_patch_count = 0

    for patch in patches:
        patch_box = tuple(
            Q(value)
            for value in patch["exact_common_p_interval"] + patch["exact_common_s_interval"]
        )
        side_records = []
        side_pair_inputs = []
        for side in ("left", "right"):
            seam = seams[patch[f"{side}_Round182_source_seam_row_id"]]
            root = patch[f"{side}_local_t_root"]
            target_chart = adjacent_chart(seam["chart"], root)
            selected_guards = []
            selected_regions = []
            source_margins = []
            target_margins = []
            for guard_row in guards_by_parent_chart[(seam["parent_id"], seam["chart"])]:
                guard = guard_boxes[guard_row["row_id"]]
                correct_root = guard[0] > 0 if root == "+" else guard[1] < 0
                strict_exterior = min(2 * guard[0] * guard[0], 2 * guard[1] * guard[1]) > 1
                if not (
                    correct_root
                    and strict_exterior
                    and positive_overlap(guard[2], guard[3], patch_box[0], patch_box[1])
                    and positive_overlap(guard[4], guard[5], patch_box[2], patch_box[3])
                ):
                    continue
                selected_guards.append(guard_row)
                near = guard[0] if root == "+" else guard[1]
                source_margins.append(2 * near * near - 1)
                for region in regions_by_guard[guard_row["row_id"]]:
                    region_box = region_boxes[region["reverse_rechart_region_row_id"]]
                    if not (
                        region["adjacent_chart"] == target_chart
                        and positive_overlap(
                            region_box[2], region_box[3], patch_box[0], patch_box[1]
                        )
                        and positive_overlap(
                            region_box[4], region_box[5], patch_box[2], patch_box[3]
                        )
                    ):
                        continue
                    selected_regions.append(region)
                    target_margins.append(
                        1 - 2 * max(region_box[0] * region_box[0], region_box[1] * region_box[1])
                    )
            need(selected_guards and selected_regions, "complete patch guard channel")
            need(all(value > 0 for value in source_margins + target_margins), "strict seam gap")
            patch_guard_histogram[len(selected_guards)] += 1
            patch_region_histogram[len(selected_regions)] += 1
            selected_region_ids = sorted(
                row["reverse_rechart_region_row_id"] for row in selected_regions
            )
            selected_binding_rows = [
                region_binding[row_id] for row_id in selected_region_ids
            ]
            bound_region_count = sum(
                row["matching_atom_graph_class_count"] > 0
                for row in selected_binding_rows
            )
            orphan_region_count = len(selected_binding_rows) - bound_region_count
            unique_binding_region_count = sum(
                row["matching_Round280_provisional_component_count"] == 1
                for row in selected_binding_rows
            )
            multiple_binding_region_count = sum(
                row["matching_Round280_provisional_component_count"] > 1
                for row in selected_binding_rows
            )
            endpoint_class_ids = sorted(
                {
                    class_id
                    for row in selected_binding_rows
                    for class_id in row["matching_atom_graph_class_ids"]
                }
            )
            endpoint_component_ids = sorted(
                {
                    component_id
                    for row in selected_binding_rows
                    for component_id in row[
                        "matching_Round280_provisional_component_ids"
                    ]
                }
            )
            endpoint_old_components = sorted(
                {
                    component_id
                    for row in selected_binding_rows
                    for component_id in row["matching_existing_Round266_component_ids"]
                }
            )
            if not endpoint_class_ids:
                endpoint_join_classification = (
                    "CONDITIONAL_ATOM_JOIN_ORPHAN__NO_R275_REGION_BINDS_A_R279_ATOM"
                )
            elif (
                orphan_region_count == 0
                and multiple_binding_region_count == 0
                and len(endpoint_component_ids) == 1
            ):
                endpoint_join_classification = (
                    "CONDITIONAL_UNIQUE_R280_COMPONENT_CHANNEL__NORMAL_CORRIDOR_MISSING"
                )
            else:
                endpoint_join_classification = (
                    "CONDITIONAL_AMBIGUOUS_R280_COMPONENT_CHANNEL__"
                    "ORPHAN_OR_MULTIPLE_REGION_BINDINGS"
                )
            endpoint_conditional_atom_join_histogram[endpoint_join_classification] += 1
            if endpoint_join_classification.startswith(
                "CONDITIONAL_ATOM_JOIN_ORPHAN"
            ):
                orphan_endpoint_direction_histogram[
                    f"{seam['chart']}->{target_chart}:{root}"
                ] += 1
            pair_inputs = []
            for region in selected_regions:
                row_id = region["reverse_rechart_region_row_id"]
                region_box = region_boxes[row_id]
                footprint = (
                    max(patch_box[0], region_box[2]),
                    min(patch_box[1], region_box[3]),
                    max(patch_box[2], region_box[4]),
                    min(patch_box[3], region_box[5]),
                )
                need(footprint[0] < footprint[1] and footprint[2] < footprint[3], "positive p/s footprint")
                pair_inputs.append((row_id, footprint))
            side_pair_inputs.append(pair_inputs)
            side_records.append(
                {
                    "side": side,
                    "Round182_source_seam_row_id": seam["row_id"],
                    "source_chart": seam["chart"],
                    "local_t_root": root,
                    "adjacent_chart": target_chart,
                    "candidate_guard_count": len(selected_guards),
                    "candidate_guard_row_ids": sorted(row["row_id"] for row in selected_guards),
                    "candidate_Round275_region_count": len(selected_regions),
                    "candidate_Round275_region_ids": selected_region_ids,
                    "candidate_Round275_region_ids_sha256": digest(selected_region_ids),
                    "candidate_atom_bound_region_count": bound_region_count,
                    "candidate_atom_orphan_region_count": orphan_region_count,
                    "candidate_unique_component_binding_region_count": unique_binding_region_count,
                    "candidate_multiple_component_binding_region_count": multiple_binding_region_count,
                    "candidate_atom_graph_class_count": len(endpoint_class_ids),
                    "candidate_atom_graph_class_ids_sha256": digest(endpoint_class_ids),
                    "candidate_Round280_provisional_component_count": len(
                        endpoint_component_ids
                    ),
                    "candidate_Round280_provisional_component_ids_sha256": digest(
                        endpoint_component_ids
                    ),
                    "candidate_existing_Round266_component_count": len(
                        endpoint_old_components
                    ),
                    "candidate_existing_Round266_component_ids_sha256": digest(
                        endpoint_old_components
                    ),
                    "conditional_atom_join_classification": endpoint_join_classification,
                    "minimum_exact_source_seam_gap_2t2_minus_1": qtext(min(source_margins)),
                    "minimum_exact_adjacent_seam_gap_1_minus_2tprime2": qtext(
                        min(target_margins)
                    ),
                    "direct_exact_seam_incident_region_count": 0,
                }
            )

        pair_descriptors = []
        conditional_node_pairs: set[tuple[str, str]] = set()
        for left_region_id, left_footprint in side_pair_inputs[0]:
            for right_region_id, right_footprint in side_pair_inputs[1]:
                plo = max(left_footprint[0], right_footprint[0])
                phi = min(left_footprint[1], right_footprint[1])
                slo = max(left_footprint[2], right_footprint[2])
                shi = min(left_footprint[3], right_footprint[3])
                if not (plo < phi and slo < shi):
                    continue
                pair_descriptors.append(
                    [
                        left_region_id,
                        right_region_id,
                        qtext(plo),
                        qtext(phi),
                        qtext(slo),
                        qtext(shi),
                    ]
                )
                conditional_node_pairs.add(
                    tuple(
                        sorted(
                            (
                                region_node_ids[left_region_id],
                                region_node_ids[right_region_id],
                            )
                        )
                    )
                )
        need(pair_descriptors and conditional_node_pairs, "positive conditional patch pairs")
        pair_descriptors.sort()
        patch_conditional_edge_histogram[len(conditional_node_pairs)] += 1
        endpoint_classes = [
            row["conditional_atom_join_classification"] for row in side_records
        ]
        endpoint_pair_classification_histogram["|".join(endpoint_classes)] += 1
        unique_label = (
            "CONDITIONAL_UNIQUE_R280_COMPONENT_CHANNEL__NORMAL_CORRIDOR_MISSING"
        )
        orphan_label = (
            "CONDITIONAL_ATOM_JOIN_ORPHAN__NO_R275_REGION_BINDS_A_R279_ATOM"
        )
        if endpoint_classes == [unique_label, unique_label]:
            patch_atom_join_classification = (
                "CONDITIONAL_UNIQUE_COMPONENT_EDGE_PREVIEW__NORMAL_CORRIDORS_MISSING"
            )
        elif orphan_label in endpoint_classes:
            patch_atom_join_classification = (
                "CONDITIONAL_ATOM_JOIN_ORPHAN_PATCH__NORMAL_CORRIDORS_AND_ATOM_BINDING_MISSING"
            )
        else:
            patch_atom_join_classification = (
                "CONDITIONAL_AMBIGUOUS_COMPONENT_EDGE_PREVIEW__NORMAL_CORRIDORS_MISSING"
            )
        patch_conditional_atom_join_histogram[patch_atom_join_classification] += 1
        conditional_seam_requested += len(conditional_node_pairs)
        rank_before = conditional_seam_rank
        for left_node, right_node in sorted(conditional_node_pairs):
            conditional_seam_rank += preview_dsu.union(left_node, right_node)
        patch_rows.append(
            closed(
                {
                    "Round268_patch_channel_row_id": "round280-seam-channel:"
                    + digest(patch["true_seam_patch_row_id"]),
                    "Round268_true_seam_patch_row_id": patch["true_seam_patch_row_id"],
                    "cyclic_transition_identity": patch["cyclic_transition_identity"],
                    "exact_common_p_interval": patch["exact_common_p_interval"],
                    "exact_common_s_interval": patch["exact_common_s_interval"],
                    "exact_positive_common_area": patch["exact_positive_common_area"],
                    "owner_shadow_half_open_pair_verified": patch[
                        "owner_shadow_half_open_pair"
                    ],
                    "forward_reverse_coordinate_identity_verified_on_all_candidate_regions": True,
                    "side_channel_rows": side_records,
                    "conditional_positive_area_region_pair_count": len(pair_descriptors),
                    "conditional_positive_area_region_pairs_sha256": digest(pair_descriptors),
                    "conditional_unique_Round275_region_node_edge_count": len(
                        conditional_node_pairs
                    ),
                    "conditional_patch_rank_reduction_count": conditional_seam_rank
                    - rank_before,
                    "conditional_atom_join_classification": patch_atom_join_classification,
                    "direct_exact_seam_incident_region_count": 0,
                    "direct_component_edge_credit": 0,
                    "conditional_only_classification": (
                        "POSITIVE_PS_PROJECTION_ONLY__STRICT_NORMAL_GAP_ON_BOTH_SIDES__"
                        "EXPLICIT_SEAM_NORMAL_CORRIDOR_REQUIRED"
                    ),
                    "Jx_Jy_same_point_glue_credit": 0,
                    "formal_component_union_credit": 0,
                    "formal_maximality_credit": 0,
                }
            )
        )

    need(len(patch_rows) == 152, "complete patch ledger")
    need(direct_seam_incident_patch_count == 0, "no direct seam promotion")

    region_payload = ledger(
        region_ledger_rows,
        "Round275_region_incidence_row_id",
        schema="cm2.round280.rechart-region-incidence.zero-credit.v1",
        status="ROUND280_RECHART_REGION_INCIDENCE_PROBE__ZERO_CREDIT",
        strict_nonpromotion=True,
    )
    patch_payload = ledger(
        patch_rows,
        "Round268_patch_channel_row_id",
        schema="cm2.round280.true-seam-channel.zero-credit.v1",
        status="ROUND280_TRUE_SEAM_CHANNEL_PROBE__CONDITIONAL_ONLY__ZERO_CREDIT",
        strict_nonpromotion=True,
    )
    gzip_write(REGION_LEDGER, region_payload)
    gzip_write(PATCH_LEDGER, patch_payload)

    class_histogram_text = {
        str(key): value for key, value in sorted(class_count_histogram.items())
    }
    result = {
        "schema": "cm2.round280.true-seam-and-rechart-incidence-probe.v1",
        "status": (
            "PASS_ROUND280_EXACT_RECHART_REGION_BINDING_AUDIT__"
            "TRUE_SEAM_REMAINS_FAIL_CLOSED_FOR_MISSING_NORMAL_CORRIDORS__ZERO_CREDIT"
        ),
        "census": {
            "Round275_reverse_rechart_region_count": 13_788,
            "Round275_region_exact_atom_class_count_histogram": class_histogram_text,
            "Round275_region_without_atom_class_binding_count": class_count_histogram[0],
            "Round275_region_with_one_atom_class_binding_count": class_count_histogram[1],
            "Round275_region_with_multiple_atom_class_bindings_count": sum(
                value for key, value in class_count_histogram.items() if key > 1
            ),
            "Round275_region_existing_Round208_occurrence_count_histogram": {
                str(key): value
                for key, value in sorted(old_occurrence_count_histogram.items())
            },
            "Round275_region_existing_Round266_component_count_histogram": {
                str(key): value
                for key, value in sorted(old_component_count_histogram.items())
            },
            "exact_region_atom_relation_histogram": dict(sorted(relation_histogram.items())),
            "source_round_binding_classification_histogram": dict(
                sorted(source_round_classification.items())
            ),
            "Round268_true_seam_patch_count": 152,
            "patch_side_candidate_guard_count_histogram": {
                str(key): value for key, value in sorted(patch_guard_histogram.items())
            },
            "patch_side_candidate_region_count_histogram": {
                str(key): value for key, value in sorted(patch_region_histogram.items())
            },
            "direct_exact_seam_incident_patch_count": 0,
            "direct_source_seam_origin_to_Round279_atom_count": (
                direct_source_seam_origin_atom_count
            ),
            "conditional_positive_projection_patch_count": 152,
            "conditional_patch_region_node_edge_count_histogram": {
                str(key): value
                for key, value in sorted(patch_conditional_edge_histogram.items())
            },
            "patch_conditional_atom_join_classification_histogram": dict(
                sorted(patch_conditional_atom_join_histogram.items())
            ),
            "patch_endpoint_conditional_atom_join_classification_histogram": dict(
                sorted(endpoint_conditional_atom_join_histogram.items())
            ),
            "patch_endpoint_pair_classification_histogram": dict(
                sorted(endpoint_pair_classification_histogram.items())
            ),
            "atom_orphan_endpoint_source_to_adjacent_direction_histogram": dict(
                sorted(orphan_endpoint_direction_histogram.items())
            ),
        },
        "zero_credit_rank_preview": {
            "Round280_base_provisional_component_node_count": len(base_component_ids),
            "Round275_region_node_count": len(region_node_ids),
            "pre_relation_node_count": len(base_component_ids) + len(region_node_ids),
            "requested_exact_region_to_Round280_component_relation_count": region_binding_requested,
            "exact_region_to_Round280_component_rank_reduction_count": region_binding_rank,
            "conditional_requested_true_seam_region_edge_count": conditional_seam_requested,
            "conditional_true_seam_rank_reduction_count_after_region_bindings": conditional_seam_rank,
            "conditional_component_count_after_included_relations": (
                len(base_component_ids)
                + len(region_node_ids)
                - region_binding_rank
                - conditional_seam_rank
            ),
            "excluded_Round275_region_to_region_relation_gate": True,
            "excluded_seam_normal_corridor_gate": True,
            "formal_DSU_rank_credit": 0,
        },
        "exact_blocker": {
            "all_13788_regions_intersect_their_exact_algebraic_rechart_images": True,
            "all_152_patches_have_positive_p_s_projection_to_Round275_channels": True,
            "every_candidate_Round275_region_is_strictly_inside_the_adjacent_chart": True,
            "every_candidate_guard_is_strictly_outside_the_source_chart": True,
            "no_rational_Round275_region_closure_contains_the_irrational_t_squared_equals_one_half_seam": True,
            "positive_p_s_projection_is_not_a_same_point_component_edge": True,
            "required_next_certificate": (
                "For every patch-side cell, construct an exact connected seam-normal "
                "corridor from t^2=1/2 to a uniquely identified Round275 region/atom "
                "class, carrying the complete return signature and half-open boundary "
                "exclusions; separately exhaust Round275 region-to-region physical "
                "overlap/common-face relations."
            ),
        },
        "attachments": {
            "Round275_region_binding_ledger": {
                "path": REGION_LEDGER.name,
                "file_sha256": file_sha256(REGION_LEDGER),
                "row_count": region_payload["row_count"],
                "rows_sha256": region_payload["rows_sha256"],
                "row_ids_sha256": region_payload["row_ids_sha256"],
                "row_hashes_sha256": region_payload["row_hashes_sha256"],
            },
            "Round268_patch_channel_ledger": {
                "path": PATCH_LEDGER.name,
                "file_sha256": file_sha256(PATCH_LEDGER),
                "row_count": patch_payload["row_count"],
                "rows_sha256": patch_payload["rows_sha256"],
                "row_ids_sha256": patch_payload["row_ids_sha256"],
                "row_hashes_sha256": patch_payload["row_hashes_sha256"],
            },
        },
        "provenance": {
            "producer_sha256": producer_sha256,
            "input_file_sha256": dict(sorted(PINS.items())),
            "Round280_atom_class_source_is_zero_credit_preview": True,
            "Round280_result_status": r280["status"],
        },
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_union_credit": 0,
            "DSU_rank_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "frozen_quotient_component_count": 63_224,
            "frozen_expanded_occurrence_count": 126_468,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    envelope = {"result": result, "result_sha256": digest(result)}
    atomic_write(RESULT, canonical(envelope) + b"\n")
    print(json.dumps(envelope, sort_keys=True, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
