"""Rational interval certificate for the explicit four-impact winding orbit."""
from fractions import Fraction as F
from math import factorial,isqrt
import json
class I:
 def __init__(self,a,b=None): self.lo=F(a);self.hi=F(a if b is None else b)
 def __add__(self,o):
  o=asI(o);return I(self.lo+o.lo,self.hi+o.hi)
 __radd__=__add__
 def __neg__(self):return I(-self.hi,-self.lo)
 def __sub__(self,o):return self+-asI(o)
 def __rsub__(self,o):return asI(o)+-self
 def __mul__(self,o):
  o=asI(o);v=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi];return I(min(v),max(v))
 __rmul__=__mul__
 def __truediv__(self,o):
  o=asI(o)
  if o.lo<=0<=o.hi:raise ValueError('division through zero')
  return self*I(1/o.hi,1/o.lo)
 def __rtruediv__(self,o):return asI(o)/self
 def __repr__(self):return str([float(self.lo),float(self.hi)])
def asI(x):return x if isinstance(x,I) else I(x)
def sq(x):
 x=asI(x)
 return I(0 if x.lo<=0<=x.hi else min(x.lo*x.lo,x.hi*x.hi),max(x.lo*x.lo,x.hi*x.hi))
def root_bounds(x):
 x=F(x)
 if x<0:raise ValueError('negative radicand')
 den=10**22;k=isqrt(x.numerator*den*den//x.denominator)
 return I(F(k,den),F(k+1,den))
def sqrt(x):
 x=asI(x);return I(root_bounds(x.lo).lo,root_bounds(x.hi).hi)
def trig(x,cos=False):
 x=asI(x);m=(x.lo+x.hi)/2;rad=(x.hi-x.lo)/2
 terms=12
 z=sum((-1)**k*m**(2*k if cos else 2*k+1)/factorial(2*k if cos else 2*k+1) for k in range(terms+1))
 deg=2*terms if cos else 2*terms+1
 rem=abs(m)**(deg+1)/factorial(deg+1)+rad
 return I(z-rem,z+rem)
def sin(x):return trig(x)
def cos(x):return trig(x,True)
rt3=sqrt(3)
def fun(r,t):return 2*r*sin(t)-sin(t)*cos(t)+rt3/2*cos(2*t)
def deriv(r,t):return 2*r*cos(t)-cos(2*t)-rt3*sin(2*t)
def bracket(r):
 a,b=F(9,10),F(1)
 if not(fun(I(r),I(a)).lo>0 and fun(I(r),I(b)).hi<0):raise ValueError('no bracket')
 while b-a>F(1,10**10):
  m=(a+b)/2;v=fun(I(r),I(m))
  if v.lo>0:a=m
  elif v.hi<0:b=m
  else:raise ValueError('ambiguous root sign')
 return a,b

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def vecminus(a,b):return [x-y for x,y in zip(a,b)]
def lat(i,j):return [I(F(i)+F(j,2)),j*rt3/2]
def midpoint(v):return [(x.lo+x.hi)/2 for x in v]
def error(v):return sqrt(sum(sq(I(-(x.hi-x.lo)/2,(x.hi-x.lo)/2)) for x in v)).hi

def clearance(q0,q1,p):
 a,b,c=midpoint(q0),midpoint(q1),midpoint(p)
 v=vecminus(b,a);w=vecminus(c,a);vv=dot(v,v);wv=dot(w,v)
 s=max(F(0),min(F(1),wv/vv));d=vecminus(w,[s*x for x in v]);nom=root_bounds(dot(d,d)).lo
 return nom-max(error(q0),error(q1))-error(p)

def run():
 
 if deriv(I(F(9,20),F(47,100)),I(F(9,10),1)).hi>=0:raise ValueError('global uniqueness')
 rows=[];clear_min=F(1);dmax=F(-100);incmin=F(1)
 for k in range(32):
  lo=F(9,20)+F(k,1600);hi=lo+F(1,1600);r=I(lo,hi)
  ta=bracket(lo)[0];tb=bracket(hi)[1];th=I(ta,tb)
  if ta<=F(92,100) or tb>=F(967,1000):raise ValueError('angle envelope')
  dv=deriv(r,th)
  if dv.hi>=-F(1,2):raise ValueError('monotonicity margin')
  dmax=max(dmax,dv.hi);c,s=cos(th),sin(th)
  if c.lo<=F(1,2):raise ValueError('incidence')
  incmin=min(incmin,c.lo)
  d=2*r*c-F(1,2);h=rt3/2-2*r*s
  if d.lo<=0 or h.lo<=0:raise ValueError('wrong diagonal branch')
  q=[[r*c,-r*s],[1-r*c,-r*s],[F(1,2)+r*c,-rt3/2+r*s],[F(3,2)-r*c,-rt3/2+r*s],[1+r*c,-r*s]]
  cc=[(0,0),(1,0),(1,-1),(2,-1),(1,0)];margin=F(10)
  for j in range(4):
   for aa in range(-4,5):
    for bb in range(-4,5):
     if (aa,bb) in [cc[j],cc[j+1]]:continue
     lower=clearance(q[j],q[j+1],lat(aa,bb))-hi
     margin=min(margin,lower)
  if margin<=F(1,200):raise ValueError('clearance failed '+str(float(margin)))
  # Every endpoint has norm <3; a center outside the finite index box
  # has norm >=sqrt(3)*5/2, leaving more than 0.8 after the radius.
  for v in q:
   if sqrt(sum(sq(x) for x in v)).hi>=3:raise ValueError('outer enumeration bound')
  clear_min=min(clear_min,margin)
  rows.append({'radius':[str(lo),str(hi)],'theta':[str(ta),str(tb)]})
 return {'schema':'a2-dyn-rational-winding-1','status':'passed','slabs':rows,'min_clearance_lower':str(clear_min),'min_incidence_lower':str(incmin),'phase_derivative_upper':str(dmax),'bounds_decimal_display':{'clearance':float(clear_min),'incidence':float(incmin),'derivative':float(dmax)},'arithmetic':'exact fractions; square roots enclosed by integer square roots; Taylor remainders explicit','scope':'existence, uniqueness in printed theta bracket, reflection, and clearance of the explicit four-impact orbit; not UNI or the LLT'}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
