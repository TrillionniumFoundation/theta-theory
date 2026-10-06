#!/usr/bin/env python3
"""Exact finite regressions for the two specified receiver-dimension cuts.

These are test fixtures, not a proof of the universal variational principle.
All checks survive python -O. No numerical optimizer supplies a certificate.
"""
from __future__ import annotations
import json
import sympy as s

checks = 0

def require(ok, message):
    global checks
    if not bool(ok):
        raise RuntimeError(message)
    checks += 1

def same(a,b,message):
    if isinstance(a,s.MatrixBase):
        require(all(s.simplify(x)==0 for x in a-b),message)
    else:
        require(s.simplify(a-b)==0,message)

def swap(d):
    return s.Matrix(d*d,d*d,lambda i,j: int(i//d==j%d and i%d==j//d))

def norm1(h):
    return s.simplify(sum(s.Abs(v)*m for v,m in h.eigenvals().items()))

def negmass(h):
    return s.simplify((norm1(h)-s.trace(h))/2)

def cyclic(d,r,h):
    return s.Matrix(d,r,lambda i,j:int(i==(h+j)%d))

def biased(d,r,t):
    L=2*(d+1)-t*t
    return s.Rational(d+1)/L+t*t*s.Rational(r-1,2*r)/L

def equal(d,r,t):
    return s.Rational(1,2)+t*t*s.Rational(d*r-1,2*d*r*(d+1))

# Two independent parameter bounds, including rank one and full rank.
for d in range(2,9):
    for k in range(1,d+1):
        for ell in range(1,d+1):
            r=min(k,ell)
            for t in (s.Rational(0),s.Rational(1,2),s.Rational(1)):
                require(s.Rational(1,2)<=equal(d,r,t)<=equal(d,d,t),'equal spectrum endpoints')
                require(biased(d,1,t)<=biased(d,r,t)<=biased(d,d,t),'biased spectrum endpoints')
            require(r<=k and r<=ell,'both retained dimensions respected')
    for r in range(1,d):
        t=s.Rational(2,3); L=2*(d+1)-t*t
        same(biased(d,r+1,t)-biased(d,r,t),t*t/(2*L*r*(r+1)),'biased adjacent increment')
        same(equal(d,r+1,t)-equal(d,r,t),t*t/(2*d*(d+1)*r*(r+1)),'equal adjacent increment')
    same(equal(d,1,s.Rational(1)),s.Rational(1,2)+s.Rational(d-1,2*d*(d+1)),'classical endpoint')
    same(equal(d,d,s.Rational(1)),s.Rational(1,2)+s.Rational(d-1,2*d*d),'full reset endpoint')

# All cyclic compression instruments, normalizations and attaining spectra.
for d in range(2,6):
    Sd=swap(d)
    for r in range(1,d+1):
        grams=s.zeros(d)
        for h in range(d):
            J=cyclic(d,r,h); V=J.H/s.sqrt(r)
            C=V/s.sqrt(d); D=V
            grams+=V.H*V
            same(s.trace(D.H*D),1,'fresh state normalized')
            require(C.rank()<=r and D.rank()<=r,'rectangular ranks')
            F=s.kronecker_product(C,D)
            K=s.simplify(F*Sd*F.H)
            Z=s.simplify(F*(s.eye(d*d)-d*Sd)*F.H)
            same(K,swap(r)/(d*r*r),'rectangular swap contraction')
            same(Z,(s.eye(r*r)-d*swap(r))/(d*r*r),'centered rectangular contraction')
            same(negmass(K),s.Rational(r-1,2*r*d),'negative mass attains rank bound')
            same(norm1(Z),s.Rational(d*r-1,r*d),'centered norm attains rank bound')
        same(grams,s.eye(d),'instrument trace preservation')

# Nonflat, singular and disjoint-support finite tests; exact radical comparisons.
diagonal_cases=[([1,0],[0,1]),([1,0],[s.Rational(1,3),s.Rational(2,3)]),
    ([s.Rational(1,5),s.Rational(4,5)],[s.Rational(4,5),s.Rational(1,5)]),
    ([s.Rational(1,2),s.Rational(1,2),0],[0,s.Rational(1,2),s.Rational(1,2)]),
    ([s.Rational(1,3),s.Rational(2,3),0],[s.Rational(1,4),s.Rational(1,4),s.Rational(1,2)])]
for aa,bb in diagonal_cases:
    d=len(aa);A=s.diag(*aa);B=s.diag(*bb);r=min(A.rank(),B.rank())
    F=s.kronecker_product(s.diag(*[s.sqrt(x) for x in aa]),s.diag(*[s.sqrt(x) for x in bb]))
    K=s.simplify(F*swap(d)*F);Z=s.simplify(F*(s.eye(d*d)-d*swap(d))*F)
    require(negmass(K)<=s.Rational(r-1,2*r),'singular negative-mass bound')
    require(norm1(Z)<=d-s.Rational(1,r),'singular centered bound')
# The equality exception must not be incorrectly excluded.
A=s.diag(1,0);B=s.diag(0,1);F=s.kronecker_product(A,B)
same(norm1(F*(s.eye(4)-2*swap(2))*F),1,'d=2 r=1 orthogonal equality exception')
require(A!=B,'exception is genuinely non-isotropic')

# A complex noncommuting rank-one factor against a full-rank fresh factor.
u=s.Matrix([1,s.I])/s.sqrt(2);C=u.H;D=s.diag(1,s.sqrt(2))/s.sqrt(3)
A=C.H*C;B=D.H*D;F=s.kronecker_product(C,D)
require(A*B!=B*A,'noncommuting fixture')
same(negmass(s.simplify(F*swap(2)*F.H)),0,'rank-one negative mass without common support')
require(norm1(s.simplify(F*(s.eye(4)-2*swap(2))*F.H))<=1,'complex centered-rank bound')

# Literal seven-device experiment, full Born contractions (not payoff formulas).
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
for t in (s.Rational(0),s.Rational(1,2),s.Rational(1)):
    devices=[(I/2,I/2)]+[((I+t*e*M)/2,(I-t*e*M)/2) for M in (X,Y,Z) for e in (-1,1)]
    for r in (1,2):
        Sp=swap(r); minus=(s.eye(r*r)-Sp)/2;plus=(s.eye(r*r)+Sp)/2
        for mode in ('biased','equal'):
            probs=[]
            for E in devices:
                q=0;mass=0
                for y in range(2):
                    for h in range(2):
                        J=cyclic(2,r,h);C=J.H/s.sqrt(2*r);D=J.H/s.sqrt(r)
                        for z in range(2):
                            receiver=s.kronecker_product(C*E[y].T*C.H,D*E[z].T*D.H)
                            effect=minus if y==z else (plus if mode=='equal' else s.zeros(r*r))
                            q+=s.trace(effect*receiver);mass+=s.trace(receiver)
                same(mass,1,'complete physical output normalization')
                probs.append(s.simplify(q))
            if mode=='equal':pC=s.Rational(1,2)
            else:pC=(3-t*t)/(6-t*t)
            score=s.simplify(pC*probs[0]+(1-pC)*(1-sum(probs[1:])/6))
            same(score,equal(2,r,t) if mode=='equal' else biased(2,r,t),'seven-device exact score')
            require(0<=score<=1,'Bayes score interval')

# Mixed-output Kraus refinement, and mixed fresh-state refinement, preserve Born values.
C0=s.eye(2)/s.sqrt(2)
V=[s.Matrix([[1,0]])/s.sqrt(3),s.Matrix([[0,1]])/s.sqrt(3),
   s.Matrix([[1,0]])*s.sqrt(s.Rational(2,3)),s.Matrix([[0,1]])*s.sqrt(s.Rational(2,3))]
same(sum((v.H*v for v in V),s.zeros(2)),s.eye(2),'rank-one refined completeness')
E=(s.eye(2)+Y)/2
oldmix=sum((v*C0*E.T*C0.H*v.H for v in V),s.zeros(1))
fresh=[s.Matrix([1,0]),s.Matrix([1,s.I])/s.sqrt(2)];weights=[s.Rational(2,5),s.Rational(3,5)]
sigma=sum((w*q*q.H for w,q in zip(weights,fresh)),s.zeros(2))
# Fresh reference dimension is one; spectral/sample index is never quantum storage.
for G in ((I+X)/2,(I+Y)/2,(I+Z)/2):
    unrefined=(oldmix[0,0]*s.trace(G*sigma)).simplify()
    refined=sum((w*(v*C0*E.T*C0.H*v.H)[0,0]*(q.H*G*q)[0,0]
                for v in V for w,q in zip(weights,fresh)))
    same(unrefined,refined,'mixed preparations refined without quantum dimension increase')

print(json.dumps({'schema':'gtf92.rank-regression/1','status':'success','exact_checks':checks,
    'tested_spectrum_dimensions':[2,8], 'tested_operator_dimensions':[2,5],
    'seven_device_born_contractions':True,'d2_r1_equality_exception':True,
    'continuum_proof_by_replay':False,'physical_reset_calibration':False,
    'independent_human_priority_clearance':False,'unrestricted_memory_hierarchy':False},
    indent=2,sort_keys=True))
