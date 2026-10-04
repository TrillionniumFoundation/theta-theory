#!/usr/bin/env python3
"""Rational instrument compilation and variable-description numerical streaming.

Input-first UNNORMALIZED Choi matrices are used. No rational Kraus factorization
or floating-point decision is used. Compilation produces mathematical channels,
not a classical physical device for an unknown quantum input. The streaming CLI
simulates specified numerical states; its OS bits implement the recurrence, not
a certification of ideal fair randomness or literal interpreter heap space.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
import os
from pathlib import Path
import sys
from typing import Callable
from instrument_streaming import (G, Matrix, ZERO, add, mul, conj, zero, identity,
                                 adjoint, plus, trace, toward_zero, round_density,
                                 uniform_below, decode_matrix, read_decimal_line)

F = Fraction

def rational_psd(a: Matrix) -> bool:
    """Reduced rational Schur complements; polynomial operand lengths in input.

    Unlike the inherited fixed-dimensional scaled recursion, rational fractions
    are reduced after each arithmetic operation. The remaining entries are ratios
    of minors. Zero pivots require a zero row. Hermitian input is mandatory.
    """
    if not a or a != adjoint(a):
        return False
    b = [[(F(x), F(y)) for x, y in row] for row in a]
    while b:
        t = b[0][0][0]
        if b[0][0][1] or t < 0:
            return False
        if t == 0:
            if any(x != 0 or y != 0 for x, y in b[0]):
                return False
            b = [row[1:] for row in b[1:]]
            continue
        c = []
        for i in range(1, len(b)):
            row = []
            for j in range(1, len(b)):
                u = mul(b[i][0], b[0][j])
                row.append((b[i][j][0] - u[0]/t, b[i][j][1] - u[1]/t))
            c.append(row)
        b = c
    return True

def partial_trace(a: Matrix, d: int, n: int) -> Matrix:
    if len(a) != d*n:
        raise ValueError('wrong Choi dimension')
    r = zero(d)
    for i in range(d):
        for j in range(d):
            for alpha in range(n):
                r[i][j] = add(r[i][j], a[i*n+alpha][j*n+alpha])
    return r

def constants(d: int, n: int, m: int) -> tuple[int, int]:
    if any(type(x) is not int or x < 1 for x in (d,n,m)):
        raise ValueError('positive integral dimensions and outcome count required')
    c = 2*n*d*(1+m*n)
    return c, 3*m*n*d*c

@dataclass
class Instrument:
    d: int
    n: int
    denominator: int
    outcomes: list[Matrix]

    @classmethod
    def from_dict(cls, raw: dict) -> 'Instrument':
        if not isinstance(raw, dict):
            raise ValueError('instrument must be an object')
        if raw.get('convention','input-first-unnormalized') != 'input-first-unnormalized':
            raise ValueError('unsupported Choi tensor convention')
        d, n, den = (raw.get(k) for k in ('input_dimension','output_dimension','denominator'))
        constants(d,n,1)
        if type(den) is not int or den < 1:
            raise ValueError('positive integral denominator required')
        ys = raw.get('outcomes')
        if not isinstance(ys, list) or not ys:
            raise ValueError('nonempty Choi outcome list required')
        mats = [decode_matrix(y,d*n) for y in ys]
        obj = cls(d,n,den,mats)
        obj.validate()
        return obj

    def validate(self) -> None:
        constants(self.d,self.n,len(self.outcomes))
        if type(self.denominator) is not int or self.denominator < 1:
            raise ValueError('invalid denominator')
        total = zero(self.d)
        for mat in self.outcomes:
            if len(mat) != self.d*self.n or not rational_psd(mat):
                raise ValueError('Choi numerator is not positive Hermitian')
            total = plus(total,partial_trace(mat,self.d,self.n))
        if total != identity(self.d,self.denominator):
            raise ValueError('Choi partial-trace identity failed')

    def to_dict(self) -> dict:
        return {'schema':'gtf66.choi-instrument/1','convention':'input-first-unnormalized',
                'input_dimension':self.d,'output_dimension':self.n,
                'denominator':self.denominator,
                'outcomes':[[[[x,y] for x,y in row] for row in mat] for mat in self.outcomes]}

    def branch(self, p: Matrix, y: int) -> Matrix:
        if len(p) != self.d or not 0 <= y < len(self.outcomes):
            raise ValueError('wrong state or outcome dimension')
        c, n = self.outcomes[y], self.n
        ans = zero(n)
        for alpha in range(n):
            for beta in range(n):
                for i in range(self.d):
                    for j in range(self.d):
                        ans[alpha][beta] = add(ans[alpha][beta],
                            mul(c[i*n+alpha][j*n+beta],p[i][j]))
        return ans


def repair_grid(grid: list[Matrix], d: int, n: int, B: int) -> Instrument:
    """Repair integer numerators of Hermitian 1/B Choi estimates.

    The norm theorem additionally REQUIRES coordinate error <=1/B to a valid
    target. This function tests legality but does not invent that input promise.
    Public compile_exact below supplies the promise by exact directed division.
    """
    c,_ = constants(d,n,len(grid))
    if type(B) is not int or B < 1:
        raise ValueError('positive integer grid required')
    if any(len(t) != d*n or t != adjoint(t) for t in grid):
        raise ValueError('grid matrices must be Hermitian of the declared size')
    residual = identity(d,B)
    for t in grid:
        x = partial_trace(t,d,n)
        residual = [[(a[0]-b[0],a[1]-b[1]) for a,b in zip(ar,br)]
                    for ar,br in zip(residual,x)]
    mats = [[row[:] for row in t] for t in grid]
    for i in range(d):
        for j in range(d):
            mats[0][i*n][j*n] = add(mats[0][i*n][j*n],residual[i][j])
    for t in mats:
        for i in range(d*n):
            t[i][i] = add(t[i][i],(c,0))
    obj = Instrument(d,n,B+len(grid)*n*c,mats)
    obj.validate()
    return obj


def compile_exact(target: Instrument, B: int) -> dict:
    target.validate()
    if type(B) is not int or B < 1:
        raise ValueError('positive grid required')
    grid = [[[(toward_zero(B*x,target.denominator),toward_zero(B*y,target.denominator))
               for x,y in row] for row in t] for t in target.outcomes]
    obj = repair_grid(grid,target.d,target.n,B)
    c,K = constants(target.d,target.n,len(grid))
    return {'schema':'gtf66.compilation/1','grid':B,
            'diamond_error_upper':str(F(K,obj.denominator)),
            'convention':'input-first-unnormalized',
            'scope':'Certified rational instrument description; not physical classical preparation.',
            'instrument':obj.to_dict()}


def verify_compilation(target: Instrument, certificate: dict) -> bool:
    """Recompute exact output; reject tampered bounds, normalization and blocks."""
    try:
        expected = compile_exact(target,certificate['grid'])
        # JSON normalizes Gaussian tuples to the canonical list representation.
        return json.dumps(expected,sort_keys=True) == json.dumps(certificate,sort_keys=True)
    except (ValueError,TypeError,KeyError,IndexError):
        return False

@dataclass
class Description:
    d: int
    initial: Matrix
    commands: dict[str,Instrument]

    @classmethod
    def from_dict(cls, raw: dict) -> 'Description':
        if not isinstance(raw,dict):
            raise ValueError('description must be an object')
        d = raw.get('dimension')
        if type(d) is not int or d < 2:
            raise ValueError('dimension must be an integer at least two')
        p = decode_matrix(raw['initial_numerator'],d)
        if not rational_psd(p) or trace(p) <= 0:
            raise ValueError('positive nonzero initial numerator required')
        supplied = raw.get('commands')
        if not isinstance(supplied,dict) or not supplied:
            raise ValueError('nonempty command object required')
        commands = {}
        for a, value in supplied.items():
            if not isinstance(a,str) or not a or not a.isascii() or any(x.isspace() for x in a):
                raise ValueError('nonempty nonspace ASCII command identifier required')
            obj = Instrument.from_dict(value)
            if obj.d!=d or obj.n!=d:
                raise ValueError('streaming commands must have the same declared dimension')
            commands[a]=obj
        return cls(d,p,commands)

    @property
    def H(self) -> int:
        return max(x.denominator.bit_length() for x in self.commands.values())

    def exact_cap(self,N:int) -> int:
        return trace(self.initial).bit_length()+N*self.H

class ChoiStreamer:
    def __init__(self, spec: Description, N: int, L: int):
        if type(N) is not int or N<2 or type(L) is not int or L<2:
            raise ValueError('N,L must be integral and at least two')
        self.spec,self.N,self.t=spec,N,0
        Q=spec.exact_cap(N)
        b=min(L,Q)+(6*spec.d*spec.d*(N+1)-1).bit_length()
        self.B=None if Q<=b else 1<<b
        self.mode='exact' if self.B is None else 'positive-grid'
        self.p=[row[:] for row in spec.initial] if self.B is None else round_density(spec.initial,self.B)

    def step(self, a: str, bit: Callable[[],int]) -> int:
        if self.t>=self.N:
            raise ValueError('too many commands')
        if a not in self.spec.commands:
            raise ValueError('unknown command: '+repr(a))
        inst=self.spec.commands[a]
        expected=inst.denominator*trace(self.p)
        total,positive,last=0,0,-1
        # No list of all branch numerators or masses is retained.
        for y in range(len(inst.outcomes)):
            w=trace(inst.branch(self.p,y))
            if w<0:
                raise RuntimeError('negative mass')
            total+=w
            if w:
                positive+=1;last=y
        if total!=expected or total<1:
            raise RuntimeError('exact instrument mass invariant failed')
        j=0 if positive==1 else uniform_below(total,bit)
        chosen=None;outcome=-1
        if positive==1:
            outcome=last;chosen=inst.branch(self.p,last)
        else:
            for y in range(len(inst.outcomes)):
                candidate=inst.branch(self.p,y)
                w=trace(candidate)
                if j<w:
                    outcome=y;chosen=candidate;break
                j-=w
        if chosen is None:
            raise RuntimeError('unreachable interval end')
        self.p=chosen if self.B is None else round_density(chosen,self.B)
        self.t+=1
        return outcome

    def finish(self) -> dict:
        if self.t!=self.N:
            raise ValueError('too few commands')
        return {'kind':'numerical-density-matrix','mode':self.mode,'dimension':self.spec.d,
                'denominator_hex':hex(trace(self.p)),
                'numerator_hex':[[[hex(x),hex(y)] for x,y in row] for row in self.p]}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='action',required=True)
    c=sub.add_parser('compile');c.add_argument('--input',type=Path,required=True)
    c.add_argument('--grid',type=int,required=True)
    s=sub.add_parser('stream');s.add_argument('--input',type=Path,required=True)
    s.add_argument('--tokens',action='store_true',help='whitespace-delimited arbitrary command identifiers')
    args=parser.parse_args()
    try:
        raw=json.loads(args.input.read_text())
        if args.action=='compile':
            obj=Instrument.from_dict(raw)
            print(json.dumps(compile_exact(obj,args.grid),sort_keys=True,indent=2))
            return 0
        spec=Description.from_dict(raw)
        N=read_decimal_line(sys.stdin.buffer)
        if N<2:raise ValueError('horizon below two')
        L=read_decimal_line(sys.stdin.buffer,spec.exact_cap(N))
        sim=ChoiStreamer(spec,N,L)
        def os_bit():return os.urandom(1)[0]&1
        def emit(a):
            print(json.dumps({'outcome':sim.step(a,os_bit)}),flush=True)
        if args.tokens:
            token=bytearray();limit=max(map(len,spec.commands))
            while True:
                x=sys.stdin.buffer.read(1)
                if not x or x.isspace():
                    if token:emit(token.decode('ascii'));token.clear()
                    if not x:break
                else:
                    if x[0]>=128 or len(token)>=limit:raise ValueError('invalid command token')
                    token.extend(x)
        else:
            while True:
                x=sys.stdin.buffer.read(1)
                if not x:break
                if x in b' \t\r\n':continue
                if x[0]>=128:raise ValueError('non-ASCII command')
                emit(x.decode('ascii'))
        print(json.dumps(sim.finish(),sort_keys=True))
        return 0
    except (ValueError,TypeError,KeyError,IndexError,OSError,json.JSONDecodeError) as e:
        print('error: '+str(e),file=sys.stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
