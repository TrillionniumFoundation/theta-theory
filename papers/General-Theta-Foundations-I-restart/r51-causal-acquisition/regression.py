#!/usr/bin/env python3
"""Exact finite regressions and independent arithmetic certificates.
These are not proofs of the continuum statements. No test relies on assert,
so ordinary and python -O execution enforce the same checks.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
COUNT=0
GROUP={}

def check(condition:bool,message:str):
    global COUNT
    if not condition:raise RuntimeError(message)
    COUNT+=1

def group(name,fn):
    old=COUNT;fn();GROUP[name]=COUNT-old

def occupation():
    laws=[[F(1,4),F(1,2),F(1,4)],[F(1,2),F(1,4),F(1,4)]]
    losses=[F(0),F(1,4),F(1)];costs=[F(1),F(2)]
    for p in (F(1,4),F(1,2),F(3,4)):
        probs=[p,1-p]
        for flat in product((F(0),F(1,2),F(1)),repeat=6):
            acc=[flat[:3],flat[3:]]
            s=sum(probs[a]*sum(laws[a][i]*acc[a][i] for i in range(3)) for a in range(2))
            if not s:continue
            x=[z/s for z in probs];h=[[x[a]*acc[a][i] for i in range(3)] for a in range(2)]
            mass=sum(sum(laws[a][i]*h[a][i] for i in range(3)) for a in range(2))
            N=sum(costs[a]*x[a] for a in range(2))
            risk=sum(sum(laws[a][i]*h[a][i]*losses[i] for i in range(3)) for a in range(2))
            check(mass==1 and sum(x)==1/s,'occupation and terminal mass')
            check(all(0<=h[a][i]<=x[a] for a in range(2) for i in range(3)),'domination')
            for z in (F(1,4),F(1,2),F(1),F(2)):
                lam=max(sum(laws[a][i]*max(z-losses[i],0) for i in range(3))/costs[a] for a in range(2))
                check(z-lam*N<=risk,'common dual lower')
    # Inaccessible circulating mass cannot be called acquired.
    check(F(1)+F(3)-F(3)==1,'phantom subtraction witness')

def support_reduction():
    weights=[F(1,3)]*3
    for c in product((F(1),F(2),F(4)),repeat=3):
      N=sum(c[i]*weights[i] for i in range(3))
      for e in product((F(0),F(1,3),F(1)),repeat=3):
        original=sum(e[i]*weights[i] for i in range(3));candidates=[]
        for i in range(3):
            if c[i]<=N:candidates.append(e[i])
        for i in range(3):
          for j in range(i+1,3):
            if c[i]==c[j]:continue
            w=(N-c[j])/(c[i]-c[j])
            if 0<=w<=1:candidates.append(w*e[i]+(1-w)*e[j])
        check(bool(candidates) and min(candidates)<=original,'two-action extremal reduction')

def perturbation():
    for p,p2 in product([F(i,10) for i in range(1,10)],repeat=2):
      for u0,u1 in product((F(0),F(1,4),F(1,2),F(1)),repeat=2):
        s=(1-p)*u0+p*u1
        if s==0:continue
        sp=(1-p2)*u0+p2*u1;d=max(s-sp,0);N=1/s
        rho=d/(1-sp) if d else F(0)
        v0=u0+rho*(1-u0);v1=u1+rho*(1-u1)
        spp=(1-p2)*v0+p2*v1
        check(spp>=s and 1/spp<=N,'same-budget repair')
        for r in (F(0),F(1,2),F(1)):
            risk=((1-p)*u0*r*r+p*u1*(1-r)**2)/s
            risk2=((1-p2)*v0*r*r+p2*v1*(1-r)**2)/spp
            check(risk2<=risk+2*N*abs(p-p2),'linear repaired loss')

def gaussian_balance():
    for k,a,b in product((F(0),F(1,2),F(1),F(4),F(10)),[F(i,10) for i in range(1,10)],[F(i,10) for i in range(1,10)]):
        q=1/(2*(k+1));D=a+b+2*k*a*b;t=(2+k*(a+b))/D;m=(a-b)/D
        vp=(t-k*m)/2;vm=(t+k*m)/2
        check(vp>0 and vm>0 and a*vp+b*vm==1,'Gaussian actual terminal mass')
        check(vp==F(1,2)+(1-q)*(1-a)*vp+q*(1-b)*vm,'Gaussian plus balance')
        check(vm==F(1,2)+q*(1-a)*vp+(1-q)*(1-b)*vm,'Gaussian minus balance')
        check(a*vp-b*vm==m and t>=1,'Gaussian moment identities')
    neg=[F(4,10),F(3,10),F(2,10),F(1,10)];pos=list(reversed(neg))
    for u in product((F(0),F(1,2),F(1)),repeat=4):
        b=sum(neg[i]*u[i] for i in range(4));a=sum(pos[i]*u[i] for i in range(4))
        remaining=b;A=F(0)
        for i in (3,2,1,0):
            take=min(remaining,neg[i]);remaining-=take;A+=take*pos[i]/neg[i]
        check(A>=a and remaining==0,'discrete likelihood-ratio dominance')
    beta=F(49,50)**2*F(27,10)*F(1,2)/F(1077,1000)**3
    check(beta==F(48020000,46268279) and beta>1,'strict curvature failure witness')
    for a in (F(1,4),F(1,2),F(3,4)):
        for p,v in product((F(1,4),F(1,2),F(3,4)),(F(1,8),F(1,4))):
            phi=lambda x:a*(x*x+(1-x)**2)+(1-a)*F(1,2)
            check(phi(p+v)+phi(p-v)-2*phi(p)==4*a*v*v,'hold-reset curvature')

def singular():
    for b in (F(1,32),F(1,16),F(1,8),F(1,2),F(1)):
      for N in (F(1),F(65,64),F(17,16),F(8,7),F(2),F(4)):
        r=max(1-N*(1-b),0)
        if not r:
            check(b<1 and 1/(1-b)<=N,'zero-risk actual mass threshold');continue
        ell=r/(N*b);check(0<ell<=1,'admissible continuous interval')
        if b<=F(1,8):
            first=r*(1+ell/2);second=r*(1+ell+ell*ell/3)
            risk=second-first*first
            check(0<=risk<=second and first<F(1,2),'single-center actual moments')
        for m in range(2,9):
            lower=r**3/(12*(N*b)**2*m*m);upper=r**3/(12*(N*b)**2*(m-1)**2)
            l=r/(N*b*(m-1));direct=(m-1)*(N*b)*l**3/12
            check(direct==upper and 0<lower<=upper,'continuous cell moments and label allocation')
    for M in range(9,100):
        m=(M-1)//4
        check(1+4*m<=M and m-1>=F(M,16),'joint total-state count')

def raw_kernels():
    for eta,x in product((F(0),F(1,3),F(3,4)),(F(-1,2),F(-1,4),F(0),F(1,4),F(1,2))):
        ys=(F(-1,2),F(0),F(1,2));nu=(F(1,4),F(1,2),F(1,4))
        likelihood=[1+4*eta*x*y for y in ys]
        check(sum(nu[i]*likelihood[i] for i in range(3))==1,'classical normalized row')
        check(all(1-eta<=v<=1+eta for v in likelihood),'classical envelope')
        pm=(x*x+F(1,2)-x)/2;pp=(x*x+F(1,2)+x)/2;p0=F(1,2)-x*x
        check(pm+pp+p0==1 and min(pm,pp,p0)>=0,'classical audit probabilities')
        check(pp-pm==x and pp+pm-x*x==F(1,2),'classical audit mean variance')
    # Exact six-direction Bloch second-design moments, a finite identity check
    # for the general Haar second-moment proof, not a substitute for it.
    dirs=[tuple(F(s) if k==j else F(0) for k in range(3)) for j in range(3) for s in (-1,1)]
    for i,j in product(range(3),repeat=2):
        check(sum(v[i]*v[j] for v in dirs)/6==(F(1,3) if i==j else 0),'quantum second moments')
    for i in range(3):check(sum(v[i] for v in dirs)==0,'quantum centering')
    for e in (F(0),F(1,4),F(1,2),F(1)):
        check(e/F(2)==(1-e)*0+e*F(1,2),'attained erasure deficiency')


def main():
    for name,fn in [('actual_action_occupation_and_dual',occupation),('two_action_reduction',support_reduction),
        ('linear_same_budget_repair',perturbation),('gaussian_balance_and_stability_separation',gaussian_balance),
        ('singular_mass_and_memory',singular),('raw_kernel_and_audit_identities',raw_kernels)]:group(name,fn)
    out=subprocess.check_output([sys.executable,str(ROOT/'gaussian_certificate.py')],text=True)
    cert=json.loads(out)
    check(cert['status']=='PASS' and len(cert['rows'])==3,'Gaussian interval certificate')
    print(json.dumps({'status':'PASS','exact_finite_checks':COUNT,'groups':GROUP,
                      'gaussian_certificate_sha256':hashlib.sha256((ROOT/'GAUSSIAN_CERTIFICATE.json').read_bytes()).hexdigest(),
                      'gaussian_rows':[{k:r[k] for k in ('N','h_enclosure','optimum_risk','checkpoint_2_risk','checkpoint_4_risk')} for r in cert['rows']],
                      'limitations':'finite identities and certified arithmetic only; continuum proofs and priority require independent mathematical review'},sort_keys=True,indent=2))
if __name__=='__main__':main()
