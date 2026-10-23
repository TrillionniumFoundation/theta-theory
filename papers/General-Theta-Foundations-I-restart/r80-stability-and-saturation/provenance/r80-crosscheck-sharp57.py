import json
import sympy as S
b,r,s,g,d,budget=S.symbols('beta r s gamma delta budget', real=True)
q=1-b
n0=s+(1-s)*d+(1-r)*g
d0=r*s+r*(1-s)*d+s*(1-r)*g
n1=b*(1-s)+q*(1-s)*d+r+q*(1-r)*g
d1=b*(1-s)*(b+q*r+q*(1-r)*(d+g))
poly=b*q*s**2*(1-r)**2*g**2+2*b*q*s*r*(1-s)*(1-r)*g*d+b*(1-r)*(b**2*(r-s)+s**2*(b+2*q*r))*g+b*q*r**2*(1-s)**2*d**2+b*s*r*(1-s)*(b+2*q*r)*d+b*s**2*r*(b+q*r)
checks={}
def test(name,expr):
    res=S.factor(expr)
    if res != 0:
        raise RuntimeError(name+': '+str(res))
    checks[name]=True
test('positive_polynomial',n1*b*(b*n0+q*d0)-d1*(b*n0+d0)-poly)
gmin=(s+(1-s)*d)*(1-budget*r)/((1-r)*(budget*s-1))
oppn=b+q*s+q*(1-s)*d+q*(1-r)*g
oppd=b*(1-r)*(b+q*s+q*(1-s)*(d+g))
F=S.factor((oppn/oppd).subs(g,gmin))
derivatives={
'delta':str(S.factor(S.diff(F,d))),
'r_delta0':str(S.factor(S.diff(F.subs(d,0),r))),
's_r_delta0':str(S.factor(S.diff(F.subs({d:0,r:0}),s))) }
endpoint=S.factor(F.subs({d:0,r:0,s:2/budget}))
claimed=(b+4*q/budget)/(b*(b+4*q/budget-4*q/budget**2))
test('opposite_orientation_minimum', endpoint-claimed)
r0=(S.sqrt(65)-1)/32
beta=S.Rational(1,4);D=beta+(1-beta)*r0
f=(b+r)/(b*(b+q*r))
expr=n1/d1
for var,claim in [(r,b/(b+q*r)**2),(s,r/(b*(b+q*r))),(d,q*r**2/(b*(b+q*r)**2))]:
    test('derivative_'+str(var),S.diff(expr,var).subs({s:0,g:0,d:0})-claim)
A=1/r0**2;FF=beta/D**2;LL=(1-beta)*r0**2/(beta*D**2)
c0=2*S.sqrt(1-beta)*r0**2/(D**2+beta*r0**2)
test('c0_algebraic',4*FF*A*LL/(A+FF)**2-c0**2)
print(json.dumps({'scope':'Independent author-team exact symbolic identities, not proof of all quantified sign conditions or external review', 'status':'PASS','identities':checks,'opposite_derivatives':derivatives,'c0_numeric_diagnostic':str(S.N(c0,16))},indent=2,sort_keys=True))
