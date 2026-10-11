#!/usr/bin/env python3
"""Finite sanity checks; these do not establish the continuous-parameter proofs."""
import json
import math
import random
from fractions import Fraction as F

counts = {}
def check(name, condition):
    counts[name] = counts.get(name, 0) + 1
    if not condition:
        raise RuntimeError('regression failed: ' + name)

def compand(p, eta, k):
    v = [math.log(max(p) / x) for x in p]
    vh = [-math.log(math.ceil(k * math.exp(-eta*x))/k)/eta for x in v]
    z = [math.exp(-x) for x in vh]
    return [x/sum(z) for x in z]

def spread(p):
    return math.log(max(p)/min(p))

def dist(p, q):
    z = [math.log(x/y) for x, y in zip(p,q)]
    return max(z)-min(z)

def rowmul(p,q):
    return [sum(p[i]*q[i][j] for i in range(len(p))) for j in range(len(p))]

rng = random.Random(20261007)
for n in range(2,7):
    for k in (1,2,3,8,21):
        for _ in range(80):
            raw = [math.exp(rng.uniform(-12,12)) for i in range(n)]
            p = [x/sum(raw) for x in raw]
            eta=.25
            q=compand(p,eta,k)
            check('inward', spread(q)<=spread(p)+1e-10)
            check('mass_floor', all(y>=x/n-1e-13 for x,y in zip(p,q)))
            check('radius', dist(p,q)<=math.exp(eta*spread(p))/(eta*k)+1e-10)
            check('normalization', abs(sum(q)-1)<1e-12)
            h=.02
            logs=[math.log(x) for x in p]
            low=[z-h*rng.random() for z in logs]
            high=[l+h for l in low]
            deficits=[max(0,max(low)-u) for u in high]
            true=[max(logs)-z for z in logs]
            check('enclosure_deficits',all(-1e-12<=v-d<=2*h+1e-12 for v,d in zip(true,deficits)))
            vh=[-math.log(math.ceil(k*math.exp(-eta*x))/k)/eta for x in deficits]
            z=[math.exp(-x) for x in vh]; z=[x/sum(z) for x in z]
            check('enclosure_mass',all(y>=x/n-1e-12 for x,y in zip(p,z)))
            check('enclosure_radius',dist(p,z)<=math.exp(eta*spread(p))/(eta*k)+2*h+1e-10)

# Exact rational singular gain and count checks, including both cross-mode edges.
check('singular_constant',(1-F(1,4096))*F(4,9)+F(900,4096)==F(85,128))
for alpha in (F(i,100) for i in range(101)):
    check('singular_row0',(1-alpha)*F(85,128)*1800+900*alpha<=F(17,20)*1800)
    check('singular_row1',F(3600,59049)+F(1,2)<F(17,20))
for m in range(1,16):
    check('singular_label_count',2*sum(2**j for j in range(m+1))==2**(m+2)-2)
for M in range(6,2001):
    n=M.bit_length()-1; m=(M+2).bit_length()-3
    check('singular_budget',2**(m+2)-2<=M and 0<=n-m<=2)
for d in range(1,7):
    for M in range(1,101):
        for b in range(1,9):
            lhs=min(M,(2**b+1)**d)**(-2/d)
            rhs=M**(-2/d)+2**(-2*b)
            check('grid_max_sum',rhs/8-1e-12<=lhs<=rhs+1e-12)

# Four-state sparse support has disjoint one-step rows but positive three-step product.
n=4; Q=[[.5 if j in (i,(i+1)%n) else 0 for j in range(n)] for i in range(n)]
Q3=[rowmul(rowmul(row,Q),Q) for row in Q]
check('primitive_support',min(map(min,Q3))>=.125)
check('no_one_step_common_mass',sum(min(Q[0][j],Q[2][j]) for j in range(n))==0)

# Algebra of the selected Lyapunov constants, not a probabilistic proof.
for _ in range(2000):
    kap=rng.random()*.99; a=rng.random()*.99; A=4*rng.random(); B=3*rng.random(); b=3*rng.random()
    lm=rng.randrange(1,6); kb=(1+kap)/2; C=kb/(kb-kap); gam=max(kb,(1+a)/2)
    c=max(1,C*lm*lm*A/(gam-a)); c0=C*lm*lm*(B+1)+c*b
    check('stopped_coefficients',C*lm*lm*A+c*a<=gam*c+1e-9)
    x=rng.random()*20; z=rng.random()*5
    check('young_inequality',(math.sqrt(kap)*x+z)**2<=kb*x*x+C*z*z+1e-9)
    check('stopped_drift_constant',c0>=c*b and gam<1)

# Finite depth recursion preserves total probability without a stationary law.
depth={(0,2):F(1,3),(1,2):F(2,3)}
for alpha in (F(0),F(1),F(1,3),F(4,5)):
    out={}
    for (i,h),p in depth.items():
        edges=[(0,h+2,(1-alpha)*(1-F(1,4096))),(0,max(h-1,0),(1-alpha)*F(1,4096)),(1,max(h-1,0),alpha)] if i==0 else [(0,h+6,F(1,2)),(1,h,F(1,2))]
        for j,h2,q in edges:
            out[j,h2]=out.get((j,h2),F(0))+p*q
    check('actual_depth_mass',sum(out.values())==1)
    depth=out

negative={
 'inward_is_not_component_mass': spread([.01,.09,.9])<=spread([.9,.09,.01])+1e-12 and .01<.9/3,
 'independent_hold_cannot_be_endogenous': F(1,2)*4 > (1-F(1,2))*(F(1,2)*4),
 'diagonal_gain_omits_transport': F(900)>F(17,20),
 'atomic_acquisition_is_not_continuous_mass': 1 > .001**.5,
 'stopped_time_selection': 1-(1-.01)**100 > .6,
 'free_clock_breaks_label_cut': sum(F(1,2)*(F(j)-F(1,2))**2 for j in (0,1))==F(1,4) and sum(F(1,2)*(F(j)-F(j))**2 for j in (0,1))==0,
 'defect_allowance_not_error_floor': sum(abs(x-y) for x,y in zip((F(1,3),F(2,3)),(F(1,3),F(2,3))))/2==0 < F(1,10),
 'later_gain_cannot_be_omitted': 3**2*F(1,100)**2>F(1,100)**2,
}
for name,ok in negative.items():
    check('negative_control:'+name,ok)
print(json.dumps({'status':'PASS','finite_checks':sum(counts.values()),'groups':counts,'negative_controls':sorted(negative),'scope':'finite regression only; not a mathematical proof'},sort_keys=True,indent=2))
