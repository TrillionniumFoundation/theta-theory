#!/usr/bin/env python3
"""Exact rank-aware description code for input-erasing preparation instruments.

Given rational Choi data I_d tensor sigma_y, encode triangular factors without
representing their irrational square roots. This is a mathematical instrument
code, not a physical classical simulator or a mutable-workspace optimum.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from math import isqrt
import json
from pathlib import Path
import sys
from typing import Iterator
from choi_streaming import Instrument
from instrument_streaming import ZERO, zero, add, mul, conj, product, adjoint, trace
from instrument_codec import pack_digits, unpack_digits

SCHEMA = 'gtf68.preparation-code/1'
ADAPTIVE_SCHEMA = 'gtf68.adaptive-preparation-code/1'


def positive(x: object, name: str) -> int:
    if type(x) is not int or x < 1:
        raise ValueError(name+' must be a positive integer')
    return x


def ranks_check(ranks: object, n: int, m: int) -> list[int]:
    if not isinstance(ranks,list) or len(ranks) != m:
        raise ValueError('one rank bound per outcome is required')
    if any(type(r) is not int or not 0 <= r <= n for r in ranks) or not any(ranks):
        raise ValueError('invalid or all-zero rank bounds')
    return ranks


def rank_dimension(n: int, ranks: list[int]) -> int:
    positive(n,'output dimension'); ranks_check(ranks,n,len(ranks))
    return sum(r*(2*n-r) for r in ranks)-1


def preparation_blocks(target: Instrument) -> list:
    target.validate()
    n,d=target.n,target.d
    blocks=[]
    for mat in target.outcomes:
        block=[row[:n] for row in mat[:n]]
        for i in range(d):
            for j in range(d):
                for a in range(n):
                    for b in range(n):
                        if mat[i*n+a][j*n+b] != (block[a][b] if i==j else ZERO):
                            raise ValueError('target is not an input-erasing preparation instrument')
        blocks.append(block)
    return blocks


def lift_blocks(blocks: list, d: int, n: int, denominator: int) -> Instrument:
    positive(d,'input dimension');positive(n,'output dimension')
    mats=[]
    for block in blocks:
        mat=zero(d*n)
        for i in range(d):
            for a in range(n):
                for b in range(n):mat[i*n+a][i*n+b]=block[a][b]
        mats.append(mat)
    ans=Instrument(d,n,denominator,mats);ans.validate();return ans


def factor_coordinates(n: int, pivots: list[list[int]]) -> Iterator[tuple[int,int,int,int]]:
    """Outcome,row,column,real/imaginary, in lower-triangular factor order."""
    for y,positions in enumerate(pivots):
        for j in positions:
            for i in range(j,n):
                for component in range(1 if i==j else 2):yield y,i,j,component


def triangular_data(blocks: list, denominator: int) -> tuple[list[list[int]],list[tuple[int,Fraction]]]:
    """Return positive pivot sets and (sign, squared coordinate), all exact.

    Each real Cholesky coordinate is a signed square root of the returned
    Fraction; no such root is computed. Zero residual pivots contribute no column.
    """
    positive(denominator,'denominator')
    pivots=[]; data=[]
    for block in blocks:
        n=len(block)
        if not n or any(len(row)!=n for row in block) or block!=adjoint(block):
            raise ValueError('nonempty Hermitian square blocks required')
        A=[[(Fraction(x,denominator),Fraction(y,denominator)) for x,y in row] for row in block]
        ys=[]
        for j in range(n):
            pivot=A[j][j][0]
            if A[j][j][1] or pivot < 0:raise ValueError('nonpositive Schur residual')
            if not pivot:
                if any(A[j][i]!=ZERO or A[i][j]!=ZERO for i in range(j,n)):
                    raise ValueError('zero pivot with nonzero residual row')
                continue
            ys.append(j)
            data.append((1,pivot))
            for i in range(j+1,n):
                for component in A[i][j]:
                    data.append(((component>0)-(component<0),component*component/pivot))
            for i in range(j+1,n):
                for k in range(j+1,n):
                    u=mul(A[i][j],conj(A[k][j]))
                    A[i][k]=(A[i][k][0]-u[0]/pivot,A[i][k][1]-u[1]/pivot)
        pivots.append(ys)
    if sum(q for _,q in data) != 1:
        raise ValueError('factor norm is not one; preparation trace must be one')
    return pivots,data


def sqrt_floor(q: Fraction) -> int:
    if not isinstance(q,Fraction) or q<0:raise ValueError('nonnegative rational square required')
    return isqrt(q.numerator//q.denominator)


def body_capacity(B: int, h: int) -> int:
    return 2*h*(2*B+1)**(h-1)


def description_bits(n: int,m: int,ranks: list[int],B:int) -> int:
    v=rank_dimension(n,ranks);D=v+1
    return 0 if not v else m*n+(body_capacity(B,D)-1).bit_length()


def encode(target: Instrument, B: int, ranks: list[int] | None=None) -> dict:
    positive(B,'grid')
    blocks=preparation_blocks(target);m=len(blocks);n=target.n
    ranks=[n]*m if ranks is None else ranks_check(ranks,n,m)
    pivots,data=triangular_data(blocks,target.denominator)
    if any(len(p)>r for p,r in zip(pivots,ranks)):raise ValueError('target exceeds a declared rank bound')
    h=len(data);v=rank_dimension(n,ranks)
    if not 1 <= h <= v+1:raise RuntimeError('internal factor dimension mismatch')
    anchor=max(range(h),key=lambda i:data[i][1])
    sign,den=data[anchor]
    if den<=0 or sign not in (-1,1):raise RuntimeError('zero anchor')
    z=[s*sqrt_floor(B*B*q/den) for s,q in data]
    if z[anchor]!=sign*B:raise RuntimeError('anchor grid mismatch')
    digits=z[:anchor]+z[anchor+1:]
    packed=(2*anchor+int(sign<0))*(2*B+1)**(h-1)+pack_digits(digits,B)
    ans={'schema':SCHEMA,'convention':'input-first-unnormalized',
         'input_dimension':target.d,'output_dimension':n,'outcome_count':m,
         'rank_bounds':ranks,'pivot_sets':pivots,'grid':B,
         'factor_coordinates':h,'rank_family_dimension':v,
         'body_hex':format(packed,'x'),
         'fixed_length_bits':description_bits(n,m,ranks,B),
         'one_use_error_squared_upper':str(Fraction(16*(h-1),B*B)),
         'scope':'Target-bound mathematical preparation code; dimensions, grid and rank bounds are public parameters. Pivot masks and a fixed-length body are charged; expanded matrices and encoder workspace are separate.'}
    decode(ans)
    return ans


def decode(raw: dict) -> Instrument:
    if not isinstance(raw,dict) or raw.get('schema')!=SCHEMA:raise ValueError('invalid preparation-code schema')
    if raw.get('convention')!='input-first-unnormalized':raise ValueError('unsupported Choi convention')
    d=positive(raw.get('input_dimension'),'input dimension');n=positive(raw.get('output_dimension'),'output dimension')
    m=positive(raw.get('outcome_count'),'outcome count');B=positive(raw.get('grid'),'grid')
    ranks=ranks_check(raw.get('rank_bounds'),n,m);v=rank_dimension(n,ranks)
    pivots=raw.get('pivot_sets')
    if not isinstance(pivots,list) or len(pivots)!=m:raise ValueError('invalid pivot-set header')
    for p,r in zip(pivots,ranks):
        if not isinstance(p,list) or any(type(j) is not int or not 0<=j<n for j in p):raise ValueError('invalid pivot position')
        if p!=sorted(set(p)) or len(p)>r:raise ValueError('noncanonical or oversized pivot set')
    coords=list(factor_coordinates(n,pivots));h=len(coords)
    if not 1<=h<=v+1:raise ValueError('empty or oversized factor chart')
    for key,value in [('factor_coordinates',h),('rank_family_dimension',v),('fixed_length_bits',description_bits(n,m,ranks,B))]:
        if type(raw.get(key)) is not int or raw[key]!=value:raise ValueError(key+' mismatch')
    cap=body_capacity(B,h);bits=(cap-1).bit_length();s=raw.get('body_hex')
    if not isinstance(s,str) or not s or len(s)>max(1,(bits+3)//4):raise ValueError('missing or overlong body')
    if any(c not in '0123456789abcdef' for c in s) or (len(s)>1 and s[0]=='0'):raise ValueError('noncanonical hexadecimal body')
    body=int(s,16)
    if body>=cap:raise ValueError('body outside its fixed-length alphabet')
    head,code=divmod(body,(2*B+1)**(h-1));anchor=head//2;sign=-1 if head%2 else 1
    digits=unpack_digits(code,B,h-1);z=digits[:anchor]+[sign*B]+digits[anchor:]
    if not v and (pivots!=[[0] if r else [] for r in ranks] or body!=0):raise ValueError('noncanonical singleton code')
    expected=str(Fraction(16*(h-1),B*B))
    if raw.get('one_use_error_squared_upper')!=expected:raise ValueError('error certificate changed')
    factors=[zero(n) for _ in range(m)]
    for value,(y,i,j,c) in zip(z,coords):
        cell=list(factors[y][i][j]);cell[c]=value;factors[y][i][j]=tuple(cell)
    blocks=[product(A,adjoint(A)) for A in factors]
    T=sum(trace(A) for A in blocks)
    if not B*B<=T<=h*B*B:raise RuntimeError('factor denominator bound failed')
    return lift_blocks(blocks,d,n,T)


def adaptive(target:Instrument,N:int,error:Fraction,ranks:list[int]|None=None)->dict:
    positive(N,'horizon')
    if not isinstance(error,Fraction) or not 0<error<2:raise ValueError('exact rational error in (0,2) required')
    ranks=[target.n]*len(target.outcomes) if ranks is None else ranks_check(ranks,target.n,len(target.outcomes))
    v=rank_dimension(target.n,ranks)
    z=isqrt(N*v)
    if z*z<N*v:z+=1
    t=Fraction(4*z,1)/error;B=max(1,(t.numerator+t.denominator-1)//t.denominator)
    code=encode(target,B,ranks)
    sq=N*Fraction(code['one_use_error_squared_upper'])
    if sq>error*error:raise RuntimeError('adaptive precision selection failed')
    return {'schema':ADAPTIVE_SCHEMA,'horizon':N,'requested_unhalved_error':str(error),
            'error_squared_upper':str(sq),'code':code,
            'scope':'One decoded preparation instrument reused by the same bounded adaptive quantum tester, including references and public stopping; not a physical classical simulator.'}


def validate_adaptive(raw:dict)->Instrument:
    if not isinstance(raw,dict) or raw.get('schema')!=ADAPTIVE_SCHEMA:raise ValueError('invalid adaptive code')
    N=positive(raw.get('horizon'),'horizon');s=raw.get('requested_unhalved_error')
    if not isinstance(s,str):raise ValueError('error must be a canonical rational string')
    err=Fraction(s)
    if str(err)!=s or not 0<err<2:raise ValueError('invalid error interval or representation')
    code=raw.get('code');obj=decode(code)
    sq=N*Fraction(code['one_use_error_squared_upper'])
    if raw.get('error_squared_upper')!=str(sq) or sq>err*err:raise ValueError('adaptive error certificate mismatch')
    return obj


def verify(target:Instrument,raw:dict)->bool:
    try:
        if raw.get('schema')==ADAPTIVE_SCHEMA:
            validate_adaptive(raw)
            expected=adaptive(target,raw['horizon'],Fraction(raw['requested_unhalved_error']),raw['code']['rank_bounds'])
        else:
            decode(raw);expected=encode(target,raw['grid'],raw['rank_bounds'])
        return json.dumps(raw,sort_keys=True)==json.dumps(expected,sort_keys=True)
    except (ValueError,TypeError,KeyError,IndexError,AttributeError,ZeroDivisionError):return False


def main()->None:
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='mode',required=True)
    for mode in ['encode','adaptive','decode','verify']:
        p=sub.add_parser(mode);p.add_argument('--input',type=Path,required=True)
        if mode in ['encode','adaptive']:p.add_argument('--ranks',help='JSON list of public rank bounds')
        if mode=='encode':p.add_argument('--grid',type=int,required=True)
        if mode=='adaptive':p.add_argument('--horizon',type=int,required=True);p.add_argument('--error',required=True)
        if mode=='verify':p.add_argument('--certificate',type=Path,required=True)
    args=ap.parse_args()
    try:
        raw=json.loads(args.input.read_text())
        if args.mode=='decode':
            obj=validate_adaptive(raw) if raw.get('schema')==ADAPTIVE_SCHEMA else decode(raw);out=obj.to_dict()
        else:
            target=Instrument.from_dict(raw)
            if args.mode=='verify':
                cert=json.loads(args.certificate.read_text());ok=verify(target,cert)
                if not ok:raise ValueError('target-bound certificate verification failed')
                out={'status':'success','scope':'Target-bound exact encoder replay; no universal theorem certification.'}
            else:
                ranks=None if args.ranks is None else json.loads(args.ranks)
                out=encode(target,args.grid,ranks) if args.mode=='encode' else adaptive(target,args.horizon,Fraction(args.error),ranks)
        print(json.dumps(out,indent=2,sort_keys=True))
    except (OSError,ValueError,TypeError,KeyError,IndexError) as exc:
        print('preparation codec: '+str(exc),file=sys.stderr);raise SystemExit(2)

if __name__=='__main__':main()
