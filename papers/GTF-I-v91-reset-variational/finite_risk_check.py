#!/usr/bin/env python3
"""Exact replay regressions; finite examples and mutation controls, not synthesis.

Both scalar grids are exhausted. Dimension-two checks concern local matrix
identities and structural validation only; a full dimension-two grid is not run.
No assertion statements are used, so optimization cannot disable validation.
"""
from __future__ import annotations

import copy
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path
import subprocess
import sys

import sympy as sp

import finite_risk_certificate as fr
import matrix_metric as mm


ROOT = Path(__file__).resolve().parent


def run_checks() -> dict:
    checks = 0
    rejected = []

    def require(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            raise RuntimeError(message)

    def rejects(name, action, exception=ValueError):
        nonlocal checks
        checks += 1
        try:
            action()
        except exception:
            rejected.append(name)
        else:
            raise RuntimeError("negative control escaped: " + name)

    examples = ["finite-risk-scalar-coarse4.json", "finite-risk-scalar-binomial4.json"]
    raws, reports = [], []
    scalar_points = 0
    for filename in examples:
        raw = mm.loads((ROOT / "examples" / filename).read_text(encoding="utf-8"))
        result = fr.replay(raw, max_grid_candidates=100)
        raws.append(raw)
        reports.append(result)
        cert = fr.validate(raw)
        K, count = fr.grid_parameters(cert.dimension, cert.r)
        require(result["status"] == "success" and result["complete_grid"],
                "complete scalar replay must succeed")
        require(result["parameter_class"] == "diagnostic-outside-theorem-range",
                "toy example must not be advertised as theorem-scale synthesis")
        require(result["readout_branches"] == 16 and result["readout_dimension"] == 1,
                "all four-call scalar branches must be present")
        require(result["candidate_tuples_checked"] == count
                and result["legal_grid_points_checked"] == count,
                "complete scalar grid cardinality")
        min_success = Fraction(1)
        # This oracle is the ordinary binomial law, independent of the matrix
        # trace implementation and its grouping of supplied readout effects.
        for numerator in range((K + 3) // 4, (3 * K) // 4 + 1):
            p = Fraction(numerator, K)
            expected = [Fraction(0), Fraction(0), Fraction(0)]
            for s in range(5):
                j = 0 if s <= 1 else 1 if s == 2 else 2
                expected[j] += comb(4, s) * p ** s * (1 - p) ** (4 - s)
            calculated = fr.probabilities(cert, sp.Matrix([[sp.Rational(numerator, K)]]))
            require(tuple(Fraction(str(q)) for q in calculated) == tuple(expected),
                    "exact Choi replay disagrees with independent binomial probabilities")
            a = Fraction(raw["a"])
            success = sum((q for q, centre in zip(expected,
                          [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)])
                          if abs(p - centre) <= a), Fraction(0))
            min_success = min(min_success, success)
            scalar_points += 1
        require(Fraction(result["minimum_grid_success"]) == min_success,
                "risk minimum must agree with independent exhaustive binomial calculation")
        require(Fraction(raw["alpha"]) == 1 - min_success,
                "example alpha records the exact finite-grid worst failure")
        require(Fraction(result["unclipped_failure_bound"])
                == Fraction(raw["alpha"]) + 4 * Fraction(raw["r"]),
                "all-real transfer must include the full m*r buffer")
        require(result["scalar_good_boundary_pairs"] > 0,
                "good-set equality cases must be exercised")
        require(fr.replay(copy.deepcopy(raw), max_grid_candidates=100) == result,
                "identical replay must be deterministic")

    coarse, fine = raws
    require(reports[0]["grid_denominator"] == 32
            and reports[0]["legal_grid_points_checked"] == 17,
            "coarse scalar grid must have exactly 17 points")
    require(reports[1]["grid_denominator"] == 128
            and reports[1]["legal_grid_points_checked"] == 65,
            "resolving scalar grid must have exactly 65 points")
    require(Fraction(reports[1]["certified_operator_radius"]) < Fraction(1, 4)
            and Fraction(reports[1]["certified_failure_bound"]) < 1,
            "second toy must give a nonvacuous all-real operator-risk guarantee")

    def mutated(raw, change):
        out = copy.deepcopy(raw)
        change(out)
        return out

    def structural(name, change, base=coarse):
        rejects(name, lambda: fr.validate(mutated(base, change)))

    structural("missing-binary-branch", lambda x: x["readout"].pop())
    structural("duplicate-or-reordered-branch-label",
               lambda x: x["readout"][1].__setitem__("y", "0000"))
    structural("incorrect-call-count", lambda x: x.__setitem__("calls", 5))
    structural("boolean-dimension", lambda x: x.__setitem__("dimension", True))
    structural("missing-readout-effect", lambda x: x["readout"][0]["effects"].pop())
    structural("wrong-readout-matrix-dimension",
               lambda x: x["readout"][0]["effects"].__setitem__(0, []))
    structural("noncanonical-rational", lambda x: x.__setitem__("r", "2/16"))
    structural("floating-rational", lambda x: x.__setitem__("alpha", 0.25))
    structural("zero-grid-radius", lambda x: x.__setitem__("r", "0"))
    structural("coarse-grid-outside-covering-lemma", lambda x: x.__setitem__("r", "1/3"))
    structural("negative-failure", lambda x: x.__setitem__("alpha", "-1/8"))
    structural("readout-not-positive",
               lambda x: x["readout"][0]["effects"][0][0][0].__setitem__(0, "-1"))
    structural("readout-not-normalized",
               lambda x: x["readout"][0]["effects"][0][0][0].__setitem__(0, "1/2"))
    structural("dictionary-outside-expanded-interior",
               lambda x: x["dictionary"][0][0][0].__setitem__(0, "0"))
    structural("nonreal-diagonal",
               lambda x: x["dictionary"][0][0][0].__setitem__(1, "1/16"))
    structural("wrong-transpose-convention",
               lambda x: x.__setitem__("choi_convention", "E^dagger instead of E^T"))
    structural("supplied-grid-is-not-trusted", lambda x: x.__setitem__("grid", []))
    structural("supplied-probability-is-not-trusted",
               lambda x: x["readout"][0].__setitem__("probability", "1"))
    structural("target-without-horizon", lambda x: x.update(
        horizon=None, target={"accuracy": "1/2", "failure": "1/2"}))
    rejects("duplicate-json-keys", lambda: mm.loads('{"schema":"a","schema":"b"}'))
    rejects("nonfinite-json-number", lambda: mm.loads('{"number":NaN}'))
    bad_risk = mutated(coarse, lambda x: x.__setitem__(
        "alpha", str(sp.Rational(x["alpha"]) - sp.Rational(1, 2 ** 40))))
    rejects("strictly-understated-grid-risk", lambda: fr.replay(bad_risk),
            fr.InvalidCertificate)
    rejects("whole-grid-budget-too-small", lambda: fr.replay(
        coarse, max_grid_candidates=16), fr.IncompleteVerification)
    require(fr.replay(coarse, max_grid_candidates=17)["complete_grid"],
            "exact whole-grid budget must succeed")
    targeted = mutated(fine, lambda x: x.__setitem__(
        "target", {"accuracy": "5/8", "failure": "4/5"}))
    require(fr.replay(targeted, max_grid_candidates=65)["target_risk_certified"] is True,
            "an optional target must be certified by the actual transfer bounds")
    impossible_target = mutated(coarse, lambda x: x.__setitem__(
        "target", {"accuracy": "1/8", "failure": "1/8"}))
    rejects("target-stronger-than-certified-transfer", lambda: fr.replay(impossible_target))

    # Nonmultiple-of-four K exercises ceiling endpoints and complete enumeration.
    K, count = fr.grid_parameters(1, sp.Rational(3, 20))
    actual = list(fr.grid_tuples(1, K))
    require(K == 27 and count == 14 and len(actual) == count,
            "rational radius must use exact integer ceiling for K")
    require(actual[0][0, 0] == sp.Rational(7, 27)
            and actual[-1][0, 0] == sp.Rational(20, 27),
            "nonintegral scalar boundary coordinates must be rounded inward")
    require(all(fr.in_interval(G, sp.Rational(1, 4), sp.Rational(3, 4))
                for G in actual), "all scalar grid points must be interior")

    # Complex local identities distinguish transpose from adjoint. This is not
    # an exhaustion of a two-dimensional certificate grid.
    E = sp.Matrix([[sp.Rational(1, 2), sp.I / 8],
                   [-sp.I / 8, sp.Rational(1, 2)]])
    A = sp.Matrix([[sp.Rational(1, 2), sp.I / 2],
                   [-sp.I / 2, sp.Rational(1, 2)]])
    identity = sp.eye(2)
    local = {
        "schema": fr.SCHEMA, "dimension": 2, "calls": 1, "horizon": 1,
        "a": "1/8", "r": "1/4", "alpha": "5/8",
        "choi_convention": fr.CONVENTION,
        "dictionary": [mm.matrix_to_json(E), mm.matrix_to_json(identity - E)],
        "readout": [
            {"y": "0", "effects": [mm.matrix_to_json(identity - A), mm.matrix_to_json(A)]},
            {"y": "1", "effects": [mm.matrix_to_json(A), mm.matrix_to_json(identity - A)]}],
        "target": None,
    }
    local_cert = fr.validate(local)
    require(fr.probabilities(local_cert, E) == (sp.Rational(3, 8), sp.Rational(5, 8)),
            "complex reference experiment must use the transposed effect")
    require(sp.trace(A * fr.choi_block(E, "1")) == sp.Rational(3, 16),
            "one Choi block has the required d^-1 normalization and transpose")
    require(sp.trace(A * E / 2) == sp.Rational(5, 16),
            "intentional adjoint/no-transpose control must give a different answer")
    blocks = [fr.choi_block(E, "".join(bits)) for bits in product("01", repeat=2)]
    require(all(mm.is_positive_semidefinite(R) for R in blocks),
            "every complex two-call Choi block must be PSD")
    require(sum((R for R in blocks), sp.zeros(4)) == sp.eye(4) / 4,
            "sum of two-call subnormalized blocks must be I/d^m")
    require(sum(sp.trace(R) for R in blocks) == 1,
            "all classical branch probabilities must normalize")
    require(fr.choi_block(E, "10")
            == sp.kronecker_product(E.transpose(), (identity - E).transpose()) / 4,
            "the string order must fix tensor order")
    require(fr.choi_block(E, "10") != fr.choi_block(E, "01"),
            "chosen example must detect a reversal of tensor factors")
    require(mm.is_positive_semidefinite(A) and mm.is_positive_semidefinite(identity - A),
            "singular but legal POVM effects must be accepted")
    require(not mm.is_positive_semidefinite(sp.Matrix([[0, 1], [1, 1]])),
            "zero-pivot row condition must reject a hidden negative direction")
    require(not mm.is_positive_semidefinite(sp.Matrix([[1, 2], [2, 1]])),
            "positive diagonal entries alone must not establish positivity")
    require(fr.op_leq(E - identity / 2, sp.Rational(1, 8))
            and not fr.op_leq(E - identity / 2, sp.Rational(1, 9)),
            "matrix norm boundary must be closed and its strict exterior rejected")
    structural("non-Hermitian-complex-readout", lambda x:
               x["readout"][0]["effects"][0][1][0].__setitem__(1, "-1/2"), local)
    structural("indefinite-complex-readout", lambda x:
               x["readout"][0]["effects"].__setitem__(0,
                   mm.matrix_to_json(sp.Matrix([[0, 1], [1, 1]]))), local)
    rejects("dimension-two-grid-is-explicitly-incomplete",
            lambda: fr.replay(local, max_grid_candidates=1), fr.IncompleteVerification)

    # Verify machine-facing status and exit behavior. Optimization must not
    # alter acceptance, parsing, counters, or deterministic report fields.
    example_path = ROOT / "examples" / examples[0]
    command = [str(ROOT / "finite_risk_certificate.py"), str(example_path),
               "--max-grid-candidates", "17"]
    normal = subprocess.run([sys.executable, *command], capture_output=True, text=True,
                            check=False)
    optimized = subprocess.run([sys.executable, "-O", *command], capture_output=True,
                               text=True, check=False)
    require(normal.returncode == 0 and optimized.returncode == 0,
            "complete-grid CLI must succeed with and without Python optimization")
    require(normal.stdout == optimized.stdout and not normal.stderr and not optimized.stderr,
            "optimized CLI output must be byte-for-byte identical")
    incomplete = subprocess.run([sys.executable, *command[:-1], "16"],
                                capture_output=True, text=True, check=False)
    require(incomplete.returncode == 2
            and mm.loads(incomplete.stdout)["status"] == "incomplete"
            and mm.loads(incomplete.stdout)["complete_grid"] is False,
            "resource cutoff must have a non-success exit and incomplete status")

    return {
        "schema": "gtf81.finite-risk-regressions/1", "status": "success",
        "checks": checks, "negative_controls": rejected,
        "complete_scalar_certificates": len(reports),
        "independently_checked_scalar_grid_points": scalar_points,
        "scalar_replays": reports,
        "complex_dimension_two_local_identities_checked": True,
        "complete_dimension_two_grid_executed": False,
        "general_optimal_learner_synthesis_executed": False,
        "optimized_cli_output_identical": True,
        "scope": ("Finite exact arithmetic regressions and complete scalar certificate "
                  "replays, with structural, convention, risk and incompleteness "
                  "negative controls; not a proof by finite experimentation."),
    }


def main() -> int:
    print(json.dumps(run_checks(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
