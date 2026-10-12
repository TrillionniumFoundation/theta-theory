#!/usr/bin/env python3
"""Finite regression models for the new algebra, not continuum proof certificates."""
from __future__ import annotations
from fractions import Fraction as F
from math import comb


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def finite_checks() -> dict:
    binomial_cases = 0
    for s in range(1, 81):
        full = sum(comb(s, j)*4**j for j in range(s+1))
        require(full == 5**s, 'binomial theorem')
        for k in (1, max(1,s//2), s, s+3):
            part = sum(comb(s, j)*4**j for j in range(min(k,s)+1))
            require(part <= 5**s, 'truncated sign sum')
            for degree in (1,2,4):
                old = degree*(2*degree-1)**(k-1)*part
                new = degree*(2*degree-1)**(k-1)*5**s
                require(old <= new, 'finite component estimate')
                binomial_cases += 1
    # The finite inequality is tested with dimension growing with the test
    # count; it must not be replaced by a fixed-dimension leading term.
    s,k=3,3
    require(sum(comb(s,j)*4**j for j in range(k+1)) > comb(s,k)*4**k,
            'asymptotic-only negative control')

    band_cases=0
    smallest_slack=None
    for j in range(201):
        theta=F(j,40000)
        s0=F(1,28)-5*theta
        s1=F(1,14)-4*theta
        others=[F(1,14)-6*theta,F(3,14)-5*theta,F(1,14)-7*theta,
                F(1,5)-4*theta,F(1,5)-5*theta,F(1,2)-5*theta,1-6*theta]
        require(s0>0 and s1>0 and all(x>s0 for x in others), 'marked band margins')
        require(F(1,2)-F(2,14)-theta>0 and F(1,2)-F(6,14)-3*theta>0,
                'analytic smallness')
        slack=min(x-s0 for x in others)
        smallest_slack=slack if smallest_slack is None else min(smallest_slack,slack)
        band_cases+=1
    require(F(1,28)-F(5,200)==F(3,280), 'inherited central exponent')
    require(F(1,14)-F(4,200)==F(9,175), 'inherited variation exponent')

    choices=[]
    for Cw in (F(1),F(2),F(17),F(10**5)):
        for ct in (F(1,10**6),F(1,7),F(1),F(100)):
            for at in (F(1,100),F(1),F(73)):
                d=F(1,56);b=1/(56*Cw);a=min(b/2,ct*b/(4*at))
                theta=min(F(1,448),ct*b/32);beta=min(F(1,448),ct*b/16)
                margins=[F(1,28)-5*theta,F(1,14)-4*theta-Cw*b-d,
                         d-4*theta,ct*b-at*a-4*theta]
                mm=[F(1,6),F(1,2)-Cw*b-d,d/2,(ct*b-at*a)/2]
                require(a>0 and b>a and 0<theta<=F(1,200) and beta>0, 'window choices')
                require(all(x>beta for x in margins+mm), 'strict rare-event/moment slack')
                require(margins[0]>=F(11,448) and margins[1]>=F(12,448)
                        and margins[2]>=F(4,448) and margins[3]>=5*ct*b/8,
                        'displayed lower margins')
                require(mm[1]>=F(13,28) and mm[2]>=F(1,112)
                        and mm[3]>=3*ct*b/8, 'displayed moment margins')
                choices.append(min(margins+mm)-beta)
    # A nonzero auxiliary band needs the volume factor, which cannot be
    # erased from a small L1 approximation error.
    theta=F(1,200);d=F(1,100)
    require(d>0 and d-4*theta<0, 'frequency-volume negative control')

    # Finite invertible collision cycles with variable genuine return heights.
    # All tests below concern exact identities under the uniform section law;
    # a finite cycle is not a billiard-mixing or Gaussian-limit model.
    heights=(1,3,5,2,6)
    r=len(heights)
    ell=(0,1,3);m=3
    u=((1,1,1,1,0),(1,1,0,1,1),(1,0,1,1,1))
    W=[F(1) for _ in range(r)]
    for j,t in enumerate(ell):
        W=[W[x]*u[j][(x+t)%r] for x in range(r)]
    mass=sum(W)/r
    require(0<mass<1, 'nontrivial multiple event')
    counts=[sum(heights[(x+t)%r] for t in range(m)) for x in range(r)]
    cutoffs=range(1,sum(heights)+1)
    eps=F(1,11)
    smoothed=[[(1-eps)*a+eps*F(sum(row),r) for a in row] for row in u]
    smoothing_cost=sum(sum(abs(F(u[j][x])-smoothed[j][x]) for x in range(r))/r
                       for j in range(len(ell)))
    models=0;changed_events=0
    for L in cutoffs:
        for shift in range(r):
            original=[W[(x+shift)%r] for x in range(r)]
            approx=[]
            for x in range(r):
                y=(x+shift)%r
                value=F(counts[y]<=L)
                for j,t in enumerate(ell):value*=smoothed[j][(y+t)%r]
                approx.append(value)
            tail=F(sum(c>L for c in counts),r)
            error=sum(abs(a-b) for a,b in zip(original,approx))/r
            require(sum(original)/r==mass, 'same-event invariant mass')
            require(error<=smoothing_cost+tail, 'whole-window L1 replacement')
            require(all(0<=v<=1 for v in approx), 'window supremum')
            truncated=[original[x]*F(counts[(x+shift)%r]<=L) for x in range(r)]
            if sum(truncated)/r!=mass:changed_events+=1
            models+=1
    require(changed_events>0, 'event replacement negative control')
    # Conditional numerator must be divided by the full original mass.
    values=[F(x*x+1) for x in range(r)]
    cond=sum(W[x]*values[x] for x in range(r))/(r*mass)
    explicit=sum(values[x] for x in range(r) if W[x])/sum(1 for x in range(r) if W[x])
    require(cond==explicit, 'unchanged event denominator')

    # Rational non-normal compression of a genuine orthogonal matrix.
    U=[[F(3,5),F(-4,13),F(48,65)],
       [F(4,5),F(3,13),F(-36,65)],
       [F(0),F(12,13),F(5,13)]]
    for i in range(3):
        for j in range(3):
            require(sum(U[t][i]*U[t][j] for t in range(3))==int(i==j), 'unitary model')
    A=[row[:2] for row in U[:2]]
    AA00=sum(A[0][t]**2 for t in range(2))
    AtA00=sum(A[t][0]**2 for t in range(2))
    require(AA00!=AtA00, 'model must be non-normal')
    compression_cases=0
    for x,y in ((F(1),F(0)),(F(3,5),F(4,5)),(F(5,13),F(-12,13))):
        f=[x,y,F(0)];Uf=[sum(U[i][j]*f[j] for j in range(3)) for i in range(3)]
        Af=Uf[:2];leak=1-sum(t*t for t in Af)
        for lam in (1,-1):
            rfull=sum((Uf[j]-lam*f[j])**2 for j in range(3))
            rsmall=sum((Af[j]-lam*f[j])**2 for j in range(2))
            require(rfull==rsmall+leak and leak>=0, 'orthogonal residual identity')
            require(rfull*rfull<=9*rsmall, 'physical squared defect at most 3 residual')
            compression_cases+=1
    require(leak>0, 'projection leakage negative control')
    # Positive defect at one scalar spectral point is not power decay:
    # U=-I, lambda=1 has defect 2, yet every power has norm one.
    require(abs(-1-1)==2 and all(abs((-1)**n)==1 for n in range(1,20)),
            'one-point defect is not power decay')

    return {'binomial_component_cases':binomial_cases,
            'subband_cases':band_cases,'minimum_subband_margin_slack':str(smallest_slack),
            'nonempty_budget_cases':len(choices),'minimum_tested_budget_slack':str(min(choices)),
            'variable_height_window_cases':models,'changed_cutoff_event_cases':changed_events,
            'orthogonal_nonnormal_compression_cases':compression_cases,
            'negative_controls':5,
            'finite_models_are_not_continuum_proof_certificates':True}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
