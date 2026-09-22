#!/usr/bin/env python3
"""Finite regressions for the sixth revision; not proof certification.

All required checks use explicit exceptions, so python -O cannot disable them.
No random simulation, network access or third-party library is required.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from functools import lru_cache
import heapq
import json
import math
import sys

MUTANTS = ('fill-forbidden-edge', 'free-unary-state', 'erase-suffix-drop',
           'ordinary-matrix-power', 'erase-critical-correction',
           'omit-bayes-floor', 'outward-quantizer', 'free-overflow')
checks = 0

def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        raise ValueError(message)

def main(mutant: str | None) -> dict:
    A = ((1, 1), (1, 0))
    P = ((F(1, 2), F(1, 2)), (F(1), F(0)))
    pi = (F(2, 3), F(1, 3))
    ratios = (F(1, 4), F(1, 3))
    q1, q2 = F(1, 5), F(2, 3)
    w = lambda k: ((1-q1)*q1**k+(1-q2)*q2**k)/2
    tail = lambda k: (q1**k+q2**k)/2
    children = lambda word: [word+(i,) for i in range(2) if not word or A[word[-1]][i]]
    @lru_cache(None)
    def mass(word: tuple[int, ...]) -> F:
        if not word:
            return F(1)
        value = pi[word[0]]
        for i, j in zip(word, word[1:]):
            value *= P[i][j]
        return value
    @lru_cache(None)
    def scale(word: tuple[int, ...]) -> F:
        value = F(1)
        for i in word:
            value *= ratios[i]
        return value
    @lru_cache(None)
    def energy_scale(word: tuple[int, ...]) -> F:
        n = len(word)
        return sum((w(k)*scale(word[k:])**2 for k in range(n)), F(0))+tail(n)
    energy = lambda word: mass(word)*energy_scale(word)
    rho = 1-(1-max(ratios)**2)*(1-q2)
    a0 = min(pi[0],pi[1],F(1,2))*min(min(ratios)**2,q1)
    words = [()]
    level = [()]
    for n in range(1, 11):
        level = [child for word in level for child in children(word)]
        words += level
        require(sum(map(mass,level),F(0)) == 1, 'admissible cylinders do not partition')
    for word in words:
        require(mass(word)>0, 'forbidden word entered the language')
        cc = children(word)
        require(sum((mass(c) for c in cc),F(0))==mass(word), 'conditional masses')
        require(sum((energy(c) for c in cc),F(0))<=rho*energy(word), 'total child contraction')
        for c in cc:
            require(a0*energy(word)<=energy(c)<=rho*energy(word), 'child energy bounds')
        for m in range(1,len(word)+1):
            suffix = word[m:]
            drop = (1-max(ratios)**2)*scale(suffix)**2*sum((w(k) for k in range(m)),F(0))
            actual = energy_scale(suffix)-energy_scale(word)
            if mutant == 'erase-suffix-drop':
                actual = F(0)
            require(actual>=drop>0, 'strict renewal suffix decrease')
            require(energy(word)<energy(suffix), 'strict suffix energy with unary predecessor')
    require(mass((1,0))==mass((1,)), 'stationarity diagnostic selected wrong cylinder')
    # Unique predecessor for suffix 1: mu[01]=mu[1], but energy still decreases.
    require(mass((0,1))==mass((1,)), 'unique predecessor equality')
    require(energy((0,1))<energy((1,)), 'strict energy is not strict mass')
    vertices = {()}
    leaves = {()}
    heap = [(-energy(()), ())]
    split_count = 0
    profiles = []
    for _ in range(600):
        _, word = heapq.heappop(heap)
        require(word in leaves, 'heap/leaf mismatch')
        leaves.remove(word)
        cc = children(word)
        for child in cc:
            vertices.add(child); leaves.add(child)
            heapq.heappush(heap, (-energy(child), child))
        split_count += 1
        require(len(vertices)==1+sum(len(children(v)) for v in vertices-leaves), 'actual tree count')
        claimed_states = 2*len(leaves)-1 if mutant=='free-unary-state' else len(vertices)
        require(claimed_states==len(vertices), 'unary vertices are persistent states')
        require(len(vertices)<=3*(2*len(leaves)-1), 'linear graph state bound')
        for vertex in vertices:
            require(vertex[1:] in vertices if vertex else True, 'suffix closure')
        es = [energy(v) for v in leaves]
        require(min(es)>=a0*max(es), 'balanced leaf energies')
        profiles.append((len(leaves),float(sum(es,F(0)))))
    # Markov pressure matrices retain structural zeros and use entrywise powers.
    def matrix(s: float, spatial: bool) -> tuple[tuple[float,float],tuple[float,float]]:
        rows=[]
        for i in range(2):
            row=[]
            for j in range(2):
                value=float(P[i][j])**s if A[i][j] else 0.0
                if mutant=='fill-forbidden-edge' and not A[i][j]: value=1.0
                if mutant=='ordinary-matrix-power' and A[i][j]: value=float(P[i][j])
                row.append(value*(float(ratios[i])**(2*s) if spatial else 1))
            rows.append(tuple(row))
        return tuple(rows)
    def spr(mm):
        a,b=mm[0];c,d=mm[1]
        return (a+d+math.sqrt((a-d)**2+4*b*c))/2
    golden=(1+math.sqrt(5))/2
    require(matrix(0,False)[1][1]==0, 'forbidden transition completed at zero pressure')
    require(abs(spr(matrix(0,False))-golden)<1e-14,'entrywise zero-power pressure')
    require(abs(spr(matrix(1,False))-1)<1e-14,'normalized Markov pressure')
    def root(q,spatial):
        lo,hi=0.,1.
        for _ in range(80):
            mid=(lo+hi)/2
            value=spr(matrix(mid,spatial))*(1 if spatial else q**mid)
            if value>1:lo=mid
            else:hi=mid
        return (lo+hi)/2
    sg=root(.4,True)
    qc=math.exp(-math.log(spr(matrix(sg,False)))/sg)
    require(0<sg<1 and 0<qc<1,'pressure roots')
    require(abs(root(qc,False)-sg)<1e-13,'pressure threshold')
    for q in [.01,.05,.1,.2,.4,.7,.9]:
        st=root(q,False)
        require(abs(q**st*spr(matrix(st,False))-1)<1e-13,'survival root residual')
        require((st>sg)==(q>qc),'root ordering')
    # Scaled critical profiles avoid underflow and test a uniform bounded window.
    a=1/9
    def scaled_profile(n,kappa,x):
        q=a*math.exp(x/n)
        total=math.fsum(q**k/(k+1)**kappa for k in range(160))
        early=math.fsum(math.exp(x*k/n)/(k+1)**kappa for k in range(n))
        if mutant=='erase-critical-correction': early=1.
        late=math.exp(x)*math.fsum(q**j/(n+j+1)**kappa for j in range(160))
        return (early+late)/total
    n=8000
    for x in [-2.,-1.,0.,1.,2.]:
        target=(1-a)*(math.expm1(x)/x if x else 1.)
        require(abs(scaled_profile(n,0,x)/n-target)<.001, 'uniform critical window kappa=0')
    def simpson(fun,n=2000):
        h=1/n
        return h/3*(fun(0)+fun(1)+4*sum(fun(k*h) for k in range(1,n,2))+2*sum(fun(k*h) for k in range(2,n,2)))
    norm_half=1/math.fsum(a**k/math.sqrt(k+1) for k in range(160))
    for x in [-2.,0.,2.]:
        target=norm_half*simpson(lambda t:2*math.exp(x*t*t))
        require(abs(scaled_profile(n,.5,x)/math.sqrt(n)-target)<.035, 'integrable critical endpoint')
    norm_one=1/math.fsum(a**k/(k+1) for k in range(160))
    norm_two=1/math.fsum(a**k/(k+1)**2 for k in range(160))
    require(abs(scaled_profile(n,1,0)/math.log(n)-norm_one)<.08,'log-log correction')
    require(abs(scaled_profile(n,2,0)-norm_two*math.pi**2/6)<.001,'bounded critical correction')
    # Inward finite compander checks include negative, saturated and extreme bins.
    def quant(x,n):
        sign=1 if x>=0 else -1;x=abs(x)
        j=min(n-1,(n*x.numerator)//(x.denominator+x.numerator))
        if mutant=='outward-quantizer':j=min(n-1,j+1)
        return sign*F(j,n-j)
    for nn in range(2,25):
        for numer in range(-200,201):
            for den in [1,3,17]:
                x=F(numer,den);z=quant(x,nn)
                require(abs(z)<=abs(x),'compander outward rounding')
                require(abs(x-z)<=(1+abs(x))**2/nn,'compander distortion bound')
        for x in [F(10000),F(-10000)]:
            require(abs(quant(x,nn))==nn-1,'saturation radius')
    random_lip_fourth=F(1,100)*F(2)**4+F(99,100)*F(1,2)**4
    require(random_lip_fourth<1 and F(2)>1, 'conditional mean contraction permits expansions')
    gaussian=[]
    for aa in [.2,.7,.97]:
        for v,omega in [(.3,.8),(1.,.2),(2.,3.)]:
            pp=0.
            for _ in range(600): pp=omega*(aa*aa*pp+v)/(aa*aa*pp+v+omega)
            if mutant=='omit-bayes-floor': pp=0.
            require(abs(pp-omega*(aa*aa*pp+v)/(aa*aa*pp+v+omega))<1e-12,'nonzero Riccati Bayes floor')
            ss=v/(1-aa*aa);latest=ss*omega/(ss+omega)
            require(0<pp<latest<ss,'full-history posterior differs from latest observation')
            gain=(aa*aa*pp+v)/(aa*aa*pp+v+omega)
            require(abs((1-gain)*aa)<1,'verified posterior contraction')
            gaussian.append(pp)
    # Exact register simulations and fixed-alphabet boundaries.
    for m in range(1,20):
        for k in range(1,7):
            packed={(i,e):i*k+e for i in range(m) for e in range(k)}
            require(len(set(packed.values()))==m*k,'event/register injection')
            for (i,e),value in packed.items():
                require(divmod(value,k)==(i,e),'event/register reconstruction')
        require(2**(m-1).bit_length()>=m,'binary checkpoint bound')
    for rr in range(1,5):
        for jj in range(2,16):
            alphabet=jj**rr+(0 if mutant=='free-overflow' else 1)
            require(alphabet==jj**rr+1,'A2 overflow label must be counted')
    return {'status':'passed','finite_checks':checks,'maximum_greedy_vertices':len(vertices),
            'maximum_greedy_leaves':len(leaves),'word_depth':10,'geometric_pressure_root':round(sg,12),
            'critical_q':round(qc,12),'gaussian_floor_checks':len(gaussian),
            'scope':'Finite regression evidence, not an infinite-dimensional proof or priority certificate.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',choices=MUTANTS)
    args=parser.parse_args()
    try:print(json.dumps(main(args.mutant),sort_keys=True,indent=2))
    except (ValueError,ArithmeticError) as exc:
        print('FAILED: '+str(exc));sys.exit(1)
