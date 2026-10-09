#!/usr/bin/env python3
"""Finite witnesses only. Mathematical proofs are in the manuscript, not these checks."""
import itertools
import json
import math
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import numpy as np

COUNTS=defaultdict(int)
def check(ok, group, message):
    if not bool(ok):
        raise RuntimeError(group+': '+message)
    COUNTS[group]+=1

# Exact finite-kernel forward calibration and Bellman--Jensen telescope.
ACTIONS=[(F(1,5),F(1,4),F(3,4)),(F(1,3),F(2,5),F(9,10))]
def outcomes(p,a):
    flip,f0,f1=ACTIONS[a]
    q=flip+(1-2*flip)*p
    r=(1-q)*f0+q*f1
    return [(r,q*f1/r),(1-r,q*(1-f1)/(1-r))]
def g(p): return p*(1-p)
@lru_cache(None)
def V(k,p):
    if k==0:return g(p)
    return min(sum(w*V(k-1,u) for w,u in outcomes(p,a)) for a in range(len(ACTIONS)))
def best(k,p):
    return min(range(len(ACTIONS)),key=lambda a:(sum(w*V(k-1,u) for w,u in outcomes(p,a)),a))
for horizon in (1,2,3):
    for p0 in (F(1,7),F(1,2),F(5,6)):
        for levels in itertools.product((1,2,3),repeat=horizon):
            state=[(F(1),p0)];defect=F(0)
            for t,L in enumerate(levels):
                cells=defaultdict(lambda:[F(0),F(0),F(0)])
                expected=F(0)
                for mass,p in state:
                    a=best(horizon-t,p)
                    for w,u in outcomes(p,a):
                        j=min(L-1,int(u*L));joint=mass*w
                        cells[j][0]+=joint;cells[j][1]+=joint*u
                        cells[j][2]+=joint*V(horizon-t-1,u)
                        expected+=joint*V(horizon-t-1,u)
                check(expected==sum(w*V(horizon-t,p) for w,p in state),'rational_pooling','Bellman equality')
                nxt=[]
                for mass,total,cellvalue in cells.values():
                    q=total/mass
                    check(F(0)<=q<=1,'rational_pooling','conditional barycenter')
                    check(mass*q==total,'rational_pooling','all incoming calibration')
                    gap=mass*V(horizon-t-1,q)-cellvalue
                    check(gap>=0,'rational_pooling','Jensen nonnegativity')
                    defect+=gap;nxt.append((mass,q))
                state=nxt
                check(sum(w for w,p in state)==1,'rational_pooling','actual probability mass')
            check(sum(w*g(p) for w,p in state)-V(horizon,p0)==defect,'rational_pooling','exact telescope')

# Deterministic finite automata under two positive-probability report symbols.
# A positive-probability path cannot be silently removed by an observer.
valid=0
for q in (1,2,3):
    for table in itertools.product(range(q),repeat=2*q):
        for mask in range(1,1<<q):
            stops={j for j in range(q) if mask&(1<<j)}
            if 0 in stops:continue
            support={0};cuts=[support];exact=None
            for t in range(1,q+2):
                support={table[2*s+y] for s in support for y in (0,1)}
                cuts.append(support)
                if support&stops:
                    if support<=stops:exact=t
                    break
            COUNTS['finite_clock_graphs']+=1
            if exact is not None:
                valid+=1
                check(all(not cuts[s]&cuts[t] for s in range(len(cuts)) for t in range(s+1,len(cuts))),
                      'finite_clock_converses','phase support overlap')
                check(len(cuts[-1])<=q-exact,'finite_clock_converses','terminal state count')
check(valid>0,'finite_clock_converses','no valid internally stopped graph tested')

# Integer allocation checks include m=1 and all small horizons.
for d in (1,2,3,5,8):
    p=2.0/d;gamma=1/(1+p)
    for n in (1,2,3,7,17,40):
        for m in (1,2,3,8,31,97):
            for betas in ((.3,), (2.4,2.4,.06)):
                a=np.ones(n)
                for t in range(n-2,-1,-1):a[t]=a[t+1]*betas[t%len(betas)]
                w=a**gamma;At=float(w.sum())
                L=1+np.floor((m-1)*w/At).astype(int)
                check(int(L.sum())<=n+m-1,'integer_allocation','total autonomous labels')
                lhs=float(np.sum(a*L**(-p)));rhs=2**p*At**(1+p)*m**(-p)
                check(lhs<=rhs*(1+1e-12),'integer_allocation','weighted bound')
                check(bool(np.all(L>=1)),'integer_allocation','lost baseline label')
check(F(12,5)*F(12,5)*F(3,50)==F(216,625),'block_witness','nonuniform product')

# Curvature and unnormalized stratum factors, as exact algebraic witnesses.
for d in (1,2,4):
    for k in (1,2,3,7,11):
        # Uniform scalar grid and quadratic g: integrated variance is 1/(12 k^2).
        exact=sum((F(j+1,k)**3-F(j,k)**3)/3-F(1,k)*F(2*j+1,2*k)**2 for j in range(k))
        check(exact==F(1,12*k*k),'rational_curvature','uniform-grid distortion')
for r in (1,2,3,5):
    for theta in (.05,.3,.7,.95):
        w=1-theta;rho=2.7
        lhs=w**(1+2/r)/(w*rho)**(2/r)
        check(abs(lhs-w*rho**(-2/r))<1e-13,'stratum_submass','mass normalization')

# Noncommuting positive-definite inverse: numerical algebra witnesses only.
def powh(x,p):
    vals,vec=np.linalg.eigh(x)
    if np.min(vals)<=0:raise RuntimeError('nonpositive test matrix')
    return (vec*vals**p)@vec.conj().T
rng=np.random.default_rng(1791331200)
for D in (2,3,4):
    for _ in range(25):
        z=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D))
        q=z@z.conj().T+np.eye(D);q=q/np.trace(q)
        z=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D))
        E=z@z.conj().T+np.eye(D);E=E*D/np.trace(E)
        root=powh(E,.5);sigma=root@q@root;sigma/=np.trace(sigma)
        qr=powh(q,.5);qi=powh(q,-.5)
        AA=qi@powh(qr@sigma@qr,.5)@qi
        inv=D*(AA@AA)/np.trace(AA@AA)
        check(np.linalg.norm(inv-E)<2e-10,'matrix_inverse_numeric','positive inverse')
        check(np.linalg.norm(AA@q@AA-sigma)<2e-10,'matrix_inverse_numeric','A q A = sigma')
        check(np.linalg.norm(E@q-q@E)>1e-6,'matrix_inverse_numeric','accidentally commuting witness')

# Gaussian likelihood/softmax identities over a continuous parameter sample.
for q in (.1,.25,.5,.8,.9):
    for y in np.linspace(-8,8,41):
        f0=math.exp(-y*y/2)/math.sqrt(2*math.pi)
        f1=math.exp(-(y-1)**2/2)/math.sqrt(2*math.pi)
        u=q*f1/((1-q)*f0+q*f1)
        z=y-.5+math.log(q/(1-q))
        soft=1/(1+math.exp(-z))
        check(abs(u-soft)<2e-14,'gaussian_numeric','raw Bayes/logit identity')
        jac=soft*(1-soft)
        check(jac>0,'gaussian_numeric','softmax Jacobian positive')

for den in range(1,31):
    for num in range(den+1):
        eps=F(num,2*den)
        source0=[1-2*eps,F(0),2*eps];source1=[F(0),1-2*eps,2*eps]
        tv=sum(abs(x-y) for x,y in zip(source0,source1))/2
        check(tv==1-2*eps,'rational_deficiency','source total variation')
        check(2*eps*F(1,4)==eps/2,'rational_deficiency','Bayes bit risk')
        check((1-tv)/2==eps,'rational_deficiency','attained minimax deficiency')

print(json.dumps({'status':'PASS','checks':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),
                  'limitations':'Exact finite checks and deterministic numerical witnesses only; not continuum proofs, exhaustive controller certification, or a priority audit.'},sort_keys=True,indent=2))
