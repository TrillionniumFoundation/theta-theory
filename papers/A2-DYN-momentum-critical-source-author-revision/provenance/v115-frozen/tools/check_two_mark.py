#!/usr/bin/env python3
"""Exact second-mark geometry and finite actual-flight diagnostics.

NOT a continuum/all-word theorem or a proof of the raw pointwise LLT.
Raises RuntimeError on any failed check, both under normal and -O Python.
"""
import json, math
from fractions import Fraction as Q
import numpy as np


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


def lattice(a,b):
    return (a+b/2, b*math.sqrt(3)/2)


def roots_for_w(w, target):
    wx,wy=w
    mag=math.hypot(wx,wy)
    check(abs(target)<mag, 'root transversality domain')
    phi=math.atan2(wy,wx)
    v=math.asin(target/mag)
    return (phi-v,phi-math.pi+v)


def symbol_and_roots():
    # Radius, separation gap and second Jacobian bound are exact rational identities.
    max_transverse = 2*(Q(47,100)+Q(3,200))
    check(max_transverse == Q(97,100),'physical maximal separation ratio')
    check(1-max_transverse**2 == Q(591,10000),'positive discriminant exact')
    c0=math.sqrt(591)/100
    cases=0
    w_list=[lattice(a,b) for a,b in [(1,0),(0,1),(1,1),(2,-1),(-1,2),(2,0)]]
    for R in [Q(9,20),Q(23,50),Q(47,100)]:
        for u1 in [Q(1,300),Q(1,150),Q(1,100)]:
            for u2 in [Q(1,400),Q(1,250),Q(1,110)]:
                for s1 in [-1,1]:
                    for s2 in [-1,1]:
                        diff=float(s2*(R+u2)-s1*(R+u1))
                        for w in w_list:
                            d=math.hypot(*w)
                            angles=roots_for_w(w,diff)
                            check(len(angles)==2,'two circle solutions')
                            for theta in angles:
                                cos,sin=math.cos(theta), math.sin(theta)
                                cross=w[1]*cos-w[0]*sin
                                longitudinal=w[0]*cos+w[1]*sin
                                exact=math.sqrt(d*d-diff*diff)
                                check(abs(cross-diff)<1e-12,'signed impact root')
                                check(abs(abs(longitudinal)-exact)<1e-12,'change-of-variables Jacobian')
                                check(exact+1e-12>=c0,'uniform physical separation constant')
                                cases+=1
    return {'two_mark_exact_root_checks':cases,'physical_gap_sq':'591/10000'}


def pair_band_integral():
    # Analytical angular coarea for two arcsine branches vs direct angle mesh.
    comparisons=0
    N=131072
    angles=2*np.pi*(np.arange(N)+.5)/N
    for R in [.45,.46,.47]:
        for w in [lattice(1,0),lattice(0,1),lattice(1,1)]:
            d=math.hypot(*w)
            proj=w[1]*np.cos(angles)-w[0]*np.sin(angles)
            for sign in [-1,1]:
                b1=sign*(R+.006)
                half=.009
                analytic=0.
                measured=0.
                for side in [-1,1]:
                    left,right=sorted([side*R,side*(R+half)])
                    xlo,xhi=(left-b1)/d,(right-b1)/d
                    check(-1<xlo<xhi<1,'arcsine interior')
                    analytic += 2*(math.asin(xhi)-math.asin(xlo))
                    measured += 2*math.pi*float(np.mean((b1+proj>left)&(b1+proj<right)))
                check(abs(analytic-measured)<1.1e-4,'two-branch coarea angular band')
                check(analytic <=4*half/(math.sqrt(591)/100)+1e-12,
                      'quadratic flux angular factor')
                comparisons+=1
    return {'arcsine_angular_coarea_tests':comparisons,'angular_grid_size':N}


def physical_flights():
    # True specular next-hit rays from a triangular lattice, not a Markov surrogate.
    centers=np.array([lattice(a,b) for a in range(-4,5) for b in range(-4,5)])
    total=0; nonzero_clearance=0; double_marks=0
    for R in [.45,.46,.47]:
        for i in range(1000):
            alpha=2*math.pi*((i*0.618033988749895)%1)
            p=1.98*((i*0.754877666246693)%1)-.99
            n=np.array([math.cos(alpha),math.sin(alpha)])
            tangent=np.array([-n[1],n[0]])
            q=R*n
            v=math.sqrt(1-p*p)*n+p*tangent
            z=centers-q
            along=z@v
            discr=R*R-(np.sum(z*z,axis=1)-along*along)
            hit=along-np.sqrt(np.maximum(discr,0))
            valid=(discr>1e-12)&(hit>1e-8)
            times=np.where(valid,hit,np.inf)
            k=int(np.argmin(times)); tau=times[k]
            check(math.isfinite(tau),'next true collision within lattice scan')
            foot=z@v
            dist=np.sqrt(np.maximum(0,np.sum(z*z,axis=1)-foot*foot))
            marks=np.where((foot>1e-8)&(foot<tau-1e-8)&(dist>R+1e-9)&
                           (dist<R+.012)&(np.arange(len(centers))!=k))[0]
            if len(marks):nonzero_clearance+=1
            if len(marks)>1:
                double_marks+=1
                for a in marks:
                    for b in marks:
                        if a==b:continue
                        w=centers[a]-centers[b]
                        check(abs(w@v)>=math.sqrt(591)/100-1e-9,
                              'actual two-mark transversality')
            total+=1
    return {'actual_physical_collision_rays':total,
            'sample_with_clearance':nonzero_clearance,
            'sample_with_multiple_marks':double_marks,
            'sample_is_not_continuum_proof':True}


if __name__=='__main__':
    data={'status':'passed','exact':symbol_and_roots(),
          'analytic_coarea':pair_band_integral(),
          'actual_lorentz_flights':physical_flights(),
          'full_raw_pointwise_LLT_certified':False}
    print(json.dumps(data,indent=2,sort_keys=True))
