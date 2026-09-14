#!/usr/bin/env python3
"""Independent finite diagnostics for the referee review of theta-theory A2 v48.

Run with Python 3 and SymPy: python independent_checks.py > INDEPENDENT_CHECKS.json
Also run with python -O and compare outputs. No network or repository writes.
These controls check identities and stated negative controls, not theorems,
relative billiard laws, analytic continuation, or an entire manuscript.
Explicit exceptions, not assert statements, enforce all checks under -O.
"""
from __future__ import annotations

import json
from fractions import Fraction as Q
from typing import Any

import sympy as s


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def zero(expression: Any, message: str) -> None:
    require(s.simplify(expression) == 0, message)


def matrix_zero(matrix: s.Matrix, message: str) -> None:
    for entry in matrix:
        zero(entry, message)


def check_density_inverse() -> dict[str, Any]:
    t = s.symbols('t', real=True)
    d = s.Integer(5)
    def action(u: Any) -> Any:
        return (1+t/7)*u**2/2 + (s.Rational(1,40)+t/13)*u**3 + (s.Rational(1,50)+t/29)*u**4
    def amplitude(u: Any) -> Any:
        return 2+t/7+(1+t/11)*u+u**2/3
    # An arbitrary positive scalar Z is enough for this algebraic cancellation.
    # It is deliberately not asserted to be the physical normalizing integral.
    def density(u: Any, v: Any) -> Any:
        return amplitude(u)*amplitude(v)*(d-action(u)-action(v))/(3+t+t*t)
    def ratio(u: Any, v: Any) -> Any:
        return s.cancel(density(u,v)*density(0,0)/(density(u,0)*density(0,v)))
    def dot(expr: Any) -> Any:
        return s.diff(expr,t).subs(t,0)
    u,v,a = s.Rational(1,5), -s.Rational(1,7), s.Rational(1,4)
    tu = action(u)/(d-action(u))
    tv = action(v)/(d-action(v))
    ta = action(a)/(d-action(a))
    zero(1-ratio(u,v)-tu*tv, 'Four-density factorization')
    log_derivative = ratio(u,v).subs(t,0)*(
        dot(density(u,v))/density(u,v).subs(t,0)
        +dot(density(0,0))/density(0,0).subs(t,0)
        -dot(density(u,0))/density(u,0).subs(t,0)
        -dot(density(0,v))/density(0,v).subs(t,0))
    zero(dot(ratio(u,v))-log_derivative, 'Four-density logarithmic derivative')
    q0 = ta.subs(t,0)
    require(bool(q0>0), 'Positive anchor')
    recovered_dot_t = -dot(ratio(u,a))/q0 + tu.subs(t,0)*dot(ratio(a,a))/(2*q0*q0)
    zero(recovered_dot_t-dot(tu), 'Anchor derivative sign and normalization')
    zero(d*recovered_dot_t/(1+tu.subs(t,0))**2-dot(action(u)), 'Action derivative')
    wrong_sign = -dot(ratio(u,a))/q0-tu.subs(t,0)*dot(ratio(a,a))/(2*q0*q0)
    require(s.simplify(wrong_sign-dot(tu)) != 0, 'Wrong anchor sign must fail')
    require(s.simplify(action(u)-action(-u)) != 0, 'Odd signed term must remain')
    return {'status':'pass','scope':'Exact rational functional identity at signed test points, with varying amplitude and scalar normalization; not a billiard realization.',
            'anchor_positive':True,'wrong_anchor_sign_detected':True,'nonzero_odd_action_term_retained':True}


def check_moving_normalizer() -> dict[str, Any]:
    t,x = s.symbols('t x', real=True)
    d=s.Integer(3); a=2+t/3; w=3+t/5
    # x=r^2, so planar integration contributes pi dx.
    Z=s.integrate(s.pi*w*(d-a*x/2),(x,0,2*d/a))
    zero(Z-s.pi*d*d*w/a, 'Exact radial-cap normalizer')
    a0,w0=a.subs(t,0),w.subs(t,0)
    predicted=s.integrate(s.pi*(s.diff(w,t).subs(t,0)*(d-a0*x/2)-w0*s.diff(a,t).subs(t,0)*x/2),(x,0,2*d/a0))
    zero(s.diff(Z,t).subs(t,0)-predicted,'Moving-support first derivative')
    density=w*(d-a*x/2)/Z
    predicted_density=s.diff(a*(d-a*x/2)/(s.pi*d*d),t).subs(t,0)
    zero(s.diff(density,t).subs(t,0)-predicted_density,'Normalized interior derivative')
    wrong=s.diff(w*(d-a*x/2),t).subs(t,0)/Z.subs(t,0)
    require(s.simplify((wrong-predicted_density).subs(x,s.Rational(1,8))) != 0,'Omitting normalizer derivative must fail')
    return {'status':'pass','normalizer':'pi*d^2*w/a','derivative_rule':'Integral of dot(w)*(d-A)_+ - w*dot(A)*1_{A<d}',
            'omitted_normalizer_detected':True,'scope':'Radial-cap functional control, not an independently realized billiard density.'}


def check_contact_blocks() -> dict[str, Any]:
    z=Q(1,3); r0=Q(3,2); r1=Q(2,3); g=Q(3,2)
    cosh=(z+1/z)/2; sinh=(1/z-z)/2
    c0,c1=cosh*r0,cosh*r1
    k0,k1=(c0-1)/g,(c1-1)/g
    require(k0>0 and k1>0 and k0!=k1,'Positive unequal contact curvatures')
    a0,a1=sinh*r0/g,sinh*r1/g
    require(g*g*a0*a1==sinh*sinh,'Leading recovery identity')
    determinants=[]
    for n in range(3,17):
        # Endpoint visits: one initial visit, then paired even-index visits;
        # opposite endpoint: paired odd-index visits. Sum the geometric tails.
        diag=1+2*z**(2*n)/(1-z**(2*n))
        off0=2*r0**n*z**n/(1-z**(2*n))
        off1=2*r1**n*z**n/(1-z**(2*n))
        determinant=diag*diag-off0*off1
        require(determinant==1,f'Contact block determinant at order {n}')
        determinants.append(str(determinant))
    return {'status':'pass','orders':list(range(3,17)),'determinants':determinants,
            'gap':str(g),'curvatures':[str(k0),str(k1)],
            'scope':'Exact geometric-series blocks and leading coefficients; not a replacement for smooth finite-remainder factorization.'}


def check_registration() -> dict[str, Any]:
    alpha=s.symbols('alpha', real=True)
    indices=[6,10,15]; bezout=[1,1,-1]
    require(sum(k*a for k,a in zip(indices,bezout))==1,'Three-harmonic Bezout witness')
    U=s.prod(s.exp(-s.I*k*alpha)**(-a) for k,a in zip(indices,bezout))
    zero(U-s.exp(s.I*alpha),'Proper rotation formula')
    zero(s.diff(U,alpha)-s.I*s.exp(s.I*alpha),'Rotation differential')
    import math
    require(all(math.gcd(indices[i],indices[j])>1 for i in range(3) for j in range(i+1,3)), 'Control must not rely on a gcd-one pair')
    margin=Q(1,10)-Q(1,100000)*sum(k*k-1 for k in indices)
    require(margin>0,'Positive curvature for harmonic support control')
    k=s.Integer(2); ratio=s.exp(-s.I*k*alpha)
    zero(s.diff(ratio,alpha)/ratio+s.I*k,'One harmonic detects infinitesimal rotation')
    return {'status':'pass','indices':indices,'bezout':bezout,'no_coprime_pair':True,
            'support_curvature_lower_bound':str(margin),'single_harmonic_local_rotation_derivative':'dot(r_k)/r_k=-i*k*dot(alpha)',
            'scope':'Registration of congruent analytic support images; global uniqueness requires gcd one, whereas local rotational velocity needs one nonzero harmonic.'}


def check_lattice_cochain() -> dict[str, Any]:
    t=s.symbols('t', real=True)
    L=s.Matrix([[2+t/7,s.Rational(1,5)+t/11],[s.Rational(1,3)-t/13,3+t/17]])
    c=[s.zeros(2,1),s.Matrix([s.Rational(1,4)+t/19,s.Rational(1,6)]),s.Matrix([s.Rational(2,5),s.Rational(3,7)-t/23])]
    m=[s.zeros(2,1),s.Matrix([1,-1]),s.Matrix([0,1])]
    p=[c[i]+L*m[i] for i in range(3)]
    gains=[s.Matrix([2,0]),s.Matrix([1,3])]
    endpoints=[(1,2),(2,0)]
    translations=[]
    for (a,b),eta in zip(endpoints,gains):
        ell=eta-m[a]+m[b]
        d=c[b]+L*ell-c[a]
        translations.append(s.simplify(p[a]+d-p[b]))
    M=s.Matrix.hstack(*gains); V=s.Matrix.hstack(*translations)
    recovered=V*M.inv()
    matrix_zero(recovered-L,'Unknown lattice cochain inverse')
    matrix_zero(s.diff(recovered,t)-s.diff(L,t),'Lattice differential')
    for i in range(3): matrix_zero(p[i]-recovered*m[i]-c[i],'Representative placement')
    require(M.det()==6,'Non-unimodular control')
    require(V.subs(t,0)!=L.subs(t,0),'Dropping the gain inverse must fail')
    return {'status':'pass','gain_matrix':[[2,1],[0,3]],'gain_determinant':6,'omitting_gain_inverse_detected':True,
            'scope':'Synthetic marked displacement cochain with moving lattice and centers, not a certified selected-channel realization.'}


def check_circular_lattice_control() -> dict[str, Any]:
    t=s.symbols('t', real=True)
    L=s.Matrix([[1,-s.sin(t)],[0,s.cos(t)]])
    for column in range(2): zero((L[:,column].T*L[:,column])[0]-1,'Selected disk-center distance')
    dotL=s.diff(L,t).subs(t,0); dotGram=s.diff(L.T*L,t).subs(t,0)
    require(dotGram!=s.zeros(2),'Nontrivial lattice-angle variation')
    J=s.Matrix([[0,-1],[1,0]])
    require(dotL[:,0]==s.zeros(2,1) and dotL!=s.zeros(2),'Not a common rotational velocity')
    require(dotL!=J and dotL!=-J,'Additional rotation negative controls')
    radius=Q(1,10)
    # For |t| <= 1/10, ||L-I||_2 <= 2*sin(|t|/2) <= 1/10.
    # Thus any nonzero lattice displacement has length >= 9/10.
    separation_margin=Q(9,10)-2*radius
    # At t=0 other lattice centers are at distance >=1 from [0,e_i].
    # If a center is within 1/2 of the moving segment, its norm is <3/2,
    # hence its integer mark has norm <5/3 and is one of eight neighbors.
    # For those neighbors, perturbation reduces segment distance by at most
    # (sqrt(2)+1)/10 < 1/4. It therefore remains >3/4, a contradiction.
    require(separation_margin>0,'Disk separation')
    return {'status':'pass','radius':str(radius),'selected_gaps':[str(1-2*radius)]*2,
            'lattice':'[[1,-sin(t)],[0,cos(t)]]','parameter_window':'|t| < 1/10',
            'dot_lattice_at_zero':[[int(x) for x in dotL.row(i)] for i in range(2)],
            'dot_gram_at_zero':[[int(x) for x in dotGram.row(i)] for i in range(2)],
            'observation_reason':'Each selected pair of identical disks is congruent in its own intrinsic channel frame; the selected gaps and both same-type laws are unchanged.',
            'scope':'A circular-table control outside the asymmetric hypotheses, not a counterexample to Theorem A or Theorem 20.5. The geometric clearance argument is in the report.'}


def main() -> None:
    result={'reviewed_source_commit':'fe21046e47a89ec3b3df8493f4d885b087e3ad7f',
            'status':'pass','kind':'Independent finite identities and explicitly scoped negative controls; no theorem-certification claim.',
            'checks':{'density_inverse_differential':check_density_inverse(),
                      'moving_support_normalizer':check_moving_normalizer(),
                      'finite_contact_blocks':check_contact_blocks(),
                      'harmonic_registration':check_registration(),
                      'marked_lattice_cochain':check_lattice_cochain(),
                      'circular_lattice_ambiguity_outside_hypotheses':check_circular_lattice_control()}}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
