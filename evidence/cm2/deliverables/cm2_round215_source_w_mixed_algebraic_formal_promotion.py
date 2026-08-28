#!/usr/bin/env python3
"""Formalize the outcome-blind Round215 mixed algebraic promotion.

The computation kernel is the pinned Round215 bounded probe.  That probe
selects all 596 frozen DELTA_H_OR_MULTI_NO_Q origins before seeing the new
closure outcome, independently rebuilds the 200 Round201-incomplete origins,
removes exactly the two frozen Round212 seam origins, and analyzes every one
of the resulting 18,432 closed 3D cells.  Only after that complete analysis
does this producer promote the two whole origins whose base, inherited,
exact-behind, and new terminal partitions are all excluded.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any

sys.dont_write_bytecode = True


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round215.source-w-mixed-algebraic-formal-promotion.v1"
OUTPUT_NAME = (
    "cm2_round215_source_w_mixed_algebraic_formal_promotion_"
    "certificate.json"
)
PROBE_NAME = "cm2_round215_source_w_mixed_algebraic_blocker_probe.py"
PROBE_SHA256 = (
    "463dfe832b32459b356bdfa0602c5eacea82569734f7ad1016c97ffa9d6c40c1"
)
EXPECTED_PROMOTED_KEYS = (
    "W:N:06.00.01111000",
    "W:S:H.06.00.01111000",
)
EXPECTED_PROMOTED_KEYS_SHA256 = (
    "f7c3a8854d6b7b561f1bb90dac18ebf7551f5ff4be1a73af764846808fbf5941"
)

OLD_EXCLUDED = 74_582
OLD_LIVE = 2_250
OLD_REMAINING = 254
NEW_CREDIT = 2
NEW_EXCLUDED = 74_584
NEW_LIVE = 2_248
NEW_REMAINING = 252
TOTAL_SOURCE_W = 76_832


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


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode()


def read_regular(path: Path, maximum: int = 16 * 1024 * 1024) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent == HERE, f"input parent:{absolute.name}")
    require(
        absolute.parent.resolve() == HERE,
        f"input parent resolution:{absolute.name}",
    )
    info = absolute.lstat()
    require(
        stat.S_ISREG(info.st_mode)
        and not absolute.is_symlink()
        and info.st_nlink == 1,
        f"input regular singleton:{absolute.name}",
    )
    require(0 < info.st_size <= maximum, f"input size:{absolute.name}")
    descriptor = os.open(
        absolute, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino) == (info.st_dev, info.st_ino)
            and stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1,
            f"input race/type:{absolute.name}",
        )
        raw = b""
        while len(raw) < opened.st_size:
            chunk = os.read(descriptor, opened.st_size - len(raw))
            require(bool(chunk), f"short read:{absolute.name}")
            raw += chunk
        require(not os.read(descriptor, 1), f"growing input:{absolute.name}")
    finally:
        os.close(descriptor)
    return raw


require(
    hashlib.sha256(read_regular(HERE / PROBE_NAME)).hexdigest()
    == PROBE_SHA256,
    "Round215 probe source pin",
)
if os.fspath(HERE) not in sys.path:
    sys.path.insert(0, os.fspath(HERE))
probe = importlib.import_module(PROBE_NAME[:-3])
require(
    Path(probe.__file__).resolve() == (HERE / PROBE_NAME).resolve(),
    "Round215 probe module identity",
)
require(
    hashlib.sha256(read_regular(HERE / PROBE_NAME)).hexdigest()
    == PROBE_SHA256,
    "Round215 probe post-import pin",
)


def rebuild() -> dict[str, Any]:
    bounded = probe.rebuild()
    whole = bounded["whole_origin_outcome"]
    promoted = whole["candidate_complete_origin_keys"]
    promotion_rows = whole["formalization_candidate_rows"]
    active = bounded["active_algebraic_census"]
    split = bounded[
        "generalized_650_scope_split_outer_conservation"
    ]
    require(
        promoted == list(EXPECTED_PROMOTED_KEYS)
        and whole["candidate_complete_origin_count"] == NEW_CREDIT
        and whole["candidate_complete_origin_keys_sha256"]
        == EXPECTED_PROMOTED_KEYS_SHA256
        and [row["origin_key"] for row in promotion_rows] == promoted
        and whole["formalization_candidate_rows_sha256"]
        == digest(promotion_rows),
        "exact outcome-derived promotion identity",
    )
    require(
        bounded["selection"][
            "selected_registry_origin_count"
        ] == 596
        and bounded["selection"][
            "independently_rebuilt_incomplete_origin_count"
        ] == 200
        and bounded["selection"][
            "active_strict_source_interior_origin_count"
        ] == 198
        and active["active_residual_cell_count"] == 18_432
        and active["analytic_closed_cell_count"] == 3_444
        and active["blocked_cell_count"] == 14_988
        and len(
            active["owner_margin_attack_fixture"][
                "enhanced_owner_margin_signs"
            ]
        ) == 8
        and split["mixed"]["origin_count"] == 596
        and split["compact_q"]["origin_count"] == 54
        and split["global_650"]["origin_count"] == 650
        and split["global_650"]["child_count"] == 182_776
        and split["global_650"][
            "geometric_residual_cell_count"
        ] == 21_128,
        "outcome-blind cohort and 650 conservation",
    )
    require(
        len(promotion_rows) == NEW_CREDIT
        and sum(
            row["Round215_new_terminal_cell_count"]
            for row in promotion_rows
        ) == 16
        and all(
            row["selection_derived_only_after_full_198_origin_analysis"]
            and row["Round176_preclosed_all_excluded"]
            and row["Round180_inherited_terminal_count"] == 116
            and row[
                "Round180_inherited_nonexcluded_terminal_count"
            ] == 0
            and row[
                "Round180_all_inherited_terminals_excluded"
            ]
            and row["Round201_residual_cell_count"] == 8
            and row["Round215_new_terminal_cell_count"] == 8
            and row["Round176_prior_terminal_count"] == 5
            and row["Round176_prior_coverage_numerator_64"] == 7
            and row["Round176_prior_all_excluded"]
            and row[
                "prior_plus_frontier_base_plus_residual_roots_equals_"
                "original_parent"
            ]
            and row["inherited_plus_final_equals_residual_roots"]
            and row[
                "exact_behind_plus_Round215_equals_final_cells"
            ]
            and row["all_3D_2D_1D_0D_target_strata_excluded"]
            and row[
                "lower_dimensional_inheritance_derived_from_strict_"
                "predicates_and_rebuilt_ledger"
            ]
            and row["independent_lower_dimensional_owner_audit"][
                "trusted_legacy_ledger_conclusion_boolean"
            ] is False
            and row["independent_lower_dimensional_owner_audit"][
                "all_owner_rows_reduce_to_excluded_closed_3D_"
                "enclosures"
            ]
            and row["independent_lower_dimensional_owner_audit"][
                "internal_and_outer_strata_classes_are_disjoint"
            ]
            and row["whole_original_physical_parent_excluded"]
            and row["whole_origin_integer_credit"] == 1
            and all(
                cell["analytic_closed"]
                and cell["method"]
                == "MONOTONE_P_SAME_SIGN_DELTA_STRICT_EXCLUSION"
                and cell[
                    "closed_box_boundary_restriction_proof"
                ][
                    "Delta_endpoints_have_same_strict_sign"
                ]
                and cell[
                    "closed_box_boundary_restriction_proof"
                ][
                    "Delta_zero_graph_intersects_closed_box"
                ] is False
                and cell[
                    "closed_box_boundary_restriction_proof"
                ]["post_enhancement_leaf"] == "unique_first"
                and (
                    cell[
                        "closed_box_boundary_restriction_proof"
                    ][
                        "unique_first_owner_mismatch_on_whole_"
                        "closed_box"
                    ]
                    or cell[
                        "closed_box_boundary_restriction_proof"
                    ][
                        "outgoing_owner_chart_mismatch_on_whole_"
                        "closed_box"
                    ]
                )
                and cell[
                    "closed_box_boundary_restriction_proof"
                ][
                    "all_applicable_owner_chart_margins_strict"
                ]
                and cell[
                    "closed_box_boundary_restriction_proof"
                ][
                    "closed_box_strict_inequalities_restrict_to_all_"
                    "faces_edges_vertices"
                ]
                and cell[
                    "strict_closed_box_predicates_restrict_to_cell_"
                    "faces_edges_vertices"
                ]
                for cell in row["Round215_new_terminal_rows"]
            )
            for row in promotion_rows
        ),
        "two complete full-dimensional whole-origin proofs",
    )
    result = {
        "status": "PARTIAL_FORMAL_ROUND215",
        "verdict": "PASS_PARTIAL_FORMAL_PROMOTION",
        "selection_and_full_census": {
            "outcome_blind_registry_priority_class":
                "DELTA_H_OR_MULTI_NO_Q",
            "registry_origin_count": 596,
            "independently_rebuilt_incomplete_origin_count": 200,
            "frozen_Round212_seam_origin_count": 2,
            "active_strict_source_interior_origin_count": 198,
            "active_residual_cell_count": 18_432,
            "candidate_selection_performed_after_full_active_analysis":
                True,
            "promoted_origin_count": NEW_CREDIT,
            "promoted_origin_keys": promoted,
            "promoted_origin_keys_sha256":
                EXPECTED_PROMOTED_KEYS_SHA256,
            "still_blocked_active_origin_count": 196,
            "retained_seam_origin_count": 2,
            "remaining_mixed_origin_count": 198,
            "compact_q_origin_count": 54,
            "remaining_priority_origin_count": NEW_REMAINING,
        },
        "formal_promotion": {
            "whole_origin_integer_credit": NEW_CREDIT,
            "promotion_rows": promotion_rows,
            "promotion_rows_sha256": digest(promotion_rows),
            "new_3D_terminal_cell_count": 16,
            "whole_origin_credit_uses_only_complete_original_origins":
                True,
            "child_volume_sheet_edge_vertex_counts_used_as_credit": False,
        },
        "bounded_probe_result": bounded,
        "bounded_probe_result_sha256": digest(bounded),
        "ledger_composition": {
            "Round212_whole_record_excluded": OLD_EXCLUDED,
            "Round212_conservative_live": OLD_LIVE,
            "Round212_remaining_priority_origins": OLD_REMAINING,
            "new_whole_origin_credit": NEW_CREDIT,
            "combined_whole_record_excluded": NEW_EXCLUDED,
            "combined_conservative_live": NEW_LIVE,
            "refined_source_W_total": TOTAL_SOURCE_W,
            "exact_integer_conservation":
                NEW_EXCLUDED + NEW_LIVE == TOTAL_SOURCE_W,
            "remaining_priority_origins": NEW_REMAINING,
            "remaining_priority_partition": {
                "incomplete_mixed_origins": 198,
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
        "implementation_disclosure": {
            "producer_imports_pinned_Round215_probe": True,
            "probe_sha256": PROBE_SHA256,
            "formal_wrapper_adds_no_new_geometric_predicate": True,
            "formal_wrapper_only_promotes_outcome_derived_complete_rows":
                True,
        },
    }
    require(
        result["ledger_composition"]["exact_integer_conservation"]
        and result["ledger_composition"]["remaining_priority_origins"]
        == (
            result["ledger_composition"][
                "remaining_priority_partition"
            ]["incomplete_mixed_origins"]
            + result["ledger_composition"][
                "remaining_priority_partition"
            ]["compact_q_origins"]
        ),
        "formal ledger conservation",
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
    require(output_allowed(path), "authorized Round215 certificate output")
    descriptor, temporary = tempfile.mkstemp(
        prefix=".cm2_round215_certificate_", suffix=".tmp", dir=HERE
    )
    tmp = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as handle:
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
    probe.ctx.prec = 192
    result = rebuild()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    atomic_write(args.output, pretty_bytes(document))
    print(digest(result))


if __name__ == "__main__":
    main()
