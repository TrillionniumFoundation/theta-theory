#!/usr/bin/env python3
"""Outward fixed-point interval certificate; no floating special functions.
The analytic optimality proof is in the manuscript. This script certifies only
specified finite arithmetic only. The interval-normal primitive is inherited
unchanged from the R51 certificate; new uses live in gaussian_certificate.py.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path

B = 10**72

def ceildiv(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError('positive denominator required')
    return -((-a)//b)

@dataclass(frozen=True)
class I:
    lo: int
    hi: int
    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError('reversed interval')
    @staticmethod
    def q(x: F | int) -> 'I':
        x=F(x)
        return I((x.numerator*B)//x.denominator, ceildiv(x.numerator*B,x.denominator))
    @staticmethod
    def lift(x):
        return x if isinstance(x,I) else I.q(x)
    def __add__(self,x):
        x=I.lift(x);return I(self.lo+x.lo,self.hi+x.hi)
    __radd__=__add__
    def __neg__(self): return I(-self.hi,-self.lo)
    def __sub__(self,x): return self+-I.lift(x)
    def __rsub__(self,x): return I.lift(x)+-self
    def __mul__(self,x):
        x=I.lift(x);p=[self.lo*x.lo,self.lo*x.hi,self.hi*x.lo,self.hi*x.hi]
        return I(min(p)//B,ceildiv(max(p),B))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=I.lift(x)
        if x.lo<=0<=x.hi:raise ZeroDivisionError('interval denominator crosses zero')
        if x.hi<0:return (-self)/(-x)
        pairs=[(self.lo,x.lo),(self.lo,x.hi),(self.hi,x.lo),(self.hi,x.hi)]
        return I(min(a*B//b for a,b in pairs),max(ceildiv(a*B,b) for a,b in pairs))
    def __rtruediv__(self,x): return I.lift(x)/self
    def square(self):
        vals=[self.lo*self.lo,self.hi*self.hi]
        lo=0 if self.lo<=0<=self.hi else min(vals)
        return I(lo//B,ceildiv(max(vals),B))
    def midpoint(self):return F(self.lo+self.hi,2*B)
    def strings(self,digits=16):
        scale=10**digits
        def fmt(v):
            sign='-' if v<0 else '';v=abs(v)
            return f'{sign}{v//scale}.{v%scale:0{digits}d}'
        return [fmt(self.lo*scale//B),fmt(ceildiv(self.hi*scale,B))]

def atan_inverse(n:int,terms:int=130)->I:
    total=I.q(0)
    for k in range(terms):
        term=I.q(F(1,(2*k+1)*n**(2*k+1)))
        total=total+term if k%2==0 else total-term
    rem=I.q(F(1,(2*terms+1)*n**(2*terms+1)))
    return I(total.lo,total.hi+rem.hi) if terms%2==0 else I(total.lo-rem.hi,total.hi)

PI=16*atan_inverse(5)-4*atan_inverse(239)
INV_SQRT=I(isqrt(B**3//(2*PI.hi)),isqrt(B**3//(2*PI.lo))+1)


def normal_tail(x:F,terms:int=240)->I:
    x=F(x)
    if x<0:return 1-normal_tail(-x,terms)
    if x>10:raise ValueError('certified implementation restricts |x| <= 10')
    if terms<=50:raise ValueError('remainder requires terms > x^2/2')
    X=I.q(x);term=X;total=I.q(0);z=X.square()/2
    for k in range(terms):
        total=total+term if k%2==0 else total-term
        term=term*z*F(2*k+1,(k+1)*(2*k+3))
    # From this index all exact absolute terms decrease to zero.
    total=I(total.lo,total.hi+term.hi) if terms%2==0 else I(total.lo-term.hi,total.hi)
    cdf=F(1,2)+INV_SQRT*total
    return I(max(0,B-cdf.hi),min(B,B-cdf.lo))

