#!/usr/bin/env python3
"""Exact rational calibration for the explicit A2 v25 recognition theorem.

Inputs are certified positive numerical *bounds*, not a table description.
This program does not verify that those bounds define a nonempty physical class.
Huge integers are represented as finite arithmetic expressions, not rounded to 0.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
from typing import Any

FIELDS = ('rho', 'M', 'R', 'M_g', 'kappa_min', 'R_plus', 'D_0',
          'eta', 'sigma', 'd_0')


def ceil(q: F) -> int:
    return -(-q.numerator // q.denominator)


def upper_log2(q: F) -> int:
    """Return the least nonnegative m with 2**m >= q, without float logs."""
    if q <= 0:
        raise ValueError('logarithm bound requires a positive rational')
    m = max(0, q.numerator.bit_length() - q.denominator.bit_length())
    if q.denominator * (1 << m) < q.numerator:
        m += 1
    while m and q.denominator * (1 << (m - 1)) >= q.numerator:
        m -= 1
    return m


def rational_inputs(data: dict[str, Any]) -> dict[str, F]:
    if set(data) != set(FIELDS):
        raise ValueError('Expected exactly these fields: ' + ', '.join(FIELDS))
    out: dict[str, F] = {}
    for name in FIELDS:
        value = data[name]
        if isinstance(value, bool) or not isinstance(value, (str, int)):
            raise ValueError(name + ': use an integer or an exact rational string')
        out[name] = F(value)
        if out[name] <= 0:
            raise ValueError(name + ': must be positive')
    return out


def calibrate(data: dict[str, Any]) -> dict[str, Any]:
    p = rational_inputs(data)
    r = p['R'] / 4
    H = 1 + 2 * p['M_g'] / p['R']
    u = p['kappa_min'] * r / 4
    a = min(p['rho'] / 8, u / (1 + u), F(1, 2))
    # 3**ceil(rho) is an intentionally conservative bound for exp(rho).
    B = 2 * (p['M'] + (p['R_plus'] + p['D_0']) * 3**ceil(p['rho']))
    C = 3 + 9 * (p['R_plus'] + 2 * p['D_0']) / p['eta']
    Delta = min(B, p['sigma']/36, p['eta']/36, p['d_0']/(4*C))
    J = ceil(4/a)
    m0 = max(1, upper_log2(3*B/Delta))
    tail_extra = upper_log2(64*p['M_g']/(7*B))
    c1 = max(1, ceil(4*H*r/B))
    # P can itself have a prohibitively long binary expansion. Keep the exact
    # expression P=m0*2**(J+3). K=P+tail_extra+2 is conservative and avoids division.
    return {
        'schema': 'a2-v25-symbolic-rational-calibration-1',
        'input_bounds': {k: str(p[k]) for k in FIELDS},
        'rational_constants': {k: str(v) for k,v in
            {'r':r, 'H':H, 'a':a, 'B':B, 'C_star':C, 'Delta_star':Delta}.items()},
        'integers': {'J':J, 'm0':m0, 'tail_extra':tail_extra, 'c1':c1},
        'exact_expressions': {
            'theta_star': f'2**(-{J+3})',
            'P': f'{m0} * 2**{J+3}',
            'E_star': f'({B}) * 2**(-P)',
            'chi_star': 'E_star / 8',
            'K': f'P + {tail_extra+2}',
            'N': f'max(2, {c1} * 2**P)',
            'value_fingerprint_dimension': '1 + 2*(N+1)',
        },
        'claims': {
            'exact_rational_and_symbolic_arithmetic': True,
            'expanded_all_fingerprint_coordinates': False,
            'physical_prior_nonemptiness_verified': False,
            'physical_sensor_executed': False,
            'polynomial_dependence_on_prior_margins': False,
            'formal_proof_certificate': False,
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bounds', type=Path, help='JSON file of exact positive rational bounds')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = calibrate(json.loads(args.bounds.read_text()))
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
