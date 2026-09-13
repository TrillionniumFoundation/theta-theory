#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v36 referee-style review.

These checks are not theorem proofs, native TeX builds, or a test of every
manuscript input. The radial probability models are not asserted to be
realized by billiard channels. No network access or repository writes occur.
Run with Python 3, NumPy and SciPy; checks remain active under python -O.
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import solve_banded

PINNED_COMMIT = "0802bfa20533feff55bf5620d39d6399d5e778f5"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def density_inverse() -> dict:
    d, a, z = 0.4, 0.22, 7.3
    def action(u):
        return 0.65*u*u + 0.12*u**3 + 0.04*u**4
    def amplitude(u):
        return math.exp(0.2*u + 0.1*u*u)
    def density(u, v):
        return amplitude(u)*amplitude(v)*(d-action(u)-action(v))/z
    def ratio(u, v):
        return density(u, v)*density(0, 0)/(density(u, 0)*density(0, v))
    anchor = math.sqrt(1-ratio(a, a))
    errors_s, errors_b = [], []
    for u in np.linspace(-0.3, 0.3, 31):
        t = (1-ratio(float(u), a))/anchor
        errors_s.append(abs(d*t/(1+t)-action(u)))
        errors_b.append(abs(density(u, 0)/density(0, 0)*(1+t)-amplitude(u)))
    require(max(errors_s + errors_b) < 1e-11, "Four-density cancellation failed")
    return {"points": 31, "signed_asymmetric_model": True,
            "max_action_error": max(errors_s), "max_amplitude_error": max(errors_b)}


def jet_algebra() -> dict:
    geometries = [(0.8, 0.7, 1.8), (1.2, 0.15, 3.5), (2.0, 2.0, 0.25)]
    det_errors, recovery_errors = [], []
    for g, k0, k1 in geometries:
        c0, c1 = 1+g*k0, 1+g*k1
        gamma = math.acosh(math.sqrt(c0*c1))
        rb = math.sqrt(c0/c1)
        ab0 = math.sqrt(c0*c1)*math.sinh(gamma)/(g*c1)
        ab1 = math.sqrt(c0*c1)*math.sinh(gamma)/(g*c0)
        recovered_gamma = math.asinh(g*math.sqrt(ab0*ab1))
        recovered_k0 = (math.cosh(recovered_gamma)*math.sqrt(ab0/ab1)-1)/g
        recovered_k1 = (math.cosh(recovered_gamma)*math.sqrt(ab1/ab0)-1)/g
        recovery_errors += [abs(recovered_gamma-gamma), abs(recovered_k0-k0), abs(recovered_k1-k1)]
        for n in range(3, 33):
            q = math.exp(-n*gamma)
            diagonal = (1+q*q)/(1-q*q)
            off0 = 2*(rb*math.exp(-gamma))**n/(1-q*q)
            off1 = 2*(math.exp(-gamma)/rb)**n/(1-q*q)
            det_errors.append(abs(diagonal*diagonal-off0*off1-1))
    require(max(det_errors + recovery_errors) < 2e-12, "Jet algebra failed")
    return {"geometries": len(geometries), "jet_blocks": len(det_errors),
            "orders": [3, 32], "max_determinant_error": max(det_errors),
            "max_leading_recovery_error": max(recovery_errors)}


def finite_halfline_envelope() -> dict:
    """Solve a finite nonlinear stationary bridge, then evaluate its envelope.

    Averaging the normalized coefficient at +u and -u cancels the first
    odd-in-u correction. Its difference from the infinite linear-orbit
    coefficient is an approximation error, not an exact identity test.
    """
    g, curvatures = 0.8, np.array([0.7, 1.8])
    cubic, quartic = np.array([0.3, -0.25]), np.array([0.2, 0.4])
    c = 1+g*curvatures
    gamma = math.acosh(math.sqrt(float(c[0]*c[1])))
    flights = 64
    endpoint_scale = 1e-3
    max_residual, max_error = 0.0, 0.0
    for b in (0, 1):
        types = (b+np.arange(flights+1)) % 2
        coefficients = []
        for u in (endpoint_scale, -endpoint_scale):
            i = np.arange(flights+1)
            rb = math.sqrt(float(c[b]/c[1-b]))
            x = u*np.exp(-gamma*i)*np.where(i % 2, rb, 1.0)
            x[-1] = 0.0
            def flights_data(xx):
                k, q3, q4 = curvatures[types], cubic[types], quartic[types]
                psi = k*xx**2/2+q3*xx**3/6+q4*xx**4/24
                dp = k*xx+q3*xx**2/2+q4*xx**3/6
                ddp = k+q3*xx+q4*xx**2/2
                h = g+psi[:-1]+psi[1:]
                dx = xx[1:]-xx[:-1]
                length = np.hypot(h, dx)
                num_l, num_r = h*dp[:-1]-dx, h*dp[1:]+dx
                gl, gr = num_l/length, num_r/length
                hll = (dp[:-1]**2+h*ddp[:-1]+1)/length-num_l**2/length**3
                hrr = (dp[1:]**2+h*ddp[1:]+1)/length-num_r**2/length**3
                hlr = (dp[:-1]*dp[1:]-1)/length-num_l*num_r/length**3
                return h, length, gl, gr, hll, hrr, hlr
            for iteration in range(20):
                h, length, gl, gr, hll, hrr, hlr = flights_data(x)
                grad = gr[:-1]+gl[1:]
                residual = float(np.max(np.abs(grad)))
                if residual < 5e-15:
                    break
                band = np.zeros((3, flights-1))
                band[1] = hrr[:-1]+hll[1:]
                band[0, 1:] = hlr[1:-1]
                band[2, :-1] = hlr[1:-1]
                x[1:-1] -= solve_banded((1, 1), band, grad)
            require(residual < 5e-15, "Nonlinear stationary solve did not converge")
            max_residual = max(max_residual, residual)
            values = {}
            for n in (3, 4, 7):
                for r in (0, 1):
                    monomial = (types == r)*(x/u)**n
                    values[n, r] = float(np.sum(h/length*(monomial[:-1]+monomial[1:])))
            coefficients.append(values)
        for (n, r), value in coefficients[0].items():
            average = (value+coefficients[1][n, r])/2
            diagonal = 1/math.tanh(n*gamma)
            expected = diagonal if r == b else rb**n/math.sinh(n*gamma)
            max_error = max(max_error, abs(average-expected))
    require(max_error < 2e-6, "Nonlinear envelope diagnostic exceeded its tolerance")
    return {"finite_flights": flights, "starting_types": 2,
            "endpoint_magnitudes": [endpoint_scale], "orders": [3, 4, 7],
            "stationary_solves": 4, "max_stationarity_residual": max_residual,
            "max_symmetric_envelope_error": max_error, "coefficient_tolerance": 2e-6}


def lattice_and_reflection() -> dict:
    marked = np.array([[2.0, 1.0], [0.0, 3.0]])  # Independent, not unimodular.
    lattice = np.array([[1.7, 0.4], [0.2, 1.2]])
    reflection = np.diag([1.0, -1.0])
    holonomy = lattice @ marked
    inverse_marked = np.linalg.inv(marked)
    recovered = holonomy @ inverse_marked
    gram = inverse_marked.T @ holonomy.T @ holonomy @ inverse_marked
    reflected = (reflection @ holonomy) @ inverse_marked
    error = max(float(np.max(np.abs(recovered-lattice))),
                float(np.max(np.abs(gram-lattice.T@lattice))),
                float(np.max(np.abs(reflected-reflection@lattice))),
                float(np.max(np.abs(reflected.T@reflected-gram))))
    perturbation = np.array([[0.003, -0.002], [0.001, 0.004]])
    lhs = np.linalg.norm(perturbation@inverse_marked, 2)
    rhs = np.linalg.norm(perturbation, 2)*np.linalg.norm(inverse_marked, 2)
    require(error < 2e-12 and lhs <= rhs+1e-15, "Holonomy/Gram diagnostic failed")
    return {"marked_cycle_determinant": 6, "max_identity_error": error,
            "perturbation_norm": float(lhs), "proved_bound_evaluated": float(rhs)}


def moving_ceiling_layer() -> dict:
    """Exact finite layer formulas for a radial model with U=-1.

    q_theta(u,v,r)=2/[pi(1+theta)^2] on
    0<r<1+theta-u^2-v^2, theta=z/k. The finite intensity includes the
    corner outside D when z>0; the target is on D only. The common-bulk
    conditional distribution is exactly parameter independent in this model.
    """
    R = 3.0
    rows = []
    for k in (64, 256, 1024, 4096):
        for z in (-1.0, 0.0, 0.8):
            factor = (1+z/k)**-2
            p = factor*(2*(R+z)/k+(z*z-R*R)/(k*k))
            target_mass = 2*(R+z)
            lower = -z
            positive_start = max(lower, 0.0)
            l1 = (2*abs(factor-1)*((R-positive_start)-(R*R-positive_start**2)/(2*k))
                  +(R*R-positive_start**2)/k)
            if lower < 0:
                l1 += 2*abs(factor-1)*(-lower)+factor*lower*lower/k
            require(0 < p < 1, "Invalid layer probability")
            require(abs(k*p-target_mass) <= l1+1e-12, "Layer variation cannot bound its mass error")
            require(k*l1 < 30 and k*k*p*p < 70, "Finite layer error budget failed")
            rows.append({"k": k, "z": z, "layer_probability": p,
                         "intensity_mass_error": abs(k*p-target_mass),
                         "intensity_L1_error": l1, "k_times_L1_error": k*l1,
                         "binomial_poisson_bound_scale_kp2": k*p*p})
    return {"model_not_claimed_billiard_realizable": True,
            "reference_strip_R": R, "common_bulk_conditional_error": 0,
            "cases": rows}


def alternative_mean() -> dict:
    """Stable evaluation of the exact mean in an explicit radial density.

    f_theta(x)=2/[pi(1+theta)^2]*(1+theta-|x|^2)_+ on R^2.
    On the null support s=1-|x|^2, the score is 1/s-2 and J=2.
    Effective sample weight np is set algebraically to 1/(delta^2*ell).
    """
    errors = []
    for ell in (16.0, 64.0, 256.0, 1024.0):
        delta = math.exp(-ell)  # Underflow at ell=1024 removes negligible terms.
        q = delta*ell**0.25
        largest = 0.0
        for h in (-1.0, 0.0, 0.5, 1.2):
            mean = 2*(delta*ell**0.5-ell**0.25
                      +h*(ell-0.25*math.log(ell)-2+2*q))/(ell*(1+delta*h)**2)
            largest = max(largest, abs(mean-2*h))
        errors.append({"ell": ell, "max_mean_error": largest,
                       "truncation_mean_budget": ell**-0.75,
                       "single_sum_fourth_moment_budget": ell**-1.5})
    require(errors[-1]["max_mean_error"] < 0.03, "Alternative-mean asymptotic diagnostic failed")
    require(all(errors[i+1]["max_mean_error"] < errors[i]["max_mean_error"]
                for i in range(len(errors)-1)), "Mean diagnostic did not improve")
    return {"boundary_information": 2, "model_not_claimed_billiard_realizable": True,
            "cases": errors}


def main() -> None:
    result = {
        "status": "PASS",
        "pinned_manuscript_commit": PINNED_COMMIT,
        "scope": "Six finite diagnostic families; not a theorem or native-build certificate.",
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checks": {"four_density_inverse": density_inverse(),
                   "finite_jet_algebra": jet_algebra(),
                   "nonlinear_finite_halfline_envelope": finite_halfline_envelope(),
                   "lattice_and_common_reflection": lattice_and_reflection(),
                   "moving_ceiling_layer": moving_ceiling_layer(),
                   "original_alternative_mean": alternative_mean()},
    }
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
