#!/usr/bin/env python3
"""Exact closed-POVM upper certificates and search-free balanced legalization.

Implements the rational covariance system of thm:closedcovariance83 and the
explicit map thm:affinerepair83. An upper certificate is not the adaptive
optimum. No physical unknown-device learner is executed by this module.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence
import sympy as s
from matrix_metric import (require, strict_keys, positive_integer, rational,
    matrix_from_json, matrix_to_json, gaussian, gaussian_parts,
    is_positive_semidefinite as psd)
from finite_outcome_certificate import matrix_tuple_legal

PAIR='gtf83.closed-povm-pair/1'
CERT='gtf83.covariance-upper/1'


def inner(a, b):
    require(len(a)==len(b) and len(a)>0,'incompatible tuple inner product')
    value=s.expand(sum(s.trace(x*y) for x,y in zip(a,b)))
    real,imag=gaussian_parts(value)
    require(imag==0,'nonreal Hermitian inner product')
    return real


def covariance(effects: Sequence[s.MatrixBase], values: Sequence[s.MatrixBase]):
    require(matrix_tuple_legal(effects,False),'effects are not a normalized legal POVM')
    d=effects[0].rows
    require(len(values)==len(effects) and all(x.shape==(d,d) and x==x.adjoint()
            for x in values),'invalid Hermitian tuple')
    for x in values:
        for a in x:gaussian_parts(a)
    total=sum((e*x for e,x in zip(effects,values)),s.zeros(d))
    return [((e*x+x*e-e*total-total.adjoint()*e)/2).applyfunc(gaussian)
            for e,x in zip(effects,values)]


def tangent_basis(d: int,k: int):
    positive_integer(d,'dimension');positive_integer(k,'outcomes')
    require(k>=2,'at least two outcomes required')
    matrices=[]
    for i in range(d):
        x=s.zeros(d);x[i,i]=1;matrices.append(x)
    for i in range(d):
        for j in range(i+1,d):
            x=s.zeros(d);x[i,j]=x[j,i]=1;matrices.append(x)
            x=s.zeros(d);x[i,j]=s.I;x[j,i]=-s.I;matrices.append(x)
    basis=[]
    for j in range(k-1):
        for a in matrices:
            row=[s.zeros(d) for _ in range(k)];row[j]=a;row[-1]=-a;basis.append(row)
    return basis


def system(effects):
    require(matrix_tuple_legal(effects,False),'not a normalized legal POVM')
    basis=tangent_basis(effects[0].rows,len(effects))
    images=[covariance(effects,b) for b in basis]
    gram=s.Matrix([[inner(a,b) for b in basis] for a in basis])
    stiffness=s.Matrix([[inner(a,c) for c in images] for a in basis])
    require(stiffness==stiffness.T and psd(stiffness),'covariance positivity or symmetry failed')
    return basis,gram,stiffness


def solve(effects,tangent,horizon: int):
    n=positive_integer(horizon,'horizon');d=effects[0].rows
    require(len(tangent)==len(effects) and sum(tangent,s.zeros(d))==s.zeros(d),
            'tangent normalization is not zero')
    basis,gram,stiffness=system(effects)
    rhs=s.Matrix([inner(a,tangent) for a in basis])
    coefficient=stiffness+gram/n
    coordinates=coefficient.inv(method='DM')*rhs
    k=[sum((coordinates[i]*basis[i][j] for i in range(len(basis))),s.zeros(d))
       .applyfunc(gaussian) for j in range(len(effects))]
    residual=[(c+x/n-h).applyfunc(gaussian)
              for c,x,h in zip(covariance(effects,k),k,tangent)]
    require(all(x==s.zeros(d) for x in residual),'nonzero exact covariance residual')
    q=s.factor(n*(rhs.T*coordinates)[0])
    require(q.is_Rational and q>=0,'invalid squared modulus')
    return q,k,gram,stiffness


def parse(raw: dict,max_system_dimension: int=256):
    strict_keys(raw,{'schema','dimension','outcomes','effects_e','effects_f'},'pair')
    require(raw['schema']==PAIR,'wrong input schema')
    d=positive_integer(raw['dimension'],'dimension');k=positive_integer(raw['outcomes'],'outcomes')
    positive_integer(max_system_dimension,'maximum system dimension')
    require(k>=2 and (k-1)*d*d<=max_system_dimension,
            'invalid alphabet or resource limit: no certificate was constructed')
    arrays=[]
    for name in ('effects_e','effects_f'):
        require(type(raw[name]) is list and len(raw[name])==k,'wrong number of effects')
        array=[matrix_from_json(x,d,name) for x in raw[name]]
        require(matrix_tuple_legal(array,False),'illegal or unnormalized POVM: '+name)
        arrays.append(array)
    return arrays


def certify(raw: dict,horizon: int,max_system_dimension: int=256):
    n=positive_integer(horizon,'horizon'); e,f=parse(raw,max_system_dimension)
    mid=[(a+b)/2 for a,b in zip(e,f)]; h=[b-a for a,b in zip(e,f)]
    q,k,gram,stiffness=solve(mid,h,n)
    encoded=json.dumps(raw,sort_keys=True,separators=(',',':')).encode()
    return {'schema':CERT,'status':'success','dimension':e[0].rows,'outcomes':len(e),
      'horizon':n,'pair_sha256':hashlib.sha256(encoded).hexdigest(),
      'system_dimension':gram.rows,'q_squared':str(q),
      'adaptive_upper_squared':str(min(s.Rational(4),4*(len(e)+1)*q)),
      'solution':[matrix_to_json(x) for x in k],
      'theorem':'thm:closedcovariance83','gram_matrix_included':True,
      'normalization':'unhalved final-state trace norm',
      'rank_or_support_restriction':False,'exact_adaptive_distance_claimed':False,
      'physical_learner_executed':False,'continuum_theorem_proved_by_replay':False}


def verify(raw: dict,certificate: dict,max_system_dimension: int=256,
           expected_horizon: int | None=None):
    require(type(certificate) is dict and 'horizon' in certificate,'invalid certificate')
    if expected_horizon is not None:
        require(certificate['horizon']==positive_integer(expected_horizon,'expected horizon'),
                'certificate horizon differs from the requested horizon')
    expected=certify(raw,certificate['horizon'],max_system_dimension)
    require(certificate==expected,'certificate differs from complete exact replay')
    return {'schema':'gtf83.covariance-replay/1','status':'success',
            'complete_exact_replay':True,'pair_sha256':expected['pair_sha256'],
            'q_squared':expected['q_squared'],'theorem':expected['theorem']}


def affine_repair(raw: Sequence[s.MatrixBase], accuracy: s.Rational):
    require(len(raw)>=2,'invalid alphabet')
    require(getattr(accuracy,'is_Rational',False) is True and accuracy>0,
            'accuracy must be a positive exact rational')
    d=raw[0].rows;k=len(raw)
    require(d>0 and all(a.shape==(d,d) and a==a.adjoint() for a in raw),
            'raw estimates must be nonempty Hermitian matrices')
    for a in raw:
        for v in a:gaussian_parts(v)
    correction=(s.eye(d)-sum(raw,s.zeros(d)))/k
    out=[((a+correction+4*accuracy*s.eye(d))/(1+4*k*accuracy)).applyfunc(gaussian)
         for a in raw]
    if matrix_tuple_legal(out,True):return out,False
    return [s.eye(d)/k for _ in range(k)],True


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('pair',type=Path);p.add_argument('--horizon',type=int,default=None)
    p.add_argument('--verify',type=Path);p.add_argument('--max-system-dimension',type=int,default=256)
    a=p.parse_args()
    try:
        raw=json.loads(a.pair.read_text())
        result=(verify(raw,json.loads(a.verify.read_text()),a.max_system_dimension,a.horizon)
                if a.verify else certify(raw,1 if a.horizon is None else a.horizon,a.max_system_dimension))
    except (ValueError,OSError,TypeError,json.JSONDecodeError) as e:
        p.exit(2,str(e)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
