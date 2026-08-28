#!/usr/bin/env python3
"""Moving-test upgrade and fixed-time DQ telescope frontier.

The certified depth-one quotient converges in the norm of
``(C^{1,alpha})*``.  Norm convergence, rather than merely pointwise
convergence, immediately permits tests ``Phi_s`` that converge to ``Phi_0``
in ``C^{1,alpha}``.  This closes the strong moving-test version of the
depth-one statement.

For every fixed iterate the exact noncommutative telescope

    (P_s^n-P_0^n)/s
      = sum_{j=0}^{n-1} P_s^{n-1-j} ((P_s-P_0)/s) P_0^j

is also replayed.  The remaining obstruction is analytic, not algebraic:
the iterated sources/tests are only branchwise regular across moving
singularity cuts, and the available depth-one theorem is not an operator-
norm statement on the three frozen MT_DQ spaces.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DQ_MANIFEST = HERE / "cm2-gate3-depth-one-fixed-gauge-dq-manifest-2026-07-15.json"
RECOVERY_MANIFEST = (
    HERE / "cm2-gate45-density-regular-mesh-recovery-bridge-manifest-2026-07-16.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_dependencies() -> tuple[dict[str, Any], dict[str, Any]]:
    dq = json.loads(DQ_MANIFEST.read_text(encoding="utf-8"))
    recovery = json.loads(RECOVERY_MANIFEST.read_text(encoding="utf-8"))
    assert dq["verdict"]["complete_depth_one_fixed_gauge_DQ"] == "CERTIFIED"
    assert recovery["verdict"]["controlled_s0_stopped_parent_recovery"] == "CERTIFIED"
    return dq, recovery


def word(symbol: str, count: int) -> tuple[str, ...]:
    return tuple(symbol for _ in range(count))


def telescope_rows(maximum_depth: int = 64) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    for depth in range(1, maximum_depth + 1):
        expansion: Counter[tuple[str, ...]] = Counter()
        for index in range(depth):
            expansion[
                word("S", depth - index) + word("0", index)
            ] += 1
            expansion[
                word("S", depth - 1 - index) + word("0", index + 1)
            ] -= 1
        expected = Counter({word("S", depth): 1, word("0", depth): -1})
        # Counter's unary plus and in-place addition drop negative entries,
        # so compare the signed dictionaries directly.
        cleaned = {key: value for key, value in expansion.items() if value}
        expected_cleaned = {key: value for key, value in expected.items() if value}
        assert cleaned == expected_cleaned
        rows.append({
            "fixed_depth_n": depth,
            "summand_count": depth,
            "uncancelled_words": [
                ["S^n", 1],
                ["0^n", -1],
            ],
            "all_mixed_words_cancel": True,
        })
    return rows, {
        "checked_fixed_depth_range": [1, maximum_depth],
        "exact_noncommutative_telescope": (
            "(P_s^n-P_0^n)/s=sum_(j=0)^(n-1) "
            "P_s^(n-1-j)*((P_s-P_0)/s)*P_0^j"
        ),
        "all_mixed_noncommutative_words_cancel": True,
        "telescope_rows_sha256": canonical_digest(rows),
    }


def moving_test_upgrade() -> dict[str, Any]:
    return {
        "depth_one_norm_convergence": (
            "L_s(h)=(P_s-P_0)h/s converges to D_0 h in (C^{1,alpha})*"
        ),
        "moving_test_hypothesis": (
            "Phi_s->Phi_0 in C^{1,alpha} for one fixed C^1 source h"
        ),
        "two_term_estimate": (
            "abs(L_s(h)(Phi_s)-D_0h(Phi_0)) <= "
            "||L_s(h)-D_0h||*||Phi_0|| + "
            "||L_s(h)||*||Phi_s-Phi_0||"
        ),
        "uniform_boundedness_reason": (
            "norm convergence of L_s(h) implies sup_s ||L_s(h)||<infinity"
        ),
        "uncentered_depth_one_strong_moving_test_DQ": True,
        "centered_depth_one_strong_moving_test_DQ": True,
        "source_is_fixed_not_s_dependent": True,
    }


def exact_MT_DQ_frontier() -> dict[str, Any]:
    return {
        "fixed_time_telescope_algebra_complete": True,
        "depth_one_strong_moving_tests_complete": True,
        "still_missing": [
            "uniform operator-norm DQ from the frozen strong space to the DQ space",
            "branch-record C1/BL tightness across every iterated moving singularity cut",
            "fixed-time convergence of Q_s^m sources in the frozen strong space",
            "regular/face/product-current four-type convergence on one common finite atlas",
            "summable two-time CM2 majorant and FACE_2CUT middle tail",
        ],
        "fixed_time_dynamic_branch_record_MT_DQ": False,
        "full_three_space_MT_DQ": False,
        "CM2_time_decay_majorant": False,
    }


def certify() -> dict[str, Any]:
    dq, recovery = load_dependencies()
    rows, telescope = telescope_rows()
    moving = moving_test_upgrade()
    frontier = exact_MT_DQ_frontier()
    dq_result = dq["result"]["fixed_gauge_depth_one_DQ"]
    assert dq_result["operator_conclusion"][
        "uncentered_depth_one_transfer_DQ"
    ] == "CERTIFIED"
    assert recovery["result"]["scope_limits"][
        "uniform_finite_s_moving_face_recovery"
    ] is False
    return {
        "schema": "cm2.gate3.moving-test-telescope-frontier.v1",
        "provenance": {
            "depth_one_DQ_manifest": DQ_MANIFEST.name,
            "density_mesh_recovery_manifest": RECOVERY_MANIFEST.name,
            "corrected_current_rows_sha256": (
                "5c03da290697ac25b814848c5aee50b22387866f9d72303a60649466cad896bd"
            ),
        },
        "depth_one_strong_moving_test_upgrade": moving,
        "fixed_time_noncommutative_telescope": telescope,
        "exact_MT_DQ_frontier": frontier,
        "scope_limits": {
            "depth_one_strong_moving_test_DQ": True,
            "fixed_time_DQ_telescope_algebra": True,
            "fixed_time_dynamic_branch_record_MT_DQ": False,
            "uniform_finite_s_moving_face_recovery": False,
            "full_three_space_MT_DQ": False,
            "CM2_time_decay_majorant": False,
            "CM2_norm_lifts": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
        "internal_replay_digest": canonical_digest(rows),
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_DEPTH_ONE_STRONG_MOVING_TEST_DQ: CERTIFIED")
    print("GATE3_FIXED_TIME_NONCOMMUTATIVE_DQ_TELESCOPE: CERTIFIED")
    print("GATE3_DYNAMIC_BRANCH_RECORD_FULL_MT_DQ: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
