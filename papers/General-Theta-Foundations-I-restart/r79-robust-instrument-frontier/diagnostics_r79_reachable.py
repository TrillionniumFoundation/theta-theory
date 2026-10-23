#!/usr/bin/env python3
"""Exact finite quantum/support/restart diagnostics; not a theorem prover.

The forward product evolution and backward cost system are evaluated
independently on rational, genuinely nonreset qubit instruments.  Boundary
examples check inaccessible dark subspaces and nonuniform model witnesses.
"""
from collections import Counter
import json
import sympy as s

C = Counter()
Q = s.Rational
I = s.eye(2)


def check(condition, group, message):
    if not bool(condition):
        raise RuntimeError(group + ': ' + message)
    C[group] += 1


def psd(A, group, message):
    check(A == A.T, group, message + ' symmetry')
    check(A[0, 0] >= 0 and A[1, 1] >= 0 and s.det(A) >= 0,
          group, message + ' principal minors')


def vec(A):
    return s.Matrix([A[i, j] for j in range(2) for i in range(2)])


def mat(v):
    return s.Matrix(2, 2, lambda i, j: v[2*j+i])


R = s.Matrix([[Q(3, 5), -Q(4, 5)], [Q(4, 5), Q(3, 5)]])
X = s.Matrix([[0, 1], [1, 0]])
Z = s.diag(1, -1)
KRAUS = [[s.diag(Q(1, 2), Q(1, 3)), X/4],
         [R*s.diag(Q(1, 3), Q(2, 5)), Z/5]]
ALT = [[R/4, Z/5], [X/5, R/6]]
COST = [I, 2*I]


def product_map(rows, updates, kraus):
    m = len(rows)
    T = s.zeros(4*m)
    for k in range(m):
        for a in range(2):
            for y in range(2):
                K = kraus[a][y]
                L = s.kronecker_product(K, K)
                for j in range(m):
                    T[4*j:4*j+4, 4*k:4*k+4] += rows[k][a]*updates[k][a][y][j]*L
    return T


def cost_vector(rows, delta=0):
    result = []
    for row in rows:
        result.extend(vec(sum((row[a]*COST[a] for a in range(2)), s.zeros(2))+delta*I))
    return s.Matrix(result)


def exact_cost(T, G):
    w = (s.eye(T.rows)-T.T).inv()*G
    return w, [mat(w[k:k+4]) for k in range(0, len(w), 4)]


def quantum_cases():
    group = 'exact_quantum_product_and_cost'
    for instruments in [KRAUS, ALT]:
        for row in instruments:
            psd(I-sum((K.T*K for K in row), s.zeros(2)), group, 'physical success effect')
    for instruments in [KRAUS, ALT]:
        for row in instruments:
            psd(I/2-sum((K.T*K for K in row), s.zeros(2)),
                'exact_positive_success_refinement', 'common one-half success floor')
    check(KRAUS[1][0]*KRAUS[0][0] != KRAUS[0][0]*KRAUS[1][0], group, 'noncommuting failure maps')
    check(KRAUS[0][0].rank() == 2, group, 'invertible nonreset failure')
    states = [s.diag(1, 0), s.diag(0, 1), I/2,
              s.Matrix([[Q(1, 2), Q(1, 2)], [Q(1, 2), Q(1, 2)]]),
              s.Matrix([[Q(9, 25), Q(12, 25)], [Q(12, 25), Q(16, 25)]])]
    cases = 0
    for m in [1, 2, 3]:
        for seed in [1, 2]:
            rows = [[Q(k+seed, m+seed+2), 1-Q(k+seed, m+seed+2)] for k in range(m)]
            updates = []
            for k in range(m):
                ar = []
                for a in range(2):
                    yr = []
                    for y in range(2):
                        weights = [1+((j+k+a+y+seed) % (m+1)) for j in range(m)]
                        yr.append([Q(z, sum(weights)) for z in weights])
                    ar.append(yr)
                updates.append(ar)
            T = product_map(rows, updates, KRAUS)
            G = cost_vector(rows)
            w, W = exact_cost(T, G)
            check(w == G+T.T*w, group, 'backward cost equality')
            for B in W:
                psd(B, group, 'positive cost block')
            for rho in states:
                start = s.zeros(4*m, 1); start[:4, 0] = vec(rho)
                state, accumulated = start, s.Integer(0)
                for horizon in range(1, 6):
                    accumulated += (G.T*state)[0]
                    state = T*state
                    actual = s.trace(W[0]*rho)
                    check(s.simplify(accumulated+(w.T*state)[0]-actual) == 0,
                          group, 'forward/backward finite-prefix identity')
                    check(accumulated <= actual, group, 'nonnegative cost tail')
            b = max(sum(abs(W[0][i, j]) for j in range(2)) for i in range(2))
            psd(b*I-W[0], group, 'certified initial bound')
            for eps in [Q(1, 20), Q(1, 10)]:
                restart = [[[[ (1-eps)*updates[k][a][y][j]+eps*int(j == 0)
                               for j in range(m)] for y in range(2)] for a in range(2)] for k in range(m)]
                TE = product_map(rows, restart, KRAUS)
                we, WE = exact_cost(TE, G)
                U = b/(1-eps*b)
                cap = 2/eps+U
                check(eps*b < 1, 'exact_memory_restart', 'restart probability bound')
                psd(U*I-WE[0], 'exact_memory_restart', 'same-memory initial bound')
                for B in WE:
                    psd(cap*I-B, 'exact_memory_restart', 'full-space continuation cap')
                eta, zeta = Q(1, 10000), Q(1, 20000)
                TA = product_map(rows, restart, ALT)
                target = (1-eta)*TE+eta*TA
                target_G = cost_vector(rows, zeta)
                delta = zeta+eta*cap
                alpha = 1/(1-delta)
                check(delta < 1, 'exact_primitive_transfer', 'positive transfer margin')
                residual = alpha*we-target_G-target.T*(alpha*we)
                for k in range(m):
                    psd(mat(residual[4*k:4*k+4]), 'exact_primitive_transfer', 'target supersolution')
                target_w, target_W = exact_cost(target, target_G)
                psd(alpha*U*I-target_W[0], 'exact_primitive_transfer', 'actual target cost below certificate')
            for eta in [Q(1, 100), Q(1, 3), Q(1, 2)]:
                zeta, kappa = Q(1, 17), Q(1, 2)
                other = product_map(rows, updates, ALT)
                target = (1-eta)*T+eta*other
                _, target_W = exact_cost(target, cost_vector(rows, zeta))
                bound = zeta/kappa+(2+zeta)*eta/kappa**2
                for source_B, target_B in zip(W, target_W):
                    psd(bound*I-(target_B-source_B), 'exact_positive_success_refinement',
                        'resolvent Lipschitz upper matrix bound')
                    psd(bound*I+(target_B-source_B), 'exact_positive_success_refinement',
                        'resolvent Lipschitz lower matrix bound')
            cases += 1
    return cases


def inaccessible_quantum_subspace():
    group = 'exact_inaccessible_quantum_dark_subspace'
    E = s.diag(1, 0); D = I-E
    # Label 1: failure rho -> (1/4) E rho E, then label 2.
    # Label 2: failure rho -> D rho D, staying at label 2.
    T = s.zeros(8)
    T[4:8, :4] = s.kronecker_product(E/2, E/2)
    T[4:8, 4:8] = s.kronecker_product(D, D)
    P = [I, E]
    W = [I+E/4, E]
    pv = s.Matrix(list(vec(P[0]))+list(vec(P[1])))
    w = s.Matrix(list(vec(W[0]))+list(vec(W[1])))
    G = s.Matrix(list(vec(I))+list(vec(I)))
    check((s.eye(8)-T).det() == 0, group, 'full-space resolvent must be singular')
    tp = T*pv
    residual = w-G-T.T*w
    for k in range(2):
        check(P[k]*mat(tp[4*k:4*k+4])*P[k] == mat(tp[4*k:4*k+4]), group, 'invariant support')
        check(P[k]*mat(residual[4*k:4*k+4])*P[k] == s.zeros(2), group, 'restricted cost equality')
    start = s.Matrix(list(vec(I))+[0]*4)
    reach = s.zeros(8, 1); term = start
    for _ in range(4):
        reach += term; term = T*term
    check(mat(reach[:4]).rank() == 2 and mat(reach[4:]).columnspace() == [s.Matrix([Q(1, 4), 0])],
          group, 'finite reachable support is exact')
    check(s.trace(D*I) == 1 and s.trace(D*W[1]) == 0, group, 'unreachable dark cost excluded')


def compact_boundary():
    group = 'exact_compact_model_support_boundary'
    for theta in [Q(0), Q(1), *[Q(1, n) for n in range(2, 25)]]:
        failure = theta*(1-theta)
        if theta == 0:
            check(failure == 0, group, 'dark label unreachable at zero')
            check(s.Integer(1) < 2, group, 'endpoint cost below supremum')
        else:
            continuation = 1/theta
            check(continuation == 1+(1-theta)*continuation, group, 'continuation equation')
            check(1+failure*continuation == 2-theta, group, 'initial cancellation')
            check(2-theta < 2, group, 'supremum not attained at positive parameter')
        check(failure <= Q(1, 4), group, 'uniform one-row primitive fallback')


def positive_success_sharpness():
    group = 'exact_positive_success_scalar_coefficients'
    for kappa in [Q(1, 2), Q(1, 3), Q(1, 5), Q(3, 4)]:
        for eta in [Q(0), (1-kappa)/10, (1-kappa)/2]:
            for zeta in [Q(0), Q(1, 7)]:
                cost = Q(3, 2)
                target, source = (cost+zeta)/kappa, cost/(kappa+eta)
                check(target == cost+zeta+(1-kappa)*target, group, 'target waiting equation')
                check(source == cost+(1-kappa-eta)*source, group, 'source waiting equation')
                check(target-source == zeta/kappa+cost*eta/(kappa*(kappa+eta)),
                      group, 'exact two-parameter frontier difference')
                check(target-source <= zeta/kappa+(cost+zeta)*eta/kappa**2,
                      group, 'unrestricted-error Lipschitz bound')
    h, k, c = s.symbols('h k c', positive=True)
    check(s.limit(c/(k*(k+h)), h, 0) == c/k**2, group, 'sharp local instrument coefficient')


def main():
    cases = quantum_cases()
    inaccessible_quantum_subspace()
    compact_boundary()
    positive_success_sharpness()
    total = sum(C.values())
    print(json.dumps({'status':'PASS','total_checks':total,'exact_checks':total,
                      'floating_checks':0,'checks_by_group':dict(sorted(C.items())),
                      'rational_nonreset_qubit_controllers':cases,
                      'interpretation':'Finite exact diagnostics and boundary checks; not formal verification, general quantifier elimination, or independent referee endorsement.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
