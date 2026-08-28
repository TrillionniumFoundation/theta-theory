#!/usr/bin/env python3
"""Fail-closed census for the Round273 signature/frontier binding gate.

This probe deliberately awards no mathematical credit.  It answers the first
question a formal Round273 producer must settle: which frozen local signature
rows are already named expanded occurrences, and how ambiguous is a lookup by
the complete ten-field return signature alone?
"""
from __future__ import annotations

import collections
import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def canonical(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def result(name: str) -> dict:
    doc = json.loads((HERE / name).read_bytes())
    assert doc["result_sha256"] == digest(doc["result"]), name
    return doc["result"]


def unpack(data: dict, table: str) -> list[dict]:
    rows = data[table]
    columns = data["row_column_schemas"][table]
    expected = data["table_census_and_sha256"][table]
    assert len(rows) == expected["row_count"] and digest(rows) == expected["rows_sha256"]
    return [dict(zip(columns, row, strict=True)) for row in rows]


def root_in_t_interval(box: list[str], root: str) -> bool:
    lo, hi = Fraction(box[0]), Fraction(box[1])
    if root == "+":
        return 0 <= lo < hi and 2 * lo * lo <= 1 <= 2 * hi * hi
    return lo < hi <= 0 and 2 * hi * hi <= 1 <= 2 * lo * lo


def positive_overlap(a0: Fraction, a1: Fraction, b0: Fraction, b1: Fraction) -> bool:
    return max(a0, b0) < min(a1, b1)


def main() -> int:
    r266 = result("cm2_round266_source_g_expanded_curved_face_closure_certificate.json")
    occurrences = r266["formal_post_Round266_expanded_occurrence_frontier_ledger"]["rows"]
    assert len(occurrences) == 126_468

    by_local_id: dict[str, dict] = {}
    components_by_signature: dict[str, set[str]] = collections.defaultdict(set)
    occurrences_by_signature: collections.Counter[str] = collections.Counter()
    components_by_key: dict[str, set[str]] = collections.defaultdict(set)
    frozen_component_ids: set[str] = set()
    for row in occurrences:
        local_id = row["local_occurrence_row_id"]
        assert local_id not in by_local_id
        by_local_id[local_id] = row
        signature_hash = row["complete_10_field_return_signature_sha256"]
        component_id = row["post_Round266_quotient_component_id"]
        frozen_component_ids.add(component_id)
        components_by_signature[signature_hash].add(component_id)
        occurrences_by_signature[signature_hash] += 1
        components_by_key[row["official_key_id"]].add(component_id)
    del r266, occurrences

    sources = (
        (
            208,
            "cm2_round208_source_g_outgoing_direct_signature_materialization_certificate.json",
            "formal_local_open_3D_signature_ledger",
            "region_row_id",
        ),
        (
            269,
            "cm2_round269_source_g_closed_collar_direct_signature_materialization_certificate.json",
            "formal_direct_side_signature_ledger",
            "signed_region_row_id",
        ),
        (
            270,
            "cm2_round270_source_g_outgoing_g_factor_signature_materialization_certificate.json",
            "formal_direct_side_signature_ledger",
            "signed_region_row_id",
        ),
        (
            271,
            "cm2_round271_source_g_wall_and_outgoing_tail_signature_materialization_certificate.json",
            "formal_side_signature_ledger",
            "signed_region_row_id",
        ),
        (
            272,
            "cm2_round272_source_g_boundary_dual_factor_wall_closure_certificate.json",
            "formal_side_signature_ledger",
            "signed_region_row_id",
        ),
    )

    total = collections.Counter()
    round_rows = []
    signed_region_refs: list[dict] = []
    global_ids: set[str] = set()
    for round_number, filename, ledger_name, id_field in sources:
        data = result(filename)
        rows = data[ledger_name]["rows"]
        census = collections.Counter()
        component_multiplicity = collections.Counter()
        occurrence_multiplicity = collections.Counter()
        key_component_multiplicity = collections.Counter()
        for row in rows:
            row_id = row[id_field]
            assert row_id not in global_ids
            global_ids.add(row_id)
            signature = row["local_return_signature"]
            signature_hash = row.get(
                "complete_10_field_return_signature_sha256", digest(signature)
            )
            assert signature_hash == digest(signature)
            key_id = signature["official_key_id"]

            direct_id = row.get("region_row_id", row_id)
            direct = by_local_id.get(direct_id)
            if direct is not None:
                assert direct["complete_10_field_return_signature_sha256"] == signature_hash
                assert direct["official_key_id"] == key_id
                census["direct_expanded_occurrence_id_match"] += 1
            else:
                census["not_directly_named_in_expanded_frontier"] += 1

            sig_component_count = len(components_by_signature.get(signature_hash, ()))
            sig_occurrence_count = occurrences_by_signature.get(signature_hash, 0)
            key_component_count = len(components_by_key.get(key_id, ()))
            component_multiplicity[sig_component_count] += 1
            occurrence_multiplicity[sig_occurrence_count] += 1
            key_component_multiplicity[key_component_count] += 1
            if sig_component_count == 1:
                census["unique_existing_component_by_signature_only"] += 1
            elif sig_component_count == 0:
                census["no_existing_component_by_signature_only"] += 1
            else:
                census["ambiguous_existing_components_by_signature_only"] += 1
            leaf_id = row.get("Round182_leaf_row_id", row.get("leaf_row_id"))
            assert leaf_id is not None
            signed_region_refs.append({
                "round": round_number,
                "row_id": row_id,
                "leaf_id": leaf_id,
                "signature_hash": signature_hash,
                "key_id": key_id,
            })

        row_summary = {
            "round": round_number,
            "signature_row_count": len(rows),
            "binding_census": dict(sorted(census.items())),
            "existing_component_count_by_signature_histogram": dict(
                sorted(component_multiplicity.items())
            ),
            "existing_occurrence_count_by_signature_histogram": dict(
                sorted(occurrence_multiplicity.items())
            ),
            "existing_component_count_by_exact_key_histogram": dict(
                sorted(key_component_multiplicity.items())
            ),
        }
        round_rows.append(row_summary)
        total["signature_rows"] += len(rows)
        total["direct_expanded_occurrence_id_matches"] += census[
            "direct_expanded_occurrence_id_match"
        ]
        total["unique_existing_component_by_signature_only"] += census[
            "unique_existing_component_by_signature_only"
        ]
        total["ambiguous_existing_components_by_signature_only"] += census[
            "ambiguous_existing_components_by_signature_only"
        ]
        total["no_existing_component_by_signature_only"] += census[
            "no_existing_component_by_signature_only"
        ]
        del data, rows

    assert total["signature_rows"] == 332_020

    r182 = result("cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json")
    collar_occurrences = unpack(r182, "collar_occurrence_rows")
    collar_leaves = unpack(r182, "collar_leaf_rows")
    seam_rows = unpack(r182, "source_chart_seam_owner_rows")
    collar_by_occurrence = {row["Round179_occurrence_row_id"]: row for row in collar_occurrences}
    assert len(collar_by_occurrence) == len(collar_occurrences)
    leaf_by_id = {row["row_id"]: row for row in collar_leaves}
    assert len(leaf_by_id) == len(collar_leaves) == 202_840
    refs_by_leaf: dict[str, list[dict]] = collections.defaultdict(list)
    refs_by_origin: dict[str, list[dict]] = collections.defaultdict(list)
    for ref in signed_region_refs:
        leaf = leaf_by_id[ref["leaf_id"]]
        collar = collar_by_occurrence[leaf["occurrence_row_id"]]
        assert leaf["retained_child_row_id"] is not None
        ref["origin_id"] = collar["origin_row_id"]
        ref["chart"] = collar["chart"]
        ref["box"] = leaf["box"]
        refs_by_leaf[ref["leaf_id"]].append(ref)
        refs_by_origin[ref["origin_id"]].append(ref)
    leaf_signature_multiplicity = collections.Counter(
        len(refs_by_leaf.get(leaf_id, ())) for leaf_id in leaf_by_id
    )
    uncovered_leaf_ids = set(leaf_by_id) - set(refs_by_leaf)
    assert len(uncovered_leaf_ids) == 64

    # The 64 rows absent from R208 are not orphans: they are the unique
    # RESIDUAL_3D leaf in each of Round204's 64 locally completed origins.
    r204 = result("cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json")
    completion_rows = r204["origin_local_completion_ledger"]["rows"]
    region204 = r204["formal_local_open_3D_region_ledger"]["rows"]
    completed_leaf_ids = {
        leaf_id
        for row in completion_rows
        for leaf_id in row["Round182_leaf_row_ids"]
    }
    assert uncovered_leaf_ids <= completed_leaf_ids
    assert all(leaf_by_id[leaf_id]["graph_classification"] == "RESIDUAL_3D" for leaf_id in uncovered_leaf_ids)
    round204_regions_on_uncovered = [
        row for row in region204 if row["leaf_row_id"] in uncovered_leaf_ids
    ]
    assert len(round204_regions_on_uncovered) > len(uncovered_leaf_ids)
    for row in round204_regions_on_uncovered:
        direct = by_local_id[row["region_row_id"]]
        assert direct["official_key_id"] == row["official_key_id"]
        ref = {
            "round": 204,
            "row_id": row["region_row_id"],
            "leaf_id": row["leaf_row_id"],
            "signature_hash": direct["complete_10_field_return_signature_sha256"],
            "key_id": row["official_key_id"],
            "origin_id": row["origin_row_id"],
            "chart": row["chart"],
            "box": row["leaf_exact_box"],
        }
        refs_by_origin[ref["origin_id"]].append(ref)

    seam_by_id = {row["row_id"]: row for row in seam_rows}
    r268 = result("cm2_round268_source_g_true_seam_candidate_geometry_exhaustion_certificate.json")
    patches = r268["formal_true_source_seam_positive_patch_ledger"]["rows"]
    assert len(patches) == 152
    incident_candidate_histogram: collections.Counter[str] = collections.Counter()
    patch_candidate_rows: list[dict] = []
    for patch in patches:
        counts = []
        keys = []
        for side in ("left", "right"):
            seam = seam_by_id[patch[f"{side}_Round182_source_seam_row_id"]]
            root = patch[f"{side}_local_t_root"]
            p0, p1 = map(Fraction, patch["exact_common_p_interval"])
            s0, s1 = map(Fraction, patch["exact_common_s_interval"])
            candidates = []
            for ref in refs_by_origin[seam["origin_row_id"]]:
                box = ref["box"]
                if (
                    ref["chart"] == patch[f"{side}_chart"]
                    and root_in_t_interval(box, root)
                    and positive_overlap(Fraction(box[2]), Fraction(box[3]), p0, p1)
                    and positive_overlap(Fraction(box[4]), Fraction(box[5]), s0, s1)
                ):
                    candidates.append(ref)
            counts.append(len(candidates))
            keys.append(sorted({ref["key_id"] for ref in candidates}))
        incident_candidate_histogram[f"{counts[0]}|{counts[1]}"] += 1
        patch_candidate_rows.append({
            "patch_id": patch["true_seam_patch_row_id"],
            "left_geometric_signed_region_candidate_count": counts[0],
            "right_geometric_signed_region_candidate_count": counts[1],
            "left_candidate_exact_key_count": len(keys[0]),
            "right_candidate_exact_key_count": len(keys[1]),
            "common_candidate_exact_key_count": len(set(keys[0]) & set(keys[1])),
        })
    del r182, r268
    output = {
        "status": "FAIL_CLOSED_ROUND273_BINDING_PROBE__NO_CREDIT",
        "frozen_frontier": {
            "expanded_occurrence_count": len(by_local_id),
            "total_component_count": 63_224,
            "component_count_with_expanded_occurrence_member": len(frozen_component_ids),
            "exact_key_count": len(components_by_key),
        },
        "round_census": round_rows,
        "total_census": dict(sorted(total.items())),
        "complete_Round182_leaf_binding_census": {
            "collar_occurrence_count": len(collar_occurrences),
            "collar_leaf_count": len(leaf_by_id),
            "signed_parent_leaf_count": len(refs_by_leaf),
            "signature_count_by_parent_leaf_histogram": dict(
                sorted(leaf_signature_multiplicity.items())
            ),
            "Round204_preexpanded_residual_leaf_count": len(uncovered_leaf_ids),
            "Round204_preexpanded_region_count_on_those_leaves": len(round204_regions_on_uncovered),
            "orphan_leaf_count_after_Round204_reconciliation": 0,
        },
        "true_seam_prebinding_census": {
            "patch_count": len(patches),
            "geometric_signed_region_candidate_count_left_pipe_right_histogram": dict(
                sorted(incident_candidate_histogram.items())
            ),
            "patch_rows": patch_candidate_rows,
            "component_edge_credit": 0,
        },
        "conclusion": {
            "signature_hash_is_not_accepted_as_a_physical_binding": True,
            "direct_provenance_binding_is_required": True,
            "geometric_region_to_frontier_attachment_is_required_for_non_Round208_rows": True,
            "component_or_maximality_credit": 0,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
