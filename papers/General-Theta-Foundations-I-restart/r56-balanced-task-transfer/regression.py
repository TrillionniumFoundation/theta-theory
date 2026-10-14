#!/usr/bin/env python3
"""Finite arithmetic and numerical regression, NOT continuous theorem verification.
All checks use explicit exceptions and therefore also execute under python -O.
"""
from fractions import Fraction as F
from itertools import combinations,product
import hashlib,json,math
C={};EXACT=[]
def test(group,ok,description,exact=None):
    if not ok: raise RuntimeError(group+': '+description)
    C[group]=C.get(group,0)+1
    if exact is not None: EXACT.append(str(exact))
def main():
    # Arbitrary raw sign-dependent joint report/audit kernels; uniform flip must
    # balance both their marginal and their squared-loss measure.
    for a,b in product(range(1,8),repeat=2):
        jp=[F(a,16),F(8-a,16),F(b,16),F(8-b,16)]
        jm=list(reversed(jp));ref=[(x+y)/2 for x,y in zip(jp,jm)]
        for l in (F(0),F(1,5),F(1,2),F(4,5),F(1)):
            after=[(l*x+(1-l)*y+l*y+(1-l)*x)/2 for x,y in zip(jp,jm)]
            test('exact_raw_task_balance',after==ref,'joint kernel',after)
            for r in (F(-1),F(0),F(2,3)):
                for mark in (0,1):
                    got=sum(after[2*mark+j]*(F(2*j-1)-r)**2 for j in (0,1))
                    want=sum(ref[2*mark+j]*(F(2*j-1)-r)**2 for j in (0,1))
                    test('exact_raw_task_balance',got==want,'unnormalized selected loss',got)
    test('exact_counterexamples',F(1)==F(1) and (F(1)-F(1))**2 != (F(-1)-F(1))**2,'report-only balance fails')
    # Paid gate identities and conditional drift over many admissible rows.
    for q in range(1,12):
        p0=F(1,q);k=1+1/p0
        for b in range(1,12):
            alpha=F(1,b);wg=k/alpha;wa=wg-1/p0
            for p in (p0,(1+p0)/2,F(1)):
                test('exact_gate_and_killed_potentials',wg>=1+(1-p)*wg+p*wa,'gate potential',wg)
            test('exact_gate_and_killed_potentials',wa==1+(1-alpha)*wg,'productive potential',wa)
            test('exact_gate_and_killed_potentials',p0*(wg-wa)==1,'predictable paid gate')
    # Exact density-cap optimum for a finite acquired law, including the
    # fractional last atom. This is a finite witness, not a proof of compactness.
    nu=[F(1,8),F(1,8),F(1,4),F(1,2)];cost=[F(0),F(1,16),F(1,4),F(1)]
    for b in (F(1),F(3,2),F(2),F(3),F(4),F(8),F(16)):
        mass=F(1);selected=[]
        for p in nu:
            x=min(b*p,mass);selected.append(x);mass-=x
        test('exact_acquired_selection',sum(selected)==1 and all(0<=s<=b*p for s,p in zip(selected,nu)),'actual density cap',selected)
        value=sum(x*c for x,c in zip(selected,cost))
        if b>=8:test('exact_acquired_selection',value==0,'actual atom threshold')
        # Constant conditional acceptance realizes exactly this selected law.
        acc=sum(x/b for x in selected);loss=sum(x*c/b for x,c in zip(selected,cost))
        test('exact_acquired_selection',acc==1/b and loss/acc==value,'rejection realization',value)
    # Terminal exports and complete tagged construction.
    for M in range(13,300):
        m=(M-1)//3-2
        test('exact_state_accounting',1+3*(2+m)<=M and m>=1 and 8*m>=M,'joint tagged program',m)
    # Physical command intersections are unchanged by duplication of names.
    contexts=[frozenset((0,1)),frozenset((1,2)),frozenset((2,3)),frozenset((0,3))]
    def cover(sets):
        masks=[]
        for mask in range(1,1<<len(sets)):
            ids=[i for i in range(len(sets)) if mask>>i&1]
            if set.intersection(*(set(sets[i]) for i in ids)):masks.append(mask)
        target=(1<<len(sets))-1
        for n in range(1,len(sets)+1):
            for rows in combinations(masks,n):
                if __import__('functools').reduce(int.__or__,rows)==target:return n
        raise RuntimeError('cover unavailable')
    a=cover(contexts);expanded=[{(x,j) for x in s for j in range(3)} for s in contexts]
    test('exact_state_accounting',a==cover(expanded)==2,'stateless aliases')
    # End-to-end dyadic certificate with exact outward/inward mass accounting.
    e=F(1,2**14);alpha=(F(1,4)-4*e)*(F(1,8)-2*e);beta=F(1,3072)
    test('exact_dyadic_certificate',alpha==F(1046529,33554432),'acceptance mass',alpha)
    test('exact_dyadic_certificate',5/alpha==F(167772160,1046529) and 5/alpha<161,'paid core budget',5/alpha)
    test('exact_dyadic_certificate',beta/alpha==F(32768,3139587),'risk upper',beta/alpha)
    test('exact_dyadic_certificate',[int((F(3,8)+e)/e),int((F(5,8)-e)/e),int((F(1,8)-e)/e)]==[6145,10239,2047],'threshold integers')
    test('exact_dyadic_certificate',F(1,32)-alpha>0,'same-report boundary mass')
    test('exact_dyadic_certificate',F(1,4)*F(1,8)*((F(1,8)**2+F(1,8)**2)/3)==beta,'rectangle loss integral')
    # Quantum checks include pure inputs, rank changes and noncommuting effects.
    import numpy as np
    I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]).astype(complex)
    paulis=[I,X,Y,Z]
    for phi in (0.,.31,1.17,math.pi/2):
        n=math.cos(phi)*X+math.sin(phi)*Y
        for eta in (0.,.5,1.):
            effects=[(I+v*eta*n)/2 for v in (-1,1)]
            for vec in ([0,0,0],[1,0,0],[0,0,1],[.2,.3,.1]):
                rho=(I+vec[0]*X+vec[1]*Y+vec[2]*Z)/2
                avg=sum(U@rho@U.conj().T for U in paulis)/4
                test('numeric_quantum',np.linalg.norm(avg-I/2)<1e-13,'Pauli average')
                for E in effects:
                    vals,V=np.linalg.eigh(E);L=(V*np.sqrt(np.maximum(vals,0)))@V.conj().T
                    state=L@avg@L
                    test('numeric_quantum',abs(np.trace(state).real-.5)<1e-13 and abs(np.trace(Z@state).real)<1e-13,'joint report/audit moments')
            test('numeric_quantum',min(np.linalg.eigvalsh(effects[0]))>=-1e-14,'positive effects')
    test('numeric_quantum',np.linalg.norm(((I+X)/2)@((I+Y)/2)-((I+Y)/2)@((I+X)/2))>.1,'noncommuting actual effects')
    # Independent floating numerical sanity for analytic tail inequalities.
    from scipy.integrate import quad
    from scipy.optimize import brentq
    from scipy.special import ndtr
    norm=math.sqrt(2*math.pi)
    def sech2(x):
        v=math.exp(-2*abs(x));return 4*v/(1+v)**2
    for a,s in ((.5,1.),(1.,1.),(2.,1.5)):
        k=a/s**2
        for b in (1.,2.,4.,20.,100.):
            tail=lambda t:ndtr((a-t)/s)+ndtr((-a-t)/s)
            t=0. if b==1 else brentq(lambda t:tail(t)-1/b,0,30*(a+s))
            density=lambda x:(math.exp(-.5*((x-a)/s)**2)+math.exp(-.5*((x+a)/s)**2))/(2*s*norm)
            D=2*b*quad(lambda x:sech2(k*x)*density(x),t,math.inf,epsabs=1e-13)[0]
            U=4*b*quad(lambda x:(2*math.exp(-2*k*x)/(1+math.exp(-2*k*x)))*density(x),t,math.inf,epsabs=1e-13)[0]
            test('numeric_gaussian',abs(tail(t)-1/b)<1e-10 and D>0,'actual tail quantile')
            test('numeric_gaussian',D<=U+1e-10 and U<=2*D+1e-10,'uniform risk squeeze')
    test('numeric_dyadic_interval',5/(161*math.pi)<float(beta/alpha)<.01044,'same-budget interval')
    exact_count=sum(v for k,v in C.items() if k.startswith('exact_'))
    result={'status':'PASS','exact_checks':exact_count,'numerical_checks':sum(C.values())-exact_count,'categories':C,'exact_transcript_sha256':hashlib.sha256('\n'.join(EXACT).encode()).hexdigest(),'dyadic':{'acceptance_lower':str(alpha),'loss_numerator_upper':str(beta),'core_cost_upper':str(5/alpha),'risk_upper':str(beta/alpha),'core_budget':161,'total_with_audit_budget':162},'scope':'finite arithmetic and floating-point regression only; neither continuous-parameter proof nor priority certification'}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
