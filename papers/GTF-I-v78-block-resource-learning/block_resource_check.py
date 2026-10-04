#!/usr/bin/env python3
"""Finite exact checks for the v78 resource and information identities.

This checks declared call arithmetic, explicit GHZ outcome laws, small
classical--quantum branch potentials, and the support-inverse collision
identity. It is not a statistical simulation or a continuum proof.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json

import sympy as sp

from matrix_metric import is_positive_semidefinite


CHECKS = 0


def check(condition, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def multiply(z, w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def power(z, n):
    out = (F(1), F(0))
    for _ in range(n):
        out = multiply(out, z)
    return out


def horizon_checks():
    cases = 0
    for N in range(1, 97):
        for b in range(1, N+1):
            q = (N+b-1)//b
            check((q-1)*b < N <= q*b, "horizon ceiling")
            check(b*b*q*q <= 4*N*N, "block call upper factor")
            check(N*N >= b*N, "block lower is at least scalar order")
            cases += 1
    confidence = []
    for k in range(3, 33):
        eta = F(1, 2**k)
        check((1/(4*eta))**3 >= 1/eta,
              "confidence logarithm conversion")
        confidence.append(str(eta))
    check((1/(4*F(1, 4)))**3 < 1/F(1, 4),
          "negative control: confidence range must be retained")
    return {"horizon_block_pairs": cases,
            "confidence_cases": len(confidence)}


def ghz_checks():
    cases = outcomes = 0
    for N in range(1, 8):
        for denominator in (8*N, 16*N, 32*N):
            t = F(1, denominator)
            z = ((1-t*t)/(1+t*t), 2*t/(1+t*t))
            check(z[0]**2+z[1]**2 == 1, "exact rational circle")
            zn = power(z, N)
            check(zn[0] > 0, "tested angle lies in the local half circle")
            sums = [F(0), F(0)]
            distance = F(0)
            for word in product((0, 1), repeat=N):
                sign = -1 if sum(word) % 2 else 1
                probabilities = []
                for orientation in (-1, 1):
                    # The GHZ density has off-diagonal entries -i/2,i/2.
                    off = (F(1), F(0))
                    for outcome in word:
                        a = -1 if outcome else 1
                        off = multiply(off, (a*z[0]/2,
                                             -a*orientation*z[1]/2))
                    observed = F(1, 2**N)-off[1]
                    predicted = F(1, 2**N)*(1+sign*orientation*zn[1])
                    check(observed == predicted, "full GHZ outcome law")
                    check(observed >= 0, "legal GHZ outcome probability")
                    probabilities.append(observed)
                sums[0] += probabilities[0]
                sums[1] += probabilities[1]
                distance += abs(probabilities[1]-probabilities[0])
                outcomes += 1
            check(sums == [1, 1], "normalized complete GHZ laws")
            check(distance == 2*abs(zn[1]), "unhalved parity separation")
            check(distance != abs(zn[1]),
                  "negative control: halved normalization")
            cases += 1
    return {"complete_ghz_laws": cases, "outcome_pairs": outcomes}


def branch_potential_checks():
    # A classical random flag selects future lengths. Conditional on the
    # flag, two pure block outputs have overlap q**(t*t). Their direct-sum
    # root fidelity is the weighted sum below, entirely rational.
    q = F(3, 4)
    cases = leaves = 0
    for M in range(1, 13):
        for b in range(1, min(M, 5)+1):
            frontier = [(0, F(1), F(1), 0)]
            terminal = []
            for depth in range(M+1):
                next_frontier = []
                for used, weight, affinity, label in frontier:
                    if used == M or (label+depth) % 5 == 4:
                        terminal.append((used, weight, affinity))
                        continue
                    t = 1+(label+depth) % min(b, M-used)
                    factor = q**(t*t)
                    before = q**(b*(M-used))*affinity
                    after = q**(b*(M-used-t))*affinity*factor
                    check(after >= before, "weighted cq block potential")
                    for outcome, probability in ((0, F(1, 3)),
                                                 (1, F(2, 3))):
                        next_frontier.append((used+t, weight*probability,
                                              affinity*factor,
                                              2*label+outcome+1))
                frontier = next_frontier
                if not frontier:
                    break
            check(not frontier, "every adaptive record terminates")
            check(sum(w for _, w, _ in terminal) == 1,
                  "complete stopping history law")
            final = sum(w*f for _, w, f in terminal)
            check(final >= q**(b*M), "variable-length fidelity budget")
            check(all(used <= M for used, _, _ in terminal),
                  "every-record call budget")
            leaves += len(terminal)
            cases += 1
    # A coherent block of length M cannot be charged as M independent
    # one-call blocks: the proposed stronger affinity lower bound fails.
    check(q**16 < q**4, "negative control: unrestricted coherent memory")
    return {"adaptive_flagged_trees": cases, "terminal_records": leaves}


def collision_checks():
    cases = noncommuting = singular = 0
    for dimension in range(1, 5):
        for rank in range(1, dimension+1):
            for seed in (1, 2):
                T = sp.zeros(dimension, rank)
                for i in range(dimension):
                    for j in range(rank):
                        T[i, j] = ((1 if i == j else 0)
                                   + sp.Rational((i+seed*j) % 3, 7)
                                   + sp.I*sp.Rational((2*i+j+seed) % 3, 11))
                gram = (T.adjoint()*T).applyfunc(sp.expand)
                check(gram.det() != 0, "full column rank preparation")
                Z = sp.trace(gram)
                rho = (T*T.adjoint()/Z).applyfunc(sp.expand)
                # Hermitian K with an exact entry-sum operator-norm bound.
                K0 = sp.zeros(rank)
                for i in range(rank):
                    K0[i, i] = sp.Rational((-1)**i, i+2)
                    for j in range(i+1, rank):
                        K0[i, j] = (sp.Rational(1, i+j+2)
                                    + sp.I*sp.Rational(seed, i+j+4))
                        K0[j, i] = sp.conjugate(K0[i, j])
                charge = 1+sum(abs(sp.re(x))+abs(sp.im(x)) for x in K0)
                r = sp.Rational(1, 4+4*seed)
                K = r*K0/charge
                Delta = (T*K*T.adjoint()/Z).applyfunc(sp.expand)
                left_inverse = (gram.inv()*T.adjoint()).applyfunc(sp.expand)
                support_inverse = (Z*left_inverse.adjoint()*left_inverse).applyfunc(sp.expand)
                plus, minus = rho/2+Delta, rho/2-Delta
                check(is_positive_semidefinite(r*rho-Delta)
                      and is_positive_semidefinite(r*rho+Delta),
                      "two relative Loewner bounds")
                check(is_positive_semidefinite(plus)
                      and is_positive_semidefinite(minus),
                      "both output blocks positive")
                collision = sp.expand(2*sp.trace(
                    (plus*plus+minus*minus)*support_inverse))
                deviation = sp.expand(sp.trace(Delta*Delta*support_inverse))
                congruence = sp.expand(sp.trace(gram*K*K)/Z)
                check(deviation == congruence,
                      "support-inverse congruence identity")
                check(collision == 1+4*deviation,
                      "binary collision factor four")
                check(collision <= 1+4*r*r,
                      "dimension-free collision upper bound")
                check(collision != 1+deviation,
                      "negative control: missing collision factor")
                if (rho*Delta-Delta*rho).applyfunc(sp.expand) != sp.zeros(dimension):
                    noncommuting += 1
                if rank < dimension:
                    singular += 1
                cases += 1
    check(noncommuting > 0 and singular > 0,
          "noncommuting and singular reference cases exercised")
    return {"exact_reference_cases": cases,
            "noncommuting_cases": noncommuting,
            "singular_cases": singular}


def main():
    report = {"schema": "gtf78.block-resource-regression/1",
              "horizon": horizon_checks(),
              "projective_witness": ghz_checks(),
              "cq_potential": branch_potential_checks(),
              "weak_measurement": collision_checks(),
              "status": "success", "floating_point_decisions": False,
              "scope": "Finite exact arithmetic, explicit outcome laws, "
                       "flagged branch budgets and support-inverse identities. "
                       "Not a continuum proof, physical learner execution, "
                       "adaptive supremum, minimax certification or priority."}
    report["exact_assertions"] = CHECKS
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
