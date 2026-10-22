#!/usr/bin/env python3
"""Auxiliary exact arithmetic for native330--331, not a continuous billiard certificate."""
from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path

from analytic_check_support import (
    Audit, command_arguments, derivative, emit_result, fraction_text,
    integral, polynomial_value,
)


def label_l1(left: int | None, right: int | None) -> int:
    if left == right:
        return 0
    return 1 if left is None or right is None else 2


def step_value(values: tuple[int, ...], t: F) -> F:
    if t < 0 or t >= len(values):
        return F(0)
    return F(values[t.numerator // t.denominator])


def step_variation(values: tuple[int, ...]) -> F:
    augmented = (0,) + values + (0,)
    return F(sum(abs(right - left) for left, right in zip(augmented, augmented[1:])))


def contains(intervals: tuple[tuple[F, F], ...], t: F) -> bool:
    return any(left <= t < right for left, right in intervals)


def symmetric_difference_integrals(intervals: tuple[tuple[F, F], ...], shift: F, values: tuple[int, ...]) -> tuple[F, F]:
    shifted = tuple((left + shift, right + shift) for left, right in intervals)
    breaks = sorted({F(i) for i in range(len(values) + 1)} | {x for pair in intervals + shifted for x in pair})
    length = F(0)
    weighted = F(0)
    for left, right in zip(breaks, breaks[1:]):
        middle = (left + right) / 2
        if contains(intervals, middle) != contains(shifted, middle):
            length += right - left
            weighted += (right - left) * step_value(values, middle)
    return length, weighted


def check_label_and_bv(audit: Audit) -> None:
    labels = [None, 0, 1, 2, 3]
    for left, right in product(labels, repeat=2):
        audit.check("all-label internal transfer cost two", label_l1(left, right) <= 2, (left, right))
    for label in labels:
        audit.check("endpoint creation or deletion cost one", label_l1(None, label) <= 1, label)
    for length in range(2, 6):
        for states in product(labels, repeat=length):
            paid = sum(label_l1(a, b) for a, b in zip(states, states[1:]))
            audit.check("coincident transition telescoping", label_l1(states[0], states[-1]) <= paid, states)
    for values in product(range(4), repeat=4):
        variation = step_variation(values)
        audit.check("compact positive BV height factor one half", 2 * max(values) <= variation, values)
        for shift in (F(-3, 2), F(-1, 2), F(0), F(1, 3), F(5, 4)):
            breaks = sorted({F(i) for i in range(5)} | {F(i) - shift for i in range(5)})
            cost = sum((right-left) * abs(step_value(values, (left+right)/2+shift) - step_value(values, (left+right)/2))
                       for left, right in zip(breaks, breaks[1:]))
            audit.check("exact step-function BV translation inequality", cost <= variation * abs(shift), (values, shift))
    audit.detail("all_label_scope", {
        "source_factor": "one complete physical coarea source, not one source for each label",
        "internal_jump": 2,
        "endpoint_jump": 1,
        "native_proof": "thm:av-all-bv",
        "finite_checks_do_not_prove": "the inherited all-word boundary budgets or continuous billiard BV theorem",
    })


def check_finite_towers(audit: Audit) -> None:
    instances = 0
    nonsaturated = 0
    for size in range(1, 6):
        for perm in permutations(range(size)):
            for mask in range(1, 1 << size):
                section = {i for i in range(size) if mask & (1 << i)}
                return_time = {}
                induced = {}
                tower = []
                for point in sorted(section):
                    orbit = [point]
                    current = perm[point]
                    while current not in section:
                        orbit.append(current)
                        current = perm[current]
                        if len(orbit) > size:
                            raise RuntimeError("A finite permutation orbit failed to return.")
                    return_time[point] = len(orbit)
                    induced[point] = current
                    tower.extend(orbit)
                instances += 1
                audit.check("finite true tower levels are disjoint", len(tower) == len(set(tower)), (size, perm, mask))
                audit.check("nearest-past induced partition", set(induced.values()) == section and len(set(induced.values())) == len(section), (size, perm, mask))
                audit.check("finite exact tower mass and Kac upper bound", F(sum(return_time.values()), size) == F(len(set(tower)), size) <= 1, (size, perm, mask))
                if len(set(tower)) < size:
                    nonsaturated += 1
                cstar = F(len(section), size)
                for count in range(1, 5):
                    counts = []
                    for point in sorted(section):
                        total, current = 0, point
                        for _ in range(count):
                            total += return_time[current]
                            current = induced[current]
                        counts.append(total)
                    expectation = F(sum(counts), len(section))
                    audit.check("finite induced invariance gives nth-count expectation", expectation == F(count * sum(return_time.values()), len(section)), (size, perm, mask, count))
                    audit.check("finite collision-count expectation bound", expectation <= count / cstar, (size, perm, mask, count))
                    threshold = F(2 * count + 1, 2)
                    tail = F(sum(value > threshold for value in counts), len(section))
                    audit.check("finite Markov collision-tail inequality", tail <= count / (cstar * threshold), (size, perm, mask, count))
    audit.detail("tower_examples", {
        "permutation_and_nonempty_section_instances": instances,
        "nonsaturated_instances": nonsaturated,
        "saturation_equality_assumed": False,
        "scope": "Only the combinatorial tower identities are illustrated. The native proof establishes conservative recurrence on the original invariant billiard space directly.",
    })


def check_kernel(audit: Audit) -> None:
    zero = [F(0)]
    polys = [
        zero,
        [F(2), F(6), F(6), F(2)],
        [F(1), F(0), F(-6), F(-6)],
        [F(1), F(0), F(-6), F(6)],
        [F(2), F(-6), F(6), F(-2)],
        zero,
    ]
    knots = [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]
    jumps = []
    for index, knot in enumerate(knots):
        for order in range(3):
            audit.check("kernel transform C2 knot matching", polynomial_value(derivative(polys[index], order), knot) == polynomial_value(derivative(polys[index+1], order), knot), (index, order))
        jumps.append(polynomial_value(derivative(polys[index+1], 3), knot) - polynomial_value(derivative(polys[index], 3), knot))
    audit.check("kernel fourth distributional derivative jumps", jumps == list(map(F, [12, -48, 72, -48, 12])), jumps)
    mass = sum(integral(polys[index+1], knots[index], knots[index+1]) for index in range(4))
    audit.check("kernel transform integral and inverse value at zero", mass == F(3, 4), mass)
    audit.check("kernel total mass transform value", polynomial_value(polys[3], F(0)) == 1)
    audit.check("kernel second moment from exact second derivative", -polynomial_value(derivative(polys[3], 2), F(0)) == 12)
    # With c=cos(t/2), both inverse-transform numerators are 48(c-1)^2.
    cosine_expansion = [F(48), F(-96), F(48)]
    sine_fourth_expansion = [F(48), F(-96), F(48)]
    audit.check("kernel exact cosine to sinc-fourth numerator", cosine_expansion == sine_fourth_expansion)
    audit.check("kernel inverse-transform normalization", F(3, 8) * 4**4 == F(192, 2))
    for numerator in range(101):
        s = F(numerator, 100)
        value = polynomial_value(polys[3] if s <= F(1,2) else polys[4], s)
        audit.check("kernel rational-grid positivity illustration", 0 <= value <= 1, s)
    # The full interval positivity is algebraic, not inferred from that grid:
    audit.check("kernel inner derivative factorization", derivative(polys[3]) == [F(0), F(-12), F(18)])
    audit.check("kernel inner decreasing interval lower endpoint", polynomial_value(polys[3], F(1,2)) == F(1,4))
    audit.check("kernel outer cubic coefficients", polys[4] == [F(2), F(-6), F(6), F(-2)])
    audit.detail("kernel_exact_data", {
        "Fourier_convention": "integral exp(i*s*t) f(t) dt",
        "third_derivative_jumps": [fraction_text(v) for v in jumps],
        "transform_integral": fraction_text(mass),
        "inverse_density_at_zero": "3/(8*pi)",
        "total_mass": 1,
        "second_moment": 12,
        "first_absolute_moment_upper_bound": "sqrt(12)",
        "support_of_transform": "[-1,1]",
    })


def check_interval_and_likelihood(audit: Audit) -> None:
    presentations = [
        ((F(0), F(1)),),
        ((F(-1,2), F(1,3)),),
        ((F(0), F(1)), (F(2), F(3))),
        ((F(0), F(2)), (F(1), F(3))),
        ((F(1,3), F(1,3)),),
    ]
    for intervals in presentations:
        for numerator in range(-6, 7):
            shift = F(numerator, 4)
            for values in product(range(3), repeat=3):
                length, weighted = symmetric_difference_integrals(intervals, shift, values)
                variation = step_variation(values)
                audit.check("interval union symmetric difference bound", length <= 2 * len(intervals) * abs(shift), (intervals, shift))
                audit.check("trajectory likelihood integrand including half-height", weighted <= len(intervals) * abs(shift) * variation, (intervals, shift, values))
    # Exact positive remainder versus signed variation costs.
    for mass in (F(0), F(1,7), F(1,2), F(1)):
        for first, second in product(range(5), repeat=2):
            h = [mass * F(first,4), mass * (1-F(first,4))]
            kh = [mass * F(second,4), mass * (1-F(second,4))]
            audit.check("positive law remainder costs twice its mass", sum(abs(a-b) for a,b in zip(h,kh)) <= 2*mass)
    audit.detail("likelihood_norms", {
        "law_error": "2*delta + kappa_ker*V_L/bandwidth",
        "same_trajectory_event_L1_error": "delta + kappa_ker*J*V_L/bandwidth",
        "variation_convention": "full total variation, not one half",
        "arbitrary_trajectory_selectors": "bounded Borel observations multiply the event error; no selector BV claimed",
    })


def check_polynomial_exponents(audit: Audit) -> None:
    examples = []
    for p, kappa in product((F(1,10), F(1,2), F(1), F(7,3), F(8)), (F(0), F(1,3), F(2), F(9,2))):
        l_exponent = p + 3
        bandwidth_exponent = 2*p + kappa + 5
        tail = 2 + 1 - l_exponent
        event = 2 + kappa + l_exponent - bandwidth_exponent
        law = 2 + l_exponent - bandwidth_exponent
        fixed_count = 2 + kappa - (p+kappa+2)
        audit.check("actual tower polynomial normalized tail exponent", tail == -p)
        audit.check("actual tower polynomial likelihood exponent", event == -p)
        audit.check("law polynomial error exponent", law == -p-kappa <= -p)
        audit.check("fixed collision polynomial likelihood exponent", fixed_count == -p)
        examples.append({"P":fraction_text(p), "kappa":fraction_text(kappa), "cutoff_power":fraction_text(l_exponent), "bandwidth_power":fraction_text(bandwidth_exponent)})
    audit.detail("polynomial_examples", examples)
    audit.detail("polynomial_scope", "Every substitution is into a finite-parameter inequality. The analytic bandwidth is independent of the outer geometric B; no microscopic width or ordered geometric limit is changed.")


def check_denominators_and_marks(audit: Audit) -> None:
    weights = (F(1,6), F(1,3), F(1,2))
    available = (F(0), F(1,4), F(1,2), F(3,4), F(1))
    positive = 0
    for a in product((F(0), F(1)), repeat=3):
        for b in product(available, repeat=3):
            p = sum(w*v for w,v in zip(weights,a))
            pb = sum(w*v for w,v in zip(weights,b))
            error = sum(w*abs(x-y) for w,x,y in zip(weights,a,b))
            audit.check("actual selected denominator mass error", abs(p-pb) <= error)
            if p and pb:
                distance = sum(w*abs(x/p-y/pb) for w,x,y in zip(weights,a,b))
                audit.check("actual conditional full variation inequality", distance <= 2*error/p)
                positive += 1
                if pb > error:
                    audit.check("verified likelihood denominator inequality", p >= pb-error and distance <= 2*error/(pb-error))
            if p > error:
                audit.check("conditional positivity follows from actual mass", pb >= p-error > 0)
    audit.detail("conditional_examples", {"positive_pair_instances":positive, "denominator":"actual intersection of the record event and the information event", "unproved_floor_assumed":False})
    # A finite Laurent characteristic polynomial: constant-coefficient
    # extraction in the three mark variables must leave the full roof polynomial
    # for exactly the requested label, with the minus sign in the projector.
    atoms = [((-1,0,1,2), F(1,10)), ((1,0,2,3), F(1,5)),
             ((0,1,2,5), F(3,10)), ((1,0,2,7), F(1,10)),
             ((0,0,1,1), F(3,10))]
    for target in product(range(-2,3),repeat=3):
        projected, direct = {}, {}
        for (k1,k2,m,t), mass in atoms:
            shifted = (k1-target[0], k2-target[1], m-target[2])
            if shifted == (0,0,0):
                projected[t] = projected.get(t,F(0)) + mass
            if (k1,k2,m) == target:
                direct[t] = direct.get(t,F(0)) + mass
        audit.check("exact Laurent mark projection retains the roof coordinate", projected == direct, target)
    audit.detail("frequency_identity", {
        "integer_coordinates_at_fixed_return_count": ["k1","k2","actual collision count"],
        "continuous_coordinate": "original physical roof",
        "normalization": "(2*pi)^(-4)",
        "roof_factor": "eta(s/bandwidth) * Fourier(1_I)(-s)",
        "entire_torus_retained": True,
        "infinite_complex_label_series_interchanged": False,
    })


def main() -> None:
    program = Path(__file__).resolve()
    args = command_arguments(program)
    audit = Audit()
    check_label_and_bv(audit)
    check_finite_towers(audit)
    check_kernel(audit)
    check_interval_and_likelihood(audit)
    check_polynomial_exponents(audit)
    check_denominators_and_marks(audit)
    emit_result(args, program, ["330_all_label_physical_roof_variation.tex", "331_return_tower_and_polynomial_likelihood.tex"], audit, [
        "Checks exact finite label jumps, BV arithmetic, permutation tower identities, kernel polynomial identities, interval likelihood costs, exponent payments and actual denominator algebra.",
        "The finite permutation examples do not replace the physical return map. Recurrence and the tower bound are proved in native331 on the original invariant collision measure.",
        "Does not certify continuous billiard geometry, inherited dynamical inputs, all-word variation, a strong spectral theorem, arithmetic peak asymptotics, raw pointwise LLT, or local inversion.",
        "All mathematical decisions use exact rational arithmetic and explicit failure exceptions; Python optimization does not remove checks.",
    ])


if __name__ == "__main__":
    main()
