#!/usr/bin/env python3
"""Finite rational enclosures supporting the analytical period-family proof.

Decimal Newton iterates are candidates only. Rounded integer interval arithmetic
and the printed global strong-convexity constant certify the minimum enclosures.
The infinite-family monotonicity and joint phase theorem are proved in the text,
not by these 18 finite samples. No dependencies outside the standard library.
"""
from __future__ import annotations
from decimal import Decimal, localcontext
from fractions import Fraction
from math import isqrt
import json

D=Decimal
S=10**75

class Iv:
    def __init__(self, lo: int, hi: int | None=None):
        self.lo=lo; self.hi=lo if hi is None else hi
        if self.lo>self.hi: raise ValueError('reversed interval')
    @staticmethod
    def point(x):
        if isinstance(x,Iv): return x
        q=Fraction(x); p=q.numerator*S; d=q.denominator
        return Iv(p//d,-((-p)//d))
    def __add__(self,b):
        b=Iv.point(b);return Iv(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self):return Iv(-self.hi,-self.lo)
    def __sub__(self,b):return self+-Iv.point(b)
    def __rsub__(self,b):return Iv.point(b)+-self
    def __mul__(self,b):
        b=Iv.point(b);v=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi]
        return Iv(min(v)//S,-((-max(v))//S))
    __rmul__=__mul__
    def reciprocal(self):
        if self.lo<=0<=self.hi:raise ZeroDivisionError('interval contains zero')
        if self.hi<0:return -(-self).reciprocal()
        return Iv(S*S//self.hi,-((-S*S)//self.lo))
    def __truediv__(self,b):return self*Iv.point(b).reciprocal()
    def __rtruediv__(self,b):return Iv.point(b)*self.reciprocal()
    def sqrt(self):
        if self.lo<0:raise ValueError('negative sqrt lower endpoint')
        a=isqrt(self.lo*S); b=isqrt(self.hi*S)
        if b*b<self.hi*S:b+=1
        return Iv(a,b)
    def square(self):
        if self.lo>=0:return self*self
        if self.hi<=0:return (-self)*(-self)
        return Iv(0,-((-max(self.lo*self.lo,self.hi*self.hi))//S))
    def maxabs(self):return Fraction(max(abs(self.lo),abs(self.hi)),S)
    def lower(self):return Fraction(self.lo,S)
    def upper(self):return Fraction(self.hi,S)
    def output(self):return {'lower_numerator':str(self.lo),'upper_numerator':str(self.hi),'denominator_power_10':75}


def segment(R,y,z=None):
    """Value, gradient and Hessian for an end segment or an interior segment."""
    root=D(3).sqrt();d=D('0.5')-R
    x=(R*R-y*y).sqrt();x2=R*R/(x*x*x)
    if z is None:
        h=root/2-x;v=d+y;hp=[y/x];vp=[D(1)];hpp=[x2]
    else:
        w=(R*R-z*z).sqrt();h=root-x-w;v=z-y
        hp=[y/x,z/w];vp=[D(-1),D(1)];hpp=[x2,R*R/(w*w*w)]
    val=(h*h+v*v).sqrt();q=[h*a+v*b for a,b in zip(hp,vp)]
    grad=[qj/val for qj in q]
    hes=[[ (hp[i]*hp[j]+vp[i]*vp[j])/val-q[i]*q[j]/(val**3)
           +(h*hpp[i]/val if i==j else 0) for j in range(len(q))] for i in range(len(q))]
    return val,grad,hes


def action(R,ys):
    n=len(ys);value=D(0);grad=[D(0)]*n;diag=[D(0)]*n;off=[D(0)]*(n-1)
    for i in (0,n-1):
        v,g,h=segment(R,ys[i]);value+=v;grad[i]+=g[0];diag[i]+=h[0][0]
    for i in range(n-1):
        v,g,h=segment(R,ys[i],ys[i+1]);value+=v
        grad[i]+=g[0];grad[i+1]+=g[1];diag[i]+=h[0][0];diag[i+1]+=h[1][1];off[i]+=h[0][1]
    return value,grad,diag,off


def solve_tridiag(diag,off,rhs):
    d=diag[:];r=rhs[:]
    for i in range(1,len(d)):
        ratio=off[i-1]/d[i-1];d[i]-=ratio*off[i-1];r[i]-=ratio*r[i-1]
    x=[D(0)]*len(d);x[-1]=r[-1]/d[-1]
    for i in range(len(d)-2,-1,-1):x[i]=(r[i]-off[i]*x[i+1])/d[i]
    return x


def candidate(R,m):
    d=D('0.5')-R;ys=[-d/4]*(2*m)
    for iteration in range(100):
        val,g,diag,off=action(R,ys)
        if max(map(abs,g))<D('1e-58'):return ys,iteration
        step=solve_tridiag(diag,off,[-x for x in g]);slope=sum(a*b for a,b in zip(g,step))
        fac=D(1)
        for _ in range(200):
            trial=[y+fac*s for y,s in zip(ys,step)]
            if all(-d<y<0 for y in trial):
                new,newgrad,_,_=action(R,trial)
                if new<=val+D('0.0001')*fac*slope or max(map(abs,newgrad))<max(map(abs,g))/2:
                    ys=trial;break
            fac/=2
        else:raise ArithmeticError('Newton line search failed')
    raise ArithmeticError('Newton iteration did not converge')


def interval_action(Rq,ys):
    R=Iv.point(Rq);d=Iv.point(Fraction(1,2))-R;rt=Iv.point(3).sqrt()
    yy=[Iv.point(Fraction(y)) for y in ys];xx=[(R.square()-y.square()).sqrt() for y in yy]
    grad=[Iv.point(0) for y in yy];value=Iv.point(0)
    for i in (0,len(yy)-1):
        h=rt/2-xx[i];v=d+yy[i];f=(h.square()+v.square()).sqrt()
        value+=f;grad[i]+=(h*yy[i]/xx[i]+v)/f
    for i in range(len(yy)-1):
        h=rt-xx[i]-xx[i+1];v=yy[i+1]-yy[i];f=(h.square()+v.square()).sqrt();value+=f
        grad[i]+=(h*yy[i]/xx[i]-v)/f
        grad[i+1]+=(h*yy[i+1]/xx[i+1]+v)/f
    err=sum(g.maxabs()**2 for g in grad)/2
    # Strong convexity: minimum >= f(candidate) - ||gradient||^2/2.
    minimum=Iv.point(value.lower()-err)
    minimum.hi=value.hi
    gap=rt-2*R;excess=minimum-2*(len(ys)//2)*gap
    return minimum,excess,max(g.maxabs() for g in grad)


def run():
    checks=0
    def require(condition,message):
        nonlocal checks
        checks+=1
        if not condition:raise ArithmeticError(message)
    # Uniform rational constants used in the complete analytical proof.
    require(Fraction(9,20)**2-Fraction(1,20)**2>Fraction(11,25)**2,'uniform x lower bound')
    require(Fraction(9,10)*Fraction(9,20)**2/Fraction(47,100)**3>1,'strong convexity')
    require(Fraction(1501,940)>Fraction(3,2),'minimum-height constant')
    require(Fraction(1,22)<Fraction(3,50),'angular section margin')
    require(Fraction(1,22)+Fraction(2,79)<Fraction(3,20),'p section margin')
    require(2*Fraction(1,20)**2/Fraction(79,100)<Fraction(1,100),'excess ceiling')
    require(Fraction(7,4)/(4*Fraction(9,20)**2)+Fraction(11,7)<Fraction(15,4),'mean derivative')
    # Horizontal cosine is > .9 for both kinds of segment on the full box.
    require(Fraction(79,200)**2>81*(Fraction(1,20)**2)/19,'end cosine')
    require(Fraction(79,100)**2>81*(Fraction(1,20)**2)/19,'interior cosine')
    results=[]
    with localcontext() as ctx:
        ctx.prec=90
        for rq in (Fraction(9,20),Fraction(23,50),Fraction(47,100)):
            R=D(rq.numerator)/D(rq.denominator);previous=None
            for m in range(1,7):
                ys,it=candidate(R,m);minimum,excess,gradient=interval_action(rq,ys)
                require(gradient<Fraction(1,10**55),'candidate gradient enclosure')
                require(excess.lo>0,'positive excess')
                require(excess.hi<S//100,'excess upper bound')
                if previous is not None:require(excess.lo>previous.hi,'separated consecutive minima')
                require(all(-2*(D('0.5')-R)/5<y<0 for y in ys),'height bound at candidate')
                require(max(abs(ys[i]-ys[-1-i]) for i in range(len(ys)))<D('1e-65'),'symmetric candidate')
                results.append({'R':str(rq),'m':m,'candidate_heights':[str(y) for y in ys],
                                'newton_iterations':it,'length_enclosure':minimum.output(),
                                'excess_enclosure':excess.output(),'gradient_bound':str(gradient)})
                previous=excess
    return {'schema':'a2-dyn-v2-excursion-certificate-1','status':'passed',
            'checks':checks,'finite_parameter_period_samples':len(results),
            'interval_precision_decimal_digits':75,'samples':results,
            'scope':'Finite minimum enclosures plus rational constants. The infinite-period and all-radius results use the analytical proof.',
            'continuum_proof_certificate':False,'full_billiard_LLT_verified':False}

if __name__=='__main__':
    try:
        print(json.dumps(run(),sort_keys=True,separators=(',',':')))
    except (ValueError,ArithmeticError) as exc:
        print(json.dumps({'status':'failed','error':str(exc)},sort_keys=True));raise SystemExit(1)
