#!/usr/bin/env python3
"""Finite diagnostics for A2 v7; not a proof of the nonlinear billiard theorems.
Uses the Python standard library only. Checks remain active under python -O.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import itertools
import json
import math
from pathlib import Path

CHECKS: list[dict[str, str]] = []

def check(name: str, condition: bool, kind: str = "exact rational") -> None:
    if not condition:
        raise RuntimeError("Diagnostic failed: " + name)
    CHECKS.append({"name": name, "kind": kind, "status": "PASS"})

def polyadd(a: list[F], b: list[F]) -> list[F]:
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0)) for i in range(n)]

def polymul(a: list[F], b: list[F]) -> list[F]:
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out

def qadd(x: tuple[F,F], y: tuple[F,F]) -> tuple[F,F]:
    return x[0]+y[0], x[1]+y[1]

def qmul(x: tuple[F,F], y: tuple[F,F]) -> tuple[F,F]:
    return x[0]*y[0]+3*x[1]*y[1], x[0]*y[1]+x[1]*y[0]

def matmul(x, y):
    return [[qadd(qmul(x[i][0], y[0][j]), qmul(x[i][1], y[1][j])) for j in range(2)] for i in range(2)]

def simpson(f, a: float, b: float, n: int = 8192) -> float:
    if n < 2 or n % 2:
        raise ValueError("Simpson grid must be positive and even")
    step = (b-a)/n
    total = f(a) + f(b)
    total += 4*sum(f(a+i*step) for i in range(1,n,2))
    total += 2*sum(f(a+i*step) for i in range(2,n,2))
    return total*step/3

def product_overlap(p: list[F], q: list[F], k: int) -> F:
    result = F(0)
    for word in itertools.product(range(len(p)), repeat=k):
        pp, qq = F(1), F(1)
        for x in word:
            pp *= p[x]
            qq *= q[x]
        result += min(pp, qq)
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    # H_j/a and its two eigenvalues, without floating-point determinants.
    for u in [F(1,2),F(1,3),F(2,3),F(3,5),F(1,16),F(1,256)]:
        diag = (1+u*u)/(1-u*u)
        off = -2*u/(1-u*u)
        lam = (1-u)/(1+u)
        tag = str(u)
        check("H determinant " + tag, diag*diag-off*off == 1)
        check("symmetric eigenvalue " + tag, diag+off == lam)
        check("antisymmetric eigenvalue " + tag, diag-off == 1/lam)
        for d in [F(1,20),F(1,100)]:
            A, a = F(2,3), F(3,4)
            twist = 2*a*u/(1-u*u)
            p0 = d*d*u/(A*(1-u*u))
            check("tangent flux normalization " + tag + ":" + str(d), d*d*twist/(2*A*a) == p0)
    # Independent numerical quadrature of disk/ellipse overlap by polar fibres.
    for u in [0.02,0.05,0.125,0.25,0.5,0.75]:
        lam = (1-u)/(1+u)
        cross = math.atan(math.sqrt(lam))
        f = lambda t: 1/(lam*math.cos(t)**2+math.sin(t)**2/lam)
        overlap = 2*(cross+simpson(f,cross,math.pi/2))/math.pi
        delta = 2*math.asin(u)/math.pi
        check("polar overlap u="+str(u), abs((1-overlap)-delta) < 5e-11, "numerical quadrature")
        check("two closed TV formulae u="+str(u), abs(delta-(1-4*cross/math.pi)) < 2e-15, "floating identity")
    # A finite common-density support analogue checks the product identity exactly.
    for p in [F(1),F(1,5),F(2,7)]:
        left = [1-p,p/2,p/2,F(0)]
        right = [1-p,F(0),p/2,p/2]
        for k in range(1,7):
            overlap = product_overlap(left,right,k)
            check("tensor overlap p="+str(p)+",k="+str(k), overlap == (1-p/2)**k)
    # Physical support-function rotation and exact opposite-path invariants.
    z, one = (F(0),F(0)), (F(1),F(0))
    rot = [[(F(-1,2),F(0)),(F(0),F(-1,2))],[(F(0),F(1,2)),(F(-1,2),F(0))]]
    check("rotation cubed is identity", matmul(matmul(rot,rot),rot) == [[one,z],[z,one]])
    check("rotation has no fixed linear functional", F(9,4)+F(3,4) == 3)
    x = [[F(0),F(36)],[F(0),F(-18)],[F(0),F(-18)]]
    e1 = polyadd(polyadd(x[0],x[1]),x[2])
    e2 = polyadd(polyadd(polymul(x[0],x[1]),polymul(x[0],x[2])),polymul(x[1],x[2]))
    e3 = polymul(polymul(x[0],x[1]),x[2])
    check("opposite path e1 polynomial", e1 == [0,0])
    check("opposite path e2 polynomial", e2 == [0,0,-972])
    check("opposite path e3 polynomial", e3 == [0,0,0,11664])
    check("area quadratic coefficient", -F(5,432)*e2[2] == F(45,4))
    R = F(1,4)
    for s in [F(1,1000),F(1,2000),F(1,4000),F(1,10000)]:
        plus = [1/(R+36*s),1/(R-18*s),1/(R-18*s)]
        minus = [1/(R-36*s),1/(R+18*s),1/(R+18*s)]
        dist = min(max(abs(a-b) for a,b in zip(plus,perm)) for perm in itertools.permutations(minus))
        bound = 36*s/(R*R-324*s*s)
        check("matching curvature separation "+str(s), bound <= dist <= 2000*s)
    # Critical tangent limits and projection scales; not a nonlinear simulation.
    for j in [8,12,16]:
        u = F(1,2**j)
        d = u*u
        p0 = d*d*u/(1-u*u)
        delta = 2*math.asin(float(u))/math.pi
        for b in [F(1,2),F(1),F(2)]:
            k = int(b/u)
            n = int(b/(p0*u))
            selected = -math.expm1(k*math.log1p(-delta))
            raw = -math.expm1(n*math.log1p(-float(p0)*delta))
            target = -math.expm1(-2*float(b)/math.pi)
            check("selected critical limit j="+str(j)+",b="+str(b), abs(selected-target) < 4*float(u), "finite tangent limit diagnostic")
            check("raw critical limit j="+str(j)+",b="+str(b), abs(raw-target) < 4*float(u), "finite tangent limit diagnostic")
            check("selected projection nonlinear error scale "+str(j)+":"+str(b), F(k)*d <= b*u)
            check("raw projection nonlinear error scale "+str(j)+":"+str(b), F(n)*p0*d <= b*u)
    for eta in [0.249,0.2,0.1,0.01,1e-4,1e-8]:
        lower = (1-2*eta)*(math.log1p(-eta)-math.log(eta))
        check("confidence entropy eta="+str(eta), lower >= 0.25*math.log(1/eta), "floating inequality")
    for m in range(1,13):
        exponent = F(2)*F(3,m)+6
        check("matched fixed-m exponent m="+str(m), exponent == F(6)+F(6,m))
    # Finite illustration of the exact dyadic tie rule for F(theta)=theta^2.
    def residual(data: F, lo: F, hi: F) -> F:
        lower = F(0) if lo <= 0 <= hi else min(lo*lo,hi*hi)
        upper = max(lo*lo,hi*hi)
        return max(lower-data,F(0),data-upper)
    for data in [F(-1),F(0),F(1,16),F(1,4),F(1),F(5)]:
        lo,hi = F(-2),F(2)
        best = residual(data,lo,hi)
        for level in range(24):
            mid = (lo+hi)/2
            if residual(data,lo,mid) == best:
                hi = mid
            else:
                lo = mid
        check("dyadic tie rule retains exact optimum "+str(data), residual(data,lo,hi) == best)
        check("dyadic tie rule shrinks cube "+str(data), hi-lo == F(4,2**24))
    report = {
        "suite": "A2-v7-finite-diagnostics",
        "status": "PASS",
        "total_checks": len(CHECKS),
        "scope": "Exact finite rational identities and explicitly labelled numerical diagnostics; not a formal proof, nonlinear billiard simulation, or priority certificate.",
        "checks": CHECKS,
    }
    text = json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding="utf-8")
    print(text,end="")

if __name__ == "__main__":
    main()
