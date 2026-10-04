#!/usr/bin/env python3
"""A2 v32 finite primitives, not an apparatus or a physical-prior certificate.

The exact local solver takes supplied rational forcing intervals and a certified
survival bound. The bisection routine requires a supplied ambiguity radius.
Angular interpolation is a floating-point diagnostic/evaluation helper; it does
not convert floating-point results into certified geometric enclosures.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import json
import math
from pathlib import Path
from typing import Callable, Mapping, Sequence

Point = tuple[int, int]
SHIFTS: tuple[Point, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))


@dataclass(frozen=True)
class Interval:
    lower: F
    upper: F

    def __post_init__(self) -> None:
        if not isinstance(self.lower, F) or not isinstance(self.upper, F):
            raise TypeError('interval endpoints must be exact Fractions')
        if self.lower > self.upper:
            raise ValueError('reversed interval')


def diamond(radius: int) -> list[Point]:
    if type(radius) is not int or radius < 0:
        raise ValueError('radius must be a nonnegative integer')
    return [(i, j) for i in range(-radius, radius + 1)
            for j in range(-radius, radius + 1) if abs(i) + abs(j) <= radius]


def _clip(x: F) -> F:
    return min(F(1), max(F(0), x))


def local_interval(forcing: Mapping[Point, Interval], depth: int,
                   inside: Callable[[Point], bool], tail: F) -> dict:
    """Enclose the killed depth iterate at (0,0), then add supplied exit tail.

    Coordinates are integer shifts of the requested laboratory target, not a
    grid at the localization scale. Missing in-aperture forcing is an error.
    States outside the aperture are killed, never wrapped or renormalized.
    """
    if type(depth) is not int or depth < 1:
        raise ValueError('positive integer depth required')
    if not isinstance(tail, F) or not 0 <= tail <= 1:
        raise ValueError('tail must be a Fraction in [0,1]')
    if not inside((0, 0)):
        raise ValueError('target must belong to the aperture')
    needed = [p for p in diamond(depth - 1) if inside(p)]
    for p in needed:
        if p not in forcing or not isinstance(forcing[p], Interval):
            raise ValueError(f'missing forcing interval at {p}')
    zero = Interval(F(0), F(0))
    previous = {p: zero for p in diamond(depth)}
    updates = 0
    for k in range(1, depth + 1):
        current: dict[Point, Interval] = {}
        for i, j in diamond(depth - k):
            p = (i, j)
            if not inside(p):
                current[p] = zero
                continue
            neighbors = [previous[(i + a, j + b)] for a, b in SHIFTS]
            g = forcing[p]
            lo = sum((v.lower for v in neighbors), F(0)) / 4 - g.upper
            hi = sum((v.upper for v in neighbors), F(0)) / 4 - g.lower
            current[p] = Interval(_clip(lo), _clip(hi))
            updates += 1
        previous = current
    v = previous[(0, 0)]
    return {'iterate': v, 'occupation': Interval(v.lower, min(F(1), v.upper + tail)),
            'forcing_centers': len(needed), 'updates': updates,
            'conditional_on_forcing_and_survival': True}


def fuzzy_bisect(label: Callable[[F], bool], lower: F, upper: F,
                 ambiguity: F, steps: int) -> Interval:
    """Return the relaxed radius enclosure, assuming the initial bracket is valid.

    Label one implies radius <= true boundary + ambiguity; label zero implies
    radius >= true boundary - ambiguity. Labels within this layer need not be
    monotone. This routine does not establish the assumption from physical data.
    """
    if not all(isinstance(x, F) for x in (lower, upper, ambiguity)):
        raise TypeError('exact Fraction endpoints and ambiguity required')
    if lower >= upper or ambiguity < 0 or type(steps) is not int or steps < 0:
        raise ValueError('invalid bisection specification')
    for _ in range(steps):
        mid = (lower + upper) / 2
        bit = label(mid)
        if type(bit) is not bool:
            raise TypeError('label callback must return bool')
        if bit:
            lower = mid
        else:
            upper = mid
    return Interval(lower - ambiguity, upper + ambiguity)


def lagrange_weights(x: F, derivative: int = 0) -> list[F]:
    """Exact derivative weights at x on the seven normalized nodes -3,...,3."""
    if not isinstance(x, F) or type(derivative) is not int or not 0 <= derivative <= 6:
        raise ValueError('Fraction x and derivative in 0,...,6 required')
    nodes = list(range(-3, 4))
    result = []
    for node in nodes:
        coef = [F(1)]
        denom = F(1)
        for other in nodes:
            if other == node:
                continue
            nxt = [F(0)] * (len(coef) + 1)
            for j, value in enumerate(coef):
                nxt[j] -= other * value
                nxt[j + 1] += value
            coef = nxt
            denom *= node - other
        for _ in range(derivative):
            coef = [(j + 1) * coef[j + 1] for j in range(len(coef) - 1)]
        result.append(sum((a * x ** j for j, a in enumerate(coef)), F(0)) / denom)
    return result


def _step_jet(r: float) -> tuple[float, float, float, float]:
    if r <= 0:
        return 0.0, 0.0, 0.0, 0.0
    if r >= 1:
        return 1.0, 0.0, 0.0, 0.0
    logit = -1 / r + 1 / (1 - r)
    if logit < -700:
        return 0.0, 0.0, 0.0, 0.0
    if logit > 700:
        return 1.0, 0.0, 0.0, 0.0
    if logit >= 0:
        q = math.exp(-logit)
        v = 1 / (1 + q)
        b = q / (1 + q) ** 2
    else:
        q = math.exp(logit)
        v = q / (1 + q)
        b = q / (1 + q) ** 2
    d1 = 1 / r ** 2 + 1 / (1 - r) ** 2
    d2 = -2 / r ** 3 + 2 / (1 - r) ** 3
    d3 = 6 / r ** 4 + 6 / (1 - r) ** 4
    return (v, b * d1, b * (d2 + (1 - 2 * v) * d1 ** 2),
            b * (d3 + 3 * (1 - 2 * v) * d1 * d2 +
                 (1 - 6 * v + 6 * v * v) * d1 ** 3))


def radial_interpolate(samples: Sequence[float], angle: float) -> tuple[float, ...]:
    """Evaluate a smooth seven-node reconstruction and derivatives through three.

    Returned doubles are evaluations, not interval certifications. A finite
    description consists of these samples and the fixed interpolation rule.
    """
    m = len(samples)
    if m < 9 or not all(math.isfinite(float(x)) for x in samples) or not math.isfinite(angle):
        raise ValueError('at least nine finite samples and a finite angle required')
    h = 2 * math.pi / m
    x = (angle % (2 * math.pi)) / h
    k = math.floor(x)
    r = x - k
    def poly(center: int) -> list[float]:
        z = F(x - center)
        return [sum(float(w) * float(samples[(center + j) % m])
                    for j, w in zip(range(-3, 4), lagrange_weights(z, d)))
                for d in range(4)]
    left, right = poly(k), poly(k + 1)
    weight = _step_jet(r)
    return tuple((left[d] + sum(math.comb(d, j) * weight[j] *
                  (right[d - j] - left[d - j]) for j in range(d + 1))) / h ** d
                 for d in range(4))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', type=Path)
    args = ap.parse_args()
    data = json.loads(args.input.read_text())
    bounds = data['aperture_integer_bounds']
    if (len(bounds) != 4 or any(type(v) is not int for v in bounds)
            or bounds[0] > bounds[1] or bounds[2] > bounds[3]):
        raise ValueError('invalid integer aperture')
    inside = lambda p: bounds[0] <= p[0] <= bounds[1] and bounds[2] <= p[1] <= bounds[3]
    forcing: dict[Point, Interval] = {}
    for row in data['forcing']:
        p = (row['i'], row['j'])
        if p in forcing or any(type(v) is not int for v in p):
            raise ValueError('duplicate or noninteger forcing coordinate')
        forcing[p] = Interval(F(row['lower']), F(row['upper']))
    result = local_interval(forcing, data['depth'], inside, F(data['survival_upper_bound']))
    for name in ('iterate', 'occupation'):
        it = result[name]
        result[name] = [str(it.lower), str(it.upper)]
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
