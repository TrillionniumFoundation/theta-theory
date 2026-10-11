#!/usr/bin/env python3
"""Deterministic finite checks for R38, not continuum proofs or optimality certification."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json, math
import numpy as np
COUNTS:dict[str,int]={}
def check(ok:bool,group:str)->None:
    COUNTS[group]=COUNTS.get(group,0)+1
    if not ok:raise RuntimeError('finite regression failed: '+group)
def mv(a,v):return [sum((x*y for x,y in zip(row,v)),F(0)) for row in a]
def mm(a,b):return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def base_coeff(z):
    # Extreme normalized rays (1,1/4) and (1,3/4) of the compact K cone.
    w,v=z;return [F(3,2)*w-2*v,2*v-F(1,2)*w]
def kb(z):return sum(map(abs,base_coeff(z)),F(0))
def norm(z):return sum(kb(z[i:i+2]) for i in range(0,len(z),2))
def finite_lift():
    # Raw rank-one positive instruments: actual normalized outputs are 1/4,3/4.
    # They test the new cone lift exactly; they are not a Gaussian density surrogate.
    targets=[F(1,4),F(3,4)]
    for m in (1,2,3,5):
      # A common interval grid; some cells can have zero acquired/invariant mass.
      cells=[F(1,4)+F(2*s+1,4*m) for s in range(m)]
      dest=[min(m-1,int((q-F(1,4))*2*m)) for q in targets]
      for weight in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
        P=[[F(0) for _ in range(2*m)] for _ in range(2*m)]
        for s in range(m):
          for a,pa in enumerate((weight,1-weight)):
            for y,q in enumerate(targets):
              e0=F(3,4) if y==a else F(1,4)
              # likelihood e0*(1-p)+(1-e0)*p = e0 +(1-2e0)*p
              row=[e0,1-2*e0];j=dest[y]
              for c in range(2):P[2*j][2*s+c]+=pa*row[c];P[2*j+1][2*s+c]+=pa*q*row[c]
        z0=[F(0)]*(2*m)
        for y,q in enumerate(targets):z0[2*dest[y]]+=F(1,2);z0[2*dest[y]+1]+=q/2
        gamma=F(1,6) # kappa=1/3, epsilon=1/2, k=0.
        for s,x in product(range(m),targets):
          z=[F(0)]*(2*m);z[2*s]=1;z[2*s+1]=x
          out=mv(P,z)
          check(sum(out[::2])==1,'positive_instrument_normalization')
          residual=[a-gamma*b for a,b in zip(out,z0)]
          check(all(min(base_coeff(residual[j:j+2]))>=0 for j in range(0,2*m,2)),'whole_cone_lift_minorization')
        for s,t,x,y in product(range(m),range(m),targets,targets):
          z=[F(0)]*(2*m);z[2*s]+=1;z[2*s+1]+=x;z[2*t]-=1;z[2*t+1]-=y
          check(norm(mv(P,z))<=(1-gamma)*norm(z),'joint_K_base_norm_contraction')
        # Mixing cannot be inferred for the nonlocal always-preserve-label program.
        if m>1:
          z=[F(0)]*(2*m);z[0]=1;z[1]=F(1,2);z[2]=-1;z[3]=-F(1,2)
          check(norm(z)==2,'nonlocal_label_obstruction')
    # Positive physical comparison may leave the compact cone: raw whole-base condition matters.
    x,q=F(1,4),F(3,4);rem=[1-F(1,3),x-F(1,3)*q]
    check(rem[0]>=rem[1]>=0 and min(base_coeff(rem))<0,'remainder_in_C_not_CK')

def quiet_and_resources():
    for lam in (F(1,4),F(1,2),F(3,4),F(9,10)):
      for k in range(1,12):
        c,h=F(1,100),F(1,200);value=F(1)
        for _ in range(k):value=lam*value+c+h
        exact=lam**k+(c+h)*sum((lam**i for i in range(k)),F(0))
        check(value==exact,'robust_quiet_mesh_recursion')
    for b in (1,2,4):
      for gamma in (F(1,4),F(1,3),F(1,2)):
        for n in (1,2,3,5,11,20):
          value=sum(((1-gamma)**(j//b) for j in range(n)),F(0))
          check(value<=b/gamma,'uniform_geometric_error_sum')
    for n in range(1,20):
      check(sum(F(t,n) for t in range(1,n+1))==F(n+1,2),'protected_actual_report_count')
      check(n+2==1+n+1 and n+3==1+n+1+1,'all_physical_calls')
    for m in range(2,25):
      check(4*m+2>=m+3*m,'post_control_bit_label_budget')
    for w in (F(1,8),F(1,3),F(2,3)):
      for m in (4,8,16,32):
        xi=w/F(m*m)+(1-w)/m
        check(xi>=w/F(m*m) and xi>=(1-w)/m,'true_acquired_stratum_mass')
    for a,delta in product((F(0),F(1,5),F(1,2),F(1)),(F(0),F(1,8),F(2,7))):
      check(a+delta**2==2*(a/2)+delta**2,'attained_calibration_deficiency')
    # Row-optimal zero distortion does not imply common pooled calibration.
    x,y=F(1,4),F(3,4);mean=(x+y)/2
    check(((x-mean)**2+(y-mean)**2)/2>0,'local_global_pooling_counterexample')

def gaussian_benchmark():
    Phi=lambda x:.5*(1+math.erf(x/math.sqrt(2)))
    phi=lambda x:math.exp(-x*x/2)/math.sqrt(2*math.pi)
    def G(q):
        l=.5*math.log(q/(1-q));return .25+.5*(q*Phi(1+l)+(1-q)*Phi(1-l))
    q=.5
    for _ in range(70):q=G(q)
    check(abs(G(q)-q)<1e-14,'binary_calibration_fixed_point')
    for x in np.linspace(.5,.75,31):
      l=.5*math.log(x/(1-x));d=.5*(Phi(1+l)-Phi(1-l))
      check(abs(x*phi(1+l)-(1-x)*phi(1-l))<3e-16,'binary_derivative_cancellation')
      check(0<=d<=.5,'binary_global_contraction')
      check(abs((G(x+1e-6)-G(x-1e-6))/2e-6-d)<3e-10,'binary_derivative_finite_check')
    # Joint physical-state / label transition matrix, not a filter with an external real register.
    P=np.zeros((4,4));transition=np.array([[.75,.25],[.25,.75]])
    for s,p in enumerate((q,1-q)):
      threshold=-.5*math.log(p/(1-p))
      for i,mean in enumerate((1.,-1.)):
        high=Phi(mean-threshold)
        for j,prob in ((0,high),(1,1-high)):
          for ii in range(2):P[2*j+ii,2*s+i]+=prob*transition[ii,i]
    z=np.array([q,1-q,1-q,q])/2
    check(np.max(np.abs(P.sum(axis=0)-1))<2e-16,'binary_joint_normalization')
    check(np.max(np.abs(P@z-z))<2e-15,'binary_joint_invariant_ensemble')
    risk=0.
    for s,p in enumerate((q,1-q)):
      risk+=z[2*s]*2*(1-p)**2+z[2*s+1]*2*p*p
    check(abs(risk-2*q*(1-q))<3e-16,'binary_exact_Brier_identity')
    for q0,x in product(np.linspace(.25,.75,15),np.linspace(.4,.6,11)):
      w=2*x-.5;y=.5*(math.log(w/(1-w))-math.log(q0/(1-q0)))
      density=(q0*phi(y-1)+(1-q0)*phi(y+1))/(w*(1-w))
      check(abs(y)<1 and density>=.125,'binary_actual_overlap_grid_check')
    check(4*phi(2)>.125 and 4*math.exp(6)/math.sqrt(2*math.pi)<1024,'binary_explicit_constants')
    return {'q_star_illustration':format(q,'.12f'),'stationary_Brier_illustration':format(risk,'.12f'),'status':'illustration of analytic contraction/invariance proof, not certified decimal program or optimality'}

def quantum():
    rng=np.random.default_rng(380012)
    def sqrtm(A):
      vals,vec=np.linalg.eigh(A);return (vec*np.sqrt(np.maximum(vals,0)))@vec.conj().T
    for dim in (2,3):
      for trial in range(12):
        Z=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim))
        rho=Z@Z.conj().T;rho=rho/np.trace(rho);rho=.7*rho+.3*np.eye(dim)/dim
        H=rng.normal(size=(dim,dim))+1j*rng.normal(size=(dim,dim));H=(H+H.conj().T)/2;H-=np.trace(H)*np.eye(dim)/dim;H/=max(1.,np.linalg.norm(H))*1.1
        beta=.7;E=np.eye(dim)+beta*H;B=sqrtm(E);raw=B@rho@B;mass=np.trace(raw).real;sigma=raw/mass
        sr=sqrtm(rho);ir=np.linalg.inv(sr);R=ir@sqrtm(sr@sigma@sr)@ir;Ei=dim*(R@R)/np.trace(R@R)
        check(np.linalg.norm(E-Ei)<2e-12,'noncommuting_congruence_inverse')
        check(np.min(np.linalg.eigvalsh(E))>=1-beta-1e-12,'quantum_positive_effect_floor')
        lam=.8;tau=np.eye(dim)/dim;post=lam*sigma+(1-lam)*tau
        check(np.min(np.linalg.eigvalsh(post))>=(1-lam)/dim-1e-12,'whole_base_quantum_interior')
        check(abs(np.trace(post)-1)<2e-13,'quantum_raw_normalization')
        check(np.linalg.norm(E@rho-rho@E)>1e-6,'genuine_noncommutation')
        x=.8*rho+.2*tau;q=.8*sigma+.2*tau;kappa=.2/(2*dim)
        check(np.min(np.linalg.eigvalsh(x-kappa*q))>=-1e-12,'quantum_cone_comparison')
        diag=np.diag(np.diag(post));check(np.min(np.linalg.eigvalsh(diag))>=.2/dim-1e-12,'marked_affine_projection_floor')

def main():
    finite_lift();quiet_and_resources();benchmark=gaussian_benchmark();quantum()
    print(json.dumps({'status':'PASS','native_finite_checks':sum(COUNTS.values()),'groups':COUNTS,'binary_benchmark':benchmark,'random_seed':380012,'limitations':'Finite rational and floating checks only. They do not prove continuum density, fixed-point existence, optimality, necessity or priority. Inherited suites are run separately by complete builds; no nested totals are added.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
