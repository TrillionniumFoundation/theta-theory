from __future__ import annotations

import hashlib
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    a = [row[:] for row in matrix]
    n = len(a)
    sign = 1
    det = Fraction(1)
    for col in range(n):
        pivot = next((row for row in range(col, n) if a[row][col]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign *= -1
        pivot_value = a[col][col]
        det *= pivot_value
        for row in range(col + 1, n):
            factor = a[row][col] / pivot_value
            for k in range(col + 1, n):
                a[row][k] -= factor * a[col][k]
    return det * sign


def solve(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    n = len(matrix)
    a = [matrix[i][:] + [rhs[i]] for i in range(n)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if a[row][col]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [entry / scale for entry in a[col]]
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            if factor:
                a[row] = [a[row][k] - factor * a[col][k] for k in range(n + 1)]
    return [a[i][-1] for i in range(n)]


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum((row[j] * vector[j] for j in range(len(vector))), Fraction(0)) for row in matrix]


def jet_coordinates(
    c: Fraction,
    k: Fraction,
    epsilon: Fraction,
    c_b: Fraction,
    k_b: Fraction,
) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction]:
    s = k + epsilon
    r2 = -c
    r3 = c**2 - s
    r5 = c**4 - 3 * c**2 * s + s**2 + epsilon**2
    r6 = -c**5 + 4 * c**3 * s - 2 * c * epsilon**2 - 3 * c * s**2 - c_b * epsilon**2
    r7 = (
        c**6
        - 5 * c**4 * s
        + 3 * c**2 * epsilon**2
        + 6 * c**2 * s**2
        + 2 * c * c_b * epsilon**2
        + c_b**2 * epsilon**2
        - 2 * epsilon**3
        - 2 * epsilon**2 * s
        - s**3
        - epsilon**2 * k_b
    )
    return r2, r3, r5, r6, r7


def invert_jet_coordinates(
    values: tuple[Fraction, Fraction, Fraction, Fraction, Fraction]
) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction]:
    r2, r3, r5, r6, r7 = values
    c = -r2
    s = c**2 - r3
    epsilon_squared = r5 - c**4 + 3 * c**2 * s - s**2
    num_root = math.isqrt(epsilon_squared.numerator)
    den_root = math.isqrt(epsilon_squared.denominator)
    if num_root**2 != epsilon_squared.numerator or den_root**2 != epsilon_squared.denominator:
        raise AssertionError("test point does not have a rational positive square root")
    epsilon = Fraction(num_root, den_root)
    k = s - epsilon
    c_b = (-c**5 + 4 * c**3 * s - 2 * c * epsilon**2 - 3 * c * s**2 - r6) / epsilon**2
    k_b = (
        c**6
        - 5 * c**4 * s
        + 3 * c**2 * epsilon**2
        + 6 * c**2 * s**2
        + 2 * c * c_b * epsilon**2
        + c_b**2 * epsilon**2
        - 2 * epsilon**3
        - 2 * epsilon**2 * s
        - s**3
        - r7
    ) / epsilon**2
    return c, k, epsilon, c_b, k_b


class Round41ExactChecks(unittest.TestCase):
    def test_triangular_jet_inverse_exactly_recovers_five_parameters(self) -> None:
        parameter = tuple(map(Fraction, (2, 3, 4, 5, 6)))
        self.assertEqual(invert_jet_coordinates(jet_coordinates(*parameter)), parameter)

    def test_finite_banded_generator_reproduces_eight_jets(self) -> None:
        c, k, epsilon, c_b, k_b = tuple(map(Fraction, (2, 3, 4, 5, 6)))
        n_sites = 8
        size = 2 * n_sites
        stiffness = [[Fraction(0) for _ in range(n_sites)] for _ in range(n_sites)]
        damping = [[Fraction(0) for _ in range(n_sites)] for _ in range(n_sites)]
        stiffness[0][0] = k + epsilon
        stiffness[0][1] = stiffness[1][0] = -epsilon
        damping[0][0] = c
        for j in range(1, n_sites):
            stiffness[j][j] = k_b + 2 * epsilon
            damping[j][j] = c_b
            if j + 1 < n_sites:
                stiffness[j][j + 1] = stiffness[j + 1][j] = -epsilon
        generator = [[Fraction(0) for _ in range(size)] for _ in range(size)]
        for j in range(n_sites):
            generator[j][n_sites + j] = Fraction(1)
            for ell in range(n_sites):
                generator[n_sites + j][ell] = -stiffness[j][ell]
                generator[n_sites + j][n_sites + ell] = -damping[j][ell]
        vector = [Fraction(0) for _ in range(size)]
        vector[n_sites] = Fraction(1)
        direct = []
        for _ in range(8):
            direct.append(vector[0])
            vector = matvec(generator, vector)
        r2, r3, r5, r6, r7 = jet_coordinates(c, k, epsilon, c_b, k_b)
        s = k + epsilon
        expected = [
            Fraction(0),
            Fraction(1),
            r2,
            r3,
            c * (-c**2 + 2 * s),
            r5,
            r6,
            r7,
        ]
        self.assertEqual(direct, expected)

    def test_six_duration_generalized_vandermonde_is_nonsingular(self) -> None:
        matrix = [
            [Fraction(j ** (ell + 1), math.factorial(ell + 1)) for ell in range(2, 8)]
            for j in range(1, 7)
        ]
        self.assertNotEqual(determinant(matrix), 0)

    def test_finite_jacobi_schur_recursion_matches_direct_inverse(self) -> None:
        w = Fraction(5)
        diagonals = list(map(Fraction, (7, 8, 9)))
        off_diagonals = list(map(Fraction, (2, 3)))
        matrix = [[Fraction(0) for _ in range(3)] for _ in range(3)]
        for j in range(3):
            matrix[j][j] = w + diagonals[j]
        for j in range(2):
            matrix[j][j + 1] = matrix[j + 1][j] = -off_diagonals[j]
        m0 = solve(matrix, [Fraction(1), Fraction(0), Fraction(0)])[0]
        tail = [row[1:] for row in matrix[1:]]
        m1 = solve(tail, [Fraction(1), Fraction(0)])[0]
        self.assertEqual(m0, 1 / (w + diagonals[0] - off_diagonals[0] ** 2 * m1))

    def test_principal_theorem_labels_are_present(self) -> None:
        expectations = {
            "round41/triangular.tex": ["thm:abstract-bvm", "lem:random-laplace"],
            "round41/lattice.tex": ["thm:jet-embedding", "prop:balanced-contrast", "thm:lattice-bvm"],
            "round41/filter_memory.tex": ["thm:filter-jets", "cor:memory-posterior"],
            "round41/infinite_jacobi.tex": ["thm:jacobi-reconstruction", "thm:jacobi-consistency"],
            "round41/preparations.tex": ["thm:preparation-mixture"],
        }
        for relative_path, labels in expectations.items():
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            for label in labels:
                self.assertIn(f"\\label{{{label}}}", text)

    def test_source_manifest_hashes_and_sizes(self) -> None:
        manifest = json.loads((ROOT / "round41/SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        for entry in manifest["files"]:
            data = (ROOT / entry["path"]).read_bytes()
            self.assertEqual(len(data), entry["bytes"], entry["path"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])


    def test_round40_uniformity_invariants_are_landed(self) -> None:
        lattice = (ROOT / "round41/lattice.tex").read_text(encoding="utf-8")
        for token in (
            r"N_{\rm cal}(m)\ge \rho m-C_{\rm cal}",
            r"\tau_{\min}",
            r"U<\infty",
            r"\cF_{i-1}\longrightarrow s_i\longrightarrow S_i",
            r"\label{lem:prefix-window-count}",
            r"\underline\tau=\min(\tau,\tau_{\min})",
        ):
            self.assertIn(token, lattice)

    def test_uncountable_class_gap_is_replaced_by_supnorm_net(self) -> None:
        appendix = (ROOT / "round41/appendix_uniformity.tex").read_text(encoding="utf-8")
        self.assertIn(r"\label{lem:supnorm-response-slln}", appendix)
        self.assertIn(r"\frac1n\sum_{i=1}^n\abs{\xi_i}", appendix)
        self.assertIn(r"\abs{f(t)^2-f^k(t)^2}\le2B\varepsilon", appendix)
        self.assertNotIn("conditional second moment at most", appendix)
        self.assertNotIn("Doob's inequality", appendix)

    def test_filter_range_is_fixed_and_separable(self) -> None:
        text = (ROOT / "round41/filter_memory.tex").read_text(encoding="utf-8")
        self.assertIn(r"\mathbb E_j^0", text)
        self.assertIn("deterministic separable Banach subspace", text)
        self.assertIn(r"K^{r+1}M_r\varepsilon", text)

    def test_quantitative_jacobi_rate_is_present(self) -> None:
        text = (ROOT / "round41/infinite_jacobi.tex").read_text(encoding="utf-8")
        for label in (
            "prop:jacobi-response-geometry",
            "thm:jacobi-rate",
            "eq:jacobi-closed-set-rate",
            "eq:jacobi-cylinder-rate",
        ):
            self.assertIn(f"\\label{{{label}}}", text)
        self.assertIn(r"2a_+<b_-<b_+<\infty", text)
        self.assertIn(r"U_J<\infty", text)

    def test_article_excludes_repository_governance(self) -> None:
        article_paths = [
            ROOT / "ROUND41_REVISION.tex",
            *sorted((ROOT / "round41").glob("*.tex")),
        ]
        forbidden = ("GitHub Actions", "SHA--256", "Round 40 report", "source manifest")
        combined = "\n".join(path.read_text(encoding="utf-8") for path in article_paths)
        for token in forbidden:
            self.assertNotIn(token, combined)


    def test_full_jacobi_posterior_ldp_and_uniform_inverse_moduli(self) -> None:
        text = (ROOT / "round41/infinite_jacobi.tex").read_text(encoding="utf-8")
        for label in (
            "eq:jacobi-posterior-ldp",
            "eq:jacobi-rate-function",
            "eq:jacobi-separation-modulus",
            "eq:jacobi-inverse-modulus",
            "eq:jacobi-denominator-rate",
        ):
            self.assertIn(f"\\label{{{label}}}", text)
        self.assertIn("Full posterior large-deviation principle", text)
        self.assertIn(r"\beta,\gamma\in\mathfrak B", text)
        self.assertIn(r"\Omega_J(r)\downarrow0", text)


if __name__ == "__main__":
    unittest.main()
