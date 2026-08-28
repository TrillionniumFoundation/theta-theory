#!/usr/bin/env python3
"""Round280 zero-credit atom-class and DSU preview.

This probe deliberately does *not* promote each Round279 atom to an expanded
occurrence.  It first quotients the canonical atoms by the complete Round279
common-face graph.  The resulting connected atom classes are then classified
by their existing Round208 occurrence anchors:

* an unanchored atom class is only a provisional new-occurrence candidate;
* a singly anchored class is connectivity evidence attached to an existing
  occurrence, not a new occurrence;
* a multiply anchored class is component-union evidence, but does not by
  itself collapse the identities of the existing occurrence rows.

The component preview starts from the 63,224 frozen Round266 components and
uses only multiply anchored Round279 atom classes.  It explicitly excludes all
152 Round268 true-seam patches and all Jx/Jy relations.  Every output remains
strictly zero-credit.

Normal execution requires a full ``PASS_INDEPENDENT_ROUND279`` verification.
``--allow-preliminary-round279`` exists only so that the schema and arithmetic
can be exercised while Round279 is being rebuilt; such output is marked
PRELIMINARY and is not a frozen result.
"""
from __future__ import annotations

import argparse
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
PREFIX = "cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe"

ROUND266_CERTIFICATE = (
    HERE / "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
)
ROUND266_VERIFICATION = (
    HERE / "cm2_round266_source_g_expanded_curved_face_closure_verification.json"
)
ROUND279_PRODUCER = (
    HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze.py"
)
ROUND279_CERTIFICATE = (
    HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_certificate.json"
)
ROUND279_ATOMS = (
    HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
)
ROUND279_EDGES = (
    HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz"
)
ROUND279_VERIFICATION = (
    HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_verification.json"
)
ROUND279_VERIFIER = (
    HERE / "cm2_round279_source_g_collar_atom_and_face_edge_freeze_verifier.py"
)

RESULT = HERE / f"{PREFIX}_result.json"
ATOM_BINDINGS = HERE / f"{PREFIX}_atom_bindings.json.gz"
ATOM_CLASSES = HERE / f"{PREFIX}_atom_graph_classes.json.gz"
COMPONENTS = HERE / f"{PREFIX}_provisional_components.json.gz"

ROUND266_CERTIFICATE_SHA256 = (
    "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf"
)
ROUND266_VERIFICATION_SHA256 = (
    "a6436c716cbbe74f0195e2d87f4084a28ca2a2e27b9fe5eeb98b6835df92b75b"
)


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


def closed(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    need("row_sha256" not in result, "row not already closed")
    result["row_sha256"] = digest(result)
    return result


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


def gzip_payload(payload: dict[str, Any]) -> bytes:
    raw = canonical(payload) + b"\n"
    return gzip.compress(raw, compresslevel=9, mtime=0)


def validate_closed_row(row: dict[str, Any], label: str) -> None:
    need("row_sha256" in row, f"{label}:row hash present")
    body = dict(row)
    claimed = body.pop("row_sha256")
    need(claimed == digest(body), f"{label}:row hash")


def validate_ledger(
    ledger: dict[str, Any],
    row_id_field: str,
    expected_count: int,
    label: str,
) -> list[dict[str, Any]]:
    rows = ledger["rows"]
    need(ledger["row_count"] == len(rows) == expected_count, f"{label}:count")
    need(ledger["rows_sha256"] == digest(rows), f"{label}:rows digest")
    ids = [row[row_id_field] for row in rows]
    need(len(set(ids)) == len(ids), f"{label}:unique ids")
    if "row_ids_sha256" in ledger:
        need(ledger["row_ids_sha256"] == digest(ids), f"{label}:ids digest")
    hashes = [row["row_sha256"] for row in rows]
    if "row_hashes_sha256" in ledger:
        need(
            ledger["row_hashes_sha256"] == digest(hashes),
            f"{label}:row hashes digest",
        )
    for row in rows:
        validate_closed_row(row, label)
    return rows


def validate_attachment(
    payload: dict[str, Any],
    attachment: dict[str, Any],
    raw: bytes,
    row_id_field: str,
    expected_count: int,
    label: str,
) -> list[dict[str, Any]]:
    need(
        attachment["file_sha256"] == hashlib.sha256(raw).hexdigest(),
        f"{label}:attachment file digest",
    )
    rows = validate_ledger(payload, row_id_field, expected_count, label)
    for field in ("row_count", "rows_sha256", "row_ids_sha256", "row_hashes_sha256"):
        need(attachment[field] == payload[field], f"{label}:attachment {field}")
    return rows


def qbox(values: list[str]) -> tuple[Q, ...]:
    result = tuple(Q(value) for value in values)
    need(len(result) == 6, "six support coordinates")
    return result


def positive_volume(box: tuple[Q, ...]) -> Q:
    volume = Q(1)
    for axis in range(3):
        width = box[2 * axis + 1] - box[2 * axis]
        need(width > 0, "strict positive support width")
        volume *= width
    return volume


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
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        if (
            self.size[left] < self.size[right]
            or (self.size[left] == self.size[right] and left > right)
        ):
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True


def load_round266() -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    need(
        file_sha256(ROUND266_CERTIFICATE) == ROUND266_CERTIFICATE_SHA256,
        "Round266 certificate pin",
    )
    need(
        file_sha256(ROUND266_VERIFICATION) == ROUND266_VERIFICATION_SHA256,
        "Round266 verification pin",
    )
    verification = json.loads(ROUND266_VERIFICATION.read_bytes())
    need(verification["status"] == "PASS_INDEPENDENT_ROUND266", "Round266 PASS")
    document = json.loads(ROUND266_CERTIFICATE.read_bytes())
    result = document["result"]
    need(document["result_sha256"] == digest(result), "Round266 result digest")
    census = result["census"]
    need(
        census["post_Round266_component_count"] == 63_224
        and census["complete_occurrence_frontier_count"] == 126_468
        and census["complete_exact_key_frontier_count"] == 116,
        "Round266 frozen census",
    )
    component_rows = validate_ledger(
        result["formal_post_Round266_component_frontier_ledger"],
        "post_Round266_component_frontier_row_id",
        63_224,
        "Round266 component",
    )
    occurrence_rows = validate_ledger(
        result["formal_post_Round266_expanded_occurrence_frontier_ledger"],
        "post_Round266_expanded_occurrence_frontier_row_id",
        126_468,
        "Round266 occurrence",
    )
    components = {
        row["post_Round266_quotient_component_id"]: row for row in component_rows
    }
    occurrences = {row["local_occurrence_row_id"]: row for row in occurrence_rows}
    need(len(components) == 63_224, "Round266 unique component ids")
    need(len(occurrences) == 126_468, "Round266 unique occurrence ids")
    return occurrences, components, result


def load_round279(
    allow_preliminary: bool,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
    dict[str, Any],
]:
    certificate_raw = ROUND279_CERTIFICATE.read_bytes()
    document = json.loads(certificate_raw)
    result = document["result"]
    need(document["result_sha256"] == digest(result), "Round279 result digest")
    need(
        result["status"] == "PASS_PRODUCER_ROUND279__FORMAL_ZERO_CREDIT_FREEZE",
        "Round279 producer status",
    )
    atom_raw = ROUND279_ATOMS.read_bytes()
    edge_raw = ROUND279_EDGES.read_bytes()
    atom_payload = json.loads(gzip.decompress(atom_raw))
    edge_payload = json.loads(gzip.decompress(edge_raw))
    atom_rows = validate_attachment(
        atom_payload,
        result["canonical_atom_ledger_attachment"],
        atom_raw,
        "canonical_atom_id",
        332_016,
        "Round279 atom",
    )
    edge_rows = validate_attachment(
        edge_payload,
        result["formal_common_face_edge_witness_ledger_attachment"],
        edge_raw,
        "formal_face_edge_witness_row_id",
        330_724,
        "Round279 edge",
    )
    need(
        result["exact_partition_contract"]["Round268_true_seam_edges_included"]
        is False,
        "Round279 excludes Round268 seams",
    )
    need(
        result["exact_partition_contract"]["Jx_Jy_same_point_edges_included"]
        is False,
        "Round279 excludes Jx/Jy",
    )

    readiness_issues: list[str] = []
    actual_producer_sha256 = file_sha256(ROUND279_PRODUCER)
    recorded_producer_sha256 = result["provenance"]["producer_file_sha256"]
    if actual_producer_sha256 != recorded_producer_sha256:
        readiness_issues.append(
            "producer_sha256_mismatch:"
            f"{recorded_producer_sha256}!={actual_producer_sha256}"
        )
    verification: dict[str, Any] | None = None
    verification_sha256: str | None = None
    if not ROUND279_VERIFICATION.exists():
        readiness_issues.append("full_independent_verification_missing")
    else:
        verification_sha256 = file_sha256(ROUND279_VERIFICATION)
        verification = json.loads(ROUND279_VERIFICATION.read_bytes())
        if verification.get("status") != "PASS_INDEPENDENT_ROUND279":
            readiness_issues.append(
                "full_independent_verification_not_PASS:"
                f"{verification.get('status')}"
            )
        if (
            verification.get("certificate_result_sha256")
            != document["result_sha256"]
        ):
            readiness_issues.append("verification_certificate_pin_mismatch")
        if verification.get("dynamic_verification_histogram") != {
            "PASS": 330_724
        }:
            readiness_issues.append("dynamic_edge_verification_not_complete")
    if readiness_issues and not allow_preliminary:
        raise ProbeError(
            "Round279 is not frozen: " + ";".join(readiness_issues)
        )
    readiness = {
        "round279_fully_frozen": not readiness_issues,
        "preliminary_override_used": bool(readiness_issues),
        "readiness_issues": readiness_issues,
        "producer_sha256_recorded": recorded_producer_sha256,
        "producer_sha256_actual": actual_producer_sha256,
        "certificate_sha256": hashlib.sha256(certificate_raw).hexdigest(),
        "certificate_result_sha256": document["result_sha256"],
        "atom_ledger_sha256": hashlib.sha256(atom_raw).hexdigest(),
        "edge_ledger_sha256": hashlib.sha256(edge_raw).hexdigest(),
        "verifier_sha256": (
            file_sha256(ROUND279_VERIFIER) if ROUND279_VERIFIER.exists() else None
        ),
        "verification_sha256": verification_sha256,
        "verification_status": (
            verification.get("status") if verification is not None else None
        ),
    }
    return atom_rows, edge_rows, result, readiness


def build(
    atoms: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    occurrences266: dict[str, dict[str, Any]],
    components266: dict[str, dict[str, Any]],
    readiness: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    atom_by_id = {row["canonical_atom_id"]: row for row in atoms}
    need(len(atom_by_id) == 332_016, "unique Round279 atoms")

    direct_occurrence_by_atom: dict[str, str] = {}
    support_volume_by_atom: dict[str, Q] = {}
    direct_count = 0
    new_atom_candidate_count = 0
    strict_support_count = 0
    total_support_volume = Q(0)
    keys_seen: set[str] = set()
    for atom in atoms:
        atom_id = atom["canonical_atom_id"]
        signature = atom["complete_10_field_return_signature"]
        need(
            atom["complete_10_field_return_signature_sha256"]
            == digest(signature),
            f"atom signature digest:{atom_id}",
        )
        key_id = signature["official_key_id"]
        keys_seen.add(key_id)
        need(
            signature["source_chart"] == atom["source_chart"]
            and signature["target_lift"] == atom["owner_target"],
            f"atom signature provenance:{atom_id}",
        )
        supports = atom["frozen_true_support_boxes"]
        need(len(supports) == 1, f"one normalized support box:{atom_id}")
        support = qbox(supports[0])
        whole = qbox(atom["whole_Round182_leaf_box"])
        volume = positive_volume(support)
        for axis in range(3):
            need(
                whole[2 * axis] <= support[2 * axis]
                and support[2 * axis + 1] <= whole[2 * axis + 1],
                f"support inside leaf:{atom_id}",
            )
        strict = support != whole
        need(
            strict
            == (atom["support_classification"] == "STRICT_FROZEN_SUBBOX"),
            f"support classification:{atom_id}",
        )
        strict_support_count += int(strict)
        support_volume_by_atom[atom_id] = volume
        total_support_volume += volume

        direct_ids = atom["existing_Round208_occurrence_row_ids"]
        need(len(direct_ids) <= 1, f"at most one Round208 anchor:{atom_id}")
        if direct_ids:
            direct_count += 1
            occurrence_id = direct_ids[0]
            need(
                occurrence_id in occurrences266,
                f"Round208 occurrence in Round266 frontier:{occurrence_id}",
            )
            source = occurrences266[occurrence_id]
            component_id = source["post_Round266_quotient_component_id"]
            need(component_id in components266, f"Round266 component:{component_id}")
            need(
                source["occurrence_source"] == "ROUND208_REGION"
                and source["source_geometry_row_id"] == occurrence_id,
                f"Round208 occurrence identity:{occurrence_id}",
            )
            need(
                source["official_key_id"] == key_id
                and source["official_key_ordinal"]
                == signature["official_key_ordinal"]
                and source["complete_10_field_return_signature_sha256"]
                == atom["complete_10_field_return_signature_sha256"]
                and source["source_chart"] == atom["source_chart"],
                f"Round208 occurrence signature binding:{occurrence_id}",
            )
            need(
                source["exact_box_sha256"] == digest(supports[0]),
                f"Round208 occurrence exact box:{occurrence_id}",
            )
            need(
                components266[component_id]["official_key_id"] == key_id,
                f"Round208 component key purity:{occurrence_id}",
            )
            direct_occurrence_by_atom[atom_id] = occurrence_id
        else:
            new_atom_candidate_count += 1
    need(
        direct_count == 36_040
        and new_atom_candidate_count == 295_976
        and strict_support_count == 4,
        "atom provenance census",
    )

    # First quotient atoms by the complete local common-face graph.
    atom_dsu = DSU(sorted(atom_by_id))
    edge_rank_reductions = 0
    edge_key_histogram: collections.Counter[str] = collections.Counter()
    seen_candidate_indices: list[int] = []
    distinct_atom_edge_pairs: set[tuple[str, str]] = set()
    for edge in edges:
        endpoints = edge["endpoint_atoms"]
        need(len(endpoints) == 2, "two edge endpoints")
        left, right = [entry["canonical_atom_id"] for entry in endpoints]
        need(left != right, "distinct edge endpoint atoms")
        need(left in atom_by_id and right in atom_by_id, "edge atoms exist")
        signature_hash = edge[
            "complete_10_field_return_signature_sha256"
        ]
        for atom_id in (left, right):
            need(
                atom_by_id[atom_id][
                    "complete_10_field_return_signature_sha256"
                ]
                == signature_hash,
                f"edge signature purity:{edge['candidate_index']}",
            )
        key_id = atom_by_id[left][
            "complete_10_field_return_signature"
        ]["official_key_id"]
        need(
            atom_by_id[right]["complete_10_field_return_signature"][
                "official_key_id"
            ]
            == key_id,
            f"edge exact-key purity:{edge['candidate_index']}",
        )
        edge_key_histogram[key_id] += 1
        seen_candidate_indices.append(edge["candidate_index"])
        distinct_atom_edge_pairs.add(tuple(sorted((left, right))))
        edge_rank_reductions += int(atom_dsu.union(left, right))
    need(
        seen_candidate_indices == list(range(330_724)),
        "complete deterministic edge index coverage",
    )
    need(
        len(distinct_atom_edge_pairs) == 330_724,
        "all Round279 atom endpoint pairs distinct",
    )

    raw_classes: dict[str, list[str]] = collections.defaultdict(list)
    for atom_id in sorted(atom_by_id):
        raw_classes[atom_dsu.find(atom_id)].append(atom_id)
    need(
        len(raw_classes) == 92_120
        and edge_rank_reductions == 239_896,
        "atom graph quotient census",
    )

    class_work: list[dict[str, Any]] = []
    class_by_atom: dict[str, str] = {}
    anchor_component_relation_count = 0
    for member_ids in raw_classes.values():
        member_ids.sort()
        descriptors = [
            {
                "canonical_atom_id": atom_id,
                "Round279_atom_row_sha256": atom_by_id[atom_id]["row_sha256"],
            }
            for atom_id in member_ids
        ]
        class_id = "round280-atom-graph-class:" + digest(descriptors)
        need(
            all(atom_id not in class_by_atom for atom_id in member_ids),
            f"unique atom class assignment:{class_id}",
        )
        for atom_id in member_ids:
            class_by_atom[atom_id] = class_id
        signatures = {
            atom_by_id[atom_id][
                "complete_10_field_return_signature_sha256"
            ]
            for atom_id in member_ids
        }
        key_ids = {
            atom_by_id[atom_id]["complete_10_field_return_signature"][
                "official_key_id"
            ]
            for atom_id in member_ids
        }
        key_ordinals = {
            atom_by_id[atom_id]["complete_10_field_return_signature"][
                "official_key_ordinal"
            ]
            for atom_id in member_ids
        }
        need(
            len(signatures) == len(key_ids) == len(key_ordinals) == 1,
            f"atom class signature/key purity:{class_id}",
        )
        occurrence_ids = sorted(
            direct_occurrence_by_atom[atom_id]
            for atom_id in member_ids
            if atom_id in direct_occurrence_by_atom
        )
        need(len(set(occurrence_ids)) == len(occurrence_ids), "unique class anchors")
        component_ids = sorted(
            {
                occurrences266[occurrence_id][
                    "post_Round266_quotient_component_id"
                ]
                for occurrence_id in occurrence_ids
            }
        )
        anchor_component_relation_count += max(0, len(component_ids) - 1)
        if not occurrence_ids:
            disposition = (
                "UNANCHORED_CONNECTED_ATOM_CLASS__"
                "PROVISIONAL_NEW_OCCURRENCE_CANDIDATE__NOT_PROMOTED"
            )
        elif len(occurrence_ids) == 1:
            disposition = (
                "SINGLE_EXISTING_OCCURRENCE_ANCHORED__"
                "CONNECTIVITY_ATTACHMENT_ONLY__NOT_PROMOTED"
            )
        else:
            disposition = (
                "MULTIPLE_EXISTING_OCCURRENCES_CONNECTED__"
                "COMPONENT_UNION_EVIDENCE_ONLY__"
                "OCCURRENCE_IDENTITIES_NOT_COLLAPSED"
            )
        class_work.append(
            {
                "atom_graph_class_id": class_id,
                "canonical_atom_ids": member_ids,
                "canonical_atom_ids_sha256": digest(member_ids),
                "canonical_atom_descriptor_sha256": digest(descriptors),
                "atom_count": len(member_ids),
                "new_atom_candidate_count": sum(
                    atom_id not in direct_occurrence_by_atom
                    for atom_id in member_ids
                ),
                "existing_Round208_occurrence_ids": occurrence_ids,
                "existing_Round208_occurrence_ids_sha256": digest(occurrence_ids),
                "existing_Round208_occurrence_count": len(occurrence_ids),
                "existing_Round266_component_ids": component_ids,
                "existing_Round266_component_ids_sha256": digest(component_ids),
                "existing_Round266_component_count": len(component_ids),
                "complete_10_field_return_signature_sha256": next(
                    iter(signatures)
                ),
                "official_key_id": next(iter(key_ids)),
                "official_key_ordinal": next(iter(key_ordinals)),
                "exact_support_box_count": len(member_ids),
                "exact_support_coordinate_volume_sum": str(
                    sum(
                        (support_volume_by_atom[atom_id] for atom_id in member_ids),
                        Q(0),
                    )
                ),
                "occurrence_identity_disposition": disposition,
            }
        )
    need(len(class_by_atom) == 332_016, "complete atom class assignment")
    class_work.sort(key=lambda row: row["atom_graph_class_id"])

    # Preview component unions induced only by anchored atom classes.
    anchor_dsu = DSU(sorted(components266))
    requested_anchor_relations = 0
    anchor_rank_reductions = 0
    for entry in class_work:
        component_ids = entry["existing_Round266_component_ids"]
        if component_ids:
            for component_id in component_ids:
                need(
                    components266[component_id]["official_key_id"]
                    == entry["official_key_id"],
                    f"anchor class key purity:{entry['atom_graph_class_id']}",
                )
            for component_id in component_ids[1:]:
                requested_anchor_relations += 1
                anchor_rank_reductions += int(
                    anchor_dsu.union(component_ids[0], component_id)
                )
    need(
        requested_anchor_relations == anchor_component_relation_count == 5_568,
        "requested anchor relation census",
    )

    anchor_groups: dict[str, list[str]] = collections.defaultdict(list)
    for component_id in sorted(components266):
        anchor_groups[anchor_dsu.find(component_id)].append(component_id)
    need(
        len(anchor_groups) == 61_152 and anchor_rank_reductions == 2_072,
        "anchor component preview census",
    )
    preview_by_anchor: dict[str, str] = {}
    component_work: list[dict[str, Any]] = []
    for component_ids in anchor_groups.values():
        component_ids.sort()
        descriptors = [
            {
                "Round266_component_id": component_id,
                "Round266_component_row_sha256": components266[component_id][
                    "row_sha256"
                ],
            }
            for component_id in component_ids
        ]
        preview_id = "round280-provisional-component:" + digest(descriptors)
        key_ids = {
            components266[component_id]["official_key_id"]
            for component_id in component_ids
        }
        need(len(key_ids) == 1, f"anchor group key purity:{preview_id}")
        for component_id in component_ids:
            preview_by_anchor[component_id] = preview_id
        component_work.append(
            {
                "provisional_component_id": preview_id,
                "component_preview_classification": (
                    "ROUND266_ANCHOR_COMPONENT_GROUP__ZERO_CREDIT"
                ),
                "official_key_id": next(iter(key_ids)),
                "source_Round266_component_ids": component_ids,
                "source_Round266_component_ids_sha256": digest(component_ids),
                "source_Round266_component_count": len(component_ids),
                "witness_atom_graph_class_ids": [],
                "unanchored_atom_graph_class_ids": [],
                "provisional_new_occurrence_candidate_count": 0,
                "component_union_credit": 0,
                "maximality_credit": 0,
            }
        )

    component_by_id = {
        row["provisional_component_id"]: row for row in component_work
    }
    preview_by_class: dict[str, str] = {}
    unanchored_class_count = 0
    anchored_class_count = 0
    for entry in class_work:
        class_id = entry["atom_graph_class_id"]
        anchors = entry["existing_Round266_component_ids"]
        if anchors:
            anchored_class_count += 1
            preview_id = preview_by_anchor[anchors[0]]
            need(
                all(preview_by_anchor[value] == preview_id for value in anchors),
                f"anchored class post assignment:{class_id}",
            )
            component_by_id[preview_id]["witness_atom_graph_class_ids"].append(
                class_id
            )
        else:
            unanchored_class_count += 1
            descriptors = [
                {
                    "unanchored_atom_graph_class_id": class_id,
                    "canonical_atom_descriptor_sha256": entry[
                        "canonical_atom_descriptor_sha256"
                    ],
                }
            ]
            preview_id = "round280-provisional-component:" + digest(descriptors)
            need(preview_id not in component_by_id, f"unique new preview:{preview_id}")
            row = {
                "provisional_component_id": preview_id,
                "component_preview_classification": (
                    "UNANCHORED_ATOM_GRAPH_CLASS__"
                    "PROVISIONAL_NEW_OCCURRENCE_CANDIDATE__ZERO_CREDIT"
                ),
                "official_key_id": entry["official_key_id"],
                "source_Round266_component_ids": [],
                "source_Round266_component_ids_sha256": digest([]),
                "source_Round266_component_count": 0,
                "witness_atom_graph_class_ids": [],
                "unanchored_atom_graph_class_ids": [class_id],
                "provisional_new_occurrence_candidate_count": 1,
                "component_union_credit": 0,
                "maximality_credit": 0,
            }
            component_work.append(row)
            component_by_id[preview_id] = row
        preview_by_class[class_id] = preview_id
    need(
        anchored_class_count == 16_532 and unanchored_class_count == 75_588,
        "anchored/unanchored atom class census",
    )
    need(
        len(component_work) == 136_740,
        "complete provisional component census",
    )

    for row in component_work:
        row["witness_atom_graph_class_ids"].sort()
        row["witness_atom_graph_class_ids_sha256"] = digest(
            row["witness_atom_graph_class_ids"]
        )
        row["witness_atom_graph_class_count"] = len(
            row["witness_atom_graph_class_ids"]
        )
    component_rows = [closed(row) for row in component_work]
    component_rows.sort(key=lambda row: row["provisional_component_id"])

    class_rows = []
    for entry in class_work:
        output = dict(entry)
        output["provisional_component_id"] = preview_by_class[
            entry["atom_graph_class_id"]
        ]
        output["expanded_occurrence_credit"] = 0
        output["component_union_credit"] = 0
        output["maximality_credit"] = 0
        class_rows.append(closed(output))
    class_rows.sort(key=lambda row: row["atom_graph_class_id"])

    atom_binding_rows = []
    for atom in sorted(atoms, key=lambda row: row["canonical_atom_id"]):
        atom_id = atom["canonical_atom_id"]
        class_id = class_by_atom[atom_id]
        direct_id = direct_occurrence_by_atom.get(atom_id)
        atom_binding_rows.append(
            closed(
                {
                    "atom_binding_row_id": (
                        "round280-atom-binding:" + digest([atom_id])
                    ),
                    "canonical_atom_id": atom_id,
                    "Round279_atom_row_sha256": atom["row_sha256"],
                    "origin_row_id": atom["origin_row_id"],
                    "Round182_occurrence_row_id": atom[
                        "Round182_occurrence_row_id"
                    ],
                    "Round182_leaf_row_id": atom["Round182_leaf_row_id"],
                    "source_signature_row_ids": atom[
                        "source_signature_row_ids"
                    ],
                    "source_signature_row_ids_sha256": digest(
                        atom["source_signature_row_ids"]
                    ),
                    "complete_10_field_return_signature_sha256": atom[
                        "complete_10_field_return_signature_sha256"
                    ],
                    "official_key_id": atom[
                        "complete_10_field_return_signature"
                    ]["official_key_id"],
                    "official_key_ordinal": atom[
                        "complete_10_field_return_signature"
                    ]["official_key_ordinal"],
                    "frozen_true_support_boxes": atom[
                        "frozen_true_support_boxes"
                    ],
                    "frozen_true_support_boxes_sha256": digest(
                        atom["frozen_true_support_boxes"]
                    ),
                    "atom_graph_class_id": class_id,
                    "provisional_component_id": preview_by_class[class_id],
                    "existing_Round208_occurrence_id": direct_id,
                    "new_expanded_occurrence_id": None,
                    "binding_disposition": (
                        "BIND_TO_EXISTING_ROUND208_OCCURRENCE__ZERO_CREDIT"
                        if direct_id is not None
                        else "DEFER_OCCURRENCE_IDENTITY_TO_ATOM_GRAPH_CLASS__"
                        "ZERO_CREDIT"
                    ),
                    "expanded_occurrence_credit": 0,
                    "component_union_credit": 0,
                    "maximality_credit": 0,
                }
            )
        )

    atom_anchor_histogram: collections.Counter[int] = collections.Counter(
        row["existing_Round208_occurrence_count"] for row in class_rows
    )
    component_anchor_histogram: collections.Counter[int] = collections.Counter(
        row["existing_Round266_component_count"] for row in class_rows
    )
    anchored_atom_count = sum(
        row["atom_count"]
        for row in class_rows
        if row["existing_Round208_occurrence_count"] > 0
    )
    unanchored_atom_count = 332_016 - anchored_atom_count
    multiple_occurrence_class_count = sum(
        row["existing_Round208_occurrence_count"] > 1 for row in class_rows
    )
    multiple_component_class_count = sum(
        row["existing_Round266_component_count"] > 1 for row in class_rows
    )
    unanchored_atom_count_histogram: collections.Counter[int] = (
        collections.Counter(
            row["atom_count"]
            for row in class_rows
            if row["existing_Round208_occurrence_count"] == 0
        )
    )
    anchored_occurrence_component_joint_histogram: collections.Counter[
        tuple[int, int]
    ] = collections.Counter(
        (
            row["existing_Round208_occurrence_count"],
            row["existing_Round266_component_count"],
        )
        for row in class_rows
        if row["existing_Round208_occurrence_count"] > 0
    )
    max_class_atom_count = max(row["atom_count"] for row in class_rows)
    max_class_occurrence_count = max(
        row["existing_Round208_occurrence_count"] for row in class_rows
    )
    max_class_component_count = max(
        row["existing_Round266_component_count"] for row in class_rows
    )

    # Per-key conservation summary.
    per_key: dict[str, dict[str, int]] = collections.defaultdict(
        lambda: collections.Counter()
    )
    for atom in atoms:
        key_id = atom["complete_10_field_return_signature"]["official_key_id"]
        per_key[key_id]["atom_count"] += 1
        per_key[key_id]["existing_Round208_atom_count"] += int(
            bool(atom["existing_Round208_occurrence_row_ids"])
        )
    for row in class_rows:
        key = row["official_key_id"]
        per_key[key]["atom_graph_class_count"] += 1
        per_key[key]["anchored_atom_graph_class_count"] += int(
            row["existing_Round208_occurrence_count"] > 0
        )
        per_key[key]["unanchored_atom_graph_class_count"] += int(
            row["existing_Round208_occurrence_count"] == 0
        )
    for component in components266.values():
        per_key[component["official_key_id"]][
            "pre_Round280_anchor_component_count"
        ] += 1
    for row in component_rows:
        per_key[row["official_key_id"]][
            "provisional_component_count_without_seams"
        ] += 1
        per_key[row["official_key_id"]][
            "post_local_glue_anchor_component_group_count"
        ] += int(row["source_Round266_component_count"] > 0)
        per_key[row["official_key_id"]][
            "provisional_new_occurrence_candidate_class_count"
        ] += row["provisional_new_occurrence_candidate_count"]
    # The collar atom universe occupies 108 of the 116 frozen exact keys.
    # The other eight keys remain present through the Round266 component
    # anchors and must be conserved unchanged in this preview.
    need(
        len(keys_seen) == 108 and len(per_key) == 116,
        "108 collar keys inside complete 116-key preview",
    )
    per_key_rows = [
        {"official_key_id": key_id, **dict(sorted(counts.items()))}
        for key_id, counts in sorted(per_key.items())
    ]
    need(
        sum(
            row["provisional_component_count_without_seams"]
            for row in per_key_rows
        )
        == 136_740,
        "per-key provisional quotient conservation",
    )

    def ledger(
        rows: list[dict[str, Any]], row_id_field: str, schema: str, status: str
    ) -> dict[str, Any]:
        return {
            "schema": schema,
            "status": status,
            "row_count": len(rows),
            "rows_sha256": digest(rows),
            "row_ids_sha256": digest([row[row_id_field] for row in rows]),
            "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
            "rows": rows,
            "strict_nonpromotion": {
                "expanded_occurrence_credit": 0,
                "component_union_credit": 0,
                "maximality_credit": 0,
            },
        }

    status_prefix = (
        "PASS_PRELIMINARY_ROUND280_SCHEMA_AND_DSU_PREVIEW__"
        if readiness["preliminary_override_used"]
        else "PASS_ROUND280_ZERO_CREDIT_SCHEMA_AND_DSU_PREVIEW__"
    )
    atom_binding_payload = ledger(
        atom_binding_rows,
        "atom_binding_row_id",
        "cm2.round280.atom-to-class-binding-preview.v1",
        status_prefix + "ATOM_BINDINGS",
    )
    class_payload = ledger(
        class_rows,
        "atom_graph_class_id",
        "cm2.round280.connected-atom-graph-class-preview.v1",
        status_prefix + "ATOM_CLASSES",
    )
    component_payload = ledger(
        component_rows,
        "provisional_component_id",
        "cm2.round280.component-dsu-preview-without-seams.v1",
        status_prefix + "COMPONENTS",
    )

    result = {
        "schema": "cm2.round280.source-g-occurrence-and-dsu-preview-probe.v1",
        "status": status_prefix.rstrip("_"),
        "round279_readiness": readiness,
        "semantic_correction": {
            "canonical_atoms_are_not_automatically_expanded_occurrences": True,
            "atom_graph_quotient_precedes_occurrence_identity_assignment": True,
            "unanchored_connected_atom_classes_are_only_provisional_new_occurrence_candidates": True,
            "multiple_existing_occurrence_ids_in_one_atom_class_are_not_automatically_collapsed": True,
            "component_union_evidence_is_distinct_from_occurrence_identity": True,
        },
        "census": {
            "Round279_canonical_atom_count": 332_016,
            "Round279_common_face_edge_count": 330_724,
            "Round279_distinct_atom_endpoint_pair_count": len(
                distinct_atom_edge_pairs
            ),
            "Round279_new_atom_candidate_count": 295_976,
            "Round208_existing_occurrence_backed_atom_count": 36_040,
            "strict_true_support_subbox_atom_count": 4,
            "atom_graph_rank_reduction_count": edge_rank_reductions,
            "atom_graph_redundant_edge_count": 330_724
            - edge_rank_reductions,
            "connected_atom_graph_class_count": len(class_rows),
            "anchored_atom_graph_class_count": anchored_class_count,
            "unanchored_atom_graph_class_count": unanchored_class_count,
            "unanchored_singleton_atom_graph_class_count": (
                unanchored_atom_count_histogram[1]
            ),
            "unanchored_nontrivial_atom_graph_class_count": (
                unanchored_class_count - unanchored_atom_count_histogram[1]
            ),
            "anchored_atom_count": anchored_atom_count,
            "unanchored_atom_count": unanchored_atom_count,
            "single_existing_occurrence_anchored_class_count": atom_anchor_histogram[
                1
            ],
            "multiple_existing_occurrence_anchored_class_count": multiple_occurrence_class_count,
            "multiple_Round266_component_anchored_class_count": multiple_component_class_count,
            "maximum_atom_count_in_one_atom_graph_class": max_class_atom_count,
            "maximum_existing_occurrence_count_in_one_atom_graph_class": max_class_occurrence_count,
            "maximum_Round266_component_count_in_one_atom_graph_class": max_class_component_count,
            "pre_preview_Round266_anchor_component_count": 63_224,
            "requested_anchor_component_relation_count": requested_anchor_relations,
            "preview_anchor_component_rank_reduction_count": anchor_rank_reductions,
            "post_local_glue_anchor_component_group_count": len(anchor_groups),
            "provisional_new_occurrence_candidate_class_count": unanchored_class_count,
            "provisional_component_count_without_Round268_seams": len(
                component_rows
            ),
            "formal_new_expanded_occurrence_count": 0,
            "formal_component_union_credit": 0,
            "formal_maximality_credit": 0,
            "collar_atom_exact_key_count": len(keys_seen),
            "complete_Round266_exact_key_count": 116,
        },
        "class_anchor_occurrence_count_histogram": {
            str(key): value for key, value in sorted(atom_anchor_histogram.items())
        },
        "class_anchor_component_count_histogram": {
            str(key): value
            for key, value in sorted(component_anchor_histogram.items())
        },
        "unanchored_class_atom_count_histogram": {
            str(key): value
            for key, value in sorted(unanchored_atom_count_histogram.items())
        },
        "anchored_class_occurrence_component_joint_histogram": {
            f"{occurrence_count}|{component_count}": value
            for (
                occurrence_count,
                component_count,
            ), value in sorted(
                anchored_occurrence_component_joint_histogram.items()
            )
        },
        "exact_support_coordinate_volume_sum_over_atoms": str(
            total_support_volume
        ),
        "per_exact_key_preview": per_key_rows,
        "attachments": {
            "atom_binding_ledger": {
                key: atom_binding_payload[key]
                for key in (
                    "row_count",
                    "rows_sha256",
                    "row_ids_sha256",
                    "row_hashes_sha256",
                )
            },
            "atom_graph_class_ledger": {
                key: class_payload[key]
                for key in (
                    "row_count",
                    "rows_sha256",
                    "row_ids_sha256",
                    "row_hashes_sha256",
                )
            },
            "provisional_component_ledger": {
                key: component_payload[key]
                for key in (
                    "row_count",
                    "rows_sha256",
                    "row_ids_sha256",
                    "row_hashes_sha256",
                )
            },
        },
        "excluded_from_preview": {
            "Round268_true_seam_patch_count": 152,
            "Round268_true_seam_edges_applied": 0,
            "Jx_Jy_same_point_edges_applied": 0,
            "lower_stratum_occurrence_promotions": 0,
        },
        "minimal_sufficient_conditions_before_occurrence_promotion": [
            "Round279 producer, atoms, edges, and full dynamic independent verifier must be hash-frozen and mutually pinned",
            "expanded-occurrence identity must be defined as a connected component of the certified positive-open support graph, not as one row per atom",
            "the complete admissible adjacency universe must include the reverse-rechart and 152 true-seam channels before final cross-chart occurrence identity is assigned",
            "every unanchored atom class must remain nonempty positive-open and exact-key pure after the final seam quotient",
            "multiply anchored classes require an explicit policy proving whether existing occurrence IDs are fragments of one occurrence or merely component-connected distinct occurrences",
            "lower-stratum provenance must not be promoted without independent physical-existence disposition",
        ],
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_union_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "maximality_credit": 0,
            "exact_key_fibre_credit": 0,
            "global_disposition_credit": 0,
            "Jx_Jy_same_point_glue_credit": 0,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return result, atom_binding_payload, class_payload, component_payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-preliminary-round279",
        action="store_true",
        help="debug only: consume an explicitly unfrozen Round279 snapshot",
    )
    parser.add_argument("--result", type=Path, default=RESULT)
    parser.add_argument("--atom-bindings", type=Path, default=ATOM_BINDINGS)
    parser.add_argument("--atom-classes", type=Path, default=ATOM_CLASSES)
    parser.add_argument("--components", type=Path, default=COMPONENTS)
    args = parser.parse_args()

    occurrences266, components266, _result266 = load_round266()
    atoms, edges, _result279, readiness = load_round279(
        args.allow_preliminary_round279
    )
    result, atom_bindings, atom_classes, components = build(
        atoms,
        edges,
        occurrences266,
        components266,
        readiness,
    )
    binding_bytes = gzip_payload(atom_bindings)
    class_bytes = gzip_payload(atom_classes)
    component_bytes = gzip_payload(components)
    result["attachments"]["atom_binding_ledger"]["file_sha256"] = (
        hashlib.sha256(binding_bytes).hexdigest()
    )
    result["attachments"]["atom_graph_class_ledger"]["file_sha256"] = (
        hashlib.sha256(class_bytes).hexdigest()
    )
    result["attachments"]["provisional_component_ledger"]["file_sha256"] = (
        hashlib.sha256(component_bytes).hexdigest()
    )
    result["provenance"] = {
        "Round266_certificate_sha256": file_sha256(ROUND266_CERTIFICATE),
        "Round266_verification_sha256": file_sha256(ROUND266_VERIFICATION),
        "Round279_certificate_sha256": readiness["certificate_sha256"],
        "Round279_atom_ledger_sha256": readiness["atom_ledger_sha256"],
        "Round279_edge_ledger_sha256": readiness["edge_ledger_sha256"],
        "Round279_verification_sha256": readiness["verification_sha256"],
        "producer_sha256": file_sha256(Path(__file__).resolve()),
    }
    result_document = {
        "result": result,
        "result_sha256": digest(result),
    }
    atomic_write(args.atom_bindings.resolve(), binding_bytes)
    atomic_write(args.atom_classes.resolve(), class_bytes)
    atomic_write(args.components.resolve(), component_bytes)
    atomic_write(
        args.result.resolve(),
        json.dumps(result_document, indent=2, sort_keys=True).encode() + b"\n",
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "result_sha256": result_document["result_sha256"],
                **result["census"],
                "round279_readiness": readiness,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
