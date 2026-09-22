"""Exact finite checks of the v120 identities; the proofs are in the TeX."""
from __future__ import annotations
from itertools import combinations, product
import sympy as sp

a,b,c,d,lam,tau = sp.symbols('a b c d lam tau')
xs = (a,b,c,d)
delta = a*d-b*c
P, Q = [a,c], [b,d]

def power_ideal(gens, degree):
    return sorted({sp.expand(sp.prod(f**u for f,u in zip(gens,e)))
                   for e in product(range(degree+1), repeat=len(gens))
                   if sum(e)==degree}, key=str)

def basis(gens):
    return sp.groebner(gens,*xs,order='grevlex')

def same_ideal(left,right):
    gl,gr=basis(left),basis(right)
    return (all(gr.reduce(p.as_expr())[1]==0 for p in gl.polys)
            and all(gl.reduce(p.as_expr())[1]==0 for p in gr.polys))

def intersection(left,right):
    g=sp.groebner([lam*p for p in left]+[(1-lam)*p for p in right],
                  lam,*xs,order='lex')
    return [p.as_expr() for p in g.polys if not p.as_expr().has(lam)]

def run():
    rows=[]
    h11,h12,h21,h22=sp.symbols('h11 h12 h21 h22')
    for square in (True,False):
        matrix=sp.Matrix([
            [a,c,0,0,0], [b,d,0,0,0],
            [h11,h12,a*a,2*a*c,c*c],
            [h21,h22,a*b if square else b*b,
             a*d+b*c if square else 2*b*d,c*d if square else d*d]])
        minors=[sp.factor(matrix[:,cols].det()) for cols in combinations(range(5),4)]
        residual=power_ideal(P,2) if square else [a*b,a*d+b*c,c*d]
        ideal=[delta**2*f for f in residual]
        assert same_ideal(minors,ideal), 'whole multiplication presentation'
        gi=basis(ideal)
        assert gi.reduce(delta**4)[1]==0 and gi.reduce(delta**3)[1]!=0
        if square:
            for j in range(1,4):
                assert same_ideal([delta**(2*j)*p for p in power_ideal(P,2*j)],
                                  intersection([delta**(2*j)],power_ideal(P,4*j)))
            primary_count=2
        else:
            q0=residual+power_ideal(P,2)+power_ideal(Q,2)
            assert same_ideal(residual,intersection(intersection(P,Q),q0))
            gj,g0=basis(residual),basis(q0)
            assert all(gj.reduce(x*delta)[1]==0 for x in xs)
            assert gj.reduce(delta)[1]!=0
            assert all(g0.reduce(p)[1]==0 for p in power_ideal(list(xs),3))
            assert g0.reduce(delta)[1]!=0
            standard=[]
            lex=sp.groebner(q0,*xs,order='lex')
            leading=[p.LM(order=lex.order).exponents for p in lex.polys]
            for e in product(range(3),repeat=4):
                if not any(all(i>=j for i,j in zip(e,lm)) for lm in leading):
                    standard.append(e)
            assert len(standard)==6
            qm=[delta**2*f for f in q0]+power_ideal(list(xs),7)
            whole=intersection(intersection(intersection([delta**2],power_ideal(P,3)),
                                            power_ideal(Q,3)),qm)
            assert same_ideal(ideal,whole), 'four-component full primary identity'
            primary_count=4
        rows.append({'type':'square' if square else 'two_factor',
                     'full_matrix_shape':list(matrix.shape),
                     'all_maximal_minors_with_free_higher_coefficients':True,
                     'primary_identity_verified':True,
                     'displayed_primary_components':primary_count,
                     'nilradical_index_verified':4})
    moving=sp.Matrix([[a*a,a*c,c*c],
                      [2*a*b+tau*b*b,a*d+b*c+tau*b*d,2*c*d+tau*d*d]])
    expected=[a*(a+tau*b),2*a*c+tau*(a*d+b*c),c*(c+tau*d)]
    actual=[moving[:,cols].det() for cols in combinations(range(3),2)]
    assert all(sp.expand(x-delta*y)==0 for x,y in zip(actual,expected))
    # Enumerate product spans for the connected sharpness family. The basis
    # multiplication is z^i z^j=z^(i+j) until truncation, with all positive
    # degree products involving an epsilon equal to zero.
    sharp=[]
    for r in range(1,9):
        for k in range(2,7):
            d0=r+k
            eps=set(range(r+2,d0))
            initial={0,1}|eps
            current=set(initial)
            ranks=[]
            for degree in range(1,r+2):
                if degree>1:
                    nxt=set()
                    for i,j in product(current,initial):
                        if i==0: nxt.add(j)
                        elif j==0: nxt.add(i)
                        elif i in eps or j in eps: continue
                        elif i+j<r+2: nxt.add(i+j)
                    current=nxt
                ranks.append(len(current))
            assert ranks==[k+j-1 for j in range(1,r+2)]
            assert ranks[-2]==d0-1 and ranks[-1]==d0
            sharp.append({'r':r,'k':k,'ranks':ranks})
    return {'kind':'exact finite regression, not theorem certification',
            'primary':rows,'square_power_range':[1,3],
            'quadratic_factor_collision_identity':True,
            'sharpness_examples':sharp,
            'proof_certification':False}
