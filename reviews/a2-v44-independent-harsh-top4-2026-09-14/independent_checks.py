#!/usr/bin/env python3
"""Finite v44 referee diagnostics, not a proof certificate.

Independent implementation; imports no author code. Requires Python 3, NumPy,
SciPy. Starts at complete support images, NOT empirical laws or analytic
continuation. Run: python independent_checks.py > CHECK_RESULTS.json
"""
from __future__ import annotations
import json
import math
import numpy as np
from scipy.optimize import brentq


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def body(theta: np.ndarray | float, radius: float, amplitude: float,
         phase: float, perturb: list[tuple[int, float, float]], order: int = 0):
    th = np.asarray(theta)
    value = np.full_like(th, radius if order == 0 else 0.0)
    for mode, a, p in [(2, amplitude, 0.0), (3, amplitude/4, phase), *perturb]:
        value += a*mode**order*np.cos(mode*th+p+order*np.pi/2)
    return value


def registration(images: list[tuple[np.ndarray, np.ndarray]], theta: np.ndarray):
    def features(values):
        return (2*np.mean(values*np.exp(1j*theta)),
                np.mean(values*np.exp(-2j*theta)),
                np.mean(values*np.exp(-3j*theta)))
    pairs = [(features(a), features(b)) for a, b in images]
    c0, z20, z30 = pairs[0][0]
    centers = []
    for (c1, z2, z3), (c2, _, _) in pairs:
        require(min(abs(z2), abs(z3), abs(z20), abs(z30)) > 1e-5,
                'Fourier nonvanishing margin failed')
        rotation = z3*z20/(z30*z2)
        centers.append(rotation*c2+c0-rotation*c1)
    v1, v2 = centers[0]-centers[1], centers[0]-centers[2]
    V = np.array([[v1.real, v2.real], [v1.imag, v2.imag]])
    cycle = centers[0]-centers[3]-v1-v2
    return V.T@V, abs(cycle)


def main() -> dict:
    rng = np.random.default_rng(20260914)
    theta = np.arange(4096)*2*np.pi/4096
    max_contact_residual = max_gram_error = max_cycle_error = 0.0
    min_gap = math.inf
    rows = []
    negative_control_residual = None
    symmetric_rejected = False
    for case in range(128):
        eps = [0.005, 0.01][case % 2] if case < 16 else rng.uniform(.005, .01)
        delta = [0.005, 0.01][(case//2) % 2] if case < 16 else rng.uniform(.005, .01)
        A = rng.normal(size=(2, 2))
        T = np.eye(2)+(.01*rng.uniform(.1, 1))*A/np.linalg.norm(A, 2)
        w = .01*rng.uniform(0, 1)*np.exp(1j*rng.uniform(-np.pi, np.pi))
        wvec = np.array([w.real, w.imag])
        # Each perturbation has sum of C0, C1, C2 bounds below 10^-6.
        perturbations = [[(m, rng.uniform(-1, 1)*1e-6/(3*(1+m+m*m)),
                            rng.uniform(-np.pi, np.pi)) for m in (4, 7, 11)]
                         for _ in range(2)]
        specs = [(1., eps, np.pi/4, perturbations[0]),
                 (.75, delta, np.pi/6, perturbations[1])]
        images = []
        for i, j in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            center = T@np.array([4.-8*i, 5.-10*j])+wvec
            center_complex = complex(*center)
            angle = math.atan2(center[1], center[0])
            def derivative(x):
                return (-center[0]*np.sin(x)+center[1]*np.cos(x)
                        -body(x, *specs[0], order=1)
                        -body(x+np.pi, *specs[1], order=1))
            contact = brentq(derivative, angle-np.pi/3, angle+np.pi/3,
                             xtol=5e-15)
            gap = (center[0]*np.cos(contact)+center[1]*np.sin(contact)
                   -body(contact, *specs[0])-body(contact+np.pi, *specs[1]))
            min_gap = min(min_gap, float(gap))
            def point(x, spec):
                return complex(body(x, *spec), body(x, *spec, order=1))*np.exp(1j*x)
            p = point(contact, specs[0])
            q = center_complex+point(contact+np.pi, specs[1])
            max_contact_residual = max(max_contact_residual,
                                       abs(q-p-gap*np.exp(1j*contact)))
            # Independently posed complete recovered images; no T is passed
            # into the registration routine.
            frame_angle = rng.uniform(-np.pi, np.pi)
            frame_origin = complex(*rng.uniform(-5, 5, size=2))
            def image(spec, c):
                shift = (c-frame_origin)*np.exp(-1j*frame_angle)
                return body(theta+frame_angle, *spec)+np.real(shift*np.exp(-1j*theta))
            images.append((image(specs[0], 0j), image(specs[1], center_complex)))
        G, cycle = registration(images, theta)
        L = T@np.diag([8., 10.])
        max_gram_error = max(max_gram_error, float(np.max(abs(G-L.T@L))))
        max_cycle_error = max(max_cycle_error, cycle)
        if case == 0:
            corrupt = [(a.copy(), b.copy()) for a, b in images]
            corrupt[3][1][:] += .002*np.cos(theta)
            _, negative_control_residual = registration(corrupt, theta)
            require(negative_control_residual > .0019, 'Cycle negative control missed')
            symmetric = [(np.ones_like(theta)+.008*np.cos(2*theta),
                          np.ones_like(theta)*.75) for _ in range(4)]
            try:
                registration(symmetric, theta)
            except RuntimeError:
                symmetric_rejected = True
        rows.append(float(np.linalg.norm(T-np.eye(2), 2)))
    require(min_gap > 4.3, 'Gap diagnostic failed')
    require(max_contact_residual < 1e-10, 'Contact diagnostic failed')
    require(max_gram_error < 1e-7 and max_cycle_error < 1e-7,
            'Image registration diagnostic failed')
    require(symmetric_rejected, 'Zero-mode negative control missed')

    u = np.linspace(-.22, .22, 89)
    d, anchor = .8, .19
    S = lambda x: .8*x*x+.11*x**3+.03*x**4+.004*x**5+.006*x**6
    B = lambda x: np.exp(.3*x+.1*x*x)
    f = lambda x, y: 3.7*B(x)*B(y)*(d-S(x)-S(y))
    R = lambda x, y: f(x, y)*f(0., 0.)/(f(x, 0.)*f(0., y))
    t = (1-R(u, anchor))/np.sqrt(1-R(anchor, anchor))
    estimated = d*t/(1+t)
    amp = f(u, 0.)/f(0., 0.)*(1+t)
    serror, berror = float(max(abs(estimated-S(u)))), float(max(abs(amp-B(u))))
    require(serror < 1e-11 and berror < 1e-11, 'Single-offset inverse diagnostic failed')
    require(float(max(abs(S(u)-S(-u)))) > 1e-3, 'Example accidentally even')
    return {
        'scope': 'Finite diagnostics only; no empirical-law-to-jet or analytic-continuation certificate.',
        'seed': 20260914,
        'geometry': {'cases': 128, 'channel_solves': 512,
                     'higher_support_modes': [4, 7, 11],
                     'independent_channel_poses': True,
                     'minimum_gap': min_gap,
                     'max_contact_vector_residual': max_contact_residual,
                     'max_lattice_gram_error': max_gram_error,
                     'max_redundant_cycle_residual': max_cycle_error},
        'negative_controls': {'corrupted_fourth_channel_detected': True,
                              'corrupted_cycle_residual': negative_control_residual,
                              'vanishing_third_mode_rejected': symmetric_rejected},
        'single_offset': {'non_even_action': True, 'unknown_nonconstant_amplitude': True,
                          'max_action_error': serror, 'max_amplitude_error': berror},
        'passed': True,
        'mathematical_certification': False
    }

if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
