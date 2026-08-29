#!/usr/bin/env python3
"""Exact finite-dimensional checks for the v5 five-paper series."""

from __future__ import annotations

from decimal import Decimal, getcontext
import json
from pathlib import Path

getcontext().prec = 70
D = Decimal
TOL = D("1e-50")
ROOT = Path(__file__).resolve().parents[1]


def mat_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))]
            for i in range(len(A))]


def mat_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))]
            for i in range(len(A))]


def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))]
            for i in range(len(A))]


def transpose(A):
    return [list(r) for r in zip(*A)]


def scale(c, A):
    return [[c * x for x in row] for row in A]


def eye(n):
    return [[D(1) if i == j else D(0) for j in range(n)] for i in range(n)]


def inv2(A):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / det, -A[0][1] / det],
            [-A[1][0] / det, A[0][0] / det]]


def max_abs(A):
    return max(abs(x) for row in A for x in row)


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    sqrt3 = D(3).sqrt()
    sqrt13 = D(13).sqrt()
    sqrt117 = D(117).sqrt()

    r1max = D(21) / D(20)
    margins = {
        "sep12": D(6) - r1max - D(1),
        "sep13": D(9) - r1max - D(1),
        "sep23": sqrt117 - D(2),
        "eclipse1": D(18) / sqrt13 - r1max - D(1),
        "eclipse2": D(6) - r1max - D(1),
        "eclipse3": D(9) - r1max - D(1),
    }
    require(all(v > 0 for v in margins.values()), "OB3 margins")

    P = [
        [D(0), D(2)/D(3), D(1)/D(3)],
        [D(1)/D(3), D(0), D(2)/D(3)],
        [D(2)/D(3), D(1)/D(3), D(0)],
    ]
    pi = [D(1)/D(3)] * 3
    require(all(abs(sum(r)-1) < TOL for r in P), "P rows")
    require(all(abs(sum(P[i][j] for i in range(3))-1) < TOL
                for j in range(3)), "P cols")

    g = [
        [D(1), D(0)],
        [-D(1)/D(2), sqrt3/D(2)],
        [-D(1)/D(2), -sqrt3/D(2)],
    ]
    mean = [sum(pi[i]*g[i][j] for i in range(3)) for j in range(2)]
    require(max(abs(x) for x in mean) < TOL, "centering")

    C0 = [[sum(pi[i]*g[i][r]*g[i][c] for i in range(3))
           for c in range(2)] for r in range(2)]
    require(max_abs(mat_sub(C0, scale(D(1)/D(2), eye(2)))) < TOL,
            "instant covariance")

    J = [[D(0), -D(1)], [D(1), D(0)]]
    A = mat_add(scale(-D(1)/D(2), eye(2)), scale(sqrt3/D(6), J))
    Pg = mat_mul(P, g)
    Ag = transpose(mat_mul(A, transpose(g)))
    require(max_abs(mat_sub(Pg, Ag)) < TOL, "Pg=Ag")

    H = inv2(mat_sub(eye(2), A))
    h = transpose(mat_mul(H, transpose(g)))
    require(max_abs(mat_sub(mat_mul(mat_sub(eye(3), P), h), g)) < TOL,
            "Poisson equation")

    S = mat_mul(A, H)
    Sigma = mat_add(C0, mat_add(mat_mul(C0, transpose(S)), mat_mul(S, C0)))
    require(max_abs(mat_sub(Sigma, scale(D(1)/D(7), eye(2)))) < TOL,
            "Green-Kubo covariance")

    Gamma = scale(D(1)/D(2),
                  mat_sub(mat_mul(C0, transpose(S)), mat_mul(S, C0)))
    require(max_abs(mat_sub(Gamma, scale(-sqrt3/D(28), J))) < TOL,
            "area anomaly")
    require(max_abs(Gamma) > TOL, "nonzero area")

    overlap = min(
        sum(min(P[i][k], P[j][k]) for k in range(3))
        for i in range(3) for j in range(i+1, 3)
    )
    dobrushin = D(1) - overlap
    require(abs(dobrushin - D(2)/D(3)) < TOL, "Dobrushin coefficient")

    Ph = mat_mul(P, h)
    basis = [
        [[D(1), D(0)], [D(0), D(0)]],
        [[D(0), D(1)], [D(1), D(0)]],
        [[D(0), D(0)], [D(0), D(1)]],
    ]
    cell = []
    for X in basis:
        total = D(0)
        for i in range(3):
            gi = [[g[i][0]], [g[i][1]]]
            phi = [[Ph[i][0]], [Ph[i][1]]]
            total += pi[i] * (
                mat_mul(mat_mul(transpose(gi), X), gi)[0][0] / D(2)
                + mat_mul(mat_mul(transpose(phi), X), gi)[0][0]
            )
        cell.append(total)
    require(abs(cell[0]-D(1)/D(14)) < TOL, "cell X11")
    require(abs(cell[1]) < TOL, "cell X12")
    require(abs(cell[2]-D(1)/D(14)) < TOL, "cell X22")

    samples = [D(-1)/D(40), D(0), D(1)/D(40)]
    max_width = D(0)
    for a in samples:
        w = [D(1)/D(10)+a, D(1)/D(5)+2*a,
             D(3)/D(10)-a, D(2)/D(5)-2*a]
        require(abs(sum(w)-1) < TOL, "FB4 weights sum")
        require(min(w) > 0, "FB4 positivity")
        max_width = max(max_width, max(w))
    require(max_width == D(9)/D(20), "FB4 max width")

    receipt = {
        "status": "PASS_V5_FINITE_DIMENSIONAL_FORMULAS",
        "geometry_margins": {k: str(v) for k, v in margins.items()},
        "Sigma_coll": [["1/7", "0"], ["0", "1/7"]],
        "Gamma_coll_as": [["0", "sqrt(3)/28"],
                          ["-sqrt(3)/28", "0"]],
        "Dobrushin": "2/3",
        "HJB_cell_basis": [str(x) for x in cell],
        "FB4_max_width": "9/20",
        "machine_check_is_peer_review": False,
    }
    out = ROOT / "status" / "FORMULA_RECEIPT.json"
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
