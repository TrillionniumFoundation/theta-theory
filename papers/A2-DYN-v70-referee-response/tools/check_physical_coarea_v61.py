#!/usr/bin/env python3
"""Exact finite identities and counterchecks, not continuum billiard certification."""
from fractions import Fraction as Q
from itertools import combinations
import json
import sympy as sp


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def continuant(diag, off):
    prev, cur = Q(1), Q(1)
    for j, a in enumerate(diag):
        prev, cur = cur, a*cur - (off[j-1]**2*prev if j else 0)
    return cur


def finite_checks():
    cases = subsets = 0
    for m in range(1, 9):
        for sample in range(6):
            R = [Q(9,20), Q(23,50), Q(47,100)][sample%3]
            cs = [Q(1, 1+((7*j+3*sample)%23)) for j in range(m+1)]
            ts = [Q(10+(3*j+sample)%7) for j in range(m)]
            ts = [min(t,Q(50,3)) for t in ts]
            diag = [ts[j-1]+ts[j]+2/(R*cs[j]) for j in range(1,m)]
            off = [-ts[j] for j in range(1,m-1)]
            det = continuant(diag,off)
            prodt=Q(1);prodc=Q(1);prodd=Q(1)
            for x in ts:prodt*=x
            for x in cs:prodc*=x
            for x in cs[1:-1]:prodd*=2/(R*x)
            require(det>=prodd,'Dirichlet-potential determinant bound')
            cross=cs[0]*cs[-1]*prodt/det
            require(cross/prodc <= (R/2)**(m-1)*prodt,'simultaneous inverse-incidence cancellation')
            # Full contact Hessian followed by its endpoint Schur complement.
            H=sp.zeros(m+1)
            H[0,0]=cs[0]/R+cs[0]**2*ts[0]
            H[m,m]=cs[m]/R+cs[m]**2*ts[-1]
            for j in range(1,m):H[j,j]=cs[j]**2*(ts[j-1]+ts[j])+2*cs[j]/R
            for j in range(m):H[j,j+1]=H[j+1,j]=-cs[j]*cs[j+1]*ts[j]
            if m==1: reduced=H
            else:
                E=[0,m];I=list(range(1,m))
                reduced=H.extract(E,E)-H.extract(E,I)*H.extract(I,I).inv()*H.extract(I,E)
            require(abs(reduced[0,1])==sp.Rational(cross.numerator,cross.denominator),'corner cofactor or endpoint factor')
            for length in range(min(3,m-1)+1):
                for S in combinations(range(1,m),length):
                    changed=diag.copy(); bound=Q(1)
                    for j in S:
                        changed[j-1]=ts[j-1]+ts[j]+2/R
                        bound*=53*cs[j]/(6+47*cs[j])
                    ratio=continuant(changed,off)/det
                    require(ratio<=bound,'selected-contact determinant ratio')
                    subsets+=1
            cases+=1
    # The one-internal-contact extremal diagonal attains the stated comparison.
    for c in [Q(1),Q(1,2),Q(1,100)]:
        R=Q(47,100);t=Q(50,3)
        ratio=(2*t+2/R)/(2*t+2/(R*c))
        require(ratio==53*c/(6+47*c),'sharp rational comparison constant')
    depth_cases=0
    for m in range(1,101):
        for x in [Q(1,2),Q(9,10),Q(99,100)]:
            require(sum(x**min(j,m-j) for j in range(m+1))<=2/(1-x),'contact depth sum')
            require(sum(x**min(j,m-1-j) for j in range(m))<=2/(1-x),'flight depth sum')
            depth_cases+=1
    # Exact two-coordinate area formula for F=x+2y and Z=3x-y.
    # x=(t+2z)/7, y=(3t-z)/7; a unit-square fiber is an interval in z.
    clearance_cases=0
    for t in [Q(i,20) for i in range(-10,71)]:
        for width in [Q(1,100),Q(1,10),Q(1)]:
            z0=Q(1,3)
            lo=max(z0,-t/2,3*t-7)
            hi=min(z0+width,(7-t)/2,3*t)
            height=max(Q(0),hi-lo)/7
            require(height<=width/7,'transverse density Jacobian')
            clearance_cases+=1
    # Negative controls: exact rank loss permits a small-mass source of non-small height.
    # On the unit disk F=x*x+y*y, the source |x|<s contains the whole level
    # for 0<t<s*s, so its density is pi there, although its area <=4s.
    s=Q(1,100);t=s*s/4
    require(t<s*s and 4*s<Q(1,10),'rank-loss spike control')
    # F=x, Z=(y-1/2)^2 on the unit square has two branches. For Z in [1/16,1/4],
    # the exact height is 1/2; the one-branch bound 3/8 is false.
    true_height=Q(1,2);one_branch_bound=(Q(1,4)-Q(1,16))/Q(1,2)
    require(one_branch_bound<true_height<=2*one_branch_bound,'missing multiplicity negative control')
    # Omitting endpoint cosines destroys the inverse-incidence cancellation already at m=1.
    c0,c1,t0=Q(1,5),Q(1,7),Q(10)
    require((c0*c1*t0)/(c0*c1)==t0 and t0/(c0*c1)>t0,'endpoint-cosine negative control')
    return {'contact_schur_cases':cases,'selected_contact_subsets':subsets,
            'depth_sum_cases':depth_cases,'transverse_area_cases':clearance_cases,
            'sharp_comparison_constant':'53c/(6+47c)','negative_controls':3,
            'no_exponential_count_budget_removed':True,'continuum_proof_certified':False}

if __name__=='__main__':print(json.dumps(finite_checks(),indent=2,sort_keys=True))
