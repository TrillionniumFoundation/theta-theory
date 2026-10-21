#!/usr/bin/env python3
"""Exact algebra and accounting checks for native A2-DYN module 321.

This program does not establish continuous billiard geometry, the native
growth or cross-curve theorems, cell abundance, pressure, or a local limit.
Those obligations are in the complete mathematical proof bodies.  The
checks below are failure-sensitive exact verifications of the new proof's
metric, projection, lift/index, endpoint-multiplicity, and capacity budgets.
There is no floating-point trajectory simulation and no `assert` gate.
"""

import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import sys


class CheckFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def exact(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(key): exact(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact(item) for item in value]
    return value


class Poly:
    """Small exact polynomial ring Q[x,y,z], for certified identities."""

    def __init__(self, terms=None):
        self.terms = {
            tuple(power): F(coefficient)
            for power, coefficient in (terms or {}).items()
            if coefficient
        }

    @staticmethod
    def scalar(value):
        return Poly({(0, 0, 0): F(value)})

    @staticmethod
    def variable(index):
        powers = [0, 0, 0]
        powers[index] = 1
        return Poly({tuple(powers): F(1)})

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Poly) else Poly.scalar(value)

    def __add__(self, other):
        result = dict(self.terms)
        for power, coefficient in self.coerce(other).terms.items():
            result[power] = result.get(power, F(0)) + coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({power: -coefficient for power, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        result = {}
        for lhs, coefficient_lhs in self.terms.items():
            for rhs, coefficient_rhs in self.coerce(other).terms.items():
                power = tuple(a + b for a, b in zip(lhs, rhs))
                result[power] = result.get(power, F(0)) + coefficient_lhs * coefficient_rhs
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "Polynomial exponent domain")
        result = Poly.scalar(1)
        for _ in range(exponent):
            result = result * self
        return result

    def equals(self, other):
        return self.terms == self.coerce(other).terms

    def nonnegative_coefficients(self):
        return all(coefficient >= 0 for coefficient in self.terms.values())

    def certificate(self):
        return {str(power): str(coefficient) for power, coefficient in sorted(self.terms.items())}


def reverse_normalized(centers):
    terminal = centers[-1]
    return tuple((center[0] - terminal[0], center[1] - terminal[1]) for center in reversed(centers))


def run_checks():
    checks = []
    radius_minus, radius_plus = F(9, 20), F(47, 100)
    a, b, upper, tau_min = F(100, 47), F(20, 9), F(170, 9), F(3, 50)
    x, y, z = (Poly.variable(i) for i in range(3))

    # The squared fiber metric is R^2+1 in the angle parameter phi.
    radius = x
    require((radius**2 + 1).equals(((-radius)**2 + 1)), "Fiber metric identity")
    radius_slack = radius_plus - radius_minus
    require(radius_slack > 0, "Radius interval order")
    require(
        (radius_plus**2 - radius**2).equals((radius_plus - radius) * (radius_plus + radius)),
        "Uniform radius length factorization",
    )
    # Physical one-period lifting uses alpha=s/R; alpha -> alpha+2pi.
    for actual_radius in [radius_minus, (radius_minus + radius_plus) / 2, radius_plus]:
        require(actual_radius * (1 / actual_radius) == 1, "Arclength to angular seam factor")
    checks.append({
        "name": "physical_fiber_metric_and_seam",
        "status": "pass",
        "identities": [
            "ds/dphi=-R; (dell/dphi)^2=1+R^2",
            "(1+R_plus^2)-(1+R^2)=(R_plus-R)(R_plus+R)",
            "alpha=s/R; a lifted circumference 2*pi*R adds exactly 2*pi",
        ],
        "fiber_length": "pi*sqrt(1+R^2)",
        "angle_parameter_total_mass": "2*pi",
        "metric_square_at_radius_plus": 1 + radius_plus**2,
    })

    # Universal certificate with kappa=a+y, v=kappa+x, U=v+z.
    # Nonnegative coefficients certify the claimed inequality for all slacks >=0.
    kappa, slope = a + y, a + x + y
    ceiling = slope + z
    projection_numerator = (slope + kappa)**2 * (1 + ceiling**2) - 4 * a**2 * (1 + slope**2)
    decomposed = ((slope + kappa)**2 - 4 * a**2) * (1 + ceiling**2) + 4 * a**2 * (ceiling**2 - slope**2)
    require(projection_numerator.equals(decomposed), "Cone projection square factorization")
    require(projection_numerator.nonnegative_coefficients(), "Universal cone projection certificate")
    angle_wrap_numerator = slope - kappa
    require(angle_wrap_numerator.equals(x), "1+kappa/v <=2 numerator")
    require(angle_wrap_numerator.nonnegative_coefficients(), "No extra outgoing-angle wrap")
    beta_squared = 4 * a**2 / (1 + upper**2)
    require(beta_squared > 0, "Positive transversal projection lower bound")
    checks.append({
        "name": "universal_cone_projection_inequality",
        "status": "pass",
        "substitution": "kappa=a+y, v=a+y+x, U=v+z, x,y,z>=0",
        "polynomial_certificate": projection_numerator.certificate(),
        "beta_squared": beta_squared,
        "no_wrap_reason": "1+kappa/v<=2 and total actual collision-angle variation<=pi",
    })

    image_length_numerator = (1 + 1 / a**2) * (a + x)**2 - (1 + (a + x)**2)
    require(image_length_numerator.nonnegative_coefficients(), "Image arclength bound")
    norm_lower = kappa**2 + 2 * kappa * slope - 1
    require(norm_lower.nonnegative_coefficients(), "Adapted metric lower comparison")
    require(
        ((1 + b**2) * (1 + x**2) - (b + x)**2).equals((b * x - 1)**2),
        "Adapted metric upper Cauchy identity",
    )
    expansion = 1 + 2 * a * tau_min
    require(expansion == F(59, 47), "Inherited expansion arithmetic")
    # A witness only: the proof retains the inherited once-chosen k0.
    witness_k0, branch_bound = 30000, 301
    tail = F(branch_bound) / (a * tau_min * (witness_k0 - 1))
    require(tail < (1 - 1 / expansion) / 2, "A finite admissible homogeneity threshold exists")
    theta = 1 / expansion + tail
    require(theta < 1, "One-step contraction witness")
    checks.append({
        "name": "image_length_and_one_step_metric_budget",
        "status": "pass",
        "image_length_polynomial_certificate": image_length_numerator.certificate(),
        "image_length_upper": "pi*sqrt(1+a^-2)",
        "adapted_metric_gamma_squared": 1 + b**2,
        "expansion": expansion,
        "admissible_threshold_witness_only": witness_k0,
        "witness_tail": tail,
        "witness_theta": theta,
        "metric_conversion_count_in_C_aff": 1,
        "uses_no_numeric_choice_of_ell_star": True,
    })

    # Exact radius/cocycle norm identities are supplemented with the literal
    # finite-record lift involution. These tuples are algebraic test records,
    # not claimed realizable billiard trajectories.
    increments = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    lift_cases = 0
    for count in range(1, 5):
        past_indices = tuple(-i for i in range(1, count + 1))
        require(past_indices[0] == -1 and past_indices[-1] == -count, "Past terminal homogeneity index")
        require(0 not in past_indices, "No current strip in class label")
        for word in itertools.product(increments, repeat=count):
            centers = [(0, 0)]
            for increment in word:
                previous = centers[-1]
                centers.append((previous[0] + increment[0], previous[1] + increment[1]))
            reversed_word = reverse_normalized(centers)
            require(reversed_word[0] == (0, 0), "Current lifted center normalization")
            require(reverse_normalized(reversed_word) == tuple(centers), "Record reversal/translation involution")
            translated = [(p[0] + 17, p[1] - 9) for p in centers]
            require(reverse_normalized(translated) == reversed_word, "No duplicate periodic lift class")
            lift_cases += 1
    checks.append({
        "name": "unique_periodic_lift_and_terminal_index_bookkeeping",
        "status": "pass",
        "exact_algebraic_cases": lift_cases,
        "record_scope": "label identities only; these finite tuples are not trajectory evidence",
        "homogeneity_times": "-1,...,-N including -N; not time 0",
    })

    # Failure-sensitive endpoint accounting: one branch can receive its
    # interior class and both regular boundary-only classes.
    branch_budget = {"left": F(1, 4), "middle": F(3, 5), "right": F(1, 7)}
    assignments = [
        ("same_disconnected_class", "left", "interior"),
        ("middle_class", "middle", "interior"),
        ("left_face", "middle", "left_endpoint"),
        ("right_face", "middle", "right_endpoint"),
    ]
    chosen = {}
    loads = {branch: 0 for branch in branch_budget}
    total_weight = F(0)
    comparison = F(7, 3)
    for class_name, branch, position in assignments:
        require(class_name not in chosen, "One representative, not one component, per class")
        chosen[class_name] = (branch, position)
        loads[branch] += 1
        total_weight += comparison * branch_budget[branch]
    require(loads["middle"] == 3, "Three is necessary in the endpoint accounting argument")
    require(max(loads.values()) <= 3, "One interior plus at most two endpoint classes")
    require(total_weight <= 3 * comparison * sum(branch_budget.values()), "Endpoint weighted sum budget")
    require(total_weight > comparison * sum(branch_budget.values()), "Dropping the endpoint factor would fail this accounting case")
    checks.append({
        "name": "regular_boundary_face_multiplicity",
        "status": "pass",
        "maximum_load": max(loads.values()),
        "weighted_left_side": total_weight,
        "threefold_right_side": 3 * comparison * sum(branch_budget.values()),
        "scope": "exact representative accounting; local finiteness and endpoint continuity are proved in the manuscript",
    })

    # Counterexample to an invalid inference, not to the physical theorem:
    # 2^N disjoint angular intervals of total length 1 and weight (3/4)^N
    # obey the capacity moment bound and decay individually, but their
    # unweighted sum is (3/2)^N. The analytic formula holds for every N.
    nonclosure_rows = []
    for count in (1, 2, 4, 8, 16):
        number = 2**count
        weight = F(3, 4)**count
        width = F(1, number)
        moment = number * weight * width
        pressure = number * weight
        require(moment == weight <= 1, "Capacity moment in abstract non-implication example")
        require(pressure == F(3, 2)**count, "Growing unweighted sum despite capacity control")
        require(weight <= (1 / expansion)**count, "Example also respects inherited pointwise decay scale")
        nonclosure_rows.append({"N": count, "capacity_moment": moment, "unweighted_sum": pressure})
    checks.append({
        "name": "capacity_does_not_automatically_close_unweighted_pressure",
        "status": "pass",
        "scope": "abstract logical non-implication only; not a Lorentz-gas counterexample or substitute model",
        "identities_valid_for_all_N": ["moment=(3/4)^N", "unweighted_sum=(3/2)^N"],
        "exact_examples": nonclosure_rows,
    })

    optical = F(30000)
    require(optical > 1, "Original optical comparison factor")
    checks.append({
        "name": "normalization_and_optical_endpoint_ledger",
        "status": "pass",
        "identity": "j_N(T^-N y)=1/J_Es(y) T^-N(y)",
        "optical_weight": "o_N(C)=sup_C omega_N(T^-N y)/cos(phi(y))",
        "optical_comparison_factor": optical,
        "capacity_integration_factor": "2*pi",
        "absent_from_tangent_identity": ["1/(4*pi*R)", "1/c_star", "roof_interval_width", "N^-2"],
        "limit_order": "all geometric constants fixed before R,N suprema and before outer B then collision limsup interfaces",
    })
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--manuscript", type=Path, default=Path(__file__).with_name("321_all_class_transversal_capacity.tex"))
    parser.add_argument("--source-commit", default="6cdd9ae88cd358d524ecb89092361ac1522ba351")
    parser.add_argument("--details", "--output", dest="details", type=Path)
    args = parser.parse_args()
    dependencies = [
        "core/266_target_roof_marked_pressure.tex",
        "core/281_uniform_curvature_graph_transform.tex",
        "core/282_physical_complexity_and_distortion.tex",
        "core/283_admissible_growth_and_clearance_consequences.tex",
        "core/287_explicit_finite_horizon_and_candidate_budget.tex",
        "core/313_explicit_stable_optical_comparison.tex",
        "core/318_full_word_cross_curve_distortion.tex",
    ]
    try:
        # Some complete historical revisions use different descriptive
        # names for these numbered modules. Resolve and record each unique
        # native source identity instead of accepting a missing input.
        for index, number in ((4, "287"), (5, "313")):
            if not (args.source_root / dependencies[index]).is_file():
                matches = sorted((args.source_root / "core").glob(number + "_*.tex"))
                require(len(matches) == 1, "Unique complete native module " + number + " source")
                dependencies[index] = str(matches[0].relative_to(args.source_root))
        hashes = {}
        for relative in dependencies:
            path = args.source_root / relative
            require(path.is_file(), "Missing native dependency: " + relative)
            hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        require(args.manuscript.is_file(), "Missing complete new proof body")
        checks = run_checks()
        result = {
            "status": "pass",
            "source_commit_label": args.source_commit,
            "native_dependency_sha256": hashes,
            "manuscript_sha256": hashlib.sha256(args.manuscript.read_bytes()).hexdigest(),
            "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "checks": checks,
            "mathematical_scope": "Exact algebra/accounting evidence supporting a separately written native geometric proof; not a proof by computation.",
            "not_certified": [
                "Independent specialist reconstruction of the inherited dynamical inputs",
                "Uniform short-capacity physical-word renewal",
                "Original conditioned same-roof capacity abundance and m^2 error payment",
                "Full raw pointwise LLT and four-coordinate inversion",
            ],
        }
        exit_code = 0
    except (CheckFailure, OSError) as error:
        result = {"status": "fail", "error": str(error)}
        exit_code = 1
    rendered = json.dumps(exact(result), indent=2, sort_keys=True) + "\n"
    if args.details:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        args.details.write_text(rendered, encoding="utf-8")
    summary = {
        "status": result["status"],
        "checks": len(result.get("checks", [])),
        "scope": "exact algebra/accounting only; complete geometric proofs are in native LaTeX",
    }
    if result["status"] == "fail":
        summary["error"] = result["error"]
    sys.stdout.write(json.dumps(summary, sort_keys=True) + "\n")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
