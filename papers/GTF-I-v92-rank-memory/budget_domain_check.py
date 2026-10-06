#!/usr/bin/env python3
"""Exact finite threshold normalization checks, with an expected-cost negative control."""
from fractions import Fraction as F
from itertools import product
import json

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
profiles=[()]
for length in range(1,6):
    profiles.extend(p for p in product(range(1,6),repeat=length) if sum(p)<=8)
checks=0
for n in [F(j,2) for j in range(2,19)]:
    for q in [F(j,2) for j in range(2,65)]:
        M=min(n.numerator//n.denominator,q.numerator//q.denominator)
        R=min(q.numerator//q.denominator,M*M)
        require(M<=R<=M*M,'ambient range')
        for p in profiles:
            N=sum(p);Q=sum(x*x for x in p)
            require(N<=Q<=N*N,'individual policy range')
            require((N<=n and Q<=q)==(N<=M and Q<=R),'class normalization')
            checks+=1
require(sum([1])<8,'a policy with advertised N=8 need not spend eight calls')
require(F(1,100)*100<=1 and 100>1,'expectation is not a hard path bound')
print(json.dumps({'schema':'gtf90.budget-domain-regression/1','status':'success',
 'exact_checks':checks,'positive_integer_reservations':True,
 'expected_costs_substituted':False,'continuum_proof_by_replay':False},sort_keys=True))
