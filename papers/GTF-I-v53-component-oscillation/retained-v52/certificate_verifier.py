"""Exact, deliberately bounded verification of supplied rational SOS certificates.

This module verifies identities; it does not search for certificates. Gram
matrices are capped at order 12 because all principal minors are checked.
No floating-point entries, approximate equalities, or solver status are trusted.
"""
from __future__ import annotations
import itertools
from typing import Sequence
import sympy as s

MAX_GRAM_ORDER = 12


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def rational_polynomial(poly: s.Expr, variables: Sequence[s.Symbol]) -> s.Poly:
    require(not s.sympify(poly).atoms(s.Float), 'floating-point coefficient')
    require(s.sympify(poly).free_symbols <= set(variables), 'undeclared variable')
    try:
        return s.Poly(poly, *variables, domain=s.QQ)
    except (s.PolynomialError, s.CoercionFailed) as exc:
        raise ValueError('not a rational polynomial') from exc


def gram_polynomial(monomials: Sequence[s.Expr], gram: s.Matrix,
                    variables: Sequence[s.Symbol]) -> s.Expr:
    n = len(monomials)
    require(0 <= n <= MAX_GRAM_ORDER, 'Gram order exceeds verification limit')
    require(gram.shape == (n, n), 'Gram shape mismatch')
    require(gram == gram.T, 'nonsymmetric Gram matrix')
    require(all(v.is_Rational for v in gram), 'nonrational Gram entry')
    for term in monomials:
        polynomial = rational_polynomial(term, variables)
        require(len(polynomial.terms()) == 1, 'basis entry is not a monomial')
        require(polynomial.terms()[0][1] == 1, 'monomial coefficient is not one')
    for length in range(1, n + 1):
        for ids in itertools.combinations(range(n), length):
            require(gram.extract(ids, ids).det() >= 0, 'Gram is not positive semidefinite')
    if n == 0:
        return s.Integer(0)
    vector = s.Matrix(monomials)
    return s.expand((vector.T * gram * vector)[0])


def check_sos(q: s.Expr, lam: s.Rational, variables: Sequence[s.Symbol],
              box: Sequence[tuple[s.Rational, s.Rational]],
              terms: Sequence[tuple[Sequence[s.Expr], s.Matrix]]) -> None:
    """Verify q-lam = sigma[-1] + sigma[0]*g0 + sum sigma[i]*gi.

    The box must be within [-1,1]^n, with g0=n-sum(x*x). Every Gram
    matrix must be rational and of order at most MAX_GRAM_ORDER.
    A successful return certifies q >= lam > 0 on that complete box.
    """
    n = len(variables)
    require(n > 0 and len(set(variables)) == n, 'variable list')
    require(len(box) == n and len(terms) == n + 2, 'missing bound or SOS term')
    require(s.sympify(lam).is_Rational and lam > 0, 'positive rational margin required')
    rational_polynomial(q, variables)
    generators = [s.Integer(1), n - sum(v*v for v in variables)]
    for variable, (left, right) in zip(variables, box):
        require(s.sympify(left).is_Rational and s.sympify(right).is_Rational,
                'nonrational interval')
        require(-1 <= left < right <= 1, 'invalid interval')
        generators.append((variable-left)*(right-variable))
    rhs = sum(gram_polynomial(m, G, variables)*g
              for (m, G), g in zip(terms, generators))
    require(rational_polynomial(s.expand(q-lam-rhs), variables).is_zero,
            'coefficient identity failed')


def local_linear_system(P: s.Matrix, Z: s.Matrix, Q: s.Matrix,
                        Y: s.Matrix, U: s.Matrix) -> tuple[s.Matrix, s.Matrix]:
    """Return complete B,b in row-major vec(T) order, including range invariance."""
    k, d = Z.shape
    ell = Y.rows
    require(P.shape == (k, k) and Q.shape == (ell, ell), 'projector shape')
    require(Y.cols == d and U.shape == (d, d), 'mean or command shape')
    variables = s.symbols(f't0:{k*ell}')
    T = s.Matrix(k, ell, variables)
    residuals = list(T*s.ones(ell, 1)-s.ones(k, 1))
    residuals += list(P*T*(s.eye(ell)-Q))
    residuals += list(P*(T*Y-Z*U.T))
    return s.linear_eq_to_matrix(residuals, variables)
