#!/usr/bin/env python3
"""Finite diagnostics for v45; no empirical-law or infinite-jet certificate.

The disk cases test clear-segment geometry, including tangency.  The image
cases start from posed support coefficients and centers, not measured laws.
Only standard-library modules are required.  Validity checks survive -O.
"""
from __future__ import annotations
import cmath
import itertools
import json
import math
import random
from collections import deque


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def det(a: complex, b: complex) -> float:
    return a.real*b.imag-a.imag*b.real


def coords(z: complex, L: tuple[complex, complex]) -> tuple[float, float]:
    d = det(*L)
    require(abs(d) > 1e-12, 'Singular lattice')
    return det(z, L[1])/d, det(L[0], z)/d


def shift(m: tuple[int, int], L: tuple[complex, complex]) -> complex:
    return m[0]*L[0]+m[1]*L[1]


def plus(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0]+b[0], a[1]+b[1]


def minus(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0]-b[0], a[1]-b[1]


def segment_distance(z: complex, p: complex, q: complex) -> float:
    v=q-p
    t=max(0., min(1., ((z-p).conjugate()*v).real/abs(v)**2))
    return abs(z-p-t*v)


def clear_edge(a: int, b: int, m: tuple[int, int], centers: list[complex],
               radii: list[float], L: tuple[complex, complex]) -> bool:
    ca, cb=centers[a], centers[b]+shift(m,L)
    u=(cb-ca)/abs(cb-ca)
    p,q=ca+radii[a]*u,cb-radii[b]*u
    # Exact necessary coordinate bounds for a disk meeting this segment.
    rownorm=(abs(L[1])/abs(det(*L)), abs(L[0])/abs(det(*L)))
    for c, cc in enumerate(centers):
        pp,qq=coords(p-cc,L),coords(q-cc,L)
        bounds=[range(math.ceil(min(pp[i],qq[i])-radii[c]*rownorm[i]-1e-10),
                      math.floor(max(pp[i],qq[i])+radii[c]*rownorm[i]+1e-10)+1)
                for i in (0,1)]
        for ell in itertools.product(*bounds):
            if (c==a and ell==(0,0)) or (c==b and ell==m):
                continue
            if segment_distance(cc+shift(ell,L),p,q)<=radii[c]+1e-10:
                return False
    return True


def skeleton(n: int, edges: list[tuple[int,int,tuple[int,int]]]):
    parent=list(range(n))
    def root(a):
        while parent[a]!=a:
            a=parent[a]
        return a
    tree=[]
    for i,(a,b,m) in enumerate(edges):
        ra,rb=root(a),root(b)
        if ra!=rb:
            parent[ra]=rb
            tree.append(i)
    require(len(tree)==n-1,'Disconnected quotient graph')
    adj=[[] for _ in range(n)]
    for i in tree:
        a,b,m=edges[i]
        adj[a].append((b,i,1)); adj[b].append((a,i,-1))
    potential=[None]*n; potential[0]=(0,0)
    order=[]; queue=deque([0])
    while queue:
        a=queue.popleft()
        for b,i,sign in adj[a]:
            if potential[b] is None:
                m=edges[i][2]
                potential[b]=plus(potential[a],(sign*m[0],sign*m[1]))
                order.append((a,b,i,sign)); queue.append(b)
    gains={i:minus(plus(potential[a],m),potential[b])
           for i,(a,b,m) in enumerate(edges) if i not in tree}
    for i,j in itertools.combinations(gains,2):
        x,y=gains[i],gains[j]
        d=x[0]*y[1]-x[1]*y[0]
        if d:
            return tree,[i,j],potential,order,[x,y]
    raise RuntimeError('Deck gain has rank below two')


def register_images(edges, design, records):
    """Inputs contain no generating lattice or obstacle locations."""
    tree,extra,pot,order,gains=design
    n=len(pot)
    seed=next(i for i,e in enumerate(edges) if e[0]==0 or e[1]==0)
    end=0 if edges[seed][0]==0 else 1
    template={0:records[seed][end][1]}
    rotations={}
    def match(source,target):
        require(abs(source[2]*source[3]*target[2]*target[3])>1e-18,'Missing harmonic anchor')
        U=source[3]*target[2]/(target[3]*source[2])
        require(abs(abs(U)-1)<1e-9,'Inconsistent harmonic ratio')
        return U/abs(U)
    for a,b,i,sign in order:
        side=0 if sign==1 else 1
        U=match(records[i][side][1],template[a]); rotations[i]=U
        template[b]={k:records[i][1-side][1][k]*U**(-k) for k in (2,3,4,7,11)}
    for i in extra:
        a,b,m=edges[i]
        rotations[i]=match(records[i][0][1],template[a])
    displacements={i:rotations[i]*(records[i][1][0]-records[i][0][0]) for i in tree+extra}
    p=[0j]*n
    for a,b,i,sign in order:
        p[b]=p[a]+sign*displacements[i]
    V=[]
    for i in extra:
        a,b,m=edges[i]
        V.append(p[a]+displacements[i]-p[b])
    x,y=gains
    d=x[0]*y[1]-x[1]*y[0]
    require(d!=0,'Singular gain matrix')
    L=((V[0]*y[1]-V[1]*x[1])/d,(-V[0]*y[0]+V[1]*x[0])/d)
    centers=[p[a]-shift(pot[a],L) for a in range(n)]
    return L,centers,seed


def image_case(edges, design, centers, L, rng):
    modes=[{k:cmath.rect(.002/(k*k),rng.uniform(-3,3)) for k in (2,3,4,7,11)} for _ in centers]
    records={}; poses={}
    for i in design[0]+design[1]:
        a,b,m=edges[i]; U=cmath.rect(1,rng.uniform(-3,3)); t=complex(rng.uniform(-8,8),rng.uniform(-8,8))
        poses[i]=U
        records[i]=[((centers[a]-t)/U,{k:U**k*z for k,z in modes[a].items()}),
                    ((centers[b]+shift(m,L)-t)/U,{k:U**k*z for k,z in modes[b].items()})]
    # The root seed must be among the selected channels.
    selected=design[0]+design[1]
    remap={j:i for i,j in enumerate(selected)}
    es=[edges[j] for j in selected]
    ds=([remap[j] for j in design[0]],[remap[j] for j in design[1]],design[2],
        [(a,b,remap[j],s) for a,b,j,s in design[3]],design[4])
    rs={remap[j]:records[j] for j in selected}
    got,c,seed=register_images(es,ds,rs)
    gauge=1/poses[selected[seed]]
    error=max(abs(got[k]-gauge*L[k]) for k in (0,1))
    center_error=max(abs(c[a]-gauge*(centers[a]-centers[0])) for a in range(len(centers)))
    gram_error=max(abs((got[i].conjugate()*got[j]).real-(L[i].conjugate()*L[j]).real) for i in (0,1) for j in (0,1))
    require(max(error,center_error,gram_error)<1e-8,'Image reconstruction residual')
    # Negative control: the denominator is not silently divided through.
    damaged={j:[(c0,dict(z)) for c0,z in r] for j,r in rs.items()}
    for r in damaged.values():
        for c0,z in r:
            z[3]=0j
    try:
        register_images(es,ds,damaged)
    except RuntimeError:
        pass
    else:
        raise RuntimeError('Zero harmonic anchor was accepted')
    return error,center_error,gram_error


def main():
    rng=random.Random(450914); cases=0; image_cases=0; maxerr=[0.,0.,0.]; total_edges=0
    for n in range(1,7):
        for repeat in range(3):
            L=(10+complex(.2*rng.random(),.1*rng.random()), .3*rng.random()+11j)
            centers=[complex(1+3*(a%3),1+4*(a//3)) for a in range(n)]
            radii=[.25+.05*rng.random() for a in range(n)]
            gap=lambda a,b,m:abs(centers[b]+shift(m,L)-centers[a])-radii[a]-radii[b]
            D0=max([gap(0,a,(0,0)) for a in range(1,n)]+[gap(0,0,(1,0)),gap(0,0,(0,1))])
            R=max(abs(c)+r for c,r in zip(centers,radii))
            # 1/||L^{-1}||_F is a rigorous lower bound for s_min(L).
            s=abs(det(*L))/math.sqrt(abs(L[0])**2+abs(L[1])**2)
            bound=math.ceil((D0+2*R)/s)
            candidates=[]
            for a in range(n):
                for b in range(a,n):
                    for m in itertools.product(range(-bound,bound+1),repeat=2):
                        if a==b and not (m[0]>0 or m[0]==0 and m[1]>0):
                            continue
                        g=gap(a,b,m)
                        require(g>0,'Overlapping disk test table')
                        if g<=D0+1e-10 and clear_edge(a,b,m,centers,radii,L):
                            candidates.append((a,b,m))
            candidates.sort(key=lambda e:gap(*e))
            design=skeleton(n,candidates)
            require(len(design[0])+len(design[1])==n+1,'Wrong channel count')
            total_edges+=len(candidates); cases+=1
            for _ in range(4):
                err=image_case(candidates,design,centers,L,rng)
                maxerr=[max(a,b) for a,b in zip(maxerr,err)]; image_cases+=1
    # Tangential blocking is not a clear channel.
    centers=[0j,4+0j,2+1j]; radii=[.2,.2,1.]
    require(not clear_edge(0,1,(0,0),centers,radii,(20+0j,20j)),'Tangency accepted')
    d01=3.6; d02=math.sqrt(5)-1.2; d21=d02
    require(d02+d21<=d01 and max(d02,d21)<d01,'Tangency descent failed')
    rejected=0
    for n,es in [(2,[(0,0,(1,0)),(0,0,(0,1))]),
                 (1,[(0,0,(1,0)),(0,0,(2,0))]),
                 (2,[(0,1,(0,0))])]:
        try: skeleton(n,es)
        except RuntimeError: rejected+=1
        else: raise RuntimeError('Invalid graph accepted')
    # A rank-two sublattice is enough; its integer determinant need not be one.
    es=[(0,0,(2,0)),(0,0,(0,3))]; ds=skeleton(1,es)
    err=image_case(es,ds,[0j],(7+.2j,.4+9j),rng)
    maxerr=[max(a,b) for a,b in zip(maxerr,err)]; image_cases+=1
    print(json.dumps({'status':'passed','disk_tables':cases,'clear_candidates':total_edges,
        'posed_image_cases':image_cases,'max_lattice_residual':maxerr[0],
        'max_center_residual':maxerr[1],'max_gram_residual':maxerr[2],
        'tangent_obstruction_rejected':True,'invalid_graphs_rejected':rejected,
        'nonunimodular_gain_determinant':6,'zero_harmonic_negative_controls':image_cases,
        'scope':'Finite disk geometry and recovered-image algebra only; not a proof or empirical-law-to-infinite-jet reconstruction.'},sort_keys=True,indent=2))

if __name__=='__main__':
    main()
