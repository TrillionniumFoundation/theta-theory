#!/usr/bin/env python3
"""Finite rational diagnostics for A2 v16; not a mathematical proof certificate.

No numerical integration, author v15 checker, external package or assert is used.
The moment implementation computes action and twist contributions separately.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

CHECKS: Counter[str] = Counter()


def require(condition: bool, group: str) -> None:
    if not condition:
        raise RuntimeError(f"Failed diagnostic: {group}")
    CHECKS[group] += 1


def det(a: list[list[F]]) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv(a: list[list[F]]) -> list[list[F]]:
    d = det(a)
    if not d:
        raise ValueError("singular matrix")
    return [[a[1][1]/d, -a[0][1]/d], [-a[1][0]/d, a[0][0]/d]]


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum(a[i][k]*b[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]


def unweighted(m: int, nu: F) -> F:
    return F(2*math.factorial(2*m), 2**m*math.factorial(m)**2*(m+1))*nu**m


def residual(m: int, nu: F) -> F:
    return F(2*math.comb(2*m, m), 2**m*(m+1)*(m+2))*nu**m


def series_mul(a: list[F], b: list[F], n: int) -> list[F]:
    return [sum(a[j]*b[k-j] for j in range(k+1)) for k in range(n+1)]


def series_power(a: list[F], n: int, exponent: F) -> list[F]:
    """(1+a)^exponent for a[0]=0 in the finite polynomial quotient."""
    if a[0]:
        raise ValueError("series requires zero constant term")
    out, power = [F(1)]+[F(0)]*n, [F(1)]+[F(0)]*n
    coefficient = F(1)
    for j in range(1, n+1):
        power = series_mul(power, a, n)
        coefficient *= (exponent-j+1)/j
        out = [x+coefficient*y for x,y in zip(out,power)]
    return out


def geometric_checks() -> None:
    grid = itertools.product([F(1,2), F(1), F(5,3)],
                             [F(3,2), F(2), F(5,2), F(3)], repeat=1)
    for g, c0 in grid:
        for c1 in [F(3,2), F(2), F(5,2), F(3)]:
            c = [c0, c1]; z = c0*c1-1; R = 1+2*z
            L = [g/(2*x*z) for x in c]
            for b in (0,1):
                co, cb = c[1-b], c[b]
                H = [[(cb-1/(2*co))/g, -1/(2*co*g)],
                     [-1/(2*co*g), (cb-1/(2*co))/g]]
                HI = inv(H)
                expected = [[L[b]*R,L[b]], [L[b],L[b]*R]]
                require(HI == expected, "quadratic_inverse")
                beta = (HI[0][0]+HI[1][1]-2*HI[0][1])/3
                plus = (HI[0][0]+HI[1][1]+2*HI[0][1])/3
                require(beta == 2*g/(3*cb), "intrinsic_difference_calibration")
                require(plus == 2*g/(3*(cb-1/co)), "sum_moment_compatibility")
                require(2/(3*beta)-1/g == (cb-1)/g, "curvature_recovery")
                for r in range(3,20):
                    if r % 2 == 0:
                        m=r//2
                        km=F(4, 2**m*(m+1)*math.factorial(m)**2)
                        own=-2*unweighted(m,L[b]*R)/math.factorial(r)
                        action=-2*unweighted(m,L[1-b])/math.factorial(r)
                        twist=-(g/co)*residual(m-1,L[1-b])/math.factorial(r-2)
                        wanted=[-km*L[b]**m*R**m,
                                -km*L[1-b]**m*(1+2*m*z)]
                    else:
                        m=(r-1)//2
                        Cm=F(4, 2**m*(m+1)*(m+2)*math.factorial(m)**2)
                        nu=L[b]*R; covariance=2*cb*co*L[b]
                        own=-2*covariance/nu*unweighted(m+1,nu)/math.factorial(r)
                        action=-4*co*unweighted(m+1,L[1-b])/math.factorial(r)
                        twist=-2*g*residual(m,L[1-b])/math.factorial(r-2)
                        wanted=[-2*cb*co*Cm*L[b]**(m+1)*R**m,
                                -2*co*Cm*L[1-b]**(m+1)*(1+2*m*z)]
                    require(own == wanted[0], "highest_block_own_entry")
                    require(action+twist == wanted[1], "highest_block_opposite_entry")
                    if r % 2 == 0:
                        require(R**m > 1+2*m*z, "even_separation")
                    else:
                        require(c0*c1*R**(2*m)-(1+2*m*z)**2 >= z*(1+2*m*z)**2 > 0,
                                "odd_separation")
            # alpha divided out: use the logarithmic last derivative to avoid radicals.
            for area in [F(1),F(7,2),F(11)]:
                diagonal_product=2*(-2*g*g/(3*c0*c0))*(-2*g*g/(3*c1*c1))*(-1/area)
                require(diagonal_product == -8*g**4/(9*area*c0*c0*c1*c1),
                        "leading_jacobian_divided_by_alpha")
                alpha_squared=1/(16*area**2*c0*c1*z)
                require(1/(16*alpha_squared*c0*c1*z) == area**2,
                        "free_area_recovery_squared")


def arclength_checks() -> None:
    # Nonzero lower odd and even jets: compute psi'/sqrt(1+psi'^2)
    # directly as a truncated series, independently of the displayed expansion.
    for seed in range(1,5):
        for r in range(3,14):
            n=r+3; p=[F(0)]*(n+1); kappa=F(seed+1,seed)
            p[1]=kappa
            for j in range(2,n+1):
                p[j]=F((-1)**(j+seed)*(seed+j), math.factorial(j))
            square=series_mul(p,p,n)
            reciprocal=series_power(square,n,F(-1,2))
            amplitude=series_mul(p,reciprocal,n)
            derivative=[F(0)]*(n+1)
            for j in range(n-r+2):
                degree=j+r
                if degree <= n:
                    derivative[degree]=amplitude[j]/(math.factorial(r-1)*degree)
            require(all(x == 0 for x in derivative[:r+1]), "arc_variation_lower_vanishing")
            require(derivative[r+1] == kappa/F((r+1)*math.factorial(r-1)),
                    "arc_variation_first_coefficient")
            sqrt=series_power(square,n,F(1,2))
            require(sqrt[2]/3 == kappa**2/6, "arc_cubic_coefficient")
            require(sqrt[3]/4 == kappa*p[2]/4, "arc_lower_asymmetric_coefficient")


def network_checks() -> None:
    # Distinct nonunimodular bases ensure no hidden determinant-one assumption.
    labels=[[[F(1),F(0)],[F(0),F(1)]],
            [[F(2),F(1)],[F(0),F(3)]],
            [[F(-1),F(2)],[F(2),F(1)]]]
    for shear in [F(-1,5),F(0),F(1,7),F(1,3)]:
        lattice=[[F(3),shear],[F(0),F(4)]]
        for marking in labels:
            displacement=mul(lattice,marking)
            require(mul(displacement,inv(marking)) == lattice, "rank_two_lattice_recovery")
        require(det(lattice)==12, "shear_fixed_covolume")
        require(lattice[0][0]==3 and lattice[1][0]==0, "shear_fixed_observed_period")
        if shear:
            require(16+shear**2>16, "shear_nonisometry_control")
    # Gauge removal along a 3-vertex spanning tree, and two independent cycles.
    tau=[(0,0),(2,1),(1,3)]
    edges=[(0,1,(2,1)),(1,2,(-1,2)),(2,0,(0,-3)),(2,0,(-1,-1))]
    transformed=[(k[0]+tau[v][0]-tau[w][0], k[1]+tau[v][1]-tau[w][1])
                 for v,w,k in edges]
    require(transformed[:2]==[(0,0),(0,0)], "tree_gauge_zero")
    require(transformed[2:]==[(1,0),(0,2)], "fundamental_cycle_labels")
    singular=[[F(1),F(2)],[F(0),F(0)]]
    try:
        inv(singular)
    except ValueError:
        CHECKS["rank_one_rejected"] += 1
    else:
        raise RuntimeError("rank-one matrix was accepted")


def structural_checks() -> None:
    for K in range(3,31):
        ne,no=K//2-1,(K-1)//2
        require(ne+no==K-2, "higher_jet_dimension")
        require(4+2*(ne+no)==2*K, "calibrated_dimension")
        if K%2==0:
            M=K//2
            require(2*(K-2)-2*(M-1)==2*M-2, "count_fiber_dimension")
    root=Path(__file__).resolve().parents[1]
    preserved={
        "core/02_local_law.tex":"ead6f0334962bf7c4c6768ed829b4f6069231ff7",
        "core/03_asymmetric_inverse.tex":"3f4443c109b2ebb698803d4af296cd61250bc8f2",
        "core/04_physical_observation.tex":"05f0342a86638594d25a75aaba112d6223b53b9f",
        "core/05_relative_laws.tex":"16888b97102aefcfd23c21eec12bad5902bffd02"}
    for path,expected in preserved.items():
        content=(root/path).read_bytes()
        actual=hashlib.sha1(f"blob {len(content)}\0".encode()+content).hexdigest()
        require(actual==expected, "retained_core_blob_identity")


def main() -> None:
    geometric_checks(); arclength_checks(); network_checks(); structural_checks()
    print(json.dumps({"schema":"a2-v16-finite-rational-diagnostics-1",
                      "status":"passed", "total_checks":sum(CHECKS.values()),
                      "checks":dict(sorted(CHECKS.items())),
                      "scope":"Finite algebra, arclength filtration diagnostics, lattice linear algebra, dimensions and retained source identity only",
                      "formal_proof_certificate":False},indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
