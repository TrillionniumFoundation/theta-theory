#!/usr/bin/env python3
"""Independent exact-arithmetic diagnostics for A1 v15 (standard library only).

These finite checks are not a proof of the uniform theorem. No author helpers,
archived test outputs, or author test suites are imported. Run:
    python3 reproduce_review.py --output EXECUTION.json
The reviewed source is e1d0ff2ef04a8641ac77923b664c4d3e8386f212.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
from typing import NamedTuple

class Q(NamedTuple):
    re: F = F(0)
    im: F = F(0)
    def __add__(self, b):
        b = cq(b); return Q(self.re + b.re, self.im + b.im)
    __radd__ = __add__
    def __neg__(self): return Q(-self.re, -self.im)
    def __sub__(self,b): return self + (-cq(b))
    def __rsub__(self,b): return cq(b) + (-self)
    def __mul__(self,b):
        b=cq(b); return Q(self.re*b.re-self.im*b.im, self.re*b.im+self.im*b.re)
    __rmul__=__mul__
    def __truediv__(self,b):
        b=cq(b); d=b.re*b.re+b.im*b.im
        if d == 0: raise ZeroDivisionError('Gaussian rational division by zero')
        return Q((self.re*b.re+self.im*b.im)/d,(self.im*b.re-self.re*b.im)/d)
    def conj(self): return Q(self.re,-self.im)
    def abs2(self): return self.re*self.re+self.im*self.im

def cq(x): return x if isinstance(x,Q) else Q(F(x),F(0))
ZERO, ONE, II = Q(), Q(F(1)), Q(F(0),F(1))
checks=Counter()
negative_controls=[]

def check(group, condition):
    checks[group]+=1
    if not condition: raise AssertionError(f'{group}: assertion {checks[group]} failed')

def mul(a,b):
    c={}
    for i,x in a.items():
        for j,y in b.items(): c[i+j]=c.get(i+j,ZERO)+x*y
    return c

def product(zs,t):
    p={0:ONE}
    for z in zs: p=mul(p,{-1:t*z.conj(),0:ONE,1:t*z})
    return p

def elementary(zs):
    e=[ONE]+[ZERO]*len(zs)
    for z in zs:
        for j in range(len(zs),0,-1): e[j]=e[j]+z*e[j-1]
    return e

def rank(a):
    a=[list(row) for row in a]; r=0
    if not a: return 0
    for j in range(len(a[0])):
        k=next((i for i in range(r,len(a)) if a[i][j]),None)
        if k is None: continue
        a[r],a[k]=a[k],a[r]; v=a[r][j]
        a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                v=a[i][j]; a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    return r

def normalized_jacobian(zs,t):
    n=len(zs); cols=[]
    if not t:
        for i in range(n):
            e=elementary(zs[:i]+zs[i+1:])
            for dz in (ONE,II):
                col=[]
                for j in range(1,n+1):
                    q=dz*e[j-1]; col.extend([q.re,q.im])
                cols.append(col)
    else:
        p=product(zs,t); den=p[0]
        for i in range(n):
            base=product(zs[:i]+zs[i+1:],t)
            for dz in (ONE,II):
                dp=mul(base,{-1:t*dz.conj(),1:t*dz})
                col=[]
                for j in range(1,n+1):
                    q=(dp.get(j,ZERO)*den-p.get(j,ZERO)*dp.get(0,ZERO))/(den*den*t**j)
                    col.extend([q.re,q.im])
                cols.append(col)
    return [[col[i] for col in cols] for i in range(2*n)]

def physical_interface():
    # Verify the actual four-cell command map at exact unit-circle points.
    eta=F(1,8)
    angles=[ONE,-ONE,II,-II,Q(F(3,5),F(4,5))]
    zs=[Q(F(0)),Q(F(1,64),F(-1,80)),Q(F(-1,48),F(1,56))]
    for z in zs:
        u=[F(1,2)+2*z.re,F(1,2)-2*z.re,F(1,2)-2*z.im,F(1,2)+2*z.im]
        a=sum(u)/4
        check('command_cube',all(eta<=v<=1-eta for v in u))
        check('command_right_inverse',a==F(1,2) and Q(u[0]-u[1],-(u[2]-u[3]))/(8*a)==z)
        for t in (F(0),F(1,64),F(1,8),F(1,2)):
            for w in angles:
                cells=[(1+t*w.re)/4,(1-t*w.re)/4,(1+t*w.im)/4,(1-t*w.im)/4]
                check('detector_normalization',sum(cells)==1)
                check('physical_likelihood_lower_bound',all((1-v)*k>=eta/8 for v,k in zip(u,cells)))
                failure=sum(v*k for v,k in zip(u,cells))
                claimed=a*(ONE+t*(z*w+z.conj()*w.conj()))
                check('physical_failure_factor',claimed==Q(failure) and failure>=eta)


def physical_metric():
    # Exact n=m=1 discrete Fourier identity via reduction modulo w^L-1.
    # General finite Fourier orthogonality is checked by the integer
    # congruence criterion (not floating-point trigonometry).
    zs=[Q(F(1,32),F(-1,48)),Q(F(-1,40),F(1,56)),Q(F(1,64),F(1,72))]
    zt=[Q(F(-1,36),F(1,44)),Q(F(1,52),F(-1,60)),Q(F(1,68),F(-1,76))]
    rho=F(1,64)
    for n in range(1,4):
        for t in (F(0),F(1,64),F(1,8),F(1,2)):
            p=product(zs[:n],t); pp=product(zt[:n],t)
            check('posterior_reality',p[0].im==0)
            check('evidence_lower_bound',p[0].re >= (1-t)**n)
            for j in range(-n,n+1):
                check('hermitian_coefficients',p[j]==p[-j].conj())
            for m in range(1,6):
                b=[]
                for j in range(m+1):
                    s=F(0)
                    for h in range((m-j)//2+1):
                        coeff=math.factorial(m)//(math.factorial(j+h)*math.factorial(h)*math.factorial(m-j-2*h))
                        s+=coeff*rho**(j+2*h)*t**(2*h)
                    b.append(s)
                query=product([Q(rho)]*m,t)
                for j in range(m+1):
                    check('query_B_coefficients',query.get(j,ZERO)==Q(t**j*b[j]))
                # Difference as a Laurent polynomial in the phase variable.
                phase={}
                for j in range(1,m+1):
                    dc=p.get(j,ZERO)/p[0]-pp.get(j,ZERO)/pp[0]
                    v=F(1,2**m)*b[j]*t**j*dc
                    phase[j]=v; phase[-j]=v.conj()
                square=mul(phase,phase); L=2*m+1
                averaged=sum((v for a,v in square.items() if a%L==0),ZERO)
                rhs=sum((F(2,2**(2*m))*b[j]**2*(t**j*(p.get(j,ZERO)/p[0]-pp.get(j,ZERO)/pp[0])).abs2() for j in range(1,m+1)),F(0))
                check('exact_discrete_Parseval',averaged==Q(rhs))
                for a in range(-2*m,2*m+1):
                    check('phase_no_aliasing',(a%L==0)==(a==0))
    # n=m=1: physical query displacement contains two, not one, factors t.
    t=F(1,8); z=zs[0]; zp=zt[0]
    good=rho**2*t**4*(z-zp).abs2()/2
    wrong=rho**2*t**2*(z-zp).abs2()/2
    check('negative_control_missing_acquisition',good!=wrong)
    negative_controls.append({'mutation':'omit acquisition attenuation in n=m=1','detected':True,'wrong_over_correct':str(wrong/good)})

def weighted_updates():
    new=Q(F(1,10),F(-1,14))
    zs=[Q(F(i+1,80),F((-1)**i,96)) for i in range(5)]
    mutation_hits=Counter()
    for n in range(0,6):
        for t in (F(0),F(1,64),F(1,8),F(1,2)):
            p=product(zs[:n],t); pn=product(zs[:n]+[new],t)
            y={j:t**j*p.get(j,ZERO)/p[0] for j in range(n+3)}
            den=ONE+new*y[1].conj()+new.conj()*y[1]
            check('update_denominator_positive',den.im==0 and den.re>=1-t)
            check('exact_evidence_ratio',den==pn[0]/p[0])
            for j in range(1,n+2):
                num=y[j]+t*t*new*y[j-1]+new.conj()*y[j+1]
                expected=t**j*pn.get(j,ZERO)/pn[0]
                check('exact_weighted_update',num/den==expected)
                if (y[j]+new*y[j-1]+new.conj()*y[j+1])/den!=expected: mutation_hits['omit_tau_squared']+=1
                if num!=expected: mutation_hits['omit_evidence_denominator']+=1
            evidence=p[0]/(2**n)
            check('actual_all_failure_evidence',evidence.im==0 and 0<evidence.re<=1)
    for name,hits in sorted(mutation_hits.items()):
        check('negative_controls_update',hits>0)
        negative_controls.append({'mutation':name,'detected':True,'counterchecks':hits})

def flags_and_volumes():
    for n in range(1,6):
        zs=[Q(F(i+1,128)) for i in range(n)]
        for t in (F(0),F(1,64),F(1,8),F(1,2)):
            jac=normalized_jacobian(zs,t)
            for k in range(1,n+1): check('normalized_flag_exact_rank',rank(jac[:2*k])==2*k)
        # Repeated central roots are a negative control for the Jacobian,
        # not a counterexample to the distinct-root lemma.
        if n>=2:
            repeated=normalized_jacobian([Q(F(1,128))]*n,F(0))
            check('negative_control_collapsed_roots',rank(repeated)<2*n)
    negative_controls.append({'mutation':'replace distinct central roots by repeated roots','detected':True})
    for k in range(1,9):
        exponents=[2*j for j in range(1,k+1) for _ in range(2)]
        for j in range(1,k+1):
            check('paired_exterior_exponents',F(2*sum(exponents[:2*j]),2*j)==2*(j+1))
        for j in range(2,k+1):
            l=2*j-1; w=F(j-1,2*j-1)
            # Both coefficients (log tau and log M) match the convex combination.
            for a in (exponents,[F(-1)]+[F(0)]*(2*k-1)):
                mid=F(2*sum(a[:l]),l)
                left=F(2*sum(a[:l-1]),l-1)
                right=F(2*sum(a[:l+1]),l+1)
                check('odd_axis_convex_combination',mid==w*left+(1-w)*right)
        for j in range(1,k):
            logM=2*j*(j+1)
            # tau=exp(-1), M=exp(logM), so log term = -2(h+1)-logM/h.
            values=[F(-2*(h+1))-F(logM,h) for h in range(1,k+1)]
            check('adjacent_phase_exact_crossing',values[j-1]==values[j])
            check('adjacent_phase_global_envelope',values[j-1]==max(values))

def bounded_dual():
    # Nonconstant likelihood: normalization of the prior matters.
    support=[F(i,4) for i in range(5)]
    mu=[F(1,5)]*5; ell=[(1+t)/2 for t in support]
    Z=sum((p*l for p,l in zip(mu,ell)),F(0))
    nu=[p*l/Z for p,l in zip(mu,ell)]
    ph=[support,[t*t for t in support]]
    means=[sum((w*x for w,x in zip(nu,row)),F(0)) for row in ph]
    gam=[[sum((nu[h]*(ph[i][h]-means[i])*(ph[j][h]-means[j]) for h in range(5)),F(0)) for j in range(2)] for i in range(2)]
    det=gam[0][0]*gam[1][1]-gam[0][1]*gam[1][0]
    check('dual_covariance_invertibility',det>0)
    inv=[[gam[1][1]/det,-gam[0][1]/det],[-gam[1][0]/det,gam[0][0]/det]]
    found=False
    for v in itertools.product((F(-1),F(0),F(1)),repeat=2):
        f=[sum((v[i]*inv[i][j]*(ph[j][h]-means[j]) for i in range(2) for j in range(2)),F(0)) for h in range(5)]
        K=max(F(1),max(map(abs,f))); eps=F(1,2); s=eps/(4*K)
        muf=sum((w*x for w,x in zip(mu,f)),F(0))
        mup=[w*(1+s*x)/(1+s*muf) for w,x in zip(mu,f)]
        Zp=sum((w*l for w,l in zip(mup,ell)),F(0))
        nup=[w*l/Zp for w,l in zip(mup,ell)]
        check('dual_prior_total_mass',sum(mup)==1)
        check('dual_relative_ball',max(abs(p/w-1) for p,w in zip(mup,mu))<=eps)
        check('dual_posterior_pullback',all(p==w*(1+s*x) for p,w,x in zip(nup,nu,f)))
        for j in range(2):
            displacement=sum(((pp-p)*x for pp,p,x in zip(nup,nu,ph[j])),F(0))
            check('dual_exact_displacement',displacement==s*v[j])
        if muf:
            found=True
            check('negative_control_unnormalized_prior',sum(w*(1+s*x) for w,x in zip(mu,f))!=1)
    check('normalization_control_nonvacuous',found)
    negative_controls.append({'mutation':'drop posterior-to-prior normalization','detected':found})

def leja_checks():
    # Distinct and coincident node configurations, including multi-scale collisions.
    samples=[(F(1,8),F(1,4),F(1,4),F(3,4)),(F(1,8),F(1,8),F(1,8)),(F(1,8),F(1,8)+F(1,256),F(1,8)+F(1,128),F(7,8)),(F(1,16),F(1,4),F(1,2),F(3,4),F(15,16))]
    for nodes in samples:
        remaining=list(range(len(nodes))); selected=[]; ds=[]
        while remaining:
            scores={i:math.prod(abs(nodes[i]-nodes[j]) for j in selected) for i in remaining}
            chosen=max(remaining,key=lambda i:(scores[i],-i))
            ds.append(scores[chosen]);selected.append(chosen);remaining.remove(chosen)
        for j in range(1,len(nodes)+1):
            V=max(math.prod(abs(nodes[b]-nodes[a]) for a,b in itertools.combinations(J,2)) for J in itertools.combinations(range(len(nodes)),j))
            d=math.prod(ds[:j])
            check('leja_volume_bounds_exact',d<=V<=math.factorial(j)*d)
        check('leja_scales_nonincreasing',all(x>=y for x,y in zip(ds,ds[1:])))
        check('leja_exact_collision_rank',sum(x>0 for x in ds)==len(set(nodes)))

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,default=Path('EXECUTION.json'))
    args=parser.parse_args()
    physical_interface(); physical_metric(); weighted_updates(); flags_and_volumes(); bounded_dual(); leja_checks()
    source=Path(__file__).read_bytes()
    result={
        'reviewed_commit':'e1d0ff2ef04a8641ac77923b664c4d3e8386f212',
        'review_date':'2026-09-07','status':'PASS',
        'python':platform.python_version(),'arithmetic':'exact rational and Gaussian-rational; no floating point',
        'script_sha256':hashlib.sha256(source).hexdigest(),
        'assertions':sum(checks.values()),'groups':dict(sorted(checks.items())),
        'negative_controls':negative_controls,
        'author_suites_rerun':False,'pdf_recompiled':False,'pdf_visual_inspection':False,
        'limitations':['Finite diagnostics are not proofs of continuum-uniform constants, arbitrary horizons, covering theorems, minimax optimality, or novelty.', 'No author suites or archived execution receipts were counted as independent executions.', 'Rank samples use normalized coefficient maps at fixed rational centers; physical rank is zero at tau=0.']}
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
