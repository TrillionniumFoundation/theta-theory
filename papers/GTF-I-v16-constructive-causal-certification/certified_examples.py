#!/usr/bin/env python3
"""Exact rational certificate arithmetic; no floating-point certificate inputs.

The polynomial example is a finite two-time nonconvex simulator problem.
The physical example uses proved collective-coordinate formulas, not a
numerical implementation of arbitrary hard-sphere collision charts.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from math import comb, factorial, lcm
from hashlib import sha256
import json

Poly = dict[tuple[int, int], int]

def add(a: Poly, b: Poly) -> Poly:
    c = dict(a)
    for k, v in b.items():
        c[k] = c.get(k, 0) + v
    return {k: v for k, v in c.items() if v}

def mul(a: Poly, b: Poly) -> Poly:
    c: Poly = {}
    for (i,j), v in a.items():
        for (k,l), w in b.items():
            key = (i+k, j+l)
            c[key] = c.get(key,0) + v*w
    return {k: v for k, v in c.items() if v}

def power(a: Poly, p: int) -> Poly:
    if p < 0: raise ValueError('negative power')
    out: Poly = {(0,0): 1}
    while p:
        if p & 1: out = mul(out,a)
        p //= 2
        if p: a = mul(a,a)
    return out

def gap_polynomial(p: int = 12) -> Poly:
    # Fi = 2 fi; Hi = 2 + Fi; L = 2/5.
    fs: list[Poly] = [{}, {(0,0):1,(1,1):-2},
        {(0,0):-1,(1,0):2,(0,1):2,(1,1):-2},
        {(1,0):2,(0,1):2,(1,1):-4}]
    out: Poly = {}
    for f in fs:
        h = add({(0,0):2},f)
        factor = add({k:5*v for k,v in f.items()},{(0,0):-4})
        out = add(out,mul(power(h,p),factor))
    # This is 10*4^p*P_{p,2/5}; positive scaling preserves signs.
    return out

def bernstein_scaled(poly: Poly, n: int) -> tuple[int, list[list[int]]]:
    """Return a common positive denominator and exact tensor coefficients."""
    d = max((max(k) for k in poly),default=0)
    if n < d: raise ValueError('degree is too small')
    common = lcm(*(comb(n,k) for k in range(d+1)))
    matrix = [[comb(a,k)*(common//comb(n,k)) if k<=a else 0
               for k in range(d+1)] for a in range(n+1)]
    first = [[sum(poly.get((i,j),0)*matrix[a][i] for i in range(d+1))
              for j in range(d+1)] for a in range(n+1)]
    values = [[sum(first[a][j]*matrix[b][j] for j in range(d+1))
               for b in range(n+1)] for a in range(n+1)]
    return common*common, values

def polynomial_certificate(p: int = 12, n: int = 96) -> dict:
    poly = gap_polynomial(p)
    den, coeff = bernstein_scaled(poly,n)
    minimum = min(map(min,coeff))
    return {'power':p,'degree_each_coordinate':n,'lower_bound':'2/5',
            'positive_scaling':str(10*4**p),'power_terms':len(poly),
            'bernstein_coefficients':(n+1)**2,
            'minimum_scaled_numerator':str(minimum),
            'common_denominator':str(den),
            'minimum_coefficient':str(Q(minimum,den)),
            'all_coefficients_strictly_positive':minimum>0,
            'coefficient_sha256':sha256(json.dumps(coeff,separators=(',',':')).encode()).hexdigest()}

BITS = 100
SCALE = 1 << BITS

def floorq(q: Q) -> Q: return Q((q.numerator*SCALE)//q.denominator,SCALE)
def ceilq(q: Q) -> Q: return -floorq(-q)

@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q
    def __post_init__(self):
        if self.lo>self.hi: raise ValueError('inverted interval')
    @staticmethod
    def point(value: int | Q) -> 'Interval':
        return Interval(Q(value),Q(value))
    def __add__(self, other: 'Interval') -> 'Interval':
        return Interval(floorq(self.lo+other.lo),ceilq(self.hi+other.hi))
    def __neg__(self) -> 'Interval': return Interval(-self.hi,-self.lo)
    def __sub__(self, other: 'Interval') -> 'Interval': return self+(-other)
    def __mul__(self, other: 'Interval') -> 'Interval':
        values=[self.lo*other.lo,self.lo*other.hi,self.hi*other.lo,self.hi*other.hi]
        return Interval(floorq(min(values)),ceilq(max(values)))
    def inverse(self) -> 'Interval':
        if self.lo<=0<=self.hi: raise ValueError('division interval contains zero')
        return Interval(floorq(1/self.hi),ceilq(1/self.lo))
    def __truediv__(self,other:'Interval')->'Interval': return self*other.inverse()
    def pow(self,n:int)->'Interval':
        if n<0: return self.inverse().pow(-n)
        out=Interval.point(1); x=self
        while n:
            if n&1: out=out*x
            n//=2
            if n: x=x*x
        return out
    def data(self)->dict:
        return {'lower':str(self.lo),'upper':str(self.hi),'width':str(self.hi-self.lo)}

def atan_unit_inverse(d: int, terms: int) -> Interval:
    if d<2 or terms<1: raise ValueError('invalid arctangent arguments')
    s=sum((Q((-1)**j,(2*j+1)*d**(2*j+1)) for j in range(terms)),Q(0))
    nxt=Q((-1)**terms,(2*terms+1)*d**(2*terms+1))
    return Interval(floorq(min(s,s+nxt)),ceilq(max(s,s+nxt)))

def pi_interval()->Interval:
    # Machin's identity: pi/4 = 4 atan(1/5) - atan(1/239).
    return Interval.point(16)*atan_unit_inverse(5,55)-Interval.point(4)*atan_unit_inverse(239,18)

def sqrt_interval(x: Interval)->Interval:
    if x.lo<0: raise ValueError('negative square root')
    def root_bound(q:Q,up:bool)->Q:
        lo=0;hi=max(SCALE,((q.numerator//q.denominator)+1)*SCALE)
        while hi-lo>1:
            mid=(lo+hi)//2
            if Q(mid*mid,SCALE*SCALE)<=q:lo=mid
            else:hi=mid
        if Q(lo*lo,SCALE*SCALE)==q:return Q(lo,SCALE)
        return Q(hi if up else lo,SCALE)
    return Interval(root_bound(x.lo,False),root_bound(x.hi,True))

def exp_negative(x: Interval)->Interval:
    if x.lo<0: raise ValueError('exp_negative needs nonnegative input')
    def scalar(t:Q)->Interval:
        s=0
        while t>1: t/=2;s+=1
        # Alternating exp(-t) series; t<=1 ensures decreasing terms.
        v=sum(((-t)**j/Q(factorial(j)) for j in range(44)),Q(0))
        nxt=(-t)**44/Q(factorial(44))
        out=Interval(floorq(min(v,v+nxt)),ceilq(max(v,v+nxt)))
        for _ in range(s):out=out*out
        return out
    low=scalar(x.hi);high=scalar(x.lo)
    return Interval(low.lo,high.hi)

def physical_certificate(N:int=2,side:Q=Q(10),time:Q=Q(1,2),order:int=10)->dict:
    if N<2 or side<=0 or time<=0 or order<0:raise ValueError('invalid physical inputs')
    pi=pi_interval();c=sqrt_interval(Interval.point(2)*pi).inverse()
    # tau^2/2 = 2*pi^2*N*time^2/side^2.
    s=Interval.point(2*N*time*time/(side*side))*pi*pi
    total=Interval.point(0)
    for k in range(order+1):
        m=2*k+1;moment=Interval.point(0)
        for j in range(m+1):
            n=abs(m-2*j)
            sign=(-1)**((n-1)//2)
            fourier=Interval.point(Q(2*sign,n))/pi
            term=Interval.point(Q(comb(m,j),2**m))*fourier*exp_negative(Interval.point(n*n)*s)
            moment=moment+term
        total=total+Interval.point(Q((-1)**k,2**k*factorial(k)*(2*k+1)))*moment
    total=c*total
    tail=c.hi*Q(1,2**(order+1)*factorial(order+1)*(2*order+3))
    value=Interval(floorq(total.lo-tail),ceilq(total.hi+tail))
    omega_sq=Interval.point(Q(4*N,1)/(side*side))*pi*pi
    # Taylor error for cos(Z+tau X), L^2(mu).
    degree=16
    double_fact=factorial(2*degree)//(2**degree*factorial(degree))
    norm_sq=omega_sq.pow(degree)*Interval.point(Q(double_fact,2))
    err=Interval.point(time**degree/Q(factorial(degree)))*sqrt_interval(norm_sq)
    alpha=Interval.point(2)*c*err # sum over two actions under a square root = sqrt(2), bounded here by 2.
    return {'particle_number':N,'torus_side':str(side),'flight_time':str(time),
            'noise_variance':1,'Taylor_cdf_order':order,'pi':pi.data(),
            'tau_squared_over_two':s.data(),'deficiency':value.data(),
            'cdf_remainder_bound':str(tail),'nonzero_graph_residual':omega_sq.data(),
            'trial_Taylor_degree':degree-1,'trial_L2_error':err.data(),
            'trial_marked_feedback_upper_bound':str(alpha.hi),
            'scope':'Exact rational arithmetic for the proved collective hard-sphere coordinate. Not an arbitrary collision-chart implementation.'}

if __name__=='__main__':
    print(json.dumps({'polynomial':polynomial_certificate(),'physical':physical_certificate()},indent=2))
