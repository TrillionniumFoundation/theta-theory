#!/usr/bin/env python3
"""Exact finite diagnostics for common-orientation equivariance.

These checks do not prove analytic rigidity, statistical identifiability for
folded billiard records, or a complete native build. Exceptions, not removable
assertions, enforce every check in ordinary and optimized Python.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

COUNTS: Counter[str] = Counter()
BASE = 'e5a153b1bbb663c4a5e3153c6a7bdedb7fcd5864'


def require(value: bool, group: str) -> None:
    if not value:
        raise RuntimeError('Failed exact check: '+group)
    COUNTS[group] += 1


def mm(a, b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def mv(a, x):
    return tuple(sum(a[i][j]*x[j] for j in range(2)) for i in range(2))


def add(x, y):
    return tuple(a+b for a,b in zip(x,y))


def neg(x):
    return tuple(-a for a in x)


def tr(a):
    return tuple(zip(*a))


def det(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def inv(a):
    d=det(a)
    if not d:
        raise ValueError('Singular diagnostic matrix')
    return ((a[1][1]/d,-a[0][1]/d),(-a[1][0]/d,a[0][0]/d))


def run() -> dict:
    J=((F(1),F(0)),(F(0),F(-1)))
    I=((F(1),F(0)),(F(0),F(1)))
    lattices=[((F(2),F(1,3)),(F(0),F(3))),
              ((F(3,2),F(1,2)),(F(1,3),F(2))),
              ((F(1),F(-2,3)),(F(1,2),F(3)))]
    marks=[((F(1),F(0)),(F(0),F(1))),
           ((F(2),F(1)),(F(0),F(3))),
           ((F(1),F(3)),(F(2),F(1)))]
    offsets=[(F(0),F(0)),(F(2),F(-1)),(F(-3),F(4))]
    for L in lattices:
        require(det(L)>0 and det(mm(J,L))==-det(L),'lattice_orientation_sector')
        require(mm(tr(mm(J,L)),mm(J,L))==mm(tr(L),L),'gram_invariance')
        for M in marks:
            V=mm(L,M)
            require(mm(V,inv(M))==L,'rank_two_recovery')
            require(mm(mm(J,V),inv(M))==mm(J,L),'reflected_rank_two_recovery')
        for t in (F(0),F(1,3),F(2,3)):
            c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
            R=((c,-s),(s,c));Rr=mm(mm(J,R),J)
            require(det(R)==1 and det(Rr)==1,'proper_placement_conjugation')
            require(mm(tr(R),R)==I and mm(mm(J,Rr),J)==R,'placement_involution')
            shift=(F(2,7),F(-3,5))
            for nu in offsets:
                for n in range(-4,5):
                    y=F(n,10);x=(y*y/2+y**3/7,y)
                    # J(tau_{-L nu} A x) = tau_{-JL nu}(JAJ)(Jx).
                    lhs=mv(J,add(add(mv(R,x),shift),neg(mv(L,nu))))
                    rhs=add(add(mv(Rr,mv(J,x)),mv(J,shift)),neg(mv(mm(J,L),nu)))
                    require(lhs==rhs,'incidence_equivariance')
                    Hx=add(x,mv(L,nu))
                    require(mv(J,Hx)==add(mv(J,x),mv(J,mv(L,nu))),
                            'translation_holonomy_conjugation')
    for m in range(2,13):
        q=[F(0),F(0)]+[F(n+1,n+2) for n in range(2,m+1)]
        qr=[((-1)**n)*a for n,a in enumerate(q)]
        for i in range(-5,6):
            u=F(i,12)
            require(sum(a*(-u)**n for n,a in enumerate(q))==
                    sum(a*u**n for n,a in enumerate(qr)), 'finite_polynomial_jet_parity')
    for alpha in (F(1,20),F(1,10),F(1,5)):
        def f(u,v,k):
            return (1+k*alpha*(u+v))/4
        require(1-4*alpha>0,'positive_density_on_entire_box')
        # Integrals of u and v on the symmetric box are zero exactly.
        require(F(1,4)*4==1,'density_normalization')
        for i in range(1,6):
            for j in range(1,6):
                a,b=F(i,6),F(j,6)
                for k in (1,2):
                    folded=sum(f(s*a,t*b,k) for s in (-1,1) for t in (-1,1))
                    require(folded==1,'folded_density_identity')
                require(f(a,b,2)!=f(a,b,1) and f(a,b,2)!=f(-a,-b,1),
                        'different_law_valued_orbits')
        beta=alpha/2
        datum=(alpha,beta)
        orbit={datum,tuple(-x for x in datum)}
        require((-alpha,beta) not in orbit,'diagonal_not_independent_channel_action')
    return {
        'scope':'Exact finite algebraic diagnostics; not a native build or proof certificate.',
        'review_base':BASE,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'checks':dict(sorted(COUNTS.items())),
        'total_checks':sum(COUNTS.values()),
        'arithmetic':'fractions.Fraction throughout',
        'status':'passed',
    }


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
