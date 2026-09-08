"""Finite-table compiler for the compact-state theorem.

All evaluation callbacks run offline. Program contains integer transitions and
fixed-point output integers only. Audit histories are returned separately and
must not be supplied to the running Machine. No continuum cover is certified
by this implementation; its guarantees are the hypotheses of the manuscript.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from typing import Callable, Sequence

Vector = tuple[F, ...]
History = tuple[tuple[int, int], ...]
Evaluator = Callable[[History], Sequence[F]]


def distance(a: Sequence[F], b: Sequence[F]) -> F:
    if len(a) != len(b):
        raise ValueError("vector dimensions differ")
    return max((abs(x-y) for x, y in zip(a, b)), default=F(0))


def dyadic(v: Sequence[F], bits: int) -> Vector:
    scale = 1 << bits
    return tuple(F(round(x*scale), scale) for x in v)


def greedy(points: Sequence[Vector], budget: int) -> tuple[int, ...]:
    if budget < 1 or not points:
        raise ValueError("positive budget and nonempty point list required")
    chosen = [0]
    nearest = [distance(v, points[0]) for v in points]
    for _ in range(1, min(budget, len(points))):
        available = (j for j in range(len(points)) if j not in chosen)
        j = max(available, key=lambda j: (nearest[j], -j))
        chosen.append(j)
        nearest = [min(d, distance(v, points[j])) for d, v in zip(nearest, points)]
    return tuple(chosen)


@dataclass(frozen=True)
class Program:
    # transitions[stage][old_index][command_index][report]
    transitions: tuple
    # outputs[stage][index][query] / 2**output_bits
    outputs: tuple
    output_bits: int
    state_counts: tuple[int, ...]


@dataclass(frozen=True)
class Audit:
    representatives: tuple
    exact_vectors: tuple
    sample_cover_radii: tuple[F, ...]
    candidate_counts: tuple[int, ...]


class Machine:
    """The only retained mutable field is an index; stage is supplied externally."""
    __slots__ = ("index",)

    def __init__(self) -> None:
        self.index = 0

    def step(self, program: Program, stage: int, command: int, report: int) -> None:
        self.index = program.transitions[stage][self.index][command][report]

    def output(self, program: Program, stage: int, query: int) -> F:
        return F(program.outputs[stage][self.index][query], 1 << program.output_bits)


def compile_tables(horizon: int, command_count: int, report_count: int,
                   budget: int, bits: int, evaluate: Evaluator,
                   predict: Evaluator, max_candidates: int = 1_000_000
                   ) -> tuple[Program, Audit]:
    """Compile finitely many grid histories; reject accidental exponential jobs.

    `evaluate` and `predict` return rational approximations. In a certified
    application their errors must be added to the dyadic rounding allowance.
    Exact Fraction callbacks, as in the tests, incur only rounding error.
    """
    if min(horizon, command_count, report_count, budget) < 1 or bits < 0:
        raise ValueError("invalid dimensions, budget, or precision")
    total = sum((command_count*report_count)**n for n in range(horizon+1))
    if total > max_candidates:
        raise ValueError(f"{total} candidates exceed explicit limit {max_candidates}")
    alphabet = tuple(product(range(command_count), range(report_count)))
    reps, vectors, approximations, radii, counts = [], [], [], [], []
    for n in range(horizon+1):
        histories = tuple(product(alphabet, repeat=n))
        exact = tuple(tuple(evaluate(h)) for h in histories)
        approx = tuple(dyadic(v, bits) for v in exact)
        selected = greedy(approx, budget)
        reps.append(tuple(histories[j] for j in selected))
        vectors.append(tuple(exact[j] for j in selected))
        approximations.append(tuple(approx[j] for j in selected))
        radii.append(max(min(distance(v, c) for c in vectors[-1]) for v in exact))
        counts.append(len(histories))
    transitions = []
    for n in range(horizon):
        rows = []
        for hist in reps[n]:
            commands = []
            for u in range(command_count):
                reports = []
                for x in range(report_count):
                    y = dyadic(tuple(evaluate(hist + ((u, x),))), bits)
                    nxt = min(range(len(reps[n+1])),
                              key=lambda j: (distance(y, approximations[n+1][j]), j))
                    reports.append(nxt)
                commands.append(tuple(reports))
            rows.append(tuple(commands))
        transitions.append(tuple(rows))
    scale = 1 << bits
    outputs = tuple(tuple(tuple(max(0, min(scale, round(v*scale)))
                                for v in predict(h)) for h in stage) for stage in reps)
    return (Program(tuple(transitions), outputs, bits, tuple(map(len, reps))),
            Audit(tuple(reps), tuple(vectors), tuple(radii), tuple(counts)))
