"""Round 53: clock-aware rational certificates with a bound observation contract.

The active certifying entry point is certify_outer, not a predicate on radii.
It validates/recomputes the certificate, checks the complete pulse map, runs
exhaustive enclosures itself, and returns immutable provenance and budgets.
Statistical coverage of the supplied reference bands is a separate premise.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from typing import Sequence
from tools import round51_certificates as core

ModelBox = core.ModelBox
ResourceLimit = core.ResourceLimit
rat, natural = core.rat, core.natural


class ContractError(ValueError):
    """The observation/model/certificate identities do not agree."""


def success_probability(rho: F, w: F) -> F:
    rho, w = rat(rho), rat(w)
    if not 0 <= rho <= 1 or not 0 <= w <= 1:
        raise ValueError("rho and w must lie in [0,1]")
    p = 1-rho+rho*w
    if p <= 0:
        raise ValueError("A positive recurring fast-probe probability is required")
    return p


@dataclass(frozen=True)
class CertificateSpec:
    box: ModelBox
    J: int
    delta: F
    t0: F
    rho: F
    w: F

    def __post_init__(self) -> None:
        if not isinstance(self.box, ModelBox):
            raise TypeError("box must be ModelBox")
        natural(self.J, "J")
        for name in ("delta", "t0", "rho", "w"):
            object.__setattr__(self, name, rat(getattr(self, name)))
        if not 0 < self.delta <= 1 or not 0 < self.t0 <= self.box.T:
            raise ValueError("Require 0<delta<=1 and 0<t0<=T")
        if 2*self.t0*self.box.Lambda > F(1,64):
            raise ValueError("Require Delta*Lambda<=1/64")
        success_probability(self.rho, self.w)


@dataclass(frozen=True)
class PulseCertificate:
    spec: CertificateSpec
    R: int
    N: int
    Delta: F
    tau: F
    p: F
    L: F
    A: F
    E: F
    kappa: F
    W: F | None = None
    kappa_weighted: F | None = None

    @property
    def m(self) -> int:
        return self.N+1


def certificate(spec: CertificateSpec, *, weighted: bool = False,
                max_order: int = 4096) -> PulseCertificate:
    if not isinstance(spec, CertificateSpec):
        raise TypeError("Use CertificateSpec, not an unbound certificate dictionary")
    natural(max_order, "max_order", 1)
    R = 4*spec.J+8
    if R > max_order:
        raise ResourceLimit("Jet order exceeds cap before power allocation")
    Delta, p = 2*spec.t0, success_probability(spec.rho,spec.w)
    x = Delta*spec.box.Lambda
    tau = 2*x/(1-x)
    L, N = spec.box.Q**(25*(spec.J+1)), R
    while L*Delta**(-R)*tau**N > spec.delta/2:
        N += 1
        if N > max_order:
            raise ResourceLimit("Clock remainder target exceeds order cap")
    A, E = 8*Delta**(-R)*4**N, Delta**(-R)*tau**N
    kap = p**(N+1)*spec.delta**2/(4*L**2*A**2)
    W = kw = None
    if weighted:
        _, rows = core.sampled_coefficients(Delta,R,N)
        W = max(sum(v*v/F(N+1-k) for k,v in enumerate(row)) for row in rows)
        if not 0 < W <= A*A:
            raise ArithmeticError("Weighted transform invariant failed")
        kw = p**(N+1)*spec.delta**2/(4*L**2*W)
    return PulseCertificate(spec,R,N,Delta,tau,p,L,A,E,kap,W,kw)


def validate_certificate(cert: PulseCertificate, *, max_order: int = 4096) -> None:
    if not isinstance(cert, PulseCertificate):
        raise ContractError("Unbound certificate type")
    expected = certificate(cert.spec, weighted=cert.W is not None, max_order=max_order)
    if cert != expected:
        raise ContractError("Certificate fields differ from exact recomputation")


# Canonical rows retain (coefficient, time), ordered by time. h(0)=0 is known.
def canonical_observable(row: Sequence[tuple[F,F]]) -> tuple[tuple[F,F], ...]:
    by_time: dict[F,F] = {}
    for coefficient, time in row:
        coefficient, time = rat(coefficient), rat(time)
        if time < 0:
            raise ContractError("Negative observation time")
        if time:
            by_time[time] = by_time.get(time,F(0))+coefficient
    return tuple((coefficient,time) for time,coefficient in sorted(by_time.items())
                 if coefficient)


def pulse_grid(cert: PulseCertificate) -> tuple:
    return tuple(canonical_observable(((F(1),k*cert.Delta+cert.spec.t0),
                                      (F(-1),k*cert.Delta)))
                 for k in range(cert.m))


def validate_grid(observables: Sequence, cert: PulseCertificate) -> tuple[int, ...]:
    expected = pulse_grid(cert)
    supplied = tuple(canonical_observable(row) for row in observables)
    if len(supplied) != cert.m:
        raise ContractError("Missing or extra pulse lags")
    if len(set(supplied)) != len(supplied):
        raise ContractError("Duplicated observable; length alone is not coverage")
    lookup = {row:i for i,row in enumerate(supplied)}
    if set(lookup) != set(expected):
        raise ContractError("Wrong observable, pulse scale, or clock")
    return tuple(lookup[row] for row in expected)


def radius_budget_satisfied(radii: Sequence[F], cert: PulseCertificate) -> bool:
    """Conditional arithmetic only: does NOT certify the source of these radii."""
    validate_certificate(cert)
    values = tuple(map(rat,radii))
    if len(values) != cert.m or any(v < 0 for v in values):
        raise ContractError("One nonnegative radius per required pulse lag")
    return cert.L*(2*cert.A*max(values)+cert.E) <= cert.spec.delta


@dataclass(frozen=True)
class OuterCertificateResult:
    certificate: PulseCertificate
    grid: tuple
    bands: tuple
    spatial_depth: int
    mesh_radius: F
    taylor_order: int
    full_boxes: tuple
    prefix_boxes: tuple
    base_errors: tuple
    statistical_radii: tuple
    representation_radii: tuple
    observable_errors: tuple
    outer_radii: tuple
    boxes_requested: int
    boxes_visited: int
    diameter_upper_bound: F
    status: str

    @property
    def diameter_certified(self) -> bool:
        return self.status == "certified"

    @property
    def complete(self) -> bool:
        return self.boxes_requested == self.boxes_visited


def certify_outer(box: ModelBox, J: int, K: int, r: F, P: int,
                  observables: Sequence, bands: Sequence,
                  cert: PulseCertificate, *, max_boxes: int = 100000,
                  max_order: int = 4096) -> OuterCertificateResult:
    """Validate the experiment before internally constructing an outer set.

    Permuted observations are accepted with their correspondingly permuted
    bands. Duplicate/cancelled terms inside one row are canonicalized exactly.
    A repeated lag, incorrect pulse coefficient, wrong clock, substituted
    model, or modified certificate is rejected, before enumeration.
    No caller-supplied outer result or numeric-radius list is trusted here.
    Empty outer sets are reported as empty, not as identified parameters.
    """
    natural(J,"J")
    validate_certificate(cert,max_order=max_order)
    if box != cert.spec.box or J != cert.spec.J:
        raise ContractError("Model box or physical depth differs from certificate")
    order = validate_grid(observables,cert)
    if len(bands) != cert.m:
        raise ContractError("Exactly one band per observable is required")
    checked = tuple(core.validate_band(*bands[i]) for i in order)
    grid = pulse_grid(cert)
    out = core.outer_boxes(box,J,K,r,P,grid,checked,max_boxes=max_boxes)
    if not out['complete'] or out['boxes_requested'] != out['boxes_visited']:
        raise ContractError("Incomplete enumeration is not certifiable")
    radii = tuple(out['outer_radii'])
    bound = cert.L*(2*cert.A*max(radii)+cert.E)
    status = ("empty" if not out['retained'] else
              "certified" if bound <= cert.spec.delta else "enclosed")
    return OuterCertificateResult(
        cert,grid,checked,K,rat(r),P,
        tuple(item['full'] for item in out['retained']),
        tuple(item['prefix'] for item in out['retained']),
        tuple((name,out['errors'][name]) for name in ('tail','mesh','taylor')),
        tuple(out['statistical_radii']),tuple(out['representation']),
        tuple(out['observable_errors']),radii,
        out['boxes_requested'],out['boxes_visited'],bound,status)
