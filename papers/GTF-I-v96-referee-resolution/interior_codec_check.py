#!/usr/bin/env python3
"""Finite exact checks only; no continuum entropy or minimax proof is inferred."""
from __future__ import annotations
from fractions import Fraction
from itertools import product
import json
import sympy as sp
import interior_codec as ic
import matrix_metric as mm


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def must_fail(fn):
    try:
        fn()
    except (ValueError, TypeError):
        return
    raise RuntimeError('negative control unexpectedly accepted')


def main():
    checks = []
    for N in [1, 2, 3, 4, 7, 8, 9, 16, 17, 10**30+1]:
        k = ic.ceil_sqrt(N)
        require((k-1)**2 < N <= k*k <= 4*N, 'integer horizon rounding')
        for d in [1, 2, 3, 17]:
            K, t = ic.parameters(d, N, sp.Rational(1, 37))
            require(sp.Rational(2*d, K) <= sp.Rational(1, 37)/(64*k), 'rounding ledger')
            require(t == sp.Rational(1, 37)/(16*k), 'greedy radius')
    checks.append('integer-horizon-and-rounding-budgets')
    X = sp.ImmutableMatrix([[0, sp.Rational(1, 4)], [sp.Rational(1, 4), 0]])
    Y = sp.ImmutableMatrix([[0, sp.I/4], [-sp.I/4, 0]])
    require(ic.op_leq(X, sp.Rational(1, 4)) and ic.op_leq(Y, sp.Rational(1, 4)), 'equality PSD')
    require(not ic.op_leq(X, sp.Rational(1, 5)), 'strict rejection')
    require(ic.op_leq(sp.zeros(3), sp.Rational(0)), 'zero pivot')
    indefinite = sp.ImmutableMatrix([[sp.Rational(1, 2), 0, sp.Rational(2, 5)],
                                     [0, sp.Rational(1, 2), sp.Rational(2, 5)],
                                     [sp.Rational(2, 5), sp.Rational(2, 5), sp.Rational(1, 2)]])
    require(not ic.op_leq(indefinite-sp.eye(3)/2, sp.Rational(1, 2)), 'full PSD versus minor prefilter')
    checks.append('exact-equality-singular-and-full-PSD-tests')
    candidates = [sp.ImmutableMatrix([[sp.Rational(1, 4)]]),
                  sp.ImmutableMatrix([[sp.Rational(3, 8)]]),
                  sp.ImmutableMatrix([[sp.Rational(1, 2)]])]
    cs, count = ic.greedy(candidates, sp.Rational(1, 8))
    require(len(cs) == 2 and count == 3, 'equality must not retain centre')
    must_fail(lambda: ic.greedy(candidates, sp.Rational(1, 8), max_candidates=1))
    must_fail(lambda: ic.construct(1, 1, '1', max_candidates=2))
    checks.append('strict-greedy-and-incomplete-construction')
    books = []
    for delta in ['1', '1/2']:
        book = ic.construct(1, 1, delta, max_candidates=1000)
        replay = ic.construct(1, 1, delta, max_candidates=1000)
        require(book == replay, 'public reconstruction differs')
        for q in [sp.Rational(1, 4), sp.Rational(1, 3), sp.Rational(1, 2),
                  sp.Rational(2, 3), sp.Rational(3, 4)]:
            E = sp.ImmutableMatrix([[q]])
            code = ic.encode(E, book)
            C = ic.decode_with_book(code, book)
            require(2*abs(q-C[0, 0]) <= 5*book.accuracy/16, 'scalar exact unhalved error')
        for bits in product('01', repeat=book.payload_bits):
            raw = {'schema': ic.CODE, 'dimension': 1, 'horizon': 1,
                   'accuracy': delta, 'payload': ''.join(bits)}
            C = ic.decode_with_book(raw, book)
            ic.interior(C, expanded=True)
        malformed = dict(raw, payload='2'*book.payload_bits)
        must_fail(lambda: ic.decode_with_book(malformed, book))
        must_fail(lambda: ic.decode_with_book(dict(raw, extra='uncharged advice'), book))
        books.append(ic.summary(book))
    checks.append('two-complete-scalar-dictionaries-replay-all-words-and-error')
    for d in [2, 3]:
        observed = list(ic.grid(d, 2))
        require(len(observed) == 1 and observed[0] == sp.eye(d)/2, 'small complete inner grid')
        E = sp.ImmutableMatrix(sp.eye(d)/2 + sp.diag(*([sp.Rational(1, 7)]+[0]*(d-1))))
        G = ic.quantize(E, 128*d)
        require(ic.op_leq(G-E, sp.Rational(1, 128)), 'multidimensional rational rounding')
    checks.append('complete-small-matrix-grids-not-theorem-scale-dictionaries')
    for eta in [Fraction(0), Fraction(1, 8)]:
        for B in [0, 1, 7, 101]:
            expected_length = (1-eta)*B
            require(expected_length+eta*B == B, 'public-erasure length identity')
    checks.append('public-abort-resource-identity-only-not-Fano-proof')
    for bad in [0, -1, True, 1.2]:
        must_fail(lambda bad=bad: ic.ceil_sqrt(bad))
    must_fail(lambda: ic.parameters(2, 1, '0'))
    must_fail(lambda: ic.parameters(2, 1, '3/2'))
    must_fail(lambda: ic.interior(sp.zeros(2)))
    print(json.dumps({'schema': 'gtf79.interior-regression/1', 'status': 'success',
                      'checks': checks, 'complete_scalar_dictionaries': books,
                      'theorem_scale_matrix_dictionary_executed': False,
                      'unknown_device_learning_executed': False,
                      'continuum_entropy_or_minimax_proved_by_tests': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
