#!/usr/bin/env python3
"""Exact local certificates for max-of-multiaffine rational row polynomials.

No optimizer, floating-point tolerance, or convexification is used. Inputs are
explicit polynomial tests on products of probability simplexes. Compiling an
experiment into all marked feedback tests is a separate, finite model task.
The command 'check' re-enumerates every covering cell and every vertex; it does
not trust claimed minima or upper witnesses. Quantifier elimination is NOT
implemented by this program. Equality thresholds may need another algorithm.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import hashlib
import json
from pathlib import Path
from typing import Any, Iterator

Row = tuple[Q, ...]
Point = tuple[Row, ...]
Box = tuple[int, ...]
Term = tuple[Q, tuple[tuple[int, int], ...]]

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()

@dataclass(frozen=True)
class Problem:
    sizes: tuple[int, ...]
    tests: tuple[tuple[Term, ...], ...]
    raw: dict[str, Any]

    @classmethod
    def load(cls, raw: dict[str, Any]) -> 'Problem':
        require(isinstance(raw, dict), 'Input must be an object')
        sizes = tuple(raw['row_sizes'])
        require(bool(sizes) and all(type(d) is int and d > 0 for d in sizes), 'Positive row sizes required')
        tests = []
        for test in raw['tests']:
            terms = []
            for coefficient, variables in test['terms']:
                require(isinstance(coefficient, (str, int)), 'Exact rational coefficient required')
                pairs = tuple(tuple(pair) for pair in variables)
                require(all(len(pair) == 2 and all(type(x) is int for x in pair) for pair in pairs), 'Invalid coordinate')
                require(all(0 <= r < len(sizes) and 0 <= j < sizes[r] for r, j in pairs), 'Coordinate out of range')
                require(len({r for r, _ in pairs}) == len(pairs), 'A monomial cannot repeat a row: not multiaffine')
                terms.append((Q(coefficient), pairs))
            tests.append(tuple(terms))
        require(bool(tests), 'At least one test is required')
        return cls(sizes, tuple(tests), raw)

    @property
    def digest(self) -> str:
        return hashlib.sha256(canonical(self.raw)).hexdigest()

    def evaluate(self, point: Point) -> tuple[Q, ...]:
        require(len(point) == len(self.sizes), 'Wrong number of rows')
        for d, row in zip(self.sizes, point):
            require(len(row) == d and sum(row) == 1 and all(x >= 0 for x in row), 'Point is not a stochastic row table')
        result = []
        for polynomial in self.tests:
            value = Q(0)
            for coef, variables in polynomial:
                term = coef
                for r, j in variables:
                    term *= point[r][j]
                value += term
            result.append(value)
        return tuple(result)

def row_vertices(box: Box, mesh: int) -> tuple[Row, ...]:
    d = len(box)
    lo = tuple(Q(b, mesh) for b in box)
    hi = tuple(Q(b + 1, mesh) for b in box)
    if sum(lo) > 1 or sum(hi) < 1:
        return ()
    vertices: set[Row] = set()
    for free in range(d):
        fixed = [j for j in range(d) if j != free]
        for bits in product((0, 1), repeat=d-1):
            row = [Q(0)] * d
            for j, bit in zip(fixed, bits):
                row[j] = hi[j] if bit else lo[j]
            row[free] = 1 - sum(row)
            if lo[free] <= row[free] <= hi[free]:
                vertices.add(tuple(row))
    return tuple(sorted(vertices))

def row_cells(d: int, mesh: int) -> list[tuple[Box, tuple[Row, ...]]]:
    require(type(mesh) is int and mesh >= 1, 'Positive integer mesh required')
    if d == 1:
        return [((mesh-1,), ((Q(1),),))]
    out = []
    for box in product(range(mesh), repeat=d):
        vertices = row_vertices(box, mesh)
        if vertices:
            out.append((box, vertices))
    return out

def cells(problem: Problem, mesh: int, max_cells: int = 1_000_000) -> Iterator[tuple[tuple[Box, ...], tuple[tuple[Row, ...], ...]]]:
    require(type(mesh) is int and mesh >= 1, 'Positive integer mesh required')
    require(type(max_cells) is int and max_cells > 0, 'Positive cell limit required')
    require(all(d == 1 or mesh**d <= max_cells for d in problem.sizes), 'Row box enumeration exceeds --max-cells; increase it explicitly')
    require(all(d == 1 or d * 2**(d-1) <= 4*max_cells for d in problem.sizes), 'Row vertex enumeration exceeds the explicit work limit')
    choices = [row_cells(d, mesh) for d in problem.sizes]
    count = 1
    for choice in choices:
        count *= len(choice)
    require(count <= max_cells, f'Full cover has {count} cells; increase --max-cells explicitly (no partial certificate emitted)')
    for selected in product(*choices):
        yield tuple(x[0] for x in selected), tuple(x[1] for x in selected)

def make_certificate(problem: Problem, mesh: int, max_cells: int = 1_000_000) -> dict[str, Any]:
    lower = None
    upper = None
    witness = None
    records = []
    evaluations = 0
    for boxes, row_sets in cells(problem, mesh, max_cells):
        minima: list[Q] | None = None
        for vertex in product(*row_sets):
            values = problem.evaluate(vertex)
            evaluations += 1
            minima = list(values) if minima is None else [min(a, b) for a, b in zip(minima, values)]
            objective = max(values)
            if upper is None or objective < upper:
                upper, witness = objective, vertex
        require(minima is not None, 'Internal empty cell')
        test = max(range(len(minima)), key=minima.__getitem__)
        local_lower = minima[test]
        lower = local_lower if lower is None else min(lower, local_lower)
        records.append({'boxes': boxes, 'test': test, 'vertex_min': str(local_lower)})
    require(lower is not None and upper is not None and witness is not None, 'No policy cell')
    return {'format': 'GTF-I-local-test-certificate-v1', 'problem_sha256': problem.digest,
            'mesh': mesh, 'lower': str(lower), 'upper': str(upper),
            'upper_rows': [[str(x) for x in row] for row in witness],
            'cells': records, 'producer_vertex_evaluations': evaluations,
            'scope': 'Exact rational polynomial certificate at the given row budgets; model compilation and physical data certification remain separate.'}

def check_certificate(problem: Problem, cert: dict[str, Any], max_cells: int = 1_000_000) -> dict[str, Any]:
    require(cert.get('format') == 'GTF-I-local-test-certificate-v1', 'Wrong certificate format')
    require(cert.get('problem_sha256') == problem.digest, 'Problem digest mismatch')
    mesh = cert['mesh']; low = Q(cert['lower']); up = Q(cert['upper'])
    require(low <= up, 'Reversed interval')
    records = {}
    for record in cert['cells']:
        key = tuple(tuple(row) for row in record['boxes'])
        require(key not in records, 'Duplicate cell')
        records[key] = record
    visited = set(); evaluations = 0
    for boxes, row_sets in cells(problem, mesh, max_cells):
        require(boxes in records, 'Coverage missing a cell')
        visited.add(boxes); record = records[boxes]
        i = record['test']
        require(type(i) is int and 0 <= i < len(problem.tests), 'Invalid test index')
        values = []
        for vertex in product(*row_sets):
            v = problem.evaluate(vertex)[i]; evaluations += 1
            require(v >= low, 'Claimed lower bound fails at a vertex')
            values.append(v)
        require(min(values) == Q(record['vertex_min']), 'Local minimum mismatch')
    require(visited == set(records), 'Certificate includes an extra cell')
    witness = tuple(tuple(Q(x) for x in row) for row in cert['upper_rows'])
    require(max(problem.evaluate(witness)) <= up, 'Upper row table does not attain claimed bound')
    return {'status': 'verified', 'problem_sha256': problem.digest, 'lower': str(low), 'upper': str(up),
            'cells_checked': len(visited), 'vertex_inequalities_checked': evaluations,
            'row_sizes': problem.sizes, 'resource_enlargement': False}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    a = sub.add_parser('make'); a.add_argument('input', type=Path); a.add_argument('output', type=Path); a.add_argument('--mesh', type=int, default=4); a.add_argument('--max-cells', type=int, default=1_000_000)
    b = sub.add_parser('check'); b.add_argument('input', type=Path); b.add_argument('certificate', type=Path); b.add_argument('--max-cells', type=int, default=1_000_000)
    args = parser.parse_args()
    try:
        p = Problem.load(json.loads(args.input.read_text()))
        if args.command == 'make':
            c = make_certificate(p, args.mesh, args.max_cells)
            checked = check_certificate(p, c, args.max_cells)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(c, indent=2)+'\n')
            print(json.dumps(checked, indent=2))
        else:
            print(json.dumps(check_certificate(p, json.loads(args.certificate.read_text()), args.max_cells), indent=2))
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, 'ERROR: '+str(exc)+'\n')
if __name__ == '__main__':
    main()
