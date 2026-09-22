"""Exact regression checks for v122. No general proof/priority certification.

The explicit rank-eleven example is checked over QQ on every projective
chart. Ideal intersections use elimination, not floating-point ranks.
"""
from __future__ import annotations
import itertools
import sympy as s


def intersection(left, right, variables):
    z = s.Dummy('elimination')
    basis = s.groebner([z*f for f in left] + [(1-z)*g for g in right],
                      z, *variables, order='lex', domain=s.QQ)
    return [g.as_expr() for g in basis.polys if not g.as_expr().has(z)]


def same_ideal(left, right, variables):
    a = s.groebner(left, *variables, order='grevlex', domain=s.QQ)
    b = s.groebner(right, *variables, order='grevlex', domain=s.QQ)
    return all(a.reduce(g)[1] == 0 for g in right) and all(b.reduce(f)[1] == 0 for f in left)


def check_powers():
    t, f = s.symbols('t f')
    records = []
    for n in range(1, 9):
        power = [t**(n+i)*f**(n-i) for i in range(n+1)]
        primary = [t**i*f**(2*n-i) for i in range(2*n+1)]
        assert same_ideal(power, intersection([t**n], primary, (t, f)), (t, f))
        G = s.groebner(power, t, f, domain=s.QQ)
        assert G.reduce(t**(2*n))[1] == 0
        assert G.reduce(t**(2*n-1))[1] != 0
        assert G.reduce(t**n)[1] != 0
        assert G.reduce(f**(2*n))[1] != 0
        # The monomial colon by t^n is exactly (t,f)^n.
        colon = [s.cancel(g/t**n) for g in power]
        expected = [t**i*f**(n-i) for i in range(n+1)]
        assert same_ideal(colon, expected, (t, f))
        length = sum(1 for i in range(n) for j in range(n) if i+j<n)
        assert length == n*(n+1)//2
        records.append({'n': n, 'intersection': True, 'irredundancy_witnesses': True,
                        'nilradical_index': 2*n, 'embedded_torsion_length': length,
                        'annihilator_colon': True})
    return records


def explicit_relation_system(e):
    x = s.symbols('x0:'+str(e))
    cross = [x[i]*x[j] for i in range(e) for j in range(i+1, e)]
    if e == 4:
        C = s.Matrix([[2,-1,2,0],[-2,0,-1,1],[2,-1,-2,0],
                      [1,-1,2,1],[1,-1,0,0],[1,-2,1,-2]])
    elif e == 3:
        C = s.Matrix([[0,0,-2],[0,-2,0],[-2,0,0]])
    else:
        raise ValueError('The regression class is e=3 or e=4.')
    Q = [s.expand(x[i]**2+sum(C[j,i]*cross[j] for j in range(len(cross)))) for i in range(e)]
    return x, cross, C, Q


def check_relations(e):
    x, cross, C, Q = explicit_relation_system(e)
    p = len(cross)
    monomials = [v*v for v in x] + cross
    relation = s.eye(e).col_join(C)
    gamma = (-C).row_join(s.eye(p))
    assert gamma*relation == s.zeros(p, e)
    assert gamma.rank() == p
    a = s.symbols('a0:'+str(e-1))
    alpha = dict(zip(x, (*a, s.Integer(1))))
    contraction = s.Matrix(monomials).jacobian(x).T.subs(alpha)
    hyperplane = [x[i]-a[i]*x[-1] for i in range(e-1)]
    products = [u*u for u in hyperplane] + [hyperplane[i]*hyperplane[j]
                 for i in range(e-1) for j in range(i+1, e-1)]
    W = s.Matrix([[s.Poly(q, *x).coeff_monomial(v) for q in products] for v in monomials])
    assert s.simplify(contraction*W) == s.zeros(e, p)
    restriction = gamma*W
    A_det = s.expand(restriction.det(method='domain-ge'))
    J = s.Matrix(Q).jacobian(x)
    J_det = s.expand(J.det(method='domain-ge'))
    C_det = s.expand((contraction*relation).det(method='domain-ge'))
    assert s.expand(C_det-J_det.subs(alpha)) == 0
    ratio = s.cancel(A_det/C_det)
    assert ratio.is_Rational and ratio != 0
    # This is an identity of polynomials, not just agreement of zero sets.
    assert s.expand(A_det-ratio*C_det) == 0
    assert s.Poly(J_det,*x).total_degree() == e
    assert s.simplify(J*s.Matrix(x) - s.Matrix([2*q for q in Q])) == s.zeros(e, 1)
    charts = []
    for k in range(e):
        variables = tuple(x[j] for j in range(e) if j != k)
        bp = s.groebner([q.subs(x[k], 1) for q in Q], *variables,
                        domain=s.QQ, order='grevlex')
        singular = s.groebner([s.diff(J_det, v).subs(x[k], 1) for v in x],
                              *variables, domain=s.QQ, order='grevlex')
        assert list(bp) == [1], ('base point', e, k)
        assert list(singular) == [1], ('singular ramification', e, k)
        charts.append({'chart': f'x{k}=1', 'basepoint_ideal_groebner_basis': ['1'],
                       'singular_ideal_groebner_basis': ['1'], 'field': 'QQ'})
    return {'e': e, 'p': p, 'hilbert_function': [1,e,p],
            'cross_term_matrix': [[int(v) for v in row] for row in C.tolist()], 'quadrics': [str(q) for q in Q],
            'jacobian_determinant': str(J_det), 'symbolic_determinant_ratio': str(ratio),
            'restriction_contraction_exact': True, 'euler_identity': True,
            'all_projective_charts': charts, 'orbit_dimension_deficit_lower_bound': e*p-e*e+1}


def run():
    return {'ordinary_primary_powers': check_powers(),
            'explicit_smooth_relation_systems': [check_relations(3), check_relations(4)],
            'general_proof_machine_certified': False,
            'primary_specialization_in_arbitrary_families_claimed': False}

if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2, default=str))
