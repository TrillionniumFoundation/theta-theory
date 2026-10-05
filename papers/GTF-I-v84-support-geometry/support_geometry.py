#!/usr/bin/env python3
"""Exact support-span decisions and transported-ridge energies.

A certificate classifies a *known* unitary orbit under the written finite-angle
theorem. It does not compute adaptive distance, synthesize recovery, or execute
an unknown-device learner. Gaussian-rational input is required, with exact rank
and positivity tests and explicit resource-cap rejection.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s
from matrix_metric import (require,strict_keys,positive_integer,gaussian,
 matrix_from_json,matrix_to_json,gaussian_parts)
from finite_outcome_certificate import matrix_tuple_legal
from covariance_metric import tangent_basis,inner,covariance,system

INPUT='gtf84.support-orbit/1'
CERT='gtf84.support-certificate/1'


def hermitian_basis(d: int):
    return [v[0] for v in tangent_basis(d,2)]


def real_coordinates(x):
    """Injective real coordinates, used only for rank, not metric projection."""
    require(x.rows==x.cols and x==x.adjoint(),'matrix is not Hermitian')
    result=[gaussian_parts(x[i,i])[0] for i in range(x.rows)]
    for i in range(x.rows):
        for j in range(i+1,x.rows):
            result.extend(gaussian_parts(x[i,j]))
    return s.Matrix(result)


def support(e):
    require(e.rows==e.cols and e==e.adjoint(),'invalid effect')
    columns=e.columnspace()
    if not columns:return s.zeros(e.rows)
    v=s.Matrix.hstack(*columns)
    p=(v*(v.adjoint()*v).inv(method='DM')*v.adjoint()).applyfunc(gaussian)
    require(p==p.adjoint() and p*p==p and p*e==e,'invalid support projector')
    return p


def support_data(effects,generator):
    require(matrix_tuple_legal(effects,False),'illegal normalized measurement')
    d=effects[0].rows;k=len(effects)
    require(generator.shape==(d,d) and generator==generator.adjoint(),'invalid generator')
    for value in generator:gaussian_parts(value)
    projections=[support(e) for e in effects]
    candidates=[(p*b*p).applyfunc(gaussian) for p in projections for b in hermitian_basis(d)]
    coord=s.Matrix.hstack(*[real_coordinates(b) for b in candidates])
    pivots=coord.rref()[1];basis=[candidates[i] for i in pivots]
    gram=s.Matrix([[s.trace(a*b) for b in basis] for a in basis])
    rhs=s.Matrix([s.trace(a*generator) for a in basis])
    c=gram.inv(method='DM')*rhs
    projected=sum((c[i]*basis[i] for i in range(len(basis))),s.zeros(d)).applyfunc(gaussian)
    complement=(generator-projected).applyfunc(gaussian)
    require(all(p*complement*p==s.zeros(d) for p in projections),'projection residual not orthogonal')
    stationary=all(generator*e==e*generator for e in effects)
    in_span=complement==s.zeros(d)
    require(not stationary or in_span,'stationary/support classification inconsistent')
    ranks=[int(s.trace(p)) for p in projections]
    dimension=d*d-len(basis)+sum((d-r)**2 for r in ranks)
    return {'projections':projections,'ranks':ranks,'basis':basis,'gram':gram,
      'coordinates':c,'projected':projected,'complement':complement,
      'kernel_dimension':dimension,'in_span':in_span,'stationary':stationary,
      'regime':'stationary' if stationary else ('square_root' if in_span else 'linear')}


def transported_energy(effects,weights,tangent,tau):
    """Exact extended energy: None means +infinity off the operator range."""
    d=effects[0].rows;k=len(effects)
    require(len(weights)==k and all(s.sympify(w).is_Rational and w>=0 for w in weights)
            and sum(weights)==1,'invalid public probability weights')
    tau=s.Rational(tau);require(tau>0,'ridge parameter must be positive')
    require(len(tangent)==k and sum(tangent,s.zeros(d))==s.zeros(d),'nonzero-sum tangent')
    basis,gram,stiffness=system(effects)
    scalar=[w*s.eye(d) for w in weights]
    weighted=s.Matrix([[inner(a,covariance(scalar,b)) for b in basis] for a in basis])
    coefficient=stiffness+tau*weighted
    rhs=s.Matrix([inner(a,tangent) for a in basis])
    if coefficient.row_join(rhs).rank()!=coefficient.rank():return None
    solution,parameters=coefficient.gauss_jordan_solve(rhs)
    solution=solution.subs({p:0 for p in parameters})
    value=s.factor((rhs.T*solution)[0])
    require(value.is_Rational and value>=0,'invalid extended energy')
    return value


def parse(raw,max_dimension=256):
    strict_keys(raw,{'schema','dimension','outcomes','effects','generator'},'support input')
    require(raw['schema']==INPUT,'wrong support input schema')
    d=positive_integer(raw['dimension'],'dimension');k=positive_integer(raw['outcomes'],'outcomes')
    cap=positive_integer(max_dimension,'maximum system dimension')
    require(k>=2 and (k-1)*d*d<=cap,'resource cap exceeded: no certificate produced')
    require(type(raw['effects']) is list and len(raw['effects'])==k,'wrong effect count')
    e=[matrix_from_json(x,d,'effect') for x in raw['effects']]
    g=matrix_from_json(raw['generator'],d,'generator')
    require(matrix_tuple_legal(e,False),'illegal or unnormalized measurement')
    return e,g


def certify(raw,max_dimension=256):
    e,g=parse(raw,max_dimension);a=support_data(e,g)
    return {'schema':CERT,'status':'success','input_sha256':hashlib.sha256(
      json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
      'dimension':g.rows,'outcomes':len(e),'support_ranks':a['ranks'],
      'support_projections':[matrix_to_json(p) for p in a['projections']],
      'support_span_dimension':len(a['basis']),'covariance_kernel_dimension':a['kernel_dimension'],
      'generator_projection':matrix_to_json(a['projected']),
      'generator_complement':matrix_to_json(a['complement']),
      'generator_in_support_span':a['in_span'],'orbit_stationary':a['stationary'],
      'finite_angle_regime':a['regime'],'theorem':'thm:orbittrichotomy84',
      'range':'fixed effects and generator; all N>=1, sufficiently small angle',
      'uniform_constants_across_measurements':False,
      'known_pair_only':True,'exact_rank_tests':True,
      'physical_protocol_executed':False,'recovery_synthesized':False,
      'exact_adaptive_distance_claimed':False,'continuum_proof_by_replay':False}


def verify(raw,certificate,max_dimension=256):
    require(type(certificate) is dict,'certificate must be an object')
    require(certificate==certify(raw,max_dimension),'support certificate differs from exact reconstruction')
    return {'schema':'gtf84.support-verification/1','status':'success','exact_replay':True,
            'physical_protocol_executed':False,'continuum_proof_by_replay':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path)
    p.add_argument('--verify',type=Path);p.add_argument('--max-system-dimension',type=int,default=256)
    a=p.parse_args()
    try:
        raw=json.loads(a.input.read_text());result=(verify(raw,json.loads(a.verify.read_text()),
            a.max_system_dimension) if a.verify else certify(raw,a.max_system_dimension))
        print(json.dumps(result,indent=2,sort_keys=True))
    except (ValueError,TypeError,KeyError,OSError,RuntimeError) as error:
        p.exit(2,'support geometry: '+str(error)+'\n')

if __name__=='__main__':main()
