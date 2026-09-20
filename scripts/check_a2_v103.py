#!/usr/bin/env python3
"""Exact, finite certificates for A2 v103; not a proof verifier.

Run with Python 3.10+ and SymPy. No floating-point differentiation,
network access, random samples, or repository mutation is used.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
import sympy as sp

PRIME = 1000003
N_JETS = 3  # alpha_1, u_11, u_12; clocks, weights, roots and V stay fixed.


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def residue(value: Any) -> int:
    num, den = sp.fraction(sp.cancel(value))
    return (int(num) % PRIME) * pow(int(den) % PRIME, -1, PRIME) % PRIME


def matrix_residues(matrix: sp.Matrix) -> list[list[int]]:
    return [[residue(matrix[i, j]) for j in range(matrix.cols)]
            for i in range(matrix.rows)]


class Jet:
    """First jets in three variables over the prime field; inverses check units."""
    def __init__(self, value: int, gradient: Any = None):
        self.value = int(value) % PRIME
        self.gradient = tuple(int(x) % PRIME for x in gradient) if gradient is not None else (0,) * N_JETS
        if len(self.gradient) != N_JETS:
            raise ValueError('Incorrect jet dimension')

    @staticmethod
    def cast(other: Any) -> Jet:
        return other if isinstance(other, Jet) else Jet(int(other))

    def __add__(self, other: Any) -> Jet:
        other = Jet.cast(other)
        return Jet(self.value + other.value, [a + b for a, b in zip(self.gradient, other.gradient)])

    __radd__ = __add__

    def __neg__(self) -> Jet:
        return Jet(-self.value, [-a for a in self.gradient])

    def __sub__(self, other: Any) -> Jet:
        return self + -Jet.cast(other)

    def __rsub__(self, other: Any) -> Jet:
        return Jet.cast(other) + -self

    def __mul__(self, other: Any) -> Jet:
        other = Jet.cast(other)
        return Jet(self.value * other.value,
                   [a * other.value + self.value * b for a, b in zip(self.gradient, other.gradient)])

    __rmul__ = __mul__

    def inverse(self) -> Jet:
        inv = pow(self.value, -1, PRIME)
        return Jet(inv, [-a * inv * inv for a in self.gradient])

    def __truediv__(self, other: Any) -> Jet:
        return self * Jet.cast(other).inverse()

    def __rtruediv__(self, other: Any) -> Jet:
        return Jet.cast(other) * self.inverse()

    def __pow__(self, exponent: int) -> Jet:
        if not isinstance(exponent, int):
            raise TypeError('Only integer powers are supported')
        if exponent < 0:
            return self.inverse() ** (-exponent)
        result = Jet(1)
        for _ in range(exponent):
            result = result * self
        return result


def variable(num: int, den: int, index: int) -> Jet:
    gradient = [0] * N_JETS
    gradient[index] = 1
    return Jet(num * pow(den, -1, PRIME), gradient)


def native_design() -> tuple[dict[str, Any], sp.Matrix]:
    """Compute the information and weight derivative over Q, then reduce."""
    r = sp.Rational
    u = [sp.Matrix([r(4, 5), r(1, 5)]), sp.Matrix([r(1, 5), r(4, 5)])]
    v = [sp.Matrix([r(3, 4), r(1, 4)]), sp.Matrix([r(1, 4), r(3, 4)])]
    alpha = [r(2, 5), r(3, 5)]
    direction = sp.Matrix([1, -1])
    blocks = []
    for clock in range(4, 9):
        f = [sp.Integer((clock - 1) ** 2), sp.Integer((clock - 2) ** 2)]
        q = sum(alpha[a] * f[a] for a in range(2))
        K = sum((alpha[a] * f[a] * u[a] * v[a].T for a in range(2)), sp.zeros(2))
        pairs = []
        for a in range(2):
            df = -(clock - a - 1)
            pairs.append((alpha[a] * df * u[a] * v[a].T, alpha[a] * df))
        pairs.append((f[0] * u[0] * v[0].T - f[1] * u[1] * v[1].T, f[0] - f[1]))
        pairs.extend((alpha[a] * f[a] * direction * v[a].T, 0) for a in range(2))
        pairs.extend((alpha[a] * f[a] * u[a] * direction.T, 0) for a in range(2))
        pairs.extend((-alpha[a] * u[a] * v[a].T, -alpha[a]) for a in range(2))
        score = sp.Matrix.hstack(*[sp.Matrix([(q * dk - K * dq)[i, j] / q ** 2
                         for i in range(2) for j in range(2)]) for dk, dq in pairs])
        W = sp.diag(*[q / K[i, j] for i in range(2) for j in range(2)])
        require(all(K[i, j] > 0 for i in range(2) for j in range(2)), 'Probability positivity failed')
        require(sum(K) == q, 'Probability normalization failed')
        blocks.append((score[:, :7], score[:, 7:], W, score.T * W * score))
    info = sum((b[3] for b in blocks), sp.zeros(9)) / 5
    free = info[:7, :7]
    B = free.inv() * info[:7, 7:]
    Q = info[7:, 7:] - info[7:, :7] * B
    require(Q == Q.T and Q[0, 0] > 0 and Q.det() > 0, 'Real quotient positivity failed')
    G = []
    for L, D, W, _ in blocks:
        E = D - L * B
        G.append(E.T * W * E)
    derivative = sp.Matrix.hstack(*[sp.Matrix([g[0, 0] - G[-1][0, 0],
          g[0, 1] - G[-1][0, 1], g[1, 1] - G[-1][1, 1]]) for g in G[:-1]])
    expected = [[235716, 140518, 511071, 71108], [695313, 878177, 193809, 605568],
                [150377, 764535, 992260, 912493]]
    require(matrix_residues(derivative) == expected, 'Design derivative certificate mismatch')
    require(residue(derivative[:, :3].det()) == 230039, 'Design minor mismatch')
    require(residue(free.det()) == 743349, 'Free information determinant mismatch')
    return {'arithmetic': 'rational, followed by unit-denominator reduction',
            'fixed_clocks': list(range(4, 9)), 'base_weights': '1/5 each',
            'profile_B_mod': matrix_residues(B), 'quotient_mod': matrix_residues(Q),
            'I_LL_determinant_mod': residue(free.det()), 'weight_jacobian_mod': expected,
            'first_three_minor_mod': 230039, 'real_quotient_positive_definite': True}, info


def native_centre(rational_info: sp.Matrix) -> dict[str, Any]:
    """Exact first jets for a fixed experiment; no weight or metric variation."""
    alpha0 = variable(2, 5, 0)
    alpha = [alpha0, 1 - alpha0]
    u0 = [variable(4, 5, 1), variable(1, 5, 2)]
    v0 = [Jet(3) / 4, Jet(1) / 4]
    u = [[a, 1 - a] for a in u0]
    v = [[a, 1 - a] for a in v0]
    direction = [1, -1]
    info = [[Jet(0) for _ in range(9)] for _ in range(9)]
    for clock in range(4, 9):
        f = [(clock - 1) ** 2, (clock - 2) ** 2]
        q = sum(alpha[a] * f[a] for a in range(2))
        K = [[sum(alpha[a] * f[a] * u[a][i] * v[a][j] for a in range(2))
              for j in range(2)] for i in range(2)]
        pairs = []
        for a in range(2):
            df = -(clock - a - 1)
            pairs.append(([[alpha[a] * df * u[a][i] * v[a][j] for j in range(2)]
                           for i in range(2)], alpha[a] * df))
        pairs.append(([[f[0] * u[0][i] * v[0][j] - f[1] * u[1][i] * v[1][j]
                       for j in range(2)] for i in range(2)], Jet(f[0] - f[1])))
        pairs.extend(([[alpha[a] * f[a] * direction[i] * v[a][j] for j in range(2)]
                       for i in range(2)], Jet(0)) for a in range(2))
        pairs.extend(([[alpha[a] * f[a] * u[a][i] * direction[j] for j in range(2)]
                       for i in range(2)], Jet(0)) for a in range(2))
        pairs.extend(([[-alpha[a] * u[a][i] * v[a][j] for j in range(2)]
                       for i in range(2)], -alpha[a]) for a in range(2))
        score = [[(q * dk[i][j] - K[i][j] * dq) / q ** 2 for dk, dq in pairs]
                 for i in range(2) for j in range(2)]
        W = [q / K[i][j] for i in range(2) for j in range(2)]
        for k in range(9):
            for l in range(9):
                info[k][l] += sum(score[e][k] * W[e] * score[e][l] for e in range(4)) / 5
    values = sp.Matrix([[x.value for x in row] for row in info])
    require(matrix_residues(rational_info) == matrix_residues(values), 'Jet/rational base cross-check failed')
    B = (values[:7, :7].inv_mod(PRIME) * values[:7, 7:]).applyfunc(lambda x: int(x) % PRIME)
    Z = (-B).col_join(sp.eye(2))
    cols = []
    for n in range(N_JETS):
        derivative = sp.Matrix([[x.gradient[n] for x in row] for row in info])
        profiled = (Z.T * derivative * Z).applyfunc(lambda x: int(x) % PRIME)
        cols.append(sp.Matrix([profiled[0, 0], profiled[0, 1], profiled[1, 1]]))
    jacobian = sp.Matrix.hstack(*cols)
    expected = [[578035, 241954, 31304], [915041, 708926, 260448], [254308, 573529, 493204]]
    require(matrix_residues(jacobian) == expected, 'Centre derivative certificate mismatch')
    require(int(jacobian.det()) % PRIME == 933885, 'Centre minor mismatch')
    return {'arithmetic': 'exact first jets over the prime field, with checked inverses',
            'parameters': ['alpha1', 'u11', 'u12'], 'fixed_clocks': list(range(4, 9)),
            'fixed_weights': '1/5 each', 'fixed_roots': [1, 2], 'fixed_second_channel': True,
            'centre_jacobian_mod': expected, 'determinant_mod': 933885,
            'independent_rational_base_information_match': True}


def structural_identities() -> dict[str, Any]:
    x, y, z, a, b, c, d = sp.symbols('x y z a b c d', real=True)
    substitutions = 0
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            require(sp.expand((a*x**3+b*y**3).subs({x:s1*z, y:s2*z}) - z**3*(a*s1+b*s2)) == 0,
                    'Coupled first residual mismatch')
            require(sp.expand((c*x**2*y**2+d*x**3*y).subs({x:s1*z, y:s2*z}) - z**4*(c+d*s1*s2)) == 0,
                    'Coupled second residual mismatch')
            substitutions += 2
    u = sp.Matrix([1, -1]); A = 3 * sp.eye(2)
    endpoint = sp.Matrix.vstack(sp.Matrix.hstack(A, u), sp.Matrix.hstack(u.T, sp.ones(1)))
    require(endpoint.det() > 0 and (A-u*u.T).det() > 0, 'Mixed endpoint example is not positive')
    one_endpoint_checks = 0
    for xx in (sp.Matrix([2,1]), sp.Matrix([1,2]), sp.Matrix([1,1]), sp.zeros(2,1)):
        for cc in (sp.Rational(1,4), sp.Integer(1), sp.Integer(4)):
            bb = sp.sqrt(cc)*u
            zz = max(sp.Integer(0), -(bb.T*xx)[0]/cc)
            actual = (xx.T*A*xx)[0] + 2*(bb.T*xx)[0]*zz + cc*zz**2
            target = (xx.T*A*xx)[0] - min((u.T*xx)[0], sp.Integer(0))**2
            require(sp.simplify(actual-target) == 0, 'Endpoint rescaling failed')
            one_endpoint_checks += 1
    L = sp.Matrix([[1,0],[1,1],[0,1]])
    centre = sp.Matrix([1,0,2]); H = sp.Matrix([[3,1,0],[1,4,1],[0,1,2]])
    optimum = -(L.T*H*L).inv()*L.T*H*centre
    residual = centre+L*optimum
    require(L.T*H*residual == sp.zeros(2,1), 'Affine metric projection failed')
    mean=sp.Matrix([2,-1]); cov=sp.diag(1,4)
    points=[mean+sp.Matrix([2,0]),mean-sp.Matrix([2,0]),mean+sp.Matrix([0,4]),mean-sp.Matrix([0,4])]
    # These equal-weight pairs have covariance diag(2,8).
    moment=sum((p.col_join(sp.ones(1))*p.col_join(sp.ones(1)).T for p in points),sp.zeros(3))/4
    require(moment[:2,:2]-mean*mean.T == 2*cov and moment[2,2] == 1, 'Affine moment identity failed')
    return {'coupled_polynomial_substitutions': substitutions,
            'one_endpoint_exact_checks': one_endpoint_checks,
            'affine_projection_stationarity': True, 'affine_moment_identity': True,
            'scope': 'Finite diagnostics of displayed constructions; universal proofs are in the manuscript.'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    require(bool(sp.isprime(PRIME)), 'Certificate modulus is not prime')
    design, info = native_design()
    centre = native_centre(info)
    result = {'status': 'exact_checks_passed', 'prime': PRIME, 'sympy_version': sp.__version__,
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'native_design': design, 'native_fixed_experiment': centre,
              'structural_diagnostics': structural_identities(),
              'scope': 'Exact finite rank certificates and displayed-example checks, not formal verification of universal theorems.'}
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main()
