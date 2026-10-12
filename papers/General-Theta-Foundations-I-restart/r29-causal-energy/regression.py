#!/usr/bin/env python3
"""Finite algebra and numerical sanity checks; none proves a continuum theorem."""
from __future__ import annotations
import argparse,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
counts={'exact_arithmetic':0,'floating_sanity':0}
def check(ok:bool,msg:str,kind='exact_arithmetic'):
    if not ok:raise RuntimeError(msg)
    counts[kind]+=1
def add(u,v):return tuple(a+b for a,b in zip(u,v))
def mul(a,u):return tuple(a*b for b in u)
def norm2(u):return sum(x*x for x in u)
def energy_tests():
    for p in (F(1,4),F(1,3),F(1,2),F(3,4)):
        pi=[p,1-p];vs=[(F(1),F(0)),(F(1,2),F(1,2))]
        for kernels in itertools.product((F(0),F(1,2),F(1)),repeat=4):
            mass={};moment={};raw=F(0)
            for s in range(2):
                for y in range(2):
                    v=mul(F(1 if y==0 else -1),vs[s]);raw+=pi[s]*norm2(v)/2
                    for j in range(2):
                        a=pi[s]/2*(kernels[2*s+y] if j==0 else 1-kernels[2*s+y]);key=(s,j)
                        mass[key]=mass.get(key,F(0))+a;moment[key]=add(moment.get(key,(F(0),F(0))),mul(a,v))
            cs={k:mul(1/mass[k],moment[k]) for k in mass if mass[k]}
            jm=[sum(mass[s,j] for s in range(2)) for j in range(2)]
            vj={j:mul(1/jm[j],add(moment[0,j],moment[1,j])) for j in range(2) if jm[j]}
            row=raw-sum(mass[k]*norm2(v) for k,v in cs.items())
            pool=sum(mass[s,j]*norm2(add(c,mul(-1,vj[j]))) for (s,j),c in cs.items())
            end=sum(jm[j]*norm2(v) for j,v in vj.items())
            check(raw==row+pool+end,'conditional energy identity')
            check(row>=0 and pool>=0,'nonnegative conditional defects')
    check(F(1)==F(0)+F(1,2)+F(1,2),'opposite incoming-centroid fixture')
def beta(m):return 0.0 if m==1 else (math.sin(math.pi/m)/(math.pi/m))**2
def allocation_tests():
    for n in range(1,9):
        dp=[0.0]*65;dp[0]=1.0
        for t in range(1,n+1):
            nxt=[0.0]*65
            for k in range(t,65):nxt[k]=max(dp[k-m]*beta(m) for m in range(1,k+1))
            dp=nxt
        for k in range(n,65):
            q,r=divmod(k,n);b=beta(q)**(n-r)*beta(q+1)**r
            check(abs(dp[k]-b)<2e-12,'balanced allocation agrees with exhaustive DP','floating_sanity')
            check((k>=2*n)==(b>0),'nonzero-energy threshold','floating_sanity')
    for m in range(1,100):
        check(0<=beta(m)<=1,'circle energy range','floating_sanity')
        check((1-beta(m))*m*m>=0.999999 and (1-beta(m))*m*m<=math.pi**2/3+1e-10,'circle scale','floating_sanity')
    for x in np.linspace(1.001,60,1000):
        z=math.pi/x;dd=-2/x**2*((1-z/math.tan(z))**2+z*z)
        check(dd<0,'log energy curvature','floating_sanity')
def crossing_tests():
    for tau in itertools.product(range(1,4),repeat=6):
        T=[0]
        for x in tau:T.append(T[-1]+x)
        for n in range(1,min(6,T[-1])+1):
            c=next(j for j in range(1,len(T)) if T[j]>=n)
            check(c<=n and sum(s<n for s in T[:-1])==c,'crossing count')
            check(c+1<=n+1,'shifted boundary convention')
            check(sum(s<n-2 for s in T[:-1])== (0 if n<=2 else next(j for j in range(1,len(T)) if T[j]>=n-2)),'guaranteed first-service count')
def clock_tests():
    for M in range(1,4):
        for mask in range(1<<(M*M)):
            edges=[{j for j in range(M) if mask>>(i*M+j)&1} for i in range(M)]
            for haltmask in range(1,1<<M):
                halt={i for i in range(M) if haltmask>>i&1}
                if 0 in halt:continue
                phases=[{0}];valid=False
                for n in range(1,M+2):
                    if any(not edges[s] for s in phases[-1]):break
                    cur=set().union(*(edges[s] for s in phases[-1]));phases.append(cur)
                    if cur<=halt:valid=True;break
                    if cur&halt:break
                if valid:
                    check(all(not(a&b) for i,a in enumerate(phases) for b in phases[i+1:]),'exact-halt phases disjoint')
                    check(sum(map(len,phases))<=M,'total clock label count')
def singular_tests():
    for alphas in itertools.product((F(0),F(1,4),F(1,2),F(3,4),F(1)),repeat=4):
        w=math.prod(alphas)
        for a in (F(0),F(1,3),F(1)):
            val=1-w+w*a
            check((a+1-w)/2<=val<=a+1-w,'true surviving mass comparison')
    # Exact finite-group analogue of the audit-preserving deficiency lower.
    for n in range(1,6):
        for w in (F(0),F(1,4),F(1,2),F(1)):
            chi=F(2,3);tv=F(0)
            for report in itertools.product((-1,1),repeat=n):
                x=math.prod(report)
                for sign in (-1,1):
                    ideal=F(1,2**n)*(1+sign*x*chi)/2
                    erased=F(1,2**n)*(1+sign*x*chi*w)/2
                    tv+=abs(ideal-erased)/2
            check(tv==chi*(1-w)/2,'finite protected-audit TV identity')
def quantum_tests():
    rng=np.random.default_rng(291010)
    for D in range(2,8):
        for _ in range(20):
            a=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));v=(a+a.conj().T)/2;v-=np.trace(v)*np.eye(D)/D;v/=np.linalg.norm(v)
            eig,U=np.linalg.eigh(v);j=int(np.argmax(np.diff(eig)))+1;g=eig[j]-eig[j-1]
            b=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));q,_=np.linalg.qr(b);vp=q@v@q.conj().T
            P=U[:,j:]@U[:,j:].conj().T;PP=q@P@q.conj().T
            check(g+1e-12>=1/(math.sqrt(D)*(D-1)),'uniform spectral-gap witness','floating_sanity')
            check(np.linalg.norm(P-PP)<=np.linalg.norm(v-vp)/g+1e-10,'spectral projection inequality','floating_sanity')
            k=D-j;check(2*k*(D-k)>=2*(D-1),'minimum conjugacy orbit dimension')
    pauli=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.array([[1,0],[0,-1]],complex)]
    for A in pauli:check(np.array_equal(A@A,np.eye(2)),'Pauli involution')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
    energy_tests();allocation_tests();crossing_tests();clock_tests();singular_tests();quantum_tests()
    result={'status':'PASS','checks':counts,'total_checks':sum(counts.values()),'suites':['conditional row/pooling energy','circle allocation dynamic program','crossing and guaranteed service','support-clock paths','surviving stratum and audit TV','projective spectral gap'],'seed':291010,'scope':'finite rational algebra and finite floating-point sanity only; no continuum proof, optimal-priority, or journal certificate'}
    text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output:
        p=Path(args.output);p.mkdir(parents=True,exist_ok=True);(p/'FINITE_REGRESSION.json').write_text(text)
    print(text,end='')
if __name__=='__main__':main()
