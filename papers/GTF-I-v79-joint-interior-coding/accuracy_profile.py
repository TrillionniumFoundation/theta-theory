"""Exact rational sufficient width-exclusion certificates for the LPS experiment.

This checks Theorem blockbudget63, specialized to Frobenius error, using
eta_b=(b+2/3)^2/5^b.  A negative result is inconclusive, not a feasible
machine.  The imported full-action LPS theorem is a mathematical premise;
this program does not certify it by testing harmonics or word samples.

All decisions below use fractions and strict inequalities.  Logarithms are
bounded by an atanh series with an explicit rational remainder; sqrt(2)
is enclosed by integer arithmetic; pi<4 gives a conservative upper bound.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from math import isqrt
import json
from typing import Any


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def eta(block_length: int, q: int = 5) -> F:
    require(isinstance(block_length, int) and block_length >= 1, 'positive block length required')
    require(isinstance(q, int) and q >= 3 and q % 2 == 1, 'q must be odd and at least three')
    return (F(block_length) + F(q-1, q+1))**2 / q**block_length


def _unit_log(x: F, terms: int) -> tuple[F,F]:
    require(F(1) <= x <= F(2), 'internal logarithm range')
    z=(x-1)/(x+1)
    power=z
    lower=F(0)
    for j in range(terms):
        lower += 2*power/(2*j+1)
        power *= z*z
    remainder=2*power/((2*terms+1)*(1-z*z))
    return lower, lower+remainder


def log_interval(x: F, terms: int = 16) -> tuple[F,F]:
    """Return closed rational lower/upper bounds for log(x), x>0."""
    x=F(x)
    require(x>0, 'logarithm argument must be positive')
    require(isinstance(terms,int) and 1 <= terms <= 256, 'terms must be in 1..256')
    s=x.numerator.bit_length()-x.denominator.bit_length()
    scale=F(2**s) if s>=0 else F(1,2**(-s))
    y=x/scale
    if y<1:
        s-=1; y*=2
    elif y>=2:
        s+=1; y/=2
    lo,hi=_unit_log(y,terms)
    l2,h2=_unit_log(F(2),terms)
    if s>=0:
        return lo+s*l2,hi+s*h2
    return lo+s*h2,hi+s*l2


def sqrt2_upper(error: F) -> F:
    """Find a rational u>sqrt(2) with u*error<1 by integer arithmetic."""
    error=F(error)
    require(error>=0 and 2*error*error<1, 'Frobenius error must be in [0,1/sqrt(2))')
    bits=max(12,error.denominator.bit_length()+error.numerator.bit_length()+4)
    while True:
        scale=2**bits
        u=F(isqrt(2*scale*scale)+1,scale)
        if u*error<1:
            return u
        bits*=2


def certificate(horizon: int, width: int, error: F, block_length: int,
                terms: int = 16) -> dict[str,Any]:
    """An excluded=True result proves W_(horizon,error)>width, conditionally
    on the paper's LPS experiment and resource model."""
    require(isinstance(horizon,int) and horizon>=0, 'nonnegative horizon required')
    require(isinstance(width,int) and width>=1, 'positive width required')
    require(isinstance(block_length,int) and block_length>=4, 'block length at least four required')
    error=F(error)
    root=sqrt2_upper(error)
    M=horizon//block_length
    z=eta(block_length)
    require(z<=F(1,4), 'invalid block norm budget')
    dl,du=log_interval(2*z-z*z,terms)
    gl,gu=log_interval(3*width/z,terms)
    deficit_lower=-du
    gap_lower=M*deficit_lower-gu
    xi_upper=root*error/(1-root*error)
    # pi=4 integral_0^1 1/(1+t^2) dt <4; hence 18*pi^2 <288.
    cost_squared_upper=288*M*xi_upper*width/z
    excluded= M>0 and gap_lower>0 and gap_lower*gap_lower>cost_squared_upper
    return {
        'schema':'gtf63.width-exclusion/1','horizon':horizon,'width':width,
        'frobenius_error':str(error),'block_length':block_length,'blocks':M,
        'log_series_terms':terms,'eta':str(z),'sqrt2_upper':str(root),
        'deficit_lower':str(deficit_lower),'gap_lower':str(gap_lower),
        'transport_squared_upper':str(cost_squared_upper),'excluded':excluded,
        'conclusion':f'W>{width}' if excluded else 'inconclusive',
        'assumption':'fixed six-command rational LPS Bloch experiment; legal D2 decoders; full-action LPS theorem',
        'arithmetic':'exact rational enclosures and strict inequalities; no floating-point decision'
    }


def verify(record: dict[str,Any]) -> bool:
    """Reject altered witnesses rather than trusting stored booleans."""
    try:
        expected=certificate(record['horizon'],record['width'],F(record['frobenius_error']),
                             record['block_length'],record['log_series_terms'])
        return record==expected and expected['excluded']
    except (ValueError,TypeError,KeyError,ZeroDivisionError):
        return False


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--horizon',type=int,required=True)
    parser.add_argument('--width',type=int,required=True)
    parser.add_argument('--error',type=str,required=True,help='nonnegative rational Frobenius tolerance')
    parser.add_argument('--block-length',type=int,required=True)
    parser.add_argument('--terms',type=int,default=16)
    parser.add_argument('--output')
    args=parser.parse_args()
    try:
        record=certificate(args.horizon,args.width,F(args.error),args.block_length,args.terms)
    except (ValueError,ZeroDivisionError) as exc:
        parser.error(str(exc))
    text=json.dumps(record,indent=2,sort_keys=True)+'\n'
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(text,encoding='utf-8')
    print(text,end='')

if __name__=='__main__':
    main()
