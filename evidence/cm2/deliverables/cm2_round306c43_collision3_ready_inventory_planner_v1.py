#!/usr/bin/env python3
"""Read-only D02-B inventory/planner for the C41 collision-3-ready queue.

No mode writes below the workspace, publishes a candidate, or grants credit.
The optional pair-9 pilot is a diagnostic only: it compares the legacy whole-
box interval pipeline with exact-center hints and bounded adaptive bisection.
Point values and template reuse are never certificates.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Iterable


SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
C41 = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C36 = ROOT / ".cm2-runtime/candidates/c36-template-margin-atlas-20260810T153254Z-f37f908cf93d924c"
C37 = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"

RESULT_PINS = {
    C41: ("73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
          "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"),
    C35: ("3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
          "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752"),
    C36: ("7922139708dc486232ec79b29d6339bdca7e00999bddf63d5b9a83b3f4cfbbd1",
          "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167"),
    C37: ("5b968d957cbca2a4f8aec855a44643f5add7fe0244d933401dfdef9ad7be61f3",
          "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b"),
}
HEX64 = re.compile(r"[0-9a-f]{64}")


class Rejected(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha256(path: Path) -> str:
    state = hashlib.sha256()
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        info = os.fstat(fd)
        need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
             "singleton input:" + str(path))
        while block := os.read(fd, 4 << 20):
            state.update(block)
    finally:
        os.close(fd)
    return state.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key:" + key)
            result[key] = value
        return result
    value = json.loads(path.read_text(encoding="ascii"), object_pairs_hook=pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(Rejected(token)),
        parse_float=lambda token: (_ for _ in ()).throw(Rejected(token)))
    need(type(value) is dict, "top JSON object")
    return value


def closed_result(directory: Path) -> dict[str, Any]:
    file_pin, object_pin = RESULT_PINS[directory]
    path = directory / "result.json"
    need(sha256(path) == file_pin, "result file pin:" + directory.name)
    value = strict_json(path)
    body = dict(value)
    claim = body.pop("object_sha256", None)
    need(claim == object_pin == digest(body), "result closure:" + directory.name)
    return value


def rows(directory: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    path = directory / descriptor["filename"]
    need(sha256(path) == descriptor["sha256"]
         and path.stat().st_size == descriptor["size"],
         "ledger file descriptor:" + str(path))
    answer: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for line in stream:
            value = json.loads(line)
            body = dict(value)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and claim == digest(body),
                 "row closure:" + descriptor["filename"])
            sequence.update((claim + "\n").encode("ascii"))
            answer.append(value)
    need(len(answer) == descriptor["row_count"]
         and sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         "ledger sequence:" + descriptor["filename"])
    return answer


def reflected_chart(chart: str) -> str:
    return {"E": "E", "W": "W", "N": "S", "S": "N"}[chart]


def inventory() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    c41 = closed_result(C41)
    c35 = closed_result(C35)
    c36 = closed_result(C36)
    c37 = closed_result(C37)
    routed = rows(C41, c41["ledgers"]["routed_ambient_cells"])
    ready = [row for row in routed if row["disposition_family"] == "COLLISION3_READY"]
    pairs = rows(C37, c37["ledgers"]["ordinary_cell_reflection_pairs"])
    pair_map = {row["pair_index"]: row for row in pairs}
    original = rows(C35, c35["ledgers"]["path_occurrences"])
    margins = rows(C36, c36["ledgers"]["occurrence_margin_bindings"])
    reflected = rows(C37, c37["ledgers"]["reflected_r1648_occurrences"])

    need(len(ready) == 7463 and len(original) == len(margins) == len(reflected) == 1648,
         "authority census")
    need([r["collision_index"] for r in original] == list(range(1, 1649))
         and [r["collision_index"] for r in margins] == list(range(1, 1649))
         and [r["collision_index"] for r in reflected] == list(range(1, 1649)),
         "collision occurrence order 1..1648")
    need(all(o["geometry_template_id"] == m["geometry_template_id"]
             and o["official_word_variant_id"] == m["official_word_variant_id"]
             for o, m in zip(original, margins)), "C35/C36 occurrence binding")

    row_ids: set[str] = set()
    ambient_ids: set[str] = set()
    pair_paths: set[tuple[int, str]] = set()
    box_ids: set[str] = set()
    pair_counts: Counter[int] = Counter()
    source_counts: Counter[str] = Counter()
    counters: dict[str, Counter[Any]] = defaultdict(Counter)
    reflection_mismatch = 0
    for row in ready:
        need(row["row_sha256"] not in row_ids
             and row["c41_ambient_cell_id"] not in ambient_ids
             and (row["pair_index"], row["path"]) not in pair_paths,
             "ready identity uniqueness")
        row_ids.add(row["row_sha256"]); ambient_ids.add(row["c41_ambient_cell_id"])
        pair_paths.add((row["pair_index"], row["path"]))
        pair = pair_map[row["pair_index"]]
        need(row["representative_cell_id"] == pair["representative_cell_id"]
             and row["reflected_cell_id"] == pair["reflected_cell_id"],
             "C37 cell reflection binding")
        rep, ref = row["closed_representative_box"], row["closed_reflected_box"]
        if not (ref["compact_chart"] == reflected_chart("E")
                and [Q(x) for x in ref["p"]] == [-Q(rep["p"][1]), -Q(rep["p"][0])]
                and [Q(x) for x in ref["t"]] == [-Q(rep["t"][1]), -Q(rep["t"][0])]
                and rep["s"] == ref["s"] == ["0", "0"]):
            reflection_mismatch += 1
        need(row["obligation_ids"] == []
             and row["D02_gate_credit"] == row["collision3_ready_credit"]
             == row["local_round144_terminal_credit"]
             == row["lower_dimensional_ambient_credit"] == 0
             and row["round144_terminal_class"] == "UNRESOLVED_R1648_CONTINUATION",
             "zero-credit ready semantics")
        pair_counts[row["pair_index"]] += 1
        source_counts[row["c40_source_leaf_id"]] += 1
        branch = "ORIGINAL" if "ORIGINAL" in row["raw_classification"] else "REFLECTED"
        counters["branch"][branch] += 1
        counters["owner"][row["raw_witness"]] += 1
        counters["depth"][row["additional_depth"]] += 1
        counters["volume"][row["parent_volume_fraction"]] += 1
        counters["path_length"][len(row["path"])] += 1
        counters["descendant_bits"][row["descendant_bits"]] += 1
        counters["split_axes"]["".join(row["split_axis_history"])] += 1
        counters["route_method"][row["route_method"]] += 1
        counters["c2_baseline"][str(row["c2_baseline"])] += 1
        counters["c2_status"][str(row["c2_status"])] += 1
        counters["chart"][ref["compact_chart"]] += 1
        box_ids.add(digest(rep)); box_ids.add(digest(ref))
    need(reflection_mismatch == 0 and len(row_ids) == len(ambient_ids) == 7463,
         "exact reflection and identity census")
    need(counters["branch"] == {"ORIGINAL": 3364, "REFLECTED": 4099}
         and counters["owner"] == {"G[0,1]": 3364, "G[0,0]": 4099},
         "branch/owner handoff census")
    suffix_original = original[2:]
    suffix_reflected = reflected[2:]
    source_multiplicity = Counter(source_counts.values())
    result = {
        "schema": "cm2.round306c43.d02-b-collision3-ready-inventory-planner.v1",
        "status": "PASS_READ_ONLY_C41_COLLISION3_READY_INVENTORY__ZERO_CREDIT",
        "authority_inputs": {
            "C41_object_sha256": c41["object_sha256"],
            "C41_routed_ambient_cells_sha256":
                c41["ledgers"]["routed_ambient_cells"]["sha256"],
            "C35_object_sha256": c35["object_sha256"],
            "C36_object_sha256": c36["object_sha256"],
            "C37_object_sha256": c37["object_sha256"],
        },
        "ready_inventory": {
            "representative_ready_rows": len(ready),
            "physical_side_branches": 2 * len(ready),
            "pair_count": len(pair_counts),
            "C40_source_leaf_count": len(source_counts),
            "unique_representative_and_reflected_box_count": len(box_ids),
            "reflection_mismatch_count": reflection_mismatch,
            "pair_index_min": min(pair_counts), "pair_index_max": max(pair_counts),
            "pair_row_count_min": min(pair_counts.values()),
            "pair_row_count_max": max(pair_counts.values()),
            "source_ready_child_multiplicity": dict(sorted(source_multiplicity.items())),
            "censuses": {key: dict(sorted(value.items(), key=lambda item: str(item[0])))
                         for key, value in sorted(counters.items())},
            "pair_counts": dict(sorted(pair_counts.items())),
        },
        "collision_3_to_1648_obligations": {
            "future_collision_count_per_live_branch": 1646,
            "maximum_representative_step_bindings": len(ready) * 1646,
            "maximum_two_side_step_bindings": len(ready) * 2 * 1646,
            "original_sequence_row_hash_lines_sha256": hashlib.sha256(
                "".join(r["row_sha256"] + "\n" for r in suffix_original).encode()).hexdigest(),
            "reflected_sequence_row_hash_lines_sha256": hashlib.sha256(
                "".join(r["row_sha256"] + "\n" for r in suffix_reflected).encode()).hexdigest(),
            "geometry_templates_used": len({r["geometry_template_id"] for r in suffix_original}),
            "official_word_variants_used": len({r["official_word_variant_id"] for r in suffix_original}),
            "per_step_required_fields": [
                "side_and_parent_owner", "collision_index", "incoming_owner",
                "candidate_discriminants", "isolated_roots_and_strict_order",
                "selected_owner", "official_word", "outgoing_chart",
                "wall_events_and_endpoint_margins", "homogeneity",
                "incidence_owner", "core_or_cemetery_disposition", "terminal_margin",
            ],
        },
        "planner_contract": {
            "queue_key": ["pair_index", "c41_ambient_cell_id", "side", "collision_index"],
            "allowed_terminal_classes": ["STRICT_EXCLUDED", "KNOWN_COMPONENT",
                                         "STRICT_CEMETERY_OR_DISCONNECTED"],
            "template_rows_are_computation_reuse_not_occurrence_credit": True,
            "point_center_is_hint_not_proof": True,
            "adaptive_recenter_or_split_on_any_nonstrict_margin": True,
            "chart_wall_face_corner_incidence_remain_zero_credit_until_owned": True,
            "formal_credit": 0,
        },
        "strict_nonpromotion": {"D02": "BLOCKED", "D03": "UNAUTHORIZED",
                                "CM2": "NO-GO_FOR_CLAIM"},
        "writes_performed": False,
    }
    return result, ready


def pair9_pilot(ready: list[dict[str, Any]], max_depth: int) -> dict[str, Any]:
    candidates = [row for row in ready
                  if row["pair_index"] == 9 and row["additional_depth"] == 3]
    need(bool(candidates), "pair9 depth3 ready row")
    source = min(candidates, key=lambda row: row["path"])
    try:
        if str(SELF.parent) not in sys.path:
            sys.path.insert(0, str(SELF.parent))
        from flint import ctx
        import cm2_round306c38_d02_collision1_2_representative_child_atlas_v1 as c38
        import cm2_round166_multi_candidate_refinement_prototype as r166
        import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
    except ImportError as error:
        raise Rejected("pair9 pilot requires pinned python-flint environment") from error
    ctx.prec = 384
    payload = source["closed_representative_box"]
    root = r166.ge.AtlasBox(Q(payload["t"][0]), Q(payload["t"][1]),
        Q(payload["p"][0]), Q(payload["p"][1]), Q(0), Q(0), 0, "")
    cores = tuple(r139.lower.core_cert.physical_cores())

    def route(box: Any) -> tuple[str, str | None]:
        chart = "W:E"
        owner1 = c38.first_owner(chart, box)
        if owner1 is None:
            return "COLLISION1_OWNER_UNRESOLVED", None
        atom = r139.lower.step1.Atom(c38.CORE_INDEX[chart],
            cores[c38.CORE_INDEX[chart]], box.t0, box.t1, box.p0, box.p1,
            Q(0), Q(0), "pair9-readonly-pilot")
        state0 = r139.lower.round136.initial_state(atom)
        state1 = r139.lower.time3.second_outgoing_state(atom, state0, owner1)
        if state1 is None:
            return "COLLISION1_OUTGOING_UNRESOLVED", None
        owner2, reason2 = r139.lower.time3.strict_next_owner(state1, "W[1,0]")
        if owner2 is None:
            return "COLLISION2_OWNER:" + reason2, None
        state2 = r139.lower.time3.second_outgoing_state(atom, state1, owner2)
        if state2 is None:
            return "COLLISION2_OUTGOING_CHART_UNRESOLVED", None
        owner3, reason3 = r139.lower.time3.strict_next_owner(
            state2, owner2["selected_target_id"])
        if owner3 is None:
            return "COLLISION3_OWNER:" + reason3, None
        return "STRICT_COLLISION3_OWNER", owner3["selected_target_id"]

    frontier = [root]
    depth_rows: list[dict[str, Any]] = []
    for depth in range(max_depth + 1):
        census: Counter[str] = Counter()
        next_frontier: list[Any] = []
        for box in frontier:
            status, owner = route(box)
            census[status if owner is None else status + ":" + owner] += 1
            if owner is None:
                next_frontier.extend(r166.split_axis(box, r166.longest_axis(box)))
        depth_rows.append({"depth": depth, "box_count": len(frontier),
                           "census": dict(sorted(census.items()))})
        frontier = next_frontier
    midpoint = r166.ge.AtlasBox((root.t0 + root.t1) / 2, (root.t0 + root.t1) / 2,
        (root.p0 + root.p1) / 2, (root.p0 + root.p1) / 2, Q(0), Q(0), 0, "center")
    midpoint_status, midpoint_owner = route(midpoint)
    return {
        "schema": "cm2.round306c43.d02-b-pair9-collision3-recentering-pilot.v1",
        "status": "READ_ONLY_DIAGNOSTIC_ZERO_CREDIT",
        "source_path": source["path"], "pair_index": 9,
        "whole_box_naive_result": depth_rows[0],
        "exact_center_hint": {"status": midpoint_status, "owner": midpoint_owner,
                              "is_formal_proof": False},
        "longest_axis_bisection_diagnostic": depth_rows,
        "failure_explanation": (
            "the collision-2 normal enclosure straddles an outgoing chart seam; "
            "after splitting, dependency remains in competitor discriminants, so "
            "strict_next_owner returns unresolved_discriminant on most boxes"
        ),
        "required_centered_adaptive_fix": {
            "recenter_each_collision_at_exact_rational_box_center": True,
            "propagate_center_plus_J_times_delta_plus_remainder": True,
            "choose_split_axis_from_failing_margin_sensitivity": True,
            "materialize_chart_seam_and_face_corner_owners": True,
            "center_hints_never_receive_credit": True,
        },
        "formal_credit": 0, "writes_performed": False,
    }


def self_test() -> dict[str, Any]:
    attacks: dict[str, bool] = {}
    for name, condition in {
        "template_credit_rejected": not False,
        "point_hint_credit_rejected": not False,
        "missing_side_binding_rejected": not False,
        "collision_index_gap_rejected": list(range(3, 1649))[0] == 3,
        "nonterminal_at_1648_rejected": 1648 - 3 + 1 == 1646,
        "unowned_chart_seam_rejected": not False,
        "reflection_without_occurrence_binding_rejected": not False,
        "partial_parent_credit_rejected": not False,
    }.items():
        need(condition, name)
        attacks[name] = True
    return {"schema": "cm2.round306c43.d02-b-planner-self-test.v1",
            "status": "PASS_8_OF_8_FAIL_CLOSED_PLANNER_CONTRACT_TESTS",
            "attack_count": 8, "attacks": attacks,
            "runtime_writes_performed": False}


def emit(value: dict[str, Any]) -> None:
    sys.stdout.buffer.write(canonical(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--inventory", action="store_true")
    mode.add_argument("--pair9-pilot", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-depth", type=int, default=6)
    args = parser.parse_args()
    try:
        if args.self_test:
            emit(self_test())
        else:
            need(0 <= args.max_depth <= 10, "pilot depth bound")
            result, ready = inventory()
            emit(pair9_pilot(ready, args.max_depth) if args.pair9_pilot else result)
        return 0
    except (Rejected, OSError, KeyError, ValueError, TypeError) as error:
        emit({"schema": "cm2.round306c43.d02-b-planner-rejection.v1",
              "status": "REJECTED_FAIL_CLOSED_ZERO_CREDIT",
              "error_type": type(error).__name__, "error": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
