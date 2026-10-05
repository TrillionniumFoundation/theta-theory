#!/usr/bin/env python3
"""Finite exact regression checks; continuum statements use the written proofs."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from copy import deepcopy
import json
import sympy as s
from finite_outcome_certificate import (
    require, grid_denominator, matrix_tuple_legal, matrix_tuple_within,
    matrix_record, check_readout, scalar_grid, verify_scalar)
from matrix_metric import is_positive_semidefinite as psd

count=0;negative=0

def check(ok,message):
    global count
    require(bool(ok),message);count+=1

def rejects(fn):
    global negative
    try: fn()
    except ValueError: negative+=1; return
    raise ValueError('negative control was incorrectly accepted')

I=s.eye(2);x=s.Matrix([[0,1],[1,0]]);y=s.Matrix([[0,-s.I],[s.I,0]]);z=s.diag(1,-1)
effects=[I/3+x/48,I/3+z/48,I/3-(x+z)/48]
h=[(x+z)/96,(y-x)/96,-(z+y)/96]
check(matrix_tuple_legal(effects),'noncommuting balanced tuple legality')
check(effects[0]*effects[1]!=effects[1]*effects[0],'fixture must not commute')
for t in [s.Rational(0),s.Rational(1,3),s.Rational(1)]:
    a=[u+t*v for u,v in zip(effects,h)]
    check(matrix_tuple_legal(a),'segment leaves balanced body')
    variance=s.zeros(2);horizontal=s.zeros(2)
    for u,v in zip(a,h):
        b=u.inv()*v/2
        check(s.simplify(u*b-v/2)==s.zeros(2),'horizontal first identity')
        check(s.simplify(b.adjoint()*u*b-v*u.inv()*v/4)==s.zeros(2),
              'horizontal squared derivative identity')
        horizontal+=u*b;variance+=v*u.inv()*v
    check(s.simplify(horizontal)==s.zeros(2),'normalization must cancel all horizontal terms')
    check(psd(s.simplify(6*sum((v*v for v in h),s.zeros(2))-variance)),
          'noncommutative inverse-order bound')
for k in range(2,8):
    f=I/2+(x+z)/32;m=k//2;q=s.Rational(2*m,k)
    a=[2*f/k]*m+[2*(I-f)/k]*m+([I/k] if k%2 else [])
    check(matrix_tuple_legal(a),'binary embedding not balanced')
    check(sum(a[:m],s.zeros(2))==q*f,'group coarse graining differs')
    check(q>=s.Rational(2,3),'embedding survival lower bound')
    for j in range(k):
        output=3*a[j]/4+sum((v/4 for i,v in enumerate(a) if i!=j),s.zeros(2))
        check(output==I/4+a[j]/2,'binary simulation is not an equality of effects')
# Exact inward rounding including the dependent final effect.
boundary=[s.diag(s.Rational(1,2),s.Rational(1,6)),I/3,
          s.diag(s.Rational(1,6),s.Rational(1,2))]
for a in [effects,boundary]:
    k=3;d=2;t=F(1,96);K=grid_denominator(d,k,t);e=s.Rational((k-1)*d,K)
    gamma=4*k*e;transformed=[(1-gamma)*v+gamma*I/k for v in a]
    rounded=[]
    for v in transformed[:-1]:
        b=s.zeros(d)
        for i in range(d):
            for j in range(i,d):
                re,im=s.expand(v[i,j]).as_real_imag()
                rr=s.floor(K*re+s.Rational(1,2))/K
                ri=0 if i==j else s.floor(K*im+s.Rational(1,2))/K
                b[i,j]=rr+s.I*ri;b[j,i]=rr-s.I*ri
        rounded.append(b)
    rounded.append(I-sum(rounded,s.zeros(d)))
    check(matrix_tuple_legal(rounded),'coupled rounding violated a spectral face')
    check(matrix_tuple_within(a,rounded,F(3)*F(e)),'rounding error budget differs')
# Every ternary length-two matrix record is retained; their traces sum to one.
records={t:matrix_record(effects,t) for t in product(range(3),repeat=2)}
check(sum(s.trace(v) for v in records.values())==1,'Choi records are not normalized')
check(all(psd(v) for v in records.values()),'a Choi record is not positive')
readout={t:[s.eye(4)/3,s.eye(4)*s.Rational(2,3)] for t in records}
check_readout(readout,3,2,4);count+=1
bad=deepcopy(readout);bad.pop((2,2));rejects(lambda:check_readout(bad,3,2,4))
bad=deepcopy(readout);bad[(0,0)]=[-s.eye(4),2*s.eye(4)];rejects(lambda:check_readout(bad,3,2,4))
bad=deepcopy(readout);bad[(0,0)]=[s.eye(4)/3,s.eye(4)/3];rejects(lambda:check_readout(bad,3,2,4))
check(matrix_tuple_within(effects,effects,F(0)),'closed equality test failed')
check(not matrix_tuple_legal([effects[0],effects[1],effects[2]+I/100]),
      'incorrect normalization was accepted')
# Full scalar certificate: no supplied grid or prefix can substitute for reconstruction.
raw=json.loads((Path(__file__).parent/'examples/finite-outcome-ternary.json').read_text())
result=verify_scalar(raw)
check(result['legal_grid_points']==3169 and result['classical_strings']==9,
      'complete scalar fixture inventory changed')
check(result['maximum_grid_failure']=='8225/36864','exact worst grid risk changed')
check(result['continuum_failure_allowance']=='3/8','trace/TV factor of two differs')
check(result['continuum_radius']=='7/24','moving-good-label radius not charged')
rejects(lambda:verify_scalar(raw,4000))
for mutate in [lambda q:q.update({'supplied_grid':[]}),
               lambda q:q['readout'].pop('2,2'),
               lambda q:q['centres'][0].__setitem__(0,'0'),
               lambda q:q['readout']['0,0'].__setitem__(0,'-1'),
               lambda q:q.update({'failure_bound':'0'}),
               lambda q:q.update({'good_radius':'2/8'}),
               lambda q:q.update({'calls':20})]:
    q=deepcopy(raw);mutate(q);rejects(lambda q=q:verify_scalar(q))
# Equality cases in scalar norms are counted as success.
K,_,grid=scalar_grid(3,F(1,24),10000)
check(any(g==tuple(F(v) for v in raw['centres'][0]) for g in grid),
      'dictionary equality point missing')
print(json.dumps({'schema':'gtf82.finite-outcome-check/1','status':'success',
 'exact_checks':count,'negative_controls':negative,'complete_scalar_certificate':result,
 'noncommuting_dimension':2,'noncommuting_outcomes':3,
 'matrix_grid_prefix_misrepresented_as_complete':False,
 'physical_learner_executed':False,'continuum_theorems_verified_by_finite_tests':False},
 indent=2,sort_keys=True))
