#!/usr/bin/env python3
"""Finite exact rational diagnostics for R76 simultaneous positivity and synthesis.

These finite calculations are not a proof of universal quantifiers, a formal
proof-assistant certificate, a human referee report, or a priority assessment.
No assertion statement is used; normal and optimized execution do the same work.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import random

COUNTS = {}
GROUP = 'initialization'


def check(condition, message):
    if not condition:
        raise RuntimeError(f'{GROUP}: {message}')
    COUNTS[GROUP] = COUNTS.get(GROUP, 0) + 1


def dot(x, y):
    return sum((a*b for a,b in zip(x,y)), F(0))


def rank(mat):
    a=[[F(x) for x in row] for row in mat]
    r=0
    for j in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][j]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r]
        z=a[r][j]
        a[r]=[x/z for x in a[r]]
        for k in range(r+1,len(a)):
            z=a[k][j]
            if z:a[k]=[x-z*y for x,y in zip(a[k],a[r])]
        r+=1
        if r==len(a):break
    return r


def min_cost_vectors(v):
    n=len(v);M=max(v);m=-min(v)
    if m<=0:raise ValueError('signed v required')
    c=[max(v[j]-int(i==j) for j in range(n)) for i in range(n)]
    d=[max(int(i==j)-v[j] for j in range(n)) for i in range(n)]
    for z in [c,d]:
        s=dot(v,z)
        if s>=0:z[v.index(-m)]+=s/m
        else:z[v.index(M)]-=s/M
    return c,d


def validate_null(v,c,d):
    n=len(v)
    check(sum(v)==1,'normalized common null vector')
    check(dot(v,c)==dot(v,d)==0,'both null constraints')
    check(all(c[i]>=v[j]-int(i==j) and d[i]>=int(i==j)-v[j]
              for i in range(n) for j in range(n)),'all two-outcome positivity inequalities')
    check(sum(d)>=n-1,'physical upper constraint')


def weighted_squared(n,C,D,gamma):
    check(gamma>=F(2*(n-2),n-4),'support range')
    z=(n-1)*(gamma*C+D)-(gamma*(n+1)+n*n-2*n-1)
    rad=4*n*(gamma-1)*(gamma+n-2)
    check(z>=0 and z*z>=rad,'exact squared supporting inequality')
    return z*z==rad


def endpoint_checks():
    global GROUP
    GROUP='strict_endpoint_polynomials'
    for n in range(5,101):
        gamma0=F(2*(n-2),n-4)
        for gamma in [gamma0,gamma0+1,2*gamma0,F(100)]:
            q=n*((n-3)*gamma-n+2)**2-4*(gamma-1)*(gamma+n-2)
            check(n*((n-3)*gamma-n+2)>0 and q>0,'strict endpoint comparison')
        if n>=6:
            check(n*(n-6)*(n-2)>=0,'Q_n(2)')
            check(2*n*(n-3)*(n-4)-4*n-4>0,'Q_n derivative at 2')
    return {'n_range':[5,100],'gamma_samples_per_n':4}


def null_vector_checks():
    global GROUP
    GROUP='arbitrary_signed_null_vectors'
    rng=random.Random(760042)
    used=0
    for n in [5,6,7,8,10,14]:
        for _ in range(120):
            v=[F(rng.randrange(-9,13),rng.randrange(1,8)) for _ in range(n-1)]
            v.append(1-sum(v))
            if min(v)>=0:continue
            c,d=min_cost_vectors(v)
            validate_null(v,c,d)
            for gamma in [F(2*(n-2),n-4),F(10),F(50)]:
                weighted_squared(n,sum(c),sum(d),gamma)
            # Add a nonnegative vector orthogonal to v, so both coefficient
            # inequalities remain true but the example need not be cost-minimal.
            ip=v.index(max(v));im=v.index(min(v));z=[F(0)]*n
            z[ip]=-v[im];z[im]=v[ip]
            cc=[c[i]+z[i]/7 for i in range(n)]
            dd=[d[i]+z[i]/11 for i in range(n)]
            validate_null(v,cc,dd)
            weighted_squared(n,sum(cc),sum(dd),F(10))
            # Independent matrix interpretation of the same exact triple.
            aa=1/(sum(c)+sum(d));p=sum(c)*aa
            A=[[aa*(int(i==j)+c[i]-v[j]) for j in range(n)] for i in range(n)]
            u=[aa*(c[i]+d[i]) for i in range(n)]
            check(sum(u)==1 and all(x>=0 for x in u),'probability column')
            check(all(0<=A[i][j]<=u[i] for i in range(n) for j in range(n)), 'bounded coefficient pair')
            check(sum(map(sum,A))==n*p,'mean identity')
            check(all(dot(v,[A[i][j] for i in range(n)])==0 for j in range(n)) and dot(v,u)==0,'joined kernel')
            # PAP=aP is equivalent to vanishing cross differences of A-aI.
            R=[[A[i][j]-aa*int(i==j) for j in range(n)] for i in range(n)]
            check(all(R[i][j]-R[i][0]-R[0][j]+R[0][0]==0
                      for i in range(n) for j in range(n)),'centered coefficient identity')
            used+=1
    return {'seed':760042,'tested_signed_vectors':used,'domains':'exact rational vectors, including nonminimal feasible c,d'}


def equality_checks():
    global GROUP
    GROUP='support_equality_and_mean_duality'
    used=0
    for n in range(5,26):
        for j in range(1,51):
            m=F(j,50)
            if not (n*m*m>1 and n*m<=n-2):continue
            M=(1+m)/(n-1)
            v=[M]*(n-1)+[-m]
            c=[M]*(n-1)+[M+M/m]
            d=[1-M]*(n-1)+[(n-1)*M*(1-M)/m]
            validate_null(v,c,d)
            gamma=(n*m*m+n-2)/(n*m*m-1)
            check(weighted_squared(n,sum(c),sum(d),gamma),'exact support equality')
            check(sum(c)==M*(n+1/m),'C equality formula')
            check(sum(d)==(1-M)*(n+1/m),'D equality formula')
            check(1/(sum(c)+sum(d))==((n-1)*M-1)/((n-1)*(n*M-1)), 'middle threshold identity')
            check((gamma+n-2)==n*(gamma-1)*m*m,'AMGM equality identity')
            used+=1
    return {'n_range':[5,25],'m_mesh_denominator':50,'equality_cases':used}


def coefficient(lams,ds,weights):
    n=len(lams[0])
    A=[[sum((weights[k]*lams[k][i]*ds[k][j] for k in range(len(weights))),F(0))
        for j in range(n)] for i in range(n)]
    u=[sum((weights[k]*lams[k][i] for k in range(len(weights))),F(0)) for i in range(n)]
    return A,u


def test_factor(n,p,a,lams,ds,weights,all_perms=False):
    check(sum(weights)==1 and all(w>0 for w in weights),'positive normalized orbit weights')
    check(all(sum(x)==1 and all(t>=0 for t in x) for x in lams),'preparation simplex')
    check(all(0<=x<=1 for d in ds for x in d),'both decoder probabilities')
    A,u=coefficient(lams,ds,weights)
    check(sum(map(sum,A))==n*p,'coefficient mean')
    check(all(0<=A[i][j]<=u[i] for i in range(n) for j in range(n)),'bounded shared pair')
    R=[[A[i][j]-a*int(i==j) for j in range(n)] for i in range(n)]
    check(all(R[i][j]-R[i][0]-R[0][j]+R[0][0]==0 for i in range(n) for j in range(n)),'PAP=aP')
    if a>0:check(rank([A[i]+[u[i]] for i in range(n)])==n-1,'joined rank n-1')
    rng=random.Random(761000+n)
    if all_perms:gs=list(permutations(range(n)))
    else:
        gs=[tuple(range(n)),tuple(list(range(1,n))+[0])]
        for _ in range(16):
            g=list(range(n));rng.shuffle(g);gs.append(tuple(g))
    for g in gs:
        beta=p+a*(sum(i==j for i,j in enumerate(g))-1)
        val=sum((A[i][g[i]] for i in range(n)),F(0))
        check(val==beta,'permutation response')
        check(1-val==(1-p)+(-a)*(sum(i==j for i,j in enumerate(g))-1),'negative contrast by output switch')
    return len(gs)


def factor_checks():
    global GROUP
    GROUP='explicit_boundary_and_interior_factors'
    cases=0;perms=0
    for n,p in [(5,F(3,8)),(6,F(3,10)),(7,F(1,4)),(9,F(1,5)),(16,F(1,10))]:
        m=(n-1)*p-1
        check(n*m*m>1 and n*m<=n-2,'middle test mean range')
        b=p/(n*p-1);a=(1-b)/(n-1)
        ls=[[F(1-b)*int(i==j)+b*int(j==n-1) for j in range(n)] for i in range(n-1)]
        ds=[[F(int(i==j))+(n*p-1)*int(j==n-1) for j in range(n)] for i in range(n-1)]
        w=[F(1,n-1)]*(n-1)
        for t in [F(1),F(2,3),F(1,3),F(0)]:
            dd=[[t*x+(1-t)*p for x in d] for d in ds]
            perms+=test_factor(n,p,t*a,ls,dd,w,all_perms=n<=6)
            cases+=1
        # Boundary rigidity's forced coefficients and preparation marginal.
        A,u=coefficient(ls,ds,w)
        check(all(A[i][i]==a for i in range(n-1)),'positive leading diagonal')
        check(all(A[i][j]==0 for i in range(n-1) for j in range(n-1) if i!=j),'zero leading off-diagonal')
        check(u==[a]*(n-1)+[b],'unique boundary preparation marginal')
    for s in [3,4,5]:
        n=s*s;tau=F(s-1,s+1);p0=F(1,n-s)
        for p in [p0/3,2*p0/3,p0]:
            a=p*tau;aa=F(s-1,s);bb=F(1,s)
            ls=[[aa*int(i==j)+bb*int(j==n-1) for j in range(n)] for i in range(n-1)]
            minimum=n*p*aa/(n-1)
            w=[minimum]*(n-1);w[0]+=1-sum(w)
            ds=[[n*p*x/((n-1)*w[i]) for x in ls[i]] for i in range(n-1)]
            perms+=test_factor(n,p,a,ls,ds,w)
            cases+=1
            if p==p0:check(all(x==F(1,n-1) for x in w),'low/middle boundary uniformity')
    for n in [5,6,9,16]:
        b=F(2,n)
        ls=[[(1-b)*int(i==j)+b*int(j==n-1) for j in range(n)] for i in range(n-1)]
        w=[F(1,n-1)]*(n-1)
        for t in [F(0),F(1,4),F(1,2),F(3,4)]:
            p=b+(1-b)*t;a=(1-p)/(n-1);d0=(n*p-2)/(n-2)
            ds=[[d0+(1-d0)*int(j in [i,n-1]) for j in range(n)] for i in range(n-1)]
            perms+=test_factor(n,p,a,ls,ds,w,all_perms=n<=6)
            cases+=1
    return {'factorization_cases':cases,'permutation_responses':perms,
            'full_group_enumerations':'Every permutation of S5 and S6 for the indicated cases; deterministic finite samples otherwise'}


def boundary_and_quantifier_checks():
    global GROUP
    GROUP='boundary_and_scope_checks'
    for n in range(5,101):
        p=F(2,n);a=F(n-2,n*(n-1))
        check(a==((n-1)*p-1)/((n-1)*(n*p-1))==(1-p)/(n-1),'middle/high meeting point')
        check(a<p and p+(n-1)*a==1,'physical saturation endpoint')
        check(n*n+1<__import__('math').factorial(n),'pure initializer selected over residual action')
    for s in range(3,16):
        n=s*s;p0=F(1,n-s);tau=F(s-1,s+1)
        check(p0*tau==((n-1)*p0-1)/((n-1)*(n*p0-1)),'low/middle meeting point')
        check(p0<F(2,n),'nonempty nonlinear interval')
        check(p0/(p0+F(1,s))==F(1,s),'endpoint null vector fixes last marginal')
        check(p0*tau==F(1,n+s),'endpoint diagonal lower bound')
        check(F(n-1,n+s)==1-F(1,s),'endpoint marginal sum forces all equalities')
    # Joined rank is essential: A alone can have smaller rank while the shared
    # preparation u lies outside its column space. The old separate rank bound
    # therefore cannot be silently substituted for the theorem's hypothesis.
    n=5;v=[F(1,3)]*4+[F(-1,3)];c,d=min_cost_vectors(v)
    aa=1/(sum(c)+sum(d));A=[[aa*(int(i==j)+c[i]-v[j]) for j in range(n)] for i in range(n)]
    u=[F(1,n)]*n
    check(rank(A)==n-1 and rank([A[i]+[u[i]] for i in range(n)])==n,'joined rank versus separate rank distinction')
    return {'n_range':[5,100],'perfect_square_meeting_points':13,'joined_rank_hypothesis_checked':True}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,default=Path(__file__).with_name('46-mean-contrast.tex'))
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    details={'strict_endpoints':endpoint_checks(),'signed_null_vectors':null_vector_checks(),
             'support_equality':equality_checks(),'positive_synthesis':factor_checks(),
             'boundaries_and_quantifiers':boundary_and_quantifier_checks()}
    total=sum(COUNTS.values())
    result={'schema':'general-theta.r76.mean-contrast-diagnostics.v1','status':'PASS',
            'total_checks':total,'exact_checks':total,'floating_checks':0,
            'checks_by_group':COUNTS,'groups':COUNTS,'arithmetic':['Z','Q'],
            'source_file':args.source.name,'source_sha256':sha256(args.source.read_bytes()).hexdigest(),
            'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'checks':details,'kind':'finite exact rational/integer diagnostics',
            'not':['formal proof','human referee report','priority clearance','proof of universal statements by finite enumeration']}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')

if __name__=='__main__':main()
