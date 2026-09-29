#!/usr/bin/env python3
"""Independent finite diagnostics for the external A2 v23 referee review.

The script imports no author verification code.  It checks finite algebra and
probability inequalities used in the laboratory-square preparation, histogram
balance, witness extraction, adaptive arrival, completion defect, and stopping
cost arguments.  It does not execute the physical scanner, verify analytic
continuation, build TeX, certify the full proof, or make an editorial decision.
"""
from __future__ import annotations

from fractions import Fraction as F
import json
import math
import random

REVIEWED_COMMIT = "b3453e025f01f0e1089878f8dd4bf57fc15f3aab"
COUNTS: dict[str, int] = {}


def check(group: str, condition: bool, detail: object = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] = COUNTS.get(group, 0) + 1


def total_variation(p: list[F], q: list[F]) -> F:
    return sum(abs(a - b) for a, b in zip(p, q)) / 2


def boundary_layer_checks() -> None:
    # Exact inequalities behind the large-square preparation proposition.
    for b in range(1, 21):
        for multiplier in range(2, 31):
            length = b * multiplier
            boundary_area = 4 * length * length - 4 * (length - b) ** 2
            check(
                "boundary_strip_area",
                boundary_area <= 8 * length * b,
                (b, length),
            )
            for area_lower, covolume_upper in (
                (1, 1),
                (1, 2),
                (2, 3),
                (3, 5),
                (5, 8),
            ):
                mixture_bound = F(
                    8 * length * b * covolume_upper,
                    area_lower * 4 * (length - b) ** 2,
                )
                displayed_bound = F(
                    8 * covolume_upper * b,
                    area_lower * length,
                )
                check(
                    "boundary_mixture_constant",
                    mixture_bound <= displayed_bound,
                    (b, length, area_lower, covolume_upper),
                )
                acceptance = F(area_lower, covolume_upper) * F(
                    (length - b) ** 2, length**2
                )
                check(
                    "free_launch_lower_bound",
                    acceptance >= F(area_lower, 4 * covolume_upper),
                    (b, length, area_lower, covolume_upper),
                )

    # Deterministic post-processing cannot increase total variation.
    rng = random.Random(20260929)
    for states in range(2, 11):
        for trial in range(100):
            raw = [rng.randint(1, 20) for _ in range(states)]
            total = sum(raw)
            base = [F(value, total) for value in raw]
            raw_other = [rng.randint(1, 20) for _ in range(states)]
            total_other = sum(raw_other)
            other = [F(value, total_other) for value in raw_other]
            weight = F(rng.randint(0, 10), 10)
            mixture = [
                (1 - weight) * base[index] + weight * other[index]
                for index in range(states)
            ]
            check(
                "mixture_tv_bound",
                total_variation(base, mixture) <= weight,
                (states, trial),
            )

            outputs = rng.randint(1, states)
            mapping = [rng.randrange(outputs) for _ in range(states)]
            base_push = [F(0) for _ in range(outputs)]
            mixture_push = [F(0) for _ in range(outputs)]
            for index, target in enumerate(mapping):
                base_push[target] += base[index]
                mixture_push[target] += mixture[index]
            check(
                "gate_tv_contraction",
                total_variation(base_push, mixture_push)
                <= total_variation(base, mixture),
                (states, trial),
            )


def histogram_balance_checks() -> None:
    for beta in (
        F(1, 10),
        F(1, 8),
        F(1, 6),
        F(1, 4),
        F(1, 3),
        F(1, 2),
        F(2, 3),
        F(3, 4),
        F(1),
    ):
        denominator = 2 * beta + 6
        target = beta / denominator
        check(
            "histogram_bias_variance_balance",
            target == F(1, 2) - F(3) / denominator,
            beta,
        )
        check(
            "preparation_bias_balance",
            (beta + 4) / denominator - F(4) / denominator == target,
            beta,
        )
        linear_exponent = F(1) - F(4) / denominator
        check(
            "linear_bernstein_smaller",
            linear_exponent > target,
            beta,
        )


def hazard_and_stopping_checks() -> None:
    # Adaptive product bounds used in the arrival lemma.
    for horizon in range(1, 101):
        for offset in range(1, 10):
            probabilities = [
                (offset + (epoch % 3)) / (50 + epoch)
                for epoch in range(1, horizon + 1)
            ]
            product = 1.0
            cumulative = 0.0
            for probability in probabilities:
                product *= 1 - probability
                cumulative += probability
            check(
                "varying_hazard_exponential_bound",
                product <= math.exp(-cumulative) + 1e-15,
                (horizon, offset),
            )

    for horizon in range(1, 101):
        for numerator in range(1, 10):
            probability = numerator / 20
            check(
                "uniform_hazard_bound",
                (1 - probability) ** horizon
                <= math.exp(-probability * horizon) + 1e-15,
                (horizon, probability),
            )

    for cutoff in (1, 2, 5, 10, 100, 1000, 10000):
        spent = sum(
            1 / (8 * (epoch + 1) ** 6)
            for epoch in range(1, cutoff + 1)
        )
        check("summable_error_budget", spent < 1 / 8, (cutoff, spent))

    # A k^3 cost is integrable against the k^-6 plus exponential tail.
    for probability in (0.01, 0.02, 0.05, 0.1, 0.2, 0.5):
        for witness_size in (1, 2, 5, 10):
            partial = sum(
                epoch**3
                * (
                    1 / (8 * (epoch + 1) ** 6)
                    + witness_size * math.exp(-probability * epoch)
                )
                for epoch in range(1, 20000)
            )
            generous_bound = sum(
                epoch**3 / (8 * (epoch + 1) ** 6)
                for epoch in range(1, 20000)
            ) + witness_size * (
                6 / probability**4 + 1 / probability**3 + 1
            )
            check(
                "finite_expected_launch_cost",
                partial < generous_bound,
                (probability, witness_size),
            )

    # Exact coupon controls in small finite models.
    for witness_size in range(1, 8):
        for denominator in (10, 20, 50):
            probability = F(1, denominator)
            if witness_size * probability >= 1:
                continue
            for horizon in (1, 2, 3, 5, 10, 20, 50):
                exact_missing = F(0)
                for subset_size in range(1, witness_size + 1):
                    exact_missing += (
                        (-1) ** (subset_size + 1)
                        * math.comb(witness_size, subset_size)
                        * (1 - subset_size * probability) ** horizon
                    )
                union_bound = witness_size * (1 - probability) ** horizon
                check(
                    "coupon_union_bound_exact",
                    exact_missing <= union_bound,
                    (witness_size, denominator, horizon),
                )
                check(
                    "coupon_exponential_tail",
                    float(union_bound)
                    <= witness_size
                    * math.exp(-float(probability) * horizon)
                    + 1e-15,
                    (witness_size, denominator, horizon),
                )

    # Cover absence and current-epoch error need only a union bound.
    for absent_numerator in range(0, 101):
        absent = F(absent_numerator, 100)
        for failure_numerator in range(0, 51):
            failure = F(failure_numerator, 1000)
            check(
                "current_epoch_union_bound",
                min(F(1), absent + failure) <= absent + failure,
                (absent, failure),
            )


def witness_and_proposal_checks() -> None:
    # Proper divisors halve the current index in the worst case.
    for index in range(2, 2001):
        for divisor in range(1, index):
            if index % divisor == 0:
                check(
                    "proper_divisor_halves_index",
                    divisor <= index // 2,
                    (index, divisor),
                )
        value = index
        steps = 0
        while value > 1:
            divisors = [
                candidate
                for candidate in range(1, value)
                if value % candidate == 0
            ]
            value = max(divisors)
            steps += 1
        check(
            "logarithmic_index_chain",
            steps <= math.floor(math.log2(index)),
            (index, steps),
        )

    # Selection among M ordered pairs dominates the M0 lower bound.
    for maximum in range(2, 101):
        lower = F(1, maximum * (maximum - 1))
        for actual in range(2, maximum + 1):
            check(
                "producer_pair_probability",
                F(1, actual * (actual - 1)) >= lower,
                (actual, maximum),
            )


def completion_defect_checks() -> None:
    # Finite exact models of the retained missing-area/index identity.
    for covolume in range(1, 31):
        for subgroup_index in range(1, 11):
            for visible_area in range(0, 11):
                for hidden_area in range(0, 11):
                    if visible_area + hidden_area >= covolume:
                        continue
                    free_area = covolume - visible_area - hidden_area
                    defect = (
                        subgroup_index * covolume
                        - free_area
                        - visible_area
                    )
                    decomposition = (
                        (subgroup_index - 1) * covolume + hidden_area
                    )
                    check(
                        "completion_defect_identity",
                        defect == decomposition,
                        (covolume, subgroup_index, visible_area, hidden_area),
                    )
                    check(
                        "completion_defect_nonnegative",
                        defect >= 0,
                        (covolume, subgroup_index, visible_area, hidden_area),
                    )
                    check(
                        "completion_zero_characterization",
                        (defect == 0)
                        == (subgroup_index == 1 and hidden_area == 0),
                        (covolume, subgroup_index, visible_area, hidden_area),
                    )


def launch_and_resource_checks() -> None:
    # Representative checks for the displayed Chernoff budget.
    for accepted in (1, 2, 5, 10, 20, 50, 100, 500, 1000):
        for probability in (0.01, 0.02, 0.05, 0.1, 0.2, 0.25):
            for alpha in (1e-1, 1e-2, 1e-4, 1e-8):
                attempts = math.ceil(
                    8 * (accepted + math.log(1 / alpha)) / probability
                )
                mean = attempts * probability
                chernoff = math.exp(-mean * (7 / 8) ** 2 / 2)
                check(
                    "launch_chernoff_budget",
                    accepted <= mean / 8 + 1e-12
                    and chernoff <= alpha + 1e-15,
                    (accepted, probability, alpha),
                )

    for horizon in range(1, 2001):
        preparations = sum(
            epoch * (epoch + 1) ** 2
            for epoch in range(1, horizon + 1)
        )
        check(
            "epoch_preparation_polynomial",
            preparations <= (horizon + 1) ** 4,
            horizon,
        )
        delta = 1e-3
        logarithmic_budget = sum(
            math.log(8 * (epoch + 1) ** 6 / delta)
            for epoch in range(1, horizon + 1)
        )
        comparison = (
            20 * (horizon + 1) * math.log((horizon + 1) / delta)
        )
        check(
            "epoch_launch_log_budget",
            logarithmic_budget <= comparison,
            horizon,
        )


def main() -> None:
    boundary_layer_checks()
    histogram_balance_checks()
    hazard_and_stopping_checks()
    witness_and_proposal_checks()
    completion_defect_checks()
    launch_and_resource_checks()
    result = {
        "schema": "a2-v23-independent-review-diagnostics-1",
        "reviewed_commit": REVIEWED_COMMIT,
        "status": "passed",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "scope": (
            "finite algebra and probability inequalities for the new v23 "
            "preparation, discovery, stopping, and retained defect arguments"
        ),
        "imports_author_verification_code": False,
        "executes_physical_scanner": False,
        "tex_build": False,
        "formal_proof_certificate": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
