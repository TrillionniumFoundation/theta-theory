#!/usr/bin/env python3
"""Finite exact fixtures and explicitly numerical complex-matrix sanity checks.

These regressions do not prove the universal lemmas or certify a physical reset.
All data and seeds are fixed; ordinary and optimized Python return identical JSON.
"""
from fractions import Fraction as F
from itertools import product
import json
import math
import numpy as np
import sympy as s
from spectral_frame import projection_decomposition, capped_distance, certificate

EXACT = 0
NUMERICAL = 0
NEGATIVE = 0


def require(ok, message):
    if not bool(ok):
        raise RuntimeError(message)


def compositions(n, d):
    if d == 1:
        yield (n,)
    else:
        for i in range(n+1):
            for tail in compositions(n-i, d-1):
                yield (i, *tail)


# Exact finite interval decompositions, all zero-support and repeated-cut cases included.
for d in range(2, 6):
    for denominator in range(1, 8):
        for integer_spectrum in compositions(denominator, d):
            lam = [F(x, denominator) for x in integer_spectrum]
            for r in range(1, d+1):
                distance, capped = capped_distance(lam, r)
                require(distance == 2*sum(max(F(0), x-F(1,r)) for x in lam), 'cap distance')
                EXACT += 1
                if max(lam) <= F(1,r):
                    atoms = projection_decomposition(lam, r)
                    require(len(atoms) <= d, 'projection-frame cardinality')
                    require(sum(w for w, _ in atoms) == 1, 'frame weights')
                    require(all(sum(w/r for w, idx in atoms if i in idx) == lam[i]
                                for i in range(d)), 'projection-frame exact barycenter')
                    EXACT += 3

bad = [({'eigenvalues':['1/2','1/2'], 'rank':True}),
       ({'eigenvalues':[0.5,0.5], 'rank':1}),
       ({'eigenvalues':['3/4','1/4'], 'rank':2}),
       ({'eigenvalues':['1/3','1/3'], 'rank':1}),
       ({'eigenvalues':['-1/4','5/4'], 'rank':1}),
       ({'eigenvalues':['1/2','1/2'], 'rank':3}),
       ({'eigenvalues':['1/0','0'], 'rank':1}),
       ({'eigenvalues':[], 'rank':1})]
for item in bad:
    try:
        certificate(item)
    except ValueError:
        NEGATIVE += 1
    else:
        raise RuntimeError('invalid spectral certificate accepted')

# Exact instrument normalization for nonuniform and singular capped initial spectra.
for lam, r in [([F(1,2),F(1,3),F(1,6)],2),
               ([F(1,3),F(1,3),F(1,3),F(0)],2),
               ([F(1,4)]*4,3), ([F(1,2),F(0),F(1,2)],2)]:
    d = len(lam)
    rho = s.diag(*[s.Rational(x.numerator,x.denominator) for x in lam])
    inv = s.diag(*[1/s.sqrt(x) if x else 0 for x in rho.diagonal()])
    total = s.zeros(d)
    for weight, subset in projection_decomposition(lam,r):
        w = s.Rational(weight.numerator,weight.denominator)
        J = s.zeros(d,r)
        for j,i in enumerate(subset):
            J[i,j] = 1
        C = s.sqrt(w/r)*J.H
        D = J.H/s.sqrt(r)
        V = C*inv
        require(s.simplify(C.H*C-w*(J*J.H)/r) == s.zeros(d), 'old Gram factor')
        require(s.simplify(s.trace(D.H*D)-1) == 0, 'fresh vector normalization')
        total += V.H*V
        EXACT += 2
    require(s.simplify(total-s.diag(*[1 if x else 0 for x in lam])) == s.zeros(d),
            'instrument complete on initial Schmidt support')
    EXACT += 1

# Literal Born rules for seven qubit devices and all eight three-cut choices.
I = s.eye(2)
pauli = [s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]

def swap(d):
    out = s.zeros(d*d)
    for i in range(d):
        for j in range(d):
            out[i*d+j,j*d+i]=1
    return out

for t in [s.Rational(0),s.Rational(1,3),s.Rational(1,2),s.Rational(1)]:
    alternatives = [[(I+sign*t*A)/2,(I-sign*t*A)/2] for A in pauli for sign in [-1,1]]
    scalar = [I/2,I/2]
    for q,k,ell in product([1,2], repeat=3):
        r=min(q,k,ell)
        J=s.eye(2)[:,:r]
        C=J.H/s.sqrt(r)
        D=C
        minus=(s.eye(r*r)-swap(r))/2
        plus=s.eye(r*r)-minus
        for equal in [False,True]:
            L=6-t*t
            pC=s.Rational(1,2) if equal else (3-t*t)/L
            def event(E):
                val=0
                for y,z in product(range(2),repeat=2):
                    effect=minus if y==z else (plus if equal else s.zeros(r*r))
                    block=s.kronecker_product(C*E[y].T*C.H,D*E[z].T*D.H)
                    val+=s.trace(effect*block)
                return s.simplify(val)
            value=s.simplify(pC*event(scalar)+(1-pC)*(1-sum(event(E) for E in alternatives)/6))
            expected=s.Rational(1,2)+t*t*(2*r-1)/(12*r) if equal else 3/L+t*t*(r-1)/(2*r*L)
            require(s.simplify(value-expected)==0, 'literal three-cut Born optimum')
            require(C.rows<=q and C.rows<=k and D.rows<=ell,'counted quantum dimensions')
            EXACT+=2

# Exact exceptional qubit face: commuting mixed factors attain equality;
# a nonzero off-diagonal cannot be mistaken for another equality case.
a=s.diag(1,0)
for x,z in [(s.Rational(1,4),s.Rational(0)),(s.Rational(2,3),s.Rational(0)),
            (s.Rational(1,2),s.Rational(1,4)),(s.Rational(1,2),s.I/3),
            (s.Rational(1,5),s.Rational(2,5))]:
    b=s.Matrix([[x,z],[s.conjugate(z),1-x]])
    require(b.det()>=0,'positive exceptional fixture')
    delta=1-s.sqrt(1-4*s.Abs(z)**2)
    require(s.simplify(4*s.Abs(z)**2-(2*delta-delta**2))==0,'exceptional pinching identity')
    require((delta==0)==(a*b==b*a),'exceptional equality iff commutation')
    EXACT+=3
require(s.diag(s.Rational(1,3),s.Rational(2,3))!=a,'mixed equality is not a common pure factor')
NEGATIVE+=1

# Stable lemma is checked exactly for commuting equal factors: Delta=purity-1/r.
for d in range(2,7):
    for r in range(1,d+1):
        if (d,r)==(2,1):
            continue
        for n in [0,1,2,3]:
            lam=[s.Rational(1,r)]*r+[s.Rational(0)]*(d-r)
            if r>1:
                eps=s.Rational(n,8*r)
                lam[0]+=eps;lam[1]-=eps
            delta=sum(x*x for x in lam)-s.Rational(1,r)
            norm=sum(s.Abs(lam[i]-(s.Rational(1,r) if i<r else 0)) for i in range(d))
            require(s.simplify(r*delta-norm*norm)>=0,'same-support spectral variance bound')
            EXACT+=1

# Explicitly numerical, deterministic complex, singular and unequal-rank fixtures.
# These supplement rather than replace the written all-matrix proof.
def psqrt(A):
    e,U=np.linalg.eigh((A+A.conj().T)/2)
    return (U*np.sqrt(np.maximum(e,0)))@U.conj().T

def tn(A):
    return float(np.abs(np.linalg.eigvalsh((A+A.conj().T)/2)).sum())

rng=np.random.default_rng(932026)
for d in range(2,7):
    for r in range(1,d+1):
        if (d,r)==(2,1):
            continue
        for trial in range(4):
            ra=r
            rb=d if trial%2 else r
            X=rng.normal(size=(d,ra))+1j*rng.normal(size=(d,ra))
            Y=rng.normal(size=(d,rb))+1j*rng.normal(size=(d,rb))
            A=X@X.conj().T;A/=np.trace(A)
            B=Y@Y.conj().T;B/=np.trace(B)
            sa,sb=psqrt(A),psqrt(B)
            S=np.asarray(swap(d)).astype(complex)
            L=np.kron(sa,sb)
            delta=d-1/r-tn(L@(np.eye(d*d)-d*S)@L)
            # Use the known smaller-rank support to contain range Z, without
            # interpreting tiny numerical zero eigenvalues as physical ranks.
            U,_,_=np.linalg.svd(X,full_matrices=False)
            P=U@U.conj().T
            K=r+(3+math.sqrt(2))**2/(d-1-1/r)
            require(delta>=-2e-10,'centered rank bound numerical sanity')
            require(max(tn(A-P/r)**2,tn(B-P/r)**2)<=K*max(delta,0)+2e-8,
                    'stable common projection numerical sanity')
            NUMERICAL+=2

print(json.dumps({'schema':'gtf93.spectral-rigidity-regression/1','status':'success',
 'exact_fixture_checks':EXACT,'deterministic_numerical_checks':NUMERICAL,
 'negative_controls':NEGATIVE,'numerical_seed':932026,
 'numerical_checks_are_continuum_proof':False,'physical_reset_calibration':False,
 'independent_human_priority_clearance':False,
 'three_cut_dimensions_are_all_times_workspace_bounds':False},sort_keys=True))
