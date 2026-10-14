#!/usr/bin/env python3
"""Deterministic finite fixtures. They are not continuum proof certificates."""
import math
import numpy as np


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    q = 47 / 53
    sigma = math.sqrt(q)
    inverse_constant = (0.47 / 2) / (1 - q)
    weighted_constant = inverse_constant * (1 + 2 * sigma / (1 - sigma))
    cases = 0
    max_scaled_entry = 0.0
    for n in (1, 2, 7, 20, 48):
        m = n + 1
        d = np.minimum(np.arange(1, m), m - np.arange(1, m))
        for phase in (0.0, 0.7, 1.3):
            c = 10.0 ** (-8 * (0.5 + 0.5 * np.sin(np.arange(n) + phase)))
            t = 1 / (0.06 + 0.8 * (0.5 + 0.5 * np.cos(np.arange(n + 1) + phase)))
            diag = t[:-1] + t[1:] + 2 / (0.47 * c)
            A = np.diag(diag)
            if n > 1:
                A += np.diag(-t[1:-1], 1) + np.diag(-t[1:-1], -1)
            N = A * c[np.newaxis, :]
            Ni = np.linalg.inv(N)
            Ai = c[:, np.newaxis] * Ni
            dist = np.abs(np.arange(n)[:, None] - np.arange(n)[None, :])
            bound = inverse_constant * np.minimum(c[:, None], c[None, :]) * q ** dist
            require(np.all(np.abs(Ai) <= bound * (1 + 1e-8)), 'refined inverse bound')
            w = sigma ** d
            weighted_rows = np.sum(np.abs(Ni) * w[None, :] / w[:, None], axis=1)
            require(float(weighted_rows.max()) <= weighted_constant, 'weighted inverse norm')
            require(np.max(np.abs(N @ Ni - np.eye(n))) < 1e-7, 'inverse residual')
            max_scaled_entry = max(max_scaled_entry, float(np.max(np.abs(Ai) / bound)))
            cases += 1
    # The weighted nonlinear row factor never grows with depth.
    for order in (2, 3, 4):
        for chi in (0.1, 0.03, 0.001):
            for depth in range(1000):
                factor = chi ** -1 * q ** (((order - 1) / 2 - 1 / 4) * depth)
                require(factor <= chi ** -1 * (1 + 1e-13), 'nonlinear weighted factor')
    # The complete clearance-guard budget has no collision-count multiplier.
    cap = 2 / (1 - q ** 0.25)
    for m in (1, 2, 17, 100, 10000):
        total = sum(q ** (min(j, m - 1 - j) / 4) for j in range(m))
        require(total <= cap * (1 + 1e-12), 'guard summability')
    # Reversible determinant and polar normalization on a concrete quadratic word.
    H = np.array([[4.0, -0.3], [-0.3, 5.0]])
    h00, h01, h11 = H[0, 0], H[0, 1], H[1, 1]
    M = np.array([[-h00/h01, -1/h01], [-np.linalg.det(H)/h01, -h11/h01]])
    S = np.diag([1., -1.])
    P = S @ np.linalg.inv(M) @ S @ M
    cstar = 91 / (10000 * math.pi)
    J = 1 / (0.46 * cstar * math.sqrt(abs(np.linalg.det(np.eye(2) - P))))
    w0 = abs(h01) / (4 * math.pi * 0.46 * cstar)
    require(math.isclose(J, 2 * math.pi * w0 / math.sqrt(np.linalg.det(H)), rel_tol=1e-11), 'square-root source normalization')
    # A physical half-circle and quadrant: direct angular coarea, no radial 1/r.
    count = 131072
    theta = (np.arange(count) + 0.5) * (2 * math.pi / count)
    x, y = np.cos(theta), np.sin(theta)
    half = x > 0
    quad = half & (y > 0)
    require(abs(half.mean() - 0.5) < 1e-12 and abs(quad.mean() - 0.25) < 1e-12, 'physical fractions')
    for radius in (1e-6, 0.01, 0.2):
        K = 2.0
        relative = np.exp(K * radius * np.cos(theta + 0.17))
        masks = [quad, half & (y <= 0)]
        errors = []
        for mask in masks:
            mass = float(mask.mean())
            value = float((relative * mask).mean())
            require(math.exp(-K*radius)*mass <= value <= math.exp(K*radius)*mass, 'multiplicative profile')
            errors.append(abs(value-mass))
        require(sum(errors) <= math.expm1(K*radius) * half.mean(), 'label-vector relative error')
    # Uniform absolute second derivatives do NOT license uniform tangent fractions.
    fractions = []
    for a in (1.0, 1e-2, 1e-4):
        r = 0.05
        mask = a * r * y - r*r*x*x > 0
        fractions.append(float(mask.mean()))
    require(fractions[-1] < 0.1 and fractions[0] > 0.45, 'angular-loss regression')
    # The positive atomic-to-collar inequality is one-sided with its explicit loss.
    for tangent in (0.0, 0.25, 0.5, 1.0):
        samples = np.array([0.0, 0.1, 0.7, 1.0])
        require(tangent <= samples.mean() + np.maximum(tangent-samples, 0).mean() + 1e-15, 'positive loss comparison')
    return {'matrix_cases': cases, 'refined_inverse_checked': True,
            'weighted_nonlinear_rows_checked': True, 'guard_geometric_sum_checked': True,
            'reversible_square_root_checked': True, 'polar_source_fraction_checked': True,
            'relative_vector_profile_checked': True, 'angular_loss_not_assumed_zero': True,
            'atomic_collar_comparison_checked': True,
            'continuum_proof_certified': False}


if __name__ == '__main__':
    import json
    print(json.dumps(finite_checks(), indent=2, sort_keys=True))
