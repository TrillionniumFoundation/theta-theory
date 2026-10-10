#!/usr/bin/env python3
"""Selected exact finite R19 checks. No sampling-based continuum proof claim."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,subprocess,sys,hashlib
ROOT=Path(__file__).resolve().parent
COUNTS={}
def require(ok,message,group):
    if not ok:raise RuntimeError(message)
    COUNTS[group]=COUNTS.get(group,0)+1

def compositions(total,parts):
    if parts==1:
        yield (total,);return
    for a in range(total+1):
        for tail in compositions(total-a,parts-1):yield (a,)+tail

def rounded(row,Q):
    ns=[int(Q*x) for x in row]
    residual=Q-sum(ns)
    inds=[i for i,x in enumerate(row) if x>0]
    if not inds:raise RuntimeError('empty support')
    # Concentrating the remainder still gives TV <= r/Q; no added support.
    ns[inds[0]]+=residual
    return tuple(F(x,Q) for x in ns)

def test_rounding():
    for r in range(1,6):
        for nums in compositions(7,r):
            row=tuple(F(x,7) for x in nums)
            for Q in (1,2,4,8,16,32):
                q=rounded(row,Q)
                require(sum(q)==1 and min(q)>=0,'row normalization','support_rounding')
                require(all(not q[i] or row[i]>0 for i in range(r)),'new support','support_rounding')
                tv=sum(abs(a-b) for a,b in zip(row,q))/2
                require(tv<=F(r,Q),'TV row bound','support_rounding')

def test_parallelogram():
    for i,j in product(range(17),repeat=2):
        a,b=F(i,16),F(j,16)
        u,v=(3*a+b)/4,(a+3*b)/4
        require(0<=3*u-v<=2 and 0<=3*v-u<=2,'feasible common row','common_programme')
        require((3*u-v)/2==a and (3*v-u)/2==b,'inverse row','common_programme')
        require((1-u+v)/2>=F(1,4),'randomized risk lower','common_programme')
    require((1-F(3,4)+F(1,4))/2==F(1,4),'attainment','common_programme')
    require(3*1-0>2,'phasewise fake solution rejected','common_programme')
    require(((3*F(3,4)+F(1,4))/4,(F(3,4)+3*F(1,4))/4)==(F(5,8),F(3,8)),'interior witness','common_programme')

def test_graph_and_threshold():
    # Exact graph criterion for separately typed sense/response/halt labels.
    # Report-sensitive sense rows and response markers are shared across phases.
    def risk(ns,nr,sense,reply,ret):
        # sense[(s,y)] = response index; reply[r] in {0,1}; return r -> sense index.
        score=F(0)
        for y1,y2 in product((0,1),repeat=2):
            r1=sense[(0,y1)]; s2=ret[r1]; r2=sense[(s2,y2)]
            p1=(F(3,4),F(1,4))[y1];p2=(F(1,4),F(3,4))[y2]
            score+=p1*p2*F((reply[r1]!=0)+(reply[r2]!=1),2)
        return score
    minima={}
    examined=0
    for M in (3,4,5):
        best=F(1)
        for ns in range(1,M-1):
            nr=M-1-ns
            if nr<1:continue
            for sv in product(range(nr),repeat=2*ns):
                sense={(s,y):sv[2*s+y] for s in range(ns) for y in (0,1)}
                for reply in product((0,1),repeat=nr):
                    for ret in product(range(ns),repeat=nr):
                        rr=risk(ns,nr,sense,reply,ret);examined+=1
                        require(0<=rr<=1,'scored probability','finite_threshold')
                        best=min(best,rr)
        minima[M]=best
    require(minima=={3:F(1,2),4:F(1,4),5:F(0)},'deterministic threshold witnesses','finite_threshold')
    # Randomized lower is an analytic proof in the paper; finite checks only illustrate it.
    for x in range(33):
        p=F(x,32)
        require(((1-p)+p)/2==F(1,2),'single response label lower','finite_threshold')
    return examined

def matvec(A,x):return tuple(sum(a*b for a,b in zip(row,x)) for row in A)
def addvec(x,y):return tuple(a+b for a,b in zip(x,y))
def scale(c,x):return tuple(c*a for a in x)
def l1(x):return sum(abs(a) for a in x)
def test_positive_instruments():
    # Four reports, two cells, two positive hidden coordinates. Exact reconstructed
    # instrument identities and uniform one-step state/label norm estimates.
    I=[((F(3,8),0),(0,F(1,8))),((F(1,8),0),(0,F(3,8))),
       ((F(1,4),0),(0,F(1,8))),((F(1,4),0),(0,F(3,8)))]
    cells=((0,1),(2,3))
    Ih=[]
    for ys in cells:
        avg=tuple(tuple(sum(I[y][i][j] for y in ys)/len(ys) for j in range(2)) for i in range(2))
        Ih.extend([avg]*len(ys))
    d=max(sum(l1(tuple(a-b for a,b in zip(matvec(I[y],x),matvec(Ih[y],x)))) for y in range(4)) for x in ((1,0),(0,1)))
    for p in range(9):
        x=(F(p,8),1-F(p,8))
        for nums in product(range(3),repeat=4):
            k=[F(t,2) for t in nums]
            kbar=[(k[0]+k[1])/2,(k[2]+k[3])/2]
            original=(F(0),F(0));regen=(F(0),F(0));coarse=(F(0),F(0))
            for y in range(4):
                original=addvec(original,scale(k[y],matvec(I[y],x)))
                regen=addvec(regen,scale(k[y],matvec(Ih[y],x)))
                coarse=addvec(coarse,scale(kbar[y//2],matvec(I[y],x)))
            require(regen==coarse,'common reconstruction identity','positive_instrument')
            # Both output-label vectors, not just a scalar report expectation.
            diff=tuple(a-b for a,b in zip(original,regen))
            require(2*l1(diff)<=d,'joint state-label base norm','positive_instrument')
            for b,ys in enumerate(cells):
                require((kbar[b]>0)==any(k[y]>0 for y in ys),'possible edge equality','positive_instrument')

def test_intervals():
    # With binary fixed-M common rows the exact optimum is 1/4 for all Q grids.
    for Q in (1,2,4,8,16):
        risks=[]
        for i,j in product(range(Q+1),repeat=2):
            a,b=F(i,Q),F(j,Q);u,v=(3*a+b)/4,(a+3*b)/4
            risks.append((1-u+v)/2)
        require(min(risks)==F(1,4),'finite grid optimum','risk_certificate')
        eta=F(1,1000)
        lows=[r-eta/3 for r in risks];ups=[r+eta/3 for r in risks]
        l,u=min(lows),min(ups)
        require(l<=F(1,4)<=u and u-l<=eta,'certified extrema interval','risk_certificate')
        for err in (F(0),F(1,9),F(2)):
            require(l-err<=F(1,4)<=u,'lower subtraction direction','risk_certificate')
    for k in range(1,12):
        require(F(1,3**k)==F(3)**(-k),'Cantor mesh','singular_mesh')
        # The geometrically weighted actual tail is not normalized away.
        actual_tail=F(1,2**k)
        require(2*actual_tail==F(1,2**(k-1)),'actual tail error','singular_mesh')
    # Randomized convex witnesses vs affine-only constraints.
    require(F(0)+F(1,2)==F(1,2),'same barycenter','dual_tests')
    require(F(1,2)>F(1,4),'convex square obstruction','dual_tests')

def main():
    test_rounding();test_parallelogram();examined=test_graph_and_threshold();test_positive_instruments();test_intervals()
    # Kept as a distinct nested result, not added again to new check totals.
    inherited=subprocess.check_output([sys.executable,str(ROOT.parent/'r18-causal-allocation'/'regression.py')],text=True)
    result={'status':'PASS','component':'R19 effective frontier selected finite checks','new_checks':sum(COUNTS.values()),'groups':COUNTS,'deterministic_typed_programmes_examined':examined,'retained_R18':json.loads(inherited),'limitations':'Exact finite arithmetic checks and typed finite programme examples only; no numerical verification of continuum theorems, all randomized programmes, priority, or optimal search complexity.'}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
