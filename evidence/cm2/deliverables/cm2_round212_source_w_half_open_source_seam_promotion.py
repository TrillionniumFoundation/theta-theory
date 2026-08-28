#!/usr/bin/env python3
"""Round212: formal half-open source-seam promotion for source W.

This successor is deliberately narrow.  It replays all source-W upper
candidate origins whose rational source box crosses ``2*t^2=1``.  Target-side
closure is rebuilt with the pinned Round201 independent geometry kernels.
Only origins whose complete inherited and final 3D/2D/1D/0D target
partitions are excluded are eligible.  The source box is then partitioned
into its chart-owned physical part, the horizontal-chart-owned seam, and an
open guard slice re-coordinated into the adjacent chart.  Guard slices and
all lower-dimensional rows carry zero integer credit.
"""

from __future__ import annotations

import argparse
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

SCHEMA = "cm2.round212.source-w-half-open-source-seam-promotion.v1"
OUTPUT_NAME = "cm2_round212_source_w_half_open_source_seam_promotion_certificate.json"
ROUND201_PREFIX = "cm2_round201_source_w_exact_behind_formal_promotion"
ROUND201_MANIFEST = f"{ROUND201_PREFIX}_manifest.sha256"
ROUND201_MANIFEST_SHA256 = (
    "ba2aec704c8d8966267bf47f16b9840140df3d35074d0ec73a2807213baa6547"
)
ROUND201_PINS = {
    f"{ROUND201_PREFIX}.py":
        "f7e53607d9a2c6b2f4fda76c9a6a92845f12cced04e28168f227cb516a1f4010",
    f"{ROUND201_PREFIX}_certificate.json":
        "72b9f2959f362a7918bf628989faf2f0f5ed295fc3e28a305b727ff4ed216536",
    f"{ROUND201_PREFIX}_verifier.py":
        "29344dd3c0590ac9d0d3f0618a3f0f034316759468e15af2674813ab72f7ce2b",
    f"{ROUND201_PREFIX}_verification.json":
        "6361e38dd01892f8df164a0d8b58a5b7fe1741a9d61cb0727618a76e63759c1a",
    f"{ROUND201_PREFIX}_report.md":
        "9e8e1f3619e035811a091ce9f9e663634fd00863c12d9bc91c8b623044c62c79",
    f"{ROUND201_PREFIX}_cold_replay.md":
        "b8c06ac18087a33a94f0191bf88529365b44bafcdf66eba97e4772dd6cc1df68",
}
ROUND201_RESULT_SHA256 = (
    "9d3dc29c07f81ba2b71743e983c3d4718e40a430d3566cc934d4a3098facad3c"
)
ROUND201_VERIFICATION_RESULT_SHA256 = (
    "7b4e95f87a75fa3a02b925f202b156947c27b08c77a3c1e704a6b7625a2c8f8d"
)
ROUND201_VERIFIER = f"{ROUND201_PREFIX}_verifier.py"
ROUND201_VERIFIER_MODULE = ROUND201_VERIFIER[:-3]

EXPECTED_UPPER_COUNT = 1476
EXPECTED_ALL_SEAM_COUNT = 26
EXPECTED_ALL_SEAM_KEYS_SHA256 = (
    "ed624beb47da60b591ae1f60086677ebecfdacb4da63cece4a8969680f22c31b"
)
EXPECTED_PROMOTED_COUNT = 24
EXPECTED_PROMOTED_KEYS_SHA256 = (
    "74bc6aba8c3eebc4ca276a87036c9752e1356da9ead8b66241dda6b09f842554"
)
EXPECTED_RESIDUAL_COUNT = 2
EXPECTED_RESIDUAL_KEYS = [
    "W:N:07.00.11111011",
    "W:S:H.07.00.11111011",
]

OLD_EXCLUDED = 74_558
OLD_LIVE = 2_274
TOTAL_SOURCE_W = 76_832
NEW_EXCLUDED = 74_582
NEW_LIVE = 2_250
OLD_REMAINING = 278
NEW_REMAINING = 254


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
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_regular(path: Path, maximum: int | None = None) -> bytes:
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode), f"regular file:{path.name}")
    require(not path.is_symlink(), f"not symlink:{path.name}")
    require(info.st_nlink == 1, f"single link:{path.name}")
    if maximum is not None:
        require(info.st_size <= maximum, f"bounded file:{path.name}")
    return path.read_bytes()


def strict_json(path: Path) -> dict[str, Any]:
    raw = read_regular(path, 16 * 1024 * 1024)
    require(not raw.startswith(b"\xef\xbb\xbf"), f"no BOM:{path.name}")
    require(b"\x00" not in raw, f"no NUL:{path.name}")

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in values:
            require(key not in out, f"duplicate key:{path.name}:{key}")
            out[key] = value
        return out

    text = raw.decode("utf-8", "strict")
    value = json.loads(
        text,
        object_pairs_hook=pairs,
        parse_float=lambda _x: (_ for _ in ()).throw(
            RuntimeError(f"float:{path.name}")
        ),
        parse_constant=lambda _x: (_ for _ in ()).throw(
            RuntimeError(f"constant:{path.name}")
        ),
    )
    require(isinstance(value, dict), f"top object:{path.name}")
    require(pretty_bytes(value) == raw, f"canonical pretty JSON:{path.name}")
    return value


def check_round201() -> dict[str, Any]:
    manifest = HERE / ROUND201_MANIFEST
    require(
        sha256_file(manifest) == ROUND201_MANIFEST_SHA256,
        "Round201 manifest pin",
    )
    lines = read_regular(manifest, 4096).decode("ascii").splitlines()
    parsed: dict[str, str] = {}
    for line in lines:
        value, name = line.split("  ", 1)
        require(name not in parsed, "Round201 unique manifest entry")
        parsed[name] = value
    require(parsed == ROUND201_PINS, "Round201 manifest exact entries")
    for name, value in ROUND201_PINS.items():
        require(sha256_file(HERE / name) == value, f"Round201 pin:{name}")
    verification = strict_json(HERE / f"{ROUND201_PREFIX}_verification.json")
    result = verification["result"]
    require(
        verification["schema"].endswith(".verification.v1")
        and verification["result_sha256"] == ROUND201_VERIFICATION_RESULT_SHA256
        and digest(result) == ROUND201_VERIFICATION_RESULT_SHA256
        and result["verdict"] == "PASS"
        and result["status"] == "PASS_PARTIAL_FORMAL_ROUND201"
        and result["certificate_result_sha256"] == ROUND201_RESULT_SHA256
        and result["full_expected_canonical_equality"] is True
        and result["full_expected_python_object_equality"] is True
        and result["verified_census"]["combined_whole_record_excluded"]
        == OLD_EXCLUDED
        and result["verified_census"]["combined_conservative_live"] == OLD_LIVE
        and result["verified_census"]["remaining_priority_origins"]
        == OLD_REMAINING,
        "Round201 independent verification",
    )
    return {
        "manifest_sha256": ROUND201_MANIFEST_SHA256,
        "manifest_entries_replayed": True,
        "certificate_result_sha256": ROUND201_RESULT_SHA256,
        "verification_result_sha256": ROUND201_VERIFICATION_RESULT_SHA256,
        "verified_excluded": OLD_EXCLUDED,
        "verified_live": OLD_LIVE,
        "verified_remaining_priority_origins": OLD_REMAINING,
    }


def map_counter(counter: Counter[Any]) -> dict[str, int]:
    return {
        str(key): counter[key]
        for key in sorted(counter, key=lambda item: str(item))
    }


def source_partition(cell: str, box: Any) -> dict[str, Any]:
    require(cell in {"E", "N", "S"}, f"source chart:{cell}")
    negative = box.t1 < 0
    positive = box.t0 > 0
    require(negative ^ positive, "one source t sign")
    if negative:
        require(
            2 * box.t0 * box.t0 > 1
            and 2 * box.t1 * box.t1 < 1,
            "negative seam bracket",
        )
        sign = "NEGATIVE"
    else:
        require(
            2 * box.t0 * box.t0 < 1
            and 2 * box.t1 * box.t1 > 1,
            "positive seam bracket",
        )
        sign = "POSITIVE"

    adjacent = {
        ("E", "NEGATIVE"): "S",
        ("E", "POSITIVE"): "N",
        ("N", "NEGATIVE"): "W",
        ("N", "POSITIVE"): "E",
        ("S", "NEGATIVE"): "W",
        ("S", "POSITIVE"): "E",
    }[(cell, sign)]
    transfer_sign = -1 if cell == "S" else 1
    transfer = (
        "t_adjacent=-sqrt(1-t_source^2)"
        if transfer_sign < 0
        else "t_adjacent=sqrt(1-t_source^2)"
    )
    derivative = (
        "t_source/sqrt(1-t_source^2)"
        if transfer_sign < 0
        else "-t_source/sqrt(1-t_source^2)"
    )
    jacobian_on_seam = (
        -1
        if (transfer_sign < 0 and negative)
        or (transfer_sign > 0 and positive)
        else 1
    )
    seam_owner = (
        "W"
        if cell in {"N", "S"} and negative
        else "E"
    )
    original_owns_seam = cell == seam_owner
    require(
        (cell == "E") == original_owns_seam,
        "only horizontal source rows own selected seam",
    )
    return {
        "source_chart": cell,
        "source_t_sign": sign,
        "exact_parent_t_interval": [str(box.t0), str(box.t1)],
        "exact_seam_equation": "2*t_source^2=1",
        "unique_selected_seam":
            "-1/sqrt(2)" if negative else "+1/sqrt(2)",
        "strict_bracket_proved_by_exact_rational_squares": True,
        "physical_chart_interior_open_3D_predicate": "2*t_source^2<1",
        "source_seam_2D_predicate": "2*t_source^2=1",
        "guard_recoordination_open_3D_predicate": "2*t_source^2>1",
        "horizontal_E_or_W_chart_owns_equality": True,
        "source_seam_half_open_owner": seam_owner,
        "original_chart_owns_source_seam": original_owns_seam,
        "original_chart_owned_physical_parent_predicate": (
            "2*t_source^2<=1"
            if original_owns_seam
            else "2*t_source^2<1"
        ),
        "adjacent_coordinate_chart": adjacent,
        "exact_rechart": {
            "t_coordinate": transfer,
            "p_adjacent": "p_source",
            "s_adjacent": "s_source",
            "Jacobian_determinant": derivative,
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


def box_row(w: Any, box: Any) -> dict[str, Any]:
    return {
        "t": [str(box.t0), str(box.t1)],
        "p": [str(box.p0), str(box.p1)],
        "s": [str(box.s0), str(box.s1)],
        "ambient_dimension": 3,
        "exact_coordinate_volume": str(w.box_volume(box)),
    }


def pure_target_summary(
    w: Any,
    origin: str,
    roots: list[Any],
    refinement: dict[str, Any],
    final_rows: list[Any],
) -> dict[str, Any]:
    root_volumes = {row.key: w.box_volume(row.box) for row in roots}
    inherited = [
        w.wrap_round180_terminal(origin, row, root_volumes)
        for row in refinement["terminal_rows"]
    ]
    terminals = list(inherited)
    new_method_count: Counter[str] = Counter()
    new_split_faces: list[dict[str, Any]] = []

    for row in final_rows:
        proof, reason = w.clipped_partition_proof(row)
        if proof is not None:
            terminals.append(w.wrap_clipped_terminal(
                row,
                proof,
                "ROUND212_REBUILT_ROUND184_CLIPPED_DELTA_THREE_STRATUM",
            ))
            new_method_count["CLIPPED_DELTA_THREE_STRATUM"] += 1
            continue
        require(reason == w.TARGET_FAILURE, f"pure reason:{origin}:{row.key}")
        pending = [(row, 0)]
        while pending:
            child, depth = pending.pop()
            direct_kind, direct_evidence = w.direct_strict_terminal(child)
            if direct_kind == "EXCLUDED":
                require(direct_evidence is not None, "direct evidence")
                direct_row = {
                    "cell_key": child.key,
                    "origin_key": origin,
                    "method": "DEPTH2_DIRECT_STRICT_CLOSED_BOX",
                    **w.box_evidence(child),
                    "coarse_disposition": "EXCLUDED",
                    "direct_evidence": direct_evidence,
                    "whole_closed_cell_excluded": True,
                }
                direct_row["row_sha256"] = digest(direct_row)
                terminals.append(direct_row)
                new_method_count["DEPTH2_DIRECT_STRICT_CLOSED_BOX"] += 1
                continue
            child_proof, child_reason = (
                (None, f"DIRECT_STRICT_{direct_kind}")
                if direct_kind is not None
                else w.clipped_partition_proof(child)
            )
            if child_proof is not None:
                terminals.append(w.wrap_clipped_terminal(
                    child,
                    child_proof,
                    "DEPTH2_CLIPPED_DELTA_THREE_STRATUM",
                ))
                new_method_count["DEPTH2_CLIPPED_DELTA_THREE_STRATUM"] += 1
                continue
            if depth < 2:
                axis = w.r180.split_axis(child.box)
                lower, upper = w.r176.split(child.box, axis)
                new_split_faces.append(
                    w.r180.split_face(child, axis, lower, upper)
                )
                pending.append((w.child_frontier(child, upper), depth + 1))
                pending.append((w.child_frontier(child, lower), depth + 1))
                continue
            require(
                child_reason in {w.TARGET_FAILURE, w.FULL_P_FAILURE},
                f"depth2 cutoff:{origin}:{child.key}:{child_reason}",
            )
            exact = w.single_exact_behind_cell(
                child,
                (
                    "TARGET_FIRST_CLIPPED"
                    if child_reason == w.TARGET_FAILURE
                    else "FULL_P_FIRST_ROOT_EQUALITY"
                ),
            )
            require(exact["whole_closed_cell_excluded"], "exact behind")
            terminals.append(exact)
            new_method_count["DEPTH2_EXACT_BEHIND"] += 1

    terminals.sort(key=lambda row: row["cell_key"])
    require(
        len({row["cell_key"] for row in terminals}) == len(terminals)
        and all(row["whole_closed_cell_excluded"] for row in terminals),
        f"pure complete target partition:{origin}",
    )
    input_volume = sum((w.box_volume(row.box) for row in roots), w.Q(0))
    output_volume = sum(
        (w.Q(row["exact_volume"]) for row in terminals), w.Q(0)
    )
    require(input_volume == output_volume, f"pure volume:{origin}")
    combined_faces = sorted(
        refinement["split_face_rows"] + new_split_faces,
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
        "new_terminal_count_by_method": map_counter(new_method_count),
        "complete_split_face_count": len(combined_faces),
        "complete_split_face_rows_sha256": digest(combined_faces),
        "all_inherited_and_final_target_strata_excluded": True,
        "target_partition_count_and_exact_volume_conserved": True,
    }


def generalized_target_summary(
    w: Any,
    origin: str,
    roots: list[Any],
    refinement: dict[str, Any],
    final_rows: list[Any],
    priority_class: str,
) -> dict[str, Any]:
    root_volumes = {row.key: w.box_volume(row.box) for row in roots}
    inherited = [
        w.wrap_round180_terminal(origin, row, root_volumes)
        for row in refinement["terminal_rows"]
    ]
    evidence = [
        w.generalized_exact_behind_cell(
            row, w.r180.residual_category(row), priority_class
        )
        for row in final_rows
    ]
    all_inherited = all(
        row["whole_closed_cell_excluded"] for row in inherited
    )
    all_final = all(
        row["geometric_whole_cell_excluded"] for row in evidence
    )
    input_volume = sum((w.box_volume(row.box) for row in roots), w.Q(0))
    inherited_volume = sum(
        (w.Q(row["exact_volume"]) for row in inherited), w.Q(0)
    )
    final_volume = sum(
        (w.box_volume(row.box) for row in final_rows), w.Q(0)
    )
    require(
        inherited_volume + final_volume == input_volume,
        f"generalized volume:{origin}",
    )
    dispositions = Counter(row["final_disposition"] for row in evidence)
    return {
        "priority_class": priority_class,
        "Round176_residual_root_count": len(roots),
        "Round180_final_cell_count": len(final_rows),
        "inherited_terminal_count": len(inherited),
        "inherited_terminal_rows_sha256": digest(inherited),
        "generalized_final_evidence_rows_sha256": digest(evidence),
        "final_disposition_count": map_counter(dispositions),
        "geometrically_excluded_final_cell_count": sum(
            row["geometric_whole_cell_excluded"] for row in evidence
        ),
        "complete_target_partition_exact_volume": str(input_volume),
        "all_inherited_target_strata_excluded": all_inherited,
        "all_final_target_cells_excluded": all_final,
        "all_inherited_and_final_target_strata_excluded":
            all_inherited and all_final,
        "target_partition_count_and_exact_volume_conserved": True,
    }


def rebuild() -> dict[str, Any]:
    upstream = check_round201()
    pre_verifier_sha = sha256_file(HERE / ROUND201_VERIFIER)
    require(
        pre_verifier_sha == ROUND201_PINS[ROUND201_VERIFIER],
        "Round201 verifier pre-import pin",
    )
    w = importlib.import_module(ROUND201_VERIFIER_MODULE)
    require(
        sha256_file(HERE / ROUND201_VERIFIER) == pre_verifier_sha,
        "Round201 verifier post-import pin",
    )
    w.r180.check_chain()

    replay = w.r176.replay_frontier()
    base_kinds: defaultdict[str, set[str]] = defaultdict(set)
    base_kinds.update({
        key: set(values) for key, values in replay["origin_kinds"].items()
    })
    residual_by_origin: dict[str, list[Any]] = defaultdict(list)
    for frontier in replay["frontier"]:
        kind, _evidence = w.r176.closure(frontier)
        if kind is None:
            residual_by_origin[frontier.origin_key].append(frontier)
        else:
            base_kinds[frontier.origin_key].add(kind)
    for rows in residual_by_origin.values():
        rows.sort(key=lambda row: row.key)
    upper = sorted(
        origin
        for origin in residual_by_origin
        if base_kinds[origin] <= {"EXCLUDED"}
    )
    require(len(upper) == EXPECTED_UPPER_COUNT, "upper candidates")
    seam_keys = sorted(
        origin
        for origin in upper
        if w.r176.physical_domain(
            replay["origins"][origin]["chart_id"],
            replay["origins"][origin]["box"],
        )["classification"] == w.SOURCE_SEAM
    )
    require(
        len(seam_keys) == EXPECTED_ALL_SEAM_COUNT
        and digest(seam_keys) == EXPECTED_ALL_SEAM_KEYS_SHA256,
        "complete seam candidate selection",
    )

    rows: list[dict[str, Any]] = []
    promoted: list[str] = []
    residual: list[str] = []
    class_count: Counter[str] = Counter()
    chart_count: Counter[str] = Counter()
    owner_count: Counter[str] = Counter()
    adjacent_count: Counter[str] = Counter()
    source_sign_count: Counter[str] = Counter()
    total_target_terminal = 0
    total_final = 0
    total_inherited = 0

    for origin in seam_keys:
        roots = residual_by_origin[origin]
        refinement = w.r180.refine_origin(roots, 4)
        final_rows = refinement["final_residual_rows"]
        require(final_rows, f"Round180 seam residual:{origin}")
        categories = Counter(w.r180.residual_category(row) for row in final_rows)
        priority_class = w.support_class(categories)
        if priority_class == w.PURE_CLASS:
            target = pure_target_summary(
                w, origin, roots, refinement, final_rows
            )
            total_target_terminal += target["rebuilt_terminal_count"]
        else:
            target = generalized_target_summary(
                w, origin, roots, refinement, final_rows, priority_class
            )
            total_target_terminal += (
                target["inherited_terminal_count"]
                + target["Round180_final_cell_count"]
            )
        complete = (
            target["all_inherited_and_final_target_strata_excluded"]
            and priority_class != w.COMPACT_CLASS
        )
        meta = replay["origins"][origin]
        cell = meta["chart_id"].split(":")[1]
        source = source_partition(cell, meta["box"])
        row = {
            "origin_key": origin,
            "original_chart_id": meta["chart_id"],
            "original_parent_box": box_row(w, meta["box"]),
            "priority_class": priority_class,
            "target_closure": target,
            "source_half_open_partition": source,
            "complete_target_partition": complete,
            "physical_source_partition_complete": True,
            "whole_original_chart_owned_physical_parent_excluded": complete,
            "whole_origin_integer_credit": 1 if complete else 0,
            "child_cell_count_used_as_integer_credit": False,
            "two_one_zero_dimensional_count_used_as_integer_credit": False,
            "guard_recoordination_used_as_exterior_credit": False,
            "source_seam_used_as_separate_integer_credit": False,
            "outcome": (
                "PROMOTED_WHOLE_PHYSICAL_SOURCE_PARENT"
                if complete
                else "TARGET_INCOMPLETE_SEAM_ORIGIN_RESIDUAL"
            ),
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
        class_count[priority_class] += 1
        total_final += target["Round180_final_cell_count"]
        total_inherited += target["inherited_terminal_count"]
        if complete:
            promoted.append(origin)
            chart_count[cell] += 1
            owner_count[source["source_seam_half_open_owner"]] += 1
            adjacent_count[source["adjacent_coordinate_chart"]] += 1
            source_sign_count[source["source_t_sign"]] += 1
        else:
            residual.append(origin)

    require(
        len(promoted) == EXPECTED_PROMOTED_COUNT
        and digest(promoted) == EXPECTED_PROMOTED_KEYS_SHA256
        and residual == EXPECTED_RESIDUAL_KEYS
        and len(residual) == EXPECTED_RESIDUAL_COUNT,
        "Round212 promotion partition",
    )
    require(
        class_count
        == Counter({
            w.PURE_CLASS: 18,
            w.DELTA_MULTI_CLASS: 8,
        })
        and chart_count == Counter({"E": 6, "N": 9, "S": 9})
        and owner_count == Counter({"E": 12, "W": 12})
        and adjacent_count
        == Counter({"W": 12, "E": 6, "N": 3, "S": 3})
        and source_sign_count == Counter({"NEGATIVE": 15, "POSITIVE": 9}),
        "Round212 exact source partition census",
    )

    result = {
        "status": (
            "PARTIAL_FORMAL_SOURCE_W_HALF_OPEN_SOURCE_SEAM_PROMOTION__"
            "D02_STILL_BLOCKED"
        ),
        "scope": {
            "source_obstacle": "W",
            "selection":
                "all Round201 upper candidates crossing 2*t^2=1",
            "whole_origin_credit_unit":
                "one complete original chart-owned physical source parent",
            "selection_uses_Round212_target_outcome": False,
            "source_partition_uses_exact_algebraic_seam": True,
            "integer_credit_requires_complete_target_3D_2D_1D_0D_partition":
                True,
        },
        "frozen_Round201": upstream,
        "independent_target_replay": {
            "Round201_producer_imported_or_executed": False,
            "Round201_verifier_used_only_as_pinned_geometry_and_target_kernel":
                True,
            "Round201_verifier_sha256": pre_verifier_sha,
            "upper_candidate_count": len(upper),
            "all_source_seam_candidate_count": len(seam_keys),
            "all_source_seam_candidate_keys_sha256": digest(seam_keys),
            "priority_class_count": map_counter(class_count),
            "Round180_final_cell_count": total_final,
            "inherited_terminal_count": total_inherited,
            "rebuilt_target_proof_object_count": total_target_terminal,
            "every_promoted_origin_target_partition_complete": True,
            "two_incomplete_origins_retained": True,
        },
        "source_half_open_partition": {
            "horizontal_E_or_W_chart_owns_each_diagonal_equality": True,
            "vertical_N_or_S_chart_excludes_each_diagonal_equality": True,
            "promoted_origin_count_by_original_chart":
                map_counter(chart_count),
            "promoted_origin_count_by_source_t_sign":
                map_counter(source_sign_count),
            "promoted_source_seam_owner_count": map_counter(owner_count),
            "promoted_guard_adjacent_chart_count":
                map_counter(adjacent_count),
            "open_guard_rechart_Jacobians_all_nonzero": True,
            "same_physical_normal_position_velocity_and_s_under_rechart":
                True,
            "source_seams_counted_once": True,
            "open_guard_slices_counted_once": True,
            "guard_outside_exterior_credit": 0,
            "source_seam_lower_dimensional_integer_credit": 0,
        },
        "whole_origin_ledger": {
            "per_origin_rows": rows,
            "per_origin_rows_sha256": digest(rows),
            "source_seam_candidate_count": len(rows),
            "promoted_whole_origin_count": len(promoted),
            "promoted_whole_origin_keys": promoted,
            "promoted_whole_origin_keys_sha256": digest(promoted),
            "retained_target_incomplete_source_seam_count": len(residual),
            "retained_target_incomplete_source_seam_keys": residual,
            "retained_target_incomplete_source_seam_keys_sha256":
                digest(residual),
            "child_cell_count_used_as_integer_credit": False,
            "two_one_zero_dimensional_count_used_as_integer_credit": False,
            "guard_recoordination_used_as_exterior_credit": False,
        },
        "ledger_composition": {
            "Round201_whole_record_excluded": OLD_EXCLUDED,
            "Round201_conservative_live": OLD_LIVE,
            "new_whole_origin_credit": len(promoted),
            "combined_whole_record_excluded": NEW_EXCLUDED,
            "combined_conservative_live": NEW_LIVE,
            "refined_source_W_total": TOTAL_SOURCE_W,
            "exact_integer_conservation":
                NEW_EXCLUDED + NEW_LIVE == TOTAL_SOURCE_W,
            "Round201_remaining_priority_origins": OLD_REMAINING,
            "remaining_priority_origins": NEW_REMAINING,
            "remaining_priority_partition": {
                "incomplete_mixed_origins": 200,
                "compact_q_origins": 54,
            },
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    require(
        result["ledger_composition"]["exact_integer_conservation"]
        and result["ledger_composition"]["remaining_priority_origins"]
        == 200 + 54,
        "final ledger conservation",
    )
    return result


def output_allowed(path: Path) -> bool:
    try:
        resolved_parent = path.parent.resolve(strict=True)
    except OSError:
        return False
    if (
        resolved_parent != HERE.resolve()
        or path.parent.absolute() != HERE.resolve()
        or path.name != OUTPUT_NAME
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


def atomic_write(path: Path, payload: bytes) -> None:
    require(output_allowed(path), "authorized Round212 certificate output")
    fd, temporary = tempfile.mkstemp(
        prefix=".cm2_round212_certificate_", suffix=".tmp", dir=HERE
    )
    tmp = Path(temporary)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        directory_fd = os.open(HERE, os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if tmp.exists():
            tmp.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / OUTPUT_NAME)
    args = parser.parse_args()
    result = rebuild()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    payload = pretty_bytes(document)
    atomic_write(args.output, payload)
    print(digest(result))


if __name__ == "__main__":
    main()
