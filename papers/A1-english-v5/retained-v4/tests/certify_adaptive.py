#!/usr/bin/env python3
"""Exact outward rational certificates for A1 v4, not a proof assistant.
The reduction from all Borel gates to these vertices is proved in the paper.
Run from any directory. No network, sampling, or floating-point comparisons.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
import hashlib
import json

@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F
    def __post_init__(self):
        assert self.lo <= self.hi
    @staticmethod
    def of(x):
        return x if isinstance(x, Interval) else Interval(F(x), F(x))
    def __add__(self, other):
        b = self.of(other); return Interval(self.lo+b.lo, self.hi+b.hi)
    __radd__ = __add__
    def __neg__(self): return Interval(-self.hi, -self.lo)
    def __sub__(self, other): return self + (-self.of(other))
    def __rsub__(self, other): return self.of(other) - self
    def __mul__(self, other):
        b=self.of(other); v=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi]
        return Interval(min(v),max(v))
    __rmul__ = __mul__
    def __truediv__(self, other):
        b=self.of(other); assert b.lo*b.hi>0, 'denominator crosses zero'
        return self*Interval(1/b.hi,1/b.lo)
    def __rtruediv__(self, other): return self.of(other)/self
    def __pow__(self, n):
        assert isinstance(n,int) and n>=0
        out=self.of(1)
        for _ in range(n): out=out*self
        return out

def imax(values):
    values=list(values); return Interval(max(x.lo for x in values),max(x.hi for x in values))

def atan_interval(inv:int,n:int)->Interval:
    """Alternating Taylor series and its next-term remainder, 0<1/inv<1."""
    s=sum((F((-1)**k, (2*k+1)*inv**(2*k+1)) for k in range(n)),F(0))
    next_term=F((-1)**n,(2*n+1)*inv**(2*n+1))
    return Interval(min(s,s+next_term),max(s,s+next_term))

def outward(x:Interval,digits:int=40)->Interval:
    scale=10**digits
    return Interval(F((x.lo*scale).__floor__(),scale),F((x.hi*scale).__ceil__(),scale))

def decimal_bounds(x:Interval,digits:int=15)->dict:
    x=outward(x,digits); scale=10**digits
    def fmt(v:F):
        n=int(v*scale); sign='-' if n<0 else ''; n=abs(n)
        return f'{sign}{n//scale}.{n%scale:0{digits}d}'
    return {'lower':fmt(x.lo),'upper':fmt(x.hi)}

PI=outward(16*atan_interval(5,40)-4*atan_interval(239,10))
scale=10**40; root=isqrt(3*scale*scale)
SQRT3=Interval(F(root,scale),F(root+1,scale))
assert SQRT3.lo**2<3<SQRT3.hi**2
A0=SQRT3/2
RADII=[F(9,20),F(47,100)]; T=F(1,20); S=F(99,100)
PROB=[[PI*r*r/A0,(A0-PI*r*r-2*T*r)/A0,2*T*r/A0] for r in RADII]
for row in PROB:
    assert all(x.lo>0 for x in row)
    assert sum(row).lo<=1<=sum(row).hi
GATES=list(product([0,1],repeat=3)); O=(0,0,0); A=(0,1,0)
PRIOR=[Interval.of(F(2,5)),Interval.of(F(3,5))]

def terminal(z): return imax([2*z[0]+z[1],z[0]+2*z[1]])
def branches(z,g):
    for j in range(3):
        if g[j]: yield [z[i]*PROB[i][j] for i in range(2)],S,j
    yield [z[i]*sum((PROB[i][j] for j in range(3) if not g[j]),Interval.of(0)) for i in range(2)],F(1),3

def one_fixed(z,g): return sum((w*terminal(zz) for zz,w,_ in branches(z,g)),Interval.of(0))
def one_opt(z): return imax(one_fixed(z,g) for g in GATES)
def two_fixed(g,h): return sum((w*one_fixed(zz,h) for zz,w,_ in branches(PRIOR,g)),Interval.of(0))
def two_adaptive(g): return sum((w*one_opt(zz) for zz,w,_ in branches(PRIOR,g)),Interval.of(0))

def certificate()->dict:
    nonadaptive={(g,h):two_fixed(g,h) for g in GATES for h in GATES}
    adaptive={g:two_adaptive(g) for g in GATES}
    vn=nonadaptive[(A,A)]; va=adaptive[A]
    assert all(vn.lo>v.hi for key,v in nonadaptive.items() if key!=(A,A))
    assert all(va.lo>v.hi for g,v in adaptive.items() if g!=A)
    next_checks=[]
    for z,w,tag in branches(PRIOR,A):
        selected=A if tag==1 else O
        values={g:one_fixed(z,g) for g in GATES}
        # Strict best here; certificate does not assume this at arbitrary states.
        assert all(values[selected].lo>v.hi for g,v in values.items() if g!=selected)
        next_checks.append({'report_tag':tag,'optimal_gate':list(selected),
                            'weighted_continuation':decimal_bounds(w*values[selected]),
                            'all_weighted_candidates':[{'gate':list(g),**decimal_bounds(w*v)} for g,v in values.items()]})
    gap=va-vn
    q=[row[1] for row in PROB]
    explicit_gap=(1-S)*(F(2,5)*q[0]*(1-q[0])+F(6,5)*q[1]*(1-q[1]))
    assert gap.lo<=explicit_gap.hi and explicit_gap.lo<=gap.hi
    assert gap.lo>F(2154,10**6)
    # Verify all terminal decision signs in the claimed A,A decision rule.
    signs={}
    for j in [0,1]:
        for k in [0,1]:
            zl=F(2,5)*(q[0] if j else 1-q[0])*(q[0] if k else 1-q[0])
            zu=F(3,5)*(q[1] if j else 1-q[1])*(q[1] if k else 1-q[1])
            diff=zl-zu
            assert (diff.lo>0) if j==k==1 else (diff.hi<0)
            signs[f'{j}{k}']=decimal_bounds(diff)
    E=F(1,20); u=RADII[1]; alpha=F(1,10000)
    eps0=(2*T*u/A0)*(E*u*u)/PI
    eps2=1-(1-eps0)**2
    oscillation=2-S*S
    transferred_gap=gap-2*oscillation*(eps2+alpha)
    assert transferred_gap.lo>F(11,10000)
    return {
      'arithmetic':'Exact fractions with outward interval enclosures; no floating-point decision',
      'scope':'All Borel gates; coverage proof is Theorem thm:adaptive-advantage, not inferred from enumeration',
      'pi':decimal_bounds(PI,40),'sqrt3':decimal_bounds(SQRT3,40),
      'pi_method':'Machin identity, 40 terms atan(1/5), 10 terms atan(1/239); next-term remainders',
      'sqrt3_method':'integer square root at denominator 10^40; both squared inequalities checked',
      'nominal':{'prior':['2/5','3/5'],'R':['9/20','47/100'],'T':'1/20','epsilon':'0',
        'acceptance_multiplier':'99/100','gate_order':['placement failure','no collision','collision'],
        'nonadaptive_combinations':64,'nonadaptive_optimal_gates':[list(A),list(A)],
        'adaptive_first_gate':list(A),'adaptive_continuations':next_checks,
        'nonadaptive_value':decimal_bounds(vn),'adaptive_value':decimal_bounds(va),
        'strict_advantage':decimal_bounds(gap),'closed_form_advantage':decimal_bounds(explicit_gap),
        'terminal_posterior_signs':signs},
      'full_cubic_transfer':{'mode_set':'{1/20} x [0,1/20] x S^1',
        'prior':'(1-1/10000)[(2/5) delta_l + (3/5) delta_u] + (1/10000) Uniform(I)',
        'payoff_oscillation':'10199/10000','one_step_TV_bound':decimal_bounds(eps0),
        'two_step_TV_bound':decimal_bounds(eps2),'certified_gap':decimal_bounds(transferred_gap),
        'strict_certified_lower_bound':'11/10000'},
      'all_nonadaptive_values':[{'first':list(g),'second':list(h),**decimal_bounds(v)} for (g,h),v in nonadaptive.items()],
      'all_adaptive_first_gate_values':[{'first':list(g),**decimal_bounds(v)} for g,v in adaptive.items()],
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }

if __name__=='__main__':
    result=certificate()
    target=Path(__file__).resolve().parents[1]/'validation'/'ADAPTIVE_CERTIFICATE.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['nominal','full_cubic_transfer']},indent=2))
