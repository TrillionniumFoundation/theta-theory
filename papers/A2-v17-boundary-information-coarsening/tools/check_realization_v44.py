#!/usr/bin/env python3
"""Finite geometric diagnostics for Section 17; not a boundary-law proof."""
from __future__ import annotations
import cmath
from fractions import Fraction as F
import itertools
import json
import math


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def mv(T: tuple, z: complex) -> complex:
    return complex(T[0]*z.real + T[1]*z.imag, T[2]*z.real + T[3]*z.imag)


def support(theta: float, radius: float, amp: float, phase: float) -> tuple:
    h = radius + amp*(math.cos(2*theta)+math.cos(3*theta+phase)/4)
    dh = amp*(-2*math.sin(2*theta)-3*math.sin(3*theta+phase)/4)
    ddh = amp*(-4*math.cos(2*theta)-9*math.cos(3*theta+phase)/4)
    return h, dh, ddh


def channel(T: tuple, w: complex, eps: float, delta: float, i: int, j: int) -> dict:
    v = mv(T, complex(4-8*i, 5-10*j)) + w
    theta0 = cmath.phase(v)
    def derivative(theta: float) -> float:
        n = cmath.exp(1j*theta)
        return (v/(1j*n)).real - support(theta,1,eps,math.pi/4)[1] - support(theta+math.pi,.75,delta,math.pi/6)[1]
    lo, hi = theta0-.1, theta0+.1
    require(derivative(lo)>0 and derivative(hi)<0, 'Contact not bracketed')
    for _ in range(65):
        mid = (lo+hi)/2
        if derivative(mid)>0: lo=mid
        else: hi=mid
    theta = (lo+hi)/2
    n = cmath.exp(1j*theta)
    a = support(theta,1,eps,math.pi/4)
    b = support(theta+math.pi,.75,delta,math.pi/6)
    p = (a[0]+1j*a[1])*n
    q = v-(b[0]+1j*b[1])*n
    gap = (v/n).real-a[0]-b[0]
    require(gap>4.3 and abs(q-p-gap*n)<1e-12, 'Invalid closest pair')
    # Simulate complete recovered curve supports in this edge frame.
    # Registration below receives only the resulting centers and modes.
    def edge_support(phi: float, kind: int) -> float:
        center, rad, amp, phase = ((0j,1,eps,math.pi/4) if kind==1 else (v,.75,delta,math.pi/6))
        return support(phi+theta,rad,amp,phase)[0] + ((center-p)/n/cmath.exp(1j*phi)).real
    def invariants(kind: int) -> dict:
        N=128
        vals=[edge_support(2*math.pi*k/N,kind) for k in range(N)]
        # Trigonometric supports have degree at most three, so the trapezoid
        # sum is exact in exact arithmetic; here it is evaluated in floats.
        z={m:sum(vals[k]*cmath.exp(-1j*m*2*math.pi*k/N) for k in range(N))/N for m in (1,2,3)}
        return {'center':2*z[1].conjugate(), 'z2':z[2], 'z3':z[3]}
    return {'first':invariants(1),'second':invariants(2), 'gap':gap,
            'theta':theta, 'curvatures':[1/(a[0]+a[2]),1/(b[0]+b[2])],
            'residual':abs(derivative(theta))}


def register(images: list[dict]) -> tuple:
    """Use only image invariants, without T, w or the contact positions."""
    ref=images[0]['first']; centers=[]
    for image in images:
        a=image['first']; b=image['second']
        U=a['z3']*ref['z2']/(ref['z3']*a['z2'])
        require(abs(abs(U)-1)<1e-10, 'Noncongruent input supports')
        U /= abs(U)
        centers.append(U*b['center'] + ref['center']-U*a['center'])
    x,y=centers[0]-centers[1],centers[0]-centers[2]
    G=(abs(x)**2,(x.conjugate()*y).real,abs(y)**2)
    return G,abs((centers[0]-centers[3])-x-y)


def main() -> None:
    require(4*F(99,100)-F(2,100)-2*F(81,80)==F(383,200),'Clearance arithmetic')
    require(F(99,100)*F(32,5)-F(407,200)>F(43,10),'All-lattice separation arithmetic')
    require(F(20,19)<F(5,4),'Curvature types not separated')
    matrices=[(1,0,0,1),(1,.005,0,1),(1.005,0,0,.995),(.997,.003,-.002,1.003)]
    shifts=[0j,.005-.005j,-.004+.006j]
    amplitudes=[.005,.0075,.01]
    max_gram=max_cycle=max_residual=0.
    cases=0
    for T,w,eps,delta in itertools.product(matrices,shifts,amplitudes,amplitudes):
        images=[channel(T,w,eps,delta,i,j) for i,j in ((0,0),(1,0),(0,1),(1,1))]
        G,cycle=register(images)
        l1,l2=mv(T,8+0j),mv(T,10j)
        expected=(abs(l1)**2,(l1.conjugate()*l2).real,abs(l2)**2)
        err=max(abs(a-b) for a,b in zip(G,expected))
        require(err<1e-8 and cycle<1e-9,'Image-based lattice reconstruction failed')
        max_gram=max(max_gram,err);max_cycle=max(max_cycle,cycle)
        max_residual=max(max_residual,*(a['residual'] for a in images))
        cases+=1
    concrete=[channel((1,.005,0,1),.005-.005j,.008,.0075,i,j) for i,j in ((0,0),(1,0),(0,1),(1,1))]
    G,cycle=register(concrete)
    print(json.dumps({'status':'passed','mathematical_certification':False,
        'scope':'Finite contact solves and reconstruction from complete edge-image support invariants, not from finite empirical laws',
        'parameter_cases':cases,'channel_solves':4*cases+4,
        'all_translate_clearance_proof_bound':'383/200','separation_proof_lower_bound':'>43/10',
        'maximum_contact_residual':max_residual,'maximum_gram_error':max_gram,
        'maximum_redundant_cycle_error':max_cycle,
        'concrete_gram':[round(x,10) for x in G],
        'concrete_channels':[{'label':label,'gap':x['gap'],'normal_angle':x['theta'],
            'curvatures':x['curvatures']} for label,x in zip(('00','10','01','11'),concrete)]},indent=2,sort_keys=True))


if __name__=='__main__':main()
