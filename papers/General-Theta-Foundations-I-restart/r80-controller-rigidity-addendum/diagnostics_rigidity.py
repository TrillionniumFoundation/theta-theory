#!/usr/bin/env python3
"""Exact finite/symbolic diagnostics; not a replacement for the written theorem."""
import json
import sympy as s
checks=0

def check(condition, name):
    global checks
    if not condition:
        raise RuntimeError(name)
    checks+=1

def zero(expr, name):
    check(s.factor(expr)==0, name)

r,x,beta=s.symbols('r x beta', positive=True)
q=1-beta
rr,ss,alpha,gamma,xi,delta=s.symbols('rr ss alpha gamma xi delta')
U=beta*(1-rr); W=beta*(1-ss)
a=rr*alpha+q*(1-rr)*gamma; b=ss*xi+q*(1-ss)*delta
cost=(W+a+b)/(U*W+U*b+W*a)
base={rr:r,ss:0,alpha:1,gamma:0,delta:0}
D=beta+q*r
F=beta/D**2; L=q*r**2/(beta*D**2)
S=r/(beta*D); Z=r**2/D**2; T=r**2/(beta*D**2)
for variable,expected in [(rr,F),(ss,S+T*xi),(delta,L),(alpha,-Z)]:
    zero(s.diff(cost,variable).subs(base)-expected,'model1 derivative '+str(variable))
zero(S-L-r/D**2,'strict success-activation penalty')
H,u,v,G,A0=s.symbols('H u v G A0')
sub={rr:r+x*H,ss:x*u,delta:x*v,gamma:x*x*G,alpha:1-x*A0}
y=s.cancel(cost.subs(sub, simultaneous=True))
zero(s.diff(y,x).subs(x,0)-(F*H+S*u+L*v+Z*A0+T*xi*u),'full model1 first-order expansion')
h1=(1-x*x)*(r+x*H); h2=(1-x*x)*x*u
p1=x*x*(r+x*H)*(1-x*A0)+(1-r-x*H)*x*x*G
p2=x*x*x*u*xi+(1-x*u)*x*v
den=h1*h2+h1*p2+h2*p1
trap=s.cancel((h1-h2)*p1/(h1*den*x))
zero(trap.subs(x,0)-(1+(1-r)*G/r)/(u+v),'full model0 trap coefficient')
zero(s.diff(1/h1,x).subs(x,0)+H/r**2,'initial-row coefficient')
AA,FF,LL,tt,HH=s.symbols('AA FF LL tt HH', positive=True)
XX=-AA*HH+1/tt; YY=FF*HH+LL*tt
zero((FF*XX+AA*YY)/(AA+FF)-(FF/tt+AA*LL*tt)/(AA+FF),'weighted cancellation')
kk=s.sqrt(FF/(AA*LL)); hh=(1/kk-LL*kk)/(AA+FF)
cc=2*s.sqrt(FF*AA*LL)/(AA+FF)
zero((-AA*hh+1/kk)-cc,'balanced model0 coefficient')
zero((FF*hh+LL*kk)-cc,'balanced model1 coefficient')
r0=(s.sqrt(65)-1)/32
zero(r0*r0+s.Rational(1,16)*r0-s.Rational(1,16),'baseline root')
check(r0.is_positive is True and (1-r0).is_positive is True,'exact interior row')
print(json.dumps({'status':'PASS','exact_checks':checks,'floating_checks':0,
 'scope':'Exact algebraic derivative/limit identities and finite constant checks, not a universal proof certificate.'},sort_keys=True))
