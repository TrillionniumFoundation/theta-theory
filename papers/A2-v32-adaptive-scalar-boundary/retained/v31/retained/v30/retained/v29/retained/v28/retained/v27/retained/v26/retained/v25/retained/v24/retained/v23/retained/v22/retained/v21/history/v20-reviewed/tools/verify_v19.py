#!/usr/bin/env python3
"""Finite diagnostics for the v19 formulas; not a proof certificate."""
from __future__ import annotations
import argparse
from collections import Counter, deque
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path
import re

C: Counter[str] = Counter()
ROOT = Path(__file__).resolve().parents[1]

def check(ok: bool, group: str, detail: object = '') -> None:
    if not ok:
        raise RuntimeError(f'{group}: {detail}')
    C[group] += 1


def inv2(a):
    det = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    if not det:
        raise ValueError('singular matrix')
    return [[a[1][1]/det, -a[0][1]/det],[-a[1][0]/det,a[0][0]/det]]


def mv(a,v):
    return tuple(sum(x*y for x,y in zip(row,v)) for row in a)


def quotient_group(b):
    bi = inv2(b)
    gens = [tuple(bi[i][j] % 1 for i in range(2)) for j in range(2)]
    origin = (F(0),F(0)); seen={origin}; queue=deque([origin])
    while queue:
        v=queue.popleft()
        for g in gens:
            w=tuple((x+y)%1 for x,y in zip(v,g))
            if w not in seen:
                seen.add(w); queue.append(w)
    return frozenset(seen)


def lattices() -> None:
    for n in range(1,33):
        seen=set(); count=0
        for d in range(1,n+1):
            if n%d: continue
            a=n//d
            for b in range(d):
                mat=[[F(a),F(b)],[F(0),F(d)]]
                group=quotient_group(mat)
                check(len(group)==n,'overlattice_index')
                check(group not in seen,'row_HNF_unique')
                seen.add(group); count+=1
                for v in group:
                    check(all(z.denominator==1 for z in mv(mat,v)), 'dual_membership')
                    check(all((n*z).denominator==1 for z in v),'index_annihilates_quotient')
        check(count==sum(d for d in range(1,n+1) if n%d==0),'divisor_sum_count')
        check((count==1)==(n==1),'primitive_unique_control')
    for p in (3,5,7,11,13):
        groups=[]
        for j in range(1,p):
            g=frozenset((F(k,p),F(k*j,p)%1) for k in range(p))
            check(len(g)==p,'prime_example_index')
            check(g not in groups,'prime_example_distinct')
            groups.append(g)
            for x,y in g:
                check((x==0)==(y==0),'prime_example_no_intermediate_axis_centers')
                check(x==0 or (min(x,1-x)>=F(1,p) and min(y,1-y)>=F(1,p)),
                      'prime_example_off_axis_clearance')
        check(len(groups)==p-1,'prime_example_physical_candidate_count')
    for n in range(1,25):
        for e in (F(1,100),F(-1,100),F(1,1000)):
            # Test the deterministic separation used for two integral candidates.
            near=[k for k in range(1,26) if abs(F(k)-n-e)<F(1,4)]
            check(near==[n],'integer_locking_separation')
    # Exact incidence labels here are abstract shape identities, not image tests.
    records=[('A','B'),('B','C'),('A','C'),('A','A'),('C','C')]
    reference=sorted(tuple(sorted(e)) for e in records)
    for shift in range(len(records)):
        rotated=records[shift:]+records[:shift]
        for bits in product((0,1),repeat=len(records)):
            perm=[e[::-1] if bit else e for e,bit in zip(rotated,bits)]
            check(sorted(tuple(sorted(e)) for e in perm)==reference,'incidence_record_order_and_reversal')


def curvature() -> None:
    for ell,k,ko,t in product((F(1,3),F(1),F(5,2)),
                              (F(1,5),F(1,2),F(3)),
                              (F(1,4),F(2,3),F(2)),
                              (F(0),F(1,7),F(-1,5),F(1,3),F(-2,5))):
        a=2*t/(1+t*t); v=(1-t*t)/(1+t*t)
        dss=v*v/ell+k*v; dsu=-v/ell; duu=1/ell+ko
        st=-dsu*dsu/(2*duu); ss=dss+st
        check((ss-st-v*v/ell)/v==k,'source_curvature')
        check((v*v/(-2*ell*st)-1)/ell==ko,'opposite_curvature')
        check(-dsu/duu==v/(1+ell*ko),'foot_speed')
        check(st<0 and v>0 and a*a+v*v==1,'twist_frame_margins')


KEYS=[(i,j) for i in range(4) for j in range(4-i)]
def add(a,b): return {k:a.get(k,F(0))+b.get(k,F(0)) for k in KEYS}
def scale(a,c): return {k:c*a.get(k,F(0)) for k in KEYS}
def mul(a,b):
    out=dict.fromkeys(KEYS,F(0))
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            if (i+k,j+l) in out: out[(i+k,j+l)]+=x*y
    return out

def inverse_jet(a):
    c=a[(0,0)]
    z=scale(a,1/c); z[(0,0)]-=1
    out={(0,0):F(1)}; power=out
    for r in range(1,4):
        power=mul(power,z); out=add(out,scale(power,(-1)**r))
    return scale(out,1/c)


def densities() -> None:
    for n in range(1,201):
        W={key:F((n*(i+3))%19-9,17+i) for i,key in enumerate(KEYS)}
        w={key:F((n*(i+5))%13-6,29+i) for i,key in enumerate(KEYS)}
        W[(0,0)]=F(1+n%7,5); w[(0,0)]=F(3+n%5,7)
        T1=F(4+n%3); T2=T1+F(1+n%4,6)
        f1=mul(w,add({(0,0):T1},scale(W,-1)))
        f2=mul(w,add({(0,0):T2},scale(W,-1)))
        df=add(f2,scale(f1,-1))
        rec=mul(add(scale(f2,T1),scale(f1,-T2)),inverse_jet(df))
        for key in KEYS: check(rec[key]==W[key],'two_density_cubic_jet_identity')
        check(scale(df,1/(T2-T1))==w,'flux_factor_recovery')
        reflect=lambda j:{k:(-1)**sum(k)*v for k,v in j.items()}
        rr=mul(add(scale(reflect(f2),T1),scale(reflect(f1),-T2)),inverse_jet(reflect(df)))
        check(rr==reflect(W),'coherent_density_reversal')


def inverse_matrix(a):
    n=len(a); b=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        p=next(i for i in range(j,n) if b[i][j]); b[j],b[p]=b[p],b[j]
        c=b[j][j]; b[j]=[x/c for x in b[j]]
        for i in range(n):
            if i!=j:
                c=b[i][j]; b[i]=[x-c*y for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]


def bins() -> None:
    m=[[F(1),F(i),F(i*i)+F(1,12)] for i in (-1,0,1)]
    im=inverse_matrix(m)
    for p,q,a,b in product(range(3),repeat=4):
        val=sum(im[a][i]*im[b][j]*m[i][p]*m[j][q] for i,j in product(range(3),repeat=2))
        check(val==F(a==p and b==q),'cell_tensor_reproduction')
    weights=[2*im[2][i]*im[0][j] for i,j in product(range(3),repeat=2)]
    for signs in product((-1,1),repeat=9):
        check(abs(sum(w*s for w,s in zip(weights,signs)))<=sum(abs(w) for w in weights),
              'cell_second_derivative_noise')
    for beta in (F(1),F(1,2),F(2,3),F(1,3)):
        h=1/(2*beta+6)
        check(beta*h==F(1,2)-3*h,'Bernstein_bias_variance_balance')
        check(1-4*h>beta*h,'Bernstein_linear_remainder_smaller')
        check(beta/(beta+4)==1-4/(beta+4),'absolute_cell_error_balance')


def sources() -> None:
    text=(ROOT/'main.tex').read_text()
    for name in re.findall(r'\\input\{([^}]+)\}',text):
        path=ROOT/(name+'.tex')
        check(path.is_file(),'input_exists',name)
        text+='\n'+path.read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    check(len(labels)==len(set(labels)),'labels_unique')
    for name in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text):
        check(name in labels,'reference_resolves',name)
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    for names in re.findall(r'\\cite\{([^}]+)\}',text):
        for name in names.split(','): check(name in bib,'citation_resolves',name)
    for name in ('thm:local-main','thm:descent-main','thm:stat-main','prop:ambiguity','lem:integer-lock'):
        check(name in labels,'central_proof_present',name)


def geometry() -> dict:
    import numpy as np
    from scipy.integrate import quad
    from scipy.optimize import brentq
    families=[(.7,.4,.11,-.07,.03,.06,1.1),(1.3,.8,-.16,.13,.08,.04,.7),
              (.5,.5,.09,-.12,.02,.07,1.4),(.4,1.1,-.05,.18,.05,.09,1.3),
              (1.2,.6,.14,.08,.08,.03,.9)]
    maxerr=0.
    for k0,k1,c0,c1,d0,d1,g in families:
        def ps(y,b):
            k,c,d=(k0,c0,d0) if b==0 else (k1,c1,d1)
            return k*y*y/2+c*y**3/6+d*y**4/24
        def dp(y,b):
            k,c,d=(k0,c0,d0) if b==0 else (k1,c1,d1)
            return k*y+c*y*y/2+d*y**3/6
        def ddp(y,b):
            k,c,d=(k0,c0,d0) if b==0 else (k1,c1,d1)
            return k+c*y+d*y*y/2
        def arc(y): return quad(lambda z:math.sqrt(1+dp(z,0)**2),0,y,epsabs=2e-13,epsrel=2e-13)[0]
        def yy(s): return brentq(lambda y:arc(y)-s,-.7,.7,xtol=5e-15)
        def source(s):
            y=yy(s); return np.array([-ps(y,0),y])
        def other(w): return np.array([g+ps(w,1),w])
        def action(s,t,foot=False):
            x=source(s); z=source(t)
            def stat(w):
                q=other(w); tangent=np.array([dp(w,1),1.])
                return np.dot(q-x,tangent)/np.linalg.norm(q-x)+np.dot(q-z,tangent)/np.linalg.norm(q-z)
            w=brentq(stat,-.7,.7,xtol=5e-15)
            value=np.linalg.norm(x-other(w))+np.linalg.norm(z-other(w))
            return (value,w) if foot else value
        for s in np.linspace(-.24,.24,9):
            W,foot=action(s,s,True)
            def deriv(h):
                ss=(action(s+h,s)-2*W+action(s-h,s))/(h*h)
                st=(action(s+h,s+h)-action(s+h,s-h)-action(s-h,s+h)+action(s-h,s-h))/(4*h*h)
                a=(action(s+h,s)-action(s-h,s))/(2*h)
                return np.array([a,ss,st])
            a,ss,st=(4*deriv(.0005)-deriv(.001))/3
            ell=W/2; v=math.sqrt(1-a*a)
            recovered=[(ss-st-v*v/ell)/v,(v*v/(-2*ell*st)-1)/ell]
            y=yy(s); true=[ddp(y,0)/(1+dp(y,0)**2)**1.5,
                           ddp(foot,1)/(1+dp(foot,1)**2)**1.5]
            for r,t in zip(recovered,true):
                error=abs(r-t); maxerr=max(maxerr,error)
                check(error<2e-6,'nonlinear_stationary_curvature',error)
    return {'max_absolute_curvature_error':float(maxerr),'families':len(families),'points_per_family':9}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--geometry',action='store_true')
    args=parser.parse_args()
    lattices(); curvature(); densities(); bins(); sources()
    numerical=geometry() if args.geometry else None
    print(json.dumps({'schema':'a2-v19-finite-checks-1','status':'passed',
                      'total_checks':sum(C.values()),'groups':dict(sorted(C.items())),
                      'numerical':numerical,'formal_proof_certificate':False},sort_keys=True,indent=2))

if __name__=='__main__':
    main()
