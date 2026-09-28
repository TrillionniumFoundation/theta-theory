#!/usr/bin/env python3
"""Independent finite diagnostics for the pinned A2 v15 review.
Not a theorem certificate, a global billiard simulation, or an interval proof.
Requires Python 3, NumPy and SciPy; no network or repository checkout needed.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import solve_banded

COUNTS: dict[str, int] = {}

def check(ok: bool, group: str, detail: str) -> None:
    if not ok:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] = COUNTS.get(group, 0) + 1

# Taylor jets in (lambda, a, u), total order <= 3; exact rational coefficients.
ORDER = 3
INDICES = tuple(t for t in itertools.product(range(ORDER + 1), repeat=3) if sum(t) <= ORDER)
ZERO = (0, 0, 0)

class Jet:
    def __init__(self, value=0, coefficients=None):
        self.c = {ZERO: F(value)} if coefficients is None else {i: F(v) for i, v in coefficients.items() if v}
    @staticmethod
    def cast(x):
        return x if isinstance(x, Jet) else Jet(x)
    @staticmethod
    def variable(value, axis):
        c = {ZERO: F(value)}
        i = tuple(int(j == axis) for j in range(3))
        c[i] = F(1)
        return Jet(coefficients=c)
    def __add__(self, other):
        b = Jet.cast(other)
        return Jet(coefficients={i: self.c.get(i, 0) + b.c.get(i, 0) for i in INDICES})
    __radd__ = __add__
    def __neg__(self):
        return Jet(coefficients={i: -v for i, v in self.c.items()})
    def __sub__(self, other):
        return self + (-Jet.cast(other))
    def __rsub__(self, other):
        return Jet.cast(other) - self
    def __mul__(self, other):
        b = Jet.cast(other)
        c = {}
        for i, x in self.c.items():
            for j, y in b.c.items():
                k = tuple(a + bb for a, bb in zip(i, j))
                if sum(k) <= ORDER:
                    c[k] = c.get(k, F(0)) + x * y
        return Jet(coefficients=c)
    __rmul__ = __mul__
    def inverse(self):
        c0 = self.c.get(ZERO, F(0))
        if not c0:
            raise ZeroDivisionError('jet has zero constant term')
        v = (self - c0) * (-1 / c0)
        ans, term = Jet(1), Jet(1)
        for _ in range(ORDER):
            term = term * v
            ans = ans + term
        return ans * (1 / c0)
    def __truediv__(self, other):
        return self * Jet.cast(other).inverse()
    def __rtruediv__(self, other):
        return Jet.cast(other) / self
    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        ans, base = Jet(1), self
        while n:
            if n & 1:
                ans = ans * base
            base = base * base
            n >>= 1
        return ans

def jet_equal(a: Jet, b: Jet, detail: str) -> None:
    for i in INDICES:
        check(a.c.get(i, 0) == b.c.get(i, 0), 'exact_mixed_jets', f'{detail}; multi-index={i}')

def scalar_checks():
    for l0, a0, u0 in itertools.product((F(1, 3), F(2, 3)), (F(-1, 2), F(2, 3)), (F(-1, 8), F(1, 8))):
        l, a, u = (Jet.variable(x, j) for j, x in enumerate((l0, a0, u0)))
        x, product = u, Jet(1)
        for n in range(1, 7):
            den = 1 + a * (1 - l) * x
            product = product / den ** 2  # R'(x)/lambda
            x = l * x / den
            closed = l ** n * u / (1 + a * (1 - l ** n) * u)
            jet_equal(x, closed, f'orbit n={n}')
            B0, Bn = (1 + a * u) ** (-2), (1 + a * x) ** (-2)
            jet_equal(product * Bn, B0, f'finite density remainder n={n}')
            z = u / (1 + a * u)
            jet_equal(x / (1 + a * x), l ** n * z, f'conjugacy n={n}')
        bad = product.c[ZERO] / l0 ** 6  # erroneously normalize by lambda^2 per return
        check(bad != product.c[ZERO], 'negative_controls', 'wrong return normalization must fail')
    for a0, a1, r0, r1, u in itertools.product((F(-1, 3), F(1, 2)), (F(1, 5),), (F(1, 3),), (F(1, 2),), (F(-1, 8), F(1, 8))):
        for ab, ao, rb in ((a0, a1, r0), (a1, a0, r1)):
            den = 1 + (ab - ao * rb) * u
            phi, derivative = rb * u / den, rb / den ** 2
            B = 1 / (1 + ab * u) ** 2
            Bo = 1 / (1 + ao * phi) ** 2
            check(Bo * derivative == rb * B, 'exact_first_flight', 'alternating cocycle')
            check(Bo * derivative != B / rb, 'negative_controls', 'reciprocal cocycle must fail')
    # An explicit family proves why the strict rate margin is needed.
    # d_a[lambda^-n R^n - z] at a=0 equals lambda^n*u^2;
    # differentiating in lambda produces n*lambda^(n-1)*u^2.
    l, u = F(1, 2), F(1, 4)
    normalized = [F(n) * l ** (n - 1) * u ** 2 / l ** n for n in (1, 4, 16, 64)]
    check(normalized == [F(n, 8) for n in (1, 4, 16, 64)], 'strict_margin', 'mixed rate polynomial')
    return {'mixed_total_order': ORDER, 'exact_orbit_depths': [1, 2, 3, 4, 5, 6],
            'strict_margin_normalized_values': [str(x) for x in normalized]}

# Physical local Euclidean flight action for facing graphs:
# ell_b(u,v) = sqrt((g+psi_b(u)+psi_o(v))^2+(u-v)^2).
def graph(x, p):
    k, c3, c4 = p
    return (k * x*x / 2 + c3 * x**3 / 6 + c4 * x**4 / 24,
            k * x + c3 * x*x / 2 + c4 * x**3 / 6,
            k + c3 * x + c4 * x*x / 2)

def edge(u, v, p, q, g):
    pu, du, ddu = graph(u, p)
    pv, dv, ddv = graph(v, q)
    h, w = g + pu + pv, u - v
    L = math.hypot(h, w)
    au, av = h * du + w, h * dv - w
    eu, ev = au / L, av / L
    huu = (du*du + h*ddu + 1) / L - au*au / L**3
    hvv = (dv*dv + h*ddv + 1) / L - av*av / L**3
    huv = (du*dv - 1) / L - au*av / L**3
    return L, eu, ev, huu, hvv, huv

def assemble(x, start, graphs, g):
    j = len(x) - 1
    es = [edge(x[i], x[i+1], graphs[(start+i)%2], graphs[(start+i+1)%2], g) for i in range(j)]
    gradient = np.array([es[i-1][2] + es[i][1] for i in range(1, j)])
    diagonal = np.array([es[i-1][4] + es[i][3] for i in range(1, j)])
    off = np.array([es[i][5] for i in range(1, j-1)])
    return es, gradient, diagonal, off

def tridiagonal_solve(diagonal, off, rhs):
    ab = np.zeros((3, len(diagonal)))
    ab[1] = diagonal
    if len(off):
        ab[0, 1:], ab[2, :-1] = off, off
    return solve_banded((1, 1), ab, rhs, check_finite=True)

def bridge(j, start, u, v, graphs, g):
    c = [1 + g*p[0] for p in graphs]
    gamma = math.acosh(math.sqrt(c[0]*c[1]))
    sig = lambda i: math.sqrt(c[1-(start+i)%2])
    x = np.array([sig(i)/sig(0)*math.sinh((j-i)*gamma)/math.sinh(j*gamma)*u
                  + sig(i)/sig(j)*math.sinh(i*gamma)/math.sinh(j*gamma)*v for i in range(j+1)])
    for _ in range(15):
        es, grad, diag, off = assemble(x, start, graphs, g)
        if not len(grad) or np.max(np.abs(grad)) < 3e-15:
            break
        x[1:-1] -= tridiagonal_solve(diag, off, grad)
    es, grad, diag, off = assemble(x, start, graphs, g)
    residual = float(np.max(np.abs(grad))) if len(grad) else 0.
    check(residual < 2e-13, 'euclidean_bridges', 'stationarity residual')
    check(all(e[5] < 0 for e in es), 'euclidean_bridges', 'negative flight twists')
    pivots = []
    for i, d in enumerate(diag):
        pivots.append(float(d if i == 0 else d - off[i-1]**2 / pivots[-1]))
    check(all(p > 0 for p in pivots), 'euclidean_bridges', 'positive Hessian pivots')
    a = [math.sqrt(c[0]*c[1])*math.sinh(gamma)/(g*c[1-b]) for b in (0, 1)]
    d0 = math.sqrt(a[start]*a[(start+j)%2])/math.sinh(j*gamma)
    logtwist = math.fsum(math.log(-e[5]) for e in es) - math.fsum(math.log(p) for p in pivots)
    bnorm = math.exp(logtwist-math.log(d0))
    energy = math.fsum(e[0]-g for e in es)
    return bnorm, energy, x, residual, es, diag, off, d0

def physical_checks():
    rows = []
    worst_ref, worst_schur, worst_residual = 0., 0., 0.
    models = ((1., ((.7, .4, .8), (1.3, -.3, 1.1))),
              (.8, ((1., .2, .6), (1., -.4, .9))))
    for model_id, (g, graphs) in enumerate(models):
        for start in (0, 1):
            for j in (1, 2, 3, 4, 8, 9, 16, 17, 32, 33):
                ans = bridge(j, start, 0., 0., graphs, g)
                referr = abs(ans[0]-1)
                worst_ref = max(worst_ref, referr)
                check(referr < 2e-12, 'reference_normalization', f'j={j}, start={start}')
            for j in (4, 8, 16, 32):
                u, v = .07, -.05
                ans = bridge(j, start, u, v, graphs, g)
                bu = bridge(j, start, u, 0., graphs, g)[0]
                bv = bridge(j, start, 0., v, graphs, g)[0]
                sep = abs(ans[0]/(bu*bv)-1)
                worst_residual = max(worst_residual, ans[3])
                # Direct Schur complement for the reduced mixed derivative.
                es, diag, off = ans[4:7]
                rhs = np.zeros(j-1); rhs[-1] = 1.
                inverse_entry = tridiagonal_solve(diag, off, rhs)[0]
                direct_twist = es[0][5]*es[-1][5]*inverse_entry
                schur = abs(direct_twist/(ans[0]*ans[7])-1)
                worst_schur = max(worst_schur, schur)
                check(schur < 2e-11, 'cofactor_schur', 'physical mixed derivative')
                rows.append({'model': model_id, 'start': start, 'flights': j,
                             'relative_separation_defect': float(f'{sep:.12g}')})
                if j == 32:
                    check(sep < 5e-11, 'relative_separation', 'separated boundary factors')
    # Compare the truncated half-line determinant with the scalar product
    # obtained by differentiating the actual stable return twice in flight.
    g, graphs = models[0]
    c = [1+g*p[0] for p in graphs]
    gamma = math.acosh(math.sqrt(c[0]*c[1])); lam = math.exp(-2*gamma)
    u = .07
    n, tail = 5, 32
    full = bridge(2*n+tail, 0, u, 0., graphs, g)
    x = full[2]
    ret_product = 1.
    for i in range(2*n):
        # Derivative of the next stationary coordinate with terminal point fixed.
        es, grad, diag, off = assemble(x[i:], i%2, graphs, g)
        rhs = np.zeros(len(diag)); rhs[0] = -es[0][5]
        phi_prime = tridiagonal_solve(diag, off, rhs)[0]
        ret_product *= phi_prime
    scaled = ret_product/lam**n
    remainder_B = bridge(tail, 0, float(x[2*n]), 0., graphs, g)[0]
    cocycle_error = abs(scaled*remainder_B/full[0]-1)
    check(cocycle_error < 2e-10, 'physical_scalar_identification', 'truncated stable derivative product')
    return {'models': [{'gap': g, 'graphs_kappa_cubic_quartic': graphs} for g, graphs in models],
            'separation_rows': rows, 'maximum_zero_endpoint_reference_error': worst_ref,
            'maximum_cofactor_schur_relative_error': worst_schur,
            'maximum_stationarity_residual': worst_residual,
            'truncated_scalar_product_relative_error': cocycle_error,
            'scalar_product_returns': n, 'terminal_tail_flights': tail}

def inverse_checks():
    for m in range(2, 10):
        for v in (F(1, 5), F(1, 3), F(1, 2)):
            Em = v**(4*(m-1))/(1-v**(4*(m-1))) - v**(4*m)/(1-v**(4*m))
            Om = v**(2*(m-1))/(1-v**(4*(m-1))) - v**(2*m)/(1-v**(4*m))
            P = (1+v**(4*m))/(1-v**(4*m)) + 2*m*Em
            Q = 2*v**(2*m)/(1-v**(4*m)) + 2*m*Om
            tm = lambda k: (1-v**(2*k))/(1+v**(2*k))
            check(P-Q == m*tm(m-1)-(m-1)*tm(m), 'exact_contact_blocks', 'antisymmetric formula')
            check(P > Q > 0, 'exact_contact_blocks', 'positive eigenvalues')
        for z in (F(1, 10), F(1), F(3)):
            U, V = (1+2*z)**m, 1+2*m*z
            s = sum(F(math.comb(m, r))*(2*z)**r for r in range(2, m+1))
            check(U-V == s and s > 0, 'exact_contact_blocks', 'two-flight separation')
    check(F(49-13, 1728) == F(1, 48), 'exact_contact_blocks', 'printed quartic example')
    # Width/profile inverse in the variable t=sqrt(E); coefficients are rational.
    for k in range(9):
        width_coefficient = F(2, 2*k+1)
        recovered = width_coefficient * F(2*k+1, 2)
        check(recovered == 1, 'exact_width_profile', f'monomial degree {k}')
    return {'orders_m': list(range(2, 10)), 'width_monomial_degrees': list(range(9))}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = {'reviewed_commit': '627c16b951994fa65acfbf3a621d0e4306131db3',
              'scope': 'Independent finite exact and floating-point diagnostics, not theorem certification.',
              'scalar': scalar_checks(), 'physical': physical_checks(), 'inverse': inverse_checks()}
    result['checks_by_group'] = dict(sorted(COUNTS.items()))
    result['total_checks'] = sum(COUNTS.values())
    result['status'] = 'PASS'
    result['versions'] = {'numpy': np.__version__, 'scipy': scipy.__version__}
    result['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(f'PASS: {result["total_checks"]} explicit checks; {args.output}')

if __name__ == '__main__':
    main()
