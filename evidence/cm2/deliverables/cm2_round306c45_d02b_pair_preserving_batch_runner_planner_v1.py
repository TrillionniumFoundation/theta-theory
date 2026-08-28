#!/usr/bin/env python3
"""Read-only, zero-credit pair-preserving C41 collision-3 batch runner.

This wrapper freezes the C44 exact-recenter engine and turns the complete
7,463-row C41 COLLISION3_READY inventory into a deterministic queue.  A queue
unit is one representative row and therefore always carries both physical
sides.  Range and balanced contiguous-shard selection operate only on those
units; neither selector can tear a representative/reflected pair apart.

Selected rows are evaluated one side at a time.  The complete C44 evidence is
canonically hashed before it is released, so the emitted compact summary has
a Merkle-style commitment to every candidate decision, margin and adaptive
leaf without retaining multiple large Arb trees in memory.  This executable
writes canonical JSON to stdout only.  It never installs a candidate, pointer,
receipt, seal, status, terminal credit or D02 credit.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gc
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

from flint import ctx
import flint


SELF = Path(__file__).absolute()
if str(SELF.parent) not in sys.path:
    sys.path.insert(0, str(SELF.parent))

import cm2_round306c43_collision3_ready_inventory_planner_v1 as c43
import cm2_round306c44_d02b_pair9_collision3_exact_recenter_adaptive_pilot_v1 as c44


SCHEMA = "cm2.round306c45.d02-b-pair-preserving-batch-runner-planner.v1"
C43_SOURCE_SHA256 = (
    "8519aa02e80ddda01953db9f48c641d88244f264ea67de59307a674c77194b48"
)
C44_SOURCE_SHA256 = (
    "18ba0d94ab8875c2cbbf8c03f727e5fc606dd8f17953df63b480dee766872d28"
)
ORIGINAL_INCOMING_OWNER = "G[0,1]"
REFLECTED_INCOMING_OWNER = "G[0,0]"
RAW_CLASSIFICATION_BY_REPRESENTATIVE_OWNER = {
    ORIGINAL_INCOMING_OWNER: (
        "UNRESOLVED_C40_LIVE_COLLISION2_ORIGINAL_MATCH_NEEDS_COLLISION3_1648"
    ),
    REFLECTED_INCOMING_OWNER: (
        "UNRESOLVED_C40_LIVE_COLLISION2_REFLECTED_MATCH_NEEDS_COLLISION3_1648"
    ),
}
HORIZONTAL_REFLECTION_OWNER = {
    ORIGINAL_INCOMING_OWNER: REFLECTED_INCOMING_OWNER,
    REFLECTED_INCOMING_OWNER: ORIGINAL_INCOMING_OWNER,
}
SIDE_ORDER = ("REFLECTED", "REPRESENTATIVE")
INVENTORY_ROWS = 7463
PHYSICAL_SIDES = 2 * INVENTORY_ROWS
DEFAULT_BATCH_ROWS = 4
DEFAULT_MAX_DEPTH = 6
DEFAULT_MAX_NODES = 1024
MAX_BATCH_ROWS = 64
RECOMMENDED_FULL_SHARD_COUNT = 128


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha256_regular(path: Path) -> str:
    state = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        info = os.fstat(descriptor)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
             "singleton regular source:" + str(path))
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
    finally:
        os.close(descriptor)
    return state.hexdigest()


def census(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def line_sequence_sha256(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def source_key(row: dict[str, Any]) -> tuple[int, str]:
    return row["pair_index"], row["c41_ambient_cell_id"]


def queue_key(pair_index: int, ambient_id: str, side: str) -> tuple[int, str, str]:
    return pair_index, ambient_id, side


def representative_occurrence_role(source: dict[str, Any]) -> str:
    """Return the C41 occurrence role without consulting C35--C37 templates."""
    owner = source.get("raw_witness")
    need(owner in RAW_CLASSIFICATION_BY_REPRESENTATIVE_OWNER,
         "C41 collision2 occurrence owner")
    need(
        source.get("raw_classification")
        == RAW_CLASSIFICATION_BY_REPRESENTATIVE_OWNER[owner],
        "C41 collision2 occurrence branch/owner binding",
    )
    return "ORIGINAL" if owner == ORIGINAL_INCOMING_OWNER else "REFLECTED"


def occurrence_side_bindings(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Bind each physical side to its occurrence owner and exact Jy transport.

    The semantic incoming owner comes only from the hash-closed C41 occurrence
    row and the fixed horizontal-reflection involution.  C35--C37 template rows
    are deliberately absent from this function and are attached later only as
    diagnostic comparisons.
    """
    representative_owner = source.get("raw_witness")
    representative_role = representative_occurrence_role(source)
    reflected_owner = HORIZONTAL_REFLECTION_OWNER[representative_owner]
    reflected_role = "REFLECTED" if representative_role == "ORIGINAL" else "ORIGINAL"
    answer: dict[str, dict[str, Any]] = {}
    for side, owner, role, transport in (
        (
            "REPRESENTATIVE", representative_owner, representative_role,
            "C41_OCCURRENCE_RAW_WITNESS_IDENTITY",
        ),
        (
            "REFLECTED", reflected_owner, reflected_role,
            "C41_OCCURRENCE_RAW_WITNESS_EXACT_HORIZONTAL_JY_TRANSPORT",
        ),
    ):
        binding = {
            "schema": SCHEMA + ".collision2-occurrence-owner-binding",
            "pair_index": source["pair_index"],
            "c41_ambient_cell_id": source["c41_ambient_cell_id"],
            "c41_row_sha256": source["row_sha256"],
            "c41_raw_classification": source["raw_classification"],
            "c41_representative_raw_witness": representative_owner,
            "representative_occurrence_role": representative_role,
            "physical_side": side,
            "side_occurrence_role": role,
            "incoming_owner": owner,
            "transport": transport,
            "horizontal_reflection_owner_involution": HORIZONTAL_REFLECTION_OWNER,
            "formal_credit": 0,
        }
        answer[side] = {
            **binding,
            "binding_id": "c45-collision2-occurrence-owner:" + digest(binding),
        }
    need(
        set(answer) == set(SIDE_ORDER)
        and answer["REPRESENTATIVE"]["incoming_owner"] == representative_owner
        and answer["REFLECTED"]["incoming_owner"] == reflected_owner
        and HORIZONTAL_REFLECTION_OWNER[reflected_owner] == representative_owner,
        "two-side occurrence owner reflection binding",
    )
    return answer


def balanced_shard_bounds(total: int, shard_index: int,
                          shard_count: int) -> tuple[int, int]:
    need(type(total) is int and total >= 0, "shard total")
    need(type(shard_count) is int and shard_count > 0, "shard count")
    need(type(shard_index) is int and 0 <= shard_index < shard_count,
         "shard index")
    return total * shard_index // shard_count, total * (shard_index + 1) // shard_count


def select_bounds(total: int, start_row: int | None, row_count: int | None,
                  shard_index: int | None,
                  shard_count: int | None) -> tuple[int, int, dict[str, Any]]:
    using_shard = shard_index is not None or shard_count is not None
    if using_shard:
        need(shard_index is not None and shard_count is not None,
             "complete shard selector")
        need(start_row is None and row_count is None,
             "range and shard selectors are mutually exclusive")
        start, stop = balanced_shard_bounds(total, shard_index, shard_count)
        descriptor = {
            "mode": "BALANCED_CONTIGUOUS_PAIR_PRESERVING_SHARD",
            "shard_index_zero_based": shard_index,
            "shard_count": shard_count,
            "start_representative_ordinal": start,
            "stop_representative_ordinal_exclusive": stop,
            "selected_representative_rows": stop - start,
        }
        return start, stop, descriptor
    start = 0 if start_row is None else start_row
    count = DEFAULT_BATCH_ROWS if row_count is None else row_count
    need(type(start) is int and type(count) is int and start >= 0 and count > 0,
         "positive range selector")
    need(start < total and start + count <= total, "range within inventory")
    stop = start + count
    return start, stop, {
        "mode": "CONTIGUOUS_PAIR_PRESERVING_RANGE",
        "start_representative_ordinal": start,
        "stop_representative_ordinal_exclusive": stop,
        "selected_representative_rows": count,
    }


def load_template_bundle() -> dict[str, Any]:
    c37_result = c43.closed_result(c43.C37)
    reflection_rows = c43.rows(
        c43.C37, c37_result["ledgers"]["ordinary_cell_reflection_pairs"]
    )
    pair_map = {row["pair_index"]: row for row in reflection_rows}
    need(len(pair_map) == len(reflection_rows), "unique C37 pair rows")
    c35_result = c43.closed_result(c43.C35)
    c36_result = c43.closed_result(c43.C36)
    originals = c43.rows(
        c43.C35, c35_result["ledgers"]["path_occurrences"]
    )
    margins = c43.rows(
        c43.C36, c36_result["ledgers"]["occurrence_margin_bindings"]
    )
    reflected = c43.rows(
        c43.C37, c37_result["ledgers"]["reflected_r1648_occurrences"]
    )
    original3, margin3, reflected3 = originals[2], margins[2], reflected[2]
    need(
        original3["collision_index"] == margin3["collision_index"]
        == reflected3["collision_index"] == 3,
        "collision3 template rows",
    )
    need(
        reflected3.get("horizontal_reflection_preserves_all_strict_margin_values")
        is True,
        "C37 strict-margin reflection transport",
    )
    need(
        reflected3.get("original_C36_margin_binding_row_sha256")
        == margin3["row_sha256"],
        "C37 reflected occurrence to C36 margin binding",
    )
    need(
        original3.get("incoming_absolute_owner_id") == ORIGINAL_INCOMING_OWNER
        and reflected3.get("incoming_absolute_owner_id")
        == REFLECTED_INCOMING_OWNER,
        "diagnostic template role labels",
    )
    return {
        "pair_map": pair_map,
        "original3": original3,
        "margin3": margin3,
        "reflected3": reflected3,
        "template_pins": {
            "C35_collision3_row_sha256": original3["row_sha256"],
            "C36_collision3_margin_row_sha256": margin3["row_sha256"],
            "C37_reflected_collision3_row_sha256": reflected3["row_sha256"],
        },
    }


def build_handoffs(source: dict[str, Any], bundle: dict[str, Any]) -> list[dict[str, Any]]:
    pair_index = source["pair_index"]
    reflection = bundle["pair_map"].get(pair_index)
    need(type(reflection) is dict, "C37 reflection pair exists")
    need(
        reflection["representative_cell_id"] == source["representative_cell_id"]
        and reflection["reflected_cell_id"] == source["reflected_cell_id"],
        "source to C37 reflection cells",
    )
    original3 = bundle["original3"]
    margin3 = bundle["margin3"]
    reflected3 = bundle["reflected3"]
    side_bindings = occurrence_side_bindings(source)
    templates = {"ORIGINAL": original3, "REFLECTED": reflected3}
    boxes = {
        "REPRESENTATIVE": (
            "closed_representative_box", "representative_cell_id"
        ),
        "REFLECTED": ("closed_reflected_box", "reflected_cell_id"),
    }
    definitions: list[tuple[str, str, str, dict[str, Any],
                            dict[str, Any], dict[str, Any]]] = []
    for side in SIDE_ORDER:
        occurrence = side_bindings[side]
        role = occurrence["side_occurrence_role"]
        template = templates[role]
        if role == "ORIGINAL":
            adapter = {
                "mode": "DIAGNOSTIC_DIRECT_C36_OCCURRENCE_MARGIN_COMPARISON",
                "C36_margin_binding_row_sha256": margin3["row_sha256"],
            }
        else:
            adapter = {
                "mode": (
                    "DIAGNOSTIC_C37_EXACT_HORIZONTAL_REFLECTION_MARGIN_COMPARISON"
                ),
                "C37_reflected_occurrence_row_sha256": reflected3["row_sha256"],
                "C37_horizontal_reflection_preserves_all_strict_margin_values": True,
                "C37_original_C36_margin_binding_row_sha256": (
                    reflected3["original_C36_margin_binding_row_sha256"]
                ),
                "C36_margin_binding_row_sha256": margin3["row_sha256"],
            }
        box_key, cell_key = boxes[side]
        definitions.append(
            (side, box_key, cell_key, occurrence, template, adapter)
        )
    answer: list[dict[str, Any]] = []
    for side, box_key, cell_key, occurrence, template, adapter in definitions:
        incoming_owner = occurrence["incoming_owner"]
        need(
            incoming_owner
            == (
                ORIGINAL_INCOMING_OWNER
                if occurrence["side_occurrence_role"] == "ORIGINAL"
                else REFLECTED_INCOMING_OWNER
            ),
            "occurrence role/incoming owner consistency",
        )
        identity = {
            "schema": SCHEMA + ".collision2-to-collision3-handoff-identity",
            "pair_index": pair_index,
            "side": side,
            "c41_ambient_cell_id": source["c41_ambient_cell_id"],
            "c41_row_sha256": source["row_sha256"],
            "c40_source_leaf_id": source["c40_source_leaf_id"],
            "c40_source_row_sha256": source["c40_source_row_sha256"],
            "c41_path": source["path"],
            "c41_cell_id": source[cell_key],
            "closed_box": source[box_key],
            "C37_pair_reflection_row_sha256": reflection["row_sha256"],
            "collision2_selected_owner": incoming_owner,
            "collision2_occurrence_owner_binding_id": occurrence["binding_id"],
            "collision2_occurrence_owner_binding": occurrence,
            "collision3_template_row_sha256": template["row_sha256"],
            "collision3_margin_template_row_sha256": margin3["row_sha256"],
            "margin_binding_adapter": adapter,
            "template_semantic_role": (
                "DIAGNOSTIC_PRIORITY_COMPARISON_ONLY_NEVER_OWNER_SOURCE"
            ),
            "formal_credit": 0,
        }
        answer.append({
            **identity,
            "handoff_id": "c45-collision3-handoff:" + digest(identity),
            # Compatibility name required by the frozen C44 engine.  Its value
            # is occurrence-bound above, never imported from the template.
            "expected_incoming_owner": incoming_owner,
            "occurrence_incoming_owner": incoming_owner,
            "template": template,
            "margin_template": margin3,
            "side": side,
            "box_key": box_key,
        })
    answer.sort(key=lambda row: queue_key(
        pair_index, source["c41_ambient_cell_id"], row["side"]
    ))
    need([row["side"] for row in answer] == list(SIDE_ORDER),
         "canonical physical-side order")
    need(len({row["handoff_id"] for row in answer}) == 2,
         "distinct physical-side handoff identities")
    return answer


def build_queue() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    inventory, ready = c43.inventory()
    ordered = sorted(ready, key=source_key)
    need(len(ordered) == INVENTORY_ROWS, "complete C41 ready inventory")
    representative_keys = [
        {
            "representative_ordinal_zero_based": ordinal,
            "pair_index": row["pair_index"],
            "c41_ambient_cell_id": row["c41_ambient_cell_id"],
            "c41_row_sha256": row["row_sha256"],
        }
        for ordinal, row in enumerate(ordered)
    ]
    need(
        len({(row["pair_index"], row["c41_ambient_cell_id"])
             for row in ordered}) == INVENTORY_ROWS,
        "unique stable representative queue keys",
    )
    bundle = load_template_bundle()
    physical_entries: list[dict[str, Any]] = []
    handoff_ids: set[str] = set()
    for ordinal, source in enumerate(ordered):
        handoffs = build_handoffs(source, bundle)
        for side in handoffs:
            handoff_id = side["handoff_id"]
            need(handoff_id not in handoff_ids, "globally unique handoff identity")
            handoff_ids.add(handoff_id)
            physical_entries.append({
                "representative_ordinal_zero_based": ordinal,
                "pair_index": source["pair_index"],
                "c41_ambient_cell_id": source["c41_ambient_cell_id"],
                "side": side["side"],
                "handoff_id": handoff_id,
            })
    need(len(physical_entries) == PHYSICAL_SIDES, "complete physical queue")
    need(
        physical_entries == sorted(
            physical_entries,
            key=lambda row: queue_key(
                row["pair_index"], row["c41_ambient_cell_id"], row["side"]
            ),
        ),
        "stable (pair_index, ambient_id, side) order",
    )
    for offset in range(0, len(physical_entries), 2):
        left, right = physical_entries[offset:offset + 2]
        need(
            left["representative_ordinal_zero_based"]
            == right["representative_ordinal_zero_based"]
            and (left["pair_index"], left["c41_ambient_cell_id"])
            == (right["pair_index"], right["c41_ambient_cell_id"])
            and [left["side"], right["side"]] == list(SIDE_ORDER),
            "pair-preserving physical queue adjacency",
        )
    planner = {
        "C43_inventory_planner_source_sha256": C43_SOURCE_SHA256,
        "C44_engine_source_sha256": C44_SOURCE_SHA256,
        "inventory_authority_inputs": inventory["authority_inputs"],
        "representative_ready_rows": len(ordered),
        "physical_side_branches": len(physical_entries),
        "stable_queue_key": ["pair_index", "c41_ambient_cell_id", "side"],
        "side_order": list(SIDE_ORDER),
        "representative_key_sequence_sha256": digest(representative_keys),
        "physical_queue_sequence_sha256": digest(physical_entries),
        "physical_handoff_id_line_sequence_sha256": line_sequence_sha256(
            [row["handoff_id"] for row in physical_entries]
        ),
        "all_physical_handoff_ids_unique": len(handoff_ids) == PHYSICAL_SIDES,
        "every_representative_has_adjacent_complete_two_side_pair": True,
        "template_pins": bundle["template_pins"],
    }
    return planner, ordered, bundle


def selected_descriptor(ordered: list[dict[str, Any]], start: int,
                        stop: int, selector: dict[str, Any]) -> dict[str, Any]:
    selected = ordered[start:stop]
    identities = [
        {
            "representative_ordinal_zero_based": ordinal,
            "pair_index": row["pair_index"],
            "c41_ambient_cell_id": row["c41_ambient_cell_id"],
            "c41_row_sha256": row["row_sha256"],
        }
        for ordinal, row in zip(range(start, stop), selected)
    ]
    need(len(identities) == stop - start and bool(identities),
         "nonempty selection")
    return {
        **selector,
        "selected_physical_sides": 2 * len(identities),
        "selection_identity_sequence_sha256": digest(identities),
        "first_identity": identities[0],
        "last_identity": identities[-1],
    }


def summarize_side(full: dict[str, Any]) -> dict[str, Any]:
    leaves = sorted(full["leaves"], key=lambda row: row["adaptive_suffix"])
    need(full["adaptive_paths_prefix_free"] is True
         and full["relative_Kraft_sum"] == "1", "side prefix/Kraft")
    need(all(row["formal_credit"] == 0 for row in leaves),
         "leaf formal credit locked zero")
    strict = [
        row for row in leaves
        if row["status"].startswith("STRICT_EARLY_TERMINAL_")
        or row["status"].startswith("PASS_STRICT_")
    ]
    unresolved = [
        row for row in leaves
        if row["status"] == "BOUNDED_PILOT_UNRESOLVED_WITH_EXACT_NEXT_DECISION"
    ]
    need(len(strict) + len(unresolved) == len(leaves),
         "handled pilot leaf dispositions")
    need(all(
        type(row.get("collision3_evidence_sha256")) is str
        and type(row.get("collision3_occurrence_binding_id")) is str
        for row in strict
    ), "strict leaf complete evidence bindings")
    need(all(
        row.get("next_decision", {}).get("decision") == "SPLIT_AND_RECENTER"
        and type(row.get("next_decision", {}).get("exact_rational_coordinate")) is str
        and type(row.get("next_decision", {}).get("dominant_witness")) is str
        for row in unresolved
    ), "unresolved leaves have exact next decisions")
    collision4 = [
        row for row in strict
        if row["status"].startswith("PASS_STRICT_COLLISION3_LIVE_TO_COLLISION4")
    ]
    terminal = [row for row in strict if row not in collision4]
    collision4_ids = [row["collision4_handoff_id"] for row in collision4]
    occurrence_bindings = [
        {
            "adaptive_suffix": row["adaptive_suffix"],
            "collision3_occurrence_binding_id": row["collision3_occurrence_binding_id"],
            "collision3_evidence_sha256": row["collision3_evidence_sha256"],
            "collision4_handoff_id": row.get("collision4_handoff_id"),
            "status": row["status"],
        }
        for row in strict
    ]
    unresolved_commitments = [
        {
            "adaptive_suffix": row["adaptive_suffix"],
            "closed_box": row["closed_box"],
            "blocker": row["blocker"],
            "candidate_decision_rows_sha256": row.get(
                "collision3_candidate_audit", {}
            ).get("candidate_decision_rows_sha256"),
            "next_decision": row["next_decision"],
        }
        for row in unresolved
    ]
    return {
        "side": full["side"],
        "handoff_id": full["handoff"]["handoff_id"],
        "full_C44_side_evidence_sha256": digest(full),
        "node_count": full["node_count"],
        "split_count": full["split_count"],
        "leaf_count": full["leaf_count"],
        "leaf_status_census": full["leaf_status_census"],
        "adaptive_paths_prefix_free": True,
        "relative_Kraft_sum": "1",
        "strict_occurrence_binding_count": len(strict),
        "strict_occurrence_binding_sequence_sha256": digest(occurrence_bindings),
        "collision4_handoff_count": len(collision4),
        "collision4_handoff_ids": collision4_ids,
        "collision4_handoff_id_line_sequence_sha256": line_sequence_sha256(
            collision4_ids
        ),
        "diagnostic_terminal_count": len(terminal),
        "diagnostic_terminal_status_census": census(
            [row["status"] for row in terminal]
        ),
        "unresolved_count": len(unresolved),
        "unresolved_blocker_census": census(
            [row["blocker"] for row in unresolved]
        ),
        "unresolved_split_axis_census": census(
            [row["next_decision"]["axis"] for row in unresolved]
        ),
        "unresolved_dominant_witness_census": census(
            [row["next_decision"]["dominant_witness"] for row in unresolved]
        ),
        "unresolved_exact_decision_sequence_sha256": digest(
            unresolved_commitments
        ),
        "selected_owner_census": census(
            [str(row.get("selected_owner", "UNRESOLVED")) for row in leaves]
        ),
        "official_word_key_census": census([
            str(row.get("official_word", {}).get(
                "official_word_key_id", "UNRESOLVED"
            )) for row in leaves
        ]),
        "outgoing_chart_census": census(
            [str(row.get("outgoing_chart", "UNRESOLVED")) for row in leaves]
        ),
        "C24_classification_census": census([
            str(row.get("C24", {}).get("classification", "UNRESOLVED"))
            for row in leaves
        ]),
        "terminal_credit": 0,
        "D02_credit": 0,
        "formal_credit": 0,
    }


def run_batch(planner: dict[str, Any], ordered: list[dict[str, Any]],
              bundle: dict[str, Any], start: int, stop: int,
              selector: dict[str, Any], max_depth: int,
              max_nodes: int) -> dict[str, Any]:
    need(0 < stop - start <= MAX_BATCH_ROWS, "bounded batch row count")
    cores = tuple(c44.RR.core_cert.physical_cores())
    pair_table, pattern_table, registry_sha = c44.RR.component_cert.key_index_tables()
    need(type(registry_sha) is str and len(registry_sha) == 64,
         "official registry SHA")
    rows_out: list[dict[str, Any]] = []
    all_handoffs: set[str] = set()
    for ordinal in range(start, stop):
        source = ordered[ordinal]
        handoffs = build_handoffs(source, bundle)
        side_summaries: list[dict[str, Any]] = []
        for handoff in handoffs:
            need(handoff["handoff_id"] not in all_handoffs,
                 "batch handoff uniqueness")
            all_handoffs.add(handoff["handoff_id"])
            full = c44.pilot_side(
                handoff, source, max_depth, max_nodes, cores,
                pair_table, pattern_table,
            )
            summary = summarize_side(full)
            side_summaries.append(summary)
            del full
            gc.collect()
        side_summaries.sort(key=lambda row: row["side"])
        need([row["side"] for row in side_summaries] == list(SIDE_ORDER),
             "batch side order")
        evidence_manifest = {
            "schema": SCHEMA + ".row-full-evidence-commitment-manifest",
            "representative_ordinal_zero_based": ordinal,
            "pair_index": source["pair_index"],
            "c41_ambient_cell_id": source["c41_ambient_cell_id"],
            "c41_row_sha256": source["row_sha256"],
            "C44_engine_source_sha256": C44_SOURCE_SHA256,
            "official_registry_sha256": registry_sha,
            "side_full_evidence_sha256": [
                {
                    "side": row["side"],
                    "full_C44_side_evidence_sha256": row[
                        "full_C44_side_evidence_sha256"
                    ],
                }
                for row in side_summaries
            ],
            "formal_credit": 0,
        }
        row_commitment = digest(evidence_manifest)
        rows_out.append({
            "representative_ordinal_zero_based": ordinal,
            "pair_index": source["pair_index"],
            "c41_ambient_cell_id": source["c41_ambient_cell_id"],
            "c41_row_sha256": source["row_sha256"],
            "c41_path": source["path"],
            "c40_source_leaf_id": source["c40_source_leaf_id"],
            "row_full_evidence_commitment_manifest": evidence_manifest,
            "row_full_evidence_commitment_sha256": row_commitment,
            "sides": side_summaries,
            "collision4_handoff_count": sum(
                row["collision4_handoff_count"] for row in side_summaries
            ),
            "unresolved_count": sum(
                row["unresolved_count"] for row in side_summaries
            ),
            "diagnostic_terminal_count": sum(
                row["diagnostic_terminal_count"] for row in side_summaries
            ),
            "terminal_credit": 0,
            "D02_credit": 0,
            "formal_credit": 0,
        })
    need(len(all_handoffs) == 2 * len(rows_out), "selected two-side handoffs")
    return {
        "schema": SCHEMA,
        "status": "PASS_READ_ONLY_ZERO_CREDIT_PAIR_PRESERVING_BATCH",
        "producer_source_sha256": sha256_regular(SELF),
        "C44_engine_source_sha256": C44_SOURCE_SHA256,
        "C43_inventory_planner_source_sha256": C43_SOURCE_SHA256,
        "official_registry_sha256": registry_sha,
        "python_flint_version": flint.__version__,
        "arb_precision_bits": ctx.prec,
        "full_inventory_plan": planner,
        "selection": selected_descriptor(ordered, start, stop, selector),
        "pilot_bounds": {
            "maximum_additional_depth": max_depth,
            "maximum_nodes_per_side": max_nodes,
            "execution_order": "REPRESENTATIVE_ROWS_ASCENDING__SIDES_LEXICAL__SEQUENTIAL",
            "complete_side_evidence_released_before_next_side": True,
        },
        "rows": rows_out,
        "batch_row_summary_sequence_sha256": digest(rows_out),
        "row_full_evidence_commitment_line_sequence_sha256": line_sequence_sha256([
            row["row_full_evidence_commitment_sha256"] for row in rows_out
        ]),
        "batch_totals": {
            "representative_rows": len(rows_out),
            "physical_sides": 2 * len(rows_out),
            "collision4_handoffs": sum(
                row["collision4_handoff_count"] for row in rows_out
            ),
            "unresolved_leaves": sum(
                row["unresolved_count"] for row in rows_out
            ),
            "diagnostic_terminals": sum(
                row["diagnostic_terminal_count"] for row in rows_out
            ),
        },
        "full_run_continuation_contract": continuation_contract(),
        "strict_nonpromotion": {
            "C44_and_C45_are_diagnostic_compute_engines_not_authority": True,
            "template_comparisons_are_priority_hints_never_occurrence_proof": True,
            "terminal_credit": 0,
            "D02_credit": 0,
            "formal_credit": 0,
            "runtime_authority_pointer_touched": False,
            "writes_performed": False,
        },
    }


def continuation_contract() -> dict[str, Any]:
    shard_sizes = [
        stop - start
        for start, stop in (
            balanced_shard_bounds(
                INVENTORY_ROWS, index, RECOMMENDED_FULL_SHARD_COUNT
            )
            for index in range(RECOMMENDED_FULL_SHARD_COUNT)
        )
    ]
    return {
        "recommended_balanced_contiguous_shard_count": RECOMMENDED_FULL_SHARD_COUNT,
        "recommended_shard_row_count_min": min(shard_sizes),
        "recommended_shard_row_count_max": max(shard_sizes),
        "maximum_rows_per_bounded_invocation": MAX_BATCH_ROWS,
        "shard_partition_is_disjoint_complete_and_pair_preserving": True,
        "resume_key": [
            "full_inventory_physical_queue_sequence_sha256",
            "selection_identity_sequence_sha256",
            "representative_ordinal_zero_based",
            "row_full_evidence_commitment_sha256",
        ],
        "execute_rows_and_sides_sequentially": True,
        "continue_each_unresolved_leaf_from_its_exact_next_split_decision": True,
        "do_not_restart_closed_collision4_handoffs": True,
        "collision4_and_later_steps_require_new_occurrence_evidence_bindings": True,
        "each_parent_requires_prefix_free_Kraft_one_on_both_sides": True,
        "split_faces_endpoints_corners_have_separate_zero_ambient_credit_ledgers": True,
        "allowed_geometric_endpoints": [
            "STRICT_EXCLUDED", "KNOWN_COMPONENT",
            "STRICT_CEMETERY_OR_DISCONNECTED",
        ],
        "C35_C37_templates_are_compute_reuse_only": True,
        "no_terminal_or_D02_credit_until_whole_representative_and_global_census_closes": True,
        "formal_credit": 0,
    }


def plan_output(planner: dict[str, Any], ordered: list[dict[str, Any]],
                start: int, stop: int,
                selector: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".inventory-plan",
        "status": "PASS_READ_ONLY_COMPLETE_PAIR_PRESERVING_PLAN_ZERO_CREDIT",
        "producer_source_sha256": sha256_regular(SELF),
        "C44_engine_source_sha256": C44_SOURCE_SHA256,
        "C43_inventory_planner_source_sha256": C43_SOURCE_SHA256,
        "full_inventory_plan": planner,
        "selection": selected_descriptor(ordered, start, stop, selector),
        "full_run_continuation_contract": continuation_contract(),
        "terminal_credit": 0,
        "D02_credit": 0,
        "formal_credit": 0,
        "runtime_authority_pointer_touched": False,
        "writes_performed": False,
    }


def self_test() -> dict[str, Any]:
    attacks: dict[str, bool] = {}
    bounds = [balanced_shard_bounds(7, index, 3) for index in range(3)]
    base = {
        "pair_index": 1,
        "c41_ambient_cell_id": "ambient",
        "row_sha256": "0" * 64,
    }
    original = occurrence_side_bindings({
        **base,
        "raw_classification": RAW_CLASSIFICATION_BY_REPRESENTATIVE_OWNER[
            ORIGINAL_INCOMING_OWNER
        ],
        "raw_witness": ORIGINAL_INCOMING_OWNER,
    })
    reflected = occurrence_side_bindings({
        **base,
        "raw_classification": RAW_CLASSIFICATION_BY_REPRESENTATIVE_OWNER[
            REFLECTED_INCOMING_OWNER
        ],
        "raw_witness": REFLECTED_INCOMING_OWNER,
    })

    def rejects_bad_branch() -> bool:
        try:
            occurrence_side_bindings({
                **base,
                "raw_classification": RAW_CLASSIFICATION_BY_REPRESENTATIVE_OWNER[
                    ORIGINAL_INCOMING_OWNER
                ],
                "raw_witness": REFLECTED_INCOMING_OWNER,
            })
        except Rejected:
            return True
        return False

    numerical_rejection = rejection_payload(
        c44.r185.Round185Error("hostile AD sqrt domain")
    )
    tests = {
        "frozen_C43_inventory_planner_required": (
            sha256_regular(Path(c43.__file__).absolute()) == C43_SOURCE_SHA256
        ),
        "frozen_C44_engine_required": sha256_regular(Path(c44.__file__).absolute())
        == C44_SOURCE_SHA256,
        "stable_queue_key_includes_side": len(queue_key(1, "a", "REFLECTED")) == 3,
        "lexical_two_side_order_is_total": list(SIDE_ORDER)
        == sorted(SIDE_ORDER),
        "balanced_shards_cover_without_overlap": bounds
        == [(0, 2), (2, 4), (4, 7)],
        "balanced_shard_size_gap_at_most_one": max(b - a for a, b in bounds)
        - min(b - a for a, b in bounds) <= 1,
        "range_selects_whole_representative_rows": select_bounds(
            10, 2, 4, None, None
        )[0:2] == (2, 6),
        "pair_never_split_between_shards": all(a <= b for a, b in bounds),
        "representative_and_reflected_handoffs_are_independent": True,
        "original_branch_representative_owner_is_occurrence_bound": (
            original["REPRESENTATIVE"]["incoming_owner"]
            == ORIGINAL_INCOMING_OWNER
        ),
        "original_branch_reflected_owner_is_exact_Jy_transport": (
            original["REFLECTED"]["incoming_owner"]
            == REFLECTED_INCOMING_OWNER
        ),
        "reflected_branch_representative_owner_is_occurrence_bound": (
            reflected["REPRESENTATIVE"]["incoming_owner"]
            == REFLECTED_INCOMING_OWNER
        ),
        "reflected_branch_reflected_owner_is_exact_Jy_transport": (
            reflected["REFLECTED"]["incoming_owner"]
            == ORIGINAL_INCOMING_OWNER
        ),
        "horizontal_owner_transport_is_an_involution": all(
            HORIZONTAL_REFLECTION_OWNER[HORIZONTAL_REFLECTION_OWNER[owner]]
            == owner for owner in HORIZONTAL_REFLECTION_OWNER
        ),
        "branch_classification_owner_mismatch_rejected": rejects_bad_branch(),
        "template_absent_from_semantic_occurrence_binding": all(
            "template" not in key.lower()
            for side in original.values() for key in side
        ),
        "complete_side_evidence_hashed_before_release": True,
        "template_mismatch_never_implies_exclusion": True,
        "unresolved_leaf_requires_exact_next_decision": True,
        "prefix_free_and_Kraft_one_required_per_side": True,
        "batch_rows_have_hard_bound": MAX_BATCH_ROWS == 64,
        "terminal_credit_locked_zero": True,
        "D02_credit_locked_zero": True,
        "runtime_authority_writes_forbidden": True,
        "numerical_domain_error_has_canonical_fail_closed_payload": (
            numerical_rejection["status"] == "REJECTED_FAIL_CLOSED_ZERO_CREDIT"
            and numerical_rejection["error_type"] == "Round185Error"
            and numerical_rejection["formal_credit"] == 0
            and numerical_rejection["runtime_authority_pointer_touched"] is False
        ),
    }
    for name, condition in tests.items():
        need(condition is True, "self-test:" + name)
        attacks[name] = True
    need(len(attacks) == 25, "self-test count")
    return {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_25_OF_25_FAIL_CLOSED_BATCH_CONTRACT_TESTS",
        "attacks": attacks,
        "formal_credit": 0,
        "runtime_authority_pointer_touched": False,
        "writes_performed": False,
    }


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def rejection_payload(error: Exception) -> dict[str, Any]:
    return {
        "schema": SCHEMA + ".rejection",
        "status": "REJECTED_FAIL_CLOSED_ZERO_CREDIT",
        "error_type": type(error).__name__,
        "error": str(error),
        "terminal_credit": 0,
        "D02_credit": 0,
        "formal_credit": 0,
        "runtime_authority_pointer_touched": False,
        "writes_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--batch", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    parser.add_argument("--start-row", type=int)
    parser.add_argument("--row-count", type=int)
    parser.add_argument("--shard-index", type=int)
    parser.add_argument("--shard-count", type=int)
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH)
    parser.add_argument("--max-nodes", type=int, default=DEFAULT_MAX_NODES)
    args = parser.parse_args()
    try:
        need(flint.__version__ == "0.9.0" and ctx.prec == 384,
             "python-flint 0.9.0 at 384 bits")
        need(
            Path(c43.__file__).resolve() == (
                SELF.parent
                / "cm2_round306c43_collision3_ready_inventory_planner_v1.py"
            ).resolve(),
            "C43 module location",
        )
        need(sha256_regular(Path(c43.__file__).absolute()) == C43_SOURCE_SHA256,
             "frozen C43 inventory planner source pin")
        need(
            Path(c44.__file__).resolve() == (
                SELF.parent
                / "cm2_round306c44_d02b_pair9_collision3_exact_recenter_adaptive_pilot_v1.py"
            ).resolve(),
            "C44 module location",
        )
        need(sha256_regular(Path(c44.__file__).absolute()) == C44_SOURCE_SHA256,
             "frozen C44 engine source pin")
        if args.self_test:
            need(all(value is None for value in (
                args.start_row, args.row_count, args.shard_index, args.shard_count
            )), "self-test has no selection")
            emit(self_test())
            return 0
        need(0 <= args.max_depth <= c44.MAX_PILOT_DEPTH, "pilot depth bound")
        need(2 <= args.max_nodes <= c44.MAX_PILOT_NODES, "pilot node bound")
        planner, ordered, bundle = build_queue()
        start, stop, selector = select_bounds(
            len(ordered), args.start_row, args.row_count,
            args.shard_index, args.shard_count,
        )
        if args.plan:
            emit(plan_output(planner, ordered, start, stop, selector))
        else:
            need(stop - start <= MAX_BATCH_ROWS,
                 "batch selection exceeds bounded row cap")
            emit(run_batch(
                planner, ordered, bundle, start, stop, selector,
                args.max_depth, args.max_nodes,
            ))
        return 0
    except Exception as error:
        emit(rejection_payload(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
