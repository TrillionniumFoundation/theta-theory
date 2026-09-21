#!/usr/bin/env python3
"""Independent finite referee diagnostics for A2 v108.

These checks test representative exact linear-algebra identities only.
They are not theorem certification and do not establish journal-level novelty.
"""
from __future__ import annotations
import itertools
import json
import sympy as s


def sym_matrix(k):
    pairs = [(i, j) for i in range(k) for j in range(i, k)]
    z = s.symbols(f"x0:{len(pairs)}")
    X = s.zeros(k)
    for zz, (i, j) in zip(z, pairs):
        X[i, j] = X[j, i] = zz
    return X, z, pairs


def sampled_conormal_matrix(A, etas):
    A = s.Matrix(A)
    k, _ = A.shape
    X, z, pairs = sym_matrix(k)
    rows = []
    for eta in map(s.Matrix, etas):
        ell = A * eta
        if any(v == 0 for v in ell):
            continue
        Dq = 2 * s.diag(*ell) * A
        basis = Dq.T.nullspace()
        probes = basis + [u + v for u, v in itertools.combinations(basis, 2)]
        for n in probes:
            f = (n.T * X * n)[0]
            rows.append([s.diff(f, zz) for zz in z])
    return s.Matrix(rows), pairs


def B_matrix(A):
    A = s.Matrix(A)
    k = A.rows
    B = s.zeros(k)
    for i in range(k):
        for j in range(i + 1, k):
            B[i, j] = B[j, i] = s.det(
                s.Matrix.hstack(A.row(i).T, A.row(j).T)
            ) ** 2
    return B


def main():
    out = {}

    A4 = s.Matrix([[1, 0], [0, 1], [1, 1], [1, 2]])
    M4, pairs4 = sampled_conormal_matrix(A4, [[1, j] for j in [3, 4, 5, 6, 7]])
    B4 = B_matrix(A4)
    b4 = s.Matrix([B4[i, j] for i, j in pairs4])
    out["d2_k4"] = {
        "symmetric_dimension": len(pairs4),
        "sampled_rank": int(M4.rank()),
        "nullity": len(pairs4) - int(M4.rank()),
        "B_in_kernel": bool(M4 * b4 == s.zeros(M4.rows, 1)),
    }

    A6 = s.Matrix([
        [1, 0, 0], [0, 1, 0], [0, 0, 1],
        [1, 1, 0], [1, 0, 1], [0, 1, 1],
    ])
    etas6 = [[1, i, j] for i in [2, 3, 4] for j in [5, 6, 7]]
    M6, pairs6 = sampled_conormal_matrix(A6, etas6)
    out["d3_k6"] = {
        "symmetric_dimension": len(pairs6),
        "sampled_rank": int(M6.rank()),
        "nullity": len(pairs6) - int(M6.rank()),
    }

    k = 4
    X, z, pairs = sym_matrix(k)
    r = [s.Integer(i) for i in range(1, k + 1)]
    d = [s.Integer(v) for v in [2, 3, 5, 7]]
    rows = []
    for i, j, l in itertools.combinations(range(k), 3):
        f = (
            (r[j] - r[i]) * X[i, j] / (d[i] * d[j])
            - (r[l] - r[i]) * X[i, l] / (d[i] * d[l])
            + (r[l] - r[j]) * X[j, l] / (d[j] * d[l])
        )
        rows.append([s.diff(f, zz) for zz in z])
    C = s.Matrix(rows)
    out["three_site_k4"] = {
        "constraint_rank": int(C.rank()),
        "native_span_dimension": len(pairs) - int(C.rank()),
        "expected_native_span_dimension": 2 * k - 1,
    }

    out["scope"] = "finite exact referee spot checks only; not theorem certification"
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
