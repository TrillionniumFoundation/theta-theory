#!/usr/bin/env python3
"""Finite exact checks for the common qubit learner's algebraic ingredients.

The continuum risk and call-complexity theorem is proved in section 55.
This program does not implement that learner, sample its risk, or certify a
universal probability bound.  It independently expands small GHZ experiments
over the Gaussian rationals and checks rational geometry, budget identities,
and the written algorithm's finite first-rejection transcript contract.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from fractions import Fraction


F = Fraction
ZERO = (F(0), F(0))
ONE = (F(1), F(0))
IMAG = (F(0), F(1))
COUNTS: Counter[str] = Counter()
NEGATIVE: Counter[str] = Counter()


class CheckFailure(RuntimeError):
    """A checked exact identity or explicit precondition failed."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise CheckFailure(label)


def check(condition: bool, category: str, label: str) -> None:
    need(condition, label)
    COUNTS[category] += 1


def reject(operation, category: str, label: str) -> None:
    try:
        operation()
    except CheckFailure:
        NEGATIVE[category] += 1
        return
    raise CheckFailure("negative control was not rejected: " + label)


def c(real=0, imag=0):
    return F(real), F(imag)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    return -a[0], -a[1]


def conj(a):
    return a[0], -a[1]


def mul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def scale(a, s):
    return a[0] * s, a[1] * s


def power(a, n):
    value = ONE
    for _ in range(n):
        value = mul(value, a)
    return value


def matrix_scale(a, s):
    return [[scale(z, s) for z in row] for row in a]


def matrix_add(a, b):
    return [[add(x, y) for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def adjoint(a):
    return [[conj(a[j][i]) for j in range(len(a))] for i in range(len(a[0]))]


def matrix_mul(a, b):
    result = [[ZERO for _ in b[0]] for _ in a]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] = add(result[i][j], mul(a[i][k], b[k][j]))
    return result


def tensor(a, b):
    return [
        [mul(a[i][j], b[k][ell]) for j in range(len(a[0])) for ell in range(len(b[0]))]
        for i in range(len(a))
        for k in range(len(b))
    ]


def tensor_product(factors):
    result = [[ONE]]
    for factor in factors:
        result = tensor(result, factor)
    return result


IDENTITY = [[ONE, ZERO], [ZERO, ONE]]


def effect(b, xyz):
    """Build E from rational Cartesian data, checking exact feasibility."""
    b = F(b)
    x, y, z = map(F, xyz)
    need(abs(b) <= 1, "bias outside [-1,1]")
    need(x * x + y * y + z * z <= (1 - abs(b)) ** 2, "nonlegal effect")
    observable = [[c(b + z), c(x, -y)], [c(x, y), c(b - z)]]
    return matrix_scale(matrix_add(IDENTITY, observable), F(1, 2)), observable


def ghz_expectation(matrix, phase, sign, length):
    """Contract an independently constructed full tensor matrix with a ket.

    The unnormalized ket has entries 1 and sign*phase.  Its squared norm is
    exactly two, so no irrational state amplitude is represented numerically.
    """
    dimension = 2**length
    need(len(matrix) == dimension, "GHZ matrix dimension")
    ket = [ZERO for _ in range(dimension)]
    ket[0] = ONE
    ket[-1] = scale(phase, sign)
    value = ZERO
    support = [i for i, amplitude in enumerate(ket) if amplitude != ZERO]
    for i in support:
        for j in support:
            value = add(value, mul(conj(ket[i]), mul(matrix[i][j], ket[j])))
    need(value[1] == 0, "Hermitian GHZ expectation is real")
    return value[0] / 2


def ghz_checks():
    # The column Gram matrix of either V below is 2I.  Conjugating by
    # V/sqrt(2) is exact over Gaussian rationals after the division by two.
    # For w=z and transverse axes x,y, these give O_01=z+ix and z+iy.
    bases = (
        ("zx", [[ONE, ONE], [neg(IMAG), IMAG]], 0, 1, -1),
        ("zy", [[ONE, ONE], [ONE, neg(ONE)]], 1, 0, 1),
    )
    unit = (F(2, 3), F(2, 3), F(1, 3))
    fixtures = [
        ("zero-effect", F(-1), (F(0),) * 3),
        ("unit-effect", F(1), (F(0),) * 3),
        ("fair-scalar", F(0), (F(0),) * 3),
        ("biased-scalar-positive", F(3, 5), (F(0),) * 3),
        ("biased-scalar-negative", F(-3, 5), (F(0),) * 3),
        ("projective-x", F(0), (F(1), F(0), F(0))),
        ("projective-y", F(0), (F(0), F(1), F(0))),
        ("projective-z", F(0), (F(0), F(0), F(1))),
        ("projective-oblique", F(0), unit),
        ("biased-interior", F(1, 4), (F(1, 4), F(1, 4), F(1, 4))),
        ("negative-biased-interior", F(-1, 4), (F(-1, 4), F(1, 4), F(1, 4))),
    ]
    for name, bias, radius in (
        ("upper-support", F(2, 5), F(3, 5)),
        ("lower-support", F(-2, 5), F(3, 5)),
        ("near-projective", F(1, 256), F(127, 128)),
        ("near-deterministic", F(127, 128), F(1, 128)),
        ("small-contrast", F(1, 2), F(1, 1024)),
    ):
        fixtures.append((name, bias, tuple(radius * t for t in unit)))

    for name, b, xyz in fixtures:
        e, observable = effect(b, xyz)
        check(matrix_add(e, matrix_add(IDENTITY, matrix_scale(e, -1))) == IDENTITY,
              "legal_effects", name + " rows sum to identity")
        for plane, basis, transverse, perpendicular, orientation in bases:
            check(matrix_mul(adjoint(basis), basis) == matrix_scale(IDENTITY, 2),
                  "frame_identities", plane + " orthonormal basis")
            rotated = matrix_scale(matrix_mul(matrix_mul(adjoint(basis), observable), basis), F(1, 2))
            off_diagonal = c(xyz[2], xyz[transverse])
            normal = orientation * xyz[perpendicular]
            check(rotated[0][1] == off_diagonal, "frame_identities", plane + " off-diagonal phase")
            check(rotated[0][0] == c(b + normal) and rotated[1][1] == c(b - normal),
                  "frame_identities", plane + " diagonal bias")
            plus = matrix_scale(matrix_add(IDENTITY, rotated), F(1, 2))
            minus = matrix_add(IDENTITY, matrix_scale(plus, -1))
            for length in range(1, 5):
                parity_tensor = tensor_product([rotated] * length)
                # Actual outcome probabilities are expanded independently for
                # the smaller blocks; the length-four parity matrix is also
                # formed as a full Kronecker product, never by a scalar power.
                outcomes = []
                if length <= 3:
                    for signs in itertools.product((-1, 1), repeat=length):
                        parity = 1
                        for sign in signs:
                            parity *= sign
                        outcomes.append((parity, tensor_product([plus if z == 1 else minus for z in signs])))
                diagonal = ((b + normal) ** length + (b - normal) ** length) / 2
                target_power = power(off_diagonal, length)
                for phase_name, phase in (("real", ONE), ("imaginary", IMAG)):
                    target = mul(phase, target_power)[0]
                    raw = {}
                    for sign in (-1, 1):
                        value = ghz_expectation(parity_tensor, phase, sign, length)
                        raw[sign] = value
                        check(value == diagonal + sign * target, "ghz_tensor_expansions",
                              name + " " + plane + " raw GHZ expansion")
                        check(-1 <= value <= 1, "ghz_bounded_observations", "parity mean in [-1,1]")
                        if outcomes:
                            total = F(0)
                            parity_mean = F(0)
                            for parity, outcome_matrix in outcomes:
                                probability = ghz_expectation(outcome_matrix, phase, sign, length)
                                check(0 <= probability <= 1, "outcome_probabilities", "legal GHZ outcome probability")
                                total += probability
                                parity_mean += parity * probability
                            check(total == 1, "outcome_normalizations", "all GHZ outcomes sum to one")
                            check(parity_mean == value, "outcome_parity_means", "outcome law yields tensor parity")
                    signed_mean = (raw[1] - raw[-1]) / 2
                    check(signed_mean == target, "random_sign_cancellation", "random sign removes diagonal bias")
                    if phase_name == "imaginary":
                        check(signed_mean == -target_power[1], "quadrature_signs", "pi/2 uses negative imaginary part")
                        if target_power[1] != 0 and length <= 2:
                            reject(lambda: need(signed_mean == target_power[1], "incorrect quadrature phase"),
                                   "incorrect_phase", "wrong sign on imaginary quadrature")
                    if diagonal != 0 and phase_name == "real" and length == 2:
                        reject(lambda: need(raw[1] == target, "omitted random sign"),
                               "omitted_random_sign", "single plus GHZ retains diagonal term")
                        unfair_mean = F(3, 4) * raw[1] - F(1, 4) * raw[-1]
                        reject(lambda: need(unfair_mean == target, "unfair sign distribution"),
                               "unfair_random_sign", "nonuniform sign leaves half the diagonal term")
    return len(fixtures)


def radical_upper(value, coefficient, radicand, additive):
    """Decide value <= coefficient*sqrt(radicand)+additive exactly."""
    need(coefficient >= 0 and radicand >= 0, "nonnegative radical comparison")
    remainder = value - additive
    return remainder <= 0 or remainder * remainder <= coefficient * coefficient * radicand


def geometry_checks():
    low_cases = 0
    high_cases = 0
    lambdas = (F(1, 4096), F(1, 128), F(1, 8), F(1))
    cosines = (F(-1), F(-3, 5), F(0), F(3, 5), F(1))
    for bias_numerator in range(-32, 33):
        b = F(bias_numerator, 32)
        for radius_numerator in range(33):
            r = F(radius_numerator, 32)
            if abs(b) + r > 1:
                continue
            w0 = 1 - b * b
            v = (w0 - r * r) / 2
            p, q = (1 + b + r) / 2, (1 + b - r) / 2
            vp, vq = p * (1 - p), q * (1 - q)
            check(v == vp + vq, "spectral_variance_identities", "sum of endpoint variances")
            check(abs(vp - vq) == r * abs(b), "spectral_variance_identities", "endpoint variance difference")
            check(w0 >= r * (2 - r), "feasibility_inequalities", "bias-contrast feasibility")
            for cosine in cosines:
                gamma = r * (1 - cosine) / 2
                splus, sminus = (1 + b + r * cosine) / 2, (1 + b - r * cosine) / 2
                check(splus == p - gamma and sminus == q + gamma,
                      "endpoint_alignment", "misaligned endpoint identity")
                for s, t in ((splus, p), (sminus, q)):
                    check(0 <= s <= 1, "endpoint_alignment", "misaligned Bernoulli parameter is legal")
                    check(abs(s * (1 - s) - t * (1 - t)) <= gamma,
                          "endpoint_variance_lipschitz", "variance perturbation is at most gamma")
                if r:
                    for estimated_radius in (F(0), r / 2, r, 2 * r):
                        error_squared = r * r + estimated_radius**2 - 2 * r * estimated_radius * cosine
                        check(gamma <= r and gamma * r <= error_squared,
                              "normalization_geometry", "gamma bounded by normalized vector error")
                        check(r * r * (2 - 2 * cosine) <= 4 * error_squared,
                              "normalization_geometry", "chord bounded by normalized vector error")
            if r <= F(7, 8):
                low_cases += 1
                check(v >= w0 / 9, "low_contrast_variance", "uniform low-contrast variance relation")
                for vt in (vp, vq):
                    check(w0 <= 4 * vt + 3 * r, "low_contrast_variance", "either endpoint controls w0 plus contrast")
                    for lam in lambdas:
                        gamma_envelope = F(0) if r == 0 else min(r, 18 * (w0 * lam + lam * lam) / r)
                        check(radical_upper(gamma_envelope, F(9), vt * lam, 72 * lam),
                              "gamma_endpoint_bounds", "exact upper envelope obeys endpoint inequality")
                        if r > lam:
                            check(18 * (w0 * lam + lam * lam) / r <= 72 * vt * lam / r + 72 * lam,
                                  "gamma_endpoint_bounds", "large-contrast reduction of gamma bound")
            if r >= F(5, 8):
                high_cases += 1
                nu = 1 - r
                check(r * nu <= v <= nu, "high_contrast_variance", "noise-to-variance comparison")
    return low_cases, high_cases


def ceil_log2_fraction(value):
    need(value > 0, "positive dyadic logarithm argument")
    exponent = 0
    bound = F(1)
    while bound < value:
        bound *= 2
        exponent += 1
    return exponent


def budget_checks():
    horizons = sorted(set(range(1, 257)) | {2**j + offset for j in range(9, 21) for offset in (-1, 0, 1)})
    for horizon in horizons:
        top = 1 << (horizon.bit_length() - 1)
        stages = [1 << j for j in range(top.bit_length())]
        check(top <= horizon < 2 * top, "dyadic_caps", "largest power-two cap")
        check(sum(stages) == 2 * top - 1 <= 2 * horizon, "dyadic_geometric_sums", "exact geometric call sum")
        jmax = len(stages) - 1
        reverse_weight = sum(length * (jmax - j) for j, length in enumerate(stages))
        check(reverse_weight == 2 * top - jmax - 2, "dyadic_geometric_sums", "exact weighted dyadic sum")
        for eta in (F(1, 8), F(1, 64), F(1, 1024)):
            public_log = ceil_log2_fraction(64 / eta)
            check(F(2) ** public_log >= 64 / eta, "dyadic_log_majorants", "rational logarithm majorant")
            per_stage = [length * (public_log + jmax - j + 1) for j, length in enumerate(stages)]
            cost = sum(per_stage)
            check(cost == 2 * top * (public_log + 2) - (public_log + jmax + 3),
                  "dyadic_budget_bounds", "exact public-call cost formula")
            check(cost <= 2 * horizon * (public_log + 2), "dyadic_budget_bounds", "no extra loglog horizon cost")
            allowances = [eta * length / (32 * horizon) for length in stages]
            check(sum(allowances) <= eta / 16, "adaptive_failure_allowances", "finite conditional-union allowance sum")
            ledger = [eta / 8, eta / 8, eta / 16, eta / 8, eta / 16, eta / 16]
            check(sum(ledger) == 9 * eta / 16 < eta,
                  "full_confidence_ledger", "coarse, product vector, dyadic, fine and two endpoint allowances")
            for stop in range(1, len(stages) + 1):
                check(sum(per_stage[:stop]) <= cost, "stopped_record_budgets", "rejection only reduces public budget")
            for length in stages:
                stage_exponent = public_log + jmax - (length.bit_length() - 1) + 1
                check(F(2) ** stage_exponent >= F(64 * horizon, length) / eta,
                      "dyadic_log_majorants", "each stage majorizes its logarithmic confidence cost")
                # zeta^2=c_*^2 delta^2 m/N; its reciprocal is rational.
                delta, cstar = F(1, 128), F(1, 1024)
                zeta_squared = cstar * cstar * delta * delta * length / horizon
                check(F(length) / zeta_squared == F(horizon) / (cstar * cstar * delta * delta),
                      "final_block_budget", "block length cancels in final precision cost")
    return len(horizons)


def phase_guard(z):
    """The total rational guard preceding every principal-argument call."""
    return z[0] > 0 and 8 * abs(z[1]) <= z[0]


def trace_selection(horizon, reports):
    """Finite control-flow model only; reports replace the physical batches.

    Accepted directions are tagged by their producing stage.  No phase is
    numerically reconstructed and no statistical law is simulated here.
    """
    need(horizon >= 1, "positive selection horizon")
    top = 1 << (horizon.bit_length() - 1)
    accepted = None
    trace = []
    length = 1
    while True:
        z1, z2 = reports[length]
        magnitude_ok = all(z[0] ** 2 + z[1] ** 2 >= F(1, 16) for z in (z1, z2))
        guard_ok = all(phase_guard(z) for z in (z1, z2))
        decision = "accept" if magnitude_ok and guard_ok else "amplitude" if not magnitude_ok else "phase"
        trace.append((length, decision))
        if decision != "accept":
            return accepted if accepted is not None else (1, "initial"), trace
        accepted = (length, "updated-at-" + str(length))
        if length == top:
            return accepted, trace
        length *= 2


def validate_stopped_trace(trace):
    """Check the first-rejection contract independently of the trace generator."""
    need(bool(trace) and trace[0][0] == 1, "selection begins at length one")
    previous_length = 0
    rejected = False
    for length, decision in trace:
        need(not rejected, "a stage was tested after first rejection")
        need(length == 1 if previous_length == 0 else length == 2 * previous_length,
             "dyadic successor length")
        need(decision in ("accept", "amplitude", "phase"), "recognized stage decision")
        rejected = decision != "accept"
        previous_length = length


def control_flow_checks():
    a, kappa = F(1, 64), F(1, 64 * 1024)
    rho = F(1, 4) - kappa
    check(rho * (1 - 2 * a * a) - kappa > 8 * (2 * a * rho + kappa),
          "phase_guard_good_events", "accepted-amplitude cone passes the dyadic guard")
    rho, zeta = F(1, 6), a / 100
    check(rho * (1 - a * a / 2) - zeta > 8 * (a * rho + zeta),
          "phase_guard_good_events", "fine-phase cone passes the guard")
    check(32 * kappa / (F(1, 4) - kappa) <= a / 4,
          "phase_update_invariant", "accepted update restores the next-stage cone")
    check(F(3, 4) + a / 100 < F(7, 8) and F(3, 4) - a / 100 > F(5, 8),
          "coarse_branch_overlap", "both branch premises have explicit numerical slack")
    check(F(8 * 4, 500) < 1,
          "coarse_branch_overlap", "pi below four proves the initial angular cone")

    accepted = (c(F(1, 2)), c(F(1, 2)))
    amplitude_boundary = (c(F(1, 4)), c(F(1, 4)))
    guard_boundary = (c(F(1, 2), F(1, 16)), c(F(1, 2), F(-1, 16)))
    rejected_reports = (
        ("amplitude", (c(F(1, 4) - F(1, 1024)), c(F(1, 2)))),
        ("amplitude", (ZERO, c(F(1, 2)))),
        ("phase", (c(F(1, 2), F(1, 8)), c(F(1, 2)))),
        ("phase", (c(F(-1, 2)), c(F(1, 2)))),
    )
    for pair in (accepted, amplitude_boundary, guard_boundary):
        selected, trace = trace_selection(1, {1: pair})
        check(selected == (1, "updated-at-1") and trace == [(1, "accept")],
              "selection_thresholds", "declared threshold and guard equalities are accepted")
    for z in (ZERO, c(-1), c(0, 1), c(F(1, 2), F(1, 8))):
        check(not phase_guard(z), "phase_fallbacks", "zero, branch-cut and out-of-cone estimates fail before argument")

    horizons = sorted(set(range(1, 129)) | {2**j + offset for j in range(8, 21) for offset in (-1, 0, 1)})
    for horizon in horizons:
        top = 1 << (horizon.bit_length() - 1)
        stages = [1 << j for j in range(top.bit_length())]
        reports = {length: accepted for length in stages}
        selected, trace = trace_selection(horizon, reports)
        validate_stopped_trace(trace)
        check(selected == (top, "updated-at-" + str(top)),
              "selection_cap_returns", "all accepted stages return the public cap")
        check([length for length, _ in trace] == stages,
              "selection_cap_returns", "all-accept transcript tests each dyadic stage once")
        for stop_index, rejected_length in enumerate(stages):
            for rejection_type, observation in rejected_reports:
                trial = dict(reports)
                trial[rejected_length] = observation
                selected, trace = trace_selection(horizon, trial)
                validate_stopped_trace(trace)
                expected = (1, "initial") if stop_index == 0 else (
                    stages[stop_index - 1], "updated-at-" + str(stages[stop_index - 1]))
                check(selected == expected, "selection_first_rejection_returns",
                      "first rejection returns the preceding accepted axis or the explicit initial fallback")
                check(trace[-1] == (rejected_length, rejection_type) and len(trace) == stop_index + 1,
                      "selection_no_post_rejection_calls", "no later scale is reached after first rejection")
                check(sum(length for length, _ in trace) <= 2 * horizon,
                      "selection_pathwise_budgets", "every finite transcript obeys the public geometric cap")

    reject(lambda: validate_stopped_trace([(1, "accept"), (2, "amplitude"), (4, "accept")]),
           "continuation_after_rejection", "continuing after amplitude rejection breaks the written contract")
    reject(lambda: validate_stopped_trace([(1, "phase"), (2, "accept")]),
           "continuation_after_rejection", "continuing after the first phase fallback breaks the written contract")
    reject(lambda: validate_stopped_trace([(1, "accept"), (4, "accept")]),
           "skipped_dyadic_update", "a larger scale requires its immediately preceding accepted update")
    return len(horizons)


def negative_geometry_checks():
    for b, xyz in (
        (F(3, 2), (F(0), F(0), F(0))),
        (F(-3, 2), (F(0), F(0), F(0))),
        (F(1, 2), (F(3, 4), F(0), F(0))),
        (F(0), (F(1), F(1), F(0))),
        (F(127, 128), (F(1, 64), F(0), F(0))),
    ):
        reject(lambda b=b, xyz=xyz: effect(b, xyz), "nonlegal_effect", "invalid rational effect")
    def low_variance_without_premise(bias, radius):
        w0 = 1 - bias * bias
        variance = (w0 - radius * radius) / 2
        need(variance >= w0 / 9, "low-contrast premise omitted")

    reject(lambda: low_variance_without_premise(F(0), F(1)),
           "omitted_low_contrast_premise", "projective variance is not bounded below by w0/9")

    def angular_scale_without_cutoff(bias, radius, horizon):
        variance = (1 - bias * bias - radius * radius) / 2
        need(variance > 0, "zero variance denominator")
        return radius * radius * horizon / variance

    reject(lambda: angular_scale_without_cutoff(F(0), F(1), 16),
           "omitted_regularization", "projective angular scale requires its finite-horizon cutoff")


def main():
    fixtures = ghz_checks()
    low_cases, high_cases = geometry_checks()
    horizons = budget_checks()
    transcript_horizons = control_flow_checks()
    negative_geometry_checks()
    print(json.dumps({
        "schema": "gtf77.common-learning-exact-checks/1",
        "status": "success",
        "scope": "Finite exact identities, first-rejection transcript contracts and negative controls; not an implementation of the full learner or a probability-risk certificate.",
        "arithmetic": "Rational and Gaussian-rational arithmetic only; no stochastic simulation or floating-point comparisons.",
        "checks": dict(sorted(COUNTS.items())),
        "negative_controls": dict(sorted(NEGATIVE.items())),
        "total_checks": sum(COUNTS.values()),
        "total_negative_controls": sum(NEGATIVE.values()),
        "fixture_counts": {
            "ghz_effects": fixtures,
            "ghz_planes": 2,
            "ghz_max_block_length": 4,
            "complete_outcome_max_block_length": 3,
            "low_contrast_grid_pairs": low_cases,
            "high_contrast_grid_pairs": high_cases,
            "dyadic_horizons": horizons,
            "first_rejection_transcript_horizons": transcript_horizons,
        },
        "proof_location": "sections/55-common-measurement-learning.tex",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
