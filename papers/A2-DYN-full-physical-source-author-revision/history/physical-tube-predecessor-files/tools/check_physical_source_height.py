#!/usr/bin/env python3
"""Exact auxiliary checks for the continuous proofs in modules 311--313.

The written proof, rather than a finite grid sample, establishes physical
continuation, all-source coverage, and continuous overlap.  This program
independently checks their algebra, rational margins, finite index rules,
and original-source normalization.  No floating-point trajectory is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

import sympy as sp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def fs(value: F) -> str:
    return f"{value.numerator}/{value.denominator}"


def sha_native(name: str) -> str:
    here = Path(__file__).resolve().parent
    for candidate in (here / name, here.parent / "core" / name):
        if candidate.exists():
            return hashlib.sha256(candidate.read_bytes()).hexdigest()
    raise RuntimeError(f"Native proof source missing: {name}")


def physical_constants() -> dict:
    Rplus, Rminus, tau = F(47, 100), F(9, 20), F(3, 50)
    q0, qa, sigma = F(47, 53), F(3263680, 3263681), F(47, 59)
    aa, lam = Rplus / tau, F(50, 47)
    K = 2 * (1 + lam) * (4 * aa + 16 * aa**2)
    rstar = min(1 / (8 * (1 + aa)), 1 / (8 * K))
    etastar = rstar / (8 * (1 + lam * aa))
    Pstar = 2 * (1 + lam * aa)
    Cinc = Pstar * (1 + 2 * aa * (1 + lam))
    Cclr = Rplus * Pstar
    delta = min(etastar, 1 / (2 * Cinc), 1 / (2 * Cclr))
    J = F(2845, 354)
    Cc = J * (1 + aa * (1 + 1 / sigma))
    Cdelta = Rplus * J * (1 + sigma)
    g, U = F(9, 40), F(320, 9)
    require(delta == F(27, 67443712), "Inherited analytic/physical radius changed.")
    require(F(10600, 12809) + F(1, 200) < F(5, 6), "The section cap is not covered.")
    require(F(5, 6) + F(1, 64) == F(163, 192) < F(17, 20), "No spare endpoint cap.")
    require(1 - F(17, 20) ** 2 == F(111, 400) > F(1, 4), "Endpoint incidence below half.")
    require(Rminus / 2 == g, "Strong-convexity lower bound has wrong units.")
    require(Cinc * delta <= F(1, 2), "Tangential continuation bound lacks half-margin.")
    require(F(1, 4) / 16 == F(1, 64), "Worst endpoint momentum increment miscomputed.")
    # All expressions below are ratios to epsilon or a_epsilon; epsilon stays fixed.
    a_per_epsilon = delta / 16
    rho_per_epsilon = g * a_per_epsilon / (8 * Rplus)
    require(2 * a_per_epsilon == delta / 8 < delta, "Physical endpoint ball exceeds tube.")
    require(Rplus * (4 * rho_per_epsilon) / g == a_per_epsilon / 2,
            "The full inverse disk leaves its physical endpoint ball.")
    require(g * a_per_epsilon**2 - Rplus * 4 * rho_per_epsilon * a_per_epsilon
            == g * a_per_epsilon**2 / 2 > 0,
            "Desired inverse momentum can have a boundary minimizer.")
    require(Rplus * 3 * rho_per_epsilon / g == 3 * a_per_epsilon / 8 < a_per_epsilon / 2,
            "Chosen grid or origin tube exceeds the inverse-ball estimate.")
    require(a_per_epsilon <= delta / 2, "Distortion exponent exceeds inherited C_dist.")
    require(a_per_epsilon / (delta / 2) == F(1, 8), "Atlas/critical endpoint radii mismatch.")
    require((2 * Cc * a_per_epsilon) / (4 * Cc * delta / 2) == F(1, 16),
            "Atlas collar widening exceeds critical-depth certificate.")
    require(0 < q0 < 1 and 0 < qa < 1 and 0 < sigma < 1, "Exponential rates not positive.")
    require(sigma**4 < q0, "Physical endpoint localization is slower than guard schedule.")
    require(F(28, 5) - tau == F(277, 50), "Original physical roof support width mismatch.")
    return {
        "R_minus": fs(Rminus), "R_plus": fs(Rplus), "tau_minus": fs(tau),
        "q0_unchanged": fs(q0), "q_anchor_unchanged": fs(qa), "sigma": fs(sigma),
        "delta_star": fs(delta), "C_inc": fs(Cinc), "C_c": fs(Cc),
        "C_Delta": fs(Cdelta), "g": fs(g), "U": fs(U),
        "a_epsilon_over_epsilon": fs(a_per_epsilon),
        "rho_epsilon_over_epsilon": fs(rho_per_epsilon),
        "full_physical_roof_support_length_over_m": "277/50",
    }


def grid_and_index_checks() -> dict:
    # Continuous covering proof: each coordinate can be rounded within 1/2.
    require(F(1, 2) ** 2 + F(1, 2) ** 2 < 1, "Nearest grid point not within rho.")
    # Continuous overlap proof: six distinct integers span at least five units,
    # exceeding any interval of length four.  Thus at most five/coordinate.
    require(F(6 - 1) > 4 and 5**2 == 25, "Interval proof of 25-fold overlap failed.")
    # Exact finite boundary illustrations of that proof on one periodic cell.
    translations = sorted({F(0), F(1), F(1, 2), F(1, 4), F(3, 4)}
                          | {F(i, 7) for i in range(8)})
    grid = [(i, j) for i in range(-3, 5) for j in range(-3, 5)]
    max_box = max_open = max_closed = 0
    for tx in translations:
        for ty in translations:
            box = sum(abs(F(i) - tx) <= 2 and abs(F(j) - ty) <= 2 for i, j in grid)
            opened = sum((F(i) - tx) ** 2 + (F(j) - ty) ** 2 < 4 for i, j in grid)
            closed = sum((F(i) - tx) ** 2 + (F(j) - ty) ** 2 <= 4 for i, j in grid)
            require(opened <= closed <= box <= 25, "A closed grid boundary violates overlap.")
            nearest_x = 0 if tx <= F(1, 2) else 1
            nearest_y = 0 if ty <= F(1, 2) else 1
            require((tx - nearest_x) ** 2 + (ty - nearest_y) ** 2 <= F(1, 2),
                    "Nearest-grid tie convention broke the cover.")
            max_box, max_open, max_closed = max(max_box, box), max(max_open, opened), max(max_closed, closed)
    index_cases = 0
    singleton_contacts = 0
    empty_ranges = 0
    for m in range(1, 257):
        dc: dict[int, int] = {}
        df: dict[int, int] = {}
        for i in range(1, m):
            di = min(i, m - i)
            dc[di] = dc.get(di, 0) + 1
        for i in range(m):
            dip = min(i, m - 1 - i)
            df[dip] = df.get(dip, 0) + 1
            require(min(min(i, m - i), min(i + 1, m - i - 1)) == dip,
                    "Flight depth omitted an adjacent contact.")
        require(max(dc.values(), default=0) <= 2 and max(df.values(), default=0) <= 2,
                "True depth count exceeds two.")
        for depth in range(m + 2):
            end = m - depth
            contacts = list(range(depth, end + 1))
            flights = list(range(depth, end))
            occupations = list(range(depth, end))
            require(len(contacts) == max(0, m - 2 * depth + 1), "Central contacts miscounted.")
            require(len(flights) == len(occupations) == max(0, m - 2 * depth),
                    "Occupation/flight half-open interval changed.")
            if depth == end:
                require(contacts == [depth] and not flights and not occupations,
                        "Singleton central contact or terminal test discarded.")
                singleton_contacts += 1
            if end < depth:
                require(not contacts and not flights and not occupations, "Nonempty reversed central range.")
                empty_ranges += 1
            index_cases += 1
    # Exact partial block tail for D=Nq+r with q>=1, r in {0,...,N-1}.
    x = sp.symbols("x", positive=True)
    for residue in range(94):
        require(sp.simplify(94 / (1 - x) - ((94 - residue) + 94 * x / (1 - x)) - residue) == 0,
                "Partially occupied first anchor block not correctly enlarged.")
    return {
        "continuous_overlap_argument": "six distinct integers span >=5>4; at most5 choices per coordinate",
        "continuous_nearest_grid_argument": "(1/2)^2+(1/2)^2=1/2<1",
        "finite_translation_pairs": len(translations) ** 2,
        "finite_max_closed_box_overlap": max_box,
        "finite_max_open_disk_overlap": max_open,
        "finite_max_closed_disk_overlap": max_closed,
        "finite_collision_counts": 256,
        "central_index_cases": index_cases,
        "retained_singleton_contacts": singleton_contacts,
        "empty_central_ranges": empty_ranges,
        "partial_anchor_blocks": 94,
        "scope": "continuous interval proof is written separately; finite boundary cases are auxiliary illustrations",
    }


def source_and_singular_algebra() -> dict:
    alpha, delta, cross, R = sp.symbols("alpha delta cross R", positive=True)
    G = sp.Matrix([[alpha, -cross], [-cross, delta]])
    sign = sp.diag(-1, 1)
    z0, z1 = sp.symbols("z0 z1", real=True)
    zeta = sp.Matrix([z0, z1])
    inverse = R * G.inv() * sign
    gradq = R * sign * zeta
    require(sp.simplify(inverse.T * gradq - R**2 * sign * G.inv() * sign * zeta) == sp.zeros(2, 1),
            "True endpoint gradient chain rule changed the physical clock.")
    e0, e1, rp = sp.symbols("e0 e1 rp", real=True)
    polar_e = sp.Matrix([e0, e1])
    h = (polar_e.T * R**2 * sign * G.inv() * sign * polar_e)[0]
    radial = (polar_e.T * (inverse.T * gradq).subs({z0: rp * e0, z1: rp * e1}))[0]
    require(sp.simplify(radial - rp * h) == 0, "Wrong radial roof derivative.")
    detG = sp.factor(G.det())
    dsource_dq = sp.Matrix([[1, 0], [-alpha / R, cross / R]])
    require(sp.simplify((dsource_dq * inverse).det() + R * cross / detG) == 0,
            "The momentum-to-source inverse determinant has a wrong R factor.")
    omega = cross / R
    u = R * cross / detG
    require(sp.simplify(u - R**2 * omega / detG) == 0, "Original optical/endpoint inverse identity failed.")
    rho, C, U, cstar, ucenter, mu, H, Rminus, Rplus, ell = sp.symbols(
        "rho C U cstar ucenter mu H Rminus Rplus ell", positive=True
    )
    tube_mass_lower = sp.pi * (2 * rho) ** 2 * ucenter / (4 * sp.pi * C)
    require(sp.simplify(tube_mass_lower - rho**2 * ucenter / C) == 0,
            "Radius-2rho disk area missing factor four.")
    center_sum = 25 * C * mu / rho**2
    angular_factor = 2 * sp.pi * U * C / (4 * sp.pi * cstar)
    atlas_bound = angular_factor * center_sum
    require(sp.simplify(atlas_bound - 25 * U * C**2 * mu / (2 * cstar * rho**2)) == 0,
            "Atlas coarea has wrong pi, overlap or section normalization.")
    rpositive, hpositive = sp.symbols("rpositive hpositive", positive=True)
    require(sp.simplify((ucenter * rpositive / (4 * sp.pi * cstar))
                        / (rpositive * hpositive) - ucenter / (4 * sp.pi * cstar * hpositive)) == 0,
            "Polar source and physical radial clock factors do not cancel.")
    # Physical roof bound from h<=2Rplus, with genuine center clock a.
    r = sp.symbols("r", positive=True)
    require(sp.integrate(2 * Rplus * r, (r, 0, rpositive)) == Rplus * rpositive**2,
            "The radial critical-roof upper bound lost a factor of two.")
    critical_density_prefactor = H * U * C * sp.sqrt(Rplus) / (2 * cstar * Rminus)
    critical_center_sum = C * mu / rho**2
    near_integral_bound = critical_density_prefactor * critical_center_sum * 2 * sp.sqrt(ell)
    require(sp.simplify(near_integral_bound - H * U * C**2 * sp.sqrt(Rplus)
                        * mu * sp.sqrt(ell) / (cstar * Rminus * rho**2)) == 0,
            "Critical inverse-gradient layer-cake coefficient incorrect.")
    v = sp.symbols("v", positive=True)
    layercake = sp.integrate(ell, (v, 0, 1 / sp.sqrt(ell))) + sp.integrate(v**-2, (v, 1 / sp.sqrt(ell), sp.oo))
    require(sp.simplify(layercake - 2 * sp.sqrt(ell)) == 0, "Borel roof-set inverse-square-root estimate failed.")
    far_integral_bound = H / (Rminus * rho) * atlas_bound * ell
    require(sp.simplify(far_integral_bound / mu
                        - H * (25 * U * C**2 / (2 * cstar * rho**2)) * ell / (Rminus * rho)) == 0,
            "Noncritical inverse-gradient factor incorrect.")
    # The physical Fourier correction sign is fixed by the exact clock identity.
    s, W, T, L = sp.symbols("s W T L", real=True)
    corrected_phase = -s * W + s * (L + W + T)
    require(sp.expand(corrected_phase - s * L - s * T) == 0,
            "Endpoint physical clock work has the wrong Fourier correction sign.")
    require(sp.expand(s * W + s * (L + W + T) - s * L - s * T) == 2 * s * W,
            "The opposite Fourier sign was not distinguished.")
    # Multiplier bound and widened incidence coefficient are independent counts.
    eps, ratio = sp.symbols("eps ratio", positive=True)
    require(sp.simplify(1 + 2 * 2 / eps * ratio / (1 - ratio)
                        - (1 + 4 / eps * ratio / (1 - ratio))) == 0,
            "Original I_m half-guard factor must be four/epsilon.")
    A, B, aa, cc = sp.symbols("A B aa cc", nonnegative=True)
    square_budget = 2 * (2 * A**2 + 2 * (2 * cc * aa * B) ** 2)
    require(sp.expand(square_budget - (4 * A**2 + 16 * cc**2 * aa**2 * B**2)) == 0,
            "Incidence widening coefficient16 miscomputed.")
    require(60000 * 25 == 1500000, "Guarded physical pressure normalization incorrect.")
    pressure = 60000 * Rplus**2 * U**2 * C * 25 * C / rho**2
    require(sp.simplify(pressure - 1500000 * Rplus**2 * U**2 * C**2 / rho**2) == 0,
            "Guarded stable pressure retained an illicit section factor.")
    return {
        "signed_inverse_source_jacobian": str(sp.factor((dsource_dq * inverse).det())),
        "optical_identity": "u=R^2*omega/det(G)",
        "atlas_roof_coefficient": "25*U*Cdist^2/(2*c_star*rho^2)",
        "near_critical_integrated_coefficient": "H_epsilon*U*Cdist^2*sqrt(R_plus)/(c_star*R_minus*rho^2)",
        "far_integrated_coefficient": "H_epsilon*C_at/(R_minus*rho)",
        "Borel_layercake_integral": "2*sqrt(ell)",
        "widened_incidence_square_factor": 16,
        "physical_fourier_correction": "exp(-i*s*W_d)",
        "guarded_pressure_coefficient": 1500000,
    }


def limit_checks() -> dict:
    # The written limit uses exp(x)>=x^k/k!, valid for every x>=0.
    # A larger exponent k than the polynomial order gives an explicit 1/m tail.
    checks = []
    for power, k in ((2, 4), (3, 5), (4, 6)):
        require(k > power, "Exponential remainder does not dominate polynomial loss.")
        checks.append({"polynomial_power": power, "exponential_series_term": k,
                       "factorial_constant": math.factorial(k), "remaining_decay_power": k - power})
    # j(ceil(theta*m)) >= theta*m/N - 2 follows from floor(x)>=x-1.
    N = 94
    count = 0
    for theta in (F(1, 100), F(1, 4), F(49, 100)):
        for m in range(1, 1025):
            depth_fraction = theta * m
            depth = -((-depth_fraction.numerator) // depth_fraction.denominator)
            j = max(0, depth // N - 1)
            require(F(j) >= theta * m / N - 2, "Anchor exponent floor/ceiling error.")
            count += 1
    return {
        "auxiliary_floor_ceiling_cases": count,
        "analytic_limit_certificate": "exp(lambda*m)>=(lambda*m)^k/k!, k>polynomial power",
        "polynomial_losses_checked": checks,
        "order": "fixed positive epsilon and all original outer widths, then m to infinity; B remains outermost",
        "epsilon_to_zero_uniformity_claimed": False,
        "unbounded_Fourier_integral_claimed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", type=Path, help="Write the identical deterministic JSON result here.")
    args = parser.parse_args()
    result = {
        "status": "passed",
        "scope": "exact auxiliary algebra and finite index checks; continuous geometry is proved in native manuscript",
        "native_sources_sha256": {
            name: sha_native(name) for name in (
                "311_finite_overlap_physical_source_height.tex",
                "312_normalized_records_singular_volume_and_pressure.tex",
                "313_explicit_physical_optical_comparison.tex",
            )
        },
        "physical_constants": physical_constants(),
        "coverage_and_indices": grid_and_index_checks(),
        "source_and_singular_algebra": source_and_singular_algebra(),
        "ordered_limits": limit_checks(),
        "unrestricted_whole_cylinder_pressure_proved": False,
        "full_original_positive_source_paid": False,
        "raw_pointwise_llt_claimed_complete": False,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.details is not None:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        args.details.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
