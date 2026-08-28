#!/usr/bin/env python3
"""Read-only whole-region direct return-signature feasibility probe.

For every strict Round195 outgoing-W candidate region, this spike recomputes
the unique first target from the complete retained target list, certifies
wall crossings and their strict order on the containing leaf enclosure,
derives the outgoing chart from the region's strict HPLUS/HMINUS signs, and
rebuilds the canonical Gate5 exact key.

No Round174/Round179 resolved signature anchor, parent-wide signature base,
Round198 adjacency assignment, or Round203 component propagation is used as
an input. Probe only: no formal attachment and zero global disposition.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import gc
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from flint import ctx

import cm2_round203_source_g_outgoing_signature_component_probe as r203


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round207.source-g-whole-region-direct-signature-probe.v1"

ROUND203_SOURCE = (
    "cm2_round203_source_g_outgoing_signature_component_probe.py"
)
ROUND203_SOURCE_SHA256 = (
    "86214ed1d37400cdde787c915b4467c7d081e018a7c7522470bdcb5d1abc351f"
)
ROUND203_REPORT = (
    "cm2_round203_source_g_outgoing_signature_component_spike_report.md"
)
ROUND203_REPORT_SHA256 = (
    "4a9cffcb920d45a27d91cf9accb723bfcbea443ede981e7c2433949ba5981721"
)

EXPECTED_LEAVES = 18_324
EXPECTED_CANDIDATES = 36_040
EXPECTED_ORIGINS = 8_268
EXPECTED_PARENTS = 912
EXPECTED_U2_LEAVES = 88
EXPECTED_U2_CANDIDATES = 176
ROUND203_DIRECT_ASSIGNED = 3_264
ROUND203_RESIDUAL = 32_776
EXPECTED_R195_LEAF_ROWS_SHA256 = (
    "0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5"
)
EXPECTED_R195_U2_ROWS_SHA256 = (
    "12fbc70f82645ae2ad252b4e88587a7841814a03fda1972a0241cd63c45d6ee0"
)
EXPECTED_DIRECT_LEAF_ROWS_SHA256 = (
    "4d541ea5bfc4b9db30e78f994e36177dee7112b4c4057c71d6d6376650e20e9e"
)
EXPECTED_ASSIGNMENT_ROWS_SHA256 = (
    "e46fc7e35f2728e48a81e47cd0266cf25c07ad63e534a9fd5b57cc8b0007bb72"
)
EXPECTED_U2_ASSIGNMENT_ROWS_SHA256 = (
    "de20109df8b913a12627b42340ccdacb88e633a5c96cd56bcdd8bafe410fee53"
)
EXPECTED_PROBE_RESULT_SHA256 = (
    "d49b3c9cef0738a03bca8f6477121c7b27aa63e3be8b9ac5854c2521f97448ce"
)
EXPECTED_DOCUMENT_SHA256 = (
    "21b388fbd147219f5f52fbdcbe8528b7b9afc06590f2bb997e70042a759f5277"
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def check_inputs() -> dict[str, Any]:
    r189 = r203.r198.r195.r191.r189
    require(
        Path(r203.__file__).resolve() == (HERE / ROUND203_SOURCE).resolve(),
        "Round203 module identity",
    )
    r189.pinned_sha256(HERE / ROUND203_SOURCE, ROUND203_SOURCE_SHA256)
    r189.pinned_sha256(HERE / ROUND203_REPORT, ROUND203_REPORT_SHA256)
    require(
        r203.EXPECTED_PROBE_RESULT_SHA256
        == "8addc49f7e1c2661fa82525f59765627f7a2cbb322a0b3b55d4ca5c6a04341d9"
        and r203.EXPECTED_DOCUMENT_SHA256
        == "7c4e34d146adb5f34637bed6eeae19719bdd477c47c235a9e57384f950f63e48",
        "Round203 embedded final result pins",
    )
    upstream = r203.check_inputs()
    return {
        **upstream,
        "Round203_probe_source_sha256": ROUND203_SOURCE_SHA256,
        "Round203_probe_report_sha256": ROUND203_REPORT_SHA256,
        "Round203_probe_result_sha256":
            r203.EXPECTED_PROBE_RESULT_SHA256,
        "Round203_probe_document_sha256":
            r203.EXPECTED_DOCUMENT_SHA256,
        "probe_only_import_before_pin_boundary": True,
    }


def direct_leaf_signature_base(
    chart: str,
    box: Any,
    registry: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[str]]:
    """Directly rebuild every signature field except the region cell."""

    r174v = r203.r198.r195.r191.r189.r188.r186.r179.r174
    chart_class = r174v.rational_chart_class(box)
    if chart_class != "inside":
        return None, ["whole_leaf_not_strictly_inside_source_chart"]
    direct_leaf = r174v.atlas.classify_box(chart, box)
    if (
        direct_leaf.classification != "unique_first"
        or direct_leaf.owner_target is None
        or direct_leaf.active_targets
        != (direct_leaf.owner_target,)
    ):
        return None, [
            "complete_candidate_list_not_unique_first:"
            + direct_leaf.classification
        ]
    target = direct_leaf.owner_target
    complete_candidates = r174v.first_hit.candidate_ids(chart)
    if target not in complete_candidates:
        return None, ["direct_target_not_in_complete_candidate_list"]

    qx, qy, ux, uy, s, _source_cosine = r174v.atlas.geometry(
        chart,
        box,
    )
    record = r174v.atlas.root_record(chart, box, target)
    reasons: list[str] = []
    if (
        record.classification != "strict_future_root"
        or record.near is None
        or not bool(record.discriminant > 0)
    ):
        reasons.append("direct_selected_root_not_strict_future")
    elif not bool(record.near < r174v.first_hit.arbq(Q(3))):
        reasons.append("direct_return_time_not_below_three")
    if reasons:
        return None, reasons

    radical = record.discriminant.sqrt()
    radius = r174v.first_hit.arbq(
        r174v.first_hit.RADIUS[target[0]]
    )
    normal_x = (
        -radical * ux + record.transverse * uy
    ) / radius
    normal_y = (
        -radical * uy - record.transverse * ux
    ) / radius
    target_object = r174v.first_hit.target_by_id(target)
    center_x, center_y = r174v.first_hit.target_center(
        target_object,
        s,
    )
    hit_x = center_x + radius * normal_x
    hit_y = center_y + radius * normal_y
    x_events, x_reasons = r174v.crossing_events(qx, hit_x, "X")
    y_events, y_reasons = r174v.crossing_events(qy, hit_y, "Y")
    reasons.extend(x_reasons)
    reasons.extend(y_reasons)
    ordered = None
    if x_events is not None and y_events is not None:
        ordered, order_reasons = r174v.order_events(
            x_events + y_events
        )
        reasons.extend(order_reasons)
    if reasons:
        return None, sorted(set(reasons))
    assert ordered is not None
    pattern = tuple(event[0] for event in ordered)
    require(
        len(pattern) <= 8
        and sum(token.startswith("X") for token in pattern) <= 4
        and sum(token.startswith("Y") for token in pattern) <= 4,
        "direct strict wall grammar",
    )
    key = r174v.exact_key(chart, target, pattern, registry)
    whole_box_outgoing, whole_box_outgoing_reasons = (
        r174v.outgoing_cell(normal_x, normal_y)
    )
    return {
        "source_chart": chart,
        "target_lift": target,
        "ordered_integer_wall_events": ordered,
        "signed_wall_word": list(pattern),
        "roof": len(pattern) + 1,
        "official_key_row": key["row"],
        "official_key_ordinal": key["ordinal"],
        "official_key_id": key["identifier"],
        "complete_retained_target_count": len(complete_candidates),
        "whole_leaf_source_chart_classification":
            "STRICTLY_INSIDE_TRUE_SOURCE_CHART",
        "complete_candidate_list_unique_first": True,
        "selected_root_strict_future_nongrazing_below_three": True,
        "wall_endpoints_and_crossing_counts_strict_on_leaf_enclosure":
            True,
        "wall_event_order_strict_on_leaf_enclosure": True,
        "whole_leaf_box_outgoing_cell": whole_box_outgoing,
        "whole_leaf_box_outgoing_reasons":
            whole_box_outgoing_reasons,
    }, []


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only Round207 direct whole-region return-signature "
            "feasibility probe; no output path and zero global credit."
        )
    )
    parser.parse_args()
    ctx.prec = 256
    pins = check_inputs()

    r198 = r203.r198
    r195 = r198.r195
    r186 = r195.r191.r189.r188.r186
    r174v = r186.r179.r174
    frozen = r174v.load_frozen_inputs()
    registry = r174v.rebuild_registry(frozen["gate5"])
    del frozen
    gc.collect()

    outgoing, collar_by_occurrence, source = (
        r195.r191.r189.load_scope()
    )
    del source
    gc.collect()
    require(len(outgoing) == EXPECTED_LEAVES, "outgoing leaf census")

    leaf_rows: list[dict[str, Any]] = []
    u2_audit_rows: list[dict[str, Any]] = []
    u2_leaf_ids: set[str] = set()
    direct_leaf_rows: list[dict[str, Any]] = []
    assignment_rows: list[dict[str, Any]] = []
    for index, raw in enumerate(outgoing, 1):
        collar = collar_by_occurrence[raw["occurrence_row_id"]]
        box = r186.r179.r174.atlas.AtlasBox(
            *(Q(value) for value in raw["box"]),
            0,
            raw["row_id"],
        )
        final_faces: dict[str, dict[str, Any]] = {}
        for side, upper, encoded in (
            ("LOWER", False, raw["lower_t_face_status"]),
            ("UPPER", True, raw["upper_t_face_status"]),
        ):
            if encoded == "U":
                final_faces[side] = r195.final_unresolved_face(
                    raw,
                    collar,
                    box,
                    side,
                    upper,
                )
        lower = (
            r195.side_summary(final_faces["LOWER"])
            if "LOWER" in final_faces
            else r195.decode_round182_face(raw["lower_t_face_status"])
        )
        upper = (
            r195.side_summary(final_faces["UPPER"])
            if "UPPER" in final_faces
            else r195.decode_round182_face(raw["upper_t_face_status"])
        )
        leaf = r195.classify_leaf(raw, collar, box, lower, upper)
        leaf_rows.append(leaf)
        is_u2 = (
            raw["lower_t_face_status"] == "U"
            and raw["upper_t_face_status"] == "U"
        )
        if is_u2:
            u2_leaf_ids.add(raw["row_id"])
            u2_audit_rows.append(r195.audit_u2_leaf(
                leaf,
                raw,
                collar,
                box,
                final_faces["LOWER"],
                final_faces["UPPER"],
            ))

        candidate_regions = r198.factor_region_rows(
            leaf,
            raw,
            collar,
            box,
            list(final_faces.values()),
            None,
            set(),
            {},
            None,
        )
        base, reasons = direct_leaf_signature_base(
            collar["chart"],
            box,
            registry,
        )
        target_matches_frozen_collar = (
            base is not None
            and base["target_lift"] == collar["owner_target"]
        )
        direct_leaf_rows.append({
            "leaf_row_id": leaf["leaf_row_id"],
            "origin_row_id": leaf["origin_row_id"],
            "parent_id": collar["parent_id"],
            "chart": collar["chart"],
            "box": raw["box"],
            "candidate_region_count": len(candidate_regions),
            "direct_base_status": (
                "DIRECT_WHOLE_LEAF_BASE_CERTIFIED"
                if base is not None and target_matches_frozen_collar
                else "DIRECT_WHOLE_LEAF_BASE_RESIDUAL"
            ),
            "direct_failure_reasons": reasons,
            "direct_target_lift":
                None if base is None else base["target_lift"],
            "frozen_collar_owner_target_for_posthoc_comparison":
                collar["owner_target"],
            "direct_target_matches_frozen_collar":
                target_matches_frozen_collar,
            "frozen_owner_used_as_direct_target_selection_input": False,
            "direct_signature_base": base,
        })

        for region in candidate_regions:
            signature = None
            status = "DIRECT_WHOLE_REGION_SIGNATURE_RESIDUAL"
            region_reasons = list(reasons)
            if base is not None and target_matches_frozen_collar:
                cell = region["outgoing_cell"]
                require(
                    (region["HPLUS_sign"], region["HMINUS_sign"])
                    == r203.CELL_SIGNS[cell],
                    f"region cell sign pair:{region['candidate_region_id']}",
                )
                target_chart = (
                    f"{base['target_lift'].split('[', 1)[0]}:{cell}"
                )
                signature = {
                    "source_chart": base["source_chart"],
                    "target_lift": base["target_lift"],
                    "ordered_integer_wall_events":
                        base["ordered_integer_wall_events"],
                    "signed_wall_word": base["signed_wall_word"],
                    "roof": base["roof"],
                    "outgoing_cell": cell,
                    "target_chart": target_chart,
                    "official_key_row": base["official_key_row"],
                    "official_key_ordinal":
                        base["official_key_ordinal"],
                    "official_key_id": base["official_key_id"],
                }
                require(
                    signature["official_key_row"]
                    == [
                        signature["source_chart"],
                        signature["target_lift"],
                        signature["signed_wall_word"],
                        signature["roof"],
                    ]
                    and signature["target_chart"]
                    == (
                        signature["target_lift"].split("[", 1)[0]
                        + ":"
                        + signature["outgoing_cell"]
                    ),
                    f"whole-region canonical signature:"
                    f"{region['candidate_region_id']}",
                )
                status = "DIRECT_WHOLE_REGION_SIGNATURE_CERTIFIED"
            elif base is not None:
                region_reasons.append(
                    "direct_target_conflicts_with_frozen_collar"
                )
            assignment_rows.append({
                "candidate_region_id": region["candidate_region_id"],
                "leaf_row_id": region["leaf_row_id"],
                "origin_row_id": region["origin_row_id"],
                "parent_id": collar["parent_id"],
                "leaf_classification":
                    region["leaf_classification"],
                "F_sign": region["F_sign"],
                "HPLUS_sign": region["HPLUS_sign"],
                "HMINUS_sign": region["HMINUS_sign"],
                "outgoing_cell": region["outgoing_cell"],
                "whole_region_outgoing_chart_proof":
                    "STRICT_HPLUS_HMINUS_SIGN_PAIR_ON_R195_REGION",
                "containing_leaf_certifies_target_and_wall_fields":
                    base is not None,
                "frozen_owner_used_as_signature_input": False,
                "resolved_anchor_or_component_used_as_signature_input":
                    False,
                "direct_failure_reasons":
                    sorted(set(region_reasons)),
                "assignment_status": status,
                "local_return_signature": signature,
                "formal_signature_row_materialized": False,
                "single_point_evaluation_used": False,
                "global_exact_key_disposition_credit": 0,
            })
        if index % 1000 == 0 or index == len(outgoing):
            print(
                f"direct-signature {index}/{len(outgoing)}",
                file=sys.stderr,
                flush=True,
            )

    leaf_rows.sort(key=lambda row: row["leaf_row_id"])
    u2_audit_rows.sort(key=lambda row: row["leaf_row_id"])
    direct_leaf_rows.sort(key=lambda row: row["leaf_row_id"])
    assignment_rows.sort(key=lambda row: row["candidate_region_id"])
    require(
        digest(leaf_rows) == EXPECTED_R195_LEAF_ROWS_SHA256,
        "Round195 leaf row pin",
    )
    require(
        len(u2_audit_rows) == EXPECTED_U2_LEAVES
        and digest(u2_audit_rows) == EXPECTED_R195_U2_ROWS_SHA256,
        "Round195 U|U row pin",
    )
    require(
        len(assignment_rows) == EXPECTED_CANDIDATES,
        "candidate assignment census",
    )
    require(
        digest(direct_leaf_rows) == EXPECTED_DIRECT_LEAF_ROWS_SHA256
        and digest(assignment_rows) == EXPECTED_ASSIGNMENT_ROWS_SHA256,
        "direct leaf/region row digest pins",
    )

    leaf_status_counts = Counter(
        row["direct_base_status"] for row in direct_leaf_rows
    )
    assignment_status_counts = Counter(
        row["assignment_status"] for row in assignment_rows
    )
    failure_reason_counts = Counter(
        reason
        for row in assignment_rows
        for reason in row["direct_failure_reasons"]
    )
    certified_leaf_bases = [
        row["direct_signature_base"]
        for row in direct_leaf_rows
        if row["direct_signature_base"] is not None
    ]
    complete_target_count_histogram = Counter(
        base["complete_retained_target_count"]
        for base in certified_leaf_bases
    )
    whole_leaf_outgoing_status_count = Counter(
        (
            "STRICT_CELL:" + base["whole_leaf_box_outgoing_cell"]
            if base["whole_leaf_box_outgoing_cell"] is not None
            else "RESIDUAL_REASON:"
            + "|".join(base["whole_leaf_box_outgoing_reasons"])
        )
        for base in certified_leaf_bases
    )
    assigned_rows = [
        row for row in assignment_rows
        if row["local_return_signature"] is not None
    ]
    residual_rows = [
        row for row in assignment_rows
        if row["local_return_signature"] is None
    ]
    require(
        len(assigned_rows) + len(residual_rows) == EXPECTED_CANDIDATES,
        "direct assignment conservation",
    )
    assigned_signatures = [
        row["local_return_signature"] for row in assigned_rows
    ]
    distinct_signature_digests = sorted({
        digest(signature) for signature in assigned_signatures
    })
    exact_key_ids = sorted({
        signature["official_key_id"] for signature in assigned_signatures
    })
    exact_key_ordinals = sorted({
        signature["official_key_ordinal"]
        for signature in assigned_signatures
    })
    require(
        len(exact_key_ids) == len(exact_key_ordinals),
        "exact key ordinal/id bijection",
    )

    involved_origins = {
        row["origin_row_id"] for row in assignment_rows
    }
    involved_parents = {
        row["parent_id"] for row in assignment_rows
    }
    residual_origins = {
        row["origin_row_id"] for row in residual_rows
    }
    residual_parents = {
        row["parent_id"] for row in residual_rows
    }
    residual_leaves = {
        row["leaf_row_id"] for row in residual_rows
    }
    require(
        len(involved_origins) == EXPECTED_ORIGINS
        and len(involved_parents) == EXPECTED_PARENTS,
        "origin/parent coverage",
    )

    word_length_counts = Counter(
        len(signature["signed_wall_word"])
        for signature in assigned_signatures
    )
    target_counts = Counter(
        signature["target_lift"]
        for signature in assigned_signatures
    )
    outgoing_counts = Counter(
        signature["outgoing_cell"]
        for signature in assigned_signatures
    )
    u2_rows = [
        row for row in assignment_rows
        if row["leaf_row_id"] in u2_leaf_ids
    ]
    require(
        len(u2_rows) == EXPECTED_U2_CANDIDATES,
        "U|U candidate census",
    )
    require(
        digest(u2_rows) == EXPECTED_U2_ASSIGNMENT_ROWS_SHA256,
        "U|U assignment row digest pin",
    )
    u2_status_counts = Counter(
        row["assignment_status"] for row in u2_rows
    )
    u2_assigned_by_leaf = Counter(
        row["leaf_row_id"] for row in u2_rows
        if row["local_return_signature"] is not None
    )
    u2_leaf_counts = Counter(
        (
            "BOTH_SIDES_DIRECTLY_CERTIFIED"
            if u2_assigned_by_leaf[leaf_id] == 2
            else "ONE_SIDE_DIRECTLY_CERTIFIED"
            if u2_assigned_by_leaf[leaf_id] == 1
            else "NO_SIDE_DIRECTLY_CERTIFIED"
        )
        for leaf_id in u2_leaf_ids
    )

    verdict = (
        "VALIDATED"
        if len(assigned_rows) == EXPECTED_CANDIDATES
        else "PARTIAL"
    )
    require(
        verdict == "VALIDATED"
        and not residual_rows
        and leaf_status_counts
        == {"DIRECT_WHOLE_LEAF_BASE_CERTIFIED": EXPECTED_LEAVES}
        and assignment_status_counts
        == {
            "DIRECT_WHOLE_REGION_SIGNATURE_CERTIFIED":
                EXPECTED_CANDIDATES
        }
        and not failure_reason_counts
        and complete_target_count_histogram == {57: EXPECTED_LEAVES}
        and whole_leaf_outgoing_status_count
        == {
            "RESIDUAL_REASON:outgoing_chart_seam":
                EXPECTED_LEAVES
        }
        and u2_status_counts
        == {
            "DIRECT_WHOLE_REGION_SIGNATURE_CERTIFIED":
                EXPECTED_U2_CANDIDATES
        }
        and u2_leaf_counts
        == {"BOTH_SIDES_DIRECTLY_CERTIFIED": EXPECTED_U2_LEAVES},
        "frozen direct signature feasibility census",
    )
    probe_result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_SOURCE_G_WHOLE_REGION_DIRECT_"
            "SIGNATURE_PROBE",
        "question":
            "Can every strict outgoing-W candidate region directly "
            "recompute one canonical local return signature from whole-"
            "region/containing-leaf interval facts, without anchors, "
            "components, parent-wide guessing, or a sampled point?",
        "verdict": verdict,
        "verdict_scope":
            "local outgoing-W direct signature feasibility only; no "
            "formal attachment and no global exact-key fibre disposition",
        "input_chain": pins,
        "direct_method_contract": {
            "complete_target_list_recomputed_per_leaf": True,
            "unique_first_target_selected_without_frozen_owner_input": True,
            "frozen_collar_owner_used_only_for_posthoc_consistency": True,
            "target_and_wall_fields_certified_on_containing_leaf_enclosure":
                True,
            "outgoing_chart_certified_separately_on_each_strict_region":
                True,
            "resolved_signature_anchor_used": False,
            "parent_signature_base_used": False,
            "Round198_adjacency_assignment_used": False,
            "Round203_component_assignment_used": False,
            "single_point_evaluation_used": False,
            "Gate5_registry_independently_rebuilt": True,
        },
        "whole_leaf_base_census": {
            "leaf_count": len(direct_leaf_rows),
            "status_count": dict(sorted(leaf_status_counts.items())),
            "failure_reason_count":
                dict(sorted(failure_reason_counts.items())),
            "direct_leaf_rows_sha256": digest(direct_leaf_rows),
            "all_direct_targets_match_frozen_collars": all(
                row["direct_target_matches_frozen_collar"]
                for row in direct_leaf_rows
            ),
            "whole_leaf_source_chart_strict_inside_count": sum(
                base["whole_leaf_source_chart_classification"]
                == "STRICTLY_INSIDE_TRUE_SOURCE_CHART"
                for base in certified_leaf_bases
            ),
            "complete_retained_target_count_histogram":
                dict(sorted(complete_target_count_histogram.items())),
            "whole_leaf_outgoing_status_count":
                dict(sorted(whole_leaf_outgoing_status_count.items())),
            "Round195_leaf_rows_sha256": digest(leaf_rows),
        },
        "whole_region_signature_census": {
            "candidate_region_count": len(assignment_rows),
            "assigned_candidate_region_count": len(assigned_rows),
            "residual_candidate_region_count": len(residual_rows),
            "assignment_status_count":
                dict(sorted(assignment_status_counts.items())),
            "assignment_rows_sha256": digest(assignment_rows),
            "distinct_local_signature_count":
                len(distinct_signature_digests),
            "distinct_local_signature_digests_sha256":
                digest(distinct_signature_digests),
            "involved_exact_key_count": len(exact_key_ids),
            "involved_exact_key_ids_sha256": digest(exact_key_ids),
            "involved_exact_key_ordinals_sha256":
                digest(exact_key_ordinals),
            "signed_wall_word_length_count":
                dict(sorted(word_length_counts.items())),
            "target_lift_count": len(target_counts),
            "target_lift_histogram_sha256":
                digest(dict(sorted(target_counts.items()))),
            "outgoing_cell_count": dict(sorted(outgoing_counts.items())),
            "residual_leaf_count": len(residual_leaves),
            "residual_origin_count": len(residual_origins),
            "residual_parent_count": len(residual_parents),
            "all_signature_fields_canonical_and_whole_region_strict":
                verdict == "VALIDATED",
            "formal_signature_rows_materialized": False,
        },
        "Round203_residual_cohort_implication": {
            "Round203_directly_anchored_candidate_count":
                ROUND203_DIRECT_ASSIGNED,
            "Round203_unanchored_candidate_count": ROUND203_RESIDUAL,
            "whole_scope_directly_certified": verdict == "VALIDATED",
            "therefore_every_Round203_unanchored_candidate_is_directly_"
            "certifiable": verdict == "VALIDATED",
            "new_directly_certifiable_unanchored_candidate_count": (
                ROUND203_RESIDUAL if verdict == "VALIDATED" else None
            ),
            "anchor_or_component_membership_used_to_select_or_certify_rows":
                False,
        },
        "U_pipe_U_side_specific_audit": {
            "U_pipe_U_leaf_count": len(u2_leaf_ids),
            "side_specific_candidate_region_count": len(u2_rows),
            "assignment_status_count":
                dict(sorted(u2_status_counts.items())),
            "leaf_side_completion_count":
                dict(sorted(u2_leaf_counts.items())),
            "assignment_rows_sha256": digest(u2_rows),
            "two_sides_evaluated_as_distinct_strict_regions": True,
            "Round195_cross_t_ordering_rebuilt": True,
        },
        "remaining_global_fibre_join_gap": {
            "local_outgoing_W_direct_signature_feasibility_complete":
                verdict == "VALIDATED",
            "separate_wall_G_residual_leaf_count": 64,
            "wall_G_signatures_processed_here": False,
            "formal_signature_attachment_emitted": False,
            "independent_direct_signature_verifier_exists": False,
            "half_open_boundary_ownership_materialized": False,
            "global_source_G_exact_key_fibre_count": 224580,
            "global_fibre_occurrence_join_and_deduplication_performed":
                False,
            "fibre_wide_all_occurrences_covered_or_excluded": False,
            "required_next":
                "if this census validates, formalize the direct signature "
                "rows with an independent verifier, close the 64 wall-G "
                "leaves, then perform the complete half-open global exact-"
                "key fibre join and coverage/exclusion proof",
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "runtime_filesystem_writes": 0,
            "output_path_option_exists": False,
            "local_direct_signature_is_not_global_disposition": True,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator": 224580,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
        },
    }
    probe_result_sha256 = digest(probe_result)
    require(
        probe_result_sha256 == EXPECTED_PROBE_RESULT_SHA256,
        "probe result digest pin",
    )
    document = {
        "schema": SCHEMA,
        "probe_result": probe_result,
        "probe_result_sha256": probe_result_sha256,
    }
    output = (
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    require(
        hashlib.sha256(output.encode()).hexdigest()
        == EXPECTED_DOCUMENT_SHA256,
        "probe JSON byte digest pin",
    )
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
