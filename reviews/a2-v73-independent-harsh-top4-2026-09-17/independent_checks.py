#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v73 referee report.

Run: python independent_checks.py > MATHEMATICAL_CHECKS.json
Dependencies: Python 3.10+, SymPy, mpmath. No repository modules or network.
These checks do NOT certify the nonlinear billiard or statistical theorems.
Polynomial test actions are not asserted to be realizable billiard actions.
All checks remain active with python -O.
"""
from __future__ import annotations
import itertools
import json
import platform
import mpmath as mp
import sympy as sp


def require(condition: object, message: str) -> None:
    if not bool(condition):
        raise RuntimeError(message)


def zero(expr: sp.Expr, message: str) -> None:
    require(sp.cancel(expr) == 0, message)


def anchor_checks() -> dict[str, int]:
    u, v = sp.symbols('u v', real=True)
    eta = sp.Rational(1, 9)
    amplitude = (1 + u/5)*(1 - v/7)*(1 + eta*u*v)
    integrated = sp.integrate(sp.integrate(amplitude, (u, 0, u)), (v, 0, v))
    counts = dict(anchor_cases=0, gate_negative_controls=0,
                  thinning_negative_controls=0, finite_clock_cases=0)
    for D, d, area, R in itertools.product(
        [sp.Rational(1, 5), sp.Rational(1, 11)],
        [sp.Integer(2), sp.Integer(3)], [sp.Integer(3), sp.Integer(7)],
        [sp.Rational(1, 4), sp.Rational(1, 3)]):
        p = sp.Rational(1, 3) * (-1 if d == 3 else 1)
        E = u*u/10 + v*v/7 - D*integrated
        zero(-sp.diff(E, u, v)/D-amplitude, 'twist/action consistency')
        residual = d-E+p*u-p*v
        upper_amp = (1+R/5)*(1+R/7)*(1+eta*R*R)
        require(d-2*abs(p)*R-(sp.Rational(1,10)+sp.Rational(1,7))*R*R
                -D*upper_amp*R*R > 0, 'positive residual on whole square')
        require((1-R/5)*(1-R/7)*(1-eta*R*R)>0, 'positive amplitude')
        raw = sp.expand(amplitude*residual)
        Z = sp.integrate(raw, (u,-R,R),(v,-R,R))
        Zsmall = sp.integrate(raw, (u,-R/2,R/2),(v,-R/2,R/2))
        pi = D*Z/(2*sp.pi*area)
        require(0 < float(pi) < 1, 'valid success probability')
        f0 = d/Z
        zero(pi*f0-D*d/(2*sp.pi*area), 'central anchor')
        zero(D*d/(2*sp.pi*pi*f0)-area, 'area recovery')
        counts['anchor_cases'] += 1
        wrong_area = sp.cancel(D*d/(2*sp.pi*pi*(d/Zsmall)))
        zero(wrong_area-area*Zsmall/Z, 'wrong-gate error factor')
        require(0 < Zsmall < Z and wrong_area != area, 'wrong gate must fail')
        counts['gate_negative_controls'] += 1
        efficiency = sp.Rational(9,10)
        apparent_area = area/efficiency
        zero(efficiency*D/(2*sp.pi*area)-D/(2*sp.pi*apparent_area),
             'unknown efficiency/area confounding')
        zero(D*d/(2*sp.pi*(efficiency*pi)*f0)-apparent_area, 'thinned area')
        require(apparent_area != area, 'efficiency must matter')
        counts['thinning_negative_controls'] += 1
        raw0 = raw.subs({u:0,v:0})
        clock = (sp.diff(raw,u,v).subs({u:0,v:0})/raw0
                 -sp.diff(raw,u).subs({u:0,v:0})*
                  sp.diff(raw,v).subs({u:0,v:0})/raw0**2)
        zero(clock-(p*p/d**2+D/d+eta), 'finite clock correction')
        counts['finite_clock_cases'] += 1
    return counts


def transfer_checks() -> dict[str, int]:
    cases = direct = 0
    for r in [2,3,4]:
        c = [sp.Rational(i+2, i+3) for i in range(r)]
        k = [sp.Rational(i+3, i+2) for i in range(r)]
        P = 2*r
        for b in range(r):
            M = sp.eye(2)
            for j in range(P):
                i=(b+j)%r
                M=sp.Matrix([[1+2*c[i]/k[i],1/k[i]],[2*c[i],1]])*M
            require(M.det()==1 and sp.trace(M)>2, 'positive hyperbolic transfer')
            for n in [1,2,3]:
                N=n*P
                # Continuant of the (N-1)-site interior Jacobi Hessian.
                prev2, prev = sp.Integer(1), sp.Integer(1)
                for j in range(1,N):
                    i=(b+j)%r
                    diag=k[(i-1)%r]+k[i]+2*c[i]
                    det = diag*prev if j==1 else diag*prev-k[(i-1)%r]**2*prev2
                    prev2, prev = prev, sp.cancel(det)
                prod=sp.prod(k[(b+j)%r] for j in range(N))
                D=sp.cancel(prod/prev)
                power=M**n
                zero(D-1/power[0,1], 'cofactor/transfer identity')
                zero(power[0,1]-M[0,1]*sp.chebyshevu(n-1,sp.trace(M)/2),
                     'returning normalization identity')
                if N<=12:
                    H=sp.zeros(N-1)
                    for j in range(1,N):
                        i=(b+j)%r
                        H[j-1,j-1]=k[(i-1)%r]+k[i]+2*c[i]
                        if j<N-1:
                            H[j-1,j]=H[j,j-1]=-k[i]
                    zero(H.det(method='domain-ge')-prev, 'direct determinant')
                    direct+=1
                cases+=1
    return dict(periodic_transfer_cases=cases, direct_determinant_cases=direct)


def sensitivity_checks() -> dict[str, object]:
    mp.mp.dps=70
    cases=0
    for r in [2,3]:
        c=[mp.mpf(i+2)/(i+3) for i in range(r)]
        k=[mp.mpf(i+3)/(i+2) for i in range(r)]
        P=2*r
        for j in range(r):
            def M_at(t: mp.mpf) -> mp.matrix:
                M=mp.eye(2)
                for h in range(P):
                    i=h%r
                    ci=c[i]+(t if i==j else 0)
                    M=mp.matrix([[1+2*ci/k[i],1/k[i]],[2*ci,1]])*M
                return M
            def chi(t: mp.mpf) -> mp.mpf:
                M=M_at(t)
                return mp.acosh((M[0,0]+M[1,1])/2)
            x=chi(mp.mpf(0))
            dx=mp.diff(chi,0)
            db=mp.diff(lambda t: mp.log(M_at(t)[0,1]),0)
            for n in [1,2,5,20]:
                actual=mp.diff(lambda t: -mp.log((M_at(t)**n)[0,1]),0)
                formula=(mp.coth(x)-n*mp.coth(n*x))*dx-db
                require(abs(actual-formula)<mp.mpf('1e-55'), 'log twist derivative')
                cases+=1
    c0=mp.mpf('0.5'); P=6
    chi0=mp.acosh(1+c0); dx0=1/mp.sqrt(c0*(c0+2))
    previous=mp.inf; limits=[]
    for n in [10,100,1000]:
        # Homogeneous one-step Q, D_(nP)=sinh(chi0)/sinh(nP chi0), k=1.
        normalized=(mp.coth(chi0)-n*P*mp.coth(n*P*chi0))*dx0/n
        error=abs(normalized+P*dx0)
        require(error<previous/8, 'linear amplification limit')
        previous=error
        limits.append(dict(n=n, normalized_derivative=mp.nstr(normalized,18),
                           distance_to_limit=mp.nstr(error,12)))
    return dict(multiprecision_derivative_cases=cases,
                homogeneous_limit=-float(P*dx0), homogeneous_sequence=limits)


def rate_checks() -> dict[str, int]:
    alpha, omega, Gamma=sp.symbols('alpha omega Gamma', positive=True)
    beta=alpha*omega/(omega+alpha*Gamma)
    zero(alpha-beta*alpha*Gamma/omega-beta, 'rare-budget balance')
    m,s=sp.symbols('m s',positive=True)
    a=s/(2*(m+s)+2); g=s/(m+s+3)
    zero(sp.Rational(1,2)-(m+1)/(2*(m+s)+2)-a, 'variance balance')
    zero(1-(m+3)/(m+s+3)-g, 'readout balance')
    cases=0
    for m0,s0,P,power,delta in itertools.product(
        [3,6],[2],[2,6],[40,80,160],[mp.mpf(0),mp.mpf('1e-30'),mp.mpf('1e-60')]):
        a=mp.mpf(s0)/(2*(m0+s0)+2); g=mp.mpf(s0)/(m0+s0+3)
        w=mp.mpf('0.6'); G=mp.mpf('0.8'); c0=mp.mpf('0.2')
        b=a*w/(w+a*G); B=mp.mpf(10)**power
        LB=mp.log(100*3*B/mp.mpf('0.05'))
        x=(LB/B)**b; t=x+delta**g
        require(0<t<1, 'schedule test regime')
        N=P*int(mp.floor(mp.log(1/t)/(P*w)))
        require(N>=P, 'positive returning length')
        q=c0*mp.exp(-G*N); n=mp.floor(B*q/2)
        require(n>=2 and n<=B, 'count regime')
        Ln=mp.log(100*3*n/mp.mpf('0.05'))
        require(mp.exp(-w*N)<=mp.exp(w*P)*t*(1+mp.mpf('1e-60')), 'floor bias')
        require(n>=B*q/3, 'count floor comparison')
        require((Ln/n)**a<=(3/c0)**a*x*(1+mp.mpf('1e-60')), 'sampling balance')
        rhs=(1+N)*(mp.exp(-w*N)+(Ln/n)**a+delta**g)
        bound=(1+1/w)*(mp.exp(w*P)+(3/c0)**a+1)*t*mp.log(mp.e/t)
        require(rhs<=bound, 'joint t log(e/t) schedule')
        cases+=1
    thresholds=0
    for a0 in [sp.Rational(1,2),sp.Rational(4,5),sp.Rational(19,20),sp.Rational(99,100)]:
        m0=3
        while 7*a0**m0>=1:
            m0+=1
        require(6*a0**m0/(1-a0**m0)<1, 'weighted inverse threshold')
        if m0>3:
            require(6*a0**(m0-1)/(1-a0**(m0-1))>=1, 'threshold minimality')
        thresholds+=1
    return dict(symbolic_balance_identities=3, returning_schedule_cases=cases,
                weighted_order_cases=thresholds)


def main() -> None:
    result={
        'status':'PASS',
        'runtime':{'python':platform.python_version(),'sympy':sp.__version__,
                   'mpmath':mp.__version__},
        'scope':'Independent finite exact algebra and multiprecision diagnostics; not a proof certificate.',
        'anchor':anchor_checks(), 'transfer':transfer_checks(),
        'sensitivity':sensitivity_checks(), 'rates':rate_checks(),
        'limitations':[
            'Polynomial actions are not asserted to be realizable billiard actions.',
            'Thinning is outside the exact-tag model, not a counterexample to its theorem.',
            'Schedule tests check algebra, not all class/count/bandwidth constants.',
            'No certification of infinite-dimensional estimates, concentration uniformity or unreviewed proofs.',
            'No manuscript diagnostic module is imported.'
        ]}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
