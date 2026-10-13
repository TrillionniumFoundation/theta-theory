#!/usr/bin/env python3
"""Finite exact/floating diagnostics, never a substitute for continuum proofs.
All checks use explicit exceptions so python -O executes the identical suite.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import hashlib,json,math
import numpy as np
COUNTS=defaultdict(int)
DIGEST=hashlib.sha256()
def check(ok:bool,group:str,tag:str)->None:
    if not ok:raise RuntimeError(group+': '+tag)
    COUNTS[group]+=1;DIGEST.update((group+':'+tag+'\n').encode())
def close(a,b,tol=2e-10):return abs(a-b)<=tol*(1+abs(a)+abs(b))
# Positive binary observation followed by an affine positive transition.
PAR=((F(1,4),F(1,2),F(1,4)),(F(3,4),F(2,3),F(-1,6)))
def ell(a,y,x):return (1+PAR[a][0]*y*x)/2
def update(a,y,x):
    eta,beta,tau=PAR[a];return beta*(x+eta*y)/(1+eta*y*x)+tau
def g(x):return 3-x/3-x*x
@lru_cache(None)
def value(rem,x):
    if rem==0:return g(x)
    return min(qvalue(rem,a,x) for a in (0,1))
def qvalue(rem,a,x):return sum(ell(a,y,x)*value(rem-1,update(a,y,x)) for y in (-1,1))
def phi(a,x):return sum(ell(a,y,x)*update(a,y,x)**2 for y in (-1,1))
def bary(atoms):
    mass=defaultdict(F);moment=defaultdict(F)
    for p,x,s in atoms:mass[s]+=p;moment[s]+=p*x
    return {s:moment[s]/p for s,p in mass.items() if p}
def run_control(n,m,u0,mode,random_update):
    atoms=[(F(1),u0,0)];total=F(0)
    for t in range(1,n+1):
        qs=bary(atoms);next_atoms=[];rows=[];delta=F(0);pers=F(0)
        for p,x,s in atoms:
            q=qs[s];best=min((0,1),key=lambda a:qvalue(n-t+1,a,q))
            actions=[(best,F(1))] if mode==0 else ([(1-best,F(1))] if mode==1 else [(0,F(1,3)),(1,F(2,3))])
            for a,pa in actions:
                delta+=p*pa*(qvalue(n-t+1,a,q)-value(n-t+1,q))
                pers+=p*pa*(phi(a,x)-phi(a,q))
                for y in (-1,1):
                    prob=p*pa*ell(a,y,x);xx=update(a,y,x);w=update(a,y,q)
                    j=min(m-1,max(0,int((w+1)*m/2)))
                    outs=[(j,F(1))] if not random_update or m==1 else [(j,F(3,4)),((j+1)%m,F(1,4))]
                    for out,pj in outs:
                        pp=prob*pj;next_atoms.append((pp,xx,out));rows.append((pp,s,a,out,w))
        qnew=bary(next_atoms);mass=defaultdict(F);moment=defaultdict(F)
        for p,s,a,j,w in rows:mass[(s,a,j)]+=p;moment[(s,a,j)]+=p*w
        centers={key:moment[key]/p for key,p in mass.items() if p}
        row=sum(p*(w-centers[(s,a,j)])**2 for p,s,a,j,w in rows)
        pool=sum(p*(centers[(s,a,j)]-qnew[j])**2 for p,s,a,j,w in rows)
        r=sum(p*(x-qnew[j])**2 for p,x,j in next_atoms)
        jj=sum(p*(value(n-t,qnew[j])-value(n-t,w)) for p,s,a,j,w in rows)
        tag=f'n{n}-m{m}-u{u0}-a{mode}-rand{int(random_update)}-t{t}'
        check(sum(p for p,_,_ in next_atoms)==1,'rational_control',tag+' mass')
        for j in qnew:
            ptotal=sum(p for p,_,_,k,_ in rows if k==j)
            mean=sum(p*w for p,_,_,k,w in rows if k==j)/ptotal
            check(mean==qnew[j],'rational_control',tag+' calibration '+str(j))
        check(delta>=0 and jj>=0 and pers>=0 and row>=0 and pool>=0,'rational_control',tag+' nonnegative')
        check(r==pers+row+pool,'rational_control',tag+' three-defect')
        if mode==0:check(delta==0,'rational_control',tag+' Bellman action')
        total+=delta+jj;atoms=next_atoms
    qs=bary(atoms);risk=sum(p*g(qs[s]) for p,_,s in atoms)
    check(risk-value(n,u0)==total,'rational_control',tag+' telescope')

def exact_tests():
    for n,m,u0,mode,rnd in product(range(1,4),range(1,4),(F(-1,2),F(0),F(1,2)),range(3),(False,True)):
        run_control(n,m,u0,mode,rnd)
    # A finite common mass over all state/action choices: minima cannot escape
    # the common interval. This is not a discretization proof of the theorem.
    for eps in (F(1,8),F(1,2),F(7,8),F(1)):
        for f in product((F(-2),F(0),F(3)),repeat=3):
            z=(F(1,2),F(1,3),F(1,6));shared=eps*sum(z[i]*f[i] for i in range(3));lo=shared+(1-eps)*min(f);hi=shared+(1-eps)*max(f)
            vals=[min(shared+(1-eps)*f[(s+a)%3] for a in (0,1)) for s in range(3)]
            check(all(lo<=v<=hi for v in vals) and max(vals)-min(vals)<=(1-eps)*(max(f)-min(f)),'rational_span',str((eps,f)))
    # Delayed INDEX: no two-label randomized encoder beats the best partition.
    vertices=list(product((-1,1),repeat=2));best=None
    for mapping in product((0,1),repeat=4):
        err=F(0)
        for label in (0,1):
            cell=[vertices[i] for i,j in enumerate(mapping) if j==label]
            if cell:
                center=[sum(F(v[k]) for v in cell)/len(cell) for k in (0,1)]
                err+=sum(sum((F(v[k])-center[k])**2 for k in (0,1)) for v in cell)/4
        best=err if best is None else min(best,err)
    check(best==1,'rational_counterexamples','INDEX full vector MSE one')
    check(best/2==F(1,2),'rational_counterexamples','INDEX random coordinate MSE half')
    check((F(0)-F(1,2))**2/2+(F(1)-F(1,2))**2/2==F(1,4),'rational_counterexamples','incompatible Dirac rows')
    eta=lam=u=F(99,100)
    curvature=lam**2*(1-eta**2)**2*(1+3*eta**2*u**2)/(1-eta**2*u**2)**3
    check(curvature>24,'rational_counterexamples','C fails P holds')
    # Attained erasure / invisible-sign alternatives in the same task.
    for a,bias,delta in product((F(0),F(1,10),F(1,2),F(1)),(F(0),F(1,3),F(1,2),F(1)),(F(0),F(1,8),F(1,2))):
        mismatch=a*(bias/2+(1-bias)/2)
        bit_mse=a*(F(1,2)*1+F(1,2)*1)
        check(mismatch==a/2 and bit_mse==a,'rational_joint',str((a,bias,delta))+' deficiency and bit')
        for response in (-delta,F(0),delta):
            priorloss=((delta-response)**2+(-delta-response)**2)/2
            check(priorloss==delta**2+response**2,'rational_joint',str((a,bias,delta,response))+' sign')
    # Retained R32 passive lane count, never used as a controlled theorem.
    for n in range(1,20):
        for Q in range(2,80):
            M=Q+2*n+1;M0=1+(M-3)//2
            check(M0-n==Q//2 and F(M0-n)>=F(Q,3),'integer_passive','lane '+str((n,Q)))

def integer_tests():
    # Exact rational geometric allocation, including every smallest budget.
    for n in range(1,41):
        weights=[F(1,2)**(n-t) for t in range(1,n+1)];A=sum(weights)
        for k in range(1,121):
            widths=[1+int((k-1)*w/A) for w in weights];err=sum(w**3/F(m*m) for w,m in zip(weights,widths))
            check(1+sum(widths)<=n+k and widths[-1]<=k and err<=F(32,k*k),'integer_allocation',str((n,k)))
            if k>=3:
                costs=[1]*(n-1)+[4];Aw=sum(c*w for c,w in zip(costs,weights));B=k-3
                widths=[1+int(B*w/Aw) for w in weights];err=sum(w**3/F(m*m) for w,m in zip(weights,widths))
                check(1+sum(c*m for c,m in zip(costs,widths))<=n+1+k and err<=F(512,k*k),'integer_postcontrol',str((n,k)))
            else:
                check(n+2<=n+1+k,'integer_postcontrol','coarse '+str((n,k)))

def root(a):
    w,v=np.linalg.eigh(a);return (v*np.sqrt(w))@v.conj().T

def floating_tests():
    rng=np.random.default_rng(34011)
    for D in (2,3,4):
        for i in range(32):
            z=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));rho=z@z.conj().T+np.eye(D);rho/=np.trace(rho)
            z=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));H=(z+z.conj().T)/2;H-=np.trace(H)*np.eye(D)/D;H/=max(1,np.linalg.norm(H));eta=.31
            E=np.eye(D)+eta*H;K=root(E);sigma=K@rho@K;sigma/=np.trace(sigma)
            rp=root(rho);ri=np.linalg.inv(rp);B=ri@root(rp@sigma@rp)@ri;Einv=D*(B@B)/np.trace(B@B)
            check(np.linalg.norm(E-Einv)<2e-10,'floating_quantum',f'inverse {D} {i}')
            h=np.linalg.norm(H);lhs=np.linalg.norm(sigma-rho)
            check(lhs<=8*eta*h+1e-12,'floating_quantum',f'quiet {D} {i}')
    # Tetrahedral POVM, physical channel and weak effects: exact analytic sign
    # checked against finite symmetric quadrature (not a ball-integral proof).
    sig=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.array([[1,0],[0,-1]],complex)]
    tetra=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)/math.sqrt(3)
    coeff=np.array([.5,1/6,1/6,1/6]);t=1/16
    effects=[a*np.eye(2)+t*sum(v[j]*sig[j] for j in range(3)) for a,v in zip(coeff,tetra)]
    check(np.linalg.norm(sum(effects)-np.eye(2))<1e-12 and min(np.linalg.eigvalsh(E).min() for E in effects)>0,'floating_quantum','tetra positive complete')
    for eta,lam,z in product((.1,.7),(.2,.8),(-.4,.4)):
        r=z*tetra[0];rho=(np.eye(2)+sum(r[j]*sig[j] for j in range(3)))/2
        # axes form a spherical second-order design. Exact mean multiplier at
        # fixed radius is gamma=(1+2 sqrt(1-eta^2/2))/3.
        gamma=(1+2*math.sqrt(1-eta*eta/2))/3
        unselective=np.zeros((2,2),complex);masses=0.
        for j,sgn in product(range(3),(-1,1)):
            H=sgn*sig[j]/math.sqrt(2);K=root(np.eye(2)+eta*H);raw=K@rho@K
            unselective+=raw/6;masses+=np.trace(raw).real/6
        mean=np.array([np.trace(s@unselective).real for s in sig])
        check(abs(masses-1)<1e-12 and np.linalg.norm(mean-gamma*r)<1e-12,'floating_quantum',str((eta,lam,z))+' mean')
        difference=-(4*t/3)*lam*float(np.dot(tetra[0],mean))
        target=-(4*t/3)*lam*gamma*float(np.dot(tetra[0],r))
        check(close(difference,target) and difference*z<0,'floating_quantum',str((eta,lam,z))+' strict switch')
    cost=.009*(math.sqrt(3)+1)/math.sqrt(2);prior=.01*math.sqrt(2)
    mills=math.exp(-12.5)/(5*math.sqrt(2*math.pi));tau=1e-6/math.sqrt(2*math.pi)
    rowerror=2*math.sqrt(2)*mills+6*tau
    check(rowerror<4e-6 and cost-2*rowerror>prior,'floating_gaussian','explicit expansive W1')
    p=np.array([.5,.25,.25]);gap=2*(p[0]-p[1])*p[2]**2/((1-p[0])*(1-p[1]))*.9**2
    check(close(gap,.0675) and gap>1e-5,'floating_gaussian','strict feedback margin')
    Lambda=28*math.exp(4)/math.sqrt(2*math.pi);eps=math.exp(-(2+math.log(21))**2/8)/math.sqrt(2*math.pi)
    check(Lambda<610 and 0<eps<1,'floating_benchmark','density overlap constants')
    for q in np.linspace(.25,.75,21):
        for y in (-100,-3,0,3,100):
            s=1/(1+(1-q)/q*math.exp(-2*y));der=.5*s*(1-s)/(q*(1-q))
            check(der<=2/3+1e-12,'floating_benchmark',f'derivative {q} {y}')
    check(close((2/3)**2/40+(2/3)/80+1/120,1/36),'floating_benchmark','three-step error')
    check(9+10*19+20*29==779 and 1+10+20+30==61,'integer_benchmark','threshold and state counts')

def main():
    exact_tests();integer_tests();floating_tests()
    print(json.dumps({'status':'PASS','native_cases':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),'check_sequence_sha256':DIGEST.hexdigest(),'normal_optimized_policy':'explicit exceptions, no assert-based checks','limitations':'finite rational/integer identities and floating diagnostics only; neither continuum proof nor numerical priority/novelty certificate; nested inherited suites are counted separately'},sort_keys=True,indent=2))
if __name__=='__main__':main()
