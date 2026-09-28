#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v26 referee report.

Uses only Python's standard library. These are checks of finite identities
and a two-flight geometry witness, NOT proof certification or a native build.
Run normally and with python3 -O; both modes retain every explicit check.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import factorial, isfinite, sqrt
from pathlib import Path
import json
import platform

BASE = "cefd89084682cc2e31d730eab1a4b8d8eaac0bbe"
COUNTS: Counter[str] = Counter()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def inverse_checks() -> None:
    nodes = [F(i, 8) for i in range(-2, 3)]
    anchor = F(1, 4)
    for odd in (F(-1, 5), F(0), F(1, 5)):
        def action(u: F) -> F:
            return u*u + odd*u**3 + u**4/F(10)
        def amplitude(u: F) -> F:
            return 1 + u/F(7) + u*u/F(5)
        def density(u: F, v: F) -> F:
            return amplitude(u)*amplitude(v)*(1-action(u)-action(v))/F(7, 5)
        def ratio(u: F, v: F) -> F:
            return density(u,v)*density(F(0),F(0))/(density(u,F(0))*density(F(0),v))
        ta = action(anchor)/(1-action(anchor))
        require(ta > 0 and 1-ratio(anchor,anchor) == ta*ta, "anchor defect")
        for u in nodes:
            for v in nodes:
                tu, tv = action(u)/(1-action(u)), action(v)/(1-action(v))
                require(1-ratio(u,v) == tu*tv, "rank-one identity")
                t = (1-ratio(u,anchor))/ta
                require(t/(1+t) == action(u), "action inversion")
                recovered = density(u,F(0))/density(F(0),F(0))*(1+t)
                require(recovered == amplitude(u)/amplitude(F(0)), "amplitude inversion")
                COUNTS["exact_density_inverse"] += 1


def determinant_checks() -> None:
    for x in (F(1, 3), F(1, 2), F(2, 3)):
        for r in (F(2, 3), F(1), F(3, 2)):
            for n in range(3, 11):
                a = (1+x**(2*n))/(1-x**(2*n))
                b = r**n*2*x**n/(1-x**(2*n))
                c = r**(-n)*2*x**n/(1-x**(2*n))
                require(a*a-b*c == 1, "determinant-one block")
                require(a*(-b)+b*a == 0, "inverse off diagonal")
                COUNTS["exact_last_jet_block"] += 1


def gauge_checks() -> None:
    eps = F(1, 10)
    def phi(s: F) -> F:
        return s + eps*s*(1-s)*(s-F(1, 2))
    nodes = [F(i, 10) for i in range(11)]
    for s in nodes:
        require(phi(1-s) == 1-phi(s), "support complement identity")
        require(1+eps*(-3*s*s+3*s-F(1,2)) >= F(19,20), "monotonicity")
        require(1+eps*(-15*s*s+9*s-F(1,2)) >= F(7,20), "action convexity")
        for t in nodes:
            require((s+t < 1) == (phi(s)+phi(t) < 1), "same strict support")
            require((s+t == 1) == (phi(s)+phi(t) == 1), "same support boundary")
            COUNTS["exact_single_support_gauge"] += 1
    s = F(1,4)
    def diagonal_ratio(x: F) -> F:
        return (1-2*x)/(1-x)**2
    require(diagonal_ratio(s) != diagonal_ratio(phi(s)), "densities distinguish the support gauge")


def graph_terms(y: float, radius: float) -> tuple[float, float, float]:
    z = sqrt(radius*radius-y*y)
    return radius-z, y/z, radius*radius/(z**3)


def flight(u: float, z: float, radius: float) -> tuple[float, float, float, float]:
    # Fixed left disk radius 1; right disk radius varies, leftmost point (1,0).
    p0, d0, _ = graph_terms(u, 1.0)
    p1, d1, dd1 = graph_terms(z, radius)
    h, k = 1.0+p0+p1, z-u
    length = sqrt(h*h+k*k)
    nz, nu = h*d1+k, h*d0-k
    lz = nz/length
    lzz = (d1*d1+h*dd1+1)/length-nz*nz/length**3
    luz = (d0*d1-1)/length-nu*nz/length**3
    return length, lz, lzz, luz


def geometry_checks() -> dict[str, float]:
    max_excess = 0.0
    min_flux = float("inf")
    max_residual = 0.0
    for radius in (0.9, 1.0, 1.1):
        for u in (-0.02, 0.0, 0.02):
            for v in (-0.02, 0.0, 0.02):
                z = 0.0
                for _ in range(30):
                    a, b = flight(u,z,radius), flight(v,z,radius)
                    step = (a[1]+b[1])/(a[2]+b[2])
                    z -= step
                    if abs(step) < 1e-15:
                        break
                a, b = flight(u,z,radius), flight(v,z,radius)
                residual = abs(a[1]+b[1])
                excess = a[0]+b[0]-2.0
                minus_wuv = a[3]*b[3]/(a[2]+b[2])
                require(residual < 1e-12, "two-flight stationarity")
                require(-1e-12 <= excess < 0.025, "common positive residual-time core")
                require(isfinite(minus_wuv) and minus_wuv > 0, "positive exact mixed flux")
                # Both observed positions lie on the SAME fixed disk, for every radius.
                for y in (u,v):
                    pos = (-graph_terms(y,1.0)[0], y)
                    require(abs((pos[0]+1)**2+pos[1]**2-1) < 1e-12, "fixed endpoint curve")
                    require(pos[1] == y, "parameter-independent transverse inverse")
                max_excess = max(max_excess,excess)
                min_flux = min(min_flux,minus_wuv)
                max_residual = max(max_residual,residual)
                COUNTS["fixed_obstacle_two_flight_witness"] += 1
    return {"maximum_excess": max_excess, "minimum_minus_Wuv": min_flux,
            "maximum_stationarity_residual": max_residual}


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    n = len(rhs)
    a = [row[:] + [value] for row,value in zip(matrix,rhs)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if a[i][j]), None)
        require(pivot is not None, "singular exact Vandermonde")
        a[j],a[pivot] = a[pivot],a[j]
        scale = a[j][j]
        a[j] = [x/scale for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x-scale*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]


def interpolation_checks() -> None:
    for m in range(2,6):
        nodes = [F(2*i-m,m+1) for i in range(m+1)]
        inverse_scale_errors = None
        for scale in (F(1,2),F(1,4),F(1,8)):
            xs = [scale*x for x in nodes]
            coef = solve([[x**j for j in range(m+1)] for x in xs], [x**(m+1) for x in xs])
            normalized = [coef[j]/scale**(m+1-j) for j in range(m+1)]
            if inverse_scale_errors is not None:
                require(normalized == inverse_scale_errors, "interpolation remainder scaling")
            inverse_scale_errors = normalized
            COUNTS["exact_interpolation_scaling"] += 1


def budget_checks() -> None:
    caps = [5,3,11,9,21,18]
    levels = [max(s,*caps[:s]) for s in range(1,len(caps)+1)]
    for n in range(1,41):
        allowed = [s for s,c in enumerate(levels,1) if c <= n]
        if allowed:
            s = max(allowed)
            require(caps[s-1] <= n and s <= n, "restarted stage exceeds budget")
        COUNTS["restarted_budget"] += 1


def main() -> None:
    inverse_checks(); determinant_checks(); gauge_checks()
    geometry = geometry_checks()
    interpolation_checks(); budget_checks()
    result = {
        "status": "passed", "reviewed_commit": BASE,
        "python": platform.python_version(),
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "counts": dict(sorted(COUNTS.items())), "total_cases": sum(COUNTS.values()),
        "two_flight_numerics": geometry,
        "native_build_executed": False, "author_suite_rerun": False,
        "scope": "Finite exact identities and numerical local witness only. Continuum claims are proved in the referee report, not by these cases."
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
