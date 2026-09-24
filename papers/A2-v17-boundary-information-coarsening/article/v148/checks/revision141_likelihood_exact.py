#!/usr/bin/env python3
"""Exact finite audits for the separated-root proof; no floating-point roots."""
from pathlib import Path
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
t=s.symbols('t')
checks={};cases=[];sturm_cases=0;score_cases=0
for r in range(2,11):
 for variant in range(6):
  alpha=[s.Rational(3*i*i+2*i-7,variant+1) for i in range(r)]
  if variant%3==0: mult=[1]*r
  elif variant%3==1: mult=[i+1 for i in range(r)]
  else: mult=[(i+1)**2+1 for i in range(r)]
  n=sum(mult)
  beta=[alpha[-1]+s.Rational((j+1)*(j+2),variant+2) for j in range(r-1)]
  D=s.Poly(s.prod(t-a for a in alpha),t,domain=s.QQ)
  Q=s.Poly(s.prod(t-b for b in beta),t,domain=s.QQ)
  H=sum((n-m)*D.exquo(s.Poly(t-a,t)).as_expr() for a,m in zip(alpha,mult))
  F=s.Poly(n*D.as_expr()*Q.diff().as_expr()-H*Q.as_expr(),t,domain=s.QQ)
  sigma=[Q.eval(a)/D.diff().eval(a) for a in alpha]
  local={
   'degree':F.degree()==2*r-3,
   'simple':s.gcd(F,F.diff()).degree()==0,
   'no_denominator_roots':s.gcd(F,D*Q).degree()==0,
   'residue_sum':sum(sigma)==1,
   'first_residue_moment':sum(a*u for a,u in zip(alpha,sigma))==sum(alpha)-sum(beta),
   'omitted_chart_obstruction':sum((n-m)*a for a,m in zip(alpha,mult))<n*sum(beta),
   'leading_coefficient':F.LC()==n*sum(beta)-sum((n-m)*a for a,m in zip(alpha,mult)),
  }
  intervals=list(zip(alpha,alpha[1:]))+list(zip(beta,beta[1:]))
  local['separated_sign_changes']=all(F.eval(a)*F.eval(b)<0 for a,b in intervals)
  local['interval_count']=len(intervals)==2*r-3
  divisors=[D.exquo(s.Poly(t-a,t,domain=s.QQ)) for a in alpha]
  zero=s.Poly(0,t,domain=s.QQ)
  local['partial_fractions']=(Q-sum((u*di for u,di in zip(sigma,divisors)),zero)).is_zero
  counts=[]
  if r<=5:
   counts=[int(F.count_roots(a,b)) for a,b in intervals]
   local['independent_sturm_counts']=counts==[1]*(2*r-3)
   sturm_cases+=1
  # Independently form the original x,y score numerators over the common
  # denominator D^2, after x=-Q/(nD), y=-t*x. Avoid expression swell.
  L=sum((m*di for m,di in zip(mult,divisors)),zero)
  LA=sum((m*a*di for m,a,di in zip(mult,alpha,divisors)),zero)
  J=sum((u*di**2 for u,di in zip(sigma,divisors)),zero)
  JA=sum((u*a*di**2 for u,a,di in zip(sigma,alpha,divisors)),zero)
  NY=n*J-Q*L; NX=n*JA-Q*LA
  local['original_score_radial_equation']=(NX-s.Poly(t,t)*NY).is_zero
  local['original_score_eliminated_equation']=(NY+F).is_zero
  score_cases+=1
  local={key:bool(value) for key,value in local.items()}
  name=f'r{r}-variant{variant}'
  checks[name]=all(local.values())
  cases.append({'r':r,'multiplicities':mult,'alpha':list(map(str,alpha)),
   'beta':list(map(str,beta)),'grouped_data':list(map(str,sigma)),
   'checks':local,'sturm_interval_counts':counts})
D=(t-1)*(t-2)*(t-3);Q=(t-4)*(t-5)
F=s.expand(3*D*s.diff(Q,t)-2*s.diff(D,t)*Q)
checks['displayed_cubic']=F==15*t**3-130*t**2+345*t-278
checks['displayed_data']=[s.cancel(Q/s.prod(t-a for a in [1,2,3] if a!=b)).subs(t,b) for b in [1,2,3]]==[6,-6,1]
out={'revision':141,'audit':'real reciprocal likelihood','ok':all(checks.values()),
 'arithmetic':'exact rational polynomial arithmetic; Sturm audits where recorded',
 'configurations':len(cases),'sturm_configurations':sturm_cases,
 'original_score_configurations':score_cases,'checks':checks,'cases':cases,
 'scope':'Finite audits of the written all-rank proof, not a formal proof certificate; unrestricted real data, not positive-definite data.'}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION141_LIKELIHOOD_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
if not out['ok']:raise SystemExit('likelihood exact audit failed')
