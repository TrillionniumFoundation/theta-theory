#!/usr/bin/env python3
"""Targeted zero-credit audit of exact-zero tangent derivatives in Round277."""
from __future__ import annotations

import collections
import gzip
import json
import multiprocessing as mp
from pathlib import Path

from flint import ctx

import cm2_round277_source_g_depth8_residual_active_graph_strategy_probe as active


HERE = Path(__file__).resolve().parent
SOURCE = (
    HERE
    / "cm2_round277_source_g_depth8_residual_indices_zero_credit.json.gz"
)
PROBE_RESULT = (
    HERE
    / "cm2_round277_source_g_depth8_residual_active_graph_strategy_probe_result.json"
)
RESULT = (
    HERE
    / "cm2_round277_source_g_active_graph_exact_zero_derivative_audit_result.json"
)


def main() -> int:
    ctx.prec = 256
    source = json.loads(gzip.decompress(SOURCE.read_bytes()))
    probe = json.loads(PROBE_RESULT.read_bytes())
    active.load_groups()
    group_by_candidate = {
        group[-1][0]: group_index
        for group_index, group in enumerate(active.GROUPS)
    }
    assert all(len(group[-1]) == 1 for group in active.GROUPS)

    target_g_groups = []
    face_axis_census = collections.Counter()
    for row in source["rows"]:
        index = row["candidate_index"]
        group_index = group_by_candidate[index]
        group = active.GROUPS[group_index]
        target = group[3]
        if target.startswith("G["):
            target_g_groups.append(group_index)
            face_axis_census["tps"[group[4]]] += 1
    assert len(target_g_groups) == 1_648
    assert face_axis_census == {"t": 1_584, "p": 64}

    forms = collections.Counter()
    cell_census = collections.Counter()
    dispositions = collections.Counter()
    with mp.get_context("fork").Pool(min(40, mp.cpu_count())) as pool:
        for output in pool.imap_unordered(
            active.worker, target_g_groups, chunksize=8
        ):
            (
                _group_index,
                _multiplicity,
                counts,
                normal_forms,
                _relations,
                candidate_dispositions,
                _unresolved,
            ) = output
            cell_census.update(dict(counts))
            forms.update(dict(normal_forms))
            dispositions.update(dict(candidate_dispositions))

    exact_zero_forms = {
        key: count
        for key, count in forms.items()
        if "EXACT_ZERO" in key[2]
    }
    exact_zero_count = sum(exact_zero_forms.values())
    global_exact_zero_count = sum(
        count
        for key, count in probe["active_normal_form_histogram"].items()
        if "EXACT_ZERO" in key
    )
    assert exact_zero_count == global_exact_zero_count == 35_328
    assert all(
        tangent_signs[-1] == "EXACT_ZERO"
        for _reason, _source_sign, tangent_signs, _classification
        in exact_zero_forms
    )
    assert dispositions == {"EXACT_POSITIVE_MATCH_SIDE_FOUND": 1_648}
    assert (
        cell_census[
            "FAILCLOSED_SOURCE_AND_HIT_ENDPOINT_FACTORS_BOTH_ACTIVE"
        ]
        == 256
    )

    result = {
        "status": (
            "ROUND277_ACTIVE_GRAPH_EXACT_ZERO_DERIVATIVE_AUDIT__"
            "PASS_ZERO_CREDIT"
        ),
        "target_G_candidate_group_count": len(target_g_groups),
        "target_G_face_axis_census": dict(sorted(face_axis_census.items())),
        "target_G_candidate_disposition_census": dict(
            sorted(dispositions.items())
        ),
        "exact_zero_terminal_cell_count": exact_zero_count,
        "exact_zero_strict_extremal_terminal_cell_count": (
            exact_zero_count - 256
        ),
        "exact_zero_failclosed_source_active_terminal_cell_count": 256,
        "all_global_exact_zero_normal_forms_reproduced_by_target_G_groups": True,
        "exact_zero_is_always_s_tangent_derivative": True,
        "algebraic_identity": (
            "FOR TARGET OBSTACLE G, CENTER_X AND CENTER_Y ARE CONSTANT; "
            "SOURCE GEOMETRY, OUTGOING NORMAL, HIT COORDINATES, AND "
            "OUTGOING_X^2-OUTGOING_Y^2 ARE INDEPENDENT OF s, SO d/ds=0"
        ),
        "safety_interpretation": [
            (
                "EXACT_ZERO IS ACCEPTED ONLY WHEN THE ARB DERIVATIVE IS "
                "THE EXACT SINGLETON ZERO, NOT WHEN ITS SIGN OVERWRAPS"
            ),
            (
                "THE 256 CELLS WHOSE WALL SOURCE FACTOR ALSO OVERWRAPS "
                "REMAIN FAIL-CLOSED"
            ),
        ],
        "audit_implementation_scope": (
            "TARGETED REPLAY THROUGH THE PROBE EVALUATOR PLUS FORMULA "
            "INSPECTION; NOT AN INDEPENDENT FORMAL VERIFIER"
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
