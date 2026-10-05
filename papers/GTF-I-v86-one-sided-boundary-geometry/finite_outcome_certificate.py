#!/usr/bin/env python3
"""Exact finite-alphabet risk certificates, Theorem multicertificate82.

Complete scalar tuple grids are supported for executable certificates. General
matrix legality, tuple distances, tensor record probabilities and readout tests
are exact reusable kernels. No matrix-grid prefix is accepted as a certificate.
This code does not run a physical learner or infer continuum risk from samples.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path
from typing import Sequence
import sympy as sp
from matrix_metric import is_positive_semidefinite as psd, gaussian_parts


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def integer(x, name: str) -> int:
    require(type(x) is int and x >= 1, name+' must be a positive integer')
    return x


def rational(x, name: str) -> F:
    require(type(x) is str, name+' must be a canonical rational string')
    try:
        v=F(x)
    except (ValueError, ZeroDivisionError) as e:
        raise ValueError(name+' is not rational') from e
    require(str(v)==x, name+' must be canonical')
    return v


def grid_denominator(d: int, k: int, radius: F) -> int:
    integer(d,'dimension'); integer(k,'outcomes')
    require(k>=2 and 0<radius<=F(1,8*k), 'invalid grid radius or alphabet')
    return math.ceil(max(F(4*(k-1)*d,1)/radius, F(8*k*(k-1)*d)))


def matrix_tuple_legal(effects: Sequence[sp.MatrixBase], balanced=True) -> bool:
    if len(effects)<2 or not effects or effects[0].rows<1:
        return False
    d=effects[0].rows; k=len(effects); identity=sp.eye(d)
    if any(a.shape!=(d,d) or a!=a.adjoint() for a in effects):
        return False
    if sum(effects,sp.zeros(d))!=identity:
        return False
    lo,hi=(sp.Rational(1,2*k),sp.Rational(3,2*k)) if balanced else (0,1)
    return all(psd(a-lo*identity) and psd(hi*identity-a) for a in effects)


def matrix_tuple_within(a, b, radius: F) -> bool:
    require(len(a)==len(b)>=2, 'different or invalid alphabets')
    require(radius>=0, 'negative norm radius')
    d=a[0].rows; t=sp.Rational(radius.numerator,radius.denominator)
    require(all(x.shape==y.shape==(d,d) and x==x.adjoint() and y==y.adjoint()
                for x,y in zip(a,b)), 'invalid Hermitian tuple dimensions')
    return all(psd(t*sp.eye(d)+(x-y)) and psd(t*sp.eye(d)-(x-y))
               for x,y in zip(a,b))


def matrix_record(effects, string):
    """Subnormalized conditional Choi record in the input-first convention."""
    require(matrix_tuple_legal(effects,False), 'not a complete legal POVM')
    d=effects[0].rows
    require(all(type(x) is int and 0<=x<len(effects) for x in string), 'invalid label')
    out=sp.ones(1,1)
    for x in string:
        out=sp.kronecker_product(out,effects[x].T/d)
    return out


def check_readout(readout, outcomes: int, calls: int, reference_dimension: int):
    """Reject missing strings, incomplete POVMs, negatives and nonrational entries."""
    strings=set(product(range(outcomes),repeat=calls))
    require(set(readout)==strings, 'the complete classical string set is required')
    sizes={len(readout[x]) for x in strings}
    require(len(sizes)==1 and next(iter(sizes))>=1, 'inconsistent output alphabet')
    for x in strings:
        effects=readout[x]
        require(all(a.shape==(reference_dimension,reference_dimension) and a==a.adjoint()
                    for a in effects), 'wrong readout dimension or Hermiticity')
        for a in effects:
            for entry in a:
                gaussian_parts(entry)
            require(psd(a), 'readout has a negative effect')
        require(sum(effects,sp.zeros(reference_dimension))==sp.eye(reference_dimension),
                'readout is not a complete POVM')


def scalar_grid(k: int, radius: F, max_candidates: int):
    """Reconstruct the complete grid. Spectral diagonal pruning is exact in d=1."""
    K=grid_denominator(1,k,radius)
    lo=math.ceil(F(K,2*k)); hi=math.floor(F(3*K,2*k))
    candidates=(hi-lo+1)**(k-1)
    require(candidates<=max_candidates,
            'incomplete construction: candidate budget is below the complete pruned grid')
    points=[]
    for prefix in product(range(lo,hi+1), repeat=k-1):
        last=K-sum(prefix)
        if lo<=last<=hi:
            points.append(tuple(F(x,K) for x in (*prefix,last)))
    require(points, 'empty grid')
    return K,candidates,points


def verify_scalar(raw: dict, max_candidates=200000):
    fields={'schema','dimension','outcomes','calls','net_radius','good_radius',
            'failure_bound','centres','readout'}
    require(type(raw) is dict and set(raw)==fields, 'missing or additional certificate fields')
    require(raw['schema']=='gtf82.scalar-finite-risk/1' and type(raw['dimension']) is int and raw['dimension']==1,
            'this complete-certificate interface supports scalar tuples only')
    k=integer(raw['outcomes'],'outcomes'); m=integer(raw['calls'],'calls')
    radius=rational(raw['net_radius'],'net radius'); a=rational(raw['good_radius'],'good radius')
    alpha=rational(raw['failure_bound'],'failure bound')
    require(a>=0 and 0<=alpha<1,'invalid risk parameters')
    require(type(raw['centres']) is list and raw['centres'],'missing centres')
    centres=[]
    for row in raw['centres']:
        require(type(row) is list and len(row)==k,'invalid centre dimension')
        c=tuple(rational(x,'centre coordinate') for x in row)
        require(sum(c)==1 and all(F(1,2*k)<=x<=F(3,2*k) for x in c),
                'centre is not a complete balanced POVM')
        centres.append(c)
    require(k**m<=max_candidates, 'incomplete construction: classical string budget exceeded')
    strings=list(product(range(k),repeat=m))
    expected={','.join(map(str,x)) for x in strings}
    table=raw['readout'];require(type(table) is dict and set(table)==expected,
                               'complete classical record list required')
    probabilities={}
    for x in strings:
        row=table[','.join(map(str,x))]
        require(type(row) is list and len(row)==len(centres),'wrong output alphabet')
        p=tuple(rational(v,'readout probability') for v in row)
        require(all(v>=0 for v in p) and sum(p)==1,'readout is not a complete positive POVM')
        probabilities[x]=p
    K,count,points=scalar_grid(k,radius,max_candidates)
    worst=F(0); argmax=None
    for g in points:
        bad=[j for j,c in enumerate(centres) if max(abs(x-y) for x,y in zip(g,c))>a]
        risk=F(0)
        for x in strings:
            probability=math.prod(g[i] for i in x)
            risk+=probability*sum(probabilities[x][j] for j in bad)
        if risk>worst:
            worst=risk;argmax=g
        require(risk<=alpha,'finite risk inequality failed at '+str(g))
    return {'schema':'gtf82.scalar-finite-risk-replay/1','status':'success',
            'dimension':1,'outcomes':k,'calls':m,'denominator':K,
            'complete_grid':True,'complete_readout':True,'pruned_candidates':count,
            'legal_grid_points':len(points),'classical_strings':len(strings),
            'maximum_grid_failure':str(worst),'grid_failure_allowance':str(alpha),
            'witness':None if argmax is None else list(map(str,argmax)),
            'continuum_radius':str(a+radius),
            'continuum_failure_allowance':str(alpha+F(m*k,2)*radius),
            'continuum_transfer_theorem':'thm:multicertificate82',
            'physical_device_executed':False,'general_matrix_grid_executed':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',type=Path)
    parser.add_argument('--max-grid-candidates',type=int,default=200000)
    args=parser.parse_args()
    try:
        result=verify_scalar(json.loads(args.certificate.read_text()),args.max_grid_candidates)
    except (ValueError,OSError,json.JSONDecodeError) as e:
        parser.exit(2,str(e)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
