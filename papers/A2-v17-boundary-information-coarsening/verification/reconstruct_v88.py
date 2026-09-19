"""Floating-point implementation of Theorem 4.1 (A2 v88).

The theorem is exact-arithmetic. This implementation reports degeneracy
instead of silently treating a numerically deficient problem as regular.
Its thresholds are numerical safeguards, not latent signal assumptions.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Reconstruction:
    roots: np.ndarray
    denominator: np.ndarray | None
    normalization_singular_values: np.ndarray
    status: str


def normalization_system(observations: np.ndarray, clocks: np.ndarray,
                         degree: int) -> tuple[np.ndarray, np.ndarray]:
    """Return the observed linear normalization system in ascending powers."""
    p = np.asarray(observations, dtype=float)
    t = np.asarray(clocks, dtype=float)
    w = np.vander(t, degree + 1, increasing=True)
    # Using an orthonormal residual basis avoids forming a nearly cancelling
    # projector when there are exactly degree+1 interpolation nodes.
    q, _ = np.linalg.qr(w, mode="complete")
    residual = q[:, degree + 1:].T
    flat = p.reshape(len(t), -1)
    columns = [(residual @ (t[:, None] ** r * flat)).ravel()
               for r in range(degree)]
    matrix = np.column_stack(columns)
    rhs = -(residual @ (t[:, None] ** degree * flat)).ravel()
    return matrix, rhs


def reconstruct(observations: np.ndarray, clocks: np.ndarray, degree: int,
                capacity: int, interval: tuple[float, float]) -> Reconstruction:
    """Recover the aggregate root multiset, with bounded-range fallback.

    Inputs have shapes (number_of_clocks, m1, m2) and (number_of_clocks,).
    Roots are returned in increasing order. This does not recover a partition
    into latent components and does not compute a residual confidence set.
    """
    p = np.asarray(observations, dtype=float)
    t = np.asarray(clocks, dtype=float)
    lo, hi = map(float, interval)
    if (p.ndim != 3 or t.ndim != 1 or p.shape[0] != len(t)
            or degree < 1 or len(t) < degree + 1
            or not 2 <= capacity <= min(p.shape[1:])
            or not lo < hi or not np.all(np.diff(t) > 0)
            or not np.all(t > hi)
            or not np.all(np.isfinite(p)) or not np.all(np.isfinite(t))):
        raise ValueError("Invalid observation shape, dimension, clocks, or interval")
    fallback = np.full(capacity * degree, lo)
    nmat, rhs = normalization_system(p, t, degree)
    if not nmat.shape[0]:
        return Reconstruction(fallback, None, np.zeros(degree), "normalization-deficient")
    a, _, nrank, svals = np.linalg.lstsq(nmat, rhs, rcond=None)
    if nrank != degree:
        return Reconstruction(fallback, None, svals, "normalization-deficient")
    if degree == 1:
        a[0] = -np.clip(-a[0], lo, hi)
    qcoef = np.r_[a, 1.0]
    qvals = np.polynomial.polynomial.polyval(t, qcoef)
    if np.any(qvals <= 0):
        return Reconstruction(fallback, qcoef, svals, "nonpositive-normalization")
    left, sv, right_t = np.linalg.svd(p[0], full_matrices=False)
    tol = np.finfo(float).eps * max(p.shape[1:]) * sv[0]
    if sv[capacity-1] <= tol:
        return Reconstruction(fallback, qcoef, svals, "observed-rank-deficient")
    left, right = left[:, :capacity], right_t[:capacity].T
    vand = np.vander(t[:degree+1], degree+1, increasing=True)
    values = (qvals[:degree+1, None, None] * p[:degree+1]).reshape(degree+1, -1)
    coeff = np.linalg.solve(vand, values).reshape(degree+1, *p.shape[1:])
    reduced = np.array([left.T @ c @ right for c in coeff])
    if np.linalg.matrix_rank(reduced[-1]) < capacity:
        return Reconstruction(fallback, qcoef, svals, "leading-coefficient-deficient")
    try:
        blocks = [np.linalg.solve(reduced[-1], c) for c in reduced[:-1]]
        companion = np.zeros((degree*capacity, degree*capacity))
        if degree > 1:
            companion[:-capacity, capacity:] = np.eye((degree-1)*capacity)
        companion[-capacity:] = -np.hstack(blocks)
        eigenvalues = np.linalg.eigvals(companion)
    except np.linalg.LinAlgError:
        return Reconstruction(fallback, qcoef, svals, "linear-algebra-failure")
    if not np.all(np.isfinite(eigenvalues)):
        return Reconstruction(fallback, qcoef, svals, "nonfinite-root")
    roots = np.sort(np.clip(eigenvalues.real, lo, hi))
    return Reconstruction(roots, qcoef, svals, "reconstructed")
