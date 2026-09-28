#!/usr/bin/env python3
"""Exact finite diagnostics, not certificates for geometry or uniform risk."""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def zero(expr, message: str) -> None:
    require(sp.expand(expr) == 0 or sp.simplify(expr) == 0, message)


def main() -> None:
    u, v = sp.symbols('u v', real=True)
    r = sp.Rational(1, 4)
    def integral(g, x):
        return sp.integrate(sp.expand(g), (x, -r, r))
    def compress(g):
        M = sp.Matrix([[integral(g, v), integral(v*g, v)]])
        N = sp.Matrix([integral(g, u), integral(u*g, u)])
        H = sp.Matrix([[integral(integral(u**i*v**j*g, u), v)
                        for j in (0, 1)] for i in (0, 1)])
        return M, N, H
    # Algebra valid for arbitrary invertible 2-by-2 factors; no symmetry assumed.
    L = sp.Matrix(2, 2, sp.symbols('l:4'))
    C = sp.Matrix(2, 2, sp.symbols('c:4'))
    R = sp.Matrix(2, 2, sp.symbols('r:4'))
    H = L*C*R
    identity = C*R*H.adjugate()*L*C - H.det()*C
    for value in identity:
        zero(value, 'generic square moment factorization')
    cases = 0
    negative_controls = 0
    for j in range(1, 7):
        p = sp.Rational((-1)**j*(j+4), 4)
        d = sp.Rational(12+j, 3)
        a, c = sp.Rational(j, 12), sp.Rational(j+1, 14)
        w, z = 1+u/5+u*u/7, 1-v/6+v*v/9
        A, B = -p*u+a*u*u, p*v+c*v*v
        require(abs(p)-2*max(a,c)*r > abs(p)/2, 'slope sign margin')
        require(d-2*abs(p)*r-(a+c)*r*r > 0, 'positive residual')
        g = sp.expand(w*z*(d-A-B))
        Z = integral(integral(g,u),v)
        f = g/Z
        M, N, H = compress(f)
        require(H.det()>0, 'positive moment determinant')
        recovered = (M*H.inv()*N)[0]
        zero(recovered-f, 'exact density reconstruction')
        W, V = integral(w,u), integral(z,v)
        covA = integral(u*A*w,u)/W-integral(u*w,u)*integral(A*w,u)/W**2
        covB = integral(v*B*z,v)/V-integral(v*z,v)*integral(B*z,v)/V**2
        zero(H.det()+W**2*V**2*covA*covB/Z**2, 'covariance determinant')
        require(sp.expand((M*H.inv().T*N)[0]-f)!=0, 'transpose negative control')
        negative_controls += 1
        cases += 1
    # Exact rank-two compression must not be asserted for a finite-flight defect.
    e = sp.symbols('e', real=True)
    g = 3+u-v+e*u*u*v*v
    M,N,H = compress(g)
    defect = sp.factor((M*H.inv()*N)[0]-g)
    require(defect != 0, 'finite rank-defect negative control')
    zero(defect.subs(e,0), 'zero-defect limit')
    require(sp.limit(defect/e,e,0) not in (sp.oo,-sp.oo,sp.zoo,sp.nan), 'first-order defect')
    negative_controls += 1
    # The first-moment matrix can be singular for a normal-incidence law.
    _,_,H0 = compress(3-u*u-2*v*v)
    zero(H0.det(),'normal-incidence singular moment matrix')
    negative_controls += 1
    # Mixing a restricted-gate normalization with full-gate profiles is wrong.
    M,N,H = compress(3+u-v)
    Hsmall = sp.Matrix([[sp.integrate(sp.integrate(u**i*v**j*(3+u-v),
                          (u,-r/2,r/2)),(v,-r/2,r/2)) for j in (0,1)] for i in (0,1)])
    require(sp.expand((M*Hsmall.inv()*N)[0]-(3+u-v)) != 0, 'same-gate negative control')
    negative_controls += 1
    rate_cases = 0
    for m in (3,4,7,12):
        for s in (1,2,4):
            a1=sp.Rational(s,2*(m+s)+1); a2=sp.Rational(s,2*(m+s)+2)
            g1=sp.Rational(s,m+s+2); g2=sp.Rational(s,m+s+3)
            require(a2<a1<sp.Rational(1,2) and g2<g1<1,'strict rate improvement')
            zero(sp.Rational(1,2)-sp.Rational(2*m+1,2*(2*(m+s)+1))-a1,'variance balance')
            zero(1-sp.Rational(m+2,m+s+2)-g1,'readout balance')
            require(sp.Rational(m+2*s,2*(m+s)+1)>=a1,'envelope dominated')
            rate_cases += 1
    alpha, omega, Gamma = sp.symbols('alpha omega Gamma', positive=True)
    beta = alpha*omega/(omega+alpha*Gamma)
    zero(alpha-beta*alpha*Gamma/omega-beta,'rare-event budget balance')
    root=Path(__file__).resolve().parents[1]
    body=(root/'article/10i_moment_reconstruction_v74.tex').read_text()
    for label in ('lem:v74-skeleton','prop:v74-nondegeneracy','cor:v74-invariant',
                  'prop:v74-finite-stability','lem:v74-estimation','thm:v74-charged','cor:v74-budget'):
        require('\\label{'+label+'}' in body,'missing theorem route: '+label)
    print(json.dumps({'status':'passed','generic_matrix_entries':4,'exact_model_cases':cases,
                      'negative_controls':negative_controls,'rate_cases':rate_cases,
                      'optimization_safe':True,
                      'scope':'Finite algebra and source-route diagnostics only. Not a proof of billiard realization, flat-tail rigidity, uniform concentration, minimax optimality, or editorial acceptance.'},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
