#!/usr/bin/env python3
"""Independent finite diagnostics accompanying the A2 v32 referee report.

These checks do not prove the manuscript's asymptotic theorems, realize a
billiard family, or build its native TeX sources. No third-party packages.
"""
from __future__ import annotations
from decimal import Decimal, localcontext
from fractions import Fraction as F
import json
import math


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def triangular_affinity(a: Decimal, b: Decimal) -> Decimal:
    """Integral of sqrt(f_a f_b), f_L(x)=2(L-x)_+/L^2 on [0,2]."""
    a, b = sorted((a, b))
    require(0 < a <= b < 2, "invalid triangular parameters")
    d = b - a
    if not d:
        return Decimal(1)
    root = (a * b).sqrt()
    integral = (a + d / 2) * root / 2
    integral -= d * d / 8 * ((a + d / 2 + root) / (d / 2)).ln()
    return 2 * integral / (a * b)


def run_checks() -> dict:
    # Finite restrictions converge, but the compact experiment need not.
    # K={0} U {1/m}; P_{n,1/n}=delta_1, and all other P_{n,t}=delta_0.
    # A reverse kernel from a one-point experiment outputs Bernoulli(r).
    grid = [F(i, 100) for i in range(101)]
    best = min(max(r, 1-r) for r in grid)
    require(best == F(1, 2), "spike experiment minimax check")
    for r in grid:
        require(max(r, 1-r) >= F(1, 2), "reverse-kernel lower bound")

    # Exact geometric moments and information for phi=log p.
    score_checks = 0
    for p in (F(1, 2), F(1, 3), F(9, 25), F(16, 25)):
        mean_t, var_t = 1/p, (1-p)/(p*p)
        require((1-p*mean_t)/(1-p) == 0, "score centering")
        require(p*p*var_t/(1-p)**2 == 1/(1-p), "score information")
        score_checks += 2

    # p=9/25, q=16/25: both radicals are 12/25.
    affinity = F(12, 25)/(1-F(12, 25))
    require(affinity == F(12, 13), "geometric affinity")
    nb = []
    for k in (1, 2, 5, 17):
        h2 = 2 - 2*affinity**k
        require(0 <= h2 <= k*(2-2*affinity), "NB product Hellinger bound")
        nb.append({"successes": k, "affinity": str(affinity**k), "H2": str(h2)})

    log_bound_checks = 0
    with localcontext() as ctx:
        ctx.prec = 100
        probs = [Decimal(s) for s in ('.001', '.01', '.1', '.36', '.64', '.8')]
        for p in probs:
            for q in probs:
                if p == q:
                    continue
                a = (p*q).sqrt()/(1-((1-p)*(1-q)).sqrt())
                h2 = 2-2*a
                upper = (p.ln()-q.ln())**2/(4*(1-Decimal('.8')))
                require(0 < h2 <= upper, "log-probability Hellinger bound")
                log_bound_checks += 1

        moving = []
        target = 2*(1-(-Decimal(1)/4).exp())
        for exponent in (2, 4, 6, 8, 10, 12):
            delta = Decimal(10)**(-exponent)
            a = triangular_affinity(Decimal(1), 1+delta)
            scale = delta*delta*(1/delta).ln()
            h2 = 2-2*a
            ratio = h2/scale
            require(Decimal('.35') < ratio < Decimal('.65'), "triangular leading order")
            k = int(1/scale)
            product_h2 = 2*(1-(Decimal(k)*a.ln()).exp())
            moving.append({"delta": str(delta), "H2_over_delta2_log": format(ratio, '.12f'),
                           "successes": k, "product_H2": format(product_h2, '.12f')})
        require(abs(Decimal(moving[-1]['H2_over_delta2_log'])-Decimal('.5')) < Decimal('.02'),
                "triangular leading coefficient diagnostic")
        require(abs(Decimal(moving[-1]['product_H2'])-target) < Decimal('.02'),
                "triangular Gaussian affinity diagnostic")

    # A positive asymmetric geometry: exp(-gamma)=1/3, r0=5/4, r1=4/5.
    t, r0, r1 = F(1, 3), F(5, 4), F(4, 5)
    c = (t+1/t)/2
    require(c*r0 > 1 and c*r1 > 1, "positive curvature margin")
    for n in range(3, 21):
        diag = (1+t**(2*n))/(1-t**(2*n))
        off0 = 2*r0**n*t**n/(1-t**(2*n))
        off1 = 2*r1**n*t**n/(1-t**(2*n))
        require(diag*diag-off0*off1 == 1, "last-jet determinant")
        N = 7
        own_partial = 1+2*sum(t**(2*n*i) for i in range(1, N+1))
        own_tail = 2*t**(2*n*(N+1))/(1-t**(2*n))
        cross_partial = 2*r0**n*sum(t**(n*(2*i+1)) for i in range(N))
        cross_tail = 2*r0**n*t**(n*(2*N+1))/(1-t**(2*n))
        require(own_partial+own_tail == diag, "own-contact multiplicity")
        require(cross_partial+cross_tail == off0, "opposite-contact multiplicity")

    # Four-density identity with an asymmetric action and unknown amplitude.
    d, anchor = F(2), F(1, 5)
    def action(u: F) -> F:
        return u*u+u**3/10+u**4/20
    def amplitude(u: F) -> F:
        return 1+u/5+u*u/7
    def density(u: F, v: F) -> F:
        return amplitude(u)*amplitude(v)*(d-action(u)-action(v))/7
    def ratio(u: F, v: F) -> F:
        return density(u, v)*density(F(0), F(0))/(density(u, F(0))*density(F(0), v))
    points = [F(-1, 4), F(-1, 7), F(0), F(1, 9), F(1, 4)]
    ta = action(anchor)/(d-action(anchor))
    require(1-ratio(anchor, anchor) == ta*ta and ta > 0, "positive anchor")
    for u in points:
        recovered_t = (1-ratio(u, anchor))/ta
        require(d*recovered_t/(1+recovered_t) == action(u), "action recovery")
        recovered_b = density(u, F(0))/density(F(0), F(0))*(1+recovered_t)
        require(recovered_b == amplitude(u), "amplitude recovery")
        for v in points:
            require(1-ratio(u, v) == action(u)*action(v)/((d-action(u))*(d-action(v))),
                    "four-density cancellation")

    rates = []
    for k in (10**4, 10**8, 10**12, 10**16):
        delta = math.sqrt(2/(k*math.log(k)))
        j = 2*math.ceil(2*math.log(k))
        rates.append({"successes": k, "even_flights": j,
                      "critical_quantity": k*delta*delta*math.log(1/delta),
                      "j_delta": j*delta,
                      "fast_mark_bound": (1+math.log(j*math.sqrt(k)))/(j*j),
                      "finite_bridge_bound_tau_half": math.exp(math.log(k)+j*math.log(.5))})

    return {"status": "passed", "reviewed_source": "a4fe5c11f18070fc03d878ba683e014b48e921af",
            "scope": "Independent exact identities and finite numerical diagnostics; not a full theorem audit, a billiard realization, or a native TeX build.",
            "finite_restriction_counterexample": {"compact_distance": "1/2", "finite_restrictions": "eventually zero", "manuscript_counterexample": False},
            "exact_score_checks": score_checks, "exact_geometric_affinity": str(affinity),
            "negative_binomial_checks": nb, "geometric_log_bound_cases": log_bound_checks,
            "triangular_boundary_checks": moving, "gaussian_target_product_H2": format(target, '.12f'),
            "last_jet_orders_checked": list(range(3, 21)), "signed_density_points": len(points),
            "illustrative_compatible_rates": rates}


if __name__ == '__main__':
    print(json.dumps(run_checks(), indent=2, sort_keys=True))
