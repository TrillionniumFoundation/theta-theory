#!/usr/bin/env python3
"""Finite exact diagnostics for all-cycle saturation and short-channel graphs.

The disk configurations test the geometric graph lemma, which requires no
asymmetry. They do not certify the analytic inverse or an infinite theorem.
No test uses assertions that disappear under Python -O.
"""
from __future__ import annotations
from collections import Counter, deque
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
from random import Random
from math import gcd
import hashlib
import json
import re

COUNT: Counter[str] = Counter()
ROOT = Path(__file__).resolve().parents[1]

def check(ok: bool, group: str) -> None:
    if not ok:
        raise RuntimeError(group)
    COUNT[group] += 1

def det(a, b):
    return a[0]*b[1]-a[1]*b[0]

def det_gcd(cols):
    g = 0
    for a,b in combinations(cols, 2):
        g = gcd(g, abs(det(a,b)))
    return g

def bezout(a: int, b: int):
    aa, bb = abs(a), abs(b)
    x0,x1,y0,y1 = 1,0,0,1
    while bb:
        q = aa//bb
        aa,bb = bb,aa-q*bb
        x0,x1 = x1,x0-q*x1
        y0,y1 = y1,y0-q*y1
    return aa, x0*(1 if a>=0 else -1), y0*(1 if b>=0 else -1)

def column_basis(cols):
    """Return (a,b,c) for column lattice [(a,0),(b,c)], 0<=b<a."""
    c, bx = 0,0
    for x,y in cols:
        c,u,v = bezout(c,y)
        bx = u*bx+v*x
    if not c:
        raise ValueError('rank smaller than two')
    a=0
    for x,y in cols:
        a=gcd(a,abs(x-(y//c)*bx))
    if not a:
        raise ValueError('rank smaller than two')
    return a,bx%a,c

def in_lattice(v, h):
    a,b,c=h; x,y=v
    return y%c==0 and (x-(y//c)*b)%a==0

def saturation():
    rng=Random(20260929)
    families=[[(1,0),(1,2),(-1,3)],[(2,0),(0,2),(1,1)],[(3,0),(0,3)]]
    for _ in range(600):
        cols=[(rng.randint(-6,6),rng.randint(-6,6)) for __ in range(rng.randint(3,6))]
        if det_gcd(cols): families.append(cols)
    for cols in families:
        h=column_basis(cols)
        q=det_gcd(cols)
        check(h[0]*h[2]==q, 'determinantal_index')
        for v in cols: check(in_lattice(v,h), 'column_basis_membership')
        pairs=[(a,b) for a,b in combinations(cols,2) if det(a,b)]
        for u,v in pairs[:4]:
            signed_n=det(u,v); n=abs(signed_n)
            bs=[(int(F(n*det(w,v),signed_n)),int(F(n*det(u,w),signed_n))) for w in cols]
            for w,b in zip(cols,bs):
                check((u[0]*b[0]+v[0]*b[1],u[1]*b[0]+v[1]*b[1])==(n*w[0],n*w[1]),
                      'exact_scaled_cycle_coordinates')
            hh=column_basis(bs); g=det_gcd(bs)
            check(g%n==0 and g//n==q,'all_cycle_calibrated_index')
            rec=[(F(u[i]*hh[0],n),F(u[i]*hh[1]+v[i]*hh[2],n)) for i in range(2)]
            check(all(x.denominator==1 for row in rec for x in row),'saturated_basis_integral')
            rc=[(int(rec[0][j]),int(rec[1][j])) for j in range(2)]
            check(column_basis(rc)==h,'saturation_basis_matches_direct_basis')
        shuffled=list(cols); rng.shuffle(shuffled)
        reversed_cols=[((-x,-y) if i%2 else (x,y)) for i,(x,y) in enumerate(shuffled)]
        check(column_basis(reversed_cols)==h,'generator_order_and_reversal')
    base=[(1,0),(1,2),(-1,3)]
    check(sorted(abs(det(a,b)) for a,b in combinations(base,2))==[2,3,5], 'no_primitive_pair_minors')
    check(det_gcd(base)==1,'all_cycles_primitive_without_pair')
    check(det_gcd(base[:2])==2,'proper_subcatalogue_not_falsely_saturated')
    for n in range(1,31):
        for gap in (F(1,100),F(1,1000)):
            candidates=[k for k in range(1,32) if abs(F(k)-n-gap)<F(1,4)]
            check(candidates==[n], 'physical_integer_lock_separation')

def vector_add(a,b): return (a[0]+b[0],a[1]+b[1])
def vector_sub(a,b): return (a[0]-b[0],a[1]-b[1])
def norm2(v): return v[0]*v[0]+v[1]*v[1]

def short_graph(centers, periods=(80,100), radius=1, cutoff=140):
    """Exact predicates for equal disks at rational periodic centers.

All lengths are in integer units. Circle/line obstruction uses squared
cross products; no floating-point intersection or rounding is performed.
"""
    lx,ly=periods; count=len(centers)
    check((cutoff+2*radius)**2>lx*lx+ly*ly, 'range_exceeds_root_covering_bound')
    kmax=(cutoff+2*radius+max(lx,ly))//min(lx,ly)+2
    copies=[(i,k,l,(c[0]+k*lx,c[1]+l*ly))
            for i,c in enumerate(centers)
            for k in range(-kmax,kmax+1) for l in range(-kmax,kmax+1)]
    all_edges={}; clear_edges=[]
    for i,c in enumerate(centers):
        for j,k,l,z in copies:
            if (j,k,l)==(i,0,0): continue
            dv=vector_sub(z,c); ds=norm2(dv)
            if ds >= (cutoff+2*radius)**2: continue
            check(ds>(2*radius)**2,'disjoint_test_disks')
            blocker=None
            for h,a,b,w in copies:
                if (h,a,b) in ((i,0,0),(j,k,l)): continue
                rel=vector_sub(w,c); projection=rel[0]*dv[0]+rel[1]*dv[1]
                if 0<projection<ds and det(rel,dv)**2<=radius*radius*ds:
                    blocker=(h,a,b,w); break
            key=(i,j,k,l)
            all_edges[key]=(ds,blocker)
            if blocker is None:
                clear_edges.append(key)
            else:
                w=blocker[3]
                check(norm2(vector_sub(w,c))<ds and norm2(vector_sub(z,w))<ds,
                      'blocked_bridge_strict_gap_descent')
    # Check the finite recursive replacement, including absolute lift offsets.
    cache={}
    def path(key):
        if key in cache: return cache[key]
        i,j,k,l=key; ds,blocker=all_edges[key]
        if blocker is None:
            result=[(i,0,0),(j,k,l)]
        else:
            h,a,b,_=blocker
            left=path((i,h,a,b))
            right=path((h,j,k-a,l-b))
            shifted=[(v,x+a,y+b) for v,x,y in right]
            check(left[-1]==shifted[0],'descent_path_concatenation')
            result=left+shifted[1:]
        cache[key]=result
        return result
    for key in all_edges:
        route=path(key)
        check(route[0]==(key[0],0,0) and route[-1]==(key[1],key[2],key[3]),
              'descent_path_preserves_lift_endpoints')
        for a,b in zip(route,route[1:]):
            step=(a[0],b[0],b[1]-a[1],b[2]-a[2])
            check(all_edges[step][1] is None,'replacement_uses_only_clear_bridges')
    # Independent quotient spanning-tree and cycle calculation.
    adjacency={i:[] for i in range(count)}
    for i,j,k,l in clear_edges: adjacency[i].append((j,(k,l)))
    placed={0:(0,0)}; queue=deque([0])
    while queue:
        i=queue.popleft()
        for j,k in adjacency[i]:
            if j not in placed:
                placed[j]=vector_add(placed[i],k); queue.append(j)
    check(len(placed)==count,'quotient_visits_every_obstacle')
    cycles=[vector_sub(vector_add(placed[i],(k,l)),placed[j]) for i,j,k,l in clear_edges]
    check(det_gcd(cycles)==1,'complete_short_graph_generates_full_deck_lattice')
    check(column_basis(cycles)==(1,0,1),'complete_graph_basis_is_full_lattice')
    # Change representatives by arbitrary vertex lattice translations.
    shifts={i:(2*i-1,i*i+1) for i in range(count)}
    pg={i:vector_sub(placed[i],shifts[i]) for i in placed}
    gauged=[]
    for i,j,k,l in clear_edges:
        kk=vector_add((k,l),vector_sub(shifts[i],shifts[j]))
        gauged.append(vector_sub(vector_add(pg[i],kk),pg[j]))
    check(gauged==cycles,'vertex_gauge_preserves_cycle_vectors')
    return {'vertices':count,'oriented_short_pairs':len(all_edges),
            'oriented_clear_edges':len(clear_edges),'range':cutoff,'radius':radius}

def source_checks():
    text=(ROOT/'main.tex').read_text()
    files=['main.tex','references.tex']
    for name in re.findall(r'\\input\{([^}]+)\}', text):
        f=ROOT/(name+'.tex'); check(f.exists(),'active_input_present')
        text+='\n'+f.read_text(); files.append(str(f.relative_to(ROOT)))
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    check(len(labels)==len(set(labels)),'unique_labels')
    for label in re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text):
        check(label in labels,'resolved_reference')
    for required in ['lem:obstruction-descent','thm:geometric-completeness',
                     'thm:all-cycle-index','prop:no-primitive-pair',
                     'thm:catalogue-rigidity','thm:catalogue-stability',
                     'prop:ambiguity','prop:lens','thm:local-main']:
        check(required in labels,'required_result_retained')
    return {f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sorted(set(files))}

def main():
    saturation()
    cases=[]
    for centers,radius,cutoff in [([(0,0)],1,140), ([(0,0),(40,30)],1,140),
                                 ([(0,0),(40,20),(20,60)],1,140),
                                 ([(0,0),(40,20),(20,60)],2,170)]:
        cases.append(short_graph(centers,radius=radius,cutoff=cutoff))
    manifest=source_checks()
    print(json.dumps({'schema':'a2-v20-finite-diagnostics-1','status':'passed',
                      'total_checks':sum(COUNT.values()),'checks':dict(sorted(COUNT.items())),
                      'periodic_graph_cases':cases,'source_sha256':manifest,
                      'scope':'finite exact integer, rational, disk-visibility and source diagnostics',
                      'formal_proof_certificate':False},indent=2,sort_keys=True))

if __name__=='__main__': main()
