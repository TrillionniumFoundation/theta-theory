#!/usr/bin/env python3
"""Exact regression for the projective score divisor; not formal verification."""
from pathlib import Path
import json
import sympy as s
ROOT = Path(__file__).resolve().parents[1]
x,y,t,u,c,e=s.symbols('x y t u c e')
checks={};cases=[]
for r in range(2,7):
 for variant in range(2):
  mult=[1+(i%2)*variant for i in range(r)]; n=sum(mult)
  al=[s.Integer(i*i+i-2) for i in range(r)]
  beta=[al[-1]+j+1 for j in range(r-1)]
  D=s.prod(t-a for a in al);Q=s.prod(t-b for b in beta)
  sig=[s.cancel(Q.subs(t,a)/s.diff(D,t).subs(t,a)) for a in al]
  L=[a*x+y for a in al];Dh=s.prod(L)
  Di=[s.prod(L[j] for j in range(r) if j!=i) for i in range(r)]
  Qh=s.expand(sum(z*d for z,d in zip(sig,Di)))
  ex=s.expand(Qh*sum((n-m)*a*d for m,a,d in zip(mult,al,Di))-n*Dh*s.diff(Qh,x))
  ey=s.expand(Qh*sum((n-m)*d for m,d in zip(mult,Di))-n*Dh*s.diff(Qh,y))
  G=s.cancel(ey/x)
  F=s.expand(n*D*s.diff(Q,t)-Q*sum((n-m)*s.prod(t-b for j,b in enumerate(al) if j!=i) for i,m in enumerate(mult)))
  local={'horizontal_form':s.expand(x*ex+y*ey)==0,
         'binary_division':s.expand(ex+y*G)==0 and s.Poly(G,x,y).total_degree()==2*r-3,
         'affine_sign':s.expand(G.subs({x:1,y:-t})+F)==0,
         'spectral_numerator':s.expand(Qh.subs({x:1,y:-t})-(-1)**(r-1)*Q)==0,
         'pole_coprimality':s.gcd(F,s.expand(D*Q))==1}
  # Compare the eliminated rational score in the chart K0=A-uB.
  k=[1-u*a for a in al];U=s.cancel(sum(z/k0 for z,k0 in zip(sig,k)))
  elim=s.cancel(sum(m*a/k0 for m,a,k0 in zip(mult,al,k))-n*s.diff(U,u)/U)
  expected=s.cancel(G.subs({x:-u,y:1})/(Dh*Qh).subs({x:-u,y:1}))
  local['infinity_chart_score']=s.cancel(elim-expected)==0
  cases.append({'r':r,'multiplicities':mult,'checks':{a:bool(b) for a,b in local.items()}})
  checks[f'r{r}-v{variant}']=all(bool(v) for v in local.values())
# The entire fixed-pencil family admits a monic chart at T != 0 (c is a unit).
F=-(6*c+4)*t*t+2*c
f=-(6*c+4)*u+2*c*u**3
g=s.expand(f/(2*c));a=(3*c+2)/c
T=s.Matrix([[0,0,0],[1,0,a],[0,1,0]])
H=s.Matrix(3,3,lambda i,j:s.trace(T**(i+j)))
checks['monic_companion_relation']=s.simplify(T**3-a*T)==s.zeros(3)
checks['trace_discriminant']=s.factor(H.det()-4*a**3)==0
checks['binary_cubic_discriminant']=s.factor(s.discriminant(f,u)-64*c*(3*c+2)**3)==0
checks['binary_trace_unit_factor']=s.factor(s.discriminant(f,u)-16*c**4*H.det())==0
checks['triple_special_fibre']=s.expand(g.subs(c,-s.Rational(2,3)))==u**3
checks['nonreduced_ramification']=s.diff(g,u).subs(c,-s.Rational(2,3))==3*u**2
checks['real_simple_projective_fibre']=s.Poly(g.subs(c,1),u).count_roots(-s.oo,s.oo)==3 and s.discriminant(g.subs(c,1),u)!=0
# Direct Hessian Schur-factor identity in the original radial/directional chart.
lam=s.symbols('lam');al=[-1,0,1];sig=[(1+c)/2,-c,(1+c)/2]
U=s.cancel(sum(z/(1-u*b) for b,z in zip(al,sig)))
rad=-3/lam+U/lam**2
tan=s.cancel(sum(b/(1-u*b) for b in al)-s.diff(U,u)/lam)
ell=s.cancel(tan.subs(lam,U/3));v=s.cancel(ell/g)
checks['eliminated_score_unit_factor']=s.factor(v)==-2*c/((u-1)*(u+1)*(c*u*u+1))
checks['full_radial_score']=s.cancel(rad.subs(lam,U/3))==0
Hrr=s.cancel(s.diff(rad,lam).subs(lam,U/3))
Hrt=s.cancel(s.diff(rad,u).subs(lam,U/3))
Htt=s.cancel(s.diff(tan,u).subs(lam,U/3))
checks['hessian_schur_derivative']=s.cancel(Htt-Hrt**2/Hrr-s.diff(ell,u))==0
checks['hessian_ramification_ideal']=s.cancel((s.diff(ell,u)-v*s.diff(g,u))/g-s.diff(v,u))==0
checks['triple_reconstructed_point']=U.subs(u,0)/3==s.Rational(1,3)
# Nonreduced base change at the triple collision: epsilon^2=0.
trunc=lambda z:s.expand(z.subs(e,0)+e*s.diff(z,e).subs(e,0))
aeps=trunc(a.subs(c,-s.Rational(2,3)+e))
Teps=s.Matrix([[0,0,0],[1,0,aeps],[0,1,0]])
checks['dual_number_collision_flat_basis']=(Teps**3-aeps*Teps).applyfunc(trunc)==s.zeros(3)
Heps=s.Matrix(3,3,lambda i,j:trunc(s.trace(Teps**(i+j))))
checks['trace_pairing_base_change']=Heps==(H.subs(c,-s.Rational(2,3)+e)).applyfunc(trunc)
checks['trace_discriminant_nonreduced_base_change']=trunc(Heps.det())==trunc(H.det().subs(c,-s.Rational(2,3)+e))
out={'revision':144,'ok':all(checks.values()),'arithmetic':'exact rational polynomial identities, companion traces, Sturm count, and dual-number base change',
     'binary_configurations':len(cases),'checks':checks,'cases':cases,
     'scope':'Regression evidence for written scheme-theoretic proofs, not formal proof or priority certification.'}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION144_PROJECTIVE_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
if not out['ok']:raise SystemExit('v144 projective exact regression failed')
