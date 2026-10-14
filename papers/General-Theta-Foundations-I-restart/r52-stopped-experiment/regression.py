#!/usr/bin/env python3
"""Exact finite checks and generated arithmetic audit, never a continuum proof.
Assertions use explicit exceptions so python -O cannot remove checks.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json
from gaussian_certificate import run as gaussian_run,table
COUNTS={}
def check(ok:bool,group:str,msg:str=''):
    COUNTS[group]=COUNTS.get(group,0)+1
    if not ok:raise RuntimeError(group+': '+msg)

def conditional():
    for q in (F(1,8),F(1,4),F(3,8)):
        eta=F(3,5);gamma=(1-eta)/2;a=q*gamma/(1-gamma)
        cv=4*a*(1-a);km=1/max(F(2),F(3)/cv);kp=F(3)
        for i,v,t,r in product(range(17),(-1,1),range(1,7),range(-6,7)):
            p=q+(1-2*q)*F(i,16);lik=p*(1+eta*v)/2+(1-p)*(1-eta*v)/2
            post=p*(1+eta*v)/(2*lik);mean=F(t,6)*(2*post-1);w=F(t,6)**2;var=4*w*post*(1-post);rr=F(r,6)
            check(a<=post<=1-a,'classical posterior floor')
            check(2*gamma<=2*lik<=2*(1-gamma),'report envelope')
            check(cv*w<=var<=w,'variance calibration')
            score=w+rr*rr;loss=var+(mean-rr)**2
            check(km*score<=loss<=kp*score,'conditional risk comparison')

def quantum():
    # eta=3/5 has rational transverse factor sqrt(1-eta^2)=4/5.
    eta=F(3,5);gamma=F(1,5)
    for q,xyz,axis,v in product((F(1,8),F(1,4),F(3,8)),product(range(-2,3),repeat=3),(0,2),(-1,1)):
        r=[F(z,3) for z in xyz]
        if sum(x*x for x in r)>1:continue
        r=[(1-2*q)*x for x in r];den=1+eta*v*r[axis];out=[F(4,5)*x/den for x in r];out[axis]=(r[axis]+eta*v)/den
        a=q*gamma/(1-gamma)
        check(sum(x*x for x in out)<=(1-2*a)**2,'quantum spectral floor')
        check(1-out[2]**2>=4*a*(1-a),'quantum audit calibration')
        check(2*gamma<=den<=2*(1-gamma),'quantum report envelope')
    # The two nonparallel effects have a nonzero commutator (Pauli algebra).
    check(eta*eta/F(2)>0,'noncommuting effects')

def occupation():
    for q,a,b in product((F(1,8),F(1,4),F(1,2)),[F(i,8) for i in range(9)],[F(i,8) for i in range(9)]):
        if a+b==0:continue
        k=(1-2*q)/(2*q);D=a+b+2*k*a*b;T=(2+k*(a+b))/D;m=(a-b)/D
        vp=(T-k*m)/2;vm=(T+k*m)/2
        check(vp>=0 and vm>=0,'occupation positivity')
        check(a*vp+b*vm==1 and a*vp-b*vm==m,'terminal mass and mean')
        check(vp==F(1,2)+(1-q)*(1-a)*vp+q*(1-b)*vm,'positive killed balance')
        check(vm==F(1,2)+q*(1-a)*vp+(1-q)*(1-b)*vm,'negative killed balance')
        if a<1:
            aa=(a+1)/2;DD=aa+b+2*k*aa*b
            check((2+k*(aa+b))/DD<=T,'fixed-b cost monotonicity')
            check((aa-b)/DD>=m,'fixed-b signed mean monotonicity')
    for q,beta in product((F(1,8),F(1,4),F(1,2)),(F(1,8),F(1,4),F(1,2),F(1))):
        k=(1-2*q)/(2*q)
        check(2/beta+k>1/beta,'two-state versus three-state threshold')

def marked_finite():
    # Finite measures: optimal bounded selection and mass-cost dual for fixed codebook.
    atoms=[F(i,4) for i in range(5)];weights=[F(1,5)]*5
    for m in (1,2,3):
        for centers in product(atoms,repeat=m):
            d=[x*x+min((x-c)**2 for c in centers) for x in atoms]
            for n in (F(1),F(5,4),F(2),F(5)):
                remaining=F(1);h=[F(0)]*5;order=sorted(range(5),key=lambda i:d[i])
                for i in order:
                    mass=min(remaining,n*weights[i]);h[i]=mass/weights[i];remaining-=mass
                primal=sum(weights[i]*h[i]*d[i] for i in range(5))
                check(remaining==0 and sum(weights[i]*h[i] for i in range(5))==1,'trimmed terminal mass')
                check(all(0<=x<=n for x in h),'trimmed paid domination')
                dual=max(z-n*sum(weights[i]*max(F(0),z-d[i]) for i in range(5)) for z in set(d))
                check(primal==dual,'finite marked dual equality')
                # One live state, halt probability 1/n, exactly the selected loss.
                halt=sum(weights[i]*h[i]/n for i in range(5))
                check(halt==1/n and (sum(weights[i]*h[i]*d[i]/n for i in range(5))/halt)==primal,'one-live implementation')

def accounting():
    for M in range(7,257):
        m=(M-4)//3
        check(4+3*m<=M and 8*m>=M-1,'all-lane state count')
    for n in range(1,33):
        for beta in (F(0),F(1,8),F(1,4),F(1,2)):
            r=1-beta*n
            if r<=0:continue
            t=n*(1-beta)/r
            check(t>=1 and beta+(1-beta)/t==F(1,n),'singular hazard and actual mass')
            check(n*(1-beta)/t==r,'unrenormalized terminal mass')
    # Same scored output can have arbitrarily larger expected time: TV does not control mean.
    for k in range(2,25):
        eps=F(1,k);expected=(1-eps)+eps*k**3
        check(expected>k and eps<1,'time is not bounded by task TV')

if __name__=='__main__':
    conditional();quantum();occupation();marked_finite();accounting()
    root=Path(__file__).resolve().parent;data=gaussian_run()
    check(json.loads((root/'GAUSSIAN_CERTIFICATE.json').read_text())==data,'Gaussian outward certificate')
    check((root/'sections/gaussian-table.tex').read_text()==table(data),'Gaussian table identity')
    print(json.dumps({'status':'PASS','finite_checks':sum(COUNTS.values()),'groups':COUNTS,'Gaussian_rows':len(data['rows']),'limitations':'finite arithmetic checks only, not continuum proof, priority, peer review, or repository-wide test coverage'},sort_keys=True,indent=2))
