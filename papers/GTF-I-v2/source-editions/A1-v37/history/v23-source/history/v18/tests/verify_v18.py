#!/usr/bin/env python3
"""Exact finite diagnostics for the new v18 identities and boundary cases.

No numerical optimization over all encoders, formal proof verification,
or numerical certification of inverse-function constants is claimed.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from math import factorial
from pathlib import Path
import platform
import random
import sys

COUNTS=Counter()
def check(value: bool, group: str) -> None:
    if not value:
        raise AssertionError(group)
    COUNTS[group]+=1

def determinant(matrix):
    a=[[F(x) for x in row] for row in matrix]
    n=len(a); value=F(1)
    if not n:
        return value
    if any(len(row)!=n for row in a):
        raise ValueError('Not square')
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:
            return F(0)
        if pivot!=j:
            a[pivot],a[j]=a[j],a[pivot];value=-value
        t=a[j][j];value*=t
        for i in range(j+1,n):
            ratio=a[i][j]/t
            for k in range(j+1,n):
                a[i][k]-=ratio*a[j][k]
    return value

def rank(matrix):
    a=[[F(x) for x in row] for row in matrix]
    if not a:
        return 0
    row=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(row,len(a)) if a[i][col]),None)
        if pivot is None:
            continue
        a[row],a[pivot]=a[pivot],a[row]
        val=a[row][col]
        a[row]=[x/val for x in a[row]]
        for i in range(len(a)):
            if i!=row:
                val=a[i][col]
                a[i]=[x-val*y for x,y in zip(a[i],a[row])]
        row+=1
        if row==len(a):
            break
    return row

def dot(a,b):
    return sum((x*y for x,y in zip(a,b)),F(0))

def normalization():
    rng=random.Random(180907)
    for q in range(1,5):
        for inputs in range(1,5):
            for _ in range(8):
                p=[F(rng.randrange(-5,6),7) for j in range(q)]
                z=F(rng.randrange(1,8),9)
                dz=[F(rng.randrange(-3,4),5) for i in range(inputs)]
                dp=[[F(rng.randrange(-2,3),3) for i in range(inputs)] for j in range(q)]
                aug=[[z]+dz]+[[z*p[j]]+[p[j]*dz[i]+z*dp[j][i] for i in range(inputs)] for j in range(q)]
                check(rank(aug)==1+rank(dp),'augmented_normalized_rank')
    check(rank([[1,0,0],[2,0,0]])-1==0,'zero_rank')
    # A positive detector independent of its command has two constant report states.
    predictions=[]
    for y in (-1,1):
        likelihood=[(1+y*x/F(2))/2 for x in (-1,1)]
        evidence=sum(likelihood)/2
        numerator=likelihood[1]/2
        check(rank([[evidence,0],[numerator,0]])-1==0,'zero_rank_report_matrix')
        predictions.append(numerator/evidence)
    check(predictions==[F(1,4),F(3,4)],'zero_rank_multiple_points')

def affine():
    for b in range(1,5):
        m=[F(i+1,20*b*b) for i in range(b)]
        for v in product((F(-1),F(0),F(1)),repeat=b):
            den=1+dot(m,v)
            theta=[x/den for x in v]
            check([x/(1-dot(m,theta)) for x in theta]==list(v),'projective_inverse')
            jac=[[(F(i==j)/den-v[i]*m[j]/den**2) for j in range(b)] for i in range(b)]
            check(determinant(jac)==den**(-b-1),'projective_jacobian')
            original_density=den/F(2**b)
            check(original_density/determinant(jac)==(1-dot(m,theta))**(-b-2)/F(2**b),'evidence_density')
    # Physical query weights are rational squares, so weighted coordinates stay exact.
    weights=[F(9,25),F(16,25)];roots=[F(3,5),F(4,5)]
    masses=[F(1,6),F(1,3),F(1,2)]
    features=[[F(-1,5),F(1,10)],[F(1,8),F(-1,12)],[F(1,6),F(1,9)]]
    tests=[[F(1,4),F(2,3)],[F(3,4),F(1,3)],[F(1,2),F(4,5)]]
    h=[[roots[j]*row[j] for j in range(2)] for row in tests]
    m=[sum(masses[k]*features[k][i] for k in range(3)) for i in range(2)]
    mean=[sum(masses[k]*h[k][j] for k in range(3)) for j in range(2)]
    cov=[[sum(masses[k]*(h[k][j]-mean[j])*(features[k][i]-m[i]) for k in range(3)) for i in range(2)] for j in range(2)]
    for u in product((F(-1),F(-1,3),F(0),F(1,3),F(1)),repeat=2):
        for y in (-1,1):
            likelihood=[(1+y*dot(u,row))/2 for row in features]
            evidence=dot(masses,likelihood)
            check(evidence>0,'positive_evidence')
            posterior=[sum(masses[k]*likelihood[k]*h[k][j] for k in range(3))/evidence for j in range(2)]
            theta=[y*x/(1+y*dot(m,u)) for x in u]
            check(posterior==[mean[j]+dot(cov[j],theta) for j in range(2)],'physical_covariance_identity')
            check(sum(weights[j]*(posterior[j]/roots[j]-mean[j]/roots[j])**2 for j in range(2))==sum((posterior[j]-mean[j])**2 for j in range(2)),'weighted_query_metric')

def integral_identity():
    nodes=[F(-1),F(-1,3),F(1,4),F(1)]
    masses=[F(1,10),F(2,10),F(3,10),F(4,10)]
    for d in range(1,5):
        phi=[[x**j for x in nodes] for j in range(d)]
        v=[[(2+x)*x**j for x in nodes] for j in range(d)]
        pair=[[sum(masses[k]*v[i][k]*phi[j][k] for k in range(4)) for j in range(d)] for i in range(d)]
        rhs=F(0)
        for indices in product(range(4),repeat=d):
            delta=determinant([[v[i][k] for k in indices] for i in range(d)])*determinant([[phi[i][k] for k in indices] for i in range(d)])
            check(delta>=0,'matched_paired_determinant_sign')
            mass=F(1)
            for k in indices:
                mass*=masses[k]
            rhs+=delta*mass
        check(determinant(pair)==rhs/factorial(d),'andreief_exact_finite_identity')
        check(determinant(pair)>0,'matched_full_support_gram')
    vals=[]
    for x0,x1 in product(nodes,repeat=2):
        delta=determinant([[1,1],[x0,x1]])*determinant([[1,1],[x0*x0,x1*x1]])
        check(delta==(x1-x0)**2*(x0+x1),'square_pairing_cancellation')
        vals.append(delta)
    check(min(vals)<0<max(vals),'paired_sign_changes')

def interior_prior():
    def moment(k,t):
        return (F(1,k+1) if k%2==0 else F(0)) + t*(F(1,k+2) if (k+1)%2==0 else F(0))
    for t in (F(-4,5),F(-1,2),F(-1,10),F(0),F(1,10),F(1,2),F(4,5)):
        cov=moment(3,t)-moment(1,t)*moment(2,t)
        check(cov==4*t/45,'interior_prior_covariance')
        for u in (F(-1),F(-1,2),F(0),F(1,2),F(1)):
            for y in (-1,1):
                alpha=F(2,5);beta=F(1,4)
                hmean=F(1,2)+beta*moment(2,t)
                cross=alpha*(moment(1,t)/2+beta*moment(3,t))
                m=alpha*moment(1,t)
                exact=(hmean+y*u*cross)/(1+y*u*m)
                check(exact==hmean+alpha*beta*cov*y*u/(1+y*u*m),'interior_prior_prediction')
                check(cross-hmean*m==alpha*beta*4*t/45,'exact_rank_discriminant')
    # Exact scalar uniform quantizer: conditional centroids and interval integrals.
    for scale in (F(0),F(1,7),F(1,2),F(1)):
        for M in range(1,17):
            total=F(0)
            for i in range(M):
                left=F(-1)+F(2*i,M);right=left+F(2,M)
                center=(left+right)/2
                total+=scale**2*((right-center)**3-(left-center)**3)/6
            check(total==scale**2/(3*M*M),'scalar_uniform_quantization_integral')

def main():
    normalization();affine();integral_identity();interior_prior()
    report={'version':18,'passed':True,'arithmetic':'exact rational and integer',
            'python':platform.python_version(),'assertions':sum(COUNTS.values()),
            'groups':dict(sorted(COUNTS.items())),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'Finite checks of identities, signs, evidence, and endpoints. Not a proof certificate, an exhaustive encoder optimization, or a certification of uniform analytic constants.'}
    output=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'validation/V18_STRUCTURAL_DIAGNOSTICS.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
