#!/usr/bin/env python3
"""Exact fixtures, deterministic numerical cross-checks and negative controls.

This script does not prove the quantified theorems or calibrate a device.
"""
from fractions import Fraction as F
import hashlib
import itertools
import json
import numpy as np
import sympy as s
from spectral_value import certify,majorant,root_interval

def require(condition,message):
    if not condition:raise RuntimeError(message)
exact=0;negative=0;numerical=0
for d in range(2,7):
    spectra=[tuple(F(1,d) for _ in range(d)),(F(1),)+(F(0),)*(d-1)]
    spectra += [tuple(F(i,sum(range(1,d+1))) for i in range(d,0,-1))]
    for v in spectra:
        for r in range(1,d+1):
            q=majorant(v,r)
            require(sum(q)==1 and all(q[i]>=q[i+1] for i in range(d-1)),'ordered normalized majorant')
            require(sum(x>0 for x in q)<=r,'majorant rank')
            require(all(sum(v[:j])<=sum(q[:j]) for j in range(1,d+1)),'majorization')
            a,b=root_interval(q,60);require(b-a<=F(1,2**60),'rational width')
            if a>0:require(sum(x/(x+a) for x in q)>=1,'root lower endpoint')
            if b>0:require(sum(x/(x+b) for x in q)<=1,'root upper endpoint')
            exact+=6
# Least-majorant property against every small rational probability vector.
for d in (3,4):
    def compositions(n,k):
        if k==1:yield(n,);return
        for i in range(n+1):
            for rest in compositions(n-i,k-1):yield(i,)+rest
    grid=sorted(set(tuple(sorted(v,reverse=True)) for v in compositions(8,d)))
    for vi in grid:
        v=tuple(F(x,8) for x in vi)
        for r in range(1,d+1):
            q=majorant(v,r)
            for zi in grid:
                z=tuple(F(x,8) for x in zi)
                if sum(x>0 for x in z)<=r and all(sum(v[:j])<=sum(z[:j]) for j in range(1,d+1)):
                    require(all(sum(q[:j])<=sum(z[:j]) for j in range(1,d+1)),'least majorant')
                    exact+=1
v=(F(3,4),F(1,8),F(1,8))
require(root_interval(v)==(F(1,2),F(1,2)),'three-dimensional rational secular root');exact+=1
q=majorant(v,2);c=s.sqrt(3)/4
require(s.simplify(sum(s.Rational(x.numerator,x.denominator)/(s.Rational(x.numerator,x.denominator)+c) for x in q)-1)==0,'rank-two radical root');exact+=1
require(majorant(v,3)==v and majorant(v,1)==(F(1),F(0),F(0)),'rank endpoints');exact+=1
I=s.eye(3);C0=s.diag(s.sqrt(3)/2,s.sqrt(2)/4,s.sqrt(2)/4)
V=[s.Matrix([[1/s.sqrt(2),0,0],[0,1,0]]),s.Matrix([[1/s.sqrt(2),0,0],[0,0,1]])]
require(sum((X.T*X for X in V),s.zeros(3))==I,'instrument complete');exact+=1
atoms=[s.diag(s.Rational(3,4),s.Rational(1,4),0),s.diag(s.Rational(3,4),0,s.Rational(1,4))]
for X,a in zip(V,atoms):require(s.simplify((X*C0).T*(X*C0)-a/2)==s.zeros(3),'fixed initial state instrument');exact+=1
require(sum(atoms,s.zeros(3))/2==C0.T*C0,'Gram barycenter');exact+=1
cert=certify({'spectrum':['3/4','1/8','1/8'],'old_dimension':3,'fresh_dimension':3,'t':'1'})
require(cert['fresh_eigenvalues_for_majorant_atom']==['3/7','2/7','2/7'],'optimal nonuniform fresh spectrum');exact+=1
cert2=certify({'spectrum':['3/4','1/8','1/8'],'old_dimension':3,'fresh_dimension':2,'t':'1'})
require(cert2['no_message_comparison']['strict_gain_criterion'],'strict receiver message');exact+=1
require(F(cert2['no_message_comparison']['gain_interval'][0])>0,'strict rational gain enclosure');exact+=1
# Exact rank-two receiver payoff gives negative mass sqrt(3)/16 per branch.
S2=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
C=s.diag(s.sqrt(s.Rational(3,8)),s.sqrt(s.Rational(1,8)))
D=s.eye(2)/s.sqrt(2);T=s.kronecker_product(C,D);K=T*S2*T
neg=sum((-e)*m for e,m in K.eigenvals().items() if e<0)
require(s.simplify(neg-s.sqrt(3)/16)==0,'receiver payoff normalization');exact+=1
# Deterministic complex PSD checks of the nonsimultaneously-diagonal case.
rng=np.random.default_rng(9410606)
def chi(x):
    x=np.maximum(np.asarray(x,float),0);return max(0.,float(np.linalg.eigvalsh(np.outer(np.sqrt(x),np.sqrt(x))-np.diag(x))[-1]))
def qfloat(x,r):
    x=np.sort(np.maximum(x,0))[::-1];m=0
    while m<r-1 and x[m]>sum(x[m:])/(r-m)+1e-13:m+=1
    return np.r_[x[:m],np.full(r-m,sum(x[m:])/(r-m))]
def roof(A,r):return chi(qfloat(np.linalg.eigvalsh(A),r))
def psd(d,k):
    X=rng.normal(size=(d,k))+1j*rng.normal(size=(d,k));A=X@X.conj().T;return A/np.trace(A).real

def sqrt(A):
    w,U=np.linalg.eigh(A);return (U*np.sqrt(np.maximum(0,w)))@U.conj().T
for d in range(2,7):
    Sw=np.eye(d*d).reshape(d,d,d,d).transpose(1,0,2,3).reshape(d*d,d*d)
    for r in range(1,d+1):
        for _ in range(15):
            A=psd(d,d);B=psd(d,r);T=np.kron(sqrt(A),sqrt(B))
            mass=-np.minimum(0,np.linalg.eigvalsh(T@Sw@T)).sum()
            bound=chi(sorted(np.linalg.eigvalsh(A),reverse=True)[:r])/2
            require(mass<=bound+2e-7,'rank-sensitive arbitrary fresh orientation')
            C=psd(d,d);w=rng.random()
            require(roof(w*A+(1-w)*C,r)>=w*roof(A,r)+(1-w)*roof(C,r)-1e-9,'spectral roof concavity')
            numerical+=2
# Wrong protocol/data interpretations are rejected rather than certified.
for data in [{'spectrum':[.5,.5]}, {'spectrum':['1/2','1/3']},
             {'spectrum':['2','-1']},{'spectrum':['1','0'],'old_dimension':True},
             {'spectrum':['1','0'],'fresh_dimension':3},{'spectrum':['1','0'],'t':'2'},
             {'spectrum':['1','0'],'bits':0},{'spectrum':['1','0'],'expected_budget':2}]:
    try:certify(data)
    except ValueError:negative+=1
    else:raise RuntimeError('invalid data accepted')
require(chi([.75,.125])<chi([.75,.25])-0.1,'top spectrum is not its concave roof');negative+=1
require(cert['fresh_eigenvalues_for_majorant_atom']!=['1/3']*3,'uniform fresh need not be optimal');negative+=1
require(not certify({'spectrum':['1','0','0'],'fresh_dimension':2})['no_message_comparison']['strict_gain_criterion'],'pure input has no strict message gain');negative+=1
require(not certify({'spectrum':['1/3']*3,'fresh_dimension':1})['no_message_comparison']['strict_gain_criterion'],'rank-one fresh has no strict message gain');negative+=1
print(json.dumps({'schema':'gtf94.spectral-check/1','status':'success','exact_checks':exact,
 'numerical_sanity_checks':numerical,'negative_controls':negative,
 'numerical_tolerances':{'leaf_upper':'2e-7','concavity':'1e-9'},
 'example_certificate_sha256':hashlib.sha256(json.dumps(cert2,sort_keys=True).encode()).hexdigest(),
 'continuum_proof_by_replay':False,'physical_calibration':False,'independent_priority_clearance':False},sort_keys=True))
