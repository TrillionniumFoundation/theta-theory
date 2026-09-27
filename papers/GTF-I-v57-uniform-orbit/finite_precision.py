"""Exact rational-to-dyadic row compiler and integer sampler.

Input JSON: {"rows": [["1/3", "2/3"], ...]}. Each compiled row consists of
integer masses with common denominator 2**bits. The script does not solve
for a realization; it compiles already supplied exact rational rows.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
from pathlib import Path
from typing import Sequence


def round_row(row: Sequence[Fraction], bits: int) -> tuple[int,...]:
    if type(bits) is not int or bits<0:raise ValueError('bits must be a nonnegative integer')
    if not row or any(x<0 for x in row) or sum(row)!=1:raise ValueError('Illegal probability row')
    q=1<<bits;values=[(x.numerator*q)//x.denominator for x in row[:-1]]
    return tuple(values+[q-sum(values)])


def sample_integer(masses: Sequence[int], random_integer: int) -> int:
    if not masses or any(type(x) is not int or x<0 for x in masses):raise ValueError('Illegal integer row')
    total=sum(masses)
    if total<1 or total&(total-1):raise ValueError('Denominator is not a positive power of two')
    if type(random_integer) is not int or not 0<=random_integer<total:raise ValueError('Random integer outside range')
    cumulative=0
    for i,mass in enumerate(masses):
        cumulative+=mass
        if random_integer<cumulative:return i
    raise RuntimeError('Inconsistent cumulative sum')


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('output',type=Path);parser.add_argument('--bits',required=True,type=int)
    args=parser.parse_args();data=json.loads(args.input.read_text())
    rows=[]
    for row in data['rows']:
        if any(isinstance(x,(float,bool)) for x in row):raise ValueError('Use exact rational strings or integers')
        rows.append(round_row([Fraction(x) for x in row],args.bits))
    args.output.write_text(json.dumps({'denominator':1<<args.bits,'integer_rows':rows},indent=2)+'\n')
    print(json.dumps({'status':'success','rows':len(rows),'bits_per_draw':args.bits,'scope':'compilation of supplied rational rows only'}))

if __name__=='__main__':main()
