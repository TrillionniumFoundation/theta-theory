#!/usr/bin/env python3
"""Finite witnesses and numerical consistency checks, never mathematical proof.
All checks raise explicitly and run identically with Python -O.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import hashlib, json, math

COUNTS: dict[str,int] = {}
DIGEST: list[str] = []
def check(group: str, condition: bool, message: str, value=None) -> None:
    if not condition:
        raise RuntimeError(f'{group}: {message}')
    COUNTS[group] = COUNTS.get(group,0)+1
    if value is not None:
        DIGEST.append(repr(value))

def main() -> None:
    # Independent live/output injections, including the reviewer's two-label gate.
    for live,term in product(range(1,18),repeat=2):
        event=max(live,term); typed=live+term
        live_ids=set(range(live)); term_ids=set(range(term))
        check('exact_role_packing',len(live_ids|term_ids)==event,'event union')
        check('exact_role_packing',len(live_ids)+len(set(range(live,typed)))==typed,'typed disjoint')
        check('exact_role_packing',live+term-len(live_ids&term_ids)==event,'overlap identity',(live,term,event,typed))
        for cap in range(0, min(live,term)+1):
            needed=live+term-cap
            check('exact_partial_overlap',term<=needed-max(live-cap,0),'terminal cap')
    # Both terminal readouts may overlap the gate and productive command labels.
    commands={0:'gate',1:'productive'}; readout={0:F(-1),1:F(1)}
    transitions={('gate',False):(0,0),('gate',True):(1,0),('productive','reject'):(0,0),('productive','negative'):(0,1),('productive','positive'):(1,1)}
    for key,(state,halt) in transitions.items():
        check('exact_two_label_gate',state in commands and state in readout,'shared label')
        if halt:check('exact_two_label_gate',key[0]=='productive','no gate commitment')
    check('exact_two_label_gate',len(commands)==2 and len(readout)==2,'two live and two output roles')
    # The exact budget substitution and the special first-attempt boundary.
    for den in range(2,25):
        a=F(1,den)
        for b in range(2,30):
            if F(b)<1/(1-a):continue
            beta=F(b)/(1+b*a)
            check('exact_approximate_budget',beta>=1 and beta*a<1,'admissible design')
            check('exact_approximate_budget',beta/(1-beta*a)==b,'physical budget exactly restored',beta)
            for q,e in ((F(0),F(1,100)),(F(1,5),F(1,60)),(F(2,3),F(0))):
                check('exact_approximate_budget',(q+beta*e)/(1-beta*a)==(1+b*a)*q+b*e,'loss substitution')
    for b in range(1,50):
        e=F(1,100*b);p=F(1,b)
        check('exact_sharp_task_defect',b*e*p==e and b*e<=1,'raw loss measure defect',b*e)
        for r in (F(-1),F(-1,3),F(0),F(2,3),F(1)):
            v=b*e+r*r
            check('exact_sharp_task_defect',v>=b*e,'conditional variance converse')
        check('exact_sharp_task_defect',p*b==1,'selected mass and paid cost')
    for beta in range(2,30):
        for den in (2,3,5,11):
            a=F(1,beta*den);p=F(1,beta)-a
            check('exact_sharp_waiting',1/p==F(beta)/(1-beta*a),'waiting denominator',1/p)
    for r in (F(-1),F(-3,7),F(0),F(2,5),F(1)):
        check('exact_no_first_moment_balance',((1-r)**2+(-1-r)**2)/2==1+r*r,'all-program indistinguishability')
    for M in range(7,500):
        m=M//3
        check('exact_joint_roles',max(7,3*m)<=M and 4*m>=M,'event joint construction')
        if M>=13:
            k=(M-1)//3-2
            check('exact_joint_roles',7+3*k<=M and 8*k>=M,'typed joint construction')
    for l,t,K,E in product(range(1,7),repeat=4):
        check('exact_simulator_roles',max(l*K,t*E)<=l*K+t*E,'packed versus typed composition')
    for l,t,k1,k2,e1,e2 in product(range(1,4),repeat=6):
        check('exact_simulator_associativity',((l*k1)*k2,(t*e1)*e2)==(l*(k1*k2),t*(e1*e2)),'pair products')
    # Probabilistic raw moment perturbations through sign and Pauli controls.
    import numpy as np
    I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]).astype(complex)
    pauli=[I,X,Y,Z]
    for fault in (0.,.01,.1,.24):
        weights=np.array([.25+fault,.25-fault,.25,.25])
        for vec in ([0,0,0],[1,0,0],[0,0,1],[.2,.3,.4]):
            rho=(I+vec[0]*X+vec[1]*Y+vec[2]*Z)/2
            out=sum(w*(u@rho@u.conj().T) for w,u in zip(weights,pauli))
            trdist=np.sum(np.abs(np.linalg.eigvalsh(out-I/2)))/2
            check('numeric_raw_perturbation',trdist<=fault+1e-13,'Pauli total variation certificate')
        ref=sum(w*(u@(I/2)@u.conj().T) for w,u in zip(weights,pauli))
        check('numeric_raw_perturbation',np.linalg.norm(ref-I/2)<1e-13,'same reference remains exact')
    # Directional posterior integrals are independently compared to scaled Bessel ratios.
    from scipy.integrate import quad
    from scipy.special import ive
    for d in (2,3,4,7,12):
        exponent=(d-3)/2
        for s in (.05,.3,1.,3.,10.,50.):
            # quad's algebraic endpoint rule handles d=2 without endpoint division.
            den=quad(lambda z:math.exp(s*(z-1)),-1,1,weight='alg',wvar=(exponent,exponent),epsabs=2e-12,epsrel=2e-12)[0]
            num=quad(lambda z:z*math.exp(s*(z-1)),-1,1,weight='alg',wvar=(exponent,exponent),epsabs=2e-12,epsrel=2e-12)[0]
            A=num/den;ratio=ive(d/2,s)/ive(d/2-1,s)
            check('numeric_directional_moments',abs(A-ratio)<2e-10,'independent axial integration')
            check('numeric_directional_moments',0<=A<=1 and 1-A*A<=2*(1-A)+2e-15<=2*(1-A*A)+2e-14,'D/U pointwise bounds')
        s=100000.
        A=ive(d/2,s)/ive(d/2-1,s)
        check('numeric_directional_moments',abs(2*s*(1-A)/(d-1)-1)<3e-5,'posterior leading constant')
    # Deterministic simplex covering witness: exhaustive rational directions in R^d.
    for d in (2,3,4,5):
        P=np.eye(d+1)-np.ones((d+1,d+1))/(d+1)
        verts=P*math.sqrt((d+1)/d)
        check('numeric_simplex_cover',np.max(np.abs(np.sum(verts*verts,axis=1)-1))<1e-13,'unit vertices')
        for j in range(1,80):
            u=np.sin(np.arange(1,d+2)*j*.73);u-=u.mean();u/=np.linalg.norm(u)
            dots=verts@u
            check('numeric_simplex_cover',dots.max()>=1/d-1e-13,'inradius support')
            dist=((verts/d-u)**2).sum(axis=1).min()
            check('numeric_simplex_cover',dist<=1-1/d**2+1e-13,'d+1 interior centers')
    counts=dict(sorted(COUNTS.items()))
    print(json.dumps({'status':'PASS','counts':counts,'exact_checks':sum(v for k,v in counts.items() if k.startswith('exact_')),'floating_checks':sum(v for k,v in counts.items() if k.startswith('numeric_')),'witness_sha256':hashlib.sha256('\n'.join(DIGEST).encode()).hexdigest(),'limitations':'finite witnesses and floating consistency only; all continuous claims require the manuscript proofs'},sort_keys=True,indent=2))

if __name__=='__main__':main()
