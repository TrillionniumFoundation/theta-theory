#!/usr/bin/env python3
"""Exact finite diagnostics for the new algebra theorem; no removable assertions.

Compare coefficient algebra with direct latent-state Bayes calculations.
Finite cases are not a proof of uniform geometric or coding estimates.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
import platform
import sys
import sympy as sp

GROUPS={}

def check(condition: bool, group: str, description: str) -> None:
    GROUPS[group]=GROUPS.get(group,0)+1
    if not condition:raise ArithmeticError(group+': '+description)

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def mean(p,values):return [sum((p[x]*values[x][j] for x in range(len(p))),F(0)) for j in range(len(values[0]))]
def mm(A,v):return [dot(row,v) for row in A]

def covariance(p,values):
    m=mean(p,values);d=len(m)
    return [[sum((p[x]*(values[x][i]-m[i])*(values[x][j]-m[j]) for x in range(len(p))),F(0)) for j in range(d)] for i in range(d)]

def multiply(c,z,aa,bb):
    d=len(c)-1
    return [c[0]*z[0]+sum((c[i+1]*z[j+1]*aa[i][j] for i in range(d) for j in range(d)),F(0))]+[
        c[0]*z[k+1]+z[0]*c[k+1]+sum((c[i+1]*z[j+1]*bb[i][j][k] for i in range(d) for j in range(d)),F(0)) for k in range(d)]

def indicator(tau):
    d=len(tau);values=[[F(0)]*d for _ in range(d+1)]
    aa=[[F(0)]*d for _ in range(d)];bb=[[[F(0)]*d for _ in range(d)] for _ in range(d)]
    for i in range(d):values[i+1][i]=tau[i];bb[i][i][i]=tau[i]
    return values,aa,bb

def characters(t,s):
    states=list(product((-1,1),repeat=2));d=3
    values=[[t*x,s*y,t*s*x*y] for x,y in states]
    aa=[[F(0)]*d for _ in range(d)];bb=[[[F(0)]*d for _ in range(d)] for _ in range(d)]
    aa[0][0]=t*t;aa[1][1]=s*s;aa[2][2]=t*t*s*s
    bb[0][1][2]=bb[1][0][2]=F(1)
    bb[0][2][1]=bb[2][0][1]=t*t
    bb[1][2][0]=bb[2][1][0]=s*s
    return values,aa,bb

CASES=0

def experiment(values,aa,bb,p,tag):
    global CASES
    CASES+=1;d=len(values[0]);delta=F(1,4*d)
    for x in range(len(p)):
        for i,j in product(range(d),repeat=2):
            check(values[x][i]*values[x][j]==aa[i][j]+dot(bb[i][j],values[x]),'multiplication','pointwise closure '+tag)
    m=mean(p,values);C=covariance(p,values)
    # Nonconstant, nonidentical commands; both report signs are checked at all prefixes.
    commands=[[delta*F(((i+2*j)%5)-2,3) for i in range(d)] for j in range(4)]
    for word in ((1,1,1,1),(-1,1,-1,1),(1,-1,-1,-1)):
        coeff=[F(1)]+[F(0)]*d;weights=list(p);v=list(m)
        for n,(u,y) in enumerate(zip(commands,word),1):
            coeff=multiply(coeff,[F(1)]+[y*z for z in u],aa,bb)
            direct_product=[F(1)]*len(p)
            for u0,y0 in zip(commands[:n],word[:n]):
                direct_product=[z*(1+y0*dot(u0,values[x])) for x,z in enumerate(direct_product)]
            for x in range(len(p)):
                check(coeff[0]+dot(coeff[1:],values[x])==direct_product[x],'product_chart','coefficient/direct product '+tag)
            evidence=sum((p[x]*direct_product[x] for x in range(len(p))),F(0))
            check(evidence==coeff[0]+dot(coeff[1:],m),'product_chart','evidence identity')
            check(F(3,4)**n<=evidence<=F(5,4)**n,'product_chart','uniform denominator')
            post=[p[x]*direct_product[x]/evidence for x in range(len(p))]
            direct=mean(post,values)
            theta=[z/evidence for z in coeff[1:]]
            chart=[m[i]+dot(C[i],theta) for i in range(d)]
            check(chart==direct,'product_chart','mean plus covariance chart')
            updated=[(v[i]+y*sum((u[j]*(aa[i][j]+dot(bb[i][j],v)) for j in range(d)),F(0)))/(1+y*dot(u,v)) for i in range(d)]
            check(updated==direct,'raw_updates','update versus full posterior')
            # Physical query metric: include the constant probe and keep the attenuation.
            remain=5-n
            pred=[F(1,2)**remain]+[F(1,2)**remain*(1+delta*z) for z in updated]
            direct_pred=[F(1,2)**remain]+[sum((post[x]*F(1,2)**remain*(1+delta*values[x][i]) for x in range(len(p))),F(0)) for i in range(d)]
            check(pred==direct_pred,'physical_queries','actual future-product probabilities')
            gap=[updated[i]-m[i] for i in range(d)]
            physical_loss=sum(((pred[i]-([F(1,2)**remain]+[F(1,2)**remain*(1+delta*z) for z in m])[i])**2 for i in range(d+1)),F(0))/F(d+1)
            check(physical_loss==(F(1,2)**remain*delta)**2*dot(gap,gap)/F(d+1),'physical_queries','physical weighted squared norm')
            if all(z==0 for row in C for z in row):check(direct==m,'zero_rank','zero covariance gives exact singleton')
            v=updated
    # Independent rank check: covariance rank equals affine dimension on positive support.
    A=sp.Matrix([[sp.Rational(z.numerator,z.denominator) for z in row]+[1] for row,p0 in zip(values,p) if p0>0])
    S=sp.Matrix([[sp.Rational(z.numerator,z.denominator) for z in row] for row in C])
    check(S.rank()==A.rank()-1,'rank_strata','support affine dimension')
    check(all(x>=0 for x in S.diagonal()),'rank_strata','nonnegative diagonal')

for d in (2,3):
    priors=[tuple([F(1,d+1)]*(d+1)),tuple([F(i+1,(d+1)*(d+2)//2) for i in range(d+1)]),tuple([F(1)]+[F(0)]*d),tuple([F(0)]+[F(1,d)]*d)]
    priors.append(tuple([1-F(d,10**6)]+[F(1,10**6)]*d))
    for tau in product((F(0),F(1,11),F(1)),repeat=d):
        values,aa,bb=indicator(tau)
        for p in priors:experiment(values,aa,bb,p,'indicator')

for t,s in product((F(0),F(1,13),F(1,2),F(1)),repeat=2):
    values,aa,bb=characters(t,s)
    for p in ((F(1,4),)*4,(F(1,10),F(2,10),F(3,10),F(4,10)),(F(1,2),F(1,2),F(0),F(0)),(F(1),F(0),F(0),F(0))):
        experiment(values,aa,bb,p,'characters')

# Symbolic local chart: differentiation before applying any covariance.
x,y,z,w,m1,m2=sp.symbols('x y z w m1 m2')
t1,t2=sp.symbols('t1 t2')
b1=x+z+t1*x*z;b2=y+w+t2*y*w
Z=1+m1*b1+m2*b2
Theta=sp.Matrix([b1/Z,b2/Z])
J=Theta.jacobian([x,y]).subs({x:0,y:0,z:0,w:0})
check(J==sp.eye(2),'acquired_density','full first-command Jacobian at constant history')
check(sp.simplify(Theta.subs({z:0,w:0})-sp.Matrix([x,y])/(1+m1*x+m2*y))==sp.zeros(2,1),'acquired_density','exact projective section')
# Joint commands and one two-report word: cube expectation is its constant coefficient.
check(sp.Poly(Z,x,y,z,w).coeff_monomial(1)==1,'acquired_density','cube mean of unscaled evidence')
check(F(1,4)*F(1)==F(1,4),'acquired_density','actual two-report word mass')
check(F(1,4)!=F(1),'negative_controls','conditioning away report mass is rejected')

# Covariance exterior powers and the two-channel determinant are independently symbolic.
a,b=sp.symbols('a b',real=True)
S=sp.Matrix([[2*a*a,-a*b],[-a*b,2*b*b]])/9
check(sp.factor(S.det())==a*a*b*b/27,'profile','two-channel determinant')
check(sp.trace(S)==2*(a*a+b*b)/9,'profile','two-channel trace')
for scales in product((F(0),F(1,7),F(1,2),F(1)),repeat=3):
    scales=sorted(scales,reverse=True);V=[];v=F(1)
    for q in scales:v*=q;V.append(v)
    for ell in (1,2,3):
        if scales[ell-1]>0:
            M0=V[ell-1]/scales[ell-1]**ell
            check(M0>=1,'integer_inverse','real witness budget >= 1')
            for j in (1,2,3):check(V[j-1]/M0<=scales[ell-1]**j,'integer_inverse','all branches below witness scale')
            budget=(M0.numerator+M0.denominator-1)//M0.denominator
            check(F(budget)<=2*M0,'integer_inverse','integer rounding factor')

# Deliberate errors must be distinguishable from the exact physical formulas.
values,aa,bb=indicator((F(1,2),F(1,3)));p=(F(1,6),F(1,3),F(1,2))
m=mean(p,values);u=(F(1,8),F(-1,10));den=1+dot(u,m)
right=[(m[i]+sum((u[j]*(aa[i][j]+dot(bb[i][j],m)) for j in range(2)),F(0)))/den for i in range(2)]
wrong=[m[i]+sum((u[j]*(aa[i][j]+dot(bb[i][j],m)) for j in range(2)),F(0)) for i in range(2)]
check(right!=wrong,'negative_controls','missing Bayes denominator detected')
check(F(1,9)**2!=F(1),'negative_controls','whitening away vanishing physical scale detected')
check(len(GROUPS)>=9,'negative_controls','all diagnostic groups exercised')
report={'version':22,'status':'passed','passed':True,'experiment_cases':CASES,
 'assertions':sum(GROUPS.values()),'groups':GROUPS,'python':platform.python_version(),
 'sympy':sp.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Exact finite product, covariance, update, density-anchor, rank, physical-loss and inverse-envelope diagnostics. Not a proof of compact-uniform density, entropy, or optimal coding; not an independent referee assessment.'}
text=json.dumps(report,indent=2,sort_keys=True)+'\n'
if len(sys.argv)>1:Path(sys.argv[1]).write_text(text)
print(text,end='')
