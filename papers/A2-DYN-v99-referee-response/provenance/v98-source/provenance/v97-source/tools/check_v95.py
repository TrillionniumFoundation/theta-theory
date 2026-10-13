#!/usr/bin/env python3
"""Exact rational fixtures for the new identities; not a continuum certificate."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def integral_line(a, b, va, vb, lo, hi):
    l, r = max(a, lo), min(b, hi)
    if l >= r:
        return F(0)
    slope = (vb-va)/(b-a)
    return (r-l)*(va+slope*((l+r)/2-a))


def fixtures() -> dict:
    count = {}
    def ck(group, ok):
        require(ok, group)
        count[group] = count.get(group, 0)+1
    vals = (F(0), F(1,4), F(1), F(2))
    for ys in product(vals, repeat=4):
        tv = sum(abs(b-a) for a,b in zip(ys,ys[1:]))
        mn = min(ys[0],ys[-1])
        ck('paired_traces', ys[0]+ys[-1]-2*mn == abs(ys[0]-ys[-1]))
        for k, s in product(range(3),(F(1,5),F(1,2),F(4,5))):
            y = (1-s)*ys[k]+s*ys[k+1]
            ck('paired_traces', abs(y-mn)<=tv)
            if ys[0]==0 or ys[-1]==0:
                ck('grazing_end', mn==0 and y<=tv)
    lam = F(47,6)
    eta = 1/(16*lam)
    for q in (F(1,64),F(1,8),F(1,2)):
        d = q*q/(256*lam)
        ck('radial_anchor', 16*d==eta*q*q)
        ck('radial_anchor', q*q-8*lam*d>q*q/4)
        ck('radial_anchor', 4*q*q+8*lam*d<9*q*q)
        for left,right in product((F(1,8),F(1),F(7),F(8),F(17)),repeat=2):
            if left+right<16:
                continue
            ck('radial_anchor', max(left,right)>=8)
            anchor = (-3*d,-2*d) if left>=8 else (2*d,3*d)
            ck('radial_anchor', -left*d<anchor[0]<anchor[1]<right*d)
        ck('thin_class', 1-2*lam*eta==F(7,8))
        ck('thin_class', 4*q*q+8*lam*eta*q*q<9*q*q)
        ck('target_cutoff', q*q-2*lam*(q*q/(8*lam))==3*q*q/4)
    profiles = [
      [[(F(0),F(1)),(F(1),F(2)),(F(3),F(1))]],
      [[(F(-1),F(0)),(F(1),F(2)),(F(2),F(0))],[(F(0),F(1)),(F(2),F(1)),(F(4),F(3))]],
      [[(F(-2),F(3)),(F(0),F(1)),(F(2),F(2))],[(F(-1),F(2)),(F(1),F(0)),(F(3),F(1))]]]
    for sheets in profiles:
        atoms=[]; lines=[]
        for nodes in sheets:
            atoms.extend([(nodes[0][0],nodes[0][1]),(nodes[-1][0],-nodes[-1][1])])
            lines.extend([(a,b,va,vb) for (a,va),(b,vb) in zip(nodes,nodes[1:])])
        def mass(lo,hi):
            return sum((integral_line(*x,lo,hi) for x in lines),F(0))
        def value(t):
            out=F(0)
            for nodes in sheets:
                for (a,va),(b,vb) in zip(nodes,nodes[1:]):
                    if a<t<b:
                        out+=va+(vb-va)*(t-a)/(b-a)
            return out
        for t,r,hp,hn in product((F(-5,7),F(2,7),F(9,7),F(16,7)),
                                (F(1,5),F(4,5),F(8,5)),(F(0),F(1,3),F(1)),(F(0),F(2,3),F(1))):
            rt=value(t)
            am,ap=mass(t-r,t)/r,mass(t,t+r)/r
            def ramp_measure(side,derivative=True,high=False):
                lo,hi=(t-r,t) if side=='-' else (t,t+r)
                out=F(0)
                if derivative:
                    for u,w in atoms:
                        if lo<u<hi:
                            ramp=(u-lo)/r if side=='-' else (hi-u)/r
                            out+=w*ramp
                for a,b,va,vb in lines:
                    l,z=max(a,lo),min(b,hi)
                    if l>=z: continue
                    slope=(vb-va)/(b-a)
                    density=slope if derivative else (hp*max(slope,0) if side=='-' else hn*max(-slope,0))
                    avg=((l+z)/2-lo)/r if side=='-' else (hi-(l+z)/2)/r
                    out+=density*(z-l)*avg
                return out
            dm,dp=ramp_measure('-'),ramp_measure('+')
            hm,hpval=ramp_measure('-',False),ramp_measure('+',False)
            ck('signed_ramps',rt-am==dm)
            ck('signed_ramps',rt-ap==-dp)
            sm,sp=max(dm-hm,0),max(-dp-hpval,0)
            joint=min(sm,sp)
            ck('projected_domination',0<=sm<=rt and 0<=sp<=rt and joint<=sm)
            ck('bidirectional_comparison',rt<=max(am,ap)+joint+hm+hpval)
    ck('no_minimum_interchange',min(3+0,0+3)!=min(3,0)+min(0,3))
    alpha=F(129,128)
    ck('exponents',alpha+1==F(257,128))
    ck('exponents',alpha/2==F(129,256))
    for n in (F(3,2),F(2),F(4)):
        ck('outer_order',n-1>0 and n*(alpha+1)/2-1>0)
    return {'counts':count,'total_checks':sum(count.values()),
            'scope':'exact rational source-packet, finite projected signed-ramp, radial-anchor and exponent fixtures',
            'formal_proof_certificate':False,'independent_human_review':False}


def checks() -> dict:
    return fixtures()


if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
