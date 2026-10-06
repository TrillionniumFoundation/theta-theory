#!/usr/bin/env python3
"""Finite R62 fixtures. These checks are not proofs of the quantified theorems."""
from fractions import Fraction as Q
from itertools import permutations,product
from pathlib import Path
import hashlib,json
import numpy as np
import sympy as s
from spectral_value import majorant,root_interval,certify

def require(ok,message):
    if not ok:raise RuntimeError(message)
def exact_matrix(a,b,message):
    require(a.shape==b.shape and all(s.simplify(x)==0 for x in a-b),message)
def swap(d):
    return s.Matrix(d*d,d*d,lambda a,b:int(a//d==b%d and a%d==b//d))
exact=0;numerical=0;negative=0
# Exact ordered qutrit moments, using the root-of-unity cancellation formula.
d=3;I=s.eye(9);S=swap(3)
for y in range(3):
    for z in range(3):
        M=s.zeros(9)
        for x,u,xp,up in product(range(3),repeat=4):
            if y==z:
                chirp=int((x+u-xp-up)%3==0 and (x*x+u*u-xp*xp-up*up)%3==0)
                coord=int(x==u==xp==up)
                M[3*x+u,3*xp+up]=s.Rational(chirp+coord,12)
            else:
                # Each other ordered label receives half of P_y tensor (I-P_y).
                ch=int((x+u-xp-up)%3==0 and (x*x+u*u-xp*xp-up*up)%3==0)
                co=int(x==u==xp==up)
                M[3*x+u,3*xp+up]=(s.Rational(int(x==xp and u==up),3)-s.Rational(ch+co,12))/2
        target=(I+S)/12 if y==z else (3*I-S)/24
        exact_matrix(M,target,'ordered qutrit moment');exact+=1
# A separate numerical construction checks all 24 actual bases, not just moments.
w=np.exp(2j*np.pi/3);bases=[np.eye(3,dtype=complex)]
for a in range(3):bases.append(np.array([[w**((a*x*x+j*x)%3)/np.sqrt(3) for j in range(3)] for x in range(3)]))
ordered=[U[:,p] for U in bases for p in permutations(range(3))]
for U in ordered:
    require(np.linalg.norm(U.conj().T@U-np.eye(3))<1e-12,'orthonormal ordered basis');numerical+=1
for y in range(3):
 for z in range(3):
    M=sum(np.kron(np.outer(U[:,y],U[:,y].conj()),np.outer(U[:,z],U[:,z].conj())) for U in ordered)/24
    target=np.array((I+S)/12 if y==z else (3*I-S)/24,dtype=complex)
    require(np.linalg.norm(M-target)<1e-12,'actual 24-basis second moments');numerical+=1
# Support-exact finite instrument, normalized readouts and actual conditional scores.
C0=s.diag(s.sqrt(3)/2,s.sqrt(2)/4,s.sqrt(2)/4)
Vs=[s.Matrix([[1/s.sqrt(2),0,0],[0,1,0]]),s.Matrix([[1/s.sqrt(2),0,0],[0,0,1]])]
Ds=[s.Matrix([[1/s.sqrt(2),0,0],[0,1/s.sqrt(2),0]]),s.Matrix([[1/s.sqrt(2),0,0],[0,0,1/s.sqrt(2)]])]
As=[s.diag(s.Rational(3,4),s.Rational(1,4),0),s.diag(s.Rational(3,4),0,s.Rational(1,4))]
exact_matrix(sum((V.H*V for V in Vs),s.zeros(3)),s.eye(3),'instrument completeness');exact+=1
pm=s.Matrix([0,1,-1,0])/s.sqrt(2);F=pm*pm.H
exact_matrix(F*F,F,'normalized antisymmetric projector');exact+=1
for V,D,A in zip(Vs,Ds,As):
 C=V*C0;exact_matrix(C.H*C,A/2,'old Gram');require(s.trace(D.H*D)==1,'fresh normalization')
 T=s.kronecker_product(C,D);K=s.simplify(T*S*T.H)
 exact_matrix(K*pm,-s.sqrt(3)*pm/16,'exact filtered-swap negative eigenpair');exact+=3
Pmsg=s.Rational(4,7)+s.sqrt(3)/56;Pnm=s.Rational(4,7)+s.sqrt(6)/112
alternatives_msg=[];alternatives_nm=[]
for U in ordered:
 Es=[np.outer(U[:,y],U[:,y].conj()) for y in range(3)]
 for is_scalar in (False,True):
    effects=[np.eye(3)/3]*3 if is_scalar else Es
    out=0.;nom=0.
    for y in range(3):
     for V,D in zip(Vs,Ds):
        C=np.array(V*C0,complex);Dnp=np.array(D,complex)
        out+=np.trace(np.array(F,complex)@np.kron(C@effects[y].T@C.conj().T,Dnp@effects[y].T@Dnp.conj().T)).real
     C=np.array(C0,complex);Dnp=np.array(Ds[0],complex)
     vec=np.zeros(6);vec[1]=1/np.sqrt(2);vec[2]=-1/np.sqrt(2)
     nom+=np.trace(np.outer(vec,vec)@np.kron(C@effects[y].T@C.conj().T,Dnp@effects[y].T@Dnp.conj().T)).real
    # The fixed initial spectrum breaks covariance: individual basis scores vary.
    if is_scalar:scalar_msg=out;scalar_nm=nom
    else:alt_msg=out;alt_nm=nom
    numerical+=2
 alternatives_msg.append(alt_msg);alternatives_nm.append(alt_nm)
require(abs(3*scalar_msg/7+4*(1-sum(alternatives_msg)/24)/7-float(Pmsg))<1e-12,'actual ensemble instrument Bayes value')
require(abs(3*scalar_nm/7+4*(1-sum(alternatives_nm)/24)/7-float(Pnm))<1e-12,'actual ensemble no-message Bayes value');numerical+=2
# A singular support in an oversized receiver: the completion adds no outcome.
C=s.Matrix([[s.sqrt(2)/2,0],[0,s.sqrt(2)/2],[0,0]])
Cplus=s.Matrix([[s.sqrt(2),0,0],[0,s.sqrt(2),0]])
chs=[s.Matrix([[s.sqrt(2)/2,0]]),s.Matrix([[0,s.sqrt(2)/2]])]
V=[ch*Cplus for ch in chs];PS=s.diag(1,1,0)
exact_matrix(sum((x.H*x for x in V),s.zeros(3)),PS,'support completeness')
for x,ch in zip(V,chs):exact_matrix(x*C,ch,'support inverse realization');exact+=1
extra=s.Matrix([[0,0,1]])
exact_matrix(sum((x.H*x for x in V+[extra]),s.zeros(3)),s.eye(3),'same-outcome CP completion');exact+=2
require(extra*C==s.zeros(1,2),'completion does not touch initial support');exact+=1
# A complex rectangular instrument checks the Heisenberg identity under all hypotheses.
K=[s.Matrix([[1,0],[0,s.I],[0,0]])/s.sqrt(2),s.Matrix([[0,1],[1,0]])/s.sqrt(2)]
X=s.Matrix([[s.Rational(2,3),s.I/6],[-s.I/6,s.Rational(1,3)]])
Z=s.Matrix([[s.Rational(3,5),s.Rational(1,5)],[s.Rational(1,5),s.Rational(2,5)]])
Ms=[];G=s.zeros(4);lhs=0
for index,k in enumerate(K):
 n=k.rows*2;v=s.Matrix([1]+[s.I if j==1 else 0 for j in range(1,n)]);M=v*v.H/2
 Ms.append(M);A=s.kronecker_product(k,s.eye(2));G+=A.H*M*A
 lhs+=s.trace(M*s.kronecker_product(k*X*k.H,Z))
exact_matrix(sum((k.H*k for k in K),s.zeros(2)),s.eye(2),'complex Kraus completeness');exact+=1
require(s.simplify(lhs-s.trace(G*s.kronecker_product(X,Z)))==0,'Heisenberg decision identity');exact+=1
require(all(e>=0 for e in G.eigenvals()) and all(e>=0 for e in (s.eye(4)-G).eigenvals()),'postponed POVM positivity');exact+=2
# Exact rational water-map continuity and L1 contraction at and across ties.
for d in range(2,7):
 for r in range(1,d+1):
  for seed in range(1,13):
   aa=[(seed+i*i)%11 for i in range(d)];bb=[(seed*3+i)%7 for i in range(d)]
   if not sum(aa) or not sum(bb):continue
   a=tuple(sorted((Q(x,sum(aa)) for x in aa),reverse=True));b=tuple(sorted((Q(x,sum(bb)) for x in bb),reverse=True))
   qa,qb=majorant(a,r),majorant(b,r)
   require(sum(abs(x-y) for x,y in zip(qa,qb))<=sum(abs(x-y) for x,y in zip(a,b)),'water map contraction')
   require(sum(qa)==1 and sum(x>0 for x in qa)<=r,'water normalization and rank');exact+=2
for a,b in [(Q(433,1000),Q(434,1000)),(Q(306,1000),Q(307,1000))]:
 target=Q(3,16) if a>Q(2,5) else Q(3,32)
 require(a*a<target<b*b,'rational algebraic enclosure');exact+=1
example=certify({'spectrum':['3/4','1/8','1/8'],'old_dimension':3,'fresh_dimension':2})
require(Q(example['no_message_comparison']['gain_interval'][0])>0,'strict rational message interval');exact+=1
# Negative controls: changing a resource/quantifier cannot be silently certified.
require(s.simplify(Pmsg-Pnm)>0,'not every continuation is concave');negative+=1
require(not example['scope']['equal_prior_formula_claimed'],'biased formula is not equal prior');negative+=1
require(not example['scope']['physical_reset_calibration'],'score does not calibrate reset');negative+=1
for data in [{'spectrum':[.75,.125,.125]}, {'spectrum':['3/4','1/8','1/8'],'fresh_dimension':True},
             {'spectrum':['1','0'],'fresh_dimension':0}, {'spectrum':['1','0'],'t':'2'}]:
 try:certify(data)
 except ValueError:negative+=1
 else:raise RuntimeError('illegal spectral input accepted')
# A source which sees the message can create classical correlations absent from a fixed source.
Z0=s.diag(1,0);Z1=s.diag(0,1);T0=s.diag(1,0);T1=s.diag(0,1)
correlated=(s.kronecker_product(T0,Z0)+s.kronecker_product(T1,Z1))/2
independent=s.eye(4)/4
require(correlated!=independent,'receiver-dependent fresh source is not a common tensor factor');negative+=1
require(C.rows>1,'postponement would retain too much under a one-dimensional old cut');negative+=1
require(majorant((Q(1),Q(0),Q(0)),2)==(Q(1),Q(0),Q(0)),'pure support cannot force a positive root');negative+=1
require(not certify({'spectrum':['3/4','1/8','1/8'],'fresh_dimension':2,'t':'0'})['no_message_comparison']['strict_gain_criterion'],'zero signal has no strict gain');negative+=1
require(not certify({'spectrum':['3/4','1/8','1/8'],'fresh_dimension':3})['no_message_comparison']['strict_gain_criterion'],'initial-rank saturation');negative+=1
print(json.dumps({'schema':'gtf96.referee-resolution-check/1','status':'success','exact_checks':exact,
 'numerical_sanity_checks':numerical,'negative_controls':negative,'numerical_tolerance':'1e-12',
 'qutrit_ordered_bases':len(ordered),'example_certificate_sha256':hashlib.sha256(json.dumps(example,sort_keys=True).encode()).hexdigest(),
 'continuum_proof_by_replay':False,'physical_calibration':False,'independent_priority_clearance':False},sort_keys=True))
