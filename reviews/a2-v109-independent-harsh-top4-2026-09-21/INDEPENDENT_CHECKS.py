#!/usr/bin/env python3
"""Independent exact diagnostics accompanying the A2 v109 referee report.

These checks verify finite combinatorial/dimension claims used in the report.
They do not certify the universal proofs or establish journal-level novelty.
"""
from __future__ import annotations
import json


def case(d: int, k: int, S: list[int]) -> dict:
    Sset = set(S)
    E = sorted(set(range(k)) - Sset)
    sums = {a + b for a in Sset for b in Sset}
    target = set(range(2 * k - 1))
    parity = [a for a in E if (k - 1 - a) % 2 == 0]
    assert len(Sset) == k - d
    assert len(E) == d
    assert sums == target
    assert parity
    return {
        "d": d,
        "k": k,
        "S": sorted(Sset),
        "E": E,
        "full_sumset": True,
        "represented_exponents": [0, 2 * k - 2],
        "positive_target_parity_exponents": parity,
        "measurement_noninjective_by_dimension": k < d * (d + 1) // 2,
    }


def manuscript_case(d: int) -> dict:
    k = 3 * d + 2
    S = list(range(d + 1)) + list(range(2 * d + 1, 3 * d + 2))
    out = case(d, k, S)
    expected_nullity = d * (2 * k - d + 1) // 2
    assert expected_nullity == 5 * d * (d + 1) // 2
    out["ambient_unrestricted_fibre_dimension"] = expected_nullity
    return out


def main() -> None:
    checks = {
        "scope": "finite exact combinatorial diagnostics; not universal proof or novelty certification",
        "reviewed_source_commit": "60999f38f745072d240909fe8c77aee5be2df69a",
        "manuscript_construction": [manuscript_case(d) for d in (2, 3, 6, 10)],
        "smaller_same-architecture_witnesses": [
            case(2, 7, [0, 1, 3, 5, 6]),
            case(6, 14, [0, 1, 2, 5, 8, 11, 12, 13]),
        ],
    }
    assert all(
        (3 * d + 2 < d * (d + 1) // 2) == (d >= 6)
        for d in range(2, 100)
    )
    checks["manuscript_noninjective_threshold_first_d"] = 6
    checks["status"] = "passed"
    print(json.dumps(checks, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
