#!/usr/bin/env python3
"""Exact first-jet support classification for two-sided C2 POVM curves.

The input is a represented first jet, not a physical device or a complete
curve. The certificate is conditional on the stated smooth-curve theorem;
it supplies neither uniform curvature constants nor recovery synthesis.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s
from matrix_metric import (require, strict_keys, positive_integer, gaussian,
                           matrix_from_json, matrix_to_json)
from finite_outcome_certificate import matrix_tuple_legal
from support_geometry import support_data, support

INPUT = 'gtf85.measurement-first-jet/1'
CERT = 'gtf85.curve-certificate/1'


def classify(effects, tangent):
    effects = [e.applyfunc(gaussian) for e in effects]
    tangent = [h.applyfunc(gaussian) for h in tangent]
    require(matrix_tuple_legal(effects, False), 'illegal measurement')
    d = effects[0].rows
    require(len(tangent) == len(effects), 'wrong tangent count')
    for h in tangent:
        require(h.shape == (d, d) and h == h.adjoint(), 'non-Hermitian tangent')
        for value in h:
            gaussian(value)
    require(sum(tangent, s.zeros(d)) == s.zeros(d), 'tangent sum is not zero')
    projections = [support(e) for e in effects]
    missing = [((s.eye(d)-p)*h*(s.eye(d)-p)).applyfunc(gaussian)
               for p,h in zip(projections,tangent)]
    realizable = all(x == s.zeros(d) for x in missing)
    require(realizable, 'first jet is not two-sided positive: missing-support block')
    gamma = (s.I*sum((p*h-h*p for p,h in zip(projections,tangent)), s.zeros(d))/2).applyfunc(gaussian)
    data = support_data(effects, gamma)
    nonzero = any(h != s.zeros(d) for h in tangent)
    regime = ('higher_order_undetermined' if not nonzero else
              ('square_root' if data['in_span'] else 'linear'))
    return {'gamma':gamma, 'projected':data['projected'], 'residual':data['complement'],
            'projections':projections, 'ranks':data['ranks'], 'in_span':data['in_span'],
            'nonzero':nonzero, 'regime':regime, 'kernel_dimension':data['kernel_dimension']}


def parse(raw, max_dimension=256):
    strict_keys(raw, {'schema','dimension','outcomes','effects','tangent'}, 'curve input')
    require(raw['schema'] == INPUT, 'wrong curve schema')
    d=positive_integer(raw['dimension'],'dimension')
    k=positive_integer(raw['outcomes'],'outcomes')
    cap=positive_integer(max_dimension,'maximum system dimension')
    require(k>=2 and (k-1)*d*d<=cap, 'resource cap exceeded: no classification produced')
    require(type(raw['effects']) is list and len(raw['effects'])==k, 'wrong effect count')
    require(type(raw['tangent']) is list and len(raw['tangent'])==k, 'wrong tangent count')
    e=[matrix_from_json(x,d,'effect') for x in raw['effects']]
    h=[matrix_from_json(x,d,'tangent') for x in raw['tangent']]
    return e,h


def certify(raw, max_dimension=256):
    e,h=parse(raw,max_dimension); c=classify(e,h)
    return {'schema':CERT, 'status':'success', 'input_sha256':hashlib.sha256(
        json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'dimension':e[0].rows,'outcomes':len(e),'support_ranks':c['ranks'],
        'support_projections':[matrix_to_json(p) for p in c['projections']],
        'two_sided_first_order_realizable':True,'tangent_nonzero':c['nonzero'],
        'support_generator':matrix_to_json(c['gamma']),
        'generator_projection':matrix_to_json(c['projected']),
        'generator_residual':matrix_to_json(c['residual']),
        'tangent_in_covariance_range':c['in_span'],
        'finite_use_regime':c['regime'],'covariance_kernel_dimension':c['kernel_dimension'],
        'theorem':'thm:curveclassification85' if c['nonzero'] else None,
        'scope':'each fixed two-sided C2 measurement curve with this nonzero first jet',
        'uniform_constants_across_curves':False,'curvature_bound_computed':False,
        'stationarity_inferred_from_zero_tangent':False,
        'exact_adaptive_distance_claimed':False,'recovery_synthesized':False,
        'physical_protocol_executed':False,'continuum_proof_by_replay':False}


def verify(raw, certificate, max_dimension=256):
    require(type(certificate) is dict and certificate == certify(raw,max_dimension),
            'curve certificate differs from complete exact reconstruction')
    return {'schema':'gtf85.curve-verification/1','status':'success','exact_replay':True,
            'physical_protocol_executed':False,'continuum_proof_by_replay':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('--verify',type=Path)
    p.add_argument('--max-system-dimension',type=int,default=256);a=p.parse_args()
    try:
        raw=json.loads(a.input.read_text())
        result=verify(raw,json.loads(a.verify.read_text()),a.max_system_dimension) if a.verify else certify(raw,a.max_system_dimension)
        print(json.dumps(result,indent=2,sort_keys=True))
    except (ValueError,TypeError,KeyError,OSError,RuntimeError) as error:
        p.exit(2,'curve geometry: '+str(error)+'\n')

if __name__=='__main__':main()
