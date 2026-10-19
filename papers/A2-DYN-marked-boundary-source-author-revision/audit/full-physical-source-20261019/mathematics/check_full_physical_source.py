#!/usr/bin/env python3
"""Exact author checks for the full physical-source and singular-multiplier proofs.

These calculations check algebra, normalizations, exponent transitions and
explicit analytical negative controls.  They do not prove the inherited
continuous billiard kernel, atlas, coarea, or final raw pointwise theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def equal(left: sp.Expr, right: sp.Expr, message: str) -> None:
    difference = sp.simplify(left - right)
    require(difference == 0, message + ": " + str(difference))


def source_file(basename: str) -> Path:
    here = Path(__file__).resolve().parent
    direct = here / basename
    if direct.is_file():
        return direct
    candidates = sorted((here.parent / "core").glob("*" + basename))
    require(len(candidates) == 1, "native source must resolve uniquely: " + basename)
    return candidates[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", type=Path)
    args = parser.parse_args()

    checks: list[dict[str, object]] = []

    def passed(name: str, **values: object) -> None:
        checks.append({"name": name, "status": "passed", **values})

    q0 = Fraction(47, 53)
    eps0 = Fraction(1, 200)
    radius_min = Fraction(9, 20)
    radius_max = Fraction(47, 100)
    require(0 < eps0 < Fraction(3, 200) < Fraction(1, 4),
            "strict actual clearance-flux range")
    require(Fraction(11, 36) > Fraction(1, 16),
            "original endpoint cap excludes epsilon incidence failures")
    weight_sum = 2 * q0 / (1 - q0)
    require(weight_sum == Fraction(47, 3), "exact unchanged incidence depth sum")
    require(1 + 2 * weight_sum == Fraction(97, 3), "actual I_m restricted mass constant")
    require(4 * weight_sum == Fraction(188, 3), "mixed weak-tail sum coefficient")
    require(6 * weight_sum == 94, "critical-disk insertion coefficient")
    require(radius_min < radius_max, "original physical radius interval")

    depth_records = 0
    contact_records = 0
    flight_records = 0
    for m in range(1, 513):
        contacts: dict[int, int] = {}
        flights: dict[int, int] = {}
        for i in range(1, m):
            d = min(i, m - i)
            contacts[d] = contacts.get(d, 0) + 1
            require(d >= 1, "interior contact depth must start at one")
            contact_records += 1
        for i in range(m):
            d = min(i, m - 1 - i)
            flights[d] = flights.get(d, 0) + 1
            require(d >= 0, "flight depth must start at zero")
            flight_records += 1
        require(all(v <= 2 for v in contacts.values()), "contact depth multiplicity")
        require(all(v <= 2 for v in flights.values()), "flight depth multiplicity")
        require(sum(contacts.values()) == m - 1, "no dropped interior contact")
        require(sum(flights.values()) == m, "no dropped physical flight")
        exact_sum = sum((q0 ** d) * count for d, count in contacts.items())
        require(exact_sum <= weight_sum, "finite exact incidence sum below full series")
        depth_records += 1
    passed("physical_depth_and_endpoint_constants",
           q0=str(q0), epsilon_sharp=str(eps0), incidence_sum=str(weight_sum),
           insertion_constant="97/3", mixed_sum_coefficient="188/3",
           critical_disk_coefficient=94, counts_checked=depth_records,
           interior_contact_records=contact_records, physical_flight_records=flight_records,
           continuous_argument="Each depth has at most two indices; the native proof sums the infinite geometric series.")

    A, B, M, e0, lam, a, K, t, b = sp.symbols(
        "A B M e0 lambda a K t b", positive=True)
    eps, U, Cd, cp, Rp, g, delta = sp.symbols(
        "epsilon U Cdist cstar Rplus g delta", positive=True)
    rho = g * delta * eps / (128 * Rp)
    cat = 25 * U * Cd ** 2 / (2 * cp * rho ** 2)
    atlas_coefficient = 25 * U * Cd ** 2 / (2 * cp) * (128 * Rp / (g * delta)) ** 2
    equal(cat * eps ** 2, atlas_coefficient, "one conditioning factor in atlas constant")
    adaptive_eps = sp.sqrt(2 * A / lam)
    equal(A / adaptive_eps ** 2, lam / 2, "high-superlevel bounded part")
    equal(2 * B * adaptive_eps / lam, 2 * B * sp.sqrt(2 * A) * lam ** sp.Rational(-3, 2),
          "high-superlevel residual tail")
    equal(sp.sqrt(2 * A / e0 ** 2), sp.sqrt(2 * A) / e0,
          "low-superlevel mass threshold")
    passed("complete_finite_count_margin_exhaustion",
           high_threshold="lambda >= 2 A / epsilon_sharp^2",
           high_tail="2 B sqrt(2 A) lambda^(-3/2)",
           low_tail_coefficient="M sqrt(2 A)/epsilon_sharp",
           all_Borel_null_set_step="mu(S) <= A epsilon^-2 |S| + B epsilon; null S then epsilon decreases at finite m",
           atlas_normalization="exactly one cstar^-1")

    layercake_results = []
    for q in (sp.Rational(2), sp.Rational(3, 2), sp.Rational(4, 3),
              sp.Rational(6, 5), sp.Rational(12, 11)):
        threshold = (K / a) ** (1 / q)
        integral = a * threshold + K * threshold ** (1 - q) / (q - 1)
        expected = q / (q - 1) * K ** (1 / q) * a ** (1 - 1 / q)
        equal(integral, expected, "all-Borel layer cake q=" + str(q))
        layercake_results.append({"q": str(q), "coefficient": str(q / (q - 1)),
                                  "mass_power": str(1 - 1 / q)})
    passed("all_Borel_layercake_exact_values", cases=layercake_results)

    J, mass = sp.symbols("J mass", positive=True)
    equal(J * sp.sqrt(cp * mass) / cp, J * cp ** sp.Rational(-1, 2) * sp.sqrt(mass),
          "I_m conditional normalization")
    equal(J * (cp * mass) ** sp.Rational(1, 4) / cp,
          J * cp ** sp.Rational(-3, 4) * mass ** sp.Rational(1, 4),
          "actual singular conditional normalization")
    passed("original_conditional_measure",
           unweighted="a=cstar mu(S)", I_m="J cstar^(-1/2) mu(S)^(1/2)",
           actual_singular="Jcross cstar^(-3/4) mu(S)^(1/4)")

    Cmom, s, u = sp.symbols("Cmom s u", positive=True)
    kernel = Cmom / (4 * sp.pi)
    A0 = Cmom / 4
    A1 = Cmom / sp.pi
    equal(kernel * sp.pi * s ** 2, A0 * s ** 2, "full physical endpoint disk area")
    equal(kernel * 2 * s * 2 * u ** 2, A1 * s * u ** 2,
          "true prefix kernel incidence window area")
    equal(1 - sp.sqrt(1 - u ** 2), u ** 2 / (1 + sp.sqrt(1 - u ** 2)),
          "exact incidence interval length identity")
    large_window_cases = [Fraction(1), Fraction(3, 2), Fraction(2), Fraction(100)]
    for uv in large_window_cases:
        require(Fraction(2) <= 2 * uv ** 2, "u>=1 incidence window remains within 2u²")
    passed("two_actual_block_kernel_intersection",
           full_block="l=m: nu{r<s} <= (Cmom/4)s²",
           prefix_block="l=i>=1: nu{r<s, c_i<u} <= (Cmom/pi)s u²",
           large_windows_checked=len(large_window_cases),
           scope="all s,u>0; no probability product or independent collision model")

    j = sp.symbols("j", integer=True, nonnegative=True)
    annulus = B * (2 ** (j + 1) * b) * (t * 2 ** j * b) ** -2
    equal(annulus, 2 * B / (t ** 2 * b) * 2 ** -j, "dyadic mixed annulus")
    equal(sp.summation(2 * B / (t ** 2 * b) * 2 ** -j, (j, 0, sp.oo)),
          4 * B / (t ** 2 * b), "complete dyadic annulus sum")
    chosen_b = (B / A) ** sp.Rational(1, 3) * t ** sp.Rational(-2, 3)
    bound = A * chosen_b ** 2 + 4 * B / (t ** 2 * chosen_b)
    equal(bound, 5 * A ** sp.Rational(1, 3) * B ** sp.Rational(2, 3) * t ** sp.Rational(-4, 3),
          "all-level mixed weak4/3 coefficient")
    passed("full_dyadic_mixed_singularity",
           annulus_sum="A b² + 4B/(t² b)",
           substitution="b=(B/A)^(1/3)t^(-2/3)",
           coefficient="5 A^(1/3) B^(2/3)",
           weak_exponent="4/3", all_levels="every t>0")

    x = sp.symbols("x", positive=True)
    disk_mass = 2 * sp.sqrt(A * B) * a ** sp.Rational(3, 2)
    disk_integral = disk_mass / a + sp.integrate(
        2 * sp.sqrt(A * B) * x ** sp.Rational(3, 2) * x ** -2, (x, 0, a))
    equal(disk_integral, 6 * sp.sqrt(A * B) * sp.sqrt(a), "mixed disk inverse-gradient constant")
    equal(A * a ** 2 / a + sp.integrate(A, (x, 0, a)),
          2 * A * a, "unmarked disk inverse-gradient constant")
    beta = sp.symbols("beta", positive=True)
    equal((sp.sqrt(2 * U * beta)) ** sp.Rational(1, 2),
          (2 * U) ** sp.Rational(1, 4) * beta ** sp.Rational(1, 4),
          "actual critical-band quarter-power")
    passed("complete_physical_critical_band",
           marked_disk_mass="2sqrt(A0 A1)a^(3/2)",
           marked_disk_singular="6sqrt(A0 A1)a^(1/2)",
           actual_I_m_coefficient=94,
           conditioned_bound="[2A0 a +94sqrt(A0 A1)sqrt(a)]/(cstar Rminus)",
           small_roof_band_power="1/4", trace_claim=False)

    p = sp.symbols("p", positive=True)
    W = sp.symbols("W", positive=True)
    strong_results = []
    rates = [
        ("plain", sp.Rational(3, 2), sp.Rational(1), sp.Rational(1, 3), 2 / p - 1),
        ("actual_I_m", sp.Rational(6, 5), sp.Rational(1, 2), sp.Rational(1, 6), 2 / p - sp.Rational(3, 2)),
        ("actual_I_m_over_gradient", sp.Rational(12, 11), sp.Rational(1, 4), sp.Rational(1, 12), 2 / p - sp.Rational(7, 4)),
    ]
    for name, q, mass_rate, weak_rate, expected in rates:
        strong_exponent = (mass_rate * (q - p) / (q - 1)
                           + weak_rate * q * (p - 1) / (q - 1)) / p
        equal(strong_exponent, expected, "complete strong-norm exponent " + name)
        endpoint = sp.simplify(expected.subs(p, q))
        require(endpoint > 0, "rate positive up to weak endpoint " + name)
        s0 = (W ** q / M) ** (1 / (q - 1))
        integral = p * (M * s0 ** (p - 1) / (p - 1)
                        + W ** q * s0 ** (p - q) / (q - p))
        expression = p * (q - 1) / ((p - 1) * (q - p)) * M ** ((q - p) / (q - 1)) * W ** (q * (p - 1) / (q - 1))
        equal(integral, expression, "mass/weak strong interpolation " + name)
        strong_results.append({"source": name, "weak_q": str(q),
                               "mass_rate": str(mass_rate), "weak_rate": str(weak_rate),
                               "strong_p_rate": str(expected),
                               "valid_strong_range": "1<p<" + str(q),
                               "normalized_spike_m_power": str(2 * q),
                               "normalized_spike_exponential_rate": str(q * weak_rate)})
    passed("full_source_strong_norms_and_normalized_spikes", sources=strong_results,
           normalization="m² does not overcome any strictly positive exponential decay",
           forbidden_endpoint="strong Lq at q=3/2,6/5,12/11 is not inferred")

    for power in (Fraction(11, 10), Fraction(6, 5), Fraction(13, 10)):
        pp = sp.Rational(power.numerator, power.denominator)
        q = sp.Rational(4, 3)
        direct = J ** pp + pp * J ** q * J ** (pp - q) / (q - pp)
        equal(direct, 4 * J ** pp / (4 - 3 * pp), "full singular physical p moment")
    require(sp.integrate(x ** -1, (x, 1, sp.oo)) == sp.oo,
            "endpoint p=4/3 tail does not imply its strong moment")
    passed("actual_singular_physical_moments", valid_range="1<p<4/3",
           constant="4 Jcross^p/(4-3p)", rational_p_cases=3,
           strong_endpoint_not_asserted=True)

    clock, work, transport, freq = sp.symbols("LQ W T s", real=True)
    compensated_argument = -freq * work + freq * (clock + work + transport)
    equal(compensated_argument - freq * clock, freq * transport,
          "actual signed endpoint-work phase")
    wrong_argument = freq * work + freq * (clock + work + transport)
    equal(wrong_argument - freq * clock, freq * (2 * work + transport),
          "positive compensation must fail")
    clock_count_cases = 0
    for theta in (Fraction(1, 100), Fraction(1, 4), Fraction(49, 100)):
        for m in range(1, 1025):
            d = (theta.numerator * m + theta.denominator - 1) // theta.denominator
            require(Fraction(d // 94) >= theta * m / 94 - 1,
                    "actual floor clock count")
            if 2 * d < m:
                require(d >= 1 and m - 2 * d >= 1, "actual central flight range")
                clock_count_cases += 1
    passed("original_full_clock_and_exact_mark_comparison",
           compensation="exp(-i s W_d)", leftover="s T_clock",
           negative_control="exp(+i s W_d) leaves s(2W_d+T_clock)",
           actual_central_range="d>=1 and 2d<m", count_cases=clock_count_cases,
           order="outer B and all original windows fixed before collision limsup",
           unchanged="full physical L_m(Q), all collision/return/displacement/terminal selectors")

    # Analytical negative controls only: these are NOT physical Lorentz trajectories.
    uniform_variable = sp.symbols("v", positive=True)
    inverse_product_integral = sp.integrate(1 / uniform_variable, (uniform_variable, 0, 1))
    require(inverse_product_integral == sp.oo, "separate weak2 tails must not imply finite product")
    equal(s ** 2 / (s * s ** 2), 1 / s, "artificial diagonal law violates the needed joint kernel bound")
    require(sp.limit(1 / s, s, 0, dir="+") == sp.oo,
            "no finite joint-intersection constant for the diagonal law")
    n = sp.symbols("n", positive=True, integer=True)
    for q in (sp.Rational(3, 2), sp.Rational(6, 5), sp.Rational(12, 11)):
        scaled_weak = n ** 2 * (n ** -2 * sp.exp(-n) ** (1 / q))
        require(sp.limit(scaled_weak, n, sp.oo) == 0,
                "tiny analytical roof spike has zero normalized weak norm")
    require(n ** 2 * n ** -2 == 1, "same analytical roof spike retains normalized height one")
    passed("analytical_negative_controls",
           status_detail="controls establish why stronger implications are NOT made",
           separate_marginals={
               "space": "v uniform on (0,1), abstract probability example only",
               "variables": "r=c=sqrt(v)",
               "both_marginal_tails": "P{r<a}=P{c<a}=a² for 0<a<1",
               "product": "1/(rc)=1/v has infinite first moment",
               "missing_intersection": "P{r<a,c<a}/(a*a²)=1/a diverges"},
           roof_spike={
               "function": "f_n(t)=n^-2 1_[0,exp(-n)](t), abstract density control only",
               "normalized_weak_norm": "exp(-n/q) tends to zero",
               "normalized_essential_height": 1},
           physical_model_evidence=False)

    source_hashes = {}
    for name in ("full_physical_source_roof_regularity.tex", "full_physical_singular_multiplier.tex"):
        path = source_file(name)
        source_hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    result = {
        "status": "passed",
        "kind": "exact author algebra and analytical controls",
        "program": "check_full_physical_source.py",
        "source_sha256": source_hashes,
        "checks": checks,
        "scope": {
            "continuous_model_proof": "native proofs plus their explicitly retained inherited physical kernel, atlas and coarea",
            "no_physical_sampling_claim": True,
            "actual_full_bulk_singular_multiplier": "verified algebra of the proved weak4/3 mechanism",
            "separate_singular_trace_proved_by_program": False,
            "full_raw_pointwise_LLT_completed": False,
            "original_events_windows_and_order_preserved": True,
        },
    }
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.details is not None:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        args.details.write_text(payload, encoding="utf-8")
    sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
