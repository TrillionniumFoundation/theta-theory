#!/usr/bin/env python3
"""Independent finite mechanical and algebraic checks for A2-DYN v2.

Uses the candidate coordinates supplied by the rational certificate but imports
no author solver, action, interval arithmetic or diagnostic code. The mechanics
checks use double precision and do not certify the infinite family. Failure
checks remain enabled under python -O.
"""
from fractions import Fraction as F
from pathlib import Path
import cmath
import json
import math
import sys


class CheckFailure(RuntimeError):pass


def run(certificate_path):
    checks=0;sections={}
    def check(value,message):
        nonlocal checks
        checks+=1
        if not value:raise CheckFailure(message)
    def dot(a,b):return a[0]*b[0]+a[1]*b[1]
    def sub(a,b):return (a[0]-b[0],a[1]-b[1])
    def norm(v):return math.hypot(*v)
    def unit(v):
        s=norm(v);return (v[0]/s,v[1]/s)
    def segdist(q,p,z):
        w=sub(p,q);u=max(0.,min(1.,dot(sub(z,q),w)/dot(w,w)))
        return norm(sub(z,(q[0]+u*w[0],q[1]+u*w[1])))
    data=json.loads(Path(certificate_path).read_text())
    check(data.get('status')=='passed','certificate status')
    start=checks;least_clear=1.
    for row in data['samples']:
        R=float(F(row['R']));m=row['m'];ys=list(map(float,row['candidate_heights']))
        D=math.sqrt(3);d=.5-R;g=D-2*R
        centers=[(D/2,-.5)]+[(0.,0.) if j%2==0 else (D,0.) for j in range(2*m)]
        contacts=[(D/2,-d)]+[(math.sqrt(R*R-y*y) if j%2==0 else D-math.sqrt(R*R-y*y),y) for j,y in enumerate(ys)]
        incoming=[];outgoing=[];selected=0
        for j,q in enumerate(contacts):
            before=contacts[(j-1)%len(contacts)];after=contacts[(j+1)%len(contacts)]
            vin=unit(sub(q,before));vout=unit(sub(after,q));normal=unit(sub(q,centers[j]))
            reflected=(vin[0]-2*dot(vin,normal)*normal[0],vin[1]-2*dot(vin,normal)*normal[1])
            check(norm(sub(reflected,vout))<2e-12,'specular reflection')
            check(dot(vout,normal)>0.04,'exterior normal incidence')
            alpha=(math.atan2(normal[1],normal[0])+math.pi/6)%(2*math.pi)
            tang=(-normal[1],normal[0]);p=dot(vout,tang)
            in_U=abs(alpha-math.pi/6)<3/50 and abs(p)<3/20
            check(in_U==(j>0 and j%2==1),'new-section membership')
            selected+=int(in_U)
            endcenter=centers[(j+1)%len(centers)]
            for k in range(-2,5):
                for l in range(-4,5):
                    if (k-l)%2:continue
                    z=(D*k/2,l/2)
                    if norm(sub(z,centers[j]))<1e-12 or norm(sub(z,endcenter))<1e-12:continue
                    clearance=segdist(q,after,z)-R
                    least_clear=min(least_clear,clearance)
                    check(clearance>0.0179,'third-disk clearance on finite sample')
        check(selected==m,'physical induced period')
        check(len(contacts)==2*m+1,'physical collision count')
        length=sum(norm(sub(contacts[(j+1)%len(contacts)],q)) for j,q in enumerate(contacts))
        e=length-2*m*g
        bracket=row['excess_enclosure'];lo=float(F(int(bracket['lower_numerator']),10**75));hi=float(F(int(bracket['upper_numerator']),10**75))
        check(abs(e-(lo+hi)/2)<2e-14,'independent optical length')
    sections['independent_physical_samples']=checks-start
    start=checks
    # Determinant by independent exact Gaussian elimination. The two otherwise
    # unknown roof entries can be arbitrary; their cancellation must be exact.
    def det(matrix):
        a=[list(map(F,r)) for r in matrix];value=F(1)
        for i in range(len(a)):
            k=next((k for k in range(i,len(a)) if a[k][i]),None)
            if k is None:return F(0)
            if k!=i:a[i],a[k]=a[k],a[i];value=-value
            t=a[i][i];value*=t
            for j in range(i+1,len(a)):
                ratio=a[j][i]/t
                for z in range(i,len(a)):a[j][z]-=ratio*a[i][z]
        return value
    for l2 in (F(1,5),F(3,25),F(17,100)):
        for l3 in (F(2,5),F(3,7)):
            for l4 in (F(4,5),F(19,30)):
                matrix=[[0,0,2,1,l2],[0,0,3,1,l3],[1,0,4,1,l4],[0,1,4,1,l4],[0,0,2,1,l2+F(7,5)]]
                check(abs(det(matrix))==F(7,5),'augmented roof determinant cancellation')
    check(4*F(1,200)**2+F(3,50)*F(3,20)==F(91,10000),'exact section volume coefficient')
    # Representative bounded increasing excess sequence: phase cancellation
    # algebra, not a replacement for the actual Bellman family.
    for m in range(1,20):
        s=F(2,7);b=F(3,11);g=F(4,5);E=F(1,100)-F(1,100*2**m);c=F(9,13)
        lhs=(2*m+1)*s+b*(2*m*g+E)-m*c
        rhs=m*(2*s+2*b*g-c)+s+b*E
        check(lhs==rhs,'subtracting repeated true base period')
    sections['exact_phase_and_volume_algebra']=checks-start
    start=checks
    for n in (16,64,256,1024):
        a=n**.1;B=a/math.sqrt(n)
        check(abs(n*n*B**4-a**4)<1e-10,'mixed four-coordinate kernel scaling')
        for b in (.1,.5,1.,3.,10.):
            # A normal edge plus a smooth residual, at an arbitrary lattice mode.
            phi_edge=cmath.exp(1j*b*20)/(1-1j*b)
            phi_res=cmath.exp(-b*b/2)
            chi=math.exp(-b*b/B**2)
            phi=phi_edge+phi_res
            recon=chi*phi+(phi_edge-chi*phi_edge)+(1-chi)*phi_res
            check(abs(phi-recon)<1e-13,'exact local decomposition at finite frequencies')
    for eps in (F(1,8),F(1,4),F(1,2)):
        for a in (2,4,8,16):
            check(F(a)**4/(1+eps*a)**8>=0,'remote Schwartz bound nonnegative')
    # Kac/reward cancellation and exact stationary residual formula in a finite
    # suspension. This tests normalization, not deterministic independence.
    weights=[F(1,3),F(2,3)];roofs=[F(2),F(5)];mean=sum(p*t for p,t in zip(weights,roofs))
    for q in (F(0),F(1),F(2),F(3),F(5),F(7)):
        tail=sum(p*max(t-q,0) for p,t in zip(weights,roofs))/mean
        age=sum(p*t/mean*max(1-q/t,0) for p,t in zip(weights,roofs))
        check(tail==age,'length-biased endpoint distribution')
    sections['local_inversion_and_clock_algebra']=checks-start
    return {'schema':'a2-dyn-v2-independent-finite-checks-1','status':'passed','total_checks':checks,
            'sections':sections,'minimum_sampled_clearance':least_clear,
            'full_billiard_LLT_verified':False,'independent_human_review_completed':False,
            'scope':'Independent finite mechanics and exact algebra; no continuum or all-branch spectral certification.'}

if __name__=='__main__':
    try:
        path=sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).resolve().parents[1]/'evidence/certify_excursion.py.json')
        print(json.dumps(run(path),sort_keys=True,separators=(',',':')))
    except (ValueError,ArithmeticError,CheckFailure,KeyError,OSError) as exc:
        print(json.dumps({'status':'failed','error':str(exc)},sort_keys=True));raise SystemExit(1)
