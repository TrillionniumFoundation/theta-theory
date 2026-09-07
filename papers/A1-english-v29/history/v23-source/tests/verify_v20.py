#!/usr/bin/env python3
"""Exact finite diagnostics for the v20 kernel criterion.

No repository theorem/proof code is imported. Finite examples are not proof
verification, a universal feasibility solver, or minimax optimization.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform
import sys
import sympy as S

COUNTS: Counter[str] = Counter()
DETAILS: dict[str, object] = {}

def check(condition: object, group: str) -> None:
    if condition is not True and condition != S.true:
        raise AssertionError(f'{group}: {condition}')
    COUNTS[group] += 1

def basis(matrix: S.Matrix) -> S.Matrix:
    cols = matrix.columnspace()
    return S.Matrix.hstack(*cols) if cols else S.zeros(matrix.rows, 0)

def annihilator(matrix: S.Matrix) -> S.Matrix:
    cols = matrix.T.nullspace()
    return S.Matrix.hstack(*cols).T if cols else S.zeros(0, matrix.rows)

def finite_pencil(E: S.Matrix, F: S.Matrix, U: S.Matrix,
                  weights: list[S.Rational]) -> dict[str, object]:
    """Evaluation columns for E,F; U contains coefficients in the F basis."""
    n, d = E.shape
    k = F.cols
    check(F.rows == n and len(weights) == n, 'pencil_dimensions')
    check(E.rank() == d and F.rank() == k and U.rank() == U.cols,
          'pencil_dimensions')
    check(sum(weights) == 1 and all(w > 0 for w in weights), 'positive_slice')
    eu = [E[:, a].multiply_elementwise((F * U)[:, i])
          for a in range(d) for i in range(U.cols)]
    W = basis(S.Matrix.hstack(*eu)) if eu else S.zeros(n, 0)
    D = S.diag(*weights)
    one = S.ones(n, 1)
    check(one.T * D * W == S.zeros(1, W.cols), 'positive_slice')
    products = [E[:, a].multiply_elementwise(F[:, i])
                for a in range(d) for i in range(k)]
    V = basis(S.Matrix.hstack(one, *products))
    chosen = S.Matrix.hstack(W, one)
    vs = []
    for col in V.columnspace():
        if chosen.row_join(col).rank() > chosen.cols:
            chosen = chosen.row_join(col)
            vs.append(col)
    v = S.Matrix.hstack(*vs) if vs else S.zeros(n, 0)
    check(chosen.cols == V.cols, 'quotient_coordinates')
    complement = U.copy()
    fs = []
    for col in S.eye(k).columnspace():
        if complement.row_join(col).rank() > complement.cols:
            complement = complement.row_join(col)
            fs.append(col)
    Q = S.Matrix.hstack(*fs) if fs else S.zeros(k, 0)
    z = S.symbols(f'z0:{len(vs)}')
    H = S.zeros(d, Q.cols)
    for a in range(d):
        for i in range(Q.cols):
            value = E[:, a].multiply_elementwise((F * Q)[:, i])
            coeff = chosen.gauss_jordan_solve(value)[0]
            H[a, i] = coeff[W.cols] + sum(coeff[W.cols + 1 + j] * z[j]
                                          for j in range(len(vs)))
    means = list(one.T * D * v)
    check(H.subs(dict(zip(z, means))) == E.T * D * F * Q,
          'quotient_pairing_identity')
    projector = W * (W.T * D * W).inv() * W.T * D if W.cols else S.zeros(n)
    h = v - one * (one.T * D * v) - projector * v
    B = h.T * D * h
    check(one.T * D * h == S.zeros(1, h.cols), 'local_tilt_identities')
    check(W.T * D * h == S.zeros(W.cols, h.cols), 'local_tilt_identities')
    check(v.T * D * h == B, 'local_tilt_identities')
    for r in range(1, B.rows + 1):
        check(B[:r, :r].det() > 0, 'positive_gram')
    A = annihilator(W)
    equations = S.Matrix.vstack(*(A * S.diag(*list(E[:, a])) * F
                                  for a in range(d))) if d else S.zeros(0, k)
    closure = k - equations.rank()
    return dict(H=H, rank=H.rank(), q=Q.cols, W=W, V=V, Q=Q,
                v=v, h=h, B=B, z=z, means=means, closure=closure)

def block_data(n: int, m: int):
    points = [(j, sign) for j in range(1, n + 1) for sign in (-1, 1)]
    E = S.Matrix([[int(j == i) for i in range(1, n + 1)] for j, sign in points])
    F = S.Matrix([[1] + [sign * j**ell for ell in range(m)] for j, sign in points])
    return points, E, F

def eight_point_and_pencils() -> None:
    points, E, F = block_data(4, 2)
    sigma = S.Matrix([0, 1, 0])
    weights = [S.Rational(j, 20) for j, sign in points]
    model = finite_pencil(E, F, sigma, weights)
    check(model['rank'] == 1 and model['q'] == 2, 'eight_point_counterexample')
    check(model['closure'] == 2, 'eight_point_counterexample')
    G = E.applyfunc(lambda x: x)  # product evaluations for U=span sigma
    G = S.diag(*[sign for j, sign in points]) * G
    check(set(map(tuple, G.tolist())) ==
          {tuple(sign * int(i == j) for i in range(4))
           for j in range(4) for sign in (-1, 1)}, 'eight_point_crosspolytope')
    check(S.ones(1, 8) * G == S.zeros(1, 4) and G.rank() == 4,
          'eight_point_crosspolytope')
    s = S.symbols('s1:5', positive=True)
    d = S.symbols('d1:5', real=True)
    H = S.Matrix([[s[j - 1], d[j - 1], j * d[j - 1]] for j in range(1, 5)])
    restricted = H.subs(dict.fromkeys(d, 0))
    check(restricted.rank() == 1 and restricted[:, 1:] == S.zeros(4, 2),
          'eight_point_counterexample')
    exact_ranks = []
    for root in range(1, 5):
        U = S.Matrix([0, -root, 1])
        q = finite_pencil(E, F, U, weights)
        check(q['rank'] == q['q'] == 2 and q['closure'] == 1,
              'eight_point_positive_exact_alternatives')
        exact_ranks.append(q['rank'])
        # Small positive local tilts preserve U and attain the generic rank.
        h, z, B = q['h'], q['z'], q['B']
        grid = (-S.Rational(1, 1000), S.Integer(0), S.Rational(1, 1000))
        found = False
        for coords in product(grid, repeat=h.cols):
            t = S.Matrix(coords)
            perturbation = h * t
            if max(map(abs, perturbation)) >= S.Rational(1, 10):
                continue
            w = [wi * (1 + hi) for wi, hi in zip(weights, perturbation)]
            actual = E.T * S.diag(*w) * F
            check(sum(w) == 1 and all(wi > 0 for wi in w), 'local_positive_witness')
            check(actual * U == S.zeros(4, 1), 'local_positive_witness')
            new_means = S.Matrix(q['means']) + B * t
            check(q['H'].subs(dict(zip(z, new_means))) == actual * q['Q'],
                  'local_positive_witness')
            if actual.rank() == 2:
                found = True
                break
        check(found, 'finite_grid_rank_witness')
    DETAILS['eight_point'] = {'containment_rank': 1, 'forced_nullity': 2,
                             'requested_nullity': 1, 'exact_alternative_ranks': exact_ranks}

def edge_cases() -> None:
    E = S.Matrix([[-1], [1]])
    F = S.ones(2, 1)
    for U, expected_rank, expected_q in ((S.ones(1, 1), 0, 0),
                                         (S.zeros(1, 0), 1, 1)):
        data = finite_pencil(E, F, U, [S.Rational(1, 2)] * 2)
        check(data['rank'] == expected_rank and data['q'] == expected_q,
              'zero_and_empty_dimensions')
    data = finite_pencil(S.ones(1, 1), S.ones(1, 1), S.zeros(1, 0), [S.Integer(1)])
    check(data['rank'] == 1 and data['B'].shape == (0, 0), 'zero_moment_dimension')
    # More columns than rows, without a fixed common kernel.
    data = finite_pencil(S.ones(3, 1), S.Matrix([[1, -1], [1, 0], [1, 1]]),
                         S.zeros(2, 0), [S.Rational(1, 3)] * 3)
    check(data['rank'] == 1 and data['q'] == 2 and data['closure'] == 0,
          'closure_not_sufficient_for_exact_kernel')
    # Positive certificate is incompatible with an annihilating probability.
    positive_function = [S.Integer(1), S.Integer(2), S.Integer(4)]
    for a, b in product((1, 2, 3), repeat=2):
        weights = [S.Rational(a, a + b + 1), S.Rational(b, a + b + 1),
                   S.Rational(1, a + b + 1)]
        check(sum(w * f for w, f in zip(weights, positive_function)) > 0,
              'infeasible_positive_certificate')

def block_classification() -> None:
    x = S.Symbol('x')
    cases = 0
    for n, m in ((3, 1), (3, 2), (4, 2), (4, 3), (5, 3)):
        points, E, F = block_data(n, m)
        for count in range(m):
            for roots in combinations(range(1, n + 1), count):
                factor = S.prod(x - j for j in roots)
                U = S.Matrix([[0] * (m - count)] +
                    [[S.expand(factor * x**ell).coeff(x, power)
                      for ell in range(m - count)] for power in range(m)])
                weights = [S.Rational(1, 2*n) +
                           (S.Rational(sign, 4*n) if j in roots else 0)
                           for j, sign in points]
                H = E.T * S.diag(*weights) * F
                check(all(w > 0 for w in weights) and sum(weights) == 1,
                      'block_positive_prior')
                check(H * U == S.zeros(n, m-count), 'block_exact_kernel')
                check(H.rank() == 1 + count and U.rank() == m-count,
                      'block_exact_kernel')
                root_eval = S.Matrix([[j**ell for ell in range(m)] for j in roots])
                if roots:
                    check(root_eval.rank() == count, 'polynomial_root_classification')
                else:
                    check(U.rank() == m, 'polynomial_root_classification')
                # The actual normalized derivative is the physical covariance.
                acquisition = S.Matrix([[S.Rational(int(j == i), 2*(n-1))
                                        for i in range(1, n)] for j, sign in points])
                queries = S.Matrix([[S.Rational(1, 2) +
                                     S.Rational(sign, 4) * S.Rational(j, n)**ell
                                     for ell in range(m)] for j, sign in points])
                w = S.Matrix(weights)
                C = queries.T * S.diag(*weights) * acquisition - (queries.T*w)*(w.T*acquisition)
                check(C.rank() == count, 'physical_prediction_rank')
                for row in queries.tolist():
                    check(all(S.Rational(1,4) <= v <= S.Rational(3,4) for v in row),
                          'physical_query_bounds')
                for row in acquisition.tolist():
                    check(sum(map(abs, row)) <= S.Rational(1,2), 'physical_likelihood_bound')
                cases += 1
    # A subspace not saturated under all polynomial multiples is not exact.
    points, E, F = block_data(5, 3)
    U = S.Matrix([0, -2, 1, 0])  # span sigma(x-2), but closure has dimension two
    weights = [S.Rational(1, 10)] * 10
    data = finite_pencil(E, F, U, weights)
    check(data['rank'] == 2 and data['q'] == 3 and data['closure'] == 2,
          'non_root_saturated_subspace')
    DETAILS['exact_block_families'] = cases

def tensor_grid() -> None:
    a, b = S.symbols('a b')
    for degree in range(1, 5):
        grid = [S.Rational(j, 100) for j in range(degree + 1)]
        polynomial = S.prod(a - grid[j] for j in range(degree)) + b**degree
        values = [polynomial.subs({a: i, b: j}) for i, j in product(grid, repeat=2)]
        check(any(v != 0 for v in values), 'tensor_grid_polynomial_witness')
        vandermonde = S.Matrix([[x**j for j in range(degree+1)] for x in grid])
        check(vandermonde.det() != 0, 'tensor_grid_interpolation')

def source_scope() -> None:
    root = Path(__file__).resolve().parents[1]
    intro = (root/'sections/introduction.tex').read_text()
    theorem = (root/'sections/exact_kernels.tex').read_text()
    check('all possible kernel subspaces' not in intro, 'scope_regression')
    check('eq:exact-kernel-criterion' in theorem and 'eq:block-root-condition' in theorem,
          'scope_regression')
    check('tab:scope' in intro and 'thm:intrinsic-streaming' in intro, 'scope_regression')

if __name__ == '__main__':
    eight_point_and_pencils()
    edge_cases()
    block_classification()
    tensor_grid()
    source_scope()
    report = {'version': 20, 'passed': True, 'assertions': sum(COUNTS.values()),
              'checks_by_group': dict(COUNTS), 'details': DETAILS,
              'python': platform.python_version(), 'sympy': S.__version__,
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'Exact finite and symbolic author diagnostics, not universal proof verification, independent peer review, or optimization over all encoders.'}
    target = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'validation/V20_DIAGNOSTICS.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
