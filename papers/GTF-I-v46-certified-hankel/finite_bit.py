#!/usr/bin/env python3
"""Integer-interval, table-free dyadic simulator for explicit rotation alphabets.

No transcendental floating-point routines are used. Python object allocation is
not the work-space constant in the manuscript's Turing-machine theorem. The
algorithm keeps O(r) fixed-precision integer registers, not a q-by-q row table.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
import random
from typing import Iterable


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def ceildiv(n: int, d: int) -> int:
    require(d > 0, 'positive divisor required')
    return -((-n) // d)


def ceil_log2(x: Fraction) -> int:
    require(x > 0, 'positive logarithm argument required')
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    while (1 << k) * x.denominator < x.numerator:
        k += 1
    return k


def root_floor(degree: int, radicand: int, bits: int) -> int:
    """floor(2**bits * radicand**(1/degree)) using integer bisection."""
    require(degree >= 1 and radicand >= 1 and bits >= 0, 'invalid root input')
    target = radicand << (degree * bits)
    lo, hi = 0, 1 << (bits + radicand.bit_length())
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** degree <= target:
            lo = mid
        else:
            hi = mid
    return lo


@dataclass(frozen=True)
class Interval:
    """Outward fixed-point interval [lo,hi]/2**bits."""
    lo: int
    hi: int
    bits: int

    def __post_init__(self) -> None:
        require(self.lo <= self.hi, 'reversed interval')

    @property
    def scale(self) -> int:
        return 1 << self.bits

    @classmethod
    def fraction(cls, value: Fraction | int, bits: int) -> Interval:
        value = Fraction(value)
        a = value.numerator << bits
        return cls(a // value.denominator, ceildiv(a, value.denominator), bits)

    def coercion(self, other: Interval | Fraction | int) -> Interval:
        if not isinstance(other, Interval):
            return Interval.fraction(other, self.bits)
        require(self.bits == other.bits, 'precision mismatch')
        return other

    def __add__(self, other: Interval | Fraction | int) -> Interval:
        o = self.coercion(other)
        return Interval(self.lo + o.lo, self.hi + o.hi, self.bits)

    __radd__ = __add__

    def __neg__(self) -> Interval:
        return Interval(-self.hi, -self.lo, self.bits)

    def __sub__(self, other: Interval | Fraction | int) -> Interval:
        return self + (-self.coercion(other))

    def __rsub__(self, other: Fraction | int) -> Interval:
        return self.coercion(other) + (-self)

    def __mul__(self, other: Interval | Fraction | int) -> Interval:
        o = self.coercion(other)
        terms = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return Interval(min(terms) // self.scale, ceildiv(max(terms), self.scale), self.bits)

    __rmul__ = __mul__

    def __truediv__(self, other: Interval | Fraction | int) -> Interval:
        o = self.coercion(other)
        require(o.lo > 0, 'division requires a strictly positive interval')
        vals = [(x * self.scale, y) for x in [self.lo, self.hi] for y in [o.lo, o.hi]]
        return Interval(min(a // b for a, b in vals), max(ceildiv(a, b) for a, b in vals), self.bits)

    def widen_units(self, units: int) -> Interval:
        return Interval(self.lo - units, self.hi + units, self.bits)

    def power(self, exponent: int) -> Interval:
        require(exponent >= 0, 'negative exponent')
        base, result = self, Interval.fraction(1, self.bits)
        while exponent:
            if exponent & 1:
                result = result * base
            exponent //= 2
            if exponent:
                base = base * base
        return result


def atan_inverse(n: int, bits: int) -> Interval:
    require(n >= 5 and bits >= 32, 'atan precision/range')
    x = Interval.fraction(Fraction(1, n), bits)
    x2, term = x * x, x
    out = Interval.fraction(0, bits)
    for j in range(bits + 10):
        out = out + (term / (2 * j + 1) if j % 2 == 0 else -(term / (2 * j + 1)))
        term = term * x2
    # Alternating-series remainder <= n**(-2*(bits+10)-1) < 2**(-bits).
    return out.widen_units(1)


def pi_interval(bits: int) -> Interval:
    return 16 * atan_inverse(5, bits) - 4 * atan_inverse(239, bits)


def sincos(x: Interval) -> tuple[Interval, Interval]:
    require(max(abs(x.lo), abs(x.hi)) <= 7 * x.scale, 'sincos range must be [-7,7]')
    require(x.bits >= 32, 'insufficient Taylor precision')
    x2 = x * x
    sine, cosine = x, Interval.fraction(1, x.bits)
    st, ct = sine, cosine
    for j in range(1, x.bits + 21):
        st = -(st * x2 / ((2 * j) * (2 * j + 1)))
        ct = -(ct * x2 / ((2 * j - 1) * (2 * j)))
        sine, cosine = sine + st, cosine + ct
    # For m>=bits+20>=52, e**7*7**(2*m+1)/(2*m+1)! < 2**(-bits).
    # All accumulated arithmetic errors are already included by directed rounding.
    return sine.widen_units(1), cosine.widen_units(1)


def lower_dyadic(i: Interval, out_bits: int) -> int:
    require(i.bits >= out_bits, 'output precision exceeds working precision')
    require(i.hi - i.lo <= (1 << (i.bits - out_bits)), 'interval not yet certified')
    return max(0, min(1 << out_bits, i.lo >> (i.bits - out_bits)))


class DyadicRotationMachine:
    """Angles alpha_i=2**(i/(r+1)); identity command has index 0."""
    def __init__(self, n: int, r: int = 1, epsilon: Fraction = Fraction(1, 1000),
                 rho: Fraction = Fraction(1, 10)) -> None:
        require(n >= 1 and r >= 1, 'n and r must be positive')
        require(0 < rho <= Fraction(1, 10) and 0 < epsilon < 1, 'invalid signal/tolerance')
        self.n, self.r, self.epsilon, self.rho = n, r, epsilon, rho
        self.b = ceil_log2(16 * Fraction(n + 2, 1) / epsilon)
        self.p = ceil_log2(16000 * Fraction(n + 2, 1) / epsilon)
        self.alpha = [0] + [root_floor(r + 1, 1 << i, self.p) % (1 << self.p) for i in range(1, r + 1)]
        scale = 1 << self.p
        bound = max(4, isqrt(2000 * (n + 2)) + 1)
        self.q = 0
        for q in range(4, bound + 1):
            distance = max(min((q * a) % scale, scale - (q * a) % scale) for a in self.alpha)
            if 1000 * n * (distance + q) <= q * q * scale:
                self.q = q
                break
        require(self.q >= 4, 'certified denominator search failed')
        self.working_bits = self.b + 64 + 4 * (n + 2).bit_length() + 4 * (self.b + 2).bit_length()
        while True:
            try:
                self._prepare()
                break
            except ValueError as exc:
                if 'not yet certified' not in str(exc):
                    raise
                self.working_bits *= 2
                require(self.working_bits <= 100000, 'precision resource guard')
        self.error_bound = Fraction(4*n+6, 1 << self.b) + Fraction(22, 7) * rho*n/Fraction(1 << self.p)
        require(self.error_bound < epsilon, 'uniform analytic error certificate failed')

    def _chord(self, angle: Fraction, radius: Interval) -> tuple[int, int, int, int]:
        qangle = angle * self.q
        offset = qangle.numerator // qangle.denominator
        t = qangle - offset
        h = 2 * self.pi / self.q
        denom = sincos(h)[0]
        a = radius * sincos((1-t)*h)[0] / denom
        b = radius * sincos(t*h)[0] / denom
        aa, bb = lower_dyadic(a, self.b), lower_dyadic(b, self.b)
        require(aa + bb <= 1 << self.b, 'nonstochastic dyadic chord')
        return offset % self.q, aa, bb, (1 << self.b) - aa - bb

    def _prepare(self) -> None:
        bits = self.working_bits
        self.pi = pi_interval(bits)
        lam = Interval.fraction(Fraction(4*self.n+1, 4*self.n), bits)
        inv = Interval.fraction(1, bits) / lam
        self.commands = [self._chord(Fraction(a, 1 << self.p), inv) for a in self.alpha]
        half = Interval.fraction(Fraction(1, 2), bits)
        self.initial = [self._chord(Fraction(j, 4), half) for j in range(4)]
        self.decoder_scale = 2*self.rho*lam.power(self.n)

    def row(self, state: int, command: int) -> tuple[tuple[int, int], ...]:
        require(0 <= state <= self.q and 0 <= command <= self.r, 'bad label or command')
        if state == self.q:
            return ((self.q, 1 << self.b),)
        off, a, b, c = self.commands[command]
        return (((state+off) % self.q, a), ((state+off+1) % self.q, b), (self.q, c))

    def initialization(self, seed: int) -> tuple[tuple[int, int], ...]:
        require(0 <= seed < 4, 'seed index outside 0..3')
        off, a, b, c = self.initial[seed]
        return ((off, a), ((off+1) % self.q, b), (self.q, c))

    def positive_answer_weight(self, state: int, query: int) -> int:
        require(0 <= query < 2 and 0 <= state <= self.q, 'bad output query or state')
        if state == self.q:
            return 1 << (self.b-1)
        sn, cs = sincos(2*self.pi*Fraction(state, self.q))
        prob = (1 + self.decoder_scale * (cs if query == 0 else sn)) / 2
        return lower_dyadic(prob, self.b)

    def sample(self, commands: Iterable[int], seed: int, query: int, rng: random.Random | None = None) -> int:
        rng = rng or random.SystemRandom()
        def draw(row: tuple[tuple[int, int], ...]) -> int:
            u = rng.getrandbits(self.b)
            for destination, mass in row:
                if u < mass:
                    return destination
                u -= mass
            raise RuntimeError('stochastic row invariant failed')
        state = draw(self.initialization(seed))
        count = 0
        for command in commands:
            require(count < self.n, 'too many commands')
            state = draw(self.row(state, command)); count += 1
        require(count == self.n, 'wrong command length')
        return 1 if rng.getrandbits(self.b) < self.positive_answer_weight(state, query) else -1

    def certificate(self) -> dict:
        return {'horizon': self.n, 'angles': self.r, 'polygon_vertices': self.q,
                'clean_labels': self.q+1, 'coin_bits_per_draw': self.b,
                'total_coin_bits': (self.n+2)*self.b, 'angle_bits': self.p,
                'interval_bits': self.working_bits, 'stored_command_parameter_rows': len(self.commands),
                'uniform_error_bound': str(self.error_bound), 'requested_error': str(self.epsilon),
                'all_rows_dyadic_and_stochastic': True, 'large_transition_table_stored': False,
                'scope': 'Certified integer-interval compiler; no claim that Python object overhead equals Turing-space constants.'}


if __name__ == '__main__':
    import argparse,json
    p=argparse.ArgumentParser();p.add_argument('--horizon',type=int,default=16);p.add_argument('--angles',type=int,default=2)
    p.add_argument('--epsilon',default='1/1000');a=p.parse_args()
    print(json.dumps(DyadicRotationMachine(a.horizon,a.angles,Fraction(a.epsilon)).certificate(),indent=2))
