#!/usr/bin/env python3
"""Independent verifier for the Round212 source-W seam promotion.

The producer is pinned and parsed as inert bytes but is never imported or
executed.  Before loading the certificate this verifier independently
replays the 26 seam-composite upper candidates and reconstructs their target
closure summaries and half-open source-chart transfers.  Certificate
acceptance is row-complete and fail-closed.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib
import json
import os
import stat
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

PREFIX = "cm2_round212_source_w_half_open_source_seam_promotion"
PRODUCER = f"{PREFIX}.py"
PRODUCER_SHA256 = (
    "dae73423b0db54987a23121197764feb3fee4c32763cf7a4b9e2275b7d5a6485"
)
CERTIFICATE = f"{PREFIX}_certificate.json"
CERTIFICATE_SHA256 = (
    "70ad8ce31edba0d0a8b082d72ba5f191224193c683ee49181213119f762a18e9"
)
CERTIFICATE_RESULT_SHA256 = (
    "a4e6e44aa55eedd376f5dd5d01a82f5c8dfae19ebb433dfb0017d07718004c7d"
)
VERIFICATION = f"{PREFIX}_verification.json"
CERTIFICATE_SCHEMA = "cm2.round212.source-w-half-open-source-seam-promotion.v1"
VERIFICATION_SCHEMA = (
    "cm2.round212.source-w-half-open-source-seam-promotion.verification.v1"
)

R201_PREFIX = "cm2_round201_source_w_exact_behind_formal_promotion"
R201_MANIFEST = f"{R201_PREFIX}_manifest.sha256"
R201_MANIFEST_SHA256 = (
    "ba2aec704c8d8966267bf47f16b9840140df3d35074d0ec73a2807213baa6547"
)
R201_PINS = {
    f"{R201_PREFIX}.py":
        "f7e53607d9a2c6b2f4fda76c9a6a92845f12cced04e28168f227cb516a1f4010",
    f"{R201_PREFIX}_certificate.json":
        "72b9f2959f362a7918bf628989faf2f0f5ed295fc3e28a305b727ff4ed216536",
    f"{R201_PREFIX}_verifier.py":
        "29344dd3c0590ac9d0d3f0618a3f0f034316759468e15af2674813ab72f7ce2b",
    f"{R201_PREFIX}_verification.json":
        "6361e38dd01892f8df164a0d8b58a5b7fe1741a9d61cb0727618a76e63759c1a",
    f"{R201_PREFIX}_report.md":
        "9e8e1f3619e035811a091ce9f9e663634fd00863c12d9bc91c8b623044c62c79",
    f"{R201_PREFIX}_cold_replay.md":
        "b8c06ac18087a33a94f0191bf88529365b44bafcdf66eba97e4772dd6cc1df68",
}
R201_VERIFIER = f"{R201_PREFIX}_verifier.py"
R201_VERIFIER_MODULE = R201_VERIFIER[:-3]
R201_VERIFICATION_RESULT_SHA256 = (
    "7b4e95f87a75fa3a02b925f202b156947c27b08c77a3c1e704a6b7625a2c8f8d"
)
ALL_SEAM_SHA256 = (
    "ed624beb47da60b591ae1f60086677ebecfdacb4da63cece4a8969680f22c31b"
)
PROMOTED_SHA256 = (
    "74bc6aba8c3eebc4ca276a87036c9752e1356da9ead8b66241dda6b09f842554"
)
RESIDUAL_KEYS = [
    "W:N:07.00.11111011",
    "W:S:H.07.00.11111011",
]


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("ascii")).hexdigest()


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def regular_bytes(path: Path, maximum: int | None = None) -> bytes:
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode), f"regular:{path.name}")
    require(not path.is_symlink(), f"not symlink:{path.name}")
    require(info.st_nlink == 1, f"single link:{path.name}")
    if maximum is not None:
        require(info.st_size <= maximum, f"bounded:{path.name}")
    return path.read_bytes()


def strict_decode(raw: bytes, label: str) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf"), f"BOM:{label}")
    require(b"\x00" not in raw, f"NUL:{label}")

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in values:
            require(key not in out, f"duplicate:{label}:{key}")
            out[key] = value
        return out

    value = json.loads(
        raw.decode("utf-8", "strict"),
        object_pairs_hook=pairs,
        parse_float=lambda _x: (_ for _ in ()).throw(
            RuntimeError(f"float:{label}")
        ),
        parse_constant=lambda _x: (_ for _ in ()).throw(
            RuntimeError(f"constant:{label}")
        ),
    )
    require(isinstance(value, dict), f"object:{label}")
    require(pretty_bytes(value) == raw, f"canonical:{label}")
    return value


def strict_file(path: Path, maximum: int) -> dict[str, Any]:
    return strict_decode(regular_bytes(path, maximum), path.name)


def check_frozen_inputs() -> dict[str, Any]:
    producer_raw = regular_bytes(HERE / PRODUCER, 2 * 1024 * 1024)
    require(
        hashlib.sha256(producer_raw).hexdigest() == PRODUCER_SHA256,
        "producer inert pin",
    )
    ast.parse(producer_raw.decode("utf-8"))
    require(
        PREFIX not in sys.modules,
        "producer module absent before reconstruction",
    )
    require(
        sha256_file(HERE / R201_MANIFEST) == R201_MANIFEST_SHA256,
        "Round201 manifest pin",
    )
    parsed: dict[str, str] = {}
    for line in regular_bytes(HERE / R201_MANIFEST, 4096).decode().splitlines():
        value, name = line.split("  ", 1)
        parsed[name] = value
    require(parsed == R201_PINS, "Round201 exact manifest")
    for name, value in R201_PINS.items():
        require(sha256_file(HERE / name) == value, f"Round201 pin:{name}")
    verification = strict_file(
        HERE / f"{R201_PREFIX}_verification.json", 16 * 1024 * 1024
    )
    require(
        verification["result_sha256"] == R201_VERIFICATION_RESULT_SHA256
        and digest(verification["result"])
        == R201_VERIFICATION_RESULT_SHA256
        and verification["result"]["verdict"] == "PASS"
        and verification["result"]["full_expected_canonical_equality"]
        and verification["result"]["verified_census"][
            "combined_whole_record_excluded"
        ] == 74_558
        and verification["result"]["verified_census"][
            "combined_conservative_live"
        ] == 2_274,
        "Round201 verified base",
    )
    return {
        "producer_sha256": PRODUCER_SHA256,
        "producer_treated_as_inert_bytes": True,
        "producer_imported_or_executed": False,
        "Round201_manifest_sha256": R201_MANIFEST_SHA256,
        "Round201_manifest_entries_replayed": True,
        "Round201_verification_result_sha256":
            R201_VERIFICATION_RESULT_SHA256,
    }


def counter_map(value: Counter[Any]) -> dict[str, int]:
    return {
        str(key): value[key]
        for key in sorted(value, key=lambda item: str(item))
    }


def independent_source_partition(cell: str, box: Any) -> dict[str, Any]:
    require(cell in {"E", "N", "S"}, f"cell:{cell}")
    neg = bool(box.t1 < 0)
    require(neg or bool(box.t0 > 0), "one sign")
    if neg:
        require(
            2 * box.t0 * box.t0 > 1 > 2 * box.t1 * box.t1,
            "negative exact square bracket",
        )
        sign = "NEGATIVE"
    else:
        require(
            2 * box.t0 * box.t0 < 1 < 2 * box.t1 * box.t1,
            "positive exact square bracket",
        )
        sign = "POSITIVE"
    adjacent = {
        "E": {"NEGATIVE": "S", "POSITIVE": "N"},
        "N": {"NEGATIVE": "W", "POSITIVE": "E"},
        "S": {"NEGATIVE": "W", "POSITIVE": "E"},
    }[cell][sign]
    negative_transfer = cell == "S"
    jacobian_on_seam = (
        -1
        if (negative_transfer and neg) or (not negative_transfer and not neg)
        else 1
    )
    owner = "W" if cell in {"N", "S"} and neg else "E"
    owns = cell == owner
    require(owns == (cell == "E"), "horizontal ownership")
    return {
        "source_chart": cell,
        "source_t_sign": sign,
        "exact_parent_t_interval": [str(box.t0), str(box.t1)],
        "exact_seam_equation": "2*t_source^2=1",
        "unique_selected_seam": "-1/sqrt(2)" if neg else "+1/sqrt(2)",
        "strict_bracket_proved_by_exact_rational_squares": True,
        "physical_chart_interior_open_3D_predicate": "2*t_source^2<1",
        "source_seam_2D_predicate": "2*t_source^2=1",
        "guard_recoordination_open_3D_predicate": "2*t_source^2>1",
        "horizontal_E_or_W_chart_owns_equality": True,
        "source_seam_half_open_owner": owner,
        "original_chart_owns_source_seam": owns,
        "original_chart_owned_physical_parent_predicate":
            "2*t_source^2<=1" if owns else "2*t_source^2<1",
        "adjacent_coordinate_chart": adjacent,
        "exact_rechart": {
            "t_coordinate": (
                "t_adjacent=-sqrt(1-t_source^2)"
                if negative_transfer
                else "t_adjacent=sqrt(1-t_source^2)"
            ),
            "p_adjacent": "p_source",
            "s_adjacent": "s_source",
            "Jacobian_determinant": (
                "t_source/sqrt(1-t_source^2)"
                if negative_transfer
                else "-t_source/sqrt(1-t_source^2)"
            ),
            "Jacobian_strictly_nonzero_on_open_guard_slice": True,
            "Jacobian_on_selected_seam": str(jacobian_on_seam),
            "same_physical_normal_position_velocity_and_s": True,
        },
        "chart_owned_part_seam_and_guard_are_disjoint": True,
        "chart_owned_part_plus_seam_plus_guard_is_complete": True,
        "seam_counted_once": True,
        "open_guard_slice_counted_once_in_adjacent_chart": True,
        "guard_outside_exterior_credit": 0,
        "source_seam_lower_dimensional_integer_credit": 0,
    }


def independent_box_row(w: Any, box: Any) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "ambient_dimension": 3,
        "exact_coordinate_volume": str(w.box_volume(box)),
    }


def independent_pure_summary(
    w: Any,
    origin: str,
    roots: list[Any],
    refinement: dict[str, Any],
    final_rows: list[Any],
) -> dict[str, Any]:
    volumes = {row.key: w.box_volume(row.box) for row in roots}
    inherited = [
        w.wrap_round180_terminal(origin, row, volumes)
        for row in refinement["terminal_rows"]
    ]
    terminals = list(inherited)
    methods: Counter[str] = Counter()
    extra_faces: list[dict[str, Any]] = []
    for initial in final_rows:
        proof, reason = w.clipped_partition_proof(initial)
        if proof is not None:
            terminals.append(w.wrap_clipped_terminal(
                initial,
                proof,
                "ROUND212_REBUILT_ROUND184_CLIPPED_DELTA_THREE_STRATUM",
            ))
            methods["CLIPPED_DELTA_THREE_STRATUM"] += 1
            continue
        require(reason == w.TARGET_FAILURE, f"pure initial reason:{origin}")
        stack = [(initial, 0)]
        while stack:
            row, depth = stack.pop()
            direct, direct_evidence = w.direct_strict_terminal(row)
            if direct == "EXCLUDED":
                item = {
                    "cell_key": row.key,
                    "origin_key": origin,
                    "method": "DEPTH2_DIRECT_STRICT_CLOSED_BOX",
                    **w.box_evidence(row),
                    "coarse_disposition": "EXCLUDED",
                    "direct_evidence": direct_evidence,
                    "whole_closed_cell_excluded": True,
                }
                item["row_sha256"] = digest(item)
                terminals.append(item)
                methods["DEPTH2_DIRECT_STRICT_CLOSED_BOX"] += 1
                continue
            proof2, reason2 = (
                (None, f"DIRECT_STRICT_{direct}")
                if direct is not None
                else w.clipped_partition_proof(row)
            )
            if proof2 is not None:
                terminals.append(w.wrap_clipped_terminal(
                    row, proof2, "DEPTH2_CLIPPED_DELTA_THREE_STRATUM"
                ))
                methods["DEPTH2_CLIPPED_DELTA_THREE_STRATUM"] += 1
                continue
            if depth < 2:
                axis = w.r180.split_axis(row.box)
                low, high = w.r176.split(row.box, axis)
                extra_faces.append(w.r180.split_face(row, axis, low, high))
                stack.append((w.child_frontier(row, high), depth + 1))
                stack.append((w.child_frontier(row, low), depth + 1))
                continue
            require(
                reason2 in {w.TARGET_FAILURE, w.FULL_P_FAILURE},
                f"pure cutoff:{origin}:{row.key}",
            )
            exact = w.single_exact_behind_cell(
                row,
                (
                    "TARGET_FIRST_CLIPPED"
                    if reason2 == w.TARGET_FAILURE
                    else "FULL_P_FIRST_ROOT_EQUALITY"
                ),
            )
            require(exact["whole_closed_cell_excluded"], "exact excluded")
            terminals.append(exact)
            methods["DEPTH2_EXACT_BEHIND"] += 1
    terminals.sort(key=lambda row: row["cell_key"])
    input_volume = sum((w.box_volume(row.box) for row in roots), w.Q(0))
    output_volume = sum(
        (w.Q(row["exact_volume"]) for row in terminals), w.Q(0)
    )
    require(
        input_volume == output_volume
        and all(row["whole_closed_cell_excluded"] for row in terminals),
        f"pure target closure:{origin}",
    )
    faces = sorted(
        refinement["split_face_rows"] + extra_faces,
        key=lambda row: row["parent_cell_key"],
    )
    return {
        "priority_class": w.PURE_CLASS,
        "Round176_residual_root_count": len(roots),
        "Round180_final_cell_count": len(final_rows),
        "inherited_terminal_count": len(inherited),
        "rebuilt_terminal_count": len(terminals),
        "rebuilt_terminal_exact_volume": str(output_volume),
        "rebuilt_terminal_rows_sha256": digest(terminals),
        "new_terminal_count_by_method": counter_map(methods),
        "complete_split_face_count": len(faces),
        "complete_split_face_rows_sha256": digest(faces),
        "all_inherited_and_final_target_strata_excluded": True,
        "target_partition_count_and_exact_volume_conserved": True,
    }


def independent_generalized_summary(
    w: Any,
    origin: str,
    roots: list[Any],
    refinement: dict[str, Any],
    final_rows: list[Any],
    priority_class: str,
) -> dict[str, Any]:
    volumes = {row.key: w.box_volume(row.box) for row in roots}
    inherited = [
        w.wrap_round180_terminal(origin, row, volumes)
        for row in refinement["terminal_rows"]
    ]
    evidence = [
        w.generalized_exact_behind_cell(
            row, w.r180.residual_category(row), priority_class
        )
        for row in final_rows
    ]
    inherited_ok = all(row["whole_closed_cell_excluded"] for row in inherited)
    final_ok = all(row["geometric_whole_cell_excluded"] for row in evidence)
    full_volume = sum((w.box_volume(row.box) for row in roots), w.Q(0))
    pieces = sum(
        (w.Q(row["exact_volume"]) for row in inherited), w.Q(0)
    ) + sum((w.box_volume(row.box) for row in final_rows), w.Q(0))
    require(full_volume == pieces, f"generalized volume:{origin}")
    dispositions = Counter(row["final_disposition"] for row in evidence)
    return {
        "priority_class": priority_class,
        "Round176_residual_root_count": len(roots),
        "Round180_final_cell_count": len(final_rows),
        "inherited_terminal_count": len(inherited),
        "inherited_terminal_rows_sha256": digest(inherited),
        "generalized_final_evidence_rows_sha256": digest(evidence),
        "final_disposition_count": counter_map(dispositions),
        "geometrically_excluded_final_cell_count": sum(
            row["geometric_whole_cell_excluded"] for row in evidence
        ),
        "complete_target_partition_exact_volume": str(full_volume),
        "all_inherited_target_strata_excluded": inherited_ok,
        "all_final_target_cells_excluded": final_ok,
        "all_inherited_and_final_target_strata_excluded":
            inherited_ok and final_ok,
        "target_partition_count_and_exact_volume_conserved": True,
    }


def reconstruct_facts() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    verifier_sha = sha256_file(HERE / R201_VERIFIER)
    require(verifier_sha == R201_PINS[R201_VERIFIER], "R201 verifier pre pin")
    w = importlib.import_module(R201_VERIFIER_MODULE)
    require(
        sha256_file(HERE / R201_VERIFIER) == verifier_sha,
        "R201 verifier post pin",
    )
    w.r180.check_chain()
    replay = w.r176.replay_frontier()
    kinds: defaultdict[str, set[str]] = defaultdict(set)
    kinds.update({key: set(value) for key, value in replay["origin_kinds"].items()})
    residuals: dict[str, list[Any]] = defaultdict(list)
    for item in replay["frontier"]:
        closed, _evidence = w.r176.closure(item)
        if closed is None:
            residuals[item.origin_key].append(item)
        else:
            kinds[item.origin_key].add(closed)
    for values in residuals.values():
        values.sort(key=lambda row: row.key)
    upper = sorted(key for key in residuals if kinds[key] <= {"EXCLUDED"})
    require(len(upper) == 1476, "independent upper count")
    seam_keys = sorted(
        key
        for key in upper
        if w.r176.physical_domain(
            replay["origins"][key]["chart_id"],
            replay["origins"][key]["box"],
        )["classification"] == w.SOURCE_SEAM
    )
    require(
        len(seam_keys) == 26 and digest(seam_keys) == ALL_SEAM_SHA256,
        "independent 26 seam set",
    )
    facts: dict[str, dict[str, Any]] = {}
    complete_keys: list[str] = []
    incomplete_keys: list[str] = []
    class_count: Counter[str] = Counter()
    target_final = 0
    target_inherited = 0
    target_objects = 0
    for key in seam_keys:
        roots = residuals[key]
        refinement = w.r180.refine_origin(roots, 4)
        final = refinement["final_residual_rows"]
        categories = Counter(w.r180.residual_category(row) for row in final)
        priority_class = w.support_class(categories)
        target = (
            independent_pure_summary(w, key, roots, refinement, final)
            if priority_class == w.PURE_CLASS
            else independent_generalized_summary(
                w, key, roots, refinement, final, priority_class
            )
        )
        complete = (
            target["all_inherited_and_final_target_strata_excluded"]
            and priority_class != w.COMPACT_CLASS
        )
        meta = replay["origins"][key]
        cell = meta["chart_id"].split(":")[1]
        facts[key] = {
            "original_chart_id": meta["chart_id"],
            "original_parent_box": independent_box_row(w, meta["box"]),
            "priority_class": priority_class,
            "target_closure": target,
            "source_half_open_partition":
                independent_source_partition(cell, meta["box"]),
            "complete": complete,
        }
        (complete_keys if complete else incomplete_keys).append(key)
        class_count[priority_class] += 1
        target_final += target["Round180_final_cell_count"]
        target_inherited += target["inherited_terminal_count"]
        target_objects += (
            target.get("rebuilt_terminal_count")
            if priority_class == w.PURE_CLASS
            else target["Round180_final_cell_count"]
            + target["inherited_terminal_count"]
        )
    require(
        len(complete_keys) == 24
        and digest(complete_keys) == PROMOTED_SHA256
        and incomplete_keys == RESIDUAL_KEYS
        and all(
            facts[key]["target_closure"]["final_disposition_count"]
            == {
                "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH": 72,
                "UNRESOLVED": 72,
            }
            for key in RESIDUAL_KEYS
        ),
        "independent 24/2 target partition and 2x72 residual",
    )
    return facts, {
        "upper_count": len(upper),
        "seam_keys": seam_keys,
        "complete_keys": complete_keys,
        "incomplete_keys": incomplete_keys,
        "class_count": class_count,
        "target_final": target_final,
        "target_inherited": target_inherited,
        "target_objects": target_objects,
    }


def validate_result(
    result: dict[str, Any],
    facts: dict[str, dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    ledger = result["whole_origin_ledger"]
    rows = ledger["per_origin_rows"]
    require(len(rows) == 26, "26 certificate rows")
    require(
        ledger["per_origin_rows_sha256"] == digest(rows),
        "row ledger digest",
    )
    require(
        [row["origin_key"] for row in rows] == summary["seam_keys"],
        "exact ordered 26 keys",
    )
    for row in rows:
        key = row["origin_key"]
        expected = facts[key]
        require(
            row["row_sha256"]
            == digest({k: v for k, v in row.items() if k != "row_sha256"}),
            f"row self digest:{key}",
        )
        for field in (
            "original_chart_id",
            "original_parent_box",
            "priority_class",
            "target_closure",
            "source_half_open_partition",
        ):
            require(row[field] == expected[field], f"row field:{key}:{field}")
        complete = expected["complete"]
        require(
            row["complete_target_partition"] is complete
            and row["physical_source_partition_complete"] is True
            and row["whole_original_chart_owned_physical_parent_excluded"]
            is complete
            and row["whole_origin_integer_credit"] == (1 if complete else 0)
            and row["child_cell_count_used_as_integer_credit"] is False
            and row["two_one_zero_dimensional_count_used_as_integer_credit"]
            is False
            and row["guard_recoordination_used_as_exterior_credit"] is False
            and row["source_seam_used_as_separate_integer_credit"] is False,
            f"credit semantics:{key}",
        )
    require(
        ledger["promoted_whole_origin_count"] == 24
        and ledger["promoted_whole_origin_keys"] == summary["complete_keys"]
        and ledger["promoted_whole_origin_keys_sha256"] == PROMOTED_SHA256
        and ledger["retained_target_incomplete_source_seam_count"] == 2
        and ledger["retained_target_incomplete_source_seam_keys"]
        == RESIDUAL_KEYS
        and ledger["retained_target_incomplete_source_seam_keys_sha256"]
        == digest(RESIDUAL_KEYS),
        "exact 24/2 certificate partition",
    )
    target = result["independent_target_replay"]
    require(
        target["upper_candidate_count"] == 1476
        and target["all_source_seam_candidate_count"] == 26
        and target["all_source_seam_candidate_keys_sha256"]
        == ALL_SEAM_SHA256
        and target["priority_class_count"]
        == counter_map(summary["class_count"])
        and target["Round180_final_cell_count"] == summary["target_final"]
        and target["inherited_terminal_count"] == summary["target_inherited"]
        and target["rebuilt_target_proof_object_count"]
        == summary["target_objects"],
        "target replay census",
    )
    source = result["source_half_open_partition"]
    require(
        source["promoted_origin_count_by_original_chart"]
        == {"E": 6, "N": 9, "S": 9}
        and source["promoted_origin_count_by_source_t_sign"]
        == {"NEGATIVE": 15, "POSITIVE": 9}
        and source["promoted_source_seam_owner_count"] == {"E": 12, "W": 12}
        and source["promoted_guard_adjacent_chart_count"]
        == {"E": 6, "N": 3, "S": 3, "W": 12}
        and source["open_guard_rechart_Jacobians_all_nonzero"] is True
        and source["source_seams_counted_once"] is True
        and source["open_guard_slices_counted_once"] is True
        and source["guard_outside_exterior_credit"] == 0
        and source["source_seam_lower_dimensional_integer_credit"] == 0,
        "source ownership and rechart census",
    )
    composition = result["ledger_composition"]
    require(
        composition["Round201_whole_record_excluded"] == 74_558
        and composition["Round201_conservative_live"] == 2_274
        and composition["new_whole_origin_credit"] == 24
        and composition["combined_whole_record_excluded"] == 74_582
        and composition["combined_conservative_live"] == 2_250
        and composition["refined_source_W_total"] == 76_832
        and composition["exact_integer_conservation"] is True
        and composition["Round201_remaining_priority_origins"] == 278
        and composition["remaining_priority_origins"] == 254
        and composition["remaining_priority_partition"]
        == {"compact_q_origins": 54, "incomplete_mixed_origins": 200},
        "74582/2250 ledger and 254 residual",
    )
    require(
        result["strict_nonpromotion"]
        == {
            "CM2": "NO-GO_FOR_CLAIM",
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
        },
        "global nonpromotion",
    )


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def semantic_attacks(
    certificate: dict[str, Any],
    facts: dict[str, dict[str, Any]],
    summary: dict[str, Any],
) -> list[str]:
    attacks: list[tuple[str, Any]] = []

    def add(name: str, mutate: Any) -> None:
        altered = copy.deepcopy(certificate)
        mutate(altered["result"])
        resign(altered)
        attacks.append((name, altered))

    def mutate_origin(
        result: dict[str, Any],
        origin: str,
        mutate: Any,
    ) -> None:
        row = next(
            item for item in result["whole_origin_ledger"]["per_origin_rows"]
            if item["origin_key"] == origin
        )
        mutate(row)
        row["row_sha256"] = digest(
            {key: value for key, value in row.items() if key != "row_sha256"}
        )
        result["whole_origin_ledger"]["per_origin_rows_sha256"] = digest(
            result["whole_origin_ledger"]["per_origin_rows"]
        )

    def promote_residual(result: dict[str, Any]) -> None:
        mutate_origin(
            result,
            RESIDUAL_KEYS[0],
            lambda row: (
                row.__setitem__("whole_origin_integer_credit", 1),
                row.__setitem__("complete_target_partition", True),
            ),
        )

    add("promote first 72-unresolved residual", promote_residual)
    add(
        "duplicate one of 24 promoted keys",
        lambda r: r["whole_origin_ledger"]["promoted_whole_origin_keys"].
        append(r["whole_origin_ledger"]["promoted_whole_origin_keys"][0]),
    )
    add(
        "omit one of 24 promoted keys",
        lambda r: r["whole_origin_ledger"]["promoted_whole_origin_keys"].pop(),
    )
    add(
        "forge excluded ledger 74583",
        lambda r: r["ledger_composition"].__setitem__(
            "combined_whole_record_excluded", 74_583
        ),
    )
    add(
        "forge live ledger 2249",
        lambda r: r["ledger_composition"].__setitem__(
            "combined_conservative_live", 2_249
        ),
    )
    add(
        "change half-open seam owner",
        lambda r: mutate_origin(
            r,
            summary["seam_keys"][0],
            lambda row: row["source_half_open_partition"].__setitem__(
                "source_seam_half_open_owner", "W"
            ),
        ),
    )
    add(
        "change adjacent guard chart",
        lambda r: mutate_origin(
            r,
            summary["seam_keys"][0],
            lambda row: row["source_half_open_partition"].__setitem__(
                "adjacent_coordinate_chart", "W"
            ),
        ),
    )
    add(
        "zero guard rechart Jacobian",
        lambda r: mutate_origin(
            r,
            summary["seam_keys"][0],
            lambda row: row["source_half_open_partition"][
                "exact_rechart"
            ].__setitem__("Jacobian_determinant", "0"),
        ),
    )
    add(
        "grant guard exterior credit",
        lambda r: r["source_half_open_partition"].__setitem__(
            "guard_outside_exterior_credit", 1
        ),
    )
    add(
        "grant seam lower-dimensional credit",
        lambda r: r["source_half_open_partition"].__setitem__(
            "source_seam_lower_dimensional_integer_credit", 1
        ),
    )
    add(
        "drop one of first residual 72 unresolved cells",
        lambda r: mutate_origin(
            r,
            RESIDUAL_KEYS[0],
            lambda row: row["target_closure"][
                "final_disposition_count"
            ].__setitem__("UNRESOLVED", 71),
        ),
    )
    add(
        "drop one of second residual 72 unresolved cells",
        lambda r: mutate_origin(
            r,
            RESIDUAL_KEYS[1],
            lambda row: row["target_closure"][
                "final_disposition_count"
            ].__setitem__("UNRESOLVED", 71),
        ),
    )
    add(
        "forge remaining priority 253",
        lambda r: r["ledger_composition"].__setitem__(
            "remaining_priority_origins", 253
        ),
    )
    add(
        "forge D02 closure",
        lambda r: r["strict_nonpromotion"].__setitem__("D02", "CLOSED"),
    )
    rejected: list[str] = []
    for name, altered in attacks:
        try:
            require(
                altered["result_sha256"] == digest(altered["result"]),
                f"attack resigned:{name}",
            )
            validate_result(altered["result"], facts, summary)
        except Exception:
            rejected.append(name)
    require(len(rejected) == len(attacks), "all semantic attacks rejected")
    return rejected


def json_attack_suite(certificate: dict[str, Any]) -> list[str]:
    raw = pretty_bytes(certificate)
    attacks = {
        "duplicate key": raw.replace(b'{\n  "result":', b'{\n  "schema": "x",\n  "result":', 1),
        "float": raw.replace(b'"new_whole_origin_credit": 24', b'"new_whole_origin_credit": 24.0', 1),
        "NaN": raw.replace(b'"new_whole_origin_credit": 24', b'"new_whole_origin_credit": NaN', 1),
        "BOM": b"\xef\xbb\xbf" + raw,
        "NUL": raw + b"\x00",
        "top array": b"[]\n",
        "trailing document": raw + b"{}\n",
        "noncanonical compact": canonical(certificate).encode() + b"\n",
    }
    rejected = []
    for name, payload in attacks.items():
        try:
            strict_decode(payload, name)
        except Exception:
            rejected.append(name)
    require(len(rejected) == len(attacks), "all JSON attacks rejected")
    return rejected


def path_allowed(path: Path, allowed_name: str) -> bool:
    try:
        parent = path.parent.resolve(strict=True)
    except OSError:
        return False
    if (
        parent != HERE.resolve()
        or path.parent.absolute() != HERE.resolve()
        or path.name != allowed_name
    ):
        return False
    if path.exists() or path.is_symlink():
        try:
            info = path.lstat()
        except OSError:
            return False
        return (
            stat.S_ISREG(info.st_mode)
            and not path.is_symlink()
            and info.st_nlink == 1
        )
    return True


def output_allowed(path: Path) -> bool:
    return path_allowed(path, VERIFICATION)


def path_attack_suite() -> list[str]:
    token = f"{os.getpid()}_{id(object())}"
    target = HERE / f".cm2_round212_path_target_{token}"
    symlink = HERE / f".cm2_round212_path_symlink_{token}"
    hardlink = HERE / f".cm2_round212_path_hardlink_{token}"
    directory = HERE / f".cm2_round212_path_directory_{token}"
    fifo = HERE / f".cm2_round212_path_fifo_{token}"
    alias = HERE / f".cm2_round212_path_parent_alias_{token}"
    nested = directory / VERIFICATION
    created: list[Path] = []
    try:
        target.write_bytes(b"round212-path-probe\n")
        created.append(target)
        symlink.symlink_to(target.name)
        created.append(symlink)
        os.link(target, hardlink)
        created.append(hardlink)
        directory.mkdir()
        created.append(directory)
        os.mkfifo(fifo)
        created.append(fifo)
        alias.symlink_to(HERE, target_is_directory=True)
        created.append(alias)
        attacks = {
            "symlink output": not path_allowed(symlink, symlink.name),
            "hardlink output": not path_allowed(hardlink, hardlink.name),
            "directory output": not path_allowed(directory, directory.name),
            "FIFO output": not path_allowed(fifo, fifo.name),
            "nested output": not output_allowed(nested),
            "parent escape": not output_allowed(
                HERE.parent / VERIFICATION
            ),
            "symlink parent alias": not output_allowed(alias / VERIFICATION),
            "producer protected": not output_allowed(HERE / PRODUCER),
            "certificate protected": not output_allowed(HERE / CERTIFICATE),
            "Round201 verifier protected":
                not output_allowed(HERE / R201_VERIFIER),
        }
        rejected = [name for name, passed in attacks.items() if passed]
        require(len(rejected) == len(attacks), "all path attacks rejected")
        return rejected
    finally:
        for path in reversed(created):
            try:
                if path.is_dir() and not path.is_symlink():
                    path.rmdir()
                else:
                    path.unlink()
            except FileNotFoundError:
                pass


def atomic_write(path: Path, payload: bytes) -> None:
    require(output_allowed(path), "authorized verification output")
    fd, name = tempfile.mkstemp(
        prefix=".cm2_round212_verification_", suffix=".tmp", dir=HERE
    )
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(HERE, os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / CERTIFICATE)
    parser.add_argument("--output", type=Path, default=HERE / VERIFICATION)
    args = parser.parse_args()
    frozen = check_frozen_inputs()
    facts, summary = reconstruct_facts()
    require(
        PREFIX not in sys.modules,
        "producer module absent after reconstruction",
    )
    certificate_raw = regular_bytes(args.certificate, 16 * 1024 * 1024)
    require(
        hashlib.sha256(certificate_raw).hexdigest() == CERTIFICATE_SHA256,
        "certificate file pin",
    )
    certificate = strict_decode(certificate_raw, CERTIFICATE)
    require(
        certificate["schema"] == CERTIFICATE_SCHEMA
        and certificate["result_sha256"] == CERTIFICATE_RESULT_SHA256
        and digest(certificate["result"]) == CERTIFICATE_RESULT_SHA256,
        "certificate canonical result pin",
    )
    validate_result(certificate["result"], facts, summary)
    semantic = semantic_attacks(certificate, facts, summary)
    json_attacks = json_attack_suite(certificate)
    path_attacks = path_attack_suite()
    result = {
        "status": "PASS_FORMAL_ROUND212",
        "verdict": "PASS",
        "producer_sha256": PRODUCER_SHA256,
        "certificate_file_sha256": CERTIFICATE_SHA256,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "independence_contract": {
            **frozen,
            "certificate_loaded_only_after_26_seam_facts_rebuilt": True,
            "producer_module_absent_after_reconstruction": True,
            "shared_pinned_Round201_target_kernels_disclosed": True,
            "implementation_diverse_target_geometry_claimed": False,
            "source_partition_independently_implemented": True,
            "complete_per_origin_semantic_validation": True,
        },
        "verified_census": {
            "upper_candidates": summary["upper_count"],
            "source_seam_composite_origins": len(summary["seam_keys"]),
            "promoted_whole_origins": len(summary["complete_keys"]),
            "retained_target_incomplete_seam_origins":
                len(summary["incomplete_keys"]),
            "retained_unresolved_cells_per_incomplete_origin": [72, 72],
            "combined_whole_record_excluded": 74_582,
            "combined_conservative_live": 2_250,
            "remaining_priority_origins": 254,
        },
        "semantic_attack_suite": {
            "attack_count": len(semantic),
            "rejected_count": len(semantic),
            "all_rejected": True,
            "attack_names": semantic,
            "every_attack_result_digest_recomputed": True,
        },
        "strict_JSON_attack_suite": {
            "attack_count": len(json_attacks),
            "rejected_count": len(json_attacks),
            "all_rejected": True,
            "attack_names": json_attacks,
        },
        "path_type_output_attack_suite": {
            "attack_count": len(path_attacks),
            "rejected_count": len(path_attacks),
            "all_rejected": True,
            "attack_names": path_attacks,
            "real_protected_files_modified": False,
            "symlink_parent_alias_rejected": True,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    document = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    atomic_write(args.output, pretty_bytes(document))
    print(digest(result))


if __name__ == "__main__":
    main()
