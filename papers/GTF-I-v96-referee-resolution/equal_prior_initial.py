#!/usr/bin/env python3
"""Rational enclosures for the equal-prior two-dimensional-old-receiver value.

Input is a supplied exact spectrum, not a device measurement or calibration.
The initial acquisition is pure with that Gram spectrum. Priors are equal;
the latent basis is drawn once and reused at both calls.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
from pathlib import Path
from typing import Any


def rational(x: Any) -> Fraction:
    if isinstance(x, bool) or not isinstance(x, (str, int)):
        raise ValueError('Use integer or rational-string data, not floating-point numbers')
    return Fraction(x)


def sqrt_interval(x: Fraction, bits: int) -> tuple[Fraction, Fraction]:
    if x < 0 or not 1 <= bits <= 4096:
        raise ValueError('Nonnegative radicand and 1..4096 precision bits required')
    if x == 0:
        return Fraction(0), Fraction(0)
    lo, hi = Fraction(0), max(Fraction(1), x)
    epsilon = Fraction(1, 1 << bits)
    while hi - lo > epsilon:
        mid = (lo + hi) / 2
        if mid * mid == x:
            return mid, mid
        if mid * mid < x:
            lo = mid
        else:
            hi = mid
    return lo, hi


def certificate(spectrum: list[Any], t: Any = '1', bits: int = 80,
                fresh_dimension: int | None = None) -> dict[str, Any]:
    if not isinstance(spectrum, list):
        raise ValueError('Spectrum must be a JSON list of exact rational values')
    a = [rational(x) for x in spectrum]
    d = len(a)
    if d < 2 or any(x < 0 for x in a) or sum(a) != 1:
        raise ValueError('A nonnegative trace-one spectrum of length at least two is required')
    ell = d if fresh_dimension is None else fresh_dimension
    if isinstance(ell, bool) or not isinstance(ell, int) or not 2 <= ell <= d:
        raise ValueError('Fresh dimension must be an integer in [2,d]')
    if isinstance(bits, bool) or not isinstance(bits, int) or not 1 <= bits <= 4096:
        raise ValueError('Precision bits must be an integer in [1,4096]')
    t = rational(t)
    if not 0 <= t <= 1:
        raise ValueError('Deformation t must lie in [0,1]')
    q = max(max(a), Fraction(1, 2))
    v = 4*q*(1-q)
    c = d*(d-2)+(2*d-1)*v
    h_lo, h_hi = sqrt_interval(c / (d*d-1), bits)
    gain = (2*d-1)*v
    psi_lo = d-1 + gain/(2*(d-1+d*h_hi))
    psi_hi = d-1 + gain/(2*(d-1+d*h_lo))
    prefactor = t*t/(2*d*(d+1))
    lower = Fraction(1, 2)+prefactor*psi_lo
    upper = Fraction(1, 2)+prefactor*psi_hi
    if not Fraction(1, 2) <= lower <= upper <= 1:
        raise ArithmeticError('Internal probability enclosure failure')
    return {
        'schema': 'gtf95.equal-prior-initial/1', 'status': 'success',
        'input_dimension': d, 'old_dimension_cap': 2, 'fresh_dimension_cap': ell,
        'supplied_spectrum': [str(x) for x in a], 'deformation': str(t),
        'rank_two_majorant': [str(q), str(1-q)], 'v': str(v),
        'radicand': str(c/(d*d-1)),
        'sqrt_lower': str(h_lo), 'sqrt_upper': str(h_hi),
        'score_lower': str(lower), 'score_upper': str(upper),
        'enclosure_width': str(upper-lower), 'precision_bits': bits,
        'equal_hypothesis_priors': True, 'same_latent_device_at_both_calls': True,
        'fixed_pure_initial_acquisition': True,
        'mathematical_theorem': 'thm:equalinitial95',
        'computed_from_supplied_exact_spectrum': True,
        'unknown_device_tomography': False, 'physical_reset_calibration': False,
        'physical_execution': False, 'continuum_proof_by_replay': False,
        'independent_priority_clearance': False,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('--bits', type=int, default=80)
    a = p.parse_args()
    try:
        data = json.loads(a.input.read_text())
        if not isinstance(data, dict):
            raise ValueError('Input must be a JSON object')
        result = certificate(data['spectrum'], data.get('t', '1'), a.bits,
                             data.get('fresh_dimension'))
    except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError) as error:
        p.exit(2, f'Invalid input: {error}\n')
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
