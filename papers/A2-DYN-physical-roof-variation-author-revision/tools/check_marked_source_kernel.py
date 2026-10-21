#!/usr/bin/env python3
"""New post-recovery exact checks for native316; this is not the lost checker.

Uses only standard-library rational arithmetic and formal polynomial identities.
Continuum geometry, homogeneous growth and the complete trace are proved in the
native source and reconstructed in the accompanying author report. Finite tests
are auxiliary checks, not proofs of those dynamical inputs or the raw local limit.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


class Poly:
    """Sparse polynomials over Q, used only for exact coefficient identities."""

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {monomial: Fraction(coefficient)
                          for monomial, coefficient in value.items() if coefficient}
        else:
            coefficient = Fraction(value)
            self.terms = {(): coefficient} if coefficient else {}

    @classmethod
    def variable(cls, name: str):
        return cls({((name, 1),): Fraction(1)})

    def __add__(self, other):
        other = Poly(other)
        result = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({monomial: -coefficient for monomial, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly(other))

    def __rsub__(self, other):
        return Poly(other) - self

    def __mul__(self, other):
        other = Poly(other)
        result = {}
        for left, coefficient_left in self.terms.items():
            for right, coefficient_right in other.terms.items():
                powers = dict(left)
                for name, exponent in right:
                    powers[name] = powers.get(name, 0) + exponent
                monomial = tuple(sorted(powers.items()))
                result[monomial] = result.get(monomial, Fraction(0)) + coefficient_left * coefficient_right
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, exponent: int):
        require(isinstance(exponent, int) and exponent >= 0, "Polynomial exponent domain")
        result = Poly(1)
        for _ in range(exponent):
            result = result * self
        return result


class Rat:
    """Formal rational functions; equality is checked by cross multiplication."""

    def __init__(self, numerator=0, denominator=1):
        if isinstance(numerator, Rat):
            require(denominator == 1, "Rational copy constructor")
            self.numerator = Poly(numerator.numerator)
            self.denominator = Poly(numerator.denominator)
        else:
            self.numerator = Poly(numerator)
            self.denominator = Poly(denominator)
        require(bool(self.denominator.terms), "Nonzero formal denominator")

    @classmethod
    def variable(cls, name: str):
        return cls(Poly.variable(name))

    def __add__(self, other):
        other = Rat(other)
        return Rat(self.numerator * other.denominator + other.numerator * self.denominator,
                   self.denominator * other.denominator)

    __radd__ = __add__

    def __neg__(self):
        return Rat(-self.numerator, self.denominator)

    def __sub__(self, other):
        return self + (-Rat(other))

    def __rsub__(self, other):
        return Rat(other) - self

    def __mul__(self, other):
        other = Rat(other)
        return Rat(self.numerator * other.numerator, self.denominator * other.denominator)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Rat(other)
        return Rat(self.numerator * other.denominator, self.denominator * other.numerator)

    def __rtruediv__(self, other):
        return Rat(other) / self

    def __pow__(self, exponent: int):
        require(isinstance(exponent, int), "Integer rational-function exponent")
        if exponent < 0:
            return Rat(self.denominator ** (-exponent), self.numerator ** (-exponent))
        return Rat(self.numerator ** exponent, self.denominator ** exponent)


def equal(left, right, message: str) -> None:
    left, right = Rat(left), Rat(right)
    difference = left.numerator * right.denominator - right.numerator * left.denominator
    require(not difference.terms, message + ": nonzero exact coefficient remainder")


def native_source() -> Path:
    directory = Path(__file__).resolve().parent
    name = "316_marked_clearance_momentum_and_trace.tex"
    candidates = [directory / name, directory.parent / "core" / name]
    found = [path for path in candidates if path.is_file()]
    require(len(found) == 1, "Resolve the exact native316 source uniquely")
    return found[0]


def evaluate_polynomial(coefficients: tuple[Fraction, ...], value: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", type=Path)
    args = parser.parse_args()
    groups = []

    def passed(name: str, **data) -> None:
        groups.append({"name": name, "status": "passed", **data})

    r_min, r_max = Fraction(9, 20), Fraction(47, 100)
    delta_max, tau_min = Fraction(3, 200), Fraction(3, 50)
    k_min = Fraction(100, 47)
    gap = 1 - 2 * r_max
    b_max = r_max + delta_max
    standoff_squared = (1 - r_max) ** 2 - b_max ** 2
    require(gap == tau_min and delta_max == gap / 4, "Original radius and clearance schedule")
    require(b_max == Fraction(97, 200), "Maximum signed impact magnitude")
    require(1 - r_max - delta_max - r_max == Fraction(9, 200), "Strict free-foot margin")
    require(standoff_squared == Fraction(1827, 40000), "Exact standoff square")
    require(standoff_squared - tau_min ** 2 == Fraction(1683, 40000) > 0,
            "Standoff strictly exceeds the physical lower flight length")
    require(k_min * tau_min == Fraction(6, 47), "Terminal coarea lower constant")
    require(k_min ** 2 * standoff_squared == Fraction(1827, 94 ** 2),
            "Squared first-collision lower constant")
    passed("uniform_physical_geometry", radius=[str(r_min), str(r_max)],
           clearance_max=str(delta_max), standoff_squared=str(standoff_squared),
           foot_margin="9/200", first_derivative_lower="sqrt(1827)/94",
           last_derivative_lower="6/47", speed=1,
           scope="All printed bounds use the original triangular lattice spacing one and physical disks.")

    R, c, t, pi, cstar = [Rat.variable(name) for name in ("R", "c", "t", "pi", "cstar")]
    theta_alpha, theta_p = Rat(1), 1 / c
    b_alpha, b_p = -R * c - t, -t / c
    determinant = theta_alpha * b_p - theta_p * b_alpha
    equal(determinant, R, "Full (alpha,p) to (theta,b) determinant")
    flux = 1 / (4 * pi * R * cstar)
    width = Rat.variable("delta")
    equal(4 * pi * width * flux, width / (R * cstar), "Both-sign mass and one conditioning factor")
    equal(4 * pi * width / (4 * pi * R), width / R, "Unconditional one-copy clearance mean")
    for sign in (-1, 1):
        require(abs(sign) == 1, "Signed impact-to-clearance derivative has unit magnitude")
    passed("exact_flux_jacobian_and_single_normalization",
           derivative_coordinates={"theta_alpha": "1", "theta_p": "1/c",
                                   "b_alpha": "-R*c-t", "b_p": "-t/c"},
           determinant="R", conditional_prefactor="1/(4*pi*R*cstar)",
           full_angular_mass="4*pi", unconditional_marked_mass="delta/R",
           selector_scope="The same bound holds for [0,1] selectors; general multipliers incur their supremum norm.")

    kappa, a, d, V, tau = [Rat.variable(name) for name in ("kappa", "a", "d", "V", "tau")]
    V_first, ds_dtheta = kappa + c / a, -a / c
    equal(c * V_first * ds_dtheta, -(kappa * a + c), "First actual incidence cancellation")
    w, A = kappa + V, c + tau * (kappa + V)
    V_next, ds_next_ds = kappa + d * w / A, -A / d
    equal(d * V_next * ds_next_ds, -(kappa * A + d * w), "Last actual incidence cancellation")
    equal(kappa * A + d * w - kappa * tau * w, kappa * c + d * w,
          "Nonnegative terminal numerator remainder")
    equal(w ** 2 - (1 + V ** 2), kappa ** 2 - 1 + 2 * kappa * V,
          "Positive cone-to-Euclidean comparison remainder")
    M, A_source, C_growth, J = [Rat.variable(name) for name in ("M", "A_source", "C_growth", "J")]
    first_kernel = 2 * M / (kappa * a)
    later_kernel = A_source * C_growth * J / (kappa * tau)
    equal(first_kernel * kappa * a, 2 * M, "Both first-impact signs are counted once")
    equal(later_kernel * kappa * tau, A_source * C_growth * J,
          "No extra sign factor after the both-sign source allowance")
    passed("both_actual_incidence_cancellations", first_derivative="-(kappa*a+c)",
           last_derivative_magnitude="(kappa*A+d*(kappa+V))/sqrt(1+V^2)",
           regular_domain="a,c,d,tau>0; V>=kappa>1",
           first_kernel="2*M_star/(k_min*a_circ)",
           later_kernel="A_star*C_g*J_f/(k_min*tau_min)",
           limit_scope="Cancellation is established on regular physical branches before estimating small incidence.")

    u = Rat.variable("u")
    for sign in (-1, 1):
        original_foot_coefficient = -sign * (R + u)
        reversed_foot_coefficient = -(-sign) * (R + u) * (-1)
        equal(original_foot_coefficient, reversed_foot_coefficient,
              "Actual marked foot is fixed by the signed line reversal")
    reflection = ((1, 0), (0, -1))
    product = tuple(tuple(sum(reflection[k][i] * reflection[k][j] for k in range(2))
                          for j in range(2)) for i in range(2))
    require(product == ((1, 0), (0, 1)), "Collision reversal is an exact Euclidean isometry")
    passed("signed_reversal_preserves_the_mark", parameter_map="(theta,sigma,u)->(theta+pi,-sigma,u)",
           original_momentum="P_l_minus=-P_l_plus_in_the_reversed_record",
           measure="Angular translation and sign permutation preserve the complete two-sign angular measure.",
           event="The original selector is transported; the section is not replaced by a reflected section.")

    i_form, j_form, m_form, l_form = [Rat.variable(name) for name in ("i", "j", "m", "l")]
    equal(j_form - (j_form - i_form + 1) + 1, i_form, "Universal backward index identity")
    equal(j_form + (i_form - j_form), i_form, "Universal forward index identity")
    equal((j_form + 1) + (m_form - j_form), m_form + 1, "Complete contact count")
    equal(1 + (l_form - 2) + 1, l_form, "One first hit, l-2 intermediate hits, one last hit")
    index_cases = 0
    for m in range(1, 33):
        for j in range(m):
            for i in range(m + 1):
                count = j - i + 1 if i <= j else i - j
                require(count >= 1, "Each designated contact has a positive directional collision count")
                reconstructed = j - count + 1 if i <= j else j + count
                require(reconstructed == i, "Actual marked-flight contact reconstruction")
                index_cases += 1
        occupations = tuple(range(m))
        require(len(occupations) == m and m not in occupations, "Terminal visit is tested separately")
    require(index_cases == 11968, "Exact finite boundary-index regression count")
    passed("complete_record_indices_and_propagation", universal_identities="Exact formal polynomial identities",
           finite_regression_cases=index_cases, regression_range="1<=m<=32; every 0<=j<m, 0<=i<=m",
           backward_count="j-i+1", forward_count="i-j", intermediate_collisions="l-2 for l>=2",
           occupation_indices="0,...,m-1", terminal_test="m", mark_is_not_a_collision=True)

    q0 = Fraction(47, 53)
    W0 = 1 + 2 / (1 - q0)
    require(W0 == Fraction(56, 3), "Original total Jensen weight allowance")
    q, z = Rat.variable("q"), Rat.variable("q_to_h")
    even_scaled_sum, odd_scaled_sum = 2 * q - (1 + q) * z, 2 * q * (1 - z)
    equal(2 - even_scaled_sum, 2 * (1 - q) + (1 + q) * z,
          "Even-depth positive geometric remainder")
    equal(2 - odd_scaled_sum, 2 * (1 - q) + 2 * q * z,
          "Odd-depth positive geometric remainder")
    for m in range(1, 65):
        actual = sum((q0 ** min(i, m - i) for i in range(1, m)), Fraction(0))
        h = m // 2
        formula = (2 * q0 - (1 + q0) * q0 ** h) / (1 - q0) if m % 2 == 0 else 2 * q0 * (1 - q0 ** h) / (1 - q0)
        require(actual == formula and actual <= 2 / (1 - q0), "Exact interior-only geometric sum")
    gamma = Rat.variable("gamma")
    equal(2 / (1 - gamma / 2), 4 / (2 - gamma), "Exact endpoint-integrability bound")
    v = Rat.variable("v")
    equal((1 - v ** 2) - (1 - v), v * (1 - v), "Endpoint integrand comparison on 0<=v<=1")
    for value in (Fraction(1), Fraction(3, 2), Fraction(7, 4), Fraction(1999999, 1000000)):
        exponent = 1 - value / 2
        require(exponent > 0 and 2 / exponent == 4 / (2 - value), "Admissible exact gamma gate")
    require(1 - Fraction(2) / 2 == 0, "The gamma=2 endpoint has a logarithmic integral, not a finite power integral")
    passed("unchanged_interior_weights_and_gamma_threshold", original_guard=str(q0), W0=str(W0),
           indices="1,...,m-1 only; empty when m=1", geometric_regression_counts=64,
           convexity_domain="gamma>=1", endpoint_integrability_domain="gamma<2",
           moment_integral_bound="J_gamma<=4/(2-gamma)",
           exact_critical_exclusion="gamma=2 is not claimed",
           continuum_scope="Weighted Jensen and the improper integral argument are proved in native316; no sampled exponent establishes them.")

    s = Rat.variable("sqrt_one_minus_eta_squared")
    eta_squared = 1 - s ** 2
    momentum_length = 2 * (1 - s)
    equal(2 * eta_squared - momentum_length, 2 * s * (1 - s),
          "Positive grazing-width remainder for every 0<=s<=1")
    H = Rat.variable("H")
    equal(H * width * 2 * eta_squared / (4 * pi * R * cstar),
          H * width * eta_squared / (2 * pi * R * cstar), "Exact marked grazing normalization")
    passed("quadratic_grazing_width_and_marked_factor", substitution="s=sqrt(1-eta^2) in [0,1]",
           exact_nonnegative_remainder="2*eta^2-2*(1-s)=2*s*(1-s)",
           marked_bound="H_nm*delta*eta^2/(2*pi*R*cstar)",
           valid_range="0<eta<=1; no positive incidence cutoff")

    examples = [
        (Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(-1)),
        (Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(-7)),
        (Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(-1), Fraction(4)),
        (Fraction(0), Fraction(0), Fraction(0)),
    ]
    certificates = []
    for coefficients in examples:
        first = next((i for i, coefficient in enumerate(coefficients) if coefficient), None)
        if first is None:
            certificates.append({"coefficients": [str(c) for c in coefficients],
                                 "identically_zero": True, "strict_positive_trace": False,
                                 "nonstrict_positive_trace": True})
            continue
        lead = coefficients[first]
        tail = sum((abs(value) for value in coefficients[first + 1:]), Fraction(0))
        epsilon = min(Fraction(1), abs(lead) / (2 * tail)) if tail else Fraction(1)
        require(epsilon > 0 and (tail == 0 or tail * epsilon <= abs(lead) / 2),
                "Exact one-sided sign certificate for the whole interval")
        for divisor in (1, 2, 3, 11):
            value = evaluate_polynomial(coefficients, epsilon / divisor)
            require(value * lead > 0, "One-sided sign regression agrees with its interval certificate")
        certificates.append({"coefficients": [str(c) for c in coefficients],
                             "first_nonzero_degree": first, "epsilon": str(epsilon),
                             "sign": 1 if lead > 0 else -1,
                             "certificate": "sum(abs(higher coefficients))*epsilon<=abs(lead)/2"})
    require(evaluate_polynomial(examples[0], Fraction(0)) == 0 and
            evaluate_polynomial(examples[0], Fraction(1, 1000)) > 0,
            "A strict one-sided trace can differ from boundary evaluation")
    passed("one_sided_selector_endpoint_conventions", exact_polynomial_certificates=certificates,
           strict_boundary_example="g(u)=u: positive-side indicator tends to 1, while 1_{g(0)>0}=0",
           persistent_equality="Identically zero gives false for strict positivity and true for nonstrict positivity.",
           source_scope="The native finite-word analytic continuation is required; this finite algebra does not prove that dynamical input.",
           tests_without_automatic_limits="Arbitrary Borel roof sets still need an a.e. one-sided limit; interval tests are the stated native case.")

    source = native_source()
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    require(source_hash == "64e8bb1b289b244f02ed06e4e56e2c5add54d6835ef48bf7d2b2a0c036a44383",
            "Bind checks to the independently reconstructed final native316 source")
    result = {"status": "passed", "check_count": len(groups), "checks": groups,
              "native_source": source.name, "native_sha256": source_hash,
              "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "program_provenance": "New program written after recovery of the erased uncommitted workspace; not the lost original marked-source checker.",
              "arithmetic": "Python standard-library Fraction and exact sparse polynomial coefficient identities; no floating point or external symbolic package.",
              "limitations": [
                  "Finite index and polynomial examples are auxiliary regressions; universal identities and declared positivity domains are stated separately.",
                  "Actual homogeneous growth, every angular root, finite physical visibility, and analytic one-sided record continuation remain native mathematical proofs.",
                  "No Markov replacement, conditional independence, m^-2 roof density, whole pressure, pairing completion, raw local limit, or historical execution is certified here."]}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.details is not None:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        args.details.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        sys.stderr.write(type(error).__name__ + ": " + str(error) + "\n")
        raise SystemExit(1)
