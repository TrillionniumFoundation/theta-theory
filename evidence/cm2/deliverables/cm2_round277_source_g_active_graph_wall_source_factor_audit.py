#!/usr/bin/env python3
"""Targeted zero-credit audit of wall source-factor handling in Round277."""
from __future__ import annotations

import collections
import gzip
import hashlib
import json
import multiprocessing as mp
from pathlib import Path

from flint import ctx

import cm2_round276_source_g_collar_region_face_binding_probe as r276
import cm2_round277_source_g_depth8_residual_active_graph_strategy_probe as active


HERE = Path(__file__).resolve().parent
SOURCE = (
    HERE
    / "cm2_round277_source_g_depth8_residual_indices_zero_credit.json.gz"
)
RESULT = (
    HERE
    / "cm2_round277_source_g_active_graph_wall_source_factor_audit_result.json"
)


def main() -> int:
    ctx.prec = 256
    source = json.loads(gzip.decompress(SOURCE.read_bytes()))
    selected = {
        row["candidate_index"]
        for row in source["rows"]
        if any(
            reason
            in row["depth8_failclosed_search"][
                "depth8_unresolved_terminal_reason_histogram"
            ]
            for reason in (
                "wall_endpoint_or_count_transition:X:0",
                "wall_endpoint_or_count_transition:Y:0",
            )
        )
    }
    assert len(selected) == 608

    active.load_groups()
    group_by_candidate = {
        group[-1][0]: group_index
        for group_index, group in enumerate(active.GROUPS)
    }
    assert all(len(group[-1]) == 1 for group in active.GROUPS)
    selected_groups = [
        group_by_candidate[index] for index in sorted(selected)
    ]

    cell_census = collections.Counter()
    disposition_census = collections.Counter()
    source_overwrap_indices = []
    with mp.get_context("fork").Pool(min(40, mp.cpu_count())) as pool:
        for output in pool.imap_unordered(
            active.worker, selected_groups, chunksize=4
        ):
            (
                group_index,
                _multiplicity,
                counts,
                _forms,
                _relations,
                dispositions,
                _unresolved,
            ) = output
            counts = dict(counts)
            cell_census.update(counts)
            disposition_census.update(dict(dispositions))
            source_fail_count = counts.get(
                "FAILCLOSED_SOURCE_AND_HIT_ENDPOINT_FACTORS_BOTH_ACTIVE",
                0,
            )
            if source_fail_count:
                assert source_fail_count == 4
                source_overwrap_indices.append(
                    active.GROUPS[group_index][-1][0]
                )

    source_overwrap_indices.sort()
    assert len(source_overwrap_indices) == 64
    assert cell_census == {
        "STRICT_DIFFERENT_COMPLETE_SIGNATURE_CELL": 12_768,
        "ACTIVE_EQUALITY_ZERO_SET_ABSENT_BY_EXTREMA": 9_600,
        "ACTIVE_EQUALITY_REGULAR_MONOTONE_GRAPH": 6_272,
        "FAILCLOSED_SOURCE_AND_HIT_ENDPOINT_FACTORS_BOTH_ACTIVE": 256,
    }
    assert disposition_census == {
        "EXACT_POSITIVE_MATCH_SIDE_FOUND": 608
    }

    result = {
        "status": (
            "ROUND277_ACTIVE_GRAPH_WALL_SOURCE_FACTOR_AUDIT__"
            "PASS_WITH_FAILCLOSED_CAVEAT__ZERO_CREDIT"
        ),
        "selected_X0_or_Y0_wall_candidate_count": len(selected),
        "candidate_disposition_census": dict(
            sorted(disposition_census.items())
        ),
        "terminal_cell_census": dict(sorted(cell_census.items())),
        "strict_source_factor_terminal_cell_count": 15_872,
        "source_and_hit_factors_both_active_terminal_cell_count": 256,
        "candidate_groups_containing_source_factor_overwrap": 64,
        "source_factor_overwrap_candidate_indices_sha256": r276.digest(
            source_overwrap_indices
        ),
        "safety_interpretation": [
            (
                "THE 256 SOURCE-OVERWRAP CELLS ARE NEVER USED AS "
                "REQUESTED-SIDE WITNESSES"
            ),
            (
                "THEIR 64 CANDIDATE GROUPS ARE ACCEPTED ONLY BECAUSE A "
                "SEPARATE STRICT EXTREMAL SIDE EXISTS ELSEWHERE"
            ),
            (
                "THOSE 64 GROUPS ARE NOT FULL ARRANGEMENT CLOSURES AND "
                "MUST RETAIN THE 256 FAIL-CLOSED CELLS"
            ),
        ],
        "audit_implementation_scope": (
            "TARGETED REPLAY THROUGH THE PROBE EVALUATOR; NOT AN "
            "INDEPENDENT FORMAL VERIFIER"
        ),
        "strict_nonpromotion": {
            "component_edge_credit": 0,
            "rank_reduction_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    RESULT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
