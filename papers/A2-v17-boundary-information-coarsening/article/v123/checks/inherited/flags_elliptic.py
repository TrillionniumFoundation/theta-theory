"""Exact finite regression checks; not a substitute for the general proofs."""
from __future__ import annotations
import sympy as s

def intersection(I, J, variables):
    u = s.Dummy('intersection_parameter')
    G = s.groebner([u*f for f in I] + [(1-u)*g for g in J], u, *variables, order='lex')
    return [g.as_expr() for g in G.polys if not g.as_expr().has(u)]

def same_ideal(I, J, variables):
    a = s.groebner(I, *variables, order='grevlex')
    b = s.groebner(J, *variables, order='grevlex')
    return all(a.reduce(f)[1] == 0 for f in J) and all(b.reduce(f)[1] == 0 for f in I)

def run():
    a,b,c,d,t,lam,k = s.symbols('a b c d t lam k')
    det = a*d-b*c
    v=(a,b,c,d,t)
    F=[t*det,t*t*a,t*t*b,t*t*c,t*t*d,t**3]
    # P_1 is the maximal ideal; P_2=(t,det) is prime complete intersection.
    mon=s.polys.monomials.itermonomials(v,3)
    P1=[m for m in mon if s.total_degree(m)==3]
    P2=[t*t,t*det,det**2]
    dec=intersection(intersection([t],P1,v),P2,v)
    assert same_ideal(F,dec,v)
    A=s.Matrix([[c*c,-lam*a*c,-2*lam*b*c],[-2*lam*a*c,-lam*b*c,c*c],[a*a,a*b+lam*c*c,b*b]])
    cubic=lam*(a**3+b**3+c**3)+(1-4*lam**3)*a*b*c
    assert s.expand(A.det()+c**3*cubic)==0
    wa=12*(-k/2)*(1-(-k/2)**3)
    wb=2*(1-20*(-k/2)**3-8*(-k/2)**6)
    j=27*k**3*(k**3+8)**3/(k**3-1)**3
    assert s.cancel(1728*4*wa**3/(4*wa**3+27*wb**2)-j)==0
    kl=(4*lam**3-1)/(3*lam)
    assert s.cancel(s.diff(j.subs(k,kl),lam))!=0
    assert ((4*lam**3-1)**3-27*lam**3).subs(lam,s.Rational(1,2))!=0
    f=s.symbols('f')
    assert same_ideal(intersection([t],[t*t,t*f,f*f],(t,f)),[t*t,t*f],(t,f))
    return {'weighted_q2_p2_full_intersection':True,
            'elliptic_restriction_determinant':True,
            'hesse_j_normalization':True,'j_nonconstant':True,
            'parameter_open_nonempty':True,'elliptic_local_primary':True,
            'general_proof_machine_certified':False}
