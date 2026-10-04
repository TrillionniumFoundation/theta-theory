#!/usr/bin/env python3
"""Integer reference for Theorem instrumentstream65 (fixed rational Kraus data).

Only the standard library is used. The physical specification is fixed before
N,L vary; loading an arbitrary specification does not give uniform-in-dimension
complexity. CPython allocation and OS entropy are not a certified bit machine.
The proof charges the integer recurrence, with an ideal fresh-fair-bit input.
The CLI emits one outcome immediately and a final legal numerical matrix.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

G = tuple[int, int]
Matrix = list[list[G]]
ZERO: G = (0, 0)

def add(a: G, b: G) -> G:
    return a[0] + b[0], a[1] + b[1]

def mul(a: G, b: G) -> G:
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]

def conj(a: G) -> G:
    return a[0], -a[1]

def scale(a: G, n: int) -> G:
    return a[0]*n, a[1]*n

def zero(d: int) -> Matrix:
    return [[ZERO for _ in range(d)] for _ in range(d)]

def identity(d: int, n: int = 1) -> Matrix:
    a = zero(d)
    for i in range(d):
        a[i][i] = (n, 0)
    return a

def adjoint(a: Matrix) -> Matrix:
    return [[conj(a[j][i]) for j in range(len(a))] for i in range(len(a))]

def product(a: Matrix, b: Matrix) -> Matrix:
    d = len(a)
    c = zero(d)
    for i in range(d):
        for j in range(d):
            for k in range(d):
                c[i][j] = add(c[i][j], mul(a[i][k], b[k][j]))
    return c

def plus(a: Matrix, b: Matrix) -> Matrix:
    return [[add(x, y) for x, y in zip(ar, br)] for ar, br in zip(a, b)]

def trace(a: Matrix) -> int:
    if any(a[i][i][1] for i in range(len(a))):
        raise ValueError("non-real diagonal")
    return sum(a[i][i][0] for i in range(len(a)))

def psd(a: Matrix) -> bool:
    """Exact fraction-free Schur test, for fixed-dimensional input validation."""
    if not a or a != adjoint(a):
        return False
    b = [row[:] for row in a]
    while b:
        pivot = b[0][0][0]
        if pivot < 0:
            return False
        if pivot == 0:
            if any(x != ZERO for x in b[0]):
                return False
            b = [row[1:] for row in b[1:]]
            continue
        c = zero(len(b)-1)
        for i in range(1, len(b)):
            for j in range(1, len(b)):
                u = scale(b[i][j], pivot)
                v = mul(b[i][0], b[0][j])
                c[i-1][j-1] = u[0]-v[0], u[1]-v[1]
        b = c
    return True

def toward_zero(n: int, d: int) -> int:
    if type(n) is not int or type(d) is not int or d <= 0:
        raise ValueError("integer numerator and positive integer divisor required")
    return n//d if n >= 0 else -((-n)//d)

def round_density(p: Matrix, B: int) -> Matrix:
    """Return numerator over B+2*d*d; p is positive with integer trace > 0."""
    d = len(p)
    z = trace(p)
    if type(B) is not int or B < 1 or z <= 0:
        raise ValueError("positive grid and nonzero positive trace required")
    a = zero(d)
    for i in range(d-1):
        a[i][i] = (toward_zero(B*p[i][i][0], z), 0)
    a[-1][-1] = (B-sum(a[i][i][0] for i in range(d-1)), 0)
    for i in range(d):
        for j in range(i+1, d):
            a[i][j] = tuple(toward_zero(B*x, z) for x in p[i][j])
            a[j][i] = conj(a[i][j])
    for i in range(d):
        a[i][i] = (a[i][i][0]+2*d, 0)
    return a

def uniform_below(total: int, bit: Callable[[], int]) -> int:
    if type(total) is not int or total < 1:
        raise ValueError("positive integer sampling total required")
    width = (total-1).bit_length()
    while True:
        value = 0
        for _ in range(width):
            x = bit()
            if type(x) is not int or x not in (0, 1):
                raise ValueError("bit source did not return 0 or 1")
            value = (value << 1) | x
        if value < total:
            return value
        # No trial counter, rejected word or random seed is retained.

def draw(weights: list[int], bit: Callable[[], int]) -> int:
    if not weights or any(type(w) is not int or w < 0 for w in weights):
        raise ValueError("nonnegative integer outcome weights required")
    if sum(weights) == 0:
        raise ValueError("zero instrument mass")
    positive = [i for i, w in enumerate(weights) if w]
    if len(positive) == 1:
        return positive[0]
    j = uniform_below(sum(weights), bit)
    for i, w in enumerate(weights):
        if j < w:
            return i
        j -= w
    raise RuntimeError("unreachable interval end")

def decode_matrix(value: object, d: int) -> Matrix:
    if not isinstance(value, list) or len(value) != d:
        raise ValueError("wrong matrix dimension")
    answer = []
    for row in value:
        if not isinstance(row, list) or len(row) != d:
            raise ValueError("wrong row dimension")
        r = []
        for x in row:
            if type(x) is int:
                r.append((x, 0))
            elif isinstance(x, list) and len(x) == 2 and all(type(t) is int for t in x):
                r.append((x[0], x[1]))
            else:
                raise ValueError("entries must be integers or Gaussian integer pairs")
        answer.append(r)
    return answer

@dataclass
class Specification:
    d: int
    q: int
    initial: Matrix
    commands: dict[str, list[list[Matrix]]]

    @classmethod
    def read(cls, path: Path) -> "Specification":
        return cls.from_dict(json.loads(path.read_text()))

    @classmethod
    def from_dict(cls, raw: dict) -> "Specification":
        if not isinstance(raw, dict):
            raise ValueError("specification must be a JSON object")
        d, q = raw.get("dimension"), raw.get("kraus_denominator")
        if type(d) is not int or d < 2 or type(q) is not int or q < 1:
            raise ValueError("dimension >= 2 and positive Kraus denominator required")
        initial = decode_matrix(raw["initial_numerator"], d)
        if not psd(initial) or trace(initial) <= 0:
            raise ValueError("initial numerator must be positive and nonzero")
        commands = {}
        supplied = raw.get("commands")
        if not isinstance(supplied, dict):
            raise ValueError("commands must be a dictionary")
        for a, outcomes in supplied.items():
            if not isinstance(a, str) or len(a) != 1 or not a.isascii() or a.isspace():
                raise ValueError("commands must be one nonspace ASCII character")
            if not isinstance(outcomes, list) or not outcomes:
                raise ValueError("instrument must be a nonempty outcome list")
            decoded = []
            completeness = zero(d)
            for branches in outcomes:
                if not isinstance(branches, list) or not branches:
                    raise ValueError("use a nonempty Kraus list, including an explicit zero matrix for a zero outcome")
                matrices = [decode_matrix(k, d) for k in branches]
                decoded.append(matrices)
                for k in matrices:
                    completeness = plus(completeness, product(adjoint(k), k))
            if completeness != identity(d, q*q):
                raise ValueError("Kraus completeness identity failed for command "+a)
            commands[a] = decoded
        if not commands:
            raise ValueError("empty command alphabet")
        return cls(d, q, initial, commands)

    def branches(self, p: Matrix, command: str) -> list[Matrix]:
        if command not in self.commands:
            raise ValueError("unknown command: "+repr(command))
        answer = []
        for matrices in self.commands[command]:
            a = zero(self.d)
            for k in matrices:
                a = plus(a, product(product(k, p), adjoint(k)))
            answer.append(a)
        return answer

class Streamer:
    def __init__(self, spec: Specification, N: int, L: int):
        if type(N) is not int or N < 2 or type(L) is not int or L < 2:
            raise ValueError("N,L must be integers at least two")
        self.spec, self.N, self.t = spec, N, 0
        b = min(L, N)+(6*spec.d*spec.d*(N+1)-1).bit_length()
        self.B = None if b >= N else 1 << b
        self.mode = "exact" if self.B is None else "positive-grid"
        self.p = [row[:] for row in spec.initial] if self.B is None else round_density(spec.initial, self.B)

    def step(self, command: str, bit: Callable[[], int]) -> int:
        if self.t >= self.N:
            raise ValueError("too many commands")
        branches = self.spec.branches(self.p, command)
        weights = [trace(p) for p in branches]
        if sum(weights) != self.spec.q**2*trace(self.p):
            raise RuntimeError("instrument mass invariant failed")
        y = draw(weights, bit)
        chosen = branches[y]
        self.p = chosen if self.B is None else round_density(chosen, self.B)
        self.t += 1
        return y

    def finish(self) -> dict:
        if self.t != self.N:
            raise ValueError("too few commands")
        return {"kind": "numerical-density-matrix",
                "mode": self.mode, "dimension": self.spec.d,
                "denominator_hex": hex(trace(self.p)),
                "numerator_hex": [[[hex(x), hex(y)] for x, y in row] for row in self.p]}

def read_decimal_line(stream, cap: int | None = None) -> int:
    value, found = 0, False
    while True:
        c = stream.read(1)
        if c == b"\n":
            if not found:
                raise ValueError("empty parameter line")
            return value
        if len(c) != 1 or not (48 <= c[0] <= 57):
            raise ValueError("decimal parameter line with newline required")
        found = True
        value = value*10+c[0]-48
        if cap is not None:
            value = min(cap, value)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, default=Path(__file__).parent/"inputs/qutrit-instrument.json")
    args = parser.parse_args()
    try:
        spec = Specification.read(args.spec)
        N = read_decimal_line(sys.stdin.buffer)
        if N < 2:
            raise ValueError("horizon below two")
        L = read_decimal_line(sys.stdin.buffer, N)
        sim = Streamer(spec, N, L)
        def os_bit() -> int:
            return os.urandom(1)[0] & 1
        while True:
            c = sys.stdin.buffer.read(1)
            if not c:
                break
            if c in b" \t\r\n":
                continue
            if c[0] >= 128:
                raise ValueError("non-ASCII command")
            y = sim.step(chr(c[0]), os_bit)
            print(json.dumps({"outcome": y}), flush=True)
        print(json.dumps(sim.finish(), sort_keys=True), flush=True)
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print("instrument_streaming: "+str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
