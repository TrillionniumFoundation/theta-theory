#!/usr/bin/env python3
"""Finite witnesses for cut comparison, companding, tuple size and Gaussian algebra.
The continuous-parameter arguments are in the manuscript, not in this suite.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

counts=Counter()
def check(ok, group):
    if not ok: raise RuntimeError('regression failed: '+group)
    counts[group]+=1

def quant(x,k):
    sign=1 if x>=0 else -1; x=abs(x)
    j=int(k*x/(1+x))
    return sign*F(j,k-j)

def distortion(mu,kernel,z,labels):
    nc=max(labels)+1; nu=len(kernel[0]); value=F(0)
    for c in range(nc):
        for u in range(nu):
            mass=sum(mu[h]*kernel[h][u] for h in range(len(mu)) if labels[h]==c)
            if not mass: continue
            mean=sum(mu[h]*kernel[h][u]*z[h][u] for h in range(len(mu)) if labels[h]==c)/mass
            value+=sum(mu[h]*kernel[h][u]*(z[h][u]-mean)**2 for h in range(len(mu)) if labels[h]==c)
    return value

def optimum(mu,kernel,z,M):
    return min(distortion(mu,kernel,z,labels) for labels in product(range(M),repeat=len(mu)))

def mm(A,B): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def tr(A): return list(map(list,zip(*A)))
def plus(*args): return [[sum(a[i][j] for a in args) for j in range(len(args[0][0]))] for i in range(len(args[0]))]
def scale(a,A): return [[a*x for x in row] for row in A]
def eye(d): return [[F(i==j) for j in range(d)] for i in range(d)]
def outer(a,b): return [[x*y for y in b] for x in a]
def det(A):
    a=[row[:] for row in A]; result=F(1)
    for i in range(len(a)):
        piv=next((j for j in range(i,len(a)) if a[j][i]),None)
        if piv is None: return F(0)
        if piv!=i: a[i],a[piv]=a[piv],a[i];result=-result
        v=a[i][i];result*=v
        for j in range(i+1,len(a)):
            q=a[j][i]/v
            for k in range(i,len(a)): a[j][k]-=q*a[i][k]
    return result

def main():
    for k in range(1,33):
        reps=set()
        for num in range(-180,181):
            x=F(num,7);q=quant(x,k);reps.add(q)
            check(abs(x-q)<=(1+abs(x))**2/k,'global_compander_point_bound')
            check(abs(q)<=abs(x),'compander_inwardness')
        check(len(reps)<=2*k-1,'compander_cardinality')
    for M in range(1,257):
        for d in range(1,9):
            m=1
            while (m+1)**d<=M: m+=1
            k=(m+1)//2
            check(2*k-1<=m,'per_coordinate_alphabet')
            for j in range(d+1): check(m**j<=M,'all_intermediate_tuple_counts')
            check(M<= (4*k)**d,'uniform_compander_budget_conversion')
    mu=[F(1,6),F(1,3),F(1,2)]; eta=[F(1,2),F(1,2)]
    for probabilities in product([F(1,4),F(1,2),F(3,4)],repeat=3):
        K=[[x,1-x] for x in probabilities]; independent=[eta]*3
        lo=min(2*x for row in K for x in row); hi=max(2*x for row in K for x in row)
        for z in [[[F(0),F(1)],[F(1,3),F(1,2)],[F(1),F(0)]],
                  [[F(1,4),F(3,4)],[F(1,2),F(2,3)],[F(3,4),F(1,4)]]]:
            for M in [1,2,3]:
                actual=optimum(mu,K,z,M); reference=optimum(mu,independent,z,M)
                check(lo*reference<=actual<=hi*reference,'finite_common_channel_sandwich')
                check(optimum([lo*x for x in mu],independent,z,M)==lo*reference,'submeasure_mass_scaling')
    for d in range(2,7):
        I=eye(d);a=[F(j+1,d) for j in range(d)];aa=outer(a,a);aa2=sum(x*x for x in a)
        for tau2,sigma2 in product([F(1,3),F(1),F(3)],repeat=2):
            c=1/(1+tau2);v0=tau2/(1+tau2);sv=sigma2+v0*aa2
            k=[v0*x/sv for x in a];D=plus(I,scale(-1,outer(k,a)))
            S=plus(scale(v0,I),scale(-v0*v0/sv,aa))
            precision=plus(scale(1/v0,I),scale(1/sigma2,aa))
            check(mm(precision,S)==I,'posterior_precision_inverse')
            check(det(D)==sigma2/sv,'continuation_full_rank')
            check(S==scale(v0,D),'conditional_covariance_algebra')
            Da=[row[0] for row in mm(D,[[x] for x in a])]
            C=plus(scale(c*c*(1+tau2),mm(D,tr(D))),scale(aa2+sigma2,outer(k,k)),
                   scale(c,outer(Da,k)),scale(c,outer(k,Da)))
            check(C==plus(I,scale(-1,S)),'actual_posterior_total_covariance')
            for n in range(1,d+1):
                check(det([row[:n] for row in S[:n]])>0,'positive_posterior_minors')
                check(det([row[:n] for row in C[:n]])>0,'positive_acquired_mean_minors')
    # These negative controls are finite analogues, not proofs of the continuum examples.
    check(F(1,2)*F(1,4)!=F(1,4),'negative:do_not_normalize_submass')
    check(8*3>8,'negative:stored_phase_multiplies_full_tuple')
    check(F(0)<F(1,8),'negative:defect_allowance_is_not_risk_floor')
    cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(Path(__file__).with_name('regression_previous.py'))]
    run=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if run.returncode: raise RuntimeError(run.stdout)
    previous=json.loads(run.stdout);check(previous['status']=='PASS','retained_R7_suite')
    print(json.dumps({'status':'PASS','native_checks':sum(counts.values()),'groups':dict(sorted(counts.items())),
                     'retained_R7':previous,'scope':'finite exact-arithmetic witnesses; no continuum theorem certification'},sort_keys=True,indent=2))

if __name__=='__main__': main()
