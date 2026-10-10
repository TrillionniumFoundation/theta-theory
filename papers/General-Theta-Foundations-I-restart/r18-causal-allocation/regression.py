#!/usr/bin/env python3
"""Selected exact finite witnesses; no finite suite proves the continuum results."""
from __future__ import annotations
import itertools,json,math
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
COUNTS=defaultdict(int)
def check(ok,group,msg):
    if not bool(ok):raise RuntimeError(group+': '+msg)
    COUNTS[group]+=1
# Static finite barycentric allocations and finite affine duals.
xs=(F(0),F(1,3),F(1));mass=(F(1,4),F(1,2),F(1,4))
for row in itertools.product((F(0),F(1,2),F(1)),repeat=3):
    p=[sum(w*r for w,r in zip(mass,row)),sum(w*(1-r) for w,r in zip(mass,row))]
    b=[sum(w*r*x for w,r,x in zip(mass,row,xs)),sum(w*(1-r)*x for w,r,x in zip(mass,row,xs))]
    check(sum(p)==1 and sum(b)==sum(w*x for w,x in zip(mass,xs)),'local_barycenters','mass/mean')
    for a0,b0,a1,b1 in itertools.product((-1,0,1),repeat=4):
        lhs=a0*p[0]+b0*b[0]+a1*p[1]+b1*b[1]
        rhs=sum(w*max(a0+b0*x,a1+b1*x) for w,x in zip(mass,xs))
        check(lhs<=rhs,'finite_affine_duals','local support-function inequality')
# A proposed spread exceeding its acquisition law has a strict witness.
target=sum(p*sign*x for p,sign,x in ((F(1,2),-1,F(-1)),(F(1,2),1,F(1))))
acquired=max(-F(0),F(0))
check(target>acquired,'strict_local_witness','absolute-value witness for delta_0 -> +/-1')
# Same-report shared allocation: max outside phase sum is essential.
for p0,p1 in itertools.product((F(1,4),F(1,2),F(1)),repeat=2):
    lhs=p0+p1;rhs=max(p0,p1)
    check(lhs>rhs,'simultaneous_obstruction','phase-conflicting deterministic assignments')
    for r in (F(0),F(1,3),F(1)):
        for c00,c01,c10,c11 in itertools.product((-1,0,1),repeat=4):
            attained=p0*(r*c00+(1-r)*c01)+p1*(r*c10+(1-r)*c11)
            support=max(p0*c00+p1*c10,p0*c01+p1*c11)
            check(attained<=support,'simultaneous_duals','shared kernel support function')
# One-dimensional finite-test relaxation: both affine signs restore the mean.
grid=[F(i,20) for i in range(21)];g=lambda x:x*(1-x)
c0=min(map(g,grid));c1=min(g(x) for x in grid if x<=F(1,2));c2=min(g(x) for x in grid if x<=F(1,2) and -x<=-F(1,2))
check((c0,c1,c2)==(0,0,F(1,4)),'finite_obstruction_relaxation','nested finite test values')
# Exact deployed posterior pooling, with arbitrary suboptimal action choices.
ACTIONS=((F(1,5),F(1,4),F(3,4)),(F(1,3),F(2,5),F(9,10)))
def outcomes(p,a):
    flip,f0,f1=ACTIONS[a];q=flip+(1-2*flip)*p;r=(1-q)*f0+q*f1
    return ((r,q*f1/r),(1-r,q*(1-f1)/(1-r)))
@lru_cache(None)
def value(k,p):
    return g(p) if k==0 else min(sum(w*value(k-1,q) for w,q in outcomes(p,a)) for a in range(2))
for n in (1,2,3):
    for p0 in (F(1,7),F(1,2),F(5,6)):
        for widths in itertools.product((1,2,3),repeat=n):
            for policy in (0,1,2):
                state=[(F(1),p0)];total=F(0)
                for t,L in enumerate(widths):
                    cells=defaultdict(lambda:[F(0),F(0)]);old=sum(w*value(n-t,p) for w,p in state);pre=F(0)
                    for w,p in state:
                        a=policy if policy<2 else min(range(2),key=lambda j:sum(v*value(n-t-1,q) for v,q in outcomes(p,j)))
                        for v,q in outcomes(p,a):
                            pre+=w*v*value(n-t-1,q);cell=min(L-1,int(q*L));cells[cell][0]+=w*v;cells[cell][1]+=w*v*q
                    new=[(w,b/w) for w,b in cells.values() if w];post=sum(w*value(n-t-1,q) for w,q in new)
                    check(pre>=old,'deployed_action_slack','Bellman action slack');check(post>=pre,'deployed_jensen','actual all-incoming Jensen')
                    check(sum(w for w,q in new)==1,'deployed_calibration','mass');total+=post-old;state=new
                risk=sum(w*g(p) for w,p in state)
                check(risk-value(n,p0)==total,'exact_telescope','sum action and Jensen slack')
# Deterministic report-neutral finite automata cannot halt at a fixed late time after a cycle.
for M in range(1,5):
    for nxt in itertools.product(range(-1,M),repeat=M):
        z=0;path=[];halt=None
        for t in range(M+2):
            if nxt[z]==-1:halt=t;break
            path.append(z);z=nxt[z]
        if halt is not None:
            check(len(set(path+[z]))==halt+1,'clock_automata','disjoint cut labels')
            check(M>=halt+1,'clock_automata','minimum state count')
# Integer allocation bounds, including the exact minimum budget.
for n in range(1,15):
    for p in (0.5,1.0,2.0):
        for m in range(1,31):
            a=[(0.7**(n-t-1)) for t in range(n)];weights=[v**(1/(1+p)) for v in a];A=sum(weights)
            L=[1+math.floor((m-1)*w/A) for w in weights]
            check(sum(L)<=n+m-1 and min(L)>=1,'integer_allocation','budget/baseline')
            check(sum(v/l**p for v,l in zip(a,L))<=2**p*m**(-p)*A**(1+p)+1e-12,'integer_allocation','weighted bound')
# Blind bottleneck: exhaustive deterministic encoders on four points and all second maps.
x=(F(0),F(1,4),F(3,4),F(1));w=(F(1,4),)*4
def loss(labels):
    cells=defaultdict(lambda:[F(0),F(0),F(0)])
    for z,p,t in zip(labels,w,x):cells[z][0]+=p;cells[z][1]+=p*t;cells[z][2]+=p*t*t
    return sum(c-b*b/a for a,b,c in cells.values())
q={L:min(loss(c) for c in itertools.product(range(L),repeat=4)) for L in range(1,4)}
for m1,m2 in itertools.product(range(1,4),repeat=2):
    best=F(100)
    for first in itertools.product(range(m1),repeat=4):
        for second in itertools.product(range(m2),repeat=m1):
            risk=loss(tuple(second[z] for z in first));best=min(best,risk)
            check(risk>=q[min(m1,m2)],'blind_bottleneck','all deterministic two-cut maps')
    check(best==q[min(m1,m2)],'blind_bottleneck_attainment','exhaustive optimum')
# Exact state floors and actual atomic tail witnesses.
for n in range(1,15):
    for M in range(n+1,n+61):
        L=(M-1)//n
        check(1+n*L<=M<1+n*(L+1),'blind_state_floor','exact phase copies')
for alpha in range(1,5):
    ratio=F(1,2**(alpha+2));c=F(2**alpha-1)
    for L in range(1,13):
        upper=c*ratio**L/(1-ratio)
        lower=c*ratio**(L+1)/64
        check(0<lower<=upper,'atomic_tail','unnormalized lower/upper masses')
        balls=[(F(7,8)*F(1,2**j),F(9,8)*F(1,2**j)) for j in range(1,L+2)]
        check(all(balls[j+1][1]<balls[j][0] for j in range(len(balls)-1)),'atomic_tail','disjoint witness balls')
# Support-preserving probability rounding.
def round_row(row,Q):
    out=[int(v*Q) for v in row];j=next(i for i,v in enumerate(row) if v>0);out[j]+=Q-sum(out)
    return tuple(F(v,Q) for v in out)
for denominator in range(1,9):
    for i in range(denominator+1):
        for j in range(denominator-i+1):
            row=(F(i,denominator),F(j,denominator),F(denominator-i-j,denominator))
            for Q in range(1,14):
                rounded=round_row(row,Q);tv=sum(abs(a-b) for a,b in zip(row,rounded))/2
                check(sum(rounded)==1 and all(v>=0 for v in rounded),'support_rounding','probability')
                check(all(not r or p>0 for p,r in zip(row,rounded)),'support_rounding','no new support')
                check(tv<=len(row)/Q,'support_rounding','row TV bound')
# Actual erased-bit deficiency and squared-loss coordinates.
for i in range(11):
    eps=F(i,20);p0=(1-2*eps,F(0),2*eps);p1=(F(0),1-2*eps,2*eps)
    tv=sum(abs(a-b) for a,b in zip(p0,p1))/2
    check(tv==1-2*eps and (1-tv)/2==eps,'erasure_task','two-point deficiency lower')
    check(2*eps*F(1,4)==eps/2,'erasure_task','attained bit squared loss')
    for N in range(3,15):
        for M in range(N,N+10):
            n=N-2
            check((M-1)-n==M-N+1 and ((M-1)-1)//n==(M-2)//(N-2),'product_task_count','physical/engine/label account')
print(json.dumps({'status':'PASS','checks':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),'arithmetic':'exact Fraction except explicitly numeric integer-allocation estimates','limitations':'selected finite identities, counterexamples and bounds; not continuum proof, priority or independent referee certification'},sort_keys=True,indent=2))
