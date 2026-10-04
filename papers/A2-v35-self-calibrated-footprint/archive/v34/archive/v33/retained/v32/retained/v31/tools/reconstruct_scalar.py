#!/usr/bin/env python3
"""Finite building blocks for A2 v30's constructive scalar inverse.

CLI: python3 tools/reconstruct_scalar.py input.json output.json
Input: {"points": [[x,y],...], "balances": [[d0,...,dm-1],...],
        "sigma": positive_number, "window": [xmin,xmax,ymin,ymax],
        "outer_cutoff": nonnegative_number}
Each balance is forward mean minus the correctly translated reverse mean.
Output includes raw hulls and explicitly does NOT certify input calibration,
continuum priors, a patch margin, or floating-point interval enclosures.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
from pathlib import Path
from typing import Sequence
import numpy as np
from scipy.spatial import cKDTree


def chain_inverse(differences: np.ndarray) -> np.ndarray:
    """Return clipped negative prefix minima for N chains of length m."""
    d = np.asarray(differences, dtype=float)
    if d.ndim != 2 or d.shape[1] == 0 or not np.isfinite(d).all():
        raise ValueError('balances must be a finite N by m array, m >= 1')
    partial = np.concatenate((np.zeros((len(d), 1)), np.cumsum(d, axis=1)), axis=1)
    return np.clip(-np.min(partial, axis=1), 0.0, 1.0)


def bellman_inverse(transition: Sequence[Sequence], forcing: Sequence,
                    steps: int, clip: bool = True) -> list:
    """Exact for Fraction inputs; caller must establish the zero-hitting bound."""
    if steps < 0 or not isinstance(steps, int):
        raise ValueError('steps must be a nonnegative integer')
    n = len(forcing)
    if len(transition) != n or any(len(row) != n for row in transition):
        raise ValueError('transition must be square and match the forcing')
    for row in transition:
        if any(x < 0 for x in row) or sum(row) != 1:
            raise ValueError('each transition row must be nonnegative and sum exactly to one')
    value = [0] * n
    for _ in range(steps):
        value = [max(0, sum(row[j] * value[j] for j in range(n)) - forcing[i])
                 for i, row in enumerate(transition)]
        if clip:
            value = [min(1, x) for x in value]
    return value


def convex_hull(points: np.ndarray) -> np.ndarray:
    """Monotone-chain hull; float predicates are not interval certification."""
    pts = sorted(set(map(tuple, np.asarray(points, dtype=float))))
    if len(pts) < 3:
        return np.asarray(pts, dtype=float).reshape(-1, 2)
    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return np.asarray(lower[:-1]+upper[:-1], dtype=float)


def threshold_hulls(points: np.ndarray, occupation: np.ndarray, sigma: float,
                    window: Sequence[float] | None = None,
                    outer_cutoff: float = 0.0) -> list[np.ndarray]:
    """Threshold at 1/2 and join all retained nodes at distance <= 4 sigma."""
    points = np.asarray(points, dtype=float)
    values = np.asarray(occupation, dtype=float)
    if (points.ndim != 2 or points.shape[1] != 2 or values.shape != (len(points),)
            or not np.isfinite(points).all() or not np.isfinite(values).all()):
        raise ValueError('points and occupation must be finite and have matching shapes')
    if not np.isfinite(sigma) or sigma <= 0 or outer_cutoff < 0:
        raise ValueError('sigma must be positive and cutoff nonnegative')
    if window is not None:
        if len(window) != 4 or not np.isfinite(window).all():
            raise ValueError('window must have four finite bounds')
        xmin, xmax, ymin, ymax = map(float, window)
        if xmin >= xmax or ymin >= ymax:
            raise ValueError('window has reversed bounds')
    selected = points[values >= .5]
    if not len(selected):
        return []
    tree = cKDTree(selected)
    unused = np.ones(len(selected), dtype=bool)
    result = []
    for start in range(len(selected)):
        if not unused[start]:
            continue
        queue = [start]; unused[start] = False; at = 0
        while at < len(queue):
            neighbors = tree.query_ball_point(selected[queue[at]], 4*sigma)
            at += 1
            for j in neighbors:
                if unused[j]:
                    unused[j] = False; queue.append(j)
        hull = convex_hull(selected[queue])
        if len(hull) < 3:
            continue
        if window is not None:
            clearance = min(hull[:,0].min()-xmin, xmax-hull[:,0].max(),
                            hull[:,1].min()-ymin, ymax-hull[:,1].max())
            if clearance <= outer_cutoff:
                continue
        result.append(hull)
    return sorted(result, key=lambda h: (float(h[:,0].mean()), float(h[:,1].mean())))


def support(hull: np.ndarray, angles: np.ndarray) -> np.ndarray:
    hull = np.asarray(hull, dtype=float)
    angles = np.asarray(angles, dtype=float)
    if hull.ndim != 2 or hull.shape[1] != 2 or len(hull) == 0:
        raise ValueError('nonempty planar hull required')
    normals = np.stack((np.cos(angles), np.sin(angles)), axis=-1)
    return np.max(normals @ hull.T, axis=-1)


def lock_rational(value: float, max_denominator: int, error: float) -> Fraction:
    """Unique bounded-denominator rational in a certified input error interval.

    This numeric convenience routine uses floats; it does not certify that
    its error argument bounds the true real-coordinate error.
    """
    if (max_denominator < 1 or not np.isfinite(value) or not np.isfinite(error)
            or error < 0 or 2*error >= 1/max_denominator**2):
        raise ValueError('invalid or nonseparating rational interval')
    found = set()
    for q in range(1, max_denominator+1):
        for p in range(int(np.ceil((value-error)*q)), int(np.floor((value+error)*q))+1):
            found.add(Fraction(p, q))
    if len(found) != 1:
        raise ValueError('interval does not identify exactly one rational')
    return found.pop()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    occupation = chain_inverse(np.asarray(data['balances']))
    hulls = threshold_hulls(np.asarray(data['points']), occupation, float(data['sigma']),
                            data.get('window'), float(data.get('outer_cutoff', 0)))
    payload = {'occupation': occupation.tolist(), 'raw_hulls': [h.tolist() for h in hulls],
               'numeric_scope': 'finite chain and threshold/hull stages only',
               'interval_certified': False, 'physical_sensor_executed': False,
               'period_margin_verified': False}
    args.output.write_text(json.dumps(payload, indent=2)+'\n')

if __name__ == '__main__':
    main()
