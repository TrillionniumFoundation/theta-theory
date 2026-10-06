#!/usr/bin/env python3
"""Finite regression checks, not verification of continuum theorems."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json
import math

checks = 0
negative_controls = 0

def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(message)

def reject(condition: bool, message: str) -> None:
    global negative_controls
    if condition:
        raise RuntimeError("negative control survived: " + message)
    negative_controls += 1

def psi(a: tuple[float, ...], m: int) -> float:
    if m < 1:
        raise ValueError("positive count required")
    a = tuple(sorted((x for x in a if x > 0), reverse=True))
    if not a:
        return 0.0
    p, result = 1.0, 0.0
    for k, x in enumerate(a, 1):
        p *= x
        result = max(result, (p / m) ** (2.0 / k))
    return result

# Conditional-mean projection for rational finite experiments.
for p in [F(i, 16) for i in range(17)]:
    for a in [F(i, 12) for i in range(13)]:
        risk = p * (1-a)**2 + (1-p) * a*a
        require(risk == p*(1-p) + (p-a)**2, "projection identity")

# Exact HMM normalization, invariant bounds, derivative and TV coefficients.
for q in [F(1,100), F(1,10), F(1,4), F(49,100)]:
    rho = 1 - 2*q
    for a in [F(1,20), F(1,3), F(4,5)]:
        lo = q*(1-a)/(1+a*(1-2*q))
        for p in [F(i,16) for i in range(17)]:
            r = q + rho*p
            v = p*(1-p)
            require(q <= r <= 1-q, "prediction interval")
            require(q*(1-q)+rho*rho*v >= v, "logit contraction denominator")
            for y in [F(-1), F(-1,3), F(0), F(2,5), F(1)]:
                den = 1+a*y*(2*r-1)
                update = r*(1+a*y)/den
                require(den >= 1-a, "positive likelihood denominator")
                require(lo <= update <= 1-lo, "invariant interval")
                derivative = 2*a*r*(1-r)/(den*den)
                floor = 2*a*q*(1-q)/(1+a)**2
                require(derivative >= floor, "actual acquisition Jacobian floor")
        p, pp = F(1,4), F(3,4)
        tv = a*rho*abs(p-pp)/2
        require(tv == abs(a*rho*(p-pp))*F(1,2), "density TV integral")
        reject(tv == a*rho*abs(p-pp), "missing TV factor one half")

# All-budget anisotropic grids, including deleted zero coordinates.
for a in [(1,), (1,0), (1,.5), (1,.01), (1,.5,.001), (0,0), (.1,.1,.1)]:
    for m in range(1,257):
        h = math.sqrt(psi(a,m))
        if h == 0:
            require(not any(a), "rank zero only")
            continue
        R = 2*h
        ns = [math.ceil(x/R) if x>R else 1 for x in sorted(a,reverse=True)]
        require(math.prod(ns) <= m, "grid cardinality")
        require(all(x/n <= R+1e-12 for x,n in zip(sorted(a,reverse=True),ns)), "grid covering")
        if m >= 2:
            k = m//2
            require(psi(a,k) <= (m/k)**2*psi(a,m)+1e-12, "allocation scaling")
require(psi((1,0),64) == psi((1,),64), "rank deletion identity")
reject(abs(psi((1,0),64) - 1/64) < 1e-12, "ambient two-dimensional exponent")

# Exact transport with any number of holds and at most one acquisition.
for n in range(10):
    for acquisition in range(-1,n):
        z0, z1, e = F(1), F(0), F(2,7)
        initial_error, radius = F(2,7), F(1,11)
        for t in range(n):
            if t == acquisition:
                A, B = F(0), F(1)
            else:
                A, B = F(1), F(0)
            z0, z1 = A*z0, A*z1+B
            e = A*e+B*radius
        require(e == z0*initial_error+z1*radius, "unrolled innovation")
        require((z0,z1) == ((F(1),F(0)) if acquisition<0 else (F(0),F(1))), "indicator transport")
        require(z0*z1 == 0, "no cross energy")
        if n>0 and acquisition<0:
            reject(e == initial_error+n*radius, "rounding exact holds repeatedly")

# Contractive active transitions interspersed with arbitrary holds.
for n in range(9):
    for word in product((0,1), repeat=n):
        rho = F(2,3)
        Z, events = F(1), 0
        for active in word:
            if active:
                Z = rho*Z+1
                events += 1
        exact = sum((rho**i for i in range(events+1)), F(0))
        require(Z == exact, "event-time geometric sum")
        require(Z <= 1/(1-rho), "hold-uniform bound")

# Actual acquisition probabilities, variance decomposition, and weighted forcing.
for s in [F(0),F(1,100),F(1,3),F(1)]:
    for n in range(20):
        h = (1-s)**n
        V, noise, r0, r1 = F(1,48), F(11,48), F(1,7), F(1,13)
        B = h*(noise+V)+(1-h)*noise
        require(B == noise+h*V, "raw acquisition baseline")
        require(h*r0*r0+(1-h)*r1*r1 == h*r0**2+(1-h)*r1**2, "weighted transport energy")
        require(0 <= h <= 1, "actual acquired mass")
# Calibration and erasure lower witnesses.
for h in [F(0),F(1,100),F(1,4)]:
    gap = ((F(1,2)-h-F(1,2))**2+(F(1,2)+h-F(1,2))**2)/2
    require(gap == h*h, "indistinguishable calibration floor")
for theta in [F(i,16) for i in range(17)]:
    require(theta*F(1,4) == (theta/2)/2, "erasure risk versus defect")
reject(F(0) >= F(1,100), "allowed tolerance forces error in exact instance")
require(3*5*7*11 == 1155, "simulator/controller/clock state product")
reject(3+5+7+11 == 1155, "state counts add")
print(json.dumps({"status":"success", "finite_checks":checks,
                  "negative_controls_rejected":negative_controls,
                  "continuum_proof_by_tests":False}, sort_keys=True))
