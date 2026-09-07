"""Independent finite construction contracts (all work is offline).

Input accuracies are external hypotheses.  Unlike a residual certificate,
acceptance here binds the requested horizon, precision, stage/query interface,
numerical name, and rounding allowance BEFORE invoking synthesis. It then fixes
reference points, tie rules, and covering allowances before reading targets.  No compiler selection, distance, or
rounding helper is imported.  This is an executable contract, not a formal
proof checker or a certificate of the supplied moment oracle.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from typing import Callable
from types import MappingProxyType
import hashlib
import json


class ContractError(ValueError):
    """A finite program does not implement its declared construction."""


def _norm(x, y):
    if len(x) != len(y):
        raise ContractError('state dimension mismatch')
    return max((abs(F(a)-F(b)) for a, b in zip(x, y)), default=F(0))


def _round_even(value, bits):
    """Exact ties-to-even rounding, independently of the compiler helper."""
    value = F(value) * (1 << bits)
    lower, rem = divmod(value.numerator, value.denominator)
    if 2*rem > value.denominator or (2*rem == value.denominator and lower % 2):
        lower += 1
    return F(lower, 1 << bits)


@dataclass(frozen=True)
class ConstructionCertificate:
    accepted: bool
    violations: tuple
    transition_entries: int
    output_entries: int
    candidate_counts: tuple
    radii: tuple
    max_selected_distance: tuple
    # The allowances depend only on the candidate data and representatives.
    # They never depend on the supplied transition targets.
    grid_order_limits: tuple
    checks: int
    request_digest: str
    input_digest: str
    total_error: F

    def require(self):
        if not self.accepted:
            raise ContractError('construction contract rejected: '+repr(self.violations[:4]))
        return self


def _input_digest(records):
    data = json.dumps(records, default=str, separators=(',', ':')).encode('ascii')
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class ConstructionRequest:
    """Trusted, immutable specification fixed BEFORE synthesis.

    raw_error is an EXTERNAL input-accuracy hypothesis for both callbacks.
    The request checks its compatibility with the deterministic rounding rule;
    it does not prove an arbitrary numerical oracle correct.
    """
    horizon: int
    commands: int
    reports: int
    budget: int
    output_bits: int
    state_dimensions: tuple
    query_counts: tuple
    raw_error: F
    total_error: F
    input_digest: str

    def __post_init__(self):
        for name in ('horizon', 'commands', 'reports', 'budget'):
            if type(getattr(self, name)) is not int or getattr(self, name) < 1:
                raise ContractError('invalid requested '+name)
        if type(self.output_bits) is not int or self.output_bits < 0:
            raise ContractError('invalid requested precision')
        for dims in (self.state_dimensions, self.query_counts):
            if type(dims) is not tuple or len(dims) != self.horizon+1:
                raise ContractError('invalid requested stage dimensions')
            if any(type(d) is not int or d < 0 for d in dims):
                raise ContractError('invalid requested coordinate count')
        if self.raw_error < 0 or self.raw_error+self.rounding_error > self.total_error:
            raise ContractError('raw input plus requested rounding exceeds total allowance')
        if len(self.input_digest) != 64:
            raise ContractError('missing frozen input identity')

    @property
    def rounding_error(self):
        return F(1, 1 << (self.output_bits+1))

    @property
    def candidate_total(self):
        return sum((self.commands*self.reports)**n for n in range(self.horizon+1))

    @property
    def digest(self):
        return _input_digest(tuple(getattr(self, name) for name in self.__dataclass_fields__))


@dataclass(frozen=True)
class FrozenNumericalName:
    """All rational callbacks evaluated once before the compiler is invoked."""
    states: object
    queries: object

    def evaluate(self, history):
        return self.states[tuple(history)]

    def predict(self, history):
        return self.queries[tuple(history)]


def bind_request(horizon, commands, reports, budget, bits, evaluate, predict,
                 raw_error, total_error, max_candidates=1_000_000, *,
                 state_dimensions=None, query_counts=None):
    """Bind external numerical inputs, never the returned program's metadata.

    Optional stage schemas come from the application. Otherwise the numerical
    input interface supplies them, before synthesis; every history is checked.
    Enumerating and hashing the name is offline work only.
    """
    if any(type(x) is not int or x < 1 for x in (horizon, commands, reports, budget)):
        raise ContractError('invalid external synthesis dimensions')
    for dims in (state_dimensions, query_counts):
        if dims is not None and (len(dims) != horizon+1 or
                any(type(d) is not int or d < 0 for d in dims)):
            raise ContractError('external schema does not specify every requested stage')
    total = sum((commands*reports)**n for n in range(horizon+1))
    if total > max_candidates:
        raise ContractError('input binding exceeds explicit resource guard')
    alphabet = tuple(product(range(commands), range(reports)))
    states, queries, records, sd, qd = {}, {}, [], [], []
    for n in range(horizon+1):
        histories = tuple(product(alphabet, repeat=n))
        vs = tuple(tuple(F(x) for x in evaluate(h)) for h in histories)
        qs = tuple(tuple(F(x) for x in predict(h)) for h in histories)
        d = len(vs[0]) if state_dimensions is None else state_dimensions[n]
        k = len(qs[0]) if query_counts is None else query_counts[n]
        if any(len(v) != d for v in vs) or any(len(q) != k for q in qs):
            raise ContractError('external numerical interface has inconsistent dimensions')
        sd.append(d); qd.append(k); records.append((vs, qs))
        states.update(zip(histories, vs)); queries.update(zip(histories, qs))
    request = ConstructionRequest(horizon, commands, reports, budget, bits,
                tuple(sd), tuple(qd), F(raw_error), F(total_error), _input_digest(records))
    name = FrozenNumericalName(MappingProxyType(states), MappingProxyType(queries))
    return request, name



def inspect_construction(program, audit, commands: int, reports: int,
                         budget: int, evaluate: Callable, predict: Callable,
                         max_candidates: int = 1_000_000, *,
                         request: 'ConstructionRequest') -> ConstructionCertificate:
    """Re-enumerate frozen numerical inputs and check every table entry.

    The immutable request is supplied independently of the returned program.
    Callbacks must be the request-bound frozen numerical name. Reject
    non-integer/out-of-range entries, wrong representatives, and wrong ties.
    `audit.exact_vectors` and its reported radii are deliberately not trusted.
    """
    if not isinstance(request, ConstructionRequest):
        raise ContractError('an independently bound ConstructionRequest is required')
    if (commands, reports, budget) != (request.commands, request.reports, request.budget):
        raise ContractError('call arguments differ from bound request')
    if max_candidates < request.candidate_total:
        raise ContractError('independent enumeration exceeds explicit resource guard')
    bits, T = request.output_bits, request.horizon
    if type(program.output_bits) is not int or program.output_bits != bits:
        raise ContractError('returned precision differs from requested precision')
    if len(program.transitions) != T:
        raise ContractError('returned horizon differs from requested horizon')
    if len(audit.representatives) != T+1 or len(program.outputs) != T+1:
        raise ContractError('stage count differs from bound request')
    if len(program.state_counts) != T+1:
        raise ContractError('state count metadata differs from bound request')
    if any(type(k) is not int or not 1 <= k <= budget for k in program.state_counts):
        raise ContractError('invalid state count metadata')
    total = sum((commands*reports)**n for n in range(T+1))
    if total > max_candidates:
        raise ContractError('independent enumeration exceeds explicit resource guard')
    alphabet = tuple(product(range(commands), range(reports)))
    violations, centers, radii, frozen, counts = [], [], [], [], []
    frozen_predictions = []
    checks = 0
    input_records = []
    # Freeze the data and compute construction-only limits, before examining
    # a single supplied transition target.
    for n, reps in enumerate(audit.representatives):
        histories = tuple(product(alphabet, repeat=n))
        raw = tuple(tuple(F(x) for x in evaluate(h)) for h in histories)
        queries = tuple(tuple(F(x) for x in predict(h)) for h in histories)
        if any(len(v) != request.state_dimensions[n] for v in raw):
            raise ContractError('state dimension differs from bound request')
        if any(len(v) != request.query_counts[n] for v in queries):
            raise ContractError('query interface differs from bound request')
        input_records.append((raw, queries))
        points = tuple(tuple(_round_even(x, bits) for x in v) for v in raw)
        index = {h:i for i,h in enumerate(histories)}
        chosen = [0]
        distances = [_norm(p, points[0]) for p in points]
        for _ in range(1, min(budget, len(points))):
            eligible = [i for i in range(len(points)) if i not in chosen]
            best_radius = max(distances[i] for i in eligible)
            nxt = next(i for i in eligible if distances[i] == best_radius)
            chosen.append(nxt)
            distances = [min(d, _norm(p, points[nxt])) for d,p in zip(distances,points)]
        expected = tuple(histories[i] for i in chosen)
        checks += 1
        if tuple(reps) != expected:
            violations.append(('representative_selection', n))
        if len(reps) < 1 or len(reps) > budget or len(set(reps)) != len(reps):
            raise ContractError('invalid representative budget or repeated history')
        if any(h not in index for h in reps):
            raise ContractError('representative is not a feasible grid history')
        if program.state_counts[n] != len(reps):
            violations.append(('state_count', n))
        cs = tuple(points[index[h]] for h in reps)
        rad = max(min(_norm(p,c) for c in cs) for p in points)
        centers.append(cs); radii.append(rad); counts.append(len(points))
        frozen.append({h:p for h,p in zip(histories,points)})
        frozen_predictions.append(dict(zip(histories,queries)))
    if _input_digest(input_records) != request.input_digest:
        raise ContractError('numerical name differs from bound request')
    transition_entries, output_entries, maxima = 0, 0, []
    for n,reps in enumerate(audit.representatives):
        if len(program.outputs[n]) != len(reps):
            raise ContractError('output state dimension mismatch')
        for i,h in enumerate(reps):
            exact_name = frozen_predictions[n][h]
            stored = program.outputs[n][i]
            if len(stored) != len(exact_name):
                raise ContractError('output query count mismatch')
            for q,(v,z) in enumerate(zip(stored,exact_name)):
                expected = int(min(F(1),max(F(0),_round_even(z,bits)))*(1<<bits))
                checks += 1; output_entries += 1
                if type(v) is not int or v != expected:
                    violations.append(('output_rounding', n, i, q))
        if n == T:
            continue
        rows = program.transitions[n]
        if len(rows) != len(reps):
            raise ContractError('transition state count mismatch')
        measured = F(0)
        for i,h in enumerate(reps):
            if len(rows[i]) != commands:
                raise ContractError('command dimension mismatch')
            for u in range(commands):
                if len(rows[i][u]) != reports:
                    raise ContractError('report dimension mismatch')
                for x in range(reports):
                    target = frozen[n+1][h+((u,x),)]
                    ds = tuple(_norm(target,c) for c in centers[n+1])
                    best = min(ds)
                    expected = ds.index(best)  # smallest-index tie rule
                    j = rows[i][u][x]
                    checks += 2; transition_entries += 1
                    if type(j) is not int or not 0 <= j < len(ds):
                        violations.append(('invalid_transition_index',n,i,u,x)); continue
                    measured = max(measured,ds[j])
                    if j != expected:
                        violations.append(('nearest_transition',n,i,u,x,j,expected))
                    if ds[j] > radii[n+1]:
                        violations.append(('fixed_cover_order',n,i,u,x))
        maxima.append(measured)
    return ConstructionCertificate(not violations,tuple(violations),transition_entries,
                                   output_entries,tuple(counts),tuple(radii),tuple(maxima),
                                   tuple(radii[1:]),checks,request.digest,
                                   request.input_digest,request.total_error)
