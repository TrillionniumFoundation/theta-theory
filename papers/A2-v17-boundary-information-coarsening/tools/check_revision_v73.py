#!/usr/bin/env python3
"""Finite exact diagnostics for the complete charged local invariant.

Model identities are not geometric realization proofs. Matrix checks do not
certify the infinite-dimensional inverse or statistical uniformity. Explicit
exceptions keep every check active under python -O.
"""
from __future__ import annotations
import json
import math
import sympy as sp
import mpmath as mp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def zero(expr, message: str) -> None:
    require(sp.simplify(expr) == 0, message)


def main() -> None:
    u,v,d,p,D,a,b,l,q,eta,area = sp.symbols('u v d p D a b l q eta area', real=True)
    residual = d + p*u - p*v - a*u*u - b*v*v + D*u*v
    amplitude = (1+l*u)*(1+q*v)*(1+eta*u*v)
    g = amplitude*residual
    clock = (sp.diff(g,u,v)/g-sp.diff(g,u)*sp.diff(g,v)/g**2).subs({u:0,v:0})
    zero(clock-(p*p/d**2+D/d+eta), 'finite clock correction')
    require(sp.simplify(clock-p*p/d**2) != 0, 'uncorrected clock negative control')

    area_cases=0
    normalization_negative_controls=0
    radius=sp.Rational(1,32)
    for j in range(1,13):
        vals={d:sp.Rational(4+j,4),p:sp.Rational((-1)**j*(j+1),10),D:sp.Rational(1,j+3),
              a:sp.Rational(j+1,7),b:sp.Rational(j+2,9),l:sp.Rational(1,4),q:sp.Rational(-1,5),
              eta:sp.Rational((-1)**j,7),area:sp.Rational(5+j,3)}
        r=residual.subs(vals); beta=amplitude.subs(vals)
        lower=vals[d]-2*abs(vals[p])*radius-(abs(vals[a])+abs(vals[b])+abs(vals[D]))*radius**2
        require(lower>0, 'positive residual fixture')
        require(abs(vals[l])*radius<1 and abs(vals[q])*radius<1 and abs(vals[eta])*radius**2<1,
                'positive amplitude fixture')
        mass=sp.integrate(beta*r,(u,-radius,radius),(v,-radius,radius))
        f00=vals[d]/mass
        pi=vals[D]*mass/(2*sp.pi*vals[area])
        recovered=vals[D]*vals[d]/(2*sp.pi*pi*f00)
        zero(recovered-vals[area], 'exact finite area anchor')
        require(0<float(pi)<1, 'success subprobability fixture')
        small=sp.integrate(beta*r,(u,-radius/2,radius/2),(v,-radius/2,radius/2))
        wrong=vals[D]*vals[d]/(2*sp.pi*pi*(vals[d]/small))
        require(sp.simplify(wrong-vals[area]) != 0, 'renormalized interior negative control')
        require(sp.simplify(2*sp.pi*recovered-vals[area]) != 0, 'missing Liouville factor control')
        area_cases+=1; normalization_negative_controls+=2

    mp.mp.dps=60
    matrix_cases=0; derivative_cases=0; asymptotic_cases=0
    for period in (2,3,4):
        cs=[sp.Rational(i+2,5) for i in range(period)]
        ks=[sp.Rational(i+3,4) for i in range(period)]
        def Q(i, value=None):
            c=cs[i] if value is None else value
            k=ks[i]
            return sp.Matrix([[1+2*c/k,1/k],[2*c,1]])
        for phase in range(period):
            M=sp.eye(2)
            for j in range(period): M=Q((phase+j)%period)*M
            zero(M.det()-1, 'unimodular monodromy')
            x=sp.trace(M)/2
            for n in (1,2,5,9):
                exact=1/(M**n)[0,1]
                recurrence=1/(M[0,1]*sp.chebyshevu(n-1,x))
                zero(exact-recurrence, 'exact returning twist')
                matrix_cases+=1
            t=sp.symbols('t',real=True)
            Mt=sp.eye(2)
            for j in range(period):
                i=(phase+j)%period
                Mt=Q(i,cs[i]+t if i==0 else cs[i])*Mt
            trace=float(sp.trace(M)); chi=mp.acosh(mp.mpf(str(sp.N(sp.trace(M)/2,60))))
            b12=mp.mpf(str(sp.N(M[0,1],60)))
            xdot=mp.mpf(str(sp.N(sp.diff(sp.trace(Mt),t).subs(t,0)/2,60)))
            bdot=mp.mpf(str(sp.N(sp.diff(Mt[0,1],t).subs(t,0),60)))
            chidot=xdot/mp.sinh(chi)
            require(chidot>0, 'positive curvature direction')
            for n in (1,3,8):
                direct=sp.diff(-sp.log((Mt**n)[0,1]),t).subs(t,0)
                numeric=mp.mpf(str(sp.N(direct,60)))
                formula=(mp.coth(chi)-n*mp.coth(n*chi))*chidot-bdot/b12
                require(abs(numeric-formula)<mp.mpf('1e-45'),'log twist derivative formula')
                derivative_cases+=1
            for n in (25,100):
                scaled=(mp.coth(chi)/n-mp.coth(n*chi))*chidot-bdot/(n*b12)
                require(abs(scaled+chidot)<=2*(abs(mp.coth(chi)*chidot)+abs(bdot/b12))/n,
                        'linear returning-length amplification')
                asymptotic_cases+=1

    s,m,omega,Gamma=sp.symbols('s m omega Gamma',positive=True)
    alpha=s/(2*(m+s)+2)
    beta=alpha*omega/(omega+alpha*Gamma)
    zero(alpha-beta*alpha*Gamma/omega-beta,'charged budget exponent identity')
    gamma=s/(m+s+3)
    zero(1-(m+3)/(m+s+3)-gamma,'readout exponent identity')
    budget_cases=0
    for mm in (3,9):
        for ss in (1,2):
            for ww,gg in ((0.2,0.7),(0.8,1.1)):
                aa=ss/(2*(mm+ss)+2); bb=aa*ww/(ww+aa*gg); cc=ss/(mm+ss+3)
                B=10.0**40; L=math.log(100*B); P=3
                x=(L/B)**bb
                for delta in (0.,1e-24,1e-12):
                    tt=x+delta**cc
                    require(tt<1,'budget test domain')
                    N=P*math.floor(math.log(1/tt)/(P*ww))
                    require(math.exp(-ww*N)<=math.exp(ww*P)*tt*(1+1e-12),'returning floor bias')
                    require(math.exp(-gg*N)>=tt**(gg/ww)*(1-1e-12),'effective count lower bound')
                    require((L/B)**aa*tt**(-aa*gg/ww)<=tt*(1+1e-12),'budget sampling balance')
                    if delta==0:
                        old=P*math.floor(aa*math.log(B/L)/(P*(ww+aa*gg)))
                        require(N==old,'zero-readout returning design unchanged')
                    budget_cases+=1
    print(json.dumps({
        'status':'passed','finite_clock_identity':True,'uncorrected_clock_negative_control':True,
        'exact_finite_area_cases':area_cases,'normalization_negative_controls':normalization_negative_controls,
        'exact_transfer_cases':matrix_cases,'log_twist_derivative_cases':derivative_cases,
        'linear_amplification_checks':asymptotic_cases,'budget_readout_cases':budget_cases,
        'scope':'Finite algebra and transfer checks only; not geometric realization, uniform PDE/dynamical estimates, statistical proof, priority clearance, or formal certification.'
    },indent=2,sort_keys=True))

if __name__=='__main__': main()
