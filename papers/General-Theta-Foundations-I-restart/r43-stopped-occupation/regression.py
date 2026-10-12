#!/usr/bin/env python3
"""Finite exact identities and deterministic numerical witnesses, not continuum proofs."""
from __future__ import annotations
import json,math,hashlib
from fractions import Fraction as F
import numpy as np
from verify import require
N=0;cases={}
def check(ok,msg,group):
 global N
 require(bool(ok),msg);N+=1;cases[group]=cases.get(group,0)+1
def invsolve(A,b):
 n=len(b);a=[list(A[i])+[b[i]] for i in range(n)]
 for j in range(n):
  k=next(k for k in range(j,n) if a[k][j]);a[j],a[k]=a[k],a[j]
  v=a[j][j];a[j]=[x/v for x in a[j]]
  for i in range(n):
   if i!=j:
    v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[j])]
 return [a[i][-1] for i in range(n)]
def mv(A,x):return [sum(a*b for a,b in zip(row,x)) for row in A]
def exact_lifts():
 for rho in (F(1,5),F(1,3),F(2,5)):
  T=[[1-rho,rho],[rho,1-rho]]
  for accuracy in (F(2,3),F(3,4),F(4,5)):
   report=[[accuracy,1-accuracy],[1-accuracy,accuracy]]
   for s in (F(1),F(1,2),F(1,5),F(1,17)):
    beta=1-s
    for mask in range(16):
     # Current report and previous label determine the next label.
     route=lambda label,y:(mask>>(2*label+y))&1
     A=[[F(0) for j in range(4)] for i in range(4)]
     B=[F(0) for i in range(4)]
     prep=[F(2,5),F(3,5)]
     for x in range(2):
      for y in range(2):
       for xp in range(2):
        B[2*y+xp]+=prep[x]*report[y][x]*T[xp][x]
        for l in range(2):A[2*route(l,y)+xp][2*l+x]+=report[y][x]*T[xp][x]
     z=invsolve([[(F(i==j)-beta*A[i][j]) for j in range(4)] for i in range(4)],[s*x for x in B])
     check(sum(z)==1 and min(z)>=0,'resolvent positive normalized','exact_resolvent')
     check(z==[s*b+beta*p for b,p in zip(B,mv(A,z))],'fixedpoint identity','exact_resolvent')
     w=[z[2*l]+z[2*l+1] for l in range(2)]
     q=[z[2*l+1]/w[l] if w[l] else F(1,2) for l in range(2)]
     # Reweighted predictive means in incoming row (l,y), before pooling.
     rowmeans=[];risk=F(0)
     for l in range(2):
      for y in range(2):
       v=[sum(report[y][x]*T[xp][x]*z[2*l+x] for x in range(2)) for xp in range(2)]
       mass=sum(v)
       if mass:rowmeans.append((mass,v[1]/mass,route(l,y)))
     # Pool first-injection and recurrent incoming ensembles by outgoing label.
     sums=[s*B[2*j+1] for j in range(2)];masses=[s*(B[2*j]+B[2*j+1]) for j in range(2)]
     for mass,u,j in rowmeans:sums[j]+=beta*mass*u;masses[j]+=beta*mass
     check(masses==w and sums==[z[1],z[3]],'actual pooled disintegration','exact_calibration')
     for j in range(2):
      risk+=z[2*j]*(q[j]**2)+z[2*j+1]*((1-q[j])**2)
     check(risk==sum(w[j]*q[j]*(1-q[j]) for j in range(2)),'conditional audit risk','exact_calibration')
     # Finite geometric truncation has genuine subprobability mass.
     finite=[F(0)]*4;term=B[:]
     for t in range(5):
      finite=[u+s*(beta**t)*v for u,v in zip(finite,term)];term=mv(A,term)
     check(sum(finite)==1-beta**5,'geometric acquisition mass','exact_stopping')
     check(sum(abs(a-b) for a,b in zip(z,finite))==beta**5,'positive resolvent remainder','exact_stopping')
def budgets():
 for M in range(2,180):
  check(1+(M-1)==M,'external initial label','integer_budgets')
  if M>=3:check(1+2*((M-1)//2)<=M,'internal halt labels','integer_budgets')
  if M>=7:check(3*((M-4)//3)+4<=M and (M-4)//3>=1,'bit lanes external','integer_budgets')
  if M>=10:check(6*((M-4)//6)+4<=M and (M-4)//6>=1,'bit lanes internal','integer_budgets')
 for s in (F(1),F(1,2),F(1,7),F(1,37)):
  b=1-s
  for H in range(1,40):
   count=sum(b**t for t in range(H))
   check(count==(1-b**H)/s and count<=min(F(H),1/s),'capped expected physical calls','exact_stopping')
 for a in (F(i,10) for i in range(11)):
  for guess in (F(i,10) for i in range(11)):
   check(a*(guess/2+(1-guess)/2)==a/2,'erasure deficiency all guessed probabilities','exact_composition')
  for readout in (F(i,10) for i in range(11)):
   check(a*(readout**2+(1-readout)**2)/2>=a/4,'bit Bayes lower','exact_composition')
def gaussian():
 Phi=lambda z:(1+math.erf(z/math.sqrt(2)))/2
 phi=lambda z:math.exp(-z*z/2)/math.sqrt(2*math.pi)
 def G(q):
  l=.5*math.log(q/(1-q));return .25+.5*(q*Phi(1+l)+(1-q)*Phi(1-l))
 for q in np.linspace(.5,.75,101):
  l=.5*math.log(q/(1-q))
  check(abs(q*phi(1+l)-(1-q)*phi(1-l))<2e-15,'Gaussian derivative cancellation','numerical_gaussian')
  der=.5*(Phi(1+l)-Phi(1-l))
  check(0<=der<=.5 and .5<=G(q)<=.75,'Gaussian invariant interval and derivative','numerical_gaussian')
 results=[]
 for s in (1.,.75,.5,.25,.1,.01,.001):
  q=.5;beta=1-s
  for it in range(60):q=s*G(.5)+beta*G(q)
  check(abs(q-(s*G(.5)+beta*G(q)))<2e-15,'Gaussian root residual','numerical_gaussian')
  risk=2*q*(1-q);check(0<risk<.5,'Gaussian risk range','numerical_gaussian')
  results.append({'s':s,'q':round(q,14),'core_risk':round(risk,14),'external_labels':3,'internal_labels':5})
 return results
def quantum():
 rng=np.random.default_rng(43012)
 def sqrtm(a):
  v,Q=np.linalg.eigh(a);return (Q*np.sqrt(np.maximum(v,0)))@Q.conj().T
 for d in (2,3,4):
  for k in range(12):
   A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));rho=A@A.conj().T+np.eye(d);rho/=np.trace(rho)
   A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));H=(A+A.conj().T)/2;H-=np.trace(H)*np.eye(d)/d;H/=max(1,np.linalg.norm(H))
   E=np.eye(d)+.3*H;K=sqrtm(E);sig=K@rho@K;sig/=np.trace(sig)
   R=sqrtm(rho);Ri=np.linalg.inv(R);B=Ri@sqrtm(R@sig@R)@Ri;recovered=d*(B@B)/np.trace(B@B)
   check(np.linalg.norm(recovered-E)<1e-10,'quantum inverse normalized congruence','numerical_quantum')
   lam=.65;out=lam*sig+(1-lam)*np.eye(d)/d
   check(np.linalg.eigvalsh(out).min()>=(1-lam)/d-1e-12,'quantum raw floor','numerical_quantum')
def stability_witness():
 def exp_upper(x):
  terms=[F(1)]
  for k in range(1,31):terms.append(terms[-1]*x/k)
  nxt=terms[-1]*x/31
  return sum(terms)+nxt/(1-x/32)
 normal_lower=sum(1/exp_upper((F(2)+F(j,16))**2/2) for j in range(1,17))/(16*F(251,100))
 check(normal_lower>F(19,1000),'rational Gaussian lower sum','exact_stability')
 lower=F(998,1000)*54*F(19,1000)/(1+F(8,10000))**3
 check(lower>F(102,100),'curvature exceeds 1.02','exact_stability')
 for u in (F(j,100) for j in range(101)):
  check(4*F(1,8)/(1+u)**3<=F(1,2),'positive reset curvature','exact_stability')
 for k in range(1,30):
  u=F(1,2**k);v=u
  for _ in range(k):v=2*v/(1+v)
  check(v>F(1,2),'same-report expansion witness','exact_stability')
exact_lifts();budgets();bench=gaussian();quantum();stability_witness()
result={'status':'PASS','native_checks':N,'check_groups':cases,'binary_gaussian_benchmark':bench,'limits':'Finite rational identities and deterministic numerical witnesses. Not continuum proofs, exhaustive control optimization, formal verification, priority or journal acceptance.'}
print(json.dumps(result,sort_keys=True,indent=2))
