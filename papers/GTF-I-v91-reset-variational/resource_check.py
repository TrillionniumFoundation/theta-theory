#!/usr/bin/env python3
"""Exact budget, tester-inclusion witness, and reset-defect regressions."""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
import sympy as s
import resource_budget as r

count=0;negative=0

def check(ok):
    global count
    if not ok:raise ValueError('resource regression failed at '+str(count))
    count+=1

def reject(fn):
    global negative
    try:fn()
    except (ValueError,TypeError,KeyError):negative+=1;return
    raise ValueError('invalid resource input accepted')

def ptr_first(a,d1,d2):
    return s.Matrix(d1*d2,d1*d2,lambda x,y:a[(y//d2)*d2+x%d2,(x//d2)*d2+y%d2])

for N in range(1,40):
    for Q in range(N,N*N+1):
        c=r.budget_witness(N,Q);w=c['run_length']
        check(w['full_blocks']*w['block_size']+w['residual']==N)
        check(4*c['realized_square_cost']>=Q and c['realized_square_cost']<=Q)
# Huge binary integers must not expand an exponentially large list of blocks.
check(r.budget_witness(10**90,10**90)['run_length']['full_blocks']==10**90)
for args in [(True,1),(1,True),(0,0),(3,2),(3,10),(2.0,3),(2,3.0)]:reject(lambda a=args:r.budget_witness(*a))

nodes={'a':{'calls':1,'children':['b','c']},'b':{'calls':2,'children':['z']},
       'c':{'calls':1,'children':['z']},'z':{'calls':0,'children':[]}}
policy={'schema':'gtf88.reset-policy/1','N':3,'b':2,'s':'1/100','gamma':'3/2','root':'a','nodes':nodes}
payload={'schema':'gtf89.quadratic-input/1','N':3,'Q':5,'policy':policy,
         'reset_defects':{'a':'1/100','b':'1/50','c':'1/200','z':'0'}}
cert=r.analyze(payload);check(cert['policy']['square_cost']==5)
check(cert['conditional_reset_defect']['worst_path_sum']=='3/100')
check(r.verify(payload,cert)==cert)
for field in ['input_sha256','witness','policy','conditional_reset_defect']:
    mutant=deepcopy(cert);mutant[field]='tampered';reject(lambda m=mutant:r.verify(payload,m))
mutant=deepcopy(cert);mutant['witness']['calls']=True;reject(lambda:r.verify(payload,mutant))
for mutate in [lambda d:d.update(Q=4),lambda d:d['reset_defects'].pop('z'),
               lambda d:d['reset_defects'].update(z='1/100'),
               lambda d:d['reset_defects'].update(a='2/200'),
               lambda d:d['reset_defects'].update(a='-1/100'),
               lambda d:d['policy']['nodes']['c']['children'].append('a')]:
    bad=deepcopy(payload);mutate(bad);reject(lambda b=bad:r.analyze(b))
reject(lambda:r.analyze(payload,max_nodes=3))

# Two-call reset tester with an entangled final receiver measurement.
I=s.eye(2);zero=s.Matrix([[1,0],[0,0]]);phi=s.Matrix([1,0,0,1]);Pi=phi*phi.T/2
# Convert ordering I1,I2,Y1,Y2 to complete slots I1,Y1,I2,Y2.
perm=[]
for i1,y1,i2,y2 in product(range(2),repeat=4):perm.append(8*i1+4*i2+2*y1+y2)
raw=s.kronecker_product(Pi,zero,zero)/4
T0=raw.extract(perm,perm);Tsum=s.eye(16)/4;T1=Tsum-T0
check(T0==T0.H and T1==T1.H)
check(all(v>=0 for v in T0.eigenvals()) and all(v>=0 for v in T1.eigenvals()))
check(T0+T1==Tsum)
PT=ptr_first(T0,4,4);check(min(PT.eigenvals())==s.Rational(-1,8))
check(PT.trace()==T0.trace())
# Exact contraction to two measurement-channel Choi matrices, including complex effects.
X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
effects=[I/2,I/2+X/4,I/2+Y/4,I/2+Z/4,zero,(I+X)/2]
for A,B in product(effects,repeat=2):
    JA=s.kronecker_product(A.T,zero)+s.kronecker_product((I-A).T,I-zero)
    JB=s.kronecker_product(B.T,zero)+s.kronecker_product((I-B).T,I-zero)
    tester=s.simplify((T0*s.kronecker_product(JA,JB)).trace())
    physical=s.simplify((Pi*s.kronecker_product(A.T/2,B.T/2)).trace())
    check(tester==physical and 0<=physical<=1)
    check(s.simplify(((T0+T1)*s.kronecker_product(JA,JB)).trace())==1)
# Every sample positive-product classical tester effect has a positive partial transpose.
for A,B in product(effects,repeat=2):
    M=s.kronecker_product(s.kronecker_product(A,zero),s.kronecker_product(B,I))
    check(all(v>=0 for v in ptr_first(M,4,4).eigenvals()))

# Complete classical replays of approximate fresh preparations with coherent-capable memory replaced by a classical register.
# Ideal X is carried unchanged; new Y is independent. Actual Y depends on old X.
replays=0
for depth in range(1,5):
  for theta,eps in product([F(1,3),F(1,2),F(2,3)],[F(0),F(1,100),F(1,20)]):
    ideal={():F(1)};actual={():F(1)}
    for _ in range(depth):
      ii={};aa={}
      for hist,p in ideal.items():
        for y in [0,1]:ii[hist+(y,)]=p*(theta if y else 1-theta)
      for hist,p in actual.items():
        q=theta+(eps if hist and hist[-1] else -eps)
        for y in [0,1]:aa[hist+(y,)]=p*(q if y else 1-q)
      ideal,actual=ii,aa
    norm=sum(abs(actual[h]-ideal[h]) for h in ideal)
    check(sum(ideal.values())==sum(actual.values())==1)
    check(norm<=2*depth*eps)
    replays+=1

print(json.dumps({'schema':'gtf89.resource-regression/1','status':'success','checks':count,
 'negative_controls':negative,'memory_witness_partial_transpose_eigenvalue':'-1/8',
 'measurement_channel_contractions':36,'complete_reset_defect_laws':replays,
 'all_hard_budgets_checked_through_N':39,
 'physical_reset_calibrated':False,'general_recovery_executed':False,
 'continuum_theorems_proved_by_tests':False,'priority_certified':False},indent=2,sort_keys=True))
