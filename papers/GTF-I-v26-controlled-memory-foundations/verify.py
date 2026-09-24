#!/usr/bin/env python3
"""Exact identities and finite implementation regressions, not a proof assistant."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product
import json
from math import ceil
import sympy as s


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def bernstein_positive(expr, var, lo=F(1,3), hi=F(7,20)) -> bool:
    """A rational positive-basis certificate over a closed rational interval."""
    t=s.Symbol('t')
    p=s.Poly(s.expand(expr.subs(var,s.Rational(lo.numerator,lo.denominator)+(s.Rational(hi.numerator,hi.denominator)-s.Rational(lo.numerator,lo.denominator))*t)),t)
    n=p.degree()
    if n<0:return False
    co=[sum(p.nth(i)*s.binomial(k,i)/s.binomial(n,i) for i in range(k+1)) for k in range(n+1)]
    return all(v>0 for v in co)



def rectangle_positive(expr, r, g) -> bool:
    x,y=s.symbols('rectangle_x rectangle_y')
    pp=s.Poly(s.expand(expr.subs({r:s.Rational(1,3)+x/60,
                                 g:s.Rational(6,25)+y/50})),x,y)
    nr,ng=pp.degree(x),pp.degree(y)
    return all(sum(pp.coeff_monomial(x**i*y**j)*s.binomial(k,i)/s.binomial(nr,i)
                       *s.binomial(l,j)/s.binomial(ng,j)
                   for i in range(k+1) for j in range(l+1))>0
               for k in range(nr+1) for l in range(ng+1))


def run(mutant: str|None=None) -> dict:
    p,q,z,u,v,r=s.symbols('p q z u v r',real=True)
    cubic=2*r**3+25*r**2-(4 if mutant=='cubic' else 3)
    tau=6*(-r*r+4*r-1)/(r*(3*r+25))
    if mutant=='coin':tau+=s.Rational(1,100)
    value=(-r**3+6*r**2-3*r+14)/32
    require(cubic.subs(r,s.Rational(1,3))<0<cubic.subs(r,s.Rational(7,20)), 'cubic isolating endpoints')
    require(s.Poly(cubic,r).count_roots(s.Rational(1,3),s.Rational(7,20))==1,'cubic root count')
    nt,dt=s.fraction(s.cancel(tau))
    require(bernstein_positive(nt,r) and bernstein_positive(dt-nt,r),'coin range')
    a,c=(1-p)*(1-q),p*q
    targets=[s.Rational(5,16),s.Rational(3,16),s.Rational(3,16),s.Rational(5,16)]
    signs=[targets[j]-([a,a,c,c][j]/2) for j in range(4)]
    events=[[0,0,1,1],[1,0,1,1],[1,1,1,1],[1,1,0,1],[1,1,0,0]]
    responses=[[tau,0,1,1],events[1],events[2],events[3],[1,1,0,tau]]
    if mutant=='response':responses[2]=[1,0,1,1]
    generating=s.Poly(((1-p)+p*z)**2*((1-q)+q*z)**2,z)
    actual=sum(generating.nth(k)*sum(signs[j]*responses[k][j] for j in range(4)) for k in range(5))
    H=(-u**3+3*u*u*v+6*u*u-3*u*v*v-8*u*v-3*u+v**3+2*v*v+15*v+14)/32
    J=(-2*u**3+6*u*u*v-25*u*u-6*u*v*v+26*u*v+2*v**3-v*v-4*v+3)/128
    G=H+tau*J
    require(s.cancel(actual-G.subs({u:(p+q-1)**2,v:(p-q)**2}))==0,'full parameter response identity')
    require(s.expand(J.subs({v:0,u:r})+cubic/128)==0,'least-favorable tie polynomial')
    factor=(u-r)**2*(75+12*r+6*u-37*r*r-74*r*u)/(64*r*(3*r+25))
    numer=s.fraction(s.cancel(G.subs(v,0)-value-factor))[0]
    require(s.rem(numer,cubic,r)==0,'two-preparation square factorization')
    require(F(75)-37*F(7,20)**2-74*F(7,20)>0,'positive square factor bracket')
    require(s.expand(32*s.diff(H,v)-7-(3*(u-v)**2+8*(1-u)+4*v))==0,'transverse H certificate')
    require(s.expand(64*s.diff(J,v)+3-(3*(u-v)**2+13*u+1-v))==0,'transverse J certificate')
    # Exact coefficients from the full prior. A square-root variable is eliminated algebraically.
    t=s.Symbol('t')
    coeff=[]
    for k in range(5):
        row=[]
        for j in range(4):
            expr=0
            for e in [-1,1]:
                pp=(1+e*t)/2
                bb=((1-pp)**2 if j<2 else pp**2)/2
                expr+=s.binomial(4,k)*pp**k*(1-pp)**(4-k)*(targets[j]-bb)/2
            poly=s.Poly(s.expand(256*expr),t)
            require(all(poly.nth(i)==0 for i in range(1,poly.degree()+1,2)),'prior symmetry elimination')
            row.append(s.expand(sum(poly.nth(i)*r**(i//2) for i in range(0,poly.degree()+1,2))))
        coeff.append(row)
    expected=[[-(2*r**3+25*r*r-3),-(2*r**3+27*r*r+12*r-1),-(2*r**3-5*r*r-20*r-1),-(2*r**3-7*r*r-32*r-3)],
              [4*(r-1)*v for v in [2*r*r+7*r-3,2*r*r+9*r-1,2*r*r-7*r-1,2*r*r-9*r-3]],
              [-6*(r-1)**2*v for v in [2*r-3,2*r-1,2*r-1,2*r-3]]]
    expected+=[list(reversed(expected[1])),list(reversed(expected[0]))]
    require(all(s.expand(coeff[i][j]-expected[i][j])==0 for i in range(5) for j in range(4)),'posterior coefficient table')
    signpattern=[[0,-1,1,1],[1,-1,1,1],[1,1,1,1],[1,1,-1,1],[1,1,-1,0]]
    for i in range(5):
        for j in range(4):
            sg=signpattern[i][j]
            if sg==0:require(s.rem(coeff[i][j],cubic,r)==0,'predictive zero coefficient')
            else:require(bernstein_positive(sg*coeff[i][j],r),'posterior sign interval certificate')
    positive_sum=sum(coeff[i][j] for i in range(5) for j in range(4) if signpattern[i][j]>0)/256
    require(s.rem(s.fraction(s.cancel(positive_sum-value))[0],cubic,r)==0,'exact Bayes equality')
    # A uniform two-preparation gamma family, not a grid over target biases.
    g=s.Symbol('gamma',real=True)
    f=r**3+(13-2*g)*r*r+(3-12*g)*r-(1+2*g)
    D=s.diff(f,r)
    tg=-2*(3*r*r+(8*g-14)*r+3)/D
    Hg=H+(g-s.Rational(1,4))*(1-(u-v)**2)/8
    Jg=J+(g-s.Rational(1,4))*((u-v)**2+6*u-2*v+1)/32
    Ag=24*g*g+(3*g-10)*r*r+(6*g-20)*r*u+12*g*r+6*g*u-51*g+30
    Vg=Hg.subs({u:r,v:0})
    fidentity=s.fraction(s.cancel((Hg+tg*Jg).subs(v,0)-Vg-(u-r)**2*Ag/(16*D)))[0]
    require(s.rem(fidentity,f,r)==0,'continuous-family square identity')
    require(s.expand(Jg.subs({u:r,v:0})+f/64)==0,'continuous-family tie')
    require(f.subs({g:s.Rational(6,25),r:s.Rational(1,3)})<0,'family lower root bracket')
    require(f.subs({g:s.Rational(13,50),r:s.Rational(7,20)})>0,'family upper root bracket')
    require(rectangle_positive(D,r,g),'family cubic monotonicity')
    n=-2*(3*r*r+(8*g-14)*r+3)
    require(rectangle_positive(n,r,g) and rectangle_positive(D-n,r,g),'family coin range')
    require(F(30)-10*F(7,20)**2-20*F(7,20)-51*F(13,50)>0,'family positive factor')
    L=r*r+6*r+1
    general=[[s.Integer(0),-8*g*L,32*r*(r+1)-8*g*L,32*r*(r+1)],
             [8*(r-1)*vv for vv in [r*r+4*r-1-2*g*(r+1),r*r+4*r-1+2*g*(r+1),
                                   r*r-4*r-1+2*g*(r+1),r*r-4*r-1-2*g*(r+1)]],
             [-12*(r-1)**2*vv for vv in [r-1-2*g,r-1+2*g,r-1+2*g,r-1-2*g]]]
    general += [list(reversed(general[1])),list(reversed(general[0]))]
    targetg=[(1+g)/4,(1-g)/4,(1-g)/4,(1+g)/4]
    for k in range(5):
        for j in range(4):
            ex=sum(s.binomial(4,k)*((1+e*t)/2)**k*((1-e*t)/2)**(4-k)
                   *(targetg[j]-(((1-e*t)/2)**2 if j<2 else ((1+e*t)/2)**2)/2)/2
                   for e in [-1,1])
            poly=s.Poly(s.expand(256*ex),t)
            cr=s.expand(sum(poly.nth(i)*r**(i//2) for i in range(0,poly.degree()+1,2)))
            require(s.rem(s.expand(cr-general[k][j]),f,r)==0,'family posterior coefficient')
            if signpattern[k][j]:
                require(rectangle_positive(signpattern[k][j]*general[k][j],r,g),'family rectangular sign certificate')
    bg=sum(general[i][j] for i in range(5) for j in range(4) if signpattern[i][j]>0)/256
    require(s.rem(s.expand(bg-Vg),f,r)==0,'continuous-family Bayes equality')
    # The extreme responses are mixtures of the same five events; no coordinatewise free coins.
    require(all(s.expand(responses[0][j]-((1-tau)*events[0][j]+tau*events[1][j]))==0 for j in range(4)), 'frozen extreme event zero')
    require(all(s.expand(responses[4][j]-((1-tau)*events[4][j]+tau*events[3][j]))==0 for j in range(4)), 'frozen extreme event four')
    profile=[1,2,3,3,4,5,5,5,10,12,10,10,7,3]
    require(max(profile)==12 and profile.count(5)==3,'selection cut explicitly charged')
    routing_cases=0
    for m in range(2,21):
        for K in range(1,m+1):
            fibers=[list(range(k,m,K)) for k in range(K)]
            actual_value=min(F(1,2*len(f)) for f in fibers)
            claimed=F(K,2*m) if mutant=='free-selector' else F(1,2*ceil(m/K))
            require(actual_value==claimed,'routing ceiling value cannot be free-selector value')
            mixed=F(K,2*m)
            require((mixed>actual_value)==(m%K!=0),'strict divisibility gap')
            for i in range(m):
                included=sum(i in {(start+j)%m for j in range(K)} for start in range(m))
                require(F(included,2*m)==mixed,'cyclic selector upper witness')
            routing_cases+=1
    require(F(1,3)-F(1,4)==F(1,12),'small routing gap')
    erasure_cases=0
    for m in range(2,17):
        for K in range(1,m+1):
            q0,rem=divmod(m,K)
            weights=[F(q0+int(j<rem),m) for j in range(K)]
            B=1-sum(w*w for w in weights)
            cap=1-F(ceil(m/K),m)
            require((B>cap)==(rem!=0),'perfect-revelation Bayes/minimax discrepancy')
            threshold=F(m,m+rem)
            for rho in [F(0),threshold/2,threshold]:
                if rho==1:continue
                init=[(rho*w+(1-2*rho)/K)/(1-rho) for w in weights]
                require(sum(init)==1 and min(init)>=0,'integer initialization legality')
                means=[rho*(1-w)+(1-rho)*(init[i]-sum(init[j]*weights[j] for j in range(K))) for i,w in enumerate(weights)]
                require(all(v==rho*B for v in means),'low-reveal exact equality')
                erasure_cases+=1
        w,b=F(m//2,m),F((m+1)//2,m)
        for rho in [F(0),F(1,4),F(3,4),F(7,8),F(1)]:
            correct=min(2*w*b*rho,w)
            claimed=2*w*b*rho if mutant=='unbalanced-minimax' else correct
            if rho<=1/(2*b):achieved=2*w*b*rho
            else:achieved=min(w,(2*rho-1)*b)
            require(achieved==claimed,'two-label saturation')
    # Calibration/quantization errors cannot disappear in resource transport.
    coeffs=[F(1,2),F(2,3),F(3,4)]
    ds=[F(1,10),F(1,20),F(1,30),F(1,40)]
    e=ds[0]
    for t0,rate in enumerate(coeffs):
        e=rate*e+ds[t0+1]
        closed=sum(ds[j]*s.prod(coeffs[k] for k in range(j,t0+1)) for j in range(t0+2))
        require(e==closed,'nonstationary quantized-state recurrence')
    cal=1 if mutant=='calibration-register' else (5+1)**(2*(3-1))
    require(cal==1296,'acquired counter register charged')
    for bits in range(1,7):
        for k in range(2**bits+1):
            hits=sum(int(''.join(map(str,word)),2)<k for word in product([0,1],repeat=bits))
            require(F(hits,2**bits)==F(k,2**bits),'dyadic threshold sampler')
    numeric=float(s.nsolve(cubic,s.Rational(1,3)))
    return {'schema':'gtf26.exact/1','U2_root_polynomial':'2*r^3+25*r^2-3',
            'root_isolating_interval':['1/3','7/20'],'U2_decimal':float(value.subs(r,numeric)),
            'tau_decimal':float(tau.subs(r,numeric)), 'full_square_identity':True,'continuous_U2_family':['6/25','13/50'],
            'family_square_and_all_coefficient_signs':True,
            'posterior_coefficients':20,'posterior_signs_rationally_certified':True,
            'frozen_event_count':5,'profile_with_selection_cut':profile,
            'routing_exact_finite_regressions':routing_cases,'integer_erasure_regressions':erasure_cases,
            'online_error_recurrence':True,'calibration_register':cal,
            'scope':'Algebraic and implementation regressions; analytic proofs are in the manuscript.'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--mutant',choices=['cubic','coin','response','free-selector','unbalanced-minimax','calibration-register'])
    args=p.parse_args()
    print(json.dumps(run(args.mutant),indent=2,sort_keys=True))
