#!/usr/bin/env python3
"""Deterministic finite fixtures for the physical cap argument; not proof certification."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import math
import numpy as np


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def checks() -> dict[str, int]:
    counts = dict(cap_cover=0, curvature=0, supporting_action=0,
                  determinant=0, gauss_integral=0, trace_tail=0, scope_controls=0)
    axes = np.array([(math.cos(j*math.pi/8), math.sin(j*math.pi/8)) for j in range(16)])
    for a in np.linspace(0, 2*math.pi, 129):
        n = np.array([math.cos(a), math.sin(a)])
        for d in (-math.pi/2+1e-10, -.9, 0., .9, math.pi/2-1e-10):
            w = np.array([math.cos(a+d), math.sin(a+d)])
            require(bool(np.any((axes@n > .5) & (axes@w > .5))), 'endpoint cover')
            counts['cap_cover'] += 1
    require(F(5,16) < F(1,3), 'exact covering angle')
    require(F(1,2)/F(47,100) == F(50,47), 'lower curvature constant')
    require(F(8)/F(3,50)+F(8)/F(9,20) == F(1360,9), 'upper curvature constant')

    # Actual first-hit trajectories. Outside this lattice box every center is
    # at distance at least 3*sqrt(3); ell<4 excludes an earlier outside hit.
    # Every collision is retained; no source claim is based on the fixtures.
    lattice = np.array([(i+j/2, j*math.sqrt(3)/2) for i in range(-5,6)
                        for j in range(-5,6) if i or j])
    rng = np.random.default_rng(750168)
    for R in (.45,.46,.47):
        for m in (1,2,4,8,16,32):
            for trial in range(6):
                a = rng.uniform(0,2*math.pi); p = rng.uniform(-.97,.97)
                n = np.array([math.cos(a),math.sin(a)])
                v = math.sqrt(1-p*p)*n+p*np.array([-n[1],n[0]])
                Q = [R*n]; C = [np.zeros(2)]; N = [n]; V=[]; L=[]; inc=[float(n@v)]
                for j in range(m):
                    centers=C[-1]+lattice; z=Q[-1]-centers
                    proj=z@v; disc=proj*proj-(np.sum(z*z,axis=1)-R*R)
                    roots=np.full(len(centers),np.inf); good=disc>1e-12
                    roots[good]=-proj[good]-np.sqrt(disc[good])
                    roots[roots<1e-9]=np.inf; k=int(np.argmin(roots)); ell=float(roots[k])
                    require(math.isfinite(ell) and .06-1e-9 <= ell < 4, 'physical first-hit flight')
                    q=Q[-1]+ell*v; nn=(q-centers[k])/R
                    nn=nn/np.linalg.norm(nn); c=-float(v@nn)
                    require(c>0, 'positive physical incidence')
                    V.append(v.copy()); L.append(ell); Q.append(q); C.append(centers[k])
                    N.append(nn); inc.append(c); v=v+2*c*nn
                    v=v/np.linalg.norm(v)
                endw=[V[0],-V[-1]]; js=[]; ss=[]
                for idx,w in zip((0,m),endw):
                    cand=np.where((axes@N[idx]>.5)&(axes@w>.5))[0]
                    require(len(cand)>0,'physical cap'); j=int(cand[0]); js.append(j)
                    e=axes[j]; ep=np.array([-e[1],e[0]])
                    ss.append(float((Q[idx]-C[idx])@ep))
                deriv=[np.array([-nn[1],nn[0]]) for nn in N]
                for idx,j,s in zip((0,m),js,ss):
                    e=axes[j]; ep=np.array([-e[1],e[0]])
                    deriv[idx]=ep-s/math.sqrt(R*R-s*s)*e
                H=np.zeros((m+1,m+1))
                for j,(v,ell) in enumerate(zip(V,L)):
                    P=(np.eye(2)-np.outer(v,v))/ell
                    H[j,j]+=deriv[j]@P@deriv[j]
                    H[j+1,j+1]+=deriv[j+1]@P@deriv[j+1]
                    off=-deriv[j]@P@deriv[j+1]; H[j,j+1]+=off; H[j+1,j]+=off
                for j in range(1,m): H[j,j]+=2*inc[j]/R
                for idx,j,s,w in zip((0,m),js,ss,endw):
                    H[idx,idx]+=float(w@axes[j])*R*R/(R*R-s*s)**1.5
                ids=[0,m]; reduced=H[np.ix_(ids,ids)]
                if m>1:
                    inside=list(range(1,m)); A=H[np.ix_(inside,inside)]
                    require(float(np.linalg.eigvalsh(A).min())>0,'internal contact Hessian')
                    cross=H[np.ix_(ids,inside)]
                    reduced=reduced-cross@np.linalg.solve(A,cross.T)
                eigen=np.linalg.eigvalsh(reduced)
                require(eigen[0]>=50/47-2e-7 and eigen[-1]<=1360/9+2e-7,
                        'physical reduced-Hessian sandwich')
                counts['curvature']+=1
                for _ in range(4):
                    trialq=[]
                    for idx,c in enumerate(C):
                        if idx in (0,m):
                            pos=0 if idx==0 else 1; e=axes[js[pos]]; ep=np.array([-e[1],e[0]])
                            s=float(rng.uniform(-.85*R,.85*R))
                            trialq.append(c+s*ep+math.sqrt(R*R-s*s)*e)
                        else:
                            a=float(rng.uniform(0,2*math.pi)); rr=R*math.sqrt(float(rng.uniform()))
                            trialq.append(c+rr*np.array([math.cos(a),math.sin(a)]))
                    triallength=sum(float(np.linalg.norm(y-x)) for x,y in zip(trialq,trialq[1:]))
                    support=sum(L)-endw[0]@(trialq[0]-Q[0])-endw[1]@(trialq[-1]-Q[-1])
                    require(triallength>=support-2e-8,'global supporting action')
                    counts['supporting_action']+=1

    # Exact normal-bounce contact determinant versus the collision twist product.
    for R in (F(9,20),F(23,50),F(47,100)):
        ell=1-2*R; v=ell/R
        P=((v+1,v),(v+2,v+1)); M=((F(1),F(0)),(F(0),F(1)))
        dets=[F(1),2/ell+2/R]
        for j in range(2,25): dets.append((2/ell+2/R)*dets[-1]-dets[-2]/ell**2)
        for m in range(1,25):
            M=tuple(tuple(sum((M[i][k]*P[k][j] for k in range(2)),F(0))
                          for j in range(2)) for i in range(2))
            require(1/M[0][1] == R*ell**(-m)/dets[m-1], 'exact twist/contact identity')
            require(ell**(-m)/dets[m-1] <= (R/2)**(m-1)*ell**(-m), 'incidence gain')
            counts['determinant']+=1

    # Ellipse coarea with the Gauss angle, without a component-count multiplier.
    theta=np.linspace(0,2*math.pi,65536,endpoint=False)
    for a,b in ((1.,1.),(2.,3.),(50/47,1360/9)):
        n=np.stack((np.cos(theta),np.sin(theta)),axis=1)
        tangent=np.stack((-n[:,1],n[:,0]),axis=1)
        ht=a*tangent[:,0]**2+b*tangent[:,1]**2
        val=2*math.pi*float(np.mean(1/ht))
        require(abs(val-2*math.pi/math.sqrt(a*b))<1e-10,'Gauss coarea identity')
        require(val <=2*math.pi/min(a,b)+1e-10,'uniform level integral')
        counts['gauss_integral']+=1

    # Exact step-trace fixtures; whole trace is summed before the positive part.
    for raw in itertools.product(range(3),repeat=4):
        height=list(map(F,raw)); trace=[(h*F(i%2),h*F(1-i%2)) for i,h in enumerate(height)]
        for i in range(4):
            for r in (F(3,2),F(5,2),F(4)):
                t=F(2*i+1,2); tail=F(0); levels=sorted(set([F(0)]+height))
                for lo,hi in zip(levels,levels[1:]):
                    u=(lo+hi)/2
                    if height[i]<=u: continue
                    l=i; h=i+1
                    while l>0 and height[l-1]>u: l-=1
                    while h<4 and height[h]>u: h+=1
                    if h-l<r: tail+=hi-lo
                losses=[]
                for sign in (-1,1):
                    vals=[]
                    for j in range(-5,9):
                        lo,hi=max(F(j),t-r if sign<0 else t),min(F(j+1),t if sign<0 else t+r)
                        if lo>=hi: continue
                        other=trace[j] if 0<=j<4 else (F(0),F(0))
                        vals.append(sum((max(F(0),a-b) for a,b in zip(trace[i],other)),F(0)))
                    losses.append(max(vals,default=F(0)))
                require(tail<=min(losses),'paired complete-trace tail')
                counts['trace_tail']+=1
    for m in (2,4,8,16):
        # Generic logical control, NOT a counterexample to physical Lorentz dynamics.
        width=F(1,m**4); density=F(1,m*m)
        require(m*m*density*(1-width)>F(1,2),'wordwise geometry alone is not dynamical decay')
        counts['scope_controls']+=1
    return counts


if __name__=='__main__':
    import json
    print(json.dumps(checks(),indent=2,sort_keys=True))
