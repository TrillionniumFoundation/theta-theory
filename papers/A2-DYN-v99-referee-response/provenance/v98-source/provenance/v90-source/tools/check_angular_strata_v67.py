#!/usr/bin/env python3
"""Deterministic finite diagnostics, not a Lorentz simulation or proof certificate."""
import math
import numpy as np


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def finite_checks():
    grid = 65536
    angles = (np.arange(grid) + 0.5) * (2 * math.pi / grid)
    w = np.column_stack((np.cos(angles), np.sin(angles)))
    x = np.linspace(0, 1, 10001)
    require(np.all(2 / math.pi * np.arcsin(x) <= x + 1e-14), 'homogeneous angular chord')
    cases = 0
    for A in [0.001, 0.25, 1.0, 4.0]:
        for L in [0.0, 0.01, 0.5, 2.0]:
            for r in [0.0001, 0.005, 0.1]:
                linear = A * w[:, 0]
                nonlinear = linear - L * r * w[:, 1] ** 2
                changed = np.mean((linear > 0) != (nonlinear > 0))
                require(changed <= min(1.0, L * r / A) + 8 / grid, 'active sign estimate')
                cases += 1
    inactive_cases = 0
    for b in [-0.3, -1e-6, 1e-6, 0.3]:
        for A in [0.0, 0.1, 3.0]:
            for L in [0.0, 0.5]:
                disk = 0.2
                denom = 2 * (A + L * disk)
                rho = min(disk, abs(b) / denom if denom else math.inf)
                r = 0.99 * rho
                f = b + A * r * w[:, 0] - L * r * r * w[:, 1] ** 2
                require(np.all((f > 0) == (b > 0)), 'inactive offset radius')
                inactive_cases += 1
    normals = np.array([[math.cos(v), math.sin(v)] for v in [0, .00001, .7, 1.2, 1.9, 2.8, 3.0]])
    tangent = w @ normals.T > 0
    r = .002
    curvature = np.array([.4, .2, .1, .3, .1, .2, .4])
    actual = w @ normals.T - r * w[:, 1, None] ** 2 * curvature > 0
    def labels(bits):
        # Physical first-hit, initial membership, and terminal membership
        # are separate. The four middle bits determine occupation.
        allowed = bits[:, 0] & bits[:, 1] & bits[:, -1]
        result = np.full(grid, -1, dtype=int)
        result[allowed] = 1 + bits[allowed, 2:-1].sum(axis=1)
        return result
    lt, la = labels(tangent), labels(actual)
    tv_vector = sum(abs(np.mean(lt == n) - np.mean(la == n)) for n in range(1, 6))
    union = np.mean(np.any(tangent != actual, axis=1))
    require(tv_vector <= 2 * union + 1e-14, 'label-vector partition')
    require(union <= min(1.0, r * float(curvature.sum())) + 64 / grid, 'scalar-test union')
    # Affine boundaries with a thin cone: no angle-separation hypothesis.
    eps = 1e-4
    thin = (w[:, 0] > 0) & ((-w[:, 0] + eps * w[:, 1]) > 0)
    thin_scaled = (r * w[:, 0] > 0) & ((-r * w[:, 0] + eps * r * w[:, 1]) > 0)
    require(np.array_equal(thin, thin_scaled), 'thin affine cone')
    # Exact collar averages of a=theta(1-K sqrt(2u)) at s=rmax^2/2.
    beta = np.array([.2, .7, .11, .03])
    K, rmax = 3.0, .02
    Q = beta * (1 - (2 / 3) * K * rmax)
    D = beta * (2 / 3) * K * rmax
    require(float(beta.sum()) <= float(Q.sum()) / (1 - K * rmax), 'positive absorption')
    require(abs(float(D.sum()) - (2 / 3) * K * rmax * float(beta.sum())) < 1e-14, 'integrated loss constant')
    # These atoms may all share one critical value: there is no word-count multiplier.
    require(np.all(beta <= Q / (1 - K * rmax)), 'coincident critical values')
    # Negative control: bounded Hessian, collapsing active gradient.
    small_A, rbad = 1e-8, .01
    bad = small_A * w[:, 0] - rbad * w[:, 1] ** 2 > 0
    collapse_loss = .5 - float(np.mean(bad))
    require(collapse_loss > .45, 'gradient-collapse negative control failed')
    # Negative control: an inactive near-zero offset needs its own radius.
    near = 1e-8 + .01 * w[:, 0] > 0
    require(float(np.mean(near)) < .51, 'inactive offset negative control failed')
    # A zero tangent cone can still carry positive physical nonlinear source.
    zero_cone_actual = (w[:, 0] > 0) & (-w[:, 0] + .1 * w[:, 1] ** 2 > 0)
    require(np.mean(zero_cone_actual) > .01, 'zero-cone source must remain in complement')
    # Abstract radial masks, not Lorentz orbits: f_m=eps_m*x-|y|^2.
    # theta=1/2, but a_m(u)=0 for sqrt(2u)>eps_m; for fixed s,
    # m^2 Q<=eps_m^2/(4s) while m^2 B=1/2 when J=m^-2.
    s = .01
    qbounds = [(m ** -6) ** 2 / (4 * s) for m in [2, 4, 8, 16]]
    require(all(qbounds[j + 1] < qbounds[j] for j in range(3)), 'ordered-limit negative control')
    require(qbounds[-1] < 1e-10, 'finite-width loss must not certify zero-width')
    for p in [.5, 1, 2, 4]:
        for ss in [1e-8, 1e-6]:
            cutoff = ss ** (-1 / (2 * p + 2))
            power = ss ** (p / (2 * p + 2))
            require(abs(cutoff * math.sqrt(ss) - power) < 1e-12, 'conditional moment exponent')
            require(abs(cutoff ** (-p) - power) < 1e-12, 'conditional tail exponent')
    return {'grid_size': grid, 'active_quadratic_cases': cases,
            'inactive_margin_cases': inactive_cases, 'exact_label_partition': True,
            'thin_affine_cone': True, 'positive_absorption': True,
            'averaged_loss_constant_two_thirds': True,
            'gradient_collapse_detected': True, 'inactive_offset_collapse_detected': True,
            'zero_tangent_fraction_positive_source_retained': True,
            'invalid_limit_interchange_detected': True,
            'conditional_moment_exponent_checked': True,
            'all_tests_are_finite_diagnostics': True,
            'lorentz_weighted_tail_certified': False,
            'continuum_proof_certified': False}


if __name__ == '__main__':
    import json
    print(json.dumps(finite_checks(), indent=2, sort_keys=True))
