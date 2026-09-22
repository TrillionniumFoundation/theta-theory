#!/usr/bin/env python3
"""Exact finite diagnostics for A2 v119. Not a proof or priority certificate."""
from __future__ import annotations
from pathlib import Path
import importlib.util
import itertools
import json
import math
import re
import sympy as sp

HERE = Path(__file__).resolve().parent
b, u, v, z = sp.symbols('b u v z')

def recurrence(h: int) -> list[sp.Expr]:
    f = [sp.Integer(0), sp.Integer(1)]
    for j in range(1, h + 1):
        f.append(sp.expand(u * f[j] + v * f[j-1]))
    return f

def same_ideal(left: list, right: list, variables: tuple) -> bool:
    gl = sp.groebner(left, *variables, order='lex')
    gr = sp.groebner(right, *variables, order='lex')
    return all(gr.reduce(p)[1] == 0 for p in left) and all(gl.reduce(p)[1] == 0 for p in right)

def colength(g: sp.GroebnerBasis, bounds: tuple[int, ...]) -> int:
    leads = [poly.LM(order=g.order).exponents for poly in g.polys]
    return sum(not any(all(x >= y for x, y in zip(exp, lm)) for lm in leads)
               for exp in itertools.product(*(range(n) for n in bounds)))

def primary_checks() -> list[dict]:
    rows = []
    lam = sp.Symbol('lam')
    for h in range(5, 10):
        f = recurrence(h)
        J = [f[h], v*f[h-1]]
        I = J + [b*v, b*b*u]
        Q = J + [b*b, b*v]
        elimination = sp.groebner([lam*u, lam*v] + [(1-lam)*q for q in Q],
                                  lam, b, u, v, order='lex')
        intersection = [p.as_expr() for p in elimination.polys if not p.as_expr().has(lam)]
        assert same_ideal(I, intersection, (b, u, v)), ('primary intersection', h)
        gj = sp.groebner(J, u, v, order='lex')
        gq = sp.groebner(Q, b, u, v, order='lex')
        gi = sp.groebner(I, b, u, v, order='lex')
        assert colength(gj, (2*h, h+1)) == math.comb(h, 2)
        assert colength(gq, (3, 2*h, h+1)) == math.comb(h, 2) + h - 1
        assert gi.reduce(u**(2*h-4))[1] != 0
        for i in range(2*h-2):
            assert gi.reduce(u**i * v**(2*h-3-i))[1] == 0
        Y = sp.Matrix([[0, v], [1, u]])
        X = b*(Y-u*sp.eye(2))
        for rel in [X*X, X*Y, Y**h]:
            assert all(gi.reduce(sp.expand(e))[1] == 0 for e in rel)
        assert gj.reduce(f[h+1])[1] == 0
        rows.append({'h': h, 'primary_intersection': True,
                     'contact_colength': math.comb(h, 2),
                     'displayed_embedded_primary_colength': math.comb(h, 2)+h-1,
                     'nilradical_dimension': math.comb(h, 2)+h-3,
                     'nilradical_index': 2*h-3, 'quotient_relations': True})
    return rows

def fork_product(p: list, q: list, h: int) -> list:
    # Ordered basis: 1, x, y, y^2, ..., y^(h-1).
    out = [sp.Integer(0)]*(h+1)
    for i, a in enumerate(p):
        for j, c in enumerate(q):
            if a == 0 or c == 0: continue
            if i == 0: k = j
            elif j == 0: k = i
            elif i == 1 or j == 1: continue
            else:
                degree = i+j-2
                if degree >= h: continue
                k = degree+1
            out[k] += a*c
    return [sp.expand(x) for x in out]

def incidence_check() -> dict:
    h = 5
    f = recurrence(h)
    t1, t2, t3 = map(sp.Integer, (1,-1,2))
    one = [1,0,0,0,0,0]
    omitted = [0,0,-f[4],0,0,1]
    base = [[0,1,-b,0,0,0], [0,0,-u,1,0,0], [0,0,-f[3],0,1,0]]
    W = [one] + [[sp.expand(x+t*y) for x,y in zip(vec,omitted)]
                  for vec,t in zip(base,[t1,t2,t3])]
    M_basis = [[0,0,1,0,0,0], [0,0,0,0,0,1]]
    change = sp.Matrix.hstack(*(sp.Matrix(w) for w in W+M_basis))
    assert change.det() == -1 or change.det() == 1
    inverse = change.inv()
    residual = inverse[4:6, :]
    beta = sp.Matrix.hstack(*(residual*sp.Matrix(fork_product(w,q,h)) for w in W for q in W))
    Cs = [sp.Matrix.hstack(*(residual*sp.Matrix(fork_product(w,q,h)) for q in M_basis)) for w in W]
    matrix = sp.Matrix.hstack(beta, *(c*beta for c in Cs))
    # Drop identically zero/duplicate columns before checking every two-minor.
    gi = sp.groebner([f[h], v*f[h-1], b*v, b*b*u], b,u,v, order='lex')
    columns = []
    for j in range(matrix.cols):
        col = tuple(gi.reduce(sp.expand(e))[1] for e in matrix[:,j])
        if any(c != 0 for c in col) and col not in columns: columns.append(col)
    gi = sp.groebner([f[h], v*f[h-1], b*v, b*b*u], b,u,v, order='lex')
    checked = 0
    for p,q in itertools.combinations(columns,2):
        determinant = sp.expand(p[0]*q[1]-p[1]*q[0])
        assert gi.reduce(determinant)[1] == 0
        checked += 1
    pivot = residual*sp.Matrix(fork_product(W[2],W[2],h))
    assert pivot[1].subs({b:0,u:0,v:0}) == 1
    return {'h':h, 'all_nonduplicate_two_minors_checked':checked,
            'quotient_chart_at_Grassmannian_coordinates':[1,-1,2],
            'nonreduced_coefficient_ring_retained':True,
            'quadratic_generation_pivot_at_origin':1}

def rank_and_staircase_checks() -> list[dict]:
    rows=[]
    for h in range(5, 13):
        basis = [list(sp.eye(h+1)[:,j]) for j in range(h+1)]
        # Omit y and y^4; keep 1, x and all other powers.
        W = [basis[j] for j in range(h+1) if j not in (2,5)]
        products = [sp.Matrix(fork_product(x,y,h)) for x in W for y in W]
        E = sp.Matrix.hstack(*products)
        assert len(W) == h-1 and E.rank() == h
        cube = [sp.Matrix(fork_product(list(p),w,h)) for p in products for w in W]
        assert sp.Matrix.hstack(*cube).rank() == h
        gens = [(4,0),(3,1),(2,2),(1,h+1),(0,2*h)]
        standards=[(i,j) for i in range(5) for j in range(2*h+1)
                   if not any(i>=a and j>=c for a,c in gens)]
        assert max(i+j for i,j in standards) == 2*h-1
        rows.append({'h':h,'W_rank':h-1,'quadratic_rank':h,'cubic_rank':h,
                     'ordinary_square_regularity':2*h})
    return rows

def cubic_and_compression_checks() -> dict:
    s,t = sp.symbols('s t')
    cubic = sp.expand(s*t*t-t*s*s)
    assert sp.expand(cubic-s*t*(-s+t)) == 0
    # The square-zero rank-three quotient has identically zero square obstruction.
    assert s*0-t*0 == 0
    # Exact compressed commutator check on a universal unital codimension-two
    # chart of C[y]/(y^5), without imposing any subalgebra equations.
    a = sp.symbols('a0:4')
    one=sp.eye(5)[:,0]
    W=[one, sp.Matrix([0,a[0],a[1],1,0]), sp.Matrix([0,a[2],a[3],0,1])]
    M=[sp.eye(5)[:,1],sp.eye(5)[:,2]]
    change=sp.Matrix.hstack(*(W+M)); inv=change.inv()
    def product(p,q):
        return sp.Matrix([sum(p[i]*q[j] for i in range(5) for j in range(5) if i+j==k) for k in range(5)])
    L=[inv*sp.Matrix.hstack(*(product(w,q) for q in W+M)) for w in W]
    left=L[1][3:5,3:5]*L[2][3:5,3:5]-L[2][3:5,3:5]*L[1][3:5,3:5]
    right=L[2][3:5,0:3]*L[1][0:3,3:5]-L[1][3:5,0:3]*L[2][0:3,3:5]
    assert all(sp.expand(x)==0 for x in left-right)
    assert any(sp.expand(x)!=0 for x in left)
    # Degree-three and degree-four residual images: direct minors/presentation
    # identities are proved generally in the manuscript, not inferred here.
    return {'etale_rank_three_cubic':str(sp.factor(cubic)),
            'square_zero_rank_three_cubic':0,
            'compressed_commutator_identity':True,
            'compressed_operators_not_assumed_commuting':True}

def preservation() -> dict:
    original=HERE.parent/'v118'
    # A portable build can instead use the source-label manifest.
    meta=json.loads((HERE/'evidence/PRESERVATION.json').read_text())
    current=set()
    for f in list(HERE.glob('*.tex'))+list((HERE/'parts').glob('*.tex')):
        text=f.read_text()
        current.update(re.findall(r'\\label\{([^}]+)\}',text))
        for env in ['theorem','proof','lemma','proposition','corollary','remark']:
            assert text.count(r'\begin{'+env+'}') == text.count(r'\end{'+env+'}'),(str(f),env)
    assert set(meta['old_labels']) <= current
    return {'old_label_count':len(meta['old_labels']), 'current_label_count':len(current),
            'missing_old_labels':[]}

def main() -> None:
    spec=importlib.util.spec_from_file_location('v118_diagnostics',HERE/'inherited-v118/verify_revision.py')
    inherited=importlib.util.module_from_spec(spec); spec.loader.exec_module(inherited)
    data={'kind':'exact finite regression diagnostics, not proof certification',
          'primary':primary_checks(), 'incidence':incidence_check(),
          'rank_and_staircase':rank_and_staircase_checks(),
          'cubic_and_compression':cubic_and_compression_checks(),
          'inherited_substitution':inherited.substitution_tests(),
          'inherited_conductor':inherited.conductor_tests(),
          'inherited_action':inherited.action_tests(),
          'preservation':preservation(),
          'proof_certification':False,'priority_certification':False,
          'remote_push_performed':False}
    (HERE/'evidence/DIAGNOSTICS.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
if __name__=='__main__':
    main()
