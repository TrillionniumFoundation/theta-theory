#!/usr/bin/env python3
"""Exact finite regression for the integer streamer; not a proof of LPS.

Checks remain enabled under python -O. Ground truth uses rational
arithmetic, not floats. Long-word tests stream commands to the machine.
"""
from __future__ import annotations
import hashlib
import io
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
import random
import subprocess
import sys
from streaming import MATRICES, StreamState, matvec, run, toward_zero

ROOT = Path(__file__).resolve().parent
COUNT = 0
CASES = 0
NEGATIVE = []
MODES = {"exact": 0, "directed-grid": 0}


def require(value: bool, message: str) -> None:
    global COUNT
    COUNT += 1
    if not value:
        raise RuntimeError(message)


def rejects(name, fn):
    try:
        fn()
    except (ValueError, RuntimeError):
        NEGATIVE.append(name)
    else:
        raise RuntimeError("negative control was accepted: " + name)


def exact_error(state, exact_n, exact_d):
    return sum((F(a, state.denominator) - F(b, exact_d)) ** 2
               for a, b in zip(state.n, exact_n)) / 2


def check_word(word, N, L):
    global CASES
    s = StreamState.initialize(N, L)
    truth = (1, 0, 0)
    td = 1
    for letter in word:
        old = s.n
        z = matvec(letter, old)
        bound = s.precision + 4 if not s.exact else 3 * (s.count + 1) + 4
        require(max(abs(i).bit_length() for i in z) <= bound, "scratch bit bound")
        s.step(letter)
        truth = matvec(letter, truth)
        td *= 5
        require(sum(a*a for a in s.n) <= s.denominator**2, "legal unit ball")
        require(sum(a*a for a in truth) == td**2, "orthogonal ground truth")
        if s.exact:
            require(s.n == truth and s.denominator == td, "exact mode identity")
        else:
            err = exact_error(s, truth, td)
            require(err <= F(3 * s.count**2, 2 * (1 << (2 * s.precision))), "prefix rounding error")
    require(s.count == N, "test input length")
    if s.exact:
        require(exact_error(s, truth, td) == 0, "zero error exact branch")
    else:
        require(exact_error(s, truth, td) <= F(1, 1 << (2 * L)), "requested endpoint precision")
    out = s.finish()
    require(int(out["density_common_denominator_hex"], 16) == 2 * s.denominator, "output denominator")
    require(s.precision == 0 or s.precision < N, "mode selection")
    CASES += 1
    MODES[out["mode"]] += 1
    return s


def main():
    # Tie the source constants to the inherited finite experimental input.
    raw = json.loads((ROOT / 'NO_IDLE_INPUT.json').read_text())
    names = dict(zip('xXyYzZ', ['A1','A1*','A2','A2*','A3','A3*']))
    for letter, M in MATRICES.items():
        for i in range(3):
            for j in range(3):
                require(F(M[i][j],5) == F(raw['commands'][names[letter]][i][j]), "input identity")
                require(sum(M[k][i]*M[k][j] for k in range(3)) == (25 if i==j else 0), "M^t M = 25 I")
    # Exhaustive exact words (all six letters) and inverse conventions.
    for n in range(2, 6):
        for w in itertools.product('xXyYzZ', repeat=n):
            check_word(iter(w), n, 2)
    rng = random.Random(20260928)
    # Approximate branch and precision transitions; word is generated online.
    for n in [12, 16, 32, 64, 128, 256]:
        for L in [2, 3, 4, 8, 16, 64]:
            for j in range(4):
                check_word((rng.choice('xXyYzZ') for _ in range(n)), n, L)
    for letter in 'xXyYzZ':
        for n in [16, 64, 128]:
            check_word(itertools.repeat(letter,n),n,2)
    # Rational-seed / denominator extension: tests the upper rounding lemma only.
    # Circle rotations do NOT have the full spectral premise of the corollary.
    for D, M in [(5, ((3,-4),(4,3))), (13, ((5,-12),(12,5)))]:
        for nsteps in [8, 32, 96]:
            L=6
            b=L+nsteps.bit_length()+3
            d=1<<b
            v=(toward_zero(3*d,5), toward_zero(4*d,5))
            target=(F(3,5), F(4,5))
            for t in range(nsteps):
                v=tuple(toward_zero(sum(row[j]*v[j] for j in range(2)),D) for row in M)
                target=tuple(sum(F(row[j],D)*target[j] for j in range(2)) for row in M)
                require(sum(a*a for a in v)<=d*d, 'rational-seed ball invariant')
                sq=sum((F(a,d)-x)**2 for a,x in zip(v,target))
                require(sq<=F(2*(t+2)**2,d*d), 'initial rounding error included')
            require(sq<=F(1,1<<(2*L)), 'rational-seed endpoint error')
    # Huge requested L is scanned with saturation, not converted into a giant int.
    s = run(io.BytesIO(b'8\n' + b'9'*100000 + b'\nxXyYzZxx\n'))
    require(s.exact and s.count == 8, 'capped precision header')
    require(s.denominator == 5**8, 'capped header exact denominator')
    # Integer truncation identity, including all signed residues modulo five.
    for n in range(-101, 102):
        a = toward_zero(n)
        require(abs(5*a) <= abs(n), 'directed absolute contraction')
        require(abs(n-5*a) <= 4, 'directed residual')
        require(a*n >= 0, 'directed sign')
    # A nearest-grid or floor implementation can leave the ball: pin a witness.
    z = matvec('y', (2,0,0))
    bad_floor = tuple(a//5 for a in z)
    bad_nearest = tuple((1 if a>=0 else -1)*((abs(a)+2)//5) for a in z)
    require(sum(a*a for a in bad_floor) > 4, 'floor update leaves unit ball')
    require(sum(a*a for a in bad_nearest) > 4, 'nearest update leaves unit ball')
    NEGATIVE.extend(['negative-floor-rounding-leaves-ball', 'nearest-rounding-leaves-ball'])
    for name, data in [
        ('empty-header',b'\n2\nxx'), ('signed-precision',b'8\n-2\nxxxxxxxx'),
        ('precision-below-two',b'8\n1\nxxxxxxxx'), ('horizon-below-two',b'1\n2\nx'),
        ('too-few-commands',b'8\n2\nxx'), ('too-many-commands',b'2\n2\nxxx'),
        ('identity-command-not-allowed',b'2\n2\nxI'), ('invalid-command',b'2\n2\nx?'),
        ('invalid-header-character',b'2a\n2\nxx'), ('missing-header-newline',b'2\n2'),
        ('unicode-command',b'2\n2\nx\xff')]:
        rejects(name, lambda data=data: run(io.BytesIO(data)))
    rejects('invalid-divisor', lambda: toward_zero(1,0))
    # CLI subprocess exercises the real stdin route and output encoding.
    payload=b'32\n2\n'+b'xyXZ'*8+b'\n'
    cli=subprocess.run([sys.executable,str(ROOT/'streaming.py')],input=payload,capture_output=True,check=True)
    obj=json.loads(cli.stdout)
    require(obj['mode']=='directed-grid', 'CLI approximate mode')
    bad=subprocess.run([sys.executable,str(ROOT/'streaming.py')],input=b'2\n2\nxI\n',capture_output=True)
    require(bad.returncode==2, 'CLI rejects invalid letter')
    receipt={
        'schema':'gtf64.regression/1','status':'success','exact_assertions':COUNT,
        'word_cases':CASES,'modes':MODES,'negative_controls':NEGATIVE,
        'cli_example_sha256':hashlib.sha256(cli.stdout).hexdigest(),
        'uses_floating_point_oracle':False,
        'scope':'Exact finite regression of the reference recurrences, parser, legal output and error bounds. Does not prove the universal entropy theorem, full LPS spectrum, or novelty.',
    }
    print(json.dumps(receipt,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
