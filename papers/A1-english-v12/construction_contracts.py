"""Independent finite construction contracts (all work is offline).

Input accuracies are external hypotheses.  Unlike a residual certificate,
acceptance here fixes the reference points, tie rules, and covering allowances
BEFORE reading the transition targets.  No compiler selection, distance, or
rounding helper is imported.  This is an executable contract, not a formal
proof checker or a certificate of the supplied moment oracle.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from typing import Callable


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

    def require(self):
        if not self.accepted:
            raise ContractError('construction contract rejected: '+repr(self.violations[:4]))
        return self


def inspect_construction(program, audit, commands: int, reports: int,
                         budget: int, evaluate: Callable, predict: Callable,
                         max_candidates: int = 1_000_000) -> ConstructionCertificate:
    """Re-enumerate frozen numerical inputs and check every table entry.

    Callbacks must return a fixed numerical name on repeated calls. The table's
    `output_bits` also specifies the construction rounding precision. Reject
    non-integer/out-of-range entries, wrong representatives, and wrong ties.
    `audit.exact_vectors` and its reported radii are deliberately not trusted.
    """
    if min(commands, reports, budget) < 1:
        raise ContractError('positive dimensions and budget required')
    bits = program.output_bits
    if type(bits) is not int or bits < 0:
        raise ContractError('nonnegative integer precision required')
    T = len(program.transitions)
    if len(audit.representatives) != T+1 or len(program.outputs) != T+1:
        raise ContractError('stage count mismatch')
    if len(program.state_counts) != T+1:
        raise ContractError('state count metadata mismatch')
    total = sum((commands*reports)**n for n in range(T+1))
    if total > max_candidates:
        raise ContractError('independent enumeration exceeds explicit resource guard')
    alphabet = tuple(product(range(commands), range(reports)))
    violations, centers, radii, frozen, counts = [], [], [], [], []
    checks = 0
    # Freeze the data and compute construction-only limits, before examining
    # a single supplied transition target.
    for n, reps in enumerate(audit.representatives):
        histories = tuple(product(alphabet, repeat=n))
        points = tuple(tuple(_round_even(x, bits) for x in evaluate(h)) for h in histories)
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
    transition_entries, output_entries, maxima = 0, 0, []
    for n,reps in enumerate(audit.representatives):
        if len(program.outputs[n]) != len(reps):
            raise ContractError('output state dimension mismatch')
        for i,h in enumerate(reps):
            exact_name = tuple(F(x) for x in predict(h))
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
                                   tuple(radii[1:]),checks)
