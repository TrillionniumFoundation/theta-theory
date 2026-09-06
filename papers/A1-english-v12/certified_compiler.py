"""Offline numerical certificates and adaptive meshes; no runtime oracle.

The accuracy of input advice is a hypothesis, not inferred from its numerical
consistency. The verifier returns explicit residual bounds for the supplied
program, including a corrupted one. It never treats approximate states as
reachable states. `Machine` and the immutable integer `Program` are unchanged.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from typing import Callable, Sequence
from finite_compiler import Program, Audit, compile_tables, distance, dyadic
from construction_contracts import inspect_construction


def formal_labels(degree: int, rank: int) -> tuple[tuple[int, ...], ...]:
    if degree < 0 or rank < 1:
        raise ValueError('nonnegative degree and positive rank required')
    if rank == 1:
        return ((degree,),)
    return tuple((i,)+tail for i in range(degree+1)
                 for tail in formal_labels(degree-i, rank-1))


def multiply(poly: dict, factor: Sequence[F]) -> dict:
    rank = len(factor)
    result = {}
    for alpha, coeff in poly.items():
        for i, value in enumerate(factor):
            beta = tuple(alpha[j]+(i == j) for j in range(rank))
            result[beta] = result.get(beta, F(0))+coeff*value
    return result


class MomentAdvice:
    """Certified formal coefficient/moment data for a fixed finite horizon.

    Bounds B and kappa apply to the true experiment; delta bounds each supplied
    entry's error. These are external certificates, not inferred by this class.
    Query coefficients are exact and their l1 norm must be <= 1 here.
    """
    def __init__(self, cells, moments, commands, horizon, delta, B, kappa):
        self.cells = tuple(tuple(map(F, row)) for row in cells)
        self.moments = {tuple(k): F(v) for k, v in moments.items()}
        self.commands = tuple(tuple(map(F, row)) for row in commands)
        self.N, self.delta, self.B, self.kappa = horizon, F(delta), F(B), F(kappa)
        self.J, self.r = len(self.cells), len(self.cells[0])
        if horizon < 1 or self.delta <= 0 or self.B < 1 or not 0 < self.kappa <= 1:
            raise ValueError('invalid certificate parameters')
        if any(len(row) != self.r for row in self.cells):
            raise ValueError('inconsistent cell dimensions')
        if any(len(g) != self.J or any(not 0 <= x <= 1 for x in g) for g in self.commands):
            raise ValueError('invalid finite command grid')
        required = {a for n in range(horizon+1) for a in formal_labels(n, self.r)}
        if not required <= self.moments.keys():
            raise ValueError('incomplete formal moment advice')
        if self.J*self.r*self.delta > 1:
            raise ValueError('factor perturbation exceeds the declared bound')
        self.cache = {}
        self.max_quotient_bound = F(0)
        self.min_denominator = None

    def factor(self, u, x):
        g = self.commands[u]
        if not 0 <= x <= self.J:
            raise ValueError('unknown report')
        if x < self.J:
            return tuple(g[x]*v for v in self.cells[x])
        return tuple(sum((1-g[j])*self.cells[j][i] for j in range(self.J))
                     for i in range(self.r))

    def product(self, history):
        if history not in self.cache:
            p = {(0,)*self.r: F(1)}
            for u, x in history:
                p = multiply(p, self.factor(u, x))
            self.cache[history] = p
        return self.cache[history]

    def integral(self, poly):
        return sum(c*self.moments[a] for a, c in poly.items())

    def ratio(self, history, query):
        n = len(history)
        if n > self.N or sum(abs(v) for v in query.values()) > 1:
            raise ValueError('query outside the certified interface')
        p = self.product(history)
        z = self.integral(p)
        D = (n*self.J*self.r*(self.B+1)**(n-1) if n else F(0))+(self.B+1)**n
        err = self.delta*D
        if err > self.kappa**n/2 or z < self.kappa**n/2:
            raise ValueError('insufficient input accuracy or invalid positive-evidence certificate')
        numerator = sum(c*d*self.moments[tuple(x+y for x, y in zip(a,b))]
                        for a, c in p.items() for b, d in query.items())
        bound = (1+sum(abs(v) for v in query.values()))*err/z
        self.max_quotient_bound = max(self.max_quotient_bound, bound)
        self.min_denominator = z if self.min_denominator is None else min(self.min_denominator,z)
        return numerator/z, bound

    def state(self, history):
        return tuple(self.ratio(history, {a:F(1)})[0]
                     for a in formal_labels(self.N-len(history),self.r))

    def predictions(self, history):
        basis = [tuple(F(1,2) if i == 0 else F(0) for i in range(self.r))]
        for j in range(1,self.r):
            basis.append(tuple(F(1,2) if i == 0 else F(1,32) if i == j else F(0)
                               for i in range(self.r)))
        values = []
        for word in product(basis, repeat=self.N-len(history)):
            q = {(0,)*self.r:F(1)}
            for f in word:
                q = multiply(q, f)
            values.append(self.ratio(history,q)[0])
        return tuple(values)


@dataclass(frozen=True)
class Residuals:
    transition: tuple[F, ...]
    output: tuple[F, ...]
    state_error: tuple[F, ...]
    query_error: tuple[F, ...]


def verify_program(program: Program, audit: Audit, command_count: int,
                   report_count: int, evaluate: Callable, predict: Callable,
                   tau: F, mesh: F, L: Sequence[F], G: Sequence[F], K: Sequence[F]) -> Residuals:
    """Compute Proposition program-certificate's bounds from fresh evaluations.

    `tau` bounds the callbacks' errors (not the error of Audit.exact_vectors,
    which is intentionally never used here). All representative histories stay
    offline. Every query, including nonconstant ones, contributes to the maximum.
    """
    T = len(program.transitions)
    if tau < 0 or mesh < 0 or len(L) != T or len(G) != T or len(K) != T+1:
        raise ValueError('invalid residual-certificate dimensions or tolerances')
    states = tuple(tuple(tuple(evaluate(h)) for h in stage) for stage in audit.representatives)
    d, o, E = [], [], [F(0)]
    for n, stage in enumerate(audit.representatives):
        outputs = []
        for i, hist in enumerate(stage):
            q = tuple(F(x,1<<program.output_bits) for x in program.outputs[n][i])
            outputs.append(distance(q, tuple(predict(hist)))+tau)
        o.append(max(outputs))
        if n == T:
            continue
        entries = []
        for i, hist in enumerate(stage):
            for u in range(command_count):
                for x in range(report_count):
                    j = program.transitions[n][i][u][x]
                    if not 0 <= j < len(states[n+1]):
                        raise ValueError('transition index outside state budget')
                    entries.append(distance(tuple(evaluate(hist+((u,x),))), states[n+1][j])+2*tau)
        d.append(max(entries))
        E.append(L[n]*E[n]+G[n]*mesh+d[-1])
    return Residuals(tuple(d),tuple(o),tuple(E),tuple(K[n]*E[n]+o[n] for n in range(T+1)))


def approximate_radii(audit, bits, commands, reports, evaluate):
    alphabet = tuple(product(range(commands),range(reports)))
    radii = []
    for n, reps in enumerate(audit.representatives):
        centers = tuple(dyadic(tuple(evaluate(h)), bits) for h in reps)
        radii.append(max(min(distance(dyadic(tuple(evaluate(h)),bits),c) for c in centers)
                         for h in product(alphabet,repeat=n)))
    return tuple(radii)


def adaptive_compile(horizon: int, reports: int, budget: int, A: F, factory: Callable,
                     absolute_tolerance: F = F(0), max_bits: int = 30,
                     max_candidates: int = 1_000_000):
    """Factory(b,tau) returns (command_count,evaluate,predict,metadata).

    The factory certifies an h=2^-b command net and callback error <= tau/2.
    Rounding uses b+2 places, leaving the total error below tau. Resource guards
    raise explicitly; they are safety limits of this implementation, not claims
    that the mathematical enumeration requires bounded memory or bounded time.
    """
    A, absolute_tolerance = F(A), F(absolute_tolerance)
    if A < 0 or not 0 <= absolute_tolerance <= 1 or max_bits < 0:
        raise ValueError('invalid adaptive parameters')
    c = A+2
    stages = []
    for b in range(max_bits+1):
        h = F(1,1<<b)
        count, evaluate, predict, metadata = factory(b,h)
        program,audit = compile_tables(horizon,count,reports,budget,b+2,evaluate,predict,max_candidates)
        contract = inspect_construction(program,audit,count,reports,budget,
                                        evaluate,predict,max_candidates).require()
        rs = contract.radii
        r = max(rs[1:])
        lower,upper = max(F(0),r/2-h),r+c*h
        stopped_radius = r >= 4*c*h
        stages.append({'b':b,'h':h,'r':r,'lower':lower,'upper':upper,
                       'radius_stop':stopped_radius,'candidate_counts':audit.candidate_counts,
                       'construction_checks':contract.checks,
                       'construction_accepted':contract.accepted})
        if stopped_radius or h <= absolute_tolerance:
            return program,audit,tuple(stages),metadata
    raise RuntimeError('explicit refinement guard reached; increase max_bits/resources')


def robust_adaptive_compile(horizon: int, reports: int, budget: int, A: F,
                            factory: Callable, data_floor: F,
                            max_bits: int = 30,
                            max_candidates: int = 1_000_000):
    """One program for every model compatible with a common numerical name.

    factory(b,h,tau), tau=max(h,data_floor), must provide an h-net and
    callback error <=tau/2 for EACH compatible model. The same fixed name is
    used by construction and the independent gate. No model-selection or
    zero-radius decision is made. This is an additional interface: the
    arbitrarily refinable, zero-floor algorithm above is unchanged.
    """
    A, rho = F(A), F(data_floor)
    if A < 0 or not 0 < rho <= 1 or horizon < 1 or max_bits < 0:
        raise ValueError('invalid robust adaptive parameters')
    c = A+4
    trace = []
    for b in range(max_bits+1):
        h = F(1,1<<b)
        tau = max(h,rho)
        count,evaluate,predict,metadata = factory(b,h,tau)
        program,audit = compile_tables(horizon,count,reports,budget,b+2,
                                      evaluate,predict,max_candidates)
        certificate = inspect_construction(program,audit,count,reports,budget,
                                           evaluate,predict,max_candidates).require()
        r = max(certificate.radii[1:])
        radius_stop, floor_stop = r >= 4*c*h, h <= rho
        trace.append({'b':b,'h':h,'tau':tau,'r':r,
                      'lower':max(F(0),r/2-tau),'upper':r+A*h+2*tau,
                      'radius_stop':radius_stop,'floor_stop':floor_stop,
                      'construction_accepted':True,
                      'construction_checks':certificate.checks,
                      'candidate_counts':certificate.candidate_counts})
        if radius_stop or floor_stop:
            return program,audit,tuple(trace),metadata
    raise RuntimeError('explicit refinement guard reached; increase max_bits/resources')
