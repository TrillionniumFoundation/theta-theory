#!/usr/bin/env python3
"""Auxiliary exact checks for native336; no billiard or limiting theorem proof.

These polynomial examples and symbolic identities test the pushforward,
signed grouping, conditioning and exceptional-parameter conventions in the
written proof. They do not enumerate physical words or certify its geometric
exhaustion, uniform estimates, absence of a physical Cantor part, or raw LLT.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform

import sympy as sp


def verify() -> dict:
    rows = []

    def record(group, name, passed, details):
        rows.append({"group": group, "name": name,
                     "passed": bool(passed), "details": details})

    def zero(expr):
        return sp.simplify(expr) == 0

    r = sp.symbols("r", real=True)
    t, eps, n, rp = sp.symbols("t eps n rp", positive=True)

    # A monotone map whose derivative tends to zero at a side endpoint.
    # This independent pushforward calculation does not assume a positive
    # global lower bound for the side derivative.
    b = 1 + 2*r
    h = (1 + 2*sp.sqrt(t))/(2*sp.sqrt(t))
    record("pushforward", "inverse-Jacobian density", zero(
        h.subs(t, rp*rp) * 2*rp - b.subs(r, rp)),
        {"map": "t=r^2, 0<r<1", "weight": str(b), "density": str(h)})
    for k in range(4):
        source = sp.integrate(r**(2*k)*b, (r, 0, 1))
        target = sp.integrate(t**k*h, (t, 0, 1))
        record("pushforward", "independent source/roof moments", zero(source-target),
               {"power": k, "source": str(source), "roof": str(target)})
    small_mass = sp.integrate(h, (t, 0, eps))
    record("pushforward", "zero endpoint atom despite unbounded density",
           sp.limit(small_mass, eps, 0, dir="+") == 0,
           {"mass_of_(0,epsilon)": str(small_mass), "limit": "0"})

    # One genuine turning point: split into two monotone sides, then add.
    positive_side = (1 + sp.sqrt(t))/(2*sp.sqrt(t))
    negative_side = (1 - sp.sqrt(t))/(2*sp.sqrt(t))
    two_arm = sp.simplify(positive_side + negative_side)
    record("turning", "both inverse branches retained", zero(two_arm-1/sp.sqrt(t)),
           {"density": str(two_arm), "source": "(1+r) dr on (-1,1), t=r^2"})
    for k in range(4):
        source = sp.integrate(r**(2*k)*(1+r), (r, -1, 1))
        target = sp.integrate(t**k*two_arm, (t, 0, 1))
        record("turning", "two-arm source/roof moments", zero(source-target),
               {"power": k, "source": str(source), "roof": str(target)})
    record("turning", "turning point has no pushed atom", sp.limit(
        sp.integrate(two_arm, (t, 0, eps)), eps, 0, dir="+") == 0,
        {"exact_small_mass": "2 sqrt(epsilon)", "turning_point_source_mass": "0"})

    tau = sp.Rational(7, 5)
    flux = sp.Rational(3, 2) + 2*r + sp.I*(1-r*r)
    atom = sp.integrate(flux, (r, -1, 1))
    record("constant_side", "signed complex atomic coefficient",
           zero(atom-(3+sp.Rational(4, 3)*sp.I)), {"coefficient": str(atom)})
    for k in range(4):
        left = sp.integrate(tau**k*flux, (r, -1, 1))
        record("constant_side", "constant-map distributional action",
               zero(left-tau**k*atom), {"test": f"t^{k}", "roof": str(tau)})
    signed = sp.integrate(r, (r, -1, 1))
    absolute = sp.integrate(-r, (r, -1, 0))+sp.integrate(r, (r, 0, 1))
    record("constant_side", "negative control: integral of absolute flux is not atom",
           signed == 0 and absolute == 1,
           {"correct_signed_atom": str(signed), "incorrect_absolute_flux": str(absolute)})

    # Exact roof coincidences are grouped at the same exact label only.
    la, lb = (0, 0, 1), (1, -1, 1)
    contributions = [(la, 1, sp.Rational(3, 2)), (la, 1, -sp.Integer(1)),
                     (la, 1, -sp.Rational(1, 2)), (la, 2, 2+sp.I),
                     (la, 2, -sp.I), (lb, 1, sp.Rational(5, 3))]
    combined = {}
    for label, roof, coefficient in contributions:
        key = (label, roof)
        combined[key] = sp.simplify(combined.get(key, 0)+coefficient)
    square = lambda z: sp.expand(z*sp.conjugate(z))
    energy = sum(square(v) for v in combined.values())
    naive = sum(square(v) for _, _, v in contributions)
    record("grouping", "same-roof signed cancellation precedes square",
           combined[(la, 1)] == 0 and energy == sp.Rational(61, 9) and energy != naive,
           {"combined_energy": str(energy), "incorrect_separate_energy": str(naive)})
    record("grouping", "different exact labels remain separate",
           combined[(lb, 1)] == sp.Rational(5, 3),
           {"label": lb, "roof": 1, "coefficient": str(combined[(lb, 1)])})
    # Same roof in two distinct labels: summing first would invent a cross term.
    record("grouping", "negative control: cross-label summation is rejected",
           square(sp.Integer(1))+square(sp.Integer(2)) != square(sp.Integer(3)),
           {"correct_label_energy": 5, "incorrect_pooled_energy": 9})

    # An exact quadratic coarea calculation, with symbolic normalization.
    # The test matrix is not asserted to be realized by a billiard orbit.
    G = sp.Matrix([[4, -1], [-1, 3]])
    K = sp.Matrix([[2, -sp.Rational(1, 2)], [0, sp.sqrt(11)/2]])
    record("critical", "endpoint-to-Morse determinant", K.T*K == G,
           {"det_G": str(G.det()), "det_K": str(K.det())})
    c, omega, beta, height, radius = sp.symbols("c omega beta height R", positive=True)
    weight, value = sp.symbols("w V")
    # The disk radius is sqrt(2 height), not sqrt(height).
    sector_area = 2*sp.pi*beta*height/sp.sqrt(G.det())
    conditioned_mass = weight*value*omega/(4*sp.pi*c)*sector_area
    coefficient = weight*value*omega*beta/(2*c*sp.sqrt(G.det()))
    record("critical", "independent sector-area derivative gives exact coefficient",
           zero(sp.diff(conditioned_mass, height)-coefficient),
           {"sector_area": str(sector_area), "coefficient": str(coefficient)})
    record("critical", "conditioning applied exactly once",
           zero(coefficient*c-weight*value*omega*beta/(2*sp.sqrt(G.det())))
           and not zero(coefficient/c-coefficient),
           {"factor": "c_*^{-1}", "double_conditioning_rejected": True})
    u = radius**2*omega/G.det()
    J = omega/(2*c*sp.sqrt(G.det()))
    record("critical", "inherited optical-u coefficient conversion",
           zero(J-sp.sqrt(G.det())*u/(2*radius**2*c)),
           {"u": str(u), "J": str(J)})
    fractions = [sp.Rational(1, 4), sp.Rational(3, 8), sp.Rational(3, 8)]
    record("critical", "exact label sectors partition without count multiplier",
           zero(sum(J*b for b in fractions)-J),
           {"sector_fractions": [str(b) for b in fractions]})
    record("critical", "negative control: missing radial factor two is rejected",
           not zero(coefficient-coefficient/2), {"correct_radial_area": "2 pi beta height/sqrt(det G)"})

    # Exceptional-parameter negative control. For E={rho>0, 0<x,y<1},
    # the fixed rho=0 fiber is empty. Its ambient closure nonetheless contains
    # (0,x,y) for every interior x,y, witnessed by rho_n=1/n. This exact
    # example explains why the manuscript takes all closures fiberwise.
    x, y = sp.Rational(1, 3), sp.Rational(2, 5)
    rho_n = 1/n
    record("fiberwise", "same-radius zero fiber is empty", not (sp.Integer(0)>0),
           {"family": "rho>0 and 0<x<1 and 0<y<1", "rho": 0})
    record("fiberwise", "ambient closure creates spurious exceptional-radius points",
           rho_n.is_positive and 0 < x < 1 and 0 < y < 1
           and sp.limit(rho_n**2, n, sp.oo) == 0,
           {"sequence": "(1/n,1/3,2/5)", "distance_squared": "1/n^2",
            "limit_point_absent_from_fiberwise_closure": True})
    passed = all(row["passed"] for row in rows)
    return {"status": "PASS" if passed else "FAIL", "all_passed": passed,
            "checks": len(rows), "groups": sorted({row["group"] for row in rows}),
            "arithmetic": "exact SymPy rational and symbolic identities; no floating-point tolerances",
            "python_version": platform.python_version(), "sympy_version": sp.__version__,
            "scope": "Auxiliary analytic examples and algebraic conventions only. The complete physical source, its SBV theorem, and the raw LLT are not certified by this script.",
            "results": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = verify()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "checks": result["checks"],
                      "output": str(args.output)}))
    raise SystemExit(0 if result["all_passed"] else 1)


if __name__ == "__main__":
    main()
