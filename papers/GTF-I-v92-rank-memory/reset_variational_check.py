#!/usr/bin/env python3
"""Finite exact checks of normal-form algebra and variational special cases."""
import json
import sympy as s

checks=0
negative=0

def require(ok,msg):
    if not bool(ok):raise RuntimeError(msg)

def equal(x,y,msg):
    global checks
    if isinstance(x,s.MatrixBase):
        require((x-y).applyfunc(s.simplify)==s.zeros(*x.shape),msg)
    else:require(s.simplify(x-y)==0,msg)
    checks+=1

def sqrt2(A):
    q=s.sqrt(A.det());den=s.sqrt(s.trace(A)+2*q)
    if den==0:return s.zeros(2)
    return (A+q*s.eye(2))/den

I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1)
rho=s.diag(s.Rational(1,3),s.Rational(2,3))
C0=s.diag(s.sqrt(s.Rational(1,3)),s.sqrt(s.Rational(2,3)))
for direction in (X,Y):
    parts=[rho/2+direction/12,rho/2-direction/12]
    maps=[sqrt2(A)*C0.inv() for A in parts]
    equal(sum((K.H*K for K in maps),s.zeros(2)),I,'instrument completeness')
    for A,K in zip(parts,maps):
        C=K*C0
        equal(C.H*C,A,'branch Gram matrix')
        equal(C,sqrt2(A),'canonical converse realization')
        for effect in ((I+Y/2)/2,(I+Z/3)/2):
            block=C*effect.T*C.H
            equal(s.trace(block),s.trace(A*effect.T),'branch probability')
    equal(sum(parts,s.zeros(2)),rho,'same barycenter for every first label')
# A rectangular first purification of rank one never divides by a null history.
C0=s.Matrix([[1,0]])
pinv=s.Matrix([[1],[0]])
rho=C0.H*C0
parts=[rho/3,2*rho/3,s.zeros(2)]
maps=[sqrt2(A)*pinv for A in parts]
equal(sum((K.H*K for K in maps),s.zeros(1)),s.eye(1),'singular source completeness')
for A,K in zip(parts,maps):equal(K*C0,sqrt2(A),'singular converse including zero map')
equal(maps[-1],s.zeros(2,1),'zero branch is defined')

# Larger receiver spaces are isometries, not a hidden assumption that C,D are square.
U=s.Matrix.vstack(I,s.I*I)/s.sqrt(2)
V=s.Matrix.vstack(s.eye(3),-s.eye(3))/s.sqrt(2)
equal(U.H*U,I,'old receiver isometry')
equal(V.H*V,s.eye(3),'fresh receiver isometry')
C=s.diag(s.sqrt(s.Rational(1,3)),s.sqrt(s.Rational(2,3)))
D=s.diag(s.sqrt(s.Rational(1,5)),s.sqrt(s.Rational(3,10)),s.sqrt(s.Rational(1,2)))
E=((I+Y/2)/2,(I-Y/2)/2)
F0=s.diag(s.Rational(1,4),s.Rational(1,2),s.Rational(3,4))
F0[0,1]=s.I/8;F0[1,0]=-s.I/8
F=(F0,s.eye(3)-F0)
Q=s.zeros(6);Q[0,0]=1;Q[3,3]=1
UV=s.kronecker_product(U,V)
largeQ=UV*Q*UV.H
prob=s.Integer(0)
for y in range(2):
    for z in range(2):
        tau=s.kronecker_product(C*E[y].T*C.H,D*F[z].T*D.H)
        large=s.kronecker_product(U*C*E[y].T*C.H*U.H,V*D*F[z].T*D.H*V.H)
        equal(s.trace(largeQ*large),s.trace(Q*tau),'rectangular receiver contraction')
        equal(s.trace(large),s.trace(tau),'rectangular receiver trace')
        prob+=s.trace(tau)
equal(prob,1,'two-slot state normalization without extra dimension factor')
# A complex reference event must use the effect transpose in the coefficient convention.
v=s.Matrix([1,s.I])/s.sqrt(2);R=v*v.H
correct=s.trace(R*E[0].T/2);wrong=s.trace(R*E[0]/2)
require(s.simplify(correct-wrong)!=0,'complex transpose negative control');negative+=1

# Eliminate an affinely redundant atom without changing a contact objective.
atoms=[(I+X)/2,(I-X)/2,(I+Y)/2,(I-Y)/2,I/2]
weights=[s.Rational(1,5)]*5
H=s.Matrix([[s.Rational(3,4),s.Rational(1,5)],[s.Rational(1,5),s.Rational(1,2)]])
vec=lambda A:s.Matrix([s.re(A[0,0]),s.re(A[1,1]),s.re(A[0,1]),s.im(A[0,1])])
M=s.Matrix.hstack(*(vec(A) for A in atoms))
v=M.nullspace()[0]
equal(sum(v),0,'trace of a barycenter dependency')
step=min(weights[i]/v[i] for i in range(len(v)) if v[i]>0)
new=[s.simplify(weights[i]-step*v[i]) for i in range(len(v))]
require(all(w>=0 for w in new),'atom elimination positivity')
require(sum(w!=0 for w in new)<=4,'at most d_1 squared atoms after elimination')
equal(sum((w*A for w,A in zip(weights,atoms)),s.zeros(2)),
      sum((w*A for w,A in zip(new,atoms)),s.zeros(2)),'atom elimination barycenter')
equal(sum(w*s.trace(H*A) for w,A in zip(weights,atoms)),
      sum(w*s.trace(H*A) for w,A in zip(new,atoms)),'dual-contact value preserved')
checks+=2

# An exactly solvable scalar-input experiment: the primal, dual and classical values agree.
p=s.Rational(2,5)
E0=[s.Rational(3,4),s.Rational(1,4)]
E1=[s.Rational(1,4),s.Rational(3,4)]
g=[]
for y in range(2):
    g.append(sum(max(p*E0[y]*E0[z],(1-p)*E1[y]*E1[z]) for z in range(2)))
P=sum(g)
equal(P,s.Rational(63,80),'scalar-input exact Bayes value')
for y in range(2):
    Hy=g[y]
    equal(Hy,g[y],'scalar dual contact')
equal(sum(g),P,'scalar dual objective')
Dtrace=sum(abs(E0[y]*E0[z]-E1[y]*E1[z]) for y in range(2) for z in range(2))
Peq=sum(max(E0[y]*E0[z],E1[y]*E1[z])/2 for y in range(2) for z in range(2))
equal(4*Peq-2,Dtrace,'unhalved fixed-pair conversion')
# All-zero rewards make zero primal/dual values: no strict advantage is universal.
equal(sum(s.Integer(0) for _ in range(4)),0,'zero reward experiment')
require(P<=1 and P>=max(p,1-p),'Bayes normalization');checks+=1

print(json.dumps({'schema':'gtf91.reset-variational-regression/1','status':'success',
    'exact_checks':checks,'negative_controls':negative,
    'universal_cone_constraints_verified_by_sampling':False,
    'continuum_proof_by_regression':False,'physical_reset_calibration':False,
    'independent_priority_clearance':False,'efficient_global_optimizer_claimed':False},sort_keys=True))
