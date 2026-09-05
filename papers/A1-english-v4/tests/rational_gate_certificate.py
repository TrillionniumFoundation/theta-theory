#!/usr/bin/env python3
"""Exact rational interval certificate for Proposition 4.2.
No floating-point numbers are used to prove the inequalities.  The finite
certificate does not certify the paper's all-budget theorems.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path

@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F
    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError("Reversed interval")
    @staticmethod
    def point(x):
        return x if isinstance(x, Interval) else Interval(F(x), F(x))
    def __add__(self, other):
        b=self.point(other); return Interval(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self): return Interval(-self.hi,-self.lo)
    def __sub__(self, other): return self + -self.point(other)
    def __rsub__(self, other): return self.point(other) + -self
    def __mul__(self, other):
        b=self.point(other); v=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi]
        return Interval(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self, other):
        b=self.point(other)
        if b.lo <= 0 <= b.hi: raise ZeroDivisionError("Interval meets zero")
        return self * Interval(1/b.hi,1/b.lo)
    def __rtruediv__(self, other): return self.point(other)/self
    def sqrt(self):
        if self.lo < 0: raise ValueError("Negative square root")
        D=10**30
        def bounds(x):
            n=isqrt((x.numerator*D*D)//x.denominator)
            exact=n*n*x.denominator==x.numerator*D*D
            return F(n,D),F(n if exact else n+1,D)
        return Interval(bounds(self.lo)[0],bounds(self.hi)[1])
    def absolute(self):
        if self.lo>=0:return self
        if self.hi<=0:return -self
        return Interval(F(0),max(-self.lo,self.hi))
    def enclosed(self, lo: str, hi: str):
        return F(lo)<self.lo and self.hi<F(hi)
    def record(self):
        D=10**24
        lo=F((self.lo.numerator*D)//self.lo.denominator,D)
        hi=F(-((-self.hi.numerator*D)//self.hi.denominator),D)
        return {"lower":str(lo),"upper":str(hi),
                "outward_receipt_grid":"10^-24",
                "decimal_display_only":[float(lo),float(hi)]}

def atan_point(x: F, terms: int=48) -> Interval:
    if not 0<=x<=F(1,4):raise ValueError("Arctangent argument outside certified range")
    s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(terms)), F(0))
    nxt=(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return Interval(min(s,s+nxt),max(s,s+nxt))

def atan(x: Interval) -> Interval:
    return Interval(atan_point(x.lo).lo,atan_point(x.hi).hi)

PI=16*atan_point(F(1,5))-4*atan_point(F(1,239))
A0=Interval.point(3).sqrt()/2

def positive_cosine_mean(a: Interval,b: Interval) -> Interval:
    b=b.absolute()
    if a.lo>=b.hi:return a
    if a.hi<=-b.hi:return Interval.point(0)
    # Only the strictly negative-a, interior case is used in this certificate.
    if not (a.hi<0 and -a.lo<b.lo):raise ValueError("Uncertified sign case")
    z=-a/b
    angle=PI/2-atan(z/(1-z*z).sqrt())
    return (a*angle+(b*b-a*a).sqrt())/PI

def certificate():
    l,u=F(9,20),F(47,100); R=[l,u]; p=[u/(l+u),l/(l+u)]
    gains=[[F(3,2),F(1,2)],[F(1,2),F(3,2)]]
    alpha=F(999,1000); b=F(1,10)
    M=[[sum(p[i]*gains[j][i]*R[i]**k for i in range(2)) for k in range(4)] for j in range(2)]
    assert M[0][1]==M[1][1]
    U=[PI/A0*M[j][2] for j in range(2)]
    H=[Interval.point(M[j][0])-U[j]-b/A0*M[j][1] for j in range(2)]
    A=b/A0*M[0][1]; B=[b/A0*M[j][3] for j in range(2)]
    assert (alpha*U[1]-U[0]).lo>0
    assert (alpha*H[0]-H[1]).lo>0
    assert (U[1]-U[0]).lo>0 and (H[0]-H[1]).lo>0
    a=(alpha-1)*A
    bb=[alpha*B[1]-B[0],alpha*B[0]-B[1]]
    Q=[M[0][0]+alpha*U[1]-U[0]+positive_cosine_mean(a,bb[0]),
       M[1][0]+alpha*H[0]-H[1]+positive_cosine_mean(a,bb[1])]
    blind_accept=alpha*(U[1]+H[0]+A+(B[1]-B[0])/PI)
    blind_reject=Interval.point(M[0][0])
    threshold=-a/bb[1]
    gap=Q[1]-blind_accept
    assert Q[0].enclosed('1.02689','1.02691')
    assert Q[1].enclosed('1.02748','1.02749')
    assert blind_accept.enclosed('1.02667','1.02669')
    assert blind_reject.enclosed('1.01086','1.01088')
    assert threshold.enclosed('-0.10631','-0.10630')
    assert gap.lo>F(8,10000)
    assert (Q[1]-Q[0]).lo>0
    assert (blind_accept-blind_reject).lo>0
    # A full-support prior in the 10^-5 TV ball retains a >7*10^-4 gap.
    width=F(3,2)-alpha*F(1,2)
    robust_gap=gap-2*width*F(1,100000)
    assert robust_gap.lo>F(7,10000)
    return {"arithmetic":"exact Fraction interval arithmetic",
            "pi_certificate":"Machin identity, 48 alternating terms per arctangent",
            "sqrt_grid_denominator":"10^30", "all_assertions_passed":True,
            "Q_fallback_1":Q[0].record(),"Q_fallback_2":Q[1].record(),
            "blind_accept":blind_accept.record(),"blind_reject":blind_reject.record(),
            "collision_cosine_threshold":threshold.record(),"gap":gap.record(),
            "full_support_perturbation_gap":robust_gap.record()}

if __name__=='__main__':
    result=certificate()
    out=Path(__file__).resolve().parents[1]/'validation'/'rational_gate_certificate.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('Exact rational gate certificate: PASS')
    print('Certified gap > 8/10000; full-support perturbation gap > 7/10000')
