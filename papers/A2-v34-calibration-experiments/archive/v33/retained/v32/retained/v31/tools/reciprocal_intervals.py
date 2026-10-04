#!/usr/bin/env python3
"""Exact rational Bellman enclosures on a finite killed observation grid.

The enclosures concern a caller-supplied forcing interval. Occupation bounds
add a caller-certified survival tail; this program neither verifies geometric
priors nor estimates physical calibration from collision bits. No wraparound
or direction-resolved output is used. See --help for the JSON interface.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from typing import Sequence

F = Fraction


def rational(value: str | int | F) -> F:
    """Accept exact integer/fraction strings, never silently coerce a float."""
    if isinstance(value, bool) or not isinstance(value, (str, int, F)):
        raise ValueError('rational inputs must be integers or exact strings')
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('invalid rational input') from exc


def natural(value: int, name: str, positive: bool = False) -> int:
    if type(value) is not int or value < int(positive):
        raise ValueError(name + ' must be ' + ('positive' if positive else 'nonnegative'))
    return value


@dataclass(frozen=True)
class KilledKernel:
    """Substochastic rational rows. Missing mass is killed, not renormalized."""
    rows: tuple[tuple[tuple[int, F], ...], ...]

    def __post_init__(self) -> None:
        n = len(self.rows)
        if n == 0:
            raise ValueError('empty transition kernel')
        for row in self.rows:
            total = F(0)
            for index, weight in row:
                if type(index) is not int or not 0 <= index < n:
                    raise ValueError('transition index out of bounds')
                if not isinstance(weight, F) or weight < 0:
                    raise ValueError('weights must be nonnegative Fractions')
                total += weight
            if total > 1:
                raise ValueError('transition row mass exceeds one')

    @property
    def size(self) -> int:
        return len(self.rows)

    def apply(self, values: Sequence[F]) -> list[F]:
        if len(values) != self.size or any(not isinstance(x, F) for x in values):
            raise ValueError('value array must match kernel and use Fractions')
        return [sum((p * values[j] for j, p in row), F(0)) for row in self.rows]


def compass_kernel(width: int, height: int, step: int = 1) -> KilledKernel:
    """Four exact shifts by step grid indices; out-of-aperture states are zero."""
    natural(width, 'width', True); natural(height, 'height', True)
    natural(step, 'step', True)
    rows = []
    for y in range(height):
        for x in range(width):
            row = []
            for dx, dy in ((step, 0), (-step, 0), (0, step), (0, -step)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < width and 0 <= yy < height:
                    row.append((yy * width + xx, F(1, 4)))
            rows.append(tuple(row))
    return KilledKernel(tuple(rows))


def clip(value: F) -> F:
    return min(F(1), max(F(0), value))


def enclose(kernel: KilledKernel, forcing_lower: Sequence[F],
            forcing_upper: Sequence[F], iterations: int,
            survival_upper: F = F(1)) -> dict[str, list[F]]:
    """Enclose the exact iterate; occupation enclosure is conditional on the tail.

    A forcing interval alone always encloses the clipped exact iterate.
    The occupation interpretation additionally requires the physical nonnegative
    solution and the mean-exit/locality hypotheses in the manuscript.
    """
    natural(iterations, 'iterations')
    low, high = list(forcing_lower), list(forcing_upper)
    if len(low) != kernel.size or len(high) != kernel.size:
        raise ValueError('forcing shape differs from transition kernel')
    if any(not isinstance(x, F) for x in low + high):
        raise ValueError('forcing entries must be Fractions')
    if any(a > b for a, b in zip(low, high)):
        raise ValueError('reversed forcing interval')
    if not isinstance(survival_upper, F) or not 0 <= survival_upper <= 1:
        raise ValueError('survival bound must be a Fraction in [0,1]')
    vl = [F(0)] * kernel.size
    vu = vl.copy()
    for _ in range(iterations):
        tl, tu = kernel.apply(vl), kernel.apply(vu)
        vl = [clip(x - g) for x, g in zip(tl, high)]
        vu = [clip(x - g) for x, g in zip(tu, low)]
    return {'iterate_lower': vl, 'iterate_upper': vu,
            'occupation_lower': vl,
            'occupation_upper': [min(F(1), x + survival_upper) for x in vu]}


def geometric_tail(iterations: int, block_length: int) -> F:
    natural(iterations, 'iterations'); natural(block_length, 'block_length', True)
    return F(1, 2 ** (iterations // block_length))


def solve_payload(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError('input must be a JSON object')
    required = {'width', 'height', 'step', 'iterations', 'forcing_lower',
                'forcing_upper', 'certified_survival_upper'}
    if set(payload) != required:
        raise ValueError('JSON keys must be exactly: ' + ', '.join(sorted(required)))
    kernel = compass_kernel(payload['width'], payload['height'], payload['step'])
    result = enclose(kernel, [rational(x) for x in payload['forcing_lower']],
                     [rational(x) for x in payload['forcing_upper']],
                     payload['iterations'], rational(payload['certified_survival_upper']))
    return {'schema': 'a2-v31-rational-enclosures-1',
            'boundary': 'killed_zero_extension_not_periodic',
            'conditional_on_supplied_forcing_and_survival_bounds': True,
            'physical_sensor_executed': False, 'formal_proof_certificate': False,
            'bounds': {key: [str(x) for x in values] for key, values in result.items()}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='JSON with width, height, step, iterations, '
                        'forcing_lower/upper arrays and certified_survival_upper')
    parser.add_argument('--output', type=Path, help='output JSON; otherwise print')
    args = parser.parse_args()
    try:
        result = solve_payload(json.loads(args.input.read_text()))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.error(str(exc))
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
