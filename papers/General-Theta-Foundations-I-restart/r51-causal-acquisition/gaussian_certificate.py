#!/usr/bin/env python3
"""Outward fixed-point interval certificate; no floating special functions.
The analytic optimality proof is in the manuscript. This script certifies only
specified finite arithmetic, feasible thresholds, and checkpoint constructions.
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


def curve(h:F,kappa:F=F(1),mu:F=F(1)):
    a=normal_tail(h-mu);b=normal_tail(h+mu)
    D=a+b+2*kappa*a*b
    T=(2+kappa*(a+b))/D
    m=(a-b)/D
    return T,m,a,b


def bracket(N:int):
    lo=F(-4);hi=F(4)
    if not curve(lo)[0].hi < N*B < curve(hi)[0].lo:
        raise RuntimeError('initial bracket not certified')
    for _ in range(50):
        mid=(lo+hi)/2;T=curve(mid)[0]
        if T.hi <= N*B:lo=mid
        elif T.lo >= N*B:hi=mid
        else:raise RuntimeError('precision insufficient to decide bisection')
    tl,ml,*_=curve(lo);th,mh,*_=curve(hi)
    if tl.hi>N*B or th.lo<N*B:raise RuntimeError('bad final mean bracket')
    opt=I((1-mh.square()).lo,(1-ml.square()).hi)
    decoder=ml.midpoint()
    feasible=1-2*decoder*ml+decoder*decoder
    return lo,hi,tl,ml,opt,feasible,decoder


def checkpoint(h:F,bins:list[F]):
    T,m,*_=curve(h);vp=(T-m)/2;vm=(T+m)/2
    boundaries=[h]+[h+x for x in bins]
    risk=I.q(0);mass=I.q(0);dec=[]
    for j,left in enumerate(boundaries):
        ap=normal_tail(left-1);am=normal_tail(left+1)
        if j+1<len(boundaries):
            right=boundaries[j+1];ap=ap-normal_tail(right-1);am=am-normal_tail(right+1)
        pp=vp*ap;pm=vm*am;p=pp+pm;diff=pp-pm
        if p.lo<=0:raise RuntimeError('nonpositive certified bin mass')
        r=(diff/p).midpoint()
        risk=risk+p*(1+r*r)-2*r*diff;mass=mass+p;dec.append(str(r))
    if not mass.lo<=B<=mass.hi:raise RuntimeError('checkpoint total mass excludes one')
    return risk,dec


def run():
    rows=[]
    for N in (2,4,8):
        lo,hi,T,m,opt,feas,dec=bracket(N)
        cp2,dec2=checkpoint(lo,[F(1)])
        cp4,dec4=checkpoint(lo,[F(1,2),F(1),F(2)])
        if not cp4.hi<cp2.lo<opt.lo:raise RuntimeError('strict comparison not certified')
        rows.append({'N':N,'h_bracket_rational':[str(lo),str(hi)],'h_enclosure':I(I.q(lo).lo,I.q(hi).hi).strings(),
                     'optimum_risk':opt.strings(),'feasible_mean':T.strings(),'feasible_risk':feas.strings(),
                     'feasible_threshold':str(lo),'feasible_decoder':str(dec),'checkpoint_2_risk':cp2.strings(),
                     'checkpoint_4_risk':cp4.strings(),'checkpoint_2_decoders':dec2,'checkpoint_4_decoders':dec4})
    return {'status':'PASS','method':'outward fixed-point integer intervals; Machin arctangent and 240-term normal power series; 50 bisections',
            'decimal_grid_digits':72,'q':'1/4','mu':'1','pi_interval':PI.strings(50),'rows':rows,
            'scope':'exact two-state autonomous optimum bracket; feasible two/four-label checkpoint constructions, not their unrestricted optima'}


def table(data):
    lines=[r'\begin{center}',r'\small',r'\begin{tabular}{@{}rllll@{}}',r'\toprule',
           r'$N$ & $h_N$ & $R_{\aut}(N,2)$ & checkpoint, $m=2$ & checkpoint, $m=4$ \\',r'\midrule']
    def enc(v,d=6):
        lo=F(v[0]);hi=F(v[1]);scale=10**d
        l=lo.numerator*scale//lo.denominator;u=ceildiv(hi.numerator*scale,hi.denominator)
        return f'[{l/scale:.{d}f}, {u/scale:.{d}f}]'
    # Formatting floats below is not used in any proof or interval endpoint.
    # Assert the displayed decimal strings still enclose the rational data.
    for row in data['rows']:
        vals=[enc(row[k]) for k in ['h_enclosure','optimum_risk','checkpoint_2_risk','checkpoint_4_risk']]
        for s,k in zip(vals,['h_enclosure','optimum_risk','checkpoint_2_risk','checkpoint_4_risk']):
            l,u=[F(v.strip()) for v in s.strip('[]').split(',')]
            if not l<=F(row[k][0])<=F(row[k][1])<=u:raise RuntimeError('display rounding invalid')
        lines.append(str(row['N'])+' & '+' & '.join('$'+v+'$' for v in vals)+r' \\')
    lines += [r'\bottomrule',r'\end{tabular}',r'\end{center}',
              'The checkpoint columns are outward enclosures of achievable risks using the feasible lower threshold, not certified intervals for the checkpoint optimum. Their two-bin boundary is $h+1$; the four-bin interior boundaries are $h+1/2,h+1,h+2$. Both tails are retained.']
    return '\n'.join(lines)+'\n'

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    result=run();text=table(result);root=Path(__file__).resolve().parent
    target=root/'sections/gaussian-table.tex'
    if args.write:
        target.write_text(text);(root/'GAUSSIAN_CERTIFICATE.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        if target.read_text()!=text:raise SystemExit('generated Gaussian table mismatch')
        if json.loads((root/'GAUSSIAN_CERTIFICATE.json').read_text())!=result:raise SystemExit('Gaussian certificate mismatch')
    print(json.dumps(result,sort_keys=True,indent=2))
