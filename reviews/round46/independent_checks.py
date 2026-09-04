#!/usr/bin/env python3
"""Independent exact-arithmetic checks for the Round 46 referee report.

Python standard library only. No network access, source mutation, or author-test
imports. These finite checks are not a proof assistant or a statistical proof.
The all-depth arguments are written out in the accompanying referee report.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import comb, factorial
from pathlib import Path
import argparse
import json

FROZEN_HEAD = "00fee70834ee5e2a1fadc55c5d118a23a4637477"
SOURCE_COMMIT = "c67f80f34fc128ba3eaece0fd8ad4ea262aa9cd1"


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def inverse(a):
    n = len(a)
    if not n or any(len(row) != n for row in a):
        raise ValueError("A nonempty square matrix is required")
    aug = [[F(x) for x in row] + [F(i == j) for j in range(n)]
           for i, row in enumerate(a)]
    for k in range(n):
        pivot = next((i for i in range(k, n) if aug[i][k]), None)
        if pivot is None:
            raise ValueError("Singular matrix")
        aug[k], aug[pivot] = aug[pivot], aug[k]
        scale = aug[k][k]
        aug[k] = [x / scale for x in aug[k]]
        for i in range(n):
            if i != k:
                scale = aug[i][k]
                aug[i] = [x - scale * y for x, y in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


def j_apply(x, a, b):
    return [b[k] * x[k] - (a[k - 1] * x[k - 1] if k else 0)
            - (a[k] * x[k + 1] if k + 1 < len(x) else 0)
            for k in range(len(x))]


def a_apply(x, c, a, b):
    q, v = x
    jq = j_apply(q, a, b)
    return v[:], [-x - c * y for x, y in zip(jq, v)]


def profile(n, offset):
    # One common admissible box: c in [1/2, 2], a in [1/4, 1/2],
    # b in [2, 3]. In particular b_- > 2 a_+.
    a = [F(1, 4) + F((7 * k + offset) % 11, 100) for k in range(n - 1)]
    b = [F(2) + F((3 * k + offset) % 13, 20) for k in range(n)]
    return a, b


def direct_moments(a, b, order):
    x = [F(1)] + [F(0)] * (len(b) - 1)
    out = []
    for _ in range(order + 1):
        out.append(x[0])
        x = j_apply(x, a, b)
    return out


def direct_jets(c, a, b, order):
    # v_r = ell A^(r+1) B, evaluated by block-vector multiplication.
    x = ([F(0)] * len(b), [F(1)] + [F(0)] * (len(b) - 1))
    out = []
    for _ in range(order + 1):
        x = a_apply(x, c, a, b)
        out.append(x[0][0])
    return out


def closed_moments(c, v, order):
    return [(-1) ** m * sum(F(comb(m, k)) * c ** (m - k) * v[m + k]
                            for k in range(m + 1))
            for m in range(order + 1)]


def polynomial(mu, k):
    if k == 0:
        return [F(1)]
    hi = inverse([[mu[r + s] for s in range(k)] for r in range(k)])
    return [-sum(hi[r][s] * mu[k + s] for s in range(k))
            for r in range(k)] + [F(1)]


def quadratic(p, mu, shift=0):
    return sum(p[r] * p[s] * mu[r + s + shift]
               for r in range(len(p)) for s in range(len(p)))


def shifted_coefficients(coefficients):
    """Exact monomial coefficients of P(z+1), low degree first."""
    return [sum(coefficients[j] * comb(j, k)
                for j in range(k, len(coefficients)))
            for k in range(len(coefficients))]


def run_checks():
    records = []
    cases = 0
    for offset in range(4):
        a, b = profile(16, offset)
        for c in (F(1, 2), F(7, 8), F(3, 2)):
            q = [F((k % 3) - 1, k + 1) for k in range(16)]
            v = [F((k % 5) - 2, k + 2) for k in range(16)]
            ax = a_apply((q, v), c, a, b)
            aax = a_apply(ax, c, a, b)
            lhs = [[u + c * w for u, w in zip(part, apart)]
                   for part, apart in zip(aax, ax)]
            assert lhs == [[-x for x in j_apply(part, a, b)] for part in (q, v)]
            jets = direct_jets(c, a, b, 24)
            assert -jets[1] == c
            assert closed_moments(c, jets, 12) == direct_moments(a, b, 12)
            cases += 1
    records.append({"name": "block identity and closed response-to-moment formula",
                    "status": "passed", "rational_profiles_and_dampings": cases,
                    "moment_orders": [0, 12], "jet_orders_v": [0, 24]})

    cases = 0
    for offset in range(4):
        a, b = profile(16, offset)
        mu = direct_moments(a, b, 16)
        for dim in range(1, 8):
            h = [[mu[r + s] for s in range(dim)] for r in range(dim)]
            decomposition = [[F(0)] * dim for _ in range(dim)]
            for k in range(dim):
                p = polynomial(mu, k)
                rho = quadratic(p, mu)
                prod = F(1)
                for ak in a[:k]:
                    prod *= ak * ak
                assert rho == prod
                padded = p + [F(0)] * (dim - len(p))
                for r in range(dim):
                    for s in range(dim):
                        decomposition[r][s] += padded[r] * padded[s] / rho
                assert quadratic(p, mu, 1) / rho == b[k]
                pn = polynomial(mu, k + 1)
                assert quadratic(pn, mu) / rho == a[k] * a[k]
            assert decomposition == inverse(h)
            cases += 1
    records.append({"name": "orthogonal-polynomial Hankel inverse and coefficient reconstruction",
                    "status": "passed", "cases": cases, "matrix_dimensions": [1, 7]})

    norms = []
    for r in range(1, 17):
        vi = inverse([[F(k ** s, factorial(s)) for s in range(r + 1)]
                      for k in range(r + 1)])
        norm = max(sum(abs(x) for x in row) for row in vi)
        assert norm <= 2 ** r * comb(2 * r, r) <= 8 ** r
        norms.append({"R": r, "exact_C_R": str(norm)})
    records.append({"name": "sharper Vandermonde row-sum bound", "status": "passed",
                    "orders": [1, 16], "norms": norms})

    certificates = {
        "current_round45_jet_composition": [-4, -16, 31],
        "new_V_exponent": [-1, 1],
        "new_R_exponent": [-1, 1],
        "new_T_exponent": [-2, 2],
        "new_b_ratio_exponent": [-1, 1],
        "new_a_ratio_exponent": [1],
        "new_separation_prefactor": [0, -121, 312],
    }
    shifted = {name: shifted_coefficients(p) for name, p in certificates.items()}
    assert all(all(x >= 0 for x in p) for p in shifted.values())
    old_failures = [j for j in range(20)
                    if 4 * (2 * j + 3) ** 2 + 8 * (j + 1) ** 3 > 12 * (j + 1) ** 3]
    assert old_failures == [0, 1, 2, 3]
    records.append({"name": "all-depth polynomial comparison certificates",
                    "status": "passed", "coefficients_after_j_equals_z_plus_1": shifted,
                    "old_round43_counterexample_depths_not_present_in_round45": old_failures})

    assert -F(13, 32) + F(3, 32) + F(1, 16) == -F(1, 4)
    for n in (1, 2, 10, 100, 1000):
        assert sum(F(1, m * (m + 1)) for m in range(1, n + 1)) == 1 - F(1, n + 1)
    records.append({"name": "current posterior exponent and confidence error allocation",
                    "status": "passed"})
    return {"reviewed_head": FROZEN_HEAD, "reviewed_source_commit": SOURCE_COMMIT,
            "all_independent_checks_passed": True, "groups": records,
            "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "limitations": ["Finite exact checks are not proof-assistant certification.",
                "All-depth analytic derivations are in the referee report.",
                "No author test suite or LaTeX build was rerun by this script.",
                "No adaptive sampling simulation or coverage experiment is performed."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a JSON result to this path")
    args = parser.parse_args()
    text = json.dumps(run_checks(), indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
