#!/usr/bin/env python3
"""Independent finite diagnostics for the pinned A2 v35 referee report.

Uses only the Python standard library. Explicit checks remain active under -O.
These calculations do not certify the full manuscript, infinite-dimensional
estimates, uniform asymptotics, physical realization, or TeX compilation.
"""
from __future__ import annotations

from fractions import Fraction as F
import json
import math

SOURCE_COMMIT = "1c50ef04fc2863b4744b5312b539cb68265054f3"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def rational_sqrt(value: F) -> F:
    require(value >= 0, "Negative rational square")
    n, d = math.isqrt(value.numerator), math.isqrt(value.denominator)
    require(n * n == value.numerator and d * d == value.denominator,
            "The diagnostic expected a rational square")
    return F(n, d)


def density_inverse() -> dict:
    d, anchor, normalizer = F(3, 2), F(2, 5), F(7)
    points = [F(-1, 3), F(-1, 5), F(0), F(2, 7), F(1, 3)]

    def action(u: F) -> F:
        return u * u / 3 + u**3 / 17 + u**4 / 41

    def amplitude(u: F) -> F:
        return 2 + u / 5 + u * u / 11

    def density(u: F, v: F) -> F:
        return amplitude(u) * amplitude(v) * (d-action(u)-action(v)) / normalizer

    def ratio(u: F, v: F) -> F:
        return density(u, v)*density(F(0), F(0))/(density(u, F(0))*density(F(0), v))

    q = rational_sqrt(1-ratio(anchor, anchor))
    require(q > 0, "Anchor must be nondegenerate")
    for u in points:
        for v in points:
            require(1-ratio(u, v) == action(u)*action(v)/((d-action(u))*(d-action(v))),
                    "Four-density cancellation failed")
        T = (1-ratio(u, anchor))/q
        require(d*T/(1+T) == action(u), "Signed action inverse failed")
        recovered_B = density(u, F(0))/density(F(0), F(0))*(1+T)
        require(recovered_B == amplitude(u)/amplitude(F(0)), "Amplitude inverse failed")
    require(action(F(-1, 3)) != action(F(1, 3)), "Example must be asymmetric")
    return {"status": "PASS", "ratio_pairs": len(points)**2,
            "signed_reconstructions": len(points), "arithmetic": "exact rational",
            "note": "The arbitrary common normalizer cancels; no global normalization is asserted."}


T = F(1, 5)  # exp(-gamma)
R = F(3, 2)  # sqrt(c0/c1)
GAP = F(7, 5)
C = (T + 1/T)/2
SINH = (1/T-T)/2
CS = [C*R, C/R]


def hyperbolic(n: int) -> tuple[F, F]:
    return (1+T**(2*n))/(1-T**(2*n)), 2*T**n/(1-T**(2*n))


def endpoint_schur(j: int, start: int) -> list[list[F]]:
    h = [[F(0) for _ in range(j+1)] for _ in range(j+1)]
    for i in range(j+1):
        h[i][i] = (1 if i in (0, j) else 2)*CS[(start+i) % 2]/GAP
        if i < j:
            h[i][i+1] = h[i+1][i] = -1/GAP
    while len(h) > 2:
        keep = [i for i in range(len(h)) if i != 1]
        pivot = h[1][1]
        require(pivot > 0, "Nonpositive Schur pivot")
        h = [[h[i][k]-h[i][1]*h[1][k]/pivot for k in keep] for i in keep]
    return h


def jacobi_and_green() -> dict:
    cases = 0
    for start in (0, 1):
        a_start = (R if start == 0 else 1/R)*SINH/GAP
        for j in (1, 2, 3, 4, 7, 10):
            end = (start+j) % 2
            a_end = (R if end == 0 else 1/R)*SINH/GAP
            ch, sh = hyperbolic(j)
            mixed = -(a_start if start == end else SINH/GAP)*sh
            expected = [[a_start*ch, mixed], [mixed, a_end*ch]]
            require(endpoint_schur(j, start) == expected, "Endpoint Hessian mismatch")
            cases += 1

    def green(i: int, k: int, start: int) -> F:
        if i == 0:
            return F(0)
        ti, tk = (start+i) % 2, (start+k) % 2
        factor = F(1) if ti != tk else (R if ti == 1 else 1/R)
        return GAP*factor/(2*SINH)*(T**abs(i-k)-T**(i+k))

    entries = 0
    for start in (0, 1):
        for i in range(1, 10):
            for k in range(1, 10):
                value = (2*CS[(start+i) % 2]*green(i, k, start)
                         -green(i-1, k, start)-green(i+1, k, start))/GAP
                require(value == int(i == k), "Half-line Green recurrence mismatch")
                entries += 1
    return {"status": "PASS", "finite_schur_cases": cases,
            "half_line_recurrence_entries": entries, "arithmetic": "exact rational",
            "note": "Recurrence uses the explicit infinite-kernel formula, not a truncated inverse."}


def last_jet_blocks() -> dict:
    for n in range(3, 17):
        ch, sh = hyperbolic(n)
        b, c = R**n*sh, R**(-n)*sh
        require(ch*ch-b*c == 1, "Last-jet determinant is not one")
        matrix, inverse = [[ch, b], [c, ch]], [[ch, -b], [-c, ch]]
        product = [[sum(matrix[i][k]*inverse[k][j] for k in range(2))
                    for j in range(2)] for i in range(2)]
        require(product == [[1, 0], [0, 1]], "Last-jet inverse mismatch")
        require(1+2*T**(2*n)/(1-T**(2*n)) == ch, "Own-site multiplicity mismatch")
        require(2*R**n*T**n/(1-T**(2*n)) == b, "Opposite-site multiplicity mismatch")
    return {"status": "PASS", "orders": [3, 16], "arithmetic": "exact rational",
            "note": "Finite orders only; not an infinite-order conditioning certificate."}


def moving_disk_moments() -> dict:
    # f_theta(x) = (2/pi)*(1+theta-|x|^2)_+/(1+theta)^2 on |x|<2.
    # Under theta=0, s=1-|x|^2 has density 2s on (0,1), score 1/s-2, J=2.
    # The mean integral below is exact. Floors/ceilings make n an integer;
    # all examples use p_n=1. No physical-billiard realization is asserted.
    records = []
    for ell in (8, 16, 32, 64, 128):
        delta = math.exp(-ell)
        q = delta*ell**0.25
        n = math.ceil(1/(delta*delta*ell))
        B = n*delta*delta*ell
        logq = math.log(1/q)
        m2 = 2*logq-4+8*q-4*q*q
        m4 = q**(-2)-16/q+48*logq+64*q-16*q*q-33
        require(m2 > 0 and m4 > 0, "Invalid truncated reference moment")
        mean_values = []
        for h in (-1.0, 0.0, 1.5):
            theta = delta*h
            require(1+theta > 0 and q > abs(theta), "Not on common support")
            mean = 2*B/ell*((q*q-q)/delta+h*(logq-2+2*q))/(1+theta)**2
            mean_values.append({"h": h, "mean_delta": round(mean, 12),
                                "limiting_mean": 2*h})
            require(math.isfinite(mean) and abs(mean) < 6, "Unbounded finite-model mean")
        variance_budget = n*delta**2*m2
        fourth_summand_budget = n*delta**4*m4
        expected_fourth_rate = B*ell**(-1.5)
        require(0 < fourth_summand_budget <= expected_fourth_rate*1.001,
                "Fourth-summand rate check failed")
        require(math.isclose(n*delta*q, B*ell**(-0.75), rel_tol=1e-12),
                "Truncated-centering scale mismatch")
        require(math.isclose(n*delta**2*logq,
                            B*(1-math.log(ell)/(4*ell)), rel_tol=1e-12),
                "Logarithmic information scale mismatch")
        records.append({"ell": ell, "means": mean_values,
                        "second_moment_sum": round(variance_budget, 12),
                        "fourth_moment_sum": round(fourth_summand_budget, 12)})
    return {"status": "PASS", "information": 2, "records": records,
            "note": "Explicit smooth moving-support model; finite diagnostic, not an asymptotic proof."}


def waiting_affinity() -> dict:
    p, q, largest_error = 0.2, 0.3, 0.0
    affinity = math.sqrt(p*q)/(1-math.sqrt((1-p)*(1-q)))
    for k in (1, 3, 5):
        numerical = sum(math.comb(t-1, k-1)*(p*q)**(k/2)
                        *((1-p)*(1-q))**((t-k)/2) for t in range(k, 1000))
        error = abs(numerical-affinity**k)
        largest_error = max(largest_error, error)
        require(error < 1e-12, "Negative-binomial affinity mismatch")
    return {"status": "PASS", "success_counts": [1, 3, 5],
            "max_absolute_error": format(largest_error, ".3g"),
            "note": "Finite sum versus closed generating-function formula; not a Poisson approximation."}


def main() -> None:
    results = {"source_commit": SOURCE_COMMIT,
               "scope": "Independent finite mathematical diagnostics; not complete-manuscript validation.",
               "density_inverse": density_inverse(),
               "jacobi_green": jacobi_and_green(),
               "last_jet_blocks": last_jet_blocks(),
               "moving_disk_moments": moving_disk_moments(),
               "waiting_affinity": waiting_affinity()}
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
