#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((row[j] * vector[j] for j in range(len(vector))), Fraction(0)) for row in matrix]


def solve_fraction(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    n = len(rhs)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col] != 0)
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        piv = aug[col][col]
        aug[col] = [value / piv for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor:
                aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(n + 1)]
    return [aug[i][-1] for i in range(n)]


class Round43SourceTests(unittest.TestCase):
    def test_publication_unit_is_materialized(self) -> None:
        required = [
            "ROUND43_REVISION.tex",
            "AUTHOR_RESPONSE_ROUND42.md",
            "ROUND43_REVIEW_INDEX.md",
            "ROUND43_READY_FOR_REVIEW.md",
            "round43/introduction.tex",
            "round43/triangular.tex",
            "round43/lattice.tex",
            "round43/filter_memory.tex",
            "round43/infinite_jacobi.tex",
            "round43/quantitative_jacobi.tex",
            "round43/effective_inversion_details.tex",
            "round43/linear_time_protocol.tex",
            "round43/preparations.tex",
            "round43/appendix_uniformity.tex",
            "round43/references.tex",
            "round43/PROOF_LEDGER.json",
            "round43/HISTORICAL_REUSE.md",
        ]
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_main_inputs_every_article_source(self) -> None:
        text = (ROOT / "ROUND43_REVISION.tex").read_text(encoding="utf-8")
        for relative in (
            "round43/introduction.tex",
            "round43/triangular.tex",
            "round43/lattice.tex",
            "round43/filter_memory.tex",
            "round43/infinite_jacobi.tex",
            "round43/quantitative_jacobi.tex",
            "round43/effective_inversion_details.tex",
            "round43/linear_time_protocol.tex",
            "round43/preparations.tex",
            "round43/appendix_uniformity.tex",
            "round43/references.tex",
        ):
            self.assertIn(f"\\input{{{relative}}}", text)

    def test_round40_gaps_are_landed(self) -> None:
        lattice = (ROOT / "round43/lattice.tex").read_text(encoding="utf-8")
        for token in (
            r"N_{\rm cal}(m)\ge \rho m-C_{\rm cal}",
            r"U<\infty",
            r"\tau_{\min}",
            r"\cF_{i-1}\longrightarrow s_i\longrightarrow S_i",
            r"\label{lem:prefix-window-count}",
            r"\label{prop:balanced-contrast}",
        ):
            self.assertIn(token, lattice)

    def test_full_ldp_and_strengthened_theorems_are_present(self) -> None:
        combined = "\n".join(
            (ROOT / p).read_text(encoding="utf-8")
            for p in (
                "round43/infinite_jacobi.tex",
                "round43/quantitative_jacobi.tex",
                "round43/effective_inversion_details.tex",
                "round43/linear_time_protocol.tex",
            )
        )
        for label in (
            "eq:jacobi-posterior-ldp",
            "eq:jacobi-denominator-rate",
            "lem:effective-response-jet",
            "lem:finite-grid-certificate",
            "thm:effective-jacobi-stability",
            "lem:response-moment-triangularity",
            "prop:effective-gram-reconstruction",
            "thm:effective-response-jet-audit",
            "thm:growing-depth-recovery",
            "thm:explicit-shrinking-block-rate",
            "cor:weighted-operator-recovery",
            "thm:adaptive-exploration-floor",
            "thm:honest-jacobi-cylinders",
            "lem:l1-impulse-geometry",
            "lem:predictable-intercept-information",
            "thm:linear-time-adaptive-jacobi",
            "thm:linear-time-honest-cylinders",
            "eq:linear-physical-time",
            "eq:linear-elapsed-rate",
            "eq:physical-time-speed",
            "eq:vandermonde-inverse-bound",
            "eq:explicit-kappa-prefactor",
            "eq:explicit-A0",
        ):
            self.assertIn(f"\\label{{{label}}}", combined)

    def test_corrected_washout_derivative_envelope_is_present(self) -> None:
        text = (ROOT / "round43/infinite_jacobi.tex").read_text(encoding="utf-8")
        self.assertIn(r"(1+\log(i+1))^{|\alpha|}", text)
        self.assertIn(r"(i+1)^{-1-\bar\epsilon_w}", text)
        self.assertNotIn(r"C_\alpha(i+1)^{-1-\epsilon_w}", text)

    def test_stale_failure_modes_are_absent(self) -> None:
        article = "\n".join(
            p.read_text(encoding="utf-8")
            for p in [ROOT / "ROUND43_REVISION.tex", *sorted((ROOT / "round43").glob("*.tex"))]
        )
        for token in (chr(12), "w_i=w_*i", "Doob's inequality", "conditional second moment at most"):
            self.assertNotIn(token, article)
        self.assertIn(r"\frac1n\log", article)

    def test_vandermonde_certificates_are_invertible(self) -> None:
        quantitative = (ROOT / "round43/quantitative_jacobi.tex").read_text(encoding="utf-8")
        self.assertIn(r"M_R=2e^{\Lambda_AT}\Lambda_A^R", quantitative)
        self.assertIn(r"C_R\le 2^{R+1}(R+1)!", quantitative)
        self.assertIn(r"K_J\delta^{2R_J+3}", quantitative)
        for order in range(1, 10):
            matrix = [
                [Fraction(k**r, math.factorial(r)) for r in range(order + 1)]
                for k in range(order + 1)
            ]
            det = Fraction(1)
            for col in range(order + 1):
                pivot = next(row for row in range(col, order + 1) if matrix[row][col] != 0)
                if pivot != col:
                    matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
                    det *= -1
                piv = matrix[col][col]
                det *= piv
                for j in range(col, order + 1):
                    matrix[col][j] /= piv
                for row in range(col + 1, order + 1):
                    factor = matrix[row][col]
                    for j in range(col, order + 1):
                        matrix[row][j] -= factor * matrix[col][j]
            self.assertNotEqual(det, 0)

    def test_response_moment_recursion_on_finite_jacobi_matrix(self) -> None:
        size = 8
        c = Fraction(3, 2)
        a = [Fraction(j + 2, j + 3) for j in range(size - 1)]
        b = [Fraction(7 + j, 3) for j in range(size)]
        jacobi = [[Fraction(0) for _ in range(size)] for _ in range(size)]
        for j in range(size):
            jacobi[j][j] = b[j]
            if j + 1 < size:
                jacobi[j][j + 1] = -a[j]
                jacobi[j + 1][j] = -a[j]

        max_m = 5
        vector = [Fraction(1)] + [Fraction(0)] * (size - 1)
        moments: list[Fraction] = []
        for _ in range(max_m + 1):
            moments.append(vector[0])
            vector = matvec(jacobi, vector)

        zero = [Fraction(0)] * size
        q = [zero[:], zero[:], [Fraction(1)] + [Fraction(0)] * (size - 1)]
        for n in range(1, 2 * max_m + 1):
            jq = matvec(jacobi, q[n])
            q.append([-c * q[n + 1][j] - jq[j] for j in range(size)])
        d = [q[r + 2][0] for r in range(2 * max_m + 1)]
        self.assertEqual(-d[1], c)

        recovered = [Fraction(1)]
        for m in range(1, max_m + 1):
            lower = sum(
                (
                    (-1) ** k
                    * math.comb(2 * m - k, 2 * m - 2 * k)
                    * c ** (2 * m - 2 * k)
                    * recovered[k]
                    for k in range(m)
                ),
                Fraction(0),
            )
            recovered.append((-1) ** m * (d[2 * m] - lower))
        self.assertEqual(recovered, moments)

    def test_gram_reconstruction_recovers_jacobi_coefficients(self) -> None:
        size = 8
        depth = 3
        a = [Fraction(j + 3, j + 5) for j in range(size - 1)]
        b = [Fraction(11 + 2 * j, 4) for j in range(size)]
        jacobi = [[Fraction(0) for _ in range(size)] for _ in range(size)]
        for j in range(size):
            jacobi[j][j] = b[j]
            if j + 1 < size:
                jacobi[j][j + 1] = -a[j]
                jacobi[j + 1][j] = -a[j]

        vector = [Fraction(1)] + [Fraction(0)] * (size - 1)
        moments: list[Fraction] = []
        for _ in range(2 * depth + 3):
            moments.append(vector[0])
            vector = matvec(jacobi, vector)

        polys: list[list[Fraction]] = []
        rhos: list[Fraction] = []
        for j in range(depth + 2):
            if j == 0:
                coeffs = [Fraction(1)]
            else:
                gram = [[moments[r + s] for s in range(j)] for r in range(j)]
                rhs = [-moments[j + r] for r in range(j)]
                coeffs = solve_fraction(gram, rhs) + [Fraction(1)]
            polys.append(coeffs)
            rho = sum(
                (
                    coeffs[r] * coeffs[s] * moments[r + s]
                    for r in range(j + 1)
                    for s in range(j + 1)
                ),
                Fraction(0),
            )
            rhos.append(rho)

        for j in range(depth + 1):
            coeffs = polys[j]
            numerator = sum(
                (
                    coeffs[r] * coeffs[s] * moments[r + s + 1]
                    for r in range(j + 1)
                    for s in range(j + 1)
                ),
                Fraction(0),
            )
            self.assertEqual(numerator / rhos[j], b[j])
            self.assertEqual(rhos[j + 1] / rhos[j], a[j] ** 2)

    def test_explicit_shrinking_rate_algebra(self) -> None:
        eta = 0.6
        log_n = 10_000.0
        j = 17.0
        log_delta = -eta * log_n / (80.0 * j)
        self.assertAlmostEqual(20.0 * j * log_delta, -eta * log_n / 4.0)
        self.assertLess(log_delta, 0.0)

    def test_predictable_intercept_subgaussian_inequality(self) -> None:
        for k in range(-80, 81):
            x = k / 10.0
            self.assertLessEqual(math.log(math.cosh(x)), x * x / 2.0 + 1e-12)

    def test_ledger_separates_evidence_from_checks(self) -> None:
        ledger = json.loads((ROOT / "round43/PROOF_LEDGER.json").read_text(encoding="utf-8"))
        self.assertFalse(ledger["formal_proof_assistant"])
        self.assertEqual(ledger["revision"], "v2")
        for obligation in ledger["obligations"].values():
            self.assertTrue(obligation.get("status"))
            self.assertTrue(obligation.get("mathematical_evidence"))
            self.assertTrue(obligation.get("machine_checks"))

    def test_round43_workflow_is_single_and_read_only(self) -> None:
        workflow_dir = ROOT / ".github/workflows"
        retained = sorted(path.name for path in workflow_dir.glob("*.yml"))
        self.assertEqual(retained, ["verify-round43.yml"])
        text = (workflow_dir / "verify-round43.yml").read_text(encoding="utf-8")
        self.assertIn("contents: read", text)
        self.assertNotIn("contents: write", text)
        self.assertNotIn("git push", text)


if __name__ == "__main__":
    unittest.main()
