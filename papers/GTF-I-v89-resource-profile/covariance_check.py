#!/usr/bin/env python3
"""Finite exact checks for the written covariance and affine-repair theorems."""
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import sympy as s
from covariance_metric import (require,inner,covariance,system,solve,certify,verify,
    affine_repair,PAIR,matrix_to_json,psd,matrix_tuple_legal)
from matrix_metric import sylvester_solution
count=0;negative=0

def check(ok,message):
    global count
    require(bool(ok),message);count+=1

def rejects(fn):
    global negative
    try:fn()
    except ValueError:negative+=1;return
    raise ValueError('negative control incorrectly accepted')

def rawpair(e,f):
    return {'schema':PAIR,'dimension':e[0].rows,'outcomes':len(e),
            'effects_e':[matrix_to_json(x) for x in e],
            'effects_f':[matrix_to_json(x) for x in f]}

I=s.eye(2);Z=s.zeros(2);x=s.Matrix([[0,1],[1,0]])
y=s.Matrix([[0,-s.I],[s.I,0]]);z=s.diag(1,-1)
e=[I/3+x/12,I/3+z/12,I/3-(x+z)/12]
f=[I/3+y/16,I/3+(z-x)/16,I/3-(y+z-x)/16]
values=[x+y,z-x,-y-z]
for a in [e,f,[s.diag(1,0),s.diag(0,1),Z],
          [(I+z)/4,(I-z)/4,(I+x)/4,(I-x)/4]]:
    k=len(a);K=values if k==3 else [x,y,z,-x-y-z]
    S=sum((aa*kk for aa,kk in zip(a,K)),Z)
    C=covariance(a,K);q=inner(K,C)
    check(sum(C,Z)==Z,'covariance range not tangent')
    check(q==s.expand(sum(s.trace(aa*kk*kk) for aa,kk in zip(a,K))-s.trace(S.adjoint()*S)),
          'covariance energy identity')
    check(all(v==Z for v in covariance(a,[x]*k)),'constant tuple not annihilated')
    check(q>=0,'negative covariance energy')
    basis,G,L=system(a);check(psd(L),'covariance matrix not PSD')
    if k==3 and a[0]==s.diag(1,0):check(L==s.zeros(L.rows),'PVM covariance not zero')
    if k==4:check(L!=s.zeros(L.rows),'nonprojective rank-one tuple falsely flat')
# Noncommuting concavity and noise-floor identities.
Sdiff=sum(((ff-ee)*kk for ee,ff,kk in zip(e,f,values)),Z)
for t in [s.Rational(0),s.Rational(1,7),s.Rational(1,2),s.Rational(1)]:
    mid=[(1-t)*a+t*b for a,b in zip(e,f)]
    actual=inner(values,covariance(mid,values))-(1-t)*inner(values,covariance(e,values))-t*inner(values,covariance(f,values))
    check(actual==s.expand(t*(1-t)*s.trace(Sdiff.adjoint()*Sdiff)),'concavity cross term')
    noisy=[(1-t)*a+t*I/3 for a in e]
    _,G,L=system(noisy);_,_,LE=system(e)
    check(psd(L-(1-t)*LE-t*G/3),'noise floor failed')
# Binary reduction and exact Gram-sensitive solve, including singular endpoints.
p=s.diag(1,0);v=s.Matrix([s.Rational(3,5),s.Rational(4,5)]);p2=v*v.T
binary=[(p,p2),(I/2,I/2+x/20),(I/2+z/4,I/2+y/8),
        (Z,I/40)]
for a,b in binary:
    mid=(a+b)/2;H=b-a;V=mid*(I-mid)
    for N in [1,2,7]:
        q,K,G,L=solve([mid,I-mid],[H,-H],N)
        old=N*s.trace(H*sylvester_solution(V,H,s.Rational(1,N)))
        check(q==2*old,'binary scalar normalization mismatch')
        check(K[0]==-K[1],'binary inverse leaves tangent space')
        check(covariance([mid,I-mid],[H,-H])[0]==(V*H+H*V).applyfunc(s.expand),
              'binary covariance not exact variance operator')
# Relabeling and rational unitary invariance.
q,*_=solve([(a+b)/2 for a,b in zip(e,f)],[b-a for a,b in zip(e,f)],5)
U=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
for permutation in [(2,0,1),(1,2,0)]:
    a=[e[i] for i in permutation];b=[f[i] for i in permutation]
    check(solve([(aa+bb)/2 for aa,bb in zip(a,b)],[bb-aa for aa,bb in zip(a,b)],5)[0]==q,
          'label covariance invariance failed')
a=[U*v*U.T for v in e];b=[U*v*U.T for v in f]
check(solve([(aa+bb)/2 for aa,bb in zip(a,b)],[bb-aa for aa,bb in zip(a,b)],5)[0]==q,
      'unitary invariance failed')
T=s.Matrix([[1,s.Rational(1,2),0],[0,s.Rational(1,2),1]])
out=[sum((T[i,j]*e[j] for j in range(3)),Z) for i in range(2)]
L=[x+y,z-x];lift=[sum((T[i,j]*L[i] for i in range(2)),Z) for j in range(3)]
check(inner(L,covariance(out,L))>=inner(lift,covariance(e,lift)),'data processing failed')
# Exact scalar distribution comparisons are independent finite operational checks.
for ep,fp in [([1,0,0],[s.Rational(9,10),s.Rational(1,10),0]),
              ([s.Rational(1,3)]*3,[s.Rational(1,4),s.Rational(1,2),s.Rational(1,4)]),
              ([0,s.Rational(1,2),s.Rational(1,2)],[s.Rational(1,20),s.Rational(9,20),s.Rational(1,2)])]:
    a=[s.Matrix([[t]]) for t in ep];b=[s.Matrix([[t]]) for t in fp]
    for n in [1,2,3,4]:
        cert=certify(rawpair(a,b),n)
        distance=sum(abs(s.prod(ep[j] for j in word)-s.prod(fp[j] for j in word))
                     for word in product(range(3),repeat=n))
        check(distance**2<=s.Rational(cert['adaptive_upper_squared']),'scalar exact distance exceeds upper')
# Good-event affine repair, including spectral faces and non-normalized raw records.
boundary=[s.diag(s.Rational(1,2),s.Rational(1,6)),I/3,s.diag(s.Rational(1,6),s.Rational(1,2))]
for target in [e,boundary]:
    for a in [s.Rational(1,1000),s.Rational(1,16),s.Rational(1)]:
        for noise in [[x,y,z],[I,I,I],[-I,I,-I]]:
            raw=[b+a*n for b,n in zip(target,noise)];fixed,fallback=affine_repair(raw,a)
            check(not fallback and matrix_tuple_legal(fixed,True),'good event repair not legal')
            check(sum(fixed,Z)==I,'affine repair sum differs')
            bound=4*a/(1+12*a)
            check(all(psd(bound*I+(u-v)) and psd(bound*I-(u-v)) for u,v in zip(fixed,target)),
                  'affine repair exceeds proved bound')
fixed,fallback=affine_repair([100*I,-100*I,Z],s.Rational(1,100))
check(fallback and fixed==[I/3]*3,'bad-record fallback absent')
# Nonorthonormal basis regression: replacing G by identity changes the cutoff.
basis,G,L=system([(a+b)/2 for a,b in zip(e,f)])
rhs=s.Matrix([inner(a,[bb-aa for aa,bb in zip(e,f)]) for a in basis])
wrong=s.factor(5*(rhs.T*(L+s.eye(L.rows)/5).inv(method='DM')*rhs)[0])
check(wrong!=q,'Gram-omission negative fixture degenerate')
raw=rawpair(e,f);cert=certify(raw,5)
check(verify(raw,cert)['complete_exact_replay'],'complete certificate replay failed')
check(verify(raw,cert,expected_horizon=5)['complete_exact_replay'],'requested horizon replay failed')
rejects(lambda:verify(raw,cert,expected_horizon=6))
rejects(lambda:verify(raw,cert,expected_horizon=True))
for field,value in [('q_squared','0'),('adaptive_upper_squared','0'),('horizon',True),
                    ('gram_matrix_included',False),('exact_adaptive_distance_claimed',True)]:
    bad=deepcopy(cert);bad[field]=value;rejects(lambda:verify(raw,bad))
bad=deepcopy(raw);bad['effects_e'][0][0][0][0]='2/6';rejects(lambda:certify(bad,1))
bad=deepcopy(raw);bad['effects_e'][0][0][0][0]='-1';rejects(lambda:certify(bad,1))
bad=deepcopy(raw);bad['effects_e'][0][0][0][0]='1/2';rejects(lambda:certify(bad,1))
bad=deepcopy(raw);bad['effects_e'][0][0][1][1]='1';rejects(lambda:certify(bad,1))
bad=deepcopy(raw);bad['dimension']=True;rejects(lambda:certify(bad,1))
bad=deepcopy(raw);bad['unexpected']=0;rejects(lambda:certify(bad,1))
rejects(lambda:certify(raw,0));rejects(lambda:certify(raw,5,1))
rejects(lambda:affine_repair(e,s.Rational(0)))
rejects(lambda:affine_repair([s.Matrix([[0,1],[0,0]]),I],s.Rational(1,10)))
print(json.dumps({'schema':'gtf83.covariance-check/1','status':'success',
 'positive_checks':count,'negative_controls':negative,'fixture_q_squared':str(q),
 'exact_scalar_product_comparisons':12,'noncommuting_matrix_tests':True,
 'boundary_and_zero_effect_tests':True,'binary_identity_checked':True,
 'gram_omission_detected':True,'affine_good_and_bad_records_checked':True,
 'continuum_theorem_verified_by_finite_tests':False,'physical_learner_executed':False},
 indent=2,sort_keys=True))
