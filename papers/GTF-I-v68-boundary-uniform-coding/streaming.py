#!/usr/bin/env python3
"""Reference integer streamer for Theorem streamspace64.

Input on stdin: decimal N, newline, decimal L, newline, then exactly N
letters from xXyYzZ (ASCII whitespace between commands is ignored).
L is parsed with saturation at N. The word and an uncapped L are never
retained. Output is a rational legal Bloch density matrix in common-
denominator form, encoded using hexadecimal strings to avoid costly
large-integer decimal conversion. No third-party packages are required.

The theorem accounts for binary integer storage and elementary bit
operations. Python interpreter/allocator and I/O buffers are not a
literal optimal-space machine; the reference executes the same integer
recurrence. Test instrumentation is deliberately outside the core.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import BinaryIO, Iterable

MATRICES: dict[str, tuple[tuple[int, int, int], ...]] = {
    "x": ((5, 0, 0), (0, -3, -4), (0, 4, -3)),
    "X": ((5, 0, 0), (0, -3, 4), (0, -4, -3)),
    "y": ((-3, 0, 4), (0, 5, 0), (-4, 0, -3)),
    "Y": ((-3, 0, -4), (0, 5, 0), (4, 0, -3)),
    "z": ((-3, -4, 0), (4, -3, 0), (0, 0, 5)),
    "Z": ((-3, 4, 0), (-4, -3, 0), (0, 0, 5)),
}


def toward_zero(n: int, divisor: int = 5) -> int:
    """Integer-only truncation. Python // on negative n is NOT this rule."""
    if divisor <= 0:
        raise ValueError("divisor must be positive")
    return n // divisor if n >= 0 else -((-n) // divisor)


def matvec(letter: str, n: tuple[int, int, int]) -> tuple[int, int, int]:
    try:
        m = MATRICES[letter]
    except KeyError as exc:
        raise ValueError("command must be one of xXyYzZ") from exc
    # A fixed three-by-three product: no input-size table is constructed.
    return tuple(sum(row[j] * n[j] for j in range(3)) for row in m)  # type: ignore[return-value]


@dataclass(slots=True)
class StreamState:
    horizon: int
    exact: bool
    precision: int  # zero in exact mode; b otherwise
    count: int
    n: tuple[int, int, int]
    denominator: int

    @classmethod
    def initialize(cls, horizon: int, capped_l: int) -> "StreamState":
        if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 2:
            raise ValueError("horizon must be an integer at least two")
        if isinstance(capped_l, bool) or not isinstance(capped_l, int) or capped_l < 2:
            raise ValueError("precision parameter must be an integer at least two")
        # Saturation also makes the programmatic entry robust to large L.
        capped_l = min(capped_l, horizon)
        b = capped_l + (horizon - 1).bit_length() + 2
        if b >= horizon:
            return cls(horizon, True, 0, 0, (1, 0, 0), 1)
        d = 1 << b
        return cls(horizon, False, b, 0, (d, 0, 0), d)

    def step(self, letter: str) -> None:
        if self.count >= self.horizon:
            raise ValueError("more commands than the declared horizon")
        z = matvec(letter, self.n)
        if self.exact:
            self.n = z
            self.denominator *= 5
        else:
            self.n = tuple(toward_zero(v) for v in z)  # type: ignore[assignment]
        self.count += 1

    def finish(self) -> dict:
        if self.count != self.horizon:
            raise ValueError("fewer commands than the declared horizon")
        x, y, z = self.n
        d = self.denominator
        # No eigenvalue test is needed in the core; legality is an invariant.
        return {
            "schema": "gtf64.integer-stream/1",
            "mode": "exact" if self.exact else "directed-grid",
            "horizon_hex": hex(self.horizon),
            "commands_read_hex": hex(self.count),
            "grid_precision_bits": self.precision,
            "bloch_numerator_hex": [hex(x), hex(y), hex(z)],
            "bloch_denominator_hex": hex(d),
            "density_common_denominator_hex": hex(2 * d),
            "density_numerators_hex": [
                [[hex(d + z), "0x0"], [hex(x), hex(-y)]],
                [[hex(x), hex(y)], [hex(d - z), "0x0"]],
            ],
            "density_entry_encoding": "[real_numerator, imaginary_numerator] over common denominator",
            "guarantee": "exact in exact mode; otherwise Frobenius error below 2^(-requested L)",
        }


def read_decimal_line(stream: BinaryIO, *, cap: int | None = None) -> int:
    """Read one nonnegative ASCII integer without buffering the entire line."""
    n = 0
    seen = False
    while True:
        c = stream.read(1)
        if c == b"\n":
            if not seen:
                raise ValueError("empty parameter line")
            return n
        if c == b"":
            raise ValueError("parameter line must end with newline")
        if not b"0" <= c <= b"9":
            raise ValueError("parameter lines contain decimal digits only")
        seen = True
        if cap is None or n < cap:
            n = n * 10 + c[0] - 48
            if cap is not None:
                n = min(n, cap)


def run(stream: BinaryIO) -> StreamState:
    horizon = read_decimal_line(stream)
    if horizon < 2:
        raise ValueError("horizon must be at least two")
    capped_l = read_decimal_line(stream, cap=horizon)
    state = StreamState.initialize(horizon, capped_l)
    while True:
        c = stream.read(1)
        if c == b"":
            break
        if c in (b" ", b"\t", b"\r", b"\n"):
            continue
        if len(c) != 1 or c[0] > 127:
            raise ValueError("commands must be ASCII xXyYzZ")
        state.step(c.decode("ascii"))
    if state.count != state.horizon:
        raise ValueError("command count does not match the declared horizon")
    return state


def main() -> int:
    try:
        state = run(sys.stdin.buffer)
        json.dump(state.finish(), sys.stdout, sort_keys=True, indent=2)
        sys.stdout.write("\n")
        return 0
    except (ValueError, OverflowError) as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
