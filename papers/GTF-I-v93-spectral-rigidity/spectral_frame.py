#!/usr/bin/env python3
"""Exact rational projection-decomposition certificates in a supplied eigenbasis.

Input JSON: {"eigenvalues": ["1/2", "1/3", "1/6"], "rank": 2}.
No eigenbasis, physical instrument, reset calibration, or priority is inferred.
"""
from __future__ import annotations
from fractions import Fraction
from pathlib import Path
from typing import Iterable
import argparse
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def rational(value: object) -> Fraction:
    require(isinstance(value, (str, int, Fraction)) and not isinstance(value, bool),
            'Use exact integer or rational-string eigenvalues, not floats or booleans.')
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError, TypeError) as exc:
        raise ValueError('Invalid rational eigenvalue.') from exc


def spectrum(values: Iterable[object], rank: int) -> list[Fraction]:
    lam = [rational(x) for x in values]
    require(bool(lam), 'The spectrum must be nonempty.')
    require(isinstance(rank, int) and not isinstance(rank, bool) and 1 <= rank <= len(lam),
            'The rank must be an integer between one and the input dimension.')
    require(all(x >= 0 for x in lam) and sum(lam) == 1,
            'Eigenvalues must be nonnegative and sum exactly to one.')
    return lam


def projection_decomposition(values: Iterable[object], rank: int) -> list[tuple[Fraction, tuple[int, ...]]]:
    """Return at most d weighted rank-r coordinate projections, exactly."""
    lam = spectrum(values, rank)
    require(max(lam) <= Fraction(1, rank), 'The supplied spectrum exceeds the 1/r cap.')
    cumulative = [Fraction(0)]
    for x in lam:
        cumulative.append(cumulative[-1] + rank*x)
    cuts = sorted({Fraction(0), Fraction(1), *(x-x.numerator//x.denominator for x in cumulative)})
    result = []
    for left, right in zip(cuts, cuts[1:]):
        if left == right:
            continue
        u = (left + right)/2
        selected = []
        for i, (a, b) in enumerate(zip(cumulative, cumulative[1:])):
            if any(a <= u+j < b for j in range(rank)):
                selected.append(i)
        require(len(selected) == rank, 'Internal interval-rank mismatch.')
        result.append((right-left, tuple(selected)))
    require(len(result) <= len(lam), 'Internal cardinality bound failed.')
    require(sum(w for w, _ in result) == 1, 'Internal weight normalization failed.')
    for i, x in enumerate(lam):
        require(sum(w/rank for w, subset in result if i in subset) == x,
                'Internal barycenter identity failed.')
    return result


def capped_distance(values: Iterable[object], rank: int) -> tuple[Fraction, list[Fraction]]:
    """Return the exact l1 distance and one nearest capped diagonal spectrum."""
    lam = spectrum(values, rank)
    cap = Fraction(1, rank)
    result = [min(x, cap) for x in lam]
    excess = 1-sum(result)
    remaining = excess
    for i, x in enumerate(result):
        add = min(cap-x, remaining)
        result[i] += add
        remaining -= add
    require(remaining == 0 and sum(result) == 1, 'Insufficient cap capacity.')
    require(sum(abs(x-y) for x, y in zip(lam, result)) == 2*excess,
            'Internal trace-distance identity failed.')
    return 2*excess, result


def certificate(data: object) -> dict:
    require(isinstance(data, dict) and set(data) == {'eigenvalues', 'rank'},
            'Expected exactly eigenvalues and rank fields.')
    require(isinstance(data['eigenvalues'], list), 'eigenvalues must be a list.')
    lam = spectrum(data['eigenvalues'], data['rank'])
    atoms = projection_decomposition(lam, data['rank'])
    return {
        'schema': 'gtf93.rational-spectral-frame/1', 'status': 'success',
        'dimension': len(lam), 'rank': data['rank'],
        'eigenvalues': list(map(str, lam)),
        'atoms': [{'weight': str(w), 'coordinates': list(subset)} for w, subset in atoms],
        'exact_barycenter_checked': True,
        'at_most_dimension_outcomes': len(atoms) <= len(lam),
        'eigenbasis_supplied_by_the_mathematical_model': True,
        'physical_instrument_executed': False, 'reset_calibration': False,
        'independent_priority_clearance': False, 'continuum_theorem_proved_by_code': False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        result = certificate(json.loads(args.input.read_text()))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
