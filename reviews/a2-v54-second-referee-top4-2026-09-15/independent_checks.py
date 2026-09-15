#!/usr/bin/env python3
"""Independent finite diagnostics for the v54 referee memorandum.
No author imports, network calls, repository writes, or optimization-sensitive asserts.
The exact finite laws are controls, not a proof of billiard realization.
Run: python independent_checks.py
"""
import json, math
from fractions import Fraction as F

def require(ok, text):
    if not ok: raise RuntimeError(text)

def tv(p,q): return sum(abs(x-y) for x,y in zip(p,q))/2

def capped(p,q,b):
    values=[]
    for k in range(1,b+1): values.extend((1-p)**(k-1)*p*x for x in q)
    values.append((1-p)**b)
    require(sum(values)==1,'normalization')
    return values

def time_risk(p0,p1,b):
    # Exact rational monotone likelihood test; equality is assigned to zero.
    t=0
    for k in range(1,b+1):
        if p0*(1-p0)**(k-1)>=p1*(1-p1)**(k-1):t=k
    return ((1-p0)**t+1-(1-p1)**t)/2,t

def risk_float(p0,p1,b):
    ell=math.log(p0/p1)/ (math.log1p(-p1)-math.log1p(-p0))
    t=min(b,math.floor(1+ell))
    return (math.exp(t*math.log1p(-p0))-math.expm1(t*math.log1p(-p1)))/2,t

def main():
    cases=0; q0=[F(1,5),F(4,5)];q1=[F(3,5),F(2,5)];epsilon=tv(q0,q1)
    for p0 in [F(1,5),F(1,2),F(4,5)]:
        for p1 in [p0/2,p0/10]:
            for b in [1,2,5,13,40]:
                x=capped(p0,q0,b);y=capped(p1,q1,b);z=capped(p1,q0,b)
                a0=1-(1-p0)**b;a1=1-(1-p1)**b
                distance=tv(x,y)
                require(a0-a1<=distance<=a0,'common cemetery bounds')
                full=(1-distance)/2; count,t=time_risk(p0,p1,b)
                require(count==(1-tv(x,z))/2,'exact count threshold risk')
                require(tv(y,z)==a1*epsilon,'kernel error with common marks')
                require(0<=count-full<=a1*epsilon/2,'full/count risk comparison')
                for p in [p0,p1]:
                    charge=sum((1-p)**k for k in range(b))
                    require(charge==(1-(1-p)**b)/p,'capped expected charge')
                rf,tf=risk_float(float(p0),float(p1),b)
                require(abs(rf-float(count))<1e-12,'closed threshold formula')
                cases+=1
    # Exact uniform-square moments and the manuscript coefficient.
    int_F=F(4,9)-F(4,9)
    int_F2=F(4,81)-F(8,81)+F(4,25)
    require(int_F==0 and int_F2==F(224,2025),'interaction moments')
    coeff=int_F2/F(256)
    require(coeff==F(7,16200),'Hellinger coefficient after normalization')
    a0sq=F(7800,49);a1sq=F(1900,9)
    require(a1sq-a0sq==F(22900,441),'actual curvature contrast')
    # Density-floor and affinity controls on two atoms.
    hellinger=[]
    for e in [1e-2,1e-3,1e-4]:
        p=[.5,.5];q=[.5+e,.5-e]
        h2=sum((math.sqrt(x)-math.sqrt(y))**2 for x,y in zip(p,q))
        n=101;product_h2=2*(-math.expm1(n*math.log1p(-h2/2)))
        require(product_h2<=n*h2+1e-14,'affinity tensorization')
        require(.9<=h2/e**2<=1.1,'positive-floor quadratic order')
        h2_zero=e+(1-math.sqrt(1-e))**2
        require(h2_zero/e**2>50,'negative control: no density floor')
        hellinger.append({'epsilon':e,'H2_over_epsilon_squared':h2/e**2})
    # Asymptotic cap risk and the large-cap failure of the any-acceptance statistic.
    asym=[]
    for p0 in [1e-2,1e-4,1e-6]:
        p1=p0*p0
        row={'p0':p0,'p1':p1,'finite_lambda':[]}
        for lam in [.5,1.,3.]:
            b=math.floor(lam/p0);risk,t=risk_float(p0,p1,b)
            row['finite_lambda'].append({'lambda':lam,'risk':risk,'limit':math.exp(-lam)/2})
        b=math.ceil(10/p1)
        risk,t=risk_float(p0,p1,b)
        naive=(math.exp(b*math.log1p(-p0))-math.expm1(b*math.log1p(-p1)))/2
        require(naive>.49 and risk<.06,'large-cap negative control')
        row['large_cap']={'optimal_count_risk':risk,'any_acceptance_risk':naive,'threshold':t}
        asym.append(row)
    # Strict improvement of the sufficient product condition.
    h=1e-3;n=round(h**-8);flight_error=h**5
    require(n*flight_error>1 and n*flight_error**2<1e-5,'joint scaling control')
    result={'status':'passed','exact_capped_law_cases':cases,'window_integral_F_squared':str(int_F2),
       'Hellinger_coefficient_without_Delta_squared_over_d4':str(coeff),
       'geometric_Delta':str(a1sq-a0sq),'positive_floor_controls':hellinger,
       'cap_regime_controls':asym,'negative_controls':['missing positive density floor','any acceptance with an excessively large cap'],
       'scope':'Finite exact rational probability controls and floating asymptotics; no infinite-flight billiard proof.'}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
