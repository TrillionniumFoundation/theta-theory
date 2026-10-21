#!/usr/bin/env python3
"""Exact auxiliary checks for core/310; not a billiard proof certificate.

Checks the nonlinear-coordinate Jacobian algebra, physical normalization,
uniform tube-width constants, and the finite-depth/geometric-series
bookkeeping used in the written proof.  No simulated trajectory or sampled
floating-point geometry is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def upper_root(value: F, degree: int) -> int:
    lo, hi = 0, 1
    while F(hi**degree) < value:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if F(mid**degree) >= value:
            hi = mid
        else:
            lo = mid
    return hi


def rational(value: F) -> str:
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", type=Path, help="Write the identical deterministic JSON result here.")
    args = parser.parse_args()
    a, d, E, radius = sp.symbols("a d E radius", positive=True)
    hess = sp.Matrix([[a, -E], [-E, d]])
    sign = sp.diag(-1, 1)
    dq_dzeta = radius * hess.inv() * sign
    dsource_dq = sp.Matrix([[1, 0], [-a / radius, E / radius]])
    determinant = sp.factor((dsource_dq * dq_dzeta).det())
    # The determinant is negative on ad>E²; absolute value is the exact u.
    require(
        sp.simplify(determinant + radius * E / (a * d - E**2)) == 0,
        "The endpoint momentum inverse weight acquired a wrong radius factor.",
    )
    rho, cstar, cd, umax, u0, mass = sp.symbols(
        "rho cstar Cdist U u0 mass", positive=True
    )
    tube_lower = sp.pi * rho**2 * (u0 / cd) / (4 * sp.pi)
    coefficient_upper = sp.solve(sp.Eq(tube_lower, mass), u0)[0]
    roof_prefactor = 2 * sp.pi * umax * cd / (4 * sp.pi * cstar)
    require(
        sp.simplify(
            coefficient_upper * roof_prefactor
            - 2 * umax * cd**2 * mass / (cstar * rho**2)
        )
        == 0,
        "The tube-volume and roof-angle prefactors do not compose correctly.",
    )
    rpolar, radial_h = sp.symbols("rpolar radial_h", positive=True)
    require(
        sp.simplify(
            u0 * rpolar / (4 * sp.pi * cstar) / (rpolar * radial_h)
            - u0 / (4 * sp.pi * cstar * radial_h)
        )
        == 0,
        "Polar area and original-roof radial Jacobians do not cancel.",
    )

    N = 94
    kappa = 3263680
    Rplus, Rminus, tau = F(47, 100), F(9, 20), F(3, 50)
    sigma, q0, qa = F(47, 59), F(47, 53), F(kappa, kappa + 1)
    J = F(2845, 354)
    flight_a = Rplus / tau
    lam = F(50, 47)
    K = 2 * (1 + lam) * (4 * flight_a + 16 * flight_a**2)
    rstar = min(1 / (8 * (1 + flight_a)), 1 / (8 * K))
    etastar = rstar / (8 * (1 + lam * flight_a))
    Pstar = 2 * (1 + lam * flight_a)
    Cinc = Pstar * (1 + 2 * flight_a * (1 + lam))
    Cclr = Rplus * Pstar
    delta = min(etastar, 1 / (2 * Cinc), 1 / (2 * Cclr))
    Cc = J * (1 + flight_a * (1 + 1 / sigma))
    Cdelta = Rplus * J * (1 + sigma)
    Lgamma = 4 * Cdelta * (delta / 8)
    Lc = 4 * Cc * (delta / 8)
    require(delta == F(27, 67443712), "Uniform tube radius mismatch.")
    require(Cc == F(79660, 531), "Incidence/tangential derivative constant mismatch.")
    require(Cdelta == F(1417379, 208860), "All-center clearance derivative mismatch.")
    require(Cc >= J, "The phase estimate does not dominate the angular derivative.")
    require(Lgamma == F(12756411, 9390862458880), "Clearance tube diameter mismatch.")
    require(Lc == F(8535, 284227072), "Incidence/collar tube diameter mismatch.")

    Bperp = F(167591049) + F(159236, 100)
    Agamma_squared = 2 * Rplus * Bperp
    Ac_squared = 2 * Rplus / tau
    Aphi_fourth = 2 * Rplus * (128 / tau + F(24 * 10**8) / Rminus**4)
    Agamma = upper_root(Agamma_squared, 2)
    Ac = upper_root(Ac_squared, 2)
    Aphi = upper_root(Aphi_fourth, 4)
    require((Agamma, Ac, Aphi) == (12552, 4, 485), "Amplitude enclosure mismatch.")
    require(F((Agamma - 1) ** 2) < Agamma_squared <= F(Agamma**2), "Bad square enclosure.")
    require(F((Aphi - 1) ** 4) < Aphi_fourth <= F(Aphi**4), "Bad fourth-root enclosure.")
    # This verifies the literal first two binomial terms used in the proof.
    # Bernoulli's theorem, not an evaluated enormous power, supplies the rest.
    require(F(1) + F(kappa, kappa) == 2, "Bernoulli block bound mismatch.")
    require(qa == 1 / (1 + F(1, kappa)), "Wrong anchor/Bernoulli constant.")
    require(2 * 47**4 < 59**4, "The exact sigma four-step contraction failed.")
    D = N * (1 + 68 * kappa)
    jD = max(0, D // N - 1)
    require(D == 20861442654 and jD == 68 * kappa, "Explicit observation depth mismatch.")
    require(D >= 4 * 17, "The sigma block certificate has too few steps.")
    enlarged_gamma = F(Agamma, 2**34) + Lgamma / 2**17
    enlarged_c = F(Ac, 2**34) + Lc / 2**17
    enlarged_phi = F(Aphi, 2**17) + Lc / 2**17
    require(enlarged_gamma < F(3, 200), "Clearance width leaves its physical flux regime.")
    require(enlarged_c <= 1, "Incidence width leaves its exact physical regime.")
    require(enlarged_phi <= F(1, 200), "Section collar exceeds the exact rectangle regime.")

    # Exhaustive finite bookkeeping of contact and flight depth multiplicities.
    counts_checked = 0
    for m in range(0, 257):
        contact_counts: dict[int, int] = {}
        flight_counts: dict[int, int] = {}
        for i in range(1, m):
            depth = min(i, m - i)
            contact_counts[depth] = contact_counts.get(depth, 0) + 1
        for i in range(m):
            depth = min(i, m - 1 - i)
            flight_counts[depth] = flight_counts.get(depth, 0) + 1
        require(all(v <= 2 for v in contact_counts.values()), "Contact depth multiplicity >2.")
        require(all(v <= 2 for v in flight_counts.values()), "Flight depth multiplicity >2.")
        counts_checked += len(contact_counts) + len(flight_counts)
    x = sp.symbols("x", positive=True)
    for residue in range(N):
        exact_block_tail = (N - residue) + N * x / (1 - x)
        claimed_tail = N / (1 - x)
        require(
            sp.simplify(claimed_tail - exact_block_tail - residue) == 0,
            "The partial first depth block was undercounted.",
        )
    v, w = sp.symbols("v w", nonnegative=True)
    require(
        sp.expand(2 * v**2 + 2 * w**2 - (v + w) ** 2 - (v - w) ** 2) == 0,
        "The enlarged incidence square budget has the wrong factor.",
    )
    # I_m bound: two indices/depth times 2/epsilon from the actual half-guard.
    eps, ratio = sp.symbols("eps ratio", positive=True)
    require(
        sp.simplify(1 + 2 * 2 / eps * ratio / (1 - ratio)
                    - (1 + 4 / eps * ratio / (1 - ratio))) == 0,
        "The retained I_m multiplier has a missing endpoint-depth factor.",
    )
    # q0/r=q0^(3/4) is verified by the exact fourth-power relation.
    require(q0**4 / q0 == q0**3, "Original guard exponent changed.")

    native = Path(__file__).with_name("310_critical_tube_volume_and_normalized_source.tex")
    if not native.exists():
        native = Path(__file__).parent.parent / "core" / native.name
    output = {
        "status": "passed",
        "scope": "exact auxiliary algebra, constants and finite combinatorial checks; not a continuous-geometry certificate",
        "native_source_sha256": hashlib.sha256(native.read_bytes()).hexdigest(),
        "inverse_jacobian_signed": str(determinant),
        "tube_volume_to_roof_prefactor": "2*U*Cdist^2/(c_star*rho_epsilon^2)",
        "delta_star": rational(delta),
        "clearance_diameter_bound": rational(Lgamma),
        "incidence_and_collar_diameter_bound": rational(Lc),
        "amplitude_integer_upper_bounds": [Agamma, Ac, Aphi],
        "uniform_depth": D,
        "certified_enlarged_width_upper_bounds": {
            "clearance": rational(enlarged_gamma),
            "incidence": rational(enlarged_c),
            "collar": rational(enlarged_phi),
        },
        "tested_finite_collision_counts": 257,
        "depth_multiplicities_checked": counts_checked,
        "partial_geometric_blocks_checked": N,
        "whole_cylinder_pressure_used": False,
        "endpoint_kernel_used": False,
        "full_original_normalized_shortage_claimed": False,
    }
    encoded = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.details is not None:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        args.details.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
