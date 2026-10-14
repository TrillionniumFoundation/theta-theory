#!/usr/bin/env python3
"""Finite exact and numerical regression fixtures, not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
import numpy as np
from check_v77 import require


def checks() -> dict:
    counts = dict(normalized_inverse=0, endpoint_forcing=0, product_guard=0,
                  geometric_split=0, target_jacobian=0, decision_current=0,
                  peak_phases=0, ordered_exponents=0)
    q=F(47,53); R=F(47,100); tau=F(3,50); ca=R/(2*(1-q))
    require((2/tau)/(2/tau+2/R)==q, 'physical row-sum constant')
    counts['normalized_inverse']+=1
    rng=np.random.default_rng(780177)
    for n in (1,2,4,9,17):
        for scale in (1.,.01,.00001):
            c=scale*(.1+.9*rng.random(n)); lengths=.06+2*rng.random(n+1)
            t=1/lengths
            a=np.diag(t[:-1]+t[1:]+2/(float(R)*c))
            if n>1: a+=np.diag(-t[1:-1],1)+np.diag(-t[1:-1],-1)
            inv=np.linalg.inv(a)
            for i,j in itertools.product(range(n),repeat=2):
                bound=float(ca)*min(c[i],c[j])*float(q)**abs(i-j)
                require(-1e-13<=inv[i,j]<=bound*(1+1e-10), 'incidence inverse fixture')
                require(inv[i,j]/c[i]<=float(ca)*float(q)**abs(i-j)*(1+1e-10),
                        'normalized inverse fixture')
                counts['normalized_inverse']+=2
            for u,v in ((1.,0.),(0.,1.),(.7,-.4)):
                forcing=np.zeros(n);forcing[0]+=t[0]*u;forcing[-1]+=t[-1]*v
                actual=np.linalg.solve(a,forcing)/c
                for j in range(n):
                    bound=float(ca/tau)*(float(q)**j*abs(u)+float(q)**(n-1-j)*abs(v))
                    require(abs(actual[j])<=bound*(1+1e-10),'endpoint forcing fixture')
                    counts['endpoint_forcing']+=1
    values=(F(0),F(1,4),F(1,2),F(1))
    for aa,bb in itertools.product(itertools.product(values,repeat=3),repeat=2):
        pa=math.prod(aa);pb=math.prod(bb)
        require(abs(pa-pb)<=sum(abs(a-b) for a,b in zip(aa,bb)), 'complete product telescoping')
        counts['product_guard']+=1
    for w,wp,J in itertools.product(values,values,(F(0),F(1,4),F(1),F(3,2),F(7))):
        require(max(F(0),w-wp*J)<=w*max(F(0),1-J)+J*abs(w-wp),'geometry/guard split')
        counts['geometric_split']+=1
    # Source slots have mass mu; target slots have mass J*mu, not mu/J.
    for mu,J,w,wp in itertools.product((F(1,3),F(2)),(F(1,4),F(1),F(4)),values,values):
        source=w*mu;target=wp*J*mu
        geom=w*max(F(0),1-J)*mu
        guard=abs(w-wp)*J*mu
        require(source<=target+geom+guard,'target-direction coarea fixture')
        counts['target_jacobian']+=1
    for u,v in itertools.product(range(8),repeat=2):
        primitive={j:F(1 if v>u else -1) for j in range(min(u,v),max(u,v))}
        for n in range(10):
            current=F(int(n==v)-int(n==u))
            coeff=primitive.get(n-1,F(0))-primitive.get(n,F(0))
            require(current==coeff,'exact unpooled occupation coefficient')
            counts['decision_current']+=1
        for z in (F(-2),F(-1),F(0),F(1),F(3,2)):
            require(z**v-z**u==(z-1)*sum((a*z**j for j,a in primitive.items()),F(0)),
                    'coincident decision interface factor')
            counts['decision_current']+=1
    for phase in (0.,math.pi/3,math.pi):
        for delta in (-.2,-.001,.003,.15):
            lhs=abs(complex(math.cos(phase+delta),math.sin(phase+delta))-
                    complex(math.cos(phase),math.sin(phase)))
            require(lhs<=abs(delta)+1e-14,'peak phase Lipschitz difference')
            counts['peak_phases']+=1
    require(abs(complex(math.cos(math.pi),math.sin(math.pi))-1)>1.9,
            'nonzero occupation peak does not acquire an ordinary difference gain')
    counts['peak_phases']+=1
    require(F(1,12)*F(1,16)==F(1,192),'outer exponent')
    counts['ordered_exponents']+=1
    for exponent,beta in itertools.product((F(0),F(1),F(8)),(F(1,4),F(1,2),F(1))):
        gamma=max(F(2),exponent/beta)+1
        require(-1+gamma/2>0 and -exponent+gamma*beta>0,'legal fixed width powers')
        counts['ordered_exponents']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite identities, exact rational inequalities, seeded optical matrices and phase fixtures only',
            'full_raw_return_LLT_proved':False,'independent_human_review':False,
            'formal_proof_certificate':False}


if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
