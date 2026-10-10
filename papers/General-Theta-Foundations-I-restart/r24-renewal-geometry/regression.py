#!/usr/bin/env python3
"""Exact finite renewal/defect arithmetic and finite matrix checks, not proofs."""
from __future__ import annotations
import argparse,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
COUNT=0
def check(ok,message):
    global COUNT
    COUNT+=1
    if not ok:raise RuntimeError(message)
def distribution(e,L):return [(1-e,(F(0),F(0))),(e,tuple([F(0)]+[F(1)]*L))]
def cycle_value(dist):
    mu=sum(p*len(c) for p,c in dist);r=sum(p*sum(c) for p,c in dist)
    return mu,r,r/mu
def cumulative(dist,N):
    ans=[F(0)]
    for n in range(1,N+1):
        v=sum(p*sum(c[:n]) for p,c in dist)
        v+=sum(p*ans[n-len(c)] for p,c in dist if len(c)<=n)
        ans.append(v)
    return ans
def discount(dist,b):
    numerator=(1-b)*sum(p*sum(b**t*x for t,x in enumerate(c)) for p,c in dist)
    return numerator/(1-sum(p*b**len(c) for p,c in dist))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args();examples=[]
    for L in (1,2,3,5,12,24):
        for e in (F(0),F(1,20),F(1,4),F(1,2),F(1)):
            dist=distribution(e,L);mu,r,g=cycle_value(dist);C=cumulative(dist,40)
            check(mu==2+e*(L-1),'cycle mean');check(r==e*L,'cycle reward')
            K=sum(p*len(c)**2 for p,c in dist)
            for n in range(1,41):
                tail=sum(sum(p*max(len(c)-s,0) for p,c in dist) for s in range(n+1))
                check(abs(C[n]-n*g)<=tail,'renewal overshoot bound')
                check(abs(C[n]/n-g)<=K/n,'second-moment bound')
                check(F(0)<=C[n]/n<=1,'unit finite risk')
            for b in (F(1,4),F(1,2),F(3,4),F(9,10)):
                j=discount(dist,b)
                check(j==e*b*(1-b**L)/(1-(1-e)*b*b-e*b**(L+1)),'discount cycle formula')
                check(abs(j-g)<=K*(1-b),'second-moment discount bound')
            examples.append({'L':L,'e':str(e),'mu':str(mu),'average':str(g),'discount_half':str(discount(dist,F(1,2)))})
    for n in (1,2,3,5,10):
        L=12*n;e=F(1,L*L);dist=distribution(e,L);mu,r,g=cycle_value(dist)
        check(cumulative(dist,n)[n]/n<=g/4,'sharp finite scale')
        check(sum(p*len(c)**2 for p,c in dist)<=8,'uniform moment witness')
    for denominator in (2,4,8,16):
        b=1-F(1,denominator);L=12*denominator;e=F(1,L*L);dist=distribution(e,L)
        check(discount(dist,b)<=cycle_value(dist)[2]/4,'sharp discount scale')
    for L in (1,2,4,8,20):
        for e in (F(1,20),F(1,5),F(1,2)):
            mu=2+e*(L-1);eps=e/2;risk=e*L/(4*mu)
            K=max(F(4),(1-e)*4+e*(L+1)**2)
            check(float(risk)<=4*float(K)**0.5*float(eps)**0.5+1e-14,'Holder defect check')
            for theta in (0,1):
                wrong=e*F(1,2)
                check(wrong==eps,'actual erasure deficiency')
                for delta in (F(0),F(1,10),F(1,2)):
                    a=(mu-1)/mu
                    total=risk+a*delta*delta
                    check(total>=risk,'calibration positive')
                    check(total-risk==a*delta**2,'calibration occupied mass')
    # Tail-dependent ratio bound against all pairs in a finite cycle family.
    family=[distribution(e,L) for L in (1,3,8) for e in (F(0),F(1,4),F(1,2))]
    for d1 in family:
        for d2 in family:
            p1={};p2={}
            for p,c in d1:p1[c]=p1.get(c,F(0))+p
            for p,c in d2:p2[c]=p2.get(c,F(0))+p
            tv=sum(abs(p1.get(c,F(0))-p2.get(c,F(0))) for c in set(p1)|set(p2))/2
            gap=abs(cycle_value(d1)[2]-cycle_value(d2)[2])
            for T in (1,2,4,8,12):
                a=max(sum(p*max(len(c)-T,0) for p,c in d) for d in (d1,d2))
                check(gap<=min(F(1),2*T*tv+4*a),'truncated ratio defect')
    for den in (3,5,7):
        for x in range(den+1):
            for y in range(den-x+1):
                row=[F(x,den),F(y,den),F(den-x-y,den)]
                for Q in (2,4,8):
                    rounded=[F((row[i]*Q).numerator//(row[i]*Q).denominator,Q) for i in range(2)]
                    rounded.append(1-sum(rounded))
                    check(sum(rounded)==1 and min(rounded)>=0,'rounded simplex')
                    check(sum(abs(a-b) for a,b in zip(row,rounded))/2<=F(3,Q),'row TV allowance')
    # Uniform scalar quantization, plus actual occupation length bias.
    for M in range(1,25):
        distortion=sum(F(1,12*M**3) for _ in range(M))
        check(distortion==F(1,12*M*M),'uniform quantization integral')
    # L=1 on left half and 3 on right; mu=3, occupied mean is 5/8, not 1/2.
    mass=F(2,3);first=(F(1,8)+3*F(3,8))/3
    check(first/mass==F(5,8),'length-biased occupation mean')
    exact_checks=COUNT
    # Finite 2x2 matrix identities. These are numerical diagnostics only.
    I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
    basis=[X,Y,Z]
    effects=[(I+s*0.25*H)/6 for H in basis for s in (-1,1)]
    def sqrt_pos(A):
        w,v=np.linalg.eigh(A);return (v*np.sqrt(np.maximum(w,0)))@v.conj().T
    roots=[sqrt_pos(A) for A in effects]
    check(np.linalg.norm(sum(effects)-I)<1e-12,'POVM normalization')
    for H in basis:
        rho=(I+0.6*H)/2
        out=sum(A@rho@A.conj().T for A in roots)
        check(abs(np.trace(out)-1)<1e-12,'audit backaction trace')
        check(np.linalg.eigvalsh(out).min()>-1e-12,'audit backaction positive')
        for J in basis:
            sigma=(I+0.2*J)/2
            out2=sum(A@sigma@A.conj().T for A in roots)
            check(np.linalg.norm(out-out2,ord='nuc')<=np.linalg.norm(rho-sigma,ord='nuc')+1e-12,'trace norm nonexpansion')
    for a in (-0.1,0,0.1):
        E=I+a*X+0.05*Z;A=sqrt_pos(E);rho=I/2
        report=A@rho@A.conj().T
        check(np.linalg.norm(report-E/2)<1e-12,'raw affine quantum load')
        check(abs(np.trace(report)-1)<1e-12,'uniform report trace')
    result={'status':'PASS','checks':COUNT,'exact_rational_checks':exact_checks,'finite_matrix_checks':COUNT-exact_checks,'cycle_examples':len(examples),'ordinary_optimized_invariant':True,'scope':'finite arithmetic and matrix diagnostics; not a proof of continuum theorems'}
    if args.output:
        out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
        (out/'renewal_certificate.json').write_text(json.dumps({'summary':result,'examples':examples},sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
