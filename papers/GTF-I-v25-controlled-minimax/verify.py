#!/usr/bin/env python3
"""Exact regression checks. They complement, and do not certify, the proofs."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json
import sys
import sympy as s


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> dict:
    p, q, gamma, z = s.symbols('p q gamma z', real=True)
    a, c = (1-p)*(1-q), p*q
    target = s.Matrix([(1+gamma)/4,(1-gamma)/4,(1-gamma)/4,(1+gamma)/4])
    signed = target-s.Matrix([a,a,c,c])/2
    tau=2*z/(z+2-gamma)
    payoff=a*signed.dot(s.Matrix([tau,0,1,1]))+(1-a-c)*sum(signed)+c*signed.dot(s.Matrix([1,1,0,tau]))
    u, v = (p+q-1)**2, (p-q)**2
    root=z*z+(4-2*gamma)*z-(1+2*gamma)
    identity=payoff-(3+z*z)/8-(2-tau)*((u-v-z)**2+4*v)/16
    numerator=s.fraction(s.cancel(identity))[0]
    require(s.rem(numerator,root,z)==0, 'marked square identity failed')
    first=(1+gamma)*(1+z)/8-(1+6*z+z*z)/16
    require(s.expand(first+root/16)==0, 'least favorable tie failed')
    zg=(s.sqrt(73)-7)/4
    exact=(85-7*s.sqrt(73))/64
    require(s.simplify((3+zg*zg)/8-exact)==0, 'original value failed')
    require(s.simplify(2*zg/(zg+s.Rational(7,4))-(2-14/s.sqrt(73)))==0, 'original coin failed')
    require(s.simplify(root.subs(z,1-2*gamma)-8*(gamma*gamma-2*gamma+s.Rational(1,2)))==0, 'parameter interval failed')
    # The old four-point rational certificate remains independently checked.
    ts=[F(1,8),F(1,5),F(4,5),F(7,8)]
    weights=[F(1,16),F(7,16),F(7,16),F(1,16)]
    Q=[F(5,16),F(3,16),F(3,16),F(5,16)]
    table=[]
    for k in range(3):
        row=[]
        for j in range(4):
            val=sum(w*(1 if k!=1 else 2)*t**k*(1-t)**(2-k)*(Q[j]-((1-t)**2 if j<2 else t*t)/2) for t,w in zip(ts,weights))
            row.append(val)
        table.append(row)
    expected=[[-1977,-1775177,2170423,3943623],[1765554,191954,191954,1765554],[3943623,2170423,-1775177,-1977]]
    require(table==[[F(v,40960000) for v in row] for row in expected], 'old certificate changed')
    require(sum(max(F(0),v) for row in table for v in row)==F(4035777,10240000),'old bound failed')
    # Exact finite controlled-experiment example, no floating-point LP.
    theta=list(product(range(2),repeat=2))
    actions=['R','L','H']
    def prob(t,act,x):
        i,j=t
        if act=='R': return F(int(x==i))
        if (act=='L' and i==0) or (act=='H' and i==1): return F(int(x==j))
        return F(1,2)
    values=[]
    for aa in actions:
        row=[]
        for bb in actions:
            val=F(0)
            for x,y in product(range(2),repeat=2):
                likelihood=[prob(t,aa,x)*prob(t,bb,y) for t in theta]
                val+=sum(max(F(0),sum(likelihood)/16-L/4) for L in likelihood)
            row.append(val)
        values.append(row)
    desired=[[F(1,2),F(5,8),F(5,8)],[F(5,8),F(7,16),F(1,2)],[F(5,8),F(1,2),F(7,16)]]
    require(values==desired, 'nonadaptive Bayes table failed: '+str(values))
    def terminal(nu):
        return sum(max(F(0),sum(nu)/4-v) for v in nu)
    def bellman(n,nu):
        stop=terminal(nu)
        if n==0:return stop
        return max([stop]+[sum(bellman(n-1,[v*prob(t,aa,x) for t,v in zip(theta,nu)]) for x in range(2)) for aa in actions])
    require(bellman(2,[F(1,4)]*4)==F(3,4),'controlled recursion failed')
    # Exhaust every deterministic channel for several small alphabets.
    partitions=0
    for m in [2,4,8]:
        for K in [1,2,4]:
            if K>m or K**m>70000:continue
            best=F(-1)
            for assignment in product(range(K),repeat=m):
                ns=[assignment.count(j) for j in range(K)]
                val=1-sum(F(n,m)**2 for n in ns)
                best=max(best,val); partitions+=1
            require(best==1-F(1,K),'channel optimum failed')
            for N in range(5):
                alpha=F(1,3); er=(1-alpha)**N
                r=[F(1,K)]*K
                for th in range(m):
                    group=th//(m//K)
                    state=[er*r[j]+(1-er)*int(j==group) for j in range(K)]
                    reward=sum(state[j]*(1-F(1,K)-int(j!=group)) for j in range(K))
                    require(reward==(1-er)*(1-F(1,K)), 'joint construction failed')
    # Rational geometric inequalities used by the physical bridge.
    require(F(1,4)**2+F(113,200)**2+F(1,40)**2<F(9,10)**2,'collision time bound')
    require(1-(F(113,200)**2+F(1,40)**2)/F(9,10)**2>F(77,100)**2,'contact normal bound')
    require(-F(3,200)+F(1443,1000)*F(87,220)>F(1,2),'outgoing signal bound')
    require(sum(F(9,2)**j/F(__import__('math').factorial(j)) for j in range(10))>80,'Gaussian tail exponential bound')
    # Negative controls must fail the same algebraic checks, even under python -O.
    rejected=0
    for wrong in [identity+F(1,100), identity-v/16, identity+u/16]:
        num=s.fraction(s.cancel(wrong))[0]
        try: require(s.rem(num,root,z)==0,'deliberately false identity')
        except RuntimeError: rejected+=1
    require(rejected==3,'negative controls did not trigger')
    return {'schema':'gtf25.exact-checks/1','marked_square_identity':True,'least_favorable_tie':True,'parameter_interval':True,'old_rational_certificate':True,'controlled_table':[[str(v) for v in row] for row in values],'adaptive_value':'3/4','deterministic_channels_checked':partitions,'physical_rational_bounds':True,'negative_controls_detected':rejected,'exact_one_preparation_value':str(exact),'interpretation':'Exact regression checks, not independent proof certification or novelty clearance.'}

if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
