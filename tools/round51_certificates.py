"""Exact rational certificates for the Round 51 mathematical submission.

Standard library only. No floating point value is accepted as certified input.
Finite tests of this module are not a formal proof of the infinite-dimensional
results. The outer construction is exhaustive, not an efficient large-depth solver.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, prod
from typing import Sequence


class ResourceLimit(RuntimeError):
    """The full requested computation exceeds its declared resource cap."""


class RepresentationError(ValueError):
    """A represented band is not contained in its declared rounding budget."""


def rat(x: int | str | F) -> F:
    if isinstance(x, bool) or not isinstance(x, (int, str, F)):
        raise TypeError("Use an integer, a rational string, or Fraction; not float")
    return F(x)


def ceilq(x: F) -> int:
    return -((-x.numerator) // x.denominator)


def natural(x: int, name: str, minimum: int = 0) -> int:
    if isinstance(x, bool) or not isinstance(x, int) or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return x


@dataclass(frozen=True)
class ModelBox:
    c: tuple[F, F]
    a: tuple[F, F]
    b: tuple[F, F]
    T: F

    def __post_init__(self) -> None:
        for name in ("c", "a", "b"):
            pair = tuple(rat(v) for v in getattr(self, name))
            if len(pair) != 2 or not 0 < pair[0] < pair[1]:
                raise ValueError(f"Invalid positive interval {name}")
            object.__setattr__(self, name, pair)
        object.__setattr__(self, "T", rat(self.T))
        if self.T <= 0 or self.b[0] <= 2 * self.a[1]:
            raise ValueError("Require T>0 and strict pinning b_- > 2 a_+")

    @property
    def Lambda(self) -> F:
        return 1 + self.c[1] + max(F(1), self.b[1] + 2 * self.a[1])

    @property
    def Q(self) -> F:
        return 8 * max(F(2), self.Lambda, self.T, 1 / self.T, 1 / self.a[0])


def series_mul(a: Sequence[F], b: Sequence[F], degree: int) -> list[F]:
    natural(degree, "degree")
    out = [F(0)] * (degree + 1)
    for i, x in enumerate(a[:degree + 1]):
        for j, y in enumerate(b[:degree + 1 - i]):
            out[i + j] += x * y
    return out


def series_div(a: Sequence[F], b: Sequence[F], degree: int) -> list[F]:
    if not b or b[0] == 0:
        raise ValueError("Nonzero constant denominator required")
    out = [F(0)] * (degree + 1)
    for k in range(degree + 1):
        out[k] = ((a[k] if k < len(a) else 0)
                  - sum(b[j] * out[k-j] for j in range(1, min(k, len(b)-1)+1))) / b[0]
    return out


def log_sqrt_series(degree: int) -> tuple[list[F], list[F]]:
    natural(degree, "degree")
    lg = [F(0)] + [F((-1)**(k+1), k) for k in range(1, degree+1)]
    sq = [F(1)]
    for k in range(1, degree+1):
        sq.append(sq[-1] * (F(1, 2) - (k-1)) / k)
    return lg, sq


def sampled_coefficients(Delta: F, R: int, N: int) -> tuple[list[list[F]], list[list[F]]]:
    Delta = rat(Delta)
    natural(R, "R", 1)
    natural(N, "N", R)
    if not 0 < Delta <= 1:
        raise ValueError("Require 0 < Delta <= 1")
    lg, sq = log_sqrt_series(N+1)
    sqrtplus = sq[:N+1]
    sqrtplus[0] += 1
    power = [F(1)] + [F(0)] * (N+1)
    cs, rows = [], []
    for r in range(1, R+1):
        power = series_mul(power, lg, N+1)
        c = [z / Delta**r for z in series_mul(power[1:], sqrtplus, N)]
        row = [sum(c[k] * (-1)**(k-l) * comb(k, l) for k in range(l, N+1))
               for l in range(N+1)]
        cs.append(c)
        rows.append(row)
    return cs, rows


def success_probability(rho: F, w: F) -> F:
    rho, w = rat(rho), rat(w)
    if not 0 < rho <= 1 or not 0 < w <= 1:
        raise ValueError("rho and atom mass must lie in (0,1]")
    return 1 - rho + rho*w


def certificate(box: ModelBox, J: int, delta: F, t0: F, rho: F, w: F,
                *, weighted: bool = False, max_order: int = 4096) -> dict:
    natural(J, "J")
    natural(max_order, "max_order", 1)
    R, j = 4*J+8, J+1
    if R > max_order:
        raise ResourceLimit("Jet order exceeds max_order before power allocation")
    delta, t0 = rat(delta), rat(t0)
    if not 0 < delta <= 1 or not 0 < t0 <= box.T:
        raise ValueError("Require 0<delta<=1 and 0<t0<=T")
    Delta = 2*t0
    if Delta * box.Lambda > F(1, 64):
        raise ValueError("The declared clock fails Delta*Lambda <= 1/64")
    p = success_probability(rho, w)
    L, N = box.Q**(25*j), R
    while L * Delta**(-R) * F(16)**(-N) > delta/2:
        N += 1
        if N > max_order:
            raise ResourceLimit("Remainder target exceeds max_order")
    A, E = 8 * Delta**(-R) * 4**N, Delta**(-R) * F(16)**(-N)
    kap = p**(N+1) * delta**2 / (4*L**2*A**2)
    out = dict(J=J, R=R, N=N, m=N+1, Delta=Delta, p=p,
               L=L, A=A, E=E, kappa=kap)
    if weighted:
        _, rows = sampled_coefficients(Delta, R, N)
        W = max(sum(z*z/F(N+1-l) for l, z in enumerate(row)) for row in rows)
        if not 0 < W <= A*A:
            raise ArithmeticError("Weighted transform budget invariant failed")
        out.update(W=W, kappa_weighted=p**(N+1)*delta**2/(4*L**2*W))
    return out


def apply_generator(vector: Sequence[F], c: F, diagonal: Sequence[F],
                    edges: Sequence[F]) -> list[F]:
    n = len(diagonal)
    if n < 1 or len(edges) != n-1 or len(vector) != 2*n:
        raise ValueError("Generator dimensions do not match")
    q, v = vector[:n], vector[n:]
    acc = [-diagonal[i]*q[i]-c*v[i]
           + (edges[i-1]*q[i-1] if i else 0)
           + (edges[i]*q[i+1] if i+1 < n else 0) for i in range(n)]
    return list(v) + acc


def boundary_jets(c: F, diagonal: Sequence[F], edges: Sequence[F], order: int) -> list[F]:
    natural(order, "order")
    n = len(diagonal)
    v = [F(0)]*(2*n)
    v[n] = F(1)
    out = [F(0)]
    for _ in range(order):
        out.append(v[0])
        v = apply_generator(v, c, diagonal, edges)
    return out


def jacobi_moments(diagonal: Sequence[F], edges: Sequence[F], order: int) -> list[F]:
    natural(order, "order")
    n = len(diagonal)
    if n < 1 or len(edges) != n-1:
        raise ValueError("Jacobi dimensions do not match")
    v, out = [F(1)] + [F(0)]*(n-1), []
    for _ in range(order+1):
        out.append(v[0])
        v = [diagonal[i]*v[i] - (edges[i-1]*v[i-1] if i else 0)
             - (edges[i]*v[i+1] if i+1 < n else 0) for i in range(n)]
    return out


def moments_from_jets(jets: Sequence[F], order: int) -> list[F]:
    natural(order, "order", 1)
    if len(jets) < 2*order+3:
        raise ValueError("Insufficient jet orders")
    c = -jets[3]
    return [(-1)**m * sum(F(comb(m,k))*c**(m-k)*jets[m+k+2]
                         for k in range(m+1)) for m in range(order+1)]


def solve(A: Sequence[Sequence[F]], b: Sequence[F]) -> list[F]:
    n = len(b)
    if len(A) != n or any(len(row) != n for row in A):
        raise ValueError("Square system required")
    aug = [list(map(rat, row)) + [rat(b[i])] for i, row in enumerate(A)]
    for k in range(n):
        pivot = next((i for i in range(k,n) if aug[i][k]), None)
        if pivot is None:
            raise ValueError("Singular moment system")
        aug[k], aug[pivot] = aug[pivot], aug[k]
        z = aug[k][k]
        aug[k] = [x/z for x in aug[k]]
        for i in range(n):
            if i != k:
                z = aug[i][k]
                aug[i] = [x-z*y for x,y in zip(aug[i],aug[k])]
    return [row[-1] for row in aug]


def recover_jacobi(mu: Sequence[F], J: int) -> tuple[list[F], list[F]]:
    natural(J, "J")
    if len(mu) < 2*J+3 or mu[0] != 1:
        raise ValueError("Need normalized moments through 2J+2")
    polys, norms = [[F(1)]], [F(1)]
    for k in range(1,J+2):
        p = solve([[mu[i+j] for j in range(k)] for i in range(k)],
                  [-mu[i+k] for i in range(k)]) + [F(1)]
        rho = sum(p[i]*p[j]*mu[i+j] for i in range(k+1) for j in range(k+1))
        if rho <= 0:
            raise ValueError("Positive Gram norms required")
        polys.append(p)
        norms.append(rho)
    diag = [sum(p[i]*p[j]*mu[i+j+1] for i in range(len(p)) for j in range(len(p)))/norms[k]
            for k,p in enumerate(polys[:-1])]
    return diag, [norms[k+1]/norms[k] for k in range(J+1)]


def step_taylor(c: F, diagonal: Sequence[F], edges: Sequence[F], t: F, P: int) -> F:
    t = rat(t)
    natural(P, "P")
    if t < 0:
        raise ValueError("Time must be nonnegative")
    jets = boundary_jets(c, diagonal, edges, P+1)
    return sum(jets[k+1]*t**(k+1)/factorial(k+1) for k in range(P+1))


def validate_band(reference: Sequence[F], represented: Sequence[F], epsilon: F) -> tuple:
    if len(reference) != 2 or len(represented) != 2:
        raise RepresentationError("Intervals need exactly two endpoints")
    lo, hi = map(rat, reference)
    a, b = map(rat, represented)
    epsilon = rat(epsilon)
    if not (lo <= hi and a <= b and epsilon >= 0 and
            lo-epsilon <= a <= lo <= hi <= b <= hi+epsilon):
        raise RepresentationError("Enclosure or representation budget violated")
    return (lo, hi), (a, b), epsilon


def outer_errors(box: ModelBox, T: F, K: int, r: F, P: int) -> dict:
    T, r = rat(T), rat(r)
    natural(K, "K", 1)
    natural(P, "P")
    if T <= 0 or r <= 0:
        raise ValueError("Positive time cap and mesh radius required")
    x = box.Lambda*T
    E0 = F(3)**ceilq(x)
    return dict(tail=2*T*E0*x**K/factorial(K), mesh=2*r*T*T*E0,
                taylor=T*E0*x**(P+1)/factorial(P+1))


def outer_boxes(box: ModelBox, J: int, K: int, r: F, P: int,
                observables: Sequence[Sequence[tuple[F,F]]],
                bands: Sequence[tuple[Sequence[F],Sequence[F],F]],
                *, max_boxes: int = 100000) -> dict:
    natural(J, "J")
    natural(K, "K", J+1)
    natural(P, "P")
    natural(max_boxes, "max_boxes", 1)
    r = rat(r)
    if r <= 0 or not observables or len(observables) != len(bands):
        raise ValueError("Positive radius and matching nonempty data required")
    terms = [[(rat(c),rat(t)) for c,t in row] for row in observables]
    if any(not row for row in terms) or any(t < 0 for row in terms for _,t in row):
        raise ValueError("Nonempty observables with nonnegative times required")
    checked = [validate_band(*b) for b in bands]
    T = max(t for row in terms for _,t in row)
    errors = outer_errors(box,T,K,r,P)
    Eq = [sum(abs(c) for c,_ in row)*sum(errors.values()) for row in terms]
    domains = [box.c] + [box.b]*(K+1) + [box.a]*K
    counts = [max(1,ceilq((hi-lo)/(2*r))) for lo,hi in domains]
    total = prod(counts)
    if total > max_boxes:
        raise ResourceLimit(f"Need {total} boxes, cap is {max_boxes}; none enumerated")
    axes = [[(lo+(hi-lo)*i/n, lo+(hi-lo)*(i+1)/n) for i in range(n)]
            for (lo,hi),n in zip(domains,counts)]
    retained, visited = [], 0
    for full in product(*axes):
        visited += 1
        centers = [(lo+hi)/2 for lo,hi in full]
        c, diag, edges = centers[0], centers[1:K+2], centers[K+2:]
        H = [sum(z*step_taylor(c,diag,edges,t,P) for z,t in row) for row in terms]
        if all(h-e <= bd[1][1] and h+e >= bd[1][0] for h,e,bd in zip(H,Eq,checked)):
            prefix = (full[0],) + tuple(full[1:J+2]) + tuple(full[K+2:K+3+J])
            retained.append(dict(full=full,prefix=prefix,centers=H))
    return dict(complete=True, boxes_requested=total, boxes_visited=visited,
                retained=retained, errors=errors, observable_errors=Eq,
                statistical_radii=[(hi-lo)/2 for (lo,hi),_,_ in checked],
                representation=[eps for _,_,eps in checked],
                outer_radii=[(ref[1]-ref[0])/2+eps+2*e for (ref,_,eps),e in zip(checked,Eq)])


def diameter_certified(radii: Sequence[F], cert: dict, delta: F) -> bool:
    delta = rat(delta)
    if not radii or delta <= 0 or any(rat(r) < 0 for r in radii):
        raise ValueError("Nonnegative nonempty radii and positive target required")
    return cert['L']*(2*cert['A']*max(map(rat,radii))+cert['E']) <= delta
