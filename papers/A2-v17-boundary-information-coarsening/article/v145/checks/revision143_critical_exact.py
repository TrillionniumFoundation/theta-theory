#!/usr/bin/env python3
"""Exact regression of the new matrix-covariant critical algebra (not proof)."""
from pathlib import Path
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
t,x,y,e=s.symbols('t x y e')
checks={};cases=[]
def zero(M):return all(s.cancel(v)==0 for v in M)
for r in range(2,6):
 for variant in range(3):
  mult=([1]*r if variant==0 else [1+(i+variant)%2 for i in range(r)])
  n=sum(mult); al=[s.Rational(i*i+2*i-3,variant+1) for i in range(r)]
  be=[al[-1]+s.Rational(j*j+3*j+4,variant+2) for j in range(r-1)]
  c=s.Rational(2*variant+3,variant+2)
  D=s.Poly(s.prod(t-a for a in al),t);Q=s.Poly(c*s.prod(t-b for b in be),t)
  H=sum((n-m)*D.exquo(s.Poly(t-a,t)).as_expr() for a,m in zip(al,mult))
  F=s.Poly(n*D.as_expr()*Q.diff().as_expr()-H*Q.as_expr(),t)
  sigma=[Q.eval(a)/D.diff().eval(a) for a in al]
  a=c*(n*sum(be)-sum((n-m)*z for m,z in zip(mult,al)))
  local={'degree_and_leading':F.degree()==2*r-3 and F.LC()==a and a>0,
   'residue_mass':sum(sigma)==c,'residue_moment':sum(z*u for z,u in zip(al,sigma))==c*(sum(al)-sum(be)),
   'sturm_separated_intervals':all(F.count_roots(l,h)==1 for l,h in list(zip(al,al[1:]))+list(zip(be,be[1:])))}
  for label,R in [('D',D),('Q',Q),('Fprime',F.diff())]:
   inv=s.invert(R,F)
   local['bezout_unit_'+label]=(R*inv).rem(F).as_expr()==1
  G=s.eye(n)
  for i in range(n-1):G[i,i+1]=s.Rational(i+1,2)
  lam=[a for a,m in zip(al,mult) for _ in range(m)]
  A=G.T*G;B=G.T*s.diag(*lam)*G;C=A.inv()*B
  Ps=[]
  for i,ai in enumerate(al):
   P=s.eye(n)
   for j,aj in enumerate(al):
    if j!=i:P=P*(C-aj*s.eye(n))/(ai-aj)
   Ps.append(P)
  local['projector_resolution']=sum(Ps,s.zeros(n))==s.eye(n) and all(P*P==P and s.trace(P)==m and (A*P).T==A*P for P,m in zip(Ps,mult))
  section=lambda sig:A*sum((u*P/m for u,P,m in zip(sig,Ps,mult)),s.zeros(n))
  tau=lambda S:[s.trace(P*A.inv()*S) for P in Ps]
  S0=section(sigma)
  E=s.zeros(n);E[0,-1]=E[-1,0]=1
  E=E-section(tau(E));S=S0+E
  local['full_data_affine_fibre']=S0.T==S0 and tau(S)==sigma and tau(E)==[0]*r
  G2=s.eye(n);G2[0,-1]=2;G2[0,0]=3
  A2=G2.T*A*G2;B2=G2.T*B*G2;C2=A2.inv()*B2
  P2=[G2.inv()*P*G2 for P in Ps]
  S2=A2*sum((u*P/m for u,P,m in zip(sigma,P2,mult)),s.zeros(n))
  local['congruence_covariance']=C2==G2.inv()*C*G2 and S2==G2.T*S0*G2
  # Symbolic trace identity, evaluated via functional calculus; no eigenvectors.
  Kinv=sum((P/(z*x+y) for P,z in zip(Ps,al)),s.zeros(n))*A.inv()
  local['functional_inverse']=zero((x*B+y*A)*Kinv-s.eye(n))
  local['matrix_trace_likelihood']=s.cancel(s.trace(S*Kinv)-sum(u/(z*x+y) for u,z in zip(sigma,al)))==0
  checks[f'r{r}-v{variant}']=all(bool(v) for v in local.values())
  cases.append({'r':r,'n':n,'multiplicities':mult,'scale':str(c),'checks':{k:bool(v) for k,v in local.items()}})
# Nonreduced base change: a monic cubic algebra over Q[epsilon]/epsilon^2.
trunc=lambda v:s.expand(s.diff(v,e).subs(e,0)*e+v.subs(e,0))
mat_trunc=lambda M:M.applyfunc(trunc)
al=[s.Integer(1),s.Integer(2),3+e];be=[4+2*e,5-e];c=s.Rational(3,2)+e;n=3
D=s.prod(t-a for a in al);Q=c*s.prod(t-b for b in be)
F=s.expand(n*D*s.diff(Q,t)-2*s.diff(D,t)*Q)
a=s.Poly(F,t).LC();monic=s.Poly(F/a,t)
co=[trunc(v) for v in monic.all_coeffs()];k=monic.degree()
T=s.zeros(k)
for j in range(k-1):T[j+1,j]=1
for i in range(k):T[i,k-1]=-co[k-i]
def at_matrix(poly):
 p=s.Poly(poly,t);out=s.zeros(k)
 for coeff in p.all_coeffs():out=mat_trunc(out*T+trunc(coeff)*s.eye(k))
 return out
def inverse_dual(M):
 M0=M.subs(e,0);M1=M.diff(e).subs(e,0);I=M0.inv()
 out=I-e*I*M1*I
 assert mat_trunc(M*out)==s.eye(k)
 return out
checks['dual_number_monic_relation']=at_matrix(sum(co[i]*t**(k-i) for i in range(k+1)))==s.zeros(k)
DM=at_matrix(D);QM=at_matrix(Q);FP=at_matrix(s.diff(F,t))
for lab,M in [('D',DM),('Q',QM),('Fprime',FP)]:
 checks['dual_number_unit_'+lab]=mat_trunc(M*inverse_dual(M))==s.eye(k)
XM=mat_trunc(-QM*inverse_dual(DM)/n);YM=mat_trunc(-T*XM)
sig=[trunc(Q.subs(t,z)/s.diff(D,t).subs(t,z)) for z in al]
scorex=s.zeros(k);scorey=s.zeros(k)
for z,u in zip(al,sig):
 inv=inverse_dual(mat_trunc(z*XM+YM));term=mat_trunc(-inv+u*inv*inv)
 scorex=mat_trunc(scorex+z*term);scorey=mat_trunc(scorey+term)
checks['dual_number_original_score_equations']=scorex==s.zeros(k) and scorey==s.zeros(k)
out={'revision':143,'ok':all(checks.values()),'arithmetic':'exact rational matrices, polynomial Bezout identities, Sturm counts, and Q[epsilon]/epsilon^2',
 'matrix_configurations':len(cases),'checks':checks,'cases':cases,
 'scope':'Finite regression checks of the written proofs; not formal proof or historical priority certification.'}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION143_CRITICAL_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
if not out['ok']:raise SystemExit('v143 exact critical regression failed')
