#!/usr/bin/env python3
"""Exact v80 confidence/readout kernels and one uniform scalar certificate.

No general quantifier elimination, theorem-scale synthesis, physical learner,
or minimax certification is executed. Checks survive python -O unchanged.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb, factorial
import json

import sympy as sp

CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def binomial_tail(n, p):
    return sum((F(comb(n, j))*p**j*(1-p)**(n-j)
                for j in range(n//2+1, n+1)), F(0))


def confidence_checks():
    # Positive Taylor remainder gives exp(3/4)>269/128>2. The displayed
    # polynomial identity then certifies q_d>4 exp(-4d^2) for EVERY d>=1.
    taylor = sum((F(3, 4)**j/factorial(j) for j in range(4)), F(0))
    check(taylor == F(269, 128) and taylor > 2, "log-two certificate")
    d = sp.symbols("d", integer=True, positive=True)
    check(sp.expand(16*d*d-9*d-6-(d-1)*(16*d+7)-1) == 0,
          "uniform positive threshold polynomial")
    cases = tails = 0
    etas = (F(1, 8), F(1, 13), F(3, 256), F(1, 1024),
            F(5, 65536), F(1, 2**63+1))
    for dimension in range(1, 65):
        q = F(1, 2**(3*dimension))
        check(F(3*(3*dimension+2), 4) < 4*dimension**2,
              "seed threshold rational inequality")
        for eta in etas:
            h = 0
            while eta*2**h < 1:
                h += 1
            check(eta*2**h >= 1 > eta*2**(h-1), "exact ceiling log")
            k = (2*h+dimension-1)//dimension
            k += 1-k % 2  # Least positive odd k with d*k >= 2*h.
            check(k > 0 and k % 2 == 1 and dimension*k >= 2*h
                  and (k == 1 or dimension*(k-2) < 2*h), "safe odd length")
            squared_union = 2**(2*k)*q**k
            check(squared_union <= F(1, 2**(dimension*k)) <= eta**2,
                  "squared amplification bound without square roots")
            if dimension in (1, 2, 7) and eta in etas[:4]:
                tail = binomial_tail(k, q)
                check(tail <= eta and tail**2 <= squared_union,
                      "exact independent-seed majority tail")
                tails += 1
            cases += 1
    return {"safe_amplification_lengths": cases, "exact_binomial_tails": tails,
            "taylor_lower_bound": str(taylor), "uniform_seed_certificate": True}


def clean(matrix):
    return matrix.applyfunc(sp.expand)


def tensor(matrices):
    out = sp.ones(1)
    for matrix in matrices:
        out = sp.kronecker_product(out, matrix)
    return clean(out)


def maxent_branch(effect):
    """Partial trace of (effect tensor I)|Phi><Phi|, without sqrt(d)."""
    d = effect.rows
    vector = sp.Matrix([int(i == j) for i in range(d) for j in range(d)])
    joint = sp.kronecker_product(effect, sp.eye(d))*(vector*vector.T/d)
    return clean(sp.Matrix(d, d, lambda u, v:
                           sum(joint[a*d+u, a*d+v] for a in range(d))))


def choi_checks():
    cases = records = transpose_controls = normalization_controls = 0
    for d, seed in product(range(1, 5), (1, 2)):
        v = sp.Matrix([j+1+sp.I*(j*j+2*j+seed) for j in range(d)])
        projector = clean(v*v.adjoint()/(v.adjoint()*v)[0])
        check(clean(projector*projector) == projector
              and projector.adjoint() == projector, "legal rank-one effect")
        E = sp.eye(d)/2+projector/8  # Spectrum contained in {1/2,5/8}.
        effects = (sp.eye(d)-E, E)
        actual = [maxent_branch(A) for A in effects]
        for y in (0, 1):
            check(actual[y] == clean(effects[y].T/d), "Choi transpose identity")
        for m in (1, 2):
            predicted, contracted, readouts, wrong = [], [], [], []
            for y in product((0, 1), repeat=m):
                R = tensor([effects[t].T/d for t in y])
                S = tensor([actual[t] for t in y])
                local = []
                for t in y:
                    w = sp.zeros(d, 1)
                    w[0] = 1
                    if d > 1:
                        w[1] = sp.I*(-1 if t else 1)
                    local.append(clean(w*w.adjoint()/(w.adjoint()*w)[0]))
                A = tensor(local)
                check(R == S, "tensor subnormalized record")
                check(clean(A*A) == A and A.adjoint() == A,
                      "conditional POVM is a projection and its complement")
                predicted.append(R)
                contracted.append(S)
                readouts.append(A)
                wrong.append(tensor([effects[t]/d for t in y]))
                records += 1
            gamma, measurement = sp.diag(*contracted), sp.diag(*readouts)
            polynomial = sp.expand(sum(sp.trace(A*R)
                                       for A, R in zip(readouts, predicted)))
            direct = sp.expand(sp.trace(measurement*gamma))
            check(direct == polynomial and 0 <= direct <= 1, "direct cq Born law")
            check(sp.trace(gamma) == 1 and sp.expand(sp.trace(
                (sp.eye(gamma.rows)-measurement)*gamma)+direct) == 1,
                  "complete two-outcome normalization")
            renormalized_trace = sum(sp.trace(R/sp.trace(R)) for R in predicted)
            check(renormalized_trace == 2**m and renormalized_trace != 1,
                  "negative control: conditional normalization loses weights")
            normalization_controls += 1
            if d > 1:
                bad = sp.expand(sum(sp.trace(A*R) for A, R in zip(readouts, wrong)))
                check(bad != direct, "negative control: omitted transpose")
                transpose_controls += 1
            cases += 1
    P = sp.Matrix([[1, -sp.I], [sp.I, 1]])/2
    E = sp.eye(2)/2+P/8
    R0, R1 = maxent_branch(sp.eye(2)-E), maxent_branch(E)
    correct = sp.trace(R0)+sp.trace(P*R1)
    missing_transpose = sp.trace((sp.eye(2)-E)/2)+sp.trace(P*E/2)
    uniform_reweighting = (1+sp.trace(P*R1)/sp.trace(R1))/2
    check((correct, missing_transpose, uniform_reweighting)
          == (sp.Rational(11, 16), sp.Rational(3, 4), sp.Rational(13, 18)),
          "sentinel: both transpose and uniform reweighting change the Born law")
    return {"matrix_cases": cases, "classical_records": records,
            "omitted_transpose_rejections": transpose_controls,
            "renormalized_record_rejections": normalization_controls,
            "uniform_reweighting_rejections": 1}


@lru_cache(None)
def log_factors(value):
    q = sp.Rational(value)
    out = dict(sp.factorint(q.p))
    for prime, exponent in sp.factorint(q.q).items():
        out[prime] = out.get(prime, 0)-exponent
    return tuple(sorted((int(p), e) for p, e in out.items() if e))


def log_sum(terms):
    # Rational coefficients of log(prime) compare exactly by unique factorization.
    out = {}
    for coefficient, argument in terms:
        for prime, exponent in log_factors(argument):
            out[prime] = out.get(prime, 0)+coefficient*exponent
    return {p: c for p, c in out.items() if c}


def relative_entropy(spectrum0, basis0, spectrum1, basis1):
    """Exact prime-log coefficients, including noncommuting spectral overlap."""
    size = len(spectrum0)
    check(sum(spectrum0) == sum(spectrum1) == 1
          and all(x > 0 for x in spectrum0+spectrum1), "positive normalized spectra")
    check(basis0.T*basis0 == basis1.T*basis1 == sp.eye(size), "orthogonal eigenbases")
    overlap = basis0.T*basis1
    terms = [(x, x) for x in spectrum0]
    terms += [(-x*overlap[a, b]**2, z)
              for a, x in enumerate(spectrum0) for b, z in enumerate(spectrum1)]
    return log_sum(terms)


def cq_entropy_checks():
    R = sp.Rational
    rotation = lambda a, b: sp.Matrix([[a, -b], [b, a]])
    bases0 = (sp.eye(2), rotation(R(5, 13), R(12, 13)))
    bases1 = (rotation(R(3, 5), R(4, 5)), rotation(R(8, 17), R(15, 17)))
    eig0, eig1 = ((R(1, 3), R(2, 3)), (R(2, 5), R(3, 5))), \
                 ((R(3, 7), R(4, 7)), (R(4, 9), R(5, 9)))
    w0, w1 = (R(1, 3), R(2, 3)), (R(3, 5), R(2, 5))
    for j in (0, 1):
        rho = bases0[j]*sp.diag(*eig0[j])*bases0[j].T
        sigma = bases1[j]*sp.diag(*eig1[j])*bases1[j].T
        check(rho*sigma != sigma*rho, "noncommuting conditional quantum states")
    before = relative_entropy([w0[j]*x for j in (0, 1) for x in eig0[j]],
                              sp.diag(*bases0),
                              [w1[j]*x for j in (0, 1) for x in eig1[j]],
                              sp.diag(*bases1))
    proxy = relative_entropy([w0[j]*x for j in (0, 1) for x in eig0[j]], sp.eye(4),
                             [w1[j]*x for j in (0, 1) for x in eig1[j]], sp.eye(4))
    check(before != proxy, "negative control: omitting noncommuting spectral overlaps")
    cases = 0
    for i, delta in product((0, 1), (R(1, 16), R(1, 32))):
        s0, s1, u0, u1 = [], [], [], []
        for j, y in product((0, 1), repeat=2):
            p1 = R(1, 2)+(delta if j == i else 0)
            s0.extend(w0[j]*R(1, 2)*x for x in eig0[j])
            s1.extend(w1[j]*(p1 if y else 1-p1)*x for x in eig1[j])
            u0.append(bases0[j])
            u1.append(bases1[j])
        after = relative_entropy(s0, sp.diag(*u0), s1, sp.diag(*u1))
        difference = {p: after.get(p, 0)-before.get(p, 0) for p in after.keys() | before.keys()}
        difference = {p: c for p, c in difference.items() if c}
        correct = log_sum([(w0[i]/2, 1/(1-4*delta**2))])
        incorrect = log_sum([(w1[i]/2, 1/(1-4*delta**2))])
        check(difference == correct, "cq entropy increment uses null branch weight")
        check(difference != incorrect, "negative control: alternative branch weight")
        cases += 1
    return {"noncommuting_conditional_pairs": 2, "exact_entropy_identities": cases,
            "wrong_weight_rejections": cases, "commuting_proxy_rejections": 1,
            "logarithms": "rational prime-log coefficients"}


def scalar_certificate():
    n, p = 49, sp.symbols("p")
    tail = sp.Poly(sum(comb(n, j)*p**j*(1-p)**(n-j)
                       for j in range(25, 50)), p)
    derivative = sp.Poly(n*comb(48, 24)*p**24*(1-p)**24, p)
    check(tail.diff() == derivative, "nonnegative factored derivative on [0,1]")
    check(tail+sp.Poly(tail.as_expr().subs(p, 1-p), p) == sp.Poly(1, p),
          "odd-majority reflection identity")
    lo, hi, c0, c1, a = F(1, 4), F(3, 4), F(3, 8), F(5, 8), F(1, 4)
    check(c0-a <= lo < c1-a < c0+a < hi <= c1+a,
          "exact exhaustive good-output interval partition")
    # On [lo,3/8) only C0 is good, on [3/8,5/8] both are good,
    # and on (5/8,hi] only C1 is good. The derivative and reflection
    # identities certify the tail bound over the WHOLE scalar interval.
    bound = binomial_tail(n, c1-a)
    check(tail.eval(sp.Rational(c1-a)) == bound and 0 < bound < F(1, 16),
          "uniform scalar ideal-risk bound")
    for boundary in (c1-a, c0+a):
        probabilities = (1-binomial_tail(n, boundary), binomial_tail(n, boundary))
        risk = sum(prob for c, prob in zip((c0, c1), probabilities) if abs(c-boundary) > a)
        check(risk == 0, "equality boundary counts both centers as good")
    eta, event = F(1, 8), F(1, 8*(n+1))
    check((n+1)*event == eta and event/2+event/2 == event,
          "preparation plus readout pathwise budget")
    check(bound+eta/2 < eta, "actual risk after unhalved-error coupling")
    return {"copies": n, "centers": [str(c0), str(c1)], "operator_radius": str(a),
            "ideal_risk_upper_bound": str(bound), "complete_event_budget": str(event),
            "actual_risk_upper_bound": str(bound+eta/2),
            "small_delta_main_theorem_fixture": False, "uniform_interval_certificate": True}


def main():
    report = {"schema": "gtf80.confidence-readout-regression/1",
              "confidence": confidence_checks(), "choi_readout": choi_checks(),
              "cq_relative_entropy": cq_entropy_checks(), "scalar_readout": scalar_certificate(),
              "status": "success", "floating_point_decisions": False,
              "general_quantifier_elimination_executed": False,
              "theorem_scale_synthesis_executed": False, "physical_learner_executed": False,
              "scope": "Exact finite kernels and one scalar interval certificate; "
                       "no general learning, minimax, physical-control, or priority certification."}
    report["exact_assertions"] = CHECKS
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
