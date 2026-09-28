#!/usr/bin/env python3
"""Independent exact finite diagnostics for A2 v55, Theorem 23.4.
Uses rational arithmetic for every finite-law assertion. No author checker
is imported. Numerical asymptotic illustrations are separately labelled.
Run identically under python and python -O; assertions are not used.
"""
from __future__ import annotations
from fractions import Fraction as F
import hashlib,itertools,json,math

def require(ok:bool,msg:str)->None:
    if not ok: raise RuntimeError(msg)
def tv(x,y): return sum(abs(a-b) for a,b in zip(x,y))/2
def risk(x,y): return sum(min(a,b) for a,b in zip(x,y))/2
def count(p,b): return [p*(1-p)**k for k in range(b)]+[(1-p)**b]
def full(p,q,b): return [p*(1-p)**k*t for k in range(b) for t in q]+[(1-p)**b]
def counts_to_full(c,q): return [x*t for x in c[:-1] for t in q]+[c[-1]]
def bit_to_full(a,base):
    acceptance=sum(base[:-1])
    return [a*x/acceptance for x in base[:-1]]+[1-a]
def run():
    ps=sorted({F(n,d) for d in (3,4,5,7) for n in range(1,d)})
    marks=[(F(1),F(0)),(F(0),F(1)),(F(1,2),F(1,2)),(F(1,4),F(3,4))]
    rows=[]; ties=0; positive_gains=0; charged_discrepancies=0
    checks=0
    for p1,p0 in itertools.combinations(ps,2):
        for b in (1,2,3,7,12):
            c0,c1=count(p0,b),count(p1,b)
            K=max([k+1 for k in range(b) if c0[k]>=c1[k]],default=0)
            require(K>=1,'threshold is nonempty')
            require(all(c0[k]>=c1[k] for k in range(K)) and all(c0[k]<c1[k] for k in range(K,b)),'monotone threshold')
            rc=risk(c0,c1)
            formula=((1-p0)**K+1-(1-p1)**K)/2
            require(rc==formula,'exact threshold risk')
            require(c0[-1]<c1[-1],'cemetery decision')
            # Check the logarithmic formula away from numerical ties; exact
            # rational equalities certify ties and either tie decision.
            z=1+math.log(float(p0/p1))/(math.log1p(-float(p1))-math.log1p(-float(p0)))
            equal=[k+1 for k in range(b) if c0[k]==c1[k]]
            if equal:
                ties+=1
                require(((1-p0)**(K-1)+1-(1-p1)**(K-1))/2==rc,'tie decision')
            elif abs(z-round(z))>1e-10:
                require(min(b,math.floor(z))==K,'log threshold')
            a0,a1=1-c0[-1],1-c1[-1]
            bit0,bit1=[1-a0,a0],[1-a1,a1]
            for q0,q1 in itertools.product(marks,repeat=2):
                f0,f1=full(p0,q0,b),full(p1,q1,b)
                eta=tv(q0,q1); rf=risk(f0,f1)
                require(sum(f0)==sum(f1)==1,'normalization')
                sim0,sim1=counts_to_full(c0,q0),counts_to_full(c1,q0)
                require(sim0==f0,'zero alternative count simulation')
                require(tv(sim1,f1)==a1*eta,'exact count simulation error')
                require(F(0)<=rc-rf<=a1*eta/2,'full/count risk bounds')
                require(a0-a1<=tv(f0,f1)<=a0,'cemetery sandwich')
                overlap=((1-p0)**b+sum(min(p0*(1-p0)**k*x,p1*(1-p1)**k*y) for k in range(b) for x,y in zip(q0,q1)))/2
                require(rf==overlap,'full overlap identity')
                require(bit_to_full(a0,f0)==f0,'zero alternative bit simulation')
                require(tv(bit_to_full(a1,f0),f1)<=a1,'bit simulation bound')
                if rc>rf: positive_gains+=1
                for p,c in ((p0,c0),(p1,c1)):
                    charge=sum(F(k+1)*c[k] for k in range(b))+b*c[-1]
                    require(charge==(1-(1-p)**b)/p,'stopped charge')
                    simcharge=sum(F(k+1)*sum(counts_to_full(c,q0)[2*k:2*k+2]) for k in range(b))+b*c[-1]
                    require(charge==simcharge,'count kernel charge')
                sim=bit_to_full(a1,f0)
                simcharge=sum(F(k+1)*sum(sim[2*k:2*k+2]) for k in range(b))+b*sim[-1]
                truecharge=(1-(1-p1)**b)/p1
                if simcharge!=truecharge: charged_discrepancies+=1
                checks+=12
                rows.append([str(p0),str(p1),b,[str(x) for x in q0],[str(x) for x in q1],K,str(rc),str(rf),str(a1*eta)])
    # Exact rational information constants from Section 23, not a
    # numerical integration of an infinite billiard or a CLT certificate.
    integral=F(4)*(F(1,25)-F(1,81))
    require(integral==F(224,2025),'F squared integral')
    require(integral/F(256)==F(7,16200),'Hellinger coefficient')
    require(F(1900,9)-F(7800,49)==F(22900,441),'actual curvature coefficient')
    require(F(1,10)-16*F(1,640)==F(3,40),'curvature radius floor')
    # Jet-block determinant using rational e^(n gamma) and type ratio.
    jet_cases=0
    for e,r in itertools.product((F(3,2),F(2),F(4)),(F(1,2),F(1),F(3))):
        coth=(e*e+1)/(e*e-1);csch=2*e/(e*e-1)
        require(coth*coth-(r*csch)*(csch/r)==1,'signed jet block determinant')
        jet_cases+=1
    illustrations=[]
    for n in (10,30,100,1000):
        p0,p1=1/n,1/n**3;b=n**4
        k=min(b,math.floor(1+math.log(p0/p1)/(math.log1p(-p1)-math.log1p(-p0))))
        tail0=math.exp(k*math.log1p(-p0));a1=-math.expm1(k*math.log1p(-p1))
        bitrisk=(1-abs(math.exp(b*math.log1p(-p1))-math.exp(b*math.log1p(-p0))))/2
        illustrations.append({'n':n,'b':b,'count_risk':(tail0+a1)/2,'bit_risk':bitrisk})
    require(illustrations[-1]['count_risk']<1e-5 and illustrations[-1]['bit_risk']>.499,'large cap negative control')
    require(positive_gains>0 and charged_discrepancies>0 and ties>0,'nonvacuous controls')
    return {'status':'passed','finite_marked_laws':len(rows),'finite_assertion_lower_bound':checks,'count_tie_cases':ties,'strict_finite_mark_improvements':positive_gains,'bit_kernel_changed_expected_charge_cases':charged_discrepancies,'case_digest_sha256':hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest(),'exact_information_constants':{'integral_F_squared':str(integral),'Hellinger_coefficient':str(integral/F(256)),'Delta':str(F(1900,9)-F(7800,49))},'exact_jet_determinant_cases':jet_cases,'large_cap_numerical_illustrations':illustrations,'scope':'Finite probability identities, algebraic controls, and labelled asymptotic illustrations only; not a proof certificate, a full billiard simulation, or a numerical proof of the limiting theorems. No author checker imported. Explicit exceptions remain active under python -O.'}
if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
